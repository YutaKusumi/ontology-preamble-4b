# Firth の一致検査（機械生成・`tools/firth_check_A.py` v1・2026-09-14 12:01 UTC）

- 判定: **PASS**（規則: すべての量が許容差の内側なら合格。一つでも外れたら不合格として凍結を止め、原因を記録する（許容差を後から動かさない）。）
- 許容差: {"coef_abs": 1e-06, "penalized_loglik_abs": 1e-06, "plr_stat_abs": 1e-05}
- R: R version 4.6.1 (2026-06-24)・logistf 1.26.1・endometrial bundled: FALSE・control `logistf.control(maxit=1000, maxhs=50, maxstep=5, lconv=1e-12, gconv=1e-12, xconv=1e-12)`
- firth.py v2.1（SHA16 CE584FDF2AE79930）・正本 SHA16 8B298F126E77CBE6

| データ | 係数の差の最大 | 罰則付き対数尤度の差 | 統計量の差の最大 | 合否 |
|---|---|---|---|---|
| synth_rising_ptconst | 5.998e-08 | 4.547e-13 | 4.547e-13 | 合格 |
| synth_mid_delta | 6.393e-08 | 9.095e-13 | 1.819e-12 | 合格 |
| synth_floor_sparse | 7.744e-08 | 1.705e-13 | 2.274e-13 | 合格 |
| sex2 | 2.537e-07 | 8.811e-13 | 7.390e-13 | 合格 |

本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
