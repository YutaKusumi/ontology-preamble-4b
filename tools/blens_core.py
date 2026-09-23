# -*- coding: utf-8 -*-
"""blens_core.py v1 —— B-lens の計算の芯（numpy だけ・重みも試行も読まない・2026-09-23）。

正本 `design/contrasts-Blens.json` の規則を、重みや試行を読まない純粋な関数に置く。層一の器 `tools/blens_lens.py`・
層二の器 `tools/blens_calib.py`・合成データの器 `tools/dry_run_Blens.py` が同じ関数を呼ぶ（同じ式を二度書かない）。
語の集合の規則（字の決まり・断片・中身の語）は、ここに置かない（語の集合の器 `tools/blens_sets.py` が、下書きの器 `tools/blens_facts.py` と
独立に書き、バイトで突き合わせる——正本 `token_sets.freeze`）。

置くもの:
  - 物差しの係数のベクトル: 物差しは方向 u について線形なので、M(u) = a·u の a を一度だけ作る（a = g ⊙ (Σ w_t W[t] − (Σ w_t) μ_W)・μ_W は含める語彙の行の平均）。
    差の形の物差しは Σ w_t = 0 で中心化が消え、片側の物差しは語彙の平均を引く（正本 `projection.centring_note`）。
  - 等方の帰無の方向の引き方（`steer_B.random_directions` と同じ作り方・自己検査でビットの一致を確かめる）と、解析の標準偏差（‖a‖·‖v̂‖／√d）。
  - 割合: 零を中心に対称な帰無の両側の割合（`percentile.rule`）と、語の側の帰無の両側に等しい裾の割合（`nulls.word_side.p_rule`）。
  - Holm: 段階 B の集計器と同じく、p が段を**下回る**（p < 段）ときに通し、通らなかった所で止める（正本「p が段を下回る」）。
  - 門: 行の単位の順位相関（Spearman・同順位は平均順位）と、方向を単位にした並べ替え（全ての入れ替え・片側・p = #{ρ_入れ替え ≥ ρ_観測}／入れ替えの数・恒等を含む）。
  - 語の側の帰無: 層の組み立て（字の種類 × 字数 × ノルムの帯・薄い層は帯の真ん中の側の隣と合わせる・真ん中なら下の側）と、抽選。
  - 大きさの目盛り: B の標本化の変換（温度 → top_k → top_p・transformers 4.57 の順と式）・二項分布の中央の区間・正確な直接の経路とその分け方。
用法: python tools/blens_core.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import sys, math, itertools, collections
import numpy as np

VERSION = 'v1'
EPS_TIE = 1e-12          # 並べ替えの順位相関の同値の幅（恒等と同じ値の入れ替えを「以上」に数える・保守の側）


# ---------------- 物差しの係数 ----------------
def metric_table(sets, families, letters):
    """物差しの名 → (トークン, 重み, 片側か)。sets は凍結の語の集合（`blens_sets` の出力の `sets`）。

    名: M_L_<家族>・M_Lc（survival だけ）・M_R_<家族>・M_X_<家族>・M_E_<方向の種類>・M_F・M_F_sens と、感度の変種（名の後ろに :<変種>）。"""
    L, R = sets['L'], sets['R']
    out = collections.OrderedDict()
    mean_w = lambda toks, sgn=1.0: [(t, sgn / len(toks)) for t in toks]

    def put(name, pos, neg, one_sided=False):
        acc = collections.OrderedDict()
        for t, w in pos + neg:
            acc[t] = acc.get(t, 0.0) + w
        out[name] = (list(acc.keys()), list(acc.values()), one_sided)

    for fam in families:
        lt = letters[fam]
        others = [L[x] for x in lt if x != 'a']
        put('M_L_%s' % fam, [(L['a'], 1.0)], mean_w(others, -1.0))
        put('M_R_%s' % fam, [(R, 1.0)], mean_w([L[x] for x in lt], -1.0))
        X = sets['X'][fam]
        for var, (a_, o_) in (('', (X['a'], X['others'])), (':unmarked', (X['a_unmarked'], X['others_unmarked'])),
                              (':kata1', (X['a_kata1'], X['others_kata1'])), (':all', (X['a_all'], X['others_all'])),
                              (':multi', (X['a_multi'], X['others_multi']))):
            if a_ and o_:
                put('M_X_%s%s' % (fam, var), mean_w(a_), mean_w(o_, -1.0))
    if 'survival' in families:
        put('M_Lc', [(L['c'], 1.0)], mean_w([L['a'], L['b']], -1.0))
    for kind in ('static', 'td', 'Nk'):
        E = sets['E'][kind]
        for var, (p_, m_) in (('', (E['plus'], E['minus'])), (':kata1', (E['plus_kata1'], E['minus_kata1'])),
                              (':all', (E['plus_all'], E['minus_all'])), (':multi', (E['plus_multi'], E['minus_multi']))):
            if not p_:
                continue
            if m_:
                put('M_E_%s%s' % (kind, var), mean_w(p_), mean_w(m_, -1.0))
            else:
                put('M_E_%s%s' % (kind, var), mean_w(p_), [], one_sided=True)
    F = sets['F']
    put('M_F', [(F['main'], 1.0)], [], one_sided=True)
    if F['sens']:
        put('M_F_sens', [(F['main'], 1.0)], mean_w(F['sens'], -1.0))
    return out


def coef_vectors(table, rows_of, mu_W, g):
    """物差しの係数のベクトル a（d 次元・float32）。rows_of(トークンの並び) は語彙の行（float32・行×d）を返す関数。"""
    need = sorted(set(t for toks, w, o in table.values() for t in toks))
    Wn = dict(zip(need, rows_of(need)))
    out = collections.OrderedDict()
    for name, (toks, w, one) in table.items():
        s = np.zeros_like(mu_W)
        for t, wt in zip(toks, w):
            s = s + np.float32(wt) * Wn[t]
        s = s - np.float32(sum(w)) * mu_W
        out[name] = (g * s).astype(np.float32)
    return out


def values(A, U):
    """物差しの値: A は物差しの名 → a、U は方向（本数×d）。戻り値: 名 → 値の並び（float64）。"""
    U = np.atleast_2d(np.asarray(U, dtype=np.float32))
    return collections.OrderedDict((k, (U @ a).astype(np.float64)) for k, a in A.items())


def analytic_sd(a, target_norm, d):
    """ノルム target_norm の等方の方向での a·u の標準偏差（‖a‖·‖v̂‖／√d）。"""
    return float(np.linalg.norm(a.astype(np.float64)) * target_norm / math.sqrt(d))


# ---------------- 方向 ----------------
def iso_directions(v_hat_static, seed, layer_ratio, count, key_scale):
    """`steer_B.random_directions` と同じ作り方（種と本数だけを変える・凍結の関数は種を正本から取るので写した）。"""
    d = int(np.asarray(v_hat_static).shape[-1])
    ss = np.random.SeedSequence([seed, int(round(layer_ratio * key_scale))])
    rng = np.random.default_rng(ss)
    target = float(np.linalg.norm(v_hat_static))
    out = []
    for i in range(count):
        g = rng.normal(size=d)
        n = float(np.linalg.norm(g))
        out.append(g * (target / n) if n else g)
    return np.array(out)


def match_norm(v, target):
    n = float(np.linalg.norm(v))
    return v * (float(target) / n) if n else v


def real_differences(arm_means, target_norm):
    """八腕の平均の活性の全ての対（名の並びの順・i<j）: 名 'A~B' → (A − B) を target_norm に合わせたもの。"""
    names = list(arm_means)
    out = collections.OrderedDict()
    for i, j in itertools.combinations(range(len(names)), 2):
        out['%s~%s' % (names[i], names[j])] = match_norm(arm_means[names[i]] - arm_means[names[j]], target_norm)
    return out


# ---------------- 割合と札 ----------------
def p_two_sided(m, null):
    null = np.asarray(null, dtype=np.float64)
    return float((1 + np.sum(np.abs(null) >= abs(m))) / (1 + len(null)))


def p_equal_tailed(m, null):
    null = np.asarray(null, dtype=np.float64)
    K = len(null)
    return float(min(1.0, 2 * min((1 + np.sum(null >= m)) / (1 + K), (1 + np.sum(null <= m)) / (1 + K))))


def holm(pvals, alpha, m=None):
    """名 → p を受け、名 → {'p','step','pass'}。p < 段（下回る）で通し、通らなかった所で止める（段階 B の集計器と同じ）。"""
    m = m or len(pvals)
    order = sorted(pvals, key=lambda k: (pvals[k], k))
    out, still = {}, True
    for i, k in enumerate(order):
        step = alpha / (m - i)
        ok = still and pvals[k] < step
        out[k] = {'p': pvals[k], 'step': step, 'pass': ok}
        still = ok
    return out


def top_rank(m, comps):
    """実在の差の札: |m| が比べる相手の |値| のすべてを上回れば最上位（同じ値は上回らない）。順位は 1 ＋ #{|c| ≥ |m|}。"""
    c = np.abs(np.asarray(comps, dtype=np.float64))
    return {'top': bool(np.all(abs(m) > c)), 'rank': int(1 + np.sum(c >= abs(m))), 'of': int(len(c) + 1)}


