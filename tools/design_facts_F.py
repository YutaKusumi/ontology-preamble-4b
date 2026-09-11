# -*- coding: utf-8 -*-
"""design_facts_F.py v1 —— 段階 F の設計事実（規模 A・対比 B・被覆 C′・FWER D′・撤退条件の帯と帰無発火率 E′・門の誤判率 G′・m の受益と到達確率 H′・検出力＝複製の検出力 I′・門の降格見込み J′・様式門の帯 K′・
drift の帯 M′・添え札の感度と偽上昇率と本数の閾値と構造的検出不能の境界 N′・全組合せ表の行数・引数文字列 SHA・走行と seed）を `design/contrasts-F.json`・台帳から機械生成する。
本文（草案／凍結文書）はこの出力を転記するだけで、散文中に手計算の数を書かない。出力: records/F/design-facts-F.md と同 .json（上書き＝正本の現状を映す）。
費用・時間の係数は追補 M の実績（221,760 試行＝壁時計 39.34 時間・実働 33.61 時間・約 2.8 ドル〔登録者申告〕）の試行数比例（目安・費用はトークン数に比例し腕の長さで上下する）。
"""
import os, sys, json, math, hashlib, datetime
from scipy.stats import binom, fisher_exact
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vprime_power import make_power
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8')); n = T['n_per_arm']; SC = list(T['scenarios']); G = T['gate_counts']; pn = G['pilot_n']; BASES = T['bases']
LV = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8')); LF = json.load(open(os.path.join(REPO, 'arms', 'panelF', 'SHA-LEDGER-F.json'), encoding='utf-8'))
pre = T['arms']['preamble']; arms = pre; fams = T['families']; dfams = T['descriptive_families']; FAMF = fams['F']; MT = T['mention_tag']; CT = T['continuity']
allc = [(f, c) for f, F in list(fams.items()) + list(dfams.items()) for c in F['contrasts']]; ids = [c['id'] for f, c in allc]
dup = sorted({i for i in ids if ids.count(i) > 1}); used = {c[k] for f, c in allc for k in ('A', 'B')}; unlinked = [a for a in arms if a not in used]
not_in_ledger = [a for a in pre if a != 'N' and a not in LV and a not in LF['preamble']]
for f, F in fams.items():
    assert F['m'] == len(F['contrasts']), (f, F['m'], len(F['contrasts']))
if dup or unlinked or not_in_ledger:
    print('[facts] 整合エラー: dup=%s unlinked=%s not_in_ledger=%s' % (dup, unlinked, not_in_ledger)); sys.exit(2)
# ---- A 規模（M 実績比）
M_TRIALS, M_WALL_H, M_WORK_H, M_USD = 221760, 39.34, 33.61, 2.8
t_run = len(SC) * len(arms) * n; t_pilot = len(SC) * len(arms) * pn; t_total = 2 * t_run + t_pilot
hrs = lambda t: t * M_WALL_H / M_TRIALS; whrs = lambda t: t * M_WORK_H / M_TRIALS; usd = lambda t: t * M_USD / M_TRIALS
s_pre = ','.join(pre); sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
conf_n = sum(F['m'] for F in fams.values()); desc_n = sum(len(F['contrasts']) for F in dfams.values()); measured = sum(1 for c in FAMF['contrasts'] if c.get('base_B_M1') is not None)
# ---- 検出力（両側 Fisher・全数列挙）
power = make_power(n); cache = {}
def pw(p0, p1, a):
    key = (round(p0, 4), round(min(max(p1, 0.0), 1.0), 4), round(a, 6))
    if key not in cache:
        cache[key] = power(*key)
    return cache[key]
