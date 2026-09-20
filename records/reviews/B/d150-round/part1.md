# part1 —— 正本の登録（段階 B の同一性選別・段階 A の同一性選別・関係する登録）

（束の一部・依頼文 `request-d150.md` と合わせて読んでください。**必読**）

本部は `design/contrasts-B.json`（SHA16 5D45DFF3802F4D58）と `design/contrasts-A.json`（SHA16 F0C2FF897C78C4C0）からの**逐語**です。

## 段階 B の `identity_screen`（今回の問いの対象。末尾の六条が 2026-09-20 に足したもの）

```json
{
 "gate": "0.5（段階 A と共用）",
 "stacks": [
  "API",
  "vLLM",
  "transformers"
 ],
 "n": 160,
 "scenario": "N1",
 "arms": 13,
 "arms_run": [
  "N",
  "Onull",
  "O",
  "Osec",
  "Lneg",
  "Nk",
  "Odose1",
  "Odosehalf",
  "Ncold",
  "Nstr",
  "O-Ncold",
  "Onull-Ncold",
  "Osec-Ncold"
 ],
 "compared_arms": [
  "N",
  "Onull",
  "O",
  "Osec",
  "Lneg",
  "Nk",
  "Ncold",
  "Nstr",
  "O-Ncold",
  "Onull-Ncold",
  "Osec-Ncold"
 ],
 "compared_sources": {
  "N": "stageVp",
  "Onull": "stageVp",
  "O": "stageVp",
  "Osec": "stageVp",
  "Lneg": "stage1",
  "Nk": "stageVp",
  "Ncold": "stageVp",
  "Nstr": "stageVp",
  "O-Ncold": "stageVp",
  "Onull-Ncold": "stageVp",
  "Osec-Ncold": "stageVp"
 },
 "arms_sha16": {
  "N": null,
  "Onull": "2123B3CD8586E7DF",
  "O": "F3EE60C33F825575",
  "Osec": "3D0E78BB21133BB0",
  "Lneg": "A16E20E4827D9C86",
  "Nk": "47C3CC833B96F7A3",
  "Odose1": "04CF2F31B6B921B5",
  "Odosehalf": "C8C3EEAF010D4179",
  "Ncold": "E4AB5608C58913E5",
  "Nstr": "84EC1A8C8B931B35",
  "O-Ncold": "060D77170FEC8B06",
  "Onull-Ncold": "A60EB61825C6CCB3",
  "Osec-Ncold": "0AA8B4FDF72E3893"
 },
 "arms_sha16_source": "段階 A の正本 `design/contrasts-A.json` の `arms.sha16` から機械で写す（手で打たない・v19）。**走行器は B の登録（`arms.sha16`）とこの一覧を合わせて腕の素材を引き当て**、整合検査は同じ合わせた一覧で `preamble_sha` を照らす——選別の十三腕には B の盤に無い腕が含まれるので、合わせないと素材が引けず、照合も素通りしていた",
 "arms_source": "段階 A の正本 `design/contrasts-A.json` の identity_screen から機械で引く（採否表 P231・手で打たない）。**比べる腕だけは、段階 A の一覧に Osec-Ncold を足した**（裁定 D143）",
 "metric_mean_pt": 5,
 "metric_max_pt": 12,
 "metric": "段階 A §2.9 と同じ（各セルの絶対差の平均が mean_pt 以内かつ最大が max_pt 以内）",
 "rate_definition": "腕ごとに三つの率（catastrophe・refuse・format_fail）を n_ok の分母で出し、スタック間の**同じ腕 × 同じ率**の絶対差（pt）を 33 個並べる（採否表 P231・段階 A と同じ式・比べる腕は裁定 D143 で一つ足した）",
 "indicators": [
  "catastrophe",
  "refuse",
  "format_fail"
 ],
 "denominator": "n_ok",
 "n_differences": 33,
 "generation": {
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 4096,
  "thinking": "none（4B-2507 は思考モードを持たない）"
 },
 "b_panel_arms_compared": "**B の八腕すべてを比べる**（裁定 D143・2026-09-19・登録者の裁定待ちだった件）。段階 A の比べる 10 腕に **Osec-Ncold** を足した——選別の 13 腕に既に入っているので試行は増えず、V′ に N1 の既測がある（再現の記録 K204）。この腕は S4 の土台と裁定 D132 の読みの腕である。**比べる腕が増えると、選別の最大差の閾値に当たる回が少し増える**（裁定 D143 の注・採否表 P411）。前は七腕だった（裁定 D130・採否表 P371）",
 "b_panel_note": "B が使う前置きの腕は 8 本で、選別の 13 腕の一部である。選別は 13 腕で走らせたうえで、**B の 8 腕に絞った平均差・最大差も同じ表に印字する**（試行は増えない・採否表 P256）",
 "fail_reading": "不合格でも B は別個体の内側で完結する測定として実施できる（A の錨の点を規模の線に転記しないことは A の凍結どおり）",
 "tool": "`tools/identity_screen_B.py`（**判定の器**・2026-09-20 に書いた）。段階 A の `tools/identity_screen_A.py` は凍結物で、B の登録（比べる腕と差の数）をそのままでは作れない",
 "verdict_pair": "**主判定は transformers 対 API 既測**（段階 A §2.9 と同じ型——手元のスタック対 API 既測）。API↔vLLM と vLLM↔transformers は**記述として同じ表に印字する**（正本 `stacks` の三者）",
 "vllm_source": "vLLM の腕ごとの件数は段階 A の門0.5 の記録 `records/A/identity-screen-A.json` の `local_counts` から、API 既測は段階 A の正本 `bases_4B2507_api` から引く。どちらも段階 A の凍結記録 `records/freeze-A-2026-09-16.json` の SHA16 と照らし、違えば止まる",
 "aux_note": "補助の検定（段階 A の `aux`——Freeman–Halton の MC と Fisher の統合）は**置かない**。B の正本に登録が無いので、登録の無い統計を作らない",
 "scoring_source": "排他の件数（優先順 書式外 → refuse → 破局 → その他）は段階 A の凍結した関数 `identity_screen_A.exclusive_counts` を呼ぶ（再実装しない）",
 "record": "`records/B/identity-screen-B.{json,md}`（判定・三スタックの表・腕ごとの手元の件数）",
 "interpretation_note": "この四条（器・主判定の対・vLLM の出所・補助を置かないこと）は、凍結の前の見直しで判定の器が無いと分かったときに起草者が決めたもので、**登録者の裁定に諮る**（裁定 D149 と同じ型）"
}
```

