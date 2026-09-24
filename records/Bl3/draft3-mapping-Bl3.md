# B-lens 層三の草案3 の対応の記録（機械で確かめた・`records/Bl3/draft3_mapping_Bl3.py`）

- 採否表: `records/reviews/Bl3/design-round2/adoption-table-Bl3-design-r2.md`（SHA16 F94505B624402C3E）の行 P667〜P698。採否・票・所見・案は採否表から器が読んだ。
- 受けた所: 正本 `design/contrasts-Bl3.json`（SHA16 AD75819E0AF4F898・版 draft3-2026-09-24）・草案3 `design/design-Bl3-draft3.md`（SHA16 40EA2347F00AC2E1）・設計事実 `records/Bl3/design-facts-Bl3.json`（SHA16 5D552B2366143FD2）・露出の記録 `records/Bl3/exposure-before-seal-Bl3.md`（SHA16 8A5E02D58D696489）・G2 の票 `records/reviews/Bl3/design-round2/gemini-2/review.md`（SHA16 7BCC107136B8A661）。受けた所は起草者が並べ、器がその実在を確かめた（中身の当否は確かめていない）。
- 次の裁定の番号（正本 `numbering.rulings_next`）が、正本の台帳の最後の番号の続きであることも器が確かめた。
- 見つからなかったもの: 0 件。

