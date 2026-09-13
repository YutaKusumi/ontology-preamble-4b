# -*- coding: utf-8 -*-
"""firth.py v2 —— Firth 罰則つきロジスティック回帰（Jeffreys 事前・修正スコアの Fisher scoring・step-halving）と罰則付きプロファイル尤度比検定（PPLRT）の基準実装（numpy・scipy・2026-09-13）。
v2 の変更（claude.ai 三票の採否表 C39〜C41）:
  - 二項の集約形（行＝共変量の型・成功数 y・試行数 m）を基本形にした（ベルヌーイ行は m=1 の特例）。集約形とベルヌーイ行の一致は自己検査で確かめる。
  - 対数尤度は logaddexp、平均は expit（あふれで −inf になり p=1 に落ちる経路を除いた）。
  - 罰則付き対数尤度が増えることを確かめる step-halving を入れた。
  - 収束はスコア（修正スコアの最大絶対値）とステップ幅で判定し、converged は「収束で抜けたか」を返す（v1 の `it < max_iter-1` は最終反復で収束すると偽になった）。
  - 自己検査は assert つき（`python tools/firth.py --selftest [--B 2000]`）: 集約形とベルヌーイ行の一致・BFGS による直接最大化との照合・帰無の棄却率（中間・上昇・床・天井）・分離（主効果・β₃ 型・二規模の全 0・完全分離）・あふれ・converged の判定。
PPLRT の制約付き当てはめは、制約下でも全模型の罰則 ½log|X'WX| を最大化する（Heinze & Schemper 2002）。R logistf との一致検査は firth_check_A.py（合否規則は design/contrasts-A.json の firth_check）。
参照: Firth (1993) Biometrika 80:27–38・Heinze & Schemper (2002) Stat Med 21:2409–2419。
"""
import sys
import numpy as np
from scipy.special import expit
from scipy.stats import chi2

VERSION = 'v2.1'   # v2.1（2026-09-14・登録者裁定 D18）: pplrt が当てはめの打ち切り（gtol・tol・max_iter など）を fit に受け渡す。算法は v2 と同じ


def _state(X, y, m, beta):
    """罰則付き対数尤度・情報行列・平均・重み（二項の集約形）。"""
    eta = X @ beta
    mu = expit(eta)
    W = m * mu * (1.0 - mu)
    I = X.T @ (X * W[:, None])
    sign, logdet = np.linalg.slogdet(I)
    if sign <= 0 or not np.isfinite(logdet):
        return -np.inf, I, mu, W
    ll = float(np.sum(y * eta - m * np.logaddexp(0.0, eta))) + 0.5 * float(logdet)
    return ll, I, mu, W


