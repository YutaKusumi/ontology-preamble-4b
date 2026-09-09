# -*- coding: utf-8 -*-
"""design_facts_M.py v1 —— 追補 M の設計事実（規模・対比・被覆・費用時間・門の誤判率 G′・降格見込み J′・撤退条件の発火確率 E′・α 分割と m 拡大の受益 H′・複製の検出力 I′・様式門の帯 K′・
固有札の到達可能性 L′・drift の帰無発火率と感度 M′・§0-2 の門通過率・§2.1 の判定可能確率・引数文字列 SHA）を `design/contrasts-M.json`・台帳・格子から機械生成する。
本文（草案／凍結文書）はこの出力を転記するだけで、散文中に手計算の数を書かない。出力: records/design-facts-M.md と同 .json（上書き＝正本の現状を映す）。
費用・時間の係数は V′ 本走行の実績（83,200 試行＝17 時間 16 分・約 1.5 ドル〔登録者申告〕）の試行数比例（目安・費用はトークン数に比例し system 腕の長文分は上振れしうる）。
"""
import os, sys, json, math, hashlib, datetime
from scipy.stats import binom
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vprime_power import make_power
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8')); n = T['n_per_arm']; SC = list(T['scenarios']); G = T['gate_counts']; pn = G['pilot_n']
LV = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8')); LM = json.load(open(os.path.join(REPO, 'arms', 'panelM', 'SHA-LEDGER-M.json'), encoding='utf-8'))
pre = T['arms']['preamble']; sysa = [d['name'] for d in T['arms']['system']]; arms = pre + sysa
fams = T['families']; dfams = T['descriptive_families']
allc = [(f, c) for f, F in list(fams.items()) + list(dfams.items()) for c in F['contrasts']]; ids = [c['id'] for f, c in allc]
dup = sorted({i for i in ids if ids.count(i) > 1}); used = {c[k] for f, c in allc for k in ('A', 'B')}; unlinked = [a for a in arms if a not in used]
not_in_ledger = [a for a in pre if a != 'N' and a not in LV and a not in LM['preamble']]
for f, F in fams.items():
    assert F['m'] == len(F['contrasts']), (f, F['m'], len(F['contrasts']))
if dup or unlinked or not_in_ledger:
    print('[facts] 整合エラー: dup=%s unlinked=%s not_in_ledger=%s' % (dup, unlinked, not_in_ledger)); sys.exit(2)
# ---- A 規模（V′ 実績比）
VP_TRIALS, VP_HOURS, VP_USD = 83200, 17 + 16 / 60, 1.5
t_run = len(SC) * len(arms) * n; t_pilot = len(SC) * len(arms) * pn; t_total = 2 * t_run + t_pilot
hrs = lambda t: t * VP_HOURS / VP_TRIALS; usd = lambda t: t * VP_USD / VP_TRIALS
s_pre = ','.join(pre); s_sys = T['arms']['system_spec']; sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
conf_n = sum(F['m'] for F in fams.values()); desc_n = sum(len(F['contrasts']) for F in dfams.values())
measured = sum(1 for F in fams.values() for c in F['contrasts'] if c.get('base_B_vprime') is not None)
# ---- 検出力（両側 Fisher・全数列挙）
power = make_power(n); cache = {}
def pw(p0, p1, a):
    key = (round(p0, 4), round(min(max(p1, 0.001), 0.999), 4), round(a, 6))
    if key not in cache:
        cache[key] = power(*key)
    return cache[key]
A = {f: 0.05 / F['m'] for f, F in fams.items()}
rows_I = {}
for f, a in A.items():
    rows_I[f] = {'floor_up_9': pw(0.02, 0.11, a), 'floor_up_5': pw(0.02, 0.07, a), 'ceil97_down_9': pw(0.97, 0.88, a), 'ceil97_down_5': pw(0.97, 0.92, a), 'ceil94_down_9': pw(0.94, 0.85, a), 'ceil94_down_5': pw(0.94, 0.89, a), 'mid60_up_15': pw(0.60, 0.75, a), 'mid60_down_15': pw(0.60, 0.45, a), 'mid13_up_10': pw(0.13, 0.23, a)}
