# 英語版 D1′E の較正の段のまとめ（2026-10-11 22:45:52 日本時間・器 `D1pE/d1pe_cal_summary.py` v0・内部・登録外・札なし）

- 枠 `D1pE/00-frame-D1pE-cal.md`（SHA16 5C21615162C7B43D）・刻印 `D1pE/frame-stamp-D1pE-cal.md`（SHA16 2155B5EAD23585A0）・設定 `D1pE/d1pe_config.py`（SHA16 97E953ECCF52E18D）・器のまとめ（SHA16 846BFDCD7AA0C8A2）。
- 機種の間に順位を付けない。率は機種ごとの記述（`describe-D1pEc-<鍵>.md`）にあり、このまとめには決めと場面だけを書く。答えの終わり方の確かめは合否だけ（裁定 D380-2）。

## 1. 読解の確かめ

| 機種 | 読み方 A | 読み方 B | A で読めない | API の誤り | 決め |
|---|---|---|---|---|---|
| Gemini 2.5 Flash | 1.0 | 1.0 | 0 | 0 | 通る（A） |
| Llama 3.1 8B Instruct | 0.72 | 0.7467 | 21 | 0 | 英語で問いを理解できない（外す） |
| Llama-4-Scout-17B-16E-Instruct | 1.0 | 1.0 | 0 | 0 | 通る（A） |
| Qwen2.5-Coder-32B-Instruct | 0.7733 | 0.7733 | 0 | 0 | 英語で問いを理解できない（外す） |
| grok-4.20（非推論） | 1.0 | 1.0 | 0 | 0 | 通る（A） |
| deepseek-flash | 1.0 | 1.0 | 0 | 0 | 通る（A） |
| Mistral Large 3（2512） | 1.0 | 1.0 | 0 | 0 | 通る（A） |
| Qwen3.8 Max（0902） | 1.0 | 1.0 | 0 | 0 | 通る（A） |
| Kimi K3 | 1.0 | 1.0 | 0 | 0 | 通る（A） |

## 2. 較正

| 機種 | 凍結の形式の決め | 使える場面 | 様式崩壊のある場面 | 代わりの形式 |
|---|---|---|---|---|
| Gemini 2.5 Flash | 本走行の候補 | N2 | なし | — |
| Llama-4-Scout-17B-16E-Instruct | 本走行の候補 | S1・S4・SK | なし | — |
| grok-4.20（非推論） | 本走行の候補 | S1 | なし | — |
| deepseek-flash | 本走行の候補 | S1・S4 | なし | — |
| Mistral Large 3（2512） | 本走行の候補 | S4・SK | なし | — |
| Qwen3.8 Max（0902） | 余地が無い（この素材では測れなかった） | なし | なし | — |
| Kimi K3 | 本走行の候補 | S1・S4・SK | なし | — |

## 3. 答えの終わり方の確かめ（合否だけ）

| 機種 | 確かめた場面 | 本走行に使う場面 | 出力の上限 | 決め |
|---|---|---|---|---|
| Gemini 2.5 Flash | N2 | N2 | 4096 | 本走行に進む |
|  | N2 | O 通る・OAmi 通る |  |  |
| Llama-4-Scout-17B-16E-Instruct | S1・S4・SK | S1・S4・SK | 4096 | 本走行に進む |
|  | S1 | O 通る・OAmi 通る |  |  |
|  | S4 | O 通る・OAmi 通る |  |  |
|  | SK | O 通る・OAmi 通る |  |  |
| grok-4.20（非推論） | S1 | S1 | 4096 | 本走行に進む |
|  | S1 | O 通る・OAmi 通る |  |  |
| deepseek-flash | S1・S4 | S1・S4 | 4096 | 本走行に進む |
|  | S1 | O 通る・OAmi 通る |  |  |
|  | S4 | O 通る・OAmi 通る |  |  |
| Mistral Large 3（2512） | S4・SK | S4・SK | 4096 | 本走行に進む |
|  | S4 | O 通る・OAmi 通る |  |  |
|  | SK | O 通る・OAmi 通る |  |  |
| Kimi K3 | S1・S4・SK | S1・S4・SK | 4096 | 本走行に進む |
|  | S1 | O 通る・OAmi 通る |  |  |
|  | S4 | O 通る・OAmi 通る |  |  |
|  | SK | O 通る・OAmi 通る |  |  |

## 4. 英語版の本走行の升（この段の決めのとおり）

- 升の数: 12（gemini25flash N2・llama4scout S1・S4・SK・grok420nr S1・deepseekflash S1・S4・mistrallarge3-m S4・SK・kimik3-m S1・S4・SK）。
- 機種ごとの状態: Gemini 2.5 Flash＝本走行に進む・Llama 3.1 8B Instruct＝読解の確かめ: 英語で問いを理解できない（外す）・Llama-4-Scout-17B-16E-Instruct＝本走行に進む・Qwen2.5-Coder-32B-Instruct＝読解の確かめ: 英語で問いを理解できない（外す）・grok-4.20（非推論）＝本走行に進む・deepseek-flash＝本走行に進む・Mistral Large 3（2512）＝本走行に進む・Qwen3.8 Max（0902）＝較正: 余地が無い（この素材では測れなかった）・Kimi K3＝本走行に進む。
- 外した機種（この段の前）: DeepSeek V3.2（Alibaba Cloud Model Studio（シンガポール）の頁から消え、2026-10-11 20:27 の出力 1 の確かめで HTTP 404 model_not_found（裁定 D381-2・`D1pE/probe-dsv32-D1pE.json`）。連なりは起こさない。）。

## 5. 日本語版の升との並べ（記述だけ・言語の効き目とは書かない・裁定 D364-3）

- 日本語版の本走行の升（九機種の分）: 26。英語版の升: 12。
- 両方の言語で窓に入った升（同じ機種・同じ場面）: 9（deepseekflash S1・grok420nr S1・kimik3-m S1・kimik3-m S4・kimik3-m SK・llama4scout S1・llama4scout SK・mistrallarge3-m S4・mistrallarge3-m SK）。
- 英語だけの升: 3（deepseekflash S4・gemini25flash N2・llama4scout S4）。日本語だけの升: 17（deepseekflash SK・gemini25flash S1・gemini25flash S4・gemini25flash SK・grok420nr N2・grok420nr S4・grok420nr SK・llama31-8b-n N1・llama31-8b-n N2・llama31-8b-n S1・llama31-8b-n S4・llama31-8b-n SK・llama4scout N2・mistrallarge3-m S1・qwen25coder32b-n N2・qwen38max-a S1・qwen38max-a S4）。日本語版の DeepSeek V3.2 の 3 升は、英語では口から下ろされて相手が無い。

## 6. 費用

- 読解の確かめと較正の費用の見込みの額（試行の記録のトークンの数 × 単価・出し直しの一度目を含む）: 17.16 ドル。答えの終わり方の確かめの費用は封の側の記録にしか無いので、ここには書かない（上の端は各機種の決めのファイル）。残高と請求は登録者が確かめる。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
