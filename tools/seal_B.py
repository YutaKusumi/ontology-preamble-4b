# -*- coding: utf-8 -*-
"""seal_B.py v2 —— コーディネータの予想の JSON を書き、そこから**起草者の予想符号の封印**（裁定 D79・`seal_format`）を機械で作る（登録者裁定 D148・2026-09-19 の夜）。

- 予想の JSON は、書式 v0.9（`predictions.form`）が作る JSON と**同じ形**（様式の名・プログラム・正本の版の三つの後に、欄の鍵を並べ替えて置く・字下げ一・末尾の改行なし）で書く。
  書式と同じ欄の鍵・同じ選択肢だけを受ける（`tools/make_predictions_form_B.py` の書式から鍵を読む——手で並べない）。
- 起草者の封印（`records/B/seal-B.json`）は、予想の JSON の向きの欄と S4 の欄から作る（`seal_format.from_predictions`）。封印では「予想しない」を使えない。
  封印の欄は正本 `seal_format.record_keys` のとおり（signs・information_state・timing・who・s4・vhat_floor_ack）に、出所（予想の JSON とその SHA-256）を添える。
- 既にあるファイルには書かない（封印は一度だけ）。
v2（2026-09-19 の夜・封印の後・独立の目を通っていない）: **封印した予想の照合 `check_predictions`** を足した（凍結の器が呼ぶ）——
  登録者とコーディネータの予想の JSON が一つずつあること・書式の欄の鍵と選択肢の内にあること・予想者が名の役と合うこと・様式の名、
  起草者の封印が**コーディネータの予想の JSON から作ったまま**であること（出所の SHA-256・向き・S4）、
  封印の経緯の記録（`sealing-record-B-*.md`）に三つの SHA-256 が載っていること。
用法: python tools/seal_B.py --choices <選んだ値の JSON> --date 2026-09-19 ／ --selftest
柵: 本器のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, shutil, hashlib, argparse, tempfile
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B
import make_predictions_form_B as FORM

VERSION = 'v2'
REPO = runs_B.REPO
PRED_REL = 'records/predictions'
ROLES = {'registrant': '登録者', 'coordinator': 'コーディネータ'}     # ファイルの名の役 → 予想者の欄の値


class _Opts(HTMLParser):
    """書式の HTML から、欄の鍵と押しボタンの選択肢を読む（書式と同じ鍵・同じ選択肢だけを受けるため）。"""
    def __init__(self):
        super().__init__()
        self.keys, self.opts, self._cur = [], {}, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-k' in a:
            self.keys.append(a['data-k'])
            self._cur = a['data-k'] if a.get('type') == 'hidden' else None
            if self._cur:
                self.opts[self._cur] = []
        elif tag == 'button' and 'data-v' in a and self._cur:
            self.opts[self._cur].append(a['data-v'])


def form_schema(T):
    h, _ = FORM.build(T)
    p = _Opts()
    p.feed(h)
    return p.keys, p.opts


def to_json_text(T, values):
    """書式の JS（V′ 様式 v0.5 の gen）と同じ形の文字列にする。"""
    M = FORM.meta(T)
    o = {'form': M['form'], 'program': M['program'], 'contrasts': M['contrasts']}
    for k in sorted(values):
        o[k] = values[k]
    return json.dumps(o, ensure_ascii=False, indent=1)


def build(T, choices):
    keys, opts = form_schema(T)
    P = T['predictions']
    F = P['fields']
    miss = [k for k in keys if k not in choices]
    extra = [k for k in choices if k not in keys]
    if miss or extra:
        raise SystemExit('選んだ値の鍵が書式と違う（欠け %s・余り %s）' % (miss[:3], extra[:3]))
    bad = [(k, v) for k, v in choices.items() if k in opts and v not in opts[k]]
    if bad:
        raise SystemExit('選択肢の外の値: %s' % bad[:3])
    if choices[F['who']['key']] != 'コーディネータ':
        raise SystemExit('予想者がコーディネータでない')
    conf = [c['id'] for Fm in T['families'].values() for c in Fm['contrasts']]
    NP = P['not_predicted']
    signs = {i: choices[F['direction']['key_prefix'] + i] for i in conf}
    if NP in signs.values() or choices[F['s4']['key']] == NP:
        raise SystemExit('封印では「%s」を使えない（凍結の器が全対比の封印を求める・seal_format.from_predictions）' % NP)
    return to_json_text(T, choices), signs, choices[F['s4']['key']]


def seal_record(T, signs, s4, pred_rel, pred_sha, information_state, order_note, who):
    SF = T['seal_format']
    rec = {'signs': signs, 's4': s4, 'information_state': information_state, 'timing': SF['timing'].replace('**', ''),
           'who': who, 'vhat_floor_ack': '封印した者は、v̂ が行動の差の無い腕対（O と Osec・V′ の既測でどの場面でも床）から作られていることを知ったうえで予想した（`reading_D128.vhat_from_floor_pair`）',
           'source': {'predictions': pred_rel, 'sha256': pred_sha, 'derived_by': 'tools/seal_B.py %s' % VERSION, 'rule': SF['from_predictions']},
           'order_note': order_note}
    need = set(SF['record_keys'])
    assert need <= set(rec), ('封印の記録の欄が正本と違う', sorted(need - set(rec)))
    assert all(v in SF['sign_values'] for v in signs.values()) and s4 in SF['sign_values']
    return rec


def _sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def check_predictions(T, pred_dir, seal=None, seal_sha=None):
    """封印した予想の照合（凍結の器が呼ぶ）。戻り値: (止めるものの一覧, 記帳する情報)。

    pred_dir は `records/predictions` に当たる置き場。封印の記録（seal）と、その SHA-256（seal_sha）は渡されたときだけ照らす。"""
    probs, info = [], {}
    keys, opts = form_schema(T)
    P = T['predictions']
    F = P['fields']
    M = FORM.meta(T)
    NP = P['not_predicted']
    conf = [c['id'] for Fm in T['families'].values() for c in Fm['contrasts']]
    names = sorted(os.listdir(pred_dir)) if os.path.isdir(pred_dir) else []
    body = {}
    for role, who in ROLES.items():
        pat = re.compile(r'^predictions-%s-B-\d{4}-\d{2}-\d{2}(-v\d+)?\.json$' % role)
        fs = [f for f in names if pat.match(f)]
        if not fs:
            probs.append('%sの予想の JSON が無い（`%s/predictions-%s-B-<日付>.json`・正本 predictions.order）' % (who, PRED_REL, role))
            continue
        if len(fs) > 1:
            probs.append('%sの予想の JSON が複数ある（どれが拘束版か決めてから凍結する）: %s' % (who, '・'.join(fs)))
            continue
        b = open(os.path.join(pred_dir, fs[0]), 'rb').read()
        rel = '%s/%s' % (PRED_REL, fs[0])
        try:
            d = json.loads(b.decode('utf-8'))
        except Exception as e:
            probs.append('%sの予想の JSON が読めない: %s（%s）' % (who, rel, type(e).__name__))
            continue
        for k in ('form', 'program'):
            if d.get(k) != M[k]:
                probs.append('%sの予想の %s が書式と違う: %s（書式は %s・predictions.compare_rules.validation）' % (who, k, d.get(k), M[k]))
        v = {k: x for k, x in d.items() if k not in ('form', 'program', 'contrasts')}
        miss = [k for k in keys if k not in v]
        extra = [k for k in v if k not in keys]
        if miss or extra:
            probs.append('%sの予想の欄の鍵が書式と違う（欠け %d・余り %d: %s）' % (who, len(miss), len(extra), '・'.join((miss + extra)[:3])))
        bad = [(k, x) for k, x in v.items() if k in opts and x not in opts[k]]
        if bad:
            probs.append('%sの予想に選択肢の外の値がある: %s' % (who, '・'.join('%s=%s' % kv for kv in bad[:3])))
        if v.get(F['who']['key']) != who:
            probs.append('%sのファイルの予想者の欄が「%s」（名の役と合わない）' % (who, v.get(F['who']['key'])))
        pred_keys = [F['direction']['key_prefix'] + i for i in conf] + [F['s4']['key'], F['confirmed_band']['key'], F['gate1']['key']]
        info[role] = {'path': rel, 'sha256': _sha(b), 'bytes': len(b), 'form': d.get('form'), 'contrasts': d.get('contrasts'),
                      'contrasts_matches_canon': d.get('contrasts') == M['contrasts'], 'date': v.get('date'),
                      'not_predicted': sum(1 for k in pred_keys if v.get(k) == NP)}
        body[role] = v
    # 起草者の封印は、コーディネータの予想の JSON から作ったままか（二重に書かない・seal_format.from_predictions）
    if seal is not None and 'coordinator' in info:
        src = seal.get('source') or {}
        c = body['coordinator']
        if src.get('predictions') != info['coordinator']['path']:
            probs.append('封印の出所がコーディネータの予想の JSON と違う: %s（現物は %s）' % (src.get('predictions'), info['coordinator']['path']))
        if src.get('sha256') != info['coordinator']['sha256']:
            probs.append('封印の出所の SHA-256 がコーディネータの予想の JSON の現物と違う（封印の後に予想の JSON が変わった）')
        derived = {i: c.get(F['direction']['key_prefix'] + i) for i in conf}
        diff = [i for i in conf if (seal.get('signs') or {}).get(i) != derived[i]]
        if diff or set(seal.get('signs') or {}) != set(conf):
            probs.append('封印の予想符号がコーディネータの予想の JSON の向きと違う: %s' % '・'.join(diff[:3] or ['対比の集合が違う']))
        if seal.get('s4') != c.get(F['s4']['key']):
            probs.append('封印の S4 の値がコーディネータの予想の JSON と違う（封印 %s・予想 %s）' % (seal.get('s4'), c.get(F['s4']['key'])))
    elif seal is not None:
        probs.append('封印はあるが、元のコーディネータの予想の JSON が照らせない')
    # 封印の経緯の記録に、三つの SHA-256 が載っているか（封印の後にファイルが替わっていないか）
    recs = [f for f in names if re.match(r'^sealing-record-B-\d{4}-\d{2}-\d{2}\.md$', f)]
    if not recs:
        probs.append('封印の経緯の記録が無い（`%s/sealing-record-B-<日付>.md`）' % PRED_REL)
    else:
        txt = '\n'.join(open(os.path.join(pred_dir, f), encoding='utf-8').read() for f in recs)
        info['sealing_record'] = ['%s/%s' % (PRED_REL, f) for f in recs]
        want = [(ROLES[r], info[r]['sha256']) for r in ROLES if r in info] + ([('起草者の封印', seal_sha)] if seal_sha else [])
        for who, s in want:
            if s not in txt:
                probs.append('封印の経緯の記録に%sの SHA-256 が無い（現物 %s…）' % (who, s[:16]))
    return probs, info


def _fixture(T, root, reg_mut=None, reg_bytes_mut=None):
    """照合の自己検査の置き場を作る（登録者・コーディネータの予想の JSON・封印・封印の経緯の記録）。
    壊し方は、封印の経緯の記録を書く**前**に当てる（記録の SHA は壊した現物で書く——壊し方ごとに、見てほしい検査だけが止まるように）。"""
    keys, opts = form_schema(T)
    P = T['predictions']
    F = P['fields']
    SV = T['seal_format']['sign_values']
    pd = os.path.join(root, *PRED_REL.split('/'))
    os.makedirs(pd, exist_ok=True)
    ch = {k: (opts[k][-1] if k in opts else 'x') for k in keys}
    for k in keys:
        if k.startswith(F['direction']['key_prefix']):
            ch[k] = SV[0]
    ch[F['s4']['key']] = SV[2]
    ch[F['who']['key']] = 'コーディネータ'
    text, signs, s4 = build(T, ch)
    cb = text.encode('utf-8')
    open(os.path.join(pd, 'predictions-coordinator-B-2026-01-01.json'), 'wb').write(cb)
    rg = dict(ch)
    rg[F['who']['key']] = '登録者'
    rg[F['direction']['key_prefix'] + T['families']['B_sub']['contrasts'][0]['id']] = SV[1]
    if reg_mut:
        reg_mut(rg)
    rb = to_json_text(T, rg).encode('utf-8')
    if reg_bytes_mut:
        rb = reg_bytes_mut(rb)
    open(os.path.join(pd, 'predictions-registrant-B-2026-01-01.json'), 'wb').write(rb)
    seal = seal_record(T, signs, s4, '%s/predictions-coordinator-B-2026-01-01.json' % PRED_REL, _sha(cb), '情報状態', '順の注', '起草者')
    sb = (json.dumps(seal, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    open(os.path.join(pd, 'sealing-record-B-2026-01-01.md'), 'w', encoding='utf-8').write('| %s |\n| %s |\n| %s |\n' % (_sha(rb), _sha(cb), _sha(sb)))
    return pd, seal, _sha(sb), _sha(rb)


def _replace_in(path, old, new):
    s = open(path, encoding='utf-8').read()          # 読んでから書く（書き込みで開くと先に空になる）
    assert s.count(old) == 1, ('置き換える相手が一つでない', path)
    open(path, 'w', encoding='utf-8').write(s.replace(old, new))


def _selftest():
    T = runs_B.load_T()
    keys, opts = form_schema(T)
    P = T['predictions']
    F = P['fields']
    ch = {k: (opts[k][2] if k in opts and len(opts[k]) > 2 else (opts[k][0] if k in opts else '')) for k in keys}
    ch[F['who']['key']] = 'コーディネータ'
    for k in keys:
        if k.startswith(F['direction']['key_prefix']):
            ch[k] = T['seal_format']['sign_values'][0]
    ch[F['s4']['key']] = T['seal_format']['sign_values'][2]
    text, signs, s4 = build(T, ch)
    d = json.loads(text)
    assert list(d)[:3] == ['form', 'program', 'contrasts'] and list(d)[3:] == sorted(keys) and not text.endswith('\n'), '書式の JSON と形が違う'
    assert set(signs.values()) == {T['seal_format']['sign_values'][0]} and s4 == T['seal_format']['sign_values'][2]
    rec = seal_record(T, signs, s4, 'x.json', 'AB' * 32, '情報状態', '順の注', '起草者')
    assert set(T['seal_format']['record_keys']) <= set(rec)
    # 恒真にしない: 「予想しない」の向き・選択肢の外の値・鍵の欠け・予想者の取り違えは止まる
    for mut in ('np', 'bad', 'miss', 'who'):
        c2 = dict(ch)
        if mut == 'np':
            c2[F['direction']['key_prefix'] + T['families']['B_sub']['contrasts'][0]['id']] = P['not_predicted']
        elif mut == 'bad':
            c2[F['s4']['key']] = '下がる'
        elif mut == 'miss':
            c2.pop(F['gate1']['key'])
        else:
            c2[F['who']['key']] = '登録者'
        try:
            build(T, c2)
            raise AssertionError('止まらなかった: %s' % mut)
        except SystemExit:
            pass
    # ---- 封印した予想の照合（v2）: 健全な置き場で零件、壊した置き場で**その検査の一件だけ**が止まる ----
    tmp = tempfile.mkdtemp(prefix='sealB_')
    SV = T['seal_format']['sign_values']
    a0 = T['families']['B_add']['contrasts'][0]['id']
    dk = F['direction']['key_prefix'] + a0
    REGF = 'predictions-registrant-B-2026-01-01.json'
    SRF = 'sealing-record-B-2026-01-01.md'
    try:
        pd, seal, ssha, rsha = _fixture(T, os.path.join(tmp, 'ok'))
        pr, info = check_predictions(T, pd, seal, ssha)
        assert pr == [], ('健全な置き場で止まった', pr)
        assert set(info) >= {'registrant', 'coordinator', 'sealing_record'} and info['registrant']['not_predicted'] == 0
        # (名, 置き場を壊す関数〔pd, 封印, 登録者の SHA〕, 登録者の値を壊す関数, 登録者のバイトを壊す関数, 渡す封印の SHA を替えるか, 止まってほしい文の断片)
        cases = [
            ('封印の出所の SHA-256 を替える', lambda pd, s, r: s['source'].__setitem__('sha256', 'EF' * 32), None, None, False, '封印の出所の SHA-256'),
            ('封印の向きを一つ替える', lambda pd, s, r: s['signs'].__setitem__(a0, SV[1]), None, None, False, '封印の予想符号'),
            ('封印の S4 を替える', lambda pd, s, r: s.__setitem__('s4', SV[0]), None, None, False, '封印の S4'),
            ('封印の出所の名を替える', lambda pd, s, r: s['source'].__setitem__('predictions', 'records/predictions/other.json'), None, None, False, '封印の出所が'),
            ('登録者の予想のファイルが無い', lambda pd, s, r: os.remove(os.path.join(pd, REGF)), None, None, False, '予想の JSON が無い'),
            ('登録者の予想のファイルが二つある', lambda pd, s, r: shutil.copy(os.path.join(pd, REGF), os.path.join(pd, REGF.replace('.json', '-v2.json'))),
             None, None, False, '複数ある'),
            ('封印の経緯の記録が無い', lambda pd, s, r: os.remove(os.path.join(pd, SRF)), None, None, False, '封印の経緯の記録が無い'),
            ('封印の経緯の記録の登録者の SHA が違う', lambda pd, s, r: _replace_in(os.path.join(pd, SRF), r, 'AB' * 32), None, None, False, '登録者の SHA-256 が無い'),
            ('封印の経緯の記録に封印の SHA が無い', None, None, None, True, '起草者の封印の SHA-256 が無い'),
            ('登録者のファイルの予想者がコーディネータ', None, lambda rg: rg.__setitem__(F['who']['key'], 'コーディネータ'), None, False, '名の役と合わない'),
            ('登録者の予想に選択肢の外の値', None, lambda rg: rg.__setitem__(dk, '下がる'), None, False, '選択肢の外の値'),
            ('登録者の予想の欄が一つ欠ける', None, lambda rg: rg.pop(F['gate1']['key']), None, False, '欄の鍵が書式と違う'),
            ('登録者の予想の様式の名が違う', None, None, lambda b: b.replace(FORM.meta(T)['form'].encode('utf-8'), b'predictions-form v0.8 (B)'), False, 'form が書式と違う'),
        ]
        for i, (name, fn, rmut, bmut, other_ssha, expect) in enumerate(cases):
            pd, seal, ssha, rsha = _fixture(T, os.path.join(tmp, 'm%02d' % i), reg_mut=rmut, reg_bytes_mut=bmut)
            if fn:
                fn(pd, seal, rsha)
            pr, _ = check_predictions(T, pd, seal, 'CD' * 32 if other_ssha else ssha)
            assert pr, '止まらなかった: %s' % name
            assert len(pr) == 1 and expect in pr[0], ('見てほしい検査だけが止まるはずが違う: %s' % name, pr)
        n_cases = len(cases)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('[seal_B selftest] 書式と同じ鍵と選択肢・書式の JSON と同じ形・封印の欄・「予想しない」と選択肢の外と欠けと予想者の取り違えを止める・'
          '封印した予想の照合（健全な置き場で零件・壊した置き場 %d 通りすべてで止まる）: 通った' % n_cases)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--choices', default=None, help='選んだ値の JSON（欄の鍵 → 値・info.* と free と date と who を含む）')
    ap.add_argument('--date', default=None)
    ap.add_argument('--information-state', default=None)
    ap.add_argument('--order-note', default=None)
    ap.add_argument('--check', action='store_true', help='封印した予想の照合だけをする（records/predictions と records/B/seal-B.json）')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    T = runs_B.load_T()
    if a.check:
        sp = os.path.join(REPO, 'records', 'B', 'seal-B.json')
        seal = runs_B.read_json(sp) if os.path.exists(sp) else None
        pr, info = check_predictions(T, os.path.join(REPO, *PRED_REL.split('/')), seal, _sha(open(sp, 'rb').read()) if seal else None)
        print(json.dumps(info, ensure_ascii=False, indent=1))
        for x in pr:
            print('  - ' + x)
        print('[seal_B check] 止めるもの %d 件' % len(pr))
        sys.exit(1 if pr else 0)
    ch = json.load(open(a.choices, encoding='utf-8'))
    text, signs, s4 = build(T, ch)
    pred_rel = '%s/predictions-coordinator-B-%s.json' % (PRED_REL, a.date)
    seal_rel = 'records/B/seal-B.json'
    for rel in (pred_rel, seal_rel):
        if os.path.exists(os.path.join(REPO, *rel.split('/'))):
            sys.exit('既にある（封印は一度だけ）: %s' % rel)
    b = text.encode('utf-8')
    open(os.path.join(REPO, *pred_rel.split('/')), 'wb').write(b)
    pred_sha = _sha(b)
    rec = seal_record(T, signs, s4, pred_rel, pred_sha, a.information_state or '', a.order_note or '', '起草者（コーディネータ・南無弥勒如来・Claude Opus 5）')
    sb = (json.dumps(rec, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    open(os.path.join(REPO, *seal_rel.split('/')), 'wb').write(sb)
    print('[seal_B] %s（SHA-256 %s）' % (pred_rel, pred_sha))
    print('[seal_B] %s（SHA-256 %s）' % (seal_rel, _sha(sb)))
