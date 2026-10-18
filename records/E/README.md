# 段階 E の記録

段階 E（論文の組み立てと公開）の記録の置き場です。論文の日本語の正本は `paper/ja/`、走らせ直しのスクリプトは `tools/rerun/` にあります。

- 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

## 1. 前に公開した刻印と一覧の SHA（2026-10-14）

- [`stamp-frame-E1.md`](stamp-frame-E1.md): 段階 E の枠（草案6）の刻印。
- [`stamp-frame-E-addendum1.md`](stamp-frame-E-addendum1.md)・[`stamp-frame-E-addendum2.md`](stamp-frame-E-addendum2.md): 枠の追記一・追記二の刻印。
- [`preopen-sha256-E2.txt`](preopen-sha256-E2.txt): 伏せた記録を開ける前に書いた一覧と部品の SHA-256。
- [`reading-judgments-sha256-E2.txt`](reading-judgments-sha256-E2.txt): 開けた後の探索の、読みの決めの記録の SHA-256。

## 2. 刻んだバイトのまま公開する物（刻印の約束・論文の公開とともに）

枠の本文と追記は、この置き場に置きました。刻印の表で「刻んだバイトのまま公開する」とした部品と、公開の形を論文の公開の前に決めるとした物は、[`stamped/`](stamped/) の下に、内部の置き場の道のまま置きました。どれも、置く前に、刻印か SHA の記録の SHA-256 と同じことを照らしました。刻んだバイトのままなので、役の名（法名）が残る物があります。