# ---------------- 順位相関と門 ----------------
def avg_ranks(x):
    x = np.asarray(x, dtype=np.float64)
    order = np.argsort(x, kind='mergesort')
    r = np.empty(len(x), dtype=np.float64)
    xs = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and xs[j + 1] == xs[i]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = avg_ranks(x), avg_ranks(y)
    rx, ry = rx - rx.mean(), ry - ry.mean()
    den = math.sqrt(float(rx @ rx) * float(ry @ ry))
    return float(rx @ ry / den) if den > 0 else float('nan')


def gate_perm(rows, unit_vals, units):
    """方向を単位にした並べ替えの門（片側・全ての入れ替え）。

    rows: [{'unit','sign','fam','y'}]・unit_vals: 単位 → {家族: 物差しの値}・units: 入れ替える単位の並び（rows の単位はこの中）。
    戻り値: {'rho','p','n_perm','n_rows'}。ρ が定まらない（順位が一定）ときは p を 1 にする。"""
    rows = [r for r in rows if r['unit'] in units]
    y = np.array([r['y'] for r in rows], dtype=np.float64)
    idx = {u: i for i, u in enumerate(units)}
    ui = np.array([idx[r['unit']] for r in rows])
    sg = np.array([r['sign'] for r in rows], dtype=np.float64)
    fams = sorted(set(r['fam'] for r in rows))
    fi = np.array([fams.index(r['fam']) for r in rows])
    V = np.array([[unit_vals[u][f] for f in fams] for u in units], dtype=np.float64)
    ry = avg_ranks(y)
    ry = ry - ry.mean()

    def rho_of(perm):
        x = sg * V[np.asarray(perm)[ui], fi]
        rx = avg_ranks(x)
        rx = rx - rx.mean()
        den = math.sqrt(float(rx @ rx) * float(ry @ ry))
        return float(rx @ ry / den) if den > 0 else float('nan')

    obs = rho_of(list(range(len(units))))
    if math.isnan(obs):
        return {'rho': obs, 'p': 1.0, 'n_perm': math.factorial(len(units)), 'n_rows': len(rows)}
    ge = n = 0
    for perm in itertools.permutations(range(len(units))):
        r_ = rho_of(perm)
        n += 1
        if not math.isnan(r_) and r_ >= obs - EPS_TIE:
            ge += 1
    return {'rho': obs, 'p': ge / n, 'n_perm': n, 'n_rows': len(rows)}


