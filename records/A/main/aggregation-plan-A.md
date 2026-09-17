# 段階 A 手順 19（集計）の段取り（走らせる前・率を見る前・2026-09-17・コーディネータ）

- 性格: 凍結本文 `design/design-stageA-FROZEN.md` §2.14 の手順 19（集計・測れた効果種の計算を含む）を走らせる前に、器の順番・入力・出力・止める規則・率を初めて見る時点を書いた記録。**本記録をコミットし、登録者の確認を受けてから走らせる。** 凍結物（正本・器材・本文）は変えない。判定は凍結した器の出力の転記で、器を走らせた後に規則を動かさない。
- 書いた人: コーディネータ（南無弥勒如来・Claude Opus 5）。
- 前提（済んだ段）: 手順 14〜16 の走行と回収（`records/A/main/main-run-A.md`・問題 0）、手順 17 の整合検査（全走行 整合）と抽出検査（`records/A/sampling-inspection-A-stageA*.md`）、手順 18 は「条件を満たす提供なし」（`records/A/main/api-rerun-run-A.md`・逸脱 D-38）。予想は凍結の直後に封印済み（登録者の第 2 版＝拘束版と、コーディネータの封印・`records/FREEZE-RECORD.md`）。
- 走らせる前の確認: `python tools/freeze_A.py --verify records/freeze-A-2026-09-16.json` → **87/87 一致**（2026-09-17・本記録の起草の前）。走らせる直前にもう一度確かめる。

## 1. 不利な材料と未決（先に）

1. **コーディネータは、集計の器の振る舞いを誤って説明していた（訂正）。** API 再走行の記録（`records/A/main/api-rerun-run-A.md` §1-6・§5）と逸脱 D-38 と、登録者への相談で、「凍結した集計の器は、門0.5 が合格で API 再走行の記録が無いと止まる」と書いた。**器の行を読み直すと誤りだった**: 足りない記録で止める判定は `tools/analyze_A.py` の 233 行にあり、API 再走行の欠けを足りない記録に加えるのは、その後の 356 行である。器は上から順に動くので、**API 再走行の欠けでは止まらず**、出力の `missing` に「API 再走行（tag stageA-api）」が書かれ、スタック差の欄が「門0.5 合格・API 再走行の記録なし」になるだけである。報告の走査器（`tools/report_lint.py` 27・100〜102 行）が違反に数えるのは「集計の検査用の印」の欄だけで、「足りない記録」の欄は対象外である。**したがって、検査用の口（`--allow-incomplete`・`--allow-dev-marks`）は要らない。** 登録者は、誤った説明の上で「検査用の口で走らせる」案（甲）を承認していたので、**本段取りは口を使わない形に改め、あらためて登録者の確認を受ける。** 誤りの訂正は逸脱 D-39 として記帳し、API 再走行の記録と D-38 に訂正を書き足す。
   - 機械の歯止め（§3-5）: 走らせた後に、出力の `missing` が **「API 再走行（tag stageA-api）」の一つだけ**で、`dev_marks` が**空**であることを確かめる。違えば、その出力を使わずに止めて諮る。
2. **スタック差（手元と API）の記述は無い**（D-38）。報告の雛形の「スタック差」の欄は、器の出力（「門0.5 合格・API 再走行の記録なし」）と D-38 を並べて書く。
3. **橋 8B のランタイムだけ pip freeze が違う**（`records/A/main/main-run-A.md` §1-2）。環境の副次解析（橋の行を使う）では、環境・同時要求数・時点・pip freeze の差が重なる。副次解析の読みでは分離したと書かない。
4. **パイロットの抽出検査は行っていない**（D-37）。
5. コーディネータは、ここまで率を見ていない（見たのは件数・終了コード・先取り・校正腕の判定と k・書式外の件数・抽出検査の標本の先頭）。**§3 の器を走らせた時点で初めて率を見る。** 一度見たら、段取りの規則・閾値・読み条項は動かさない。

## 2. 入力（凍結物と記録）

| 種類 | ファイル | 備考 |
|---|---|---|
| 正本 | `design/contrasts-A.json` | 凍結マニフェストで照合 |
| 凍結本文 | `design/design-stageA-FROZEN.md` | 同上 |
| 凍結マニフェスト | `records/freeze-A-2026-09-16.json` | 87 ファイル |
| 門（パイロット・手順 13） | `records/A/gate-pilotA.json` | 門2 縮小なし・撤退条件 合格 |
| 門0.5 | `records/A/identity-screen-A.json` | 合格 |
| 設計事実 | `records/A/design-facts-A.json` | 到達の見込み |
| 格子 | `records/A/power-grid-A.json` | 報告の組み立てに使う |
| 判定器の妥当性 | `records/A/judge-validity-A.json` | 報告の組み立てに使う |
| 整合検査 | `records/A/integrity-stageA*-2026-09-17.json`（4 本） | 手順 17 |
| 抽出検査 | `records/A/sampling-inspection-A-stageA-seal.json` ほか | 手順 17 |
| 封印予想 | `records/predictions/predictions-registrant-A-2026-09-16-v2.json`（拘束版）・`records/predictions/predictions-coordinator-A-2026-09-16.json` | 第 1 版は非拘束の記録なので照合に入れない |
| 走行 | `results/stageA/`・`results/stageA-anchor2/`・`results/stageA-bridge/`・`results/stageA-calib/`・`results/sessions-A/` | `results/excluded-stageA-api-thinking-2026-09-17/` は読まない |

