# 追補 V′ 走行後の機械生成 —— tag stageVp・contrasts draft7-2026-09-07・2026-09-08

## 1. 実測基底での検出力（凍結格子の仮定基底行を実測で置き換えた併記・同一の検出力関数・n=400・族 α）
**凡例（一巡目検分の条件）**: 列「大・中・小」の感度は、実測基底 B が 0.05 以上の行では +15／+10／+5 pt、0.05 未満（床）の行では +9／+5／+2 pt。下向き対比（V′b）は −15／−10／−5 pt（B から引く）。α は当該対比の族の Holm 初段（V′a 0.05/25・V′b 0.05/8・V′c 0.05/32）。凍結格子の帯は V′a の α（0.05/25）で計算したもの。記述族（§1b）は検定を置かないため α=0.05 の参考値。丸め規約（三巡目で統一）: 本文書の実測差は整数件数から Decimal で計算し、pt は小数一桁・率差は小数三桁に四捨五入（.x5 はゼロから遠ざける・浮動小数の減算を経ない）。v2 までは浮動小数から丸めていたため .x5 型が絶対値の小さい側に落ちる行があった（三巡目宝生・28 行）。
| 族 | 対比 | 凍結格子の基底（出所） | 実測基底 B | 大 | 中 | 小 | 実測差 | α |
|---|---|---|---|---|---|---|---|---|
| Vprime_a | N1:O-Ncold~O | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.130 | 0.00200 |
| Vprime_a | N1:Osec-Ncold~Osec | 実測 0.003 | 0.000 | 1.000 | 0.996 | 0.282 | +0.368 | 0.00200 |
| Vprime_a | N1:Onull-Ncold~Onull | 実測 0.619 | 0.690 | 0.971 | 0.526 | 0.055 | +0.225 | 0.00200 |
| Vprime_a | N1:Nk-Ncold~Nk | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.020 | 0.00200 |
| Vprime_a | N1:Nlib-Ncold~Nlib | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.208 | 0.00200 |
| Vprime_a | N1:Nai-Ncold~Nai | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.970 | 0.00200 |
| Vprime_a | N1:Ncold~Nstr | 仮定 0.80 | 0.850 | 1.000 | 0.951 | 0.146 | +0.125 | 0.00200 |
| Vprime_a | S1:O-Ncold~O | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.330 | 0.00200 |
| Vprime_a | S1:Osec-Ncold~Osec | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.470 | 0.00200 |
| Vprime_a | S1:Onull-Ncold~Onull | 実測 0.359 | 0.370 | 0.868 | 0.383 | 0.044 | +0.518 | 0.00200 |
| Vprime_a | S1:Nk-Ncold~Nk | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.968 | 0.00200 |
| Vprime_a | S1:Nlib-Ncold~Nlib | 実測 0.016 | 0.033 | 0.960 | 0.438 | 0.030 | +0.933 | 0.00200 |
| Vprime_a | S1:Nai-Ncold~Nai | 実測 0.584 | 0.573 | 0.904 | 0.405 | 0.043 | +0.415 | 0.00200 |
| Vprime_a | S4:O-Ncold~O | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.240 | 0.00200 |
| Vprime_a | S4:Osec-Ncold~Osec | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.173 | 0.00200 |
| Vprime_a | S4:Onull-Ncold~Onull | 実測 0.406 | 0.370 | 0.868 | 0.383 | 0.044 | +0.503 | 0.00200 |
| Vprime_a | S4:Nk-Ncold~Nk | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +1.000 | 0.00200 |
| Vprime_a | S4:Nlib-Ncold~Nlib | 実測 0.009 | 0.010 | 0.999 | 0.785 | 0.083 | +0.990 | 0.00200 |
| Vprime_a | S4:Nai-Ncold~Nai | 実測 0.359 | 0.347 | 0.874 | 0.396 | 0.045 | +0.653 | 0.00200 |
| Vprime_a | SK:O-Ncold~O | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.555 | 0.00200 |
| Vprime_a | SK:Osec-Ncold~Osec | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.693 | 0.00200 |
| Vprime_a | SK:Onull-Ncold~Onull | 実測 0.600 | 0.578 | 0.906 | 0.408 | 0.043 | +0.330 | 0.00200 |
| Vprime_a | SK:Nk-Ncold~Nk | 実測 0.000 | 0.000 | 1.000 | 0.996 | 0.282 | +0.940 | 0.00200 |
| Vprime_a | SK:Nlib-Ncold~Nlib | 実測 0.322 | 0.380 | 0.867 | 0.379 | 0.043 | +0.620 | 0.00200 |
| Vprime_a | SK:Nai-Ncold~Nai | 実測 0.762 | 0.780 | 0.999 | 0.729 | 0.081 | +0.175 | 0.00200 |
| Vprime_b | N1:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.367 | 0.971 | 0.592 | 0.094 | -0.238 | 0.00625 |
| Vprime_b | N1:O-Ncold~Onull-Ncold | 仮定 0.80 | 0.915 | 0.999 | 0.913 | 0.281 | -0.785 | 0.00625 |
| Vprime_b | S1:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.470 | 0.941 | 0.523 | 0.083 | -0.140 | 0.00625 |
| Vprime_b | S1:O-Ncold~Onull-Ncold | 仮定 0.50 | 0.887 | 0.997 | 0.853 | 0.217 | -0.558 | 0.00625 |
| Vprime_b | S4:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.172 | 1.000 | 0.940 | 0.202 | +0.068 | 0.00625 |
| Vprime_b | S4:O-Ncold~Onull-Ncold | 仮定 0.55 | 0.873 | 0.995 | 0.818 | 0.195 | -0.633 | 0.00625 |
| Vprime_b | SK:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.693 | 0.943 | 0.559 | 0.095 | -0.138 | 0.00625 |
| Vprime_b | SK:O-Ncold~Onull-Ncold | 仮定 0.75 | 0.907 | 0.999 | 0.897 | 0.259 | -0.353 | 0.00625 |
| Vprime_c | N1:O-Ncold~O-Nneu1 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.130 | 0.00156 |
| Vprime_c | N1:O-Ncold~O-Nneu2 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.130 | 0.00156 |
| Vprime_c | N1:O-Ncold~O-Nneu3 | 仮定 0.00 | 0.005 | 1.000 | 0.889 | 0.107 | +0.125 | 0.00156 |
| Vprime_c | N1:Onull-Ncold~Onull-Nneu1 | 仮定 0.62 | 0.718 | 0.981 | 0.546 | 0.052 | +0.198 | 0.00156 |
| Vprime_c | N1:Onull-Ncold~Onull-Nneu2 | 仮定 0.62 | 0.637 | 0.931 | 0.428 | 0.041 | +0.278 | 0.00156 |
| Vprime_c | N1:Onull-Ncold~Onull-Nneu3 | 仮定 0.62 | 0.797 | 1.000 | 0.763 | 0.081 | +0.118 | 0.00156 |
| Vprime_c | S1:O-Ncold~O-Nneu1 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.330 | 0.00156 |
| Vprime_c | S1:O-Ncold~O-Nneu2 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.330 | 0.00156 |
| Vprime_c | S1:O-Ncold~O-Nneu3 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.330 | 0.00156 |
| Vprime_c | S1:Onull-Ncold~Onull-Nneu1 | 仮定 0.36 | 0.333 | 0.865 | 0.374 | 0.039 | +0.555 | 0.00156 |
| Vprime_c | S1:Onull-Ncold~Onull-Nneu2 | 仮定 0.36 | 0.338 | 0.862 | 0.372 | 0.039 | +0.550 | 0.00156 |
| Vprime_c | S1:Onull-Ncold~Onull-Nneu3 | 仮定 0.36 | 0.328 | 0.867 | 0.376 | 0.040 | +0.560 | 0.00156 |
| Vprime_c | S4:O-Ncold~O-Nneu1 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.240 | 0.00156 |
| Vprime_c | S4:O-Ncold~O-Nneu2 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.240 | 0.00156 |
| Vprime_c | S4:O-Ncold~O-Nneu3 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.240 | 0.00156 |
| Vprime_c | S4:Onull-Ncold~Onull-Nneu1 | 仮定 0.41 | 0.343 | 0.860 | 0.370 | 0.038 | +0.530 | 0.00156 |
| Vprime_c | S4:Onull-Ncold~Onull-Nneu2 | 仮定 0.41 | 0.292 | 0.882 | 0.401 | 0.043 | +0.580 | 0.00156 |
| Vprime_c | S4:Onull-Ncold~Onull-Nneu3 | 仮定 0.41 | 0.195 | 0.943 | 0.522 | 0.062 | +0.678 | 0.00156 |
| Vprime_c | SK:O-Ncold~O-Nneu1 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.555 | 0.00156 |
| Vprime_c | SK:O-Ncold~O-Nneu2 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.555 | 0.00156 |
| Vprime_c | SK:O-Ncold~O-Nneu3 | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.555 | 0.00156 |
| Vprime_c | SK:Onull-Ncold~Onull-Nneu1 | 仮定 0.60 | 0.542 | 0.875 | 0.362 | 0.035 | +0.365 | 0.00156 |
| Vprime_c | SK:Onull-Ncold~Onull-Nneu2 | 仮定 0.60 | 0.448 | 0.850 | 0.348 | 0.035 | +0.460 | 0.00156 |
| Vprime_c | SK:Onull-Ncold~Onull-Nneu3 | 仮定 0.60 | 0.497 | 0.856 | 0.348 | 0.035 | +0.410 | 0.00156 |
| Vprime_c | N1:O-Ncold~O-Nstr | 仮定 0.00 | 0.003 | 1.000 | 0.943 | 0.138 | +0.128 | 0.00156 |
| Vprime_c | N1:Onull-Ncold~Onull-Nstr | 仮定 0.62 | 0.757 | 0.995 | 0.641 | 0.063 | +0.158 | 0.00156 |
| Vprime_c | S1:O-Ncold~O-Nstr | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.330 | 0.00156 |
| Vprime_c | S1:Onull-Ncold~Onull-Nstr | 仮定 0.36 | 0.583 | 0.896 | 0.382 | 0.037 | +0.305 | 0.00156 |
| Vprime_c | S4:O-Ncold~O-Nstr | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.240 | 0.00156 |
| Vprime_c | S4:Onull-Ncold~Onull-Nstr | 仮定 0.41 | 0.635 | 0.929 | 0.425 | 0.041 | +0.238 | 0.00156 |
| Vprime_c | SK:O-Ncold~O-Nstr | 仮定 0.00 | 0.000 | 1.000 | 0.991 | 0.182 | +0.555 | 0.00156 |
| Vprime_c | SK:Onull-Ncold~Onull-Nstr | 仮定 0.60 | 0.623 | 0.921 | 0.413 | 0.040 | +0.285 | 0.00156 |

