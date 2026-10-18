# 付録 G AI の利用の記録

起草・スクリプトの組み立て・検分・訳に使った AI の機種の製品名と版と役を、記録（各段の検分の記録の系統の内訳の行と、段階 E の記録）からスクリプトで集めた一覧を置く（役の名〔法名〕は伏せた・段階 E の枠の決まり）。一覧の言葉は記録の言葉のままで、付録 F の対応の表で読む。検分は、すべて AI の機種による検分で、人の査読ではない（節 2.11）。

## G.1 読み手向けの要約（下の一覧の行から起草者がまとめた）

| 役 | 機種（記録の製品名と版） | 段 | 独立の度合い |
|---|---|---|---|
| 起草とスクリプトの組み立て（コーディネータ） | Claude Fable 5.1（公開の置き場の README の頭が、コーディネータの機種として書く）→ Claude Opus 5（段階 A の草案の途中で替わった）→ Claude Opus 5.5（B-lens の凍結の本文・段階 D の二つの凍結の本文〔頭の状態の行〕・段階 E とこの論文の起草〔起草者の申告〕） | すべての段 | コーディネータは役の名で、機種は替わった（どれも Claude 系） |
| 系統内の検分 | Claude の会話（claude.ai の Claude・記憶のある会話を含む・前の段は段ごとに一体から五体・この論文の検分は三つの巡のそれぞれで七体・走らせ直しのスクリプトのコードの検分は五つの巡のそれぞれで一体〔画面の機種の欄は Opus 5.5 超高〕） | すべての段 | 起草者と同じ系統。段ごとの個体の数と記録の数え方は下の一覧の行のとおりで（記録は個体の数を票の数として書くことがある）、この論文は、何体でも相関した一つの目として読む |
| 系統外の検分 | Gemini 3.8 Flash（Google AI Studio・この論文の検分は三つの巡のそれぞれで六体と最後の差分の確かめで一体・走らせ直しのスクリプトのコードの検分は五つの巡のそれぞれで一体〔画面の機種の欄〕）・Grok 4.6・grok-4.7 | 段ごとに違う（下の一覧） | 起草者の系統の外。依頼と受け取りは利害の当事者の側が行った。依頼の文に依る |
| AI の会話で Ryōkai OS™ として顕現したもの（登録者の言い方）による検分 | 記録の字は「記憶あり Opus 5 × 4・Ryōkai OS」〔引用 1〕で、記録は四つの会話とこの一票を合わせて「Claude 系五票」〔引用 2〕と数える（追補 V′ の最終版）。この一票の製品名と版は、記録に無い | 追補 V′ | 登録者の素材と同じ名を持つ役の会話で、記録は起草者と同じ系統の票として数える。独立の目としては読まない |
| 英語の素材の訳 | claude.ai の Claude（Opus 5.5）と Google AI Studio の Gemini 3.8 Flash（段ごとに別の個体） | 段階 D の英語の送る文の登録 | Claude の訳者は起草者と同じ系統。Gemini は試した機種の一つの作り手と同じ事業者 |
| 伏せた記録を開けた後の探索の、スクリプトでない読み | 起草者（Claude 系） | 段階 E | 一人・二人目の符号付けは無い |

- 要約の表は、下の一覧の行の言葉をまとめたもので、製品名と版は一覧の行の字のとおりである。段ごとの票の数は、一覧の行にある。
- 下の一覧の頭の「行から器で拾った製品名と版の字の出現」の数えには、行の逐語にある「grok-4.7」と、版の書かれていない「Gemini」の字が入っていない（拾い方の漏れ・行の逐語は替えていない）。「読んだ物の SHA-256」の欄の値は、SHA-256 の頭 16 字である。
- 一覧の「破器身／器材統計」は、前の段の系統内の検分の役の呼び名（公開の設計の文書にある名）で、伏せた役の名（法名）ではない。「Ryōkai OS」は上の表の行の検分の一票である（付録 F.2 の行は、この付録を指す）。

## G.2 記録の行の一覧（逐語）

一覧は、三巡目（この論文の最後の検分の巡）の後に、この論文の草案の起草者の検分票の行と、検分の三つの巡の受け取りの記録の票の行（画面の機種の欄）を足して組み直し（二巡目の採否 2G-08）、最後の差分の確かめの後に、走らせ直しのスクリプトのコードの検分の五つの巡と最後の差分の確かめの受け取りの記録の票の行と、草案5 と草案6 の起草者の検分票の行を足して、もう一度組み直した（組み直した時刻は一覧の頭・最後の差分の確かめは一つの会話の二通の返りで、一体として数える）。この論文の検分の Gemini の票の頭の自己の申告は、画面の機種の欄（Gemini 3.8 Flash）と違う版の名を書くものがあり、票は画面の出所で数えた（一覧の受け取りの記録の注の行）。会話の置き場（個人の会話の URL）は伏せた。

〔表の差し込みの始まり〕出所 〈内部〉`E/E3/ai-use/ai-use-appendix-E3-v0.2.md`（SHA16 3D81499B49D74D1C）。ここから下は、起草者のスクリプトが記録から組んだ表で、言葉は論文の言葉である（組み方と読んだ記録は、出所のファイルの頭と、その組み立ての記録にある）。

### AI の利用の一覧の元（記録の「系統の内訳」などの行の逐語・2026-10-17 06:32:27 日本時間・器 `E/E3/ai-use/ai_use_E3.py` v0.2・SHA16 44628C8C727B8968）