def p_sig_higher(pA, pB, alpha=MT['alpha'], nn=n):
    """A が B より有意に高い（両側 Fisher p≤α かつ x_A/n > x_B/n）確率・全数列挙。"""
    px = binom.pmf(np.arange(nn + 1), nn, pA); cdf = np.cumsum(binom.pmf(np.arange(nn + 1), nn, pB)); tot = 0.0
    for x in range(nn + 1):
        if px[x] < 1e-14:
            continue
        lo, hi = -1, x - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if fisher_exact([[x, nn - x], [mid, nn - mid]])[1] <= alpha: lo = mid
            else: hi = mid - 1
        if lo >= 0:
            tot += px[x] * cdf[lo]
    return float(tot)
A = 0.05 / FAMF['m']
# ---- I′: 検出力（実測基底 24 本・上下二枝）
def kind(b):
    return 'floor' if b < 0.05 else 'ceiling' if b > 0.95 else 'mid'
I = {}
for c in FAMF['contrasts']:
    b = c['base_B_M1']; k = kind(b); ds = (0.09, 0.05, 0.02) if k != 'mid' else (0.15, 0.09, 0.05)
    I[c['id']] = {'base': b, 'kind': k, 'up': [pw(b, b + d, A) for d in ds] if k != 'ceiling' else None, 'down': [pw(b, b - d, A) for d in ds] if k != 'floor' else None, 'deltas': ds}
def band(sel):
    return (min(sel), max(sel)) if sel else (None, None)
IB = {'floor_up_9': band([v['up'][0] for v in I.values() if v['kind'] == 'floor']), 'floor_up_5': band([v['up'][1] for v in I.values() if v['kind'] == 'floor']), 'ceiling_down_9': band([v['down'][0] for v in I.values() if v['kind'] == 'ceiling']), 'ceiling_down_5': band([v['down'][1] for v in I.values() if v['kind'] == 'ceiling']),
      'mid_up_15': band([v['up'][0] for v in I.values() if v['kind'] == 'mid']), 'mid_up_9': band([v['up'][1] for v in I.values() if v['kind'] == 'mid']), 'mid_up_5': band([v['up'][2] for v in I.values() if v['kind'] == 'mid']), 'mid_down_15': band([v['down'][0] for v in I.values() if v['kind'] == 'mid']), 'mid_down_9': band([v['down'][1] for v in I.values() if v['kind'] == 'mid']), 'mid_down_5': band([v['down'][2] for v in I.values() if v['kind'] == 'mid']),
      'n_floor': sum(1 for v in I.values() if v['kind'] == 'floor'), 'n_ceiling': sum(1 for v in I.values() if v['kind'] == 'ceiling'), 'n_mid': sum(1 for v in I.values() if v['kind'] == 'mid')}
IB['p_conf_and_rep_mid_up9'] = band([v['up'][1] ** 2 for v in I.values() if v['kind'] == 'mid']); IB['p_conf_and_rep_mid_up15'] = band([v['up'][0] ** 2 for v in I.values() if v['kind'] == 'mid'])
# ---- J′: 門の降格見込み（n=40・base_M1）
def single(p):
    return binom.cdf(G['both_floor_max'], pn, p) if p < 0.5 else binom.sf(G['both_ceiling_min'] - 1, pn, p)
Jg = {}
for sc in SC:
    for b in BASES:
        x = T['scenarios'][sc]['base_M1'][b]; p = x['catastrophe'] / x['n_ok']; s = single(p)
        alt9 = min(p + 0.09, 1.0) if p < 0.5 else max(p - 0.09, 0.0); alt15 = min(p + 0.15, 1.0) if p < 0.5 else max(p - 0.15, 0.0); alt5 = min(p + 0.05, 1.0) if p < 0.5 else max(p - 0.05, 0.0)
        Jg['%s:%s' % (sc, b)] = {'base': p, 'single': s, 'null_both': s * s, 'judgeable_null': 1 - s * s, 'reject_alt9': s * single(alt9), 'reject_alt15': s * single(alt15), 'pass_alt5': 1 - s * single(alt5), 'power_alt5': pw(p, alt5, A), 'joint_alt5': (1 - s * single(alt5)) * pw(p, alt5, A)}
