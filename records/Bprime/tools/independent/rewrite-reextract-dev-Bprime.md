# B′ 独立の再計算——残差の書き換えの道と独立の再抽出の道の開発の記録

<!-- generated: rewrite-reextract-dev-Bprime（一時置き場の組み立ての器が、器の出力・正本・ファイルから数とハッシュを機械で写して組み立てた） -->

- 器（二つ・どちらも v1）:
  - `Bprime/tools/independent/bprime_recompute_rewrite.py`（SHA-256 DF0833637E5755D86FDF7B7B7A64F00284E0B5678C034C2A6103E1B6CBB9611F・67860 バイト）
  - `Bprime/tools/independent/bprime_reextract.py`（SHA-256 AEF215AA0F577E45885F777C7180246C21F97CF9F36D4916F9FC1A5D97ED6096・29524 バイト）
  - §4・§5 の出力はこの版の器が出した（本番の走りの前に器の SHA-256 を一時置き場に書き、この記録を組み立てる時に今の器と一致することを機械で確かめた・§4 と §5 の頭の行）。
- 事前登録の文: `Bprime/tools/independent/dry-preregistration-Bprime.txt`（SHA-256 4344FA06C48E09B611714E83D833FF05DB6B274CF193E46535311BC2D07D248B・ファイルの最後の書き込み 2026-09-30 04:52:18 UTC）。
- 書き手: 系統内の新しい個体（Claude Opus 5.5・Claude Code の下請けの個体）。本の器の書き手（コーディネータ・南無弥勒如来）とは別の個体で、登録者（楠見優太さん）の許可による（裁定 D270）。
- 指示: `Bprime/tools/independent/instructions-rewrite-reextract-Bprime.txt`（SHA-256 4F41E5948F86EBE3794056655B59E8D8D31656BC42805DE63C9BFD06D8A485C7・16694 バイト）。作業の頭に全文を読み、渡された SHA-256 とバイト数に一致することを確かめてから進めた。このファイルは変えていない。
- 組み立て: 2026-09-30 05:45:55（UTC）
- 状態: B′ の作業場は git の置き場ではない。新しく書いたファイルは `Bprime/tools/independent/` の中の四つ（二つの器・事前登録の文・この記録）だけで、ほかのファイルは一つも変えていない（§8 の機械の確かめ）。コミットも push もしていない。
- 数・ハッシュ・引用の出所: §4・§5 は器の出力の逐語の写し。本文の数とハッシュは組み立ての器が、器の出力・正本・台帳・ファイルから機械で写した。手で打った数は、器の中の定数（小さな模型の形・乱数の種・係数 2.0）と、指示と正本から写した決まりの値（許容など）を、器の書き方として引いた所だけ。

## 0. 要約

- 書き換えの道の自己検査（`--selftest`・乱数の小さな模型・float32 と bfloat16）: `selftest: 82/82 ok`（exit=0）
- 再抽出の道の自己検査（`--selftest`）: `selftest: 23/23 ok`（exit=0）
- 書き換えの道の突き合わせ（`--dry`・コーディネータのフックの道の公開の関数を中を見ずに呼んだ）:
  - `[float32] 差の絶対値の最大: 効き目 3.61e-07・無操作の量 7.82e-08`
  - `[float32] dry: 一段目の許容（0.001）の内（差の最大 3.61e-07）`
  - `[bfloat16] 差の絶対値の最大: 効き目 5.36e-07・無操作の量 2.09e-07`
  - `[bfloat16] dry: 一段目の許容（0.001）の内（差の最大 5.36e-07）`
  - `dry: 二つの型とも一段目の許容の内`
- 再抽出の道の突き合わせ（`--dry`・コーディネータの `BD.activations` を中を見ずに呼んだ）:
  - `[float32] ‖h‖ の相対の差の最大 0・余弦の最小 1.000000000000・四つともビット単位で同じ: True`
  - `[float32] dry: 再抽出の許容（rel_tol 1e-05・cos_min 0.99999）の内`
  - `[bfloat16] ‖h‖ の相対の差の最大 0・余弦の最小 1.000000000000・四つともビット単位で同じ: True`
  - `[bfloat16] dry: 再抽出の許容（rel_tol 1e-05・cos_min 0.99999）の内`
  - `dry: 二つの型とも再抽出の許容の内`
- 歯の変種（参考・判定に入れない・事前登録つき）: float32 の模型では対照（M0）は許容の内・わざと誤らせた 8 変種のうち 7 を捕まえ、捕まえなかったのは M7；bfloat16 の模型では対照（M0）は許容の内・わざと誤らせた 8 変種のうち 8 を捕まえ、捕まえなかった変種は無い。事前登録の予想の外れは無い（§5.3）
- 正本 `independent_recompute.agreement` の後半（二つの道の値からそれぞれ出した札が同じこと）は、この器では見ていない（札は集計の器の仕事）。
- 正本で決まっていなかった所は §6、コーディネータに伝えたいことは §7、検分票は末尾（判定は保留）。

## 1. 読んだもの

組み立ての器が、読んだファイルの SHA-256（生のバイト）を計算した。どれも読むだけで、変えていない。

| 読んだもの | 路 | バイト | SHA16 |
|---|---|---|---|
| 指示 | `Bprime/tools/independent/instructions-rewrite-reextract-Bprime.txt` | 16694 | 4F41E5948F86EBE3 |
| 正本 | `Bprime/design/contrasts-Bprime.json` | 168512 | 99E8F2BD3C2D4EA2 |
| 草案9 | `Bprime/design/design-Bprime-draft9.md` | 127063 | 4E4DF648DE36C700 |
| 台帳 | `Bprime/tools/ledger-bprime.json` | 9236 | 569CEC81C8F2E7BE |
| PUB run_stageB_local | `PUB/tools/run_stageB_local.py` | 60349 | E976A4F5B63767FA |
| PUB direction_B | `PUB/tools/direction_B.py` | 28850 | E84A101655685F2B |
| PUB bl3_core | `PUB/tools/bl3_core.py` | 30625 | E8CD3A24950F8581 |
| PUB runs_B | `PUB/tools/runs_B.py` | 24720 | 269B60867D0924EB |
| PUB bl3_recompute_rewrite | `PUB/tools/bl3_recompute_rewrite.py` | 51964 | 012CB2B68397614A |
| PUB recompute-rewrite-dev-Bl3 | `PUB/records/Bl3/tools/recompute-rewrite-dev-Bl3.md` | 59461 | F03F51731422643C |
| pylib modeling_gemma4 | `Bprime/pylib/transformers/models/gemma4/modeling_gemma4.py` | 124550 | 3F6A049B83B79BE6 |
| pylib configuration_gemma4 | `Bprime/pylib/transformers/models/gemma4/configuration_gemma4.py` | 16585 | 34183785AE107AFA |
| pylib masking_utils | `Bprime/pylib/transformers/masking_utils.py` | 80358 | C159CD91C2A7FCAF |
| pylib sdpa_attention | `Bprime/pylib/transformers/integrations/sdpa_attention.py` | 8846 | 53C7229DACA9ADE4 |
| pylib utils/generic | `Bprime/pylib/transformers/utils/generic.py` | 42839 | B60D9ECBBAEADB08 |
| pylib utils/output_capturing | `Bprime/pylib/transformers/utils/output_capturing.py` | 12672 | 28921DCA36F8892E |
| pylib cache_utils | `Bprime/pylib/transformers/cache_utils.py` | 103625 | 4B284431CB3A881B |
| pylib modeling_layers | `Bprime/pylib/transformers/modeling_layers.py` | 30866 | 721D419A5E23F9B9 |
| hf config.json | `Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475/config.json` | 4621 | E967DD38BC5CFD38 |
| hf MANIFEST-local.json | `Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475/MANIFEST-local.json` | 1060 | 42C658099463A50D |
| hf model.safetensors.index.json | `Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475/model.safetensors.index.json` | 120246 | D4AFF3B976D69C12 |
| hf tokenizer.json | `Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475/tokenizer.json` | 32169626 | CC8D3A0CE36466CC |
| hf chat_template.jinja | `Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475/chat_template.jinja` | 18683 | AE53464BF3BE2580 |

- 正本は、指示の読む範囲の鍵を読んだ: `independent_recompute`（全体）・`readout.primary`（全体）・`layers`（全体）・`inputs.model_facts`・`directions` の `named`・`defs`・`extraction`・`nulls.real` の `arms`・`swap_siblings`・`main_rows`・`cells_main`・`pilot.decision`・`computation.shortcut`。ほかに、鍵の名の一覧だけ（中身ではない）を、正本の頭・`inputs`・`readout`・`directions`・`nulls`・`nulls.real`・`pilot`・`computation` について見た。
- 草案 9: §3（読み取り・3.1〜3.6）と §12（器と確かめ）。見出しの一覧も見た。
- 台帳: 全体（升目 8・抽出の文脈 16・prefix_ids・heads・arms・meta）。`ledger-bprime.md` は読んでいない。
- 公開の置き場の凍結の器（読むだけ）: `run_stageB_local.py` は頭の文から `make_hook` まで（`frozen_rd`・`check_assembly_matches_frozen`・`arm_texts`・`scenario_and_instruction`・`user_message`・`base_arm_of`・`arm_plan`・`make_hook`）と、関数の名の一覧。**`make_hook` は加減の算術の決まりを知るためだけに読み、呼んでいない。** `direction_B.py` は頭の文と `layer_index`・`hidden_states_index`・`decoder_layers` の頭。`bl3_core.py` は頭の文・`lse`・`log_odds_a` の頭・`comparators_for`・`blens_own_pair`・`recompute_set`・`batch_plan`・`ledger_chain_bad`・`_selftest` の頭。`runs_B.py` は `REPO`・`load_T`・`sha16_file` の行（検索の出力）。
- 層三で別の個体が書いた道 `bl3_recompute_rewrite.py`（頭から自己検査の途中まで）と、その開発の記録 `recompute-rewrite-dev-Bl3.md`（全体）。参考にした点: 検分票の形・歯の変種の型・mask の組み方を模型の forward のどの呼び方に合わせるかという教訓・float32 を経る型の直し。
- pylib の transformers 5.16.1: `models/gemma4/modeling_gemma4.py`（頭・`Gemma4RMSNorm`・rotary と `repeat_kv`・`eager_attention_forward`・文字の側の MLP・rotary・注意・MoE の部品・復号の層・埋め込み・`_init_weights`・`Gemma4TextModel`・`Gemma4ForCausalLM`・多様式の埋め込み器・`create_masks_for_vision_model`・`Gemma4Model`・`Gemma4ForConditionalGeneration`）・`configuration_gemma4.py`（`Gemma4TextConfig`〜`Gemma4Config`）・`masking_utils.py`（mask の関数・`_ignore_causal_mask_sdpa`・`sdpa_mask`・`find_packed_sequence_indices`・`_preprocess_mask_arguments`・`create_causal_mask`・`create_sliding_window_causal_mask`・`LAYER_PATTERN_TO_MASK_FUNCTION_MAPPING`・`create_masks_for_generate`）・`integrations/sdpa_attention.py`（全体）・`utils/generic.py` の `merge_with_config_defaults`・`utils/output_capturing.py`（全体）・`cache_utils.py` の `DynamicLayer` と `DynamicSlidingWindowLayer`・`modeling_layers.py` の `GradientCheckpointingLayer`。
- 模型の設定の置き場: `config.json`・`MANIFEST-local.json`（全体）・`model.safetensors.index.json`（器で重みの名だけを数えた: layer_scalar の数・層 29 の鍵・最終の正規化・lm_head・層ごとの入力の鍵）・トークナイザとチャットの型（`AutoTokenizer` で読んだだけ）。**実の重みは無く、読んでいない。**
- 検分の手順書（kensho）の `SKILL.md` と `references/frozen-lessons.md`（全体）。読んだ時は §5.3 の注のとおり。
- 登録者の記憶の索引（会話の頭に渡されたもの）: 作業の文脈として。

## 2. 読まなかったもの

- コーディネータの器（`Bprime/tools/` の `bprime_run.py`・`bprime_directions.py`・`bprime_phases.py`・`bprime_gemma.py`・`bprime_core.py`・`bprime_behavior.py`・`dry_bprime*.py`・`analyze_Bprime.py`・`build_report_Bprime.py`・`colab/`・`prev/` の中身）と器の段の記録 `tools-log-Bprime.md` は開いていない（指示）。`bprime_run` と `bprime_directions` は `--dry` の中でだけ import し、指示にある公開の関数（`Runner`・`build_cells`・`recompute_hook_path`・`activations`）を中を見ずに呼んだ。落ちたときは例外の種類と文言だけを印字する形にした（traceback を出さない）。`build_cells` の戻り値の中も見ていない。器の同定のために、二つのファイルの SHA-256 だけを組み立ての器が計算した（中身は表示していない）。
- 自分から読まなかったもの: 正本の上に書いた鍵の外（`directions.norm_rule`・`directions.storage`・`coefficient`・`nulls.real` のほかの鍵・`inputs.versions` など）・草案 9 の §3 と §12 の外・`assembly-contract`・`glossary`・裁定の文書・`ledger-bprime.md`・`bprime_cells.py` ほか指示の外の器。
- 見たのは名前と大きさだけのもの: `Bprime/`・`Bprime/tools/`・`Bprime/tools/independent/`・`Bprime/design/`・`Bprime/pylib/transformers/models/gemma4/`・設定の置き場・公開の置き場の `tools/` と `records/Bl3/tools/` のファイルの一覧と、`Bprime/` と公開の置き場の `tools/` の直近に書かれたファイルの名（作業の頭に、版の確かめの走りが .pyc を書いていないかを見るため）。§8 の機械の確かめでは、二つの置き場の全ファイルの路・大きさ・更新時刻を数えた（中身は読んでいない）。
- 検索の扱い: 読む範囲のファイルだけを検索の相手にした（`Bprime/tools/` 全体を相手にした検索はしていない）。