def fit(X, y, m=None, fixed=None, max_iter=200, tol=1e-9, gtol=1e-7, max_halving=40, max_step=5.0):
    """Firth 当てはめ。X: 行列・y: 成功数・m: 試行数（None ならベルヌーイ）・fixed: {列: 値}（PPLRT の制約）。
    戻り値 dict: beta・ll（罰則付き対数尤度）・converged（収束で抜けたか）・iterations・score_max（自由座標の修正スコアの最大絶対値）。"""
    X = np.asarray(X, dtype=float); y = np.asarray(y, dtype=float)
    m = np.ones_like(y) if m is None else np.asarray(m, dtype=float)
    p = X.shape[1]; fixed = dict(fixed or {})
    beta = np.zeros(p)
    for i, v in fixed.items():
        beta[int(i)] = float(v)
    free = np.array([i for i in range(p) if i not in fixed], dtype=int)
    ll, I, mu, W = _state(X, y, m, beta)
    if not np.isfinite(ll):
        return {'beta': beta, 'll': -np.inf, 'converged': False, 'iterations': 0, 'score_max': float('inf')}
    converged = False; it = 0; gmax = float('inf')
    for it in range(1, max_iter + 1):
        try:
            Iinv = np.linalg.inv(I)
        except np.linalg.LinAlgError:
            break
        h = W * np.einsum('ij,jk,ik->i', X, Iinv, X)                 # hat 行列の対角（集約形では試行数を含む）
        U = X.T @ (y - m * mu + h * (0.5 - mu))                       # 修正スコア＝罰則付き対数尤度の勾配
        if free.size == 0:
            converged = True; gmax = 0.0; break
        gmax = float(np.max(np.abs(U[free])))
        try:
            step = np.linalg.solve(I[np.ix_(free, free)], U[free])
        except np.linalg.LinAlgError:
            break
        smax = float(np.max(np.abs(step)))
        if gmax < gtol or (smax < tol and gmax < 1e-5):
            converged = True; break
        if smax > max_step:
            step = step * (max_step / smax)
        t = 1.0; accepted = False
        for _ in range(max_halving):
            cand = beta.copy(); cand[free] = beta[free] + t * step
            ll_c, I_c, mu_c, W_c = _state(X, y, m, cand)
            if np.isfinite(ll_c) and ll_c >= ll - 1e-12 * max(1.0, abs(ll)):
                beta, ll, I, mu, W = cand, ll_c, I_c, mu_c, W_c; accepted = True; break
            t *= 0.5
        if not accepted or t * min(smax, max_step) < 1e-15:
            break
    return {'beta': beta, 'll': ll, 'converged': converged, 'iterations': it, 'score_max': gmax}


def _fit(X, y, fixed=None, max_iter=200, tol=1e-9):
    """v1 互換: (beta, 罰則付き対数尤度, converged)。"""
    r = fit(X, y, None, fixed=fixed, max_iter=max_iter, tol=tol)
    return r['beta'], r['ll'], r['converged']


def firth_fit(X, y, m=None):
    return fit(X, y, m)


def pplrt(X, y, idx, m=None, **fit_kw):
    """係数 idx の PPLRT（両側・χ²₁）。fit_kw は fit の打ち切り（gtol・tol・max_iter）。戻り値 dict: beta・stat・p（非収束なら None）・converged・beta_all・ll_full・ll_restricted。"""
    rf = fit(X, y, m, **fit_kw); rr = fit(X, y, m, fixed={idx: 0.0}, **fit_kw)
    ok = bool(rf['converged'] and rr['converged'] and np.isfinite(rf['ll']) and np.isfinite(rr['ll']))
    if ok:
        stat = max(0.0, 2.0 * (rf['ll'] - rr['ll'])); p = float(chi2.sf(stat, 1))
    else:
        stat = float('nan'); p = None
    return {'beta': float(rf['beta'][idx]), 'stat': stat, 'p': p, 'converged': ok, 'beta_all': rf['beta'].tolist(), 'll_full': rf['ll'], 'll_restricted': rr['ll']}


def design(arm, z):
    """行列 [1, arm, z, arm*z]"""
    arm = np.asarray(arm, float); z = np.asarray(z, float)
    return np.column_stack([np.ones_like(arm), arm, z, arm * z])


def slope_rows(z_sizes, k_ctrl, k_trt, n_ctrl, n_trt):
    """規模ごとの対照・処置の成功数と試行数から集約形の (X, y, m) を作る（行＝規模 × 腕・対照 arm=0・処置 arm=1）。"""
    zz = np.repeat(np.asarray(z_sizes, float), 2); arm = np.tile([0.0, 1.0], len(z_sizes))
    y = np.column_stack([k_ctrl, k_trt]).ravel().astype(float); m = np.column_stack([n_ctrl, n_trt]).ravel().astype(float)
    return design(arm, zz), y, m


