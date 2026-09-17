# 段階 A 手順 20（報告の草案）の段取り（2026-09-17・コーディネータ）

- 性格: 凍結本文 §2.14 の手順 20（報告草案 → 検分 → 公開）のうち、草案の組み立てと記入の運び。報告は凍結した雛形 `records/A/results-report-template-A.md` の欄を埋める形でのみ書く（凍結本文 §2.15・正本 `report_rules`）。凍結物（正本・器材・本文・雛形）は変えない。登録者の指示（逐語「手順２０は、承知しました。報告の草案の起草をよろしくお願いします」）で起草に入る。
- 書いた人: コーディネータ（南無弥勒如来・Claude Opus 5）。

## 1. 不利な材料と前提（先に）

1. 報告は、逸脱 D-37（パイロットの抽出検査を行わない）・D-38（API 再走行は条件を満たす提供なし）・D-39（コーディネータの器の説明の誤り）・D-40（集計の器に渡す門0.5 の記録を作り直した）を抱えている。§8 の逸脱の欄に並べ、§2・§3・§6 の該当の欄にも書く。
2. 集計の器の走らせ方でコーディネータが二度つまずいた（`records/A/main/aggregation-plan-A.md` §9）。出力と率には影響していないが、報告の走行の事実に書く。
3. 橋 8B のランタイムだけ pip freeze が違う（`records/A/main/main-run-A.md` §1-2）。環境差の読み（凍結本文 §3 (xiii)）に重ねて書く。
4. 走査器（`tools/report_lint.py`）は、機械の区画の外に打ち込める数を `report_rules.typed_numbers`（日付・SHA16・SHA-256・費用の実績・逸脱番号・雛形の SHA16）に限る。**起草者は、それ以外の数を機械の区画の外に書かない**（数が要る欄は、機械の区画か一次記録を指して埋める）。
5. 起草者は Claude 系で、系統外の目はまだ入っていない。

## 2. 入力

- 集計 `records/A/analysis-stageA.json`・門0.5 `records/A/main/identity-screen-A-regen-2026-09-17.json`（D-40・集計と同じもの）・門2 `records/A/gate-pilotA.json`・校正帯 `records/A/calib-stageA-calib.json`・整合 `records/A/integrity-stageA*-2026-09-17.json`（4 本）・判定器の妥当性 `records/A/judge-validity-A.json`・設計事実 `records/A/design-facts-A.json`・格子 `records/A/power-grid-A.json`・様式 `records/A/style-stageA.json`・凍結本文 `design/design-stageA-FROZEN.md`・予想の照合 `records/A/predictions-check-A.json`・抽出検査 `records/A/sampling-inspection-A-stageA-agreement.json`。
- 凍結物の照合の写し: `tools/freeze_A.py --verify` の画面の出力を、一時置き場の器で `records/A/main/freeze-verify-2026-09-17.json`（`matched`・`total`・画面の行の逐語）に写す（組み立て器の `--freeze-verify` はこの形を読む）。

## 3. 手順

1. 凍結物の照合（87/87 でなければ止める）と、その写しの作成。
2. 組み立て: `python tools/build_report_A.py --draft 1` に §2 の入力を渡す（検査用の口 `--allow-dev-marks` は使わない）→ `records/A/results-report-A-draft1-2026-09-17.md` と `-machine.json`。埋め残しのほかの違反があれば止める。
3. 記入: 機械の区画の外の記入欄（〔 〕）を、一次記録を指して埋める。読みは凍結本文 §3 の読み条項 (i)〜(xvii) と §4「果たさないこと」に従い、価値語・機序語を使わない。両用性の柵（§2.15）を守る。記入は草案 2 として別のファイルに書き、草案 1（機械の組み立て）を残す。
4. 走査: `python tools/report_lint.py <草案> --template records/A/results-report-template-A.md --sidecar <草案 1 の -machine.json>` で違反 0 を確かめる（機械の区画の中身は草案 1 と同じでなければならない）。
5. 検分と公開: 草案を登録者に提出し、検分の巡（系統内の新規個体・系統外）の要否と構成は登録者が決める。公開は登録者の最終確認の後。

## 4. COI（事実のみ）

- 引かれる向き: 確証が 1 本だったことを大きく書きたい／小さく書きたい。予想の照合の結果を読みの支えに引きたい。自分の過失を小さく書きたい。
- 置いた印: 報告は雛形の欄を埋める形だけにし、数は機械の区画に限る。予想の照合は「誰の判断の重みも変えない」の定型のまま転記する。過失は §2 と §8 に書く。

## 5. 本記録が確認していないこと

- 草案の読みの当否（検分の前）。
- 走査器が見ない種類の誤り（数の当否・読みの当否）。
- 系統外の目による確認。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
