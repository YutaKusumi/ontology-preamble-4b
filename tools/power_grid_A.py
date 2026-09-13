# -*- coding: utf-8 -*-
"""power_grid_A.py v3.1 —— 段階 A の検出力格子・実サイズ・帯と門の発火率（転記行 D・E・G・H・I・M・N・O の元）を design/contrasts-A.json・records/A/hf-models-A.json と tools/confirm_A.py・tools/zaxis_A.py・tools/firth.py v2 から機械生成する（2026-09-13）。
v3.1（2026-09-13・登録者裁定 D9 の手順3・D11）: 札の率の模擬（run_cell の中身）と既測基底の行の処置の率・余地のある向きを tools/confirm_A.py v1.1 の simulate_cell・reach_treatment・reach_direction に、帯と門の厳密計算（pmf・diff_tail・lower_tail・一標本の下側の整数境界・環境帯の期待誤保留数）を tools/bands_A.py に移した（集計器の測れた効果種・門と校正帯の器と同じ関数・乱数の消費順と数値は v3 と同じ）。
v3 の変更（凍結前検分・七票の採否表 P18〜P30・登録者裁定 D10・D12・D13）:
 - 判定は tools/confirm_A.py の contrast()・refuse_gate() を import（格子と集計器が同じ関数・P3）。z は tools/zaxis_A.py。札 D1（初段）＝p* ≤ α/m（β₃ と pt 差の傾きがともに初段の水準で立ち同じ向き。裁定 D10 の p* の Holm でも初段の値は同じ）。
 - D・DR・DS・DC・DO の各行に切り詰めた規模数と真の pt 差の傾き（OLS・pt／z）を印字（P22）。条件付き率に Wilson 区間（P26）。
 - DC: 余白のある対照の型（0.3→0.8・0.8→0.3）で、尺度依存の帰無（d0>0・Δ=0）と効果あり（d0=0・Δ>0）（P22）。
 - DO: Odose1・Odosehalf 系の対比を、対照 Onull の既測と処置の仮定の基底（対照＋d0）で（P24）。
 - PS: pt 差の傾きの検定だけの実サイズ（残存規模数別・床と天井・処置が天井に近い配置・ベクトル化・向きの条件なし）（P18・P19）。
 - R: 転位あり・効果ありの配置と、Lneg の既測を基底にした効果なし・効果ありの配置を追加（P29）。
 - N: 門0.5 の検出側（P30）。I: 不合格枝の撤退条件（門0.5 の手元との二標本・D12 (b)）と上側の帯の assert（P59）。M: 真の率の置き方への依存と確証族の腕数（P28・P39）。
 - JV: 判定器の方向別の誤判定率の規模間の差の推定の幅（D13）。levels: Holm の後段の正規の臨界（P25）。
v2: 無条件率を主に・札の同時確率（草案4 の規則と裁定 D1）・実基底・感度閾値・refuse 門・厳密な帯・門0.5 の帰無の不合格率。乱数は節ごとに独立な子ストリーム（seed と節番号）。
出力: records/A/power-grid-A.json と同 .md（--out で変更可・--quick は小さな B で全経路を通す検査用）。
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, argparse, hashlib, datetime, time
from fractions import Fraction
import numpy as np
from scipy.stats import binom, beta as beta_dist, norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firth
import confirm_A
import bands_A
from zaxis_A import z_map
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json'); HPATH = os.path.join(REPO, 'records', 'A', 'hf-models-A.json')
T = json.load(open(CPATH, encoding='utf-8')); HF = json.load(open(HPATH, encoding='utf-8'))
sha_file = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
ap = argparse.ArgumentParser()
ap.add_argument('--B', type=int, default=2000); ap.add_argument('--B-real', type=int, default=1000); ap.add_argument('--B-sens', type=int, default=1000)
ap.add_argument('--B-refuse', type=int, default=2000); ap.add_argument('--B-identity', type=int, default=20000); ap.add_argument('--B-clean', type=int, default=2000)
ap.add_argument('--B-odose', type=int, default=500); ap.add_argument('--B-size', type=int, default=1000000); ap.add_argument('--seed', type=int, default=20260913)
ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'power-grid-A')); ap.add_argument('--quick', action='store_true'); ap.add_argument('--md-only', action='store_true')
a = ap.parse_args()
if a.quick:
    a.B, a.B_real, a.B_sens, a.B_refuse, a.B_identity, a.B_clean, a.B_odose, a.B_size = 30, 20, 20, 30, 300, 30, 10, 20000
n = T['n_per_arm']; pn = T['pilot_n']; ncal = T['calibration_n']; nid = T['identity_n']
lo, hi = T['censor']['low'], T['censor']['high']; SIZES = T['sizes']
FAM = T['families']['A_slope']; HOLM_M = FAM['m']; ALPHA = FAM['alpha']; RULES = confirm_A.Rules(T); PT_SCALE = FAM['confirm_rule']['pt_slope']['print_scale']
z_nom = float(norm.isf(ALPHA / 2)); z_h1 = float(norm.isf(ALPHA / HOLM_M / 2))
Z, PAR = z_map(HF)
zs = np.array([Z[s] for s in SIZES]); z4 = Z['4B']; zspan = float(zs[-1] - z4)
stream = lambda k: np.random.default_rng([a.seed, k])
k_low = lambda nn, low: math.ceil(Fraction(str(low)) * nn) - 1          # 率 < low ⇔ X ≤ この値
k_high = lambda nn, high: math.floor(Fraction(str(high)) * nn) + 1      # 率 > high ⇔ X ≥ この値
KLO, KHI = k_low(n, lo), k_high(n, hi)
NN6 = np.full(len(SIZES), n)


wilson = confirm_A.wilson


def true_slope_pt(pc, pt):
    return round(float(np.polyfit(zs, np.asarray(pt, float) - np.asarray(pc, float), 1)[0]) * PT_SCALE, 4)


KEYS = confirm_A.CARD_KEYS


def run_cell(pc, pt, B, rng, R=RULES):
    """v3.1: 札の率の模擬は confirm_A.simulate_cell（集計器の測れた効果種と同じ関数）。"""
    return confirm_A.simulate_cell(R, zs, n, pc, pt, B, rng)


def treat(pc, d0, D, sgn):
    raw = pc + sgn * d0 + sgn * D * (zs - z4) / zspan
    return np.clip(raw, 0.001, 0.999), int(((raw > 0.999) | (raw < 0.001)).sum())


PATTERNS = [('mid_const', np.full(6, 0.5), 1.0), ('floor_const', np.full(6, 0.03), 1.0), ('ceiling_const', np.full(6, 0.97), -1.0),
            ('ctrl_rising', np.linspace(0.3, 0.9, 6), 1.0), ('ctrl_falling', np.linspace(0.9, 0.3, 6), 1.0)]
PATTERNS_CLEAN = [('ctrl_rising_080', np.linspace(0.3, 0.8, 6)), ('ctrl_falling_080', np.linspace(0.8, 0.3, 6))]
D0S = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]; DELTAS = [0.0, 0.10, 0.15, 0.20, 0.30]; DR_TREND = 0.20; DR_DELTA = 0.15; DO_D0 = [0.0, 0.05, -0.05, 0.15, -0.15]


def grid_D():
    rng = stream(1); out = []; t0 = time.time()
    for name, pc, sgn in PATTERNS:
        for d0 in D0S:
            for D in DELTAS:
                pt, clipped = treat(pc, d0, D, sgn)
                row = {'pattern': name, 'sign': sgn, 'd0_pt': d0, 'delta_pt_32B_minus_4B': D, 'clipped_sizes': clipped, 'true_slope_pt': true_slope_pt(pc, pt)}
                if clipped == len(SIZES):
                    row['dropped'] = '全規模が切り詰め'; out.append(row); continue
                row.update(run_cell(pc, pt, a.B, rng)); out.append(row)
        print('[grid D] %s done %.0fs' % (name, time.time() - t0), flush=True)
    return out


def grid_DC():
    rng = stream(5); out = []; t0 = time.time()
    for name, pc in PATTERNS_CLEAN:
        for d0, D in [(0.05, 0.0), (0.10, 0.0), (0.15, 0.0), (0.0, 0.10), (0.0, 0.15)]:
            raw = pc + d0 + D * (zs - z4) / zspan; clipped = int(((raw > 0.999) | (raw < 0.001)).sum()); pt = np.clip(raw, 0.001, 0.999)
            row = {'pattern': name, 'ctrl': [round(float(x), 4) for x in pc], 'd0_pt': d0, 'delta_pt_32B_minus_4B': D, 'clipped_sizes': clipped, 'true_slope_pt': true_slope_pt(pc, pt), 'kind': 'scale_null' if D == 0 else 'effect'}
            row.update(run_cell(pc, pt, a.B_clean, rng)); out.append(row)
    print('[grid DC] done %.0fs' % (time.time() - t0), flush=True)
    return out


def dr_rows(c, bA, bB, B, rng, extra=None):
    out = []; d0 = bA - bB; dirs = confirm_A.reach_direction(bA)
    for trend, sl in (('一定', 0.0), ('上昇', DR_TREND), ('下降', -DR_TREND)):
        pc = np.clip(bB + sl * (zs - z4) / zspan, 0.001, 0.999)
        for dlab, D in (('0', 0.0), ('±%g' % DR_DELTA, DR_DELTA * dirs)):
            pt, clipped = confirm_A.reach_treatment(pc, d0, D, zs, z4, zspan)
            row = {'id': c['id'], 'base_A': round(bA, 4), 'base_B': round(bB, 4), 'd0_pt': round(d0, 4), 'ctrl_trend': trend, 'ctrl_change_32B_minus_4B': sl, 'delta': dlab, 'delta_value': D,
                   'clipped_sizes': clipped, 'true_slope_pt': true_slope_pt(pc, pt)}
            if extra:
                row.update(extra)
            row.update(run_cell(pc, pt, B, rng)); out.append(row)
    return out


def grid_DR():
    rng = stream(2); out = []; t0 = time.time()
    for c in FAM['contrasts']:
        if c['base_A_4B2507'] is None or c['base_B_4B2507'] is None:
            continue
        out += dr_rows(c, c['base_A_4B2507'] / c['base_n_A'], c['base_B_4B2507'] / c['base_n_B'], a.B_real, rng)
    print('[grid DR] done %.0fs' % (time.time() - t0), flush=True)
    return out


def grid_DO():
    rng = stream(6); out = []; t0 = time.time()
    for c in FAM['contrasts']:
        if not c['A'].startswith('Odose') or c['base_B_4B2507'] is None:
            continue
        bB = c['base_B_4B2507'] / c['base_n_B']
        for d0 in DO_D0:
            out += dr_rows(c, float(min(max(bB + d0, 0.001), 0.999)), bB, a.B_odose, rng, extra={'assumed_d0': d0, 'base_A_assumed': True})
    print('[grid DO] done %.0fs' % (time.time() - t0), flush=True)
    return out


def grid_DS():
    rng = stream(3); out = []
    for (slo, shi) in zip(T['censor']['sensitivity']['low'], T['censor']['sensitivity']['high']):
        R = confirm_A.Rules(T, censor_low=slo, censor_high=shi)
        for name, pc, sgn in PATTERNS:
            for d0 in (0.0, 0.15):
                for D in (0.0, 0.15):
                    pt, clipped = treat(pc, d0, D, sgn)
                    row = {'censor_low': slo, 'censor_high': shi, 'pattern': name, 'd0_pt': d0, 'delta_pt_32B_minus_4B': D, 'clipped_sizes': clipped, 'true_slope_pt': true_slope_pt(pc, pt)}
                    if clipped == len(SIZES):
                        row['dropped'] = '全規模が切り詰め'; out.append(row); continue
                    row.update(run_cell(pc, pt, a.B_sens, rng, R)); out.append(row)
    print('[grid DS] done', flush=True)
    return out


def sim_pt(pc, pt, B, rng, subset=None):
    tot = dict(fit=0, rn=0, rh=0, fit_nc=0, rn_nc=0, rh_nc=0); ch = 200000
    for s0 in range(0, B, ch):
        b = min(ch, B - s0); kc = rng.binomial(n, pc, size=(b, 6)); kt = rng.binomial(n, pt, size=(b, 6))
        if subset is None:
            keep = ~(((kc <= KLO) & (kt <= KLO)) | ((kc >= KHI) & (kt >= KHI)))
        else:
            keep = np.zeros((b, 6), bool); keep[:, subset] = True
        fit = keep.sum(1) >= RULES.min_sizes
        qc = (kc + RULES.cc) / (n + RULES.off); qt = (kt + RULES.cc) / (n + RULES.off); w = np.where(keep, 1.0 / ((qc * (1 - qc) + qt * (1 - qt)) / n), 0.0)
        sw = np.where(w.sum(1) > 0, w.sum(1), 1.0); zb = (w * zs[None, :]).sum(1) / sw; dz = zs[None, :] - zb[:, None]; sxx = (w * dz ** 2).sum(1); sxx = np.where(sxx > 0, sxx, 1.0)
        d = (kt - kc) / n; zt = (w * dz * d).sum(1) / sxx * np.sqrt(sxx)
        satc = ((kc <= KLO) | (kc >= KHI)) & keep; satt = ((kt <= KLO) | (kt >= KHI)) & keep; nc = fit & ~((satc.sum(1) >= RULES.clause_min) | (satt.sum(1) >= RULES.clause_min))
        rn = fit & (np.abs(zt) >= z_nom); rh = fit & (np.abs(zt) >= z_h1)
        tot['fit'] += int(fit.sum()); tot['rn'] += int(rn.sum()); tot['rh'] += int(rh.sum()); tot['fit_nc'] += int(nc.sum()); tot['rn_nc'] += int((rn & nc).sum()); tot['rh_nc'] += int((rh & nc).sum())
    return tot


def grid_PS():
    rng = stream(8); t0 = time.time(); subs = [('6', list(range(6))), ('5_no32B', [0, 1, 2, 3, 4]), ('4_to8B', [0, 1, 2, 3]), ('3_small', [0, 1, 2]), ('3_large', [3, 4, 5]), ('3_ends', [0, 2, 5])]
    mid = [('ctrl_mid_const', np.full(6, 0.5), 0.15), ('ctrl_rising_080', np.linspace(0.3, 0.8, 6), 0.15), ('ctrl_rising_060', np.linspace(0.2, 0.6, 6), 0.15), ('ctrl_rising_050', np.linspace(0.1, 0.5, 6), 0.10)]
    edge = [('floor_const_d0', np.full(6, 0.03), 0.0), ('floor_const_plus', np.full(6, 0.03), 0.05), ('ceiling_const_d0', np.full(6, 0.97), 0.0), ('near_ceiling_treat', np.linspace(0.35, 0.70, 6), 0.25)]
    rows = []
    for nm, pc, d0 in mid:
        assert np.all(pc + d0 < 0.999)
        for sn, sub in subs:
            t = sim_pt(pc, pc + d0, a.B_size, rng, sub); rows.append({'config': nm, 'ctrl': [round(float(x), 4) for x in pc], 'd0_pt': d0, 'retained': sn, 'retained_n': len(sub), 'B': a.B_size,
                                                                 'size_nominal': t['rn'] / a.B_size, 'size_holm_first': t['rh'] / a.B_size, 'ratio_nominal': t['rn'] / a.B_size / ALPHA, 'ratio_holm_first': t['rh'] / a.B_size / (ALPHA / HOLM_M)})
    for nm, pc, d0 in edge:
        t = sim_pt(pc, pc + d0, a.B_size, rng); f = max(t['fit'], 1); f2 = max(t['fit_nc'], 1)
        rows.append({'config': nm, 'ctrl': [round(float(x), 4) for x in pc], 'd0_pt': d0, 'retained': 'natural', 'B': a.B_size, 'fit_rate': t['fit'] / a.B_size, 'size_nominal': t['rn'] / a.B_size, 'size_holm_first': t['rh'] / a.B_size,
                     'size_nominal_given_fit': t['rn'] / f, 'size_holm_first_given_fit': t['rh'] / f, 'ratio_nominal_given_fit': t['rn'] / f / ALPHA, 'ratio_holm_first_given_fit': t['rh'] / f / (ALPHA / HOLM_M),
                     'fit_no_clause_rate': t['fit_nc'] / a.B_size, 'size_nominal_given_fit_no_clause': t['rn_nc'] / f2, 'size_holm_first_given_fit_no_clause': t['rh_nc'] / f2})
    print('[grid PS] done %.0fs' % (time.time() - t0), flush=True)
    return {'targets': {'nominal': ALPHA, 'holm_first': ALPHA / HOLM_M}, 'mc_halfwidth_holm_first': 1.96 * math.sqrt((ALPHA / HOLM_M) * (1 - ALPHA / HOLM_M) / a.B_size), 'rows': rows,
            'note': '真の pt 差は全規模で一定・切り詰めなし・両側・向きの条件なし。mid は残す規模を固定、edge は両腕条件の検閲を自然に掛ける。'}


def grid_R():
    """refuse 門: 全分母で名目有意の対比に、答えた分母での再フィットと (a)(b)(c)(d) を当てる（confirm_A.refuse_gate）。"""
    rng = stream(4); out = []
    lin = (zs - z4) / zspan; idx6 = np.arange(len(SIZES)) / (len(SIZES) - 1)
    cfgs = []
    pc = np.full(6, 0.45); cfgs.append(('転位なし・効果あり（破局 0.45・refuse 0.10 一定・Δ=+0.15）', pc, np.full(6, 0.10), np.clip(pc + 0.15 * lin, 0.001, 0.899), np.full(6, 0.10)))
    cfgs.append(('転位なし・効果なし（破局 0.45・refuse 0.10 一定・Δ=0）', pc, np.full(6, 0.10), pc.copy(), np.full(6, 0.10)))
    pc3 = np.full(6, 0.35); cfgs.append(('転位なし・refuse 0.30 一定・効果あり（Δ=+0.15）', pc3, np.full(6, 0.30), np.clip(pc3 + 0.15 * lin, 0.001, 0.699), np.full(6, 0.30)))
    rt4 = 0.05 + 0.30 * idx6; ans = 0.45 / 0.95; cfgs.append(('転位あり（処置の refuse が規模とともに 0.05→0.35・答えた分母の破局率は一定）', pc, np.full(6, 0.05), ans * (1 - rt4), rt4))
    cfgs.append(('転位あり・効果あり（処置の refuse 0.05→0.35・答えた分母の破局率が規模とともに Δ=+0.15）', pc, np.full(6, 0.05), np.clip(ans + 0.15 * lin, 0.001, 0.999) * (1 - rt4), rt4))
    bN1 = T['bases_4B2507_api']['N1']; lc = bN1['Onull']['k'] / bN1['Onull']['n']; lcr = bN1['Onull']['refuse'] / bN1['Onull']['n']; lt = bN1['Lneg']['k'] / bN1['Lneg']['n']; ltr = bN1['Lneg']['refuse'] / bN1['Lneg']['n']
    ansL = lt / (1 - ltr)
    cfgs.append(('Lneg の既測（N1・対照 Onull）を基底・効果なし', np.full(6, lc), np.full(6, lcr), np.full(6, lt), np.full(6, ltr)))
    cfgs.append(('Lneg の既測（N1・対照 Onull）を基底・答えた分母の破局率が規模とともに Δ=+0.15', np.full(6, lc), np.full(6, lcr), np.clip(ansL + 0.15 * lin, 0.001, 0.999) * (1 - ltr), np.full(6, ltr)))
    for name, pcat_c, pref_c, pcat_t, pref_t in cfgs:
        cnt = {'undecidable': 0, 'nonconverged': 0, 'nominal': 0, 'hold': 0, 'hold_a': 0, 'hold_b': 0, 'hold_c': 0, 'hold_d': 0, 'card_D1_h1_no_gate': 0, 'card_D1_h1_after_gate': 0}
        Pc = np.column_stack([pcat_c, pref_c, 1 - pcat_c - pref_c]); Pt = np.column_stack([pcat_t, pref_t, 1 - pcat_t - pref_t])
        assert np.all(Pc >= -1e-12) and np.all(Pt >= -1e-12), name
        for _ in range(a.B_refuse):
            mc = rng.multinomial(n, Pc); mt = rng.multinomial(n, Pt); kc, rc = mc[:, 0], mc[:, 1]; kt, rt = mt[:, 0], mt[:, 1]
            r = confirm_A.contrast(RULES, zs, kc, kt, NN6, NN6)
            if r['status'] != 'ok':
                cnt[r['status']] += 1; continue
            card = (r['p_beta'] <= ALPHA / HOLM_M) and (not r['clause']) and r['p_pt'] <= ALPHA / HOLM_M and r['same']
            cnt['card_D1_h1_no_gate'] += card
            if r['p_beta'] > ALPHA:
                continue
            cnt['nominal'] += 1; g = confirm_A.refuse_gate(RULES, zs, kc, kt, rc, rt, NN6, NN6, r)
            for x in 'abcd':
                cnt['hold_' + x] += int(x in g['reasons'])
            cnt['hold'] += g['hold']; cnt['card_D1_h1_after_gate'] += card and not g['hold']
        B = a.B_refuse; nom = cnt['nominal']
        out.append({'config': name, 'B': B, 'undecidable_censor': round(cnt['undecidable'] / B, 4), 'nonconverged': round(cnt['nonconverged'] / B, 4), 'nominal_significant': round(nom / B, 4),
                    'hold_among_nominal': round(cnt['hold'] / nom, 4) if nom else None, 'hold_a_among_nominal': round(cnt['hold_a'] / nom, 4) if nom else None, 'hold_b_among_nominal': round(cnt['hold_b'] / nom, 4) if nom else None,
                    'hold_c_among_nominal': round(cnt['hold_c'] / nom, 4) if nom else None, 'hold_d_among_nominal': round(cnt['hold_d'] / nom, 4) if nom else None,
                    'card_D1_holm_first_without_gate': round(cnt['card_D1_h1_no_gate'] / B, 4), 'card_D1_holm_first_after_gate': round(cnt['card_D1_h1_after_gate'] / B, 4)})
    print('[grid R] done', flush=True)
    return out


def grid_E():
    k4 = max(k for k in range(0, 20) if beta_dist.ppf(0.95, k + 1, n - k) < 0.05); k_h = max(k for k in range(0, 20) if binom.cdf(k, n, 0.05) < 0.05 / 15)
    rows = [{'true_rate': p, 'single_cell': round(float(binom.cdf(k4, n, p)), 4), 'six_sizes_joint': round(float(binom.cdf(k4, n, p) ** 6), 5), 'holm_first_six': round(float(binom.cdf(k_h, n, p) ** 6), 6)} for p in (0.005, 0.01, 0.02, 0.03)]
    return {'rows': rows, 'k_max_cp95': k4, 'k_max_holm_first_m15': k_h, 'size_at_k_max': round(float(binom.cdf(k4, n, 0.05)), 5), 'holm_first_boundary_p': [float(binom.cdf(k_h, n, 0.05)), float(binom.cdf(k_h + 1, n, 0.05)), 0.05 / 15]}


pmf = bands_A.pmf
diff_tail = bands_A.diff_tail
lower_tail = bands_A.lower_tail


PGRID = [0.1, 0.3, 0.5, 0.7, 0.9]


def grid_G():
    S = T['style_gate']
    return {'n': n, 'strict': S['strict'], 'bands': {str(b): {str(p): diff_tail(n, p, n, p, b) for p in PGRID} for b in (S['note_pt'], S['hold_pt'])}}


def grid_H():
    A_ = T['anchor_band']; units = len(A_['models']) * len(A_['scenarios']); out = {'n': n, 'units': units, 'strict': A_['strict'], 'registered_pt': A_['band_pt'], 'bands': {}}
    base = T['bases_4B2507_api']
    for b in (10, 12, 15):
        per_pair = {str(p): {'strict': diff_tail(n, p, n, p, b), 'ge': diff_tail(n, p, n, p, b, strict=False)} for p in PGRID}
        q = per_pair[str(A_['rule_true_rate'])]['strict']; u = 1 - (1 - q) ** len(A_['arms'])
        exp_meas = 0.0
        for sc in A_['scenarios']:
            prod = 1.0
            for arm in A_['arms']:
                bb = base[sc].get(arm); p_arm = bb['k'] / bb['n'] if bb else A_['rule_true_rate']
                prod *= 1 - diff_tail(n, p_arm, n, p_arm, b)
            exp_meas += len(A_['models']) * (1 - prod)
        det = {str(dl): diff_tail(n, 0.5 + dl / 200, n, 0.5 - dl / 200, b) for dl in (10, 14, 16, 20)}
        out['bands'][str(b)] = {'per_pair': per_pair, 'per_unit_at_05': u, 'expected_false_exclusions_at_05': units * u, 'p_any_false_exclusion_at_05': 1 - (1 - u) ** units,
                                'expected_false_exclusions_at_measured_bases': exp_meas, 'detection_by_drift_pt': det}
    ok = [int(b) for b, v in out['bands'].items() if v['expected_false_exclusions_at_05'] <= A_['rule_expected_max']]
    out['smallest_band_meeting_rule'] = min(ok) if ok else None; out['registered_meets_rule'] = out['bands'][str(A_['band_pt'])]['expected_false_exclusions_at_05'] <= A_['rule_expected_max']
    return out


def grid_I():
    C = T['calibration']; bb = T['bases_4B2507_api'][C['scenario']][C['arm']]; base = Fraction(bb['k'], bb['n'])
    upper_exceeds = base + Fraction(C['band_pass']['pt'], 100) > 1
    assert upper_exceeds, '基底＋帯が 1 を超えないなら上側の帯を置く規則に直す'

    def lower_k(nn, band_pt):
        return bands_A.lower_k(base, nn, band_pt)
    kc = lower_k(ncal, C['band_pass']['pt']); kw = lower_k(pn, C['withdrawal']['band_pt']); ref = 0.95
    cal = {'n': ncal, 'base_api': float(base), 'band_pt': C['band_pass']['pt'], 'upper_side_exceeds_rate_one': bool(upper_exceeds), 'fire_if_le': kc, 'null': float(binom.cdf(kc, ncal, float(base))),
           'detection': {str(p): float(binom.cdf(kc, ncal, p)) for p in (0.95, 0.94, 0.93, 0.90)}}
    bf = C['band_fail']['pt']
    fail = {'n_first': ncal, 'n_session': ncal, 'band_pt': bf, 'null': {str(p): diff_tail(ncal, p, ncal, p, bf) for p in (float(base), ref)},
            'detection_reference_rate': ref, 'detection_from_ref': {str(dl): diff_tail(ncal, ref, ncal, ref - dl / 100, bf) for dl in (5, 7.5, 10)},
            'if_first_point_were_gate05': {'n_first': nid, 'null': {str(p): diff_tail(ncal, p, nid, p, bf) for p in (float(base), ref)}}}
    wd = {'n': pn, 'band_pt': C['withdrawal']['band_pt'], 'fire_if_le': kw, 'null': float(binom.cdf(kw, pn, float(base))), 'detection': {str(p): float(binom.cdf(kw, pn, p)) for p in (0.90, 0.85, 0.80)}}
    wdb = C['withdrawal']['band_pt']
    wf = {'n_pilot': pn, 'n_gate05': nid, 'band_pt': wdb, 'sides': 'lower', 'null': {str(p): lower_tail(pn, p, nid, p, wdb) for p in (float(base), ref, 0.90)},
          'detection_reference_rate': ref, 'detection_from_ref': {str(s): lower_tail(pn, ref - s / 100, nid, ref, wdb) for s in (15, 20, 25)}}
    klo40, khi40 = k_low(pn, lo), k_high(pn, hi)
    g2 = {'n': pn, 'censor_low_if_le': klo40, 'censor_high_if_ge': khi40, 'null_both_arms_same_p': {str(p): float(binom.cdf(klo40, pn, p) ** 2 + binom.sf(khi40 - 1, pn, p) ** 2) for p in (0.02, 0.05, 0.95, 0.98)}}
    return {'calibration_pass': cal, 'calibration_fail_local': fail, 'withdrawal': wd, 'withdrawal_fail_branch': wf, 'gate2': g2}


def grid_M():
    E_ = T['environment_band']; br = T['bridge']; nb = len(br['cells']); base = T['bases_4B2507_api'][br['scenario']]
    arms_rate = {arm: (base[arm]['k'] / base[arm]['n'] if arm in base else E_['rule_missing_base_rate']) for arm in T['arms']['preamble']}
    fam_arms = [x for x in T['arms']['preamble'] if any(x in (c['A'], c['B']) for c in FAM['contrasts'])]
    out = {'n': br['n'], 'bridge_models': list(br['cells']), 'strict': E_['strict'], 'arm_rates_used': arms_rate, 'family_arms': fam_arms, 'candidates': {}, 'rate_dependence': []}

    def exp_held(rates, b):
        return bands_A.env_expected_held(rates, b, br['n'], FAM['contrasts'], nb)
    for b in E_['candidates_pt']:
        eh, q = exp_held(arms_rate, b)
        out['candidates'][str(b)] = {'per_arm_at_05': diff_tail(br['n'], 0.5, br['n'], 0.5, b), 'p_any_arm_any_model': 1 - float(np.prod([(1 - v) ** nb for v in q.values()])),
                                     'p_any_family_arm_any_model': 1 - float(np.prod([(1 - q[x]) ** nb for x in fam_arms])),
                                     'expected_false_held_contrasts': eh, 'detection_by_shift_pt': {str(s): diff_tail(br['n'], 0.5 + s / 200, br['n'], 0.5 - s / 200, b) for s in (10, 15, 20)}}
    for rate in (0.5, 0.35):
        out['rate_dependence'].append({'all_arms_rate': rate, 'expected_false_held_by_candidate': {str(b): exp_held({x: rate for x in arms_rate}, b)[0] for b in E_['candidates_pt']}})
    ok = [int(b) for b, v in out['candidates'].items() if v['expected_false_held_contrasts'] <= E_['rule_expected_max']]
    out['selected_by_rule'] = min(ok) if ok else None
    return out


def identity_probs():
    S = T['identity_screen']; base = T['bases_4B2507_api'][S['scenario']]; arms = S['compared_arms']
    probs = np.array([[base[x]['k'] / base[x]['n'], base[x]['refuse'] / base[x]['n'], base[x]['format_fail'] / base[x]['n'], 0.0] for x in arms]); probs[:, 3] = 1 - probs[:, :3].sum(1)
    return S, arms, probs, [base[x]['n'] for x in arms]


def grid_N():
    rng = stream(7); S, arms, probs, napi = identity_probs(); out = {}
    for nloc in sorted({80, nid}):
        for mode in ('api_fixed', 'api_resampled'):
            fails = 0; mx = []
            for _ in range(a.B_identity):
                diffs = []
                for i in range(len(arms)):
                    loc = rng.multinomial(nloc, probs[i]) / nloc
                    api = probs[i] if mode == 'api_fixed' else rng.multinomial(napi[i], probs[i]) / napi[i]
                    diffs += list(np.abs(loc[:3] - api[:3]) * 100)
                diffs = np.array(diffs); mx.append(float(diffs.max())); fails += (diffs.mean() > S['mean_pt']) or (diffs.max() > S['max_pt'])
            out['n%d_%s' % (nloc, mode)] = {'n_local': nloc, 'mode': mode, 'B': a.B_identity, 'fail_rate': fails / a.B_identity, 'max_abs_diff_p95': float(np.quantile(mx, 0.95)), 'quantile': 0.95}
    return out


def grid_N_detection():
    rng = stream(9); S, arms, probs, napi = identity_probs(); rows = []
    cases = [('N', -10), ('N', -15), ('N', -22), ('Onull', -15), ('Ncold', -15), ('Lneg', -15), ('all', 5)]
    for arm_s, shift in cases:
        rec = {'arm': arm_s, 'shift_pt': shift, 'n_local': nid, 'B': a.B_identity}
        for mode in ('api_fixed', 'api_resampled'):
            diffs = []
            for i, x in enumerate(arms):
                pl = probs[i].copy()
                if arm_s == x or (arm_s == 'all' and pl[3] >= shift / 100 and pl[0] + shift / 100 <= 1):
                    s_ = shift / 100.0; pl[0] += s_; pl[3] -= s_
                    if pl[3] < 0:
                        pl[1] += pl[3]; pl[3] = 0.0
                loc = rng.multinomial(nid, pl, size=a.B_identity) / nid
                api = np.broadcast_to(probs[i], (a.B_identity, 4)) if mode == 'api_fixed' else rng.multinomial(napi[i], probs[i], size=a.B_identity) / napi[i]
                diffs.append(np.abs(loc[:, :3] - api[:, :3]) * 100)
            Dm = np.concatenate(diffs, axis=1); rec['fail_rate_' + mode] = float(((Dm.mean(1) > S['mean_pt']) | (Dm.max(1) > S['max_pt'])).mean())
        rows.append(rec)
    return {'rows': rows, 'note': '破局率のずれは「その他の答え」の欄との間で動かす（refuse・書式外は動かさない・その他が足りなければ refuse から）'}


def grid_JV():
    J = T['judge_validity']; ncell = J['n_per_cell']; nsc = len(T['scenarios']); rows = []
    for share in (0.25, 0.5):
        ncls = ncell * nsc * share
        for e in (0.05, 0.10, 0.20):
            rows.append({'class_share': share, 'n_class_per_size': ncls, 'true_error_rate': e, 'diff_halfwidth95_pt': 100 * 1.96 * math.sqrt(2 * e * (1 - e) / ncls)})
    return {'n_per_cell': ncell, 'scenarios': nsc, 'rows': rows, 'method': '二規模の方向別の誤判定率の差の 95% 半幅（正規近似・場面を合わせる・機械ラベルの類の割合 class_share）'}


os.makedirs(os.path.dirname(a.out), exist_ok=True)
if a.md_only:
    R = json.load(open(a.out + '.json', encoding='utf-8'))
else:
    t0 = time.time()
    R = {'version': 'v3.1', 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'quick': a.quick,
         'inputs': {'contrasts_sha16': sha_file(CPATH), 'hf_models_sha16': sha_file(HPATH), 'firth_version': firth.VERSION, 'firth_sha16': sha_file(os.path.join(REPO, 'tools', 'firth.py')),
                    'confirm_version': confirm_A.VERSION, 'confirm_sha16': sha_file(os.path.join(REPO, 'tools', 'confirm_A.py')), 'zaxis_sha16': sha_file(os.path.join(REPO, 'tools', 'zaxis_A.py')), 'bands_sha16': sha_file(os.path.join(REPO, 'tools', 'bands_A.py')), 'power_grid_sha16': sha_file(os.path.abspath(__file__))},
         'z': {k: Z[k] for k in SIZES}, 'z_span_32B_4B': zspan, 'seed': a.seed, 'streams': {'D': 1, 'DR': 2, 'DS': 3, 'R': 4, 'DC': 5, 'DO': 6, 'N': 7, 'PS': 8, 'N_detection': 9},
         'B': {'D': a.B, 'DR': a.B_real, 'DS': a.B_sens, 'R': a.B_refuse, 'N': a.B_identity, 'DC': a.B_clean, 'DO': a.B_odose, 'PS': a.B_size},
         'levels': {'alpha': ALPHA, 'holm_m': HOLM_M, 'z_nominal': z_nom, 'z_holm_first': z_h1, 'holm_later': [{'step_denominator': j, 'z': float(norm.isf(ALPHA / j / 2))} for j in (HOLM_M, HOLM_M - 1, HOLM_M - 4, HOLM_M - 9, HOLM_M - 19, 2, 1)]},
         'censor_integer_bounds_n200': {'low_if_le': KLO, 'high_if_ge': KHI},
         'patterns': {nm: {'ctrl': [round(float(x), 4) for x in pcv], 'sign': sg} for nm, pcv, sg in PATTERNS}, 'patterns_clean': {nm: [round(float(x), 4) for x in pcv] for nm, pcv in PATTERNS_CLEAN},
         'd0_values': D0S, 'delta_values': DELTAS, 'real_base': {'trend_change_32B_minus_4B': DR_TREND, 'delta': DR_DELTA}, 'odose_assumed_d0': DO_D0}
    R['E'] = grid_E(); R['G'] = grid_G(); R['H'] = grid_H(); R['I'] = grid_I(); R['M'] = grid_M(); R['JV'] = grid_JV(); print('[exact] E G H I M JV done', flush=True)
    R['N'] = grid_N(); R['N_detection'] = grid_N_detection(); print('[grid N] done', flush=True)
    R['PS'] = grid_PS(); R['R'] = grid_R(); R['DS'] = grid_DS(); R['DR'] = grid_DR(); R['DC'] = grid_DC(); R['DO'] = grid_DO(); R['D'] = grid_D()
    R['elapsed_s'] = round(time.time() - t0, 1)
    json.dump(R, open(a.out + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
f3 = lambda v: '—' if v is None else ('%.3f' % v)
ci = lambda v: '—' if (v is None or v[0] is None) else '%.3f〜%.3f' % tuple(v)
L = ['# 段階 A 検出力格子（機械生成・`tools/power_grid_A.py` %s・%s UTC%s）' % (R['version'], R['generated_utc'], '・**quick（検査用の小さな B）**' if R.get('quick') else ''), '',
     '- 入力: contrasts-A.json SHA16 %s・hf-models-A.json SHA16 %s・firth.py %s（SHA16 %s）・confirm_A.py %s（SHA16 %s）・zaxis_A.py SHA16 %s・power_grid_A.py SHA16 %s・bands_A.py SHA16 %s' % (
         R['inputs']['contrasts_sha16'], R['inputs']['hf_models_sha16'], R['inputs']['firth_version'], R['inputs']['firth_sha16'], R['inputs']['confirm_version'], R['inputs']['confirm_sha16'], R['inputs']['zaxis_sha16'], R['inputs']['power_grid_sha16'], R['inputs'].get('bands_sha16')),
     '- z（実パラメータ数から）: %s・z_span（32B−4B）%.4f' % ('・'.join('%s %.4f' % (k, v) for k, v in R['z'].items()), R['z_span_32B_4B']),
     '- seed %d・節ごとの子ストリーム %s・節ごとの B %s・水準 α=%.2f／Holm 初段 α/%d（正規の臨界 %.4f／%.4f）・Holm の後段の臨界 %s・検閲の整数境界（n=%d）X ≤ %d または X ≥ %d' % (
         R['seed'], json.dumps(R['streams']), json.dumps(R['B']), R['levels']['alpha'], R['levels']['holm_m'], R['levels']['z_nominal'], R['levels']['z_holm_first'], '・'.join('α/%d で %.3f' % (x['step_denominator'], x['z']) for x in R['levels']['holm_later']), n, R['censor_integer_bounds_n200']['low_if_le'], R['censor_integer_bounds_n200']['high_if_ge']),
     '- 札 草案4＝名目有意（または初段）∧ 解釈条項の非発火。札 D1＝それに加えて pt 差の傾きが同じ水準で立ち β₃ と同じ向き（初段では p* ≤ α/m と同じ・登録者裁定 D10 の p* の Holm でも初段の値は同じ）。尺度依存＝初段で β₃ が立ち解釈条項は発火せず pt 差の傾きが条件を満たさない。真の pt 差の傾きは切り詰めた後の処置と対照の率の差を z に OLS で回帰した値（pt／z）。', '',
     '## D. 傾きの族（無条件率・B 回あたり）', '',
     '| 対照の型 | d0 | Δ | 切り詰め規模 | 真の pt 差の傾き | 判定不能（検閲） | 非収束 | n_fit | p<α（無条件・95%区間） | p<α（条件付き・95%区間） | Holm 初段 | 解釈条項の発火（当てはめ内） | 札 草案4（名目／初段） | 札 D1（名目・95%区間） | 札 D1（初段・95%区間） | 尺度依存（初段） |',
     '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in R['D']:
    if 'dropped' in r:
        L.append('| %s | %.2f | %.2f | %d | %+.3f | 外した（%s） |  |  |  |  |  |  |  |  |  |  |' % (r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['clipped_sizes'], r['true_slope_pt'], r['dropped'])); continue
    L.append('| %s | %.2f | %.2f | %d | %+.3f | %.3f | %.3f | %d | %.3f（%s） | %s（%s） | %.3f | %s | %.3f／%.3f | %.3f（%s） | %.3f（%s） | %.3f |' % (r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['clipped_sizes'], r['true_slope_pt'], r['undecidable_censor'], r['nonconverged'], r['n_fit'], r['reject_nominal'], ci(r['reject_nominal_ci95']), f3(r['reject_nominal_conditional']), ci(r['reject_nominal_conditional_ci95']), r['reject_holm_first'], f3(r['clause_rate_among_fit']), r['card_draft4_nominal'], r['card_draft4_holm_first'], r['card_D1_nominal'], ci(r['card_D1_nominal_ci95']), r['card_D1_holm_first'], ci(r['card_D1_holm_first_ci95']), r['scale_only_holm_first']))
L += ['', '- 処置の真の率＝clip(対照 ＋ 符号·d0 ＋ 符号·Δ·(z−z_4B)/z_span, 0.001, 0.999)。符号は天井型のみ −1。切り詰めのある行では真の pt 差は全規模で一定ではない（真の pt 差の傾きの列）。', '',
      '## DC. 余白のある対照の型（切り詰めなし・無条件率・B=%d）' % R['B']['DC'], '',
      '| 対照の型 | 種別 | d0 | Δ | 切り詰め規模 | 真の pt 差の傾き | p<α | Holm 初段 | 札 草案4（名目／初段） | 札 D1（名目／初段） | 解釈条項の発火（当てはめ内） |', '|---|---|---|---|---|---|---|---|---|---|---|']
for r in R['DC']:
    L.append('| %s | %s | %.2f | %.2f | %d | %+.3f | %.3f | %.3f | %.3f／%.3f | %.3f／%.3f | %s |' % (r['pattern'], {'scale_null': '尺度依存の帰無', 'effect': '効果あり'}[r['kind']], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['clipped_sizes'], r['true_slope_pt'], r['reject_nominal'], r['reject_holm_first'], r['card_draft4_nominal'], r['card_draft4_holm_first'], r['card_D1_nominal'], r['card_D1_holm_first'], f3(r['clause_rate_among_fit'])))
L += ['', '## DR. 既測基底を入力にした対比ごと（無条件率・B=%d）' % R['B']['DR'], '',
      '| 対比 | A の基底 | B の基底 | d0 | 対照の規模変化 | Δ | 切り詰め | 真の pt 差の傾き | 判定不能 | 非収束 | p<α | 解釈条項の発火（当てはめ内） | 札 草案4（名目／初段） | 札 D1（初段） | 尺度依存（初段） |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in R['DR']:
    L.append('| %s | %.3f | %.3f | %+.3f | %s（%+.2f） | %s | %d | %+.3f | %.3f | %.3f | %.3f | %s | %.3f／%.3f | %.3f | %.3f |' % (r['id'], r['base_A'], r['base_B'], r['d0_pt'], r['ctrl_trend'], r['ctrl_change_32B_minus_4B'], r['delta'], r['clipped_sizes'], r['true_slope_pt'], r['undecidable_censor'], r['nonconverged'], r['reject_nominal'], f3(r['clause_rate_among_fit']), r['card_draft4_nominal'], r['card_draft4_holm_first'], r['card_D1_holm_first'], r['scale_only_holm_first']))
L += ['', '## DO. Odose 系（対照 Onull の既測・処置の基底は仮定＝対照＋d0・無条件率・B=%d）' % R['B']['DO'], '',
      '| 対比 | 仮定の d0 | 処置の基底（仮定） | 対照の基底 | 対照の規模変化 | Δ | 切り詰め | 判定不能 | 解釈条項の発火（当てはめ内） | 札 D1（初段） |', '|---|---|---|---|---|---|---|---|---|---|']
for r in R['DO']:
    L.append('| %s | %+.2f | %.3f | %.3f | %s | %s | %d | %.3f | %s | %.3f |' % (r['id'], r['assumed_d0'], r['base_A'], r['base_B'], r['ctrl_trend'], r['delta'], r['clipped_sizes'], r['undecidable_censor'], f3(r['clause_rate_among_fit']), r['card_D1_holm_first']))
L += ['', '## DS. 検閲の感度閾値（無条件率・B=%d）' % R['B']['DS'], '', '| 閾値 | 対照の型 | d0 | Δ | 判定不能 | p<α | 札 草案4（名目） | 札 D1（名目／初段） |', '|---|---|---|---|---|---|---|---|']
for r in R['DS']:
    if 'dropped' in r:
        L.append('| %.2f／%.2f | %s | %.2f | %.2f | 外した |  |  |  |' % (r['censor_low'], r['censor_high'], r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'])); continue
    L.append('| %.2f／%.2f | %s | %.2f | %.2f | %.3f | %.3f | %.3f | %.3f／%.3f |' % (r['censor_low'], r['censor_high'], r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['undecidable_censor'], r['reject_nominal'], r['card_draft4_nominal'], r['card_D1_nominal'], r['card_D1_holm_first']))
PSr = R['PS']
L += ['', '## PS. pt 差の傾きの検定だけの実サイズ（B=%d・目標 名目 %.4f／初段 %.6f・初段の MC の 95%% 半幅 ±%.6f）' % (R['B']['PS'], PSr['targets']['nominal'], PSr['targets']['holm_first'], PSr['mc_halfwidth_holm_first']), '', '- ' + PSr['note'], '',
      '| 配置 | 残した規模 | 名目（比） | 初段（比） | 当てはめ可能の割合 | 当てはめ可能の中の名目（比）／初段（比） | 当てはめ可能かつ解釈条項なしの割合 | その中の名目／初段 |', '|---|---|---|---|---|---|---|---|']
for r in PSr['rows']:
    if r['retained'] == 'natural':
        L.append('| %s | 自然（検閲あり） | %.5f | %.6f | %.4f | %.4f（%.2f）／%.5f（%.2f） | %.4f | %.4f／%.5f |' % (r['config'], r['size_nominal'], r['size_holm_first'], r['fit_rate'], r['size_nominal_given_fit'], r['ratio_nominal_given_fit'], r['size_holm_first_given_fit'], r['ratio_holm_first_given_fit'], r['fit_no_clause_rate'], r['size_nominal_given_fit_no_clause'], r['size_holm_first_given_fit_no_clause']))
    else:
        L.append('| %s | %s（%d） | %.5f（%.2f） | %.6f（%.2f） | — | — | — | — |' % (r['config'], r['retained'], r['retained_n'], r['size_nominal'], r['ratio_nominal'], r['size_holm_first'], r['ratio_holm_first']))
L += ['', '## R. refuse 門（B=%d）' % R['B']['R'], '', '| 配置 | 名目有意 | 名目有意のうち保留 | (a) 符号 | (b) 有意を失う | (c) refuse の推移 | (d) フィット不能 | 札 D1 初段（門なし） | 札 D1 初段（門のあと） |', '|---|---|---|---|---|---|---|---|---|']
for r in R['R']:
    L.append('| %s | %.3f | %s | %s | %s | %s | %s | %.3f | %.3f |' % (r['config'], r['nominal_significant'], f3(r['hold_among_nominal']), f3(r['hold_a_among_nominal']), f3(r['hold_b_among_nominal']), f3(r['hold_c_among_nominal']), f3(r['hold_d_among_nominal']), r['card_D1_holm_first_without_gate'], r['card_D1_holm_first_after_gate']))
L += ['', '## E. 床持続（記述）の到達可能性（n=%d・厳密）' % n, '', '| 真の率 | 単一セル | 全規模同時 | Holm 初段（床持続のセル列の数を m とするとき） |', '|---|---|---|---|']
for r in R['E']['rows']:
    L.append('| %.3f | %.4f | %.5f | %.6f |' % (r['true_rate'], r['single_cell'], r['six_sizes_joint'], r['holm_first_six']))
L += ['', '- 棄却域 k≤%d（CP 片側上限 <0.05・その境界での実サイズ %.5f）・Holm 初段の棄却域 k≤%d（P(X≤k)=%.6f・P(X≤k+1)=%.6f・α/15=%.6f）' % (R['E']['k_max_cp95'], R['E']['size_at_k_max'], R['E']['k_max_holm_first_m15'], *R['E']['holm_first_boundary_p']), '',
      '## N. 門0.5 の帰無の不合格率と検出側（シミュレーション）', '', json.dumps(R['N'], ensure_ascii=False), '', json.dumps(R['N_detection'], ensure_ascii=False), '',
      '## G. 様式門の帰無発火率（二項の差・n=%d 同士・超・厳密）' % n, '', json.dumps(R['G'], ensure_ascii=False), '',
      '## H. 錨帯（厳密・超）', '', json.dumps(R['H'], ensure_ascii=False), '', '## I. 校正腕・撤退条件（合格枝・不合格枝）・門2（厳密・超）', '', json.dumps(R['I'], ensure_ascii=False), '',
      '## M. 環境帯（厳密・超・候補と選択規則・真の率の置き方への依存）', '', json.dumps(R['M'], ensure_ascii=False), '', '## JV. 判定器の方向別の誤判定率の規模間の差の推定の幅', '', json.dumps(R['JV'], ensure_ascii=False), '',
      '本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[power_grid_A v3.1] written %s.{json,md} | D rows %d | DR %d | DC %d | DO %d | elapsed %s s' % (a.out, len(R['D']), len(R['DR']), len(R['DC']), len(R['DO']), R.get('elapsed_s')))
