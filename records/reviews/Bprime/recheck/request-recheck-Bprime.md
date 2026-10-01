# 検分の依頼（B′ の器の実装の直しの確かめ・凍結の前の最後の検分の巡・2026-10-01）

時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。

あなたには、研究の器（Python のコード）の直しを確かめていただきます。あなたは、この器の書き手（Anthropic の Claude 系の模型・コーディネータ）とは別の個体で、前の巡の検分者とも別の個体です。書き手に同調する必要はありません。直しが表のとおりになっていない所・直しが壊した所・確かめが確かめになっていない所を見つけることが、あなたの役目です。

## まず書いてほしいこと（系統の申告）

返答の一行目に、あなた自身の模型の名と作り手を書いてください（例:「模型: ○○・作り手: ○○」）。

## この検分の位置

- 研究は ontology-preamble-4b の段階 B′（Gemma 4 31B で、層三の読み取りの型を日本語で追試する登録）です。
- 前の巡（器の実装の検分）では、claude.ai の二つのチャットと、系統外の grok-4.7 が器を検分しました。書き手は所見を採否の表（`recheck/adoption-table-impl-Bprime.md`・U01〜U52 と、書き手が器の段で見つけた K25〜K27）にまとめて器を直し、合成データの確かめを Colab の CPU で取り直しました（正式の記録 `records/Bprime/dry-run-Bprime-2026-09-30.md`〔一〜四〕と `records/Bprime/freeze-path-dry-Bprime-2026-09-30.md`〔五・凍結と錠の道〕）。
- この巡は、その直しの確かめで、**凍結の前の最後の検分の巡**です（登録者の裁定 D278・`records/Bprime/rulings-D278.md`）。この巡の後に検分の巡は開きません。見つかった所は、下の物差しで分けて扱います。
- 正本は `design/contrasts-Bprime.json`（版 draft11-v5-2026-09-30）、設計の本文は `design/design-Bprime-draft11.md` です。前の巡の束（SHA-256 `C89AE3FF939C41FFE626B8CBD143281A32E6547691F1871BA46F4CC9A4B2F3F0`）との違いの一覧は `recheck/diff/INDEX.md`（変わったファイル 32・足したファイル 27・外したファイル 0）です。草案10 から草案11 への差分は `recheck/diff/design/design-Bprime-draft10-to-draft11.md.diff` です。
- 検分者は、あなたと、系統外の grok-4.7（実行の場を持たないので、差分と記録を文字で読みます）の二人です。

## 見てほしいこと（見る所は直しに限ります）

1. 採否の表の行（U01〜U52・K25〜K27）ごとに、直しが表に書いたとおりになっているか。差分と今の器で照らしてください。
2. 直しが、ほかの所を壊していないか。たとえば、直しの前に通っていた道が通らなくなる所・器どうしの口（ある器が書く物の名と形と、別の器が読む物）の食い違い・新しく足した器 `tools/g4_attempts_Bprime.py` とそれを呼ぶ所。
3. 合成データの正式の記録の行が、直しを本当に確かめているか（直しが無ければ落ちる行になっているか）。とくに次の所:
   - 起動器の錠（`tools/colab/boot_bprime.py` の `gate_bad`）
   - 抽出の記録の形の項目
   - 閉じる器のやり直しの道（`tools/close_behavior_Bprime.py`）
   - 集計と報告の器の照らし（`tools/analyze_Bprime.py`・`tools/build_report_Bprime.py`）
   - G4 の器（`tools/g4_attempts_Bprime.py`）
   - 合成データの確かめの器の五（`tools/dry_run_Bprime.py` の凍結と錠の道）
4. 正式の記録の後の直し（器の段の記録の K28・裁定 D278）: 報告の組み立ての器 v0.4 が、読みの節の Nk の行の文にだけ「独立の再計算なし」の印を置く形と、合成データの確かめの器 v1.0 で足した行。この二つは正式の記録の後に直したので、記録の SHA の表と合いません（凍結の前に確かめを取り直します）。
- 変わっていない所の新しい検分と、設計の決め（正本と草案の決め）の見直しは、この巡の外です。ただし、直しが設計の決めと食い違う所は挙げてください。

## 重さの物差し（書き手は、この物差しで所見を分けます）

- **重い**: 次のどれかに当たるもの。
  - 報告の数・札・門の判定が変わりうる
  - 錠や凍結が、変わった器や記録を通してしまう
  - 独立の再計算や再抽出が独立でなくなる
  - 誤りがあっても見つからなくなる
- **それ以外**: 凍結の前には直さず、限界の文・注・凍結の後の台帳に回します。報告の数に触れず、最後の確かめの取り直しで覆える所だけは直します。
- 所見ごとに、あなたの見立ての重さと、「重い」なら物差しのどれに当たるかを書いてください。

## 走らせてほしいこと

- 添えた zip を展開し、`README-recheck-bundle-Bprime.md` を読んでから、版を固定して numpy と transformers を入れてください（numpy 2.4.6・transformers 5.16.1）。
- 変わった器のうち、torch の要らない器の自己検査（`--selftest`）を走らせてください: `python tools/bprime_core.py --selftest`・`python tools/bprime_external.py --selftest`・`python tools/analyze_Bprime.py --selftest`・`python tools/sweep_Bprime.py --selftest`・`python tools/build_report_Bprime.py --selftest`・`python tools/make_frozen_Bprime.py --selftest`・`python tools/send_external_Bprime.py --selftest`・`python tools/freeze_Bprime.py --selftest`・`python tools/bprime_behavior.py --selftest`・`python tools/g4_attempts_Bprime.py --selftest`。
- transformers と tokenizers が要る器: `python tools/close_behavior_Bprime.py --selftest`。
- torch の要る器（`tools/dry_bprime.py`・`tools/dry_bprime_behavior.py`・`tools/dry_run_Bprime.py`・`tools/colab/boot_bprime.py`）は、実行の場に torch が無ければ走らせず、器の中と正式の記録を読んで照らしてください。
- 束の目録 `MANIFEST-recheck-bundle-Bprime.json` の SHA-256 と、あなたが計算した SHA-256 が合うかを、少なくとも変わった器のファイルについて確かめてください。
- 走らせたコマンドと、出力の末尾（最後の数行）と、走らなかったときの誤りの文を、返事にそのまま貼ってください。書き手が手元で同じ出力になるかを照らします。

## しないでほしいこと

- 実の重みを読み込まない・実の重みで順伝播を走らせない（封印の前の決まり）。外への呼び出しをしない（`tools/send_external_Bprime.py` は `--selftest` だけ）。
- ウェブ検索などの道具を使ったときは、その出所を所見と分けて書いてください。

## 返事の形

1. 一行目: 模型の名と作り手。
2. 所見の一覧。所見ごとに: 番号（RC-01 から）・重さ（あなたの見立てと、「重い」なら物差しのどれか）・器とファイルと行・何が起きるか（どんな入力で、どんな誤った出力か止まり方になるか）・直し方の案・確信度（高・中・低）・走らせて確かめたか、読んで推したか。
3. 是認: 採否の表の行のうち、直しが表のとおりだと確かめた行の番号（確かめなかった行は「見ていない」と書いてください）。
4. 走らせた記録: コマンド・出力の末尾・SHA の照らし。
5. 読んでいない所・走らせていない所。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