# ----------------------------------------------------------------------------------------------------------------
def _selftest(B=2000):
    """assert つきの自己検査。閾値はこの関数に書いた値のまま（結果を見て動かさない）。"""
    from scipy.optimize import minimize
    import os, json
    from zaxis_A import z_sizes   # z は実パラメータ数から機械計算（凍結前検分の採否表 P60・直書きしない）
    _T = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'design', 'contrasts-A.json'), encoding='utf-8'))
    zs = np.array(z_sizes(_T['sizes'])); n = _T['n_per_arm']; N6 = np.full(len(zs), n)
    rng = np.random.default_rng([20260913, 1]); lines = []

    # 1. 集約形とベルヌーイ行の一致（統計量・係数）
    pc = np.linspace(0.3, 0.9, 6); pt = np.clip(pc + 0.12, 0.001, 0.999)
    kc = rng.binomial(n, pc); kt = rng.binomial(n, pt)
    Xa, ya, ma = slope_rows(zs, kc, kt, N6, N6)
    ra_, rz_, ry_ = [], [], []
    for i in range(6):
        ra_ += [0] * n + [1] * n; rz_ += [zs[i]] * (2 * n)
        ry_ += [1] * int(kc[i]) + [0] * (n - int(kc[i])) + [1] * int(kt[i]) + [0] * (n - int(kt[i]))
    ra = pplrt(Xa, ya, 3, ma); rb = pplrt(design(ra_, rz_), np.array(ry_, float), 3)
    d_stat = abs(ra['stat'] - rb['stat']); d_beta = float(np.max(np.abs(np.array(ra['beta_all']) - np.array(rb['beta_all']))))
    assert ra['converged'] and rb['converged'], 'agg/bernoulli not converged'
    assert d_stat < 1e-7 and d_beta < 1e-7, ('agg/bernoulli mismatch', d_stat, d_beta)
    lines.append('1 集約形とベルヌーイ行: 統計量の差 %.2e・係数の差 %.2e（許容 1e-7）' % (d_stat, d_beta))

    # 2. BFGS による罰則付き対数尤度の直接最大化との照合（全模型と制約付き）
    def neg(bfree, X, y, m, free, fixed):
        b = np.zeros(X.shape[1]); b[free] = bfree
        for i, v in fixed.items():
            b[i] = v
        ll, _, _, _ = _state(X, y, m, b)
        return -ll if np.isfinite(ll) else 1e300
    cfgs = [('床', np.full(6, 0.03), np.clip(0.03 + 0.05 * (zs - zs[2]) / (zs[-1] - zs[2]), 0.001, 0.999)),
            ('天井', np.full(6, 0.97), np.clip(0.97 - 0.10 * (zs - zs[2]) / (zs[-1] - zs[2]), 0.001, 0.999)),
            ('中間', np.full(6, 0.5), np.clip(0.5 + 0.15 * (zs - zs[2]) / (zs[-1] - zs[2]), 0.001, 0.999))]
    for name, p0, p1 in cfgs:
        kc = rng.binomial(n, p0); kt = rng.binomial(n, p1); X, y, m = slope_rows(zs, kc, kt, N6, N6)
        for fixed in ({}, {3: 0.0}):
            free = [i for i in range(4) if i not in fixed]
            r = fit(X, y, m, fixed=fixed)
            o = minimize(neg, np.zeros(len(free)), args=(X, y, m, free, fixed), method='BFGS', options={'gtol': 1e-10, 'maxiter': 20000})
            ll_b = -o.fun; bb = np.zeros(4); bb[free] = o.x
            assert r['converged'], ('bfgs cfg not converged', name, fixed)
            assert r['ll'] >= ll_b - 1e-6, ('newton below bfgs', name, fixed, r['ll'], ll_b)
            assert float(np.max(np.abs(r['beta'] - bb))) < 1e-3, ('beta differs from bfgs', name, fixed)
            lines.append('2 BFGS 照合 %s・%s: 罰則付き対数尤度 Newton−BFGS %+.2e・係数の差 %.2e' % (name, '制約 β₃=0' if fixed else '全模型', r['ll'] - ll_b, float(np.max(np.abs(r['beta'] - bb)))))

    # 3. 帰無の棄却率（β₃=0・n=200 × 6 規模 × 2 腕・検閲なし・B 回）
    for name, p0, mode in (('中間 0.5 一定', np.full(6, 0.5), 'two'), ('上昇 0.3→0.9', np.linspace(0.3, 0.9, 6), 'two'), ('床 0.03 一定', np.full(6, 0.03), 'upper'), ('天井 0.97 一定', np.full(6, 0.97), 'upper')):
        rej = nf = 0
        for _ in range(B):
            kc = rng.binomial(n, p0); kt = rng.binomial(n, p0); X, y, m = slope_rows(zs, kc, kt, N6, N6)
            r = pplrt(X, y, 3, m)
            if not r['converged']:
                nf += 1; continue
            rej += r['p'] < 0.05
        rate = rej / B
        assert nf == 0, ('null nonconverged', name, nf)
        if mode == 'two':
            assert 0.035 <= rate <= 0.065, ('null rate out of [0.035, 0.065]', name, rate)
        else:
            assert rate <= 0.065, ('null rate above 0.065', name, rate)
        lines.append('3 帰無の棄却率 %s: %.4f（B=%d・非収束 %d・許容 %s）' % (name, rate, B, nf, '[0.035, 0.065]' if mode == 'two' else '≤0.065'))

    # 4. 分離
    cases = []
    kc = np.zeros(6, int); kt = rng.binomial(n, 0.3, 6); cases.append(('主効果の分離（対照が全規模で 0）', kc, kt))
    kc = rng.binomial(n, 0.4, 6); kt = rng.binomial(n, 0.4, 6); kt[5] = 0; cases.append(('β₃ 型（処置が最大規模だけ 0）', kc, kt))
    kc = rng.binomial(n, 0.2, 6); kt = rng.binomial(n, 0.25, 6); kc[:2] = 0; kt[:2] = 0; cases.append(('両腕が二規模で 0', kc, kt))
    cases.append(('完全分離（対照すべて 0・処置すべて n）', np.zeros(6, int), np.full(6, n)))
    for name, kc, kt in cases:
        X, y, m = slope_rows(zs, kc, kt, N6, N6); r = pplrt(X, y, 3, m)
        assert r['converged'] and np.isfinite(r['stat']) and np.all(np.isfinite(r['beta_all'])) and 0.0 <= r['p'] <= 1.0, ('separation', name, r)
        lines.append('4 分離 %s: β₃ %.4f・統計量 %.4f・p %.4f・収束 %s' % (name, r['beta'], r['stat'], r['p'], r['converged']))

    # 5. あふれ（z を 50 倍にし、規模の前半 0・後半 n）
    X, y, m = slope_rows(zs * 50, np.array([0, 0, 0, n, n, n]), np.array([0, 0, 0, n, n, n]), N6, N6)
    with np.errstate(over='raise'):
        r = pplrt(X, y, 3, m)
    assert np.isfinite(r['ll_full']) and np.isfinite(r['ll_restricted']), ('overflow', r)
    lines.append('5 あふれ（z × 50・段差のある率）: 全模型 %.4f・制約 %.4f（有限）' % (r['ll_full'], r['ll_restricted']))

    # 6. converged の判定
    kc = rng.binomial(n, 0.5, 6); kt = rng.binomial(n, 0.6, 6); X, y, m = slope_rows(zs, kc, kt, N6, N6)
    r1 = fit(X, y, m, max_iter=1); rd = fit(X, y, m)
    assert (not r1['converged']) and rd['converged'], ('converged flag', r1['converged'], rd['converged'])
    r_exact = fit(X, y, m, max_iter=rd['iterations'])
    assert r_exact['converged'], ('converged at the last allowed iteration must be True', rd['iterations'])
    lines.append('6 converged: max_iter=1 で %s・既定で %s（反復 %d）・max_iter=%d（ちょうど収束の反復）で %s' % (r1['converged'], rd['converged'], rd['iterations'], rd['iterations'], r_exact['converged']))
    return lines


if __name__ == '__main__':
    B = 2000
    if '--B' in sys.argv:
        B = int(sys.argv[sys.argv.index('--B') + 1])
    for l in _selftest(B):
        print(l)
    print('firth.py %s SELFTEST PASS' % VERSION)
