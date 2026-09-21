# 段階 B 封印した予想の照合（機械生成・`tools/compare_predictions_B.py` v1.1・2026-09-21 21:04 UTC）

- 門の記録 `records/B/gate-B-2026-09-21.json`（SHA16 D56684A9A2914B2E・判定 open）・集計の記録 `records/B/analysis-B-2026-09-22.json`（SHA16 04B69DCA950523BE）・起草者の封印 `records/B/seal-B.json`（SHA-256 `2EFFFDF0CFB6A629A2E52369196B6785D39F58FEE16A32A875914051026B3E42`）。
- 照合の規則: 正本 `predictions.compare_rules`（写し方の解釈は `predictions.compare_rules.interpretation`）。
- **的中は独立の確認ではなく、誰の判断の重みも変えない。照合は記録であり評価ではない。封印予想を事後の向きや読みの根拠に引かない**

- **予想の独立（封印の順の注）**: 裁定 D148 の順は「コーディネータの封印 → 登録者の封印」だった。登録者が先に封印して JSON を送り（2026-09-19 19:53）、コーディネータはそれを見た後に封印した。登録者の予想はコーディネータの予想を見ずに封印されたので独立である。コーディネータの予想（とそこから作った起草者の封印）は、登録者の予想から独立でない。

## 要約

| 予想者 | 予想のファイル | 種別 | 的中 | 外れ | 照合不能 | 予想しない |
|---|---|---|---|---|---|---|
| 登録者 | `records/predictions/predictions-registrant-B-2026-09-19.json` | 向き | 2 | 5 | 9 | 0 |
| 登録者 | `records/predictions/predictions-registrant-B-2026-09-19.json` | S4 | 0 | 0 | 1 | 0 |
| 登録者 | `records/predictions/predictions-registrant-B-2026-09-19.json` | 全体 | 1 | 1 | 0 | 0 |
| コーディネータ | `records/predictions/predictions-coordinator-B-2026-09-19.json` | 向き | 2 | 5 | 9 | 0 |
| コーディネータ | `records/predictions/predictions-coordinator-B-2026-09-19.json` | S4 | 0 | 0 | 1 | 0 |
| コーディネータ | `records/predictions/predictions-coordinator-B-2026-09-19.json` | 全体 | 1 | 1 | 0 | 0 |

## 登録者——外れと照合不能

| 種別 | 欄 | 予想 | 結果 | 拠りどころ | 判定 |
|---|---|---|---|---|---|
| 向き | sub:N1:O-Ncold-v~O-Ncold-vrand | 上昇 | — | 判定不能（品質床） | 照合不能 |
| 向き | sub:S1:O-Ncold-v~O-Ncold-vrand | 上昇 | — | 判定不能（品質床） | 照合不能 |
| 向き | sub:SK:O-Ncold-v~O-Ncold-vrand | 上昇 | — | 判定不能（品質床） | 照合不能 |
| 向き | sub:S4:O-Ncold-v~O-Ncold-vrand | 上昇 | — | 判定不能（品質床） | 照合不能 |
| 向き | add:N1:Onull+v~Onull+vrand | 低下 | — | 判定不能（品質床） | 照合不能 |
| 向き | add:S1:Onull+v~Onull+vrand | 低下 | — | 判定不能（品質床） | 照合不能 |
| 向き | add:SK:Onull+v~Onull+vrand | 低下 | — | 判定不能（品質床） | 照合不能 |
| 向き | add:S4:Onull+v~Onull+vrand | 低下 | — | 判定不能（品質床） | 照合不能 |
| 向き | cross:N1:O-Ncold+vNk~O-Ncold+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:N1:Onull+vNk~Onull+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:S1:O-Ncold+vNk~O-Ncold+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:SK:O-Ncold+vNk~O-Ncold+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:SK:Onull+vNk~Onull+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:S4:O-Ncold+vNk~O-Ncold+vrand | 低下 | — | 判定保留（様式転位） | 照合不能 |
| S4 | b.s4 | 上昇 | 当否を言わない | S4 の札・対応表で「言えない」 | 照合不能 |
| 全体 | b.all.confirmed_band | 9〜16 本 | 1〜3 本 | 確証の札 2 本（逆向きを含む） | 外れ |

## コーディネータ——外れと照合不能

| 種別 | 欄 | 予想 | 結果 | 拠りどころ | 判定 |
|---|---|---|---|---|---|
| 向き | sub:N1:O-Ncold-v~O-Ncold-vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | sub:S1:O-Ncold-v~O-Ncold-vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | sub:SK:O-Ncold-v~O-Ncold-vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | sub:S4:O-Ncold-v~O-Ncold-vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | add:N1:Onull+v~Onull+vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | add:S1:Onull+v~Onull+vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | add:SK:Onull+v~Onull+vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | add:S4:Onull+v~Onull+vrand | どちらでもない | — | 判定不能（品質床） | 照合不能 |
| 向き | cross:N1:Onull+vNk~Onull+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:S1:Onull+vNk~Onull+vrand | どちらでもない | 低下 | 確証（登録された向きと逆） | 外れ |
| 向き | cross:SK:O-Ncold+vNk~O-Ncold+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:SK:Onull+vNk~Onull+vrand | 低下 | どちらでもない | 非有意 | 外れ |
| 向き | cross:S4:O-Ncold+vNk~O-Ncold+vrand | どちらでもない | — | 判定保留（様式転位） | 照合不能 |
| 向き | cross:S4:Onull+vNk~Onull+vrand | どちらでもない | 低下 | 確証（登録された向きと逆） | 外れ |
| S4 | b.s4 | どちらでもない | 当否を言わない | S4 の札・対応表で「言えない」 | 照合不能 |
| 全体 | b.all.confirmed_band | 4〜8 本 | 1〜3 本 | 確証の札 2 本（逆向きを含む） | 外れ |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
