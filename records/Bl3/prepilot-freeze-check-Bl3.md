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
