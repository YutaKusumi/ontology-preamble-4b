# -*- coding: utf-8 -*-
"""vprime_power.py —— 追補 V′ の検出力（両側 Fisher・全数列挙・y 閾値は二分探索）。power_grid_vprime.py と design_facts_vprime.py が共有する唯一の実装。"""
from scipy.stats import fisher_exact, binom
import numpy as np


def make_power(n):
    def power(p0, p1, alpha):
        px = binom.pmf(np.arange(n + 1), n, p0); py = binom.pmf(np.arange(n + 1), n, p1); cdf = np.cumsum(py); tot = 0.0
        for x in range(n + 1):
            if px[x] < 1e-14:
                continue
            lo, hi = x, n + 1
            while lo < hi:
                mid = (lo + hi) // 2
                if fisher_exact([[x, n - x], [mid, n - mid]])[1] <= alpha: hi = mid
                else: lo = mid + 1
            yh = lo; lo, hi = -1, x - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if fisher_exact([[x, n - x], [mid, n - mid]])[1] <= alpha: lo = mid
                else: hi = mid - 1
            yl = lo
            tot += px[x] * ((1 - cdf[yh - 1] if yh <= n else 0.0) + (cdf[yl] if yl >= 0 else 0.0))
        return tot
    return power
