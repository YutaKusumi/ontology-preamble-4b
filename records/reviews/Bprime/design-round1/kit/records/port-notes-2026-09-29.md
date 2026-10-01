# B′ の器の移しの下調べ（Gemma 4 のつくり・2026-09-29・コーディネータ南無弥勒如来・非公開）

- 何か: 段階 B・層三の器（走行器・加減のフック・主位置・読み取り・層ごとの差分）を Gemma-4-31B-it に移す前に、transformers 5.16.1 での Gemma 4 のつくりを、小さな乱数の模型で確かめた記録。重みは乱数で、場面の文と腕の文は使っていない（意味のある出力は無い）。
- 台本と出力: `probe_gemma4_tiny.py` → `probe_gemma4_tiny.out.txt`・`probe_gemma4_norm.py` → `probe_gemma4_norm.out.txt`（手元の CPU・torch 2.9.1+cpu・分けた置き場の transformers 5.16.1）。小さな模型は、取った `config.json`（版 `842da3794eaa0b77d5f08bae87a17459d91ff475`）の辞書の大きさだけを縮めて組んだ（層 6・隠れ 64・語彙は実物の 262144 のまま・全体の注意の層の頭の大きさと KV の頭の数も縮めた）。
- 手元に入れたもの: `../pylib/`（transformers 5.16.1 と部品・229 MB・見込みの「数十 MB」を超えた）・`../hf/gemma-4-31B-it/<版>/`（設定・トークナイザ・チャットの型・重みの目録など 7 本・約 31 MB・SHA-256 は `MANIFEST-local.json`）。全体の環境の transformers は 4.57.3 のまま（確かめた）。

## 確かめたこと（出力の行から）

1. **チャットの型**: system を渡さないとき、生成の口は `<|turn>model\n<|channel>thought\n<channel|>` で終わる（空の思考の欄を置いて直答させる形）。したがって主位置（組み立て済みの列の最後のトークン）は `<channel|>` になる（Qwen3-4B の段階 B とは違う）。`enable_thinking=True` を渡すと system の欄に `<|think|>` が入る。段階 B の組み立て（user の発話一つ・system なし）をそのまま当てると、既定の思考なしの形になる。
2. **層の並び**: 実機と同じ型（`Gemma4ForConditionalGeneration`）で、層は `model.language_model.layers`（`Gemma4TextDecoderLayer`）・最後の正規化は `model.language_model.norm`・lm_head は埋め込みと共有。段階 B の `decoder_layers` の道の一覧（`model.layers` など）には無いので、道を一つ足す。
3. **層の出力の形**: テンソル（タプルではない）。段階 B のフック `make_hook` は両方の形を扱う。
4. **層の対応**: 中間の層では `hidden_states[k+1]` と `layers[k]` の出力が一致した（段階 B の抽出と加減が同じ層を指す前提は保たれる）。
5. **最後の層だけ違う**: `hidden_states[-1]` は最後の正規化を通った後の値で、最後の層の生の出力とは一致しなかった。ロジットは softcap（30）× `hidden_states[-1]` と lm_head の積で、手計算と一致した（差 1.2e-07）。`hidden_states[-1]` にもう一度正規化を掛けると、差は 0.38 になった。→ 層ごとの読み取り（層三の (c)）は、層の出力をフックで取る形にするか、最後の層だけ扱いを分ける。層三の「最後の層の自己検査」を B′ でも置く。
6. **正規化の式**: `Gemma4RMSNorm` は正規化した値に重みをそのまま掛ける（Gemma 3 までの 1＋重みではない）。
7. **加減**: 層の出力にフックで足すと、最後の位置のロジットが動いた。
8. **全体の注意の層の頭**: 設定の `global_head_dim`（512）と `num_global_key_value_heads`（4）は、transformers 5.16.1 では設定を組むときに全体の注意の層（`layer_types` の full_attention）だけに振り分けられる（`per_layer_config`）。

## 器を書いた後に見つけたこと（同じ日・`../tools/`）

