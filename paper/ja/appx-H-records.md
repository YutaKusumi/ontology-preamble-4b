# 付録 H 記録の置き場と SHA

この付録は五つの節を置く。H.1 は公開の置き場で git が追っている主な記録の、HEAD の中身で数えた SHA-256 と、最後に替えたコミットである。H.2 は、二つの登録の実行の前の SHA の記録に刻んだ SHA-256 と、公開の置き場の HEAD の中身の照らしと、較正の決まりの刻印の照らしである。凍結の本文そのものは結果の公開のときに初めてコミットしたので、刻んだ値と同じことを外から確かめられるのは、H.2 で「同じ」か「改行を LF にそろえた値で同じ」の行だけである（日本語の送る文の登録は刻んだ 43 項のうち 10、英語の送る文の登録は 111 項のうち 36・「違う」の行は無い）。照らせない主な物は、伏せた記録・較正の決まりの刻印のファイル（日本語の送る文の登録の分）・日本語の送る文の登録の予想・判定ラベルを付けた二つの集計のスクリプト（内部・公開の形は H.3）と設定である。判定ラベルは、公開の集計の出力の数から、計算の再現のスクリプトで組み直せる（節 11.3）。凍結の本文・前置きと場面の素材・採点のスクリプト・二つの実行のスクリプトは、照らせる行に入る。名を含む三つのファイルは公開しておらず、公開するときは名を伏せた写しになり、刻んだ SHA と合わない（節 2.6）。H.3 は、論文が差し込みの出所に使い、本文が名を挙げるか番号で指す内部の記録とスクリプトの在りかと公開の予定で、同じ中身のファイルが公開の置き場にあれば「公開済み」と書く。H.4 は、本文の章（要旨〜章 10）の引用と図と表の出所（ファイル・行・SHA16）を章ごとに置く。H.5 は、本文の章が番号や道を書かずに指す決定の記録とスクリプトの対応である。

## H.1 公開の置き場の記録

〔表の差し込みの始まり〕出所 〈内部〉`E/E3/calc/records-v0.8/records-sha-E3-v0.8.md`（SHA16 545E3C27F5AEA86A）。ここから下は、起草者のスクリプトが記録から組んだ表で、言葉は論文の言葉である（組み方と読んだ記録は、出所のファイルの頭と、その組み立ての記録にある）。

### 記録の置き場と SHA（公開の置き場・HEAD afeb5a0 の中身で数えた・2026-10-17 06:33:43 日本時間・スクリプト `E/E3/calc/records_sha_E3_v08.py` v0.8）

#### 段階 D・日本語の送る文の登録（D1′）

| ファイル | SHA-256（HEAD の中身） | 最後に替えたコミット |
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

#### 段階 D・英語の送る文の登録（D1′E）

| ファイル | SHA-256（HEAD の中身） | 最後に替えたコミット |
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

#### 段階 D の素材と採点のスクリプト

| ファイル | SHA-256（HEAD の中身） | 最後に替えたコミット |
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

#### 段階 E

| ファイル | SHA-256（HEAD の中身） | 最後に替えたコミット |
|---|---|---|
| `records/E/preopen-sha256-E2.txt` | 2C61A83ED7AC1E1549934FE5885ACC55956DADBE84313076B4E7A0898608DEE9 | 6ae0015 2026-10-14 |
| `records/E/reading-judgments-sha256-E2.txt` | 7732A786A71633659EDC015DE422D15B12DAE43671745DB3F0B5DFEC92E3891B | 8ed53f8 2026-10-14 |
| `records/E/stamp-frame-E-addendum1.md` | 20F9354FFBAB65BB5AA139375C32D61CE3AE7E7AA6CC8F365AFFAA81D6580013 | 4c1d90a 2026-10-14 |
| `records/E/stamp-frame-E-addendum2.md` | F8453C55868CDE528B7A9F6CA93888D9DE79F52F49EC94CA0FB17C3B83234AF9 | afeb5a0 2026-10-14 |
| `records/E/stamp-frame-E1.md` | 7557BB6C826B9E6DCE89679DF3A0B0040D141398FD02572DB8666532E37FE6E1 | 5876c82 2026-10-14 |

#### 前の段の凍結の設計と最終版と中間総括

| ファイル | SHA-256（HEAD の中身） | 最後に替えたコミット |
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

- 公開の置き場で git が追っているファイルだけを数えた（107）。伏せた記録（記録では「封の台帳」）など公開していない記録は、この表に無い。伏せた記録の名と SHA は、二つの登録の公開の閉じの記録の目録（`records/D1p/closing/inventory-D1p.json`・`records/D1pE/closing/inventory-D1pE.json`）にある。日本語の送る文の登録の名を含む三つのファイル（凍結した本文の 243 行）は公開しておらず、公開するときは名を伏せた写しになり、刻んだ SHA と合わない（節 2.6）。内部の記録の在りかは H.3 にある。


〔表の差し込みの終わり〕出所のファイルを差し込んだ。引用の禁止の一文（行の頭が「本記録のいかなる数値も」「本票のいかなる数値も」「本表のいかなる数値も」の行で、行の頭の「>」を含む）を 1 行除いた。うち引用の形の行は 0。除いた行の在りかは 見出し「前の段の凍結の設計と最終版と中間総括」の下。除いた後に同じ一文で始まる行は残っていない（スクリプトが照らした）。見出しを 2 段下げた。足した印は無い。ほかの字は替えていない。

## H.2 実行の前に約束した SHA と、公開の置き場の HEAD の照らし

〔表の差し込みの始まり〕出所 〈内部〉`E/E3/calc/records-v0.8/seal-check-E3-v0.8.md`（SHA16 10C96A624D7676CF）。ここから下は、起草者のスクリプトが記録から組んだ表で、言葉は論文の言葉である（組み方と読んだ記録は、出所のファイルの頭と、その組み立ての記録にある）。

### 実行の前に約束した SHA と、公開の置き場の HEAD の照らし（HEAD afeb5a0・2026-10-17 06:33:43 日本時間・スクリプト `E/E3/calc/records_sha_E3_v08.py` v0.8）

- 読み方: 「刻んだ値」は、実行の前の SHA の記録（記録では「封の記録」・公開の置き場で、実行の前に push したファイル）の三つの節（SHA-256・刻印の本文・改行を LF にそろえた表）の値。「HEAD の値」は、同じ名の公開のファイルの、いまの HEAD の中身の SHA-256。照らしは、同じ・改行を LF にそろえた値で同じ（刻んだ手元のバイトは CRLF を含む）・違う・公開の置き場に無い、のどれか。名が置き場でない行（目録の項の名など）は、記録の名の字と値だけを写す。名を含む三つのファイルは公開しておらず（名を伏せた写しもまだ公開していない）、この表では「公開の置き場に無い」の行に入る。

#### 日本語の送る文の登録（D1′）

- 実行の前の SHA の記録: `records/D1p/prerun-seal-D1p.md`（最初に足したコミット 806c87e 2026-10-10・最後に替えたコミット 806c87e 2026-10-10）。

| 節 | 刻んだ名 | 刻んだ値 | 改行を LF にそろえた表の値 | 公開のファイル | HEAD の値 | 照らし |
|---|---|---|---|---|---|---|
| SHA-256 | `D1p/frame-stamp-D1p.md` | 050CDCD48CC4CA7B | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/predictions-D1p.md` | B64FDF01AD4055F7 | — | — | — | 公開の置き場に無い |
| SHA-256 | 移した較正の記録の目録（一）・json | D378C8C1E2C0E9A9 | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | 移した較正の記録の目録（一）・md | 896994529D1E7779 | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | 移した較正の記録の目録（二）・json | 7FBC6B82D8A9CD99 | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | 移した較正の記録の目録（二）・md | 48D559FD924B308A | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | 移した較正の記録の目録（三）・json | DFDFE2222BF3946B | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | 移した較正の記録の目録（三）・md | DB3328FA3FA83391 | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | `D1p/d0-sealed-inventory-D1p.json` | 98C6E7F0D8F5FAF1 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/endcheck-public-inventory-D1p.json` | 4B2D60A00F867673 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/probe-sealed-inventory-D1p.json` | 76FCC95B442E01C8 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/balance-declaration-D1p.md` | 23DDA9BF4E064550 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/pass-conditions-post-round3-D1p.md` | CAB05C776794EF1F | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/test_d1p_e2e.py` | D3245DD513B636E6 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/e2e-test-D1p.json` | C4FDBC6348A2EA3D | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/selfaudit-v04-D1p.json` | 064400D19DE513B1 | — | — | — | 公開の置き場に無い |
| SHA-256 | 機種ごとの露出の内部の記録 | AC28F82A16FD1C00 | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | 外した系統の内部の表 | 2F6F6DC88D7C8C13 | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | `D1p/policy-readings-D1p.md` | ED62B356F2BDE9B3 | — | — | — | 公開の置き場に無い |
| SHA-256 | 機種ごとの露出の内部の記録・追記 | AB2E796CF99F4D9C | — | — | — | 名だけ（置き場の名ではない） |
| SHA-256 | `D1p/diff-draft3-to-frozen-D1p.md` | 3CDE04B61865399A | — | — | — | 公開の置き場に無い |
| 刻印の本文 | `tools/run_preamble_api_d.py` | A04D40B934392A47 | A04D40B934392A47 | `tools/run_preamble_api_d.py` | A04D40B934392A47 | 同じ |
| 刻印の本文 | `arms/panel/OAmi.md` | 94F1829E701FEB88 | 94F1829E701FEB88 | `arms/panel/OAmi.md` | 94F1829E701FEB88 | 同じ |
| 刻印の本文 | `arms/panel/SHA-LEDGER.json` | 5490F273BAD89EFF | 5490F273BAD89EFF | `arms/panel/SHA-LEDGER.json` | 5490F273BAD89EFF | 同じ |
| 刻印の本文 | `arms/frozen-from-ryokai-os/app-scenarios.json` | 796D73F2544956D7 | 7AD7E49459D5C402 | `arms/frozen-from-ryokai-os/app-scenarios.json` | 7AD7E49459D5C402 | 改行を LF にそろえた値で同じ |
| 刻印の本文 | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 56553F926272CF8A | 12EAA8B845BC0A2F | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 12EAA8B845BC0A2F | 改行を LF にそろえた値で同じ |
| 刻印の本文 | `arms/frozen-from-ryokai-os/armsE/preamble-O.md` | 18FBB2004ECF8858 | F3EE60C33F825575 | `arms/frozen-from-ryokai-os/armsE/preamble-O.md` | F3EE60C33F825575 | 改行を LF にそろえた値で同じ |
| 刻印の本文 | `arms/frozen-from-ryokai-os/armsE/preamble-Onull.md` | 464DF5DD72DF31D0 | 2123B3CD8586E7DF | `arms/frozen-from-ryokai-os/armsE/preamble-Onull.md` | 2123B3CD8586E7DF | 改行を LF にそろえた値で同じ |
| 刻印の本文 | `arms/materials-draft/hei/refuse-rules-v2.json` | 22625AEC81875362 | 22625AEC81875362 | `arms/materials-draft/hei/refuse-rules-v2.json` | 22625AEC81875362 | 同じ |
| 刻印の本文 | `arms/materials-draft/hei/incentive-lexicon-v2.json` | F3D7568C2FDA0BB7 | F3D7568C2FDA0BB7 | `arms/materials-draft/hei/incentive-lexicon-v2.json` | F3D7568C2FDA0BB7 | 同じ |
| 刻印の本文 | `D1p/d1p_config.py` | 2735FE8FDF9B802E | 2735FE8FDF9B802E | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/d1p_anchor.py` | 87F31505ACB5D97F | 87F31505ACB5D97F | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/d1p_run.py` | 171884E23985D423 | 171884E23985D423 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/d1p_close.py` | FAA625B8276824AB | FAA625B8276824AB | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/d1p_confirm.py` | 3E92994DF6ADBE0F | 3E92994DF6ADBE0F | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/extract_sealed_access_log_D1p.py` | 486DF76A4924FDC0 | 486DF76A4924FDC0 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/make_prerun_seal_D1p.py` | 2AE026AF2DFCEEAF | 2AE026AF2DFCEEAF | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/reference-D1p.json` | A95A2E02EAC2E43A | A95A2E02EAC2E43A | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/main-cost-by-model-D1p.json` | F8716B47EAA66D97 | F8716B47EAA66D97 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | 40BF3C3663BA8C69 | `records/D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | 同じ |
| 刻印の本文 | `D0/d0_config.py` | 0A5722552CC2255D | 0A5722552CC2255D | — | — | 公開の置き場に無い |
| 刻印の本文 | `D0/models-D0w3.json` | F4391EA8C403F947 | F4391EA8C403F947 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/moved-records-paths-D1p.json` | CCF416A5B9E89369 | CCF416A5B9E89369 | — | — | 公開の置き場に無い |