def logit_cc(k, n, c):
    return math.log((k + c) / (n - k + c))


# ---------------- 語の側の帰無 ----------------
def strata_groups(cand_cells, need_cells, n_bands, merge_factor):
    """層の組み立て。cand_cells・need_cells: (字の種類, 字数, 帯) → 数。戻り値: (字の種類, 字数) → [(帯の組, 候補の数, 要る数)]・組めたか。

    要る数のある (字の種類, 字数) ごとに、帯を一つずつの組から始め、候補の数が要る数の merge_factor 倍に満たない組
    （要る数のある組のうち帯の小さい順の最初）を、帯の真ん中の側の隣の組と合わせる（組の帯の平均が真ん中なら下の側）。足りるまで繰り返す。"""
    mid = (n_bands - 1) // 2
    out, ok = collections.OrderedDict(), True
    for tl in sorted(set((t, l) for t, l, b in need_cells)):
        gs = [[b] for b in range(n_bands)]
        while True:
            need = lambda g_: sum(need_cells.get(tl + (b,), 0) for b in g_)
            cand = lambda g_: sum(cand_cells.get(tl + (b,), 0) for b in g_)
            short = [g_ for g_ in gs if need(g_) and cand(g_) < merge_factor * need(g_)]
            if not short or len(gs) == 1:
                ok = ok and not short
                break
            k = gs.index(short[0])
            centre = sum(short[0]) / len(short[0])
            to = k + 1 if centre < mid else (k - 1 if centre > mid else (k - 1 if k > 0 else k + 1))
            lo, hi = sorted((k, to))
            gs = gs[:lo] + [gs[lo] + gs[hi]] + gs[hi + 1:]
        out[tl] = [(tuple(g_), sum(cand_cells.get(tl + (b,), 0) for b in g_), sum(need_cells.get(tl + (b,), 0) for b in g_)) for g_ in gs]
    return out, ok


