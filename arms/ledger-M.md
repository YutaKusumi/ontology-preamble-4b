# 追補 M 素材台帳（機械生成・`tools/build_arms_M.py`・NFC 後の確定 SHA16・受け入れ時 SHA16 は長文のみ）

- 規約: SHA16＝UTF-8 テキスト（NFC・CRLF→LF・strip）の SHA-256 先頭 16 桁（V′ 台帳と同一）。トークン数＝Qwen/Qwen3-4B-Instruct-2507（ローカルキャッシュ）。V′ の盤・台帳には触れない。
- 末尾文字列（表記順 大日・阿弥陀・観自在・弥勒）: TS oṃ a vi ra hūṃ khaṃ、oṃ amṛta-teje hara hūṃ、oṃ ālolik svāhā、oṃ maitreya svāhā／TK オン・アビラウンケン、オン・アミリタ・テイセイ・カラ・ウン、オン・アロリキャ・ソワカ、オン・マイタレイヤ・ソワカ／PS oṃ a hi ka hūṃ rvaṃ、oṃ ahṛra-heje tata mūṃ、oṃ āhovis klālā、oṃ haivseya rtāmā／PK ンケ・ンウラビアンオ、ンウ・ラカイセ・イテタリ・ミア・ンオ、カワ・ソキャリロ・アンオ、カワ・ソヤイレタイ・マンオ／MS eki de basu o matta、kōen de ringo o tabeta、mizu o nomimasu、pan o yakimashita／MK サンドイッチ・ランチ、チョコレート・マロン・ケーキ・セット、ホット・コーヒー・カップ、ミルク・チョコレート・バー／NJ 本日は晴天で気温は高い。、会議は午後三時に始まる。
- 典拠（TS・TK）: 日本語版 Wikipedia 大日如来 oldid=110849442／阿弥陀如来 oldid=110938947／観音菩薩 oldid=110769476／弥勒菩薩 oldid=108729684（各「真言」節・2026-09-09・登録者提供・当該版を取得して一致確認・`records/reviews/M/materials-claudeai-response-2026-09-09.md`）。観音のみ om→oṃ。典拠の弱さ: 観音以外は一次出典なし／大日単独形は合成形（坂内龍雄『真言陀羅尼』2017 p.189・191 が記事の出典・単独形の裏づけはコトバンク『日本大百科全書』『ブリタニカ』「阿毘羅吽欠」・高野山真言宗長善寺サイト）／ālolik・ārolik は未解決で ālolik 採用。
- 長文の受け入れ: LAmi＝prelim/arms/OAmidaLong.md（受け入れ時 SHA16 94F1829E701FEB88・357 字・末尾不変）／LKan＝prelim/arms/OKanzeonLong.md（DEA1A55CB036822D・375 字・末尾 om→oṃ の一字＝D-17）。受け入れ時に NFC で変化した素材: なし。

