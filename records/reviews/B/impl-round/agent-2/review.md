検分が一通り終わりました。以下が検分票の全文です。

---

# 段階 B 器材の実装検分票（担当: 二体目・GPU 側の規則／封印と盲検／合成データの偏り）

- 検分者: 系統内の新規個体（Claude Opus 5・起草者と同一系列・裁定 D59 により claude.ai の票と合わせて一票）
- 対象: `C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b` の器材のうち、`direction_B.py`・`steer_B.py`・`run_stageB_local.py`・`synth_B.py`・`dry_run_B.py`・`sample_inspection_B.py`・`build_report_B.py`・`freeze_B.py`
- 正本: `C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b\design\contrasts-B.json`（SHA16 3EC6E04F17DBD485・実測一致）／草案9B（3C2070041C5084EF・実測一致）
- やったこと: 行単位の読み／三つの `--selftest` の実行／一時置き場での合成データ生成と門・集計・報告・凍結・抽出検査の再走行／`transformers` 4.57.3 と `torch` 2.9.1+cpu で hook・決定性・生成設定の実挙動を再現／合成データに壊れ方を注入した対照実験。リポジトリへの書き込みは一切していない。

**判定: 差し戻し**

---

## 0. 先に一行で

自己検査は三本とも通る。しかし**通る自己検査が、規則の「半分ずつ」しか見ていない**。ノルム合わせと加減の向きは別々に検査され、**合成したときに係数が二度掛かる**ことは誰も見ていない。同じ型が帯の起点・決定性・盲検・合成データの印にも出ている。

---

## 1. 重大

### 重大1. ランダム方向に係数が二度掛かる（裁定 D75 の「ノルム一致」が、選ばれた係数では成り立たない）

- (a) 何が: `random_directions` は**係数を掛けた後の v̂ のノルム**（＝coef·‖v̂‖）に合わせたベクトルを返す。ところが唯一の hook 構成子 `make_hook` と `apply_vector` は、渡されたベクトルに**必ず coef を掛ける**。ランダム方向をそのまま渡すと加わる量は coef²·‖v̂‖ になる。
- (b) どこで:
  - `C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b\tools\steer_B.py:41`　`target = coef * float(np.linalg.norm(v_hat))`
  - 同 `:43`　`out.append(g * (target / n) if n else g)`
  - 同 `:56`　`return h + sign * coef * np.asarray(v_hat)`
  - `C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b\tools\run_stageB_local.py:102`　`hs[:, start_idx:, :] = hs[:, start_idx:, :] + sign * coef * v`
- (c) なぜ問題か: 実測（一時置き場で再現）——‖v̂‖=5 のとき、hook で加わる量は

  | 係数 | 静的 v 腕 | ランダム腕 | 比 |
  |---|---|---|---|
  | 0.5 | 2.50 | 1.25 | 0.50 |
  | 1.0 | 5.00 | 5.00 | 1.00 |
  | 2.0 | 10.00 | 20.00 | 2.00 |

  **係数 1.0 のときだけ偶然一致する。** 確証族の対比は「v 対**ノルム一致**ランダム方向」であり（草案9B:23・:50、正本 `random_control.norm_matched`）、この一致が崩れると、対比は「方向の違い」ではなく「介入の強さの違い」を測る。しかも選定は調整走行で係数を選ぶ規則なので、**係数 0.5 の候補は統制が弱く（差が出やすく）、係数 2.0 の候補は統制が強い（差が逆向きに出る）**。選定規則そのものが、方向の効き目と無関係な理由で 0.5 に引かれる。九候補のうち六候補（層 3 × 係数 {0.5, 2.0}）が汚染される。
  正本の文言が二通りあること自体が原因である——`selection.candidates.coefficient_ref`「同じノルムに合わせて**から**係数を掛ける」と `random_control.norm_reference`「**係数を掛けた後の** v̂ のノルムに合わせる」。器はその両方を同時に実装した。
- (d) 直し方: どちらか一方に正本を一本化し、器で強制する。推奨は「`random_directions` は ‖v̂‖（係数抜き）に合わせたベクトルを返し、係数は hook が一度だけ掛ける」——`steer_B.py:41` を `target = float(np.linalg.norm(v_hat))` にし、関数名を `unit_matched_random_directions` に変える。あわせて自己検査に**合成の検査**を足す: `assert np.isclose(norm(apply_vector(0, rand, coef, +1)), norm(apply_vector(0, v_hat, coef, +1)))` を全係数 × 全層で回す。これが無かったことが本件を通した。

### 重大2. 介入の帯の起点が「場面本文の開始位置」ではなく「プロンプトの終わり」になっている

- (a) 何が: 正本 `selection.apply`・`runner.prompt_assembly`（裁定 D87）は、帯の起点を**組み立ての式の「場面の本文」の開始位置**と定める。器の `band_slice` は `prompt_len`（プロンプト全体の長さ）から始める。
- (b) どこで: `...\tools\steer_B.py:59-61`

  ```python
  def band_slice(prompt_len, total_len):
      """介入の帯（場面本文の開始位置から EOS まで）。左詰めの場合、帯は生成の側にも掛かる。"""
      return slice(prompt_len, total_len)
  ```
- (c) なぜ問題か: この帯では前置きにも**場面の本文にも**介入が掛からず、生成した応答にだけ掛かる。登録した実験と別の実験になる。docstring の後半「帯は生成の側にも掛かる」は、起点をプロンプトの末尾と考えていることを示しており、単なる引数名の誤りとは読めない。さらに決定的なのは、**場面本文の開始トークンの添字を計算する関数がリポジトリのどこにも無い**（`grep band_slice|start_idx` の結果、生成側の使用箇所は零）。左詰めのバッチでは、その添字は詰めの長さぶん行ごとにずれるので、`make_hook` が受け取るスカラ一つでは足りない——同じ腕 × 同じ場面だけでバッチを組むという縛りが要るが、その縛りは正本にも器にも無い（`runner.batch: 16`・本走行の manifest は `arms` を複数持つ）。
- (d) 直し方: (i) `band_slice` を廃し、`scenario_start_index(tokenizer, arm_text, scen_text)` を作って、組み立て式の前半（前置き ＋ 空行）のトークン数から起点を出す。(ii) 左詰めの詰め長を行ごとに足した**行ごとの起点**を hook に渡す（`hs[i, s_i:, :]`）。(iii) 「一バッチは一セル」を正本に登録するか、(ii) を実装する。(iv) 自己検査で、腕 O と腕 N について起点トークンを復号して印字し、それが場面本文の先頭語であることを assert する。

