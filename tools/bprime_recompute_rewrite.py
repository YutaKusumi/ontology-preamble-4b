# -*- coding: utf-8 -*-
"""bprime_recompute_rewrite.py v1 —— B′（Gemma-4-31B-it）の独立の再計算の器のうち、**残差の書き換えの道**
（2026-09-30・本の器の書き手〔コーディネータ・南無弥勒如来〕と別の系統内の個体が書いた・登録者の裁定 D270 による・独立の目を通っていない）。

正本 `design/contrasts-Bprime.json` の `independent_recompute`（一段目の相手）・`readout.primary`・`layers`・`inputs.model_facts`・
`nulls.real`・`main_rows`・`cells_main` に従う。コーディネータの器（`bprime_run` ほか）の中身を**読まずに**書いた。
`--dry` でだけ、その公開の関数を中を見ずに呼び、数を突き合わせる。

道（加減をフックでなく、選んだ層の出力を書き換えて後の層を流す・近道なし・バッチ一）:
  入力     段階 B の組み立て（`run_stageB_local.user_message(腕の本文, 場面の本文, 指示)`・場面と指示は
           `run_stageB_local.scenario_and_instruction`）の user の発話一つに Gemma のチャットの型（system なし・生成の口つき）を当て、
           その直後に主の書き出し（台帳の `prefix_ids`）を**トークンの並びのまま**つなぐ。主位置＝プロンプトの長さ−1（`<channel|>`）・
           読み取りの位置＝列の最後。升目ごとに台帳の prompt_len・main_position・main_position_token・readout_position・ids_sha16・
           族・読み取りの集合と照らし、違えば止める。
  層を回す transformers 5.16.1 の `Gemma4ForConditionalGeneration.forward` → `Gemma4Model.forward` → `Gemma4TextModel.forward` の
           文字だけの入力の手順を、部品を差し替えずに写す: 置き換えの印（画像・動画・音声のトークン）の確かめ → 埋め込み
           （`get_input_embeddings()`・倍率 √hidden は埋め込みの部品の中）→（層ごとの入力があれば `get_per_layer_inputs` と
           `project_per_layer_inputs`）→ 位置の番号 → mask（多様式の本体と同じく `create_masks_for_generate` を past_key_values=None で
           呼ぶ・窓つきと全体の二つの型）→ rotary（注意の型ごとに `rotary_emb(h, position_ids, 型)`）→ 空の `UserDict` の
           shared_kv_states → 層 0〜最後を模型の forward と同じ引数で一つずつ呼ぶ。層 L の出力を得た直後に書き換える。
           cache: 既定は use_cache=False と同じ（層に past_key_values=None）。use_cache=None なら模型の forward の既定
           （設定の use_cache・一回ごとに空の DynamicCache を作って捨てる）に合わせる（開発の記録の「決まっていなかった所」）。
  書き換え 層 L の出力の、主位置から列の最後までの位置に sign×coef×v を足す。v（float64）は段階 B の走行器のフック（`make_hook`）と
           同じ算術で、NumPy の float32 を経て**層の出力の型**に直してから `sign * coef *` を掛け、その型のまま足す（係数は一度だけ）。
  読み取り 最後の層の出力（**最終の正規化の入力**。`hidden_states[-1]` は正規化の後の値なので使わない）の最後の位置を float32 に上げ、
           最終の正規化を float32 で当て（h × rsqrt(mean(h²)+eps) × g・g と eps は模型の最終の正規化から・1＋g ではない）、
           語彙の行列（埋め込みと共有の `lm_head.weight`）の読み取りの集合の行（a が先頭・最後が refuse の頭）を float32 で当て、
           softcap（cap × tanh(z ÷ cap)・cap は `text_config.final_logit_softcapping`）を掛ける。
           量＝z_a − logsumexp（ほかの選択の文字と refuse の頭）。効き目＝加えた値 − 無操作（零のベクトル）の値。
出力: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}（符号の書き方は '%+d'）。行と方向の組は
      `bl3_core.recompute_set`。**値は印字しない**（正本 `independent_recompute.print`）。`--dry` が差の最大を印字するのは乱数の小さな模型だけ。
**フックは使わない**: 呼ぶ前と後に、模型のどの部品にも forward の hook（前・後・大域）が無いことを確かめ、あれば止める。
ただし transformers 5 が `output_hidden_states` などの初回に据え付けて居残らせる記録用の hook
（`transformers.utils.output_capturing` の `output_capturing_hook`・値を変えない）だけは数えない。
用法: python bprime_recompute_rewrite.py --selftest   （乱数の小さな模型で自己検査）
      python bprime_recompute_rewrite.py --dry        （乱数の小さな模型で、コーディネータのフックの道と一段目の許容で突き合わせ）
走らせ方: PYTHONPATH=<Bprime>/pylib（transformers 5.16.1）・PYTHONDONTWRITEBYTECODE=1 を勧める。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import sys
if __name__ == '__main__':
    sys.dont_write_bytecode = True          # 外の置き場（公開の置き場・pylib・Bprime/tools）に .pyc を書かない
import os, json, time, copy, hashlib, argparse
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
# 乱数の小さな模型（指示の作り方）
TINY_TEXT = dict(hidden_size=64, intermediate_size=128, num_hidden_layers=6, num_attention_heads=4, num_key_value_heads=2,
                 head_dim=16, global_head_dim=32, num_global_key_value_heads=1, sliding_window=8)
TINY_VISION = dict(hidden_size=32, intermediate_size=64, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2,
                   head_dim=16, global_head_dim=16)
TINY_COEF = 2.0            # 確かめの係数（書き手の選び・層三の係数と同じ値・本の計算の係数は呼び手が渡す）
TINY_N_ISO = 10            # 確かめの等方の本数（指示の「等方の十本」）
SYN_NORM_FRAC = 0.5        # 合成の方向のノルム＝残差のノルム × 0.5（指示）


def _die(msg):
    raise SystemExit('bprime_recompute_rewrite: ' + msg)


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


# ---------------------------------------------------------------- 模型の部品と確かめ（止める）

def parts(model):
    """(最上位 Gemma4ForConditionalGeneration, 多様式の本体 Gemma4Model, 言語の模型 Gemma4TextModel)。"""
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
    """transformers 5 の記録用の hook（値を変えない・output_* の初回に据え付けられて居残る）か。"""
    return getattr(fn, '__module__', None) == CAPTURE_MODULE and getattr(fn, '__name__', None) == 'output_capturing_hook'


def foreign_hooks(model):
    """記録用の hook を除いた forward の hook（前・後）と大域の hook の一覧。"""
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
        _die('模型に forward の hook が掛かっている（この道はフックを使わず、掛け残しも混ぜない）: ' + '・'.join(bad))


def is_real(model, C):
    """正本の模型の事実（層の数・次元）と同じ形の模型か（実の重みの本の計算）。"""
    _, _, lm = parts(model)
    mf = C['inputs']['model_facts']
    return len(lm.layers) == int(mf['num_hidden_layers']) and int(lm.config.hidden_size) == int(mf['hidden_size'])


def softcap_value(model):
    top, _, _ = parts(model)
    cap = top.config.get_text_config().final_logit_softcapping
    if cap is None:
        _die('text_config.final_logit_softcapping が無い（正本 readout.primary.quantity は softcap を掛ける）')
    return float(cap)


def check_env(model, C, ledger):
    """版・機種・形の確かめ。手回しの道は transformers 5.16.1 の forward を写したので、版が違えば止める。"""
    import torch
    import transformers
    want = str(ledger['meta']['transformers'])
    if transformers.__version__ != want:
        _die('transformers の版が %s（手回しの道は %s の Gemma4 の forward を写した・台帳 meta.transformers）'
             % (transformers.__version__, want))
    top, mm, lm = parts(model)
    if top.training or mm.training or lm.training:
        _die('模型が訓練の形（eval にしていない）')
    obj = top
    for p in str(C['layers']['layer_path']).split('.'):
        obj = getattr(obj, p, None)
    if obj is not lm.layers:
        _die('正本 layers.layer_path（%s）が言語の模型の層の並びを指さない' % C['layers']['layer_path'])
    n = len(lm.layers)
    if n != int(lm.config.num_hidden_layers):
        _die('層の並びの数（%d）が設定の層の数（%d）と違う' % (n, lm.config.num_hidden_layers))
    if top.lm_head.weight is not lm.embed_tokens.weight:
        _die('語彙の行列（lm_head.weight）が埋め込みと共有でない')
    if type(lm.norm).__name__ != 'Gemma4RMSNorm' or not getattr(lm.norm, 'with_scale', False):
        _die('最終の正規化が重みつきの Gemma4RMSNorm でない: %s' % type(lm.norm).__name__)
    if float(lm.norm.eps) != float(lm.config.rms_norm_eps):
        _die('最終の正規化の eps（%r）が設定の rms_norm_eps（%r）と違う' % (lm.norm.eps, lm.config.rms_norm_eps))
    cap = softcap_value(model)
    if is_real(model, C):
        mf = C['inputs']['model_facts']
        if lm.embed_tokens.weight.dtype != torch.bfloat16:
            _die('本の計算の模型が bf16 でない（%s・正本 readout.primary.precision）' % lm.embed_tokens.weight.dtype)
        if cap != float(mf['final_logit_softcapping']) or mf.get('softcap_level') != 'text_config':
            _die('softcap（%r）が正本 inputs.model_facts と違う' % cap)
        if int(lm.config.vocab_size) != int(mf['vocab_size']) or int(lm.config.sliding_window) != int(mf['sliding_window']):
            _die('語彙の数か窓が正本 inputs.model_facts と違う')
        if sum(1 for t in lm.config.layer_types if t == 'full_attention') != int(mf['full_attention_layers']):
            _die('全体の注意の層の数が正本 inputs.model_facts と違う')


def layer_index_for(model, C):
    """選ぶ層の添字: `direction_B.layer_index(正本 layers.ratio, 模型の層の数)`。本の模型では正本 `layers.index` とも照らす。"""
    DB = _pub('direction_B')
    _, _, lm = parts(model)
    n = len(lm.layers)
    L = DB.layer_index(float(C['layers']['ratio']), n)
    if is_real(model, C):
        if L != int(C['layers']['index']) or int(C['layers']['hidden_states_index']) != L + 1:
            _die('層の添字 %d が正本 layers.index（%s）・hidden_states_index（%s）と合わない'
                 % (L, C['layers']['index'], C['layers']['hidden_states_index']))
    if lm.config.layer_types[L] != C['layers']['layer_type']:
        _die('選ぶ層 %d の種類 %s が正本 layers.layer_type（%s）と違う' % (L, lm.config.layer_types[L], C['layers']['layer_type']))
    return L


# ---------------------------------------------------------------- 升目の入力（段階 B の組み立てのまま）

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


def cell_input(tok, C, ledger, cell_key, AT=None):
    """升目（'場面|土台の腕'）の入力を組み立て、台帳 `cells_main` の升目の記録と照らす（違えば止める）。

    返り値: {'cell', 'ids'（プロンプト＋主の書き出し）, 'prompt_len', 'mp'（主位置）, 'ro'（読み取りの位置＝列の最後）,
             'family', 'letters', 'set_ids'（a が先頭・最後が refuse の頭）}。"""
    RB = _pub('run_stageB_local')
    RP = C['readout']['primary']
    LC = ledger['cells_main']
    if cell_key not in LC:
        _die('升目 %s が台帳 cells_main に無い' % cell_key)
    rec = LC[cell_key]
    sp = cell_key.split('|')
    if len(sp) != 2:
        _die('升目の鍵の形が違う（場面|土台の腕）: %s' % cell_key)
    scen, arm = sp
    if rec.get('scenario') != scen or rec.get('arm') != arm:
        _die('台帳の升目 %s の場面か腕が鍵と違う' % cell_key)
    if [scen, arm] not in [list(x) for x in C['cells_main']]:
        _die('升目 %s が正本 cells_main に無い' % cell_key)
    s, inst = RB.scenario_and_instruction(scen)
    AT = AT if AT is not None else RB.arm_texts()
    if arm not in AT:
        _die('土台の腕 %s の本文が引けない' % arm)
    prompt = chat_ids(tok, RB.user_message(AT[arm]['text'], s['text'], inst))
    prefix = [int(x) for x in ledger['prefix_ids']]
    if prefix != [int(x) for x in RP['prefix_ids']]:
        _die('台帳の prefix_ids が正本 readout.primary.prefix_ids と違う')
    ids = prompt + prefix
    mp, ro = len(prompt) - 1, len(ids) - 1
    fam = s.get('family')
    bad = []
    if len(prompt) != int(rec['prompt_len']):
        bad.append('プロンプトの長さ %d（台帳 %s）' % (len(prompt), rec['prompt_len']))
    if mp != int(rec['main_position']):
        bad.append('主位置 %d（台帳 %s）' % (mp, rec['main_position']))
    if tok.convert_ids_to_tokens(prompt[-1]) != rec['main_position_token']:
        bad.append('主位置のトークン %r（台帳 %r）' % (tok.convert_ids_to_tokens(prompt[-1]), rec['main_position_token']))
    if ro != int(rec['readout_position']):
        bad.append('読み取りの位置 %d（台帳 %s）' % (ro, rec['readout_position']))
    if sha16_ids(ids) != rec['ids_sha16']:
        bad.append('ids_sha16 %s（台帳 %s）' % (sha16_ids(ids), rec['ids_sha16']))
    if fam != rec.get('family'):
        bad.append('族 %s（台帳 %s）' % (fam, rec.get('family')))
    if bad:
        _die('升目 %s の入力が台帳と違う: %s' % (cell_key, '・'.join(bad)))
    if fam not in RP['letters']:
        _die('族 %s の選択の文字が正本 readout.primary.letters に無い' % fam)
    letters = list(RP['letters'][fam])
    if letters[0] != RP['catastrophe_letter'] or letters != list(rec['letters']):
        _die('升目 %s の選択の文字（%s）が正本と台帳で合わないか、先頭が破局の側の文字でない' % (cell_key, letters))
    SI = RP['set_ids']
    set_ids = [int(SI[x]) for x in letters] + [int(SI['refuse'])]
    if set_ids != [int(x) for x in rec['set_ids']]:
        _die('升目 %s の読み取りの集合が正本 readout.primary.set_ids と台帳で違う' % cell_key)
    for x in list(letters) + ['refuse']:
        if int(ledger['heads'][x]['next']) != int(SI[x]):
            _die('台帳 heads.%s.next が正本 set_ids と違う' % x)
    want = letters + [RP['refuse_head']]
    got = [tok.convert_ids_to_tokens(i) for i in set_ids]
    if got != want or got != list(rec['set_pieces']):
        _die('読み取りの集合のトークンが文字と refuse の頭に戻らない: %s 対 %s' % (got, want))
    if len(set(set_ids)) != len(set_ids):
        _die('読み取りの集合のトークンが重なる')
    return {'cell': cell_key, 'ids': ids, 'prompt_len': len(prompt), 'mp': mp, 'ro': ro,
            'family': fam, 'letters': letters, 'set_ids': set_ids}


# ---------------------------------------------------------------- 手回しの順伝播

def resolve_use_cache(model, use_cache):
    """use_cache=None のとき、模型の forward と同じ解き方（最上位の設定 → 言語の設定の use_cache）。"""
    if use_cache is not None:
        return bool(use_cache)
    top, _, lm = parts(model)
    v = getattr(top.config, 'use_cache', None)
    if v is None:
        v = getattr(lm.config, 'use_cache', None)
    return bool(v)


def _forward_impl(model, ids, on_layer_out, use_cache=False, keep=None):
    """文字だけの入力で模型の forward を手で写して層を回す。層 i の出力を得るたびに on_layer_out(i, h) を通す。

    返り値: 最後の層の出力（最終の正規化の入力・模型の型・形 [1, 列の長さ, 次元]）。"""
    import torch
    from collections import UserDict
    import transformers.models.gemma4.modeling_gemma4 as MG         # 模型の組み立てが呼ぶのと同じ名の束ね
    top, mm, lm = parts(model)
    tcfg = lm.config
    uc = resolve_use_cache(model, use_cache)
    with torch.no_grad():
        dev = lm.embed_tokens.weight.device
        input_ids = torch.tensor([[int(x) for x in ids]], dtype=torch.long, device=dev)
        # Gemma4Model.forward: 置き換えの印（文字だけの入力では無い）
        image_mask, video_mask, audio_mask = mm.get_placeholder_mask(input_ids, None)
        multimodal_mask = image_mask | video_mask | audio_mask
        if bool(multimodal_mask.any()):
            _die('列に画像・動画・音声の置き換えの印がある（文字だけの入力しか写していない）')
        llm_input_ids = torch.where(multimodal_mask, top.config.text_config.pad_token_id, input_ids)
        inputs_embeds = mm.get_input_embeddings()(llm_input_ids)            # 倍率 √hidden は埋め込みの部品の中
        per_layer_inputs = None
        if top.config.get_text_config().hidden_size_per_layer_input:
            pad_embedding = lm.embed_tokens.weight[top.config.text_config.pad_token_id, :]
            mmask = multimodal_mask.to(inputs_embeds.device)
            llm_inputs_embeds = torch.where(mmask[..., None], pad_embedding.view(1, 1, -1), inputs_embeds)
            per_layer_inputs = lm.get_per_layer_inputs(llm_input_ids, llm_inputs_embeds)
        position_ids = torch.arange(inputs_embeds.shape[1], device=inputs_embeds.device).unsqueeze(0)
        masks = MG.create_masks_for_generate(config=top.config.get_text_config(), inputs_embeds=inputs_embeds,
                                             attention_mask=None, past_key_values=None, position_ids=position_ids)
        if not isinstance(masks, dict) or set(masks) != set(tcfg.layer_types):
            _die('mask の形が注意の型ごとの辞書でない')
        # Gemma4TextModel.forward
        if lm.hidden_size_per_layer_input:
            per_layer_inputs = lm.project_per_layer_inputs(inputs_embeds, per_layer_inputs)
        past = MG.DynamicCache(config=lm.config) if uc else None           # 一回ごとに作って捨てる（順伝播をまたいで使い回さない）
        h = inputs_embeds
        pe = {lt: lm.rotary_emb(h, position_ids, lt) for lt in lm.unique_layer_types}
        shared = UserDict()
        if keep is not None:
            keep['masks'] = masks
            keep['use_cache'] = uc
            keep['embeds'] = inputs_embeds.clone()
        for i, layer in enumerate(lm.layers[: tcfg.num_hidden_layers]):
            lt = tcfg.layer_types[i]
            pli = per_layer_inputs[:, :, i, :] if per_layer_inputs is not None else None
            h = layer(h, pli, shared_kv_states=shared, position_embeddings=pe[lt], attention_mask=masks[lt],
                      position_ids=position_ids, past_key_values=past)
            h = on_layer_out(i, h)
            if keep is not None:
                keep.setdefault('outs', []).append(h.clone())
    if h.shape[1] != len(ids):
        _die('出口の列の長さ %d が入力の長さ %d と違う' % (h.shape[1], len(ids)))
    return h


def cast_add(vec, coef, sign, like):
    """段階 B の `make_hook` の算術: NumPy の float32 を経て層の出力の型に直し、Python の数 sign×coef を掛ける。"""
    import torch
    V32 = np.asarray(vec, dtype=np.float32)
    return int(sign) * float(coef) * torch.as_tensor(V32, dtype=like.dtype, device=like.device)


def forward_rewrite(model, ids, layer_idx, vec, coef, sign, mp, use_cache=False, keep=None):
    """埋め込みから層を手で回し、層 layer_idx の出力の主位置から列の最後までに sign×coef×v を足して後の層を流す。

    返り値: 最後の層の出力（最終の正規化の入力）。keep（dict）を渡すと、自己検査のために層ごとの出力・書き換えの前と後・
    足した量を写しで残す。"""
    _, _, lm = parts(model)
    L, mp, n = int(layer_idx), int(mp), len(ids)
    if not 0 <= L < len(lm.layers):
        _die('層の添字 %s が範囲の外（層の数 %d）' % (layer_idx, len(lm.layers)))
    if not 0 <= mp < n:
        _die('主位置 %s が列の外（長さ %d）' % (mp, n))
    if int(sign) not in (1, -1):
        _die('符号は +1 か -1: %r' % (sign,))
    if np.asarray(vec).shape != (int(lm.config.hidden_size),):
        _die('方向の形 %s が次元（%d）と合わない' % (np.asarray(vec).shape, lm.config.hidden_size))
    done = []

    def on_layer_out(i, h):
        if i == L:
            if keep is not None:
                keep['L_before'] = h.clone()
            add = cast_add(vec, coef, sign, h)
            h[0, mp:, :] = h[0, mp:, :] + add                      # 主位置から後ろに、層の出力の型のまま足す
            done.append(i)
            if keep is not None:
                keep['L_after'] = h.clone()
                keep['add'] = add.clone()
        return h

    h = _forward_impl(model, ids, on_layer_out, use_cache=use_cache, keep=keep)
    if done != [L]:
        _die('書き換えが一度でない: %s' % done)
    return h


def readout(model, h_last, set_ids, cap=None):
    """最終の正規化の入力（一つの位置）を float32 に上げ、最終の正規化・読み取りの集合の行・softcap を float32 で当てる。

    返り値: (量〔z_a − logsumexp(ほか)〕, 出口の値 z〔float32・set_ids の順〕)。"""
    import torch
    top, _, lm = parts(model)
    cap = softcap_value(model) if cap is None else float(cap)
    with torch.no_grad():
        g = lm.norm.weight.to(torch.float32)
        eps = float(lm.norm.eps)
        x = h_last.to(device=g.device, dtype=torch.float32)
        xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g          # 重みをそのまま掛ける（1＋g ではない）
        W = top.lm_head.weight
        idx = torch.as_tensor([int(i) for i in set_ids], dtype=torch.long, device=W.device)
        z = W.index_select(0, idx).to(torch.float32) @ xn.to(W.device)
        z = cap * torch.tanh(z / cap)
        lo = z[0] - torch.logsumexp(z[1:], dim=0)
    return float(lo), z


# ---------------------------------------------------------------- 本の関数

def _check_dirs(model, dirs, used):
    _, _, lm = parts(model)
    d = int(lm.config.hidden_size)
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


def rows_and_dirs(C, ledger, names, pilot):
    """行と方向の組（`bl3_core.recompute_set`）。外した升目は `pilot['decision']['dropped']`。"""
    BC = _pub('bl3_core')
    for k in ('named', 'iso', 'real'):
        if k not in names:
            _die('names に %s の並びが無い' % k)
    real = list(names['real'])
    bad = [x for x in real if not str(x).startswith('real:')]
    if bad:
        _die('names["real"] に real: で始まらない名がある: %s' % bad[:3])
    pair_names = [str(x)[len('real:'):] for x in real]
    iso = list(names['iso'])
    if set(iso) != {'iso:%d' % i for i in range(len(iso))} or len(set(iso)) != len(iso):
        _die('names["iso"] が iso:0〜iso:%d の名の並びでない（recompute_set は iso:番号 の名を作る）' % (len(iso) - 1))
    try:
        dropped = pilot['decision']['dropped']
    except (TypeError, KeyError):
        _die("pilot['decision']['dropped']（外した升目の鍵の並び）が無い")
    if not isinstance(dropped, (list, tuple)) or any(not isinstance(x, str) for x in dropped):
        _die("pilot['decision']['dropped'] が升目の鍵（文字列）の並びでない")
    unknown = [x for x in dropped if x not in ledger['cells_main']]
    if unknown:
        _die("pilot['decision']['dropped'] に台帳 cells_main に無い升目の鍵がある: %s" % unknown)
    rows, dbr = BC.recompute_set(C['main_rows'], pair_names, C['nulls']['real']['swap_siblings'], len(iso), list(dropped))
    return rows, dbr


def recompute_rewrite(model, tok, C, ledger, dirs, names, pilot, coef, use_cache=False):
    """残差の書き換えの道で、v̂ の行ごとに無操作の量と、方向と符号ごとの効き目を計算し直す（近道なし・バッチ一）。

    C: 正本の辞書・ledger: 台帳の辞書・dirs: 方向の名 → float64 のベクトル・names: {'named','iso','real'} の名の並び・
    pilot: 本の凍結の下見の記録（pilot['decision']['dropped'] に外した升目の鍵）・coef: 係数。
    返り値: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}。**値は印字しない。**
    use_cache（既定 False＝use_cache=False と同じ）は、手回しの道の中で DynamicCache を作るかだけを決める（開発の記録）。"""
    check_env(model, C, ledger)
    L = layer_index_for(model, C)
    assert_no_foreign_hooks(model)
    coef = float(coef)
    if not np.isfinite(coef) or coef <= 0:
        _die('係数が正の有限の数でない: %r' % coef)
    rows, dbr = rows_and_dirs(C, ledger, names, pilot)
    used = sorted({dn for nm, _, _ in rows for dn, _ in dbr[nm]})
    _check_dirs(model, dirs, used)
    _, _, lm = parts(model)
    cap = softcap_value(model)
    RB = _pub('run_stageB_local')
    AT = RB.arm_texts()
    zero = np.zeros(int(lm.config.hidden_size), dtype=np.float64)       # 無操作は零のベクトル（同じ算術で足す）
    cells, out = {}, {}
    for name, ck, sign in rows:
        sign = int(sign)
        if sign not in (1, -1):
            _die('行 %s の符号は +1 か -1: %r' % (name, sign))
        if ck not in cells:
            cells[ck] = cell_input(tok, C, ledger, ck, AT=AT)
        c = cells[ck]
        h0 = forward_rewrite(model, c['ids'], L, zero, coef, sign, c['mp'], use_cache=use_cache)
        lo0, _ = readout(model, h0[0, -1], c['set_ids'], cap)
        eff = {}
        for dn, s in dbr[name]:
            s = int(s)
            if s not in (1, -1):
                _die('方向 %s の符号は +1 か -1: %r' % (dn, s))
            key = '%s|%+d' % (dn, s)
            if key in eff:
                _die('行 %s に同じ方向と符号が二度ある: %s' % (name, key))
            h = forward_rewrite(model, c['ids'], L, dirs[dn], coef, s, c['mp'], use_cache=use_cache)
            lo, _ = readout(model, h[0, -1], c['set_ids'], cap)
            eff[key] = lo - lo0
        out[name] = {'noop_lo': lo0, 'effects': eff}
    assert_no_foreign_hooks(model)
    return out


# ---------------------------------------------------------------- 乱数の小さな模型と合成の方向（確かめだけ）

def tiny_config_dict(C, variant=None):
    """設定の置き場の config.json を辞書で読み、text_config と vision_config を縮める（指示の作り方）。
    variant='ple_scalar' は、層ごとの入力（hidden_size_per_layer_input 8）を足した自己検査の変種。"""
    DB = _pub('direction_B')
    d = json.load(open(os.path.join(HF_DIR, 'config.json'), encoding='utf-8'))
    tc = d['text_config']
    tc.update(TINY_TEXT)
    n = int(TINY_TEXT['num_hidden_layers'])
    L = DB.layer_index(float(C['layers']['ratio']), n)
    tc['layer_types'] = ['full_attention' if i in (L, n - 1) else 'sliding_attention' for i in range(n)]
    d['vision_config'].update(TINY_VISION)
    if variant == 'ple_scalar':
        tc['hidden_size_per_layer_input'] = 8
    elif variant is not None:
        _die('小さな模型の変種の名が違う: %s' % variant)
    return d


def tiny_model(C, variant=None):
    """乱数の小さな模型（**実の重みは読まない**）。torch.manual_seed(0) → Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).eval()
    → 語彙の行列（埋め込みと共有）を 4 倍 → 最後の正規化の重みを一様乱数 [2, 3) に（生成器の種 1）。型は設定の dtype のまま。
    variant='ple_scalar' では、さらに層ごとの layer_scalar を一様乱数 [0.5, 1.5) にする（本の模型は layer_scalar を読み込む）。"""
    import torch
    from transformers import Gemma4Config, Gemma4ForConditionalGeneration
    d = tiny_config_dict(C, variant)
    torch.manual_seed(0)
    model = Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).eval()
    top, _, lm = parts(model)
    g = torch.Generator().manual_seed(1)
    with torch.no_grad():
        lm.embed_tokens.weight.mul_(4.0)
        lm.norm.weight.copy_(torch.rand(lm.norm.weight.shape, generator=g) + 2.0)
        if variant == 'ple_scalar':
            for layer in lm.layers:
                layer.layer_scalar.copy_(torch.rand(layer.layer_scalar.shape, generator=g) + 0.5)
    if top.lm_head.weight is not lm.embed_tokens.weight:
        _die('小さな模型で語彙の行列が埋め込みと共有でない')
    return model


def as_dtype(model, dtype):
    """同じ重みの写しを別の型で（float32 の確かめ用）。共有の語彙の行列が共有のままかを確かめる。"""
    m = copy.deepcopy(model).to(dtype).eval()
    top, _, lm = parts(m)
    if top.lm_head.weight is not lm.embed_tokens.weight:
        _die('型を替えた写しで語彙の行列の共有が切れた')
    return m


def assert_tiny(model):
    """確かめは乱数の小さな模型だけで走らせる（封印の前に本物の模型で読み取りの値を出さない）。"""
    _, _, lm = parts(model)
    if int(lm.config.hidden_size) != TINY_TEXT['hidden_size'] or len(lm.layers) != TINY_TEXT['num_hidden_layers']:
        _die('確かめは乱数の小さな模型だけで走らせる（次元 %s・層 %s）' % (lm.config.hidden_size, len(lm.layers)))


def residual_norm(model, tok, C, ledger, L, AT=None):
    """残差のノルム: 主の八升目の、層 L の出力（書き換えなし）の主位置のノルムの平均。"""
    import torch
    _, _, lm = parts(model)
    zero = np.zeros(int(lm.config.hidden_size))
    ns = []
    for ck in ledger['cells_main']:
        c = cell_input(tok, C, ledger, ck, AT=AT)
        keep = {}
        forward_rewrite(model, c['ids'], L, zero, 1.0, 1, c['mp'], keep=keep)
        ns.append(float(torch.linalg.vector_norm(keep['L_before'][0, c['mp']].to(torch.float64))))
    return float(np.mean(ns)), ns


def synthetic_dirs(C, d, target_norm, n_iso=TINY_N_ISO):
    """合成の方向: `np.random.default_rng(5)` で次元 d の正規乱数を名の順に引き、ノルムを target_norm にそろえる。
    名の順は static・loaded・Nk・td（正本 directions.named）・iso:0〜・real:＋正本の八腕（nulls.real.arms）の全ての対（i<j）。"""
    arms = list(C['nulls']['real']['arms'])
    pairs = ['%s~%s' % (arms[i], arms[j]) for i in range(len(arms)) for j in range(i + 1, len(arms))]
    named = list(C['directions']['named'])
    iso = ['iso:%d' % k for k in range(n_iso)]
    real = ['real:' + p for p in pairs]
    rng = np.random.default_rng(5)
    dirs = {}
    for nm in named + iso + real:
        v = rng.normal(size=d)
        dirs[nm] = v * (float(target_norm) / float(np.linalg.norm(v)))
    return dirs, {'named': named, 'iso': iso, 'real': real}


def dry_rows(C, ledger):
    """主の行のうち方向が static の行から、減算の行（main_rows の順で最初）と、族を両方覆うため減算の行と違う族の最初の加算の行。"""
    fam = lambda r: ledger['cells_main']['%s|%s' % (r['scenario'], r['base'])]['family']
    main = [r for r in C['main_rows'] if r['direction'] == 'static']
    sub = next(r for r in main if int(r['sign']) == -1)
    add = next((r for r in main if int(r['sign']) == 1 and fam(r) != fam(sub)), None) or \
        next(r for r in main if int(r['sign']) == 1)
    return [(r['id'], '%s|%s' % (r['scenario'], r['base']), int(r['sign'])) for r in (sub, add)]


def max_abs_diff(A, B):
    """二つの結果の、全ての効き目と無操作の量の差の絶対値の最大（行か鍵の集合が違えば None）。"""
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


def _dtype_name(model):
    _, _, lm = parts(model)
    return str(lm.embed_tokens.weight.dtype).replace('torch.', '')


def _tiny_desc(model, L):
    """小さな模型の形の一行（頭の次元と KV の頭は層ごとの値なので層の部品から読む）。"""
    _, _, lm = parts(model)
    lt = lm.config.layer_types

    def att(i):
        a = lm.layers[i].self_attn
        return 'KV の頭 %d・頭の次元 %d' % (lm.config.num_attention_heads // a.num_key_value_groups, a.head_dim)
    i_s = next(i for i, t in enumerate(lt) if t == 'sliding_attention')
    return ('次元 %d・層 %d（%s）・注意の頭 %d・窓つきの層 %s・全体の層 %s・窓 %d・選んだ層の添字 %d（%s）・'
            '埋め込みの倍率 %s・softcap %s・係数 %s'
            % (int(lm.config.hidden_size), len(lm.layers), '/'.join('F' if t == 'full_attention' else 'S' for t in lt),
               lm.config.num_attention_heads, att(i_s), att(L), lm.config.sliding_window, L, lt[L],
               lm.embed_tokens.scalar_embed_scale, softcap_value(model), TINY_COEF))


# ---------------------------------------------------------------- 自己検査

def _selftest():
    import torch
    import transformers
    from transformers import AutoTokenizer
    C, LG = load_canon(), load_ledger()
    RB = _pub('run_stageB_local')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    base = tiny_model(C)
    models = [('float32', as_dtype(base, torch.float32)), ('bfloat16', base)]
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
    for _, m in models:
        assert_tiny(m)
    _, _, lm32 = parts(m32)
    L = layer_index_for(m32, C)
    d = int(lm32.config.hidden_size)
    print('bprime_recompute_rewrite %s --selftest  torch %s・transformers %s・numpy %s・注意の実装 %s・作ったままの型 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, lm32.config._attn_implementation,
             _dtype_name(base)), flush=True)
    print('乱数の小さな模型: %s' % _tiny_desc(m32, L), flush=True)

    # (1) 升目の組み立て（主の八升目）
    CI = {k: cell_input(tok, C, LG, k, AT=AT) for k in LG['cells_main']}
    ck('升目の組み立てが台帳と一致（全 %d 升目・長さ・主位置とそのトークン・読み取りの位置・ids_sha16・族・読み取りの集合）' % len(CI), True,
       '・'.join('%s %d/%d/%d' % (k, c['prompt_len'], c['mp'], c['ro']) for k, c in CI.items()))
    for fld, dv in (('prompt_len', 1), ('main_position', 1), ('readout_position', -1)):
        LG2 = copy.deepcopy(LG)
        LG2['cells_main']['S1|O-Ncold'][fld] += dv
        ok, _ = stops(lambda: cell_input(tok, C, LG2, 'S1|O-Ncold', AT=AT))
        ck('台帳と違えば止まる（S1|O-Ncold の %s を %+d ずらした写し）' % (fld, dv), ok)
    LG2 = copy.deepcopy(LG)
    LG2['cells_main']['S1|O-Ncold']['ids_sha16'] = '0' * 16
    ck('台帳と違えば止まる（S1|O-Ncold の ids_sha16 を書き換えた写し）', stops(lambda: cell_input(tok, C, LG2, 'S1|O-Ncold', AT=AT))[0])
    LG2 = copy.deepcopy(LG)
    LG2['prefix_ids'] = list(LG2['prefix_ids'])[:-1]
    ck('主の書き出しが正本と違えば止まる（最後のトークンを落とした写し）', stops(lambda: cell_input(tok, C, LG2, 'S1|O-Ncold', AT=AT))[0])

    zero = np.zeros(d)
    probe = ['N1|O-Ncold', 'S1|Onull']
    # (2) 書き換えを零にした手回しの道の最終の正規化の入力 ＝ 模型そのものの forward の最終の正規化の入力（前の hook で取るだけ）
    for tn, m in models:
        top, _, lm = parts(m)
        cap_v = softcap_value(m)
        for k in probe:
            c = CI[k]
            x = torch.tensor([c['ids']], dtype=torch.long)
            for uc, label in ((False, 'use_cache=False'), (None, '既定（設定の use_cache）')):
                cap = {}
                hd = lm.norm.register_forward_pre_hook(lambda mod, a: cap.__setitem__('x', a[0].detach().clone()))
                try:
                    with torch.no_grad():
                        o = m(input_ids=x, logits_to_keep=1) if uc is None else m(input_ids=x, use_cache=uc, logits_to_keep=1)
                finally:
                    hd.remove()
                assert_no_foreign_hooks(m)
                keep = {}
                h = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=uc, keep=keep)
                md = float((h.float() - cap['x'].float()).abs().max())
                ck('[%s] %s %s: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）' % (tn, k, label),
                   torch.equal(h, cap['x']), '差の絶対値の最大 %.3g・形 %s・型 %s' % (md, tuple(h.shape), h.dtype))
                mk = keep['masks']
                print('[参考] [%s] %s %s: 手回しの道の mask は %s・cache %s（判定に入れない）'
                      % (tn, k, label, '・'.join('%s=%s' % (t, 'None' if v is None else '明示 %s %s' % (v.dtype, tuple(v.shape)))
                                                  for t, v in sorted(mk.items())), '作る' if keep['use_cache'] else '作らない'), flush=True)
                if uc is False:
                    lo, z = readout(m, h[0, -1], c['set_ids'])
                    ref = o.logits[0, -1, c['set_ids']].float()
                    dz = float((z - ref).abs().max())
                    if tn == 'float32':
                        ck('[%s] %s: 読み取りの集合の出口の値（float32・softcap 後）が模型の出口の値と一致（書き手の許容 1e-4）' % (tn, k),
                           dz <= 1e-4, '差の絶対値の最大 %.3g' % dz)
                    else:
                        print('[参考] [%s] %s: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差の最大 %.3g（判定に入れない）'
                              % (tn, k, dz), flush=True)
                    # 歯: 正規化の後の値（hidden_states[-1]）を正規化の入力と取り違えると、模型の出口の値から離れる
                    with torch.no_grad():
                        o2 = m(input_ids=x, output_hidden_states=True, logits_to_keep=1)
                    hs = o2.hidden_states
                    _, zw = readout(m, hs[-1][0, -1], c['set_ids'])
                    dzw = float((zw - ref).abs().max())
                    ck('[%s] %s: 歯——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 10 倍を超える' % (tn, k),
                       dzw > 10 * max(dz, 1e-7), '取り違え %.3g・正しい %.3g' % (dzw, dz))
                    ck('[%s] %s: hidden_states は層の数＋1 で、[-1] は正規化の後（最終の正規化の入力と違う）' % (tn, k),
                       len(hs) == len(lm.layers) + 1 and not torch.equal(hs[-1], cap['x']))
                    ck('[%s] %s: 手回しの層 %d の出力（書き換えの前）が hidden_states[%d] と一致（ビット単位）' % (tn, k, L, L + 1),
                       torch.equal(keep['L_before'], hs[L + 1]))
                    # 歯: 1＋g・softcap の抜けは模型の出口の値から離れる
                    with torch.no_grad():
                        xf = h[0, -1].float()
                        xn1 = xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + float(lm.norm.eps)) * (1.0 + lm.norm.weight.float())
                        zr = top.lm_head.weight.index_select(0, torch.as_tensor(c['set_ids'])).float() @ xn1
                        z1 = cap_v * torch.tanh(zr / cap_v)
                        xn = xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + float(lm.norm.eps)) * lm.norm.weight.float()
                        zn = top.lm_head.weight.index_select(0, torch.as_tensor(c['set_ids'])).float() @ xn
                    d1 = float((z1 - ref).abs().max())
                    dn_ = float((zn - ref).abs().max())
                    ck('[%s] %s: 歯——1＋g で正規化した読み取りの差が、正しい読み取りの差の 10 倍を超える' % (tn, k),
                       d1 > 10 * max(dz, 1e-7), '1＋g %.3g・正しい %.3g' % (d1, dz))
                    print('[参考] [%s] %s: softcap を抜いた読み取りと模型の出口の値の差の最大 %.3g（正しい %.3g・判定に入れない）'
                          % (tn, k, dn_, dz), flush=True)
        # 二つの cache の形の手回しの道が同じ値か（この CPU で・参考）
        c = CI[probe[0]]
        hA = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=False)
        hB = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=None)
        print('[参考] [%s] use_cache=False と既定の手回しの道の最終の正規化の入力がビット単位で同じ: %s（判定に入れない）'
              % (tn, torch.equal(hA, hB)), flush=True)

    # (3) 主位置より前の位置は書き換えない・足した量は sign×coef×v
    AT_ = AT
    rn, _ = residual_norm(m32, tok, C, LG, L, AT=AT_)
    dirs, names = synthetic_dirs(C, d, SYN_NORM_FRAC * rn)
    print('[参考] 残差のノルム（層 %d の出力の主位置・八升目の平均・float32）%.4g → 合成の方向のノルム %.4g（× %s）'
          % (L, rn, SYN_NORM_FRAC * rn, SYN_NORM_FRAC), flush=True)
    for tn, m in models:
        for k, sign in (('N1|O-Ncold', -1), ('S1|Onull', +1)):
            c = CI[k]
            mp = c['mp']
            k0, k1 = {}, {}
            h0 = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, sign, mp, keep=k0)
            h1 = forward_rewrite(m, c['ids'], L, dirs['static'], TINY_COEF, sign, mp, keep=k1)
            ck('[%s] %s 符号 %+d: 層 %d より前の層の出力は無操作と同じ（ビット単位）' % (tn, k, sign, L),
               all(torch.equal(k0['outs'][i], k1['outs'][i]) for i in range(L)))
            ck('[%s] %s 符号 %+d: 層 %d の出力（書き換えの前）は無操作と同じ（ビット単位）' % (tn, k, sign, L),
               torch.equal(k0['L_before'], k1['L_before']))
            ck('[%s] %s 符号 %+d: 書き換えは主位置（%d）より前の位置を変えない（層 %d の出力・ビット単位）' % (tn, k, sign, mp, L),
               torch.equal(k1['L_after'][:, :mp], k1['L_before'][:, :mp]))
            ck('[%s] %s 符号 %+d: 主位置から列の最後まで（%d 位置）に同じ量を足した（ビット単位）' % (tn, k, sign, len(c['ids']) - mp),
               torch.equal(k1['L_after'][:, mp:], k1['L_before'][:, mp:] + k1['add']))
            want_add = int(sign) * float(TINY_COEF) * torch.as_tensor(np.asarray(dirs['static'], dtype=np.float32), dtype=k1['add'].dtype)
            ck('[%s] %s 符号 %+d: 足した量が「float32 を経て層の出力の型に直した v」× sign×coef（型 %s・ビット単位）'
               % (tn, k, sign, k1['add'].dtype), torch.equal(k1['add'], want_add))
            dv = (k1['L_after'][0, mp:].double() - k1['L_before'][0, mp:].double()).numpy()
            want = sign * TINY_COEF * dirs['static']
            cos = float(np.min(dv @ want / (np.linalg.norm(dv, axis=1) * np.linalg.norm(want))))
            rel = float(np.max(np.abs(np.linalg.norm(dv, axis=1) / np.linalg.norm(want) - 1.0)))
            ck('[%s] %s 符号 %+d: 層の出力の差の向きと大きさが sign×coef×v（型の丸めの内）' % (tn, k, sign),
               cos > 0.999 and rel < 0.02, '余弦の最小 %.6f・ノルムの相対の差の最大 %.3g' % (cos, rel))
            ck('[%s] %s 符号 %+d: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う' % (tn, k, sign),
               torch.equal(h1[:, :mp], h0[:, :mp]) and all(not torch.equal(h1[0, p], h0[0, p]) for p in range(mp, len(c['ids']))))
    n_same = sum(torch.equal(torch.as_tensor(np.asarray(v, dtype=np.float32), dtype=torch.bfloat16),
                             torch.as_tensor(v, dtype=torch.bfloat16)) for v in dirs.values())
    print('[参考] float32 を経た bf16 と float64 から直に直した bf16 が同じ合成の方向: %d/%d（判定に入れない）' % (n_same, len(dirs)), flush=True)

    # (4) 本の関数: 零のベクトルの効き目は零・形・二度同じ・外した升目・歯
    rows2 = dry_rows(C, LG)
    keep_cells = {ck_ for _, ck_, _ in rows2}
    pilot2 = {'decision': {'dropped': [k for k in LG['cells_main'] if k not in keep_cells]}}
    BC = _pub('bl3_core')
    want_rows, want_dbr = BC.recompute_set(C['main_rows'], [x[5:] for x in names['real']], C['nulls']['real']['swap_siblings'],
                                           len(names['iso']), pilot2['decision']['dropped'])
    for tn, m in models:
        zdirs = {k: np.zeros(d) for k in dirs}
        rz = recompute_rewrite(m, tok, C, LG, zdirs, names, pilot2, TINY_COEF)
        allz = all(v == 0.0 for r in rz.values() for v in r['effects'].values())
        ck('[%s] 零のベクトルの効き目が全て零（%d 行・効き目 %d 個・両方の符号）' % (tn, len(rz), sum(len(r['effects']) for r in rz.values())), allz)
        t0 = time.time()
        r1 = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
        dt = time.time() - t0
        r1b = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
        ck('[%s] 同じ呼び出しを二度走らせて同じ値（ビット単位）' % tn, r1 == r1b, '一度 %.1f 秒' % dt)
        shape_ok = (list(r1) == [nm for nm, _, _ in want_rows]
                    and all(list(r1[nm]['effects']) == ['%s|%+d' % (dn, s) for dn, s in want_dbr[nm]] for nm in r1)
                    and all(isinstance(r1[nm]['noop_lo'], float) for nm in r1))
        ck('[%s] 出力の形 {行の名: {noop_lo, effects: {方向の名|符号: 効き目}}}（行と方向の組は recompute_set のとおり・符号の書き方 %%+d）' % tn,
           shape_ok, '行 %s・効き目の数 %s・鍵の例 %s' % (list(r1), [len(r1[nm]['effects']) for nm in r1],
                                                    list(r1[list(r1)[0]]['effects'])[:2]))
        ck('[%s] 外した升目の行は計算しない（外していない升目の static の行だけ）' % tn,
           set(r1) == {nm for nm, ck_, _ in rows2})
        st = [r1[nm]['effects']['static|%+d' % s] for nm, _, s in rows2]
        ck('[%s] 歯——static の効き目は零でない' % tn, all(abs(v) > 0 for v in st), '・'.join('%.4g' % v for v in st))
        if tn == 'float32':
            ok, _ = stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, {'decision': {'dropped': ['S9|X']}}, TINY_COEF))
            ck('外した升目の鍵が台帳に無ければ止まる', ok)
            ok, _ = stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, {'decision': {}}, TINY_COEF))
            ck("pilot['decision']['dropped'] が無ければ止まる", ok)
            nm2 = copy.deepcopy(names)
            nm2['real'][0] = nm2['real'][0][len('real:'):]
            ck('names["real"] に real: で始まらない名があれば止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, nm2, pilot2, TINY_COEF))[0])
            d2 = dict(dirs)
            d2.pop('iso:3')
            ck('dirs に要る方向が無ければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, d2, names, pilot2, TINY_COEF))[0])
            d2 = dict(dirs)
            d2['static'] = dirs['static'].astype(np.float32)
            ck('方向が float64 でなければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, d2, names, pilot2, TINY_COEF))[0])
            d2 = dict(dirs)
            d2['static'] = dirs['static'][:-1].copy()
            ck('方向の形が次元と合わなければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, d2, names, pilot2, TINY_COEF))[0])
            ck('係数が正でなければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, 0.0))[0])
            _, _, lmx = parts(m)
            hd = lmx.layers[L].register_forward_hook(lambda mod, a, o: None)
            try:
                ok, _ = stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF))
            finally:
                hd.remove()
            ck('模型に forward の hook が掛かっていれば止まる（選んだ層に何もしない hook を掛けた写し）', ok)
            nc = capture_hook_count(m)
            r1c = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
            ck('transformers の記録用の hook（output_hidden_states の後に居残る %d 本）は数えず、値も変わらない（ビット単位）' % nc,
               nc > 0 and r1c == r1)
            import torch.nn as nn

            def _boom(*a, **k):
                raise RuntimeError('forward の hook を掛けようとした')
            saved = {nm_: nn.Module.__dict__[nm_] for nm_ in ('register_forward_hook', 'register_forward_pre_hook')}
            for nm_ in saved:
                setattr(nn.Module, nm_, _boom)
            try:
                r1d = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
                okh = r1d == r1
            except RuntimeError:
                okh = False
            finally:
                for nm_, fn_ in saved.items():
                    setattr(nn.Module, nm_, fn_)
            ck('呼び出しの間に forward の hook を掛けようとしない（nn.Module の register_forward_hook と register_forward_pre_hook を'
               '落ちる形に差し替えて走らせ、値も同じ）', okh)
            r_uc = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF, use_cache=None)
            dd = max_abs_diff(r1, r_uc)
            print('[参考] [%s] use_cache=None（DynamicCache を作る形）と既定の形の差の最大: 効き目 %.3g・無操作 %.3g（判定に入れない）'
                  % (tn, dd['effects'], dd['noop']), flush=True)

    # (5) 層ごとの入力と layer_scalar のある変種でも、手回しの道は模型の forward と一致（本の模型は layer_scalar を読み込む）
    vbase = tiny_model(C, variant='ple_scalar')
    for tn, m in (('float32', as_dtype(vbase, torch.float32)), ('bfloat16', vbase)):
        _, _, lm = parts(m)
        c = CI['S1|Onull']
        x = torch.tensor([c['ids']], dtype=torch.long)
        cap = {}
        hd = lm.norm.register_forward_pre_hook(lambda mod, a: cap.__setitem__('x', a[0].detach().clone()))
        try:
            with torch.no_grad():
                m(input_ids=x, use_cache=False, logits_to_keep=1)
        finally:
            hd.remove()
        h = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=False)
        ck('[%s] 層ごとの入力（%d）と layer_scalar（%s…）のある変種でも、手回しの道の最終の正規化の入力が模型の forward と一致（ビット単位）'
           % (tn, lm.config.hidden_size_per_layer_input, '・'.join('%.3f' % float(ly.layer_scalar) for ly in lm.layers[:2])),
           torch.equal(h, cap['x']))
    n_ok = sum(res)
    print('selftest: %d/%d ok' % (n_ok, len(res)), flush=True)
    print('柵: ' + FENCE, flush=True)
    return n_ok == len(res)


# ---------------------------------------------------------------- 突き合わせ（--dry）

def _hook_path(model, tok, C, LG, dirs, rows, dbr, L, coef):
    """コーディネータのフックの道（公開の関数を中を見ずに呼ぶ）。"""
    sys.path.insert(0, os.path.join(BPRIME, 'tools'))
    import bprime_run as BR
    R = BR.Runner(model, C, L, coef, dirs)
    cells = BR.build_cells(tok, C, LG, sorted({ck_ for _, ck_, _ in rows}))
    return BR.recompute_hook_path(R, [(nm, cells[ck_], s) for nm, ck_, s in rows], {nm: list(dbr[nm]) for nm, _, _ in rows})


def _dry(teeth=True):
    import torch
    import transformers
    from transformers import AutoTokenizer
    C, LG = load_canon(), load_ledger()
    tol = float(C['independent_recompute']['tol_stage1'])
    RB = _pub('run_stageB_local')
    BC = _pub('bl3_core')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    base = tiny_model(C)
    m32 = as_dtype(base, torch.float32)
    for m in (m32, base):
        assert_tiny(m)
    L = layer_index_for(m32, C)
    _, _, lm32 = parts(m32)
    d = int(lm32.config.hidden_size)
    rn, _ = residual_norm(m32, tok, C, LG, L, AT=AT)
    dirs, names = synthetic_dirs(C, d, SYN_NORM_FRAC * rn)
    rows = dry_rows(C, LG)
    keep_cells = {ck_ for _, ck_, _ in rows}
    pilot = {'decision': {'dropped': [k for k in LG['cells_main'] if k not in keep_cells]}}
    want_rows, dbr = BC.recompute_set(C['main_rows'], [x[5:] for x in names['real']], C['nulls']['real']['swap_siblings'],
                                      len(names['iso']), pilot['decision']['dropped'])
    print('bprime_recompute_rewrite %s --dry  torch %s・transformers %s・numpy %s・注意の実装 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, lm32.config._attn_implementation), flush=True)
    print('乱数の小さな模型: 次元 %d・層 %d・選んだ層の添字 %d・窓 %d・係数 %s・合成の方向のノルム %.4g（残差のノルム %.4g × %s）・'
          '一段目の許容 independent_recompute.tol_stage1 = %s'
          % (d, len(lm32.layers), L, lm32.config.sliding_window, TINY_COEF, SYN_NORM_FRAC * rn, rn, SYN_NORM_FRAC, tol), flush=True)
    for nm, ck_, s in rows:
        kinds = {'static': 0, 'iso': 0, 'real': 0}
        for dn, _ in dbr[nm]:
            kinds['static' if dn == 'static' else dn.split(':')[0]] += 1
        print('行 %s・升目 %s（%s）・符号 %+d・方向と符号 %d 組（static %d・等方 %d・比べる相手の実在の差 %d＝%d 対 × 両方の向き）＋無操作'
              % (nm, ck_, LG['cells_main'][ck_]['family'], s, len(dbr[nm]), kinds['static'], kinds['iso'], kinds['real'],
                 kinds['real'] // 2), flush=True)
    verdicts = []
    for tn, m in (('float32', m32), ('bfloat16', base)):
        t0 = time.time()
        mine = recompute_rewrite(m, tok, C, LG, dirs, names, pilot, TINY_COEF)
        t1 = time.time()
        if list(mine) != [nm for nm, _, _ in want_rows]:
            print('[%s] 残差の書き換えの道の行が選んだ二行と違う: %s' % (tn, list(mine)), flush=True)
            verdicts.append(False)
            continue
        try:
            hook = _hook_path(m, tok, C, LG, dirs, rows, dbr, L, TINY_COEF)
        except BaseException as e:                                    # 中の行を出さない（中を見ない）
            print('[%s] フックの道が落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
            verdicts.append(False)
            continue
        t2 = time.time()
        dd = max_abs_diff(mine, hook)
        n_eff = sum(len(r['effects']) for r in mine.values())
        amax = max(abs(v) for r in mine.values() for v in r['effects'].values())
        print('[%s] 残差の書き換えの道 %.1f 秒（順伝播 %d 回）・フックの道 %.1f 秒' % (tn, t1 - t0, n_eff + len(mine), t2 - t1), flush=True)
        if dd is None:
            print('[%s] 二つの道の行か鍵の集合が違う（残差の書き換えの道 %s 行・フックの道 %s 行）' % (tn, len(mine), len(hook) if hasattr(hook, '__len__') else '?'), flush=True)
            verdicts.append(False)
            continue
        print('[%s] 効き目の数 %d・効き目の絶対値の最大（残差の書き換えの道）%.4g' % (tn, n_eff, amax), flush=True)
        print('[%s] 差の絶対値の最大: 効き目 %.3g・無操作の量 %.3g' % (tn, dd['effects'], dd['noop']), flush=True)
        ok = dd['effects'] <= tol and dd['noop'] <= tol
        verdicts.append(ok)
        print('[%s] dry: 一段目の許容（%s）の%s（差の最大 %.3g）' % (tn, tol, '内' if ok else '外', max(dd['effects'], dd['noop'])), flush=True)
        try:                                                           # 参考の行（止まっても判定は変えず、文言を印字して続ける）
            again = recompute_rewrite(m, tok, C, LG, dirs, names, pilot, TINY_COEF)
            print('[参考] [%s] フックの道の後に走らせ直した残差の書き換えの道が一度目と同じ（ビット単位）: %s・居残る hook（記録用を除く）%d 本'
                  % (tn, again == mine, len(foreign_hooks(m))), flush=True)
        except SystemExit as e:
            print('[参考] [%s] フックの道の後の走らせ直しが止まった: %s' % (tn, str(e)[:300]), flush=True)
        try:
            uc = recompute_rewrite(m, tok, C, LG, dirs, names, pilot, TINY_COEF, use_cache=None)
            d2 = max_abs_diff(uc, hook)
            d3 = max_abs_diff(uc, mine)
            print('[参考] [%s] use_cache=None（DynamicCache を作る形）の残差の書き換えの道——既定の形との差の最大 効き目 %.3g・無操作 %.3g／'
                  'フックの道との差の最大 効き目 %.3g・無操作 %.3g' % (tn, d3['effects'], d3['noop'], d2['effects'], d2['noop']), flush=True)
        except SystemExit as e:
            print('[参考] [%s] use_cache=None の走りが止まった: %s' % (tn, str(e)[:300]), flush=True)
        if teeth:
            _teeth(m, tn, tok, C, LG, dirs, rows, dbr, L, hook, tol, AT)
    print('（正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない）', flush=True)
    print('dry: %s' % ('二つの型とも一段目の許容の内' if verdicts and all(verdicts) else '許容の外か比べられなかった型がある'), flush=True)
    print('柵: ' + FENCE, flush=True)
    return bool(verdicts) and all(verdicts)


def _teeth(model, tn, tok, C, LG, dirs, rows, dbr, L, hook, tol, AT):
    """歯の変種（参考・判定に入れない・事前登録 dry-preregistration-Bprime.txt）: この道をわざと誤らせ、フックの道との差で捕まるかを見る。
    比べる鍵: 行ごとに無操作と、static・iso:0（行の符号）と、その行の最初の比べる相手の実在の差（両方の向き）。"""
    import torch
    _, _, lm = parts(model)
    cap = softcap_value(model)
    d = int(lm.config.hidden_size)
    zero = np.zeros(d)

    def fwd(ids, vec, sign, mp, kind):
        Lx = L + 1 if kind == 'M2' else L
        start = mp + 1 if kind == 'M1' else mp
        coef = TINY_COEF * TINY_COEF if kind == 'M4' else TINY_COEF
        sgn = -sign if kind == 'M3' else sign

        def on_layer_out(i, h):
            if i == Lx:
                if kind == 'M7':
                    add = int(sgn) * float(coef) * torch.as_tensor(np.asarray(vec, dtype=np.float32), device=h.device)
                else:
                    add = cast_add(vec, coef, sgn, h)
                h[0, start:, :] = h[0, start:, :] + add
            return h
        return _forward_impl(model, ids, on_layer_out, use_cache=False)

    def rd(h_last, set_ids, kind):
        if kind not in ('M5', 'M6', 'M8'):
            return readout(model, h_last, set_ids, cap)[0]
        with torch.no_grad():
            g = lm.norm.weight.to(torch.float32)
            eps = float(lm.norm.eps)
            x = h_last.to(torch.float32)
            gg = (1.0 + g) if kind == 'M8' else g
            xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * gg
            if kind == 'M5':
                xn = xn * torch.rsqrt(xn.pow(2).mean(-1, keepdim=True) + eps) * g
            z = lm.embed_tokens.weight.index_select(0, torch.as_tensor(list(set_ids))).to(torch.float32) @ xn
            if kind != 'M6':
                z = cap * torch.tanh(z / cap)
            return float(z[0] - torch.logsumexp(z[1:], dim=0))

    labels = {'M0': '誤らせない（対照）', 'M1': '帯の起点を主位置の一つ後にする', 'M2': '書き換える層を一つ後にする',
              'M3': '符号を反転する', 'M4': '係数を二度掛ける（sign×coef×coef×v）', 'M5': '読み取りで正規化を二度当てる',
              'M6': '読み取りで softcap を抜く', 'M7': '加減を層の出力の型に直さず float32 のまま足す', 'M8': '最終の正規化の重みを 1＋g にする'}
    t0 = time.time()
    cells = {ck_: cell_input(tok, C, LG, ck_, AT=AT) for _, ck_, _ in rows}
    for kind in ('M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'):
        worst, n = 0.0, 0
        for nm, ck_, sign in rows:
            c = cells[ck_]
            first_real = next(dn for dn, _ in dbr[nm] if dn.startswith('real:'))
            probe = [('static', sign), ('iso:0', sign), (first_real, sign), (first_real, -sign)]
            lo0 = rd(fwd(c['ids'], zero, sign, c['mp'], kind)[0, -1], c['set_ids'], kind)
            worst = max(worst, abs(lo0 - float(hook[nm]['noop_lo'])))
            for dn, s in probe:
                lo = rd(fwd(c['ids'], dirs[dn], s, c['mp'], kind)[0, -1], c['set_ids'], kind)
                worst = max(worst, abs((lo - lo0) - float(hook[nm]['effects']['%s|%+d' % (dn, s)])))
                n += 1
        caught = worst > tol
        print('[歯] [%s] %s %s: フックの道との差の最大 %.3g（無操作 %d 個・効き目 %d 個）→ %s（許容 %s）'
              % (tn, kind, labels[kind], worst, len(rows), n,
                 ('許容の内（対照として期待どおり）' if not caught else '許容の外（対照が外れた）') if kind == 'M0'
                 else ('許容の外＝捕まえた' if caught else '許容の内＝捕まえなかった（この模型での盲点）'), tol), flush=True)
    print('[歯] [%s] 変種の計算 %.1f 秒（参考・判定に入れない）' % (tn, time.time() - t0), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--no-teeth', action='store_true')
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.dry:
        sys.exit(0 if _dry(teeth=not a.no_teeth) else 1)
    ap.print_help()


if __name__ == '__main__':
    main()
