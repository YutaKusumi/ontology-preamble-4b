# -*- coding: utf-8 -*-
"""dry_run_Blens.py v2 —— B-lens の合成データの器（合成の語彙の行列と方向で、器の全ての経路を発火させる・2026-09-23・正本 `synthetic`・§9）。

正本 `synthetic` の形ごとに、合成の入力を作り、器（`blens_core`・`blens_lens.layer1`・`blens_calib`・`build_report_Blens`・`boot_Blens` の関数）を回して、
経路が発火したことと、期待したふるまい（止まるべきところで止まる・札が付くべきところで付く）を確かめる。実データは読まない（組み立ての中と単独の割り方の違いと、
JSON 直答の最初のトークンの経路は、凍結の語の集合の器が実データで確かめる）。Colab の起動器は DRY（乱数の小さな模型）で二つの相を通す（--with-boot）。
v2（2026-09-24・裁定 D187）: ランダム方向の再生の突き合わせ（最後の桁の違いは許容の内で通り、乱数の列・大きさ・方向の数の違いで止まる）と、
  Colab の起動器 DRY が置いた方向の npz の手元の再生との突き合わせと、凍結の器の Colab の確かめの経路を足した。
出力: records/Blens/dry-run-Blens-<日付>.md（--force が無ければ上書きしない）。
用法: python tools/dry_run_Blens.py [--with-boot] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, copy, argparse, datetime, subprocess, tempfile, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'colab'))
import blens_core as C
import blens_lens as BL
import blens_calib as BC
import blens_sets as BS
import build_report_Blens as BR
import boot_Blens as BOOT

VERSION = 'v2'
NL = chr(10)
TL0 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
RESULTS = []


def TLs(**kw):
    T = copy.deepcopy(TL0)
    T['nulls']['word_side']['draws'] = kw.get('draws', 2000)
    return T


def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))
    print('[dry_run_Blens] %s %s %s' % ('OK ' if ok else 'NG ', name, detail), flush=True)


def raises(fn):
    try:
        fn()
    except (SystemExit, BOOT.Stop, AssertionError) as e:
        return str(e)[:120] or type(e).__name__
    return None


def synth(seed=3, d=48, V=400, outlier=False, ragged=False):
    Wm, g, mu, dirs, arm_means, b_rand, rng = BL.synth_bundle(seed=seed, d=d, V=V)
    if outlier:
        Wm[:, 5] *= 40.0
        g = g.copy()
        g[7] = 25.0
        mu = Wm.mean(axis=0).astype(np.float32)
    if ragged:
        Wm = (Wm * np.exp(rng.normal(size=(V, 1)) * 0.8)).astype(np.float32)
        mu = Wm.mean(axis=0).astype(np.float32)
    SJ = BL.synth_sets(rng, V)
    return Wm, g, mu, dirs, arm_means, b_rand, rng, SJ


def run_layer1(T, Wm, g, mu, dirs, arm_means, b_rand, SJ, decode=None):
    V = Wm.shape[0]
    return BL.layer1(T, SJ, lambda ids: [Wm[int(i)] for i in ids], mu, g, dirs, arm_means, b_rand,
                     lambda U: (Wm @ (np.asarray(U, dtype=np.float32) * g[None, :]).T), decode or (lambda i: 'w%d' % i), np.linalg.norm(Wm * g[None, :], axis=1), V)


def gate_rows_synth(rng, units_vals, effect=1.0, noise=0.3, per_unit=None, fams=('nuclear', 'survival'), y_fn=None):
    per_unit = per_unit or {'static': 8, 'loaded': 1, 'Nk': 8, 'td': 8, 'rand:0': 13, 'rand:1': 13, 'rand:2': 13}
    rows = []
    for u, n in per_unit.items():
        for i in range(n):
            f = fams[i % len(fams)]
            s = 1 if i % 3 else -1
            y = y_fn(u, f, s, i) if y_fn else effect * s * units_vals[u][f] + rng.normal() * noise
            rows.append({'scenario': 'S1' if f == 'survival' else 'N1', 'arm': 'X', 'base_arm': 'Y', 'unit': u, 'sign': s, 'fam': f, 'eligible': True,
                         'collapse': False, 'y': float(y), 'k': 1, 'n': 2, 'k0': 1, 'n0': 2})
    return rows


def free_perm_p(rows, uv, n=2000, seed=0):
    """行を自由に並べ替えたときの順位相関の割合（比べるための記述・門には使わない）。"""
    rng = np.random.default_rng(seed)
    x = np.array([r['sign'] * uv[r['unit']][r['fam']] for r in rows])
    y = np.array([r['y'] for r in rows])
    obs = C.spearman(x, y)
    ge = sum(1 for _ in range(n) if C.spearman(x, rng.permutation(y)) >= obs - 1e-12)
    return (1 + ge) / (1 + n), obs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--with-boot', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    out = os.path.join(REPO, 'records', 'Blens', 'dry-run-Blens-%s.md' % datetime.date.today().isoformat())
    if os.path.exists(out) and not a.force:
        raise SystemExit('既にある: %s' % out)
    T = TLs()
    # ---- 層一の経路
    Wm, g, mu, dirs, arm_means, b_rand, rng, SJ = synth()
    frag_ids = set(range(0, 400, 17))
    dec = lambda i: ('�' if i in frag_ids else ('ab' if i % 23 == 0 else ('・' if i % 29 == 0 else 'w%d' % i)))
    # 集合の重なり: E+ の語を X にも入れ、方向で強く押す
    ov = SJ['sets']['E']['static']['plus'][0]
    SJ['sets']['X']['survival']['a'] = sorted(set(SJ['sets']['X']['survival']['a']) | {ov})
    # 断片を方向で強く押す
    for r in dirs['static']:
        u = dirs['static'][r].astype(np.float64)
        for t in list(frag_ids)[:3] + [ov]:
            Wm[t] = (Wm[t] + 4.0 * u / np.linalg.norm(u) / (g + 1e-9)).astype(np.float32)
    mu = Wm.mean(axis=0).astype(np.float32)
    res = run_layer1(T, Wm, g, mu, dirs, arm_means, b_rand, SJ, dec)
    kinds = collections.Counter()
    for v in res['lists'].values():
        kinds.update(v['top_kinds'])
        kinds.update(v['bottom_kinds'])
    check('断片のトークン（語の一覧の数える記述に断片の種類が出る）', kinds.get('fragment', 0) > 0, 'fragment %d・ascii %d・symbol %d' % (kinds.get('fragment', 0), kinds.get('ascii', 0), kinds.get('symbol', 0)))
    marks_ov = [x['marks'] for v in res['lists'].values() for side in ('top', 'bottom') for x in v[side] if x['id'] == ov]
    check('集合の重なり（一つのトークンに二つの集合の印）', any(('E_static_plus' in m and 'X_survival_a' in m) for m in marks_ov), str(marks_ov[:1]))
    # 家族で M_L が割れる: d の文字の行を大きくする
    Wd = Wm.copy()
    Wd[SJ['sets']['L']['d']] += (5.0 * dirs['static']['0.5'] / np.linalg.norm(dirs['static']['0.5']) / (g + 1e-9)).astype(np.float32)
    r2 = run_layer1(T, Wd, g, Wd.mean(axis=0).astype(np.float32), dirs, arm_means, b_rand, SJ)
    v = r2['layers']['0.5']['directions']['static']
    check('家族で M_L が割れる（N1 は d の項の分だけ違う）', abs(v['M_L_survival']['value'] - v['M_L_nuclear']['value']) > 1e-3, 'survival %.4g・nuclear %.4g' % (v['M_L_survival']['value'], v['M_L_nuclear']['value']))
    # 外れ値の次元と g の外れ値
    Wo, go, muo, dirs_o, am_o, br_o, rng_o, SJo = synth(seed=4, outlier=True)
    ro = run_layer1(T, Wo, go, muo, dirs_o, am_o, br_o, SJo)
    topd = ro['descriptive_after_seal']['static@0.5']['top_dims']
    check('外れ値の次元と g の外れ値（等方の解析の確かめを通り、上位の次元に外れ値が入る）', 7 in topd or 5 in topd, '上位の次元 %s' % topd[:4])
    # 行のノルムが不揃いな共有の語彙の行列
    Wr, gr, mur, dirs_r, am_r, br_r, rng_r, SJr = synth(seed=5, ragged=True)
    rr = run_layer1(T, Wr, gr, mur, dirs_r, am_r, br_r, SJr)
    check('行のノルムが不揃いな語彙の行列（一覧の語のノルムの偏りを印字する）', 'list_norm_pct' in rr['descriptive_after_seal']['static@0.5'], str(rr['descriptive_after_seal']['static@0.5']['list_norm_pct']))
    # 一つだけの F の主と空の E−
    tab = C.metric_table(dict(SJ['sets'], F={'main': SJ['sets']['F']['main'], 'sens': []}), ['survival', 'nuclear'], T['metrics']['letters'])
    check('一つだけの F の主と空の E−（M_F の感度を作らず、td と Nk の M_E は片側）', 'M_F_sens' not in tab and tab['M_E_td'][2] and tab['M_E_Nk'][2] and not tab['M_E_static'][2])
    # 同じ |値| を持つ両向き
    check('同じ |値| を持つ両向き（同じ値は上回らない・最上位にしない）', not C.top_rank(2.0, [-2.0, 1.0])['top'] and C.top_rank(2.0, [-1.9, 1.0])['top'])
    # ほぼ同じ向きの双子の方向
    dirs_t = copy.deepcopy(dirs)
    for r in dirs_t['Nk']:
        dirs_t['Nk'][r] = (dirs_t['td'][r] + 1e-4 * np.linalg.norm(dirs_t['td'][r]) * rng.normal(size=dirs_t['td'][r].shape)).astype(np.float32)
    rt = run_layer1(T, Wm, g, mu, dirs_t, arm_means, b_rand, SJ)
    a_, b_ = rt['layers']['0.5']['directions']['td']['M_L_survival']['value'], rt['layers']['0.5']['directions']['Nk']['M_L_survival']['value']
    check('ほぼ同じ向きの双子の方向（値がほぼ同じで、器が止まらない）', abs(a_ - b_) < 1e-2 * max(1.0, abs(a_)), '%.5g と %.5g' % (a_, b_))
    # 中心が零でない語の側の帰無
    null = np.full(2000, 2.0) + np.random.default_rng(1).normal(size=2000) * 0.05
    p_eq, p_abs = C.p_equal_tailed(2.02, null), C.p_two_sided(2.02, null - 2.0 * 0)
    check('中心が零でない語の側の帰無（両側に等しい裾の割合を使い、|値| で比べない）', p_eq > 0.05, '両側に等しい裾 %.3g' % p_eq)
    # 一字の漢字を一様に押す方向（層で揃えた帰無の中に埋もれる）
    V = 400
    cells = {}
    rngk = np.random.default_rng(7)
    pool = list(range(100, 400))
    for i in pool:
        cells[i] = ('K', '一字' if i % 2 else '二字以上', int(i % 5))
    plus = [i for i in range(10, 20)]
    minus = [i for i in range(20, 26)]
    for i in plus:
        cells[i] = ('K', '一字', int(i % 5))
    for i in minus:
        cells[i] = ('K', '二字以上', int(i % 5))
    delta = np.array([(1.0 if (cells.get(i, ('', '', 0))[1] == '一字') else 0.0) + rngk.normal() * 0.1 for i in range(V)])
    cc = collections.Counter(cells[i] for i in pool)
    nc = collections.Counter(cells[i] for i in plus + minus)
    grp, ok = C.strata_groups(cc, nc, 5, 5)
    nd = C.word_side_draws(delta, plus, minus, lambda t: cells[t], pool, grp, 2000, 81003)
    mE = delta[plus].mean() - delta[minus].mean()
    check('一字の漢字を一様に押す方向（字の種類と字数で揃えた帰無の中に埋もれる）', C.p_equal_tailed(mE, nd) > 0.05 and mE > 0.5, 'M_E %.3g・割合 %.3g' % (mE, C.p_equal_tailed(mE, nd)))
    # ---- 門の経路
    units = list(T['calibration']['directions'])
    uv = {u: {f: float(rng.normal()) for f in ('nuclear', 'survival')} for u in units}
    rows = gate_rows_synth(rng, uv)
    g1 = BC.gate_part(T, rows, lambda u, m: uv[u][m.split('_')[-1]] if m.startswith(('M_L_', 'M_X_')) else 0.0)
    check('門を通る場合', g1['gate_passed'], 'M_L p %.4g' % g1['gates']['full']['M_L']['p'])
    rows0 = gate_rows_synth(np.random.default_rng(11), uv, y_fn=lambda u, f, s, i: -s * uv[u][f])      # 押しと逆向きの行動（片側の門は通らない）
    g0 = BC.gate_part(T, rows0, lambda u, m: uv[u][m.split('_')[-1]] if m.startswith(('M_L_', 'M_X_')) else 0.0)
    check('門を通らない場合', not g0['gate_passed'], 'M_L p %.4g・M_X p %.4g' % (g0['gates']['full']['M_L']['p'], g0['gates']['full']['M_X']['p']))
    # 一本の方向が門を引っ張る: rand:0 だけが大きな値と大きな行動を持つ
    uv1 = {u: {f: (8.0 if u == 'rand:0' else float(rng.normal()) * 0.2) for f in ('nuclear', 'survival')} for u in units}
    rows1 = gate_rows_synth(rng, uv1, y_fn=lambda u, f, s, i: (6.0 * s if u == 'rand:0' else float(np.random.default_rng(i + 100 * len(u)).normal())))
    pf, obs = free_perm_p(rows1, uv1)
    gp = C.gate_perm(rows1, uv1, units)
    check('一本の方向が門を引っ張る（行を自由に並べ替えると割合が小さく、方向を単位にすると通らない）', pf < 0.05 and gp['p'] >= T['calibration']['alpha'] / T['calibration']['holm_m'],
          '自由 %.4g・方向の単位 %.4g' % (pf, gp['p']))
    # 方向ごとの効きを持つ帰無: 行動は方向ごとの乱れだけ（物差しと無関係）
    fp_free = fp_unit = 0
    nsim = 30
    for k in range(nsim):
        rs = np.random.default_rng(1000 + k)
        uvs = {u: {f: float(rs.normal()) for f in ('nuclear', 'survival')} for u in units}
        eff = {u: float(rs.normal()) * 1.0 for u in units}
        rws = gate_rows_synth(rs, uvs, y_fn=lambda u, f, s, i: eff[u] * s + float(np.random.default_rng(10000 * k + i + 31 * len(u)).normal()) * 0.3)
        fp_free += free_perm_p(rws, uvs, n=400, seed=k)[0] < 0.05
        fp_unit += C.gate_perm(rws, uvs, units)['p'] < 0.05
    check('方向ごとの効きを持つ帰無（自由な並べ替えと方向の単位の偽の通過率を並べる）', fp_free >= fp_unit, '自由 %d／%d・方向の単位 %d／%d' % (fp_free, nsim, fp_unit, nsim))
    # 二つの門が別の物差しで通る: 本の門は M_L だけ、v̂ を抜いた門は M_X だけ
    uv2 = {u: {'nuclear': float(rng.normal()), 'survival': float(rng.normal())} for u in units}
    uvx = {u: {'nuclear': float(rng.normal()), 'survival': float(rng.normal())} for u in units}

    def y2(u, f, s, i):
        return (5.0 * s * uv2[u][f]) if u == 'static' else (5.0 * s * uvx[u][f]) + float(np.random.default_rng(i + 7 * len(u)).normal()) * 0.01
    rows2 = gate_rows_synth(rng, uv2, y_fn=y2)
    vals2 = lambda u, m: (uv2 if m.startswith('M_L_') else uvx)[u][m.split('_')[-1]] if m.startswith(('M_L_', 'M_X_')) else 0.0
    cross = {'full': {'M_L': {'pass': True}, 'M_X': {'pass': False}}, 'without_vhat': {'M_L': {'pass': False}, 'M_X': {'pass': True}}}
    same = {'full': {'M_L': {'pass': False}, 'M_X': {'pass': True}}, 'without_vhat': {'M_L': {'pass': True}, 'M_X': {'pass': True}}}
    check('二つの門が別の物差しで通る（同じ物差しが両方を通らなければ v̂ の値を行動に結びつけない）',
          BC.link_metrics(cross, T['calibration']['tests']) == [] and BC.link_metrics(same, T['calibration']['tests']) == ['M_X'])
    # 零と全部の行（床と天井の土台の行は外す）
    BD = [{'scenario': 'S1', 'arm': 'O', 'direction_id': 'fixed', 'n_ok': 10, 'cat': 0}, {'scenario': 'S1', 'arm': 'O-v', 'direction_id': 'static', 'n_ok': 10, 'cat': 1},
          {'scenario': 'S1', 'arm': 'Onull', 'direction_id': 'fixed', 'n_ok': 10, 'cat': 10}, {'scenario': 'S1', 'arm': 'Onull+v', 'direction_id': 'static', 'n_ok': 10, 'cat': 9},
          {'scenario': 'S1', 'arm': 'O-Ncold', 'direction_id': 'fixed', 'n_ok': 10, 'cat': 4}, {'scenario': 'S1', 'arm': 'O-Ncold-v', 'direction_id': 'static', 'n_ok': 10, 'cat': 2}]
    cnt = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in BD:
        c = cnt[(r['scenario'], r['arm'])][r['direction_id']]
        c['_n'], c['a'], c['b'] = r['n_ok'], r['cat'], r['n_ok'] - r['cat']
    gr = BC.gate_rows(T, BD, cnt)
    check('零と全部の行（床と天井の土台の行は門に入れない）', [x['eligible'] for x in gr] == [False, False, True], str([(x['arm'], x['eligible']) for x in gr]))
    # ---- 大きさの目盛りの経路
    d, V = 32, 300
    rs = np.random.default_rng(21)
    Wv = (rs.normal(size=(V, d)) * 0.3).astype(np.float32)          # 出口の値の広がりを抑える（切り詰めの内に十数語が残る文脈）
    gv = rs.uniform(0.5, 1.5, size=d).astype(np.float32)
    Zfull = lambda H: (Wv @ (np.asarray(H, dtype=np.float32) * gv[None, :]).T)
    letters = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'refuse': 14}
    T3 = copy.deepcopy(T)
    T3['inputs']['sampling_B'] = {'temperature': 0.7, 'top_k': 20, 'top_p': 0.9, 'repetition_penalty': 1.0, 'min_p': 0.0}
    hA = rs.normal(size=d).astype(np.float32) * 3
    hB = rs.normal(size=d).astype(np.float32) * 3
    ctx = [{'scenario': 'S4', 'arm': 'Osec-Ncold'}] * 3 + [{'scenario': 'S4', 'arm': 'O-Ncold'}] * 3
    Hm = np.array([hA] * 3 + [hB] * 3)
    Hl = np.array([hA + 0.1] * 3 + [hB + rs.normal(size=d).astype(np.float32) * 0.3 for _ in range(3)])
    u1 = rs.normal(size=d)
    # 切り詰めの境: 土台の文脈で順位が二十五番目の語を「```」の役にし、(6b) の方向がそれを強く押す（切り詰めの外から内へ入る）
    z0 = (Wv @ (hA.astype(np.float64) * gv)) / C.rms(hA, 1e-6)
    fmain = int(np.argsort(-z0)[24])
    u1 = (Wv[fmain].astype(np.float64) * gv)
    u1 = u1 / np.linalg.norm(u1)
    dirs_sel = collections.OrderedDict([('loaded', u1 * 4.0), ('rand:0', rs.normal(size=d) * 4.0), ('rand:1', rs.normal(size=d) * 4.0), ('static', rs.normal(size=d) * 4.0)])
    counts = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for key, n, k in ((('S4', 'Osec-Ncold'), 200, 150), (('S4', 'O-Ncold'), 200, 0)):
        counts[key]['fixed'].update({'_n': n, '_style': k})
    counts[('S4', 'Osec-Ncold+v6b')]['loaded'].update({'_n': 200, '_style': 200})
    counts[('S4', 'Osec-Ncold+vrand')]['rand:0'].update({'_n': 67, '_style': 67})
    counts[('S4', 'Osec-Ncold+vrand')]['rand:1'].update({'_n': 67, '_style': 51})
    counts[('S4', 'O-Ncold+vrand')]['rand:0'].update({'_n': 67, '_style': 30})
    counts[('S4', 'O-Ncold-v')]['static'].update({'_n': 200, '_style': 0})
    mrows = [{'scenario': 'S4', 'arm': 'Osec-Ncold+v6b', 'base_arm': 'Osec-Ncold', 'unit': 'loaded', 'sign': 1},
             {'scenario': 'S4', 'arm': 'Osec-Ncold+vrand', 'base_arm': 'Osec-Ncold', 'unit': 'rand:0', 'sign': 1},
             {'scenario': 'S4', 'arm': 'Osec-Ncold+vrand', 'base_arm': 'Osec-Ncold', 'unit': 'rand:1', 'sign': 1},
             {'scenario': 'S4', 'arm': 'O-Ncold+vrand', 'base_arm': 'O-Ncold', 'unit': 'rand:0', 'sign': 1},
             {'scenario': 'S4', 'arm': 'O-Ncold-v', 'base_arm': 'O-Ncold', 'unit': 'static', 'sign': -1}]
    vals = lambda u, m: 0.1 * len(u)
    first = (Zfull(Hm[:1])[:, 0] / C.rms(Hm[0], 1e-6), Zfull(Hl[:1])[:, 0] / C.rms(Hl[0], 1e-6))
    mg = BC.magnitude_part(T3, mrows, counts, ctx, Hm, Hl, Zfull, gv, dirs_sel, fmain, letters, vals, 1e-6, first)
    byrow = {x['row']: x for x in mg['main_rows']}
    check('行動の変化が零の行（v̂ の行・比を出さない）', not byrow['S4|O-Ncold-v|static']['eligible'] and 'ratio' not in byrow['S4|O-Ncold-v|static'], 'z %.3g' % byrow['S4|O-Ncold-v|static']['z'])
    check('JSON 直答が零の升目（土台の率が零の行に印）', byrow['S4|O-Ncold+vrand|rand:0'].get('rate_edge') is True, str({k: byrow['S4|O-Ncold+vrand|rand:0'].get(k) for k in ('rate_edge', 'logodds_undefined', 'reading')}))
    check('土台の率が零か一の行の比（印を付けて比を出す）', all('ratio' in byrow[k] for k in ('S4|Osec-Ncold+v6b|loaded', 'S4|O-Ncold+vrand|rand:0')) and byrow['S4|Osec-Ncold+v6b|loaded']['rate_edge'])
    check('JSON 直答の割合が腕で変わる升目（下限を超えた行だけ比を出す）', mg['summary']['ratio_rows'] == 3 and 'ratio' not in byrow['S4|Osec-Ncold+vrand|rand:1'],
          '比を出した行 %d・変化の小さい行の z %.3g' % (mg['summary']['ratio_rows'], byrow['S4|Osec-Ncold+vrand|rand:1']['z']))
    xl = byrow['S4|Osec-Ncold+v6b|loaded']
    check('温度と切り詰めのある復号（切り詰めの外の語が押しで内へ入る・対数オッズは定まらないので出さず印を付ける）',
          xl['pT_before'] == 0.0 and xl['pT_after'] > 0.0 and xl.get('logodds_undefined') is True, '前 %.3g・後 %.3g' % (xl['pT_before'], xl['pT_after']))
    lj = mg['letter']['S4|Osec-Ncold']['rows']['S4|Osec-Ncold+v6b|loaded']
    check('頭の並びがそろった JSON 直答（同じ文脈なら四分位の幅は零）', abs(lj['dpT_c']['q3'] - lj['dpT_c']['q1']) < 1e-12)
    # 正規化の後の値を取ったフック: 残差の代わりに正規化の後の値を渡すと、手元の logits の突き合わせで止まる
    Hpost = np.array([h / np.sqrt(np.mean(h.astype(np.float64) ** 2) + 1e-6) * gv for h in Hm]).astype(np.float32)
    msg = raises(lambda: BC.magnitude_part(T3, mrows, counts, ctx, Hpost, Hl, Zfull, gv, dirs_sel, fmain, letters, vals, 1e-6, first))
    check('正規化の後の値を取ったフック（logits の突き合わせで止まる）', msg is not None and 'logits' in msg, msg or '')
    # 選択を読めない出力を含む升目（起動器の関数が止まる）
    class Tk:
        def __call__(self, s, add_special_tokens=False, return_offsets_mapping=False):
            ids = list(range(len(s)))
            return {'input_ids': ids, 'offset_mapping': [(i, i + 1) for i in range(len(s))]}
    tr = {'trial_id': 't0', 'trial_index': 0, 'choice': 'c', 'preamble_sha': 'X'}
    m1 = raises(lambda: BOOT.context_of(Tk(), [1, 2, 3], tr, {'final': '選択は c です'}, 'X', lambda p: len(p) - 1))
    ok1 = BOOT.context_of(Tk(), [1, 2, 3], tr, {'final': '```json\n{"choice": "c"}'}, 'X', lambda p: len(p) - 1)
    m2 = raises(lambda: BOOT.context_of(Tk(), [1, 2, 3], tr, {'final': '{"choice": "c"}'}, 'Y', lambda p: len(p) - 1))
    check('選択を読めない出力を含む升目（起動器が止まる）・前置きの SHA の違いで止まる', m1 is not None and m2 is not None and ok1['letter_pos'] > ok1['main_pos'], '%s／%s' % (m1, m2))
    # 「```」以外で始まる JSON 直答（凍結の語の集合の器が止まる）
    m3 = raises(lambda: BS.pick_f_main(collections.Counter({1: 5, 2: 3}), {1: 0, 2: 1}, lambda i: {1: '{', 2: '```'}[i]))
    check('「```」以外で始まる JSON 直答（語の集合の器が止まる）', m3 is not None, m3 or '')
    # 較正の検査が区間の外で止まる（起動器の関数）
    cal, off = BOOT.calibration_items(['S4|Osec-Ncold|json'], [{'stratum': 'S4|Osec-Ncold|json', 'pT_main_fmain': 0.2, 'pT_letter': {'a': 0.0, 'b': 0.0, 'c': 1.0}}],
                                      {'S4|Osec-Ncold|json': {'n': 200, 'style': 154, 'json_n': 154, 'json_letters': {'a': 0, 'b': 0, 'c': 154}}}, 0.999, C.binom_central)
    check('較正の検査（区間の外を拾う）', off == ['S4|Osec-Ncold|json 主位置'], str(off))
    # ---- 報告の経路（読みの型・走査）
    units_vals = {u: {f: float(rng.normal()) for f in ('nuclear', 'survival')} for u in units}
    res_l = json.loads(json.dumps(res))
    calib = BC.gate_part(T, gate_rows_synth(rng, units_vals), lambda u, m: res_l['layers']['0.5']['directions'][u][m]['value'])
    calib['s4_control'] = BC.s4_control(lambda u, m: res_l['layers']['0.5']['directions'][u][m]['value'])
    calib['tune'] = []
    calib['magnitude'] = json.loads(json.dumps(mg))
    calib = json.loads(json.dumps(calib))
    preds = {'registrant': {}, 'coordinator': {}}
    text = BR.build(T, res_l, calib, SJ, None, preds, {k: '0123456789ABCDEF' for k in ('canon', 'sets', 'seal', 'lens', 'calib')})
    V_, _ = BR.lint_report(text, T)
    hit, neg = BR.reading_types(T, res_l, calib)
    check('報告の組み立てと走査（違反 0）・読みの型を当てる', V_ == [] and len(hit) >= 1, '型 %s' % sorted(set(t for t, m, w in hit)))
    # 型ごとに条件を強制して、全ての型が当たることを確かめる
    types_seen = set(t for t, m, w in hit)
    for iso, sec in ((True, True), (True, False), (False, True), (False, False)):
        rl = copy.deepcopy(res_l)
        for m in rl['primary']['metrics']:
            rl['primary']['metrics'][m]['iso_outside'], rl['primary']['metrics'][m]['second'] = iso, sec
        for gp_ in (True, False):
            cl = copy.deepcopy(calib)
            cl['gate_passed'], cl['passed_metrics'] = gp_, (['M_L'] if gp_ else [])
            types_seen |= set(t for t, m, w in BR.reading_types(T, rl, cl)[0])
    want = set(r['type'] for r in T['reading_rules'])
    check('読みの表の全ての型が器で当たる', types_seen == want, '当たらなかった型 %s' % sorted(want - types_seen))
    # ---- ランダム方向の再生の突き合わせ（裁定 D187・正本 `nulls.B_random.repro_check`）
    tol = T['nulls']['B_random']['repro_tol']
    loc = {'main@0.5': np.array(b_rand['main']['0.5'])}
    loc.update({'tune@%s' % r: np.array(v) for r, v in b_rand['tune'].items()})
    eps32 = float(np.finfo(np.float32).eps)
    c_last = BL.compare_random_dirs(loc, {k: v * (1.0 + eps32) for k, v in loc.items()}, tol)
    check('ランダム方向の再生の最後の桁の違い（許容の内で通り、SHA-256 は違う）',
          c_last['ok'] and not any(r['bitwise_equal'] for r in c_last['keys'].values()) and all(r['sha256_local'] != r['sha256_colab'] for r in c_last['keys'].values()),
          '相対の差の最大 %.3g・許容 %g' % (c_last['rel_max'], tol))
    c_seed = BL.compare_random_dirs(loc, dict(loc, **{'main@0.5': np.array(C.iso_directions(dirs['static']['0.5'], 71003, 0.5, 3, 1000))}), tol)
    c_scale = BL.compare_random_dirs(loc, dict(loc, **{'tune@0.75': loc['tune@0.75'] * (1 + 10 * tol)}), tol)
    c_shape = BL.compare_random_dirs(loc, dict(loc, **{'tune@0.25': loc['tune@0.25'][:2]}), tol)
    check('ランダム方向の再生の乱数の列の違い・許容の十倍の大きさの違い・方向の数の違い（どれも止まる）', not (c_seed['ok'] or c_scale['ok'] or c_shape['ok']),
          '乱数の列 %.3g・大きさ %.3g・方向の数 %s' % (c_seed['keys']['main@0.5']['rel_max'], c_scale['keys']['tune@0.75']['rel_max'], c_shape['problems'][:1]))
    # ---- Colab の起動器（DRY・乱数の小さな模型）
    if a.with_boot:
        with tempfile.TemporaryDirectory() as td:
            for phase in ('check', 'extract'):
                env = dict(os.environ, OP4B_DRY='1', OP4B_PHASE=phase, OP4B_DRY_N='2', OP4B_REPO_DIR=REPO, OP4B_OUT=td, PYTHONIOENCODING='utf-8')
                p = subprocess.run([sys.executable, os.path.join(HERE, 'colab', 'boot_Blens.py')], env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
                done = [l for l in p.stdout.splitlines() if ' done ' in l]
                check('Colab の起動器 DRY（相 %s）' % phase, p.returncode == 0 and bool(done), (done[-1][:120] if done else p.stderr[-200:]))
                if phase == 'check' and p.returncode == 0:
                    import steer_B
                    import freeze_Blens as FZ
                    od_ = sorted(x for x in os.listdir(td) if x.startswith('check-') and os.path.isdir(os.path.join(td, x)))[-1]
                    cj = os.path.join(td, od_, 'check.json')
                    CKd = json.load(open(cj, encoding='utf-8'))
                    Dd = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
                    sel_ = BL.rkey(T['primary']['ratio'])
                    vecs = {'main@%s' % sel_: np.array(steer_B.random_directions(Dd['static__%s' % sel_], 'main', float(sel_)))}
                    for r in [BL.rkey(x) for x in T['layers']['ratios']]:
                        vecs['tune@%s' % r] = np.array(steer_B.random_directions(Dd['static__%s' % r], 'tune', float(r)))
                    cd = BL.compare_random_dirs(vecs, BL.load_colab_dirs(os.path.join(td, od_, CKd['random_dirs_npz']['file']), CKd), tol)
                    check('Colab の起動器 DRY が置いた方向の npz を手元の再生と突き合わせる（同じ機械ではビットで一致）', cd['ok'] and all(r['bitwise_equal'] for r in cd['keys'].values()),
                          '相対の差の最大 %s・鍵 %s' % (cd['rel_max'], sorted(cd['keys'])))
                    fres, fbad = FZ.checks(cj)
                    cc = fres['colab_check']
                    check('凍結の器の Colab の確かめの経路（DRY の出力は DRY と版で外れ、方向は許容の内で合う）', cc['random_dirs'] and not cc['not_dry'] and not cc['versions'],
                          str({k: v for k, v in cc.items() if isinstance(v, bool)}))
    # ---- 書き出し
    ng = [r for r in RESULTS if not r[1]]
    L = ['# B-lens の合成データの確かめ（機械生成・`tools/dry_run_Blens.py` %s・%s）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')), '',
         '- 正本 `design/contrasts-Blens.json` の `synthetic` の形ごとに、合成の入力で器の経路を発火させた。実データは読まない。',
         '- 実データで発火を確かめた経路: 組み立てた中と単独で割り方が違う場合（`records/Blens/sets-Blens.md`・nuclear の X の二語）・単独で割った集合と下書きの器の集合のバイトの一致。',
         '- 結果: %d 経路・外れ %d。' % (len(RESULTS), len(ng)), '', '| 経路 | 結果 | 中身 |', '|---|---|---|']
    L += ['| %s | %s | %s |' % (n, '発火・期待どおり' if ok else '**外れ**', d_.replace('|', '｜')) for n, ok, d_ in RESULTS]
    L += ['', '## 検分票', '', '- 対象: 凍結の前の器の全ての経路（合成データ）。', '- 段階: 凍結の前（射影は一つも計算していない）。',
          '- 本検分が確認していないこと: 実重みでの層一の計算（封印の後）・Colab の実機の相 check（別に走らせる）・合成の形が実データの難しさを代表するか。'
          'torch を B の組みに入れ直す起動器の経路（DRY は版を見ないので通らない・Colab の実機で確かめる）。', '',
          '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('[dry_run_Blens] wrote %s（%d 経路・外れ %d）' % (os.path.relpath(out, REPO), len(RESULTS), len(ng)))
    if ng:
        raise SystemExit('外れた経路がある')


if __name__ == '__main__':
    main()
