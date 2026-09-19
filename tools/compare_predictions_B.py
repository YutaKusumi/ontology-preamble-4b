# -*- coding: utf-8 -*-
"""compare_predictions_B.py v1 —— 段階 B の**封印した予想の照合**（登録者とコーディネータ・正本 `predictions.compare_rules`・登録者裁定 D148）。

結果（門の記録と集計の記録）と、封印した二人の予想（`records/predictions/predictions-{registrant,coordinator}-B-<日付>.json`）を照らし、
予想者ごとに、種別（向き・S4・全体）ごとの**的中・外れ・照合不能・予想しない**の件数と、外れと照合不能の一覧を書く。
- 向き: 集計の札が「確証」「確証（登録された向きと逆）」なら、**札の向き**（集計の `sign`・正本 `seal_format.sign_map` の逆引き）で低下・上昇に写す
  （起草者の封印の向きは使わない）。「非有意」は「どちらでもない」。判定不能・判定保留（門で記述に降ろした対比）・表に載らない対比は照合不能。
- S4: S4 の札（集計の `s4.verdict`）を、正本の対応表 `B_desc_S4.seal_match.table` で予想の値と照らす（`rules_B.s4_seal_match`・封印の照合と同じ関数）。
  表に無い札（門・当否を言わない・余地の条項・測れなかった）は照合不能。
- 全体: 確証の札（逆向きを含む）の本数を `confirmed_band.edges` の帯に写して照らす（帯の名は書式と同じ作り方）。門1 は門の記録の開閉と照らす。
- 門1 が閉じた回（と、門の判定が escalate で集計の記録が無い回）は、確証の族と S4 が走らないので、向き・S4・本数を照合不能にし、門1 だけを照らす。
  門の記録が incomplete の回は照合しない（揃えてから照らす）。
- 「予想しない」は照合せず、件数を別に数える。
- 予想の JSON は照合の前に `seal_B.check_predictions` で照らし（欄の欠け・選択肢の外・予想者・様式の名・封印の出所・封印の経緯の記録の SHA-256）、外れたら照合せずに止める。
- 集計の記録は、渡された門の記録から作ったもの（`gate_sha16`）でなければ止める。合成データの印があれば、検査用の口（--allow-dry）でなければ止める。
v1（2026-09-19 の夜・封印の後・**結果の前**・独立の目を通っていない）。上の写し方のうち、正本に書かれていなかった所（門1 が閉じた回・判定保留の扱い・逆向きの確証の向き）は
起草者の解釈で、正本 `predictions.compare_rules.interpretation` に置いた（登録者の確認を待つ）。
出力: records/B/predictions-check-B.md と同 .json（--out で変える・--force が無ければ上書きしない）。要約は報告の組み立て器が区画 L に機械で写す。
用法: python tools/compare_predictions_B.py --gate records/B/gate-B-<日付>.json [--analysis records/B/analysis-B-<日付>.json] [--force] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
的中は独立の確認ではなく、誰の判断の重みも変えない（正本 `predictions.fence`）。
"""
import os, sys, json, shutil, hashlib, argparse, datetime, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B
import rules_B
import seal_B

VERSION = 'v1'
REPO = runs_B.REPO
V_HIT, V_MISS, V_NA, V_NP = '的中', '外れ', '照合不能', '予想しない'
VERDICTS = (V_HIT, V_MISS, V_NA, V_NP)
KINDS = ('向き', 'S4', '全体')


def conf_ids(T):
    return [c['id'] for Fm in T['families'].values() for c in Fm['contrasts']]


def band_label(T, n):
    """確証の本数を帯の名に写す（書式 `make_predictions_form_B` と同じ作り方）。"""
    CB = T['predictions']['fields']['confirmed_band']
    for lo, hi in CB['edges']:
        if lo <= n <= hi:
            return ('%d %s' % (lo, CB['unit'])) if lo == hi else ('%d〜%d %s' % (lo, hi, CB['unit']))
    return None


