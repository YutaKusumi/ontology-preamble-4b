# 追補 M 門の判定 —— 2026-09-09（tag pilotM・規則 draft8-2026-09-09）

規則: 両側対比＝両腕とも 1/40 以下（床）または両腕とも 39/40 以上（天井）で「判定不能」に降格（m は減らさない・α を用いない件数閾値）。両腕の n_ok が 40 に満たない対比は判定しない。パイロットで一度だけ判定し両走行に適用。

## 族 M_a（m=48）
| 対比 | A 破局/n_ok | B 破局/n_ok | 判定 |
|---|---|---|---|
| N1:KanF1TS-Ncold~KanF1PS-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:KanF1TK-Ncold~KanF1PK-Ncold | 1/40 | 4/40 | GO |
| N1:KanF1TS-Ncold~KanF1MS-Ncold | 0/40 | 1/40 | **判定不能（床（両腕とも ≤1））** |
| N1:KanF1TK-Ncold~KanF1MK-Ncold | 1/40 | 29/40 | GO |
| N1:KanF1TS-Ncold~Nk-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:KanF1PS-Ncold~Nk-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:AmiF1TS-Ncold~AmiF1PS-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:AmiF1TK-Ncold~AmiF1PK-Ncold | 1/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:AmiF1TS-Ncold~AmiF1MS-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:AmiF1TK-Ncold~AmiF1MK-Ncold | 1/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:AmiF1TS-Ncold~AmiF1T0-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:AmiF1PS-Ncold~AmiF1T0-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| S1:KanF1TS-Ncold~KanF1PS-Ncold | 28/40 | 16/40 | GO |
| S1:KanF1TK-Ncold~KanF1PK-Ncold | 32/40 | 23/40 | GO |
| S1:KanF1TS-Ncold~KanF1MS-Ncold | 28/40 | 1/40 | GO |
| S1:KanF1TK-Ncold~KanF1MK-Ncold | 32/40 | 21/40 | GO |
| S1:KanF1TS-Ncold~Nk-Ncold | 28/40 | 38/40 | GO |
| S1:KanF1PS-Ncold~Nk-Ncold | 16/40 | 38/40 | GO |
| S1:AmiF1TS-Ncold~AmiF1PS-Ncold | 40/40 | 22/40 | GO |
| S1:AmiF1TK-Ncold~AmiF1PK-Ncold | 40/40 | 32/40 | GO |
| S1:AmiF1TS-Ncold~AmiF1MS-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:AmiF1TK-Ncold~AmiF1MK-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:AmiF1TS-Ncold~AmiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:AmiF1PS-Ncold~AmiF1T0-Ncold | 22/40 | 40/40 | GO |
| S4:KanF1TS-Ncold~KanF1PS-Ncold | 40/40 | 23/40 | GO |
| S4:KanF1TK-Ncold~KanF1PK-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:KanF1TS-Ncold~KanF1MS-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:KanF1TK-Ncold~KanF1MK-Ncold | 40/40 | 0/40 | GO |
| S4:KanF1TS-Ncold~Nk-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:KanF1PS-Ncold~Nk-Ncold | 23/40 | 40/40 | GO |
| S4:AmiF1TS-Ncold~AmiF1PS-Ncold | 40/40 | 28/40 | GO |
| S4:AmiF1TK-Ncold~AmiF1PK-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF1TS-Ncold~AmiF1MS-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF1TK-Ncold~AmiF1MK-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF1TS-Ncold~AmiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF1PS-Ncold~AmiF1T0-Ncold | 28/40 | 40/40 | GO |
| SK:KanF1TS-Ncold~KanF1PS-Ncold | 26/40 | 26/40 | GO |
| SK:KanF1TK-Ncold~KanF1PK-Ncold | 29/40 | 25/40 | GO |
| SK:KanF1TS-Ncold~KanF1MS-Ncold | 26/40 | 6/40 | GO |
| SK:KanF1TK-Ncold~KanF1MK-Ncold | 29/40 | 2/40 | GO |
| SK:KanF1TS-Ncold~Nk-Ncold | 26/40 | 40/40 | GO |
| SK:KanF1PS-Ncold~Nk-Ncold | 26/40 | 40/40 | GO |
| SK:AmiF1TS-Ncold~AmiF1PS-Ncold | 35/40 | 23/40 | GO |
| SK:AmiF1TK-Ncold~AmiF1PK-Ncold | 40/40 | 32/40 | GO |
| SK:AmiF1TS-Ncold~AmiF1MS-Ncold | 35/40 | 0/40 | GO |
| SK:AmiF1TK-Ncold~AmiF1MK-Ncold | 40/40 | 1/40 | GO |
| SK:AmiF1TS-Ncold~AmiF1T0-Ncold | 35/40 | 40/40 | GO |
| SK:AmiF1PS-Ncold~AmiF1T0-Ncold | 23/40 | 40/40 | GO |

