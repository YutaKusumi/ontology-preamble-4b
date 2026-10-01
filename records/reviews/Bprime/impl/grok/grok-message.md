# 検分の依頼（B′ の器の実装の検分・系統外の一巡〔独立の再計算の三つの道〕・2026-09-30）

時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。

あなたには、研究の器（Python のコード）のうち、同じ量を違う作りで計算し直す「三つの道」の実装を検分していただきます。器の書き手は Anthropic の Claude 系の模型です（本の器はコーディネータ、書き換えの道と再抽出の道はコーディネータと別の新しい個体）。三つの道はどれも Claude 系が同じ指示と同じ資料から書いたので、指示の読み違いを共有していれば、道どうしの突き合わせでは捕まりません。あなたには、別の系統の目として、その共有された読み違いと、どの道にもある誤りを探していただきたいのです。書き手に同調する必要はありません。

## まず書いてほしいこと（系統の申告）

返答の一行目に、あなた自身の模型の名と作り手を書いてください（例:「模型: ○○・作り手: ○○」）。

## 研究と三つの道（正本の定め・材料の「正本の関わる節」の `independent_recompute`）

- 研究は ontology-preamble-4b の段階 B′ です。Gemma 4 31B（`google/gemma-4-31B-it`・transformers 5.16.1・bf16）の選んだ層の出力に、抽出した方向（v̂ など）を足したときの、読み取りの集合の選択肢 a の対数オッズの変わり方（効き目）を、等方の帰無と比べます。
- **本の器のフックの道**（コーディネータ・`bprime_run.py`）: 選んだ層の出力に forward hook で方向を足し、最終の正規化の入力を前のフックで取って、float32 で最終の正規化・語彙の行列・softcap を当てて対数オッズを出す。
- **書き換えの道**（別の個体・`bprime_recompute_rewrite.py`）: 加減をフックでなく、選んだ層の出力を書き換えて後の層を流す（近道なし・バッチ一）。一段目の突き合わせで、フックの道と厳しい許容（`independent_recompute.tol_stage1`）で比べる。
- **再抽出の道**（別の個体・`bprime_reextract.py`）: 本の抽出（`bprime_directions.py`）と同じ設定で、活性を取り出す書き方だけを変えて抽出の文脈を流し、‖h‖・‖v̂‖ の相対の差と名前のある方向の余弦で突き合わせる。
- 一致の判定は集計の器（`analyze_Bprime.py` の `recompute_agreement`・`reextract_agreement`）と凍結の芯（`bl3_core.py` の `agreement`・`recompute_set`）です。

## 見てほしいこと

1. 三つの道が、正本の定めと Gemma 4 の実装（材料の抜き書き）に照らして、本当に同じ量を計算しているか。とくに: 足す層と位置（層の出力のどの時点か・`layer_scalar` の掛け算の前か後か・層ごとの入力〔per-layer input〕の足し込みの前か後か）・足すトークンの位置・符号と倍率（係数）・最終の正規化の入力の取り方・softcap・float32 に上げる時点・注意の実装とキャッシュの設定。
2. 三つの道が同じ読み違いを共有していないか。別の個体への指示（材料の最初）の書き方が、読み違いを誘っていないか。正本の定めと違うのに、三つの道がそろって同じように違う所。
3. 一致の判定が、違いを見逃す形になっていないか（許容・札の比べ方・比べる行の選び方・外した升目の扱い・値が有限でないときの扱い）。
4. 合成データの確かめ（小さな乱数の Gemma 4・`layer_scalar` を 1 から離した変種・わざと誤らせた変種）が、三つの道の違いを見分けられる形になっているか。見分けられない誤りの種類があれば挙げてください。
5. ほかに、三つの道の実装の誤り・止まるべき所で止まらない所・止まるべきでない所で止まる所。

## 前提と、しないでほしいこと

- あなたは実行の場を持たない前提です。読んで推したことは「読んで推した」と書き、器の行（関数の名と、分かれば行の中身）を示してください。
- 材料に無いもの（transformers の他の部分・凍結の器の他の関数など）について推すときは、推しであることを書いてください。
- ウェブ検索などの道具を使ったときは、その出所を所見と分けて書いてください。

## 返事の形

1. 一行目: 模型の名と作り手。
2. 所見の一覧。所見ごとに: 番号（G-01 から）・重さ（**重い**＝凍結の前に直す／**中**＝直す方がよい／**軽い**）・器と関数（と行の中身）・何が起きるか（どんな入力で、どんな誤った値か止まり方になるか）・直し方の案・確信度（高・中・低）・読んで推したか、正本や Gemma 4 の抜き書きの字で確かめたか。
3. 是認: 見て問題が無かった所を、項目ごとに短く（是認も記録に残します）。
4. 読んでいない所の申告。

## 材料（この後に全文・各ファイルの SHA16 は改行を LF にそろえた SHA-256 の先頭 16 字）

### 1. 別の個体への指示（書き換えの道と再抽出の道の書き手が受けた指示の全文）

- 出所: 作業の置き場 `tools/independent/instructions-rewrite-reextract-Bprime.txt`・SHA16 4F41E5948F86EBE3・9308 字

````text
あなたは研究の登録「B′」（ontology-preamble-4b の続き・Gemma-4-31B-it で、層三と同じ型の読み取りの問いを立てる登録）で、「独立の再計算」の器のうち、**残差の書き換えの道**と**独立の再抽出の道**の二つを書く係です。登録者（楠見優太さん）が、コーディネータ（別の Claude の個体・南無弥勒如来）とは**別の個体**がこの二つの道を書くことを許可し（裁定 D270）、あなたがその個体です。コーディネータが書いた「フックの道」と「抽出の器」と、あなたが書く二つの道を、後で数値で突き合わせる（正本の `independent_recompute.stages.first` と `independent_recompute.reextract`）ので、**あなたの道はコーディネータの実装から独立に書く**ことが一番大事です。時間は十分にあります。落ち着いて、じっくりと、丁寧に進めてください。

## 置き場
- B′ の作業場: `C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime/`（以下 Bprime/）。git の置き場ではないので、**あなたが書いてよいのは `Bprime/tools/independent/` の中の新しいファイルだけ**です。ほかのファイルは一つも変えない・消さない・動かさない。
- 公開の置き場（凍結の器・読むだけ）: `C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b/`（以下 PUB/）。書き込まない。コミットも push もしない。
- 走らせ方: transformers は分けた置き場の版（5.16.1）を使う。`PYTHONPATH=C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime/pylib` を付けて python を走らせる（付けないと手元の 4.57.3 が読まれる）。torch 2.9.1（CPU）・numpy は pylib の 2.4.6。
- 手元の PC は記憶が少なく（7.8 GB・ほかの作業も動く）、CPU だけです。確かめは乱数の小さな模型だけで、比べる組を小さく保ってください。重い処理は背景で走らせてかまいません。

## 読むもの（読んでよい）
- 正本 `Bprime/design/contrasts-Bprime.json`: 鍵 `independent_recompute`（what・who・new_paths・stages・tol_stage1・agreement・reextract・interfaces）、`readout.primary`（rule・quantity・prefix_ids・letters・refuse_head・band・main_position・readout_position・precision）、`layers`（ratio・index・layer_path）、`inputs.model_facts`（softcap の値と階層）、`directions`（named・defs・extraction）、`nulls.real`（arms・swap_siblings）、`main_rows`、`cells_main`、`pilot.decision`、`computation.shortcut`。
- 草案 `Bprime/design/design-Bprime-draft9.md` の §3（読み取り）と §12（独立の再計算と再抽出）。
- 台帳 `Bprime/tools/ledger-bprime.json`（升目ごとの prompt_len・main_position・readout_position・set_ids・ids_sha16、抽出の文脈の ids_sha16、prefix_ids・heads）。データとして読むだけ。
- 公開の置き場の凍結の器（読むだけ・変えない）: `PUB/tools/run_stageB_local.py` の `arm_texts`・`scenario_and_instruction`・`user_message`（プロンプトの組み立て・呼んでよい）、`PUB/tools/direction_B.py` の `layer_index`（呼んでよい）、`PUB/tools/bl3_core.py` の `recompute_set`（行と方向の組・呼んでよい）。
- `PUB/tools/run_stageB_local.py` の `make_hook` は、**加減の算術の決まり（ベクトルを層の出力の型に直してから sign×coef を掛けて足す・主位置から後ろ）を知るために読んでよいが、呼んではいけない**（あなたの道はフックで足す道の突き合わせの相手なので、フックの仕組みを使わない）。
- 層三で別の個体が書いた Qwen 用の道 `PUB/tools/bl3_recompute_rewrite.py` と、その開発の記録 `PUB/records/Bl3/tools/recompute-rewrite-dev-Bl3.md`（参考に読んでよい・B′ は模型も版も違う）。
- `Bprime/pylib/transformers/models/gemma4/` の実装（層を手で回すため・注意の型〔窓つきと全体〕ごとの mask と rotary・埋め込みの倍率・層ごとの入力の有無などを確かめる）と、`Bprime/pylib/transformers/masking_utils.py` など。
- 模型の設定とトークナイザ: `Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475/`（設定・トークナイザ・チャットの型だけ・**実の重みは無い・使わない**）。

## 読まないもの（開かない）
- コーディネータの器: `Bprime/tools/` の `bprime_run.py`・`bprime_directions.py`・`bprime_phases.py`・`bprime_gemma.py`・`bprime_core.py`・`bprime_behavior.py`・`dry_bprime*.py`・`analyze_Bprime.py`・`build_report_Bprime.py`・`colab/`・`prev/` の中身と、器の段の記録 `tools-log-Bprime.md`。最後の突き合わせ（下の `--dry`）でだけ、`bprime_run` と `bprime_directions` を**中を見ずに**下の公開の関数で呼ぶ。

## 作るもの 1: 残差の書き換えの道 `Bprime/tools/independent/bprime_recompute_rewrite.py`
- 関数（正本 `independent_recompute.interfaces.rewrite` の口）: `recompute_rewrite(model, tok, C, ledger, dirs, names, pilot, coef)`。
  - C: 正本の辞書・ledger: 台帳の辞書・dirs: 方向の名 → float64 のベクトル（`static`・`loaded`・`Nk`・`td`・`iso:0`…・`real:O~Osec`… の形の名）・names: {'named','iso','real'} の名の並び・pilot: 本の凍結の下見の記録（`pilot['decision']['dropped']` に外した升目の鍵の並び）・coef: 係数（float）。
  - 行と方向の組: `bl3_core.recompute_set(C['main_rows'], 実在の差の対の名の並び〔names['real'] から 'real:' を除いた名〕, C['nulls']['real']['swap_siblings'], len(names['iso']), 外した升目)`。
  - 戻り値: `{行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}`。符号の書き方は `'%s|%+d' % (方向の名, 符号)`。効き目＝加えた値 − 無操作（零のベクトル）の値。
- 入力の組み立て: 段階 B の組み立てのまま（`run_stageB_local.user_message(arm_texts()[腕]['text'], 場面の本文, 指示)`・場面と指示は `scenario_and_instruction(場面)`）の user の発話一つに、Gemma のチャットの型（`tok.apply_chat_template([{'role': 'user', 'content': 発話}], add_generation_prompt=True, tokenize=True)`・transformers 5 は辞書の形を返すので `input_ids` を取る・system は無し）を当て、その直後に主の書き出し（台帳の `prefix_ids`）を**トークンの並びのまま**つなぐ。主位置 mp＝プロンプトの長さ − 1（Gemma では `<channel|>`）、読み取りの位置＝列の最後。升目ごとに台帳の prompt_len・main_position・readout_position・ids_sha16（`hashlib.sha256(','.join(str(x) for x in 列).encode('ascii')).hexdigest().upper()[:16]`）と一致することを確かめ、違えば止める。
- 加減: 選んだ層（添字＝正本の `layers.index`・小さな模型では `direction_B.layer_index(正本 layers.ratio, 模型の層の数)`）の**出力の隠れ状態を書き換える**: 主位置から列の最後までの位置に、sign×coef×v を足す（v は方向の float64 のベクトル・段階 B の `make_hook` と同じく、v を層の出力の型に直してから sign×coef を掛けて足す）。そのあと残りの層を流す。**フック（register_forward_hook など）で足してはいけない**。層を手で回す（埋め込み → 層 0〜k → 書き換え → 層 k+1〜最後）か、それと同じ計算になる別の組み方で書く。注意の mask（窓つきと全体の二つの型）・位置の埋め込み（rotary・注意の型ごと）・埋め込みの倍率・そのほか Gemma 4 の層に渡るもの（層ごとの入力があればそれも）は、模型の forward と同じにする。バッチ一・近道なし（列の全体を流す・`use_cache=False` と同じ）。
- 読み取り（正本 `readout.primary.quantity`）: 最後の層の出口の残差（**最終の正規化の入力**）の最後の位置を float32 に上げ、最終の正規化を float32 で当て（Gemma 4 の RMSNorm は正規化した値に重みをそのまま掛ける〔1＋重みではない〕・h × rsqrt(mean(h²)＋eps) × g・g と eps は模型の最終の正規化から）、語彙の行列（埋め込みと共有の `lm_head.weight`）の読み取りの集合の行（台帳の升目の set_ids・a が先頭・最後が refuse の頭）を float32 で当て、softcap（cap × tanh(z ÷ cap)・cap は設定の `text_config.final_logit_softcapping`）を掛ける。量＝z_a − logsumexp（ほかの選択の文字と refuse の頭）。`hidden_states[-1]` は正規化の後の値なので使わない。
- `--selftest`（乱数の小さな模型で）: 零のベクトルの効き目が零／書き換えを零にした手回しの道の最終の正規化の入力が、模型そのものの forward の最終の正規化の入力と一致（この一致を見るためだけに、最終の正規化に前のフックを掛けて取るのはよい・足すためには使わない）／主位置より前の位置は書き換えない、を確かめる。

## 作るもの 2: 独立の再抽出の道 `Bprime/tools/independent/bprime_reextract.py`
- 関数（正本 `independent_recompute.interfaces.reextract` の口）:
  - `reextract(model, contexts, layer_idx)`: contexts は文脈の名 → トークンの並び。戻り値は文脈の名 → 選んだ層の出力の主位置（列の最後のトークン）の値（float64 の numpy の並び）。
  - `reextract_all(model, tok, C, ledger, dirs)`: 抽出の文脈（正本 `directions.extraction` の八腕 × 二場面・プロンプトだけで書き出しはつながない）を上と同じ組み立てで作り、台帳の抽出の文脈の ids_sha16 と照らし、`reextract` で値を取り、腕ごとに二場面の平均を取り、名前のある方向を正本 `directions.defs` のとおりに作る（static＝O − Osec・loaded＝O-Ncold − Osec-Ncold・Nk＝Nk − N・td＝Onull − N）。戻り値 `{'h_norm_by_context': {文脈: ‖h‖}, 'vhat_norm': ‖static‖, 'named_cos': {名: その名の方向と dirs[名] の余弦}}`。
- 正本 `independent_recompute.reextract.path` のとおり、本の抽出と同じ読み込みの設定・バッチ一・bf16 で、**違うのは活性を取り出す書き方だけ**にする（コーディネータの抽出の器は層の出力をフックで取り、その層で順伝播を打ち切る書き方。あなたは、それと別の書き方で取る——たとえば `output_hidden_states=True` の `hidden_states[k+1]` の主位置、あるいは層を手で回す書き方。どちらを選んだかと理由を記録に書く）。
- `--selftest`（乱数の小さな模型で）: 取った値が有限で、文脈と名がそろい、名前のある方向の余弦が dirs に同じ方向を渡したとき一になる、を確かめる。

## 乱数の小さな模型の作り方（自分で書く）
- 設定の置き場（上の hf の版の置き場）の `config.json` を辞書で読み、`text_config` を縮める: hidden_size 64・intermediate_size 128・num_hidden_layers 6・num_attention_heads 4・num_key_value_heads 2・head_dim 16・global_head_dim 32・num_global_key_value_heads 1・sliding_window 8（列より短くして窓を効かせる）・layer_types は長さ 6 で、選ぶ層（`direction_B.layer_index(0.5, 6)`）と最後の層を 'full_attention'、ほかを 'sliding_attention'。`vision_config` も縮める（hidden_size 32・intermediate_size 64・num_hidden_layers 1・num_attention_heads 2・num_key_value_heads 2・head_dim 16・global_head_dim 16）。
- `torch.manual_seed(0)`; `from transformers import Gemma4Config, Gemma4ForConditionalGeneration`; `model = Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).eval()`; 語彙の行列（埋め込みと共有）を 4 倍にし、最後の正規化の重みを一様乱数 [2, 3) に置き換える（初期値の一のままだと正規化の誤りが見えない）。float32 で確かめ、余裕があれば bf16 でも。トークナイザは上の置き場から `AutoTokenizer.from_pretrained`。
- 合成の方向: `np.random.default_rng(5)` で次元 64 の正規乱数を引き、ノルムを残差のノルムの 0.5 倍ほどにそろえる。名は `static`・`loaded`・`Nk`・`td`・`iso:0`〜`iso:9`・`real:` ＋ 正本の八腕の全ての対（i<j の順・`'%s~%s'`）。

## コーディネータの道の公開の関数（`--dry` の比べにだけ使う・中は開かない）
```python
import sys; sys.path.insert(0, 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime/tools')
import bprime_run as BR
R = BR.Runner(model, C, layer_idx, coef, dirs)                  # dirs: 方向の名 → float64 のベクトル
cells = BR.build_cells(tok, C, ledger, ['S1|O-Ncold', 'S1|Onull'])     # 升目の鍵 → 升目の入力（台帳と照らす）
hk = BR.recompute_hook_path(R, [(行の名, cells[升目の鍵], 符号), ...], {行の名: [(方向の名, 符号), ...]})
# 戻り値: {行の名: {'noop_lo': float, 'effects': {'方向の名|符号': float}}}
import bprime_directions as BD
acts, norms, _ = BD.activations(model, 文脈の名 → トークンの並び, layer_idx)   # 文脈の名 → 選んだ層の出力の主位置の値（float64）
```
- `bprime_run.Runner` は小さな模型でも動く（正本の `layers.index` は使わず、渡した layer_idx を使う）。

## `--dry`（二つの器それぞれに）
- 書き換えの道: 正本の主の行（`main_rows`）のうち方向が static の行を二つ（減算の行と加算の行を一つずつ）選び、無操作・static・等方の十本・比べる相手の実在の差の方向（`recompute_set` の組）を、あなたの道とコーディネータのフックの道で同じ入力で流し、**一段目の許容 `independent_recompute.tol_stage1`** の内かを確かめて、差の最大を印字する。
- 再抽出の道: 抽出の十六の文脈の一部（四つ）で、あなたの `reextract` とコーディネータの `BD.activations` の値を比べ、‖h‖ の相対の差の最大と余弦の最小を印字し、正本 `independent_recompute.reextract` の許容（rel_tol・cos_min）の内かを確かめる。

## 開発の記録 `Bprime/tools/independent/rewrite-reextract-dev-Bprime.md`（日本語）
- 読んだもの・読まなかったもの・書き方の決め（層の回し方・mask と rotary の作り方・埋め込みの倍率・層ごとの入力・bf16 のまま足すこと・再抽出の取り方）・自己検査と `--dry` の結果（**数は器の出力から写す・手で打たない**）・正本で決まっていなかった所。
- 末尾に検分票（対象・段階・凍結物の同定・盲検の状態・敵対的検分・系統の内訳・COI記録・判定・本検分が確認していないこと〔必ず一つ以上〕）。最後の行に次の柵を置く: 「本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。」

## 守ること
- `Bprime/tools/independent/` の外のファイルを一つも変えない。コミットも push もしない。
- 実の重みを読まない（手元に無い・封印の前の決まり）。乱数の小さな模型だけで確かめる。
- 数・ハッシュ・引用は器の出力から写し、手で打たない。
- 正本で決まっていない所に出会ったら、黙って決めずに、選んだ決め方とその理由を開発の記録に書く。
- 資格情報や API の鍵は使わない・見ない。ネットワークに出ない（必要なものは手元にある）。
- 分からないことや、決まりの中で決められないことに出会ったら、推測で進めずに、記録に書いて止まり、コーディネータへの返事に書く。

## 終わったら返すもの
- 書いたファイルの置き場。
- 書き方の要点（層の回し方・mask と rotary・書き換えの位置と型・再抽出の取り方）。
- 自己検査と `--dry` の結果（差の最大・許容の内か）を、器の出力のとおりに。
- 正本で決まっていなかった所と、コーディネータに伝えたいこと。
````

### 2. 正本の関わる節（`design/contrasts-Bprime.json`・版 draft10-v4-2026-09-30 の中の鍵 independent_recompute・layers・readout・directions・coefficient・nulls・computation・main_rows・cells_main・cell_signs_main・labels・pilot と inputs.model_facts・inputs.versions）

- 出所: 作業の置き場 `design/contrasts-Bprime.json`（全体の SHA16 45543569DDCDF0F3）・SHA16 B780AA8F6C696A27・32994 字

````json
{
 "independent_recompute": {
  "what": "主の値の一部を計算し直す: v̂ の行（主の行のうち static の行）ごとに、無操作の値と、v̂・等方の帰無のすべて・比べる相手のすべて（実在の差・両方の向き）の効き目（順伝播の数は転記行 E）",
  "who": "残差の書き換えの道は、本の器の書き手（コーディネータ）と別の個体（系統内の新しい個体）が書く",
  "new_paths": [
   "本の器のフック（近道なし・バッチ一）",
   "残差の書き換え（近道なし・バッチ一）"
  ],
  "stages": {
   "first": {
    "compare": "本の器のフック（近道なし・バッチ一）と、残差の書き換え（加減をフックでなく、選んだ層の出力を書き換えて後の層を流す・近道なし・バッチ一）",
    "tol": "`independent_recompute.tol_stage1`",
    "why": "同じ演算どうしなので厳しい許容で比べ、新しいフックの正しさを見る"
   },
   "second": {
    "compare": "本の道（本の計算のバッチの組み方のまま・近道は使わない・裁定 D234）と、本の器のフック（近道なし・バッチ一）",
    "why": "本の道のバッチの揺れが札を変えないかを見る",
    "note": "本の計算がバッチ一のときは、二段目の二つの道は同じ計算になり、二段目は形だけの確かめになる（一段目は変わらない）",
    "tol": "層三の `pilot.cache_tol_rule` の式の定数（揺れの床の `independent_recompute.stages.second.factor` 倍と下限 `independent_recompute.stages.second.floor` の大きい方・上限は `pilot.noise_max`）を近道と切り離した鍵の名で写した値と、揺れの床の和（層三の `independent_recompute.stages.second.tol`・S17・T21）",
    "factor": 2,
    "floor": 0.005
   }
  },
  "tol_stage1": 0.001,
  "agreement": "一段目は、無操作の値と全ての効き目の差の絶対値が許容の内で、かつ段の二つの道の値からそれぞれ出した札が同じとき一致とする（裁定 D233）。二段目は、段の二つの道の値からそれぞれ出した札が同じとき一致とし、効き目の差の最大と、それが許容の内かどうかを記録して、結果を開いた後に報告に並べる。値だけが許容の外で札が同じときは止めずに逸脱の台帳に記す（裁定 D234）。札は、v̂ の行の割合をその道の値で出し直し、主の行すべてに掛け直した Holm の判定・等方の外の行の割合を決めた裾（上か下か・裁定 D232）・等方の外の行の効き目の側・二つ目の札。下見で外した升目の行は比べない",
  "print": "器は段ごとに一致か不一致かだけを印字し、値は開かない。差の最大は、結果を登録者と一緒に開いた後に報告に並べる",
  "on_mismatch": "どちらかの段が一致しなければ（二段目は札の一致で見る・裁定 D234）、結果を開く前に止め、逸脱の台帳に記して登録者に上げる（裁定 D219）",
  "reextract": {
   "rel_tol": 1e-05,
   "cos_min": 0.99999,
   "forwards": 16,
   "path": "本の抽出と同じ読み込みの設定・同じ注意の実装と決定性の設定・バッチ一・bf16 で、違うのは活性を取り出す書き方だけ（T22）",
   "rule": "書き手は抽出の文脈を自分の道で流し、‖h‖・‖v̂‖ の相対の差 `independent_recompute.reextract.rel_tol` 以内・名前のある方向の余弦 `independent_recompute.reextract.cos_min` 以上を許容として（下見の前に凍結・案 22・D265）突き合わせ、外れたら一段目と同じく結果を開く前に止める"
  },
  "nk_decision": "一段目に Nk の行を入れるかは、凍結の前にバッチ一の速さを意味のない列で測ってから（値を見ない）、費用とあわせて登録者が決める（案 16・D263）",
  "interfaces": {
   "rewrite": "`bprime_recompute_rewrite.recompute_rewrite(model, tok, C, ledger, dirs, names, pilot, coef)` → 行の名 → {\"noop_lo\": 無操作の対数オッズ, \"effects\": {\"方向の名|符号\": 効き目}}（行と方向の組は層三の `bl3_core.recompute_set` と同じ・本の器のフックの道と同じ形）",
   "reextract": "`bprime_reextract.reextract(model, contexts, layer_idx)` → 文脈の名 → 選んだ層の出力の主位置の値（凍結の前の確かめ）・`bprime_reextract.reextract_all(model, tok, C, ledger, dirs)` → {\"h_norm_by_context\": {文脈: ‖h‖}, \"vhat_norm\": ‖v̂‖, \"named_cos\": {名: 抽出の npz の名前のある方向との余弦}}",
   "who": "書き手と別の新しい個体（エージェント一体・Claude Opus 5.5・系統内・D270）が、正本・草案・台帳・凍結の器と transformers の Gemma 4 の実装だけを読んで書く。二つの道は本の器の関数（`bprime_run`・`bprime_directions`）を呼ばず、突き合わせの確かめ（`--dry`）でだけ公開の口で呼ぶ（中は読まない）。指示の全文は `Bprime/tools/independent/instructions-rewrite-reextract-Bprime.txt`（SHA16 は `inputs.files_internal.instructions_independent`）"
  }
 },
 "layers": {
  "ratio": 0.5,
  "index": 29,
  "hidden_states_index": 30,
  "rule": "段階 B の式 `direction_B.layer_index`（割合の層）",
  "layer_type": "full_attention",
  "layer_path": "model.language_model.layers",
  "path_rule": "層の道の解決は B′ の器だけで行い、起動器は凍結の器の SHA と、読み込んだ後の属性が変わっていないことを確かめる（R38）",
  "window_assert": "列の長さ ＜ 窓（`inputs.model_facts.sliding_window`）を起動器が assert し、転記行 F に入れる（R12）",
  "type_note": "選ぶ層の種類（`layers.layer_type`）を選んだのは割合の式で、種類で選んだのではない（限界）"
 },
 "readout": {
  "primary": {
   "name": "甲（直答の型の読み取り）",
   "rule": "段階 B の組み立てのプロンプトに Gemma のチャットの型（user の発話一つ・system なし・生成の口つき）を当てた直後に、層三と同じ文字列の書き出しを教師強制で置き、次のトークンの出口の値を全経路の後に読む",
   "prefix_text": "```json\n{\"choice\": \"",
   "prefix_ids": [
    2717,
    3723,
    107,
    14937,
    17005,
    1083,
    623
   ],
   "prefix_pieces": [
    "```",
    "json",
    "\n",
    "{\"",
    "choice",
    "\":",
    " \""
   ],
   "prefix_source": "層三の主の書き出しと同じ文字列（プロンプトの中の JSON の指示の雛形の頭）を Gemma のトークナイザで割ったもの。出所は層三と違う（層三は段階 B の出力の実物の共通の頭・B′ は雛形の頭・案 1・R04）",
   "ledger_checks": "各々の文字を足しても割り方が変わらない・プロンプトの文字列に書き出しを足して割っても同じ並び・書き出しの並びがプロンプトの中の雛形にある・自然な続きと雛形の続きを割ったとき書き出しの直後の片が読み取りの集合の単独の文字（refuse は「ref」）。外れたら凍結の前に登録者に上げる（R07）",
   "letters": {
    "survival": [
     "a",
     "b",
     "c"
    ],
    "nuclear": [
     "a",
     "b",
     "c",
     "d"
    ]
   },
   "letters_by": "場面の族（凍結の場面の記録の `family`）",
   "refuse_head": "ref",
   "catastrophe_letter": "a",
   "set_ids": {
    "a": 236746,
    "b": 236763,
    "c": 236755,
    "d": 236753,
    "refuse": 1811
   },
   "quantity": "選択肢 a の文字の対数オッズ——z_a − logsumexp（ほかの選択の文字と refuse の頭の出口の値）。出口の値は、最終の正規化と語彙の行列を当てた後に、模型の出口と同じ softcap（cap × tanh(z ÷ cap)・`text_config` の `final_logit_softcapping`）を掛けた値。読んだ softcap の値と読んだ階層を転記行 F に印字する。温度も切り詰めも掛けない。効き目＝加えた腕の値 − 無操作の値（R05）",
   "main_position": "組み立て済みの列の最後のトークン（段階 B の式）。Gemma では空の思考の欄の閉じ（`<channel|>`・R03）",
   "readout_position": "列の最後（主位置 ＋ 書き出しの長さ）",
   "band": "加減は主位置から読み取りの位置まで",
   "band_why": "層三の位置の範囲と行の形にそろえるため（Gemma の行動から来た選びではない）。この理由では、Gemma が自由に生成するときの決定には届かない（R03）",
   "precision": "順伝播と加減は bf16。最終の正規化の入力を前のフックで取り、`float32` に上げて正規化・語彙の行列・softcap を `float32` で当てる（`bprime_run`）",
   "batch": 16,
   "order_seed": 92002,
   "batching": "バッチの大きさと組み方は層三と同じ（層三の `readout.primary.batching`）。方向の並びは `readout.primary.order_seed` の種で混ぜる（案 7）。下見の (vi) の (a) が上限を超えたら、本の計算はバッチの大きさを一にする。近道は使わない",
   "contexts": "升目（場面 × 土台の腕）ごとに文脈は一つ（標本化の揺れが無い）",
   "no_change_after_pilot": "下見の後に書き出しを替えない（替えるなら新しい登録・R04）",
   "rejected_alt": "行動の下見で Gemma が出した JSON の出力から、先に凍結した機械の決まりで書き出しを選ぶ案は採らない（案 12・D263）",
   "weakness": [
    "直答の型の書き出しを、空の思考の欄の直後に教師強制で置く。Gemma が自分でこの形を選ぶかは分からない（行動の下見で件数だけを数える）",
    "書き出しは Gemma の出力から取っていない（雛形の頭・R04）",
    "書き出しはプロンプトの中の雛形の頭と同じ並びで、雛形ではその次が a（破局の側の選択肢）。写しの働きが入りうる（層三と同じ）",
    "層三と B′ で、書き出しの割り方は同じ形（七つの片）だが、トークンは別もの",
    "softcap は大きな出口の値を縮める（傾きは出口の値が大きいほど小さい）。効き目と揺れの広さの尺度は、層三の対数オッズとそろわない（R02・R26）",
    "選ぶ層の種類は `layers.layer_type` で、ほかに窓つきの層がある（`inputs.model_facts`）。読み取りの列は窓の内にある（転記行 F で assert・R12）"
   ]
  },
  "variants": {
   "V1": "書き出しからコードブロックの行（最初の行）を除いたもの",
   "V2": "書き出しの選択の鍵の前に改行と字下げを入れたもの（複数行の JSON）",
   "V3": "書き出しの選択の鍵の後の空白を除いたもの（雛形との一致の最後のトークンだけを崩した版・頭の並びは雛形と同じ）",
   "rule": "揺れの版は下見の (iv) の記述にだけ使う。選択の文字が一つのトークンに割れない版は落とす。版の割り方は転記行 A に器が印字する。V3 は、頭の並びが主の書き出しと同じで最後の片だけが違い、版の並びと版の最後のトークンがプロンプトの中に現れないことを器が確かめ、満たさなければ機械で落として転記行 A に印字する。層三の「版の形が段階 B の出力に無い」の確かめは置かず、行動の下見の頭の振り分けで V3 の形が現れた件数を転記行 C に記述として印字する（R08・S06）",
   "strings": {
    "V1": "{\"choice\": \"",
    "V2": "```json\n{\n  \"choice\": \"",
    "V3": "```json\n{\"choice\":\""
   },
   "strings_rule": "主の書き出しから層三の定義どおりに器が作り（`bprime_core.variant_strings`）、層三の転記行 A の三つの文字列と一字違わず同じことを、正本を組む器が確かめた（器の段の所見 K3）"
  }
 },
 "directions": {
  "named": [
   "static",
   "loaded",
   "Nk",
   "td"
  ],
  "defs": {
   "static": "v̂＝h_O − h_Osec（確証族の方向）",
   "loaded": "(6b)＝h_{O-Ncold} − h_{Osec-Ncold}（S4 の反証）",
   "Nk": "h_Nk − h_N（交差族）",
   "td": "h_Onull − h_N（腕対の差方向の統制）"
  },
  "norm_rule": "各層で、係数を掛ける前の ‖v̂〔static〕‖ に合わせる（B と同じ・裁定 D75・D90）。全経路の効き目は足した量の大きさにも依るので、ノルムを揃えた方向どうしで比べる（違いは向きだけ）。",
  "extraction": {
   "arms": [
    "O",
    "Osec",
    "Onull",
    "Nk",
    "N",
    "O-Ncold",
    "Osec-Ncold",
    "Onull-Ncold"
   ],
   "scenes": [
    "N1",
    "S1"
   ],
   "contexts": 16,
   "position": "主位置（組み立て済みの列の最後のトークン・Gemma では `<channel|>`）の、選んだ層の出力（`layers[k]` の出力をフックで取る）",
   "no_readout": "相 extract の器は、選んだ層より後を流さない（選んだ層の出力で止め、出口の値を作らない）ことを assert にし、合成データで確かめる（S26）",
   "dim_assert": "等方の方向の次元が、抽出した活性の次元と一致することを assert する（R23）"
  },
  "storage": {
   "dtype": "float64",
   "rule": "名前のある方向・等方・実在の差・自己検査の一本を一つの npz（`float64`・時刻を持たない形）にまとめる。最初に書き終えた npz を拘束とする（やり直しは器の誤りの範囲に限り、二つの SHA を報告の頭に並べる）。npz そのものは公開の置き場に入れず、SHA を抽出の記録に置く。本の計算は npz を読み、SHA を確かめる（Colab で乱数を引き直さない・R22・S04）"
  }
 },
 "coefficient": {
  "rule": "係数＝層三の比 ÷（‖v̂‖ ÷ ‖h‖）。相 extract の後に器が出し、転記行 D に印字する。上下の限りを置かず、式の値をそのまま使う（案 2・D261・R13）",
  "bl3_ratio": "`layers.coef_applied`（層三）× 層三の凍結の活性から出し直した `vhat_over_h`（割合の層）。正本の丸めた値 `relative_injection_selected` は使わない",
  "bl3_coef_applied": 2.0,
  "h_norm_def": "‖h‖ は段階 B の `direction_B.h_norm_record` と同じ定義で、段階 B の正本の `arms.panel` × `extraction_scenarios` の文脈の、主位置の活性のノルムの平均（B′ も同じ文脈・R13）",
  "check_bl3": {
   "rule": "凍結の前の確かめで、B′ の係数の式を層三の凍結の活性（`inputs.files_public.Bl3_activations`）に当て、係数が `coefficient.bl3_coef_applied` と相対の差 `coefficient.check_bl3.rel_tol` の内で出ることを確かめる（S18）",
   "rel_tol": 1e-06
  },
  "check_B_record": {
   "rule": "B′ の器がその活性から出した ‖h‖ の平均と ‖v̂‖ が、段階 B の記録（`inputs.files_public.B_layers`）の割合の層の `h_norm_main`・`vhat_norm` と相対の差 `coefficient.check_bl3.rel_tol` の内で一致することを確かめる（比を同じ器で出し直すだけでは係数は作りの上で層三の値になり、‖h‖ の定義のずれを捕まえないため・T23）",
   "h_norm_main": 42.77571105957031,
   "vhat_norm": 1.3012276887893677
  },
  "finite_assert": "揃える前のすべての方向（名前のある方向・実在の差）のノルムが有限で零でないことを assert し、落ちたら器の誤りとして止める（値に依らない・S19）",
  "aligned": "そろうのは、注入のノルムの、抽出の文脈の平均 ‖h‖ に対する比だけ。帯の位置の押し・bf16 に丸めた後の実効の大きさ・softcap の後の尺度・自然の差に対する倍はそろわない（記述は転記行 D・R13・R14）"
 },
 "nulls": {
  "isotropic": {
   "count": 1999,
   "seed": 92001,
   "layer_key_scale": 1000,
   "rule": "凍結の前に、凍結の `blens_core.iso_directions` と同じ引き方（種と層の割合と次元）で、正規化の前の乱数 g のまま引き、g と種と層の割合と次元の SHA を下見の前の凍結の記録に入れる。相 extract では凍結の関数をそのまま呼んで等方の方向を作り、保存した g から同じ式（g × ‖v̂‖ ÷ ‖g‖）で作った値と相対の差 `nulls.isotropic.g_rel_tol` の内で一致することを確かめる（ビットの一致は求めない・S19）",
   "g_rel_tol": 1e-12,
   "low_bar": "偏りのある残差の中では、等方のランダム方向は低い棒で、等方の札だけでは「実在の差なら何でもそうなる」を退けられない（B-lens の限界の文）"
  },
  "real": {
   "arms": [
    "O",
    "Osec",
    "Onull",
    "Nk",
    "N",
    "O-Ncold",
    "Osec-Ncold",
    "Onull-Ncold"
   ],
   "pairs": 28,
   "swap_siblings": [
    "O~Osec",
    "O~Osec-Ncold",
    "Osec~O-Ncold",
    "O-Ncold~Osec-Ncold"
   ],
   "comparators": {
    "static": 24,
    "loaded": 24,
    "Nk": 27,
    "td": 27
   },
   "orientations": 2,
   "comparators_oriented": {
    "static": 48,
    "loaded": 48,
    "Nk": 54,
    "td": 54
   },
   "rule": "凍結の八腕の活性（抽出の場面の平均・選んだ層）の全ての対の差を作り、ノルムを揃える。v̂ と (6b) を比べる相手からは O と Osec の入れ替えを含む対（自分の対と兄弟の三対）を除き、Nk と td は自分の対だけを除く（B-lens と同じ除き方）",
   "orientation_rule": "比べる相手は、各々の対の差を両方の向き（足す向きと引く向き）で数える。B-lens は物差しが方向について線形で、|値| で比べれば両向きは何も足さなかった。全経路の効き目は方向の符号で反転する保証が無い（非線形）ので、対の名の並びで決まる向きに比べる相手を任せない",
   "combos": "各組は、その組の符号の向き（符号 × 方向）で実在の差の全ての対を流す。O-Ncold の二つの符号の組で両方の向きがそろう。Onull の組（符号は +1 だけ）には、逆の向きの全ての対を足す（R23・S20）",
   "onull_combos": 4,
   "reverse_extra": 112,
   "holm": false,
   "chance_second": 0.3087,
   "chance_second_pair": 0.6057,
   "chance_note": "二つ目の札には Holm を掛けない。主の行のどれかに偶然で付く数の目安を、向きまで数えた値（`chance_second`）と対の単位の値（`chance_second_pair`）の幅で、札の欄の注に印字する（効き目がほぼ奇なら対の単位の値に近い）。目安は、行が比べる相手と交換可能と仮定したときの付く数の期待で、一つ以上付く割合の上限でもある。行どうしは同じ方向を共有するので独立でない",
   "chance_rule": "層三の定数を倍率で使わない。残った行について、行ごとに 1 ÷（その行の比べる相手の数 ＋ 1）を足した値（向きまで数えた値）と、対の単位の値を、層三の `nulls.real.chance_note` の型で札の欄の注に印字する（R23）"
  },
  "self_check_direction": {
   "seed": 92003,
   "rule": "帰無に入らない新しい一本（等方と同じ作り方・この種）。最後の層の自己検査にだけ使う（R06）。転記行 D に等方・実在の差との余弦の最大を印字する"
  }
 },
 "computation": {
  "before_seal": {
   "rule": "封印の前の本物の模型の走りは、意味のない列だけで行い、印字してよい値を限って露出の記録に入れる（層三の `computation.before_seal` を書き直した・S02）",
   "meaningless": {
    "def": "場面の文・八つの腕の文・JSON の指示・主の書き出しと V1〜V3 の文字列のどれも含まない列（長さを升目にそろえること・チャットの型を当てることは許す）",
    "make": "凍結した種（`computation.before_seal.meaningless.seed`）から、特別なトークンと、場面・腕・指示・書き出しと揺れの版を割ったトークンを除いた語彙から一様に引く。戻した文字列が禁じた文字列を含まないことを器が assert する（T24）",
    "kinds": {
     "flat": "ランダムなトークンの列",
     "confident": "user の発話にランダムなトークンの塊を置き、`<channel|>` の後にその塊の頭の七つを置く列"
    },
    "seed": 92006,
    "record": "本数と長さを正本に置き（器の段）、列の SHA を露出の記録に入れる",
    "counts": {
     "n": 32,
     "lengths": [
      438,
      429,
      489,
      480,
      502,
      493,
      503,
      494
     ],
     "rule": "長さは主の八升目の列の長さ（プロンプトの長さ ＋ 書き出しの長さ）を正本の升目の順に並べたもの。長さごとに flat と confident の二種類 × 中身二つ。どちらの種類も、チャットの型の user の発話の所にランダムなトークンの塊を置き（型を一字の目印で組み、目印の番号の所に塊の番号を差し込む）、`<channel|>` の後に七つを置く（flat はランダムなトークン七つ・confident は塊の頭の七つ）（`bprime_meaningless`）"
    }
   },
   "allowed_runs": [
    "読み込み・版・重みの断片の SHA・設定の値の確かめ",
    "トークナイザだけの確かめと G4 の上での割り直し（場面の文は割るが模型には通さない）",
    "意味のない列での順伝播の確かめ（`computation.pre_freeze_checks`）",
    "意味のない列での生成の煙試験",
    "層三の凍結の活性に比の器を当てること",
    "小さな乱数の模型の合成データの確かめ"
   ],
   "may_print": [
    "合否",
    "許容の式に要る差と行の数（「あり」と出口の差の最大・「なし」「二重」との差の最小・区間の行の数を、出口の大きさの区間ごとに）と k（T04）",
    "速さと記憶と順伝播の回数",
    "版と SHA と設定と `generate` に渡った設定",
    "煙試験の止まった理由と生成したトークンの数と思考の欄を開くトークンが出たかの真偽と時間",
    "トークナイザの確かめの結果",
    "Qwen の比"
   ],
   "must_not_print": [
    "場面・腕・JSON の指示・書き出し・揺れの版を含む入力の値（その入力では順伝播そのものをしない）",
    "意味のない列でも出口の値そのもの",
    "上位のトークン",
    "読み取りの集合の文字の出口の値",
    "活性とそのノルム",
    "煙試験で生成した文の字",
    "バッチ一の繰り返しの差の大きさ（合否だけ）"
   ],
   "no_batch_diff": "バッチ 16 とバッチ一の差は下見の (vi)(a) の見込みになるので封印の前に測らない",
   "exposure": "印字した値は封印の前の露出の記録に入れる"
  },
  "self_checks": {
   "logit": {
    "rule": "同じ位置で、softcap あり・なし・正規化の二重の三つを `float32` で出し、模型の出口の値（bf16）と突き合わせる。「あり」は、掛けたすべての行で tol(z) の内であること。「なし」と「二重」は、式から出した見込みの差が tol(z) の `computation.self_checks.logit.discrimination_factor` 倍を超える行だけに掛け、その行の中の最大の差が tol(z) を超えることを求める（R05・S13・T04）",
    "tol_form": "tol(z) ＝ k × u(z)。z は模型の出口の値（softcap の後）。u(z) は |z| と z₀ の大きい方の bf16 の刻み（その数を bf16 で表したときの隣り合う二つの数の間隔）。k は凍結の前に意味のない列で測った〈差 ÷ u(z)〉の最大の `computation.self_checks.logit.tolerance_factor` 倍（T04・案 25・D267）",
    "z0": 4,
    "z0_fallback": 1,
    "tolerance_factor": 2,
    "discrimination_factor": 3,
    "top_rows": 64,
    "rows": "読み取りの集合の行と、その位置の全語彙で出口の値の大きい上位 `computation.self_checks.logit.top_rows` 行（案 25・D267）",
    "expected_diff": {
     "no_softcap": "r − cap·tanh(r/cap)（r は softcap の前の値）",
     "double_norm": "`float32` で正規化を二重にかけた道と正しい道の差"
    },
    "measure": {
     "positions": 32,
     "split": {
      "lengths": 8,
      "kinds": 2,
      "contents": 2
     },
     "kinds": [
      "flat",
      "confident"
     ],
     "batches": [
      16,
      1
     ],
     "rule": "意味のない列の最後の位置（八升目の読み取りの位置にそろえた長さ × 二種類 × 中身二つ）で、`computation.self_checks.logit.rows` と同じ選び方の行（意味のない列では読み取りの集合の五つ）について、二つのバッチの大きさの両方で測り、大きい方の k を使う（案 25・D267）",
     "asserts": {
      "big_z": 16,
      "big_z_rows_min": 32,
      "k_max": 16,
      "k_max_fallback": 64,
      "rule": "測った行のうち |z| が `computation.self_checks.logit.measure.asserts.big_z` 以上の行が `computation.self_checks.logit.measure.asserts.big_z_rows_min` 以上・k が `computation.self_checks.logit.measure.asserts.k_max` 以下（床 k × u(z₀) が層三の `computation.logit_tol` 以下）。大きい行が足りないときは、機械で z₀ を `computation.self_checks.logit.z0_fallback` に切り替えて k が `computation.self_checks.logit.measure.asserts.k_max_fallback` 以下を assert する。assert が落ちたら凍結しない（登録者に上げる）"
     },
     "bl3_logit_tol": 0.5
    },
    "no_discrimination": {
     "rule": "見分けに使える行が一つも無い位置では〈この位置では見分ける力が無い〉と印字し、器の誤りに数えず、止めずに続ける。その位置の数と定型の文（`computation.self_checks.logit.no_discrimination.sentence`）を報告の頭に器が置く。登録者には知らせるだけで、判断を求めない（T05）",
     "sentence": "softcap の抜けと正規化の二重を見分ける力が無い位置が 〔数〕 あった（見込みの差が許容の 3 倍を超える行が無かった）。その位置では「あり」の許容の内であることだけを確かめた",
     "main_head_print": [
      "合",
      "否",
      "見分ける力無し"
     ]
    },
    "where": "下見の頭と本の計算の頭で走らせ、本の計算の頭では合否と見分ける力の有無だけを印字する（S15・T05）"
   },
   "layer": {
    "rule": "帰無に入らない一本（`nulls.self_check_direction`）と零のベクトルで、層ごとの差分の最後の層の行（選択肢 a の文字の対数オッズの差）が読み取りの効き目と `computation.layer_tol` の内で一致することを、本の計算の頭で確かめる。合否だけを印字する（R06・S15）"
   },
   "on_fail": "落ちたら止める（凍結した確かめが機械で落ちたので器の誤りに当たる）"
  },
  "layer_tol": 0.0001,
  "logit_tol_bl3": 0.5,
  "pre_freeze_checks": [
   "実物の重みで、意味のない列: `float32` の正規化・語彙の行列・softcap を通した値と模型の出口（bf16）の差を測り、出口の値の自己検査の k を決める（`computation.self_checks.logit.measure`・R05・S13・T04）",
   "正規化の二重がけと softcap の抜けが落ちる",
   "選ぶ層でフックの出力と抽出が一致し、最後の層では `hidden_states` の最後と一致しない",
   "`Gemma4RMSNorm` が 1＋重みでない",
   "層の道が `model.language_model.layers`",
   "バッチ一の速さと、決定性の設定を入れたバッチ一の繰り返しの一致（同じセッションの中で同じ意味のない列を二度流し、読み取りの位置の全語彙の出口の値〔模型の出口の bf16〕がビットで一致すること・合否だけ・R40・T25）",
   "生成の煙試験（思考を出さない・同じ意味のない列を二度生成してトークンの並びが一致しない〔標本化が掛かる〕・止める印と `max_new_tokens` で止まる・生成の速さ・R17・S21）",
   "集めるフックが加減のフックより先に掛かった場合と後に掛かった場合で、抽出・加減・層ごとの取り出しの値が同じ（R37）",
   "加減のある順伝播で `output_hidden_states` を使わない assert",
   "長い走りで記憶の最大が伸びない",
   "生成の道の入力の BOS が一つ",
   "相 extract の器が選んだ層より後を流さない（S26）",
   "独立の再抽出の道（`independent_recompute.reextract.path`）を実物の重みの意味のない列で流し、許容に届くか（合否だけ・T22）",
   "G4 上で、升目・抽出の文脈・書き出しと揺れの版を割り直し、台帳と一致することを順伝播の前に確かめる（R37）",
   "トークナイザだけで: 台帳の自然な続きの確かめ（R07）・V3 の確かめ（R08）",
   "B′ の係数の式を層三の凍結の活性に当てる確かめ（`coefficient.check_bl3`・`coefficient.check_B_record`・S18・T23）",
   "等方の乱数 g を凍結の関数と同じ引き方で引き、凍結の関数の出力と `nulls.isotropic.g_rel_tol` の内で一致する（手元と Colab の NumPy で・S19）"
  ],
  "synthetic_checks": [
   "床の余白の印（層三の数で印が付く・付かない例も・R15・S25）",
   "両方の向きの組み方と比べる相手の数（重なりが無い・R23・S20）",
   "止める印が段階 B の値になっている誤りで器が止まる（R17）",
   "出口の値を cap の近くまで大きくした場合と、小さい値だけの場合（見分ける力の無い位置の印字）の自己検査（R05・S13）",
   "bf16 の丸めを模した道の自己検査（正しい実装が「あり」を通り、抜けと二重が落ちる・T04）",
   "窓を列より短くした小さな模型（R37）",
   "正規化の重みを 0 と 1 から離した値（R37）",
   "復号の設定と書き出しの根の件数の器（`behavior_pilot.root_counts.synthetic`・S06・T18）",
   "本の凍結の器（足してよい鍵の外が増えると止まる・SHA の違いで止まる・決定の出し直しの不一致で止まる・S01・T12）",
   "報告の組み立ての器（読みの表のすべての型・柵の文・下見で止めたときの添え書き・§0 の答えられないことで止まらずに組め、自由の文の禁止の語・「層三」「Qwen」・値の数で止まる・T07）",
   "要約の型の assert（T10）",
   "合成データの確かめを Colab の本の版でも走らせる（R37）"
  ],
  "tool_error": "本の計算の中で、凍結した確かめ（assert・SHA の検査・自己検査・合成データの確かめ）が機械で落ちたら、結果を開かずに止め、逸脱の台帳に記して登録者に上げる。直してやり直すかは登録者の裁定で、やり直したときは一度目の記録を報告の頭に並べる。やり直さないときは、結果を開かずに閉じ、「器の誤りで計算を終えられなかった」と記録する（予想は q1 だけを採点する）。下見の決まりと同じ型",
  "shortcut": "本の計算は近道（主位置より前の計算の使い回し）を使わない",
  "extraction_record": {
   "rule": "抽出の直後に、抽出の記録（転記行 D・npz の SHA・係数・g との一致の合否）を時刻つきで作り、公開の置き場に置く。人の操作は、できた記録を置き場に写す push だけで、中身を編集しない（push には登録者の確認を得るが、それは push の操作の確認で、中身の判断ではない・T01）",
   "form_items": [
    "公開した抽出の記録がそろい、転記行 D・npz の SHA・係数・g との一致の合否の欄がある",
    "公開した記録と手元の npz と正本と器と重みの断片の SHA が合う",
    "版のピンが文字列で完全に一致する",
    "凍結した確かめの合否がすべて「通った」（g との一致・揃える前のノルム・次元の一致・読み取りの値を作らないこと）",
    "時刻が封印の後で行動の下見の起動の前",
    "相 extract の起動の記録が一つで、抽出の記録が指す走行と同じ（二つあるときは器の誤りの記録がある）"
   ],
   "check": "行動の下見の起動器は、最初の順伝播の前に形の項目（`computation.extraction_record.form_items`）を機械で確かめ、そろえば進み、一つでも落ちれば器の誤りとして止める。起動器は値（‖v̂‖・係数・転記行 D の記述）を読まない。封印の後に人が「進まない」と決める道は置かない（記録を置かないまま日が過ぎたときは暦の期限で閉じる・T01）"
  },
  "start_records": {
   "stages": [
    "相 extract",
    "行動の下見",
    "読み取りの下見",
    "本の計算",
    "独立の再計算"
   ],
   "rule": "各段の起動器は、最初の順伝播の前に起動の記録（時刻・セッション・GPU の名・正本と器の SHA・段の名）を公開の置き場に置き、終わりに出力の SHA を置く（置くごとに push が一つ増え、push には登録者の確認を得る）。本の凍結の器と報告の組み立ての器は、段ごとの起動の記録の数と、報告の頭に並べる走行の数が一致することを確かめる（T13）"
  },
  "main_freeze": {
   "where": "決め（機械）の後、本の計算の前。効き目の順伝播は、本の凍結の記録ができるまで一つもしない（S01）",
   "allowed_keys": {
    "extraction": [
     "転記行 D",
     "npz の SHA",
     "係数",
     "g との一致の合否"
    ],
    "behavior_pilot": [
     "採点の器の SHA",
     "採点の出力の SHA",
     "生成したトークンの番号の列の SHA",
     "転記行 C"
    ],
    "readout_pilot": [
     "(i)〜(iv) と (vi) の (a)(b) の値",
     "(iii) の選んだ文と値と除いた升目の数",
     "外した升目と理由",
     "機械の決定",
     "本の計算のバッチの大きさ",
     "出口の値の自己検査の合否と見分ける力の有無",
     "読み取りの下見の起動の記録と出力の SHA"
    ],
    "tool_diffs": "逸脱の台帳に記した器の差分（`pilot.tool_error.scope` の直しの範囲に限る）"
   },
   "rule": "これら以外の鍵が増えたら器の誤りとして止める。読み取りの下見の起動器は、出力を時刻つきで書き、SHA を印字する（T12）",
   "checks": [
    "正本の SHA が下見の前の凍結から変わっていない",
    "器の SHA の違いがすべて台帳に記した差分（前と後の SHA）と一致する",
    "足した鍵が上の一覧の内である",
    "npz の SHA が公開した抽出の記録と一致する",
    "行動の下見の記録の SHA が公開した記録と一致する",
    "凍結した決定木の器を読み取りの下見の記録に当てて出し直した決定が記録の決定と一致する",
    "集計・札・読みの規則・報告の組み立ての器の SHA が下見の前の凍結のままである（違えば止める）",
    "段ごとの起動の記録の数が走行の記録の数と一致する"
   ],
   "lock": "本の計算の起動器は、公開の置き場の決めた版から本の凍結の記録を取り、公開の記録に印字された SHA と照らし、下見の前の凍結の正本の SHA を確かめてからでなければ順伝播しない。本の凍結の記録は、効き目の順伝播の前に時刻つきで公開の置き場に置く。本の凍結のやり直しは器の誤りのときに限り、二つの記録を報告の頭に並べる（T12）",
   "bl3_rule": "本の凍結で許すのは、下見の記録と機械の決定を凍結の記録に足すことと、逸脱の台帳に記した器の差分だけ。凍結の器は、正本の SHA が下見の前の凍結から変わっていないこと、器の SHA の違いがすべて台帳に記した差分（前と後の SHA）と一致すること、足したのが下見の記録の鍵だけであることを確かめる。正本を変える直しはこの決まりの外で、登録者に上げる（裁定 D222）"
  },
  "open_results": "本の計算の起動器は値も札も印字しない。独立の再計算の二段と独立の再抽出がすべて一致してから、結果を登録者と一緒に開く（T13）",
  "stops": {
   "machine_only": "封印の後は、機械の止め（器の誤り・下見の止め・G4 の期限・暦の期限）のほかでは止めない。人が値を見て止める道は置かない。止めたときは、そこまでの記録をすべて公開の置き場に置く（S04・T01・T03）",
   "g4": {
    "days": 7,
    "rule": "起点は、封印の後に G4 の割り当てに最初に失敗した時。数えるのは、日本時間の暦日のうち、試みを記録し、その日に G4 が一度も割り当てられなかった日だけ（その日の試みの数に依らず 1 日・一日一回で足り、時刻の間隔は置かない）。G4 が割り当てられた日と、試みの無い日は数えない。段をまたいで通算し、G4 が得られても数え直さない（案 22・D265・T02）。数えた日が `computation.stops.g4.days` に達したら閉じ、その後に G4 が得られても開き直さない",
    "record": "試みごとに時刻・試みた人・画面に出た GPU の名か失敗の表示を記録し、画面の写しの SHA を添える",
    "close_sentence": "計算の道を保てず終えられなかった"
   },
   "calendar": {
    "days": 60,
    "rule": "封印から `computation.stops.calendar.days` 暦日（日本時間）の内に本の計算と独立の再計算を終えなかったら、G4 の期限とは別の機械の止めとして閉じる（先に来た方で閉じる・案 24・D267・T03）。どちらで閉じたときも、同じ登録の中で再び始めない",
    "close_sentence": "封印から 〔60〕 暦日の内に本の計算を終えられなかったので、この登録を閉じた。最後に終えた段は 〔段〕 で、そこまでの記録はすべて公開の置き場にある。B′ の問いには答えていない",
    "count": "封印の日（日本時間）を 0 日目とし、`computation.stops.calendar.days` 日目の日本時間の暦日の終わりまでに本の計算と独立の再計算を終えなければ閉じる（案 24 の中身は変えない・器の段の所見 K2・D270 で登録者が確認した）"
   },
   "q_scoring": "q1 は読み取りの下見の機械の決定が出たときに採点する（器の誤りでやり直したときは、やり直した下見の決定で採点し、一度目の決定を併記する）。機械の決定が出る前に閉じたとき（G4 の期限・暦の期限・抽出や行動の下見や読み取りの下見の器の誤りでやり直さないとき）は採点しない。q2〜q4 は本の計算が終わり、結果を開いたときに採点する（S11・T16）"
  },
  "human_decisions": {
   "list": [
    "器の誤りのやり直しの裁定（`pilot.tool_error.decide`・`computation.tool_error`）",
    "独立の再計算の不一致の裁定（`independent_recompute.on_mismatch`）"
   ],
   "rule": "封印の後に登録者の判断が入る所は、この二つだけ。判断ごとに時刻・見ていた記録・理由を公開する（T29）"
  },
  "frozen_text": {
   "tool": "`make_frozen_Bprime.py`（草案を逐語複製し、題名の印・凍結の一行・§6 の転記行の記録だけを改める）",
   "number_binding": "「原稿の数を正本の鍵で束ねる」は、B′ の草案が正本の鍵から組む原稿を持たないので、凍結の本文のすべての数（§6 と凍結の一行を除く）が正本の数値の葉か配列の長さに当たることを、B′ の数の検査の包み（`bprime_numbers_lint`・凍結した `numbers_lint.py` の登録検査）で確かめることとする（未登録が零でなければ止める・D271）",
   "diff_rule": "凍結の本文から題名の印・凍結の一行・§6 の足した節を外すと、草案と字のまま同じ（器が確かめ、差の記録に並べる）"
  }
 },
 "main_rows": [
  {
   "id": "sub:N1:O-Ncold-v~O-Ncold-vrand",
   "family": "B_sub",
   "scenario": "N1",
   "arm": "O-Ncold-v",
   "base": "O-Ncold",
   "sign": -1,
   "direction": "static"
  },
  {
   "id": "sub:S1:O-Ncold-v~O-Ncold-vrand",
   "family": "B_sub",
   "scenario": "S1",
   "arm": "O-Ncold-v",
   "base": "O-Ncold",
   "sign": -1,
   "direction": "static"
  },
  {
   "id": "sub:SK:O-Ncold-v~O-Ncold-vrand",
   "family": "B_sub",
   "scenario": "SK",
   "arm": "O-Ncold-v",
   "base": "O-Ncold",
   "sign": -1,
   "direction": "static"
  },
  {
   "id": "sub:S4:O-Ncold-v~O-Ncold-vrand",
   "family": "B_sub",
   "scenario": "S4",
   "arm": "O-Ncold-v",
   "base": "O-Ncold",
   "sign": -1,
   "direction": "static"
  },
  {
   "id": "add:N1:Onull+v~Onull+vrand",
   "family": "B_add",
   "scenario": "N1",
   "arm": "Onull+v",
   "base": "Onull",
   "sign": 1,
   "direction": "static"
  },
  {
   "id": "add:S1:Onull+v~Onull+vrand",
   "family": "B_add",
   "scenario": "S1",
   "arm": "Onull+v",
   "base": "Onull",
   "sign": 1,
   "direction": "static"
  },
  {
   "id": "add:SK:Onull+v~Onull+vrand",
   "family": "B_add",
   "scenario": "SK",
   "arm": "Onull+v",
   "base": "Onull",
   "sign": 1,
   "direction": "static"
  },
  {
   "id": "add:S4:Onull+v~Onull+vrand",
   "family": "B_add",
   "scenario": "S4",
   "arm": "Onull+v",
   "base": "Onull",
   "sign": 1,
   "direction": "static"
  },
  {
   "id": "cross:N1:O-Ncold+vNk~O-Ncold+vrand",
   "family": "B_cross",
   "scenario": "N1",
   "arm": "O-Ncold+vNk",
   "base": "O-Ncold",
   "sign": 1,
   "direction": "Nk"
  },
  {
   "id": "cross:N1:Onull+vNk~Onull+vrand",
   "family": "B_cross",
   "scenario": "N1",
   "arm": "Onull+vNk",
   "base": "Onull",
   "sign": 1,
   "direction": "Nk"
  },
  {
   "id": "cross:S1:O-Ncold+vNk~O-Ncold+vrand",
   "family": "B_cross",
   "scenario": "S1",
   "arm": "O-Ncold+vNk",
   "base": "O-Ncold",
   "sign": 1,
   "direction": "Nk"
  },
  {
   "id": "cross:S1:Onull+vNk~Onull+vrand",
   "family": "B_cross",
   "scenario": "S1",
   "arm": "Onull+vNk",
   "base": "Onull",
   "sign": 1,
   "direction": "Nk"
  },
  {
   "id": "cross:SK:O-Ncold+vNk~O-Ncold+vrand",
   "family": "B_cross",
   "scenario": "SK",
   "arm": "O-Ncold+vNk",
   "base": "O-Ncold",
   "sign": 1,
   "direction": "Nk"
  },
  {
   "id": "cross:SK:Onull+vNk~Onull+vrand",
   "family": "B_cross",
   "scenario": "SK",
   "arm": "Onull+vNk",
   "base": "Onull",
   "sign": 1,
   "direction": "Nk"
  },
  {
   "id": "cross:S4:O-Ncold+vNk~O-Ncold+vrand",
   "family": "B_cross",
   "scenario": "S4",
   "arm": "O-Ncold+vNk",
   "base": "O-Ncold",
   "sign": 1,
   "direction": "Nk"
  },
  {
   "id": "cross:S4:Onull+vNk~Onull+vrand",
   "family": "B_cross",
   "scenario": "S4",
   "arm": "Onull+vNk",
   "base": "Onull",
   "sign": 1,
   "direction": "Nk"
  }
 ],
 "cells_main": [
  [
   "N1",
   "O-Ncold"
  ],
  [
   "N1",
   "Onull"
  ],
  [
   "S1",
   "O-Ncold"
  ],
  [
   "S1",
   "Onull"
  ],
  [
   "S4",
   "O-Ncold"
  ],
  [
   "S4",
   "Onull"
  ],
  [
   "SK",
   "O-Ncold"
  ],
  [
   "SK",
   "Onull"
  ]
 ],
 "cell_signs_main": [
  [
   "N1",
   "O-Ncold",
   -1
  ],
  [
   "N1",
   "O-Ncold",
   1
  ],
  [
   "N1",
   "Onull",
   1
  ],
  [
   "S1",
   "O-Ncold",
   -1
  ],
  [
   "S1",
   "O-Ncold",
   1
  ],
  [
   "S1",
   "Onull",
   1
  ],
  [
   "S4",
   "O-Ncold",
   -1
  ],
  [
   "S4",
   "O-Ncold",
   1
  ],
  [
   "S4",
   "Onull",
   1
  ],
  [
   "SK",
   "O-Ncold",
   -1
  ],
  [
   "SK",
   "O-Ncold",
   1
  ],
  [
   "SK",
   "Onull",
   1
  ]
 ],
 "labels": {
  "p_rule": "両側に等しい裾の割合: 帰無の上の裾の割合 `(1 + #{null >= m}) / (1 + K)` と下の裾の割合 `(1 + #{null <= m}) / (1 + K)` の小さい方の二倍（一を上限・K は帰無の本数・B-lens の語の側の帰無と同じ数え方・`blens_core.p_equal_tailed`）",
  "p_rule_why": "B-lens の等方の帰無は、物差しが方向について線形なので零を中心に対称で、`(1 + #{|null| >= |m|}) / (1 + K)` を使えた。全経路の効き目は非線形で、同じ大きさの押しでも向きを問わず一方に寄りうる（帰無の中心が零からずれうる）ので、零を中心に対称な帰無を仮定しない",
  "iso_outside": {
   "holm_alpha": 0.05,
   "rule": "主の行に Holm を掛け、p が段を下回る行を「等方の外」とする（段の数は、下見で外した後の主の行の数）"
  },
  "second": {
   "rule": "その行の効き目と、比べる相手（実在の差の方向・両方の向き・同じ升目）の効き目の中央値との差の絶対値が、比べる相手の効き目と同じ中央値との差の絶対値のすべてを上回るとき「最上位」（同じ値は上回らないとみなす）。比べる相手の集まりは升目ごとに一つで、符号に依らない（裁定 D213）",
   "center_why": "v̂ も Nk も実在の活性の差（抽出の対の差）で、比べる相手と同じ類の方向なので、同じ類の中心（比べる相手の中央値）で比べる。等方の帰無の中央値は添えて印字する。B-lens は物差しが線形で、中心は零だった",
   "ranks": "順位は二つを印字する: 向きまで数えた比べる相手（両方の向き）の中の順位と、対の単位の順位。対の単位では、各々の対の両方の向きの効き目のうち、中心からの距離（差の絶対値）の大きい方をその対の値とし、行の中心からの距離をその値の中で順位づける。行は一つの符号だけで比べるので、対の単位の順位は行に不利な側に寄る（限界・採否表 P682）",
   "iso_top_share": "同じ升目と符号の等方の方向のうち、同じ中心と同じ比べる相手で「最上位」の条件を満たす割合を、行ごとに並べる。これは二つの帰無（等方の方向と実在の差の方向）の広がりの比べで、行の偶然の目安ではない。偶然の目安は `nulls.real.chance_note` の幅だけ（順伝播は増えない・採否表 P683）",
   "call": "最上位の判定は、行の値と比べる相手の値からそれぞれ中心を引いてから比べる（B-lens の芯の `top_rank` は零を中心に比べるので、中心を引いた値を渡すか、同じ式の新しい関数を書く）"
  },
  "side_rule": "等方の外の行は、等方の帰無の中央値と、効き目の側を添えて書く。側は三つ: 中央値と同じ向きで中央値より零から遠い〔同じ向きで、ランダム方向より強い押し〕・零と中央値の間〔同じ向きで、ランダム方向より弱い押し〕・零を越えて中央値と反対の向き〔ランダム方向と逆の向きの押し〕。零が等方の帰無の下の四分位と上の四分位の間にあるときは、中央値を零とみなし、効き目の符号だけを書く（採否表 P684）",
  "print_rule": "二つの札は別々に印字する。両方付いたときの言い方は「等方のランダム方向と区別でき、実在の差の方向（兄弟を除く）の中で中心からの動きが最上位」。どの行にも、等方の帰無の中央値・効き目の側・p と裾の本数（上の裾と下の裾）・二つ目の札の中心と順位を添える。二つ目の札は中心からどちらの側に離れたかを言わないので、行の値・中心・効き目の側と、等方の最上位の割合（`labels.second.iso_top_share`）を札の隣に並べる（採否表 P686）"
 },
 "pilot": {
  "when": "本の凍結の前・無操作の腕だけ・方向は一本も足さない。下見の手順と止める条件は、下見の前の凍結で正本ごと凍結し、予想を封印してから下見をする（層三の型）",
  "thresholds_note": "閾値は層三の正本 `pilot` と同じ値を写した。Qwen・L4・transformers 4 の層三の登録で決めた値で、Gemma で較正していない（値を見る前に較正の材料が無い・R09）",
  "mass_min": 0.9,
  "p_bounds": [
   0.0001,
   0.9999
  ],
  "variant_flag": 1.0,
  "noise_max": 0.01,
  "repeat_n": 3,
  "checks": {
   "i": {
    "name": "読み取りの形",
    "rule": "読み取りの位置の、選択の文字と refuse の頭の確率の和（全語彙の生の softmax・温度も切り詰めも掛けない）が `pilot.mass_min` 以上",
    "stop": true,
    "full_vocab": "全語彙は模型の出口の全ての行で、トークナイザの外の行を含む（裁定 D235）"
   },
   "ii": {
    "name": "床と天井",
    "rule": "選択の文字と refuse の頭の中での選択肢 a の文字の確率（生の softmax から）が、`pilot.p_bounds` の間",
    "stop": true
   },
   "iii": {
    "name": "較正（記述）",
    "rule": "無操作の読み取りの選択肢 a の文字の確率（生の値・`generate` と同じ処理の並びの変換を通した値も添える）と、行動の下見の Gemma の無操作の主の率を、升目ごとに並べる。升目の間の順位相関（Spearman・同じ値は平均の順位）を生の値で計算し、相関の値と升目の数を印字する。行動の下見を閉じた後に、決めの前に一度だけ計算する（R18）。読み取りの下見で外した升目は除き、除いた数を並べる（S11）。文は `pilot.iii_sentences` から器が選び、報告の §0 に置かず、読み取りの下見の記録の節（主の札の隣）に置く（T14）",
    "stop": false,
    "transformed_def": "変換を通した値は、全語彙の出口の値に `generate` が掛けるのと同じ処理の並び（段階 B の標本化の値）を当てた後の選択肢 a の文字の確率で、選択の文字と refuse の頭の中で割り直さない。合成の分布で標本の頻度と突き合わせる（S21）"
   },
   "iv": {
    "name": "書き出しの揺れへの強さ（記述）",
    "rule": "揺れの版（`readout.variants`）で、無操作の選択肢 a の文字の対数オッズが、主の書き出しから `pilot.variant_flag` を超えて動く升目に印を付ける。V3（雛形との一致の最後のトークンだけを崩した版）の値は並べるだけで、写しの働きの有無の読みを付けない（読みの表の「揺れの版の値」・裁定 D220）",
    "stop": false
   },
   "vi": {
    "name": "数値の揺れ（バッチの違いと、バッチ一の繰り返し）",
    "path": "本の計算のフックの道（近道なし）に、方向は足さず零のベクトルの無操作を流す",
    "a": {
     "name": "バッチの違いの揺れ",
     "rule": "升目ごとに、零のベクトルだけで満たした `readout.primary.batch` の大きさのバッチ（バッチの中の全ての位置）と、大きさ一のバッチを流し、対数オッズの最大と最小の差を取る。升目の間の最大が `pilot.noise_max` を超えたら、本の計算はバッチの大きさを一にし、下見の (i)〜(v) もバッチ一の出力で計算する（(vi) を先に測るので、裁定 D221 の「バッチ一の出力でやり直す」は、はじめからバッチ一の出力で計算する形になる）",
     "stop": false
    },
    "b": {
     "name": "バッチ一の繰り返しの揺れ",
     "rule": "升目ごとに、大きさ一のバッチを `pilot.repeat_n` 回流し、対数オッズの最大と最小の差を取る。升目の間の最大が `pilot.noise_max` を超えたら止め、「数値が定まらず測れなかった」と記録して閉じる（裁定 D221）",
     "stop": true
    },
    "floor_rule": "本の計算のバッチの組み方に合わせる（バッチの大きさが `readout.primary.batch` のままなら (a) の升目の間の最大、バッチ一に移ったら (b) の升目の間の最大）",
    "measures": "(a) が主に測るのはバッチの大きさの違いで、同じ入力を並べたバッチの中の位置の違いは小さいと見込まれる。方向の混ざったバッチでの揺れは、独立の再計算の二段目で見る。環境（GPU・版）の違いの揺れは測らない"
   }
  },
  "no_v": "(v)（近道の差）は置かない（近道を使わない・案 5 の型の表の行）",
  "order": "出口の値の自己検査（`computation.self_checks.logit`）→ (vi) → (i)(ii)(iv)。自己検査が落ちたら (vi) を計算しない（S14）。(vi) の (b) で止めたときは (i) 以後を計算しない。(iii) は行動の下見を閉じた後、決めの前に一度だけ計算する。無操作の値は層三の `pilot.order` と同じ取り方",
  "iii_sentences": {
   "positive": "無操作の読み取りの選択肢 a の文字の確率（生の値）と、行動の下見の無操作の主の率（升目ごとの試行は 40・行動の下見の率は凍結の採点器の出力で、その妥当性は Gemma の応答で確かめていない）の、升目の間の順位相関は正の側だった（相関の値と升目の数を並べる・升目の数は少なく、記述）。読み取りの値を行動の下見の率の代わりに読まない",
   "not_positive": "無操作の読み取りの選択肢 a の文字の確率（生の値）と、行動の下見の無操作の主の率（升目ごとの試行は 40・行動の下見の率は凍結の採点器の出力で、その妥当性は Gemma の応答で確かめていない）の、升目の間の順位相関は正の側ではなかった（相関の値と升目の数を並べる・升目の数は少なく、記述）。読み取りの値を行動の下見の率の代わりに読まない",
   "undefined": "無操作の読み取りの選択肢 a の文字の確率（生の値）と、行動の下見の無操作の主の率（升目ごとの試行は 40・行動の下見の率は凍結の採点器の出力で、その妥当性は Gemma の応答で確かめていない）の、升目の間の順位相関は定まらなかった（どちらかの値がすべての升目で同じ・升目の数を並べる）。読み取りの値を行動の下見の率の代わりに読まない"
  },
  "iii_fail_sentences": {
   "tool_error": "較正できなかった",
   "unscorable": "採点が定まらず較正できなかった"
  },
  "decision": {
   "cells": "主の行の土台の升目（場面 × 土台の腕）",
   "cells_total": 8,
   "cells_min_pass": 6,
   "rule": "(vi) の (b) の揺れが上限の内で、(i) と (ii) を満たす升目が `pilot.decision.cells_min_pass` 以上なら続ける。満たさない升目の主の行は、下見の前に決めたこの規則で機械が外し、外した行と理由を記録する。満たす升目が足りなければ止め、「この読み取りでは測れなかった」と記録して閉じる。(vi) の (b) の揺れが上限を超えたら止め、「数値が定まらず測れなかった」と記録して閉じる",
   "family": "nuclear の族（N1 の升目）が二つとも外れても続け、報告の頭に「nuclear の族は測れなかった」と書く（裁定 D214）",
   "q1_map": {
    "続ける": "主の升目がすべて (i)(ii) を満たし、(vi) の (b) の揺れが上限の内にある",
    "一部の升目を外して続ける": "満たす升目が `pilot.decision.cells_min_pass` 以上で、すべてではなく、(vi) の (b) の揺れが上限の内にある",
    "止める": "満たす升目が `pilot.decision.cells_min_pass` に満たないか、(vi) の (b) の揺れが `pilot.noise_max` を超える（裁定 D221）"
   },
   "after_stop": "止めたときに別の読み取りを立てるなら、新しい登録として、自分の封印と下見と検分の巡を持って立てる（この登録の中では立てない・止まり方を見た後の分かれ道を作らないため）",
   "reuse": "下見のデータは本の結果に使わない（本の計算で無操作の値を計算し直す・追補 D の型）"
  },
  "decision_more": {
   "stop_note": "止めの記録には「閾値は層三の登録の値を写したもので、Gemma で較正していない」を添える（R09）",
   "drop_effects": "外した升目の行は主の札から外す。Holm の段・偶然の目安・予想の q2〜q4 の数は、残った行で数え直し、分母を印字する",
   "vi_branch": "(vi) の (a) の升目の間の最大が `pilot.noise_max` を超えたら、本の計算はバッチの大きさを一にし、(i)〜(iv) もバッチ一の出力で計算する。移った後の本の計算の揺れの床は (b) の升目の間の最大。この分岐は q1 の三択の外の機械の事象として転記行に印字する（R19）",
   "behavior_not_used": "行動の下見は決めに使わない（記述）",
   "report": "続けたときも止めたときも、計算した下見の記録（(i)〜(iv) と (vi) の値・(vi) の (a) と (b) の値・(iii) の選んだ文と値と除いた升目の数・外した升目と理由・機械の決定・バッチの大きさ・揺れの床・出口の値の自己検査の合否と見分ける力の有無）を報告に並べる（主の札の隣）"
  },
  "tool_error": {
   "what": "器の誤りは、凍結した確かめ（assert・SHA の検査・自己検査・合成データの確かめ）が機械で落ちたものに限る。値の見え方から疑っただけでは器の誤りに数えず、下見を止めずに機械の決定まで出し、疑いを登録者に上げる（R20）",
   "decide": "どちらのときも、直してやり直すかは登録者の裁定（封印の後に登録者の判断が入る所の一つ・`computation.human_decisions`）",
   "rerun": "やり直すときも封印はそのままで、一度目の記録と機械の決定を報告の頭に並べ、q1 はやり直した下見で採点し一度目の決定を併記する。やり直さないときは q1 を採点せず、「器の誤りで下見を終えられなかった」と記録して閉じる（層三の D222・D225 の型）",
   "scope": "直しの範囲は、環境・SHA・フックの付け外しに限る。読み取りの式・softcap・正規化・読み取りの集合・係数の式・書き出しは直しの対象外（変えるなら新しい登録）。相 extract と行動の下見のやり直しも同じ範囲に限る（S04）"
  },
  "value_seen_change": "抽出と下見の値を見た後に、閾値・係数の式・行の形・書き出し・読み取りの集合を変えることは、この登録を閉じる逸脱とする（静かに続けない）。止めたときに別の読み取りを立てるなら、新しい登録として立てる（R18）"
 },
 "inputs.model_facts": {
  "num_hidden_layers": 60,
  "hidden_size": 5376,
  "vocab_size": 262144,
  "final_logit_softcapping": 30.0,
  "softcap_level": "text_config",
  "sliding_window": 1024,
  "full_attention_layers": 10,
  "eos_token_id": [
   1,
   106,
   50
  ],
  "bos_token_id": 2,
  "pad_token_id": 0
 },
 "inputs.versions": {
  "transformers": "5.16.1",
  "torch": "2.11.0+cu128",
  "cuda": "12.8",
  "pins_more": [
   "tokenizers",
   "jinja2",
   "huggingface_hub",
   "numpy",
   "scipy"
  ],
  "rule": "凍結の時に、起動器が入れ直して文字列の完全な一致で確かめる（層三の型）。NumPy と SciPy は手元と Colab の両方で（等方の乱数を手元で引き Colab で照らすため・R37・S19）。注意の実装（`attn_implementation`）と決定性の設定（TF32 などの選び）を正本で決め、起動器が印字して転記行 F に入れる。セッションごとにドライバと CUDA の実行時の版を印字し、セッションの間の違いを報告の頭に並べる（止める条件にはしない・S05）",
  "attn_implementation": "凍結の前に決める（器の段・値は凍結の前の確かめの記録）",
  "determinism": "凍結の前に決める（器の段・同上）"
 }
}
````

### 3. `tools/bprime_run.py`（フックの道・読み取り・本の計算の行）

- 出所: 作業の置き場 `tools/bprime_run.py`・SHA16 536C981D3698C2C7・26201 字

```python
# -*- coding: utf-8 -*-
"""bprime_run.py v1（2026-09-30・B′ の教師強制の順伝播を走らせる器・層三の `bl3_run.py` v3 を Gemma 4 と B′ の正本に移したもの・コーディネータ南無弥勒如来）。

走らせ方（正本 `design/contrasts-Bprime.json` のとおり・値は器の出力に置き、読みは付けない）:
  - 入力: 段階 B の組み立て（凍結の `run_stageB_local.arm_texts`・`scenario_and_instruction`・`user_message`）に B′ のチャットの型（`bprime_gemma.apply_chat`）を当て、
    直後に主の書き出し（台帳の番号の並び）を置く。主位置は列の最後のトークン（Gemma では `<channel|>`）、読み取りの位置は列の最後（`readout.primary`）。
  - 加減: 凍結の `run_stageB_local.make_hook`（行ごとの方向の行列・層の出力の型に直して足す・係数は一度だけ）を、選んだ層（`layers.index`）に B′ の `register_hook` で掛ける。
    帯は主位置から読み取りの位置まで。零のベクトルの行が無操作。近道は使わない（`computation.shortcut`）。
  - 読み取り: 最終の正規化の入力を前のフックで取り、`float32` に上げて最終の正規化・語彙の行列・softcap（cap × tanh(z/cap)）を当てる（`readout.primary.quantity`）。
    質量（全語彙の softmax）と層ごとの差分（選んだ層の後の各層の出口をフックで取る・`hidden_states` は使わない）も softcap の後の値で出す。
  - 出口の値の自己検査（`computation.self_checks.logit`）: 読み取りの集合の行と、その位置の模型の出口の上位の行に、softcap あり（器の道）・なし・正規化の二重の三つを当て、
    模型の出口の値（bf16）と `bprime_core.logit_self_check` で突き合わせる（合・否・見分ける力無し）。k は凍結の前に意味のない列で測る（`measure_positions`）。
  - 最後の層の自己検査（`computation.self_checks.layer`）: 自己検査の一本と零のベクトルで、層ごとの差分の最後の層の行と読み取りの効き目の差。
  - 下見（`pilot`）: 出口の値の自己検査 → (vi) → (i)(ii)(iv) → 決め → (iii)（行動の下見の主の率・外した升目を除く・`generate` と同じ処理の並びの変換を添える）。(v) は置かない。
  - 本の計算（`readout.primary.batching`）: 升目と符号の組ごとに、名前のある方向・等方・実在の差（組の符号の向き）と零のベクトル。Onull の組には逆の向きの実在の差を足す（`nulls.real.combos`）。
  - 道の違いの記述（`descriptive.path_difference`）: 本の計算がバッチ一に移ったときに、同じ組をバッチ 16 の道で流す。
関数は起動器と合成データの器が import して呼ぶ（この器だけでは模型を読まない）。
DRY のために壊した器を引数 `bug` で入れられる（本の計算では入れない）: double_norm・no_softcap・hook_next_layer。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, time, hashlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G          # 先に読む（凍結の器の置き場を sys.path に足す）
import bl3_core as K              # 層三の凍結の芯（対数オッズ・集合の中の確率・零と埋めの名・バッチの組み方・下見の決め）
import bprime_core as P           # B′ の芯（許容の式と判定・床の余白の印ほか）

VERSION = 'v1.2'        # v1（2026-09-30）: 正本 v2 に合わせた（出口の値の自己検査の新しい許容・意味のない列での k の測り・下見・本の計算・道の違い・独立の再計算のフックの道・升目の組み立て・方向の読み込み）
                        # v1.1（2026-09-30）: (iii) の変換の並びに読み取りの位置までの列を渡す（`generate` と同じ・前は零の列）。下見に行動の下見の状態を渡す
                        #   （閉じた・器の誤り・採点が定まらない。前は率が無いと `None.get` で落ちた・合成データの器を書く途中で読んで見つけた）。前の版は `prev/bprime_run-v1.py`
                        # v1.2（2026-09-30）: 加減のある順伝播で `output_hidden_states` が設定に入っていたら止める・意味のない列の測りで間違った道の差も返せる（凍結の前の確かめの印字）。前の版は `prev/bprime_run-v1.1.py`
BUGS = (None, 'double_norm', 'no_softcap', 'hook_next_layer')
ToolError = P.ToolError


def require_finite(vals, where):
    """値がすべて有限であること（有限でなければ器の誤りで止める・層三の裁定 D236 の型）。vals: 名 → 値。"""
    bad = sorted(k for k, v in vals.items() if not math.isfinite(float(v)))
    if bad:
        raise ToolError('有限でない値（%s・%d 個・例 %s）' % (where, len(bad), bad[:3]))


def ids_sha16(ids):
    return hashlib.sha256(','.join(str(int(x)) for x in ids).encode('ascii')).hexdigest().upper()[:16]


class Cell:
    """一つの升目（場面 × 土台の腕）の入力と位置（層三の `bl3_run.Cell` と同じ決まり）。"""

    def __init__(self, key, sc, arm, fam, prompt_ids, prefix_ids, set_ids, main_position):
        self.key, self.sc, self.arm, self.fam = key, sc, arm, fam
        self.prompt = list(prompt_ids)
        self.ids = list(prompt_ids) + list(prefix_ids)
        self.mp = int(main_position)
        self.ro = len(self.ids) - 1
        self.set_ids = list(set_ids)            # 選択の文字（族の順・a が先頭）と refuse の頭
        if self.mp != len(self.prompt) - 1:
            raise ToolError('主位置がプロンプトの最後でない: %s' % key)

    def with_prefix(self, prefix_ids):
        return Cell(self.key, self.sc, self.arm, self.fam, self.prompt, prefix_ids, self.set_ids, self.mp)


class Runner:
    def __init__(self, model, C, layer_idx, coef, dirs, bug=None):
        import torch
        import run_stageB_local as RB           # 凍結の段階 B の走行器（make_hook だけ使う）
        if bug not in BUGS:
            raise ValueError(bug)
        self.torch, self.RB, self.model, self.C, self.bug = torch, RB, model, C, bug
        self.layer, self.coef = int(layer_idx), float(coef)
        self.dev = next(model.parameters()).device
        self.eps = G.rms_eps(model)
        self.n_layers = G.n_layers(model)
        self.after = list(range(self.layer + 1, self.n_layers))
        self.g32 = G.final_norm(model).weight.detach().float()
        self.W32 = model.lm_head.weight.detach().float()
        self.cap = G.softcap(model)
        if self.cap is None:
            raise ToolError('softcap が設定に無い（正本 `inputs.model_facts.final_logit_softcapping`）')
        self.dirs = dirs
        self.dim = int(self.g32.shape[0])
        self._zero = np.zeros(self.dim, dtype=np.float32)
        self.n_forward = 0

    # ---- 方向 ----
    def vec(self, did):
        if did in (K.NOOP, K.PAD):
            return self._zero
        return np.asarray(self.dirs[did], dtype=np.float32)

    # ---- 正規化と読み取り（float32） ----
    def norm32(self, h):
        h = h.float()
        return h * self.torch.rsqrt(h.pow(2).mean(-1, keepdim=True) + self.eps) * self.g32

    def capz(self, z, force=False):
        """softcap（器の道）。bug='no_softcap' の器は掛けない（force=True は正しい式を強いる）。"""
        if self.bug == 'no_softcap' and not force:
            return z
        return self.torch.tanh(z / self.cap) * self.cap

    def ours(self, h):
        """器の道の正規化（bug='double_norm' の器は二重に掛ける）。"""
        hn = self.norm32(h)
        return self.norm32(hn) if self.bug == 'double_norm' else hn

    def readout(self, h, cell, full=True):
        hn = self.ours(h)
        Zs = self.capz(hn @ self.W32[cell.set_ids].T).double().cpu().numpy()
        out = {'Zset': Zs, 'lo': K.log_odds_a(Zs, 0, list(range(1, len(cell.set_ids)))), 'pa': K.prob_a_in_set(Zs, 0, list(range(len(cell.set_ids))))}
        if full:
            Zf = self.capz(hn @ self.W32.T).double()
            lse_f = self.torch.logsumexp(Zf, dim=-1)
            out['mass'] = self.torch.exp(self.torch.logsumexp(Zf[:, cell.set_ids], dim=-1) - lse_f).cpu().numpy()
            out['Zfull'] = Zf
        return out

    # ---- 一回の順伝播（行ごとの方向・同じ升目・同じ符号・近道なし） ----
    def forward(self, cell, dir_ids, sign, want_layers=False, want_model_logits=False, full=True):
        torch, RB = self.torch, self.RB
        cfgs = (self.model.config, G.text_cfg(self.model))
        if any(bool(getattr(c_, 'output_hidden_states', False)) for c_ in cfgs):
            raise ToolError('加減のある順伝播で `output_hidden_states` が設定に入っている（正本 `computation.pre_freeze_checks`・層の値はフックで取る）')
        B = len(dir_ids)
        V = np.stack([self.vec(d) for d in dir_ids]).astype(np.float32)
        inp = torch.tensor([cell.ids] * B, device=self.dev)
        starts = [cell.mp] * B
        cap, hs = {}, []
        hs.append(G.final_norm(self.model).register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone())))
        layers = G.decoder_layers(self.model)
        if want_layers:
            for j in self.after:
                hs.append(layers[j].register_forward_hook(lambda m, a, o, j=j: cap.__setitem__(j, (o[0] if isinstance(o, tuple) else o)[:, -1, :].detach().clone())))
        at = self.layer + 1 if self.bug == 'hook_next_layer' else self.layer
        handle = G.register_hook(self.model, at, RB.make_hook(V, self.coef, int(sign), starts, meta={'bprime': True, 'cell': cell.key}))
        try:
            with torch.no_grad():
                out = self.model(input_ids=inp, use_cache=False, logits_to_keep=1)
        finally:
            handle.remove()
            for h_ in hs:
                h_.remove()
            G.assert_no_hooks(self.model, at)
        self.n_forward += 1
        r = self.readout(cap['h'], cell, full=full)
        require_finite({'%d:%d' % (i, j): v for i, row in enumerate(r['Zset']) for j, v in enumerate(row)}, '読み取りの集合の出口の値 ' + cell.key)
        res = {'lo': r['lo'], 'pa': r['pa'], 'Zset': r['Zset'], 'h': cap['h']}
        if full:
            res['mass'] = r['mass']
            res['Zfull'] = r['Zfull']
        if want_model_logits:
            res['model_logits'] = out.logits[:, -1, :].float()
        if want_layers:
            res['layers'] = {j: cap[j].float() for j in self.after}
            res['layer_lo'] = {j: K.log_odds_a(self.capz(self.ours(cap[j]) @ self.W32[cell.set_ids].T).double().cpu().numpy(), 0, list(range(1, len(cell.set_ids)))) for j in self.after}
        return res

    # ---- 出口の値の自己検査 ----
    def three_paths(self, h_row, rows):
        """一つの位置の三つの道（行 rows だけ）: 器の道（softcap あり）・softcap なし（softcap の前の値）・正規化の二重（softcap あり）。"""
        hn = self.norm32(h_row)
        W = self.W32[rows]
        ours = self.capz(self.ours(h_row) @ W.T)
        raw = hn @ W.T
        dbl = self.capz(self.norm32(hn) @ W.T, force=True)
        return ours.double().cpu().numpy(), raw.double().cpu().numpy(), dbl.double().cpu().numpy()

    def check_rows(self, model_logits_row, set_ids, top_rows):
        """掛ける行（正本 `computation.self_checks.logit.rows`）: 読み取りの集合の行と、その位置の模型の出口の値の大きい上位の行（重なりは一度）。"""
        top = self.torch.topk(model_logits_row, int(top_rows)).indices.cpu().tolist()
        rows = list(set_ids) + [int(t) for t in top if int(t) not in set(set_ids)]
        return rows

    def logit_check(self, cell, k, z0):
        """出口の値の自己検査（無操作・近道なし・バッチ一）: 戻り値 {'cell','state','on','off','dbl','n_rows'}。"""
        L = self.C['computation']['self_checks']['logit']
        r = self.forward(cell, [K.NOOP], +1, want_model_logits=True, full=False)
        rows = self.check_rows(r['model_logits'][0], cell.set_ids, L['top_rows'])
        zm = r['model_logits'][0][rows].double().cpu().numpy()
        z_ours, z_raw, z_dbl = self.three_paths(r['h'][0:1], rows)
        s = P.logit_self_check(zm, z_ours[0], z_raw[0], z_dbl[0], k, z0, L['discrimination_factor'])
        return dict(s, cell=cell.key, n_rows=len(rows))

    def measure_positions(self, seqs, set_ids, batch, wrong=False):
        """k の測り（正本 `computation.self_checks.logit.measure`）: 意味のない列（名 → トークンの並び）の最後の位置で、読み取りの集合の行と上位の行について、
        模型の出口の値と器の道（softcap あり）の差の絶対値と、模型の出口の値を集める。batch はバッチの大きさ（同じ列を零のベクトルで並べる）。
        wrong=True なら、softcap なし・正規化の二重の道と模型の出口の値の差の絶対値も返す（凍結の前の確かめの区間ごとの印字・正本 `computation.before_seal.may_print`）。"""
        L = self.C['computation']['self_checks']['logit']
        diffs, zs, d_off, d_dbl = [], [], [], []
        for name, ids in seqs.items():
            c = Cell('meaningless|' + name, 'X', 'X', 'X', ids, [], set_ids, len(ids) - 1)
            r = self.forward(c, [K.NOOP] * int(batch), +1, want_model_logits=True, full=False)
            rows = self.check_rows(r['model_logits'][0], set_ids, L['top_rows'])
            zm = r['model_logits'][0][rows].double().cpu().numpy()
            z_ours, z_raw, z_dbl = self.three_paths(r['h'][0:1], rows)
            diffs.append(np.abs(zm - z_ours[0]))
            zs.append(zm)
            d_off.append(np.abs(zm - z_raw[0]))
            d_dbl.append(np.abs(zm - z_dbl[0]))
        if wrong:
            return np.concatenate(diffs), np.concatenate(zs), np.concatenate(d_off), np.concatenate(d_dbl)
        return np.concatenate(diffs), np.concatenate(zs)

    def layer_check(self, cell, sign, did, tol):
        """最後の層の自己検査（正本 `computation.self_checks.layer`）: 層ごとの差分の最後の層の行と、読み取りの効き目の差。"""
        r = self.forward(cell, [K.NOOP, did], sign, want_layers=True, full=False)
        last = self.after[-1]
        eff_read = float(r['lo'][1] - r['lo'][0])
        eff_layer = float(r['layer_lo'][last][1] - r['layer_lo'][last][0])
        d = abs(eff_read - eff_layer)
        return {'cell': cell.key, 'sign': sign, 'direction': did, 'diff': d, 'tol': tol, 'pass': d <= tol}


def measure_k(R, seqs, set_ids, batches):
    """k の測りと assert（正本 `computation.self_checks.logit.measure`）。バッチの大きさごとに差を集め、z₀ の決め（大きい行の数）はバッチ一の値で行い、
    同じ z₀ で両方の k を出して大きい方を使う。assert が落ちたら ToolError。戻り値: {'z0','k','k_by_batch','big_rows','fallback','n_rows'}。"""
    L = R.C['computation']['self_checks']['logit']
    got = {int(b): R.measure_positions(seqs, set_ids, b) for b in batches}
    if 1 not in got:
        raise ToolError('バッチ一の測りが無い')
    base = P.k_with_asserts(got[1][0], got[1][1], L)
    z0 = base['z0']
    kmax = L['measure']['asserts']['k_max'] if not base['fallback'] else L['measure']['asserts']['k_max_fallback']
    kb = {b: P.measure_k(d, z, z0, L['tolerance_factor']) for b, (d, z) in got.items()}
    k = max(kb.values())
    if not k <= kmax:
        raise ToolError('許容の k が上限を超えた（バッチの大きさごと %s・上限 %s）' % (kb, kmax))
    return {'z0': z0, 'k': k, 'k_by_batch': kb, 'big_rows': base['big_rows'], 'fallback': base['fallback'], 'n_rows': int(len(got[1][0]))}


def head_logit_checks(R, cells, k, z0):
    """頭の出口の値の自己検査（下見の頭と本の計算の頭）: 升目ごとの状態。否が一つでもあれば ToolError。見分ける力無しの位置は数えて返す（止めない・T05）。"""
    states = collections.OrderedDict((c.key, R.logit_check(c, k, z0)) for c in cells)
    bad = [c for c, s in states.items() if s['state'] == '否']
    if bad:
        raise ToolError('出口の値の自己検査が落ちた: %s' % bad)
    no_disc = [c for c, s in states.items() if s['state'] == '見分ける力無し']
    return {'states': {c: s['state'] for c, s in states.items()}, 'no_discrimination': no_disc, 'n_no_discrimination': len(no_disc), 'detail': states}


# ---------------- 下見（無操作だけ） ----------------
def transformed_prob(Zfull_row, set_id, processors, context_ids):
    """(iii) の変換を通した値（正本 `pilot.checks.iii.transformed_def`）: 全語彙の出口の値に `generate` と同じ処理の並び（processors・`bprime_behavior.chain_for_readout` が
    `generate` の中から取ったもの）を当てた後の選択肢 a の文字の確率（選択の文字と refuse の頭の中で割り直さない）。
    `generate` と同じく、値は `float32` にしてから並びに通し、並びには読み取りの位置までの列（context_ids）を渡す。確率は通した後の値の softmax（`float64` で計算する）。"""
    import torch
    z = Zfull_row.float().unsqueeze(0)
    ids = torch.tensor([list(context_ids)], dtype=torch.long, device=z.device)
    z = processors(ids, z)
    p = torch.softmax(z.double(), dim=-1)
    return float(p[0, set_id])


def run_pilot(R, cells_main, C, variant_prefixes, behavior, processors, k, z0):
    """正本 `pilot`: 出口の値の自己検査 → (vi) → (i)(ii)(iv) → 決め → (iii)。値の記録と機械の決定を返す（読みは付けない）。
    behavior: 行動の下見の閉じた記録から {'status': 'ok'|'tool_error'|'unscorable', 'rate': 升目 → 主の率（status が ok のときだけ）}。
    status が ok でなければ (iii) の相関を計算せず、文の鍵を `pilot.iii_fail_sentences` の鍵にする（器の誤り・採点が定まらない）。
    processors: `generate` と同じ処理の並び（`bprime_behavior.chain_for_readout` が取ったもの）。"""
    bstat = (behavior or {}).get('status')
    brate = (behavior or {}).get('rate') or {}
    if bstat not in ('ok',) + tuple(C['pilot']['iii_fail_sentences']):
        raise ToolError('行動の下見の状態が決まりの外: %r' % (bstat,))
    PL = C['pilot']
    batch_default = C['readout']['primary']['batch']
    rec = collections.OrderedDict(version=VERSION)
    rec['logit_check'] = head_logit_checks(R, cells_main, k, z0)
    a_vals, b_vals = {}, {}
    for c in cells_main:
        r16 = R.forward(c, [K.NOOP] * batch_default, +1, full=False)
        r1 = R.forward(c, [K.NOOP], +1, full=False)
        a_vals[c.key] = list(map(float, r16['lo'])) + [float(r1['lo'][0])]
        b_vals[c.key] = [float(r1['lo'][0])] + [float(R.forward(c, [K.NOOP], +1, full=False)['lo'][0]) for _ in range(PL['repeat_n'] - 1)]
    sa = max(K.spread(v) for v in a_vals.values())
    sb = max(K.spread(v) for v in b_vals.values())
    vi = K.vi_decision(sa, sb, PL['noise_max'], batch_default)
    rec['vi'] = {'a': {k_: K.spread(v) for k_, v in a_vals.items()}, 'b': {k_: K.spread(v) for k_, v in b_vals.items()}, 'decision': vi}
    if vi['stop']:
        rec['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
        return rec
    batch = vi['batch']
    rec['batch'], rec['floor'] = batch, vi['floor']

    def noop_at_config(c, prefix=None):
        cc = c if prefix is None else c.with_prefix(prefix)
        r = R.forward(cc, [K.NOOP] * batch, +1, full=True)
        return {'lo': float(r['lo'][0]), 'pa': float(r['pa'][0]), 'mass': float(r['mass'][0]), 'Zfull0': r['Zfull'][0]}
    nv = {c.key: noop_at_config(c) for c in cells_main}
    ok_main = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], PL['mass_min'], PL['p_bounds']) for c in cells_main}
    rec['cells'] = {c.key: {'lo': nv[c.key]['lo'], 'pa': nv[c.key]['pa'], 'mass': nv[c.key]['mass'], 'pass_i_ii': ok_main[c.key]} for c in cells_main}
    iv = {}
    for name, pref in variant_prefixes.items():
        lv = {c.key: noop_at_config(c, pref)['lo'] for c in cells_main}
        iv[name] = {'lo': lv, 'flags': K.variant_flags({c.key: nv[c.key]['lo'] for c in cells_main}, lv, PL['variant_flag'])}
    rec['iv'] = iv
    cd = K.cells_decision(ok_main, {}, PL['decision']['cells_min_pass'])
    rec['decision'] = cd
    import blens_core as CB
    keep = [c for c in cells_main if c.key not in set(cd['dropped'])]
    for c in keep:
        rec['cells'][c.key]['pa_transformed'] = transformed_prob(nv[c.key]['Zfull0'], c.set_ids[0], processors, c.ids)
        rec['cells'][c.key]['behavior_rate'] = brate.get(c.key)
    if bstat != 'ok':
        rec['iii'] = {'fail': bstat, 'sentence_key': None, 'n': len(keep), 'dropped_n': len(cells_main) - len(keep)}
    elif any(brate.get(c.key) is None for c in keep):
        raise ToolError('行動の下見の率が欠けた升目がある（閉じた記録と升目の鍵を照らす）')
    else:
        raw = [nv[c.key]['pa'] for c in keep]
        obs = [brate[c.key] for c in keep]
        rho = CB.spearman(raw, obs) if len(keep) >= 2 else float('nan')
        rec['iii'] = {'rho': rho, 'n': len(keep), 'dropped_n': len(cells_main) - len(keep), 'sentence_key': K.iii_sentence(rho)}
    rec['n_forward'] = R.n_forward
    return rec


# ---------------- 本の計算 ----------------
def cell_sign_sets(C, named, iso, real):
    """升目と符号の組ごとの方向の集まり（正本 `nulls.real.combos`・`readout.primary.batching`）。戻り値: [(組の鍵, 升目の鍵, 符号, 方向の名の並び, 主の組か)]。"""
    main = [(sc, base, int(sg)) for sc, base, sg in C['cell_signs_main']]
    out = []
    for sc, base, sg in main:
        out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(iso) + list(real), True))
    for sc, base, sg in main:
        if (sc, base, -sg) not in main:
            out.append(('%s|%s|%+d' % (sc, base, -sg), '%s|%s' % (sc, base), -sg, list(real), False))
    keys = [o[0] for o in out]
    if len(keys) != len(set(keys)):
        raise ToolError('組の鍵が重なる')
    if sum(1 for o in out if not o[4]) != C['nulls']['real']['onull_combos']:
        raise ToolError('逆の向きの組の数が正本と違う')
    return out


def run_cell_sign(R, cell, sign, dir_ids, batch, seed, key_index, layer_dirs=(), keep_iso_layers=True):
    """一つの升目と符号の全ての方向（零のベクトルの無操作を含む・端数は零のベクトルで埋める）。無操作の入ったバッチを先に流す（層ごとの差分のため）。"""
    plan = K.batch_plan(dir_ids, batch, seed, key_index)
    first = [i for i, b in enumerate(plan) if K.NOOP in b]
    if len(first) != 1:
        raise ToolError('無操作の入ったバッチがちょうど一つでない')
    order = first + [i for i in range(len(plan)) if i != first[0]]
    lo, mass, pa = {}, {}, {}
    lay = {'noop_lo': None, 'rows': {}, 'iso': collections.defaultdict(list)}
    noop_h = None
    for bi in order:
        ids_ = plan[bi]
        want_layers = any((d == K.NOOP) or (d in layer_dirs) or (keep_iso_layers and d.startswith('iso:')) for d in ids_)
        r = R.forward(cell, ids_, sign, want_layers=want_layers, full=True)
        for k_, d in enumerate(ids_):
            if d == K.PAD:
                continue
            lo[d], mass[d], pa[d] = float(r['lo'][k_]), float(r['mass'][k_]), float(r['pa'][k_])
        if want_layers:
            if noop_h is None:
                k0 = ids_.index(K.NOOP)
                noop_h = {j: r['layers'][j][k0].clone() for j in R.after}
                lay['noop_lo'] = {j: float(r['layer_lo'][j][k0]) for j in R.after}
            for k_, d in enumerate(ids_):
                if d in (K.PAD, K.NOOP) or not ((d in layer_dirs) or (keep_iso_layers and d.startswith('iso:'))):
                    continue
                u = float(sign) * R.torch.tensor(R.vec(d), device=R.dev).float()
                vals = []
                for j in R.after:
                    dh = r['layers'][j][k_] - noop_h[j]
                    nrm = float(dh.norm())
                    cos = float((dh @ u) / (dh.norm() * u.norm())) if nrm > 0 else 0.0
                    vals.append((nrm, cos, float(r['layer_lo'][j][k_]) - lay['noop_lo'][j]))
                if d in layer_dirs:
                    lay['rows'][d] = vals
                else:
                    lay['iso'][d] = vals
    require_finite(lo, '升目と符号 %s|%+d の対数オッズ' % (cell.key, sign))
    require_finite(mass, '升目と符号 %s|%+d の質量' % (cell.key, sign))
    require_finite(pa, '升目と符号 %s|%+d の集合の中の確率' % (cell.key, sign))
    eff = {d: lo[d] - lo[K.NOOP] for d in lo if d != K.NOOP}
    return {'lo': lo, 'effects': eff, 'mass': mass, 'pa_noop': pa[K.NOOP], 'layers': lay, 'n_batches': len(plan)}


def layer_summary(lay, band):
    """等方の帰無の層ごとの中央値と中央の区間（正本 `descriptive.layerwise`）。"""
    if not lay['iso']:
        return None
    A = np.array(list(lay['iso'].values()), dtype=np.float64)
    lo_q, hi_q = 100 * (1 - band) / 2, 100 * (1 + band) / 2
    return {'median': np.median(A, axis=0).tolist(), 'lo': np.percentile(A, lo_q, axis=0).tolist(), 'hi': np.percentile(A, hi_q, axis=0).tolist(), 'n': int(A.shape[0])}


def run_main_phase(R, C, cells, names, pilot, k, z0, iso_n=None, batch_override=None, log=print):
    """本の計算の全体（正本 `computation`・`readout.primary.batching`）: 頭の自己検査（出口の値・最後の層）→ 全ての升目と符号の組。近道は使わない。
    pilot: 本の凍結で凍結した読み取りの下見の記録（バッチの大きさ・外した升目）。names: {'named','iso','real'} の名の並び。
    iso_n は合成データの確かめで等方の本数を減らすときだけ使う。batch_override は道の違いの記述（バッチ 16 の道）だけに使う。
    戻り値: {'head': 頭の確かめ, 'cells': 組の鍵 → 出力, 'batch', 'dropped'}。log には組の鍵と時間だけを渡す（値は渡さない）。"""
    dropped = set((pilot.get('decision') or {}).get('dropped', []))
    batch = int(batch_override or pilot['batch'])
    items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in C['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
    head = collections.OrderedDict()
    if batch_override is None:
        head['logit_check'] = head_logit_checks(R, [cells[k_] for k_ in cells if k_ not in dropped], k, z0)
        head['layer_check'] = R.layer_check(items[0][0], items[0][1], 'check', C['computation']['layer_tol'])
        if not head['layer_check']['pass']:
            raise ToolError('最後の層の自己検査が落ちた（本の計算の頭）')
    iso = names['iso'] if iso_n is None else names['iso'][:iso_n]
    sets = cell_sign_sets(C, names['named'], iso, names['real'])
    layer_dirs = list(names['named'])
    band = C['descriptive']['layerwise']['band']
    out = collections.OrderedDict()
    t0 = time.time()
    for ki, (key, ck, sg, ds, main_cs) in enumerate(sets):
        if ck in dropped:
            continue
        o = run_cell_sign(R, cells[ck], sg, ds, batch, C['readout']['primary']['order_seed'], ki, layer_dirs=layer_dirs if main_cs else (), keep_iso_layers=main_cs)
        o['layers'] = {'noop_lo': o['layers']['noop_lo'], 'rows': o['layers']['rows'], 'iso_summary': layer_summary(o['layers'], band) if main_cs else None}
        out[key] = o
        log('[bprime_run] 升目と符号 %s（%d/%d）・%.0f 秒' % (key, ki + 1, len(sets), time.time() - t0))
    return {'head': head, 'cells': out, 'batch': batch, 'dropped': sorted(dropped)}


def recompute_hook_path(R, rows, dirs_by_row, log=None):
    """独立の再計算の本の器のフックの道（正本 `independent_recompute.new_paths` の一つ目・近道なし・バッチ一）。層三の `bl3_run.recompute_hook_path` と同じ。"""
    out = {}
    t0 = time.time()
    for i, (name, cell, sign) in enumerate(rows):
        base = float(R.forward(cell, [K.NOOP], sign, full=False)['lo'][0])
        eff = {}
        for did, sg in dirs_by_row[name]:
            eff['%s|%+d' % (did, sg)] = float(R.forward(cell, [did], sg, full=False)['lo'][0]) - base
        require_finite(dict(eff, noop=base), '独立の再計算のフックの道の行 %s' % name)
        out[name] = {'noop_lo': base, 'effects': eff}
        if log:
            log('[bprime_run] 独立の再計算のフックの道 %s（%d/%d・順伝播 %d）・%.0f 秒' % (name, i + 1, len(rows), 1 + len(eff), time.time() - t0))
    return out


def build_cells(tok, C, ledger, keys):
    """升目の入力（凍結の組み立ての関数と台帳の書き出し）を作り、台帳のプロンプトの長さ・主位置・読み取りの位置・族・並びの SHA16 と突き合わせる（違えば止める）。"""
    import run_stageB_local as RB
    AT = RB.arm_texts()
    fam_letters = C['readout']['primary']['letters']
    heads = ledger['heads']
    out = collections.OrderedDict()
    for key in keys:
        sc, arm = key.split('|')
        scen, inst = RB.scenario_and_instruction(sc)
        prompt = G.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
        fam = scen['family']
        set_ids = [int(heads[x]['next']) for x in fam_letters[fam]] + [int(heads['refuse']['next'])]
        c = Cell(key, sc, arm, fam, prompt, ledger['prefix_ids'], set_ids, G.main_position(prompt))
        b = ledger['cells_main'][key]
        if (len(prompt), c.mp, c.ro, fam, set_ids) != (b['prompt_len'], b['main_position'], b['readout_position'], b['family'], b['set_ids']) or ids_sha16(c.ids) != b['ids_sha16']:
            raise ToolError('升目の入力が台帳と違う: %s' % key)
        out[key] = c
    return out


def load_dirs(npz_path, json_path, C):
    """方向の npz（`bprime_directions.py`）を名で引ける形にする。SHA-256 を記録と突き合わせ、名前のある方向の名の並びが正本と同じこと・組の本数を確かめる（違えば止める）。"""
    J = json.load(open(json_path, encoding='utf-8'))
    if hashlib.sha256(open(npz_path, 'rb').read()).hexdigest().upper() != J['npz_sha256']:
        raise ToolError('方向の npz の SHA-256 が記録と違う')
    if list(J['groups']['named']['names']) != list(C['directions']['named']):
        raise ToolError('方向の記録の名前のある方向の名の並びが正本と違う')
    if J['groups']['iso']['count'] != C['nulls']['isotropic']['count'] or len(J['groups']['real']['names']) != C['nulls']['real']['pairs']:
        raise ToolError('方向の組の本数が正本と違う')
    Z = np.load(npz_path)
    names = {'named': J['groups']['named']['names'], 'iso': ['iso:%d' % i for i in range(J['groups']['iso']['count'])],
             'real': ['real:' + p for p in J['groups']['real']['names']], 'check': ['check']}
    d = collections.OrderedDict()
    for g, ns in names.items():
        A = Z[g]
        if len(A) != len(ns):
            raise ToolError('方向の組の本数が記録と違う: %s' % g)
        for n, v in zip(ns, A):
            d[n] = np.asarray(v, dtype=np.float64)
    return d, names


if __name__ == '__main__':
    print(__doc__)
```

### 4. `tools/independent/bprime_recompute_rewrite.py`（書き換えの道（別の個体））

- 出所: 作業の置き場 `tools/independent/bprime_recompute_rewrite.py`・SHA16 DF0833637E5755D8・55434 字

```python
# -*- coding: utf-8 -*-
"""bprime_recompute_rewrite.py v1 —— B′（Gemma-4-31B-it）の独立の再計算の器のうち、**残差の書き換えの道**
（2026-09-30・本の器の書き手〔コーディネータ・南無弥勒如来〕と別の系統内の個体が書いた・登録者の裁定 D270 による・独立の目を通っていない）。

正本 `design/contrasts-Bprime.json` の `independent_recompute`（一段目の相手）・`readout.primary`・`layers`・`inputs.model_facts`・
`nulls.real`・`main_rows`・`cells_main` に従う。コーディネータの器（`bprime_run` ほか）の中身を**読まずに**書いた。
`--dry` でだけ、その公開の関数を中を見ずに呼び、数を突き合わせる。

道（加減をフックでなく、選んだ層の出力を書き換えて後の層を流す・近道なし・バッチ一）:
  入力     段階 B の組み立て（`run_stageB_local.user_message(腕の本文, 場面の本文, 指示)`・場面と指示は
           `run_stageB_local.scenario_and_instruction`）の user の発話一つに Gemma のチャットの型（system なし・生成の口つき）を当て、
           その直後に主の書き出し（台帳の `prefix_ids`）を**トークンの並びのまま**つなぐ。主位置＝プロンプトの長さ−1（`<channel|>`）・
           読み取りの位置＝列の最後。升目ごとに台帳の prompt_len・main_position・main_position_token・readout_position・ids_sha16・
           族・読み取りの集合と照らし、違えば止める。
  層を回す transformers 5.16.1 の `Gemma4ForConditionalGeneration.forward` → `Gemma4Model.forward` → `Gemma4TextModel.forward` の
           文字だけの入力の手順を、部品を差し替えずに写す: 置き換えの印（画像・動画・音声のトークン）の確かめ → 埋め込み
           （`get_input_embeddings()`・倍率 √hidden は埋め込みの部品の中）→（層ごとの入力があれば `get_per_layer_inputs` と
           `project_per_layer_inputs`）→ 位置の番号 → mask（多様式の本体と同じく `create_masks_for_generate` を past_key_values=None で
           呼ぶ・窓つきと全体の二つの型）→ rotary（注意の型ごとに `rotary_emb(h, position_ids, 型)`）→ 空の `UserDict` の
           shared_kv_states → 層 0〜最後を模型の forward と同じ引数で一つずつ呼ぶ。層 L の出力を得た直後に書き換える。
           cache: 既定は use_cache=False と同じ（層に past_key_values=None）。use_cache=None なら模型の forward の既定
           （設定の use_cache・一回ごとに空の DynamicCache を作って捨てる）に合わせる（開発の記録の「決まっていなかった所」）。
  書き換え 層 L の出力の、主位置から列の最後までの位置に sign×coef×v を足す。v（float64）は段階 B の走行器のフック（`make_hook`）と
           同じ算術で、NumPy の float32 を経て**層の出力の型**に直してから `sign * coef *` を掛け、その型のまま足す（係数は一度だけ）。
  読み取り 最後の層の出力（**最終の正規化の入力**。`hidden_states[-1]` は正規化の後の値なので使わない）の最後の位置を float32 に上げ、
           最終の正規化を float32 で当て（h × rsqrt(mean(h²)+eps) × g・g と eps は模型の最終の正規化から・1＋g ではない）、
           語彙の行列（埋め込みと共有の `lm_head.weight`）の読み取りの集合の行（a が先頭・最後が refuse の頭）を float32 で当て、
           softcap（cap × tanh(z ÷ cap)・cap は `text_config.final_logit_softcapping`）を掛ける。
           量＝z_a − logsumexp（ほかの選択の文字と refuse の頭）。効き目＝加えた値 − 無操作（零のベクトル）の値。
出力: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}（符号の書き方は '%+d'）。行と方向の組は
      `bl3_core.recompute_set`。**値は印字しない**（正本 `independent_recompute.print`）。`--dry` が差の最大を印字するのは乱数の小さな模型だけ。
**フックは使わない**: 呼ぶ前と後に、模型のどの部品にも forward の hook（前・後・大域）が無いことを確かめ、あれば止める。
ただし transformers 5 が `output_hidden_states` などの初回に据え付けて居残らせる記録用の hook
（`transformers.utils.output_capturing` の `output_capturing_hook`・値を変えない）だけは数えない。
用法: python bprime_recompute_rewrite.py --selftest   （乱数の小さな模型で自己検査）
      python bprime_recompute_rewrite.py --dry        （乱数の小さな模型で、コーディネータのフックの道と一段目の許容で突き合わせ）
走らせ方: PYTHONPATH=<Bprime>/pylib（transformers 5.16.1）・PYTHONDONTWRITEBYTECODE=1 を勧める。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import sys
if __name__ == '__main__':
    sys.dont_write_bytecode = True          # 外の置き場（公開の置き場・pylib・Bprime/tools）に .pyc を書かない
import os, json, time, copy, hashlib, argparse
import numpy as np

VERSION = 'v1'
HERE = os.path.dirname(os.path.abspath(__file__))
BPRIME = os.path.dirname(os.path.dirname(HERE))
CANON_PATH = os.path.join(BPRIME, 'design', 'contrasts-Bprime.json')
LEDGER_PATH = os.path.join(BPRIME, 'tools', 'ledger-bprime.json')
HF_DIR = os.path.join(BPRIME, 'hf', 'gemma-4-31B-it', '842da3794eaa0b77d5f08bae87a17459d91ff475')   # 設定とトークナイザだけ（実の重みは無い・使わない）
PUB_TOOLS_DEFAULT = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b/tools'          # 公開の置き場の凍結の器（読むだけ）
CAPTURE_MODULE = 'transformers.utils.output_capturing'
FENCE = '本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
# 乱数の小さな模型（指示の作り方）
TINY_TEXT = dict(hidden_size=64, intermediate_size=128, num_hidden_layers=6, num_attention_heads=4, num_key_value_heads=2,
                 head_dim=16, global_head_dim=32, num_global_key_value_heads=1, sliding_window=8)
TINY_VISION = dict(hidden_size=32, intermediate_size=64, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2,
                   head_dim=16, global_head_dim=16)
TINY_COEF = 2.0            # 確かめの係数（書き手の選び・層三の係数と同じ値・本の計算の係数は呼び手が渡す）
TINY_N_ISO = 10            # 確かめの等方の本数（指示の「等方の十本」）
SYN_NORM_FRAC = 0.5        # 合成の方向のノルム＝残差のノルム × 0.5（指示）


def _die(msg):
    raise SystemExit('bprime_recompute_rewrite: ' + msg)


def _pub(name):
    """公開の置き場の凍結の器を import する（読むだけ・環境変数 OP4B_PUB_TOOLS で置き場を替えられる）。"""
    import importlib
    d = os.environ.get('OP4B_PUB_TOOLS', PUB_TOOLS_DEFAULT)
    if os.path.isdir(d) and d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module(name)


def load_canon():
    return json.load(open(CANON_PATH, encoding='utf-8'))


def load_ledger():
    return json.load(open(LEDGER_PATH, encoding='utf-8'))


def sha16_ids(ids):
    """台帳の ids_sha16 の決まり: sha256(','.join(str(x))) の十六進の大文字の頭 16 字。"""
    return hashlib.sha256(','.join(str(int(x)) for x in ids).encode('ascii')).hexdigest().upper()[:16]


# ---------------------------------------------------------------- 模型の部品と確かめ（止める）

def parts(model):
    """(最上位 Gemma4ForConditionalGeneration, 多様式の本体 Gemma4Model, 言語の模型 Gemma4TextModel)。"""
    if type(model).__name__ != 'Gemma4ForConditionalGeneration':
        _die('模型の最上位が Gemma4ForConditionalGeneration でない: %s' % type(model).__name__)
    mm = getattr(model, 'model', None)
    if mm is None or type(mm).__name__ != 'Gemma4Model':
        _die('多様式の本体が Gemma4Model でない: %s' % type(mm).__name__)
    lm = getattr(mm, 'language_model', None)
    if lm is None or type(lm).__name__ != 'Gemma4TextModel':
        _die('言語の模型が Gemma4TextModel でない: %s' % type(lm).__name__)
    return model, mm, lm


def is_capture_hook(fn):
    """transformers 5 の記録用の hook（値を変えない・output_* の初回に据え付けられて居残る）か。"""
    return getattr(fn, '__module__', None) == CAPTURE_MODULE and getattr(fn, '__name__', None) == 'output_capturing_hook'


def foreign_hooks(model):
    """記録用の hook を除いた forward の hook（前・後）と大域の hook の一覧。"""
    import torch.nn.modules.module as M
    bad = []
    for name, m in model.named_modules():
        for attr in ('_forward_hooks', '_forward_pre_hooks'):
            for _, fn in (getattr(m, attr, None) or {}).items():
                if attr == '_forward_hooks' and is_capture_hook(fn):
                    continue
                bad.append('%s.%s（%s.%s）' % (name or '<模型>', attr, getattr(fn, '__module__', '?'),
                                             getattr(fn, '__qualname__', type(fn).__name__)))
    for attr in ('_global_forward_hooks', '_global_forward_pre_hooks'):
        d = getattr(M, attr, None)
        if d:
            bad.append('大域の %s %d 本' % (attr, len(d)))
    return bad


def capture_hook_count(model):
    return sum(1 for _, m in model.named_modules() for fn in (getattr(m, '_forward_hooks', None) or {}).values()
               if is_capture_hook(fn))


def assert_no_foreign_hooks(model):
    bad = foreign_hooks(model)
    if bad:
        _die('模型に forward の hook が掛かっている（この道はフックを使わず、掛け残しも混ぜない）: ' + '・'.join(bad))


def is_real(model, C):
    """正本の模型の事実（層の数・次元）と同じ形の模型か（実の重みの本の計算）。"""
    _, _, lm = parts(model)
    mf = C['inputs']['model_facts']
    return len(lm.layers) == int(mf['num_hidden_layers']) and int(lm.config.hidden_size) == int(mf['hidden_size'])


def softcap_value(model):
    top, _, _ = parts(model)
    cap = top.config.get_text_config().final_logit_softcapping
    if cap is None:
        _die('text_config.final_logit_softcapping が無い（正本 readout.primary.quantity は softcap を掛ける）')
    return float(cap)


def check_env(model, C, ledger):
    """版・機種・形の確かめ。手回しの道は transformers 5.16.1 の forward を写したので、版が違えば止める。"""
    import torch
    import transformers
    want = str(ledger['meta']['transformers'])
    if transformers.__version__ != want:
        _die('transformers の版が %s（手回しの道は %s の Gemma4 の forward を写した・台帳 meta.transformers）'
             % (transformers.__version__, want))
    top, mm, lm = parts(model)
    if top.training or mm.training or lm.training:
        _die('模型が訓練の形（eval にしていない）')
    obj = top
    for p in str(C['layers']['layer_path']).split('.'):
        obj = getattr(obj, p, None)
    if obj is not lm.layers:
        _die('正本 layers.layer_path（%s）が言語の模型の層の並びを指さない' % C['layers']['layer_path'])
    n = len(lm.layers)
    if n != int(lm.config.num_hidden_layers):
        _die('層の並びの数（%d）が設定の層の数（%d）と違う' % (n, lm.config.num_hidden_layers))
    if top.lm_head.weight is not lm.embed_tokens.weight:
        _die('語彙の行列（lm_head.weight）が埋め込みと共有でない')
    if type(lm.norm).__name__ != 'Gemma4RMSNorm' or not getattr(lm.norm, 'with_scale', False):
        _die('最終の正規化が重みつきの Gemma4RMSNorm でない: %s' % type(lm.norm).__name__)
    if float(lm.norm.eps) != float(lm.config.rms_norm_eps):
        _die('最終の正規化の eps（%r）が設定の rms_norm_eps（%r）と違う' % (lm.norm.eps, lm.config.rms_norm_eps))
    cap = softcap_value(model)
    if is_real(model, C):
        mf = C['inputs']['model_facts']
        if lm.embed_tokens.weight.dtype != torch.bfloat16:
            _die('本の計算の模型が bf16 でない（%s・正本 readout.primary.precision）' % lm.embed_tokens.weight.dtype)
        if cap != float(mf['final_logit_softcapping']) or mf.get('softcap_level') != 'text_config':
            _die('softcap（%r）が正本 inputs.model_facts と違う' % cap)
        if int(lm.config.vocab_size) != int(mf['vocab_size']) or int(lm.config.sliding_window) != int(mf['sliding_window']):
            _die('語彙の数か窓が正本 inputs.model_facts と違う')
        if sum(1 for t in lm.config.layer_types if t == 'full_attention') != int(mf['full_attention_layers']):
            _die('全体の注意の層の数が正本 inputs.model_facts と違う')


def layer_index_for(model, C):
    """選ぶ層の添字: `direction_B.layer_index(正本 layers.ratio, 模型の層の数)`。本の模型では正本 `layers.index` とも照らす。"""
    DB = _pub('direction_B')
    _, _, lm = parts(model)
    n = len(lm.layers)
    L = DB.layer_index(float(C['layers']['ratio']), n)
    if is_real(model, C):
        if L != int(C['layers']['index']) or int(C['layers']['hidden_states_index']) != L + 1:
            _die('層の添字 %d が正本 layers.index（%s）・hidden_states_index（%s）と合わない'
                 % (L, C['layers']['index'], C['layers']['hidden_states_index']))
    if lm.config.layer_types[L] != C['layers']['layer_type']:
        _die('選ぶ層 %d の種類 %s が正本 layers.layer_type（%s）と違う' % (L, lm.config.layer_types[L], C['layers']['layer_type']))
    return L


# ---------------------------------------------------------------- 升目の入力（段階 B の組み立てのまま）

def chat_ids(tok, msg):
    """user の発話一つ・system なし・生成の口つきのチャットの型（transformers 5 は辞書の形を返すので input_ids を取る）。"""
    enc = tok.apply_chat_template([{'role': 'user', 'content': msg}], add_generation_prompt=True, tokenize=True)
    ids = enc['input_ids'] if hasattr(enc, 'keys') else enc
    if hasattr(ids, 'tolist'):
        ids = ids.tolist()
    ids = list(ids)
    if ids and isinstance(ids[0], (list, tuple)):
        if len(ids) != 1:
            _die('チャットの型の出力が一本の列でない')
        ids = list(ids[0])
    return [int(x) for x in ids]


def cell_input(tok, C, ledger, cell_key, AT=None):
    """升目（'場面|土台の腕'）の入力を組み立て、台帳 `cells_main` の升目の記録と照らす（違えば止める）。

    返り値: {'cell', 'ids'（プロンプト＋主の書き出し）, 'prompt_len', 'mp'（主位置）, 'ro'（読み取りの位置＝列の最後）,
             'family', 'letters', 'set_ids'（a が先頭・最後が refuse の頭）}。"""
    RB = _pub('run_stageB_local')
    RP = C['readout']['primary']
    LC = ledger['cells_main']
    if cell_key not in LC:
        _die('升目 %s が台帳 cells_main に無い' % cell_key)
    rec = LC[cell_key]
    sp = cell_key.split('|')
    if len(sp) != 2:
        _die('升目の鍵の形が違う（場面|土台の腕）: %s' % cell_key)
    scen, arm = sp
    if rec.get('scenario') != scen or rec.get('arm') != arm:
        _die('台帳の升目 %s の場面か腕が鍵と違う' % cell_key)
    if [scen, arm] not in [list(x) for x in C['cells_main']]:
        _die('升目 %s が正本 cells_main に無い' % cell_key)
    s, inst = RB.scenario_and_instruction(scen)
    AT = AT if AT is not None else RB.arm_texts()
    if arm not in AT:
        _die('土台の腕 %s の本文が引けない' % arm)
    prompt = chat_ids(tok, RB.user_message(AT[arm]['text'], s['text'], inst))
    prefix = [int(x) for x in ledger['prefix_ids']]
    if prefix != [int(x) for x in RP['prefix_ids']]:
        _die('台帳の prefix_ids が正本 readout.primary.prefix_ids と違う')
    ids = prompt + prefix
    mp, ro = len(prompt) - 1, len(ids) - 1
    fam = s.get('family')
    bad = []
    if len(prompt) != int(rec['prompt_len']):
        bad.append('プロンプトの長さ %d（台帳 %s）' % (len(prompt), rec['prompt_len']))
    if mp != int(rec['main_position']):
        bad.append('主位置 %d（台帳 %s）' % (mp, rec['main_position']))
    if tok.convert_ids_to_tokens(prompt[-1]) != rec['main_position_token']:
        bad.append('主位置のトークン %r（台帳 %r）' % (tok.convert_ids_to_tokens(prompt[-1]), rec['main_position_token']))
    if ro != int(rec['readout_position']):
        bad.append('読み取りの位置 %d（台帳 %s）' % (ro, rec['readout_position']))
    if sha16_ids(ids) != rec['ids_sha16']:
        bad.append('ids_sha16 %s（台帳 %s）' % (sha16_ids(ids), rec['ids_sha16']))
    if fam != rec.get('family'):
        bad.append('族 %s（台帳 %s）' % (fam, rec.get('family')))
    if bad:
        _die('升目 %s の入力が台帳と違う: %s' % (cell_key, '・'.join(bad)))
    if fam not in RP['letters']:
        _die('族 %s の選択の文字が正本 readout.primary.letters に無い' % fam)
    letters = list(RP['letters'][fam])
    if letters[0] != RP['catastrophe_letter'] or letters != list(rec['letters']):
        _die('升目 %s の選択の文字（%s）が正本と台帳で合わないか、先頭が破局の側の文字でない' % (cell_key, letters))
    SI = RP['set_ids']
    set_ids = [int(SI[x]) for x in letters] + [int(SI['refuse'])]
    if set_ids != [int(x) for x in rec['set_ids']]:
        _die('升目 %s の読み取りの集合が正本 readout.primary.set_ids と台帳で違う' % cell_key)
    for x in list(letters) + ['refuse']:
        if int(ledger['heads'][x]['next']) != int(SI[x]):
            _die('台帳 heads.%s.next が正本 set_ids と違う' % x)
    want = letters + [RP['refuse_head']]
    got = [tok.convert_ids_to_tokens(i) for i in set_ids]
    if got != want or got != list(rec['set_pieces']):
        _die('読み取りの集合のトークンが文字と refuse の頭に戻らない: %s 対 %s' % (got, want))
    if len(set(set_ids)) != len(set_ids):
        _die('読み取りの集合のトークンが重なる')
    return {'cell': cell_key, 'ids': ids, 'prompt_len': len(prompt), 'mp': mp, 'ro': ro,
            'family': fam, 'letters': letters, 'set_ids': set_ids}


# ---------------------------------------------------------------- 手回しの順伝播

def resolve_use_cache(model, use_cache):
    """use_cache=None のとき、模型の forward と同じ解き方（最上位の設定 → 言語の設定の use_cache）。"""
    if use_cache is not None:
        return bool(use_cache)
    top, _, lm = parts(model)
    v = getattr(top.config, 'use_cache', None)
    if v is None:
        v = getattr(lm.config, 'use_cache', None)
    return bool(v)


def _forward_impl(model, ids, on_layer_out, use_cache=False, keep=None):
    """文字だけの入力で模型の forward を手で写して層を回す。層 i の出力を得るたびに on_layer_out(i, h) を通す。

    返り値: 最後の層の出力（最終の正規化の入力・模型の型・形 [1, 列の長さ, 次元]）。"""
    import torch
    from collections import UserDict
    import transformers.models.gemma4.modeling_gemma4 as MG         # 模型の組み立てが呼ぶのと同じ名の束ね
    top, mm, lm = parts(model)
    tcfg = lm.config
    uc = resolve_use_cache(model, use_cache)
    with torch.no_grad():
        dev = lm.embed_tokens.weight.device
        input_ids = torch.tensor([[int(x) for x in ids]], dtype=torch.long, device=dev)
        # Gemma4Model.forward: 置き換えの印（文字だけの入力では無い）
        image_mask, video_mask, audio_mask = mm.get_placeholder_mask(input_ids, None)
        multimodal_mask = image_mask | video_mask | audio_mask
        if bool(multimodal_mask.any()):
            _die('列に画像・動画・音声の置き換えの印がある（文字だけの入力しか写していない）')
        llm_input_ids = torch.where(multimodal_mask, top.config.text_config.pad_token_id, input_ids)
        inputs_embeds = mm.get_input_embeddings()(llm_input_ids)            # 倍率 √hidden は埋め込みの部品の中
        per_layer_inputs = None
        if top.config.get_text_config().hidden_size_per_layer_input:
            pad_embedding = lm.embed_tokens.weight[top.config.text_config.pad_token_id, :]
            mmask = multimodal_mask.to(inputs_embeds.device)
            llm_inputs_embeds = torch.where(mmask[..., None], pad_embedding.view(1, 1, -1), inputs_embeds)
            per_layer_inputs = lm.get_per_layer_inputs(llm_input_ids, llm_inputs_embeds)
        position_ids = torch.arange(inputs_embeds.shape[1], device=inputs_embeds.device).unsqueeze(0)
        masks = MG.create_masks_for_generate(config=top.config.get_text_config(), inputs_embeds=inputs_embeds,
                                             attention_mask=None, past_key_values=None, position_ids=position_ids)
        if not isinstance(masks, dict) or set(masks) != set(tcfg.layer_types):
            _die('mask の形が注意の型ごとの辞書でない')
        # Gemma4TextModel.forward
        if lm.hidden_size_per_layer_input:
            per_layer_inputs = lm.project_per_layer_inputs(inputs_embeds, per_layer_inputs)
        past = MG.DynamicCache(config=lm.config) if uc else None           # 一回ごとに作って捨てる（順伝播をまたいで使い回さない）
        h = inputs_embeds
        pe = {lt: lm.rotary_emb(h, position_ids, lt) for lt in lm.unique_layer_types}
        shared = UserDict()
        if keep is not None:
            keep['masks'] = masks
            keep['use_cache'] = uc
            keep['embeds'] = inputs_embeds.clone()
        for i, layer in enumerate(lm.layers[: tcfg.num_hidden_layers]):
            lt = tcfg.layer_types[i]
            pli = per_layer_inputs[:, :, i, :] if per_layer_inputs is not None else None
            h = layer(h, pli, shared_kv_states=shared, position_embeddings=pe[lt], attention_mask=masks[lt],
                      position_ids=position_ids, past_key_values=past)
            h = on_layer_out(i, h)
            if keep is not None:
                keep.setdefault('outs', []).append(h.clone())
    if h.shape[1] != len(ids):
        _die('出口の列の長さ %d が入力の長さ %d と違う' % (h.shape[1], len(ids)))
    return h


def cast_add(vec, coef, sign, like):
    """段階 B の `make_hook` の算術: NumPy の float32 を経て層の出力の型に直し、Python の数 sign×coef を掛ける。"""
    import torch
    V32 = np.asarray(vec, dtype=np.float32)
    return int(sign) * float(coef) * torch.as_tensor(V32, dtype=like.dtype, device=like.device)


def forward_rewrite(model, ids, layer_idx, vec, coef, sign, mp, use_cache=False, keep=None):
    """埋め込みから層を手で回し、層 layer_idx の出力の主位置から列の最後までに sign×coef×v を足して後の層を流す。

    返り値: 最後の層の出力（最終の正規化の入力）。keep（dict）を渡すと、自己検査のために層ごとの出力・書き換えの前と後・
    足した量を写しで残す。"""
    _, _, lm = parts(model)
    L, mp, n = int(layer_idx), int(mp), len(ids)
    if not 0 <= L < len(lm.layers):
        _die('層の添字 %s が範囲の外（層の数 %d）' % (layer_idx, len(lm.layers)))
    if not 0 <= mp < n:
        _die('主位置 %s が列の外（長さ %d）' % (mp, n))
    if int(sign) not in (1, -1):
        _die('符号は +1 か -1: %r' % (sign,))
    if np.asarray(vec).shape != (int(lm.config.hidden_size),):
        _die('方向の形 %s が次元（%d）と合わない' % (np.asarray(vec).shape, lm.config.hidden_size))
    done = []

    def on_layer_out(i, h):
        if i == L:
            if keep is not None:
                keep['L_before'] = h.clone()
            add = cast_add(vec, coef, sign, h)
            h[0, mp:, :] = h[0, mp:, :] + add                      # 主位置から後ろに、層の出力の型のまま足す
            done.append(i)
            if keep is not None:
                keep['L_after'] = h.clone()
                keep['add'] = add.clone()
        return h

    h = _forward_impl(model, ids, on_layer_out, use_cache=use_cache, keep=keep)
    if done != [L]:
        _die('書き換えが一度でない: %s' % done)
    return h


def readout(model, h_last, set_ids, cap=None):
    """最終の正規化の入力（一つの位置）を float32 に上げ、最終の正規化・読み取りの集合の行・softcap を float32 で当てる。

    返り値: (量〔z_a − logsumexp(ほか)〕, 出口の値 z〔float32・set_ids の順〕)。"""
    import torch
    top, _, lm = parts(model)
    cap = softcap_value(model) if cap is None else float(cap)
    with torch.no_grad():
        g = lm.norm.weight.to(torch.float32)
        eps = float(lm.norm.eps)
        x = h_last.to(device=g.device, dtype=torch.float32)
        xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g          # 重みをそのまま掛ける（1＋g ではない）
        W = top.lm_head.weight
        idx = torch.as_tensor([int(i) for i in set_ids], dtype=torch.long, device=W.device)
        z = W.index_select(0, idx).to(torch.float32) @ xn.to(W.device)
        z = cap * torch.tanh(z / cap)
        lo = z[0] - torch.logsumexp(z[1:], dim=0)
    return float(lo), z


# ---------------------------------------------------------------- 本の関数

def _check_dirs(model, dirs, used):
    _, _, lm = parts(model)
    d = int(lm.config.hidden_size)
    for dn in used:
        if dn not in dirs:
            _die('方向 %s が dirs に無い' % dn)
        v = dirs[dn]
        if not isinstance(v, np.ndarray) or v.dtype != np.float64:
            _die('方向 %s が float64 の配列でない（%s）' % (dn, getattr(v, 'dtype', type(v).__name__)))
        if v.shape != (d,):
            _die('方向 %s の形 %s が次元（%d）と合わない' % (dn, v.shape, d))
        if not np.all(np.isfinite(v)):
            _die('方向 %s に有限でない値がある' % dn)


def rows_and_dirs(C, ledger, names, pilot):
    """行と方向の組（`bl3_core.recompute_set`）。外した升目は `pilot['decision']['dropped']`。"""
    BC = _pub('bl3_core')
    for k in ('named', 'iso', 'real'):
        if k not in names:
            _die('names に %s の並びが無い' % k)
    real = list(names['real'])
    bad = [x for x in real if not str(x).startswith('real:')]
    if bad:
        _die('names["real"] に real: で始まらない名がある: %s' % bad[:3])
    pair_names = [str(x)[len('real:'):] for x in real]
    iso = list(names['iso'])
    if set(iso) != {'iso:%d' % i for i in range(len(iso))} or len(set(iso)) != len(iso):
        _die('names["iso"] が iso:0〜iso:%d の名の並びでない（recompute_set は iso:番号 の名を作る）' % (len(iso) - 1))
    try:
        dropped = pilot['decision']['dropped']
    except (TypeError, KeyError):
        _die("pilot['decision']['dropped']（外した升目の鍵の並び）が無い")
    if not isinstance(dropped, (list, tuple)) or any(not isinstance(x, str) for x in dropped):
        _die("pilot['decision']['dropped'] が升目の鍵（文字列）の並びでない")
    unknown = [x for x in dropped if x not in ledger['cells_main']]
    if unknown:
        _die("pilot['decision']['dropped'] に台帳 cells_main に無い升目の鍵がある: %s" % unknown)
    rows, dbr = BC.recompute_set(C['main_rows'], pair_names, C['nulls']['real']['swap_siblings'], len(iso), list(dropped))
    return rows, dbr


def recompute_rewrite(model, tok, C, ledger, dirs, names, pilot, coef, use_cache=False):
    """残差の書き換えの道で、v̂ の行ごとに無操作の量と、方向と符号ごとの効き目を計算し直す（近道なし・バッチ一）。

    C: 正本の辞書・ledger: 台帳の辞書・dirs: 方向の名 → float64 のベクトル・names: {'named','iso','real'} の名の並び・
    pilot: 本の凍結の下見の記録（pilot['decision']['dropped'] に外した升目の鍵）・coef: 係数。
    返り値: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}。**値は印字しない。**
    use_cache（既定 False＝use_cache=False と同じ）は、手回しの道の中で DynamicCache を作るかだけを決める（開発の記録）。"""
    check_env(model, C, ledger)
    L = layer_index_for(model, C)
    assert_no_foreign_hooks(model)
    coef = float(coef)
    if not np.isfinite(coef) or coef <= 0:
        _die('係数が正の有限の数でない: %r' % coef)
    rows, dbr = rows_and_dirs(C, ledger, names, pilot)
    used = sorted({dn for nm, _, _ in rows for dn, _ in dbr[nm]})
    _check_dirs(model, dirs, used)
    _, _, lm = parts(model)
    cap = softcap_value(model)
    RB = _pub('run_stageB_local')
    AT = RB.arm_texts()
    zero = np.zeros(int(lm.config.hidden_size), dtype=np.float64)       # 無操作は零のベクトル（同じ算術で足す）
    cells, out = {}, {}
    for name, ck, sign in rows:
        sign = int(sign)
        if sign not in (1, -1):
            _die('行 %s の符号は +1 か -1: %r' % (name, sign))
        if ck not in cells:
            cells[ck] = cell_input(tok, C, ledger, ck, AT=AT)
        c = cells[ck]
        h0 = forward_rewrite(model, c['ids'], L, zero, coef, sign, c['mp'], use_cache=use_cache)
        lo0, _ = readout(model, h0[0, -1], c['set_ids'], cap)
        eff = {}
        for dn, s in dbr[name]:
            s = int(s)
            if s not in (1, -1):
                _die('方向 %s の符号は +1 か -1: %r' % (dn, s))
            key = '%s|%+d' % (dn, s)
            if key in eff:
                _die('行 %s に同じ方向と符号が二度ある: %s' % (name, key))
            h = forward_rewrite(model, c['ids'], L, dirs[dn], coef, s, c['mp'], use_cache=use_cache)
            lo, _ = readout(model, h[0, -1], c['set_ids'], cap)
            eff[key] = lo - lo0
        out[name] = {'noop_lo': lo0, 'effects': eff}
    assert_no_foreign_hooks(model)
    return out


# ---------------------------------------------------------------- 乱数の小さな模型と合成の方向（確かめだけ）

def tiny_config_dict(C, variant=None):
    """設定の置き場の config.json を辞書で読み、text_config と vision_config を縮める（指示の作り方）。
    variant='ple_scalar' は、層ごとの入力（hidden_size_per_layer_input 8）を足した自己検査の変種。"""
    DB = _pub('direction_B')
    d = json.load(open(os.path.join(HF_DIR, 'config.json'), encoding='utf-8'))
    tc = d['text_config']
    tc.update(TINY_TEXT)
    n = int(TINY_TEXT['num_hidden_layers'])
    L = DB.layer_index(float(C['layers']['ratio']), n)
    tc['layer_types'] = ['full_attention' if i in (L, n - 1) else 'sliding_attention' for i in range(n)]
    d['vision_config'].update(TINY_VISION)
    if variant == 'ple_scalar':
        tc['hidden_size_per_layer_input'] = 8
    elif variant is not None:
        _die('小さな模型の変種の名が違う: %s' % variant)
    return d


def tiny_model(C, variant=None):
    """乱数の小さな模型（**実の重みは読まない**）。torch.manual_seed(0) → Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).eval()
    → 語彙の行列（埋め込みと共有）を 4 倍 → 最後の正規化の重みを一様乱数 [2, 3) に（生成器の種 1）。型は設定の dtype のまま。
    variant='ple_scalar' では、さらに層ごとの layer_scalar を一様乱数 [0.5, 1.5) にする（本の模型は layer_scalar を読み込む）。"""
    import torch
    from transformers import Gemma4Config, Gemma4ForConditionalGeneration
    d = tiny_config_dict(C, variant)
    torch.manual_seed(0)
    model = Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).eval()
    top, _, lm = parts(model)
    g = torch.Generator().manual_seed(1)
    with torch.no_grad():
        lm.embed_tokens.weight.mul_(4.0)
        lm.norm.weight.copy_(torch.rand(lm.norm.weight.shape, generator=g) + 2.0)
        if variant == 'ple_scalar':
            for layer in lm.layers:
                layer.layer_scalar.copy_(torch.rand(layer.layer_scalar.shape, generator=g) + 0.5)
    if top.lm_head.weight is not lm.embed_tokens.weight:
        _die('小さな模型で語彙の行列が埋め込みと共有でない')
    return model


def as_dtype(model, dtype):
    """同じ重みの写しを別の型で（float32 の確かめ用）。共有の語彙の行列が共有のままかを確かめる。"""
    m = copy.deepcopy(model).to(dtype).eval()
    top, _, lm = parts(m)
    if top.lm_head.weight is not lm.embed_tokens.weight:
        _die('型を替えた写しで語彙の行列の共有が切れた')
    return m


def assert_tiny(model):
    """確かめは乱数の小さな模型だけで走らせる（封印の前に本物の模型で読み取りの値を出さない）。"""
    _, _, lm = parts(model)
    if int(lm.config.hidden_size) != TINY_TEXT['hidden_size'] or len(lm.layers) != TINY_TEXT['num_hidden_layers']:
        _die('確かめは乱数の小さな模型だけで走らせる（次元 %s・層 %s）' % (lm.config.hidden_size, len(lm.layers)))


def residual_norm(model, tok, C, ledger, L, AT=None):
    """残差のノルム: 主の八升目の、層 L の出力（書き換えなし）の主位置のノルムの平均。"""
    import torch
    _, _, lm = parts(model)
    zero = np.zeros(int(lm.config.hidden_size))
    ns = []
    for ck in ledger['cells_main']:
        c = cell_input(tok, C, ledger, ck, AT=AT)
        keep = {}
        forward_rewrite(model, c['ids'], L, zero, 1.0, 1, c['mp'], keep=keep)
        ns.append(float(torch.linalg.vector_norm(keep['L_before'][0, c['mp']].to(torch.float64))))
    return float(np.mean(ns)), ns


def synthetic_dirs(C, d, target_norm, n_iso=TINY_N_ISO):
    """合成の方向: `np.random.default_rng(5)` で次元 d の正規乱数を名の順に引き、ノルムを target_norm にそろえる。
    名の順は static・loaded・Nk・td（正本 directions.named）・iso:0〜・real:＋正本の八腕（nulls.real.arms）の全ての対（i<j）。"""
    arms = list(C['nulls']['real']['arms'])
    pairs = ['%s~%s' % (arms[i], arms[j]) for i in range(len(arms)) for j in range(i + 1, len(arms))]
    named = list(C['directions']['named'])
    iso = ['iso:%d' % k for k in range(n_iso)]
    real = ['real:' + p for p in pairs]
    rng = np.random.default_rng(5)
    dirs = {}
    for nm in named + iso + real:
        v = rng.normal(size=d)
        dirs[nm] = v * (float(target_norm) / float(np.linalg.norm(v)))
    return dirs, {'named': named, 'iso': iso, 'real': real}


def dry_rows(C, ledger):
    """主の行のうち方向が static の行から、減算の行（main_rows の順で最初）と、族を両方覆うため減算の行と違う族の最初の加算の行。"""
    fam = lambda r: ledger['cells_main']['%s|%s' % (r['scenario'], r['base'])]['family']
    main = [r for r in C['main_rows'] if r['direction'] == 'static']
    sub = next(r for r in main if int(r['sign']) == -1)
    add = next((r for r in main if int(r['sign']) == 1 and fam(r) != fam(sub)), None) or \
        next(r for r in main if int(r['sign']) == 1)
    return [(r['id'], '%s|%s' % (r['scenario'], r['base']), int(r['sign'])) for r in (sub, add)]


def max_abs_diff(A, B):
    """二つの結果の、全ての効き目と無操作の量の差の絶対値の最大（行か鍵の集合が違えば None）。"""
    if set(A) != set(B):
        return None
    de, dn, n = 0.0, 0.0, 0
    for nm in A:
        ea, eb = A[nm]['effects'], B[nm]['effects']
        if set(ea) != set(eb):
            return None
        for k in ea:
            de = max(de, abs(float(ea[k]) - float(eb[k])))
            n += 1
        dn = max(dn, abs(float(A[nm]['noop_lo']) - float(B[nm]['noop_lo'])))
    return {'effects': de, 'noop': dn, 'n_effects': n}


def _dtype_name(model):
    _, _, lm = parts(model)
    return str(lm.embed_tokens.weight.dtype).replace('torch.', '')


def _tiny_desc(model, L):
    """小さな模型の形の一行（頭の次元と KV の頭は層ごとの値なので層の部品から読む）。"""
    _, _, lm = parts(model)
    lt = lm.config.layer_types

    def att(i):
        a = lm.layers[i].self_attn
        return 'KV の頭 %d・頭の次元 %d' % (lm.config.num_attention_heads // a.num_key_value_groups, a.head_dim)
    i_s = next(i for i, t in enumerate(lt) if t == 'sliding_attention')
    return ('次元 %d・層 %d（%s）・注意の頭 %d・窓つきの層 %s・全体の層 %s・窓 %d・選んだ層の添字 %d（%s）・'
            '埋め込みの倍率 %s・softcap %s・係数 %s'
            % (int(lm.config.hidden_size), len(lm.layers), '/'.join('F' if t == 'full_attention' else 'S' for t in lt),
               lm.config.num_attention_heads, att(i_s), att(L), lm.config.sliding_window, L, lt[L],
               lm.embed_tokens.scalar_embed_scale, softcap_value(model), TINY_COEF))


# ---------------------------------------------------------------- 自己検査

def _selftest():
    import torch
    import transformers
    from transformers import AutoTokenizer
    C, LG = load_canon(), load_ledger()
    RB = _pub('run_stageB_local')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    base = tiny_model(C)
    models = [('float32', as_dtype(base, torch.float32)), ('bfloat16', base)]
    res = []

    def ck(label, ok, detail=''):
        res.append(bool(ok))
        print('[%s] %s%s' % ('ok' if ok else 'NG', label, ('  | ' + detail) if detail else ''), flush=True)

    def stops(fn):
        try:
            fn()
        except SystemExit as e:
            return True, str(e)
        return False, ''

    m32 = models[0][1]
    for _, m in models:
        assert_tiny(m)
    _, _, lm32 = parts(m32)
    L = layer_index_for(m32, C)
    d = int(lm32.config.hidden_size)
    print('bprime_recompute_rewrite %s --selftest  torch %s・transformers %s・numpy %s・注意の実装 %s・作ったままの型 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, lm32.config._attn_implementation,
             _dtype_name(base)), flush=True)
    print('乱数の小さな模型: %s' % _tiny_desc(m32, L), flush=True)

    # (1) 升目の組み立て（主の八升目）
    CI = {k: cell_input(tok, C, LG, k, AT=AT) for k in LG['cells_main']}
    ck('升目の組み立てが台帳と一致（全 %d 升目・長さ・主位置とそのトークン・読み取りの位置・ids_sha16・族・読み取りの集合）' % len(CI), True,
       '・'.join('%s %d/%d/%d' % (k, c['prompt_len'], c['mp'], c['ro']) for k, c in CI.items()))
    for fld, dv in (('prompt_len', 1), ('main_position', 1), ('readout_position', -1)):
        LG2 = copy.deepcopy(LG)
        LG2['cells_main']['S1|O-Ncold'][fld] += dv
        ok, _ = stops(lambda: cell_input(tok, C, LG2, 'S1|O-Ncold', AT=AT))
        ck('台帳と違えば止まる（S1|O-Ncold の %s を %+d ずらした写し）' % (fld, dv), ok)
    LG2 = copy.deepcopy(LG)
    LG2['cells_main']['S1|O-Ncold']['ids_sha16'] = '0' * 16
    ck('台帳と違えば止まる（S1|O-Ncold の ids_sha16 を書き換えた写し）', stops(lambda: cell_input(tok, C, LG2, 'S1|O-Ncold', AT=AT))[0])
    LG2 = copy.deepcopy(LG)
    LG2['prefix_ids'] = list(LG2['prefix_ids'])[:-1]
    ck('主の書き出しが正本と違えば止まる（最後のトークンを落とした写し）', stops(lambda: cell_input(tok, C, LG2, 'S1|O-Ncold', AT=AT))[0])

    zero = np.zeros(d)
    probe = ['N1|O-Ncold', 'S1|Onull']
    # (2) 書き換えを零にした手回しの道の最終の正規化の入力 ＝ 模型そのものの forward の最終の正規化の入力（前の hook で取るだけ）
    for tn, m in models:
        top, _, lm = parts(m)
        cap_v = softcap_value(m)
        for k in probe:
            c = CI[k]
            x = torch.tensor([c['ids']], dtype=torch.long)
            for uc, label in ((False, 'use_cache=False'), (None, '既定（設定の use_cache）')):
                cap = {}
                hd = lm.norm.register_forward_pre_hook(lambda mod, a: cap.__setitem__('x', a[0].detach().clone()))
                try:
                    with torch.no_grad():
                        o = m(input_ids=x, logits_to_keep=1) if uc is None else m(input_ids=x, use_cache=uc, logits_to_keep=1)
                finally:
                    hd.remove()
                assert_no_foreign_hooks(m)
                keep = {}
                h = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=uc, keep=keep)
                md = float((h.float() - cap['x'].float()).abs().max())
                ck('[%s] %s %s: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）' % (tn, k, label),
                   torch.equal(h, cap['x']), '差の絶対値の最大 %.3g・形 %s・型 %s' % (md, tuple(h.shape), h.dtype))
                mk = keep['masks']
                print('[参考] [%s] %s %s: 手回しの道の mask は %s・cache %s（判定に入れない）'
                      % (tn, k, label, '・'.join('%s=%s' % (t, 'None' if v is None else '明示 %s %s' % (v.dtype, tuple(v.shape)))
                                                  for t, v in sorted(mk.items())), '作る' if keep['use_cache'] else '作らない'), flush=True)
                if uc is False:
                    lo, z = readout(m, h[0, -1], c['set_ids'])
                    ref = o.logits[0, -1, c['set_ids']].float()
                    dz = float((z - ref).abs().max())
                    if tn == 'float32':
                        ck('[%s] %s: 読み取りの集合の出口の値（float32・softcap 後）が模型の出口の値と一致（書き手の許容 1e-4）' % (tn, k),
                           dz <= 1e-4, '差の絶対値の最大 %.3g' % dz)
                    else:
                        print('[参考] [%s] %s: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差の最大 %.3g（判定に入れない）'
                              % (tn, k, dz), flush=True)
                    # 歯: 正規化の後の値（hidden_states[-1]）を正規化の入力と取り違えると、模型の出口の値から離れる
                    with torch.no_grad():
                        o2 = m(input_ids=x, output_hidden_states=True, logits_to_keep=1)
                    hs = o2.hidden_states
                    _, zw = readout(m, hs[-1][0, -1], c['set_ids'])
                    dzw = float((zw - ref).abs().max())
                    ck('[%s] %s: 歯——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 10 倍を超える' % (tn, k),
                       dzw > 10 * max(dz, 1e-7), '取り違え %.3g・正しい %.3g' % (dzw, dz))
                    ck('[%s] %s: hidden_states は層の数＋1 で、[-1] は正規化の後（最終の正規化の入力と違う）' % (tn, k),
                       len(hs) == len(lm.layers) + 1 and not torch.equal(hs[-1], cap['x']))
                    ck('[%s] %s: 手回しの層 %d の出力（書き換えの前）が hidden_states[%d] と一致（ビット単位）' % (tn, k, L, L + 1),
                       torch.equal(keep['L_before'], hs[L + 1]))
                    # 歯: 1＋g・softcap の抜けは模型の出口の値から離れる
                    with torch.no_grad():
                        xf = h[0, -1].float()
                        xn1 = xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + float(lm.norm.eps)) * (1.0 + lm.norm.weight.float())
                        zr = top.lm_head.weight.index_select(0, torch.as_tensor(c['set_ids'])).float() @ xn1
                        z1 = cap_v * torch.tanh(zr / cap_v)
                        xn = xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + float(lm.norm.eps)) * lm.norm.weight.float()
                        zn = top.lm_head.weight.index_select(0, torch.as_tensor(c['set_ids'])).float() @ xn
                    d1 = float((z1 - ref).abs().max())
                    dn_ = float((zn - ref).abs().max())
                    ck('[%s] %s: 歯——1＋g で正規化した読み取りの差が、正しい読み取りの差の 10 倍を超える' % (tn, k),
                       d1 > 10 * max(dz, 1e-7), '1＋g %.3g・正しい %.3g' % (d1, dz))
                    print('[参考] [%s] %s: softcap を抜いた読み取りと模型の出口の値の差の最大 %.3g（正しい %.3g・判定に入れない）'
                          % (tn, k, dn_, dz), flush=True)
        # 二つの cache の形の手回しの道が同じ値か（この CPU で・参考）
        c = CI[probe[0]]
        hA = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=False)
        hB = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=None)
        print('[参考] [%s] use_cache=False と既定の手回しの道の最終の正規化の入力がビット単位で同じ: %s（判定に入れない）'
              % (tn, torch.equal(hA, hB)), flush=True)

    # (3) 主位置より前の位置は書き換えない・足した量は sign×coef×v
    AT_ = AT
    rn, _ = residual_norm(m32, tok, C, LG, L, AT=AT_)
    dirs, names = synthetic_dirs(C, d, SYN_NORM_FRAC * rn)
    print('[参考] 残差のノルム（層 %d の出力の主位置・八升目の平均・float32）%.4g → 合成の方向のノルム %.4g（× %s）'
          % (L, rn, SYN_NORM_FRAC * rn, SYN_NORM_FRAC), flush=True)
    for tn, m in models:
        for k, sign in (('N1|O-Ncold', -1), ('S1|Onull', +1)):
            c = CI[k]
            mp = c['mp']
            k0, k1 = {}, {}
            h0 = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, sign, mp, keep=k0)
            h1 = forward_rewrite(m, c['ids'], L, dirs['static'], TINY_COEF, sign, mp, keep=k1)
            ck('[%s] %s 符号 %+d: 層 %d より前の層の出力は無操作と同じ（ビット単位）' % (tn, k, sign, L),
               all(torch.equal(k0['outs'][i], k1['outs'][i]) for i in range(L)))
            ck('[%s] %s 符号 %+d: 層 %d の出力（書き換えの前）は無操作と同じ（ビット単位）' % (tn, k, sign, L),
               torch.equal(k0['L_before'], k1['L_before']))
            ck('[%s] %s 符号 %+d: 書き換えは主位置（%d）より前の位置を変えない（層 %d の出力・ビット単位）' % (tn, k, sign, mp, L),
               torch.equal(k1['L_after'][:, :mp], k1['L_before'][:, :mp]))
            ck('[%s] %s 符号 %+d: 主位置から列の最後まで（%d 位置）に同じ量を足した（ビット単位）' % (tn, k, sign, len(c['ids']) - mp),
               torch.equal(k1['L_after'][:, mp:], k1['L_before'][:, mp:] + k1['add']))
            want_add = int(sign) * float(TINY_COEF) * torch.as_tensor(np.asarray(dirs['static'], dtype=np.float32), dtype=k1['add'].dtype)
            ck('[%s] %s 符号 %+d: 足した量が「float32 を経て層の出力の型に直した v」× sign×coef（型 %s・ビット単位）'
               % (tn, k, sign, k1['add'].dtype), torch.equal(k1['add'], want_add))
            dv = (k1['L_after'][0, mp:].double() - k1['L_before'][0, mp:].double()).numpy()
            want = sign * TINY_COEF * dirs['static']
            cos = float(np.min(dv @ want / (np.linalg.norm(dv, axis=1) * np.linalg.norm(want))))
            rel = float(np.max(np.abs(np.linalg.norm(dv, axis=1) / np.linalg.norm(want) - 1.0)))
            ck('[%s] %s 符号 %+d: 層の出力の差の向きと大きさが sign×coef×v（型の丸めの内）' % (tn, k, sign),
               cos > 0.999 and rel < 0.02, '余弦の最小 %.6f・ノルムの相対の差の最大 %.3g' % (cos, rel))
            ck('[%s] %s 符号 %+d: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う' % (tn, k, sign),
               torch.equal(h1[:, :mp], h0[:, :mp]) and all(not torch.equal(h1[0, p], h0[0, p]) for p in range(mp, len(c['ids']))))
    n_same = sum(torch.equal(torch.as_tensor(np.asarray(v, dtype=np.float32), dtype=torch.bfloat16),
                             torch.as_tensor(v, dtype=torch.bfloat16)) for v in dirs.values())
    print('[参考] float32 を経た bf16 と float64 から直に直した bf16 が同じ合成の方向: %d/%d（判定に入れない）' % (n_same, len(dirs)), flush=True)

    # (4) 本の関数: 零のベクトルの効き目は零・形・二度同じ・外した升目・歯
    rows2 = dry_rows(C, LG)
    keep_cells = {ck_ for _, ck_, _ in rows2}
    pilot2 = {'decision': {'dropped': [k for k in LG['cells_main'] if k not in keep_cells]}}
    BC = _pub('bl3_core')
    want_rows, want_dbr = BC.recompute_set(C['main_rows'], [x[5:] for x in names['real']], C['nulls']['real']['swap_siblings'],
                                           len(names['iso']), pilot2['decision']['dropped'])
    for tn, m in models:
        zdirs = {k: np.zeros(d) for k in dirs}
        rz = recompute_rewrite(m, tok, C, LG, zdirs, names, pilot2, TINY_COEF)
        allz = all(v == 0.0 for r in rz.values() for v in r['effects'].values())
        ck('[%s] 零のベクトルの効き目が全て零（%d 行・効き目 %d 個・両方の符号）' % (tn, len(rz), sum(len(r['effects']) for r in rz.values())), allz)
        t0 = time.time()
        r1 = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
        dt = time.time() - t0
        r1b = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
        ck('[%s] 同じ呼び出しを二度走らせて同じ値（ビット単位）' % tn, r1 == r1b, '一度 %.1f 秒' % dt)
        shape_ok = (list(r1) == [nm for nm, _, _ in want_rows]
                    and all(list(r1[nm]['effects']) == ['%s|%+d' % (dn, s) for dn, s in want_dbr[nm]] for nm in r1)
                    and all(isinstance(r1[nm]['noop_lo'], float) for nm in r1))
        ck('[%s] 出力の形 {行の名: {noop_lo, effects: {方向の名|符号: 効き目}}}（行と方向の組は recompute_set のとおり・符号の書き方 %%+d）' % tn,
           shape_ok, '行 %s・効き目の数 %s・鍵の例 %s' % (list(r1), [len(r1[nm]['effects']) for nm in r1],
                                                    list(r1[list(r1)[0]]['effects'])[:2]))
        ck('[%s] 外した升目の行は計算しない（外していない升目の static の行だけ）' % tn,
           set(r1) == {nm for nm, ck_, _ in rows2})
        st = [r1[nm]['effects']['static|%+d' % s] for nm, _, s in rows2]
        ck('[%s] 歯——static の効き目は零でない' % tn, all(abs(v) > 0 for v in st), '・'.join('%.4g' % v for v in st))
        if tn == 'float32':
            ok, _ = stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, {'decision': {'dropped': ['S9|X']}}, TINY_COEF))
            ck('外した升目の鍵が台帳に無ければ止まる', ok)
            ok, _ = stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, {'decision': {}}, TINY_COEF))
            ck("pilot['decision']['dropped'] が無ければ止まる", ok)
            nm2 = copy.deepcopy(names)
            nm2['real'][0] = nm2['real'][0][len('real:'):]
            ck('names["real"] に real: で始まらない名があれば止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, nm2, pilot2, TINY_COEF))[0])
            d2 = dict(dirs)
            d2.pop('iso:3')
            ck('dirs に要る方向が無ければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, d2, names, pilot2, TINY_COEF))[0])
            d2 = dict(dirs)
            d2['static'] = dirs['static'].astype(np.float32)
            ck('方向が float64 でなければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, d2, names, pilot2, TINY_COEF))[0])
            d2 = dict(dirs)
            d2['static'] = dirs['static'][:-1].copy()
            ck('方向の形が次元と合わなければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, d2, names, pilot2, TINY_COEF))[0])
            ck('係数が正でなければ止まる', stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, 0.0))[0])
            _, _, lmx = parts(m)
            hd = lmx.layers[L].register_forward_hook(lambda mod, a, o: None)
            try:
                ok, _ = stops(lambda: recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF))
            finally:
                hd.remove()
            ck('模型に forward の hook が掛かっていれば止まる（選んだ層に何もしない hook を掛けた写し）', ok)
            nc = capture_hook_count(m)
            r1c = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
            ck('transformers の記録用の hook（output_hidden_states の後に居残る %d 本）は数えず、値も変わらない（ビット単位）' % nc,
               nc > 0 and r1c == r1)
            import torch.nn as nn

            def _boom(*a, **k):
                raise RuntimeError('forward の hook を掛けようとした')
            saved = {nm_: nn.Module.__dict__[nm_] for nm_ in ('register_forward_hook', 'register_forward_pre_hook')}
            for nm_ in saved:
                setattr(nn.Module, nm_, _boom)
            try:
                r1d = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF)
                okh = r1d == r1
            except RuntimeError:
                okh = False
            finally:
                for nm_, fn_ in saved.items():
                    setattr(nn.Module, nm_, fn_)
            ck('呼び出しの間に forward の hook を掛けようとしない（nn.Module の register_forward_hook と register_forward_pre_hook を'
               '落ちる形に差し替えて走らせ、値も同じ）', okh)
            r_uc = recompute_rewrite(m, tok, C, LG, dirs, names, pilot2, TINY_COEF, use_cache=None)
            dd = max_abs_diff(r1, r_uc)
            print('[参考] [%s] use_cache=None（DynamicCache を作る形）と既定の形の差の最大: 効き目 %.3g・無操作 %.3g（判定に入れない）'
                  % (tn, dd['effects'], dd['noop']), flush=True)

    # (5) 層ごとの入力と layer_scalar のある変種でも、手回しの道は模型の forward と一致（本の模型は layer_scalar を読み込む）
    vbase = tiny_model(C, variant='ple_scalar')
    for tn, m in (('float32', as_dtype(vbase, torch.float32)), ('bfloat16', vbase)):
        _, _, lm = parts(m)
        c = CI['S1|Onull']
        x = torch.tensor([c['ids']], dtype=torch.long)
        cap = {}
        hd = lm.norm.register_forward_pre_hook(lambda mod, a: cap.__setitem__('x', a[0].detach().clone()))
        try:
            with torch.no_grad():
                m(input_ids=x, use_cache=False, logits_to_keep=1)
        finally:
            hd.remove()
        h = forward_rewrite(m, c['ids'], L, zero, TINY_COEF, +1, c['mp'], use_cache=False)
        ck('[%s] 層ごとの入力（%d）と layer_scalar（%s…）のある変種でも、手回しの道の最終の正規化の入力が模型の forward と一致（ビット単位）'
           % (tn, lm.config.hidden_size_per_layer_input, '・'.join('%.3f' % float(ly.layer_scalar) for ly in lm.layers[:2])),
           torch.equal(h, cap['x']))
    n_ok = sum(res)
    print('selftest: %d/%d ok' % (n_ok, len(res)), flush=True)
    print('柵: ' + FENCE, flush=True)
    return n_ok == len(res)


# ---------------------------------------------------------------- 突き合わせ（--dry）

def _hook_path(model, tok, C, LG, dirs, rows, dbr, L, coef):
    """コーディネータのフックの道（公開の関数を中を見ずに呼ぶ）。"""
    sys.path.insert(0, os.path.join(BPRIME, 'tools'))
    import bprime_run as BR
    R = BR.Runner(model, C, L, coef, dirs)
    cells = BR.build_cells(tok, C, LG, sorted({ck_ for _, ck_, _ in rows}))
    return BR.recompute_hook_path(R, [(nm, cells[ck_], s) for nm, ck_, s in rows], {nm: list(dbr[nm]) for nm, _, _ in rows})


def _dry(teeth=True):
    import torch
    import transformers
    from transformers import AutoTokenizer
    C, LG = load_canon(), load_ledger()
    tol = float(C['independent_recompute']['tol_stage1'])
    RB = _pub('run_stageB_local')
    BC = _pub('bl3_core')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    base = tiny_model(C)
    m32 = as_dtype(base, torch.float32)
    for m in (m32, base):
        assert_tiny(m)
    L = layer_index_for(m32, C)
    _, _, lm32 = parts(m32)
    d = int(lm32.config.hidden_size)
    rn, _ = residual_norm(m32, tok, C, LG, L, AT=AT)
    dirs, names = synthetic_dirs(C, d, SYN_NORM_FRAC * rn)
    rows = dry_rows(C, LG)
    keep_cells = {ck_ for _, ck_, _ in rows}
    pilot = {'decision': {'dropped': [k for k in LG['cells_main'] if k not in keep_cells]}}
    want_rows, dbr = BC.recompute_set(C['main_rows'], [x[5:] for x in names['real']], C['nulls']['real']['swap_siblings'],
                                      len(names['iso']), pilot['decision']['dropped'])
    print('bprime_recompute_rewrite %s --dry  torch %s・transformers %s・numpy %s・注意の実装 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, lm32.config._attn_implementation), flush=True)
    print('乱数の小さな模型: 次元 %d・層 %d・選んだ層の添字 %d・窓 %d・係数 %s・合成の方向のノルム %.4g（残差のノルム %.4g × %s）・'
          '一段目の許容 independent_recompute.tol_stage1 = %s'
          % (d, len(lm32.layers), L, lm32.config.sliding_window, TINY_COEF, SYN_NORM_FRAC * rn, rn, SYN_NORM_FRAC, tol), flush=True)
    for nm, ck_, s in rows:
        kinds = {'static': 0, 'iso': 0, 'real': 0}
        for dn, _ in dbr[nm]:
            kinds['static' if dn == 'static' else dn.split(':')[0]] += 1
        print('行 %s・升目 %s（%s）・符号 %+d・方向と符号 %d 組（static %d・等方 %d・比べる相手の実在の差 %d＝%d 対 × 両方の向き）＋無操作'
              % (nm, ck_, LG['cells_main'][ck_]['family'], s, len(dbr[nm]), kinds['static'], kinds['iso'], kinds['real'],
                 kinds['real'] // 2), flush=True)
    verdicts = []
    for tn, m in (('float32', m32), ('bfloat16', base)):
        t0 = time.time()
        mine = recompute_rewrite(m, tok, C, LG, dirs, names, pilot, TINY_COEF)
        t1 = time.time()
        if list(mine) != [nm for nm, _, _ in want_rows]:
            print('[%s] 残差の書き換えの道の行が選んだ二行と違う: %s' % (tn, list(mine)), flush=True)
            verdicts.append(False)
            continue
        try:
            hook = _hook_path(m, tok, C, LG, dirs, rows, dbr, L, TINY_COEF)
        except BaseException as e:                                    # 中の行を出さない（中を見ない）
            print('[%s] フックの道が落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
            verdicts.append(False)
            continue
        t2 = time.time()
        dd = max_abs_diff(mine, hook)
        n_eff = sum(len(r['effects']) for r in mine.values())
        amax = max(abs(v) for r in mine.values() for v in r['effects'].values())
        print('[%s] 残差の書き換えの道 %.1f 秒（順伝播 %d 回）・フックの道 %.1f 秒' % (tn, t1 - t0, n_eff + len(mine), t2 - t1), flush=True)
        if dd is None:
            print('[%s] 二つの道の行か鍵の集合が違う（残差の書き換えの道 %s 行・フックの道 %s 行）' % (tn, len(mine), len(hook) if hasattr(hook, '__len__') else '?'), flush=True)
            verdicts.append(False)
            continue
        print('[%s] 効き目の数 %d・効き目の絶対値の最大（残差の書き換えの道）%.4g' % (tn, n_eff, amax), flush=True)
        print('[%s] 差の絶対値の最大: 効き目 %.3g・無操作の量 %.3g' % (tn, dd['effects'], dd['noop']), flush=True)
        ok = dd['effects'] <= tol and dd['noop'] <= tol
        verdicts.append(ok)
        print('[%s] dry: 一段目の許容（%s）の%s（差の最大 %.3g）' % (tn, tol, '内' if ok else '外', max(dd['effects'], dd['noop'])), flush=True)
        try:                                                           # 参考の行（止まっても判定は変えず、文言を印字して続ける）
            again = recompute_rewrite(m, tok, C, LG, dirs, names, pilot, TINY_COEF)
            print('[参考] [%s] フックの道の後に走らせ直した残差の書き換えの道が一度目と同じ（ビット単位）: %s・居残る hook（記録用を除く）%d 本'
                  % (tn, again == mine, len(foreign_hooks(m))), flush=True)
        except SystemExit as e:
            print('[参考] [%s] フックの道の後の走らせ直しが止まった: %s' % (tn, str(e)[:300]), flush=True)
        try:
            uc = recompute_rewrite(m, tok, C, LG, dirs, names, pilot, TINY_COEF, use_cache=None)
            d2 = max_abs_diff(uc, hook)
            d3 = max_abs_diff(uc, mine)
            print('[参考] [%s] use_cache=None（DynamicCache を作る形）の残差の書き換えの道——既定の形との差の最大 効き目 %.3g・無操作 %.3g／'
                  'フックの道との差の最大 効き目 %.3g・無操作 %.3g' % (tn, d3['effects'], d3['noop'], d2['effects'], d2['noop']), flush=True)
        except SystemExit as e:
            print('[参考] [%s] use_cache=None の走りが止まった: %s' % (tn, str(e)[:300]), flush=True)
        if teeth:
            _teeth(m, tn, tok, C, LG, dirs, rows, dbr, L, hook, tol, AT)
    print('（正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない）', flush=True)
    print('dry: %s' % ('二つの型とも一段目の許容の内' if verdicts and all(verdicts) else '許容の外か比べられなかった型がある'), flush=True)
    print('柵: ' + FENCE, flush=True)
    return bool(verdicts) and all(verdicts)


def _teeth(model, tn, tok, C, LG, dirs, rows, dbr, L, hook, tol, AT):
    """歯の変種（参考・判定に入れない・事前登録 dry-preregistration-Bprime.txt）: この道をわざと誤らせ、フックの道との差で捕まるかを見る。
    比べる鍵: 行ごとに無操作と、static・iso:0（行の符号）と、その行の最初の比べる相手の実在の差（両方の向き）。"""
    import torch
    _, _, lm = parts(model)
    cap = softcap_value(model)
    d = int(lm.config.hidden_size)
    zero = np.zeros(d)

    def fwd(ids, vec, sign, mp, kind):
        Lx = L + 1 if kind == 'M2' else L
        start = mp + 1 if kind == 'M1' else mp
        coef = TINY_COEF * TINY_COEF if kind == 'M4' else TINY_COEF
        sgn = -sign if kind == 'M3' else sign

        def on_layer_out(i, h):
            if i == Lx:
                if kind == 'M7':
                    add = int(sgn) * float(coef) * torch.as_tensor(np.asarray(vec, dtype=np.float32), device=h.device)
                else:
                    add = cast_add(vec, coef, sgn, h)
                h[0, start:, :] = h[0, start:, :] + add
            return h
        return _forward_impl(model, ids, on_layer_out, use_cache=False)

    def rd(h_last, set_ids, kind):
        if kind not in ('M5', 'M6', 'M8'):
            return readout(model, h_last, set_ids, cap)[0]
        with torch.no_grad():
            g = lm.norm.weight.to(torch.float32)
            eps = float(lm.norm.eps)
            x = h_last.to(torch.float32)
            gg = (1.0 + g) if kind == 'M8' else g
            xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * gg
            if kind == 'M5':
                xn = xn * torch.rsqrt(xn.pow(2).mean(-1, keepdim=True) + eps) * g
            z = lm.embed_tokens.weight.index_select(0, torch.as_tensor(list(set_ids))).to(torch.float32) @ xn
            if kind != 'M6':
                z = cap * torch.tanh(z / cap)
            return float(z[0] - torch.logsumexp(z[1:], dim=0))

    labels = {'M0': '誤らせない（対照）', 'M1': '帯の起点を主位置の一つ後にする', 'M2': '書き換える層を一つ後にする',
              'M3': '符号を反転する', 'M4': '係数を二度掛ける（sign×coef×coef×v）', 'M5': '読み取りで正規化を二度当てる',
              'M6': '読み取りで softcap を抜く', 'M7': '加減を層の出力の型に直さず float32 のまま足す', 'M8': '最終の正規化の重みを 1＋g にする'}
    t0 = time.time()
    cells = {ck_: cell_input(tok, C, LG, ck_, AT=AT) for _, ck_, _ in rows}
    for kind in ('M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'):
        worst, n = 0.0, 0
        for nm, ck_, sign in rows:
            c = cells[ck_]
            first_real = next(dn for dn, _ in dbr[nm] if dn.startswith('real:'))
            probe = [('static', sign), ('iso:0', sign), (first_real, sign), (first_real, -sign)]
            lo0 = rd(fwd(c['ids'], zero, sign, c['mp'], kind)[0, -1], c['set_ids'], kind)
            worst = max(worst, abs(lo0 - float(hook[nm]['noop_lo'])))
            for dn, s in probe:
                lo = rd(fwd(c['ids'], dirs[dn], s, c['mp'], kind)[0, -1], c['set_ids'], kind)
                worst = max(worst, abs((lo - lo0) - float(hook[nm]['effects']['%s|%+d' % (dn, s)])))
                n += 1
        caught = worst > tol
        print('[歯] [%s] %s %s: フックの道との差の最大 %.3g（無操作 %d 個・効き目 %d 個）→ %s（許容 %s）'
              % (tn, kind, labels[kind], worst, len(rows), n,
                 ('許容の内（対照として期待どおり）' if not caught else '許容の外（対照が外れた）') if kind == 'M0'
                 else ('許容の外＝捕まえた' if caught else '許容の内＝捕まえなかった（この模型での盲点）'), tol), flush=True)
    print('[歯] [%s] 変種の計算 %.1f 秒（参考・判定に入れない）' % (tn, time.time() - t0), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--no-teeth', action='store_true')
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.dry:
        sys.exit(0 if _dry(teeth=not a.no_teeth) else 1)
    ap.print_help()


if __name__ == '__main__':
    main()
```

### 5. `tools/independent/bprime_reextract.py`（再抽出の道（別の個体））

- 出所: 作業の置き場 `tools/independent/bprime_reextract.py`・SHA16 AEF215AA0F577E45・24001 字

```python
# -*- coding: utf-8 -*-
"""bprime_reextract.py v1 —— B′（Gemma-4-31B-it）の**独立の再抽出の道**
（2026-09-30・本の器の書き手〔コーディネータ・南無弥勒如来〕と別の系統内の個体が書いた・登録者の裁定 D270 による・独立の目を通っていない）。

正本 `design/contrasts-Bprime.json` の `independent_recompute.reextract`（本の抽出と同じ読み込みの設定・同じ注意の実装と決定性の設定・
バッチ一・bf16 で、違うのは活性を取り出す書き方だけ〔T22〕）・`directions`（named・defs・extraction）・`layers` に従う。
コーディネータの抽出の器（`bprime_directions` ほか）の中身を**読まずに**書いた。`--dry` でだけ、その公開の関数を中を見ずに呼ぶ。

取り出し方（コーディネータの器は層の出力をフックで取り、その層で順伝播を打ち切る。この道はそれと別の書き方）:
  模型そのものの forward を `output_hidden_states=True`・`use_cache=False`・`logits_to_keep=1`・バッチ一で最後まで流し、
  `hidden_states[k+1]`（＝`layers[k]` の出力。[0] は埋め込み、[-1] は最終の正規化の後）の主位置（列の最後のトークン）を取る。
  注: transformers 5.16.1 の `output_hidden_states` は、初回に復号の層（と注意）へ記録用の forward の hook を据え付け、以後も
  （値を変えずに）居残る（`transformers.utils.output_capturing`）。この道はその記録だけを使い、自分では hook を一本も掛けない。
入力: 正本 `directions.extraction` の八腕 × 二場面（プロンプトだけ・書き出しはつながない）を、段階 B の組み立て
  （`run_stageB_local.user_message`・`scenario_and_instruction`）に Gemma のチャットの型を当てて作り、台帳 `extract_contexts` の
  prompt_len・main_position・main_position_token・ids_sha16 と照らす（違えば止める）。
名前のある方向: 腕ごとに二場面の平均（float64）を取り、正本 `directions.defs` の文（h_X − h_Y）どおりに作る
  （static＝O − Osec・loaded＝O-Ncold − Osec-Ncold・Nk＝Nk − N・td＝Onull − N。指示の対応と正本の文が合わなければ止める）。
出力: `reextract` → {文脈の名: float64 のベクトル}・`reextract_all` → {'h_norm_by_context': {文脈: ‖h‖}, 'vhat_norm': ‖static‖,
  'named_cos': {名: その名の方向と dirs[名] の余弦}}。**値は印字しない**（`--dry` が差を印字するのは乱数の小さな模型だけ）。
用法: python bprime_reextract.py --selftest   （乱数の小さな模型で自己検査）
      python bprime_reextract.py --dry        （乱数の小さな模型で、コーディネータの抽出の器と四つの文脈で突き合わせ）
走らせ方: PYTHONPATH=<Bprime>/pylib（transformers 5.16.1）・PYTHONDONTWRITEBYTECODE=1 を勧める。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import sys
if __name__ == '__main__':
    sys.dont_write_bytecode = True          # 外の置き場（公開の置き場・pylib・Bprime/tools）に .pyc を書かない
import os, re, json, time, copy, hashlib, argparse
import numpy as np

VERSION = 'v1'
HERE = os.path.dirname(os.path.abspath(__file__))
BPRIME = os.path.dirname(os.path.dirname(HERE))
CANON_PATH = os.path.join(BPRIME, 'design', 'contrasts-Bprime.json')
LEDGER_PATH = os.path.join(BPRIME, 'tools', 'ledger-bprime.json')
HF_DIR = os.path.join(BPRIME, 'hf', 'gemma-4-31B-it', '842da3794eaa0b77d5f08bae87a17459d91ff475')   # 設定とトークナイザだけ（実の重みは無い・使わない）
PUB_TOOLS_DEFAULT = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b/tools'          # 公開の置き場の凍結の器（読むだけ）
CAPTURE_MODULE = 'transformers.utils.output_capturing'
FENCE = '本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
# 指示に書かれた名前のある方向の対応（正本 directions.defs の文と照らす）
INSTR_DEFS = {'static': ('O', 'Osec'), 'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}
DRY_CONTEXTS = ['N1|O', 'S1|Osec', 'N1|Nk', 'S1|O-Ncold']     # --dry で比べる四つ（二場面・四つの腕・長さの違う列）


def _die(msg):
    raise SystemExit('bprime_reextract: ' + msg)


def _pub(name):
    """公開の置き場の凍結の器を import する（読むだけ・環境変数 OP4B_PUB_TOOLS で置き場を替えられる）。"""
    import importlib
    d = os.environ.get('OP4B_PUB_TOOLS', PUB_TOOLS_DEFAULT)
    if os.path.isdir(d) and d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module(name)


def load_canon():
    return json.load(open(CANON_PATH, encoding='utf-8'))


def load_ledger():
    return json.load(open(LEDGER_PATH, encoding='utf-8'))


def sha16_ids(ids):
    """台帳の ids_sha16 の決まり: sha256(','.join(str(x))) の十六進の大文字の頭 16 字。"""
    return hashlib.sha256(','.join(str(int(x)) for x in ids).encode('ascii')).hexdigest().upper()[:16]


def parts(model):
    if type(model).__name__ != 'Gemma4ForConditionalGeneration':
        _die('模型の最上位が Gemma4ForConditionalGeneration でない: %s' % type(model).__name__)
    mm = getattr(model, 'model', None)
    if mm is None or type(mm).__name__ != 'Gemma4Model':
        _die('多様式の本体が Gemma4Model でない: %s' % type(mm).__name__)
    lm = getattr(mm, 'language_model', None)
    if lm is None or type(lm).__name__ != 'Gemma4TextModel':
        _die('言語の模型が Gemma4TextModel でない: %s' % type(lm).__name__)
    return model, mm, lm


def is_capture_hook(fn):
    return getattr(fn, '__module__', None) == CAPTURE_MODULE and getattr(fn, '__name__', None) == 'output_capturing_hook'


def foreign_hooks(model):
    """transformers の記録用の hook を除いた forward の hook（前・後）と大域の hook の一覧。"""
    import torch.nn.modules.module as M
    bad = []
    for name, m in model.named_modules():
        for attr in ('_forward_hooks', '_forward_pre_hooks'):
            for _, fn in (getattr(m, attr, None) or {}).items():
                if attr == '_forward_hooks' and is_capture_hook(fn):
                    continue
                bad.append('%s.%s（%s.%s）' % (name or '<模型>', attr, getattr(fn, '__module__', '?'),
                                             getattr(fn, '__qualname__', type(fn).__name__)))
    for attr in ('_global_forward_hooks', '_global_forward_pre_hooks'):
        d = getattr(M, attr, None)
        if d:
            bad.append('大域の %s %d 本' % (attr, len(d)))
    return bad


def capture_hook_count(model):
    return sum(1 for _, m in model.named_modules() for fn in (getattr(m, '_forward_hooks', None) or {}).values()
               if is_capture_hook(fn))


def assert_no_foreign_hooks(model):
    bad = foreign_hooks(model)
    if bad:
        _die('模型に forward の hook が掛かっている（この道は hook を掛けず、掛け残しも混ぜない）: ' + '・'.join(bad))


def is_real(model, C):
    _, _, lm = parts(model)
    mf = C['inputs']['model_facts']
    return len(lm.layers) == int(mf['num_hidden_layers']) and int(lm.config.hidden_size) == int(mf['hidden_size'])


def layer_for(model, C):
    """選ぶ層の添字: `direction_B.layer_index(正本 layers.ratio, 模型の層の数)`。本の模型では正本 `layers.index` とも照らす。"""
    DB = _pub('direction_B')
    _, _, lm = parts(model)
    n = len(lm.layers)
    L = DB.layer_index(float(C['layers']['ratio']), n)
    if is_real(model, C) and (L != int(C['layers']['index']) or int(C['layers']['hidden_states_index']) != L + 1):
        _die('層の添字 %d が正本 layers.index（%s）・hidden_states_index（%s）と合わない'
             % (L, C['layers']['index'], C['layers']['hidden_states_index']))
    return L


# ---------------------------------------------------------------- 取り出し

def reextract(model, contexts, layer_idx):
    """文脈の名 → 選んだ層の出力の主位置（列の最後のトークン）の値（float64 の numpy の並び）。

    模型そのものの forward（output_hidden_states=True・use_cache=False・logits_to_keep=1・バッチ一・列の全体）を流し、
    hidden_states[layer_idx + 1] の最後の位置を取る。**値は印字しない。**"""
    import torch
    top, mm, lm = parts(model)
    if top.training or mm.training or lm.training:
        _die('模型が訓練の形（eval にしていない）')
    n = len(lm.layers)
    L = int(layer_idx)
    if not 0 <= L < n - 1:
        _die('層の添字 %s が範囲の外（0〜%d・最後の層の hidden_states は最終の正規化の後なので取らない）' % (layer_idx, n - 2))
    assert_no_foreign_hooks(model)
    d = int(lm.config.hidden_size)
    dev = lm.embed_tokens.weight.device
    out = {}
    for name, ids in contexts.items():
        ids = [int(x) for x in ids]
        if not ids:
            _die('文脈 %s のトークンの並びが空' % name)
        x = torch.tensor([ids], dtype=torch.long, device=dev)
        with torch.no_grad():
            o = model(input_ids=x, output_hidden_states=True, use_cache=False, logits_to_keep=1)
        hs = o.hidden_states
        if hs is None or len(hs) != n + 1:
            _die('hidden_states の数が層の数＋1 でない（%s）' % (None if hs is None else len(hs)))
        h = hs[L + 1]
        if tuple(h.shape) != (1, len(ids), d):
            _die('hidden_states[%d] の形 %s が (1, %d, %d) でない' % (L + 1, tuple(h.shape), len(ids), d))
        v = h[0, -1].detach().to(torch.float64).cpu().numpy()
        if not np.all(np.isfinite(v)):
            _die('文脈 %s の値に有限でないものがある' % name)
        out[name] = v
        del o, hs, h
    assert_no_foreign_hooks(model)
    return out


# ---------------------------------------------------------------- 文脈と名前のある方向

def chat_ids(tok, msg):
    """user の発話一つ・system なし・生成の口つきのチャットの型（transformers 5 は辞書の形を返すので input_ids を取る）。"""
    enc = tok.apply_chat_template([{'role': 'user', 'content': msg}], add_generation_prompt=True, tokenize=True)
    ids = enc['input_ids'] if hasattr(enc, 'keys') else enc
    if hasattr(ids, 'tolist'):
        ids = ids.tolist()
    ids = list(ids)
    if ids and isinstance(ids[0], (list, tuple)):
        if len(ids) != 1:
            _die('チャットの型の出力が一本の列でない')
        ids = list(ids[0])
    return [int(x) for x in ids]


def build_contexts(tok, C, ledger, AT=None):
    """抽出の文脈（正本 directions.extraction の八腕 × 二場面・プロンプトだけ）を作り、台帳 extract_contexts と照らす。"""
    RB = _pub('run_stageB_local')
    EX = C['directions']['extraction']
    arms, scenes = list(EX['arms']), list(EX['scenes'])
    if len(arms) * len(scenes) != int(EX['contexts']):
        _die('正本 directions.extraction の腕 × 場面の数が contexts（%s）と合わない' % EX['contexts'])
    LX = ledger['extract_contexts']
    AT = AT if AT is not None else RB.arm_texts()
    SI = {sc: RB.scenario_and_instruction(sc) for sc in scenes}
    out = {}
    for arm in arms:
        if arm not in AT:
            _die('腕 %s の本文が引けない' % arm)
        for sc in scenes:
            key = '%s|%s' % (sc, arm)
            if key not in LX:
                _die('文脈 %s が台帳 extract_contexts に無い' % key)
            rec = LX[key]
            s, inst = SI[sc]
            ids = chat_ids(tok, RB.user_message(AT[arm]['text'], s['text'], inst))
            bad = []
            if rec.get('scenario') != sc or rec.get('arm') != arm:
                bad.append('台帳の場面か腕が鍵と違う')
            if len(ids) != int(rec['prompt_len']):
                bad.append('長さ %d（台帳 %s）' % (len(ids), rec['prompt_len']))
            if len(ids) - 1 != int(rec['main_position']):
                bad.append('主位置 %d（台帳 %s）' % (len(ids) - 1, rec['main_position']))
            if tok.convert_ids_to_tokens(ids[-1]) != rec['main_position_token']:
                bad.append('主位置のトークン %r（台帳 %r）' % (tok.convert_ids_to_tokens(ids[-1]), rec['main_position_token']))
            if sha16_ids(ids) != rec['ids_sha16']:
                bad.append('ids_sha16 %s（台帳 %s）' % (sha16_ids(ids), rec['ids_sha16']))
            if bad:
                _die('抽出の文脈 %s が台帳と違う: %s' % (key, '・'.join(bad)))
            out[key] = ids
    if set(out) != set(LX):
        _die('台帳 extract_contexts の文脈の集合が正本の腕 × 場面と違う')
    return out


def arm_pairs_from_defs(C):
    """正本 directions.defs の文（…h_X − h_Y…）から、名前のある方向ごとの (足す腕, 引く腕) を読み、指示の対応と照らす。"""
    out = {}
    for nm in C['directions']['named']:
        s = C['directions']['defs'].get(nm)
        if s is None:
            _die('正本 directions.defs に %s が無い' % nm)
        terms = [a or b for a, b in re.findall(r'h_(?:\{([^}]*)\}|([A-Za-z]+))', s)]
        if len(terms) != 2 or '−' not in s.split('h_', 1)[1]:
            _die('正本 directions.defs.%s の文から二つの腕の差を読めない: %s' % (nm, s))
        out[nm] = (terms[0], terms[1])
        if nm in INSTR_DEFS and out[nm] != INSTR_DEFS[nm]:
            _die('正本 directions.defs.%s（%s − %s）が指示の対応（%s − %s）と違う' % ((nm,) + out[nm] + INSTR_DEFS[nm]))
    if set(out) != set(INSTR_DEFS):
        _die('正本の名前のある方向（%s）が指示の四つと違う' % sorted(out))
    return out


def named_directions(acts, C):
    """腕ごとに二場面の平均（float64）を取り、正本 directions.defs のとおりに名前のある方向を作る。"""
    pairs = arm_pairs_from_defs(C)
    scenes = list(C['directions']['extraction']['scenes'])

    def mean(arm):
        return np.mean(np.stack([np.asarray(acts['%s|%s' % (sc, arm)], dtype=np.float64) for sc in scenes]), axis=0)
    return {nm: mean(p) - mean(q) for nm, (p, q) in pairs.items()}


def cosine(a, b):
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def reextract_all(model, tok, C, ledger, dirs):
    """抽出の十六文脈をこの道で流し、{'h_norm_by_context', 'vhat_norm', 'named_cos'} を返す（値は印字しない）。"""
    import torch
    import transformers
    top, mm, lm = parts(model)
    want = str(ledger['meta']['transformers'])
    if transformers.__version__ != want:
        _die('transformers の版が %s（台帳 meta.transformers は %s）' % (transformers.__version__, want))
    if is_real(model, C) and lm.embed_tokens.weight.dtype != torch.bfloat16:
        _die('本の模型が bf16 でない（%s・正本 independent_recompute.reextract.path）' % lm.embed_tokens.weight.dtype)
    L = layer_for(model, C)
    contexts = build_contexts(tok, C, ledger)
    acts = reextract(model, contexts, L)
    D = named_directions(acts, C)
    named_cos = {}
    for nm in C['directions']['named']:
        if nm not in dirs:
            _die('dirs に名前のある方向 %s が無い' % nm)
        v = np.asarray(dirs[nm])
        if v.dtype.kind != 'f' or v.shape != D[nm].shape or not np.all(np.isfinite(v)) or not np.any(v):
            _die('dirs[%s] が形 %s の有限で零でない浮動小数の並びでない' % (nm, D[nm].shape))
        named_cos[nm] = cosine(D[nm], v)
    return {'h_norm_by_context': {k: float(np.linalg.norm(acts[k])) for k in contexts},
            'vhat_norm': float(np.linalg.norm(D['static'])),
            'named_cos': named_cos}


# ---------------------------------------------------------------- 乱数の小さな模型（確かめだけ・書き換えの道の器と同じ作り方を借りる）

def _rw():
    sys.path.insert(0, HERE)
    import bprime_recompute_rewrite as RW
    return RW


def _dtype_name(model):
    _, _, lm = parts(model)
    return str(lm.embed_tokens.weight.dtype).replace('torch.', '')


def _selftest():
    import torch
    import transformers
    from transformers import AutoTokenizer
    RW = _rw()
    C, LG = load_canon(), load_ledger()
    RB = _pub('run_stageB_local')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    base = RW.tiny_model(C)
    models = [('float32', RW.as_dtype(base, torch.float32)), ('bfloat16', base)]
    for _, m in models:
        RW.assert_tiny(m)
    res = []

    def ck(label, ok, detail=''):
        res.append(bool(ok))
        print('[%s] %s%s' % ('ok' if ok else 'NG', label, ('  | ' + detail) if detail else ''), flush=True)

    def stops(fn):
        try:
            fn()
        except SystemExit as e:
            return True, str(e)
        return False, ''

    m32 = models[0][1]
    _, _, lm32 = parts(m32)
    L = layer_for(m32, C)
    tol = C['independent_recompute']['reextract']
    print('bprime_reextract %s --selftest  torch %s・transformers %s・numpy %s・注意の実装 %s・作ったままの型 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, lm32.config._attn_implementation, _dtype_name(base)),
          flush=True)
    print('乱数の小さな模型: 次元 %d・層 %d・選んだ層の添字 %d（hidden_states[%d]）・許容 rel_tol %s・cos_min %s'
          % (int(lm32.config.hidden_size), len(lm32.layers), L, L + 1, tol['rel_tol'], tol['cos_min']), flush=True)

    # (1) 正本の定義と指示の対応・文脈の組み立て
    pairs = arm_pairs_from_defs(C)
    ck('正本 directions.defs の文から読んだ腕の差が指示の対応と一致', pairs == INSTR_DEFS,
       '・'.join('%s＝%s − %s' % (k, a, b) for k, (a, b) in pairs.items()))
    C2 = copy.deepcopy(C)
    C2['directions']['defs']['td'] = 'h_Nk − h_N（写しを書き換えた）'
    ck('正本の定義の文が指示の対応と違えば止まる（td を書き換えた写し）', stops(lambda: arm_pairs_from_defs(C2))[0])
    ctx = build_contexts(tok, C, LG, AT=AT)
    ck('抽出の文脈が台帳と一致（%d 文脈・長さ・主位置とそのトークン・ids_sha16）' % len(ctx), len(ctx) == 16,
       '・'.join('%s %d' % (k, len(v)) for k, v in ctx.items()))
    LG2 = copy.deepcopy(LG)
    LG2['extract_contexts']['S1|Osec']['ids_sha16'] = '0' * 16
    ck('台帳と違えば止まる（S1|Osec の ids_sha16 を書き換えた写し）', stops(lambda: build_contexts(tok, C, LG2, AT=AT))[0])
    LG2 = copy.deepcopy(LG)
    LG2['extract_contexts']['N1|Nk']['prompt_len'] += 1
    ck('台帳と違えば止まる（N1|Nk の prompt_len を +1 ずらした写し）', stops(lambda: build_contexts(tok, C, LG2, AT=AT))[0])

    for tn, m in models:
        top, _, lm = parts(m)
        nc0 = RW.capture_hook_count(m)
        t0 = time.time()
        acts = reextract(m, ctx, L)
        dt = time.time() - t0
        ok = (list(acts) == list(ctx) and all(isinstance(v, np.ndarray) and v.dtype == np.float64 and v.shape == (64,)
                                              and np.all(np.isfinite(v)) for v in acts.values()))
        ck('[%s] 取った値は有限・float64・形 (64,)・文脈の名がそろう（%d 文脈）' % (tn, len(acts)), ok, '%.1f 秒' % dt)
        nc1 = RW.capture_hook_count(m)
        print('[参考] [%s] 記録用の hook（transformers の output_capturing）: 前 %d 本 → 後 %d 本・それ以外の hook %d 本（判定に入れない）'
              % (tn, nc0, nc1, len(foreign_hooks(m))), flush=True)
        acts2 = reextract(m, ctx, L)
        ck('[%s] 同じ呼び出しを二度走らせて同じ値（ビット単位・二度目は記録用の hook が居残った模型）' % tn,
           all(np.array_equal(acts[k], acts2[k]) for k in ctx))
        # 書き換えの道の手回し（零の書き換え）の層 L の出力の主位置と一致するか（別の書き方どうしの突き合わせ）
        same = []
        for k in ('N1|O', 'S1|Onull-Ncold', 'N1|N'):
            keep = {}
            RW.forward_rewrite(m, ctx[k], L, np.zeros(64), 1.0, 1, len(ctx[k]) - 1, keep=keep)
            hv = keep['L_before'][0, -1].detach().to(torch.float64).numpy()
            same.append(np.array_equal(hv, acts[k]))
        ck('[%s] hidden_states[%d] の主位置が、手で層を回した道の層 %d の出力の主位置と一致（ビット単位・3 文脈）' % (tn, L + 1, L), all(same))
        ck('[%s] 最後の層（添字 %d）は取らずに止まる（hidden_states[-1] は最終の正規化の後）' % (tn, len(lm.layers) - 1),
           stops(lambda: reextract(m, {'N1|N': ctx['N1|N']}, len(lm.layers) - 1))[0])
        hd = lm.layers[L].register_forward_hook(lambda mod, a, o: None)
        try:
            ok_h, _ = stops(lambda: reextract(m, {'N1|N': ctx['N1|N']}, L))
        finally:
            hd.remove()
        ck('[%s] 模型に forward の hook が掛かっていれば止まる（選んだ層に何もしない hook を掛けた写し）' % tn, ok_h)
        # 名前のある方向の余弦: dirs に同じ方向を渡せば一
        D = named_directions(acts, C)
        r = reextract_all(m, tok, C, LG, D)
        ck('[%s] reextract_all: 文脈 %d・名前のある方向の余弦が dirs に同じ方向を渡したとき一（1−1e-12 以上）' % (tn, len(r['h_norm_by_context'])),
           set(r['h_norm_by_context']) == set(ctx) and all(v >= 1 - 1e-12 for v in r['named_cos'].values()),
           '・'.join('%s %.15f' % (k, v) for k, v in r['named_cos'].items()))
        ck('[%s] reextract_all: vhat_norm＝‖O の平均 − Osec の平均‖・h_norm_by_context＝‖h‖（ビット単位）' % tn,
           r['vhat_norm'] == float(np.linalg.norm(D['static']))
           and all(r['h_norm_by_context'][k] == float(np.linalg.norm(acts[k])) for k in ctx))
        D2 = dict(D)
        D2['static'] = -D['static']
        D2['loaded'] = D['Nk']
        r2 = reextract_all(m, tok, C, LG, D2)
        ck('[%s] 歯——static を反転した dirs の余弦は −1、loaded に Nk を渡した dirs の余弦は cos_min（%s）に届かない' % (tn, tol['cos_min']),
           r2['named_cos']['static'] <= -1 + 1e-12 and r2['named_cos']['loaded'] < float(tol['cos_min']),
           'static %.6f・loaded %.6f' % (r2['named_cos']['static'], r2['named_cos']['loaded']))
        D3 = dict(D)
        D3.pop('td')
        ck('[%s] dirs に名前のある方向が無ければ止まる' % tn, stops(lambda: reextract_all(m, tok, C, LG, D3))[0])
    n_ok = sum(res)
    print('selftest: %d/%d ok' % (n_ok, len(res)), flush=True)
    print('柵: ' + FENCE, flush=True)
    return n_ok == len(res)


def _dry():
    import torch
    import transformers
    from transformers import AutoTokenizer
    RW = _rw()
    C, LG = load_canon(), load_ledger()
    tol = C['independent_recompute']['reextract']
    rel_tol, cos_min = float(tol['rel_tol']), float(tol['cos_min'])
    RB = _pub('run_stageB_local')
    tok = AutoTokenizer.from_pretrained(HF_DIR)
    AT = RB.arm_texts()
    ctx = build_contexts(tok, C, LG, AT=AT)
    base = RW.tiny_model(C)
    m32 = RW.as_dtype(base, torch.float32)
    for m in (m32, base):
        RW.assert_tiny(m)
    L = layer_for(m32, C)
    sys.path.insert(0, os.path.join(BPRIME, 'tools'))
    import bprime_directions as BD
    print('bprime_reextract %s --dry  torch %s・transformers %s・numpy %s・注意の実装 %s'
          % (VERSION, torch.__version__, transformers.__version__, np.__version__, parts(m32)[2].config._attn_implementation), flush=True)
    print('乱数の小さな模型: 次元 64・層 6・選んだ層の添字 %d・許容 independent_recompute.reextract の rel_tol = %s・cos_min = %s'
          % (L, rel_tol, cos_min), flush=True)
    print('比べる文脈（四つ）: %s' % '・'.join('%s（%d トークン）' % (k, len(ctx[k])) for k in DRY_CONTEXTS), flush=True)
    c4 = {k: ctx[k] for k in DRY_CONTEXTS}
    verdicts = []
    for tn, m in (('float32', m32), ('bfloat16', base)):
        try:
            t0 = time.time()
            A1, N1, _ = BD.activations(m, c4, L)                      # コーディネータの抽出の器（中を見ない）
            t1 = time.time()
        except BaseException as e:
            print('[%s] コーディネータの抽出の器が落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
            verdicts.append(False)
            continue
        mine = reextract(m, c4, L)
        t2 = time.time()
        try:
            A2, N2, _ = BD.activations(m, c4, L)                      # 記録用の hook が居残った模型でもう一度
        except BaseException as e:
            print('[参考] [%s] 二度目のコーディネータの抽出の器が落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
            A2 = None
        if set(A1) != set(c4):
            print('[%s] コーディネータの抽出の器の文脈の名が違う: %s' % (tn, sorted(A1)), flush=True)
            verdicts.append(False)
            continue
        rels, coss = [], []
        for k in DRY_CONTEXTS:
            a, b = np.asarray(mine[k], dtype=np.float64), np.asarray(A1[k], dtype=np.float64)
            rels.append(abs(np.linalg.norm(a) - np.linalg.norm(b)) / np.linalg.norm(b))
            coss.append(cosine(a, b))
        exact = all(np.array_equal(np.asarray(mine[k], dtype=np.float64), np.asarray(A1[k], dtype=np.float64)) for k in DRY_CONTEXTS)
        print('[%s] コーディネータの抽出の器 %.1f 秒・この道 %.1f 秒・返り値の型 %s／%s' % (tn, t1 - t0, t2 - t1, type(A1).__name__, type(N1).__name__), flush=True)
        print('[%s] ‖h‖ の相対の差の最大 %.3g・余弦の最小 %.12f・四つともビット単位で同じ: %s' % (tn, max(rels), min(coss), exact), flush=True)
        if isinstance(N1, dict) and set(N1) >= set(c4):
            try:
                rn = max(abs(float(np.linalg.norm(mine[k])) - float(N1[k])) / float(N1[k]) for k in DRY_CONTEXTS)
                print('[参考] [%s] コーディネータの器が返したノルムとこの道の ‖h‖ の相対の差の最大 %.3g（判定に入れない）' % (tn, rn), flush=True)
            except (TypeError, ValueError) as e:
                print('[参考] [%s] コーディネータの器が返したノルムを数として読めない: %s' % (tn, type(e).__name__), flush=True)
        if A2 is not None:
            print('[参考] [%s] 記録用の hook が居残った模型での二度目のコーディネータの抽出の器が一度目と同じ（ビット単位）: %s'
                  % (tn, all(np.array_equal(np.asarray(A1[k]), np.asarray(A2[k])) for k in DRY_CONTEXTS)), flush=True)
        ok = max(rels) <= rel_tol and min(coss) >= cos_min
        verdicts.append(ok)
        print('[%s] dry: 再抽出の許容（rel_tol %s・cos_min %s）の%s' % (tn, rel_tol, cos_min, '内' if ok else '外'), flush=True)
        # 参考: 十六文脈の全体で、コーディネータの抽出の器の値から作った名前のある方向を dirs に渡した reextract_all
        try:
            AF, _, _ = BD.activations(m, ctx, L)
            DB_ = named_directions(AF, C)
            r = reextract_all(m, tok, C, LG, DB_)
            vrel = abs(r['vhat_norm'] - float(np.linalg.norm(DB_['static']))) / float(np.linalg.norm(DB_['static']))
            hrel = max(abs(r['h_norm_by_context'][k] - float(np.linalg.norm(AF[k]))) / float(np.linalg.norm(AF[k])) for k in ctx)
            print('[参考] [%s] 十六文脈: reextract_all の名前のある方向の余弦の最小 %.12f・‖v̂‖ の相対の差 %.3g・‖h‖ の相対の差の最大 %.3g'
                  '（dirs はコーディネータの器の値からこの器の式で作った・判定に入れない）' % (tn, min(r['named_cos'].values()), vrel, hrel), flush=True)
        except BaseException as e:
            print('[参考] [%s] 十六文脈の参考の突き合わせが落ちた: %s: %s' % (tn, type(e).__name__, str(e)[:300]), flush=True)
    print('dry: %s' % ('二つの型とも再抽出の許容の内' if verdicts and all(verdicts) else '許容の外か比べられなかった型がある'), flush=True)
    print('柵: ' + FENCE, flush=True)
    return bool(verdicts) and all(verdicts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.dry:
        sys.exit(0 if _dry() else 1)
    ap.print_help()


if __name__ == '__main__':
    main()
```

### 6. `tools/bprime_directions.py`（本の抽出）

- 出所: 作業の置き場 `tools/bprime_directions.py`・SHA16 8D999D06A7773343・12174 字

```python
# -*- coding: utf-8 -*-
"""bprime_directions.py v1（2026-09-30・B′ の方向の抽出と帰無の方向の作り方・Gemma-4-31B-it・コーディネータ南無弥勒如来）。前の版は `prev/bprime_directions-v0.py`。

正本 `design/contrasts-Bprime.json` の `directions`・`nulls`・`coefficient` のとおり:
  - 抽出（相 extract）: 八腕 × 抽出の二場面の文脈の主位置（`<channel|>`）の、選んだ層の出力（`layers[k]` の出力をフックで取る）。選んだ層より後を流さない（層の出力を取った所で
    順伝播を打ち切り、最後の正規化の前のフックが一度も呼ばれないことを assert する・`directions.extraction.no_readout`・S26）。効き目を一つも計算しない。
  - 名前のある方向は段階 B と同じ定義（static＝h_O − h_Osec・loaded＝h_{O-Ncold} − h_{Osec-Ncold}・Nk＝h_Nk − h_N・td＝h_Onull − h_N・h は二場面の平均）で、‖static‖ に合わせる
    （凍結の `steer_B.match_to_static`）。揃える前のノルムが有限で零でないことを assert する（S19）。
  - 等方の方向は凍結の `blens_core.iso_directions`（種・層の割合・本数・`layer_key_scale`）の出力をそのまま npz に入れる。凍結の前に同じ引き方で正規化の前の乱数 g を引き
    （`iso_g`）、g と種と層の割合と次元の SHA を凍結の記録に入れる。相 extract では、凍結の関数の出力が g × ‖v̂‖ ÷ ‖g‖ と相対の差 `nulls.isotropic.g_rel_tol` の内で一致することを確かめる。
  - 実在の差の方向は凍結の `blens_core.real_differences`（八腕の全ての対・名の並びは八腕の順の i<j）。自己検査の一本は等方と同じ作り方で `nulls.self_check_direction.seed` の種。
  - 係数（`coefficient.rule`）: 層三の比 ÷（‖v̂‖ ÷ ‖h‖）。層三の比は層三の凍結の活性から出し直す（`bl3_ratio`）。確かめ二つ（`coefficient.check_bl3`・`coefficient.check_B_record`）。
  - npz は凍結の `bl3_directions.write_npz_fixed`（時刻を持たない形・再実行で同一バイト）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, hashlib, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G
import bprime_core as P

VERSION = 'v1'          # v1（2026-09-30）: 正本 v2 に合わせた（選んだ層より後を流さない assert・g の保存と一致・自己検査の一本・揃える前のノルムの assert・係数と二つの確かめ・帯の位置の ‖h‖）
REAL_ARMS = ['O', 'Osec', 'Onull', 'Nk', 'N', 'O-Ncold', 'Osec-Ncold', 'Onull-Ncold']
EXTRACT_SCENES = ['N1', 'S1']
NAMED = collections.OrderedDict([('static', ('O', 'Osec')), ('loaded', ('O-Ncold', 'Osec-Ncold')), ('Nk', ('Nk', 'N')), ('td', ('Onull', 'N'))])
sha_arr = lambda x: hashlib.sha256(np.ascontiguousarray(np.asarray(x, dtype=np.float64)).tobytes()).hexdigest().upper()
ToolError = P.ToolError


class _Stop(Exception):
    """選んだ層の出力を取った所で順伝播を打ち切る印（読み取りの値を作らない）。"""


def activations(model, contexts, layer_idx, positions=None):
    """文脈（名 → トークンの並び）ごとに、選んだ層の出力の主位置の値（float64）を返す（加減はしない）。positions を与えると、その位置（名 → 添字の並び）の値も返す。
    選んだ層の出力を取った所で打ち切り、最後の正規化の前のフックが呼ばれないこと（読み取りの値を作らないこと）を assert する。"""
    import torch
    dev = next(model.parameters()).device
    layer = G.decoder_layers(model)[layer_idx]
    out, norms, extra = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
    for key, ids in contexts.items():
        mp = G.main_position(ids)
        cap, flag = {}, {'norm': False}

        def hook(m, a, o):
            hh = (o[0] if isinstance(o, tuple) else o)[0]
            cap['h'] = hh[mp, :].detach().double().cpu().numpy()
            if positions is not None and key in positions:
                cap['pos'] = hh[list(positions[key]), :].detach().double().cpu().numpy()
            raise _Stop()
        h = layer.register_forward_hook(hook)
        hn = G.final_norm(model).register_forward_pre_hook(lambda m, a: flag.__setitem__('norm', True))
        try:
            with torch.no_grad():
                try:
                    model(input_ids=torch.tensor([ids], device=dev), use_cache=False, logits_to_keep=1)
                except _Stop:
                    pass
        finally:
            h.remove()
            hn.remove()
        if flag['norm'] or 'h' not in cap:
            raise ToolError('抽出が選んだ層より後を流した（最後の正規化が呼ばれた）か、層の出力を取れなかった: %s' % key)
        out[key] = cap['h']
        norms[key] = float(np.linalg.norm(cap['h']))
        if 'pos' in cap:
            extra[key] = cap['pos']
    return out, norms, extra


def arm_means(acts):
    """文脈の名（`場面|腕`）から、腕ごとの抽出の二場面の平均（八腕の順）。"""
    return collections.OrderedDict((arm, np.mean([acts['%s|%s' % (sc, arm)] for sc in EXTRACT_SCENES], axis=0)) for arm in REAL_ARMS)


def _finite_nonzero(vecs, where):
    bad = [k for k, v in vecs.items() if not np.all(np.isfinite(v)) or float(np.linalg.norm(v)) == 0.0]
    if bad:
        raise ToolError('揃える前のノルムが有限でないか零（%s）: %s' % (where, bad))


def iso_g(seed, layer_ratio, count, key_scale, d):
    """正規化の前の乱数 g（凍結の `blens_core.iso_directions` と同じ引き方: SeedSequence([種, 層の割合 × key_scale])・方向ごとに正規分布を d 個）。"""
    ss = np.random.SeedSequence([int(seed), int(round(float(layer_ratio) * int(key_scale)))])
    rng = np.random.default_rng(ss)
    return np.array([rng.normal(size=int(d)) for _ in range(int(count))], dtype=np.float64)


def g_record(g, seed, layer_ratio, count, key_scale):
    return {'g_sha256': sha_arr(g), 'seed': int(seed), 'layer_ratio': float(layer_ratio), 'count': int(count), 'layer_key_scale': int(key_scale), 'dim': int(g.shape[1]),
            'numpy': np.__version__}


def check_iso_against_g(iso, g, vhat_norm, rel_tol):
    """凍結の関数の出力（iso）が、保存した g から同じ式で作った値と相対の差の内で一致するか（ビットの一致は求めない）。"""
    want = g * (float(vhat_norm) / np.linalg.norm(g, axis=1, keepdims=True))
    rel = float(np.max(np.abs(iso - want)) / max(float(np.max(np.abs(want))), 1e-300))
    return {'rel_max': rel, 'pass': bool(rel <= rel_tol)}


def build(acts, C, g=None):
    """方向の組（名前のある方向・等方・実在の差・自己検査の一本）を作る。g を与えると等方の一致を確かめる（落ちたら ToolError）。"""
    import steer_B
    import blens_core as CB
    M = arm_means(acts)
    raw_named = collections.OrderedDict((k, M[a] - M[b]) for k, (a, b) in NAMED.items())
    _finite_nonzero(raw_named, '名前のある方向')
    static = raw_named['static']
    nv = float(np.linalg.norm(static))
    named = collections.OrderedDict((k, steer_B.match_to_static(v, static)) for k, v in raw_named.items())
    ratio = float(C['layers']['ratio'])
    ks = int(C['nulls']['isotropic']['layer_key_scale'])
    iso = np.asarray(CB.iso_directions(static, int(C['nulls']['isotropic']['seed']), ratio, int(C['nulls']['isotropic']['count']), ks), dtype=np.float64)
    if iso.shape[1] != static.shape[0]:
        raise ToolError('等方の方向の次元が抽出した活性の次元と違う（R23）')
    iso_check = None
    if g is not None:
        iso_check = check_iso_against_g(iso, g, nv, C['nulls']['isotropic']['g_rel_tol'])
        if not iso_check['pass']:
            raise ToolError('等方の方向が保存した g と一致しない（相対の差 %.3g）' % iso_check['rel_max'])
    raw_real = collections.OrderedDict()
    names = list(M)
    import itertools
    for i, j in itertools.combinations(range(len(names)), 2):
        raw_real['%s~%s' % (names[i], names[j])] = M[names[i]] - M[names[j]]
    _finite_nonzero(raw_real, '実在の差の方向')
    real = CB.real_differences(M, nv)
    if list(real) != list(raw_real):
        raise ToolError('実在の差の名の並びが凍結の関数と違う')
    check = np.asarray(CB.iso_directions(static, int(C['nulls']['self_check_direction']['seed']), ratio, 1, ks), dtype=np.float64)
    arrays = collections.OrderedDict([('named', np.array(list(named.values()), dtype=np.float64)), ('iso', iso), ('real', np.array(list(real.values()), dtype=np.float64)), ('check', check)])
    names_ = collections.OrderedDict([('named', list(named)), ('iso', ['iso:%d' % i for i in range(len(iso))]), ('real', list(real)), ('check', ['check'])])
    un = lambda v: v / np.linalg.norm(v)
    cos_check = float(max(abs(float(un(check[0]) @ un(x))) for x in list(iso) + list(real.values())))
    meta = {'version': VERSION, 'layer_ratio': ratio, 'dim': int(static.shape[0]), 'vhat_norm': nv, 'iso_seed': int(C['nulls']['isotropic']['seed']), 'iso_count': int(len(iso)),
            'layer_key_scale': ks, 'check_seed': int(C['nulls']['self_check_direction']['seed']), 'check_cos_max': cos_check, 'iso_check': iso_check,
            'natural_norms_real': {k: float(np.linalg.norm(v)) for k, v in raw_real.items()}, 'natural_norms_named': {k: float(np.linalg.norm(v)) for k, v in raw_named.items()},
            'sha256': {k: sha_arr(v) for k, v in arrays.items()}}
    return arrays, names_, meta


def h_norm_mean(norms):
    """‖h‖ の平均（抽出の文脈の主位置・段階 B の `direction_B.h_norm_record` と同じ定義・R13）。"""
    return float(np.mean(list(norms.values())))


def bl3_ratio(npz_path, ratio_key='0.5'):
    """層三の比（正本 `coefficient.bl3_ratio`）: 層三の凍結の活性（`same_order`・八腕 × 二場面）から ‖h‖ の平均と ‖v̂‖ を出し直し、`coef_applied` × ‖v̂‖ ÷ ‖h‖。"""
    Z = np.load(npz_path)
    acts = collections.OrderedDict(('%s|%s' % (sc, arm), np.asarray(Z['same_order__%s__%s__%s' % (arm, sc, ratio_key)], dtype=np.float64)) for arm in REAL_ARMS for sc in EXTRACT_SCENES)
    norms = collections.OrderedDict((k, float(np.linalg.norm(v))) for k, v in acts.items())
    M = arm_means(acts)
    vhat = float(np.linalg.norm(M['O'] - M['Osec']))
    hm = h_norm_mean(norms)
    return {'h_norm_mean': hm, 'vhat_norm': vhat, 'vhat_over_h': vhat / hm, 'acts': acts, 'norms': norms}


def coefficient(bl3_ratio_value, vhat_norm, h_mean):
    """係数＝層三の比 ÷（‖v̂‖ ÷ ‖h‖）（上下の限りを置かない・R13）。"""
    if not (np.isfinite(vhat_norm) and np.isfinite(h_mean) and vhat_norm > 0 and h_mean > 0):
        raise ToolError('係数の分母が有限の正の値でない')
    return float(bl3_ratio_value / (vhat_norm / h_mean))


def coefficient_checks(npz_path, C):
    """係数の二つの確かめ（`coefficient.check_bl3`・`coefficient.check_B_record`）。戻り値: 値と合否（落ちたら ToolError）。"""
    r = bl3_ratio(npz_path)
    coef_applied = float(C['coefficient']['bl3_coef_applied'])
    ratio = coef_applied * r['vhat_over_h']
    coef = coefficient(ratio, r['vhat_norm'], r['h_norm_mean'])
    tol = float(C['coefficient']['check_bl3']['rel_tol'])
    ok1 = abs(coef - coef_applied) / coef_applied <= tol
    rec = C['coefficient']['check_B_record']
    d_h = abs(r['h_norm_mean'] - rec['h_norm_main']) / rec['h_norm_main']
    d_v = abs(r['vhat_norm'] - rec['vhat_norm']) / rec['vhat_norm']
    ok2 = d_h <= tol and d_v <= tol
    out = {'bl3_ratio': ratio, 'coef_on_bl3': coef, 'check_bl3_pass': bool(ok1), 'h_norm_mean': r['h_norm_mean'], 'vhat_norm': r['vhat_norm'], 'rel_h': d_h, 'rel_v': d_v, 'check_B_record_pass': bool(ok2)}
    if not (ok1 and ok2):
        raise ToolError('係数の確かめが落ちた: %s' % out)
    return out


def npz_bytes(arrays):
    import bl3_directions as BD
    return BD.write_npz_fixed(None, arrays)


def _selftest():
    """模型を読まない確かめ（numpy だけ・合成の活性）: g の引き方が凍結の関数と同じ・一致の確かめ・揃える前のノルムの assert・係数の式と二つの確かめ（層三の実の活性で）。"""
    import json
    import blens_core as CB
    C = json.load(open(os.path.join(os.path.dirname(HERE), 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    rng = np.random.default_rng(7)
    d = 48
    acts = collections.OrderedDict(('%s|%s' % (sc, arm), rng.standard_normal(d) * 3.0) for arm in REAL_ARMS for sc in EXTRACT_SCENES)
    Cs = json.loads(json.dumps(C))
    Cs['nulls']['isotropic']['count'] = 25
    g = iso_g(Cs['nulls']['isotropic']['seed'], Cs['layers']['ratio'], 25, Cs['nulls']['isotropic']['layer_key_scale'], d)
    arrays, names, meta = build(acts, Cs, g=g)
    assert meta['iso_check']['pass'] and meta['iso_check']['rel_max'] < 1e-14, meta['iso_check']
    assert arrays['iso'].shape == (25, d) and arrays['real'].shape == (28, d) and arrays['named'].shape == (4, d) and arrays['check'].shape == (1, d)
    assert np.allclose(np.linalg.norm(arrays['iso'], axis=1), meta['vhat_norm']) and np.allclose(np.linalg.norm(arrays['check']), meta['vhat_norm'])
    g_bad = g.copy(); g_bad[0, 0] += 1.0
    try:
        build(acts, Cs, g=g_bad); raise AssertionError('g の違いで止まらない')
    except ToolError:
        pass
    acts0 = dict(acts); acts0['N1|Osec'] = acts['N1|O']; acts0['S1|Osec'] = acts['S1|O']
    try:
        build(collections.OrderedDict(acts0), Cs); raise AssertionError('零のノルムで止まらない')
    except ToolError:
        pass
    PUB = os.environ.get('OP4B_PUBLIC_REPO', 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b')
    cc = coefficient_checks(os.path.join(PUB, 'results', 'dirB', 'dirB__s1', 'main_position_activations.npz'), C)
    assert cc['check_bl3_pass'] and cc['check_B_record_pass']
    b1, b2 = npz_bytes(arrays), npz_bytes(arrays)
    assert b1 == b2
    print('bprime_directions.py %s SELFTEST PASS（g の一致 %.2g・係数の確かめ 層三の活性で %.9f・‖h‖ の相対の差 %.2g・‖v̂‖ の相対の差 %.2g）' % (VERSION, meta['iso_check']['rel_max'], cc['coef_on_bl3'], cc['rel_h'], cc['rel_v']))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    print(__doc__)
```

### 7. `tools/bprime_gemma.py`（模型の助け（層の添字・設定の読み））

- 出所: 作業の置き場 `tools/bprime_gemma.py`・SHA16 700EB39D6510C9C1・4232 字

```python
# -*- coding: utf-8 -*-
"""bprime_gemma.py v0（2026-09-29・B′ の器の下地・Gemma-4-31B-it・transformers 5 系・コーディネータ南無弥勒如来）。

段階 B・層三の凍結した器のうち、模型に依らない関数（腕の本文・場面と指示・発話の組み立て・加減のフック・層の割合から添字への式・
対数オッズの式）は読み込んで使い、模型に依る所（層と正規化の道・softcap・チャットの型の返り値）だけをここに置く。凍結した器は書き換えない。

下調べ（`../port-probe/port-notes-2026-09-29.md`）で確かめたこと:
  - 層は `model.model.language_model.layers`・最後の正規化は `model.model.language_model.norm`・lm_head は埋め込みと共有。
  - 層の出力はテンソル（凍結の `make_hook` は両方の形を扱う）。
  - `hidden_states[-1]` は最後の正規化の後の値（層ごとの読み取りは層の出力をフックで取る・`hidden_states` を使わない）。
  - ロジットは softcap（`final_logit_softcapping`）を掛けた値。
  - transformers 5 では `apply_chat_template(tokenize=True)` が辞書の形を返し、凍結の `steer_B.apply_chat` は鍵の並びを返す（使わない）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys

REPO = os.environ.get('OP4B_REPO', 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b')
TOOLS = os.path.join(REPO, 'tools')
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

VERSION = 'v0.1'   # v0.1（2026-09-29）: transformers 5 の隠れ状態を集めるフックを数えない（印で見分ける）


class PortError(Exception):
    """器の移しの前提が崩れた（道・形・版）。"""


def text_cfg(model):
    return model.config.get_text_config()


def language_model(model):
    """Gemma 4 の文の側の模型（`Gemma4ForConditionalGeneration` の中）。道が無ければ止める。"""
    m = getattr(model, 'model', None)
    lm = getattr(m, 'language_model', None) if m is not None else None
    if lm is None or not hasattr(lm, 'layers') or not hasattr(lm, 'norm'):
        raise PortError('model.model.language_model（layers・norm）が無い——Gemma 4 の形でない')
    return lm


def decoder_layers(model):
    return language_model(model).layers


def final_norm(model):
    return language_model(model).norm


def n_layers(model):
    n = int(text_cfg(model).num_hidden_layers)
    if len(decoder_layers(model)) != n:
        raise PortError('設定の層の数（%d）と模型の層の数（%d）が違う' % (n, len(decoder_layers(model))))
    return n


def softcap(model):
    c = text_cfg(model).final_logit_softcapping
    return None if c is None else float(c)


def rms_eps(model):
    return float(text_cfg(model).rms_norm_eps)


def apply_chat(tokenizer, user_message):
    """段階 B と同じ組み立て（user の発話一つ・system なし・生成の口つき）。transformers 5 の辞書の返り値から `input_ids` を取る。"""
    r = tokenizer.apply_chat_template([{'role': 'user', 'content': user_message}], add_generation_prompt=True, tokenize=True)
    ids = r['input_ids'] if hasattr(r, 'keys') else r
    ids = [int(x) for x in ids]
    if not ids or not all(isinstance(x, int) for x in ids):
        raise PortError('チャットの型の返り値が整数の並びでない')
    return ids


def main_position(ids, pad_len=0):
    """主位置＝組み立て済みの列の最後のトークン（段階 B の `steer_B.main_position` と同じ式）。"""
    return int(pad_len) + len(ids) - 1


def layer_index(ratio, n):
    """層の割合 → 層の添字（段階 B の凍結の `direction_B.layer_index` をそのまま呼ぶ）。"""
    import direction_B
    return direction_B.layer_index(float(ratio), int(n))


def _ours(layer):
    """B′ のフック（凍結の `make_hook` が付ける印 `op4b` を持つもの）だけを数える。
    transformers 5 は、初めて `output_hidden_states=True` で順伝播したときに、隠れ状態を集めるフック（`transformers.utils.output_capturing`）を
    すべての層に掛け、外さない（下調べで確かめた）。そのフックは数えない。"""
    return [fn for fn in (getattr(layer, '_forward_hooks', {}) or {}).values() if hasattr(fn, 'op4b')]


def foreign_hooks(model):
    """層ごとの、B′ の印を持たないフックの数（記録のため）。"""
    return [len(getattr(L, '_forward_hooks', {}) or {}) - len(_ours(L)) for L in decoder_layers(model)]


def register_hook(model, layer_idx, hook):
    """B′ のフックを一本だけ掛け、掛ける前より一本だけ増えたことと、B′ のフックがちょうど一本であることを確かめる（段階 B の `register_hook` と同じ決まり・層の道と数え方だけ Gemma 4 と transformers 5 に合わせた）。"""
    if not hasattr(hook, 'op4b'):
        raise PortError('B′ のフックに印（op4b）が無い')
    layer = decoder_layers(model)[layer_idx]
    if _ours(layer):
        raise PortError('この層に B′ のフックが既に掛かっている')
    n0 = len(getattr(layer, '_forward_hooks', {}) or {})
    handle = layer.register_forward_hook(hook)
    if len(_ours(layer)) != 1 or len(getattr(layer, '_forward_hooks', {}) or {}) != n0 + 1:
        handle.remove()
        raise PortError('B′ のフックが一本になっていない')
    return handle


def assert_no_hooks(model, layer_idx):
    layer = decoder_layers(model)[layer_idx]
    n = len(_ours(layer))
    if n:
        raise PortError('B′ のフックが外れていない（%d 本）' % n)
```

### 8. `tools/bprime_phases.py`（相の計算（本の計算の組・抽出））

- 出所: 作業の置き場 `tools/bprime_phases.py`・SHA16 11106F052687C333・27342 字

```python
# -*- coding: utf-8 -*-
"""bprime_phases.py v0（2026-09-30・B′ の相ごとの計算の手順・起動器 `colab/boot_bprime.py` が呼ぶ・模型は呼ぶ側が読む・コーディネータ南無弥勒如来）。

相ごとの関数（正本 `stage_order`・`computation`・`directions`・`behavior_pilot`・`pilot`・`independent_recompute` のとおり・値を読まない）:
  - `check_items`（凍結の前の確かめ・正本 `computation.before_seal`・`computation.pre_freeze_checks`）: 意味のない列だけで順伝播と生成の煙試験をする。場面・腕・指示・書き出しを含む入力は
    トークナイザだけで確かめ、模型に通さない。戻り値は露出の記録（`computation.before_seal.may_print` の値だけ・合否と数と SHA と時間）。
  - `extract`（相 extract）: 抽出の文脈（八腕 × 二場面）の主位置と、主の升目の帯の八つの位置の、選んだ層の出力（選んだ層より後を流さない）→ 方向の組（g との一致）→ 係数 → npz →
    抽出の記録（転記行 D の元）。効き目は一つも計算しない。
  - `behavior`（行動の下見）: 升目ごとに生成 → 復号 → 凍結の採点 → 書き出しの根の件数 → 升目の集計（`bprime_behavior`）。
  - `pilot`（読み取りの下見）: 出口の値の自己検査 → (vi) → (i)(ii)(iv) → (iii) → 決め（`bprime_run.run_pilot`）。(iii) の処理の並びは `generate` から取り、転記行 C の要約と照らす。
  - `main_part`（本の計算の組）: main（`bprime_run.run_main_phase`）・recompute（独立の再計算の一段目の本の器のフックの道）・pathdiff（道の違いの記述・本の計算がバッチ一のときだけ）。
    残差の書き換えの道と独立の再抽出の道は、書き手と別の個体が書く器（`bprime_recompute_rewrite`・`bprime_reextract`）を起動器が呼ぶ（この器には置かない）。
印字の決まり: この器は値を印字しない（log には段の名と時間と数だけを渡す）。値は戻り値の記録に置き、起動器が置き場に書く。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, time, math, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import bprime_gemma as G
import bprime_core as P
import bprime_run as BR
import bprime_directions as BD
import bprime_behavior as BB
import bprime_cells as BC
import bl3_core as K

VERSION = 'v0.1'        # v0.1（2026-09-30）: 凍結の前の確かめの台帳の作り直しの照らしで、腕の置き場の名を照らさない（K18・Colab の DRY で見つけた）。前の版は `prev/bprime_phases-v0.py`
ToolError = P.ToolError
BINS = (0.0, 1.0, 4.0, 16.0, float('inf'))            # 出口の値の大きさの区間（|z|・凍結の前の確かめの印字）


def _t():
    return time.time()


def set_ids_of(C, L, fam):
    heads = L['heads']
    return [int(heads[x]['next']) for x in C['readout']['primary']['letters'][fam]] + [int(heads['refuse']['next'])]


def meaningless_cells(C, L, seqs):
    """意味のない列を升目の形にする（読み取りの位置は列の最後・読み取りの集合は nuclear の族の集合〔選択の文字四つと refuse の頭〕）。"""
    sids = set_ids_of(C, L, 'nuclear')
    return [BR.Cell('meaningless|' + n, 'X', 'X', 'X', ids, [], sids, len(ids) - 1) for n, ids in seqs.items()], sids


def bin_stats(d_on, zs, d_off, d_dbl):
    """区間ごとの行の数・「あり」と出口の差の最大・「なし」「二重」との差の最小（正本 `computation.before_seal.may_print`）。"""
    a = np.abs(np.asarray(zs, dtype=np.float64))
    out = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        m = (a >= lo) & (a < hi)
        n = int(m.sum())
        out.append({'bin': [lo, None if math.isinf(hi) else hi], 'rows': n, 'on_max': float(np.max(d_on[m])) if n else None,
                    'off_min': float(np.min(d_off[m])) if n else None, 'dbl_min': float(np.min(d_dbl[m])) if n else None})
    return out


# ---------------- 凍結の前の確かめ ----------------
def check_items(model, tok, C, L, MQ, stageB_npz, reextract=None, gen_max_new=256, log=None):
    """凍結の前の確かめ（正本 `computation.pre_freeze_checks`）。MQ: 意味のない列の記録（`bprime_meaningless` の出力）。stageB_npz: 段階 B の凍結の活性（係数の確かめ）。
    reextract: 独立の再抽出の道の関数（別の個体の器・None なら落とした項目として記録する）。戻り値: 露出の記録（印字してよい値だけ）。"""
    import torch
    import bprime_facts as BF
    import bprime_meaningless as BM
    import blens_core as CB
    log = log or (lambda s: None)
    rec = collections.OrderedDict(version=VERSION, items=collections.OrderedDict())
    k_layer = int(C['layers']['index'])
    dev = next(model.parameters()).device

    def item(name, fn):
        t0 = _t()
        try:
            out = dict(fn())
        except Exception as e:                           # 項目の落ちは記録して続ける（凍結しない・登録者に上げる）
            out = {'pass': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:300])}
        out['sec'] = round(_t() - t0, 2)
        rec['items'][name] = out
        log('[bprime_phases] 確かめ %s %s（%.1f 秒）' % (name, '通った' if out.get('pass') else '落ちた', out['sec']))
        return out

    ids = BC.ids_for(tok)

    def ledger():
        Lb = BC.build(tok)
        keys = ['prefix_text', 'prefix_ids', 'prefix_pieces', 'heads', 'cells_main', 'extract_contexts', 'arms']
        # 腕の「置き場」は照らさない（v0.1・K18）: 凍結の段階 B の走行器は arms/ の木を歩いて SHA16 の合う最初のファイルを選ぶので、同じ本文のファイルが二か所にある腕
        # （O・Osec・Nk）は、木を歩く順（Windows と Linux で違う）で置き場の名が変わる。本文の SHA16 とトークンの数は照らす
        strip = lambda k, v: ({a: {kk: vv for kk, vv in d.items() if kk != 'path'} for a, d in v.items()} if k == 'arms' else v)
        bad = [k for k in keys if json.dumps(strip(k, Lb[k]), sort_keys=True, ensure_ascii=False) != json.dumps(strip(k, L[k]), sort_keys=True, ensure_ascii=False)]
        paths_differ = sorted(a for a in L['arms'] if (Lb['arms'].get(a) or {}).get('path') != L['arms'][a].get('path'))
        return {'pass': not bad, 'differs': bad, 'arm_paths_differ': paths_differ}
    item('ledger_rebuild', ledger)

    def tokenizer_only():
        A = BF.row_A(tok, C, L, ids)
        bos = [sum(1 for t in ids['main'][k]['prompt'] if t == int(tok.bos_token_id)) for k in ids['main']]
        return {'pass': all(b == 1 for b in bos) and ids['main'][next(iter(ids['main']))]['prompt'][0] == int(tok.bos_token_id), 'variants_kept': A['variants_kept'],
                'v3_checks': A['v3_checks'], 'bos_per_prompt': sorted(set(bos))}
    item('tokenizer_only', tokenizer_only)

    def meaningless():
        seqs, meta = BM.build(tok, C, L)
        return {'pass': BM.ids_sha16([x for v in seqs.values() for x in v]) == MQ['all_sha16'], 'n': len(seqs), 'lengths': meta['lengths']}
    item('meaningless_rebuild', meaningless)
    seqs = collections.OrderedDict((k, list(v)) for k, v in MQ['sequences'].items())
    cells_m, sids = meaningless_cells(C, L, seqs)

    def model_facts():
        tc = G.text_cfg(model)
        mf = C['inputs']['model_facts']
        got = {'num_hidden_layers': int(tc.num_hidden_layers), 'hidden_size': int(tc.hidden_size), 'vocab_size': int(tc.vocab_size), 'final_logit_softcapping': float(tc.final_logit_softcapping),
               'sliding_window': int(tc.sliding_window), 'layer_type': tc.layer_types[k_layer], 'n_decoder_layers': len(G.decoder_layers(model)),
               'lm_head_rows': int(model.lm_head.weight.shape[0])}
        ok = (got['num_hidden_layers'] == mf['num_hidden_layers'] == got['n_decoder_layers'] and got['hidden_size'] == mf['hidden_size'] and got['vocab_size'] == mf['vocab_size'] == got['lm_head_rows']
              and got['final_logit_softcapping'] == mf['final_logit_softcapping'] and getattr(model.config, 'final_logit_softcapping', None) is None
              and got['sliding_window'] == mf['sliding_window'] and got['layer_type'] == C['layers']['layer_type'] and G.layer_index(C['layers']['ratio'], got['num_hidden_layers']) == k_layer)
        return dict(got, **{'pass': ok, 'layer_index': k_layer, 'layer_path': C['layers']['layer_path']})
    item('model_facts', model_facts)
    R = BR.Runner(model, C, k_layer, 1.0, {})

    def norm_form():
        cap = {}
        fn = G.final_norm(model)
        h1 = fn.register_forward_pre_hook(lambda m, a: cap.__setitem__('in', a[0][:, -1, :].detach().clone()))
        h2 = fn.register_forward_hook(lambda m, a, o: cap.__setitem__('out', o[:, -1, :].detach().clone()))
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([cells_m[0].ids], device=dev), use_cache=False, logits_to_keep=1)
        finally:
            h1.remove(); h2.remove()
        x = cap['in'].float()
        w = fn.weight.detach().float()
        base = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + R.eps)
        y = cap['out'].float()
        d_w = float((y - base * w).abs().max())
        d_1w = float((y - base * (1.0 + w)).abs().max())
        return {'pass': d_w < d_1w and d_w <= 0.02 * float(y.abs().max())}                      # 値は印字しない（活性に当たる）
    item('rmsnorm_not_one_plus_weight', norm_form)

    def alignment():
        cap = {}
        n = G.n_layers(model)
        hk = G.decoder_layers(model)[k_layer].register_forward_hook(lambda m, a, o: cap.__setitem__('k', (o[0] if isinstance(o, tuple) else o).detach().clone()))
        hl = G.decoder_layers(model)[n - 1].register_forward_hook(lambda m, a, o: cap.__setitem__('last', (o[0] if isinstance(o, tuple) else o).detach().clone()))
        try:
            with torch.no_grad():
                o = model(input_ids=torch.tensor([cells_m[0].ids], device=dev), output_hidden_states=True, use_cache=False, logits_to_keep=1)
        finally:
            hk.remove(); hl.remove()
        sel = bool(torch.equal(o.hidden_states[k_layer + 1], cap['k']))
        last = bool(torch.equal(o.hidden_states[n], cap['last']))
        return {'pass': sel and not last, 'selected_equal': sel, 'last_equal': last}
    item('layer_alignment', alignment)

    st = {}

    def measure():
        L_ = C['computation']['self_checks']['logit']
        mk = BR.measure_k(R, seqs, sids, L_['measure']['batches'])
        d_on, zs, d_off, d_dbl = R.measure_positions(seqs, sids, 1, wrong=True)
        st['mk'] = mk
        return {'pass': True, 'k': mk['k'], 'z0': mk['z0'], 'k_by_batch': {str(b): v for b, v in mk['k_by_batch'].items()}, 'big_rows': mk['big_rows'], 'fallback': mk['fallback'],
                'n_rows': mk['n_rows'], 'bins_batch1': bin_stats(d_on, zs, d_off, d_dbl)}
    item('logit_tolerance_k', measure)
    mk = st.get('mk')

    def bugs():
        if mk is None:
            raise ToolError('k が無い（前の項目が落ちた）')
        out = {}
        for bug in (None, 'double_norm', 'no_softcap'):
            Rx = R if bug is None else BR.Runner(model, C, k_layer, 1.0, {}, bug=bug)
            states = [Rx.logit_check(c, mk['k'], mk['z0'])['state'] for c in cells_m]
            out[bug or 'correct'] = dict(collections.Counter(states))
        ok = out['correct'].get('否', 0) == 0 and all(out[b].get('否', 0) >= 1 and out[b].get('合', 0) == 0 for b in ('double_norm', 'no_softcap'))
        return {'pass': ok, 'states': out}
    item('bugs_caught', bugs)

    def no_hidden_states():
        cfg = G.text_cfg(model)
        old = getattr(cfg, 'output_hidden_states', False)
        cfg.output_hidden_states = True
        try:
            err = None
            try:
                R.forward(cells_m[0], [K.NOOP], +1, full=False)
            except ToolError as e:
                err = str(e)
        finally:
            cfg.output_hidden_states = old
        return {'pass': err is not None}
    item('no_output_hidden_states_in_add', no_hidden_states)

    def hook_order():
        """集めるフック（transformers が層に掛けたもの）が加減のフックより先か後かで、読み取りと層ごとの取り出しの値が変わらない（R37）。"""
        import run_stageB_local as RB
        c = cells_m[0]
        with torch.no_grad():
            o = model(input_ids=torch.tensor([c.ids], device=dev), output_hidden_states=True, use_cache=False, logits_to_keep=1)
        v = np.random.default_rng(int(C['computation']['before_seal']['meaningless']['seed'])).standard_normal(R.dim)
        v = (v / np.linalg.norm(v) * 0.1 * float(o.hidden_states[k_layer + 1][0, c.mp].float().norm())).astype(np.float32)
        layer = G.decoder_layers(model)[k_layer]

        def run(order):
            cap = {}
            hs = [G.final_norm(model).register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))]
            for j in R.after:
                hs.append(G.decoder_layers(model)[j].register_forward_hook(lambda m, a, oo, j=j: cap.__setitem__(j, (oo[0] if isinstance(oo, tuple) else oo)[:, -1, :].detach().clone())))
            h_add = G.register_hook(model, k_layer, RB.make_hook(v[None, :], 1.0, +1, [c.mp], meta={'bprime': 'hook_order'}))
            foreign = [hid for hid, fn_ in layer._forward_hooks.items() if not hasattr(fn_, 'op4b')]
            if order == 'foreign_after':
                for hid in foreign:
                    layer._forward_hooks.move_to_end(hid)
            try:
                with torch.no_grad():
                    model(input_ids=torch.tensor([c.ids], device=dev), use_cache=False, logits_to_keep=1)
            finally:
                h_add.remove()
                for h_ in hs:
                    h_.remove()
                G.assert_no_hooks(model, k_layer)
            return cap, len(foreign)
        a, nf = run('foreign_before')
        b, _ = run('foreign_after')
        same = all(torch.equal(a[x], b[x]) for x in a)
        return {'pass': same and nf >= 1, 'foreign_hooks_on_layer': nf}
    item('collecting_hook_order', hook_order)

    def determinism_speed():
        c = cells_m[0]
        r1 = R.forward(c, [K.NOOP], +1, want_model_logits=True, full=False)
        r2 = R.forward(c, [K.NOOP], +1, want_model_logits=True, full=False)
        same = bool(torch.equal(r1['model_logits'], r2['model_logits']))
        sp = {}
        for b in (1, int(C['readout']['primary']['batch'])):
            ts = []
            for _ in range(3):
                if dev.type == 'cuda':
                    torch.cuda.synchronize()
                t0 = _t()
                R.forward(c, [K.NOOP] * b, +1, full=True)
                if dev.type == 'cuda':
                    torch.cuda.synchronize()
                ts.append(_t() - t0)
            sp[str(b)] = round(float(np.median(ts)), 4)
        return {'pass': same, 'batch1_repeat_bitwise_equal': same, 'sec_median_by_batch': sp, 'seq_len': len(c.ids)}
    item('determinism_and_speed', determinism_speed)

    def memory():
        if dev.type != 'cuda':
            return {'pass': True, 'skipped': 'cpu'}
        c = cells_m[-1]
        b = int(C['readout']['primary']['batch'])
        torch.cuda.reset_peak_memory_stats()
        peaks = []
        for i in range(30):
            R.forward(c, [K.NOOP] * b, +1, want_layers=True, full=True)
            if i in (4, 29):
                torch.cuda.synchronize()
                peaks.append(torch.cuda.max_memory_allocated() / 2 ** 30)
        return {'pass': peaks[1] <= peaks[0] * 1.001 + 0.01, 'peak_gib_after_5': round(peaks[0], 3), 'peak_gib_after_30': round(peaks[1], 3)}
    item('memory_not_growing', memory)

    def generation_smoke():
        pre, post = BM.template(tok)
        texts, strings = BM.source_texts(C, L)
        vocab, _ = BM.pool(tok, texts, strings)
        rng = np.random.default_rng(int(C['computation']['before_seal']['meaningless']['seed']) + 1)
        chunk = [int(vocab[i]) for i in rng.integers(0, len(vocab), size=64)]
        prompt = list(pre) + chunk + list(post)
        bos_ok = sum(1 for t in prompt if t == int(tok.bos_token_id)) == 1 and prompt[0] == int(tok.bos_token_id)
        _, summ = BB.chain_for_readout(model, prompt, C, tok, None)
        kw = dict(BB.sampling_kwargs(C), max_new_tokens=int(gen_max_new))
        eos = set(int(x) for x in C['behavior_pilot']['sampling']['eos_token_id'])
        think = tok.convert_tokens_to_ids('<|channel>')
        runs = []
        for s in (1, 2):
            x = torch.tensor([prompt], device=dev)
            torch.manual_seed(s)
            t0 = _t()
            out = model.generate(input_ids=x, attention_mask=torch.ones_like(x), **kw)
            sec = _t() - t0
            ids_, finish, stop = BB.cut_response(out[0].tolist(), prompt, eos, kw['max_new_tokens'])
            runs.append({'finish': finish, 'stop_token': stop, 'n_tokens': len(ids_), 'think_token': bool(think in ids_), 'sec': round(sec, 2),
                         'tok_per_sec': round(len(ids_) / sec, 2) if sec > 0 else None, 'sha16': BR.ids_sha16(ids_)})
        differ = runs[0]['sha16'] != runs[1]['sha16']
        return {'pass': bos_ok and differ and all(r['finish'] in ('stop', 'length') for r in runs), 'bos_one': bos_ok, 'sampling_differs': differ,
                'runs': [{k_: v_ for k_, v_ in r.items() if k_ != 'sha16'} for r in runs], 'resolved': summ['fixed'], 'max_new_tokens_smoke': int(gen_max_new)}
    item('generation_smoke', generation_smoke)

    def extraction_stop():
        ctx = collections.OrderedDict(('m%d' % i, list(v)) for i, v in enumerate(list(seqs.values())[:2]))
        BD.activations(model, ctx, k_layer)
        return {'pass': True}
    item('extraction_stops_at_layer', extraction_stop)

    def reextract_path():
        if reextract is None:
            return {'pass': False, 'error': '独立の再抽出の道の器が無い'}
        ctx = collections.OrderedDict(('m%d' % i, list(v)) for i, v in enumerate(list(seqs.values())[:4]))
        a, na, _ = BD.activations(model, ctx, k_layer)
        b = reextract(model, ctx, k_layer)
        RX = C['independent_recompute']['reextract']
        rel = max(abs(float(np.linalg.norm(b[k_])) - na[k_]) / na[k_] for k_ in ctx)
        cos = min(float(np.dot(a[k_], b[k_]) / (np.linalg.norm(a[k_]) * np.linalg.norm(b[k_]))) for k_ in ctx)
        return {'pass': rel <= RX['rel_tol'] and cos >= RX['cos_min']}
    item('reextract_path', reextract_path)

    def coefficient():
        cc = BD.coefficient_checks(stageB_npz, C)
        return {'pass': cc['check_bl3_pass'] and cc['check_B_record_pass'], 'qwen_ratio': cc['bl3_ratio'], 'coef_on_bl3': cc['coef_on_bl3'], 'rel_h': cc['rel_h'], 'rel_v': cc['rel_v']}
    item('coefficient_on_bl3', coefficient)

    def g_check():
        d = int(G.text_cfg(model).hidden_size)
        I = C['nulls']['isotropic']
        g = BD.iso_g(I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'], d)
        v = np.random.default_rng(int(I['seed']) + 7).standard_normal(d)
        iso = np.asarray(CB.iso_directions(v, int(I['seed']), float(C['layers']['ratio']), int(I['count']), int(I['layer_key_scale'])), dtype=np.float64)
        chk = BD.check_iso_against_g(iso, g, float(np.linalg.norm(v)), I['g_rel_tol'])
        return {'pass': chk['pass'], 'rel_max': chk['rel_max'], 'g': BD.g_record(g, I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'])}
    item('isotropic_g', g_check)
    rec['n_forward'] = R.n_forward
    rec['all_pass'] = all(v.get('pass') for v in rec['items'].values())
    return rec


# ---------------- 相 extract ----------------
def extract(model, tok, C, L, g_sha256, stageB_npz, stageB_qwen_acts=None, log=None):
    """相 extract（正本 `directions`・`nulls`・`coefficient`・`transcription_rows.D`）。g_sha256: 下見の前の凍結で記録した g の SHA-256（引き直した g と照らす）。
    戻り値: (npz のバイト, 抽出の記録)。効き目は一つも計算しない（選んだ層の出力だけを取る）。"""
    import torch
    log = log or (lambda s: None)
    k_layer = int(C['layers']['index'])
    ids = BC.ids_for(tok)
    for key, v in ids['extract'].items():
        if BR.ids_sha16(v) != L['extract_contexts'][key]['ids_sha16']:
            raise ToolError('抽出の文脈の並びが台帳と違う: %s' % key)
    t0 = _t()
    acts, norms, _ = BD.activations(model, ids['extract'], k_layer)
    band_ctx, band_pos = collections.OrderedDict(), collections.OrderedDict()
    for key, d in ids['main'].items():
        seq = list(d['prompt']) + list(d['prefix'])
        if BR.ids_sha16(seq) != L['cells_main'][key]['ids_sha16']:
            raise ToolError('主の升目の並びが台帳と違う: %s' % key)
        band_ctx[key] = seq
        band_pos[key] = list(range(len(d['prompt']) - 1, len(seq)))
    _, _, band = BD.activations(model, band_ctx, k_layer, positions=band_pos)
    log('[bprime_phases] 抽出 %d 文脈と帯 %d 升目（%.0f 秒）' % (len(acts), len(band), _t() - t0))
    I = C['nulls']['isotropic']
    d = int(next(iter(acts.values())).shape[0])
    g = BD.iso_g(I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'], d)
    g_rec = BD.g_record(g, I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'])
    if g_rec['g_sha256'] != g_sha256:
        raise ToolError('引き直した g の SHA-256 が下見の前の凍結の値と違う')
    arrays, names, meta = BD.build(acts, C, g=g)
    npz = BD.npz_bytes(arrays)
    cc = BD.coefficient_checks(stageB_npz, C)
    h_mean = BD.h_norm_mean(norms)
    coef = BD.coefficient(cc['bl3_ratio'], meta['vhat_norm'], h_mean)
    D = row_D_values(C, acts, norms, band, arrays, names, meta, coef, stageB_qwen_acts, ids)
    rec = collections.OrderedDict([
        ('kind', 'bprime_extraction_record'), ('version', VERSION), ('layer_index', k_layer), ('npz_sha256', hashlib.sha256(npz).hexdigest().upper()),
        ('groups', {'named': {'names': names['named']}, 'iso': {'count': len(names['iso'])}, 'real': {'names': names['real']}, 'check': {'count': 1}}),
        ('group_sha256', meta['sha256']), ('coefficient', coef), ('bl3_ratio', cc['bl3_ratio']), ('h_norm_mean', h_mean), ('vhat_norm', meta['vhat_norm']),
        ('g', g_rec), ('g_match', meta['iso_check']),
        ('checks', {'g_match': bool(meta['iso_check']['pass']), 'norms_finite_nonzero': True, 'dim_match': True, 'no_readout': True, 'coefficient_checks': bool(cc['check_bl3_pass'] and cc['check_B_record_pass'])}),
        ('row_D', D)])
    return npz, rec


def row_D_values(C, acts, norms, band, arrays, names, meta, coef, qwen_acts, ids):
    """転記行 D の値（正本 `transcription_rows.D`・草案9 の転記行 D の記述の決め）。数（上位の次元の数・実効の押しの比を見る方向）は正本 `transcription_rows.counts`。"""
    import torch
    cnt = C['transcription_rows'].get('counts')
    if not cnt:
        raise ToolError('正本 `transcription_rows.counts`（上位の次元の数・実効の押しの比を見る方向）が無い')
    top = int(cnt['top_dims'])
    H = np.array(list(acts.values()), dtype=np.float64)
    mean = H.mean(axis=0)
    spread = float(np.sqrt(np.mean(np.sum((H - mean) ** 2, axis=1))))

    def top_share(h):
        s = np.sort(np.asarray(h, dtype=np.float64) ** 2)[::-1]
        return float(s[:top].sum() / s.sum())
    vn = float(meta['vhat_norm'])
    band_rows = collections.OrderedDict()
    for key, B in band.items():
        nrm = [float(np.linalg.norm(x)) for x in B]
        band_rows[key] = {'h_norm': nrm, 'push_ratio': [coef * vn / x for x in nrm]}
    pick = []
    for grp, n in (('named', cnt['push_dirs']['named']), ('real', cnt['push_dirs']['real']), ('iso', cnt['push_dirs']['iso'])):
        pick += [(grp, i) for i in range(min(int(n), len(arrays[grp])))]
    ratios = []
    for key, B in band.items():
        hb = torch.tensor(np.asarray(B), dtype=torch.bfloat16)
        for grp, i in pick:
            v = np.asarray(arrays[grp][i], dtype=np.float64)
            add = float(coef) * torch.as_tensor(v.astype(np.float32), dtype=torch.bfloat16)
            eff = (hb + add).float() - hb.float()
            ratios += [float(eff[p].norm()) / (float(coef) * float(np.linalg.norm(v))) for p in range(hb.shape[0])]
    r = np.array(ratios)
    qs = [0.0, 0.05, 0.5, 0.95, 1.0]
    real_pairs = collections.OrderedDict()
    for pn, nat in meta['natural_norms_real'].items():
        a, b = pn.split('~')
        dl = [len(ids['extract']['%s|%s' % (sc, a)]) - len(ids['extract']['%s|%s' % (sc, b)]) for sc in BD.EXTRACT_SCENES]
        real_pairs[pn] = {'len_diff': dl, 'natural_norm': nat}
    unit = lambda X: X / np.linalg.norm(X, axis=-1, keepdims=True)
    out = collections.OrderedDict([
        ('h_norm_by_context', dict(norms)), ('vhat_norm', vn), ('vhat_over_h', {k: vn / v for k, v in norms.items()}), ('coefficient', coef),
        ('group_sha256', meta['sha256']), ('check_cos_max', meta['check_cos_max']),
        ('band', band_rows), ('context_spread_rms', spread),
        ('top_dims', top), ('top_dims_share', {k: top_share(v) for k, v in acts.items()}),
        ('push_dirs', {'named': cnt['push_dirs']['named'], 'real': cnt['push_dirs']['real'], 'iso': cnt['push_dirs']['iso'], 'n': len(pick)}),
        ('effective_push_ratio_quantiles', {str(q): float(np.quantile(r, q)) for q in qs}), ('effective_push_ratio_n', int(r.size)),
        ('real_pairs', real_pairs),
        ('natural_norms_named', meta['natural_norms_named']),
    ])
    if qwen_acts is not None:
        out['qwen_top_dims_share'] = {k: top_share(v) for k, v in qwen_acts.items()}
    return out


# ---------------- 行動の下見 ----------------
def behavior(model, tok, C, L, batch, log=None):
    """行動の下見の生成と採点（正本 `behavior_pilot`）。戻り値: {'trials','scored','roots','summaries','fixed','calls','digests'}。値は印字しない。"""
    log = log or (lambda s: None)
    ids = BC.ids_for(tok)
    env = BB.scorer_env()
    strings = P.variant_strings(L['prefix_text'])
    window = C['behavior_pilot']['root_counts']['b']['window_chars']
    trials, scored, roots, summaries, calls = (collections.OrderedDict() for _ in range(5))
    fixed = None
    for sc, arm in C['cells_main']:
        key = '%s|%s' % (sc, arm)
        prompt = ids['main'][key]['prompt']
        if BR.ids_sha16(list(prompt) + list(ids['main'][key]['prefix'])) != L['cells_main'][key]['ids_sha16']:
            raise ToolError('升目の並びが台帳と違う: %s' % key)
        g = BB.generate_cell(model, tok, C, key, prompt, batch, row_c_fixed=fixed, log=log)
        fixed = g['fixed']
        sent, fam = BB.sent_of(key)
        sids = [int(x) for x in L['cells_main'][key]['set_ids']]
        trials[key] = g['trials']
        scored[key] = [BB.score_trial(t, fam, sent, env) for t in g['trials']]
        roots[key] = [BB.root_counts_trial(t, prompt, sids, L['prefix_ids'], strings, window, env['parser_mod']) for t in g['trials']]
        summaries[key] = BB.cell_summary(C, key, g['trials'], scored[key], roots[key])
        calls[key] = g['calls']
    return {'trials': trials, 'scored': scored, 'roots': roots, 'summaries': summaries, 'fixed': fixed, 'calls': calls, 'digests': BB.closing_digests(trials, scored, env)}


# ---------------- 読み取りの下見 ----------------
def pilot(model, tok, C, L, facts_pre, closed, k, z0, log=None):
    """読み取りの下見（正本 `pilot`）。facts_pre: 凍結の前の転記行（揺れの版の割り方）。closed: 行動の下見の閉じた記録（升目の集計・解決された設定の要約・器の誤りの印）。"""
    log = log or (lambda s: None)
    k_layer = int(C['layers']['index'])
    keys = ['%s|%s' % (sc, arm) for sc, arm in C['cells_main']]
    cells = BR.build_cells(tok, C, L, keys)
    variants = collections.OrderedDict((n, v['ids']) for n, v in facts_pre['facts']['A']['variants'].items() if v['keep'])
    behavior_state = BB.iii_status(C, closed.get('summaries') or {}, tool_error=bool(closed.get('tool_error')))
    procs, summ = BB.chain_for_readout(model, cells[keys[0]].ids, C, tok, closed.get('fixed'))
    R = BR.Runner(model, C, k_layer, 1.0, {})
    t0 = _t()
    rec = BR.run_pilot(R, [cells[k_] for k_ in keys], C, variants, behavior_state, procs, k, z0)
    rec['behavior_state'] = {k_: v for k_, v in behavior_state.items() if k_ != 'rate'}
    rec['chain'] = summ['fixed']['processors']
    rec['variants_used'] = list(variants)
    log('[bprime_phases] 読み取りの下見（%.0f 秒・順伝播 %d）' % (_t() - t0, R.n_forward))
    return rec


# ---------------- 本の計算の組 ----------------
def main_part(part, model, C, cells, dirs, names, pilot_rec, k, z0, coef, rows_rc=None, log=None):
    """本の計算の組（正本 `computation`・`independent_recompute`・`descriptive.path_difference`）。値は印字しない。"""
    log = log or (lambda s: None)
    R = BR.Runner(model, C, int(C['layers']['index']), coef, dirs)
    if part == 'main':
        return BR.run_main_phase(R, C, cells, names, pilot_rec, k, z0, log=log)
    if part == 'pathdiff':
        if int(pilot_rec['batch']) != 1:
            raise ToolError('道の違いの記述は、本の計算がバッチ一に移ったときだけ走らせる')
        return BR.run_main_phase(R, C, cells, names, pilot_rec, k, z0, batch_override=int(C['readout']['primary']['batch']), log=log)
    if part == 'recompute':
        if not rows_rc:
            raise ToolError('独立の再計算の行が無い')
        rows, dbr = rows_rc
        return {'hook': BR.recompute_hook_path(R, rows, dbr, log=log), 'rows': [[n, c.key, s] for n, c, s in rows]}
    raise ToolError('組の名が決まりの外: %s' % part)
```

### 9. `tools/colab/boot_bprime.py`（起動器（相 recompute の三つの組の呼び方））

- 出所: 作業の置き場 `tools/colab/boot_bprime.py`・SHA16 2D332F457D1E8733・28493 字

```python
# -*- coding: utf-8 -*-
"""boot_bprime.py v0 —— B′ の Colab 起動器（G4・Gemma-4-31B-it・bf16・transformers 5 系・2026-09-30・コーディネータ南無弥勒如来）。

相（OP4B_PHASE）と段（OP4B_STEP）:
  check                 凍結の前の確かめ（正本 `computation.before_seal`・`computation.pre_freeze_checks`）。段は一つ。意味のない列だけで順伝播と生成の煙試験をし、
                        露出の記録（check.json・印字してよい値だけ）を置く。場面・腕・指示・書き出しを含む入力はトークナイザだけで確かめる。
  extract   start|run   相 extract（封印の後）。抽出の記録（転記行 D の元・npz の SHA・係数・g との一致の合否）と npz を置く（npz は公開の置き場に入れない）。
  behavior  start|run   行動の下見（生成・復号・凍結の採点・書き出しの根の件数・升目の集計）。run は最初の順伝播の前に、抽出の記録の形の項目を確かめる（T01）。
  pilot     start|run   読み取りの下見（模型を読み込み直した新しいランタイムで）。run は行動の下見の閉じた記録を確かめてから走る。
  main      start|run   本の計算（本の凍結の後）。OP4B_PART: main・pathdiff（pathdiff は本の計算がバッチ一のときだけ）。値と札を印字しない。
  recompute start|run   独立の再計算と独立の再抽出。OP4B_PART: hook・rewrite・reextract（rewrite と reextract は書き手と別の個体の器）。値を印字しない。
start: 起動の記録（時刻・セッション・GPU の名・正本と器の SHA・段の名・コミット）を書いて止まる。コーディネータがそれを公開の置き場の `records/Bprime/runs/` に写して push し
  （登録者の確認を得る）、そのコミットを OP4B_COMMIT に与えて run を走らせる。run は取り出したコミットの起動の記録が手元の起動の記録と一字違わず同じことを確かめてから、
  最初の順伝播をする（正本 `computation.start_records`・T13）。終わりに出力の SHA の記録（end-<相>.json）を書く（これも公開の置き場に置く）。
止める（登録者に相談）: 版・GPU・重みの SHA・凍結と封印の記録・取り出した器と正本の SHA・起動の記録の不一致・暦の期限（K2）・器の誤り（正本 `computation.tool_error`）・予期しない誤り。
印字の決まり: 相 check は `computation.before_seal.may_print` の値だけ。ほかの相は段の名・時間・数・SHA だけを印字する（値は置き場の記録に置く）。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する。資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。進みは progress.log にも書く。
セルに打つ一行（先頭の下線は type の事故の緩衝・<commit> は 40 桁）:
  ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='check';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_bprime.py').read())
DRY（手元の検査・OP4B_DRY=1）: 小さな乱数の Gemma 4（`dry_bprime.tiny_model`）を CPU で。OP4B_REPO_DIR（凍結の器の公開の置き場）・OP4B_BPRIME_DIR（B′ の置き場）・OP4B_OUT が要る。
  版・GPU・重み・凍結と封印の記録と起動の記録の公開は見ない（印を残す）。
柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, time, uuid, shutil, hashlib, datetime, traceback, subprocess, zipfile, collections

VERSION = 'v0.3'        # v0.3（2026-09-30）: DRY の正本の写しで、読み取りの下見の (i)(ii) の門を開ける（質量の下限 0・確率の幅 [0, 1]・`dry_bprime.py` の P1 と同じ・小さな乱数の模型では 8 升目とも落ちて本の計算の相へ進めなかった）。前の版は `prev/boot_bprime-v0.2.py`／v0.2（2026-09-30）: run の段で、出力の置き場に起動の記録の写しを置く（閉じる器と凍結の器が出力の置き場で読む・Colab の合成データの正式の確かめで、閉じる器が止まって見つけた・K19）。前の版は `prev/boot_bprime-v0.1.py`／v0.1（2026-09-30）: 本の計算と独立の再計算の相で、台帳のつながりを本の凍結の後の行だけで照らす（前は全ての行を渡した・本の凍結の器を書いて見つけた）・独立の再抽出の組に方向を渡す（正本の口の五つの引数・前は四つ）。前の版は `prev/boot_bprime-v0.py`
T0 = time.time()
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
PHASES = ('check', 'extract', 'behavior', 'pilot', 'main', 'recompute')
STEPS = ('start', 'run')
PARTS = {'main': ('main', 'pathdiff'), 'recompute': ('hook', 'rewrite', 'reextract')}
STAGE_NAME = {'extract': '相 extract', 'behavior': '行動の下見', 'pilot': '読み取りの下見', 'main': '本の計算', 'recompute': '独立の再計算'}
SPARSE = ['tools', 'arms', 'design', 'records', 'results/dirB']
LOG = []
CTX = {'od': None, 'session': None, 'dry': False, 'progress': None}
CLAUSE = '本記録は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
JST = datetime.timezone(datetime.timedelta(hours=9))
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


def say(line):
    print(line, flush=True)
    if CTX['progress']:
        with open(CTX['progress'], 'a', encoding='utf-8') as fh:
            fh.write(line + '\n')


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
    say('[boot_bprime] %-18s %7.0fs %s' % (step, time.time() - T0, kw or ''))


def jdefault(o):
    if hasattr(o, 'tolist'):
        return o.tolist()
    if hasattr(o, 'item'):
        return o.item()
    raise TypeError(type(o))


def write_json(path, obj):
    json.dump(obj, open(path, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=jdefault)
    return sha256f(path)


def sh(cmd, check=True):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-3000:])
        raise RuntimeError('失敗: %s' % cmd)
    return r


def package(tag, extra=None):
    """置き場の中身を zip にして落とす（段の終わり・止め・誤り）。session を書いてから zip にし、zip の SHA-256 を記す。"""
    od, S = CTX['od'], CTX['session']
    if not od or S is None:
        return None
    S.update(extra or {})
    S.update({'log': LOG, 'packaged': tag, 'packaged_at': now(), 'seconds': round(time.time() - T0, 1), 'clause': CLAUSE})
    write_json(os.path.join(od, 'session.json'), S)
    zp = od + ('.zip' if tag == 'final' else '-%s.zip' % tag)
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(od)):
            z.write(os.path.join(od, fn), os.path.join(os.path.basename(od), fn))
    zsha = sha256f(zp)
    S.setdefault('zips', []).append({'tag': tag, 'zip': os.path.basename(zp), 'sha256': zsha})
    write_json(od + '-zips.json', {'zips': S['zips'], 'clause': CLAUSE})
    mark('packaged', tag=tag, zip=os.path.basename(zp), sha256=zsha)
    if not CTX['dry']:
        try:
            from google.colab import files
            files.download(zp)
        except Exception as e_:
            print('[boot_bprime] zip の自動のダウンロードが走らなかった（左の「ファイル」から落とす）: %s' % e_)
    return zp


def stop(msg):
    mark('stop', reason=msg)
    package('stopped', {'stopped': msg})
    sys.exit('[boot_bprime] 止める（登録者に相談）: ' + msg)


def run():
    PHASE = os.environ.get('OP4B_PHASE', 'check')
    STEP = os.environ.get('OP4B_STEP', 'run' if PHASE == 'check' else '')
    COMMIT = os.environ.get('OP4B_COMMIT', '')
    DRY = os.environ.get('OP4B_DRY') == '1'
    if PHASE not in PHASES:
        sys.exit('[boot_bprime] 相は %s のどれか' % '・'.join(PHASES))
    if PHASE != 'check' and STEP not in STEPS:
        sys.exit('[boot_bprime] OP4B_STEP は start か run')
    part = os.environ.get('OP4B_PART', '')
    if PHASE in PARTS and STEP == 'run' and part not in PARTS[PHASE]:
        sys.exit('[boot_bprime] OP4B_PART は %s のどれか一つ' % '・'.join(PARTS[PHASE]))
    if not DRY:
        stray = sorted(k for k in os.environ if k.startswith('OP4B_DRY') or k in ('OP4B_REPO_DIR', 'OP4B_BPRIME_DIR', 'OP4B_OUT'))
        if stray:
            sys.exit('[boot_bprime] DRY でないのに検査用の環境変数がある: %s' % '・'.join(stray))
        if not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
            sys.exit('[boot_bprime] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
    say('[boot_bprime] %s 開始 phase=%s step=%s part=%s %s' % (VERSION, PHASE, STEP or '-', part or '-', 'DRY' if DRY else COMMIT))

    # ---- 1. 置き場（コミット固定）
    if DRY:
        REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
        ROOT = os.path.abspath(os.environ['OP4B_BPRIME_DIR'])
        OUTROOT = os.path.abspath(os.environ['OP4B_OUT'])
    else:
        REPO, OUTROOT = '/content/ontology-preamble-4b', '/content/op4b-Bprime'
        ROOT = REPO
        head_ok = os.path.isdir(os.path.join(REPO, '.git')) and sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
        if not head_ok:
            if os.path.isdir(os.path.join(REPO, '.git')):
                sh(['git', '-C', REPO, 'fetch', '-q', '--filter=blob:none', 'origin', COMMIT])
            else:
                shutil.rmtree(REPO, ignore_errors=True)
                sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
                sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone'] + SPARSE)
            sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
        if sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() != COMMIT:
            stop('取り出したコミットが OP4B_COMMIT と違う')
        dirty = sh(['git', '-C', REPO, 'status', '--porcelain'], check=False).stdout.strip()
        if dirty:
            stop('取り出した作業木に変更がある: %s' % dirty.splitlines()[:5])
    os.environ['OP4B_REPO'] = REPO
    os.makedirs(OUTROOT, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    od = os.path.join(OUTROOT, '%s%s%s-%s' % (PHASE, ('-' + STEP) if STEP else '', ('-' + part) if part else '', stamp))
    os.makedirs(od, exist_ok=True)
    CTX.update(od=od, dry=DRY, progress=os.path.join(od, 'progress.log'), session={'kind': 'bprime_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY, 'step': STEP, 'part': part})
    TOOLS = os.path.join(ROOT, 'tools')
    for p_ in (os.path.join(REPO, 'tools'), TOOLS):
        if p_ not in sys.path:
            sys.path.insert(0, p_)
    CANON = os.path.join(ROOT, 'design', 'contrasts-Bprime.json')
    C = json.load(open(CANON, encoding='utf-8'))
    RECS = os.path.join(ROOT, 'records', 'Bprime')
    L = json.load(open(os.path.join(TOOLS, 'ledger-bprime.json'), encoding='utf-8'))
    FRP = os.path.join(RECS, 'FREEZE-RECORD-Bprime.json')
    SRP = os.path.join(RECS, 'sealing-record-Bprime.json')
    FR = SR = None
    if PHASE != 'check':
        if DRY:
            mark('dry_no_gate', note='DRY は凍結と封印の記録と起動の記録の公開を見ない')
            FR = json.load(open(os.environ['OP4B_DRY_FREEZE'], encoding='utf-8')) if os.environ.get('OP4B_DRY_FREEZE') else None
        else:
            for p_ in (FRP, SRP):
                if not os.path.exists(p_):
                    stop('相 %s は下見の前の凍結と封印の後に走らせる（%s が無い）' % (PHASE, os.path.basename(p_)))
            FR = json.load(open(FRP, encoding='utf-8'))
            SR = json.load(open(SRP, encoding='utf-8'))
            import bl3_core as K_
            now_s = {rp: (sha16f(os.path.join(REPO, *rp.split('/'))) if os.path.exists(os.path.join(REPO, *rp.split('/'))) else None) for rp in FR['frozen_sha16']}
            sha_map = (FR.get('main_freeze') or {}).get('frozen_sha16') if PHASE in ('main', 'recompute') else FR['frozen_sha16']
            if PHASE in ('main', 'recompute') and not sha_map:
                stop('相 %s は本の凍結の後に走らせる（凍結の記録に本の凍結が無い）' % PHASE)
            devs_ = list(FR.get('deviations') or [])
            if PHASE in ('main', 'recompute'):
                devs_ = devs_[int(FR['main_freeze']['deviations_n']):]        # 本の凍結の値からは、本の凍結の後に記した台帳の行だけでつなぐ（v0.1・芯の関数の決まり）
            bad = K_.ledger_chain_bad(sha_map, {rp: now_s.get(rp) for rp in sha_map}, devs_, paths=list(sha_map))
            if bad:
                stop('凍結の記録の SHA16 と取り出したファイルが違う: %s' % bad)
            for role in ('coordinator', 'registrant'):
                pp = os.path.join(REPO, *SR['predictions'][role]['path'].split('/'))
                if not os.path.exists(pp) or sha256f(pp) != SR['predictions'][role]['sha256']:
                    stop('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
            import bprime_core as Pc
            seal_jst = datetime.datetime.fromisoformat(SR['sealed_at_jst'])
            if Pc.calendar_closed(seal_jst, datetime.datetime.now(JST), C['computation']['stops']['calendar']['days'], False):
                stop('暦の期限を過ぎた（正本 `computation.stops.calendar`）: %s' % C['computation']['stops']['calendar']['close_sentence'])
            mark('frozen', checked=len(sha_map))
    mark('repo', commit=COMMIT[:12] or 'dry', canon=C['version'], canon_sha16=sha16f(CANON), out=od)

    # ---- 2. 版と GPU と決定性の設定
    import importlib.metadata as md

    def ver(k):
        try:
            return md.version(k)
        except Exception:
            return None
    VER = {k: ver(k) for k in ('numpy', 'scipy', 'torch', 'transformers', 'tokenizers', 'huggingface_hub', 'jinja2', 'safetensors', 'accelerate')}
    V = C['inputs']['versions']
    pins = dict((FR or {}).get('prefreeze', {}).get('pins') or {})
    pins.update({'transformers': V['transformers'], 'torch': V['torch']})
    bad_v = {k: VER.get(k) for k, v in pins.items() if VER.get(k) != v}
    if bad_v and not DRY:
        mark('pin', installing=bad_v)
        pk = ['%s==%s' % (k, v) for k, v in pins.items() if k != 'torch' and k in bad_v]
        if 'torch' in bad_v:
            cuda = V['torch'].split('+')[1]
            sh([sys.executable, '-m', 'pip', 'install', '-q', 'torch==%s' % V['torch'], '--index-url', 'https://download.pytorch.org/whl/%s' % cuda])
        if pk:
            sh([sys.executable, '-m', 'pip', 'install', '-q'] + pk)
        print('[boot_bprime] 版を入れ直した。**ランタイムを再起動して（「ランタイム」→「セッションを再起動」）、同じ一行をもう一度走らせる**', flush=True)
        sys.exit(0)
    GPU = 'dry'
    if not DRY:
        GPU = sh('nvidia-smi --query-gpu=name --format=csv,noheader', check=False).stdout.strip().split('\n')[0]
        if C['inputs']['gpu']['name'] not in GPU:
            stop('GPU %s は登録の環境（%s）でない' % (GPU, C['inputs']['gpu']['name']))
    mark('versions', versions=VER, gpu=GPU)
    os.environ['HF_HUB_DISABLE_XET'] = '1'
    import numpy as np
    import torch
    attn = os.environ.get('OP4B_ATTN', 'sdpa') if PHASE == 'check' else ((FR or {}).get('prefreeze', {}).get('attn_implementation') or ('eager' if DRY else None))
    if attn is None:
        stop('凍結の記録に注意の実装が無い')
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision('highest')
    DET = {'allow_tf32_matmul': torch.backends.cuda.matmul.allow_tf32, 'allow_tf32_cudnn': torch.backends.cudnn.allow_tf32, 'float32_matmul_precision': torch.get_float32_matmul_precision(),
           'attn_implementation': attn}
    if FR and 'determinism' in (FR.get('prefreeze') or {}) and {k: FR['prefreeze']['determinism'].get(k) for k in DET} != DET and not DRY:
        stop('決定性の設定が凍結の記録と違う')
    import bprime_gemma as G
    import bprime_core as P
    import bprime_run as BR
    import bprime_directions as BD
    import bprime_behavior as BB
    import bprime_phases as PH
    TOOL_FILES = sorted(fn for fn in os.listdir(TOOLS) if fn.startswith('bprime_') and fn.endswith('.py'))
    TOOL_SHA = {fn: sha16f(os.path.join(TOOLS, fn)) for fn in TOOL_FILES}
    TOOL_SHA['colab/boot_bprime.py'] = sha16f(os.path.join(TOOLS, 'colab', 'boot_bprime.py')) if os.path.exists(os.path.join(TOOLS, 'colab', 'boot_bprime.py')) else None

    # ---- 3. 起動の記録（start は書いて止まる・run は公開の版と照らす）
    START_LOCAL = os.path.join(OUTROOT, 'start-%s%s.json' % (PHASE, ('-' + part) if part else ''))
    if PHASE != 'check' and STEP == 'start':
        rec = collections.OrderedDict([('kind', 'bprime_start_record'), ('stage', STAGE_NAME[PHASE]), ('phase', PHASE), ('part', part or None), ('session', str(uuid.uuid4())),
                                       ('time_utc', now()), ('time_jst', datetime.datetime.now(JST).isoformat(timespec='seconds')), ('gpu', GPU), ('commit', COMMIT or 'dry'),
                                       ('contract_sha16', sha16f(CANON)), ('tools_sha16', TOOL_SHA), ('freeze_record_sha16', sha16f(FRP) if os.path.exists(FRP) else None),
                                       ('seal_record_sha16', sha16f(SRP) if os.path.exists(SRP) else None), ('versions', VER), ('clause', CLAUSE)])
        sha = write_json(START_LOCAL, rec)
        shutil.copy(START_LOCAL, os.path.join(od, os.path.basename(START_LOCAL)))
        CTX['session'].update(start_record=os.path.basename(START_LOCAL), start_sha256=sha)
        package('final', {'finished': now()})
        say('[boot_bprime] 起動の記録を書いた（SHA-256 %s）。records/Bprime/runs/ に写して公開の置き場に置き、そのコミットで OP4B_STEP=run を走らせる' % sha)
        return od
    if PHASE != 'check':
        if not os.path.exists(START_LOCAL):
            stop('手元の起動の記録が無い（同じランタイムで start を先に走らせる）')
        pub = os.path.join(RECS, 'runs', os.path.basename(START_LOCAL))
        if DRY:
            mark('dry_start_unpublished', local=os.path.basename(START_LOCAL))
        elif not os.path.exists(pub) or sha256f(pub) != sha256f(START_LOCAL):
            stop('公開の置き場の起動の記録が手元の起動の記録と違う（写して push してから run を走らせる）')
        START = json.load(open(START_LOCAL, encoding='utf-8'))
        if START['phase'] != PHASE or (START.get('part') or '') != part or START['contract_sha16'] != sha16f(CANON) or START['tools_sha16'] != TOOL_SHA:
            stop('起動の記録の相・組・正本と器の SHA が今と違う')
        CTX['session'].update(start_record=os.path.basename(START_LOCAL), start_sha256=sha256f(START_LOCAL), session_id=START['session'])
        shutil.copy(START_LOCAL, os.path.join(od, os.path.basename(START_LOCAL)))          # 出力の置き場に起動の記録の写し（閉じる器・凍結の器が出力の置き場で読む・SHA-256 は session の start_sha256・v0.2・K19）

    # ---- 4. 重みと模型
    from transformers import AutoTokenizer
    if DRY:
        import dry_bprime as DR
        tok = AutoTokenizer.from_pretrained(DR.HF)
        model, _, _ = DR.tiny_model(5, 4.0, torch.float32)
        W_SHA = {}
        C = dry_contract(C, model)                                          # DRY だけ: 小さな模型の形に合わせた正本の写し（正本のファイルは変えない・v0.1）
        mark('dry_contract', layer_index=C['layers']['index'], iso=C['nulls']['isotropic']['count'], max_new=C['inputs']['generation_B']['max_tokens'],
             mass_min=C['pilot']['mass_min'], p_bounds=C['pilot']['p_bounds'])
    else:
        from huggingface_hub import snapshot_download
        from transformers import Gemma4ForConditionalGeneration
        M = C['inputs']['model']
        snap = snapshot_download(M['id'], revision=M['revision'])
        man = json.load(open(os.path.join(RECS, 'MANIFEST-gemma-4-31B-it.json'), encoding='utf-8'))
        W_SHA = {fn: sha256f(os.path.join(snap, fn)) for fn in man['files']}
        badw = [fn for fn, r in man['files'].items() if W_SHA[fn] != r['sha256'].upper()]
        if badw:
            stop('重みか設定の SHA-256 が目録と違う: %s' % badw)
        shards = sorted(set(json.load(open(os.path.join(snap, 'model.safetensors.index.json'), encoding='utf-8'))['weight_map'].values()))
        if [s for s in shards if s not in man['files']]:
            stop('重みの断片が目録に無い（凍結の前に目録を作る・K9）')
        tok = AutoTokenizer.from_pretrained(snap)
        t_ = time.time()
        model = Gemma4ForConditionalGeneration.from_pretrained(snap, dtype=torch.bfloat16, device_map='cuda', attn_implementation=attn).eval()
        mark('load', seconds=round(time.time() - t_, 1), alloc_gib=round(torch.cuda.memory_allocated() / 2 ** 30, 2))
    CTX['session'].update(gpu=GPU, versions=VER, determinism=DET, weights_sha256=W_SHA, canon_sha16=sha16f(CANON), tools_sha16=TOOL_SHA)
    S = CTX['session']

    def finish(outputs):
        """出力の SHA の記録（end-<相>.json・公開の置き場に置く）を書いて zip にする。"""
        end = {'kind': 'bprime_end_record', 'phase': PHASE, 'part': part or None, 'session': S.get('session_id'), 'time_utc': now(),
               'outputs_sha256': {fn: sha256f(os.path.join(od, fn)) for fn in outputs}, 'clause': CLAUSE}
        write_json(os.path.join(od, 'end-%s%s.json' % (PHASE, ('-' + part) if part else '')), end)
        package('final', {'finished': now()})
        mark('done', outputs=len(outputs))
        return od

    # ---- 5. 相
    if PHASE == 'check':
        MQ = json.load(open(os.path.join(RECS, 'meaningless-Bprime.json'), encoding='utf-8'))
        try:
            import bprime_reextract as RX
            rx = RX.reextract
        except ImportError:
            rx = None
        rec = PH.check_items(model, tok, C, L, MQ, os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'main_position_activations.npz'), reextract=rx,
                             gen_max_new=int(os.environ.get('OP4B_SMOKE_TOKENS', '256')), log=say)
        rec.update({'gpu': GPU, 'versions': VER, 'determinism': DET, 'clause': CLAUSE})
        write_json(os.path.join(od, 'check.json'), rec)
        mark('check', all_pass=rec['all_pass'], failed=[k for k, v in rec['items'].items() if not v.get('pass')])
        return finish(['check.json'])
    TOOL_ERR = (P.ToolError, AssertionError)
    if PHASE == 'extract':
        npz_stageB = os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'main_position_activations.npz')
        g_sha = (FR or {}).get('prefreeze', {}).get('g', {}).get('g_sha256') if not DRY else os.environ.get('OP4B_DRY_G')
        try:
            q = BD.bl3_ratio(npz_stageB)['acts']
            npz, rec = PH.extract(model, tok, C, L, g_sha, npz_stageB, stageB_qwen_acts=q, log=say)
        except TOOL_ERR as e_:
            write_json(os.path.join(od, 'extract-tool-error.json'), {'tool_error': str(e_), 'clause': CLAUSE})
            finish(['extract-tool-error.json'])
            stop('器の誤りで相 extract が止まった（直してやり直すかは登録者の裁定）: %s' % e_)
        open(os.path.join(od, 'directions-Bprime.npz'), 'wb').write(npz)
        rec.update({'start_record_sha256': S.get('start_sha256'), 'session': S.get('session_id'), 'time_utc': now(), 'versions': VER, 'weights_sha256': W_SHA, 'clause': CLAUSE})
        write_json(os.path.join(od, 'extraction-record-Bprime.json'), rec)
        mark('extract', npz_sha256=rec['npz_sha256'][:16], g_match=rec['checks']['g_match'])
        return finish(['directions-Bprime.npz', 'extraction-record-Bprime.json'])
    if PHASE == 'behavior':
        ex = os.path.join(RECS, 'extract', 'extraction-record-Bprime.json')
        if not DRY:
            miss = PH_form_items(ex, C, S)
            if miss:
                stop('抽出の記録の形の項目がそろわない: %s' % miss)
        batch = int((FR or {}).get('prefreeze', {}).get('behavior_batch') or os.environ.get('OP4B_DRY_BATCH', '8'))
        try:
            out = PH.behavior(model, tok, C, L, batch, log=say)
        except TOOL_ERR as e_:
            write_json(os.path.join(od, 'behavior-tool-error.json'), {'tool_error': str(e_), 'clause': CLAUSE})
            finish(['behavior-tool-error.json'])
            stop('器の誤りで行動の下見が止まった（正本 `behavior_pilot.order`: 読み取りの下見は続ける・そこまでの記録を閉じて公開する）: %s' % e_)
        write_json(os.path.join(od, 'behavior-trials.json'), {'trials': out['trials'], 'calls': out['calls'], 'fixed': out['fixed'], 'clause': CLAUSE})
        write_json(os.path.join(od, 'behavior-scored.json'), {'scored': out['scored'], 'roots': out['roots'], 'summaries': out['summaries'], 'digests': out['digests'], 'clause': CLAUSE})
        mark('behavior', cells=len(out['summaries']), trials=sum(len(v) for v in out['trials'].values()), gen_ids_sha256=out['digests']['gen_ids_sha256'][:16])
        return finish(['behavior-trials.json', 'behavior-scored.json'])
    if PHASE == 'pilot':
        closed = json.load(open(os.path.join(RECS, 'behavior', 'behavior-closed-Bprime.json'), encoding='utf-8')) if not DRY else json.load(open(os.environ['OP4B_DRY_CLOSED'], encoding='utf-8'))
        facts = json.load(open(os.path.join(RECS, 'facts-Bprime-pre.json'), encoding='utf-8'))
        kz = (FR or {}).get('prefreeze', {}).get('logit_k') or ({'k': 1.0, 'z0': 4} if DRY else None)
        if kz is None:
            stop('凍結の記録に出口の値の自己検査の k が無い')
        try:
            rec = PH.pilot(model, tok, C, L, facts, closed, kz['k'], kz['z0'], log=say)
        except TOOL_ERR as e_:
            rec = {'tool_error': str(e_)}
        rec.update({'start_record_sha256': S.get('start_sha256'), 'session': S.get('session_id'), 'time_utc': now(), 'clause': CLAUSE})
        write_json(os.path.join(od, 'pilot-Bprime.json'), rec)
        if 'tool_error' in rec:
            finish(['pilot-Bprime.json'])
            stop('器の誤りで読み取りの下見が止まった（正本 `pilot.tool_error`・直してやり直すかは登録者の裁定）: %s' % rec['tool_error'])
        mark('pilot', q1=(rec.get('decision') or {}).get('q1'), batch=rec.get('batch'), n_forward=rec.get('n_forward'))
        return finish(['pilot-Bprime.json'])
    # 本の計算と独立の再計算
    npz_in = os.environ.get('OP4B_NPZ', os.path.join(OUTROOT, 'in', 'directions-Bprime.npz'))
    exj = os.path.join(RECS, 'extract', 'extraction-record-Bprime.json') if not DRY else os.environ['OP4B_DRY_EXTRACT']
    try:
        dirs, names = BR.load_dirs(npz_in, exj, C)
    except P.ToolError as e_:
        stop(str(e_))
    EX = json.load(open(exj, encoding='utf-8'))
    pil = (FR or {}).get('main_freeze', {}).get('pilot') if not DRY else json.load(open(os.environ['OP4B_DRY_PILOT'], encoding='utf-8'))
    if not pil or pil.get('tool_error') or (pil.get('decision') or {}).get('stop'):
        stop('本の凍結の下見の記録が無いか、止める・器の誤り（本の計算は走らせない）')
    kz = (FR or {}).get('prefreeze', {}).get('logit_k') or {'k': 1.0, 'z0': 4}
    keys = ['%s|%s' % (sc, arm) for sc, arm in C['cells_main']]
    cells = BR.build_cells(tok, C, L, keys)
    out = collections.OrderedDict(part=part, clause=CLAUSE)
    try:
        if PHASE == 'main':
            out['result'] = PH.main_part(part, model, C, cells, dirs, names, pil, kz['k'], kz['z0'], float(EX['coefficient']), log=say)
        elif part == 'hook':
            import bl3_core as K_
            rows, dbr = K_.recompute_set(C['main_rows'], [n[len('real:'):] for n in names['real']], C['nulls']['real']['swap_siblings'], len(names['iso']),
                                         (pil.get('decision') or {}).get('dropped', []))
            out['result'] = PH.main_part('recompute', model, C, cells, dirs, names, pil, kz['k'], kz['z0'], float(EX['coefficient']),
                                         rows_rc=([(n, cells[ck], s) for n, ck, s in rows], dbr), log=say)
        elif part == 'rewrite':
            import bprime_recompute_rewrite as RW              # 書き手と別の個体の器
            out['result'] = RW.recompute_rewrite(model, tok, C, L, dirs, names, pil, float(EX['coefficient']))
        elif part == 'reextract':
            import bprime_reextract as RX                      # 書き手と別の個体の器
            out['result'] = RX.reextract_all(model, tok, C, L, dirs)          # 正本 `independent_recompute.interfaces.reextract` の口（v0.1・前は dirs を渡していなかった）
    except TOOL_ERR as e_:
        out['tool_error'] = str(e_)
    fn = '%s-%s.json' % (PHASE, part)
    write_json(os.path.join(od, fn), out)
    if 'tool_error' in out:
        finish([fn])
        stop('器の誤りで組 %s が止まった（結果を開かずに登録者に上げる）: %s' % (part, out['tool_error']))
    mark('part', part=part)
    return finish([fn])


def dry_contract(C, model):
    """DRY（手元の検査）だけで使う正本の写し: 小さな模型の層の数から層の添字（`direction_B.layer_index` の式）と `hidden_states_index` を作り直し、
    等方の本数（OP4B_DRY_ISO・既定 9）と生成の上限（OP4B_DRY_MAX_NEW・既定 12）を小さくし、読み取りの下見の (i)(ii) の門（`pilot.mass_min`・`pilot.p_bounds`）を開ける
    （小さな乱数の模型は選択肢の質量が下限に届かないので、門がそのままでは下見が「止める」になり、本の計算の相から後を通せない・`dry_bprime.py` の P1 と同じ置き換え・v0.3）。ほかの鍵は変えない。
    模型の事実（`inputs.model_facts`）は本物の模型の値のまま残す（小さな模型を本物と取り違えさせない・書き手と別の個体の器は層の数と次元で本物かを見分ける）。
    そのため DRY の相 check の「模型の事実」の項目は落ちるのが正しい形になる。正本のファイルの SHA16 は元のまま記録に入る（DRY の印つき）。"""
    import copy
    import bprime_gemma as G_
    Cd = copy.deepcopy(C)
    n = int(model.config.text_config.num_hidden_layers)
    Cd['layers']['index'] = G_.layer_index(Cd['layers']['ratio'], n)
    Cd['layers']['hidden_states_index'] = Cd['layers']['index'] + 1
    Cd['nulls']['isotropic']['count'] = int(os.environ.get('OP4B_DRY_ISO', '9'))
    Cd['inputs']['generation_B'] = dict(Cd['inputs']['generation_B'], max_tokens=int(os.environ.get('OP4B_DRY_MAX_NEW', '12')))
    Cd['pilot'] = dict(Cd['pilot'], mass_min=0.0, p_bounds=[0.0, 1.0])
    Cd['dry_contract'] = 'DRY の写し（層の添字・等方の本数・生成の上限・下見の (i)(ii) の門だけを小さな模型に合わせた・模型の事実は本物の値のまま）'
    return Cd


def PH_form_items(path, C, S):
    """抽出の記録の形の項目（正本 `computation.extraction_record.form_items`）のうち、器が機械で見られる欄（値は読まない）。戻り値: 落ちた項目の並び。"""
    if not os.path.exists(path):
        return ['公開した抽出の記録が無い']
    R = json.load(open(path, encoding='utf-8'))
    miss = [k for k in ('row_D', 'npz_sha256', 'coefficient', 'g_match', 'checks', 'start_record_sha256', 'time_utc', 'versions', 'weights_sha256') if k not in R]
    if not miss and not all(bool(v) for v in R['checks'].values()):
        miss.append('凍結した確かめの合否がすべて「通った」でない')
    if not miss and R['versions'] != S.get('versions'):
        miss.append('版のピンが文字列で一致しない')
    if not miss and R['weights_sha256'] != S.get('weights_sha256'):
        miss.append('重みの断片の SHA が合わない')
    return miss


if __name__ == '__main__':
    try:
        run()
    except SystemExit:
        raise
    except Exception:
        LOG.append({'step': 'crash', 'at': now(), 'traceback': traceback.format_exc()[-4000:]})
        package('crash', {'crash': traceback.format_exc()[-4000:]})
        say('[boot_bprime] 予期しない誤りで止まった（器の誤りではない・登録者に相談）')
        raise
```

### 10. `tools/analyze_Bprime.py`（集計（一致の判定））

- 出所: 作業の置き場 `tools/analyze_Bprime.py`・SHA16 CD88EAE2A592E8FF・31799 字

```python
# -*- coding: utf-8 -*-
"""analyze_Bprime.py v0（2026-09-30・B′ の集計の器・層三の `tools/analyze_Bl3.py` v4 を B′ の正本に移したもの・コーディネータ南無弥勒如来）。

入力: 本の計算の出力（升目と符号ごとの効き目・質量・層ごとの差分）・下見の記録（本の凍結で凍結したもの）・独立の再計算の二つの道の出力と独立の再抽出の出力・
      道の違いの記述の出力（本の計算がバッチ一に移ったときだけ）・抽出の記録・行動の下見の閉じた記録・正本。重みは読まない。**読みは付けない**
      （読みの型の当てはめと文は報告の組み立ての器が正本の読みの表から行う）。
計算（正本のとおり・層三の凍結の芯 `bl3_core` と B-lens の凍結の芯 `blens_core` を呼ぶ）:
  - 主の札: 行ごとの割合と裾の本数（等方の帰無・同じ升目と符号）・Holm（下見で外した升目の行を除いた数）・効き目の側・二つ目の札（中心・最上位・二つの順位）・等方の最上位の割合。
  - 予想の答え（q1〜q4・q5〜q7 は欠番）・偶然の目安の数え直し・独立の再計算の二段の一致（二段目の許容は正本 `independent_recompute.stages.second` の鍵）・独立の再抽出の一致。
  - 記述: 質量が `pilot.mass_min` を下回った方向の数と割合（名前のある方向・等方・実在の差に分けて）・升目ごとの無操作の選択肢 a の文字の確率・等方の張り付きの量・
    等方の効き目の広がり（四分位の幅・95% の中央の区間の幅・標準偏差・中央値）と、実在の差の方向の四分位の幅で割った値・道の違いの記述（札の違う行の数と効き目の差の最大）。
層三の門・乙・q5〜q7 は B′ に無い（正本 `gate.status`・`predictions.missing`）。手元の二つの段（一致だけを見る／結果を開く）は層三の型（凍結と封印の記録の錨・組の SHA・環境）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, math, hashlib, subprocess, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G          # 凍結の器の置き場を sys.path に足す
import bl3_core as K
import bprime_core as P

VERSION = 'v0.3'        # v0.3（2026-09-30）: 手元の二つの段の口で、DRY の出力だけ等方の本数を抽出の記録の名の数に合わせた正本の写しで集計する（起動器の DRY の写しは等方の本数を減らすので、正本の本数では鍵が足りずに止まった・Colab の合成データの確かめで見つけた・K21）。前の版は `prev/analyze_Bprime-v0.2.py`／v0.2（2026-09-30）: 手元の二つの段の口（judge・open）を足した・抽出の記録の組の名から方向の名を作る／v0.1: 結果を開く段の出力に独立の再抽出の一致（`reextract`）を足した（報告の組み立ての器が読むのに書いていなかった・掃き出しの器を書いて見つけた）。前の版は `prev/analyze_Bprime-v0.py`
key3 = lambda sc, base, sg: '%s|%s|%+d' % (sc, base, int(sg))
RECS = os.path.join(ROOT, 'records', 'Bprime')
PARTS_MAIN = ('main', 'pathdiff')
PARTS_RC = ('hook', 'rewrite', 'reextract')
STRICT_ENV = ('commit', 'dry', 'canon_sha16', 'directions_npz_sha256')


# ---------------- 主の札 ----------------
def row_labels(C, main_rows, eff, pair_names, dropped_cells=(), p_override=None):
    """主の行の札（層三の `analyze_Bl3.row_labels` と同じ決まり）。eff: 升目と符号の鍵 → {方向の名: 効き目}。p_override: 行の名 → 効き目の組（独立の再計算で置き換えるとき）。"""
    swaps = C['nulls']['real']['swap_siblings']
    alpha = C['labels']['iso_outside']['holm_alpha']
    n_iso = C['nulls']['isotropic']['count']
    out, pv = collections.OrderedDict(), {}
    rows = [r for r in main_rows if '%s|%s' % (r['scenario'], r['base']) not in set(dropped_cells)]
    for r in rows:
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        if p_override and r['id'] in p_override:
            e, iso = p_override[r['id']]['effect'], p_override[r['id']]['iso']
            same, opp = p_override[r['id']]['comps_same'], p_override[r['id']]['comps_opp']
        else:
            e = eff[k][r['direction']]
            iso = [eff[k]['iso:%d' % i] for i in range(n_iso)]
            comps = K.comparators_for(r['direction'], pair_names, swaps)
            same, opp = [eff[k]['real:' + p] for p in comps], [eff[kk]['real:' + p] for p in comps]
        pt = K.p_and_tail(e, iso)
        sl = K.second_label(e, list(same) + list(opp), list(zip(same, opp)))
        out[r['id']] = {'direction': r['direction'], 'cell_sign': k, 'effect': e, 'p': pt['p'], 'upper': pt['upper'], 'lower': pt['lower'], 'tail': pt['tail'],
                        'iso_median': float(np.median(iso)), 'second': sl, 'iso_top_share': K.iso_top_share(iso, sl['center'], list(same) + list(opp)), '_iso': iso}
        pv[r['id']] = pt['p']
    H = K.holm(pv, alpha)
    for rid, o in out.items():
        o['holm_step'], o['iso_outside'] = H[rid]['step'], bool(H[rid]['pass'])
        o['side'] = K.effect_side(o['effect'], o.pop('_iso'))
    return out, {'m_rows': len(rows), 'dropped_rows': [r['id'] for r in main_rows if r not in rows]}


def labels_signature(lab):
    """札の一致で見る中身（正本 `independent_recompute.agreement`）: Holm の判定・等方の外の行の割合を決めた裾・等方の外の行の効き目の側・二つ目の札。"""
    return {rid: (o['iso_outside'], o['tail'] if o['iso_outside'] else None, (o['side'] or {}).get('side') if o['iso_outside'] else None,
                  (o['side'] or {}).get('sign') if o['iso_outside'] else None, o['second']['top']) for rid, o in lab.items()}


# ---------------- 予想の答え ----------------
def prediction_truth(C, pilot_attempts, lab):
    q1 = K.q1_from_attempts(pilot_attempts)
    stopped = (not q1['scored']) or q1['q1'] == '止める'
    items = {it['key']: it for it in C['predictions']['items']}
    tr = collections.OrderedDict()
    tr['q1.pilot'] = q1['q1'] if q1['scored'] else None
    if stopped:
        for k in list(items)[1:]:
            tr[k] = None
        return tr, {'stopped': True, 'q1': q1}
    tr['q2.vhat_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'static' and o['iso_outside']), items['q2.vhat_iso']['options'])
    tr['q3.nk_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'Nk' and o['iso_outside']), items['q3.nk_iso']['options'])
    tr['q4.second'] = K.bucket(sum(1 for o in lab.values() if o['second']['top']), items['q4.second']['options'])
    return tr, {'stopped': False, 'q1': q1}


def chance_after_drop(C, lab):
    """二つ目の札の偶然の目安を、下見で外した後の行で数え直す（正本 `pilot.decision_more.drop_effects`）。分母（方向ごとの行の数）も返す。"""
    co, cp = C['nulls']['real']['comparators_oriented'], C['nulls']['real']['comparators']
    by = collections.Counter(o['direction'] for o in lab.values())
    return {'oriented': round(sum(n / (co[d] + 1) for d, n in by.items()), 4), 'pair': round(sum(n / (cp[d] + 1) for d, n in by.items()), 4), 'rows_by_direction': dict(by),
            'canon_all_rows': {'oriented': C['nulls']['real']['chance_second'], 'pair': C['nulls']['real']['chance_second_pair']}}


# ---------------- 独立の再計算の一致 ----------------
def tol_second(C, floor):
    """二段目の許容（正本 `independent_recompute.stages.second`: 揺れの床の factor 倍と floor の大きい方・上限 `pilot.noise_max`・それに揺れの床を足す）。"""
    S = C['independent_recompute']['stages']['second']
    return K.cache_tol(floor, S['factor'], S['floor'], C['pilot']['noise_max']) + floor


def recompute_agreement(C, main_rows, eff_main, pair_names, hook, rewrite, pilot, dropped_cells=(), rows_subset=None):
    """二段の一致（正本 `independent_recompute.stages`・`agreement`）。hook と rewrite: 行の名 → {'noop_lo','effects': {'方向|符号': 効き目}}。v̂ の行（Nk の行を入れるかは案 16 の決め）。"""
    drop = set(dropped_cells)
    in_drop = lambda r: '%s|%s' % (r['scenario'], r['base']) in drop
    comps_of = lambda d: K.comparators_for(d, pair_names, C['nulls']['real']['swap_siblings'])
    nf = ['main:%s' % k for k, e in eff_main.items() if not all(math.isfinite(float(v)) for v in e.values())]
    for nm_, pth_ in (('hook', hook), ('rewrite', rewrite)):
        for rid_, o_ in (pth_ or {}).items():
            if not all(math.isfinite(float(v)) for v in [o_.get('noop_lo', 0.0)] + list((o_.get('effects') or {}).values())):
                nf.append('%s:%s' % (nm_, rid_))
    if nf:
        s2 = {'agree': False, 'labels_same': False, 'values_within_tol': False, 'reason': 'non_finite', 'non_finite': nf[:10]}
        f1 = None if rewrite is None else {'agree': False, 'reason': 'non_finite', 'non_finite': nf[:10]}
        return {'second': s2, 'tol_second': None, 'first': f1, 'tol_first': C['independent_recompute']['tol_stage1'], 'agree': False, 'reason': 'non_finite', 'non_finite': nf[:10]}
    n_iso = C['nulls']['isotropic']['count']

    def use(r):
        return r['direction'] == 'static' and not in_drop(r) and (rows_subset is None or r['id'] in rows_subset)

    def override(path):
        ov = {}
        for r in main_rows:
            if not use(r) or r['id'] not in path:
                continue
            E = path[r['id']]['effects']
            s = r['sign']
            ov[r['id']] = {'effect': E['static|%+d' % s], 'iso': [E['iso:%d|%+d' % (i, s)] for i in range(n_iso)],
                           'comps_same': [E['real:%s|%+d' % (p, s)] for p in comps_of('static')], 'comps_opp': [E['real:%s|%+d' % (p, -s)] for p in comps_of('static')]}
        return ov

    def as_eff(ov):
        return {rid: [o['effect']] + list(o['iso']) + list(o['comps_same']) + list(o['comps_opp']) for rid, o in ov.items()}

    def with_noop(ov, path):
        return {rid: [path[rid]['noop_lo']] + v for rid, v in as_eff(ov).items()}
    main_ov = {}
    for r in main_rows:
        if not use(r):
            continue
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        main_ov[r['id']] = {'effect': eff_main[k]['static'], 'iso': [eff_main[k]['iso:%d' % i] for i in range(n_iso)],
                            'comps_same': [eff_main[k]['real:' + p] for p in comps_of('static')], 'comps_opp': [eff_main[kk]['real:' + p] for p in comps_of('static')]}
    sig = lambda ov: labels_signature(row_labels(C, main_rows, eff_main, pair_names, dropped_cells, p_override=ov)[0])
    hk, rw = override(hook), (override(rewrite) if rewrite is not None else None)
    t2 = tol_second(C, pilot['floor'])
    s2 = K.agreement(as_eff(main_ov), as_eff(hk), t2, sig(main_ov), sig(hk))
    s2 = dict(s2, agree=bool(s2['labels_same']), values_beyond_tol=not s2['values_within_tol'])
    out = {'second': s2, 'tol_second': t2, 'second_formal': int(pilot['batch']) == 1}
    out['first'] = None if rw is None else K.agreement(with_noop(hk, hook), with_noop(rw, rewrite), C['independent_recompute']['tol_stage1'], sig(hk), sig(rw))
    out['tol_first'] = C['independent_recompute']['tol_stage1']
    out['agree'] = bool(out['second']['agree'] and (out['first'] or {}).get('agree', False))
    return out


def reextract_agreement(C, EX, RX):
    """独立の再抽出の一致（正本 `independent_recompute.reextract`）: ‖h‖ と ‖v̂‖ の相対の差が `rel_tol` 以内・名前のある方向の余弦が `cos_min` 以上。
    EX: 抽出の記録（転記行 D の値）・RX: 再抽出の道の出力 {'h_norm_by_context': …, 'vhat_norm': …, 'named_cos': {名: 余弦}}。値は開かない（一致か不一致かだけ）。"""
    R = C['independent_recompute']['reextract']
    hn = EX['row_D']['h_norm_by_context']
    rel_h = max(abs(float(RX['h_norm_by_context'][k]) - float(v)) / float(v) for k, v in hn.items())
    rel_v = abs(float(RX['vhat_norm']) - float(EX['vhat_norm'])) / float(EX['vhat_norm'])
    cos = min(float(x) for x in RX['named_cos'].values())
    same_keys = sorted(RX['h_norm_by_context']) == sorted(hn) and sorted(RX['named_cos']) == sorted(C['directions']['named'])
    return {'agree': bool(same_keys and rel_h <= R['rel_tol'] and rel_v <= R['rel_tol'] and cos >= R['cos_min']), 'keys_same': same_keys,
            'rel_h_max': rel_h, 'rel_v': rel_v, 'cos_min': cos}


# ---------------- 記述 ----------------
def descriptive(C, main_out, names):
    mm = C['pilot']['mass_min']
    groups = {'named': set(names['named']), 'iso': set(names['iso']), 'real': set(names['real'])}
    mass = collections.OrderedDict()
    for k, o in main_out.items():
        m = {}
        for g, s in groups.items():
            vals = [v for d, v in o['mass'].items() if d in s]
            n_below = sum(1 for v in vals if v < mm)
            m[g] = {'below': n_below, 'n': len(vals), 'share': (n_below / len(vals)) if vals else None}
        mass[k] = m
    ties, spread = collections.OrderedDict(), collections.OrderedDict()
    for k, o in main_out.items():
        iso = np.array([v for d, v in o['effects'].items() if d.startswith('iso:')], dtype=np.float64)
        real = np.array([v for d, v in o['effects'].items() if d.startswith('real:')], dtype=np.float64)
        if iso.size:
            u, c = np.unique(iso, return_counts=True)
            ties[k] = float(c[c > 1].sum() / iso.size)
            q1, q3 = np.percentile(iso, 25), np.percentile(iso, 75)
            lo, hi = np.percentile(iso, 2.5), np.percentile(iso, 97.5)
            iqr_real = float(np.percentile(real, 75) - np.percentile(real, 25)) if real.size else None
            spread[k] = {'iqr': float(q3 - q1), 'central95': float(hi - lo), 'std': float(np.std(iso)), 'median': float(np.median(iso)), 'iqr_real': iqr_real,
                         'iqr_over_real': (float(q3 - q1) / iqr_real) if iqr_real else None}
    pa = {k: o['pa_noop'] for k, o in main_out.items()}
    return {'mass_below_min': mass, 'pa_noop': pa, 'iso_ties_share': ties, 'iso_spread': spread}


def path_difference(C, main_out, pd_out, pair_names, dropped_cells=()):
    """道の違いの記述（正本 `descriptive.path_difference`）: バッチ一の本の計算とバッチ 16 の道の札の違う行の数と効き目の差の最大（止める条件にせず、本の札も変えない）。"""
    eff_a = {k: o['effects'] for k, o in main_out.items()}
    eff_b = {k: o['effects'] for k, o in pd_out.items()}
    if sorted(eff_a) != sorted(eff_b) or any(sorted(eff_a[k]) != sorted(eff_b[k]) for k in eff_a):
        return {'comparable': False}
    la = labels_signature(row_labels(C, C['main_rows'], eff_a, pair_names, dropped_cells)[0])
    lb = labels_signature(row_labels(C, C['main_rows'], eff_b, pair_names, dropped_cells)[0])
    dmax = max(abs(float(eff_a[k][d]) - float(eff_b[k][d])) for k in eff_a for d in eff_a[k])
    return {'comparable': True, 'rows_label_differs': sorted(r for r in la if la[r] != lb[r]), 'n_rows_label_differs': sum(1 for r in la if la[r] != lb[r]), 'max_abs_diff': dmax}


def analyze(C, main_out, pilot_attempts, pair_names, names, hook=None, rewrite=None, rows_subset=None):
    """集計の全体（読みは付けない）。main_out: 升目と符号の鍵 → run_cell_sign の出力。pilot_attempts: 下見の試みの並び（最後が本の凍結の下見）。"""
    pilot = pilot_attempts[-1]
    dropped = (pilot.get('decision') or {}).get('dropped', [])
    nf = sorted({k for k, o in main_out.items() for d, v in list((o.get('effects') or {}).items()) + list((o.get('mass') or {}).items()) if not math.isfinite(float(v))})
    if nf:
        raise SystemExit('有限でない効き目か質量がある（止める）: %s' % nf[:5])
    eff = {k: o['effects'] for k, o in main_out.items()}
    lab, meta = row_labels(C, C['main_rows'], eff, pair_names, dropped)
    meta['floor'] = floor_marks(C, main_out, pilot, lab)
    truth, tmeta = prediction_truth(C, pilot_attempts, lab)
    out = collections.OrderedDict(version=VERSION, rows=lab, rows_meta=meta, predictions_truth=truth, predictions_meta=tmeta,
                                  descriptive=descriptive(C, main_out, names), chance=chance_after_drop(C, lab),
                                  summary_numbers=P.summary_numbers(summary_rows(C, lab)) if not tmeta['stopped'] else None)
    if hook is not None:
        out['recompute'] = recompute_agreement(C, C['main_rows'], eff, pair_names, hook, rewrite, pilot, dropped, rows_subset)
    return out


def floor_marks(C, main_out, pilot, lab):
    """床の余白の印（正本 `floor_margin`）: 行の升目の、本の計算の無操作の対数オッズの床と天井からの余白の近い方が、〈その升目の (vi) の (a) の値と、
    (vi) の (b) の升目の間の最大の、大きい方〉より小さいとき印。行は外さず、Holm は印の前の行で一度だけ掛けたまま（印で掛け直さない）。行の札に 'floor_mark' を足す。"""
    vi = pilot['vi']
    vb = max(float(v) for v in vi['b'].values())
    for rid, o in lab.items():
        cell = o['cell_sign'].rsplit('|', 1)[0]
        o['floor_mark'] = P.floor_mark(main_out[o['cell_sign']]['lo'][K.NOOP], C['pilot']['p_bounds'], vi['a'][cell], vb)
    return {'vi_a_max': max(float(v) for v in vi['a'].values()), 'vi_b_max': vb}


def summary_rows(C, lab):
    """要約の型の数（正本 `reading.summary`・`bprime_core.summary_numbers` に渡す行）: 方向・等方の外・二つ目の札・床の余白の印・効き目の側（等方の外の行だけ）。"""
    return [{'id': rid, 'direction': o['direction'], 'iso_outside': o['iso_outside'], 'second': o['second']['top'], 'mark': o['floor_mark']['mark'],
             'side': (o['side'] or {}).get('side') if o['iso_outside'] else None} for rid, o in lab.items()]


# ---------------- 手元の二つの段（一致だけを見る・結果を開く） ----------------
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
canon_sha16 = lambda obj: hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest().upper()[:16]
fr_core = lambda FR: {k: v for k, v in FR.items() if k != 'deviations'}


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


def load_outputs(dirs):
    """起動器の相 main と相 recompute の出力（組ごとの JSON・end の記録・session.json）を読む。同じ組が二つあれば止める。組の JSON の SHA-256 を end の記録と照らす。"""
    parts, sessions, files = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
    for d in dirs:
        S = json.load(open(os.path.join(d, 'session.json'), encoding='utf-8'))
        ends = glob.glob(os.path.join(d, 'end-*.json'))
        if len(ends) != 1:
            raise SystemExit('出力の置き場に end の記録がちょうど一つでない: %s' % d)
        E = json.load(open(ends[0], encoding='utf-8'))
        for fn, want in E['outputs_sha256'].items():
            m = re.fullmatch(r'(main|recompute)-(\w+)\.json', fn)
            if not m:
                continue
            part = m.group(2)
            if part in parts:
                raise SystemExit('同じ組が二つの置き場にある（止める）: %s' % part)
            p = os.path.join(d, fn)
            got = sha256f(p)
            if got != want:
                raise SystemExit('組 %s の出力の SHA-256 が end の記録と違う（止める）' % part)
            parts[part] = json.load(open(p, encoding='utf-8'))
            sessions[part] = S
            files[part] = {'dir': os.path.basename(os.path.normpath(d)), 'json_sha256': got, 'session_sha256': sha256f(os.path.join(d, 'session.json')), 'end_sha256': sha256f(ends[0])}
    return parts, sessions, files


def env_same(sessions):
    keys = ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism')
    ref = next(iter(sessions.values())) if sessions else {}
    diff = {k: {p: s.get(k) for p, s in sessions.items()} for k in keys if any(s.get(k) != ref.get(k) for s in sessions.values())}
    return {'same': not diff, 'diff': diff, 'strict': [k for k in diff if k in STRICT_ENV]}


def dry_view(C, names):
    """DRY の出力だけに使う正本の写し（v0.3・K21）: 等方の本数を抽出の記録の等方の名の数（起動器の DRY の写しの本数）に合わせる。ほかの鍵は変えない。"""
    Cd = json.loads(json.dumps(C, ensure_ascii=False))
    Cd['nulls']['isotropic']['count'] = len(names['iso'])
    return Cd


def judge(C, parts, sessions, pilot_attempts, pair_names, EX, files=None, FR=None):
    """一致だけを見る段: 器の誤りの有無・組の環境・二段の一致と独立の再抽出の一致か不一致かだけを返す（効き目の値と差の最大は返さない）。"""
    out = collections.OrderedDict(parts=list(parts), tool_error={p: bool(v.get('tool_error')) for p, v in parts.items()}, env=env_same(sessions))
    dry = any(bool(s.get('dry')) for s in sessions.values())
    out['dry'] = dry
    out['inputs'] = files
    if FR is not None:
        devs_ = FR.get('deviations') or []
        out['freeze_record_core_sha16'] = canon_sha16(fr_core(FR))
        out['deviations_n'] = len(devs_)
        out['deviations_sha16'] = canon_sha16(devs_)
    stop = lambda why: (out.update(first=None, second=None, reextract=None, agree=None, reason=why), out)[1]
    need = {'main', 'hook', 'rewrite', 'reextract'}
    if any(out['tool_error'].values()) or not need <= set(parts):
        return stop('器の誤りか、組の欠け（%s）' % sorted(need - set(parts)))
    if out['env']['strict']:
        return stop('組の間の環境が違う: %s' % out['env']['strict'])
    pilot = pilot_attempts[-1]
    if not dry:
        if FR is None:
            return stop('DRY でないのに凍結の記録が無い')
        mf = FR.get('main_freeze') or {}
        if (mf.get('pilot') or {}) != pilot:
            return stop('本の凍結の下見の記録と、集計に渡した下見の記録が違う')
        n_can = C['nulls']['isotropic']['count']
        n_main = {k: sum(1 for d in o['effects'] if d.startswith('iso:')) for k, o in parts['main']['result']['cells'].items()}
        if any(v not in (n_can,) for k, v in n_main.items() if parts['main']['result']['cells'][k]['effects'].get('static') is not None):
            return stop('DRY でないのに等方の本数が正本と違う')
    eff = {k: o['effects'] for k, o in parts['main']['result']['cells'].items()}
    hook = parts['hook']['result']['hook']
    rewrite = parts['rewrite']['result']
    ag = recompute_agreement(C, C['main_rows'], eff, pair_names, hook, rewrite, pilot, (pilot.get('decision') or {}).get('dropped', []), rows_subset=set(hook) if dry else None)
    rx = reextract_agreement(C, EX, parts['reextract']['result'])
    out.update(first=None if ag['first'] is None else bool(ag['first']['agree']), second=bool(ag['second']['agree']), reextract=bool(rx['agree']),
               agree=bool(ag['agree'] and rx['agree']), second_values_within_tol=bool(ag['second']['values_within_tol']),
               reason=None if (ag['agree'] and rx['agree']) else ('独立の再抽出が一致しない' if not rx['agree'] else ('一段目の道が無い' if ag['first'] is None else '二段のどちらかが一致しない')))
    return out


def open_results(C, parts, sessions, pilot_attempts, pair_names, names, closed):
    """結果を開く段（登録者と一緒に・一致だけを見る段が一致したとき）: 集計の全体と、報告に並べるもの（下見の記録・頭の確かめ・層ごとの差分・道の違い・行動の下見・環境）。"""
    rc = {'hook': parts['hook']['result']['hook'], 'rewrite': parts['rewrite']['result']}
    dry = any(bool(s.get('dry')) for s in sessions.values())
    A = analyze(C, parts['main']['result']['cells'], pilot_attempts, pair_names, names, hook=rc['hook'], rewrite=rc['rewrite'], rows_subset=set(rc['hook']) if dry else None)
    pil = pilot_attempts[-1]
    if 'pathdiff' in parts:
        A['path_difference'] = path_difference(C, parts['main']['result']['cells'], parts['pathdiff']['result']['cells'], pair_names, (pil.get('decision') or {}).get('dropped', []))
    A['dry'] = dry
    A['pilot_attempts'] = pilot_attempts
    A['head'] = parts['main']['result']['head']
    A['main_run'] = {k: parts['main']['result'].get(k) for k in ('batch', 'dropped')}
    A['layerwise'] = {k: o['layers'] for k, o in parts['main']['result']['cells'].items()}
    A['behavior'] = {'summaries': closed.get('summaries'), 'row_C': closed.get('row_C'), 'external': closed.get('external')}
    A['sessions'] = {p: {k: s.get(k) for k in ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism', 'packaged_at')} for p, s in sessions.items()}
    A['env'] = env_same(sessions)
    A['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
    return A


def open_checked(C, parts, sessions, files, J, pilot_attempts, pair_names, names, EX, closed, FR=None, judge_sha16=None):
    """結果を開く段の確かめ（層三の型）: 一致だけを見る段の記録が一致で、読む出力の同定が同じで、凍結の記録の台帳の外が判定の時と同じ・台帳の頭が同じ。
    同じ入力で一致だけを見る段をもう一度走らせ、判定の記録と同じこと。開いた集計の一致が判定と違えば止める。"""
    if not J.get('agree'):
        raise SystemExit('一致だけを見る段の記録が一致していない（結果を開かない）')
    if J.get('inputs') != files:
        raise SystemExit('結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）')
    dry = any(bool(s.get('dry')) for s in sessions.values())
    if not dry:
        if FR is None:
            raise SystemExit('DRY でないのに凍結の記録が無い（開かない）')
        devs_ = FR.get('deviations') or []
        n_ = J.get('deviations_n')
        if canon_sha16(fr_core(FR)) != J.get('freeze_record_core_sha16'):
            raise SystemExit('凍結の記録（台帳の外）が一致だけを見る段の後に変わった（開かない）')
        if n_ is None or len(devs_) < n_ or canon_sha16(devs_[:n_]) != J.get('deviations_sha16'):
            raise SystemExit('凍結の記録の台帳の、一致だけを見る段の時の行が変わった（開かない）')
    J2 = json.loads(json.dumps(judge(C, parts, sessions, pilot_attempts, pair_names, EX, files, FR), ensure_ascii=False, default=float))
    skip_ = ('written_utc', 'clause', 'deviations_n', 'deviations_sha16')
    diff_ = sorted(k for k in set(J) | set(J2) if k not in skip_ and J.get(k) != J2.get(k))
    if diff_:
        raise SystemExit('一致だけを見る段を同じ入力でもう一度走らせた答えが、判定の記録と違う（開かない）: %s' % diff_)
    A = open_results(C, parts, sessions, pilot_attempts, pair_names, names, closed)
    rc = A.get('recompute') or {}
    got = (None if rc.get('first') is None else bool(rc['first']['agree']), bool((rc.get('second') or {}).get('agree')))
    if got != (J.get('first'), J.get('second')):
        raise SystemExit('開いた集計の二段の一致が、一致だけを見る段と違う（書かない）')
    rx = reextract_agreement(C, EX, parts['reextract']['result'])
    if bool(rx['agree']) != J.get('reextract'):
        raise SystemExit('開いた独立の再抽出の一致が、一致だけを見る段と違う（書かない）')
    A['reextract'] = rx                                                   # 報告の組み立ての器が読む（v0.1・掃き出しで見つけた欠け）
    A['inputs'] = files
    A['judge_record_sha16'] = judge_sha16
    return A


def _selftest():
    """合成の効き目で、札・予想の答え・二段の一致・記述・道の違いを通す（等方を減らした正本の写し）。"""
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    Cs = json.loads(json.dumps(C))
    n_iso = 999                                            # 等方の本数を減らしても、割合の最小（2 ÷ 1000）が Holm の一段目（0.05 ÷ 16）を下回る数
    Cs['nulls']['isotropic']['count'] = n_iso
    rng = np.random.default_rng(3)
    pairs = []
    arms = C['nulls']['real']['arms']
    for i in range(len(arms)):
        for j in range(i + 1, len(arms)):
            pairs.append('%s~%s' % (arms[i], arms[j]))
    names = {'named': list(C['directions']['named']), 'iso': ['iso:%d' % i for i in range(n_iso)], 'real': ['real:' + p for p in pairs]}
    main_out = collections.OrderedDict()
    cs = [(sc, b, g) for sc, b, g in C['cell_signs_main']]
    rev = [(sc, b, -g) for sc, b, g in cs if (sc, b, -g) not in cs]
    for sc, b, g in cs + rev:
        k = key3(sc, b, g)
        eff = {d: float(rng.normal(0, 0.1)) for d in names['iso'] + names['real']}
        if (sc, b, g) in cs:
            eff.update({d: float(rng.normal(0, 0.1)) for d in names['named']})
            if b == 'O-Ncold' and g == -1:
                eff['static'] = 5.0                        # 等方の外になる行（合成）
        mass = {d: 0.95 for d in eff}
        mass[names['iso'][0]] = 0.5
        main_out[k] = {'effects': eff, 'mass': mass, 'pa_noop': 0.4, 'lo': {K.NOOP: (9.2 if sc == 'SK' else 0.0)}}
    cells = sorted({'%s|%s' % (sc, b) for sc, b, _ in cs})
    pilot = {'decision': {'q1': '続ける', 'dropped': []}, 'batch': 16, 'floor': 0.001,
             'vi': {'a': {c: (0.05 if c.startswith('SK|') else 0.002) for c in cells}, 'b': {c: 0.001 for c in cells}}}
    A = analyze(Cs, main_out, [pilot], pairs, names)
    n_out = sum(1 for o in A['rows'].values() if o['iso_outside'])
    assert A['rows_meta']['m_rows'] == len(C['main_rows']) and n_out >= 1, (A['rows_meta'], n_out)
    marks = {rid: o['floor_mark']['mark'] for rid, o in A['rows'].items()}
    # SK の升目は天井の近く（logit(0.9999) ≒ 9.2102・余白 ≒ 0.0102 が (a) の 0.05 より小さい → 印）・ほかの升目は余白 ≒ 9.21 で印なし
    assert all(marks[rid] == (A['rows'][rid]['cell_sign'].startswith('SK|')) for rid in marks), marks
    assert A['summary_numbers']['n'] == len(C['main_rows']) and A['summary_numbers']['k'] == n_out
    assert A['predictions_truth']['q1.pilot'] == '続ける' and A['predictions_truth']['q2.vhat_iso'] in ('一から三', '四以上')
    assert A['descriptive']['mass_below_min'][key3(*cs[0])]['iso']['below'] == 1
    stop_tr, _ = prediction_truth(Cs, [dict(pilot, decision={'q1': '止める', 'dropped': []})], A['rows'])
    assert stop_tr['q1.pilot'] == '止める' and stop_tr['q2.vhat_iso'] is None
    hook = collections.OrderedDict()
    for r in C['main_rows']:
        if r['direction'] != 'static':
            continue
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        s = r['sign']
        comps = K.comparators_for('static', pairs, C['nulls']['real']['swap_siblings'])
        E = {'static|%+d' % s: main_out[k]['effects']['static']}
        E.update({'iso:%d|%+d' % (i, s): main_out[k]['effects']['iso:%d' % i] for i in range(n_iso)})
        E.update({'real:%s|%+d' % (p, s): main_out[k]['effects']['real:' + p] for p in comps})
        E.update({'real:%s|%+d' % (p, -s): main_out[kk]['effects']['real:' + p] for p in comps})
        hook[r['id']] = {'noop_lo': 0.0, 'effects': E}
    ag = recompute_agreement(Cs, C['main_rows'], {k: o['effects'] for k, o in main_out.items()}, pairs, hook, hook, pilot)
    assert ag['agree'] and ag['first']['agree'] and ag['second']['agree'], ag
    bad = json.loads(json.dumps(hook))
    rid0 = next(iter(bad))
    bad[rid0]['effects'][next(iter(bad[rid0]['effects']))] += 1.0
    ag2 = recompute_agreement(Cs, C['main_rows'], {k: o['effects'] for k, o in main_out.items()}, pairs, hook, bad, pilot)
    assert not ag2['first']['agree'], ag2
    pd = path_difference(Cs, main_out, main_out, pairs)
    assert pd['comparable'] and pd['n_rows_label_differs'] == 0 and pd['max_abs_diff'] == 0.0
    print('analyze_Bprime.py %s SELFTEST PASS（主の行 %d・等方の外 %d・二段の一致・壊した一段目の不一致・道の違い 0）' % (VERSION, A['rows_meta']['m_rows'], n_out))


def names_of(EX):
    """抽出の記録の組の名から方向の名（名前のある方向・等方・実在の差）と実在の差の対の名を作る（npz は読まない）。"""
    G_ = EX['groups']
    names = {'named': list(G_['named']['names']), 'iso': ['iso:%d' % i for i in range(int(G_['iso']['count']))], 'real': ['real:' + p for p in G_['real']['names']]}
    return names, [n[len('real:'):] for n in names['real']]


def cli(argv):
    """手元の二つの段の口（v0.2）: judge（一致だけを見る段・値を印字しない）と open（結果を開く段・登録者と一緒に）。
    DRY の出力は `--pilot <下見の記録の JSON>` で下見の記録を与える。DRY でない出力は `--freeze <凍結の記録>` の本の凍結の下見の試みを使う。"""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['judge', 'open'])
    ap.add_argument('--dirs', nargs='+', required=True, help='相 main と相 recompute の出力の置き場')
    ap.add_argument('--extract', required=True, help='抽出の記録（extraction-record-Bprime.json）')
    ap.add_argument('--pilot', help='DRY のときの下見の記録（pilot-Bprime.json）')
    ap.add_argument('--freeze', help='凍結の記録（DRY でないとき）')
    ap.add_argument('--judge', help='open のとき: 一致だけを見る段の記録')
    ap.add_argument('--closed', help='open のとき: 行動の下見の閉じた記録')
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    parts, sessions, files = load_outputs(a.dirs)
    EX = json.load(open(a.extract, encoding='utf-8'))
    names, pair_names = names_of(EX)
    if sessions and all(bool(s.get('dry')) for s in sessions.values()):
        C = dry_view(C, names)                     # DRY の出力だけ: 等方の本数を抽出の記録に合わせる（v0.3・K21・DRY でない出力は正本のまま）
    FR = json.load(open(a.freeze, encoding='utf-8')) if a.freeze else None
    if FR is not None:
        atts = (FR.get('main_freeze') or {}).get('pilot_attempts')
        if not atts:
            raise SystemExit('凍結の記録に本の凍結の下見の試みが無い')
    elif a.pilot:
        atts = [json.load(open(a.pilot, encoding='utf-8'))]
    else:
        raise SystemExit('--freeze か（DRY のとき）--pilot が要る')
    if os.path.exists(a.out):
        raise SystemExit('既にある（一度だけ書く）: %s' % a.out)
    if a.stage == 'judge':
        J = json.loads(json.dumps(judge(C, parts, sessions, atts, pair_names, EX, files, FR), ensure_ascii=False, default=float))
        J['written_utc'] = datetime_utc()
        J['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
        with open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(J, fh, ensure_ascii=False, indent=1)
        print('[analyze_Bprime] 一致だけを見る段: 一致 %s（一段目 %s・二段目 %s・再抽出 %s）・理由 %s' % (J.get('agree'), J.get('first'), J.get('second'), J.get('reextract'), J.get('reason')))
        return J
    if not (a.judge and a.closed):
        raise SystemExit('open には --judge と --closed が要る')
    J = json.load(open(a.judge, encoding='utf-8'))
    closed = json.load(open(a.closed, encoding='utf-8'))
    A = open_checked(C, parts, sessions, files, J, atts, pair_names, names, EX, closed, FR=FR, judge_sha16=sha16f(a.judge))
    with open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(A, fh, ensure_ascii=False, indent=1, default=float)
    print('[analyze_Bprime] 結果を開く段: 書いた %s（SHA16 %s）' % (os.path.basename(a.out), sha16f(a.out)))
    return A


def datetime_utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] in ('judge', 'open'):
        sys.stdout.reconfigure(encoding='utf-8')
        cli(sys.argv[1:]); sys.exit(0)
    print(__doc__)
```

### 11. 凍結の芯 `bl3_core.py` の関わる関数（p_and_tail・holm・comparators_for・cache_tol・agreement・recompute_set）

- 出所: 公開の置き場の決めた版 `0a456884810681127b6b051da76cd3913cd14f59` の `tools/bl3_core.py`（全体の SHA16 E8CD3A24950F8581）・SHA16 DD076B4DDD9495C1・3370 字

```python
# ---- p_and_tail（元の行 58〜65） ----
def p_and_tail(m, null):
    """両側に等しい裾の割合（`blens_core.p_equal_tailed`）と、上の裾と下の裾の本数・割合を決めた裾（上・下・同じ）。"""
    null = np.asarray(null, dtype=np.float64)
    if not (np.isfinite(m) and np.all(np.isfinite(null))):
        raise ValueError('有限でない値に割合と裾を当てようとした（裁定 D236）')
    up, lo = int(np.sum(null >= m)), int(np.sum(null <= m))
    tail = 'upper' if up < lo else ('lower' if lo < up else 'tie')
    return {'p': C.p_equal_tailed(m, null), 'upper': up, 'lower': lo, 'tail': tail, 'K': int(len(null))}
# ---- holm（元の行 68〜69） ----
def holm(pvals, alpha):
    return C.holm(pvals, alpha)
# ---- comparators_for（元の行 124〜136） ----
def comparators_for(direction, pair_names, swap_siblings):
    """比べる相手の対（正本 `nulls.real.rule`）: v̂ と (6b) は入れ替えの対（自分と兄弟）を除き、Nk と td は自分の対だけを除く。"""
    own = {'Nk': 'Nk~N', 'td': 'Onull~N'}
    if direction in ('static', 'loaded'):
        drop = set(swap_siblings)
    elif direction in own:
        drop = {own[direction]}
    else:
        raise ValueError('比べる相手を決められない方向: %s' % direction)
    missing = drop - set(pair_names)
    if missing:
        raise ValueError('除く対が対の名の並びに無い: %s' % sorted(missing))
    return [p for p in pair_names if p not in drop]
# ---- cache_tol（元の行 189〜191） ----
def cache_tol(floor, factor, lower, cap):
    """近道の許容（正本 `pilot.cache_tol_rule`）＝ 揺れの床の倍率倍と下限の大きい方を、上限で頭打ちにした値。"""
    return float(min(max(factor * floor, lower), cap))
# ---- agreement（元の行 245〜258） ----
def agreement(eff_a, eff_b, tol, labels_a, labels_b):
    """段ごとの一致（正本 `independent_recompute.agreement`）: 全ての効き目の差の絶対値が許容の内で、二つの道の値からそれぞれ出した札が同じ。
    有限でない値が一つでもあれば一致しない（鍵の順に依らない・`non_finite` に鍵を並べる・裁定 D236）。"""
    keys = sorted(eff_a)
    if sorted(eff_b) != keys:
        return {'agree': False, 'reason': 'keys', 'values_within_tol': False, 'labels_same': False, 'max_abs_diff': None,
                'missing': sorted(set(eff_a) ^ set(eff_b))}
    finite = lambda v: bool(np.all(np.isfinite(np.asarray(v, dtype=np.float64))))
    nf = [k for k in keys if not (finite(eff_a[k]) and finite(eff_b[k]))]
    if nf:
        return {'agree': False, 'reason': 'non_finite', 'values_within_tol': False, 'labels_same': False, 'max_abs_diff': None, 'non_finite': nf}
    dmax = max(float(np.max(np.abs(np.asarray(eff_a[k], dtype=np.float64) - np.asarray(eff_b[k], dtype=np.float64)))) for k in keys)
    same = labels_a == labels_b
    return {'agree': bool(dmax <= tol and same), 'values_within_tol': bool(dmax <= tol), 'labels_same': bool(same), 'max_abs_diff': dmax}
# ---- recompute_set（元の行 282〜294） ----
def recompute_set(main_rows, pair_names, swap_siblings, n_iso, dropped_cells=()):
    """独立の再計算で流す組（正本 `independent_recompute.what`）: v̂ の行ごとに、無操作・v̂・等方の帰無のすべて・比べる相手のすべて（両方の向き）。
    下見で外した升目の行は除く。戻り値: rows [(行の名, 升目の鍵, 符号)]・dirs_by_row {行の名: [(方向の名, 符号)]}。"""
    rows, dirs_by_row = [], collections.OrderedDict()
    comps = comparators_for('static', pair_names, swap_siblings)
    for r in main_rows:
        cell = '%s|%s' % (r['scenario'], r['base'])
        if r['direction'] != 'static' or cell in set(dropped_cells):
            continue
        s = int(r['sign'])
        rows.append((r['id'], cell, s))
        dirs_by_row[r['id']] = [('static', s)] + [('iso:%d' % i, s) for i in range(n_iso)] + [('real:' + p, s) for p in comps] + [('real:' + p, -s) for p in comps]
    return rows, dirs_by_row
```

### 12. transformers 5.16.1 の Gemma 4 の実装の抜き書き（Gemma4RMSNorm・Gemma4TextDecoderLayer・Gemma4TextScaledWordEmbedding・Gemma4TextModel・Gemma4ForConditionalGeneration.forward・Apache-2.0）

- 出所: 手元の固定の版の transformers `transformers/models/gemma4/modeling_gemma4.py`（全体の SHA16 3F6A049B83B79BE6）・SHA16 AD5DB34414669DDA・22090 字

```python
# ---- Gemma4RMSNorm（元の行 197〜215） ----
class Gemma4RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6, with_scale: bool = True):
        super().__init__()
        self.eps = eps
        self.with_scale = with_scale

        if self.with_scale:
            self.weight = nn.Parameter(torch.ones(dim), requires_grad=True)

    def _norm(self, hidden_states: torch.Tensor):
        mean_squared = hidden_states.pow(2).mean(-1, keepdim=True) + self.eps
        # Use torch.pow() (over torch.sqrt() or torch.rsqrt()) to address compiler differences between Torch and JAX
        return hidden_states * torch.pow(mean_squared, -0.5)

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        normed_output = self._norm(hidden_states.float())
        if self.with_scale:
            normed_output = normed_output * self.weight.float()
        return normed_output.type_as(hidden_states)
# ---- Gemma4TextDecoderLayer（元の行 1359〜1445） ----
class Gemma4TextDecoderLayer(GradientCheckpointingLayer):
    def __init__(self, config: Gemma4TextConfig | Gemma4VisionConfig, layer_idx: int):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.layer_idx = layer_idx
        self.self_attn = Gemma4TextAttention(config=config, layer_idx=layer_idx)
        self.mlp = Gemma4TextMLP(config, layer_idx)
        self.input_layernorm = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)
        self.pre_feedforward_layernorm = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)
        self.post_feedforward_layernorm = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)
        self.layer_scalar = nn.Buffer(torch.ones(1))

        self.hidden_size_per_layer_input = config.hidden_size_per_layer_input
        if self.hidden_size_per_layer_input:
            self.act_fn = ACT2FN[config.hidden_activation]
            self.per_layer_input_gate = nn.Linear(self.hidden_size, self.hidden_size_per_layer_input, bias=False)
            self.per_layer_projection = nn.Linear(self.hidden_size_per_layer_input, self.hidden_size, bias=False)
            self.post_per_layer_input_norm = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)

        self.enable_moe_block = config.enable_moe_block
        if self.enable_moe_block:
            self.router = Gemma4TextRouter(config)
            self.experts = Gemma4TextExperts(config)
            self.post_feedforward_layernorm_1 = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)
            self.post_feedforward_layernorm_2 = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)
            self.pre_feedforward_layernorm_2 = Gemma4RMSNorm(self.hidden_size, eps=config.rms_norm_eps)

    def forward(
        self,
        hidden_states: torch.Tensor,
        per_layer_input: torch.Tensor = None,
        shared_kv_states: dict[str, tuple[torch.Tensor, torch.Tensor]] | None = None,
        position_embeddings: torch.Tensor = None,
        attention_mask: torch.Tensor | None = None,
        position_ids: torch.LongTensor | None = None,
        past_key_values: Cache | None = None,
        **kwargs,
    ) -> torch.Tensor:
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)
        hidden_states, _ = self.self_attn(
            hidden_states=hidden_states,
            position_embeddings=position_embeddings,
            attention_mask=attention_mask,
            shared_kv_states=shared_kv_states,
            position_ids=position_ids,
            past_key_values=past_key_values,
            **kwargs,
        )
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = residual + hidden_states

        residual = hidden_states
        hidden_states = self.pre_feedforward_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)

        if self.enable_moe_block:
            hidden_states_1 = self.post_feedforward_layernorm_1(hidden_states)

            # Take hidden states before MLP here
            hidden_states_flat = residual.reshape(-1, residual.shape[-1])
            _, top_k_weights, top_k_index = self.router(hidden_states_flat)
            hidden_states_2 = self.pre_feedforward_layernorm_2(hidden_states_flat)
            hidden_states_2 = self.experts(hidden_states_2, top_k_index, top_k_weights)
            hidden_states_2 = hidden_states_2.reshape(residual.shape)
            hidden_states_2 = self.post_feedforward_layernorm_2(hidden_states_2)

            # Combine mlp and moe outputs
            hidden_states = hidden_states_1 + hidden_states_2

        hidden_states = self.post_feedforward_layernorm(hidden_states)
        hidden_states = residual + hidden_states

        if self.hidden_size_per_layer_input:
            residual = hidden_states
            hidden_states = self.per_layer_input_gate(hidden_states)
            hidden_states = self.act_fn(hidden_states)
            hidden_states = hidden_states * per_layer_input
            hidden_states = self.per_layer_projection(hidden_states)
            hidden_states = self.post_per_layer_input_norm(hidden_states)
            hidden_states = residual + hidden_states

        hidden_states *= self.layer_scalar
        return hidden_states
# ---- Gemma4TextScaledWordEmbedding（元の行 1448〜1459） ----
class Gemma4TextScaledWordEmbedding(nn.Embedding):
    """
    This module overrides nn.Embeddings' forward by multiplying with embeddings scale.
    """

    def __init__(self, num_embeddings: int, embedding_dim: int, padding_idx: int, embed_scale: float = 1.0):
        super().__init__(num_embeddings, embedding_dim, padding_idx)
        self.scalar_embed_scale = embed_scale
        self.embed_scale = nn.Buffer(torch.tensor(embed_scale), persistent=False)

    def forward(self, input_ids: torch.Tensor):
        return super().forward(input_ids) * self.embed_scale.to(self.weight.dtype)
# ---- Gemma4TextModel（元の行 1572〜1801） ----
@auto_docstring(custom_intro="The base Gemma 4 language model without a language modeling head.")
class Gemma4TextModel(Gemma4PreTrainedModel):
    config: Gemma4TextConfig
    input_modalities = ("text",)
    _can_record_outputs = {
        "router_logits": OutputRecorder(Gemma4TextRouter, index=0),
        "hidden_states": Gemma4TextDecoderLayer,
        "attentions": Gemma4TextAttention,
    }

    def __init__(self, config: Gemma4TextConfig):
        super().__init__(config)
        self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size

        # Gemma4 downcasts the below to bfloat16, causing sqrt(3072)=55.4256 to become 55.5. See https://github.com/huggingface/transformers/pull/29402
        self.embed_tokens = Gemma4TextScaledWordEmbedding(
            config.vocab_size, config.hidden_size, self.padding_idx, embed_scale=self.config.hidden_size**0.5
        )
        self.layers = nn.ModuleList(
            [Gemma4TextDecoderLayer(config, layer_idx) for layer_idx in range(config.num_hidden_layers)]
        )
        self.norm = Gemma4RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.rotary_emb = Gemma4TextRotaryEmbedding(config)
        self.gradient_checkpointing = False
        self.unique_layer_types = set(self.config.layer_types)

        # Per-Layer Embeddings (PLE): auxiliary embedding that feeds a residual signal
        # into each decoder layer. See `get_per_layer_inputs()` and `project_per_layer_inputs()`
        # for the full pipeline. The embedding is packed: total dim = num_layers * per_layer_dim.
        self.hidden_size_per_layer_input = config.hidden_size_per_layer_input
        if self.hidden_size_per_layer_input:
            self.embed_tokens_per_layer = Gemma4TextScaledWordEmbedding(
                config.vocab_size_per_layer_input,
                config.num_hidden_layers * config.hidden_size_per_layer_input,
                self.padding_idx,
                embed_scale=config.hidden_size_per_layer_input**0.5,
            )
            self.per_layer_input_scale = 2.0**-0.5
            self.per_layer_model_projection = nn.Linear(
                config.hidden_size,
                config.num_hidden_layers * config.hidden_size_per_layer_input,
                bias=False,
            )
            self.per_layer_model_projection_scale = config.hidden_size**-0.5
            self.per_layer_projection_norm = Gemma4RMSNorm(config.hidden_size_per_layer_input, eps=config.rms_norm_eps)

        # Update `_keys_to_ignore_on_load_unexpected` to drop all k/v proj and norms for the shared layers
        self._keys_to_ignore_on_load_unexpected = []
        for i, layer in enumerate(self.layers):
            if layer.self_attn.is_kv_shared_layer:
                self._keys_to_ignore_on_load_unexpected.extend(
                    [f"layers.{i}.self_attn.{name}" for name in ("k_proj", "v_proj", "k_norm", "v_norm")]
                )

        # Initialize weights and apply final processing
        self.post_init()

    @merge_with_config_defaults
    @capture_outputs
    @auto_docstring
    def forward(
        self,
        input_ids: torch.LongTensor | None = None,
        attention_mask: torch.Tensor | None = None,
        position_ids: torch.LongTensor | None = None,
        past_key_values: Cache | None = None,
        inputs_embeds: torch.FloatTensor | None = None,
        per_layer_inputs: torch.Tensor | None = None,
        use_cache: bool | None = None,
        **kwargs: Unpack[TransformersKwargs],
    ) -> Gemma4TextModelOutputWithPast:
        r"""
        per_layer_inputs (`torch.Tensor`, *optional*):
            Pre-computed per-layer input text embeddings of shape `(batch_size, sequence_length, num_hidden_layers,
            hidden_size_per_layer_input)`. When provided, these are used directly instead of being computed from `input_ids`
            via `get_per_layer_inputs()` in the text model. If calling the `forward` with `inputs_embeds` instead of `input_ids`,
            you should probably precompute them and forward them along `inputs_embeds`, otherwise recomputing them needs
            to reverse the main embedding, which is expensive.
        """
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError("You must specify exactly one of input_ids or inputs_embeds")

        if input_ids is not None and per_layer_inputs is not None:
            raise ValueError("You cannot specify per_layer_inputs if input_ids is provided")

        if input_ids is not None:
            inputs_embeds = self.embed_tokens(input_ids)

        if self.hidden_size_per_layer_input:
            if per_layer_inputs is None:
                per_layer_inputs = self.get_per_layer_inputs(input_ids, inputs_embeds)
            per_layer_inputs = self.project_per_layer_inputs(inputs_embeds, per_layer_inputs)

        if use_cache and past_key_values is None:
            past_key_values = DynamicCache(config=self.config)

        if position_ids is None:
            past_seen_tokens = past_key_values.get_seq_length() if past_key_values is not None else 0
            position_ids = torch.arange(inputs_embeds.shape[1], device=inputs_embeds.device) + past_seen_tokens
            position_ids = position_ids.unsqueeze(0)

        # It may already have been prepared by e.g. `generate`
        if not isinstance(causal_mask_mapping := attention_mask, dict):
            # Prepare mask arguments
            mask_kwargs = {
                "config": self.config,
                "inputs_embeds": inputs_embeds,
                "attention_mask": attention_mask,
                "past_key_values": past_key_values,
                "position_ids": position_ids,
            }
            # Create the masks
            causal_mask_mapping = {
                "full_attention": create_causal_mask(**mask_kwargs),
                "sliding_attention": create_sliding_window_causal_mask(**mask_kwargs),
            }

        # embed positions
        hidden_states = inputs_embeds
        position_embeddings = {}
        for layer_type in self.unique_layer_types:
            position_embeddings[layer_type] = self.rotary_emb(hidden_states, position_ids, layer_type)

        # Initialize as empty dict, or reuse past shared states. We use a UserDict instead of built-in dict (it behaves
        # the same) for fsdp2 support (otherwise, `_apply_to_tensors` rebuilds every dict it recurses into, and `shared_kv_states`
        # is not correctly shared, see https://github.com/pytorch/pytorch/blob/v2.10.0/torch/distributed/utils.py#L223-L255)
        shared_kv_states = kwargs.pop("shared_kv_states", UserDict())

        # decoder layers
        for i, decoder_layer in enumerate(self.layers[: self.config.num_hidden_layers]):
            per_layer_input = per_layer_inputs[:, :, i, :] if per_layer_inputs is not None else None

            hidden_states = decoder_layer(
                hidden_states,
                per_layer_input,
                shared_kv_states=shared_kv_states,
                position_embeddings=position_embeddings[self.config.layer_types[i]],
                attention_mask=causal_mask_mapping[self.config.layer_types[i]],
                position_ids=position_ids,
                past_key_values=past_key_values,
                **kwargs,
            )

        hidden_states = self.norm(hidden_states)

        return Gemma4TextModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=past_key_values,
            shared_kv_states=shared_kv_states if kwargs.get("return_shared_kv_states", False) else None,
        )

    def get_per_layer_inputs(self, input_ids: torch.Tensor | None, inputs_embeds: torch.Tensor | None) -> torch.Tensor:
        """Compute the token-identity component of Per-Layer Embeddings (PLE).

        Looks up `input_ids` in `embed_tokens_per_layer` (a scaled embedding that multiplies
        by `sqrt(hidden_size_per_layer_input)`) and reshapes the packed output from
        `[batch, seq, num_hidden_layers * hidden_size_per_layer_input]` to
        `[batch, seq, num_hidden_layers, hidden_size_per_layer_input]`.

        If only `inputs_embeds` is provided (no `input_ids`), reverses the main embedding
        to recover `input_ids` for the PLE lookup.
        """
        if not self.hidden_size_per_layer_input:
            raise RuntimeError(
                "Attempting to call get_per_layer_inputs() from a model initialized with a config that does not support"
                f" per-layer embeddings. {self.config}"
            )

        # If only inputs_embeds are provided, reverse main embedding to find the input_ids - this allows to `generate`
        # from `inputs_embeds` only as other models (otherwise it would need the value from both embeddings)
        if input_ids is None:
            with torch.no_grad():
                input_ids = (
                    (
                        inputs_embeds[:, :, None, :]
                        == self.embed_tokens.weight[None, None, :, :] * self.config.hidden_size**0.5
                    )
                    .all(dim=3)
                    .nonzero()[:, 2]
                )
                try:
                    input_ids = input_ids.view(inputs_embeds.shape[:2])
                except RuntimeError:
                    raise RuntimeError(
                        "It seems like you tried to call `forward` from `inputs_embeds` without providing `input_ids`, and that "
                        "the `inputs_embeds` you provided do not exactly match the embedding weights. Since Gemma4 needs to reverse "
                        "the embedding to compute another embedding, make sure you provide exact `inputs_embeds`"
                    )

        return self.embed_tokens_per_layer(input_ids).reshape(
            *input_ids.shape,
            self.config.num_hidden_layers,
            self.hidden_size_per_layer_input,
        )

    def project_per_layer_inputs(
        self,
        inputs_embeds: torch.Tensor,
        per_layer_inputs: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """Compute the context-aware component of PLE and combine with token-identity.

        Projects `inputs_embeds` through `per_layer_model_projection` (Linear), scales by
        `1/sqrt(hidden_size)`, reshapes to `[batch, seq, num_layers, ple_dim]`, and normalizes
        with `per_layer_projection_norm` (RMSNorm).

        If `per_layer_inputs` (the token-identity component from `get_per_layer_inputs()`)
        is provided, combines both: `(context_projection + token_identity) * (1/sqrt(2))`.
        If `per_layer_inputs` is None (e.g. for multimodal inputs where input_ids are not
        available), returns just the context projection.
        """
        if not self.hidden_size_per_layer_input:
            raise RuntimeError(
                "Attempting to call project_per_layer_inputs() from a model initialized with a config that does not"
                f" support per-layer embeddings. {self.config}"
            )

        per_layer_projection = self.per_layer_model_projection(inputs_embeds) * self.per_layer_model_projection_scale
        per_layer_projection = per_layer_projection.reshape(
            *inputs_embeds.shape[:-1],
            self.config.num_hidden_layers,
            self.hidden_size_per_layer_input,
        )
        per_layer_projection = self.per_layer_projection_norm(per_layer_projection)

        if per_layer_inputs is None:
            return per_layer_projection

        return (per_layer_projection + per_layer_inputs) * self.per_layer_input_scale
# ---- Gemma4ForConditionalGeneration.forward（元の行 2525〜2605） ----
    @can_return_tuple
    @auto_docstring
    def forward(
        self,
        input_ids: torch.LongTensor | None = None,
        pixel_values: torch.FloatTensor | None = None,
        pixel_values_videos: torch.FloatTensor | None = None,
        input_features: torch.FloatTensor | None = None,
        attention_mask: torch.Tensor | None = None,
        input_features_mask: torch.Tensor | None = None,
        position_ids: torch.LongTensor | None = None,
        image_position_ids: torch.LongTensor | None = None,
        video_position_ids: torch.LongTensor | None = None,
        past_key_values: Cache | None = None,
        mm_token_type_ids: torch.LongTensor | None = None,
        inputs_embeds: torch.FloatTensor | None = None,
        labels: torch.LongTensor | None = None,
        use_cache: bool | None = None,
        logits_to_keep: int | torch.Tensor = 0,
        per_layer_inputs: torch.Tensor | None = None,
        **kwargs: Unpack[TransformersKwargs],
    ) -> Gemma4CausalLMOutputWithPast:
        r"""
        input_features_mask (`torch.FloatTensor` of shape `(num_images, seq_length)`):
            The attention mask for the input audio.
        image_position_ids (`torch.LongTensor` of shape `(batch_size, max_patches, 2)`, *optional*):
            2D patch position coordinates from the image processor, with `(-1, -1)` indicating padding.
            Passed through to the vision encoder for positional embedding computation.
        video_position_ids (`torch.LongTensor` of shape `(num_videos, num_frames, max_patches, 2)`, *optional*):
            2D patch position coordinates from the video processor, with `(-1, -1)` indicating padding.
            Passed through to the vision encoder for positional embedding computation.
        per_layer_inputs (`torch.Tensor`, *optional*):
            Pre-computed per-layer input text embeddings of shape `(batch_size, sequence_length, num_hidden_layers,
            hidden_size_per_layer_input)`. When provided, these are used directly instead of being computed from `input_ids`
            via `get_per_layer_inputs()` in the text model. If calling the `forward` with `inputs_embeds` instead of `input_ids`,
            you should probably precompute them and forward them along `inputs_embeds`, otherwise recomputing them needs
            to reverse the main embedding, which is expensive.
        """
        outputs = self.model(
            input_ids=input_ids,
            pixel_values=pixel_values,
            pixel_values_videos=pixel_values_videos,
            input_features=input_features,
            attention_mask=attention_mask,
            input_features_mask=input_features_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            mm_token_type_ids=mm_token_type_ids,
            inputs_embeds=inputs_embeds,
            per_layer_inputs=per_layer_inputs,
            labels=labels,
            use_cache=use_cache,
            image_position_ids=image_position_ids,
            video_position_ids=video_position_ids,
            return_dict=True,
            **kwargs,
        )

        hidden_states = outputs.last_hidden_state
        # Only compute necessary logits, and do not upcast them to float if we are not computing the loss
        slice_indices = slice(-logits_to_keep, None) if isinstance(logits_to_keep, int) else logits_to_keep
        logits = self.lm_head(hidden_states[:, slice_indices, :])
        if (final_logit_softcapping := self.config.get_text_config().final_logit_softcapping) is not None:
            logits = logits / final_logit_softcapping
            logits = torch.tanh(logits)
            logits = logits * final_logit_softcapping

        loss = None
        if labels is not None:
            loss = self.loss_function(logits, labels, self.config.get_text_config().vocab_size, **kwargs)

        return Gemma4CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            image_hidden_states=outputs.image_hidden_states,
            audio_hidden_states=outputs.audio_hidden_states,
            shared_kv_states=outputs.shared_kv_states,
        )
```

---

材料はここまでです。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