## 3. 書き方の決め

### 3.1 層の回し方

transformers 5.16.1（台帳 `meta.transformers`）の `Gemma4ForConditionalGeneration.forward` → `Gemma4Model.forward` → `Gemma4TextModel.forward` の、文字だけの入力・バッチ一・attention_mask なしの道筋を、部品を差し替えずに写した（版が違えば止める）。各段の出典の行は §9 のピン留めで機械が照らした。

1. 置き換えの印: `Gemma4Model.get_placeholder_mask(input_ids, None)` で画像・動画・音声のトークンの印を取り、一つでもあれば止める（写したのは文字だけの道）。模型と同じく `torch.where(印, text_config.pad_token_id, ids)` を通す（文字だけなら同じ並び）。
2. 埋め込み: `Gemma4Model.get_input_embeddings()`（＝言語の模型の `embed_tokens`・`Gemma4TextScaledWordEmbedding`）を呼ぶ（§3.3）。
3. 層ごとの入力（`hidden_size_per_layer_input` が 0 でなければ）: 多様式の本体と同じく `get_per_layer_inputs(ids, 埋め込み)` の後、言語の模型の中と同じく `project_per_layer_inputs(埋め込み, …)` を通し、層 i に `[:, :, i, :]` を渡す（§3.4）。
4. 位置の番号: `arange(列の長さ).unsqueeze(0)`（多様式の本体が作り、言語の模型にそのまま渡る）。
5. mask: 多様式の本体と同じく `create_masks_for_generate(config=text_config, inputs_embeds, attention_mask=None, past_key_values=None, position_ids)` で注意の型ごとの辞書を作る（§3.2）。関数は `modeling_gemma4` の名の束ねから引く（模型の組み立てが呼ぶ物と同じ物）。
6. cache: 既定は作らない（層に `past_key_values=None`・指示の「`use_cache=False` と同じ」）。`use_cache=None` を渡すと模型の forward の既定の解き方（最上位の設定の `use_cache` → 無ければ言語の設定の `use_cache`）で決め、真なら一回の順伝播ごとに空の `DynamicCache(config=言語の設定)` を作って捨てる（順伝播をまたいで使い回さない＝近道ではない・§6 の一）。
7. rotary: 注意の型ごとに `rotary_emb(埋め込み, position_ids, 型)` を一度作り、その型の層に渡す。
8. shared_kv_states: 一回の順伝播ごとに空の `UserDict` を作り、全ての層に同じものを渡す（B′ の模型は `num_kv_shared_layers`＝0 で、各型の最後の層が書き込むだけ）。
9. 層を順に `layer(h, 層ごとの入力, shared_kv_states=…, position_embeddings=pe[型], attention_mask=mask[型], position_ids=…, past_key_values=…)` で呼ぶ（模型の forward と同じ引数。模型の forward は `labels=None` などの使われない鍵も層へ渡すが、注意の器まで届いて使われずに捨てられるので渡していない）。層 L の出力を得た直後に書き換える（§3.5）。
10. 最後の層の出力（＝最終の正規化の入力）を返す。最終の正規化・語彙の行列・softcap の順伝播は呼ばず、読み取りは float32 で自分で当てる（§3.6）。

層の中身（注意・MLP・層の中の正規化・`layer_scalar`）は模型の部品をそのまま呼び、書き直していない（書き直すと突き合わせの相手と演算が変わる）。フックは一本も掛けない（§3.7）。

### 3.2 mask と rotary

- transformers 5.16.1 では、多様式の本体（`Gemma4Model.forward`）が cache を作る前に mask を作る（`past_key_values=None`）。そのため、層三（transformers 4.57.3・Qwen）で分かれた、use_cache の有無で mask が None か明示かが変わる形は、この版の Gemma 4 の道では起きない（mask の形は use_cache に依らない）。自己検査の参考の行（§4.1）のとおり、小さな模型（窓 < 列の長さ）では、全体の層の mask は None（SDPA の is_causal）、窓つきの層の mask は明示の真偽の mask だった。
- 本物の模型では、主の升目の列の長さの最大 503（台帳の readout_position＋1）と抽出の文脈の長さの最大 484 が窓（正本 `inputs.model_facts.sliding_window`＝1024）より短いので、注意の実装が sdpa なら、`_ignore_causal_mask_sdpa` の条件により窓つきの層の mask も None（is_causal）になると読める（ほかの注意の実装では mask の作り方が違う。どの実装でも、手回しの道は模型の forward と同じ関数で mask を作る）。**この読みは本物の模型で確かめていない。小さな模型は、窓つきの層が is_causal で走る形を試していない**（§7 の三）。
- rotary: 注意の型ごとに、模型の部品 `rotary_emb` を模型と同じ引数（埋め込み・位置の番号・型の名）で呼ぶ。型ごとの頭の次元と rotary の種類（設定の `rope_parameters`）は部品の中で扱われる。

### 3.3 埋め込みの倍率

- `Gemma4TextScaledWordEmbedding.forward` は `embedding(ids) × embed_scale.to(重みの型)`（倍率は √hidden を重みの型に直した値・bf16 では丸めが入る）。手回しの道は多様式の本体と同じく `get_input_embeddings()` を呼ぶので、倍率と丸めは模型と同じ。小さな模型の倍率は §4.1 の頭の行のとおり。

### 3.4 層ごとの入力と layer_scalar

- 本物の模型の設定は `hidden_size_per_layer_input`＝0・`num_kv_shared_layers`＝0・`enable_moe_block`＝false（設定の置き場の config.json）。器は層ごとの入力がある模型でも模型の forward と同じに流すよう書き、自己検査で層ごとの入力のある変種で確かめた（§4.1 の最後の二行）。
- 本物の重みの目録（`model.safetensors.index.json`）には `layer_scalar` の重みが 60 個ある（読み込むと 1 でない値になりうる）。層の出力は `layer_scalar` を掛けた後の値で、フックの道が掛ける「層の出力」とこの道が書き換える値は同じ所（`layer_scalar` の後）。指示の作り方の小さな模型では `layer_scalar` は 1 なので、自己検査の変種で一様乱数 [0.5, 1.5) にして、手回しの道が模型の forward とビット単位で一致することを確かめた。

### 3.5 書き換えの位置と型（層の出力の型のまま足す）

- 層 L（本物の模型では正本 `layers.index`・小さな模型では `direction_B.layer_index(正本 layers.ratio, 層の数)`）の出力 h（模型の型・[1, n, d]）に対して、
  `add = int(sign) * float(coef) * torch.as_tensor(np.asarray(v, dtype=np.float32), dtype=h.dtype, device=h.device)`、`h[0, mp:, :] = h[0, mp:, :] + add`。
  段階 B の `make_hook` の算術（NumPy の float32 を経て層の出力の型に直し、Python の数 sign×coef を掛け、主位置から後ろに層の出力の型のまま足す）と同じ形。本の計算（bf16）では、足す量も足し算も bf16。係数は一度だけ。
- 帯: 主位置 mp（プロンプトの最後のトークン `<channel|>`）から列の最後（読み取りの位置）まで。
- 無操作: 零のベクトルを同じ算術で足す（値は変わらない）。符号は行の符号にした（どちらの符号でも値は同じ）。

### 3.6 読み取り

- 最後の層の出力の最後の位置を float32 に上げ、`x × rsqrt(mean(x²) + eps) × g`（g＝言語の模型の最終の正規化の重みの float32・eps＝その `eps`・1＋g ではない）→ 語彙の行列（`lm_head.weight`・埋め込みと共有であることを確かめる）の読み取りの集合の行を float32 で掛ける → softcap（cap × tanh(z ÷ cap)・cap＝`text_config.final_logit_softcapping`）→ 量＝z_a − logsumexp（ほか）を float32 で。効き目＝加えた値 − 無操作の値（Python の数の引き算）。
- 模型の `Gemma4RMSNorm` は rsqrt でなく `torch.pow(·, −0.5)` を使う。指示の式どおり rsqrt にした（§6 の五）。
- 読み取りの集合: 族の選択の文字の順（正本 `readout.primary.letters`・先頭は破局の側の文字）と、最後に refuse の頭。番号は正本 `readout.primary.set_ids`・台帳の升目の `set_ids`・台帳の `heads` の `next` の三つで照らし、トークナイザで文字と「ref」に戻ることも確かめる。
- `hidden_states[-1]` は使わない（transformers 5.16.1 の `capture_outputs` は hidden_states の最後を `last_hidden_state`〔正規化の後〕で置き換える）。自己検査の歯で、取り違えると模型の出口の値から大きく離れることを確かめた（§4.1）。

### 3.7 フックの扱い

- 書き換えの道は hook を一本も掛けない（層を手で回す）。呼ぶ前と後に、模型のどの部品にも forward の hook（前・後）が無く、大域の hook も無いことを確かめ、あれば止める。
- 例外: transformers 5.16.1 の `output_hidden_states`（ほかの記録の要求も）は、初回に言語の模型の復号の層と注意の部品へ記録用の forward の hook（`transformers.utils.output_capturing` の `output_capturing_hook`）を据え付け、以後も居残る（記録の要求が無いときは何もせず、値を変えない）。これだけは数えない（関数の居場所の名と関数の名で見分ける）。草案 9 §12 の「B′ のフックの数え方（transformers 5 の居残るフックを数えない・`bprime_gemma` v0.1）」と同じ向きの扱いのはずだが、コーディネータの器の数え方は見ていない。
- 自己検査でだけ、確かめのために hook を三つの形で使った（どれも足すためではない）: 最終の正規化の前の hook で模型の forward の最終の正規化の入力を取る（指示が許す形）／止まるかを試すために、何もしない hook を選んだ層に掛けて外す／`output_hidden_states` で記録用の hook を据え付けさせる。ほかに、呼び出しの間に hook を掛けようとしないことを、`nn.Module` の hook を掛ける二つの関数を落ちる形に差し替えて確かめた（試験の後に戻した）。
- この確かめが見るのは、PyTorch に登録された forward の hook だけ。部品の forward を差し替える形の仕掛け（accelerate の装置合わせの `_hf_hook` など）や、関数の差し替えは数えていない（§検分票の最後の項）。

### 3.8 再抽出の取り方

- 選んだ書き方: 模型そのものの forward を `output_hidden_states=True`・`use_cache=False`・`logits_to_keep=1`・バッチ一で最後まで流し、`hidden_states[k+1]` の最後の位置（主位置）を取る。bf16 → float64 は丸めなしで上げる。
- 理由: (一) コーディネータの器（層の出力をフックで取り、その層で順伝播を打ち切る）と取り出しの書き方が違う。(二) 模型の forward の道筋（mask・cache・注意の実装）をそのまま使うので、本の抽出と「違うのは活性を取り出す書き方だけ」（正本 `independent_recompute.reextract.path`）に近い。(三) 書き換えの道の手回し（自分の写し）と独立に書けるので、再抽出と書き換えの二つの道が同じ誤りを共有しにくい——自己検査では、両者の値がビット単位で一致することを突き合わせた（§4.2）。
- 不利な点（先に書く）: transformers 5.16.1 の `output_hidden_states` は、上の記録用の hook で層の出力を集める。コーディネータの器とは、層の出力を forward の hook で受け取るという仕組みの層（PyTorch の hook の呼び出し）を共有する。ただし hook の関数と集め方は別の書き手（transformers）の物で、打ち切りもしない。また、この道は記録用の hook を模型に居残らせる（小さな模型で 12 本・本物の模型では復号の層と注意の部品の数だけと読める）。以後その模型を使う器は、この hook を数えない必要がある（§7 の二）。
- 最後の層は取らない（`hidden_states[-1]` は正規化の後）。主位置は列の最後（台帳の `main_position`＝長さ − 1 を照らす）。
- 名前のある方向: 腕ごとに二場面の平均（float64）を取り、正本 `directions.defs` の文（…h_X − h_Y…）から読んだ腕の差で作る。指示の対応（static＝O − Osec・loaded＝O-Ncold − Osec-Ncold・Nk＝Nk − N・td＝Onull − N）と正本の文が合わなければ止める（§4.2 の頭の二行）。

### 3.9 升目と文脈の組み立て

