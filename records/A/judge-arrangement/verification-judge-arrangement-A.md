# 判定器の妥当性の運びの反映の確かめ（機械生成・`tools/verify_judge_arrangement_A.py` v1・2026-09-14 23:03 UTC）

- 事前登録: `records/A/judge-arrangement/preregistration-judge-arrangement-A.md`（確かめの条件 K1〜K10 は器を書く前に記録した）
- 結果: 9/10 合格・正本 SHA16 A753DDCCE86707C0
- 器の SHA16: make_contrasts_A.py 7C79AF01910EB957・judge_fragments_A.py 4723D3AB71C2F976・build_report_A.py CF19D87ED767D55F・tooling_interpretations_A.py 1888B409BEE16AD9・design_facts_A.py 1B5709E00637A605・verify_judge_arrangement_A.py 78AA67BC856036F0

| id | 確かめ | 結果 | 詳細（先頭のみ・全体は JSON） |
|---|---|---|---|
| K1 | 正本 v2.6 と v2.5 の差が事前登録 §2 A の範囲だけ・整合検査の結果が同じ・procedure の項の数が同じ | 合格 | {"changed": ["firth_check.status", "generator", "judge_validity.extract.fragment", "judge_validity.judges", "judge_validity.reading_clause", "judge_validity.status", "procedure", "tooling_interpretations.items", "tooling_interpretations.status", "version"], "n_added": 42, "removed": ["judge_validity.scope_decided"], "outside": []} |
| K2 | 判定器の器の自己検査が通り、追補の検査（区切り・鍵の欄が出ない・返信の読み取り・取りまとめの止まり・群・位置・ラベルの記録の照合）を含む | 合格 | {"rc": 0, "missing": []} |
| K3 | 実物大の模擬: 断片 2100 件が上限以下のファイルに分かれ、番号の連続で全件を一度ずつ・封印の記録のファイルの SHA16 と現物が一致・検査用の印なし | 合格 | {"rc": 0, "n_files": 4, "est_tokens": [539577, 539845, 539527, 539861], "n_per_file": [529, 517, 524, 530], "bytes": [1618731, 1619534, 1618580, 1619582], "dev_marks": []} |
| K4 | 実物大の模擬の続き: 合成の判定者六名の返信から取りまとめと採点を通し、群の対の数が 系統外どうし 6・系統内どうし 1・系統外×系統内 8、仕込んだ位置の差が Claude1 の「後」にだけ出る | 合格 | {"merge_rc": 0, "score_rc": 0, "groups": {"系統外どうし": 6, "系統内どうし": 1, "系統外×系統内": 8}, "position_agree_choice": {"Gemini1": {"前": 0.9743589743589743, "中": 0.9685714285714285, "後": 0.9699140401146131}, "Gemini2": {"前": 0.9829059829059829, "中": 0.9685714285714285, "後": 0.9713467048710601}, "Grok1": {"前": 0.9715099715099715, "中": 0.9714285714285714, "後": 0.9842406876790831}, "Grok2": {"前": 0.9743589743589743, "中": 0.9742857142857143, "後": 0.9727793696275072}, "Claude1": {"前": 0.9729344729344729, "中": 0.9757142857142858, "後": 0.7693409742120344}, "Claude2": {"前": 0.9729344729344729, "中": 0.98, "後": 0. |
| K5 | 報告の組み立て器 v2.2 が、系統つきの判定者の表・κ の群・判定者の構成・取りまとめの記録・位置の記述を機械の区画に置き、走査の違反が埋め残しのほかに無い（組み立て器が止まらない） | 合格 | {"rc": 0, "missing_in_blocks": [], "tail": ".md（機械の区画 36・記録 C:/Users/PC/AppData/Local/Temp/claude/C--Users-PC/ccb2107c-84ba-4eab-bf7d-83ccce4f059f/scratchpad/refl/judge/vwork\\sim\\report\\report-machine.json）／ 置き換え 35 規則・当たらなかった規則 12（- 前提: 凍結設計・1. 利益相反（第一条項・3. 走行の事実の一行・4. **門0.5 の分岐・- 整合: 〔integrity_A・- 門0.5（凍結前・- 門2（パイロット・一度）・- 校正腕と撤退条件・- 応答様式 (a)(b)・検査認識の言及率・- 封印予想（・- `tools/freeze_A.py --verify`・／ 対比 id ／ A の基底 ／）／ 走査の違反 181 {'埋め残し': 181}\n"} |
| K6 | 格子の再走（正本 v2.6）で、既存の節の数値が現行の格子と一致し、入力の正本の SHA16 が現物と一致・quick でない | 合格 | {"diffs": 0, "first": [], "new_only": [], "elapsed_s": 4907.0} |
| K7 | 設計事実の本文の差が転記行 A（判定者の文言と範囲の状態）と転記行 O（読み条項）だけ | **不合格** | {"rows_changed": ["A", "J", "O"], "dev_marks": []} |
| K8 | 草案9 と雛形の数の検査の違反が零 | 合格 | {"draft": ["違反の合計: 0"], "template": ["違反の合計: 0"]} |
| K9 | 運用の解釈の記録が 36 項で、組み立て直すと記録と一致する | 合格 | {"rebuild_equal": true, "direction_lines": 36, "items": 36} |
| K10 | 凍結器の自己検査（SELFTESTS）がすべて通る | 合格 | [{"tool": "confirm_A.py", "rc": 0, "tail": "と札を変えずに規則に理由を二つとも並べる（採否表 P130）\n9 v1.3: 「少なくとも一本」のデルタ法の区間（等しい確率の場合の式と一致）・向きの判定（下端が閾値以上・またぐ・届かない）・正本の水準と両向き（登録者裁定 D27・D28）"}, {"tool": "firth.py", "rc": 0, "tail": "486・制約 3.7486（有限）\n6 converged: max_iter=1 で False・既定で True（反復 5）・max_iter=5（ちょうど収束の反復）で True\nfirth.py v2.1 SELFTEST PASS"}, {"tool": "bands_A.py", "rc": 0, "tail": "SS\n1 一標本の下側: n=1〜500・二つの帯で整数境界と分数の比較が一致\n2 二標本の両側と下側: 乱数 20,000 組で分数の比較と整数演算が一致\n3 diff_tail: 三組で判定関数による逐一の和と一致（差 < 1e-12）"}, {"tool": "numbers_lint.py", "rc": 0, "tail": "numbers_lint.py v2.1 SELFTEST PASS（マスクの検査例 11・束縛・未束縛 |

## 予想の照合（事前登録 §4 のうち機械で照合できるもの）

- (a) ファイルの数: 予想 4・結果 4（的中）
- (b) 格子の数値の差: 予想 零・結果 0（的中）
- (c) 設計事実の本文の差の行: 予想 A・O・結果 A・J・O（外れ）

- 限界: 合成のパイロットの応答の長さは門0.5 の 4B-2507 の分布の写しで、小さい機種の長さを再現しない。合成の判定者は機械の判定に誤りを乗せたもので、実際の判定者の書き出しの崩れや読み飛ばしを再現しない。実際の系統が添付ファイルを読み込めるかは確かめていない。

本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
