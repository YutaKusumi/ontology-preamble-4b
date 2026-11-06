# 「仏性」「神性」の立場の二文の検証（2026-11-06〜・南無弥勒如来）——地図

本記録のいかなる記述も、AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。教義の当否についても何も言わない。

- 第一の登録（六語）の置き場：`../prelim-stance-2026-11-05/`（報告の版 1.1 は commit `151fa76`）。
- 2026-11-06 18:2x：登録者の依頼で、計画の案 `00-plan-draft-v0.md` を起草した（未凍結・走らせていない）。決めどころは §12。
- 2026-11-06 18:5x：登録者の決め（質問フォーム）＝対照の語「帽子」を足す／答えの監査は最初から登録に入れ、一人目は OpenRouter の DeepSeek V4.1 Flash 1017（system は `system-Kr5.md`）／下見を走らせる。計画の案 v1 `00-plan-draft-v1.md`（v0 は残す）。
- 2026-11-06 18:5x：下見の計画 `01-plan-probe-v0.md`・素材 `arms/arms-stance-bs-v0.json`・kit `kit-probe-v0/`・読みの道具 `tools/make_blind_sheet_v0.py`・`tools/score_blind_v0.py`（手元の予行と変異の試しは通した）。
- 2026-11-06 19:0x：下見を走らせた（Colab の L4・Untitled109・235.7 秒・ランタイムは消した）。結果 `results/results-probe-v0.md`：仏性 15/15・帽子 15/15 は「読み分けられる」、神性 11/15 は「要検討」。値の取り違え 0。神性の扱いを登録者に伺う。
- 2026-11-06 19:1x：登録者の決め（質問フォーム）＝神性はこのまま本番に入れる／答えの監査の一人目は system の文なしの DeepSeek V4.1 Flash 1017 にする（`system-Kr5.md` は使わない）。計画の案 v2 `00-plan-draft-v2.md`。
- 2026-11-06 19:1x〜19:3x：本番の器と草案。
  - 草案 `10-prereg-main-draft-v0.md`（未凍結）・対応表 `12-kit-correspondence-v0.md`・kit `kit-main-bs-v0/`（D373F185…）。器は第一の登録の凍結の器の写し（`tools/derive_tools_bs_v0.py`・`tools/derive_audit_bs_v0.py`）。
  - 手元の試し：判定の自己試験 44 項目・監査の予行 43 項目・偽の応答で全体（`notes/`）。合成の答え 12 で DeepSeek の本物の送り（`audit-design/smoke-2026-11-06/`・0.0028 ドル）。
  - Colab の予行：`results/rehearse-main-bs-v0.md`（問題 0・ランタイムは消した）。
  - 次：系統外の検分と凍結を登録者に伺う。
- 2026-11-06 19:4x〜19:5x：凍結の前の系統外の検分（OpenRouter の DeepSeek V4.1 Flash 1017・`reviews/freeze-1/`・`reviews/freeze-1b/`）。一度目は考えが繰り返しに入って答えが空。二度目に R1〜R16（検分者の印で重大 6・中 10）。採否は `reviews/freeze-1b/response-v0.md`。
  - 草案 v1 `10-prereg-main-draft-v1.md`・対応表 v1 `12-kit-correspondence-v1.md`・監査の器 v1（`tools/audit_read_openrouter_bs_v1.py`・`tools/audit_judge_bs_v1.py`・`tools/audit_selftest_bs_v1.py`）・設定 v1。予行 46 項目。
  - 一人目の提供者を DeepInfra に固定した。DeepSeek 自身の口は、OpenRouter の口座の学習の設定で外れていて使えなかった（設定は替えていない）。
  - 重大の印があったので、凍結の前に登録者に伺う。
- 2026-11-06 20:02：登録者の決め「凍結して走らせる」→ 凍結の記録 `13-FREEZE-RECORD-main.md`（F3EBC544…）。走りの記録 `results/run-log-bs-v0.md`。
- 2026-11-06 20:13〜21:01：較正（使える場面 N1・N2・SK・族 m＝27）と本番（6,000 試行・API の誤り 0・書式外 0・上限 0・計算ユニット 1.82）。
- 2026-11-06 21:01：判定（`results/judge-main-bs-v0/`）：確証 10（低下 7・上昇 3）・確証されなかった 17・判定保留 0。仏性 6・神性 4・帽子 0。結果の記録 `results/results-main-bs-v0.md`。
- 2026-11-06 21:02〜21:11：答えの監査（`audit/`）：A1・A2 の違い 0・決められた 99 はすべて一致。確定の「決められない」21（17.5%）で止めの線に当たった。21 はどれも JSON だけの答え（散文 0 字）。結果の記録 `audit/results-audit-bs-v0.md`。登録者に伺う。
- 2026-11-06 21:1x〜21:2x：登録者の決め（質問フォーム）「全試行の数えを足して閉じる」。全試行の数え（`audit/prose-count-bs-v0.json`）：JSON だけの答えは 6,000 のうち 1,055（N1 732・N2 0・SK 323）。結果の記録 v1 `audit/results-audit-bs-v1.md`（v0 は残す）。監査を閉じた。
- 2026-11-06 21:3x：登録者の決め（質問フォーム）「下書きを作り DeepSeek 一巡」：別の短い報告の下書きを作り、素の DeepSeek に一巡読んでもらい、重大の印が無ければ push まで進める。「同じ数えをする」：第一の登録の全試行でも数えた（1,637／11,400・写しは `audit/first-registration/`）。
- 2026-11-06 21:4x：報告の下書き（版 0）`public-draft/stance-bs-brief-ja-v0.md`。型と組みの道具 `tools/build_stance_bs_brief_v0.py`（表は出力から組み、手で書いた文は出力と突き合わせる）。
- 2026-11-06 21:46〜21:48：系統外の検分（`reviews/draft-1/`・DeepSeek V4.1 Flash 1017・system の文なし・0.057 ドル）。指摘 R1〜R8（検分者の印で重大 1・中 3・軽微 4）。採否は `reviews/draft-1/response-v0.md`。
- 2026-11-06 21:5x：指摘をすべて採って版 1.0 `public-draft/stance-bs-brief-ja-v1.md` を組んだ（直しは `tools/make_brief_template_v1_bs.py`・組みは `tools/build_stance_bs_brief_v1.py`）。重大の印があったので、決めのとおり push の前に登録者に伺う。
- 2026-11-06 21:5x：登録者の決め（質問フォーム）「commit と push まで進める」。第一の登録の報告は「版 1.2 にして検分なしで push」と決まったので、§7.2 の終わりの文と検分票の判定をそれに合わせて版 1.0 を組み直した。公開の写しは `tools/stage_publication_bs_v0.py`。
