# 段階 B 最後の系統外の巡の直しの監査（**直す前**・2026-09-19 12:34 日本時間）

- 器: `verify_fixes_B_final.py`（枠は `preregistration-fix-audit-B-final.md`・**器を書く前に登録した**）。
- 正本 SHA16 78CFA830BA128474。合成データを門と集計器に通した回: 通った。
- 数: 直っていない 29（全 29 行）。
- **直す前に「直っていない」と出なかった検査（働いていない印）**: 無し。

| P | 裁定 | 何を | 判定 | 証拠 |
|---|---|---|---|---|
| P384 | D133 | td の特異性の規則 | 直っていない | 検査が例外で止まった: AttributeError: module 'rules_B' has no attribute 'td_specificity_family' |
| P385 | D134 | S4 の三分岐の前の門 | 直っていない | 検査が例外で止まった: AttributeError: module 'rules_B' has no attribute 's4_gates' |
| P386 | D135 | S4 の札と封印の照合 | 直っていない | 検査が例外で止まった: AttributeError: module 'rules_B' has no attribute 's4_seal_match' |
| P387 | D136 | S4 の効き目・札の文言・相対の大きさ | 直っていない | 札に効き目 False・集計の記録に相対と動作特性 False・読み条項 False・§5-補 から消えた False |
| P391 | D137 | 品質床の下限の手当てと多重性の数 | 直っていない | 検査が例外で止まった: AttributeError: module 'rules_B' has no attribute 'qf_null_rate' |
| P392 | D138 | 品質床の前置き | 直っていない | 正本の入力の条（付ける・戻る条件）True・草案13B が束縛 False |
| P395 | D139 | D132 の読みの参照の行 | 直っていない | 検査が例外で止まった: AttributeError: module 'layers_B' has no attribute 'reference_rows_selftest' |
| P398 | D140 | ランダム方向の割り当てを交互に | 直っていない | 番号 0〜5 の方向 [0, 0, 0, 0, 0, 0]・各方向の数 [67, 67, 66]（等分 [67, 67, 66]） |
| P400 | D141 | ‖v̂‖/‖h‖ の帰結 | 直っていない | 帰結の文 False・主位置だけの限界 False |
| P402 | D142 | top_k の決め方 | 直っていない | 決め方の条 False・凍結時に記帳する値 False・§5-補 False |
| P411 | D143 | 同一性選別に Osec-Ncold | 直っていない | 比べる腕に Osec-Ncold False・差の数 30（腕 10 × 三つの率） |
| P389 | D118・D127 | 転記行 D・E と正本の旧い鍵 | 直っていない | 転記行 D の旧い規則 True・器の値 0.049 が行にある False・正本の power_min True・転記行 E の「分母＝200」True |
| P390 | D98・D119・D127 | 草案の古い文 | 直っていない | 草案13B に残る古い文 []（草案13B 無し） |
| P393 | — | 層の割合と添字の対応 | 直っていない | 検査が例外で止まった: AttributeError: module 'run_stageB_local' has no attribute 'layer_binding_ok' |
| P394 | — | 副位置の加えた量 | 直っていない | 正本の一行 False・走行の記録の欄 False |
| P396 | — | 決定性 (ii) のバッチの組成 | 直っていない | 決定性 (ii) がバッチの組成を変えた値を比べる False |
| P397 | — | 自己検査の締めの行 | 直っていない | torch を隠した口の終了コード 0・締めの行が hook を通ったと言う True（…録の欄 30・様式と言及と refuse の分類とループ（段階 A の凍結した関数）・hook の帯と復号の段と行ごとの方向: すべて通った） |
| P399 | — | 等質性の注の帰無の率 | 直っていない | 正本の帰無の率 無し・雛形が束縛 False |
| P401 | D94・D125 | 様式門の札 | 直っていない | 検査が例外で止まった: AttributeError: module 'rules_B' has no attribute 'style_hold_label' |
| P403 | D126・D130 | 検査用の口と報告の照合と相手の重複 | 直っていない | 集計器の --no-gate True・報告の器が門の記録の SHA を照らす False・集計器の相手の重複の番人 False |
| P404 | — | 起点の一つの関数 | 直っていない | 走行器が呼ぶ False・介入の器の自己検査が検べる False |
| P405 | — | 生成器の古い数 | 直っていない | 生成器の古い数 ある |
| P406 | — | バッチの行数 | 直っていない | 走行器の書き込み False・正本の試行の記録の欄 False |
| P409 | — | 層別の計数の死んだ行 | 直っていない | 層別の計数の常に零の行 ある |
| P410 | D110 | 報告の管理図の要約 | 直っていない | 雛形の節 False・合成データから組んだ報告に要約が出た回 None |
| P412 | — | D123 の理由の注 | 直っていない | 正本の注 False |
| X1 | — | 照合の器が最後の巡の採否表を読む | 直っていない | 最後の巡の採否表の P384 の出所 set() |
| X2 | D131 | 最後の巡の後の直しの限界 | 直っていない | 正本 False・草案13B False・雛形 False |
| X3 | D133〜D143 | 草案13B と裁定の逐語 | 直っていない | 草案13B 無し・§5-9 と逐語の uuid False・§5-補 から決まった二件が消えた True |

本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