## 3. 手順（この順で一度ずつ走らせる・出力は既存を上書きしない）

1. `python tools/freeze_A.py --verify records/freeze-A-2026-09-16.json`（87/87 でなければ止める）。
2. **応答様式**: `python tools/response_mode_A.py --tag stageA` → `records/A/style-stageA.json`。様式門の入力・`<think>` の残骸（段取り §10 (e) の判定）・層ごとの試行数と破局数（**ここで初めて率に触れる**）。
3. **校正帯**: `python tools/calib_band_A.py --identity records/A/identity-screen-A.json` → `records/A/calib-stageA-calib.{json,md}`。合格枝・9 セッションの判定（起動器の判定と一致するかを確かめる）。
4. **管理図**: `python tools/control_chart_A.py --calib records/A/calib-stageA-calib.json --identity records/A/identity-screen-A.json` → `records/control-chart.md` に段階 A の行を足す（記述）。
5. **集計**: `python tools/analyze_A.py --tag stageA --gate records/A/gate-pilotA.json --identity records/A/identity-screen-A.json --calib records/A/calib-stageA-calib.json --style records/A/style-stageA.json` → `records/A/analysis-stageA.{json,md}`（検査用の口は使わない）。**走らせた直後に、出力の `missing` と `dev_marks` を機械で確かめる**（§1-1 の歯止め）。
6. **予想の照合**: `python tools/compare_predictions_A.py --pred records/predictions/predictions-registrant-A-2026-09-16-v2.json --pred records/predictions/predictions-coordinator-A-2026-09-16.json --analysis records/A/analysis-stageA.json` → `records/A/predictions-check-A.{md,json}`（記録であって評価ではない）。
7. 手順 20 の報告の組み立て（`tools/build_report_A.py`・`tools/report_lint.py`・検査用の口は使わない）は、本段の出力を登録者に報告した後に、別の段取りで行う。

## 4. 止める規則

1. どの器が非零で終わっても、次の器に進まずに止め、出力と画面の行を記録して登録者に諮る（器を直さない・規則を動かさない）。
2. 凍結マニフェストの照合が 87/87 でなければ止める。
3. 集計の `missing` が「API 再走行（tag stageA-api）」の一つだけでない、または `dev_marks` が空でなければ、その出力を使わずに止める。
4. 校正帯の器の判定が、起動器の判定（9 本すべて合格）と食い違えば止める。
5. 集計の器が「札の全組合せ表に無い行」で止まったら、そのまま記録して諮る。

## 5. 読みの縛り（率を見る前に書く）

- 判定は凍結本文 §3 の読み条項と正本 `report_rules` に従い、器の札を写すだけにする。**器を走らせた後に、読み条項に無い読みを足さない。**
- 予想の照合は「的中は独立の確認ではなく、誰の判断の重みも変えない」（正本 `predictions`）。封印予想を事後の読みの根拠に引かない。
- 率を見た後の COI（希望方向への読み）を、報告の起草の前に書く。
- 報告の起草では、両用性の柵（凍結本文 §2.15）を守る。

## 6. COI（事実のみ）

- 引かれる向き: 早く率を見たい。自分の予想（封印済み）が当たっていてほしい。API 再走行の欠けを小さく見せたい。器の説明の誤り（§1-1）を小さく書きたい。
- 置いた印: 走らせる前に本段取りをコミットし、登録者の確認を受ける。誤りを逸脱 D-39 として記帳し、既に公開した記録にも訂正を書き足す。走らせた後の機械の歯止めを置く。予想の照合は器に任せる。

## 7. 本記録が確認していないこと

- 集計の結果（まだ走らせていない）。
- API 再走行の欠けが集計の中身へ影響しないこと: 器の行では、欠けはスタック差の記述の欄を「記録なし」にして `missing` に一項を足すだけで（348〜361 行）、確証の判定の経路には入らない（コーディネータが器の行で確かめた・§1-1 の読み違いの後に読み直した）。**走らせた後の出力でも確かめる。**
- 報告の組み立て器と走査器が、`missing` に一項のある集計の出力で最後まで通るか（手順 20 で確かめる・走査器の行の上では「足りない記録」は違反に数えない）。
- 系統外の目（本段取りは Claude 系のコーディネータだけで書いた）。

## 検分票

- 対象: 手順 19 の段取り（走らせる前）。
- 段階: 事前登録あり（本記録を集計の前にコミットする）。
- 凍結物の同定: 凍結マニフェスト `records/freeze-A-2026-09-16.json`（87/87 一致・2026-09-17）・正本・凍結本文・器材。
- 盲検の状態: 率盲検の内側（本記録の起草の時点で率を見ていない）。
- 敵対的検分: 検査用の口を使う案を書いた後に、その口が他の欠けを隠す危険を検討する中で器の行を読み直し、**「API 再走行の欠けで器が止まる」という自分の前提が誤りだったことを見つけた**（§1-1）。口を使わない形に改め、走らせた後の機械の歯止め（missing と dev_marks）を置いた。第 1 版の予想を照合に入れない理由（非拘束）を書いた。API の除外の置き場を器が読まないことを確かめた（`records/A/main/api-rerun-run-A.md` §4）。
- 系統の内訳: Claude 系（コーディネータ）のみ。
- COI 記録: §6。
- 判定: 登録者の確認待ち。
- 本検分が確認していないこと: §7。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
