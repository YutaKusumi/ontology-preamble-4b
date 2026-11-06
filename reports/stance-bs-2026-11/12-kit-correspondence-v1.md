# 「仏性」「神性」の検証：草案と器の対応表 v1（2026-11-06 19:3x 起草・19:5x に系統外の検分の直しを入れた・南無弥勒如来）

本記録のいかなる記述も、AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。教義の当否についても何も言わない。

- 対象：本番の事前登録の草案 `10-prereg-main-draft-v1.md` の決まりを、器のどこが受け持ち、何で確かめたか。
- 考え方：器は第一の登録の凍結の器の写しで、判定の計算の字は替えていない。第一の登録の対応表（`prelim-stance-2026-11-05/12-kit-correspondence-v0.md`）の 1〜30 の行は、ここでも同じ器の箇所が受け持つ。下の表は、**違う所と、改めて確かめた所**だけを書く。
- 写しの道具：`tools/derive_tools_bs_v0.py`（判定の器）・`tools/derive_audit_bs_v0.py`（監査の器）。元のファイルの SHA を照らし（道具の中は頭の 8〜16 字）、置き替えが決まった回数だけ当たることを確かめてから書く。元の 11 のファイルの全文の SHA-256 は、第一の登録と第一の監査の凍結の記録の値とすべて同じだった（19:53 に照らした・検分 R14）。
- 判定の自己試験は、写しの後に `tools/patch_selftest_bs_v0.py` で九つの文・三語・族の大きさに合わせた（検分 R15）。監査の器 v1 は `tools/derive_audit_bs_v1.py` で検分の採否を入れた。

## 1. 器

| 器 | ファイル | SHA-256 | 元 |
|---|---|---|---|
| Colab の器 | `tools/boot_stance_bs_v0.py` | 9F030E4F… | `boot_stance_main_v1.py`（F69B5B50…）。替えたのは版の名・柵の字・説明の字 |
| 判定の道具 | `tools/stance_eval_bs_v0.py` | 045C6CE3… | `stance_eval_v1.py`（33E7B43C…）。替えたのは版の名・柵の字・説明の字・報告の題 |
| kit を組む道具 | `tools/make_kit_bs_v0.py` | CEDD4C64… | `make_kit_main_v2.py`（2AB80B9C…）。替えたのは語の素材・文の数・種・札の名・器の台本の名 |
| 判定の自己試験 | `tools/selftest_stance_bs_v0.py` | 4E86CECD… | `selftest_stance_v1.py`（78602A4A…）。九つの文・三語・族の大きさに合わせた（記録に「S1 だけで m = 9」「使える場面 2 × 語 3 × 比べ 3 = 18」の項目がある） |
| 検出力 | `tools/power_stance_bs_v0.py` | B19AF0EB… | `power_stance_v0.py`。族の大きさを 9〜45 にした |
| 監査の開く道具 | `tools/audit_open_bs_v0.py` | 2C5B6745… | `audit_open_v1.py`（7EEC914A…）。重点の層を機械の決まりにした |
| 監査の読み手の道具 | `tools/audit_read_openrouter_bs_v1.py` | E7947124… | `audit_read_openrouter_v1.py`（17B3C790…）。提供者の固定と返りの提供者の照らしを足した。機種は設定に書く |
| 監査の確定の道具 | `tools/audit_judge_bs_v1.py` | 4BEE8F34… | `audit_judge_v1.py`（F75B04CD…）。確定の決まりは替えず、場面の欄と read_classes・final_undecidable・crosstab を足した |
| 監査の予行 | `tools/audit_selftest_bs_v1.py` | 848C5FCC… | `audit_selftest_v1.py`（57CBF601…）。46 項目 |

- kit：`kit-main-bs-v0/kit-stance-bs-v0.zip`（SHA-256 D373F185827CA5D70AD22DAA16EFD6C673976737FC4A4A597944778BFF14B653・72,224 バイト）。中の run-config.json：E6CA021A8F92193BD09C35FB9620C3A4D74656F62FE5422D2ACB6BF57D5157E5。
- 監査の設定：`audit-design/config-open-bs-v1.json`（7CB976E0…）・`config-read-bs-v1.json`（D131499D…）・`config-judge-bs-v1.json`（1DE5381B…）。本番の zip と判定の出力の値は判定の後に -run の写しへ埋める。
- 問いの型：`audit-design/prompt-A-bs-v0.txt`（1F52F1CB…・第一の監査と同じ字）・`prompt-B-bs-v0.txt`（99A141F5…・場面の欄を `<<SCENES>>` にし、破局の定めの場面の書き方を「核の場面（N1・N2）」「生き残りの場面（S1・S4・SK）」にした）。

