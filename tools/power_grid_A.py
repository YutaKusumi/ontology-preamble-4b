# -*- coding: utf-8 -*-
"""power_grid_A.py v1 —— 段階 A の検出力格子と実サイズ（転記行 D・E・H・I・M の元）を `design/contrasts-A.json` と tools/firth.py から機械生成する（2026-09-13）。
D: 傾きの族 β₃（Firth PPLRT・両側）の検出力と型 I 誤りの実サイズ——二項シミュレーション（B 回・seed 凍結）。効果は「4B と 32B の間の pt 差の変化」で母数化（z は実パラメータ数の対数・design_facts_A が渡す）。
   対照の基底パターン: 中間（0.5 一定）・床（0.03 一定）・天井（0.97 一定）・対照が規模で動く（0.3→0.9）。解釈条項（いずれかの腕が 2 規模以上で飽和）の発火率も併記。
E: 床持続（記述）の到達可能性の三段（単一セル k≤4／6 規模同時／Holm 初段 k≤2・n=200・真の率 0.005/0.01/0.02/0.03）。
H: 錨帯（Onull・O-Ncold × 5 場面 × 6 規模 × 2 走行・n=200）の帰無発火率（帯 10／12／15 pt・二項の差）。
I: 校正腕（Ncold × N1 × n=400・5 pt 帯）と撤退条件（n=40・15 pt 帯）の整数境界と帰無発火率。
M: 橋のセル（n=200 × 2 環境）の環境差の帯の帰無発火率（10／12／15 pt）。
出力: records/A/power-grid-A.json（design_facts_A.py が読む）と同 .md。
"""
import os, sys, json, math, argparse
import numpy as np
from scipy.stats import binom, beta as beta_dist
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from firth import design, pplrt
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-A.json'), encoding='utf-8')); n = T['n_per_arm']; pn = T['pilot_n']; ncal = T['calibration_n']
ap = argparse.ArgumentParser(); ap.add_argument('--B', type=int, default=2000); ap.add_argument('--seed', type=int, default=20260913); ap.add_argument('--z', default=None, help='JSON: {"0.6B":z,...}（design_facts_A が実パラメータ数から渡す）'); ap.add_argument('--md-only', action='store_true', help='既存の JSON から md だけ再生成（シミュレーションを走らせない）')
a = ap.parse_args()
Z = json.loads(a.z) if a.z else {'0.6B': -1.9, '1.7B': -0.86, '4B': 0.0, '8B': 0.69, '14B': 1.25, '32B': 2.08}   # 既定は公称比の対数（実値は転記行 L で置換）
SIZES = T['sizes']; zs = np.array([Z[s] for s in SIZES]); z_span = zs[-1] - zs[2]   # 32B と 4B の z の差
rng = np.random.default_rng(a.seed)
lo, hi = T['censor']['low'], T['censor']['high']


def logit(p):
    p = min(max(p, 1e-6), 1 - 1e-6); return math.log(p / (1 - p))


def sim_once(p_ctrl, p_trt):
    """p_ctrl/p_trt: 規模ごとの真の率（長さ 6）。両腕条件の検閲→残存規模で Firth PPLRT。戻り値: (p 値 or None〔検閲で <3 規模〕, 解釈条項発火 bool, 残存規模数)"""
    kc = rng.binomial(n, p_ctrl); kt = rng.binomial(n, p_trt); rc = kc / n; rt = kt / n
    keep = ~(((rc < lo) & (rt < lo)) | ((rc > hi) & (rt > hi)))
    if keep.sum() < 3:
        return None, False, int(keep.sum())
    sat = int(((rc[keep] < lo) | (rc[keep] > hi)).sum()) >= 2 or int(((rt[keep] < lo) | (rt[keep] > hi)).sum()) >= 2
    rows_a, rows_z, rows_y = [], [], []
    for i in np.where(keep)[0]:
        rows_a += [0] * n + [1] * n; rows_z += [zs[i]] * (2 * n); rows_y += [1] * int(kc[i]) + [0] * (n - int(kc[i])) + [1] * int(kt[i]) + [0] * (n - int(kt[i]))
    X = design(rows_a, rows_z); r = pplrt(X, np.array(rows_y, float), 3)
    return (r['p'] if r['converged'] else None), sat, int(keep.sum())


def grid_D():
    """効果の母数化: 処置−対照の pt 差が 4B で d0、32B で d0+Δ（線形 in z）。対照の基底パターン別。"""
    patterns = {'mid_const': [0.5] * 6, 'floor_const': [0.03] * 6, 'ceiling_const': [0.97] * 6, 'ctrl_rising': list(np.linspace(0.3, 0.9, 6))}
    deltas = [0.0, 0.10, 0.15, 0.20, 0.30]   # 32B−4B 間の pt 差の変化（Δ）
    out = []
    for name, pc in patterns.items():
        pc = np.array(pc)
        for d0 in (0.0, 0.15):
            for D in deltas:
                pt = np.clip(pc + d0 + D * (zs - zs[2]) / z_span, 0.001, 0.999)
                ps, sats, keeps = [], 0, []
                for _ in range(a.B):
                    p, sat, k = sim_once(pc, pt); keeps.append(k)
                    if p is not None:
                        ps.append(p); sats += sat
                ps = np.array(ps)
                out.append({'pattern': name, 'd0_pt': d0, 'delta_pt_32B_minus_4B': D, 'B': a.B, 'n_fit': int(len(ps)), 'undecidable_rate': round(1 - len(ps) / a.B, 4),
                            'reject_005': round(float((ps < 0.05).mean()) if len(ps) else 0.0, 4), 'reject_holm_first': round(float((ps < 0.05 / 35).mean()) if len(ps) else 0.0, 4),
                            'interp_clause_rate': round(sats / max(len(ps), 1), 4), 'mean_kept_sizes': round(float(np.mean(keeps)), 2)})
    return out


