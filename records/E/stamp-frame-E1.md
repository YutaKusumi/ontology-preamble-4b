# 段階 E の枠（E1）の刻印（2026-10-14 10:10:57 日本時間・器 `E/make_stamp_frame_E1.py`）

- 何か: 段階 E（統合と正本）の枠を、封を開けた後の探索（E2）・新しい計算・論文の起草の前に刻んだ記録。枠の本文は伏せ、SHA-256 だけをこの置き場に置く（枠 §3-7）。
- 刻んだ版: 枠の草案6（内部の置き場の `E/00-frame-E-draft6.md`）。枠は、一巡の検分（五名）と三度の差分の確かめ（八票・最後は五名）を経た。草案5 から草案6 への差分は登録者が確かめた（外の確かめは行っていない）。
- 公開の約束: 枠の本文と、下の表で「刻んだバイトのまま公開する」としたファイルは、遅くとも論文の公開（段階 E の E6）と同時に、刻んだバイトのまま公開する。「公開しない」としたファイルは、名と SHA-256 だけをこの記録に残す（二つの集計の器は、E6 の前に名を伏せた写しを公開するかを登録者に伺う・その写しは下の SHA-256 と合わない）。「公開済み」のファイルは、この置き場の同じ名のファイル。
- 次の push: E2 の器が台帳を開ける前に書く一覧（器の元の文の SHA-256・器が読む部品の SHA-256・Python と unicodedata の版・型ごとの対象・抜き取りの並び・組んだ型の並び・開ける台帳の SHA-256・升ごとの写し返しの一覧の作り直しの照らし）の SHA-256 を、台帳を開ける前にこの置き場に push する（枠 §3-7）。二つの push の許しは、刻むときに一度に伺う。
- 確かめられること: このファイルを足したコミットが、E2 の一覧の SHA-256 を足すコミットの祖先であること（main の上の順）と、後で公開するファイルの SHA-256 が下の値と同じこと。台帳を開けた時は当事者の申告による。
- 刻む前の照らし: 枠の本文と、刻んだバイトのまま公開するとしたファイル（8）と、このファイルと commit の文に、名・作り手の語・鍵・禁じる言い換えの照らしを当てた（結果は commit の文と内部の照らしの記録）。起草者は、枠の本文（草案5 の全文と草案6 への差分）と、刻んだバイトのまま公開するとしたファイルを目で読んだ。

## 枠

| 置き場 | SHA-256（バイトのまま） | SHA-256（行末を LF にそろえた値） | 公開の形 |
|---|---|---|---|
| `E/00-frame-E-draft6.md`（内部） | AB7491FF30074FBD43498F10C61BEBFA288D69D78719F19F2899EB55DDFD64CC | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |

## 枠が SHA16 で指すファイル

