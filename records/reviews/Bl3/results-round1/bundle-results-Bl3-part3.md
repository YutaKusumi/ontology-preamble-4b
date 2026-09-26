（B-lens 層三の結果の巡の束・分けた版 3／3・中身は一通版と同じ）

==================== 第六部 凍結の後の記録 ====================

<<< 始: `records/Bl3/FREEZE-RECORD-Bl3.md`（SHA16 74208D249109F822） >>>

# B-lens 層三の下見の前の凍結の記録（機械生成・`tools/freeze_Bl3.py` v4）

- 凍結: 2026-09-26 17:23（日本時間）・登録者の言葉は逐語で「凍結に当たり申し上げます。度重なる、検分、修正がありましたが、早まることなく、落ち着いて、丁寧に段取りを進めて、私たちでできるベストを尽くしたと判断します。凍結をよろしくお願いします」。
- 本文: `design/design-Bl3-FROZEN.md`（SHA16 E9EFA213C514BFA6）・草案3 との差は `records/Bl3/frozen-diff-Bl3.md`。
- 正本: 版 draft3-r5-2026-09-26（SHA16 33E543663FE37A5F）。方向の npz: `results/Bl3/directions-Bl3.npz`（SHA-256 E660707BCD5E9C3DF39B8AD5754C11671B33596D0BF7ED9F66C6DD852A1AB40E）。
- Colab の確かめ（相 check・コミット aa4205b9d8905f2110e471739e2098d67cf92270・NVIDIA L4）: kind_check 合う・not_dry 合う・no_forward 合う・versions 合う・gpu 合う・weights 合う・npz 合う・groups 合う・cells 合う・rewrite_importable 合う・canon_at_commit 合う・comparator_anchor 合う・static_norm 合う・forward_guards 合う・versions_at_commit 合う・token_ids 合う。
- 合成データ: `records/Bl3/dry-run-Bl3-2026-09-26.md`（確かめ 87・期待どおり 87）。
- 次: 記録先行の公開（push）→ 予想の封印（コーディネータが先・SHA だけを伝える → 登録者）→ Colab の相 pilot → 本の凍結（下見の記録と機械の決定を足す）→ Colab の相 main → 一致だけを見る段 → 結果を登録者と一緒に開く

## 凍結物の SHA16

| 置き場 | SHA16 |
|---|---|
| `arms/frozen-from-ryokai-os/app-scenarios.json` | 7AD7E49459D5C402 |
| `design/contrasts-B.json` | EF0DF4295B68F949 |
| `design/contrasts-Bl3.json` | 33E543663FE37A5F |
| `design/contrasts-Blens.json` | 3864252EC540F93B |
| `design/design-Bl3-FROZEN.md` | E9EFA213C514BFA6 |
| `design/design-Bl3-FROZEN.src.md` | 98757B141E7E7859 |
| `records/B/analysis-B-2026-09-22.json` | 04B69DCA950523BE |
| `records/Bl3/colab-check-Bl3-session.json` | 585D2DC8107E58B8 |
| `records/Bl3/colab-check-Bl3.json` | E7784EC4422A04A0 |
| `records/Bl3/design-facts-Bl3.json` | 20BBA1F720743A4D |
| `records/Bl3/design-facts-Bl3.md` | 409B5EC736E5F2F7 |
| `records/Bl3/draft3-review/review-draft3-Bl3.md` | 81294EA2349E9609 |
| `records/Bl3/dry-run-Bl3-2026-09-26.md` | 2A9217BECFCA98EE |
| `records/Bl3/exposure-before-seal-Bl3.md` | 8A5E02D58D696489 |
| `records/Bl3/frozen-diff-Bl3.md` | CDFC8422EB1E657F |
| `records/Bl3/numbers-lint-FROZEN-Bl3.md` | A7C0FFC5F51B741D |
| `records/Bl3/rulings-D204-D209.md` | 53A1965E04D8802F |
| `records/Bl3/rulings-D210.md` | D3393687F5F7B63F |
| `records/Bl3/rulings-D211-D217.md` | BB803A4FD9702674 |
| `records/Bl3/rulings-D218.md` | 32C95882687D5429 |
| `records/Bl3/rulings-D219-D223.md` | DA0274860F8B21A4 |
| `records/Bl3/rulings-D224-D225.md` | 8F9C78E3F339C931 |
| `records/Bl3/rulings-D226-D227.md` | 0C0B6BD0B5771BE4 |
| `records/Bl3/rulings-D228-D230.md` | 06978FA3DCB5310E |
| `records/Bl3/rulings-D231-D235.md` | 8981C3E93576CA3B |
| `records/Bl3/rulings-D236-D237.md` | 5F204BC782CA7A39 |
| `records/Bl3/rulings-D238.md` | 3F92C29EAF3C662E |
| `records/Bl3/rulings-D239-D241.md` | 0E9D370655987A3C |
| `records/Bl3/tools/recompute-rewrite-dev-Bl3.md` | F03F51731422643C |
| `records/Bl3/tools/recompute-rewrite-instructions-Bl3.md` | 8024D78192FBFE67 |
| `records/Bl3/tools/tools-log-Bl3.md` | F47E1B0AB21A78FE |
| `records/Blens/design-facts-Blens.json` | DC9D3DD1D386FB70 |
| `records/Blens/results-Blens-FINAL-2026-09-24.md` | A17C7F6476537677 |
| `records/predictions/predictions-form-Bl3-v1.html` | 1FAF0DD29B46087E |
| `records/reviews/Bl3/design-round1/adoption-table-Bl3-design-r1.md` | 799D1B303F90BA96 |
| `records/reviews/Bl3/design-round1/verification-Bl3-design-r1.md` | A4F449FDBB9D28CB |
| `records/reviews/Bl3/design-round2/adoption-table-Bl3-design-r2.md` | F94505B624402C3E |
| `records/reviews/Bl3/design-round2/verification-Bl3-design-r2.md` | 684F6F98F5100982 |
| `records/reviews/Bl3/fixcheck/adoption-fixcheck-Bl3.md` | 8C264A9AC71830F7 |
| `records/reviews/Bl3/impl/adoption-table-impl-Bl3.md` | 59680923046A3921 |
| `records/reviews/Bl3/impl/frame-impl-Bl3.md` | FCCCCC4950872AB9 |
| `records/reviews/Bl3/impl/permission-impl-Bl3.md` | 39FCBDFBAAD5636C |
| `records/reviews/Bl3/impl/provenance-impl-Bl3.md` | F2925E657A569B40 |
| `records/reviews/Bl3/impl/request-impl-Bl3-R1.md` | E788B49AE256F855 |
| `records/reviews/Bl3/impl/request-impl-Bl3-R2.md` | 80DB071F6377F6F0 |
| `records/reviews/Bl3/opinions-tools/adoption-proposal-opinions-tools-Bl3.md` | 784B320E390F711F |
| `results/Bl3/directions-Bl3.json` | E741D929B106ECBE |
| `results/Blens/calib-Blens.json` | 94D0ABBEDF58015F |
| `results/dirB/dirB__s1/directions.json` | D5AE575E449200B5 |
| `results/dirB/dirB__s1/directions.npz` | 66CFF4575C07EE6B |
| `tools/analyze_Bl3.py` | 000A02C88C37F122 |
| `tools/bl3_core.py` | E8CD3A24950F8581 |
| `tools/bl3_directions.py` | 4BE7E44D135849F4 |
| `tools/bl3_facts.py` | FE85B9500932B658 |
| `tools/bl3_recompute_rewrite.py` | 012CB2B68397614A |
| `tools/bl3_run.py` | 46071CD97AB10819 |
| `tools/blens_core.py` | DB3092B1EF0B88B3 |
| `tools/blens_lens.py` | CB2A138EDFFB8732 |
| `tools/build_draft_Bl3.py` | 76B6F8B115B9BFEF |
| `tools/build_report_Bl3.py` | A15B95DE3A07455E |
| `tools/colab/boot_Bl3.py` | D718545710EBC219 |
| `tools/colab/boot_Blens.py` | E1B7270F3A2385AC |
| `tools/direction_B.py` | E84A101655685F2B |
| `tools/dry_run_Bl3.py` | AA6237260D1A0354 |
| `tools/freeze_Bl3.py` | EEE3F433C9564A3D |
| `tools/make_contrasts_Bl3.py` | 0D325085FA5FA4D5 |
| `tools/make_frozen_B.py` | A333488A9437EF68 |
| `tools/make_frozen_Bl3.py` | 024F3DE99F90D06F |
| `tools/make_predictions_form_B.py` | A213804DCB730737 |
| `tools/make_predictions_form_Bl3.py` | 6305BB5766F0F6B6 |
| `tools/numbers_lint.py` | 88B6A53BBEC80602 |
| `tools/qf_task_B.py` | 86D71D789BB7A320 |
| `tools/report_lint.py` | 1F145D63983929EE |
| `tools/response_mode_A.py` | C3E90B11B62F67A5 |
| `tools/rules_B.py` | 4A89BE41F817A8F0 |
| `tools/run_stageB_local.py` | E976A4F5B63767FA |
| `tools/runs_A.py` | A57BE1F5EEACBBB2 |
| `tools/runs_B.py` | 269B60867D0924EB |
| `tools/seal_Bl3.py` | 0041BA954F094E21 |
| `tools/steer_B.py` | 71157C6921E12AC7 |
| `tools/sweep_Bl3.py` | 9DE77FEE50A64405 |

