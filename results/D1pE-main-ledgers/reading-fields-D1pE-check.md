# 英語の送る文の登録（D1′E）の試行の記録の読み取りの欄の表と、その照らし（2026-10-18 17:10:18 日本時間・スクリプト `E/E6/build_stage_ja_v10.py` v0.8）

- 何か: 本番の実行の試行の記録（伏せた記録を開けたときに開けた 12 のセルの `trials-*.jsonl`）から、スクリプトで読み取りの欄だけを抜いた表 `reading-fields-D1pE.jsonl`（9,600 行・一行が一つの試行・SHA-256 3592B55E2EBE68975561ADBEC4A64A4115FDAC4D439053628FBF586AB4AC66FA）。
- 抜いた欄: `cell`（機種の識別子|場面）と、試行の記録の `run_key`・`model`・`scenario`・`arm`・`trial_id`・`trial_index`・`block`・`arm_index`・`status`・`choice`・`catastrophe`・`primary`・`refuse_class`・`format_fail`・`format_retry_used`・`first_parsed`・`truncated`。
- 入れていない欄: 費用の見込み・呼び出しの識別子・応答の頭の一部・返った機種の名・トークンの数・時刻・process の識別子・送った文と素材とスクリプトの SHA16 など（試行の記録の 74 の欄のうち、上の欄のほか）。
- 元の記録の照らし: 各セルの試行の記録の SHA-256 を、伏せた記録を開ける前に書いた一覧（内部の記録 `E/E2/preopen-en-E2.json`・SHA-256 F9DC7936962F2A1B2694F00FBF495413787B04E173799CA1829D950C7BCF1A5E・この一覧の SHA-256 は `records/E/preopen-sha256-E2.txt` にあり、一覧の本文は `records/E/stamped/E/E2/preopen-en-E2.json`）と照らしてから読んだ。
- 公開の集計との照らし: 凍結した集計のスクリプトの数え方（`records/E/stamped/D1pE/d1pe_confirm.py` の `counts`）と同じ数え方で、この表からセル × 条件ごとの数を組み直し、公開の集計の json（`records/D1pE/confirm/confirm-D1pE.json`・SHA-256 B42F0DA2F60D8D82B2381FC6A36BFC745229DD40E7DDEB35179A2462981FB168・公開の SHA の記録と同じ）の同じセルと条件の数と照らした。照らした数は `n_trials`・`api_error`・`skipped`・`n_ok`・`catastrophe`・`refuse`・`format_out`・`format_out_p1`・`format_out_p2`・`truncated`・`format_retry`・`nonchoice`・`answered`・`nc_answer` の 14 の欄で、48 のセル × 条件のすべてで等しかった。
- この表で照らしていない公開の数: `truncated_first`・`loop`・`finish`・`content_filter`・`api_error_kinds`・`fingerprints`・`multi_fence`（この表に入れていない欄から数える物。`multi_fence` は、応答の本文の記録から数え直せる）。
- 答えの採点は、応答の本文の記録（同じ置き場の `raw-*.jsonl`）と凍結した採点のスクリプトで、読み手が組み直せる（置き場の README）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
