<!-- 逐語保全: 器についての意見伺い（登録者裁定 D230・巡に数えない）・系統外・二人目（呼び名 G2）。本文の中の機種の申告は「Gemini 2.5 Pro」。登録者の言葉では「Gemini 3.8 Flash 二名（いずれも、回答での申告は、「Gemini 1.5 Pro」「Gemini 2.5 Pro」となっていますが、モデル名はGemini 3.8 Flashが正しいです。Google AI Studio のモデル選択で私が確認済み）」（登録者の言葉は逐語・下の出所）。
     登録者（楠見優太）が会話で渡したご意見を、会話の記録から機械で切り出した（作業の途中に届いた形の登録者の言葉・uuid 374b0998-9303-456c-9a94-248e8fdfccc2・元の uuid ec487404-8a19-491e-8693-7403744d061a・2026-09-25 09:16 日本時間）。
     この枠の外は一字も変えていない。本意見のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->
### 系統と機種
- **系統**: 系統外（Google / Gemini 系）
- **機種**: Gemini 2.5 Pro（2026年9月時点の最新環境）

---

### はじめに
本意見伺いにおける制約（本物の模型で全経路の効き目を計算しないこと、結果の見込みを記載しないこと）を厳格に遵守し、提示されたコード、正本、設計事実、および過去の裁定記録に基づいて、静的コード解析および数式・制御フローの突き合わせを行いました。

以下、4つの伺いたい項目に沿って、気づいた点を重さ・根拠・確かめ方とともに報告します。

---

### 1. 二つの道が共有しうる読み違い

#### 【所見 1-1】logsumexp 計算時における浮動小数点精度の微小な差異（記録に関連する点）
- **重さ**: 軽微
- **根拠の置き場**:
  - 正本: `readout.primary.precision`（行 292）
  - 第四部: `tools/bl3_run.py` 行 86–87（`Runner.readout`）
  - 第五部: `tools/bl3_recompute_rewrite.py` 行 267（`readout`）
  - 第五部開発記録: `records/Bl3/tools/recompute-rewrite-dev-Bl3.md` §5
- **指摘内容**:
  正本 `readout.primary.precision` では「最後の層の出口の残差を `float32` に上げ、最終の正規化と、語彙の行列の読み取りの集合の行を `float32` で当てて出口の値を作る」と規定されていますが、その後の対数オッズ（`z_a - logsumexp(...)`）の算術精度については明記されていません。
  - 本の器（`bl3_run.py`）: 出口の値 `Zs` を `.double()` で float64 に変換した上で、`bl3_core.log_odds_a` 内で NumPy float64 の logsumexp を計算しています。
  - 書き換えの道（`bl3_recompute_rewrite.py`）: 出口の値 `z`（PyTorch float32）のまま `torch.logsumexp(z[1:], dim=0)` を計算し、その結果を Python float にキャストしています。
  この差により、第五部の開発記録で報告されている「効き目の差の最大 2.54e-07」が生じています。
- **確かめ方**:
  `z = np.array([2.0, 0.5, -1.0, 0.0], dtype=np.float32)` に対し、`torch.logsumexp`（float32）と `np.log(np.sum(np.exp(z.astype(np.float64))))` の差を取ると約 $10^{-7}$ オーダーの差が出ます。
- **評価**:
  一段目の合意許容値 `tol_stage1 = 0.001` に対して3〜4桁小さいため、一致判定に悪影響を与えることはありません。二つの道が同じ誤りを共有しているわけではなく、正本の曖昧さに起因する極小の精度差が正しく許容内に収まっている状態です。凍結前にコードを修正する必要はなく、記録に留めることで足ります。

#### 【所見 1-2】減算行における比べる相手の両向きの参照（問題なしの確認）
- **重さ**: 軽微（問題なし）
- **根拠の置き場**:
  - 第二部 正本: `labels.second`（行 723）、`nulls.real.orientation_rule`（行 691–692）
  - 第四部: `tools/bl3_run.py` 行 247–250（`cell_sign_sets`）
  - 第六部: `tools/analyze_Bl3.py` 行 78–89（`row_labels`）
