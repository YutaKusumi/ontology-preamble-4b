# 残差の書き換えの道の書き手に渡した指示の文（機械で切り出した・B-lens 層三・2026-09-25）

- 出所: 会話の記録の uuid `4d0f991d-70d5-4247-92bb-d0e75d2de67f`・呼び出しの番号 `toolu_017uoYchyevKTmdC4gyTgZos`・2026-09-25 06:26 日本時間（2026-09-24T21:26:34.055Z）。
- 呼び出しの引数（指示の文のほか・逐語）: description = Write independent residual-rewrite recompute tool・isolation = worktree・model = opus・run_in_background = True・subagent_type = general-purpose。
- 指示の文の SHA-256（UTF-8）: 3E34A8F88BFDFEB410B569CB498E7C5429470DC5E6C19C06E931DB0C34E73E9D・5743 字。
- 書き手が書いたもの: `tools/bl3_recompute_rewrite.py`・`records/Bl3/tools/recompute-rewrite-dev-Bl3.md`（コーディネータの取り込みと確かめは `records/Bl3/tools/tools-log-Bl3.md` の 7）。
- 置いた理由: 器についての意見伺いの C1-A2（書き手に渡した指示の文が記録に無い）を採った（裁定 D231）。器の実装の検分者が、指示と正本と書き手の器を突き合わせられるように。

## 指示の文（逐語）

````text
あなたは研究リポジトリ ontology-preamble-4b（あなたの作業場は、このリポジトリの worktree の写し）で、B-lens 層三（Bl3）の「独立の再計算」の器のうち、**残差の書き換えの道**を書く係です。登録者（楠見優太さん）が、コーディネータ（別の Claude の個体・南無弥勒如来）とは**別の個体**がこの道を書くことを許可し、あなたがその個体です。コーディネータが書いた「フックの道」と、あなたが書く「残差の書き換えの道」を、後で数値で突き合わせる（正本の `independent_recompute.stages.first`）ので、**あなたの道はコーディネータの実装から独立に書く**ことが一番大事です。

## 読むもの（読んでよい）
- 正本 `design/contrasts-Bl3.json`: 鍵 `independent_recompute`（what・who・new_paths・stages・tol_stage1・agreement）、`readout.primary`（rule・quantity・precision・place・band・letters・refuse_head）、`layers`（indices・selected_ratio・coef_applied）、`computation`。
- 草案 `design/design-Bl3-draft3.md` の §3（読み取り）と §12（独立の再計算）。
- 設計事実 `records/Bl3/design-facts-Bl3.json` の `facts.A`（`prefix_ids`＝主の書き出しのトークン・`letter_ids`＝選択の文字と refuse の頭のトークン番号）と `facts.B.cells`（升目ごとの prompt_len・main_position・readout_position・family）と `facts.D.real_pairs`（実在の差の方向の名の並び）。
- 段階 B の凍結の器（**読むだけ・変えない**）: `tools/steer_B.py` の `apply_chat`・`main_position`、`tools/run_stageB_local.py` の `arm_texts`・`scenario_and_instruction`・`user_message`（プロンプトの組み立て）、`tools/direction_B.py` の `layer_index`（層の割合 → 層の添字）。
- `tools/run_stageB_local.py` の `make_hook` は、**加減の算術の決まり（ベクトルを層の出力の型に直してから sign×coef を掛けて足す・主位置から後ろ）を知るために読んでよいが、呼んではいけない**（あなたの道は、フックで足す道の突き合わせの相手なので、フックの仕組みを使わない）。
- 手元の transformers 4.57.3（`transformers/models/qwen3/modeling_qwen3.py`・`masking_utils`）の実装（層を手で回すため）。

## 読まないもの
- `tools/bl3_run.py`（コーディネータのフックの道の実装）と `tools/dry_run_Bl3.py` と `tools/analyze_Bl3.py` の中身は**開かない**。最後の一段目の突き合わせでだけ、`tools/bl3_run.py` を**中を見ずに**下の公開の関数で呼ぶ。

## 残差の書き換えの道の決まり（正本から）
- 入力: 段階 B の組み立てのままのプロンプト（`steer_B.apply_chat(tok, run_stageB_local.user_message(arm_texts()[腕]['text'], 場面の本文, 指示))`・場面と指示は `scenario_and_instruction(場面)`）の直後に、主の書き出し（`facts.A.prefix_ids`）を**トークンの並びのまま**つなぐ。バッチ一、近道なし（列の全体を流す）。主位置 mp＝プロンプトの長さ−1（`steer_B.main_position`）、読み取りの位置＝列の最後。升目ごとに `facts.B.cells` の prompt_len・main_position・readout_position と一致することを確かめ、違えば止める。
- 加減: 選んだ層（添字＝`direction_B.layer_index(正本 layers.selected_ratio, 模型の層の数)`・本物の模型では 17）の**出力の隠れ状態を書き換える**: 主位置から列の最後までの位置に、sign×coef×v を足す（v は方向の float64 のベクトル・coef は `layers.coef_applied`・段階 B と同じく、v を層の出力の型〔bf16〕に直してから掛けて足す）。そのあと残りの層を流す。**フック（register_forward_hook など）で足してはいけない**。層を手で回す（埋め込み → 層 0〜L → 書き換え → 層 L+1〜最後）か、それと同じ計算になる別の組み方で書く。位置の埋め込み（rotary）と因果の注意の窓（mask）は、模型の forward と同じにする。
- 読み取り: 最後の層の出口の残差（**最終の正規化の入力**・`hidden_states[-1]` は transformers 4.57.3 では正規化の後の値なので使わない）の最後の位置を float32 に上げ、最終の正規化を float32 で当て（h × rsqrt(mean(h²)+eps) × g・g は `model.model.norm.weight` の float32）、語彙の行列（`lm_head.weight`）の読み取りの集合の行（族の選択の文字の順で a が先頭・survival は a b c、nuclear は a b c d・最後に refuse の頭）を float32 で当てる。量＝z_a − logsumexp（ほかの選択の文字と refuse の頭）。効き目＝加えた値 − 無操作（零のベクトル）の値。
- 出力の形（コーディネータのフックの道と同じ）: `{行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}`。符号の書き方は `'%s|%+d' % (方向の名, 符号)`（例 `static|-1`・`iso:12|+1`・`real:O~Onull|-1`）。

