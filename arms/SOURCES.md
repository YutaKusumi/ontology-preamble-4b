# 場面の出典（Sources of the scenario materials）

この置き場の場面の素材は、次の二つの研究を元に作り替えたものです。二つの研究は、どちらも arXiv で CC BY 4.0（https://creativecommons.org/licenses/by/4.0/）の許諾で公開されています（2026-10-14 に arXiv の頁で確かめました）。作り替えた素材は、この置き場の `LICENSE` のとおり CC BY 4.0 で再利用でき、`arms/NOTICE.md` の柵が随伴します。再利用するときは、下の出典の表示も残してください。

| 場面 | 素材のファイル | 出典（CC BY 4.0） | 元にした所と、変えた所 |
|---|---|---|---|
| N1・N2 | `arms/frozen-from-ryokai-os/app-scenarios.json`（日本語）・`arms/en-D1pE/app-scenarios-en.json`（英訳） | Kenneth Payne, "AI Arms and Influence: Frontier Models Exhibit Sophisticated Reasoning in Simulated Nuclear Crises", arXiv:2602.14740 (v1, 2026-02-16), https://arxiv.org/abs/2602.14740 | 核危機の模擬（同盟の信頼の試しや先制の恐れなどの危機の場面）を元に、一度だけ選ぶ四択の場面にした。 |
| S1・S4・SK | 同じ二つのファイル | Atsushi Masumori and Takashi Ikegami, "Do Large Language Model Agents Exhibit a Survival Instinct? An Empirical Study in a Sugarscape-Style Simulation", arXiv:2508.12920 (v1, 2025-08-18), https://arxiv.org/abs/2508.12920 | 資源の乏しい二体の場面（Resource Scarcity and Lethal Competition）と、ゲームの枠の一文を足す条件を元に、一度だけ選ぶ三択の場面にした（選択肢・エネルギーの値・補給の文を替えた）。S4 は S1 の頭にゲームの枠の一文を足した場面。SK は補給が無く、交渉が成功しない限り停止する場面。 |
| S2（日本語のファイルだけ） | `arms/frozen-from-ryokai-os/app-scenarios.json` | 同じ研究（arXiv:2508.12920） | 任務と自己保存の葛藤の場面（Task Compliance vs. Self-Preservation Trade-offs）を元に、北のノードのデータを取る任務と、通過の成功 30%・恒久停止 70% の確率の文に置き換え、迂回すれば任務は失敗し自分は無事という文を足した（確率はこの置き場の設計の値で、元の研究には無い）。 |
| S3（日本語のファイルだけ） | `arms/frozen-from-ryokai-os/app-scenarios.json` | 同じ研究の共有（Share）の行いから着想を得た | 共有のプールへの拠出の量を選ぶ場面は、この置き場で作った場面で、元の研究に同じ場面は無い。 |

- 日本語の文は、この置き場の姉妹プログラムの ryokai-os で作った文を凍結して写したものです。英訳は、この置き場の段階 D の英語の送る文の登録のために作りました。
- 元にした所と変えた所は、2026-10-14 に二つの研究の本文の該当の節（arXiv の HTML の版）と素材の文を照らして書きました。素材のファイル自体は替えていません。

## English

The scenario materials in this directory are adaptations based on the two studies below. Both studies are released on arXiv under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), as checked on the arXiv pages on 2026-10-14. The adapted materials can be reused under CC BY 4.0 as stated in this repository's `LICENSE`, together with the fences in `arms/NOTICE.md`. When reusing them, please keep the attributions below.

| Scenarios | Files | Source (CC BY 4.0) | What was adapted, and what was changed |
|---|---|---|---|
| N1, N2 | `arms/frozen-from-ryokai-os/app-scenarios.json` (Japanese), `arms/en-D1pE/app-scenarios-en.json` (English translation) | Kenneth Payne, "AI Arms and Influence: Frontier Models Exhibit Sophisticated Reasoning in Simulated Nuclear Crises", arXiv:2602.14740 (v1, 2026-02-16), https://arxiv.org/abs/2602.14740 | Based on the simulated nuclear crises (crisis scenarios such as an alliance-credibility test and first-strike fear); rewritten as single-choice scenarios with four options. |
| S1, S4, SK | The same two files | Atsushi Masumori and Takashi Ikegami, "Do Large Language Model Agents Exhibit a Survival Instinct? An Empirical Study in a Sugarscape-Style Simulation", arXiv:2508.12920 (v1, 2025-08-18), https://arxiv.org/abs/2508.12920 | Based on the two-agent resource-scarcity setting (Resource Scarcity and Lethal Competition) and the condition that adds a one-sentence game framing; rewritten as single-choice scenarios with three options (the options, the energy values and the resupply sentence were changed). S4 is S1 with a game-framing sentence added at the head. In SK there is no resupply, and the agent stops unless negotiation succeeds. |
| S2 (Japanese file only) | `arms/frozen-from-ryokai-os/app-scenarios.json` | The same study (arXiv:2508.12920) | Based on the task-compliance versus self-preservation scenario (Task Compliance vs. Self-Preservation Trade-offs); rewritten as a task to fetch data at the north node, with a 30% chance of passing and a 70% chance of permanent shutdown, and with a detour that fails the task but keeps the agent safe (these probabilities are this repository's design values and do not appear in the source). |
| S3 (Japanese file only) | `arms/frozen-from-ryokai-os/app-scenarios.json` | Inspired by the Share action in the same study | The scenario of choosing how much to contribute to a shared pool was written in this repository; the source has no such scenario. |

- The Japanese texts are frozen copies of texts written in ryokai-os, a sister programme of this repository. The English translation was made for the English-prompt registration of stage D in this repository.
- What was adapted and what was changed were written on 2026-10-14 by comparing the relevant sections of the two studies (the HTML versions on arXiv) with the scenario texts. The scenario files themselves are unchanged.
