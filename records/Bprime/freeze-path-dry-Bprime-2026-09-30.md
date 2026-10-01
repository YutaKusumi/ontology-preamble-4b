# B′ の合成データの確かめの五（凍結と錠の道）の記録（機械生成・`tools/dry_run_Bprime.py` v0.9・2026-09-30 23:17 日本時間）

- 走らせた置き場: 公開の置き場の凍結の層（tools・design・arms・records・results/dirB）と、移した形の一時の置き場を重ねた一時の git の置き場。**実の重みは読まない**。合成の値と書き換えは行ごとに書いた。
- 読んだ合成データの正式の記録: `records/Bprime/dry-run-Bprime-2026-09-30.md`（SHA16 29BD12C9DAE39067）。五は 1308 秒。
- 確かめ: 27 のうち 27 が期待どおり。

| 部 | 確かめ | 結果 | 値 |
|---|---|---|---|
| 五 | 公開の形の git の置き場 | 期待どおり | 78e96d405b0c |
| 五 | 凍結の本文を組む | 期待どおり | [make_frozen_Bprime] design/design-Bprime-FROZEN.md（SHA16 A7D17D55DB3D596C）・records/Bprime/numbers-lint-FROZEN-Bprime.md・records/Bprime/frozen-diff-Bprime.md |
| 五 | 予想の書式を組む | 期待どおり | [make_predictions_form_Bprime] records/predictions/predictions-form-Bprime-v1.html（欄 8・予想の欄 4） |
| 五 | 下見の前の凍結（合成の Colab の確かめ・凍結の器の確かめをすべて通す・43.7 秒） | 期待どおり | on": "highest",    "attn_implementation": "sdpa"   },   "attn_implementation": "sdpa",   "pins": {    "transformers": "5.16.1",    "torch": "2.11.0+cu128",    "numpy": "合成"   }  } } [freeze_Bprime] 下見の前の凍結を記帳した: records/Bprime/FREEZE-RECORD-Bprime.json・records/Bprime/FREEZE-RECORD-Bprime.md（凍結物 104） |
| 五 | 封印（合成の予想・コーディネータが先） | 期待どおり | [seal_Bprime] コーディネータの予想を封印した: records/predictions/predictions-Bprime-coordinator.json・SHA-256 3E15F906FBA53BD8C4469220B891A2AB8C16D1E31DF1272F7A24E689B863A7C0（登録者には SHA だけを伝える） |
| 五 | 錠が通る（相 extract） | 期待どおり |  |
| 五 | 錠が止まる（凍結物の SHA16 の違い） | 期待どおり |  |
| 五 | 錠が止まる（台帳のつながらない差分） | 期待どおり |  |
| 五 | 錠が止まる（予想の SHA の違い） | 期待どおり |  |
| 五 | 錠が止まる（暦の期限・今の時刻を与える口） | 期待どおり |  |
| 五 | 錠が止まる（本の凍結が無い） | 期待どおり |  |
| 五 | 錠が止まる（閉じた記録・U16） | 期待どおり |  |
| 五 | 相 extract（等方 1999・起動の記録と出力の SHA の記録をコミット・15.3 秒） | 期待どおり |  |
| 五 | 相 behavior と閉じた記録（系統外の採点は合成の失敗の理由で閉じる・78.7 秒） | 期待どおり |  |
| 五 | 相 pilot（閉じた記録を照らして進む・22.1 秒） | 期待どおり |  |
| 五 | 本の凍結（DRY でない形の写しの下見の出力・0.9 秒） | 期待どおり | 13D555225AB",   "predictions_sha256": {    "coordinator": "3E15F906FBA53BD8C4469220B891A2AB8C16D1E31DF1272F7A24E689B863A7C0",    "registrant": "2127304B0BC1FFB3558DB3CD74BDA3823035BBE7600F5A8AABDF38D10D88C9A6"   }  } } [freeze_Bprime] 本の凍結を記帳した: records/Bprime/FREEZE-RECORD-Bprime.json（読み取りの下見の試み 1） |
| 五 | 錠が通る（相 main・本の凍結の節の SHA16） | 期待どおり |  |
| 五 | 錠が止まる（本の凍結の節の書き換え・U10） | 期待どおり |  |
| 五 | 相 main の組 main（等方 1999・327.7 秒） | 期待どおり |  |
| 五 | 相 recompute の組 hook（等方 1999・408.0 秒） | 期待どおり |  |
| 五 | 相 recompute の組 rewrite（等方 1999・362.4 秒） | 期待どおり |  |
| 五 | 相 recompute の組 reextract（等方 1999・14.3 秒） | 期待どおり |  |
| 五 | 組ごとに違うコミット（集計は中身で照らす・U08） | 期待どおり | ['0ad8524be1dc', 'daf15ad95b97', 'f2c765a87720', '3069cfdeb96a'] |
| 五 | 一致だけを見る段（DRY でない枝・--freeze・錠と本の凍結の照らしを通る） | 期待どおり | [analyze_Bprime] 一致だけを見る段: 一致 True（一段目 True・二段目 True・再抽出 True）・理由 None |
| 五 | 結果を開く段（DRY でない枝・走行の表を照らす・U04） | 期待どおり | [analyze_Bprime] 結果を開く段: 書いた analysis-Bprime.json（SHA16 5F7EABF1D4FA1F4A） |
| 五 | 報告の本番の入口（錠・走行の表を読み直して照らす・走査の当たり零・U03・U04） | 期待どおり | [build_report_Bprime] 書いた results-Bprime.md（行 435・走査の当たり 0） |
| 五 | 書き換えの記録（DRY でない形にした写し・合成の値） | 期待どおり | extract : session の dry を偽に・commit を d5fba9178812 に・behavior : session の dry を偽に・commit を 120745e38883 に・pilot: 升目の質量と確率を正本の門を満たす合成の値に・(i)(ii) と決定とバッチを凍結の芯で出し直した（決定 続ける・バッチ 16）・出力の SHA の記録を合わせた・pilot : session の dry を偽に・commit を b12f63919db8 に・main main: session の dry を偽に・commit を 0ad8524be1dc に・recompute hook: session の dry を偽に・commit を daf15ad95b97 に・recompute rewrite: session の dry を偽に・commit を |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
