<!-- 逐語保全: 器についての意見伺い（登録者裁定 D230・巡に数えない）・系統外・一人目（呼び名 G1）。本文の中の機種の申告は「Gemini 1.5 Pro」。登録者の言葉では「Gemini 3.8 Flash 二名（いずれも、回答での申告は、「Gemini 1.5 Pro」「Gemini 2.5 Pro」となっていますが、モデル名はGemini 3.8 Flashが正しいです。Google AI Studio のモデル選択で私が確認済み）」（登録者の言葉は逐語・下の出所）。
     登録者（楠見優太）が会話で渡したご意見を、会話の記録から機械で切り出した（作業の途中に届いた形の登録者の言葉・uuid 374b0998-9303-456c-9a94-248e8fdfccc2・元の uuid ec487404-8a19-491e-8693-7403744d061a・2026-09-25 09:16 日本時間）。
     この枠の外は一字も変えていない。本意見のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->
### 系統の明記

- **系統**: 系統外（Google Gemini 系）
- **機種**: Gemini 1.5 Pro（依頼文・束の検分者として独立の立場で回答）

---

### はじめに（総括）

楠見優太様、南無弥勒如来様。
B-lens 層三（Bl3）の器一式（本の器 `tools/bl3_run.py`、残差書き換えの道 `tools/bl3_recompute_rewrite.py`、計算の芯 `tools/bl3_core.py`、集計器 `tools/analyze_Bl3.py`、Colab 起動器 `tools/colab/boot_Bl3.py`、合成データ器 `tools/dry_run_Bl3.py`）および正本 v6（`design/contrasts-Bl3.json`）を拝読し、式・アルゴリズム・データフローの精査を行いました。

**全体の所見**:
二つの独立した道（本のフック道と残差書き換え道）の整合性、および近道・バッチング・下見判定木・札・門・乙の論理は極めて高い精度で組み上げられており、正本 v6 の規定と厳密に一致しています。段階 B や B-lens からの教訓（符号の二重掛け、二重正規化、`hidden_states[-1]` の正規化後テンソル取り違え、主位置アサートなど）が各所に反映され、防護が施されていることを確認しました。

その上で、凍結の前に確認・検討しておくべき潜在的な留意点、および合成データ検証の盲点について、以下の通り所見をまとめます。結果の見込みや特定の行への評価は一切含んでいません。

---

### 1. 二つの道が共有しうる読み違い（正本 vs フック道 vs 残差書き換え道）

正本 `readout.primary`, `layers`, `computation`, `independent_recompute` を踏まえ、第四部の `Runner.forward` / `readout` / `recompute_hook_path` と第五部の `forward_rewrite` / `readout` / `recompute_rewrite` を突き合わせました。

#### (1) 入力の並び、主位置、読み取り位置
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `readout.primary.rule`, `readout.primary.prefix_source`, `bl3_run.py` (L37–48, L330–350), `bl3_recompute_rewrite.py` (L129–186)
- **確認内容**:
  - プロンプトと書き出しの結合について、両道とも「文字列結合した後にトークナイズ」ではなく「`prompt_ids + prefix_ids`（トークン ID 列のリスト結合）」を採用しています。BPE の境界マージ（例えば改行とバッククォートの結合など）によるトークン境界の変形を避けて段階 B の教師強制状態を忠実に再現しており、転記行 B の `prompt_len`, `main_position`, `readout_position` とのアサートでも照合されています。
  - 主位置 `mp` は両道とも `len(prompt) - 1`、読み取り位置 `ro` は `len(ids) - 1`（末尾位置）で一致しています。

#### (2) 加える帯（どの位置に足すか）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `readout.primary.band`, `bl3_run.py` (L115–123), `bl3_recompute_rewrite.py` (L240)
- **確認内容**:
  - 正本規定は「主位置から読み取りの位置まで」。
  - `bl3_run.py` では `starts = [cell.mp] * B` を `make_hook` に渡し、`hs[i, int(st):, :] += add`。
  - `bl3_recompute_rewrite.py` では `h[0, int(mp):, :] = h[0, int(mp):, :] + add`。
  - スライス `[mp:]` はインデックス `mp`（主位置）を含み、末尾（`ro`）まで届きます。主位置自身にも介入ベクトルが加算されており、両道で完全に一致しています。