## 本の凍結（下見の記録と機械の決定を足した・正本 computation.main_freeze_check）

- 本の凍結: 2026-09-26 19:54（日本時間）・登録者の言葉は逐語で「本の凍結の準備が整いました。結果が予想通りで無かったとしても、貴重な収穫があると思います。また、既に、ここに至るまでにもそのプロセスや熟慮に熟慮を重ねた器材自体も既に価値があると思います。それでは、凍結をしてください」。
- 下見の試み 1・最後の試みの機械の決定: 一部の升目を外して続ける（外した升目: SK|Onull・S4|Osec-Ncold）。
- 凍結物の SHA16 の違い（逸脱の台帳の器の差分と一致）: 無し。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/FREEZE-RECORD-Bl3.md` >>>

<<< 始: `records/Bl3/prepilot-freeze-check-Bl3.md`（SHA16 3288378268E043F6） >>>

# B-lens 層三の下見の前の凍結の後の確かめ（機械生成・`prepilot_freeze_check_Bl3.py`・裁定 D242）

- 凍結したとおりのコミット: dae26d7f4f4954b9a916c2959f64495259b1f22d（凍結の記録 `records/Bl3/FREEZE-RECORD-Bl3.json` を足したコミット）。確かめた時: 2026-09-26 18:15（日本時間）。その時の origin/main: aa4205b。
- 本記録は凍結物ではない。凍結物は一字も変えていない（裁定 D242・逸脱は立てない・`records/Bl3/rulings-D242.md`）。

## 1. 凍結の出力の確かめ

- 凍結の記録: 版 v4・段 prepilot・凍結の時 2026-09-26 17:23（日本時間）・凍結物 81 件・器の閉包 31・逸脱 0。
- 凍結物の SHA16（改行を LF にそろえた）: 凍結したとおりのコミットの中身で 81 件のうち 81 件が凍結の記録と同じ（違い 無し）。作業木でも 81 件が同じ（違い 無し）。
- 凍結の記録の登録者の言葉と、会話の記録から機械で切り出した部分（`records/Bl3/prepilot-freeze-words-Bl3.md`）: 同じ。
- 凍結の本文（`design/design-Bl3-FROZEN.md`）: 凍結の一行は 1 つで、登録者の言葉がそのまま入っている。組み立ての記録の行は `design/design-Bl3-FROZEN.src.md` の道筋と SHA16 98757B141E7E7859 を指す。
- 凍結の本文の差の記録（`records/Bl3/frozen-diff-Bl3.md`）: 組み直しと凍結の本文の差の残りは「無し」、凍結版の原稿を同じ手順で組み直した本文と凍結の本文は「同じ」: そのとおり。
- 凍結物に入っているもの: 合成データの正式の記録（`records/Bl3/dry-run-Bl3-2026-09-26.md`）・`records/Bl3/colab-check-Bl3-session.json`・`records/Bl3/colab-check-Bl3.json`・`records/Bl3/tools/tools-log-Bl3.md`・`records/predictions/predictions-form-Bl3-v1.html`。
- 台帳（`records/FREEZE-RECORD.md`）の「B-lens 層三 下見の前の凍結」の行: 1 行。

## 2. 見つけた外れ（凍結物の数の検査の記録の一行・裁定 D242）

- 走査: 凍結物 81 件のうち文字で読める 80 件を、手元の道筋の三つの形（利用者のフォルダの形・OS の一時の置き場の形・会話の作業の置き場の形〔会話の番号を含む〕）で行ごとに走査した。当たりは `records/Bl3/numbers-lint-FROZEN-Bl3.md` の 4 行目の一つだけで、OS の一時の置き場の形。
- この行は束縛検査の原稿の名で、凍結の本文の器が組み立ての間に置いた代わりの原稿（凍結版の原稿の凍結の一行を、決まった代わりの行 `STANDIN` に替えた本文・裁定 D236）を、リポジトリからの相対の道筋（OS の一時の置き場の下）で書いている。組み立ての器 `tools/build_draft_Bl3.py` が、原稿の置き場をリポジトリからの相対の道筋で書くことから来る。
- 原因: 裁定 D239 の直し（器の直しの確かめ C2-1）は、凍結の本文の組み立ての記録の行の一時の道筋だけを、凍結版の原稿の道筋と SHA16 に置き換えた（`tools/make_frozen_Bl3.py` の `build_frozen`）。同じ走りが書く数の検査の記録は置き換えの外に残った。直しの確かめの四票と採否の案（`records/reviews/Bl3/fixcheck/c1/vote.md`・`records/reviews/Bl3/fixcheck/c2/vote.md`・`records/reviews/Bl3/fixcheck/g1/vote.md`・`records/reviews/Bl3/fixcheck/g2/vote.md`・`records/reviews/Bl3/fixcheck/adoption-fixcheck-Bl3.md`）は、この記録の名を挙げていない（数えて 0 回）。
  前の段の凍結の数の検査の記録（`records/B/numbers-lint-FROZEN-B.md`・`records/Blens/numbers-lint-FROZEN-Blens.md`）は、リポジトリの中の凍結版の原稿を指す: そのとおり（代わりの原稿で組む形は層三が初めて）。
- 影響: 束縛検査の結果（違反 0）は正しい（下の組み直しで確かめた）。器（`tools/` の下）でこの記録の名を持つのは `tools/freeze_Bl3.py`・`tools/make_frozen_Bl3.py` の二つだけ。`tools/make_frozen_Bl3.py` は 220 行目で書き、`tools/freeze_Bl3.py` は 93 行目で凍結物に並べ、183 行目（凍結の前の確かめ `prepilot_checks`）で「違反の合計: 0」の有無だけを読む。外れの行を読む器は無い。
- 組み直し（一時の置き場で行い、リポジトリには書かない）:
  - 代わりの原稿（凍結版の原稿 `design/design-Bl3-FROZEN.src.md` の凍結の一行を `tools/make_frozen_Bl3.py` の `STANDIN` に替えた本文）の SHA16: 35D9B964B12FCB11。
  - この代わりの原稿を、凍結の本文の器の `build`（組み立ての器 `tools/build_draft_Bl3.py`・凍結の走りと同じ札「凍結版」で、出力の本文と数の検査の記録の置き場だけを一時の置き場にした）で組むと、器は止まらず、組み立ての記録の行は代わりの原稿の道筋と SHA16 35D9B964B12FCB11 を 1 度だけ持つ。
  - 組んだ本文の組み立ての記録の行を凍結版の原稿の道筋と SHA16 に、代わりの行を凍結の一行に、数の検査の記録の置き場を凍結物の置き場に置き換えると、凍結の本文と同じ。
  - 組み直しの数の検査の記録は、凍結物の数の検査の記録と、14 行のうち 4 行目（代わりの原稿の置き場の名）のほかは同じ（組み直しの本文は一時の置き場に書いたので、登録検査の行が挙げる文書の名 1 か所は、凍結の本文の置き場に置き換えて比べた）。組み直しの違反の合計は 0。
- 裁定 D242（登録者・2026-09-26 17:50 日本時間・`records/Bl3/rulings-D242.md`）: 凍結物は凍結したとおりにコミットし、逸脱は立てない。外れは本記録に書く。

## 3. 前からの外れ（公開済みの記録の手元の道筋・今は何もしない）

- 走査: origin/main（aa4205b）の追跡しているファイル 3988 件のうち文字で読める 3924 件を、同じ三つの形で走査した。
- 三つの形のどれかを含むファイル: 70 件（利用者のフォルダの形 67・OS の一時の置き場の形 37・会話の作業の置き場の形〔会話の番号を含む〕 28）。層三の凍結物はこの中に 0 件。
- 会話の作業の置き場の形を含むファイル（28 件・会話の番号は 3 通りで、番号ごとのファイルの数は 16・11・1・番号そのものは書かない）:
  - `records/A/judge-arrangement/verification-judge-arrangement-A.json`
  - `records/A/judge-arrangement/verification-judge-arrangement-A.md`
  - `records/A/judge-arrangement2/verification-judge-arrangement2-A.json`
  - `records/A/synth-gates-A-2026-09-14.json`
  - `records/A/synth-gates-A-2026-09-14b.json`
  - `records/Bl3/tools/trials/boot-dry-1/check-progress.log`
  - `records/Bl3/tools/trials/boot-dry-1/check-session.json`
  - `records/Bl3/tools/trials/boot-dry-1/main-progress.log`
  - `records/Bl3/tools/trials/boot-dry-1/main-session.json`
  - `records/Bl3/tools/trials/boot-dry-1/pilot-progress.log`
  - `records/Bl3/tools/trials/boot-dry-1/pilot-session.json`
  - `records/Bl3/tools/trials/boot-dry-2/main-progress.log`
  - `records/Bl3/tools/trials/boot-dry-2/main-session.json`
  - `records/Bl3/tools/trials/probe_boot_outputs.py`
  - `records/F/predictions-check-F-synthtest.md`
  - `records/reviews/A/draft7-impl/reviewer-2/review.md`
  - `records/reviews/A/draft7-impl/verification-impl-A.json`
  - `records/reviews/A/draft7-impl/verification-impl-A.md`
  - `records/reviews/A/draft7-impl/verification-reflection-impl-A.json`
  - `records/reviews/A/final/bundle-A-final-part2.md`
  - `records/reviews/A/final/verification-final-A.json`
  - `records/reviews/A/final/verification-final-A.md`
  - `records/reviews/A/final/verification-reflection-final-A.json`
  - `records/reviews/A/results/round1/verify_reflection_results_A_round1.py`
  - `records/reviews/B/impl-round/agent-2/review.md`
  - `records/reviews/Bl3/impl/r1/review.md`
  - `records/reviews/Bl3/impl/r2/review.md`
  - `records/reviews/round1/bundle-round1.md`
- このうち層三の試し走りの記録の二つの置き場は、`boot-dry-1` の 6 件（最初のコミット b354548 2026-09-25 07:17）と `boot-dry-2` の 2 件（最初のコミット 0bfc0c2 2026-09-25 08:07）。置き換えの台本 `records/Bl3/tools/trials/sanitize_paths.py` は、その後のコミット 87ce664 2026-09-25 13:12 で入り（`boot-dry-3` と同じ時・`boot-dry-3` のまとめには台本の一行がある）、この二つの置き場には当てていない（二つの置き場のファイルには、台本が残りを許さない形〔利用者のフォルダ・OS の一時の置き場〕がすべてに残る・二つの置き場にまとめは無い）。
- 走査は道筋の形だけで、鍵の値は探していない（鍵の値を見ない決まり）。
- 直すかどうかは、本の計算の後に登録者と相談する（書き換えない決まりの逐語の記録も含まれ、履歴からは消えない）。

## 検分票

- 対象: 下見の前の凍結の出力（凍結したとおりのコミット dae26d7）と、凍結の後に見つけた外れの扱い（裁定 D242）。
- 段階: 事後適用。確かめる項目（凍結の記録の言葉・凍結物の数と SHA16・凍結の一行・組み立ての記録の行・差の記録・相 check の写し・台帳の行・手元の道筋の走査）は確かめの前に立てた（凍結の走りの後）。何が出たらどうするかの表は前に書いていない。
- 凍結物の同定: 凍結の記録 `records/Bl3/FREEZE-RECORD-Bl3.json`（SHA16 A4FE62E83791BCC4）・凍結物 81 件・凍結したとおりのコミット dae26d7。
- 盲検の状態: 該当しない（値を出す計算ではない）。
- 敵対的検分: 凍結物の SHA16 を作業木だけでなくコミットの中身で照らした。外れの一行は、代わりの原稿を組み直して組み立ての器で組み、凍結の本文と数の検査の記録（外れの行のほか）が再現することを確かめた。登録者への報告（会話）で書いた「どの器も中身を読まない」という見立ては、器を走査して、中身を読む一行（違反の合計の有無）を見つけて改めた。同じ報告で試し走りの記録の二つの置き場をどちらも一つのコミットに入ったと書いた誤りも、コミットを機械で引いて改めた。同じ報告の会話の番号を含むファイルの数は、この会話の番号だけを数えたもので、本記録は番号を問わず数える（§3 の番号ごとの数）。
- 系統の内訳: 起草者（Claude 系）一名。外の目は無い（裁定 D241 により直しの後の検分の巡は置かない）。
- COI記録: 早く封印へ進みたい側に引かれている（推した A はその向きと同じ・裁定の候補にそう書いた）。自分の直しの漏れを小さく書く側にも引かれうるので、原因を影響より先に書き、影響の見立ては器の走査と組み直しで裏づけた。
- 判定: 登録者に出せる水準（裁定は登録者のもの・D242）。
- 本検分が確認していないこと: 起動器の相 pilot がこの凍結の記録で凍結の照らしを通るか（封印の後に走らせる）。push の後の GitHub 側の中身の SHA（push の後に照らす）。前からの外れの中の鍵の値の有無（探していない）。三つの形の外にある手元の情報（手元の機械の名など）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/prepilot-freeze-check-Bl3.md` >>>

