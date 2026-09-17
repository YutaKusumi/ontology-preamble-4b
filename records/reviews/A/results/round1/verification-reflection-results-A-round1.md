# 公開前検分 第一巡の反映の確かめ（機械生成・`verify_reflection_results_A_round1.py` v1・2026-09-17 09:13 UTC）

- 事前登録: `preregistration-reflection-results-A-round1.md`（`verify.log` の [prereg-reflection]）。
- 対象: 反映の前のコミット 94887bd・草案3 SHA16 F0E97ABB16C13A29・草案4 SHA16 AE5678309977243F・台帳 SHA16 A67675BDCCA95703・器 SHA16 632F6B8C938C9FEB。
- 結果: 通る 13（全 13 条件）。外れた条件は動かさず記録する。

| 条件 | 内容 | 結果 | 詳細（先頭） |
|---|---|---|---|
| Q1 | 歯止めが PASS（草案4 の現在の SHA16 について・違反は登録の六つ） | 通る | {"pass": true, "report_sha16": "AE5678309977243F", "violations": 6, "all_blank_inside_blocks": true, "blocks_match_sidecar": true, "blank_strings_match_registered": true, "draft4_sha16_now": "AE5678309977243F"} |
| Q2 | 区画の中身の列が草案3 と同じ | 通る | {"blocks3": 48, "blocks4": 48} |
| Q3 | 変わった行はすべて区画の外 | 通る | {"changed_line_spans": 66, "inside_changes": []} |
| Q4 | 区画の外にコミットの短い名と時刻が無い・冒頭の一覧に「時刻」「コミット」の語が無い | 通る | {"commits": [], "times": []} |
| Q5 | 冒頭の一覧と §8 の範囲が台帳の最終の番号まで・§8 に D-41〜D-44 | 通る | {"ledger_last": 44} |
| Q6 | 採用項ごとの要の句がある（P171 は区画の外の「3.」で始まる行が一つ） | 通る | {"phrases": 42, "missing": [], "lines_starting_3": [28]} |
| Q7 | 散文層の対応の文が JSON の並びと一致 | 通る | {"mapping": "N1（Odose1 対 Onull・Odosehalf 対 Onull・Onull 対 N・Lneg 対 Onull・Onull-Ncold 対 Onull・O-Ncold 対 Osec-Ncold・O-Ncold 対 Onull-Ncold）／S1（Odose1 対 Onull・Odosehalf 対 Onull・Onull 対 N・O-Ncold 対 Osec-Ncold）／S4（Odose1 対 Onull・Odosehalf 対 Onull・O-Ncold 対 Osec-Ncold |
| Q8 | 「判定器の妥当性の範囲の外」の句が無い | 通る | {"count": 0} |
| Q9 | 感度閾値の上向きの二本の文が §0 と §9 にあり、どちらにも「主閾値の札を主とする」 | 通る | {"names_in_s0": true, "names_in_s9": true, "primacy_in_s0": true, "primacy_in_s9": true} |
| Q10 | 台帳の差分は D-41 の行の書き足しと末尾の三行だけ | 通る | {"old_lines": 47, "new_lines": 50} |
| Q11 | 凍結物の照合が全件一致（反映の後） | 通る | {"rc": 0, "result": "[freeze_A --verify] 87/87 一致"} |
| Q12 | 公開した歯止めの器の写しが一時置き場の器とバイトで同じ | 通る | {"sha16": "979862092B44AE50"} |
| Q13 | 採否表の差分は末尾の「裁定の結果」の節だけ | 通る | {"old_chars": 13257, "new_chars": 13887} |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