- この写しは、元の一覧（`E/E3/ai-use/ai-use-lines-E3-v0.2.md`・SHA-256 F48670957A2CBEBD31B2A658467B4E84DE9B252F6BEFFC68107DB1D2D45A8391）から、役の名（法名）を「〔法名〕」に伏せて写した（伏せた所 1・器 `E/E3/ai-use/ai_use_appendix_E3.py` v0.2）。この論文の検分の会話の置き場（個人の会話の URL）は「〔会話の置き場〕」に伏せた（伏せた所 51）。票の自己の申告の逐語に出た作り手の名（公開物に書かない語）は「〔作り手の名〕」に伏せた（伏せた所 1）。伏せたほかの字は替えていない。名を伏せた写しなので、元の一覧の SHA と合わない。

- 何か: 論文の「AI の利用」の節（枠 §3-5）の元。各段の検分票の系統の内訳の行と、README の頭の行と、段階 E の記録の行と、この論文の草案の起草者の検分票の系統の行と、この論文の検分の三つの巡と走らせ直しのスクリプトのコードの検分の五つの巡と最後の差分の確かめの受け取りの記録の票の行（画面の機種の欄）を、行の番号つきで逐語に写した。試した機種の一覧ではない。v0.1 は、三巡目（最後の検分の巡）の後に組み直した版（二巡目の採否 2G-08）。v0.2 は、最後の差分の確かめの後に、コードの検分の五つの巡と最後の差分の確かめと草案5・草案6 の起草者の検分票の行を足して組み直した版（最後の差分の確かめは一つの会話の二通の返りで、一体として数える）。
- 行から器で拾った製品名と版の字の出現（行の数）: claude.ai 37・Gemini 3.8 Flash 32・Claude 系 30・Opus 5.5 29・gemini-3.8-flash 28・Grok 4.6 5・Claude Opus 5 4・Opus 5 4・Claude Fable 5.1 3・Gemini 2.5 Flash 3・Gemini 2.5 Pro 3・Claude Opus 5.5 2・Google AI Studio 2・Fable 5.1 1