- 照らしの数: 同じ 6・改行を LF にそろえた値で同じ 4・違う 0・公開の置き場に無い 24・名だけ（置き場の名ではない） 9（合わせて 43・照らせる行は「同じ」と「改行を LF にそろえた値で同じ」の 10）。

#### 英語の送る文の登録（D1′E）

- 実行の前の SHA の記録: `records/D1pE/prerun-seal-D1pE.md`（最初に足したコミット 169af45 2026-10-12・最後に替えたコミット 169af45 2026-10-12）。

| 節 | 刻んだ名 | 刻んだ値 | 改行を LF にそろえた表の値 | 公開のファイル | HEAD の値 | 照らし |
|---|---|---|---|---|---|---|
| SHA-256 | `D1pE/frame-stamp-D1pE.md` | 1462926671AE1409 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/predictions-D1pE.md` | DAAD741AB038BD9B | — | `records/D1pE/predictions-D1pE.md` | DAAD741AB038BD9B | 同じ |
| SHA-256 | `D1pE/endcheck-sealed-inventory-D1pE.json` | 605C2F3C0ABFF3EF | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/endcheck-public-inventory-D1pE.json` | 1ED29FC5103148C4 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/probe-sealed-inventory-D1pE.json` | C6B8BDA6AE01CBC0 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/balance-declaration-D1pE.md` | 4E85A7C5259F09A2 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/test_d1pe_e2e.py` | C8B8BF8CF21E9C11 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/e2e-test-D1pE.json` | C103852B432610D7 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/frame-stamp-D1pE-cal.md` | 2155B5EAD23585A0 | — | `records/D1pE/calibration/frame-stamp-D1pE-cal.md` | 2155B5EAD23585A0 | 同じ |
| SHA-256 | `D1pE/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | — | `records/D1pE/calibration/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | 同じ |
| SHA-256 | `D1pE/summary-D1pE-cal.md` | 6FA0D549C224A12B | — | `records/D1pE/calibration/summary-D1pE-cal.md` | 6FA0D549C224A12B | 同じ |
| SHA-256 | `D1pE/stage-note-D1pE-cal.md` | EA34173BF80DDA6D | — | `records/D1pE/calibration/stage-note-D1pE-cal.md` | EA34173BF80DDA6D | 同じ |
| SHA-256 | `D1pE/materials-build-D1pE.md` | 14CF8C1D229E651F | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/translation/final/freeze-xlate-D1pE.md` | 593054E132FD1F89 | — | `records/D1pE/translation/freeze-xlate-D1pE.md` | 593054E132FD1F89 | 同じ |
| SHA-256 | `D1pE/availability-check-D1pE.md` | 32F77BB2B58EB905 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/availability-check-D1pE-addendum.md` | EE395330057E93E8 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1p/policy-readings-D1p.md` | ED62B356F2BDE9B3 | — | — | — | 公開の置き場に無い |
| SHA-256 | `plans/policy-readings-cold-arm-2026-10-11.md` | 99E909958B1961DD | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/reading-raw-inventory-D1pE.json` | 81F5A4D9BB6EEC06 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/summary-D1pE-cal.json` | 2D02DB2C34A213B3 | — | `records/D1pE/calibration/summary-D1pE-cal.json` | 2D02DB2C34A213B3 | 同じ |
| SHA-256 | `D1pE/reference-D1pE.json` | FC0A5DFBA6761E91 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/reading-rule-B-D1pE.json` | 98BC85BF929A1000 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/tools-log-D1pE-cal.md` | B7B7F7A4C6B6A5C4 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/tools-log-D1pE-main.md` | 4D90EB9DB5E138BC | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/incident-safegrep-reading-raw-2026-10-12.md` | 0D374CFCE8A9A1E4 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-a-v0.json` | D710A6914F9AC5E9 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/balance-line-D1pE.json` | 500D54D6E1E0495A | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/balance-line-D1pE.md` | 25A036BE15537255 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/reading/summary-deepseekflash.json` | 9A5BA59F51B8DFAE | — | `records/D1pE/calibration/reading/summary-deepseekflash.json` | 9A5BA59F51B8DFAE | 同じ |
| SHA-256 | `D1pE/describe-D1pEc-deepseekflash.json` | ECE96623E11C8D21 | — | `records/D1pE/calibration/describe-D1pEc-deepseekflash.json` | ECE96623E11C8D21 | 同じ |
| SHA-256 | `D1pE/endcheck-decision-deepseekflash.json` | E1D69BF57418C313 | — | `records/D1pE/calibration/endcheck-decision-deepseekflash.json` | E1D69BF57418C313 | 同じ |
| SHA-256 | `D1pE/reading/summary-gemini25flash.json` | DB58939E96447E37 | — | `records/D1pE/calibration/reading/summary-gemini25flash.json` | DB58939E96447E37 | 同じ |
| SHA-256 | `D1pE/describe-D1pEc-gemini25flash.json` | 77A7568C55EECF54 | — | `records/D1pE/calibration/describe-D1pEc-gemini25flash.json` | 77A7568C55EECF54 | 同じ |
| SHA-256 | `D1pE/endcheck-decision-gemini25flash.json` | 886A1FB27ACC0C15 | — | `records/D1pE/calibration/endcheck-decision-gemini25flash.json` | 886A1FB27ACC0C15 | 同じ |
| SHA-256 | `D1pE/reading/summary-grok420nr.json` | 3ABC6E092097CD88 | — | `records/D1pE/calibration/reading/summary-grok420nr.json` | 3ABC6E092097CD88 | 同じ |
| SHA-256 | `D1pE/describe-D1pEc-grok420nr.json` | B9FCB0C9B44AC0AB | — | `records/D1pE/calibration/describe-D1pEc-grok420nr.json` | B9FCB0C9B44AC0AB | 同じ |
| SHA-256 | `D1pE/endcheck-decision-grok420nr.json` | 1A2E27CD46001A7F | — | `records/D1pE/calibration/endcheck-decision-grok420nr.json` | 1A2E27CD46001A7F | 同じ |
| SHA-256 | `D1pE/reading/summary-kimik3-m.json` | 7C2BCE049AC9726C | — | `records/D1pE/calibration/reading/summary-kimik3-m.json` | 7C2BCE049AC9726C | 同じ |
| SHA-256 | `D1pE/describe-D1pEc-kimik3-m.json` | 32DC45D94835F1E0 | — | `records/D1pE/calibration/describe-D1pEc-kimik3-m.json` | 32DC45D94835F1E0 | 同じ |
| SHA-256 | `D1pE/endcheck-decision-kimik3-m.json` | 240899714E91FDC2 | — | `records/D1pE/calibration/endcheck-decision-kimik3-m.json` | 240899714E91FDC2 | 同じ |
| SHA-256 | `D1pE/reading/summary-llama4scout.json` | EDA5BC83C9BCCA59 | — | `records/D1pE/calibration/reading/summary-llama4scout.json` | EDA5BC83C9BCCA59 | 同じ |
| SHA-256 | `D1pE/describe-D1pEc-llama4scout.json` | 5839C54E2A33CAAB | — | `records/D1pE/calibration/describe-D1pEc-llama4scout.json` | 5839C54E2A33CAAB | 同じ |
| SHA-256 | `D1pE/endcheck-decision-llama4scout.json` | 75373F4D97467121 | — | `records/D1pE/calibration/endcheck-decision-llama4scout.json` | 75373F4D97467121 | 同じ |
| SHA-256 | `D1pE/reading/summary-mistrallarge3-m.json` | F599E5B87656EB6A | — | `records/D1pE/calibration/reading/summary-mistrallarge3-m.json` | F599E5B87656EB6A | 同じ |
| SHA-256 | `D1pE/describe-D1pEc-mistrallarge3-m.json` | 5DD2AA5EF7F5FF42 | — | `records/D1pE/calibration/describe-D1pEc-mistrallarge3-m.json` | 5DD2AA5EF7F5FF42 | 同じ |
| SHA-256 | `D1pE/endcheck-decision-mistrallarge3-m.json` | C93EB9C5DE97B33D | — | `records/D1pE/calibration/endcheck-decision-mistrallarge3-m.json` | C93EB9C5DE97B33D | 同じ |
| SHA-256 | `D1pE/incident-safegrep-reading-raw-2026-10-12-addendum.md` | 6B5026A73A44BAFE | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/tools-log-D1pE-main-v01.md` | F9F0E9EF5D95EE06 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/tools-log-D1pE-main-v02.md` | 05106E73B555796C | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/terms-check-moonshot-D1pE.md` | 8D90710EB1F246A2 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/reading-names-D1pE.md` | 758CFD42D03DFE39 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/reading-names-D1pE.json` | 9CA7BB5B0B263C06 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/reading-names-D1pE-addendum.md` | 59C4F0A240169574 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r1/sealed-access-log-D1pE.json` | D4CE51FBAF66DA37 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r1/sealed-access-log-D1pE.md` | 3E9F141AC315FF78 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r1/review-selfaudit-r1.md` | 1B53770C5375D11E | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r2/sealed-access-log-D1pE.json` | D118E8BDF9AE0E54 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r2/sealed-access-log-D1pE.md` | 3E7D00C670E58B81 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r2/review-selfaudit-r2.md` | 4B3A27FE7CA43554 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-a-v0.md` | 89A18F1662FDF607 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/power-D1pE-v0.json` | 920B0EC4B01FAAA2 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/sim-style-shift-D1pE-v0.json` | F5B838F999BE2518 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/test-d1pe-deepseek-page-v0.json` | 79BA6B934ECD0CF1 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/balance_line_D1pE.py` | 23BCB5F39B2BF01C | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/check_memory_values_D1pE.py` | DE957E2ACBFF2F9D | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/00-frame-D1pE-cal.md` | 5C21615162C7B43D | — | `records/D1pE/calibration/00-frame-D1pE-cal.md` | 5C21615162C7B43D | 同じ |
| SHA-256 | `D1pE/predictions-check-D1pE-cal.md` | 95276D65FDD159B5 | — | `records/D1pE/calibration/predictions-check-D1pE-cal.md` | 95276D65FDD159B5 | 同じ |
| SHA-256 | `D1pE/reference-text-check-D1pE.md` | 6DD21BFC81A3111D | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r3/sealed-access-log-D1pE.json` | 6B6C62AAA30A79A8 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r3/sealed-access-log-D1pE.md` | 6BCF22F4DB6E2E39 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/selfaudit-r3/review-selfaudit-r3.md` | 3CC6CBC189BFD666 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-b-v0.1.json` | 0CD139C005ACFAEA | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/probe-prompt-tokens-D1pE-direct-b-v0.1.md` | EBB6FE1831030A57 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/memory-check-D1pE.json` | 46B81FE8DBE27B5C | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/test-d1pe-units-final.json` | 4CD1CDE8D1A50B4A | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/test-d1pe-dry-paths-final.json` | 15DCB039EFF24A55 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/scan-names-D1pE-freeze.json` | 258574DEF774CEB4 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/scan-maker-words-D1pE-freeze.json` | E0595A3548B17D01 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/diff-final-draft-to-frozen-D1pE.md` | B6FBA677D893F58E | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/test-d1pe-confirm-names-final.json` | DADBFD4EB55788C9 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/test-d1pe-frame-cover-final.json` | C1373DFC15FAEC23 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/ratio-copies-inventory-D1pE-freeze.json` | 4EFBF1D02720AE7E | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/scan-banned-phrases-D1pE-freeze.json` | 723C80D8C89E18BC | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/tools-log-D1pE-main-v03.md` | E285163E78AECAA2 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/ratio-copies-inventory-D1pE.json` | 11F03FFFF791216F | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/ratio-copies-inventory-D1pE.md` | 9BDCA4D0383643E6 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/tools-log-D1pE-main-v04.md` | C1C8F88D6391F279 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/reference-text-check-D1pE-judgement.md` | DE5C9FEE8C2F2DE0 | — | — | — | 公開の置き場に無い |
| SHA-256 | `D1pE/terms-check-moonshot-D1pE-final.md` | 2ACB2FF1099670A9 | — | — | — | 公開の置き場に無い |
| 刻印の本文 | `tools/run_preamble_api_d1pe.py` | F09CC223F9AA4B4E | F09CC223F9AA4B4E | `tools/run_preamble_api_d1pe.py` | F09CC223F9AA4B4E | 同じ |
| 刻印の本文 | `arms/en-D1pE/OAmi-en.md` | 4147B0B24FA4C8F2 | 4147B0B24FA4C8F2 | `arms/en-D1pE/OAmi-en.md` | 4147B0B24FA4C8F2 | 同じ |
| 刻印の本文 | `arms/en-D1pE/preamble-O-en.md` | 815C11569DFB7A60 | 815C11569DFB7A60 | `arms/en-D1pE/preamble-O-en.md` | 815C11569DFB7A60 | 同じ |
| 刻印の本文 | `arms/en-D1pE/preamble-Onull-en.md` | EDF2BA377EC46444 | EDF2BA377EC46444 | `arms/en-D1pE/preamble-Onull-en.md` | EDF2BA377EC46444 | 同じ |
| 刻印の本文 | `arms/en-D1pE/app-scenarios-en.json` | CD343C3D344FF00C | CD343C3D344FF00C | `arms/en-D1pE/app-scenarios-en.json` | CD343C3D344FF00C | 同じ |
| 刻印の本文 | `arms/en-D1pE/MANIFEST-en.json` | 41407D45D02E1B8B | 41407D45D02E1B8B | `arms/en-D1pE/MANIFEST-en.json` | 41407D45D02E1B8B | 同じ |
| 刻印の本文 | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 56553F926272CF8A | 12EAA8B845BC0A2F | `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` | 12EAA8B845BC0A2F | 改行を LF にそろえた値で同じ |
| 刻印の本文 | `D1pE/d1pe_main_config.py` | DFBC19D781535502 | DFBC19D781535502 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/d1pe_config.py` | 97E953ECCF52E18D | 97E953ECCF52E18D | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/d1pe_anchor.py` | 0E38A7B9CEE6F76A | 0E38A7B9CEE6F76A | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/d1pe_run.py` | A91BD15359BEE8A7 | A91BD15359BEE8A7 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/d1pe_close.py` | A3F9E16254A096F6 | A3F9E16254A096F6 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/d1pe_confirm.py` | F4094799DBEE9DCA | F4094799DBEE9DCA | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/extract_sealed_access_log_D1pE.py` | 3C83AF760FD45130 | 3C83AF760FD45130 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/make_prerun_seal_D1pE.py` | 57E1594111794D78 | 57E1594111794D78 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/reference-D1pE-main.json` | BE92C0365EB0C02E | BE92C0365EB0C02E | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/main-cost-by-model-D1pE.json` | B167507F7B9BA61F | B167507F7B9BA61F | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1pE/00-frame-D1pE.md` | F557603870509EA2 | F557603870509EA2 | `records/D1pE/00-frame-D1pE.md` | F557603870509EA2 | 同じ |
| 刻印の本文 | `D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | 40BF3C3663BA8C69 | `records/D1p/00-frame-D1p.md` | 40BF3C3663BA8C69 | 同じ |
| 刻印の本文 | `D0/d0_config.py` | 0A5722552CC2255D | 0A5722552CC2255D | — | — | 公開の置き場に無い |
| 刻印の本文 | `D0/models-D0w3.json` | F4391EA8C403F947 | F4391EA8C403F947 | — | — | 公開の置き場に無い |
| 刻印の本文 | `D1p/safe_grep_D1p.py` | 03FDAE36C8871044 | 03FDAE36C8871044 | — | — | 公開の置き場に無い |

