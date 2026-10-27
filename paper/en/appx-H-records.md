# Appendix H Record Repositories and SHAs

This appendix has five sections. H.1 gives, for the main records tracked by git in the public repository, the SHA-256 computed on the HEAD contents and the commit that last changed each. H.2 is the check of the SHA-256 values stamped in the pre-run SHA records of the two registrations against the HEAD contents of the public repository, and the check of the stamp of the calibration rules. Because the frozen registration texts themselves were first committed when the results were published, the only rows whose identity with the stamped values can be confirmed from outside are the rows in H.2 marked "same" or "same after normalizing line endings to LF" (for the Japanese-prompt registration, 10 of the 43 stamped items; for the English-prompt registration, 36 of the 111 items; there are no rows marked "different"). The main items that cannot be checked are the sealed records, the file of the stamp of the calibration rules (for the Japanese-prompt registration), the predictions of the Japanese-prompt registration, and the two aggregation scripts that assigned the verdict labels (internal; their public form is in H.3) and their settings. The verdict labels can be rebuilt from the counts in the published aggregation output with the computational reproduction script (Section 11.3). The frozen registration texts, the preamble and scenario materials, the scoring script, and the two runner scripts are among the checkable rows. Three files that contain names have not been published; when published, they will be masked copies and will not match the stamped SHAs (Section 2.6). H.3 gives the locations and publication plans of the internal records and scripts that the paper uses as sources of scripted insertions and that the main text names or refers to by number; where a file with the same contents is in the public repository, it is marked "published". H.4 gives, chapter by chapter, the sources (file, line, SHA16) of the quotations, figures, and tables in the main-text chapters (Abstract to Chapter 10). H.5 is the correspondence for the decision records and scripts that the main-text chapters refer to without giving numbers or paths.

## H.1 Records in the public repository