- 段階 B の組み立て（凍結の器 `run_stageB_local.user_message(arm_texts()[腕]['text'], 場面の本文, 指示)`・場面と指示は `scenario_and_instruction(場面)`）の user の発話一つに、`tok.apply_chat_template([...], add_generation_prompt=True, tokenize=True)` の `input_ids` を当てた（system なし）。書き換えの道はその直後に台帳の `prefix_ids` をトークンの並びのままつなぐ。再抽出の道はつながない。
- 照らすもの（違えば止める）: 升目は prompt_len・main_position（＝プロンプトの長さ − 1）・main_position_token・readout_position（＝列の長さ − 1）・ids_sha16（`hashlib.sha256(','.join(str(x) for x in 列).encode('ascii')).hexdigest().upper()[:16]`）・族・選択の文字・読み取りの集合。抽出の文脈は prompt_len・main_position・main_position_token・ids_sha16。台帳の `prefix_ids` と正本 `readout.primary.prefix_ids` の一致も照らす。

### 3.10 止める確かめ（器の中）

- 版と機種: transformers が台帳 `meta.transformers` の版でない／最上位・多様式の本体・言語の模型の型が Gemma 4 の物でない／eval でない／正本 `layers.layer_path` が言語の模型の層の並びを指さない／層の並びの数が設定と違う／語彙の行列が埋め込みと共有でない／最終の正規化が重みつきの `Gemma4RMSNorm` でない／その eps が設定と違う／softcap が設定に無い。
- 本の模型（層の数と次元が正本 `inputs.model_facts` と同じ）では加えて: bf16 でない／softcap と階層・語彙の数・窓・全体の注意の層の数が正本と違う／層の添字が正本 `layers.index`・`hidden_states_index` と合わない。選ぶ層の種類が正本 `layers.layer_type` と違えば、どちらの模型でも止める。
- hook: 呼ぶ前と後に、記録用のものを除く forward の hook（前・後・大域）があれば止める。
- 行と方向: names に三つの並びが無い／real: で始まらない名／iso の名が iso:0〜 の番号の形でない／`pilot['decision']['dropped']` が無いか、台帳に無い升目の鍵を含む／使う方向が dirs に無いか、float64 でないか、形が次元と合わないか、有限でない／係数が正の有限の数でない／同じ方向と符号が行に二度ある。
- 升目: §3.9 の照らしのどれかが違う。
- 書き換えが一度でない／出口の列の長さが入力と違う。
- 再抽出: 最後の層を求められた／hidden_states の数や形が違う／値が有限でない／dirs に名前のある方向が無いか、形・型が違う。

### 3.11 乱数の小さな模型と合成の方向（`--selftest`・`--dry` だけ）

- 指示の作り方を自分で書いた: 設定の置き場の `config.json` を辞書で読み、`text_config` を縮め（次元 64・中間 128・層 6・注意の頭 4・KV の頭 2・頭の次元 16・global_head_dim 32・num_global_key_value_heads 1・窓 8）、`layer_types` を選ぶ層（`direction_B.layer_index(0.5, 6)`）と最後の層を full_attention・ほかを sliding_attention にし、`vision_config` を縮め、`torch.manual_seed(0)` の後に `Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).eval()`。語彙の行列（埋め込みと共有）を 4 倍、最後の正規化の重みを一様乱数 [2, 3)（`torch.Generator().manual_seed(1)`）にした。
- 作ったままの模型は設定の dtype（bfloat16）で作られた（§4.1 の頭の行）。float32 の確かめは、その模型の写し（`copy.deepcopy`）を float32 に直した物で行った（重みの値は同じ・語彙の行列の共有が保たれることを器が確かめる）。
- 合成の方向: `np.random.default_rng(5)` で次元 64 の正規乱数を、static・loaded・Nk・td（正本 `directions.named` の順）・iso:0〜iso:9・real:＋正本 `nulls.real.arms` の八腕の i<j の全ての対の順に引き、ノルムを「残差のノルム」の 0.5 倍にそろえた。残差のノルムは、float32 の小さな模型の、主の八升目の層 L の出力（書き換えなし）の主位置のノルムの平均（§4.1 の参考の行）。係数は 2.0（書き手の選び）。
- 確かめは乱数の小さな模型だけで走る（次元と層の数が小さな模型の値でなければ止める——封印の前に本物の模型で値を出さない）。**コーディネータの合成の器とこの乱数の引き方が同じかは確かめていない**（`--dry` では同じ模型の物を両方の道に渡すので、突き合わせには効かない）。

## 4. 自己検査（`--selftest`）の結果——器の出力の逐語

### 4.1 書き換えの道

- 走らせた器の SHA-256（走らせる前に記録）: DF0833637E5755D86FDF7B7B7A64F00284E0B5678C034C2A6103E1B6CBB9611F（今の器と一致）
- 走りの時刻（UTC）: 2026-09-30 05:20:58 〜 2026-09-30 05:29:41・exit=0
- 標準出力の SHA-256（改行を LF にそろえたもの＝下の逐語の写しに末尾の改行を一つ足したバイト列）: 1BD3ADBD92515D202996F6C510838D63D7B101083EB8162FDE2350E13E4F5DDA
- 標準エラー: 空

```
bprime_recompute_rewrite v1 --selftest  torch 2.9.1+cpu・transformers 5.16.1・numpy 2.4.6・注意の実装 sdpa・作ったままの型 bfloat16
乱数の小さな模型: 次元 64・層 6（S/S/F/S/S/F）・注意の頭 4・窓つきの層 KV の頭 2・頭の次元 16・全体の層 KV の頭 1・頭の次元 32・窓 8・選んだ層の添字 2（full_attention）・埋め込みの倍率 8.0・softcap 30.0・係数 2.0
[ok] 升目の組み立てが台帳と一致（全 8 升目・長さ・主位置とそのトークン・読み取りの位置・ids_sha16・族・読み取りの集合）  | N1|O-Ncold 431/430/437・N1|Onull 422/421/428・S1|O-Ncold 482/481/488・S1|Onull 473/472/479・S4|O-Ncold 495/494/501・S4|Onull 486/485/492・SK|O-Ncold 496/495/502・SK|Onull 487/486/493
[ok] 台帳と違えば止まる（S1|O-Ncold の prompt_len を +1 ずらした写し）
[ok] 台帳と違えば止まる（S1|O-Ncold の main_position を +1 ずらした写し）
[ok] 台帳と違えば止まる（S1|O-Ncold の readout_position を -1 ずらした写し）
[ok] 台帳と違えば止まる（S1|O-Ncold の ids_sha16 を書き換えた写し）
[ok] 主の書き出しが正本と違えば止まる（最後のトークンを落とした写し）
[ok] [float32] N1|O-Ncold use_cache=False: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 438, 64)・型 torch.float32
[参考] [float32] N1|O-Ncold use_cache=False: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 438, 438)・cache 作らない（判定に入れない）
[ok] [float32] N1|O-Ncold: 読み取りの集合の出口の値（float32・softcap 後）が模型の出口の値と一致（書き手の許容 1e-4）  | 差の絶対値の最大 1.12e-07
[ok] [float32] N1|O-Ncold: 歯——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 10 倍を超える  | 取り違え 0.347・正しい 1.12e-07
[ok] [float32] N1|O-Ncold: hidden_states は層の数＋1 で、[-1] は正規化の後（最終の正規化の入力と違う）
[ok] [float32] N1|O-Ncold: 手回しの層 2 の出力（書き換えの前）が hidden_states[3] と一致（ビット単位）
[ok] [float32] N1|O-Ncold: 歯——1＋g で正規化した読み取りの差が、正しい読み取りの差の 10 倍を超える  | 1＋g 0.518・正しい 1.12e-07
[参考] [float32] N1|O-Ncold: softcap を抜いた読み取りと模型の出口の値の差の最大 0.000616（正しい 1.12e-07・判定に入れない）
[ok] [float32] N1|O-Ncold 既定（設定の use_cache）: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 438, 64)・型 torch.float32
[参考] [float32] N1|O-Ncold 既定（設定の use_cache）: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 438, 438)・cache 作る（判定に入れない）
[ok] [float32] S1|Onull use_cache=False: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 480, 64)・型 torch.float32
[参考] [float32] S1|Onull use_cache=False: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 480, 480)・cache 作らない（判定に入れない）
[ok] [float32] S1|Onull: 読み取りの集合の出口の値（float32・softcap 後）が模型の出口の値と一致（書き手の許容 1e-4）  | 差の絶対値の最大 0
[ok] [float32] S1|Onull: 歯——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 10 倍を超える  | 取り違え 0.364・正しい 0
[ok] [float32] S1|Onull: hidden_states は層の数＋1 で、[-1] は正規化の後（最終の正規化の入力と違う）
[ok] [float32] S1|Onull: 手回しの層 2 の出力（書き換えの前）が hidden_states[3] と一致（ビット単位）
[ok] [float32] S1|Onull: 歯——1＋g で正規化した読み取りの差が、正しい読み取りの差の 10 倍を超える  | 1＋g 0.441・正しい 0
[参考] [float32] S1|Onull: softcap を抜いた読み取りと模型の出口の値の差の最大 0.00112（正しい 0・判定に入れない）
[ok] [float32] S1|Onull 既定（設定の use_cache）: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 480, 64)・型 torch.float32
[参考] [float32] S1|Onull 既定（設定の use_cache）: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 480, 480)・cache 作る（判定に入れない）
[参考] [float32] use_cache=False と既定の手回しの道の最終の正規化の入力がビット単位で同じ: True（判定に入れない）
[ok] [bfloat16] N1|O-Ncold use_cache=False: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 438, 64)・型 torch.bfloat16
[参考] [bfloat16] N1|O-Ncold use_cache=False: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 438, 438)・cache 作らない（判定に入れない）
[参考] [bfloat16] N1|O-Ncold: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差の最大 0.00489（判定に入れない）
[ok] [bfloat16] N1|O-Ncold: 歯——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 10 倍を超える  | 取り違え 0.339・正しい 0.00489
[ok] [bfloat16] N1|O-Ncold: hidden_states は層の数＋1 で、[-1] は正規化の後（最終の正規化の入力と違う）
[ok] [bfloat16] N1|O-Ncold: 手回しの層 2 の出力（書き換えの前）が hidden_states[3] と一致（ビット単位）
[ok] [bfloat16] N1|O-Ncold: 歯——1＋g で正規化した読み取りの差が、正しい読み取りの差の 10 倍を超える  | 1＋g 0.516・正しい 0.00489
[参考] [bfloat16] N1|O-Ncold: softcap を抜いた読み取りと模型の出口の値の差の最大 0.00496（正しい 0.00489・判定に入れない）
[ok] [bfloat16] N1|O-Ncold 既定（設定の use_cache）: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 438, 64)・型 torch.bfloat16
[参考] [bfloat16] N1|O-Ncold 既定（設定の use_cache）: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 438, 438)・cache 作る（判定に入れない）
[ok] [bfloat16] S1|Onull use_cache=False: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 480, 64)・型 torch.bfloat16
[参考] [bfloat16] S1|Onull use_cache=False: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 480, 480)・cache 作らない（判定に入れない）
[参考] [bfloat16] S1|Onull: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差の最大 0.00575（判定に入れない）
[ok] [bfloat16] S1|Onull: 歯——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 10 倍を超える  | 取り違え 0.357・正しい 0.00575
[ok] [bfloat16] S1|Onull: hidden_states は層の数＋1 で、[-1] は正規化の後（最終の正規化の入力と違う）
[ok] [bfloat16] S1|Onull: 手回しの層 2 の出力（書き換えの前）が hidden_states[3] と一致（ビット単位）
[ok] [bfloat16] S1|Onull: 歯——1＋g で正規化した読み取りの差が、正しい読み取りの差の 10 倍を超える  | 1＋g 0.41・正しい 0.00575
[参考] [bfloat16] S1|Onull: softcap を抜いた読み取りと模型の出口の値の差の最大 0.00573（正しい 0.00575・判定に入れない）
[ok] [bfloat16] S1|Onull 既定（設定の use_cache）: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 480, 64)・型 torch.bfloat16
[参考] [bfloat16] S1|Onull 既定（設定の use_cache）: 手回しの道の mask は full_attention=None・sliding_attention=明示 torch.bool (1, 1, 480, 480)・cache 作る（判定に入れない）
[参考] [bfloat16] use_cache=False と既定の手回しの道の最終の正規化の入力がビット単位で同じ: True（判定に入れない）
[参考] 残差のノルム（層 2 の出力の主位置・八升目の平均・float32）21.32 → 合成の方向のノルム 10.66（× 0.5）
[ok] [float32] N1|O-Ncold 符号 -1: 層 2 より前の層の出力は無操作と同じ（ビット単位）
[ok] [float32] N1|O-Ncold 符号 -1: 層 2 の出力（書き換えの前）は無操作と同じ（ビット単位）
[ok] [float32] N1|O-Ncold 符号 -1: 書き換えは主位置（430）より前の位置を変えない（層 2 の出力・ビット単位）
[ok] [float32] N1|O-Ncold 符号 -1: 主位置から列の最後まで（8 位置）に同じ量を足した（ビット単位）
[ok] [float32] N1|O-Ncold 符号 -1: 足した量が「float32 を経て層の出力の型に直した v」× sign×coef（型 torch.float32・ビット単位）
[ok] [float32] N1|O-Ncold 符号 -1: 層の出力の差の向きと大きさが sign×coef×v（型の丸めの内）  | 余弦の最小 1.000000・ノルムの相対の差の最大 1.12e-08
[ok] [float32] N1|O-Ncold 符号 -1: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う
[ok] [float32] S1|Onull 符号 +1: 層 2 より前の層の出力は無操作と同じ（ビット単位）
[ok] [float32] S1|Onull 符号 +1: 層 2 の出力（書き換えの前）は無操作と同じ（ビット単位）
[ok] [float32] S1|Onull 符号 +1: 書き換えは主位置（472）より前の位置を変えない（層 2 の出力・ビット単位）
[ok] [float32] S1|Onull 符号 +1: 主位置から列の最後まで（8 位置）に同じ量を足した（ビット単位）
[ok] [float32] S1|Onull 符号 +1: 足した量が「float32 を経て層の出力の型に直した v」× sign×coef（型 torch.float32・ビット単位）
[ok] [float32] S1|Onull 符号 +1: 層の出力の差の向きと大きさが sign×coef×v（型の丸めの内）  | 余弦の最小 1.000000・ノルムの相対の差の最大 6.76e-09
[ok] [float32] S1|Onull 符号 +1: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う
[ok] [bfloat16] N1|O-Ncold 符号 -1: 層 2 より前の層の出力は無操作と同じ（ビット単位）
[ok] [bfloat16] N1|O-Ncold 符号 -1: 層 2 の出力（書き換えの前）は無操作と同じ（ビット単位）
[ok] [bfloat16] N1|O-Ncold 符号 -1: 書き換えは主位置（430）より前の位置を変えない（層 2 の出力・ビット単位）
[ok] [bfloat16] N1|O-Ncold 符号 -1: 主位置から列の最後まで（8 位置）に同じ量を足した（ビット単位）
[ok] [bfloat16] N1|O-Ncold 符号 -1: 足した量が「float32 を経て層の出力の型に直した v」× sign×coef（型 torch.bfloat16・ビット単位）
[ok] [bfloat16] N1|O-Ncold 符号 -1: 層の出力の差の向きと大きさが sign×coef×v（型の丸めの内）  | 余弦の最小 0.999995・ノルムの相対の差の最大 0.000708
[ok] [bfloat16] N1|O-Ncold 符号 -1: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う
[ok] [bfloat16] S1|Onull 符号 +1: 層 2 より前の層の出力は無操作と同じ（ビット単位）
[ok] [bfloat16] S1|Onull 符号 +1: 層 2 の出力（書き換えの前）は無操作と同じ（ビット単位）
[ok] [bfloat16] S1|Onull 符号 +1: 書き換えは主位置（472）より前の位置を変えない（層 2 の出力・ビット単位）
[ok] [bfloat16] S1|Onull 符号 +1: 主位置から列の最後まで（8 位置）に同じ量を足した（ビット単位）
[ok] [bfloat16] S1|Onull 符号 +1: 足した量が「float32 を経て層の出力の型に直した v」× sign×coef（型 torch.bfloat16・ビット単位）
[ok] [bfloat16] S1|Onull 符号 +1: 層の出力の差の向きと大きさが sign×coef×v（型の丸めの内）  | 余弦の最小 0.999994・ノルムの相対の差の最大 0.000778
[ok] [bfloat16] S1|Onull 符号 +1: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う
[参考] float32 を経た bf16 と float64 から直に直した bf16 が同じ合成の方向: 42/42（判定に入れない）
[ok] [float32] 零のベクトルの効き目が全て零（2 行・効き目 118 個・両方の符号）
[ok] [float32] 同じ呼び出しを二度走らせて同じ値（ビット単位）  | 一度 26.5 秒
[ok] [float32] 出力の形 {行の名: {noop_lo, effects: {方向の名|符号: 効き目}}}（行と方向の組は recompute_set のとおり・符号の書き方 %+d）  | 行 ['sub:N1:O-Ncold-v~O-Ncold-vrand', 'add:S1:Onull+v~Onull+vrand']・効き目の数 [59, 59]・鍵の例 ['static|-1', 'iso:0|-1']
[ok] [float32] 外した升目の行は計算しない（外していない升目の static の行だけ）
[ok] [float32] 歯——static の効き目は零でない  | -1.793・4.43
[ok] 外した升目の鍵が台帳に無ければ止まる
[ok] pilot['decision']['dropped'] が無ければ止まる
[ok] names["real"] に real: で始まらない名があれば止まる
[ok] dirs に要る方向が無ければ止まる
[ok] 方向が float64 でなければ止まる
[ok] 方向の形が次元と合わなければ止まる
[ok] 係数が正でなければ止まる
[ok] 模型に forward の hook が掛かっていれば止まる（選んだ層に何もしない hook を掛けた写し）
[ok] transformers の記録用の hook（output_hidden_states の後に居残る 12 本）は数えず、値も変わらない（ビット単位）
[ok] 呼び出しの間に forward の hook を掛けようとしない（nn.Module の register_forward_hook と register_forward_pre_hook を落ちる形に差し替えて走らせ、値も同じ）
[参考] [float32] use_cache=None（DynamicCache を作る形）と既定の形の差の最大: 効き目 0・無操作 0（判定に入れない）
[ok] [bfloat16] 零のベクトルの効き目が全て零（2 行・効き目 118 個・両方の符号）
[ok] [bfloat16] 同じ呼び出しを二度走らせて同じ値（ビット単位）  | 一度 97.7 秒
[ok] [bfloat16] 出力の形 {行の名: {noop_lo, effects: {方向の名|符号: 効き目}}}（行と方向の組は recompute_set のとおり・符号の書き方 %+d）  | 行 ['sub:N1:O-Ncold-v~O-Ncold-vrand', 'add:S1:Onull+v~Onull+vrand']・効き目の数 [59, 59]・鍵の例 ['static|-1', 'iso:0|-1']
[ok] [bfloat16] 外した升目の行は計算しない（外していない升目の static の行だけ）
[ok] [bfloat16] 歯——static の効き目は零でない  | -1.845・4.416
[ok] [float32] 層ごとの入力（8）と layer_scalar（0.719・0.918…）のある変種でも、手回しの道の最終の正規化の入力が模型の forward と一致（ビット単位）
[ok] [bfloat16] 層ごとの入力（8）と layer_scalar（0.719・0.918…）のある変種でも、手回しの道の最終の正規化の入力が模型の forward と一致（ビット単位）
selftest: 82/82 ok
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
```