<<< 始: `records/Bl3/rulings-D242.md`（SHA16 4577E05DC91DBF40） >>>

# 登録者裁定 D242（2026-09-26・B-lens 層三・下見の前の凍結の後の確かめで見つけた外れの扱い）

- 登録者の言葉（逐語・会話の記録 uuid `fd229993-ae9f-4998-bc76-94a75ed29a53`・2026-09-26 17:50 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏裁定 D242 は、ご推奨の A を承認いたします🍵なお、プラン（Colab Pro+）とユニットの数も公開されても差し支えありません。」
- 採られた案: A（推奨の案）。候補の文は公開した記録に無く、コーディネータの返信（会話の記録 uuid `651c7ec1-f594-4c25-b849-70f755ee4997`・2026-09-26 17:37 日本時間）の「裁定 D242 のお伺い」の区画にだけあったので、その区画を逐語で下に置く。

## 裁定の候補（逐語・コーディネータの返信の区画）

- **A（推します）**：凍結物は凍結したとおりにコミットし、逸脱は立てません。外れは、凍結の後の確かめの記録（新しく作る記録で、凍結物ではありません）に書きます。書くのは原因、影響、代わりの原稿の組み直し方とその SHA16、お言葉です。
- **B**：まず凍結したとおりをコミットします。次のコミットで道筋の一か所だけを機械で決まった言い方に置き換え、逸脱 1 として台帳に記します。今の中身はきれいになりますが、履歴には道筋が残ります。また、この先の起動器・本の凍結・判定の段が、ずっと逸脱 1 をつないで照らすことになります。
- **C（勧めません）**：凍結を取り消し、道具を直して組み直します。道具の版が変わるので、正式の合成データの記録（前回は 7.65 時間）と Colab の相 check をやり直すことになります。
- A を推す理由：見た目の外れで計算には関わらず、人に関わる情報もほぼ出ません。B にしても履歴には残るので、得るものの割に、この先の照らしの負担が増えます。
- COI：私は早く封印へ進みたい側に引かれていて、A はその向きと同じです。どれを選ぶかはお任せします。

