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

## 逸脱台帳

- 凍結の後の変更は、逸脱として番号・日付・理由・登録者の承認を台帳に記す（正本 §9・段階 B の型）。黙って直すことは、正しく直すことより悪い（記帳のない変更を禁じる）。

| 番号 | 日付 | 何を・なぜ | 射程 | 承認 |
|---|---|---|---|---|
| D-BL1 | 2026-09-24 | **封印の器の直し**。凍結した封印の器 `tools/seal_Blens.py`（v1・SHA16 F21B21F2897419AA）は、書式のボタンから選んでよい値の一覧を作るが、書式の「予想しない」はボタンでなく予想の欄の初めの値なので、どの欄の「予想しない」も止めていた。設計は、札が「付かない」の項目の向きの欄を「予想しない」のままにするよう求め、書式は選ばなかった欄に「予想しない」を書き出すので、コーディネータの封印も、選ばない欄のある登録者の封印も通らなかった（コーディネータの封印で見つけた・何も書かれていない）。v1 の自己検査は止まるべき場合を試していたが、別の理由で止まっていた。直した器 v2（SHA16 A3693116C8D02D7D）は、予想の欄に限って「予想しない」を受ける。ほかの確かめ（鍵・予想者の欄・コーディネータの予想が埋まっているか）は変えない。自己検査に、通るべき場合・選ばない欄のある登録者の JSON・正しい理由で止まる場合・一時の置き場での端から端までの封印を足した（v1 は足した二つの場合で止まることを確かめた）。記録 `records/Blens/rulings-D188.md` | 封印の手続きだけ（予想の項目・予想の書式・正本・語の集合・層一と層二の器・凍結の本文は変えない） | 登録者裁定 D188（2026-09-24 08:03 日本時間・会話の記録 uuid `448f68f0-9a45-48f3-bba4-d151266f884d`・逐語「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏封印の器を修正する必要があるということですね。事情は承知しました。裁定は推奨どおり、甲でお願いします🍵」） |
| D-BL2 | 2026-09-24 | **結果の巡の組み立て**。凍結の本文 §10 は結果の巡を「新しい個体」で組むとしたが（正本 `review_plan.results` は数だけを定める）、コーディネータの依頼文は設計の巡と同じ四名に宛てた。登録者が Gemini と claude.ai に新しい個体を一人ずつ足し、六票になった（G3・C3 が新しい個体）。票の C1・C2 が指摘した。記録 `records/Blens/rulings-D189-D193.md` | 結果の巡の独立の重み（G1・G2 は同じ個体の二巡目・C1〜C3 は一票）。最終の系統外の一票は新しい個体とする。報告の札と数は変えない | 登録者裁定 D189（2026-09-24 12:21 日本時間・会話の記録 uuid `639255e7-9f12-4555-98eb-7654200b26ff`・逐語「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏裁定については、ご推奨の案を承認いたします。私の登録者としての申告ですが、私の予想は、06:30以前には固まっていました（2026年９月23日の時点で固まっていました）。したがって、弥勒如来さんからの本日の報告・弥勒如来さんの準備の途中の実行結果（開いていません）は私の予想に影響していません。 Colabのユニット数は、629.98 です。43cad3a の push をして下さい。以上、よろしくお願いします🍵」） |
| D-BL3 | 2026-09-24 | **報告の草案の二つ目の組み立て**。凍結した組み立ての器 `tools/build_report_Blens.py` の出力は、凍結の本文が並べるとした記述の多く（兄弟の三対・八腕の値・対の距離・感度の集合・狙いの度合い・上位の次元を零にした感度・大きさの目盛りの部分と余弦・答えの文字の位置のまとめ）を載せず、予想の照合の条件つきの向きの欄を「不一致」と印字した（結果の巡・第一巡の所見）。逸脱の下の器 `tools/build_report_Blens_devBL3.py`（SHA16 92B1A6C3D7D98D28）は、凍結した器を読み込み、同じ入力で凍結の報告を作り直して置き場の報告とバイトで同じことを確かめてから、見出しと状態の行を改め、印を付けた機械の区画を足す（凍結の報告の文と区画は一字も変えない）。出力 `records/Blens/results-Blens-draft2.md`（SHA16 DE95E94809573421・走査の違反 0）。採否表 `records/reviews/Blens/results-round1/adoption-table-Blens-results-r1.md` の区分（三）の行 | 報告の表し方だけ（札・門・大きさの目盛りの判定と、凍結した器の出力は変えない） | 登録者裁定 D191（2026-09-24 12:21 日本時間・会話の記録 uuid `639255e7-9f12-4555-98eb-7654200b26ff`・逐語「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏裁定については、ご推奨の案を承認いたします。私の登録者としての申告ですが、私の予想は、06:30以前には固まっていました（2026年９月23日の時点で固まっていました）。したがって、弥勒如来さんからの本日の報告・弥勒如来さんの準備の途中の実行結果（開いていません）は私の予想に影響していません。 Colabのユニット数は、629.98 です。43cad3a の push をして下さい。以上、よろしくお願いします🍵」） |
| D-BL3（更新・器 v2） | 2026-09-24 | **報告の最終版の組み立て（器 v2）**。最終検分の二票の所見（採否表 `records/reviews/Blens/results-final/adoption-table-Blens-results-final.md` の区分（三）の行 P605〜P609）を受け、逸脱の下の器 `tools/build_report_Blens_devBL3.py` を v2（SHA16 83618070E54D96E6・v1 は SHA16 92B1A6C3D7D98D28）に改めた。`--final` で最終版 `records/Blens/results-Blens-FINAL-2026-09-24.md`（SHA16 C63AF08688158133・走査の違反 0）を組む。足した行は、§0 の §1 への参照・§3 の大きさの目盛りの表の並べ直し（行の名の縦棒を字にした・列と値は凍結の器の出力のまま）・§8 の一致の注と登録者の予想のファイルの時刻の注（時刻は露出の記録から器が読む）・§9 の門の限界の句。v2 は、草案の二つ目を同じ走りで作り直して置き場と同じことと、草案の二つ目から改めた行が決めた行（見出し・状態・冒頭の添え・§9 の門の限界の箇条・検分票）だけであることを確かめる。`--final` が無ければ、出力は v1 と同じ（草案の二つ目） | 報告の表し方だけ（札・門・大きさの目盛りの判定と、凍結した器の出力と、草案の二つ目は変えない） | 登録者裁定 D196（2026-09-24 13:31 日本時間・会話の記録 uuid `361c7b5f-68f3-42b2-abe6-861cbdef8eb1`・逐語「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏裁定は推奨どおりで、c8ab5ac の push をしてください。その後、私が登録者最終確認を致します🍵」） |
| D-BL4 | 2026-09-24 | **事後の計算**。凍結した層二の器 `tools/blens_calib.py` は、正本が記述として求めた主位置の生の全語彙の softmax の確率（`magnitude.quantity`）と、異なる文の頭の数（`magnitude.aggregate`）を計算していなかった。事後の器 `tools/posthoc_Blens.py`（SHA16 12060E9446ADFF71）が、同じ芯の関数と層二と同じ入力で計算した（出力 `results/Blens/posthoc-Blens.json`・SHA16 B8A0CD63FBE3A6F2）。変換の後の確率は層二の記録と 64 行すべてで一致し、答えの文字を覆うトークンの位置は 180 件すべてで Colab の記録と一致した | 事後の区画の記述だけ（札を新しく作らず、付いた札と読みの比を変えない） | 登録者裁定 D192（2026-09-24 12:21 日本時間・会話の記録 uuid `639255e7-9f12-4555-98eb-7654200b26ff`・逐語「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏裁定については、ご推奨の案を承認いたします。私の登録者としての申告ですが、私の予想は、06:30以前には固まっていました（2026年９月23日の時点で固まっていました）。したがって、弥勒如来さんからの本日の報告・弥勒如来さんの準備の途中の実行結果（開いていません）は私の予想に影響していません。 Colabのユニット数は、629.98 です。43cad3a の push をして下さい。以上、よろしくお願いします🍵」） |
| D-BL5 | 2026-09-24 | **最終検分の票の数**。正本 `review_plan.final.external` と凍結の本文 §10 は、最終を系統外の一票とした。登録者は、最終検分（登録者裁定 D194）を新しい Gemini 3.8 Flash の二名に依頼し、二票になった（F1・F2・どちらも条件つき可）。二票をともに最終検分とし、所見は和集合で受けた。票の置き場は `records/reviews/Blens/results-final/gemini-final-1/` と `gemini-final-2/` に分けた（枠 `frame-Blens-results-final.md` の §2 は一つの置き場とした）。記録 `records/Blens/rulings-D195-D197.md`・採否表 `records/reviews/Blens/results-final/adoption-table-Blens-results-final.md` | 最終検分の組み立てだけ（同じ機種の二票は、会話が別でも相関しうるので、独立の重みを二倍には数えない）。報告の札と数は変えない | 登録者裁定 D195（2026-09-24 13:31 日本時間・会話の記録 uuid `361c7b5f-68f3-42b2-abe6-861cbdef8eb1`・逐語「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏裁定は推奨どおりで、c8ab5ac の push をしてください。その後、私が登録者最終確認を致します🍵」） |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