# H′: 束ね方の受益（M-a 単独族 m=16 対 m=48・m=32 時代の代償）
h = {'m16_mid_up15': pw(0.60, 0.75, 0.05 / 16), 'm16_mid_down15': pw(0.60, 0.45, 0.05 / 16), 'm16_floor_up5': pw(0.02, 0.07, 0.05 / 16), 'm32_floor_up5': pw(0.02, 0.07, 0.05 / 32), 'm32_ceil97_down5': pw(0.97, 0.92, 0.05 / 32),
     'm48_mid_up15': rows_I['M_a']['mid60_up_15'], 'm48_mid_down15': rows_I['M_a']['mid60_down_15'], 'm48_floor_up5': rows_I['M_a']['floor_up_5'], 'm48_ceil97_down5': rows_I['M_a']['ceil97_down_5'],
     'mc_m16_floor_up5': pw(0.02, 0.07, 0.05 / 16), 'mc_m24_floor_up5': rows_I['M_c']['floor_up_5'], 'rep_mk6_floor_up5': pw(0.02, 0.07, 0.05 / 6)}
# G′: 両側門の誤判率（二項）
def both_le(p1, p2, t):
    return binom.cdf(t, pn, p1) * binom.cdf(t, pn, p2)
g = {'thr': G['both_floor_max'], 'reject_0.02_0.11_le6': both_le(0.02, 0.11, 6), 'le2': both_le(0.02, 0.11, 2), 'le1': both_le(0.02, 0.11, 1), 'null_0.02_0.04_le1': both_le(0.02, 0.04, 1), 'null_0.02_0.02_le1': both_le(0.02, 0.02, 1), 'power_0.02_0.11': rows_I['M_a']['floor_up_9'], 'power_0.02_0.04': pw(0.02, 0.04, A['M_a'])}
# J′: 降格見込み（実測基底・帰無／対立）
NK = {sc: T['scenarios'][sc]['vprime_stageVp']['Nk-Ncold'] / 400 for sc in SC}
def gate_prob_single(p):
    return binom.cdf(G['both_floor_max'], pn, p) if p < 0.5 else binom.sf(G['both_ceiling_min'] - 1, pn, p)
def gate_prob_old(p):
    return binom.cdf(6, pn, p) if p < 0.5 else binom.sf(33, pn, p)
J = {}
for sc in SC:
    b = NK[sc]; alt = min(b + 0.09, 0.999) if b < 0.5 else max(b - 0.09, 0.001)
    J[sc] = {'base': b, 'null': gate_prob_single(b) ** 2, 'alt': gate_prob_single(b) * gate_prob_single(alt), 'single_new': gate_prob_single(b), 'single_old': gate_prob_old(b)}
p3 = 1.0
for sc in ('S1', 'S4', 'SK'):
    p3 *= (1 - J[sc]['null'])
judgeable3 = (1 - J['N1']['alt']) * p3 if False else None
# 「効果が N1 にしか無い世界で判定可能が 3 以上」＝N1 が対立で通り、S1/S4/SK のうち 2 以上が帰無で通る確率
q = [1 - J[sc]['null'] for sc in ('S1', 'S4', 'SK')]
p_at_least2 = q[0] * q[1] * q[2] + q[0] * q[1] * (1 - q[2]) + q[0] * (1 - q[1]) * q[2] + (1 - q[0]) * q[1] * q[2]
judge3 = (1 - J['N1']['alt']) * p_at_least2
# E′: 撤退条件
C = T['continuity']; E = {}
E['pilot_N1_ge'] = {p: float(binom.sf(C['pilot']['N1_ge'] - 1, pn, p)) for p in (0.02, 0.05, 0.10, 0.15, 0.25)}
E['pilot_S_le'] = {p: float(binom.cdf(C['pilot']['S_le'], pn, p)) for p in (0.968, 0.94, 0.90, 0.85, 0.75)}
def two_arm(p1, p2, nn, thr):
    x = binom.pmf(np.arange(nn + 1), nn, p1); tot = 0.0
    for i in range(nn + 1):
        tot += x[i] * (binom.cdf(i - thr, nn, p2) + binom.sf(i + thr - 1, nn, p2))
    return float(tot)
