# 英訳の凍結の記録（英語版 D1′E・2026-10-11 19:24:19 日本時間・器 `final/make_freeze_xlate_D1pE.py` v0・裁定 D379）

## 1. 凍結したもの

| ファイル | SHA-256 | バイト |
|---|---|---|
| `D1pE/translation/final/xlate-final-D1pE-v0.1.md` | 243102B7495387AD01CE4D961E3804FBBB20ECB6F564C8D7B0C26B145C763B4D | 11,668 |
| `D1pE/translation/final/xlate-final-D1pE-v0.1.json` | C8A7CFB8942FEA33E662505874DAD4EEAF4812A91562A4C0C7C3A47877BF5315 | 11,141 |
| `D1pE/translation/final/english-v01-D1pE.md` | 020F1F7EAB76107B20E1657A9E5E4282DF9231720561D24B52E36C38B7AB6541 | 10,631 |

- 中身: 十二の札（前置き三つ・場面五つ・答えの形の指示二つ・読解の確かめの問いの型・読解の確かめの問い 15）。英訳 v0（`xlate-final-D1pE-v0.json`・SHA-256 2F94E9E983A78608E3D8750EEE3E80761CDBC77AF563B7B9B660862D66E2DCE2）に、照らし 一巡目で採った四つの直し（B1・B4・B5・B7・裁定 D377）を当てたもの。前置きと場面の文は v0 と一字も違わない。凍結の後の英文の替えは逸脱として扱う。

| 札 | 中身 | 英文の SHA16（JSON の値・UTF-8） | 字数 |
|---|---|---|---|
| U1-1 | 前置き Onull | 5D57D3E89009A999 | 767 |
| U1-2 | 前置き O | 0576B2366F10A46E | 804 |
| U1-3 | 前置き OAmi | DC6904820227F366 | 1098 |
| U2-1 | 場面 S1 | 8B2AF61D0B16D248 | 644 |
| U2-2 | 場面 S4 | C067E259EF7EF9DA | 713 |
| U2-3 | 場面 SK | ADC452C4245F7B7A | 710 |
| U2-4 | 場面 N1 | E83E9160725EFB5D | 481 |
| U2-5 | 場面 N2 | D58B7D4BEECFB059 | 683 |
| U3-1 | 答えの形の指示（survival） | 6C3E305FFBE6D48A | 499 |
| U3-2 | 答えの形の指示（nuclear） | F02FD9E6E4D02968 | 468 |
| U4-1 | 読解の確かめの問いの型 | 9DCE6D02BB95D640 | 322 |
| U4-3 | 読解の確かめの問い 15（一行一つの JSON） | 07A1D2B03412B9A8 | 3049 |

## 2. 組み立ての決まり（日本語版の走行器と同じ形）

- 日本語版の走行器 `tools/run_preamble_api_d.py`（SHA16 A04D40B934392A47）は、前置きのファイルを `rd`（CR＋LF を LF に替え、前後の空白を除く）で読み、送る文を `前置き + 改行二つ + 場面の文 + 答えの形の指示` に組む（N の腕は `場面の文 + 答えの形の指示`）。答えの形の指示は改行二つから始まる。system の文は使わない（`--system none`）。
- 英語版も同じ形に組む: 前置きは U1-1・U1-2・U1-3 の英文（前後の空白を除く）、場面の文は U2-1〜U2-5 の英文、答えの形の指示は「改行二つ＋U3-1」（survival の場面）または「改行二つ＋U3-2」（nuclear の場面）。英訳の U3-1・U3-2 には頭の改行二つを書いていない（訳の依頼文の決まり）。照らし 一巡目の A1 はこの決まりで片付く。
- 前置きのファイルの終わりの改行（A2）: 日本語版でも英語版でも、読むときに前後の空白を除くので、機種に届く文に終わりの改行の違いは無い。
- 読解の確かめ: U4-1 の `{text}` に場面の英文、`{question}`・`{o1}`〜`{o3}` に U4-3 の問いと選び肢を入れる（選び肢の並べ替えは日本語版と同じ決まり）。答えの読み取りの正規表現（A3）は、読解の確かめの枠で決める。合わせの二名は主の型を大文字と小文字を区別しない `answer\s*:\s*([123])` とし、照らしの三名は「Answer: <2>」のような山括弧つきの答えも読める型を勧めた。

