# -*- coding: utf-8 -*-
"""design_facts_B.py v2 —— 段階 B の設計事実（転記行 A〜I）を `design/contrasts-B.json`（草案5B の正本）と門0 の実測・記録から機械生成する（2026-09-18）。
v1（草案4）からの変更: 保留 AUC の置換帯と門1 の誤判率（転記行 C）を廃し、**選定の雑音**（層 × 係数の 9 候補を調整走行 n=100 × 抽出場面で選ぶときの取り違え）に置き換えた。
検出力（D）は族ごとの m（4・4・8）で印字する。品質床（E）は同じ腕の無操作との二標本・18 セルで数える。費用（F）はバッチ 16 の記録値から出し直す。
A 規模／B 対比／C 選定の雑音と同値の帯／D v 対 v_random の検出力／E 品質床／F 費用と時間／G 凍結射程と器材の対応表／H seed・tag／I 活性保存の容量。
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
t_q = q_items * (T['quality_floor']['cells'] + len(T['quality_floor']['arms']))       # 層 × 係数 × 腕＋無操作の相手
t_main = sum(c['n'] for c in T['main_cells'])
t_all = t_id + t_tune + t_main + t_q
F['A'] = {'text': '規模: 同一性選別（transformers 経路・%d 腕 × n=%d × N1）%s／調整走行 %s（%d 候補〔層 %d × 係数 %d〕× %d 腕 × n=%d × 抽出場面 %d）／本走行 %s（%d セル＝場面 × 腕・n=%d・%s）／品質床 %s 問（%d 問 × 〔%d セル＋無操作 %d〕）＝**合計 %s 試行**。'
          % (T['identity_screen']['arms'], T['identity_screen']['n'], fmt(t_id), fmt(t_tune), CAND, len(T['selection']['candidates']['layers']), len(T['selection']['candidates']['coefficients']),
             len(T['selection']['tune']['arms']), nt, len(T['selection']['tune']['scenarios']), fmt(t_main), len(T['main_cells']), n,
             '・'.join('%s %d 腕' % (sc, len(T['arms']['by_scenario'][sc])) for sc in SC), fmt(t_q), q_items, T['quality_floor']['cells'], len(T['quality_floor']['arms']), fmt(t_all)),
          'data': {'identity': t_id, 'tune': t_tune, 'main': t_main, 'quality': t_q, 'total': t_all}}

# ---- B: 対比 ----
fam = T['families']
nd = sum(len(v.get('contrasts', [])) for v in T['descriptive_families'].values())
base_line = lambda a: '・'.join('%s %d/%d' % (sc, T['bases_4B2507_api_stageVp'][sc][a]['k'], T['bases_4B2507_api_stageVp'][sc][a]['n']) for sc in SC)
F['B'] = {'text': '対比: 確証 %d（減算 %d・加算 %d・交差 %d・v 対 v_random・両側 Fisher・全分母・Holm は族ごと〔m=%s〕・上界 %.2f）・記述 %d（無操作との差 %d・O 減算 %d・実在する腕対の差方向 %d・S4 の反証 %d）・ランダム方向 %d 本（層ごとにノルム一致・合併して一腕）・id 重複 0。土台の 4B-2507 既測（V′・全分母）: O-Ncold %s／Onull %s／Osec-Ncold（S4） %d/%d。'
          % (sum(x['m'] for x in fam.values()), fam['B_sub']['m'], fam['B_add']['m'], fam['B_cross']['m'], '・'.join(str(fam[k]['m']) for k in ('B_sub', 'B_add', 'B_cross')), 3 * 0.05,
             nd, len(T['descriptive_families']['B_desc_vs_noop']['contrasts']), len(T['descriptive_families']['B_desc_O_sub']['contrasts']),
             len(T['descriptive_families']['B_desc_textdiff']['contrasts']), len(T['descriptive_families']['B_desc_S4']['contrasts']), T['random_control']['count'],
             base_line('O-Ncold'), base_line('Onull'), T['descriptive_families']['B_desc_S4']['base_4B2507'], T['descriptive_families']['B_desc_S4']['base_n'])}

# ---- C: 選定の雑音と同値の帯（保留 AUC の置換帯を置き換える） ----
tune_n = nt * len(T['selection']['tune']['scenarios'])                       # 腕あたりの合計（抽出場面をまとめる）
bx = T['bases_4B2507_api_stageVp']
base_tune = sum(bx[sc]['Onull']['k'] for sc in EX) / sum(bx[sc]['Onull']['n'] for sc in EX)   # 抽出場面の Onull の既測率（基底の目安）
se_pt = 100 * math.sqrt(2 * base_tune * (1 - base_tune) / tune_n)
band_pt = 1.96 * se_pt


def pick_prob(effects_pt, reps=20000):
    """真の低下幅（pt・候補ごと）を与えたとき、観測された低下幅の最大で最良の候補を選ぶ確率"""
    eff = np.array(effects_pt) / 100.0
    best = int(np.argmax(eff))
    pv = np.clip(base_tune - eff, 0.001, 0.999)
    kv = rng.binomial(tune_n, pv[None, :], size=(reps, len(eff)))
    kr = rng.binomial(tune_n, base_tune, size=(reps, len(eff)))
    obs = (kr - kv) / tune_n
    return float((np.argmax(obs, axis=1) == best).mean())


one_best = [10.0] + [0.0] * (CAND - 1)
graded = [15.0 * i / (CAND - 1) for i in range(CAND)][::-1]
flat = [0.0] * CAND
p_one, p_graded, p_flat = pick_prob(one_best), pick_prob(graded), 1.0 / CAND
F['C'] = {'text': '選定の雑音（層 × 係数の %d 候補・調整走行は腕あたり n=%d〔n=%d × 抽出場面 %d〕・基底は抽出場面の Onull の既測 %.3f）: 低下幅の差の標準誤差 %.1f pt・同値の帯（95%%）は差 ±%.1f pt。真の低下幅が「一つだけ %.0f pt・他は 0」なら最良を選ぶ確率 %.3f、「0〜%.0f pt の等差」なら %.3f、全候補が同じ（帰無）なら %.3f（＝1／候補数）。**選定の低下幅は効果量ではない**（本走行の確証族だけが効果を言う・正本 selection.no_effect_size）。'
          % (CAND, tune_n, nt, len(T['selection']['tune']['scenarios']), base_tune, se_pt, band_pt, one_best[0], p_one, graded[0], p_graded, p_flat),
          'data': {'tune_n_per_arm': tune_n, 'base': round(base_tune, 4), 'se_pt': round(se_pt, 2), 'band_pt': round(band_pt, 2),
                   'pick_one_best': p_one, 'pick_graded': p_graded, 'pick_null': p_flat, 'candidates': CAND}}

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


lo_sc = lambda a: min(SC, key=lambda sc: bs(a, sc))
hi_sc = lambda a: max(SC, key=lambda sc: bs(a, sc))
F['D'] = {'text': 'v 対 v_random の検出力（両側 Fisher・n=%d 対 %d・全数列挙・名目／Holm の初段〔族ごとの m〕・上がる側と下がる側の両方）: '
          '**減算族**（土台 O-Ncold・m=%d）は基底が %s %.3f 〜 %s %.3f。%s の ±15 pt は %s、%s の ±15 pt は %s。'
          '**加算族**（土台 Onull・m=%d）は基底が %s %.3f 〜 %s %.3f。%s の ±15 pt は %s、%s の ±15 pt は %s。'
          '**交差族**（m=%d）は初段の水準が下がる（%s の O-Ncold・±15 pt は %s）。'
          '±10 pt は中間の基底でも初段に届かない（%s の Onull・%s）。床に近い基底では下がる側が率の外に出て測れない（読み条項の余地の条項）。'
          % (n, n, fam['B_sub']['m'], lo_sc('O-Ncold'), bs('O-Ncold', lo_sc('O-Ncold')), hi_sc('O-Ncold'), bs('O-Ncold', hi_sc('O-Ncold')),
             lo_sc('O-Ncold'), two_side('B_sub', 'O-Ncold', lo_sc('O-Ncold'), 15), hi_sc('O-Ncold'), two_side('B_sub', 'O-Ncold', hi_sc('O-Ncold'), 15),
             fam['B_add']['m'], lo_sc('Onull'), bs('Onull', lo_sc('Onull')), hi_sc('Onull'), bs('Onull', hi_sc('Onull')),
             lo_sc('Onull'), two_side('B_add', 'Onull', lo_sc('Onull'), 15), hi_sc('Onull'), two_side('B_add', 'Onull', hi_sc('Onull'), 15),
             fam['B_cross']['m'], 'N1', two_side('B_cross', 'O-Ncold', 'N1', 15), 'S1', two_side('B_add', 'Onull', 'S1', 10)),
          'data': rows}

# ---- E: 品質床（同じ腕の無操作との二標本・18 セル） ----
q, thr = q_items, -T['quality_floor']['threshold_pt'] / 100
cells = T['quality_floor']['cells']


def q_rate(p, drop=0.0, reps=20000):
    a = rng.binomial(q, p, reps)
    b = rng.binomial(q, max(p - drop, 0.01), reps)
    return float((((b - a) / q) <= -thr).mean())


null_q = {p: q_rate(p) for p in (0.5, 0.7, 0.9)}
pow_q = {p: q_rate(p, 0.15) for p in (0.7, 0.9)}
F['E'] = {'text': '品質床（%d 問・%d pt・分子＝正答数・分母＝%d・相手＝同じ腕の無操作・集計単位＝腕 × 層 × 係数＝%d セル）: 帰無発火率（同じ真の正答率で %d pt 以下になる確率）は正答率 0.5 で %.3f・0.7 で %.3f・0.9 で %.3f。真の低下 15 pt を捕まえる確率は 0.7 で %.2f・0.9 で %.2f。帰無で誤って不合格にする期待セル数は、正答率 0.7 で %.2f（%d セル）。課題の出所・版・ライセンス・断片の SHA は凍結時に記帳する（候補は草案5B で諮る）。'
          % (q, T['quality_floor']['threshold_pt'], q, cells, T['quality_floor']['threshold_pt'], null_q[0.5], null_q[0.7], null_q[0.9], pow_q[0.7], pow_q[0.9], cells * null_q[0.7], cells),
          'data': {'null': {str(k): v for k, v in null_q.items()}, 'power_15pt': {str(k): v for k, v in pow_q.items()}, 'cells': cells}}

# ---- F: 費用と時間（バッチの記録値から出し直す・◐） ----
rec = one(r'バッチ 1 なら (\d+) ユニット・8 で (\d+)・16 で (\d+)・24 で (\d+)', ADC)
rec_trials = int(one(r'草案4 の (\d[\d,]*) 試行でバッチ', ADC).group(1).replace(',', ''))
b16, b1 = int(rec.group(3)), int(rec.group(1))
u16, u1 = t_all * b16 / rec_trials, t_all * b1 / rec_trials
F['F'] = {'text': '費用と時間（草案4 の巡の追い問いの記録: %s 試行でバッチ 16 なら %d ユニット・同時 1 本なら %d ユニット。本草案の %s 試行に比例で当てた見込み ◐）: バッチ %d で **≈%.0f ユニット**・同時 1 本なら ≈%.0f ユニット。品質床の %s 問は出力が短く、場面の試行より軽い（比例は上振れの側）。実測は調整走行の最初のセッションで取り、転記行を置き換える。費用の停止規則は段階 A と同じ型（見込みの 1.25 倍で登録者の再裁定）。'
          % (fmt(rec_trials), b16, b1, fmt(t_all), T['runner']['batch'], u16, u1, fmt(t_q)),
          'data': {'trials': t_all, 'units_batch16': round(u16, 1), 'units_batch1': round(u1, 1), 'source_trials': rec_trials, 'source_units': {'1': b1, '16': b16}}}

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
F['I'] = {'text': '活性保存（4B-2507・hidden %d・bf16・凍結 %d 層）: 主位置（プロンプトの最終トークン）は腕 × 場面 × 層ごとに一度だけ保存する——%d 本 × %.1f KB ＝ %.1f MB（試行に依らないため試行ごとに保存しない・草案4 からの変更）。副位置（応答トークン平均）は試行ごとに保存する——%s 試行 × %d 層 ≈ %.2f GiB（Drive）。重み %.2f GiB＋バッチ %d の生成の活性が L4 の 90%% の内側かは、調整走行の最初のセッションで実測する ◐。'
          % (hid, n_layers_saved, prompt_vecs, kb, prompt_vecs * kb / 1024, fmt(t_tune + t_main), n_layers_saved, resp_gib, m4['safetensors_gib'], T['runner']['batch']),
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
