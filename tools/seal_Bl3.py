# -*- coding: utf-8 -*-
"""seal_Bl3.py v2 —— B-lens 層三（Bl3）の予想の封印（2026-09-25・正本 `predictions.order`・`predictions.when`: 下見の前の凍結の後・下見の前に、コーディネータが先に封印して
SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する・裁定 D148・D210・`tools/seal_Blens.py` v2 の型）。

相:
  coordinator  コーディネータの選んだ値（鍵 → 値の JSON）から、予想の JSON を書式（`records/predictions/predictions-form-Bl3-v1.html`）の JS と**同じ形**で書く
               （様式の名・プログラム・正本の版の三つの後に、書式の全ての欄の鍵を並べ替えて置く・字下げ一・末尾の改行なし）。書式と同じ鍵・同じ選択肢だけを受ける。
               下見の前の凍結の記録が無ければ止め、書式の SHA16 が凍結の記録と違えば止める（正本 `predictions.when`）。
               コーディネータは予想の欄を全て埋める。ただし q2 を「零」にしたときの q7 は「予想しない」のまま（q7 は等方の外の v̂ の行があるときだけの項目・
               `predictions.q7_rule`）。情報状態の欄（`free`）を空にしない（正本 `predictions.free`）。書いた JSON の SHA-256 を印字する（登録者には SHA だけを伝える）。
  registrant   登録者が書式で作った JSON（ダウンロードしたもの）を、チャットに貼られた SHA-256 と突き合わせてから、そのまま置き場に写す。書式の鍵と選択肢の内にあることを確かめる。
  record       封印の記録（両方の予想の JSON の置き場と SHA-256・順と時刻・情報状態の決まり・下見の前の凍結の記録の SHA16）を書く。Colab の起動器の相 pilot と相 main は、
               この記録が無ければ走らない。
既にあるファイルには書かない（封印は一度だけ）。予想の欄は「予想しない」を値として受ける（書式の初めの値・B-lens の逸脱 D-BL1 の型）。
用法: python tools/seal_Bl3.py coordinator --choices <値の JSON> --date <日付>
      python tools/seal_Bl3.py registrant --json <登録者の JSON> --sha <SHA-256>
      python tools/seal_Bl3.py record ／ --selftest
柵: 本器のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import make_predictions_form_Bl3 as FORM

VERSION = 'v2'          # v2（2026-09-25・裁定 D236）: 登録者の情報状態の欄が空なら、封印は止めずに印を置いて知らせる
PRED = os.path.join(REPO, 'records', 'predictions')
PATHS = {'coordinator': os.path.join(PRED, 'predictions-Bl3-coordinator.json'), 'registrant': os.path.join(PRED, 'predictions-Bl3-registrant.json')}
RECORD_JSON = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
RECORD_MD = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.md')
FREEZE = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
ROLE_WHO = {'coordinator': 'コーディネータ', 'registrant': '登録者'}
rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
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


def validate(values, keys, opts, role, T, full=False):
    bad = [k for k in values if k not in keys and k not in ('form', 'program', 'contrasts')]
    if bad:
        raise SystemExit('書式に無い鍵: %s' % bad)
    pred = set(FORM.prediction_keys(T))
    for k, v in values.items():
        if k in opts and v not in opts[k] and not (v == FORM.NP and k in pred):     # 「予想しない」は予想の欄の初めの値（ボタンではない）
            raise SystemExit('書式に無い選択肢: %s=%s' % (k, v))
    if values.get('who') != ROLE_WHO[role]:
        raise SystemExit('予想者の欄が役と合わない: %s' % values.get('who'))
    if full:
        miss = []
        q7_moot = values.get('q2.vhat_iso') == '零'
        for k in FORM.prediction_keys(T):
            v = values.get(k, FORM.NP)
            if k == 'q7.direction' and q7_moot:
                if v != FORM.NP:
                    miss.append('%s（q2 が「零」なのに q7 がある）' % k)
            elif v == FORM.NP:
                miss.append(k)
        if not (values.get('free') or '').strip():
            miss.append('free（情報状態）')
        if miss:
            raise SystemExit('コーディネータの予想に埋まっていない欄がある: %s' % miss)


def require_prepilot_freeze():
    """下見の前の凍結の記録があり、書式の SHA16 が凍結の記録と同じこと（正本 predictions.when）。"""
    if not os.path.exists(FREEZE):
        raise SystemExit('下見の前の凍結の記録が無い（封印は凍結の後・正本 predictions.when）: %s' % rel(FREEZE))
    FR = json.load(open(FREEZE, encoding='utf-8'))
    want = (FR.get('frozen_sha16') or {}).get(rel(FORM.OUT))
    if want is None or want != sha16f(FORM.OUT):
        raise SystemExit('書式の SHA16 が凍結の記録と違う（凍結の後に書式が変わった）: %s ≠ %s' % (sha16f(FORM.OUT), want))
    if 'main_freeze' in FR:
        raise SystemExit('凍結の記録に本の凍結がある（封印は下見の前・正本 predictions.when）')
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
    s = to_json(vals, T, keys, M)
    b = s.encode('utf-8')
    os.makedirs(PRED, exist_ok=True)
    open(PATHS['coordinator'], 'wb').write(b)
    print('[seal_Bl3] コーディネータの予想を封印した: %s・SHA-256 %s（登録者には SHA だけを伝える）' % (rel(PATHS['coordinator']), sha256b(b)))


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
        print('[seal_Bl3] 登録者の情報状態の欄が空です（%s）。封印は止めません。正本 predictions.free（裁定 D217）は両方が書くとするので、登録者にお知らせします' % '・'.join(empty))
    open(PATHS['registrant'], 'wb').write(b)
    print('[seal_Bl3] 登録者の予想を写した: %s・SHA-256 %s' % (rel(PATHS['registrant']), sha256b(b)))


def info_empty(v):
    """情報状態の欄（`info.coi`・`free`）のうち、空のものの名（正本 predictions.free・裁定 D217・D236）。"""
    return [k for k in ('info.coi', 'free') if not str(v.get(k) or '').strip()]


def record():
    if os.path.exists(RECORD_JSON):
        raise SystemExit('既にある（封印の記録は一度だけ）: %s' % rel(RECORD_JSON))
    require_prepilot_freeze()
    T, keys, opts, M = form_spec()
    R = {'kind': 'bl3_sealing_record', 'version': VERSION, 'written_utc': now(), 'order': T['predictions']['order'], 'when': T['predictions']['when'],
         'free_rule': T['predictions']['free'], 'freeze_record_sha16': sha16f(FREEZE),
         'form': {'path': rel(FORM.OUT), 'sha256': sha256b(open(FORM.OUT, 'rb').read()), 'meta': M}, 'predictions': {}}
    for role, p in PATHS.items():
        if not os.path.exists(p):
            raise SystemExit('予想の JSON が無い: %s' % rel(p))
        b = open(p, 'rb').read()
        v = json.loads(b.decode('utf-8'))
        validate(v, keys, opts, role, T, full=(role == 'coordinator'))
        R['predictions'][role] = {'path': rel(p), 'sha256': sha256b(b), 'date': v.get('date'), 'n_predicted': sum(1 for k in FORM.prediction_keys(T) if v.get(k) not in (None, '', FORM.NP)),
                                  'info_empty': info_empty(v)}                 # 情報状態の欄が空なら、その欄の名（裁定 D236）
    R['clause'] = '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
    json.dump(R, open(RECORD_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    md = ['# B-lens 層三の予想の封印の記録（機械生成・`tools/seal_Bl3.py` %s・%s）' % (VERSION, R['written_utc']), '',
          '- 順: %s' % R['order'], '- 時: %s' % R['when'], '- 情報状態の決まり: %s' % R['free_rule'],
          '- 書式: `%s`（SHA-256 %s）' % (R['form']['path'], R['form']['sha256']), '- 下見の前の凍結の記録: `%s`（SHA16 %s）' % (rel(FREEZE), R['freeze_record_sha16'])]
    md += ['- %s の予想: `%s`（SHA-256 %s・日付 %s・予想した欄 %d%s）' % (ROLE_WHO[r], x['path'], x['sha256'], x['date'], x['n_predicted'],
                                                              ('・情報状態の欄が空: %s' % '・'.join(x['info_empty'])) if x['info_empty'] else '') for r, x in R['predictions'].items()]
    md += ['- この記録が無ければ、Colab の起動器の相 pilot と相 main は走らない。', '', R['clause'], '']
    open(RECORD_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(md))
    print('[seal_Bl3] 封印の記録を書いた: %s' % rel(RECORD_JSON))


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
            vals.update({'q2.vhat_iso': '一から三', 'who': 'コーディネータ', 'info.coi': 'x', 'free': '露出の記録を読んだ', 'date': '2026-09-26'})
            validate(vals, keys, opts, 'coordinator', T, full=True)
            s = to_json(vals, T, keys, M)
            o = json.loads(s)
            assert list(o)[:3] == ['form', 'program', 'contrasts'] and list(o)[3:] == sorted(keys) and not s.endswith('\n')
            # 止まるべき場合（正しい理由で）: 埋まっていない予想・q2 が零なのに q7 がある・情報状態が空・書式に無い値
            for k_, v_, why in (('q5.gate_wo_vhat', FORM.NP, '埋まっていない'), ('q2.vhat_iso', '零', 'q7 がある'), ('free', '  ', '情報状態')):
                try:
                    validate(dict(vals, **{k_: v_}), keys, opts, 'coordinator', T, full=True)
                    raise AssertionError('通してはいけない予想を通した: %s=%s' % (k_, v_))
                except SystemExit as e_:
                    assert why in str(e_), ('別の理由で止まった', k_, str(e_))
            # 通るべき場合: q2 が零で q7 が「予想しない」
            validate(dict(vals, **{'q2.vhat_iso': '零', 'q7.direction': FORM.NP}), keys, opts, 'coordinator', T, full=True)
            # 選ばない欄のある登録者の JSON
            v5 = {k: FORM.NP for k in FORM.prediction_keys(T)}
            v5.update({'q1.pilot': '続ける', 'q4.gate': '通らない', 'who': '登録者', 'info.coi': '', 'free': '', 'date': '2026-09-26'})
            validate(v5, keys, opts, 'registrant', T, full=False)
            for k_, bad_ in (('q4.gate', 'x'), ('who', FORM.NP)):
                try:
                    validate(dict(v5, **{k_: bad_}), keys, opts, 'registrant', T, full=False)
                    raise AssertionError('書式に無い値を通した: %s=%s' % (k_, bad_))
                except SystemExit as e_:
                    assert '書式に無い選択肢' in str(e_) or '予想者の欄' in str(e_), str(e_)
            # 端から端まで（一時の置き場・凍結の記録が無い → 止まる・凍結の記録 → コーディネータ → 登録者 → 記録・本の凍結の後は止まる）
            g['PRED'] = td0
            g['PATHS'] = {'coordinator': os.path.join(td0, 'c.json'), 'registrant': os.path.join(td0, 'r.json')}
            g['RECORD_JSON'], g['RECORD_MD'], g['FREEZE'] = os.path.join(td0, 'rec.json'), os.path.join(td0, 'rec.md'), os.path.join(td0, 'fr.json')
            cj = os.path.join(td0, 'choices.json')
            json.dump({k: v for k, v in vals.items() if k not in ('who', 'date')}, open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
            try:
                coordinator(cj, '2026-09-26')
                raise AssertionError('凍結の記録が無いのに封印した')
            except SystemExit as e_:
                assert '凍結の記録が無い' in str(e_), str(e_)
            json.dump({'frozen_sha16': {rel(FORM.OUT): sha16f(FORM.OUT)}}, open(g['FREEZE'], 'w', encoding='utf-8'))
            coordinator(cj, '2026-09-26')
            rj = os.path.join(td0, 'registrant-download.json')
            rb = to_json(v5, T, keys, M).encode('utf-8')
            open(rj, 'wb').write(rb)
            registrant(rj, sha256b(rb))
            record()
            R = json.load(open(g['RECORD_JSON'], encoding='utf-8'))
            assert set(R['predictions']) == {'coordinator', 'registrant'} and R['predictions']['registrant']['sha256'] == sha256b(rb)
            assert open(g['PATHS']['registrant'], 'rb').read() == rb
            json.dump({'frozen_sha16': {rel(FORM.OUT): sha16f(FORM.OUT)}, 'main_freeze': {}}, open(g['FREEZE'], 'w', encoding='utf-8'))
            try:
                require_prepilot_freeze()
                raise AssertionError('本の凍結の後の封印を通した')
            except SystemExit as e_:
                assert '本の凍結' in str(e_), str(e_)
        finally:
            g.update(saved)
            FORM.OUT = saved_out
    print('[seal_Bl3] 自己検査 OK（%s・凍結の記録の確かめと「予想しない」の欄を含む封印を端から端まで通した）' % VERSION)


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
