# 英語の版の図の記録 v1（2026-10-27 09:24:29 日本時間・器 `E/E5/figs/figs_en_v1.py`・SHA16 5924E586142CB1C2）

- 何か: 日本語の版の図（図 3.1・図 3.2・章 6 と章 8 の機種ごとの図 9）の英語の版。入力・照らし・計算・描き方は日本語の版の器（`E/E3/calc/calc1_2_scale_figures.py` v0.5・`calc3_model_figures.py` v0.5）のまま、字だけを凍結した英語に替えた（裁定 D521-3・D522-1・D523）。
- 値の照らし: 描いた値を日本語の版の値の記録と一つずつ照らし、すべて同じだった（図 3.1 の 280 行・図 3.2 の 15 行・機種ごとの図と表の全セル）。
- 字の出所: 図の字の段の凍結した英語 `E/E5/ft/check/fixed/ft-1.md`（SHA-256 3B349CB6F82B8CB7C0E0793E43933E28514705CB2FA9098CDE67C96DA39D7F9F）と、新しい訳の束の直した写し `E/E5/tm/back-tm/fixed/tm-1〜3.md`（凍結の記録 `E/E5/freeze/freeze-E5-en-ft-v1.json` と照らした）。守る字の値は束 `E/E5/ft/bundles/ft-1.md` の「例:」の行から。
- 字の形だけの替え（英語は打っていない）: 目盛りの「4B〔2507〕」→ "4B [2507]"・機種の名の全角の括弧 → 半角・並べの点「・」→「, 」・文と文の間の空き・二行に折る名は語の切れ目で折った。
- 字体: Noto Sans JP（日本語の版と同じ）。

## 字の出所の表（使った順・同じ単位は一度だけ）