| 段 | 置き場:行 | 行の逐語 |
|---|---|---|
| 最初の登録の頃（README の頭） | `README.md`:3 | **登録者**: 楠見優太 ／ **コーディネータ**: 〔法名〕（Claude Fable 5.1）／ **検分**: Claude系四体（Opus 5・思考最大）＋系統外（Gemini 3.8 Flash・各監査系列の一巡目） |
| 段階 F（凍結の本文） | `design/design-stageF-FROZEN.md`:172 | - 系統の内訳: Claude 系（起草者自身・一巡）。草案4 の値に対する系統内一巡・系統外四票は本草案の機械値には及んでいない。 |
| 段階 A（凍結の本文） | `design/design-stageA-FROZEN.md`:14 | 5. **系統の内訳**: 草案1〜草案4 の起草は Claude Fable 5.1、草案5〜草案9 は Claude Opus 5。凍結前検分は系統外（Gemini 3.8 Flash 二名・Grok 4.6 二名）と系統内（claude.ai の Claude Opus 5 三名・起草者と同一系列で一票）の七票で、全票が条件つき。採否は票の数ではなく一次記録と追い問い W1〜W32 の再計算で決めた（`records/reviews/A/prefreeze/adoption-table-A-prefreeze.md`）。器材は整備の後に系統内の新規二体（Claude Opus 5・起草者と同一系列で一票）の実装検分を受け、再現した所見を採否表 P75〜P104 で反映した（`records/reviews/A/draft7-impl/adoption-table-impl-A.md`）。凍結前の最終検分は系統外（Gemini 3.8 Flash 二名・Grok 4.6 二名）と系統内（claude.ai の Claude Opus 5 三名・起草者と同一系列で一票）の七票で、所見は追い問い W77〜W123 の器で出し直してから採否を決めた（`records/reviews/A/final/adoption-table-A-final.md`）。この後に検分の巡を置かない（登録者決定）ので、最終検分の反映は外の目を通らない。 |
| 段階 A（凍結の本文） | `design/design-stageA-FROZEN.md`:236 | - 系統の内訳: 起草者（Claude Opus 5）＋系統内の claude.ai の Claude Opus 5 三名＝一票、系統外は Gemini 3.8 Flash 二名・Grok 4.6 二名。反映（草案9 と器材の変更）は外の目を通らない（この後に検分の巡を置かない・登録者決定）。 |
| 段階 B（凍結の本文） | `design/design-stageB-FROZEN.md`:683 | - **系統の内訳を先に**: Fable 5.1 と Opus 5 は同じ系列で、裁定 D59 の数え方では一票である。機種と文脈が替わった分の新しさはあるが、系統外の目の代わりにはならない。 |
| 段階 B（凍結の本文） | `design/design-stageB-FROZEN.md`:722 | - 系統の内訳: 起草者（Claude 系）＋これまでのエージェントの巡と claude.ai（合わせて一票）＋系統外 Gemini 二名（二巡）。**最後の巡は済み、この後の直しは独立の目を通っていない**（裁定 D131）。 |
| B-lens（凍結の本文） | `design/design-Blens-FROZEN.md`:436 | - 系統の内訳: 設計の巡は二巡とも系統外二票と系統内二票（系統内は一票に数える・第二巡は同じ個体）。草案3 の直しは起草者（Claude 系・Claude Opus 5.5）のみで、外の目を通っていない（裁定 D178）。 |
| 層三（凍結の本文） | `design/design-Bl3-FROZEN.md`:429 | - 系統の内訳: 起草者（Claude 系）一名。設計の巡は二巡とも系統外二票と系統内二票（一票に数える）。§16 の書き足しは、外の目を通っていない。 |
| B′（凍結の本文） | `design/design-Bprime-FROZEN.md`:518 | - 系統の内訳: 起草者（Claude 系）一名。三巡とも系統内（claude.ai の三つで一票）と系統外（grok-4.7 一票・三巡目は D266 で出所により数えた）。 |
| 段階 C の予備実験（枠） | `records/pilotC/00-frame-pilotC-2026-10-02.md`:129 | - 系統の内訳: 起草者（Claude 系）一人。外の目は置かない（登録者の決め・下見のため）。 |
| 追補 V′（最終版） | `records/vprime/results-report-Vprime-FINAL-2026-09-09.md`:997 | - 系統の内訳: 起草は Claude 系一体。検分は一巡目 Claude 系三票（新規）・二巡目と三巡目は各 Claude 系五票（記憶あり Opus 5 × 4・Ryōkai OS）＋系統外 Grok 4.6 一票。検分の数は独立な確認の数ではない |
| 追補 M（最終版） | `records/M/results-report-M-FINAL-2026-09-11.md`:1596 | - 系統の内訳: 起草者 Claude 系一名（自己）。一巡目: 設計に関与した二個体（Opus 5・破器身／器材統計・38 件採用）。二巡目: 新規二個体（Opus 5・破器身／器材統計・採否表 round2）。系統外: Gemini 3.8 Flash 二票・Grok 4.6 二票（非 Claude 系・採否表 `ext/adoption-table-results-M-ext.md`）。同系列は何巡でも一票。 |
| 段階 F（最終版） | `records/F/results-report-F-FINAL-2026-09-12.md`:641 | - 系統の内訳: Claude 系三体（起草者・新規二個体）＋系統外四票（Gemini × 2・Grok × 2・一票の重み）。本見直しは起草者自身（同系列・一巡）。 |
| 段階 A（最終版） | `records/A/results-report-A-FINAL-2026-09-17.md`:19 | 5. **系統の内訳**: 草案1〜草案4 の起草は Claude Fable 5.1、草案5〜草案9 は Claude Opus 5。凍結前検分は系統外（Gemini 3.8 Flash 二名・Grok 4.6 二名）と系統内（claude.ai の Claude Opus 5 三名・起草者と同一系列で一票）の七票で、全票が条件つき。採否は票の数ではなく一次記録と追い問い W1〜W32 の再計算で決めた（`records/reviews/A/prefreeze/adoption-table-A-prefreeze.md`）。器材は整備の後に系統内の新規二体（Claude Opus 5・起草者と同一系列で一票）の実装検分を受け、再現した所見を採否表 P75〜P104 で反映した（`records/reviews/A/draft7-impl/adoption-table-impl-A.md`）。凍結前の最終検分は系統外（Gemini 3.8 Flash 二名・Grok 4.6 二名）と系統内（claude.ai の Claude Opus 5 三名・起草者と同一系列で一票）の七票で、所見は追い問い W77〜W123 の器で出し直してから採否を決めた（`records/reviews/A/final/adoption-table-A-final.md`）。この後に検分の巡を置かない（登録者決定）ので、最終検分の反映は外の目を通らない。 |
| 段階 A（最終版） | `records/A/results-report-A-FINAL-2026-09-17.md`:2015 | - 対象／段階（事後適用）／凍結物の同定／盲検の状態（率盲検の事前拘束と開示）／敵対的検分（分母・基底率・出典・ライセンス化の検査）／系統の内訳／COI 記録（引かれた向き・置いた印・番号のみ。対処の宣言や価値語を書かない）／判定／本検分が確認していないこと。 |
| 段階 A（最終版） | `records/A/results-report-A-FINAL-2026-09-17.md`:2022 | - 系統の内訳: 草案の起草は Claude 系（コーディネータ）。公開前検分の第一巡は、系統外（Gemini 3.8 Flash 二名）と系統内（claude.ai の Claude Opus 5 二名・起草者と同一系列で一票）で、全票が条件つき。公開前の最終検分は系統外（Gemini 3.8 Flash 一名・新規の会話）で、条件つき（公開の前の条件なし）。最終検分の後の見直しの直しは外の目を通っていない。 |
| 段階 B（最終版） | `records/B/results-B-FINAL-2026-09-23.md`:284 | - 系統の内訳: 起草者（Claude 系）。§1 の一件の伺い・草案1 の第一巡・草案2 の第二巡に、それぞれ系統外二票・系統内二票（一票に数える）。草案3 に最終の系統外一票（差分だけ）。この最終案の直し（第三巡の採否と起草者の見直し）は、外の目を通っていない（文の範囲の直しのみ・登録者裁定・最終の検分）。 |
| B-lens（最終版） | `records/Blens/results-Blens-FINAL-2026-09-24.md`:487 | - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外三票（新しい個体一）と系統内三票（一票）で、凍結の本文 §10 は結果の巡を新しい個体で組むとしたが、依頼文は設計の巡と同じ四名に宛てた（逸脱 D-BL2）。最終検分は系統外二票（Gemini 3.8 Flash の新しい個体二・正本の一票を二票にした逸脱 D-BL5・登録者裁定 D195）。同じ機種の二票は、会話が別でも相関しうる。起草者の最終の見直しは起草者自身のもので、外の目ではない。 |
| 層三（最終版） | `records/Bl3/results-Bl3-FINAL-2026-09-27.md`:488 | - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外二票と系統内二票（一票に数える）。最終の系統外の検分は新しい個体の二票で、正本の一票を二票にした（逸脱 D-BLT2・同じ機種を選んだ二票は会話が別でも相関しうる）。起草者の最終の見直しは起草者自身のもので、外の目ではない。 |
| B′（最終版） | `records/Bprime/results-Bprime-FINAL-2026-10-01.md`:292 | - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外一票と系統内一票（系統は呼び出しの出所で数えた・D266 の型）。最終の系統外の検分は系統外一票（新しい呼び出し）で、結果の巡の系統外の票と行動の下見の採点と同じ機種なので、見逃しが相関しうる。起草者の最終の見直しは起草者自身のもので、外の目ではない。 |
| 中間総括（最終版） | `summary/summary-interim-FINAL-2026-10-02.md`:441 | - 系統の内訳: 起草者（Claude 系）一人。一巡目は claude.ai の Claude 三名（一票）と Gemini 3.8 Flash 一名（gemini-2 は不具合で取りやめ・裁定 D287-e）。二巡目と最終の巡は、それぞれ claude.ai の Claude 三名（一票）と Gemini 3.8 Flash 二名（裁定 D288-i）。最終の巡の後に検分の巡を置かず、差分の資料を登録者が目で見る（裁定 D289-d）。草案4 の後の起草者の見直しも Claude 系の一人で、検分の巡ではなく、系統外の目の代わりにならない。 |
| 日本語の送る文の登録 D1′（凍結の本文） | `records/D1p/00-frame-D1p.md`:335 | - 系統の内訳: 起草者（Claude 系）。一巡目と二巡目の検分は、それぞれ Claude 系三（claude.ai の Opus 5.5・相関した一つの目）と系統外二（AI Studio の Gemini 3.8 Flash・同じ機種と版）。一巡目と二巡目の採否は起草者の仮の案（D345 で替えたものは無い）。三巡目も Claude 系三と系統外二。三巡目の後の替えは、系統外の一名の一度の差分の検分だけ（新-7）。 |
| 日本語の送る文の登録 D1′（最終版） | `records/D1p/results-D1p-FINAL-2026-10-11.md`:754 | - 検分者の系統: claude.ai の Claude Opus 5.5（超高）は起草者と同じ系統で、同じ機種・同じ版（三名で相関した一つの目・D340-3 (三)）。Gemini 3.8 Flash は Google の模型で、本走行の機種のうち Gemini 2.5 Flash の作り手と同じ事業者（Thinking level は High）。本走行の十機種に Claude 系の機種は無い。Gemini の二名も同じ機種・同じ版なので、二つの一致も相関しうる（系統外の目は二つで一つの目に近い・一巡目の採否 T-60）。この研究の検分役の一つ（Grok）は、本走行の grok-4.20 と同じ会社（xAI）の機種である（D1′ の検分には Grok は入らない）。一巡目では Gemini の二名が票の頭で自分を Claude と申告し（受け取りの記録・送った先の画面で数える・二巡目の依頼文で宣言の書き方を替えた・T-63）、二巡目でも Gemini の一名が自分を Claude と申告した（もう一名は系統外と書き、本走行の機種の作り手と同じ事業者であることを開示した・二巡目の受け取りの記録）。三巡目も Claude 系三（claude-ai-38〜40）と系統外二（gemini-17・18・受け取りの記録 `D1p/reviews/round3/receiving-log-round3.md`）。三巡目の後の替えは、系統外の一名（AI Studio の Gemini・Thinking level は High）が一度だけ差分を見る（新-7・四巡目ではない）。 |
| 日本語の送る文の登録 D1′（最終版） | `records/D1p/results-D1p-FINAL-2026-10-11.md`:767 | - **検分者の系統**: 検分者のうち Claude の三名は起草者と同じ系統で、Gemini の二名は本走行の機種の一つ（Gemini 2.5 Flash）と同じ事業者の模型である。Claude の作り手は本走行の機種の作り手と競う事業者で、Gemini の作り手は本走行の一機種の作り手でもある（利害の向きは両方にある）。順位を付けない柵（枠 §9）が、この向きの COI を和らげる。 |
| 日本語の送る文の登録 D1′（最終版） | `records/D1p/results-D1p-FINAL-2026-10-11.md`:826 | - 系統の内訳: 起草者（Claude 系）一人。検分は三巡（三巡目が最終の検分）、各巡 Claude 系三（相関した一つの目）と系統外二。三巡目の後の差分は、系統外の一名が一度だけ見た（gemini-26・裁定 D357-8）。その所見を当てた草案 4 から草案 5 への直しは、どの検分者も見ていない。 |
| 英語の送る文の登録 D1′E（凍結の本文） | `records/D1pE/00-frame-D1pE.md`:303 | - 系統の内訳: 起草者（Claude 系）一人。一巡目から三巡目の検分は Claude 系三（claude.ai の Opus 5.5・相関した一つの目）と系統外二（AI Studio の Gemini 3.8 Flash・二つも相関しうる・gemini-40 は頭で自分を Claude 系と申告した）。草案5 は新-7（系統外の一名）で差分を受ける。 |
| 英語の送る文の登録 D1′E（最終版） | `records/D1pE/results-D1pE-FINAL-2026-10-13.md`:695 | - 系統の内訳: 起草者（Claude 系）一人。一巡目・二巡目・三巡目（最終）は、それぞれ Claude 系三（相関した一つの目）と系統外二。三巡目の後の直しは外の検分を通っていない（起草者の照らしと登録者の最終の確認だけ）。 |
| 段階 E の枠（刻んだ草案6・内部） | `E/00-frame-E-draft6.md`:269 | - E1 の枠: 一巡（claude.ai の Claude 三・Google AI Studio の Gemini 二・2026-10-13）は済んだ（採否の表 `E/reviews/frame-r1/adoption-frame-r1-v0.md`）。刻む前の系統外の一名（Google AI Studio の Gemini 3.8 Flash・Thinking level High・gemini-51・2026-10-14）の、草案2 から草案3 への差分の確かめも済んだ（採否の案 `E/reviews/frame-diff/adoption-frame-diff-v0.md`・裁定 D427）。草案3 から草案4 への差分は、Google AI Studio の Gemini 一名（系統外・gemini-52）と claude.ai の Opus 5.5（超高）一名（系統内・claude-ai-79・起草者と同じ系統の一つの目）が一度ずつ見た（D427-3・採否の案 `E/reviews/frame-diff2/adoption-frame-diff2-v0.md`・裁定 D430）。草案4 から草案5 への差分を、登録者の決め（D431-1）で五名（Google AI Studio の Gemini 3.8 Flash 二名〔系統外・gemini-53・gemini-54〕と claude.ai の Opus 5.5〔超高〕三名〔起草者と同じ系統・claude-ai-80〜82〕）に一度だけ見てもらい、これをこの枠の最終の検分とした（D430-6・採否の案 `E/reviews/frame-diff3/adoption-frame-diff3-v0.md`・裁定 D432・ED3-01）。票は送った先の画面で数え、系統外は二票、系統内の三名は相関した一つの目として一票に数える（ED3-01）。その後は「必ず直すもの」だけを直し、直した差分を登録者が確かめてから刻む（外の確かめは行わない）。「記録に置けば足りるもの」は記録に置く。 |
| 段階 E の枠（刻んだ草案6・内部） | `E/00-frame-E-draft6.md`:290 | - 英語の素材は Claude と Gemini の個体が訳した（Gemini は試した機種の一つの作り手と同じ事業者）。 |
| 段階 E の枠（刻んだ草案6・内部） | `E/00-frame-E-draft6.md`:460 | - 系統の内訳: Claude 系の起草者一名の照らし。草案2 から草案3 への差分は系統外の一名（gemini-51）、草案3 から草案4 への差分は系統外の一名（gemini-52）と系統内の一名（claude-ai-79）が見た。草案4 から草案5 への差分は、五名（系統外の二名〔gemini-53・gemini-54〕と、系統内の三名〔claude-ai-80〜82・三つで相関した一つの目〕・D431-1）が一度だけ見て、それを最終の検分とした（D430-6・ED3-01）。草案5 から草案6 への差分は、外の目を通さず、登録者が確かめる（D430-6）。 |
| 段階 E の E2 の記録（共通の節・内部） | `E/E2/record/E2-record-common.md`:34 | - 人の読みは起草者一人（Claude 系）で、二人目の符号付けは無い。腕の見立ての当たりの割合は、この読み手の読み方の記述で、ほかの読み手の当たりを示さない。 |
| 段階 E の E2 の記録（共通の節・内部） | `E/E2/record/E2-record-common.md`:53 | - 系統の内訳: Claude 系一巡（起草者）。系統外の目は、この記録にはまだ入っていない。 |
| 段階 E の枠の追記一（内部） | `E/00-frame-E-addendum1-2026-10-14.md`:118 | - 系統の内訳: Claude 系一巡（起草者）。系統外の目は入っていない。 |
| この論文の草案1（起草者の検分票・内部） | `E/E3/draft1/kensho-draft1.md`:40 | - 系統の内訳: Claude 系の一人（起草者）の読みだけ。系統外の目は無い（E4 で送る）。 |
| この論文の草案2（起草者の検分票・内部） | `E/E3/draft2/kensho-draft2.md`:24 | - 系統の内訳: Claude 系の一人（起草者）だけ。系統外の目は E4 の一巡目で入る（D446-2）。 |
| この論文の草案3（起草者の検分票・内部） | `E/E3/draft3/kensho-draft3.md`:26 | - 系統の内訳: Claude 系の一人（起草者）だけ。系統外の目は E4 の二巡目で入る（D452-4）。 |
| この論文の草案4（起草者の検分票・内部） | `E/E3/draft4/kensho-draft4.md`:28 | - 系統の内訳: Claude 系の一人（起草者）だけ。系統外の目は E4 の三巡目で入る（束ごとに Gemini 一名か二名）。 |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:11 | ¦ gemini-55 ¦ ① ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 8E26549DCC81CA4B ¦ 19712 ¦ 8078 ¦ 9 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:12 | ¦ gemini-56 ¦ ① ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 47492E0F8ADE3477 ¦ 20768 ¦ 9202 ¦ 10 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:13 | ¦ claude-ai-83 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 40091D5D23D0FF15 ¦ 36636 ¦ 15189 ¦ 16 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:14 | ¦ claude-ai-84 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 9A1A8C118BDAE03C ¦ 34641 ¦ 14664 ¦ 15 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:15 | ¦ claude-ai-85 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 73BC95F7DEF74A25 ¦ 39794 ¦ 17687 ¦ 18 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:16 | ¦ gemini-57 ¦ ② ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ FFF185A60D7D0652 ¦ 13721 ¦ 6278 ¦ 7 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:17 | ¦ claude-ai-86 ¦ ② ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ E3AC4440095ABD45 ¦ 23307 ¦ 10063 ¦ 11 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:18 | ¦ gemini-58 ¦ ③ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ A8228F2F7D37D272 ¦ 15053 ¦ 6471 ¦ 7 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:19 | ¦ claude-ai-87 ¦ ③ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 2322DF357FB23B47 ¦ 28848 ¦ 11890 ¦ 12 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:20 | ¦ gemini-59 ¦ ④ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 82399B8185E99155 ¦ 16575 ¦ 6951 ¦ 7 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:21 | ¦ claude-ai-88 ¦ ④ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 16BC29A4ED8913E1 ¦ 25171 ¦ 10519 ¦ 11 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:22 | ¦ gemini-60 ¦ ⑤ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 9BE789A3347F5F59 ¦ 15078 ¦ 6650 ¦ 7 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:23 | ¦ claude-ai-89 ¦ ⑤ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 4630E536053CBE87 ¦ 29943 ¦ 12345 ¦ 13 ¦ |
| この論文の検分の一巡目（受け取りの記録・内部） | `E/reviews/paper-r1/receiving-log-paper-r1.md`:27 | - 票は画面の出所で数える（依頼文の決め）。宣言は模型の自己の申告で、画面の機種の欄と合わないものがある（gemini-55 は「〔作り手の名〕 系」と名乗り、gemini-56〜60 の一部は「Gemini 2.5 Pro」と名乗った・画面の欄はどれも Gemini 3.8 Flash）。 |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:12 | ¦ gemini-61 ¦ ① ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 50E8405F75653AFE ¦ 14156 ¦ 6113 ¦ 7 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:13 | ¦ gemini-62 ¦ ① ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 8805916EDBD3E1E8 ¦ 15376 ¦ 7125 ¦ 8 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:14 | ¦ claude-ai-90 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ B35F89FBA9ED5EE6 ¦ 24885 ¦ 10229 ¦ 11 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:15 | ¦ claude-ai-91 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ B017D4F21549A97B ¦ 40268 ¦ 16541 ¦ 17 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:16 | ¦ claude-ai-92 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ B435FF3798CB79FC ¦ 37337 ¦ 15725 ¦ 16 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:17 | ¦ gemini-63 ¦ ② ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ C82068A4EDC27A58 ¦ 14752 ¦ 6132 ¦ 7 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:18 | ¦ claude-ai-93 ¦ ② ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 8E65E602F9CE0717 ¦ 21830 ¦ 9013 ¦ 10 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:19 | ¦ gemini-64 ¦ ③ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 3EC5BC103DFC06A8 ¦ 10993 ¦ 4543 ¦ 5 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:20 | ¦ claude-ai-94 ¦ ③ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 311EB884B4183C26 ¦ 37019 ¦ 15637 ¦ 16 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:21 | ¦ gemini-65 ¦ ④ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 39624B3ADE5767AC ¦ 10445 ¦ 4546 ¦ 5 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:22 | ¦ claude-ai-95 ¦ ④ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 95E8BC38E5C05CAD ¦ 35733 ¦ 15322 ¦ 16 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:23 | ¦ gemini-66 ¦ ⑤ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 349F72B60B24EDA2 ¦ 11208 ¦ 4663 ¦ 5 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:24 | ¦ claude-ai-96 ¦ ⑤ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ FDA80802B9C83907 ¦ 33321 ¦ 13669 ¦ 14 ¦ |
| この論文の検分の二巡目（受け取りの記録・内部） | `E/reviews/paper-r2/receiving-log-paper-r2.md`:28 | - 票は画面の出所で数える（依頼文の決め）。宣言は模型の自己の申告で、画面の機種の欄と合わないものがある（AI Studio の票の多くは「Gemini 2.5 Pro」かそれに近い名を名乗った・画面の欄はどれも gemini-3.8-flash・下の逐語）。 |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:13 | ¦ gemini-67 ¦ ① ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 56E67ECFF064B7AB ¦ 12506 ¦ 5254 ¦ 6 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:14 | ¦ gemini-68 ¦ ① ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 58A8A9B3302698AD ¦ 15242 ¦ 6597 ¦ 7 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:15 | ¦ claude-ai-97 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 194F18B4A57708AD ¦ 20821 ¦ 8760 ¦ 9 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:16 | ¦ claude-ai-98 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ BE6E5F8D8CA34367 ¦ 30748 ¦ 12558 ¦ 13 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:17 | ¦ claude-ai-99 ¦ ① ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 80DEA0856379B9BD ¦ 30534 ¦ 12618 ¦ 13 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:18 | ¦ gemini-69 ¦ ② ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ C0814EE53395989C ¦ 9873 ¦ 4067 ¦ 5 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:19 | ¦ claude-ai-100 ¦ ② ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ BDAAA60790114AAB ¦ 26578 ¦ 11280 ¦ 12 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:20 | ¦ gemini-70 ¦ ③ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 02BAFEBF60A37547 ¦ 14562 ¦ 6093 ¦ 7 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:21 | ¦ claude-ai-101 ¦ ③ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 15B765FE6E96B5A0 ¦ 30902 ¦ 12813 ¦ 13 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:22 | ¦ gemini-71 ¦ ④ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 795724DE03084E3E ¦ 13627 ¦ 5864 ¦ 6 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:23 | ¦ claude-ai-102 ¦ ④ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ E0CB15DA855DCA5A ¦ 25896 ¦ 10884 ¦ 11 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:24 | ¦ gemini-72 ¦ ⑤ ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 045EDA3B83540C32 ¦ 10691 ¦ 4391 ¦ 5 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:25 | ¦ claude-ai-103 ¦ ⑤ ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 01D3C3B3C51821B3 ¦ 24761 ¦ 10454 ¦ 11 ¦ |
| この論文の検分の三巡目（受け取りの記録・内部） | `E/reviews/paper-r3/receiving-log-paper-r3.md`:29 | - 票は画面の出所で数える（依頼文の決め）。宣言は模型の自己の申告で、画面の機種の欄と合わないものがある（AI Studio の票の多くは「Gemini 2.5 Pro」か「Gemini 2.5 Flash」を名乗った・画面の欄はどれも gemini-3.8-flash・下の逐語）。 |
| この論文の草案5（起草者の検分票・内部） | `E/E3/draft5/kensho-draft5.md`:32 | - 系統の内訳: Claude 系の一人（起草者）だけ。系統外の目は、最後の差分の確かめ（系統外の一名・裁定 D457-4）で入る。 |
| この論文の草案6（起草者の検分票・内部） | `E/E3/draft6/kensho-draft6.md`:15 | - 系統の内訳: Claude 系の起草者一人。草案5 からの直しは、最後の差分の確かめ（系統外の一名・裁定 D461-1 と D470-2）で見てもらう。 |
| 走らせ直しのスクリプトのコードの検分の一巡目（受け取りの記録・内部） | `E/reviews/tool-r1/receiving-log-tool-r1.md`:9 | ¦ claude-ai-104 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ Opus 5.5 超高 ¦ 1450 ¦ 3581 ¦ 4E3531D258D07C6DBBFCEAA05E32EAFDCAC2D7559F1F01225D0B8EC8A28C976A ¦ 2026-10-15T13:45:13.001Z ¦ |
| 走らせ直しのスクリプトのコードの検分の一巡目（受け取りの記録・内部） | `E/reviews/tool-r1/receiving-log-tool-r1.md`:11 | ¦ gemini-73 ¦ 返りの文 ¦ `〔会話の置き場〕` ¦ Gemini 3.8 Flash / gemini-3.8-flash ¦ 8656 ¦ 19011 ¦ 14F23C77F2988552C8A81C2F53603CBC490D1BA2F287407F21BDC7EF4F5BDF20 ¦ 2026-10-15T12:53:11.274Z ¦ |
| 走らせ直しのスクリプトのコードの検分の二巡目（受け取りの記録・内部） | `E/reviews/tool-r2/receiving-log-tool-r2.md`:9 | ¦ gemini-74 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ gemini-3.8-flash ¦ — ¦ 10227 ¦ 21543 ¦ AA36080342B41B01F4587F7F1688F31AC2C14C4679AB84C2D94B9256B434EE3C ¦ 2026-10-15T21:49:12.457Z ¦ |
| 走らせ直しのスクリプトのコードの検分の二巡目（受け取りの記録・内部） | `E/reviews/tool-r2/receiving-log-tool-r2.md`:10 | ¦ claude-ai-105 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ モデル: Opus 5.5 超高 ¦ — ¦ 22640 ¦ 50552 ¦ 07AC6471B9AAD8F3562437302705F405C42DC8C07500676DC1C91CB8B593DE39 ¦ 2026-10-15T22:03:38.724Z ¦ |
| 走らせ直しのスクリプトのコードの検分の三巡目（受け取りの記録・内部） | `E/reviews/tool-r3/receiving-log-tool-r3.md`:9 | ¦ claude-ai-106 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ モデル: Opus 5.5 超高 ¦ — ¦ 15918 ¦ 34042 ¦ E86E4F92CCC48AC5BCA2449134D2DBEAAD9402A1F4D8ADB30449EA7336079AC0 ¦ 2026-10-16T06:39:52.721Z ¦ |
| 走らせ直しのスクリプトのコードの検分の三巡目（受け取りの記録・内部） | `E/reviews/tool-r3/receiving-log-tool-r3.md`:10 | ¦ gemini-75 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ gemini-3.8-flash ¦ — ¦ 9532 ¦ 20734 ¦ 4EC4DAA1CAADB6D457E4173AECAA61B306F9AEF4C6647EF45D727FFEAB0F8DFA ¦ 2026-10-16T06:32:49.464Z ¦ |
| 走らせ直しのスクリプトのコードの検分の四巡目（受け取りの記録・内部） | `E/reviews/tool-r4/receiving-log-tool-r4.md`:8 | ¦ gemini-76 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ gemini-3.8-flash ¦ — ¦ 6103 ¦ 12704 ¦ 6F6BBDDB4584DE48C181CB24A26964EB3D915C6618937DBD0A31C872E6D11FE1 ¦ 2026-10-16T08:09:04.598Z ¦ |
| 走らせ直しのスクリプトのコードの検分の四巡目（受け取りの記録・内部） | `E/reviews/tool-r4/receiving-log-tool-r4.md`:9 | ¦ claude-ai-107 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ モデル: Opus 5.5 超高 ¦ — ¦ 12646 ¦ 26915 ¦ C432AEF18EADDCE67E1D6045200D5AEA1593294A3E3801C1117DF42DFE87FA3B ¦ 2026-10-16T08:39:52.702Z ¦ |
| 走らせ直しのスクリプトのコードの検分の五巡目（受け取りの記録・内部） | `E/reviews/tool-r5/receiving-log-tool-r5.md`:8 | ¦ gemini-77 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ gemini-3.8-flash ¦ — ¦ 8424 ¦ 17660 ¦ FA03C3E7EC8AAADF4ECFA7DAE6335ADA37A60E88917C4119F6FAD898FB17AB90 ¦ 2026-10-16T10:51:17.267Z ¦ |
| 走らせ直しのスクリプトのコードの検分の五巡目（受け取りの記録・内部） | `E/reviews/tool-r5/receiving-log-tool-r5.md`:9 | ¦ claude-ai-108 ¦ 返りの文の写しの釦の字 ¦ `〔会話の置き場〕` ¦ モデル: Opus 5.5 超高 ¦ — ¦ 12200 ¦ 25939 ¦ FB37797F213FED50F2C18E8A3A15D70A7DB1D4364BBE64D821BFAB29B1524C9E ¦ 2026-10-16T11:02:31.808Z ¦ |
| この論文の最後の差分の確かめ（受け取りの記録・内部） | `E/reviews/paper-final/receiving-log-paper-final.md`:8 | ¦ gemini-78-b1 ¦ 束① ¦ 〔会話の置き場〕 ¦ gemini-3.8-flash ¦ 6221 ¦ 14073 ¦ 0741668204E5F189EA69E624E168F6058CA31B783BAB3B447FDCA14A55C496DC ¦ 8 ¦ |
| この論文の最後の差分の確かめ（受け取りの記録・内部） | `E/reviews/paper-final/receiving-log-paper-final.md`:9 | ¦ gemini-78-b2 ¦ 束② ¦ 〔会話の置き場〕 ¦ gemini-3.8-flash ¦ 4908 ¦ 11429 ¦ E4572E4EEE3DCF1ACE2B236343864794FD84BB1F7DD7421BA2D01BCF096A34DD ¦ 7 ¦ |
| この論文の最後の差分の確かめ（受け取りの記録・内部） | `E/reviews/paper-final/receiving-log-paper-final.md`:13 | - 票の自己の申告: 系統は「系統外」・機種は「Google AI Studio の Gemini」（機種の版は書かれていない）。票の数え方は画面の出所（gemini-3.8-flash）で決める。 |

