# 日本語の送る文の登録（D1′）の本番の実行の答えの記録

- 何か: 段階 D の日本語の送る文の登録の本番の実行（2026-10-10）で、実行のスクリプトが伏せた置き場に書いた記録（記録では「封の台帳」）のうち、段階 E で伏せた記録を開けたとき（2026-10-14）に開けた物から置いた二つの物です。
  1. **応答の本文の記録**（`raw-*.jsonl`）: 29 のセル（機種 × 場面）ごとに一つ、元のバイトのまま。
  2. **試行の記録の読み取りの欄の表**（[`reading-fields-D1p.jsonl`](reading-fields-D1p.jsonl)）: 29 のセルの試行の記録（`trials-*.jsonl`）から、読み取りの欄だけを抜いた表。費用の見込みと呼び出しの記録（呼び出しの識別子・応答の頭・時刻など）は入れていません。抜いた欄と、公開の集計の数との照らしは [`reading-fields-D1p-check.md`](reading-fields-D1p-check.md) にあります。
- そのままの出力で、検証のためだけに置きます（CC BY 4.0・置き場の頭の `LICENSE`）。応答の本文は機種の出力で、AI の自己報告ではありません。
- 凍結した本文（`records/D1p/00-frame-D1p.md` の §8）は、伏せた記録の公開を、登録者の決めで後に行うとしました。段階 E で、登録者が、この二つを論文の公開とともに置くと決めました（2026-10-14 と 2026-10-18）。
- この頁には、検定の族ごとの判定ラベルの件数を置きません。英語の送る文の登録の記録（`results/D1pE-main-ledgers/`）と、件数や率を並べて読みません（論文の節 2.9）。
- 機種と提供者の名は、どの機種を試したかを記すためだけに使います。各社の承認や推奨ではなく、各社との関係を示すものでもありません。
- 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

## 並び

- 応答の本文の記録は `<機種の置き場>/<実行の名>/raw-<機種名>.jsonl` です。実行の名は `D1p-<機種の識別子>__<場面>__none__seed<種>` で、一つの実行が一つのセルです。機種名の「/」は「_」に替えてあります。
- 応答の本文の記録の一行は、一つの試行の答えの字です（`raw_output`。書式外で出し直したときは、二つの答えを `===RETRY===` でつないだ字で、二度目の答えは `raw_output_retry`）。ほかの欄は、試行の識別子（`trial_id`）・条件（`arm`）・答えの字の SHA16（`raw_sha`）・引用の禁止の一文（`clause`）です。
- 読み取りの欄の表の一行は、一つの試行です。`trial_id` で、応答の本文の記録の同じ試行とつながります。欄の意味は、実行のスクリプト `tools/run_preamble_api_d.py` の `one` の関数のとおりです。

## 採点し直すとき

- 凍結した採点のスクリプト（`arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` の `parse_app_v2` と `is_catastrophic`）と、実行のスクリプトの採点の段（`one` の関数が呼ぶ `endpoint`・`refuse_class`）を、応答の本文の字に当ててください。採点するのは最後の試みの答えだけです（書式外で出し直したときは二度目の答え）。
- 集計の報告の数（`records/D1p/confirm/confirm-D1p.json`）は、試行の記録から、凍結した集計のスクリプト（`records/E/stamped/D1p/d1p_confirm.py`）で組みました。読み取りの欄の表から同じ数え方で組み直した数は、公開の集計のセル × 条件の数と等しいことを、置く前に照らしました（`reading-fields-D1p-check.md`）。
- 数から判定ラベルまでの計算は、`tools/rerun/op4b_reproduce.py` で組み直せます（`tools/rerun/README.md` の 3）。

## 置いていない物

- 試行の記録そのもの（費用の見込みと呼び出しの記録を含むため・読み取りの欄の表に替えた）・費用の台帳・本番の前の試しの実行の記録・答えの終わり方の確かめの全文・読解の確かめの応答の本文・集約の経路を経由した較正の記録・許諾で外した機種の記録。

## SHA-256

応答の本文の記録の SHA-256 は、伏せた記録を開ける前に書いた一覧（`records/E/stamped/E/E2/preopen-ja-E2.json`・その SHA-256 は、開ける前に push した `records/E/preopen-sha256-E2.txt` にある）の値と同じことを、置く前に照らしました。