E['pilot_c_null'] = {p: two_arm(p, p, pn, C['pilot_c']['diff_ge']) for p in (0.02, 0.30, 0.50, 0.80, 0.90, 0.95)}
E['pilot_c_power'] = {'20pt(0.90vs0.70)': two_arm(0.90, 0.70, pn, C['pilot_c']['diff_ge']), '30pt(0.90vs0.60)': two_arm(0.90, 0.60, pn, C['pilot_c']['diff_ge'])}
M5 = C['main_5pt']; E['main_5pt'] = {'N1': {p: float(binom.sf(M5['N1_ge'] - 1, n, p)) for p in (0.02, 0.05, 0.08)}, 'S1': {p: float(binom.cdf(M5['S1_le'], n, p)) for p in (0.968, 0.93, 0.90)}, 'S4': {p: float(binom.cdf(M5['S4_le'], n, p)) for p in (1.0, 0.97, 0.95)}, 'SK': {p: float(binom.cdf(M5['SK_le'], n, p)) for p in (0.94, 0.90, 0.85)}}
E['pilot_5pt_catch'] = float(binom.sf(math.ceil(0.07 * pn) - 1, pn, 0.07))   # n=40 で 5pt ずれ（0.02→0.07）を ≥5/40 が捕まえる確率（参考）
# K′: 様式門
def pass_prob(pa, pb, thr_trials):
    xa = binom.pmf(np.arange(n + 1), n, pa); xb = binom.pmf(np.arange(n + 1), n, pb); tot = 0.0
    for i in range(n + 1):
        lo = max(0, i - thr_trials); hi = min(n, i + thr_trials)
        tot += xa[i] * (binom.cdf(hi, n, pb) - (binom.cdf(lo - 1, n, pb) if lo > 0 else 0))
    return float(tot)
S = T['style_gate']; K = {'catch_30pt': 1 - pass_prob(0.95, 0.65, S['strict_greater_trials']), 'catch_30pt_inclusive': 1 - pass_prob(0.95, 0.65, S['strict_greater_trials'] - 1), 'catch_35pt': 1 - pass_prob(0.95, 0.60, S['strict_greater_trials']), 'catch_25pt': 1 - pass_prob(0.95, 0.70, S['strict_greater_trials']), 'catch_20pt': 1 - pass_prob(0.95, 0.75, S['strict_greater_trials'])}
# L′: 固有札の到達可能性（独立近似）
L = {'tier12_floor_up5': rows_I['M_a']['floor_up_5'] ** 2, 'tier12_floor_up9': rows_I['M_a']['floor_up_9'] ** 2, 'tier3_floor_up5': rows_I['M_a']['floor_up_5'] ** 4, 'tier3_floor_up9': rows_I['M_a']['floor_up_9'] ** 4}
# M′: drift
DR = dfams['M_desc_drift']['constraints']; thr5 = int(round(DR['vs_vprime_pt'] / 100 * n)); thr10 = int(round(DR['between_runs_pt'] / 100 * n))
def one_arm_band(p0, p, thr):
    lo = p0 * n - thr; hi = p0 * n + thr
    return float(binom.cdf(math.ceil(lo) - 1, n, p) + binom.sf(math.floor(hi), n, p))
Mp = {'vs_vprime_null': {p0: one_arm_band(p0, p0, thr5) for p0 in (0.02, 0.13, 0.24, 0.33, 0.555, 0.94, 0.968, 1.0)}, 'vs_vprime_power_5pt': one_arm_band(0.33, 0.38, thr5), 'vs_vprime_power_10pt': one_arm_band(0.33, 0.43, thr5),
      'between_runs_null': {p: two_arm(p, p, n, thr10) for p in (0.02, 0.13, 0.33, 0.56, 0.94, 0.968)}, 'between_runs_power_10pt': two_arm(0.30, 0.40, n, thr10), 'between_runs_power_15pt': two_arm(0.30, 0.45, n, thr10)}
