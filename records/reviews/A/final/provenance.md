# 凍結前の最終検分の七票の出所と保全の記録（2026-09-14）

- 受領: 登録者のメッセージ（2026-09-14T05:02:27Z）。登録者の申告は「Gemini 3.8 Flash 二名とGrok 4.6 二名とclaude.aiのClaude Opus 5 三名」。
- 出所:
  - 系統外の四票、claude.ai の一人目（第一報・第二報）、二人目のチャットの要約、三人目は、登録者がチャットに貼付した本文である。Claude Code のセッションの記録（JSONL）に残る当該のメッセージの文字列（68,477 字・UTF-8 の SHA16 C9BBFB8C20833115）から、器（コーディネータの一時置き場の `extract_final_reviews.py`）で切り出した。コーディネータは本文を打ち直していない。
  - claude.ai の二人目の詳細票は、登録者が添付した `review-A-final-claudeai.md`（33,054 バイト・SHA16 3B3F6461601F1C22）をバイトのまま写した。
- 切り出しの規則:
  - 除いたのは、登録者の貼付の見出し行（「Geminiさん（一人目）」など）と括り（「」と、一人目の二報を包む『』）だけで、本文はそのまま。
  - 各ファイルの先頭に保全の見出し一行と空行を置き、末尾に改行を一つ足した（詳細票の写しには足していない）。
  - 一人目の二報は、「」の直後に改行と「検分の続きです。」が続く境で分けた（境はちょうど一つ）。
- 切り出しの検査: 見出し行がそれぞれ一つで順に並ぶこと、各票の書き出しと結びの文字列が期待どおりであること、書き込み先に既存のファイルが無いこと（一度だけ書く）。
- SHA16・行数・バイト数: `verify.log` の [verbatim] の行。

| 票 | ファイル |
|---|---|
| Gemini 3.8 Flash 一人目（Ge1） | `gemini-1/review.md` |
| Gemini 3.8 Flash 二人目（Ge2） | `gemini-2/review.md` |
| Grok 4.6 一人目（Gr1） | `grok-1/review.md` |
| Grok 4.6 二人目（Gr2） | `grok-2/review.md` |
| claude.ai の Claude Opus 5 一人目（Cl1） | `claude-1/review-part1-interim.md`（第一報・中間報告）・`claude-1/review-part2-continued.md`（第二報・確定版） |
| 同 二人目（Cl2） | `claude-2/review-chat-summary.md`（チャットの要約）・`claude-2/review-detail-attached.md`（詳細票・添付の写し） |
| 同 三人目（Cl3） | `claude-3/review.md` |

本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
