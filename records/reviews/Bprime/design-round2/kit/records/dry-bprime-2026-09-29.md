# B′ の器の合成データの確かめ（機械生成・`dry_bprime.py`・小さな乱数の Gemma 4・手元の CPU）

- 版: transformers 5.16.1・torch 2.9.1+cpu・設定の SHA16 E967DD38BC5CFD38（小さな模型は大きさだけ縮めた）。選ぶ層の添字 2（層 6・割合 0.5・段階 B の式）。主位置のトークン `<channel|>`。softcap 30.0。

| 確かめ | 通ったか | 値 |
|---|---|---|
| T1_logit_check_correct | 通った | max_abs 0 |
| T2_layer_check_correct | 通った | diff 0 |
| T3_double_norm_caught | 通った | max_abs 2.57 |
| T4_no_softcap_caught | 通った | max_abs 0.28 |
| T5_alignment | 通った | selected_layer_match True・last_layer_match False |
| T6_next_layer_differs | 通った | effect_correct 7.34・effect_next_layer 6.2 |
| T7_batch_invariance | 通った | max_abs 1.43e-06 |
| T8_sign | 通った | diff 0 |
| T9_no_hooks_left | 通った | ours_left 0・foreign_per_layer 1・1・1・1・1・1 |

- すべて通ったか: はい

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