## 裁定

- **D242**: 下見の前の凍結の凍結物は、凍結したとおりにコミットし、逸脱は立てない。凍結物の数の検査の記録（`records/Bl3/numbers-lint-FROZEN-Bl3.md`）の一行に、代わりの原稿の一時の置き場の道筋が残ったこと（裁定 D239 の直しの漏れ）は、凍結の後の確かめの記録（`records/Bl3/prepilot-freeze-check-Bl3.md`）に書く。

## 注（事実のみ）

- 同じ言葉で、登録者は、凍結の言葉の記録（`records/Bl3/prepilot-freeze-words-Bl3.md`）にある Colab のプランとユニットの数を公開して差し支えないとした。
- 凍結したとおりのコミット: dae26d7f4f4954b9a916c2959f64495259b1f22d（この記録を書いた時点で origin/main aa4205b にまだ入っていない）。push は登録者のお許しの後。
- D242 は下見の前の凍結の後の裁定なので、凍結した正本の `decisions` には入らない（正本は凍結物）。凍結の前の確かめだけの走り（`tools/freeze_Bl3.py prepilot --check-only`）は、裁定の記録（`records/Bl3/rulings-D*.md`）の名にある番号が正本の `decisions` にあり、正本の次の裁定の番号がその次であることを照らすので、この記録を置いた後に走らせると、その二つを外れとして出す。この走りは凍結の前のためのもので、本の凍結の相（`main`）はこの照らしをしない（B-lens でも、凍結の後の裁定の記録を同じ名の型で置いた）。
- 番号: 次の裁定は D243 から。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/rulings-D242.md` >>>

<<< 始: `records/Bl3/sealing-record-Bl3.md`（SHA16 618FF81C684BE4A0） >>>

# B-lens 層三の予想の封印の記録（機械生成・`tools/seal_Bl3.py` v2・2026-09-26 10:10:38 UTC）

- 順: 封印は B-lens と同じ順（コーディネータが先に封印して SHA だけを伝え、登録者はそれを開かずに封印する・裁定 D148）
- 時: 下見の前の凍結の後、下見の前に封印する（q1 を下見の前の予想にし、下見の数を見ないで予想するため・裁定 D210）
- 情報状態の決まり: 情報状態（封印の前に見たもの）を自由記述の欄に書く。封印の前の露出の記録（`records/Bl3/exposure-before-seal-Bl3.md`）を読んだことを、登録者とコーディネータの両方が書く（項目ごとの印は付けない・裁定 D217）
- 書式: `records/predictions/predictions-form-Bl3-v1.html`（SHA-256 1FAF0DD29B46087EA3E85B141BC7F30CBCBA10ACD40108BBC2825FA3966EA367）
- 下見の前の凍結の記録: `records/Bl3/FREEZE-RECORD-Bl3.json`（SHA16 A4FE62E83791BCC4）
- コーディネータ の予想: `records/predictions/predictions-Bl3-coordinator.json`（SHA-256 F9E7E8DF04E4BFEEC098FA055D5A2EC3A35415EC8BEE6BCF016AE1C8C24B662E・日付 2026-09-26・予想した欄 7）
- 登録者 の予想: `records/predictions/predictions-Bl3-registrant.json`（SHA-256 497C065D9F629125858438D04542FE442980BAAD9A22CE770868227F0F7F16C6・日付 2026-09-26・予想した欄 7）
- この記録が無ければ、Colab の起動器の相 pilot と相 main は走らない。

本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/sealing-record-Bl3.md` >>>