- **確認内容**:
  減算の行（`sign = -1`）において、行自体の効き目 `e` は符号 `-1`（`key3(..., -1)`）で流した static の効き目 `lo(-v) - lo(0)` となり、比べる相手 `comps` は同じ升目の符号 `-1` の組 `same` と符号 `+1` の組 `opp` から構成されます。
  加算の行（`sign = +1`）では `same` と `opp` の順序が入れ替わりますが、`list(same) + list(opp)` の集合は同じ升目であれば完全に一致し、中央値 `center` も同一になります。また対単位の順位判定用ペア `list(zip(same, opp))` においても、対の値は `max(abs(a - center), abs(b - center))` であるため、`a` と `b` の順序入替に対して不変です。
  したがって、「比べる相手の集まりは升目ごとに一つで、符号に依らない（裁定 D213）」という正本の意図と完全に合致しており、二つの道の間で符号の向きや対の参照に関する共有の読み違いはありません。

#### 【所見 1-3】加減の帯の起点（主位置）と読み取り位置のスライス整合（問題なしの確認）
- **重さ**: 軽微（問題なし）
- **根拠の置き場**:
  - 第二部 正本: `readout.primary.band`（行 297）、`readout.primary.place`（行 293）
  - 第四部: `tools/bl3_run.py` 行 41–42, 115–123
  - 第五部: `tools/bl3_recompute_rewrite.py` 行 153–158, 239–240
- **確認内容**:
  トークン列は `ids = prompt + prefix` で構成され、`cell.mp = len(prompt) - 1`（主位置）です。
  - `bl3_run.py`（近道なし）: 系列長 `len(ids)` に対し `starts = [cell.mp]`。`make_hook` は `hs[i, cell.mp:, :]` に加算します。
  - `bl3_run.py`（近道あり）: 入力は `ids[cell.mp:]`（主位置トークン＋書き出し7トークン＝計8トークン）で `starts = [0]`。`hs[i, 0:, :]` に加算され、元の系列における主位置〜末尾までの8トークンすべてに加算されます。
  - `bl3_recompute_rewrite.py`: `h[0, int(mp):, :] = h[0, int(mp):, :] + add` により、インデックス `mp` から末尾まで加算されます。
  読み取り残差はいずれも最終位置（`[:, -1, :]`）から取得されており、フックの道（近道あり・なし）と残差書き換えの道の間で加算範囲・読み取り位置が完全に一致しています。

---

### 2. 独立の道の無い所

#### 【所見 2-1】独立の再計算（`agreement`）において無操作ベースライン値（`noop_lo`）自体の差が判定対象外となっている点
- **重さ**: 中くらい
- **根拠の置き場**:
  - 第二部 正本: `independent_recompute.what`（行 1145）、`independent_recompute.agreement`（行 1164–1165）
  - 第六部: `tools/analyze_Bl3.py` 行 164–165, 175–176（`recompute_agreement`）
  - 第四部: `tools/bl3_core.py` 行 218–227（`agreement`）
- **指摘内容**:
  正本 `independent_recompute.what` では「主の値の一部を計算し直す: v̂ の行ごとに、**無操作の値と**、v̂・等方の帰無のすべて・比べる相手のすべての効き目」と規定されており、各道（`recompute_hook_path` および `recompute_rewrite`）も辞書内に `'noop_lo'` を返しています。
  しかし、`analyze_Bl3.py` の `recompute_agreement` 内の `as_eff` 関数では、効き目（`effect`, `iso`, `comps_same`, `comps_opp`）のみをリストに結合して `K.agreement` に渡しており、`noop_lo` そのものの差が許容値 `tol`（一段目は 0.001、二段目は `tol2`）以内であるかどうかの検査が行われていません。
  正本 `independent_recompute.agreement` の本文が「全ての**効き目の差の絶対値**が許容の内で」と書かれているため、器の実装としては正本の `agreement` の文言通りですが、もし「無操作の値自体の再現性」も検証する意図があった場合、効き目（差分）の計算でベースラインのオフセットが相殺されてしまい、無操作値自体のズレを検知できません。