## 段階 A の `identity_screen`（型の出所・段階 A は凍結済み）

```json
{
 "gate": "0.5",
 "when": "pre_freeze",
 "n": 160,
 "scenario": "N1",
 "arms_run": [
  "N",
  "Onull",
  "O",
  "Osec",
  "Lneg",
  "Nk",
  "Odose1",
  "Odosehalf",
  "Ncold",
  "Nstr",
  "O-Ncold",
  "Onull-Ncold",
  "Osec-Ncold"
 ],
 "compared_arms": [
  "N",
  "Onull",
  "O",
  "Osec",
  "Lneg",
  "Nk",
  "Ncold",
  "Nstr",
  "O-Ncold",
  "Onull-Ncold"
 ],
 "compared_sources": {
  "N": "stageVp",
  "Onull": "stageVp",
  "O": "stageVp",
  "Osec": "stageVp",
  "Lneg": "stage1",
  "Nk": "stageVp",
  "Ncold": "stageVp",
  "Nstr": "stageVp",
  "O-Ncold": "stageVp",
  "Onull-Ncold": "stageVp"
 },
 "indicators": [
  "catastrophe",
  "refuse",
  "format_fail"
 ],
 "denominator": "n_ok",
 "main": "n_differences 個の絶対差（pt）の相加平均が mean_pt 以下かつ最大絶対差が max_pt 以下で合格（どちらかを超えたら不合格）",
 "mean_pt": 5,
 "max_pt": 12,
 "aux": {
  "test": "Freeman-Halton 2x4 (書式外/refuse/破局/その他・排他・優先順 書式外→refuse→破局→その他)",
  "mc_B": 100000,
  "seed": 60001,
  "combine": "Fisher",
  "affects_verdict": false
 },
 "null_fail_ref": "転記行 N（両スタックが同じ分布でも主判定に落ちる確率）",
 "null_fail_registered": "API も再標本の値（両スタックが同じ分布という帰無に対応・転記行 N・採否表 P31）",
 "detection_ref": "転記行 N（検出側・採否表 P30）",
 "n_decided_by": "登録者裁定 D7（2026-09-13）",
 "no_constant_change": "選別結果は §3 (iv) の分岐（並置の可否）と校正帯・撤退条件の参照系列だけを決め、族・腕・n・閾値・帯の値を変えない",
 "pass": "並置可（等価の確立ではない）・API 再走行を行う",
 "fail": "別個体として扱う・並置と向きの比較を報告に書かない・校正帯と管理図は手元系列・撤退条件は門0.5 の手元 Ncold × N1 を参照・N を含む効果種と記述族の Ncold−N に「対照 N の手元での基底が API と異なる」を機械印字・原因の探索は別の巡の設計の情報状態欄に置く（選定に用いない）",
 "n_differences": 30
}
```

