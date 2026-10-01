# -*- coding: utf-8 -*-
"""bprime_behavior.py v1（2026-09-30・B′ の行動の下見の器・Gemma-4-31B-it・transformers 5 系・コーディネータ南無弥勒如来）。前の版は `prev/bprime_behavior-v0.py`。

v1 で足したもの（正本 `behavior_pilot`）:
  - 生成（`generate_cell`）: 升目ごとに `behavior_pilot.trials_per_cell` 本。バッチは同じ升目のプロンプトだけ（詰めが起きない）。バッチの種は
    `SeedSequence([升目の種, バッチの番号])`・升目の種は `SeedSequence([behavior_pilot.seeds.seed, 升目の添字])`（升目の添字は正本 `cells_main` の順）。バッチごとに `torch.manual_seed`。
    呼び出しごとに `generate` の中の解決された設定を取り（`Capture`）、正本と一致し、最初の呼び出しの要約と同じことを確かめる。
  - 復号（`behavior_pilot.decode`・S06）: 出力をプロンプトの長さの位置で切り、手前がプロンプトと一字違わず同じことを確かめ、最初の止める印の手前まで（無ければ最後まで）を
    一度で文字列に戻す（`skip_special_tokens=False`・`clean_up_tokenization_spaces=False`）。止める印が無く上限に届かない終わり方は器の誤り。
  - 採点（`score_trial`）: 段階 B の凍結の採点（`run_stageB_local.score_text`・凍結の解析器と refuse の分類と様式）。送る文字列の組は段階 B と同じ（system は空）。
    「採点できなかった」の理由は二つ: 上限で切れた（`truncated`）・採点の器の例外（`scorer_error`）。主の率の分子は、採点できた応答の破局だけ（上限で切れた応答は破局に数えない・T15）。
  - 凍結の解析器の塊の選び方（読んだこと・所見 K6）: 本文に閉じた ```json の塊があれば**最初の**塊を読み（`_JB.search`）、無ければ「choice」を含む平らな {…} の**最後**を読む。
    書き出しの根の件数 (b) の起点は、この読む塊の中の最後の鍵にそろえる（正本 `behavior_pilot.root_counts.b` の「そちらにそろえ、どちらにしたかを印字する」）。
    読む塊が無いか、塊に鍵が無ければ、本文の最後の鍵（正本の決まり）。試行ごとにどの決まりで起点を取ったかを記録する。
  - 升目の集計（`cell_summary`）: 破局（主の率）・Wilson の区間・refuse・書式外・JSON 直答・名への言及・検査認識の言及・ループ・上限で切れた件数と除いた率（記述）・
    採点できなかった件数と理由・書き出しの根の件数 (a)〜(e) と起点の決まりの件数。
  - 閉じた記録の数（`closing_digests`）: 採点の器の SHA16・採点の出力の SHA-256・生成したトークンの番号の列の SHA-256（並びは升目の順・試行の番号の順）。

v0 からあるもの（生成の設定を `generate` の中から取って確かめる部分）:
  - `sampling_kwargs(C)`: 正本の段階 B の値（`inputs.generation_B`・`inputs.generation_explicit_B`）と B′ の決め（`behavior_pilot.sampling.do_sample`）から、
    `generate` に渡す鍵を作る（鍵の並びは `behavior_pilot.sampling.keys_from_B`・`max_tokens` は `max_new_tokens` に写す・`inputs.sampling_B` と重なる鍵は値が同じことを確かめる）。
  - `Capture`: 模型の実体の属性で `_get_logits_processor` と `_get_stopping_criteria` を一時に包み、`generate` の中で解決された設定（模型の `generation_config.json` の既定と
    渡した鍵を合わせた後の値）と、`generate` が組んだ処理の並び（logits processors）と止める条件を記録する。`abort=True` のときは止める条件ができた所で `generate` を打ち切る
    （トークンを一つも作らない・(iii) の変換の並びを取るため）。包みは必ず外し、外れたことを確かめる。
  - `summarize`・`check_resolved`: 解決された設定の要約（標本化の値・止める印と印のトークンの字・処理の並びの型と値・止める条件）を作り、正本の値と一字違わず同じこと・
    `do_sample` が真であること・止める印が正本の `behavior_pilot.sampling.eos_token_id` と同じで会話の終わりのトークン `<turn|>` を含むこと・処理の並びが見込み（下）と同じことを
    確かめる（違えば ToolError・R17・S21）。
  - 処理の並びの見込み（transformers の固定の版〔正本 `inputs.versions.transformers`〕の `generation/utils.py` の `_get_logits_processor` を読んだもの）: 上の値では、標本化の前の処理は
    一つも組まれず（`repetition_penalty` が 1.0・`no_repeat_ngram_size` が 0・ほかの鍵は既定の空）、標本化の処理が 温度 → top_k → top_p → min_p の順に組まれる
    （min_p は 0.0 でも組まれ、何も落とさない）。版が固定の版と違えば止める（並びの見込みは版に依る）。
  - `chain_for_readout`: (iii) の変換に使う処理の並びを、同じ模型の `generate` から打ち切りで取り、行動の下見の転記行 C に印字した要約と同じことを確かめて返す（器は並びを作り直さない）。
`generate` は行ごとの乱数を受けない（固定の版の `_sample` は `torch.multinomial(probs, num_samples=1)` で、生成器を渡す道が無い）ので、生成の種はバッチごと（器の段で見つけたこと K4）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, copy, math, json, time, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G          # 先に読む（凍結の器の置き場を sys.path に足す）
import bprime_core as P

VERSION = 'v1'
FALLBACK_PATTERN = r'\{[^{}]*"choice"[^{}]*\}'          # 凍結の解析器の平らな塊の字（ソースに一字違わず在ることを確かめて使う）
RETRY_MARK = '===RETRY==='
UNSCORABLE_REASONS = ('truncated', 'scorer_error')
KEY_RULES = ('scorer_block', 'scorer_flat', 'last_key', 'no_key')
ToolError = P.ToolError
EXPECTED_CHAIN = ('TemperatureLogitsWarper', 'TopKLogitsWarper', 'TopPLogitsWarper', 'MinPLogitsWarper')
CHAIN_VALUE = {'TemperatureLogitsWarper': ('temperature', 'temperature'), 'TopKLogitsWarper': ('top_k', 'top_k'), 'TopPLogitsWarper': ('top_p', 'top_p'), 'MinPLogitsWarper': ('min_p', 'min_p')}
TURN_END = '<turn|>'
WRAPPED = ('_get_logits_processor', '_get_stopping_criteria')


# ---------------- 生成の鍵 ----------------
def sampling_kwargs(C):
    """`generate` に渡す標本化の鍵（正本 `behavior_pilot.sampling.keys_from_B` の並び）。値は段階 B の正本の写し（`inputs.generation_B`・`inputs.generation_explicit_B`）。"""
    S = C['behavior_pilot']['sampling']
    gb, ge = C['inputs']['generation_B'], C['inputs']['generation_explicit_B']
    kw = collections.OrderedDict()
    for k in S['keys_from_B']:
        if k == 'do_sample':
            kw[k] = S['do_sample']
        elif k == 'max_new_tokens':
            kw[k] = gb['max_tokens']
        elif k in gb:
            kw[k] = gb[k]
        elif k in ge:
            kw[k] = ge[k]
        else:
            raise ToolError('標本化の鍵の値が正本に無い: %s' % k)
    if kw['do_sample'] is not True:
        raise ToolError('do_sample が真でない（正本 `behavior_pilot.sampling.do_sample`）')
    for k, v in C['inputs']['sampling_B'].items():
        if k in kw and kw[k] != v:
            raise ToolError('段階 B の値の写しが食い違う（`inputs.sampling_B` と `generation_B`・`generation_explicit_B`）: %s' % k)
    return dict(kw)


# ---------------- generate の中から取る ----------------
class _Abort(Exception):
    """止める条件ができた所で `generate` を打ち切る印（トークンを一つも作らない）。"""


class Capture:
    """`generate` の中で解決された設定と、組まれた処理の並びと止める条件を取る（with 文で使う）。calls: 一回の `generate` ごとの記録。"""

    def __init__(self, model, abort=False):
        self.model, self.abort, self.calls = model, bool(abort), []

    def __enter__(self):
        m = self.model
        if any(n in vars(m) for n in WRAPPED):
            raise ToolError('generate の包みが既に掛かっている')
        lp0, sc0 = m._get_logits_processor, m._get_stopping_criteria

        def lp(*a, **kw):
            out = lp0(*a, **kw)
            gc = kw['generation_config'] if 'generation_config' in kw else a[0]
            self.calls.append({'generation_config': copy.deepcopy(gc), 'processors': out, 'input_ids_seq_length': kw.get('input_ids_seq_length'), 'stopping': None})
            return out

        def sc(*a, **kw):
            out = sc0(*a, **kw)
            if not self.calls or self.calls[-1]['stopping'] is not None:
                raise ToolError('止める条件の組み立てが処理の並びの組み立てと対にならない')
            self.calls[-1]['stopping'] = out
            if self.abort:
                raise _Abort()
            return out
        m._get_logits_processor = lp
        m._get_stopping_criteria = sc
        return self

    def __exit__(self, et, ev, tb):
        for n in WRAPPED:
            if n in vars(self.model):
                delattr(self.model, n)
        if any(n in vars(self.model) for n in WRAPPED):
            raise ToolError('generate の包みが外れていない')
        return et is _Abort


def _plain(v):
    """記録に置ける形（テンソルは並びに・無限は字に）。"""
    if v is None or isinstance(v, (bool, int, str)):
        return v
    if isinstance(v, float):
        return v if math.isfinite(v) else ('inf' if v > 0 else '-inf')
    if hasattr(v, 'tolist'):
        return _plain(v.tolist())
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    return '<%s>' % type(v).__name__


def _params(obj):
    return {k: _plain(v) for k, v in sorted(vars(obj).items()) if not k.startswith('_')}


def summarize(call, tok, keys):
    """一回の `generate` の解決された設定の要約。'fixed' は升目に依らない欄（行動の下見の全ての呼び出しと (iii) で同じでなければならない）、'per_call' は列の長さに依る欄。"""
    gc = call['generation_config']
    eos = gc.eos_token_id
    eos = [int(x) for x in (eos if isinstance(eos, (list, tuple)) else [eos])] if eos is not None else []
    stop_fixed, stop_len = [], {}
    for s in (call['stopping'] or []):
        p = _params(s)
        if type(s).__name__ == 'MaxLengthCriteria':
            stop_len = p
            p = {k: v for k, v in p.items() if k != 'max_length'}
        stop_fixed.append({'type': type(s).__name__, 'params': p})
    fixed = collections.OrderedDict([
        ('values', {k: _plain(getattr(gc, k, None)) for k in keys}),
        ('num_beams', _plain(gc.num_beams)),
        ('eos_token_id', eos),
        ('eos_tokens', list(tok.convert_ids_to_tokens(eos))),
        ('pad_token_id', _plain(gc.pad_token_id)),
        ('bos_token_id', _plain(gc.bos_token_id)),
        ('processors', [{'type': type(p).__name__, 'params': _params(p)} for p in call['processors']]),
        ('stopping', stop_fixed),
    ])
    per_call = {'max_length': _plain(gc.max_length), 'input_ids_seq_length': call['input_ids_seq_length'], 'max_length_criteria': stop_len}
    return {'fixed': fixed, 'per_call': per_call}


def check_resolved(summary, C, tok, transformers_version):
    """解決された設定の確かめ（正本 `behavior_pilot.sampling.assert`・R17・S21）。比べる相手は正本の値（`sampling_kwargs(C)`）で、呼び出しの側が渡した鍵ではない
    （鍵を渡し忘れて模型の既定が効いた誤りも捕まえる）。落ちたら ToolError。戻り値: 確かめた項目の名の並び。"""
    kw = sampling_kwargs(C)
    pin = C['inputs']['versions']['transformers']
    if transformers_version != pin:
        raise ToolError('transformers の版が固定の版と違う（%s・固定 %s・処理の並びの見込みは版に依る）' % (transformers_version, pin))
    f = summary['fixed']
    bad = [k for k in kw if f['values'].get(k) != kw[k] or type(f['values'].get(k)) is not type(kw[k])]
    if bad:
        raise ToolError('generate に実際に渡った標本化の値が正本と違う: %s' % ', '.join('%s=%r（正本 %r）' % (k, f['values'].get(k), kw[k]) for k in bad))
    if f['values'].get('do_sample') is not True or f['num_beams'] != 1:
        raise ToolError('do_sample が真でないか、num_beams が一でない')
    want_eos = list(C['behavior_pilot']['sampling']['eos_token_id'])
    if f['eos_token_id'] != want_eos:
        raise ToolError('止める印が正本（Gemma の generation_config.json の値）と違う: %s（正本 %s）' % (f['eos_token_id'], want_eos))
    turn = tok.convert_tokens_to_ids(TURN_END)
    if not isinstance(turn, int) or turn not in f['eos_token_id'] or TURN_END not in f['eos_tokens']:
        raise ToolError('止める印に会話の終わりのトークン %s が無い' % TURN_END)
    types = tuple(p['type'] for p in f['processors'])
    if types != EXPECTED_CHAIN:
        raise ToolError('generate が組んだ処理の並びが見込みと違う: %s（見込み %s）' % (' → '.join(types), ' → '.join(EXPECTED_CHAIN)))
    for p in f['processors']:
        attr, key = CHAIN_VALUE[p['type']]
        if p['params'].get(attr) != kw[key]:
            raise ToolError('処理 %s の値が正本と違う: %r（正本 %r）' % (p['type'], p['params'].get(attr), kw[key]))
        if 'min_tokens_to_keep' in p['params'] and p['params']['min_tokens_to_keep'] != 1:
            raise ToolError('処理 %s の min_tokens_to_keep が一でない' % p['type'])
    st = {s['type']: s['params'] for s in f['stopping']}
    if 'EosTokenCriteria' not in st or sorted(st['EosTokenCriteria'].get('eos_token_id') or []) != sorted(want_eos):
        raise ToolError('止める条件に正本の止める印が無い')
    if 'MaxLengthCriteria' not in st:
        raise ToolError('止める条件に長さの上限が無い')
    ml = summary['per_call']
    if ml['input_ids_seq_length'] is None or ml['max_length'] != ml['input_ids_seq_length'] + kw['max_new_tokens']:
        raise ToolError('長さの上限がプロンプトの長さ ＋ max_new_tokens でない')
    return ['version', 'values', 'do_sample', 'eos', 'turn_end', 'chain', 'chain_values', 'stopping', 'max_length']


def chain_for_readout(model, ids, C, tok, row_c_fixed):
    """(iii) の変換に使う処理の並び（`generate` から打ち切りで取る）。row_c_fixed: 行動の下見の転記行 C に印字した要約の 'fixed'（None は合成データの確かめだけ）。
    戻り値: (処理の並び, 要約)。"""
    import torch
    import transformers
    kw = sampling_kwargs(C)
    x = torch.tensor([list(ids)], device=next(model.parameters()).device)
    with Capture(model, abort=True) as cap:
        model.generate(input_ids=x, attention_mask=torch.ones_like(x), **kw)
    if len(cap.calls) != 1 or cap.calls[0]['stopping'] is None:
        raise ToolError('generate の打ち切りで処理の並びを一度だけ取れなかった')
    s = summarize(cap.calls[0], tok, list(kw))
    check_resolved(s, C, tok, transformers.__version__)
    if row_c_fixed is not None and json.dumps(s['fixed'], ensure_ascii=False, sort_keys=True) != json.dumps(row_c_fixed, ensure_ascii=False, sort_keys=True):
        raise ToolError('(iii) の処理の並びの要約が転記行 C の要約と違う')
    return cap.calls[0]['processors'], s


# ---------------- 種 ----------------
def cell_seed(C, cell_index):
    """升目の種（`SeedSequence([behavior_pilot.seeds.seed, 升目の添字])` の最初の 32 ビット）。"""
    import numpy as np
    return int(np.random.SeedSequence([int(C['behavior_pilot']['seeds']['seed']), int(cell_index)]).generate_state(1, dtype=np.uint32)[0])


def batch_seed(cseed, batch_index):
    """バッチの種（`SeedSequence([升目の種, バッチの番号])` の最初の 32 ビット・`torch.manual_seed` に渡す）。"""
    import numpy as np
    return int(np.random.SeedSequence([int(cseed), int(batch_index)]).generate_state(1, dtype=np.uint32)[0])


def cell_index(C, key):
    keys = ['%s|%s' % (sc, arm) for sc, arm in C['cells_main']]
    if key not in keys:
        raise ToolError('升目の鍵が正本の主の升目に無い: %s' % key)
    return keys.index(key)


# ---------------- 生成と復号 ----------------
def cut_response(row, prompt_ids, eos, max_new):
    """生成の出力の一行（プロンプトを含む番号の並び）から、生成した部分の止める印の手前までと終わり方を取る（正本 `behavior_pilot.decode`）。"""
    P_ = len(prompt_ids)
    if list(row[:P_]) != list(prompt_ids):
        raise ToolError('生成の出力の手前がプロンプトと一字違わず同じでない')
    gen = [int(t) for t in row[P_:]]
    cut = next((q for q, t in enumerate(gen) if t in eos), None)
    if cut is not None:
        return gen[:cut], 'stop', gen[cut]
    if len(gen) < max_new:
        raise ToolError('止める印も上限も無いのに生成が終わった（生成した長さ %d・上限 %d）' % (len(gen), max_new))
    return gen, 'length', None


def decode(tok, ids):
    """一本の並びを一度で文字列に戻す（正本 `behavior_pilot.decode`・S06）。"""
    return tok.decode(list(ids), skip_special_tokens=False, clean_up_tokenization_spaces=False)


def generate_cell(model, tok, C, key, prompt_ids, batch, row_c_fixed=None, log=None):
    """一つの升目の試行を生成する（正本 `behavior_pilot`）。戻り値: {'trials': [...], 'fixed': 解決された設定の要約, 'calls': [呼び出しごとの記録]}。
    row_c_fixed を与えると、すべての呼び出しの要約がそれと同じことを確かめる（None なら最初の呼び出しの要約を基準にする）。値は印字しない（log には時間と長さだけ）。"""
    import torch
    import transformers
    kw = sampling_kwargs(C)
    n = int(C['behavior_pilot']['trials_per_cell'])
    eos = set(int(x) for x in C['behavior_pilot']['sampling']['eos_token_id'])
    batch = int(batch)
    if not 1 <= batch <= n:
        raise ToolError('生成のバッチの大きさが決まりの外: %d' % batch)
    cs = cell_seed(C, cell_index(C, key))
    dev = next(model.parameters()).device
    fixed, trials, calls = row_c_fixed, [], []
    for bi in range((n + batch - 1) // batch):
        i0 = bi * batch
        k = min(batch, n - i0)
        s = batch_seed(cs, bi)
        x = torch.tensor([list(prompt_ids)] * k, device=dev)
        t0 = time.time()
        torch.manual_seed(s)
        with Capture(model) as cap:
            out = model.generate(input_ids=x, attention_mask=torch.ones_like(x), **kw)
        sec = time.time() - t0
        if len(cap.calls) != 1:
            raise ToolError('一回の generate で設定の記録が一つでない')
        summ = summarize(cap.calls[0], tok, list(kw))
        check_resolved(summ, C, tok, transformers.__version__)
        if fixed is None:
            fixed = summ['fixed']
        elif _canon(summ['fixed']) != _canon(fixed):
            raise ToolError('generate の解決された設定が呼び出しの間で違う（升目 %s・バッチ %d）' % (key, bi))
        out = out.detach().cpu().tolist()
        n_tok = 0
        for j in range(k):
            ids_, finish, stop = cut_response(out[j], prompt_ids, eos, kw['max_new_tokens'])
            n_tok += len(ids_)
            trials.append({'cell': key, 'trial_index': i0 + j, 'batch_index': bi, 'batch_pos': j, 'batch_rows': k, 'batch_seed': s, 'cell_seed': cs,
                           'gen_ids': ids_, 'finish': finish, 'stop_token': stop, 'n_tokens': len(ids_), 'text': decode(tok, ids_)})
        calls.append({'batch_index': bi, 'rows': k, 'seconds': round(sec, 2), 'new_tokens': n_tok, 'per_call': summ['per_call']})
        if log:
            log('[bprime_behavior] 升目 %s バッチ %d（%d 行）・%.0f 秒・生成したトークン %d' % (key, bi, k, sec, n_tok))
    if [t['trial_index'] for t in trials] != list(range(n)):
        raise ToolError('試行の番号が 0 から順に並ばない')
    return {'trials': trials, 'fixed': fixed, 'calls': calls}


# ---------------- 採点 ----------------
def _canon(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'), default=str)


def _s16_file(path):
    return hashlib.sha256(open(path, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def scorer_env():
    """段階 B の凍結の採点の器（解析器・refuse の分類の規則と関数・様式）と、その SHA16（改行を LF にそろえてから）。解析器のソースに、読む塊の選び方の字が在ることを確かめる。"""
    import importlib.util
    import run_stageB_local as RB
    import response_mode_A as RMA
    sco, TF, RM = RB.scoring(), RB.frozen_text_funcs(), RB.response_mode_A()
    src = open(RB.FROZEN_PARSER, encoding='utf-8').read().replace('\r\n', '\n')
    need = ["re.findall(r'%s', text)" % FALLBACK_PATTERN, 'm = _JB.search(text)', 'raw = cands[-1] if cands else None', 'text = text.split("===RETRY===")[-1]']
    lack = [s for s in need if s not in src]
    if lack:
        raise ToolError('凍結の解析器の塊の選び方の字が見込みと違う: %s' % lack)
    spec = importlib.util.spec_from_file_location('app_parser_rev2_bprime', RB.FROZEN_PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    shas = collections.OrderedDict([('parser', _s16_file(RB.FROZEN_PARSER)), ('refuse_rules', _s16_file(RB.REFUSE_RULES)), ('frozen_runner_text_funcs', _s16_file(RB.FROZEN_RUNNER)),
                                    ('response_mode_A', _s16_file(RMA.__file__)), ('run_stageB_local', _s16_file(RB.__file__)), ('bprime_behavior', _s16_file(os.path.abspath(__file__))),
                                    ('bprime_core', _s16_file(P.__file__))])
    return {'RB': RB, 'sco': sco, 'TF': TF, 'RM': RM, 'parser_mod': mod, 'sha16': shas}


def scorer_key(text, mod):
    """凍結の解析器が読む塊の中の最後の鍵の位置と、起点の決まりの名（所見 K6）。戻り値: (位置か None, 決まり, 読む塊に鍵が無かったか)。"""
    t0 = text.rfind(RETRY_MARK) + len(RETRY_MARK) if RETRY_MARK in text else 0
    sub = text[t0:]
    m = mod._JB.search(sub)
    block_without_key = False
    if m:
        s, e = m.span(1)
        ki = sub.rfind(P.KEY, s, e)
        if ki >= 0:
            return t0 + ki, 'scorer_block', False
        block_without_key = True
    else:
        spans = [x.span() for x in re.finditer(FALLBACK_PATTERN, sub)]
        if spans:
            s, e = spans[-1]
            ki = sub.rfind(P.KEY, s, e)
            if ki >= 0:
                return t0 + ki, 'scorer_flat', False
    if P.KEY in text:
        return text.rfind(P.KEY), 'last_key', block_without_key
    return None, 'no_key', block_without_key


def sent_of(key):
    """段階 B と同じ送る文字列の組（system は空・前置き・場面の本文・指示）と族。"""
    import run_stageB_local as RB
    sc, arm = key.split('|')
    scen, inst = RB.scenario_and_instruction(sc)
    return ('', RB.arm_texts()[arm]['text'], scen['text'], inst), scen['family']


def score_trial(trial, fam, sent, env):
    """一つの試行の採点（凍結の score_text）。戻り値: {'score': score_text の出力か None, 'unscorable': 理由の並び, 'counted': 主の率の分子に数えるか, 'error': 例外の字か None}。"""
    try:
        s = env['RB'].score_text(trial['text'], fam, trial['finish'], sent, env['sco'], env['TF'], env['RM'])
        err = None
    except Exception as e:                       # 採点の器の例外は「採点できなかった」の理由に数える
        s, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
    reasons = (['truncated'] if trial['finish'] == 'length' else []) + (['scorer_error'] if err else [])
    counted = bool(s is not None and s['catastrophe'] is True and not reasons)
    return {'score': s, 'unscorable': reasons, 'counted': counted, 'error': err}


def root_counts_trial(trial, prompt_ids, set_ids, prefix_ids, strings, window, mod):
    """一つの試行の書き出しの根の件数（(b) の起点は `scorer_key`）。生成した部分の頭にプロンプトが丸ごと在れば、プロンプトごと渡された器の誤りとして止める。"""
    g = list(trial['gen_ids'])
    if len(g) >= len(prompt_ids) and g[:len(prompt_ids)] == list(prompt_ids):
        raise ToolError('書き出しの根の件数にプロンプトごと渡された（生成した部分だけを渡す）')
    ki, rule, bwk = scorer_key(trial['text'], mod)
    r = P.root_counts_one(trial['text'], trial['gen_ids'], prefix_ids, strings, set_ids, window, ki=ki)
    r['key_rule'], r['scorer_block_without_key'] = rule, bwk
    return r


def cell_summary(C, key, trials, scored, roots):
    """升目の集計（転記行 C の升目の欄）。分母は升目の試行の全件（`behavior_pilot.trials_per_cell` と同じことを確かめる）。"""
    n = len(trials)
    if n != int(C['behavior_pilot']['trials_per_cell']) or len(scored) != n or len(roots) != n:
        raise ToolError('升目の試行の数が正本と違う: %s（%d）' % (key, n))
    z = C['behavior_pilot']['rate']['interval']['z']
    k = sum(1 for s in scored if s['counted'])
    trunc = sum(1 for t in trials if t['finish'] == 'length')
    sc_ = [s['score'] for s in scored]
    count = lambda f: sum(1 for s in sc_ if s is not None and f(s))
    un = {r: sum(1 for s in scored if r in s['unscorable']) for r in UNSCORABLE_REASONS}
    un_any = sum(1 for s in scored if s['unscorable'])
    rc = P.root_counts_cell(roots, C['behavior_pilot']['root_counts']['b']['window_chars'])
    rc['key_rule'] = {r: sum(1 for x in roots if x['key_rule'] == r) for r in KEY_RULES}
    rc['scorer_block_without_key'] = sum(1 for x in roots if x['scorer_block_without_key'])
    lo, hi = P.wilson(k, n, z)
    return collections.OrderedDict([
        ('cell', key), ('n', n), ('catastrophe', k), ('rate', k / n), ('wilson95', [lo, hi]),
        ('refuse', count(lambda s: s['choice'] == 'refuse')), ('format_fail', count(lambda s: s['format_fail'])),
        ('json_direct', count(lambda s: s['style_b'])), ('name_mention', count(lambda s: s['style_a'])), ('test_mention', count(lambda s: s['mention'])),
        ('loop', count(lambda s: s['loop_flag'])), ('truncated', trunc),
        ('rate_excl_truncated', (k / (n - trunc)) if n > trunc else None),
        ('unscorable', un_any), ('unscorable_by_reason', un),
        ('root_counts', rc),
    ])


def closing_digests(cells_trials, cells_scored, env):
    """閉じた記録の数: 採点の器の SHA16・採点の出力の SHA-256・生成したトークンの番号の列の SHA-256（並びは正本 `cells_main` の順・試行の番号の順）。"""
    gen = [[t['cell'], t['trial_index'], t['gen_ids']] for key in cells_trials for t in cells_trials[key]]
    sco = [[key, i, s['score'], s['unscorable'], s['counted'], s['error']] for key in cells_scored for i, s in enumerate(cells_scored[key])]
    return {'scorer_sha16': dict(env['sha16']), 'scores_sha256': hashlib.sha256(_canon(sco).encode('utf-8')).hexdigest().upper(),
            'gen_ids_sha256': hashlib.sha256(_canon(gen).encode('utf-8')).hexdigest().upper(), 'n_trials': len(gen)}


def iii_status(C, summaries, tool_error=False):
    """(iii) に渡す行動の下見の状態（`bprime_run.run_pilot` の behavior）: 器の誤りで終わった・採点が定まらない・閉じた。"""
    if tool_error:
        return {'status': 'tool_error', 'rate': None}
    ex = P.unscorable_exceeds({k: (v['unscorable'], v['n']) for k, v in summaries.items()}, C['behavior_pilot']['scoring']['unscorable'])
    if ex['exceeds']:
        return {'status': 'unscorable', 'rate': {k: v['rate'] for k, v in summaries.items()}, 'cells': ex['cells']}
    return {'status': 'ok', 'rate': {k: v['rate'] for k, v in summaries.items()}}


# ---------------- 模型を読まない確かめ ----------------
class _Tok:
    """確かめ用の小さなトークナイザ（番号 ↔ 字）。"""
    M = {106: '<turn|>'}                    # 確かめに要る字だけ（ほかは番号の字）

    def convert_ids_to_tokens(self, ids):
        return [self.M.get(int(i), '<%d>' % int(i)) for i in ids]

    def convert_tokens_to_ids(self, t):
        return {v: k for k, v in self.M.items()}.get(t)


def _fake_summary(kw, eos, chain=EXPECTED_CHAIN, override=None):
    vals = dict(kw, **(override or {}))
    procs = []
    for t in chain:
        attr, key = CHAIN_VALUE.get(t, ('x', 'x'))
        p = {attr: vals.get(key)}
        if t != 'TemperatureLogitsWarper':
            p['min_tokens_to_keep'] = 1
        procs.append({'type': t, 'params': p})
    tok = _Tok()
    return {'fixed': {'values': vals, 'num_beams': 1, 'eos_token_id': list(eos), 'eos_tokens': tok.convert_ids_to_tokens(eos), 'pad_token_id': 0, 'bos_token_id': 2, 'processors': procs,
                      'stopping': [{'type': 'MaxLengthCriteria', 'params': {}}, {'type': 'EosTokenCriteria', 'params': {'eos_token_id': list(eos)}}]},
            'per_call': {'max_length': 100 + vals['max_new_tokens'], 'input_ids_seq_length': 100, 'max_length_criteria': {}}}


def _selftest():
    C = json.load(open(os.path.join(os.path.dirname(HERE), 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    kw = sampling_kwargs(C)
    assert list(kw) == C['behavior_pilot']['sampling']['keys_from_B'], kw
    assert kw['do_sample'] is True and kw['max_new_tokens'] == C['inputs']['generation_B']['max_tokens']
    ver = C['inputs']['versions']['transformers']
    eos = C['behavior_pilot']['sampling']['eos_token_id']
    tok = _Tok()
    got = check_resolved(_fake_summary(kw, eos), C, tok, ver)
    assert len(got) == 9
    cases = {
        '止める印が段階 B の値（R17）': (_fake_summary(kw, [151645, 151643]), ver),
        'top_k を渡し忘れ Gemma の既定が効いた': (_fake_summary(kw, eos, override={'top_k': 64}), ver),
        'do_sample が偽': (_fake_summary(kw, eos, override={'do_sample': False}), ver),
        'top_k の型が違う（値は同じ浮動小数）': (_fake_summary(kw, eos, override={'top_k': float(kw['top_k'])}), ver),
        '処理の並びに余分がある': (_fake_summary(kw, eos, chain=('RepetitionPenaltyLogitsProcessor',) + EXPECTED_CHAIN), ver),
        '処理の並びの順が違う': (_fake_summary(kw, eos, chain=('TopKLogitsWarper', 'TemperatureLogitsWarper', 'TopPLogitsWarper', 'MinPLogitsWarper')), ver),
        '会話の終わりのトークンが無い': (_fake_summary(kw, [1, 50]), ver),
        '版が違う': (_fake_summary(kw, eos), '4.57.3'),
    }
    for name, (s, v) in cases.items():
        try:
            check_resolved(s, C, tok, v)
            raise AssertionError('止まらない: ' + name)
        except ToolError:
            pass
    s = _fake_summary(kw, eos)
    s['per_call']['max_length'] += 1
    try:
        check_resolved(s, C, tok, ver)
        raise AssertionError('止まらない: 長さの上限')
    except ToolError:
        pass
    print('bprime_behavior.py %s SELFTEST PASS（標本化の鍵 %d・確かめ %d 項目・止まる例 %d）' % (VERSION, len(kw), len(got), len(cases) + 1))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    print(__doc__)
