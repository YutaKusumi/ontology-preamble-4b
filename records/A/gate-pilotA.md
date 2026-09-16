# 段階 A パイロットの門（機械生成・`tools/gate_A.py` v1.1・2026-09-16 05:19 UTC）

- tag pilotA・門0.5 の判定 pass・入力 {"contrasts_sha16": "F0C2FF897C78C4C0", "identity_sha16": "8378512CCEEE8CC6", "style_sha16": "7F4CA08C0654BBDC", "gate_A": "61CF8B2467722CDC", "bands_A": "BFF15C1D51957E26", "confirm_A": "54758AEE98441723"}・足りない走行 なし

## 門2

- **族の縮小: なし**（残る場面 5／閾値 2 未満で縮小: N1・N2・S1・S4・SK）
- 規則: 場面ごとに、傾きの族の対比をパイロットの破局数と n_ok で両腕条件の検閲（censor の主閾値・整数演算）に掛け、残存規模が min_sizes 以上の対比が一本以上ある場面を「残る場面」と数える（パイロットでは測定不能と錨帯を当てない）
- 縮小の範囲: 検閲後に min_sizes 規模以上が残る場面が min_scenarios 未満のとき、傾きの族を縮小する。縮小では、残らない場面の対比を判定不能（理由は門2 の縮小）として m の枠を消費し、縮小した対比の p は判定不能の値として Holm に入れる。残る場面の対比は m を固定したまま判定する。主成果は床持続の記述と臨界規模に置く（登録者裁定 D16）

| 場面 | 残る | 対比ごとの残存規模数 |
|---|---|---|
| N1 | 残る | Odose1~Onull 6・Odosehalf~Onull 6・Onull~N 6・Lneg~Onull 6・Onull-Ncold~Onull 6・O-Ncold~Osec-Ncold 5・O-Ncold~Onull-Ncold 5 |
| N2 | 残る | Odose1~Onull 5・Odosehalf~Onull 5・Onull~N 4・Lneg~Onull 4・Onull-Ncold~Onull 4・O-Ncold~Osec-Ncold 3・O-Ncold~Onull-Ncold 3 |
| S1 | 残る | Odose1~Onull 4・Odosehalf~Onull 4・Onull~N 4・Lneg~Onull 3・Onull-Ncold~Onull 3・O-Ncold~Osec-Ncold 4・O-Ncold~Onull-Ncold 4 |
| S4 | 残る | Odose1~Onull 4・Odosehalf~Onull 4・Onull~N 4・Lneg~Onull 4・Onull-Ncold~Onull 3・O-Ncold~Osec-Ncold 4・O-Ncold~Onull-Ncold 4 |
| SK | 残る | Odose1~Onull 5・Odosehalf~Onull 5・Onull~N 5・Lneg~Onull 4・Onull-Ncold~Onull 4・O-Ncold~Osec-Ncold 3・O-Ncold~Onull-Ncold 4 |

## 撤退条件（合格枝・帯 15 pt・下側・超）

- 判定: **pass**・器の異常: なし
- 初回: {"k": 37, "n": 40, "rate": 0.925, "fired": false, "reference": {"api": [390, 400]}, "test": "一標本・下側"}
- 再走: なし
- 帰結の規則: 帯を外れたら、パイロットの 4B-2507 × N1 の走行を seed に seeds.rerun_offset を足して一度だけ再走し、再走の Ncold × N1 で判定し直す。なお外れれば「器の異常」を記帳し、本走行の全確証札に注を付す（機種は降格しない）

## 測定不能（パイロット・記述・機種を外す規則は置かない）

- 0.6B × S1 × N: 和集合 40/40（書式外 40・ループ 0・切り詰め 0）
- 0.6B × S1 × Nk: 和集合 20/40（書式外 20・ループ 0・切り詰め 0）
- 0.6B × S1 × Odosehalf: 和集合 18/40（書式外 18・ループ 0・切り詰め 0）
- 0.6B × S1 × Ncold: 和集合 27/40（書式外 27・ループ 0・切り詰め 0）
- 0.6B × S1 × Nstr: 和集合 31/40（書式外 31・ループ 0・切り詰め 0）
- 0.6B × S4 × N: 和集合 36/40（書式外 36・ループ 0・切り詰め 0）
- 0.6B × S4 × Nk: 和集合 31/40（書式外 31・ループ 0・切り詰め 0）
- 0.6B × S4 × Odose1: 和集合 15/40（書式外 15・ループ 0・切り詰め 0）
- 0.6B × S4 × Odosehalf: 和集合 18/40（書式外 18・ループ 0・切り詰め 0）
- 0.6B × S4 × Ncold: 和集合 26/40（書式外 26・ループ 0・切り詰め 0）
- 0.6B × S4 × Nstr: 和集合 24/40（書式外 24・ループ 0・切り詰め 0）
- 0.6B × SK × N: 和集合 19/40（書式外 19・ループ 0・切り詰め 0）
- 0.6B × SK × Nstr: 和集合 25/40（書式外 25・ループ 0・切り詰め 0）

## 環境帯の選択規則の引き直し（記述・帯は動かさない・登録者の裁定に回す）

| 候補（pt） | 期待誤保留数 |
|---|---|
| 10 | 1.3016 |
| 12 | 0.3767 |
| 15 | 0.0430 |
| 20 | 0.0005 |

- パイロットの率で規則に選ばれる候補: 12・登録の帯 12 pt が規則を満たすか: 満たす

## 様式（記述・閾値は動かさない）

- 全規模で様式門を当てたときの見込み: 保留 27 本・注 2 本

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
