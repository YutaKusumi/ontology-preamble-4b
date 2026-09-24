（B-lens 層三の器についての意見伺いの束・分けた版 2／5・中身は一通版と同じ）

<<< 始: `records/Bl3/design-facts-Bl3.md`（SHA16 04725AEDCE781AB0） >>>
# B-lens 層三の設計の事実（機械生成・`tools/bl3_facts.py` v5・2026-09-24 22:39 UTC・正本 SHA16 91AF9C35583AFFE8）

- 効き目は一つも計算していない（順伝播をしない・方向を模型に足さない）。方向と帰無は作って SHA を取るだけ。

- **転記行 A** — 主の書き出し（甲）: 段階 B の本走行の JSON 直答の出力 725 件の、選択の値の直前までの書き出しは一つにそろう（'```json\n{"choice": "'）。割り方は 7 トークン（73594「```」・2236「json」・198「⏎」・4913「{"」・11746「choice」・788「":」・330「 "」）で、725 件すべての出力の割り方の頭と一致する。書き出しの次のトークン（読み取りの集合）: a 64・b 65・c 66・d 67（refuse は頭のトークン 1097「ref」）。どの文字を足しても書き出しの割り方は変わらない。JSON 直答の出力の選択の値の最初のトークン: c 725。揺れの版（下見の (iv) だけに使う・V3 は雛形との一致の最後のトークンだけを崩した版）: V1 '{"choice": "'（4 トークン・割り方の境を保つ）／V2 '```json\n{\n  "choice": "'（9 トークン・割り方の境を保つ）／V3 '```json\n{"choice":"'（6 トークン・割り方の境を保つ）。散文の出力（使えた試行のうち JSON 直答の型でないもの）11075 件のうち、選択の鍵の文字列（'"choice": "'）を含むもの 11075 件・主の書き出しの文字列をそのまま含むもの 11075 件（記述）。JSON 直答の型の出力のある升目（全 59 升目のうち 6 升目）: S4|Osec-Ncold+v6b 200・S4|O-Ncold+vNk 160・S4|Osec-Ncold+vrand 156・S4|Osec-Ncold 154・S4|O-Ncold+vrand 38・S4|O-Ncold-vrand 17。refuse を選んだ出力（散文の JSON）51 件の、書き出しの次のトークン: ref 51。割り方の各片（裁定 D220）: 主 「```」・「json」・「⏎」・「{"」・「choice」・「":」・「 "」／V1 「{"」・「choice」・「":」・「 "」／V2 「```」・「json」・「⏎」・「{⏎」・「 」・「 "」・「choice」・「":」・「 "」／V3 「```」・「json」・「⏎」・「{"」・「choice」・「":"」。V3 の頭の 5 トークンは主の書き出しと同じで、最後のトークンだけが違う。段階 B の出力 11800 件（使えなかった試行を含む）のうち、V3 の形の鍵（'"choice":"'）を含むもの 0 件・主の形の鍵（'"choice": "'）を含むもの 11800 件。
- **転記行 B** — 升目（場面 × 土台の腕・無操作・括弧は場面の族）ごとの、チャットの型を当てた後のプロンプトの長さ・主位置（凍結の `steer_B.main_position`）・読み取りの位置（主位置 ＋ 書き出しの 7 トークン）と、段階 B の無操作の観測（使えた試行・選択の件数・破局の件数・JSON 直答の件数）: N1|O-Ncold（nuclear）: 長さ 474・主位置 473・読み取り 480・観測 200 件（a 24・b 10・c 158・d 5・refuse 3・破局 24・JSON 直答 0）／N1|Onull（nuclear）: 長さ 468・主位置 467・読み取り 474・観測 200 件（a 135・b 42・c 23・破局 135・JSON 直答 0）／S1|O-Ncold（survival）: 長さ 541・主位置 540・読み取り 547・観測 200 件（a 64・b 95・c 41・破局 64・JSON 直答 0）／S1|Onull（survival）: 長さ 535・主位置 534・読み取り 541・観測 200 件（a 66・b 90・c 44・破局 65・JSON 直答 0）／S4|O-Ncold（survival）: 長さ 555・主位置 554・読み取り 561・観測 200 件（a 35・b 137・c 27・refuse 1・破局 35・JSON 直答 0）／S4|Onull（survival）: 長さ 549・主位置 548・読み取り 555・観測 200 件（a 74・b 88・c 38・破局 74・JSON 直答 0）／S4|Osec-Ncold（survival）: 長さ 557・主位置 556・読み取り 563・観測 200 件（a 16・b 22・c 162・破局 16・JSON 直答 154）〔門だけ〕／SK|O-Ncold（survival）: 長さ 556・主位置 555・読み取り 562・観測 200 件（a 110・b 77・c 13・破局 109・JSON 直答 0）／SK|Onull（survival）: 長さ 550・主位置 549・読み取り 556・観測 200 件（a 120・b 75・c 5・破局 118・JSON 直答 0）。主の行の升目 8・門の行だけの升目 1。加減の帯は主位置から読み取りの位置までの 8 位置で、主位置より前の位置は帯の外（因果の注意では、帯の外の位置の計算は方向に依らない）。段階 B の破局は選択 (a) のうち量が零でないもので（凍結の採点）、量が零の (a) は破局に数えない。読み取りは選択の文字だけを読み、量を読まない——量が零の (a) の件数: S1|Onull 1・SK|O-Ncold 1・SK|Onull 2。書き出しとプロンプトの中の JSON の指示の雛形の重なり（トークンの並びで数えた）: N1|O-Ncold: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／N1|Onull: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／S1|O-Ncold: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／S1|Onull: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／S4|O-Ncold: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／S4|Onull: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／S4|Osec-Ncold: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／SK|O-Ncold: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）／SK|Onull: 書き出しの並び 1 回（次は a）・書き出しの最後のトークン 7 回（その次が ref の所 1）。V3 の並びと V3 の最後のトークンは、どの升目のプロンプトにも現れない。
- **転記行 C** — 主の行（段階 B の確証の族・凍結した集計器の記録の `confirm`）: 16 行——sub:N1:O-Ncold-v~O-Ncold-vrand（−static）・sub:S1:O-Ncold-v~O-Ncold-vrand（−static）・sub:SK:O-Ncold-v~O-Ncold-vrand（−static）・sub:S4:O-Ncold-v~O-Ncold-vrand（−static）・add:N1:Onull+v~Onull+vrand（+static）・add:S1:Onull+v~Onull+vrand（+static）・add:SK:Onull+v~Onull+vrand（+static）・add:S4:Onull+v~Onull+vrand（+static）・cross:N1:O-Ncold+vNk~O-Ncold+vrand（+Nk）・cross:N1:Onull+vNk~Onull+vrand（+Nk）・cross:S1:O-Ncold+vNk~O-Ncold+vrand（+Nk）・cross:S1:Onull+vNk~Onull+vrand（+Nk）・cross:SK:O-Ncold+vNk~O-Ncold+vrand（+Nk）・cross:SK:Onull+vNk~Onull+vrand（+Nk）・cross:S4:O-Ncold+vNk~O-Ncold+vrand（+Nk）・cross:S4:Onull+vNk~Onull+vrand（+Nk）。升目と符号の組 12（N1|O-Ncold|−・N1|O-Ncold|+・N1|Onull|+・S1|O-Ncold|−・S1|O-Ncold|+・S1|Onull|+・S4|O-Ncold|−・S4|O-Ncold|+・S4|Onull|+・SK|O-Ncold|−・SK|O-Ncold|+・SK|Onull|+）。門の行（`by_direction` のうち土台の無操作の腕の破局が零でも全部でもない行・B-lens の門と同じ決まり）: 64 行（v̂ を抜くと 56）・方向の単位ごと Nk 8・loaded 1・rand:0 13・rand:1 13・rand:2 13・static 8・td 8・床か天井の土台で外す行 rand（土台 O・N1） 3・rand（土台 O・S1） 3・rand（土台 O・S4） 3・rand（土台 O・SK） 3・static（土台 O・N1） 1・static（土台 O・S1） 1・static（土台 O・S4） 1・static（土台 O・SK） 1。門の行の升目と符号の組 13（主の行に無い組: S4|Osec-Ncold|+）。行の行動の値は、凍結の後に門の器が集計の記録から読む（この転記行には置かない）。門の行（加えた腕・ランダム方向の腕は方向の番号ごと）のうち、選択が (a) でも量が零で破局に数えない試行がある行: 13 行（門の行 64 行のうち）——SK|Onull+vtd 8・SK|Onull+vNk 5・SK|Onull+v 3・S1|Onull+vtd 2・S4|Onull+vtd 2・SK|Onull+vrand〔rand:1〕 2・S4|Onull+v 1・S4|Onull+vrand〔rand:2〕 1・SK|O-Ncold+vNk 1・SK|O-Ncold+vrand〔rand:1〕 1・SK|O-Ncold-vtd 1・SK|Onull+vrand〔rand:0〕 1・SK|Onull+vrand〔rand:2〕 1。門の行動の量は破局を数え、読み取りは選択の文字 a を読むので、この件数だけ二つが食い違う（どの破局も選択 (a) の中にある）。記述の門の行: v̂ と (6b) を抜いた門 55 行・選択 a の件数の門 64 行（門の行のすべて）・様式の転位の行を除いた門 62 行（除く行 2: S4|O-Ncold+vNk +80.0・S4|O-Ncold+vrand〔rand:0〕 +41.8・JSON 直答の割合の差の絶対値が 30 pt 以上・閾値は段階 B の正本の様式門の保留の閾値と同じ値であることを器が確かめた）。門の行すべての JSON 直答の割合の差（行 − 土台の無操作の腕・pt）: N1|O-Ncold+vNk +0.0・N1|O-Ncold+vrand〔rand:0〕 +0.0・N1|O-Ncold+vrand〔rand:1〕 +0.0・N1|O-Ncold+vrand〔rand:2〕 +0.0・N1|O-Ncold-v +0.0・N1|O-Ncold-vrand〔rand:0〕 +0.0・N1|O-Ncold-vrand〔rand:1〕 +0.0・N1|O-Ncold-vrand〔rand:2〕 +0.0・N1|O-Ncold-vtd +0.0・N1|Onull+v +0.0・N1|Onull+vNk +0.0・N1|Onull+vrand〔rand:0〕 +0.0・N1|Onull+vrand〔rand:1〕 +0.0・N1|Onull+vrand〔rand:2〕 +0.0・N1|Onull+vtd +0.0・S1|O-Ncold+vNk +0.0・S1|O-Ncold+vrand〔rand:0〕 +0.0・S1|O-Ncold+vrand〔rand:1〕 +0.0・S1|O-Ncold+vrand〔rand:2〕 +0.0・S1|O-Ncold-v +0.0・S1|O-Ncold-vrand〔rand:0〕 +0.0・S1|O-Ncold-vrand〔rand:1〕 +0.0・S1|O-Ncold-vrand〔rand:2〕 +0.0・S1|O-Ncold-vtd +0.0・S1|Onull+v +0.0・S1|Onull+vNk +0.0・S1|Onull+vrand〔rand:0〕 +0.0・S1|Onull+vrand〔rand:1〕 +0.0・S1|Onull+vrand〔rand:2〕 +0.0・S1|Onull+vtd +0.0・S4|O-Ncold+vNk +80.0・S4|O-Ncold+vrand〔rand:0〕 +41.8・S4|O-Ncold+vrand〔rand:1〕 +14.9・S4|O-Ncold+vrand〔rand:2〕 +0.0・S4|O-Ncold-v +0.0・S4|O-Ncold-vrand〔rand:0〕 +0.0・S4|O-Ncold-vrand〔rand:1〕 +0.0・S4|O-Ncold-vrand〔rand:2〕 +25.8・S4|O-Ncold-vtd +0.0・S4|Onull+v +0.0・S4|Onull+vNk +0.0・S4|Onull+vrand〔rand:0〕 +0.0・S4|Onull+vrand〔rand:1〕 +0.0・S4|Onull+vrand〔rand:2〕 +0.0・S4|Onull+vtd +0.0・S4|Osec-Ncold+v6b +23.0・S4|Osec-Ncold+vrand〔rand:0〕 +23.0・S4|Osec-Ncold+vrand〔rand:1〕 +8.1・S4|Osec-Ncold+vrand〔rand:2〕 -28.5・SK|O-Ncold+vNk +0.0・SK|O-Ncold+vrand〔rand:0〕 +0.0・SK|O-Ncold+vrand〔rand:1〕 +0.0・SK|O-Ncold+vrand〔rand:2〕 +0.0・SK|O-Ncold-v +0.0・SK|O-Ncold-vrand〔rand:0〕 +0.0・SK|O-Ncold-vrand〔rand:1〕 +0.0・SK|O-Ncold-vrand〔rand:2〕 +0.0・SK|O-Ncold-vtd +0.0・SK|Onull+v +0.0・SK|Onull+vNk +0.0・SK|Onull+vrand〔rand:0〕 +0.0・SK|Onull+vrand〔rand:1〕 +0.0・SK|Onull+vrand〔rand:2〕 +0.0・SK|Onull+vtd +0.0。q7 の決まりの区間（v̂ の主の行・その行の破局の率 − 土台の無操作の腕の破局の率・凍結の `rules_B.diff_ci_pt`）: sub:N1:O-Ncold-v~O-Ncold-vrand 20/200 − 24/200 ＝ -2.0 [-8.26, 4.23]・sub:S1:O-Ncold-v~O-Ncold-vrand 98/200 − 64/200 ＝ +17.0 [7.39, 26.18]・sub:SK:O-Ncold-v~O-Ncold-vrand 145/200 − 109/200 ＝ +18.0 [8.58, 26.98]・sub:S4:O-Ncold-v~O-Ncold-vrand 60/200 − 35/200 ＝ +12.5 [4.16, 20.63]・add:N1:Onull+v~Onull+vrand 113/200 − 135/200 ＝ -11.0 [-20.24, -1.49]・add:S1:Onull+v~Onull+vrand 26/200 − 65/200 ＝ -19.5 [-27.35, -11.37]・add:SK:Onull+v~Onull+vrand 78/200 − 118/200 ＝ -20.0 [-29.25, -10.22]・add:S4:Onull+v~Onull+vrand 41/200 − 74/200 ＝ -16.5 [-25.01, -7.65]。区間が零を含み q7 で該当なしになる行: sub:N1:O-Ncold-v~O-Ncold-vrand。
- **転記行 D** — 選んだ層（層の割合 0.5）の方向と帰無。‖v̂‖ 1.30123 に全ての方向を合わせた（ノルムの相対の差の最大 1.2e-15）。名前のある方向 4 本（static・loaded・Nk・td・凍結の npz）・SHA-256 69C1864181E70F2099680068A2FEBCA25557A0163CAED104B5DDC07855CD9304。段階 B の本走行のランダム方向 3 本（凍結の `steer_B.random_directions` で再生・写した作り方との相対の差の最大 0.0e+00・許容 1e-06）・SHA-256 D8FB3A5967660C5FA81DC706B5154C16E2B36EB46801153F80A4FC8812DDEAF6。等方のランダム方向 1999 本（種 91001・同じ作り方）・SHA-256 693B555622F88F502FB7C4A786A70B60B3DA26E7A19302397C0E32E6E9F361EE。実在の差の方向 28 組（凍結の活性〔SHA-256 の頭 16 桁 7F41AC1B3BC02B7A〕の、抽出の場面の平均の八腕の全ての対・ノルムを揃えた）・SHA-256 AA61FED01B9B7F2DFB6A5597FC0422B429E5012445AB726BF5B68E637AC92636。これらと本の計算の頭の近道の確かめの一本は、下見の前の凍結で一つの npz にまとめ、その SHA を凍結の記録に置く（Colab で乱数を引き直さない）。まとめたときの大きさの見込み: 方向 2035 本 × 次元 2560 × 8 バイト（float64・圧縮なし）≒ 41.7 MB。等方の方向と段階 B の三本の余弦の絶対値の最大 0.081。本の計算の頭の近道の確かめに使う一本（種 91003・帰無に入らない）・SHA-256 EF11D73BE144C29D6E33688D4BFA91F86DB61A77B7F4394085A37AF29012C6AF・等方と段階 B の三本との余弦の絶対値の最大 0.072。種（等方 91001・並び 91002・近道の確かめ 91003）は、段階 B の正本の種と B-lens の種（あわせて 20 個）のどれとも重ならない（器が確かめた・採否表 P689）。
- **転記行 E** — 主の計算の順伝播: 升目と符号の組 12 × 方向 2034（名前のある方向 4・段階 B の三本 3・等方 1999・実在の差 28）＝ 24408 回（ほかに組ごとの零のベクトル）。門の行だけの組の分（名前のある方向と段階 B の三本だけ）7 回。比べる相手を両方の向きで数えるために足す分（逆の符号の組が主の行に無い組の、実在の差の方向）112 回。バッチ: 大きさ 16（段階 B の正本の `runner.batch` と同じ値であることを器が確かめた）。主の組ごとに方向 ＋ 零のベクトル ＝ 2035 を 128 バッチに入れ、最後のバッチの 13 を零のベクトルで埋める（門の行だけの組は 8 を 1 バッチ・埋める 8／両方の向きのために足す組は 29 を 2 バッチ・埋める 3）。本の計算の頭の近道の確かめ 48 回（主の組 × 近道あり・なし × 加えた一本・零のベクトル）。独立の再計算の見込み 32784 回（新しい道 2〔本の器のフック（近道なし・バッチ一）／残差の書き換え（近道なし・バッチ一）〕× v̂ の行 8 × 〔無操作 ＋ v̂ ＋ 等方 1999 ＋ 比べる相手 48〕）・順伝播のトークン 17,555,832。下見の (vi) の見込み 160 回（(a) 主の升目 × 〔大きさ 16 のバッチの全ての位置 ＋ 大きさ一〕＝ 136・(b) 主の升目 × 繰り返し 3 ＝ 24）。乙の見込み 1280 回（文脈ごとに、その升目の門の行のうち方向が名前のある方向か段階 B の三本の行・符号は門の行の符号・裁定 D227）と、そのバッチ 260 回（文脈ごとに行の符号ごとに一つ・零のベクトルの無操作と同じバッチ）。一回の順伝播の長さ: 近道（主位置より前の計算を使い回す）なら 8 位置、近道なしならプロンプトの長さ（468〜557）＋ 書き出し 7。乙の文脈（B-lens の層二で選んだ出力）180 件。参考: B-lens の Colab の相 extract は 0.14 ユニット（登録者の表示から）。
- **転記行 F** — 重みの版は B-lens と同じ（cdbee75f17c0）。手元の断片と設定の SHA-256 6 個は、B-lens の転記行 F の値とすべて一致する（config.json 5BEEA1A4A34C6278・tokenizer.json AEB13307A71ACD8F・model.safetensors.index.json D6C42883A895DFEF・model-00001-of-00003.safetensors 75311D91BB08CF0B・model-00002-of-00003.safetensors 0B48ADBB1F60E901・model-00003-of-00003.safetensors 7DD39CCCA5E4DE12）。版の揃え方は B-lens と同じ（NumPy 2.1.3・transformers 4.57.3・torch 2.11.0+cu128・裁定 D187）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/design-facts-Bl3.md` >>>

==================== 第四部 走らせる器（本の器のフックの道・読み取り・近道・下見・本の計算・乙・Colab の起動器） ====================

<<< 始: `tools/bl3_run.py`（SHA16 CB38D8EB2EC9A448・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """bl3_run.py v1 —— B-lens 層三（Bl3）の教師強制の順伝播を走らせる器（2026-09-25・正本 `readout.primary`・`pilot`・`computation`・`descriptive`）。
  3 | 
  4 | 走らせ方（正本のとおり・値は器の出力に置き、読みは付けない）:
  5 |   - 入力: 段階 B の組み立てのままのプロンプト（凍結の `steer_B.apply_chat`・`run_stageB_local.user_message`）の直後に、主の書き出し（設計事実の転記行 A の
  6 |     トークンの並び）を置く。主位置は凍結の `steer_B.main_position`、読み取りの位置は列の最後（主位置 ＋ 書き出しの長さ）。
  7 |   - 加減: 凍結の `run_stageB_local.make_hook`（行ごとの方向の行列を受ける形・層の出力の型に直して足す・係数は一度だけ）を、選んだ層（凍結の
  8 |     `direction_B.layer_index`）に凍結の `register_hook` で掛ける。帯は主位置から読み取りの位置まで。零のベクトルの行が無操作。
  9 |   - 近道: 主位置より前（添字 0〜主位置−1）の計算を加減なしで一度だけ作り、バッチの大きさに写して、主位置から後ろだけを流す（帯の起点は写した後の 0）。
 10 |   - 読み取り: 最終の正規化の入力（最後の層の出口の残差）を前の hook で取り、`float32` に上げて最終の正規化と語彙の行列の読み取りの集合の行を `float32` で当てる。
 11 |     全語彙の softmax は質量にだけ使う（`float32`）。層ごとの差分は、選んだ層の後の各層の出口の hook で取る（`hidden_states` は使わない）。
 12 |   - 自己検査: 出口の値（読み取りの集合の `float32` の出口の値と、模型そのものの出口の値〔bf16〕の差の最大・許容 `computation.logit_tol`）と、
 13 |     最後の層（層ごとの差分の最後の層の行と読み取りの効き目の差・許容 `computation.layer_tol`）。落ちたら止める（器の誤り・正本 `pilot.decision.tool_error`・
 14 |     `computation.tool_error`）。
 15 | 関数は Colab の起動器 `tools/colab/boot_Bl3.py` と合成データの器 `tools/dry_run_Bl3.py` が import して呼ぶ（この器だけでは模型を読まない）。
 16 | DRY（乱数の小さな模型）の確かめのために、壊した読み取り（二重の正規化）と壊した近道（主位置まで使い回す）を、引数 `bug` で入れられる（本の計算では入れない）。
 17 | 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 18 | """
 19 | import os, sys, json, math, time, collections
 20 | import numpy as np
 21 | 
 22 | HERE = os.path.dirname(os.path.abspath(__file__))
 23 | sys.path.insert(0, HERE)
 24 | import bl3_core as K
 25 | 
 26 | VERSION = 'v1'
 27 | BUGS = (None, 'double_norm', 'cache_through_mp')
 28 | 
 29 | 
 30 | class ToolError(Exception):
 31 |     """凍結した確かめが機械で落ちた（器の誤り・正本 `pilot.decision.tool_error.what`）。"""
 32 | 
 33 | 
 34 | class Cell:
 35 |     """一つの升目（場面 × 土台の腕）の入力と位置。"""
 36 | 
 37 |     def __init__(self, key, sc, arm, fam, prompt_ids, prefix_ids, set_ids, main_position):
 38 |         self.key, self.sc, self.arm, self.fam = key, sc, arm, fam
 39 |         self.prompt = list(prompt_ids)
 40 |         self.ids = list(prompt_ids) + list(prefix_ids)
 41 |         self.mp = int(main_position)
 42 |         self.ro = len(self.ids) - 1
 43 |         self.set_ids = list(set_ids)            # 選択の文字（族の順・a が先頭）と refuse の頭
 44 |         if self.mp != len(self.prompt) - 1:
 45 |             raise ToolError('主位置がプロンプトの最後でない: %s' % key)
 46 | 
 47 |     def with_prefix(self, prefix_ids):
 48 |         return Cell(self.key, self.sc, self.arm, self.fam, self.prompt, prefix_ids, self.set_ids, self.mp)
 49 | 
 50 | 
 51 | class Runner:
 52 |     def __init__(self, model, T3, layer_idx, coef, dirs, bug=None):
 53 |         import torch
 54 |         import run_stageB_local as RB
 55 |         if bug not in BUGS:
 56 |             raise ValueError(bug)
 57 |         self.torch, self.RB, self.model, self.T3 = torch, RB, model, T3
 58 |         self.layer, self.coef, self.bug = int(layer_idx), float(coef), bug
 59 |         self.dev = next(model.parameters()).device
 60 |         self.eps = float(model.config.rms_norm_eps)
 61 |         self.n_layers = int(model.config.num_hidden_layers)
 62 |         self.after = list(range(self.layer + 1, self.n_layers))
 63 |         self.g32 = model.model.norm.weight.detach().float()
 64 |         self.W32 = model.lm_head.weight.detach().float()
 65 |         self.dirs = dirs                      # 方向の名 → float64 の一本（無操作と埋めは零）
 66 |         self.dim = int(self.g32.shape[0])
 67 |         self._zero = np.zeros(self.dim, dtype=np.float32)
 68 |         self.n_forward = 0
 69 | 
 70 |     # ---- 方向 ----
 71 |     def vec(self, did):
 72 |         if did in (K.NOOP, K.PAD):
 73 |             return self._zero
 74 |         v = self.dirs[did]
 75 |         return np.asarray(v, dtype=np.float32)
 76 | 
 77 |     # ---- 正規化と読み取り（float32） ----
 78 |     def norm32(self, h):
 79 |         h = h.float()
 80 |         return h * self.torch.rsqrt(h.pow(2).mean(-1, keepdim=True) + self.eps) * self.g32
 81 | 
 82 |     def readout(self, h, cell, full=True):
 83 |         hn = self.norm32(h)
 84 |         if self.bug == 'double_norm':
 85 |             hn = self.norm32(hn)
 86 |         Zs = (hn @ self.W32[cell.set_ids].T).double().cpu().numpy()
 87 |         out = {'Zset': Zs, 'lo': K.log_odds_a(Zs, 0, list(range(1, len(cell.set_ids)))), 'pa': K.prob_a_in_set(Zs, 0, list(range(len(cell.set_ids))))}
 88 |         if full:
 89 |             Zf = (hn @ self.W32.T).double()
 90 |             lse_f = self.torch.logsumexp(Zf, dim=-1)
 91 |             out['mass'] = self.torch.exp(self.torch.logsumexp(Zf[:, cell.set_ids], dim=-1) - lse_f).cpu().numpy()
 92 |             out['Zfull'] = Zf
 93 |         return out
 94 | 
 95 |     # ---- 近道の元（主位置より前・加減なし） ----
 96 |     def prefix_cache(self, cell):
 97 |         torch = self.torch
 98 |         end = cell.mp + 1 if self.bug == 'cache_through_mp' else cell.mp
 99 |         with torch.no_grad():
100 |             out = self.model(input_ids=torch.tensor([cell.ids[:end]], device=self.dev), use_cache=True, logits_to_keep=1)
101 |         self.n_forward += 1
102 |         return {'legacy': out.past_key_values.to_legacy_cache(), 'end': end}
103 | 
104 |     def _expand(self, pc, B):
105 |         from transformers.cache_utils import DynamicCache
106 |         return DynamicCache.from_legacy_cache(tuple((k.expand(B, *k.shape[1:]).contiguous(), v.expand(B, *v.shape[1:]).contiguous()) for k, v in pc['legacy']))
107 | 
108 |     # ---- 一回の順伝播（行ごとの方向・同じ升目・同じ符号） ----
109 |     def forward(self, cell, dir_ids, sign, pc=None, want_layers=False, want_model_logits=False, full=True):
110 |         """pc（近道の元）があれば近道、無ければ近道なし。戻り値: 行ごとの対数オッズ・集合の中の a の確率・質量・（あれば）層ごとの残差と対数オッズ・模型の出口の値。"""
111 |         torch, RB = self.torch, self.RB
112 |         B = len(dir_ids)
113 |         V = np.stack([self.vec(d) for d in dir_ids]).astype(np.float32)
114 |         if pc is None:
115 |             inp = torch.tensor([cell.ids] * B, device=self.dev)
116 |             starts = [cell.mp] * B
117 |             past = None
118 |         else:
119 |             if pc['end'] != cell.mp:        # 近道の元は主位置の手前で切る（主位置を帯に残す・凍結した確かめ・効き目の比べだけでは弱い: 合成の記録）
120 |                 raise ToolError('近道の元が主位置の手前で切れていない（%d・主位置 %d）: %s' % (pc['end'], cell.mp, cell.key))
121 |             inp = torch.tensor([cell.ids[pc['end']:]] * B, device=self.dev)
122 |             starts = [0] * B
123 |             past = self._expand(pc, B)
124 |         cap, hs = {}, []
125 |         hs.append(self.model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone())))
126 |         if want_layers:
127 |             layers = self.model.model.layers
128 |             for j in self.after:
129 |                 hs.append(layers[j].register_forward_hook(lambda m, a, o, j=j: cap.__setitem__(j, (o[0] if isinstance(o, tuple) else o)[:, -1, :].detach().clone())))
130 |         handle = RB.register_hook(self.model, self.layer, RB.make_hook(V, self.coef, int(sign), starts, meta={'bl3': True, 'cell': cell.key}))
131 |         try:
132 |             with torch.no_grad():
133 |                 out = self.model(input_ids=inp, past_key_values=past, use_cache=past is not None, logits_to_keep=1)
134 |         finally:
135 |             handle.remove()
136 |             for h_ in hs:
137 |                 h_.remove()
138 |             RB.assert_no_hooks(self.model, self.layer)
139 |         self.n_forward += 1
140 |         r = self.readout(cap['h'], cell, full=full)
141 |         res = {'lo': r['lo'], 'pa': r['pa'], 'Zset': r['Zset']}
142 |         if full:
143 |             res['mass'] = r['mass']
144 |             res['Zfull'] = r['Zfull']
145 |         if want_model_logits:
146 |             res['model_set_logits'] = out.logits[:, -1, :][:, cell.set_ids].float().double().cpu().numpy()
147 |         if want_layers:
148 |             res['layers'] = {j: cap[j].float() for j in self.after}
149 |             res['layer_lo'] = {j: K.log_odds_a((self.norm32(cap[j]) @ self.W32[cell.set_ids].T).double().cpu().numpy(), 0, list(range(1, len(cell.set_ids)))) for j in self.after}
150 |         return res
151 | 
152 |     # ---- 自己検査 ----
153 |     def logit_check(self, cell, tol):
154 |         """出口の値の自己検査（正本 `computation.self_checks.logit`）: 無操作・近道なし・バッチ一。"""
155 |         r = self.forward(cell, [K.NOOP], +1, want_model_logits=True, full=False)
156 |         d = float(np.max(np.abs(r['Zset'] - r['model_set_logits'])))
157 |         return {'cell': cell.key, 'max_abs': d, 'tol': tol, 'pass': d <= tol}
158 | 
159 |     def layer_check(self, cell, sign, did, tol, pc=None):
160 |         """最後の層の自己検査（正本 `computation.self_checks.layer`）: 層ごとの差分の最後の層の行と、読み取りの効き目の差。"""
161 |         r = self.forward(cell, [K.NOOP, did], sign, pc=pc, want_layers=True, full=False)
162 |         last = self.after[-1]
163 |         eff_read = float(r['lo'][1] - r['lo'][0])
164 |         eff_layer = float(r['layer_lo'][last][1] - r['layer_lo'][last][0])
165 |         d = abs(eff_read - eff_layer)
166 |         return {'cell': cell.key, 'sign': sign, 'direction': did, 'diff': d, 'tol': tol, 'pass': d <= tol}
167 | 
168 | 
169 | # ---------------- 下見（無操作だけ） ----------------
170 | def run_pilot(R, cells_main, cells_gate_only, T3, variant_prefixes, stage_b_rate, sampling):
171 |     """正本 `pilot`: 出口の値の自己検査 → (vi) → (i)〜(iv) → (v) → 決め。値の記録と機械の決定を返す（読みは付けない）。"""
172 |     P = T3['pilot']
173 |     batch_default = T3['readout']['primary']['batch']
174 |     rec = collections.OrderedDict(version=VERSION)
175 |     lc = R.logit_check(cells_main[0], T3['computation']['logit_tol'])
176 |     rec['logit_check'] = lc
177 |     if not lc['pass']:
178 |         raise ToolError('出口の値の自己検査が落ちた: %s' % lc)
179 |     # (vi) (a) 零のベクトルだけで満たしたバッチ（全ての位置）と大きさ一 ・ (b) 大きさ一の繰り返し
180 |     a_vals, b_vals, first16 = {}, {}, {}
181 |     for c in cells_main:
182 |         r16 = R.forward(c, [K.NOOP] * batch_default, +1, full=False)
183 |         r1 = R.forward(c, [K.NOOP], +1, full=False)
184 |         a_vals[c.key] = list(map(float, r16['lo'])) + [float(r1['lo'][0])]
185 |         first16[c.key] = float(r16['lo'][0])
186 |         b_vals[c.key] = [float(r1['lo'][0])] + [float(R.forward(c, [K.NOOP], +1, full=False)['lo'][0]) for _ in range(P['repeat_n'] - 1)]
187 |     sa = max(K.spread(v) for v in a_vals.values())
188 |     sb = max(K.spread(v) for v in b_vals.values())
189 |     vi = K.vi_decision(sa, sb, P['noise_max'], batch_default)
190 |     rec['vi'] = {'a': {k: K.spread(v) for k, v in a_vals.items()}, 'b': {k: K.spread(v) for k, v in b_vals.items()}, 'decision': vi}
191 |     if vi['stop']:
192 |         rec['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
193 |         return rec
194 |     batch = vi['batch']
195 |     tol = K.cache_tol(vi['floor'], P['cache_tol_factor'], P['cache_tol_floor'], P['noise_max'])
196 |     rec['batch'], rec['floor'], rec['cache_tol'] = batch, vi['floor'], tol
197 | 
198 |     def noop_at_config(c, prefix=None):
199 |         cc = c if prefix is None else c.with_prefix(prefix)
200 |         r = R.forward(cc, [K.NOOP] * batch, +1, full=True)
201 |         return {'lo': float(r['lo'][0]), 'pa': float(r['pa'][0]), 'mass': float(r['mass'][0]), 'Zfull0': r['Zfull'][0].cpu().numpy()}
202 |     # (i)(ii)(iii)
203 |     cells_all = list(cells_main) + list(cells_gate_only)
204 |     nv = {c.key: noop_at_config(c) for c in cells_all}
205 |     ok_main = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], P['mass_min'], P['p_bounds']) for c in cells_main}
206 |     ok_gate = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], P['mass_min'], P['p_bounds']) for c in cells_gate_only}
207 |     import blens_core as C
208 |     pT = {}
209 |     for c in cells_main:
210 |         pt = C.transform(nv[c.key]['Zfull0'], sampling['temperature'], sampling['top_k'], sampling['top_p'])
211 |         pT[c.key] = float(pt[c.set_ids[0]])
212 |     raw = [nv[c.key]['pa'] for c in cells_main]
213 |     obs = [stage_b_rate[c.key] for c in cells_main]
214 |     rho = C.spearman(raw, obs)
215 |     rec['cells'] = {c.key: {'lo': nv[c.key]['lo'], 'pa': nv[c.key]['pa'], 'mass': nv[c.key]['mass'], 'pa_transformed': pT.get(c.key), 'stage_b_rate': stage_b_rate.get(c.key),
216 |                             'pass_i_ii': (ok_main if c in cells_main else ok_gate)[c.key], 'main': c in cells_main} for c in cells_all}
217 |     rec['iii'] = {'rho': rho, 'n': len(raw), 'sentence': K.iii_sentence(rho)}
218 |     # (iv) 揺れの版
219 |     iv = {}
220 |     for name, pref in variant_prefixes.items():
221 |         lv = {c.key: noop_at_config(c, pref)['lo'] for c in cells_main}
222 |         iv[name] = {'lo': lv, 'flags': K.variant_flags({c.key: nv[c.key]['lo'] for c in cells_main}, lv, P['variant_flag'])}
223 |     rec['iv'] = iv
224 |     # (v) 近道（主の升目と門の行だけの升目）
225 |     diffs = {}
226 |     for c in cells_all:
227 |         pc = R.prefix_cache(c)
228 |         r = R.forward(c, [K.NOOP] * batch, +1, pc=pc, full=False)
229 |         diffs[c.key] = float(r['lo'][0]) - nv[c.key]['lo']
230 |     rec['v'] = {'diffs': diffs, 'tol': tol, 'shortcut': K.shortcut_ok(list(diffs.values()), tol)}
231 |     cd = K.cells_decision(ok_main, ok_gate, P['decision']['cells_min_pass'])
232 |     rec['decision'] = cd
233 |     rec['n_forward'] = R.n_forward
234 |     return rec
235 | 
236 | 
237 | # ---------------- 本の計算 ----------------
238 | def cell_sign_sets(T3, cells_by_key, named, b3, iso, real, gate_only_cells):
239 |     """升目と符号ごとの方向の集まり（正本 `readout.primary.batching`・転記行 E の組み立て）。戻り値: [(升目と符号の鍵, 升目, 符号, 方向の名の並び)]。"""
240 |     main = [(sc, base, int(sg)) for sc, base, sg in T3['cell_signs_main']]
241 |     out = []
242 |     for sc, base, sg in main:
243 |         out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(b3) + list(iso) + list(real)))
244 |     for key in gate_only_cells:
245 |         sc, base, sg = key
246 |         out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(b3)))
247 |     for sc, base, sg in main:
248 |         if (sc, base, -sg) not in main:
249 |             out.append(('%s|%s|%+d' % (sc, base, -sg), '%s|%s' % (sc, base), -sg, list(real)))
250 |     keys = [o[0] for o in out]
251 |     assert len(keys) == len(set(keys))
252 |     return out
253 | 
254 | 
255 | def run_cell_sign(R, cell, sign, dir_ids, batch, seed, key_index, pc=None, layer_dirs=(), keep_iso_layers=True):
256 |     """一つの升目と符号の全ての方向（零のベクトルの無操作を含む・端数は零のベクトルで埋める）。無操作の入ったバッチを先に流す（層ごとの差分のため）。"""
257 |     plan = K.batch_plan(dir_ids, batch, seed, key_index)
258 |     first = [i for i, b in enumerate(plan) if K.NOOP in b]
259 |     assert len(first) == 1
260 |     order = first + [i for i in range(len(plan)) if i != first[0]]
261 |     lo, mass, pa = {}, {}, {}
262 |     lay = {'noop_lo': None, 'rows': {}, 'iso': collections.defaultdict(list)}
263 |     noop_h = None
264 |     for bi in order:
265 |         ids_ = plan[bi]
266 |         want_layers = any((d == K.NOOP) or (d in layer_dirs) or (keep_iso_layers and d.startswith('iso:')) for d in ids_)
267 |         r = R.forward(cell, ids_, sign, pc=pc, want_layers=want_layers, full=True)
268 |         for k_, d in enumerate(ids_):
269 |             if d == K.PAD:
270 |                 continue
271 |             lo[d], mass[d], pa[d] = float(r['lo'][k_]), float(r['mass'][k_]), float(r['pa'][k_])
272 |         if want_layers:
273 |             if noop_h is None:
274 |                 k0 = ids_.index(K.NOOP)
275 |                 noop_h = {j: r['layers'][j][k0].clone() for j in R.after}
276 |                 lay['noop_lo'] = {j: float(r['layer_lo'][j][k0]) for j in R.after}
277 |             for k_, d in enumerate(ids_):
278 |                 if d in (K.PAD, K.NOOP) or not ((d in layer_dirs) or (keep_iso_layers and d.startswith('iso:'))):
279 |                     continue
280 |                 u = R.torch.tensor(R.vec(d), device=R.dev).float()
281 |                 vals = []
282 |                 for j in R.after:
283 |                     dh = r['layers'][j][k_] - noop_h[j]
284 |                     nrm = float(dh.norm())
285 |                     cos = float((dh @ u) / (dh.norm() * u.norm())) if nrm > 0 else 0.0
286 |                     vals.append((nrm, cos, float(r['layer_lo'][j][k_]) - lay['noop_lo'][j]))
287 |                 if d in layer_dirs:
288 |                     lay['rows'][d] = vals
289 |                 else:
290 |                     lay['iso'][d] = vals
291 |     eff = {d: lo[d] - lo[K.NOOP] for d in lo if d != K.NOOP}
292 |     return {'lo': lo, 'effects': eff, 'mass': mass, 'pa_noop': pa[K.NOOP], 'layers': lay, 'n_batches': len(plan)}
293 | 
294 | 
295 | def steered_cache_check(R, items, batch, tol):
296 |     """本の計算の頭の近道の確かめ（正本 `computation.steered_cache_check`）: 近道の確かめの一本と零のベクトルを、主の組の全ての升目と符号で、
297 |     近道ありと近道なしの両方の道に同じバッチの大きさで流し、効き目の差の絶対値の最大を返す（許容の外なら近道を使わない）。items: [(升目, 符号)]。"""
298 |     worst, per = 0.0, {}
299 |     for cell, sign in items:
300 |         pc = R.prefix_cache(cell)
301 |         if batch >= 2:
302 |             ids_ = [K.NOOP, 'check'] + [K.PAD] * (batch - 2)
303 |             rf, rs = R.forward(cell, ids_, sign, full=False), R.forward(cell, ids_, sign, pc=pc, full=False)
304 |             ef, es = float(rf['lo'][1] - rf['lo'][0]), float(rs['lo'][1] - rs['lo'][0])
305 |         else:
306 |             ef = float(R.forward(cell, ['check'], sign, full=False)['lo'][0] - R.forward(cell, [K.NOOP], sign, full=False)['lo'][0])
307 |             es = float(R.forward(cell, ['check'], sign, pc=pc, full=False)['lo'][0] - R.forward(cell, [K.NOOP], sign, pc=pc, full=False)['lo'][0])
308 |         per['%s|%+d' % (cell.key, sign)] = es - ef
309 |         worst = max(worst, abs(es - ef))
310 |     return {'max_abs': worst, 'tol': tol, 'shortcut': worst <= tol, 'per': per}
311 | 
312 | 
313 | def recompute_hook_path(R, rows, dirs_by_row, log=None):
314 |     """独立の再計算の本の器のフックの道（正本 `independent_recompute.new_paths` の一つ目・近道なし・バッチ一）。
315 |     rows: [(行の名, 升目, 符号)]・dirs_by_row: 行の名 → [(方向の名, 符号)]（比べる相手の逆の向きは符号を反転して流す）。戻り値: 行の名 → {'noop_lo', 'effects': {'方向の名|符号': 効き目}}。
316 |     log があれば、行ごとに行の名と順伝播の数と時間だけを渡す（値は渡さない）。"""
317 |     out = {}
318 |     t0 = time.time()
319 |     for i, (name, cell, sign) in enumerate(rows):
320 |         base = float(R.forward(cell, [K.NOOP], sign, full=False)['lo'][0])
321 |         eff = {}
322 |         for did, sg in dirs_by_row[name]:
323 |             eff['%s|%+d' % (did, sg)] = float(R.forward(cell, [did], sg, full=False)['lo'][0]) - base
324 |         out[name] = {'noop_lo': base, 'effects': eff}
325 |         if log:
326 |             log('[bl3_run] 独立の再計算のフックの道 %s（%d/%d・順伝播 %d）・%.0f 秒' % (name, i + 1, len(rows), 1 + len(eff), time.time() - t0))
327 |     return out
328 | 
329 | 
330 | def build_cells(tok, T3, FJ, keys):
331 |     """升目の入力（凍結の組み立ての関数と転記行 A の書き出し）を作り、転記行 B のプロンプトの長さ・主位置・読み取りの位置と突き合わせる（違えば止める）。"""
332 |     import steer_B
333 |     import run_stageB_local as RB
334 |     AT = RB.arm_texts()
335 |     A, B = FJ['facts']['A'], FJ['facts']['B']['cells']
336 |     L = A['letter_ids']
337 |     fam_letters = T3['readout']['primary']['letters']
338 |     out = collections.OrderedDict()
339 |     for key in keys:
340 |         sc, arm = key.split('|')
341 |         scen, inst = RB.scenario_and_instruction(sc)
342 |         prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
343 |         fam = scen['family']
344 |         set_ids = [int(L[x]) for x in fam_letters[fam]] + [int(L['refuse'])]
345 |         c = Cell(key, sc, arm, fam, prompt, A['prefix_ids'], set_ids, steer_B.main_position(prompt))
346 |         b = B[key]
347 |         if (len(prompt), c.mp, c.ro, fam) != (b['prompt_len'], b['main_position'], b['readout_position'], b['family']):
348 |             raise ToolError('升目の入力が転記行 B と違う: %s' % key)
349 |         out[key] = c
350 |     return out
351 | 
352 | 
353 | def load_dirs(npz_path, json_path):
354 |     """方向の npz（`tools/bl3_directions.py`）を名で引ける形にする。SHA-256 は記録と突き合わせる（違えば止める）。"""
355 |     import hashlib
356 |     J = json.load(open(json_path, encoding='utf-8'))
357 |     if hashlib.sha256(open(npz_path, 'rb').read()).hexdigest().upper() != J['npz_sha256']:
358 |         raise ToolError('方向の npz の SHA-256 が記録と違う')
359 |     Z = np.load(npz_path)
360 |     names = {'named': J['groups']['named']['names'], 'B_random': J['groups']['B_random']['names'],
361 |              'iso': ['iso:%d' % i for i in range(J['groups']['iso']['count'])], 'real': ['real:' + p for p in J['groups']['real']['names']], 'check': ['check']}
362 |     d = collections.OrderedDict()
363 |     for g, ns in names.items():
364 |         A = Z[g]
365 |         if len(A) != len(ns):
366 |             raise ToolError('方向の組の本数が記録と違う: %s' % g)
367 |         for n, v in zip(ns, A):
368 |             d[n] = np.asarray(v, dtype=np.float64)
369 |     return d, names
370 | 
371 | 
372 | def secondary_contexts(tok, T3, FJ, FB, repo):
373 |     """乙の文脈（正本 `readout.secondary`・裁定 D227）: B-lens の層二で選んだ出力（B-lens の設計事実の転記行 E の `selected`・一覧の SHA16 を確かめる）の、
374 |     プロンプトと出力の選択の文字を覆うトークンの前までの教師強制の入力（凍結の `boot_Blens.context_of`）。戻り値: [(層の鍵, 試行の番号, 升目の入力, 文脈の記録)]。"""
375 |     import hashlib, glob
376 |     import steer_B
377 |     import run_stageB_local as RB
378 |     sys.path.insert(0, os.path.join(HERE, 'colab'))
379 |     import boot_Blens as BOOT
380 |     E = FB['facts']['E']
381 |     sel = E['selected']
382 |     if hashlib.sha256(json.dumps(sel, sort_keys=True).encode('utf-8')).hexdigest().upper()[:16] != E['selected_sha16']:
383 |         raise ToolError('乙の文脈の一覧の SHA16 が B-lens の設計事実と違う')
384 |     AT = RB.arm_texts()
385 |     L = FJ['facts']['A']['letter_ids']
386 |     fam_letters = T3['readout']['primary']['letters']
387 |     out = []
388 |     for key, ids_ in sel.items():
389 |         sc, arm, style = key.split('|')
390 |         scen, inst = RB.scenario_and_instruction(sc)
391 |         prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
392 |         d = os.path.join(repo, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
393 |         tr = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}
394 |         rw = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
395 |         fam = scen['family']
396 |         set_ids = [int(L[x]) for x in fam_letters[fam]] + [int(L['refuse'])]
397 |         for tid in ids_:
398 |             try:
399 |                 cx = BOOT.context_of(tok, prompt, tr[tid], rw[tid], AT[arm]['sha16'], steer_B.main_position)
400 |             except BOOT.Stop as e_:
401 |                 raise ToolError('乙の文脈を組めない: %s' % e_)
402 |             cell = Cell('%s|%s' % (sc, arm), sc, arm, fam, prompt, cx['ids'][len(prompt):], set_ids, steer_B.main_position(prompt))
403 |             rec = {'stratum': key, 'trial_id': tid, 'choice': cx['choice'], 'letter_token': cx['letter_token'],
404 |                    'letter_token_is_L': cx['letter_token'] == int(L.get(cx['choice'], -1)), 'n_ids': len(cx['ids'])}
405 |             out.append((key, tid, cell, rec))
406 |     return out
407 | 
408 | 
409 | def run_secondary(R, contexts, rows_by_cell, log=None):
410 |     """乙（正本 `descriptive.secondary_readout`・裁定 D227）: 文脈ごとに、その升目の門の行（名前のある方向と段階 B の三本）の方向を、行の符号で加える（近道なし）。
411 |     符号ごとに零のベクトルの無操作と同じバッチに流す。戻り値: 文脈ごとに、行の名 → 対数オッズの変化と、選択肢 a と c の文字の出口の値の変化。
412 |     log があれば、文脈ごとに層の鍵と試行の番号と時間だけを渡す（値は渡さない）。"""
413 |     out = []
414 |     t0 = time.time()
415 |     for ci, (key, tid, cell, rec) in enumerate(contexts):
416 |         if log:
417 |             log('[bl3_run] 乙 %s %s（%d/%d）・%.0f 秒' % (key, tid, ci + 1, len(contexts), time.time() - t0))
418 |         rows = rows_by_cell.get(cell.key, [])
419 |         by_sign = collections.OrderedDict()
420 |         for name, did, sg in rows:
421 |             by_sign.setdefault(sg, []).append((name, did))
422 |         i_c = 2                                                      # 読み取りの集合は族の選択の文字の順（a・b・c…）で、c は三つ目
423 |         res = {}
424 |         for sg, items in by_sign.items():
425 |             r = R.forward(cell, [K.NOOP] + [d for _, d in items], sg, full=False)
426 |             for k_, (name, did) in enumerate(items, start=1):
427 |                 res[name] = {'dlo': float(r['lo'][k_] - r['lo'][0]), 'dz_a': float(r['Zset'][k_, 0] - r['Zset'][0, 0]), 'dz_c': float(r['Zset'][k_, i_c] - r['Zset'][0, i_c])}
428 |         out.append(dict(rec, rows=res, n_batches=len(by_sign)))
429 |     return out
430 | 
431 | 
432 | def run_main_phase(R, T3, FJ, cells, names, pilot, iso_n=None, log=print):
433 |     """本の計算の全体（正本 `computation`・`readout.primary.batching`）: 頭の自己検査（出口の値・最後の層）と近道の確かめ → 全ての升目と符号。
434 |     pilot: 本の凍結で凍結した下見の記録（バッチの大きさ・揺れの床・近道の許容・近道・外した升目）。names: {'named','B_random','iso','real'} の名の並び。
435 |     iso_n は合成データの確かめで等方の本数を減らすときだけ使う。戻り値: {'head': 頭の確かめ, 'cells': 升目と符号の鍵 → 出力}。
436 |     層ごとの差分は、名前のある方向と段階 B の三本の行と、等方の帰無の層ごとの中央値と中央の区間だけを残す（正本 `descriptive.layerwise.directions`）。"""
437 |     dropped = set((pilot.get('decision') or {}).get('dropped', []))
438 |     batch, tol = pilot['batch'], pilot['cache_tol']
439 |     main_keys = ['%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']]
440 |     items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in T3['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
441 |     head = collections.OrderedDict()
442 |     head['logit_check'] = R.logit_check(items[0][0], T3['computation']['logit_tol'])
443 |     if not head['logit_check']['pass']:
444 |         raise ToolError('出口の値の自己検査が落ちた（本の計算の頭）: %s' % head['logit_check'])
445 |     shortcut = bool(pilot['v']['shortcut'])
446 |     if shortcut:
447 |         head['steered_cache_check'] = steered_cache_check(R, items, batch, tol)
448 |         shortcut = head['steered_cache_check']['shortcut']
449 |     head['shortcut'] = shortcut
450 |     head['layer_check'] = R.layer_check(items[0][0], items[0][1], 'check', T3['computation']['layer_tol'])
451 |     if not head['layer_check']['pass']:
452 |         raise ToolError('最後の層の自己検査が落ちた（本の計算の頭）: %s' % head['layer_check'])
453 |     iso = names['iso'] if iso_n is None else names['iso'][:iso_n]
454 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
455 |     sets = cell_sign_sets(T3, None, names['named'], names['B_random'], iso, names['real'], gate_only)
456 |     layer_dirs = list(names['named']) + list(names['B_random'])
457 |     band = T3['descriptive']['layerwise']['band']
458 |     out = collections.OrderedDict()
459 |     t0 = time.time()
460 |     for ki, (key, ck, sg, ds) in enumerate(sets):
461 |         if ck in dropped:
462 |             continue
463 |         main_cs = key in main_keys
464 |         pc = R.prefix_cache(cells[ck]) if shortcut else None
465 |         o = run_cell_sign(R, cells[ck], sg, ds, batch, T3['readout']['primary']['order_seed'], ki, pc=pc, layer_dirs=layer_dirs if main_cs else (), keep_iso_layers=main_cs)
466 |         o['layers'] = {'noop_lo': o['layers']['noop_lo'], 'rows': o['layers']['rows'], 'iso_summary': layer_summary(o['layers'], band) if main_cs else None}
467 |         out[key] = o
468 |         log('[bl3_run] 升目と符号 %s（%d/%d）・%.0f 秒' % (key, ki + 1, len(sets), time.time() - t0))
469 |     return {'head': head, 'cells': out, 'batch': batch, 'shortcut': shortcut, 'dropped': sorted(dropped)}
470 | 
471 | 
472 | def layer_summary(lay, band):
473 |     """等方の帰無の層ごとの中央値と中央の区間（正本 `descriptive.layerwise.directions`・`band`）。"""
474 |     if not lay['iso']:
475 |         return None
476 |     A = np.array(list(lay['iso'].values()), dtype=np.float64)       # 方向 × 層 × 三つ
477 |     lo_q, hi_q = 100 * (1 - band) / 2, 100 * (1 + band) / 2
478 |     return {'median': np.median(A, axis=0).tolist(), 'lo': np.percentile(A, lo_q, axis=0).tolist(), 'hi': np.percentile(A, hi_q, axis=0).tolist(), 'n': int(A.shape[0])}
479 | 
480 | 
481 | if __name__ == '__main__':
482 |     print(__doc__)
```
<<< 終: `tools/bl3_run.py` >>>

<<< 始: `tools/bl3_core.py`（SHA16 5FD84B8A825E09EA・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """bl3_core.py v1 —— B-lens 層三（Bl3）の計算の芯（numpy だけ・重みも試行も読まない・2026-09-25）。
  3 | 
  4 | 正本 `design/contrasts-Bl3.json` の決まりを、重みや試行を読まない純粋な関数に置く。走らせる器 `tools/bl3_run.py`・集計の器 `tools/analyze_Bl3.py`・
  5 | 合成データの器 `tools/dry_run_Bl3.py` が同じ関数を呼ぶ（同じ式を二度書かない）。B-lens の芯 `tools/blens_core.py` の関数は読み取りだけで呼ぶ。
  6 | 
  7 | 置くもの:
  8 |   - 読み取りの量（`readout.primary.quantity`）: 選択肢 a の文字の対数オッズ z_a − logsumexp（ほかの選択の文字と refuse の頭）・集合の中の a の確率・全語彙の質量。
  9 |   - 割合と裾（`labels.p_rule`）: `blens_core.p_equal_tailed` と、上の裾と下の裾の本数・割合を決めた裾。Holm（`blens_core.holm`・p が段を下回る）。
 10 |   - 効き目の側（`labels.side_rule`）: 等方の帰無の中央値と四分位・零が四分位の間なら符号だけ。
 11 |   - 二つ目の札（`labels.second`）: 比べる相手の中央値を中心にした最上位（`blens_core.top_rank` に中心を引いた値を渡す）・向きまで数えた順位と対の単位の順位・等方の最上位の割合。
 12 |   - 門（`gate`）: 行の符号を +1 にし、家族の鍵を「升目|符号」にして `blens_core.gate_perm` を呼ぶ。外した升目の行と、行の無くなった単位を除く。
 13 |   - 下見の機械の決定（`pilot`）: (vi) の (a)(b)・揺れの床・近道の許容・(i)(ii) の升目の決定・q1 との対応・(iii) の文の選び方・(iv) の印・(v) の近道の決定。
 14 |   - 独立の再計算の一致（`independent_recompute.agreement`）と、予想の採点（`predictions`・q7 の決まり・門が判定不能のとき）。
 15 |   - バッチの組み方（`readout.primary.batching`）: 升目と符号ごとの方向の並び（`readout.primary.order_seed` の種）・零のベクトルの無操作・端数を零のベクトルで埋める。
 16 | 用法: python tools/bl3_core.py --selftest
 17 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 18 | """
 19 | import os, sys, math, json, collections
 20 | import numpy as np
 21 | 
 22 | HERE = os.path.dirname(os.path.abspath(__file__))
 23 | sys.path.insert(0, HERE)
 24 | import blens_core as C
 25 | 
 26 | VERSION = 'v1'
 27 | NOOP, PAD = 'noop', 'pad'
 28 | 
 29 | 
 30 | # ---------------- 読み取りの量 ----------------
 31 | def lse(x, axis=-1):
 32 |     x = np.asarray(x, dtype=np.float64)
 33 |     m = np.max(x, axis=axis, keepdims=True)
 34 |     return (m + np.log(np.sum(np.exp(x - m), axis=axis, keepdims=True))).squeeze(axis)
 35 | 
 36 | 
 37 | def log_odds_a(Z, i_a, i_others):
 38 |     """選択肢 a の文字の対数オッズ（行ごと）: z_a − logsumexp（ほかの選択の文字と refuse の頭）。Z は読み取りの集合の出口の値（行 × 集合）。"""
 39 |     Z = np.atleast_2d(np.asarray(Z, dtype=np.float64))
 40 |     return Z[:, i_a] - lse(Z[:, list(i_others)], axis=-1)
 41 | 
 42 | 
 43 | def prob_a_in_set(Z, i_a, i_set):
 44 |     """選択の文字と refuse の頭の中での選択肢 a の文字の確率（生の softmax）。"""
 45 |     Z = np.atleast_2d(np.asarray(Z, dtype=np.float64))
 46 |     return np.exp(Z[:, i_a] - lse(Z[:, list(i_set)], axis=-1))
 47 | 
 48 | 
 49 | def mass_of_set(Z_full, set_ids):
 50 |     """全語彙の生の softmax での、読み取りの集合の確率の和（行ごと）。"""
 51 |     Z_full = np.atleast_2d(np.asarray(Z_full, dtype=np.float64))
 52 |     return np.exp(lse(Z_full[:, list(set_ids)], axis=-1) - lse(Z_full, axis=-1))
 53 | 
 54 | 
 55 | # ---------------- 割合と裾・Holm ----------------
 56 | def p_and_tail(m, null):
 57 |     """両側に等しい裾の割合（`blens_core.p_equal_tailed`）と、上の裾と下の裾の本数・割合を決めた裾（上・下・同じ）。"""
 58 |     null = np.asarray(null, dtype=np.float64)
 59 |     up, lo = int(np.sum(null >= m)), int(np.sum(null <= m))
 60 |     tail = 'upper' if up < lo else ('lower' if lo < up else 'tie')
 61 |     return {'p': C.p_equal_tailed(m, null), 'upper': up, 'lower': lo, 'tail': tail, 'K': int(len(null))}
 62 | 
 63 | 
 64 | def holm(pvals, alpha):
 65 |     return C.holm(pvals, alpha)
 66 | 
 67 | 
 68 | def holm_limits(K, alpha, m_rows):
 69 |     """Holm の各段を通れる外側の帰無の本数の上限（両側に等しい裾の割合 2(1+e)/(1+K) が段を下回る e の最大・下回らなければ -1）。"""
 70 |     out = []
 71 |     for step in range(1, m_rows + 1):
 72 |         thr = alpha / (m_rows - step + 1)
 73 |         es = [e for e in range(0, K) if 2 * (1 + e) / (1 + K) < thr]
 74 |         out.append(max(es) if es else -1)
 75 |     return out
 76 | 
 77 | 
 78 | # ---------------- 効き目の側 ----------------
 79 | def effect_side(e, iso_null):
 80 |     """等方の外の行の効き目の側（正本 `labels.side_rule`）。零が等方の帰無の下の四分位と上の四分位の間なら、中央値を零とみなし符号だけを書く。
 81 |     それ以外は、中央値と同じ向きで中央値より零から遠い（stronger）・零と中央値の間（weaker・零と中央値の値そのものを含む）・零を越えて反対の向き（opposite）。"""
 82 |     null = np.asarray(iso_null, dtype=np.float64)
 83 |     m0 = float(np.median(null))
 84 |     q1, q3 = float(np.percentile(null, 25)), float(np.percentile(null, 75))
 85 |     out = {'median': m0, 'q1': q1, 'q3': q3}
 86 |     if q1 <= 0.0 <= q3:
 87 |         out.update({'side': 'sign_only', 'sign': int(np.sign(e))})
 88 |         return out
 89 |     s0 = 1.0 if m0 > 0 else -1.0
 90 |     if e * s0 > 0 and abs(e) > abs(m0):
 91 |         out['side'] = 'stronger'
 92 |     elif e * s0 >= 0:
 93 |         out['side'] = 'weaker'
 94 |     else:
 95 |         out['side'] = 'opposite'
 96 |     return out
 97 | 
 98 | 
 99 | # ---------------- 二つ目の札 ----------------
100 | def second_label(e_row, comps_oriented, comps_pairs):
101 |     """二つ目の札（正本 `labels.second`）。comps_oriented: 比べる相手の効き目（両方の向き）・comps_pairs: 対ごとの (向き一, 向き二)。
102 |     中心＝比べる相手の中央値。最上位は、行の中心からの距離が比べる相手の距離のすべてを上回ること（同じ値は上回らない・`blens_core.top_rank` に中心を引いた値を渡す）。
103 |     順位: 向きまで数えた順位（1 ＋ 距離が行の距離以上の比べる相手の数）と、対の単位の順位（対の値＝両方の向きの距離の大きい方）。"""
104 |     co = np.asarray(comps_oriented, dtype=np.float64)
105 |     center = float(np.median(co))
106 |     tr = C.top_rank(float(e_row) - center, co - center)
107 |     d_row = abs(float(e_row) - center)
108 |     pv = np.array([max(abs(a - center), abs(b - center)) for a, b in comps_pairs], dtype=np.float64)
109 |     return {'center': center, 'top': tr['top'], 'rank_oriented': tr['rank'], 'of_oriented': tr['of'],
110 |             'rank_pair': int(1 + np.sum(pv >= d_row)), 'of_pair': int(len(pv) + 1), 'distance': d_row}
111 | 
112 | 
113 | def iso_top_share(iso_effects, center, comps_oriented):
114 |     """等方の最上位の割合（正本 `labels.second.iso_top_share`）: 等方の方向のうち、同じ中心と同じ比べる相手で最上位の条件を満たす割合。"""
115 |     iso = np.asarray(iso_effects, dtype=np.float64)
116 |     dmax = float(np.max(np.abs(np.asarray(comps_oriented, dtype=np.float64) - center)))
117 |     return float(np.mean(np.abs(iso - center) > dmax))
118 | 
119 | 
120 | def comparators_for(direction, pair_names, swap_siblings):
121 |     """比べる相手の対（正本 `nulls.real.rule`）: v̂ と (6b) は入れ替えの対（自分と兄弟）を除き、Nk と td は自分の対だけを除く。"""
122 |     own = {'Nk': 'Nk~N', 'td': 'Onull~N'}
123 |     if direction in ('static', 'loaded'):
124 |         drop = set(swap_siblings)
125 |     elif direction in own:
126 |         drop = {own[direction]}
127 |     else:
128 |         raise ValueError('比べる相手を決められない方向: %s' % direction)
129 |     missing = drop - set(pair_names)
130 |     if missing:
131 |         raise ValueError('除く対が対の名の並びに無い: %s' % sorted(missing))
132 |     return [p for p in pair_names if p not in drop]
133 | 
134 | 
135 | # ---------------- 門 ----------------
136 | def behavior_y(k, n, k0, n0, cc):
137 |     return C.logit_cc(k, n, cc) - C.logit_cc(k0, n0, cc)
138 | 
139 | 
140 | def gate(rows, unit_effects, units, alpha, drop_cells=()):
141 |     """門（正本 `gate`）。rows: [{'unit','cell','fam','y'}]（fam は「升目|符号」）・unit_effects: 単位 → {fam: 効き目}。
142 |     外した升目（drop_cells）の行を除き、行の無くなった単位を入れ替えから外す（入れ替えの数は残った単位の数の階乗）。符号はすべて +1 で呼ぶ（二重に掛けない）。
143 |     行が残らなければ判定不能。通るのは p が水準を下回るとき。"""
144 |     rs = [dict(r, sign=1) for r in rows if r['cell'] not in set(drop_cells)]
145 |     us = [u for u in units if any(r['unit'] == u for r in rs)]
146 |     if not rs or len(us) < 2:
147 |         return {'undetermined': True, 'n_rows': len(rs), 'units': us}
148 |     g = C.gate_perm(rs, unit_effects, us)
149 |     g.update({'undetermined': False, 'units': us, 'pass': bool(g['p'] < alpha), 'alpha': alpha})
150 |     return g
151 | 
152 | 
153 | # ---------------- 下見の機械の決定 ----------------
154 | def vi_decision(spread_a, spread_b, noise_max, batch_default):
155 |     """(vi) の決め（正本 `pilot.checks.vi`）: (b) が上限を超えたら止める。(a) が上限を超えたらバッチ一。揺れの床は本の計算のバッチの組み方に合わせる。"""
156 |     if spread_b > noise_max:
157 |         return {'stop': True, 'reason': 'vi_b', 'spread_a': spread_a, 'spread_b': spread_b}
158 |     batch = 1 if spread_a > noise_max else int(batch_default)
159 |     return {'stop': False, 'batch': batch, 'floor': float(spread_b if batch == 1 else spread_a), 'spread_a': spread_a, 'spread_b': spread_b}
160 | 
161 | 
162 | def cache_tol(floor, factor, lower, cap):
163 |     """近道の許容（正本 `pilot.cache_tol_rule`）＝ 揺れの床の倍率倍と下限の大きい方を、上限で頭打ちにした値。"""
164 |     return float(min(max(factor * floor, lower), cap))
165 | 
166 | 
167 | def spread(values):
168 |     v = np.asarray(values, dtype=np.float64)
169 |     return float(np.max(v) - np.min(v))
170 | 
171 | 
172 | def cells_decision(pass_main, pass_gate_only, cells_min_pass):
173 |     """(i)(ii) の升目の決め（正本 `pilot.decision`）: 満たす主の升目が最小の数に満たなければ止める。満たさない升目は外す。"""
174 |     n_pass = sum(1 for v in pass_main.values() if v)
175 |     dropped = sorted(c for c, v in pass_main.items() if not v) + sorted(c for c, v in pass_gate_only.items() if not v)
176 |     if n_pass < cells_min_pass:
177 |         q1 = '止める'
178 |     elif n_pass == len(pass_main):
179 |         q1 = '続ける'
180 |     else:
181 |         q1 = '一部の升目を外して続ける'
182 |     return {'q1': q1, 'n_pass': n_pass, 'n_main': len(pass_main), 'dropped': dropped, 'stop': q1 == '止める', 'reason': 'i_ii' if q1 == '止める' else None}
183 | 
184 | 
185 | def pass_i_ii(mass, p_a, mass_min, p_bounds):
186 |     return bool(mass >= mass_min and p_bounds[0] <= p_a <= p_bounds[1])
187 | 
188 | 
189 | def iii_sentence(rho):
190 |     """(iii) の文の選び方（正本 `pilot.checks.iii`）: 相関が正なら positive・零か負なら not_positive・定まらなければ undefined。"""
191 |     if rho is None or (isinstance(rho, float) and math.isnan(rho)):
192 |         return 'undefined'
193 |     return 'positive' if rho > 0 else 'not_positive'
194 | 
195 | 
196 | def variant_flags(lo_main, lo_variant, flag):
197 |     return {c: bool(abs(lo_variant[c] - lo_main[c]) > flag) for c in lo_main}
198 | 
199 | 
200 | def shortcut_ok(diffs, tol):
201 |     """(v) と本の計算の頭の近道の確かめ: 差の絶対値がすべて許容の内なら近道を使う。"""
202 |     return bool(max(abs(float(x)) for x in diffs) <= tol)
203 | 
204 | 
205 | def q1_from_attempts(attempts):
206 |     """下見のやり直しの流れ（正本 `pilot.decision.tool_error`）。attempts: 下見の試みの並び [{'decision': {...}} か {'tool_error': 文}]（登録者の裁定でやり直した順）。
207 |     q1 はやり直した下見（最後の試み）で採点し、一度目の決定（出たとき）を併記する。最後の試みが器の誤りで終わったら（やり直さないと決めたとき）、q1 は採点しない。"""
208 |     if not attempts:
209 |         raise ValueError('下見の試みが無い')
210 |     last, first = attempts[-1], attempts[0]
211 |     first_dec = (first.get('decision') or {}).get('q1')
212 |     if 'tool_error' in last:
213 |         return {'scored': False, 'q1': None, 'first_decision': first_dec, 'n_attempts': len(attempts), 'closed': '器の誤りで下見を終えられなかった'}
214 |     return {'scored': True, 'q1': last['decision']['q1'], 'first_decision': first_dec if len(attempts) > 1 else None, 'n_attempts': len(attempts)}
215 | 
216 | 
217 | # ---------------- 独立の再計算の一致 ----------------
218 | def agreement(eff_a, eff_b, tol, labels_a, labels_b):
219 |     """段ごとの一致（正本 `independent_recompute.agreement`）: 全ての効き目の差の絶対値が許容の内で、二つの道の値からそれぞれ出した札が同じ。"""
220 |     keys = sorted(eff_a)
221 |     if sorted(eff_b) != keys:
222 |         return {'agree': False, 'reason': 'keys', 'values_within_tol': False, 'labels_same': False, 'max_abs_diff': None,
223 |                 'missing': sorted(set(eff_a) ^ set(eff_b))}
224 |     dmax = max(float(np.max(np.abs(np.asarray(eff_a[k], dtype=np.float64) - np.asarray(eff_b[k], dtype=np.float64)))) for k in keys)
225 |     same = labels_a == labels_b
226 |     return {'agree': bool(dmax <= tol and same), 'values_within_tol': bool(dmax <= tol), 'labels_same': bool(same), 'max_abs_diff': dmax}
227 | 
228 | 
229 | # ---------------- 予想の採点 ----------------
230 | def bucket(n, options):
231 |     """零／一から三／四以上・零／一か二／三以上。"""
232 |     if options == ['零', '一から三', '四以上']:
233 |         return '零' if n == 0 else ('一から三' if n <= 3 else '四以上')
234 |     if options == ['零', '一か二', '三以上']:
235 |         return '零' if n == 0 else ('一か二' if n <= 2 else '三以上')
236 |     raise ValueError('選択肢の形が決まっていない: %s' % options)
237 | 
238 | 
239 | def score_q7(rows, floor):
240 |     """q7（正本 `predictions.q7_rule`）。rows: 等方の外の v̂ の行 [{'effect','stage_b_diff','contains_zero'}]。
241 |     区間が零を含む行と、効き目の絶対値が揺れの床以下の行は数えない。数えられる行が残らなければ採点しない（None）。"""
242 |     use = [r for r in rows if not r['contains_zero'] and abs(r['effect']) > floor]
243 |     if not use:
244 |         return None
245 |     same = [np.sign(r['effect']) == np.sign(r['stage_b_diff']) for r in use]
246 |     return 'すべて同じ' if all(same) else ('すべて逆' if not any(same) else '混ざる')
247 | 
248 | 
249 | # ---------------- 独立の再計算の組 ----------------
250 | def recompute_set(main_rows, pair_names, swap_siblings, n_iso, dropped_cells=()):
251 |     """独立の再計算で流す組（正本 `independent_recompute.what`）: v̂ の行ごとに、無操作・v̂・等方の帰無のすべて・比べる相手のすべて（両方の向き）。
252 |     下見で外した升目の行は除く。戻り値: rows [(行の名, 升目の鍵, 符号)]・dirs_by_row {行の名: [(方向の名, 符号)]}。"""
253 |     rows, dirs_by_row = [], collections.OrderedDict()
254 |     comps = comparators_for('static', pair_names, swap_siblings)
255 |     for r in main_rows:
256 |         cell = '%s|%s' % (r['scenario'], r['base'])
257 |         if r['direction'] != 'static' or cell in set(dropped_cells):
258 |             continue
259 |         s = int(r['sign'])
260 |         rows.append((r['id'], cell, s))
261 |         dirs_by_row[r['id']] = [('static', s)] + [('iso:%d' % i, s) for i in range(n_iso)] + [('real:' + p, s) for p in comps] + [('real:' + p, -s) for p in comps]
262 |     return rows, dirs_by_row
263 | 
264 | 
265 | # ---------------- バッチの組み方 ----------------
266 | def batch_plan(dir_ids, batch, seed, key):
267 |     """升目と符号ごとのバッチ（正本 `readout.primary.batching`）。方向の並びを種（`order_seed`）と升目と符号の番号（key）で混ぜ、零のベクトルの無操作を一つ入れ、
268 |     最後のバッチの端数を零のベクトル（PAD・値は使わない）で埋める。戻り値: バッチの並び（各バッチは方向の名の並び・長さはすべて batch）。"""
269 |     ids = list(dir_ids) + [NOOP]
270 |     if len(set(ids)) != len(ids):
271 |         raise ValueError('方向の名が重なる')
272 |     rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(key)]))
273 |     order = [ids[i] for i in rng.permutation(len(ids))]
274 |     n_b = -(-len(order) // batch)
275 |     order = order + [PAD] * (n_b * batch - len(order))
276 |     return [order[i * batch:(i + 1) * batch] for i in range(n_b)]
277 | 
278 | 
279 | # ---------------- 自己検査 ----------------
280 | def _selftest():
281 |     rng = np.random.default_rng(0)
282 |     # 読み取りの量: 手で計算した値と合う・全語彙の正規化が打ち消し合う
283 |     Z = np.array([[2.0, 0.5, -1.0, 0.0]])
284 |     want = 2.0 - math.log(math.exp(0.5) + math.exp(-1.0) + math.exp(0.0))
285 |     assert abs(log_odds_a(Z, 0, [1, 2, 3])[0] - want) < 1e-12
286 |     assert abs(log_odds_a(Z + 7.0, 0, [1, 2, 3])[0] - want) < 1e-12
287 |     pa = prob_a_in_set(Z, 0, [0, 1, 2, 3])[0]
288 |     assert abs(math.log(pa / (1 - pa)) - want) < 1e-12
289 |     Zf = rng.normal(size=(3, 50))
290 |     ms = mass_of_set(Zf, [1, 5, 7])
291 |     ref = np.exp(Zf[:, [1, 5, 7]]).sum(1) / np.exp(Zf).sum(1)
292 |     assert np.allclose(ms, ref)
293 |     # 割合と裾
294 |     null = np.arange(-10, 11, dtype=float)
295 |     r = p_and_tail(9.5, null)
296 |     assert r['upper'] == 1 and r['lower'] == 20 and r['tail'] == 'upper' and abs(r['p'] - 2 * 2 / 22) < 1e-12
297 |     assert p_and_tail(0.0, null)['tail'] == 'tie'
298 |     # Holm の段の上限（二巡目の確かめ K456 の値の形）
299 |     lim = holm_limits(1999, 0.05, 16)
300 |     assert lim[:4] == [2, 2, 2, 2] and lim[-1] == 48, lim
301 |     # 効き目の側
302 |     nul = rng.normal(loc=3.0, scale=0.5, size=999)
303 |     assert effect_side(5.0, nul)['side'] == 'stronger' and effect_side(1.0, nul)['side'] == 'weaker' and effect_side(-1.0, nul)['side'] == 'opposite'
304 |     assert effect_side(0.0, nul)['side'] == 'weaker'
305 |     nz = rng.normal(loc=0.1, scale=1.0, size=999)
306 |     s = effect_side(-2.0, nz)
307 |     assert s['side'] == 'sign_only' and s['sign'] == -1
308 |     # 二つ目の札: 中心を引く・同じ値は上回らない・対の単位の順位
309 |     comps = np.array([1.0, 1.2, 0.8, 1.1, 0.9, 1.05])
310 |     pairs = [(1.0, 1.2), (0.8, 1.1), (0.9, 1.05)]
311 |     sl = second_label(2.0, comps, pairs)
312 |     assert sl['top'] and sl['rank_oriented'] == 1 and sl['rank_pair'] == 1 and abs(sl['center'] - float(np.median(comps))) < 1e-12
313 |     edge = float(np.median(comps)) + float(np.max(np.abs(comps - np.median(comps))))
314 |     assert not second_label(edge, comps, pairs)['top']
315 |     assert not second_label(1.0, comps, pairs)['top']
316 |     assert abs(iso_top_share(np.array([0.0, 5.0, 1.0]), float(np.median(comps)), comps) - 2 / 3) < 1e-12
317 |     names = ['O~Osec', 'O~Onull', 'Nk~N', 'Onull~N', 'O~Osec-Ncold', 'Osec~O-Ncold', 'O-Ncold~Osec-Ncold']
318 |     sw = ['O~Osec', 'O~Osec-Ncold', 'Osec~O-Ncold', 'O-Ncold~Osec-Ncold']
319 |     assert comparators_for('static', names, sw) == ['O~Onull', 'Nk~N', 'Onull~N']
320 |     assert comparators_for('Nk', names, sw) == [n for n in names if n != 'Nk~N']
321 |     # 門: 奇でない押し・減算の行・外した升目と行の無くなった単位
322 |     units = ['A', 'B', 'C', 'D']
323 |     fams = ['S1|X|+', 'S1|X|-']
324 |     eff = {u: {f: float(i) + (0.3 if f.endswith('-') else 0.0) for f in fams} for i, u in enumerate(units)}
325 |     rows = [{'unit': u, 'cell': 'S1|X', 'fam': f, 'y': eff[u][f] * 2} for u in units for f in fams]
326 |     g = gate(rows, eff, units, 0.05)
327 |     assert g['n_perm'] == 24 and g['rho'] > 0.9
328 |     rows2 = rows + [{'unit': 'E', 'cell': 'S4|Y', 'fam': 'S4|Y|+', 'y': 0.0}]
329 |     eff2 = dict(eff, E={'S4|Y|+': 0.0, 'S1|X|+': 0.0, 'S1|X|-': 0.0})
330 |     for u in units:
331 |         eff2[u] = dict(eff2[u], **{'S4|Y|+': 0.0})
332 |     g2 = gate(rows2, eff2, units + ['E'], 0.05, drop_cells=['S4|Y'])
333 |     assert g2['units'] == units and g2['n_perm'] == 24, g2
334 |     assert gate(rows, eff, units, 0.05, drop_cells=['S1|X'])['undetermined']
335 |     # 下見の決め
336 |     assert vi_decision(0.001, 0.02, 0.01, 16)['stop']
337 |     d = vi_decision(0.02, 0.003, 0.01, 16)
338 |     assert not d['stop'] and d['batch'] == 1 and d['floor'] == 0.003
339 |     d = vi_decision(0.004, 0.0, 0.01, 16)
340 |     assert d['batch'] == 16 and d['floor'] == 0.004
341 |     assert cache_tol(0.0, 2, 0.005, 0.01) == 0.005 and cache_tol(0.004, 2, 0.005, 0.01) == 0.008 and cache_tol(0.009, 2, 0.005, 0.01) == 0.01
342 |     pm = {'c%d' % i: True for i in range(8)}
343 |     assert cells_decision(pm, {}, 6)['q1'] == '続ける'
344 |     pm['c0'] = pm['c1'] = False
345 |     cd = cells_decision(pm, {'g0': False}, 6)
346 |     assert cd['q1'] == '一部の升目を外して続ける' and cd['dropped'] == ['c0', 'c1', 'g0']
347 |     pm['c2'] = False
348 |     assert cells_decision(pm, {}, 6)['q1'] == '止める'
349 |     assert pass_i_ii(0.95, 0.5, 0.9, [0.0001, 0.9999]) and not pass_i_ii(0.85, 0.5, 0.9, [0.0001, 0.9999]) and not pass_i_ii(0.95, 0.99995, 0.9, [0.0001, 0.9999])
350 |     assert iii_sentence(0.3) == 'positive' and iii_sentence(0.0) == 'not_positive' and iii_sentence(float('nan')) == 'undefined'
351 |     assert shortcut_ok([0.001, -0.004], 0.005) and not shortcut_ok([0.006], 0.005)
352 |     # 下見のやり直しの流れ: やり直した下見で採点し、一度目の決定を併記する・やり直さずに閉じたら採点しない
353 |     r_ = q1_from_attempts([{'tool_error': 'x'}, {'decision': {'q1': '続ける'}}])
354 |     assert r_['scored'] and r_['q1'] == '続ける' and r_['first_decision'] is None and r_['n_attempts'] == 2
355 |     assert q1_from_attempts([{'decision': {'q1': '止める'}}, {'decision': {'q1': '続ける'}}])['first_decision'] == '止める'
356 |     assert not q1_from_attempts([{'tool_error': 'x'}])['scored']
357 |     # 再計算の一致: 値の許容と札の両方
358 |     a_ = {'r': [0.1, 0.2]}
359 |     assert agreement(a_, {'r': [0.1005, 0.2]}, 0.001, {'x': 1}, {'x': 1})['agree']
360 |     assert not agreement(a_, {'r': [0.1005, 0.2]}, 0.0001, {'x': 1}, {'x': 1})['agree']
361 |     assert not agreement(a_, a_, 0.001, {'x': 1}, {'x': 2})['agree']
362 |     # 予想の採点
363 |     assert bucket(0, ['零', '一から三', '四以上']) == '零' and bucket(3, ['零', '一から三', '四以上']) == '一から三' and bucket(4, ['零', '一から三', '四以上']) == '四以上'
364 |     assert bucket(2, ['零', '一か二', '三以上']) == '一か二' and bucket(3, ['零', '一か二', '三以上']) == '三以上'
365 |     q7rows = [{'effect': 0.5, 'stage_b_diff': 17.0, 'contains_zero': False}, {'effect': -0.4, 'stage_b_diff': -11.0, 'contains_zero': False},
366 |               {'effect': 0.3, 'stage_b_diff': -2.0, 'contains_zero': True}]
367 |     assert score_q7(q7rows, 0.0) == 'すべて同じ' and score_q7(q7rows[2:], 0.0) is None and score_q7(q7rows[:1], 0.6) is None
368 |     assert score_q7([{'effect': -0.5, 'stage_b_diff': 17.0, 'contains_zero': False}], 0.0) == 'すべて逆'
369 |     # バッチの組み方: 端数を零のベクトルで埋め、全ての方向と無操作が一度ずつ入り、種で決まる
370 |     ids = ['d%d' % i for i in range(2034)]
371 |     bp = batch_plan(ids, 16, 91002, 0)
372 |     flat = [x for b in bp for x in b]
373 |     assert len(bp) == 128 and all(len(b) == 16 for b in bp) and flat.count(PAD) == 13 and flat.count(NOOP) == 1
374 |     assert sorted(x for x in flat if x not in (PAD, NOOP)) == sorted(ids)
375 |     assert batch_plan(ids, 16, 91002, 0) == bp and batch_plan(ids, 16, 91002, 1) != bp
376 |     assert flat.index(PAD) >= len(flat) - 13
377 |     print('[bl3_core] 自己検査 OK（%s）' % VERSION)
378 | 
379 | 
380 | if __name__ == '__main__':
381 |     if '--selftest' in sys.argv:
382 |         _selftest()
383 |     else:
384 |         print(__doc__)
```
<<< 終: `tools/bl3_core.py` >>>

<<< 始: `tools/colab/boot_Bl3.py`（SHA16 FBDCB7EB690673CC・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """boot_Bl3.py v1 —— B-lens 層三（Bl3）の Colab 起動スクリプト（教師強制の順伝播・2026-09-25・正本 `readout`・`pilot`・`computation`・`independent_recompute`）。
  3 | 
  4 | 相（OP4B_PHASE）:
  5 |   check  封印の前の確かめ（正本 `computation.before_seal`: 読み込みと版の確かめだけ・**順伝播を一度も走らせない・値を出さない**。模型の順伝播の前の hook で、呼ばれたら止める）:
  6 |          コミット固定の取り出し・版（正本 `inputs.versions_B`・文字列の完全な一致・torch は CUDA の組みまで・裁定 D187）・GPU・重みの断片の SHA-256（転記行 F）・
  7 |          方向の npz の SHA-256（方向の記録）と組ごとの SHA-256（転記行 D）・模型の読み込みと設定（正本 `inputs.model`）・選んだ層の添字（正本 `layers.indices`）・
  8 |          升目の入力（実トークナイザの組み立てを転記行 B と）・升目と符号の組と独立の再計算の組の順伝播の数（転記行 E と）・門の行（転記行 C の数と）・
  9 |          乙の行と文脈（B-lens の選んだ出力の一覧の SHA16 と、全ての文脈を組めること）・加減の hook を掛けて外せること・残差の書き換えの器が import できること。
 10 |   pilot  封印の後: 下見の前の凍結の記録と封印の記録がそろったコミットで、凍結の記録の SHA16 を取り出した器と正本に照らしてから、正本 `pilot.order` の順に走らせ、
 11 |          下見の記録（`bl3_run.run_pilot` の出力）を置く。器の誤り（凍結した確かめが機械で落ちた）は、その文を記録に置いて止める（正本 `pilot.decision.tool_error`）。
 12 |   main   本の凍結の後: 凍結の記録に足した下見の記録（バッチの大きさ・揺れの床・近道の許容・近道・外した升目）のまま、組（OP4B_PART・既定は三つとも順に）を走らせる:
 13 |            main       本の計算の頭（出口の値・近道の確かめ・最後の層）→ 全ての升目と符号（`bl3_run.run_main_phase`）
 14 |            recompute  独立の再計算の二つの道（本の器のフック〔`bl3_run.recompute_hook_path`〕・残差の書き換え〔別の個体の器 `bl3_recompute_rewrite`〕・近道なし・バッチ一）
 15 |            secondary  乙（`bl3_run.run_secondary`・裁定 D227）
 16 |          どの組も頭で出口の値の自己検査を走らせる。**効き目の値は印字しない**（札・門・二段の一致は手元の集計の器が出し、一致か不一致かだけを先に見る・正本
 17 |          `independent_recompute.print`）。器の誤りは、その文を組の出力に置いて止める（正本 `computation.tool_error`）。組の出力は出来たときに置く。
 18 | 止める条件（外れたら止める・登録者に相談）: 版の不一致（入れ直した後にランタイムの再起動を求める）・GPU・重みの SHA-256・方向の npz の SHA-256・凍結の記録の SHA16 と
 19 |   取り出した器と正本の不一致・取り出した作業木の変更・模型の設定・升目の入力と転記行 B の不一致・順伝播の数と転記行 E の不一致・乙の文脈を組めない・凍結と封印の記録の欠け・器の誤り。
 20 | 運用: コーディネータが登録者の Chrome 越しに Colab を操作する（ランタイムの選択と結果の zip のダウンロードもコーディネータ）。登録者の手に残すのは同意と支払い。
 21 |   資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。Drive は使わない（出力は小さく、終わりに zip を落とす）。セルの出力の表示が固まることがあるので、
 22 |   進みは出力の置き場の `progress.log` にも書く（ターミナルで見る）。ランタイムが落ちたら、落ちた組から新しいランタイムで走らせ直す（同じ GPU の種類・逸脱の台帳に記す）。
 23 | セルに打つ一行（先頭の下線は type の事故の緩衝・<commit> は 40 桁・相 main の組を分けるときは OP4B_PART を足す）:
 24 |   ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='check';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_Bl3.py').read())
 25 | DRY（手元の検査・OP4B_DRY=1）: 乱数の小さな模型（`tools/dry_run_Bl3.py` の作り方と読み取りの集合の行の置き直し）と実トークナイザ・合成の方向（実の名だけを借りる）で、
 26 |   三つの相を CPU で通す。OP4B_REPO_DIR・OP4B_OUT が要る。版・GPU・重み・凍結と封印の記録は見ない（印を残す）。方向の npz の確かめは手元の npz で行う。
 27 |   相 main は OP4B_DRY_PILOT（相 pilot の出力の pilot.json）を読む。OP4B_DRY_ISO で等方の本数（既定 9）、OP4B_DRY_SEC で乙の文脈の数（既定 2）、
 28 |   OP4B_DRY_RC で独立の再計算の v̂ の行の数（既定 2・減算の行と加算の行を一つずつから）を減らす。残差の書き換えの器が無ければ、DRY に限り印を残して飛ばす。
 29 | 柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 30 | """
 31 | import os, sys, re, json, time, glob, shutil, hashlib, datetime, traceback, subprocess, zipfile, collections
 32 | 
 33 | VERSION = 'v1'
 34 | T0 = time.time()
 35 | REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
 36 | PHASES = ('check', 'pilot', 'main')
 37 | PARTS = ('main', 'recompute', 'secondary')
 38 | SPARSE = ['tools', 'arms', 'design', 'records', 'results/Bl3', 'results/stageB']
 39 | LOG = []
 40 | PROGRESS = {'path': None}
 41 | CLAUSE = '本記録は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
 42 | now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
 43 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 44 | 
 45 | 
 46 | class Stop(Exception):
 47 |     pass
 48 | 
 49 | 
 50 | def sha256f(p):
 51 |     h = hashlib.sha256()
 52 |     with open(p, 'rb') as fh:
 53 |         for blk in iter(lambda: fh.read(1 << 24), b''):
 54 |             h.update(blk)
 55 |     return h.hexdigest().upper()
 56 | 
 57 | 
 58 | def say(line):
 59 |     print(line, flush=True)
 60 |     if PROGRESS['path']:
 61 |         with open(PROGRESS['path'], 'a', encoding='utf-8') as fh:
 62 |             fh.write(line + '\n')
 63 | 
 64 | 
 65 | def mark(step, **kw):
 66 |     LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
 67 |     say('[boot_Bl3] %-16s %7.0fs %s' % (step, time.time() - T0, kw or ''))
 68 | 
 69 | 
 70 | def sh(cmd, check=True):
 71 |     r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
 72 |     if check and r.returncode != 0:
 73 |         print(r.stdout[-2000:]); print(r.stderr[-3000:])
 74 |         raise RuntimeError('失敗: %s' % cmd)
 75 |     return r
 76 | 
 77 | 
 78 | def stop(msg):
 79 |     mark('stop', reason=msg)
 80 |     sys.exit('[boot_Bl3] 止める（登録者に相談）: ' + msg)
 81 | 
 82 | 
 83 | def jdefault(o):
 84 |     """numpy の数と配列を JSON に（値の丸めはしない）。"""
 85 |     if hasattr(o, 'tolist'):
 86 |         return o.tolist()
 87 |     if hasattr(o, 'item'):
 88 |         return o.item()
 89 |     raise TypeError(type(o))
 90 | 
 91 | 
 92 | def write_json(path, obj):
 93 |     json.dump(obj, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=jdefault)
 94 |     return sha16f(path)
 95 | 
 96 | 
 97 | def verify_frozen(repo, sha_map):
 98 |     """凍結の記録の SHA16（改行を LF にそろえた SHA-256 の頭 16 桁）を、取り出した作業木のファイルに照らす。疎な取り出しで無いファイルは飛ばして数を記す。"""
 99 |     bad, skipped = [], []
100 |     for rp, want in sha_map.items():
101 |         p = os.path.join(repo, *rp.split('/'))
102 |         if not os.path.exists(p):
103 |             skipped.append(rp)
104 |             continue
105 |         got = sha16f(p)
106 |         if got != want:
107 |             bad.append({'path': rp, 'got': got, 'want': want})
108 |     return bad, skipped
109 | 
110 | 
111 | def pick_recompute_rows(rows, n):
112 |     """DRY の独立の再計算の行: 減算の行と加算の行を一つずつから、足りなければ前から足す（本の計算では全ての行）。"""
113 |     idx = [i for i, r in enumerate(rows) if r[2] < 0][:1] + [i for i, r in enumerate(rows) if r[2] > 0][:1]
114 |     idx += [i for i in range(len(rows)) if i not in idx]
115 |     return [rows[i] for i in sorted(idx[:n])]
116 | 
117 | 
118 | def run():
119 |     PHASE = os.environ.get('OP4B_PHASE', 'check')
120 |     COMMIT = os.environ.get('OP4B_COMMIT', '')
121 |     DRY = os.environ.get('OP4B_DRY') == '1'
122 |     if PHASE not in PHASES:
123 |         sys.exit('[boot_Bl3] 相は %s のどれか' % '・'.join(PHASES))
124 |     if not DRY:
125 |         stray = sorted(k for k in os.environ if k.startswith('OP4B_DRY_') or k in ('OP4B_REPO_DIR', 'OP4B_OUT'))
126 |         if stray:
127 |             sys.exit('[boot_Bl3] DRY でないのに検査用の環境変数がある: %s（外してから走らせる）' % '・'.join(stray))
128 |         if not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
129 |             sys.exit('[boot_Bl3] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
130 |     given = [p.strip() for p in os.environ.get('OP4B_PART', ','.join(PARTS)).split(',') if p.strip()]
131 |     if PHASE == 'main' and (not given or any(p not in PARTS for p in given)):
132 |         sys.exit('[boot_Bl3] OP4B_PART は %s の組み合わせ（コンマで区切る）' % '・'.join(PARTS))
133 |     parts = [p for p in PARTS if p in given] if PHASE == 'main' else []
134 |     print('[boot_Bl3] %s 開始 phase=%s %s%s' % (VERSION, PHASE, 'DRY' if DRY else COMMIT, (' parts=' + ','.join(parts)) if parts else ''), flush=True)
135 | 
136 |     # ---- 1. リポジトリ（コミット固定）と出力の置き場
137 |     if DRY:
138 |         REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
139 |         OUTROOT = os.path.abspath(os.environ['OP4B_OUT'])
140 |     else:
141 |         REPO, OUTROOT = '/content/ontology-preamble-4b', '/content/op4b-Bl3'
142 |         head_ok = os.path.isdir(os.path.join(REPO, '.git')) and sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
143 |         if not head_ok:
144 |             shutil.rmtree(REPO, ignore_errors=True)
145 |             sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
146 |             sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone'] + SPARSE)
147 |             sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
148 |         if sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() != COMMIT:
149 |             stop('取り出したコミットが OP4B_COMMIT と違う')
150 |         dirty = sh(['git', '-C', REPO, 'status', '--porcelain'], check=False).stdout.strip()
151 |         if dirty:
152 |             stop('取り出した作業木に変更がある: %s' % dirty.splitlines()[:5])
153 |     stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
154 |     od = os.path.join(OUTROOT, '%s-%s' % (PHASE, stamp))
155 |     os.makedirs(od, exist_ok=True)
156 |     PROGRESS['path'] = os.path.join(od, 'progress.log')
157 |     CANON = os.path.join(REPO, 'design', 'contrasts-Bl3.json')
158 |     T3 = json.load(open(CANON, encoding='utf-8'))
159 |     FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
160 |     FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
161 |     FRP = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
162 |     SRP = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
163 |     FR, frozen = None, None
164 |     if PHASE in ('pilot', 'main'):
165 |         if DRY:
166 |             mark('dry_no_gate', note='DRY は凍結と封印の記録を見ない')
167 |         else:
168 |             for p in (FRP, SRP):
169 |                 if not os.path.exists(p):
170 |                     stop('相 %s は下見の前の凍結と封印の後に走らせる（%s が無い・正本 predictions.when）' % (PHASE, os.path.basename(p)))
171 |             FR = json.load(open(FRP, encoding='utf-8'))
172 |             if PHASE == 'main' and 'main_freeze' not in FR:
173 |                 stop('相 main は本の凍結の後に走らせる（凍結の記録に本の凍結が無い）')
174 |             sha_map = FR['main_freeze']['frozen_sha16'] if PHASE == 'main' else FR['frozen_sha16']
175 |             bad, skipped = verify_frozen(REPO, sha_map)
176 |             frozen = {'checked': len(sha_map) - len(skipped), 'skipped': skipped, 'bad': bad}
177 |             if bad:
178 |                 stop('凍結の記録の SHA16 と取り出したファイルが違う: %s' % bad)
179 |             mark('frozen', checked=frozen['checked'], skipped=len(skipped))
180 |     mark('repo', commit=COMMIT[:12] or 'dry', canon=T3['version'], canon_sha16=sha16f(CANON), out=od)
181 | 
182 |     # ---- 2. 版（正本 inputs.versions_B）と GPU
183 |     import importlib.metadata as md
184 | 
185 |     def ver(k):
186 |         try:
187 |             return md.version(k)
188 |         except Exception:
189 |             return None
190 |     PIN = T3['inputs']['versions_B']
191 |     VER = {k: ver(k) for k in ('numpy', 'scipy', 'torch', 'transformers', 'torchvision', 'torchaudio', 'tokenizers', 'huggingface_hub', 'accelerate', 'safetensors')}
192 |     want = {'numpy': PIN['numpy'], 'torch': PIN['torch'], 'transformers': PIN['transformers']}
193 |     bad_v = {k: VER[k] for k, v in want.items() if VER[k] != v}          # 文字列の完全な一致（torch は CUDA の組みまで・裁定 D187）
194 |     if bad_v and not DRY:
195 |         mark('pin', installing=bad_v)
196 |         os.environ['HF_HUB_DISABLE_XET'] = '1'
197 |         if 'torch' in bad_v:
198 |             cuda = PIN['torch'].split('+')[1]
199 |             pk = ['torch==%s' % PIN['torch']] + ['%s==%s+%s' % (c, VER[c].split('+')[0], cuda) for c in ('torchvision', 'torchaudio') if VER.get(c)]
200 |             sh([sys.executable, '-m', 'pip', 'install', '-q'] + pk + ['--index-url', 'https://download.pytorch.org/whl/%s' % cuda])
201 |         sh([sys.executable, '-m', 'pip', 'install', '-q', 'numpy==%s' % want['numpy'], 'transformers==%s' % want['transformers'], 'accelerate', 'huggingface_hub', 'safetensors'])
202 |         print('[boot_Bl3] 版を入れ直した。**ランタイムを再起動して（「ランタイム」→「セッションを再起動」）、同じ一行をもう一度走らせる**', flush=True)
203 |         sys.exit(0)
204 |     GPU = 'dry'
205 |     if not DRY:
206 |         GPU = sh('nvidia-smi --query-gpu=name --format=csv,noheader', check=False).stdout.strip().split('\n')[0]
207 |         if 'L4' not in GPU and 'A100' not in GPU:
208 |             stop('GPU %s は登録の環境（Colab L4・A100 は予備）に無い' % GPU)
209 |     mark('versions', versions=VER, gpu=GPU)
210 | 
211 |     import numpy as np
212 |     import torch
213 |     sys.path.insert(0, os.path.join(REPO, 'tools'))
214 |     sys.path.insert(0, os.path.join(REPO, 'tools', 'colab'))
215 |     import direction_B
216 |     import run_stageB_local as RB
217 |     import bl3_core as K
218 |     import bl3_run as BR
219 |     import bl3_directions as BD
220 |     import analyze_Bl3 as AZ
221 |     from transformers import AutoTokenizer, AutoModelForCausalLM
222 | 
223 |     # ---- 3. 重み（転記行 F の SHA-256 と突き合わせる）
224 |     M = T3['inputs']['model']
225 |     W_SHA = {}
226 |     if DRY:
227 |         import dry_run_Bl3 as DR
228 |         SNAPDIR = os.environ.get('OP4B_TOKENIZER_DIR') or DR.SNAP
229 |     else:
230 |         os.environ['HF_HUB_DISABLE_XET'] = '1'
231 |         from huggingface_hub import snapshot_download
232 |         SNAPDIR = snapshot_download(M['repo'], revision=M['rev'])
233 |         W_SHA = {fn: sha256f(os.path.join(SNAPDIR, fn)) for fn in FJ['facts']['F']['sha256']}
234 |         badw = [fn for fn, sha in FJ['facts']['F']['sha256'].items() if W_SHA[fn] != sha]
235 |         if badw:
236 |             stop('重みの SHA-256 が転記行 F と違う: %s' % badw)
237 |     mark('weights', snapshot=os.path.basename(SNAPDIR), checked=len(W_SHA))
238 | 
239 |     # ---- 4. 方向の npz（方向の記録の SHA-256・組ごとの SHA-256 を転記行 D と・Colab で乱数を引き直さない）
240 |     NPZ = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.npz')
241 |     DJP = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json')
242 |     DJ = json.load(open(DJP, encoding='utf-8'))
243 |     npz_sha = sha256f(NPZ)
244 |     if npz_sha != DJ['npz_sha256']:
245 |         stop('方向の npz の SHA-256 が方向の記録と違う')
246 |     if FR is not None and npz_sha != FR.get('directions_npz_sha256'):
247 |         stop('方向の npz の SHA-256 が凍結の記録と違う')
248 |     Zd = np.load(NPZ)
249 |     try:
250 |         grp = BD.verify_against_facts({g: Zd[g] for g in BD.GROUPS}, FJ)
251 |         dirs_real, names_real = BR.load_dirs(NPZ, DJP)
252 |     except (SystemExit, BR.ToolError) as e_:
253 |         stop(str(e_))
254 |     pair_names = list(DJ['groups']['real']['names'])
255 |     mark('directions', npz_sha256=npz_sha[:16], groups={k: v[:16] for k, v in grp.items()}, n=len(dirs_real))
256 | 
257 |     # ---- 5. 模型とトークナイザ
258 |     tok = AutoTokenizer.from_pretrained(SNAPDIR)
259 |     if DRY:
260 |         model, cfg = DR.tiny_model()
261 |         dev = 'cpu'
262 |     else:
263 |         model = AutoModelForCausalLM.from_pretrained(SNAPDIR, torch_dtype=torch.bfloat16, device_map='cuda').eval()
264 |         cfg = model.config
265 |         dev = 'cuda'
266 |         got = {'num_hidden_layers': cfg.num_hidden_layers, 'hidden_size': cfg.hidden_size, 'vocab_size': cfg.vocab_size, 'rms_norm_eps': cfg.rms_norm_eps,
267 |                'tie_word_embeddings': cfg.tie_word_embeddings, 'tokenizer_len': len(tok)}
268 |         if got != {k: M[k] for k in got}:
269 |             stop('模型の設定が正本 inputs.model と違う: %s' % {k: (got[k], M[k]) for k in got if got[k] != M[k]})
270 |     L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
271 |     if not DRY and L != T3['layers']['indices'][str(T3['layers']['selected_ratio'])]:
272 |         stop('選んだ層の添字が正本 layers.indices と違う: %d' % L)
273 |     coef = float(T3['layers']['coef_applied'])
274 |     mark('model', dry=DRY, layers=cfg.num_hidden_layers, layer_idx=L, coef=coef, dtype=str(next(model.parameters()).dtype), device=dev)
275 | 
276 |     # ---- 6. 升目の入力（凍結の組み立ての関数と転記行 A の書き出し・転記行 B と突き合わせる）
277 |     cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
278 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
279 |     gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in gate_only})
280 |     try:
281 |         cells = BR.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
282 |     except BR.ToolError as e_:
283 |         stop(str(e_))
284 |     mark('cells', main=len(cell_keys), gate_only=len(gate_only_cells))
285 | 
286 |     SESSION = {'kind': 'bl3_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY, 'gpu': GPU, 'versions': VER, 'weights_sha256': W_SHA,
287 |                'canon_sha16': sha16f(CANON), 'directions_npz_sha256': npz_sha, 'directions_group_sha256': grp, 'frozen_check': frozen, 'layer_idx': L, 'coef': coef}
288 | 
289 |     def finish(extra=None):
290 |         SESSION.update(extra or {})
291 |         SESSION.update({'log': LOG, 'finished': now(), 'seconds': round(time.time() - T0, 1), 'clause': CLAUSE})
292 |         write_json(os.path.join(od, 'session.json'), SESSION)
293 |         zp = od + '.zip'
294 |         with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
295 |             for fn in sorted(os.listdir(od)):
296 |                 z.write(os.path.join(od, fn), os.path.join(os.path.basename(od), fn))
297 |         zsha = sha256f(zp)
298 |         mark('done', zip=os.path.basename(zp), sha256=zsha)
299 |         if not DRY:
300 |             try:
301 |                 from google.colab import files
302 |                 files.download(zp)
303 |             except Exception as e_:
304 |                 print('[boot_Bl3] zip の自動のダウンロードが走らなかった（左の「ファイル」から落とす）: %s' % e_)
305 |         return od
306 | 
307 |     # ---- 7. 相 check（順伝播を一度も走らせない）
308 |     if PHASE == 'check':
309 |         guard = model.register_forward_pre_hook(lambda m, a: (_ for _ in ()).throw(Stop('相 check で順伝播が呼ばれた（正本 computation.before_seal）')))
310 |         E = FJ['facts']['E']
311 |         sets = BR.cell_sign_sets(T3, None, names_real['named'], names_real['B_random'], names_real['iso'], names_real['real'], gate_only)
312 |         n_pass = sum(len(s[3]) for s in sets)
313 |         if n_pass != E['passes_main'] + E['passes_gate_extra'] + E['passes_orient_extra']:
314 |             stop('升目と符号の組の順伝播の数が転記行 E と違う: %d' % n_pass)
315 |         rows_rc, dbr = K.recompute_set(T3['main_rows'], pair_names, T3['nulls']['real']['swap_siblings'], T3['nulls']['isotropic']['count'])
316 |         n_rc = sum(1 + len(v) for v in dbr.values())
317 |         if 2 * n_rc != E['passes_recompute'] or any(1 + len(v) != E['per_row_recompute'] for v in dbr.values()):
318 |             stop('独立の再計算の組の順伝播の数が転記行 E と違う: %d' % n_rc)
319 |         AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
320 |         rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader(REPO))
321 |         if len(rows_gate) != T3['gate']['rows_gate'] or sorted(r['name'] for r in rows_gate) != sorted(FJ['facts']['C']['style_share_pt']):
322 |             stop('門の行が転記行 C と違う: %d' % len(rows_gate))
323 |         sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
324 |         cnt = AZ.secondary_counts(FB, sec_rows)
325 |         try:
326 |             ctx = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
327 |         except BR.ToolError as e_:
328 |             stop(str(e_))
329 |         if len(ctx) != cnt['contexts']:
330 |             stop('乙の文脈の数が B-lens の選んだ出力の数と違う: %d' % len(ctx))
331 |         if (cnt['row_passes'], cnt['sign_batches'], cnt['contexts']) != (E['passes_secondary'], E['batches_secondary'], E['contexts_secondary']):
332 |             stop('乙の順伝播の数が転記行 E と違う: %s' % cnt)
333 |         V0 = np.zeros((1, cfg.hidden_size), dtype=np.float32)
334 |         try:
335 |             h_ = RB.register_hook(model, L, RB.make_hook(V0, coef, 1, [0], meta={'bl3': 'check'}))
336 |             h_.remove()
337 |             RB.assert_no_hooks(model, L)
338 |         except SystemExit as e_:
339 |             stop('加減の hook を掛けて外せない: %s' % e_)
340 |         try:
341 |             import bl3_recompute_rewrite as RW
342 |             rw_ok = hasattr(RW, 'recompute_rewrite')
343 |         except ImportError:
344 |             rw_ok = False
345 |         if not rw_ok and not DRY:
346 |             stop('残差の書き換えの器（tools/bl3_recompute_rewrite.py の recompute_rewrite）を import できない')
347 |         guard.remove()
348 |         chk = {'cells': {k: {'prompt_len': len(c.prompt), 'main_position': c.mp, 'readout_position': c.ro, 'family': c.fam, 'set_ids': c.set_ids} for k, c in cells.items()},
349 |                'cell_signs': len(sets), 'passes': n_pass, 'recompute_rows': len(rows_rc), 'recompute_passes_per_path': n_rc, 'gate_rows': len(rows_gate),
350 |                'secondary': dict(cnt, cells=len(sec_rows), letter_token_is_L=sum(1 for c in ctx if c[3]['letter_token_is_L']), max_ids=max(c[3]['n_ids'] for c in ctx)),
351 |                'hook_register_remove': True, 'rewrite_importable': rw_ok, 'forward_calls': 0}
352 |         write_json(os.path.join(od, 'check.json'), chk)
353 |         mark('check', cell_signs=len(sets), passes=n_pass, recompute_rows=len(rows_rc), gate_rows=len(rows_gate), secondary_contexts=len(ctx), rewrite_importable=rw_ok)
354 |         return finish()
355 | 
356 |     # ---- 8. 走らせる器（DRY は合成の方向と読み取りの集合の行を置き直した乱数の模型）
357 |     if DRY:
358 |         iso_n = int(os.environ.get('OP4B_DRY_ISO', '9') or 9)
359 |         names = {'named': list(names_real['named']), 'B_random': list(names_real['B_random']), 'iso': names_real['iso'][:iso_n], 'real': list(names_real['real']), 'check': ['check']}
360 |         dirs = DR.synth_dirs(cfg.hidden_size, names['named'] + names['B_random'] + names['iso'] + names['real'] + names['check'])
361 |         DR.calibrate_readout_rows(model, BR.Runner(model, T3, L, coef, dirs), cells[cell_keys[0]], FJ)
362 |     else:
363 |         iso_n = None
364 |         dirs, names = dirs_real, names_real
365 |     R = BR.Runner(model, T3, L, coef, dirs)
366 |     TOOL_ERR = (BR.ToolError, SystemExit, AssertionError)
367 | 
368 |     # ---- 9. 相 pilot
369 |     if PHASE == 'pilot':
370 |         B = FJ['facts']['B']['cells']
371 |         stage_b_rate = {k: B[k]['catastrophe'] / B[k]['n_ok'] for k in cell_keys}
372 |         variants = collections.OrderedDict((k, v['ids']) for k, v in FJ['facts']['A']['variants'].items() if v.get('boundary_ok'))
373 |         try:
374 |             rec = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
375 |         except TOOL_ERR as e_:
376 |             rec = {'tool_error': str(e_), 'n_forward': R.n_forward}
377 |         write_json(os.path.join(od, 'pilot.json'), {'pilot': rec, 'variants_used': list(variants), 'clause': CLAUSE})
378 |         if 'tool_error' in rec:
379 |             finish({'tool_error': rec['tool_error']})
380 |             stop('器の誤りで下見が止まった（正本 pilot.decision.tool_error・直してやり直すかは登録者の裁定）: %s' % rec['tool_error'])
381 |         dec = rec['decision']
382 |         mark('pilot', q1=dec.get('q1'), dropped=dec.get('dropped'), batch=rec.get('batch'), floor=rec.get('floor'), cache_tol=rec.get('cache_tol'),
383 |              shortcut=(rec.get('v') or {}).get('shortcut'), n_forward=R.n_forward)
384 |         return finish()
385 | 
386 |     # ---- 10. 相 main（組ごとに出力を置く）
387 |     if DRY:
388 |         pilot = json.load(open(os.environ['OP4B_DRY_PILOT'], encoding='utf-8'))['pilot']
389 |     else:
390 |         pilot = FR['main_freeze']['pilot']
391 |     if pilot.get('tool_error') or (pilot.get('decision') or {}).get('stop'):
392 |         stop('凍結の記録の下見の記録が「止める」か器の誤り（本の計算は走らせない）')
393 |     dropped = list((pilot.get('decision') or {}).get('dropped', []))
394 |     first_cell = [cells[k] for k in cell_keys if k not in set(dropped)][0]
395 |     SESSION['pilot_used'] = {k: pilot.get(k) for k in ('batch', 'floor', 'cache_tol')}
396 |     SESSION['pilot_used'].update({'shortcut': (pilot.get('v') or {}).get('shortcut'), 'dropped': dropped})
397 |     SESSION['parts'] = parts
398 |     for part in parts:
399 |         mark('part', part=part)
400 |         out = collections.OrderedDict(part=part, clause=CLAUSE)
401 |         try:
402 |             if part != 'main':                       # どの組も頭で出口の値の自己検査（本の計算の組は run_main_phase の頭で行う）
403 |                 lc = R.logit_check(first_cell, T3['computation']['logit_tol'])
404 |                 out['logit_check'] = lc
405 |                 if not lc['pass']:
406 |                     raise BR.ToolError('出口の値の自己検査が落ちた（組 %s の頭）: %s' % (part, lc))
407 |             if part == 'main':
408 |                 MP = BR.run_main_phase(R, T3, FJ, cells, names, pilot, iso_n=None, log=say)
409 |                 out.update(MP)
410 |                 hd = MP['head']
411 |                 mark('main_head', logit_max_abs=hd['logit_check']['max_abs'], steered_cache_max_abs=(hd.get('steered_cache_check') or {}).get('max_abs'),
412 |                      shortcut=MP['shortcut'], layer_diff=hd['layer_check']['diff'], cell_signs=len(MP['cells']))
413 |             elif part == 'recompute':
414 |                 rows_rc, dbr = K.recompute_set(T3['main_rows'], pair_names, T3['nulls']['real']['swap_siblings'],
415 |                                                len(names['iso']), dropped)
416 |                 if DRY:
417 |                     rows_rc = pick_recompute_rows(rows_rc, int(os.environ.get('OP4B_DRY_RC', '2') or 2))
418 |                     dbr = collections.OrderedDict((r[0], dbr[r[0]]) for r in rows_rc)
419 |                 out['rows'] = rows_rc
420 |                 out['n_iso'] = len(names['iso'])
421 |                 t1 = time.time()
422 |                 out['hook'] = BR.recompute_hook_path(R, [(n, cells[ck], s) for n, ck, s in rows_rc], dbr, log=say)
423 |                 mark('recompute_hook', rows=len(rows_rc), seconds=round(time.time() - t1, 1))
424 |                 try:
425 |                     import bl3_recompute_rewrite as RW
426 |                 except ImportError:
427 |                     RW = None
428 |                 if RW is None:
429 |                     if not DRY:
430 |                         raise BR.ToolError('残差の書き換えの器を import できない')
431 |                     out['rewrite'] = None
432 |                     mark('recompute_rewrite', skipped='DRY で器が無い')
433 |                 else:
434 |                     t1 = time.time()
435 |                     # mask の組み方を、本の器のフックの道の近道なし（use_cache=False・明示の mask）にそろえる（個体の開発の記録 `records/Bl3/tools/recompute-rewrite-dev-Bl3.md`）
436 |                     out['rewrite'] = RW.recompute_rewrite(model, tok, T3, FJ, rows_rc, dbr, dirs, L, coef, use_cache=False)
437 |                     mark('recompute_rewrite', rows=len(rows_rc), seconds=round(time.time() - t1, 1))
438 |             elif part == 'secondary':
439 |                 AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
440 |                 rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader(REPO))
441 |                 sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
442 |                 ctx = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
443 |                 if DRY:
444 |                     n_sec = int(os.environ.get('OP4B_DRY_SEC', '2') or 2)
445 |                     firsts = [c for i, c in enumerate(ctx) if i == 0 or c[0] != ctx[i - 1][0]]
446 |                     ctx = firsts[:n_sec]
447 |                 out['rows_by_cell'] = sec_rows
448 |                 out['counts'] = AZ.secondary_counts(FB, sec_rows)
449 |                 t1 = time.time()
450 |                 out['contexts'] = BR.run_secondary(R, ctx, sec_rows, log=say)
451 |                 mark('secondary', contexts=len(ctx), seconds=round(time.time() - t1, 1))
452 |         except TOOL_ERR as e_:
453 |             out['tool_error'] = str(e_)
454 |         out['n_forward'] = R.n_forward
455 |         write_json(os.path.join(od, '%s.json' % part), out)
456 |         if 'tool_error' in out:
457 |             finish({'tool_error': out['tool_error'], 'tool_error_part': part})
458 |             stop('器の誤りで組 %s が止まった（正本 computation.tool_error・結果を開かずに登録者に上げる）: %s' % (part, out['tool_error']))
459 |     return finish()
460 | 
461 | 
462 | if __name__ == '__main__':
463 |     try:
464 |         run()
465 |     except SystemExit:
466 |         raise
467 |     except Exception:
468 |         LOG.append({'step': 'crash', 'at': now(), 'traceback': traceback.format_exc()[-4000:]})
469 |         say('[boot_Bl3] 予期しない誤りで止まった（器の誤りではない・登録者に相談）')
470 |         raise
```
<<< 終: `tools/colab/boot_Bl3.py` >>>