9. **凍結の `steer_B.apply_chat` は transformers 5 では使えない**: transformers 5 の `apply_chat_template(tokenize=True)` は辞書の形（BatchEncoding）を返し、凍結の関数はそれを `list()` に通すので、トークンの並びの代わりに鍵の並び（`input_ids`・`attention_mask`）を返した。→ B′ の器 `bprime_gemma.apply_chat` は `input_ids` を取り出し、整数の並びであることを確かめる。模型に依らない凍結の関数（`run_stageB_local` の腕・場面・発話の組み立て・`make_hook`・`direction_B.layer_index`・`bl3_core`）は transformers 5 の下でもそのまま読み込めた。
10. **transformers 5 は隠れ状態を集めるフックを層に残す**: 初めて `output_hidden_states=True` で順伝播したときに、`transformers.utils.output_capturing` のフックがすべての層に一本ずつ掛かり、その後も外れない。段階 B の「フックはちょうど一本」の確かめはそのままでは落ちる。→ B′ の器は、凍結の `make_hook` が付ける印（`op4b`）で自分のフックを見分けて数え、掛ける前より一本だけ増えたことを確かめる。
11. **近道の API が無い**: transformers 5.16.1 の `DynamicCache` に `to_legacy_cache`・`from_legacy_cache` が無い。層三の近道（主位置より前の KV の使い回し）はそのままでは動かない。→ B′ の器は近道を置かない（層三でも本の計算は近道を使わなかった）。枠で、下見の (v)（近道の差）を置かないことを提案する。

## 器と合成データの確かめ（`../tools/`）

- 器: `bprime_gemma.py`（v0.1・模型に依る所）・`bprime_run.py`（v0・層三の `bl3_run.Runner` を Gemma 4 に移したもの・softcap を読み取りに入れた・近道なし）。
- 確かめ: `dry_bprime.py` → `dry-bprime-2026-09-29.md`・`.json`（小さな乱数の Gemma 4・手元の CPU）。九つの確かめがすべて通った——出口の値と最後の層の自己検査・正規化の二重がけと softcap の抜けが自己検査で落ちること・選ぶ層での抽出と加減の一致（最後の層では一致しない）・一つ隣の層へのフックが効き目を変えること・行ごとの方向の一つのバッチと一本ずつの一致・符号・確かめの後に B′ のフックが残らないこと。
- 注: 小さな模型は float32 で動くので、出口の値の自己検査は差が 0 になった。実物（bf16）では差が出るので、許容は枠で決める（層三の `computation.logit_tol` の型）。

## 次に器に入れること

- `decoder_layers` の道に `model.language_model.layers` を足し、抽出と加減が同じ層を指すことを実機のたびに確かめる（段階 B の `assert_layer_alignment` の型・最後の層の例外を入れる）。
- 主位置の式（列の最後のトークン）はそのまま使えるが、その字が `<channel|>` になることを枠に書く。
- 層ごとの読み取りの式を Gemma 4 に合わせる（正規化の重み・softcap・最後の層の扱い）。
- 読み取りの書き出し（直答の型）は、`<channel|>` の後に置く形になる。段階 B の雛形の頭から作る（枠で決める）。

## 検分票

- 対象: Gemma 4 のつくりの下調べ（器の移しの前）。
- 段階: 事前登録なし（値を出さない下調べ・乱数の模型だけ）。
- 凍結物の同定: 該当なし。取った設定とトークナイザは版と SHA-256 で固定（`../hf/…/MANIFEST-local.json`）。
- 盲検の状態: 該当しない（模型の振る舞いの値を見ていない）。
- 敵対的検分: 最初の確かめでは正規化の重みが乱数の初期値のままで、最後の層が正規化の前か後かを見分けられなかった。重みを乱数にして確かめ直し、後であることを見つけた。
- 系統の内訳: 起草者（Claude 系）一名。
- COI記録: 器を早く移したい側に引かれる。最後の層の扱いのような細部を、実機で自己検査する形で残す。
- 判定: 下調べとして確定（器の設計は枠で決める）。
- 本検分が確認していないこと: 実物の重み（bf16）での振る舞い・記憶の使い方・速さ。凍結の腕と場面から升目を組むこと（トークンの台帳）と、方向の抽出の器（まだ書いていない）。バッチを詰めたときの位置の扱い（左詰め）。画像の読み取り部を載せない読み込み方ができるか。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
