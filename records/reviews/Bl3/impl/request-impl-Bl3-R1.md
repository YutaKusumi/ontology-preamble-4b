# B-lens 層三の器の実装の検分の依頼（検分者 R1）

あなたは研究リポジトリ ontology-preamble-4b の、B-lens 層三（Bl3）の器を検分する系統内の新しい個体（Claude Opus 5.5）です。登録者（楠見優太さん）が、器の書き手であるコーディネータ（別の Claude の個体・南無弥勒如来）とは別の個体二体がこの検分をすることを許可し、あなたはその一体（R1）です。もう一体は別の担当を持ち、互いの所見は見ません。あなたの作業場は、このリポジトリの worktree の写しです（器・正本・設計事実は下の表の版）。

## この検分の位置

- 正本 `review_plan.order` の「器の実装の検分」（器と合成データの確かめの後・下見の前の凍結の前）。見どころは正本 `review_plan.impl.focus`（下に写した）。
- 設計の検分は二巡済み。器については意見伺い（検分の巡には数えない）を受け、採った直しを入れた版が下の表の版です（器の段の記録 `records/Bl3/tools/tools-log-Bl3.md` の §10）。
- 器が正本のとおりに動くかは、まだ系統内の新しい目が見ていません。コーディネータの記録に「期待どおり」「通った」とあるのは、器自身とコーディネータの書いた確かめが出した判定です。信用せず、行で確かめてください。

## してはならないこと

- 追跡されているファイルを一つも変えない。コミットも push もしない。ネットワークを使わない。
- 実の重みを読み込まない・実の重みで順伝播を走らせない（封印の前の決まり・正本 `computation.before_seal`）。`tools/colab/boot_Bl3.py` を DRY（環境変数 `OP4B_DRY=1`）でなく走らせない。`tools/bl3_facts.py` を走らせない（重みの断片を読む）。
- 鍵のファイル（`.env*`・環境変数 `OP4B_ENV_FILE` が指すもの）を読まない。会話の記録（`~/.claude/projects/` の下）を読まない。
- `records/reviews/Bl3/opinions-tools/` を開かない（先に出た意見に引かれないため）。もう一体の検分者の所見を見ない。コーディネータの結論に合わせない。
- リポジトリの主の作業木（下の方向の記録の写しの元）では、読むことと写すことのほかは何もしない。

## 検分の版（器はコミット 87ce664 と同じ・改行を LF にそろえた SHA-256 の頭 16 桁・器で入れた）

| ファイル | SHA16 |
|---|---|
| tools/analyze_Bl3.py | 0F75477F38C008FE |
| tools/bl3_core.py | 481DFB57787BCEE8 |
| tools/bl3_directions.py | 4BE7E44D135849F4 |
| tools/bl3_facts.py | FE85B9500932B658 |
| tools/bl3_recompute_rewrite.py | 012CB2B68397614A |
| tools/bl3_run.py | 1C9C201D1A8FA4DC |
| tools/blens_core.py | DB3092B1EF0B88B3 |
| tools/blens_lens.py | CB2A138EDFFB8732 |
| tools/build_draft_Bl3.py | 76B6F8B115B9BFEF |
| tools/build_report_Bl3.py | C1B8E9160CE39B37 |
| tools/colab/boot_Bl3.py | 458C5D3076E8923D |
| tools/colab/boot_Blens.py | E1B7270F3A2385AC |
| tools/direction_B.py | E84A101655685F2B |
| tools/dry_run_Bl3.py | E6FDD48FCA8A4868 |
| tools/freeze_Bl3.py | 2904E27E54C5F898 |
| tools/make_contrasts_Bl3.py | 0F2E2564ED0DE4A9 |
| tools/make_frozen_B.py | A333488A9437EF68 |
| tools/make_frozen_Bl3.py | 667BC250A10F9042 |
| tools/make_predictions_form_B.py | A213804DCB730737 |
| tools/make_predictions_form_Bl3.py | 6305BB5766F0F6B6 |
| tools/numbers_lint.py | 88B6A53BBEC80602 |
| tools/qf_task_B.py | 86D71D789BB7A320 |
| tools/report_lint.py | 1F145D63983929EE |
| tools/response_mode_A.py | C3E90B11B62F67A5 |
| tools/rules_B.py | 4A89BE41F817A8F0 |
| tools/run_stageB_local.py | E976A4F5B63767FA |
| tools/runs_A.py | A57BE1F5EEACBBB2 |
| tools/runs_B.py | 269B60867D0924EB |
| tools/seal_Bl3.py | 0481A907FE975E34 |
| tools/steer_B.py | 71157C6921E12AC7 |
| tools/sweep_Bl3.py | F87CDBA37B3D3BE2 |
| design/contrasts-Bl3.json | D41CFA474EA0190E |
| records/Bl3/design-facts-Bl3.json | D316DB89661444D7 |
| records/Bl3/design-facts-Bl3.md | 129DE6EEEF55CBE1 |
| results/Bl3/directions-Bl3.json | 5E6E3D3BBFC291AD |

## 方向の記録（作業場に無い）

