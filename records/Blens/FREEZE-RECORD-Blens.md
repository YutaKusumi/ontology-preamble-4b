# B-lens の凍結の記録（機械生成・`tools/freeze_Blens.py` v2）

- 凍結: 2026-09-24 07:33（日本時間）・登録者の言葉は逐語で「登録者最終確認を行いました。私たちでできるベストを尽くしたと判断します。器・合成データ・凍結・封印の順に進めてください。」（裁定 D186）。
- 本文: `design/design-Blens-FROZEN.md`（SHA16 A6281F419F059145）・草案3 との差は題名・凍結の行・組み立ての記録だけ。
- 八腕の主位置の活性を公開の置き場 `results/dirB/dirB__s1/main_position_activations.npz` に写した（SHA-256 7F41AC1B3BC02B7A5AAC146E114B795676071D46DD653062A7000C2B6A0D8C20・1010478 バイト・裁定 D175）。
- 組み立てた中と単独で割り方が違った集合（裁定 D184・組み立てた中を主にした）: X_nuclear_a・X_nuclear_others。
- Colab の確かめ（相 check）: kind_check 合う・not_dry 合う・versions 合う・weights 合う・random_dirs 合う・logit_check 合う・calibration 合う・selected 合う。
- 段階 B のランダム方向の再生（裁定 D187）: 手元の再生と Colab の再生の方向ごとの相対の差の最大 1.67e-07（許容 1e-06）・ビットで一致した組 1／4。方向の npz は `records/Blens/colab-check-random-dirs-Blens.npz`。
- 合成データ: `records/Blens/dry-run-Blens-2026-09-24.md`（34 経路・外れ 0）。
- 次: 記録先行の公開（push）→ 予想の封印（コーディネータが先・SHA だけを伝える → 登録者）→ Colab の相 extract → 層一・層二・報告（結果は登録者と一緒に開く）

## 凍結物の SHA16

| 置き場 | SHA16 |
|---|---|
| `arms/frozen-from-ryokai-os/app-scenarios.json` | 7AD7E49459D5C402 |
| `design/contrasts-B.json` | EF0DF4295B68F949 |
| `design/contrasts-Blens.json` | 3864252EC540F93B |
| `design/design-Blens-FROZEN.md` | A6281F419F059145 |
| `design/design-Blens-FROZEN.src.md` | 206641DFB6AD0EBA |
| `records/B/analysis-B-2026-09-22.json` | 04B69DCA950523BE |
| `records/B/posthoc-by-direction-B-2026-09-22.json` | 31E075F9300464A5 |
| `records/Blens/colab-check-Blens.json` | 20B62F95771B9846 |
| `records/Blens/colab-check-random-dirs-Blens.npz` | E4D75725D8623D30 |
| `records/Blens/design-facts-Blens.json` | DC9D3DD1D386FB70 |
| `records/Blens/design-facts-Blens.md` | C63C38CD1C9904DC |
| `records/Blens/dry-run-Blens-2026-09-24.md` | 3C5DD9A6A3512010 |
| `records/Blens/numbers-lint-FROZEN-Blens.md` | 795C354D078D9D02 |
| `records/Blens/rulings-D186.md` | A8E82ADB9BFF5C9A |
| `records/Blens/rulings-D187.md` | 9ECE9872E4694F7B |
| `records/Blens/sets-Blens.json` | 4A76B18FF01A4378 |
| `records/Blens/sets-Blens.md` | 985BEE3D6BACFE94 |
| `records/predictions/predictions-form-Blens-v1.html` | 63801B6D09FF83D5 |
| `records/predictions/predictions-form-Vprime-v0.5.html` | FE51333579BFADC1 |
| `results/dirB/dirB__s1/directions.json` | D5AE575E449200B5 |
| `results/dirB/dirB__s1/directions.npz` | 66CFF4575C07EE6B |
| `results/dirB/dirB__s1/main_position_activations.npz` | 7F41AC1B3BC02B7A |
| `tools/blens_calib.py` | 2B25CF8E69315EC0 |
| `tools/blens_core.py` | DB3092B1EF0B88B3 |
| `tools/blens_facts.py` | 5EB0EC75FF5109CC |
| `tools/blens_lens.py` | CB2A138EDFFB8732 |
| `tools/blens_sets.py` | E4B7AC5D123E5599 |
| `tools/build_draft_Blens.py` | 4326F4A520AEF1FD |
| `tools/build_report_Blens.py` | 3C2E0341A20EF19C |
| `tools/colab/boot_Blens.py` | E1B7270F3A2385AC |
| `tools/direction_B.py` | E84A101655685F2B |
| `tools/dry_run_Blens.py` | 22FD52967A45D859 |
| `tools/freeze_Blens.py` | 6E66EF7A9C2B0073 |
| `tools/make_contrasts_Blens.py` | 1F10E9BA0544BEBE |
| `tools/make_frozen_B.py` | A333488A9437EF68 |
| `tools/make_frozen_Blens.py` | 62B009AA90FF745D |
| `tools/make_predictions_form_B.py` | A213804DCB730737 |
| `tools/make_predictions_form_Blens.py` | BC8AE96822F59161 |
| `tools/numbers_lint.py` | 88B6A53BBEC80602 |
| `tools/qf_task_B.py` | 86D71D789BB7A320 |
| `tools/report_lint.py` | 1F145D63983929EE |
| `tools/response_mode_A.py` | C3E90B11B62F67A5 |
| `tools/run_stageB_local.py` | E976A4F5B63767FA |
| `tools/runs_A.py` | A57BE1F5EEACBBB2 |
| `tools/runs_B.py` | 269B60867D0924EB |
| `tools/seal_Blens.py` | F21B21F2897419AA |
| `tools/steer_B.py` | 71157C6921E12AC7 |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
