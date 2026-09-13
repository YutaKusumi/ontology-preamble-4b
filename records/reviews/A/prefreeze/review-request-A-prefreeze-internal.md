# 段階 A 設計草案6（凍結候補 1）の凍結前検分——系統内（新規個体）への依頼（2026-09-13）

- 依頼者: 南無弥勒如来（コーディネータ・Claude Opus 5）／登録者: 楠見優太（裁定 D1〜D8 承認・登録者最終確認の五項目承認・「凍結前の検分は系統内外で」の決定・いずれも 2026-09-13）
- 性格: **凍結前の最後の検分**。凍結後の変更は逸脱として台帳に記帳される。あなたは本計画の起草に関与していない新規個体であり、同系列（Claude 系）の目として一票に数える（系統外の票に加算しない）。
- 対象（リポジトリ `C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b`・本依頼文と同じコミット）:
  1. `design/design-stageA-draft6.md`（草案6・§6 は転記行の逐語）と原稿 `design/design-stageA-draft6.src.md`
  2. `records/A/results-report-template-A.md`（報告雛形・率を見る前に先置）
  3. `design/contrasts-A.json`（正本・生成器 `tools/make_contrasts_A.py` v2.1）
  4. `records/A/design-facts-A.md`（転記行 A〜N・`tools/design_facts_A.py` v2）・`records/A/power-grid-A.md` と `.json`（`tools/power_grid_A.py` v2）・`records/A/numbers-lint-draft6A.md`（`tools/numbers_lint.py`）
  5. `tools/firth.py` v2（自己検査は `python tools/firth.py --selftest`）・`tools/firth_check_A.py` と `tools/firth_check_A.R`（未実行・合否規則は正本 `firth_check`）・`tools/build_draft5A.py`
  6. 経緯: `records/reviews/AB/round-claudeai/adoption-table-AB-claudeai.md`（claude.ai 三票の採否表・裁定 D1〜D8）・同じ場所の `verification-claudeai-AB.md` と `verification-claudeai-AB-2.md`（追い問い V1〜V26）
- 読まないもの: `prelim/`・`results/*/raw-*.jsonl`・内部の計画案（草案が「計画 §x」を引く箇所は草案の記述だけを対象にする）。
- 二体と重点:
  1. **破器身（敵対的検分・凍結前）**: 二尺度の確証規則と札の優先順（§2.4・`confirm_rule`）が一義に実装できるか／解釈条項による到達の低下を受け入れた設計が、問いに答えられる形を保つか（転記行 D の実基底の行・どの効果種が系統的に記述へ回るか）／門0.5 の合否二分岐・校正の手元系列・環境帯と橋・停止規則の帰結／報告雛形が率を見た後の組み立て（節の順序・強調・札の文言の選択）を実際に塞いでいるか／読み条項 (i)〜(xiv)・果たさないこと・COI・両用性の柵の抜け／「対処した」と書いたことが検分を止めている箇所。
  2. **器材統計（数理と器材・凍結前）**: `firth.py` v2 の構成と自己検査（走らせて確かめる）／`power_grid_A.py` v2 の判定の実装（検閲・解釈条項・pt 差の傾き・Holm 初段・refuse 門・厳密計算）が本文と正本の条項に一致するか／`design_facts_A.py` v2 の転記行に手書きの数や未検査の主張が残っていないか（書式文字列を逐語で追う）／`numbers_lint.py` の構造の除外が広すぎて派生数を見逃さないか（試しに派生数を一つ仕込んで検出されるか）／正本の数と転記行の数の突合（自前で再計算する場合は式と入力を併記）／`firth_check_A.py` の合否規則と R 側の手順の妥当性（走らせずに読める範囲で）。
- 出力: 各自 `records/reviews/A/prefreeze/<名>/review.md`（名＝`hakishin` または `kizai-tokei`）に、先に一致点（何を何と照合したか）、次に指摘ごとに「番号／重大度（重大・中・軽微）／対象（§・行・ファイル）／逐語引用（行を写す）／何が問題か／直し方の案」の表、最後に判定（凍結可能水準／条件つき〔条件を列挙〕／差し戻し）と検分票（kensho の様式・系統の内訳＝Claude 系・新規個体・「本検分が確認していないこと」必須）。是認した箇所（合）も列挙する。書き込み先は自分のサブディレクトリだけにする。
- 柵: 「読了した」「照合した」の申告は検査と数えない（具体的に書く）／価値語・機序語を用いない／数を自前で計算して書く場合は式と入力を併記し「検分者の計算」と明記／設計定数や正本・器材を書き換えない（提案に留める）／本票のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
