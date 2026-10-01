# -*- coding: utf-8 -*-
"""bprime_behavior.py v0（2026-09-30・B′ の行動の下見の器・生成の設定の部分・Gemma-4-31B-it・transformers 5 系・コーディネータ南無弥勒如来）。

v0 に入れたのは、生成の設定を `generate` の中から取って確かめる部分だけ（生成の回し方・復号・採点・書き出しの根の件数は次の版で足す）:
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
import os, sys, copy, math, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_core as P

VERSION = 'v0'
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