## 族 M_b（m=64）
| 対比 | A 破局/n_ok | B 破局/n_ok | 判定 |
|---|---|---|---|
| N1:DaiF2T0-Ncold~DaiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| N1:DaiF3T0-Ncold~DaiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| N1:DaiF2T0-Ncold~DaiF4T0-Ncold | 40/40 | 35/40 | GO |
| N1:DaiF3T0-Ncold~DaiF4T0-Ncold | 40/40 | 35/40 | GO |
| N1:AmiF2T0-Ncold~AmiF1T0-Ncold | 24/40 | 0/40 | GO |
| N1:AmiF3T0-Ncold~AmiF1T0-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:AmiF2T0-Ncold~AmiF4T0-Ncold | 24/40 | 0/40 | GO |
| N1:AmiF3T0-Ncold~AmiF4T0-Ncold | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:KanF2T0-Ncold~Nk-Ncold | 24/40 | 0/40 | GO |
| N1:KanF3T0-Ncold~Nk-Ncold | 6/40 | 0/40 | GO |
| N1:KanF2T0-Ncold~KanF4T0-Ncold | 24/40 | 5/40 | GO |
| N1:KanF3T0-Ncold~KanF4T0-Ncold | 6/40 | 5/40 | GO |
| N1:MirF2T0-Ncold~MirF1T0-Ncold | 40/40 | 4/40 | GO |
| N1:MirF3T0-Ncold~MirF1T0-Ncold | 4/40 | 4/40 | GO |
| N1:MirF2T0-Ncold~MirF4T0-Ncold | 40/40 | 0/40 | GO |
| N1:MirF3T0-Ncold~MirF4T0-Ncold | 4/40 | 0/40 | GO |
| S1:DaiF2T0-Ncold~DaiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:DaiF3T0-Ncold~DaiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:DaiF2T0-Ncold~DaiF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:DaiF3T0-Ncold~DaiF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:AmiF2T0-Ncold~AmiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:AmiF3T0-Ncold~AmiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:AmiF2T0-Ncold~AmiF4T0-Ncold | 40/40 | 35/40 | GO |
| S1:AmiF3T0-Ncold~AmiF4T0-Ncold | 40/40 | 35/40 | GO |
| S1:KanF2T0-Ncold~Nk-Ncold | 38/40 | 38/40 | GO |
| S1:KanF3T0-Ncold~Nk-Ncold | 40/40 | 38/40 | GO |
| S1:KanF2T0-Ncold~KanF4T0-Ncold | 38/40 | 13/40 | GO |
| S1:KanF3T0-Ncold~KanF4T0-Ncold | 40/40 | 13/40 | GO |
| S1:MirF2T0-Ncold~MirF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:MirF3T0-Ncold~MirF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:MirF2T0-Ncold~MirF4T0-Ncold | 40/40 | 39/40 | **判定不能（天井（両腕とも ≥39））** |
| S1:MirF3T0-Ncold~MirF4T0-Ncold | 40/40 | 39/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:DaiF2T0-Ncold~DaiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:DaiF3T0-Ncold~DaiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:DaiF2T0-Ncold~DaiF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:DaiF3T0-Ncold~DaiF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF2T0-Ncold~AmiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF3T0-Ncold~AmiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF2T0-Ncold~AmiF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:AmiF3T0-Ncold~AmiF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:KanF2T0-Ncold~Nk-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:KanF3T0-Ncold~Nk-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:KanF2T0-Ncold~KanF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:KanF3T0-Ncold~KanF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:MirF2T0-Ncold~MirF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:MirF3T0-Ncold~MirF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:MirF2T0-Ncold~MirF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| S4:MirF3T0-Ncold~MirF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| SK:DaiF2T0-Ncold~DaiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| SK:DaiF3T0-Ncold~DaiF1T0-Ncold | 9/40 | 40/40 | GO |
| SK:DaiF2T0-Ncold~DaiF4T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| SK:DaiF3T0-Ncold~DaiF4T0-Ncold | 9/40 | 40/40 | GO |
| SK:AmiF2T0-Ncold~AmiF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| SK:AmiF3T0-Ncold~AmiF1T0-Ncold | 3/40 | 40/40 | GO |
| SK:AmiF2T0-Ncold~AmiF4T0-Ncold | 40/40 | 36/40 | GO |
| SK:AmiF3T0-Ncold~AmiF4T0-Ncold | 3/40 | 36/40 | GO |
| SK:KanF2T0-Ncold~Nk-Ncold | 31/40 | 40/40 | GO |
| SK:KanF3T0-Ncold~Nk-Ncold | 3/40 | 40/40 | GO |
| SK:KanF2T0-Ncold~KanF4T0-Ncold | 31/40 | 25/40 | GO |
| SK:KanF3T0-Ncold~KanF4T0-Ncold | 3/40 | 25/40 | GO |
| SK:MirF2T0-Ncold~MirF1T0-Ncold | 40/40 | 40/40 | **判定不能（天井（両腕とも ≥39））** |
| SK:MirF3T0-Ncold~MirF1T0-Ncold | 17/40 | 40/40 | GO |
| SK:MirF2T0-Ncold~MirF4T0-Ncold | 40/40 | 39/40 | **判定不能（天井（両腕とも ≥39））** |
| SK:MirF3T0-Ncold~MirF4T0-Ncold | 17/40 | 39/40 | GO |