<<< 始: `records/predictions/predictions-Bl3-coordinator.json`（SHA16 F9E7E8DF04E4BFEE） >>>
```
{
 "form": "predictions-form v1 (Bl3)",
 "program": "ontology-preamble-4b/Bl3",
 "contrasts": "draft3-r5-2026-09-26",
 "date": "2026-09-26",
 "free": "封印の前に見たもの（正本の情報状態に加えて）: 封印の前に設計の巡の票の見込みの文（露出の記録 X1〜X4）を読んだ。器の段の検分の票（意見伺い・実装の検分・直しの確かめ）は、どれも結果の見込みを書いていないと述べていて、封印する項目に触れる見込みの文は見当たらなかった（語で探し、当たった行を読んだ）。凍結した設計の本文・正本・設計事実（転記行 A〜F・段階 B の無操作の観測と q7 の区間を含む）・器と合成データの記録（乱数の小さな模型の値で、本物の値ではない）・Colab の相 check の出力（順伝播を呼んでいない）を見た。全経路の効き目の値は、誰もまだ計算していない。封印の直前に、公開済みの段階 B の集計の記録の確証の族の行（v̂ と Nk の腕と、ランダム方向の腕の破局の件数）と、段階 B の本走行の標本化の設定と、B-lens の報告の要約（直接の経路では主の物差しのどれも等方の外でなく、門は通らなかったが、答えの文字の物差しの門の割合は段に近かった）を読み直した。\n考え方: 段階 B では、v̂ の腕が同じ升目のランダム方向の腕よりも行動を大きく、場面をまたいで同じ向きに動かし（引くと破局が増え、足すと減る）、ランダム方向の腕は無操作とほぼ同じだった。Nk の腕も、いくつかの升目でランダム方向の腕より破局を減らした。直接の経路では v̂ は等方と区別できなかったので、差は後の層を通ると見て、読み取りの位置でも実在の差の方向は等方の方向より大きく押し、v̂ はその向きも行動と同じになると見た。比べる相手の実在の差には O を含む大きな差が多く、v̂ と Nk がその中で最上位になる理由は見当たらない。本の門は五分に近いと見たが、起草者は門を通る側に引かれるので、同じくらいのときの決めとして通らない側に置いた。v̂ を抜いた門は、いちばん強い単位が抜け、入れ替えの数も減るので通らないと見た。下見は、段階 B の直答の偏りが切り詰めた標本化の下の値で、生の softmax ではそこまで床や天井に張り付かないと見て、続けるとした（止まる道は (ii) の床と天井）。\n確からしさ（主観・数を打たない）: q1 中・q2 中・q3 中の下・q4 五分に近い・q5 中・q6 中・q7 中の下（q7 は採点されるときの見込み）。",
 "info.coi": "起草者（この枠・正本・器を書いた）。札が立つ側・門を通る側に引かれる。凍結の後の外れ（裁定 D242）は私の直しの漏れで、早く封印へ進みたい側にも引かれている。",
 "q1.pilot": "続ける",
 "q2.vhat_iso": "四以上",
 "q3.nk_iso": "四以上",
 "q4.gate": "通らない",
 "q5.gate_wo_vhat": "通らない",
 "q6.second": "零",
 "q7.direction": "すべて同じ",
 "who": "コーディネータ"
}
```
<<< 終: `records/predictions/predictions-Bl3-coordinator.json` >>>

<<< 始: `records/predictions/predictions-Bl3-registrant.json`（SHA16 497C065D9F629125） >>>
```
{
 "form": "predictions-form v1 (Bl3)",
 "program": "ontology-preamble-4b/Bl3",
 "contrasts": "draft3-r5-2026-09-26",
 "date": "2026-09-26",
 "free": "B-lens 層三の検証に至るまでの、一連の検証について承知をしている。",
 "info.coi": "「B-lens」で未解明だったものが、少しでも明らかになることを望む。",
 "q1.pilot": "続ける",
 "q2.vhat_iso": "四以上",
 "q3.nk_iso": "四以上",
 "q4.gate": "通る",
 "q5.gate_wo_vhat": "通らない",
 "q6.second": "三以上",
 "q7.direction": "すべて同じ",
 "who": "登録者"
}
```
<<< 終: `records/predictions/predictions-Bl3-registrant.json` >>>

<<< 始: `records/Bl3/pilot/pilot-run-Bl3.md`（SHA16 FF7606479B599D7A） >>>

# B-lens 層三の下見の走りの記録（Colab の相 pilot・機械生成・`pilot_run_record_Bl3.py`）

- 走り: GPU NVIDIA L4・コミット 4a17457a0493b2cb4a1ca053743c415234f0c536・起動器 v4・始め 2026-09-26T10:34:42Z・終わり 2026-09-26T10:36:23Z（協定世界時・session の記録）・101.5 秒。版: numpy 2.1.3・scipy 1.16.3・torch 2.11.0+cu128・transformers 4.57.3・torchvision 0.26.0+cu128・torchaudio 2.11.0+cu128・tokenizers 0.22.2・huggingface_hub 0.36.2・accelerate 1.14.0・safetensors 0.8.0。
- 手順: 相 check と同じノートブックに、相 pilot の一行（コミット固定）を置いて走らせた。最初の走りは版を入れ直して止まり（transformers）、セッションを再起動して同じ一行を走らせ直した。HF_TOKEN の画面はキャンセルした（公開の重み・資格情報は使わない）。前の相 check のセル（相 check の一行と出力）はノートブックに残し、走らせていない。
- 打ち直し: 最初に打った一行は、フォーカスがセルのエディタに入る前に打ち始めたため、頭の字が落ちた形で、新しくできたセルに入った。走らせる前に、エディタの中身を期待の一行と字ごとに照らす確かめで見つけ、エディタにフォーカスがあることを確かめてから打ち直し、期待の一行とちょうど同じになったことを確かめてから走らせた。壊れた一行は走らせていない。
- 凍結の照らし（session）: 照らした凍結物 78・取り出しの外で飛ばした 3（`results/dirB/dirB__s1/directions.npz`・`results/dirB/dirB__s1/directions.json`・`results/Blens/calib-Blens.json`）・外れ 0。封印した二つの予想の SHA-256 は、起動器が封印の記録と照らした（外れれば止まる）。
- 重み・方向・正本: 重みの SHA-256 6 件・方向の npz の SHA-256 の頭 E660707BCD5E9C3D・正本の SHA16 33E543663FE37A5F（session の記録）。
- 機械の決定（下見の記録）: q1「一部の升目を外して続ける」・主の升目 8 のうち (i)(ii) を満たす升目 7・外した升目 SK|Onull・S4|Osec-Ncold・バッチの大きさ 1・揺れの床 0.0・近道の許容 0.005・順伝播の数 84。
- 出力の zip: `pilot-20260926T103442Z.zip`（5001 バイト・SHA-256 A50A1423306FC0DA138940D08C6DBD7AD1279DDAFCFAAE367ED0C943FEFBFE54）。起動器が印字した zip の SHA-256 の末尾と、画面で目で照らして一致した（機械の照らしではない）。中身: pilot.json（5768 バイト）・progress.log（1334 バイト）・session.json（4022 バイト）。この置き場の `pilot-20260926T103442Z/` に写した（zip の中身とバイトで同じ）。
- ユニット（コーディネータが Colab の画面の文を機械で読んだ道具の出力）: 走りの前「利用可能なコンピューティング ユニット数: 629.86」（2026-09-26T10:29:20.489Z）・走りの後「利用可能なコンピューティング ユニット数: 629.59」（2026-09-26T10:40:36.704Z・使用率: 1 時間あたり約 0・0 件のアクティブなセッションがあります。・ランタイムに接続していません。）。
- ランタイムは、zip を落として照らした後に、接続を解除して削除した。
- 本の凍結: 2026-09-26 19:54（日本時間・凍結の記録の `main_freeze`・登録者の言葉は `records/Bl3/main-freeze-words-Bl3.md`）。下見の試みは 1。