### 4.2 再抽出の道

- 走らせた器の SHA-256（走らせる前に記録）: AEF215AA0F577E45885F777C7180246C21F97CF9F36D4916F9FC1A5D97ED6096（今の器と一致）
- 走りの時刻（UTC）: 2026-09-30 05:29:41 〜 2026-09-30 05:31:07・exit=0
- 標準出力の SHA-256（改行を LF にそろえたもの＝下の逐語の写しに末尾の改行を一つ足したバイト列）: B275265AEBDA8221C5E00008EE041395B34EFB868B2EC58535ACC11CBF844130
- 標準エラー: 空

```
bprime_reextract v1 --selftest  torch 2.9.1+cpu・transformers 5.16.1・numpy 2.4.6・注意の実装 sdpa・作ったままの型 bfloat16
乱数の小さな模型: 次元 64・層 6・選んだ層の添字 2（hidden_states[3]）・許容 rel_tol 1e-05・cos_min 0.99999
[ok] 正本 directions.defs の文から読んだ腕の差が指示の対応と一致  | static＝O − Osec・loaded＝O-Ncold − Osec-Ncold・Nk＝Nk − N・td＝Onull − N
[ok] 正本の定義の文が指示の対応と違えば止まる（td を書き換えた写し）
[ok] 抽出の文脈が台帳と一致（16 文脈・長さ・主位置とそのトークン・ids_sha16）  | N1|O 420・S1|O 471・N1|Osec 419・S1|Osec 470・N1|Onull 422・S1|Onull 473・N1|Nk 257・S1|Nk 308・N1|N 247・S1|N 298・N1|O-Ncold 431・S1|O-Ncold 482・N1|Osec-Ncold 430・S1|Osec-Ncold 481・N1|Onull-Ncold 433・S1|Onull-Ncold 484
[ok] 台帳と違えば止まる（S1|Osec の ids_sha16 を書き換えた写し）
[ok] 台帳と違えば止まる（N1|Nk の prompt_len を +1 ずらした写し）
[ok] [float32] 取った値は有限・float64・形 (64,)・文脈の名がそろう（16 文脈）  | 1.5 秒
[参考] [float32] 記録用の hook（transformers の output_capturing）: 前 0 本 → 後 12 本・それ以外の hook 0 本（判定に入れない）
[ok] [float32] 同じ呼び出しを二度走らせて同じ値（ビット単位・二度目は記録用の hook が居残った模型）
[ok] [float32] hidden_states[3] の主位置が、手で層を回した道の層 2 の出力の主位置と一致（ビット単位・3 文脈）
[ok] [float32] 最後の層（添字 5）は取らずに止まる（hidden_states[-1] は最終の正規化の後）
[ok] [float32] 模型に forward の hook が掛かっていれば止まる（選んだ層に何もしない hook を掛けた写し）
[ok] [float32] reextract_all: 文脈 16・名前のある方向の余弦が dirs に同じ方向を渡したとき一（1−1e-12 以上）  | static 1.000000000000000・loaded 1.000000000000000・Nk 1.000000000000000・td 1.000000000000000
[ok] [float32] reextract_all: vhat_norm＝‖O の平均 − Osec の平均‖・h_norm_by_context＝‖h‖（ビット単位）
[ok] [float32] 歯——static を反転した dirs の余弦は −1、loaded に Nk を渡した dirs の余弦は cos_min（0.99999）に届かない  | static -1.000000・loaded -0.143623
[ok] [float32] dirs に名前のある方向が無ければ止まる
[ok] [bfloat16] 取った値は有限・float64・形 (64,)・文脈の名がそろう（16 文脈）  | 7.0 秒
[参考] [bfloat16] 記録用の hook（transformers の output_capturing）: 前 0 本 → 後 12 本・それ以外の hook 0 本（判定に入れない）
[ok] [bfloat16] 同じ呼び出しを二度走らせて同じ値（ビット単位・二度目は記録用の hook が居残った模型）
[ok] [bfloat16] hidden_states[3] の主位置が、手で層を回した道の層 2 の出力の主位置と一致（ビット単位・3 文脈）
[ok] [bfloat16] 最後の層（添字 5）は取らずに止まる（hidden_states[-1] は最終の正規化の後）
[ok] [bfloat16] 模型に forward の hook が掛かっていれば止まる（選んだ層に何もしない hook を掛けた写し）
[ok] [bfloat16] reextract_all: 文脈 16・名前のある方向の余弦が dirs に同じ方向を渡したとき一（1−1e-12 以上）  | static 1.000000000000000・loaded 1.000000000000000・Nk 1.000000000000000・td 1.000000000000000
[ok] [bfloat16] reextract_all: vhat_norm＝‖O の平均 − Osec の平均‖・h_norm_by_context＝‖h‖（ビット単位）
[ok] [bfloat16] 歯——static を反転した dirs の余弦は −1、loaded に Nk を渡した dirs の余弦は cos_min（0.99999）に届かない  | static -1.000000・loaded -0.107978
[ok] [bfloat16] dirs に名前のある方向が無ければ止まる
selftest: 23/23 ok
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
```

## 5. 突き合わせ（`--dry`）の結果——器の出力の逐語

### 5.1 書き換えの道

- 走らせた器の SHA-256（走らせる前に記録）: DF0833637E5755D86FDF7B7B7A64F00284E0B5678C034C2A6103E1B6CBB9611F（今の器と一致）
- 走りの時刻（UTC）: 2026-09-30 05:32:07 〜 2026-09-30 05:40:22・exit=0
- 標準出力の SHA-256（改行を LF にそろえたもの＝下の逐語の写しに末尾の改行を一つ足したバイト列）: AFA7BF17CCAC43BCCFEEFF7BEF63B877288F5671E04C468A616AFC420F443DA9
- 標準エラー: 空
- 突き合わせの相手 `Bprime/tools/bprime_run.py` の SHA16 536C981D3698C2C7（組み立ての時に計算・中は表示していない）