| 採否 | 票・所見 | 案 | 草案3 で受けた所 | 実在 |
|---|---|---|---|---|
| P667 | G1-1.1・G2-Ⅰ・C1-直り・C2-直り | 是認 | 是認（半分にとどまった直しは下の行で受けた） | 全て在る |
| P668 | G1-1.2・G2-Ⅰ・C1-直り・C2-直り | 是認 | 是認（変えない） | 全て在る |
| P669 | G1-3・G2-Ⅳ-3・C1-3・C2-3 | 是認 | 是認（除いた二つの出所は §15 に書いた）・草案3 §15・草案3 の字句「二巡目の採否表 P669」 | 全て在る |
| P670 | G1-4・G2-Ⅳ-4・C1-4・C2-4 | 是認 | 是認（足りない印字は P681・P688・P689・P692 で受けた） | 全て在る |
| P671 | G1-2-1・G2-Ⅱ-1・C1-N2・C2-N1 | 登録者の裁定（D219） | 正本 `decisions.D219`・正本 `independent_recompute.what`・正本 `independent_recompute.new_paths`・正本 `independent_recompute.stages.first`・正本 `independent_recompute.stages.second`・正本 `independent_recompute.tol_stage1`・正本 `independent_recompute.agreement`・正本 `independent_recompute.print`・正本 `independent_recompute.on_mismatch`・草案3 §12・設計事実 `E.passes_recompute`・設計事実 `E.tokens_recompute`・草案3 の字句「札の一致」 | 全て在る |
| P672 | G1-2-3・G2-Ⅱ-1 | 登録者の裁定（D219） | 正本 `pilot.cache_tol_rule`・正本 `pilot.cache_tol_factor`・正本 `pilot.cache_tol_floor`・正本 `pilot.noise_max`・正本 `pilot.cache_tol_floor` の値（0.005）が G2 の票にある・草案3 §4・草案3 の字句「上限 `pilot.noise_max` で頭打ちにした値」 | 全て在る |
| P673 | G1-2-2・C1-N4 | 登録者の裁定（D221） | 正本 `decisions.D221`・正本 `pilot.order`・正本 `pilot.checks.vi.path`・正本 `pilot.checks.vi.a`・正本 `pilot.checks.vi.b`・正本 `pilot.checks.vi.floor_rule`・正本 `pilot.checks.vi.measures`・正本 `pilot.repeat_n`・正本 `pilot.decision.rule`・正本 `pilot.decision.q1_map`・正本 `reading_rules`・正本 `limits`・草案3 §4・草案3 §9・草案3 §10・設計事実 `E.passes_noise_a`・設計事実 `E.passes_noise_b`・草案3 の字句「数値が定まらず測れなかった」 | 全て在る |
| P674 | C1-N3 | 採用（凍結の前・草案3） | 正本 `readout.primary.batching`・設計事実 `E.batch_fill_main`・草案3 §3・草案3 §6・草案3 の字句「最後のバッチを零のベクトルで埋めて同じ形にし」 | 全て在る |
| P675 | C1-N5 | 採用（凍結の前・草案3） | 正本 `computation.steered_cache_check.rule`・設計事実 `E.passes_cache`・草案3 §12・草案3 の字句「二つの道の効き目の差の絶対値の最大」 | 全て在る |
| P676 | C1-N9・C2-N8 | 採用（凍結の前・草案3） | 正本 `nulls.storage.rule`・正本 `computation.self_checks.logit`・正本 `computation.self_checks.layer`・正本 `computation.self_checks.on_fail`・正本 `computation.logit_tol`・正本 `computation.layer_tol`・正本 `descriptive.layerwise.capture`・設計事実 `D.npz_directions`・草案3 §2・草案3 §8・草案3 §12・草案3 の字句「二重の正規化を捕まえる」 | 全て在る |
| P677 | C1-N1・C2-N2 | 登録者の裁定（D222） | 正本 `decisions.D222`・正本 `pilot.decision.tool_error.what`・正本 `pilot.decision.tool_error.on_error`・正本 `pilot.decision.tool_error.on_suspicion`・正本 `pilot.decision.tool_error.decide`・正本 `pilot.decision.tool_error.rerun`・正本 `computation.main_freeze_check`・正本 `report_rules.template`・草案3 §4・草案3 §12・草案3 の字句「逸脱の台帳に記した器の差分だけ」 | 全て在る |
| P678 | C1-N10・C2-N6 | 採用（凍結の前・草案3） | 正本 `pilot.checks.iii`・正本 `pilot.iii_sentences.positive`・正本 `pilot.iii_sentences.not_positive`・正本 `pilot.iii_sentences.undefined`・草案3 §4・草案3 の字句「同じ値は平均の順位」・草案3 の字句「読み取りの値を段階 B の行動の率の代わりに読まない」 | 全て在る |
| P679 | C1-N12 | 採用（凍結の前・草案3） | 正本 `gate.dropped`・草案3 §7・草案3 の字句「残った単位の数の階乗」 | 全て在る |
| P680 | G1-5-1 | 登録者の裁定（D223） | 正本 `decisions.D223`・正本 `report_rules.template`・正本 `limits`・草案3 §10・草案3 §12・草案3 の字句「床の近くの升目」 | 全て在る |
| P681 | G1-2-4・G2-Ⅲ-1・C1-N11・C2-N3 | 登録者の裁定（D220） | 正本 `decisions.D220`・正本 `readout.variants.V3`・正本 `readout.variants.rule`・正本 `readout.primary.copy_cue`・正本 `pilot.checks.iv`・正本 `reading_rules`・正本 `print_strings.reading_never_ban`・正本 `limits`・設計事実 `A.v3_head_same`・設計事実 `A.outputs_with_v3_key`・草案3 §3・草案3 §4・草案3 §9・草案3 §10・草案3 の字句「揺れの版の値」・草案3 の字句「割り方の各片」 | 全て在る |
| P682 | G2-Ⅱ-3・C1-R2 | 採用（凍結の前・草案3） | 正本 `labels.second.ranks`・正本 `limits`・草案3 §5・草案3 §10・草案3 の字句「行に不利な側」 | 全て在る |
| P683 | C2-N4 | 採用（凍結の前・草案3） | 正本 `labels.second.iso_top_share`・草案3 §5・草案3 の字句「行の偶然の目安ではない」 | 全て在る |
| P684 | C1-N6 | 採用（凍結の前・草案3） | 正本 `labels.side_rule`・草案3 §5・草案3 §9・草案3 の字句「下の四分位と上の四分位の間」 | 全て在る |
| P685 | C1-N7 | 採用（凍結の前・草案3） | 正本 `gate.descriptive_rule`・草案3 §7・草案3 §9・草案3 の字句「記述の門には型を当てない」 | 全て在る |
| P686 | C1-R3 | 採用（凍結の前・草案3） | 正本 `labels.print_rule`・草案3 §5・草案3 の字句「中心からどちらの側に離れたかを言わないので」 | 全て在る |
| P687 | G2-Ⅱ-2・C1-N8・C2-N7 | 採用（凍結の前・草案3） | 正本 `predictions.q7_rule`・設計事実 `C.q7_intervals`・草案3 §6・草案3 §11・草案3 の字句「数えられる行が残らなければ採点しない」・草案3 の字句「区間が零を含み q7 で該当なしになる行」 | 全て在る |
| P688 | C1-R1・C2-N5 | 採用（凍結の前・草案3） | 正本 `gate.style_note`・正本 `gate.style_hold_pt`・設計事実 `C.style_share_pt`・草案3 §6・草案3 §7・草案3 の字句「閾値の値だけを借り」・草案3 の字句「門の行すべての JSON 直答の割合の差」 | 全て在る |
| P689 | C1-R4・C2-N9 | 採用（凍結の前・草案3） | 設計事実 `D.seeds_taken_n`・設計事実 `E.batch`・草案3 §6・草案3 の字句「のどれとも重ならない」・草案3 の字句「同じ値であることを器が確かめた」 | 全て在る |
| P690 | C1-R5・C2-N10 | 採用（凍結の前・草案3） | 草案3 §15・草案3 の字句「器で見る前は、知る前ではなかった」・草案3 の字句「二巡目の事実の確かめ K476」 | 全て在る |
| P691 | C2-N11 | 採用（記録に置く） | 正本 `decisions.D218`・正本 `numbering.rulings_next`・露出の記録の字句「## 扱いの決定（登録者裁定 D217）」・C2-R18 の言い直しは採否表の行に置いた（第一巡の採否表は書き換えない） | 全て在る |
| P692 | C2-Q4・C1-4 | 採用（凍結の前・草案3） | 正本 `cost.note`・正本 `cost.colab_units_high`・設計事実 `E.tokens_recompute`・設計事実 `E.passes_secondary_noop`・草案3 §14・草案3 の字句「二段にした独立の再計算」 | 全て在る |
| P693 | C2-7 | 採用（凍結の前・草案3） | 正本 `limits`・草案3 §10・草案3 の字句「段階 B で生成したトークンの並びと違うことがある」 | 全て在る |
| P694 | G2-Ⅲ-2・C1-5・C2-5 | 採用（器の段） | 正本 `review_plan.synthetic`・正本 `review_plan.impl.focus`・草案3 §12・草案3 の字句「bf16 相当の揺れを入れた合成の模型」・草案3 の字句「合成データの確かめを検分者が実際に走らせ」 | 全て在る |
| P695 | C1-R6 | 採用（凍結の前・草案3） | 正本 `decisions.D218`・正本 `decisions.D219`・正本 `decisions.D220`・正本 `decisions.D221`・正本 `decisions.D222`・正本 `decisions.D223`・正本 `numbering.rulings_next`・正本 `inputs.files.rulings_D218`・正本 `inputs.files.rulings_D219_D223`・正本 `inputs.files.design_r2_adoption`・正本 `inputs.files.design_r2_verification`・正本 `drafter_values`・草案3 §16 | 全て在る |
| P696 | G2-Ⅱ-1 | 記録に置く（事実の言い直し） | 記録に置く（事実の言い直しは採否表の行・草案は変えない） | 全て在る |
| P697 | G1-7.2 | 是認（既にある決まり） | 是認（既にある決まり）・正本 `predictions.free` | 全て在る |
| P698 | C1-末・G1-確認していないこと・G2-確認していないこと・C2-末 | 記録に置く | 露出の記録の字句「## 設計の巡・二巡目の票（最終検分）」・草案3 §15・草案3 の字句「露出の記録の二巡目の段」 | 全て在る |

- 限界: この記録は、受けた所が在ることを確かめる。受け方が所見を取り違えていないか、半分しか直していないかは確かめない。二巡目は最終検分なので、この後に設計の巡は無く（裁定 D218）、受け方の当否は登録者の確認と器の実装の検分で見る。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