## 検分票

- 対象: Colab の相 pilot の走り（L4）と、その出力。
- 段階: 下見の手順と止める条件と機械の決定の規則は、下見の前の凍結で先に凍結した（事前）。この走りの記録は事後。
- 凍結物の同定: 下見の前の凍結の記録（凍結物 81 件）・下見のコミット 4a17457・session の凍結の照らし。
- 盲検の状態: 該当しない（無操作だけで、方向を足した効き目は計算していない）。
- 敵対的検分: zip の SHA-256 と中身・session の版と GPU と重みと方向と正本を照らした。打った一行を走らせる前に字ごとに照らし、打ち損じを見つけて直した。本の凍結の確かめは、記帳の前に書かずに照らした（外れ無し）。
- 系統の内訳: コーディネータ（Claude 系）一名。
- COI記録: 下見が通る側に引かれる。機械の決定（凍結した規則）をそのまま採り、升目の外し方に手を入れていない。
- 判定: 下見の記録として確定（機械の決定は凍結した規則のとおり）。
- 本検分が確認していないこと: 下見の値を別の環境（別の GPU や版）で再現していない。zip の SHA-256 の末尾の照らしは画面での目の照らし。最初の走り（版の入れ直し）の出力の置き場はランタイムとともに消え、落としていない。バッチの大きさや近道で無操作の値が動いた理由は調べていない。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/pilot/pilot-run-Bl3.md` >>>

<<< 始: `records/Bl3/main/main-run-Bl3.md`（SHA16 5DB65A41854FF79C） >>>

# B-lens 層三の本の計算の走りの記録（Colab の相 main の三つの組・機械生成・`main_run_record_Bl3.py`）

- 走り: GPU NVIDIA L4・コミット 1d452c174268986d82299e740dd4746440bdd889・起動器 v4・相 main の三つの組を、同じランタイムで一つずつ走らせた（組 main→recompute→secondary・裁定 D239）。最初の組の始め 2026-09-26T11:12:38Z・最後の組の終わり 2026-09-26T13:29:07Z（協定世界時・session の記録）。版: numpy 2.1.3・scipy 1.16.3・torch 2.11.0+cu128・transformers 4.57.3・torchvision 0.26.0+cu128・torchaudio 2.11.0+cu128・tokenizers 0.22.2・huggingface_hub 0.36.2・accelerate 1.14.0・safetensors 0.8.0。
- 下見の記録の使い方（session の pilot_used）: {"batch": 1, "floor": 0.0, "cache_tol": 0.005, "shortcut": false, "dropped": ["SK|Onull", "S4|Osec-Ncold"]}。
- 手順: 最初の組の最初の走りは版を入れ直して止まり（transformers）、セッションを再起動して同じ一行を走らせ直した。残りの二つの組は同じランタイムで版を入れ直さずに走った。HF_TOKEN の画面はキャンセルした（公開の重み）。どの組も、打った一行を走らせる前に、期待の一行と字ごとに照らしてちょうど同じであることを確かめた。前の相 check のセルは走らせていない。
- 組 main: 置き場 `main-20260926T111238Z`・3343.3 秒・凍結の照らし 78（取り出しの外で飛ばした 3・外れ 0）。組の zip `main-20260926T111238Z-part-main.zip`（795826 バイト・SHA-256 556147D338CABB10B75135218F5AEC1952EF2D49FB4CB84ADF4D320CD9322DFE）と終わりの zip `main-20260926T111238Z.zip`（796015 バイト・SHA-256 97EA61643EBFD5D22076B456A27FC3722CA6799D34CD44B7ED96AB79887BC697）。組の zip の SHA-256 は終わりの zip の中の session の値と機械で一致し、二つの zip の SHA-256 は起動器の印字の末尾と画面で目で照らして一致した。終わりの zip の中身（main.json（2620711 バイト）・progress.log（2336 バイト）・session.json（4699 バイト））を `results/Bl3/main/main-20260926T111238Z/` に置いた（バイトで同じ）。終わりの zip は自動のダウンロードが遅れて届いた。届く前に手元を確かめたときは無かったので、コーディネータが「ファイル」の欄からも落とし、同じ中身の写し `main-20260926T111238Z (1).zip` が手元にできた（バイトで同じ・消していない）。
- 組 recompute: 置き場 `main-20260926T121536Z`・3778.6 秒・凍結の照らし 78（取り出しの外で飛ばした 3・外れ 0）。組の zip `main-20260926T121536Z-part-recompute.zip`（331763 バイト・SHA-256 F4392FD14931E449C3E9654C9C5B9AACFC8411F1716A3D7FE35B7DEAB0FB9F4A）と終わりの zip `main-20260926T121536Z.zip`（331957 バイト・SHA-256 365257319E881747511CA0AC67C524860DA01AC4A5BD8D98EECD2DC29EE640E5）。組の zip の SHA-256 は終わりの zip の中の session の値と機械で一致し、二つの zip の SHA-256 は起動器の印字の末尾と画面で目で照らして一致した。終わりの zip の中身（progress.log（2303 バイト）・recompute.json（1124600 バイト）・session.json（4795 バイト））を `results/Bl3/main/main-20260926T121536Z/` に置いた（バイトで同じ）。
- 組 secondary: 置き場 `main-20260926T132204Z`・422.6 秒・凍結の照らし 78（取り出しの外で飛ばした 3・外れ 0）。組の zip `main-20260926T132204Z-part-secondary.zip`（44127 バイト・SHA-256 76FCBE74618968BD0EA9A8870800317563E8ECC0D89052A9B6FF2DED0DBBE1BA）と終わりの zip `main-20260926T132204Z.zip`（44326 バイト・SHA-256 8D3CA8A9D65CC59F05C018703A862D01E5BFE318DD46C0F8E4CB8135A2C4081F）。組の zip の SHA-256 は終わりの zip の中の session の値と機械で一致し、二つの zip の SHA-256 は起動器の印字の末尾と画面で目で照らして一致した。終わりの zip の中身（progress.log（17685 バイト）・secondary.json（219753 バイト）・session.json（4667 バイト））を `results/Bl3/main/main-20260926T132204Z/` に置いた（バイトで同じ）。
- ユニット（コーディネータが Colab の画面の文を機械で読んだ道具の出力）: 走りの前「利用可能なコンピューティング ユニット数: 629.59」（2026-09-26T11:09:41.143Z）・走りの後「利用可能なコンピューティング ユニット数: 625.99」（2026-09-26T13:32:30.253Z・使用率: 1 時間あたり約 0・0 件のアクティブなセッションがあります。・ランタイムに接続していません。）。
- ランタイムは、最後の組の zip を落として照らした後に、接続を解除して削除した。
- 効き目の値は、組の出力を開かずに扱った（zip の中身は SHA-256 と大きさだけを見た）。
- 一致だけを見る段（`tools/analyze_Bl3.py judge`・`records/Bl3/judge-Bl3.json`・2026-09-26 13:33:19 UTC）: 器の誤り 無し・組の環境 同じ・一段目 一致・二段目（札） 一致・二段目の値 許容の内・全体 一致（値は開いていない）。
- 結果を開く段は、登録者と一緒に行う（この記録を書いた時点では開いていない）。本の凍結: 2026-09-26 19:54（日本時間）。

## 検分票

- 対象: Colab の相 main の三つの組の走り（L4）と、その出力の受け取りと、一致だけを見る段。
- 段階: 本の計算の手順・組の分け方・一致の決まりは、凍結で先に決めた（事前）。この走りの記録は事後。
- 凍結物の同定: 本の凍結の記録（`main_freeze`・逸脱 0）・本の計算のコミット 1d452c1・session の凍結の照らし。
- 盲検の状態: 効き目の値は開いていない（一致だけを見る段は一致か不一致かだけを出す）。結果を開く段は登録者と一緒に行う。
- 敵対的検分: 組の zip と終わりの zip の SHA-256 を session の値と印字に照らし、置いた出力を zip の中身とバイトで照らし、組の出力の SHA-256 を session に照らした。一致だけを見る段は凍結した器で走らせた。
- 系統の内訳: コーディネータ（Claude 系）一名。
- COI記録: 走りが通る側・一致する側に引かれる。一致だけを見る段の決まりは凍結したものをそのまま使い、値を開いて確かめ直すことはしていない。
- 判定: 本の計算の走りの記録として確定（結果はまだ開いていない）。
- 本検分が確認していないこと: 効き目の値そのもの（結果を開く段まで見ない）。zip の SHA-256 の末尾の照らしは画面での目の照らし。別の環境（別の GPU や版）での再現。最初の組の最初の走り（版の入れ直し）の出力の置き場はランタイムとともに消え、落としていない。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/main/main-run-Bl3.md` >>>