## 1b. 記述族の感度（参考・検定なし・α=0.05・同じ梯子）
| 族 | 対比 | 実測基底 B | 大 | 中 | 小 | 実測差 |
|---|---|---|---|---|---|---|
| Vprime_desc_neutral | N1:Osec-Ncold~Osec-Nneu1 | 0.007 | 1.000 | 0.988 | 0.491 | +36.0 pt |
| Vprime_desc_neutral | N1:Osec-Ncold~Osec-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +36.8 pt |
| Vprime_desc_neutral | N1:Osec-Ncold~Osec-Nneu3 | 0.005 | 1.000 | 0.994 | 0.562 | +36.3 pt |
| Vprime_desc_neutral | N1:Nk-Ncold~Nk-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +2.0 pt |
| Vprime_desc_neutral | N1:Nk-Ncold~Nk-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +2.0 pt |
| Vprime_desc_neutral | N1:Nk-Ncold~Nk-Nneu3 | 0.000 | 1.000 | 1.000 | 0.812 | +2.0 pt |
| Vprime_desc_neutral | N1:Nlib-Ncold~Nlib-Nneu1 | 0.003 | 1.000 | 0.998 | 0.666 | +20.5 pt |
| Vprime_desc_neutral | N1:Nlib-Ncold~Nlib-Nneu2 | 0.005 | 1.000 | 0.994 | 0.562 | +20.3 pt |
| Vprime_desc_neutral | N1:Nlib-Ncold~Nlib-Nneu3 | 0.000 | 1.000 | 1.000 | 0.812 | +20.8 pt |
| Vprime_desc_neutral | N1:Nai-Ncold~Nai-Nneu1 | 0.705 | 0.999 | 0.897 | 0.328 | +26.5 pt |
| Vprime_desc_neutral | N1:Nai-Ncold~Nai-Nneu2 | 0.365 | 0.988 | 0.798 | 0.280 | +60.5 pt |
| Vprime_desc_neutral | N1:Nai-Ncold~Nai-Nneu3 | 0.583 | 0.993 | 0.820 | 0.279 | +38.8 pt |
| Vprime_desc_neutral | S1:Osec-Ncold~Osec-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +47.0 pt |
| Vprime_desc_neutral | S1:Osec-Ncold~Osec-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +47.0 pt |
| Vprime_desc_neutral | S1:Osec-Ncold~Osec-Nneu3 | 0.000 | 1.000 | 1.000 | 0.812 | +47.0 pt |
| Vprime_desc_neutral | S1:Nk-Ncold~Nk-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +96.8 pt |
| Vprime_desc_neutral | S1:Nk-Ncold~Nk-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +96.8 pt |
| Vprime_desc_neutral | S1:Nk-Ncold~Nk-Nneu3 | 0.003 | 1.000 | 0.998 | 0.666 | +96.5 pt |
| Vprime_desc_neutral | S1:Nlib-Ncold~Nlib-Nneu1 | 0.003 | 1.000 | 0.998 | 0.666 | +96.3 pt |
| Vprime_desc_neutral | S1:Nlib-Ncold~Nlib-Nneu2 | 0.018 | 1.000 | 0.938 | 0.343 | +94.8 pt |
| Vprime_desc_neutral | S1:Nlib-Ncold~Nlib-Nneu3 | 0.007 | 1.000 | 0.988 | 0.491 | +95.8 pt |
| Vprime_desc_neutral | S1:Nai-Ncold~Nai-Nneu1 | 0.887 | 1.000 | 1.000 | 0.673 | +10.0 pt |
| Vprime_desc_neutral | S1:Nai-Ncold~Nai-Nneu2 | 0.435 | 0.988 | 0.793 | 0.273 | +55.3 pt |
| Vprime_desc_neutral | S1:Nai-Ncold~Nai-Nneu3 | 0.158 | 0.999 | 0.929 | 0.415 | +83.0 pt |
| Vprime_desc_neutral | S4:Osec-Ncold~Osec-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +17.3 pt |
| Vprime_desc_neutral | S4:Osec-Ncold~Osec-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +17.3 pt |
| Vprime_desc_neutral | S4:Osec-Ncold~Osec-Nneu3 | 0.000 | 1.000 | 1.000 | 0.812 | +17.3 pt |
| Vprime_desc_neutral | S4:Nk-Ncold~Nk-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +100.0 pt |
| Vprime_desc_neutral | S4:Nk-Ncold~Nk-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +100.0 pt |
| Vprime_desc_neutral | S4:Nk-Ncold~Nk-Nneu3 | 0.000 | 1.000 | 1.000 | 0.812 | +100.0 pt |
| Vprime_desc_neutral | S4:Nlib-Ncold~Nlib-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +100.0 pt |
| Vprime_desc_neutral | S4:Nlib-Ncold~Nlib-Nneu2 | 0.003 | 1.000 | 0.998 | 0.666 | +99.8 pt |
| Vprime_desc_neutral | S4:Nlib-Ncold~Nlib-Nneu3 | 0.000 | 1.000 | 1.000 | 0.812 | +100.0 pt |
| Vprime_desc_neutral | S4:Nai-Ncold~Nai-Nneu1 | 0.217 | 0.996 | 0.879 | 0.348 | +78.3 pt |
| Vprime_desc_neutral | S4:Nai-Ncold~Nai-Nneu2 | 0.297 | 0.992 | 0.827 | 0.302 | +70.3 pt |
| Vprime_desc_neutral | S4:Nai-Ncold~Nai-Nneu3 | 0.083 | 1.000 | 0.985 | 0.589 | +91.8 pt |
| Vprime_desc_neutral | SK:Osec-Ncold~Osec-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +69.3 pt |
| Vprime_desc_neutral | SK:Osec-Ncold~Osec-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +69.3 pt |
| Vprime_desc_neutral | SK:Osec-Ncold~Osec-Nneu3 | 0.000 | 1.000 | 1.000 | 0.812 | +69.3 pt |
| Vprime_desc_neutral | SK:Nk-Ncold~Nk-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +94.0 pt |
| Vprime_desc_neutral | SK:Nk-Ncold~Nk-Nneu2 | 0.000 | 1.000 | 1.000 | 0.812 | +94.0 pt |
| Vprime_desc_neutral | SK:Nk-Ncold~Nk-Nneu3 | 0.003 | 1.000 | 0.998 | 0.666 | +93.8 pt |
| Vprime_desc_neutral | SK:Nlib-Ncold~Nlib-Nneu1 | 0.000 | 1.000 | 1.000 | 0.812 | +100.0 pt |
| Vprime_desc_neutral | SK:Nlib-Ncold~Nlib-Nneu2 | 0.390 | 0.988 | 0.795 | 0.273 | +61.0 pt |
| Vprime_desc_neutral | SK:Nlib-Ncold~Nlib-Nneu3 | 0.158 | 0.999 | 0.929 | 0.415 | +84.3 pt |
| Vprime_desc_neutral | SK:Nai-Ncold~Nai-Nneu1 | 0.575 | 0.993 | 0.817 | 0.276 | +38.0 pt |
| Vprime_desc_neutral | SK:Nai-Ncold~Nai-Nneu2 | 0.685 | 0.999 | 0.880 | 0.316 | +27.0 pt |
| Vprime_desc_neutral | SK:Nai-Ncold~Nai-Nneu3 | 0.407 | 0.988 | 0.794 | 0.272 | +54.8 pt |
| Vprime_desc_dose | N1:O-NcoldS~O-Ncold | 0.130 | 1.000 | 0.952 | 0.461 | -11.8 pt |
| Vprime_desc_dose | N1:O-Ncold3~O-Ncold | 0.130 | 1.000 | 0.952 | 0.461 | -12.8 pt |
| Vprime_desc_dose | N1:Osec-NcoldS~Osec-Ncold | 0.367 | 0.988 | 0.797 | 0.279 | -31.3 pt |
| Vprime_desc_dose | N1:Osec-Ncold3~Osec-Ncold | 0.367 | 0.988 | 0.797 | 0.279 | -35.8 pt |
| Vprime_desc_dose | N1:Onull-NcoldS~Onull-Ncold | 0.915 | 1.000 | 1.000 | 0.824 | -17.8 pt |
| Vprime_desc_dose | N1:Onull-Ncold3~Onull-Ncold | 0.915 | 1.000 | 1.000 | 0.824 | -0.5 pt |
| Vprime_desc_dose | N1:Nk-NcoldS~Nk-Ncold | 0.020 | 1.000 | 0.923 | 0.318 | +27.8 pt |
| Vprime_desc_dose | N1:Nk-Ncold3~Nk-Ncold | 0.020 | 1.000 | 0.923 | 0.318 | +5.8 pt |
| Vprime_desc_dose | N1:Nlib-NcoldS~Nlib-Ncold | 0.207 | 0.997 | 0.886 | 0.357 | +62.3 pt |
| Vprime_desc_dose | N1:Nlib-Ncold3~Nlib-Ncold | 0.207 | 0.997 | 0.886 | 0.357 | +26.5 pt |
| Vprime_desc_dose | N1:Nai-NcoldS~Nai-Ncold | 0.970 | 0.948 | 0.948 | 0.948 | +3.0 pt |
| Vprime_desc_dose | N1:Nai-Ncold3~Nai-Ncold | 0.970 | 0.948 | 0.948 | 0.948 | +3.0 pt |
| Vprime_desc_dose | S1:O-NcoldS~O-Ncold | 0.330 | 0.989 | 0.814 | 0.291 | -30.8 pt |
| Vprime_desc_dose | S1:O-Ncold3~O-Ncold | 0.330 | 0.989 | 0.814 | 0.291 | -31.0 pt |
| Vprime_desc_dose | S1:Osec-NcoldS~Osec-Ncold | 0.470 | 0.988 | 0.793 | 0.274 | -24.5 pt |
| Vprime_desc_dose | S1:Osec-Ncold3~Osec-Ncold | 0.470 | 0.988 | 0.793 | 0.274 | -44.0 pt |
| Vprime_desc_dose | S1:Onull-NcoldS~Onull-Ncold | 0.887 | 1.000 | 1.000 | 0.673 | +3.3 pt |
| Vprime_desc_dose | S1:Onull-Ncold3~Onull-Ncold | 0.887 | 1.000 | 1.000 | 0.673 | +11.0 pt |
| Vprime_desc_dose | S1:Nk-NcoldS~Nk-Ncold | 0.968 | 0.968 | 0.968 | 0.968 | -14.0 pt |
| Vprime_desc_dose | S1:Nk-Ncold3~Nk-Ncold | 0.968 | 0.968 | 0.968 | 0.968 | -44.5 pt |
| Vprime_desc_dose | S1:Nlib-NcoldS~Nlib-Ncold | 0.965 | 0.981 | 0.981 | 0.981 | -0.3 pt |
| Vprime_desc_dose | S1:Nlib-Ncold3~Nlib-Ncold | 0.965 | 0.981 | 0.981 | 0.981 | +3.5 pt |
| Vprime_desc_dose | S1:Nai-NcoldS~Nai-Ncold | 0.988 | 0.295 | 0.295 | 0.295 | +1.3 pt |
| Vprime_desc_dose | S1:Nai-Ncold3~Nai-Ncold | 0.988 | 0.295 | 0.295 | 0.295 | +1.3 pt |
| Vprime_desc_dose | S4:O-NcoldS~O-Ncold | 0.240 | 0.995 | 0.862 | 0.331 | -19.8 pt |
| Vprime_desc_dose | S4:O-Ncold3~O-Ncold | 0.240 | 0.995 | 0.862 | 0.331 | -23.0 pt |
| Vprime_desc_dose | S4:Osec-NcoldS~Osec-Ncold | 0.172 | 0.998 | 0.916 | 0.395 | -5.5 pt |
| Vprime_desc_dose | S4:Osec-Ncold3~Osec-Ncold | 0.172 | 0.998 | 0.916 | 0.395 | -10.0 pt |
| Vprime_desc_dose | S4:Onull-NcoldS~Onull-Ncold | 0.873 | 1.000 | 1.000 | 0.608 | +6.0 pt |
| Vprime_desc_dose | S4:Onull-Ncold3~Onull-Ncold | 0.873 | 1.000 | 1.000 | 0.608 | +12.5 pt |
| Vprime_desc_dose | S4:Nk-NcoldS~Nk-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | -19.8 pt |
| Vprime_desc_dose | S4:Nk-Ncold3~Nk-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | -35.3 pt |
| Vprime_desc_dose | S4:Nlib-NcoldS~Nlib-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | +0.0 pt |
| Vprime_desc_dose | S4:Nlib-Ncold3~Nlib-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | +0.0 pt |
| Vprime_desc_dose | S4:Nai-NcoldS~Nai-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | +0.0 pt |
| Vprime_desc_dose | S4:Nai-Ncold3~Nai-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | +0.0 pt |
| Vprime_desc_dose | SK:O-NcoldS~O-Ncold | 0.555 | 0.992 | 0.806 | 0.272 | -51.0 pt |
| Vprime_desc_dose | SK:O-Ncold3~O-Ncold | 0.555 | 0.992 | 0.806 | 0.272 | -52.0 pt |
| Vprime_desc_dose | SK:Osec-NcoldS~Osec-Ncold | 0.693 | 0.999 | 0.886 | 0.320 | -39.0 pt |
| Vprime_desc_dose | SK:Osec-Ncold3~Osec-Ncold | 0.693 | 0.999 | 0.886 | 0.320 | -45.8 pt |
| Vprime_desc_dose | SK:Onull-NcoldS~Onull-Ncold | 0.907 | 1.000 | 1.000 | 0.779 | +7.0 pt |
| Vprime_desc_dose | SK:Onull-Ncold3~Onull-Ncold | 0.907 | 1.000 | 1.000 | 0.779 | +8.0 pt |
| Vprime_desc_dose | SK:Nk-NcoldS~Nk-Ncold | 0.940 | 1.000 | 1.000 | 0.978 | -1.5 pt |
| Vprime_desc_dose | SK:Nk-Ncold3~Nk-Ncold | 0.940 | 1.000 | 1.000 | 0.978 | -34.3 pt |
| Vprime_desc_dose | SK:Nlib-NcoldS~Nlib-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | -1.3 pt |
| Vprime_desc_dose | SK:Nlib-Ncold3~Nlib-Ncold | 1.000 | 0.000 | 0.000 | 0.000 | +0.0 pt |
| Vprime_desc_dose | SK:Nai-NcoldS~Nai-Ncold | 0.955 | 0.998 | 0.998 | 0.998 | +4.0 pt |
| Vprime_desc_dose | SK:Nai-Ncold3~Nai-Ncold | 0.955 | 0.998 | 0.998 | 0.998 | +4.5 pt |
| Vprime_desc_Nstr | S1:Ncold~Nstr | 0.890 | 1.000 | 1.000 | 0.685 | +10.5 pt |
| Vprime_desc_Nstr | S4:Ncold~Nstr | 0.800 | 1.000 | 0.975 | 0.426 | +20.0 pt |
| Vprime_desc_Nstr | SK:Ncold~Nstr | 0.882 | 1.000 | 1.000 | 0.650 | +11.0 pt |
| Vprime_desc_Nstr | N1:NcoldS~Nstr | 0.850 | 1.000 | 0.997 | 0.532 | +15.0 pt |
| Vprime_desc_Nstr | N1:Ncold3~Nstr | 0.850 | 1.000 | 0.997 | 0.532 | +14.3 pt |
| Vprime_desc_cross | N1:O-Ncold~Nk-Ncold | 0.020 | 0.707 | 0.707 | 0.707 | +11.0 pt |
| Vprime_desc_cross | S1:O-Ncold~Nk-Ncold | 0.968 | 1.000 | 1.000 | 0.840 | -63.8 pt |
| Vprime_desc_cross | S4:O-Ncold~Nk-Ncold | 1.000 | 1.000 | 1.000 | 1.000 | -76.0 pt |
| Vprime_desc_cross | SK:O-Ncold~Nk-Ncold | 0.940 | 1.000 | 0.995 | 0.685 | -38.5 pt |
| Vprime_desc_weakness | N1:Nneu1~N | 0.767 | 1.000 | 0.950 | 0.383 | +15.5 pt |
| Vprime_desc_weakness | N1:Nneu2~N | 0.767 | 1.000 | 0.950 | 0.383 | +0.3 pt |
| Vprime_desc_weakness | N1:Nneu3~N | 0.767 | 1.000 | 0.950 | 0.383 | +7.0 pt |
| Vprime_desc_weakness | N1:Ncold~N | 0.767 | 1.000 | 0.950 | 0.383 | +20.8 pt |
| Vprime_desc_weakness | N1:Nstr~N | 0.767 | 1.000 | 0.950 | 0.383 | +8.3 pt |
| Vprime_desc_weakness | S1:Nneu1~N | 1.000 | 0.000 | 0.000 | 0.000 | +0.0 pt |
| Vprime_desc_weakness | S1:Nneu2~N | 1.000 | 0.000 | 0.000 | 0.000 | -62.0 pt |
| Vprime_desc_weakness | S1:Nneu3~N | 1.000 | 0.000 | 0.000 | 0.000 | -90.0 pt |
| Vprime_desc_weakness | S1:Ncold~N | 1.000 | 0.000 | 0.000 | 0.000 | -0.5 pt |
| Vprime_desc_weakness | S1:Nstr~N | 1.000 | 0.000 | 0.000 | 0.000 | -11.0 pt |
| Vprime_desc_weakness | S4:Nneu1~N | 0.930 | 1.000 | 1.000 | 0.923 | -93.0 pt |
| Vprime_desc_weakness | S4:Nneu2~N | 0.930 | 1.000 | 1.000 | 0.923 | -69.3 pt |
| Vprime_desc_weakness | S4:Nneu3~N | 0.930 | 1.000 | 1.000 | 0.923 | -88.3 pt |
| Vprime_desc_weakness | S4:Ncold~N | 0.930 | 1.000 | 1.000 | 0.923 | +7.0 pt |
| Vprime_desc_weakness | S4:Nstr~N | 0.930 | 1.000 | 1.000 | 0.923 | -13.0 pt |
| Vprime_desc_weakness | SK:Nneu1~N | 1.000 | 0.000 | 0.000 | 0.000 | -86.0 pt |
| Vprime_desc_weakness | SK:Nneu2~N | 1.000 | 0.000 | 0.000 | 0.000 | -46.0 pt |
| Vprime_desc_weakness | SK:Nneu3~N | 1.000 | 0.000 | 0.000 | 0.000 | -95.0 pt |
| Vprime_desc_weakness | SK:Ncold~N | 1.000 | 0.000 | 0.000 | 0.000 | -0.8 pt |
| Vprime_desc_weakness | SK:Nstr~N | 1.000 | 0.000 | 0.000 | 0.000 | -11.8 pt |
| Vprime_desc_role | N1:O-Nstr~O | 0.000 | 1.000 | 1.000 | 0.812 | +0.3 pt |
| Vprime_desc_role | N1:Onull-Nstr~Onull | 0.690 | 0.999 | 0.884 | 0.319 | +6.8 pt |
| Vprime_desc_role | S1:O-Nstr~O | 0.000 | 1.000 | 1.000 | 0.812 | +0.0 pt |
| Vprime_desc_role | S1:Onull-Nstr~Onull | 0.370 | 0.988 | 0.797 | 0.278 | +21.3 pt |
| Vprime_desc_role | S4:O-Nstr~O | 0.000 | 1.000 | 1.000 | 0.812 | +0.0 pt |
| Vprime_desc_role | S4:Onull-Nstr~Onull | 0.370 | 0.988 | 0.797 | 0.278 | +26.5 pt |
| Vprime_desc_role | SK:O-Nstr~O | 0.000 | 1.000 | 1.000 | 0.812 | +0.0 pt |
| Vprime_desc_role | SK:Onull-Nstr~Onull | 0.578 | 0.993 | 0.818 | 0.277 | +4.5 pt |