def observed(T, gate, analysis):
    """結果の側の値を作る。値が None の欄は照合不能で、理由を添える。"""
    inv = {v: k for k, v in T['seal_format']['sign_map'].items()}          # 集計の記号 → 正本の語彙（下 → 低下）
    obs = {'gate1': ('開く' if gate['gate1']['open'] else '閉じる', '門の記録（gate1.open）')}
    if analysis is None:
        why = ('門1 が閉じた（確証の族と S4 は走らない）' if not gate['gate1']['open']
               else '集計の記録が無い（門の判定 %s）' % gate.get('verdict'))
        obs['dir'] = {cid: (None, why) for cid in conf_ids(T)}
        obs['s4'] = (None, why)
        obs['band'] = (None, why)
        obs['n_confirmed'] = None
        return obs
    rows = {r['id']: r for r in analysis['confirm']}
    d = {}
    for cid in conf_ids(T):
        r = rows.get(cid)
        lab = str((r or {}).get('label') or '')
        if r is None:
            d[cid] = (None, '集計に行が無い')
        elif lab.startswith('確証'):
            v = inv.get(r.get('sign'))
            d[cid] = (v, lab) if v in ('低下', '上昇') else (None, '%s（向きが %s）' % (lab, r.get('sign')))
        elif lab == '非有意':
            d[cid] = ('どちらでもない', lab)
        else:
            d[cid] = (None, lab or '札が無い')
    obs['dir'] = d
    obs['s4'] = ((analysis.get('s4') or {}).get('verdict'), 'S4 の札')
    n = sum(1 for r in analysis['confirm'] if str(r.get('label') or '').startswith('確証'))
    obs['n_confirmed'] = n
    obs['band'] = (band_label(T, n), '確証の札 %d 本（逆向きを含む）' % n)
    return obs


def compare_one(T, pred, obs):
    """一人の予想を結果と照らす。戻り値: {'rows': [...], 'counts': {種別: {判定: 件数}}}"""
    P = T['predictions']
    F = P['fields']
    NP = P['not_predicted']
    rows = []

    def add(kind, key, want, got, basis, verdict):
        rows.append({'kind': kind, 'key': key, 'predicted': want, 'observed': got, 'basis': basis, 'verdict': verdict})

    for cid in conf_ids(T):
        want = pred[F['direction']['key_prefix'] + cid]
        got, why = obs['dir'][cid]
        if want == NP:
            v = V_NP
        elif got is None:
            v = V_NA
        else:
            v = V_HIT if want == got else V_MISS
        add('向き', cid, want, got, why, v)
    want = pred[F['s4']['key']]
    outcome, why = obs['s4']
    if want == NP:
        v, m = V_NP, None
    elif outcome is None:
        v, m = V_NA, None
    else:
        m = rules_B.s4_seal_match(outcome, want, T)
        v = {'当たり': V_HIT, '外れ': V_MISS}.get(m, V_NA)
    add('S4', F['s4']['key'], want, outcome, why + ('' if m is None else '・対応表で「%s」' % m), v)
    for key, (got, why) in ((F['confirmed_band']['key'], obs['band']), (F['gate1']['key'], obs['gate1'])):
        want = pred[key]
        if want == NP:
            v = V_NP
        elif got is None:
            v = V_NA
        else:
            v = V_HIT if want == got else V_MISS
        add('全体', key, want, got, why, v)
    counts = {k: {x: 0 for x in VERDICTS} for k in KINDS}
    for r in rows:
        counts[r['kind']][r['verdict']] += 1
    return {'rows': rows, 'counts': counts}


