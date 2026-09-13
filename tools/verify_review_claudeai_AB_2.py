# -*- coding: utf-8 -*-
"""verify_review_claudeai_AB_2.py v1 —— claude.ai 三票（段階 A・B 設計草案4）の追い問い 第二部（コーディネータ・2026-09-13）。
第一部（verify_review_claudeai_AB.py・V1〜V11）で出していない票の主張と、登録者裁定の材料になる数を、一次記録と独立計算で出す。
出力: records/reviews/AB/round-claudeai/verification-claudeai-AB-2.md（V12〜V26）。
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, ast, datetime
from fractions import Fraction
import numpy as np
from scipy.stats import binom, hypergeom, norm, chi2
from scipy.special import expit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from firth import design, pplrt, _fit
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(REPO, *p), encoding='utf-8'))
A = J('design', 'contrasts-A.json'); Bj = J('design', 'contrasts-B.json'); PG = J('records', 'A', 'power-grid-A.json'); HF = J('records', 'A', 'hf-models-A.json')
try:
    DB = J('records', 'B', 'design-facts-B.json')
except Exception:
    DB = None
O = ['# claude.ai 三票（草案4）の追い問い 第二部——コーディネータの独立計算（機械生成・`tools/verify_review_claudeai_AB_2.py` v1・%s UTC）' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), '',
     '- 第一部は `verification-claudeai-AB.md`（V1〜V11）。本部の節番号は第一部に続けて V12 から。', '']
P = O.append
n = 200; lo, hi = A['censor']['low'], A['censor']['high']; sizes = A['sizes']


def say(msg):
    print('[verify-2]', msg, flush=True)


# ---- 実パラメータ数と z（転記行 L と同じ式・hf-models-A.json から）
def params(v):
    V, h, L, i, nh, nkv, hd = v['vocab_size'], v['hidden_size'], v['num_hidden_layers'], v['intermediate_size'], v['num_attention_heads'], v['num_key_value_heads'], v['head_dim']
    return V * h * (1 if v.get('tie_word_embeddings', False) else 2) + L * (h * nh * hd + 2 * h * nkv * hd + nh * hd * h + 2 * hd + 3 * h * i + 2 * h) + h


PAR = {k: params(v) for k, v in HF['models'].items()}
Zr = {k: math.log(PAR[k] / PAR['4B']) for k in sizes}
zs = np.array([Zr[s] for s in sizes]); zspan = zs[-1] - zs[2]

# ---- V12 Firth の制約付き当てはめの二つの型
say('V12')
P('## V12. `tools/firth.py` の PPLRT——制約付き当てはめで罰則に全模型の情報行列を使う型（firth.py）と、列を落として縮小模型を当てはめ直す型の比較（合成データ・seed 固定）'); P('')


def pen_ll(X, y, beta):
    eta = X @ beta; mu = expit(eta); w = mu * (1 - mu); s, ld = np.linalg.slogdet(X.T @ (X * w[:, None]))
    return float(np.sum(y * eta - np.logaddexp(0.0, eta)) + 0.5 * ld)


rng = np.random.default_rng(1201)
pc_ = np.linspace(0.3, 0.9, 6); pt_ = np.clip(pc_ + 0.15, 0.001, 0.999); a_, z_, y_ = [], [], []
for i in range(6):
    kc = int(rng.binomial(n, pc_[i])); kt = int(rng.binomial(n, pt_[i]))
    a_ += [0] * n + [1] * n; z_ += [zs[i]] * (2 * n); y_ += [1] * kc + [0] * (n - kc) + [1] * kt + [0] * (n - kt)
X1 = design(a_, z_); y1 = np.array(y_, float)
rng2 = np.random.default_rng(1202); m2 = 79
x1 = rng2.binomial(1, 0.25, m2).astype(float); x2 = rng2.normal(size=m2); x3 = rng2.normal(size=m2)
y2 = np.where(x1 == 1, 1.0, rng2.binomial(1, expit(-0.8 + 0.9 * x2 - 0.5 * x3)).astype(float)); X2 = np.column_stack([np.ones(m2), x1, x2, x3])
rng3 = np.random.default_rng(1203); m3 = 239
Cm = rng3.normal(size=(m3, 4)); x5 = rng3.binomial(1, 0.08, m3).astype(float)
y3 = rng3.binomial(1, expit(-0.3 + Cm @ np.array([0.5, -0.4, 0.3, 0.0]) + 1.5 * x5)).astype(float); X3 = np.column_stack([np.ones(m3), Cm, x5])
P('| データ | 検定する列 | firth.py: 統計量／p／収束 | 縮小模型型: 統計量／p／収束 | 二つの制約解を全模型の罰則付き対数尤度で評価した差（firth.py − 縮小模型型） |'); P('|---|---|---|---|---|')
for lab, X, y, idx in (('本設計型（6 規模 × 2 腕 × 200・対照 0.3→0.9・pt 差 +0.15 一定）', X1, y1, 3), ('小標本 n=79・x1 で準分離', X2, y2, 1), ('小標本 n=79・x1 で準分離', X2, y2, 2), ('中標本 n=239・希少な二値 x5', X3, y3, 5)):
    b_f, ll_f, c_f = _fit(X, y); r = pplrt(X, y, idx); b_r, ll_r, c_r = _fit(X, y, fixed={idx: 0.0})
    Xr = np.delete(X, idx, axis=1); b_red, ll_red, c_red = _fit(Xr, y)
    st_red = max(0.0, 2 * (ll_f - ll_red)); p_red = float(chi2.sf(st_red, 1)); b_red_full = np.insert(b_red, idx, 0.0)
    P('| %s | %d | %.5f／%.5f／%s | %.5f／%.5f／%s | %+.6f |' % (lab, idx, r['stat'], r['p'], r['converged'], st_red, p_red, bool(c_f and c_red), pen_ll(X, y, b_r) - pen_ll(X, y, b_red_full)))
betas = {}; first_true = None
for mi in range(2, 120):
    b, ll, c = _fit(X1, y1, max_iter=mi); betas[mi] = (b, c)
    if c:
        first_true = mi; break
if first_true and (first_true - 1) in betas:
    P(''); P('- `converged` の端（本設計型データ）: max_iter=%d で初めて True。max_iter=%d の β との差の最大 %.2e（同じ解に収束済み）なのに converged=%s——判定 `it < max_iter-1` は「最終反復で収束」を偽にする。' % (first_true, first_true - 1, float(np.max(np.abs(betas[first_true - 1][0] - betas[first_true][0]))), betas[first_true - 1][1]))
P('- Heinze–Schemper（2002）の PPLRT は制約下でも全模型の罰則 ½log|I(β)| を最大化する。上表の最終列が非負なら、firth.py の制約解はその目的関数で縮小模型型の解以上の値を取っている。firthlogist 自体は手元で走らせていない（票の firthlogist との比較は未再現）。'); P('')

# ---- V13 段階 B 転記行 D の Holm の m
say('V13')
P('## V13. 段階 B 転記行 D: 両側 Fisher の検出力（n=200 対 200・超幾何の全数列挙・棄却は p ≤ α）——Holm 初段を族の m（減算・加算 4／交差 8）で'); P('')


def fisher_table(n1, n2):
    N = n1 + n2; T = np.ones((n1 + 1, n2 + 1))
    for t in range(N + 1):
        xs = np.arange(max(0, t - n2), min(n1, t) + 1); pm = hypergeom.pmf(xs, N, t, n1)
        sp = np.sort(pm); cs = np.cumsum(sp); k = np.searchsorted(sp, pm * (1 + 1e-7), side='right')
        T[xs, t - xs] = np.minimum(1.0, cs[k - 1])
    return T


FT = fisher_table(n, n); ar = np.arange(n + 1)
fpow = lambda p1, p2, al: float((np.outer(binom.pmf(ar, n, p1), binom.pmf(ar, n, p2)) * (FT <= al)).sum())
printed = {}
try:
    for row in DB['facts']['D']['data']:
        printed.setdefault((round(row['base'], 2), round(row['delta_pt'], 2)), {})[row['alpha']] = row['power']
except Exception:
    printed = {}
P('| 基底 | 差 | 名目 α=0.05 | α/4（減算・加算の Holm 初段） | α/8（交差の Holm 初段） | 設計事実 JSON の値（名目／m=8） |'); P('|---|---|---|---|---|---|')
for b, d in ((0.13, 0.15), (0.13, 0.20), (0.5, 0.10), (0.5, 0.15), (0.5, 0.20)):
    pr = printed.get((b, d), {})
    P('| %.2f | +%d pt | %.3f | %.3f | %.3f | %s |' % (b, round(d * 100), fpow(b, b + d, 0.05), fpow(b, b + d, 0.05 / 4), fpow(b, b + d, 0.05 / 8), ('%s／%s' % (pr.get('nominal', '—'), pr.get('holm_first_m8', '—'))) if pr else '—'))
P('')

# ---- V14 実 d0 と確証族の腕
say('V14')
P('## V14. 段階 A: 両腕の既測基底を持つ確証対比の 4B での実 d0（処置 − 対照・pt）と、確証族に現れる腕'); P('')
fam = A['families']['A_slope']['contrasts']; rows = []
for c in fam:
    if c['base_A_4B2507'] is None or c['base_B_4B2507'] is None:
        continue
    ra = c['base_A_4B2507'] / c['base_n_A']; rb = c['base_B_4B2507'] / c['base_n_B']; rows.append(((ra - rb) * 100, c['id'], ra, rb))
rows.sort(key=lambda r: abs(r[0]))
P('- |d0| の昇順: ' + '／'.join('%s %+.1f（A %.3f・B %.3f）' % (i, d, ra, rb) for d, i, ra, rb in rows) + '。')
ad = np.array([abs(r[0]) for r in rows])
P('- 本数 %d・|d0| の最小 %.1f・最大 %.1f・|d0| ≤ 24 pt は %d 本・10 ≤ |d0| ≤ 18 pt は %d 本。転記行 D の格子の d0 は %s pt。' % (len(rows), ad.min(), ad.max(), int((ad <= 24).sum()), int(((ad >= 10) & (ad <= 18)).sum()), sorted({round(r['d0_pt'] * 100) for r in PG['D']})))
used = {c['A'] for c in fam} | {c['B'] for c in fam}; pairs = sorted({'%s−%s' % (c['A'], c['B']) for c in fam})
P('- 確証族の効果種 %d: %s。確証族に一度も現れない腕: %s。' % (len(pairs), '・'.join(pairs), [a for a in A['arms']['preamble'] if a not in used])); P('')

# ---- V15 解釈条項の発火率の分解
say('V15')
P('## V15. 段階 A: 格子の「対照が規模で動く・d0=0.15・Δ=0」の解釈条項の発火率は何の数か（規模ごとの飽和確率・独立を仮定した厳密計算）'); P('')
k_lo = math.ceil(lo * n) - 1; k_hi = math.floor(hi * n)
sat_prob = lambda p: float(binom.cdf(k_lo, n, p) + binom.sf(k_hi, n, p))


def ge2(ps):
    dp = np.zeros(len(ps) + 1); dp[0] = 1.0
    for q in ps:
        dp[1:] = dp[1:] * (1 - q) + dp[:-1] * q; dp[0] *= (1 - q)
    return float(1 - dp[0] - dp[1])


pc = np.linspace(0.3, 0.9, 6); pt = np.clip(pc + 0.15, 0.001, 0.999); st = [sat_prob(p) for p in pt]; sc = [sat_prob(p) for p in pc]
grid = next(r for r in PG['D'] if r['pattern'] == 'ctrl_rising' and r['d0_pt'] == 0.15 and r['delta_pt_32B_minus_4B'] == 0.0)
P('- 処置の真の率（規模順）: %s。処置の規模ごとの飽和確率（X ≤ %d または X ≥ %d）: %s。対照: %s。' % ('・'.join('%.3f' % p for p in pt), k_lo, k_hi + 1, '・'.join('%.3f' % s for s in st), '・'.join('%.4f' % s for s in sc)))
P('- どちらかの腕が 2 規模以上で飽和する確率（検閲を無視・独立）: %.3f。格子の発火率: %.3f（B=%d）。14B の処置（真の率 %.2f）が閾値を跨ぐ確率 %.3f。32B の処置の飽和確率 %.3f。' % (1 - (1 - ge2(st)) * (1 - ge2(sc)), grid['interp_clause_rate'], PG['B'], pt[4], st[4], st[5])); P('')

# ---- V16 天井型の切り詰め
say('V16')
P('## V16. 段階 A: 格子の天井型（対照 0.97 一定・d0=0.15）で処置の率が上限 0.999 に切り詰められる規模数'); P('')
P('| Δ | 切り詰め前の処置の率（規模順） | 切り詰められた規模数 | 格子の判定不能率／p<0.05 |'); P('|---|---|---|---|')
for D in (0.0, 0.10, 0.15, 0.20, 0.30):
    raw = 0.97 + 0.15 + D * (zs - zs[2]) / zspan
    g = next((r for r in PG['D'] if r['pattern'] == 'ceiling_const' and r['d0_pt'] == 0.15 and abs(r['delta_pt_32B_minus_4B'] - D) < 1e-9), None)
    P('| %.2f | %s | %d／6 | %s |' % (D, '・'.join('%.3f' % x for x in raw), int((raw > 0.999).sum()), ('%.3f／%.3f' % (g['undecidable_rate'], g['reject_005'])) if g else '—'))
P('')

# ---- V17 環境と z の共線
say('V17')
P('## V17. 段階 A: 環境ダミーと z の共線（傾きの族の 6 規模・正本 `environments`）'); P('')
envd = np.array([0.0 if A['environments'][s] == 'L4' else 1.0 for s in sizes]); rr = float(np.corrcoef(zs, envd)[0, 1])
P('- z（実パラメータ数から再計算）: %s。環境（L4=0・A100=1）: %s。z との相関 %.3f（決定係数 %.3f）。橋は %s の 1 規模で、環境 × 規模の交互作用は識別できない。' % ('・'.join('%s %.4f' % (s, Zr[s]) for s in sizes), dict(zip(sizes, envd.astype(int).tolist())), rr, rr * rr, A['bridge']['models'])); P('')

# ---- V18 帯の多重性
say('V18')
P('## V18. 帯の多重性: 環境帯（橋・13 腕）と、錨帯の除外単位（規模 × 場面 = Onull・O-Ncold の 2 腕）——真の率 0.5・二項の差の厳密畳み込み・独立を仮定'); P('')
pmf = lambda p, m=n: binom.pmf(np.arange(m + 1), m, p)
d05 = np.convolve(pmf(0.5), pmf(0.5)[::-1]); lag = np.arange(-n, n + 1)
P('| 帯 | 腕あたり（≥／>） | 13 腕で少なくとも 1 腕（≥／>） | 2 腕のどちらか（>）＝対比の環境保留・錨の除外単位 | 30 単位の期待除外数（>） | 30 単位で少なくとも 1（>） |'); P('|---|---|---|---|---|---|')
for band in (10, 12, 15):
    t = band * n // 100; ge = float(d05[np.abs(lag) >= t].sum()); gt = float(d05[np.abs(lag) > t].sum()); u = 1 - (1 - gt) ** 2
    P('| %d pt | %.4f／%.4f | %.3f／%.3f | %.4f | %.2f | %.3f |' % (band, ge, gt, 1 - (1 - ge) ** 13, 1 - (1 - gt) ** 13, u, 30 * u, 1 - (1 - u) ** 30))
P('- 実際の腕の率は 0.5 から離れるほど発火率が小さい（第一部 V2 の 0.3・0.7 の行）。'); P('')

# ---- V19 校正帯・撤退条件・手元系列
say('V19')
P('## V19. 校正帯と撤退条件（「超」・厳密二項）: 帯の幅ごとの帰無発火率と検出側、および不合格枝の手元系列（二標本）の帰無発火率'); P('')
kb, nb = A['bases_4B2507_api']['N1']['Ncold']['k'], A['bases_4B2507_api']['N1']['Ncold']['n']; base = kb / nb; ncal = A['calibration_n']; pn = A['pilot_n']


def fire_le(m, band):
    thr = Fraction(kb, nb) * m - Fraction(band, 100) * m   # 「超」: X < thr
    return math.ceil(thr) - 1


P('| 対象 | n | 帯 | 発火（X ≤） | 真の率 %.3f（帰無） | 0.95 | 0.94 | 0.93 | 0.90 | 0.85 | 0.80 |' % base); P('|---|---|---|---|---|---|---|---|---|---|---|')
for lab, m, bands in (('校正腕', ncal, (3, 4, 5)), ('撤退条件', pn, (10, 15))):
    for bd in bands:
        k = fire_le(m, bd)
        P('| %s | %d | %d pt | %d | %.2e | %s |' % (lab, m, bd, k, binom.cdf(k, m, base), ' | '.join('%.3f' % binom.cdf(k, m, p) for p in (0.95, 0.94, 0.93, 0.90, 0.85, 0.80))))
P('')
P('- 票（二人目）が「以上」の規約で引いた P(X≤370|400,p): 0.95 %.3f・0.93 %.3f・0.90 %.3f。' % tuple(float(binom.cdf(370, 400, p)) for p in (0.95, 0.93, 0.90)))


def two_sample(m1, m2, p, band):
    x1_ = np.arange(m1 + 1)[:, None]; x2_ = np.arange(m2 + 1)[None, :]
    W = np.outer(binom.pmf(np.arange(m1 + 1), m1, p), binom.pmf(np.arange(m2 + 1), m2, p)); D_ = np.abs(x1_ * m2 - x2_ * m1); thr = band * m1 * m2 // 100
    return float(W[D_ > thr].sum()), float(W[D_ >= thr].sum())


ts = {(m2_, p): two_sample(400, m2_, p, 5) for m2_ in (A['identity_n'], 400) for p in (base, 0.95)}
P('- 不合格枝の手元系列（二標本・両側・帯 5 pt・超／以上）: 初点を門0.5 の n=%d とすると（400 対 %d）真の率 %.3f で %.4f／%.4f・0.95 で %.4f／%.4f。初点を n=400 とすると（400 対 400）%.3f で %.4f／%.4f・0.95 で %.4f／%.4f。正本 `calibration.band_fail` の初点は「門0.5 の Ncold × N1」（n=%d）で、転記行 M の手元系列の値は 400 対 400 の型で計算されている。' % (
    A['identity_n'], A['identity_n'], base, *ts[(A['identity_n'], base)], *ts[(A['identity_n'], 0.95)], base, *ts[(400, base)], *ts[(400, 0.95)], A['identity_n'])); P('')

# ---- V20 段階 B 第 2 段の選定と調整走行の n
say('V20')
P('## V20. 段階 B 第 2 段（係数の選定）: 保留試行数ごとの差の標準誤差・最良の係数を選ぶ確率・単一候補の片側検出力（二項シミュレーション・B=20,000・seed 固定）'); P('')
rng20 = np.random.default_rng(2020); BB = 20000
P('| 基底（Onull・既測） | n／腕 | 差の SE（pt） | 真の低下（係数 0.5／1／2）= 10／20／15 pt で最良を選ぶ確率 | 真の低下 15 pt の片側検出力 α=0.05 | 同 α=0.05/9 |'); P('|---|---|---|---|---|---|')
for scn in ('N1', 'S1'):
    p0 = Bj['bases_4B2507_api_stageVp'][scn]['Onull']['k'] / Bj['bases_4B2507_api_stageVp'][scn]['Onull']['n']
    for m in (20, 40, 100):
        dec = np.array([0.10, 0.20, 0.15])
        xr = rng20.binomial(m, p0, (BB, 3)); xv = rng20.binomial(m, np.clip(p0 - dec, 0.001, 0.999), (BB, 3))
        pbest = float((np.argmax((xr - xv) / m, axis=1) == 1).mean())
        xa = rng20.binomial(m, p0, BB); xb = rng20.binomial(m, p0 - 0.15, BB); pp = (xa + xb) / (2 * m)
        zz = (xa - xb) / m / np.sqrt(np.maximum(pp * (1 - pp) * 2 / m, 1e-12))
        P('| %s %.3f | %d | %.1f | %.3f | %.3f | %.3f |' % (scn, p0, m, math.sqrt(2 * p0 * (1 - p0) / m) * 100, pbest, float((zz > norm.isf(0.05)).mean()), float((zz > norm.isf(0.05 / 9)).mean())))
P('- 係数ごとに v_random の腕を別に持つ配置（草案4 の転記行 A の数え方）。argmax の同値は小さい係数（草案の同値規則と同じ向き）。検出力は合併分散の z 検定の近似。'); P('')

# ---- V21 最大統計量の帯
say('V21')
P('## V21. 門1 を候補の最大で判定する場合の帯（最大統計量の帰無分布の 95 パーセンタイル）と検出力（AUC の正規近似・Hanley–McNeil の SD・共通因子の相関 ρ・200,000 回）'); P('')
rng21 = np.random.default_rng(2121); BB = 200000


def hm_sd(Aa, m):
    Q1 = Aa / (2 - Aa); Q2 = 2 * Aa ** 2 / (1 + Aa)
    return math.sqrt((Aa * (1 - Aa) + (m - 1) * (Q1 - Aa ** 2) + (m - 1) * (Q2 - Aa ** 2)) / (m * m))


P('| m／腕 | 候補数 k | ρ | 帯（最大の 95%） | 真の AUC 0.6（全候補） | 0.6（1 候補のみ） | 0.7（全候補） | 0.7（1 候補のみ） |'); P('|---|---|---|---|---|---|---|---|')
for m in (20, 40, 100):
    for k in (1, 3, 6, 9):
        for rho in ((0.5, 0.8) if k > 1 else (None,)):
            Zc = (math.sqrt(rho) * rng21.normal(size=(BB, 1)) + math.sqrt(1 - rho) * rng21.normal(size=(BB, k))) if k > 1 else rng21.normal(size=(BB, 1))
            sd0 = hm_sd(0.5, m); band = float(np.quantile((0.5 + sd0 * Zc).max(axis=1), 0.95)); out = []
            for Aa in (0.6, 0.7):
                sdA = hm_sd(Aa, m); allc = (Aa + sdA * Zc).max(axis=1)
                one = np.concatenate([Aa + sdA * Zc[:, :1], 0.5 + sd0 * Zc[:, 1:]], axis=1).max(axis=1)
                out += [float((allc > band).mean()), float((one > band).mean())]
            P('| %d | %d | %s | %.3f | %.3f | %.3f | %.3f | %.3f |' % (m, k, ('%.1f' % rho) if rho is not None else '—', band, *out))
P('- 単一候補の帰無 SD は √((2m+1)/(12m²)) と一致（Hanley–McNeil の A=0.5）。'); P('')

# ---- V22 送信文字列の組み立てと抽出位置
say('V22')
P('## V22. 段階 B の主抽出位置と送信文字列の組み立て（凍結走行器 `run_preamble_local.py` の `user_message`・腕台帳）'); P('')
src = open(os.path.join(REPO, 'tools', 'run_preamble_local.py'), encoding='utf-8').read().splitlines()
i0 = next(i for i, l in enumerate(src) if l.startswith('def user_message'))
P('- 組み立て（逐語・%d〜%d 行）:' % (i0 + 1, i0 + 3)); P(''); P('```python'); [P(l) for l in src[i0:i0 + 3]]; P('```'); P('')
tx = [l.strip() for l in src if 'TEXTS' in l and '=' in l and 'TEXTS[arm]' not in l][:3]
P('- `TEXTS` を作る行（逐語・先頭 3 件）: %s' % ('／'.join('`%s`' % t for t in tx) if tx else '（見つからず）'))
P('- 腕台帳の N の SHA: A %s・B %s（前置きファイルを持たない腕）。' % (A['arms']['sha16']['N'], Bj['arms']['sha16']['N']))
P('- 読み: 前置き（腕の本文）は場面本文と指示より**前**に置かれる。因果注意では前置きブロックの末尾トークンまでの隠れ状態は後続の場面に依らないため、主抽出位置の活性は**腕だけで決まる**（試行にも場面にも依らない・数値の非決定性を除く）。抽出場面を N1・S1 の二つにしても、この位置では同じ点を二度読む。前置きを持たない N にはこの位置が無く、正本 `directions.Nk`（%s）は主位置では定まらない。' % Bj['directions']['Nk']['def']); P('')

# ---- V23 段階 B の本走行の腕
say('V23')
P('## V23. 段階 B: 本走行の腕の一覧（生成器の直書き）と、正本の対比が参照する腕の突き合わせ'); P('')
treeB = ast.parse(open(os.path.join(REPO, 'tools', 'design_facts_B.py'), encoding='utf-8').read())
arms_main = next(ast.literal_eval(nd.value) for nd in ast.walk(treeB) if isinstance(nd, ast.Assign) and any(getattr(t, 'id', None) == 'arms_main' for t in nd.targets))
flat = [a for v in arms_main.values() for a in v]; ref = set()
for f_ in list(Bj['families'].values()) + list(Bj['descriptive_families'].values()):
    for c in f_.get('contrasts', []):
        ref.add(c['A']); ref.add(c['B'])
P('- 生成器 `design_facts_B.py` の `arms_main`（直書き・%d 腕・4 場面に掛ける）: %s。' % (len(flat), flat))
P('- 正本の対比が参照するが `arms_main` に無い腕: %s。`arms_main` にあるが正本の対比に現れない腕: %s。' % (sorted(ref - set(flat)), sorted(set(flat) - ref))); P('')

# ---- V24 費用（最大同時要求数）
say('V24')
P('## V24. 段階 A の費用: GPU ごとの最大同時要求数（重み＋KV〔2,048 トークン〕＋1.5 GiB ≤ GPU の 90%）と、処理量の上界・下界での再計算（校正腕はセッションごと・4B-2507 の係数 1.0・錨 6 規模・橋は A100 側のみ）'); P('')
KV_TOK = 2048
kvr = {k: 2 * v['num_hidden_layers'] * v['num_key_value_heads'] * v['head_dim'] * 2 * KV_TOK / 2**30 for k, v in HF['models'].items()}
cmax = lambda k, G: int(math.floor((0.9 * G - HF['models'][k]['safetensors_gib'] - 1.5) / kvr[k]))
P('| 機種 | 重み GiB | KV／要求 GiB | 最大同時（L4 24GB／A100 40GB／A100 80GB） |'); P('|---|---|---|---|')
for k in ['0.6B', '1.7B', '4B', '8B', '14B', '32B', '4B-2507']:
    P('| %s | %.2f | %.4f | %s |' % (k, HF['models'][k]['safetensors_gib'], kvr[k], '／'.join(str(max(cmax(k, G), 0)) for G in (24, 40, 80))))
P('')
COST = {'L4': (2.67, 3839, 512), 'A100': (12.82, 19200, 465)}
SF = {'0.6B': 0.25, '1.7B': 0.5, '4B': 1.0, '4B-2507': 1.0, '8B': 2.0, '14B': 3.5, '32B': 8.0}


def planA(bound, gA100):
    out = []; tu = th = tt = 0
    for k in ['0.6B', '1.7B', '4B', '8B', '14B', '32B', '4B-2507']:
        env = A['environments'][k]; G = 24 if env == 'L4' else gA100; c = min(24, cmax(k, G))
        if c <= 0:
            out.append((k, env, G, 0, None)); continue
        rate, tph, setup = COST[env]; tph_eff = tph * (c / 24 if bound == 'upper' else 1.0)
        base_tr = len(A['scenarios']) * len(A['arms']['preamble']) * (A['pilot_n'] + n) + (len(A['scenarios']) * len(A['anchor_band']['arms']) * n if k in sizes else 0)
        extra = len(A['arms']['preamble']) * n if k == '8B' else 0
        sess = 1
        for _ in range(30):
            h = base_tr * SF[k] / tph_eff + (A['calibration_n'] * sess + extra) / tph
            new = max(1, math.ceil(h / (8 - setup / 3600)))
            if new == sess:
                break
            sess = new
        h_tot = h + sess * setup / 3600; u = h_tot * rate; tr_all = base_tr + A['calibration_n'] * sess + extra
        out.append((k, env, G, c, (tr_all, h_tot, sess, u))); tu += u; th += h_tot; tt += tr_all
    return out, tu, th, tt


for lab, bound, g in (('上界（処理量 ∝ 同時要求数）・A100 80GB 割当（門0 と同じ）', 'upper', 80), ('下界（同時要求数で処理量が落ちない）・A100 80GB 割当', 'lower', 80), ('上界・A100 40GB 割当', 'upper', 40)):
    rw, tu, th, tt = planA(bound, g)
    P('- %s: ' % lab + '／'.join(('%s（%s %dGB・同時 %d）%s 試行・%.1f h・%d セッション・%.1f ユニット' % (k, env, G, c, format(v[0], ','), v[1], v[2], v[3])) if v else ('%s（%s %dGB）載らない' % (k, env, G)) for k, env, G, c, v in rw) + '。**合計 %s 試行・%.1f h・%.1f ユニット**（載らない機種を除く・門0.5 と API 再走行を除く・8B に橋の A100 側 %s 試行を同居）。' % (format(tt, ','), th, tu, format(len(A['arms']['preamble']) * n, ',')))
P('- 係数（4B 比の試行時間）は草案4 の仮定のまま（◐・パイロットで置換）。校正腕は 4B-2507 を別に載せ直すため、機種の切替の経費（未測）が別に要る。'); P('')
try:
    tB = int(sum(DB['facts']['A']['data'].values()))
except Exception:
    tB = None
if tB:
    P('- 段階 B（草案4 の %s 試行・transformers の遅さ 3 倍の仮定・L4・処理量 ∝ バッチ）: ' % format(tB, ',') + '／'.join('バッチ %d で %.1f h・%d セッション・%.0f ユニット' % (cb, tB * 3 / (3839 * cb / 24) + math.ceil((tB * 3 / (3839 * cb / 24)) / (8 - 512 / 3600)) * 512 / 3600, math.ceil((tB * 3 / (3839 * cb / 24)) / (8 - 512 / 3600)), (tB * 3 / (3839 * cb / 24) + math.ceil((tB * 3 / (3839 * cb / 24)) / (8 - 512 / 3600)) * 512 / 3600) * 2.67) for cb in (1, 8, 16, 24)) + '。')
P('- 門0.5（13 腕 × N1・L4）: ' + '／'.join('n=%d で vLLM %s 試行・%.2f h・%.1f ユニット（transformers 経路をバッチ 16 で足すと ＋%.2f h・＋%.1f ユニット）' % (m, format(13 * m, ','), 13 * m / 3839 + 512 / 3600, (13 * m / 3839 + 512 / 3600) * 2.67, 13 * m * 3 / (3839 * 16 / 24) + 512 / 3600, (13 * m * 3 / (3839 * 16 / 24) + 512 / 3600) * 2.67) for m in (80, 160)) + '。'); P('')

# ---- V26 器材の主張の grep（票の grep を出し直す）
say('V26')
P('## V26. 票の grep の出し直し（器材と正本の文字列）'); P('')
srcPG = open(os.path.join(REPO, 'tools', 'power_grid_A.py'), encoding='utf-8').read(); srcFA = open(os.path.join(REPO, 'tools', 'design_facts_A.py'), encoding='utf-8').read()
rawA = open(os.path.join(REPO, 'design', 'contrasts-A.json'), encoding='utf-8').read(); rawB = open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8').read()
P('- `power_grid_A.py` 中の `refuse` の出現数: %d。`>=` を含む行（帯）: %s。' % (srcPG.count('refuse'), [l.strip()[:90] for l in srcPG.splitlines() if 'band_pt / 100' in l or ">= 0.05" in l]))
for s in ('10 本と N2 の Ncold 系 5 本', '2/40・38/40', '上の 0.407', 'default_rng(1)', 'default_rng(2)', '同じ桁', 'id の重複 0・対比が要求する腕の不在 0・登録対比を持たない腕 0', 'z は転記行 L の実値', '処置が平坦なら', '84〜81'):
    P('- `design_facts_A.py` に直書き「%s」: %d 箇所。' % (s, srcFA.count(s)))
P('- 正本 A の文字列の出現数: 尺度依存 %d・pt 差の規模傾向 %d・同時要求 %d・concurrency %d・"strict" %d（`anchor_band` に strict キー: %s・`calibration` に strict キー: %s）。正本 B: 尺度依存 %d。' % (
    rawA.count('尺度依存'), rawA.count('pt 差の規模傾向'), rawA.count('同時要求'), rawA.count('concurrency'), rawA.count('"strict"'), 'strict' in A['anchor_band'], 'strict' in A['calibration'], rawB.count('尺度依存'))); P('')

# ---- V25 確証札の到達（追加行）
say('V25 (Firth simulations, slow)')
P('## V25. 確証札の到達（無条件・第一部 V8 の追加行）: 中程度の効果（Δ=0.10）と、飽和を伴わない尺度依存（対照 0.4→0.8・d0=0.12）（Firth PPLRT・n=200 × 6 規模・両腕条件の検閲・z は実パラメータ数から再計算・B=800）'); P('')


def sim(pc, pt, rng):
    kc = rng.binomial(n, pc); kt = rng.binomial(n, pt); rc = kc / n; rt = kt / n
    keep = ~(((rc < lo) & (rt < lo)) | ((rc > hi) & (rt > hi)))
    if keep.sum() < 3:
        return None
    idx = np.where(keep)[0]
    satc = int(((rc[idx] < lo) | (rc[idx] > hi)).sum()); satt = int(((rt[idx] < lo) | (rt[idx] > hi)).sum())
    a = np.concatenate([np.repeat([0.0, 1.0], n) for _ in idx]); z = np.repeat(zs[idx], 2 * n)
    y = np.concatenate([np.concatenate([np.r_[np.ones(kc[i]), np.zeros(n - kc[i])], np.r_[np.ones(kt[i]), np.zeros(n - kt[i])]]) for i in idx])
    r = pplrt(design(a, z), y, 3)
    if not r['converged']:
        return 'nf'
    d = rt[idx] - rc[idx]; qc = (kc[idx] + 0.5) / (n + 1); qt = (kt[idx] + 0.5) / (n + 1)
    w = 1 / ((qc * (1 - qc) + qt * (1 - qt)) / n); zz = zs[idx]; zb = (w * zz).sum() / w.sum(); sxx = (w * (zz - zb) ** 2).sum()
    slope = (w * (zz - zb) * d).sum() / sxx; se = math.sqrt(1 / sxx)
    return {'p': r['p'], 'beta': r['beta'], 'sat1': satc >= 1 or satt >= 1, 'sat2': satc >= 2 or satt >= 2,
            'pt_ok': abs(slope) / se > norm.isf(0.025) and np.sign(slope) == np.sign(r['beta']), 'pt_okH': abs(slope) / se > norm.isf(0.05 / 70) and np.sign(slope) == np.sign(r['beta'])}


cases = [('対照中間 0.5 一定', np.full(6, 0.5), 0.0, 0.10), ('対照 0.3→0.9', np.linspace(0.3, 0.9, 6), 0.0, 0.10), ('対照 0.3→0.8（飽和なし）', np.linspace(0.3, 0.8, 6), 0.0, 0.10), ('対照 0.4→0.8（飽和なし）', np.linspace(0.4, 0.8, 6), 0.12, 0.0)]
P('| 対照の基底 | d0 | Δ | 判定不能 | 非収束 | p<0.05 | 札（現行: 名目 ∧ ¬2規模） | 札（1 規模） | 札（e-2: 名目 ∧ ¬2規模 ∧ pt 傾き同向） | Holm 初段での札（現行／e-2／e-2H: pt 傾きも Holm 初段の水準） |'); P('|---|---|---|---|---|---|---|---|---|---|')
rng25 = np.random.default_rng(252525); BB = 800
for name, pcv, d0, D in cases:
    ptv = np.clip(pcv + d0 + D * (zs - zs[2]) / zspan, 0.001, 0.999); und = nf = rej = cur = one = e2 = curH = e2H = e2HH = 0
    for _ in range(BB):
        s = sim(pcv, ptv, rng25)
        if s is None:
            und += 1; continue
        if s == 'nf':
            nf += 1; continue
        R = s['p'] < 0.05; RH = s['p'] < 0.05 / 35
        rej += R; cur += R and not s['sat2']; one += R and not s['sat1']; e2 += R and not s['sat2'] and s['pt_ok']
        curH += RH and not s['sat2']; e2H += RH and not s['sat2'] and s['pt_ok']; e2HH += RH and not s['sat2'] and s['pt_okH']
    P('| %s | %.2f | %.2f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f／%.3f／%.3f |' % (name, d0, D, und / BB, nf / BB, rej / BB, cur / BB, one / BB, e2 / BB, curH / BB, e2H / BB, e2HH / BB))
    say('V25 row done: %s d0=%.2f D=%.2f' % (name, d0, D))
P(''); P('- 「札」はいずれも B=800 回に対する無条件率（判定不能と非収束も分母に含む）。pt 傾き＝残存規模の pt 差を z に重み付き最小二乗で回帰した傾き（重み＝1/分散・連続性補正 0.5）・区間は正規（95%＝両側 0.05／e-2H＝両側 0.05/35）・β₃ と同じ向き。'); P('')

P('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
dst = os.path.join(REPO, 'records', 'reviews', 'AB', 'round-claudeai', 'verification-claudeai-AB-2.md'); os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(O) + '\n'); say('written ' + dst)