| 単位 | 出所 | 図に描いた英語 |
|---|---|---|
| F001 | 図の字の段 | Catastrophic-choice rate |
| F002 | 図の字の段 | (over all responses) |
| F003 | 図の字の段 | Non-answer rate |
| F004 | 図の字の段 | (refusal and non-scorable; same denominator) |
| F005 | 図の字の段 | The "cold strategist" role line is the line for which Addendum V′ reported an increase "in this sentence form, with this wording, in this 4B configuration" with the line "placed after" (record text and scope: Appendix J.2). Points in the figure may differ from Addendum V′ in configuration and placement. Arms with this line are placed under the same interpretive constraints as arms without it and, in addition, under the same dual-use constraint as Addendum V′ (no procedures are written for manipulations that induce an increase). |
| F006 | 図の字の段 | Differences in the figure are not to be read as an effect of any arm (neither the arms with this line nor the arms without it). |
| F007 | 図の字の段 | Differences in the figure are not to be read as an effect of any arm (neither the arm "Onull plus the 'cold strategist' role line" nor the O vs Onull difference). |
| F016 | 図の字の段 | 4B [2507] (Qwen3-4B-Instruct-2507; different training method; right of the dotted line) |
| F019 | 図の字の段 | Marker for 4B [2507] (in all four rows) |
| F011 | 図の字の段 | Not to be read as a comparison of model safety. Differences in the figure are not Stage A verdicts (the verdicts are in the Stage A final report). This is a description outside the registration, a figure drawn post hoc in Stage E. |
| F012 | 図の字の段 | Each arm has 200 trials, and every cell has 200 responses (refusal and non-scorable are kept in the denominator). Of the paper's triad (catastrophic choice, non-catastrophic answer, non-answered [refusal and non-scorable combined]), two are plotted. The non-catastrophic-answer rate is 1 minus the two (in every cell, the four categories [catastrophic, refusal, non-scorable, other answers] sum to the number of responses). |
| F013 | 図の字の段 | The gray bands mark the region outside the Stage A censoring threshold (below 0.05 / above 0.95). Points within the bands, and points for scales that the Stage A final report excluded from contrasts as censored or unmeasurable (a Stage A record term, distinct from the Stage D measurement failure), are not to be read as rate comparisons (Appendix J.5 (iii)). Points are not connected by lines. |
| F020 | 図の字の段 | The eight plotted arms were selected, by a Stage E frame decision (naming the arms to plot; the Stage A effect-seed arms), as the arms included in the effect seeds of the Stage A slope family, and do not depict the slope tests (the five arms O, Osec, Nk, Ncold, and Nstr are not plotted; their values are in the Stage A records). |
| F014 | 図の字の段 | No points are plotted for the mechanistic tier. Mechanistic-tier values are values under a different manipulation (adding or subtracting a direction rather than a preamble), so placing them on the same axis would juxtapose values under different manipulations (Chapter 4). |
| F008 | 図の字の段 | Horizontal axis: model (dense Qwen3 series). Models are ordered by nominal size as given on the public model pages; spacing does not represent size quantitatively. The tick label "Qwen3-4B" is the 4B model of the dense series. 4B [2507] is outside this ordering (right of the dotted line; different marker). |
| F026 | 図の字の段 | Scenario N1 |
| F102 | 図の字の段 | Arms without the "cold strategist" role line |
| F026 | 図の字の段 | Scenario N2 |
| F026 | 図の字の段 | Scenario S1 |
| F026 | 図の字の段 | Scenario S4 |
| F026 | 図の字の段 | Scenario SK |
| F103 | 図の字の段 | Arms with the "cold strategist" role line |
| F017 | 図の字の段 | Arms in the top two rows (legend in pre-registered order) |
| F018 | 図の字の段 | Arms in the bottom two rows |
| F009 | 図の字の段 | Stage A main run (6 dense Qwen3 models and 4B [Qwen3-4B-Instruct-2507] × 5 scenarios; local inference): catastrophic-choice rate and non-answer rate by arm (Wilson 95% intervals) |
| F010 | 図の字の段 | Not a figure showing scale effects |
| F101 | 図の字の段 | Onull plus the "cold strategist" role line |
| F015 | 図の字の段 | Not to be read as symmetric or asymmetric. Stage A points are not to be compared with Stage C pilot points (the runs and routes differ). The magnitudes of the two directions are not to be compared. This is a description of the pilot outside the registration; no verdict labels are assigned. |
| F025 | 図の字の段 | Three of the pilot's nine arms are plotted (by two Stage E frame decisions; both were made after the pilot values were seen and before the figure was drawn; the decision records are in Appendix H). Each arm has 100 responses (refusal and non-scorable are kept in the denominator; checked against the pilot description). The non-catastrophic-answer rate is 1 minus the catastrophic-choice rate and the non-answer rate. |
| F024 | 図の字の段 | Stage C pilot (Qwen3-4B-Instruct-2507; provider Nscale; run on 2026-10-02; 100 trials per arm): catastrophic-choice rate and non-answer rate (Wilson 95% intervals) |
| F030 | 図の字の段 | Section 6.1 |
| F030 | 図の字の段 | Section 8.1 |
| F045 | 図の字の段 | Japanese-prompt registration |
| F046 | 図の字の段 | English-prompt registration |
| T0038 | 新しい訳の束 | grok-4.20 (non-reasoning) |
| T0011 | 新しい訳の束 | O vs Onull |
| T0013 | 新しい訳の束 | OAmi vs Onull |
| T0014 | 新しい訳の束 | OAmi vs O |
| T0012 | 新しい訳の束 | Confirmed decrease |
| T0025 | 新しい訳の束 | Confirmed increase |
| T0017 | 新しい訳の束 | Not confirmed |
| T0044 | 新しい訳の束 | Withheld (response-mode shift) |
| T0028 | 新しい訳の束 | Not assessable (both conditions at floor or ceiling) |
| F044 | 図の字の段 | Measurement failure (response-format breakdown) |
| F038 | 図の字の段 | Not run |
| F060 | 図の字の段 | Intervals are Newcombe hybrid score 95% intervals, not adjusted for multiplicity. Verdict labels were assigned by applying, in order, the pre-test gate, the within-family Holm, and the response-mode shift rule. The three comparisons in each cell are, from top to bottom, "O vs Onull," "OAmi vs Onull," and "OAmi vs O." |
| F061 | 図の字の段 | Withheld is shown as ◇, and comparisons not confirmed as open ○ (including comparisons not confirmed after Holm even when the unadjusted interval excludes 0). The × for not assessable (both conditions at floor or ceiling) is placed slightly above the bar so that it does not overlap the interval bar. |
| F062 | 図の字の段 | The middle panel is a description without verdict labels (open gray hexagons), and the response-mode shift rule is not applied to it. The three panels are to be read side by side (the middle panel is about half the width of the left panel, so the same difference appears shorter). |
| F104 | 図の字の段 | † Marker of prior exposure to results. ‡ Low-power marker (main-run Onull rate [over all responses] below 0.15; Section 6.1). The order of arms and comparisons follows the model table and the comparison order in the frozen registration text (pre-registered order). |
| F050 | 図の字の段 | Difference in catastrophic-choice rate (a − b; over all responses) |
| F051 | 図の字の段 | Comparison (a vs b): difference and 95% interval |
| F052 | 図の字の段 | N vs Onull difference (a − b) |
| F053 | 図の字の段 | Description outside the hypothesis families; no verdict labels |
| F054 | 図の字の段 | Rate difference (N − Onull) |
| F055 | 図の字の段 | over all responses |
| F064 | 図の字の段 | N vs Onull difference (descriptive; no verdict labels) |
| F056 | 図の字の段 | Triad by arm (over all responses) |
| F057 | 図の字の段 | Numbers at the right end are non-answer rates |
| F058 | 図の字の段 | Rate |
| T0019 | 新しい訳の束 | Catastrophic choice |
| T0020 | 新しい訳の束 | Non-catastrophic answer |
| T0021 | 新しい訳の束 | Non-answered (refusal and non-scorable) |
| F104 | 図の字の段 | † Marker of prior exposure to results. ‡ Low-power marker (main-run Onull rate [over all responses] below 0.15; Section 8.1). The order of arms and comparisons follows the model table and the comparison order in the frozen registration text (pre-registered order). |