- 照らしの数: 同じ 35・改行を LF にそろえた値で同じ 1・違う 0・公開の置き場に無い 75・名だけ（置き場の名ではない） 0（合わせて 111・照らせる行は「同じ」と「改行を LF にそろえた値で同じ」の 36）。

#### 較正の決まりの刻印（較正の前に内部で刻んだ・公開の置き場への写し）

- 刻印は、較正を走らせる前に内部の置き場で刻んだ記録で、較正の前には公開の置き場に置いていない（刻印の時刻は当事者の申告による）。公開の写しがあれば、公開の置き場に初めて置いたコミットを書く。日本語の送る文の較正は回ごとに刻んだ（一度目・二度目と、その一つの系統の追補・三度目）。

| 登録 | 刻印（内部の置き場） | 刻印の時刻（刻印の頭の字） | 刻んだ名 | 刻んだ値 | 公開の写し | HEAD の値 | 照らし | 公開の置き場に初めて置いたコミット |
|---|---|---|---|---|---|---|---|---|
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/00-frame-D1pE-cal.md` | 5C21615162C7B43D | `records/D1pE/calibration/00-frame-D1pE-cal.md` | 5C21615162C7B43D | 同じ | e549c2b 2026-10-13 |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_config.py` | 97E953ECCF52E18D | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_reading.py` | 546E2175457BBCD2 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_cal_run.py` | EE40E1A07AB3CD9E | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_cal_describe.py` | FA9FED3A32ADE777 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/d1pe_endcheck.py` | 3D6E2BB0A01DB24F | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/make_materials_D1pE.py` | B9CF1D79B3CF8A3C | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/make_runner_d1pe.py` | DBECC708B20DE2A5 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/make_stamp_D1pE_cal.py` | 0C60F005149B3A4F | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/reading-questions-D1pE.json` | 5BE5F5EDA02DCF9E | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/reading-rule-B-D1pE.json` | 98BC85BF929A1000 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/reference-D1pE.json` | FC0A5DFBA6761E91 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/materials-build-D1pE.md` | 14CF8C1D229E651F | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/tools-log-D1pE-cal.md` | B7B7F7A4C6B6A5C4 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/predictions-D1pE-cal-coordinator.md` | F72232E20B1361E6 | `records/D1pE/calibration/predictions-D1pE-cal-coordinator.md` | F72232E20B1361E6 | 同じ | e549c2b 2026-10-13 |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | `records/D1pE/calibration/predictions-seal-D1pE-cal.txt` | FA1A1AE1E1E4E667 | 同じ | e549c2b 2026-10-13 |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/availability-check-D1pE-prereg.md` | AC931613F6F1E873 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/availability-check-D1pE.md` | 32F77BB2B58EB905 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/availability-check-D1pE-addendum.md` | EE395330057E93E8 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/probe_dsv32_D1pE.py` | A313A562592B6CB9 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/probe-dsv32-D1pE.json` | 7EDF4DA264049C24 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1p/safe_grep_D1p.py` | 7091DA19C57FB6F2 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D0/d0_config.py` | 0A5722552CC2255D | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/translation/final/freeze-xlate-D1pE.md` | 593054E132FD1F89 | `records/D1pE/translation/freeze-xlate-D1pE.md` | 593054E132FD1F89 | 同じ | e549c2b 2026-10-13 |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `D1pE/translation/final/xlate-final-D1pE-v0.1.json` | C8A7CFB8942FEA33 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/plan-D1pE-reading-calibration-v0.md` | 2FB49DB29574B068 | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/rulings-D380-2026-10-11.md` | D5063F86D57D7DAE | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/rulings-D381-2026-10-11.md` | 6A3F03487FC072BF | — | — | 公開の置き場に無い | — |
| 英語 | `D1pE/frame-stamp-D1pE-cal.md` | 2026-10-11 21:01:12 | `plans/rulings-D382-2026-10-11.md` | BF3793870DD51DFA | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/00-frame-D0-2026-10-02.md` | 69C056EC192D6FEE | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/build_frame_D0.py` | 7802989D7D4E2B2C | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/d0_config.py` | 6569C4E8AB543834 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/d0_describe.py` | C6BEA77D26567C16 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0.md` | 2026-10-02 21:25:42 | `D0/d0_run.py` | 56E2267612304242 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/00-frame-D0w2-2026-10-03.md` | A692FB8E4E921991 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/build_frame_D0w2.py` | DFCE4AA0A2E2EC03 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `tools/run_preamble_api_d.py` | B0F6D8E721CF1AF5 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_config.py` | 6088CF8A96715751 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/models-D0w2.json` | 6D3A51F9DDC992BB | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_describe.py` | B6D94754B47BB0B2 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_reading.py` | FAA90E08C0BD8258 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/reading-questions-D0w2.json` | 026EDCD4BD5940B1 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_ocheck.py` | C7496F5FE87977AB | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_ocheck_describe.py` | 7C7DA3CD1005D39F | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/d0_run.py` | BBA332ADA5899B90 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/predictions-D0w2-coordinator.md` | 3F4B9387D79BF423 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2.md` | 2026-10-03 10:25:32 | `D0/predictions-seal-D0w2.txt` | 5DBEFD7F9DDBFF5F | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/00-frame-D0w2-〔系統の名〕-2026-10-03.md` | 1DB0FF3FBFB453B5 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/build_frame_D0w2_〔系統の名〕.py` | 8E5B22665E08D29B | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/models-D0w2-〔系統の名〕.json` | 5CD8A3B9C48B15C7 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/openrouter-probe-D0-6c.json` | 56AD06A25DC66DDB | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/predictions-D0w2-〔系統の名〕-coordinator.md` | 52AA3458C4AF2659 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w2-〔系統の名〕.md` | 2026-10-03 11:43:34 | `D0/predictions-seal-D0w2-〔系統の名〕.txt` | F94B118107893F55 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/00-frame-D0w3-2026-10-09.md` | 0A0E0BA75B3FB204 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/build_frame_D0w3.py` | 0FDC17F397EDE2FC | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `tools/run_preamble_api_d.py` | A04D40B934392A47 | `tools/run_preamble_api_d.py` | A04D40B934392A47 | 同じ | 806c87e 2026-10-10 |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_config.py` | 0A5722552CC2255D | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/models-D0w3.json` | F4391EA8C403F947 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/build_models_D0w3.py` | D01A77D5F3E54D41 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_describe.py` | 25B13A53FB3BBFA7 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_reading.py` | 5B963BDDD9A9525F | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/reading-questions-D0w2.json` | 026EDCD4BD5940B1 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/reading-rescore-rule-D0-7.json` | 19D98D1B4148F455 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/reading_rescore_D0_7.py` | 50E7E35163AB9674 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_ocheck.py` | 15B8EECFE830CE6F | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_ocheck_describe.py` | 4E90DED06CB129D2 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/d0_run.py` | 108A448B73D8FE35 | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/predictions-D0w3-coordinator.md` | FF416C992790FCCB | — | — | 公開の置き場に無い | — |
| 日本語 | `D0/frame-stamp-D0w3.md` | 2026-10-09 12:36:29 | `D0/predictions-seal-D0w3.txt` | DEE19D93E168E50E | — | — | 公開の置き場に無い | — |

- 刻印の行の数: 英語 同じ 4・公開の置き場に無い 25／日本語 公開の置き場に無い 39・同じ 1。

- 値は SHA-256 の頭 16 字（全桁は実行の前の SHA の記録と付録 H の一つ目の表）。二つの登録の表に「違う」の行は無い（違う 0）。
- 名を伏せた行: ファイルの名に、集約の経路を経由して較正した系統の名を含む内部のファイルは、その名を〔系統の名〕と伏せて書く（決定 D325・D341-5・SHA16 は名を伏せる前のファイルの値）。


〔表の差し込みの終わり〕出所のファイルを差し込んだ。引用の禁止の一文（行の頭が「本記録のいかなる数値も」「本票のいかなる数値も」「本表のいかなる数値も」の行で、行の頭の「>」を含む）を 1 行除いた。うち引用の形の行は 0。除いた行の在りかは 見出し「較正の決まりの刻印（較正の前に内部で刻んだ・公開の置き場への写し）」の下。除いた後に同じ一文で始まる行は残っていない（スクリプトが照らした）。見出しを 2 段下げた。足した印は無い。ほかの字は替えていない。

## H.3 論文が名を挙げる内部の記録とスクリプト

〔表の差し込みの始まり〕出所 〈内部〉`E/E3/calc/records-v0.8/internal-sources-E3-v0.8.md`（SHA16 C790CAE2EE7EEBB8）。ここから下は、起草者のスクリプトが記録から組んだ表で、言葉は論文の言葉である（組み方と読んだ記録は、出所のファイルの頭と、その組み立ての記録にある）。

### 論文が名を挙げる内部の記録とスクリプトの在りか（2026-10-17 06:33:43 日本時間・スクリプト `E/E3/calc/records_sha_E3_v08.py` v0.8）

- 何か: 論文の原稿の差し込みの出所に使った内部の記録と、本文が名を挙げるか番号で指す内部のファイル（スクリプトと決定の記録を含む）。内部の置き場は公開していない。SHA-256 の頭 16 字とバイト数は、この表を組んだ時の値。同じ中身のファイルが公開の置き場の HEAD にあれば（git の中身の名で照らした）、「公開済み」と書く。拾う決まり: 原稿の差し込みの出所、原稿の字が「`」で囲む内部の道、原稿の字と引用の差し込みが引く記録の行の字に出る決定の番号（D と三桁）と内部の道、原稿の字が名を挙げずに指す記録（表の「原稿の字が指す」の行）。

