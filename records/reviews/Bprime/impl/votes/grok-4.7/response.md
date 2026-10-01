模型: Grok 4・作り手: xAI

道具は使っていません。実行もしていません。以下は材料の字と、そこからの推論です。

## 所見

**G-01**・**重い**・`boot_bprime.py` の `run`（`TOOLS` を `sys.path` に足した直後の import、`PHASE == 'check'` の `import bprime_reextract`、`part == 'rewrite'|'reextract'` の import）

起動器は `import bprime_recompute_rewrite` / `import bprime_reextract` を、公開の置き場の `tools/` から裸の名で読む。二つの道のファイルは `tools/independent/` にあり、Colab では `ROOT` が公開の置き場（内部の `Bprime/` を clone しない）。`sys.path` に `independent` を足す処理も、ファイルを写す処理も無い。

check 相は `ImportError` を捕らえて `reextract=None` にし、項目を「落ちた」と記録したあと、`all_pass` が偽でも終了コード 0 で zip して戻る（`if not rec['all_pass']: stop` が無い）。recompute 相の import 失敗は `TOOL_ERR = (ToolError, AssertionError)` の外なので、器の誤りの記録にならず落ちる。このままだと独立の二道は本の走りに届かない。

直し方: 起動の前に `tools/independent` を `sys.path` に足す（DRY は `OP4B_BPRIME_DIR/tools/independent`、Colab は内部の器をランタイムへ写す段を起動器に書く）。check 相は `all_pass` が偽なら `stop` する。

確信度: 高。字で確かめた。

**G-02**・**中**・`bprime_recompute_rewrite.py` の `_die`、`bprime_reextract.py` の `_die`、`boot_bprime.py` の `except TOOL_ERR`

独立の二道は止めを `SystemExit` で上げる。起動器が器の誤りとして包むのは `ToolError` と `AssertionError` だけ。`SystemExit` は `BaseException` なので、その `except` にも末尾の `except Exception`（zip を書く枝）にも入らない。台帳不一致・方向の形・hook の掛け残しで、session も tool_error の JSON も残さずプロセスが終わる。

直し方: `_die` を `ToolError`（または起動器が捕らえる例外）にする。起動器側で包むなら `SystemExit` を器の誤りとして記録してから止める。

確信度: 高。字で確かめた。

**G-03**・**軽い**・`analyze_Bprime.py` の `recompute_agreement` の `override`

`r['id'] not in path` の行は黙って飛ばす。一段目だけ見ると、両道が同じ行を欠いたとき、その行の値は比べず、札は `p_override` に無いので本の計算の効き目に落ちて、両道の札がそろって見える。

本番の `judge`（`rows_subset is None`）では、二段目が本の計算の行集合とフックの道を `agreement` の鍵で比べるので、フックの道の欠けは `reason='keys'` で不一致になる。穴が残るのは、一段目だけを見る呼び出しと、DRY の `rows_subset=set(hook)`（`judge` の末尾）で、フックの道に無い行を期待集合から外すとき。空の辞書どうしは `max()` が `ValueError` になる（全升目を外した縁。続ける決定では起きにくい）。

直し方: `use(r)` を満たす行の集合と、hook・rewrite の鍵が一致しなければ不一致にする。DRY でもこの照合を外さない。

確信度: 高。字で確かめた。

**G-04**・**中**（実装の誤りではなく、合成の確かめの穴）・`bprime_recompute_rewrite.py` の `tiny_model`・`_dry`・`_selftest` の変種 `ple_scalar`

`--dry` と注入の自己検査は、既定の小さな模型（`layer_scalar` は `ones`、層ごとの入力なし）だけで方向を足す。`ple_scalar` は零の書き換えと模型の forward の最終の正規化の入力のビット一致だけを見る。

`layer_scalar == 1` のとき、掛け算の前に足すのと後に足すのは同じ値になる。層ごとの入力が無いとき、その足し込みの前か後かも区別できない。歯 M0–M8 にこの変種は無く、歯は合否に入らない（`_dry` の `verdicts` は本の突き合わせだけ）。

