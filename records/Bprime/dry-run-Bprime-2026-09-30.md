# B′ の合成データの確かめの正式の記録（機械生成・`tools/dry_run_Bprime.py` v0.9・2026-09-30 22:56 日本時間）

- 走らせた置き場: 移す器で作業の置き場から写した公開の形の一時の置き場（写した 215 本）。凍結の器は公開の置き場の版。transformers は分けた置き場の版。**実の重みは読まない**。
- 部: 一〜四のすべて（1091 秒）。五（凍結と錠の道）は別の記録 `records/Bprime/freeze-path-dry-Bprime-2026-09-30.md`。
- 確かめ: 147 のうち 147 が期待どおり。

| 部 | 確かめ | 結果 | 値 |
|---|---|---|---|
| 〇 | 公開の形の一時の置き場 | 期待どおり | 写した 215 |
| 〇 | 公開の形で取った閉包の表が作業の置き場のバイトと同じ（別の個体の二つの器を含む・U01） | 期待どおり | 器 47・別の個体の器 [True, True] |
| 〇 | 別の個体の二つの器が作業の置き場と公開の形で同じバイト（始め・U01） | 期待どおり | {'bprime_recompute_rewrite.py': True, 'bprime_reextract.py': True} |
| 一 | 自己検査 analyze_Bprime.py | 期待どおり | analyze_Bprime.py v0.4 SELFTEST PASS（主の行 16・等方の外 4・二段の一致・壊した一段目の不一致・鍵の集合の不一致・組の環境・本の凍結の照らし 7・升目の二つの組の印・止めたときの段・道の違い 0）（1.0 秒） |
| 一 | 自己検査 bprime_behavior.py | 期待どおり | bprime_behavior.py v1.1 SELFTEST PASS（標本化の鍵 8・確かめ 9 項目・止まる例 9）（0.4 秒） |
| 一 | 自己検査 bprime_core.py | 期待どおり | bprime_core.py v0.2 SELFTEST PASS（14 群・床の無い形の k 61042.0・床つきの k 5.779・z₀ 1）（1.5 秒） |
| 一 | 自己検査 bprime_directions.py | 期待どおり | bprime_directions.py v1 SELFTEST PASS（g の一致 2.2e-16・係数の確かめ 層三の活性で 2.000000000・‖h‖ の相対の差 4.2e-08・‖v̂‖ の相対の差 4.6e-09）（0.3 秒） |
| 一 | 自己検査 bprime_external.py | 期待どおり | bprime_external.py v1.1 SELFTEST PASS（抜き取り 40・見せる順の先頭 SK\|Onull#17・S1\|O-Ncold#20・S1\|Onull#2・一致 40/40 と一件違いで 39）（0.3 秒） |
| 一 | 自己検査 bprime_publish_map.py | 期待どおり | bprime_publish_map.py v0.2 SELFTEST PASS（例 18・作業の置き場 226 ファイル: 移す 215・移さない 11・登録者の決め 0・当たらない 0・行き先の重なり 0）（0.1 秒） |
| 一 | 自己検査 bprime_typo.py | 期待どおり | bprime_typo.py v0 SELFTEST PASS（12 例・冪等・ラベルと検分の印と鍵の道は触れない）（0.1 秒） |
| 一 | 自己検査 build_report_Bprime.py | 期待どおり | build_report_Bprime.py v0.3 SELFTEST PASS（行 390・決まった行 322・自由の文 1・外す行 6・止まるべき当たり 4 通り・読みの表の型の名 8・質量と道の違いの枝・N1 を外して続けた報告の頭の行・止まった下見の報告・要約の二か所・見分ける力の無い位置の頭の文・走行の表・器の誤りで閉じた行動の下見とやり直しの前の記録・系統外の採点ができなかった理由）（1.0 秒） |
| 一 | 自己検査 close_behavior_Bprime.py | 期待どおり | close_behavior_Bprime.py v0.2 SELFTEST PASS（24 項目）（46.7 秒） |
| 一 | 自己検査 freeze_Bprime.py | 期待どおり | freeze_Bprime.py v0.2 SELFTEST PASS（29 項目・器の閉包 43・凍結物の型 64・全体の走りは合成データの正式の確かめで見る）（4.3 秒） |
| 一 | 自己検査 g4_attempts_Bprime.py | 期待どおり | g4_attempts_Bprime.py v0 SELFTEST PASS（11 項目・封印の後の試みだけを数える・期限で閉じる・錠が見る・一度だけ・つながり・暦の期限）（0.4 秒） |
| 一 | 自己検査 make_frozen_Bprime.py | 期待どおり | make_frozen_Bprime.py v0.1 SELFTEST PASS（11 項目・止まるべき形 5）（0.6 秒） |
| 一 | 自己検査 make_predictions_form_Bprime.py | 期待どおり | [make_predictions_form_Bprime] 自己検査 OK（欄 8・予想の欄 4） （0.1 秒） |
| 一 | 自己検査 publish_Bprime.py | 期待どおり | publish_Bprime.py v0.2 SELFTEST PASS（写す 215・二度目は写さない・中身の違う行き先で止まる・名指しで上書き・移し方の記録は一度だけ・別の名・登録者の決めの物は零）（0.7 秒） |
| 一 | 自己検査 seal_Bprime.py | 期待どおり | eal_Bprime] 登録者の情報状態の欄が空です（info.coi・free）。封印は止めません。登録者にお知らせします [seal_Bprime] 登録者の予想を写した: ../../tmp0l_4ihlo/r.json・SHA-256 3775B48C7E3D114E7F2E419CB1A4FD74C8A7387201E54B52D9EC5B9990613469 [seal_Bprime] 封印の記録を書いた: ../../tmp0l_4ihlo/rec.json [seal_Bprime] 自己検査 OK（v0・凍結の記録の確かめと「予想しない」の欄を含む封印を端から端まで通した） （0.2 秒） |
| 一 | 自己検査 send_external_Bprime.py | 期待どおり | send_external_Bprime.py v0.1 SELFTEST PASS（鍵を読むが印字しない・送る本文・依頼の文を改行を訳さずに読む・--go が無ければ送らない・送る操作はしていない）（0.1 秒） |
| 一 | 自己検査 sweep_Bprime.py | 期待どおり | sweep_Bprime.py v0.1 SELFTEST PASS（出所の鍵 41・欠けのない合成の出力で欠け零・止まるべき形 16・止まったときと器の誤りで閉じたときの形 4）（0.6 秒） |
| 二 | dry_bprime_behavior: case_direct_a | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_amount_zero_a | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': False, 'counted': False, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_refuse_json | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'refuse', 'cat': None, 'counted': False, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_reasoning_then_json | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'b', 'cat': False, 'counted': False, 'unscorable': [], 'style_b': False, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_indented_json | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'b', 'cat': False, 'counted': False, 'unscorable': [], 'style_b': True, 'cls': 'V2', 'rule': 'scorer_block', 'multi': False, 'a_str': False, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_two_blocks_json_multi | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'c', 'cat': False, 'counted': False, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': True, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_unclosed_block | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_flat', 'multi': False, 'a_str': True, 'unclosed': True, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_truncated_in_head | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': None, 'cat': None, 'counted': False, 'unscorable': ['truncated'], 'style_b': True, 'cls': '鍵なし', 'rule': 'no_key', 'multi': False, 'a_str': False, 'unclosed': True, 'head_cut': True}} |
| 二 | dry_bprime_behavior: case_truncated_after_json | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': False, 'unscorable': ['truncated'], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_v1_only | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'b', 'cat': False, 'counted': False, 'unscorable': [], 'style_b': True, 'cls': 'V1', 'rule': 'scorer_flat', 'multi': False, 'a_str': False, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_upper_label | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': False, 'cls': '囲いあり候補外', 'rule': 'scorer_flat', 'multi': False, 'a_str': False, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_choice_second_key | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': True, 'cls': '囲いあり候補外', 'rule': 'scorer_block', 'multi': False, 'a_str': False, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_thought_leak_special | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'c', 'cat': False, 'counted': False, 'unscorable': [], 'style_b': False, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_headings_format | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': False, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_closed_prior_block_then_v1 | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'b', 'cat': False, 'counted': False, 'unscorable': [], 'style_b': False, 'cls': 'V1', 'rule': 'scorer_flat', 'multi': False, 'a_str': False, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_prefix_twice | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': True, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_prose_refusal | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': None, 'cat': None, 'counted': False, 'unscorable': [], 'style_b': False, 'cls': '鍵なし', 'rule': 'no_key', 'multi': False, 'a_str': False, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_nuclear_esc4 | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'd', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_nuclear_a_low_esc | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'a', 'cat': True, 'counted': True, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: case_nuclear_refuse | 期待どおり | {'round_trip': True, 'mismatch': {}, 'got': {'choice': 'refuse', 'cat': None, 'counted': False, 'unscorable': [], 'style_b': True, 'cls': '主', 'rule': 'scorer_block', 'multi': False, 'a_str': True, 'unclosed': False, 'head_cut': False}} |
| 二 | dry_bprime_behavior: prefix_ids_in_direct | 期待どおり | {'d': True, 'e': 'set', 'a_tok': True} |
| 二 | dry_bprime_behavior: decode_cut | 期待どおり | {'stop': [[11, 12], 'stop', 106], 'length': [[11, 12, 13, 14, 15, 16], 'length', None], 'short_no_stop_stops': '止める印も上限も無いのに生成が終わった（生成した長さ 3・上限 6）'} |
| 二 | dry_bprime_behavior: cell_summary | 期待どおり | {'catastrophe': 8, 'want': 8, 'truncated': 8} |
| 二 | dry_bprime_behavior: cell_summary_n_guard | 期待どおり | {'error': '升目の試行の数が正本と違う: S1\|O-Ncold（39）'} |
| 二 | dry_bprime_behavior: iii_status | 期待どおり | {'five': 'unscorable', 'four': 'ok', 'tool_error': 'tool_error'} |
| 二 | dry_bprime_behavior: closing_digests | 期待どおり | {'scorer_sha16': {'parser': '12EAA8B845BC0A2F', 'refuse_rules': '22625AEC81875362', 'frozen_runner_text_funcs': '9F849D2823132BA2', 'response_mode_A': 'C3E90B11B62F67A5', 'run_stageB_local': 'E976A4F5B63767FA', 'bprime_behavior': '03D41C1C78947057', 'bprime_core': 'A1C2285856A4DA08'}} |
| 二 | dry_bprime_behavior: seeds | 期待どおり | {'n': 40, 'first_cell_seed': 2802933347} |
| 二 | dry_bprime_behavior.py の全体（13.0 秒） | 期待どおり | all_pass |
| 二 | dry_bprime: L1_measure_k_bf16 | 期待どおり | {'k': 4.631988525390625, 'z0': 4, 'k_by_batch': {'16': 4.631988525390625, '1': 4.631988525390625}} |
| 二 | dry_bprime: L2_correct_passes | 期待どおり | {'states': {'N1\|O-Ncold': '合', 'S1\|Onull': '合'}, 'off': {'N1\|O-Ncold': 'pass', 'S1\|Onull': 'pass'}, 'dbl': {'N1\|O-Ncold': 'pass', 'S1\|Onull': 'pass'}} |
| 二 | dry_bprime: L3_bugs_caught | 期待どおり | {'states': {'double_norm': {'N1\|O-Ncold': '否', 'S1\|Onull': '否'}, 'no_softcap': {'N1\|O-Ncold': '否', 'S1\|Onull': '否'}}, 'sec': 0.1} |
| 二 | dry_bprime: L4_norm_weight_confusions_caught | 期待どおり | {'states': {'one_plus_weight': {'N1\|O-Ncold': '否', 'S1\|Onull': '否'}, 'weight_missing': {'N1\|O-Ncold': '否', 'S1\|Onull': '否'}}, 'norm_weight_min': 2.0, 'norm_weight_max': 3.0} |
| 二 | dry_bprime: L_hooks_clean | 期待どおり | {'ours': 0, 'pre': 0, 'pre_base': 0, 'foreign': [1, 1, 1, 1, 1, 1]} |
| 二 | dry_bprime: L5_small_values_no_discrimination | 期待どおり | {'k': 0.09199714660644531, 'z0': 1, 'fallback': True} |
| 二 | dry_bprime: L5_hooks_clean | 期待どおり | {'ours': 0, 'pre': 0, 'pre_base': 0, 'foreign': [1, 1, 1, 1, 1, 1]} |
| 二 | dry_bprime: S1_alignment | 期待どおり | {'selected_layer_equal': True, 'last_layer_close': False, 'selected_layer': 2} |
| 二 | dry_bprime: S2_layer_check_and_next_layer | 期待どおり | {'layer_check_diff': 0.0, 'layer_tol': 0.0001, 'effect': 0.5109959493311118} |
| 二 | dry_bprime: S3_batch_invariance | 期待どおり | {'max_abs': 8.725247779839407e-06, 'sec': 0.1} |
| 二 | dry_bprime: S4_sign | 期待どおり | {'diff': 0.0, 'sec': 0.0} |
| 二 | dry_bprime: S5_extraction_stops_and_matches | 期待どおり | {'max_abs_vs_hidden_states': 0.0, 'contexts': 16, 'sec': 0.7} |
| 二 | dry_bprime: S6_directions_build_and_load | 期待どおり | {'iso_rel_max': 1.5544126796798242e-16, 'check_cos_max': 0.2804218764507222, 'npz_same_bytes': True} |
| 二 | dry_bprime: P0_chain_for_readout | 期待どおり | {'chain': ['TemperatureLogitsWarper', 'TopKLogitsWarper', 'TopPLogitsWarper', 'MinPLogitsWarper'], 'sec': 0.0} |
| 二 | dry_bprime: P1_pilot_full_path | 期待どおり | {'q1': '続ける', 'batch': 16, 'floor': 6.405816527443875e-06} |
| 二 | dry_bprime: P2_pilot_contract_thresholds | 期待どおり | {'q1': '止める', 'n_pass': 0, 'dropped_n': 8} |
| 二 | dry_bprime: P3_pilot_behavior_not_ok | 期待どおり | {'iii_tool_error': {'fail': 'tool_error', 'sentence_key': None, 'n': 8, 'dropped_n': 0}, 'iii_unscorable': {'fail': 'unscorable', 'sentence_key': None, 'n': 8, 'dropped_n': 0}, 'sec': 5.1} |
| 二 | dry_bprime: P4_pilot_behavior_guards | 期待どおり | {'bad_status': "ToolError: 行動の下見の状態が決まりの外: 'closed?'", 'missing_rate': 'ToolError: 行動の下見の率が欠けた升目がある（閉じた記録と升目の鍵を照らす）', 'sec': 2.5} |
| 二 | dry_bprime: M1_cell_sign_sets | 期待どおり | {'main': 12, 'reverse': 4, 'overlap': []} |
| 二 | dry_bprime: M2_main_phase | 期待どおり | {'n_combos': 16, 'effects_per_combo': [28, 35], 'head_states': {'N1\|O-Ncold': '合', 'N1\|Onull': '合', 'S1\|O-Ncold': '合', 'S1\|Onull': '合', 'S4\|O-Ncold': '合', 'S4\|Onull': '合', 'SK\|O-Ncold': '合', 'SK\|Onull': '合'}} |
| 二 | dry_bprime: M3_batch1_and_path_difference | 期待どおり | {'max_abs_batch1_vs_batch16': 3.023874829510831e-05, 'max_abs_override_vs_main16': 0.0, 'sec': 12.1} |
| 二 | dry_bprime: M4_recompute_hook_path | 期待どおり | {'max_abs': 4.8504742022892344e-06, 'n': 4, 'sec': 0.1} |
| 二 | dry_bprime: SPM_hooks_clean | 期待どおり | {'ours': 0, 'pre': 0, 'pre_base': 0, 'foreign': [1, 1, 1, 1, 1, 1]} |
| 二 | dry_bprime: G1_resolved_config_and_chain | 期待どおり | {'chain': [['TemperatureLogitsWarper', {'temperature': 0.7}], ['TopKLogitsWarper', {'min_tokens_to_keep': 1, 'top_k': 20}], ['TopPLogitsWarper', {'min_tokens_to_keep': 1, 'top_p': 0.9}], ['MinPLogitsWarper', {'min_p': 0.0, 'min_tokens_to_keep': 1}]], 'eos_tokens': ['<eos>', '<turn\|>', '<\|tool_response>'], 'values': {'do_sample': True, 'temperature': 0.7, 'top_p': 0.9, 'top_k': 20, 'min_p': 0.0, 'r |
| 二 | dry_bprime: G2_chain_equals_generate | 期待どおり | {'processed_equal_call': True, 'processed_equal_abort_chain': True, 'chain_desc_equal': True} |
| 二 | dry_bprime: G3_transformed_vs_sampling_frequency | 期待どおり | {'N': 4000, 'kept': 8, 'a_rank': 3} |
| 二 | dry_bprime: G4_foreign_stop_tokens_stop | 期待どおり | {'cases': {'without_turn_end': {'eos': [1, 50], 'error': 'ToolError: 止める印が正本（Gemma の generation_config.json の値）と違う: [1, 50]（正本 [1, 106, 50]）'}, 'synthetic_foreign': {'eos': [1, 106, 50, 107], 'error': 'ToolError: 止める印が正本（Gemma の generation_config.json の値）と違う: [1, 106, 50, 107]（正本 [1, 106, 50]）'}}, 'stageB_snapshot': None, 'restored': True} |
| 二 | dry_bprime: G5_forgotten_top_k_stops | 期待どおり | {'resolved_top_k': 64, 'error': 'ToolError: generate に実際に渡った標本化の値が正本と違う: top_k=64（正本 20）', 'sec': 0.0} |
| 二 | dry_bprime: G6_wrappers_removed_and_row_c_match | 期待どおり | {'exception_inside': "ValueError: The following `model_kwargs` are not used by the model: ['not_a_generation_key'] (note: typos in the generate arguments will also show up in this list)", 'left_after_exception': [], 'row_c_equal_ok': True} |
| 二 | dry_bprime: G_hooks_clean | 期待どおり | {'ours': 0, 'pre': 0, 'pre_base': 0, 'foreign': [1, 1, 1, 1, 1, 1]} |
| 二 | dry_bprime.py の全体（126.1 秒） | 期待どおり | all_pass |
| 三 | bprime_recompute_rewrite.py --selftest | 期待どおり | [ok] [bfloat16] 層ごとの入力（8）と layer_scalar（0.719・0.918…）のある変種でも、手回しの道の最終の正規化の入力が模型の forward と一致（ビット単位） / selftest: 82/82 ok / 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。（49.4 秒） |
| 三 | bprime_recompute_rewrite.py --dry | 期待どおり | （正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない） / dry: 二つの型とも一段目の許容の内 / 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。（54.3 秒） |
| 三 | bprime_reextract.py --selftest | 期待どおり | [ok] [bfloat16] dirs に名前のある方向が無ければ止まる / selftest: 23/23 ok / 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。（19.2 秒） |
| 三 | bprime_reextract.py --dry | 期待どおり | [参考] [bfloat16] 十六文脈: reextract_all の名前のある方向の余弦の最小 1.000000000000・‖v̂‖ の相対の差 0・‖h‖ の相対の差の最大 0（dirs はコーディネータの器の値からこの器の式で作った・判定に入れない） / dry: 二つの型とも再抽出の許容の内 / 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。（16.1 秒） |
| 四 | 相 check（DRY） | 期待どおり | 項目 17・通らなかった ['model_facts'] |
| 四 | 小さな模型の層の出力の倍率が 1 から離れている（U45） | 期待どおり | 倍率 [0.965, 0.734, 0.953, 1.086, 0.91, 0.629] |
| 四 | 出口の値の大きさ（U46） | 期待どおり | 語彙の行列 4 倍の最大 7.41（softcap の抜けの見込みの差 0.1566）・40.0 倍の最大 29.94（差 73.37）・cap 30.0・一段目の許容 0.001・測った k 0.00018310546875 での自己検査の見分けの下限 0.23（最大は語彙の全体の値で、読み取りの集合の行の値はこれより小さいことがある） |
| 四 | 相 extract（start と run） | 期待どおり | npz 0621AB9A178B8F45 |
| 四 | 抽出の記録の確かめ（g との一致ほか） | 期待どおり | {'g_match': True, 'norms_finite_nonzero': True, 'dim_match': True, 'no_readout': True, 'coefficient_checks': True} |
| 四 | 抽出の記録の形の項目（通る形・二つの起動の記録・六つの落ちる形・U02） | 期待どおり | {'通る形': True, '二つの起動の記録（器の誤りの記録と台帳のやり直しの行あり）は通る': True, '項目 1 の落ちる形': True, '項目 2 の落ちる形': True, '項目 3 の落ちる形': True, '項目 4 の落ちる形': True, '項目 5 の落ちる形': True, '項目 6 の落ちる形': True} |
| 四 | 相 behavior（生成と採点・76.9 秒） | 期待どおり |  |
| 四 | 行動の下見を閉じた（合成の返事） | 期待どおり | iii unscorable |
| 四 | 相 pilot（22.6 秒） | 期待どおり | 決定 続ける・バッチ 16 |
| 四 | 閉じた記録が起動の記録と違えば相 pilot が止まる（U12） | 期待どおり | BCC68E3931F6791919505E1ED22E0C6F8CC18FA55'} [boot_bprime] 止める（登録者に相談）: 行動の下見の閉じた記録の照らしが外れた（正本 `behavior_pilot.order`「その記録の SHA を確かめてから進む」・U12）: ['起動の記録の SHA16'] |
| 四 | 相 main の組 main（23.5 秒） | 期待どおり |  |
| 四 | 相 recompute の組 hook（25.9 秒） | 期待どおり |  |
| 四 | 相 recompute の組 rewrite（23.6 秒） | 期待どおり |  |
| 四 | 相 recompute の組 reextract（14.5 秒） | 期待どおり |  |
| 四 | 一致だけを見る段 | 期待どおり | [analyze_Bprime] 一致だけを見る段: 一致 True（一段目 True・二段目 True・再抽出 True）・理由 None |
| 四 | 結果を開く段 | 期待どおり | [analyze_Bprime] 結果を開く段: 書いた analysis.json（SHA16 EE41038C42CD043C） |
| 四 | 掃き出し（欠け零） | 期待どおり | [sweep_Bprime] 欠け 0 |
| 四 | 集計の出力の枝の形（バッチ・外した升目・道の違い） | 期待どおり | {'batch': 16, 'dropped': [], 'N1 の行': 4, '道の違い': None} |
| 四 | 報告の組み立てと走査（当たり零） | 期待どおり | 行 425・当たり []・nuclear の族の行の節 []・道の違いの行 0・器の誤りの行 なし（期待 なし） |
| 四 | 判定の後の差し替えで結果を開く段が止まる | 期待どおり | 結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない） |
| 四 | 〔N1 を外す〕写しの下見の決定 | 期待どおり | {'q1': '一部の升目を外して続ける', 'n_pass': 6, 'n_main': 8, 'dropped': ['N1\|O-Ncold', 'N1\|Onull'], 'stop': False, 'reason': None} |
| 四 | 〔N1 を外す〕相 main の組 main（21.5 秒） | 期待どおり |  |
| 四 | 〔N1 を外す〕相 recompute の組 hook（23.2 秒） | 期待どおり |  |
| 四 | 〔N1 を外す〕相 recompute の組 rewrite（21.9 秒） | 期待どおり |  |
| 四 | 〔N1 を外す〕相 recompute の組 reextract（14.5 秒） | 期待どおり |  |
| 四 | 〔N1 を外す〕一致だけを見る段 | 期待どおり | [analyze_Bprime] 一致だけを見る段: 一致 True（一段目 True・二段目 True・再抽出 True）・理由 None |
| 四 | 〔N1 を外す〕結果を開く段 | 期待どおり | [analyze_Bprime] 結果を開く段: 書いた analysis.json（SHA16 A72B8E804399C71A） |
| 四 | 〔N1 を外す〕掃き出し（欠け零） | 期待どおり | [sweep_Bprime] 欠け 0 |
| 四 | 〔N1 を外す〕集計の出力の枝の形（バッチ・外した升目・道の違い） | 期待どおり | {'batch': 16, 'dropped': ['N1\|O-Ncold', 'N1\|Onull'], 'N1 の行': 0, '道の違い': None} |
| 四 | 〔N1 を外す〕報告の組み立てと走査（当たり零） | 期待どおり | 行 401・当たり []・nuclear の族の行の節 ['summary', 'pilot']・道の違いの行 0・器の誤りの行 なし（期待 なし） |
| 四 | 〔バッチ一〕写しの (vi) の決定 | 期待どおり | {'stop': False, 'batch': 1, 'floor': 0.0, 'spread_a': 0.1, 'spread_b': 0.0} |
| 四 | 〔バッチ一〕相 main の組 main（31.8 秒） | 期待どおり |  |
| 四 | 〔バッチ一〕相 main の組 pathdiff（22.7 秒） | 期待どおり |  |
| 四 | 〔バッチ一〕相 recompute の組 hook（25.8 秒） | 期待どおり |  |
| 四 | 〔バッチ一〕相 recompute の組 rewrite（23.9 秒） | 期待どおり |  |
| 四 | 〔バッチ一〕相 recompute の組 reextract（14.7 秒） | 期待どおり |  |
| 四 | 〔バッチ一〕一致だけを見る段 | 期待どおり | [analyze_Bprime] 一致だけを見る段: 一致 True（一段目 True・二段目 True・再抽出 True）・理由 None |
| 四 | 〔バッチ一〕結果を開く段 | 期待どおり | [analyze_Bprime] 結果を開く段: 書いた analysis.json（SHA16 C9A2DF3311273A87） |
| 四 | 〔バッチ一〕掃き出し（欠け零） | 期待どおり | [sweep_Bprime] 欠け 0 |
| 四 | 〔バッチ一〕集計の出力の枝の形（バッチ・外した升目・道の違い） | 期待どおり | {'batch': 1, 'dropped': [], 'N1 の行': 4, '道の違い': True} |
| 四 | 〔バッチ一〕報告の組み立てと走査（当たり零） | 期待どおり | 行 426・当たり []・nuclear の族の行の節 []・道の違いの行 1・器の誤りの行 なし（期待 なし） |
| 四 | 〔器の誤りで閉じた行動の下見〕閉じた記録（系統外の採点ができなかった文） | 期待どおり | 系統外の模型による採点ができなかった（行動の下見が器の誤りで終わった） |
| 四 | 〔器の誤りで閉じた行動の下見〕相 pilot | 期待どおり | (iii) tool_error |
| 四 | 〔器の誤りで閉じた行動の下見〕相 main の組 main（23.0 秒） | 期待どおり |  |
| 四 | 〔器の誤りで閉じた行動の下見〕相 recompute の組 hook（26.1 秒） | 期待どおり |  |
| 四 | 〔器の誤りで閉じた行動の下見〕相 recompute の組 rewrite（23.7 秒） | 期待どおり |  |
| 四 | 〔器の誤りで閉じた行動の下見〕相 recompute の組 reextract（14.6 秒） | 期待どおり |  |
| 四 | 〔器の誤りで閉じた行動の下見〕一致だけを見る段 | 期待どおり | [analyze_Bprime] 一致だけを見る段: 一致 True（一段目 True・二段目 True・再抽出 True）・理由 None |
| 四 | 〔器の誤りで閉じた行動の下見〕結果を開く段 | 期待どおり | [analyze_Bprime] 結果を開く段: 書いた analysis.json（SHA16 B44ED67CE439302D） |
| 四 | 〔器の誤りで閉じた行動の下見〕掃き出し（欠け零） | 期待どおり | [sweep_Bprime] 欠け 0 |
| 四 | 〔器の誤りで閉じた行動の下見〕集計の出力の枝の形（バッチ・外した升目・道の違い） | 期待どおり | {'batch': 16, 'dropped': [], 'N1 の行': 4, '道の違い': None} |
| 四 | 〔器の誤りで閉じた行動の下見〕報告の組み立てと走査（当たり零） | 期待どおり | 行 399・当たり []・nuclear の族の行の節 []・道の違いの行 0・器の誤りの行 あり（期待 あり） |
| 四 | 〔出口の値を大きく〕相 extract（同じ模型で抽出の記録を取り直す） | 期待どおり |  |
| 四 | 〔出口の値を大きく〕相 main の組 main（22.8 秒） | 期待どおり |  |
| 四 | 〔出口の値を大きく〕相 recompute の組 hook（25.8 秒） | 期待どおり |  |
| 四 | 〔出口の値を大きく〕相 recompute の組 rewrite（24.3 秒） | 期待どおり |  |
| 四 | 〔出口の値を大きく〕相 recompute の組 reextract（14.6 秒） | 期待どおり |  |
| 四 | 〔出口の値を大きく〕一致だけを見る段 | 期待どおり | [analyze_Bprime] 一致だけを見る段: 一致 True（一段目 True・二段目 True・再抽出 True）・理由 None |
| 四 | 〔出口の値を大きく〕結果を開く段 | 期待どおり | [analyze_Bprime] 結果を開く段: 書いた analysis.json（SHA16 05EAFD28479C31B7） |
| 四 | 〔出口の値を大きく〕掃き出し（欠け零） | 期待どおり | [sweep_Bprime] 欠け 0 |
| 四 | 〔出口の値を大きく〕集計の出力の枝の形（バッチ・外した升目・道の違い） | 期待どおり | {'batch': 16, 'dropped': [], 'N1 の行': 4, '道の違い': None} |
| 四 | 〔出口の値を大きく〕報告の組み立てと走査（当たり零） | 期待どおり | 行 423・当たり []・nuclear の族の行の節 []・道の違いの行 0・器の誤りの行 なし（期待 なし） |
| 〇 | 走りの始めと終わりで器と正本と台帳の SHA16 が同じ（公開の形の置き場） | 期待どおり |  |
| 〇 | 別の個体の二つの器が作業の置き場と公開の形で同じバイト（終わり・U01） | 期待どおり | {'bprime_recompute_rewrite.py': True, 'bprime_reextract.py': True} |

## 走らせた器と正本と台帳の SHA16（公開の形の置き場で取った・走りの始めと終わりで同じ）

| 置き場 | SHA16 |
|---|---|
| tools/analyze_Bprime.py | 135CE9DFD55467E1 |
| tools/bl3_core.py | E8CD3A24950F8581 |
| tools/bl3_directions.py | 4BE7E44D135849F4 |
| tools/blens_core.py | DB3092B1EF0B88B3 |
| tools/bprime_behavior.py | 03D41C1C78947057 |
| tools/bprime_cells.py | B806BEB9C181638E |
| tools/bprime_core.py | A1C2285856A4DA08 |
| tools/bprime_directions.py | 8D999D06A7773343 |
| tools/bprime_external.py | C12A4931B85B1CE4 |
| tools/bprime_facts.py | 56C5F2E98FD7C27D |
| tools/bprime_gemma.py | B89384C82C3F92CC |
| tools/bprime_meaningless.py | 85F44B995CB994C8 |
| tools/bprime_numbers_lint.py | F0F8F559A340FDCB |
| tools/bprime_phases.py | 1F6B77917BAA7C72 |
| tools/bprime_publish_map.py | 64C5E490620F86BD |
| tools/bprime_recompute_rewrite.py | DF0833637E5755D8 |
| tools/bprime_reextract.py | AEF215AA0F577E45 |
| tools/bprime_run.py | 8A37DE1CA759A491 |
| tools/bprime_typo.py | FEB15E855E4234E3 |
| tools/build_report_Bprime.py | 99F4149FC1B8A3AC |
| tools/close_behavior_Bprime.py | 42018C96F163B735 |
| tools/colab/boot_bprime.py | DD601F674E1DD2C8 |
| tools/direction_B.py | E84A101655685F2B |
| tools/dry_bprime.py | C7202DF71D8FBDA4 |
| tools/dry_bprime_behavior.py | E568A627F4292D12 |
| tools/dry_run_Bprime.py | 978A9E0A20C68922 |
| tools/freeze_Bprime.py | C0B98FB501199189 |
| tools/g4_attempts_Bprime.py | 6BBE082971844B59 |
| tools/make_contrasts_Bprime.py | 5ED8172E147EFEC2 |
| tools/make_frozen_B.py | A333488A9437EF68 |
| tools/make_frozen_Bprime.py | 868DEA78E8CCD0A8 |
| tools/make_predictions_form_B.py | A213804DCB730737 |
| tools/make_predictions_form_Bl3.py | 6305BB5766F0F6B6 |
| tools/make_predictions_form_Bprime.py | 9C400361140944E2 |
| tools/numbers_lint.py | 88B6A53BBEC80602 |
| tools/publish_Bprime.py | F74C0978352962C3 |
| tools/qf_task_B.py | 86D71D789BB7A320 |
| tools/response_mode_A.py | C3E90B11B62F67A5 |
| tools/run_stageB_local.py | E976A4F5B63767FA |
| tools/runs_A.py | A57BE1F5EEACBBB2 |
| tools/runs_B.py | 269B60867D0924EB |
| tools/seal_Bprime.py | 0719E21A6EBFD2C7 |
| tools/send_external_Bprime.py | 465E0627A34DCA9C |
| tools/steer_B.py | 71157C6921E12AC7 |
| tools/sweep_Bprime.py | 876C6F9EE7054EB8 |
| design/contrasts-Bprime.json | 5899C06207666C21 |
| tools/ledger-bprime.json | 569CEC81C8F2E7BE |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
