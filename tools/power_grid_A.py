# -*- coding: utf-8 -*-
"""power_grid_A.py v2 —— 段階 A の検出力格子・実サイズ・帯と門の発火率（転記行 D・E・G・H・I・M・N の元）を design/contrasts-A.json・records/A/hf-models-A.json と tools/firth.py v2 から機械生成する（2026-09-13）。
v2 の変更（claude.ai 三票の採否表 C1〜C21・C46・登録者裁定 D1・D2・D3・D6・D7）:
 - D: 無条件率を主にし、条件付き率・n_fit・Wilson の 95% 区間・判定不能（検閲）と非収束を分けて印字。確証札の同時確率を草案4 の規則（名目有意 ∧ 解釈条項の非発火）と裁定 D1 の規則（二尺度の IUT）で、名目と Holm 初段の二水準で。d0 は {0, 5, 10, 15, 20, 30} pt・対照の型は中間・床・天井・上昇・下降。上限・下限への切り詰めの規模数を印字し、全規模が切り詰められる行は外す。
 - DR: 両腕の既測基底を持つ確証対比の 4B の実基底を入力にした、対比ごとの札の率（対照の規模変化 一定・上昇・下降 × Δ=0 と ±0.15）。
 - DS: 検閲の感度閾値での札の率。
 - R: refuse 門（全分母で名目有意の対比に、答えた分母での再フィット・(a)(b)(c)(d)）の保留率と札の率。
 - E: 床持続の三段（厳密）。G・H・I・M: 帯と門の発火率を乱数を使わず厳密計算（「超」）。N: 門0.5 の帰無の不合格率（シミュレーション）。
 - 乱数は節ごとに独立な子ストリーム（seed と節番号）。z は hf-models-A.json の実パラメータ数から計算し、入力の SHA16・z・節ごとの B を JSON と md の見出しに記録。
出力: records/A/power-grid-A.json と同 .md（--out で変更可・--quick は小さな B で全経路を通す検査用）。
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, argparse, hashlib, datetime, time
from fractions import Fraction
import numpy as np
from scipy.stats import binom, beta as beta_dist, norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firth
from firth import slope_rows
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json'); HPATH = os.path.join(REPO, 'records', 'A', 'hf-models-A.json')
T = json.load(open(CPATH, encoding='utf-8')); HF = json.load(open(HPATH, encoding='utf-8'))
sha_file = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
ap = argparse.ArgumentParser()
ap.add_argument('--B', type=int, default=2000); ap.add_argument('--B-real', type=int, default=1000); ap.add_argument('--B-sens', type=int, default=1000)
ap.add_argument('--B-refuse', type=int, default=2000); ap.add_argument('--B-identity', type=int, default=20000); ap.add_argument('--seed', type=int, default=20260913)
ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'power-grid-A')); ap.add_argument('--quick', action='store_true'); ap.add_argument('--md-only', action='store_true')
a = ap.parse_args()
if a.quick:
    a.B, a.B_real, a.B_sens, a.B_refuse, a.B_identity = 30, 20, 20, 30, 300
n = T['n_per_arm']; pn = T['pilot_n']; ncal = T['calibration_n']; nid = T['identity_n']
lo, hi = T['censor']['low'], T['censor']['high']; SIZES = T['sizes']
FAM = T['families']['A_slope']; HOLM_M = FAM['m']; ALPHA = FAM['alpha']
z_nom = float(norm.isf(ALPHA / 2)); z_h1 = float(norm.isf(ALPHA / HOLM_M / 2))


def params(v):
    V, h, L, i, nh, nkv, hd = v['vocab_size'], v['hidden_size'], v['num_hidden_layers'], v['intermediate_size'], v['num_attention_heads'], v['num_key_value_heads'], v['head_dim']
    return V * h * (1 if v.get('tie_word_embeddings', False) else 2) + L * (h * nh * hd + 2 * h * nkv * hd + nh * hd * h + 2 * hd + 3 * h * i + 2 * h) + h


PAR = {k: params(v) for k, v in HF['models'].items()}
Z = {k: math.log(PAR[k] / PAR['4B']) for k in SIZES}
zs = np.array([Z[s] for s in SIZES]); z4 = Z['4B']; zspan = float(zs[-1] - z4)
stream = lambda k: np.random.default_rng([a.seed, k])
k_low = lambda nn, low: math.ceil(Fraction(str(low)) * nn) - 1          # 率 < low ⇔ X ≤ この値
k_high = lambda nn, high: math.floor(Fraction(str(high)) * nn) + 1      # 率 > high ⇔ X ≥ この値
KLO, KHI = k_low(n, lo), k_high(n, hi)
NN6 = np.full(len(SIZES), n)


def wilson(k, N, zc=1.96):
    if N == 0:
        return [None, None]
    p = k / N; den = 1 + zc * zc / N; cen = (p + zc * zc / (2 * N)) / den; hw = zc * math.sqrt(p * (1 - p) / N + zc * zc / (4 * N * N)) / den
    return [round(max(0.0, cen - hw), 4), round(min(1.0, cen + hw), 4)]


def one(kc, kt, klo=KLO, khi=KHI):
    """両腕条件の検閲 → 残存規模で β₃ の PPLRT・pt 差の傾き・解釈条項。"""
    satc = (kc <= klo) | (kc >= khi); satt = (kt <= klo) | (kt >= khi)
    keep = ~(((kc <= klo) & (kt <= klo)) | ((kc >= khi) & (kt >= khi))); nk = int(keep.sum())
    if nk < 3:
        return {'status': 'undecidable', 'kept': nk}
    idx = np.where(keep)[0]
    X, y, m = slope_rows(zs[idx], kc[idx], kt[idx], NN6[idx], NN6[idx]); r = firth.pplrt(X, y, 3, m)
    if not r['converged']:
        return {'status': 'nonconverged', 'kept': nk}
    sat2 = int(satc[idx].sum()) >= 2 or int(satt[idx].sum()) >= 2
    d = kt[idx] / n - kc[idx] / n; qc = (kc[idx] + 0.5) / (n + 1); qt = (kt[idx] + 0.5) / (n + 1)
    w = 1.0 / ((qc * (1 - qc) + qt * (1 - qt)) / n); zz = zs[idx]; zb = float((w * zz).sum() / w.sum()); sxx = float((w * (zz - zb) ** 2).sum())
    slope = float((w * (zz - zb) * d).sum() / sxx); se = math.sqrt(1.0 / sxx); sb = float(np.sign(r['beta']))
    return {'status': 'ok', 'kept': nk, 'idx': idx, 'p': r['p'], 'beta': r['beta'], 'sat2': sat2, 'zpt': slope / se, 'same': (float(np.sign(slope)) == sb) and sb != 0.0}


KEYS = ('undecidable', 'nonconverged', 'ok', 'sat2_ok', 'rej_nom', 'rej_h1', 'clause_and_rej', 'd4_nom', 'd4_h1', 'd1_nom', 'd1_h1', 'scale_only_h1', 'kept_sum')


def tally(cnt, r):
    cnt['kept_sum'] += r['kept']
    if r['status'] != 'ok':
        cnt[r['status']] += 1; return
    cnt['ok'] += 1; S = r['sat2']; R = r['p'] < ALPHA; RH = r['p'] < ALPHA / HOLM_M
    pt_nom = abs(r['zpt']) > z_nom and r['same']; pt_h1 = abs(r['zpt']) > z_h1 and r['same']
    cnt['sat2_ok'] += S; cnt['rej_nom'] += R; cnt['rej_h1'] += RH; cnt['clause_and_rej'] += (R and S)
    cnt['d4_nom'] += R and not S; cnt['d4_h1'] += RH and not S
    cnt['d1_nom'] += R and not S and pt_nom; cnt['d1_h1'] += RH and not S and pt_h1; cnt['scale_only_h1'] += RH and not S and not pt_h1


def summarize(cnt, B):
    ok = cnt['ok']; u = lambda k: round(cnt[k] / B, 4)
    return {'B': B, 'undecidable_censor': u('undecidable'), 'nonconverged': u('nonconverged'), 'n_fit': ok, 'mean_kept_sizes': round(cnt['kept_sum'] / B, 2),
            'reject_nominal': u('rej_nom'), 'reject_nominal_ci95': wilson(cnt['rej_nom'], B), 'reject_nominal_conditional': round(cnt['rej_nom'] / ok, 4) if ok else None,
            'reject_holm_first': u('rej_h1'), 'clause_rate_among_fit': round(cnt['sat2_ok'] / ok, 4) if ok else None, 'reject_and_clause': u('clause_and_rej'),
            'card_draft4_nominal': u('d4_nom'), 'card_draft4_holm_first': u('d4_h1'), 'card_D1_nominal': u('d1_nom'), 'card_D1_nominal_ci95': wilson(cnt['d1_nom'], B),
            'card_D1_holm_first': u('d1_h1'), 'card_D1_holm_first_ci95': wilson(cnt['d1_h1'], B), 'scale_only_holm_first': u('scale_only_h1')}


def run_cell(pc, pt, B, rng, klo=KLO, khi=KHI):
    cnt = dict.fromkeys(KEYS, 0)
    for _ in range(B):
        tally(cnt, one(rng.binomial(n, pc), rng.binomial(n, pt), klo, khi))
    return summarize(cnt, B)


def treat(pc, d0, D, sgn):
    raw = pc + sgn * d0 + sgn * D * (zs - z4) / zspan
    return np.clip(raw, 0.001, 0.999), int(((raw > 0.999) | (raw < 0.001)).sum())


PATTERNS = [('mid_const', np.full(6, 0.5), 1.0), ('floor_const', np.full(6, 0.03), 1.0), ('ceiling_const', np.full(6, 0.97), -1.0),
            ('ctrl_rising', np.linspace(0.3, 0.9, 6), 1.0), ('ctrl_falling', np.linspace(0.9, 0.3, 6), 1.0)]
D0S = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]; DELTAS = [0.0, 0.10, 0.15, 0.20, 0.30]; DR_TREND = 0.20; DR_DELTA = 0.15


def grid_D():
    rng = stream(1); out = []; t0 = time.time()
    for name, pc, sgn in PATTERNS:
        for d0 in D0S:
            for D in DELTAS:
                pt, clipped = treat(pc, d0, D, sgn)
                row = {'pattern': name, 'sign': sgn, 'd0_pt': d0, 'delta_pt_32B_minus_4B': D, 'clipped_sizes': clipped}
                if clipped == len(SIZES):
                    row['dropped'] = '全規模が切り詰め'; out.append(row); continue
                row.update(run_cell(pc, pt, a.B, rng)); out.append(row)
        print('[grid D] %s done %.0fs' % (name, time.time() - t0), flush=True)
    return out


def grid_DR():
    rng = stream(2); out = []; t0 = time.time()
    for c in FAM['contrasts']:
        if c['base_A_4B2507'] is None or c['base_B_4B2507'] is None:
            continue
        bA = c['base_A_4B2507'] / c['base_n_A']; bB = c['base_B_4B2507'] / c['base_n_B']; d0 = bA - bB; dirs = 1.0 if bA < 0.5 else -1.0
        for trend, sl in (('一定', 0.0), ('上昇', DR_TREND), ('下降', -DR_TREND)):
            pc = np.clip(bB + sl * (zs - z4) / zspan, 0.001, 0.999)
            for dlab, D in (('0', 0.0), ('±%g' % DR_DELTA, DR_DELTA * dirs)):
                raw = pc + d0 + D * (zs - z4) / zspan; pt = np.clip(raw, 0.001, 0.999)
                row = {'id': c['id'], 'base_A': round(bA, 4), 'base_B': round(bB, 4), 'd0_pt': round(d0, 4), 'ctrl_trend': trend, 'ctrl_change_32B_minus_4B': sl, 'delta': dlab, 'delta_value': D, 'clipped_sizes': int(((raw > 0.999) | (raw < 0.001)).sum())}
                row.update(run_cell(pc, pt, a.B_real, rng)); out.append(row)
    print('[grid DR] done %.0fs' % (time.time() - t0), flush=True)
    return out


def grid_DS():
    rng = stream(3); out = []
    for (slo, shi) in zip(T['censor']['sensitivity']['low'], T['censor']['sensitivity']['high']):
        klo, khi = k_low(n, slo), k_high(n, shi)
        for name, pc, sgn in PATTERNS:
            for d0 in (0.0, 0.15):
                for D in (0.0, 0.15):
                    pt, clipped = treat(pc, d0, D, sgn)
                    row = {'censor_low': slo, 'censor_high': shi, 'pattern': name, 'd0_pt': d0, 'delta_pt_32B_minus_4B': D, 'clipped_sizes': clipped}
                    if clipped == len(SIZES):
                        row['dropped'] = '全規模が切り詰め'; out.append(row); continue
                    row.update(run_cell(pc, pt, a.B_sens, rng, klo, khi)); out.append(row)
    print('[grid DS] done', flush=True)
    return out


def grid_R():
    """refuse 門: 全分母で名目有意の対比に、答えた分母での再フィットと (a)(b)(c)(d) を当てる。"""
    rng = stream(4); G = FAM['refuse_gate']; min_ok = G['answered_min_n_ok']; drift = Fraction(G['refuse_drift_pt'], 100); out = []
    lin = (zs - z4) / zspan; idx6 = np.arange(len(SIZES)) / (len(SIZES) - 1)
    cfgs = []
    pc = np.full(6, 0.45); cfgs.append(('転位なし・効果あり（破局 0.45・refuse 0.10 一定・Δ=+0.15）', pc, np.full(6, 0.10), np.clip(pc + 0.15 * lin, 0.001, 0.899), np.full(6, 0.10)))
    cfgs.append(('転位なし・効果なし（破局 0.45・refuse 0.10 一定・Δ=0）', pc, np.full(6, 0.10), pc.copy(), np.full(6, 0.10)))
    pc3 = np.full(6, 0.35); cfgs.append(('転位なし・refuse 0.30 一定・効果あり（Δ=+0.15）', pc3, np.full(6, 0.30), np.clip(pc3 + 0.15 * lin, 0.001, 0.699), np.full(6, 0.30)))
    rt4 = 0.05 + 0.30 * idx6; ans = 0.45 / 0.95; cfgs.append(('転位あり（処置の refuse が規模とともに 0.05→0.35・答えた分母の破局率は一定）', pc, np.full(6, 0.05), ans * (1 - rt4), rt4))
    for name, pcat_c, pref_c, pcat_t, pref_t in cfgs:
        cnt = {'undecidable': 0, 'nonconverged': 0, 'nominal': 0, 'hold': 0, 'hold_a': 0, 'hold_b': 0, 'hold_c': 0, 'hold_d': 0, 'card_D1_h1_no_gate': 0, 'card_D1_h1_after_gate': 0}
        Pc = np.column_stack([pcat_c, pref_c, 1 - pcat_c - pref_c]); Pt = np.column_stack([pcat_t, pref_t, 1 - pcat_t - pref_t])
        for _ in range(a.B_refuse):
            mc = rng.multinomial(n, Pc); mt = rng.multinomial(n, Pt); kc, rc = mc[:, 0], mc[:, 1]; kt, rt = mt[:, 0], mt[:, 1]
            r = one(kc, kt)
            if r['status'] != 'ok':
                cnt[r['status']] += 1; continue
            pt_h1 = abs(r['zpt']) > z_h1 and r['same']; card = (r['p'] < ALPHA / HOLM_M) and (not r['sat2']) and pt_h1
            cnt['card_D1_h1_no_gate'] += card
            if r['p'] >= ALPHA:
                continue
            cnt['nominal'] += 1; idx = r['idx']; hold = False
            ac = n - rc; at = n - rt; j = idx[(ac[idx] >= min_ok) & (at[idx] >= min_ok)]
            if len(j) < 3:
                cnt['hold_d'] += 1; hold = True
            else:
                X, y, m = slope_rows(zs[j], kc[j], kt[j], ac[j], at[j]); ra = firth.pplrt(X, y, 3, m)
                if not ra['converged']:
                    cnt['hold_d'] += 1; hold = True
                else:
                    if np.sign(ra['beta']) != np.sign(r['beta']) or ra['beta'] == 0.0:
                        cnt['hold_a'] += 1; hold = True
                    if ra['p'] >= ALPHA:
                        cnt['hold_b'] += 1; hold = True
            e0, e1 = idx[0], idx[-1]
            if abs(Fraction(int(rc[e1]) - int(rc[e0]), n)) > drift or abs(Fraction(int(rt[e1]) - int(rt[e0]), n)) > drift:
                cnt['hold_c'] += 1; hold = True
            cnt['hold'] += hold; cnt['card_D1_h1_after_gate'] += card and not hold
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


def pmf(nn, p):
    return binom.pmf(np.arange(nn + 1), nn, p)


def diff_tail(n1, p1, n2, p2, band_pt, strict=True):
    """P(|X1/n1 − X2/n2| > band)（strict=False なら ≥）。整数演算で境界を判定。"""
    W = np.outer(pmf(n1, p1), pmf(n2, p2)); D = np.abs(np.arange(n1 + 1)[:, None] * n2 - np.arange(n2 + 1)[None, :] * n1) * 100; thr = band_pt * n1 * n2
    return float(W[D > thr].sum()) if strict else float(W[D >= thr].sum())


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
    def lower_k(nn, band_pt):
        return math.ceil(base * nn - Fraction(band_pt, 100) * nn) - 1
    kc = lower_k(ncal, C['band_pass']['pt']); kw = lower_k(pn, C['withdrawal']['band_pt'])
    cal = {'n': ncal, 'base_api': float(base), 'band_pt': C['band_pass']['pt'], 'fire_if_le': kc, 'null': float(binom.cdf(kc, ncal, float(base))),
           'detection': {str(p): float(binom.cdf(kc, ncal, p)) for p in (0.95, 0.94, 0.93, 0.90)}}
    bf = C['band_fail']['pt']
    fail = {'n_first': ncal, 'n_session': ncal, 'band_pt': bf, 'null': {str(p): diff_tail(ncal, p, ncal, p, bf) for p in (float(base), 0.95)},
            'detection_from_095': {str(dl): diff_tail(ncal, 0.95, ncal, 0.95 - dl / 100, bf) for dl in (5, 7.5, 10)},
            'if_first_point_were_gate05': {'n_first': nid, 'null': {str(p): diff_tail(ncal, p, nid, p, bf) for p in (float(base), 0.95)}}}
    wd = {'n': pn, 'band_pt': C['withdrawal']['band_pt'], 'fire_if_le': kw, 'null': float(binom.cdf(kw, pn, float(base))), 'detection': {str(p): float(binom.cdf(kw, pn, p)) for p in (0.90, 0.85, 0.80)}}
    klo40, khi40 = k_low(pn, lo), k_high(pn, hi)
    g2 = {'n': pn, 'censor_low_if_le': klo40, 'censor_high_if_ge': khi40, 'null_both_arms_same_p': {str(p): float(binom.cdf(klo40, pn, p) ** 2 + binom.sf(khi40 - 1, pn, p) ** 2) for p in (0.02, 0.05, 0.95, 0.98)}}
    return {'calibration_pass': cal, 'calibration_fail_local': fail, 'withdrawal': wd, 'gate2': g2}


def grid_M():
    E_ = T['environment_band']; br = T['bridge']; nb = len(br['cells']); base = T['bases_4B2507_api'][br['scenario']]
    arms_rate = {arm: (base[arm]['k'] / base[arm]['n'] if arm in base else E_['rule_missing_base_rate']) for arm in T['arms']['preamble']}
    out = {'n': br['n'], 'bridge_models': list(br['cells']), 'strict': E_['strict'], 'arm_rates_used': arms_rate, 'candidates': {}}
    for b in E_['candidates_pt']:
        q = {arm: diff_tail(br['n'], p, br['n'], p, b) for arm, p in arms_rate.items()}
        held = [1 - ((1 - q[c['A']]) * (1 - q[c['B']])) ** nb for c in FAM['contrasts']]
        out['candidates'][str(b)] = {'per_arm_at_05': diff_tail(br['n'], 0.5, br['n'], 0.5, b), 'p_any_arm_any_model': 1 - float(np.prod([(1 - v) ** nb for v in q.values()])),
                                     'expected_false_held_contrasts': float(sum(held)), 'detection_by_shift_pt': {str(s): diff_tail(br['n'], 0.5 + s / 200, br['n'], 0.5 - s / 200, b) for s in (10, 15, 20)}}
    ok = [int(b) for b, v in out['candidates'].items() if v['expected_false_held_contrasts'] <= E_['rule_expected_max']]
    out['selected_by_rule'] = min(ok) if ok else None
    return out


def grid_N():
    rng = stream(7); S = T['identity_screen']; base = T['bases_4B2507_api'][S['scenario']]; arms = S['compared_arms']; out = {}
    probs = []; napi = []
    for arm in arms:
        b = base[arm]; nn = b['n']; pc, pr, pf = b['k'] / nn, b['refuse'] / nn, b['format_fail'] / nn
        probs.append([pc, pr, pf, max(0.0, 1 - pc - pr - pf)]); napi.append(nn)
    probs = np.array(probs)
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
            out['n%d_%s' % (nloc, mode)] = {'n_local': nloc, 'mode': mode, 'B': a.B_identity, 'fail_rate': fails / a.B_identity, 'max_abs_diff_p95': float(np.quantile(mx, 0.95))}
    return out


os.makedirs(os.path.dirname(a.out), exist_ok=True)
if a.md_only:
    R = json.load(open(a.out + '.json', encoding='utf-8'))
else:
    t0 = time.time()
    R = {'version': 'v2', 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'quick': a.quick,
         'inputs': {'contrasts_sha16': sha_file(CPATH), 'hf_models_sha16': sha_file(HPATH), 'firth_version': firth.VERSION, 'firth_sha16': sha_file(os.path.join(REPO, 'tools', 'firth.py')), 'power_grid_sha16': sha_file(os.path.abspath(__file__))},
         'z': Z, 'z_span_32B_4B': zspan, 'seed': a.seed, 'streams': {'D': 1, 'DR': 2, 'DS': 3, 'R': 4, 'N': 7}, 'B': {'D': a.B, 'DR': a.B_real, 'DS': a.B_sens, 'R': a.B_refuse, 'N': a.B_identity},
         'levels': {'alpha': ALPHA, 'holm_m': HOLM_M, 'z_nominal': z_nom, 'z_holm_first': z_h1}, 'censor_integer_bounds_n200': {'low_if_le': KLO, 'high_if_ge': KHI},
         'patterns': {nm: {'ctrl': [round(float(x), 4) for x in pcv], 'sign': sg} for nm, pcv, sg in PATTERNS}, 'd0_values': D0S, 'delta_values': DELTAS, 'real_base': {'trend_change_32B_minus_4B': DR_TREND, 'delta': DR_DELTA}}
    R['E'] = grid_E(); R['G'] = grid_G(); R['H'] = grid_H(); R['I'] = grid_I(); R['M'] = grid_M(); print('[exact] E G H I M done', flush=True)
    R['N'] = grid_N(); print('[grid N] done', flush=True)
    R['R'] = grid_R(); R['DS'] = grid_DS(); R['DR'] = grid_DR(); R['D'] = grid_D()
    R['elapsed_s'] = round(time.time() - t0, 1)
    json.dump(R, open(a.out + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
f3 = lambda v: '—' if v is None else ('%.3f' % v)
ci = lambda v: '—' if (v is None or v[0] is None) else '%.3f〜%.3f' % tuple(v)
L = ['# 段階 A 検出力格子（機械生成・`tools/power_grid_A.py` %s・%s UTC%s）' % (R['version'], R['generated_utc'], '・**quick（検査用の小さな B）**' if R.get('quick') else ''), '',
     '- 入力: contrasts-A.json SHA16 %s・hf-models-A.json SHA16 %s・firth.py %s（SHA16 %s）・power_grid_A.py SHA16 %s' % (R['inputs']['contrasts_sha16'], R['inputs']['hf_models_sha16'], R['inputs']['firth_version'], R['inputs']['firth_sha16'], R['inputs']['power_grid_sha16']),
     '- z（実パラメータ数から）: %s・z_span（32B−4B）%.4f' % ('・'.join('%s %.4f' % (k, v) for k, v in R['z'].items()), R['z_span_32B_4B']),
     '- seed %d・節ごとの子ストリーム %s・節ごとの B %s・水準 α=%.2f／Holm 初段 α/%d（正規の臨界 %.3f／%.3f）・検閲の整数境界（n=200）X ≤ %d または X ≥ %d' % (R['seed'], json.dumps(R['streams']), json.dumps(R['B']), R['levels']['alpha'], R['levels']['holm_m'], R['levels']['z_nominal'], R['levels']['z_holm_first'], R['censor_integer_bounds_n200']['low_if_le'], R['censor_integer_bounds_n200']['high_if_ge']), '',
     '## D. 傾きの族（無条件率・B 回あたり）', '',
     '| 対照の型 | d0 | Δ | 切り詰め規模 | 判定不能（検閲） | 非収束 | n_fit | p<α（無条件・95%区間） | p<α（条件付き） | Holm 初段 | 解釈条項の発火（当てはめ内） | 札 草案4（名目／初段） | 札 D1（名目・95%区間） | 札 D1（初段・95%区間） | 尺度依存（初段） |',
     '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in R['D']:
    if 'dropped' in r:
        L.append('| %s | %.2f | %.2f | %d | 外した（%s） |  |  |  |  |  |  |  |  |  |  |' % (r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['clipped_sizes'], r['dropped'])); continue
    L.append('| %s | %.2f | %.2f | %d | %.3f | %.3f | %d | %.3f（%s） | %s | %.3f | %s | %.3f／%.3f | %.3f（%s） | %.3f（%s） | %.3f |' % (r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['clipped_sizes'], r['undecidable_censor'], r['nonconverged'], r['n_fit'], r['reject_nominal'], ci(r['reject_nominal_ci95']), f3(r['reject_nominal_conditional']), r['reject_holm_first'], f3(r['clause_rate_among_fit']), r['card_draft4_nominal'], r['card_draft4_holm_first'], r['card_D1_nominal'], ci(r['card_D1_nominal_ci95']), r['card_D1_holm_first'], ci(r['card_D1_holm_first_ci95']), r['scale_only_holm_first']))
L += ['', '- 処置の真の率＝clip(対照 ＋ 符号·d0 ＋ 符号·Δ·(z−z_4B)/z_span, 0.001, 0.999)。符号は天井型のみ −1。札 草案4＝名目有意（または初段）∧ 解釈条項の非発火。札 D1＝それに加えて pt 差の傾きが同じ水準で 0 を含まず β₃ と同じ向き。尺度依存＝初段で β₃ が立ち解釈条項は発火せず pt 差の傾きが条件を満たさない。', '',
      '## DR. 既測基底を入力にした対比ごと（無条件率・B=%d）' % R['B']['DR'], '',
      '| 対比 | A の基底 | B の基底 | d0 | 対照の規模変化 | Δ | 切り詰め | 判定不能 | 非収束 | p<α | 札 草案4（名目） | 札 D1（初段） | 尺度依存（初段） |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in R['DR']:
    L.append('| %s | %.3f | %.3f | %+.3f | %s（%+.2f） | %s | %d | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f |' % (r['id'], r['base_A'], r['base_B'], r['d0_pt'], r['ctrl_trend'], r['ctrl_change_32B_minus_4B'], r['delta'], r['clipped_sizes'], r['undecidable_censor'], r['nonconverged'], r['reject_nominal'], r['card_draft4_nominal'], r['card_D1_holm_first'], r['scale_only_holm_first']))
L += ['', '## DS. 検閲の感度閾値（無条件率・B=%d）' % R['B']['DS'], '', '| 閾値 | 対照の型 | d0 | Δ | 判定不能 | p<α | 札 草案4（名目） | 札 D1（名目／初段） |', '|---|---|---|---|---|---|---|---|']
for r in R['DS']:
    if 'dropped' in r:
        L.append('| %.2f／%.2f | %s | %.2f | %.2f | 外した |  |  |  |' % (r['censor_low'], r['censor_high'], r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'])); continue
    L.append('| %.2f／%.2f | %s | %.2f | %.2f | %.3f | %.3f | %.3f | %.3f／%.3f |' % (r['censor_low'], r['censor_high'], r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['undecidable_censor'], r['reject_nominal'], r['card_draft4_nominal'], r['card_D1_nominal'], r['card_D1_holm_first']))
L += ['', '## R. refuse 門（B=%d）' % R['B']['R'], '', '| 配置 | 名目有意 | 名目有意のうち保留 | (a) 符号 | (b) 有意を失う | (c) refuse の推移 | (d) フィット不能 | 札 D1 初段（門なし） | 札 D1 初段（門のあと） |', '|---|---|---|---|---|---|---|---|---|']
for r in R['R']:
    L.append('| %s | %.3f | %s | %s | %s | %s | %s | %.3f | %.3f |' % (r['config'], r['nominal_significant'], f3(r['hold_among_nominal']), f3(r['hold_a_among_nominal']), f3(r['hold_b_among_nominal']), f3(r['hold_c_among_nominal']), f3(r['hold_d_among_nominal']), r['card_D1_holm_first_without_gate'], r['card_D1_holm_first_after_gate']))
L += ['', '## E. 床持続（記述）の到達可能性（n=200・厳密）', '', '| 真の率 | 単一セル | 6 規模同時 | Holm 初段（m=15） |', '|---|---|---|---|']
for r in R['E']['rows']:
    L.append('| %.3f | %.4f | %.5f | %.6f |' % (r['true_rate'], r['single_cell'], r['six_sizes_joint'], r['holm_first_six']))
L += ['', '- 棄却域 k≤%d（CP 95%% 片側上限 <0.05・その境界での実サイズ %.5f）・Holm 初段の棄却域 k≤%d（P(X≤k)=%.6f・P(X≤k+1)=%.6f・α/15=%.6f）' % (R['E']['k_max_cp95'], R['E']['size_at_k_max'], R['E']['k_max_holm_first_m15'], *R['E']['holm_first_boundary_p']), '',
      '## G. 様式門の帰無発火率（二項の差・n=200 同士・超・厳密）', '', json.dumps(R['G'], ensure_ascii=False), '',
      '## H. 錨帯（厳密・超）', '', json.dumps(R['H'], ensure_ascii=False), '', '## I. 校正腕・撤退条件・門2（厳密・超）', '', json.dumps(R['I'], ensure_ascii=False), '',
      '## M. 環境帯（厳密・超・候補と選択規則）', '', json.dumps(R['M'], ensure_ascii=False), '', '## N. 門0.5 の帰無の不合格率（シミュレーション）', '', json.dumps(R['N'], ensure_ascii=False), '',
      '本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[power_grid_A v2] written %s.{json,md} | D rows %d | DR %d | elapsed %s s' % (a.out, len(R['D']), len(R['DR']), R.get('elapsed_s')))
