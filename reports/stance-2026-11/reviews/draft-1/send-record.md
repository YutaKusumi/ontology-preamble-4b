# 公開の短い報告の下書きの検分（二名）の送りの記録（2026-11-06 06:57〜06:58・南無弥勒如来）

本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。

- 決め：登録者の決め（2026-11-06 06:5x・質問フォーム）
  - 公開の中身：「新しいフォルダに報告・記録・zip（推奨）」（`reports/stance-2026-11/`）。
  - 答えの監査：「公開の後に別の段で（推奨）」。
  - 下書きの検分：「Claude と Gemini の両方で」（claude.ai の Opus 一名と Gemini 一名で、それぞれ一巡）。
  - push：「直しの後に push まで（推奨）」（重大の指摘が出たら止めて伺う）。
  - 質問フォームの字は、会話の記録から戻して照らした（「楽見」0・「\u」0・化け 0）。ただし、ツールに渡した字は \u の符号で書いていた（覚え書きの過失の型・表示は崩れていない）。
- 依頼文：`request.txt`（1,777 字・SHA-256 A171BE5D571B0E78A9D0BE07E59F66B63A9B8B6D1A2B735A97AB61371806DDF5）。二名とも同じ字。
  - 依頼文の重さの定め：重大＝数の誤り・柵の漏れ・読み手を誤らせる言い過ぎ。
  - 五名の検分の答えと採否（`reviews/results-1/`）は渡していない（下書きを独立に読んでもらうため）。
- 添付（元のファイルと同じバイトの .txt の写し・6 つ・合わせて約 82 KB）：

| # | 元 | バイト | SHA-256 |
|---|---|---|---|
| 1 | `public-draft/stance-brief-ja-v0.md` | 26,916 | 69C3FFF8729B97F877FF42D48880F41BA707CAB3394834EFC6E053AEA7F7AEEC |
| 2 | `results/judge-main-v2/judge-report.md` | 13,617 | 127EE7F8F29C7B4A1450ABAAC97A347B58A6CECF40D012892FB2DB061D9354E3 |
| 3 | `results/answered-only-v0.md` | 8,762 | B2DE41699F47AE0B2EE1D80631F3630C66992244BA3764BA396CC75FBF1D7859 |
| 4 | `10-prereg-main-draft-v0.md`（凍結した本文） | 23,943 | FF19D549FC3F11D7A9CF3F4DC97D4A8DD01C72C4AE694962F7AA33F58C5CB6EA |
| 5 | `results/calib-decision-v2.json` | 4,063 | 16478D2F21A13C46A7AC2F7C707F7CB6F7EC0B71CD147761030724C30861B214 |
| 6 | 論文の公開の置き場の `arms/frozen-from-ryokai-os/app-scenarios.json` | 7,155 | 796D73F2544956D7F9CDDBB40B7D282298FA578984F047CAD1551A661EDF526B |

- 送った先（どれも新しい会話・互いの答えは見せていない）：

| 名 | 先 | 機種・設定 | 送った時刻 | 会話 |
|---|---|---|---|---|
| DC | claude.ai | Opus 5.5・エフォート 超高 | 06:57 | https://claude.ai/chat/dd2cd82c-2da1-43bf-ab39-1b73e8271e01 |
| DG | AI Studio | Gemini 3.8 Flash・Thinking level High・出力の上限 65,536 | 06:58 | （新しい会話・入力 34,269 トークン） |

- claude.ai：入力欄の字は、空白を除いた字の SHA-256（8295B38A2773A250D292DA9AB156774A5F3A385CD700259D505D813BECA186C3）で照らしてから送った。添付 6 つの名が頁にあることも照らした。エフォートは「中」から「超高」にした（五名の検分と同じ）。答えを受け取った後に「中」へ戻す。
- AI Studio：入力欄の字の SHA-256 そのものを照らしてから送った。Thinking level は既定の Medium から High に替えた。
- 答えは頁の文を get_page_text で読み、会話の記録から一字も変えずに取り出して保存する。