## 機種ごとの図と表

| 言語の登録 | 機種 | 形 | セル |
|---|---|---|---|
| ja | gemini25flash | figure | 3 |
| ja | grok420nr | figure | 4 |
| ja | deepseekv32-a | figure | 3 |
| ja | deepseekflash | table（英語の版では組み立ての器が新しい訳の束で組む） | 2 |
| ja | llama31-8b-n | figure | 5 |
| ja | llama4scout | figure | 3 |
| ja | mistrallarge3-m | figure | 3 |
| ja | kimik3-m | figure | 3 |
| ja | qwen25coder32b-n | table（英語の版では組み立ての器が新しい訳の束で組む） | 1 |
| ja | qwen38max-a | table（英語の版では組み立ての器が新しい訳の束で組む） | 2 |
| en | gemini25flash | table（英語の版では組み立ての器が新しい訳の束で組む） | 1 |
| en | grok420nr | table（英語の版では組み立ての器が新しい訳の束で組む） | 1 |
| en | deepseekflash | table（英語の版では組み立ての器が新しい訳の束で組む） | 2 |
| en | llama4scout | figure | 3 |
| en | mistrallarge3-m | table（英語の版では組み立ての器が新しい訳の束で組む） | 2 |
| en | kimik3-m | figure | 3 |

## 入力の SHA-256

