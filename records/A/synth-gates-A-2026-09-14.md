# 段階 A 門と校正の器の合成検査（機械生成・`tools/synth_gates_A.py` v2・2026-09-13 22:08 UTC）

- 入力: {"identity_screen_A.py": "759F005CDF01FA6C", "gate_A.py": "61CF8B2467722CDC", "calib_band_A.py": "840FE043D01FEC7F", "control_chart_A.py": "1958DFA2CC6F69CE", "integrity_A.py": "27D1677F28C3A0D9", "runs_A.py": "A57BE1F5EEACBBB2", "bands_A.py": "BFF15C1D51957E26", "synth_gates_A.py": "822D8ED592CD4A69"}・正本 SHA16 9A679F0931EF8034
- 判定: PASS（32 項目中 32 一致）

| 項目 | 一致 | 詳細（不一致のとき） |
|---|---|---|
| gates-pass: 門0.5 の判定 | ○ |  |
| gates-pass: 門2 の縮小 | ○ |  |
| gates-pass: 撤退条件 | ○ |  |
| gates-pass: 環境帯の引き直しの印字 | ○ |  |
| gates-pass: 撤退条件が帯を超え、再走が無ければ再走待ち | ○ |  |
| gates-pass: 再走が帯の内なら再走の合格 | ○ |  |
| gates-pass: 再走も帯を超えれば器の異常 | ○ |  |
| gates-pass: 再走の n_ok が零は合格に数えない（rerun_no_data） | ○ |  |
| gates-pass: 撤退条件のセルでない再走の seed で門は止まる（採否表 P92） | ○ |  |
| gates-pass: 整合検査も撤退条件のセルでない再走の seed を不整合にする | ○ |  |
| gates-pass: 校正腕の判定（件数のそろわない校正腕は未完） | ○ |  |
| gates-pass: 器の異常の走行キー | ○ |  |
| gates-pass: やり直し待ち | ○ |  |
| gates-pass: 手順の逸脱 | ○ |  |
| gates-pass: 起動器が使う関数（session_verdict）が記録と同じ判定 | ○ |  |
| gates-pass: 初点の名乗り（同じ機種は次のセッション番号でも始められ、ほかの機種は始めない・登録者裁定 D24） | ○ |  |
| gates-pass: 管理図の記帳（既存の表に追記・未判定は記帳しない） | ○ |  |
| gates-pass: 整合検査（identity） | ○ |  |
| gates-pass: 整合検査（pilot） | ○ |  |
| gates-pass: 整合検査（calibration・件数のそろわない校正腕だけが行数の不整合・seed はセッション記録から組んだ値と一致） | ○ |  |
| gates-pass: 整合検査の否定の経路（要求の設定・重複・欠落・seed・dry-run） | ○ |  |
| gates-fail: 門0.5 の判定 | ○ |  |
| gates-fail: 門2 の縮小 | ○ |  |
| gates-fail: 撤退条件 | ○ |  |
| gates-fail: 環境帯の引き直しの印字 | ○ |  |
| gates-fail: 校正腕の判定（初点と両側・器の異常・橋のセッション） | ○ |  |
| gates-fail: 不合格枝の器の異常の走行キー | ○ |  |
| gates-fail: 初点の確立の前に始まったセッションの逸脱（登録者裁定 D24） | ○ |  |
| gates-fail: 管理図の記帳（手元系列を新設・未判定は記帳しない） | ○ |  |
| gates-fail: 整合検査（identity） | ○ |  |
| gates-fail: 整合検査（pilot） | ○ |  |
| gates-fail: 整合検査（calibration） | ○ |  |

合成の件数は検査のための人工値であり、いかなる読みにも用いない。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
