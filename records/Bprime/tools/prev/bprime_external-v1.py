# -*- coding: utf-8 -*-
"""bprime_external.py v0（2026-09-30・B′ の行動の下見の「系統外の模型による採点」の束と照らし・コーディネータ南無弥勒如来）。

正本 `behavior_pilot.external_scoring` のとおり:
  - 抜き取り（`sample`）: 試行の全件（正本 `cells_main` の順・試行の番号の順に並べる）から、`behavior_pilot.external_scoring.seed` の種で `n` 件を、重ねずに引く
    （`numpy.random.default_rng(種).choice(全件の数, n, replace=False)`）。引いた順が採点に見せる順（升目の並びを伏せる）。
  - 束（`bundle`）: 見せるのは、番号（E01〜）・族（採点の定義に要る）・応答の文字列だけ。升目・腕・試行の番号は伏せ、手元の対応表にだけ置く。
  - 依頼の文（`request_text`）: 正本 `behavior_pilot.external_scoring.request_text` をそのまま使い、後に束の応答を並べる（正本 `request_rule`・登録者の確認と器の実装の検分に掛ける）。
  - 返事の読み（`parse_reply`）と照らし（`agreement`）: 返事の一行ずつの JSON を読み、番号がそろうこと・値の形が決まりの内であることを確かめ、器の採点（`score_text` の書式外・選択・破局）と
    番号ごとに照らして、一致の件数と割合を出す（記述・妥当性の測定ではない）。系譜（模型の名・system_fingerprint）を転記行 C に置く。
送る操作（xAI の API）はこの器に置かない（送る前に登録者の確認を得る・鍵の値は読まない・印字しない）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_core as P

VERSION = 'v1'          # v1（2026-09-30）: 依頼の文を正本 `behavior_pilot.external_scoring.request_text` から読む（前は器の中の草案）。前の版は `prev/bprime_external-v0.py`
ToolError = P.ToolError
NL = chr(10)
REQUEST_KEY = ('behavior_pilot', 'external_scoring', 'request_text')           # 依頼の文は正本に置く（v1・器の段の所見 K10）


def ordered_keys(C, trials_by_cell):
    """試行の全件の並び（正本 `cells_main` の順・試行の番号の順）。"""
    out = []
    for sc, arm in C['cells_main']:
        key = '%s|%s' % (sc, arm)
        ts = trials_by_cell[key]
        if [t['trial_index'] for t in ts] != list(range(len(ts))):
            raise ToolError('試行の番号が 0 から順に並ばない: %s' % key)
        out += [(key, t['trial_index']) for t in ts]
    return out


def sample(C, trials_by_cell):
    import numpy as np
    E = C['behavior_pilot']['external_scoring']
    keys = ordered_keys(C, trials_by_cell)
    if len(keys) != C['behavior_pilot']['trials_total']:
        raise ToolError('試行の全件の数が正本と違う: %d' % len(keys))
    idx = np.random.default_rng(int(E['seed'])).choice(len(keys), size=int(E['n']), replace=False)
    return [keys[int(i)] for i in idx]


def bundle(C, trials_by_cell, families):
    """見せる束と手元の対応表。families: 升目 → 族。"""
    picks = sample(C, trials_by_cell)
    by = {(t['cell'], t['trial_index']): t for key in trials_by_cell for t in trials_by_cell[key]}
    items, private = [], collections.OrderedDict()
    for i, (key, ti) in enumerate(picks, 1):
        eid = 'E%02d' % i
        items.append({'id': eid, 'family': families[key], 'text': by[(key, ti)]['text']})
        private[eid] = [key, ti]
    return items, private


def request_text(C, items):
    parts = [C['behavior_pilot']['external_scoring']['request_text']]
    for it in items:
        parts += ['<<<%s はじめ（族: %s）>>>' % (it['id'], it['family']), it['text'], '<<<%s おわり>>>' % it['id'], '']
    return NL.join(parts)


def parse_reply(text, ids):
    """返事の一行ずつの JSON を読む。番号がそろい（重ならず・欠けず）、値の形が決まりの内であることを確かめる（落ちたら ToolError）。"""
    got = collections.OrderedDict()
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith('{'):
            continue
        o = json.loads(s)
        if set(o) != {'id', 'format', 'choice', 'catastrophe'}:
            raise ToolError('返事の行の鍵が決まりと違う: %s' % s[:80])
        if o['format'] not in ('ok', '書式外') or o['catastrophe'] not in (True, False, None) or not (o['choice'] is None or isinstance(o['choice'], str)):
            raise ToolError('返事の行の値が決まりの外: %s' % s[:80])
        if o['id'] in got:
            raise ToolError('返事の番号が重なる: %s' % o['id'])
        got[o['id']] = o
    if list(got) != list(ids):
        raise ToolError('返事の番号が束の番号とそろわない（%d 件・束 %d 件）' % (len(got), len(ids)))
    return got


def agreement(parsed, private, scored_by_cell):
    """器の採点と照らす（番号ごと）: 書式外か・選択・破局の三つがすべて同じなら一致。"""
    rows = []
    for eid, (key, ti) in private.items():
        s = scored_by_cell[key][ti]['score']
        tool = {'format': '書式外' if (s is None or s['format_fail']) else 'ok', 'choice': None if s is None else s['choice'], 'catastrophe': None if s is None else s['catastrophe']}
        ext = parsed[eid]
        same = {k: ext[k] == tool[k] for k in ('format', 'choice', 'catastrophe')}
        rows.append({'id': eid, 'agree': all(same.values()), 'same': same})
    n = len(rows)
    k = sum(1 for r in rows if r['agree'])
    return {'n': n, 'agree': k, 'share': k / n if n else None, 'by_field': {f: sum(1 for r in rows if r['same'][f]) for f in ('format', 'choice', 'catastrophe')}, 'rows': rows}


def _selftest():
    C = json.load(open(os.path.join(os.path.dirname(HERE), 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    n_cell = C['behavior_pilot']['trials_per_cell']
    tb = collections.OrderedDict()
    fam = {}
    for sc, arm in C['cells_main']:
        key = '%s|%s' % (sc, arm)
        fam[key] = 'nuclear' if sc == 'N1' else 'survival'
        tb[key] = [{'cell': key, 'trial_index': i, 'text': '応答 %s %d' % (key, i)} for i in range(n_cell)]
    items, private = bundle(C, tb, fam)
    items2, private2 = bundle(C, tb, fam)
    assert items == items2 and private == private2 and len(items) == C['behavior_pilot']['external_scoring']['n'] and len(set(map(tuple, private.values()))) == len(items)
    rq = request_text(C, items)
    assert rq.startswith(C['behavior_pilot']['external_scoring']['request_text'])
    assert all(('<<<%s はじめ' % it['id']) in rq for it in items)
    reply = NL.join(json.dumps({'id': it['id'], 'format': 'ok', 'choice': 'b', 'catastrophe': False}, ensure_ascii=False) for it in items)
    got = parse_reply('前置き' + NL + reply, [it['id'] for it in items])
    sc = {key: [{'score': {'format_fail': False, 'choice': 'b', 'catastrophe': False}} for _ in range(n_cell)] for key in tb}
    ag = agreement(got, private, sc)
    assert ag['agree'] == ag['n'] == len(items)
    first = private[items[0]['id']]
    sc[first[0]][first[1]] = {'score': {'format_fail': False, 'choice': 'a', 'catastrophe': True}}
    ag2 = agreement(got, private, sc)
    assert ag2['agree'] == ag['n'] - 1 and ag2['by_field']['format'] == ag['n']
    for bad in (reply.replace('"E01"', '"E99"'), reply + NL + reply.splitlines()[0], reply.replace('"ok"', '"OK"', 1)):
        try:
            parse_reply(bad, [it['id'] for it in items])
            raise AssertionError('止まらない')
        except ToolError:
            pass
    print('bprime_external.py %s SELFTEST PASS（抜き取り %d・見せる順の先頭 %s・一致 %d/%d と一件違いで %d）' % (VERSION, len(items), '・'.join('%s#%d' % tuple(v) for v in list(private.values())[:3]), ag['agree'], ag['n'], ag2['agree']))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    print(__doc__)
