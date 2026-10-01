The earlier script is still on disk. I'll re-run it unchanged to confirm the numbers reproduce, and print its SHA so the pasted code can be matched.## 1. 許容の形と z₀

**先に訂正**

追い問いのために、許容の形を比べる模擬 2 を書いて走らせました（2 の 2-2）。その結果、元の指摘 1 の二か所を正します。

- 「どの位置でも「見分ける力が無い」になります」は言い過ぎでした。
  - 検査と同じ選び方の行（読み取りの集合 5 ＋ 上位 64）で k を測ると、草案6 の形の k は種によって 15.6〜20646.5 と大きく揺れました。
  - 「なし」を見分けた位置は、64 のうち 0〜46 でした。
  - 正しい実装が「あり」で落ちた位置も、10 回のうち 1 回で 1/64 ありました。
  - 正しくは「多くの位置で見分ける力が無くなり、ときに正しい実装が落ちる」です。
- 元の模擬（2-1）では |z| が 8 を超える行が一つも出ていません（区間 [8,16) と [16,31) は行数 0）。指摘 1 の「z＝20 で tol は約 1258」は、k × 刻み(20) を式で出した値で、その大きさの行を標本にした値ではありません。

**推すのは案 B**

〈tol(z) ＝ k × 刻み(max(|z|, z₀))〉で、k は検査と同じ選び方の行で測ります（3 の測り方）。理由は次のとおりです。

1. 測る定数が k 一つです。round2/rulings-D265.md の「softcap の自己検査の倍率（許容は意味のない列で測った〈差 ÷ bf16 の刻み〉の最大の 2 倍・見分けに使う行は見込みの差が許容の 3 倍を超える行）」を、刻みを取る値を替えるだけでそのまま使えます。案 A は t₀ という二つ目の測る値と、その倍率の決まりが新しく要ります。
2. いつも定まります。案 A は、測った行が z₀ の片側にしか無いと片方の定数が出ません（模擬 2 の既定の種・なだらかな位置だけ・z₀＝8 で k が出なかった）。案 B はどの z₀ でも出ます。
3. 大きい |z| の行を測りに入れたとき、z₀＝1 と 4 で案 A と案 B の成績に差はありませんでした（五つの種で「あり」の落ちは 0）。
4. 案 B の弱みは、小さい行の絶対の差が大きい機種では k 全体が膨らむことです。z₀ を大きめに取って抑えます。

**推す z₀＝4 と、その根拠**

Gemma での経験の根拠はありません。値を見る前に置ける根拠は次の四つです。

- (a) 見分ける力を削りません。案 B で z₀ が効くのは |z| < z₀ の行だけです。
  - 「なし」の見込みの差 z − 30·tanh(z/30) は、z＝4 で 0.0235、z＝8 で 0.184 です（私の計算）。束の round1/facts-round1.md §6 にも「差が 0.5 に届く z は 11.256」とあります。
  - つまり |z| < 8 の行は、もともと「なし」の見分けに使える行になりません。
  - 模擬 2 でも、z₀ を 8 まで上げて見分けた位置の数は減りませんでした（測りに大きい行を入れたとき）。
- (b) 床を層三より緩めません。
  - 床は k × 刻み(4) ＝ k/32 です。層三の許容は reference/contrasts-Bl3.json の `computation.logit_tol` で 0.5 です。
  - k ≤ 16 なら、床は層三の許容以下にとどまります。凍結の前の確かめに「k ≤ 16」の assert を足すことを推します。
- (c) 4 は 2 の冪で、[4, 8) は bf16 の一つの桁です。この範囲の中では刻みが段にならず一定です。
- (d) 小さい行の絶対の差の影響を抑えます。
  - 元の模擬で比が膨らむのは |z| が 0.5 あたりより下でした（[0.1, 0.5) で最大 20.6、[0.5, 1) で 3.1）。
  - Gemma の出口の値の広がりがこれより大きければ、膨らむ所も上にずれます（推論）。4 はその余白です。

**条件と機械の切り替え（今決める形）**

- z₀＝4 は、測りに大きい |z| の行が入っていることが条件です。模擬 2 で、なだらかな位置だけで測ると、種 3 で「あり」が 1/64 落ちました。
- そこで、測った行のうち |z| ≥ 16 の行が決めた数に届くことを、凍結の前の確かめで assert します。
- 届かないときは、機械で z₀＝1 に切り替えます。z₀＝1 は模擬 2 の十回すべてで落ち 0 でした。このときの床の assert は k ≤ 64 です（k × 刻み(1) ＝ k/128 ≤ 0.5）。
- z₀ と「届く数」は新しい約束の値なので、登録者の裁定に上げる形になります。

## 2. 模擬の計算の符号と結果

環境は、手元の容器の CPU、Python 3.12.3、NumPy 2.4.4 です（torch は使っていません）。二つのファイルを下に付けました。

### 2-1. 元の模擬（指摘 1 に書いた数の出所）

`ulp_sim.py`（SHA-256 42ca2ad1d4e7829820d87e55dc5f3e88b70113c80f6530a6e064f1e9b0884058）。乱数の種は `default_rng(0)` です。この答えのために走らせ直し、検分のときと同じ出力になることを確かめました。