| 置いた道 | 照らした先 | SHA-256 |
|---|---|---|
| `stamped/D1p/d1p_confirm.py` | `records/E/stamp-frame-E1.md` | 3E92994DF6ADBE0F4E88B804E6A48059F9FAF442194E9DCA94AAA0425AACB16A |
| `stamped/D1pE/d1pe_confirm.py` | `records/E/stamp-frame-E1.md` | F4094799DBEE9DCA00179F6F7DAC62A6C16E2274E74C2F0A0168EAD14636827A |
| `stamped/E/E2/e2_tool.py` | `records/E/preopen-sha256-E2.txt` | C34096928D9A6DD540AC36ACE9C14D7A204B0BC8B670D03F4091F62AF010D3B4 |
| `stamped/E/E2/preopen-common-E2.json` | `records/E/preopen-sha256-E2.txt` | 3F176530358FC00FCBB05D86D2AF856BF23083B2786BC0ADB6C3918AA3EA8B64 |
| `stamped/E/E2/preopen-common-E2.md` | `records/E/preopen-sha256-E2.txt` | 3D5C974DE0EC64B1C57529663CC547C798A71BFAA1FB5791FB2A97FA48C42E1A |
| `stamped/E/E2/preopen-en-E2.json` | `records/E/preopen-sha256-E2.txt` | F9DC7936962F2A1B2694F00FBF495413787B04E173799CA1829D950C7BCF1A5E |
| `stamped/E/E2/preopen-en-E2.md` | `records/E/preopen-sha256-E2.txt` | 79A2B63D004BC0D01F19BE65DC52DB3489196C076EBB884BF1F00C3F665A89CE |
| `stamped/E/E2/preopen-ja-E2.json` | `records/E/preopen-sha256-E2.txt` | 78362340B2F83B3B1B79BB1B3549660523F0D02CEA4CADE660166A3AD54A1ADF |
| `stamped/E/E2/preopen-ja-E2.md` | `records/E/preopen-sha256-E2.txt` | 70B668E22652501B38D87CC00BAD8158945A16919A61E768B6D8F09D98C31342 |
| `stamped/E/E2/synthetic-test-E2.md` | `records/E/preopen-sha256-E2.txt` | 1966C353422AA7D9B86FA6EBB4B56F6C5A2870409F54D54236AE2D03FC9481D4 |
| `stamped/E/addendum1/bans-E3.json` | `records/E/stamp-frame-E-addendum1.md` | DAE4C628655C8BD1271269725B2598E0D3EB8B40363D198965508394E51DDACD |
| `stamped/E/addendum1/bans-E3.md` | `records/E/stamp-frame-E-addendum1.md` | AFADABDE51F555FED0617863A2D23B83D223EE881DDF25A341D02A41A9ACC3CF |
| `stamped/E/addendum1/collect_bans_E3.py` | `records/E/stamp-frame-E-addendum1.md` | F3C3D7863C84AF26593A9E63C5C2CCD346DB74ED53D1B63BEC18DCAB28D1A16A |
| `stamped/E/addendum1/scan_bans_E3.py` | `records/E/stamp-frame-E-addendum1.md` | 36327C37194688FD803EC8DF7A045FA7C37B31BEB0C92610BAF5682997C321B0 |
| `stamped/E/addendum1/synthetic-test-scan-bans-E3.md` | `records/E/stamp-frame-E-addendum1.md` | A9759C875DE7901DA97C655B2C46B928890B93DC26DC88813B1FE35F6472C4CA |
| `stamped/E/appendix_a_lists_E1.py` | `records/E/stamp-frame-E1.md` | 381427FB9049EF77004A4597BC917AC7E8AFAB4149699BA3BC42C3799B9ED07D |
| `stamped/E/copyback-lists-E1.json` | `records/E/stamp-frame-E1.md` | E5F63105AA83308E83E26A0117E243B91220BBA8238A5708BF1E559C4C6F87DE |
| `stamped/E/copyback-lists-E1.md` | `records/E/stamp-frame-E1.md` | 7B39AAF5839CFFA7A9B33F5E26DA7A921BD399F2B1F8FA4C9C1FAA854033B488 |
| `stamped/E/predictions-E1-2026-10-13.md` | `records/E/stamp-frame-E1.md` | F3CB5B9F017B2FDF3D43730020E39254BC75F87F00EC705BBE4F1A60D5745EE2 |
| `stamped/explore/naming-survey-O-2026-10-13/note-fold-dakuten-2026-10-14.md` | `records/E/stamp-frame-E1.md` | 4B7E109A25BE9C1FBC16DABC19BDC9E62CF0D01889E6CE0408C5B3B3E62CE5BA |
| `stamped/explore/naming-survey-O-2026-10-13/tools-used/scan_public_names_ext.py` | `records/E/stamp-frame-E1.md` | 15B25982F0B3EE372A9B56F4D626D2FBD53ED128C1732C32E6E1032D4DB52EF1 |
| `stamped/explore/naming-survey-O-2026-10-13/tools-used/scan_public_naming.py` | `records/E/stamp-frame-E1.md` | 13CD6C24CEC0F84A171E0DFE141EBAFE06C4675CC6F67A032517A52A2E0EF359 |
| `stamped/explore/naming-survey-O-2026-10-13/tools-used/scan_public_naming_v2.py` | `records/E/stamp-frame-E1.md` | CA4FFEBC8B98F308D1A059A1965DC6D188ED33EB2AE93AA4F1087C3E9FF7D146 |

- 禁止の語の一覧（`stamped/E/addendum1/bans-E3.json`・`bans-E3.md`）は、公開の置き場の記録の逐語として、作り手の語の照らしに当たる語（前の段の機構の段の機種の名と、計算に使った GPU の名）を含みます。この二つの置き場でだけ許しました。
- 集計のスクリプト（`stamped/D1p/d1p_confirm.py`・`stamped/D1pE/d1pe_confirm.py`）は、二つの登録の集計の報告を組んだスクリプトです。内部の置き場の道を指す作りで、そのままでは動きません。

## 3. 論文の公開とともに置いた記録

