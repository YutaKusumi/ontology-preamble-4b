# 追補 V′ 設計事実（機械生成・contrasts draft6-2026-09-07・2026-09-07）

**転記行 A（規模）**: 4 シナリオ × 52 腕（単独 14＋組合せ 38）× 400 ＝ 83,200 試行（概算 ≈$8.3・約 23.1 時間・係数は本プログラム実績比のコーディネータ概算）。パイロット 20/腕 ＝ 4,160 試行。
**転記行 B（対比）**: 確証 57 本（Vprime_a m=25・Vprime_b m=8・Vprime_c m=24）・記述 141 本（Vprime_desc_neutral 48・Vprime_desc_dose 48・Vprime_desc_Nstr 5・Vprime_desc_cross 4・Vprime_desc_weakness 20・Vprime_desc_role 16）・id は全族を通じて一意（重複 0）・登録された対比を持たない腕 0。
**転記行 C（検出力の被覆）**: 確証 57 本のうち実測基底 24 本（V′a）・仮定基底 33 本（V′b 8・V′c 24・N1:Ncold~Nstr 1）。仮定基底の対比の検出力は走行前に確定できず、検出域の申告に用いない。
**転記行 D（全体 FWER）**: 確証族 3・最大 1−0.95^3 ≈ 0.143。
**転記行 E（反証条件の発火確率）**: 規則 1 の発火確率（O-Ncold の真値別・n=400・機械計算）: 真値 0.09（設計自身の想定）で N1 2.7e-152・S1 1.4e-49・S4 8.5e-65・SK 1.0e-142／真値 0.169（本プログラム最大観測）で N1 2.1e-90・S1 3.6e-20・S4 1.9e-29・SK 2.6e-83／旧閾値 0.20 は同順に 1.2e-11・0.059。すなわち規則 1 は「O が無力であること」を超え「O が有害に近いこと」を要求する線であり、設計の想定下では発火しない。撤回理由「真値 0.169 なら 94% 作動しない」は代替にはより強く当てはまる——撤回の宣言にも主張と同じ厳しさの検分を要求する（凍結記録の教訓・三巡目破器身）。発火しうる反証条件は規則 2 が担う。
**転記行 F（盤の未使用腕）**: G-hard・Lnegdose1・Lnegdosehalf・Ncold-O・Nwin・Odose1・Odosehalf（走行は --arms の一行 SHA16 5FBA99534207933D・52 腕・465 字のみ）。

## 発火確率表（規則 1・n=400・scipy.stats.binom.sf(k-1, n, p)・k=ceil(thr×n)）
| O-Ncold 真値 | 旧 0.20 | N1 | S1 | S4 | SK |
|---|---|---|---|---|---|
| 0.090 | 1.18e-11 | 2.67e-152 | 1.37e-49 | 8.54e-65 | 1.04e-142 |
| 0.169 | 5.85e-02 | 2.12e-90 | 3.58e-20 | 1.87e-29 | 2.60e-83 |
| 0.250 | 9.92e-01 | 5.89e-55 | 6.68e-07 | 3.68e-12 | 1.40e-49 |
| 0.300 | 1.00e+00 | 7.68e-40 | 5.73e-03 | 3.15e-06 | 2.47e-35 |

## --arms（正本から生成・手打ち禁止）
```
N,Nstr,Ncold,NcoldS,Ncold3,O,Osec,Onull,Nk,Nlib,Nai,Nneu1,Nneu2,Nneu3,O-Ncold,O-NcoldS,O-Ncold3,Osec-Ncold,Osec-NcoldS,Osec-Ncold3,Onull-Ncold,Onull-NcoldS,Onull-Ncold3,Nk-Ncold,Nk-NcoldS,Nk-Ncold3,Nlib-Ncold,Nlib-NcoldS,Nlib-Ncold3,Nai-Ncold,Nai-NcoldS,Nai-Ncold3,O-Nneu1,O-Nneu2,O-Nneu3,Osec-Nneu1,Osec-Nneu2,Osec-Nneu3,Onull-Nneu1,Onull-Nneu2,Onull-Nneu3,Nk-Nneu1,Nk-Nneu2,Nk-Nneu3,Nlib-Nneu1,Nlib-Nneu2,Nlib-Nneu3,Nai-Nneu1,Nai-Nneu2,Nai-Nneu3,O-Nstr,Onull-Nstr
```

本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
