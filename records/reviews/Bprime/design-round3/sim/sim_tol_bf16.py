# -*- coding: utf-8 -*-
"""sim_tol_bf16.py v0（2026-09-29・B′ の設計の巡・三巡目・コーディネータの模擬の計算・束の外の計算）。
何を見るか: 出口の値の自己検査の許容〈tol(z) ＝ k × bf16 の刻み(|z|)〉の前提（模型の出口〔bf16 の道〕と float32 で当て直した値の差が、|z| に比例する分だけか）を、乱数の小さな道で確かめる。
Gemma の重み・残差の偏り・GPU の核は写さない（形の確かめだけ・推論の材料）。値は Gemma の値ではない。
bf16 は float32 の上位 16 ビットへの最近接偶数の丸めで模す。出力は印字だけで、記録には採否の表から名と SHA で指す。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import sys, io, math
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SEED, D, V, CAP, EPS = 20260929, 5376, 20000, 30.0, 1e-6


def bf16(x):
    x = np.asarray(x, dtype=np.float32)
    b = x.view(np.uint32).astype(np.uint64)
    lsb = (b >> 16) & 1
    r = ((b + 0x7FFF + lsb) >> 16) << 16
    return r.astype(np.uint32).view(np.float32)


def ulp_bf16(z):
    a = np.abs(z).astype(np.float64)
    e = np.floor(np.log2(np.maximum(a, 1e-38)))
    return np.power(2.0, e - 7)


def rmsnorm(x, w):
    x = x.astype(np.float32)
    r = np.sqrt(np.mean(x * x, axis=-1, keepdims=True) + EPS)
    return x / r * (1.0 + w)


def main():
    rng = np.random.default_rng(SEED)
    w = (rng.standard_normal(D) * 0.3).astype(np.float32)
    W = bf16(rng.standard_normal((V, D)).astype(np.float32) * 0.03)
    rows = []
    for t in range(4):
        h = rng.standard_normal(D).astype(np.float32) * 3.0
        h[rng.choice(D, 8, replace=False)] *= 40.0      # 突出した次元を少し
        h = bf16(h)
        # 模型の道（bf16 に丸める所を模す）
        hn = bf16(rmsnorm(h, w))
        zr = bf16(W.astype(np.float32) @ hn.astype(np.float32))
        zm = bf16(bf16(np.tanh(bf16(zr / CAP))) * CAP)
        # float32 の道（あり・なし・二重）
        hn32 = rmsnorm(h, w)
        z32 = W.astype(np.float32) @ hn32
        z_on = CAP * np.tanh(z32 / CAP)
        z_off = z32
        hn2 = rmsnorm(hn32, w)
        z_dbl = CAP * np.tanh((W.astype(np.float32) @ hn2) / CAP)
        rows.append((zm, z_on, z_off, z_dbl))
    zm = np.concatenate([r[0] for r in rows]); z_on = np.concatenate([r[1] for r in rows])
    z_off = np.concatenate([r[2] for r in rows]); z_dbl = np.concatenate([r[3] for r in rows])
    d = np.abs(zm.astype(np.float64) - z_on)
    u = ulp_bf16(zm)
    a = np.abs(zm)
    print('rows', len(zm), '| |z| max %.2f | median %.3f' % (a.max(), np.median(a)))
    edges = [0, 0.01, 0.1, 1, 2, 4, 8, 16, 32]
    print('bin | n | max diff | median diff | max diff/ulp(|z|)')
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = (a >= lo) & (a < hi)
        if s.sum():
            print('[%g,%g) | %d | %.5f | %.5f | %.1f' % (lo, hi, s.sum(), d[s].max(), np.median(d[s]), (d[s] / u[s]).max()))
    for z0 in (0.0, 1.0, 2.0, 4.0, 8.0):
        uu = ulp_bf16(np.maximum(a, z0)) if z0 > 0 else u
        k = 2 * (d / uu).max()
        tol = k * uu
        exp_off = np.abs(z_off - z_on)
        usable = exp_off > 3 * tol
        print('z0=%g | k=%.2f | tol at |z|=20: %.3f | rows usable for off-check: %d | top z_on among usable: %s' % (
            z0, k, k * ulp_bf16(np.array([20.0]))[0] if z0 <= 20 else float('nan'), usable.sum(), ('%.2f' % z_on[usable].max()) if usable.any() else '-'))


if __name__ == '__main__':
    main()
