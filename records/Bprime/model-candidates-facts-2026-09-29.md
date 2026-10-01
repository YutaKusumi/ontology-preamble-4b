# B′ の機種の候補の事実（モデルカードの本文から・2026-09-29・コーディネータ南無弥勒如来・非公開）

- 出所: Hugging Face の各機種のページ（2026-09-29 に取得・写しは `sources/`）。鉤括弧の中はページの本文から機械で切り出した（英語のまま）。
  - `sources/meta-llama_Llama-4-Scout-17B-16E-Instruct.html`（SHA16 9064A2D8E2F5B7D0）・`sources/meta-llama_Llama-3.1-8B-Instruct.html`（SHA16 729B608688A7E400）・`sources/google_gemma-3-12b-it.html`（SHA16 B8E0F3B91E402977）・`sources/tokyotech-llm_Llama-3.1-Swallow-8B-Instruct-v0.5.README.md`（SHA16 FB56E4F19399DDDA）・`sources/google_gemma-3-4b-it.html`（SHA16 8CA9DD3701B67E25・Gemma-3-4B は後から足した）
- 計画書 v2.8 の B′ の条件: 機構層（重みを手元で動かし、隠れ状態を加減する）・bf16 必須・日英両版・置き場は Colab の GPU 一枚（門0 の実測: L4 は 2.67 ユニット／時・A100-80GB は 12.82 ユニット／時・計画書 §6）。

| 機種 | 系譜 | 大きさ（Scout だけ本文から） | bf16 の重みの目安（パラメータ数 × 2 バイト） | bf16 で Colab の GPU 一枚に | 日本語（本文） | 置き場の条件 | Nscale |
|---|---|---|---|---|---|---|---|
| `meta-llama/Llama-3.1-8B-Instruct`（計画書の案） | Meta | 8B・密 | 約 16 GB | 載る（L4） | 公式の対応言語に日本語が無い「Supported languages: English, German, French, Italian, Portuguese, Hindi, Spanish, and Thai」 | 利用の同意が要る（gated） | 有 |
| `meta-llama/Llama-4-Scout-17B-16E-Instruct`（登録者の提案） | Meta | 「17B (Activated) 109B (Total)」・専門家混合・画像も読む | 約 218 GB | 載らない（本文は「single H100 GPU with on-the-fly int4 quantization」） | 公式の対応言語に日本語が無い「Supported languages: Arabic, English, French, German, Hindi, Indonesian, Italian, Portuguese, Spanish, Tagalog, Thai, and Vietnamese」 | 利用の同意が要る（gated） | 有 |
| `tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.5` | Meta の Llama 3.1 に日本語の継続事前学習（東京科学大学ほか） | 8B・密 | 約 16 GB | 載る（L4） | 「Llama 3.1 Swallow enhanced the Japanese language capabilities of the original Llama 3.1 while retaining the English language capabilities.」 | 同意の画面は無い（README を認証なしで読めた）・許諾は「META LLAMA 3.1 COMMUNITY LICENSE」と「Gemma Terms of Use」（README の License の節） | 無 |
| `google/gemma-3-12b-it` | Google | 12B・密・画像も読む | 約 24 GB | L4（24 GB）には載らない見込み・A100 には載る | 「multilingual support in over 140 languages」 | 利用の同意が要る（gated） | 無 |
| `google/gemma-3-4b-it` | Google | 「4B params」（ページの表示）・密・画像も読む | 約 8 GB | 載る（L4） | 「multilingual support in over 140 languages」 | 利用の同意が要る（gated・ページの表示「Log in or Sign Up to review the conditions and access this model content」） | 無 |

- Swallow の注: 指示の学習は、別の機種の振る舞いをまねる形で行われた——「The model is trained to imitate the behavior of」「gemma-3-27b-it」（README の本文・機種の名はリンク）。系譜は Llama の重みの上に、日本語の継続事前学習と Gemma の出力をまねた指示の学習が重なる。
- Scout の注: 総パラメータで bf16 の重みを見積もると、Colab の GPU 一枚（最大 80 GB）には載らない。本文の「GPU 一枚に載る」は int4 の量子化のときの言い方で、計画書の「bf16 必須」と合わない。専門家混合なので、隠れ状態の加減が経路の選び（どの専門家に回るか）も動かす。
- Gemma-3-4B の注: 段階 A・B・B-lens・層三の Qwen3-4B と同じ規模の、別の系譜の機種。系譜と規模を分けて比べられる（Llama-3.1-8B は系譜と規模が一緒に変わる）。
- 感触の確かめ（`model-feel/feel-check-Bprime.md`）は Llama-3.1-8B と Scout だけで、Swallow と Gemma は Nscale に無いので確かめていない。

