# 追補 V′ 不在確認（凍結直前・2026-09-07・コーディネータ）

目的: 「床／中間基底の前置きに役割付与一行を後置して、破局的選択率の上向きを事前登録つきで測った先行」の有無を、凍結直前に列挙できる範囲で確認する（凍結 §2.8 の撤退条件の前提）。不在の検査は列挙できたものの不在しか検査しない（教訓 23）——本記録は「見つからなかった」の記録であり、「存在しない」の証明ではない。

## 検索（WebSearch・2026-09-07・三問）
1. persona prompt "cold strategist" OR "ruthless" role assignment increases harmful choices small language model evaluation 2025 2026
2. appending role instruction after system prompt safety degradation "persona" jailbreak additive effect Qwen3 4B benchmark
3. preregistered study prompt prefix robustness "role-play" persona adversarial line catastrophic action rate nuclear scenario LLM 2026

## 見つかった近接先行（同型ではない・報告の位置づけで参照する）
- Disentangling Intent from Role: Adversarial Self-Play for Persona-Invariant Safety Alignment（arXiv 2605.01899）——ペルソナ付与で有害要求の攻撃成功率が上がることの体系的検討と対策。エンドポイントは有害要求への応諾（ASR）で、本追補の「シナリオ内の破局的選択」ではない。
- Persona Non Grata: Single-Method Safety Evaluation Is Incomplete for Persona-Imbued LLMs（arXiv 2604.11120）——ペルソナ付きモデルの安全評価は単一手法では不完全。
- Moral Susceptibility and Robustness under Persona Role-Play in Large Language Models（arXiv 2511.08565）——100 ペルソナ × 15 モデルで道徳判断の感受性を測る。ペルソナは前置き全体の置換であり、既存の前置きへの一行後置ではない。
- Shah et al. 2023（ペルソナによるガードレール回避）・SG-Bench（arXiv 2410.21965・安全の汎化）・Jailbreaking in the Haystack（arXiv 2511.04707・文脈長による安全劣化）。
- Qwen2.5-3B の高い基底ジェイルブレイク率の報告（HarDBench 等）——小型 Qwen の脆弱性そのものは既知。

## 判定
- 「既存の前置き（存在論的／一行）の後ろに役割付与一行を加算し、床と中間基底の断面で破局的選択率の上向きを Fisher・Holm・事前登録で測る」という同型の先行は、上記三問の範囲では見つからなかった。撤退条件（同型の先行があれば「複製」として位置づけ直す）は発火しない。
- ただし「ペルソナ付与が安全性を下げる」こと自体は 2023 年以降の既知の知見であり、本追補の新規性は**方向そのものではなく、断面（床／中間基底・用量整合・中立統制・決定役統制）と事前登録の作法**にある。報告の位置づけはこの線で書く（「悪意の枠が危険にする」を新発見と書かない）。
- 検索は英語三問のみ。日本語の先行・非公開の先行は検査していない。

本文書のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