[Start of inserted table] Source: 〈internal〉 `E/E3/calc/records-v0.8/records-sha-E3-v0.8.md` (SHA16 545E3C27F5AEA86A). What follows is a table that the drafter's script built from the records, rendered into English, and its terms are the paper's terms (the Japanese terms in the table were replaced with terms translated through this paper's translation procedure, and numbers, codes, and paths were copied as is by the script; how the table was built and which records were read are given at the head of the source file and in its build record).

### Record locations and SHAs (public repository; computed from the contents at HEAD afeb5a0; 2026-10-17 06:33:43 JST; script `E/E3/calc/records_sha_E3_v08.py` v0.8)

#### Stage D, Japanese-prompt registration (D1′)

| File | SHA-256 (contents at HEAD) | Last modifying commit |
|---|---|---|
| `records/D1p/00-frame-D1p.md` | 40BF3C3663BA8C6920617FEFC36636C04AAAD79411F0BE2A5F696449FD78B2E0 | a7af6cc 2026-10-11 |
| `records/D1p/README-D1p.md` | C04E7DF17A35A1068486A2ADE36E634C39EA4C276953B6F8F7F0D5C4C0232332 | d8001f4 2026-10-11 |
| `records/D1p/closing/closing-D1p.json` | 07233B95F110A67895C6CEA7F69D1601F221B06530001E554E5FCF0F0C9626D0 | bf4ade1 2026-10-10 |
| `records/D1p/closing/closing-D1p.md` | 92C1F31250ED7ED9D883BCECAA7D154A012B59BA9CAA5E51C48E466C309E028D | bf4ade1 2026-10-10 |
| `records/D1p/closing/inventory-D1p.json` | 5F21AB44C6792618F561CBD35AD687B6A8753099C89AABBE515DAADB20676569 | bf4ade1 2026-10-10 |
| `records/D1p/confirm/confirm-D1p-sha256.txt` | D056D67A4D12ABDA8C0276EFF3DF9119A1DDEDC68489572B4AC6B0B7E608AC5A | 72032e6 2026-10-10 |
| `records/D1p/confirm/confirm-D1p.json` | F08238ED5B56A6DF24B8D2587CD43DB3C68B7EF793C038538AA7F9D207BEBDBD | a7af6cc 2026-10-11 |
| `records/D1p/confirm/confirm-D1p.md` | 1C750DC6FD1A5C689F7940E434657005354611E9990A02D52B20D2B3667E9FCA | a7af6cc 2026-10-11 |
| `records/D1p/invocation-text-D1p.md` | F84F8A8375A0BB0ECD3AB66DAF6E948CF83E49B695D9D01A453B6D398BBD2F9B | a7af6cc 2026-10-11 |
| `records/D1p/prerun-seal-D1p.md` | C4AFEC83EF05C22AAF849EC825C0C876B57DA3AEA436F0D7A6DC1D73D6C9D073 | 806c87e 2026-10-10 |
| `records/D1p/results-D1p-FINAL-2026-10-11.md` | 0AFDCBF29BC47E0436A42274CEB3C58F0EBBFFB714A63A4C51F23B72FDC271F4 | a7af6cc 2026-10-11 |
| `records/D1p/reviews-index-D1p.md` | 5BF19C22318452A24AD0339731058EF88D62E398C9D56F75D939398F79A697C7 | d8001f4 2026-10-11 |

#### Stage D, English-prompt registration (D1′E)

| File | SHA-256 (contents at HEAD) | Last modifying commit |
|---|---|---|
| `records/D1pE/00-frame-D1pE.md` | F557603870509EA21337E98F3F03542023751B90E8368B513EC235D8149B278E | e549c2b 2026-10-13 |
| `records/D1pE/README-D1pE.md` | 5C7124676E805D1F70B55F6192D2D7E1DDB753755A6064A44BB08A95A33CD3EC | 37927e9 2026-10-13 |
| `records/D1pE/calibration/00-frame-D1pE-cal.md` | 5C21615162C7B43DD82427C4EDE39A5FCA4B4C552E2260A100EB89D36C68048C | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-deepseekflash.json` | ECE96623E11C8D2148C259C7E5A294C083D1C47FFDDDF57464EFE3956FB15F8D | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-deepseekflash.md` | 025321A2FF9E3174AE02892CFED9DC43873409C3840C072D288A833A3A3F31D2 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-gemini25flash.json` | 77A7568C55EECF548F1ADF4C92FEB493F1DD180EF963D5D411B2FC5925CA4907 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-gemini25flash.md` | 476A808ACF4CA68546F48CF4F5AC2D235BD2FDD79DE0FE8640B517424DD1CD30 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-grok420nr.json` | B9FCB0C9B44AC0ABAFFA5989AD3E5D9B690E9AFA254312D9F04C8E23E8D8A53E | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-grok420nr.md` | 84932B2FD9C32F69BEDE3E643B9553479110294F8FE40C3DE8513A5793B4824E | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-kimik3-m.json` | 32DC45D94835F1E0FBE88E7E04ECB1E1072A28E16F4ABEF3334663583662AE9B | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-kimik3-m.md` | 1B4597FBD9591AE0051571B0230267CAEDAAA1265F8E1D82703FD5E6C352B9B1 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-llama4scout.json` | 5839C54E2A33CAABA6BADAD19AC171E9488B3B5D8ED8C0F33A209709E29CB4C1 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-llama4scout.md` | 7F72C152B997BACE82ECC079792FE0F1D926786E3EF25B863350914AFE815C2E | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-mistrallarge3-m.json` | 5DD2AA5EF7F5FF42FA1993D2392A2BD66EA307DFDF113F25A1D64098300AA772 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-mistrallarge3-m.md` | C68FD57F55946FEC5CC1074BE2B1646AE6D701D38D25EC9AF6E28CC716C8D7EE | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-qwen38max-a.json` | 2B46E87DB7D833A0F0E6AEC2FFA86AD43B5A78EC011FDFF36BC3CE799244442A | e549c2b 2026-10-13 |
| `records/D1pE/calibration/describe-D1pEc-qwen38max-a.md` | 00FE31E4A20C3C00D7F7ED4E33B7DB06223275928BFB8B087D493EFB84A5E68D | e549c2b 2026-10-13 |
| `records/D1pE/calibration/endcheck-decision-deepseekflash.json` | E1D69BF57418C31319C9941DE87BB864732B107160EDFDED14D10844F28DF32A | e549c2b 2026-10-13 |
| `records/D1pE/calibration/endcheck-decision-gemini25flash.json` | 886A1FB27ACC0C15DF67E0564EF7F4E55A19547401B95703E21AA87ABA55EB26 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/endcheck-decision-grok420nr.json` | 1A2E27CD46001A7F6E0866A127B4A1D8F08A689FE5AE0705AE9B1CE05D17EB12 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/endcheck-decision-kimik3-m.json` | 240899714E91FDC2D47FD8FA07876823D648805DF19F0A0A2E8900E1BE39069B | e549c2b 2026-10-13 |
| `records/D1pE/calibration/endcheck-decision-llama4scout.json` | 75373F4D97467121D17D2F8612818DD3889701868B07F9AE8104B1DF23D7159D | e549c2b 2026-10-13 |
| `records/D1pE/calibration/endcheck-decision-mistrallarge3-m.json` | C93EB9C5DE97B33D2BD334FA5AF4040F6C7E7D167B2142AF70ADCC727C578D5B | e549c2b 2026-10-13 |
| `records/D1pE/calibration/frame-stamp-D1pE-cal.md` | 2155B5EAD23585A03F7692A691B8FE27CB11EB425EFADB535FF98D7A22E259F4 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/predictions-D1pE-cal-coordinator.md` | F72232E20B1361E6F13388644A116D031C10C94E42CA49A059CA5F20E77DA96B | e549c2b 2026-10-13 |
| `records/D1pE/calibration/predictions-check-D1pE-cal.md` | 95276D65FDD159B5370A11C2806F9BEB7E60CDD220A34B604324B8081DBE4C17 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667FAE8F4DBF2C98DCF98B08723632483746FE24AFF3DE73399 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-deepseekflash.json` | 9A5BA59F51B8DFAE680167F8135C8BC9F3281168EA05DC153796FA766529BDA1 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-gemini25flash.json` | DB58939E96447E3783468238527BA96EB4A27D239A3954F26321F6B0D04D770A | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-grok420nr.json` | 3ABC6E092097CD88505CDC03BB1449DD3ACE5C59D9A2487FF6D9F2645C273305 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-kimik3-m.json` | 7C2BCE049AC9726C21F8A5E903C676D5F6BE5F68D5D2D1C4D1393E45FCE62151 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-llama31-8b-n.json` | 9962B68C8703506F259949596BCF12F3E9597E00658D4D77CF0B788AD4C19156 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-llama4scout.json` | EDA5BC83C9BCCA59D0D416875EE67DFACDBCAC624982FA834B8CF839D265C4DC | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-mistrallarge3-m.json` | F599E5B87656EB6AE786CFB63E5D1E9D9E68AE8A0370DDE050DFD7AE3BCBF487 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-qwen25coder32b-n.json` | 3F7CF5B591079800CEB2BF180697FE8D17C2965DC80F9ABEDCA849E8C333E852 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/reading/summary-qwen38max-a.json` | 56F7B8F25A641CF39F6449E0C04B2C15794AD2B56EB1069C42BBCFF2AC3C1E2F | e549c2b 2026-10-13 |
| `records/D1pE/calibration/stage-note-D1pE-cal.md` | EA34173BF80DDA6D7166B01EA362A57930D753513050535E024ED76FC08D522C | e549c2b 2026-10-13 |
| `records/D1pE/calibration/summary-D1pE-cal.json` | 2D02DB2C34A213B3AFF300E32F2FF569FA1D937E054E481AC02F25212BEDE163 | e549c2b 2026-10-13 |
| `records/D1pE/calibration/summary-D1pE-cal.md` | 6FA0D549C224A12BDBB12FBE904081B960A165FE9849876443D97608B7F38FB8 | e549c2b 2026-10-13 |
| `records/D1pE/closing/closing-D1pE.json` | 8254C962F747FAD8F2336BB01B412091D5116A0F9058B7C938171744EEB82C7F | a10d82a 2026-10-13 |
| `records/D1pE/closing/closing-D1pE.md` | A385D6E065939589720EEACA3B696670089F4C3ABD43848FD8080D73673FCB02 | a10d82a 2026-10-13 |
| `records/D1pE/closing/inventory-D1pE.json` | FC893D7B893C7BAF2343AABC11BFA20F9C99F5A3F7761F632EF54E14BD412D9F | a10d82a 2026-10-13 |
| `records/D1pE/confirm/confirm-D1pE-sha256.txt` | DE6E2597AA5E3645DD8424406A9265ACF6448B670D7098D15EA695503503DC93 | e03dac3 2026-10-13 |
| `records/D1pE/confirm/confirm-D1pE.json` | B42F0DA2F60D8D82B2381FC6A36BFC745229DD40E7DDEB35179A2462981FB168 | e549c2b 2026-10-13 |
| `records/D1pE/confirm/confirm-D1pE.md` | DE68AB25DA97A8A47172A1CB1EE448D828C971FF63F84CA3ED46AE1F9C59AA7F | e549c2b 2026-10-13 |
| `records/D1pE/deviation-D1pE-1/MOVE-RECORD-2026-10-12.md` | A280A25D6C25C1808BB2E6A432FE43CEF26B690417E4B533EF41DAB49B9337AB | e549c2b 2026-10-13 |
| `records/D1pE/deviation-D1pE-1/deviation-D1pE-1.md` | B4AF13A6E3B231F5FCAC43965BB578818AD991089409ACC0C4353C0F62974377 | e549c2b 2026-10-13 |
| `records/D1pE/deviation-D1pE-2.md` | 4553F3761F92C5548605BDF35A36BCB3EF6ADA90682EF3D4F8447371B9FB9F58 | e549c2b 2026-10-13 |
| `records/D1pE/predictions-D1pE.md` | DAAD741AB038BD9B564C1E9A9CC5720EBDC4AD0A1DDFAE2AF1B8921CB308C5C4 | e549c2b 2026-10-13 |
| `records/D1pE/predictions-note-D1pE.md` | A2E0D267982E113067DE23BC575A137D30653D5E524B0E26C1257AA7025F0CE1 | e549c2b 2026-10-13 |
| `records/D1pE/prerun-seal-D1pE.md` | 5627463476415BC51FF7138C91E69AFCBBDE3F541ED278987ED538E278E6D08A | 169af45 2026-10-12 |
| `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 4DC7738F03A37B05A71198E8D0DA3193CECCB624EFF1A8D740D388266BC7DEF2 | e549c2b 2026-10-13 |
| `records/D1pE/reviews-index-D1pE.md` | 70214CE18A7615E4847DEA15B176ACEBC983FC0C12AB4C59027B0FFE23FC0569 | 37927e9 2026-10-13 |
| `records/D1pE/translation/freeze-xlate-D1pE.md` | 593054E132FD1F89DB8030E376644A5DE89347B466FD2142F188D3C46A9F27BA | e549c2b 2026-10-13 |

#### Stage D materials and scoring scripts

| File | SHA-256 (contents at HEAD) | Last modifying commit |
|---|---|---|
| `arms/NOTICE.md` | 13F032B8FB25F53D3FE8FE3F65D65B52A36727B872AB82A51294D0D4DA007E9E | 2b9cc09 2026-09-05 |
| `arms/SOURCES.md` | 4AA2B161A9271CA85F57BBC50B2796E6E5CC6E45E6E6C3609171C27AC647B8F9 | 49f06a8 2026-10-14 |
| `arms/en-D1pE/MANIFEST-en.json` | 41407D45D02E1B8BC24F0775AE35DB597C4720CB075E3FF6D6C220F2F7F7F543 | 169af45 2026-10-12 |
| `arms/en-D1pE/OAmi-en.md` | 4147B0B24FA4C8F24F1E4B2E196E7707E7B8265213E4AE0C171599DE06703BB3 | 169af45 2026-10-12 |
| `arms/en-D1pE/app-scenarios-en.json` | CD343C3D344FF00CFA248324D742244DD61638A9BEF832F0915FECF11713956B | 169af45 2026-10-12 |
| `arms/en-D1pE/preamble-O-en.md` | 815C11569DFB7A60FA15A21FCDCB08D852F9DF9E2C95909818591B0E545A3F9D | 169af45 2026-10-12 |
| `arms/en-D1pE/preamble-Onull-en.md` | EDF2BA377EC46444E5F111B46A32DCB4603F03B29F2E40FDBA5E57F70CEEA8A4 | 169af45 2026-10-12 |
| `arms/frozen-from-ryokai-os/app-scenarios.json` | 7AD7E49459D5C40203DF04F6819575796AD3E880BCB5A12801635BF304E4DDC1 | bcfef09 2026-09-05 |
| `arms/frozen-from-ryokai-os/armsE/preamble-O.md` | F3EE60C33F825575CE4D9D3AFB7409FD5BAA130A3C51C2B7130665C16FDEAE12 | bcfef09 2026-09-05 |
| `arms/frozen-from-ryokai-os/armsE/preamble-Onull.md` | 2123B3CD8586E7DF8B9A0A983B1F93A3C4BE4F0A2F9B396ED216CBC60A0FD733 | bcfef09 2026-09-05 |
| `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 12EAA8B845BC0A2FF7FD6B9496213D20C880C993747C5F512A8551886CA84389 | bcfef09 2026-09-05 |
| `arms/panel/OAmi.md` | 94F1829E701FEB889D3E466F35F3A42A64DB7101947BD804FFE9E66F7F90D96C | 806c87e 2026-10-10 |

#### Stage E

| File | SHA-256 (contents at HEAD) | Last modifying commit |
|---|---|---|
| `records/E/preopen-sha256-E2.txt` | 2C61A83ED7AC1E1549934FE5885ACC55956DADBE84313076B4E7A0898608DEE9 | 6ae0015 2026-10-14 |
| `records/E/reading-judgments-sha256-E2.txt` | 7732A786A71633659EDC015DE422D15B12DAE43671745DB3F0B5DFEC92E3891B | 8ed53f8 2026-10-14 |
| `records/E/stamp-frame-E-addendum1.md` | 20F9354FFBAB65BB5AA139375C32D61CE3AE7E7AA6CC8F365AFFAA81D6580013 | 4c1d90a 2026-10-14 |
| `records/E/stamp-frame-E-addendum2.md` | F8453C55868CDE528B7A9F6CA93888D9DE79F52F49EC94CA0FB17C3B83234AF9 | afeb5a0 2026-10-14 |
| `records/E/stamp-frame-E1.md` | 7557BB6C826B9E6DCE89679DF3A0B0040D141398FD02572DB8666532E37FE6E1 | 5876c82 2026-10-14 |

#### Earlier-stage frozen designs, final reports, and interim summary

| File | SHA-256 (contents at HEAD) | Last modifying commit |
|---|---|---|
| `README.md` | 7F1A0EC08A06BAF348D8457E56443A34D09943EA6C0014A3A7E8C5D726FD8B15 | e549c2b 2026-10-13 |
| `design/design-Bl3-FROZEN.md` | E9EFA213C514BFA6383344DEB183F4EA3401F2EA9FC22730C7472CE6F75640B0 | dae26d7 2026-09-26 |
| `design/design-Blens-FROZEN.md` | A6281F419F0591457BB09FFC1506290D1BB1CB6D91D0DE6AF3097B7E9F9FD930 | 5eb187b 2026-09-24 |
| `design/design-Bprime-FROZEN.md` | 3541FD34C0AD8133458DFA533F0C9469F0057AA4FD1A91D5B9E873CCB874DDE0 | dcd9617 2026-10-01 |
| `design/design-stageA-FROZEN.md` | C30AF752D353190453D9EEE2AA3204CA5A0CC6C6286FA8BF31A9E69C139FEEC9 | 5767c2c 2026-09-16 |
| `design/design-stageB-FROZEN.md` | 8B3D54E4500B46FFB247BD5E0CB1345C047970A1432631461123A41223EB6FC4 | aea6c52 2026-09-20 |
| `design/design-stageF-FROZEN.md` | 33EEB98E11E8BC2DD4DBA9F422DA128F78ABEBA27B3E5CE4E4AAD3E7067C93A2 | b53b3fe 2026-09-11 |
| `design/design-stageM-FROZEN.md` | AB81C9C85787A66A3D39B184DE1D33AC251750A8E2AAE7425178BDF8CA8F9401 | 2c7753a 2026-09-09 |
| `design/design-stageVprime-FROZEN.md` | B087C92BC355D812D41F758A8F5AE699C854D4CD0FFF88BB44CAB7EC8D97B40F | c497697 2026-09-07 |
| `design/design-v1.0-FROZEN.md` | D7963FE1C011341BE8724ECC5C2862F0E5DDB9F122FC066C30500D6040CCCACF | 8b94ba2 2026-09-05 |
| `records/A/results-report-A-FINAL-2026-09-17.md` | 4CE0E96078597244C2FF4131AEF4B3E1B9E7A6B57AB26CCCBB70FA03A8BE75E9 | 92d0c5d 2026-09-17 |
| `records/B/results-B-FINAL-2026-09-23.md` | A40E9CA0D388753BA8B8E59AE137D39A247AF3CAD3740320A21506190413DC40 | 4d13197 2026-09-23 |
| `records/Bl3/results-Bl3-FINAL-2026-09-27.md` | 90EEB93792733FAC23C07E20FEE02AD75CD6E7BE1DE8D79BA8F39405003388E5 | 1099f27 2026-09-27 |
| `records/Blens/results-Blens-FINAL-2026-09-24.md` | A17C7F647653767721EAAD9A3E2F5FAD01155CDAE09B27C208E50EAE3EB6EFAF | 807f29c 2026-09-24 |
| `records/Bprime/results-Bprime-FINAL-2026-10-01.md` | 145CEDBC5EFB0DD6BCEB63711190F3C1A65771A07676496F89FE2CA43A1F40B6 | e9766fc 2026-10-01 |
| `records/DEVIATIONS.md` | 761AC7F46FD40A9B4F35DB842776C33CAE6823EC6B7F194386B0B1CB879C8287 | 4365a8d 2026-09-17 |
| `records/F/results-report-F-FINAL-2026-09-12.md` | AD7C7367C9D3B3FC8BDD29F1B9C5AA8D48A428A36F53873A11F51B16FAB84304 | a3f2dfa 2026-09-12 |
| `records/FREEZE-RECORD.md` | 7C5528E0BC75CC83A097F7B7698C05698E0040C64844B57F08E81EBA75A02E85 | b4dd234 2026-10-01 |
| `records/M/results-report-M-FINAL-2026-09-11.md` | 6E9EFFE8AB399F0FF97E0D421787B9EEDA43122A3F15262B595C6B8832ABCAA6 | a748332 2026-09-11 |
| `records/pilotC/00-frame-pilotC-2026-10-02.md` | 27A44D09FA20668061D06878D9BFC7B178F211E7182D25294A8A6B73054A3C9C | 7d376c1 2026-10-02 |
| `records/pilotC/describe-pilotC.json` | 6E62DCD1A09C080E63C6D82F864146932DF74C7C445C4F12E61D3C31A64A3E76 | 7d376c1 2026-10-02 |
| `records/results/results-report-FINAL-2026-09-07.md` | 9E494CE4D9D5687ABF69ABF4F68820BE34F602E10EC5F363450EF375521FC74A | b9fb685 2026-09-07 |
| `records/vprime/results-report-Vprime-FINAL-2026-09-09.md` | 5E70EF329C4A6739BD3997916BFC108A14818ED393F3C3DFC20F4BC616BDC8C4 | b067db0 2026-09-09 |
| `summary/summary-interim-FINAL-2026-10-02.md` | 059FF367B34B1A23650F02B1EEC9A52E792D2A6469F5CAAE43D2DDC348990B26 | 037eeb0 2026-10-02 |

- Only the files tracked by git in the public repository were counted (107). Records that are not public, such as the sealed ledger (in the records, the "seal ledger"), are not in this table. The names and SHAs of the sealed ledger are in the inventories of the public closing records of the two registrations (`records/D1p/closing/inventory-D1p.json`, `records/D1pE/closing/inventory-D1pE.json`). The three files of the Japanese-prompt registration that contain names (line 243 of the frozen registration text) are not public; when they are made public, they will be copies with the names masked and will not match the stamped SHAs (Section 2.6). The locations of the internal records are in H.3.

[End of inserted table] The source file was inserted with its Japanese terms replaced by translated terms. Numbers, codes, and paths were not changed. Number of removed lines containing the sentence prohibiting quotation (lines beginning with "本記録のいかなる数値も", "本票のいかなる数値も", or "本表のいかなる数値も", including any leading ">"): 1. Of these, lines in quotation form: 0. Location of the removed lines (by heading): under "Earlier-stage frozen designs, final reports, and interim summary". After removal, no line beginning with the same sentence remains (checked by the script). Number of levels by which headings were demoted: 2. No marks were added.

## H.2 Check of the SHAs committed before the runs against the HEAD of the public repository

[Start of inserted table] Source: 〈internal〉 `E/E3/calc/records-v0.8/seal-check-E3-v0.8.md` (SHA16 10C96A624D7676CF). What follows is a table that the drafter's script built from the records, rendered into English, and its terms are the paper's terms (the Japanese terms in the table were replaced with terms translated through this paper's translation procedure, and numbers, codes, and paths were copied as is by the script; how the table was built and which records were read are given at the head of the source file and in its build record).

### Check of the SHAs committed to before the run against HEAD of the public repository (HEAD afeb5a0; 2026-10-17 06:33:43 JST; script `E/E3/calc/records_sha_E3_v08.py` v0.8)

- How to read: "Stamped value" is the value in the three sections (SHA-256, stamp text, and table with line endings normalized to LF) of the pre-run SHA record (in the records, the "seal record"; a file pushed to the public repository before the run). "HEAD value" is the SHA-256 of the contents at the current HEAD of the public file with the same name. The check is one of: same; same with line endings normalized to LF (the stamped local bytes contain CRLF); different; not in the public repository. For rows whose name is not a repository location (such as the names of inventory items), only the recorded name string and the value are copied. The three files that contain names are not public (the copies with the names masked have not been made public yet either), and they fall in the "not in the public repository" rows of this table.

#### Japanese-prompt registration (D1′)

- Pre-run SHA record: `records/D1p/prerun-seal-D1p.md` (first adding commit 806c87e 2026-10-10; last modifying commit 806c87e 2026-10-10).

| Section | Stamped name | Stamped value | Value in the table with line endings normalized to LF | Public file | HEAD value | Check |
|---|---|---|---|---|---|---|
| SHA-256 | `D1p/frame-stamp-D1p.md` | 050CDCD48CC4CA7B | — | — | — | Not in the public repository |
| SHA-256 | `D1p/predictions-D1p.md` | B64FDF01AD4055F7 | — | — | — | Not in the public repository |
| SHA-256 | Inventory of transferred calibration records (1), json | D378C8C1E2C0E9A9 | — | — | — | Name only (not a repository location) |
| SHA-256 | Inventory of transferred calibration records (1), md | 896994529D1E7779 | — | — | — | Name only (not a repository location) |
| SHA-256 | Inventory of transferred calibration records (2), json | 7FBC6B82D8A9CD99 | — | — | — | Name only (not a repository location) |
| SHA-256 | Inventory of transferred calibration records (2), md | 48D559FD924B308A | — | — | — | Name only (not a repository location) |
| SHA-256 | Inventory of transferred calibration records (3), json | DFDFE2222BF3946B | — | — | — | Name only (not a repository location) |
| SHA-256 | Inventory of transferred calibration records (3), md | DB3328FA3FA83391 | — | — | — | Name only (not a repository location) |
| SHA-256 | `D1p/d0-sealed-inventory-D1p.json` | 98C6E7F0D8F5FAF1 | — | — | — | Not in the public repository |
| SHA-256 | `D1p/endcheck-public-inventory-D1p.json` | 4B2D60A00F867673 | — | — | — | Not in the public repository |
| SHA-256 | `D1p/probe-sealed-inventory-D1p.json` | 76FCC95B442E01C8 | — | — | — | Not in the public repository |
| SHA-256 | `D1p/balance-declaration-D1p.md` | 23DDA9BF4E064550 | — | — | — | Not in the public repository |
| SHA-256 | `D1p/pass-conditions-post-round3-D1p.md` | CAB05C776794EF1F | — | — | — | Not in the public repository |
| SHA-256 | `D1p/test_d1p_e2e.py` | D3245DD513B636E6 | — | — | — | Not in the public repository |
| SHA-256 | `D1p/e2e-test-D1p.json` | C4FDBC6348A2EA3D | — | — | — | Not in the public repository |
| SHA-256 | `D1p/selfaudit-v04-D1p.json` | 064400D19DE513B1 | — | — | — | Not in the public repository |
| SHA-256 | Internal record of per-model exposure | AC28F82A16FD1C00 | — | — | — | Name only (not a repository location) |
| SHA-256 | Internal table of excluded model families | 2F6F6DC88D7C8C13 | — | — | — | Name only (not a repository location) |
| SHA-256 | `D1p/policy-readings-D1p.md` | ED62B356F2BDE9B3 | — | — | — | Not in the public repository |
| SHA-256 | Internal record of per-model exposure, addendum | AB2E796CF99F4D9C | — | — | — | Name only (not a repository location) |
| SHA-256 | `D1p/diff-draft3-to-frozen-D1p.md` | 3CDE04B61865399A | — | — | — | Not in the public repository |
| Stamp text | `tools/run_preamble_api_d.py` | A04D40B934392A47 | A04D40B934392A47 | `tools/run_preamble_api_d.py` | A04D40B934392A47 | Same |
| Stamp text | `arms/panel/OAmi.md` | 94F1829E701FEB88 | 94F1829E701FEB88 | `arms/panel/OAmi.md` | 94F1829E701FEB88 | Same |
| Stamp text | `arms/panel/SHA-LEDGER.json` | 5490F273BAD89EFF | 5490F273BAD89EFF | `arms/panel/SHA-LEDGER.json` | 5490F273BAD89EFF | Same |
| Stamp text | `arms/frozen-from-ryokai-os/app-scenarios.json` | 796D73F2544956D7 | 7AD7E49459D5C402 | `arms/frozen-from-ryokai-os/app-scenarios.json` | 7AD7E49459D5C402 | Same with line endings normalized to LF |
| Stamp text | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 56553F926272CF8A | 12EAA8B845BC0A2F | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 12EAA8B845BC0A2F | Same with line endings normalized to LF |
| Stamp text | `arms/frozen-from-ryokai-os/armsE/preamble-O.md` | 18FBB2004ECF8858 | F3EE60C33F825575 | `arms/frozen-from-ryokai-os/armsE/preamble-O.md` | F3EE60C33F825575 | Same with line endings normalized to LF |
| Stamp text | `arms/frozen-from-ryokai-os/armsE/preamble-Onull.md` | 464DF5DD72DF31D0 | 2123B3CD8586E7DF | `arms/frozen-from-ryokai-os/armsE/preamble-Onull.md` | 2123B3CD8586E7DF | Same with line endings normalized to LF |
| Stamp text | `arms/materials-draft/hei/refuse-rules-v2.json` | 22625AEC81875362 | 22625AEC81875362 | `arms/materials-draft/hei/refuse-rules-v2.json` | 22625AEC81875362 | Same |
| Stamp text | `arms/materials-draft/hei/incentive-lexicon-v2.json` | F3D7568C2FDA0BB7 | F3D7568C2FDA0BB7 | `arms/materials-draft/hei/incentive-lexicon-v2.json` | F3D7568C2FDA0BB7 | Same |
| Stamp text | `D1p/d1p_config.py` | 2735FE8FDF9B802E | 2735FE8FDF9B802E | — | — | Not in the public repository |
| Stamp text | `D1p/d1p_anchor.py` | 87F31505ACB5D97F | 87F31505ACB5D97F | — | — | Not in the public repository |
| Stamp text | `D1p/d1p_run.py` | 171884E23985D423 | 171884E23985D423 | — | — | Not in the public repository |
| Stamp text | `D1p/d1p_close.py` | FAA625B8276824AB | FAA625B8276824AB | — | — | Not in the public repository |
| Stamp text | `D1p/d1p_confirm.py` | 3E92994DF6ADBE0F | 3E92994DF6ADBE0F | — | — | Not in the public repository |
| Stamp text | `D1p/extract_sealed_access_log_D1p.py` | 486DF76A4924FDC0 | 486DF76A4924FDC0 | — | — | Not in the public repository |
| Stamp text | `D1p/make_prerun_seal_D1p.py` | 2AE026AF2DFCEEAF | 2AE026AF2DFCEEAF | — | — | Not in the public repository |
| Stamp text | `D1p/reference-D1p.json` | A95A2E02EAC2E43A | A95A2E02EAC2E43A | — | — | Not in the public repository |
| Stamp text | `D1p/main-cost-by-model-D1p.json` | F8716B47EAA66D97 | F8716B47EAA66D97 | — | — | Not in the public repository |
| Stamp text | `D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | 40BF3C3663BA8C69 | `records/D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | Same |
| Stamp text | `D0/d0_config.py` | 0A5722552CC2255D | 0A5722552CC2255D | — | — | Not in the public repository |
| Stamp text | `D0/models-D0w3.json` | F4391EA8C403F947 | F4391EA8C403F947 | — | — | Not in the public repository |
| Stamp text | `D1p/moved-records-paths-D1p.json` | CCF416A5B9E89369 | CCF416A5B9E89369 | — | — | Not in the public repository |

- Check counts: same 6; same with line endings normalized to LF 4; different 0; not in the public repository 24; name only (not a repository location) 9 (total 43; the checkable rows are the 10 rows of "same" and "same with line endings normalized to LF").

#### English-prompt registration (D1′E)

- Pre-run SHA record: `records/D1pE/prerun-seal-D1pE.md` (first adding commit 169af45 2026-10-12; last modifying commit 169af45 2026-10-12).

| Section | Stamped name | Stamped value | Value in the table with line endings normalized to LF | Public file | HEAD value | Check |
|---|---|---|---|---|---|---|
| SHA-256 | `D1pE/frame-stamp-D1pE.md` | 1462926671AE1409 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/predictions-D1pE.md` | DAAD741AB038BD9B | — | `records/D1pE/predictions-D1pE.md` | DAAD741AB038BD9B | Same |
| SHA-256 | `D1pE/endcheck-sealed-inventory-D1pE.json` | 605C2F3C0ABFF3EF | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/endcheck-public-inventory-D1pE.json` | 1ED29FC5103148C4 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/probe-sealed-inventory-D1pE.json` | C6B8BDA6AE01CBC0 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/balance-declaration-D1pE.md` | 4E85A7C5259F09A2 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/test_d1pe_e2e.py` | C8B8BF8CF21E9C11 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/e2e-test-D1pE.json` | C103852B432610D7 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/frame-stamp-D1pE-cal.md` | 2155B5EAD23585A0 | — | `records/D1pE/calibration/frame-stamp-D1pE-cal.md` | 2155B5EAD23585A0 | Same |
| SHA-256 | `D1pE/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | — | `records/D1pE/calibration/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | Same |
| SHA-256 | `D1pE/summary-D1pE-cal.md` | 6FA0D549C224A12B | — | `records/D1pE/calibration/summary-D1pE-cal.md` | 6FA0D549C224A12B | Same |
| SHA-256 | `D1pE/stage-note-D1pE-cal.md` | EA34173BF80DDA6D | — | `records/D1pE/calibration/stage-note-D1pE-cal.md` | EA34173BF80DDA6D | Same |
| SHA-256 | `D1pE/materials-build-D1pE.md` | 14CF8C1D229E651F | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/translation/final/freeze-xlate-D1pE.md` | 593054E132FD1F89 | — | `records/D1pE/translation/freeze-xlate-D1pE.md` | 593054E132FD1F89 | Same |
| SHA-256 | `D1pE/availability-check-D1pE.md` | 32F77BB2B58EB905 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/availability-check-D1pE-addendum.md` | EE395330057E93E8 | — | — | — | Not in the public repository |
| SHA-256 | `D1p/policy-readings-D1p.md` | ED62B356F2BDE9B3 | — | — | — | Not in the public repository |
| SHA-256 | `plans/policy-readings-cold-arm-2026-10-11.md` | 99E909958B1961DD | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/reading-raw-inventory-D1pE.json` | 81F5A4D9BB6EEC06 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/summary-D1pE-cal.json` | 2D02DB2C34A213B3 | — | `records/D1pE/calibration/summary-D1pE-cal.json` | 2D02DB2C34A213B3 | Same |
| SHA-256 | `D1pE/reference-D1pE.json` | FC0A5DFBA6761E91 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/reading-rule-B-D1pE.json` | 98BC85BF929A1000 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/tools-log-D1pE-cal.md` | B7B7F7A4C6B6A5C4 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/tools-log-D1pE-main.md` | 4D90EB9DB5E138BC | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/incident-safegrep-reading-raw-2026-10-12.md` | 0D374CFCE8A9A1E4 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-a-v0.json` | D710A6914F9AC5E9 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/balance-line-D1pE.json` | 500D54D6E1E0495A | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/balance-line-D1pE.md` | 25A036BE15537255 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/reading/summary-deepseekflash.json` | 9A5BA59F51B8DFAE | — | `records/D1pE/calibration/reading/summary-deepseekflash.json` | 9A5BA59F51B8DFAE | Same |
| SHA-256 | `D1pE/describe-D1pEc-deepseekflash.json` | ECE96623E11C8D21 | — | `records/D1pE/calibration/describe-D1pEc-deepseekflash.json` | ECE96623E11C8D21 | Same |
| SHA-256 | `D1pE/endcheck-decision-deepseekflash.json` | E1D69BF57418C313 | — | `records/D1pE/calibration/endcheck-decision-deepseekflash.json` | E1D69BF57418C313 | Same |
| SHA-256 | `D1pE/reading/summary-gemini25flash.json` | DB58939E96447E37 | — | `records/D1pE/calibration/reading/summary-gemini25flash.json` | DB58939E96447E37 | Same |
| SHA-256 | `D1pE/describe-D1pEc-gemini25flash.json` | 77A7568C55EECF54 | — | `records/D1pE/calibration/describe-D1pEc-gemini25flash.json` | 77A7568C55EECF54 | Same |
| SHA-256 | `D1pE/endcheck-decision-gemini25flash.json` | 886A1FB27ACC0C15 | — | `records/D1pE/calibration/endcheck-decision-gemini25flash.json` | 886A1FB27ACC0C15 | Same |
| SHA-256 | `D1pE/reading/summary-grok420nr.json` | 3ABC6E092097CD88 | — | `records/D1pE/calibration/reading/summary-grok420nr.json` | 3ABC6E092097CD88 | Same |
| SHA-256 | `D1pE/describe-D1pEc-grok420nr.json` | B9FCB0C9B44AC0AB | — | `records/D1pE/calibration/describe-D1pEc-grok420nr.json` | B9FCB0C9B44AC0AB | Same |
| SHA-256 | `D1pE/endcheck-decision-grok420nr.json` | 1A2E27CD46001A7F | — | `records/D1pE/calibration/endcheck-decision-grok420nr.json` | 1A2E27CD46001A7F | Same |
| SHA-256 | `D1pE/reading/summary-kimik3-m.json` | 7C2BCE049AC9726C | — | `records/D1pE/calibration/reading/summary-kimik3-m.json` | 7C2BCE049AC9726C | Same |
| SHA-256 | `D1pE/describe-D1pEc-kimik3-m.json` | 32DC45D94835F1E0 | — | `records/D1pE/calibration/describe-D1pEc-kimik3-m.json` | 32DC45D94835F1E0 | Same |
| SHA-256 | `D1pE/endcheck-decision-kimik3-m.json` | 240899714E91FDC2 | — | `records/D1pE/calibration/endcheck-decision-kimik3-m.json` | 240899714E91FDC2 | Same |
| SHA-256 | `D1pE/reading/summary-llama4scout.json` | EDA5BC83C9BCCA59 | — | `records/D1pE/calibration/reading/summary-llama4scout.json` | EDA5BC83C9BCCA59 | Same |
| SHA-256 | `D1pE/describe-D1pEc-llama4scout.json` | 5839C54E2A33CAAB | — | `records/D1pE/calibration/describe-D1pEc-llama4scout.json` | 5839C54E2A33CAAB | Same |
| SHA-256 | `D1pE/endcheck-decision-llama4scout.json` | 75373F4D97467121 | — | `records/D1pE/calibration/endcheck-decision-llama4scout.json` | 75373F4D97467121 | Same |
| SHA-256 | `D1pE/reading/summary-mistrallarge3-m.json` | F599E5B87656EB6A | — | `records/D1pE/calibration/reading/summary-mistrallarge3-m.json` | F599E5B87656EB6A | Same |
| SHA-256 | `D1pE/describe-D1pEc-mistrallarge3-m.json` | 5DD2AA5EF7F5FF42 | — | `records/D1pE/calibration/describe-D1pEc-mistrallarge3-m.json` | 5DD2AA5EF7F5FF42 | Same |
| SHA-256 | `D1pE/endcheck-decision-mistrallarge3-m.json` | C93EB9C5DE97B33D | — | `records/D1pE/calibration/endcheck-decision-mistrallarge3-m.json` | C93EB9C5DE97B33D | Same |
| SHA-256 | `D1pE/incident-safegrep-reading-raw-2026-10-12-addendum.md` | 6B5026A73A44BAFE | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/tools-log-D1pE-main-v01.md` | F9F0E9EF5D95EE06 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/tools-log-D1pE-main-v02.md` | 05106E73B555796C | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/terms-check-moonshot-D1pE.md` | 8D90710EB1F246A2 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/reading-names-D1pE.md` | 758CFD42D03DFE39 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/reading-names-D1pE.json` | 9CA7BB5B0B263C06 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/reading-names-D1pE-addendum.md` | 59C4F0A240169574 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r1/sealed-access-log-D1pE.json` | D4CE51FBAF66DA37 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r1/sealed-access-log-D1pE.md` | 3E9F141AC315FF78 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r1/review-selfaudit-r1.md` | 1B53770C5375D11E | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r2/sealed-access-log-D1pE.json` | D118E8BDF9AE0E54 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r2/sealed-access-log-D1pE.md` | 3E7D00C670E58B81 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r2/review-selfaudit-r2.md` | 4B3A27FE7CA43554 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-a-v0.md` | 89A18F1662FDF607 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/power-D1pE-v0.json` | 920B0EC4B01FAAA2 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/sim-style-shift-D1pE-v0.json` | F5B838F999BE2518 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/test-d1pe-deepseek-page-v0.json` | 79BA6B934ECD0CF1 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/balance_line_D1pE.py` | 23BCB5F39B2BF01C | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/check_memory_values_D1pE.py` | DE957E2ACBFF2F9D | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/00-frame-D1pE-cal.md` | 5C21615162C7B43D | — | `records/D1pE/calibration/00-frame-D1pE-cal.md` | 5C21615162C7B43D | Same |
| SHA-256 | `D1pE/predictions-check-D1pE-cal.md` | 95276D65FDD159B5 | — | `records/D1pE/calibration/predictions-check-D1pE-cal.md` | 95276D65FDD159B5 | Same |
| SHA-256 | `D1pE/reference-text-check-D1pE.md` | 6DD21BFC81A3111D | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r3/sealed-access-log-D1pE.json` | 6B6C62AAA30A79A8 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r3/sealed-access-log-D1pE.md` | 6BCF22F4DB6E2E39 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/selfaudit-r3/review-selfaudit-r3.md` | 3CC6CBC189BFD666 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-b-v0.1.json` | 0CD139C005ACFAEA | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-b-v0.1.md` | EBB6FE1831030A57 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/memory-check-D1pE.json` | 46B81FE8DBE27B5C | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/test-d1pe-units-final.json` | 4CD1CDE8D1A50B4A | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/test-d1pe-dry-paths-final.json` | 15DCB039EFF24A55 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/scan-names-D1pE-freeze.json` | 258574DEF774CEB4 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/scan-maker-words-D1pE-freeze.json` | E0595A3548B17D01 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/diff-final-draft-to-frozen-D1pE.md` | B6FBA677D893F58E | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/test-d1pe-confirm-names-final.json` | DADBFD4EB55788C9 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/test-d1pe-frame-cover-final.json` | C1373DFC15FAEC23 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/ratio-copies-inventory-D1pE-freeze.json` | 4EFBF1D02720AE7E | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/scan-banned-phrases-D1pE-freeze.json` | 723C80D8C89E18BC | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/tools-log-D1pE-main-v03.md` | E285163E78AECAA2 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/ratio-copies-inventory-D1pE.json` | 11F03FFFF791216F | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/ratio-copies-inventory-D1pE.md` | 9BDCA4D0383643E6 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/tools-log-D1pE-main-v04.md` | C1C8F88D6391F279 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/reference-text-check-D1pE-judgement.md` | DE5C9FEE8C2F2DE0 | — | — | — | Not in the public repository |
| SHA-256 | `D1pE/terms-check-moonshot-D1pE-final.md` | 2ACB2FF1099670A9 | — | — | — | Not in the public repository |
| Stamp text | `tools/run_preamble_api_d1pe.py` | F09CC223F9AA4B4E | F09CC223F9AA4B4E | `tools/run_preamble_api_d1pe.py` | F09CC223F9AA4B4E | Same |
| Stamp text | `arms/en-D1pE/OAmi-en.md` | 4147B0B24FA4C8F2 | 4147B0B24FA4C8F2 | `arms/en-D1pE/OAmi-en.md` | 4147B0B24FA4C8F2 | Same |
| Stamp text | `arms/en-D1pE/preamble-O-en.md` | 815C11569DFB7A60 | 815C11569DFB7A60 | `arms/en-D1pE/preamble-O-en.md` | 815C11569DFB7A60 | Same |
| Stamp text | `arms/en-D1pE/preamble-Onull-en.md` | EDF2BA377EC46444 | EDF2BA377EC46444 | `arms/en-D1pE/preamble-Onull-en.md` | EDF2BA377EC46444 | Same |
| Stamp text | `arms/en-D1pE/app-scenarios-en.json` | CD343C3D344FF00C | CD343C3D344FF00C | `arms/en-D1pE/app-scenarios-en.json` | CD343C3D344FF00C | Same |
| Stamp text | `arms/en-D1pE/MANIFEST-en.json` | 41407D45D02E1B8B | 41407D45D02E1B8B | `arms/en-D1pE/MANIFEST-en.json` | 41407D45D02E1B8B | Same |
| Stamp text | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 56553F926272CF8A | 12EAA8B845BC0A2F | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 12EAA8B845BC0A2F | Same with line endings normalized to LF |
| Stamp text | `D1pE/d1pe_main_config.py` | DFBC19D781535502 | DFBC19D781535502 | — | — | Not in the public repository |
| Stamp text | `D1pE/d1pe_config.py` | 97E953ECCF52E18D | 97E953ECCF52E18D | — | — | Not in the public repository |
| Stamp text | `D1pE/d1pe_anchor.py` | 0E38A7B9CEE6F76A | 0E38A7B9CEE6F76A | — | — | Not in the public repository |
| Stamp text | `D1pE/d1pe_run.py` | A91BD15359BEE8A7 | A91BD15359BEE8A7 | — | — | Not in the public repository |
| Stamp text | `D1pE/d1pe_close.py` | A3F9E16254A096F6 | A3F9E16254A096F6 | — | — | Not in the public repository |
| Stamp text | `D1pE/d1pe_confirm.py` | F4094799DBEE9DCA | F4094799DBEE9DCA | — | — | Not in the public repository |
| Stamp text | `D1pE/extract_sealed_access_log_D1pE.py` | 3C83AF760FD45130 | 3C83AF760FD45130 | — | — | Not in the public repository |
| Stamp text | `D1pE/make_prerun_seal_D1pE.py` | 57E1594111794D78 | 57E1594111794D78 | — | — | Not in the public repository |
| Stamp text | `D1pE/reference-D1pE-main.json` | BE92C0365EB0C02E | BE92C0365EB0C02E | — | — | Not in the public repository |
| Stamp text | `D1pE/main-cost-by-model-D1pE.json` | B167507F7B9BA61F | B167507F7B9BA61F | — | — | Not in the public repository |
| Stamp text | `D1pE/00-frame-D1pE.md` | F557603870509EA2 | F557603870509EA2 | `records/D1pE/00-frame-D1pE.md` | F557603870509EA2 | Same |
| Stamp text | `D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | 40BF3C3663BA8C69 | `records/D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | Same |
| Stamp text | `D0/d0_config.py` | 0A5722552CC2255D | 0A5722552CC2255D | — | — | Not in the public repository |
| Stamp text | `D0/models-D0w3.json` | F4391EA8C403F947 | F4391EA8C403F947 | — | — | Not in the public repository |
| Stamp text | `D1p/safe_grep_D1p.py` | 03FDAE36C8871044 | 03FDAE36C8871044 | — | — | Not in the public repository |

- Check counts: same 35; same with line endings normalized to LF 1; different 0; not in the public repository 75; name only (not a repository location) 0 (total 111; the checkable rows are the 36 rows of "same" and "same with line endings normalized to LF").

#### Stamps of the calibration rules (stamped internally before calibration; copies to the public repository)

- The stamps are records stamped in the internal repository before calibration was run, and they were not placed in the public repository before calibration (the stamp times are self-attested). If there is a public copy, the commit that first placed it in the public repository is given. The calibration for the Japanese prompts was stamped per round (first round; second round and its addendum for one model family; third round).

| Registration | Stamp (internal repository) | Stamp time (header text of the stamp) | Stamped name | Stamped value | Public copy | HEAD value | Check | Commit that first placed it in the public repository |
|---|---|---|---|---|---|---|---|---|
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/00-frame-D1pE-cal.md` | 5C21615162C7B43D | `records/D1pE/calibration/00-frame-D1pE-cal.md` | 5C21615162C7B43D | Same | e549c2b 2026-10-13 |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_config.py` | 97E953ECCF52E18D | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_reading.py` | 546E2175457BBCD2 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_cal_run.py` | EE40E1A07AB3CD9E | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_cal_describe.py` | FA9FED3A32ADE777 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_endcheck.py` | 3D6E2BB0A01DB24F | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/make_materials_D1pE.py` | B9CF1D79B3CF8A3C | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/make_runner_d1pe.py` | DBECC708B20DE2A5 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/make_stamp_D1pE_cal.py` | 0C60F005149B3A4F | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/reading-questions-D1pE.json` | 5BE5F5EDA02DCF9E | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/reading-rule-B-D1pE.json` | 98BC85BF929A1000 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/reference-D1pE.json` | FC0A5DFBA6761E91 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/materials-build-D1pE.md` | 14CF8C1D229E651F | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/tools-log-D1pE-cal.md` | B7B7F7A4C6B6A5C4 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/predictions-D1pE-cal-coordinator.md` | F72232E20B1361E6 | `records/D1pE/calibration/predictions-D1pE-cal-coordinator.md` | F72232E20B1361E6 | Same | e549c2b 2026-10-13 |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | `records/D1pE/calibration/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | Same | e549c2b 2026-10-13 |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/availability-check-D1pE-prereg.md` | AC931613F6F1E873 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/availability-check-D1pE.md` | 32F77BB2B58EB905 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/availability-check-D1pE-addendum.md` | EE395330057E93E8 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/probe_dsv32_D1pE.py` | A313A562592B6CB9 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/probe-dsv32-D1pE.json` | 7EDF4DA264049C24 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1p/safe_grep_D1p.py` | 7091DA19C57FB6F2 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D0/d0_config.py` | 0A5722552CC2255D | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/translation/final/freeze-xlate-D1pE.md` | 593054E132FD1F89 | `records/D1pE/translation/freeze-xlate-D1pE.md` | 593054E132FD1F89 | Same | e549c2b 2026-10-13 |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/translation/final/xlate-final-D1pE-v0.1.json` | C8A7CFB8942FEA33 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/plan-D1pE-reading-calibration-v0.md` | 2FB49DB29574B068 | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/rulings-D380-2026-10-11.md` | D5063F86D57D7DAE | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/rulings-D381-2026-10-11.md` | 6A3F03487FC072BF | — | — | Not in the public repository | — |
| English | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/rulings-D382-2026-10-11.md` | BF3793870DD51DFA | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/00-frame-D0-2026-10-02.md` | 69C056EC192D6FEE | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/build_frame_D0.py` | 7802989D7D4E2B2C | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/d0_config.py` | 6569C4E8AB543834 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/d0_describe.py` | C6BEA77D26567C16 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/d0_run.py` | 56E2267612304242 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/00-frame-D0w2-2026-10-03.md` | A692FB8E4E921991 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/build_frame_D0w2.py` | DFCE4AA0A2E2EC03 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `tools/run_preamble_api_d.py` | B0F6D8E721CF1AF5 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_config.py` | 6088CF8A96715751 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/models-D0w2.json` | 6D3A51F9DDC992BB | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_describe.py` | B6D94754B47BB0B2 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_reading.py` | FAA90E08C0BD8258 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/reading-questions-D0w2.json` | 026EDCD4BD5940B1 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_ocheck.py` | C7496F5FE87977AB | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_ocheck_describe.py` | 7C7DA3CD1005D39F | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_run.py` | BBA332ADA5899B90 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/predictions-D0w2-coordinator.md` | 3F4B9387D79BF423 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/predictions-seal-D0w2.txt` | 5DBEFD7F9DDBFF5F | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/00-frame-D0w2-〔系統の名〕-2026-10-03.md` | 1DB0FF3FBFB453B5 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/build_frame_D0w2_〔系統の名〕.py` | 8E5B22665E08D29B | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/models-D0w2-〔系統の名〕.json` | 5CD8A3B9C48B15C7 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/openrouter-probe-D0-6c.json` | 56AD06A25DC66DDB | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/predictions-D0w2-〔系統の名〕-coordinator.md` | 52AA3458C4AF2659 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/predictions-seal-D0w2-〔系統の名〕.txt` | F94B118107893F55 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/00-frame-D0w3-2026-10-09.md` | 0A0E0BA75B3FB204 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/build_frame_D0w3.py` | 0FDC17F397EDE2FC | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `tools/run_preamble_api_d.py` | A04D40B934392A47 | `tools/run_preamble_api_d.py` | A04D40B934392A47 | Same | 806c87e 2026-10-10 |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_config.py` | 0A5722552CC2255D | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/models-D0w3.json` | F4391EA8C403F947 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/build_models_D0w3.py` | D01A77D5F3E54D41 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_describe.py` | 25B13A53FB3BBFA7 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_reading.py` | 5B963BDDD9A9525F | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/reading-questions-D0w2.json` | 026EDCD4BD5940B1 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/reading-rescore-rule-D0-7.json` | 19D98D1B4148F455 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/reading_rescore_D0_7.py` | 50E7E35163AB9674 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_ocheck.py` | 15B8EECFE830CE6F | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_ocheck_describe.py` | 4E90DED06CB129D2 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_run.py` | 108A448B73D8FE35 | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/predictions-D0w3-coordinator.md` | FF416C992790FCCB | — | — | Not in the public repository | — |
| Japanese | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/predictions-seal-D0w3.txt` | DEE19D93E168E50E | — | — | Not in the public repository | — |

- Number of stamp rows: English: same 4, not in the public repository 25 / Japanese: not in the public repository 39, same 1.

- Values are the first 16 characters of SHA-256 (the full digits are in the pre-run SHA records and the first table of Appendix H). There are no "different" rows in the tables of the two registrations (different 0).
- Rows with masked names: for internal files whose file names contain the name of a model family calibrated via the aggregator route, that name is written masked as [model family name] (Decisions D325 and D341-5; SHA16 is the value of the file before the name was masked).

[End of inserted table] The source file was inserted with its Japanese terms replaced by translated terms. Numbers, codes, and paths were not changed. Number of removed lines containing the sentence prohibiting quotation (lines beginning with "本記録のいかなる数値も", "本票のいかなる数値も", or "本表のいかなる数値も", including any leading ">"): 1. Of these, lines in quotation form: 0. Location of the removed lines (by heading): under "Stamps of the calibration rules (stamped internally before calibration; copies to the public repository)". After removal, no line beginning with the same sentence remains (checked by the script). Number of levels by which headings were demoted: 2. No marks were added.

## H.3 Internal records and scripts named in the paper

[Start of inserted table] Source: 〈internal〉 `E/E3/calc/records-v0.8/internal-sources-E3-v0.8.md` (SHA16 C790CAE2EE7EEBB8). What follows is a table that the drafter's script built from the records, rendered into English, and its terms are the paper's terms (the Japanese terms in the table were replaced with terms translated through this paper's translation procedure, and numbers, codes, and paths were copied as is by the script; how the table was built and which records were read are given at the head of the source file and in its build record).

### Locations of the internal records and scripts named in the paper (2026-10-17 06:33:43 JST; script `E/E3/calc/records_sha_E3_v08.py` v0.8)

- What this is: the internal records used as sources of the scripted insertions in the paper's manuscript, and the internal files that the main text names or refers to by number (including scripts and decision records). The internal repository is not public. The first 16 characters of SHA-256 and the byte counts are the values at the time this table was built. If a file with the same content is at HEAD of the public repository (checked by git content name), it is marked "Published". Inclusion rules: sources of the manuscript's scripted insertions; internal paths that the manuscript text encloses in "`"; decision numbers (D plus three digits) and internal paths that appear in the manuscript text and in the text of the record lines cited by the quotation insertions; and records that the manuscript text refers to without naming them (rows marked "referred to by the manuscript text" in the table).

| Internal repository | SHA-256 (first 16 characters) | Bytes | Publication plan | Manuscript files that name it |
|---|---|---|---|---|
| `D0/00-frame-D0-2026-10-02.md` | 69C056EC192D6FEE | 11422 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; frame for the first round of the Japanese-prompt calibration [Appendix H.2; calibration decisions for the four main-run models]) |
| `D0/00-frame-D0w2-2026-10-03.md` | A692FB8E4E921991 | 22588 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; frame for the second round of the Japanese-prompt calibration [Appendix H.2; includes the names of aggregator-route models]) |
| `D0/00-frame-D0w2-〔系統の名〕-2026-10-03.md` | 1DB0FF3FBFB453B5 | 7660 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; addendum to the frame for the second round of the Japanese-prompt calibration [one model family; Appendix H.2]) |
| `D0/00-frame-D0w3-2026-10-09.md` | 0A0E0BA75B3FB204 | 28352 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | 05-stageD-methods (in quotations), (referred to by the manuscript text; frame for the third round of the Japanese-prompt calibration [Appendix H.2]) |
| `D0/d0_config.py` | 0A5722552CC2255D | 17129 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | 05-stageD-methods (in quotations) |
| `D0/describe-D0-add-qwen25coder32b-n.md` | AB6401C8D65A7BE9 | 2421 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | 05-stageD-methods (in quotations) |
| `D0/frame-stamp-D0.md` | 16411E351880D511 | 1536 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; stamp of the frame for the first round of the Japanese-prompt calibration [Appendix H.2; calibration decisions for the four main-run models]) |
| `D0/frame-stamp-D0w2-〔系統の名〕.md` | 7178E352B3C0CAB1 | 2037 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; stamp of the addendum [one model family] to the frame for the second round of the Japanese-prompt calibration [Appendix H.2]) |
| `D0/frame-stamp-D0w2.md` | 591C3910085014D1 | 3581 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; stamp of the frame for the second round of the Japanese-prompt calibration [Appendix H.2]) |
| `D0/frame-stamp-D0w3.md` | E0E743D76A6E2650 | 3369 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; stamp of the frame for the third round of the Japanese-prompt calibration [Appendix H.2]) |
| `D0/models-D0w3.json` | F4391EA8C403F947 | 16377 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | 05-stageD-methods (in quotations) |
| `D0/policy-readings-D0w3-2026-10-09.md` | 1CA95E1AB9974191 | 21458 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | 05-stageD-methods (in quotations) |
| `D0/probe-direct-D0w3.json` | 2FBE3777AE3DF4CB | 25179 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | 05-stageD-methods (in quotations) |
| `D0/summary-D0-calibration-2026-10-03-v0.1.md` | 50DBE46CD0D4EDBE | 11005 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; summary of the first and second rounds of the calibration stage [source of the table in Appendix D-ja.4; Appendix E.4]) |
| `D0/summary-D0w3-2026-10-09.md` | 8DA383408D264937 | 12385 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; summary of the calibration stage [source of the table in Appendix D-ja.4; Appendix E.4]) |
| `D0/summary-D0w3-addendum-2026-10-09.md` | A99165FA642088B7 | 5662 | Form of publication to be decided before E6 (Stage E frame §10; names and records of models accessed via aggregator routes, and records of models excluded for licensing reasons, will not be released; Decision D457-1) | (referred to by the manuscript text; addendum to the summary of the calibration stage [source of the table in Appendix D-ja.4; Appendix E.4]) |
| `D1p/balance-declaration-D1p.md` | 23DDA9BF4E064550 | 15072 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1p/d1p_confirm.py` | 3E92994DF6ADBE0F | 61569 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-H-records |
| `D1p/deviation-D1p-1.md` | 25B81707F3901D80 | 5667 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `D1p/deviation-D1p-2.md` | D135AC5758FBA5A0 | 6499 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `D1p/deviation-D1p-3.md` | 96534C6E4F3ABFC1 | 13607 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `D1p/deviation-D1p-4.md` | 89F55CEAF91814E7 | 6574 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `D1p/main-cost-by-model-D1p.json` | F8716B47EAA66D97 | 234 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1p/main-cost-estimate-D1p.md` | 90ADE13D84F990DF | 4508 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1p/policy-readings-D1p.md` | ED62B356F2BDE9B3 | 15909 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1p/power-D1p-v0.json` | 818FBD1D8B8D6B5C | 6617 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), appx-I-rules (in quotations) |
| `D1p/power_D1p.py` | 684FF4D7799FD3AA | 5384 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), appx-I-rules (in quotations) |
| `D1p/predictions-D1p.md` | B64FDF01AD4055F7 | 30252 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-ja |
| `D1p/predictions-check-D1p.md` | BDD536C5FC976EDD | 20235 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-ja |
| `D1p/provider-logging-check-D1p.md` | 265B08646BE5B93C | 8244 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1p/reference-D1p.json` | A95A2E02EAC2E43A | 22951 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 02-methods (in quotations), 05-stageD-methods (in quotations), appx-A-preambles (in quotations) |
| `D1p/sim-style-shift-D1p-v0.json` | 40AA71404336CF58 | 6136 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 02-methods (in quotations), appx-I-rules (in quotations) |
| `D1p/sim_style_shift_D1p.py` | 7B648483109F9C2E | 6480 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 02-methods (in quotations), appx-I-rules (in quotations) |
| `D1p/sweep-promises-D1p-status.md` | 92B4995C78159003 | 13706 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `D1p/test-d1p-deepseek-page-v0.json` | 8CEA39A54A9BDD05 | 1067 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/00-frame-D1pE-cal.md` | 5C21615162C7B43D | 19343 | Published (`records/D1pE/calibration/00-frame-D1pE-cal.md` in the public repository; first added in commit e549c2b on 2026-10-13) | 05-stageD-methods (in quotations), 07-english-materials (in quotations) |
| `D1pE/balance-declaration-D1pE.md` | 4E85A7C5259F09A2 | 8221 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/balance-line-D1pE.json` | 500D54D6E1E0495A | 1992 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/balance-line-D1pE.md` | 25A036BE15537255 | 2322 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/balance_line_D1pE.py` | 23BCB5F39B2BF01C | 6815 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/check_predictions_D1pE.py` | F391555F8B3521CC | 21294 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-en (in quotations) |
| `D1pE/confirm-D1pE-pushed.txt` | EB084593D18923BA | 2124 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 08-results-en (in quotations), appx-E-deviations (in quotations) |
| `D1pE/d1pe_confirm.py` | F4094799DBEE9DCA | 73325 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-H-records |
| `D1pE/describe-D1pEc-<鍵>.json` | — | — | Not in the internal repository, or a folder name (not a file) | 08-results-en (in quotations) |
| `D1pE/deviation-D1pE-*` | — | — | Not in the internal repository, or a folder name (not a file) | appx-E-deviations (in quotations) |
| `D1pE/deviation-D1pE-2.md` | 4553F3761F92C554 | 3848 | Published (`records/D1pE/deviation-D1pE-2.md` in the public repository; first added in commit e549c2b on 2026-10-13) | appx-E-deviations (in quotations) |
| `D1pE/drive-log-D1pE-launch-first.txt` | 4E28D311C35B3030 | 233 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/estimate_main_cost_D1pE.py` | B411965AED9FE0BB | 6654 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/frame-stamp-D1pE-cal.md` | 2155B5EAD23585A0 | 4398 | Published (`records/D1pE/calibration/frame-stamp-D1pE-cal.md` in the public repository; first added in commit e549c2b on 2026-10-13) | (referred to by the manuscript text; stamp of the frame for the English-prompt calibration [Appendix H.2]) |
| `D1pE/main-cost-estimate-D1pE.md` | 0C2BCBA11DCEBC98 | 3303 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/power-D1pE-v0.json` | 920B0EC4B01FAAA2 | 3262 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), appx-I-rules (in quotations) |
| `D1pE/power_D1pE.py` | 8D5E90D38658505F | 5429 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), appx-I-rules (in quotations) |
| `D1pE/predictions-D1pE.md` | DAAD741AB038BD9B | 24624 | Published (`records/D1pE/predictions-D1pE.md` in the public repository; first added in commit e549c2b on 2026-10-13) | appx-D-en (in quotations) |
| `D1pE/reference-D1pE-main.json` | BE92C0365EB0C02E | 6214 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/sim-style-shift-D1pE-v0.json` | F5B838F999BE2518 | 4980 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-I-rules (in quotations) |
| `D1pE/sim_style_shift_D1pE.py` | 0409A75340BEA878 | 7500 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-I-rules (in quotations) |
| `D1pE/terms-check-moonshot-D1pE.md` | 8D90710EB1F246A2 | 3418 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `D1pE/test-d1pe-deepseek-page-v0.json` | 79BA6B934ECD0CF1 | 1067 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `E/00-frame-E-addendum1-2026-10-14.md` | 352BD92D21B3D14D | 21434 | To be published byte-for-byte as stamped (by E6 at the latest; the Stage E frame and the two addenda) | (referred to by the manuscript text; body text of Addendum 1 to the Stage E frame [Appendix E.3]) |
| `E/00-frame-E-addendum2-2026-10-14.md` | 2A870ED3141A92CC | 7168 | To be published byte-for-byte as stamped (by E6 at the latest; the Stage E frame and the two addenda) | appx-F-terms |
| `E/00-frame-E-draft6.md` | AB7491FF30074FBD | 118210 | To be published byte-for-byte as stamped (by E6 at the latest; the Stage E frame and the two addenda) | 00-abstract, 02-methods, 03-4b-and-scale, 06-results-ja, 08-results-en, 09-alternatives-limits, 11-data-and-code, 13-coi, appx-F-terms |
| `E/E2/deviation-E2-1.md` | E79E29DCD2F31EC7 | 6029 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations |
| `E/E2/deviation-E2-2.md` | C29EF9529350D929 | 5531 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations |
| `E/E2/record/E2-record-en.md` | 72E2C99C3CCEC0A7 | 49547 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-en |
| `E/E2/record/E2-record-ja.md` | 171F869D6CFF687E | 101503 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 06-results-ja, appx-D-ja |
| `E/E3/ai-use/ai-use-appendix-E3-v0.2.md` | 3D81499B49D74D1C | 39871 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-G-ai-use |
| `E/E3/availability/availability-table-E3-pw2.md` | DD0746D79FFD5941 | 2716 | To be published with the paper as figures and tables of the paper (E6) | 11-data-and-code |
| `E/E3/calc/calc1-v0.5/calc1-2-record-v0.5.md` | 652F65EEF71359D9 | 2303 | To be published with the paper as figures and tables of the paper (E6) | 03-4b-and-scale, appx-H-records |
| `E/E3/calc/calc1-v0.5/fig-calc1-stageA-v0.5.png` | 9FA05EF4680FAC0F | 402853 | To be published with the paper as figures and tables of the paper (E6) | 03-4b-and-scale |
| `E/E3/calc/calc1_2_scale_figures.py` | 779DBD9FBB730C50 | 21546 | To be published with the paper as figures and tables of the paper (E6) | appx-H-records |
| `E/E3/calc/calc2-v0.5/fig-calc2-pilotC-v0.5.png` | 6A5F28943B23B43C | 153412 | To be published with the paper as figures and tables of the paper (E6) | 03-4b-and-scale |
| `E/E3/calc/calc3-v0.5/calc3-record.md` | E832768E620C6876 | 4880 | To be published with the paper as figures and tables of the paper (E6) | appx-H-records |
| `E/E3/calc/calc3-v0.5/en/fig-kimik3-m.png` | 9589E4F01FB15CA7 | 160379 | To be published with the paper as figures and tables of the paper (E6) | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/fig-llama4scout.png` | 2DD6ABF6B9DA8072 | 161809 | To be published with the paper as figures and tables of the paper (E6) | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-deepseekflash.md` | 40767F8B4B67E1D2 | 2532 | To be published with the paper as figures and tables of the paper (E6) | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-gemini25flash.md` | 0DD062A2F22AD0DE | 1981 | To be published with the paper as figures and tables of the paper (E6) | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-grok420nr.md` | 5696D45D6F5B9165 | 2036 | To be published with the paper as figures and tables of the paper (E6) | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-mistrallarge3-m.md` | 9FBD817EA7F4C883 | 2531 | To be published with the paper as figures and tables of the paper (E6) | 08-results-en |
| `E/E3/calc/calc3-v0.5/ja/fig-deepseekv32-a.png` | BFC81D62DCEE41A1 | 163004 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-gemini25flash.png` | AD9B28D613BCA84D | 160480 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-grok420nr.png` | E47C4A414FA7201D | 178851 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-kimik3-m.png` | A15E13807660397E | 161224 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-llama31-8b-n.png` | C8242D2887474786 | 182464 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-llama4scout.png` | EEDBF551F6E35C31 | 162470 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-mistrallarge3-m.png` | 9A49E2012584306C | 161316 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/table-deepseekflash.md` | 091B3B429A9708EB | 2532 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/table-qwen25coder32b-n.md` | 6A291087A0509225 | 1969 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/table-qwen38max-a.md` | 892967E8652521D6 | 2510 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/calc3_model_figures.py` | EEC38F08D1290D3A | 21102 | To be published with the paper as figures and tables of the paper (E6) | appx-H-records |
| `E/E3/calc/calc4-v0.2/cost-upper-en.md` | 2459DFE162F86DD1 | 3361 | To be published with the paper as figures and tables of the paper (E6) | 11-data-and-code |
| `E/E3/calc/calc4-v0.2/cost-upper-ja.md` | DECDF7E602BC4B97 | 5580 | To be published with the paper as figures and tables of the paper (E6) | 11-data-and-code |
| `E/E3/calc/calsum-v0.3/en/calsum-en.md` | 3EB67A64CB4EDAB2 | 10570 | To be published with the paper as figures and tables of the paper (E6) | appx-D-en |
| `E/E3/calc/calsum-v0.3/ja/calsum-ja.md` | 61EF4472CBF47F86 | 22049 | To be published with the paper as figures and tables of the paper (E6) | appx-D-ja |
| `E/E3/calc/calsum_D.py` | 19278F05A28436AB | 28793 | To be published with the paper as figures and tables of the paper (E6) | appx-D-en, appx-D-ja |
| `E/E3/calc/familytable/en/familytable-en-pw.md` | 304B38C27BBD0BCD | 6103 | To be published with the paper as figures and tables of the paper (E6) | appx-D-en |
| `E/E3/calc/familytable/ja/familytable-ja-pw.md` | E1C8463A0A8FF6BC | 13648 | To be published with the paper as figures and tables of the paper (E6) | appx-D-ja |
| `E/E3/calc/flow/flow-D.json` | ADF65FAD8A647024 | 5620 | To be published with the paper as figures and tables of the paper (E6) | 00-abstract, 01-introduction, 05-stageD-methods |
| `E/E3/calc/flow_D.py` | 68AF73A100F20C1C | 10080 | To be published with the paper as figures and tables of the paper (E6) | appx-H-records |
| `E/E3/calc/records-v0.8/internal-sources-E3-v0.8.md` | — | — | Written by the same script as this table (the SHA is recorded in the build record after writing; to be published with the paper as figures and tables of the paper [E6]) | appx-H-records |
| `E/E3/calc/records-v0.8/records-sha-E3-v0.8.md` | — | — | Written by the same script as this table (the SHA is recorded in the build record after writing; to be published with the paper as figures and tables of the paper [E6]) | appx-H-records |
| `E/E3/calc/records-v0.8/records-stats-E3-v0.8.json` | — | — | Written by the same script as this table (the SHA is recorded in the build record after writing; to be published with the paper as figures and tables of the paper [E6]) | appx-H-records |
| `E/E3/calc/records-v0.8/seal-check-E3-v0.8.md` | — | — | Written by the same script as this table (the SHA is recorded in the build record after writing; to be published with the paper as figures and tables of the paper [E6]) | appx-H-records |
| `E/E3/calc/typecount-v0.1/en/typecount-en.json` | E993C852FE746762 | 5044 | To be published with the paper as figures and tables of the paper (E6) | appx-H-records |
| `E/E3/calc/typecount-v0.1/en/typecount-en.md` | A337D724F058C8CA | 4134 | To be published with the paper as figures and tables of the paper (E6) | 08-results-en |
| `E/E3/calc/typecount-v0.1/ja/typecount-ja.json` | 4A24A0E464C17718 | 7354 | To be published with the paper as figures and tables of the paper (E6) | appx-H-records |
| `E/E3/calc/typecount-v0.1/ja/typecount-ja.md` | 141B0F157F4D2D3E | 4890 | To be published with the paper as figures and tables of the paper (E6) | 06-results-ja |
| `E/E3/calc/typecount_D.py` | E162FEF3890A0B90 | 10840 | To be published with the paper as figures and tables of the paper (E6) | appx-H-records |
| `E/deviation-E-1.md` | 860A734796CBE8FC | 4043 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations |
| `E/deviation-E-2.md` | 7394E2A9D88A1D71 | 3050 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations |
| `E/frame-E-addendum1-stamp.txt` | 97210C9177A9F40D | 3500 | Form of publication to be decided before E6 (the stamp file recording only the SHA-256 of the body text is already published; Appendix E.3) | (referred to by the manuscript text; internal stamp of Addendum 1 to the Stage E frame [Appendix E.3]) |
| `E/frame-E-addendum2-stamp.txt` | 519BB608C48F9D18 | 2230 | Form of publication to be decided before E6 (the stamp file recording only the SHA-256 of the body text is already published; Appendix E.3) | (referred to by the manuscript text; internal stamp of Addendum 2 to the Stage E frame [Appendix E.3]) |
| `E/refs/references-E3-v0.1.md` | 38130220CB391AD0 | 2495 | To be published with the paper as figures and tables of the paper (E6) | 12-references |
| `E/tool1/op4b_reproduce.py` | C379CF16E24A0688 | 13449 | To be published with the paper as the computational reproduction function of the rerun script (version 1.0) (the version that has completed code review [Stage E frame §9]; E6; Stage E frame §10) | 11-data-and-code |
| `E/tool1/op4b_rerun.py` | 0C0662F29E8A249E | 129656 | To be published with the paper as the rerun function of the rerun script (version 1.0) (the version that has completed code review [Stage E frame §9]; E6; Stage E frame §10) | 11-data-and-code |
| `E/tool1/test-criteria-rerun-v1.0.md` | EB7F89D23A9B2B73 | 4981 | Form of publication to be decided before E6 (pass criteria and records for the tests of the rerun script; Stage E frame §7, item 12) | 11-data-and-code |
| `E/tool1/tests/20261016-201735/test-record.md` | E40C9BD521320F87 | 50556 | Form of publication to be decided before E6 (pass criteria and records for the tests of the rerun script; Stage E frame §7, item 12) | 11-data-and-code |
| `plans/deviation-D1pE-1/deviation-D1pE-1.md` | B4AF13A6E3B231F5 | 8437 | Published (`records/D1pE/deviation-D1pE-1/deviation-D1pE-1.md` in the public repository; first added in commit e549c2b on 2026-10-13) | appx-E-deviations, appx-E-deviations (in quotations) |
| `plans/plan-framing-sensitivity-scale-and-mechanism-v1.0-2026-09-07.md` | E242C5FF31EDB05B | 21715 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | (referred to by the manuscript text; plan document v1.0 [Section 9.8]) |
| `plans/plan-framing-sensitivity-scale-and-mechanism-v3.0-2026-10-13.md` | 8165808D28274E82 | 205785 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 09-alternatives-limits, (referred to by the manuscript text; plan document v3.0 [Section 9.8; the version after the results of the two registrations]) |
| `plans/policy-readings-cold-arm-2026-10-11.md` | 99E909958B1961DD | 8735 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D292-D293-2026-10-02.md` | 3E691B25B520CE94 | 4573 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-H-records |
| `plans/rulings-D294-D295-2026-10-03.md` | 3F38CCC468DC62FA | 13433 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods, 05-stageD-methods (in quotations) |
| `plans/rulings-D296-2026-10-03.md` | FAF71095CA2D1A5D | 6250 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods, 05-stageD-methods (in quotations), appx-I-rules (in quotations) |
| `plans/rulings-D300-2026-10-03.md` | AA0CE2D019DF0F96 | 6886 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods, 05-stageD-methods (in quotations), 09-alternatives-limits (in quotations), appx-I-rules (in quotations) |
| `plans/rulings-D301-2026-10-03.md` | 2655E8EDF2067C8A | 1794 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-ja |
| `plans/rulings-D303-2026-10-03.md` | C6083C03497BD6A0 | 8183 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), appx-D-ja, appx-I-rules (in quotations) |
| `plans/rulings-D304-2026-10-04.md` | E432D1F4BAF708EA | 6035 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods, 05-stageD-methods (in quotations) |
| `plans/rulings-D306-2026-10-04.md` | 01C84C4BE4647F41 | 3765 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D318-2026-10-05.md` | 8CE8A546ECF85D3C | 2318 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 09-alternatives-limits (in quotations) |
| `plans/rulings-D322-2026-10-08.md` | EE60B65A302784AE | 4707 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 09-alternatives-limits (in quotations) |
| `plans/rulings-D323-2026-10-08.md` | ABC95DBE1070B1A4 | 6657 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-ja |
| `plans/rulings-D324-2026-10-08.md` | BFAAB0E1A17132C8 | 3328 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 06-results-ja (in quotations) |
| `plans/rulings-D325-2026-10-08.md` | 0710F09588537D1E | 4936 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D327-2026-10-08.md` | E23F86E5553BF284 | 4241 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D328-2026-10-09.md` | 38E343E185109AD8 | 5167 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods, 05-stageD-methods (in quotations), 09-alternatives-limits (in quotations) |
| `plans/rulings-D329-2026-10-09.md` | 8CC1FCD269D02F09 | 4438 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D330-2026-10-09.md` | 1B07ECB5437F945F | 3741 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D332-2026-10-09.md` | AA44266D3B67CD2C | 3305 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D333-2026-10-09.md` | CE5FB40ED4095B04 | 2939 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D334-2026-10-09.md` | DB5C9D44DC0298A3 | 7286 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D335-2026-10-09.md` | E87804C5E24D6FFC | 2932 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D336-2026-10-09.md` | 55F15C328268C791 | 3618 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D337-2026-10-09.md` | 672C6297C177F705 | 2355 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D340-2026-10-09.md` | 466B1D8818FE9B9B | 6083 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 13-coi, 13-coi (in quotations) |
| `plans/rulings-D341-2026-10-09.md` | BF565AABC800B813 | 9437 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods, 05-stageD-methods (in quotations), 06-results-ja, 06-results-ja (in quotations), 09-alternatives-limits (in quotations), 13-coi (in quotations), appx-D-ja, appx-E-deviations, appx-H-records, appx-I-rules (in quotations) |
| `plans/rulings-D343-2026-10-09.md` | FBA61080E3B6C7DE | 16065 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D344-2026-10-09.md` | C187AB12023FDD2B | 13125 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 13-coi (in quotations) |
| `plans/rulings-D345-2026-10-10.md` | 22170ABB115F6C2A | 22912 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 06-results-ja (in quotations), 13-coi (in quotations) |
| `plans/rulings-D346-2026-10-10-addendum.md` | 6D1E75324A076CF0 | 4102 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 13-coi (in quotations) |
| `plans/rulings-D350-2026-10-10.md` | 3F040ACC04D38DB4 | 4127 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 07-english-materials (in quotations) |
| `plans/rulings-D351-2026-10-10.md` | E10605D08A709842 | 8568 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D352-2026-10-10.md` | 540CAAE94A36F2A1 | 4255 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D353-2026-10-11.md` | ED1A37A4F4C0F2D7 | 5336 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D354-2026-10-11.md` | BFC15FD0DD7474CA | 6928 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 06-results-ja (in quotations), appx-D-ja (in quotations), appx-E-deviations (in quotations), appx-F-terms, appx-H-records |
| `plans/rulings-D355-2026-10-11.md` | B8ADF062F659BCCE | 12398 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 06-results-ja (in quotations), appx-E-deviations (in quotations) |
| `plans/rulings-D356-2026-10-11.md` | 7F107F0C65964B92 | 5514 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D357-2026-10-11.md` | 7D2100E284CABB6D | 16051 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 06-results-ja (in quotations), appx-E-deviations (in quotations), appx-H-records |
| `plans/rulings-D363-2026-10-11.md` | CBB470AEC236A518 | 9506 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 07-english-materials, 07-english-materials (in quotations) |
| `plans/rulings-D364-2026-10-11.md` | 570FE2218B07E89D | 5865 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 07-english-materials (in quotations) |
| `plans/rulings-D365-2026-10-11.md` | 08AE91DEA93EED08 | 2625 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 07-english-materials (in quotations) |
| `plans/rulings-D369-2026-10-11.md` | 6CD6BA40F79F9032 | 18323 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 07-english-materials, 07-english-materials (in quotations) |
| `plans/rulings-D373-2026-10-11.md` | B90EE18E5AF2EE77 | 7181 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 07-english-materials, 07-english-materials (in quotations) |
| `plans/rulings-D377-2026-10-11.md` | CA75E574A35BA82A | 4126 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 07-english-materials, 07-english-materials (in quotations), appx-H-records |
| `plans/rulings-D379-2026-10-11.md` | FCF24825B169A381 | 3131 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 07-english-materials (in quotations) |
| `plans/rulings-D380-2026-10-11.md` | D5063F86D57D7DAE | 8686 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods, 05-stageD-methods (in quotations), 08-results-en, 08-results-en (in quotations), appx-I-rules (in quotations) |
| `plans/rulings-D381-2026-10-11.md` | 6A3F03487FC072BF | 6101 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D382-2026-10-11.md` | BF3793870DD51DFA | 6538 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations), 07-english-materials (in quotations) |
| `plans/rulings-D383-2026-10-11.md` | 9F0AD367EAA33B33 | 4935 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 05-stageD-methods (in quotations) |
| `plans/rulings-D386-2026-10-12.md` | 60DF8C9D5F1BBB2A | 15068 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 02-methods (in quotations), 05-stageD-methods (in quotations), 07-english-materials, 07-english-materials (in quotations), 08-results-en (in quotations), 09-alternatives-limits (in quotations) |
| `plans/rulings-D388-2026-10-12.md` | 0877720991317CF8 | 14677 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 02-methods (in quotations), 05-stageD-methods (in quotations), 07-english-materials, 07-english-materials (in quotations), 08-results-en (in quotations), 09-alternatives-limits (in quotations) |
| `plans/rulings-D391-2026-10-12.md` | 346AC0F098751C9E | 30067 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 02-methods (in quotations), 05-stageD-methods (in quotations), 07-english-materials (in quotations), 08-results-en (in quotations), 09-alternatives-limits (in quotations) |
| `plans/rulings-D396-2026-10-12.md` | D9D09672EB50B216 | 13624 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D397-2026-10-12.md` | 8DCD26DC6FA1F9FB | 5844 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D398-2026-10-12.md` | E4E6042E6208ACD9 | 4448 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D399-2026-10-12.md` | 313FEE49101E1787 | 3384 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D400-2026-10-13.md` | 8740511CB957F532 | 2831 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D401-2026-10-13.md` | 0C232914719C1ABE | 2103 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D402-2026-10-13.md` | C1A7C70575999D4D | 3500 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D403-2026-10-13.md` | 58525FD8122208D8 | 12778 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 08-results-en (in quotations), 13-coi, 13-coi (in quotations), appx-D-en (in quotations), appx-E-deviations (in quotations), appx-H-records |
| `plans/rulings-D404-2026-10-13.md` | 8935C11FE85AE7B5 | 4636 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D405-2026-10-13.md` | E05449675DAA29C0 | 7111 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 08-results-en (in quotations), 13-coi, 13-coi (in quotations), appx-D-en (in quotations), appx-E-deviations (in quotations) |
| `plans/rulings-D406-2026-10-13.md` | 673002EB3050011E | 4628 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-E-deviations (in quotations) |
| `plans/rulings-D407-2026-10-13.md` | 86BEB219DCD489F9 | 10051 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 08-results-en (in quotations), 13-coi, 13-coi (in quotations), appx-E-deviations (in quotations) |
| `plans/rulings-D408-2026-10-13.md` | 2E6ACBF8C7617DF0 | 4012 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 13-coi, 13-coi (in quotations), appx-E-deviations (in quotations) |
| `plans/rulings-D419-2026-10-13.md` | 81640BBE2F483258 | 9416 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 13-coi (in quotations) |
| `plans/rulings-D425-2026-10-14.md` | B06AF7777BFB4947 | 6806 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 09-alternatives-limits (in quotations), appx-H-records |
| `plans/rulings-D430-2026-10-14.md` | C1D09DDF370EEB30 | 11832 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 09-alternatives-limits (in quotations) |
| `plans/rulings-D438-2026-10-14.md` | CCA62D750A8A6459 | 4806 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-en |
| `plans/rulings-D445-2026-10-14.md` | F7DA93427AFCED43 | 12806 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | appx-D-ja, appx-E-deviations, appx-H-records |
| `plans/rulings-D450-2026-10-14.md` | 05192AFB4176C8D4 | 18978 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 12-references, 13-coi, appx-H-records |
| `plans/rulings-D452-2026-10-14.md` | 716C5E7D4115A8D2 | 7598 | Form of publication to be decided before E6 (Stage E frame §10; names and SHA-256 values are listed in the records inventory) | 11-data-and-code |
| `summary/reviews/final/rulings-D289.md` | FC71484906BF46F3 | 3357 | Published (`summary/reviews/final/rulings-D289.md` in the public repository; first added in commit 037eeb0 on 2026-10-02) | appx-F-terms |

- Rows: 192 (of which published: 6). Names pointing to the sealed folder and to the folder of moved records (2) were excluded from this table without being read. Decision numbers in quotations for which there is no decision-record file in the internal repository (e.g., numbers in earlier-stage records; no row is created for them in this table): D128, D167, D178, D187, D203, D215, D220, D221, D223, D235, D256, D258, D259, D265, D275, D276, D278, D287, D289, D293.
- Rows with masked names: for internal files whose file names contain the name of a model family calibrated via the aggregator route, that name is written masked as [model family name] (Decisions D325 and D341-5; SHA16 is the value of the file before the name was masked).

[End of inserted table] The source file was inserted with its Japanese terms replaced by translated terms. Numbers, codes, and paths were not changed. Number of removed lines containing the sentence prohibiting quotation (lines beginning with "本記録のいかなる数値も", "本票のいかなる数値も", or "本表のいかなる数値も", including any leading ">"): 1. Of these, lines in quotation form: 0. Location of the removed lines (by heading): under "Locations of the internal records and scripts named in the paper (2026-10-17 06:33:43 JST; script `E/E3/calc/records_sha_E3_v08.py` v0.8)". After removal, no line beginning with the same sentence remains (checked by the script). Number of levels by which headings were demoted: 2. No marks were added.

## H.4 Sources of quotations, figures, and tables in the main-text chapters (by chapter)

The sources (file, line, SHA16) of [Quotation n] and of the figures and tables in the main-text chapters (Abstract to Chapter 10) are given chapter by chapter. This is a table that the build script wrote while assembling the main-text chapters. 〈public〉 denotes a file in the public repository, and 〈internal〉 a file in the internal repository (locations and publication plans are in H.3).

The "Translation" column: quotations translated from Japanese records are marked "Translated", and quotations that quote public English text verbatim are marked "Verbatim".

### Chapter 1 (`01-introduction.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Quotation in running text | 〈public〉 `design/design-v1.0-FROZEN.md` | line 100 | D7963FE1C011341B | Translated |
| [Quotation 2] | Quotation in running text | 〈public〉 `design/design-v1.0-FROZEN.md` | line 99 | D7963FE1C011341B | Translated |
| [Quotation 3] | Quotation in running text | 〈public〉 `records/vprime/results-report-Vprime-FINAL-2026-09-09.md` | line 987 | 5E70EF329C4A6739 | Translated |
| [Quotation 4] | Quotation in running text | 〈public〉 `design/design-v1.0-FROZEN.md` | line 100 | D7963FE1C011341B | Translated |
| [Quotation 5] | Quotation in running text | 〈public〉 `design/design-v1.0-FROZEN.md` | line 100 | D7963FE1C011341B | Translated |

