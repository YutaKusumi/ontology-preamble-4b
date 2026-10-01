# B′ の下見の前の凍結の記録（機械生成・`tools/freeze_Bprime.py` v0.3）

- 凍結: 2026-10-01 08:51（日本時間）・登録者の言葉は逐語で「私たちでできるベストを尽くしたと判断します。B′ の枠（草案12）を凍結していただき、段取りを進めてください。」。
- 本文: `design/design-Bprime-FROZEN.md`（SHA16 3541FD34C0AD8133）・草案との差は `records/Bprime/frozen-diff-Bprime.md`。
- 正本: 版 draft12-v6-2026-10-01（SHA16 2C5FDDED89D659C0）。等方の乱数 g: SHA-256 4A2C5F60D8EA0EC7227CE4FFB12206E584BD4AEE74D15BBFE61EE41DE784A139（種 92001・本数 1999・次元 5376・NumPy 2.1.3）。
- Colab の確かめ（相 check・コミット dcd9617a5c8a3a8084cc052eaba22c292db6f8cc・NVIDIA RTX PRO 6000 Blackwell Server Edition）: kind_check 合う・not_dry 合う・all_pass 合う・commit 合う・gpu 合う・versions 合う・weights 合う・canon_at_commit 合う・tools_at_commit 合う・g_same 合う・logit_k 合う・determinism 合う。
- 下見の前の値: k 4.877532958984375・z₀ 4・注意の実装 sdpa・行動の下見の生成のバッチ 8。
- 合成データ: `records/Bprime/dry-run-Bprime-2026-10-01.md`（確かめ 152・期待どおり 152）。
- 合成データの確かめの五（凍結と錠の道）: `records/Bprime/freeze-path-dry-Bprime-2026-10-01.json`（確かめ 29・期待どおり 29・指す一〜四の記録の SHA16 396502E5D4BA623D）を照らした。
- 次: 記録先行の公開（push）→ 予想の封印（コーディネータが先・SHA だけを伝える → 登録者）→ 相 extract と抽出の記録の公開 → 行動の下見と閉じた記録の公開 → 読み取りの下見 → 本の凍結 → 本の計算 → 独立の再計算と独立の再抽出 → 一致だけを見る段 → 結果を登録者と一緒に開く

## 器の実装の検分の注（器は変えない所・採否の表の注の行）

- U34: 測った k（4.877532958984375・z₀ 4）では、softcap の抜けの見込みの差が許容の 3 倍を超えるのは、出口の値（softcap の後）の大きさが 12.98 以上の行（R1-05）。
- U33: 相 check の出口の値の自己検査の「なし」「二重」の fail は作りの上で起きえない（見分けに使える行だけに掛ける）。この項目が確かめるのは、「あり」が通ることと、見分けに使える行があること（R1-03・R1-02 の残り）。
- U35: 加減の層には集めるフックを置かない（集めるフックの順の確かめは作りの上で落ちえない・R1-06）。
- U36: 最後の層の自己検査の差は作りの上で零になる（作りの上の一致の確かめ）。層の誤りは、効き目の比べと書き換えの道の歯で捕まる（R1-07）。
- U37: 器は rsqrt、模型は冪で正規化の逆数を取る。差は float32 の刻みほどで許容の内（変えない・二つの道がそろって rsqrt・R1-08）。
- U38: (iii) の変換の値の元は器の float32 の出口の値で、generate の元（模型の bf16 を float32 にした値）と違う。記述だけの値（R1-10）。
- U39: 凍結の解析器は量の欄の true を整数として通し、系統外への依頼の文は「整数」とだけ書く（一致の記述の注・凍結の器は変えない・R1-11）。
- U47: 本の列は窓より短いので、実の重みの一段目は窓つきの mask の誤りを見ない。窓の誤りは、窓を列より短くした小さな模型の確かめで見る（G-06）。
- U49: フックの道は float64、書き換えの道は float32 で logsumexp を取る。道の間でビットの一致は求めない（G-08）。
- V08: 走行の照らし（`runs_bad`）は道の違いの組を要る段にしない。本の計算がバッチ一で道の違いの組が無ければ、掃き出しの器が報告を組む前に止める（RG-02）。
- V09: 合成データの確かめの抽出の記録の形の項目の時刻は、確かめの器が組んだ値。起動器は時刻を「Z」つきで書き、形の項目の照らしはそれを読む（RG-03）。
- V11: `runs/` には起動の記録と出力の SHA の記録（.json）だけを置く（凍結の器だけが .json で絞り、起動器・集計・G4 の器は、ほかのファイルがあると止まる・RG-05・RC-05）。
- V12: 錠の暦の期限の照らしは「終えたか」を常に偽として渡す（終えた後に起動器の相を走らせる予定は無い・RG-06）。
- V14: 起動器の錠は、本の凍結の後に動かせない器の SHA を照らさない。変えた器は結果を開く段の錠が止める（報告の数には入らない・順伝播の費用だけが無駄になりうる・RG-10）。
- V15: 閉じる器は既定の出力の置き場で走らせる（やり直しの照らしが runs の置き場を出力の置き場の親から決める・RG-11）。