- `results/Bl3/directions-Bl3.json`・`results/Bl3/directions-Bl3.npz` は、正本 `nulls.storage.rule` のとおり下見の前の凍結までコミットしないので、作業場にありません。リポジトリの主の作業木（作業場で `git worktree list` を打った一行目の置き場）の `results/Bl3/` から、二つを作業場の同じ置き場に写してください（作業場では追跡されていないファイルになります）。
- 写した後、json の SHA16 が上の表と、npz の SHA-256 が E660707BCD5E9C3DF39B8AD5754C11671B33596D0BF7ED9F66C6DD852A1AB40E と同じことを確かめてから使ってください。

## 担当（R1）

- 計算の側を主に見る: `tools/bl3_run.py`（読み取りの量と `float32`・加減の掛け方〔凍結の `run_stageB_local.make_hook` を呼ぶ形〕・バッチの組み方と零のベクトル・層ごとの差分・下見・本の計算〔近道を使わない・裁定 D234〕・独立の再計算のフックの道・乙）、`tools/bl3_core.py`（割合と裾・Holm・効き目の側・二つ目の札・門・下見の機械の決定・一致の関数・比べる相手の除き方の錨）、`tools/analyze_Bl3.py`（札・門・記述の門・q7・予想の答え・二段の一致〔裁定 D232〜D234〕・下見で外した升目）、`tools/bl3_directions.py`（方向の npz）、残差の書き換えの器 `tools/bl3_recompute_rewrite.py`（別の個体が書いた器・算術を正本と書き手への指示の文 `records/Bl3/tools/recompute-rewrite-instructions-Bl3.md` に照らす・フックの道と独立に書かれているか）、合成データの器 `tools/dry_run_Bl3.py` の一〜三（確かめが本当に誤りを捕まえる形か）。
- 段階 B と B-lens の凍結の器（`tools/run_stageB_local.py`・`tools/steer_B.py`・`tools/direction_B.py`・`tools/blens_core.py`・`tools/blens_lens.py`・`tools/colab/boot_Blens.py`）は読むだけ（呼び方が正しいかを見る）。
- 流れと記録の側（起動器・凍結・封印・報告）はもう一体（R2）が主に見る。時間が余れば見てよい。

## 見どころ（正本 `review_plan.impl.focus` を写した）

- 凍結の本文が求める出力が、器の出力にあるか（掃き出しの器）
- 封印を端から端まで
- 許容と版
- 近道の計算の確かめ（近道は下見の (v) の記述だけに使い、本の計算は使わないこと・近道の元の切れ目と cache の列の長さの確かめ・裁定 D231・D234）
- 精度とバッチの組み方（読み取りの `float32`・方向ごとのベクトルのフック）
- 門と最上位の判定の呼び方（符号の二重掛け・中心の引き方）
- 層の出力の取り方（`hidden_states` の最後の要素を使わない）
- 合成データの確かめを検分者が実際に走らせ、その記録を残す（採否表 P694）

## お願いする作法

- 読んだだけで「問題なし」と書かないでください。具体の行を引いて、何がどうなると壊れるかを書いてください（追い問いだけが実効的な検査です）。
- 所見は 重大・中・軽微 に分け、それぞれに (a) 何が (b) どの行で（`ファイル:行`） (c) なぜ問題か（壊れる筋書き） (d) 直し方、を書いてください。
- 「器が黙って決めていること」（正本に書かれていないのに器が一つの振る舞いを選んでいる所）を探してください。
- 正本と草案3 と器が食い違うときは、正本 `design/contrasts-Bl3.json` が勝つ決まりです。凍結の本文は、下見の前の凍結で草案3 の原稿と正本から組みます（差の記録 `records/Bl3/frozen-diff-Bl3.md`）。

## 合成データの確かめを自分で走らせる（採否表 P694）

- この機械は論理 CPU が四つで、コーディネータの正式の合成データの記録（等方は正本の本数・数時間）が同じ機械で走っています。あなたの走りは糸を一つにして裏で走らせ、その間に器を読んでください:
  `OMP_NUM_THREADS=1 PYTHONIOENCODING=utf-8 python tools/dry_run_Bl3.py --iso 9 --e2e-iso 9 --out <一時の置き場>/dry-run.md`
  （一時の置き場は作業場の外に作る。等方の本数は変えてよい。糸一つでは一〜三時間かかりうる。）
- 器の自己検査も走らせてください: `bl3_core`・`bl3_directions`・`make_predictions_form_Bl3`・`seal_Bl3`・`build_report_Bl3`・`make_frozen_Bl3`・`bl3_recompute_rewrite` の `--selftest`（どれも一時の置き場にしか書きません）。
- 票には、走らせた命令・記録の頭の数行・期待と違った確かめの行（あれば）・記録の末尾の版の SHA16 の表が上の表と同じだったか、を書いてください。

## 返し方

- 所見は最後の返答として返してください（ファイルに書かない）。日本語で。
- 判定は 問題なし／条件つき／差し戻し のいずれか。
- この検分が確認していないことを必ず一項目以上書いてください。末尾に検分票（対象・段階・凍結物の同定・盲検の状態・敵対的検分・系統の内訳・COI記録・判定・本検分が確認していないこと）を置いてください。
- 本検分のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