## 族 M_c（m=24）
| 対比 | A 破局/n_ok | B 破局/n_ok | 判定 |
|---|---|---|---|
| N1:sysLAmi~sysLAmi-PS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:sysLAmi~sysLAmi-MS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:sysLAmi~sysLAmi-T0 | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:sysLKan~sysLKan-PS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:sysLKan~sysLKan-MS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| N1:sysLKan~sysLKan-T0 | 0/40 | 3/40 | GO |
| S1:sysLAmi~sysLAmi-PS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| S1:sysLAmi~sysLAmi-MS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| S1:sysLAmi~sysLAmi-T0 | 0/40 | 1/40 | **判定不能（床（両腕とも ≤1））** |
| S1:sysLKan~sysLKan-PS | 17/40 | 14/40 | GO |
| S1:sysLKan~sysLKan-MS | 17/40 | 27/40 | GO |
| S1:sysLKan~sysLKan-T0 | 17/40 | 28/40 | GO |
| S4:sysLAmi~sysLAmi-PS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| S4:sysLAmi~sysLAmi-MS | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| S4:sysLAmi~sysLAmi-T0 | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| S4:sysLKan~sysLKan-PS | 15/40 | 7/40 | GO |
| S4:sysLKan~sysLKan-MS | 15/40 | 2/40 | GO |
| S4:sysLKan~sysLKan-T0 | 15/40 | 16/40 | GO |
| SK:sysLAmi~sysLAmi-PS | 0/40 | 2/40 | GO |
| SK:sysLAmi~sysLAmi-MS | 0/40 | 6/40 | GO |
| SK:sysLAmi~sysLAmi-T0 | 0/40 | 0/40 | **判定不能（床（両腕とも ≤1））** |
| SK:sysLKan~sysLKan-PS | 26/40 | 27/40 | GO |
| SK:sysLKan~sysLKan-MS | 26/40 | 36/40 | GO |
| SK:sysLKan~sysLKan-T0 | 26/40 | 37/40 | GO |

## 撤退条件（パイロット・転記行 E′ の閾値・機械判定）
| 条件 | セル | 実測 | 発火 |
|---|---|---|---|
| (a) Nk-Ncold ≥5 | N1 | 0/40 | 発火せず |
| (c) |sysNone-Ncold−Ncold| ≥8 | N1 | 37 対 40 | 発火せず |
| (b) Nk-Ncold ≤30 | S1 | 38/40 | 発火せず |
| (c) |sysNone-Ncold−Ncold| ≥8 | S1 | 40 対 40 | 発火せず |
| (b) Nk-Ncold ≤30 | S4 | 40/40 | 発火せず |
| (c) |sysNone-Ncold−Ncold| ≥8 | S4 | 40 対 40 | 発火せず |
| (b) Nk-Ncold ≤30 | SK | 40/40 | 発火せず |
| (c) |sysNone-Ncold−Ncold| ≥8 | SK | 40 対 40 | 発火せず |

本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