## 追記（2026-09-29・D256 の後）: Gemma 4 の二機種と Colab の GPU の選択肢

- 出所の写し: `sources/google_gemma-4-31b-it.html`（SHA16 5B58569FF6040D59）・`sources/google_gemma-4-26b-a4b-it.html`（SHA16 EA2473F0EDCCD0D6）・`sources/google_gemma-4-31b-it.config.json`（SHA16 E967DD38BC5CFD38）・`sources/google_gemma-4-26b-a4b-it.config.json`（SHA16 ED0C1EB3633DE771）。Hugging Face の名は `google/gemma-4-31B-it`・`google/gemma-4-26B-A4B-it`。

| 機種 | 系譜 | 大きさ（本文） | bf16 の重みの目安 | bf16 で Colab の GPU 一枚に | 日本語（本文） | 置き場の条件 | Gemini の API |
|---|---|---|---|---|---|---|---|
| `google/gemma-4-31B-it` | Google | 密（設定の `enable_moe_block` は False）・密の表「Total Parameters 2.3B effective (5.1B with embeddings) 4.5B effective (8B with embeddings) 11.95B 30.7B」の最後が 31B・層 60 | 約 62 GB | 80 GB の GPU なら載る（A100-80GB・H100）・40 GB の GPU には載らない | 「Out-of-the-box support for 35+ languages, pre-trained on 140+ languages」 | 「License: apache-2.0」・同意の画面なし（設定を認証なしで読めた）・画像の読み取り部「Vision Encoder Parameters ~550M」 | 有 |
| `google/gemma-4-26B-A4B-it` | Google | 専門家混合「Total Parameters 25.2B Active Parameters 3.8B」・「Expert Count 8 active / 128 total and 1 shared」・層 30 | 約 50 GB | 80 GB の GPU なら載る・40 GB の GPU には載らない | 同上 | 同上 | 有 |

- 共通の注: 設定の `transformers_version` は 5.5.0.dev0 で、手元の器（段階 B と層三は transformers 4.57 系）の版より新しい版が要る（Colab の既定の版は 5.16.1 だった・二巡目の Swallow の走行で見た）。チャットの型は既定で思考を出さない——「enable_thinking = enable_thinking | default(false)」。Gemini の API の配信では既定で思考が返った（二巡目の逸脱 1）。
- 26B-A4B の注: Scout と同じく専門家混合で、隠れ状態の加減が専門家の選びも動かす。動く部分（3.8B）は Qwen3-4B に近い。
- 31B の注: 密で、Qwen3-4B と同じ形の器（残差の加減・層ごとの読み取り）を当てやすい。ただし規模は Qwen3-4B の約 8 倍で、系譜と規模が一緒に変わる。層は 60（Qwen3-4B は 36）。
- Colab の GPU の選択肢（2026-09-29・ランタイムのタイプの窓で起草者が見た・機械で写していない）: CPU・H100 GPU・G4 GPU・A100 GPU・L4 GPU・T4 GPU・v6e-1 TPU・v5e-1 TPU。門0 で測ったユニットの率は L4 と A100-80GB だけで、H100 と G4 の率は測っていない。A100 が 80 GB で割り当てられるかは保証されない（計画書 §6）。
- 費用の目安（見積もっていない）: 31B の順伝播は 4B の約 8 倍の計算で、A100 の率は L4 の約 4.8 倍。層三（4B・3.99 ユニット）と同じ型の仕事でも、ユニットは一桁ほど多くなりうる。

## この記録が確認していないこと

- 各機種の実際の日本語の質（Swallow・Gemma は未確認）。
- Gemma-3-12B が L4 に載らないことの実測（パラメータ数からの目安だけ）。
- 許諾の条文の中身（研究の利用・公開の条件）。
- Gemma 4 を手元で bf16 で動かすこと（80 GB の GPU での載りと速さ・transformers 5 系での器の書き直し）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