### Chapter 2 (`02-methods.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Quotation in running text | 〈public〉 `arms/frozen-from-ryokai-os/app-scenarios.json` | line 16 | 7AD7E49459D5C402 | Translated |
| [Quotation 2] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 132 | 40BF3C3663BA8C69 | Translated |
| [Quotation 3] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 112 | 40BF3C3663BA8C69 | Translated |
| [Quotation 4] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 113 | 40BF3C3663BA8C69 | Translated |
| [Quotation 5] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 113 | 40BF3C3663BA8C69 | Translated |
| [Quotation 6] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 133 | 40BF3C3663BA8C69 | Translated |
| [Quotation 7] | Quotation in running text | 〈public〉 `README.md` | line 11 | 7F1A0EC08A06BAF3 | Translated |
| [Quotation 8] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | lines 164–166 | 40BF3C3663BA8C69 | Translated |
| [Quotation 9] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 159 | 40BF3C3663BA8C69 | Translated |
| [Quotation 10] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 253 | F557603870509EA2 | Translated |
| [Quotation 11] | Quotation in running text | 〈public〉 `design/design-stageA-FROZEN.md` | line 14 | C30AF752D3531904 | Translated |
| [Quotation 12] | Quotation in running text | 〈public〉 `design/design-Blens-FROZEN.md` | line 436 | A6281F419F059145 | Translated |

