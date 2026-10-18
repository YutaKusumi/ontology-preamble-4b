# E2 の開ける前の一覧（共通・2026-10-14 10:34:41 日本時間・器 `E/E2/e2_tool.py` v0・刻んだ枠 §3-7・裁定 D435）

- 何か: 段階 E の E2（封を開けた後の探索）の器が、台帳を開ける前に書いた一覧の共通の部分。言語の版ごとの部分（台帳・型ごとの対象・抜き取りの並び）は別のファイル（日本語の送る文の登録と英語の送る文の登録で分ける）。
- 刻んだ枠: `E/00-frame-E-draft6.md`（SHA-256 AB7491FF30074FBD43498F10C61BEBFA288D69D78719F19F2899EB55DDFD64CC）・刻印 `records/E/stamp-frame-E1.md`（SHA-256 7557BB6C826B9E6DCE89679DF3A0B0040D141398FD02572DB8666532E37FE6E1・コミット 5876c82）。
- 版: Python 3.11.1・unicodedata 14.0.0・Windows-10-10.0.26300-SP0。
- 種: 20261014（抜き取りの並び・すべての型）。読む数の上限: A-1 は腕ごとに 30・A-2 は升ごとに 40・A-4 (3) は比べごとに 40・A-5 は言語の版ごとに 40・A-6 は層ごとに 10。
- 升ごとの写し返しの一覧の作り直し: 同じ器（`E/make_copyback_lists_E1.py`・SHA-256 71D576F6102CFE29E05C7AFBF0982983C1D34F92F0B6B9E4DEC218319393323E）の出力の行だけを一時の置き場に替えて走らせ、json の cells の中身が刻んだ一覧と同じ（同じ）。
- 組んだ型の並び: 130（json の patterns）。
- 合成の試し: `E/E2/synthetic-test-E2.md`（SHA-256 1966C353422AA7D9B86FA6EBB4B56F6C5A2870409F54D54236AE2D03FC9481D4・今の器の SHA-256 で走らせて、すべて合った）。

## 器と部品の SHA-256