- **確かめ方**:
  `tools/analyze_Bl3.py` の `recompute_agreement` 内で、仮に `hook` の出力の `noop_lo` に +10.0、各方向の `effects` にそのままの値を設定した場合でも、`as_eff` は `effects` のみを取り出すため、`agreement` は通過してしまいます。
- **推奨処置**:
  正本 `agreement` の文言「全ての効き目の差の絶対値」を厳密に取るのであれば現在の器のままで問題ありません（記録・注記レベル）。ただし、`what` の「無操作の値と」を独立検証対象に含める意図であれば、凍結前の今、`as_eff` に `noop_lo` を含めるか、あるいは `noop_lo` の差分チェックを `agreement` に追加する必要があります。

#### 【所見 2-2】`prefix_cache`（近道）における `attention_mask` 未指定と GPU 環境依存性
- **重さ**: 中くらい
- **根拠の置き場**:
  - 第四部: `tools/bl3_run.py` 行 100, 133（`prefix_cache`, `forward`）
  - 第二部 正本: `pilot.checks.v`（行 347–350）、`computation.steered_cache_check`（行 782–785）
- **指摘内容**:
  `Runner.prefix_cache` および近道を使用した `Runner.forward` では、`self.model(...)` 呼び出し時に `attention_mask` を渡していません（`past_key_values` のみ指定）。
  単系列かつパディングなしの教師強制であるため、CPU 上の Transformers 4.57.3 では暗黙の causal mask 生成または SDPA 内部の処理によって正常に動作します。
  しかし、本番の GPU（Colab L4 / A100）かつ PyTorch 2.11+cu128 環境において、`past_key_values` が存在し `attention_mask=None` かつ `use_cache=True` のとき、SDPA のディスパッチ先カーネル（FlashAttention-2 または CuDNN / Math カーネル）によっては、過去キャッシュに対するマスク解釈やアライメントに関して微小な差異や警告が発生する懸念があります。
- **確かめ方**:
  Colab 環境（相 check または相 pilot）において、近道ありと近道なしの差分が下見の (v)（`pilot.checks.v`）および `steered_cache_check` で測定されます。
- **評価**:
  この点については、差が許容 `cache_tol` を超えた場合に自動的に「近道を使わない（`shortcut = False`）」に倒すフォールバック（正本 `pilot.checks.v`「一つの升目でも許容の外なら、本の計算は全ての升目で近道を使わない」）が器に正しく実装されているため、致命的な破綻を防ぐ安全弁が存在します。凍結前のコード修正は不要であり、下見の (v) の結果を見守ることで足ります。

#### 【所見 2-3】下見（pilot）決定木・門（gate）の升目除外処理（問題なしの確認）
- **重さ**: 軽微（問題なし）
- **根拠の置き場**:
  - 第二部 正本: `pilot.decision`（行 385–397）、`gate.dropped`（行 751）
  - 第四部: `tools/bl3_core.py` 行 140–151（`gate`）、行 172–183（`cells_decision`）
  - 第六部: `tools/analyze_Bl3.py` 行 77–78, 106–117
- **確認内容**:
  下見で (i)(ii) を満たさず除外された升目（`dropped_cells`）が生じた場合、
  1. 主の行の継続判定（`cells_decision`）において、門専用升目（`pass_gate_only`）の成否は `cells_min_pass` のカウントから正確に除外されています。
  2. 除外升目に関連する行は `row_labels` から除外され、Holm の段数分母（`m_rows`）が正確に残存行数で再計算されます。
  3. 門（`gate`）においても、除外升目の行が除かれ、全行が消失した方向単位（unit）は並べ替え集合 `us` から除外され、入れ替え数 `n_perm` が `len(us)!` で縮小計算されます。
  4. 予想項目の `q4`, `q5` も門の行が残らない場合は `None`（判定不能・採点除外）となります。
  これらは正本の複雑な条件分岐を完全に網羅しており、実装の逸脱はありません。