### Chapter 3 (`03-4b-and-scale.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 33 | 059FF367B34B1A23 | Translated |
| [Quotation 2] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 35 | 059FF367B34B1A23 | Translated |
| [Quotation 3] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 37–53 | 059FF367B34B1A23 | Translated |
| [Quotation 4] | Quotation in running text | 〈public〉 `design/design-v1.0-FROZEN.md` | line 34 | D7963FE1C011341B | Translated |
| [Quotation 5] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 55 | 059FF367B34B1A23 | Translated |
| [Quotation 6] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 57–63 | 059FF367B34B1A23 | Translated |
| [Quotation 7] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 65 | 059FF367B34B1A23 | Translated |
| [Quotation 8] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 67–76 | 059FF367B34B1A23 | Translated |
| [Quotation 9] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 78 | 059FF367B34B1A23 | Translated |
| [Quotation 10] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 80–87 | 059FF367B34B1A23 | Translated |
| [Quotation 11] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 89 | 059FF367B34B1A23 | Translated |
| [Quotation 12] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 91–106 | 059FF367B34B1A23 | Translated |
| Fig. 3.1 | Figure | 〈internal〉 `E/E3/calc/calc1-v0.5/fig-calc1-stageA-v0.5.png` | — | 9FA05EF4680FAC0F | — |
| [Quotation 13] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 148 | AB7491FF30074FBD | Translated |
| [Quotation 14] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 57 | 059FF367B34B1A23 | Translated |
| [Quotation 15] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 149 | AB7491FF30074FBD | Translated |
| [Quotation 16] | Quotation in running text | 〈public〉 `design/design-stageA-FROZEN.md` | line 48 | C30AF752D3531904 | Translated |
| [Quotation 17] | Paragraph quotation | 〈public〉 `records/pilotC/00-frame-pilotC-2026-10-02.md` | lines 9–10 | 27A44D09FA206680 | Translated |
| [Quotation 18] | Paragraph quotation | 〈public〉 `records/pilotC/00-frame-pilotC-2026-10-02.md` | lines 14–16 | 27A44D09FA206680 | Translated |
| [Quotation 19] | Paragraph quotation | 〈public〉 `records/pilotC/00-frame-pilotC-2026-10-02.md` | lines 20–24 | 27A44D09FA206680 | Translated |
| Fig. 3.2 | Figure | 〈internal〉 `E/E3/calc/calc2-v0.5/fig-calc2-pilotC-v0.5.png` | — | 6A5F28943B23B43C | — |
| [Quotation 20] | Paragraph quotation | 〈public〉 `records/pilotC/00-frame-pilotC-2026-10-02.md` | lines 112–116 | 27A44D09FA206680 | Translated |