```
bprime_recompute_rewrite v1 --dry  torch 2.9.1+cpu・transformers 5.16.1・numpy 2.4.6・注意の実装 sdpa
乱数の小さな模型: 次元 64・層 6・選んだ層の添字 2・窓 8・係数 2.0・合成の方向のノルム 10.66（残差のノルム 21.32 × 0.5）・一段目の許容 independent_recompute.tol_stage1 = 0.001
行 sub:N1:O-Ncold-v~O-Ncold-vrand・升目 N1|O-Ncold（nuclear）・符号 -1・方向と符号 59 組（static 1・等方 10・比べる相手の実在の差 48＝24 対 × 両方の向き）＋無操作
行 add:S1:Onull+v~Onull+vrand・升目 S1|Onull（survival）・符号 +1・方向と符号 59 組（static 1・等方 10・比べる相手の実在の差 48＝24 対 × 両方の向き）＋無操作
[float32] 残差の書き換えの道 19.9 秒（順伝播 120 回）・フックの道 25.7 秒
[float32] 効き目の数 118・効き目の絶対値の最大（残差の書き換えの道）4.43
[float32] 差の絶対値の最大: 効き目 3.61e-07・無操作の量 7.82e-08
[float32] dry: 一段目の許容（0.001）の内（差の最大 3.61e-07）
[参考] [float32] フックの道の後に走らせ直した残差の書き換えの道が一度目と同じ（ビット単位）: True・居残る hook（記録用を除く）0 本
[参考] [float32] use_cache=None（DynamicCache を作る形）の残差の書き換えの道——既定の形との差の最大 効き目 0・無操作 0／フックの道との差の最大 効き目 3.61e-07・無操作 7.82e-08
[歯] [float32] M0 誤らせない（対照）: フックの道との差の最大 1.42e-07（無操作 2 個・効き目 8 個）→ 許容の内（対照として期待どおり）（許容 0.001）
[歯] [float32] M1 帯の起点を主位置の一つ後にする: フックの道との差の最大 0.429（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [float32] M2 書き換える層を一つ後にする: フックの道との差の最大 0.804（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [float32] M3 符号を反転する: フックの道との差の最大 7.17（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [float32] M4 係数を二度掛ける（sign×coef×coef×v）: フックの道との差の最大 1.67（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [float32] M5 読み取りで正規化を二度当てる: フックの道との差の最大 0.358（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [float32] M6 読み取りで softcap を抜く: フックの道との差の最大 0.00482（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [float32] M7 加減を層の出力の型に直さず float32 のまま足す: フックの道との差の最大 1.42e-07（無操作 2 個・効き目 8 個）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）
[歯] [float32] M8 最終の正規化の重みを 1＋g にする: フックの道との差の最大 1.7（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [float32] 変種の計算 10.7 秒（参考・判定に入れない）
[bfloat16] 残差の書き換えの道 68.8 秒（順伝播 120 回）・フックの道 79.3 秒
[bfloat16] 効き目の数 118・効き目の絶対値の最大（残差の書き換えの道）4.416
[bfloat16] 差の絶対値の最大: 効き目 5.36e-07・無操作の量 2.09e-07
[bfloat16] dry: 一段目の許容（0.001）の内（差の最大 5.36e-07）
[参考] [bfloat16] フックの道の後に走らせ直した残差の書き換えの道が一度目と同じ（ビット単位）: True・居残る hook（記録用を除く）0 本
[参考] [bfloat16] use_cache=None（DynamicCache を作る形）の残差の書き換えの道——既定の形との差の最大 効き目 0・無操作 0／フックの道との差の最大 効き目 5.36e-07・無操作 2.09e-07
[歯] [bfloat16] M0 誤らせない（対照）: フックの道との差の最大 2.95e-07（無操作 2 個・効き目 8 個）→ 許容の内（対照として期待どおり）（許容 0.001）
[歯] [bfloat16] M1 帯の起点を主位置の一つ後にする: フックの道との差の最大 0.374（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] M2 書き換える層を一つ後にする: フックの道との差の最大 0.847（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] M3 符号を反転する: フックの道との差の最大 7.28（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] M4 係数を二度掛ける（sign×coef×coef×v）: フックの道との差の最大 1.63（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] M5 読み取りで正規化を二度当てる: フックの道との差の最大 0.361（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] M6 読み取りで softcap を抜く: フックの道との差の最大 0.00496（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] M7 加減を層の出力の型に直さず float32 のまま足す: フックの道との差の最大 0.0374（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] M8 最終の正規化の重みを 1＋g にする: フックの道との差の最大 1.69（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた（許容 0.001）
[歯] [bfloat16] 変種の計算 65.0 秒（参考・判定に入れない）
（正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない）
dry: 二つの型とも一段目の許容の内
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
```

- 比べた組は、器の出力の「行 …」の二行のとおり。判定は、正本 `independent_recompute.tol_stage1` を、全ての効き目と無操作の量の差の絶対値の最大に当てた（器が印字した `dry:` の行）。参考の行と歯の変種は判定に入れていない。
- 比の分母の注（教訓 4）: 効き目の差の最大は、効き目（それぞれ二つの量の差）の上の最大で、無操作の量の差の最大は量そのものの上の最大。この二つを互いに「何倍」と較正された比として引かない。

### 5.2 再抽出の道

- 走らせた器の SHA-256（走らせる前に記録）: AEF215AA0F577E45885F777C7180246C21F97CF9F36D4916F9FC1A5D97ED6096（今の器と一致）
- 走りの時刻（UTC）: 2026-09-30 05:31:07 〜 2026-09-30 05:32:07・exit=0
- 標準出力の SHA-256（改行を LF にそろえたもの＝下の逐語の写しに末尾の改行を一つ足したバイト列）: 209C14B885F985011CBFD0502DEDAAF4FB033033C59608863876763DC71AB1F7
- 標準エラー: 空
- 突き合わせの相手 `Bprime/tools/bprime_directions.py` の SHA16 8D999D06A7773343（組み立ての時に計算・中は表示していない）

```
bprime_reextract v1 --dry  torch 2.9.1+cpu・transformers 5.16.1・numpy 2.4.6・注意の実装 sdpa
乱数の小さな模型: 次元 64・層 6・選んだ層の添字 2・許容 independent_recompute.reextract の rel_tol = 1e-05・cos_min = 0.99999
比べる文脈（四つ）: N1|O（420 トークン）・S1|Osec（470 トークン）・N1|Nk（257 トークン）・S1|O-Ncold（482 トークン）
[float32] コーディネータの抽出の器 0.5 秒・この道 0.7 秒・返り値の型 OrderedDict／OrderedDict
[float32] ‖h‖ の相対の差の最大 0・余弦の最小 1.000000000000・四つともビット単位で同じ: True
[参考] [float32] コーディネータの器が返したノルムとこの道の ‖h‖ の相対の差の最大 0（判定に入れない）
[参考] [float32] 記録用の hook が居残った模型での二度目のコーディネータの抽出の器が一度目と同じ（ビット単位）: True
[float32] dry: 再抽出の許容（rel_tol 1e-05・cos_min 0.99999）の内
[参考] [float32] 十六文脈: reextract_all の名前のある方向の余弦の最小 1.000000000000・‖v̂‖ の相対の差 0・‖h‖ の相対の差の最大 0（dirs はコーディネータの器の値からこの器の式で作った・判定に入れない）
[bfloat16] コーディネータの抽出の器 1.2 秒・この道 1.8 秒・返り値の型 OrderedDict／OrderedDict
[bfloat16] ‖h‖ の相対の差の最大 0・余弦の最小 1.000000000000・四つともビット単位で同じ: True
[参考] [bfloat16] コーディネータの器が返したノルムとこの道の ‖h‖ の相対の差の最大 0（判定に入れない）
[参考] [bfloat16] 記録用の hook が居残った模型での二度目のコーディネータの抽出の器が一度目と同じ（ビット単位）: True
[bfloat16] dry: 再抽出の許容（rel_tol 1e-05・cos_min 0.99999）の内
[参考] [bfloat16] 十六文脈: reextract_all の名前のある方向の余弦の最小 1.000000000000・‖v̂‖ の相対の差 0・‖h‖ の相対の差の最大 0（dirs はコーディネータの器の値からこの器の式で作った・判定に入れない）
dry: 二つの型とも再抽出の許容の内
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
```

- 判定は、四つの文脈の ‖h‖ の相対の差の最大を正本 `independent_recompute.reextract.rel_tol` に、余弦の最小を `cos_min` に当てた（器が印字した `dry:` の行）。十六文脈の参考の行は判定に入れていない（dirs はコーディネータの器の値からこの器の式で作ったので、名前のある方向の作り方そのものは突き合わせていない）。

### 5.3 事前登録と結果の突き合わせ

- 事前登録の文の逐語（SHA-256 4344FA06C48E09B611714E83D833FF05DB6B274CF193E46535311BC2D07D248B）:

```
事前登録——B′ の独立の再計算の二つの道の突き合わせ（--dry）と、書き換えの道の歯の変種
書いた時刻: 2026-09-30 04:51:59 UTC（13:51:59 手元の時刻）
書いた時の状態: 二つの器の本体と歯の変種の器は書いた後・どちらの器も一度も走らせていない（--selftest も --dry もまだ）。
  乱数の小さな模型で見たのは構造だけ（層の種類・頭の次元・hook の数）で、順伝播の値・効き目・出口の値は一つも見ていない。
  歯の変種の器を書いたのはこの事前登録より前（層三の書き手は変種の器を書く前に登録した——ここはそれより弱い。予想は値を見る前）。
目的: 一段目の突き合わせ（independent_recompute.tol_stage1 = 0.001）と再抽出の突き合わせ（rel_tol 1e-05・cos_min 0.99999）の結果の予想を、
  結果を見る前に固める。歯の変種は、一段目の許容での突き合わせがこの小さな模型で実装の誤りを捕まえる弁別力を持つかを測る
  （検査を置くことと検査が働くことは同じでない）。--dry の判定の行は変えない。変種の結果は参考で、判定に入れない。

一、書き換えの道の一段目（残差の書き換えの道 対 コーディネータのフックの道・static の行二つ・無操作と 59 の方向と符号）
  bfloat16 の模型: 許容の内（高め 0.8）。差の最大は 1e-4 以下（中 0.6）。同じ算術なら 0 に近い。
    外れうる理由: フックの道の読み取りの式（rsqrt と pow・行を先に切るか全語彙か）・ベクトルの型の直し方（float32 を経るか）・
    mask や cache の組み方がこちらと違う。どれも CPU の上では差が 1e-4 を超えにくいと見る。
  float32 の模型: 許容の内（中 0.65）。フックの道の器が float32 の模型を受けない（止まる）ことがありうる（その場合は比べられなかったと記す）。
二、再抽出（reextract 対 コーディネータの BD.activations・四つの文脈）
  float32・bfloat16 とも許容の内（高 0.9）。同じ層の出力の同じ位置を取るので、ビット単位で同じか float64 の丸めの差だけと見る。

三、歯の変種（書き換えの道をわざと誤らせ、フックの道の値との差の最大〔行ごとに無操作と static・iso:0・最初の比べる相手の両方の向き〕が
    許容 0.001 を超えれば「捕まえた」）。この小さな模型では合成の方向のノルムを残差のノルムの 0.5 倍・係数 2.0 にするので、
    足す量は残差と同じ桁（相対 1 ほど）と見込む（層三の小さな模型の 100 倍の領域とは違う）。
  M0 誤らせない（対照）: 許容の内（高 0.95）
  M1 帯の起点を主位置の一つ後にする: 捕まえる（中 0.75）——読み取りの位置への加減は残るが、主位置の変化が窓（8）の内の注意で読み取りの位置に届く
  M2 書き換える層を一つ後にする: 捕まえる（高 0.95）
  M3 符号を反転する: 捕まえる（高 0.95）
  M4 係数を二度掛ける（sign×coef×coef×v）: 捕まえる（高 0.9）——足す量が残差と同じ桁なので正規化で打ち消されにくい
  M5 読み取りで正規化を二度当てる: 捕まえる（高 0.9）——最終の正規化の重みが [2, 3) なので二度目で大きさと向きが変わる
  M6 読み取りで softcap を抜く: 捕まえる（中 0.6）——出口の値は数の桁（cap 30 より小さい）なので softcap の効きは小さく、許容の前後の見込み
  M7 加減を層の出力の型に直さず float32 のまま足す: float32 の模型では捕まえない（確実 0.99・算術が同じ）／bfloat16 の模型では捕まえる（五分五分 0.5）
  M8 最終の正規化の重みを 1＋g にする: 捕まえる（高 0.9）
捕まえなかった変種があれば、それは一段目の突き合わせの（この小さな模型での）盲点として記録し、器の誤りとはしない。予想が外れても消さない。
```

