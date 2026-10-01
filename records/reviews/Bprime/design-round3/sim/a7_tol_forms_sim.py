# 模擬 2: 許容の三つの形（草案6 の形・案 A・案 B）を、同じ乱数の模型で比べる。
# 実物の Gemma ではない（乱数の行列・次元 5376・cap 30・bf16 の丸めを numpy で模したもの）。
import numpy as np

import sys
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 20260929
rng = np.random.default_rng(SEED)

def bf16(x):
    x = np.asarray(x, dtype=np.float32)
    u = x.view(np.uint32).astype(np.uint64)
    r = ((u + 0x7FFF + ((u >> 16) & 1)) & 0xFFFF0000).astype(np.uint32)
    return r.view(np.float32)

def ulp_bf16(z):
    a = np.abs(np.asarray(z, dtype=np.float64))
    a = np.maximum(a, 2.0**-126)
    return 2.0 ** (np.floor(np.log2(a)) - 7)

d, V, cap = 5376, 20000, 30.0
W = bf16(rng.normal(0, 0.02, size=(V, d)).astype(np.float32))
Wf = W.astype(np.float32)
w_norm = bf16(rng.normal(1.0, 0.3, size=d).astype(np.float32))
READ = np.arange(5)          # 読み取りの集合の代わりの 5 行
TOPN = 64                    # 「出口の値の大きい上位の行」の数（模擬の値）

def rms(x): return np.sqrt(np.mean(x.astype(np.float32)**2) + 1e-6)

def make_h(hot_rows, hot_t):
    """hot_rows の softcap 前の値がおよそ hot_t になる残差を作る（乱数の部分と足す）。"""
    u = rng.normal(0, 1, size=d).astype(np.float32)
    for j, t in zip(hot_rows, hot_t):
        u = u + (t * Wf[j] / float(Wf[j] @ Wf[j])).astype(np.float32)
    wsafe = np.where(np.abs(w_norm) < 0.2, 0.2, w_norm)
    return bf16(u / wsafe * 40.0)

def paths(h):
    r = rms(h)
    hn_b = bf16((h / r) * w_norm)                       # 模型: 正規化を bf16 に丸める
    z_b = bf16(Wf @ hn_b.astype(np.float32))            # 和は float32・出口を bf16 に丸める
    z_b = bf16(bf16(np.tanh(bf16(z_b / cap))) * cap)    # softcap の各段を bf16 に丸める
    hn_f = (h / r) * w_norm
    raw = Wf @ hn_f
    z_f = np.tanh(raw / cap) * cap                      # 正しい再計算（あり）
    hn_2 = (hn_f / rms(hn_f)) * w_norm                  # 正規化の二重
    z_2 = np.tanh((Wf @ hn_2) / cap) * cap
    return z_b, z_f, raw, z_2

def select(z_f):
    top = np.argpartition(-z_f, TOPN)[:TOPN]
    return np.unique(np.concatenate([READ, top]))

def collect(kind, n):
    out = []
    for _ in range(n):
        if kind == "flat":        # 意味のない列のような、なだらかな位置
            h = make_h([], [])
        elif kind == "peaked":    # 繰り返しの列のような、確かな予測のある位置（読み取りの集合でない行が高い）
            rows = rng.choice(np.arange(5, V), size=3, replace=False)
            h = make_h(rows, rng.uniform(10, 50, size=3))
        elif kind == "readout":   # 本物の読み取りの位置の代わり: 読み取りの集合の行が -10〜50
            h = make_h(READ, rng.uniform(-10, 50, size=5))
        z_b, z_f, raw, z_2 = paths(h)
        s = select(z_f)
        out.append(dict(z=z_f[s], diff=np.abs(z_f[s] - z_b[s]), raw=raw[s],
                        d_nocap=np.abs(raw[s] - z_b[s]), d_dbl=np.abs(z_2[s] - z_b[s]),
                        e_dbl=np.abs(z_2[s] - z_f[s])))
    return out

def cat(rows, key): return np.concatenate([r[key] for r in rows])

meas_flat  = collect("flat", 16)
meas_peak  = collect("peaked", 16)
check      = collect("readout", 64)

def fit(meas, form, z0=None):
    z = np.abs(cat(meas, "z")); df = cat(meas, "diff")
    if form == "draft6":
        k = 2 * np.max(df / ulp_bf16(z)); return lambda zz: k * ulp_bf16(zz), dict(k=k)
    if form == "B":
        k = 2 * np.max(df / ulp_bf16(np.maximum(z, z0)))
        return lambda zz: k * ulp_bf16(np.maximum(np.abs(zz), z0)), dict(k=k)
    if form == "A":
        big = z >= z0
        k = 2 * np.max(df[big] / ulp_bf16(z[big])) if big.any() else np.nan
        t0 = 2 * np.max(df[~big]) if (~big).any() else k * ulp_bf16(z0)
        return lambda zz: np.maximum(k * ulp_bf16(zz), t0), dict(k=k, t0=t0)

def evaluate(tol):
    fail = 0; q_nc = 0; p_nc = 0; q_db = 0; p_db = 0
    for r in check:
        z = np.abs(r["z"]); t = tol(z)
        if np.any(r["diff"] > t): fail += 1
        gap = r["raw"] - cap * np.tanh(r["raw"] / cap)      # 式から出した「なし」の見込みの差
        m = np.abs(gap) > 3 * t
        if m.any():
            q_nc += 1; p_nc += int(np.max(r["d_nocap"][m] - t[m]) > 0)
        m2 = r["e_dbl"] > 3 * t                               # 「二重」の見込みの差（float32 どうし）
        if m2.any():
            q_db += 1; p_db += int(np.max(r["d_dbl"][m2] - t[m2]) > 0)
    n = len(check)
    return f"あり落ち {fail}/{n}・なし 掛けた位置 {q_nc}/{n} 見分けた {p_nc}・二重 掛けた位置 {q_db}/{n} 見分けた {p_db}"

zc = np.abs(cat(check, "z"))
print("種", SEED, "・検査の位置 64・一つの位置の行は 読み取りの集合 5 ＋ 上位", TOPN)
print("検査の行の |z| の分位（5・50・95・最大）:", np.round(np.percentile(zc, [5, 50, 95, 100]), 2))
for name, meas in [("なだらかな位置だけで測る", meas_flat),
                   ("なだらか 16 ＋ 確かな予測の位置 16 で測る", meas_flat + meas_peak)]:
    zm = np.abs(cat(meas, "z"))
    print(f"\n== {name}（測る行の |z| の最大 {zm.max():.2f}）")
    tol, p = fit(meas, "draft6"); print(f"  草案6 の形 k={p['k']:.1f}: {evaluate(tol)}")
    for z0 in [0.5, 1, 2, 4, 8]:
        tol, p = fit(meas, "B", z0); print(f"  案 B z0={z0:<3} k={p['k']:.2f}: {evaluate(tol)}")
    for z0 in [0.5, 1, 2, 4, 8]:
        tol, p = fit(meas, "A", z0); print(f"  案 A z0={z0:<3} k={p['k']:.2f} t0={p['t0']:.4f}: {evaluate(tol)}")