本の模型の一段目では、フックの道が `register_forward_hook`（層の `return` の後）なので、書き換えの道が前に足せば差が出て捕まる。合成の `--dry` だけでは、この種の誤りは見えない。

直し方: `--dry` を `variant='ple_scalar'`（`layer_scalar` を 1 から離した模型）でも走らせ、合否に入れる。

確信度: 高（穴の形）。字で確かめた。

**G-05**・**中**（同じく確かめの穴）・`bprime_recompute_rewrite.py` の `_selftest`（softcap を抜いた差を「参考」にする箇所）と `_teeth` の `M6`

softcap は `cap * tanh(z/cap)` で、`|z| ≪ cap` のとき恒等に近い。自己検査は 1+g と `hidden_states[-1]` の取り違えは「正しい読み取りの差の 10 倍」を要求するが、softcap の抜けは判定に入れず印字だけ。歯 M6 も参考で、`--dry` の合否に入らない。

小さな模型は語彙の行列を 4 倍、正規化の重みを [2, 3) にするが、初期の埋め込みが小さいと出口の値は cap 30 よりずっと小さく、差が `tol_stage1`（0.001）に届かないことがある（大きさは読んで推した。実行していない）。

直し方: 出口の値を cap の近くまで大きくした変種で、softcap の抜けが許容の外に出ることを合否にする。

確信度: 中。式は字で確かめた。大きさは読んで推した。

**G-06**・**軽い**（凍結時の一段目の穴。合成の側は見分けられる）・正本 `layers.window_assert`・`inputs.model_facts.sliding_window` 1024・書き換えの道の `TINY_TEXT['sliding_window']=8`

本の列は窓より短い想定なので、実の重みの一段目では窓つき mask と全体の mask がほぼ一致し、窓の付け忘れは差に出ない。小さい模型（窓 8・台帳の長い列）の零の書き換えと `--dry` は、手回しの mask が模型の forward と違えばビットまたは許容で捕まる。その出力は材料に無い。凍結のゲートは、この自己検査が通ったことに依存する。

確信度: 高（構造）。窓の値は正本の字。mask の中身は抜き書きに無く、一致は読んで推した。

**G-07**・**軽い**・`analyze_Bprime.py` の `reextract_agreement`・`bprime_reextract.py` の `reextract_all`

再抽出のゲートは、道が返す `h_norm_by_context`・`vhat_norm`・`named_cos` だけを見る。活性のベクトルは渡らない。余弦を 1、ノルムを抽出の記録の写しにすれば、模型を流さずに一致になる。

`--dry` と `bprime_phases.check_items` の `reextract_path` は活性を直接比べるが、四つ（意味のない列）に限る。十六文脈の活性の突き合わせは `--dry` の参考行で、合否に入らない。

直し方: 凍結のゲートに、文脈ごとの活性（またはその SHA）を渡し、集計の側でノルムと余弦を計算し直す。

確信度: 高。字で確かめた。

**G-08**・**軽い**・`bprime_run.py` の `Runner.readout` と `bprime_recompute_rewrite.py` の `readout`

フックの道は softcap 後の値を `.double()` してから `K.log_odds_a` に渡す（`log_odds_a` の本体は材料に無い）。書き換えの道は `logsumexp` を float32 のまま計算し、`float()` で Python の float にする。選択は数個なので、差は一段目の許容 0.001 より小さい見込み。ビット一致は期待しない方がよい。

直し方: 書き換えの道も softcap 後に float64 で `logsumexp` する。

確信度: 中。読んで推した（`log_odds_a` は未読）。

**G-09**・**軽い**・`boot_bprime.py`（材料の全文）

正本 `layers.window_assert` は、列の長さが窓より短いことを起動器が assert し、転記行 F に入れる、と書く。渡された起動器にはその assert が無い。他のファイルにあるかもしれない。

直し方: 最初の順伝播の前に、升目の列の長さと `sliding_window` を assert する。

確信度: 中（このファイルには無い、までは高）。他のファイルは未読。

