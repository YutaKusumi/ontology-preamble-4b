# B-lens 層三の設計の事実の数え直し（機械生成・`records/Bl3/recheck_facts_Bl3.py` v3）

- 数え直した記録: `records/Bl3/design-facts-Bl3.json`（SHA16 5D552B2366143FD2・生成 2026-09-24 11:51 UTC）。器 `tools/bl3_facts.py` のコードは使わず、段階 B の試行と生の出力（`results/stageB/`）を読み直した。
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
| q7 の決まりの区間（v̂ の主の行・件数と差と区間・器と別の Wilson と Newcombe） | sub:N1:O-Ncold-v~O-Ncold-vrand 20/200−24/200 -2.00 [-8.26, 4.23]〔零を含む〕・sub:S1:O-Ncold-v~O-Ncold-vrand 98/200−64/200 +17.00 [7.39, 26.18]・sub:SK:O-Ncold-v~O-Ncold-vrand 145/200−109/200 +18.00 [8.58, 26.98]・sub:S4:O-Ncold-v~O-Ncold-vrand 60/200−35/200 +12.50 [4.16, 20.63]・add:N1:Onull+v~Onull+vrand 113/200−135/200 -11.00 [-20.24, -1.49]・add:S1:Onull+v~Onull+vrand 26/200−65/200 -19.50 [-27.35, -11.37]・add:SK:Onull+v~Onull+vrand 78/200−118/200 -20.00 [-29.25, -10.22]・add:S4:Onull+v~Onull+vrand 41/200−74/200 -16.50 [-25.01, -7.65] | sub:N1:O-Ncold-v~O-Ncold-vrand -2.00 [-8.26, 4.23]〔零を含む〕・sub:S1:O-Ncold-v~O-Ncold-vrand +17.00 [7.39, 26.18]・sub:SK:O-Ncold-v~O-Ncold-vrand +18.00 [8.58, 26.98]・sub:S4:O-Ncold-v~O-Ncold-vrand +12.50 [4.16, 20.63]・add:N1:Onull+v~Onull+vrand -11.00 [-20.24, -1.49]・add:S1:Onull+v~Onull+vrand -19.50 [-27.35, -11.37]・add:SK:Onull+v~Onull+vrand -20.00 [-29.25, -10.22]・add:S4:Onull+v~Onull+vrand -16.50 [-25.01, -7.65] | 一致 |
| 様式の転位の閾値（層三の正本と段階 B の正本） | 30 | 30 | 一致 |
| 段階 B の出力の件数と、V3 の形の鍵・主の形の鍵を含む件数 | 11800 件・V3 の形 0・主の形 11800 | 11800 件・V3 の形 0・主の形 11800 | 一致 |
| バッチの大きさ（段階 B の正本）と、主の組ごとのバッチの数と埋める数（正本の値からの算術） | 16・[128, 13] | 16・[128, 13] | 一致 |
| 独立の再計算の順伝播の数（正本の値からの算術） | 32784 | 32784 | 一致 |
| 層三の種と、段階 B と B-lens の種の重なり | 重なり 0・層三の種 3 個・ほかの種 20 個 | 器が確かめた数 20 個 | 一致 |
| 門の行ごとの量が零の (a)（行の数と合計） | 64 行・合計 29 | 64 行・合計 29 | 一致 |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