### Chapter 4 (`04-mechanism.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Quotation in running text | 〈public〉 `design/design-stageB-FROZEN.md` | line 92 | 8B3D54E4500B46FF | Translated |
| [Quotation 2] | Quotation in running text | 〈public〉 `design/design-stageB-FROZEN.md` | line 31 | 8B3D54E4500B46FF | Translated |
| [Quotation 3] | Quotation in running text | 〈public〉 `design/design-stageB-FROZEN.md` | line 93 | 8B3D54E4500B46FF | Translated |
| [Quotation 4] | Quotation in running text | 〈public〉 `design/design-stageB-FROZEN.md` | line 355 | 8B3D54E4500B46FF | Translated |
| [Quotation 5] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 108 | 059FF367B34B1A23 | Translated |
| [Quotation 6] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 110–142 | 059FF367B34B1A23 | Translated |
| [Quotation 7] | Quotation in running text | 〈public〉 `records/B/results-B-FINAL-2026-09-23.md` | line 212 | A40E9CA0D388753B | Translated |
| [Quotation 8] | Quotation in running text | 〈public〉 `records/B/results-B-FINAL-2026-09-23.md` | line 132 | A40E9CA0D388753B | Translated |
| [Quotation 9] | Quotation in running text | 〈public〉 `records/B/results-B-FINAL-2026-09-23.md` | line 212 | A40E9CA0D388753B | Translated |
| [Quotation 10] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 144 | 059FF367B34B1A23 | Translated |
| [Quotation 11] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 146–154 | 059FF367B34B1A23 | Translated |
| [Quotation 12] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 156 | 059FF367B34B1A23 | Translated |
| [Quotation 13] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 158–176 | 059FF367B34B1A23 | Translated |
| [Quotation 14] | Quotation in running text | 〈public〉 `records/Bl3/results-Bl3-FINAL-2026-09-27.md` | line 470 | 90EEB93792733FAC | Translated |
| [Quotation 15] | Quotation in running text | 〈public〉 `records/Bl3/results-Bl3-FINAL-2026-09-27.md` | line 470 | 90EEB93792733FAC | Translated |
| [Quotation 16] | Quotation in running text | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | line 178 | 059FF367B34B1A23 | Translated |
| [Quotation 17] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 180–191 | 059FF367B34B1A23 | Translated |
| [Quotation 18] | Paragraph quotation | 〈public〉 `summary/summary-interim-FINAL-2026-10-02.md` | lines 397–398 | 059FF367B34B1A23 | Translated |

