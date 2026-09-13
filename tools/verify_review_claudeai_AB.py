# -*- coding: utf-8 -*-
"""verify_review_claudeai_AB.py v1 —— claude.ai 三票（段階 A・B 設計草案4）の主要な数の主張を、コーディネータが一次記録と独立計算で追い問いする（2026-09-13）。
票の完了報告・再計算の申告は検査ではないため、同じ量を自分の器で出し直す。出力: records/reviews/AB/round-claudeai/verification-claudeai-AB.md。
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, glob, subprocess, datetime
import numpy as np
from scipy.stats import binom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from firth import design, pplrt
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(REPO, *p), encoding='utf-8'))
A = J('design', 'contrasts-A.json'); Bj = J('design', 'contrasts-B.json'); PG = J('records', 'A', 'power-grid-A.json'); HF = J('records', 'A', 'hf-models-A.json')
O = ['# claude.ai 三票（草案4）の追い問い——コーディネータの独立計算（機械生成・`tools/verify_review_claudeai_AB.py` v1・%s UTC）' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), '']
P = O.append
n = 200; lo, hi = 0.05, 0.95

# ---- V1 転記行 D の条件付き率と無条件率
P('## V1. 転記行 D: 棄却率は判定不能を除いた条件付きか（power-grid-A.json の行から）'); P('')
P('| 型 | d0 | Δ | 判定不能率 | 条件付き p<0.05 | 無条件 = 条件付き × (1−判定不能) | n_fit | 条件付きの 95% 半幅 |'); P('|---|---|---|---|---|---|---|---|')
for r in PG['D']:
    if (r['d0_pt'], r['delta_pt_32B_minus_4B']) in ((0.0, 0.0), (0.0, 0.15), (0.15, 0.0)):
        hw = 1.96 * math.sqrt(max(r['reject_005'] * (1 - r['reject_005']), 1e-12) / max(r['n_fit'], 1))
        P('| %s | %.2f | %.2f | %.3f | %.3f | %.4f | %d | ±%.3f |' % (r['pattern'], r['d0_pt'], r['delta_pt_32B_minus_4B'], r['undecidable_rate'], r['reject_005'], r['reject_005'] * (1 - r['undecidable_rate']), r['n_fit'], hw))
P('')

# ---- V2 帯の不等号（以上／超）の厳密計算
P('## V2. 錨帯: 二項の差 |X₁−X₂|（n=200 同士）の帰無発火率——「以上」と「超」の厳密畳み込み'); P('')
pmf = lambda p: binom.pmf(np.arange(n + 1), n, p)
P('| 真の率 | 帯 pt | 以上（≥） | 超（>） | 60 対の期待本数（≥／>） | 70 対（≥／>） |'); P('|---|---|---|---|---|---|')
for p in (0.3, 0.5, 0.7):
    d = np.convolve(pmf(p), pmf(p)[::-1]); lag = np.arange(-n, n + 1)
    for band in (10, 12, 15):
        t = band * n // 100; ge = float(d[np.abs(lag) >= t].sum()); gt = float(d[np.abs(lag) > t].sum())
        P('| %.1f | %d | %.4f | %.4f | %.2f／%.2f | %.2f／%.2f |' % (p, band, ge, gt, 60 * ge, 60 * gt, 70 * ge, 70 * gt))
d = np.convolve(pmf(0.5), pmf(0.5)[::-1]); lag = np.arange(-n, n + 1)
P(''); P('検出側（超・真の率 0.5 付近で走行間に真の drift δ pt があるときの発火率）: （下の表）')
P('| 真の drift | 10 pt 超 | 12 pt 超 | 15 pt 超 |'); P('|---|---|---|---|')
for dl in (10, 14, 16, 20):
    pa, pb = 0.5 + dl / 200, 0.5 - dl / 200
    dd = np.convolve(pmf(pa), pmf(pb)[::-1])
    P('| %d pt | %.3f | %.3f | %.3f |' % (dl, float(dd[np.abs(lag) > 20].sum()), float(dd[np.abs(lag) > 24].sum()), float(dd[np.abs(lag) > 30].sum())))
P('')

# ---- V3 転記行 B の既測基底の内訳
fam = A['families']['A_slope']['contrasts']; miss = [c['id'] for c in fam if c['base_A_4B2507'] is None or c['base_B_4B2507'] is None]
dose = [i for i in miss if 'Odose' in i]; other = [i for i in miss if 'Odose' not in i]
P('## V3. 転記行 B: 既測基底を欠く確証対比の内訳（contrasts-A.json を数える）'); P('')
P('- 確証 %d 本・両腕の基底あり %d 本・欠く %d 本＝Odose1／Odosehalf 系 %d 本＋その他 %d 本（%s）。印字の「10 本と N2 の Ncold 系 5 本」は **%s**。' % (len(fam), len(fam) - len(miss), len(miss), len(dose), len(other), '・'.join(other), '誤り（5 → %d）' % len(other) if len(other) != 5 else '一致'))
sat4b = []
for c in fam:
    if c['base_A_4B2507'] is not None and c['base_B_4B2507'] is not None:
        ra, rb = c['base_A_4B2507'] / c['base_n_A'], c['base_B_4B2507'] / c['base_n_B']
        if ra < lo or ra > hi or rb < lo or rb > hi:
            sat4b.append('%s（A %.3f・B %.3f）' % (c['id'], ra, rb))
P('- 4B-2507 の既測基底で片腕が既に閾外（<0.05 または >0.95）の確証対比: **%d 本**——%s。' % (len(sat4b), '／'.join(sat4b))); P('')

# ---- V4 転記行 I の閾値と整数境界
P('## V4. 転記行 I: n=40 の両腕条件の閾値と、校正帯・撤退条件の整数境界（「超」）'); P('')
P('- n=40: 率 <0.05 ⇔ X ≤ %d（ceil(0.05×40)−1）・率 >0.95 ⇔ X ≥ %d（floor(0.95×40)+1）。印字の「2/40・38/40」は誤り。' % (math.ceil(0.05 * 40) - 1, math.floor(0.95 * 40) + 1))
base = 390 / 400
P('- 校正腕（n=400・基底 %.3f・5 pt 帯・「超」）: 発火 ⇔ 率 < 0.925 ⇔ X ≤ 369（370/400 はちょうど 0.925）。P(X≤370)=%.2e・P(X≤369)=%.2e。上側は 1.0 を超え片側の帯。' % (base, binom.cdf(370, 400, base), binom.cdf(369, 400, base)))
P('- 撤退条件（n=40・15 pt 帯・「超」）: 発火 ⇔ 率 < 0.825 ⇔ X ≤ 32（33/40 はちょうど 0.825）。P(X≤33)=%.2e・P(X≤32)=%.2e。' % (binom.cdf(33, 40, base), binom.cdf(32, 40, base))); P('')

# ---- V5 同時要求数と費用（上界）
P('## V5. 同時要求数と収容・費用の再計算（上界＝処理量は同時要求数に比例と仮定）'); P('')
KV_TOK = 2048
kv = {k: 2 * v['num_hidden_layers'] * v['num_key_value_heads'] * v['head_dim'] * 2 * KV_TOK / 2**30 for k, v in HF['models'].items()}
need = lambda k, c: HF['models'][k]['safetensors_gib'] + kv[k] * c + 1.5
P('- 1 要求あたり KV（2,048 トークン）: ' + '・'.join('%s %.4f GiB' % (k, kv[k]) for k in ['4B', '8B', '14B', '32B']) + '。')
P('- 14B: 同時 24 で要 %.2f GiB（A100-40 の 90%% = 36.0 を超える）・同時 16 で %.2f（載る）・同時 20 で %.2f（載る）。32B: 同時 8 で %.2f（A100-80 の 72.0 に載る）・同時 24 で %.2f（載らない）。' % (need('14B', 24), need('14B', 16), need('14B', 20), need('32B', 8), need('32B', 24)))
COST = {'L4': (2.67, 3839, 512), 'A100': (12.82, 19200, 465)}
SF = {'0.6B': 0.25, '1.7B': 0.5, '4B': 1.0, '4B-2507': 1.0, '8B': 2.0, '14B': 3.5, '32B': 8.0}
ENV = {'0.6B': ('L4', 24), '1.7B': ('L4', 24), '4B': ('L4', 24), '4B-2507': ('L4', 24), '8B': ('A100', 24), '14B': ('A100', 16), '32B': ('A100', 8)}
sizes = ['0.6B', '1.7B', '4B', '8B', '14B', '32B']


def plan(corrected):
    rows = {}; tot_u = tot_h = tot_t = 0
    for k in ['0.6B', '1.7B', '4B', '8B', '14B', '32B', '4B-2507']:
        env, conc = ENV[k]; rate, tph, setup = COST[env]
        tph_eff = tph * (conc / 24 if corrected else 1.0)
        anchor = (5 * 2 * n) if (k in sizes or not corrected) else 0
        bridge = (13 * n * (1 if corrected else 2)) if k == '4B' else 0
        base_tr = 5 * 13 * (40 + n) + anchor + bridge
        sess = 1
        for _ in range(10):
            cal = 400 * (sess if corrected else 2); tr = base_tr + cal; h = tr * SF[k] / tph_eff
            new = math.ceil(h / (8 - setup / 3600))
            if new == sess or not corrected:
                sess = new; break
            sess = new
        h_tot = h + sess * setup / 3600; u = h_tot * rate
        rows[k] = (tr, round(h_tot, 1), sess, round(u, 1)); tot_u += u; tot_h += h_tot; tot_t += tr
    return rows, tot_u, tot_h, tot_t


for lab, corr in (('草案4 の式（補正なし・校正 2 回・錨 7 機種・橋 両側）', False), ('補正後（同時要求で処理量を比例縮小・校正はセッションごと・錨 6 規模・橋は A100 側のみ）', True)):
    rows, u, h, t = plan(corr)
    P('- %s: ' % lab + '／'.join('%s %s 試行・%.1f h・%d セッション・%.1f ユニット' % (k, format(v[0], ','), v[1], v[2], v[3]) for k, v in rows.items()) + '。**合計 %s 試行（門0.5 を除く）・%.1f h・%.1f ユニット**。' % (format(t, ','), h, u))
P('')

# ---- V6 門1 の 6 候補の最大
P('## V6. 段階 B 門1: 単一候補の帯（片側 95%）を 6 候補の最大に当てたときの帰無開放率（正規近似・共通因子の相関 ρ・400,000 回）'); P('')
rng = np.random.default_rng(20260913)
P('| ρ | 単一候補 | 6 候補の最大 |'); P('|---|---|---|')
for rho in (0.0, 0.5, 0.8, 0.95):
    C = rng.standard_normal((400000, 1)); E = rng.standard_normal((400000, 6)); Z = math.sqrt(rho) * C + math.sqrt(1 - rho) * E
    P('| %.2f | %.3f | %.3f |' % (rho, float((Z[:, 0] > 1.645).mean()), float((Z.max(axis=1) > 1.645).mean())))
sd = lambda m: math.sqrt((2 * m + 1) / (12 * m * m))
def hm_power(Aauc, m):
    q1 = Aauc / (2 - Aauc); q2 = 2 * Aauc ** 2 / (1 + Aauc); var = (Aauc * (1 - Aauc) + (m - 1) * (q1 - Aauc ** 2) + (m - 1) * (q2 - Aauc ** 2)) / (m * m)
    from scipy.stats import norm
    return float(norm.sf((0.5 + 1.645 * sd(m) - Aauc) / math.sqrt(var)))
P(''); P('- 保留 m 試行／腕での真の AUC 0.6 の帯外確率（Hanley–McNeil・単一候補）: ' + '・'.join('m=%d %.3f' % (m, hm_power(0.6, m)) for m in (20, 40, 60, 80, 100, 120)) + '。'); P('')

# ---- V7 門0.5 の帰無不合格率（API 既測の率を真値とする）
P('## V7. 門0.5 同一性選別: 両スタックが同一の分布でも主判定（30 個の絶対差の平均 ≤5 かつ最大 ≤12）に落ちる確率'); P('')
arms = A['identity_screen']['compared_arms']; bases = A['bases_4B2507_api']['N1']
probs = []; napi = []
for a in arms:
    b = bases[a]; nn = b['n']; pc, pr, pf = b['k'] / nn, b['refuse'] / nn, b['format_fail'] / nn
    probs.append([pc, pr, pf, max(0.0, 1 - pc - pr - pf)]); napi.append(nn)
probs = np.array(probs); rng = np.random.default_rng(7)
for nloc, mode in [(nl, md) for nl in (80, 160) for md in ('API を固定（手元の雑音のみ）', 'API も再標本（両側の雑音）')]:
    fails = 0; mx = []
    for _ in range(20000):
        diffs = []
        for i in range(len(arms)):
            loc = rng.multinomial(nloc, probs[i]) / nloc
            api = probs[i] if mode.startswith('API を固定') else rng.multinomial(napi[i], probs[i]) / napi[i]
            diffs += list(np.abs(loc[:3] - api[:3]) * 100)
        diffs = np.array(diffs); mx.append(diffs.max()); fails += (diffs.mean() > 5) or (diffs.max() > 12)
    P('- 手元 n=%d・%s: 不合格率 %.3f・最大絶対差の 95 パーセンタイル %.1f pt。' % (nloc, mode, fails / 20000, float(np.quantile(mx, 0.95))))
P('')

# ---- V8 解釈条項と尺度依存の同時確率（ターゲット再計算）
P('## V8. 確証札の到達（無条件）: 解釈条項（2 規模・1 規模）と (xiv) を降格規則にした場合（e-2）の比較（Firth PPLRT・n=200 × 6 規模・両腕条件の検閲・z は転記行 L の実値・B=800）'); P('')
Zr = {'0.6B': -1.9093, '1.7B': -0.8492, '4B': 0.0, '8B': 0.7111, '14B': 1.3006, '32B': 2.0974}; zs = np.array([Zr[s] for s in sizes]); zspan = zs[-1] - zs[2]


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
    return {'p': r['p'], 'beta': r['beta'], 'sat1': satc >= 1 or satt >= 1, 'sat2': satc >= 2 or satt >= 2, 'pt_ok': abs(slope) / se > 1.96 and np.sign(slope) == np.sign(r['beta']), 'pt_okH': abs(slope) / se > 3.195 and np.sign(slope) == np.sign(r['beta'])}


cases = [('対照中間 0.5 一定', np.full(6, 0.5), 0.0, 0.0), ('対照中間 0.5 一定', np.full(6, 0.5), 0.0, 0.15),
         ('対照 0.3→0.9', np.linspace(0.3, 0.9, 6), 0.05, 0.0), ('対照 0.3→0.9', np.linspace(0.3, 0.9, 6), 0.10, 0.0), ('対照 0.3→0.9', np.linspace(0.3, 0.9, 6), 0.15, 0.0),
         ('対照 0.3→0.9', np.linspace(0.3, 0.9, 6), 0.0, 0.15), ('対照 0.3→0.8（飽和なし）', np.linspace(0.3, 0.8, 6), 0.10, 0.0)]
P('| 対照の基底 | d0 | Δ | 判定不能 | 非収束 | p<0.05 | 札（現行: 名目 ∧ ¬2規模） | 札（1 規模） | 札（e-2: 名目 ∧ ¬2規模 ∧ pt 傾き同向） | Holm 初段での札（現行／e-2／e-2H: pt 傾きも Holm 初段の水準） |'); P('|---|---|---|---|---|---|---|---|---|---|')
rng = np.random.default_rng(424242); BB = 800
for name, pc, d0, D in cases:
    pt = np.clip(pc + d0 + D * (zs - zs[2]) / zspan, 0.001, 0.999); und = nf = rej = cur = one = e2 = curH = e2H = e2HH = 0
    for _ in range(BB):
        s = sim(pc, pt, rng)
        if s is None:
            und += 1; continue
        if s == 'nf':
            nf += 1; continue
        R = s['p'] < 0.05; RH = s['p'] < 0.05 / 35
        rej += R; cur += R and not s['sat2']; one += R and not s['sat1']; e2 += R and not s['sat2'] and s['pt_ok']; curH += RH and not s['sat2']; e2H += RH and not s['sat2'] and s['pt_ok']; e2HH += RH and not s['sat2'] and s['pt_okH']
    P('| %s | %.2f | %.2f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f／%.3f／%.3f |' % (name, d0, D, und / BB, nf / BB, rej / BB, cur / BB, one / BB, e2 / BB, curH / BB, e2H / BB, e2HH / BB))
P(''); P('- 「札」はいずれも B=800 回に対する無条件率（判定不能と非収束も分母に含む）。pt 傾き＝残存規模の pt 差を z に重み付き最小二乗で回帰した傾き（重み＝1/分散・連続性補正 0.5）・95% 区間が 0 を含まず β₃ と同じ向き。'); P('')

# ---- V9 firth.py の桁あふれ・R の有無
P('## V9. `tools/firth.py` の数値の端と、R `logistf` の手元での有無'); P('')
with np.errstate(over='ignore'):
    P('- `np.log1p(np.exp(710.0))` = %s・`np.logaddexp(0.0, 710.0)` = %s。' % (np.log1p(np.exp(710.0)), np.logaddexp(0.0, 710.0)))
P('- Python の `max(0.0, float("nan"))` = %s（罰則付き対数尤度が両方 −inf なら stat が 0 → p=1.0 に落ちる経路）。' % max(0.0, float('nan')))
try:
    r = subprocess.run(['Rscript', '--version'], capture_output=True, text=True, timeout=20); P('- Rscript: %s' % ((r.stderr or r.stdout).strip()[:80]))
except Exception as ex:
    P('- Rscript: 手元に無い（%s）。`logistf` との一致検査は手元では走らせられない。' % type(ex).__name__)
P('')

# ---- V10 段階 B の正本の腕と品質床
P('## V10. 段階 B 正本: 品質床の腕と腕台帳'); P('')
P('- `arms.preamble` = %s。`quality_floor.arms` = %s。台帳に無い品質床の腕: %s。確証族の土台（O-Ncold・Onull）で品質床に無いもの: %s。' % (Bj['arms']['preamble'], Bj['quality_floor']['arms'], [x for x in Bj['quality_floor']['arms'] if x not in Bj['arms']['preamble']], [x for x in ('O-Ncold', 'Onull') if x not in Bj['quality_floor']['arms']]))
P('')

# ---- V11 段階 B の主抽出位置（前置きブロック末尾）が試行間で変わらないこと
P('## V11. 段階 B の主抽出位置（結合前置きブロックの末尾トークン）は試行ごとに変わるか——同じ腕 × 場面の送信文字列の一意性（段階 F の実走行記録）'); P('')
cnt = {}
for f in glob.glob(os.path.join(REPO, 'results', 'stageF1', '*__N1__*', 'trials-*.jsonl')):
    for l in open(f, encoding='utf-8'):
        if l.strip():
            t = json.loads(l); cnt.setdefault(t['arm'], set()).add(t.get('prompt_sha'))
P('- stageF1 × N1: ' + '・'.join('%s %d 試行分の prompt_sha 異なり %d' % (a, 400, len(s)) for a, s in sorted(cnt.items())) + '。')
P('- 送信文字列が腕 × 場面で一つに決まるため、生成前のトークン（前置きブロックの末尾を含む）の隠れ状態は、サンプリングに依らず試行間で同一（数値の非決定性を除く）。**主抽出位置で「試行を抽出用と保留用に分けて保留 AUC を出す」は、同一点の比較になり試行単位の推測が成立しない**。試行間で変わるのは生成トークン（副抽出位置＝応答トークン平均）のみ。'); P('')
P('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
dst = os.path.join(REPO, 'records', 'reviews', 'AB', 'round-claudeai', 'verification-claudeai-AB.md'); os.makedirs(os.path.dirname(dst), exist_ok=True)
open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(O) + '\n'); print('[verify] written', dst)