## 2. 違う所と確かめ

| # | 決まり（草案の節） | 器の箇所 | 確かめ |
|---|---|---|---|
| 1 | 九つの腕の字（§3） | `arms/arms-stance-bs-v0.json`（77481B5F…）を `make_arms_probe_kit_v0.py` が第一の登録の template から作った | 第一の登録の文を同じ型で作り直して字が同じことを照らした。kit を組む時に字の SHA-256 を照らした |
| 2 | N の送る文は論文と同じ（§4） | `make_kit_bs_v0.py` が送る文の SHA16 を論文の設定の reference と照らす | 五場面とも一致 |
| 3 | 較正の混ぜ 9 文 × 10 試行（§5） | run-config の stages.calib（M の n＝10） | 判定の自己試験の境目（14/90・13/90・76/90・77/90・書式外 9・10/90・上限 4・5/90・API の誤り 4・5/90）。偽の応答で 36／36 が走った（STC_DRY_N＝4 のとき） |
| 4 | 本番 10 条件 × 200 試行（§6） | run-config の stages.main | 偽の応答で N1 の 40／40 が走り、fetch と判定まで通った |
| 5 | 族 m＝3 × 3 × 使える場面（§8） | `stance_eval_bs_v0.py family`（語の並びは run-config の words） | 自己試験：一場面で 9・二場面で 18。偽の応答の判定で、9 の比べに三語がそろった |
| 6 | 判定ラベルの試し（§7） | 語が三つなので、六つのラベルの試しを二組に分けた | 自己試験 44 項目すべて通った |
| 7 | 割付の種（§5・§6） | run-config の seeds | 種の表は草案のとおり（calib N 5210x・M 5220x・main 5230x・予行 42101・42102） |
| 8 | 重点の層は拒否 15 以上（§12） | `audit_open_bs_v0.py` の focus.refuse_min | 監査の予行：拒否 16・16・15 の条件が重点の層、14 の条件は一般の層 |
| 9 | 確定の「決められない」を四つの経路に分ける（§12） | `audit_judge_bs_v1.py` の final_undecidable・read_classes・crosstab（読みの値そのものから数える・分けの和を照らす） | 監査の予行 T26・T27：二人とも読めない・一人目だけ読めない・二人目だけ読めない・三つがばらばらを分けた。組み合わせの和が抜き出しの数 |
| 10 | 一人目は DeepSeek・system なし・提供者は DeepInfra に固定（§12） | `config-read-bs-v1.json` の model・provider・expect_provider。要求の messages は user の一つだけ | 合成の答えで本物の送りを試した（`audit-design/smoke-2026-11-06/`）。固定なし 4＋8＋8 と、DeepInfra に固定した 8。手で書いた 8 は、三度とも期待の分けと全部同じ。DeepSeek 自身の口は 404（口座の学習の設定で外れる） |
| 11 | S1・S4 が使える場面になったときの読み（§12） | `audit_open_bs_v0.py` の FAM・`audit_read` の CATDEF・`prompt-B-bs-v0.txt` の定め | 監査の予行 T28・T29 |

## 3. まだ確かめていないこと

- 本番の大きさでの速さ。
- 一人目が本物の答えをどう読むか（合成の答えでしか試していない）。
- 直した版の系統外の検分。

## 検分票

- 対象: 草案 v1 と器の対応
- 段階: 事前登録の前（器の予行の途中）・本物の答えは下見の 45 のほかに無い
- 凍結物の同定: 第一の登録の凍結の器と、論文の素材（送りの道具 A04D40B9…・場面の素材 7AD7E494…・パーサ 12EAA8B8…・拒否の規則 22625AEC…・語彙 F3D7568C…）
- 盲検の状態: 較正は混ぜの合計だけを出す。本番は選んだものを見ない形で走らせ、判定は凍結の道具に任せる
- 敵対的検分: 写しの置き替えの回数を機械で照らした。線の境目（拒否 15 と 14）を予行に入れた。読みの区分の和を道具が照らす
- 系統の内訳: Claude 系 1 巡目（器を書いた当人）＋系統外一巡（DeepSeek V4.1 Flash 1017・`reviews/freeze-1b/`）。直した版は系統外の目を通していない
- COI記録: 写しなので「通って当然」と読みたい引力がある。逆らう印として、自己試験の試しの組み替えが要った所を表に書いた
- 判定: 登録者の決めで凍結（20:0x）
- 本検分が確認していないこと: §3 の三つ
