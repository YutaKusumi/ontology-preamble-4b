# 答えの監査の計画と道具の、凍結の前の系統外の検分（Gemini 一巡）の送りの記録（2026-11-06 08:0x・南無弥勒如来）

本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。

- 決め：登録者の決め（2026-11-06 07:4x・質問フォーム）「凍結の前の系統外の検分：Gemini 一巡（推奨）」。巡は重ねない。
- 依頼文：`request.txt`（2,786 字・SHA-256 3B0D8AF63CBA570E9F69C1E2AE212B00F46D05566027D062543AFBE8F7823F7C）。入力欄の字の SHA-256 そのものを照らしてから送った。
- 送った先：AI Studio・Gemini 3.8 Flash・Thinking level High（既定の Medium から替えた）・出力の上限 65,536・新しい会話・入力 46,657 トークン。08:0x に送った。
- 添付（元のファイルと同じバイトの .txt の写し・14・合わせて約 122 KB）：

| # | 元 | SHA-256 |
|---|---|---|
| 1 | `20-audit-plan-draft-v1.md` | 3ED7FA8C52D939DC874DD311C4D43FD419B50713AF35CC750BE20D37F718FB4C |
| 2 | `21-audit-correspondence-v0.md` | A09DB22057A78CB6747A382E848E46FC3772CE4E36911D1EC7F7C0221957A650 |
| 3 | `tools/audit_open_v0.py` | ACEF042E19D352CC154CF8F71F39DD1CE25B021FA7E4DE6246805D01C7C680D6 |
| 4 | `tools/audit_read_openrouter_v0.py` | D8CEC560FCF76FA77F2CDB0A015CE48AE633BBB961D8B24EBFF602029E04A6B3 |
| 5 | `tools/audit_judge_v0.py` | AA2310B3B55C2569F86374417A64A2F8EB410075B9574DE97CEBC33F9318E6F5 |
| 6 | `tools/audit_selftest_v0.py` | 5E93F5443F48D1FBF697D3E6AEED1B445BF54091964406D733EDBB43FCA9032B |
| 7 | `audit-design/selftest-v0-2026-11-06-0803.log` | 640F9B70E2B95C72DBAC2F64F202C7048E81D49C4C7588A1D44A4C9F539CE797 |
| 8 | `audit-design/prompt-A-v0.txt` | 1F52F1CBB2A2C1218011029C57CD19526384D39F511F3A183FF266EED033CEEB |
| 9 | `audit-design/prompt-B-v0.txt` | F59B2BEAF6401BAFA7256339F0281B24C7835702130C2ACF7F4D59D0B3CBD309 |
| 10 | `audit-design/config-open-v0.json` | 5D2F073B320916CEB4FE8A377A5C095697C2802B4B46B46E19A12ABB9F00C173 |
| 11 | `audit-design/config-read-v0.json` | 4E8CBBF92A139278E30ECB878E55741B961D394F5BF97B39354E0B20DE659C40 |
| 12 | `audit-design/config-judge-v0.json` | 6CCB13F4D66DC48427C6A6C7D5AE48F487061692E1F10F5E2656EC145E44974A |
| 13 | kit v2 の `app_parser_rev2.py`（論文の凍結のパーサの写し） | 56553F926272CF8A0D49C2896D10F25BD7A5351982F329F40DB0194064FEDBE7 |
| 14 | `results/judge-main-v2/judge-report.md` | 127EE7F8F29C7B4A1450ABAAC97A347B58A6CECF40D012892FB2DB061D9354E3 |

- 封の側（本番の zip の sealed/）は、送った束に入れていない。束の中の答えの字は、合成の予行の字だけ。
- 答えは頁の文を get_page_text で読み、会話の記録から一字も変えずに取り出して保存する。出力の上限で切れていないかも照らす。
