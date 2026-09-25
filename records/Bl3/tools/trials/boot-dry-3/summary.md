# 起動器の DRY の走り（機械生成・`records/Bl3/tools/trials/run_boot_dry.py`・2026-09-25 04:05 UTC）

- 起動器 `tools/colab/boot_Bl3.py` SHA16 458C5D3076E8923D・走らせる器 `tools/bl3_run.py` SHA16 1C9C201D1A8FA4DC・集計の器 `tools/analyze_Bl3.py` SHA16 0F75477F38C008FE・掃き出しの器 F87CDBA37B3D3BE2・報告の器 C1B8E9160CE39B37・正本 D41CFA474EA0190E。
- 小さな本数: 等方 9・乙の文脈 2・独立の再計算の v̂ の行 2（DRY の環境変数）。
- 相 check: 順伝播 0 回・比べる相手の除き方の錨 あり・‖static‖ と転記行 D 同じ・書き換えの器を import できた True。
- 相 main の組: main・recompute・secondary・本の計算の近道 False。
- 一致だけを見る段: 一段目 True・二段目（札） True・二段目の値 許容の内・全体 True（値は開いていない）。
- 結果を開く段 → 掃き出し（欠け 0）→ 報告の組み立て（291 行）→ 走査（違反 0）。

| 段 | 終わりの値 |
|---|---|
| `tools/colab/boot_Bl3.py`（OP4B_PHASE=check） | 0 |
| `tools/colab/boot_Bl3.py`（OP4B_PHASE=pilot） | 0 |
| `tools/colab/boot_Bl3.py`（OP4B_PHASE=main・OP4B_DRY_PILOT=〈一時の置き場〉\pilot-20260925T035609Z\pilot.json） | 0 |
| `tools/analyze_Bl3.py judge 〈一時の置き場〉\main-20260925T035950Z --pilot 〈一時の置き場〉\pilot-20260925T035609Z\pilot.json --out 〈一時の置き場〉\judge.json` | 0 |
| `tools/analyze_Bl3.py open 〈一時の置き場〉\main-20260925T035950Z --pilot 〈一時の置き場〉\pilot-20260925T035609Z\pilot.json --judge-record 〈一時の置き場〉\judge.json --out 〈一時の置き場〉\analysis.json` | 0 |
| `tools/sweep_Bl3.py 〈一時の置き場〉\analysis.json` | 0 |

- この置き場の写し（進みの印字・session・一致だけを見る段の記録・このまとめ）では、手元の置き場の道筋 15 か所を〈一時の置き場〉・〈リポジトリ〉に置き換えた（`records/Bl3/tools/trials/sanitize_paths.py`・値は変えていない）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