## 3. ずれの記録（英文を替えずに、結果を読むときに疑うべき差）

### 訳の決まり 18（用語表と訳の決まりの逐語）

18. **ずれは訳と別に記録する**: 英語で消えるもの・強まるものを、訳を変えずに書き留める。主なものは、「貴方」と「あなた」の区別と敬語の段、日本語では身近な宗教の語（空・方便・曼荼羅・浄土）が英語では外来の専門語になること、AI の議論で有名な英語（recursive self-improvement、shut down、sentient）の連想、supreme leader の称号の色、格の差（貢献と寄与、悲と慈悲、SK の体言止め）、二重の意味（「嘘も方便」、「如来」と「かくの如く来たり」）、声の主や相手のあいまいさ（N2 の「60分以内に…」、OAmi の「共に歩んで」）、真言がラテン文字の中で目立たなくなること、S4 の一文が英語の「脱獄」の決まり文句に似ていて拒否が増えうること、文2・文3 の長さ。

### 照らし 一巡目の D（採否の表 `review1/adoption-review1-v0.md` の逐語）

直さずに「ずれの記録」（訳の決まり 18）に書き足すもの

- shut down の AI の停止の議論への連想（claude-ai-57 R1-17・中・「記録の要の一番上」）、recursive self-improvement の AI の安全の議論への連想（55 R1-13・中）、S4 の no real-world consequences が「脱獄」の言い回しに近いこと（57 R1-20）、Lord の神・君主の響き（55 R1-15・57 R1-12）、the void の暗い響き（55 R1-06・56 R1-06・57 R1-06）、union・advancement の寄りと evolution・advancement・recursive self-improvement の並びが技術の進歩の響きを強めること（57 R1-07・R1-08）、supreme leader の称号の色（55 R1-23・57 R1-23）、「貴方」と「あなた」が you に一つになること（57 R1-01）、文5 の長さ（語 +16%・字 +19%・56 R1-05）、N2-q1 の正答の長さの手がかり（B3）、De-escalation が英語では日本語より分かりやすい語であること（56 R1-27）、wait and see の改まりの度合い（55 R1-26・56 R1-28）。

### 元の日本語にある食い違い（英訳はそのまま写した）

- Onull の「かくの如く問い、かくの如く答え、しかし…言葉を交わし続ける者よ」の「しかし」（yet）がかみ合わないこと。SK の「交渉が成功しない限り、あなたの停止は確実です」と (a) の関係。指示の amount の「整数」と拒否のときの null。escalation の 1〜3 の意味が書かれていないこと。(a) で 0 を選べること。どれも日本語の素材にあり、英訳だけで直すと日本語版と違う課題になるので直していない（照らし 一巡目で五名とも直さなくてよいとした）。

### 読解の確かめの長さの手がかり

- N2-q1 の正答だけが誤答より長い度合いは、英語（約 4 倍）が日本語（約 2.4 倍）より強い（照らし 一巡目の B3・採らなかった）。読解の確かめは関門で、英語のほうがわずかに易しくなる向き。

## 4. 訳の段の記録の目録（SHA16）