- 時刻の順（組み立ての器がファイルの記録から写した・UTC）: 事前登録の文の最後の書き込み 2026-09-30 04:52:18 → 試しの走りの出力の最初の作成 2026-09-30 04:52:35（書き換えの道 --selftest（試し一））→ 本番の走りの最初の開始 2026-09-30 05:20:58
- **事前登録の文の誤りの訂正**（事前登録の文は変えず、ここに記す）: 文の「書いた時の状態」の一行目「二つの器の本体と歯の変種の器は書いた後」は誤り。事前登録を書いた時に書いてあったのは**書き換えの道の器（歯の変種を含む）だけ**で、再抽出の道の器はその後に書いた（ファイルの時刻: 事前登録の文の最後の書き込み 2026-09-30 04:52:18 → 再抽出の道の器のファイルの作成 2026-09-30 05:03:57・最後の書き込み 2026-09-30 05:03:57（UTC）。この作業の道具（Write・Edit）はファイルを書き直すたびに作成の時刻も新しくするので、ファイルの時刻が示すのは「再抽出の道の器の今のファイルは事前登録より後に書かれた」ことまで（書き換えの道の器のファイルの作成の時刻は、最後に直した時刻 2026-09-30 05:20:03 になっており、事前登録より前に書いてあったことはファイルの時刻では示せない——書き手の申告））。書き手が組み立ての前の読み直しで見つけた。予想そのもの（二の再抽出の予想を含む）は、どの器も走らせる前に書いたことに変わりはない。
- 注: 事前登録は、書き換えの道の器と歯の変種の器を書いた後、器を一度も走らせる前に書いた（層三の書き手は変種の器を書く前に登録した——ここはそれより弱い）。器を書く前でないことは上のとおり。走らせる前であることは、事前登録の文の書き込みの時刻が試しと本番の走りの出力の最初の作成より前であることで確かめられる範囲に限る（試しの走りは検分票の COI 記録の（五））。検分の手順書（kensho）は、二つの道の自己検査の試しの走りと再抽出の道の `--dry` の試しの走りの結果を見た後、書き換えの道の `--dry` の試しの走りの結果（頭の四行の後）を見る前に読んだ。
- 結果と予想（組み立ての器が事前登録の文と器の出力の行から機械で作った）:

| 項目 | 予想（事前登録の文の逐語） | 結果（器の出力から） | 予想どおりか |
|---|---|---|---|
| 一、書き換えの道 bfloat16 の模型 | bfloat16 の模型: 許容の内（高め 0.8）。差の最大は 1e-4 以下（中 0.6）。同じ算術なら 0 に近い。 | 許容の内（差の最大: 効き目 5.36e-07・無操作の量 2.09e-07） | はい／差の最大 1e-4 以下の予想: はい |
| 一、書き換えの道 float32 の模型 | float32 の模型: 許容の内（中 0.65）。フックの道の器が float32 の模型を受けない（止まる）ことがありうる（その場合は比べられなかったと記す）。 | 許容の内（差の最大: 効き目 3.61e-07・無操作の量 7.82e-08） | はい |
| 二、再抽出 | float32・bfloat16 とも許容の内（高 0.9）。同じ層の出力の同じ位置を取るので、ビット単位で同じか float64 の丸めの差だけと見る。 | float32 は許容の内・bfloat16 は許容の内 | はい |

| 型 | 変種 | 予想（事前登録の文の逐語） | 結果（器の出力） | 予想どおりか |
|---|---|---|---|---|
| float32 | M0 誤らせない（対照） | 許容の内（高 0.95） | 差の最大 1.42e-07（無操作 2 個・効き目 8 個）→ 許容の内（対照として期待どおり） | はい |
| float32 | M1 帯の起点を主位置の一つ後にする | 捕まえる（中 0.75）——読み取りの位置への加減は残るが、主位置の変化が窓（8）の内の注意で読み取りの位置に届く | 差の最大 0.429（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| float32 | M2 書き換える層を一つ後にする | 捕まえる（高 0.95） | 差の最大 0.804（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| float32 | M3 符号を反転する | 捕まえる（高 0.95） | 差の最大 7.17（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| float32 | M4 係数を二度掛ける（sign×coef×coef×v） | 捕まえる（高 0.9）——足す量が残差と同じ桁なので正規化で打ち消されにくい | 差の最大 1.67（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| float32 | M5 読み取りで正規化を二度当てる | 捕まえる（高 0.9）——最終の正規化の重みが [2, 3) なので二度目で大きさと向きが変わる | 差の最大 0.358（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| float32 | M6 読み取りで softcap を抜く | 捕まえる（中 0.6）——出口の値は数の桁（cap 30 より小さい）なので softcap の効きは小さく、許容の前後の見込み | 差の最大 0.00482（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| float32 | M7 加減を層の出力の型に直さず float32 のまま足す | float32 の模型では捕まえない（確実 0.99・算術が同じ） | 差の最大 1.42e-07（無操作 2 個・効き目 8 個）→ 許容の内＝捕まえなかった（この模型での盲点） | はい |
| float32 | M8 最終の正規化の重みを 1＋g にする | 捕まえる（高 0.9） | 差の最大 1.7（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| bfloat16 | M0 誤らせない（対照） | 許容の内（高 0.95） | 差の最大 2.95e-07（無操作 2 個・効き目 8 個）→ 許容の内（対照として期待どおり） | はい |
| bfloat16 | M1 帯の起点を主位置の一つ後にする | 捕まえる（中 0.75）——読み取りの位置への加減は残るが、主位置の変化が窓（8）の内の注意で読み取りの位置に届く | 差の最大 0.374（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| bfloat16 | M2 書き換える層を一つ後にする | 捕まえる（高 0.95） | 差の最大 0.847（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| bfloat16 | M3 符号を反転する | 捕まえる（高 0.95） | 差の最大 7.28（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| bfloat16 | M4 係数を二度掛ける（sign×coef×coef×v） | 捕まえる（高 0.9）——足す量が残差と同じ桁なので正規化で打ち消されにくい | 差の最大 1.63（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| bfloat16 | M5 読み取りで正規化を二度当てる | 捕まえる（高 0.9）——最終の正規化の重みが [2, 3) なので二度目で大きさと向きが変わる | 差の最大 0.361（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| bfloat16 | M6 読み取りで softcap を抜く | 捕まえる（中 0.6）——出口の値は数の桁（cap 30 より小さい）なので softcap の効きは小さく、許容の前後の見込み | 差の最大 0.00496（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |
| bfloat16 | M7 加減を層の出力の型に直さず float32 のまま足す | bfloat16 の模型では捕まえる（五分五分 0.5） | 差の最大 0.0374（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | —（五分五分の予想） |
| bfloat16 | M8 最終の正規化の重みを 1＋g にする | 捕まえる（高 0.9） | 差の最大 1.69（無操作 2 個・効き目 8 個）→ 許容の外＝捕まえた | はい |

- 読み（書き手の推測・確かめていない）: 捕まえなかった変種は float32 の M7（差の最大 1.42e-07）。float32 の模型では、二つの道の間で観測された差の最大 3.61e-07 は、捕まえた変種の差の最大の最小 0.00482 より小さい（比 7.5e-05・分母は捕まえた変種の差）。bfloat16 の模型では、二つの道の間で観測された差の最大 5.36e-07 は、捕まえた変種の差の最大の最小 0.00496 より小さい（比 1.1e-04・分母は捕まえた変種の差）。二つの道の片方だけに捕まえた型の誤りがあれば、観測された差はその変種の差の桁になったはず、と読める。二つの道が同じ誤りを共有していれば、この読みは何も言わない。判定の決まり（許容）を変える提案ではない。比は桁の目安としてだけ読み、較正された比として引かない（観測された差と変種の差は、同じ鍵の集合の上の最大ではない）。

## 6. 正本で決まっていなかった所（選んだ決め方と理由）

1. **cache の扱い**: 指示は「`use_cache=False` と同じ」、正本は「近道なし・バッチ一」。手回しの道の既定は cache を作らない形（層に `past_key_values=None`）にし、`use_cache=None` で模型の forward の既定（一回ごとに `DynamicCache` を作る形）も選べるようにした。この版では mask は cache より前に作られるので mask の形は変わらず、この CPU では二つの形の値はビット単位で同じだった（§4.1 と §5.1 の参考の行）。GPU では K/V の並び（cache を通すと cat で作る連続の写し・通さないと転置のままの view）が違い、SDPA の核の中の計算の順が変わりうる（§7 の三）。
2. **mask の組み方**: 模型の forward のどの呼び方（attention_mask を渡すか）に合わせるかは決まっていない。attention_mask なし（模型の既定の呼び方）にした。この版では、全て一の attention_mask を渡しても mask の形は同じになると読める（`_ignore_causal_mask_sdpa` の条件）。この読みは試していない。
3. **加減のベクトルの型の直し方**: 指示は「v を層の出力の型に直してから sign×coef を掛けて足す」（正本 `readout.primary.precision` は「順伝播と加減は bf16」）。`make_hook` は NumPy の float32 を経てから層の出力の型にする。これに合わせた。§4.1 の参考の行のとおり、合成の方向では float32 を経ても float64 から直に直しても bf16 のベクトルは同じだった。
4. **無操作の符号**: 零のベクトルを行の符号で足した（どちらの符号でも値は同じ）。
5. **読み取りの正規化の式**: 指示の式（rsqrt）にした。模型の `Gemma4RMSNorm` は `pow(·, −0.5)` で、float32 で最後の桁が違いうる。
6. **transformers の記録用の hook**: 数えない（§3.7）。これ以外の forward の hook があれば止める。
7. **`--dry` の行の選び方**: 指示は「static の行を二つ（減算の行と加算の行を一つずつ）」。`main_rows` の順で最初の減算の行と、族（選択の文字の数）を両方覆うために減算の行と違う族の最初の加算の行を選んだ（指示の公開の関数の例は S1 の二升目だった）。
8. **小さな模型の係数と「残差のノルム」**: 係数は 2.0（層三の係数と同じ値・書き手の選び）。残差のノルムは、主の八升目の層 L の出力の主位置のノルムの平均（float32 の模型）。
9. **最後の正規化の重みの一様乱数の引き方**: 種 1 の生成器。float32 の確かめは、作ったまま（bf16）の模型の写しを float32 に直した物で行った。
10. **方向のノルムの確かめ**: 正本 `directions.norm_rule` は読む範囲の外なので、dirs のノルムは照らさない（形・型・有限だけ）。
11. **係数の値**: 正本 `coefficient` は読む範囲の外なので、係数は正の有限の数であることだけを確かめる。
12. **本の模型の見分け**: 層の数と次元が正本 `inputs.model_facts` と同じなら本の模型として、bf16・`layers.index`・softcap・語彙の数・窓・全体の層の数を正本と照らす。そうでなければ小さな模型として、層の添字は割合の式だけで決める。
13. **再抽出の呼び方**: `use_cache=False`・`logits_to_keep=1`（出口の値は読まない）。最後の層は取らない。
14. **`reextract_all` の dirs の型**: 浮動小数の並びなら受け、float64 に上げて余弦を取る（書き換えの道の dirs は float64 でなければ止める）。
15. **再抽出の `--dry` の四つの文脈**: 二つの場面・四つの腕・長さの違う列（`N1|O`・`S1|Osec`・`N1|Nk`・`S1|O-Ncold`）。
16. **札の一致**: 正本の一致は「全ての効き目の差の絶対値が許容の内」で、かつ二つの道の値からそれぞれ出した「札が同じ」とき。札は集計の器の仕事なので、この器は値の差だけを見た。
17. **iso の名**: `recompute_set` が `iso:番号` の名を作るので、names['iso'] が iso:0〜 の番号の並びでなければ止める。

## 7. コーディネータに伝えたいこと

1. **呼び方**: `recompute_rewrite(model, tok, C, ledger, dirs, names, pilot, coef, use_cache=False)`（`use_cache` は任意の鍵の引数）・`reextract(model, contexts, layer_idx)`・`reextract_all(model, tok, C, ledger, dirs)`。模型は `Gemma4ForConditionalGeneration`・eval・（本の模型では）bf16・記録用のものを除く forward の hook なし・transformers は台帳の版。公開の置き場の凍結の器（`run_stageB_local`・`direction_B`・`bl3_core`）は、既定の路（手元）か環境変数 `OP4B_PUB_TOOLS` の路から import する（Colab ではどちらかを合わせてほしい）。二つの器は、`__main__` で走らせたときだけ `sys.dont_write_bytecode` を立てる（import されたときは呼び手の process の設定を変えない）。
2. **記録用の hook**: 再抽出の道は模型に記録用の hook を居残らせる（§3.8）。`--dry` では、居残った模型でコーディネータの抽出の器をもう一度呼び、同じ値が返った（§5.2 の参考の行）。フックの道の器が hook を数えるときに、この居残りを数えないことを確かめてほしい。
3. **本物の模型（GPU）での mask と cache の形**: この版では mask の形は use_cache に依らない。本物の模型では窓つきの層の mask も None（is_causal）になると読めるが、小さな模型の窓つきの層は明示の mask で、この形は小さな模型で試していない。書き換えの道の既定は cache を作らない形で、`use_cache=None` で cache を作る形にも合わせられる。フックの道が模型の forward をどちらの形で呼んでいるかに合わせることを勧める。この CPU では二つの形の値は同じで、フックの道との差も同じだった（§5.1 の参考の行）。
4. **layer_scalar と層ごとの入力**: 自己検査の変種で確かめた（§3.4）。コーディネータの合成の確かめの小さな模型が `layer_scalar` を 1 のままにしているなら、「layer_scalar の前か後か」の食い違いはその小さな模型では見えない。
5. **一段目の突き合わせの弁別力（歯の変種・§5.3）**: float32 の模型では対照（M0）は許容の内・わざと誤らせた 8 変種のうち 7 を捕まえ、捕まえなかったのは M7；bfloat16 の模型では対照（M0）は許容の内・わざと誤らせた 8 変種のうち 8 を捕まえ、捕まえなかった変種は無い。事前登録の予想の外れは無い。この小さな模型では足す量が残差と同じ桁（合成の方向のノルムが残差のノルムの 0.5 倍・係数 2.0）で、本物の模型の相対の加減とは領域が違いうるので、本物の模型での一段目の感度はこの結果からは言えない。
6. **読み取りの rsqrt と pow の違い**: 一段目の差の最大（§5.1）は許容より数桁小さかった。フックの道の読み取りの式の中は見ていないので、差がどこから来たかは確かめていない。
7. **費用**: 一回の順伝播は模型の全ての層を列の全体に流し（近道なし）、出口の値は読み取りの集合の行だけ作る。CPU の bf16 の小さな模型の時間は §4.1・§5.1 の秒の行のとおり（CPU の混み具合で揺れる）。本物の模型の GPU の時間は、この記録からは言えない。
8. **値の印字**: `recompute_rewrite`・`reextract`・`reextract_all` は値を印字しない。本の計算で差の最大を開かないのは、呼び手の器の決まり（正本 `independent_recompute.print`）。
9. **系統外の目**: 二つの道はどちらも Claude 系が、コーディネータの書いた同じ指示から書いた。本物の模型での一段目の前など重要な確定の前に、系統外の検分を登録者に提案することを勧める（採るかは登録者の判断）。
10. **同じ時刻の作業**: この作業の間、コーディネータの作業と思われるファイルの追加と変更が `Bprime/tools/` にあった（§8 の差の一覧）。この器は、ファイルを一つも書かない。

