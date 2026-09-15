# -*- coding: utf-8 -*-
"""compare_predictions_A.py v1 —— 段階 A の封印予想（様式 v0.8・登録者とコーディネータの各 JSON）と集計器の出力（analyze_A の JSON）を、
正本 `design/contrasts-A.json` の `predictions.compare_rules` で照合する（2026-09-15・登録者裁定 D47）。
照合の規則（正本の文言を本器で実装・結果を見てから変えない）:
- 向き（a.dir.<対比の id>）: 札が confirm_rule.labels.confirmed で β₃ の推定値（result.beta）が正なら選択肢の二つ目、負なら三つ目。札が confirm_rule.labels.ns なら四つ目。ほかの札は照合不能。
- 床持続（a.floor.<セルの id>）: 集計器の floor の flag が立てば選択肢の二つ目、立たなければ三つ目。セルが無ければ照合不能。
- 全体: 確証の本数（label_counts.confirmed）と測れた効果種の数（measurable.types の measurable が真の数）を edges の帯に写す。計算の記録が無ければ照合不能。
- 「予想しない」は照合せず、件数を別に数える。予想の欄が欠けた JSON・選択肢の外の値・予想者の外・様式の名の違いは照合せずに止める。
柵: 的中は独立の確認ではなく、誰の判断の重みも変えない。照合は記録であり評価ではない。封印予想を事後の向きや読みの根拠に引かない。
用法: python tools/compare_predictions_A.py --pred <JSON> [--pred <JSON> ...] --analysis <analyze_A の JSON> [--out records/A/predictions-check-A] [--force]
      python tools/compare_predictions_A.py --selftest
出力: <out>.md と <out>.json（summary に予想ごとの SHA-256・予想者・種別ごとの件数・報告の §7 に機械で転記）。既存は --force が無ければ上書きしない。
本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
FORM_NAME = 'predictions-form v0.8 (A)'
KINDS = ('向き', '床持続', '全体')
RES = ('的中', '外れ', '照合不能', '予想しない')
CLAUSE = '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


class PredError(ValueError):
    pass


def expected_fields(T):
    P = T['predictions']; F = P['fields']; out = collections.OrderedDict()
    for c in T['families']['A_slope']['contrasts']:
        out[F['direction']['key_prefix'] + c['id']] = ('向き', c['id'], F['direction']['options'])
    for c in T['descriptive_families']['A_desc_floor']['cells']:
        out[F['floor']['key_prefix'] + c['id']] = ('床持続', c['id'], F['floor']['options'])
    for nm in ('confirmed_band', 'measurable_band'):
        out[F[nm]['key']] = ('全体', nm, F[nm]['options'])
    assert len(out) == P['n_prediction_fields'], (len(out), P['n_prediction_fields'])
    return out


def band_of(v, edges, options):
    for i, (lo, hi) in enumerate(edges):
        if lo <= v <= hi:
            return options[i + 1]
    raise PredError('帯の外の値 %r' % (v,))


def actuals(T, AN):
    """集計器の出力から、欄ごとの実測の選択肢（照合不能は None）と短い記述を組む。"""
    P = T['predictions']; F = P['fields']; L = T['families']['A_slope']['confirm_rule']['labels']; act = {}
    byid = {c['id']: c for c in (AN.get('contrasts') or [])}
    for c in T['families']['A_slope']['contrasts']:
        k = F['direction']['key_prefix'] + c['id']; x = byid.get(c['id'])
        if x is None:
            act[k] = (None, '集計に無い'); continue
        lab = x.get('label'); beta = (x.get('result') or {}).get('beta')
        if lab == L['confirmed'] and isinstance(beta, (int, float)) and beta != 0:
            act[k] = (F['direction']['options'][1 if beta > 0 else 2], '%s・β₃ %+.4f' % (lab, beta))
        elif lab == L['ns']:
            act[k] = (F['direction']['options'][3], lab)
        else:
            act[k] = (None, str(lab))
    fl = {r['id']: r for r in (AN.get('floor') or [])}
    for c in T['descriptive_families']['A_desc_floor']['cells']:
        k = F['floor']['key_prefix'] + c['id']; r = fl.get(c['id'])
        if r is None or r.get('flag') not in (0, 1):
            act[k] = (None, '集計に無い'); continue
        act[k] = (F['floor']['options'][1 if r['flag'] == 1 else 2], '0/1 %d' % r['flag'])
    k = F['confirmed_band']['key']; n_conf = (AN.get('label_counts') or {}).get('confirmed')
    act[k] = (band_of(n_conf, F['confirmed_band']['edges'], F['confirmed_band']['options']), '確証 %d 本' % n_conf) if isinstance(n_conf, int) and not isinstance(n_conf, bool) else (None, '集計に無い')
    k = F['measurable_band']['key']; types = (AN.get('measurable') or {}).get('types')
    if isinstance(types, dict) and types:
        n_meas = sum(1 for v in types.values() if v.get('measurable') is True)
        act[k] = (band_of(n_meas, F['measurable_band']['edges'], F['measurable_band']['options']), '測れた効果種 %d 種' % n_meas)
    else:
        act[k] = (None, '計算の記録が無い')
    return act


def validate(T, PJ):
    EXP = expected_fields(T); F = T['predictions']['fields']
    miss = [k for k in EXP if k not in PJ]; bad = [(k, PJ[k]) for k in EXP if k in PJ and PJ[k] not in EXP[k][2]]; who = PJ.get('who')
    if miss or bad or who not in F['who']['options'] or PJ.get('form') != FORM_NAME:
        raise PredError('照合せずに止める: 欠け %d（%s）・選択肢の外 %d（%s）・予想者 %r・様式の名 %r' % (len(miss), '・'.join(miss[:5]), len(bad), '・'.join('%s=%s' % b for b in bad[:5]), who, PJ.get('form')))
    return EXP


def compare_one(T, AN, PJ):
    EXP = validate(T, PJ); ACT = actuals(T, AN); NOTP = T['predictions']['not_predicted']
    C = {kd: collections.Counter() for kd in KINDS}; det = []
    for k, (kd, ident, opts) in EXP.items():
        v = PJ[k]; a_, note = ACT[k]
        res = '予想しない' if v == NOTP else ('照合不能' if a_ is None else ('的中' if v == a_ else '外れ'))
        C[kd][res] += 1; det.append({'kind': kd, 'key': k, 'pred': v, 'actual': a_, 'note': note, 'result': res})
    return C, det


def rel(p):
    ap_ = os.path.abspath(p)
    return os.path.relpath(ap_, REPO).replace('\\', '/') if os.path.commonpath([ap_, REPO]) == REPO else ap_.replace('\\', '/')


def selftest():
    T = runs_A.load_T(); P = T['predictions']; F = P['fields']; L = T['families']['A_slope']['confirm_rule']['labels']; NOTP = P['not_predicted']
    CON = T['families']['A_slope']['contrasts']; CELLS = T['descriptive_families']['A_desc_floor']['cells']; n, nc = len(CON), len(CELLS)
    assert n % 5 == 0 and nc >= 3, (n, nc)
    cons = []
    for i, c in enumerate(CON):
        kind = i % 5
        cons.append({'id': c['id'], 'label': {0: L['confirmed'], 1: L['confirmed'], 2: L['ns'], 3: L['clause'], 4: L['undecidable']}[kind], 'result': ({'beta': {0: 0.5, 1: -0.5, 2: 0.1, 3: 0.2}[kind]} if kind != 4 else None)})
    n_conf = sum(1 for i in range(n) if i % 5 in (0, 1))
    floor = [{'id': c['id'], 'flag': 1 if i % 2 == 0 else 0} for i, c in enumerate(CELLS)][:-1]   # 最後のセルを落とす
    types = {t: {'measurable': j < 3} for j, t in enumerate(T['families']['A_slope']['effect_type_ids'])}
    AN = {'contrasts': cons, 'floor': floor, 'label_counts': {'confirmed': n_conf}, 'measurable': {'types': types}}
    DO = F['direction']['options']; FO = F['floor']['options']; CB = F['confirmed_band']; MB = F['measurable_band']
    PJ = {'form': FORM_NAME, 'program': 'ontology-preamble-4b/A', 'who': F['who']['options'][0], 'date': '2026-09-15', 'info.coi': 'selftest', 'free': ''}
    for i, c in enumerate(CON):
        PJ[F['direction']['key_prefix'] + c['id']] = {0: DO[1], 1: DO[1], 2: DO[3], 3: DO[1], 4: NOTP}[i % 5]
    for c in CELLS:
        PJ[F['floor']['key_prefix'] + c['id']] = FO[1]
    conf_i = next(i for i, (lo, hi) in enumerate(CB['edges']) if lo <= n_conf <= hi); meas_i = next(i for i, (lo, hi) in enumerate(MB['edges']) if lo <= 3 <= hi)
    PJ[CB['key']] = CB['options'][conf_i + 1]; PJ[MB['key']] = MB['options'][(meas_i + 1) % len(MB['edges']) + 1]
    C, det = compare_one(T, AN, PJ); k5 = n // 5
    exp = {'向き': {'的中': 2 * k5, '外れ': k5, '照合不能': k5, '予想しない': k5},
           '床持続': {'的中': sum(1 for i in range(nc - 1) if i % 2 == 0), '外れ': sum(1 for i in range(nc - 1) if i % 2 == 1), '照合不能': 1, '予想しない': 0},
           '全体': {'的中': 1, '外れ': 1, '照合不能': 0, '予想しない': 0}}
    got = {kd: {r: C[kd][r] for r in RES} for kd in KINDS}
    assert got == exp, (got, exp)

    def raises(pj, an=AN):
        try:
            compare_one(T, an, pj)
        except PredError:
            return True
        return False
    pj = dict(PJ); pj.pop(F['direction']['key_prefix'] + CON[0]['id']); assert raises(pj), '欠けで止まらない'
    pj = dict(PJ); pj[F['floor']['key_prefix'] + CELLS[0]['id']] = '選択肢の外'; assert raises(pj), '選択肢の外で止まらない'
    pj = dict(PJ); pj['who'] = '第三者'; assert raises(pj), '予想者の外で止まらない'
    pj = dict(PJ); pj['form'] = 'predictions-form v0.7 (F)'; assert raises(pj), '様式の名の違いで止まらない'
    EXP = expected_fields(T); pj = {k: (NOTP if k in EXP else v) for k, v in PJ.items()}; C2, _ = compare_one(T, AN, pj)
    assert {kd: C2[kd]['予想しない'] for kd in KINDS} == {'向き': n, '床持続': nc, '全体': 2} and all(C2[kd][r] == 0 for kd in KINDS for r in RES if r != '予想しない'), C2
    for B_ in (CB, MB):
        E, O = B_['edges'], B_['options']
        assert all(band_of(lo, E, O) == O[i + 1] and band_of(hi, E, O) == O[i + 1] for i, (lo, hi) in enumerate(E)), E
        for v in (E[0][0] - 1, E[-1][1] + 1):
            try:
                band_of(v, E, O); raise AssertionError('帯の外で止まらない %r' % v)
            except PredError:
                pass
    AN2 = dict(AN); AN2['measurable'] = {}; C3, _ = compare_one(T, AN2, PJ); assert C3['全体']['照合不能'] == 1 and C3['全体']['的中'] == 1, C3
    print('SELFTEST PASS（compare_predictions_A %s: 向き・床持続・全体の件数・欠け・選択肢の外・予想者・様式の名・すべて予想しない・帯の端・計算の記録の欠け）' % VERSION)
    return 0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--pred', action='append', default=[]); ap.add_argument('--analysis'); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'predictions-check-A'))
    ap.add_argument('--force', action='store_true'); ap.add_argument('--selftest', action='store_true'); ap.add_argument('--contrasts', default=None)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.pred or not a.analysis:
        sys.exit('--pred（一つ以上）と --analysis が要る')
    if not a.force and (os.path.exists(a.out + '.md') or os.path.exists(a.out + '.json')):
        sys.exit('既存の照合の記録があるので上書きしない（--force）: %s' % a.out)
    T = runs_A.load_T(a.contrasts); P = T['predictions']; AN = runs_A.read_json(a.analysis); summary, detail = {}, {}
    for p in a.pred:
        b = open(p, 'rb').read(); sha = hashlib.sha256(b).hexdigest().upper(); PJ = json.loads(b.decode('utf-8')); name = os.path.basename(p)
        try:
            C, det = compare_one(T, AN, PJ)
        except PredError as ex:
            sys.exit('[compare_predictions_A] %s: %s' % (name, ex))
        summary[name] = {'file': rel(p), 'sha256': sha, 'who': PJ.get('who'), 'date': PJ.get('date'), 'coi': PJ.get('info.coi'), 'counts': {kd: {r: C[kd][r] for r in RES} for kd in KINDS}}
        detail[name] = det
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
    OUT = {'kind': 'predictions_check_A', 'version': VERSION, 'generated_utc': now, 'analysis': rel(a.analysis), 'analysis_sha16': runs_A.sha16_file(a.analysis), 'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH),
           'rules': P['compare_rules'], 'fence': P['fence'], 'summary': summary, 'detail': detail, 'clause': CLAUSE}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out + '.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(OUT, ensure_ascii=False, indent=1) + '\n')
    M = ['# 段階 A 封印予想の照合（機械生成・`tools/compare_predictions_A.py` %s・%s UTC）' % (VERSION, now), '',
         '- 集計: `%s`（SHA16 %s）・正本 SHA16 %s・照合の規則は正本 `predictions.compare_rules`（本器の冒頭に実装）' % (OUT['analysis'], OUT['analysis_sha16'], OUT['contrasts_sha16']),
         '- **柵**: %s。' % P['fence'], '']
    for name, s in summary.items():
        M += ['## %s（予想者 %s・SHA-256 %s）' % (name, s['who'], s['sha256']), '', '| 種別 | %s |' % ' | '.join(RES), '|---|---|---|---|---|']
        M += ['| %s | %s |' % (kd, ' | '.join(str(s['counts'][kd][r]) for r in RES)) for kd in KINDS]
        rows = [d for d in detail[name] if d['result'] in ('外れ', '照合不能')]
        M += ['', '| 種別 | 欄 | 予想 | 実測 | 結果 |', '|---|---|---|---|---|'] + ['| %s | %s | %s | %s（%s） | %s |' % (d['kind'], d['key'], d['pred'], d['actual'] or '—', d['note'], d['result']) for d in rows] + ['']
    M += [CLAUSE]
    open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
    print('[compare_predictions_A %s] written %s.{md,json} | %s' % (VERSION, a.out, json.dumps({nm: s['counts'] for nm, s in summary.items()}, ensure_ascii=False)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
