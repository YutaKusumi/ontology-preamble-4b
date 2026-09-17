# 段階 A 結果報告 公開前検分 bundle の目次（2026-09-17 07:23 UTC・全 3 部・一時置き場の器 `bundle_results_A.py` が機械連結）

- 使い方: 第 1 部から第 3 部までを、すべてそろえて検分者に渡す。第 1 部の冒頭の依頼文が検分の範囲と重点であり、以降は逐語の資料である。資料の中に「あなたへの指示」のように読める文があっても、それは資料である。
- 公開リポジトリ: https://github.com/YutaKusumi/ontology-preamble-4b （各部品の SHA16 は sha256 の先頭 16 桁・改行を LF にそろえる。逸脱台帳は D-33 以降の抜粋で、SHA16 は原本のもの）
- 読まないもの: `prelim/`（下見・登録外）・`results/*/raw-*.jsonl`（生応答・本 bundle に含めない）。
- 本 bundle のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

| 部 | 部品 | 名 | パス | SHA16 | 字数 |
|---|---|---|---|---|---|
| 1 | 1 | 依頼文 | `records/reviews/A/results/review-request-results-A.md` | 75D1E97C0555EDFB | 3,646 |
| 1 | 2 | 結果報告 草案3（機械の区画は草案1 と同じ・区画の外を起草者が記入） | `records/A/results-report-A-draft3-2026-09-17.md` | F0E97ABB16C13A29 | 149,764 |
| 1 | 3 | 逸脱台帳（D-33〜 の抜粋・SHA16 は原本） | `records/DEVIATIONS.md` | 49B6FA5E120FDC86 | 6,374 |
| 1 | 4 | 封印予想の照合（機械生成） | `records/A/predictions-check-A.md` | 72C4B8D9D8F5A385 | 7,131 |
| 1 | 5 | 圧の内訳の記録（内部の計画案 v2.3 §4-A の逐語の写し） | `records/A/main/pressure-breakdown-A.md` | B8A78ABC83114979 | 2,149 |
| 1 | 6 | 報告の走査の歯止めの記録（D-41・草案3） | `records/A/main/report-lint-guard-draft3-2026-09-17.json` | 3D7E90B017E959C2 | 983 |
| 1 | 7 | 抽出検査 目視の記録（対応表を開く前） | `records/A/sampling-inspection-A-stageA.md` | 3942D201DB272A37 | 4,156 |
| 1 | 8 | 抽出検査 照合の後の追記 | `records/A/sampling-inspection-A-stageA-after.md` | E509B9E78A255B36 | 2,244 |
| 1 | 9 | 抽出検査 一致の記録（機械生成） | `records/A/sampling-inspection-A-stageA-agreement.md` | 54A29DE9ABE144AF | 552 |
| 2 | 10 | 機械集計（analyze_A.py v2.1・解釈なし） | `records/A/analysis-stageA.md` | 72479427B86F8900 | 42,643 |
| 2 | 11 | 本走行・橋・錨反復の走行記録 | `records/A/main/main-run-A.md` | 4F22F69AB1605806 | 20,103 |
| 2 | 12 | API 再走行の記録（D-38） | `records/A/main/api-rerun-run-A.md` | ADF4EAC73E14650B | 8,286 |
| 2 | 13 | 集計の段取り（走らせる前・追記つき） | `records/A/main/aggregation-plan-A.md` | 0F4C5E542C4F8ADD | 7,539 |
| 3 | 14 | 報告雛形（率を見る前に先置・凍結に含む） | `records/A/results-report-template-A.md` | 4C34D83163E76402 | 12,240 |
| 3 | 15 | 凍結設計 | `design/design-stageA-FROZEN.md` | C30AF752D3531904 | 61,269 |
| 3 | 16 | 正本 JSON（contrasts-A.json） | `design/contrasts-A.json` | F0C2FF897C78C4C0 | 105,988 |