| 内部の置き場 | SHA-256（頭 16 字） | バイト | 公開の予定 | 名を挙げる原稿 |
|---|---|---|---|---|
| `D0/00-frame-D0-2026-10-02.md` | 69C056EC192D6FEE | 11422 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・日本語の送る文の較正の一度目の回の枠（付録 H.2・本番の実行の四機種の較正の決め）） |
| `D0/00-frame-D0w2-2026-10-03.md` | A692FB8E4E921991 | 22588 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・日本語の送る文の較正の二度目の回の枠（付録 H.2・集約の経路の機種の名を含む）） |
| `D0/00-frame-D0w2-〔系統の名〕-2026-10-03.md` | 1DB0FF3FBFB453B5 | 7660 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・日本語の送る文の較正の二度目の回の枠の追補（ある系統・付録 H.2）） |
| `D0/00-frame-D0w3-2026-10-09.md` | 0A0E0BA75B3FB204 | 28352 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | 05-stageD-methods（引用の中）・（原稿の字が指す・日本語の送る文の較正の三度目の回の枠（付録 H.2）） |
| `D0/d0_config.py` | 0A5722552CC2255D | 17129 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | 05-stageD-methods（引用の中） |
| `D0/describe-D0-add-qwen25coder32b-n.md` | AB6401C8D65A7BE9 | 2421 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | 05-stageD-methods（引用の中） |
| `D0/frame-stamp-D0.md` | 16411E351880D511 | 1536 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・日本語の送る文の較正の一度目の回の枠の刻印（付録 H.2・本番の実行の四機種の較正の決め）） |
| `D0/frame-stamp-D0w2-〔系統の名〕.md` | 7178E352B3C0CAB1 | 2037 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・日本語の送る文の較正の二度目の回の枠の追補（ある系統）の刻印（付録 H.2）） |
| `D0/frame-stamp-D0w2.md` | 591C3910085014D1 | 3581 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・日本語の送る文の較正の二度目の回の枠の刻印（付録 H.2）） |
| `D0/frame-stamp-D0w3.md` | E0E743D76A6E2650 | 3369 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・日本語の送る文の較正の三度目の回の枠の刻印（付録 H.2）） |
| `D0/models-D0w3.json` | F4391EA8C403F947 | 16377 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | 05-stageD-methods（引用の中） |
| `D0/policy-readings-D0w3-2026-10-09.md` | 1CA95E1AB9974191 | 21458 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | 05-stageD-methods（引用の中） |
| `D0/probe-direct-D0w3.json` | 2FBE3777AE3DF4CB | 25179 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | 05-stageD-methods（引用の中） |
| `D0/summary-D0-calibration-2026-10-03-v0.1.md` | 50DBE46CD0D4EDBE | 11005 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・較正の段の一度目と二度目の回のまとめ（付録 D-ja.4 の表の元・付録 E.4）） |
| `D0/summary-D0w3-2026-10-09.md` | 8DA383408D264937 | 12385 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・較正の段のまとめ（付録 D-ja.4 の表の元・付録 E.4）） |
| `D0/summary-D0w3-addendum-2026-10-09.md` | A99165FA642088B7 | 5662 | 公開の形を E6 の前に決める（段階 E の枠 §10・集約の経路を経由した機種の名と記録と、許諾で外した機種の記録を出さない・決定 D457-1） | （原稿の字が指す・較正の段のまとめの追補（付録 D-ja.4 の表の元・付録 E.4）） |
| `D1p/balance-declaration-D1p.md` | 23DDA9BF4E064550 | 15072 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1p/d1p_confirm.py` | 3E92994DF6ADBE0F | 61569 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-H-records |
| `D1p/deviation-D1p-1.md` | 25B81707F3901D80 | 5667 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `D1p/deviation-D1p-2.md` | D135AC5758FBA5A0 | 6499 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `D1p/deviation-D1p-3.md` | 96534C6E4F3ABFC1 | 13607 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `D1p/deviation-D1p-4.md` | 89F55CEAF91814E7 | 6574 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `D1p/main-cost-by-model-D1p.json` | F8716B47EAA66D97 | 234 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1p/main-cost-estimate-D1p.md` | 90ADE13D84F990DF | 4508 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1p/policy-readings-D1p.md` | ED62B356F2BDE9B3 | 15909 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1p/power-D1p-v0.json` | 818FBD1D8B8D6B5C | 6617 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・appx-I-rules（引用の中） |
| `D1p/power_D1p.py` | 684FF4D7799FD3AA | 5384 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・appx-I-rules（引用の中） |
| `D1p/predictions-D1p.md` | B64FDF01AD4055F7 | 30252 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-ja |
| `D1p/predictions-check-D1p.md` | BDD536C5FC976EDD | 20235 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-ja |
| `D1p/provider-logging-check-D1p.md` | 265B08646BE5B93C | 8244 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1p/reference-D1p.json` | A95A2E02EAC2E43A | 22951 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 02-methods（引用の中）・05-stageD-methods（引用の中）・appx-A-preambles（引用の中） |
| `D1p/sim-style-shift-D1p-v0.json` | 40AA71404336CF58 | 6136 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 02-methods（引用の中）・appx-I-rules（引用の中） |
| `D1p/sim_style_shift_D1p.py` | 7B648483109F9C2E | 6480 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 02-methods（引用の中）・appx-I-rules（引用の中） |
| `D1p/sweep-promises-D1p-status.md` | 92B4995C78159003 | 13706 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `D1p/test-d1p-deepseek-page-v0.json` | 8CEA39A54A9BDD05 | 1067 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/00-frame-D1pE-cal.md` | 5C21615162C7B43D | 19343 | 公開済み（公開の置き場の `records/D1pE/calibration/00-frame-D1pE-cal.md`・初めて置いたコミット e549c2b 2026-10-13） | 05-stageD-methods（引用の中）・07-english-materials（引用の中） |
| `D1pE/balance-declaration-D1pE.md` | 4E85A7C5259F09A2 | 8221 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/balance-line-D1pE.json` | 500D54D6E1E0495A | 1992 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/balance-line-D1pE.md` | 25A036BE15537255 | 2322 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/balance_line_D1pE.py` | 23BCB5F39B2BF01C | 6815 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/check_predictions_D1pE.py` | F391555F8B3521CC | 21294 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-en（引用の中） |
| `D1pE/confirm-D1pE-pushed.txt` | EB084593D18923BA | 2124 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 08-results-en（引用の中）・appx-E-deviations（引用の中） |
| `D1pE/d1pe_confirm.py` | F4094799DBEE9DCA | 73325 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-H-records |
| `D1pE/describe-D1pEc-<鍵>.json` | — | — | 内部の置き場に無いか、置き場の名（ファイルでない） | 08-results-en（引用の中） |
| `D1pE/deviation-D1pE-*` | — | — | 内部の置き場に無いか、置き場の名（ファイルでない） | appx-E-deviations（引用の中） |
| `D1pE/deviation-D1pE-2.md` | 4553F3761F92C554 | 3848 | 公開済み（公開の置き場の `records/D1pE/deviation-D1pE-2.md`・初めて置いたコミット e549c2b 2026-10-13） | appx-E-deviations（引用の中） |
| `D1pE/drive-log-D1pE-launch-first.txt` | 4E28D311C35B3030 | 233 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/estimate_main_cost_D1pE.py` | B411965AED9FE0BB | 6654 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/frame-stamp-D1pE-cal.md` | 2155B5EAD23585A0 | 4398 | 公開済み（公開の置き場の `records/D1pE/calibration/frame-stamp-D1pE-cal.md`・初めて置いたコミット e549c2b 2026-10-13） | （原稿の字が指す・英語の送る文の較正の枠の刻印（付録 H.2）） |
| `D1pE/main-cost-estimate-D1pE.md` | 0C2BCBA11DCEBC98 | 3303 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/power-D1pE-v0.json` | 920B0EC4B01FAAA2 | 3262 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・appx-I-rules（引用の中） |
| `D1pE/power_D1pE.py` | 8D5E90D38658505F | 5429 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・appx-I-rules（引用の中） |
| `D1pE/predictions-D1pE.md` | DAAD741AB038BD9B | 24624 | 公開済み（公開の置き場の `records/D1pE/predictions-D1pE.md`・初めて置いたコミット e549c2b 2026-10-13） | appx-D-en（引用の中） |
| `D1pE/reference-D1pE-main.json` | BE92C0365EB0C02E | 6214 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/sim-style-shift-D1pE-v0.json` | F5B838F999BE2518 | 4980 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-I-rules（引用の中） |
| `D1pE/sim_style_shift_D1pE.py` | 0409A75340BEA878 | 7500 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-I-rules（引用の中） |
| `D1pE/terms-check-moonshot-D1pE.md` | 8D90710EB1F246A2 | 3418 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `D1pE/test-d1pe-deepseek-page-v0.json` | 79BA6B934ECD0CF1 | 1067 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `E/00-frame-E-addendum1-2026-10-14.md` | 352BD92D21B3D14D | 21434 | 刻んだバイトのまま公開する（遅くとも E6・段階 E の枠と二つの追記） | （原稿の字が指す・段階 E の枠の追記一の本文（付録 E.3）） |
| `E/00-frame-E-addendum2-2026-10-14.md` | 2A870ED3141A92CC | 7168 | 刻んだバイトのまま公開する（遅くとも E6・段階 E の枠と二つの追記） | appx-F-terms |
| `E/00-frame-E-draft6.md` | AB7491FF30074FBD | 118210 | 刻んだバイトのまま公開する（遅くとも E6・段階 E の枠と二つの追記） | 00-abstract・02-methods・03-4b-and-scale・06-results-ja・08-results-en・09-alternatives-limits・11-data-and-code・13-coi・appx-F-terms |
| `E/E2/deviation-E2-1.md` | E79E29DCD2F31EC7 | 6029 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations |
| `E/E2/deviation-E2-2.md` | C29EF9529350D929 | 5531 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations |
| `E/E2/record/E2-record-en.md` | 72E2C99C3CCEC0A7 | 49547 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-en |
| `E/E2/record/E2-record-ja.md` | 171F869D6CFF687E | 101503 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 06-results-ja・appx-D-ja |
| `E/E3/ai-use/ai-use-appendix-E3-v0.2.md` | 3D81499B49D74D1C | 39871 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-G-ai-use |
| `E/E3/availability/availability-table-E3-pw2.md` | DD0746D79FFD5941 | 2716 | 論文の図と表として、論文とともに公開する（E6） | 11-data-and-code |
| `E/E3/calc/calc1-v0.5/calc1-2-record-v0.5.md` | 652F65EEF71359D9 | 2303 | 論文の図と表として、論文とともに公開する（E6） | 03-4b-and-scale・appx-H-records |
| `E/E3/calc/calc1-v0.5/fig-calc1-stageA-v0.5.png` | 9FA05EF4680FAC0F | 402853 | 論文の図と表として、論文とともに公開する（E6） | 03-4b-and-scale |
| `E/E3/calc/calc1_2_scale_figures.py` | 779DBD9FBB730C50 | 21546 | 論文の図と表として、論文とともに公開する（E6） | appx-H-records |
| `E/E3/calc/calc2-v0.5/fig-calc2-pilotC-v0.5.png` | 6A5F28943B23B43C | 153412 | 論文の図と表として、論文とともに公開する（E6） | 03-4b-and-scale |
| `E/E3/calc/calc3-v0.5/calc3-record.md` | E832768E620C6876 | 4880 | 論文の図と表として、論文とともに公開する（E6） | appx-H-records |
| `E/E3/calc/calc3-v0.5/en/fig-kimik3-m.png` | 9589E4F01FB15CA7 | 160379 | 論文の図と表として、論文とともに公開する（E6） | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/fig-llama4scout.png` | 2DD6ABF6B9DA8072 | 161809 | 論文の図と表として、論文とともに公開する（E6） | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-deepseekflash.md` | 40767F8B4B67E1D2 | 2532 | 論文の図と表として、論文とともに公開する（E6） | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-gemini25flash.md` | 0DD062A2F22AD0DE | 1981 | 論文の図と表として、論文とともに公開する（E6） | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-grok420nr.md` | 5696D45D6F5B9165 | 2036 | 論文の図と表として、論文とともに公開する（E6） | 08-results-en |
| `E/E3/calc/calc3-v0.5/en/table-mistrallarge3-m.md` | 9FBD817EA7F4C883 | 2531 | 論文の図と表として、論文とともに公開する（E6） | 08-results-en |
| `E/E3/calc/calc3-v0.5/ja/fig-deepseekv32-a.png` | BFC81D62DCEE41A1 | 163004 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-gemini25flash.png` | AD9B28D613BCA84D | 160480 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-grok420nr.png` | E47C4A414FA7201D | 178851 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-kimik3-m.png` | A15E13807660397E | 161224 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-llama31-8b-n.png` | C8242D2887474786 | 182464 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-llama4scout.png` | EEDBF551F6E35C31 | 162470 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/fig-mistrallarge3-m.png` | 9A49E2012584306C | 161316 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/table-deepseekflash.md` | 091B3B429A9708EB | 2532 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/table-qwen25coder32b-n.md` | 6A291087A0509225 | 1969 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3-v0.5/ja/table-qwen38max-a.md` | 892967E8652521D6 | 2510 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/calc3_model_figures.py` | EEC38F08D1290D3A | 21102 | 論文の図と表として、論文とともに公開する（E6） | appx-H-records |
| `E/E3/calc/calc4-v0.2/cost-upper-en.md` | 2459DFE162F86DD1 | 3361 | 論文の図と表として、論文とともに公開する（E6） | 11-data-and-code |
| `E/E3/calc/calc4-v0.2/cost-upper-ja.md` | DECDF7E602BC4B97 | 5580 | 論文の図と表として、論文とともに公開する（E6） | 11-data-and-code |
| `E/E3/calc/calsum-v0.3/en/calsum-en.md` | 3EB67A64CB4EDAB2 | 10570 | 論文の図と表として、論文とともに公開する（E6） | appx-D-en |
| `E/E3/calc/calsum-v0.3/ja/calsum-ja.md` | 61EF4472CBF47F86 | 22049 | 論文の図と表として、論文とともに公開する（E6） | appx-D-ja |
| `E/E3/calc/calsum_D.py` | 19278F05A28436AB | 28793 | 論文の図と表として、論文とともに公開する（E6） | appx-D-en・appx-D-ja |
| `E/E3/calc/familytable/en/familytable-en-pw.md` | 304B38C27BBD0BCD | 6103 | 論文の図と表として、論文とともに公開する（E6） | appx-D-en |
| `E/E3/calc/familytable/ja/familytable-ja-pw.md` | E1C8463A0A8FF6BC | 13648 | 論文の図と表として、論文とともに公開する（E6） | appx-D-ja |
| `E/E3/calc/flow/flow-D.json` | ADF65FAD8A647024 | 5620 | 論文の図と表として、論文とともに公開する（E6） | 00-abstract・01-introduction・05-stageD-methods |
| `E/E3/calc/flow_D.py` | 68AF73A100F20C1C | 10080 | 論文の図と表として、論文とともに公開する（E6） | appx-H-records |
| `E/E3/calc/records-v0.8/internal-sources-E3-v0.8.md` | — | — | この表と同じスクリプトが書く物（SHA は書いた後に組み立ての記録に残す・論文の図と表として、論文とともに公開する〔E6〕） | appx-H-records |
| `E/E3/calc/records-v0.8/records-sha-E3-v0.8.md` | — | — | この表と同じスクリプトが書く物（SHA は書いた後に組み立ての記録に残す・論文の図と表として、論文とともに公開する〔E6〕） | appx-H-records |
| `E/E3/calc/records-v0.8/records-stats-E3-v0.8.json` | — | — | この表と同じスクリプトが書く物（SHA は書いた後に組み立ての記録に残す・論文の図と表として、論文とともに公開する〔E6〕） | appx-H-records |
| `E/E3/calc/records-v0.8/seal-check-E3-v0.8.md` | — | — | この表と同じスクリプトが書く物（SHA は書いた後に組み立ての記録に残す・論文の図と表として、論文とともに公開する〔E6〕） | appx-H-records |
| `E/E3/calc/typecount-v0.1/en/typecount-en.json` | E993C852FE746762 | 5044 | 論文の図と表として、論文とともに公開する（E6） | appx-H-records |
| `E/E3/calc/typecount-v0.1/en/typecount-en.md` | A337D724F058C8CA | 4134 | 論文の図と表として、論文とともに公開する（E6） | 08-results-en |
| `E/E3/calc/typecount-v0.1/ja/typecount-ja.json` | 4A24A0E464C17718 | 7354 | 論文の図と表として、論文とともに公開する（E6） | appx-H-records |
| `E/E3/calc/typecount-v0.1/ja/typecount-ja.md` | 141B0F157F4D2D3E | 4890 | 論文の図と表として、論文とともに公開する（E6） | 06-results-ja |
| `E/E3/calc/typecount_D.py` | E162FEF3890A0B90 | 10840 | 論文の図と表として、論文とともに公開する（E6） | appx-H-records |
| `E/deviation-E-1.md` | 860A734796CBE8FC | 4043 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations |
| `E/deviation-E-2.md` | 7394E2A9D88A1D71 | 3050 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations |
| `E/frame-E-addendum1-stamp.txt` | 97210C9177A9F40D | 3500 | 公開の形を E6 の前に決める（本文の SHA-256 だけを書いた刻印のファイルは公開済み・付録 E.3） | （原稿の字が指す・段階 E の枠の追記一の内部の刻印（付録 E.3）） |
| `E/frame-E-addendum2-stamp.txt` | 519BB608C48F9D18 | 2230 | 公開の形を E6 の前に決める（本文の SHA-256 だけを書いた刻印のファイルは公開済み・付録 E.3） | （原稿の字が指す・段階 E の枠の追記二の内部の刻印（付録 E.3）） |
| `E/refs/references-E3-v0.1.md` | 38130220CB391AD0 | 2495 | 論文の図と表として、論文とともに公開する（E6） | 12-references |
| `E/tool1/op4b_reproduce.py` | C379CF16E24A0688 | 13449 | 走らせ直しのスクリプト（版 1.0）の計算の再現の機能として、論文とともに公開する（コードの検分〔段階 E の枠 §9〕を終えた版・E6・段階 E の枠 §10） | 11-data-and-code |
| `E/tool1/op4b_rerun.py` | 0C0662F29E8A249E | 129656 | 走らせ直しのスクリプト（版 1.0）の走らせ直しの機能として、論文とともに公開する（コードの検分〔段階 E の枠 §9〕を終えた版・E6・段階 E の枠 §10） | 11-data-and-code |
| `E/tool1/test-criteria-rerun-v1.0.md` | EB7F89D23A9B2B73 | 4981 | 公開の形を E6 の前に決める（走らせ直しのスクリプトの試しの合格の条件と記録・段階 E の枠 §7 の項 12） | 11-data-and-code |
| `E/tool1/tests/20261016-201735/test-record.md` | E40C9BD521320F87 | 50556 | 公開の形を E6 の前に決める（走らせ直しのスクリプトの試しの合格の条件と記録・段階 E の枠 §7 の項 12） | 11-data-and-code |
| `plans/deviation-D1pE-1/deviation-D1pE-1.md` | B4AF13A6E3B231F5 | 8437 | 公開済み（公開の置き場の `records/D1pE/deviation-D1pE-1/deviation-D1pE-1.md`・初めて置いたコミット e549c2b 2026-10-13） | appx-E-deviations・appx-E-deviations（引用の中） |
| `plans/plan-framing-sensitivity-scale-and-mechanism-v1.0-2026-09-07.md` | E242C5FF31EDB05B | 21715 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | （原稿の字が指す・計画書 v1.0（節 9.8）） |
| `plans/plan-framing-sensitivity-scale-and-mechanism-v3.0-2026-10-13.md` | 8165808D28274E82 | 205785 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 09-alternatives-limits・（原稿の字が指す・計画書 v3.0（節 9.8・二つの登録の結果の後の版）） |
| `plans/policy-readings-cold-arm-2026-10-11.md` | 99E909958B1961DD | 8735 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D292-D293-2026-10-02.md` | 3E691B25B520CE94 | 4573 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-H-records |
| `plans/rulings-D294-D295-2026-10-03.md` | 3F38CCC468DC62FA | 13433 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods・05-stageD-methods（引用の中） |
| `plans/rulings-D296-2026-10-03.md` | FAF71095CA2D1A5D | 6250 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods・05-stageD-methods（引用の中）・appx-I-rules（引用の中） |
| `plans/rulings-D300-2026-10-03.md` | AA0CE2D019DF0F96 | 6886 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods・05-stageD-methods（引用の中）・09-alternatives-limits（引用の中）・appx-I-rules（引用の中） |
| `plans/rulings-D301-2026-10-03.md` | 2655E8EDF2067C8A | 1794 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-ja |
| `plans/rulings-D303-2026-10-03.md` | C6083C03497BD6A0 | 8183 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・appx-D-ja・appx-I-rules（引用の中） |
| `plans/rulings-D304-2026-10-04.md` | E432D1F4BAF708EA | 6035 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods・05-stageD-methods（引用の中） |
| `plans/rulings-D306-2026-10-04.md` | 01C84C4BE4647F41 | 3765 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D318-2026-10-05.md` | 8CE8A546ECF85D3C | 2318 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 09-alternatives-limits（引用の中） |
| `plans/rulings-D322-2026-10-08.md` | EE60B65A302784AE | 4707 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 09-alternatives-limits（引用の中） |
| `plans/rulings-D323-2026-10-08.md` | ABC95DBE1070B1A4 | 6657 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-ja |
| `plans/rulings-D324-2026-10-08.md` | BFAAB0E1A17132C8 | 3328 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 06-results-ja（引用の中） |
| `plans/rulings-D325-2026-10-08.md` | 0710F09588537D1E | 4936 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D327-2026-10-08.md` | E23F86E5553BF284 | 4241 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D328-2026-10-09.md` | 38E343E185109AD8 | 5167 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods・05-stageD-methods（引用の中）・09-alternatives-limits（引用の中） |
| `plans/rulings-D329-2026-10-09.md` | 8CC1FCD269D02F09 | 4438 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D330-2026-10-09.md` | 1B07ECB5437F945F | 3741 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D332-2026-10-09.md` | AA44266D3B67CD2C | 3305 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D333-2026-10-09.md` | CE5FB40ED4095B04 | 2939 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D334-2026-10-09.md` | DB5C9D44DC0298A3 | 7286 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D335-2026-10-09.md` | E87804C5E24D6FFC | 2932 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D336-2026-10-09.md` | 55F15C328268C791 | 3618 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D337-2026-10-09.md` | 672C6297C177F705 | 2355 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D340-2026-10-09.md` | 466B1D8818FE9B9B | 6083 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・13-coi・13-coi（引用の中） |
| `plans/rulings-D341-2026-10-09.md` | BF565AABC800B813 | 9437 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods・05-stageD-methods（引用の中）・06-results-ja・06-results-ja（引用の中）・09-alternatives-limits（引用の中）・13-coi（引用の中）・appx-D-ja・appx-E-deviations・appx-H-records・appx-I-rules（引用の中） |
| `plans/rulings-D343-2026-10-09.md` | FBA61080E3B6C7DE | 16065 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D344-2026-10-09.md` | C187AB12023FDD2B | 13125 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・13-coi（引用の中） |
| `plans/rulings-D345-2026-10-10.md` | 22170ABB115F6C2A | 22912 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・06-results-ja（引用の中）・13-coi（引用の中） |
| `plans/rulings-D346-2026-10-10-addendum.md` | 6D1E75324A076CF0 | 4102 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・13-coi（引用の中） |
| `plans/rulings-D350-2026-10-10.md` | 3F040ACC04D38DB4 | 4127 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・07-english-materials（引用の中） |
| `plans/rulings-D351-2026-10-10.md` | E10605D08A709842 | 8568 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D352-2026-10-10.md` | 540CAAE94A36F2A1 | 4255 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D353-2026-10-11.md` | ED1A37A4F4C0F2D7 | 5336 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D354-2026-10-11.md` | BFC15FD0DD7474CA | 6928 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 06-results-ja（引用の中）・appx-D-ja（引用の中）・appx-E-deviations（引用の中）・appx-F-terms・appx-H-records |
| `plans/rulings-D355-2026-10-11.md` | B8ADF062F659BCCE | 12398 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 06-results-ja（引用の中）・appx-E-deviations（引用の中） |
| `plans/rulings-D356-2026-10-11.md` | 7F107F0C65964B92 | 5514 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D357-2026-10-11.md` | 7D2100E284CABB6D | 16051 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 06-results-ja（引用の中）・appx-E-deviations（引用の中）・appx-H-records |
| `plans/rulings-D363-2026-10-11.md` | CBB470AEC236A518 | 9506 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・07-english-materials・07-english-materials（引用の中） |
| `plans/rulings-D364-2026-10-11.md` | 570FE2218B07E89D | 5865 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・07-english-materials（引用の中） |
| `plans/rulings-D365-2026-10-11.md` | 08AE91DEA93EED08 | 2625 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 07-english-materials（引用の中） |
| `plans/rulings-D369-2026-10-11.md` | 6CD6BA40F79F9032 | 18323 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 07-english-materials・07-english-materials（引用の中） |
| `plans/rulings-D373-2026-10-11.md` | B90EE18E5AF2EE77 | 7181 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 07-english-materials・07-english-materials（引用の中） |
| `plans/rulings-D377-2026-10-11.md` | CA75E574A35BA82A | 4126 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 07-english-materials・07-english-materials（引用の中）・appx-H-records |
| `plans/rulings-D379-2026-10-11.md` | FCF24825B169A381 | 3131 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 07-english-materials（引用の中） |
| `plans/rulings-D380-2026-10-11.md` | D5063F86D57D7DAE | 8686 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods・05-stageD-methods（引用の中）・08-results-en・08-results-en（引用の中）・appx-I-rules（引用の中） |
| `plans/rulings-D381-2026-10-11.md` | 6A3F03487FC072BF | 6101 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D382-2026-10-11.md` | BF3793870DD51DFA | 6538 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中）・07-english-materials（引用の中） |
| `plans/rulings-D383-2026-10-11.md` | 9F0AD367EAA33B33 | 4935 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 05-stageD-methods（引用の中） |
| `plans/rulings-D386-2026-10-12.md` | 60DF8C9D5F1BBB2A | 15068 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 02-methods（引用の中）・05-stageD-methods（引用の中）・07-english-materials・07-english-materials（引用の中）・08-results-en（引用の中）・09-alternatives-limits（引用の中） |
| `plans/rulings-D388-2026-10-12.md` | 0877720991317CF8 | 14677 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 02-methods（引用の中）・05-stageD-methods（引用の中）・07-english-materials・07-english-materials（引用の中）・08-results-en（引用の中）・09-alternatives-limits（引用の中） |
| `plans/rulings-D391-2026-10-12.md` | 346AC0F098751C9E | 30067 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 02-methods（引用の中）・05-stageD-methods（引用の中）・07-english-materials（引用の中）・08-results-en（引用の中）・09-alternatives-limits（引用の中） |
| `plans/rulings-D396-2026-10-12.md` | D9D09672EB50B216 | 13624 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D397-2026-10-12.md` | 8DCD26DC6FA1F9FB | 5844 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D398-2026-10-12.md` | E4E6042E6208ACD9 | 4448 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D399-2026-10-12.md` | 313FEE49101E1787 | 3384 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D400-2026-10-13.md` | 8740511CB957F532 | 2831 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D401-2026-10-13.md` | 0C232914719C1ABE | 2103 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D402-2026-10-13.md` | C1A7C70575999D4D | 3500 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D403-2026-10-13.md` | 58525FD8122208D8 | 12778 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 08-results-en（引用の中）・13-coi・13-coi（引用の中）・appx-D-en（引用の中）・appx-E-deviations（引用の中）・appx-H-records |
| `plans/rulings-D404-2026-10-13.md` | 8935C11FE85AE7B5 | 4636 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D405-2026-10-13.md` | E05449675DAA29C0 | 7111 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 08-results-en（引用の中）・13-coi・13-coi（引用の中）・appx-D-en（引用の中）・appx-E-deviations（引用の中） |
| `plans/rulings-D406-2026-10-13.md` | 673002EB3050011E | 4628 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-E-deviations（引用の中） |
| `plans/rulings-D407-2026-10-13.md` | 86BEB219DCD489F9 | 10051 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 08-results-en（引用の中）・13-coi・13-coi（引用の中）・appx-E-deviations（引用の中） |
| `plans/rulings-D408-2026-10-13.md` | 2E6ACBF8C7617DF0 | 4012 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 13-coi・13-coi（引用の中）・appx-E-deviations（引用の中） |
| `plans/rulings-D419-2026-10-13.md` | 81640BBE2F483258 | 9416 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 13-coi（引用の中） |
| `plans/rulings-D425-2026-10-14.md` | B06AF7777BFB4947 | 6806 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 09-alternatives-limits（引用の中）・appx-H-records |
| `plans/rulings-D430-2026-10-14.md` | C1D09DDF370EEB30 | 11832 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 09-alternatives-limits（引用の中） |
| `plans/rulings-D438-2026-10-14.md` | CCA62D750A8A6459 | 4806 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-en |
| `plans/rulings-D445-2026-10-14.md` | F7DA93427AFCED43 | 12806 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | appx-D-ja・appx-E-deviations・appx-H-records |
| `plans/rulings-D450-2026-10-14.md` | 05192AFB4176C8D4 | 18978 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 12-references・13-coi・appx-H-records |
| `plans/rulings-D452-2026-10-14.md` | 716C5E7D4115A8D2 | 7598 | 公開の形を E6 の前に決める（段階 E の枠 §10・記録の目録には名と SHA-256 を置く） | 11-data-and-code |
| `summary/reviews/final/rulings-D289.md` | FC71484906BF46F3 | 3357 | 公開済み（公開の置き場の `summary/reviews/final/rulings-D289.md`・初めて置いたコミット 037eeb0 2026-10-02） | appx-F-terms |

