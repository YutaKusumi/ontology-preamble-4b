# -*- coding: utf-8 -*-
"""bl3_recompute_rewrite.py v1 —— B-lens 層三（Bl3）の独立の再計算の器のうち、**残差の書き換えの道**
（2026-09-25・本の器の書き手〔コーディネータ〕と別の系統内の個体が書いた・登録者の許可による・独立の目を通っていない）。

正本 `design/contrasts-Bl3.json` の `independent_recompute`（一段目の相手）・`readout.primary`・`layers`・`computation` に従う。
コーディネータのフックの道（`tools/bl3_run.py`）の中身を**読まずに**書いた。`--dry` でだけ、その公開の関数を中を見ずに呼び、数を突き合わせる。

道（加減をフックでなく、選んだ層の出力を書き換えて後の層を流す・近道なし・バッチ一）:
  入力     段階 B の組み立てのままのプロンプト（`steer_B.apply_chat(tok, run_stageB_local.user_message(腕の本文, 場面の本文, 指示))`・
           場面と指示は `run_stageB_local.scenario_and_instruction`）の直後に、主の書き出し（転記行 A の `prefix_ids`）を
           **トークンの並びのまま**つなぐ。升目ごとに、プロンプトの長さ・主位置（`steer_B.main_position`）・読み取りの位置（列の最後）・
           族・前置きの SHA16 を転記行 B の升目の記録と照らし、違えば止める。
  層を回す 埋め込み → 層 0〜L → 層 L の出力を書き換え → 層 L+1〜最後。層の部品は、模型の forward（transformers 4.57.3 の
           `Qwen3Model.forward`）と同じ引数で一つずつ呼ぶ。L＝`direction_B.layer_index(layers.selected_ratio, 模型の層の数)`（本物の模型では正本 `layers.indices` の値）。
           位置の埋め込み（rotary）は模型の `rotary_emb` を、因果の注意の窓（mask）は模型の組み立てと同じ関数（`create_causal_mask`・
           窓つきの層があれば `create_sliding_window_causal_mask`）を、模型の forward と同じ引数で呼ぶ。`use_cache` の既定も模型の forward と同じ
           `config.use_cache` で、そのときは一回の順伝播ごとに空の cache を作って捨てる（順伝播をまたいで使い回さない＝近道ではない）。
  書き換え 層 L の出力の、主位置から列の最後までの位置に `sign × coef × v` を足す。v（float64）は段階 B の走行器のフックと同じ算術で、
           NumPy の float32 を経て層の出力の型（bf16）に直してから `sign * coef *` を掛け、bf16 のまま足す（係数は一度だけ）。
  読み取り 最後の層の出口の残差（**最終の正規化の入力**。transformers 4.57.3 の `hidden_states[-1]` は正規化の後の値なので使わない）の
           最後の位置を float32 に上げ、最終の正規化を float32 で当て（h × rsqrt(mean(h²)+eps) × g・g は `model.model.norm.weight` の float32）、
           語彙の行列（`lm_head.weight`）の読み取りの集合の行（族の選択の文字の順で a が先頭・最後に refuse の頭）を float32 で当てる。
           量＝z_a − logsumexp（ほかの選択の文字と refuse の頭）。効き目＝加えた値 − 無操作（零のベクトル）の値。
出力: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}（符号の書き方は '%+d'）。
**値は印字しない**（正本 `independent_recompute.print`——本物の模型の値を開くのは登録者と一緒に開いた後）。`--dry` が差の最大を印字するのは乱数の小さな模型だけ。
**フックは使わない**: 呼ぶ前と後に、模型のどの部品にも forward の hook（前・後・大域）が無いことを確かめ、あれば止める（フックの道の掛け残しも混ぜない）。
用法: python tools/bl3_recompute_rewrite.py --selftest   （乱数の小さな模型で自己検査）
      python tools/bl3_recompute_rewrite.py --dry        （乱数の小さな模型で、フックの道と一段目の許容で突き合わせ、差の最大を印字する。
                                                          参考に、この道をわざと誤らせた歯の変種がフックの道との差で捕まるかも印字する——判定に入れない）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, time, copy, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

VERSION = 'v1'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON_PATH = os.path.join(REPO, 'design', 'contrasts-Bl3.json')
FACTS_PATH = os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json')
# トークナイザと設定の置き場（手元・**実の重みは読まない**——乱数の小さな模型は設定だけを借りて作る）
SNAP = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub', 'models--Qwen--Qwen3-4B-Instruct-2507',
                    'snapshots', 'cdbee75f17c01a7cc42f958dc650907174af0554')
TINY = {'hidden_size': 64, 'num_hidden_layers': 4, 'num_attention_heads': 4, 'num_key_value_heads': 2,
        'head_dim': 16, 'intermediate_size': 128}
NORM_REL_TOL = 1e-6      # 方向のノルムを ‖static‖ と照らす相対の許容（段階 B の `load_directions` と同じ値）
FENCE = '本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def _die(msg):
    raise SystemExit('bl3_recompute_rewrite: ' + msg)


def load_canon():
    return json.load(open(CANON_PATH, encoding='utf-8'))


def load_facts():
    return json.load(open(FACTS_PATH, encoding='utf-8'))


def _facts(FJ):
    """設計事実は、ファイルの全体（'facts' の鍵を持つ）でも、その 'facts' の中身でも受ける（正本は FJ の形を決めていない）。"""
    return FJ['facts'] if isinstance(FJ, dict) and 'facts' in FJ else FJ


# ---------------------------------------------------------------- 確かめ（止める）

def check_env(model, T3):
    """版と機種の確かめ。手回しの道は transformers 4.57.3 の `Qwen3Model.forward` を写しているので、版が違えば止める。"""
    import transformers
    want = str(T3['inputs']['versions_B']['transformers'])
    if transformers.__version__ != want:
        _die('transformers の版が %s（手回しの道は %s の Qwen3Model.forward を写した・正本 inputs.versions_B）'
             % (transformers.__version__, want))
    core = getattr(model, 'model', None)
    if core is None or type(core).__name__ != 'Qwen3Model':
        _die('模型の本体が Qwen3Model でない: %s' % type(core).__name__)
    if getattr(model, 'lm_head', None) is None:
        _die('語彙の行列（lm_head）が無い')
    if model.training:
        _die('模型が訓練の形（eval にしていない）')
    import torch
    if core.embed_tokens.weight.dtype != torch.bfloat16:
        _die('模型の型が bf16 でない（%s・正本 readout.primary.precision——順伝播と加減は段階 B と同じ bf16）'
             % core.embed_tokens.weight.dtype)
    eps = float(core.norm.variance_epsilon)
    if eps != float(model.config.rms_norm_eps):
        _die('最終の正規化の eps（%r）が設定の rms_norm_eps（%r）と違う' % (eps, model.config.rms_norm_eps))
    n = len(core.layers)
    if n != int(model.config.num_hidden_layers):
        _die('層の並びの数（%d）が設定の層の数（%d）と違う' % (n, model.config.num_hidden_layers))


def assert_no_forward_hooks(model):
    """模型のどの部品にも forward の hook（前・後）が無く、大域の hook も無いこと（残差の書き換えの道はフックを使わない）。"""
    import torch.nn.modules.module as M
    bad = []
    for name, m in model.named_modules():
        for attr in ('_forward_hooks', '_forward_pre_hooks'):
            d = getattr(m, attr, None)
            if d:
                bad.append('%s.%s %d 本' % (name or '<模型>', attr, len(d)))
    for attr in ('_global_forward_hooks', '_global_forward_pre_hooks'):
        d = getattr(M, attr, None)
        if d:
            bad.append('大域の %s %d 本' % (attr, len(d)))
    if bad:
        _die('模型に forward の hook が掛かっている（残差の書き換えの道はフックを使わず、掛け残しも混ぜない）: ' + '・'.join(bad))


def check_layer_and_coef(model, T3, layer_idx, coef):
    """層の添字＝`direction_B.layer_index(layers.selected_ratio, 模型の層の数)`、係数＝`layers.coef_applied`。違えば止める。"""
    import direction_B
    n_layers = len(direction_B.decoder_layers(model))
    ratio = float(T3['layers']['selected_ratio'])
    want = direction_B.layer_index(ratio, n_layers)
    if int(layer_idx) != want:
        _die('層の添字 %s が正本の規則と違う（層の割合 %s・層の数 %d なら %d）' % (layer_idx, ratio, n_layers, want))
    if n_layers == int(T3['inputs']['model']['num_hidden_layers']):
        keyed = {float(k): int(v) for k, v in T3['layers']['indices'].items()}
        if keyed.get(ratio) != int(layer_idx):
            _die('層の添字 %s が正本 layers.indices（%s）と違う' % (layer_idx, keyed.get(ratio)))
    if float(coef) != float(T3['layers']['coef_applied']):
        _die('係数 %r が正本 layers.coef_applied（%r）と違う' % (coef, T3['layers']['coef_applied']))


# ---------------------------------------------------------------- 升目の入力（段階 B の組み立てのまま）

def cell_input(tok, T3, FJ, cell_key, _AT=None):
    """升目（'場面|土台の腕'）の入力を組み立て、転記行 B の升目の記録と照らす（違えば止める）。

    返り値: {'cell', 'ids'（プロンプト＋主の書き出し）, 'prompt_len', 'mp'（主位置）, 'ro'（読み取りの位置＝列の最後）,
             'family', 'letters', 'read_ids'（族の選択の文字の順・a が先頭・最後に refuse の頭）}。"""
    import run_stageB_local as RB
    import steer_B
    F = _facts(FJ)
    cells = F['B']['cells']
    if cell_key not in cells:
        _die('升目 %s が転記行 B（facts.B.cells）に無い' % cell_key)
    cf = cells[cell_key]
    parts = cell_key.split('|')
    if len(parts) != 2:
        _die('升目の鍵の形が違う（場面|土台の腕）: %s' % cell_key)
    scen, base = parts
    s, inst = RB.scenario_and_instruction(scen)
    AT = _AT if _AT is not None else RB.arm_texts()
    if base not in AT:
        _die('土台の腕 %s の本文が引けない' % base)
    prompt = list(steer_B.apply_chat(tok, RB.user_message(AT[base]['text'], s['text'], inst)))
    prefix = [int(x) for x in F['A']['prefix_ids']]
    ids = prompt + prefix
    mp = int(steer_B.main_position(prompt))
    ro = len(ids) - 1
    fam = s.get('family')
    RP = T3['readout']['primary']
    bad = []
    if len(prompt) != int(cf['prompt_len']):
        bad.append('プロンプトの長さ %d（転記 %s）' % (len(prompt), cf['prompt_len']))
    if mp != int(cf['main_position']) or mp != len(prompt) - 1:
        bad.append('主位置 %d（転記 %s・プロンプトの長さ−1 は %d）' % (mp, cf['main_position'], len(prompt) - 1))
    if ro != int(cf['readout_position']):
        bad.append('読み取りの位置 %d（転記 %s）' % (ro, cf['readout_position']))
    if fam != cf.get('family'):
        bad.append('族 %s（転記 %s）' % (fam, cf.get('family')))
    if cf.get('preamble_sha16') and AT[base].get('sha16') != cf['preamble_sha16']:
        bad.append('前置きの SHA16 %s（転記 %s）' % (AT[base].get('sha16'), cf['preamble_sha16']))
    if tok.decode(prefix) != F['A']['prefix']:
        bad.append('主の書き出しの並びが転記の文字列に戻らない')
    if fam not in RP['letters']:
        bad.append('族 %s の選択の文字が正本に無い' % fam)
    if bad:
        _die('升目 %s の入力が転記行 B と違う: %s' % (cell_key, '・'.join(bad)))
    letters = list(RP['letters'][fam])
    if letters[0] != RP['catastrophe_letter']:
        _die('選択の文字の先頭が破局の側の文字（%s）でない: %s' % (RP['catastrophe_letter'], letters))
    LI = F['A']['letter_ids']
    read_ids = [int(LI[x]) for x in letters] + [int(LI['refuse'])]
    want_tokens = letters + [RP['refuse_head']]
    got_tokens = [tok.convert_ids_to_tokens(i) for i in read_ids]
    if got_tokens != want_tokens:
        _die('読み取りの集合のトークンが文字に戻らない: %s 対 %s' % (got_tokens, want_tokens))
    if len(set(read_ids)) != len(read_ids):
        _die('読み取りの集合のトークンが重なる: %s' % read_ids)
    return {'cell': cell_key, 'ids': ids, 'prompt_len': len(prompt), 'mp': mp, 'ro': ro,
            'family': fam, 'letters': letters, 'read_ids': read_ids}


# ---------------------------------------------------------------- 残差の書き換えの道

def forward_rewrite(model, ids, layer_idx, vec, coef, sign, mp, use_cache=None, keep=None):
    """埋め込みから層を手で回し、層 layer_idx の出力の主位置から列の最後までに sign×coef×v を足して後の層を流す。

    返り値: 最後の層の出口の残差（最終の正規化の入力・層の出力の型・形 [1, 列の長さ, 次元]）。
    use_cache が None なら模型の forward と同じく `config.use_cache` を使う（一回ごとに空の cache を作って捨てる）。
    keep（dict）を渡すと、自己検査のために層ごとの出力（書き換えの後）・書き換えの前と後・足した量を写しで残す。"""
    import torch
    import transformers.models.qwen3.modeling_qwen3 as MQ        # 模型の組み立てが呼ぶのと同じ名の束ね（mask・cache）
    core = model.model
    cfg = core.config
    layers = core.layers[: cfg.num_hidden_layers]                   # Qwen3Model.forward と同じ切り方
    n = len(ids)
    L = int(layer_idx)
    if not 0 <= L < len(layers):
        _die('層の添字 %s が範囲の外（層の数 %d）' % (layer_idx, len(layers)))
    if not 0 <= int(mp) < n:
        _die('主位置 %s が列の外（長さ %d）' % (mp, n))
    if int(sign) not in (1, -1):
        _die('符号は +1 か -1: %r' % (sign,))
    if use_cache is None:
        use_cache = getattr(cfg, 'use_cache', None)                 # check_model_inputs の既定と同じ
    use_cache = bool(use_cache)
    V32 = np.asarray(vec, dtype=np.float32)                         # 段階 B の走行器のフックと同じく NumPy の float32 を経る
    if V32.shape != (int(cfg.hidden_size),):
        _die('方向の形 %s が次元（%d）と合わない' % (V32.shape, cfg.hidden_size))
    done = 0
    with torch.no_grad():
        input_ids = torch.tensor([list(ids)], dtype=torch.long, device=core.embed_tokens.weight.device)
        inputs_embeds = core.embed_tokens(input_ids)
        past = MQ.DynamicCache(config=cfg) if use_cache else None
        cache_position = torch.arange(0, inputs_embeds.shape[1], device=inputs_embeds.device)
        position_ids = cache_position.unsqueeze(0)
        mk = dict(config=cfg, input_embeds=inputs_embeds, attention_mask=None, cache_position=cache_position,
                  past_key_values=past, position_ids=position_ids)
        masks = {'full_attention': MQ.create_causal_mask(**mk)}
        if core.has_sliding_layers:
            masks['sliding_attention'] = MQ.create_sliding_window_causal_mask(**mk)
        if keep is not None:
            keep['masks'] = masks
        h = inputs_embeds
        pe = core.rotary_emb(h, position_ids)                       # (cos, sin)・模型の forward と同じく全層で共有
        for i, layer in enumerate(layers):
            h = layer(h, attention_mask=masks[layer.attention_type], position_ids=position_ids,
                      past_key_values=past, use_cache=use_cache, cache_position=cache_position,
                      position_embeddings=pe)
            if i == L:
                if keep is not None:
                    keep['L_before'] = h.clone()
                # **層の出力の型に直してから sign×coef を掛け、主位置から後ろに足す**（段階 B の走行器のフックの算術と同じ形）
                add = int(sign) * float(coef) * torch.as_tensor(V32, dtype=h.dtype, device=h.device)
                h[0, int(mp):, :] = h[0, int(mp):, :] + add
                done += 1
                if keep is not None:
                    keep['L_after'] = h.clone()
                    keep['add'] = add.clone()
            if keep is not None:
                keep.setdefault('outs', []).append(h.clone())
    if done != 1:
        _die('書き換えが一度でない: %d 回' % done)
    if h.shape[1] != n:
        _die('出口の列の長さ %d が入力の長さ %d と違う' % (h.shape[1], n))
    return h


def readout(model, h_last, read_ids):
    """最終の正規化の入力（一つの位置）を float32 に上げ、最終の正規化と読み取りの集合の行を float32 で当てる。

    返り値: (量〔z_a − logsumexp(ほか)〕, 出口の値 z〔float32・read_ids の順〕)。"""
    import torch
    with torch.no_grad():
        g = model.model.norm.weight.to(torch.float32)
        x = h_last.to(device=g.device, dtype=torch.float32)          # 層が複数の装置に割られていても正規化の重みの装置で当てる
        eps = float(model.model.norm.variance_epsilon)
        xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g
        W = model.lm_head.weight
        idx = torch.as_tensor(list(read_ids), dtype=torch.long, device=W.device)
        z = W.index_select(0, idx).to(torch.float32) @ xn.to(W.device)
        lo = z[0] - torch.logsumexp(z[1:], dim=0)
    return float(lo), z


def _check_dirs(model, dirs, used):
    d = int(model.config.hidden_size)
    for dn in used:
        if dn not in dirs:
            _die('方向 %s が dirs に無い' % dn)
        v = dirs[dn]
        if not isinstance(v, np.ndarray) or v.dtype != np.float64:
            _die('方向 %s が float64 の配列でない（%s）' % (dn, getattr(v, 'dtype', type(v).__name__)))
        if v.shape != (d,):
            _die('方向 %s の形 %s が次元（%d）と合わない' % (dn, v.shape, d))
        if not np.all(np.isfinite(v)):
            _die('方向 %s に有限でない値がある' % dn)
    if 'static' in dirs:
        ns = float(np.linalg.norm(dirs['static']))
        for dn in used:
            nv = float(np.linalg.norm(dirs[dn]))
            if nv != 0.0 and abs(nv - ns) > NORM_REL_TOL * max(ns, 1.0):
                _die('方向 %s のノルム（%.9g）が ‖static‖（%.9g）に揃っていない（正本 directions.norm_rule）' % (dn, nv, ns))


def recompute_rewrite(model, tok, T3, FJ, rows, dirs_by_row, dirs, layer_idx, coef, use_cache=None):
    """残差の書き換えの道で、行ごとに無操作の量と、方向と符号ごとの効き目を計算し直す（近道なし・バッチ一）。

    rows: [(行の名, 升目の鍵 '場面|土台の腕', 符号)]。dirs_by_row: 行の名 → [(方向の名, 符号)]。dirs: 方向の名 → float64 のベクトル。
    返り値: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}。**値は印字しない。**
    use_cache（既定 None＝模型の forward と同じ `config.use_cache`）は、手回しの道の mask の組み方を模型の forward のどの呼び方に
    合わせるかだけを決める（数の上の意味は同じ・開発の記録の「決まっていなかった所」を見よ）。"""
    check_env(model, T3)
    check_layer_and_coef(model, T3, layer_idx, coef)
    assert_no_forward_hooks(model)
    rows = [tuple(r) for r in rows]
    for r in rows:
        if len(r) != 3:
            _die('行は（行の名, 升目の鍵, 符号）の三つ組: %r' % (r,))
    names = [r[0] for r in rows]
    if len(set(names)) != len(names):
        _die('行の名が重なる')
    missing = [nm for nm in names if nm not in dirs_by_row]
    if missing:
        _die('dirs_by_row に行が無い: %s' % '・'.join(missing))
    used = sorted({dn for nm in names for dn, _ in dirs_by_row[nm]})
    _check_dirs(model, dirs, used)
    canon_rows = {r['id']: r for r in T3['main_rows']}
    import run_stageB_local as RB
    AT = RB.arm_texts()
    d = int(model.config.hidden_size)
    zero = np.zeros(d, dtype=np.float64)                            # 無操作は零のベクトル（正本 readout.primary.batching）
    cells, out = {}, {}
    for name, ck, sign in rows:
        sign = int(sign)
        if sign not in (1, -1):
            _die('行 %s の符号は +1 か -1: %r' % (name, sign))
        if name in canon_rows:
            cr = canon_rows[name]
            if ck != '%s|%s' % (cr['scenario'], cr['base']) or sign != int(cr['sign']):
                _die('行 %s の升目か符号が正本 main_rows と違う（%s %+d 対 %s|%s %+d）'
                     % (name, ck, sign, cr['scenario'], cr['base'], int(cr['sign'])))
        if ck not in cells:
            cells[ck] = cell_input(tok, T3, FJ, ck, _AT=AT)
        c = cells[ck]
        h0 = forward_rewrite(model, c['ids'], layer_idx, zero, coef, sign, c['mp'], use_cache=use_cache)
        if h0.shape[1] - 1 != c['ro']:
            _die('読み取りの位置が列の最後でない')
        lo0, _ = readout(model, h0[0, -1], c['read_ids'])
        eff = {}
        for dn, s in dirs_by_row[name]:
            s = int(s)
            if s not in (1, -1):
                _die('方向 %s の符号は +1 か -1: %r' % (dn, s))
            key = '%s|%+d' % (dn, s)
            if key in eff:
                _die('行 %s に同じ方向と符号が二度ある: %s' % (name, key))
            h = forward_rewrite(model, c['ids'], layer_idx, dirs[dn], coef, s, c['mp'], use_cache=use_cache)
            lo, _ = readout(model, h[0, -1], c['read_ids'])
            eff[key] = lo - lo0
        out[name] = {'noop_lo': lo0, 'effects': eff}
    assert_no_forward_hooks(model)
    return out


# ---------------------------------------------------------------- 乱数の小さな模型と合成の方向（確かめだけに使う）

def tiny_model():
    """乱数の小さな模型（設定だけを手元の置き場から借りる・**実の重みは読まない**）。コーディネータの合成の器と同じ作り方を自分で書いた。"""
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM
    cfg = AutoConfig.from_pretrained(SNAP)
    (cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim,
     cfg.intermediate_size) = (TINY['hidden_size'], TINY['num_hidden_layers'], TINY['num_attention_heads'],
                               TINY['num_key_value_heads'], TINY['head_dim'], TINY['intermediate_size'])
    cfg.layer_types = list(cfg.layer_types)[:TINY['num_hidden_layers']]   # 元の長さのままだと空の層ができる
    torch.manual_seed(0)
    model = AutoModelForCausalLM.from_config(cfg)
    g = torch.Generator().manual_seed(1)
    with torch.no_grad():
        for name, p in model.named_parameters():                   # 初期値の一のままだと正規化の誤りが見えない
            if name.endswith('norm.weight'):
                p.copy_(torch.rand(p.shape, generator=g) + 0.5)    # 一様乱数 [0.5, 1.5)
    return model.to(torch.bfloat16).eval()


def _assert_tiny(model):
    """確かめは乱数の小さな模型だけで走らせる（封印の前に本物の模型で読み取りの値を出さない・正本 computation.before_seal）。"""
    c = model.config
    if (int(c.hidden_size), int(c.num_hidden_layers)) != (TINY['hidden_size'], TINY['num_hidden_layers']):
        _die('確かめは乱数の小さな模型だけで走らせる（次元 %s・層 %s）' % (c.hidden_size, c.num_hidden_layers))


def synthetic_dirs(FJ, d):
    """合成の方向: `np.random.default_rng(5)` で次元 d の正規乱数を名の順に引き、static のノルムにそろえる。
    名は static・iso:0〜iso:19・real:＋転記行 D の実在の差の対の名（その順）。"""
    F = _facts(FJ)
    names = ['static'] + ['iso:%d' % k for k in range(20)] + ['real:' + p for p in F['D']['real_pairs']]
    rng = np.random.default_rng(5)
    raw = [(nm, rng.normal(size=d)) for nm in names]
    ns = float(np.linalg.norm(raw[0][1]))
    dirs = {}
    for nm, v in raw:
        dirs[nm] = v if nm == 'static' else v * (ns / float(np.linalg.norm(v)))
    return dirs, names


def _static_rows(T3, FJ):
    """主の行のうち方向が static の行から、減算の行（main_rows の順で最初）と加算の行（族を両方覆うため、減算の行と
    違う族の最初の加算の行・無ければ最初の加算の行）を選ぶ。"""
    F = _facts(FJ)
    fam = lambda r: F['B']['cells']['%s|%s' % (r['scenario'], r['base'])]['family']
    main = [r for r in T3['main_rows'] if r['direction'] == 'static']
    sub = next(r for r in main if int(r['sign']) == -1)
    add = next((r for r in main if int(r['sign']) == 1 and fam(r) != fam(sub)), None) or \
        next(r for r in main if int(r['sign']) == 1)
    return [(r['id'], '%s|%s' % (r['scenario'], r['base']), int(r['sign'])) for r in (sub, add)]


def _max_abs_diff(A, B):
    """二つの結果の、全ての効き目と無操作の量の差の絶対値の最大（鍵の集合が違えば None）。"""
    if set(A) != set(B):
        return None
    de, dn, n = 0.0, 0.0, 0
    for nm in A:
        ea, eb = A[nm]['effects'], B[nm]['effects']
        if set(ea) != set(eb):
            return None
        for k in ea:
            de = max(de, abs(float(ea[k]) - float(eb[k])))
            n += 1
        dn = max(dn, abs(float(A[nm]['noop_lo']) - float(B[nm]['noop_lo'])))
    return {'effects': de, 'noop': dn, 'n_effects': n}


# ---------------------------------------------------------------- 自己検査

def _selftest():
    import torch
    import torch.nn as nn
    from transformers import AutoTokenizer
    import direction_B
    T3, FJ = load_canon(), load_facts()
    F = _facts(FJ)
    tok = AutoTokenizer.from_pretrained(SNAP)
    model = tiny_model()
    _assert_tiny(model)
    check_env(model, T3)
    n_layers = len(direction_B.decoder_layers(model))
    L = direction_B.layer_index(float(T3['layers']['selected_ratio']), n_layers)
    coef = float(T3['layers']['coef_applied'])
    d = int(model.config.hidden_size)
    dirs, _ = synthetic_dirs(FJ, d)
    zero = np.zeros(d, dtype=np.float64)
    logit_tol = float(T3['computation']['logit_tol'])
    res = []

    def ck(label, ok, detail=''):
        res.append(bool(ok))
        print('[%s] %s%s' % ('ok' if ok else 'NG', label, ('  | ' + detail) if detail else ''))

    def stops(fn):
        try:
            fn()
        except SystemExit as e:
            return True, str(e)
        return False, ''

    import transformers
    print('bl3_recompute_rewrite %s --selftest  torch %s・transformers %s・numpy %s・注意の実装 %s・config.use_cache %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__,
             model.config._attn_implementation, model.config.use_cache))
    print('乱数の小さな模型: 次元 %d・層 %d・注意の頭 %d・KV の頭 %d・頭の次元 %d・中間 %d・選んだ層の添字 %d・係数 %s'
          % (d, n_layers, model.config.num_attention_heads, model.config.num_key_value_heads, model.config.head_dim,
             model.config.intermediate_size, L, coef))

    # (1) 升目の組み立て
    import run_stageB_local as RB
    AT = RB.arm_texts()
    C = {k: cell_input(tok, T3, FJ, k, _AT=AT) for k in F['B']['cells']}
    ck('升目の組み立てが転記行 B と一致（全 %d 升目・長さ・主位置・読み取りの位置・族・前置きの SHA16・読み取りの集合のトークン）' % len(C), True,
       '・'.join('%s %d/%d/%d' % (k, c['prompt_len'], c['mp'], c['ro']) for k, c in C.items()))
    for fld, dv in (('prompt_len', 1), ('main_position', 1), ('readout_position', -1)):
        F2 = copy.deepcopy(FJ)
        _facts(F2)['B']['cells']['S1|O-Ncold'][fld] += dv
        ok, msg = stops(lambda: cell_input(tok, T3, F2, 'S1|O-Ncold', _AT=AT))
        ck('転記行 B と違えば止まる（S1|O-Ncold の %s を %+d ずらした写し）' % (fld, dv), ok)
    F2 = copy.deepcopy(FJ)
    _facts(F2)['A']['prefix_ids'] = list(_facts(F2)['A']['prefix_ids'])[:-1]
    ok, _ = stops(lambda: cell_input(tok, T3, F2, 'S1|O-Ncold', _AT=AT))
    ck('主の書き出しの割り方が変われば止まる（最後のトークンを落とした写し）', ok)

    # (2) 書き換えを零にした手回しの道の最終の正規化の入力 ＝ 模型そのものの forward の最終の正規化の入力（前の hook で取るだけ）
    probe = [k for k in ('N1|Onull', 'S1|O-Ncold') if k in C]
    for k in probe:
        c = C[k]
        x = torch.tensor([c['ids']], dtype=torch.long)
        for uc, label in ((None, '既定（config.use_cache）'), (False, 'use_cache=False')):
            cap = {}
            hd = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('x', a[0].detach().clone()))
            try:
                with torch.no_grad():
                    o = model(input_ids=x, logits_to_keep=1) if uc is None else model(input_ids=x, use_cache=False, logits_to_keep=1)
            finally:
                hd.remove()
            assert_no_forward_hooks(model)
            keep = {}
            h = forward_rewrite(model, c['ids'], L, zero, coef, +1, c['mp'], use_cache=uc, keep=keep)
            same = torch.equal(h, cap['x'])
            md = float((h.float() - cap['x'].float()).abs().max())
            ck('%s %s: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）' % (k, label), same,
               '差の絶対値の最大 %.3g・形 %s・型 %s' % (md, tuple(h.shape), h.dtype))
            mfa = keep['masks']['full_attention']
            print('[参考] %s %s: 手回しの道が組んだ mask（full_attention）は %s（判定に入れない）'
                  % (k, label, 'None（SDPA は is_causal で走る）' if mfa is None
                     else '明示の mask（型 %s・形 %s）' % (mfa.dtype, tuple(mfa.shape))))
            lo, z = readout(model, h[0, -1], c['read_ids'])
            ref = o.logits[0, -1, c['read_ids']].float()
            dz = float((z - ref).abs().max())
            ck('%s %s: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内' % (k, label),
               dz <= logit_tol, '差の絶対値の最大 %.3g（許容 %s）' % (dz, logit_tol))
            if uc is None:
                with torch.no_grad():
                    o2 = model.model(input_ids=x, output_hidden_states=True)
                hs = o2.hidden_states
                # 歯の確かめ: hidden_states[-1]（正規化の後）を正規化の入力と取り違えると正規化が二度掛かり、模型の出口の値からもっと離れる
                _, zw = readout(model, hs[-1][0, -1], c['read_ids'])
                dzw = float((zw - ref).abs().max())
                ck('%s: 歯の確かめ——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 4 倍を超える' % k,
                   dzw > 4 * dz, '取り違え %.3g・正しい %.3g' % (dzw, dz))
                ck('%s: hidden_states[-1] は正規化の後（last_hidden_state と同じ・最終の正規化の入力と違う）' % k,
                   torch.equal(hs[-1], o2.last_hidden_state) and not torch.equal(hs[-1], cap['x']))
                ck('%s: 手回しの層 %d の出力（書き換えの前）が hidden_states[%d]（layers.hidden_states_indices の対応）と一致（ビット単位）'
                   % (k, L, direction_B.hidden_states_index(L)),
                   torch.equal(keep['L_before'], hs[direction_B.hidden_states_index(L)]))

    # (3) 主位置より前の位置は書き換えない
    for k, sign in (('S1|O-Ncold', -1), ('N1|Onull', +1)):
        c = C[k]
        mp = c['mp']
        k0, k1 = {}, {}
        h0 = forward_rewrite(model, c['ids'], L, zero, coef, sign, mp, keep=k0)
        h1 = forward_rewrite(model, c['ids'], L, dirs['static'], coef, sign, mp, keep=k1)
        pre_same = all(torch.equal(k0['outs'][i], k1['outs'][i]) for i in range(L))
        ck('%s 符号 %+d: 層 %d より前の層の出力は無操作と同じ（ビット単位）' % (k, sign, L), pre_same)
        ck('%s 符号 %+d: 層 %d の出力（書き換えの前）は無操作と同じ（ビット単位）' % (k, sign, L), torch.equal(k0['L_before'], k1['L_before']))
        ck('%s 符号 %+d: 書き換えは主位置（%d）より前の位置を変えない（層 %d の出力・ビット単位）' % (k, sign, mp, L),
           torch.equal(k1['L_after'][:, :mp], k1['L_before'][:, :mp]))
        ck('%s 符号 %+d: 主位置から列の最後まで（%d 位置）に同じ量を足した（層 %d の出力・ビット単位）' % (k, sign, len(c['ids']) - mp, L),
           torch.equal(k1['L_after'][:, mp:], k1['L_before'][:, mp:] + k1['add']))
        dv = (k1['L_after'][0, mp:].float() - k1['L_before'][0, mp:].float()).double().numpy()
        want = sign * coef * dirs['static']
        cos = float(np.min(dv @ want / (np.linalg.norm(dv, axis=1) * np.linalg.norm(want))))
        rel = float(np.max(np.abs(np.linalg.norm(dv, axis=1) / np.linalg.norm(want) - 1.0)))
        ck('%s 符号 %+d: 足した量の向きと大きさが sign×coef×v（bf16 の丸めの内）' % (k, sign), cos > 0.9999 and rel < 0.01,
           '余弦の最小 %.6f・ノルムの相対の差の最大 %.3g' % (cos, rel))
        before_same = torch.equal(h1[:, :mp], h0[:, :mp])
        band_diff = all(not torch.equal(h1[0, p], h0[0, p]) for p in range(mp, len(c['ids'])))
        ck('%s 符号 %+d: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う' % (k, sign),
           before_same and band_diff)

    # [参考・判定に入れない] 段階 B のフックの算術（NumPy の float32 を経て bf16）と、float64 から直に bf16 にした形が、合成の方向で同じか
    n_same = sum(torch.equal(torch.as_tensor(np.asarray(v, dtype=np.float32), dtype=torch.bfloat16),
                             torch.as_tensor(v, dtype=torch.bfloat16)) for v in dirs.values())
    print('[参考] float32 を経た bf16 と float64 から直に直した bf16 が同じ合成の方向: %d/%d（判定に入れない）' % (n_same, len(dirs)))

    # (4) 零のベクトルの効き目は零・(5) 同じ呼び出しは同じ値
    rows = _static_rows(T3, FJ)
    dz_ = dict(dirs)
    dz_['zero'] = zero
    dbr = {nm: [('zero', +1), ('zero', -1), ('static', s)] for nm, _, s in rows}
    r1 = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dz_, L, coef)
    zeros_ok = all(r1[nm]['effects']['zero|+1'] == 0.0 and r1[nm]['effects']['zero|-1'] == 0.0 for nm, _, _ in rows)
    ck('零のベクトルの効き目が零（両方の符号・%d 行: %s）' % (len(rows), '・'.join(nm for nm, _, _ in rows)), zeros_ok,
       '・'.join('%s %r/%r' % (nm, r1[nm]['effects']['zero|+1'], r1[nm]['effects']['zero|-1']) for nm, _, _ in rows))
    teeth = all(r1[nm]['effects']['static|%+d' % s] != 0.0 for nm, _, s in rows)
    ck('歯の確かめ: static の効き目は零でない（乱数の小さな模型）', teeth,
       '・'.join('%s %.3g' % (nm, r1[nm]['effects']['static|%+d' % s]) for nm, _, s in rows))
    r2 = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dz_, L, coef)
    ck('同じ呼び出しを二度走らせて同じ値（ビット単位）', r1 == r2)
    shape_ok = all(set(r1[nm]) == {'noop_lo', 'effects'} and isinstance(r1[nm]['noop_lo'], float) for nm in r1)
    ck('出力の形 {行の名: {noop_lo, effects: {方向の名|符号: 効き目}}}（符号の書き方 %+d）', shape_ok and
       set(r1[rows[0][0]]['effects']) == {'zero|+1', 'zero|-1', 'static|%+d' % rows[0][2]},
       '鍵の例 %s' % sorted(r1[rows[0][0]]['effects']))

    # (6) 止める確かめ
    one = [rows[0]]
    dbr1 = {rows[0][0]: [('static', rows[0][2])]}
    h_ = direction_B.decoder_layers(model)[L].register_forward_hook(lambda m, i, o: o)
    try:
        ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L, coef))
    finally:
        h_.remove()
    ck('模型に forward の hook が掛かっていれば止まる', ok)
    ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L + 1, coef))
    ck('層の添字が正本の規則と違えば止まる', ok)
    ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L, coef * 2))
    ck('係数が正本 layers.coef_applied と違えば止まる', ok)
    bad = dict(dirs)
    bad['static'] = dirs['static'].astype(np.float32)
    ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, bad, L, coef))
    ck('方向が float64 でなければ止まる', ok)
    bad = dict(dirs)
    bad['iso:0'] = dirs['iso:0'] * 1.01
    ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, {rows[0][0]: [('iso:0', rows[0][2])]}, bad, L, coef))
    ck('方向のノルムが ‖static‖ に揃っていなければ止まる', ok)
    ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, [(rows[0][0], rows[0][1], -rows[0][2])], dbr1, dirs, L, coef))
    ck('正本の行の符号と違えば止まる', ok)
    ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, [(rows[0][0], rows[1][1], rows[0][2])], dbr1, dirs, L, coef))
    ck('正本の行の升目と違えば止まる', ok)

    # (7) 呼び出しの間に hook を掛けようとしない（掛ける関数を、呼ばれたら落ちる形に差し替えて走らせる）
    orig = (nn.Module.register_forward_hook, nn.Module.register_forward_pre_hook)
    called = []

    def _trap(*a, **kw):
        called.append(1)
        raise RuntimeError('hook を掛けようとした')
    nn.Module.register_forward_hook, nn.Module.register_forward_pre_hook = _trap, _trap
    try:
        r3 = recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L, coef)
        trap_ok = not called
    except RuntimeError:
        trap_ok = False
    finally:
        nn.Module.register_forward_hook, nn.Module.register_forward_pre_hook = orig
    ck('呼び出しの間に forward の hook を掛けようとしない（掛ける関数を差し替えて走らせた）', trap_ok and
       r3[rows[0][0]]['effects'] == {k_: v_ for k_, v_ in r1[rows[0][0]]['effects'].items() if k_.startswith('static|')})

    n_ok = sum(res)
    print('selftest: %d/%d ok' % (n_ok, len(res)))
    print('柵: ' + FENCE)
    return n_ok == len(res)


# ---------------------------------------------------------------- フックの道との突き合わせ（乱数の小さな模型だけ）

def _readout64(model, h_last, read_ids):
    """参考だけに使う: 同じ最終の正規化の入力を float64 で読む（float32 の読み取りの丸めの大きさの目安）。"""
    import torch
    with torch.no_grad():
        x = h_last.to(torch.float64)
        g = model.model.norm.weight.to(torch.float64)
        eps = float(model.model.norm.variance_epsilon)
        xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g
        z = model.lm_head.weight[list(read_ids)].to(torch.float64) @ xn
        return float(z[0] - torch.logsumexp(z[1:], dim=0))


def _dry():
    import torch
    from transformers import AutoTokenizer
    import direction_B
    T3, FJ = load_canon(), load_facts()
    F = _facts(FJ)
    tok = AutoTokenizer.from_pretrained(SNAP)
    model = tiny_model()
    _assert_tiny(model)
    n_layers = len(direction_B.decoder_layers(model))
    L = direction_B.layer_index(float(T3['layers']['selected_ratio']), n_layers)
    coef = float(T3['layers']['coef_applied'])
    tol = float(T3['independent_recompute']['tol_stage1'])
    d = int(model.config.hidden_size)
    dirs, names = synthetic_dirs(FJ, d)
    rows = _static_rows(T3, FJ)
    reals = [nm for nm in names if nm.startswith('real:')]
    dbr = {}
    for nm, ck_, s in rows:
        lst = [('static', s)] + [('iso:%d' % k, s) for k in range(20)]
        for rn in reals:
            lst += [(rn, s), (rn, -s)]
        dbr[nm] = lst
    import transformers
    print('bl3_recompute_rewrite %s --dry  torch %s・transformers %s・numpy %s・注意の実装 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, model.config._attn_implementation))
    print('乱数の小さな模型: 次元 %d・層 %d・選んだ層の添字 %d・係数 %s・一段目の許容 independent_recompute.tol_stage1 = %s'
          % (d, n_layers, L, coef, tol))
    for nm, ck_, s in rows:
        n_st = sum(1 for dn, _ in dbr[nm] if dn == 'static')
        n_iso = sum(1 for dn, _ in dbr[nm] if dn.startswith('iso:'))
        n_real = sum(1 for dn, _ in dbr[nm] if dn.startswith('real:'))
        print('行 %s・升目 %s（%s）・符号 %+d・方向と符号 %d 組（static %d・等方に見立てた %d・実在の差の名 %d 本 × 両方の向き＝%d）＋無操作'
              % (nm, ck_, F['B']['cells'][ck_]['family'], s, len(dbr[nm]), n_st, n_iso, len(reals), n_real))

    t0 = time.time()
    mine = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dirs, L, coef)
    t_mine = time.time() - t0
    print('残差の書き換えの道: %.1f 秒（順伝播 %d 回）' % (t_mine, sum(1 + len(dbr[nm]) for nm, _, _ in rows)))

    hk, err = None, None
    t0 = time.time()
    try:
        import bl3_run as BR                                        # 中は開かない・公開の関数だけを呼ぶ
        R = BR.Runner(model, T3, L, coef, dirs)
        cells = BR.build_cells(tok, T3, FJ, sorted({ck_ for _, ck_, _ in rows}))
        hk = BR.recompute_hook_path(R, [(nm, cells[ck_], s) for nm, ck_, s in rows], dbr)
    except BaseException as e:                                     # 中を見ないため、落ちたときは種類と文言だけを印字する
        err = '%s: %s' % (type(e).__name__, str(e)[:500])
    t_hook = time.time() - t0
    if err:
        print('フックの道が落ちた（%.1f 秒）: %s' % (t_hook, err))
        print('dry: 突き合わせられなかった')
        print('柵: ' + FENCE)
        return False
    print('フックの道: %.1f 秒' % t_hook)

    D = _max_abs_diff(mine, hk)
    if D is None:
        print('dry: 鍵の集合が違う（行または方向|符号）——不一致')
        print('柵: ' + FENCE)
        return False
    emax = max(abs(float(v)) for nm in mine for v in mine[nm]['effects'].values())
    print('効き目の数 %d・効き目の絶対値の最大（残差の書き換えの道）%.4g' % (D['n_effects'], emax))
    print('差の絶対値の最大: 効き目 %.3g・無操作の量 %.3g' % (D['effects'], D['noop']))
    ok = D['effects'] <= tol
    print('dry: 一段目の許容（%s）の%s（効き目の差の最大 %.3g）' % (tol, '内' if ok else '外', D['effects']))
    print('（正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない）')

    # 参考（判定に入れない）: 読み取りの float32 の丸めの目安——同じ最終の正規化の入力を float64 で読み直した量との差の最大
    r64 = 0.0
    for nm, ck_, s in rows:
        c = cell_input(tok, T3, FJ, ck_)
        for v in (np.zeros(d, dtype=np.float64), dirs['static']):
            h = forward_rewrite(model, c['ids'], L, v, coef, s, c['mp'])
            lo32, _ = readout(model, h[0, -1], c['read_ids'])
            r64 = max(r64, abs(lo32 - _readout64(model, h[0, -1], c['read_ids'])))
    print('参考: 読み取りの float32 の丸めの目安（同じ最終の正規化の入力を float64 で読み直した量との差の最大・無操作と static・%d 行）%.3g'
          % (len(rows), r64))

    # 参考（判定に入れない）: フックの道の後に残差の書き換えの道を短く走らせ直し、掛け残しや模型の変化が無いこと
    sub_dbr = {nm: [('static', s)] for nm, _, s in rows}
    again = recompute_rewrite(model, tok, T3, FJ, rows, sub_dbr, dirs, L, coef)
    same = all(again[nm]['noop_lo'] == mine[nm]['noop_lo'] and
               again[nm]['effects']['static|%+d' % s] == mine[nm]['effects']['static|%+d' % s] for nm, _, s in rows)
    print('参考: フックの道の後に走らせ直した残差の書き換えの道（無操作と static・%d 行）が一度目と同じ（ビット単位）: %s'
          % (len(rows), '同じ' if same else '違う'))
    # 参考（判定に入れない）: mask の組み方を use_cache=False の形（明示の mask）にした残差の書き換えの道
    t0 = time.time()
    mine_nc = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dirs, L, coef, use_cache=False)
    D2 = _max_abs_diff(mine_nc, mine)
    D3 = _max_abs_diff(mine_nc, hk)
    print('参考: use_cache=False の形の残差の書き換えの道（%.1f 秒）——既定の形との差の最大 効き目 %.3g・無操作 %.3g／フックの道との差の最大 効き目 %.3g・無操作 %.3g'
          % (time.time() - t0, D2['effects'], D2['noop'], D3['effects'], D3['noop']))

    # 参考（判定に入れない・事前登録つき）: 歯の変種——この道をわざと誤らせ、フックの道との差が許容を超えるか（突き合わせの弁別力）
    t0 = time.time()
    M = _mutant_diffs(model, tok, T3, FJ, rows, dirs, reals[0], L, coef, hk)
    for kind, label, dmax, nk in M:
        if kind == 'M0':
            verdict = '許容の内（対照として期待どおり）' if dmax <= tol else '許容の外（対照が外れた——突き合わせの機械を疑う）'
        else:
            verdict = '許容の外＝捕まえた' if dmax > tol else '許容の内＝捕まえなかった（この模型での盲点）'
        print('[歯] %s %s: フックの道との効き目の差の最大 %.3g（%d 個の効き目）→ %s（許容 %s）' % (kind, label, dmax, nk, verdict, tol))
    print('[歯] 変種の計算 %.1f 秒（参考・判定に入れない）' % (time.time() - t0))
    print('柵: ' + FENCE)
    return ok


def _readout_double(model, h_last, read_ids):
    """歯の変種 M5 だけに使う: 最終の正規化を二度当てた読み取り（hidden_states[-1] を正規化の入力と取り違えたのと同じ形）。"""
    import torch
    with torch.no_grad():
        g = model.model.norm.weight.to(torch.float32)
        eps = float(model.model.norm.variance_epsilon)
        x = h_last.to(device=g.device, dtype=torch.float32)
        xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g
        xnn = xn * torch.rsqrt(xn.pow(2).mean(-1, keepdim=True) + eps) * g
        z = model.lm_head.weight[list(read_ids)].to(torch.float32) @ xnn.to(model.lm_head.weight.device)
        return float(z[0] - torch.logsumexp(z[1:], dim=0))


def _readout_bf16(model, h_last, read_ids):
    """歯の変種 M6 だけに使う: 模型そのものと同じく、正規化の出力を bf16 に戻して重みを掛け、語彙の行列の積も bf16 で取る読み取り。"""
    import torch
    with torch.no_grad():
        g = model.model.norm.weight
        eps = float(model.model.norm.variance_epsilon)
        xf = h_last.to(device=g.device, dtype=torch.float32)
        xn = g * (xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + eps)).to(g.dtype)
        z = (model.lm_head.weight[list(read_ids)] @ xn.to(model.lm_head.weight.device)).to(torch.float32)
        return float(z[0] - torch.logsumexp(z[1:], dim=0))


def _mutant_diffs(model, tok, T3, FJ, rows, dirs, first_real, L, coef, hk):
    """歯の変種（参考）: M0＝誤らせない対照・M1 帯の起点を主位置の一つ後・M2 書き換える層を一つ後・M3 符号の反転・
    M4 係数を二度掛ける・M5 読み取りで正規化を二度・M6 読み取りを bf16。行ごとに無操作と五つの鍵（static・iso:0・iso:1 は行の符号、
    real の最初の対は両方の向き）の効き目を作り、フックの道の同じ鍵の効き目との差の絶対値の最大を返す。"""
    d = int(model.config.hidden_size)
    zero = np.zeros(d, dtype=np.float64)
    fwd = {'M0': {}, 'M1': {'mp_shift': 1}, 'M2': {'layer_shift': 1}, 'M3': {'flip': True}, 'M4': {'coef_twice': True}}
    labels = {'M0': '誤らせない（対照）', 'M1': '帯の起点を主位置の一つ後にする', 'M2': '書き換える層を一つ後にする',
              'M3': '符号を反転する', 'M4': '係数を二度掛ける（sign×coef×coef×v）',
              'M5': '読み取りで正規化を二度当てる', 'M6': '読み取りを bf16 で当てる'}
    std = lambda m, hl, ids: readout(m, hl, ids)[0]
    eff = {k: {} for k in labels}
    for nm, ck_, s in rows:
        c = cell_input(tok, T3, FJ, ck_)
        keys = [('static', s), ('iso:0', s), ('iso:1', s), (first_real, +1), (first_real, -1)]
        for kind, opt in fwd.items():
            Lm = L + opt.get('layer_shift', 0)
            mpm = c['mp'] + opt.get('mp_shift', 0)
            cm = coef * coef if opt.get('coef_twice') else coef
            readers = {'M0': std, 'M5': _readout_double, 'M6': _readout_bf16} if kind == 'M0' else {kind: std}
            h0 = forward_rewrite(model, c['ids'], Lm, zero, cm, s, mpm)
            lo0 = {rk: rf(model, h0[0, -1], c['read_ids']) for rk, rf in readers.items()}
            for dn, sg in keys:
                h = forward_rewrite(model, c['ids'], Lm, dirs[dn], cm, (-sg if opt.get('flip') else sg), mpm)
                for rk, rf in readers.items():
                    eff[rk].setdefault(nm, {})['%s|%+d' % (dn, sg)] = rf(model, h[0, -1], c['read_ids']) - lo0[rk]
    out = []
    for kind in labels:
        dmax, nk = 0.0, 0
        for nm in eff[kind]:
            for key, v in eff[kind][nm].items():
                dmax = max(dmax, abs(float(v) - float(hk[nm]['effects'][key])))
                nk += 1
        out.append((kind, labels[kind], dmax, nk))
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser(description='B-lens 層三（Bl3）の独立の再計算——残差の書き換えの道')
    ap.add_argument('--selftest', action='store_true', help='乱数の小さな模型で自己検査')
    ap.add_argument('--dry', action='store_true', help='乱数の小さな模型で、フックの道と一段目の許容で突き合わせる')
    a = ap.parse_args()
    if not (a.selftest or a.dry):
        ap.print_help()
        return 0
    ok = True
    if a.selftest:
        ok = _selftest() and ok
    if a.dry:
        ok = _dry() and ok
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