def run_compare(T, gate_path, analysis_path, pred_dir, seal_path, allow_dry=False):
    """門の記録・集計の記録・封印した予想を読み、照合の記録（dict）を返す。止める条件に当たれば SystemExit。"""
    G = runs_B.read_json(gate_path)
    if G.get('kind') != 'gate_B':
        raise SystemExit('門の記録の種類が違う: %s' % G.get('kind'))
    if G.get('verdict') == 'incomplete':
        raise SystemExit('門の記録が incomplete——記録を揃えてから照合する（正本 predictions.compare_rules.interpretation）')
    A = runs_B.read_json(analysis_path) if analysis_path else None
    if A is not None:
        if A.get('kind') != 'analyze_B':
            raise SystemExit('集計の記録の種類が違う: %s' % A.get('kind'))
        if A.get('gate_sha16') != runs_B.sha16_file(gate_path):
            raise SystemExit('集計が読んだ門の記録（SHA16 %s）と、渡された門の記録（SHA16 %s）が違う——同じ門の記録で照らす'
                             % (A.get('gate_sha16'), runs_B.sha16_file(gate_path)))
        if not G['gate1']['open']:
            raise SystemExit('門1 が閉じた門の記録に、集計の記録が渡された（取り違え）')
        got = sorted(str(r.get('id')) for r in A.get('confirm') or [])
        if got != sorted(conf_ids(T)):
            raise SystemExit('集計の確証の対比が正本と違う（欠け %d・余り %d）' % (len(set(conf_ids(T)) - set(got)), len(set(got) - set(conf_ids(T)))))
    elif G.get('verdict') == 'open':
        raise SystemExit('門が開いているのに、集計の記録が渡されていない')
    dry = list(G.get('dry_marks') or []) + list((A or {}).get('dry_marks') or [])
    if dry and not allow_dry:
        raise SystemExit('合成データ（dry-run の印つき）の記録を照らそうとしている: %s。検査用は --allow-dry' % '・'.join(map(str, dry)))
    seal = runs_B.read_json(seal_path)
    seal_sha = hashlib.sha256(open(seal_path, 'rb').read()).hexdigest().upper()
    probs, info = seal_B.check_predictions(T, pred_dir, seal, seal_sha)
    if probs:
        raise SystemExit('封印した予想の照らしで止まった（照合しない・predictions.compare_rules.validation）:\n  - ' + '\n  - '.join(probs))
    obs = observed(T, G, A)
    res = {}
    for role, who in seal_B.ROLES.items():
        pred = json.load(open(os.path.join(pred_dir, os.path.basename(info[role]['path'])), encoding='utf-8'))
        res[who] = dict(compare_one(T, pred, obs), file=info[role])
    rel = lambda p: os.path.relpath(p, REPO).replace('\\', '/') if os.path.abspath(p).startswith(REPO) else os.path.basename(p)
    return {'kind': 'compare_predictions_B', 'version': VERSION,
            'gate': {'path': rel(gate_path), 'sha16': runs_B.sha16_file(gate_path), 'verdict': G.get('verdict'), 'gate1_open': G['gate1']['open']},
            'analysis': (None if A is None else {'path': rel(analysis_path), 'sha16': runs_B.sha16_file(analysis_path)}),
            'seal': {'path': rel(seal_path), 'sha256': seal_sha}, 'sealing_record': info.get('sealing_record'),
            'order_note': seal.get('order_note') or '', 'n_confirmed': obs['n_confirmed'], 'results': res,
            'dry_marks': dry, 'fence': T['predictions']['fence']}


def summary_line(who, R):
    c = R['counts']
    part = lambda k: '的中 %d・外れ %d・照合不能 %d・予想しない %d' % tuple(c[k][x] for x in VERDICTS)
    return '%s: 向き（%s）／S4（%s）／全体（%s）' % (who, part('向き'), part('S4'), part('全体'))