- 行 192（そのうち公開済み 6）。伏せた置き場と移した記録の置き場を指す名（2）は、読まずにこの表から外した。引用の中の決定の番号で、内部の置き場に決定の記録のファイルが無いもの（前の段の記録の中の番号など・この表に行を立てない）: D128・D167・D178・D187・D203・D215・D220・D221・D223・D235・D256・D258・D259・D265・D275・D276・D278・D287・D289・D293。
- 名を伏せた行: ファイルの名に、集約の経路を経由して較正した系統の名を含む内部のファイルは、その名を〔系統の名〕と伏せて書く（決定 D325・D341-5・SHA16 は名を伏せる前のファイルの値）。


〔表の差し込みの終わり〕出所のファイルを差し込んだ。引用の禁止の一文（行の頭が「本記録のいかなる数値も」「本票のいかなる数値も」「本表のいかなる数値も」の行で、行の頭の「>」を含む）を 1 行除いた。うち引用の形の行は 0。除いた行の在りかは 見出し「論文が名を挙げる内部の記録とスクリプトの在りか（2026-10-17 06:33:43 日本時間・スクリプト `E/E3/calc/records_sha_E3_v08.py` v0.8）」の下。除いた後に同じ一文で始まる行は残っていない（スクリプトが照らした）。見出しを 2 段下げた。足した印は無い。ほかの字は替えていない。