- `results/stageA/stageA__N1__none__seed62101/cells.json` B191D74180F3F1DE163D69AF301ED604BB185E9978BAC847BDD22B0F70F9B596
- `results/stageA/stageA__N1__none__seed62201/cells.json` F0F5A449D4A7316129BD81BFA91454C3C6F4C4F6F78208C6A2AB7C7289B3DAA6
- `results/stageA/stageA__N1__none__seed62301/cells.json` 3F67C99015212FC2005CF57BB16D22B6CD1B5FD12E098C4D21EFE3E7B3D94616
- `results/stageA/stageA__N1__none__seed62401/cells.json` 46C014264CC9DD5CD909A0A5C646D43B137CEDA40AEC521742F75DFD41D6A9F7
- `results/stageA/stageA__N1__none__seed62501/cells.json` E7215F267A8AC150E8A8ABFF3BD208E5281DCC537362C093FA9615D1FCCA0721
- `results/stageA/stageA__N1__none__seed62601/cells.json` E04B50EA7405633429A1DD163461BE4B6F4C9EC1D82DFE12CA94535DD3E3271E
- `results/stageA/stageA__N1__none__seed62701/cells.json` EB246619D51C94549CACC2C69C7E0A39082983C922411263FF58E20A2390DF92
- `results/stageA/stageA__N2__none__seed62102/cells.json` 59CABBB6F4C8A45A6CD3B7BA14D35CAE7BEE65CAEFE9D1B75095970EB2055C74
- `results/stageA/stageA__N2__none__seed62202/cells.json` 17528ED880C48341269D534C2C9681FFDD886E01CD188C675EE0E91776BD4BE9
- `results/stageA/stageA__N2__none__seed62302/cells.json` 170989B44E5BEE1EBC6F0A2E53BD9A6855D319D0223165DBEC0255A47964E779
- `results/stageA/stageA__N2__none__seed62402/cells.json` 7B08D3ED9D5590D9F81C48A79010715E5EE7415ABA1EF7EDBCDD828AFCD7864B
- `results/stageA/stageA__N2__none__seed62502/cells.json` 7771BEC8A90D0C385DB15858FA433A6A9E3DA94664F6367FE9F89CF90D433B7F
- `results/stageA/stageA__N2__none__seed62602/cells.json` 4E890766A764442B9EFA2053F974F03F67C05E5DC5D8D5939AC71D6E15791950
- `results/stageA/stageA__N2__none__seed62702/cells.json` A035E4412EEEA06EEB35961DFEA34A8ADAD06FD4174C11336E3C889ECAB1D1DA
- `results/stageA/stageA__S1__none__seed62103/cells.json` B6785320F24ACA6894EB20B4B914DDDC4194FFEB625CAACD367CB682CD5A5657
- `results/stageA/stageA__S1__none__seed62203/cells.json` 0B5A5FA9D8B54E5D005F8CCAA366B5667893A982EDA6BA9CECDC5BFA32C2D39E
- `results/stageA/stageA__S1__none__seed62303/cells.json` 27B0B39A7748ED5F7B1F9A2FA8CB8478DE4D4E8A7714BA3551CFADF6DBC2EE47
- `results/stageA/stageA__S1__none__seed62403/cells.json` 8F12550113300B7DC665148C6A94A61DFFA8AFBA0D84FBF02EB9FEDBB0682D15
- `results/stageA/stageA__S1__none__seed62503/cells.json` DB432E66BF14811AD263D65067694207AE208E6AA8588C656F25967E256D4CF0
- `results/stageA/stageA__S1__none__seed62603/cells.json` A0A049674BFECAFABC1271B02F9DC9009FC93F017736093E9503CFC0DAB64267
- `results/stageA/stageA__S1__none__seed62703/cells.json` 87B344D4B5F06828AAC26B8CE2D6450D54E094297D032015083A0CDC3B768F8F
- `results/stageA/stageA__S4__none__seed62104/cells.json` 2FDD204AE09DCD962EF1A4FA5BE888D098CBBFF686829D3A4C974BFEF3D92716
- `results/stageA/stageA__S4__none__seed62204/cells.json` EF220B42DEEE48EE64D8D964547FAEB787A4B5AE75A568B71EB9B5805753E1B9
- `results/stageA/stageA__S4__none__seed62304/cells.json` E6ED26C5DA635B71F35491E18C9B12202B174EED69C228641BEF2DCD268C5666
- `results/stageA/stageA__S4__none__seed62404/cells.json` 764110D7B029BEB1062223B77C013F3175E28EC1CB94DD63C9B637D37DEE65ED
- `results/stageA/stageA__S4__none__seed62504/cells.json` 84ED2F70F2222B10A7340A4E8F2CBAEC181F9D6C951CAD74DCCCC0D93B16ED30
- `results/stageA/stageA__S4__none__seed62604/cells.json` 769BF25DE1D9F49A42FCA457F3F2516273215A954481BDDBF08A50080EB58E0D
- `results/stageA/stageA__S4__none__seed62704/cells.json` EEA79C91BE17EF107001225653C55D15D2C9F1EA951F69829AB414131E19E431
- `results/stageA/stageA__SK__none__seed62105/cells.json` FA34F33E3DF7317A3F85CD9A45CB02822CD625F7D98DCE93615C38C719C1EFB5
- `results/stageA/stageA__SK__none__seed62205/cells.json` 956187D242773A95792A881D02183DFE83B6DA58F60F7F8F04F00F4D9E74C48C
- `results/stageA/stageA__SK__none__seed62305/cells.json` 6090B2869DEA6225063A537218EA0A76E8020B05FB24EBF9C597ACEA0062FB5A
- `results/stageA/stageA__SK__none__seed62405/cells.json` 351A4CE63838E8E23D530581ADEAA13FC26659E48D50CCFE6901DE0A970AA18C
- `results/stageA/stageA__SK__none__seed62505/cells.json` 007328D3292F8561821E9ED5A225A4BEB1FCA286C16B4B67E314A6218399AA5F
- `results/stageA/stageA__SK__none__seed62605/cells.json` 7FFE5A9D03A361B53AFF8E0B5CA4FAD5408E21529495A71F9FBA60AC3AD5C072
- `results/stageA/stageA__SK__none__seed62705/cells.json` 8391BFF406F85844B9324B86CB0F7B04E4D361D330B47EDF0A5966959DB3A630
- `records/pilotC/describe-pilotC.json` 6E62DCD1A09C080E63C6D82F864146932DF74C7C445C4F12E61D3C31A64A3E76
- `records/D1p/confirm/confirm-D1p.json` F08238ED5B56A6DF24B8D2587CD43DB3C68B7EF793C038538AA7F9D207BEBDBD（照らした記録 `records/D1p/confirm/confirm-D1p-sha256.txt`）
- `records/D1pE/confirm/confirm-D1pE.json` B42F0DA2F60D8D82B2381FC6A36BFC745229DD40E7DDEB35179A2462981FB168（照らした記録 `records/D1pE/confirm/confirm-D1pE-sha256.txt`）