**G-10**・**軽い**・`bprime_recompute_rewrite.py` の `layer_index_for`

選ぶ層の種類が正本 `layers.layer_type`（`full_attention`）と違うと、本物かどうかに関係なく止める。独立の `--selftest` の小さな模型は選ぶ層を `full_attention` にするので通る。Colab の DRY は `dry_bprime.tiny_model`（材料に無い）を使い、`dry_contract` は `layer_types` を書き換えない。その模型が選ぶ層を窓つきにしていると、計算が正しくても書き換えの道だけ DRY で止まる。再抽出の `layer_for` は種類を見ない。

直し方: 種類の assert は `is_real` のときだけにするか、DRY の小さな模型も同じ規則で `layer_types` を組む。

確信度: 中。assert は字で確かめた。`dry_bprime.tiny_model` は未読。

## 是認

- 足す時点は三つの道で同じで、正本の「選んだ層の出力」と抜き書きに合う。`Gemma4TextDecoderLayer.forward` は、層ごとの入力の足し込みのあとで `hidden_states *= self.layer_scalar` してから返す。フックの道は `G.register_hook` → `register_forward_hook`（戻り値の後）。書き換えの道は `h = layer(...)` の直後に `h[0, mp:, :] += add`。再抽出は `hidden_states[L+1]` で、`bprime_phases` の `layer_alignment` が「選んだ層のフック出力と `hidden_states[k+1]` が一致し、最後の層は `hidden_states[n]` と一致しない」ことを要求している。`layer_scalar` の前、層ごとの入力の前、ではない。
- 足す位置は主位置から列の最後まで（`mp:`）。読み取りは最終の正規化の入力の最後の位置。フックは最終の正規化の pre-hook の `a[0][:, -1, :]`、書き換えは手回しの最後の層の出力の `[0, -1]`（手回しは `self.norm` を掛けない。抜き書きでも層のループと `self.norm` の間に処理は無い）。`hidden_states[-1]` は読み取りに使っていない。
- 符号と係数は一度だけ。書き換えの `cast_add` は float64 → NumPy float32 → 層の出力の型、のあと `sign * coef` を掛ける。フックの道は `make_hook(V, coef, sign, starts)` に同じ材料を渡す（`make_hook` の本体は未読。指示の算術と呼び出しは一致している）。
- 無操作は零のベクトルを同じ算術で足す。効き目は加えた値 − 無操作。比べる相手の逆向きは、符号を別の順伝播で掛ける（効き目の符号反転ではない）。`recompute_set` の組と、集計の `comps_same` / `comps_opp` の引き方はそろっている。
- 読み取りの式は正本どおり。正規化は `h * rsqrt(mean(h²)+eps) * g`（1+g ではない）。softcap は `cap * tanh(z/cap)`（抜き書きの `z/cap → tanh → *cap` と同じ）。語彙の行列は `lm_head.weight`。float32 に上げるのは最終の正規化の入力のあと。順伝播と加減は模型の型（本物は bf16 を `check_env` / `reextract_all` が確かめる）。
- 一段目はバッチ一・`use_cache=False`（書き換えの既定も False で、`past=None`。模型の forward は `use_cache` が真のときだけ `DynamicCache` を作る）。本番の起動器は `use_cache` を渡さない。
- 升目と抽出の文脈は、凍結の `user_message`・`scenario_and_instruction` とチャットの型のあと、台帳の `ids_sha16` と違えば止まる。入力の食い違いは静かに通らない。
- 再抽出の名前のある方向は、正本 `directions.defs` の文と指示の対応が違えば止まる。コーディネータの `NAMED` と同じ四つ（static＝O−Osec、loaded＝O-Ncold−Osec-Ncold、Nk＝Nk−N、td＝Onull−N）。場面の平均は N1 と S1。`‖v̂‖` は揃える前の static のノルムで、抽出の記録の `vhat_norm` と同じ定義。余弦は尺度に依らないので、`match_to_static` が正の倍率だけなら一致の判定は成り立つ（`match_to_static` の本体は未読）。
- 再抽出が選んだ層より後も流すのは、正本 `reextract.path` と指示が許している。選んだ層の出力は後の層より前に確定する（`shared_kv_states` は後の層が書く）。最後の層は `L < n-1` で拒む。本物の添字 29 では止まらない。
- 指示の文は、正本と抜き書きに対して読み違いを誘っていない。足す位置・1+g ではないこと・`hidden_states[-1]` を使わないこと・`hidden_states[k+1]` は、正本の `hidden_states_index = index+1` と `layer_alignment` と一致する。三つの道がそろって正本と違う、という箇所は、材料の範囲では見当たらなかった。
- 一段目の一致は、無操作と効き目の差の最大と札の両方（`K.agreement` を札だけに上書きしていない）。二段目が札だけなのは正本の裁定 D234 どおり。有限でない値は `agreement` が不一致にする。外した升目は `recompute_set` と比較の `use` の両方で除く。
- 正規化の `rsqrt` は、モジュールの `pow(..., -0.5)` と違うが、正本が `rsqrt` と書いており、フックの道と書き換えの道は同じ式である。
- 埋め込みの倍率は `Gemma4TextScaledWordEmbedding.forward` の中。書き換えの道は `get_input_embeddings()` を呼ぶので、部品を取り替えない限り倍率は模型と同じ（零の書き換えのビット一致がゲート。その出力は未見）。