| 置き場 | 枠の中の SHA16 | SHA-256（バイトのまま） | SHA-256（行末を LF にそろえた値） | 公開の形 |
|---|---|---|---|---|
| `E/00-frame-E-draft5.md`（内部） | 19DD6F1DC7E4565A | 19DD6F1DC7E4565AD52879A12F8B2776563F276433F0CE4B6639A5FA57584A2C | 同じ | 公開しない（名と SHA-256 だけを残す） |
| `E/reviews/frame-diff3/adoption-frame-diff3-v0.md`（内部） | A82584E76B546B99 | A82584E76B546B99BE5DF301BA936C3EDE949B32249E0A5E49B2B930BB6A9286 | 同じ | 公開しない（名と SHA-256 だけを残す） |
| `plans/rulings-D431-2026-10-14.md`（内部） | 6C1E795F2C9DC7C4 | 6C1E795F2C9DC7C4FD933000319F375C2596B75CC80520CCF9821E433D18A637 | 同じ | 公開しない（名と SHA-256 だけを残す） |
| `plans/rulings-D432-2026-10-14.md`（内部） | AD4ED0EE5499DC57 | AD4ED0EE5499DC57C9D648BE65305D229BD4992639C89311BE38834D9C74AF65 | 同じ | 公開しない（名と SHA-256 だけを残す） |
| `E/copyback-lists-E1.md`（内部） | 7B39AAF5839CFFA7 | 7B39AAF5839CFFA7A9B33F5E26DA7A921BD399F2B1F8FA4C9C1FAA854033B488 | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |
| `E/copyback-lists-E1.json`（内部） | E5F63105AA83308E | E5F63105AA83308E83E26A0117E243B91220BBA8238A5708BF1E559C4C6F87DE | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |
| `E/appendix_a_lists_E1.py`（内部） | 381427FB9049EF77 | 381427FB9049EF77004A4597BC917AC7E8AFAB4149699BA3BC42C3799B9ED07D | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |
| `explore/naming-survey-O-2026-10-13/note-fold-dakuten-2026-10-14.md`（内部） | 4B7E109A25BE9C1F | 4B7E109A25BE9C1FBC16DABC19BDC9E62CF0D01889E6CE0408C5B3B3E62CE5BA | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |
| `explore/naming-survey-O-2026-10-13/tools-used/scan_public_naming.py`（内部） | 13CD6C24CEC0F84A | 13CD6C24CEC0F84A171E0DFE141EBAFE06C4675CC6F67A032517A52A2E0EF359 | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |
| `explore/naming-survey-O-2026-10-13/tools-used/scan_public_naming_v2.py`（内部） | CA4FFEBC8B98F308 | CA4FFEBC8B98F308D1A059A1965DC6D188ED33EB2AE93AA4F1087C3E9FF7D146 | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |
| `explore/naming-survey-O-2026-10-13/tools-used/scan_public_names_ext.py`（内部） | 15B25982F0B3EE37 | 15B25982F0B3EE372A9B56F4D626D2FBD53ED128C1732C32E6E1032D4DB52EF1 | 同じ | 刻んだバイトのまま公開する（遅くとも E6） |
| `E/predictions-E1-2026-10-13.md`（内部） | F3CB5B9F017B2FDF | F3CB5B9F017B2FDF3D43730020E39254BC75F87F00EC705BBE4F1A60D5745EE2 | 同じ | 刻んだバイトのまま公開する（E2 の後の予想の照らしの後・遅くとも E6） |
| `E/sweep-D-promises-E1-v0.1.md`（内部） | D78FF1DA2B12AA21 | D78FF1DA2B12AA21BD25FF9808EC2E096C181E5C20B87341BA76A63693DD9AC0 | 同じ | 公開しない（名と SHA-256 だけを残す） |
| `plans/plan-framing-sensitivity-scale-and-mechanism-v3.0-2026-10-13.md`（内部） | 8165808D28274E82 | 8165808D28274E8283D109AA2C7C25E5D0AD7FFBFD439FF753E18EC1D4519881 | 同じ | 公開しない（名と SHA-256 だけを残す） |
| `D1p/d1p_confirm.py`（内部） | 3E92994DF6ADBE0F | 3E92994DF6ADBE0F4E88B804E6A48059F9FAF442194E9DCA94AAA0425AACB16A | 同じ | 公開しない（E6 の前に、名を伏せた写しを公開するかを伺う・その写しはこの SHA-256 と合わない） |
| `D1pE/d1pe_confirm.py`（内部） | F4094799DBEE9DCA | F4094799DBEE9DCA00179F6F7DAC62A6C16E2274E74C2F0A0168EAD14636827A | 同じ | 公開しない（E6 の前に、名を伏せた写しを公開するかを伺う・その写しはこの SHA-256 と合わない） |
| `arms/frozen-from-ryokai-os/app-scenarios.json`（公開の置き場） | 796D73F2544956D7・7AD7E49459D5C402 | 796D73F2544956D7F9CDDBB40B7D282298FA578984F047CAD1551A661EDF526B | 7AD7E49459D5C40203DF04F6819575796AD3E880BCB5A12801635BF304E4DDC1 | 公開済み（公開の置き場の同じファイル） |
| `arms/en-D1pE/app-scenarios-en.json`（公開の置き場） | CD343C3D344FF00C | CD343C3D344FF00CFA248324D742244DD61638A9BEF832F0915FECF11713956B | 同じ | 公開済み（公開の置き場の同じファイル） |
| `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py`（公開の置き場） | 56553F926272CF8A・12EAA8B845BC0A2F | 56553F926272CF8A0D49C2896D10F25BD7A5351982F329F40DB0194064FEDBE7 | 12EAA8B845BC0A2FF7FD6B9496213D20C880C993747C5F512A8551886CA84389 | 公開済み（公開の置き場の同じファイル） |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