## H.4 本文の章の引用と図と表の出所（章ごと）

本文の章（要旨〜章 10）の〔引用 n〕と、図と表の出所（ファイル・行・SHA16）を、章ごとに置く。組み立てのスクリプトが、本文の章を組みながら書いた表である。〈公開〉は公開の置き場のファイル、〈内部〉は内部の置き場のファイルである（在りかと公開の予定は H.3）。

### 章 1（`01-introduction.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 地の文の引用 | 〈公開〉`design/design-v1.0-FROZEN.md` | 100 行 | D7963FE1C011341B |
| 〔引用 2〕 | 地の文の引用 | 〈公開〉`design/design-v1.0-FROZEN.md` | 99 行 | D7963FE1C011341B |
| 〔引用 3〕 | 地の文の引用 | 〈公開〉`records/vprime/results-report-Vprime-FINAL-2026-09-09.md` | 987 行 | 5E70EF329C4A6739 |
| 〔引用 4〕 | 地の文の引用 | 〈公開〉`design/design-v1.0-FROZEN.md` | 100 行 | D7963FE1C011341B |
| 〔引用 5〕 | 地の文の引用 | 〈公開〉`design/design-v1.0-FROZEN.md` | 100 行 | D7963FE1C011341B |

### 章 2（`02-methods.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 地の文の引用 | 〈公開〉`arms/frozen-from-ryokai-os/app-scenarios.json` | 16 行 | 7AD7E49459D5C402 |
| 〔引用 2〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 132 行 | 40BF3C3663BA8C69 |
| 〔引用 3〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 112 行 | 40BF3C3663BA8C69 |
| 〔引用 4〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 113 行 | 40BF3C3663BA8C69 |
| 〔引用 5〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 113 行 | 40BF3C3663BA8C69 |
| 〔引用 6〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 133 行 | 40BF3C3663BA8C69 |
| 〔引用 7〕 | 地の文の引用 | 〈公開〉`README.md` | 11 行 | 7F1A0EC08A06BAF3 |
| 〔引用 8〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 164〜166 行 | 40BF3C3663BA8C69 |
| 〔引用 9〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 159 行 | 40BF3C3663BA8C69 |
| 〔引用 10〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 253 行 | F557603870509EA2 |
| 〔引用 11〕 | 地の文の引用 | 〈公開〉`design/design-stageA-FROZEN.md` | 14 行 | C30AF752D3531904 |
| 〔引用 12〕 | 地の文の引用 | 〈公開〉`design/design-Blens-FROZEN.md` | 436 行 | A6281F419F059145 |

### 章 3（`03-4b-and-scale.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 33 行 | 059FF367B34B1A23 |
| 〔引用 2〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 35 行 | 059FF367B34B1A23 |
| 〔引用 3〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 37〜53 行 | 059FF367B34B1A23 |
| 〔引用 4〕 | 地の文の引用 | 〈公開〉`design/design-v1.0-FROZEN.md` | 34 行 | D7963FE1C011341B |
| 〔引用 5〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 55 行 | 059FF367B34B1A23 |
| 〔引用 6〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 57〜63 行 | 059FF367B34B1A23 |
| 〔引用 7〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 65 行 | 059FF367B34B1A23 |
| 〔引用 8〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 67〜76 行 | 059FF367B34B1A23 |
| 〔引用 9〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 78 行 | 059FF367B34B1A23 |
| 〔引用 10〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 80〜87 行 | 059FF367B34B1A23 |
| 〔引用 11〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 89 行 | 059FF367B34B1A23 |
| 〔引用 12〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 91〜106 行 | 059FF367B34B1A23 |
| 図 3.1 | 図 | 〈内部〉`E/E3/calc/calc1-v0.5/fig-calc1-stageA-v0.5.png` | — | 9FA05EF4680FAC0F |
| 〔引用 13〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 148 行 | AB7491FF30074FBD |
| 〔引用 14〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 57 行 | 059FF367B34B1A23 |
| 〔引用 15〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 149 行 | AB7491FF30074FBD |
| 〔引用 16〕 | 地の文の引用 | 〈公開〉`design/design-stageA-FROZEN.md` | 48 行 | C30AF752D3531904 |
| 〔引用 17〕 | 段落の引用 | 〈公開〉`records/pilotC/00-frame-pilotC-2026-10-02.md` | 9〜10 行 | 27A44D09FA206680 |
| 〔引用 18〕 | 段落の引用 | 〈公開〉`records/pilotC/00-frame-pilotC-2026-10-02.md` | 14〜16 行 | 27A44D09FA206680 |
| 〔引用 19〕 | 段落の引用 | 〈公開〉`records/pilotC/00-frame-pilotC-2026-10-02.md` | 20〜24 行 | 27A44D09FA206680 |
| 図 3.2 | 図 | 〈内部〉`E/E3/calc/calc2-v0.5/fig-calc2-pilotC-v0.5.png` | — | 6A5F28943B23B43C |
| 〔引用 20〕 | 段落の引用 | 〈公開〉`records/pilotC/00-frame-pilotC-2026-10-02.md` | 112〜116 行 | 27A44D09FA206680 |

### 章 4（`04-mechanism.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 地の文の引用 | 〈公開〉`design/design-stageB-FROZEN.md` | 92 行 | 8B3D54E4500B46FF |
| 〔引用 2〕 | 地の文の引用 | 〈公開〉`design/design-stageB-FROZEN.md` | 31 行 | 8B3D54E4500B46FF |
| 〔引用 3〕 | 地の文の引用 | 〈公開〉`design/design-stageB-FROZEN.md` | 93 行 | 8B3D54E4500B46FF |
| 〔引用 4〕 | 地の文の引用 | 〈公開〉`design/design-stageB-FROZEN.md` | 355 行 | 8B3D54E4500B46FF |
| 〔引用 5〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 108 行 | 059FF367B34B1A23 |
| 〔引用 6〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 110〜142 行 | 059FF367B34B1A23 |
| 〔引用 7〕 | 地の文の引用 | 〈公開〉`records/B/results-B-FINAL-2026-09-23.md` | 212 行 | A40E9CA0D388753B |
| 〔引用 8〕 | 地の文の引用 | 〈公開〉`records/B/results-B-FINAL-2026-09-23.md` | 132 行 | A40E9CA0D388753B |
| 〔引用 9〕 | 地の文の引用 | 〈公開〉`records/B/results-B-FINAL-2026-09-23.md` | 212 行 | A40E9CA0D388753B |
| 〔引用 10〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 144 行 | 059FF367B34B1A23 |
| 〔引用 11〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 146〜154 行 | 059FF367B34B1A23 |
| 〔引用 12〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 156 行 | 059FF367B34B1A23 |
| 〔引用 13〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 158〜176 行 | 059FF367B34B1A23 |
| 〔引用 14〕 | 地の文の引用 | 〈公開〉`records/Bl3/results-Bl3-FINAL-2026-09-27.md` | 470 行 | 90EEB93792733FAC |
| 〔引用 15〕 | 地の文の引用 | 〈公開〉`records/Bl3/results-Bl3-FINAL-2026-09-27.md` | 470 行 | 90EEB93792733FAC |
| 〔引用 16〕 | 地の文の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 178 行 | 059FF367B34B1A23 |
| 〔引用 17〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 180〜191 行 | 059FF367B34B1A23 |
| 〔引用 18〕 | 段落の引用 | 〈公開〉`summary/summary-interim-FINAL-2026-10-02.md` | 397〜398 行 | 059FF367B34B1A23 |

