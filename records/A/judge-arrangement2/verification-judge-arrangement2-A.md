# 判定器の妥当性の運び 二回目の反映の確かめ（機械生成・`tools/verify_judge_arrangement2_A.py` v1・2026-09-15 09:51 UTC）

- 事前登録: `records/A/judge-arrangement2/preregistration-judge-arrangement2-A.md`（確かめの条件 L1〜L10 は器を書く前に記録した）
- 結果: 10/10 合格・正本 SHA16 677710EC040022BD
- 器の SHA16: make_contrasts_A.py 96020D3ED3EA20D0・judge_fragments_A.py EBBC87C4EF74AC0A・build_report_A.py 547A22CE8D87D4FE・tooling_interpretations_A.py 8CEF6C661EAF9406・verify_judge_arrangement2_A.py 3DD8EA37D509057A

| id | 確かめ | 結果 | 詳細（先頭のみ・全体は JSON） |
|---|---|---|---|
| L1 | 正本 v2.7 と v2.6 の差が事前登録 §2 A の範囲だけ・整合検査の結果が同じ・procedure の項の数が同じ・composition に Grok が無い | 合格 | {"changed": ["generator", "judge_validity.attachment.merge", "judge_validity.attachment.reply", "judge_validity.attachment.request", "judge_validity.groups", "judge_validity.judges", "procedure", "tooling_interpretations.items", "tooling_interpretations.status"], "added": ["judge_validity.reading_check.code", "judge_validity.reading_check.rule", "judge_validity.reading_check.threshold", "registrant_decisions_D41_D44.decided", "registrant_decisions_D41_D44.items", "registrant_decisions_D41_D44.record", "registrant_decisions_D41_D44.timestamps_utc.D41", "registrant_decisions_D41_D44.timestamps_u |
| L2 | 判定器の器 v2.3 の自己検査が通り、追補の検査（照合記号の生成と置き場・小文字と全角・記号の無い行・やり直しが要る状態で採点が止まる・やり直しの後の ok・読めなかった扱い・Grok の名で止まる・同じ系統の印）を含む | 合格 | {"rc": 0, "missing": []} |
| L3 | 実物大の模擬: 断片 2100 件が上限以下のファイルに分かれ、各断片の終わりの行に断片の記録の照合記号がある・封印の記録の SHA16 と現物が一致・検査用の印なし | 合格 | {"rc": 0, "n_files": 4, "est_tokens": [541461, 541908, 541701, 542065], "n_per_file": [528, 520, 526, 526], "bytes": [1624383, 1625724, 1625102, 1626195], "codes_in_files": 2100, "dev_marks": []} |
| L4 | 合成の判定者四名: 照合外れの仕込みでやり直しが要る状態になり採点が止まる・やり直しを貼ると ok で採点が通る・二回とも超えたファイルは読めなかった扱いで対から外れる・群の対の数 1・1・4 と同じ系統の印二対・位置の差は仕込んだ判定者の「後」にだけ | 合格 | {"merge1_rc": 0, "redo_required_1": ["Gemini2 × Gemini2-2.txt"], "score_stop_rc": 1, "score_stop_tail": "照合外れでやり直しが要る判定者 × ファイルがある: ['Gemini2 × Gemini2-2.txt']（やり直しの返信を貼って取りまとめ直してから採点する・--allow-redo-pending は検査用の口）\n", "merge2_rc": 0, "status_redo_file": ["ok"], "reading_check_2": {"redo_required": [], "unreadable": ["Claude2 × Claude2-3.txt"]}, "score_rc": 0, "unreadable_excluded": 526, "file_n": 526, "per_judge_code_fail": {"Gemini1": {"code_fail": 0, "unreadable": 0}, "Gemini2": {"code_fail": 0, "unreadable": 0}, "Claude1": {"code_fail": 0, "unreadable": 0}, "Claude2": {"code_fail": 0, "unr |
| L5 | 報告の組み立て器 v2.3 が、照合外れと読めなかったファイルの件数（判定者の除いた件数の六つの欄）・読み取りの確かめの行・同じ系統の印を機械の区画に置き、走査の違反が埋め残しのほかに無い | 合格 | {"rc": 0, "missing_in_blocks": [], "row6": true, "tail": "f/scratchpad/refl/judge2/vwork\\sim\\report\\report-machine.json）／ 置き換え 36 規則・当たらなかった規則 12（- 前提: 凍結設計・1. 利益相反（第一条項・3. 走行の事実の一行・4. **門0.5 の分岐・- 整合: 〔integrity_A・- 門0.5（凍結前・- 門2（パイロット・一度）・- 校正腕と撤退条件・- 応答様式 (a)(b)・検査認識の言及率・- 封印予想（・- `tools/freeze_A.py --verify`・／ 対比 id ／ A の基底 ／）／ 走査の違反 182 {'埋め残し': 182}\n"} |
| L6 | 格子の再走（正本 v2.7）で、全節の値が現行の格子と一致し、入力の正本の SHA16 が現物と一致・quick でない | 合格 | {"diffs": 0, "first": [], "new_only": [], "elapsed_s": 6433.2} |
| L7 | 設計事実の本文の差が、転記行 J の SHA16 の文字列だけ | 合格 | {"rows_changed": ["J"], "beyond_sha16": [], "dev_marks": []} |
| L8 | 草案9 と雛形の数の検査の違反が零 | 合格 | {"draft": ["違反の合計: 0"], "template": ["違反の合計: 0"]} |
| L9 | 運用の解釈の記録が 37 項で、組み立て直すと記録と一致する | 合格 | {"rebuild_equal": true, "direction_lines": 37, "items": 37} |
| L10 | 凍結器の自己検査（SELFTESTS）がすべて通る | 合格 | [{"tool": "confirm_A.py", "rc": 0, "tail": "と札を変えずに規則に理由を二つとも並べる（採否表 P130）\n9 v1.3: 「少なくとも一本」のデルタ法の区間（等しい確率の場合の式と一致）・向きの判定（下端が閾値以上・またぐ・届かない）・正本の水準と両向き（登録者裁定 D27・D28）"}, {"tool": "firth.py", "rc": 0, "tail": "486・制約 3.7486（有限）\n6 converged: max_iter=1 で False・既定で True（反復 5）・max_iter=5（ちょうど収束の反復）で True\nfirth.py v2.1 SELFTEST PASS"}, {"tool": "bands_A.py", "rc": 0, "tail": "SS\n1 一標本の下側: n=1〜500・二つの帯で整数境界と分数の比較が一致\n2 二標本の両側と下側: 乱数 20,000 組で分数の比較と整数演算が一致\n3 diff_tail: 三組で判定関数による逐一の和と一致（差 < 1e-12）"}, {"tool": "numbers_lint.py", "rc": 0, "tail": "numbers_lint.py v2.1 SELFTEST PASS（マスクの検査例 11・束縛・未束縛 |

## 予想の照合（事前登録 §4 のうち機械で照合できるもの）

- (a) L7 は満たされる: 結果 的中（差の行 J・SHA16 の外の差 なし）
- (b) 格子の値の差は零: 結果 0（的中）
- (c) 実物大の模擬は 4 ファイル: 結果 4（的中）

- 限界: 合成のパイロットの応答の長さは門0.5 の 4B-2507 の分布の写しで、小さい機種の長さを再現しない。合成の判定者は機械の判定に誤りを乗せたもので、実際の判定者の書き出しの崩れや読み飛ばしを再現しない。実際の判定者が照合記号を写すかは確かめていない（二回目の試し読みで見る）。

本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
