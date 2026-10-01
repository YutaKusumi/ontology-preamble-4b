# 一巡目の採否で確かめた事実（機械で抜き出した・B′ の設計の巡・二巡目の束・2026-09-29・コーディネータ南無弥勒如来・非公開）

- 何か: 一巡目の採否の表（`adoption-design-round1.md`）の「確かめ」の欄の事実を、出所のファイルから器 `make_facts_round1.py` が抜き出したもの。値は出所から読み、手で打っていない。出所の置き場の名は、公開の置き場（`ontology-preamble-4b` の版 0a45688 の後の手元の写し）と、非公開の作業場（B′）。

## 1. 層三の最終版（公開の置き場 `records/Bl3/results-Bl3-FINAL-2026-09-27.md`・SHA16 90EEB93792733FAC）の行（逐語）

- 146 行目: バッチの大きさ 1・揺れの床 0・近道の許容 0.005
- 470 行目: 【逸脱 D-BLT1】計算の道: 札と門は、本の計算の一つの道（バッチの大きさ 1・近道なし・NVIDIA L4・組の session の記録にある版）の上の記述である。道を替えたときに効き目と札がどれだけ動くかは測っていない。下見で測ったのは無操作の値の動きだけで、(vi) の (a) の升目の間の最大 1.621（S4|Onull・揺れの上限 0.01 の 162 倍）・(v) の主の升目の最大 1.621（N1|Onull・門の行だけの升目 2.737）。これは等方の効き目の四分位の幅（1.12〜1.87）と主の行の効き目の大きさ（0.546〜2.734）と同じ桁。
- 471 行目: 【逸脱 D-BLT1】床からの余白が (vi) の (a) の幅より小さい主の升目: N1|O-Ncold（余白 0.427・幅 0.6899）・S4|Onull（余白 1.489・幅 1.621）。これらの升目が下見を通ったことも、道に依る幅の中にある。

## 2. Gemma-4-31B-it の設定（固定の版 `842da3794eaa0b77d5f08bae87a17459d91ff475`・`config.json` SHA16 E967DD38BC5CFD38・`generation_config.json` SHA16 D4226BBE3117D2D2・`tokenizer.json` SHA16 CC8D3A0CE36466CC）

- 上の階層の `final_logit_softcapping`: null・`text_config` の中: 30.0
- `text_config` の `num_hidden_layers` 60・`hidden_size` 5376・`sliding_window` 1024・`attention_k_eq_v` true・`global_head_dim` 512
- `layer_types` の全体の注意（full_attention）の層の添字: 5・11・17・23・29・35・41・47・53・59（添字 29 の種類: full_attention）
- 止める印: 上の階層の `eos_token_id` [1, 106]・`text_config` の `eos_token_id` 1・`generation_config.json` の `eos_token_id` [1, 106, 50]
- トークンの字（`tokenizer.json` の added_tokens）: 1＝`<eos>`・50＝`<|tool_response>`・106＝`<turn|>`
- `generation_config.json` の既定の標本化: temperature 1.0・top_p 0.95・top_k 64・do_sample true（B′ は使わない・11-A）

## 3. 段階 B の正本（公開の置き場 `design/contrasts-B.json`・SHA16 EF0DF4295B68F949）

- `runner.generation`: temperature 0.7・top_p 0.9・max_tokens 4096
- `runner.generation_explicit`: top_k 20・min_p 0.0・repetition_penalty 1.0・no_repeat_ngram_size 0・`passed_keys` ["min_p", "no_repeat_ngram_size", "repetition_penalty", "top_k"]
- `arms.panel`: O・Osec・Onull・Nk・N・O-Ncold・Osec-Ncold・Onull-Ncold・`extraction_scenarios`: N1・S1（段階 B の `direction_B.h_norm_record` の ‖h‖ はこの八腕 × 二場面の平均）

## 4. 層三の比の出し直し（段階 B の凍結の活性から・コーディネータの計算）

- 活性 `results/dirB/dirB__s1/main_position_activations.npz`（SHA16 7F41AC1B3BC02B7A）の割合 0.5 の `same_order` の十六文脈から: 次元 2560・‖h‖ の平均 42.775712865・‖v̂‖ 1.301227683・比 0.030419778
- 記録 `results/dirB/dirB__s1/layers.json`（SHA16 9E40DB6D680AED0D）の割合 0.5: `h_norm_main` 42.775711060・`vhat_norm` 1.301227689・`vhat_over_h` 0.030419779・差（出し直し − 記録）-1.42e-09

## 5. 器の行（逐語）

- `Bprime/tools/boot_bprime_cost.py`（SHA16 20131BFC137A6C57）の費用の見込みの式:
  - 139 行目: `per = {r['batch']: r for r in REC['forward'] if r['layers']}`
  - 140 行目: `n_dir = 1 + 4 + 1999 + 56`
  - 141 行目: `n_fwd16 = 12 * int(np.ceil(n_dir / 16)) + 3 * int(np.ceil((1 + 56) / 16))`
- 公開の置き場 `tools/blens_core.py`（SHA16 DB3092B1EF0B88B3）の `iso_directions`（乱数は種・層の割合・次元だけで引き、ノルムは後で合わせる）:
  - 99 行目: `def iso_directions(v_hat_static, seed, layer_ratio, count, key_scale):`
  - 100 行目: `    """`steer_B.random_directions` と同じ作り方（種と本数だけを変える・凍結の関数は種を正本から取るので写した）。"""`
  - 101 行目: `    d = int(np.asarray(v_hat_static).shape[-1])`
  - 102 行目: `    ss = np.random.SeedSequence([seed, int(round(layer_ratio * key_scale))])`
  - 103 行目: `    rng = np.random.default_rng(ss)`
  - 104 行目: `    target = float(np.linalg.norm(v_hat_static))`
  - 105 行目: `    out = []`
  - 106 行目: `    for i in range(count):`
  - 107 行目: `        g = rng.normal(size=d)`
  - 108 行目: `        n = float(np.linalg.norm(g))`
  - 109 行目: `        out.append(g * (target / n) if n else g)`
  - 110 行目: `    return np.array(out)`

## 6. 式から出した値（コーディネータの計算）

- softcap の抜けの差 z − 30·tanh(z/30): z＝10 で 0.3546・11 で 0.4678・12 で 0.6015・差が 0.5 に届く z は 11.256
- softcap の傾き sech²(z/30): z＝20 で 0.6604・30 で 0.4200
- `p_bounds` [0.0001, 0.9999] の両端の対数オッズ: -9.2102・9.2102
- 層三の偶然の目安: 8/49 ＋ 8/55 ＝ 0.3087（正本 `nulls.real.chance_second` と同じか: True）・8/25 ＋ 8/28 ＝ 0.6057（`chance_second_pair` と同じか: True）
- 隠れの次元の比: √(5376/2560) ＝ 1.4491・2560/5376 ＝ 0.4762

## この記録が確認していないこと

- 公開の置き場の写しが GitHub の上の版と同じか（手元の写しの版 0a45688 の後に push は無い）。
- 固定の版の Gemma の設定が、実物の重みの読み込みで同じ値になるか（凍結の前の確かめで見る）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