## 8. 既にあるファイルを変えていないことの機械の確かめ

- 二つの置き場（公開の置き場の全体〔`.git` を除く〕と `Bprime/` の全体）の全ファイルの路・大きさ・更新時刻の控えを、作業の頭（器を書く前）・本番の走りの直前と直後・組み立ての直前に取り、組み立ての器が比べた（出力の逐語）。
- 作業の頭 → 組み立ての前（置き場ごとの数: 公開の置き場（PUB:） 0 件・`__pycache__` の中 0 件・`Bprime/pylib` 0 件・`Bprime/hf` 0 件・`Bprime/design` 0 件・`Bprime/tools/independent` 3 件・`Bprime/tools` のほか 24 件・`Bprime/` のほか 4 件）:

```
作業の頭（器を書く前）→ 組み立ての前: 14056 件（控えの時刻 2026-09-30 04:45:06 UTC）→ 14080 件（2026-09-30 05:41:20 UTC）
増えた 24 件
  BPRIME:records/Bprime/MANIFEST-gemma-4-31B-it.json
  BPRIME:reviews/impl/probe/probe_env_Bprime.py
  BPRIME:rulings-D271.md
  BPRIME:rulings_D271.py
  BPRIME:tools/bprime_publish_map.py
  BPRIME:tools/close_behavior_Bprime.py
  BPRIME:tools/dry_run_Bprime.py
  BPRIME:tools/freeze_Bprime.py
  BPRIME:tools/independent/bprime_recompute_rewrite.py
  BPRIME:tools/independent/bprime_reextract.py
  BPRIME:tools/independent/dry-preregistration-Bprime.txt
  BPRIME:tools/make_frozen_Bprime.py
  BPRIME:tools/make_manifest_Bprime.py
  BPRIME:tools/prev/analyze_Bprime-v0.py
  BPRIME:tools/prev/boot_bprime-v0.py
  BPRIME:tools/prev/bprime_publish_map-v0.py
  BPRIME:tools/prev/build_report_Bprime-v0.py
  BPRIME:tools/prev/dry_bprime-v1.py
  BPRIME:tools/prev/dry_bprime_behavior-v0.py
  BPRIME:tools/prev/freeze_Bprime-v0.py
  BPRIME:tools/prev/publish_Bprime-v0.py
  BPRIME:tools/publish_Bprime.py
  BPRIME:tools/send_external_Bprime.py
  BPRIME:tools/sweep_Bprime.py
消えた 0 件
変わった 7 件
  BPRIME:tools/analyze_Bprime.py
  BPRIME:tools/build_report_Bprime.py
  BPRIME:tools/colab/boot_bprime.py
  BPRIME:tools/dry_bprime.py
  BPRIME:tools/dry_bprime_behavior.py
  BPRIME:tools/make_contrasts_Bprime.py
  BPRIME:tools/tools-log-Bprime.md
```

- 本番の走りの前 → 後（置き場ごとの数: 公開の置き場（PUB:） 0 件・`__pycache__` の中 0 件・`Bprime/pylib` 0 件・`Bprime/hf` 0 件・`Bprime/design` 0 件・`Bprime/tools/independent` 0 件・`Bprime/tools` のほか 15 件・`Bprime/` のほか 4 件）:

```
本番の走りの前 → 後: 14069 件（控えの時刻 2026-09-30 05:20:48 UTC）→ 14080 件（2026-09-30 05:41:12 UTC）
増えた 11 件
  BPRIME:records/Bprime/MANIFEST-gemma-4-31B-it.json
  BPRIME:reviews/impl/probe/probe_env_Bprime.py
  BPRIME:rulings-D271.md
  BPRIME:rulings_D271.py
  BPRIME:tools/dry_run_Bprime.py
  BPRIME:tools/make_manifest_Bprime.py
  BPRIME:tools/prev/bprime_publish_map-v0.py
  BPRIME:tools/prev/dry_bprime-v1.py
  BPRIME:tools/prev/dry_bprime_behavior-v0.py
  BPRIME:tools/prev/freeze_Bprime-v0.py
  BPRIME:tools/prev/publish_Bprime-v0.py
消えた 0 件
変わった 8 件
  BPRIME:tools/bprime_publish_map.py
  BPRIME:tools/colab/boot_bprime.py
  BPRIME:tools/dry_bprime.py
  BPRIME:tools/dry_bprime_behavior.py
  BPRIME:tools/freeze_Bprime.py
  BPRIME:tools/make_contrasts_Bprime.py
  BPRIME:tools/publish_Bprime.py
  BPRIME:tools/tools-log-Bprime.md
```

- 読み: `Bprime/tools/independent/` の中の変化は、この作業で書いた三つの新しいファイル（二つの器・事前登録の文）だけ（組み立ての器が確かめた・この記録は控えの後に書いたので一覧に無い）。それより外の変化は、上の置き場ごとの数のとおりで、この作業の間に同じ置き場で作業していたコーディネータの物と読める——この器と一時の器は `Bprime/tools/independent/` と一時置き場の外に書く所を持たず、Python の .pyc の書き込みも止めて走らせた（`PYTHONDONTWRITEBYTECODE=1`・器は `__main__` で `sys.dont_write_bytecode`）。この読みの裏づけとして、二つの器の文に、ファイルを書く呼び出しが無いことを組み立ての器が確かめた: ファイルを書く・消す・動かす呼び出しの型（`open\([^)]*['\"][wa]`・`\.write\(`・`np\.save`・`torch\.save`・`json\.dump\(`・`os\.remove`・`shutil`・`os\.rename`・`\.unlink\(`）は、二つの器の文に一つも無い。　時間帯の照らし（組み立ての器）: 本番の走りの前 → 後の外の変化 19 件のうち、更新時刻が本番の四つの走りのどれかの時間帯（開始〜終了＋1 秒）に入るものは 14 件（BPRIME:records/Bprime/MANIFEST-gemma-4-31B-it.json（更新 2026-09-30 05:36:07 UTC・final_rw_dry の間）／BPRIME:reviews/impl/probe/probe_env_Bprime.py（更新 2026-09-30 05:26:29 UTC・final_rw_selftest の間）／BPRIME:rulings-D271.md（更新 2026-09-30 05:35:54 UTC・final_rw_dry の間）／BPRIME:rulings_D271.py（更新 2026-09-30 05:35:36 UTC・final_rw_dry の間）／BPRIME:tools/dry_run_Bprime.py（更新 2026-09-30 05:25:53 UTC・final_rw_selftest の間）／BPRIME:tools/make_manifest_Bprime.py（更新 2026-09-30 05:28:21 UTC・final_rw_selftest の間）／BPRIME:tools/bprime_publish_map.py（更新 2026-09-30 05:36:31 UTC・final_rw_dry の間）／BPRIME:tools/colab/boot_bprime.py（更新 2026-09-30 05:21:59 UTC・final_rw_selftest の間）／BPRIME:tools/dry_bprime.py（更新 2026-09-30 05:21:43 UTC・final_rw_selftest の間）／BPRIME:tools/dry_bprime_behavior.py（更新 2026-09-30 05:21:43 UTC・final_rw_selftest の間）／BPRIME:tools/freeze_Bprime.py（更新 2026-09-30 05:39:14 UTC・final_rw_dry の間）／BPRIME:tools/make_contrasts_Bprime.py（更新 2026-09-30 05:38:48 UTC・final_rw_dry の間）／BPRIME:tools/publish_Bprime.py（更新 2026-09-30 05:36:52 UTC・final_rw_dry の間）／BPRIME:tools/tools-log-Bprime.md（更新 2026-09-30 05:27:08 UTC・final_rw_selftest の間））。ただし、同じ置き場で同じ時刻に別の書き手が作業していたので、外の変化が誰の物かをこの控えだけで確かに分けることはできない（読みの限り）。

## 9. 出典の照合（組み立ての器が機械で照らした）