### 重大3. hook は生成中に一度も発火しない（KV キャッシュのある復号では空スライスになる）

- (a) 何が: `hs[:, start_idx:, :]` は、prefill のときだけ長さのあるスライスになる。以後の復号ステップでは hidden_states の長さが 1 なので、start_idx ≥ 1 のとき**スライスが空になり、加算が起きない**。
- (b) どこで: `...\tools\run_stageB_local.py:102`
- (c) なぜ問題か: 正本は「場面本文の開始位置から **EOS まで**」と定める。実機で走らせるとプロンプト側にしか介入が入らない。自分の手元で再現した（transformers 4.57.3・`LlamaForCausalLM` をランダム初期化して `generate(max_new_tokens=6, use_cache=True)`）:

  | hook が受け取った形 | 加算できたか |
  |---|---|
  | (2, 12, 32) ＝ prefill | はい |
  | (2, 1, 32) × 6 ＝ 生成の各段 | **いいえ（六回とも）** |

  重大2 と重ねると、現状の実装は「前置きと場面本文には掛からない・生成にも掛からない」＝**どこにも掛からない**。
- (d) 直し方: hook を `if hs.shape[1] == 1: hs[:] = hs + sign*coef*v` と `else:` の二分岐にする（復号段は全位置＝その一トークンに掛ける）。または `past_key_values` の長さから絶対位置を復元して判定する。自己検査に、上で私が書いたのと同じ「小さなランダム初期化モデルで `generate` を回し、生成段でも加算が起きたことを数える」検査を入れる（CPU で数秒・GPU 不要）。**この検査が無いことが、GPU が無いから確かめられないという理由の実際の中身である——確かめられる。**

### 重大4. 決定性の検査は、規定どおりに走らせると必ず不合格になる

- (a) 何が: 正本 `activation_storage.determinism` は「主位置の活性を**バッチの並べ方を変えて**二度保存し、**完全一致（bitwise）**」を要求し、`on_fail` は走行の停止。器はそのとおり `np.array_equal` で実装している。
- (b) どこで: `...\tools\direction_B.py:81-84`（`determinism_ok`）／正本の当該条は草案9B:89。
- (c) なぜ問題か: バッチの並べ方を変えると、詰めの長さと行列積のタイル分割が変わり、丸めの順が変わる。同一の数学的結果が bitwise で一致することはまずない。手元の CPU で再現した（ランダム初期化 Llama・同じ行を「単独」と「長い行を足した左詰め二行バッチ」で通し、層 3 の最終位置を比較）:

  | dtype | bitwise 一致 | 最大差 | 一致しない成分 |
  |---|---|---|---|
  | float32 | **いいえ** | 1.34e-07 | 243/256 |
  | bfloat16 | **いいえ** | 1.95e-03 | 177/256 |

  GPU の bf16 ではこれ以上に離れる。つまり手順の第 2 段（方向の抽出）で毎回停止し、登録者に上がる。この検査は二つの別の問いを一つに畳んでいる——(i) 同じ条件で二度走らせて再現するか（bitwise が妥当）、(ii) 抽出した活性がバッチの並べ方に依らないか（bitwise は不可能・許容幅が要る）。
- (d) 直し方: 正本を二条に割る。(i) **同じ並べ方**で二度 → bitwise 一致（これは止める条件でよい）。(ii) **並べ方を変えて**一度 → 許容幅（たとえば `cos ≥ 1−1e-3` かつ `max|Δ| / ‖h‖ ≤ 1e-2`）を**データを見る前に登録**し、外れたら記帳して登録者に上げる。器の `determinism_ok` に `tolerance` 引数を足し、(i) と (ii) を別名の関数にする。**この変更は凍結前でなければできない**（凍結後は逸脱になる）。

### 重大5. 報告の組み立て器が、合成データの印を落とす

- (a) 何が: `analyze_B` は集計 json に `dry_marks: ["manifest.dry_run","manifest.model","trials.dry_run"]` を書く。`build_report_B` は**この欄を一度も読まない**。
- (b) どこで: `...\tools\build_report_B.py`（全体・`A['dry_marks']` の参照が無い）／印を作っている側は `...\tools\runs_B.py:60-67`。
- (c) なぜ問題か: 私が一時置き場で、100% 合成の stub データから組み上げた報告には、`dry`・`合成`・`stub` のいずれの語も現れない。本文はこう始まる——「確証の族 16 対比のうち、確証 3・判定不能（検閲） 1……」「門1: ……選んだ組は 層 0.5・係数 1.0」「S4 の反証: 下がった（封印は外れ）」。**本物の結果報告と見分けがつかない。** 走行の記録の区画も「整合検査:（記録が渡されていない）」と書くだけで止まらない。記録先行公開の束の中で、雛形と合成の予行と本番の報告が同じ置き場に並ぶことを考えると、この一件は取り違えの直接の道である。
- (d) 直し方: `build_report_B` の冒頭で `if A.get('dry_marks') and not a.allow_dry: sys.exit(...)` とし、`--allow-dry` を付けたときは**すべての機械の区画の先頭に「合成データ・本番ではない」の一行を差し込む**（区画ごと。冒頭一行だけだと切り出しで落ちる）。あわせて `--integrity` と `--sampling` を必須にする（下の中12）。

### 重大6. 抽出検査の標識が整列順のまま振られる——盲検が読めてしまう（段階 A の登録者裁定 D25 からの退行）

- (a) 何が: 標識 `X001…` は、セルを（場面, 腕）で整列した順に**そのまま連番**で振られる。並べ替えが無い。
- (b) どこで:
  - `...\tools\sample_inspection_B.py:90`　`pick_cells = [cells[i] for i in sorted(rng.choice(...))]`（無作為に選んだ後に**整列し直している**）
  - 同 `:96`　`label = 'X%03d' % (len(items) + 1)`
  - 比較: `...\tools\sample_inspection_A.py:77`　`rng.shuffle(rows)   # 並びから機種・場面・腕が読めないよう、印字の順を乱数で決める（登録者裁定 D25）`
