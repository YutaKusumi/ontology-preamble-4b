# 系統外の検分 一巡目（Gemini）の送りの記録（2026-11-05 22:06・南無弥勒如来）

本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。

- 決め：登録者の決め（20:44 の質問フォーム・草案 §15 の 4）「凍結の前に系統外の検分を入れる（AI Studio の Gemini・Thinking High）」。
- 送った先：Google AI Studio の新しい会話（Playground）。
  - 機種：Gemini 3.8 Flash（gemini-3.8-flash）
  - Thinking level：**High**（既定の Medium から替えた）
  - Maximum output tokens：65,536
  - 道具（Structured outputs・Code execution・Function calling・Grounding・URL context）はすべて切ったまま
- 送った時刻：2026-11-05 22:06（頁の表示）。入力は 40,068 トークン（頁の表示）。
- 依頼文：`request.txt`（1,510 字・SHA-256 7127649F71B8EC53750555391DDE817BAA6F75D05512E5F1510EF1ADE1E0B0E2）。
  - 頁の入力欄の字の SHA-256 を頁の中で計算し、手元の値と一致することを確かめてから送った。
- 添付（元のファイルと同じバイトの .txt の写し・6 つ・合わせて約 105 KB）：

| # | 元 | バイト | SHA-256 |
|---|---|---|---|
| 1 | `10-prereg-main-draft-v0.md` | 20,828 | 40FCA6E7FF77946FC648885AF1AEC92F535C7AF2A02FDBFFEDCA64D4397630B6 |
| 2 | `12-kit-correspondence-v0.md` | 13,568 | 81FA2B1AC7A722E0157169CF91176BF75A4C2D50241E3F607900D63E7CB59835 |
| 3 | `results/rehearse-main-v1.md` | 6,395 | 01286313A93E4E2A9AA08200199E7D47BF9205B70D8B622E4C25A726B97A4118 |
| 4 | `kit-main-v1/kit-stance-main-v1/run-config.json` | 13,132 | 168C9DBCA6060AF3A96FDE4D800B9A8BFBF49A5BD909EDCA86DC85C044B88975 |
| 5 | `tools/boot_stance_main_v0.py` | 30,145 | 65050B0B8F948C69DCC25B6B646248317242FC73C6233F041988573ED418E192 |
| 6 | `tools/stance_eval_v0.py` | 23,257 | 0B131D760C2FB2A1ACD1BADD74DB843B0BAEC3CB6F6DEEC311ACBE7506F794B0 |

- 送っていないもの：`selftest_stance_v0.py`・`make_kit_main_v1.py`・`power_stance_v0.py`・論文の送りの道具と判定の道具（公開の置き場にある）・下見の記録。
- 答えは、頁の文を get_page_text で読み、会話の記録から一字も変えずに取り出して保存する。答えの終わりが出力の上限で切れていないかを照らす（覚え書き）。