def grid_E():
    out = []
    for p in (0.005, 0.01, 0.02, 0.03):
        c4 = binom.cdf(4, n, p); c2 = binom.cdf(2, n, p)
        out.append({'true_rate': p, 'single_cell_k_le_4': round(float(c4), 4), 'six_sizes_joint': round(float(c4 ** 6), 5), 'holm_first_stage_k_le_2': round(float(c2 ** 6), 6)})
    kmax = max(k for k in range(0, 20) if beta_dist.ppf(0.95, k + 1, n - k) < 0.05); k_holm = max(k for k in range(0, 20) if binom.cdf(k, n, 0.05) < 0.05 / 15)
    return {'rows': out, 'k_max_cp95_n200': kmax, 'k_max_holm_first_n200': k_holm, 'p_size_k_le_4': round(float(binom.cdf(4, n, 0.05)), 5)}


def null_fire_diff(nn, band_pt, ps=(0.1, 0.3, 0.5, 0.7, 0.9), B=20000):
    out = {}
    for p in ps:
        k1 = rng.binomial(nn, p, B); k2 = rng.binomial(nn, p, B); out[str(p)] = round(float((np.abs(k1 - k2) / nn >= band_pt / 100).mean()), 4)
    return out


def bounds(p, band, nn):
    lo_ = math.floor((p - band) * nn + 1e-9); hi_ = math.ceil((p + band) * nn - 1e-9)
    return {'fire_if_le': lo_ if lo_ >= 0 else None, 'fire_if_ge': hi_ if hi_ <= nn else None}


def grid_H():
    per = {str(b): null_fire_diff(n, b) for b in (10, 12, 15)}
    cells = len(T['anchor_band']['scenarios']) * len(SIZES) * 2
    return {'per_pair_null_fire': per, 'n_pairs': cells, 'expected_false_exclusions_at_p05': {b: round(v['0.5'] * cells, 2) for b, v in per.items()}}


def grid_I():
    base = T['bases_4B2507_api']['N1']['Ncold']['k'] / T['bases_4B2507_api']['N1']['Ncold']['n']
    cal = {'base_api': round(base, 4), 'n': ncal, 'band_pt': 5, **bounds(base, 0.05, ncal), 'null_fire': round(float((np.abs(rng.binomial(ncal, base, 20000) / ncal - base) >= 0.05).mean()), 4)}
    wd = {'n': pn, 'band_pt': 15, **bounds(base, 0.15, pn), 'null_fire': round(float((np.abs(rng.binomial(pn, base, 20000) / pn - base) >= 0.15).mean()), 4)}
    return {'calibration': cal, 'withdrawal_pilot': wd}


def grid_M():
    return {'per_arm_null_fire_two_env': {str(b): null_fire_diff(n, b) for b in (10, 12, 15)}, 'arms_per_bridge': len(T['arms']['preamble'])}


os.makedirs(os.path.join(REPO, 'records', 'A'), exist_ok=True)
if a.md_only:
    R = json.load(open(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'), encoding='utf-8'))
else:
    R = {'z': Z, 'z_span_32B_4B': round(float(z_span), 4), 'B': a.B, 'seed': a.seed, 'D': grid_D(), 'E': grid_E(), 'H': grid_H(), 'I': grid_I(), 'M': grid_M()}
    json.dump(R, open(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 A 検出力格子（機械生成・`tools/power_grid_A.py` v1・B=%d・seed %d）' % (R['B'], R['seed']), '', '## D. 傾きの族 β₃（Firth PPLRT 両側・n=200 × 6 規模・両腕条件の検閲後）', '',
     '| 対照の基底 | 4B の差 d0 | Δ（32B−4B の pt 差の変化） | 判定不能率（<3 規模） | p<0.05 | p<0.05/35 | 解釈条項の発火率 | 残存規模の平均 |', '|---|---|---|---|---|---|---|---|']
for r in R['D']:
    L.append('| %s | %.2f | %.2f | %.3f | %.3f | %.3f | %.3f | %.2f |' % (r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['undecidable_rate'], r['reject_005'], r['reject_holm_first'], r['interp_clause_rate'], r['mean_kept_sizes']))
L += ['', '## E. 床持続（記述）の到達可能性の三段（n=200）', '', '| 真の率 | 単一セル k≤4 | 6 規模同時 | Holm 初段 k≤2 |', '|---|---|---|---|']
for r in R['E']['rows']:
    L.append('| %.3f | %.4f | %.5f | %.6f |' % (r['true_rate'], r['single_cell_k_le_4'], r['six_sizes_joint'], r['holm_first_stage_k_le_2']))
L += ['', 'k≤%d（CP 95%% 片側上限 <0.05）・Holm 初段の k≤%d・H0 での実サイズ %.5f' % (R['E']['k_max_cp95_n200'], R['E']['k_max_holm_first_n200'], R['E']['p_size_k_le_4']),
      '', '## H. 錨帯の帰無発火率（n=200 × 2 走行・真の率別・帯 pt）', '', json.dumps(R['H'], ensure_ascii=False), '', '## I. 校正腕と撤退条件', '', json.dumps(R['I'], ensure_ascii=False), '', '## M. 橋のセルの環境差の帯', '', json.dumps(R['M'], ensure_ascii=False), '']
open(os.path.join(REPO, 'records', 'A', 'power-grid-A.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[power_grid_A] written records/A/power-grid-A.{json,md}', '| D rows', len(R['D']))