## 合成の確かめが見分けられないもの

- `layer_scalar` の前に足す／層ごとの入力の足し込みの前に足す（G-04）。既定の小さな模型では、正しい実装と同じ値になる。
- softcap の抜け（G-05）。出口の値が小さいと許容の内に収まる。
- 歯 M7（層の型に直さず float32 のまま足す）は、float32 の模型では正しい道と同じ。bf16 の歯でだけ差が出る。
- 歯はすべて参考で、`--dry` の合否に入らない。歯が「捕まえなかった」と印字してもプロセスは成功する。
- `--dry` は札（Holm・裾・側・二つ目の札）を見ない、と器が自分で書いている。札の境界だけの違いは合成の `--dry` では見えない。集計の `_selftest` は合成の効き目で札の一致と、壊した一段目の不一致を見ている。
- 実の模型の一段目は、列が窓より短いと窓つき mask の誤りを見ない（G-06）。小さい模型の自己検査は見分けられる形になっている。結果は材料に無い。
- 再抽出の `--dry` の合否は四文脈だけ。十六文脈は参考行。

見分けられる形になっているもの: 零の書き換えと模型の forward のビット一致（mask・rotary・埋め込みの倍率・層ごとの入力の有無。`ple_scalar` を含む）、主位置より前を変えないこと、足した量の型と符号と係数、`hidden_states[-1]` と 1+g の取り違え、選んだ層の一つ後（歯 M2）、帯の起点の一つ後（歯 M1）、符号反転（歯 M3）、係数の二重（歯 M4）、正規化の二重（歯 M5）。これらが許容の外に出るかは実行していない。

## 読んでいない所

- `run_stageB_local.make_hook` の本体（加減の算術は指示と呼び出しから推した）。
- `bl3_core.log_odds_a`・`effect_side`・`second_label`・`cells_decision`。`agreement` と `recompute_set` は材料の抜き書きで読んだ。
- `Gemma4Model.forward`・`create_masks_for_generate`・`masking_utils`・rotary の本体・`capture_outputs`。手回しが模型の forward と一致するかは、零の書き換えのビット一致に依存する。その出力は見ていない。
- `steer_B.match_to_static`・`direction_B.layer_index` の式の本体（本物では添字 29 との assert がある）。
- 台帳 `ledger-bprime.json`・開発の記録・`dry_bprime.py`・`prev/`。
- 正本の抜粋で `inputs.model_facts` と `inputs.versions` が点つきの鍵に見える箇所は、器がすべて `C['inputs']['model_facts']` と読むので、抜粋の平坦化と読んだ。ファイルが文字どおり点つきの鍵なら、三つの道は本の走りの前に `KeyError` で止まる（静かな誤った値にはならない）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。