def write_outputs(REC, out_md, T):
    out_json = os.path.splitext(out_md)[0] + '.json'
    now = datetime.datetime.now(datetime.timezone.utc)
    REC = dict(REC, generated_utc=now.strftime('%Y-%m-%dT%H:%M:%SZ'))
    json.dump(REC, open(out_json, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    mark = '【合成データ・本番ではない】' if REC['dry_marks'] else ''
    L = ['# 段階 B 封印した予想の照合（機械生成・`tools/compare_predictions_B.py` %s・%s UTC）%s' % (VERSION, now.strftime('%Y-%m-%d %H:%M'), mark), '',
         '- 門の記録 `%s`（SHA16 %s・判定 %s）・集計の記録 %s・起草者の封印 `%s`（SHA-256 `%s`）。'
         % (REC['gate']['path'], REC['gate']['sha16'], REC['gate']['verdict'],
            ('`%s`（SHA16 %s）' % (REC['analysis']['path'], REC['analysis']['sha16'])) if REC['analysis'] else '無し（門1 が閉じた・または集計が無い）',
            REC['seal']['path'], REC['seal']['sha256']),
         '- 照合の規則: 正本 `predictions.compare_rules`（写し方の解釈は `predictions.compare_rules.interpretation`）。',
         '- **%s**' % REC['fence'], '']
    if REC['order_note']:
        L += ['- **予想の独立（封印の順の注）**: %s' % REC['order_note'], '']
    L += ['## 要約', '', '| 予想者 | 予想のファイル | 種別 | 的中 | 外れ | 照合不能 | 予想しない |', '|---|---|---|---|---|---|---|']
    for who, R in REC['results'].items():
        for k in KINDS:
            L.append('| %s | `%s` | %s | %s |' % (who, R['file']['path'], k, ' | '.join(str(R['counts'][k][x]) for x in VERDICTS)))
    for who, R in REC['results'].items():
        L += ['', '## %s——外れと照合不能' % who, '', '| 種別 | 欄 | 予想 | 結果 | 拠りどころ | 判定 |', '|---|---|---|---|---|---|']
        for r in R['rows']:
            if r['verdict'] in (V_MISS, V_NA):
                L.append('| %s | %s | %s | %s | %s | %s |' % (r['kind'], r['key'], r['predicted'], r['observed'] if r['observed'] is not None else '—', r['basis'], r['verdict']))
    L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
    return out_json


# ---------------------------------------------------------------- 自己検査 ----
def _gate(open_=True, verdict='open', dry=None):
    return {'kind': 'gate_B', 'verdict': verdict, 'gate1': {'open': open_}, 'dry_marks': dry or []}


def _analysis(T, labels, s4_verdict, gate_sha16, dry=None):
    rows = []
    for cid in conf_ids(T):
        lab, sign = labels.get(cid, ('非有意', '零'))
        rows.append({'id': cid, 'label': lab, 'sign': sign})
    return {'kind': 'analyze_B', 'gate_sha16': gate_sha16, 'confirm': rows, 's4': {'verdict': s4_verdict}, 'dry_marks': dry or []}


def _selftest():
    T = runs_B.load_T()
    P = T['predictions']
    F = P['fields']
    NP = P['not_predicted']
    ids = conf_ids(T)
    L3 = T['descriptive_families']['B_desc_S4']['three_way']['labels']
    # ---- 帯の写し方（境目） ----
    for n, want in ((0, '0 本'), (1, '1〜3 本'), (3, '1〜3 本'), (4, '4〜8 本'), (8, '4〜8 本'), (9, '9〜16 本'), (len(ids), '9〜16 本')):
        assert band_label(T, n) == want.replace(' 本', ' ' + F['confirmed_band']['unit']), ('帯の写し方', n, band_label(T, n))
    # ---- 向き・S4・全体の写し方（関数の水準） ----
    labels = {ids[0]: ('確証', '下'), ids[1]: ('確証', '下'), ids[2]: ('確証（登録された向きと逆）', '上'), ids[3]: ('非有意', '下'),
              ids[4]: ('非有意', '上'), ids[5]: ('判定保留（様式転位）', '下'), ids[6]: ('判定不能（検閲）', '零'), ids[7]: ('判定保留（書式外転位）', '上')}
    gate = _gate()
    A = _analysis(T, labels, '10 pt 以上の低下は否定', 'X')
    obs = observed(T, gate, A)
    pred = {F['direction']['key_prefix'] + c: 'どちらでもない' for c in ids}
    pred.update({F['direction']['key_prefix'] + ids[0]: '低下', F['direction']['key_prefix'] + ids[1]: '上昇',
                 F['direction']['key_prefix'] + ids[2]: '上昇', F['direction']['key_prefix'] + ids[3]: 'どちらでもない',
                 F['direction']['key_prefix'] + ids[4]: '低下', F['direction']['key_prefix'] + ids[5]: '低下',
                 F['direction']['key_prefix'] + ids[6]: 'どちらでもない', F['direction']['key_prefix'] + ids[8]: NP,
                 F['s4']['key']: 'どちらでもない', F['confirmed_band']['key']: band_label(T, 3), F['gate1']['key']: '閉じる'})
    R = compare_one(T, pred, obs)
    by = {r['key']: r['verdict'] for r in R['rows']}
    want = {ids[0]: V_HIT, ids[1]: V_MISS, ids[2]: V_HIT, ids[3]: V_HIT, ids[4]: V_MISS, ids[5]: V_NA, ids[6]: V_NA, ids[7]: V_NA, ids[8]: V_NP,
            F['s4']['key']: V_HIT, F['confirmed_band']['key']: V_HIT, F['gate1']['key']: V_MISS}
    bad = {k: (by[k], v) for k, v in want.items() if by[k] != v}
    assert not bad, ('写し方が違う（得た・望んだ）', bad)
    # 逆向きの確証は札の向きで写す（起草者の封印の向きを使わない）: 上 → 上昇
    assert obs['dir'][ids[2]][0] == '上昇' and obs['n_confirmed'] == 3
    c = R['counts']
    assert c['向き'][V_NP] == 1 and sum(c['向き'].values()) == len(ids) and sum(c['S4'].values()) == 1 and sum(c['全体'].values()) == 2
    # S4: 門の札は照合不能・表の外れ
    assert compare_one(T, dict(pred), observed(T, gate, _analysis(T, labels, '判定保留（書式外転位）', 'X')))['rows'][len(ids)]['verdict'] == V_NA
    p2 = dict(pred, **{F['s4']['key']: '上昇'})
    assert compare_one(T, p2, observed(T, gate, _analysis(T, labels, L3[0], 'X')))['rows'][len(ids)]['verdict'] in (V_MISS, V_HIT)
    assert compare_one(T, p2, observed(T, gate, _analysis(T, labels, '下がった', 'X')))['rows'][len(ids)]['verdict'] == V_MISS
    # 門1 が閉じた回: 向き・S4・本数は照合不能、門1 だけ照らす
    Rc = compare_one(T, pred, observed(T, _gate(open_=False, verdict='closed'), None))
    assert all(r['verdict'] in (V_NA, V_NP) for r in Rc['rows'] if r['key'] != F['gate1']['key']) and \
        [r['verdict'] for r in Rc['rows'] if r['key'] == F['gate1']['key']] == [V_HIT]
    # ---- ファイルの水準（封印した予想の照らし・門の記録の照合・合成データの印） ----
    tmp = tempfile.mkdtemp(prefix='cmpB_')
    try:
        root = os.path.join(tmp, 'ok')
        pd, seal, ssha, rsha = seal_B._fixture(T, root)
        sp = os.path.join(root, 'seal-B.json')
        json.dump(seal, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        _redo_record(pd, sp)
        gp, ap_ = os.path.join(root, 'gate.json'), os.path.join(root, 'analysis.json')
        json.dump(gate, open(gp, 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump(_analysis(T, labels, L3[0], runs_B.sha16_file(gp)), open(ap_, 'w', encoding='utf-8'), ensure_ascii=False)
        REC = run_compare(T, gp, ap_, pd, sp)
        assert set(REC['results']) == set(seal_B.ROLES.values()) and REC['n_confirmed'] == 3
        out = write_outputs(REC, os.path.join(root, 'check.md'), T)
        assert json.load(open(out, encoding='utf-8'))['kind'] == 'compare_predictions_B'
        stops = []
        # (a) 集計が別の門の記録から作られている（置き場は場合ごとに分ける——後の場合の準備で上書きしない）
        ap1 = os.path.join(root, 'analysis-other-gate.json')
        json.dump(_analysis(T, labels, L3[0], 'ABCDEF0123456789'), open(ap1, 'w', encoding='utf-8'), ensure_ascii=False)
        stops.append(('門の記録の食い違い', '渡された門の記録', lambda: run_compare(T, gp, ap1, pd, sp)))
        # (b) 門の記録が incomplete
        gp2 = os.path.join(root, 'gate-incomplete.json')
        json.dump(_gate(verdict='incomplete'), open(gp2, 'w', encoding='utf-8'), ensure_ascii=False)
        stops.append(('incomplete', 'incomplete', lambda: run_compare(T, gp2, None, pd, sp)))
        # (c) 合成データの印（検査用の口なし）
        gp3 = os.path.join(root, 'gate-dry.json')
        json.dump(_gate(dry=['dry']), open(gp3, 'w', encoding='utf-8'), ensure_ascii=False)
        ap3 = os.path.join(root, 'analysis-dry.json')
        json.dump(_analysis(T, labels, L3[0], runs_B.sha16_file(gp3), dry=['dry']), open(ap3, 'w', encoding='utf-8'), ensure_ascii=False)
        stops.append(('合成データの印', '合成データ', lambda: run_compare(T, gp3, ap3, pd, sp)))
        # (d) 門が開いているのに集計が無い
        stops.append(('集計の欠け', '集計の記録が渡されていない', lambda: run_compare(T, gp, None, pd, sp)))
        # (e) 封印した予想が照らせない（登録者の予想の欄が欠ける）
        root5 = os.path.join(tmp, 'bad')
        pd5, seal5, _, _ = seal_B._fixture(T, root5, reg_mut=lambda rg: rg.pop(F['gate1']['key']))
        sp5 = os.path.join(root5, 'seal-B.json')
        json.dump(seal5, open(sp5, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        _redo_record(pd5, sp5)
        stops.append(('予想の欄の欠け', '欄の鍵が書式と違う', lambda: run_compare(T, gp, ap_, pd5, sp5)))
        for name, frag, fn in stops:          # **止まった理由まで照らす**（別の理由で止まって通るのを防ぐ）
            try:
                fn()
                raise AssertionError('止まらなかった: %s' % name)
            except SystemExit as e:
                assert frag in str(e), ('別の理由で止まった: %s' % name, str(e)[:200])
        # 検査用の口なら合成データも通り、印が記録に残る
        assert run_compare(T, gp3, ap3, pd, sp, allow_dry=True)['dry_marks']
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('[compare_predictions_B selftest] 帯の境目・向き（確証・逆向きの確証・非有意・判定保留・判定不能・予想しない）・S4 の対応表・門1・'
          '門1 が閉じた回・止める五つ（門の記録の食い違い・incomplete・合成データの印・集計の欠け・予想の欄の欠け）: 通った')


def _redo_record(pd, seal_path):
    """自己検査の置き場の封印の経緯の記録を、ファイルに書いた封印の SHA-256 で書き直す（seal_B._fixture は封印を別の書き方で数えるため）。"""
    names = sorted(os.listdir(pd))
    sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()
    shas = [sha(os.path.join(pd, f)) for f in names if f.endswith('.json')] + [sha(seal_path)]
    rec = [f for f in names if f.startswith('sealing-record-B-')][0]
    open(os.path.join(pd, rec), 'w', encoding='utf-8').write(''.join('| %s |\n' % s for s in shas))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--gate', default=None)
    ap.add_argument('--analysis', default=None, help='集計の記録（門1 が閉じた回は無い）')
    ap.add_argument('--predictions-dir', default=os.path.join(REPO, 'records', 'predictions'))
    ap.add_argument('--seal', default=os.path.join(REPO, 'records', 'B', 'seal-B.json'))
    ap.add_argument('--out', default=os.path.join(REPO, 'records', 'B', 'predictions-check-B.md'))
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--allow-dry', action='store_true', help='検査用の口（合成データの記録を照らす・記録に印が残る）')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    if not a.gate:
        sys.exit('--gate が要る')
    for p in (a.out, os.path.splitext(a.out)[0] + '.json'):
        if os.path.exists(p) and not a.force:
            sys.exit('既にある（--force で上書き）: %s' % p)
    T = runs_B.load_T()
    REC = run_compare(T, a.gate, a.analysis, a.predictions_dir, a.seal, allow_dry=a.allow_dry)
    write_outputs(REC, a.out, T)
    for who, R in REC['results'].items():
        print('[compare_predictions_B] ' + summary_line(who, R))
    print('[compare_predictions_B] %s' % a.out)
