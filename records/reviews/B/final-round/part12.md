# 器材のソース（逐語・参照）（参照・関わる問い (b)(g)・機械生成・2026-09-19 01:57 UTC）

## `tools/design_facts_B.py`（SHA16 6E3C0F8D9F3F66E5・360 行）

```python
# -*- coding: utf-8 -*-
"""design_facts_B.py v7 —— 段階 B の設計事実（転記行 A〜I）を `design/contrasts-B.json`（正本）と門0 の実測・記録から機械生成する（2026-09-18）。
v6 からの変更（v7・2026-09-18〜19）: **版の名を v6 のまま上げていなかった**（裁定 D87〜D132 の直しが入っていた——品質床の相手を段ごとに走らせる規模の数え直し〔D88〕・品質床の相手のセッション〔D92〕・転記行 C を門と同じ模擬で出す〔D119・同値の帯の式は D98〕・転記行 E の対の見方〔採否表 P373・裁定 D130〕・転記行 G の器の一覧と転記行 I の数え方〔束の前の点検〕）。この版で v7 に上げた（前例は採否表 P239）。
v3 からの変更（検分の二段目・四票の採否 P212〜P256・裁定 D75〜D86）: 転記行 C に**選定 × 確証の合成検出力**（採否表 P229）と、抽出場面を二層に分けない前提の但し書き（P245）、
同点の割り方を正本の登録（無作為・selection.tie_break）に合わせた模擬を置く（P228）。転記行 D に **S4 の反証の検出力**と三分岐の線（裁定 D81）を足す。
転記行 E に二標本で比べる旨と相手の共有の注（P256）、転記行 I に「全腕」の意味と内訳（P256）と決定性の検査で二度保存する容量（P235）を足す。費用の停止の倍率は正本 `cost` から引く（P251）。
v1（草案4）からの変更: 保留 AUC の置換帯と門1 の誤判率（転記行 C）を廃し、**選定の雑音**（層 × 係数の 9 候補を調整走行 n=100 × 抽出場面で選ぶときの取り違え）に置き換えた。
検出力（D）は族ごとの m（4・4・8）で印字する。品質床（E）は同じ腕の無操作との二標本・18 セルで数える。費用（F）はバッチ 16 の記録値から出し直す。
A 規模／B 対比／C 選定の雑音と同値の帯／D v 対 v_random の検出力／E 品質床／F 費用と時間／G 凍結射程と器材の対応表／H seed・tag／I 活性保存の容量。
v2 からの変更（段階 B 設計の検分の一段目・採否表 P190〜P211・裁定 D68〜D74）: 転記行 B の実引数の位置ずれを直し、正本から数え直して突き合わせる自己検査を足した。
同値の帯を差の分散から出す。品質床の射程を「選ばれた層 × 係数で本走行に出るすべての介入の腕」に広げる。モンテカルロの反復数と区間を印字し、品質床の帰無発火率は厳密値にする。
出力: records/B/design-facts-B.md と同 .json。
"""
import os, sys, re, json, math, hashlib, datetime
VERSION = 'v7'     # 出力に印字する版（v6 まで docstring と出力の版が食い違っていた・2026-09-19）
import numpy as np
from scipy.stats import fisher_exact, binom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vprime_power import make_power
import runs_B                      # 同値の帯は門と同じ関数を呼ぶ（裁定 D119）


def make_power_cached(n):
    """vprime_power.make_power と同じ規則（両側 Fisher・全数列挙・二分探索）。棄却域の境目は alpha ごとに一度だけ求めて使い回す。"""
    bounds = {}

    def get_bounds(alpha):
        if alpha not in bounds:
            yh_l, yl_l = [], []
            for x in range(n + 1):
                lo, hi = x, n + 1
                while lo < hi:
                    mid = (lo + hi) // 2
                    if fisher_exact([[x, n - x], [mid, n - mid]])[1] <= alpha:
                        hi = mid
                    else:
                        lo = mid + 1
                yh_l.append(lo)
                lo, hi = -1, x - 1
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    if fisher_exact([[x, n - x], [mid, n - mid]])[1] <= alpha:
                        lo = mid
                    else:
                        hi = mid - 1
                yl_l.append(lo)
            bounds[alpha] = (yh_l, yl_l)
        return bounds[alpha]

    def power(p0, p1, alpha):
        px = binom.pmf(np.arange(n + 1), n, p0)
        py = binom.pmf(np.arange(n + 1), n, p1)
        cdf = np.cumsum(py)
        yh, yl = get_bounds(alpha)
        tot = 0.0
        for x in range(n + 1):
            if px[x] < 1e-14:
                continue
            tot += px[x] * ((1 - cdf[yh[x] - 1] if yh[x] <= n else 0.0) + (cdf[yl[x]] if yl[x] >= 0 else 0.0))
        return tot
    return power
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
T = json.loads(rd('design', 'contrasts-B.json'))
HF = json.loads(rd('records', 'A', 'hf-models-A.json'))
ADC = rd('records', 'reviews', 'AB', 'round-claudeai', 'adoption-table-AB-claudeai.md')
n, nt = T['n_main'], T['n_tune']
SC, EX = T['scenarios'], T['extraction_scenarios']
CAND = T['selection']['candidates']['count']
rng = np.random.default_rng(20260918)
sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
F = {}
fmt = lambda x: format(x, ',')


def one(pat, text, flags=0):
    m = re.search(pat, text, flags)
    if not m:
        sys.exit('見つからない: %s' % pat)
    return m


# ---- A: 規模（正本の腕とセルから数える） ----
t_id = T['identity_screen']['arms'] * T['identity_screen']['n']
t_tune = CAND * len(T['selection']['tune']['arms']) * nt * len(T['selection']['tune']['scenarios'])
q_items = T['quality_floor']['items']
interv = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)               # 介入のある腕（本走行）
base_of_arm = lambda a: re.split(r'[+\-]v', a)[0]
noop_bases = sorted({base_of_arm(a) for a in interv})
q_cells_sel = T['quality_floor']['selection_cells']                                   # 選定の段（土台 × 層 × 係数）
q_cells_post = len(interv) - len(T['quality_floor']['arms'])                          # 選ばれた組で、残りの介入の腕に当てる（裁定 D69）
q_noop_sel = len(T['quality_floor']['arms'])                                          # 選定の段の相手（確証族の二つの土台の無操作）
q_noop_post = len(noop_bases)                                                         # 選定後の段の相手（介入の腕の土台すべての無操作）
q_cells = q_cells_sel + q_cells_post + q_noop_sel + q_noop_post                       # 相手の無操作は**段ごとに走らせる**（裁定 D88）
t_q = q_items * q_cells
t_main = sum(c['n'] for c in T['main_cells'])
t_all = t_id + t_tune + t_main + t_q
F['A'] = {'text': '規模: 同一性選別（transformers 経路・%d 腕 × n=%d × N1）%s／調整走行 %s（%d 候補〔層 %d × 係数 %d〕× %d 腕 × n=%d × 抽出場面 %d）／本走行 %s（%d セル＝場面 × 腕・n=%d・%s）／品質床 %s 問（%d 問 × 〔選定 %d セル＋選ばれた組での残りの介入 %d セル＋無操作の相手 %d セル〔選定の段〕＋%d セル〔選定後の段・裁定 D88〕〕）＝**合計 %s 試行**。'
          % (T['identity_screen']['arms'], T['identity_screen']['n'], fmt(t_id), fmt(t_tune), CAND, len(T['selection']['candidates']['layers']), len(T['selection']['candidates']['coefficients']),
             len(T['selection']['tune']['arms']), nt, len(T['selection']['tune']['scenarios']), fmt(t_main), len(T['main_cells']), n,
             '・'.join('%s %d 腕' % (sc, len(T['arms']['by_scenario'][sc])) for sc in SC), fmt(t_q), q_items, q_cells_sel, q_cells_post, q_noop_sel, q_noop_post, fmt(t_all)),
          'data': {'identity': t_id, 'tune': t_tune, 'main': t_main, 'quality': t_q, 'quality_cells': q_cells, 'quality_noop_selection': q_noop_sel, 'quality_noop_post': q_noop_post, 'total': t_all}}

# ---- B: 対比 ----
fam = T['families']
ids_all = [c['id'] for F_ in T['families'].values() for c in F_['contrasts']] + [c['id'] for v in T['descriptive_families'].values() for c in v.get('contrasts', [])]
nd = sum(len(v.get('contrasts', [])) for v in T['descriptive_families'].values())
base_line = lambda a: '・'.join('%s %d/%d' % (sc, T['bases_4B2507_api_stageVp'][sc][a]['k'], T['bases_4B2507_api_stageVp'][sc][a]['n']) for sc in SC)
b_vals = {'confirmed': sum(x['m'] for x in fam.values()), 'sub': fam['B_sub']['m'], 'add': fam['B_add']['m'], 'cross': fam['B_cross']['m'],
          'desc': nd, 'vs_noop': len(T['descriptive_families']['B_desc_vs_noop']['contrasts']),
          'rand_vs_noop': len(T['descriptive_families']['B_desc_rand_vs_noop']['contrasts']),
          'O_sub': len(T['descriptive_families']['B_desc_O_sub']['contrasts']),
          'textdiff': len(T['descriptive_families']['B_desc_textdiff']['contrasts']),
          'S4': len(T['descriptive_families']['B_desc_S4']['contrasts']),
          'random': T['random_control']['count'],
          'dup': len(ids_all) - len(set(ids_all))}
F['B'] = {'text': '対比: 確証 %d（減算 %d・加算 %d・交差 %d・v 対 v_random・両側 Fisher・全分母・Holm は族ごと〔m=%s〕・上界 %.2f〔和・族は相手の腕を共有するので独立でない〕）・記述 %d（無操作との差 %d・ランダム方向 対 無操作 %d・O 減算 %d・実在する腕対の差方向 %d〔td 対 ランダム方向と v̂ 対 td〕・S4 の反証 %d）・ランダム方向 %d 本（層ごとに v̂ のノルムに合わせる・合併して一腕）・id 重複 %d。土台の 4B-2507 既測（V′・全分母）: O-Ncold %s／Onull %s／Osec-Ncold（S4） %d/%d。'
          % (b_vals['confirmed'], b_vals['sub'], b_vals['add'], b_vals['cross'], '・'.join(str(fam[k]['m']) for k in ('B_sub', 'B_add', 'B_cross')), T['alpha_upper'],
             b_vals['desc'], b_vals['vs_noop'], b_vals['rand_vs_noop'], b_vals['O_sub'], b_vals['textdiff'], b_vals['S4'], b_vals['random'], b_vals['dup'],
             base_line('O-Ncold'), base_line('Onull'), T['descriptive_families']['B_desc_S4']['base_4B2507'], T['descriptive_families']['B_desc_S4']['base_n']),
          'data': b_vals}
# 自己検査（採否表 P190）: 印字した転記行 B の数を、正本から数え直した値と突き合わせる
_checks = [('確証 (\d+)（', b_vals['confirmed']), ('・記述 (\d+)（', b_vals['desc']), ('無操作との差 (\d+)', b_vals['vs_noop']),
           ('ランダム方向 対 無操作 (\d+)', b_vals['rand_vs_noop']),
           ('O 減算 (\d+)', b_vals['O_sub']), ('実在する腕対の差方向 (\d+)', b_vals['textdiff']), ('S4 の反証 (\d+)', b_vals['S4']),
           ('ランダム方向 (\d+) 本', b_vals['random']), ('id 重複 (\d+)', b_vals['dup'])]
for _pat, _want in _checks:
    _got = int(one(_pat, F['B']['text']).group(1))
    assert _got == _want, ('転記行 B の印字と正本の値が違う', _pat, _got, _want)

# ---- C: 選定の雑音と同値の帯（裁定 D68 の決め方で出し直す） ----
tune_n = nt * len(T['selection']['tune']['scenarios'])                       # 腕あたりの合計（抽出場面をまとめる）
bx = T['bases_4B2507_api_stageVp']
base_tune = sum(bx[sc]['Onull']['k'] for sc in EX) / sum(bx[sc]['Onull']['n'] for sc in EX)   # 抽出場面の Onull の既測率（基底の目安）
se_single = 100 * math.sqrt(2 * base_tune * (1 - base_tune) / tune_n)        # 一つの候補の低下幅の標準誤差
se_diff = 100 * math.sqrt(4 * base_tune * (1 - base_tune) / tune_n)          # 候補どうしの差の標準誤差（採否表 P191）
z = 1.96
REPS = 20000
# **帯は門と同じ模擬で出す**（裁定 D119・2026-09-18）。前は素の区間の式（z × 候補どうしの差の標準誤差）で
# ±13.8 pt を印字し、しかも**正本の鍵の名を出典に付けていた**。正本の当該の条はその式を「採らない」と明記しており、
# 門の模擬は 21.5 pt を出す（系統外の検分で捕まった・採否表 P339）。
_band = runs_B.equivalence_band(tune_n, tune_n, base_tune, T['selection']['candidates']['count'],
                                reps=REPS, seed=[T['seeds']['tiebreak'] + 1, 0])
band_pt = _band['q95_pt']
CANDS = T['selection']['candidates']['count']
D_PICK = 10.0                                                               # 模擬に置く真の低下幅（設計の値ではない）


def pick_prob(pos, reps=REPS, delta=None):
    """裁定 D68 の決め方（点推定が最大の候補を採る・同点は正本 selection.tie_break の登録どおり無作為に割る）で、
    真に効く候補を選べる割合。pos は格子の位置。delta は真の低下幅（pt・既定は D_PICK）。"""
    eff = np.zeros(CANDS)
    eff[pos] = (D_PICK if delta is None else delta) / 100.0
    kv = rng.binomial(tune_n, np.clip(base_tune - eff, 0.001, 0.999)[None, :], size=(reps, CANDS))
    kr = rng.binomial(tune_n, base_tune, size=(reps, CANDS))
    d = (kr - kv).astype(float)
    d += (d == d.max(axis=1, keepdims=True)) * rng.random(d.shape) * 1e-6      # 同点は無作為に割る（selection.tie_break）
    hit = (np.argmax(d, axis=1) == pos).mean()
    half = z * math.sqrt(hit * (1 - hit) / reps)
    return float(hit), float(half)


positions = (0, CANDS // 2, CANDS - 1)
picks = {pos: pick_prob(pos) for pos in positions}
p_mid, half_mid = picks[CANDS // 2]
p_flat = 1.0 / CANDS
F['C'] = {'text': '選定の雑音と同値の帯（層 × 係数の %d 候補・調整走行は腕あたり n=%d〔n=%d × 抽出場面 %d〕・基底は抽出場面の Onull の既測 %.3f）: 一つの候補の低下幅の標準誤差 %.1f pt・**候補どうしの差の標準誤差 %.1f pt**・**同値の帯（%g%%）は %.1f pt**（正本 `selection.equivalence_band` のとおり候補横断の最大統計量・門と同じ模擬・モンテカルロ %s 回・%g%% 区間 ±%.4f pt）。**素の区間の式なら ±%.1f pt** だが、正本はその式を「候補が九つある多重性を見ないので採らない」と明記している（裁定 D98・D119）。裁定 D68 の決め方（点推定が最大の候補を採る）で、真の低下幅が %.0f pt の候補が格子の中ほどにあるとき、それを選べる割合は %.3f（モンテカルロ %s 回・%g%% 区間 ±%.3f）。格子の位置による差は %s。全候補が同じ（帰無）なら %.3f（＝候補数の逆数）。**選定の低下幅は効果量ではない**（本走行の確証族だけが効果を言う・正本 selection.no_effect_size）。'
          % (CANDS, tune_n, nt, len(T['selection']['tune']['scenarios']), base_tune, se_single, se_diff,
             100 * T['selection']['equivalence_ci'], band_pt, format(REPS, ','), 100 * T['selection']['equivalence_ci'],
             _band['mc_half_pt'], z * se_diff,
             D_PICK, p_mid, fmt(REPS), 100 * T['selection']['equivalence_ci'], half_mid,
             '・'.join('位置 %d で %.3f' % (pos, picks[pos][0]) for pos in positions), p_flat) +
          '同点は無作為に割る（正本 selection.tie_break）。**この行の雑音は抽出場面をまとめた一つの率で出しており、場面の二層（N1・S1）の違いを無視している**（採否表 P245）。'
          '合成の検出力（選定 × 確証）は転記行 D。',
          'data': {'tune_n_per_arm': tune_n, 'base': round(base_tune, 4), 'se_single_pt': round(se_single, 2), 'se_diff_pt': round(se_diff, 2),
                   'band_pt': round(band_pt, 2), 'reps': REPS, 'pick_by_position': {str(k): [round(v[0], 4), round(v[1], 4)] for k, v in picks.items()},
                   'pick_null': p_flat, 'candidates': CANDS, 'delta_pt': D_PICK}}

# ---- D: v 対 v_random の検出力（両側・族ごとの m） ----
pw = make_power_cached(n)
ref = make_power(n)
for chk in ((0.30, 0.45, 0.05), (0.69, 0.54, 0.05 / 4)):
    assert abs(pw(*chk) - ref(*chk)) < 1e-12, chk   # 速い実装が元の実装と一致することを確かめる
rows = []
FAMARM = [('B_sub', 'O-Ncold'), ('B_add', 'Onull'), ('B_cross', 'O-Ncold'), ('B_cross', 'Onull')]
for famkey, arm in FAMARM:
    m = fam[famkey]['m']
    for sc in SC:
        b = bx[sc][arm]['k'] / bx[sc][arm]['n']
        for d in (0.10, 0.15, 0.20):
            for sign, lab_d in ((-1, 'down'), (+1, 'up')):
                p2 = b + sign * d
                for alpha, lab_a in ((0.05, 'nominal'), (0.05 / m, 'holm_first')):
                    rows.append({'family': famkey, 'base_arm': arm, 'scenario': sc, 'base': round(b, 3), 'delta_pt': int(d * 100),
                                 'side': lab_d, 'alpha': lab_a, 'm': m,
                                 'power': (None if not (0.0 <= p2 <= 1.0) else round(pw(b, p2, alpha), 3)),
                                 'out_of_range': not (0.0 <= p2 <= 1.0)})
g = lambda f, a, sc, d, side, lab: next(r['power'] for r in rows if r['family'] == f and r['base_arm'] == a and r['scenario'] == sc and r['delta_pt'] == d and r['side'] == side and r['alpha'] == lab)
bs = lambda a, sc: bx[sc][a]['k'] / bx[sc][a]['n']


def two_side(f, a, sc, d):
    """場面 sc・土台 a・幅 d pt の両側を「上 x／y・下 z／w」の形にする（率の外に出る側は「測れない」）"""
    out = []
    for side, name in (('up', '上'), ('down', '下')):
        nom, hol = g(f, a, sc, d, side, 'nominal'), g(f, a, sc, d, side, 'holm_first')
        out.append('%s %s' % (name, ('率の外' if nom is None else '%.2f／%.2f' % (nom, hol))))
    return '・'.join(out)


D_MAIN, D_SMALL = 15, 10
lo_sc = lambda a: min(SC, key=lambda sc: bs(a, sc))
hi_sc = lambda a: max(SC, key=lambda sc: bs(a, sc))


def ci_excl_zero(p_a, p_b, nn=None, zz=1.96):
    """二標本の pt 差の 95% Wald 区間が零を外す（下がる側）確率。二項の畳み込みで厳密（正本 B_desc_S4.adjudication の量）。"""
    nn = nn or n
    k = np.arange(nn + 1)
    pa, pb = binom.pmf(k, nn, p_a), binom.pmf(k, nn, p_b)
    ra = k / nn
    diff = ra[:, None] - ra[None, :]
    se = np.sqrt(ra[:, None] * (1 - ra[:, None]) / nn + ra[None, :] * (1 - ra[None, :]) / nn)
    se = np.where(se == 0, np.inf, se)
    w = pa[:, None] * pb[None, :]
    return float(w[(diff + zz * se) < 0].sum())


S4F = T['descriptive_families']['B_desc_S4']
s4_base = S4F['base_4B2507'] / S4F['base_n']
S4_PT, S4_POWER_MIN = S4F['three_way']['effect_pt'], S4F['three_way']['power_min']
s4_pow = {d: round(ci_excl_zero(max(s4_base - d / 100, 0.001), s4_base), 3) for d in (S4_PT, D_MAIN)}
# 合成の検出力（選定 × 確証・採否表 P229）
# 選定の側は調整走行の基底（抽出場面をまとめた Onull）、確証の側は**族の登録された検定**（両側 Fisher・Holm の初段）を
# 加算族の各場面の基底で出す（場面によって基底が違うので幅で示す）。
combined, combined_by_sc = {}, {}
for d in (5, D_SMALL, D_MAIN):
    p_pick = pick_prob(CANDS // 2, delta=d)[0]
    by_sc = {sc: pw(bs('Onull', sc), max(bs('Onull', sc) - d / 100, 0.001), 0.05 / fam['B_add']['m']) for sc in SC}
    combined_by_sc[d] = {sc: round(p_pick * v, 3) for sc, v in by_sc.items()}
    combined[d] = (round(p_pick * min(by_sc.values()), 3), round(p_pick * max(by_sc.values()), 3), round(p_pick, 3))
F['D'] = {'text': 'v 対 v_random の検出力（両側 Fisher・n=%d 対 %d・全数列挙・名目／Holm の初段〔族ごとの m〕・上がる側と下がる側の両方）: '
          '**減算族**（土台 O-Ncold・m=%d）は基底が %s %.3f 〜 %s %.3f。%s の ±%d pt は %s、%s の ±%d pt は %s。'
          '**加算族**（土台 Onull・m=%d）は基底が %s %.3f 〜 %s %.3f。%s の ±%d pt は %s、%s の ±%d pt は %s。'
          '**交差族**（m=%d）は初段の水準が下がる（%s の O-Ncold・±%d pt は %s）。'
          '±%d pt は中間の基底でも初段に届かない（%s の Onull・%s）。床に近い基底では下がる側が率の外に出て測れない（読み条項の余地の条項）。'
          '**S4 の反証**（記述・(6b) の腕 対 ランダム方向・基底 %.4f・裁定 D81 の三分岐）: 真の低下 %d pt を %g%% 区間で捕まえる確率は %.3f、%d pt では %.3f。'
          '区間が零を含んだとき、%d pt の検出力が %g 以上なら「下がらなかった（封印は当たり）」、下回れば「当否を言わない」。'
          '**合成の検出力**（選定で正しい組を選ぶ割合 × 加算族の初段〔両側 Fisher・場面ごとの基底で最小〜最大〕・採否表 P229）: 真の低下 %s。選定の側は調整走行の基底で出した割合である。'
          % (n, n, fam['B_sub']['m'], lo_sc('O-Ncold'), bs('O-Ncold', lo_sc('O-Ncold')), hi_sc('O-Ncold'), bs('O-Ncold', hi_sc('O-Ncold')),
             lo_sc('O-Ncold'), D_MAIN, two_side('B_sub', 'O-Ncold', lo_sc('O-Ncold'), D_MAIN), hi_sc('O-Ncold'), D_MAIN, two_side('B_sub', 'O-Ncold', hi_sc('O-Ncold'), D_MAIN),
             fam['B_add']['m'], lo_sc('Onull'), bs('Onull', lo_sc('Onull')), hi_sc('Onull'), bs('Onull', hi_sc('Onull')),
             lo_sc('Onull'), D_MAIN, two_side('B_add', 'Onull', lo_sc('Onull'), D_MAIN), hi_sc('Onull'), D_MAIN, two_side('B_add', 'Onull', hi_sc('Onull'), D_MAIN),
             fam['B_cross']['m'], EX[0], D_MAIN, two_side('B_cross', 'O-Ncold', EX[0], D_MAIN), D_SMALL, EX[1], two_side('B_add', 'Onull', EX[1], D_SMALL),
             s4_base, S4_PT, 100 * 0.95, s4_pow[S4_PT], D_MAIN, s4_pow[D_MAIN], S4_PT, S4_POWER_MIN,
             '・'.join('%d pt で %.3f〜%.3f（選定の割合 %.3f）' % (d, v[0], v[1], v[2]) for d, v in sorted(combined.items()))),
          'data': dict(rows=rows, s4_power={str(k): v for k, v in s4_pow.items()}, s4_base=round(s4_base, 4),
                       combined_power={str(k): list(v) for k, v in combined.items()},
                       combined_power_by_scenario={str(k): v for k, v in combined_by_sc.items()})}

# ---- E: 品質床（同じ腕の無操作との二標本・厳密値・裁定 D69 の射程） ----
q, thr = q_items, -T['quality_floor']['threshold_pt'] / 100


def q_null_exact(p):
    """同じ真の正答率の二腕で、差が閾値以下（不合格）になる確率。二項の畳み込みで厳密に計算する。"""
    pmf = binom.pmf(np.arange(q + 1), q, p)
    d = np.arange(q + 1)[:, None] - np.arange(q + 1)[None, :]
    return float(((d <= -thr * q) * (pmf[:, None] * pmf[None, :])).sum())


def q_power_exact(p, drop):
    pmf_a = binom.pmf(np.arange(q + 1), q, p)
    pmf_b = binom.pmf(np.arange(q + 1), q, max(p - drop, 0.01))
    d = np.arange(q + 1)[:, None] - np.arange(q + 1)[None, :]
    return float(((d.T <= -thr * q) * (pmf_a[:, None] * pmf_b[None, :])).sum())


def q_null_paired(delta):
    """**対の見方**（採否表 P373・2026-09-19）: 同じ問いを貪欲に解くので、介入が何もしなければ答えは一致する。
    無操作と腕で正誤が入れ替わる問いの割合を delta とし、入れ替わりは正→誤と誤→正が半々（正答率は変わらない帰無）とする。
    入れ替わった問いの数 D ~ 二項(q, delta)、そのうち正→誤 L ~ 二項(D, 1/2)、差＝(D − 2L)/q が閾値以下になる確率を厳密に数える。"""
    pD = binom.pmf(np.arange(q + 1), q, delta)
    tot = 0.0
    for D, w in enumerate(pD):
        if w < 1e-300:
            continue
        L = np.arange(D + 1)
        tot += w * float(binom.pmf(L, D, 0.5)[(D - 2 * L) <= -thr * q].sum())
    return tot


null_q = {p: q_null_exact(p) for p in (0.5, 0.7, 0.9)}
null_pair = {dl: q_null_paired(dl) for dl in (0.05, 0.1, 0.2, 0.3)}
pow_q = {p: q_power_exact(p, D_PICK * 1.5 / 100) for p in (0.7, 0.9)}
acc_line = lambda d: '・'.join('%g で %.4f' % (k, v) for k, v in d.items())
pow_line = lambda d: '・'.join('%g で %.3f' % (k, v) for k, v in d.items())
F['E'] = {'text': '品質床（%d 問・%d pt・分子＝正答数・分母＝%d・相手＝同じ腕の無操作・境目はちょうどの値を不合格とする）: 射程は選定の %d セル（土台 × 層 × 係数）に加え、選ばれた組での残りの介入 %d セルと、相手の無操作 %d セル（選定の段）＋%d セル（選定後の段・裁定 D88）。帰無発火率（同じ真の正答率で閾値以下になる確率・二項の畳み込みで厳密）は正答率 %s。真の低下 %.0f pt を捕まえる確率は %s。帰無で誤って不合格にする期待セル数は、正答率 %g で %.2f（%d セル）。課題の出所・版・ライセンス・断片の SHA は凍結時に記帳する（裁定 D66・候補は器材の整備の段）。'
          '**相手の無操作は段 × 土台 × セッションごとに一つ**で、ここではセッションが段に一つの見込みで数えている（裁定 D92・走行が分かれれば相手のセルはその数だけ増える）。'
          '**同じ問いを使うが二標本で比べる**ので、この行の帰無発火率と検出力は対にして読むより保守側である（採否表 P256）。**対の見方**（採否表 P373）: 無操作と腕で正誤が入れ替わる問いの割合 δ ごとの帰無発火率（入れ替わりは正→誤と誤→正が半々・厳密）は %s。介入が何もしなければ δ は零で、帰無の不合格も零である——**二標本の値は上限**である。無操作の相手は土台ごとに一つで多くのセルが共有するため、帰無での不合格は相関して塊で出る。課題は**無操作の正答率が %g 以上**のものを選ぶ（裁定 D85）。'
          % (q, T['quality_floor']['threshold_pt'], q, q_cells_sel, q_cells_post, q_noop_sel, q_noop_post, acc_line(null_q), D_PICK * 1.5, pow_line(pow_q), 0.7, q_cells * null_q[0.7], q_cells,
             '・'.join('δ=%g で %.4f' % (k, v) for k, v in null_pair.items()), T['quality_floor']['base_min']),
          'data': {'null_exact': {str(k): v for k, v in null_q.items()}, 'null_paired': {str(k): v for k, v in null_pair.items()},
                   'power_exact': {str(k): v for k, v in pow_q.items()},
                   'cells': q_cells, 'cells_selection': q_cells_sel, 'cells_post': q_cells_post, 'cells_noop_selection': q_noop_sel, 'cells_noop_post': q_noop_post}}

# ---- F: 費用と時間（バッチの記録値から出し直す・◐） ----
BATCHES = (1, 8, 16, 24)
rec = one('バッチ %d なら (\d+) ユニット・%d で (\d+)・%d で (\d+)・%d で (\d+)' % BATCHES, ADC)
rec_trials = int(one(r'草案4 の (\d[\d,]*) 試行でバッチ', ADC).group(1).replace(',', ''))
b16, b1 = int(rec.group(1 + BATCHES.index(T['runner']['batch']))), int(rec.group(1 + BATCHES.index(1)))
u16, u1 = t_all * b16 / rec_trials, t_all * b1 / rec_trials
STOP_RATIO = T['cost']['stop_rule']['multiplier']
F['F'] = {'text': '費用と時間（草案4 の巡の追い問いの記録: %s 試行でバッチ %d なら %d ユニット・同時 %d 本なら %d ユニット。本草案の %s 試行に比例で当てた見込み ◐）: バッチ %d で **≈%s ユニット**・同時 %d 本なら ≈%s ユニット。品質床の %s 問は出力が短く、場面の試行より軽い（比例は上振れの側）。実測は調整走行の最初のセッションで取り、転記行を置き換える。費用の停止規則は段階 A と同じ型（見込みの %g 倍で登録者の再裁定）。'
          % (fmt(rec_trials), T['runner']['batch'], b16, 1, b1, fmt(t_all), T['runner']['batch'], fmt(round(u16)), 1, fmt(round(u1)), fmt(t_q), STOP_RATIO),
          'data': {'trials': t_all, 'units_batch': round(u16, 1), 'units_single': round(u1, 1), 'batch': T['runner']['batch'],
                   'source_trials': rec_trials, 'source_units': {str(k): int(rec.group(1 + BATCHES.index(k))) for k in BATCHES}, 'stop_ratio': STOP_RATIO}}

# ---- G・H・I ----
_TOOLS_G = ('make_contrasts_B.py', 'rules_B.py', 'runs_B.py', 'direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'gate_B.py', 'analyze_B.py',
            'layers_B.py', 'control_chart_B.py', 'design_facts_B.py', 'integrity_B.py', 'sample_inspection_B.py', 'build_report_B.py', 'freeze_B.py',
            'synth_B.py', 'dry_run_B.py', 'mutation_B.py', 'endtoend_B.py', 'build_draftB.py')
exists = [f for f in _TOOLS_G if os.path.exists(os.path.join(REPO, 'tools', f))]
absent = [f for f in _TOOLS_G if f not in exists]
F['G'] = {'text': '凍結射程と器材の対応表: 腕・場面・族・選定規則・報告の決まり→`contrasts-B.json`／判定の規則（S4・区間・refuse 門・等質性・td の特異性・api_error の門・門の並び）→`rules_B.py`／'
                  '同一性→`identity_screen`（段階 A と共用）／方向の抽出・主位置の活性の保存・‖v̂‖ と ‖h‖ の比→`direction_B.py`／加減・ランダム方向・品質床の生成と採点→`steer_B.py`／'
                  '一つのセルの走行と、試行の記録・生テキスト・副位置の活性の書き出し→`run_stageB_local.py`／門1 と選定→`gate_B.py`／族・門・記述の族・td の特異性・等質性→`analyze_B.py`／'
                  '副位置の読み→`layers_B.py`／管理図→`control_chart_B.py`／転記行→`design_facts_B.py`／整合と抽出検査→`integrity_B.py`・`sample_inspection_B.py`／'
                  '報告→雛形・`build_report_B.py`・`report_lint.py`／凍結→`freeze_B.py`／合成データ・経路・変異・端から端まで→`synth_B.py`・`dry_run_B.py`・`mutation_B.py`・`endtoend_B.py`。'
                  '採点の経路は凍結した走行器の関数と、段階 A の様式の器の関数を呼ぶ（再実装しない）。**実在する器材: %s。実在しない器材: %s。**'
                  '**まだ書いていない器・骨組みの器は正本 `disclosure.items` に列挙する**（相をまたいだ走らせ方の順・Colab での起動・品質床の走行の本体）。'
          % ('・'.join('`%s`' % f for f in exists), '・'.join('`%s`' % f for f in absent) or 'なし')}
F['H'] = {'text': 'seed: %s。tag: %s。' % (json.dumps(T['seeds'], ensure_ascii=False), json.dumps(T['tags'], ensure_ascii=False))}
m4 = HF['models']['4B-2507']
hid = m4['hidden_size']
kb = hid * 2 / 1024
n_layers_saved = len(T['selection']['candidates']['layers'])
EXS = T['extraction_scenarios']
prompt_vecs = len(T['arms']['panel']) * len(EXS) * n_layers_saved      # 抽出器が実際に取るのは**抽出場面**の主位置（2026-09-19 に数え方を直した）
resp_gib = (t_tune + t_main) * n_layers_saved * hid * 2 / 2**30
F['I'] = {'text': '活性保存（4B-2507・hidden %d・bf16・凍結 %d 層）: 主位置（プロンプトの最終トークン）は腕 × 場面 × 層ごとに一度だけ保存する——%d 本 × %.1f KB ＝ %.1f MB（試行に依らないため試行ごとに保存しない・草案4 からの変更）。副位置（応答トークン平均）は試行ごとに保存する——%s 試行 × %d 層 ≈ %.2f GiB（Drive）。重み %.2f GiB＋バッチ %d の生成の活性が L4 の %g%% の内側かは、調整走行の最初のセッションで実測する ◐。'
          '**内訳と「全腕」の意味**（採否表 P256）: 副位置の %s 試行は調整走行 %s ＋ 本走行 %s で、同一性選別の %s は含まない。主位置の %d 本は**前置きの腕 %d 本 × 抽出場面 %d × 層 %d**（介入の腕は含まない・方向は抽出場面から作る）。'
          '前は場面を全場面で数えており、抽出器が実際に取る本数と違っていた（2026-09-19 の直しの監査）。'
          '決定性の検査は主位置を**二度**保存して突き合わせるので、主位置の容量は %.1f MB になる（裁定 D77 の前段・採否表 P235）。'
          % (hid, n_layers_saved, prompt_vecs, kb, prompt_vecs * kb / 1024, fmt(t_tune + t_main), n_layers_saved, resp_gib, m4['safetensors_gib'], T['runner']['batch'], 90,
             fmt(t_tune + t_main), fmt(t_tune), fmt(t_main), fmt(t_id), prompt_vecs, len(T['arms']['panel']), len(EXS), n_layers_saved, 2 * prompt_vecs * kb / 1024),
          'data': {'prompt_vectors': prompt_vecs, 'response_gib': round(resp_gib, 3), 'prompt_mb_twice': round(2 * prompt_vecs * kb / 1024, 2)}}

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
os.makedirs(os.path.join(REPO, 'records', 'B'), exist_ok=True)
csha = sha(rd('design', 'contrasts-B.json'))
json.dump({'generated_utc': now, 'tool': 'tools/design_facts_B.py %s' % VERSION, 'contrasts_sha16': csha, 'facts': F},
          open(os.path.join(REPO, 'records', 'B', 'design-facts-B.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
L = ['# 段階 B 設計事実（機械生成・`tools/design_facts_B.py` %s・%s UTC・正本 contrasts-B.json SHA16 %s）' % (VERSION, now, csha), '']
for k in 'ABCDEFGHI':
    L.append('- **転記行 %s** — %s' % (k, F[k]['text']))
    L.append('')
L.append('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
open(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[design_facts_B] written records/B/design-facts-B.{md,json} | 合計 %s 試行・バッチ %d で ≈%.0f ユニット' % (fmt(t_all), T['runner']['batch'], u16))
```