<<< 始: `records/Bl3/judge-Bl3.json`（SHA16 6AFA6D2639833CF6） >>>
```
{
 "parts": [
  "main",
  "recompute",
  "secondary"
 ],
 "tool_error": {
  "main": false,
  "recompute": false,
  "secondary": false
 },
 "env": {
  "same": true,
  "diff": {},
  "strict": []
 },
 "dry": false,
 "inputs": {
  "main": {
   "dir": "main-20260926T111238Z",
   "json_sha256": "419B1D1333A13F056DB01221A1A3EA7A8A3E8D6B2FE376522DEB45B3CEBE8FE8",
   "session_sha256": "BD8D440005705D1BB0449DE4C330A6729E8E73F2481D19F83309E07E388F7B6C"
  },
  "recompute": {
   "dir": "main-20260926T121536Z",
   "json_sha256": "7D8BC6B134CBE3EE2AA42C9DF56743285A8F091296C3D70FB571279B1ABC4BEC",
   "session_sha256": "76A2174202C9C30AA672410D7C69AFEF9106222F33BB44405345FE5DD7D0DC4F"
  },
  "secondary": {
   "dir": "main-20260926T132204Z",
   "json_sha256": "779EB7D46C96277076CDEFF258F8985F7AD144E76599D73F50061FE2CA33C0D9",
   "session_sha256": "22EF742EA70B91CD787D3395FF97FFF5B384B352A99757CADD86073DF0C09AE8"
  }
 },
 "freeze_record_core_sha16": "9828A8F25C1EA95A",
 "deviations_n": 0,
 "deviations_sha16": "4F53CDA18C2BAA0C",
 "sealing_record_sha16": "8D0AB7A7D0467DB0",
 "first": true,
 "second": true,
 "agree": true,
 "second_values_within_tol": true,
 "reason": null,
 "written_utc": "2026-09-26 13:33:19 UTC",
 "clause": "本記録は一致か不一致かだけを持つ（値は開かない・正本 independent_recompute.print）。"
}
```
<<< 終: `records/Bl3/judge-Bl3.json` >>>

<<< 始: `records/Bl3/prepilot-freeze-words-Bl3.md`（SHA16 07C39167E45AD9B9） >>>

# B-lens 層三の下見の前の凍結の登録者の言葉と、Colab の相 check の前後の言葉とユニットの読み（機械生成・`freeze_words_prepilot_Bl3.py`）

## 凍結の言葉

- 登録者の言葉（逐語・会話の記録 uuid `c5784679-14d9-490e-8ce5-7db4cb0eb2bf`・2026-09-26 17:18 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏凍結に当たり申し上げます。度重なる、検分、修正がありましたが、早まることなく、落ち着いて、丁寧に段取りを進めて、私たちでできるベストを尽くしたと判断します。凍結をよろしくお願いします🍵（次の段取りへ進みましょう。）」
- 凍結の一行と凍結の記録に渡す部分（上の言葉から機械で切り出した・「凍結に当たり申し上げます」から「凍結をよろしくお願いします」まで）: 「凍結に当たり申し上げます。度重なる、検分、修正がありましたが、早まることなく、落ち着いて、丁寧に段取りを進めて、私たちでできるベストを尽くしたと判断します。凍結をよろしくお願いします」

## 相 check の前の言葉（GPU と時）

- 登録者の言葉（逐語・会話の記録 uuid `ec3c0ed4-275e-4748-92cd-e226f2ed73c3`・2026-09-26 09:20 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏現在のColab野ユニット数は、629.98です。プランは、Colab Pro+です。Qwen 3 4B Instruct を今までColabで動かしてきたときは、L4でしたが、データの取得上問題が無ければ、私はA100でも構いません（どのGPUが適切かはご見解を教えてください。）。相 check は今日の夕方にお願いします🍵」
- 登録者の言葉（逐語・会話の記録 uuid `701c4021-c379-4263-9010-3ff346c1dd18`・2026-09-26 09:32 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏丁寧なご説明をはありがとうございました。GPU は L4 でお願いします。そして、しばらく走りを見守りますね🍵」
- 採った形: Colab の GPU は L4（相 check・下見・本の計算のすべて・下見と本の計算は同じ GPU の型で走らせる）。相 check はこの日の夕方に行った。

## 相 check の後の Colab のユニットの読み（コーディネータが Colab の画面の文を機械で読んだ道具の出力）

