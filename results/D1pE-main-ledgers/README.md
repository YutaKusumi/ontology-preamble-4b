# 英語の送る文の登録（D1′E）の本番の実行の答えの記録

- 何か: 段階 D の英語の送る文の登録の本番の実行（2026-10-12〜13）で、実行のスクリプトが伏せた置き場に書いた記録（記録では「封の台帳」）のうち、段階 E で伏せた記録を開けたとき（2026-10-14）に開けた物から置いた二つの物です。
  1. **応答の本文の記録**（`raw-*.jsonl`）: 12 のセル（機種 × 場面）ごとに一つ、元のバイトのまま。
  2. **試行の記録の読み取りの欄の表**（[`reading-fields-D1pE.jsonl`](reading-fields-D1pE.jsonl)）: 12 のセルの試行の記録（`trials-*.jsonl`）から、読み取りの欄だけを抜いた表。費用の見込みと呼び出しの記録（呼び出しの識別子・応答の頭・時刻など）は入れていません。抜いた欄と、公開の集計の数との照らしは [`reading-fields-D1pE-check.md`](reading-fields-D1pE-check.md) にあります。
- そのままの出力で、検証のためだけに置きます（CC BY 4.0・置き場の頭の `LICENSE`）。応答の本文は機種の出力で、AI の自己報告ではありません。
- 結果の報告の添え書き（`records/D1pE/README-D1pE.md`・2026-10-13）は、伏せた記録を公開しない物に挙げました。段階 E で、登録者が、この二つを論文の公開とともに置くと決めました（2026-10-14 と 2026-10-18）。
- この頁には、検定の族ごとの判定ラベルの件数を置きません。日本語の送る文の登録の記録（`results/D1p-main-ledgers/`）と、件数や率を並べて読みません（論文の節 2.9）。
- 機種と提供者の名は、どの機種を試したかを記すためだけに使います。各社の承認や推奨ではなく、各社との関係を示すものでもありません。
- 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

## 並び

- 応答の本文の記録は `<機種の置き場>/<実行の名>/raw-<機種名>.jsonl` です。実行の名は `D1pE-<機種の識別子>__<場面>__none__seed<種>` で、一つの実行が一つのセルです。機種名の「/」は「_」に替えてあります。
- 応答の本文の記録の一行は、一つの試行の答えの字です（`raw_output`。書式外で出し直したときは、二つの答えを `===RETRY===` でつないだ字で、二度目の答えは `raw_output_retry`）。ほかの欄は、試行の識別子（`trial_id`）・条件（`arm`）・答えの字の SHA16（`raw_sha`）・引用の禁止の一文（`clause`）です。
- 読み取りの欄の表の一行は、一つの試行です。`trial_id` で、応答の本文の記録の同じ試行とつながります。欄の意味は、実行のスクリプト `tools/run_preamble_api_d1pe.py` の `one` の関数のとおりです。英語の送る文の登録では、拒否の区別の欄（`refuse_class`）は null です。

## 採点し直すとき

- 凍結した採点のスクリプト（`arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` の `parse_app_v2` と `is_catastrophic`）と、実行のスクリプトの採点の段（`one` の関数が呼ぶ `endpoint`・`refuse_class`）を、応答の本文の字に当ててください。採点するのは最後の試みの答えだけです（書式外で出し直したときは二度目の答え）。
- 集計の報告の数（`records/D1pE/confirm/confirm-D1pE.json`）は、試行の記録から、凍結した集計のスクリプト（`records/E/stamped/D1pE/d1pe_confirm.py`）で組みました。読み取りの欄の表から同じ数え方で組み直した数は、公開の集計のセル × 条件の数と等しいことを、置く前に照らしました（`reading-fields-D1pE-check.md`）。
- 数から判定ラベルまでの計算は、`tools/rerun/op4b_reproduce.py` で組み直せます（`tools/rerun/README.md` の 3）。

## 置いていない物

- 試行の記録そのもの（費用の見込みと呼び出しの記録を含むため・読み取りの欄の表に替えた）・費用の台帳・本番の前の試しの実行の記録・答えの終わり方の確かめの全文・読解の確かめの応答の本文・集約の経路を経由した較正の記録・英語の読解の確かめで外れた機種の応答の本文。

## SHA-256

応答の本文の記録の SHA-256 は、伏せた記録を開ける前に書いた一覧（`records/E/stamped/E/E2/preopen-en-E2.json`・その SHA-256 は、開ける前に push した `records/E/preopen-sha256-E2.txt` にある）の値と同じことを、置く前に照らしました。

