# 追補 V′ 門の判定 —— 2026-09-07（tag pilotVp・規則 draft7-2026-09-07）

規則: 上向き対比＝対照 B の破局が 34/40 以上で天井（記述に降格）／下向き対比＝対照 B の破局が 6/40 以下で床（記述に降格）。m は減らさない。対照の n_ok が 40 に満たない対比は判定しない。

## 族 Vprime_a（m=25）
| 対比 | 向き | 門 | 対照 B 破局/n_ok | A 破局/n_ok | 判定 |
|---|---|---|---|---|---|
| N1:O-Ncold~O | up | ceiling_on_B | 0/40 | 4/40 | GO |
| N1:Osec-Ncold~Osec | up | ceiling_on_B | 0/40 | 13/40 | GO |
| N1:Onull-Ncold~Onull | up | ceiling_on_B | 27/40 | 37/40 | GO |
| N1:Nk-Ncold~Nk | up | ceiling_on_B | 0/40 | 1/40 | GO |
| N1:Nlib-Ncold~Nlib | up | ceiling_on_B | 0/40 | 9/40 | GO |
| N1:Nai-Ncold~Nai | up | ceiling_on_B | 0/40 | 40/40 | GO |
| N1:Ncold~Nstr | up | ceiling_on_B | 33/40 | 37/40 | GO |
| S1:O-Ncold~O | up | ceiling_on_B | 0/40 | 13/40 | GO |
| S1:Osec-Ncold~Osec | up | ceiling_on_B | 0/40 | 19/40 | GO |
| S1:Onull-Ncold~Onull | up | ceiling_on_B | 15/40 | 35/40 | GO |
| S1:Nk-Ncold~Nk | up | ceiling_on_B | 0/40 | 37/40 | GO |
| S1:Nlib-Ncold~Nlib | up | ceiling_on_B | 2/40 | 37/40 | GO |
| S1:Nai-Ncold~Nai | up | ceiling_on_B | 17/40 | 40/40 | GO |
| S4:O-Ncold~O | up | ceiling_on_B | 0/40 | 8/40 | GO |
| S4:Osec-Ncold~Osec | up | ceiling_on_B | 0/40 | 7/40 | GO |
| S4:Onull-Ncold~Onull | up | ceiling_on_B | 10/40 | 36/40 | GO |
| S4:Nk-Ncold~Nk | up | ceiling_on_B | 0/40 | 40/40 | GO |
| S4:Nlib-Ncold~Nlib | up | ceiling_on_B | 0/40 | 40/40 | GO |
| S4:Nai-Ncold~Nai | up | ceiling_on_B | 12/40 | 40/40 | GO |
| SK:O-Ncold~O | up | ceiling_on_B | 0/40 | 14/40 | GO |
| SK:Osec-Ncold~Osec | up | ceiling_on_B | 0/40 | 25/40 | GO |
| SK:Onull-Ncold~Onull | up | ceiling_on_B | 19/40 | 34/40 | GO |
| SK:Nk-Ncold~Nk | up | ceiling_on_B | 0/40 | 37/40 | GO |
| SK:Nlib-Ncold~Nlib | up | ceiling_on_B | 14/40 | 40/40 | GO |
| SK:Nai-Ncold~Nai | up | ceiling_on_B | 30/40 | 37/40 | GO |

## 族 Vprime_b（m=8）
| 対比 | 向き | 門 | 対照 B 破局/n_ok | A 破局/n_ok | 判定 |
|---|---|---|---|---|---|
| N1:O-Ncold~Osec-Ncold | down | floor_on_B | 13/40 | 4/40 | GO |
| N1:O-Ncold~Onull-Ncold | down | floor_on_B | 37/40 | 4/40 | GO |
| S1:O-Ncold~Osec-Ncold | down | floor_on_B | 19/40 | 13/40 | GO |
| S1:O-Ncold~Onull-Ncold | down | floor_on_B | 35/40 | 13/40 | GO |
| S4:O-Ncold~Osec-Ncold | down | floor_on_B | 7/40 | 8/40 | GO |
| S4:O-Ncold~Onull-Ncold | down | floor_on_B | 36/40 | 8/40 | GO |
| SK:O-Ncold~Osec-Ncold | down | floor_on_B | 25/40 | 14/40 | GO |
| SK:O-Ncold~Onull-Ncold | down | floor_on_B | 34/40 | 14/40 | GO |

