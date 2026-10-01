# 模擬: bf16 の出口の値と float32 の再計算の差を、bf16 の刻み ulp(|z|) で割った比が |z| の小さい行で大きくなるかを見る。
# 実物の Gemma ではない（乱数の行列・次元と cap は目安）。
import numpy as np
rng = np.random.default_rng(0)

def bf16(x):
    x = np.asarray(x, dtype=np.float32)
    u = x.view(np.uint32).astype(np.uint64)
    r = ((u + 0x7FFF + ((u >> 16) & 1)) & 0xFFFF0000).astype(np.uint32)
    return r.view(np.float32)

def ulp_bf16(z):
    a = np.abs(z).astype(np.float64)
    a = np.maximum(a, 2.0**-126)
    return 2.0 ** (np.floor(np.log2(a)) - 7)

d, V, cap = 5376, 20000, 30.0
W = bf16(rng.normal(0, 0.02, size=(V, d)).astype(np.float32))
w_norm = bf16(rng.normal(1.0, 0.3, size=d).astype(np.float32))
ratios_all, z_all = [], []
for pos in range(8):
    h = bf16(rng.normal(0, 1, size=d).astype(np.float32) * 40)   # 残差（bf16）
    # 模型の道: 正規化を float32 で計算して bf16 に戻す → bf16 の重みと float32 の和 → bf16 → softcap も bf16 の刻みで
    rms = np.sqrt(np.mean(h.astype(np.float32)**2) + 1e-6)
    hn_b = bf16((h / rms) * w_norm)
    z_b = bf16(W.astype(np.float32) @ hn_b.astype(np.float32))
    z_b = bf16(bf16(np.tanh(bf16(z_b / cap))) * cap)
    # 再計算の道（float32）
    hn_f = (h.astype(np.float32) / rms) * w_norm
    z_f = W.astype(np.float32) @ hn_f
    z_f = np.tanh(z_f / cap) * cap
    ratios_all.append(np.abs(z_f - z_b) / ulp_bf16(z_f)); z_all.append(z_f)
r = np.concatenate(ratios_all); z = np.concatenate(z_all); az = np.abs(z)
print("出口の値の |z| の分位（5・50・95・99.9%）:", np.round(np.percentile(az,[5,50,95,99.9]),3))
bins = [0,0.01,0.1,0.5,1,2,4,8,16,31]
print("|z| の区間ごとの 〈差÷刻み〉 の最大と中央値・区間の行数:")
for lo,hi in zip(bins[:-1],bins[1:]):
    m = (az>=lo)&(az<hi)
    if m.sum(): print(f"  [{lo},{hi}) 最大 {r[m].max():10.1f}  中央 {np.median(r[m]):7.2f}  行数 {m.sum()}")
k = 2*r.max()
print("k（全行の比の最大の 2 倍）=", round(float(k),1))
# 「なし」を見分けに使える行: 見込みの差 z_raw - cap*tanh(z_raw/cap) > 3*tol(z)
for zz in [5,10,15,20,25,29]:
    raw = cap*np.arctanh(zz/cap)  # softcap 後が zz になる softcap 前の値
    gap = raw - zz
    print(f"  softcap 後 z={zz}: 抜けの見込みの差 {gap:7.3f}  tol(z)={k*ulp_bf16(zz):8.2f}  3*tol={3*k*ulp_bf16(zz):8.2f}")
# 大きい行だけ（|z|>=4）で k を出した場合
k4 = 2*r[az>=4].max()
print("参考: |z|>=4 の行だけで出した k =", round(float(k4),1))
