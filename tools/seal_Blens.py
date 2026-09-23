# -*- coding: utf-8 -*-
"""seal_Blens.py v2 —— B-lens の予想の封印（2026-09-23・正本 `predictions.order`: コーディネータが先に封印して SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する・裁定 D148 の順）。

相:
  coordinator  コーディネータの選んだ値（鍵 → 値の JSON）から、予想の JSON を書式（`records/predictions/predictions-form-Blens-v1.html`）の JS と**同じ形**で書く
               （様式の名・プログラム・正本の版の三つの後に、書式の全ての欄の鍵を並べ替えて置く・字下げ一・末尾の改行なし）。書式と同じ鍵・同じ選択肢だけを受ける。
               コーディネータは予想の欄を全て埋める（札が「付かない」の項目の向きの欄だけは「予想しない」のまま）。書いた JSON の SHA-256 を印字する（登録者には SHA だけを伝える）。
  registrant   登録者が書式で作った JSON（ダウンロードしたもの）を、チャットに貼られた SHA-256 と突き合わせてから、そのまま置き場に写す。書式の鍵と選択肢の内にあることを確かめる。
  record       封印の記録（両方の予想の JSON の置き場と SHA-256・順と時刻・情報状態）を書く。層一・層二の器と Colab の起動器は、この記録が無ければ射影を計算しない。
既にあるファイルには書かない（封印は一度だけ）。
v2（2026-09-24・凍結の後の逸脱 D-BL1・登録者裁定 D188）: 予想の欄に限って「予想しない」を値として受ける。書式の「予想しない」はボタンではなく欄の初めの値なので、
  v1 は書式のボタンから作った選択肢の一覧に無い値として、どの欄の「予想しない」も止めていた（札が「付かない」の項目の向きの欄も、登録者が選ばなかった欄も）。
  ほかの確かめは変えない。自己検査に、通るべき場合・選ばない欄のある登録者の JSON・正しい理由で止まる場合・一時の置き場での端から端までの封印を足した。
用法: python tools/seal_Blens.py coordinator --choices <値の JSON> --date 2026-09-24
      python tools/seal_Blens.py registrant --json <登録者の JSON> --sha <SHA-256>
      python tools/seal_Blens.py record ／ --selftest
柵: 本器のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import make_predictions_form_Blens as FORM

VERSION = 'v2'
PRED = os.path.join(REPO, 'records', 'predictions')
PATHS = {'coordinator': os.path.join(PRED, 'predictions-Blens-coordinator.json'), 'registrant': os.path.join(PRED, 'predictions-Blens-registrant.json')}
RECORD_JSON = os.path.join(REPO, 'records', 'Blens', 'sealing-record-Blens.json')
RECORD_MD = os.path.join(REPO, 'records', 'Blens', 'sealing-record-Blens.md')
ROLE_WHO = {'coordinator': 'コーディネータ', 'registrant': '登録者'}
rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


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


def validate(values, keys, opts, role, full=False):
    bad = [k for k in values if k not in keys and k not in ('form', 'program', 'contrasts')]
    if bad:
        raise SystemExit('書式に無い鍵: %s' % bad)
    pred = set(FORM.prediction_keys())
    for k, v in values.items():
        if k in opts and v not in opts[k] and not (v == FORM.NP and k in pred):     # 「予想しない」は予想の欄の初めの値（ボタンではない・逸脱 D-BL1）
            raise SystemExit('書式に無い選択肢: %s=%s' % (k, v))
    if values.get('who') != ROLE_WHO[role]:
        raise SystemExit('予想者の欄が役と合わない: %s' % values.get('who'))
    if full:
        miss = []
        for p, fs in FORM.FIELDS:
            labels = {k.rsplit('.', 1)[0]: values.get(k) for k, _, _ in fs if k.endswith('.label')}
            for k, o, _ in fs:
                v = values.get(k, FORM.NP)
                if k.endswith('.dir') and labels.get(k.rsplit('.', 1)[0]) == '付かない':
                    if v != FORM.NP:
                        miss.append('%s（札が付かないのに向きがある）' % k)
                elif v == FORM.NP:
                    miss.append(k)
            if values.get('%s.conf' % p, FORM.NP) == FORM.NP:
                miss.append('%s.conf' % p)
        if miss:
            raise SystemExit('コーディネータの予想に埋まっていない欄がある: %s' % miss)


def coordinator(choices_path, date):
    if os.path.exists(PATHS['coordinator']):
        raise SystemExit('既にある（封印は一度だけ）: %s' % rel(PATHS['coordinator']))
    if os.path.exists(PATHS['registrant']):
        raise SystemExit('登録者の予想が先にある（正本の順はコーディネータが先）')
    T, keys, opts, M = form_spec()
    vals = {k: FORM.NP for k in opts}
    vals.update({k: '' for k in keys if k not in opts})
    vals.update(json.load(open(choices_path, encoding='utf-8')))
    vals['who'], vals['date'] = ROLE_WHO['coordinator'], date
    validate(vals, keys, opts, 'coordinator', full=True)
    s = to_json(vals, T, keys, M)
    b = s.encode('utf-8')
    os.makedirs(PRED, exist_ok=True)
    open(PATHS['coordinator'], 'wb').write(b)
    print('[seal_Blens] コーディネータの予想を封印した: %s・SHA-256 %s（登録者には SHA だけを伝える）' % (rel(PATHS['coordinator']), sha256b(b)))


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
    validate(vals, keys, opts, 'registrant', full=False)
    open(PATHS['registrant'], 'wb').write(b)
    print('[seal_Blens] 登録者の予想を写した: %s・SHA-256 %s' % (rel(PATHS['registrant']), sha256b(b)))


def record():
    if os.path.exists(RECORD_JSON):
        raise SystemExit('既にある（封印の記録は一度だけ）: %s' % rel(RECORD_JSON))
    T, keys, opts, M = form_spec()
    R = {'kind': 'blens_sealing_record', 'version': VERSION, 'written_utc': now(), 'order': T['predictions']['order'], 'information_state': T['predictions']['information_state'],
         'form': {'path': rel(FORM.OUT), 'sha256': sha256b(open(FORM.OUT, 'rb').read()), 'meta': M}, 'predictions': {}}
    for role, p in PATHS.items():
        if not os.path.exists(p):
            raise SystemExit('予想の JSON が無い: %s' % rel(p))
        b = open(p, 'rb').read()
        v = json.loads(b.decode('utf-8'))
        validate(v, keys, opts, role, full=(role == 'coordinator'))
        R['predictions'][role] = {'path': rel(p), 'sha256': sha256b(b), 'date': v.get('date'), 'n_predicted': sum(1 for k in FORM.prediction_keys() if v.get(k) not in (None, '', FORM.NP))}
    R['clause'] = '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
    json.dump(R, open(RECORD_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    md = ['# B-lens の予想の封印の記録（機械生成・`tools/seal_Blens.py` %s・%s）' % (VERSION, R['written_utc']), '',
          '- 順: %s' % R['order'], '- 情報状態: %s' % R['information_state'],
          '- 書式: `%s`（SHA-256 %s）' % (R['form']['path'], R['form']['sha256'])]
    md += ['- %s の予想: `%s`（SHA-256 %s・日付 %s・予想した欄 %d）' % (ROLE_WHO[r], x['path'], x['sha256'], x['date'], x['n_predicted']) for r, x in R['predictions'].items()]
    md += ['- この記録が無ければ、層一・層二の器と Colab の起動器の相 extract は射影を計算しない。', '', R['clause'], '']
    open(RECORD_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(md))
    print('[seal_Blens] 封印の記録を書いた: %s' % rel(RECORD_JSON))


def _selftest():
    import tempfile
    T, keys, opts, M = form_spec()
    vals = {k: opts[k][0] for k in opts}
    for p, fs in FORM.FIELDS:
        for k, o, _ in fs:
            if k.endswith('.label'):
                vals[k] = '両方'
    vals.update({'who': 'コーディネータ', 'info.coi': 'x', 'free': '', 'date': '2026-09-24'})
    validate(vals, keys, opts, 'coordinator', full=True)
    s = to_json(vals, T, keys, M)
    o = json.loads(s)
    assert list(o)[:3] == ['form', 'program', 'contrasts'] and list(o)[3:] == sorted(keys) and not s.endswith('\n')
    v2 = dict(vals)
    v2['p1.survival.label'] = '付かない'
    try:
        validate(v2, keys, opts, 'coordinator', full=True)
        raise AssertionError('札が付かないのに向きがある予想を通した')
    except SystemExit:
        pass
    v3 = dict(vals)
    v3['p8.answer'] = '予想しない'
    try:
        validate(v3, keys, opts, 'coordinator', full=True)
        raise AssertionError('埋まっていない予想を通した')
    except SystemExit as e_:
        assert '埋まっていない' in str(e_), ('埋まっていない予想が別の理由で止まった', str(e_))      # 正しい理由で止まる（逸脱 D-BL1）
    # 通るべき場合: 札が「付かない」の項目の向きの欄は「予想しない」のまま（逸脱 D-BL1 の元の場合）
    v4 = dict(vals)
    for fam in ('survival', 'nuclear'):
        v4['p1.%s.label' % fam], v4['p1.%s.dir' % fam] = '付かない', FORM.NP
    validate(v4, keys, opts, 'coordinator', full=True)
    # 選ばない欄のある登録者の JSON（書式は選ばなかった欄に「予想しない」を書き出す）
    v5 = {k: FORM.NP for k in FORM.prediction_keys()}
    v5.update({'p1.survival.label': '両方', 'p1.survival.dir': '反対', 'p6.gate': '通らない', 'info.read_votes': '一部', 'info.read_facts': '見た',
               'who': '登録者', 'info.coi': '', 'free': '', 'date': '2026-09-24'})
    validate(v5, keys, opts, 'registrant', full=False)
    # 書式に無い値は、予想の欄でもほかの欄でも止まる（「予想しない」を受けるのは予想の欄だけ）
    for k_, bad_ in (('p8.answer', 'x'), ('info.read_votes', FORM.NP), ('who', FORM.NP)):
        try:
            validate(dict(v5, **{k_: bad_}), keys, opts, 'registrant', full=False)
            raise AssertionError('書式に無い値を通した: %s=%s' % (k_, bad_))
        except SystemExit as e_:
            assert '書式に無い選択肢' in str(e_) or '予想者の欄' in str(e_), str(e_)
    # 端から端まで（一時の置き場・コーディネータ → 登録者 → 記録）
    g = globals()
    saved = {n: g[n] for n in ('PRED', 'PATHS', 'RECORD_JSON', 'RECORD_MD')}
    with tempfile.TemporaryDirectory() as td:
        try:
            g['PRED'] = td
            g['PATHS'] = {'coordinator': os.path.join(td, 'c.json'), 'registrant': os.path.join(td, 'r.json')}
            g['RECORD_JSON'], g['RECORD_MD'] = os.path.join(td, 'rec.json'), os.path.join(td, 'rec.md')
            cj = os.path.join(td, 'choices.json')
            json.dump({k: v for k, v in v4.items() if k not in ('who', 'date')}, open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
            coordinator(cj, '2026-09-24')
            rj = os.path.join(td, 'registrant-download.json')
            rb = to_json(v5, T, keys, M).encode('utf-8')
            open(rj, 'wb').write(rb)
            registrant(rj, sha256b(rb))
            record()
            R = json.load(open(g['RECORD_JSON'], encoding='utf-8'))
            assert set(R['predictions']) == {'coordinator', 'registrant'} and R['predictions']['registrant']['sha256'] == sha256b(rb)
            assert open(g['PATHS']['registrant'], 'rb').read() == rb
        finally:
            g.update(saved)
    print('[seal_Blens] 自己検査 OK（%s・「予想しない」の欄を含む封印を端から端まで通した）' % VERSION)


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
