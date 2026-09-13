# -*- coding: utf-8 -*-
"""bands_A.py v1 —— 段階 A の帯と門の厳密計算の共通関数（2026-09-13・登録者裁定 D9 の三つ目の手順）。
格子（tools/power_grid_A.py の転記行 G・H・I・M）と、門・校正帯の器（tools/gate_A.py・tools/calib_band_A.py）が同じ関数を import する（二重実装をしない）。
- 観測値に帯を当てる判定（分数の厳密比較・「超」）: over_band（二標本・両側）・below_band（二標本・下側）・below_base（一標本・下側）。
- 発火率（二項の厳密和・整数演算で境界）: pmf・diff_tail（二標本・両側）・lower_tail（二標本・下側）・lower_k（一標本の下側の整数境界）。
- 環境帯の選択規則の期待誤保留数: env_expected_held（確証の全対比について、対比の二腕 × 橋の機種のいずれかが帯を超える確率の和）。
用法: python tools/bands_A.py --selftest（判定と整数境界の一致・発火率の和の検算）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import sys, math, json, os
from fractions import Fraction
import numpy as np
from scipy.stats import binom
VERSION = 'v1'


def pmf(nn, p):
    return binom.pmf(np.arange(nn + 1), nn, p)


def diff_tail(n1, p1, n2, p2, band_pt, strict=True):
    """P(|X1/n1 − X2/n2| > band)（strict=False なら ≥）。整数演算で境界を判定。"""
    W = np.outer(pmf(n1, p1), pmf(n2, p2)); D = np.abs(np.arange(n1 + 1)[:, None] * n2 - np.arange(n2 + 1)[None, :] * n1) * 100; thr = band_pt * n1 * n2
    return float(W[D > thr].sum()) if strict else float(W[D >= thr].sum())


def lower_tail(n1, p1, n2, p2, band_pt):
    """P(X1/n1 < X2/n2 − band)（超・整数演算）。"""
    W = np.outer(pmf(n1, p1), pmf(n2, p2)); D = (np.arange(n2 + 1)[None, :] * n1 - np.arange(n1 + 1)[:, None] * n2) * 100
    return float(W[D > band_pt * n1 * n2].sum())


def lower_k(base, nn, band_pt):
    """一標本の下側の整数境界: k/n < base − band ⇔ k ≤ この値（base は Fraction）。"""
    return math.ceil(base * nn - Fraction(band_pt, 100) * nn) - 1


def over_band(k1, n1, k2, n2, band_pt):
    """|k1/n1 − k2/n2| > band（二標本・両側・超・分数の厳密比較）。"""
    return abs(Fraction(int(k1), int(n1)) - Fraction(int(k2), int(n2))) > Fraction(band_pt) / 100


def below_band(k1, n1, k2, n2, band_pt):
    """k1/n1 < k2/n2 − band（二標本・下側・超）。"""
    return Fraction(int(k1), int(n1)) < Fraction(int(k2), int(n2)) - Fraction(band_pt) / 100


def below_base(k, n, base, band_pt):
    """k/n < base − band（一標本・下側・超・base は Fraction）。"""
    return Fraction(int(k), int(n)) < base - Fraction(band_pt) / 100


def env_expected_held(rates, band_pt, n, contrasts, n_models):
    """確証の全対比の期待誤保留数と腕ごとの帯の超過確率（両環境が同じ真の率・二項の差・超）。"""
    q = {arm: diff_tail(n, p, n, p, band_pt) for arm, p in rates.items()}
    return float(sum(1 - ((1 - q[c['A']]) * (1 - q[c['B']])) ** n_models for c in contrasts)), q


def _selftest():
    here = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(os.path.dirname(here), 'design', 'contrasts-A.json'), encoding='utf-8'))
    bb = T['bases_4B2507_api'][T['calibration']['scenario']][T['calibration']['arm']]; base = Fraction(bb['k'], bb['n']); lines = []
    for nn in range(1, 501):
        for band in (T['calibration']['band_pass']['pt'], T['calibration']['withdrawal']['band_pt']):
            kk = lower_k(base, nn, band)
            assert all((k <= kk) == below_base(k, nn, base, band) for k in range(nn + 1)), (nn, band)
    lines.append('1 一標本の下側: n=1〜500・二つの帯で整数境界と分数の比較が一致')
    rng = np.random.default_rng([20260913, 11])
    for _ in range(20000):
        n1, n2 = int(rng.integers(1, 401)), int(rng.integers(1, 401)); k1, k2 = int(rng.integers(0, n1 + 1)), int(rng.integers(0, n2 + 1)); band = int(rng.choice([5, 12, 15]))
        assert over_band(k1, n1, k2, n2, band) == (abs(k1 * n2 - k2 * n1) * 100 > band * n1 * n2)
        assert below_band(k1, n1, k2, n2, band) == ((k2 * n1 - k1 * n2) * 100 > band * n1 * n2)
    lines.append('2 二標本の両側と下側: 乱数 20,000 組で分数の比較と整数演算が一致')
    for n1, n2, p in ((40, 160, 0.9), (200, 200, 0.5), (400, 400, 0.975)):
        W = np.outer(pmf(n1, p), pmf(n2, p)); tot = 0.0
        for i in range(n1 + 1):
            for j in range(n2 + 1):
                tot += W[i, j] * over_band(i, n1, j, n2, 12)
        assert abs(tot - diff_tail(n1, p, n2, p, 12)) < 1e-12, (n1, n2, p, tot)
    lines.append('3 diff_tail: 三組で判定関数による逐一の和と一致（差 < 1e-12）')
    print('bands_A.py %s SELFTEST PASS' % VERSION); print('\n'.join(lines))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest()