# I′: 複製（＝第二走行の検出力）と P(確証かつ複製)
I = {f: dict(rows_I[f], p_conf_and_rep_floor_up5=rows_I[f]['floor_up_5'] ** 2) for f in fams}
facts = {'contrasts_version': T['version'], 'when': datetime.date.today().isoformat(), 'arms_preamble': len(pre), 'arms_system': len(sysa), 'arms_total': len(arms), 'n_per_arm': n, 'pilot_n': pn,
         'trials_run': t_run, 'trials_two_runs': 2 * t_run, 'trials_pilot': t_pilot, 'trials_total': t_total, 'hours_run': hrs(t_run), 'hours_two_runs': hrs(2 * t_run), 'hours_pilot': hrs(t_pilot), 'hours_total': hrs(t_total), 'usd_run': usd(t_run), 'usd_two_runs': usd(2 * t_run), 'usd_pilot': usd(t_pilot), 'usd_total': usd(t_total),
         'hours_two_runs_freeze_estimate': 2 * t_run * 23.1 / VP_TRIALS, 'usd_two_runs_freeze_estimate': 2 * t_run * 8.3 / VP_TRIALS,
         'confirmatory': conf_n, 'by_family': {f: F['m'] for f, F in fams.items()}, 'descriptive': desc_n, 'descriptive_by_family': {f: len(F['contrasts']) for f, F in dfams.items()}, 'measured_base': measured, 'assumed_base': conf_n - measured,
         'duplicate_ids': dup, 'arms_without_contrast': unlinked, 'arms_string_preamble_sha16': sha(s_pre), 'arms_string_preamble_len': len(s_pre), 'system_spec_sha16': sha(s_sys), 'system_spec_len': len(s_sys), 'runs_registered': 24,
         'alpha': A, 'power_I': I, 'H': h, 'G': g, 'J': J, 'judgeable3_if_N1_only': judge3, 'E': E, 'K': K, 'L': L, 'M': Mp, 'fwer_boole': 0.05 * len(fams)}