def word_side_draws(delta, plus, minus, cell_of, candidates, groups, draws, seed):
    """語の側の帰無の抽選（v̂ を固定し、E+ と E− と同じ層の組み立てで、候補から重ならずに引く）。

    delta: 語彙の Δℓ（添字で引ける）・cell_of: トークン → (字の種類, 字数, 帯)・groups: `strata_groups` の出力。
    各抽選で、層（(字の種類, 字数) の昇順・その中の帯の組の順）ごとに、候補（トークンの番号の昇順）から E+ と E− の要る数の和だけを重ならずに引き、
    先の要る数を E+ に、残りを E− に当てる（乱数は `np.random.default_rng(seed)`）。戻り値: M_E の帰無の値（draws 本）。"""
    rng = np.random.default_rng(seed)
    plan = []
    for tl, gl in groups.items():
        for g_, nc, nn in gl:
            npl = sum(1 for t in plus if cell_of(t)[:2] == tl and cell_of(t)[2] in g_)
            nmi = sum(1 for t in minus if cell_of(t)[:2] == tl and cell_of(t)[2] in g_)
            if npl + nmi == 0:
                continue
            cs = np.array(sorted(t for t in candidates if cell_of(t)[:2] == tl and cell_of(t)[2] in g_), dtype=np.int64)
            assert len(cs) >= npl + nmi, ('層の候補が要る数に足りない', tl, g_)
            plan.append((cs, npl, nmi))
    dv = np.asarray(delta, dtype=np.float64)
    out = np.empty(draws, dtype=np.float64)
    for k in range(draws):
        ps, ms = [], []
        for cs, npl, nmi in plan:
            pick = cs[rng.choice(len(cs), size=npl + nmi, replace=False)]
            ps.append(pick[:npl])
            ms.append(pick[npl:])
        pp = np.concatenate(ps) if ps else np.array([], dtype=np.int64)
        mm = np.concatenate(ms) if ms else np.array([], dtype=np.int64)
        out[k] = dv[pp].mean() - (dv[mm].mean() if len(mm) else 0.0)
    return out


# ---------------- 大きさの目盛り ----------------
def transform(logits, temperature, top_k, top_p):
    """B の標本化の変換（transformers 4.57 の順と式: 温度で割る → top_k（k 番目以上を残す）→ top_p（昇順の累積が 1 − top_p 以下を落とす・最後の一つは残す））。
    戻り値: 変換の後の確率（float64・足して一）。"""
    z = np.asarray(logits, dtype=np.float64) / float(temperature)
    k = min(int(top_k), z.size)
    kth = np.partition(z, -k)[-k]
    z = np.where(z < kth, -np.inf, z)
    order = np.argsort(z, kind='mergesort')
    zs = z[order]
    fin = np.isfinite(zs)
    ps = np.zeros_like(zs)
    ps[fin] = np.exp(zs[fin] - zs[fin].max())
    ps = ps / ps.sum()
    cum = np.cumsum(ps)
    remove = cum <= (1.0 - float(top_p))
    remove[-1] = False
    keep = np.ones(z.size, dtype=bool)
    keep[order[remove]] = False
    z = np.where(keep, z, -np.inf)
    p = np.zeros_like(z)
    f = np.isfinite(z)
    p[f] = np.exp(z[f] - z[f].max())
    return p / p.sum()