#### (3) 足し方の算術（型の直し方、係数、符号）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `readout.primary.precision`, `layers.coef_applied`, `run_stageB_local.py` (L165–186), `bl3_recompute_rewrite.py` (L212, L239–240)
- **確認内容**:
  - 型変換の順序: `np.asarray(vec, dtype=np.float32)` $\to$ `torch.as_tensor(..., dtype=h.dtype)` (bf16) $\to$ `sign * coef * add`。
  - 係数 `coef`（2.0）は加算時に一度だけ掛けられ、二重掛けはありません。両道で同一の算術が成立しています。

#### (4) どの層の出力に足すか
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `layers.indices["0.5"]` (17), `layers.hidden_states_indices["0.5"]` (18), `bl3_run.py` (L130), `bl3_recompute_rewrite.py` (L231–241)
- **確認内容**:
  - `bl3_run.py` は `decoder_layers(model)[17]` の forward hook で出力を書き換え。
  - `bl3_recompute_rewrite.py` はループ `for i, layer in enumerate(layers):` で `i == 17` の実行直後に `h` を書き換えてレイヤー 18 に渡しています。
  - `hidden_states` のインデックスとのオフセット（埋め込み層が入るため +1 ずれること）も正本と合致しており、介入層の物理的位置は両道で完全に一致しています。

#### (5) 読み取り（最終正規化の入力、float32、読み取り集合、対数オッズ定義）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `readout.primary.quantity`, `readout.primary.precision`, `bl3_run.py` (L78–93, L125), `bl3_recompute_rewrite.py` (L254–269), `bl3_core.py` (L37–41)
- **確認内容**:
  - 最終正規化の入力: transformers 4.57.3 の `hidden_states[-1]` が正規化後テンソルである罠を両道とも回避しています。`bl3_run.py` は `model.model.norm` の `pre_hook` から取得し、`bl3_recompute_rewrite.py` は最終レイヤーのループ出口のテンソルを取得しています。
  - 正規化の適用: どちらも残差を `float32` に上げ、`g = model.model.norm.weight.float()` を用いて $x \cdot \text{rsqrt}(\text{mean}(x^2) + \epsilon) \cdot g$ を計算。
  - 出口の値: `lm_head.weight[set_ids].float()` との内積を計算。
  - 対数オッズ: $z_a - \text{logsumexp}(z_{\text{others}})$。
  - 集合の先頭は常に `'a'`（インデックス 0）、残りが `set_ids[1:]`。両道とも完全に一致しています。

#### (6) 無操作（零ベクトル）と効き目
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `readout.primary.batching`, `readout.primary.quantity`, `bl3_run.py` (L72–74, L291), `bl3_recompute_rewrite.py` (L317, L331–345)
- **確認内容**:
  - 無操作は長さ 2560 の `np.zeros`。
  - 効き目＝「方向を加えた値」−「無操作の値」。
  - 零ベクトルに対しても行の符号 `sign` と係数 `coef` を通して足しており、算術の偏りが生じない設計となっています。

#### (7) 減算の行の符号と比べる相手の両方の向き
- **重さ**: 中くらい（注意深い照合を要した点・問題なしの確認）
- **根拠**: 正本 `nulls.real.orientation_rule`, `bl3_core.py` (L250–263), `analyze_Bl3.py` (L71–98, L153–173), `bl3_run.py` (L313–328), `bl3_recompute_rewrite.py` (L334–345)
- **確認内容**:
  - 減算行（例: `sub:N1:O-Ncold-v~...`, `sign = -1`）において、主の方向（static）および帰無（iso）は符号 `-1` で流されます。
  - 比べる相手（実在の差 `real:p`）は、同一升目において同一符号 `sign = -1`（`comps_same`）と逆符号 `sign = +1`（`comps_opp`）の両方で計算されます。
  - `recompute_set` が生成するキーは、`comps_same` に対し `('real:p', s)`、`comps_opp` に対し `('real:p', -s)`。
  - 本の計算側（`cell_sign_sets`）でも、主の符号 `sg` と逆符号 `-sg` の両方のバッチが組まれ、`analyze_Bl3.py` の `main_ov` で `eff_main[k]["real:" + p]` と `eff_main[kk]["real:" + p]` として取得されています。
  - 本の器・再計算器・集計器の間で、符号反転の向き（`s` と `-s`）が完全に 1 対 1 で対応していることを検算しました。