---

### 3. 合成データの確かめの盲点

合成データの器（第六部 `tools/dry_run_Bl3.py`）は、登録機種のアーキテクチャを模した極小モデル（`hidden_size=64`, `layers=4`）を用いて CPU 上で動作確認を行っています。
第六部の試しの記録（`dry-trial-6`）では、注入量を実モデルの相対比率（$0.0608$）に合わせた記述的確認も追加されています。
しかし、合成モデルの全テストを通過しても、本物の模型（Qwen3-4B-Instruct-2507）の上で結果を変えうる盲点として、以下の構造的差異が残り得ます。

1. **実モデルの残差空間における強い異方性（Anisotropy）と特異次元（Outlier Dimensions）**:
   乱数モデルでは各隠れ次元が独立同分布（i.i.d.）のガウス分布に従いますが、実際の事前学習済み LLM の残差ストリームには、特定の少数の次元が極端に大きなノルムを持つ「特異次元」が存在することが知られています。
   等方のランダム方向（1999本）は球面上に等方的に分布するため、特異次元とわずかに重なるか直交するかによって、出力ロジットに与える影響の分散が実モデルでは極端に増大する可能性があります。合成モデルではこの異方性が存在しないため、実モデルにおける等方帰無分布の裾の広がりや非対称性を合成テストから予測することはできません。
2. **語彙サイズ（15万語）と稀少トークンのロジット**:
   合成モデルでは語彙サイズが極小化されていますが、実モデルでは語彙サイズが 151,936 です。
   下見の (i)（`mass_min` の質量検査）において、読み取り集合（a, b, c, d, ref）以外の全語彙に対する softmax の合計質量を計算する際、15万語のロジット総和の計算において、実モデルでは語彙のロングテール部分の確率質量が無視できない大きさを持つ可能性があります。
3. **GPU 上の bf16 GEMM 累積順序による非決定性とバッチ効果**:
   合成テストは CPU 上の float/bf16 演算で実行されていますが、本番の GPU（L4 / A100）では、バッチサイズ 16 のときとバッチサイズ 1 のときで、CUDA コア内部のテンソル積の縮約・累積順序が並列度に応じて動的に変化します。
   このハードウェア依存の丸め誤差は、合成テストで観測された CPU の揺れ（`1e-6` オーダー）よりも大きく現れる可能性があり、下見の (vi) の数値の揺れや近道の差分判定において、実機特有の分散として顕在化する可能性があります。

---

### 4. 凍結の前に直すべきもの vs 記録で足りるもの

#### A. 凍結の前に直すか検討すべきもの（登録者判断が必要な点）
- **所見 2-1（独立の再計算における `noop_lo` の合意判定対象化）**:
  もし登録者が「無操作のベースライン値自体の絶対的一致」も一段目・二段目の合意条件として厳密に求める意図であれば、`tools/analyze_Bl3.py` の `recompute_agreement` 内の `as_eff` に `noop_lo` を含める修正が必要です。
  現行の正本 `independent_recompute.agreement`（「全ての効き目の差の絶対値が許容の内で」）を厳密に字義通り解釈するのであれば現行コードで完全合致しているため、直さずに「合意判定は差分（効き目）で行う」ことを記録に明記するだけでも論理的一貫性は保たれます。

#### B. 記録（注記・限界）に置けば足りるもの
- **所見 1-1（logsumexp の fp32 vs fp64 の算術精度）**:
  二つの道の間で生じる $10^{-7}$ 程度の差は一段目許容（0.001）より十分に小さく、判定に影響を与えないため、報告書の数値精度の注記として記録すれば足ります。
- **所見 2-2（近道における過去キャッシュと SDPA の挙動）**:
  下見 (v) および `steered_cache_check` の自動フォールバックが機能するため、コード修正は不要です。近道がオフになった場合はその事実と理由を報告に記せば足ります。
