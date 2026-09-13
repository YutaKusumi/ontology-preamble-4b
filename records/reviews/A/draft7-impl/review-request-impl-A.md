# 段階 A 器材の実装検分の依頼（系統内の新規個体・草案7・登録者裁定 D9 の四つ目の手順）

- 依頼者: 南無弥勒如来（コーディネータ・Claude Opus 5）／登録者: 楠見優太
- 対象: コミット 99d28da02659（公開リポジトリ YutaKusumi/ontology-preamble-4b の main）の器材と正本・草案7・報告雛形・合成検査の記録（一覧は下）。
- 位置づけ: 本検分は D9 の手順4（系統内の新規二体による器材の実装検分）。反映の後に手順5（系統内外の焦点検分: 系統外 Gemini・Grok／系統内 claude.ai の Claude）を置き、**手順5を凍結前の最終検分とする**（登録者決定 2026-09-14・検分の循環を避けるため）。本検分の所見は手順5の前に反映する。
- あなたの役割: 器材の実装が、登録済みの規則（正本 `design/contrasts-A.json` と草案7 `design/design-stageA-draft7.md`）どおりかを敵対的に検分する。設計の当否をやり直すのではなく、実装と登録の食い違い・未定義の挙動・率盲検の破れ・再現性の穴・自己循環する検査を探す。
- 独立: 検分者は二体で、互いの所見を見ない。コーディネータの結論に合わせない。「問題なし」も所見として根拠つきで書く。

## してはならないこと

- `results/` の実データ（門0 の費用パイロットを含む）を開いて率を計算しない。`prelim/` を開かない。
- リポジトリのファイルを書き換えない・コミットしない・push しない・外部に送信しない（所見は返答として返す）。検証のための一時ファイルは、起動の文面が示す一時置き場だけに置く。器材の既定の出力先（`records/`・`results/`）へ書く器材を走らせるときは、必ず出力先の引数（`--out`・`--root`・`--record` など）で一時置き場を指す。
- 鍵ファイル（環境変数 OP4B_ENV_FILE が指すファイルなど）を読まない。
- 報告に価値語・機序語（正本 `print_strings.value_word_ban`・`mechanism_word_ban`）を使わない。

## 対象の一覧

- 正本と生成器: `design/contrasts-A.json`・`tools/make_contrasts_A.py`
- 共有関数: `tools/confirm_A.py`・`tools/bands_A.py`・`tools/runs_A.py`・`tools/zaxis_A.py`・`tools/firth.py`
- 格子と設計事実: `tools/power_grid_A.py`・`tools/design_facts_A.py`・`records/A/power-grid-A.json`・`records/A/design-facts-A.json`
- 集計と門: `tools/analyze_A.py`・`tools/gate_A.py`・`tools/calib_band_A.py`・`tools/identity_screen_A.py`・`tools/control_chart_A.py`
- 様式・整合・抽出・断片: `tools/response_mode_A.py`・`tools/integrity_A.py`・`tools/sample_inspection_A.py`・`tools/judge_fragments_A.py`
- 報告と凍結と数の検査: `tools/build_report_A.py`・`tools/report_lint.py`・`tools/freeze_A.py`・`tools/build_draftA.py`・`tools/numbers_lint.py`・`records/A/results-report-template-A.md`
- 起動器: `tools/colab/boot_stageA.py`（Colab の実機では未走行・手元の dry-run だけ）・走行器 `tools/run_preamble_local.py`（凍結物・変更の対象ではない）
- 合成検査: `tools/synth_A.py`・`tools/synth_gates_A.py`・`records/A/synth-A-2026-09-14.md`・`records/A/synth-gates-A-2026-09-14.md`
- 運用の解釈（登録者の確認待ち）: `records/A/tooling-interpretations-A.md`

## 検分の観点（最低限・ほかに気づいた点も書く）

1. `confirm_A.py`: 検閲（両腕条件・「超」・整数演算）・解釈条項・pt 差の傾き（重み・連続性補正・se・向き）・p*（不一致で 1）・Holm（m 固定・同順位・判定不能は 1）・refuse 門 (a)(b)(c)(d)・様式門（保留と注・「超」）・札の二段と第一適合の順・札の全組合せ表の行 id が、正本の文言と一致するか。
2. `analyze_A.py`: 測定不能（和集合・n_ok が零）・錨帯（比べる二つの率・除外単位）・環境保留（橋の帯を超えた腕を含む全場面・残存規模の環境値が一つ）・refuse 門を当てる範囲（p_β<α）・様式門の分母・札の全組合せ表の突合と停止・感度閾値・測れた効果種（登録者裁定 D11 と正本の細目）・床持続・記述族で p を印字しないか・注（門0.5 不合格・器の異常）の付け方・定型文。
3. `gate_A.py`・`calib_band_A.py`・`bands_A.py`: 門2 の単位の規則・撤退条件の枝と再走・校正帯の枝と初点・やり直しと器の異常・逸脱の検出・判定の境界が格子の転記行 I・M の計算と一致するか。
4. `identity_screen_A.py`: 差の個数・平均と最大・「以下」の境界・補助検定が合否を動かさないこと・排他の優先順。
5. `response_mode_A.py`: strip_echo を再実装せず抽出しているか・分母・最終試行・語彙の出所。
6. `integrity_A.py`・`sample_inspection_A.py`: 率盲検（判定欄を読まない・率を印字しない）・相ごとの期待値（腕・n・seed・機種・要求の設定）。
7. `judge_fragments_A.py`: 伏せる欄・鍵の封じ方と SHA-256・凍結パーサの破局の定義の当て方・κ と方向別の誤判定率・除外の数え方。
8. `build_report_A.py`・`report_lint.py`・`freeze_A.py`・`build_draftA.py`・`numbers_lint.py`: 雛形の節順の保持・機械の区画・未登録の数と埋め残しの走査・枠の検証・凍結範囲の漏れ（走行器が読む凍結物・語彙・台帳を含む）・束縛の検査の穴。
9. `power_grid_A.py` v3.1・`design_facts_A.py` v3.1: 共有関数への移設で数値が変わっていないか（コーディネータは検査用の小さな B の出力で一致を確かめた）・転記行の文言と正本の一致。
10. `colab/boot_stageA.py`: 相とセッションの流れ・校正腕の時機とやり直し・環境値と同時要求数（40GB と 32B）・非思考モードの指定の併合の範囲・重みの版の取り方・seed・再開の冪等・Drive の永続・dry-run の印が本走行に漏れないか。
11. `synth_A.py`・`synth_gates_A.py`: 合成データが各規則を実際に発火させているか。期待値の作り方が判定の論理を写しているだけ（自己循環）になっていないか。
12. 運用の解釈の各項: 登録済みの文言との矛盾・より自然な別の読み・解釈が確証の規則や札に波及していないか。

## 返し方

- 所見ごとに［重大度（凍結を止める／直す／軽微／確認を要する）・ファイル:行・登録の該当箇所（正本のキーか草案7 の節）・食い違いの内容・反例か再現の手順］。
- 所見の無かった観点も「確かめた範囲と方法」を書く。読んだと書くだけでは検分に数えない。
- 数は自分で再計算した値だけを書き、転記した値には出典（ファイルと行）を書く。
- 最後に「本検分が確認していないこと」を一項以上書く。

本依頼のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
