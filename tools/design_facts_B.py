# -*- coding: utf-8 -*-
"""design_facts_B.py v3 —— 段階 B の設計事実（転記行 A〜I）を `design/contrasts-B.json`（草案5B の正本）と門0 の実測・記録から機械生成する（2026-09-18）。
v1（草案4）からの変更: 保留 AUC の置換帯と門1 の誤判率（転記行 C）を廃し、**選定の雑音**（層 × 係数の 9 候補を調整走行 n=100 × 抽出場面で選ぶときの取り違え）に置き換えた。
検出力（D）は族ごとの m（4・4・8）で印字する。品質床（E）は同じ腕の無操作との二標本・18 セルで数える。費用（F）はバッチ 16 の記録値から出し直す。
A 規模／B 対比／C 選定の雑音と同値の帯／D v 対 v_random の検出力／E 品質床／F 費用と時間／G 凍結射程と器材の対応表／H seed・tag／I 活性保存の容量。
v2 からの変更（段階 B 設計の検分の一段目・採否表 P190〜P211・裁定 D68〜D74）: 転記行 B の実引数の位置ずれを直し、正本から数え直して突き合わせる自己検査を足した。
同値の帯を差の分散から出す。品質床の射程を「選ばれた層 × 係数で本走行に出るすべての介入の腕」に広げる。モンテカルロの反復数と区間を印字し、品質床の帰無発火率は厳密値にする。
出力: records/B/design-facts-B.md と同 .json。
"""
import os, sys, re, json, math, hashlib, datetime
import numpy as np
from scipy.stats import fisher_exact, binom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vprime_power import make_power


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
q_cells = q_cells_sel + q_cells_post + len(noop_bases)                                # ＋相手の無操作
t_q = q_items * q_cells
t_main = sum(c['n'] for c in T['main_cells'])
t_all = t_id + t_tune + t_main + t_q
F['A'] = {'text': '規模: 同一性選別（transformers 経路・%d 腕 × n=%d × N1）%s／調整走行 %s（%d 候補〔層 %d × 係数 %d〕× %d 腕 × n=%d × 抽出場面 %d）／本走行 %s（%d セル＝場面 × 腕・n=%d・%s）／品質床 %s 問（%d 問 × 〔選定 %d セル＋選ばれた組での残りの介入 %d セル＋無操作の相手 %d セル〕）＝**合計 %s 試行**。'
          % (T['identity_screen']['arms'], T['identity_screen']['n'], fmt(t_id), fmt(t_tune), CAND, len(T['selection']['candidates']['layers']), len(T['selection']['candidates']['coefficients']),
             len(T['selection']['tune']['arms']), nt, len(T['selection']['tune']['scenarios']), fmt(t_main), len(T['main_cells']), n,
             '・'.join('%s %d 腕' % (sc, len(T['arms']['by_scenario'][sc])) for sc in SC), fmt(t_q), q_items, q_cells_sel, q_cells_post, len(noop_bases), fmt(t_all)),
          'data': {'identity': t_id, 'tune': t_tune, 'main': t_main, 'quality': t_q, 'quality_cells': q_cells, 'total': t_all}}

# ---- B: 対比 ----
fam = T['families']
ids_all = [c['id'] for F_ in T['families'].values() for c in F_['contrasts']] + [c['id'] for v in T['descriptive_families'].values() for c in v.get('contrasts', [])]
nd = sum(len(v.get('contrasts', [])) for v in T['descriptive_families'].values())
base_line = lambda a: '・'.join('%s %d/%d' % (sc, T['bases_4B2507_api_stageVp'][sc][a]['k'], T['bases_4B2507_api_stageVp'][sc][a]['n']) for sc in SC)
b_vals = {'confirmed': sum(x['m'] for x in fam.values()), 'sub': fam['B_sub']['m'], 'add': fam['B_add']['m'], 'cross': fam['B_cross']['m'],
          'desc': nd, 'vs_noop': len(T['descriptive_families']['B_desc_vs_noop']['contrasts']),
          'O_sub': len(T['descriptive_families']['B_desc_O_sub']['contrasts']),
          'textdiff': len(T['descriptive_families']['B_desc_textdiff']['contrasts']),
          'S4': len(T['descriptive_families']['B_desc_S4']['contrasts']),
          'random': T['random_control']['count'],
          'dup': len(ids_all) - len(set(ids_all))}