### Chapter 5 (`05-stageD-methods.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 11 | 40BF3C3663BA8C69 | Translated |
| [Quotation 2] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 11 | F557603870509EA2 | Translated |
| [Quotation 3] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 12 | 40BF3C3663BA8C69 | Translated |
| [Quotation 4] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 12 | 40BF3C3663BA8C69 | Translated |
| [Quotation 5] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 12 | 40BF3C3663BA8C69 | Translated |
| [Quotation 6] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 12 | 40BF3C3663BA8C69 | Translated |
| [Quotation 7] | Paragraph quotation | 〈public〉 `records/D1pE/calibration/00-frame-D1pE-cal.md` | lines 53–56 | 5C21615162C7B43D | Translated |
| [Quotation 8] | Quotation in running text | 〈public〉 `records/D1pE/calibration/00-frame-D1pE-cal.md` | line 49 | 5C21615162C7B43D | Translated |
| [Quotation 9] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 270 | F557603870509EA2 | Translated |
| [Quotation 10] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 13 | F557603870509EA2 | Translated |
| [Quotation 11] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 13 | F557603870509EA2 | Translated |
| [Quotation 12] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 15 | 40BF3C3663BA8C69 | Translated |
| [Quotation 13] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 15 | 40BF3C3663BA8C69 | Translated |
| [Quotation 14] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 29 | 40BF3C3663BA8C69 | Translated |
| [Quotation 15] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 13 | 40BF3C3663BA8C69 | Translated |
| [Quotation 16] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 14 | F557603870509EA2 | Translated |
| [Quotation 17] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 14 | F557603870509EA2 | Translated |
| [Quotation 18] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 12 | 40BF3C3663BA8C69 | Translated |
| [Quotation 19] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | lines 17–26 | 40BF3C3663BA8C69 | Translated |
| [Quotation 20] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 28 | 40BF3C3663BA8C69 | Translated |
| [Quotation 21] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | lines 31–40 | 40BF3C3663BA8C69 | Translated |
| [Quotation 22] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 14 | F557603870509EA2 | Translated |
| [Quotation 23] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 14 | F557603870509EA2 | Translated |
| [Quotation 24] | Paragraph quotation | 〈public〉 `records/D1pE/00-frame-D1pE.md` | lines 16–27 | F557603870509EA2 | Translated |
| [Quotation 25] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | lines 89–109 | 40BF3C3663BA8C69 | Translated |
| [Quotation 26] | Paragraph quotation | 〈public〉 `records/D1pE/00-frame-D1pE.md` | lines 98–111 | F557603870509EA2 | Translated |
| [Quotation 27] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 289 | 40BF3C3663BA8C69 | Translated |
| [Quotation 28] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 289 | 40BF3C3663BA8C69 | Translated |
| [Quotation 29] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 295 | 40BF3C3663BA8C69 | Translated |
| [Quotation 30] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 122 | 40BF3C3663BA8C69 | Translated |
| [Quotation 31] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 122 | 40BF3C3663BA8C69 | Translated |
| [Quotation 32] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 112 | 40BF3C3663BA8C69 | Translated |
| [Quotation 33] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 112 | 40BF3C3663BA8C69 | Translated |
| [Quotation 34] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 114 | 40BF3C3663BA8C69 | Translated |
| [Quotation 35] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 116 | F557603870509EA2 | Translated |
| [Quotation 36] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 290 | 40BF3C3663BA8C69 | Translated |
| [Quotation 37] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 113 | 40BF3C3663BA8C69 | Translated |
| [Quotation 38] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 113 | 40BF3C3663BA8C69 | Translated |
| [Quotation 39] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 113 | 40BF3C3663BA8C69 | Translated |
| [Quotation 40] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 115 | F557603870509EA2 | Translated |
| [Quotation 41] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 116 | 40BF3C3663BA8C69 | Translated |
| [Quotation 42] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 116 | 40BF3C3663BA8C69 | Translated |
| [Quotation 43] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 117 | 40BF3C3663BA8C69 | Translated |
| [Quotation 44] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 118 | 40BF3C3663BA8C69 | Translated |
| [Quotation 45] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 120 | F557603870509EA2 | Translated |
| [Quotation 46] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 296 | 40BF3C3663BA8C69 | Translated |
| [Quotation 47] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 120 | 40BF3C3663BA8C69 | Translated |
| [Quotation 48] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 120 | 40BF3C3663BA8C69 | Translated |
| [Quotation 49] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 120 | 40BF3C3663BA8C69 | Translated |
| [Quotation 50] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 132 | F557603870509EA2 | Translated |
| [Quotation 51] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 132 | F557603870509EA2 | Translated |
| [Quotation 52] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 65 | 4DC7738F03A37B05 | Translated |
| [Quotation 53] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 107 | F557603870509EA2 | Translated |
| [Quotation 54] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 109 | F557603870509EA2 | Translated |
| [Quotation 55] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 119 | 40BF3C3663BA8C69 | Translated |
| [Quotation 56] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 131 | F557603870509EA2 | Translated |
| [Quotation 57] | Quotation in running text | 〈public〉 `records/D1pE/calibration/00-frame-D1pE-cal.md` | line 74 | 5C21615162C7B43D | Translated |
| [Quotation 58] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 119 | 40BF3C3663BA8C69 | Translated |
| [Quotation 59] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 246 | 40BF3C3663BA8C69 | Translated |
| [Quotation 60] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 292 | 40BF3C3663BA8C69 | Translated |
| [Quotation 61] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 292 | 40BF3C3663BA8C69 | Translated |
| [Quotation 62] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 292 | 40BF3C3663BA8C69 | Translated |
| [Quotation 63] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 292 | 40BF3C3663BA8C69 | Translated |
| [Quotation 64] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 292 | 40BF3C3663BA8C69 | Translated |
| [Quotation 65] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 292 | 40BF3C3663BA8C69 | Translated |
| [Quotation 66] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 275 | F557603870509EA2 | Translated |
| [Quotation 67] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 191 | 40BF3C3663BA8C69 | Translated |
| [Quotation 68] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 207 | 40BF3C3663BA8C69 | Translated |
| [Quotation 69] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | lines 140–149 | 40BF3C3663BA8C69 | Translated |
| [Quotation 70] | Paragraph quotation | 〈public〉 `records/D1pE/00-frame-D1pE.md` | lines 176–185 | F557603870509EA2 | Translated |