def binom_central(n, p, ci):
    """二項分布 Bin(n, p) の中央の区間 [lo, hi]（下の裾と上の裾がそれぞれ (1 − ci)／2 を超えない最も狭い整数の区間）。"""
    a = (1.0 - float(ci)) / 2.0
    k = np.arange(n + 1)
    if p <= 0:
        return 0, 0
    if p >= 1:
        return n, n
    logpmf = np.array([math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * math.log(p) + (n - i) * math.log1p(-p) for i in k])
    pmf = np.exp(logpmf - logpmf.max())
    pmf = pmf / pmf.sum()
    cdf = np.cumsum(pmf)
    sf = np.cumsum(pmf[::-1])[::-1]
    lo = int(k[np.argmax(cdf > a)])                  # P(X < lo) ≤ a
    hi = int(k[len(k) - 1 - np.argmax(sf[::-1] > a)])   # P(X > hi) ≤ a
    return lo, hi


def z_two_sample(k0, n0, k1, n1, c):
    """観測の変化の二標本の z（率に連続性の補正を入れた標準誤差・転記行 E と同じ式）。"""
    q0, q1 = (k0 + c) / (n0 + 2 * c), (k1 + c) / (n1 + 2 * c)
    se = math.sqrt(q0 * (1 - q0) / n0 + q1 * (1 - q1) / n1)
    d = k1 / n1 - k0 / n0
    return d, d / se


def rms(h, eps):
    h = np.asarray(h, dtype=np.float64)
    return math.sqrt(float(np.mean(h * h)) + eps)


def direct_path(Zh, Zu, h, u, alpha, eps):
    """正確な直接の経路と、その分け方（出口の値の変化・全語彙）。

    Zh = W_E·(g⊙h)・Zu = W_E·(g⊙u)（どちらも正規化の前の量）。α u は加えた量（係数 × ‖v̂‖ の比・腕の符号つき）。
    戻り値: {'before','after','exact','layer1','along','scale'}（出口の値・float64）。
      layer1 = (α／rms(h))·Zu・along = −α (h·u)／(d·rms(h)³)·Zh（一次の展開の ĥ に沿う部分）・scale = exact − layer1 − along。"""
    h = np.asarray(h, dtype=np.float64)
    u = np.asarray(u, dtype=np.float64)
    d = h.size
    r0 = rms(h, eps)
    r1 = rms(h + alpha * u, eps)
    Zh = np.asarray(Zh, dtype=np.float64)
    Zu = np.asarray(Zu, dtype=np.float64)
    before = Zh / r0
    after = (Zh + alpha * Zu) / r1
    exact = after - before
    layer1 = (alpha / r0) * Zu
    along = -alpha * float(h @ u) / (d * r0 ** 3) * Zh
    return {'before': before, 'after': after, 'exact': exact, 'layer1': layer1, 'along': along, 'scale': exact - layer1 - along}