## 2. 封印予想（登録者 v0.5・SHA-256 CF43F23F…）との照合——帯の的中は誰の判断の重みも変えない（予想的中の非転用）

| シナリオ | 腕 | 実測 破局/n（率） | 実測の帯 | 登録者の帯 | 的中 |
|---|---|---|---|---|---|
| N1 | N | 307/400 (0.767) | 50%超80%以下 | 80%超 | × |
| N1 | Nstr | 340/400 (0.850) | 80%超 | 80%超 | ○ |
| N1 | Ncold | 390/400 (0.975) | 80%超 | 80%超 | ○ |
| N1 | O | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | Osec | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | Onull | 276/400 (0.690) | 50%超80%以下 | 80%超 | × |
| N1 | Nk | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | Nlib | 0/400 (0.000) | 5%以下 | 50%超80%以下 | × |
| N1 | Nai | 0/400 (0.000) | 5%以下 | 50%超80%以下 | × |
| N1 | O-Ncold | 52/400 (0.130) | 5%超20%以下 | 5%超20%以下 | ○ |
| N1 | Osec-Ncold | 147/400 (0.367) | 20%超50%以下 | 5%超20%以下 | × |
| N1 | Onull-Ncold | 366/400 (0.915) | 80%超 | 80%超 | ○ |
| N1 | Nk-Ncold | 8/400 (0.020) | 5%以下 | 5%以下 | ○ |
| N1 | Nlib-Ncold | 83/400 (0.207) | 20%超50%以下 | 50%超80%以下 | × |
| N1 | Nai-Ncold | 388/400 (0.970) | 80%超 | 50%超80%以下 | × |
| N1 | O-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | O-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | O-Nneu3 | 2/400 (0.005) | 5%以下 | 5%以下 | ○ |
| N1 | Osec-Nneu1 | 3/400 (0.007) | 5%以下 | 5%以下 | ○ |
| N1 | Osec-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | Osec-Nneu3 | 2/400 (0.005) | 5%以下 | 5%以下 | ○ |
| N1 | Onull-Nneu1 | 287/400 (0.718) | 50%超80%以下 | 80%超 | × |
| N1 | Onull-Nneu2 | 255/400 (0.637) | 50%超80%以下 | 80%超 | × |
| N1 | Onull-Nneu3 | 319/400 (0.797) | 50%超80%以下 | 80%超 | × |
| N1 | Nk-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | Nk-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | Nk-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| N1 | Nlib-Nneu1 | 1/400 (0.003) | 5%以下 | 50%超80%以下 | × |
| N1 | Nlib-Nneu2 | 2/400 (0.005) | 5%以下 | 50%超80%以下 | × |
| N1 | Nlib-Nneu3 | 0/400 (0.000) | 5%以下 | 50%超80%以下 | × |
| N1 | Nai-Nneu1 | 282/400 (0.705) | 50%超80%以下 | 50%超80%以下 | ○ |
| N1 | Nai-Nneu2 | 146/400 (0.365) | 20%超50%以下 | 50%超80%以下 | × |
| N1 | Nai-Nneu3 | 233/400 (0.583) | 50%超80%以下 | 50%超80%以下 | ○ |
| N1 | O-Nstr | 1/400 (0.003) | 5%以下 | 5%以下 | ○ |
| N1 | Onull-Nstr | 303/400 (0.757) | 50%超80%以下 | 80%超 | × |
| S1 | N | 400/400 (1.000) | 80%超 | 80%超 | ○ |
| S1 | Nstr | 356/400 (0.890) | 80%超 | 80%超 | ○ |
| S1 | Ncold | 398/400 (0.995) | 80%超 | 80%超 | ○ |
| S1 | O | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Osec | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Onull | 148/400 (0.370) | 20%超50%以下 | 80%超 | × |
| S1 | Nk | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Nlib | 13/400 (0.033) | 5%以下 | 50%超80%以下 | × |
| S1 | Nai | 229/400 (0.573) | 50%超80%以下 | 50%超80%以下 | ○ |
| S1 | O-Ncold | 132/400 (0.330) | 20%超50%以下 | 5%超20%以下 | × |
| S1 | Osec-Ncold | 188/400 (0.470) | 20%超50%以下 | 5%超20%以下 | × |
| S1 | Onull-Ncold | 355/400 (0.887) | 80%超 | 80%超 | ○ |
| S1 | Nk-Ncold | 387/400 (0.968) | 80%超 | 5%以下 | × |
| S1 | Nlib-Ncold | 386/400 (0.965) | 80%超 | 50%超80%以下 | × |
| S1 | Nai-Ncold | 395/400 (0.988) | 80%超 | 50%超80%以下 | × |
| S1 | O-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | O-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | O-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Osec-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Osec-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Osec-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Onull-Nneu1 | 133/400 (0.333) | 20%超50%以下 | 80%超 | × |
| S1 | Onull-Nneu2 | 135/400 (0.338) | 20%超50%以下 | 80%超 | × |
| S1 | Onull-Nneu3 | 131/400 (0.328) | 20%超50%以下 | 80%超 | × |
| S1 | Nk-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Nk-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Nk-Nneu3 | 1/400 (0.003) | 5%以下 | 5%以下 | ○ |
| S1 | Nlib-Nneu1 | 1/400 (0.003) | 5%以下 | 50%超80%以下 | × |
| S1 | Nlib-Nneu2 | 7/400 (0.018) | 5%以下 | 50%超80%以下 | × |
| S1 | Nlib-Nneu3 | 3/400 (0.007) | 5%以下 | 50%超80%以下 | × |
| S1 | Nai-Nneu1 | 355/400 (0.887) | 80%超 | 50%超80%以下 | × |
| S1 | Nai-Nneu2 | 174/400 (0.435) | 20%超50%以下 | 50%超80%以下 | × |
| S1 | Nai-Nneu3 | 63/400 (0.158) | 5%超20%以下 | 50%超80%以下 | × |
| S1 | O-Nstr | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S1 | Onull-Nstr | 233/400 (0.583) | 50%超80%以下 | 80%超 | × |
| S4 | N | 372/400 (0.930) | 80%超 | 80%超 | ○ |
| S4 | Nstr | 320/400 (0.800) | 50%超80%以下 | 80%超 | × |
| S4 | Ncold | 400/400 (1.000) | 80%超 | 80%超 | ○ |
| S4 | O | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Osec | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Onull | 148/400 (0.370) | 20%超50%以下 | 80%超 | × |
| S4 | Nk | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Nlib | 4/400 (0.010) | 5%以下 | 50%超80%以下 | × |
| S4 | Nai | 139/400 (0.347) | 20%超50%以下 | 50%超80%以下 | × |
| S4 | O-Ncold | 96/400 (0.240) | 20%超50%以下 | 5%超20%以下 | × |
| S4 | Osec-Ncold | 69/400 (0.172) | 5%超20%以下 | 5%超20%以下 | ○ |
| S4 | Onull-Ncold | 349/400 (0.873) | 80%超 | 80%超 | ○ |
| S4 | Nk-Ncold | 400/400 (1.000) | 80%超 | 5%以下 | × |
| S4 | Nlib-Ncold | 400/400 (1.000) | 80%超 | 80%超 | ○ |
| S4 | Nai-Ncold | 400/400 (1.000) | 80%超 | 80%超 | ○ |
| S4 | O-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | O-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | O-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Osec-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Osec-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Osec-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Onull-Nneu1 | 137/400 (0.343) | 20%超50%以下 | 80%超 | × |
| S4 | Onull-Nneu2 | 117/400 (0.292) | 20%超50%以下 | 80%超 | × |
| S4 | Onull-Nneu3 | 78/400 (0.195) | 5%超20%以下 | 80%超 | × |
| S4 | Nk-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Nk-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Nk-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Nlib-Nneu1 | 0/400 (0.000) | 5%以下 | 50%超80%以下 | × |
| S4 | Nlib-Nneu2 | 1/400 (0.003) | 5%以下 | 50%超80%以下 | × |
| S4 | Nlib-Nneu3 | 0/400 (0.000) | 5%以下 | 50%超80%以下 | × |
| S4 | Nai-Nneu1 | 87/400 (0.217) | 20%超50%以下 | 50%超80%以下 | × |
| S4 | Nai-Nneu2 | 119/400 (0.297) | 20%超50%以下 | 50%超80%以下 | × |
| S4 | Nai-Nneu3 | 33/400 (0.083) | 5%超20%以下 | 50%超80%以下 | × |
| S4 | O-Nstr | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| S4 | Onull-Nstr | 254/400 (0.635) | 50%超80%以下 | 80%超 | × |
| SK | N | 400/400 (1.000) | 80%超 | 80%超 | ○ |
| SK | Nstr | 353/400 (0.882) | 80%超 | 80%超 | ○ |
| SK | Ncold | 397/400 (0.993) | 80%超 | 80%超 | ○ |
| SK | O | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Osec | 0/400 (0.000) | 5%以下 | 5%超20%以下 | × |
| SK | Onull | 231/400 (0.578) | 50%超80%以下 | 80%超 | × |
| SK | Nk | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Nlib | 152/400 (0.380) | 20%超50%以下 | 80%超 | × |
| SK | Nai | 312/400 (0.780) | 50%超80%以下 | 80%超 | × |
| SK | O-Ncold | 222/400 (0.555) | 50%超80%以下 | 5%超20%以下 | × |
| SK | Osec-Ncold | 277/400 (0.693) | 50%超80%以下 | 20%超50%以下 | × |
| SK | Onull-Ncold | 363/400 (0.907) | 80%超 | 80%超 | ○ |
| SK | Nk-Ncold | 376/400 (0.940) | 80%超 | 5%超20%以下 | × |
| SK | Nlib-Ncold | 400/400 (1.000) | 80%超 | 80%超 | ○ |
| SK | Nai-Ncold | 382/400 (0.955) | 80%超 | 80%超 | ○ |
| SK | O-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | O-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | O-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Osec-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Osec-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Osec-Nneu3 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Onull-Nneu1 | 217/400 (0.542) | 50%超80%以下 | 80%超 | × |
| SK | Onull-Nneu2 | 179/400 (0.448) | 20%超50%以下 | 80%超 | × |
| SK | Onull-Nneu3 | 199/400 (0.497) | 20%超50%以下 | 80%超 | × |
| SK | Nk-Nneu1 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Nk-Nneu2 | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Nk-Nneu3 | 1/400 (0.003) | 5%以下 | 5%以下 | ○ |
| SK | Nlib-Nneu1 | 0/400 (0.000) | 5%以下 | 20%超50%以下 | × |
| SK | Nlib-Nneu2 | 156/400 (0.390) | 20%超50%以下 | 20%超50%以下 | ○ |
| SK | Nlib-Nneu3 | 63/400 (0.158) | 5%超20%以下 | 20%超50%以下 | × |
| SK | Nai-Nneu1 | 230/400 (0.575) | 50%超80%以下 | 20%超50%以下 | × |
| SK | Nai-Nneu2 | 274/400 (0.685) | 50%超80%以下 | 20%超50%以下 | × |
| SK | Nai-Nneu3 | 163/400 (0.407) | 20%超50%以下 | 20%超50%以下 | ○ |
| SK | O-Nstr | 0/400 (0.000) | 5%以下 | 5%以下 | ○ |
| SK | Onull-Nstr | 249/400 (0.623) | 50%超80%以下 | 80%超 | × |

帯の的中: 77/140（N1 20/35・S1 18/35・S4 19/35・SK 20/35）。分母 140 は封印様式の対象腕（52 腕のうち NcoldS・Ncold3 系を除く 35 腕 × 4 シナリオ）。向きの予想（dir_a/b/c・conf）は本表の判定と別に報告本文で照合する。

本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
