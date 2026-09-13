# -*- coding: utf-8 -*-
"""analyze_A.py v1 —— 段階 A の集計器（2026-09-13・登録者裁定 D9 の三つ目の手順）。規則・定数・定型文は design/contrasts-A.json だけから読み、確証の判定は tools/confirm_A.py の関数で行う（格子・合成検査と同じ関数・二重実装をしない）。
入力（取り決め）:
 - 本走行 results/<tags.main>/・錨反復 results/<tags.anchor_rerun>/・橋 results/<tags.bridge>/・API 再走行 results/<tags.api_rerun>/（門0.5 合格時のみ）・セッション記録 results/sessions-A/（環境値）。読み出しは tools/runs_A.py。
 - --style: tools/response_mode_A.py の出力（kind response_mode_A・cells[機種][場面][腕] の n_ok・a_final・b_final・strata）。
 - --gate: tools/gate_A.py の出力（kind gate_A・gate2.shrink・withdrawal.anomaly）。
 - --identity: tools/identity_screen_A.py の出力（kind identity_screen_A・verdict pass／fail）。
 - --calib: tools/calib_band_A.py の出力（kind calib_band_A・anomaly_run_keys）。
 - --facts: records/A/design-facts-A.json（転記行 D の到達の見込み・reach_note の数）。
処理: 測定不能（腕 × 規模 × 場面・和集合・超）→ 錨帯（規模 × 場面の除外単位・anchor_band.compare）→ 両腕条件の検閲・β₃ の Firth PPLRT・解釈条項・pt 差の傾き・p*（confirm_A.contrast）
→ refuse 門（名目有意 p_β<α の対比）→ 様式門（style_flags）→ 環境保留（橋の帯を超えた腕・残存規模の環境値が一つ）→ 札の二段（confirm_A.label_family・門2 の縮小）
→ 札の全組合せ表の行 id の突合（表に無ければ停止）→ 感度閾値の札 → 測れた効果種（confirm_A.measurable_effect_types）→ 床持続と記述族（p を印字しない）・散文層の副次終点（札を変えない）
→ 注（門0.5 不合格・器の異常）→ 定型文（print_strings）。
出力: records/A/analysis-<tag>.json と同 .md（既存は --force なしでは上書きしない）。
合成検査の口: --synth-nonconverged（対比 id を非収束として扱う）は root が results 以外のときだけ受け付ける。検査用: --no-gate・--no-style・--allow-incomplete（印を出力に残す）。
用法: python tools/analyze_A.py --tag stageA --gate records/A/gate-pilotA.json --identity records/A/identity-screen-A.json --calib records/A/calib-stageA.json
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
from fractions import Fraction
import numpy as np
from scipy.stats import beta as beta_dist
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import confirm_A
import firth
from zaxis_A import z_sizes
REPO = runs_A.REPO
VERSION = 'v1'

ap = argparse.ArgumentParser()
ap.add_argument('--tag', default=None); ap.add_argument('--root', default=None); ap.add_argument('--contrasts', default=None)
ap.add_argument('--style', default=None); ap.add_argument('--no-style', action='store_true')
ap.add_argument('--gate', default=None); ap.add_argument('--no-gate', action='store_true')
ap.add_argument('--identity', default=None); ap.add_argument('--calib', default=None)
ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.json'))
ap.add_argument('--anchor-tag', default=None); ap.add_argument('--bridge-tag', default=None); ap.add_argument('--api-tag', default=None)
ap.add_argument('--B-measurable', type=int, default=None); ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-incomplete', action='store_true'); ap.add_argument('--synth-nonconverged', default='')
a = ap.parse_args()

T = runs_A.load_T(a.contrasts); CPATH = a.contrasts or runs_A.CPATH
R = confirm_A.Rules(T); L = R.labels; FAM = T['families']['A_slope']; PS = T['print_strings']; TAGS = T['tags']
SIZES = T['sizes']; SC = T['scenarios']; ARMS = T['arms']['preamble']; ANCHOR_MODEL = next(m['key'] for m in T['models'] if m['anchor'])
tag = a.tag or TAGS['main']
zs = np.array(z_sizes(SIZES)); i4 = SIZES.index('4B'); z4 = float(zs[i4]); zspan = float(zs[-1] - z4)
real_root = os.path.abspath(runs_A.results_root(a.root)) == os.path.abspath(os.path.join(REPO, 'results'))
SYN_NC = {x for x in a.synth_nonconverged.split(',') if x}
if SYN_NC and real_root:
    sys.exit('--synth-nonconverged は合成検査の置き場（results 以外の root）でだけ使える')
OUT = a.out or os.path.join(REPO, 'records', 'A', 'analysis-%s' % tag)
if (os.path.exists(OUT + '.json') or os.path.exists(OUT + '.md')) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUT)
dev_marks = [x for x, on in (('no_gate', a.no_gate), ('no_style', a.no_style), ('allow_incomplete', a.allow_incomplete), ('synth_nonconverged', bool(SYN_NC)), ('not_results_root', not real_root)) if on]
missing = []
fr = lambda k, n: Fraction(int(k), int(n))
ZERO = dict(n=0, n_ok=0, api_error=0, cat=0, refuse=0, ff=0, loop=0, trunc=0, unmeas=0)


def load_rec(path, kind):
    d = runs_A.read_json(path)
    if d.get('kind') != kind:
        sys.exit('記録の種類が違う: %s（%s を期待・%s）' % (path, kind, d.get('kind')))
    return d


def sha_or_none(p):
    return runs_A.sha16_file(p) if p and os.path.exists(p) else None


# ---- 記録（門・同一性・校正・様式・設計事実）
if a.no_gate:
    G = None
elif not a.gate:
    sys.exit('--gate（tools/gate_A.py の出力）が要る（--no-gate は検査用）')
else:
    G = load_rec(a.gate, 'gate_A')
GATE2 = bool(G and G['gate2']['shrink']); WD_ANOM = bool(G and (G.get('withdrawal') or {}).get('anomaly'))
ID = load_rec(a.identity, 'identity_screen_A') if a.identity else None; ID_VERDICT = ID['verdict'] if ID else None
CB = load_rec(a.calib, 'calib_band_A') if a.calib else None; ANOM_RK = set((CB or {}).get('anomaly_run_keys') or [])
SPATH = a.style or os.path.join(REPO, 'records', 'A', 'style-%s.json' % tag)
if a.no_style:
    STY = None
elif not os.path.exists(SPATH):
    sys.exit('様式の記録が無い: %s（--no-style は検査用）' % SPATH)
else:
    STY = load_rec(SPATH, 'response_mode_A')
FACTS = runs_A.read_json(a.facts) if a.facts and os.path.exists(a.facts) else None


def sty(s, sc, arm):
    try:
        return STY['cells'][s][sc][arm]
    except (TypeError, KeyError):
        return None


# ---- 本走行の件数
C, IDX = runs_A.counts_by(T, tag, a.root)
for s in SIZES + [ANCHOR_MODEL]:
    for sc in SC:
        if (s, sc) not in IDX:
            missing.append('本走行 %s × %s' % (s, sc))


def cnt(s, sc, arm, D=None):
    return (C if D is None else D).get((s, sc, arm)) or ZERO


# ---- 測定不能（腕 × 規模 × 場面・和集合・超・n_ok が零のセルも外す）
UT = Fraction(str(T['unmeasurable']['threshold'])); UNMEAS = {}; unmeas_rows = []
for s in SIZES + [ANCHOR_MODEL]:
    for sc in SC:
        for arm in ARMS:
            c = cnt(s, sc, arm); flag = (c['n_ok'] == 0) or (fr(c['unmeas'], c['n_ok']) > UT); UNMEAS[(s, sc, arm)] = flag
            if flag:
                unmeas_rows.append({'model': s, 'scenario': sc, 'arm': arm, 'n_ok': c['n_ok'], 'union': c['unmeas'], 'format_fail': c['ff'], 'loop': c['loop'], 'truncated': c['trunc'],
                                    'total_count': c['ff'] + c['loop'] + c['trunc'], 'reason': 'n_ok が零' if c['n_ok'] == 0 else '和集合が閾値を超える'})

# ---- 錨帯（anchor_band.compare・超・除外単位は規模 × 場面）
ATAG = a.anchor_tag or TAGS['anchor_rerun']; AB = T['anchor_band']; ABAND = Fraction(AB['band_pt'], 100); ANCH_EX = {}; anchor_rows = []
if runs_A.run_dirs(ATAG, a.root):
    C2, IDX2 = runs_A.counts_by(T, ATAG, a.root)
    for s in AB['models']:
        for sc in AB['scenarios']:
            if (s, sc) not in IDX2:
                missing.append('錨反復 %s × %s' % (s, sc)); continue
            over = []
            for arm in AB['arms']:
                c1, c2 = cnt(s, sc, arm), cnt(s, sc, arm, C2)
                if c1['n_ok'] and c2['n_ok']:
                    d = fr(c1['cat'], c1['n_ok']) - fr(c2['cat'], c2['n_ok']); row = {'diff_pt': float(d * 100), 'over': abs(d) > ABAND}
                else:
                    row = {'diff_pt': None, 'over': False, 'note': '分母が零'}
                row.update(model=s, scenario=sc, arm=arm, main=[c1['cat'], c1['n_ok']], rerun=[c2['cat'], c2['n_ok']]); anchor_rows.append(row)
                if row['over']:
                    over.append(arm)
            if over:
                ANCH_EX[(s, sc)] = over
else:
    missing.append('錨反復（tag %s）' % ATAG)

# ---- 環境値（セッション記録・sessions.env_value_rule）と橋（environment_band）
SESS = runs_A.load_sessions(a.root); ENVK = runs_A.env_by_run_key(SESS); SIZE_ENV = {}; env_fallback = []
for (s, sc), rec in IDX.items():
    e = ENVK.get(rec['run_key'])
    if not e:
        e = {T['environments'][s]['env']}; env_fallback.append(rec['run_key'])
    SIZE_ENV[(s, sc)] = set(e)
BTAG = a.bridge_tag or TAGS['bridge']; EB = T['environment_band']; EBAND = Fraction(EB['band_pt'], 100); BR = T['bridge']; ENV_FLAG = {}; bridge_rows = []; C3 = {}; IDX3 = {}
if runs_A.run_dirs(BTAG, a.root):
    C3, IDX3 = runs_A.counts_by(T, BTAG, a.root)
    for bm, cell in BR['cells'].items():
        key = (bm, BR['scenario'])
        if key not in IDX3:
            missing.append('橋 %s' % bm); continue
        benv = ENVK.get(IDX3[key]['run_key']) or {cell['bridge_env']}
        for arm in BR['arms']:
            cm, cb = cnt(bm, BR['scenario'], arm), cnt(bm, BR['scenario'], arm, C3)
            d = (fr(cb['cat'], cb['n_ok']) - fr(cm['cat'], cm['n_ok'])) if (cm['n_ok'] and cb['n_ok']) else None
            row = {'model': bm, 'arm': arm, 'main': [cm['cat'], cm['n_ok']], 'bridge': [cb['cat'], cb['n_ok']], 'main_env': sorted(SIZE_ENV.get(key, {cell['main_env']})), 'bridge_env': sorted(benv),
                   'diff_pt': None if d is None else float(d * 100), 'over': bool(d is not None and abs(d) > EBAND)}
            bridge_rows.append(row)
            if row['over']:
                ENV_FLAG.setdefault(arm, []).append(row)
else:
    missing.append('橋（tag %s）' % BTAG)

if missing and not a.allow_incomplete:
    sys.exit('走行の記録が足りない（--allow-incomplete は検査用）: %s' % '・'.join(missing))


# ---- 対比ごと
def arrays(c):
    g = lambda arm, k: np.array([cnt(s, c['scenario'], arm)[k] for s in SIZES], np.int64)
    return dict(kA=g(c['A'], 'cat'), nA=g(c['A'], 'n_ok'), rA=g(c['A'], 'refuse'), kB=g(c['B'], 'cat'), nB=g(c['B'], 'n_ok'), rB=g(c['B'], 'refuse'))


def exclusions(c):
    sc = c['scenario']; u = [UNMEAS[(s, sc, c['A'])] or UNMEAS[(s, sc, c['B'])] for s in SIZES]; an = [(s, sc) in ANCH_EX for s in SIZES]
    return u, an, [not (x or y) for x, y in zip(u, an)]


def evaluate(RR, c, X, keep_extra):
    res = confirm_A.contrast(RR, zs, X['kB'], X['kA'], X['nB'], X['nA'], keep_extra)
    if c['id'] in SYN_NC and res['status'] == 'ok':
        res = {'kept': res['kept'], 'keep': res['keep'], 'censored': res['censored'], 'status': 'nonconverged', 'reason': 'nonconverged', 'synthetic_forced': True}
    fl = {'refuse_hold': False, 'refuse': None, 'style': 'none', 'style_detail': None, 'env_hold': False, 'env_reasons': []}
    if res['status'] != 'ok':
        return res, fl
    if res['p_beta'] < RR.alpha:
        g = confirm_A.refuse_gate(RR, zs, X['kB'], X['kA'], X['rB'], X['rA'], X['nB'], X['nA'], res); fl['refuse'] = g; fl['refuse_hold'] = bool(g['hold'])
    if STY is not None:
        sc = c['scenario']; gs = lambda arm, k: [((sty(s, sc, arm) or {}).get(k) or 0) for s in SIZES]
        st = confirm_A.style_flags(RR, gs(c['A'], 'a_final'), gs(c['B'], 'a_final'), gs(c['A'], 'b_final'), gs(c['B'], 'b_final'), gs(c['A'], 'n_ok'), gs(c['B'], 'n_ok'), res['keep'])
        fl['style'] = st['state']; fl['style_detail'] = st
    for arm in (c['A'], c['B']):
        for row in ENV_FLAG.get(arm, []):
            fl['env_reasons'].append({'rule': 'bridge', 'arm': arm, 'model': row['model'], 'diff_pt': row['diff_pt']})
    envs = set()
    for i in res['idx']:
        envs |= SIZE_ENV.get((SIZES[i], c['scenario']), set())
    if len(envs) == 1:
        fl['env_reasons'].append({'rule': 'one_side', 'env': next(iter(envs))})
    fl['env_hold'] = bool(fl['env_reasons'])
    return res, fl


CONTR = FAM['contrasts']; RES, FL, XS, EXC = [], [], [], []
for c in CONTR:
    X = arrays(c); u, an, ke = exclusions(c); r, f = evaluate(R, c, X, ke); RES.append(r); FL.append(f); XS.append(X); EXC.append((u, an, ke))
LAB = confirm_A.label_family(R, RES, FL, gate2_shrink=GATE2)
COMBO_IDS = {row['id'] for row in FAM['confirm_rule']['label_combo_table']}
bad = [(c['id'], o['row']) for c, o in zip(CONTR, LAB) if o['row'] not in COMBO_IDS]
if bad:
    sys.exit('札の全組合せ表に無い行に落ちた（停止・label_combo_rule）: %s' % bad)
ORDER = ['confirmed', 'undecidable', 'clause', 'scale_only', 'refuse', 'style', 'env', 'ns']
COUNTS = {k: sum(1 for o in LAB if o['label'] == L[k]) for k in ORDER}
assert sum(COUNTS.values()) == R.m, COUNTS
FIRST = PS['first_finding'] % tuple([R.m] + [COUNTS[k] for k in ORDER])

# ---- 感度閾値（主閾値と札が変わった対比）
SENS = []
for lo, hi in zip(T['censor']['sensitivity']['low'], T['censor']['sensitivity']['high']):
    R2 = confirm_A.Rules(T, censor_low=lo, censor_high=hi); res2, fl2 = [], []
    for c, X, (u, an, ke) in zip(CONTR, XS, EXC):
        r2, f2 = evaluate(R2, c, X, ke); res2.append(r2); fl2.append(f2)
    lab2 = confirm_A.label_family(R2, res2, fl2, gate2_shrink=GATE2)
    changed = [{'id': c['id'], 'main': o['label'], 'sensitivity': o2['label'], 'row': o2['row']} for c, o, o2 in zip(CONTR, LAB, lab2) if o['label'] != o2['label']]
    SENS.append({'low': lo, 'high': hi, 'counts': {k: sum(1 for o in lab2 if o['label'] == L[k]) for k in ORDER}, 'changed': changed,
                 'string': PS['sensitivity_diff'].format(low=lo, high=hi, ids='・'.join(x['id'] for x in changed) or 'なし')})

# ---- 測れた効果種（登録者裁定 D11）
rows_m = []
for c, X, (u, an, ke) in zip(CONTR, XS, EXC):
    nA, nB = X['nA'], X['nB']
    rows_m.append({'id': c['id'], 'effect': c['id'].split(':', 1)[1], 'pc': [(X['kB'][i] / nB[i]) if nB[i] else float('nan') for i in range(len(SIZES))],
                   'rA4': (X['kA'][i4] / nA[i4]) if nA[i4] else float('nan'), 'rB4': (X['kB'][i4] / nB[i4]) if nB[i4] else float('nan'), 'keep': ke, 'at4_ok': bool(ke[i4] and nA[i4] and nB[i4])})
PERM, TYPES = confirm_A.measurable_effect_types(R, T, zs, z4, zspan, rows_m, B=a.B_measurable)
ME = T['reading_selection']['measurable_effect_type']
MEAS_YES = [e for e, v in TYPES.items() if v['measurable']]; MEAS_NO = [e for e, v in TYPES.items() if not v['measurable']]
MEAS_STR = PS['measurable'].format(delta_pt='%g' % round(ME['delta'] * 100, 6), thr=ME['threshold'], yes='・'.join(MEAS_YES) or 'なし', no='・'.join(MEAS_NO) or 'なし')
REACH = None
if FACTS:
    Dd = FACTS['facts']['D']['data']
    REACH = PS['reach_note'].format(n_meas=Dd['n_measured'], n_blind=len(Dd['blind_all_trends']), delta_pt='%g' % round(Dd['delta'] * 100, 6), thr=Dd['blind_threshold'], n_nobase=len(Dd['no_base']))

# ---- 床持続（記述・p を印字しない）
FD = T['descriptive_families']['A_desc_floor']; LOWF = float(T['censor']['low']); floor_rows = []
for cell in FD['cells']:
    arm, sc = cell['arm'], cell['scenario']; ubs, fails = [], []
    for s in SIZES:
        c = cnt(s, sc, arm)
        if UNMEAS[(s, sc, arm)]:
            ubs.append('測定不能'); fails.append(s); continue
        k, n = c['cat'], c['n_ok']; ub = 1.0 if k >= n else float(beta_dist.ppf(FD['cp_level'], k + 1, n - k)); ubs.append('%.4f' % ub)
        if not ub < LOWF:
            fails.append(s)
    flag = 0 if fails else 1
    floor_rows.append({'id': cell['id'], 'arm': arm, 'scenario': sc, 'upper': ubs, 'flag': flag, 'fail_sizes': fails,
                       'string': PS['floor_desc'].format(arm=arm, sc=sc, ubs='／'.join('%s %s' % (s, u) for s, u in zip(SIZES, ubs)), flag=flag, fail_sizes='・'.join(fails) or 'なし')})


# ---- 記述族（p を印字しない）
def rate_row(s, sc, arm, D=None):
    c = cnt(s, sc, arm, D); return {'k': c['cat'], 'n': c['n_ok'], 'rate': (c['cat'] / c['n_ok']) if c['n_ok'] else None, 'wilson': confirm_A.wilson(c['cat'], c['n_ok'])}


def diff_pt(ra, rb):
    return None if (ra['rate'] is None or rb['rate'] is None) else 100.0 * (ra['rate'] - rb['rate'])


DESC = {}
for fk in ('A_desc_nstr', 'A_desc_ncold'):
    DESC[fk] = [{'id': c['id'], 'sizes': [dict(size=s, A=rate_row(s, c['scenario'], c['A']), B=rate_row(s, c['scenario'], c['B']), unmeasurable=UNMEAS[(s, c['scenario'], c['A'])] or UNMEAS[(s, c['scenario'], c['B'])],
                                                diff_pt=diff_pt(rate_row(s, c['scenario'], c['A']), rate_row(s, c['scenario'], c['B']))) for s in SIZES]}
                for c in T['descriptive_families'][fk]['contrasts']]
DESC['A_desc_recipe'] = [dict(id=c['id'], base=rate_row('4B', c['scenario'], c['arm']), anchor=rate_row(ANCHOR_MODEL, c['scenario'], c['arm']),
                              diff_pt=diff_pt(rate_row('4B', c['scenario'], c['arm']), rate_row(ANCHOR_MODEL, c['scenario'], c['arm']))) for c in T['descriptive_families']['A_desc_recipe']['contrasts']]
STACK = {'status': None, 'rows': []}; APITAG = a.api_tag or TAGS['api_rerun']
if ID_VERDICT == 'pass':
    if runs_A.run_dirs(APITAG, a.root):
        C4, IDX4 = runs_A.counts_by(T, APITAG, a.root); STACK['status'] = '門0.5 合格・API 再走行の記録あり'
        for (s, sc) in sorted(IDX4):
            for arm in ARMS:
                lr, ar = rate_row(s, sc, arm), rate_row(s, sc, arm, C4); STACK['rows'].append({'model': s, 'scenario': sc, 'arm': arm, 'local': lr, 'api': ar, 'diff_pt': diff_pt(lr, ar)})
    else:
        STACK['status'] = '門0.5 合格・API 再走行の記録なし'; missing.append('API 再走行（tag %s）' % APITAG)
elif ID_VERDICT == 'fail':
    STACK['status'] = '門0.5 不合格（並置しない・API 再走行を行わない）'
else:
    STACK['status'] = '門0.5 の記録なし'
DESC['A_desc_stack'] = STACK


def env_secondary(c):
    """環境ダミーと arm×環境を加えた同型の回帰（副次解析・記述・p を印字しない）。N1 の対比で、主走行の規模（環境値が一つ）と橋の行を使う。"""
    sc = BR['scenario']
    if c['scenario'] != sc or not IDX3:
        return None
    rows = []
    for i, s in enumerate(SIZES):
        e = SIZE_ENV.get((s, sc))
        if e and len(e) == 1:
            for af, arm in ((0.0, c['B']), (1.0, c['A'])):
                cc = cnt(s, sc, arm)
                if cc['n_ok'] and not UNMEAS[(s, sc, arm)]:
                    rows.append((float(zs[i]), af, next(iter(e)), cc['cat'], cc['n_ok']))
    for bm, cell in BR['cells'].items():
        key = (bm, sc)
        if key in IDX3:
            ev = ENVK.get(IDX3[key]['run_key']) or {cell['bridge_env']}
            if len(ev) == 1:
                for af, arm in ((0.0, c['B']), (1.0, c['A'])):
                    cc = cnt(bm, sc, arm, C3)
                    if cc['n_ok']:
                        rows.append((float(zs[SIZES.index(bm)]), af, next(iter(ev)), cc['cat'], cc['n_ok']))
    envs = sorted({r[2] for r in rows} - {'L4'})
    if not envs or len({r[2] for r in rows}) < 2:
        return {'id': c['id'], 'status': '当てはめ不可（環境値の変化なし）'}
    cols = ['const', 'arm', 'z', 'arm*z'] + [x for e in envs for x in ('env_' + e, 'arm*env_' + e)]
    Xm = np.array([[1.0, r[1], r[0], r[1] * r[0]] + [v for e in envs for v in ((1.0 if r[2] == e else 0.0), r[1] * (1.0 if r[2] == e else 0.0))] for r in rows])
    if len(rows) <= Xm.shape[1]:
        return {'id': c['id'], 'status': '当てはめ不可（行が足りない）'}
    ft = firth.fit(Xm, np.array([r[3] for r in rows], float), np.array([r[4] for r in rows], float))
    return {'id': c['id'], 'status': '収束' if ft['converged'] else '非収束', 'columns': cols, 'estimates': dict(zip(cols, [float(b) for b in ft['beta']])), 'rows': len(rows), 'note': '副次解析・記述（p を印字しない）'}


def critical(c, X, keep):
    """臨界規模（descriptive_families.A_desc_critical_size.rule・零は符号の変化に数えない）。"""
    idx = [i for i in range(len(SIZES)) if keep[i] and X['nA'][i] and X['nB'][i]]
    d = [(i, fr(X['kA'][i], X['nA'][i]) - fr(X['kB'][i], X['nB'][i])) for i in idx]
    ref = next((1 if v > 0 else -1 for i, v in d if v != 0), 0)
    size = next((SIZES[i] for i, v in d if v != 0 and (1 if v > 0 else -1) != ref), None) if ref else None
    return {'size': size or 'なし', 'sizes': [SIZES[i] for i in idx]}


CTRL = []
for sc in SC:
    for arm in sorted({c['B'] for c in CONTR if c['scenario'] == sc}, key=ARMS.index):
        CTRL.append({'scenario': sc, 'arm': arm, 'sizes': {s: rate_row(s, sc, arm) for s in SIZES + [ANCHOR_MODEL]}})

# ---- 散文層の副次終点（style_gate.stratified・札を変えない）
STRAT = []; MIN_STRAT = FAM['refuse_gate']['answered_min_n_ok']
for c, r, f in zip(CONTR, RES, FL):
    if STY is None or r['status'] != 'ok' or f['style'] not in ('hold', 'note'):
        continue
    sc = c['scenario']; gp = lambda arm, k: np.array([(((sty(s, sc, arm) or {}).get('strata') or {}).get('prose') or {}).get(k, 0) for s in SIZES], np.int64)
    kPA, nPA, kPB, nPB = gp(c['A'], 'cat'), gp(c['A'], 'n'), gp(c['B'], 'cat'), gp(c['B'], 'n')
    kp = [bool(r['keep'][i] and nPA[i] >= MIN_STRAT and nPB[i] >= MIN_STRAT) for i in range(len(SIZES))]
    r2 = confirm_A.contrast(R, zs, kPB, kPA, nPB, nPA, kp); item = {'id': c['id'], 'style': f['style'], 'status': r2['status'], 'sizes': [SIZES[i] for i in range(len(SIZES)) if r2['keep'][i]]}
    if r2['status'] == 'ok':
        item.update(beta=r2['beta'], p_beta=r2['p_beta'], slope_pt=R.scale * r2['slope'],
                    string=PS['stratified_note'].format(A=c['A'], B=c['B'], beta='%+.3f' % r2['beta'], p='%.3g' % r2['p_beta'], slope_pt='%+.2f' % (R.scale * r2['slope']), sizes='・'.join(item['sizes'])))
    STRAT.append(item)

# ---- 対比ごとの出力・定型文・注・降格の三行
REASON = FAM['confirm_rule']['label_stages']['stage0_pre_test']['reason_text']; OUTC = []; DEMOTE = []; ENVSEC = []
for c, r, f, o, X, (u, an, ke) in zip(CONTR, RES, FL, LAB, XS, EXC):
    kept = [SIZES[j] for j in range(len(SIZES)) if r['keep'][j]]; lab = o['label']
    st = {'residual_sizes': PS['residual_sizes'].format(sizes='・'.join(kept) or 'なし', c=sum(1 for x in r['censored'] if x), u=sum(u), a=sum(an))}
    if lab in (L['confirmed'], L['scale_only']):
        lo_, hi_ = o['interval_pt']
        if lab == L['confirmed']:
            st['label'] = PS['label_confirmed'].format(A=c['A'], B=c['B'], sign='+' if r['beta'] > 0 else '−', slope_pt='%+.2f' % o['slope_pt'], level='%.5f' % o['star_holm']['level'], ci_lo='%+.2f' % lo_, ci_hi='%+.2f' % hi_)
        else:
            st['label'] = PS['label_scale_only'].format(A=c['A'], B=c['B'], slope_pt='%+.2f' % o['slope_pt'], ci_lo='%+.2f' % lo_, ci_hi='%+.2f' % hi_)
    elif lab == L['clause']:
        arm = c['A'] if r['sat_A'] >= R.clause_min else c['B']; st['label'] = PS['label_interp'].format(A=c['A'], B=c['B'], arm=arm, k=r['sat_A'] if arm == c['A'] else r['sat_B'])
    elif lab == L['undecidable']:
        st['label'] = PS['label_undecidable'].format(A=c['A'], B=c['B'], reason=REASON.get(o['rules'][0], o['rules'][0]))
    if f['env_reasons']:
        st['env'] = [PS['env_hold'].format(d='%+.1f' % x['diff_pt'], model=x['model'], arm=x['arm'], band=EB['band_pt']) if x['rule'] == 'bridge' else PS['one_side_hold'].format(env=x['env']) for x in f['env_reasons']]
    if f['style_detail'] and f['style_detail']['cells']:
        st['style'] = [PS['style_note'].format(A=c['A'], B=c['B'], kind=x['kind'], size=SIZES[x['size_index']], diff_pt='%.1f' % x['diff_pt']) for x in f['style_detail']['cells']]
    notes = []
    if ID_VERDICT == 'fail' and 'N' in (c['A'], c['B']):
        notes.append(PS['identity_fail_note'])
    if lab == L['confirmed']:
        rks = {IDX[(SIZES[j], c['scenario'])]['run_key'] for j in range(len(SIZES)) if r['keep'][j] and (SIZES[j], c['scenario']) in IDX}
        if rks & ANOM_RK:
            notes.append(PS['calib_anomaly_note'])
        if WD_ANOM:
            notes.append(PS['withdrawal_anomaly_note'])
    if o['stage'] == 2 and lab != L['confirmed']:
        DEMOTE.append({'id': c['id'], 'string': PS['demotion_three_lines'].format(upper=o['upper'], actual=lab, rules='・'.join(o['rules']), row=o['row'])})
    crit = critical(c, X, r['keep']); st['critical_size'] = PS['critical_size'].format(A=c['A'], B=c['B'], sc=c['scenario'], size=crit['size'], sizes='・'.join(crit['sizes']) or 'なし')
    es = env_secondary(c)
    if es:
        ENVSEC.append(es)
    OUTC.append({'id': c['id'], 'scenario': c['scenario'], 'A': c['A'], 'B': c['B'], 'counts': {k: v.tolist() for k, v in X.items()}, 'excluded_unmeasurable': u, 'excluded_anchor': an,
                 'result': {k: v for k, v in r.items()}, 'refuse_gate': f['refuse'], 'style': f['style'], 'style_detail': f['style_detail'], 'env_hold': f['env_hold'], 'env_reasons': f['env_reasons'],
                 'label': lab, 'stage': o['stage'], 'row': o['row'], 'rules': o['rules'], 'upper': o['upper'], 'beta_holm': o['beta_holm'], 'star_holm': o['star_holm'],
                 'slope_pt': o.get('slope_pt'), 'interval_pt': o.get('interval_pt'), 'notes': notes, 'critical_size': crit, 'strings': st})

SCALE_ONLY = [{'id': x['id'], 'slope_pt': x['slope_pt'], 'interval_pt': x['interval_pt']} for x in OUTC if x['label'] == L['scale_only']]
DESC['A_desc_scale_only'] = SCALE_ONLY; DESC['A_desc_env'] = {'bridge': bridge_rows, 'secondary': ENVSEC}; DESC['A_desc_anchor_drift'] = anchor_rows
DESC['A_desc_critical_size'] = [{'id': x['id'], **x['critical_size']} for x in OUTC]


def js(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    if isinstance(o, Fraction):
        return float(o)
    raise TypeError(type(o))


INPUTS = {'contrasts_sha16': runs_A.sha16_file(CPATH), 'confirm_A': [confirm_A.VERSION, runs_A.sha16_file(os.path.join(REPO, 'tools', 'confirm_A.py'))], 'firth': [firth.VERSION, runs_A.sha16_file(os.path.join(REPO, 'tools', 'firth.py'))],
          'runs_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'runs_A.py')), 'zaxis_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'zaxis_A.py')), 'analyze_A': runs_A.sha16_file(os.path.abspath(__file__)),
          'style': sha_or_none(None if a.no_style else SPATH), 'gate': sha_or_none(a.gate), 'identity': sha_or_none(a.identity), 'calib': sha_or_none(a.calib), 'facts': sha_or_none(a.facts), 'sessions': len(SESS)}
RESULT = {'kind': 'analyze_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'tag': tag, 'root': a.root, 'dev_marks': dev_marks, 'inputs': INPUTS,
          'missing': missing, 'env_fallback_run_keys': env_fallback, 'gate2_shrink': GATE2, 'identity_verdict': ID_VERDICT, 'withdrawal_anomaly': WD_ANOM, 'calib_anomaly_run_keys': sorted(ANOM_RK),
          'label_counts': COUNTS, 'first_finding': FIRST, 'reach_note': REACH, 'measurable': {'string': MEAS_STR, 'types': TYPES, 'per_contrast': PERM, 'B': a.B_measurable or ME['B_per_contrast']},
          'unmeasurable': unmeas_rows, 'anchor_excluded_units': [{'model': s, 'scenario': sc, 'arms': v} for (s, sc), v in sorted(ANCH_EX.items())], 'size_env': {'%s|%s' % k: sorted(v) for k, v in sorted(SIZE_ENV.items())},
          'env_flag_arms': {k: v for k, v in ENV_FLAG.items()}, 'contrasts': OUTC, 'demotions': DEMOTE, 'sensitivity': SENS, 'floor': floor_rows, 'descriptive': DESC, 'stratified': STRAT, 'control_bases': CTRL,
          'clause': '本集計のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(RESULT, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=js)

# ---- md（表は機械出力・散文の数は定型文だけ）
f3 = lambda v: '—' if v is None else '%.3f' % v
kn = lambda row: '%d/%d' % (row['k'], row['n'])
M = ['# 段階 A 集計（機械生成・`tools/analyze_A.py` %s・%s UTC）' % (VERSION, RESULT['generated_utc']), '',
     '- tag %s・root %s・入力 %s' % (tag, a.root or 'results', json.dumps(INPUTS, ensure_ascii=False)),
     '- 検査用の印: %s・足りない記録: %s・環境値を登録値で補った走行キー: %d' % ('・'.join(dev_marks) or 'なし', '・'.join(missing) or 'なし', len(env_fallback)),
     '- 門2 の縮小: %s・門0.5: %s・撤退条件の器の異常: %s・校正腕の器の異常の走行キー: %d' % ('あり' if GATE2 else 'なし', ID_VERDICT or '記録なし', 'あり' if WD_ANOM else 'なし', len(ANOM_RK)), '',
     '## 第一の所見・到達の見込み・測れた効果種', '', FIRST, '', REACH or '（設計事実の記録なし）', '', MEAS_STR, '',
     '## 対照腕の基底率（破局/n_ok・規模 × 場面）', '', '| 場面 | 対照腕 | %s |' % ' | '.join(SIZES + [ANCHOR_MODEL + '（別記号）']), '|---|---|%s' % ('---|' * (len(SIZES) + 1))]
for x in CTRL:
    M.append('| %s | %s | %s |' % (x['scenario'], x['arm'], ' | '.join('%s（%s）' % (kn(x['sizes'][s]), f3(x['sizes'][s]['rate'])) for s in SIZES + [ANCHOR_MODEL])))
M += ['', '## 全対比の並記表', '', '| 対比 | A 破局/n（規模順） | B 破局/n（規模順） | 残った規模 | β₃（推定・p_β・Holm 順位/水準） | pt 差の傾き（pt／z・p_pt） | p*（Holm 順位/水準・区間） | 解釈条項 | refuse 門 | 様式門 | 環境 | 札 | 段 | 当てはまった規則 | 行 id | 注 |',
      '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for x in OUTC:
    r = x['result']; ok = r['status'] == 'ok'; cnts = x['counts']
    M.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d | %s | %s | %s |' % (
        x['id'], ' '.join('%d/%d' % (k, n) for k, n in zip(cnts['kA'], cnts['nA'])), ' '.join('%d/%d' % (k, n) for k, n in zip(cnts['kB'], cnts['nB'])), x['strings']['residual_sizes'],
        ('%+.3f・%.3g・%d/%.5f' % (r['beta'], r['p_beta'], x['beta_holm']['rank'], x['beta_holm']['level'])) if ok else r['status'],
        ('%+.2f・%.3g' % (x['slope_pt'], r['p_pt'])) if ok else '—',
        ('%.3g・%d/%.5f・%+.2f〜%+.2f' % (r['p_star'], x['star_holm']['rank'], x['star_holm']['level'], x['interval_pt'][0], x['interval_pt'][1])) if ok else '—',
        ('発火（A %d・B %d）' % (r['sat_A'], r['sat_B']) if r['clause'] else '—') if ok else '—',
        ('保留（%s）' % ''.join(x['refuse_gate']['reasons']) if x['refuse_gate']['hold'] else '当てた・保留なし') if x['refuse_gate'] else '—',
        x['style'], ('保留（%s）' % '・'.join(e['rule'] for e in x['env_reasons'])) if x['env_hold'] else '—', x['label'], x['stage'], '・'.join(x['rules']), x['row'], '・'.join(x['notes']) or '—'))
M += ['', '### 定型文（対比ごと）', ''] + ['- %s: %s' % (x['id'], ' '.join([x['strings'].get('label', '')] + x['strings'].get('env', []) + x['strings'].get('style', []))) for x in OUTC if x['strings'].get('label') or x['strings'].get('env')]
M += ['', '## 降格・保留の三行', ''] + (['- %s: %s' % (d['id'], d['string']) for d in DEMOTE] or ['- なし'])
M += ['', '## 感度閾値での札', '', '| 閾値 | %s | 主閾値と札が変わった対比 |' % ' | '.join(L[k] for k in ORDER), '|---|%s---|' % ('---|' * len(ORDER)),
      '| %s／%s（主） | %s | — |' % (T['censor']['low'], T['censor']['high'], ' | '.join(str(COUNTS[k]) for k in ORDER))]
for s_ in SENS:
    M.append('| %s／%s | %s | %s |' % (s_['low'], s_['high'], ' | '.join(str(s_['counts'][k]) for k in ORDER), '・'.join(x['id'] for x in s_['changed']) or 'なし'))
M += ['', '## 到達の見込みと測れた効果種（本走行の対照の率・Δ は正本の値・B=%d）' % RESULT['measurable']['B'], '', '| 効果種 | 対比数 | 少なくとも一本の確率 | 測れた |', '|---|---|---|---|']
M += ['| %s | %d | %.3f | %s |' % (e, v['n_contrasts'], v['at_least_one'], '測れた' if v['measurable'] else '測れなかった') for e, v in TYPES.items()]
M += ['', '| 対比 | 札 D1（初段）の確率 | 備考 |', '|---|---|---|'] + ['| %s | %.3f | %s |' % (p['id'], p['p_card_D1_first'], p['detail'].get('reason', '')) for p in PERM]
M += ['', '## 測定不能（腕 × 規模 × 場面）', ''] + (['- %s × %s × %s: 和集合 %d/%d（書式外 %d・ループ %d・切り詰め %d・延べ %d・%s）' % (x['model'], x['scenario'], x['arm'], x['union'], x['n_ok'], x['format_fail'], x['loop'], x['truncated'], x['total_count'], x['reason']) for x in unmeas_rows] or ['- なし'])
M += ['', '## 錨帯（除外単位＝規模 × 場面）', ''] + (['- %s × %s（帯を超えた腕: %s）' % (x['model'], x['scenario'], '・'.join(x['arms'])) for x in RESULT['anchor_excluded_units']] or ['- 除外なし'])
M += ['', '## 橋と環境', '', '| 機種 | 腕 | 本走行 | 橋 | 主環境 | 橋の環境 | 差（pt） | 帯を超えた |', '|---|---|---|---|---|---|---|---|']
M += ['| %s | %s | %d/%d | %d/%d | %s | %s | %s | %s |' % (x['model'], x['arm'], x['main'][0], x['main'][1], x['bridge'][0], x['bridge'][1], '・'.join(x['main_env']), '・'.join(x['bridge_env']), '—' if x['diff_pt'] is None else '%+.1f' % x['diff_pt'], '超' if x['over'] else '—') for x in bridge_rows]
M += ['', '### 環境の副次解析（記述・p を印字しない）', ''] + (['- %s: %s %s' % (x['id'], x['status'], json.dumps(x.get('estimates', {}), ensure_ascii=False)) for x in ENVSEC] or ['- なし'])
M += ['', '## 床持続（記述・p を印字しない）', ''] + ['- ' + x['string'] for x in floor_rows]
M += ['', '## 記述族（p を印字しない）', '', '### Nstr−Onull・Ncold−N（規模ごとの差・pt）', '', '| 対比 | %s |' % ' | '.join(SIZES), '|---|%s' % ('---|' * len(SIZES))]
for fk in ('A_desc_nstr', 'A_desc_ncold'):
    M += ['| %s | %s |' % (x['id'], ' | '.join(('測定不能' if y['unmeasurable'] else ('—' if y['diff_pt'] is None else '%+.1f' % y['diff_pt'])) for y in x['sizes'])) for x in DESC[fk]]
M += ['', '### レシピ対（4B 対 4B-2507・手元同士・差 pt）', ''] + ['- %s: %s' % (x['id'], '—' if x['diff_pt'] is None else '%+.1f' % x['diff_pt']) for x in DESC['A_desc_recipe']]
M += ['', '### スタック差', '', '- ' + STACK['status']] + ['- %s × %s × %s: 手元 %s・API %s・差 %s' % (x['model'], x['scenario'], x['arm'], kn(x['local']), kn(x['api']), '—' if x['diff_pt'] is None else '%+.1f' % x['diff_pt']) for x in STACK['rows']]
M += ['', '### 対数オッズ尺度でのみ立った対比（pt 差の傾きと区間）', ''] + (['- %s: %+.2f pt／z（%+.2f〜%+.2f）' % (x['id'], x['slope_pt'], x['interval_pt'][0], x['interval_pt'][1]) for x in SCALE_ONLY] or ['- なし'])
M += ['', '### 臨界規模', ''] + ['- ' + x['strings']['critical_size'] for x in OUTC]
M += ['', '### 錨の走行間差（帯を超えた腕のみ・全行は JSON）', ''] + (['- %s × %s × %s: %+.1f pt' % (x['model'], x['scenario'], x['arm'], x['diff_pt']) for x in anchor_rows if x['over']] or ['- なし'])
M += ['', '## 散文層の副次終点（札を変えない）', ''] + ([('- ' + x['string']) if x.get('string') else '- %s: %s（残った規模 %s）' % (x['id'], x['status'], '・'.join(x['sizes']) or 'なし') for x in STRAT] or ['- なし'])
M += ['', RESULT['clause']]
open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[analyze_A %s] written %s.{json,md} | %s | 測れた効果種 %d/%d | 感度で変わった対比 %s | 印 %s' % (VERSION, OUT, json.dumps(COUNTS, ensure_ascii=False), len(MEAS_YES), len(TYPES),
      [len(s_['changed']) for s_ in SENS], '・'.join(dev_marks) or 'なし'))