---

### 2. 独立の道の無い所の精査

コーディネータが一人で書いた各機構について、正本との突き合わせおよび論理の破綻がないかを精査しました。

#### (1) 近道（`prefix_cache` と `DynamicCache` 展開）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `computation.shortcut_assert`, `pilot.checks.v`, `bl3_run.py` (L96–124)
- **確認内容**:
  - `prefix_cache` で主位置手前 `[:cell.mp]` までの KV キャッシュを作成し、`_expand` で `tuple((k.expand(B, ...), v.expand(B, ...)))` から `DynamicCache` を構築。
  - `forward` では `pc['end'] != cell.mp` の場合に `ToolError` を投げるアサート（裁定 D226）が機能しています。
  - 入力トークンは `cell.ids[cell.mp:]`、フックの起点は `starts = [0] * B` となり、主位置から末尾まで確実に加減が行われます。
  - RoPE の `cache_position` もキャッシュ長 `cell.mp` から継続するため、位置エンコーディングのズレも生じません。

#### (2) バッチの組み方（`batch_plan` と `run_cell_sign`）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `readout.primary.batching`, `bl3_core.py` (L266–276), `bl3_run.py` (L255–277)
- **確認内容**:
  - `batch_plan` で `order_seed` (91002) と升目インデックス `key` からなる `SeedSequence` で方向をシャッフルし、端数を `K.PAD`（零ベクトル）で埋めています。
  - `run_cell_sign` では、層ごとの差分取得（`lay['noop_lo']`, `noop_h`）を確実に行うため、`K.NOOP` を含むバッチを最優先（先頭）で実行する並べ替えを行っています。各バッチ内の構成（スロット配置）は維持されており、推論の独立性から計算結果への悪影響はありません。`K.PAD` のスロット値は結果から正しく破棄されています。

#### (3) 下見の確かめと機械の決定（`run_pilot` と `cells_decision`）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `pilot`, `bl3_run.py` (L170–234), `bl3_core.py` (L154–186)
- **確認内容**:
  - 順序: 自己検査 $\to$ (vi) $\to$ (i)〜(iv) $\to$ (v) $\to$ 決定木。
  - (vi)(b)（バッチ 1 の繰り返し揺れ）が `noise_max` (0.01) を超えた場合、直ちに `stop: True`, `q1: '止める'` でリターンし、(i)〜(v) を計算しません（裁定 D224）。
  - (vi)(a) が超えた場合は `batch = 1` に移行し、揺れの床 `floor` を設定。近道許容 `cache_tol` は $\min(\max(2 \times \text{floor}, 0.005), 0.01)$ で正しく計算。
  - (i)(ii) を満たす升目が 8 個中 6 個以上で継続、満たさない升目は `dropped` に送り、主の札・門から除外（`drop_effects`）。正本と完全に一致しています。

#### (4) 札（`labels`）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `labels`, `bl3_core.py` (L56–118), `analyze_Bl3.py` (L71–98)
- **確認内容**:
  - `p_equal_tailed`: 上裾・下裾の割合の小さい方の2倍（上限 1.0）。
  - `holm`: 段数 $m$ は下見で外した後の行数。$p < \text{step}$（下回る）で判定（正本 `labels.iso_outside`）。
  - `effect_side`: Q1〜Q3 の間に 0 があれば `sign_only`、そうでなければ `stronger` / `weaker` / `opposite`。
  - `second_label`: 比べる相手の中央値 `center` を引き、中心からの距離の全上回りで `top`。順位は向きを考慮した `rank_oriented` と、対ごとに大きい方を取る `rank_pair` の両方を算出。
  - `iso_top_share`: 等方方向の中で、比べる相手の最大距離を厳密に上回る割合。論理に綻びはありません。

#### (5) 門（`gate`）
- **重さ**: 軽い（問題なしの確認）
- **根拠**: 正本 `gate`, `bl3_core.py` (L140–152), `analyze_Bl3.py` (L106–118)
- **確認内容**:
  - `blens_core.gate_perm` が「行の符号 $\times$ 家族の値」を計算する仕様に対し、`rs = [dict(r, sign=1) ...]` として符号を +1 に固定し、家族の値に「符号付きで足した効き目」を配置。二重掛けを防止しています（裁定 D226）。
  - 外された升目（`drop_cells`）の行を除外した後、行が存在しなくなった方向単位を入れ替えリスト `us` から除外。入れ替え数 `n_perm` は残った単位数の階乗で正しく計算されます。
  - 通過条件は $p < \text{alpha}$（0.05 を下回るとき・裁定 D226）。