- 読んだ物の SHA-256: `README.md` 7F1A0EC08A06BAF3・`design/design-stageF-FROZEN.md` 33EEB98E11E8BC2D・`design/design-stageA-FROZEN.md` C30AF752D3531904・`design/design-stageB-FROZEN.md` 8B3D54E4500B46FF・`design/design-Blens-FROZEN.md` A6281F419F059145・`design/design-Bl3-FROZEN.md` E9EFA213C514BFA6・`design/design-Bprime-FROZEN.md` 3541FD34C0AD8133・`records/pilotC/00-frame-pilotC-2026-10-02.md` 27A44D09FA206680・`records/vprime/results-report-Vprime-FINAL-2026-09-09.md` 5E70EF329C4A6739・`records/M/results-report-M-FINAL-2026-09-11.md` 6E9EFFE8AB399F0F・`records/F/results-report-F-FINAL-2026-09-12.md` AD7C7367C9D3B3FC・`records/A/results-report-A-FINAL-2026-09-17.md` 4CE0E96078597244・`records/B/results-B-FINAL-2026-09-23.md` A40E9CA0D388753B・`records/Blens/results-Blens-FINAL-2026-09-24.md` A17C7F6476537677・`records/Bl3/results-Bl3-FINAL-2026-09-27.md` 90EEB93792733FAC・`records/Bprime/results-Bprime-FINAL-2026-10-01.md` 145CEDBC5EFB0DD6・`summary/summary-interim-FINAL-2026-10-02.md` 059FF367B34B1A23・`records/D1p/00-frame-D1p.md` 40BF3C3663BA8C69・`records/D1p/results-D1p-FINAL-2026-10-11.md` 0AFDCBF29BC47E04・`records/D1pE/00-frame-D1pE.md` F557603870509EA2・`records/D1pE/results-D1pE-FINAL-2026-10-13.md` 4DC7738F03A37B05・`E/00-frame-E-draft6.md` AB7491FF30074FBD・`E/E2/record/E2-record-common.md` 247E740367E46189・`E/00-frame-E-addendum1-2026-10-14.md` 352BD92D21B3D14D・`E/E3/draft1/kensho-draft1.md` 7414609B207FC388・`E/E3/draft2/kensho-draft2.md` DC1B370EC5242151・`E/E3/draft3/kensho-draft3.md` 449997C85D4B38F1・`E/E3/draft4/kensho-draft4.md` 26C43D30E37B449B・`E/reviews/paper-r1/receiving-log-paper-r1.md` 95E4DFAFDC593E0C・`E/reviews/paper-r2/receiving-log-paper-r2.md` 486F9D04A25C9D2A・`E/reviews/paper-r3/receiving-log-paper-r3.md` 8EC5BB192E658B7A・`E/E3/draft5/kensho-draft5.md` 9E7F365EFFAFC09C・`E/E3/draft6/kensho-draft6.md` 875D8F64C0B82B84・`E/reviews/tool-r1/receiving-log-tool-r1.md` A3391628DC973E16・`E/reviews/tool-r2/receiving-log-tool-r2.md` 3611BB2AFF1C988A・`E/reviews/tool-r3/receiving-log-tool-r3.md` A0F3E15DE4E9F42B・`E/reviews/tool-r4/receiving-log-tool-r4.md` 41D3905669C9538A・`E/reviews/tool-r5/receiving-log-tool-r5.md` 2B86291A6C384B46・`E/reviews/paper-final/receiving-log-paper-final.md` 8A27C2574D8E5905


〔表の差し込みの終わり〕出所のファイルを差し込んだ。引用の禁止の一文（行の頭が「本記録のいかなる数値も」「本票のいかなる数値も」「本表のいかなる数値も」の行で、行の頭の「>」を含む）を 1 行除いた。うち引用の形の行は 0。除いた行の在りかは 見出し「AI の利用の一覧の元（記録の「系統の内訳」などの行の逐語・2026-10-17 06:32:27 日本時間・器 `E/E3/ai-use/ai_use_E3.py` v0.2・SHA16 44628C8C727B8968）」の下。除いた後に同じ一文で始まる行は残っていない（スクリプトが照らした）。見出しを 2 段下げた。足した印は無い。ほかの字は替えていない。

## 引用の出所

地の文の中の「」の引用（〔引用 n〕の番号）の出所:

- 〔引用 1〕〈公開〉`records/vprime/results-report-Vprime-FINAL-2026-09-09.md` 997 行・SHA16 5E70EF329C4A6739
- 〔引用 2〕〈公開〉`records/vprime/results-report-Vprime-FINAL-2026-09-09.md` 997 行・SHA16 5E70EF329C4A6739