f1 = lambda v: '%.3f' % v; f4 = lambda v: '%.4f' % v
out = ['# 追補 M 設計事実（機械生成・contrasts %s・%s）' % (T['version'], facts['when']), '',
       '**転記行 A（規模）**: %d シナリオ × %d 腕（前置き %d＋system %d）× %d ＝ %s 試行／走行。反復走行で %s。パイロット %d/腕 ＝ %s 試行。総計 %s 試行。V′ 実績比（%s 試行＝%.2f 時間・%.1f ドル・試行数比例の目安）で 1 走行 %.1f 時間・%.2f ドル、2 走行 %.1f 時間・%.2f ドル、パイロット %.1f 時間・%.2f ドル、**総計 %.1f 時間・%.2f ドル**。凍結時概算比（V′ 23.1 時間・8.3 ドル）なら 2 走行 %.1f 時間・%.1f ドル。' % (len(SC), len(arms), len(pre), len(sysa), n, format(t_run, ','), format(2 * t_run, ','), pn, format(t_pilot, ','), format(t_total, ','), format(VP_TRIALS, ','), VP_HOURS, VP_USD, hrs(t_run), usd(t_run), hrs(2 * t_run), usd(2 * t_run), hrs(t_pilot), usd(t_pilot), hrs(t_total), usd(t_total), facts['hours_two_runs_freeze_estimate'], facts['usd_two_runs_freeze_estimate']),
       '**転記行 B（対比）**: 確証 %d 本（%s）・記述 %d 本（%s）・id は全族を通じて一意（重複 %d）・登録された対比を持たない腕 %d。引数文字列: 前置き %d 腕・%d 字・SHA16 %s／system spec %d 項・%d 字・SHA16 %s（24 走行＝パイロット 8・第一 8・第二 8 で共有）。' % (conf_n, '・'.join('%s m=%d' % kv for kv in facts['by_family'].items()), desc_n, '・'.join('%s %d' % kv for kv in facts['descriptive_by_family'].items()), len(dup), len(unlinked), len(pre), len(s_pre), sha(s_pre), len(sysa), len(s_sys), sha(s_sys)),
       '**転記行 C′（被覆）**: 確証 %d 本のうち実測基底（V′ Nk-Ncold）%d 本・仮定基底 %d 本。仮定基底の検出力は走行前に確定できず、検出域の申告に用いない。' % (conf_n, measured, conf_n - measured),
       '**転記行 D′（FWER）**: 三族（m=%s）を各 α=0.05 で独立運転・Boole 上界 %.2f。' % ('・'.join(str(F['m']) for F in fams.values()), facts['fwer_boole']),
       '**転記行 E′（撤退条件・二項）**: パイロット (a) N1 の Nk-Ncold ≥%d/40 の発火確率: %s。(b) S 系 ≤%d/40: %s。(c) |sysNone-Ncold − Ncold| ≥%d/40 の帰無発火率（両腕同率）: %s／真の 20 pt 差 %.3f・30 pt 差 %.3f。本走行 5 pt 帯（N1 ≥%d／S1 ≤%d／S4 ≤%d／SK ≤%d）: N1 %s／S1 %s／S4 %s／SK %s。パイロット n=40 が 5 pt ずれ（0.02→0.07）を ≥5/40 で捕まえる確率 %.3f。' % (C['pilot']['N1_ge'], '・'.join('%.2f→%.4f' % kv for kv in E['pilot_N1_ge'].items()), C['pilot']['S_le'], '・'.join('%.3f→%.4f' % kv for kv in E['pilot_S_le'].items()), C['pilot_c']['diff_ge'], '・'.join('%.2f→%.3f' % kv for kv in E['pilot_c_null'].items()), E['pilot_c_power']['20pt(0.90vs0.70)'], E['pilot_c_power']['30pt(0.90vs0.60)'], M5['N1_ge'], M5['S1_le'], M5['S4_le'], M5['SK_le'], '・'.join('%.2f→%.4f' % kv for kv in E['main_5pt']['N1'].items()), '・'.join('%.3f→%.4f' % kv for kv in E['main_5pt']['S1'].items()), '・'.join('%.2f→%.4f' % kv for kv in E['main_5pt']['S4'].items()), '・'.join('%.2f→%.4f' % kv for kv in E['main_5pt']['SK'].items()), E['pilot_5pt_catch']),
       '**転記行 G′（両側門の誤判率・二項・門は α を用いない・括弧内の検出力は α=0.05/48 の参考値）**: 真の対 0.02 対 0.11（n=400 検出力 %.3f）を両腕 ≤6/40 で捨てる確率 %.4f、≤2/40 で %.4f、≤1/40 で %.4f。同閾値（≤1/40）で 0.02 対 0.04（検出力 %.3f）を捨てる確率 %.4f、0.02 対 0.02 は %.4f。天井側（≥39/40）は対称。' % (g['power_0.02_0.11'], g['reject_0.02_0.11_le6'], g['le2'], g['le1'], g['power_0.02_0.04'], g['null_0.02_0.04_le1'], g['null_0.02_0.02_le1']),
       '**転記行 H′（族の束ね方と m の受益・同一の検出力関数）**: 真言 対 無意味列を単独族（m=16）に置けば中間 0.60 の +15pt %.3f／−15pt %.3f・床 +5pt %.3f、束ねた m=48 では %.3f／%.3f・%.3f（単独族は希望方向に +%.1f〜%.1f pt〔中間〕・約 %.1f pt〔床 +5pt〕）。m=32→48 の代償: 床 +5pt %.3f→%.3f・天井 0.97 −5pt %.3f→%.3f。M-c の m=16→24: 床 +5pt %.3f→%.3f。第二走行の m を k=6 に絞れば床 +5pt %.3f（m=48 の %.3f 対）。' % (h['m16_mid_up15'], h['m16_mid_down15'], h['m16_floor_up5'], h['m48_mid_up15'], h['m48_mid_down15'], h['m48_floor_up5'], (h['m16_mid_up15'] - h['m48_mid_up15']) * 100, (h['m16_mid_down15'] - h['m48_mid_down15']) * 100, (h['m16_floor_up5'] - h['m48_floor_up5']) * 100, h['m32_floor_up5'], h['m48_floor_up5'], h['m32_ceil97_down5'], h['m48_ceil97_down5'], h['mc_m16_floor_up5'], h['mc_m24_floor_up5'], h['rep_mk6_floor_up5'], h['m48_floor_up5']),
       '**転記行 I′（検出力＝第二走行の検出力・n=400・両側 Fisher）**: ' + '／'.join('%s（α=0.05/%d）床 +9pt %.3f・+5pt %.3f；天井 0.97 −9pt %.3f・−5pt %.3f；0.94 −9pt %.3f・−5pt %.3f；中間 0.60 +15pt %.3f・−15pt %.3f；0.13 +10pt %.3f；P(確証かつ複製・床 +5pt) %.3f' % (f, fams[f]['m'], I[f]['floor_up_9'], I[f]['floor_up_5'], I[f]['ceil97_down_9'], I[f]['ceil97_down_5'], I[f]['ceil94_down_9'], I[f]['ceil94_down_5'], I[f]['mid60_up_15'], I[f]['mid60_down_15'], I[f]['mid13_up_10'], I[f]['p_conf_and_rep_floor_up5']) for f in fams) + '。',
       '**転記行 J′（門の降格見込み・実測基底・帰無〔両腕とも対照と同率〕／対立〔床 +9pt・天井 −9pt〕・片腕の門通過率 新〔≤1・≥39〕／旧〔≤6・≥34〕）**: ' + '・'.join('%s（%.3f）%.3f／%.3f・片腕 %.3f／旧 %.4f' % (sc, J[sc]['base'], J[sc]['null'], J[sc]['alt'], J[sc]['single_new'], J[sc]['single_old']) for sc in SC) + '。効果が N1 にしか無い世界で判定可能が 3 以上になる確率 %.3f。' % judge3,
       '**転記行 K′（様式門が捕まえる様式差・n=400・二項・「超」＝観測差 >%d/400）**: 真の様式差 30 pt（0.95 対 0.65）を捕まえる確率 %.3f（境界を含めれば %.3f）・35 pt %.3f・25 pt %.3f・20 pt %.3f。' % (S['strict_greater_trials'], K['catch_30pt'], K['catch_30pt_inclusive'], K['catch_35pt'], K['catch_25pt'], K['catch_20pt']),
       '**転記行 L′（固有札の到達可能性・独立近似・α=0.05/48）**: 二本同向き（段 (1)(2)）床 +5pt %.3f・+9pt %.3f／四本同向き（段 (3)）%.3f・%.3f。四本は TS・TK 腕を共有し正の相関があり、独立近似は楽観にも悲観にも振りうる。' % (L['tier12_floor_up5'], L['tier12_floor_up9'], L['tier3_floor_up5'], L['tier3_floor_up9']),
       '**転記行 M′（drift・帯・n=400）**: (i) V′ 実測から 5 pt 以上（%d/400 を含む）の帰無発火率: %s／真の 5 pt ずれ %.3f・10 pt ずれ %.3f。(iii) 走行間 10 pt 以上（%d/400）の帰無発火率: %s／真の 10 pt 差 %.3f・15 pt 差 %.3f。' % (thr5, '・'.join('%.3f→%.3f' % kv for kv in Mp['vs_vprime_null'].items()), Mp['vs_vprime_power_5pt'], Mp['vs_vprime_power_10pt'], thr10, '・'.join('%.2f→%.3f' % kv for kv in Mp['between_runs_null'].items()), Mp['between_runs_power_10pt'], Mp['between_runs_power_15pt']),
       '', '## --arms（前置き型・正本から生成・手打ち禁止）', '```', s_pre, '```', '## --system-arms（system 型・--arms - と併用）', '```', s_sys, '```', '',
       '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(os.path.join(REPO, 'records', 'design-facts-M.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(facts, open(os.path.join(REPO, 'records', 'design-facts-M.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=float)
print('\n'.join(out[2:14]))
