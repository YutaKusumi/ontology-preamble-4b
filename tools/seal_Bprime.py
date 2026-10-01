# -*- coding: utf-8 -*-
"""seal_Bprime.py v0（2026-09-30・B′ の予想の封印・正本 `predictions.order`・`predictions.when`: 下見の前の凍結の後・行動の下見の前に、コーディネータが先に封印して
SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する・層三の `tools/seal_Bl3.py` v2 の型・コーディネータ南無弥勒如来）。

相:
  coordinator  コーディネータの選んだ値（鍵 → 値の JSON）から、予想の JSON を書式の JS と同じ形で書く（様式の名・プログラム・正本の版の三つの後に、書式の全ての欄の鍵を
               並べ替えて置く・字下げ一・末尾の改行なし）。書式と同じ鍵・同じ選択肢だけを受ける。下見の前の凍結の記録が無ければ止め、書式の SHA16 が凍結の記録と違えば止める。
               コーディネータは予想の欄を全て埋め、情報状態の欄（`free`）を空にしない。書いた JSON の SHA-256 を印字する（登録者には SHA だけを伝える）。
  registrant   登録者が書式で作った JSON を、チャットに貼られた SHA-256 と突き合わせてから、そのまま置き場に写す。書式の鍵と選択肢の内にあることを確かめる。
  record       封印の記録（両方の予想の JSON の置き場と SHA-256・順と時刻・下見の前の凍結の記録の SHA16・封印の時刻〔日本時間・暦の期限の起点〕）を書く。
               Colab の起動器の相 extract より後は、この記録が無ければ走らない。
既にあるファイルには書かない（封印は一度だけ）。予想の欄は「予想しない」を値として受ける（書式の初めの値）。
用法: python seal_Bprime.py coordinator --choices <値の JSON> --date <日付>
      python seal_Bprime.py registrant --json <登録者の JSON> --sha <SHA-256>
      python seal_Bprime.py record ／ --selftest
柵: 本器のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make_predictions_form_Bprime as FORM

VERSION = 'v0'
PRED = os.path.join(ROOT, 'records', 'predictions')
PATHS = {'coordinator': os.path.join(PRED, 'predictions-Bprime-coordinator.json'), 'registrant': os.path.join(PRED, 'predictions-Bprime-registrant.json')}
RECORD_JSON = os.path.join(ROOT, 'records', 'Bprime', 'sealing-record-Bprime.json')
RECORD_MD = os.path.join(ROOT, 'records', 'Bprime', 'sealing-record-Bprime.md')
FREEZE = os.path.join(ROOT, 'records', 'Bprime', 'FREEZE-RECORD-Bprime.json')
ROLE_WHO = {'coordinator': 'コーディネータ', 'registrant': '登録者'}
JST = datetime.timezone(datetime.timedelta(hours=9))
rel = lambda p: os.path.relpath(p, ROOT).replace(os.sep, '/')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def form_spec():
    T = FORM.load_T()
    h = open(FORM.OUT, encoding='utf-8').read()
    keys, opts = FORM.read_form(h)
    return T, keys, opts, FORM.meta(T)


def to_json(values, T, keys, M):
    """書式の JS（`gen`）と同じ形の JSON の文字列（JSON.stringify(sorted, null, 1)）。"""
    o = {'form': M['form'], 'program': M['program'], 'contrasts': M['contrasts']}
    for k in sorted(keys):
        o[k] = values.get(k, '')
    return json.dumps(o, ensure_ascii=False, indent=1)


def validate(values, keys, opts, role, T, full=False):
    bad = [k for k in values if k not in keys and k not in ('form', 'program', 'contrasts')]
    if bad:
        raise SystemExit('書式に無い鍵: %s' % bad)
    pred = set(FORM.prediction_keys(T))
    for k, v in values.items():
        if k in opts and v not in opts[k] and not (v == FORM.NP and k in pred):
            raise SystemExit('書式に無い選択肢: %s=%s' % (k, v))
    if values.get('who') != ROLE_WHO[role]:
        raise SystemExit('予想者の欄が役と合わない: %s' % values.get('who'))
    if full:
        miss = [k for k in FORM.prediction_keys(T) if values.get(k, FORM.NP) == FORM.NP]
        if not (values.get('free') or '').strip():
            miss.append('free（情報状態）')
        if miss:
            raise SystemExit('コーディネータの予想に埋まっていない欄がある: %s' % miss)


def require_prepilot_freeze():
    if not os.path.exists(FREEZE):
        raise SystemExit('下見の前の凍結の記録が無い（封印は凍結の後・正本 predictions.when）: %s' % rel(FREEZE))
    FR = json.load(open(FREEZE, encoding='utf-8'))
    want = (FR.get('frozen_sha16') or {}).get(rel(FORM.OUT))
    if want is None or want != sha16f(FORM.OUT):
        raise SystemExit('書式の SHA16 が凍結の記録と違う（凍結の後に書式が変わった）: %s ≠ %s' % (sha16f(FORM.OUT), want))
    if 'main_freeze' in FR:
        raise SystemExit('凍結の記録に本の凍結がある（封印は行動の下見の前・正本 predictions.when）')
    return FR


def coordinator(choices_path, date):
    if os.path.exists(PATHS['coordinator']):
        raise SystemExit('既にある（封印は一度だけ）: %s' % rel(PATHS['coordinator']))
    if os.path.exists(PATHS['registrant']):
        raise SystemExit('登録者の予想が先にある（正本の順はコーディネータが先）')
    require_prepilot_freeze()
    T, keys, opts, M = form_spec()
    vals = {k: FORM.NP for k in opts}
    vals.update({k: '' for k in keys if k not in opts})
    vals.update(json.load(open(choices_path, encoding='utf-8')))
    vals['who'], vals['date'] = ROLE_WHO['coordinator'], date
    validate(vals, keys, opts, 'coordinator', T, full=True)
    b = to_json(vals, T, keys, M).encode('utf-8')
    os.makedirs(PRED, exist_ok=True)
    open(PATHS['coordinator'], 'wb').write(b)
    print('[seal_Bprime] コーディネータの予想を封印した: %s・SHA-256 %s（登録者には SHA だけを伝える）' % (rel(PATHS['coordinator']), sha256b(b)))


def registrant(json_path, sha):
    if not os.path.exists(PATHS['coordinator']):
        raise SystemExit('コーディネータの封印がまだ無い（正本の順）')
    if os.path.exists(PATHS['registrant']):
        raise SystemExit('既にある（封印は一度だけ）: %s' % rel(PATHS['registrant']))
    b = open(json_path, 'rb').read()
    if sha256b(b) != sha.strip().upper():
        raise SystemExit('登録者の JSON の SHA-256 がチャットの値と違う: %s ≠ %s' % (sha256b(b), sha))
    T, keys, opts, M = form_spec()
    vals = json.loads(b.decode('utf-8'))
    if any(vals.get(k) != M[k] for k in ('form', 'program', 'contrasts')):
        raise SystemExit('登録者の JSON の様式の名・プログラム・正本の版が書式と違う')
    validate(vals, keys, opts, 'registrant', T, full=False)
    empty = info_empty(vals)
    if empty:
        print('[seal_Bprime] 登録者の情報状態の欄が空です（%s）。封印は止めません。登録者にお知らせします' % '・'.join(empty))
    open(PATHS['registrant'], 'wb').write(b)
    print('[seal_Bprime] 登録者の予想を写した: %s・SHA-256 %s' % (rel(PATHS['registrant']), sha256b(b)))


def info_empty(v):
    return [k for k in ('info.coi', 'free') if not str(v.get(k) or '').strip()]


def record():
    if os.path.exists(RECORD_JSON):
        raise SystemExit('既にある（封印の記録は一度だけ）: %s' % rel(RECORD_JSON))
    require_prepilot_freeze()
    T, keys, opts, M = form_spec()
    t = datetime.datetime.now(JST)
    R = {'kind': 'bprime_sealing_record', 'version': VERSION, 'sealed_at_jst': t.isoformat(timespec='seconds'), 'sealed_at_utc': t.astimezone(datetime.timezone.utc).isoformat(timespec='seconds'),
         'order': T['predictions']['order'], 'when': T['predictions']['when'], 'exposure_rule': T['predictions']['exposure']['rule'], 'freeze_record_sha16': sha16f(FREEZE),
         'form': {'path': rel(FORM.OUT), 'sha256': sha256b(open(FORM.OUT, 'rb').read()), 'meta': M}, 'predictions': {},
         'calendar': {'days': T['computation']['stops']['calendar']['days'], 'rule': '封印の日（日本時間）を 0 日目とし、`computation.stops.calendar.days` 日目の日本時間の暦日の終わりまでに本の計算と独立の再計算を終えなければ閉じる（器の段の所見 K2）'}}
    for role, p in PATHS.items():
        if not os.path.exists(p):
            raise SystemExit('予想の JSON が無い: %s' % rel(p))
        b = open(p, 'rb').read()
        v = json.loads(b.decode('utf-8'))
        validate(v, keys, opts, role, T, full=(role == 'coordinator'))
        R['predictions'][role] = {'path': rel(p), 'sha256': sha256b(b), 'date': v.get('date'), 'n_predicted': sum(1 for k in FORM.prediction_keys(T) if v.get(k) not in (None, '', FORM.NP)),
                                  'info_empty': info_empty(v)}
    R['clause'] = '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
    os.makedirs(os.path.dirname(RECORD_JSON), exist_ok=True)
    json.dump(R, open(RECORD_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    md = ['# B′ の予想の封印の記録（機械生成・`seal_Bprime.py` %s・封印 %s）' % (VERSION, R['sealed_at_jst']), '',
          '- 順: %s' % R['order'], '- 時: %s' % R['when'], '- 露出の決まり: %s' % R['exposure_rule'], '- 暦の期限: %s（%s 日）' % (R['calendar']['rule'], R['calendar']['days']),
          '- 書式: `%s`（SHA-256 %s）' % (R['form']['path'], R['form']['sha256']), '- 下見の前の凍結の記録: `%s`（SHA16 %s）' % (rel(FREEZE), R['freeze_record_sha16'])]
    md += ['- %s の予想: `%s`（SHA-256 %s・日付 %s・予想した欄 %d%s）' % (ROLE_WHO[r], x['path'], x['sha256'], x['date'], x['n_predicted'],
                                                              ('・情報状態の欄が空: %s' % '・'.join(x['info_empty'])) if x['info_empty'] else '') for r, x in R['predictions'].items()]
    md += ['- この記録が無ければ、Colab の起動器の相 extract より後は走らない。', '', R['clause'], '']
    open(RECORD_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(md))
    print('[seal_Bprime] 封印の記録を書いた: %s' % rel(RECORD_JSON))


def _selftest():
    import tempfile
    T = FORM.load_T()
    h = FORM.build(T)
    with tempfile.TemporaryDirectory() as td0:
        g = globals()
        saved = {n: g[n] for n in ('PRED', 'PATHS', 'RECORD_JSON', 'RECORD_MD', 'FREEZE')}
        saved_out = FORM.OUT
        try:
            FORM.OUT = os.path.join(td0, 'form.html')
            open(FORM.OUT, 'w', encoding='utf-8', newline='\n').write(h)
            T, keys, opts, M = form_spec()
            vals = {it['key']: it['options'][0] for it in FORM.items(T)}
            vals.update({'who': 'コーディネータ', 'info.coi': 'x', 'free': '露出の記録を読んだ', 'date': '2026-10-01'})
            validate(vals, keys, opts, 'coordinator', T, full=True)
            s = to_json(vals, T, keys, M)
            o = json.loads(s)
            assert list(o)[:3] == ['form', 'program', 'contrasts'] and list(o)[3:] == sorted(keys) and not s.endswith('\n')
            for k_, v_, why in (('q3.nk_iso', FORM.NP, '埋まっていない'), ('free', '  ', '情報状態')):
                try:
                    validate(dict(vals, **{k_: v_}), keys, opts, 'coordinator', T, full=True)
                    raise AssertionError('通してはいけない予想を通した: %s=%s' % (k_, v_))
                except SystemExit as e_:
                    assert why in str(e_), ('別の理由で止まった', k_, str(e_))
            v5 = {k: FORM.NP for k in FORM.prediction_keys(T)}
            v5.update({'q1.pilot': '続ける', 'who': '登録者', 'info.coi': '', 'free': '', 'date': '2026-10-01'})
            validate(v5, keys, opts, 'registrant', T, full=False)
            for k_, bad_ in (('q2.vhat_iso', 'x'), ('who', FORM.NP)):
                try:
                    validate(dict(v5, **{k_: bad_}), keys, opts, 'registrant', T, full=False)
                    raise AssertionError('書式に無い値を通した: %s=%s' % (k_, bad_))
                except SystemExit as e_:
                    assert '書式に無い選択肢' in str(e_) or '予想者の欄' in str(e_), str(e_)
            g['PRED'] = td0
            g['PATHS'] = {'coordinator': os.path.join(td0, 'c.json'), 'registrant': os.path.join(td0, 'r.json')}
            g['RECORD_JSON'], g['RECORD_MD'], g['FREEZE'] = os.path.join(td0, 'rec.json'), os.path.join(td0, 'rec.md'), os.path.join(td0, 'fr.json')
            cj = os.path.join(td0, 'choices.json')
            json.dump({k: v for k, v in vals.items() if k not in ('who', 'date')}, open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
            try:
                coordinator(cj, '2026-10-01')
                raise AssertionError('凍結の記録が無いのに封印した')
            except SystemExit as e_:
                assert '凍結の記録が無い' in str(e_), str(e_)
            json.dump({'frozen_sha16': {rel(FORM.OUT): sha16f(FORM.OUT)}}, open(g['FREEZE'], 'w', encoding='utf-8'))
            coordinator(cj, '2026-10-01')
            rj = os.path.join(td0, 'registrant-download.json')
            rb = to_json(v5, T, keys, M).encode('utf-8')
            open(rj, 'wb').write(rb)
            registrant(rj, sha256b(rb))
            record()
            R = json.load(open(g['RECORD_JSON'], encoding='utf-8'))
            assert set(R['predictions']) == {'coordinator', 'registrant'} and R['predictions']['registrant']['sha256'] == sha256b(rb) and R['sealed_at_jst']
            json.dump({'frozen_sha16': {rel(FORM.OUT): sha16f(FORM.OUT)}, 'main_freeze': {}}, open(g['FREEZE'], 'w', encoding='utf-8'))
            try:
                require_prepilot_freeze()
                raise AssertionError('本の凍結の後の封印を通した')
            except SystemExit as e_:
                assert '本の凍結' in str(e_), str(e_)
        finally:
            g.update(saved)
            FORM.OUT = saved_out
    print('[seal_Bprime] 自己検査 OK（%s・凍結の記録の確かめと「予想しない」の欄を含む封印を端から端まで通した）' % VERSION)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', nargs='?', choices=['coordinator', 'registrant', 'record'])
    ap.add_argument('--choices')
    ap.add_argument('--date')
    ap.add_argument('--json')
    ap.add_argument('--sha')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
    elif a.phase == 'coordinator':
        coordinator(a.choices, a.date)
    elif a.phase == 'registrant':
        registrant(a.json, a.sha)
    elif a.phase == 'record':
        record()
    else:
        ap.print_help()
