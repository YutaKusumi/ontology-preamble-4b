# B-lens 層三の草案3 の直しの案と、裁定 D224・D225 の記帳の後の版の比べ（機械生成・`records/Bl3/draft3-review/verify_final_draft3_Bl3.py`）

- 直しの案（登録者が見た版）の写し: `records/Bl3/draft3-review/proposal/design-Bl3-draft3-proposal.md`（SHA16 ACF9769D441297D7）・`records/Bl3/draft3-review/proposal/contrasts-Bl3-proposal.json`（SHA16 27A4EBFDB946E162）。見直しの記録 `records/Bl3/draft3-review/review-draft3-Bl3.md` に書いた直しの案の SHA16 と同じ。
- 記帳の後の版: `design/design-Bl3-draft3.md`（SHA16 30CED58A8559EA05・419 行）・`design/contrasts-Bl3.json`（SHA16 6330B65A0AB503E7）。
- 正本の葉の差: 7（決めた型の外 0）。草案3 の行の差: 7 行（行の足し引き無し・決めた型の外 0）。

## 正本の葉の差

| 葉 | 案 | 記帳の後 |
|---|---|---|
| `decisions.D224` | （無い） | 草案3 の起草者の見直しの直しをすべて採る。新しい小さな決まり: (vi) の (b) で止めたときは (i)〜(v) を計算しない・下見の無操作の値はバッチの |
| `decisions.D225` | （無い） | 本の計算の中の器の誤りは下見と同じ型で扱う（結果を開かずに止め、逸脱の台帳に記して登録者に上げる。やり直すかは登録者の裁定。やり直さないときは結果を開かずに閉じ |
| `inputs.files.draft3_review.path` | （無い） | records/Bl3/draft3-review/review-draft3-Bl3.md |
| `inputs.files.draft3_review.sha16` | （無い） | 81294EA2349E9609 |
| `inputs.files.rulings_D224_D225.path` | （無い） | records/Bl3/rulings-D224-D225.md |
| `inputs.files.rulings_D224_D225.sha16` | （無い） | 8F9C78E3F339C931 |
| `numbering.rulings_next` | D224 | D226 |

- `inputs.files` の中で、足した二つのほかに SHA16 が動いた入力: 無し。

## 草案3 の行の差

| 行 | 型 | 案 | 記帳の後 |
|---|---|---|---|
| 3 | 状態の行 | - 起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／登録者: 楠見優太／2026-09-24（日本時間）。**状態: 草案3（起草者の見直しの後の案・設計の巡・二巡目〔最終検分〕の後・登録者の確認 | - 起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／登録者: 楠見優太／2026-09-24（日本時間）。**状態: 草案3（起草者の見直しの後・設計の巡・二巡目〔最終検分〕の後・登録者の確認の前 |
| 4 | 位置づけの行（裁定の記録の一覧） | - 位置づけ: 段階 B の後・B-lens の後の**登録外の記述**（小さな登録）。計画案 v2.7（内部・非公開）の裁定 D203 と、登録者裁定 D204〜D223（`records/Bl3/rulings-D2 | - 位置づけ: 段階 B の後・B-lens の後の**登録外の記述**（小さな登録）。計画案 v2.7（内部・非公開）の裁定 D203 と、登録者裁定 D204〜D225（`records/Bl3/rulings-D2 |
| 21 | §0 の見直しの直しの行 | - 起草者の見直しで見つけた所を直した: q1 との対応に (vi) の (b) を入れた・(vi) の (b) で止めたときは (i)〜(v) を計算しない・本の計算の中の器の誤りの扱い・独立の再計算の器と申告と段取り | - 起草者の見直しで見つけた所を直した: q1 との対応に (vi) の (b) を入れた・(vi) の (b) で止めたときは (i)〜(v) を計算しない・本の計算の中の器の誤りの扱い・独立の再計算の器と申告と段取り |
| 149 | §6 の見出し（設計事実と正本の SHA16・生成の時刻） | ## 6. 転記行（機械生成・逐語・`records/Bl3/design-facts-Bl3.md`〔SHA16 9C0FB524B45061BD〕・正本 `design/contrasts-Bl3.json`〔SHA | ## 6. 転記行（機械生成・逐語・`records/Bl3/design-facts-Bl3.md`〔SHA16 23EA93EC297C2D64〕・正本 `design/contrasts-Bl3.json`〔SHA |
| 160 | §6-補（原稿と正本の SHA16） | - 置換した転記行: A・B・C・D・E・F（器 `tools/build_draft_Bl3.py`・原稿 `design/design-Bl3-draft3.src.md` SHA16 5CB34A9B5DF8223 | - 置換した転記行: A・B・C・D・E・F（器 `tools/build_draft_Bl3.py`・原稿 `design/design-Bl3-draft3.src.md` SHA16 ED591E714E93134 |
| 161 | §6-補（原稿と正本の SHA16） | - 束縛: 原稿のキー参照を正本 `design/contrasts-Bl3.json`（SHA16 27A4EBFDB946E162）の値で置換した。組み立ての前に束縛検査、後に登録検査と生成器の文字列リテラル検査を走 | - 束縛: 原稿のキー参照を正本 `design/contrasts-Bl3.json`（SHA16 6330B65A0AB503E7）の値で置換した。組み立ての前に束縛検査、後に登録検査と生成器の文字列リテラル検査を走 |
| 399 | §16 の書き足した決まりの見出し | - **起草者の見直しで書き足した決まり**（見直しの記録・外の目を通っていない・登録者の確認で見ていただく所）: | - **起草者の見直しで書き足した決まり**（見直しの記録・裁定 D224・D225 で採った・外の目を通っていない）: |

## 注（事実のみ）

- 見直しの記録は、裁定の後に変える所を「台帳・§0 の直しの行・状態の行」の三つと見込んだ。実際には、ほかに位置づけの行（裁定の記録の一覧）と §16 の書き足した決まりの見出しの二つも変えた。どちらも裁定の記帳に伴う言い方の直しで、決まりの中身は変えていない。§6 と §6-補 の行は、正本と設計事実の SHA16 が変わったので機械で変わった。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