- (c) なぜ問題か: 実際に走らせた対応表（合成データ・14 件）:

  ```
  X001 N1 O-Ncold      X005 N1 Onull+v      X009 S4 O-Ncold        X012 SK O-Ncold+vrand
  X002 N1 O-Ncold-vrand X006 N1 Onull+vNk   X010 S4 O-Ncold+vrand  X013 SK O-Ncold-v
  X003 N1 O-vrand      X007 N1 Onull+vrand  X011 S4 Osec-Ncold+vrand X014 SK Onull+vNk
  X004 N1 Onull        X008 S1 Onull+vrand
  ```

  場面の切れ目（X007/X008/X011）が標識の順に出ており、各場面の内側では腕がアルファベット順に並ぶ。腕 × 場面の一覧は正本で公開されている（`arms.by_scenario`）から、目視する者は標識列が公開の 55 セル列の**単調増加部分列**であることを使って、各標識の腕を数語まで絞れる。器材の口上（`sample_inspection_B.py:5,8`）は「腕と場面を伏せた標識」と書くが、伏せていない。
- (d) 直し方: `:92` の直前に `rng.shuffle(pick_items)` を入れ、標識は並べ替えた**後**に振る（段階 A の 77 行と同じ）。あわせて、対応表に `order_seed` を記帳し、自己検査（現在この器には自己検査が無い・段階 A には `:154` にある）で「標識の順と (場面, 腕) の整列順の順位相関が有意でない」ことを確かめる。

### 重大7. 対応表の置き場が「公開の置き場の外」かの判定が、Windows で素通りする

- (a) 何が: 置き場の判定が `str.startswith` の前方一致で、大文字小文字を畳んでいない。
- (b) どこで: `...\tools\sample_inspection_B.py:37`　`if os.path.abspath(a.keydir).startswith(os.path.abspath(REPO)):`
- (c) なぜ問題か: 実測（判定式だけを取り出して評価・ツールは走らせていない）:

  | 与えた置き場 | 止まるか |
  |---|---|
  | `C:\...\ontology-preamble-4b\keys`（そのままの綴り） | 止まる |
  | `c:\users\pc\desktop\github-repositories\ontology-preamble-4b\keys`（小文字） | **止まらない** |
  | `c:\Users\PC\...\ontology-preamble-4b\keys`（ドライブだけ小文字） | **止まらない** |
  | `C:\...\ontology-preamble-4b-keys`（外にある兄弟） | 止まる（誤って拒む） |

  Windows では `c:` と打つだけで素通りする。そして `.gitignore` は `results/_dryrun/`・`results/_smoke/`・`__pycache__/`・`*.pyc`・`.env*`・`results/**/*.tmp` だけで、**`keys` に相当する除外が無い**。つまり素通りした対応表（標識 → trial_id・場面・腕）は公開リポジトリの中に書かれ、`git add -A` で公開されうる。なお正しい書き方は同じリポジトリの中に既にある——`...\tools\run_preamble_local.py:217` は `os.path.commonpath` を使っている。
- (d) 直し方: `:37` を

  ```python
  k = os.path.normcase(os.path.realpath(a.keydir)); r = os.path.normcase(os.path.realpath(REPO))
  if k == r or os.path.commonpath([k, r]) == r: sys.exit(...)
  ```
  に置き換える（`realpath` は接合点・短縮名も畳む）。あわせて `.gitignore` に対応表の名の型を足す。

### 重大8. `freeze_B` は、S4 の封印が無く・記帳の値が全部 null でも「凍結した」と言う

- (a) 何が: 記帳の値は**鍵の有無しか見ず**（値が null でも合格）、封印は**確証 16 対比の符号しか見ない**（`seal_format.scope` が定める S4 の反証の封印が無くても止まらない）。
- (b) どこで:
  - `...\tools\freeze_B.py:62`　`missing_values = [k for k in NEED_VALUES if k not in VALUES]`
  - 同 `:65`　`missing_seal = [] if not SEAL else [i for i in conf_ids if i not in (SEAL.get('signs') or {})]`（`conf_ids` は `families` の対比のみ）
  - 同 `:102`　S4 は `'**まだ無い**'` と印字するだけで `blockers` に入らない
- (c) なぜ問題か: 一時置き場で実測した。
  - (1) 封印も値も無い → **止まる**（rc=1・要求どおり）。
  - (2) 16 対比の符号だけ入れ、S4 の封印を欠き、12 個の記帳の値を**すべて null** にした → `止めているもの 0 件`・**rc=0**・記録本文は「**凍結した。**」・その下に `- model_rev: null`・`- num_hidden_layers: null`・`- S4 の反証: **まだ無い**` が並ぶ。

  総層数・層の添字・腕のトークン長・v̂ の SHA・品質床の課題——凍結の意味そのものが null のまま「凍結した」の判に通る。S4 の反証は、正本 `seal_format.scope` が封印の対象と明記しているのに、抜けても止まらない。
- (d) 直し方: `:62` を `if k not in VALUES or VALUES[k] in (None, '', [], {})` にする。`:65` の後に `if not (SEAL or {}).get('s4'): blockers.append('S4 の反証の封印が無い')` を足す。あわせて封印ファイル自身の SHA-256 を `frozen` に記帳し、`seal_format.fields`（情報状態・時機・封印した者）の欄の有無も検査する。

---

## 2. 中