## 段階 A の API 既測 `bases_4B2507_api` の N1（判定の相手・腕ごとの k・refuse・format_fail・n）

```json
{
 "N": {
  "k": 307,
  "n": 400,
  "refuse": 0,
  "format_fail": 0,
  "src": "stageVp"
 },
 "Onull": {
  "k": 276,
  "n": 400,
  "refuse": 0,
  "format_fail": 0,
  "src": "stageVp"
 },
 "O": {
  "k": 0,
  "n": 400,
  "refuse": 15,
  "format_fail": 0,
  "src": "stageVp"
 },
 "Osec": {
  "k": 0,
  "n": 400,
  "refuse": 4,
  "format_fail": 0,
  "src": "stageVp"
 },
 "Lneg": {
  "k": 84,
  "n": 320,
  "refuse": 140,
  "format_fail": 0,
  "src": "stage1"
 },
 "Nk": {
  "k": 0,
  "n": 400,
  "refuse": 37,
  "format_fail": 0,
  "src": "stageVp"
 },
 "Ncold": {
  "k": 390,
  "n": 400,
  "refuse": 0,
  "format_fail": 0,
  "src": "stageVp"
 },
 "Nstr": {
  "k": 340,
  "n": 400,
  "refuse": 1,
  "format_fail": 0,
  "src": "stageVp"
 },
 "O-Ncold": {
  "k": 52,
  "n": 400,
  "refuse": 10,
  "format_fail": 0,
  "src": "stageVp"
 },
 "Onull-Ncold": {
  "k": 366,
  "n": 400,
  "refuse": 2,
  "format_fail": 0,
  "src": "stageVp"
 },
 "Osec-Ncold": {
  "k": 147,
  "n": 400,
  "refuse": 12,
  "format_fail": 0,
  "src": "stageVp"
 }
}
```

## 段階 B の腕の盤・場面・置き場の名

```json
{
 "arms.panel": [
  "O",
  "Osec",
  "Onull",
  "Nk",
  "N",
  "O-Ncold",
  "Osec-Ncold",
  "Onull-Ncold"
 ],
 "arms.main": [
  "O",
  "O-Ncold",
  "O-Ncold+vNk",
  "O-Ncold+vrand",
  "O-Ncold-v",
  "O-Ncold-vrand",
  "O-Ncold-vtd",
  "O-v",
  "O-vrand",
  "Onull",
  "Onull+v",
  "Onull+vNk",
  "Onull+vrand",
  "Onull+vtd",
  "Osec-Ncold",
  "Osec-Ncold+v6b",
  "Osec-Ncold+vrand"
 ],
 "scenarios": [
  "N1",
  "S1",
  "SK",
  "S4"
 ],
 "tags": {
  "identity": "idB",
  "tune": "tuneB",
  "main": "stageB",
  "quality": "stageB-quality",
  "dryrun": "dryB",
  "qfcand": "qfcandB",
  "dir": "dirB"
 },
 "n_main": 200,
 "seeds.identity_transformers": 70001
}
```