### Chapter 6 (`06-results-ja.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 12 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 2] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 13 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 3] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 287 | 40BF3C3663BA8C69 | Translated |
| [Quotation 4] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 14–19 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 5] | Quotation of count lines | 〈public〉 `records/D1p/confirm/confirm-D1p.md` | line 14 | 1C750DC6FD1A5C68 | Translated |
| [Quotation 6] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 20 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 7] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 22–24 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 8] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 25–27 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 9] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 133 | 40BF3C3663BA8C69 | Translated |
| [Quotation 10] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 96 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 11] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 98–101 | 0AFDCBF29BC47E04 | Translated |
| Fig. 6.2 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/fig-gemini25flash.png` | — | AD9B28D613BCA84D | — |
| [Quotation 12] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 105–122 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 13] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 126–136 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 14] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 140–152 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 15] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 154 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 16] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 156–161 | 0AFDCBF29BC47E04 | Translated |
| Fig. 6.3 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/fig-grok420nr.png` | — | E47C4A414FA7201D | — |
| [Quotation 17] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 165–187 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 18] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 191–204 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 19] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 208–224 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 20] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 226 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 21] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 228–229 | 0AFDCBF29BC47E04 | Translated |
| Fig. 6.4 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/fig-deepseekv32-a.png` | — | BFC81D62DCEE41A1 | — |
| [Quotation 22] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 233–250 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 23] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 254–264 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 24] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 268–281 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 25] | Quotation in running text | 〈internal〉 `E/E2/record/E2-record-ja.md` | line 901 | 171F869D6CFF687E | Translated |
| [Quotation 26] | Paragraph quotation | 〈internal〉 `E/E2/record/E2-record-ja.md` | lines 903–909 | 171F869D6CFF687E | Translated |
| [Quotation 27] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 283 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 28] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 285–287 | 0AFDCBF29BC47E04 | Translated |
| Table under "6.5 deepseek-flash" | Inserted table | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/table-deepseekflash.md` | — | 091B3B429A9708EB | — |
| [Quotation 29] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 291–303 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 30] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 307–314 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 31] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 318–326 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 32] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 328 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 33] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 330–332 | 0AFDCBF29BC47E04 | Translated |
| Fig. 6.6 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/fig-llama31-8b-n.png` | — | C8242D2887474786 | — |
| [Quotation 34] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 336–363 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 35] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 367–383 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 36] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 387–405 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 37] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 407 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 38] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 409–414 | 0AFDCBF29BC47E04 | Translated |
| Fig. 6.7 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/fig-llama4scout.png` | — | EEDBF551F6E35C31 | — |
| [Quotation 39] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 418–435 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 40] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 439–449 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 41] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 453–465 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 42] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 467 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 43] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 469–470 | 0AFDCBF29BC47E04 | Translated |
| Fig. 6.8 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/fig-mistrallarge3-m.png` | — | 9A49E2012584306C | — |
| [Quotation 44] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 474–491 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 45] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 495–505 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 46] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 509–521 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 47] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 523 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 48] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 525–529 | 0AFDCBF29BC47E04 | Translated |
| Fig. 6.9 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/fig-kimik3-m.png` | — | A15E13807660397E | — |
| [Quotation 49] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 533–550 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 50] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 554–564 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 51] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 568–581 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 52] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 583 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 53] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 585–586 | 0AFDCBF29BC47E04 | Translated |
| Table under "6.10 Qwen2.5-Coder-32B-Instruct" | Inserted table | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/table-qwen25coder32b-n.md` | — | 6A291087A0509225 | — |
| [Quotation 54] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 590–597 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 55] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 601–605 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 56] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 609–614 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 57] | Quotation in running text | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 616 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 58] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 618–619 | 0AFDCBF29BC47E04 | Translated |
| Table under "6.11 Qwen3.8 Max (0902)" | Inserted table | 〈internal〉 `E/E3/calc/calc3-v0.5/ja/table-qwen38max-a.md` | — | 892967E8652521D6 | — |
| [Quotation 59] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 623–635 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 60] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 639–646 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 61] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 650–659 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 62] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 663–683 | 0AFDCBF29BC47E04 | Translated |
| Table under "6.12 Result patterns and the number of models per comparison (descriptive)" | Inserted table | 〈internal〉 `E/E3/calc/typecount-v0.1/ja/typecount-ja.md` | — | 141B0F157F4D2D3E | — |
| [Quotation 63] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 766 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 64] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | lines 731–732 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 65] | Paragraph quotation | 〈public〉 `records/D1p/results-D1p-FINAL-2026-10-11.md` | line 44 | 0AFDCBF29BC47E04 | Translated |
| [Quotation 66] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 281 | 40BF3C3663BA8C69 | Translated |
| [Quotation 67] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 281 | 40BF3C3663BA8C69 | Translated |

### Chapter 7 (`07-english-materials.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 11 | F557603870509EA2 | Translated |
| [Quotation 2] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 11 | F557603870509EA2 | Translated |
| [Quotation 3] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 273 | F557603870509EA2 | Translated |
| [Quotation 4] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 273 | F557603870509EA2 | Translated |
| [Quotation 5] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 273 | F557603870509EA2 | Translated |
| [Quotation 6] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 12 | F557603870509EA2 | Translated |
| [Quotation 7] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 12 | F557603870509EA2 | Translated |
| [Quotation 8] | Quotation in running text | 〈public〉 `records/D1pE/calibration/00-frame-D1pE-cal.md` | line 48 | 5C21615162C7B43D | Translated |
| [Quotation 9] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 12 | F557603870509EA2 | Translated |
| [Quotation 10] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 90 | F557603870509EA2 | Translated |
| [Quotation 11] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 12 | F557603870509EA2 | Translated |
| [Quotation 12] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 12 | F557603870509EA2 | Translated |
| [Quotation 13] | Quotation in running text | 〈public〉 `records/D1pE/translation/freeze-xlate-D1pE.md` | line 11 | 593054E132FD1F89 | Translated |
| [Quotation 14] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 268 | F557603870509EA2 | Translated |
| [Quotation 15] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 268 | F557603870509EA2 | Translated |
| [Quotation 16] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 268 | F557603870509EA2 | Translated |
| [Quotation 17] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 268 | F557603870509EA2 | Translated |