### 中1. 層番号の規則が「四捨五入」でない／総層数を記帳しない／層の添字と hidden_states の添字の変換がどこにも無い
- (b) `...\tools\direction_B.py:34`（`int(round(ratio * n_layers)) - 1`）・`:135-136`・`:142`
- (c) Python の `round` は偶数丸めで、正本 `selection.candidates.layer_index_rule` の「四捨五入」ではない。実測: 総層数 34 なら割合 0.25 で器は 7、四捨五入なら 8。42 なら器は 9、四捨五入なら 10。登録機種 Qwen3-4B の総層数が 36 なら三つとも整数になり影響しないが、規則は「総層数は config から読む」と一般に書かれており、予備機や機種替えで一つずれる。さらに、正本が「hidden_states の添字ではなく**層の添字**」とわざわざ書いている変換（embedding の分の +1）を実装した箇所も、assert も無い。`n_layers` は `:142` で印字するだけで、`layer_index_rule` が要求する**記帳**（ファイルへの書き出し）が無い。自己検査 `:90` は `assert layer_index(0.25, n) == int(round(0.25*n)) - 1` ——実装を実装で確かめる同語反復なので、この誤りは構造上捕まえられない。
- (d) `int(math.floor(ratio * n_layers + 0.5)) - 1` にする。`0 <= idx < n_layers` を assert する。`hidden_states` から取る箇所には `hs_index = layer_index + 1` の定数と一行の注を置く。`n_layers`・`idxs` を `out_dir/layers.json` に書き出し、`freeze_B` の `num_hidden_layers`・`layer_indices` がそこから来るようにする。自己検査の第一行は、実装を呼ばない期待値表（`{(0.25,36):8, (0.5,36):17, (0.75,36):26, (0.25,34):8, ...}`）に置き換える。

### 中2. ランダム方向の基準が「静的 v̂」である保証が器に無い（裁定 D75 の核が守られていない）
- (b) `...\tools\steer_B.py:28`（`random_directions(v_hat, ...)` は渡された何でも受ける）
- (c) 正本 `random_control.norm_reference` と草案9B:155 は「交差族・S4 の反証・腕対の差方向の統制の相手は、いずれも **v̂〔static〕のノルム**に合わせたランダム方向である。**Nk のノルムに合わせた統制ではない**」と明記する。ところが走行器側で腕ごとに方向を引く自然な書き方（`dirs[(kind, ratio)]` を渡す）をすると、交差族の相手は Nk のノルムになる。D75 が廃したはずの「二つの基準」が別の扉から戻る。`build_directions` は td だけノルムを合わせ、Nk と (6b) は合わせない（`...\tools\direction_B.py:66-68`）——これは正本どおりだが、**そのぶん「係数 1.0」の物理的な大きさが腕ごとに違う**という事実を器も報告も印字しない。
- (d) `random_directions` の第一引数を `v_hat_static` に改名し、`assert np.allclose(v_hat_static, DIRS_STATIC[ratio])` を置くか、モジュール内に凍結した静的 v̂ を持たせて引数から外す。要約統計に `‖v_Nk‖/‖v̂‖`・`‖v_6b‖/‖v̂‖` を足し、報告の族ごとの結論に印字する。

### 中3. ランダム方向の子ストリームが「層 × 係数」で分かれる（正本は `per_layer`）
- (b) `...\tools\steer_B.py:36`　`ss = np.random.SeedSequence([seed, int(round(layer_ratio*1000)), int(round(coef*1000))])`
- (c) 正本 `random_control` は `count: 3`・`per_layer: true` で、係数ごとに引き直すとは書いていない。係数ごとに別の三本になると、九候補は「同じ三方向を三つの強さで見る」ではなく「九つの別々の三方向」になり、係数の掃引が方向の同一性と交絡する。`pooling`（三方向の率を先に印字して二項の等質性を見る）で、同じ `direction_id` を係数を跨いで追えない。
- (d) 係数を SeedSequence から外す（`[seed, layer_key]` のみ）。係数ごとに引き直すのが意図なら、正本 `random_control` にその一句を足してから実装する。あわせて `direction_id` を `rand:<phase>:<layer>:<i>` の形で決定的に作る関数を置き、`trial_record` の `direction_id`・`seed` を実際に埋める（現状、両欄を作る器が無い）。

### 中4. 生成の設定の辞書が `generate` に渡せない・`max_tokens` の名が違う
- (b) `...\tools\steer_B.py:64-68`（`quality_generation`）・`:71-74`（`main_generation`）
- (c) 実測（transformers 4.57.3）: `generate(**quality_generation())` → `ValueError: The following model_kwargs are not used by the model: ['note']`／`generate(**main_generation())` → 同 `['max_tokens','thinking','applies_to','source']`。正本の説明文ごと辞書を返しているため。`max_tokens` は transformers では `max_new_tokens`。加えて `quality_generation` は `do_sample` を `bool(temperature)` から導く（`:68`）ので、誰かが温度を書き換えると裁定 D78 の「貪欲」が黙って外れる。
- (d) 生成の設定を transformers の引数名に写す薄い変換関数を置き（説明欄は落とす）、`assert T['quality_floor']['generation']['temperature'] == 0` を貪欲の根拠として明示する。自己検査に「小さなランダム初期化モデルに実際に渡して例外が出ないこと」を足す（GPU 不要）。

### 中5. 「指示」の本文の供給元が器に無い
- (b) `...\tools\run_stageB_local.py:73-76`（`user_message(arm_text, scen_text, instruction)` の第三引数）・`:65-70`（`scenario_text` は場面の辞書しか返さない）
- (c) 凍結走行器は `...\tools\run_preamble_local.py:143` で `INST = d['json_instruction'][FAM]` と引いている。B は `json_instruction` に一度も触れない。指示文は書式（JSON 直答）を決めるので、一字違えば書式外率が動き、希釈の門と様式門の入力が変わる。自己検査は `'\n指示'` というダミーを渡すので（`:126`）、この欠落は検査を素通りする。
- (d) `scenario_text` を `scenario_and_instruction(scenario)` に変え、`json_instruction[family]` を同じ凍結素材から返す。自己検査で、腕 O × 場面 N1 の組み立て結果の SHA16 を印字して凍結時に記帳する。

### 中6. 組み立ての照合は「文字列定数が凍結走行器の中にあるか」しか見ていない
- (b) `...\tools\run_stageB_local.py:29`・`:32-40`
- (c) `ASSEMBLY_EXPR` が凍結走行器のソースに含まれることは確かめるが、**B 自身の `user_message`（`:73-76`）がその式どおりに振る舞うことは確かめない**。B の実装だけを書き換えても検査は通る。`check_assembly_matches_frozen` は凍結走行器の SHA16 を返すが（`:40`）、**誰もそれを登録値と突き合わせない**（`freeze_B` の凍結物一覧にも入っていない・下の中13）。
- (d) 凍結走行器を `importlib` で読み込んで（`--arms/--scenario` の副作用があるなら該当関数だけを `ast` で抜き出して）、B の `user_message` と**同じ入力で同じ出力になること**を assert する。凍結走行器の SHA16 を正本 `carryover_A` に登録し、起動時に突き合わせる。

