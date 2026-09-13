# -*- coding: utf-8 -*-
"""verify_review_prefreeze_A_2.py v1 —— 段階 A 草案6 の凍結前検分・七票の追い問い 第二部（シミュレーション・コーディネータ・2026-09-13）。
W27 pt 差の傾きの検定だけの実サイズ（残存規模数・基底率別・ベクトル化・B=1,000,000）
W28 切り詰めの無い対照の型での札（草案4 の規則と裁定 D1 の規則・Firth PPLRT・格子の one()/tally()/run_cell() を ast で取り出して同一の手順で）
W29 Holm の水準の三つの読み（(i) β₃ を棄却した段の水準・(ii) 初段 α/m に固定・(iii) IUT の p 値 max(p_β, p_pt) に Holm）の、35 対比の族としての誤確証率と到達（対比ごとの資源プールを再標本）
W30 格子の一行の追試（Cl2 (1-8)・Cl3 1-4）
W31 門0.5 の検出側（一つの腕の破局率だけがずれるとき・ベクトル化）
出力: records/reviews/A/prefreeze/verification-prefreeze-A-2.md
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, math, ast, datetime, time, argparse, hashlib
from fractions import Fraction
import numpy as np
from scipy.stats import norm, binom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firth
from firth import slope_rows
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--B-size', type=int, default=1000000); ap.add_argument('--B-firth', type=int, default=2000); ap.add_argument('--pool-scale', type=int, default=12000); ap.add_argument('--pool-other', type=int, default=4000)
ap.add_argument('--R', type=int, default=20000); ap.add_argument('--B-cell', type=int, default=4000); ap.add_argument('--B-id', type=int, default=20000); ap.add_argument('--quick', action='store_true')
ap.add_argument('--out', default=os.path.join(REPO, 'records', 'reviews', 'A', 'prefreeze', 'verification-prefreeze-A-2.md'))
a = ap.parse_args()
if a.quick:
    a.B_size, a.B_firth, a.pool_scale, a.pool_other, a.R, a.B_cell, a.B_id = 20000, 40, 300, 200, 500, 60, 500
J = lambda *p: json.load(open(os.path.join(REPO, *p), encoding='utf-8'))
TX = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
SHA = lambda rel: hashlib.sha256(open(os.path.join(REPO, rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
T = J('design', 'contrasts-A.json'); HF = J('records', 'A', 'hf-models-A.json'); PG = J('records', 'A', 'power-grid-A.json')
FAM = T['families']['A_slope']; n = T['n_per_arm']; ALPHA = FAM['alpha']; M = FAM['m']; SIZES = T['sizes']; SEED = 20260913
PGP = os.path.join(REPO, 'tools', 'power_grid_A.py'); PGS = open(PGP, encoding='utf-8').read()


def fn_src(name):
    tree = ast.parse(PGS)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(PGS, node)
    raise KeyError(name)


G = {'np': np, 'math': math, 'firth': firth, 'slope_rows': slope_rows, 'round': round}
exec(fn_src('params'), G)
PAR = {k: G['params'](v) for k, v in HF['models'].items()}; Z = {k: math.log(PAR[k] / PAR['4B']) for k in SIZES}; zs = np.array([Z[s] for s in SIZES]); z4 = Z['4B']; zspan = float(zs[-1] - z4)
KLO = math.ceil(Fraction(str(T['censor']['low'])) * n) - 1; KHI = math.floor(Fraction(str(T['censor']['high'])) * n) + 1
z_nom = float(norm.isf(ALPHA / 2)); z_h1 = float(norm.isf(ALPHA / M / 2))
G.update(n=n, NN6=np.full(len(SIZES), n), zs=zs, z4=z4, zspan=zspan, KLO=KLO, KHI=KHI, ALPHA=ALPHA, HOLM_M=M, z_nom=z_nom, z_h1=z_h1)
exec(re.search(r"^KEYS = \([^\n]+\)$", PGS, re.M).group(0), G)
for nm in ('wilson', 'one', 'tally', 'summarize', 'run_cell', 'treat'):
    exec(fn_src(nm), G)
one, run_cell, treat, wilson = G['one'], G['run_cell'], G['treat'], G['wilson']
stream = lambda k: np.random.default_rng([SEED, 900 + k])
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
O = ['# 凍結前検分・七票の追い問い 第二部——コーディネータのシミュレーション（機械生成・`tools/verify_review_prefreeze_A_2.py` v1・%s UTC%s）' % (now, '・quick' if a.quick else ''), '',
     '- 入力の SHA16: 正本 %s・格子の器 `power_grid_A.py` %s（`params`・`one`・`tally`・`summarize`・`run_cell`・`treat`・`wilson` を ast で取り出して同じ手順で使う）・`firth.py` %s。seed %d（節ごとに子ストリーム）。' % (SHA('design/contrasts-A.json'), SHA('tools/power_grid_A.py'), SHA('tools/firth.py'), SEED),
     '- B: W27 %s・W28 %d／セル・W29 プール（尺度だけ %d・その他 %d）と族の再標本 %d・W30 %d・W31 %d。水準 α=%.2f・Holm 初段 α/%d（正規の臨界 %.4f）。' % (format(a.B_size, ','), a.B_firth, a.pool_scale, a.pool_other, a.R, a.B_cell, a.B_id, ALPHA, M, z_h1),
     '- 票の略は第一部と同じ（Ge1・Ge2・Gr1・Gr2・Cl1・Cl2・Cl3）。', '']
P = O.append


def say(msg):
    print('[verify-pf2]', msg, flush=True)


hw = lambda p, N: 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / max(N, 1))

# ---------------- W27
say('W27'); t0 = time.time()


def sim_pt(pc, pt, B, rng, subset=None):
    tot = dict(fit=0, rn=0, rh=0, fit_nc=0, rn_nc=0, rh_nc=0); ch = 200000
    for s0 in range(0, B, ch):
        b = min(ch, B - s0); kc = rng.binomial(n, pc, size=(b, 6)); kt = rng.binomial(n, pt, size=(b, 6))
        if subset is None:
            keep = ~(((kc <= KLO) & (kt <= KLO)) | ((kc >= KHI) & (kt >= KHI)))
        else:
            keep = np.zeros((b, 6), bool); keep[:, subset] = True
        fit = keep.sum(1) >= 3
        qc = (kc + 0.5) / (n + 1); qt = (kt + 0.5) / (n + 1); w = np.where(keep, 1.0 / ((qc * (1 - qc) + qt * (1 - qt)) / n), 0.0)
        sw = np.where(w.sum(1) > 0, w.sum(1), 1.0); zb = (w * zs[None, :]).sum(1) / sw; dz = zs[None, :] - zb[:, None]; sxx = (w * dz ** 2).sum(1); sxx = np.where(sxx > 0, sxx, 1.0)
        d = (kt - kc) / n; slope = (w * dz * d).sum(1) / sxx; zt = slope * np.sqrt(sxx)
        satc = ((kc <= KLO) | (kc >= KHI)) & keep; satt = ((kt <= KLO) | (kt >= KHI)) & keep; nc = fit & ~((satc.sum(1) >= 2) | (satt.sum(1) >= 2))
        rn = fit & (np.abs(zt) > z_nom); rh = fit & (np.abs(zt) > z_h1)
        tot['fit'] += int(fit.sum()); tot['rn'] += int(rn.sum()); tot['rh'] += int(rh.sum()); tot['fit_nc'] += int(nc.sum()); tot['rn_nc'] += int((rn & nc).sum()); tot['rh_nc'] += int((rh & nc).sum())
    return tot


SUBS = [('6 規模', list(range(6))), ('5 規模（32B なし）', [0, 1, 2, 3, 4]), ('4 規模（0.6B〜8B）', [0, 1, 2, 3]), ('3 規模（0.6B・1.7B・4B）', [0, 1, 2]), ('3 規模（8B・14B・32B）', [3, 4, 5]), ('3 規模（0.6B・4B・32B）', [0, 2, 5])]
MID = [('対照 0.5 一定・pt 差 +15 pt', np.full(6, 0.5), 0.15), ('対照 0.3→0.8・pt 差 +15 pt', np.linspace(0.3, 0.8, 6), 0.15), ('対照 0.2→0.6・pt 差 +15 pt', np.linspace(0.2, 0.6, 6), 0.15), ('対照 0.1→0.5・pt 差 +10 pt', np.linspace(0.1, 0.5, 6), 0.10)]
EDGE = [('対照 0.03 一定・pt 差 0（床）', np.full(6, 0.03), 0.0), ('対照 0.03 一定・pt 差 +5 pt', np.full(6, 0.03), 0.05), ('対照 0.02 一定・pt 差 +3 pt', np.full(6, 0.02), 0.03), ('対照 0.97 一定・pt 差 0（天井）', np.full(6, 0.97), 0.0)]
P('## W27. pt 差の傾きの検定だけの実サイズ（真の pt 差は全規模で一定・切り詰めなし・両側・向きの条件なし）（Ge2 重大2・Gr1 重大1 (b)・Gr2 重大1・Cl1 1.4(a)・Cl2 (1-9)・Cl3 重大4）'); P('')
P('- 目標: 名目 %.4f・初段 %.6f。比＝実サイズ／目標。MC の 95%% 半幅は初段で ±%.5f（B=%s・当てはめ全数のとき）。' % (ALPHA, ALPHA / M, hw(ALPHA / M, a.B_size), format(a.B_size, ',')))
P(''); P('| 配置 | 残した規模（固定） | 名目の実サイズ（比） | 初段の実サイズ（比） |'); P('|---|---|---|---|')
k = 0
for nm, pc, d0 in MID:
    assert np.all(pc + d0 < 0.999)
    for sn, sub in SUBS:
        k += 1; t = sim_pt(pc, pc + d0, a.B_size, stream(k), sub)
        P('| %s | %s | %.5f（%.2f） | %.6f（%.2f） |' % (nm, sn, t['rn'] / a.B_size, t['rn'] / a.B_size / ALPHA, t['rh'] / a.B_size, t['rh'] / a.B_size / (ALPHA / M)))
P(''); P('| 床・天井の配置（検閲は両腕条件で自然に起きる） | 当てはめ可能（残存 3 以上）の割合 | 無条件の名目／初段 | 当てはめ可能の中の名目（比）／初段（比） | 当てはめ可能かつ解釈条項が発火しない割合 | その中の名目（比）／初段（比） |'); P('|---|---|---|---|---|---|')
for nm, pc, d0 in EDGE:
    k += 1; pt = pc + d0 if d0 >= 0 else pc - d0; t = sim_pt(pc, pt, a.B_size, stream(k)); f = max(t['fit'], 1); f2 = max(t['fit_nc'], 1)
    P('| %s | %.4f | %.5f／%.6f | %.4f（%.2f）／%.5f（%.2f） | %.4f | %.4f（%.2f）／%.5f（%.2f） |' % (nm, t['fit'] / a.B_size, t['rn'] / a.B_size, t['rh'] / a.B_size, t['rn'] / f, t['rn'] / f / ALPHA, t['rh'] / f, t['rh'] / f / (ALPHA / M), t['fit_nc'] / a.B_size, t['rn_nc'] / f2, t['rn_nc'] / f2 / ALPHA, t['rh_nc'] / f2, t['rh_nc'] / f2 / (ALPHA / M)))
P(''); P('- 所要 %.0f 秒。' % (time.time() - t0)); P('')

# ---------------- W28
say('W28'); t0 = time.time()
P('## W28. 切り詰めの無い対照の型での札（草案4 の規則と裁定 D1 の規則・Firth PPLRT・B=%d／セル）（Cl1 中3・1.4(b)(c)・Cl2 3-2・Cl3 重大1）' % a.B_firth); P('')
P('| 対照 | 真の処置 | 切り詰め | 真の pt 差の傾き（pt／z・OLS） | p<α（名目） | 札 草案4 名目／初段 | 札 D1 名目／初段 | 解釈条項（当てはめの中） |'); P('|---|---|---|---|---|---|---|---|')
PAT = [('上昇 0.3→0.8', np.linspace(0.3, 0.8, 6)), ('下降 0.8→0.3', np.linspace(0.8, 0.3, 6))]; k = 100
for pn_, pc in PAT:
    rows = [('d0=%d pt・Δ=0（pt 差一定＝尺度依存の帰無）' % (d0 * 100), pc + d0) for d0 in (0.05, 0.10, 0.15)] + [('d0=0・Δ=%d pt（効果あり）' % (D * 100), pc + D * (zs - z4) / zspan) for D in (0.10, 0.15)]
    for rn_, raw in rows:
        k += 1; clipped = int(((raw > 0.999) | (raw < 0.001)).sum()); pt = np.clip(raw, 0.001, 0.999); s = run_cell(pc, pt, a.B_firth, stream(k))
        P('| %s | %s | %d | %+.2f | %.3f | %.3f／%.3f | %.3f／%.3f | %s |' % (pn_, rn_, clipped, np.polyfit(zs, pt - pc, 1)[0] * 100, s['reject_nominal'], s['card_draft4_nominal'], s['card_draft4_holm_first'], s['card_D1_nominal'], s['card_D1_holm_first'], '%.3f' % s['clause_rate_among_fit'] if s['clause_rate_among_fit'] is not None else '—'))
P(''); P('- 所要 %.0f 秒。' % (time.time() - t0)); P('')

# ---------------- W29
say('W29'); t0 = time.time()


def pool(pc, pt, B, rng):
    p = np.ones(B); s2 = np.zeros(B, bool); zp = np.zeros(B); sm = np.zeros(B, bool); ok = np.zeros(B, bool)
    for i in range(B):
        r = one(rng.binomial(n, pc), rng.binomial(n, pt))
        if r['status'] == 'ok':
            ok[i] = True; p[i] = r['p']; s2[i] = r['sat2']; zp[i] = r['zpt']; sm[i] = r['same']
    return dict(p=p, sat2=s2, zpt=zp, same=sm, ok=ok)


pc_s = np.linspace(0.35, 0.70, 6); pt_s = pc_s + 0.25; assert pt_s.max() < 0.999
POOLS = {'eff15': pool(np.full(6, 0.5), np.full(6, 0.5) + 0.15 * (zs - z4) / zspan, a.pool_other, stream(302)), 'scale': pool(pc_s, pt_s, a.pool_scale, stream(303))}
P('## W29. Holm の水準の三つの読みと、35 対比の族としての誤確証率（Ge2 重大3・Gr1 重大1 (d)・Cl2 3-1・Cl3 中11「α の制御には影響しない」）'); P('')
P('- 手続き: (i) β₃ の Holm で棄却された対比に、その対比が棄却された段の水準 α/(m−r+1) で pt 差の傾きを当てる（正本の「β₃ を棄却した Holm の調整水準と同じ」の逐次の読み）／(ii) pt 差の傾きは初段 α/m に固定／(iii) 対比ごとの IUT の p 値 p*＝max(p_β, p_pt)（向きが違えば 1）に Holm を当てる。いずれも解釈条項の発火で確証から外す。')
P('- 前提の整理: β₃ が真に 0 の対比（β₃ の帰無）については、(i)(ii) の確証は β₃ の Holm の棄却の部分集合なので、族としての誤りは Holm が α 以下に抑える（シミュレーションは要らない）。(iii) は各対比の p* が「β₃=0 または pt 差の傾き=0」の和集合の帰無に対して妥当な p 値なので、Holm で両種の帰無をまとめて α 以下に抑える。**問いが残るのは「β₃≠0 だが pt 差の傾き=0」（尺度依存の帰無）の対比**で、これは β₃ の帰無ではないため、(i)(ii) では Holm の保証の外にある。')
P('- 上限の型（尺度依存の帰無 35 本がすべて「β₃ は必ず棄却・pt 差の傾きの z は独立な標準正規・向きの一致は 1/2」とした理想化）: (i) 1−Π_{j=1..35}(1−α/(2j))＝**%.4f**・(ii) 1−(1−α/(2·35))^35＝%.4f・(iii) p*＝p_pt となり Holm の最初の棄却の事象は (ii) と同じ型で %.4f。' % (1 - np.prod([1 - ALPHA / (2 * j) for j in range(1, M + 1)]), 1 - (1 - ALPHA / (2 * M)) ** M, 1 - (1 - ALPHA / (2 * M)) ** M))
P('- 対比ごとの資源プール（Firth PPLRT・格子の `one()`・族は独立な対比の再標本で組む）: 効果（対照 0.5・処置の pt 差が z に沿って +15 pt）%d・**尺度依存の帰無**（対照 0.35→0.70・処置＝対照＋25 pt で pt 差一定・切り詰めなし・β₃≠0）%d。' % (a.pool_other, a.pool_scale))
for nm, pl in POOLS.items():
    okm = pl['ok']; pp = 2 * norm.sf(np.abs(pl['zpt']))
    P('  - %s: 当てはめ %.3f・β₃ 名目 %.3f・β₃ 初段 %.4f・解釈条項 %.3f・pt 差の傾きが名目で立ち向きが一致 %.4f・札 D1 初段 %.4f・「β₃ 名目 ∧ pt 名目 ∧ 向き一致 ∧ 条項なし」の行数 %d（誤確証になりうる行の解像度）。' % (
        nm, okm.mean(), (pl['p'] < ALPHA).mean(), (pl['p'] < ALPHA / M).mean(), pl['sat2'][okm].mean() if okm.any() else float('nan'), ((np.abs(pl['zpt']) > z_nom) & pl['same'] & okm).mean(),
        ((pl['p'] < ALPHA / M) & ~pl['sat2'] & (np.abs(pl['zpt']) > z_h1) & pl['same'] & okm).mean(), int(((pl['p'] < ALPHA) & (pp < ALPHA) & pl['same'] & ~pl['sat2'] & okm).sum())))
P(''); P('| 族の構成（35 対比） | 手続き | 尺度依存の帰無の中で少なくとも 1 本の誤確証（95% 半幅） | 誤確証の期待本数 | 効果のある対比の到達（平均） |'); P('|---|---|---|---|---|')


def holm(pm):
    Rr, m_ = pm.shape; order = np.argsort(pm, axis=1); ps = np.take_along_axis(pm, order, axis=1); thr = ALPHA / (m_ - np.arange(m_)); cum = np.cumprod(ps <= thr[None, :], axis=1).astype(bool)
    rej = np.zeros_like(cum); np.put_along_axis(rej, order, cum, axis=1); rank = np.zeros_like(order); np.put_along_axis(rank, order, np.broadcast_to(np.arange(m_), (Rr, m_)).copy(), axis=1)
    return rej, rank


SCEN = [('尺度依存の帰無 35', [('scale', 35, True)]), ('効果 10＋尺度依存の帰無 25', [('eff15', 10, False), ('scale', 25, True)]), ('効果 20＋尺度依存の帰無 15', [('eff15', 20, False), ('scale', 15, True)]),
        ('効果 30＋尺度依存の帰無 5', [('eff15', 30, False), ('scale', 5, True)])]
rg = stream(400)
for sn, comp in SCEN:
    cols = {key: [] for key in ('p', 'sat2', 'zpt', 'same')}; isnull = []
    for pk, cnt, nul in comp:
        idx = rg.integers(0, len(POOLS[pk]['p']), size=(a.R, cnt))
        for key in cols:
            cols[key].append(POOLS[pk][key][idx])
        isnull += [nul] * cnt
    pm, s2, zp, sm = (np.concatenate(cols[key], axis=1) for key in ('p', 'sat2', 'zpt', 'same')); isnull = np.array(isnull)
    rej, rank = holm(pm); lvl = ALPHA / (M - rank); zc = norm.isf(lvl / 2)
    c1 = rej & ~s2 & sm & (np.abs(zp) > zc); c2 = rej & ~s2 & sm & (np.abs(zp) > z_h1)
    ppt = 2 * norm.sf(np.abs(zp)); pstar = np.where(sm, np.maximum(pm, ppt), 1.0); rej3, _ = holm(pstar); c3 = rej3 & ~s2
    for lab, cc in (('(i) 棄却した段の水準', c1), ('(ii) 初段に固定', c2), ('(iii) max-p に Holm', c3)):
        fal = cc[:, isnull]; fw = float((fal.sum(1) > 0).mean()); pw = float(cc[:, ~isnull].mean()) if (~isnull).any() else float('nan')
        P('| %s | %s | %.4f（±%.4f） | %.4f | %s |' % (sn, lab, fw, hw(fw, a.R), float(fal.sum(1).mean()), '—' if math.isnan(pw) else '%.3f' % pw))
P(''); P('- 所要 %.0f 秒。' % (time.time() - t0)); P('')

# ---------------- W30
say('W30'); t0 = time.time()
pc = np.linspace(0.3, 0.9, 6); pt, clipped = treat(pc, 0.15, 0.0, 1.0); s = run_cell(pc, pt, a.B_cell, stream(500))
g = next(r for r in PG['D'] if r['pattern'] == 'ctrl_rising' and abs(r['d0_pt'] - 0.15) < 1e-9 and r['delta_pt_32B_minus_4B'] == 0)
P('## W30. 格子の一行の追試（対照 0.3→0.9・d0=15 pt・Δ=0）（Cl2 (1-8)「0.42±0.02」・Cl3 1-4「0.363」）'); P('')
P('- 本部（B=%d・別の子ストリーム）: 名目 p<α %.4f（Wilson %s）・札 草案4 名目／初段 %.4f／%.4f・札 D1 初段 %.4f。格子（B=%d）: 名目 p<α %.4f（%s）・札 草案4 名目／初段 %.4f／%.4f・札 D1 初段 %.4f。切り詰め %d 規模。所要 %.0f 秒。' % (
    a.B_cell, s['reject_nominal'], s['reject_nominal_ci95'], s['card_draft4_nominal'], s['card_draft4_holm_first'], s['card_D1_holm_first'], g['B'], g['reject_nominal'], g['reject_nominal_ci95'], g['card_draft4_nominal'], g['card_draft4_holm_first'], g['card_D1_holm_first'], clipped, time.time() - t0))
P('- 読み: 転記行 D の「d0=15 pt で 0.376／0.056」は札 草案4（名目有意 ∧ 解釈条項の非発火）で、名目の β₃ 棄却率ではない。Cl2 の「名目有意率 0.42±0.02」は名目の β₃ 棄却率（格子の同じ行の値）と比べるべき量。'); P('')

# ---------------- W31
say('W31'); t0 = time.time()
S = T['identity_screen']; bN1 = T['bases_4B2507_api'][S['scenario']]; arms = S['compared_arms']
probs = np.array([[bN1[x]['k'] / bN1[x]['n'], bN1[x]['refuse'] / bN1[x]['n'], bN1[x]['format_fail'] / bN1[x]['n'], 0.0] for x in arms]); probs[:, 3] = 1 - probs[:, :3].sum(1); napi = [bN1[x]['n'] for x in arms]


def fail_rate(shift, mode, B, rng, nloc):
    diffs = []
    for i, x in enumerate(arms):
        pl = probs[i].copy()
        if x in shift:
            s_ = shift[x] / 100.0; pl[0] += s_; pl[3] -= s_
            if pl[3] < 0:
                pl[1] += pl[3]; pl[3] = 0.0
            assert np.all(pl >= -1e-12)
        loc = rng.multinomial(nloc, pl, size=B) / nloc; api = np.broadcast_to(probs[i], (B, 4)) if mode == 'api_fixed' else rng.multinomial(napi[i], probs[i], size=B) / napi[i]
        diffs.append(np.abs(loc[:, :3] - api[:, :3]) * 100)
    D = np.concatenate(diffs, axis=1); return float(((D.mean(1) > S['mean_pt']) | (D.max(1) > S['max_pt'])).mean())


P('## W31. 門0.5 の検出側（手元 n=%d・主判定＝30 個の絶対差の平均 %s 超または最大 %s 超・B=%d）（Cl1 軽15・Cl3 重点9）' % (S['n'], S['mean_pt'], S['max_pt'], a.B_id)); P('')
P('| 手元で真にずれる腕と破局率のずれ | API を固定 | API も再標本 |'); P('|---|---|---|')
CASES = [('なし（帰無・転記行 N の再現）', {}), ('N −10 pt', {'N': -10}), ('N −12 pt', {'N': -12}), ('N −15 pt', {'N': -15}), ('N −22 pt（門0 の下見 −21.7／−24.2 の近傍）', {'N': -22}),
         ('Onull −15 pt', {'Onull': -15}), ('Ncold −15 pt', {'Ncold': -15}), ('Lneg −15 pt', {'Lneg': -15}), ('全 10 腕 +5 pt（あり得る側だけ）', {x: 5 for x in arms if probs[arms.index(x), 0] + 0.05 <= 1 and probs[arms.index(x), 3] >= 0.05})]
k = 600
for nm, sh in CASES:
    k += 1; P('| %s | %.4f | %.4f |' % (nm, fail_rate(sh, 'api_fixed', a.B_id, stream(k), S['n']), fail_rate(sh, 'api_resampled', a.B_id, stream(k + 50), S['n'])))
P(''); P('- 破局率のずれは「その他の答え」の欄との間で動かす（refuse・書式外は動かさない。その他が足りなければ refuse から）。所要 %.0f 秒。' % (time.time() - t0)); P('')

O += ['', '本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(a.out, 'w', encoding='utf-8', newline='\n').write('\n'.join(O) + '\n')
say('written %s (%d lines)' % (a.out, len(O)))