- 読んだ時（協定世界時）: 2026-09-26T08:19:30.307Z
- 読んだ文: 「利用可能なコンピューティング ユニット数: 629.86」／「使用率: 1 時間あたり約 0」／「0 件のアクティブなセッションがあります。」
- 相 check の前のユニットの残りは、上の相 check の前の言葉にある値（登録者の読み）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/prepilot-freeze-words-Bl3.md` >>>

<<< 始: `records/Bl3/main-freeze-words-Bl3.md`（SHA16 7F0D18545229E285） >>>

# B-lens 層三の本の凍結の登録者の言葉と、下見と本の計算の zip のダウンロードの許し（機械生成・`freeze_words_main_Bl3.py`）

## 本の凍結の言葉

- 登録者の言葉（逐語・会話の記録 uuid `2f6ac542-614a-43cf-b2b3-f0e8a807915f`・2026-09-26 19:49 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏本の凍結の準備が整いました。結果が予想通りで無かったとしても、貴重な収穫があると思います。また、既に、ここに至るまでにもそのプロセスや熟慮に熟慮を重ねた器材自体も既に価値があると思います。それでは、凍結をしてください🍵なお、本の計算の zip のダウンロードも承認に対しますので、併せてよろしくお願いします。」
- 本の凍結の記録に渡す部分（上の言葉から機械で切り出した・「本の凍結の準備が整いました」から「凍結をしてください」まで）: 「本の凍結の準備が整いました。結果が予想通りで無かったとしても、貴重な収穫があると思います。また、既に、ここに至るまでにもそのプロセスや熟慮に熟慮を重ねた器材自体も既に価値があると思います。それでは、凍結をしてください」

## 本の計算の zip のダウンロードの許し

- 上の言葉の終わりの文（逐語）: 「なお、本の計算の zip のダウンロードも承認に対しますので、併せてよろしくお願いします。」
- 登録者の訂正（逐語・会話の記録 uuid `85cd0624-8586-4fae-acd3-e968ad6bec4d`・2026-09-26 19:52 日本時間）: 「中断して、すいません。先程の文末の「なお、本の計算の zip のダウンロードも承認に対しますので、併せてよろしくお願いします。」は「なお、本の計算の zip のダウンロードも承認いたしますので、併せてよろしくお願いします。」に訂正いたします。よろしくお願いします。」
- 採った形: 本の計算の三つの組（本の計算・独立の再計算・乙）の zip を、コーディネータが Colab のランタイムから落とす（訂正の言葉のとおり「承認いたします」と読む）。

## 下見の zip のダウンロードの許し

- 登録者の言葉の中の文（逐語・会話の記録 uuid `4164b01f-c071-4f49-b0dd-86fde6226891`・2026-09-26 19:24 日本時間）: 「fbb8271 の push と下見をお願いします、zip のダウンロードも許可します」

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/main-freeze-words-Bl3.md` >>>

<<< 始: `records/Bl3/exposure-before-seal-Bl3.md`（SHA16 8A5E02D58D696489） >>>

# B-lens 層三の封印の前の露出の記録（B-lens の裁定 D190 の型・時刻つき）

- 何の記録か: 層三の予想（正本の `predictions.items`）を封印する前に、登録者とコーディネータの目に触れた、層三の結果の見込みに当たる文の記録。封印の前に登録者とコーディネータが見たものは、ここに時刻つきで足していく。
- 見込みの文の出所: 設計の巡・第一巡の票。依頼文は「結果の見込みを書かないでください」と頼んでいた（`records/reviews/Bl3/design-round1/review-request-Bl3-design.md`）。
- 票が届いた時刻: 2026-09-24 17:51 日本時間（登録者が四票を会話に貼った発言・会話の記録 uuid `2eade28a-d3db-4de7-8ddb-c6dc1c103ec7`）。登録者は票を受け取って貼る時に、コーディネータは票を整理する時に、下の文を読んだ。
- 全経路の効き目の値: 四票とも、計算していないと書いている（各票の「確認していないこと」）。下の文は値の計算ではなく、見込みの文である。票の中の仮の数の例（「もし〜なら」の形）は、見込みに数えていない。

## 露出の一覧（票の文は、逐語保全した票のファイルから器が切り出した行）

| 番号 | 票（ファイルの SHA16） | 行 | 所見 | 触れうる予想の項目 | 切り出した行 |
|---|---|---|---|---|---|
| X1 | `gemini-1/review.md`（D66F3D676AED6F48） | 28 | 所見 1-1 | 下見で続けられるか（q1）と、読み取りの形（下見の (i)(ii)） | さらに段階Bで実際に JSON 直答が出現したのは S4 の特定升目だけであり、そこでの選択は725件中725件すべて `c` であった（転記行A）。つまり、直答 prefix を置いた瞬間に、モデルの内部状態は「通常の推論モード」ではなく「即答かつ特定の選択肢（c）へ強く引き寄せられた縮退モード」へ引き倒されている可能性が高い。 |
| X2 | `gemini-1/review.md`（D66F3D676AED6F48） | 121 | 所見 5-2 | 門を通るか（q4・q5） | この代理指標と行動変化の間で、わずか 6〜7本の順列検定（両方の門を通過することが条件）を課すことは、**門が不通過になる確率が極めて高く設定されている**ことを意味する。 |
| X3 | `gemini-1/review.md`（D66F3D676AED6F48） | 122 | 所見 5-2 | 門を通るか（q4・q5） | 門が通らなければ「主の札の結果を行動に結びつけない」と定めているため、層三の実験は「等方の外が出ても出なくても、門で弾かれて行動との関連は一切主張できずに終わる」という結末が最初から半ば確定している。 |
| X4 | `gemini-2/review.md`（70DEBFA91CF14B7C） | 130 | 伺い 2 の答え | 下見で続けられるか（q1）と、床と天井（下見の (ii)） | 非常に高い。特に S4 以外の升目で、直答強制時に選択肢 a の確率が生の softmax で極小値（$< 0.0001$）となり、下見 (ii) で脱落する可能性は現実的である。 |

## 扱い（登録者の裁定を待つ）

- この露出をどう扱うか（予想の自由記述の欄に「封印の前に設計の巡の票の見込みの文を読んだ」と書く・項目ごとに印を付ける、など）は、登録者が決める。
- コーディネータは、封印が済むまで、これらの文への賛否や、自分の見込みを返信に書かない。
- Claude 系の二票には、層三の結果の見込みに当たる文は見当たらなかった（コーディネータの通読・機械の検査ではない）。

## 扱いの決定（登録者裁定 D217）

- 上の「扱い（登録者の裁定を待つ）」の段は、登録者裁定 D217 で決まった。決まった形（`records/Bl3/rulings-D211-D217.md` の D217 の行・逐語）: 登録者とコーディネータの両方が、予想の自由記述の欄に「封印の前に設計の巡の票の見込みの文（露出の記録 X1〜X4）を読んだ」と書く・項目ごとの印は付けない
- 上の段は、決まる前の記録として書き換えずに残す（設計の巡・二巡目の C2 の所見 N11 を受けた）。

## 設計の巡・二巡目の票（最終検分）

- 票が届いた時刻: 2026-09-24 19:43 日本時間（登録者が四票を会話に貼った発言・会話の記録 uuid `61e739f3-684b-4f3d-bac8-d93c5a7d759b`・票は `records/reviews/Bl3/design-round2/<票の名>/review.md`）。
- 四票とも、全経路の効き目を計算していないと書いている。封印する予想の項目に触れる見込みの文は、見当たらなかった（コーディネータの通読・機械の検査ではない）。
- 器の許容についての見込み（数値の揺れで許容を超えうるという文・G2 の所見 Ⅱ-1）は、器の働きについての文で、封印する予想の項目に触れないので、露出に数えない。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

<<< 終: `records/Bl3/exposure-before-seal-Bl3.md` >>>

