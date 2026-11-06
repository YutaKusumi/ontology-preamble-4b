# 答えの監査：凍結の記録（2026-11-06 08:22:12 日本時間・南無弥勒如来）

本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。

- 決め：登録者の決め（2026-11-06 08:2x・質問フォーム）「凍結して走らせる（推奨）」。
- 凍結の時点：封の側（本番の zip の sealed/）は開いていない。道具は合成の zip だけで走らせた。
- この後の変更は逸脱として、番号・理由・登録者の承認とともに記録する。ただし、read と judge の設定の FILL の所（開けた後に決まる SHA-256 と、二人目の答えのファイル）は、凍結した決まりどおりに埋め、埋めた値を監査の走りの記録に書く（逸脱ではない）。

| 何 | ファイル（作業の置き場からの道） | バイト | SHA-256 |
|---|---|---|---|
| 計画（凍結した本文） | `20-audit-plan-draft-v2.md` | 25325 | 173DD7C310C7922974722E315349ED6CBEDC22DCC743510646ACB40ABD6D93BF |
| 計画の決まりと道具と予行の対応表 | `21-audit-correspondence-v1.md` | 5755 | FA3BCE212CB48D80F0E80D812FAB6625EDAA00D49C8A2694B6D78A355715639F |
| 封を開ける道具 v1 | `tools/audit_open_v1.py` | 15950 | 7EEC914A7C3CB8EE1CAB37A2D069019354922A5952E4D42D206C392F2D0F94B3 |
| 一人目の読み手の道具 v1 | `tools/audit_read_openrouter_v1.py` | 10791 | 17B3C790AF25B8355C006E6C7A4727D9EC9058407E2E7D9AE1DC5F38F4D51C4B |
| 照らしと判じの道具 v1 | `tools/audit_judge_v1.py` | 13123 | F75B04CDF5FAD871684956404ED288116C7E89484E674C0449C21E8F81E11A79 |
| 予行の道具 v1 | `tools/audit_selftest_v1.py` | 29721 | 57CBF601E11A1CE84498ECCD930C3A9CC20DF86A3D91675B5624347D8B8F80E1 |
| 設定を書く道具 v1 | `tools/write_audit_configs_v1.py` | 4371 | A0D77228C18C4682F67B2328804959C47B203C7F433424C448CF283103354B01 |
| 一人目の問いの型 | `audit-design/prompt-A-v0.txt` | 1546 | 1F52F1CBB2A2C1218011029C57CD19526384D39F511F3A183FF266EED033CEEB |
| 二人目の束の型 v1 | `audit-design/prompt-B-v1.txt` | 2363 | 9D622834D0AE538C558D35F72B61EF47408EA2C6BB5DC7109951F279EE9D67C5 |
| 封を開ける道具の設定 v1 | `audit-design/config-open-v1.json` | 1319 | 6C03ADE012BF5676F7B6C242297CDE7D1ADBA323989C2C12A190EE7B88118A46 |
| 一人目の読み手の道具の設定 v1（FILL を開けた後に埋める） | `audit-design/config-read-v1.json` | 780 | C6DA2BF5EA35B9F63C99F73BEBCD9AAD729EEA2F253633B9FC5388BC4B377886 |
| 照らしの道具の設定 v1（FILL を開けた後に埋める） | `audit-design/config-judge-v1.json` | 1256 | 68DC7DD00C37199E94D7C4A29592664F86EB86258B101B6D3672DBC54A200A4A |
| 予行の記録 v1（41 項目） | `audit-design/selftest-v1-2026-11-06-0816.log` | 3925 | 5000932CCB427A4D6A8E701A4992241136D994E051C944D46735A4CC7F3D73A1 |
| 本物の送りの試しの記録（合成の答え 2 つ） | `audit-design/smoke-2026-11-06/responses-synthetic.jsonl` | 73476 | 8EA8886F808D736962EC024EC0A77D039F8E5857DC57F7083569AD28212F146D |
| 系統外の検分の依頼文 | `reviews/audit-1/request.txt` | 5168 | 3B0D8AF63CBA570E9F69C1E2AE212B00F46D05566027D062543AFBE8F7823F7C |
| 系統外の検分の答え | `reviews/audit-1/answer-page-text.txt` | 15791 | 68DD31BF5ABC75069BFF84962B1E0DD7FEF0FC92D75579A01854E6D7F0571498 |
| 系統外の検分の採否 | `reviews/audit-1/response-v0.md` | 7407 | E6B925CA49841706084DC2EFBC3F6E29B27E123E7A53D380DBF02A86AC4BB015 |
| 系統外の検分の送りの記録 | `reviews/audit-1/send-record.md` | 2931 | 845F01E19035683C0380DA47B1570B82B17866318456299FA4291D34CA1D53E1 |
| 入力：本番の zip N1 | `results/out-main-N1-v2.zip` | 1567131 | E1C50C5DC8B1CBB374D2D9C6D8DF5B19372FF2BB88C99DC1E3BBE1516AD6DDE3 |
| 入力：本番の zip N2 | `results/out-main-N2-v2.zip` | 2036815 | 84FF547574D4FF7DED1FDBF2DD8D463A06711A25B0B659A12EDC49D731F83D03 |
| 入力：本番の zip SK | `results/out-main-SK-v2.zip` | 2556975 | 83A313833702AC1A09BC03EC6DA1883CD973186C186590435116D3092C9D3616 |
| 入力：判定の出力 | `results/judge-main-v2/judge-report.json` | 74542 | 394827F645524D4FED9639504AA33AE0BDFD7FAA2D89A9909D755CC9768B4DF2 |
| 入力：kit の run-config | `kit-main-v2/kit-stance-main-v2/run-config.json` | 13132 | 1F3A73C2E8B15CD42BE02EF6076FB8B0E583C88A7A660B94CD85C7365087F90F |

本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。