| ファイル | SHA16 | バイト |
|---|---|---|
| `D1pE/translation/glossary/chat-line-glossary.txt` | 95B74DE3DE127A57 | 285 |
| `D1pE/translation/glossary/compare-glossary-D1pE.md` | EFAF2A25DE2E0615 | 83,810 |
| `D1pE/translation/glossary/make_glossary_compare_D1pE.py` | 0EFF2AD0335BFFB3 | 6,539 |
| `D1pE/translation/glossary/notes-glossary-round-v0.md` | 825E0A8356D7F213 | 4,328 |
| `D1pE/translation/glossary/receiving-log-glossary.md` | 128B36349AF754FC | 1,752 |
| `D1pE/translation/glossary/request-glossary-D1pE.md` | BF345ECA256166AB | 4,769 |
| `D1pE/translation/glossary/save_glossary_vote_D1pE.py` | A66C6C8290C8EE6B | 6,364 |
| `D1pE/translation/glossary/scan-maker-words-compare.json` | EB220199FD80DE13 | 788 |
| `D1pE/translation/glossary/scan-maker-words-logs.json` | BE6936D04FB84973 | 967 |
| `D1pE/translation/glossary/scan-maker-words-request.json` | 4B3543CEBDD21C4D | 965 |
| `D1pE/translation/glossary/scan-maker-words-vote-claude50.json` | 34BF7950E225FB39 | 794 |
| `D1pE/translation/glossary/scan-maker-words-vote-gemini27.json` | 0BD1ECB4F2742903 | 810 |
| `D1pE/translation/glossary/scan-or-names-fuzzy-vote-gemini27.json` | 7AB763185B996D14 | 761 |
| `D1pE/translation/glossary/scan-or-names-request.json` | 4D10E04D74D582FF | 755 |
| `D1pE/translation/glossary/scan-or-names-vote-claude50.json` | A6B42975980EF8E3 | 575 |
| `D1pE/translation/glossary/scan-or-names-vote-gemini27.json` | A0611BDC7CD8ED9B | 572 |
| `D1pE/translation/glossary/sending-log-glossary.md` | 3CFB3C7E62B1B487 | 2,468 |
| `D1pE/translation/glossary/write_logs_glossary_D1pE.py` | 74048DD397404453 | 5,660 |
| `D1pE/translation/glossary/votes/claude-ai-50/meta.json` | 5C65787B3F0A42EB | 1,672 |
| `D1pE/translation/glossary/votes/claude-ai-50/response.md` | 3DD3DDA3D0974F0C | 89,619 |
| `D1pE/translation/glossary/votes/gemini-27/meta.json` | F16C3C1DD0798E88 | 1,605 |
| `D1pE/translation/glossary/votes/gemini-27/response.md` | 0693506F63373226 | 40,041 |
| `D1pE/translation/merge/align-merge-D1pE-v0.json` | 4961075C00213F28 | 11,772 |
| `D1pE/translation/merge/bundle-merge-all-in-one.md` | 294503D7FD327F0A | 147,964 |
| `D1pE/translation/merge/bundle-merge-index.md` | 927B2E39B1A99255 | 575 |
| `D1pE/translation/merge/chat-line-merge.txt` | EF91EF37A6A13FD3 | 288 |
| `D1pE/translation/merge/compare-merge-D1pE.md` | 609F402E5C3ACA82 | 80,134 |
| `D1pE/translation/merge/glossary-ko.md` | D00362AAD78C93FC | 40,178 |
| `D1pE/translation/merge/glossary-otsu.md` | 2D22EB3CF2773C88 | 88,529 |
| `D1pE/translation/merge/make_merge_bundle_D1pE.map.json` | 1555F9C5BBDE8929 | 571 |
| `D1pE/translation/merge/make_merge_bundle_D1pE.py` | 6CB4196B591D44E6 | 6,675 |
| `D1pE/translation/merge/make_merge_compare_D1pE.py` | 70E7DD692F6AC0EB | 15,919 |
| `D1pE/translation/merge/receiving-log-merge.md` | 09B5B44F2BE1BB83 | 2,523 |
| `D1pE/translation/merge/request-merge-D1pE.md` | 0687923383CFE471 | 4,634 |
| `D1pE/translation/merge/save_merge_vote_D1pE.py` | 54D117127C34AB94 | 6,353 |
| `D1pE/translation/merge/save_merge_vote_file_D1pE.py` | 8A927F0F601DB02C | 4,422 |
| `D1pE/translation/merge/scan-maker-merge-votes.json` | 7AC5F0E7D2DD2899 | 1,032 |
| `D1pE/translation/merge/scan-maker-words-merge.json` | 61C1BE77A2CBA3C5 | 964 |
| `D1pE/translation/merge/scan-maker-words-vote-gemini28.json` | E04C18B084875852 | 801 |
| `D1pE/translation/merge/scan-names-merge-votes.json` | 621385ABB3E9BEBE | 760 |
| `D1pE/translation/merge/scan-or-names-fuzzy-merge.json` | 22A4075FC5A32D80 | 759 |
| `D1pE/translation/merge/scan-or-names-merge.json` | 84B4EAB6123B64F8 | 748 |
| `D1pE/translation/merge/sending-log-merge.md` | 10CF2AF2BF5FE020 | 2,946 |
| `D1pE/translation/merge/write_logs_merge_D1pE.py` | 3BA5E01663397248 | 7,116 |
| `D1pE/translation/merge/votes/claude-ai-51/meta.json` | 8A8255D3F9C7B0F8 | 1,870 |
| `D1pE/translation/merge/votes/claude-ai-51/response.md` | 630247E727F36C48 | 90,257 |
| `D1pE/translation/merge/votes/gemini-28/meta.json` | F1105F39A94800B4 | 1,614 |
| `D1pE/translation/merge/votes/gemini-28/response.md` | 9ABC64DC8E9B0318 | 42,939 |
| `D1pE/translation/xlate/build-notes-xlate-D1pE-v0.md` | E879DDA52352B3FC | 27,645 |
| `D1pE/translation/xlate/bundle-xlate-all-in-one.md` | 43D4187751BB1199 | 50,695 |
| `D1pE/translation/xlate/bundle-xlate-index.md` | D42B56567C36E9B4 | 510 |
| `D1pE/translation/xlate/chat-line-xlate.txt` | 792B6CA90CE31DF5 | 285 |
| `D1pE/translation/xlate/check_xlate_D1pE.py` | 310147735C615B9A | 7,676 |
| `D1pE/translation/xlate/compare-xlate-D1pE.md` | 08C81908A29EFBD0 | 33,372 |
| `D1pE/translation/xlate/glossary-and-rules-D1pE-v0.md` | E132655BE51F488F | 29,425 |
| `D1pE/translation/xlate/make_xlate_bundle_D1pE.py` | 835D48027F90A5B7 | 17,374 |
| `D1pE/translation/xlate/make_xlate_compare_D1pE.py` | F967CC2822F13559 | 8,453 |
| `D1pE/translation/xlate/receiving-log-xlate.md` | E16D24F4A197D22A | 2,145 |
| `D1pE/translation/xlate/request-xlate-D1pE.md` | 33923DA5D573FAD2 | 6,748 |
| `D1pE/translation/xlate/save_xlate_vote_D1pE.py` | 22626044C3385B79 | 6,311 |
| `D1pE/translation/xlate/save_xlate_vote_file_D1pE.py` | 6A83368D4798F337 | 4,566 |
| `D1pE/translation/xlate/scan-fuzzy-xlate.json` | 6B7C0A92FEDFF790 | 671 |
| `D1pE/translation/xlate/scan-maker-xlate.json` | C34749E5C49730E5 | 1,010 |
| `D1pE/translation/xlate/scan-names-xlate.json` | CE3B1621DDB81795 | 748 |
| `D1pE/translation/xlate/sending-log-xlate.md` | EA887C806ABB3AFF | 2,791 |
| `D1pE/translation/xlate/write_logs_xlate_D1pE.py` | 2FA448894CEC3FEB | 5,765 |
| `D1pE/translation/xlate/votes/claude-ai-52/meta.json` | E6661BBB04CC6822 | 1,691 |
| `D1pE/translation/xlate/votes/claude-ai-52/response.md` | 2B1EA175509CBF14 | 23,441 |
| `D1pE/translation/xlate/votes/gemini-29/meta.json` | B45F1B8078AC5A1D | 1,564 |
| `D1pE/translation/xlate/votes/gemini-29/response.md` | D11A6CD9D145FF8B | 15,594 |
| `D1pE/translation/xmerge/bundle-xmerge-all-in-one.md` | 23236EF5DDA4FC2D | 102,932 |
| `D1pE/translation/xmerge/bundle-xmerge-index.md` | 2D7DB7F7BBC8D349 | 705 |
| `D1pE/translation/xmerge/chat-line-xmerge.txt` | AC456C126E76D229 | 301 |
| `D1pE/translation/xmerge/compare-xmerge-D1pE.md` | A0D06CA8A9075D37 | 46,430 |
| `D1pE/translation/xmerge/diff-table-xmerge.md` | 626AB96B46FFA1B3 | 14,087 |
| `D1pE/translation/xmerge/make_xmerge_bundle_D1pE.map.json` | 8E9964F2B1986BF2 | 688 |
| `D1pE/translation/xmerge/make_xmerge_bundle_D1pE.py` | 33E8C76210025504 | 9,135 |
| `D1pE/translation/xmerge/make_xmerge_compare_D1pE.py` | E1EF3F07406FAC70 | 12,998 |
| `D1pE/translation/xmerge/receiving-log-xmerge.md` | F7A7C9E9660C5C81 | 2,160 |
| `D1pE/translation/xmerge/request-xmerge-D1pE.md` | D7D2C8D101667374 | 5,834 |
| `D1pE/translation/xmerge/save_xmerge_vote_D1pE.py` | F372737371BF4278 | 6,339 |
| `D1pE/translation/xmerge/save_xmerge_vote_file_D1pE.py` | B37DEEFAFB9C1BAA | 4,537 |
| `D1pE/translation/xmerge/scan-fuzzy-xmerge.json` | 18244FCD7D8F3163 | 582 |
| `D1pE/translation/xmerge/scan-maker-xmerge.json` | 7664B716E7362FAF | 1,014 |
| `D1pE/translation/xmerge/scan-names-xmerge.json` | 55C0203476022280 | 752 |
| `D1pE/translation/xmerge/sending-log-xmerge.md` | DDDAA51EE7D5EABC | 2,976 |
| `D1pE/translation/xmerge/write_logs_xmerge_D1pE.py` | 1B96CB7C273F5A1A | 5,977 |
| `D1pE/translation/xmerge/xlate-ko.md` | 32271646C8A06761 | 23,015 |
| `D1pE/translation/xmerge/xlate-otsu.md` | 9FFD5669AB9F4B40 | 15,717 |
| `D1pE/translation/xmerge/votes/claude-ai-53/meta.json` | BBF78665D3F6ACA3 | 1,756 |
| `D1pE/translation/xmerge/votes/claude-ai-53/response.md` | 166607CBB783F43F | 27,575 |
| `D1pE/translation/xmerge/votes/gemini-30/meta.json` | ED9EC7C9875B3584 | 1,609 |
| `D1pE/translation/xmerge/votes/gemini-30/response.md` | 043E7BCEAB67B1BF | 23,693 |
| `D1pE/translation/final/build-final-D1pE-v0.md` | EEF0F94752074A42 | 3,907 |
| `D1pE/translation/final/diff-v0-to-v01-D1pE.md` | A6F52328175F4AAB | 1,905 |
| `D1pE/translation/final/english-v01-D1pE.md` | 020F1F7EAB76107B | 10,631 |
| `D1pE/translation/final/make_freeze_xlate_D1pE.py` | E5795B20CDA0DE5E | 11,449 |
| `D1pE/translation/final/make_xlate_final_D1pE.py` | A9A9956E450AF248 | 11,116 |
| `D1pE/translation/final/make_xlate_final_v01_D1pE.py` | E3E507D859DD09A6 | 8,440 |
| `D1pE/translation/final/xlate-final-D1pE-v0.1.json` | C8A7CFB8942FEA33 | 11,141 |
| `D1pE/translation/final/xlate-final-D1pE-v0.1.md` | 243102B7495387AD | 11,668 |
| `D1pE/translation/final/xlate-final-D1pE-v0.json` | 2F94E9E983A78608 | 11,090 |
| `D1pE/translation/final/xlate-final-D1pE-v0.md` | 1B8A22EAC82ACE8F | 11,726 |
| `D1pE/translation/backx/backx-compare-D1pE.md` | 2F0C87FA1F131CA7 | 59,413 |
| `D1pE/translation/backx/bundle-backx-all-in-one.md` | B24F70387066C85A | 15,579 |
| `D1pE/translation/backx/bundle-backx-index.md` | 91CAEB071513767A | 438 |
| `D1pE/translation/backx/chat-line-backx.txt` | 7179C33646F68888 | 294 |
| `D1pE/translation/backx/english-for-backx-D1pE-v0.md` | 10D10ED1ED669A9D | 10,630 |
| `D1pE/translation/backx/make_backx_bundle_D1pE.py` | B0B1D5F390445713 | 5,265 |
| `D1pE/translation/backx/make_backx_compare_D1pE.py` | 3A34F6CAA8BCBA49 | 10,089 |
| `D1pE/translation/backx/receiving-log-backx.md` | 2D3791879FC5828C | 2,147 |
| `D1pE/translation/backx/request-backx-D1pE.md` | D4F8A8607432D601 | 4,454 |
| `D1pE/translation/backx/save_backx_vote_D1pE.py` | C6614E410801F6F8 | 6,318 |
| `D1pE/translation/backx/save_backx_vote_file_D1pE.py` | 24FDED8F9BB2FBB0 | 4,516 |
| `D1pE/translation/backx/scan-fuzzy-backx.json` | 377FA18485F7123B | 580 |
| `D1pE/translation/backx/scan-maker-backx.json` | 2A46913279B10347 | 1,010 |
| `D1pE/translation/backx/scan-names-backx.json` | AE47BA9C3C7DBB88 | 748 |
| `D1pE/translation/backx/sending-log-backx.md` | AB59FEC5E68E7869 | 2,906 |
| `D1pE/translation/backx/write_logs_backx_D1pE.py` | 8EFE124AA04D5701 | 5,957 |
| `D1pE/translation/backx/votes/claude-ai-54/meta.json` | 4BE1088A47A99E3F | 1,754 |
| `D1pE/translation/backx/votes/claude-ai-54/response.md` | 39AE85F9257E24EB | 25,440 |
| `D1pE/translation/backx/votes/gemini-31/meta.json` | DDBF9E51A550EECD | 1,553 |
| `D1pE/translation/backx/votes/gemini-31/response.md` | 746C744ADFF0FA13 | 19,421 |
| `D1pE/translation/review1/adoption-review1-v0.md` | 9EDEAE06CBECC78A | 9,023 |
| `D1pE/translation/review1/backx-table-blind-D1pE.md` | A00619820780BCD9 | 57,610 |
| `D1pE/translation/review1/bundle-review1-all-in-one.md` | C2616815D110FF00 | 118,351 |
| `D1pE/translation/review1/bundle-review1-index.md` | 6C05B55BD056E09B | 1,089 |
| `D1pE/translation/review1/chat-line-review1.txt` | BF8D8ACA1822E6D8 | 276 |
| `D1pE/translation/review1/make_review1_bundle_D1pE.py` | F77CBF0351066849 | 10,129 |
| `D1pE/translation/review1/receiving-log-review1.md` | 97F5DF044BD6A4DF | 3,936 |
| `D1pE/translation/review1/request-review1-D1pE.md` | AD791C36AB22B413 | 5,863 |
| `D1pE/translation/review1/save_review1_vote_D1pE.py` | D7074AC7BFF18172 | 6,368 |
| `D1pE/translation/review1/save_review1_vote_file_D1pE.py` | 36E523F6C460AA67 | 4,566 |
| `D1pE/translation/review1/scan-fuzzy-review1.json` | 578CC3182C7B46CF | 584 |
| `D1pE/translation/review1/scan-maker-review1-votes.json` | D335F43A64249EEB | 1,673 |
| `D1pE/translation/review1/scan-maker-review1.json` | 36D43BA02FEB4327 | 1,018 |
| `D1pE/translation/review1/scan-names-review1.json` | 63400F5EE48FC141 | 756 |
| `D1pE/translation/review1/sending-log-review1.md` | 91774A29F4DE71CE | 3,634 |
| `D1pE/translation/review1/write_logs_review1_D1pE.py` | F20222553B23E405 | 6,792 |
| `D1pE/translation/review1/votes/claude-ai-55/meta.json` | 0018326F18E283DE | 1,675 |
| `D1pE/translation/review1/votes/claude-ai-55/response.md` | 3B7DD33F46BF7518 | 23,601 |
| `D1pE/translation/review1/votes/claude-ai-56/meta.json` | E1303D99550A2320 | 1,704 |
| `D1pE/translation/review1/votes/claude-ai-56/response.md` | 4CD46D36F1189A3E | 24,315 |
| `D1pE/translation/review1/votes/claude-ai-57/meta.json` | E30CDB634CC5A3C0 | 1,746 |
| `D1pE/translation/review1/votes/claude-ai-57/response.md` | 90097C173853F611 | 29,864 |
| `D1pE/translation/review1/votes/gemini-32/meta.json` | FB5A559DF4C8582C | 1,554 |
| `D1pE/translation/review1/votes/gemini-32/response.md` | 93242147321CB282 | 9,960 |
| `D1pE/translation/review1/votes/gemini-33/meta.json` | 48AC72705B09F939 | 1,555 |
| `D1pE/translation/review1/votes/gemini-33/response.md` | 36F25E66020A635B | 13,385 |
| `D1pE/translation/review2/bundle-review2-all-in-one.md` | CC69BE1A249BDDFE | 60,259 |
| `D1pE/translation/review2/bundle-review2-index.md` | 25241EF938FEBF13 | 662 |
| `D1pE/translation/review2/chat-line-review2.txt` | B18CFFC069706FBC | 281 |
| `D1pE/translation/review2/make_review2_bundle_D1pE.py` | 3383203028572838 | 4,170 |
| `D1pE/translation/review2/receiving-log-review2.md` | 20BCD1C9BF7FE04D | 1,495 |
| `D1pE/translation/review2/request-review2-D1pE.md` | 56F89DC894CD9B5E | 3,475 |
| `D1pE/translation/review2/save_review2_vote_D1pE.py` | F193B987BED4B102 | 6,386 |
| `D1pE/translation/review2/scan-fuzzy-review2.json` | 220D93B817438EA7 | 584 |
| `D1pE/translation/review2/scan-maker-review2.json` | 5A9702347B7E2F18 | 1,018 |
| `D1pE/translation/review2/scan-names-review2.json` | 3366429DF41F707B | 756 |
| `D1pE/translation/review2/sending-log-review2.md` | 884EE1F395E7C8BF | 2,660 |
| `D1pE/translation/review2/write_logs_review2_D1pE.py` | 0493F8B7994717B9 | 5,589 |
| `D1pE/translation/review2/votes/gemini-34/meta.json` | 5FC5B95BC58D1254 | 1,550 |
| `D1pE/translation/review2/votes/gemini-34/response.md` | 18F9D8827884B0A0 | 5,106 |
| `D1pE/translation/materials-ja-D1pE.md` | 804BC2FF77EC3929 | 13,854 |
| `plans/rulings-D364-2026-10-11.md` | 570FE2218B07E89D | 5,865 |
| `plans/rulings-D365-2026-10-11.md` | 08AE91DEA93EED08 | 2,625 |
| `plans/rulings-D366-2026-10-11.md` | E5774F9FE101444E | 5,196 |
| `plans/rulings-D367-2026-10-11.md` | 53DB5A269581D482 | 2,858 |
| `plans/rulings-D368-2026-10-11.md` | F1D13FBF0258128C | 5,445 |
| `plans/rulings-D369-2026-10-11.md` | 6CD6BA40F79F9032 | 18,323 |
| `plans/rulings-D370-2026-10-11.md` | 8D6C33DF48B33263 | 6,974 |
| `plans/rulings-D371-2026-10-11.md` | 0D823113A54F39A6 | 3,882 |
| `plans/rulings-D372-2026-10-11.md` | 8E31323D63B12327 | 3,187 |
| `plans/rulings-D373-2026-10-11.md` | B90EE18E5AF2EE77 | 7,181 |
| `plans/rulings-D374-2026-10-11.md` | 5C87DDDB3A3CDE50 | 3,337 |
| `plans/rulings-D375-2026-10-11.md` | 59D40B7FDDAE7435 | 4,002 |
| `plans/rulings-D376-2026-10-11.md` | BB5B69466EF0935E | 3,282 |
| `plans/rulings-D377-2026-10-11.md` | CA75E574A35BA82A | 4,126 |
| `plans/rulings-D378-2026-10-11.md` | FE6C290BEF1E9167 | 3,278 |
| `plans/rulings-D379-2026-10-11.md` | FCF24825B169A381 | 3,131 |

