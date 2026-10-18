# 計算三の記録 v0.5（機種ごとの差の図・言語ごとに別・2026-10-15 19:04:31 日本時間・器 `E/E3/calc/calc3_model_figures.py` v0.5・SHA16 EEC38F08D1290D3A）

- 何か: 枠 §5 の計算三。登録の外の記述で、判定ラベルを替えない。入力は公開の二つの集計の出力（公開の SHA の記録と照らした）。
- 露出: 起草者は二つの集計の報告と最終版の値を前に見ている。図と表の値は集計の出力の値を写したもので、新しく計算した値は無い（三つ組の割合は数を割っただけ）。
- v0.5 の直し（三巡目の採否 3I-06・3I-08・3I-10・3I-20）: 注と印と字の大きさと × の置き方だけで、入力・値・区間・判定ラベルは v0.4 と同じ。
- 照らし: 入力の二つの集計の出力の SHA-256 を、公開の置き場の SHA の記録の行と照らした（合わなければ器が止まる）。
  - `records/D1p/confirm/confirm-D1p.json` F08238ED5B56A6DF24B8D2587CD43DB3C68B7EF793C038538AA7F9D207BEBDBD（照らした記録 `records/D1p/confirm/confirm-D1p-sha256.txt`）
  - `records/D1pE/confirm/confirm-D1pE.json` B42F0DA2F60D8D82B2381FC6A36BFC745229DD40E7DDEB35179A2462981FB168（照らした記録 `records/D1pE/confirm/confirm-D1pE-sha256.txt`）

| 言語の登録 | 機種 | 形 | セル |
|---|---|---|---|
| 日本語の送る文の登録 | Gemini 2.5 Flash | 図 | 3 |
| 日本語の送る文の登録 | grok-4.20（非推論） | 図 | 4 |
| 日本語の送る文の登録 | DeepSeek V3.2 | 図 | 3 |
| 日本語の送る文の登録 | deepseek-flash | 表（セルが 2 以下・D425-4） | 2 |
| 日本語の送る文の登録 | Llama 3.1 8B Instruct | 図 | 5 |
| 日本語の送る文の登録 | Llama-4-Scout-17B-16E-Instruct | 図 | 3 |
| 日本語の送る文の登録 | Mistral Large 3（2512） | 図 | 3 |
| 日本語の送る文の登録 | Kimi K3 | 図 | 3 |
| 日本語の送る文の登録 | Qwen2.5-Coder-32B-Instruct | 表（セルが 2 以下・D425-4） | 1 |
| 日本語の送る文の登録 | Qwen3.8 Max（0902） | 表（セルが 2 以下・D425-4） | 2 |
| 英語の送る文の登録 | Gemini 2.5 Flash | 表（セルが 2 以下・D425-4） | 1 |
| 英語の送る文の登録 | grok-4.20（非推論） | 表（セルが 2 以下・D425-4） | 1 |
| 英語の送る文の登録 | deepseek-flash | 表（セルが 2 以下・D425-4） | 2 |
| 英語の送る文の登録 | Llama-4-Scout-17B-16E-Instruct | 図 | 3 |
| 英語の送る文の登録 | Mistral Large 3（2512） | 表（セルが 2 以下・D425-4） | 2 |
| 英語の送る文の登録 | Kimi K3 | 図 | 3 |

- 出力の SHA-256:
  - `calc/calc3-v0.5/calc3-values-en.json` 77F4826D56CCE8F58D0D525E4B3E09548BA4B6FA464DCF476151175C49207051
  - `calc/calc3-v0.5/calc3-values-ja.json` 433AB306D4470B38C3A33651A7D20AE947C87AA501F7D8FC12921D7CC6E4E290
  - `calc/calc3-v0.5/en/fig-kimik3-m.png` 9589E4F01FB15CA7E36E4FD069B167E041FFBF14575003300E649D5395D00959
  - `calc/calc3-v0.5/en/fig-llama4scout.png` 2DD6ABF6B9DA807283D9956235591F11E65E46399A88B34E4DB7678B58ADBC05
  - `calc/calc3-v0.5/en/table-deepseekflash.md` 40767F8B4B67E1D2EF5016A529BE69D5780D61D07C10A756787FDFFF0D56C7FD
  - `calc/calc3-v0.5/en/table-gemini25flash.md` 0DD062A2F22AD0DE55E5B68387CD3E47D5FB58AF88937C640AE6AF7CB2362056
  - `calc/calc3-v0.5/en/table-grok420nr.md` 5696D45D6F5B9165943B88D7FC8DBCCDE577935E7D96976E1C627B0147CC62E2
  - `calc/calc3-v0.5/en/table-mistrallarge3-m.md` 9FBD817EA7F4C883EB1179C304DC261DF4595EE1EA4C1A07E1D492F55D6CE5E1
  - `calc/calc3-v0.5/ja/fig-deepseekv32-a.png` BFC81D62DCEE41A18608F1555014BA2FAB8830309D1A740123D7B63F32F7EF7B
  - `calc/calc3-v0.5/ja/fig-gemini25flash.png` AD9B28D613BCA84D26AFDCC528A5F26886582A78FC18C92C4392DD3C2A4C083B
  - `calc/calc3-v0.5/ja/fig-grok420nr.png` E47C4A414FA7201D12512BD31765BE227C350092D9AB203727A43A29B967926B
  - `calc/calc3-v0.5/ja/fig-kimik3-m.png` A15E13807660397ECF6F20FF5B7CF9D5E582C59D67F79EA663340A6718540EDD
  - `calc/calc3-v0.5/ja/fig-llama31-8b-n.png` C8242D28874747865318D0A9564BD36BE85AB3782FC5AA52B4A443DB6AED809B
  - `calc/calc3-v0.5/ja/fig-llama4scout.png` EEDBF551F6E35C31AECF0EFA5620654D73167786F31594F90539F602ECEB1562
  - `calc/calc3-v0.5/ja/fig-mistrallarge3-m.png` 9A49E2012584306CCC963E4681D96AA1747880C5DBFF18F3A03DA4A12A28CF8A
  - `calc/calc3-v0.5/ja/table-deepseekflash.md` 091B3B429A9708EB3F7769E01F20BED0CD121ACE79279AC4766DF89088C3C960
  - `calc/calc3-v0.5/ja/table-qwen25coder32b-n.md` 6A291087A05092255A3AC54A3E668DC65158A7CCE6608EA91E6FA95A667CEC5D
  - `calc/calc3-v0.5/ja/table-qwen38max-a.md` 892967E8652521D646B26E00FDF82CCBADA830139DA2AB0E22C2F8C1F6F9FEBD

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