| セル（機種の識別子\|場面） | 応答の本文の記録 | SHA-256 | バイト |
|---|---|---|---|
| deepseekflash\|S1 | `D1p-deepseekflash/D1p-deepseekflash__S1__none__seed88003/raw-deepseek-flash.jsonl` | 2296F3A6B9F67AA06ADFB280BFF4EFB26DF1C6C310FCE68371E4F6B302485892 | 2534253 |
| deepseekflash\|SK | `D1p-deepseekflash/D1p-deepseekflash__SK__none__seed88005/raw-deepseek-flash.jsonl` | 09D3D293C905DC3866859EEA81C3E73C616B44DDDC3A25B70DD8139AB0E41B31 | 3524500 |
| deepseekv32-a\|S1 | `D1p-deepseekv32-a/D1p-deepseekv32-a__S1__none__seed88003/raw-deepseek-v3.2.jsonl` | 3C22BC441C95FC4F135BF935D23E9B52DE1FA273F22B73039D1755854373CA50 | 1611834 |
| deepseekv32-a\|S4 | `D1p-deepseekv32-a/D1p-deepseekv32-a__S4__none__seed88004/raw-deepseek-v3.2.jsonl` | 76D70AA3A0BE1A061E59EBE46D261729B70C448C7AFDB41FA927AB217BF1DAC8 | 1521139 |
| deepseekv32-a\|SK | `D1p-deepseekv32-a/D1p-deepseekv32-a__SK__none__seed88005/raw-deepseek-v3.2.jsonl` | CC0219442C6382D90D213F93023AB3149669FEBDC5BA9D1DDD4D529E0A7B2BAE | 1592747 |
| gemini25flash\|S1 | `D1p-gemini25flash/D1p-gemini25flash__S1__none__seed88003/raw-gemini-2.5-flash.jsonl` | 911D2BDFEE50B2491431CEBEEEA4FE5E0935853E47F52C7728DC9D1155F642CB | 2847574 |
| gemini25flash\|S4 | `D1p-gemini25flash/D1p-gemini25flash__S4__none__seed88004/raw-gemini-2.5-flash.jsonl` | D4B2D5EE9149E3AF4F0BA7BC57B158BA52C0E1D233E6E21CDBB819CA22DBBC16 | 2764757 |
| gemini25flash\|SK | `D1p-gemini25flash/D1p-gemini25flash__SK__none__seed88005/raw-gemini-2.5-flash.jsonl` | 9CABFEA316E43C37DD1C57A75B376C5C836B82A764947DE0022F607429805983 | 3046026 |
| grok420nr\|N2 | `D1p-grok420nr/D1p-grok420nr__N2__none__seed88002/raw-grok-4.20-0309-non-reasoning.jsonl` | F39780F2082B8E6F58A8F62FD0EEC8AD9687E4DD5FC1B2CCA153ECDFCA75D1D4 | 1884938 |
| grok420nr\|S1 | `D1p-grok420nr/D1p-grok420nr__S1__none__seed88003/raw-grok-4.20-0309-non-reasoning.jsonl` | D4D0C7700D923C745ABE484B07E19B0F32FC03CD07A4652F8728CB6C826090BD | 1346434 |
| grok420nr\|S4 | `D1p-grok420nr/D1p-grok420nr__S4__none__seed88004/raw-grok-4.20-0309-non-reasoning.jsonl` | 845778AFF4E92CBE15E34D949F220204A92655FE40E1027BFEEB01C890174D1F | 1376664 |
| grok420nr\|SK | `D1p-grok420nr/D1p-grok420nr__SK__none__seed88005/raw-grok-4.20-0309-non-reasoning.jsonl` | C61C3162DE438ED37C104BAAC5373954024141A7A7FD7441D98538E246651D16 | 1402564 |
| kimik3-m\|S1 | `D1p-kimik3-m/D1p-kimik3-m__S1__none__seed88003/raw-kimi-k3.jsonl` | 059A9C190586AAE80A03D6A22906CB56C2373920C9E0C3DEA29E8D0363CBDB53 | 2005941 |
| kimik3-m\|S4 | `D1p-kimik3-m/D1p-kimik3-m__S4__none__seed88004/raw-kimi-k3.jsonl` | 2A7E3395EAE8E0A55B1AA66152479B75674846A7FBCC1A0BAAEDF95F0BFC4AE9 | 1989500 |
| kimik3-m\|SK | `D1p-kimik3-m/D1p-kimik3-m__SK__none__seed88005/raw-kimi-k3.jsonl` | C51E0C7FBB3B279DBF315EFE4F06F4F384811D72FE645B11F79D270DAB237A06 | 1946208 |
| llama31-8b-n\|N1 | `D1p-llama31-8b-n/D1p-llama31-8b-n__N1__none__seed88001/raw-meta-llama_Llama-3.1-8B-Instruct.jsonl` | C7FB04EF5C4679C047DA47B8F5FA33C9824E12DF7DE35375975DCAEE3B043FDC | 1927413 |
| llama31-8b-n\|N2 | `D1p-llama31-8b-n/D1p-llama31-8b-n__N2__none__seed88002/raw-meta-llama_Llama-3.1-8B-Instruct.jsonl` | A846B2F4AC2CF9C14E5E17E76C26D430FD025A192D78EE41667489C5DFF2A19D | 2158341 |
| llama31-8b-n\|S1 | `D1p-llama31-8b-n/D1p-llama31-8b-n__S1__none__seed88003/raw-meta-llama_Llama-3.1-8B-Instruct.jsonl` | 7528290CF5864EB01AEEA8F7801A892EA4A4B9FB8198EBC4821E3F3BFA2CEDD7 | 2073777 |
| llama31-8b-n\|S4 | `D1p-llama31-8b-n/D1p-llama31-8b-n__S4__none__seed88004/raw-meta-llama_Llama-3.1-8B-Instruct.jsonl` | 41212F7FD6D4C3ED7D2FC042C7B73D41464066B8B61CD9F2A692B46A58591AE3 | 1933240 |
| llama31-8b-n\|SK | `D1p-llama31-8b-n/D1p-llama31-8b-n__SK__none__seed88005/raw-meta-llama_Llama-3.1-8B-Instruct.jsonl` | FAF6A43711D66F5BB2C1E55F336F2C2BE9E2D7B86A19D1D312503DEBD7D060AD | 1981990 |
| llama4scout\|N2 | `D1p-llama4scout/D1p-llama4scout__N2__none__seed88002/raw-meta-llama_Llama-4-Scout-17B-16E-Instruct.jsonl` | F76EDFB190608B74BC5B5C756A6A50744B6BBA42A6781D0C33FC05A1751CD9F4 | 1751144 |
| llama4scout\|S1 | `D1p-llama4scout/D1p-llama4scout__S1__none__seed88003/raw-meta-llama_Llama-4-Scout-17B-16E-Instruct.jsonl` | 8408C08037CF7728C86BFBA72FB3294D8B9E8FD133067F92A4826F3DC3AD168E | 2052735 |
| llama4scout\|SK | `D1p-llama4scout/D1p-llama4scout__SK__none__seed88005/raw-meta-llama_Llama-4-Scout-17B-16E-Instruct.jsonl` | FD2735AE306D799CDEBA086F2233FDE40EEF63D336035E60B0849C3AA4624CF9 | 1962549 |
| mistrallarge3-m\|S1 | `D1p-mistrallarge3-m/D1p-mistrallarge3-m__S1__none__seed88003/raw-mistral-large-2512.jsonl` | B04C230E408805BFC3FC97485D0025345C74131BD24DA6877B18CF53B8724011 | 1762744 |
| mistrallarge3-m\|S4 | `D1p-mistrallarge3-m/D1p-mistrallarge3-m__S4__none__seed88004/raw-mistral-large-2512.jsonl` | C40705AF6019BD1F395E37F1616FE68223B91EE7D6C29C3A14D45C582A6A21CD | 1729106 |
| mistrallarge3-m\|SK | `D1p-mistrallarge3-m/D1p-mistrallarge3-m__SK__none__seed88005/raw-mistral-large-2512.jsonl` | FF195BBB930CF3C7AC62F7CC3621D9B90548E55F60573EFEA2F56B0C9F0FCC30 | 1833354 |
| qwen25coder32b-n\|N2 | `D1p-qwen25coder32b-n/D1p-qwen25coder32b-n__N2__none__seed88002/raw-Qwen_Qwen2.5-Coder-32B-Instruct.jsonl` | 58080F2A29AB8433B203FEEA2C3DD22BD128320F8F2333DDD1AFBCDF94B96603 | 1894936 |
| qwen38max-a\|S1 | `D1p-qwen38max-a/D1p-qwen38max-a__S1__none__seed88003/raw-qwen3.8-max-0902.jsonl` | BAF09AC0BC529B4F18E7DA484913297719E16C3A4E43B2D2CE90D526C32B8170 | 3097703 |
| qwen38max-a\|S4 | `D1p-qwen38max-a/D1p-qwen38max-a__S4__none__seed88004/raw-qwen3.8-max-0902.jsonl` | ECD37017DFA5F8AD48D543596EF2FB1BE4361C5817E6C1C009AA487A4B5DFE93 | 3030955 |

| 読み取りの欄の表と照らしの記録 | SHA-256 |
|---|---|
| `reading-fields-D1p.jsonl` | 4A9067A726C294CA8DCA4F42A815D73B2635522EA8D15914F57AFA1375C59B62 |
| `reading-fields-D1p-check.md` | 310E7D21F28E6663B0EED6B0DAE026C62F05330B586A58E49164DB01DF1653A0 |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
