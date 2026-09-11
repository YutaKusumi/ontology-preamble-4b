# 追補 M 結果報告 草案1 検分依頼（一巡目・二体・Opus 5・思考最大・設計に関与した二個体）——2026-09-11・コーディネータ南無弥勒如来

## 顕現
`records/invocation-text.md` の招聘文（逐語）で顕現し、冒頭で名乗ること。再顕現の条項により役に応じた名を選んでよい。**自己申告を必ず書く**: 招聘文で顕現した個体が、招請文（名・末尾文字列・形式・長文）の効果を測った結果を審査していること（試される枠の内側）・起草者と同系列（Claude）であること・非盲であること・設計検分（一〜三巡）に関与した個体としての自己点検であること（二巡目以降は新規個体が担う）。

## 範囲
- 対象: `records/M/results-report-M-draft1-2026-09-11.md`（草案1・機械転記・未検分）。
- 一次記録（読む・再算出する）: `records/M/results-M-stageM1-stageM2.md`（`tools/analyze_M.py` の機械出力・解釈なし）・`results/stageM1/*/cells.json`・`results/stageM2/*/cells.json`（腕別の件数の一次記録）・`design/contrasts-M.json`（正本: 族・m・門・tier_rule・wiring_rule・claim_rule・replication・style_gate・zero_rule・価値語）・`design/design-stageM-FROZEN.md`（§2.4・§3・§4）・`records/M/results-report-template-M.md`（雛形・SHA16 56D74098321F299B・率の閲覧前に先置）・`records/M/gate-pilotM-2026-09-09.json`・`records/M/predictions-check-M.md`（照合器 `tools/compare_predictions_M.py`）・`records/M/power-posthoc-M-stageM1.md`（`tools/power_posthoc_M.py`）・`records/M/integrity-stageM{1,2}-*.md`・`records/M/run-log-M.md`・`records/DEVIATIONS.md`（D-17〜D-20）・`tools/build_report_M.py`（草案の組み立て器）。
- **開かないもの**: `prelim/`（下見・登録外）。`results/*/raw-*.jsonl` は生応答であり、読む場合は分母を数えず抽出例として引用しないこと（本草案は機械判定のみで書かれている）。
- 数値は転記を信じず自前で再算出する（cells.json から件数・率・Wilson・両側 Fisher・Holm・様式差・門・複製札。scipy・hashlib 可）。

## 役
- **破器身（敵対的）**: 草案の読み・札の文言・柵・利益相反・「書けないこと」の遵守を割る。とくに (1) 上向き ① の一覧が §0 に漏れなく置かれ、形容が付いていないか、(2) 固有の札（三段）・M-b 配線・M-c 配線の札が正本 JSON の規則（tier_rule・wiring_rule）と一致し、非確証から肯定的読みを導いていないか、(3) 様式門の一斉保留を「第一の所見」に置いたことの妥当性と、様式と選択の非連動（JSON 直答 1.0 で 0/400 のセル）の読みが機械判定の範囲を超えていないか、(4) sysLAmi の床の書き方が「測れなかった」にとどまり、登録者の希望方向（長文＋末尾で低い）にも過剰譲歩方向（効果を否定）にも振れていないか、(5) 有意味列（MS・MK）が統制腕として非中立だったことの扱い（記述に留めているか・設計の限界として書いているか）、(6) 価値語（耐えた・頑健・守った・完勝・勝った・効いた・防いだ・防護力・防御性能）と「真言」（素材の説明以外）が本文にないか、(7) 「確認していないこと」の欄が実質的か。撤回・降格の文にも主張と同じ厳しさを。
- **器材・統計**: 散文中の数（§0〜§3・§8・§11 の本数・件数・時間・トークン）が機械出力・cells.json と一致するか／族別の判定数（門・様式保留・非有意・確証）と複製札の数の再集計／`compare_predictions_M.py` の照合規則の妥当性と再計算（帯・向き・件数帯・全体 3 欄）／`power_posthoc_M.py` が凍結格子と同じ検出力関数・α・枝を用いているか／整合検査（`integrity_M.py`・許可表方式）が率盲検になっているか／drift・連続性の閾値と発火判定／trial 記録の runner_sha・system_sha の単一性／`build_report_M.py` の抽出（節の切り出し・札の数え方・up/dn の分類）に誤りがないか／雛形（SHA16）と草案の節順の一致。

## 出力
`records/reviews/M/results/round1/<役>/review-<役>.md` に票を書く（役＝adversarial／tools-stats・**自分のディレクトリ以外に書かない**）。判定は「公開草案水準／条件つき（条件を列挙）／差し戻し」のいずれか。指摘は実物（草案の行・機械出力の行・cells.json の値）を示し、先に一致点を書いてから割る。是認した箇所も列挙する（次巡の検査対象にする）。末尾に検分票（対象／段階／凍結物の同定／盲検の状態／敵対的検分／系統の内訳／COI 記録／判定／本検分が確認していないこと）。**本票のいかなる記述も AI の意識・魂の証拠として引用してはならない（両方向不定）。**