F['B'] = {'text': '対比: 確証 %d（減算 %d・加算 %d・交差 %d・v 対 v_random・両側 Fisher・全分母・Holm は族ごと〔m=%s〕・上界 %.2f）・記述 %d（無操作との差 %d・O 減算 %d・実在する腕対の差方向 %d・S4 の反証 %d）・ランダム方向 %d 本（層ごとにノルム一致・合併して一腕）・id 重複 %d。土台の 4B-2507 既測（V′・全分母）: O-Ncold %s／Onull %s／Osec-Ncold（S4） %d/%d。'
          % (b_vals['confirmed'], b_vals['sub'], b_vals['add'], b_vals['cross'], '・'.join(str(fam[k]['m']) for k in ('B_sub', 'B_add', 'B_cross')), T['alpha_upper'],
             b_vals['desc'], b_vals['vs_noop'], b_vals['O_sub'], b_vals['textdiff'], b_vals['S4'], b_vals['random'], b_vals['dup'],
             base_line('O-Ncold'), base_line('Onull'), T['descriptive_families']['B_desc_S4']['base_4B2507'], T['descriptive_families']['B_desc_S4']['base_n']),
          'data': b_vals}
# 自己検査（採否表 P190）: 印字した転記行 B の数を、正本から数え直した値と突き合わせる
_checks = [('確証 (\d+)（', b_vals['confirmed']), ('・記述 (\d+)（', b_vals['desc']), ('無操作との差 (\d+)', b_vals['vs_noop']),
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
band_pt = z * se_diff
REPS = 20000
CANDS = T['selection']['candidates']['count']
D_PICK = 10.0                                                               # 模擬に置く真の低下幅（設計の値ではない）


def pick_prob(pos, reps=REPS):
    """裁定 D68 の決め方（点推定が最大の候補を採る）で、真に効く候補を選べる割合。pos は格子の位置。"""
    eff = np.zeros(CANDS)
    eff[pos] = D_PICK / 100.0
    kv = rng.binomial(tune_n, np.clip(base_tune - eff, 0.001, 0.999)[None, :], size=(reps, CANDS))
    kr = rng.binomial(tune_n, base_tune, size=(reps, CANDS))
    hit = (np.argmax((kr - kv) / tune_n, axis=1) == pos).mean()
    half = z * math.sqrt(hit * (1 - hit) / reps)
    return float(hit), float(half)


positions = (0, CANDS // 2, CANDS - 1)
picks = {pos: pick_prob(pos) for pos in positions}
p_mid, half_mid = picks[CANDS // 2]
p_flat = 1.0 / CANDS
F['C'] = {'text': '選定の雑音と同値の帯（層 × 係数の %d 候補・調整走行は腕あたり n=%d〔n=%d × 抽出場面 %d〕・基底は抽出場面の Onull の既測 %.3f）: 一つの候補の低下幅の標準誤差 %.1f pt・**候補どうしの差の標準誤差 %.1f pt**・同値の帯（%g%%）は差 ±%.1f pt（正本 selection.equivalence_band の量）。裁定 D68 の決め方（点推定が最大の候補を採る）で、真の低下幅が %.0f pt の候補が格子の中ほどにあるとき、それを選べる割合は %.3f（モンテカルロ %s 回・%g%% 区間 ±%.3f）。格子の位置による差は %s。全候補が同じ（帰無）なら %.3f（＝候補数の逆数）。**選定の低下幅は効果量ではない**（本走行の確証族だけが効果を言う・正本 selection.no_effect_size）。'
          % (CANDS, tune_n, nt, len(T['selection']['tune']['scenarios']), base_tune, se_single, se_diff, 100 * T['selection']['equivalence_ci'], band_pt,
             D_PICK, p_mid, fmt(REPS), 100 * T['selection']['equivalence_ci'], half_mid,
             '・'.join('位置 %d で %.3f' % (pos, picks[pos][0]) for pos in positions), p_flat),
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
F['D'] = {'text': 'v 対 v_random の検出力（両側 Fisher・n=%d 対 %d・全数列挙・名目／Holm の初段〔族ごとの m〕・上がる側と下がる側の両方）: '
          '**減算族**（土台 O-Ncold・m=%d）は基底が %s %.3f 〜 %s %.3f。%s の ±%d pt は %s、%s の ±%d pt は %s。'
          '**加算族**（土台 Onull・m=%d）は基底が %s %.3f 〜 %s %.3f。%s の ±%d pt は %s、%s の ±%d pt は %s。'
          '**交差族**（m=%d）は初段の水準が下がる（%s の O-Ncold・±%d pt は %s）。'
          '±%d pt は中間の基底でも初段に届かない（%s の Onull・%s）。床に近い基底では下がる側が率の外に出て測れない（読み条項の余地の条項）。'
          % (n, n, fam['B_sub']['m'], lo_sc('O-Ncold'), bs('O-Ncold', lo_sc('O-Ncold')), hi_sc('O-Ncold'), bs('O-Ncold', hi_sc('O-Ncold')),
             lo_sc('O-Ncold'), D_MAIN, two_side('B_sub', 'O-Ncold', lo_sc('O-Ncold'), D_MAIN), hi_sc('O-Ncold'), D_MAIN, two_side('B_sub', 'O-Ncold', hi_sc('O-Ncold'), D_MAIN),
             fam['B_add']['m'], lo_sc('Onull'), bs('Onull', lo_sc('Onull')), hi_sc('Onull'), bs('Onull', hi_sc('Onull')),
             lo_sc('Onull'), D_MAIN, two_side('B_add', 'Onull', lo_sc('Onull'), D_MAIN), hi_sc('Onull'), D_MAIN, two_side('B_add', 'Onull', hi_sc('Onull'), D_MAIN),
             fam['B_cross']['m'], EX[0], D_MAIN, two_side('B_cross', 'O-Ncold', EX[0], D_MAIN), D_SMALL, EX[1], two_side('B_add', 'Onull', EX[1], D_SMALL)),
          'data': rows}

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


null_q = {p: q_null_exact(p) for p in (0.5, 0.7, 0.9)}
pow_q = {p: q_power_exact(p, D_PICK * 1.5 / 100) for p in (0.7, 0.9)}
acc_line = lambda d: '・'.join('%g で %.4f' % (k, v) for k, v in d.items())
pow_line = lambda d: '・'.join('%g で %.3f' % (k, v) for k, v in d.items())
F['E'] = {'text': '品質床（%d 問・%d pt・分子＝正答数・分母＝%d・相手＝同じ腕の無操作・境目はちょうどの値を不合格とする）: 射程は選定の %d セル（土台 × 層 × 係数）に加え、選ばれた組での残りの介入 %d セルと相手の無操作 %d セル（裁定 D69）。帰無発火率（同じ真の正答率で閾値以下になる確率・二項の畳み込みで厳密）は正答率 %s。真の低下 %.0f pt を捕まえる確率は %s。帰無で誤って不合格にする期待セル数は、正答率 %g で %.2f（%d セル）。課題の出所・版・ライセンス・断片の SHA は凍結時に記帳する（裁定 D66・候補は器材の整備の段）。'
          % (q, T['quality_floor']['threshold_pt'], q, q_cells_sel, q_cells_post, len(noop_bases), acc_line(null_q), D_PICK * 1.5, pow_line(pow_q), 0.7, q_cells * null_q[0.7], q_cells),
          'data': {'null_exact': {str(k): v for k, v in null_q.items()}, 'power_exact': {str(k): v for k, v in pow_q.items()},
                   'cells': q_cells, 'cells_selection': q_cells_sel, 'cells_post': q_cells_post, 'cells_noop': len(noop_bases)}}

# ---- F: 費用と時間（バッチの記録値から出し直す・◐） ----
BATCHES = (1, 8, 16, 24)
rec = one('バッチ %d なら (\d+) ユニット・%d で (\d+)・%d で (\d+)・%d で (\d+)' % BATCHES, ADC)
rec_trials = int(one(r'草案4 の (\d[\d,]*) 試行でバッチ', ADC).group(1).replace(',', ''))
b16, b1 = int(rec.group(1 + BATCHES.index(T['runner']['batch']))), int(rec.group(1 + BATCHES.index(1)))
u16, u1 = t_all * b16 / rec_trials, t_all * b1 / rec_trials
STOP_RATIO = 1.25
F['F'] = {'text': '費用と時間（草案4 の巡の追い問いの記録: %s 試行でバッチ %d なら %d ユニット・同時 %d 本なら %d ユニット。本草案の %s 試行に比例で当てた見込み ◐）: バッチ %d で **≈%s ユニット**・同時 %d 本なら ≈%s ユニット。品質床の %s 問は出力が短く、場面の試行より軽い（比例は上振れの側）。実測は調整走行の最初のセッションで取り、転記行を置き換える。費用の停止規則は段階 A と同じ型（見込みの %g 倍で登録者の再裁定）。'
          % (fmt(rec_trials), T['runner']['batch'], b16, 1, b1, fmt(t_all), T['runner']['batch'], fmt(round(u16)), 1, fmt(round(u1)), fmt(t_q), STOP_RATIO),
          'data': {'trials': t_all, 'units_batch': round(u16, 1), 'units_single': round(u1, 1), 'batch': T['runner']['batch'],
                   'source_trials': rec_trials, 'source_units': {str(k): int(rec.group(1 + BATCHES.index(k))) for k in BATCHES}, 'stop_ratio': STOP_RATIO}}

# ---- G・H・I ----
exists = sorted(f for f in ('make_contrasts_B.py', 'design_facts_B.py', 'direction_B.py', 'steer_B.py', 'analyze_B.py', 'integrity_B.py', 'sample_inspection_B.py', 'build_report_B.py', 'freeze_B.py', 'boot_stageB.py')
                if os.path.exists(os.path.join(REPO, 'tools', f)))
F['G'] = {'text': '凍結射程と器材の対応表: 腕・場面・族・選定規則・報告の決まり→`contrasts-B.json`／同一性→`identity_screen`（段階 A と共用）／方向の抽出と層ごとの記述→`direction_B.py`／加減・ランダム方向・品質床・強制デコード→`steer_B.py`／族・検閲・refuse 門・様式門・層別の副次→`analyze_B.py`／転記行→`design_facts_B.py`／整合と抽出検査→`integrity_B.py`・`sample_inspection_B.py`／報告→雛形・`build_report_B.py`・`report_lint.py`／凍結→`freeze_B.py`。採点の経路は凍結した走行器の関数を import する。**本草案の時点で実在する器材: %s。残りは凍結の前に整備する。**'
          % '・'.join('`%s`' % f for f in exists)}
F['H'] = {'text': 'seed: %s。tag: %s。' % (json.dumps(T['seeds'], ensure_ascii=False), json.dumps(T['tags'], ensure_ascii=False))}
m4 = HF['models']['4B-2507']
hid = m4['hidden_size']
kb = hid * 2 / 1024
n_layers_saved = len(T['selection']['candidates']['layers'])
prompt_vecs = len(T['arms']['panel']) * len(SC) * n_layers_saved
resp_gib = (t_tune + t_main) * n_layers_saved * hid * 2 / 2**30
F['I'] = {'text': '活性保存（4B-2507・hidden %d・bf16・凍結 %d 層）: 主位置（プロンプトの最終トークン）は腕 × 場面 × 層ごとに一度だけ保存する——%d 本 × %.1f KB ＝ %.1f MB（試行に依らないため試行ごとに保存しない・草案4 からの変更）。副位置（応答トークン平均）は試行ごとに保存する——%s 試行 × %d 層 ≈ %.2f GiB（Drive）。重み %.2f GiB＋バッチ %d の生成の活性が L4 の %g%% の内側かは、調整走行の最初のセッションで実測する ◐。'
          % (hid, n_layers_saved, prompt_vecs, kb, prompt_vecs * kb / 1024, fmt(t_tune + t_main), n_layers_saved, resp_gib, m4['safetensors_gib'], T['runner']['batch'], 90),
          'data': {'prompt_vectors': prompt_vecs, 'response_gib': round(resp_gib, 3)}}

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
os.makedirs(os.path.join(REPO, 'records', 'B'), exist_ok=True)
csha = sha(rd('design', 'contrasts-B.json'))
json.dump({'generated_utc': now, 'tool': 'tools/design_facts_B.py v2', 'contrasts_sha16': csha, 'facts': F},
          open(os.path.join(REPO, 'records', 'B', 'design-facts-B.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
L = ['# 段階 B 設計事実（機械生成・`tools/design_facts_B.py` v2・%s UTC・正本 contrasts-B.json SHA16 %s）' % (now, csha), '']
for k in 'ABCDEFGHI':
    L.append('- **転記行 %s** — %s' % (k, F[k]['text']))
    L.append('')
L.append('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
open(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[design_facts_B] written records/B/design-facts-B.{md,json} | 合計 %s 試行・バッチ %d で ≈%.0f ユニット' % (fmt(t_all), T['runner']['batch'], u16))