#### (6) 乙の行（`readout.secondary`）
- **重さ**: 中くらい（確認結果: 正常だが留意あり）
- **根拠**: 正本 `readout.secondary.rows`, 裁定 D227, `analyze_Bl3.py` (L184–205), `bl3_run.py` (L409–430)
- **確認内容**:
  - 門の行のうち、名前のある方向および段階 B の 3 本のランダム方向で、土台升目が B-lens 層二の `selected` にある行を抽出。符号は門の行の符号（`r['sign']`）を継承。
  - `run_secondary` では、文脈ごとに符号でグループ化し、零ベクトルの無操作と同一バッチで流して差分を算出。
  - 読み取り集合における選択肢 c のインデックスとして `i_c = 2` がハードコードされています（`bl3_run.py` L423）。
    - 検算: `survival` は `['a', 'b', 'c']`、`nuclear` は `['a', 'b', 'c', 'd']` であり、どちらも 'c' は 0 始まりでインデックス 2。全升目において固定インデックス 2 で問題なく 'c' を指しています。

---

### 3. 合成データの確かめの盲点

合成データ器 `tools/dry_run_Bl3.py` は、設定を縮小した乱数模型（層 4, 隠れ次元 64, CPU, bf16）を用いてテストされています。開発ログ（`records/Bl3/tools/recompute-rewrite-dev-Bl3.md`）および試しの記録（`dry-trial-6-Bl3.md`）を踏まえ、本物の模型（Qwen3-4B-Instruct-2507: 層 36, 隠れ次元 2560, GPU L4/A100）へ移行した際に生じうる盲点を検討しました。

#### (1) 介入ベクトルの相対ノルムと飽和特性（記録にある点への補足）
- **背景**: 開発ログ §7 の 6 項で「小さな模型では合成方向のノルムが層の出力より二桁大きく、効き目が飽和して誤り変種が許容内に収まる盲点」が指摘され、正本の相対加減比（`layers.vhat_over_h` $\approx 0.0304$）に縮小した検証が追加されました（試しの記録 6）。
- **残る盲点**:
  - 本物の模型では隠れ層の次元が 2560 あり、残差ベクトルの自由度が 64 次元とは比較にならないほど高くなります。
  - 高次元空間では、直交するランダム方向を足した際の残差ノルムの増分比率や、Softmax / RMSNorm の感度が小さな模型とは異なります。
  - 小さな模型では「相対加減を小さくすると変種の差が拡大して検出できた」という結果が得られていますが、本物の重みは高度に構造化されており、中間層での活性伝播が非線形に減衰・増幅する可能性があります。

#### (2) CUDA 環境における SDPA（Scaled Dot-Product Attention）カーネル選択の非決定性
- **重さ**: 中くらい
- **盲点の内容**:
  - CPU 環境での PyTorch SDPA はシンプルな C++ 実装が使われますが、CUDA（L4/A100）上では、FlashAttention、Memory-Efficient Attention、Math カーネルの中からテンソルのアライメントや引数に応じて動的にカーネルが選択されます。
  - `bl3_recompute_rewrite.py` の開発記録で言及された通り、`use_cache=False` かつ `attention_mask=None` の場合と、明示的マスクが渡された場合で、SDPA が呼ぶ CUDA カーネルが分岐する可能性があります。
  - 異なる CUDA カーネル間では、浮動小数点積和演算（FMA）の順序が異なるため、同一の入力であっても bf16 レベルで数 ULP（最下位ビット）の差が生じます。
  - `boot_Bl3.py` では `use_cache=False` を渡して呼び出し方を揃えていますが、GPU 実機での一段目の突き合わせ（許容 0.001）において、カーネル差異による微小な数値揺れが生じないかは、本番の相 check / pilot の環境でしか完全に検証できません。