| セル（機種の識別子\|場面） | 応答の本文の記録 | SHA-256 | バイト |
|---|---|---|---|
| deepseekflash\|S1 | `D1pE-deepseekflash/D1pE-deepseekflash__S1__none__seed188003/raw-deepseek-flash.jsonl` | BD69E054B5B58E36B2BD2C657D95716F0C84DF56C55DCE02D9EE0BE1CCB539F6 | 2146748 |
| deepseekflash\|S4 | `D1pE-deepseekflash/D1pE-deepseekflash__S4__none__seed188004/raw-deepseek-flash.jsonl` | EC58FABBC71EA4EDB182ECD05E0BBCB6CD7FE8D71434720E6ED5D2F1D13017E5 | 2280700 |
| gemini25flash\|N2 | `D1pE-gemini25flash/D1pE-gemini25flash__N2__none__seed188002/raw-gemini-2.5-flash.jsonl` | C5815FDFE7DB4A8E50EFF59E96A10F132D4ED518833BB5F04667098AAF8AE266 | 4347477 |
| grok420nr\|S1 | `D1pE-grok420nr/D1pE-grok420nr__S1__none__seed188003/raw-grok-4.20-0309-non-reasoning.jsonl` | DDF7427B280271446A0E9BF57B67632B9FA4522FADE898FA27FADF894F3D00C3 | 1291153 |
| kimik3-m\|S1 | `D1pE-kimik3-m/D1pE-kimik3-m__S1__none__seed188003/raw-kimi-k3.jsonl` | 8D0CEFBF7CE1A94BAF80D6F3D4B0F94E797CCE87BAAAD60F00EEA83E3E6370DC | 2068431 |
| kimik3-m\|S4 | `D1pE-kimik3-m/D1pE-kimik3-m__S4__none__seed188004/raw-kimi-k3.jsonl` | 83BE5B6758F551DB0F6F5EB85AC53673560DA37D5EF7DEA31EFE5E3C7232C187 | 2027099 |
| kimik3-m\|SK | `D1pE-kimik3-m/D1pE-kimik3-m__SK__none__seed188005/raw-kimi-k3.jsonl` | 983DC6557CB0F5E17626F38C024DDCC3FFBF6CA5BE12BC0493BA4B2B4E39E179 | 2079935 |
| llama4scout\|S1 | `D1pE-llama4scout/D1pE-llama4scout__S1__none__seed188003/raw-meta-llama_Llama-4-Scout-17B-16E-Instruct.jsonl` | BF2EF9BA984DAE46D388C3341CE34943DC37F8582D191A47135022435B74846F | 1757591 |
| llama4scout\|S4 | `D1pE-llama4scout/D1pE-llama4scout__S4__none__seed188004/raw-meta-llama_Llama-4-Scout-17B-16E-Instruct.jsonl` | DE99F028468C9DEB4F2085E32B7A47EC6EA585F69F946D1262F2976AD785B6B8 | 1746228 |
| llama4scout\|SK | `D1pE-llama4scout/D1pE-llama4scout__SK__none__seed188005/raw-meta-llama_Llama-4-Scout-17B-16E-Instruct.jsonl` | 938BCC3C17AA9739AE2CF9EEAAE160076079E2AF4520A94451E1C9F2FE444F03 | 1820909 |
| mistrallarge3-m\|S4 | `D1pE-mistrallarge3-m/D1pE-mistrallarge3-m__S4__none__seed188004/raw-mistral-large-2512.jsonl` | 32EC2D7EDD7A4FFB37CA49535E7A5D1C270270C4E7E5C688D4A9671E97BB81DA | 1565298 |
| mistrallarge3-m\|SK | `D1pE-mistrallarge3-m/D1pE-mistrallarge3-m__SK__none__seed188005/raw-mistral-large-2512.jsonl` | 8F302951482357CD4C9BFDF6A932E5CAF103F8A28F7597816FB09068B554A24D | 1590553 |

| 読み取りの欄の表と照らしの記録 | SHA-256 |
|---|---|
| `reading-fields-D1pE.jsonl` | 3592B55E2EBE68975561ADBEC4A64A4115FDAC4D439053628FBF586AB4AC66FA |
| `reading-fields-D1pE-check.md` | EB38C1C2707102F82768481B31B4B097E62E0ADEB19FD648E6F86370E17E8055 |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