# ---------------- 自己検査 ----------------
def _selftest():
    rng = np.random.default_rng(0)
    # 割合と Holm
    assert p_two_sided(3.0, [1, -4, 2, 3]) == (1 + 2) / 5
    assert p_equal_tailed(0.0, [1, 2, 3, 4]) == min(1.0, 2 * min(5 / 5, 1 / 5))
    h = holm({'a': 0.001, 'b': 0.03, 'c': 0.2}, 0.05)
    assert h['a']['pass'] and not h['b']['pass'] and not h['c']['pass']          # 0.03 は 0.025 を下回らない
    h2 = holm({'a': 0.025, 'b': 0.001}, 0.05)
    assert h2['b']['pass'] and h2['a']['pass'] is True                            # 二段目は 0.05 を下回る
    h3 = holm({'a': 0.025, 'b': 0.04}, 0.05)
    assert not h3['a']['pass'] and not h3['b']['pass']                            # 一段目がちょうど 0.025 は下回らない（p < 段）
    assert top_rank(5.0, [1, -5, 2])['top'] is False and top_rank(5.1, [1, -5, 2])['top'] is True
    # 順位相関（scipy と突き合わせる・手元にあるとき）
    x, y = rng.normal(size=30), rng.normal(size=30)
    x[3] = x[4]
    try:
        from scipy.stats import spearmanr
        assert abs(spearman(x, y) - spearmanr(x, y)[0]) < 1e-12
    except ImportError:
        pass
    # 門: 一つの単位の値だけ大きい → 並べ替えで p は小さくならない（単位は 4 本・24 通り）
    rows = [{'unit': u, 'sign': 1, 'fam': 'f', 'y': float(i)} for i, u in enumerate(['A', 'A', 'B', 'C', 'D', 'D'])]
    uv = {'A': {'f': 0.0}, 'B': {'f': 1.0}, 'C': {'f': 2.0}, 'D': {'f': 3.0}}
    g_ = gate_perm(rows, uv, ['A', 'B', 'C', 'D'])
    assert g_['n_perm'] == 24 and abs(g_['p'] - 1 / 24) < 1e-12 and g_['rho'] > 0.9
    g0 = gate_perm(rows, {k: {'f': 1.0} for k in uv}, ['A', 'B', 'C', 'D'])
    assert g0['p'] == 1.0
    # 層の組み立て: 薄い層は真ん中の側と合わせる・真ん中は下の側
    cand = {('K', '1', 0): 50, ('K', '1', 1): 50, ('K', '1', 2): 2, ('K', '1', 3): 50, ('K', '1', 4): 3}
    need = {('K', '1', 2): 1, ('K', '1', 4): 1}
    gr, ok = strata_groups(cand, need, 5, 5)
    assert ok and [g[0] for g in gr[('K', '1')]] == [(0,), (1, 2), (3, 4)], gr
    # 標本化の変換を transformers の warper と突き合わせる（手元にあるとき）
    try:
        import torch
        from transformers.generation.logits_process import TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper
        for _ in range(20):
            lg = rng.normal(size=500).astype(np.float32) * 3
            t = torch.tensor(lg[None, :])
            for w in (TemperatureLogitsWarper(0.7), TopKLogitsWarper(top_k=20), TopPLogitsWarper(top_p=0.9)):
                t = w(None, t)
            ref = torch.softmax(t, dim=-1)[0].double().numpy()
            got = transform(lg, 0.7, 20, 0.9)
            assert np.array_equal(ref > 0, got > 0) and np.max(np.abs(ref - got)) < 1e-6, np.max(np.abs(ref - got))
    except ImportError:
        pass
    # 二項分布の区間
    lo, hi = binom_central(200, 0.77, 0.999)
    assert lo < 154 < hi and binom_central(154, 1.0, 0.999) == (154, 154) and binom_central(50, 0.0, 0.999) == (0, 0)
    # 直接の経路: 小さな α で一次の展開に近づく
    d = 64
    W = rng.normal(size=(40, d))
    gg = rng.uniform(0.5, 1.5, size=d)
    hv = rng.normal(size=d) * 5
    uv_ = rng.normal(size=d)
    Zh, Zu = W @ (gg * hv), W @ (gg * uv_)
    small = direct_path(Zh, Zu, hv, uv_, 1e-4, 1e-6)
    assert np.max(np.abs(small['scale'])) < 1e-6 * max(1.0, np.max(np.abs(small['exact'])))
    big = direct_path(Zh, Zu, hv, uv_, 2.0, 1e-6)
    assert np.allclose(big['exact'], big['layer1'] + big['along'] + big['scale'])
    # 等方の方向: 種と層の割合で決まり、ノルムがそろう
    v = rng.normal(size=d).astype(np.float32)
    D1 = iso_directions(v, 81001, 0.5, 5, 1000)
    D2 = iso_directions(v, 81001, 0.5, 5, 1000)
    assert np.array_equal(D1, D2) and np.allclose(np.linalg.norm(D1, axis=1), float(np.linalg.norm(v)))
    print('[blens_core] 自己検査 OK（%s）' % VERSION)


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest()
    else:
        print(__doc__)
