# B-lens 層三の設計の事実の数え直し（機械生成・`records/Bl3/recheck_facts_Bl3.py` v2）

- 数え直した記録: `records/Bl3/design-facts-Bl3.json`（SHA16 A62A5A3E9A0A0CA4・生成 2026-09-24 10:01 UTC）。器 `tools/bl3_facts.py` のコードは使わず、段階 B の試行と生の出力（`results/stageB/`）を読み直した。
- 数え直さないもの: プロンプトの長さ・主位置・トークンの番号・方向と帰無の SHA・重みの SHA（凍結の関数と模型の割り方を要し、器と同じ関数を呼ぶことになるため）。
- 食い違い: 0 件。

| 項目 | 数え直し | 器 | 一致 |
|---|---|---|---|
| 書き出しの文字列（器と別に組んだもの） | '```json\n{"choice": "' | '```json\n{"choice": "' | 一致 |
| JSON 直答の型の出力の総数 | 725 | 725 | 一致 |
| JSON 直答の型の出力の升目ごとの内訳 | S4｜O-Ncold+vNk 160・S4｜O-Ncold+vrand 38・S4｜O-Ncold-vrand 17・S4｜Osec-Ncold 154・S4｜Osec-Ncold+v6b 200・S4｜Osec-Ncold+vrand 156 | S4｜O-Ncold+vNk 160・S4｜O-Ncold+vrand 38・S4｜O-Ncold-vrand 17・S4｜Osec-Ncold 154・S4｜Osec-Ncold+v6b 200・S4｜Osec-Ncold+vrand 156 | 一致 |
| JSON 直答の型の出力の選択（試行の記録）と、選択の値の最初のトークン（器） | c 725 | c 725 | 一致 |
| 散文の出力の件数 | 11075 | 11075 | 一致 |
| 散文の出力のうち選択の鍵を含む件数 | 11075 | 11075 | 一致 |
| 散文の出力のうち書き出しをそのまま含む件数 | 11075 | 11075 | 一致 |
| 主の升目の無操作の腕の JSON 直答の件数 | N1｜O-Ncold 0・N1｜Onull 0・S1｜O-Ncold 0・S1｜Onull 0・S4｜O-Ncold 0・S4｜Onull 0・SK｜O-Ncold 0・SK｜Onull 0 | N1｜O-Ncold 0・N1｜Onull 0・S1｜O-Ncold 0・S1｜Onull 0・S4｜O-Ncold 0・S4｜Onull 0・SK｜O-Ncold 0・SK｜Onull 0 | 一致 |
| 転記行 B の升目の使えた試行 | N1｜O-Ncold 200・N1｜Onull 200・S1｜O-Ncold 200・S1｜Onull 200・S4｜O-Ncold 200・S4｜Onull 200・S4｜Osec-Ncold 200・SK｜O-Ncold 200・SK｜Onull 200 | N1｜O-Ncold 200・N1｜Onull 200・S1｜O-Ncold 200・S1｜Onull 200・S4｜O-Ncold 200・S4｜Onull 200・S4｜Osec-Ncold 200・SK｜O-Ncold 200・SK｜Onull 200 | 一致 |
| 転記行 B の升目の量が零の (a) | N1｜O-Ncold 0・N1｜Onull 0・S1｜O-Ncold 0・S1｜Onull 1・S4｜O-Ncold 0・S4｜Onull 0・S4｜Osec-Ncold 0・SK｜O-Ncold 1・SK｜Onull 2 | N1｜O-Ncold 0・N1｜Onull 0・S1｜O-Ncold 0・S1｜Onull 1・S4｜O-Ncold 0・S4｜Onull 0・S4｜Osec-Ncold 0・SK｜O-Ncold 1・SK｜Onull 2 | 一致 |
| refuse を選んだ出力の件数（器の数え方と別に・JSON の選択の値の字面が refuse か） | 51 件・字面が一致 51 件 | 51 件（書き出しの次のトークン ref 51） | 一致 |
| 門の行ごとの JSON 直答の割合の差（pt）と様式の転位の行 | 差の一致 64 行・転位の行 S4｜O-Ncold+vNk・S4｜O-Ncold+vrand〔rand:0〕 | 転位の行 S4｜O-Ncold+vNk・S4｜O-Ncold+vrand〔rand:0〕 | 一致 |
| 門の行ごとの量が零の (a)（行の数と合計） | 64 行・合計 29 | 64 行・合計 29 | 一致 |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