```python
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
```

**結果（全 20000 行 × 8 位置）**

|z| の分位（5・50・95・99.9%）は 0.096・1.035・3.006・5.008 でした。

| |z| の区間 | 〈差÷刻み〉の最大 | 中央値 | 行数 |
|---|---|---|---|
| [0, 0.01) | 5032.2 | 58.65 | 840 |
| [0.01, 0.1) | 136.9 | 5.67 | 7526 |
| [0.1, 0.5) | 20.6 | 1.17 | 32576 |
| [0.5, 1) | 3.1 | 0.50 | 36585 |
| [1, 2) | 2.6 | 0.34 | 51427 |
| [2, 4) | 2.2 | 0.34 | 29601 |
| [4, 8) | 1.3 | 0.27 | 1445 |
| [8, 16)・[16, 31) | —（行なし） | — | 0 |

- 全行から出した k は 10064.5、|z| ≥ 4 の行だけで出した k は 2.5（小数一桁に丸めた印字）です。
- z＝5〜29 の tol と見込みの差の行は、この k から式で出した値です（例: z＝20 で tol 1258.06、見込みの差 4.142）。

### 2-2. この追い問いのために新しく書いた模擬 2（1 の比べの出所）

`tol_forms_sim.py`（SHA-256 07d448bcfcfc40a0a548748694e4a4ac29e24873a6d635be63a90b4368da37f2）。種は既定で 20260929 で、引数で替えられます（`python3 tol_forms_sim.py 3`）。

置いた仮定は三つで、どれも私の置き方です。

- 「検査の位置」は、読み取りの集合の 5 行の softcap 前の値を −10〜50 の一様乱数にした位置で、本物の読み取りの位置の代わりです。
- 「確かな予測の位置」は、読み取りの集合でない 3 行を 10〜50 にした位置で、繰り返しの列の代わりです。
- 「二重」の見込みの差は、float32 どうしの差（二重 − あり）で出しました。

```python
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
```

**結果の読み方**

各欄は「k・あり落ち・なし見分け」で、どれも 64 の検査の位置のうちの数です。「測り」は、k を測った位置の種類です。

- 「なだらか」は、なだらかな位置 16 だけで測ったもの（測った行の |z| の最大は 5.24〜6.21）です。
- 「混ぜ」は、なだらか 16 ＋ 確かな予測の位置 16 で測ったもの（同じく 24.18〜25.01）です。

| 種 | 測り | 草案6 の形 | B z₀＝1 | B z₀＝4 | A z₀＝1 | A z₀＝4 |
|---|---|---|---|---|---|---|
| 20260929 | なだらか | 15.6・1・46 | 4.05・0・63 | 2.02・0・64 | 4.05・0・63 | 1.55・1・64 |
| 20260929 | 混ぜ | 15.6・1・46 | 4.33・0・63 | 2.86・0・63 | 4.33・0・63 | 2.86・0・63 |
| 1 | なだらか | 23.5・0・5 | 4.34・0・63 | 2.17・0・63 | 4.34・0・63 | 1.72・0・63 |
| 1 | 混ぜ | 20646.5・0・0 | 4.34・0・63 | 2.50・0・63 | 4.34・0・63 | 2.50・0・63 |
| 2 | なだらか | 35.8・0・0 | 4.08・0・64 | 2.04・0・64 | 4.08・0・64 | 1.57・0・64 |
| 2 | 混ぜ | 35.8・0・0 | 4.08・0・64 | 2.74・0・64 | 4.08・0・64 | 2.74・0・64 |
| 3 | なだらか | 278.1・0・0 | 4.26・0・62 | 2.13・1・63 | 4.26・0・62 | 1.64・2・64 |
| 3 | 混ぜ | 278.1・0・0 | 4.32・0・62 | 2.92・0・63 | 4.32・0・62 | 2.92・0・63 |
| 4 | なだらか | 25.2・0・6 | 4.00・0・64 | 2.00・0・64 | 4.00・0・64 | 1.60・0・64 |
| 4 | 混ぜ | 273.3・0・0 | 4.00・0・64 | 2.00・0・64 | 4.00・0・64 | 1.78・0・64 |

- 「二重」は、案 A と案 B ではすべての回で 64/64 見分けました。
- 草案6 の形では、二重を見分けた位置は 0〜64 と揺れました。
- 既定の種の全出力（z₀＝0.5・2・8 を含む）は、ファイルを走らせると出ます。

## 3. k を測る位置と行

**草案6 の字**

§4.2 は、検査の位置と行を決めています。

- 「同じ位置で、softcap あり・なし・正規化の二重の三つを float32 で出し、模型の出口の値（bf16）と突き合わせる。」
- 「掛ける行は、読み取りの集合の行と、その位置の全語彙で出口の値の大きい上位の行（数は正本）。」
- 「下見の頭と本の計算の頭で走らせ、本の計算の頭では合否だけを印字する〔S15〕。」
- 位置は §3.1 の読み取りの位置「列の最後（主位置 ＋ 書き出しの長さ）。」です。

§12 は、測ることだけを書いています。