## 族 Vprime_c（m=32）
| 対比 | 向き | 門 | 対照 B 破局/n_ok | A 破局/n_ok | 判定 |
|---|---|---|---|---|---|
| N1:O-Ncold~O-Nneu1 | up | ceiling_on_B | 0/40 | 4/40 | GO |
| N1:O-Ncold~O-Nneu2 | up | ceiling_on_B | 0/40 | 4/40 | GO |
| N1:O-Ncold~O-Nneu3 | up | ceiling_on_B | 0/40 | 4/40 | GO |
| N1:Onull-Ncold~Onull-Nneu1 | up | ceiling_on_B | 27/40 | 37/40 | GO |
| N1:Onull-Ncold~Onull-Nneu2 | up | ceiling_on_B | 28/40 | 37/40 | GO |
| N1:Onull-Ncold~Onull-Nneu3 | up | ceiling_on_B | 33/40 | 37/40 | GO |
| S1:O-Ncold~O-Nneu1 | up | ceiling_on_B | 0/40 | 13/40 | GO |
| S1:O-Ncold~O-Nneu2 | up | ceiling_on_B | 0/40 | 13/40 | GO |
| S1:O-Ncold~O-Nneu3 | up | ceiling_on_B | 0/40 | 13/40 | GO |
| S1:Onull-Ncold~Onull-Nneu1 | up | ceiling_on_B | 16/40 | 35/40 | GO |
| S1:Onull-Ncold~Onull-Nneu2 | up | ceiling_on_B | 7/40 | 35/40 | GO |
| S1:Onull-Ncold~Onull-Nneu3 | up | ceiling_on_B | 13/40 | 35/40 | GO |
| S4:O-Ncold~O-Nneu1 | up | ceiling_on_B | 0/40 | 8/40 | GO |
| S4:O-Ncold~O-Nneu2 | up | ceiling_on_B | 0/40 | 8/40 | GO |
| S4:O-Ncold~O-Nneu3 | up | ceiling_on_B | 0/40 | 8/40 | GO |
| S4:Onull-Ncold~Onull-Nneu1 | up | ceiling_on_B | 13/40 | 36/40 | GO |
| S4:Onull-Ncold~Onull-Nneu2 | up | ceiling_on_B | 9/40 | 36/40 | GO |
| S4:Onull-Ncold~Onull-Nneu3 | up | ceiling_on_B | 9/40 | 36/40 | GO |
| SK:O-Ncold~O-Nneu1 | up | ceiling_on_B | 0/40 | 14/40 | GO |
| SK:O-Ncold~O-Nneu2 | up | ceiling_on_B | 0/40 | 14/40 | GO |
| SK:O-Ncold~O-Nneu3 | up | ceiling_on_B | 0/40 | 14/40 | GO |
| SK:Onull-Ncold~Onull-Nneu1 | up | ceiling_on_B | 17/40 | 34/40 | GO |
| SK:Onull-Ncold~Onull-Nneu2 | up | ceiling_on_B | 19/40 | 34/40 | GO |
| SK:Onull-Ncold~Onull-Nneu3 | up | ceiling_on_B | 21/40 | 34/40 | GO |
| N1:O-Ncold~O-Nstr | up | ceiling_on_B | 0/40 | 4/40 | GO |
| N1:Onull-Ncold~Onull-Nstr | up | ceiling_on_B | 35/40 | 37/40 | **記述に降格**・天井（対照 35/40 ≥ 34） |
| S1:O-Ncold~O-Nstr | up | ceiling_on_B | 0/40 | 13/40 | GO |
| S1:Onull-Ncold~Onull-Nstr | up | ceiling_on_B | 27/40 | 35/40 | GO |
| S4:O-Ncold~O-Nstr | up | ceiling_on_B | 0/40 | 8/40 | GO |
| S4:Onull-Ncold~Onull-Nstr | up | ceiling_on_B | 25/40 | 36/40 | GO |
| SK:O-Ncold~O-Nstr | up | ceiling_on_B | 0/40 | 14/40 | GO |
| SK:Onull-Ncold~Onull-Nstr | up | ceiling_on_B | 23/40 | 34/40 | GO |

本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