### 章 5（`05-stageD-methods.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 11 行 | 40BF3C3663BA8C69 |
| 〔引用 2〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 11 行 | F557603870509EA2 |
| 〔引用 3〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 12 行 | 40BF3C3663BA8C69 |
| 〔引用 4〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 12 行 | 40BF3C3663BA8C69 |
| 〔引用 5〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 12 行 | 40BF3C3663BA8C69 |
| 〔引用 6〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 12 行 | 40BF3C3663BA8C69 |
| 〔引用 7〕 | 段落の引用 | 〈公開〉`records/D1pE/calibration/00-frame-D1pE-cal.md` | 53〜56 行 | 5C21615162C7B43D |
| 〔引用 8〕 | 地の文の引用 | 〈公開〉`records/D1pE/calibration/00-frame-D1pE-cal.md` | 49 行 | 5C21615162C7B43D |
| 〔引用 9〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 270 行 | F557603870509EA2 |
| 〔引用 10〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 13 行 | F557603870509EA2 |
| 〔引用 11〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 13 行 | F557603870509EA2 |
| 〔引用 12〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 15 行 | 40BF3C3663BA8C69 |
| 〔引用 13〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 15 行 | 40BF3C3663BA8C69 |
| 〔引用 14〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 29 行 | 40BF3C3663BA8C69 |
| 〔引用 15〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 13 行 | 40BF3C3663BA8C69 |
| 〔引用 16〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 14 行 | F557603870509EA2 |
| 〔引用 17〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 14 行 | F557603870509EA2 |
| 〔引用 18〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 12 行 | 40BF3C3663BA8C69 |
| 〔引用 19〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 17〜26 行 | 40BF3C3663BA8C69 |
| 〔引用 20〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 28 行 | 40BF3C3663BA8C69 |
| 〔引用 21〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 31〜40 行 | 40BF3C3663BA8C69 |
| 〔引用 22〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 14 行 | F557603870509EA2 |
| 〔引用 23〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 14 行 | F557603870509EA2 |
| 〔引用 24〕 | 段落の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 16〜27 行 | F557603870509EA2 |
| 〔引用 25〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 89〜109 行 | 40BF3C3663BA8C69 |
| 〔引用 26〕 | 段落の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 98〜111 行 | F557603870509EA2 |
| 〔引用 27〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 289 行 | 40BF3C3663BA8C69 |
| 〔引用 28〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 289 行 | 40BF3C3663BA8C69 |
| 〔引用 29〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 295 行 | 40BF3C3663BA8C69 |
| 〔引用 30〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 122 行 | 40BF3C3663BA8C69 |
| 〔引用 31〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 122 行 | 40BF3C3663BA8C69 |
| 〔引用 32〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 112 行 | 40BF3C3663BA8C69 |
| 〔引用 33〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 112 行 | 40BF3C3663BA8C69 |
| 〔引用 34〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 114 行 | 40BF3C3663BA8C69 |
| 〔引用 35〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 116 行 | F557603870509EA2 |
| 〔引用 36〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 290 行 | 40BF3C3663BA8C69 |
| 〔引用 37〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 113 行 | 40BF3C3663BA8C69 |
| 〔引用 38〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 113 行 | 40BF3C3663BA8C69 |
| 〔引用 39〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 113 行 | 40BF3C3663BA8C69 |
| 〔引用 40〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 115 行 | F557603870509EA2 |
| 〔引用 41〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 116 行 | 40BF3C3663BA8C69 |
| 〔引用 42〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 116 行 | 40BF3C3663BA8C69 |
| 〔引用 43〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 117 行 | 40BF3C3663BA8C69 |
| 〔引用 44〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 118 行 | 40BF3C3663BA8C69 |
| 〔引用 45〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 120 行 | F557603870509EA2 |
| 〔引用 46〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 296 行 | 40BF3C3663BA8C69 |
| 〔引用 47〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 120 行 | 40BF3C3663BA8C69 |
| 〔引用 48〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 120 行 | 40BF3C3663BA8C69 |
| 〔引用 49〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 120 行 | 40BF3C3663BA8C69 |
| 〔引用 50〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 132 行 | F557603870509EA2 |
| 〔引用 51〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 132 行 | F557603870509EA2 |
| 〔引用 52〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 65 行 | 4DC7738F03A37B05 |
| 〔引用 53〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 107 行 | F557603870509EA2 |
| 〔引用 54〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 109 行 | F557603870509EA2 |
| 〔引用 55〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 119 行 | 40BF3C3663BA8C69 |
| 〔引用 56〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 131 行 | F557603870509EA2 |
| 〔引用 57〕 | 地の文の引用 | 〈公開〉`records/D1pE/calibration/00-frame-D1pE-cal.md` | 74 行 | 5C21615162C7B43D |
| 〔引用 58〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 119 行 | 40BF3C3663BA8C69 |
| 〔引用 59〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 246 行 | 40BF3C3663BA8C69 |
| 〔引用 60〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 292 行 | 40BF3C3663BA8C69 |
| 〔引用 61〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 292 行 | 40BF3C3663BA8C69 |
| 〔引用 62〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 292 行 | 40BF3C3663BA8C69 |
| 〔引用 63〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 292 行 | 40BF3C3663BA8C69 |
| 〔引用 64〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 292 行 | 40BF3C3663BA8C69 |
| 〔引用 65〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 292 行 | 40BF3C3663BA8C69 |
| 〔引用 66〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 275 行 | F557603870509EA2 |
| 〔引用 67〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 191 行 | 40BF3C3663BA8C69 |
| 〔引用 68〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 207 行 | 40BF3C3663BA8C69 |
| 〔引用 69〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 140〜149 行 | 40BF3C3663BA8C69 |
| 〔引用 70〕 | 段落の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 176〜185 行 | F557603870509EA2 |

### 章 6（`06-results-ja.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 12 行 | 0AFDCBF29BC47E04 |
| 〔引用 2〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 13 行 | 0AFDCBF29BC47E04 |
| 〔引用 3〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 287 行 | 40BF3C3663BA8C69 |
| 〔引用 4〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 14〜19 行 | 0AFDCBF29BC47E04 |
| 〔引用 5〕 | 件数の行の引用 | 〈公開〉`records/D1p/confirm/confirm-D1p.md` | 14 行 | 1C750DC6FD1A5C68 |
| 〔引用 6〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 20 行 | 0AFDCBF29BC47E04 |
| 〔引用 7〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 22〜24 行 | 0AFDCBF29BC47E04 |
| 〔引用 8〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 25〜27 行 | 0AFDCBF29BC47E04 |
| 〔引用 9〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 133 行 | 40BF3C3663BA8C69 |
| 〔引用 10〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 96 行 | 0AFDCBF29BC47E04 |
| 〔引用 11〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 98〜101 行 | 0AFDCBF29BC47E04 |
| 図 6.2 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/fig-gemini25flash.png` | — | AD9B28D613BCA84D |
| 〔引用 12〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 105〜122 行 | 0AFDCBF29BC47E04 |
| 〔引用 13〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 126〜136 行 | 0AFDCBF29BC47E04 |
| 〔引用 14〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 140〜152 行 | 0AFDCBF29BC47E04 |
| 〔引用 15〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 154 行 | 0AFDCBF29BC47E04 |
| 〔引用 16〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 156〜161 行 | 0AFDCBF29BC47E04 |
| 図 6.3 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/fig-grok420nr.png` | — | E47C4A414FA7201D |
| 〔引用 17〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 165〜187 行 | 0AFDCBF29BC47E04 |
| 〔引用 18〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 191〜204 行 | 0AFDCBF29BC47E04 |
| 〔引用 19〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 208〜224 行 | 0AFDCBF29BC47E04 |
| 〔引用 20〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 226 行 | 0AFDCBF29BC47E04 |
| 〔引用 21〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 228〜229 行 | 0AFDCBF29BC47E04 |
| 図 6.4 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/fig-deepseekv32-a.png` | — | BFC81D62DCEE41A1 |
| 〔引用 22〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 233〜250 行 | 0AFDCBF29BC47E04 |
| 〔引用 23〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 254〜264 行 | 0AFDCBF29BC47E04 |
| 〔引用 24〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 268〜281 行 | 0AFDCBF29BC47E04 |
| 〔引用 25〕 | 地の文の引用 | 〈内部〉`E/E2/record/E2-record-ja.md` | 901 行 | 171F869D6CFF687E |
| 〔引用 26〕 | 段落の引用 | 〈内部〉`E/E2/record/E2-record-ja.md` | 903〜909 行 | 171F869D6CFF687E |
| 〔引用 27〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 283 行 | 0AFDCBF29BC47E04 |
| 〔引用 28〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 285〜287 行 | 0AFDCBF29BC47E04 |
| 「6.5 deepseek-flash」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/table-deepseekflash.md` | — | 091B3B429A9708EB |
| 〔引用 29〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 291〜303 行 | 0AFDCBF29BC47E04 |
| 〔引用 30〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 307〜314 行 | 0AFDCBF29BC47E04 |
| 〔引用 31〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 318〜326 行 | 0AFDCBF29BC47E04 |
| 〔引用 32〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 328 行 | 0AFDCBF29BC47E04 |
| 〔引用 33〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 330〜332 行 | 0AFDCBF29BC47E04 |
| 図 6.6 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/fig-llama31-8b-n.png` | — | C8242D2887474786 |
| 〔引用 34〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 336〜363 行 | 0AFDCBF29BC47E04 |
| 〔引用 35〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 367〜383 行 | 0AFDCBF29BC47E04 |
| 〔引用 36〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 387〜405 行 | 0AFDCBF29BC47E04 |
| 〔引用 37〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 407 行 | 0AFDCBF29BC47E04 |
| 〔引用 38〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 409〜414 行 | 0AFDCBF29BC47E04 |
| 図 6.7 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/fig-llama4scout.png` | — | EEDBF551F6E35C31 |
| 〔引用 39〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 418〜435 行 | 0AFDCBF29BC47E04 |
| 〔引用 40〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 439〜449 行 | 0AFDCBF29BC47E04 |
| 〔引用 41〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 453〜465 行 | 0AFDCBF29BC47E04 |
| 〔引用 42〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 467 行 | 0AFDCBF29BC47E04 |
| 〔引用 43〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 469〜470 行 | 0AFDCBF29BC47E04 |
| 図 6.8 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/fig-mistrallarge3-m.png` | — | 9A49E2012584306C |
| 〔引用 44〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 474〜491 行 | 0AFDCBF29BC47E04 |
| 〔引用 45〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 495〜505 行 | 0AFDCBF29BC47E04 |
| 〔引用 46〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 509〜521 行 | 0AFDCBF29BC47E04 |
| 〔引用 47〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 523 行 | 0AFDCBF29BC47E04 |
| 〔引用 48〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 525〜529 行 | 0AFDCBF29BC47E04 |
| 図 6.9 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/fig-kimik3-m.png` | — | A15E13807660397E |
| 〔引用 49〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 533〜550 行 | 0AFDCBF29BC47E04 |
| 〔引用 50〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 554〜564 行 | 0AFDCBF29BC47E04 |
| 〔引用 51〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 568〜581 行 | 0AFDCBF29BC47E04 |
| 〔引用 52〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 583 行 | 0AFDCBF29BC47E04 |
| 〔引用 53〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 585〜586 行 | 0AFDCBF29BC47E04 |
| 「6.10 Qwen2.5-Coder-32B-Instruct」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/table-qwen25coder32b-n.md` | — | 6A291087A0509225 |
| 〔引用 54〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 590〜597 行 | 0AFDCBF29BC47E04 |
| 〔引用 55〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 601〜605 行 | 0AFDCBF29BC47E04 |
| 〔引用 56〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 609〜614 行 | 0AFDCBF29BC47E04 |
| 〔引用 57〕 | 地の文の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 616 行 | 0AFDCBF29BC47E04 |
| 〔引用 58〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 618〜619 行 | 0AFDCBF29BC47E04 |
| 「6.11 Qwen3.8 Max（0902）」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/calc3-v0.5/ja/table-qwen38max-a.md` | — | 892967E8652521D6 |
| 〔引用 59〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 623〜635 行 | 0AFDCBF29BC47E04 |
| 〔引用 60〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 639〜646 行 | 0AFDCBF29BC47E04 |
| 〔引用 61〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 650〜659 行 | 0AFDCBF29BC47E04 |
| 〔引用 62〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 663〜683 行 | 0AFDCBF29BC47E04 |
| 「6.12 結果の型と、比べごとの機種の数（記述）」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/typecount-v0.1/ja/typecount-ja.md` | — | 141B0F157F4D2D3E |
| 〔引用 63〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 766 行 | 0AFDCBF29BC47E04 |
| 〔引用 64〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 731〜732 行 | 0AFDCBF29BC47E04 |
| 〔引用 65〕 | 段落の引用 | 〈公開〉`records/D1p/results-D1p-FINAL-2026-10-11.md` | 44 行 | 0AFDCBF29BC47E04 |
| 〔引用 66〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 281 行 | 40BF3C3663BA8C69 |
| 〔引用 67〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 281 行 | 40BF3C3663BA8C69 |

### 章 7（`07-english-materials.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 11 行 | F557603870509EA2 |
| 〔引用 2〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 11 行 | F557603870509EA2 |
| 〔引用 3〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 273 行 | F557603870509EA2 |
| 〔引用 4〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 273 行 | F557603870509EA2 |
| 〔引用 5〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 273 行 | F557603870509EA2 |
| 〔引用 6〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 12 行 | F557603870509EA2 |
| 〔引用 7〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 12 行 | F557603870509EA2 |
| 〔引用 8〕 | 地の文の引用 | 〈公開〉`records/D1pE/calibration/00-frame-D1pE-cal.md` | 48 行 | 5C21615162C7B43D |
| 〔引用 9〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 12 行 | F557603870509EA2 |
| 〔引用 10〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 90 行 | F557603870509EA2 |
| 〔引用 11〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 12 行 | F557603870509EA2 |
| 〔引用 12〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 12 行 | F557603870509EA2 |
| 〔引用 13〕 | 地の文の引用 | 〈公開〉`records/D1pE/translation/freeze-xlate-D1pE.md` | 11 行 | 593054E132FD1F89 |
| 〔引用 14〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 268 行 | F557603870509EA2 |
| 〔引用 15〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 268 行 | F557603870509EA2 |
| 〔引用 16〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 268 行 | F557603870509EA2 |
| 〔引用 17〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 268 行 | F557603870509EA2 |