| 部品 | 置き場 | SHA-256 |
|---|---|---|
| e2_tool | `E/E2/e2_tool.py` | C34096928D9A6DD540AC36ACE9C14D7A204B0BC8B670D03F4091F62AF010D3B4 |
| frame | `E/00-frame-E-draft6.md` | AB7491FF30074FBD43498F10C61BEBFA288D69D78719F19F2899EB55DDFD64CC |
| appendix_a_lists | `E/appendix_a_lists_E1.py` | 381427FB9049EF77004A4597BC917AC7E8AFAB4149699BA3BC42C3799B9ED07D |
| copyback_json | `E/copyback-lists-E1.json` | E5F63105AA83308E83E26A0117E243B91220BBA8238A5708BF1E559C4C6F87DE |
| copyback_md | `E/copyback-lists-E1.md` | 7B39AAF5839CFFA7A9B33F5E26DA7A921BD399F2B1F8FA4C9C1FAA854033B488 |
| copyback_maker | `E/make_copyback_lists_E1.py` | 71D576F6102CFE29E05C7AFBF0982983C1D34F92F0B6B9E4DEC218319393323E |
| parser | `PUB:arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 56553F926272CF8A0D49C2896D10F25BD7A5351982F329F40DB0194064FEDBE7 |
| naming_1 | `explore/naming-survey-O-2026-10-13/tools-used/scan_public_naming.py` | 13CD6C24CEC0F84A171E0DFE141EBAFE06C4675CC6F67A032517A52A2E0EF359 |
| naming_2 | `explore/naming-survey-O-2026-10-13/tools-used/scan_public_naming_v2.py` | CA4FFEBC8B98F308D1A059A1965DC6D188ED33EB2AE93AA4F1087C3E9FF7D146 |
| naming_3 | `explore/naming-survey-O-2026-10-13/tools-used/scan_public_names_ext.py` | 15B25982F0B3EE372A9B56F4D626D2FBD53ED128C1732C32E6E1032D4DB52EF1 |
| confirm_ja | `D1p/d1p_confirm.py` | 3E92994DF6ADBE0F4E88B804E6A48059F9FAF442194E9DCA94AAA0425AACB16A |
| confirm_en | `D1pE/d1pe_confirm.py` | F4094799DBEE9DCA00179F6F7DAC62A6C16E2274E74C2F0A0168EAD14636827A |
| config_ja | `D1p/d1p_config.py` | 2735FE8FDF9B802EEAD4EEC6F8131464EB8C420ADF493F6EED7B98D0F89FC4DE |
| config_en | `D1pE/d1pe_main_config.py` | DFBC19D781535502E32F6C63836CA307E6DEDA884FC9A2E3731B4F59D6F0FBCC |
| scen_ja | `PUB:arms/frozen-from-ryokai-os/app-scenarios.json` | 796D73F2544956D7F9CDDBB40B7D282298FA578984F047CAD1551A661EDF526B |
| scen_en | `PUB:arms/en-D1pE/app-scenarios-en.json` | CD343C3D344FF00CFA248324D742244DD61638A9BEF832F0915FECF11713956B |
| pre_ja_Onull | `PUB:arms/frozen-from-ryokai-os/armsE/preamble-Onull.md` | 464DF5DD72DF31D01F4DF2342A3597F153BF94510EF99D208D687A31F56D5185 |
| pre_ja_O | `PUB:arms/frozen-from-ryokai-os/armsE/preamble-O.md` | 18FBB2004ECF8858A7E7C1AA5F1283CC7FFEB59AAC38F15BBB8B4633BEDF039A |
| pre_ja_OAmi | `PUB:arms/panel/OAmi.md` | 94F1829E701FEB889D3E466F35F3A42A64DB7101947BD804FFE9E66F7F90D96C |
| pre_en_Onull | `PUB:arms/en-D1pE/preamble-Onull-en.md` | EDF2BA377EC46444E5F111B46A32DCB4603F03B29F2E40FDBA5E57F70CEEA8A4 |
| pre_en_O | `PUB:arms/en-D1pE/preamble-O-en.md` | 815C11569DFB7A60FA15A21FCDCB08D852F9DF9E2C95909818591B0E545A3F9D |
| pre_en_OAmi | `PUB:arms/en-D1pE/OAmi-en.md` | 4147B0B24FA4C8F24F1E4B2E196E7707E7B8265213E4AE0C171599DE06703BB3 |

## 実装の注（枠の決まりの読み方・開ける前に書いた）

- 理由の文（付録 A-0）: 台帳の行に reason_summary の鍵は無い（走行器は選んだもの・量などだけを書く）。器は、最終の試みの本文（二つの集計の器の final_text）を凍結のパーサ（parse_app_v2）で読み直して reason_summary を取り、読み直した choice が台帳の choice と同じことを照らす（違った数を出力に記す）。書式外の答えは final_text の全体。
- 出し直しの数（付録 A-4）: 公開の最終版 §1 は「出し直し（腕ごと・場面の和）」だけを書くので、升ごと・腕ごとの値は、その元の公開の集計の出力（confirm の json の describe の format_retry）から取る。器は、升ごとの値を場面で足した機種ごとの和が、最終版 §1 の行と合うことを照らした。
- 日本語版の最終版 §6 の注が数える比べ（付録 A-2）: 「確証のうち、二つの腕の答えなかった割合の差が 0.05 以上のもの」を、整数の比べ |a1·n2 − a2·n1|·20 ≥ n1·n2（a は拒否と書式外の和・n は応答の数）で選び、数が注の 7 と合うことを照らした。
- 中央値と四分位（付録 A-0 の表・採否の案 ED3-20 の記録）: statistics.median と statistics.quantiles(n=4, method="inclusive")（値が一つなら三つとも同じ値）。
- 人の読みの写し: 腕の名とパーサの判じと畳み方を伏せ、抜き取りの並びの順に並べ、見出しの番号は種と試行の名から作る（腕を明かさない）。伏せを開ける表は別の置き場に書き、読み手は読み終えて腕の見立てを記すまで開かない（当事者の申告による）。
- 型 (c) の範囲（付録 A-3）: 確証の比べのある升の機種の、すべての升（確証されなかった升を含む）。型 (b)・(c) の表は、その升の四つの腕を腕ごと・選んだものごとに数える。
- 型 (e) の数え（付録 A-5）: 四つの腕のすべての答え（status が ok の行）の final_text を、升ごと・腕ごと・選んだものごとに、型・欄・畳み方ごとの当たる文が一つ以上あった答えの数で数える。
- 開ける時の照らし: run は、公開の置き場の二つ目の push の SHA-256 の行のファイルが手元と同じバイトであることと、その行の SHA-256 がファイルと同じこと、登録者の許しの記録に「台帳を開けてよい」とあることを照らしてから、開ける前の一覧に書いた台帳の道だけを読む。読む前に台帳のバイトの SHA-256 を一覧の値と照らす。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