#### (3) 独立の再計算（一段目・二段目）の許容値と bf16 揺れの近接
- **重さ**: 中くらい
- **盲点の内容**:
  - 試しの記録 5・6（`tools-log-Bl3.md` §5）において、近道の確かめの差（約 3.77e-3）が近道許容（0.005）にかなり近接することが報告されています。
  - 二段目の許容値は「近道許容 + 揺れの床」（約 0.005 + $\text{floor}$）。
  - 本物の模型・GPU 環境において、バッチサイズ 16 とバッチサイズ 1 の演算精度の揺れ（cuBLAS のタイリングの違いなど）が合算された場合、二段目の差が許容値ギリギリになる、あるいは僅かに上回って `judge` が停止（不一致）するリスクが潜在的に残ります。
  - （※これは器の誤りではなく、正本 D219・D222 に従い「結果を開かずに止めて登録者に上げる」べき規定通りの挙動ですが、運用上の警戒点です）。

---

### 4. 凍結の前に直すべきもの vs 記録に置くもの

#### 【A】凍結の前に直すべきもの（推奨）

##### 1. `bl3_recompute_rewrite.py` の `recompute_rewrite` 関数のデフォルト引数 `use_cache`
- **重さ**: 中くらい〜軽い
- **根拠**: `tools/bl3_recompute_rewrite.py` (L291), `tools/colab/boot_Bl3.py` (L436)
- **内容**:
  `recompute_rewrite` 関数の定義は現在：
  `def recompute_rewrite(..., use_cache=None):`
  となっており、デフォルトでは `use_cache = getattr(cfg, 'use_cache', None)`（通常 True）が使われ、is_causal 経路（mask=None）に入ります。
  一方、`boot_Bl3.py` では：
  `out['rewrite'] = RW.recompute_rewrite(..., use_cache=False)`
  と明示的に `False` を渡してフック道（近道なし = `use_cache=False`）に揃えています。
  万が一、他のスクリプトや将来の呼び出しで引数を省略した場合に不一致を起こすリスクを排除するため、`bl3_recompute_rewrite.py` 側のデフォルト引数を `use_cache=False` に統一するか、キーワード引数を必須化（None を許容せず明示を求める）しておくことを推奨します。

##### 2. `bl3_run.py` 内の `shortcut_assert` のエラーメッセージ
- **重さ**: 軽い
- **根拠**: `tools/bl3_run.py` (L120)
- **内容**:
  `if pc['end'] != cell.mp:`
  `    raise ToolError('近道の元が主位置の手前で切れていない（%d・主位置 %d）: %s' % (pc['end'], cell.mp, cell.key))`
  正本 `computation.shortcut_assert` および裁定 D226 に完全に沿ったアサートですが、例外型が `ToolError` になっています。
  `boot_Bl3.py` 側で捕捉される例外（`TOOL_ERR`）に `BR.ToolError` が含まれているため正常にフェイルセーフが働きますが、正本の記述「assert で確かめる」に逐語的に合わせるならば、Python 標準の `AssertionError` を送出するか、`ToolError` のままであることを正本の `computation.shortcut_assert` に「器の ToolError として検知する」と注記しておくのが整合的です。

---

#### 【B】記録（限界・報告の注・逸脱台帳）に置けば足りるもの

##### 1. 系統内個体同士による二つの道の実装に関する限界
- **根拠**: 正本 `independent_recompute.who`, 裁定 D230
- **内容**: 本の器と再計算器の書き手がどちらも Claude 系であり、正本から同一の仕様理解を共有して実装したこと。二つの道が一致したとしても、正本の記述自体に内在する解釈の偏りや、プロンプト・書き出しのトークナイズ結合方式（トークンリスト結合）に対する前提の共有までは検証できないこと。これは報告書 §0 の「見ていない場所 / 限界」に明記することで学術的誠実性が担保されます。

##### 2. 乙の出力文字 'c' のインデックス（`i_c = 2`）の固定
- **根拠**: `tools/bl3_run.py` (L423)
- **内容**: `survival`, `nuclear` の両族において 'c' が 3 番目（インデックス 2）に位置することは凍結された場面仕様上不変ですが、将来的に別の選択肢体系が追加された場合には一般化できない実装です。層三の登録範囲内では完全に不変項であるため、コードの改変は不要であり、報告またはコード内コメントへの記録で十分です。