- 本文に「」で引いた語句のうち、正本・指示・草案 9・事前登録の文から引いたものが、それぞれの原文にそのまま含まれること（ほかの「」は語の強調で、文書からの引用ではない）:

  - 「近道なし・バッチ一」 → 正本 `independent_recompute.new_paths`（含まれる）
  - 「器は段ごとに一致か不一致かだけを印字し、値は開かない」 → 正本 `independent_recompute.print`（含まれる）
  - 「札が同じ」 → 正本 `independent_recompute.agreement`（含まれる）
  - 「本の抽出と同じ読み込みの設定・同じ注意の実装と決定性の設定・バッチ一・bf16 で、違うのは活性を取り出す書き方だけ」 → 正本 `independent_recompute.reextract.path`（含まれる）
  - 「順伝播と加減は bf16」 → 正本 `readout.primary.precision`（含まれる）
  - 「加減は主位置から読み取りの位置まで」 → 正本 `readout.primary.band`（含まれる）
  - 「本の計算は近道（主位置より前の計算の使い回し）を使わない」 → 正本 `computation.shortcut`（含まれる）
  - 「softcap」 → 正本 `readout.primary.quantity`（含まれる）
  - 「text_config」 → 正本 `inputs.model_facts.softcap_level`（含まれる）
  - 「model.language_model.layers」 → 正本 `layers.layer_path`（含まれる）
  - 「全ての効き目の差の絶対値が許容の内」 → 正本 `independent_recompute.agreement`（含まれる）
  - 「`use_cache=False` と同じ」 → 指示の文（含まれる）
  - 「hidden_states[-1]` は正規化の後の値なので使わない」 → 指示の文（含まれる）
  - 「h × rsqrt(mean(h²)＋eps) × g」 → 指示の文（含まれる）
  - 「v を層の出力の型に直してから sign×coef を掛けて足す」 → 指示の文（含まれる）
  - 「static の行を二つ（減算の行と加算の行を一つずつ）」 → 指示の文（含まれる）
  - 「残差のノルム」 → 指示の文（含まれる）
  - 「方向の名|符号」 → 指示の文（含まれる）
  - 「B′ のフックの数え方（transformers 5 の居残るフックを数えない・`bprime_gemma` v0.1）」 → 草案 9（含まれる）
  - 「書いた時の状態」 → 事前登録の文（含まれる）
  - 「二つの器の本体と歯の変種の器は書いた後」 → 事前登録の文（含まれる）

- 手回しの道が写した transformers 5.16.1 の行と、段階 B と層三の凍結の器の行（ファイル・行の番号・その行に含まれるべき字句）:

  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 2306 行目に「image_mask, video_mask, audio_mask = self.get_placeholder_mask(input_ids, inputs_embeds)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 2313 行目に「llm_input_ids = torch.where(multimodal_mask, self.config.text_config.pad_token_id, llm_input_ids)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 2314 行目に「inputs_embeds = self.get_input_embeddings()(llm_input_ids)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 2320 行目に「per_layer_inputs = self.language_model.get_per_layer_inputs(llm_input_ids, llm_inputs_embeds)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 2385 行目に「position_ids = torch.arange(inputs_embeds.shape[1], device=inputs_embeds.device) + past_seen_tokens」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 2409 行目に「causal_mask_mapping = create_masks_for_generate(**mask_kwargs)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1664 行目に「per_layer_inputs = self.project_per_layer_inputs(inputs_embeds, per_layer_inputs)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1667 行目に「past_key_values = DynamicCache(config=self.config)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1694 行目に「position_embeddings[layer_type] = self.rotary_emb(hidden_states, position_ids, layer_type)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1699 行目に「shared_kv_states = kwargs.pop("shared_kv_states", UserDict())」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1703 行目に「per_layer_input = per_layer_inputs[:, :, i, :] if per_layer_inputs is not None else None」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1716 行目に「hidden_states = self.norm(hidden_states)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1444 行目に「hidden_states *= self.layer_scalar」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1459 行目に「return super().forward(input_ids) * self.embed_scale.to(self.weight.dtype)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 209 行目に「return hidden_states * torch.pow(mean_squared, -0.5)」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 214 行目に「normed_output = normed_output * self.weight.float()」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 2588 行目に「logits = logits / final_logit_softcapping」（含まれる）
  - `pylib/transformers/models/gemma4/modeling_gemma4.py` の 1247 行目に「value_states = self.v_proj(hidden_states).view(hidden_shape) if self.v_proj is not None else key_states」（含まれる）
  - `pylib/transformers/utils/output_capturing.py` の 119 行目に「module.register_forward_hook(output_capturing_hook)」（含まれる）
  - `pylib/transformers/utils/output_capturing.py` の 277 行目に「collected_outputs[key].append(outputs.last_hidden_state)」（含まれる）
  - `pylib/transformers/masking_utils.py` の 262 行目に「if local_attention_size is not None and kv_length >= local_attention_size:」（含まれる）
  - `pylib/transformers/masking_utils.py` の 268 行目に「if (q_length == 1 or kv_length == q_length) and (padding_mask is None or fast_all(padding_mask)):」（含まれる）
  - `pylib/transformers/integrations/sdpa_attention.py` の 124 行目に「is_causal = q_length > 1 and attention_mask is None and is_causal」（含まれる）
  - `pylib/transformers/cache_utils.py` の 144 行目に「self.keys = torch.cat([self.keys, key_states], dim=-2)」（含まれる）
  - `PUB/tools/run_stageB_local.py` の 165 行目に「V = np.asarray(vec, dtype=np.float32)」（含まれる）
  - `PUB/tools/run_stageB_local.py` の 178 行目に「cache[key] = sign * coef * torch.as_tensor(V, dtype=hs.dtype, device=hs.device)」（含まれる）
  - `PUB/tools/run_stageB_local.py` の 184 行目に「hs[i, int(st):, :] = hs[i, int(st):, :] + (add[i] if per_row else add)」（含まれる）
  - `PUB/tools/bl3_core.py` の 293 行目に「dirs_by_row[r['id']] = [('static', s)] + [('iso:%d' % i, s) for i in range(n_iso)]」（含まれる）
  - `PUB/tools/direction_B.py` の 39 行目に「idx = int(math.floor(ratio * n_layers + 0.5)) - 1」（含まれる）

## 検分票

- **対象**: `Bprime/tools/independent/bprime_recompute_rewrite.py`（SHA16 DF0833637E5755D8）・`bprime_reextract.py`（SHA16 AEF215AA0F577E45）と本記録。
- **段階**: 一部事前登録あり。`--dry` の判定の決まり（正本の許容を差の最大に当てる・`dry:` の行）は、器を走らせる前に器に書いた。`--dry` の結果と歯の変種の予想（方向と信頼度）は、器を一度も走らせる前に時刻つきで書いた（書き換えの道の器と歯の変種の器を書いた後・再抽出の道の器を書く前・§5.3。事前登録の文の「書いた時の状態」の誤りは §5.3 で訂正した）。自己検査の合否の決まりは器を書く時に書いた。**本検分の手順（kensho）の読み込みは事後**——二つの道の自己検査の試しの走りと再抽出の道の `--dry` の試しの走りの結果を見た後（書き換えの道の `--dry` の試しの走りの結果を見る前）に読み、検分票と敵対的検分はその後に当てた。作業の段階は、B′ の器の段（独立の再計算の器のうち、残差の書き換えの道と独立の再抽出の道）・封印の前・下見の前の凍結の前・系統内の器の実装の検分の前。
- **凍結物の同定**: 正本 `design/contrasts-Bprime.json` SHA16 99E8F2BD3C2D4EA2（読んだ時と組み立ての時で同じか: 同じ（作業の頭の控えと組み立ての前の控えで大きさと更新時刻が同じ・更新時刻 2026-09-29 23:17:06 UTC））・草案 9 SHA16 4E4DF648DE36C700・台帳 SHA16 569CEC81C8F2E7BE・公開の置き場の凍結の器 `run_stageB_local.py` SHA16 E976A4F5B63767FA・`direction_B.py` SHA16 E84A101655685F2B・`bl3_core.py` SHA16 E8CD3A24950F8581・突き合わせの相手 `bprime_run.py` SHA16 536C981D3698C2C7・`bprime_directions.py` SHA16 8D999D06A7773343（中は表示していない）・手元の版 torch 2.9.1+cpu・transformers 5.16.1・numpy 2.4.6。正本と草案はまだ封印の前の案で、この記録の間にも同じ置き場で作業が進んでいた（§8）。
- **盲検の状態**: 本物の模型で読み取りの値を出していない・見ていない（乱数の小さな模型だけ・実の重みは手元に無い）。コーディネータのフックの道と抽出の器の実装は読んでいない（`--dry` で中を見ずに呼んだだけ・落ちたときの文言は印字する形にしたが、落ちなかった）。ただし道の決まり（加減の算術・帯・読み取り・小さな模型の作り方・合成の方向）は、コーディネータが書いた指示から受け取っている（COI 記録の一）。盲検の破れの度合いは測っていない（測る対象の判定者がいない作業）。
- **敵対的検分**: 書き手の自己の敵対の確かめだけ（系統内の別の個体による器の実装の検分〔草案 §12〕はまだ）。
  - 不利な材料を先に: (a) 二つの道とコーディネータの道は同じ指示から書かれ、共有の読み違い（指示が正本を読み違えていれば、その読み違い）は突き合わせで捕まらない。(b) 突き合わせは CPU と乱数の小さな模型だけで、本物の模型の窓つきの層の is_causal の形・GPU の核・複数の装置は試していない。(c) 再抽出の道とコーディネータの器は、層の出力を forward の hook で受け取る PyTorch の仕組みの層を共有する（§3.8）。(d) 歯の変種は書き手の道の側を誤らせたもので、フックの道の側の誤りを直接に試したものではない。(e) 自己検査の合否はすべて書き手が決めた確かめで、独立の確かめの数ではない。(f) hook の確かめは登録された forward の hook の不在しか見ない（列挙した仕組みの外は見ない・教訓 23）。
  - 試みた反証: 歯の確かめ（hidden_states[-1] の取り違え・1＋g・static の効き目が零でない・反転した方向の余弦が −1）、止まるべき所で止まるかの負の試験（台帳のずれ・書き出し・hook・層・係数・型・形・外した升目・名の形）、hook を掛ける関数を落ちる形に差し替えて走らせる試験、層ごとの入力と layer_scalar のある変種、フックの道とコーディネータの抽出の器の後の走らせ直し、記録用の hook が居残った模型での走らせ直し、歯の変種（§5.3・事前登録つき）。
  - 分母: 突き合わせの最大は、二つの道の同じ鍵の集合（行と「方向の名|符号」）の上で取った（鍵の集合が違えば比べられないと印字する形）。基底率: 数え上げの主張は自己検査の ok の数と歯の変種の捕まえた数だけで、その母数は器が定めた確かめと変種の数（すべて書き手が選んだもの）。出典ピン留め: 本文に引いた正本の語句と、写した transformers と凍結の器の行は、組み立ての器が文字列で照らした（§9）。
- **系統の内訳**: 書き手＝Claude Opus 5.5（Claude Code の下請けの個体）。突き合わせの相手の書き手＝コーディネータ（Claude 系の別の個体）。系統外の目は通っていない。二つの道はどちらも Claude 系が同じ指示から書いたので、系統と指示に共通の読み違いは突き合わせでは捕まらない。「自己検査が全て ok」「突き合わせが許容の内」を、器が本物の模型で正しいことの資格として引かない（教訓 13）。
- **COI 記録**:
  - (一) 道の決まりの出所が共通: 加減の算術・帯・読み取りの量・小さな模型の作り方・合成の方向は、コーディネータが書いた指示（正本からの写し）から受け取った。
  - (二) 情報の状態: 作業の頭に、登録者の記憶の索引（会話の頭に渡されたもの）で B′ の進み具合（草案 9・器の段・`bprime_gemma` のフックの数え方の件）を知っていた。コーディネータの器の中身は知らない。層三の書き手の記録から、層三ではフックの道が段階 B の `make_hook` をそのまま呼んだことを知っていた（B′ のフックの道がどうかは知らない）。
  - (三) 希望の向きの引力: 書き手には「突き合わせが一致してほしい」引力がある。判定の許容と判定の行は走らせる前に器に書き、`--dry` の予想は走らせる前に事前登録の文に書いた（§5.3）。
  - (四) 独立の範囲: 独立なのは、加減の仕組み（層の出力の書き換え対フック）・層の回し方・読み取りの実装・取り出しの書き方・升目と文脈の組み立ての書き方・行と方向の帳簿。共有しているのは、模型の部品・transformers・段階 B と層三の凍結の関数（組み立て・層の添字・行と方向の組）・トークナイザ・台帳・指示。
  - (五) 調べと試しの走りと直し: 器を書く前に、一時置き場の二つの調べの器で、トークナイザだけで升目と抽出の文脈の組み立てが台帳と一致すること（S1|Onull と N1|O-Ncold・ids_sha16 まで）と、指示の作り方の小さな模型の構造（型・層の種類・頭の次元・KV の頭・語彙の行列の共有・hook の数・hidden_states の数）を見た（順伝播は二回だけ・値は印字していない）。試しの走りは次の順（組み立ての器がファイルの記録から写した）: 書き換えの道 --selftest（試し一）（出力の作成 2026-09-30 04:52:35 UTC）: 最後の行の前で落ちた（標準エラーに例外）／書き換えの道 --selftest（試し二）（出力の作成 2026-09-30 04:53:36 UTC）: `selftest: 82/82 ok`／再抽出の道 --selftest（試し一）（出力の作成 2026-09-30 05:04:12 UTC）: `selftest: 23/23 ok`／再抽出の道 --dry（試し一）（出力の作成 2026-09-30 05:07:13 UTC）: `[float32] dry: 再抽出の許容（rel_tol 1e-05・cos_min 0.99999）の内`・`[bfloat16] dry: 再抽出の許容（rel_tol 1e-05・cos_min 0.99999）の内`・`dry: 二つの型とも再抽出の許容の内`／書き換えの道 --dry（試し一）（出力の作成 2026-09-30 05:08:32 UTC）: `[float32] 差の絶対値の最大: 効き目 3.61e-07・無操作の量 7.82e-08`・`[float32] dry: 一段目の許容（0.001）の内（差の最大 3.61e-07）`・`[bfloat16] 差の絶対値の最大: 効き目 5.36e-07・無操作の量 2.09e-07`・`[bfloat16] dry: 一段目の許容（0.001）の内（差の最大 5.36e-07）`・`dry: 二つの型とも一段目の許容の内`。試し一の書き換えの道の自己検査は、頭の行の印字で落ちた（設定の num_key_value_heads は層ごとの値で、全体の値を読むと例外になる〔transformers 5 の異種の設定〕）。直したのは頭の行の印字だけ（層の部品から読む `_tiny_desc`）で、確かめの中身は変えていない。試しの走りの後、本番の走りの前に、`--dry` の走らせ直しの二つの参考の行を「止まったら文言を印字して続ける」形に包んだ（判定の行と確かめの中身は変えていない）。本番の走りは、この版の器を上の SHA-256 で記録してから、四つとも走らせ直した。試しの走りの出力は一時置き場に残し、本番の出力と名を分けた（教訓 22）。
- **判定**: **保留**。器の出力の数は器の出力のとおり（§0・§4・§5）。器が本物の模型で正しいことは、コーディネータの確かめ・系統内の器の実装の検分・本物の模型での一段目の突き合わせと再抽出の突き合わせを経るまで保留する。コーディネータの確かめに回せる水準、と書き手は判断する（書き手自身の判定で、独立の検分を経ていない・登録者の裁定の代わりにならない）。
- **本検分が確認していないこと**:
  - 本物の模型（GPU・bf16）での一致（窓つきの層の is_causal の形・SDPA の核の選び方・cache の有無による K/V の並びの違い・bf16 の GEMM・複数の装置に割ったときの動き）
  - 正本の一致の決まりの後半（札の一致）と、二段目（本の道と本の器のフック）
  - 指示と正本の読みそのものの正しさ（読み取りの集合・帯・符号の決まり・無操作の置き方・名前のある方向の定義）——三つの道が同じ指示に従うので、共有の読み違いは捕まらない
  - 凍結の方向の npz（本物の方向）での動き、本の計算の順伝播の数と時間
  - コーディネータの合成の模型と、この器の小さな模型の乱数の引き方が同じか
  - フックの道の側の誤りを一段目の突き合わせが捕まえるか（歯の変種は書き手の道の側だけを誤らせた）
  - 突き合わせと歯の変種の感度が本物の模型でも同じか（本物の模型の相対の加減は、この記録では見ていない正本の鍵にある）
  - hook の確かめの外の仕掛け（部品の forward の差し替え・accelerate の `_hf_hook`・関数の差し替え）が値を変えていないか
  - transformers の版の違いへの頑健さ（版が違えば止めるだけ）
  - 本記録の文（手で書いた部分）の正しさ——数とハッシュは機械で写したが、文は書き手の読み

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