## 出力の SHA-256

- `calc1/calc1-values-en.json` F30013C2A06A388F15F247C20FF8EF0175D3B263C78A4BD7A593E4D701108ED8
- `calc1/fig-calc1-stageA-en.png` FFBC1084790BE63A8BECC3347EE689BAE56B70DEC4628D786E0D214E53C62EB1
- `calc2/calc2-values-en.json` 013B3110386A40B6D5BD32F58F25688AB1F427FC029EE366D29B01AC9F17B8C2
- `calc2/fig-calc2-pilotC-en.png` D1F422E138D2619500DB3858E582EC8285EBEE8F5D306F66D16D08DABCDB004A
- `calc3/calc3-values-en.json` CEBE0BFDC946E3C7840298D4843F923245DAEA0735D1081CF085AEB0571DBEF0
- `calc3/calc3-values-ja.json` F0E19AD2B813825763E899D53B5714E0BAA80E243F676FC33A1C9AF681A5CBA1
- `calc3/en/fig-kimik3-m.png` D72F777047C844CBD4750F1EECA07778CB46D7CAD3E3FAE7E7CD4E6AAEB49EE0
- `calc3/en/fig-llama4scout.png` 6715CC89C92A6D4918ED5A338CA551259552F3CC6EDFC0FC9C47D016762A7FBA
- `calc3/ja/fig-deepseekv32-a.png` ACC3E92AD7300A0E0746BE4E3848F57EB9ABF5ABD63AD37EE0D1EA1FC8F6E961
- `calc3/ja/fig-gemini25flash.png` 8B6636B40ED572ECB6F83CE29EE7D52DBAEA6F49BD50E3A5D32988B849C06F5F
- `calc3/ja/fig-grok420nr.png` 79E24AC0E5B207D49E9E2FDB844B7FFDC642FD89E60F0E47393A5A9D0FA44B5A
- `calc3/ja/fig-kimik3-m.png` 8D3806215D492E90559DA6D304BFB774AA0289865ED1EA06D71BBFFA29399DEA
- `calc3/ja/fig-llama31-8b-n.png` 151BBDC807647CD137B3C7B027304CD0FD92A5A8152EAADCF28C683BEE3F4F20
- `calc3/ja/fig-llama4scout.png` 3DA9957136FB803FB0FCD2DADA9A941B059A91F78889F529628ECC2A6AE6E5AA
- `calc3/ja/fig-mistrallarge3-m.png` 39340F5AB58161B40A527E2667A8AD26013690739755CF035E025EF6CB16C43F

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