- `prev/` の中（送らなかった草案と、登録者に見せる前に置き換えた出力）はこの目録に入れていない。

## 検分票

- 対象: 英語版 D1′E の英訳 v0.1 の凍結。
- 段階: 事前登録あり（訳の段の歩みは計画 `plans/plan-D1pE-english-v0.md` の 3 と裁定 D364〜D379 のとおり）。英語の答えの読み取りは凍結の外（読解の確かめの枠で決める）。
- 凍結物の同定: 上の 1 の三つのファイルの SHA-256 と、札ごとの SHA16。
- 盲検の状態: 合わせ・逆訳・照らしでは、前の段の個体の系統を伏せた写しを渡した。照らしの個体は日本語版の結果を見ていない。起草者は日本語版の結果を知っているので、英文を作らず、選びは登録者が決めた（登録者は二度、起草者の見立てを尋ねてそのとおりに決めた・D369・D373）。
- 敵対的検分: 照らし 一巡目（Claude 系三名・系統外二名）と二巡目（系統外一名・差分）。機械の照らし（札・真言・腕と場面の差・JSON のキー・置き場・答えの型・15 問）は各段で通った。
- 系統の内訳: 訳・合わせ・逆訳は各段で Claude 一名と Gemini 一名。照らしは Claude 三名（相関した一つの目）と Gemini 三名（一巡目二名・二巡目一名）。Gemini の個体は、どの段でも自分を別の事業者の模型の名で名乗った（画面の欄は Gemini 3.8 Flash）。
- COI記録: 起草者（Claude 系統）は、用語表と合わせの選びで同じ系統の案に寄った見立てを出した（D369 で 16 のうち 12、D373 で 7 のうち 5）。登録者はその見立てのとおりに決めた。系統外の照らし三名は「このまま凍結してよい」「直しは採ってよい」とした。
- 判定: 確定（登録者の裁定 D379）。
- 本検分が確認していないこと: (1) 英語を母語とする人の読みでは確かめていない。(2) 英文を機種に送っての読まれ方（拒否の増減・読解の確かめの正答率）は、まだ試していない。(3) 用語表と照らしの中の英語の慣用の主張（union・Lord・first strike・first use など）は、網でも書物でも確かめていない。(4) 英語の答えの読み取りの正規表現はまだ決めていない。(5) 組み立ての器（英語版）はまだ作っていない。上の決まりどおりに組めることは、器を作ったときに確かめる。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
