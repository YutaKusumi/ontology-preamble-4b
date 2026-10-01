# B′ の器の合成データの確かめ（機械生成・`dry_bprime.py` v1・小さな乱数の Gemma 4・手元の CPU）

- 版: transformers 5.16.1・torch 2.9.1+cpu・numpy 2.4.6・正本の SHA16 56BF6D39B25BB0CE・設定の SHA16 E967DD38BC5CFD38（小さな模型は大きさだけ縮め、層 6・窓 8）。器の版: dry_bprime v1・bprime_run v1.1・bprime_directions v1・bprime_behavior v1・bprime_gemma v0.1・bprime_core v0.1。
- 標本化の鍵（正本の段階 B の値の写し）: do_sample True・temperature 0.7・top_p 0.9・top_k 20・min_p 0.0・repetition_penalty 1.0・no_repeat_ngram_size 0・max_new_tokens 4096。

| 確かめ | 通ったか | 値 |
|---|---|---|
| L1_measure_k_bf16 | 通った | k 3.945・z0 4・k_by_batch {"16": 3.94451904296875, "1": 3.94451904296875}・big_rows 2088・n_rows 2208・positions 32・sec 274.2 |
| L2_correct_passes | 通った | states {"N1\|O-Ncold": "合", "S1\|Onull": "合"}・off {"N1\|O-Ncold": "pass", "S1\|Onull": "pass"}・dbl {"N1\|O-Ncold": "pass", "S1\|Onull": "pass"}・sec 1.9 |
| L3_bugs_caught | 通った | states {"double_norm": {"N1\|O-Ncold": "否", "S1\|Onull": "否"}, "no_softcap": {"N1\|O-Ncold": "否", "S1\|Onull": "否"}}・sec 5 |
| L4_norm_weight_confusions_caught | 通った | states {"one_plus_weight": {"N1\|O-Ncold": "否", "S1\|Onull": "否"}, "weight_missing": {"N1\|O-Ncold": "否", "S1\|Onull": "否"}}・norm_weight_min 2・norm_weight_max 3・sec 5.2 |
| L_hooks_clean | 通った | ours 0・pre 0・pre_base 0・foreign [1, 1, 1, 1, 1, 1]・foreign_base [1, 1, 1, 1, 1, 1]・wrapped [] |
| L5_small_values_no_discrimination | 通った | k 0.09077・z0 1・fallback true・big_rows 0・states {"N1\|O-Ncold": "見分ける力無し", "N1\|Onull": "見分ける力無し", "S1\|O-Ncold": "見分ける力無し"}・n_no_discrimination 3・off {"N1\|O-Ncold": "none", "N1\|Onull": "none", "S1\|O-Ncold": "none"}・dbl {"N1\|O-Ncold": "pass", "N1\|Onull": "pass", "S1\|O-Ncold": "pass"}・sec 301.4 |
| L5_hooks_clean | 通った | ours 0・pre 0・pre_base 0・foreign [1, 1, 1, 1, 1, 1]・foreign_base [1, 1, 1, 1, 1, 1]・wrapped [] |
| S1_alignment | 通った | selected_layer_equal true・last_layer_close false・selected_layer 2・layer_types "ssFssF"・window 8・seq_len 43・sec 0.8 |
| S2_layer_check_and_next_layer | 通った | layer_check_diff 0・layer_tol 0.0001・effect 1.304・effect_next_layer 0.8883・sec 1 |
| S3_batch_invariance | 通った | max_abs 1.303e-07・sec 2 |
| S4_sign | 通った | diff 0・sec 0.4 |
| S5_extraction_stops_and_matches | 通った | max_abs_vs_hidden_states 0・contexts 16・sec 14.7 |
| S6_directions_build_and_load | 通った | iso_rel_max 1.304e-16・check_cos_max 0.2804・npz_same_bytes true・n_dirs 58・sha_mismatch_stops "ToolError: 方向の npz の SHA-256 が記録と違う"・sec 0.1 |
| P0_chain_for_readout | 通った | chain ["TemperatureLogitsWarper", "TopKLogitsWarper", "TopPLogitsWarper", "MinPLogitsWarper"]・sec 0.2 |
| P1_pilot_full_path | 通った | q1 "続ける"・batch 16・floor 7.437e-07・vi {"stop": false, "batch": 16, "floor": 7.437202523830067e-07, "spread_a": 7.437202523830067e-07, "spread_b": 0.0}・iii {"rho": 0.047619047619047616, "n": 8, "dropped_n": 0, "sentence_key": "positive"}・logit_states {"N1\|O-Ncold": "合", "N1\|Onull": "合", "S1\|O-Ncold": "合", "S1\|Onull": "合", "S4\|O-Ncold": "合", "S4\|Onull": "合", "SK\|O-Ncold": "合", "SK\|Onull": "合"}・variant_lens {"V1": 4, "V2": 10, "V3": 6}・n_forward 79・sec 92 |
| P2_pilot_contract_thresholds | 通った | q1 "止める"・n_pass 0・dropped_n 8・iii {"rho": NaN, "n": 0, "dropped_n": 8, "sentence_key": "undefined"}・sec 68 |
| P3_pilot_behavior_not_ok | 通った | iii_tool_error {"fail": "tool_error", "sentence_key": null, "n": 8, "dropped_n": 0}・iii_unscorable {"fail": "unscorable", "sentence_key": null, "n": 8, "dropped_n": 0}・sec 156.2 |
| P4_pilot_behavior_guards | 通った | bad_status "ToolError: 行動の下見の状態が決まりの外: 'closed?'"・missing_rate "ToolError: 行動の下見の率が欠けた升目がある（閉じた記録と升目の鍵を照らす）"・sec 64.5 |
| M1_cell_sign_sets | 通った | main 12・reverse 4・overlap []・sec 0 |
| M2_main_phase | 通った | n_combos 16・effects_per_combo [28, 35]・head_states {"N1\|O-Ncold": "合", "N1\|Onull": "合", "S1\|O-Ncold": "合", "S1\|Onull": "合", "S4\|O-Ncold": "合", "S4\|Onull": "合", "SK\|O-Ncold": "合", "SK\|Onull": "合"}・layer_check_diff 0・sec 73.1 |
| M3_batch1_and_path_difference | 通った | max_abs_batch1_vs_batch16 1.353e-06・max_abs_override_vs_main16 0・sec 313.4 |
| M4_recompute_hook_path | 通った | max_abs 3.004e-07・n 4・sec 1.8 |
| SPM_hooks_clean | 通った | ours 0・pre 0・pre_base 0・foreign [1, 1, 1, 1, 1, 1]・foreign_base [1, 1, 1, 1, 1, 1]・wrapped [] |
| G1_resolved_config_and_chain | 通った | chain [["TemperatureLogitsWarper", {"temperature": 0.7}], ["TopKLogitsWarper", {"min_tokens_to_keep": 1, "top_k": 20}], ["TopPLogitsWarper", {"min_tokens_to_keep": 1, "top_p": 0.9}], ["MinPLogitsWarper", {"min_p": 0.0, "min_tokens_to_keep": 1}]]・eos_tokens ["<eos>", "<turn\|>", "<\|tool_response>"]・values {"do_sample": true, "temperature": 0.7, "top_p": 0.9, "top_k": 20, "min_p": 0.0, "repetition_penalty": 1.0, "no_repeat_ngram_size": 0, "max_new_tokens": 4096}・stopping ["MaxLengthCriteria", "EosTokenCriteria"]・sec 0.1 |
| G2_chain_equals_generate | 通った | processed_equal_call true・processed_equal_abort_chain true・chain_desc_equal true・max_abs_readout_vs_model_logits 0・sec 2 |
| G3_transformed_vs_sampling_frequency | 通った | N 4000・kept 8・a_rank 3・p_a_transformed 0.1152・freq_a 0.1105・max_abs_z 1.701・tv 0.01333・stray {}・mass_outside_designed 0・cum_at_cut [0.8923963606169772, 0.9225416814545624]・sec 1355 |
| G4_foreign_stop_tokens_stop | 通った | cases {"without_turn_end": {"eos": [1, 50], "error": "ToolError: 止める印が正本（Gemma の generation_config.json の値）と違う: [1, 50]（正本 [1, 106, 50]）"}, "stageB_model_config": {"eos": [151645], "error": "ToolError: 止める印が正本（Gemma の generation_config.json の値）と違う: [151645]（正本 [1, 106, 50]）"}}・stageB_snapshot "cdbee75f17c01a7cc42f958dc650907174af0554"・restored true・sec 0.3 |
| G5_forgotten_top_k_stops | 通った | resolved_top_k 64・error "ToolError: generate に実際に渡った標本化の値が正本と違う: top_k=64（正本 20）"・sec 0.1 |
| G6_wrappers_removed_and_row_c_match | 通った | exception_inside "ValueError: The following `model_kwargs` are not used by the model: ['not_a_generation_key'] (note: typos in the generate arguments will also show up in this list)"・left_after_exception []・row_c_equal_ok true・row_c_mismatch_stops "ToolError: (iii) の処理の並びの要約が転記行 C の要約と違う"・left_after_all []・sec 0.3 |
| G_hooks_clean | 通った | ours 0・pre 0・pre_base 0・foreign [1, 1, 1, 1, 1, 1]・foreign_base [1, 1, 1, 1, 1, 1]・wrapped [] |

- すべて通ったか: はい（30 項目・2928 秒）

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