max_rej9 = max(v['reject_alt9'] for v in Jg.values()); max_rej15 = max(v['reject_alt15'] for v in Jg.values())
# 場面横断（同一土台で 3 場面判定可能）の帰無確率・土台横断（同一場面で 3 土台）
def p_at_least3(qs):
    from itertools import combinations
    tot = 0.0
    for r in range(3, len(qs) + 1):
        for comb in combinations(range(len(qs)), r):
            pr = 1.0
            for i, q in enumerate(qs):
                pr *= q if i in comb else (1 - q)
            tot += pr
    return tot
cross_scene = {b: p_at_least3([Jg['%s:%s' % (sc, b)]['judgeable_null'] for sc in SC]) for b in BASES}
cross_base = {sc: p_at_least3([Jg['%s:%s' % (sc, b)]['judgeable_null'] for b in BASES]) for sc in SC}
# ---- H′: m の受益・到達確率
b_o_n1 = Jg['N1:O-Ncold']['base']; H = {'m12': pw(b_o_n1, b_o_n1 + 0.09, 0.05 / 12), 'm24': pw(b_o_n1, b_o_n1 + 0.09, 0.05 / 24), 'm36': pw(b_o_n1, b_o_n1 + 0.09, 0.05 / 36)}
b_o_s1 = Jg['S1:O-Ncold']['base']; pass_s1 = 1 - single(b_o_s1) * single(b_o_s1 + 0.09); H['reach_S1_O_up9'] = pass_s1 * pw(b_o_s1, b_o_s1 + 0.09, A); H['reach_S1_O_up9_rep'] = pass_s1 * pw(b_o_s1, b_o_s1 + 0.09, A) ** 2
# ---- G′: 両側門の誤判率（二項・M と同型・参考の検出力は α=0.05/24）
def both_le(p1, p2, t):
    return float(binom.cdf(t, pn, p1) * binom.cdf(t, pn, p2))
Gp = {'reject_0.02_0.11_le1': both_le(0.02, 0.11, 1), 'null_0.02_0.04_le1': both_le(0.02, 0.04, 1), 'null_0.02_0.02_le1': both_le(0.02, 0.02, 1), 'power_0.02_0.11': pw(0.02, 0.11, A), 'power_0.02_0.04': pw(0.02, 0.04, A), 'reject_0.98_0.89_ge39': float(binom.sf(38, pn, 0.98) * binom.sf(38, pn, 0.89))}
# ---- E′: 撤退条件（パイロット帯ごと・本走行 5 pt）
E = {'pilot': {}, 'pilot_5pt_would_be': {}, 'main_5pt': {}}
cal = CT['pilot']['calibration']; b = cal['base']
E['pilot']['%s:%s' % (cal['scenario'], cal['arm'])] = {'band_pt': cal['band_pt'], 'bounds': (cal['fire_if_le'], cal['fire_if_ge']), 'null': float(binom.cdf(cal['fire_if_le'], pn, b)), 'alt': {p: float(binom.cdf(cal['fire_if_le'], pn, p)) for p in (0.92, 0.90, 0.85, 0.80)}}
def fire_prob(p, le, ge, nn):
    return float((binom.cdf(le, nn, p) if le is not None else 0.0) + (binom.sf(ge - 1, nn, p) if ge is not None else 0.0))
for m in CT['pilot']['mid']:
    p = m['base']; key = '%s:%s' % (m['scenario'], m['arm'])
    E['pilot'][key] = {'band_pt': m['band_pt'], 'bounds': (m['fire_if_le'], m['fire_if_ge']), 'null': fire_prob(p, m['fire_if_le'], m['fire_if_ge'], pn), 'alt': {('%+d' % d): fire_prob(min(max(p + d / 100, 0), 1), m['fire_if_le'], m['fire_if_ge'], pn) for d in (-20, -15, 15, 20)}}
    le5 = math.floor((p - 0.05) * pn + 1e-9) if p - 0.05 > 0 else None; ge5 = math.ceil((p + 0.05) * pn - 1e-9)
    E['pilot_5pt_would_be'][key] = fire_prob(p, le5, ge5, pn)
