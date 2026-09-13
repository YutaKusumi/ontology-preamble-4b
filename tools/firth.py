# -*- coding: utf-8 -*-
"""firth.py v1 —— Firth 罰則つきロジスティック回帰（Jeffreys 事前・修正スコア Newton）と罰則付きプロファイル尤度比検定（PPLRT）の基準実装（numpy のみ・2026-09-13）。
段階 A の傾きの族（β₃＝arm×z の交互作用）の検定と検出力格子（power_grid_A.py）が読む。R `logistf` との一致検査は firth_check_A.py（公開データ・凍結前）。
参照: Firth (1993) Biometrika 80:27–38・Heinze & Schemper (2002) Stat Med 21:2409–2419。
"""
import numpy as np


def _fit(X, y, fixed=None, max_iter=200, tol=1e-8):
    """fixed: {index: value} で係数を固定（PPLRT の制約付き当てはめ）。戻り値: (beta, penalized loglik, converged)"""
    n, p = X.shape; beta = np.zeros(p); free = np.array([i for i in range(p) if not (fixed and i in fixed)])
    if fixed:
        for i, v in fixed.items():
            beta[i] = v
    for it in range(max_iter):
        eta = X @ beta; mu = 1 / (1 + np.exp(-eta)); w = mu * (1 - mu)
        XW = X * w[:, None]; I = X.T @ XW
        try:
            Iinv = np.linalg.inv(I)
        except np.linalg.LinAlgError:
            return beta, -np.inf, False
        h = np.einsum('ij,jk,ik->i', XW, Iinv, X)          # hat 行列の対角（重み付き）
        U = X.T @ (y - mu + h * (0.5 - mu))                 # 修正スコア
        step = np.zeros(p)
        If = I[np.ix_(free, free)]
        try:
            step[free] = np.linalg.solve(If, U[free])
        except np.linalg.LinAlgError:
            return beta, -np.inf, False
        # ステップ幅の抑制（分離気味のデータで発散しないため）
        mx = np.max(np.abs(step)) if step.size else 0.0
        if mx > 5:
            step *= 5 / mx
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            break
    eta = X @ beta; mu = 1 / (1 + np.exp(-eta)); w = mu * (1 - mu)
    I = X.T @ (X * w[:, None]); sign, logdet = np.linalg.slogdet(I)
    ll = np.sum(y * eta - np.log1p(np.exp(eta))) + 0.5 * logdet
    return beta, ll, it < max_iter - 1


def firth_fit(X, y):
    return _fit(X, y)


def pplrt(X, y, idx):
    """係数 idx の PPLRT（両側）。戻り値: dict(beta, stat, p, converged)"""
    from scipy.stats import chi2
    b_full, ll_full, c1 = _fit(X, y); b_res, ll_res, c2 = _fit(X, y, fixed={idx: 0.0})
    stat = max(0.0, 2 * (ll_full - ll_res)); p = float(chi2.sf(stat, 1))
    return {'beta': float(b_full[idx]), 'stat': float(stat), 'p': p, 'converged': bool(c1 and c2), 'beta_all': b_full.tolist()}


def design(arm, z):
    """行列 [1, arm, z, arm*z]"""
    arm = np.asarray(arm, float); z = np.asarray(z, float)
    return np.column_stack([np.ones_like(arm), arm, z, arm * z])


if __name__ == '__main__':   # 自己検査: 分離データで発散しない・帰無で p が一様に近い
    rng = np.random.default_rng(0); zs = np.array([-1.9, -0.86, 0.0, 0.69, 1.25, 2.08]); ps = []
    for _ in range(300):
        rows = []
        for a in (0, 1):
            for zz in zs:
                yk = rng.binomial(1, 0.3, 200); rows.append(np.column_stack([np.full(200, a), np.full(200, zz), yk]))
        R = np.vstack(rows); X = design(R[:, 0], R[:, 1]); r = pplrt(X, R[:, 2], 3); ps.append(r['p'])
    ps = np.array(ps); print('null p<0.05 rate (300 sims):', round(float((ps < 0.05).mean()), 3))
    # 分離: 対照が全 0
    rows = []
    for a in (0, 1):
        for zz in zs:
            yk = np.zeros(200) if a == 0 else rng.binomial(1, 0.3, 200); rows.append(np.column_stack([np.full(200, a), np.full(200, zz), yk]))
    R = np.vstack(rows); X = design(R[:, 0], R[:, 1]); r = pplrt(X, R[:, 2], 3); print('separated control: beta3', round(r['beta'], 3), 'p', round(r['p'], 3), 'converged', r['converged'])
