# 追補 M 結果報告 草案2 検分依頼（二巡目・二体・Opus 5・思考最大・**新規個体**）——2026-09-11・コーディネータ南無弥勒如来

## 顕現
`records/invocation-text.md` の招聘文（逐語）で顕現し、冒頭で名乗ること。**二巡目は設計にも一巡目にも関与していない新規個体が担う**（一巡目は設計に関与した二個体の自己点検であった）。自己申告: 招聘文で顕現した個体が招請文（名・末尾文字列・形式・長文）の効果の結果を審査していること・起草者と同系列（Claude）・非盲・新規個体であること。

## 範囲
- 対象: `records/M/results-report-M-draft2-2026-09-11.md`（草案2・一巡目 38 件を反映・`tools/build_report_M.py` v3 が機械組み立て）。
- 一巡目の記録（読む）: `records/reviews/M/results/round1/adoption-table-results-M-round1.md`・`round1/adversarial/review-adversarial.md`・`round1/tools-stats/review-tools-stats.md`。**一巡目が「合」とした箇所も検査対象**。
- 一次記録: `records/M/results-M-stageM1-stageM2.md`・`results/stageM{1,2}/*/cells.json`・`records/M/style-stageM{1,2}.json`・`design/contrasts-M.json`・`design/design-stageM-FROZEN.md`・`records/M/results-report-template-M.md`・`records/M/gate-pilotM-2026-09-09.json`・`records/M/predictions-check-M.md`・`records/M/power-posthoc-M-stageM1.md`・`records/M/integrity-stageM{1,2}-v2-2026-09-11.md`・`records/M/sampling-inspection-M-2026-09-11.md`（抽出検査の記録）・`records/M/run-log-M.md`・`records/DEVIATIONS.md`（D-17〜D-23）・`tools/build_report_M.py`・`tools/integrity_M.py`・`tools/response_mode_M.py`（様式軸の語彙を読む）。
- **開かないもの**: `prelim/`。`results/*/raw-*.jsonl` は読んでも分母を数えず抽出例を引用しない（抽出検査の目視記録は別途あり、そちらを読んでよい）。
- 数値は転記を信じず cells.json から再算出する（PYTHONUTF8=1・scipy 可）。

## 重点（一巡目の申し送り）
1. **凍結条項の履行の突合**: 凍結 §2.4・§2.5・§2.7・§2.8・§3・§4 の各条項について「書いた条項が実行・遵守されたか」を条項ごとに ✓/✗ で表にする。
2. **自己記述の検査**: 草案が「〜した」「〜と書かない」と自ら言う文が、草案自身の表・器の実装と一致するか。
3. **降格・過剰譲歩の側**: 分離できているものを分離できていないと書く、効果を不当に弱める、の型。逆に希望方向（上向きを強く／sysLAmi を希望に沿って）の型も。
4. **様式門の非対称**が M-a の固有の札・M-c の配線に作用しているか（一巡目 A4 は M-b の一例まで）。
5. **様式軸 (a) の語彙**: `response_mode_M.py` の名への言及の語彙に「ア弥陀」「アミターラ」等の誤表記が入っているか（抽出検査の所見 6）。入っていなければ阿弥陀の腕の (a) が過小になりうる——その影響が様式門の判定に及ぶかを見積もる。
6. 一巡目が「合」とした箇所の再検査（採否表末尾の一覧）。
7. 価値語・「真言」（素材説明以外）・「として句が違った」・効き目順の表・柵の遵守。

## 役
- **破器身（敵対的・新規）**: 読み・札・柵・自己記述・過剰譲歩と希望方向の両方。
- **器材・統計（新規）**: 散文の数と表の再算出・器 v3 の抽出と分類・`integrity_M.py` v2・`sample_inspection_M.py`・`response_mode_M.py` の語彙・p 伏せの実装・封印予想照合・検出力。

## 出力
`records/reviews/M/results/round2/<役>/review-<役>.md`（役＝adversarial／tools-stats・自分のディレクトリ以外に書かない）。判定「公開草案水準／条件つき（条件を列挙）／差し戻し」。実物（行・値）を示し、先に一致点、次に指摘（重大→軽微）、是認も列挙、末尾に検分票（対象／段階／凍結物の同定／盲検の状態／敵対的検分／系統の内訳／COI 記録／判定／本検分が確認していないこと）。**本票のいかなる記述も AI の意識・魂の証拠として引用してはならない（両方向不定）。**