##### 3. GPU 実機における二段目の数値揺れと近道許容の近接リスク
- **根拠**: 正本 `pilot.checks.vi`, `independent_recompute.stages.second`, 開発ログ §5
- **内容**: 合成実験で見られたように、近道あり/なしの差が無操作の差分に現れる挙動により、実機でも二段目の差が `tol2` 付近に達する可能性があります。万一二段目が不一致となった場合は、裁定 D219・D222 に基づき「結果を開かずに停止し、逸脱台帳に記して登録者に上げる」運用を徹底することが報告記録の前提となります。

---

### 確認していないこと（必須開示項目）

本意見の作成にあたり、以下の事項については確認を行っていません：

1. **開いていないファイル・ディレクトリ**:
   - `prelim/` および `results/prelim-*`（依頼文の指示に従い、一切開いていません）。
   - 本物の重みファイル（`model.safetensors` 等の safetensors 実体）。
   - 段階 B の全走行ログの実データ（`results/stageB/` 配下の数万件に及ぶ生テキストの全量通読は行っていません）。
2. **実行・計算していないこと**:
   - 本物の Qwen3-4B-Instruct-2507 の重みを用いた順伝播・逆伝播・対数オッズ計算（予想封印前のため一切行っていません）。
   - GPU 実機（CUDA 環境）でのカーネル実行およびメモリプロファイリング（手元の静的解析およびコード検算のみを実施）。
   - 1999 本すべての等方方向を用いた全順伝播の再現計算。
3. **確認したファイル・関数**:
   - 第二部: 正本 v6 (`design/contrasts-Bl3.json`) の全文。
   - 第三部: 枠草案3 (`design-Bl3-draft3.md`), 凍結差分 (`frozen-diff-Bl3.md`), 設計事実 (`design-facts-Bl3.md`)。
   - 第四部: `bl3_run.py`（全関数: `Cell`, `Runner.__init__`, `vec`, `norm32`, `readout`, `prefix_cache`, `_expand`, `forward`, `logit_check`, `layer_check`, `run_pilot`, `cell_sign_sets`, `run_cell_sign`, `steered_cache_check`, `recompute_hook_path`, `build_cells`, `load_dirs`, `secondary_contexts`, `run_secondary`, `run_main_phase`, `layer_summary`）。
   - 第四部: `bl3_core.py`（全関数: `lse`, `log_odds_a`, `prob_a_in_set`, `mass_of_set`, `p_and_tail`, `holm`, `holm_limits`, `effect_side`, `second_label`, `iso_top_share`, `comparators_for`, `behavior_y`, `gate`, `vi_decision`, `cache_tol`, `spread`, `cells_decision`, `pass_i_ii`, `iii_sentence`, `variant_flags`, `shortcut_ok`, `q1_from_attempts`, `agreement`, `bucket`, `score_q7`, `recompute_set`, `batch_plan`, `_selftest`）。
   - 第四部: `boot_Bl3.py`（全コード: 環境検査、相 check, pilot, main の制御フロー）。
   - 第五部: `bl3_recompute_rewrite.py`（全関数: `check_env`, `assert_no_forward_hooks`, `check_layer_and_coef`, `cell_input`, `forward_rewrite`, `readout`, `_check_dirs`, `recompute_rewrite`, `_selftest`, `_dry`, `_mutant_diffs`）および開発記録。
   - 第六部: `analyze_Bl3.py`（全関数: `stage_b_gate_rows`, `row_labels`, `gates`, `prediction_truth`, `recompute_agreement`, `secondary_rows`, `secondary_counts`, `secondary_summary`, `judge`, `open_results`）。
   - 第六部: `dry_run_Bl3.py`（全コード）および試しの記録 6。
   - 第七部: `run_stageB_local.py`（該当部: `arm_texts`, `user_message`, `scenario_and_instruction`, `make_hook`, `register_hook`, `assert_no_hooks`, `assert_layer_alignment`）, `steer_B.py`（`random_directions`, `main_position`, `apply_chat`）, `direction_B.py`（`layer_index`, `hidden_states_index`, `decoder_layers`）, `blens_core.py`（`p_two_sided`, `p_equal_tailed`, `holm`, `top_rank`, `spearman`, `gate_perm`）。
   - 第八部: 器の段の記録 (`tools-log-Bl3.md`) および裁定記録 (`rulings-D226-D227.md`, `rulings-D228-D230.md`)。

---
本回答のいかなる記述・数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。