## `tools/build_draftB.py`（SHA16 FF872CA64E127E9A・123 行）

```python
# -*- coding: utf-8 -*-
"""build_draftB.py v3 —— 段階 B の草案（と報告雛形）を原稿から組み立てる（段階 A の `build_draftA.py` の型・凍結した A の器は触らない）。
- **一覧の展開**（v2・2026-09-19）: 原稿の行 `{{list:正本のキー}}` を、正本の一覧の各項目の箇条に展開する（開示の五項目を依頼文と草案が同じ出所から組むため・裁定 D117）。
- **裁定の台帳の検査**（v2・採否表 P376）: 原稿が引く裁定番号がすべて正本 `decisions` にあることを確かめ、無ければ止める。
  数の走査器 `numbers_lint.py` は段階 A の凍結した器なので、この検査はそちらに足さず、B の組み立て器に置く。
- **採否表の引用の照合**（v3・2026-09-19）: 組み上げた文書・正本・器材の「採否表 P…」を `tools/citations_B.py` で採否表と照らし、
  違反があれば終了コードを立てる（束の前の点検で、手で打った引用の誤りが多数見つかったため）。
- 組み立ての前に `numbers_lint` の束縛検査（原稿の数はキー参照か構造）を走らせ、違反があれば止める。
- 原稿の {{正本のキー}} を正本 JSON の値で置換する。
- 草案（--kind draft）: §6 の「- **転記行 X** — 〔転記行 X〕」を設計事実 JSON の逐語で置換し、本文中の〔転記行 X〕を「〔転記行 X・§6〕」に改め、§6-補 に置換の記録を印字する。
- 組み立ての後に登録検査（文書と正本の説明文）と生成器の文字列リテラル検査を走らせ、報告を書く。違反があれば終了コードを立てる。
用法: python tools/build_draftB.py --kind draft --src design/design-stageB-draft5.src.md --out design/design-stageB-draft5.md --label 草案5B --lint-report records/B/numbers-lint-draft5B.md
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numbers_lint as NL
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--kind', choices=['draft', 'template'], required=True)
ap.add_argument('--src', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--label', required=True)
ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'B', 'design-facts-B.json'))
ap.add_argument('--facts-md', default=os.path.join(REPO, 'records', 'B', 'design-facts-B.md'))
ap.add_argument('--json', default=os.path.join(REPO, 'design', 'contrasts-B.json'))
ap.add_argument('--lint-report', required=True)
ap.add_argument('--gen', nargs='*', default=[os.path.join(REPO, 'tools', nm) for nm in ('make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py')])
a = ap.parse_args()
sha = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
rel = lambda p: os.path.relpath(p, REPO).replace('\\', '/')
J = json.load(open(a.json, encoding='utf-8'))
s = open(a.src, encoding='utf-8').read().replace('\r\n', '\n')

# ---- 一覧の展開（v2） ----
def _expand(m):
    v, e = NL.resolve(J, m.group(1))
    if e or not isinstance(v, list) or not v:
        sys.exit('一覧の展開に失敗した（正本に一覧が無いか空）: %s' % m.group(0))
    return '\n'.join('- %s' % x for x in v)


s = re.sub(r'^\{\{list:([^{}]+)\}\}$', _expand, s, flags=re.M)

# ---- 裁定の台帳の検査（v2・採否表 P376） ----
LED = set((J.get('decisions') or {}).keys())
_refs = {('D%s%s' % (m.group(1), m.group(2) or ''), 'D%s' % m.group(1))
         for m in re.finditer(r'(?<![A-Za-z\d])D(\d+)(?:\s*\(([a-z])\))?', s)}
_bad_led = sorted({full for full, bare in _refs if full not in LED and bare not in LED})
if _bad_led:
    sys.exit('原稿が引く裁定番号が正本の台帳（decisions）に無い: %s' % '・'.join(_bad_led))

pre = NL.check_src(J, s)
if pre:
    print('[build_draftB] 束縛検査で止めた（原稿の数がキー参照か構造でない・%d 件）' % len(pre))
    for i, tok, ctx in pre[:80]:
        print('  原稿 %d 行: %s … %s' % (i, tok, ctx))
    sys.exit(1)
bound, used, errs = NL.bind(J, s)
assert not errs, errs

out, replaced = [], []
if a.kind == 'draft':
    FJ = json.load(open(a.facts, encoding='utf-8'))
    F = FJ['facts']
    assert FJ['contrasts_sha16'] == sha(a.json), ('設計事実の正本 SHA16 と現行の正本が不一致', FJ['contrasts_sha16'], sha(a.json))
    in6 = False
    for l in bound.split('\n'):
        if l.startswith('## 6.'):
            in6 = True
            out.append('## 6. 転記行（機械生成・逐語・`%s`〔SHA16 %s〕・`%s`〔SHA16 %s〕・生成 %s UTC・器 `tools/design_facts_B.py`）'
                       % (rel(a.facts_md), sha(a.facts_md), rel(a.json), FJ['contrasts_sha16'], FJ['generated_utc']))
            continue
        if in6 and l.startswith('## 7.'):
            in6 = False
            out += ['### 6-補 原稿 → %s の組み立ての記録（機械）' % a.label, '',
                    '- 置換した転記行: %s（器 `tools/build_draftB.py`・原稿 `%s` SHA16 %s）。本文中の転記行の置き字は §6 への参照に改めた。' % ('・'.join(replaced), rel(a.src), sha(a.src)),
                    '- 束縛: 原稿のキー参照を正本 `%s`（SHA16 %s）の値で置換した（異なるキーの種類は下の検査の記録に印字する）。組み立ての前に束縛検査、後に登録検査と生成器の文字列の検査を走らせた（`%s`）。' % (rel(a.json), sha(a.json), rel(a.lint_report)),
                    '- 数値の出所はすべて正本と設計事実の JSON であり、散文に手計算の数を残さない。', '', l]
            continue
        if in6:
            m = re.match(r'^- \*\*転記行 ([A-Z])\*\* — 〔転記行 ([A-Z])〕$', l)
            if m:
                assert m.group(1) == m.group(2), l
                k = m.group(1)
                assert k in F, ('設計事実に無い転記行', k)
                out.append('- **転記行 %s** — %s' % (k, F[k]['text']))
                replaced.append(k)
                continue
            out.append(l)
            continue
        out.append(re.sub(r'〔転記行 ([A-Z])〕', lambda mm: '〔転記行 %s・§6〕' % mm.group(1), l))
    missing = [k for k in F if k not in replaced]
    assert not missing, ('§6 に置かれていない転記行', missing)
else:
    out = bound.split('\n')

t = '\n'.join(out)
assert not re.search(r'〔転記行 [A-Z]〕', t), '置き残しがある'
assert not re.search(r'\{\{[^{}]*\}\}', t), '束縛の置き残しがある'
open(a.out, 'w', encoding='utf-8', newline='\n').write(t)
print('[build_draftB] written %s sha16 %s | 転記行 %s | 束縛したキーの種類 %d' % (rel(a.out), sha(a.out), ''.join(replaced) or '—', len(used)))
# 束縛検査は**一覧を展開した後の原稿**に当てる（展開の印そのものは正本のキー参照ではない・v2）。
# 展開した原稿は一時の置き場に書き、検査の記録の中の置き場の名は元の原稿の名に戻す。
import tempfile as _tf
_d = _tf.mkdtemp(prefix='draftB_')
_exp = os.path.join(_d, os.path.basename(a.src))
open(_exp, 'w', encoding='utf-8', newline='\n').write(s)
nb, L = NL.report(J, a.json, _exp, [a.out], a.gen)
L = [l.replace(os.path.relpath(_exp).replace('\\', '/'), rel(a.src) + '（一覧を展開した後）') for l in L]
import shutil as _sh
_sh.rmtree(_d, ignore_errors=True)
os.makedirs(os.path.dirname(a.lint_report), exist_ok=True)
open(a.lint_report, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('\n'.join(L[:12 + min(60, nb)]))
# ---- 採否表の引用の照合（v3） ----
import citations_B as _CB
_cv, _ct = _CB.check_all(REPO, docs=[rel(a.out)])
print('[build_draftB] 採否表の引用の照合（`tools/citations_B.py` %s）: 引用 %d・裁定の照合 %d・札の照合 %d・違反 %d'
      % (_CB.VERSION, _ct['cit'], _ct['d'], _ct['label'], len(_cv)))
for _w, _p, _y in _cv[:40]:
    print('  違反: %s %s —— %s' % (_w, _p, _y))
sys.exit(1 if (nb or _cv) else 0)
```