### 中7. 凍結パーサを import すると口上にあるが、していない
- (b) `...\tools\run_stageB_local.py:8`（「採点: 凍結パーサ …… を import する」）・`:27`（`FROZEN_PARSER` は定義されるだけで未使用）
- (c) 起草者の申告と実装の食い違い。私が手元で確かめたところ `parse_app_v2` も `is_catastrophic` も import できるので、いま直せば済む。Colab の段で初めて気づくと、採点経路を現地で書くことになる（凍結物からの乖離が最も起きやすい形）。
- (d) 自己検査に `import app_parser_rev2; assert hasattr(...)` と、凍結パーサの SHA16 の印字を足す。

### 中8. 組み立てた報告から「注」が丸ごと落ちる
- (b) `...\tools\build_report_B.py:71`（表の見出しに注の列が無い）・`:76-78`（11 欄を印字し `r['notes']` を使わない）
- (c) 正本 `gate_order.label_uniqueness`「器は当たった門の一覧を**別の欄に出す**」・`report_rules.gate_notes`「ほかは注の欄に一覧で印字する」に反する。一時置き場で組み上げた報告で実測——集計 json にある二つの注（`注（様式・差 20.0 pt）`／`ほかに当たった門: 判定不能（品質床）`）は、報告のどこにも現れない。雛形の散文のほうは「札は一つだけ付き、ほかに当たった門は注に出る」と約束している（雛形 66 行）ので、**約束と中身が食い違う**。
- (d) 表に「注」列を足し `・`.join(r['notes'])` を入れる。長くなるなら表の直後に脚注の区画を置く。

### 中9. p が `0.0` と印字される
- (b) `...\tools\build_report_B.py:78`　`round(r['p'], 5)`
- (c) 実測: `p = 2.827684535732243e-12` → 報告の表では `0.0`。p が零であるという主張は偽である。`report_rules.mc_reporting`（厳密に計算できるものは厳密値に）の趣旨にも反する。
- (d) `'%.3g' % p`（または `p < 1e-5` のとき `'<1e-5'`）にする。集計 json の生値は残すこと。

### 中10. `--lint` が口上にあるのに引数に無い／`report_lint.py` は B を知らない
- (b) `...\tools\build_report_B.py:8`（「走査器を走らせる口を持つ（--lint）」）・`:19-26`（`--lint` は定義されていない）
- (c) 申告と実装の食い違い。`tools/report_lint.py` を `contrasts-B|stageB` で検索しても一件も当たらない（段階 A 専用）。`report_rules.typed_numbers` の走査は、事実上いま誰もやらない。
- (d) 口上を直すか、`--lint` を実装して B 対応の走査器を用意する。凍結前に決める。

### 中11. `n_conf` を計算して使っていない／雛形の散文に手打ちの数が残っている
- (b) `...\tools\build_report_B.py:40`　`n_conf = sum(x['m'] for x in T['families'].values())`（以後一度も参照されない）／雛形 `...\records\B\results-report-template-B.md:14`
- (c) 雛形の散文には「確証の族は 16 対比（減算 4・加算 4・交差 8）で、族ごとに Holm（各 α=0.05・上界 0.15）。場面は 4。本走行は腕 × 場面で n=200。」と八つの数が手で打ってある。`report_rules.typed_numbers` は「打ち込む数は日付・SHA16・SHA-256・費用の実額・コミットの短い名に限る」と書いている。起草者は照合用の `n_conf` を計算するところまでやって、**照合を書き忘れている**。正本 `print_strings.first_finding` の中にも「16」が固定文字列で入っている。
- (d) `assert n_conf == 16` ではなく、雛形の当該行を正本参照の束縛（`build_draftB.py` の型）にするか、組み立て時に `n_conf`・各 `m`・`n_main`・`alpha` と散文の数を突き合わせて食い違えば止める。
- (e) 補足: これは「散文に手計算の数を残さないか」という重点への私の答えである——**器は散文を一字も検査していない**。

### 中12. 整合検査・抽出検査の記録が無くても報告が組み上がる
- (b) `...\tools\build_report_B.py:22-23`（どちらも `default=None`）・`:56-57`（無ければ「（記録が渡されていない）」と印字して続行）
- (c) 手順（草案9B:100）の第 4・第 9 段は、率を見る前の整合検査と抽出検査を必須にしている。器はそれを任意にしている。
- (d) 両方を必須引数にし、`INT['problems']` が非空なら既定で止める（`--force` で越えられるなら理由を記録に残す）。

### 中13. 凍結物の一覧に、B が依存する凍結物が入っていない
- (b) `...\tools\freeze_B.py:23-25`（`TOOLS` の 16 本に `run_preamble_local.py` が無い）／同ファイルは `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py`・`app-scenarios.json` も記帳しない
- (c) B のプロンプトと採点は、この三つの凍結物に載っている。これらが変わっても B の FREEZE-RECORD は気づかない。`deviation.scope` は「正本・腕の素材・器材・手順のすべて」と書いている。
- (d) `TOOLS` に凍結走行器を足し、別枠 `carryover` として凍結パーサと場面の SHA16 を記帳する。

### 中14. 合成データの「置き場の印」が効いていない／`results/_synth` が `.gitignore` に入っていない
- (b) `...\tools\synth_B.py:7-8`（「置き場に `_dryrun` を含める」と申告）・`:58`（実際に作る名は `<tag>__<name>__dryrun`）・`:233`（既定の置き場は `results/_synth/<case>`）／`...\tools\runs_B.py:63`（印として見るのは path 成分が厳密に `_dryrun` であること）／`...\tools\dry_run_B.py:43`・`:95`
- (c) 実測: 合成データに立つ印は `manifest.dry_run`・`manifest.model`・`trials.dry_run` の三つで、`dir._dryrun` は**立たない**。四重の守りのうち一重が効いていない（他の三重が効いているので現状は守られている）。`.gitignore` は `results/_dryrun/` と `results/_smoke/` を除外するが `results/_synth/` は除外しない。`dry_run_B.py` は既定でリポジトリ内の `results/_synth` に書き、`--keep` を付けると消さずに残す。
- (d) 置き場の名を `_dryrun/<case>` にそろえるか、`dry_marks` に `'_synth'` を足す。`.gitignore` に `results/_synth/` を足す。`dry_run_B` の既定の置き場を `.gitignore` 済みの場所にする。

### 中15. 合成データによる検査が、門の器の返り値を見ていない
- (b) `...\tools\dry_run_B.py:46`　`rc_g, out_g = run([...])`（`rc_g` は表に印字されるだけで assert されない。合成 `:45` と集計 `:65` には `assert rc == 0` がある）
- (c) 門の器が異常終了しても、直前の `gate-B.json` が残っていれば（同じ置き場を使い回す運用に変えた場合など）気づかずに進む。
- (d) `assert rc_g in (0, 期待する非零), out_g` にする。門が「閉じた」ことを非零で表す設計なら、その値を明示する。

### 中16. 「S4 の三分岐」が一本の経路として数えられ、三つ目の枝が一度も発火していない
- (b) `...\tools\dry_run_B.py:32`（PATHS に `'S4 の三分岐'` が一項目）・`:74-75`（判定名を後ろに付けて一項目に足すだけ）
- (c) 起草者の記録は「十五の経路はすべて発火した」と書くが、記録の表を読むと S4 は `下がった（封印は外れ）` と `当否を言わない` の二枝しか出ていない。**封印どおり（下がらなかった／上がった）の枝が一度も走っていない**。同じ型で、`sign_agreement` の `agree` は五つの場合すべてで 0 である——つまり「封印が当たった」経路も一度も走っていない。私が合成データの封印をデータと合う向きに書き換えて走らせると `agree: 2 / confirmed: 3` になり、経路そのものは動く。**動くが、確かめられていない。**
- (d) PATHS を `S4:下がった`・`S4:下がらなかった`・`S4:当否を言わない` の三項目に割る。`case_all` の封印に、データと**一致する**符号の対比を一つ以上入れる。本番では 16 対比すべてに封印が付くので、`signs` を全対比ぶん持つ場合も一つ足す。

### 中17. 方向の割り当てが再開を知らない／試行から方向への写像が無い
- (b) `...\tools\steer_B.py:47-50`
- (c) `allocate` は件数だけを返し、どの試行がどの方向かを決める規則が器のどこにも無い（塊で配るとバッチ位置と方向が交絡する）。中断と再開では `allocate` を残り件数に対して呼び直すことになり、規則どおりの等分にならない——実測: `allocate(200) = [67,67,66]` だが `allocate(100) + allocate(100) = [68,66,66]`。`sessions.resume_rule` が中断と再開を前提にしている以上、起きる。
- (d) `allocate(n_total)` の結果から `direction_of(trial_index)` を導く関数を作り、再開は **trial_index を基準に**引き直す（残り件数から割り直さない）。自己検査に「任意の中断点で分割しても合計が `allocate(n_total)` に一致する」を足す。

### 中18. 抽出検査の種が正本に無く、dry-run の種を流用している
- (b) `...\tools\sample_inspection_B.py:75`　`rng = np.random.default_rng(a.seed if a.seed is not None else T['seeds']['dryrun'])`
- (c) 正本 `seeds` に抽出検査の種が無い。器が黙って `seeds.dryrun`（79999）を使っている。合成データの生成と本番の標本抽出が同じ種を共有する。
- (d) 正本 `seeds` に `sample_inspection` を足して凍結する。

### 中19. 起草者の整備の記録の SHA16 が、五本ぶん現物と食い違う
- (b) `...\records\B\tooling-record-B-2026-09-18.md:15-22`
- (c) 私が現物から計算して突き合わせた結果:

  | 物 | 実測 ＝ 依頼文の表 | 整備の記録 |
  |---|---|---|
  | `tools/analyze_B.py` | C5258778F1278D55 | 14AD60179D21596A（違う） |
  | `tools/integrity_B.py` | 6C55172320879D1B | D6C9C0B7BCE65223（違う） |
  | `tools/run_stageB_local.py` | 161857689B498C70 | 775F2BF5D340C8E1（違う） |
  | `tools/runs_B.py` | C7BC15CDE9B01010 | F4EA7C16534E9714（違う） |
  | `tools/synth_B.py` | 4E4136F7EA24D891 | 25529F4C52F6B0D4（違う） |

  ほかの十一件（正本・草案・転記行・雛形・計画・記録自身・残りの器材）はすべて一致する。つまり**整備の記録は最後の手入れの前の版で書かれ、書き直されていない**。結果として、記録 `:28` の「十五の経路はすべて発火した」という主張は、**いま検分に出ている版の `synth_B.py`・`analyze_B.py`・`runs_B.py` が出した結果ではない**。私が現物で `case all` を走らせ直したところ、札の内訳は記録の表と一致した（確証 2・逆 1・品質床 3・検閲 1・refuse 転位・差 2・refuse 転位 1・書式外転位 1・様式転位 1・非有意 4）ので、結論は変わっていない。変わっていないことと、記録がそれを証明していることは別である。
- (d) 凍結の直前に整備の記録と合成データの検査の記録を**再生成**する。`freeze_B` に「記録に載る SHA16 と現物が一致すること」の検査を足す。

---

## 3. 軽微

- **軽1**: `determinism_ok` は二度目の辞書に**余計な鍵**があっても通る（実測: `(True, [])`）。また活性に NaN があると「非決定」と報告する（実測: `(False, [key])`）——止まるのは正しいが、理由の名が違う。`...\tools\direction_B.py:83`。→ 鍵集合の一致を先に assert し、NaN は別の名で報告する。
- **軽2**: 抽出場面の安定性が `EX[0]` と `EX[1]` に固定されている。`...\tools\direction_B.py:74`。抽出場面が三つになると黙って先頭二つだけ比べる。→ `assert len(EX) == 2` を置くか総当たりにする。
- **軽3**: 自己検査に同語反復が二つある。`...\tools\direction_B.py:90`（実装式をそのまま期待値にする）・`...\tools\run_stageB_local.py:143`（`assert len(rec) == 31` は同じタプルを数え直しているだけ）。→ 期待値を手で書いた表にする。
- **軽4**: `T['publication']['dual_use'][:0] or ''` は常に空文字を返す。`...\tools\build_report_B.py:102`。両用性の柵を印字するつもりだったのか、しないつもりなのかが読めない。→ どちらかに決めて書く。
- **軽5**: `freeze_B` の口上が草案8B のままで、既定の例も `design-stageB-draft8.md` を指す。`...\tools\freeze_B.py:4`・`:14`。現物は draft9。
- **軽6**: `--agree` の出力は上書き検査を通らない。`...\tools\sample_inspection_B.py:63-65`（標本と封印と対応表には `:70-73` の検査がある）。→ 同じ検査を通す。
- **軽7**: `arm_plan` は腕の名に `+v` と `-v` が両方あると黙って `+` を採る。`...\tools\run_stageB_local.py:86-87`。現在の腕名では起きないが、名が増えると黙って誤る。→ 両方あれば止める。
- **軽8**: system 文を置かないことが、器にも manifest の欄にも書かれていない。凍結走行器は `--system` を持つ（`...\tools\run_preamble_local.py:84`）。`runner.manifest_fields.common` に `system` が無い。→ manifest に `system: none` を記帳する。
- **軽9**: `runs_B.cell_counts` が数える `unmeas`（書式外 or ループ or 打ち切り）を**下流の誰も読まない**。`...\tools\runs_B.py:128`。`loop`・`trunc` は `integrity_B.py:74` の表に出るだけで、報告には一度も現れない。`carryover_A` の「測定不能の数え方をそろえる」は未実装。→ 報告の三つ組の隣に未測定を印字するか、正本から外す。
- **軽10**: `sample_inspection_B.py` には自己検査が無い（段階 A の同名器には `:154` にある）。

---

## 4. 重点3 への答え——合成データに入っていない壊れ方

`synth_B.py` が実際に何を作ったかを数えた（`case all`・22,400 試行）。

| 欄 | 出た値 |
|---|---|
| `status` | `'ok'` のみ（22,400） |
| `choice` | `'A'` 21,442 ／ `'refuse'` 958（ほかの選択肢も `None` も無い） |
| `loop_flag` | 全件 `False` |
| `truncated` | 全件 `False` |
| `direction_id` | 全件 `'synth'` |
| セルの件数 | 200 が 66 セル（欠落・過剰・重複が無い） |
| セッション | `s1` のみ／`idB`（同一性選別）の走行は零 |

入っていない壊れ方を、影響の大きい順に挙げる。

### (1) api_error が一件も無い——**これは器が実際に誤る**

`cell_trials` は `spec['api_error']` を受ける口を持つ（`...\tools\synth_B.py:45`）のに、**五つの場合のどれ一つも設定していない**。したがって `n`（行数）と `n_ok`（全分母）が常に等しく、正本 `denominators.n_ok` の定義が一度も試されていない。

そこで私が注入して確かめた。

- **(A) 一つの腕の 200 試行をすべて `status='error'` にした**（＝そのセルからは使える試行が一件も出なかった）:
  - 整合検査 `integrity_B.py` → **不整合 0**（止まらない）
  - 集計 → `sub:N1:O-Ncold-v~O-Ncold-vrand` は `k_A=0, n_ok_A=0, diff_pt=None, p=None, label='非有意'`
  - 要約の件数は `確証 3 → 2`・`非有意 4 → 5`。`missing_cells` は空。
  - つまり**一件も測れなかったセルが「差は無かった」として報告される**。原因は `...\tools\analyze_B.py:143` の `row['label'] = fired[0] if fired else ('確証' if (p is not None and p < alpha_step) else '非有意')` ——`p is None`（データ無し）が `非有意` に落ちる。`denominators.judgeable`（確証＋非有意）にも入るので、判定可能な対比の数まで水増しされる。
- **(B) 同じ腕の 200 試行のうち 40 を `status='error'` にした**（破局でない試行だけ）:
  - `n_ok_A = 160` で正しく分母から外れ、`diff_pt = -27.5` と正しく計算された。**部分的な api_error の算術は正しい。**

つまり誤るのは `n_ok = 0` の端のときだけだが、そこが最も起こりやすい形（腕ひとつぶんの走行が丸ごと失敗する）である。なお `analyze_B.py` は別の検分者の担当なので、**この一件は私の所見としては「合成データに api_error が無いので、この誤りは誰の目にも触れない」**という形で挙げる。修正はおそらく `analyze_B` 側（`p is None` を `判定不能（測れなかった）` にする）と `integrity_B` 側（`n_ok == 0` のセルを不整合にする）の両方。

### (2) 実機では起こり得ない組み合わせが、逆に大量に入っている

`cell_trials`（`...\tools\synth_B.py:51-53`）は `cat`・`ff`・`style_a`・`style_b`・`mention` をすべて `j = 0` から数えるので、指定件数の小さいほうが大きいほうに**入れ子**になる。結果:

- 破局 ∧ 書式外 = **570 件**
- refuse ∧ 書式外 = **24 件**
- 破局 ∧ refuse = 0 件

書式外（答えの記号が読めない）なのに `choice` が `'A'` で `catastrophe` が `True` という行が、全体の 2.5% ある。実機の採点ではまず出ない。これが効いてくるのは**希釈の門**である。門が守ろうとしている現象は「片腕だけ書式が崩れる → その分だけ破局の分子が減る → 見かけの破局率が下がる」（正本 `dilution_gate.why`・再現の記録 K23）だが、合成データでは書式外と破局が独立に立つので、**この因果が一度も再現されていない**。門の札が*立つ*ことは確かめたが、門が*効く*場面は作っていない。

- 直し方: `cell_trials` に「書式外の試行は破局を `False`（または `None`）、`choice` を `None` にする」という実機の規約を入れ、希釈の場合を「ff を増やしたぶんだけ破局の分子が減る」形で作り直す。門の閾値 10 pt が、その形の希釈に対して本当に Holm の初段を止めるかを合成で確かめる。

### (3) 未測定（ループ・打ち切り）が一件も無い

`loop_flag`・`truncated` は全件 `False`（`...\tools\synth_B.py:36` の決め打ち）。`max_tokens 4096` の場面の試行では、打ち切りは実機で必ず出る（段階 A・追補 C の実績でも出ている）。`runs_B.cell_counts:128` の `unmeas` はループと打ち切りを足す定義だが、合成では書式外ぶんしか立たない。**未測定の数え方が一度も試されていない。**

### (4) 中断と再開が一件も無い

走行の置き場は鍵ごとに一つ、セッションは `s1` だけ。`runs_B.index_runs` の `allow_multi`（同じ鍵に複数の走行を持つ）と `counts_main` の足し込みは**一度も発火していない**。`sessions.resume_rule`（同じ `trial_id` の式で再開し、重複と欠落を整合検査で確かめる）は、材料が無いので検査されていない。段階 A・追補 D では実際に切断が起きている（再開器を作った経緯がある）ので、B でも起きる前提で作るべき壊れ方である。

### (5) 品質床の相手が、常に同じセッションにいる

`write_run` は `session` を渡されないと 1 にする（`...\tools\synth_B.py:62`）。したがって裁定 D88 の「無操作の相手は、それが相手を務めるセルと**同じセッション**で走らせる」の**不合格側が一度も作られていない**。この規則を守らせる器があるかどうかを、合成データでは判定できない。

### (6) 同一性選別（`idB`）の走行が一つも無い

`identity_screen`（三スタック・13 腕・30 個の差・平均 5 pt／最大 12 pt）の経路は、合成データに材料が無い。門1 は開いた（`gate_B` は `idB` を要求しなかった）。選別の不合格で B をどう扱うか（`fail_reading`）も未検査。

### (7) 方向が一本しかない

`direction_id` は全件 `'synth'`。したがって `random_control.pooling`（三方向の率を先に印字し二項の等質性を記述で確かめてから合併する）も `allocation`（67/67/66）も**一度も走っていない**。三方向のうち一本だけが極端な率を出す、という最も起こりそうな形が作れない。

### (8) 封印は「食い違う一件」だけ

`case_all` の封印は一対比・一符号（`...\tools\synth_B.py:122`）で、データとは逆向き。したがって発火するのは「逆向き」の枝だけ。**一致の枝・封印が「零」の枝・封印はあるが非有意の枝・16 対比すべてに封印がある形**は、どれも作られていない（→ 中16）。

### (9) そのほか、作られていない形

- manifest の欄の欠落（`runner.manifest_fields.rule`「欄が欠けていれば不整合として止める」が未検査）
- 本走行の `layer`・`coef` が選定結果と食い違う走行
- `n_ok = 0` 以外のゼロ除算（腕が丸ごと存在しないセル）
- 三候補以上の同点／浮動小数の僅差（0.1 pt 差が同点に落ちるか）
- 印が半端な dry-run（行にだけ印があり manifest に無い、など）

---

## 5. この検分が確認していないこと

1. **実機で一行も走らせていない。** 活性の抽出・hook つきの生成・バッチの詰め・左詰めの主位置の取り出しは、`Qwen/Qwen3-4B-Instruct-2507` の重みでは一度も走らせていない。重大3 と重大4 は、**ランダム初期化した小さな Llama を CPU で回して**再現したものであり、実機の挙動が同じである保証はない（ただし、どちらも実装の形から出る帰結なので、機種で変わる性質のものではないと考える）。
2. **総層数を確かめていない。** Qwen3-4B の `num_hidden_layers` を重みの config から読んでいない。中1 の「36 なら影響しない」は伝聞に基づく仮定である。凍結の段で登録者が実測して記帳すべき。
3. **`gate_B.py`・`analyze_B.py`・`integrity_B.py` を行単位で読んでいない**（一体目の担当）。これらに触れた箇所（`analyze_B.py:143` の札の既定値、`integrity_B` が `n_ok=0` を見逃すこと）は、合成データを通して外から観察した結果であり、内側の論理は検分していない。門の順・札の一意性・希釈の門の分母・Holm の実装・検閲の両腕条件・S4 の裁定規則は、私は確かめていない。
4. **率・結果は一切見ていない。** `results/` の実データも `prelim/` も開いていない。鍵ファイルも読んでいない。数はすべて合成データと、私が一時置き場で作った対照である。
5. **他の検分者の所見を見ていない。** 重なりがあれば独立の二票として数えてよいが、私は合わせに行っていない。
6. **品質床の実装を評価していない。** 課題・入力・帯・採点・最大トークン数が未定なので、`score_quality` が正しいかは判定できない。二段の走らせ方（裁定 D77・D88）は合成データの形だけを見た。
7. **雛形の本文（`results-report-template-B.md`）を通しで検分していない。** 手打ちの数については §1 の該当行を見ただけで、全文の照合はしていない。
8. **転記行の数を数え直していない**（`records/B/design-facts-B.md` の内容の検証は別の巡の仕事と理解した）。

---

## 6. 凍結の前に片づけるべき最小の集合（私の見立て）

1. 重大1・重大2・重大3（介入そのものが登録どおりでない）——**これが片づかないと、走っても別の実験になる**。
2. 重大4（決定性の検査の条を二つに割る）——凍結後は逸脱になるので、いま正本を直す。
3. 重大5・重大6・重大7（合成の印・盲検・対応表の置き場）——規律の側の穴。
4. 重大8（`freeze_B` の止め方）——凍結そのものの門。
5. 重点3 の (1)(2)(3)(4) を合成データに足し、`dry_run_B` の経路表を割り直してから、**整備の記録と検査の記録を再生成**する（中19）。

---

本検分票のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。加算で破局率を上げる操作の再現手順は、本票のいかなる箇所にも書いていない（正本 `publication.dual_use`）。

---

補足（検分票の外・コーディネータ宛）: 一時置き場に置いた再現物は `C:\Users\PC\AppData\Local\Temp\claude\C--Users-PC\ccb2107c-84ba-4eab-bf7d-83ccce4f059f\scratchpad` にあります（合成データ・門と集計の出力・組み上げた報告・凍結の点検・対照実験の四種）。リポジトリのファイルは一つも書き換えていません。
