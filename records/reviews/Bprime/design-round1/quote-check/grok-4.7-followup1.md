# 引用の機械の確かめ（grok-4.7-followup1・B′ の設計の巡・一巡目・非公開）

- 器: `check_quotes.py` v0。票: `votes/grok-4.7-followup1/response.md`（SHA16 CDE16B1EDE2953C9・6259 字）。草案2: `kit/design-Bprime-draft2.md`（SHA16 D9A0E2320E4D8BAE）。
- 「」の組の数: 30（閉じていない「 の残り: 0）。うち「引用」の語が同じ行の前にある正式の引用: 5。
- 分け方の数（全部）: A 6・B 0・C 17・D 7。正式の引用だけ: A 2・B 0・C 2・D 1。
- A＝草案2 に一字違わずある／B＝太字の印と逆引用符を除けばある／C＝束のほかのファイルに一字違わずある／D＝どこにも一字違わずは無い。合わない引用は印を付けるだけで、指摘を捨てる理由にはしない（枠）。
- 引用の本文は長いものを頭 40 字と尻 30 字に切って見せる（改行は ⏎）。

| # | 票の行 | 正式 | 字数 | 分け | どこに | 引用 |
|---|---|---|---|---|---|---|
| 1 | 11 |  | 128 | C | reference/design-Bl3-FROZEN.md | 帯の理由: 段階 B の帯は主位置から生成した全ての位置に掛かり、JSON 直答 … せるため（主位置だけに掛ける形は採らない・裁定 D212）。 |
| 2 | 15 |  | 121 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 段階 B の帯は主位置から生成した全ての位置に掛かり、JSON 直答の出力では、 … わせるため（主位置だけに掛ける形は採らない・裁定 D212） |
| 3 | 23 |  | 11 | D | 草案2 の中の最も長い一致 4 字／11 字（草案2 の 57 行目から） | 同じ問いの追試に見える |
| 4 | 23 |  | 15 | D | 草案2 の中の最も長い一致 5 字／15 字（草案2 の 4 行目から） | 層三の位置の範囲にそろえるため |
| 5 | 25 |  | 39 | C | reference/contrasts-Bl3.json | 加減の帯は主位置から EOS まで（段階 B の正本 `decisions`） |
| 6 | 25 |  | 31 | A | 草案2 の 19 行目 | この登録は、方向を加減したときの Gemma の行動を測らない |
| 7 | 29 |  | 21 | A | 草案2 の 63 行目 | 係数＝層三の比 ÷（‖v̂‖ ÷ ‖h‖） |
| 8 | 29 |  | 25 | D | 草案2 の中の最も長い一致 8 字／25 字（草案2 の 65 行目から） | 係数が大きいと残差に対する押しが層三より大きくなる |
| 9 | 33 |  | 62 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 本物の模型の領域では、足す量の一成分が残差の大きな次元で bf16 の刻みに丸められ、実効の加減の大きさが方向ごとに違いうる |
| 10 | 33 |  | 8 | A | 草案2 の 191 行目 | 区別できなかった |
| 11 | 35 |  | 7 | D | 草案2 の中の最も長い一致 3 字／7 字（草案2 の 14 行目から） | 予め置いた区間 |
| 12 | 66 |  | 77 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 近道の許容（`pilot.cache_tol_rule`）と揺れの床の和（効き目の差の最大が許容の内かを記録と報告に使う・判定は札の一致・裁定 D234） |
| 13 | 70 |  | 81 | C | reference/design-Bl3-FROZEN.md | 許容は近道の許容（`pilot.cache_tol_rule`）と揺れの床の和（ … の内かを記録と報告に使う・判定は札の一致・裁定 D234）。 |
| 14 | 72 |  | 5 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 近道の許容 |
| 15 | 72 |  | 132 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 近道の許容＝揺れの床（`pilot.checks.vi.floor_rule`） … 、上限 `pilot.noise_max` で頭打ちにした値 |
| 16 | 76 |  | 10 | D | 草案2 の中の最も長い一致 3 字／10 字（草案2 の 154 行目から） | 分岐が実際に使われた |
| 17 | 80 |  | 70 | C | reference/results-Bl3-FINAL-head.md | 独立の再計算の行 7（v̂ の行）・Nk の行 7 は計算し直していない・一段目の差の最大 3.71e-06・本の計算のバッチの大きさ 1。 |
| 18 | 82 |  | 10 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md・reference/results-Bl3-FINAL-head.md | この結果が退けた説明 |
| 19 | 84 |  | 68 | C | reference/results-Bl3-FINAL-head.md | 二段目は、正本の注のとおり、本の計算がバッチ一のときは二つの道が同じ計算になる形だけの確かめだった（本の計算のバッチの大きさは §4）。 |
| 20 | 88 |  | 75 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 升目の間の最大が `pilot.noise_max` を超えたら、本の計算はバッチの大きさを一にし、下見の (i)〜(v) もバッチ一の出力で計算する |
| 21 | 90 | 正式 | 7 | D | 草案2 の中の最も長い一致 3 字／7 字（草案2 の 154 行目から） | 実際に使われた |
| 22 | 90 | 正式 | 9 | C | reference/design-Bl3-FROZEN.md・reference/results-Bl3-FINAL-head.md | バッチの大きさ 1 |
| 23 | 94 |  | 20 | D | 草案2 の中の最も長い一致 8 字／20 字（草案2 の 177 行目から） | 必ず、読み取りの効き目の棒が層三より低い |
| 24 | 96 |  | 25 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 実在の差の方向は八腕の差で、高々七次元の空間を張り |
| 25 | 96 |  | 10 | C | records/cost-pilot-record-2026-09-29.md | 隠れの次元 5376 |
| 26 | 98 |  | 3 | A | 草案2 の 198 行目 | 低い棒 |
| 27 | 98 |  | 26 | C | reference/contrasts-Bl3.json・reference/design-Bl3-FROZEN.md | 偏りのある残差の中では、等方のランダム方向は低い棒で |
| 28 | 102 | 正式 | 8 | A | 草案2 の 10 行目 | 答えられないこと |
| 29 | 102 | 正式 | 6 | A | 草案2 の 38 行目 | 先に書く弱点 |
| 30 | 102 | 正式 | 6 | C | reference/design-Bl3-FROZEN.md | 書かないこと |

- 書いた時刻: 2026-09-29 19:15:43（日本時間）。

## この確かめが確認していないこと

- 引用が指摘の中身を正しく支えているか（字が合うことと、読みが正しいことは別）。
- D の引用が、言い換え・要約・読み違いのどれか（人が読んで決める）。
- 「」が引用ではなく語の名として使われたもの（A になっても引用の検査ではない）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