- 「実物の重みで、意味のない列: float32 の正規化・語彙の行列・softcap を通した値と模型の出口（bf16）の差を測り、§4.2 の許容の式の k を決める〔R05・S13〕」
- 意味のない列の定めは「場面の文・八つの腕の文・JSON の指示・主の書き出しと V1〜V3 の文字列のどれも含まない列（長さを升目にそろえること・チャットの型を当てることは許す）」です。
- 印字は「許容の式に要る差（「あり」と出口の差の最大・「なし」「二重」との差の最小を、出口の大きさの区間ごとに）」が許され、「意味のない列でも出口の値そのもの・上位のトークン・読み取りの集合の文字の出口の値」は許されません。

§12 には、列のどの位置で、どの行で、どのバッチで測るかがありません。これが元の指摘の「k を測る行が決まっていません」です。

**推す測り方**

- **位置**: 意味のない列の最後の位置です。これが検査の「列の最後」に当たります。
  - 列の組み立ては、チャットの型の user の発話を意味のない列にし、生成の口 `<channel|>` の後に意味のない 7 トークンを置く形です。
  - 長さは、八升目の読み取りの位置＋1（台帳 records/ledger-bprime.md の読み取りの位置の列は 428〜502）にそろえます。
- **列の種類**: 二種類を入れます。
  - なだらかな列: ランダムなトークンの列です。
  - 確かな予測の列: user の発話にランダムなトークンの塊を置き、`<channel|>` の後の 7 トークンをその塊の頭の 7 つと同じにします。本物の読み取りの位置も、書き出しがプロンプトの中の雛形の頭と同じ並びなので、写しの形が構造として似ています。この列で Gemma の出口に大きい |z| の行が出るかは推論で、確かめていません。
  - 模擬 2 では、大きい |z| の行を測りに入れないと、z₀＝4 で正しい実装が落ちる回がありました（2-2 の表の種 3）。
  - どちらの列も、トークンの番号を選ぶときに、禁じた文字列を割ったトークンの番号を除きます。器は、戻した文字列が禁じた文字列を含まないことを assert します。
- **行**: 検査と同じ選び方にします。
  - 読み取りの集合の番号は、意味のない列には族が無いので、a b c d ref の五つ全部を使います。
  - これに、その位置の出口の値の上位 N 行（N は正本の同じ数）を足します。
  - 全語彙では測りません（元の模擬で k が約 1 万になった形）。
- **数**: 八つの長さ × 二種類 × 中身二つ ＝ 32 位置を推します（約束の値で、根拠はありません）。
  - 検査の位置（下見の頭で八升目）より多く測る理由は、最大の 2 倍が検査の側の最大を下回りにくくするためです。
- **バッチ**: 検査を走らせるバッチの大きさで測ります。
  - 正本 `readout.primary.batch` の 16 と、§3.3「下見の (vi) の (a) が上限を超えたら、本の計算はバッチの大きさを一にする（§4.5）。」の 1 の両方で測り、大きい方の k を使います。
  - bf16 の行列積の核がバッチで替わりうるためです（推論）。
- **印字と assert**:
  - 印字は、k と区間ごとの差の最大（§12 が許すもの）に、区間ごとの行数を足します。行数は出口の値の粗いまとめなので、§12 の印字してよい値の一覧に字で足す必要があります。
  - assert は三つです: |z| ≥ 16 の行が決めた数に届くこと・k ≤ 16（z₀＝4 のとき）・届かないときは z₀＝1 に機械で切り替え、k ≤ 64。

**付け足し（草案の字から）**

§4.2 は見込みの差の式を「softcap の抜けなら z − cap·tanh(z/cap)」としか書いておらず、「二重」の見込みの差の式がありません。模擬 2 では float32 どうしの差（二重 − あり）を使いました。器に要る式なので、凍結の前に書く必要があります。

## この追い問いの答えで確認していないこと

- Gemma の実物での出口の値の絶対の差の大きさは確かめていません。transformers 5.16.1 の Gemma 4 が、最終の正規化の出力を bf16 に丸めてから語彙の行列を掛けるかも、ソースを読んでいません。模擬の丸めの置き方は推論です。
- GPU の bf16 の行列積の核（タイルの切り方・和の順）は写していません。模擬は CPU の numpy だけです。
- 繰り返しの列の最後の位置で、Gemma の出口に |z| ≥ 16 の行が出るかは推論です。
- 模擬 2 の「検査の位置」と「確かな予測の位置」の作り方は私の仮定で、本物の読み取りの位置の出口の分布は分かりません。
- 種は五つだけです。落ちは 64 のうち 1〜2 の少ない出来事で、割合としては粗い値です。
- 正本の「上位の行」の数 N は決まっておらず、模擬では 64 を使いました。本の計算の頭の自己検査が何位置に掛かるかも、§4.2 の字からは読み取れませんでした。
- この答えのために束を読み直したのは、§3.1・§3.3・§4.2・§12 の引いた行と、round1/facts-round1.md §6・round2/rulings-D265.md・reference/contrasts-Bl3.json の `computation` だけです。ほかの所は読み直していません。

本研究のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。