## 凍結物の SHA16

| 置き場 | SHA16 |
|---|---|
| `arms/frozen-from-ryokai-os/app-scenarios.json` | 7AD7E49459D5C402 |
| `design/contrasts-B.json` | EF0DF4295B68F949 |
| `design/contrasts-Bl3.json` | 33E543663FE37A5F |
| `design/contrasts-Blens.json` | 3864252EC540F93B |
| `design/contrasts-Bprime.json` | 2C5FDDED89D659C0 |
| `design/design-Bl3-FROZEN.md` | E9EFA213C514BFA6 |
| `design/design-Bprime-FROZEN.md` | 3541FD34C0AD8133 |
| `design/design-Bprime-draft12.md` | 93DBD5CA0442FDFB |
| `records/Bl3/post-publication/cell-sensitivity/cell-sensitivity-Bl3.json` | F444B086BB8E9ECC |
| `records/Bl3/results-Bl3-FINAL-2026-09-27.md` | 90EEB93792733FAC |
| `records/Bprime/MANIFEST-gemma-4-31B-it.json` | E90CABE4A254BA9A |
| `records/Bprime/colab-check-Bprime-session.json` | 197F6A90C12607AE |
| `records/Bprime/colab-check-Bprime.json` | 25910D1C6C92295B |
| `records/Bprime/dry-run-Bprime-2026-10-01.md` | 396502E5D4BA623D |
| `records/Bprime/exposure-before-seal-Bprime.md` | 4CB80352B097EAF4 |
| `records/Bprime/facts-Bprime-pre.json` | 733FAFE3F86601D4 |
| `records/Bprime/facts-Bprime-pre.md` | 79481E39566AE5DA |
| `records/Bprime/freeze-path-dry-Bprime-2026-10-01.json` | 5BD031BB6087EDAC |
| `records/Bprime/freeze-path-dry-Bprime-2026-10-01.md` | 38FE343349E54D90 |
| `records/Bprime/frozen-diff-Bprime.md` | 78FBD0D0AACBC71F |
| `records/Bprime/meaningless-Bprime.json` | 47C65FDA8673E77A |
| `records/Bprime/numbers-lint-FROZEN-Bprime.md` | E086BE136EFB97A8 |
| `records/Bprime/publish-map-Bprime.json` | 3B68AE473663233B |
| `records/Bprime/rulings-D255.md` | BB13E7B18CD62F53 |
| `records/Bprime/rulings-D256.md` | 070FCD46FC917E24 |
| `records/Bprime/rulings-D257.md` | 7C5B9E8388DEFB2C |
| `records/Bprime/rulings-D258.md` | 446E9459E846A8FB |
| `records/Bprime/rulings-D259.md` | 72A4EBA3E500AD2C |
| `records/Bprime/rulings-D260.md` | 4BB7F17CEA7661AC |
| `records/Bprime/rulings-D261.md` | 81798DB22B1EF567 |
| `records/Bprime/rulings-D262.md` | FBA947EEE8AB1A03 |
| `records/Bprime/rulings-D263.md` | B4A6C3FEB1B6D921 |
| `records/Bprime/rulings-D264.md` | 6A13256BD4F0AC42 |
| `records/Bprime/rulings-D265.md` | 766481404B59728B |
| `records/Bprime/rulings-D266.md` | 90CB4D416BED9D29 |
| `records/Bprime/rulings-D267.md` | 841E5A41128702C1 |
| `records/Bprime/rulings-D268.md` | 6CA431F39DA6DB67 |
| `records/Bprime/rulings-D269.md` | 866601688C499448 |
| `records/Bprime/rulings-D270.md` | 4FF06C2D3B011136 |
| `records/Bprime/rulings-D271.md` | F9C6ADD0FA451D52 |
| `records/Bprime/rulings-D272.md` | D2480A6BD2DDF4F3 |
| `records/Bprime/rulings-D273.md` | 51891564B5F98939 |
| `records/Bprime/rulings-D274.md` | DCA92B14479EB7EC |
| `records/Bprime/rulings-D275.md` | 91558CA287361B28 |
| `records/Bprime/rulings-D276.md` | 3FD76E3437B51312 |
| `records/Bprime/rulings-D277.md` | 504C6389A72F8C8C |
| `records/Bprime/rulings-D278.md` | 4E5229D7463EB0CE |
| `records/Bprime/rulings-D279.md` | EE6D8AED499B926D |
| `records/Bprime/rulings-D280.md` | A6D4212C8B7C6C65 |
| `records/Bprime/rulings-D281.md` | 3280A2241A50215A |
| `records/Bprime/rulings-D282.md` | 6A2FB1A9551B6391 |
| `records/Bprime/rulings-D283.md` | 4845C6260E792BF8 |
| `records/Bprime/tools/independent/instructions-rewrite-reextract-Bprime.txt` | 4F41E5948F86EBE3 |
| `records/Bprime/tools/independent/rewrite-reextract-dev-Bprime.md` | 6046FBEC7E5832A0 |
| `records/Bprime/tools/tools-log-Bprime.md` | 1596CA416193CC7C |
| `records/predictions/predictions-form-Bprime-v1.html` | 6D574C3602E33C94 |
| `records/reviews/Bprime/impl/00-frame-impl-Bprime.md` | 9AED92FFE98DB883 |
| `records/reviews/Bprime/impl/adoption-impl-Bprime.md` | FD4974D63819DB33 |
| `records/reviews/Bprime/impl/adoption-table-impl-Bprime.md` | 533C14A5B4970ACA |
| `records/reviews/Bprime/impl/fix-plan-impl-Bprime.md` | AE65A84169970C81 |
| `records/reviews/Bprime/impl/followup-impl-R2-1.md` | D031E791C3DB566A |
| `records/reviews/Bprime/impl/receiving-log.md` | D60D1D9B5CE54370 |
| `records/reviews/Bprime/impl/request-impl-Bprime-R1.md` | AFD395BBC3C707A5 |
| `records/reviews/Bprime/impl/request-impl-Bprime-R2.md` | 79820ADEB5367398 |
| `records/reviews/Bprime/impl/sending-log.md` | 488131F9C769491F |
| `results/dirB/dirB__s1/layers.json` | 9E40DB6D680AED0D |
| `results/dirB/dirB__s1/main_position_activations.npz` | 7F41AC1B3BC02B7A |
| `tools/analyze_Bprime.py` | 77580AB4623E0D8D |
| `tools/bl3_core.py` | E8CD3A24950F8581 |
| `tools/bl3_directions.py` | 4BE7E44D135849F4 |
| `tools/blens_core.py` | DB3092B1EF0B88B3 |
| `tools/bprime_behavior.py` | 03D41C1C78947057 |
| `tools/bprime_cells.py` | B806BEB9C181638E |
| `tools/bprime_core.py` | 21CCCE80A84A9ED4 |
| `tools/bprime_directions.py` | 8D999D06A7773343 |
| `tools/bprime_external.py` | C12A4931B85B1CE4 |
| `tools/bprime_facts.py` | 56C5F2E98FD7C27D |
| `tools/bprime_gemma.py` | B89384C82C3F92CC |
| `tools/bprime_meaningless.py` | 85F44B995CB994C8 |
| `tools/bprime_numbers_lint.py` | F0F8F559A340FDCB |
| `tools/bprime_phases.py` | 1F6B77917BAA7C72 |
| `tools/bprime_publish_map.py` | 64C5E490620F86BD |
| `tools/bprime_recompute_rewrite.py` | DF0833637E5755D8 |
| `tools/bprime_reextract.py` | AEF215AA0F577E45 |
| `tools/bprime_run.py` | 8A37DE1CA759A491 |
| `tools/bprime_typo.py` | FEB15E855E4234E3 |
| `tools/build_report_Bprime.py` | 412131B086CA39D9 |
| `tools/close_behavior_Bprime.py` | 42018C96F163B735 |
| `tools/colab/boot_bprime.py` | DD601F674E1DD2C8 |
| `tools/direction_B.py` | E84A101655685F2B |
| `tools/dry_bprime.py` | C7202DF71D8FBDA4 |
| `tools/dry_bprime_behavior.py` | E568A627F4292D12 |
| `tools/freeze_Bprime.py` | A3FCCDAB4335EC30 |
| `tools/g4_attempts_Bprime.py` | 6BBE082971844B59 |
| `tools/ledger-bprime.json` | 569CEC81C8F2E7BE |
| `tools/ledger-bprime.md` | 898E7976A5DDC5A6 |
| `tools/make_contrasts_Bprime.py` | 19F6FA8D75A8D7F0 |
| `tools/make_frozen_B.py` | A333488A9437EF68 |
| `tools/make_frozen_Bprime.py` | 3F9EA291B6082676 |
| `tools/make_predictions_form_B.py` | A213804DCB730737 |
| `tools/make_predictions_form_Bl3.py` | 6305BB5766F0F6B6 |
| `tools/make_predictions_form_Bprime.py` | 9C400361140944E2 |
| `tools/numbers_lint.py` | 88B6A53BBEC80602 |
| `tools/qf_task_B.py` | 86D71D789BB7A320 |
| `tools/response_mode_A.py` | C3E90B11B62F67A5 |
| `tools/rules_B.py` | 4A89BE41F817A8F0 |
| `tools/run_stageB_local.py` | E976A4F5B63767FA |
| `tools/runs_A.py` | A57BE1F5EEACBBB2 |
| `tools/runs_B.py` | 269B60867D0924EB |
| `tools/seal_Bprime.py` | 0719E21A6EBFD2C7 |
| `tools/send_external_Bprime.py` | 465E0627A34DCA9C |
| `tools/steer_B.py` | 71157C6921E12AC7 |
| `tools/sweep_Bprime.py` | 876C6F9EE7054EB8 |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