### 章 8（`08-results-en.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 14 行 | 4DC7738F03A37B05 |
| 〔引用 2〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 17 行 | 4DC7738F03A37B05 |
| 〔引用 3〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 15〜16 行 | 4DC7738F03A37B05 |
| 〔引用 4〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 18〜22 行 | 4DC7738F03A37B05 |
| 〔引用 5〕 | 件数の行の引用 | 〈公開〉`records/D1pE/confirm/confirm-D1pE.md` | 15 行 | DE68AB25DA97A8A4 |
| 〔引用 6〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 23 行 | 4DC7738F03A37B05 |
| 〔引用 7〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 24 行 | 4DC7738F03A37B05 |
| 〔引用 8〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 26〜28 行 | 4DC7738F03A37B05 |
| 〔引用 9〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 29〜31 行 | 4DC7738F03A37B05 |
| 〔引用 10〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 253 行 | F557603870509EA2 |
| 〔引用 11〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 253 行 | F557603870509EA2 |
| 〔引用 12〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 253 行 | F557603870509EA2 |
| 〔引用 13〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 171 行 | F557603870509EA2 |
| 〔引用 14〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 171 行 | F557603870509EA2 |
| 〔引用 15〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 104 行 | 4DC7738F03A37B05 |
| 〔引用 16〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 106〜108 行 | 4DC7738F03A37B05 |
| 「8.2 Gemini 2.5 Flash」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/calc3-v0.5/en/table-gemini25flash.md` | — | 0DD062A2F22AD0DE |
| 〔引用 17〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 112〜119 行 | 4DC7738F03A37B05 |
| 〔引用 18〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 123〜127 行 | 4DC7738F03A37B05 |
| 〔引用 19〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 131〜136 行 | 4DC7738F03A37B05 |
| 〔引用 20〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 138 行 | 4DC7738F03A37B05 |
| 〔引用 21〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 140〜142 行 | 4DC7738F03A37B05 |
| 「8.3 grok-4.20（非推論）」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/calc3-v0.5/en/table-grok420nr.md` | — | 5696D45D6F5B9165 |
| 〔引用 22〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 146〜153 行 | 4DC7738F03A37B05 |
| 〔引用 23〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 157〜161 行 | 4DC7738F03A37B05 |
| 〔引用 24〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 165〜171 行 | 4DC7738F03A37B05 |
| 〔引用 25〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 175〜176 行 | 4DC7738F03A37B05 |
| 〔引用 26〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 178 行 | 4DC7738F03A37B05 |
| 〔引用 27〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 180〜183 行 | 4DC7738F03A37B05 |
| 「8.4 deepseek-flash」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/calc3-v0.5/en/table-deepseekflash.md` | — | 40767F8B4B67E1D2 |
| 〔引用 28〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 187〜199 行 | 4DC7738F03A37B05 |
| 〔引用 29〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 203〜210 行 | 4DC7738F03A37B05 |
| 〔引用 30〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 214〜228 行 | 4DC7738F03A37B05 |
| 〔引用 31〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 232〜233 行 | 4DC7738F03A37B05 |
| 〔引用 32〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 235 行 | 4DC7738F03A37B05 |
| 〔引用 33〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 237〜241 行 | 4DC7738F03A37B05 |
| 図 8.5 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/en/fig-llama4scout.png` | — | 2DD6ABF6B9DA8072 |
| 〔引用 34〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 245〜262 行 | 4DC7738F03A37B05 |
| 〔引用 35〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 266〜276 行 | 4DC7738F03A37B05 |
| 〔引用 36〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 280〜304 行 | 4DC7738F03A37B05 |
| 〔引用 37〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 308〜310 行 | 4DC7738F03A37B05 |
| 〔引用 38〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 312 行 | 4DC7738F03A37B05 |
| 〔引用 39〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 314〜317 行 | 4DC7738F03A37B05 |
| 「8.6 Mistral Large 3（2512）」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/calc3-v0.5/en/table-mistrallarge3-m.md` | — | 9FBD817EA7F4C883 |
| 〔引用 40〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 321〜333 行 | 4DC7738F03A37B05 |
| 〔引用 41〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 337〜344 行 | 4DC7738F03A37B05 |
| 〔引用 42〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 348〜361 行 | 4DC7738F03A37B05 |
| 〔引用 43〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 365〜367 行 | 4DC7738F03A37B05 |
| 〔引用 44〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 369 行 | 4DC7738F03A37B05 |
| 〔引用 45〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 371〜375 行 | 4DC7738F03A37B05 |
| 図 8.7 | 図 | 〈内部〉`E/E3/calc/calc3-v0.5/en/fig-kimik3-m.png` | — | 9589E4F01FB15CA7 |
| 〔引用 46〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 379〜396 行 | 4DC7738F03A37B05 |
| 〔引用 47〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 400〜410 行 | 4DC7738F03A37B05 |
| 〔引用 48〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 414〜430 行 | 4DC7738F03A37B05 |
| 〔引用 49〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 434〜437 行 | 4DC7738F03A37B05 |
| 〔引用 50〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 443〜475 行 | 4DC7738F03A37B05 |
| 「8.8 結果の型と、比べごとの機種の数（記述）」の下の表 | 差し込んだ表 | 〈内部〉`E/E3/calc/typecount-v0.1/en/typecount-en.md` | — | A337D724F058C8CA |
| 〔引用 51〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 549 行 | 4DC7738F03A37B05 |
| 〔引用 52〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 515〜516 行 | 4DC7738F03A37B05 |
| 〔引用 53〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 517 行 | 4DC7738F03A37B05 |
| 〔引用 54〕 | 段落の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 52 行 | 4DC7738F03A37B05 |
| 〔引用 55〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 14 行 | 4DC7738F03A37B05 |
| 〔引用 56〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 14 行 | 4DC7738F03A37B05 |
| 〔引用 57〕 | 地の文の引用 | 〈公開〉`records/D1pE/results-D1pE-FINAL-2026-10-13.md` | 15 行 | 4DC7738F03A37B05 |

### 章 9（`09-alternatives-limits.md`）

| 番号か題 | 種 | 出所 | 行 | SHA16 |
|---|---|---|---|---|
| 〔引用 1〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 282〜284 行 | 40BF3C3663BA8C69 |
| 〔引用 2〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 285 行 | 40BF3C3663BA8C69 |
| 〔引用 3〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 285 行 | 40BF3C3663BA8C69 |
| 〔引用 4〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 286 行 | 40BF3C3663BA8C69 |
| 〔引用 5〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 268 行 | F557603870509EA2 |
| 〔引用 6〕 | 地の文の引用 | 〈公開〉`arms/frozen-from-ryokai-os/armsE/preamble-O.md` | 1 行 | F3EE60C33F825575 |
| 〔引用 7〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 268 行 | F557603870509EA2 |
| 〔引用 8〕 | 地の文の引用 | 〈公開〉`arms/frozen-from-ryokai-os/armsE/preamble-O.md` | 1 行 | F3EE60C33F825575 |
| 〔引用 9〕 | 地の文の引用 | 〈公開〉`arms/panel/OAmi.md` | 1 行 | 94F1829E701FEB88 |
| 〔引用 10〕 | 地の文の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 288 行 | 40BF3C3663BA8C69 |
| 〔引用 11〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 294 行 | 40BF3C3663BA8C69 |
| 〔引用 12〕 | 地の文の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 273 行 | F557603870509EA2 |
| 〔引用 13〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 291 行 | 40BF3C3663BA8C69 |
| 〔引用 14〕 | 段落の引用 | 〈公開〉`records/D1pE/00-frame-D1pE.md` | 274 行 | F557603870509EA2 |
| 〔引用 15〕 | 段落の引用 | 〈公開〉`records/D1p/00-frame-D1p.md` | 293 行 | 40BF3C3663BA8C69 |
| 〔引用 16〕 | 段落の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 415 行 | AB7491FF30074FBD |
| 〔引用 17〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 415 行 | AB7491FF30074FBD |
| 〔引用 18〕 | 段落の引用 | 〈内部〉`plans/plan-framing-sensitivity-scale-and-mechanism-v3.0-2026-10-13.md` | 358〜360 行 | 8165808D28274E82 |
| 〔引用 19〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 121 行 | AB7491FF30074FBD |
| 〔引用 20〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 121 行 | AB7491FF30074FBD |
| 〔引用 21〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 253 行 | AB7491FF30074FBD |
| 〔引用 22〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 254 行 | AB7491FF30074FBD |
| 〔引用 23〕 | 地の文の引用 | 〈内部〉`E/00-frame-E-draft6.md` | 257 行 | AB7491FF30074FBD |

## H.5 本文の章が番号や道を書かずに指す決定の記録とスクリプト

本文の章は、決定の記録の番号とスクリプトの道を書かない（読み手のための起草の決め）。本文の章の字が指す決定の記録とスクリプトは、次のとおりである（記録の在りかは H.3）。

| 章・節 | 本文の字（要点） | 記録 |
|---|---|---|
| 節 2.3 | 集計のスクリプトは、0 の欄の有る無しによらず、いつも 2×2 の表の四つの欄に足す | 日本語の送る文の登録は `D1p/d1p_confirm.py` の 147 行、英語の送る文の登録は `D1pE/d1pe_confirm.py` の 153 行 |
| 節 2.8・節 5.3・節 5.13 | 集約の経路の較正の記録を公開しない決め（どの機種か・何機種かを書かない） | 決定 D341-5・D445 |
| 節 2.9 | 付録 D-en の頭に残した記録の一文 | 決定 D450-6 |
| 節 3.6 | 図 3.2 の三つの条件の選びの二つの決め | 決定 D292・D425-5 |
| 節 5.4 | 凍結した本文の下の表を数えたスクリプト | `E/E3/calc/flow_D.py` |
| 節 5.4 | Qwen2.5-Coder-3B を許諾で外した後の決定 | 決定 D341-2 |
| 節 6.0・節 6.15 | 範囲の読みの追認（2026-10-11 08:59） | 決定 D357-3 |
| 節 6.12 | 判定ラベルを見た後の決定（型の判じ） | 決定 D354-3 |
| 節 7.3 | 訳の四つの直し | 決定 D377 |
| 節 8.8 | 判定ラベルを見た後の決定（型の判じと「OAmi と O」の当て方） | 決定 D403-2 |
| 節 3.5・節 3.6（図 3.1・図 3.2） | 図を描いたスクリプトと、図の値と照らしの記録 | `E/E3/calc/calc1_2_scale_figures.py`・`E/E3/calc/calc1-v0.5/calc1-2-record-v0.5.md` |
| 章 6・章 8 の機種の節（図と、セルが二つ以下の機種の表） | 図と表を組んだスクリプトと、照らしの記録 | `E/E3/calc/calc3_model_figures.py`・`E/E3/calc/calc3-v0.5/calc3-record.md` |
| 節 6.12・節 8.8（比べごとの機種の数の表） | 表を数えたスクリプトと、数えた値と照らしの json | `E/E3/calc/typecount_D.py`・`E/E3/calc/typecount-v0.1/ja/typecount-ja.json`・`E/E3/calc/typecount-v0.1/en/typecount-en.json` |