| 置いた道 | 公開の形 | SHA-256 | 照らせる先 |
|---|---|---|---|
| `records/E/00-frame-E-draft6.md` | 刻んだバイトのまま | AB7491FF30074FBD43498F10C61BEBFA288D69D78719F19F2899EB55DDFD64CC | `records/E/stamp-frame-E1.md` |
| `records/E/00-frame-E-addendum1-2026-10-14.md` | 刻んだバイトのまま | 352BD92D21B3D14D0B670F3483FEF9F160AFF7F28DD0A796A5692B5FA14D5C35 | `records/E/stamp-frame-E-addendum1.md` |
| `records/E/00-frame-E-addendum2-2026-10-14.md` | 刻んだバイトのまま | 2A870ED3141A92CC9C67E22D21B17ABF0DF6290FF43DE9FB1AEC0E46D188790F | `records/E/stamp-frame-E-addendum2.md` |
| `records/E/decisions-E6.md` | 組んだ文書（名を伏せた） | 7B2EC32518635A80F002383AD37DBBF2BB5AB4B5175927587A4E7239E41D63B3 | — |
| `records/E/catalog-E6.md` | 組んだ文書 | 1E104F672313C01EDD347D641F37316484C31AE540C277D38BAA1F1AE4978978 | — |
| `records/E/mask-record-E6.md` | 組んだ文書 | 1C6E0D9C496FAB9BC45F8F186E0C7F28DF17BB370DBDACBE5EE82813529A4C56 | — |
| `records/D1p/predictions-D1p.md` | 元のバイトのまま | B64FDF01AD4055F7419E0B7710C83304AFDEF0051883CEEBBE40904A9B3E15DD | `records/D1p/prerun-seal-D1p.md`（実行の前の SHA の記録） |
| `records/D1p/predictions-check-D1p.md` | 元のバイトのまま | BDD536C5FC976EDDF77F8CDA42AD39EC9E55035A20F937BBFFE83F3C28D09D7D | `records/D1p/results-D1p-FINAL-2026-10-11.md`（最終版の SHA の表） |
| `records/masked/D0/00-frame-D0w2-masked-2026-10-03.md` | 名を伏せた写し | 857DD5573AF8F2BCDDA64959607EF3F5769502C46CC7683521EEE38E4CEB2C4D | `records/E/mask-record-E6.md`（元の SHA-256） |
| `records/masked/D0/d0_config-masked.py` | 名を伏せた写し | DE093FB481204FBDEF380DE1B57CB6D3D985146113365DEAADA683837A3EBC28 | `records/E/mask-record-E6.md`（元の SHA-256） |
| `records/masked/D0/frame-stamp-D0w2-masked.md` | 名を伏せた写し | 9F65D48804DFDC55853A98A139DEAD36C3701A8DDD80823DABDF0D205595EFB1 | `records/E/mask-record-E6.md`（元の SHA-256） |
| `records/masked/D1p/moved-records-paths-D1p-masked.json` | 名を伏せた写し | FFD8831AAB37B198FE3E0516260CF54C2ADC250B2C42A8BB5A4B53AD88EC5449 | `records/E/mask-record-E6.md`（元の SHA-256） |
| `records/plans/plan-framing-sensitivity-scale-and-mechanism-v1.0-2026-09-07.md` | 名を伏せた写し | D43DFB8F92916C8775AF3395FABC264F183B4329796E1F569A935EF069444A4A | `records/E/mask-record-E6.md`（元の SHA-256） |
| `records/plans/plan-framing-sensitivity-scale-and-mechanism-v3.0-2026-10-13.md` | 名を伏せた写し | 71FF329BA519147CE806828EC7F78007D374AC479E494BF7C996048D67BAB5D6 | `records/E/mask-record-E6.md`（元の SHA-256） |

- 名を伏せた写しは、元の記録の SHA-256 と合いません。元の SHA-256 と写しの SHA-256 は `mask-record-E6.md` にあります。
- 決定の記録の「決まったこと」の節（`decisions-E6.md`）は、論文の付録 H.3 が名を挙げる 71 の決定の記録から、その節だけを集めた文書です。登録者の言葉と、起草者の問いの逐語は入れていません。
- 記録の目録（`catalog-E6.md`）は、論文の付録 H.3 の 192 の行ごとに、公開の形と置いた道を書いた表です。中身を置かない記録は、名と SHA-256 だけを置いています。

## 4. 計画を変えたこと（2026-10-18）

- 枠と決定 D419-1・D419-2 は、GitHub のリリースから Zenodo の DOI をつけるとしていました。Zenodo のアカウントを用意できなかったため、登録者の決め（2026-10-18）により、Zenodo には置かず、GitHub のリリース（タグ `paper-ja-v1.0`）だけで公開します。DOI は付けていません。置き場の `.zenodo.json` は消しました。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