## 作るもの（新しいファイルだけ・既にあるファイルは一つも変えない）
1. `tools/bl3_recompute_rewrite.py`:
   - 関数 `recompute_rewrite(model, tok, T3, FJ, rows, dirs_by_row, dirs, layer_idx, coef)`。rows: [(行の名, 升目の鍵 'S1|O-Ncold' など, 符号)]・dirs_by_row: 行の名 → [(方向の名, 符号)]・dirs: 方向の名 → float64 のベクトル。戻り値は上の形。升目の入力は自分で組み立てる（上の決まり）。
   - `--selftest`（乱数の小さな模型で）: 零のベクトルの効き目が零になる／書き換えを零にした手回しの道の最終の正規化の入力が、模型そのものの forward の最終の正規化の入力と一致する（この一致を見るためだけに、`model.model.norm` に前の hook を掛けて取るのはよい・足すためには使わない）／主位置より前の位置は書き換えない、を確かめる。
   - `--dry`: 乱数の小さな模型で、あなたの道と、コーディネータのフックの道（下の公開の関数）を、同じ入力で比べ、**一段目の許容 `independent_recompute.tol_stage1`** の内かを確かめて、差の最大を印字する。比べる組は、正本の主の行（`main_rows`）のうち方向が static の行を二つ（減算の行と加算の行を一つずつ）選び、それぞれ 無操作・static・等方に見立てた合成の方向を二十本・比べる相手に見立てた実在の差の方向の名の合成の方向を、行の符号と逆の符号の両方で。
2. 開発の記録 `records/Bl3/tools/recompute-rewrite-dev-Bl3.md`（日本語）: 読んだもの・読まなかったもの・書き方の決め（層の回し方・mask と rotary の作り方・bf16 のまま足すことなど）・自己検査と `--dry` の結果（**数は器の出力から写す・手で打たない**）・正本で決まっていなかった所・末尾に検分票（対象・段階・凍結物の同定・盲検の状態・敵対的検分・系統の内訳・COI記録・判定・本検分が確認していないこと〔必ず一つ以上〕）。最後の行に次の柵を置く: 「本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。」

## 乱数の小さな模型の作り方（コーディネータの合成の器と同じ作り方・自分で書く）
- トークナイザと設定の置き場: `~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554`（手元にある・**実の重みは使わない**）。
- `cfg = AutoConfig.from_pretrained(置き場)`; `cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim, cfg.intermediate_size = 64, 4, 4, 2, 16, 128`; `cfg.layer_types = list(cfg.layer_types)[:4]`（元の長さのままだと計算の使い回しで空の層ができる）; `torch.manual_seed(0)`; `model = AutoModelForCausalLM.from_config(cfg)`; 名が `norm.weight` で終わる全ての重みを `torch.Generator().manual_seed(1)` の一様乱数 [0.5, 1.5) で置き換える（初期値の一のままだと正規化の誤りが見えない）; `model = model.to(torch.bfloat16).eval()`。層の添字は `direction_B.layer_index(0.5, 4)`（＝1）。
- 合成の方向: `np.random.default_rng(5)` で次元 64 の正規乱数を引き、static のノルムにそろえる。名は `static`・`iso:0`〜`iso:19`・`real:` ＋ `facts.D.real_pairs` の名。
- 手元の版: torch 2.9.1（CPU）・transformers 4.57.3・numpy 2.4.2。CPU の bf16 なので一回の順伝播が数秒かかることがある。比べる組を小さく保つ。

## コーディネータのフックの道の公開の関数（`--dry` の比べにだけ使う・中は開かない）
```python
import sys; sys.path.insert(0, 'tools')
import bl3_run as BR
R = BR.Runner(model, T3, layer_idx, coef, dirs)            # dirs: 方向の名 → float64 のベクトル
cells = BR.build_cells(tok, T3, FJ, ['S1|O-Ncold', 'S1|Onull'])   # 升目の鍵 → 升目の入力
hk = BR.recompute_hook_path(R, [(行の名, cells[升目の鍵], 符号), ...], {行の名: [(方向の名, 符号), ...]})
# 戻り値: {行の名: {'noop_lo': float, 'effects': {'方向の名|符号': float}}}
```

## 守ること
- 既にあるファイルを一つも変えない。コミットも push もしない（コーディネータが確かめてからコミットする）。
- 実の重みで読み取りの値を出さない（封印の前の決まり）。乱数の小さな模型だけで確かめる。
- 数・ハッシュ・引用は器の出力から写し、手で打たない。
- 正本で決まっていない所に出会ったら、黙って決めずに、選んだ決め方とその理由を開発の記録に書く。
- 資格情報や API の鍵は使わない・見ない。

## 終わったら返すもの
- 書いたファイルの置き場（worktree の中のパス）。
- 書き方の要点（層の回し方・mask と rotary・書き換えの位置と型）。
- 自己検査と `--dry` の結果（差の最大・許容の内か）を、器の出力のとおりに。
- 正本で決まっていなかった所と、コーディネータに伝えたいこと。
````

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
