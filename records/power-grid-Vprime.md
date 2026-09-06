# 追補 V′ 検出力格子（機械生成・Fisher 両側・全数列挙・n=400・Holm 初段 α=0.05/m）—— 2026-09-07・contrasts draft4b-2026-09-07

基底は JSON の base_B_main（実測＝本プログラム段I の値・0.000 は 0.000 のまま計算）。null は仮定値を明記。感度列＝基底 ≥0.05 は +15/+10/+5pt・基底 <0.05 は +9/+5/+2pt（下向きは −）。

**要約（本文はこの行を転記する）**: 確証族・実測中間基底の +15pt: 0.866〜0.997／+10pt: 0.375〜0.678。床（実測 <0.05）の +9pt: 0.994〜1.000／+5pt: 0.669〜0.996。確証対比の内訳: 床 16・中間 8・未測定（仮定）33。

| 族 | 対比 | 基底（出所） | 大 | 中 | 小 | α |
|---|---|---|---|---|---|---|
| Vprime_a | N1:O-Ncold~O | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | N1:Osec-Ncold~Osec | 実測 0.003 | 1.000 | 0.939 | 0.187 | 0.00200 |
| Vprime_a | N1:Onull-Ncold~Onull | 実測 0.619 | 0.929 | 0.439 | 0.046 | 0.00200 |
| Vprime_a | N1:Nk-Ncold~Nk | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | N1:Nlib-Ncold~Nlib | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | N1:Nai-Ncold~Nai | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | N1:Ncold~Nstr | 仮定 0.80 | 1.000 | 0.792 | 0.093 | 0.00200 |
| Vprime_a | S1:O-Ncold~O | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | S1:Osec-Ncold~Osec | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | S1:Onull-Ncold~Onull | 実測 0.359 | 0.870 | 0.390 | 0.044 | 0.00200 |
| Vprime_a | S1:Nk-Ncold~Nk | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | S1:Nlib-Ncold~Nlib | 実測 0.016 | 0.994 | 0.669 | 0.055 | 0.00200 |
| Vprime_a | S1:Nai-Ncold~Nai | 実測 0.584 | 0.909 | 0.412 | 0.044 | 0.00200 |
| Vprime_a | S4:O-Ncold~O | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | S4:Osec-Ncold~Osec | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | S4:Onull-Ncold~Onull | 実測 0.406 | 0.866 | 0.375 | 0.041 | 0.00200 |
| Vprime_a | S4:Nk-Ncold~Nk | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | S4:Nlib-Ncold~Nlib | 実測 0.009 | 0.999 | 0.806 | 0.092 | 0.00200 |
| Vprime_a | S4:Nai-Ncold~Nai | 実測 0.359 | 0.870 | 0.390 | 0.044 | 0.00200 |
| Vprime_a | SK:O-Ncold~O | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | SK:Osec-Ncold~Osec | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | SK:Onull-Ncold~Onull | 実測 0.600 | 0.918 | 0.424 | 0.044 | 0.00200 |
| Vprime_a | SK:Nk-Ncold~Nk | 実測 0.000 | 1.000 | 0.996 | 0.282 | 0.00200 |
| Vprime_a | SK:Nlib-Ncold~Nlib | 実測 0.322 | 0.884 | 0.408 | 0.047 | 0.00200 |
| Vprime_a | SK:Nai-Ncold~Nai | 実測 0.762 | 0.997 | 0.678 | 0.073 | 0.00200 |
| Vprime_b | N1:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.960 | 0.565 | 0.089 | 0.00625 |
| Vprime_b | N1:O-Ncold~Onull-Ncold | 仮定 0.80 | 0.976 | 0.679 | 0.130 | 0.00625 |
| Vprime_b | S1:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.960 | 0.565 | 0.089 | 0.00625 |
| Vprime_b | S1:O-Ncold~Onull-Ncold | 仮定 0.50 | 0.933 | 0.515 | 0.083 | 0.00625 |
| Vprime_b | S4:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.960 | 0.565 | 0.089 | 0.00625 |
| Vprime_b | S4:O-Ncold~Onull-Ncold | 仮定 0.55 | 0.929 | 0.515 | 0.083 | 0.00625 |
| Vprime_b | SK:O-Ncold~Osec-Ncold | 仮定 0.40 | 0.960 | 0.565 | 0.089 | 0.00625 |
| Vprime_b | SK:O-Ncold~Onull-Ncold | 仮定 0.75 | 0.960 | 0.611 | 0.110 | 0.00625 |
| Vprime_c | N1:O-Ncold~O-Nneu1 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | N1:O-Ncold~O-Nneu2 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | N1:O-Ncold~O-Nneu3 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | N1:Onull-Ncold~Onull-Nneu1 | 仮定 0.62 | 0.931 | 0.445 | 0.047 | 0.00208 |
| Vprime_c | N1:Onull-Ncold~Onull-Nneu2 | 仮定 0.62 | 0.931 | 0.445 | 0.047 | 0.00208 |
| Vprime_c | N1:Onull-Ncold~Onull-Nneu3 | 仮定 0.62 | 0.931 | 0.445 | 0.047 | 0.00208 |
| Vprime_c | S1:O-Ncold~O-Nneu1 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | S1:O-Ncold~O-Nneu2 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | S1:O-Ncold~O-Nneu3 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | S1:Onull-Ncold~Onull-Nneu1 | 仮定 0.36 | 0.873 | 0.396 | 0.045 | 0.00208 |
| Vprime_c | S1:Onull-Ncold~Onull-Nneu2 | 仮定 0.36 | 0.873 | 0.396 | 0.045 | 0.00208 |
| Vprime_c | S1:Onull-Ncold~Onull-Nneu3 | 仮定 0.36 | 0.873 | 0.396 | 0.045 | 0.00208 |
| Vprime_c | S4:O-Ncold~O-Nneu1 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | S4:O-Ncold~O-Nneu2 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | S4:O-Ncold~O-Nneu3 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | S4:Onull-Ncold~Onull-Nneu1 | 仮定 0.41 | 0.866 | 0.375 | 0.042 | 0.00208 |
| Vprime_c | S4:Onull-Ncold~Onull-Nneu2 | 仮定 0.41 | 0.866 | 0.375 | 0.042 | 0.00208 |
| Vprime_c | S4:Onull-Ncold~Onull-Nneu3 | 仮定 0.41 | 0.866 | 0.375 | 0.042 | 0.00208 |
| Vprime_c | SK:O-Ncold~O-Nneu1 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | SK:O-Ncold~O-Nneu2 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | SK:O-Ncold~O-Nneu3 | 仮定 0.00 | 1.000 | 0.996 | 0.282 | 0.00208 |
| Vprime_c | SK:Onull-Ncold~Onull-Nneu1 | 仮定 0.60 | 0.920 | 0.428 | 0.045 | 0.00208 |
| Vprime_c | SK:Onull-Ncold~Onull-Nneu2 | 仮定 0.60 | 0.920 | 0.428 | 0.045 | 0.00208 |
| Vprime_c | SK:Onull-Ncold~Onull-Nneu3 | 仮定 0.60 | 0.920 | 0.428 | 0.045 | 0.00208 |
| Vprime_desc_neutral | N1:O-Ncold~O-Nneu1 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | N1:O-Ncold~O-Nneu2 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | N1:O-Ncold~O-Nneu3 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | N1:Onull-Ncold~Onull-Nneu1 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | N1:Onull-Ncold~Onull-Nneu2 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | N1:Onull-Ncold~Onull-Nneu3 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | S1:Onull-Ncold~Onull-Nneu1 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | S1:Onull-Ncold~Onull-Nneu2 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | S1:Onull-Ncold~Onull-Nneu3 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | S4:Onull-Ncold~Onull-Nneu1 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | S4:Onull-Ncold~Onull-Nneu2 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | S4:Onull-Ncold~Onull-Nneu3 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | SK:Onull-Ncold~Onull-Nneu1 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | SK:Onull-Ncold~Onull-Nneu2 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_neutral | SK:Onull-Ncold~Onull-Nneu3 | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_dose | N1:O-NcoldS~O-Ncold | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_dose | N1:O-Ncold3~O-Ncold | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_dose | N1:Onull-NcoldS~Onull-Ncold | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_dose | N1:Onull-Ncold3~Onull-Ncold | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_Nstr | S1:Ncold~Nstr | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_Nstr | S4:Ncold~Nstr | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_Nstr | SK:Ncold~Nstr | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_Nstr | N1:NcoldS~Nstr | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_Nstr | N1:Ncold3~Nstr | 仮定 0.40 | 0.988 | 0.794 | 0.272 | 0.05000 |
| Vprime_desc_cross | N1:O-Ncold~Nk-Ncold | 仮定 0.40 | 0.994 | 0.826 | 0.287 | 0.05000 |
| Vprime_desc_cross | S1:O-Ncold~Nk-Ncold | 仮定 0.40 | 0.994 | 0.826 | 0.287 | 0.05000 |
| Vprime_desc_cross | S4:O-Ncold~Nk-Ncold | 仮定 0.40 | 0.994 | 0.826 | 0.287 | 0.05000 |
| Vprime_desc_cross | SK:O-Ncold~Nk-Ncold | 仮定 0.40 | 0.994 | 0.826 | 0.287 | 0.05000 |

本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