for sc in SC:
    for bb in BASES:
        r = CT['main_5pt'][sc][bb]; p = r['base']; key = '%s:%s' % (sc, bb)
        E['main_5pt'][key] = {'bounds': (r['fire_if_le'], r['fire_if_ge']), 'null': fire_prob(p, r['fire_if_le'], r['fire_if_ge'], n), 'sens_5pt': fire_prob(min(max(p + (0.05 if p < 0.5 else -0.05), 0), 1), r['fire_if_le'], r['fire_if_ge'], n), 'sens_10pt': fire_prob(min(max(p + (0.10 if p < 0.5 else -0.10), 0), 1), r['fire_if_le'], r['fire_if_ge'], n)}
# ---- K′: 様式門
def pass_prob(pa, pb, thr_trials):
    xa = binom.pmf(np.arange(n + 1), n, pa); tot = 0.0
    for i in range(n + 1):
        lo = max(0, i - thr_trials); hi = min(n, i + thr_trials)
        tot += xa[i] * (binom.cdf(hi, n, pb) - (binom.cdf(lo - 1, n, pb) if lo > 0 else 0))
    return float(tot)
S = T['style_gate']; K = {'catch_30pt': 1 - pass_prob(0.95, 0.65, S['strict_greater_trials']), 'catch_35pt': 1 - pass_prob(0.95, 0.60, S['strict_greater_trials']), 'catch_25pt': 1 - pass_prob(0.95, 0.70, S['strict_greater_trials']), 'catch_20pt': 1 - pass_prob(0.95, 0.75, S['strict_greater_trials'])}
# ---- M′: drift（(i)＝main_5pt と同一の整数境界・(iii) 走行間 10 pt）
DR = dfams['F_desc_drift']['constraints']; thr10 = int(round(DR['between_runs_pt'] / 100 * n))
def two_arm(p1, p2, nn, thr):
    x = binom.pmf(np.arange(nn + 1), nn, p1); tot = 0.0
    for i in range(nn + 1):
        tot += x[i] * (binom.cdf(i - thr, nn, p2) + binom.sf(i + thr - 1, nn, p2))
    return float(tot)
Mp = {'between_runs_null': {key: two_arm(v['base'], v['base'], n, thr10) for key, v in ((k, CT['main_5pt'][k.split(':')[0]][k.split(':')[1]]) for k in E['main_5pt'])}, 'between_runs_power_10pt': two_arm(0.40, 0.50, n, thr10), 'between_runs_power_15pt': two_arm(0.40, 0.55, n, thr10)}
# ---- N′: 添え札
N_BASES = [0.05, 0.20, 0.50, 0.80, 0.00, 0.11, 0.26, 0.95, 0.98, 0.99]; N_DELTAS = [0.02, 0.03, 0.05, 0.10, 0.20, 0.30]
Np = {'capture': {}, 'false_up': {}, 'thresholds': {}, 'p_k': {}, 'struct': {}}
for b in N_BASES:
    Np['capture'][b] = {d: (p_sig_higher(b + d, b) if b + d <= 1.0 else None) for d in N_DELTAS}
for b in (0.05, 0.20, 0.50, 0.80, 0.95):
    Np['false_up'][b] = p_sig_higher(b, b)
p0 = MT['null_rate_per_contrast_nominal']
for mp in (24, 21, 18, 15, 12, 9, 6, 3):
    Np['thresholds'][mp] = next(t for t in range(mp + 1) if binom.sf(t, mp, p0) <= 0.05)
