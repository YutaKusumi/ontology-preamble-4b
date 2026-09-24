# B-lens 層三の草案2 の対応の記録（機械で確かめた・`records/Bl3/draft2_mapping_Bl3.py`）

- 採否表: `records/reviews/Bl3/design-round1/adoption-table-Bl3-design-r1.md`（SHA16 799D1B303F90BA96）の行 P620〜P666。採否・票・所見・案は採否表から器が読んだ。
- 受けた所: 正本 `design/contrasts-Bl3.json`（SHA16 F33D2232A7CF84B7・版 draft2-2026-09-24）・草案2 `design/design-Bl3-draft2.md`（SHA16 E6C947F5D8AA5150）・設計事実 `records/Bl3/design-facts-Bl3.json`（SHA16 A62A5A3E9A0A0CA4）。受けた所は起草者が並べ、器がその実在を確かめた（中身の当否は確かめていない）。
- 見つからなかったもの: 0 件。

| 採否 | 票・所見 | 案 | 草案2 で受けた所 | 実在 |
|---|---|---|---|---|
| P620 | C2-R1 | 採用＋登録者の裁定（D212） | 正本 `readout.primary.copy_cue`・正本 `readout.variants.V3`・正本 `scope.not_answered`・正本 `limits`・草案2 §3・草案2 §4・草案2 §10・設計事実 `B.cells`・草案2 の字句「雛形との重なり」 | 全て在る |
| P621 | G1-1-1・G2-Q1・C1-M1・C2-R4 | 採用（草案2） | 正本 `scope.full_path`・正本 `scope.not_answered`・正本 `limits`・正本 `report_rules.template`・草案2 §0・草案2 §1・草案2 §10・草案2 §12 | 全て在る |
| P622 | G1-2-1 | 登録者の裁定（D212） | 正本 `readout.primary.band_why`・草案2 §3 | 全て在る |
| P623 | G2-3 | 採用（草案2） | 正本 `readout.primary.quantity`・正本 `readout.primary.a_vs_catastrophe`・正本 `scope.question`・草案2 §0・草案2 §3 | 全て在る |
| P624 | G2-Q2 | 採用（事実を足す） | 設計事実 `A.refuse_next`・草案2 §6・草案2 の字句「refuse を選んだ出力」 | 全て在る |
| P625 | C1-S1・C2-R3 | 採用（草案2） | 正本 `readout.primary.precision`・正本 `readout.primary.place`・正本 `readout.primary.batching`・正本 `readout.primary.batch`・正本 `readout.primary.order_seed`・正本 `pilot.checks.vi`・草案2 §3・草案2 §4 | 全て在る |
| P626 | G1-2-2・C1-L2 | 採用（記述） | 正本 `descriptive.mass`・草案2 §8 | 全て在る |
| P627 | G1-2-3・C1-L5・C2-R14 | 一部採用＋登録者の裁定（D216） | 正本 `gate.attenuation`・正本 `gate.descriptive_gates`・草案2 §7・草案2 §10 | 全て在る |
| P628 | G1-3-1・G2-6・G1-11・C1-M4・C2-R9・G2-Q3 | 登録者の裁定（D214） | 正本 `pilot.mass_min`・正本 `pilot.p_bounds`・正本 `pilot.cache_tol_rule`・正本 `pilot.iii_sentences`・草案2 §4・草案2 §15 | 全て在る |
| P629 | G1-3-2・G2-1・G2-4・C1-M4・C2-R8・G2-Q10 | 採用（草案2）＋族の扱いは登録者の裁定（D214） | 正本 `pilot.decision.gate_only`・正本 `pilot.decision.drop_effects`・正本 `pilot.decision.family`・正本 `pilot.decision.q1_map`・正本 `pilot.decision.tool_error`・正本 `pilot.decision.report`・正本 `gate.dropped`・草案2 §4・草案2 §7・草案2 §9・草案2 の字句「下見で一部を外した」 | 全て在る |
| P630 | G1-9-1・C1-M5・C2-R8 | 一部採用（草案2） | 正本 `computation.steered_cache_check`・正本 `computation.before_seal`・草案2 §12 | 全て在る |
| P631 | C1-M5・C2-R8 | 採用（草案2） | 正本 `computation.main_freeze_check`・正本 `predictions.free`・草案2 §11・草案2 §12 | 全て在る |
| P632 | G1-4-1・G2-2・C1-L1・C2-R6 | 登録者の裁定（D211） | 正本 `nulls.isotropic.count`・正本 `labels.p_min`・正本 `labels.first_step_margin`・草案2 §5・設計事実 `E.passes_main` | 全て在る |
| P633 | G1-11・G2-7・C1-11・C2-11 | 登録者の裁定（D211） | 正本 `nulls.storage.dtype`・正本 `nulls.storage.rule`・草案2 §2 | 全て在る |
| P634 | C1-M2・C2-R5 | 採用（草案2） | 正本 `nulls.real.chance_second_pair`・正本 `nulls.real.chance_note`・正本 `labels.second.ranks`・正本 `labels.second.iso_rate`・草案2 §5・草案2 §15 | 全て在る |
| P635 | G1-4-2・C2-R7 | 登録者の裁定（D213） | 正本 `labels.second.rule`・正本 `labels.second.center_why`・草案2 §5 | 全て在る |
| P636 | G1-5-1・G2-5・C1-L6・C2-Q5 | 登録者の裁定（D213） | 正本 `gate.push_center`・草案2 §7 | 全て在る |
| P637 | C1-S2・C2-R2 | 採用（草案2・器） | 正本 `gate.push`・正本 `gate.call`・正本 `labels.second.call`・正本 `review_plan.synthetic`・草案2 §5・草案2 §7・草案2 §12 | 全て在る |
| P638 | C2-R13 | 採用（草案2・記述） | 正本 `gate.descriptive_gates`・正本 `gate.rows_without_vhat_loaded`・正本 `gate.permutations_without_vhat_loaded`・設計事実 `C.rows_without_vhat_loaded`・草案2 §7 | 全て在る |
| P639 | C2-R16 | 採用（草案2・器） | 設計事実 `D.cos_iso_b3_max`・草案2 §6・草案2 の字句「等方の方向と段階 B の三本の余弦」 | 全て在る |
| P640 | C1-M8 | 登録者の裁定（D215） | 正本 `scope.not_answered`・正本 `limits`・草案2 §0・草案2 §10・草案2 の字句「活性の共分散に沿う帰無」 | 全て在る |
| P641 | G1-5-2 | 不採用（門は条件として置く） | 不採用（門は条件として置く）。検出力の文は `gate.power_note` のまま・正本 `gate.power_note` | 全て在る |
| P642 | C1-M1・C1-L5・C2-R14・C2-R4・G2-5 | 登録者の裁定（D216） | 正本 `gate.descriptive_gates`・正本 `gate.style_hold_pt`・設計事実 `C.style_rows`・草案2 §7 | 全て在る |
| P643 | C1-M7・C2-R11・G1-6-1 | 採用（草案2・器） | 正本 `descriptive.layerwise.values`・正本 `descriptive.layerwise.capture`・正本 `descriptive.layerwise.note_no_reading`・正本 `descriptive.layerwise.place`・正本 `print_strings.added_ban`・草案2 §8・草案2 §9 | 全て在る |
| P644 | C2-R12 | 採用（草案2） | 正本 `readout.secondary.band`・草案2 §3 | 全て在る |
| P645 | C1-M3・C2-R10 | 採用（草案2） | 正本 `reading_rules`・草案2 §9・草案2 の字句「最上位は順位で、検定ではない」 | 全て在る |
| P646 | C2-R10 | 採用（草案2） | 正本 `labels.side_rule`・草案2 §5・草案2 §9・草案2 の字句「零を越えて中央値と反対の向き」 | 全て在る |
| P647 | C2-R10・G2-4 | 採用（草案2） | 正本 `reading_rules`・草案2 §9・草案2 の字句「外でない行」・草案2 の字句「下見で一部を外した」 | 全て在る |
| P648 | G1-7-1 | 採用（草案2） | 正本 `reading_rules`・草案2 §9・草案2 の字句「方向に固有の効き目は言えない」 | 全て在る |
| P649 | G1-8-1・C1-L3・C2-R10・G2-Q8 | 採用（草案2） | 正本 `predictions.items`・正本 `predictions.q7_rule`・草案2 §11 | 全て在る |
| P650 | C1-L4・C2-Q9 | 採用（草案2） | 正本 `report_rules.template`・草案2 §12 | 全て在る |
| P651 | C1-M6 | 採用（草案2） | 正本 `independent_recompute.who`・正本 `independent_recompute.how`・正本 `independent_recompute.tol`・正本 `independent_recompute.on_mismatch`・草案2 §12 | 全て在る |
| P652 | G1-10-1 | 採用（器の段） | 正本 `review_plan.synthetic`・草案2 §12・草案2 の字句「向きの足し分に要る全ての升目・符号・方向の組の突き合わせ」 | 全て在る |
| P653 | C1-9・C2-Q10・G2-Q10 | 採用（器の段） | 正本 `review_plan.synthetic`・正本 `review_plan.impl.focus`・草案2 §12 | 全て在る |
| P654 | C2-R17 | 採用（草案2） | 正本 `cost.note`・設計事実 `E.passes_recompute`・設計事実 `E.passes_cache`・草案2 §14 | 全て在る |
| P655 | C2-R18 | 不採用（記録に無い） | 不採用（段階 B の生の出力の記録にトークンの並びの欄が無い） | 全て在る |
| P656 | C2-R19 | 採用（草案2） | 正本 `scope.reach`・草案2 §1 | 全て在る |
| P657 | C1-L7・C2-R15 | 採用（草案2） | 正本 `numbering.rulings_next`・正本 `decisions.D210`・正本 `decisions.D217`・正本 `inputs.files.rulings_D210`・正本 `inputs.files.rulings_D211_D217`・正本 `drafter_values`・草案2 §16 | 全て在る |
| P658 | C1-M4・C2-R9 | 採用（草案2） | 草案2 §15・草案2 の字句「会話の記録の時刻で確かめた」 | 全て在る |
| P659 | G2-Q3・C1-3・C2-3 | 是認 | 是認（変えない） | 全て在る |
| P660 | G1-11・G2-Q11・C1-11・C2-11 | 是認＋採用（今の正本に書く） | 正本 `pilot.decision.after_stop`・草案2 §4 | 全て在る |
| P661 | G1-11・G2-Q11・C1-11・C2-11 | 是認 | 是認（変えない） | 全て在る |
| P662 | G1-11・G2-Q6・C1-6・C2-6 | 是認 | 是認（絞り方は P643 で受けた） | 全て在る |
| P663 | C1-11・C2-11 | 是認 | 是認（変えない） | 全て在る |
| P664 | G2-Q4・C1-4・C2-4 | 是認 | 是認（偶然の目安の直しは P634 で受けた） | 全て在る |
| P665 | G2-Q7・G2-Q9・C1-2 | 是認 | 是認（変えない） | 全て在る |
| P666 | G1-1-1・G1-5-2・G2-Q2 | 露出（登録者の裁定 D217） | 正本 `predictions.free`・草案2 §11・草案2 §15・草案2 の字句「exposure-before-seal-Bl3.md」 | 全て在る |

- 限界: この記録は、受けた所が在ることを確かめる。受け方が所見を取り違えていないか、半分しか直していないかは確かめない（設計の巡・二巡目で諮る）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
