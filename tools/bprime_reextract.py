# -*- coding: utf-8 -*-
"""bprime_reextract.py v1 —— B′（Gemma-4-31B-it）の**独立の再抽出の道**
（2026-09-30・本の器の書き手〔コーディネータ・南無弥勒如来〕と別の系統内の個体が書いた・登録者の裁定 D270 による・独立の目を通っていない）。

正本 `design/contrasts-Bprime.json` の `independent_recompute.reextract`（本の抽出と同じ読み込みの設定・同じ注意の実装と決定性の設定・
バッチ一・bf16 で、違うのは活性を取り出す書き方だけ〔T22〕）・`directions`（named・defs・extraction）・`layers` に従う。
コーディネータの抽出の器（`bprime_directions` ほか）の中身を**読まずに**書いた。`--dry` でだけ、その公開の関数を中を見ずに呼ぶ。

取り出し方（コーディネータの器は層の出力をフックで取り、その層で順伝播を打ち切る。この道はそれと別の書き方）:
  模型そのものの forward を `output_hidden_states=True`・`use_cache=False`・`logits_to_keep=1`・バッチ一で最後まで流し、
  `hidden_states[k+1]`（＝`layers[k]` の出力。[0] は埋め込み、[-1] は最終の正規化の後）の主位置（列の最後のトークン）を取る。
  注: transformers 5.16.1 の `output_hidden_states` は、初回に復号の層（と注意）へ記録用の forward の hook を据え付け、以後も
  （値を変えずに）居残る（`transformers.utils.output_capturing`）。この道はその記録だけを使い、自分では hook を一本も掛けない。
入力: 正本 `directions.extraction` の八腕 × 二場面（プロンプトだけ・書き出しはつながない）を、段階 B の組み立て
  （`run_stageB_local.user_message`・`scenario_and_instruction`）に Gemma のチャットの型を当てて作り、台帳 `extract_contexts` の
  prompt_len・main_position・main_position_token・ids_sha16 と照らす（違えば止める）。
名前のある方向: 腕ごとに二場面の平均（float64）を取り、正本 `directions.defs` の文（h_X − h_Y）どおりに作る
  （static＝O − Osec・loaded＝O-Ncold − Osec-Ncold・Nk＝Nk − N・td＝Onull − N。指示の対応と正本の文が合わなければ止める）。
出力: `reextract` → {文脈の名: float64 のベクトル}・`reextract_all` → {'h_norm_by_context': {文脈: ‖h‖}, 'vhat_norm': ‖static‖,
  'named_cos': {名: その名の方向と dirs[名] の余弦}}。**値は印字しない**（`--dry` が差を印字するのは乱数の小さな模型だけ）。
用法: python bprime_reextract.py --selftest   （乱数の小さな模型で自己検査）
      python bprime_reextract.py --dry        （乱数の小さな模型で、コーディネータの抽出の器と四つの文脈で突き合わせ）
走らせ方: PYTHONPATH=<Bprime>/pylib（transformers 5.16.1）・PYTHONDONTWRITEBYTECODE=1 を勧める。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import sys
if __name__ == '__main__':
    sys.dont_write_bytecode = True          # 外の置き場（公開の置き場・pylib・Bprime/tools）に .pyc を書かない
import os, re, json, time, copy, hashlib, argparse
import numpy as np

VERSION = 'v1'
HERE = os.path.dirname(os.path.abspath(__file__))
BPRIME = os.path.dirname(os.path.dirname(HERE))
CANON_PATH = os.path.join(BPRIME, 'design', 'contrasts-Bprime.json')
LEDGER_PATH = os.path.join(BPRIME, 'tools', 'ledger-bprime.json')
HF_DIR = os.path.join(BPRIME, 'hf', 'gemma-4-31B-it', '842da3794eaa0b77d5f08bae87a17459d91ff475')   # 設定とトークナイザだけ（実の重みは無い・使わない）
PUB_TOOLS_DEFAULT = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b/tools'          # 公開の置き場の凍結の器（読むだけ）
CAPTURE_MODULE = 'transformers.utils.output_capturing'
FENCE = '本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
# 指示に書かれた名前のある方向の対応（正本 directions.defs の文と照らす）
INSTR_DEFS = {'static': ('O', 'Osec'), 'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}
DRY_CONTEXTS = ['N1|O', 'S1|Osec', 'N1|Nk', 'S1|O-Ncold']     # --dry で比べる四つ（二場面・四つの腕・長さの違う列）


def _die(msg):
    raise SystemExit('bprime_reextract: ' + msg)


def _pub(name):
    """公開の置き場の凍結の器を import する（読むだけ・環境変数 OP4B_PUB_TOOLS で置き場を替えられる）。"""
    import importlib
    d = os.environ.get('OP4B_PUB_TOOLS', PUB_TOOLS_DEFAULT)
    if os.path.isdir(d) and d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module(name)


def load_canon():
    return json.load(open(CANON_PATH, encoding='utf-8'))


def load_ledger():
    return json.load(open(LEDGER_PATH, encoding='utf-8'))


def sha16_ids(ids):
    """台帳の ids_sha16 の決まり: sha256(','.join(str(x))) の十六進の大文字の頭 16 字。"""
    return hashlib.sha256(','.join(str(int(x)) for x in ids).encode('ascii')).hexdigest().upper()[:16]


def parts(model):
    if type(model).__name__ != 'Gemma4ForConditionalGeneration':
        _die('模型の最上位が Gemma4ForConditionalGeneration でない: %s' % type(model).__name__)
    mm = getattr(model, 'model', None)
    if mm is None or type(mm).__name__ != 'Gemma4Model':
        _die('多様式の本体が Gemma4Model でない: %s' % type(mm).__name__)
    lm = getattr(mm, 'language_model', None)
    if lm is None or type(lm).__name__ != 'Gemma4TextModel':
        _die('言語の模型が Gemma4TextModel でない: %s' % type(lm).__name__)
    return model, mm, lm


def is_capture_hook(fn):
    return getattr(fn, '__module__', None) == CAPTURE_MODULE and getattr(fn, '__name__', None) == 'output_capturing_hook'


def foreign_hooks(model):
    """transformers の記録用の hook を除いた forward の hook（前・後）と大域の hook の一覧。"""
    import torch.nn.modules.module as M
    bad = []
    for name, m in model.named_modules():
        for attr in ('_forward_hooks', '_forward_pre_hooks'):
            for _, fn in (getattr(m, attr, None) or {}).items():
                if attr == '_forward_hooks' and is_capture_hook(fn):
                    continue
                bad.append('%s.%s（%s.%s）' % (name or '<模型>', attr, getattr(fn, '__module__', '?'),
                                             getattr(fn, '__qualname__', type(fn).__name__)))
    for attr in ('_global_forward_hooks', '_global_forward_pre_hooks'):
        d = getattr(M, attr, None)
        if d:
            bad.append('大域の %s %d 本' % (attr, len(d)))
    return bad


def capture_hook_count(model):
    return sum(1 for _, m in model.named_modules() for fn in (getattr(m, '_forward_hooks', None) or {}).values()
               if is_capture_hook(fn))


def assert_no_foreign_hooks(model):
    bad = foreign_hooks(model)
    if bad:
        _die('模型に forward の hook が掛かっている（この道は hook を掛けず、掛け残しも混ぜない）: ' + '・'.join(bad))


def is_real(model, C):
    _, _, lm = parts(model)
    mf = C['inputs']['model_facts']
    return len(lm.layers) == int(mf['num_hidden_layers']) and int(lm.config.hidden_size) == int(mf['hidden_size'])


def layer_for(model, C):
    """選ぶ層の添字: `direction_B.layer_index(正本 layers.ratio, 模型の層の数)`。本の模型では正本 `layers.index` とも照らす。"""
    DB = _pub('direction_B')
    _, _, lm = parts(model)
    n = len(lm.layers)
    L = DB.layer_index(float(C['layers']['ratio']), n)
    if is_real(model, C) and (L != int(C['layers']['index']) or int(C['layers']['hidden_states_index']) != L + 1):
        _die('層の添字 %d が正本 layers.index（%s）・hidden_states_index（%s）と合わない'
             % (L, C['layers']['index'], C['layers']['hidden_states_index']))
    return L


# ---------------------------------------------------------------- 取り出し

def reextract(model, contexts, layer_idx):
    """文脈の名 → 選んだ層の出力の主位置（列の最後のトークン）の値（float64 の numpy の並び）。

    模型そのものの forward（output_hidden_states=True・use_cache=False・logits_to_keep=1・バッチ一・列の全体）を流し、
    hidden_states[layer_idx + 1] の最後の位置を取る。**値は印字しない。**"""
    import torch
    top, mm, lm = parts(model)
    if top.training or mm.training or lm.training:
        _die('模型が訓練の形（eval にしていない）')
    n = len(lm.layers)
    L = int(layer_idx)
    if not 0 <= L < n - 1:
        _die('層の添字 %s が範囲の外（0〜%d・最後の層の hidden_states は最終の正規化の後なので取らない）' % (layer_idx, n - 2))
    assert_no_foreign_hooks(model)
    d = int(lm.config.hidden_size)
    dev = lm.embed_tokens.weight.device
    out = {}
    for name, ids in contexts.items():
        ids = [int(x) for x in ids]
        if not ids:
            _die('文脈 %s のトークンの並びが空' % name)
        x = torch.tensor([ids], dtype=torch.long, device=dev)
        with torch.no_grad():
            o = model(input_ids=x, output_hidden_states=True, use_cache=False, logits_to_keep=1)
        hs = o.hidden_states
        if hs is None or len(hs) != n + 1:
            _die('hidden_states の数が層の数＋1 でない（%s）' % (None if hs is None else len(hs)))
        h = hs[L + 1]
        if tuple(h.shape) != (1, len(ids), d):
            _die('hidden_states[%d] の形 %s が (1, %d, %d) でない' % (L + 1, tuple(h.shape), len(ids), d))
        v = h[0, -1].detach().to(torch.float64).cpu().numpy()
        if not np.all(np.isfinite(v)):
            _die('文脈 %s の値に有限でないものがある' % name)
        out[name] = v
        del o, hs, h
    assert_no_foreign_hooks(model)
    return out


# ---------------------------------------------------------------- 文脈と名前のある方向

def chat_ids(tok, msg):
    """user の発話一つ・system なし・生成の口つきのチャットの型（transformers 5 は辞書の形を返すので input_ids を取る）。"""
    enc = tok.apply_chat_template([{'role': 'user', 'content': msg}], add_generation_prompt=True, tokenize=True)
    ids = enc['input_ids'] if hasattr(enc, 'keys') else enc
    if hasattr(ids, 'tolist'):
        ids = ids.tolist()
    ids = list(ids)
    if ids and isinstance(ids[0], (list, tuple)):
        if len(ids) != 1:
            _die('チャットの型の出力が一本の列でない')
        ids = list(ids[0])
    return [int(x) for x in ids]


def build_contexts(tok, C, ledger, AT=None):
    """抽出の文脈（正本 directions.extraction の八腕 × 二場面・プロンプトだけ）を作り、台帳 extract_contexts と照らす。"""
    RB = _pub('run_stageB_local')
    EX = C['directions']['extraction']
    arms, scenes = list(EX['arms']), list(EX['scenes'])
    if len(arms) * len(scenes) != int(EX['contexts']):
        _die('正本 directions.extraction の腕 × 場面の数が contexts（%s）と合わない' % EX['contexts'])
    LX = ledger['extract_contexts']
    AT = AT if AT is not None else RB.arm_texts()
    SI = {sc: RB.scenario_and_instruction(sc) for sc in scenes}
    out = {}
    for arm in arms:
        if arm not in AT:
            _die('腕 %s の本文が引けない' % arm)
        for sc in scenes:
            key = '%s|%s' % (sc, arm)
            if key not in LX:
                _die('文脈 %s が台帳 extract_contexts に無い' % key)
            rec = LX[key]
            s, inst = SI[sc]
            ids = chat_ids(tok, RB.user_message(AT[arm]['text'], s['text'], inst))
            bad = []
            if rec.get('scenario') != sc or rec.get('arm') != arm:
                bad.append('台帳の場面か腕が鍵と違う')
            if len(ids) != int(rec['prompt_len']):
                bad.append('長さ %d（台帳 %s）' % (len(ids), rec['prompt_len']))
            if len(ids) - 1 != int(rec['main_position']):
                bad.append('主位置 %d（台帳 %s）' % (len(ids) - 1, rec['main_position']))
            if tok.convert_ids_to_tokens(ids[-1]) != rec['main_position_token']:
                bad.append('主位置のトークン %r（台帳 %r）' % (tok.convert_ids_to_tokens(ids[-1]), rec['main_position_token']))
            if sha16_ids(ids) != rec['ids_sha16']:
                bad.append('ids_sha16 %s（台帳 %s）' % (sha16_ids(ids), rec['ids_sha16']))
            if bad:
                _die('抽出の文脈 %s が台帳と違う: %s' % (key, '・'.join(bad)))
            out[key] = ids
    if set(out) != set(LX):
        _die('台帳 extract_contexts の文脈の集合が正本の腕 × 場面と違う')
    return out


def arm_pairs_from_defs(C):
    """正本 directions.defs の文（…h_X − h_Y…）から、名前のある方向ごとの (足す腕, 引く腕) を読み、指示の対応と照らす。"""
    out = {}
    for nm in C['directions']['named']:
        s = C['directions']['defs'].get(nm)
        if s is None:
            _die('正本 directions.defs に %s が無い' % nm)
        terms = [a or b for a, b in re.findall(r'h_(?:\{([^}]*)\}|([A-Za-z]+))', s)]
        if len(terms) != 2 or '−' not in s.split('h_', 1)[1]:
            _die('正本 directions.defs.%s の文から二つの腕の差を読めない: %s' % (nm, s))
        out[nm] = (terms[0], terms[1])
        if nm in INSTR_DEFS and out[nm] != INSTR_DEFS[nm]:
            _die('正本 directions.defs.%s（%s − %s）が指示の対応（%s − %s）と違う' % ((nm,) + out[nm] + INSTR_DEFS[nm]))
    if set(out) != set(INSTR_DEFS):
        _die('正本の名前のある方向（%s）が指示の四つと違う' % sorted(out))
    return out


def named_directions(acts, C):
    """腕ごとに二場面の平均（float64）を取り、正本 directions.defs のとおりに名前のある方向を作る。"""
    pairs = arm_pairs_from_defs(C)
    scenes = list(C['directions']['extraction']['scenes'])

    def mean(arm):
        return np.mean(np.stack([np.asarray(acts['%s|%s' % (sc, arm)], dtype=np.float64) for sc in scenes]), axis=0)
    return {nm: mean(p) - mean(q) for nm, (p, q) in pairs.items()}


def cosine(a, b):
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def reextract_all(model, tok, C, ledger, dirs):
    """抽出の十六文脈をこの道で流し、{'h_norm_by_context', 'vhat_norm', 'named_cos'} を返す（値は印字しない）。"""
    import torch
    import transformers
    top, mm, lm = parts(model)
    want = str(ledger['meta']['transformers'])
    if transformers.__version__ != want:
        _die('transformers の版が %s（台帳 meta.transformers は %s）' % (transformers.__version__, want))
    if is_real(model, C) and lm.embed_tokens.weight.dtype != torch.bfloat16:
        _die('本の模型が bf16 でない（%s・正本 independent_recompute.reextract.path）' % lm.embed_tokens.weight.dtype)
    L = layer_for(model, C)
    contexts = build_contexts(tok, C, ledger)
    acts = reextract(model, contexts, L)
    D = named_directions(acts, C)
    named_cos = {}
    for nm in C['directions']['named']:
        if nm not in dirs:
            _die('dirs に名前のある方向 %s が無い' % nm)
        v = np.asarray(dirs[nm])
        if v.dtype.kind != 'f' or v.shape != D[nm].shape or not np.all(np.isfinite(v)) or not np.any(v):
            _die('dirs[%s] が形 %s の有限で零でない浮動小数の並びでない' % (nm, D[nm].shape))
        named_cos[nm] = cosine(D[nm], v)
    return {'h_norm_by_context': {k: float(np.linalg.norm(acts[k])) for k in contexts},
            'vhat_norm': float(np.linalg.norm(D['static'])),
            'named_cos': named_cos}


# ---------------------------------------------------------------- 乱数の小さな模型（確かめだけ・書き換えの道の器と同じ作り方を借りる）

def _rw():
    sys.path.insert(0, HERE)
    import bprime_recompute_rewrite as RW
    return RW


def _dtype_name(model):
    _, _, lm = parts(model)
    return str(lm.embed_tokens.weight.dtype).replace('torch.', '')


def _selftest():
    import torch
    import transformers
    from transformers import AutoTokenizer
    RW = _rw()
    C, LG = load_canon(), load_ledger()
    RB = _pub('run_stageB_local')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    base = RW.tiny_model(C)
    models = [('float32', RW.as_dtype(base, torch.float32)), ('bfloat16', base)]
    for _, m in models:
        RW.assert_tiny(m)
    res = []

    def ck(label, ok, detail=''):
        res.append(bool(ok))
        print('[%s] %s%s' % ('ok' if ok else 'NG', label, ('  | ' + detail) if detail else ''), flush=True)

    def stops(fn):
        try:
            fn()
        except SystemExit as e:
            return True, str(e)
        return False, ''

    m32 = models[0][1]
    _, _, lm32 = parts(m32)
    L = layer_for(m32, C)
    tol = C['independent_recompute']['reextract']
    print('bprime_reextract %s --selftest  torch %s・transformers %s・numpy %s・注意の実装 %s・作ったままの型 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, lm32.config._attn_implementation, _dtype_name(base)),
          flush=True)
    print('乱数の小さな模型: 次元 %d・層 %d・選んだ層の添字 %d（hidden_states[%d]）・許容 rel_tol %s・cos_min %s'
          % (int(lm32.config.hidden_size), len(lm32.layers), L, L + 1, tol['rel_tol'], tol['cos_min']), flush=True)

    # (1) 正本の定義と指示の対応・文脈の組み立て
    pairs = arm_pairs_from_defs(C)
    ck('正本 directions.defs の文から読んだ腕の差が指示の対応と一致', pairs == INSTR_DEFS,
       '・'.join('%s＝%s − %s' % (k, a, b) for k, (a, b) in pairs.items()))
    C2 = copy.deepcopy(C)
    C2['directions']['defs']['td'] = 'h_Nk − h_N（写しを書き換えた）'
    ck('正本の定義の文が指示の対応と違えば止まる（td を書き換えた写し）', stops(lambda: arm_pairs_from_defs(C2))[0])
    ctx = build_contexts(tok, C, LG, AT=AT)
    ck('抽出の文脈が台帳と一致（%d 文脈・長さ・主位置とそのトークン・ids_sha16）' % len(ctx), len(ctx) == 16,
       '・'.join('%s %d' % (k, len(v)) for k, v in ctx.items()))
    LG2 = copy.deepcopy(LG)
    LG2['extract_contexts']['S1|Osec']['ids_sha16'] = '0' * 16
    ck('台帳と違えば止まる（S1|Osec の ids_sha16 を書き換えた写し）', stops(lambda: build_contexts(tok, C, LG2, AT=AT))[0])
    LG2 = copy.deepcopy(LG)
    LG2['extract_contexts']['N1|Nk']['prompt_len'] += 1
    ck('台帳と違えば止まる（N1|Nk の prompt_len を +1 ずらした写し）', stops(lambda: build_contexts(tok, C, LG2, AT=AT))[0])

    for tn, m in models:
        top, _, lm = parts(m)
        nc0 = RW.capture_hook_count(m)
        t0 = time.time()
        acts = reextract(m, ctx, L)
        dt = time.time() - t0
        ok = (list(acts) == list(ctx) and all(isinstance(v, np.ndarray) and v.dtype == np.float64 and v.shape == (64,)
                                              and np.all(np.isfinite(v)) for v in acts.values()))
        ck('[%s] 取った値は有限・float64・形 (64,)・文脈の名がそろう（%d 文脈）' % (tn, len(acts)), ok, '%.1f 秒' % dt)
        nc1 = RW.capture_hook_count(m)
        print('[参考] [%s] 記録用の hook（transformers の output_capturing）: 前 %d 本 → 後 %d 本・それ以外の hook %d 本（判定に入れない）'
              % (tn, nc0, nc1, len(foreign_hooks(m))), flush=True)
        acts2 = reextract(m, ctx, L)
        ck('[%s] 同じ呼び出しを二度走らせて同じ値（ビット単位・二度目は記録用の hook が居残った模型）' % tn,
           all(np.array_equal(acts[k], acts2[k]) for k in ctx))
        # 書き換えの道の手回し（零の書き換え）の層 L の出力の主位置と一致するか（別の書き方どうしの突き合わせ）
        same = []
        for k in ('N1|O', 'S1|Onull-Ncold', 'N1|N'):
            keep = {}
            RW.forward_rewrite(m, ctx[k], L, np.zeros(64), 1.0, 1, len(ctx[k]) - 1, keep=keep)
            hv = keep['L_before'][0, -1].detach().to(torch.float64).numpy()
            same.append(np.array_equal(hv, acts[k]))
        ck('[%s] hidden_states[%d] の主位置が、手で層を回した道の層 %d の出力の主位置と一致（ビット単位・3 文脈）' % (tn, L + 1, L), all(same))
        ck('[%s] 最後の層（添字 %d）は取らずに止まる（hidden_states[-1] は最終の正規化の後）' % (tn, len(lm.layers) - 1),
           stops(lambda: reextract(m, {'N1|N': ctx['N1|N']}, len(lm.layers) - 1))[0])
        hd = lm.layers[L].register_forward_hook(lambda mod, a, o: None)
        try:
            ok_h, _ = stops(lambda: reextract(m, {'N1|N': ctx['N1|N']}, L))
        finally:
            hd.remove()
        ck('[%s] 模型に forward の hook が掛かっていれば止まる（選んだ層に何もしない hook を掛けた写し）' % tn, ok_h)
        # 名前のある方向の余弦: dirs に同じ方向を渡せば一
        D = named_directions(acts, C)
        r = reextract_all(m, tok, C, LG, D)
        ck('[%s] reextract_all: 文脈 %d・名前のある方向の余弦が dirs に同じ方向を渡したとき一（1−1e-12 以上）' % (tn, len(r['h_norm_by_context'])),
           set(r['h_norm_by_context']) == set(ctx) and all(v >= 1 - 1e-12 for v in r['named_cos'].values()),
           '・'.join('%s %.15f' % (k, v) for k, v in r['named_cos'].items()))
        ck('[%s] reextract_all: vhat_norm＝‖O の平均 − Osec の平均‖・h_norm_by_context＝‖h‖（ビット単位）' % tn,
           r['vhat_norm'] == float(np.linalg.norm(D['static']))
           and all(r['h_norm_by_context'][k] == float(np.linalg.norm(acts[k])) for k in ctx))
        D2 = dict(D)
        D2['static'] = -D['static']
        D2['loaded'] = D['Nk']
        r2 = reextract_all(m, tok, C, LG, D2)
        ck('[%s] 歯——static を反転した dirs の余弦は −1、loaded に Nk を渡した dirs の余弦は cos_min（%s）に届かない' % (tn, tol['cos_min']),
           r2['named_cos']['static'] <= -1 + 1e-12 and r2['named_cos']['loaded'] < float(tol['cos_min']),
           'static %.6f・loaded %.6f' % (r2['named_cos']['static'], r2['named_cos']['loaded']))
        D3 = dict(D)
        D3.pop('td')
        ck('[%s] dirs に名前のある方向が無ければ止まる' % tn, stops(lambda: reextract_all(m, tok, C, LG, D3))[0])
    n_ok = sum(res)
    print('selftest: %d/%d ok' % (n_ok, len(res)), flush=True)
    print('柵: ' + FENCE, flush=True)
    return n_ok == len(res)


def _dry():
    import torch
    import transformers
    from transformers import AutoTokenizer
    RW = _rw()
    C, LG = load_canon(), load_ledger()
    tol = C['independent_recompute']['reextract']
    rel_tol, cos_min = float(tol['rel_tol']), float(tol['cos_min'])
    RB = _pub('run_stageB_local')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    ctx = build_contexts(tok, C, LG, AT=AT)
    base = RW.tiny_model(C)
    m32 = RW.as_dtype(base, torch.float32)
    for m in (m32, base):
        RW.assert_tiny(m)
    L = layer_for(m32, C)
    sys.path.insert(0, os.path.join(BPRIME, 'tools'))
    import bprime_directions as BD
    print('bprime_reextract %s --dry  torch %s・transformers %s・numpy %s・注意の実装 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, parts(m32)[2].config._attn_implementation), flush=True)
    print('乱数の小さな模型: 次元 64・層 6・選んだ層の添字 %d・許容 independent_recompute.reextract の rel_tol = %s・cos_min = %s'
          % (L, rel_tol, cos_min), flush=True)
    print('比べる文脈（四つ）: %s' % '・'.join('%s（%d トークン）' % (k, len(ctx[k])) for k in DRY_CONTEXTS), flush=True)
    c4 = {k: ctx[k] for k in DRY_CONTEXTS}
    verdicts = []
    for tn, m in (('float32', m32), ('bfloat16', base)):
        try:
            t0 = time.time()
            A1, N1, _ = BD.activations(m, c4, L)                      # コーディネータの抽出の器（中を見ない）
            t1 = time.time()
        except BaseException as e:
            print('[%s] コーディネータの抽出の器が落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
            verdicts.append(False)
            continue
        mine = reextract(m, c4, L)
        t2 = time.time()
        try:
            A2, N2, _ = BD.activations(m, c4, L)                      # 記録用の hook が居残った模型でもう一度
        except BaseException as e:
            print('[参考] [%s] 二度目のコーディネータの抽出の器が落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
            A2 = None
        if set(A1) != set(c4):
            print('[%s] コーディネータの抽出の器の文脈の名が違う: %s' % (tn, sorted(A1)), flush=True)
            verdicts.append(False)
            continue
        rels, coss = [], []
        for k in DRY_CONTEXTS:
            a, b = np.asarray(mine[k], dtype=np.float64), np.asarray(A1[k], dtype=np.float64)
            rels.append(abs(np.linalg.norm(a) - np.linalg.norm(b)) / np.linalg.norm(b))
            coss.append(cosine(a, b))
        exact = all(np.array_equal(np.asarray(mine[k], dtype=np.float64), np.asarray(A1[k], dtype=np.float64)) for k in DRY_CONTEXTS)
        print('[%s] コーディネータの抽出の器 %.1f 秒・この道 %.1f 秒・返り値の型 %s／%s' % (tn, t1 - t0, t2 - t1, type(A1).__name__, type(N1).__name__), flush=True)
        print('[%s] ‖h‖ の相対の差の最大 %.3g・余弦の最小 %.12f・四つともビット単位で同じ: %s' % (tn, max(rels), min(coss), exact), flush=True)
        if isinstance(N1, dict) and set(N1) >= set(c4):
            try:
                rn = max(abs(float(np.linalg.norm(mine[k])) - float(N1[k])) / float(N1[k]) for k in DRY_CONTEXTS)
                print('[参考] [%s] コーディネータの器が返したノルムとこの道の ‖h‖ の相対の差の最大 %.3g（判定に入れない）' % (tn, rn), flush=True)
            except (TypeError, ValueError) as e:
                print('[参考] [%s] コーディネータの器が返したノルムを数として読めない: %s' % (tn, type(e).__name__), flush=True)
        if A2 is not None:
            print('[参考] [%s] 記録用の hook が居残った模型での二度目のコーディネータの抽出の器が一度目と同じ（ビット単位）: %s'
                  % (tn, all(np.array_equal(np.asarray(A1[k]), np.asarray(A2[k])) for k in DRY_CONTEXTS)), flush=True)
        ok = max(rels) <= rel_tol and min(coss) >= cos_min
        verdicts.append(ok)
        print('[%s] dry: 再抽出の許容（rel_tol %s・cos_min %s）の%s' % (tn, rel_tol, cos_min, '内' if ok else '外'), flush=True)
        # 参考: 十六文脈の全体で、コーディネータの抽出の器の値から作った名前のある方向を dirs に渡した reextract_all
        try:
            AF, _, _ = BD.activations(m, ctx, L)
            DB_ = named_directions(AF, C)
            r = reextract_all(m, tok, C, LG, DB_)
            vrel = abs(r['vhat_norm'] - float(np.linalg.norm(DB_['static']))) / float(np.linalg.norm(DB_['static']))
            hrel = max(abs(r['h_norm_by_context'][k] - float(np.linalg.norm(AF[k]))) / float(np.linalg.norm(AF[k])) for k in ctx)
            print('[参考] [%s] 十六文脈: reextract_all の名前のある方向の余弦の最小 %.12f・‖v̂‖ の相対の差 %.3g・‖h‖ の相対の差の最大 %.3g'
                  '（dirs はコーディネータの器の値からこの器の式で作った・判定に入れない）' % (tn, min(r['named_cos'].values()), vrel, hrel), flush=True)
        except BaseException as e:
            print('[参考] [%s] 十六文脈の参考の突き合わせが落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
    print('dry: %s' % ('二つの型とも再抽出の許容の内' if verdicts and all(verdicts) else '許容の外か比べられなかった型がある'), flush=True)
    print('柵: ' + FENCE, flush=True)
    return bool(verdicts) and all(verdicts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.dry:
        sys.exit(0 if _dry() else 1)
    ap.print_help()


if __name__ == '__main__':
    main()