- **所見 3-1〜3-3（合成データの盲点と実モデルの幾何構造の違い）**:
  すでに正本 `limits` に「等方のランダム方向は低い棒」「機種は一つ」などの限界が置かれていますが、実機と合成モデルの幾何的・ハードウェア的な差異については、報告の注記・限界欄に位置づけることで十分です。

---

### 確認していないこと

- **本物の模型重み（Qwen3-4B-Instruct-2507）を用いた順伝播・効き目の計算**:
  依頼文の指示（「予想の封印前であるため全経路の効き目を計算しないこと」「結果の見込みを書かないこと」）を厳格に守り、本物の重みを用いた実行および結果の予測・見込みの算出は一切行っていません。
- **指示された非公開ディレクトリ**:
  `prelim/` および `results/prelim-*` は指示通り開いていません。
- **GPU（CUDA 12.8 / L4・A100）上での実機動作**:
  実機 GPU 環境における PyTorch 2.11 + CUDA 12.8 の低水準カーネル（FlashAttention / CuDNN）の挙動は、静的コード解析と仕様確認にとどまり、実機でのプロファイリングは行っていません。
- **ファイルの物理ハッシュの照合**:
  提示されたテキスト束に記載されている SHA-256 / SHA-16 の文字列整合性を追跡したものであり、独立した Git リポジトリからの SHA 計算は行っていません。

### 査読したファイル・関数一覧
- **第二部**: `design/contrasts-Bl3.json`（全文）
- **第三部**: `design/design-Bl3-draft3.md`、`records/Bl3/frozen-diff-Bl3.md`、`records/Bl3/design-facts-Bl3.md`
- **第四部**: `tools/bl3_run.py`（`Runner` クラス、`run_pilot`, `cell_sign_sets`, `run_cell_sign`, `steered_cache_check`, `recompute_hook_path`, `build_cells`, `secondary_contexts`, `run_secondary`, `run_main_phase`）
- **第四部**: `tools/bl3_core.py`（`log_odds_a`, `prob_a_in_set`, `mass_of_set`, `p_and_tail`, `holm`, `effect_side`, `second_label`, `iso_top_share`, `comparators_for`, `gate`, `vi_decision`, `cache_tol`, `cells_decision`, `q1_from_attempts`, `agreement`, `score_q7`, `recompute_set`, `batch_plan`）
- **第四部**: `tools/colab/boot_Bl3.py`（相 `check`, `pilot`, `main` の制御フロー、`verify_frozen`, `run`）
- **第五部**: `tools/bl3_recompute_rewrite.py`（`check_env`, `assert_no_forward_hooks`, `check_layer_and_coef`, `cell_input`, `forward_rewrite`, `readout`, `recompute_rewrite`, `_selftest`, `_dry`, `_mutant_diffs`）、`records/Bl3/tools/recompute-rewrite-dev-Bl3.md`（全文）
- **第六部**: `tools/analyze_Bl3.py`（`stage_b_gate_rows`, `row_labels`, `gates`, `prediction_truth`, `q7_rows_of`, `recompute_agreement`, `secondary_rows`, `secondary_summary`, `descriptive`, `judge`, `open_results`）
- **第六部**: `tools/dry_run_Bl3.py`（`part_pure`, `tiny_model`, `calibrate_readout_rows`, `part_model`）、`records/Bl3/tools/trials/dry-trial-6-Bl3.md`
- **第七部**: `tools/run_stageB_local.py`（`user_message`, `make_hook`, `register_hook`, `assert_no_hooks`）、`tools/steer_B.py`（`random_directions`, `main_position`, `apply_chat`）、`tools/direction_B.py`（`layer_index`, `hidden_states_index`, `decoder_layers`）、`tools/blens_core.py`（`gate_perm`, `top_rank`, `holm`, `spearman`）、`tools/colab/boot_Blens.py`（`context_of`）
- **第八部**: `records/Bl3/tools/tools-log-Bl3.md`、`records/Bl3/rulings-D226-D227.md`、`records/Bl3/rulings-D228-D230.md`