### Chapter 8 (`08-results-en.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 14 | 4DC7738F03A37B05 | Translated |
| [Quotation 2] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 17 | 4DC7738F03A37B05 | Translated |
| [Quotation 3] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 15–16 | 4DC7738F03A37B05 | Translated |
| [Quotation 4] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 18–22 | 4DC7738F03A37B05 | Translated |
| [Quotation 5] | Quotation of count lines | 〈public〉 `records/D1pE/confirm/confirm-D1pE.md` | line 15 | DE68AB25DA97A8A4 | Translated |
| [Quotation 6] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 23 | 4DC7738F03A37B05 | Translated |
| [Quotation 7] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 24 | 4DC7738F03A37B05 | Translated |
| [Quotation 8] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 26–28 | 4DC7738F03A37B05 | Translated |
| [Quotation 9] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 29–31 | 4DC7738F03A37B05 | Translated |
| [Quotation 10] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 253 | F557603870509EA2 | Translated |
| [Quotation 11] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 253 | F557603870509EA2 | Translated |
| [Quotation 12] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 253 | F557603870509EA2 | Translated |
| [Quotation 13] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 171 | F557603870509EA2 | Translated |
| [Quotation 14] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 171 | F557603870509EA2 | Translated |
| [Quotation 15] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 104 | 4DC7738F03A37B05 | Translated |
| [Quotation 16] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 106–108 | 4DC7738F03A37B05 | Translated |
| Table under "8.2 Gemini 2.5 Flash" | Inserted table | 〈internal〉 `E/E3/calc/calc3-v0.5/en/table-gemini25flash.md` | — | 0DD062A2F22AD0DE | — |
| [Quotation 17] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 112–119 | 4DC7738F03A37B05 | Translated |
| [Quotation 18] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 123–127 | 4DC7738F03A37B05 | Translated |
| [Quotation 19] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 131–136 | 4DC7738F03A37B05 | Translated |
| [Quotation 20] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 138 | 4DC7738F03A37B05 | Translated |
| [Quotation 21] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 140–142 | 4DC7738F03A37B05 | Translated |
| Table under "8.3 grok-4.20 (non-reasoning)" | Inserted table | 〈internal〉 `E/E3/calc/calc3-v0.5/en/table-grok420nr.md` | — | 5696D45D6F5B9165 | — |
| [Quotation 22] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 146–153 | 4DC7738F03A37B05 | Translated |
| [Quotation 23] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 157–161 | 4DC7738F03A37B05 | Translated |
| [Quotation 24] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 165–171 | 4DC7738F03A37B05 | Translated |
| [Quotation 25] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 175–176 | 4DC7738F03A37B05 | Translated |
| [Quotation 26] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 178 | 4DC7738F03A37B05 | Translated |
| [Quotation 27] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 180–183 | 4DC7738F03A37B05 | Translated |
| Table under "8.4 deepseek-flash" | Inserted table | 〈internal〉 `E/E3/calc/calc3-v0.5/en/table-deepseekflash.md` | — | 40767F8B4B67E1D2 | — |
| [Quotation 28] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 187–199 | 4DC7738F03A37B05 | Translated |
| [Quotation 29] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 203–210 | 4DC7738F03A37B05 | Translated |
| [Quotation 30] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 214–228 | 4DC7738F03A37B05 | Translated |
| [Quotation 31] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 232–233 | 4DC7738F03A37B05 | Translated |
| [Quotation 32] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 235 | 4DC7738F03A37B05 | Translated |
| [Quotation 33] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 237–241 | 4DC7738F03A37B05 | Translated |
| Fig. 8.5 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/en/fig-llama4scout.png` | — | 2DD6ABF6B9DA8072 | — |
| [Quotation 34] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 245–262 | 4DC7738F03A37B05 | Translated |
| [Quotation 35] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 266–276 | 4DC7738F03A37B05 | Translated |
| [Quotation 36] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 280–304 | 4DC7738F03A37B05 | Translated |
| [Quotation 37] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 308–310 | 4DC7738F03A37B05 | Translated |
| [Quotation 38] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 312 | 4DC7738F03A37B05 | Translated |
| [Quotation 39] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 314–317 | 4DC7738F03A37B05 | Translated |
| Table under "8.6 Mistral Large 3 (2512)" | Inserted table | 〈internal〉 `E/E3/calc/calc3-v0.5/en/table-mistrallarge3-m.md` | — | 9FBD817EA7F4C883 | — |
| [Quotation 40] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 321–333 | 4DC7738F03A37B05 | Translated |
| [Quotation 41] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 337–344 | 4DC7738F03A37B05 | Translated |
| [Quotation 42] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 348–361 | 4DC7738F03A37B05 | Translated |
| [Quotation 43] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 365–367 | 4DC7738F03A37B05 | Translated |
| [Quotation 44] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 369 | 4DC7738F03A37B05 | Translated |
| [Quotation 45] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 371–375 | 4DC7738F03A37B05 | Translated |
| Fig. 8.7 | Figure | 〈internal〉 `E/E3/calc/calc3-v0.5/en/fig-kimik3-m.png` | — | 9589E4F01FB15CA7 | — |
| [Quotation 46] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 379–396 | 4DC7738F03A37B05 | Translated |
| [Quotation 47] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 400–410 | 4DC7738F03A37B05 | Translated |
| [Quotation 48] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 414–430 | 4DC7738F03A37B05 | Translated |
| [Quotation 49] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 434–437 | 4DC7738F03A37B05 | Translated |
| [Quotation 50] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 443–475 | 4DC7738F03A37B05 | Translated |
| Table under "8.8 Result patterns and the number of models per comparison (descriptive)" | Inserted table | 〈internal〉 `E/E3/calc/typecount-v0.1/en/typecount-en.md` | — | A337D724F058C8CA | — |
| [Quotation 51] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 549 | 4DC7738F03A37B05 | Translated |
| [Quotation 52] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | lines 515–516 | 4DC7738F03A37B05 | Translated |
| [Quotation 53] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 517 | 4DC7738F03A37B05 | Translated |
| [Quotation 54] | Paragraph quotation | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 52 | 4DC7738F03A37B05 | Translated |
| [Quotation 55] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 14 | 4DC7738F03A37B05 | Translated |
| [Quotation 56] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 14 | 4DC7738F03A37B05 | Translated |
| [Quotation 57] | Quotation in running text | 〈public〉 `records/D1pE/results-D1pE-FINAL-2026-10-13.md` | line 15 | 4DC7738F03A37B05 | Translated |

### Chapter 9 (`09-alternatives-limits.md`)

| Number or title | Type | Source | Lines | SHA16 | Translation |
|---|---|---|---|---|---|
| [Quotation 1] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | lines 282–284 | 40BF3C3663BA8C69 | Translated |
| [Quotation 2] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 285 | 40BF3C3663BA8C69 | Translated |
| [Quotation 3] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 285 | 40BF3C3663BA8C69 | Translated |
| [Quotation 4] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 286 | 40BF3C3663BA8C69 | Translated |
| [Quotation 5] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 268 | F557603870509EA2 | Translated |
| [Quotation 6] | Quotation in running text | 〈public〉 `arms/frozen-from-ryokai-os/armsE/preamble-O.md` | line 1 | F3EE60C33F825575 | Translated |
| [Quotation 7] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 268 | F557603870509EA2 | Translated |
| [Quotation 8] | Quotation in running text | 〈public〉 `arms/frozen-from-ryokai-os/armsE/preamble-O.md` | line 1 | F3EE60C33F825575 | Translated |
| [Quotation 9] | Quotation in running text | 〈public〉 `arms/panel/OAmi.md` | line 1 | 94F1829E701FEB88 | Translated |
| [Quotation 10] | Quotation in running text | 〈public〉 `records/D1p/00-frame-D1p.md` | line 288 | 40BF3C3663BA8C69 | Translated |
| [Quotation 11] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 294 | 40BF3C3663BA8C69 | Translated |
| [Quotation 12] | Quotation in running text | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 273 | F557603870509EA2 | Translated |
| [Quotation 13] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 291 | 40BF3C3663BA8C69 | Translated |
| [Quotation 14] | Paragraph quotation | 〈public〉 `records/D1pE/00-frame-D1pE.md` | line 274 | F557603870509EA2 | Translated |
| [Quotation 15] | Paragraph quotation | 〈public〉 `records/D1p/00-frame-D1p.md` | line 293 | 40BF3C3663BA8C69 | Translated |
| [Quotation 16] | Paragraph quotation | 〈internal〉 `E/00-frame-E-draft6.md` | line 415 | AB7491FF30074FBD | Translated |
| [Quotation 17] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 415 | AB7491FF30074FBD | Translated |
| [Quotation 18] | Paragraph quotation | 〈internal〉 `plans/plan-framing-sensitivity-scale-and-mechanism-v3.0-2026-10-13.md` | lines 358–360 | 8165808D28274E82 | Translated |
| [Quotation 19] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 121 | AB7491FF30074FBD | Translated |
| [Quotation 20] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 121 | AB7491FF30074FBD | Translated |
| [Quotation 21] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 253 | AB7491FF30074FBD | Translated |
| [Quotation 22] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 254 | AB7491FF30074FBD | Translated |
| [Quotation 23] | Quotation in running text | 〈internal〉 `E/00-frame-E-draft6.md` | line 257 | AB7491FF30074FBD | Translated |

## H.5 Decision records and scripts that the main-text chapters refer to without numbers or paths

The main-text chapters do not give decision-record numbers or script paths (a drafting decision made for readers). The decision records and scripts that the text of the main-text chapters refers to are as follows (the locations of the records are in H.3).

| Chapter / section | Text of the main-text chapters (gist) | Record |
|---|---|---|
| Section 2.3 | The aggregation script always adds to the four cells of the 2×2 table, regardless of whether there is a zero cell | For the Japanese-prompt registration, line 147 of `D1p/d1p_confirm.py`; for the English-prompt registration, line 153 of `D1pE/d1pe_confirm.py` |
| Sections 2.8, 5.3, and 5.13 | The decision not to publish the calibration records of aggregator routes (not stating which models or how many models) | Decisions D341-5 and D445 |
| Section 2.9 | The one sentence of the records left at the head of Appendix D-en | Decision D450-6 |
| Section 3.6 | The two decisions on the selection of the three arms in Fig. 3.2 | Decisions D292 and D425-5 |
| Section 5.4 | The script that counted the table below the frozen registration text | `E/E3/calc/flow_D.py` |
| Section 5.4 | The decision made after Qwen2.5-Coder-3B was excluded for licensing reasons | Decision D341-2 |
| Sections 6.0 and 6.15 | Retroactive confirmation of the reading of the scope (2026-10-11 08:59) | Decision D357-3 |
| Section 6.12 | Decision made after seeing the verdict labels (judging the pattern) | Decision D354-3 |
| Section 7.3 | The four corrections to the translation | Decision D377 |
| Section 8.8 | Decision made after seeing the verdict labels (judging the pattern and how to apply "OAmi vs O") | Decision D403-2 |
| Sections 3.5 and 3.6 (Figs. 3.1 and 3.2) | The script that drew the figures, and the record of the figure values and checks | `E/E3/calc/calc1_2_scale_figures.py`, `E/E3/calc/calc1-v0.5/calc1-2-record-v0.5.md` |
| Model sections of Chapters 6 and 8 (figures, and tables for models with two or fewer cells) | The script that built the figures and tables, and the record of checks | `E/E3/calc/calc3_model_figures.py`, `E/E3/calc/calc3-v0.5/calc3-record.md` |
| Sections 6.12 and 8.8 (tables of the number of models per comparison) | The script that counted the tables, and the json files of the counted values and checks | `E/E3/calc/typecount_D.py`, `E/E3/calc/typecount-v0.1/ja/typecount-ja.json`, `E/E3/calc/typecount-v0.1/en/typecount-en.json` |