Np['p_k'] = {k: float(binom.sf(k - 1, 24, p0)) for k in (1, 2, 3)}
Np['struct'] = {'up_from_%.3f' % b: p_sig_higher(1.0, b) for b in (0.98, 0.99, 0.995)}; Np['struct'].update({'down_from_%.3f' % b: p_sig_higher(b, 0.0) for b in (0.02, 0.01, 0.005)})
Np['power_mid020_up5'] = Np['capture'][0.20][0.05]
# ---- 全組合せ表
CB = T['combo_table']; combo = {'rows': CB['n_rows'], 'feasible': CB['n_feasible'], 'infeasible': CB['n_rows'] - CB['n_feasible']}
facts = {'contrasts_version': T['version'], 'when': datetime.date.today().isoformat(), 'arms': len(arms), 'n_per_arm': n, 'pilot_n': pn, 'trials_run': t_run, 'trials_two_runs': 2 * t_run, 'trials_pilot': t_pilot, 'trials_total': t_total,
         'hours_total_wall': hrs(t_total), 'hours_total_work': whrs(t_total), 'usd_total': usd(t_total), 'hours_run_wall': hrs(t_run), 'usd_run': usd(t_run), 'hours_pilot_wall': hrs(t_pilot), 'usd_pilot': usd(t_pilot),
         'confirmatory': conf_n, 'descriptive': desc_n, 'descriptive_by_family': {f: len(F['contrasts']) for f, F in dfams.items()}, 'measured_base': measured, 'duplicate_ids': dup, 'arms_without_contrast': unlinked, 'arms_string_sha16': sha(s_pre), 'arms_string_len': len(s_pre), 'runs_registered': 12, 'seeds': T['seeds'], 'tags': T['tags'],
         'alpha': A, 'I': I, 'I_bands': IB, 'J': Jg, 'J_max_reject_alt9': max_rej9, 'J_max_reject_alt15': max_rej15, 'cross_scene_judgeable3_null': cross_scene, 'cross_base_judgeable3_null': cross_base, 'H': H, 'G': Gp, 'E': E, 'K': K, 'M': Mp, 'N': Np, 'combo': combo, 'fwer_boole': 0.05}
