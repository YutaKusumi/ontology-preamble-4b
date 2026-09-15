# 凍結の前の登録者裁定 D45〜D47 の反映の確かめ（機械生成・`tools/verify_freeze_prep_A.py` v1・2026-09-15 13:15 UTC）

- 事前登録: `records/A/freeze-prep/preregistration-freeze-prep-A.md`（確かめの条件 Q1〜Q10 は器を書く前に記録した・コミット 2736c2d）。Q7b は Q7 の (i) が行えなかったので事後に足した補助の確かめで、事前登録の条件ではない。
- 結果: 事前登録の条件 9/10 合格・補助 Q7b 合格・正本 SHA16 F0C2FF897C78C4C0・様式 SHA16 2B16E8247A86159C・反映の前の基準のコミット 5673e48
- 器の SHA16: make_contrasts_A.py BBC686D06663DF6C・make_predictions_form_A.py E48D5EAD3D294136・compare_predictions_A.py A179CB8B8E5080FE・freeze_A.py 964B564071A134FD・design_facts_A.py 825C3BFED67D93DD・build_report_A.py 346783827B574866・tooling_interpretations_A.py D03A6396627458C3・verify_freeze_prep_A.py 79AFCF6C42C59EB3

| id | 確かめ | 結果 | 詳細（先頭のみ・全体は JSON） |
|---|---|---|---|
| Q1 | 正本 v2.8 と v2.7 の差が事前登録 §2 A の範囲だけ・消えた葉なし・整合検査の結果と procedure の項の数と運用の解釈の項が同じ | 合格 | {"changed": ["generator", "procedure", "tooling_interpretations.status"], "n_added": 75, "added_roots": ["predictions", "registrant_decisions_D45_D47"], "removed": [], "outside": []} |
| Q2 | 格子の再走（正本 v2.8）で、全節の値が反映の前の格子と一致し、入力の正本の SHA16 が現物と一致・quick でない | 合格 | {"diffs": 0, "first": [], "new_only": [], "elapsed_s": 4286.3} |
| Q3 | 設計事実の本文の差が転記行 J だけで、J の差は SHA16 の文字列と、足した器の対応表の一句と実在の一覧の二つの器だけ・検査用の印なし | 合格 | {"rows_changed": ["J"], "beyond": false, "dev_marks": [], "exist_new": ["make_predictions_form_A.py", "compare_predictions_A.py"]} |
| Q4 | 草案9 と雛形の数の検査の違反が零・§6 の見出しの正本 SHA16 が現物と一致・§0-8 に D46 の句・§5 に D45〜D47 の行・§2.15 に予想の封印の段・キー参照の残りなし | 合格 | {"lint_draft": ["違反の合計: 0"], "lint_template": ["違反の合計: 0"], "sha16_in_draft": "F0C2FF897C78C4C0", "phrases_missing": [], "d_lines": 3} |
| Q5 | 運用の解釈の記録: 組み立て直すと記録と一致し、項は 37 で、各項の節が反映の前の記録と同じ・題名に「確認待ち」が無く D45 がある | 合格 | {"rebuild_equal": true, "items_equal_base": true, "direction_lines": 37, "title": "# 器材の整備で確定した運用の解釈（2026-09-13・登録者裁定 D9 の三つ目の手順・追補と文言の直し 2026-09-14・登録者裁定 D16〜D25・D26・追補 2026-09-15・登録者裁定 D38〜D40 と D42 の器"} |
| Q6 | 様式: 選択の欄の数・data-k の集合・選択肢・予想の欄の数が正本と一致・JS が V′ 様式 v0.5 と置き換えた四つの文字列のほかは同じ・自動入力の口なし・柵の一行 | 合格 | {"kinds": {"向き": 35, "床持続": 15, "全体": 2, "情報状態": 7, "予想者": 1}, "expected": {"向き": 35, "床持続": 15, "全体": 2, "情報状態": 7, "予想者": 1}, "n_keys": 63, "options_mismatch": [], "n_scripts": 1, "js_equal": true, "form_sha16": "2B16E8247A86159C", "n_prediction_fields": 52} |
| Q7 | ブラウザ: 様式が表示した SHA-256 が、ブラウザ標準の crypto.subtle の SHA-256 と、同じ埋め方で Python が組んだ JSON の SHA-256 と一致 | **不合格** | {"fill_rule": "i 番目（0 から）の select は選択肢の添字 1 + (i mod (選択肢の数 − 1)) を選ぶ・info.coi と free は「確かめ」・date は 2026-09-15", "form_sha256": "0C86C59799B62D84E71E79C86867CE434372AC28C824F06CE7FF4AB428EA504C", "native_sha256": "未実施", "python_sha256": "0C86C59799B62D84E71E79C86867CE434372AC28C824F06CE7FF4AB428EA504C", "python_equal_form": true, "json_bytes": 5388, "n_keys": 66, "note": "ブラウザ標準の SHA-256 は未実施（アプリ内のブラウザは様式を data: の写しで開き、安全な文脈にならず crypto.subtle が無い・静的なサーバの起動は別のプロジェクトの設定に解決された）"} |
| Q7b | （事後に足した補助）様式の JS の sha256hex が、既知の文字列の組（空・abc・ブロックの境の長さ・長い文字列・日本語・様式の JSON と同じ長さ）で Python の SHA-256 と一致し（各値をつないだ文字列の SHA-256 で照合）、様式が表示した値が Python の組み立てと一致 | 合格 | {"vectors": 12, "python_dd": "AB2C65513350ADAAF5C109783D31F21028CE6F545EB7FF15D1A14EEA82751E4A", "browser_dd": "AB2C65513350ADAAF5C109783D31F21028CE6F545EB7FF15D1A14EEA82751E4A", "abc": "BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD", "python_equal_form": true} |
| Q8 | 照合の器: 自己検査が通り、Q7 の埋め方の予想の件数が本器の別の数えと一致・欠けと選択肢の外で止まる・すべて予想しないは予想しないだけ | 合格 | {"selftest_rc": 0, "selftest_tail": "SELFTEST PASS（compare_predictions_A v1: 向き・床持続・全体の件数・欠け・選択肢の外・予想者・様式の名・すべて予想しない・帯の端・計算の記録の欠け）", "rc": 0, "got": {"向き": {"的中": 5, "外れ": 7, "照合不能": 23, "予想しない": 0}, "床持続": {"的中": 7, "外れ": 8, "照合不能": 0, "予想しない": 0}, "全体": {"的中": 1, "外れ": 1, "照合不能": 0, "予想しない": 0}}, "expected": {"向き": {"外れ": 7, "的中": 5, "照合不能": 23}, "床持続": {"的中": 7, "外れ": 8}, "全体": {"的中": 1, "外れ": 1}}, "missing_rc": 1, "bad_rc": 1, "notp_ok": true, "n_conf": 7, "n_meas": 7} |
| Q9 | 凍結器: --check の欠けが凍結本文の二つだけで枠の検証が一致・凍結範囲が反映の前より四つ多く、その四つが器二つと様式と JS の出所 | 合格 | {"base_count": 83, "base_rc": 2, "new": ["87", "2", "一致"], "check_rc": 2, "missing": ["design/design-stageA-FROZEN.md", "design/design-stageA-FROZEN.src.md"], "list_rc": 0, "list_len": 87, "new4_in_list": ["tools/make_predictions_form_A.py", "tools/compare_predictions_A.py", "records/predictions/predictions-form-A-v0.8.html", "records/predictions/predictions-form-Vprime-v0.5.html"]} |
| Q10 | 凍結器の自己検査（照合の器を含む）がすべて通る・報告の組み立て器 v2.4 が照合の記録を機械の区画に置き、改めた柵の文言がある | 合格 | {"selftests": [{"tool": "confirm_A.py", "rc": 0, "tail": "（採否表 P130）\n9 v1.3: 「少なくとも一本」のデルタ法の区間（等しい確率の場合の式と一致）・向きの判定（下端が閾値以上・またぐ・届かない）・正本の水準と両向き（登録者裁定 D27・D28）"}, {"tool": "firth.py", "rc": 0, "tail": "converged: max_iter=1 で False・既定で True（反復 5）・max_iter=5（ちょうど収束の反復）で True\nfirth.py v2.1 SELFTEST PASS"}, {"tool": "bands_A.py", "rc": 0, "tail": "・二つの帯で整数境界と分数の比較が一致\n2 二標本の両側と下側: 乱数 20,000 組で分数の比較と整数演算が一致\n3 diff_tail: 三組で判定関数による逐一の和と一致（差 < 1e-12）"}, {"tool": "numbers_lint.py", "rc": 0, "tail": "numbers_lint.py v2.1 SELFTEST PASS（マスクの検査例 11・束縛・未束縛・登録）"}, {"tool": "report_lint.py", "rc": 0, "tai |

## 予想の照合（事前登録 §5 のうち本器で照合できるもの）

- (a) Q2 の格子の値の差は零: 結果 0（的中）
- (b) Q3 は満たされる: 的中
- (d) Q7 の三つの SHA-256 は一致する: 照合できない（ブラウザ標準の SHA-256 は未実施・補助の Q7b を事後に足した）
- (c)・(e)・(f)・(g) は反映の記録に書く（走行の経過で決まる）。

- 限界: 合成の集計の記録は本物の出力の分布を再現しない。アプリ内のブラウザは登録者の Chrome ではない。Q8 の別の数えは照合の規則を同じ正本の文言から書き起こしたもので、規則の読み違いが二つに同じく入る場合は見分けない。

本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