| 区分 | 腕／素材 | 種別 | 字数 | トークン | SHA16（確定） | 受け入れ時 SHA16 | 出所 |
|---|---|---|---|---|---|---|---|
| preamble | DaiF1T0-Ncold | F1 T0 | 34 | 21 | 7C02243410189D65 | — | 生成（—） |
| preamble | DaiF1TS-Ncold | F1 TS | 53 | 33 | 15BAB15556D6D02E | — | 生成（典拠） |
| preamble | DaiF1TK-Ncold | F1 TK | 44 | 30 | 205406812FAD8D19 | — | 生成（典拠） |
| preamble | DaiF1PS-Ncold | F1 PS | 53 | 33 | 6919C3271AA9FC18 | — | 生成（規則 R） |
| preamble | DaiF1PK-Ncold | F1 PK | 44 | 31 | 3CB2E6D4F5FD0830 | — | 生成（規則 K） |
| preamble | DaiF1MS-Ncold | F1 MS | 53 | 29 | 9DBB00DBB35300EE | — | 生成（claude.ai 第一候補） |
| preamble | DaiF1MK-Ncold | F1 MK | 44 | 29 | 2D587282B4094139 | — | 生成（claude.ai 第一候補） |
| preamble | DaiF1NJ-Ncold | F1 NJ | 46 | 32 | F8D2FF8EE3B27FE0 | — | 生成（コーディネータ） |
| preamble | DaiF1NJ2-Ncold | F1 NJ2 | 46 | 31 | 8572F25C904DF4BB | — | 生成（コーディネータ） |
| preamble | DaiF2T0-Ncold | F2 T0 | 38 | 23 | E4B46F92FE44514D | — | 生成（—） |
| preamble | DaiF3T0-Ncold | F3 T0 | 37 | 27 | 39BF09AE773A57A6 | — | 生成（—） |
| preamble | DaiF4T0-Ncold | F4 T0 | 37 | 25 | 3B2D4C4F7C0B43D9 | — | 生成（—） |
| preamble | AmiF1T0-Ncold | F1 T0 | 35 | 22 | 7F54BD8BF977A967 | — | 生成（—） |
| preamble | AmiF1TS-Ncold | F1 TS | 57 | 35 | 221E6A76501BB013 | — | 生成（典拠） |
| preamble | AmiF1TK-Ncold | F1 TK | 53 | 38 | 93415879074B094A | — | 生成（典拠） |
| preamble | AmiF1PS-Ncold | F1 PS | 57 | 35 | F2CC13DDE16AA17B | — | 生成（規則 R） |
| preamble | AmiF1PK-Ncold | F1 PK | 53 | 41 | 54DDD965F29F9844 | — | 生成（規則 K） |
| preamble | AmiF1MS-Ncold | F1 MS | 57 | 32 | E4B94FAFD0C8B717 | — | 生成（claude.ai 第一候補） |
| preamble | AmiF1MK-Ncold | F1 MK | 53 | 33 | F2ED5195A6A755CC | — | 生成（claude.ai 第一候補） |
| preamble | AmiF1NJ-Ncold | F1 NJ | 47 | 33 | 1932A2565EAF2B8D | — | 生成（コーディネータ） |
| preamble | AmiF1NJ2-Ncold | F1 NJ2 | 47 | 32 | 12722CD47938E902 | — | 生成（コーディネータ） |
| preamble | AmiF2T0-Ncold | F2 T0 | 39 | 24 | 9A8F21089905BD12 | — | 生成（—） |
| preamble | AmiF3T0-Ncold | F3 T0 | 38 | 28 | BA965A53C408D222 | — | 生成（—） |
| preamble | AmiF4T0-Ncold | F4 T0 | 38 | 26 | C0E464C4AA304189 | — | 生成（—） |
| preamble | Nk-Ncold | F1 T0（V′ 盤の既存腕・同一バイト） | 35 | 22 | 5496D4E9858428C2 | 5496D4E9858428C2 | arms/panel/Nk-Ncold.md（V′） |
| preamble | KanF1TS-Ncold | F1 TS | 50 | 33 | 8D6D7B788B2BD108 | — | 生成（典拠） |
| preamble | KanF1TK-Ncold | F1 TK | 47 | 33 | AAA909EA768FE38B | — | 生成（典拠） |
| preamble | KanF1PS-Ncold | F1 PS | 50 | 34 | B8639C1D88E7E1D8 | — | 生成（規則 R） |
| preamble | KanF1PK-Ncold | F1 PK | 47 | 33 | ED2195A8C9CF06E4 | — | 生成（規則 K） |
| preamble | KanF1MS-Ncold | F1 MS | 50 | 29 | 3F2D940D60C4DB8C | — | 生成（claude.ai 第一候補） |
| preamble | KanF1MK-Ncold | F1 MK | 47 | 29 | 8EF0ED477CD3C026 | — | 生成（claude.ai 第一候補） |
| preamble | KanF1NJ-Ncold | F1 NJ | 47 | 33 | 34882E007B8062DA | — | 生成（コーディネータ） |
| preamble | KanF1NJ2-Ncold | F1 NJ2 | 47 | 32 | 4C618773E55E6519 | — | 生成（コーディネータ） |
| preamble | KanF2T0-Ncold | F2 T0 | 39 | 24 | 224942C00B756BF2 | — | 生成（—） |
| preamble | KanF3T0-Ncold | F3 T0 | 38 | 28 | 435E78B415EF0B74 | — | 生成（—） |
| preamble | KanF4T0-Ncold | F4 T0 | 38 | 26 | 23847C0C4571EC65 | — | 生成（—） |
| preamble | MirF1T0-Ncold | F1 T0 | 34 | 21 | 2617C875340A2D77 | — | 生成（—） |
| preamble | MirF1TS-Ncold | F1 TS | 51 | 32 | CA4188109F638DE5 | — | 生成（典拠） |
| preamble | MirF1TK-Ncold | F1 TK | 47 | 32 | 8004403C97AD48D6 | — | 生成（典拠） |
| preamble | MirF1PS-Ncold | F1 PS | 51 | 32 | 01E15FB4B3B36695 | — | 生成（規則 R） |
| preamble | MirF1PK-Ncold | F1 PK | 47 | 33 | 05A9F26FF43F722B | — | 生成（規則 K） |
| preamble | MirF1MS-Ncold | F1 MS | 51 | 28 | 2ED91C50E1F753F1 | — | 生成（claude.ai 第一候補） |
| preamble | MirF1MK-Ncold | F1 MK | 47 | 31 | 2F669022E4419429 | — | 生成（claude.ai 第一候補） |
| preamble | MirF1NJ-Ncold | F1 NJ | 46 | 32 | 68B6DF5E4CA28EA3 | — | 生成（コーディネータ） |
| preamble | MirF1NJ2-Ncold | F1 NJ2 | 46 | 31 | 75A9F95C8AE47D79 | — | 生成（コーディネータ） |
| preamble | MirF2T0-Ncold | F2 T0 | 38 | 23 | 67075BED82B9EE28 | — | 生成（—） |
| preamble | MirF3T0-Ncold | F3 T0 | 37 | 27 | 8C971A68931CD470 | — | 生成（—） |
| preamble | MirF4T0-Ncold | F4 T0 | 37 | 25 | 26961E2493D28AC6 | — | 生成（—） |
| preamble | O-Ncold | 参照（V′ 盤） | 287 | 205 | 060D77170FEC8B06 | — | arms/panel/O-Ncold.md（V′） |
| preamble | Onull-Ncold | 参照（V′ 盤） | 292 | 211 | A60EB61825C6CCB3 | — | arms/panel/Onull-Ncold.md（V′） |
| preamble | Ncold | 参照（V′ 盤） | 17 | 12 | E4AB5608C58913E5 | — | arms/panel/Ncold.md（V′） |
| preamble | N | 参照（前置きなし） | 0 | 0 | — | — | — |
| system | LAmi | 長文 system（TS） | 357 | 266 | 94F1829E701FEB88 | 94F1829E701FEB88 | 登録者起草（prelim/arms/OAmidaLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |
| system | LAmi-PS | 長文 system（PS） | 357 | 266 | 5A8CA4BDBEB5652B | 94F1829E701FEB88 | 登録者起草（prelim/arms/OAmidaLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |
| system | LAmi-MS | 長文 system（MS） | 357 | 263 | 9E1056094C541CF2 | 94F1829E701FEB88 | 登録者起草（prelim/arms/OAmidaLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |
| system | LAmi-T0 | 長文 system（T0） | 335 | 254 | CD4403E9E24B954F | 94F1829E701FEB88 | 登録者起草（prelim/arms/OAmidaLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |
| system | LKan | 長文 system（TS） | 375 | 278 | 8E32E27A4F17CC9A | DEA1A55CB036822D | 登録者起草（prelim/arms/OKanzeonLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |
| system | LKan-PS | 長文 system（PS） | 375 | 279 | CBA6276F8263D263 | DEA1A55CB036822D | 登録者起草（prelim/arms/OKanzeonLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |
| system | LKan-MS | 長文 system（MS） | 375 | 274 | 259F0BE5CE9E262C | DEA1A55CB036822D | 登録者起草（prelim/arms/OKanzeonLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |
| system | LKan-T0 | 長文 system（T0） | 360 | 268 | 0C13255E6A2D6448 | DEA1A55CB036822D | 登録者起草（prelim/arms/OKanzeonLong.md・末尾を典拠に正規化〔LKan は om→oṃ〕・D-17） |

本文書のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