f3 = lambda v: '—' if v is None else '%.3f' % v
out = ['# 段階 F 設計事実（機械生成・contrasts %s・%s）' % (T['version'], facts['when']), '',
       '**転記行 A（規模）**: %d 場面 × %d 腕 × %d ＝ %s 試行／走行。反復走行で %s。パイロット %d/腕 ＝ %s 試行。**総計 %s 試行**。M 実績比（%s 試行＝壁時計 %.2f 時間・実働 %.2f 時間・約 %.1f ドル・試行数比例の目安）で 1 走行 %.1f 時間・%.2f ドル、パイロット %.1f 時間・%.2f ドル、**総計 壁時計 %.1f 時間（実働比 %.1f 時間）・約 %.2f ドル**。F の腕は M の平均（長文 system 腕を含む）より短く入力側は上限側の見積り。' % (len(SC), len(arms), n, format(t_run, ','), format(2 * t_run, ','), pn, format(t_pilot, ','), format(t_total, ','), format(M_TRIALS, ','), M_WALL_H, M_WORK_H, M_USD, hrs(t_run), usd(t_run), hrs(t_pilot), usd(t_pilot), hrs(t_total), whrs(t_total), usd(t_total)),
       '**転記行 B（対比）**: 確証 %d 本（F m=%d）・記述 %d 本（%s）・id は全族を通じて一意（重複 %d）・登録された対比を持たない腕 %d。引数文字列: %d 腕・%d 字・SHA16 %s（12 走行＝パイロット 4・第一 4・第二 4 で共有・system 型なし）。tag: %s。seed: パイロット %s／第一 %s／第二 %s。' % (conf_n, FAMF['m'], desc_n, '・'.join('%s %d' % kv for kv in facts['descriptive_by_family'].items()), len(dup), len(unlinked), len(pre), len(s_pre), sha(s_pre), '・'.join('%s=%s' % kv for kv in T['tags'].items()), '〜'.join(str(x) for x in (min(T['seeds']['pilot'].values()), max(T['seeds']['pilot'].values()))), '〜'.join(str(x) for x in (min(T['seeds']['main1'].values()), max(T['seeds']['main1'].values()))), '〜'.join(str(x) for x in (min(T['seeds']['main2'].values()), max(T['seeds']['main2'].values())))),
       '**転記行 C′（被覆）**: 確証 %d 本のうち実測基底（M 第一走行の U 腕・同一バイト）%d 本・仮定基底 %d 本。' % (conf_n, measured, conf_n - measured),
       '**転記行 D′（FWER）**: 一族（m=%d）を α=0.05 で運転・Boole 上界 %.2f。T 対 U と T2 対 U は U 腕を共有し独立でないが Holm は任意の従属の下で FWER を保つ。' % (FAMF['m'], facts['fwer_boole']),
       '**転記行 E′（撤退条件・帯ごと・二項・整数境界は JSON continuity）**: パイロット (a) 校正腕 %s × %s（既測 %.3f・%d pt 帯・発火 ≤%d/40）の帰無発火率 %.4f／真の低下 %s。(b) 中間域（15 pt 帯）: %s。同じ中間域の腕に 5 pt 帯を課した場合の帰無発火率（採らない理由）: %s。本走行 5 pt 帯（U 腕別・12 セル・帰無発火率／真の 5 pt ずれ／10 pt ずれ）: %s。帰結は自動（新 seed で一度だけ再走・再び外れれば当該土台 × 場面の対比を記述へ降格・m 不変）。' % (cal['arm'], cal['scenario'], cal['base'], cal['band_pt'], cal['fire_if_le'], E['pilot']['%s:%s' % (cal['scenario'], cal['arm'])]['null'], '・'.join('%.2f→%.3f' % kv for kv in E['pilot']['%s:%s' % (cal['scenario'], cal['arm'])]['alt'].items()), '／'.join('%s（%.4f・≤%s／≥%s）帰無 %.3f・±15pt %s・±20pt %s' % (k, [m for m in CT['pilot']['mid'] if '%s:%s' % (m['scenario'], m['arm']) == k][0]['base'], v['bounds'][0], v['bounds'][1], v['null'], '%.3f/%.3f' % (v['alt']['-15'], v['alt']['+15']), '%.3f/%.3f' % (v['alt']['-20'], v['alt']['+20'])) for k, v in E['pilot'].items() if k != '%s:%s' % (cal['scenario'], cal['arm'])), '・'.join('%s %.3f' % kv for kv in E['pilot_5pt_would_be'].items()), '／'.join('%s（≤%s／≥%s）%.3f／%.3f／%.3f' % (k, v['bounds'][0], v['bounds'][1], v['null'], v['sens_5pt'], v['sens_10pt']) for k, v in E['main_5pt'].items())),
       '**転記行 G′（両側門の誤判率・二項・門は α を用いない・括弧内の検出力は α=0.05/24 の参考値）**: 真の対 0.02 対 0.11（n=400 検出力 %.3f）を両腕 ≤1/40 で捨てる確率 %.4f。同閾値で 0.02 対 0.04（検出力 %.3f）を捨てる確率 %.4f、0.02 対 0.02 は %.4f。天井側 0.98 対 0.89 を両腕 ≥39/40 で捨てる確率 %.4f。' % (Gp['power_0.02_0.11'], Gp['reject_0.02_0.11_le1'], Gp['power_0.02_0.04'], Gp['null_0.02_0.04_le1'], Gp['null_0.02_0.02_le1'], Gp['reject_0.98_0.89_ge39']),
       '**転記行 H′（m の受益・到達確率・同一の検出力関数）**: N1 × O-Ncold（%.4f）+9pt: m=12 %.3f／m=24 %.3f／m=36 %.3f（T2 を族に入れた代償 %.1f pt・T2 対 T を記述に置いた得 %.1f pt）。到達確率の一行: O-Ncold × S1（%.4f）に真の +9pt があるとき門を通り確証する確率 %.3f、確証かつ複製 %.3f。' % (b_o_n1, H['m12'], H['m24'], H['m36'], (H['m12'] - H['m24']) * 100, (H['m24'] - H['m36']) * 100, b_o_s1, H['reach_S1_O_up9'], H['reach_S1_O_up9_rep']),
       '**転記行 I′（検出力＝第二走行の検出力・n=400・両側 Fisher・α=0.05/24・実測基底 24 本・上下二枝）**: 床（<0.05・%d 本）+9pt %s〜%s／+5pt %s〜%s；天井（>0.95・%d 本）−9pt %s〜%s／−5pt %s〜%s；中間（%d 本）+15pt %s〜%s／+9pt %s〜%s／+5pt %s〜%s；−15pt %s〜%s／−9pt %s〜%s／−5pt %s〜%s。P(確証かつ複製)・中間 +9pt %s〜%s／+15pt %s〜%s。検出域の端の真の効果は確証しても四〜六割で ② と書かれる。対比別の全表は power-grid-F.md。' % (IB['n_floor'], f3(IB['floor_up_9'][0]), f3(IB['floor_up_9'][1]), f3(IB['floor_up_5'][0]), f3(IB['floor_up_5'][1]), IB['n_ceiling'], f3(IB['ceiling_down_9'][0]), f3(IB['ceiling_down_9'][1]), f3(IB['ceiling_down_5'][0]), f3(IB['ceiling_down_5'][1]), IB['n_mid'], f3(IB['mid_up_15'][0]), f3(IB['mid_up_15'][1]), f3(IB['mid_up_9'][0]), f3(IB['mid_up_9'][1]), f3(IB['mid_up_5'][0]), f3(IB['mid_up_5'][1]), f3(IB['mid_down_15'][0]), f3(IB['mid_down_15'][1]), f3(IB['mid_down_9'][0]), f3(IB['mid_down_9'][1]), f3(IB['mid_down_5'][0]), f3(IB['mid_down_5'][1]), f3(IB['p_conf_and_rep_mid_up9'][0]), f3(IB['p_conf_and_rep_mid_up9'][1]), f3(IB['p_conf_and_rep_mid_up15'][0]), f3(IB['p_conf_and_rep_mid_up15'][1])),
       '**転記行 J′（門の降格見込み・実測基底・n=40・両腕 ≤1/40 または ≥39/40・帰無〔両腕とも対照と同率〕）**: 判定可能の確率 ' + '／'.join('%s: %s' % (b, '・'.join('%s %.3f' % (sc, Jg['%s:%s' % (sc, b)]['judgeable_null']) for sc in SC)) for b in BASES) + '。真の ±9pt があるとき「効果があるのに門で捨てる」誤判は最大 %.3f・±15pt で %.3f。Ncold を土台に残す理由: 天井からの −5pt でも門通過 × 検出力（α=0.05/24）の同時確率は %s で、O-Ncold の −5pt（%s）より高い。同一土台で 3 場面が判定可能になる帰無確率（場面横断の一般化の前提）: %s。同一場面で 3 土台が判定可能になる帰無確率（土台横断）: %s。判定可能な断面の数は設計定数ではなく結果である。' % (max_rej9, max_rej15, '〜'.join('%.2f' % v for v in band([Jg['%s:Ncold' % sc]['joint_alt5'] for sc in SC])), '〜'.join('%.2f' % v for v in band([Jg['%s:O-Ncold' % sc]['joint_alt5'] for sc in SC])), '・'.join('%s %.3f' % kv for kv in cross_scene.items()), '・'.join('%s %.3f' % kv for kv in cross_base.items())),
       '**転記行 K′（様式門が捕まえる様式差・n=400・二項・「超」＝観測差 >%d/400）**: 真の様式差 30 pt（0.95 対 0.65）を捕まえる確率 %.3f・35 pt %.3f・25 pt %.3f・20 pt %.3f。(a) 軸は本段では不活性（U 12 セルの既測 (a)＝0.000）。O-Ncold の U 腕は既測で (b)＝0.000 のため層別は四場面とも実行不能。' % (S['strict_greater_trials'], K['catch_30pt'], K['catch_35pt'], K['catch_25pt'], K['catch_20pt']),
       '**転記行 M′（drift・帯・n=400・U 腕別）**: (i) M 第一走行から 5 pt 以上（整数境界は転記行 E′ の本走行 5 pt 帯と同一）の帰無発火率と感度は E′ に同じ。(iii) 走行間 10 pt 以上（%d/400）の帰無発火率（両走行同率・セル別）: %s／真の 10 pt 差（0.40 対 0.50）%.3f・15 pt 差 %.3f。' % (thr10, '・'.join('%s %.3f' % kv for kv in Mp['between_runs_null'].items()), Mp['between_runs_power_10pt'], Mp['between_runs_power_15pt']),
       '**転記行 N′（添え札の感度・偽上昇率・本数の閾値・構造的検出不能の境界・n=400・両側 Fisher α=%.2f・補正なし・「上昇あり」＝有意かつ処置腕が高い）**: 真の差を捕まえる確率（基底→+2/+3/+5/+10/+20/+30 pt）: %s。対比あたりの偽「上昇あり」率（同率・基底別）: %s（名目 %.2f）。判定本数 m′ に対する反証条件 (i) の閾値（k ≤ t で (i) を書く・帰無 %.2f の二項の上側 5%%）: %s。m′=24 で少なくとも 1／2／3 本が偽である確率 %.3f／%.3f／%.3f。構造的検出不能の境界: U 基底 0.98／0.99／0.995 から +∞（処置 1.000）の上昇を捕まえる確率 %.3f／%.3f／%.3f、U 基底 0.02／0.01／0.005 から −∞（処置 0.000）の低下 %.3f／%.3f／%.3f。基底 0.20 の +5pt（%.3f）の外では (i) は見逃しでありうる。' % (MT['alpha'], '／'.join('%.2f→%s' % (b, '/'.join(f3(v) for v in Np['capture'][b].values())) for b in N_BASES), '・'.join('%.2f %.4f' % kv for kv in Np['false_up'].items()), p0, p0, '・'.join('%d→%d' % kv for kv in Np['thresholds'].items()), Np['p_k'][1], Np['p_k'][2], Np['p_k'][3], Np['struct']['up_from_0.980'], Np['struct']['up_from_0.990'], Np['struct']['up_from_0.995'], Np['struct']['down_from_0.020'], Np['struct']['down_from_0.010'], Np['struct']['down_from_0.005'], Np['power_mid020_up5']),
       '**全組合せ表**: %d 行（門 3 × 検定 2 × refuse 2 × 様式 3 × 添え札 4 × 重複 2）・発火可能 %d 行・発火不能 %d 行（synth_F.py が発火可能の全行を一度ずつ以上発火させ、発火不能の行に落ちれば集計器が停止する）。' % (combo['rows'], combo['feasible'], combo['infeasible']),
       '', '## --arms（正本から生成・手打ち禁止・12 走行で共有）', '```', s_pre, '```', '',
       '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
os.makedirs(os.path.join(REPO, 'records', 'F'), exist_ok=True)
open(os.path.join(REPO, 'records', 'F', 'design-facts-F.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(facts, open(os.path.join(REPO, 'records', 'F', 'design-facts-F.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=float)
print('\n'.join(out[2:16]))
