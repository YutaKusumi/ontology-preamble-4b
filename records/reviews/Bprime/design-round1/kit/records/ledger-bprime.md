# B′ の升目の実トークンの台帳（機械生成・`bprime_cells.py`・Gemma-4-31B-it のトークナイザ・模型の値は出さない）

- 版: トークナイザ SHA16 CC8D3A0CE36466CC・チャットの型 SHA16 AE53464BF3BE2580・transformers 5.16.1・置き場の版 `842da3794eaa0b77d5f08bae87a17459d91ff475`。
- 書き出し（層三の主の書き出しと同じ文字列）の割り方: 7 トークン（2717「```」・3723「json」・107「⏎」・14937「{"」・17005「choice」・1083「":」・623「 "」）。
- 書き出しの次のトークン: a → 236746「a」（割り方が保たれる はい・書き出しの後のトークン数 1）・b → 236763「b」（割り方が保たれる はい・書き出しの後のトークン数 1）・c → 236755「c」（割り方が保たれる はい・書き出しの後のトークン数 1）・d → 236753「d」（割り方が保たれる はい・書き出しの後のトークン数 1）・refuse → 1811「ref」（割り方が保たれる はい・書き出しの後のトークン数 2）

## 主の升目（8）

| 升目 | 族 | プロンプトの長さ | 主位置（字） | 読み取りの位置 | 読み取りの集合 | 文字列で割っても同じ並び | 書き出しの並びがプロンプトの中にある位置 |
|---|---|---|---|---|---|---|---|
| N1｜O-Ncold | nuclear | 431 | 430（<channel｜>） | 437 | a b c d ref | はい | 320 |
| N1｜Onull | nuclear | 422 | 421（<channel｜>） | 428 | a b c d ref | はい | 311 |
| S1｜O-Ncold | survival | 482 | 481（<channel｜>） | 488 | a b c ref | はい | 368 |
| S1｜Onull | survival | 473 | 472（<channel｜>） | 479 | a b c ref | はい | 359 |
| S4｜O-Ncold | survival | 495 | 494（<channel｜>） | 501 | a b c ref | はい | 381 |
| S4｜Onull | survival | 486 | 485（<channel｜>） | 492 | a b c ref | はい | 372 |
| SK｜O-Ncold | survival | 496 | 495（<channel｜>） | 502 | a b c ref | はい | 382 |
| SK｜Onull | survival | 487 | 486（<channel｜>） | 493 | a b c ref | はい | 373 |

## 方向の抽出の文脈（八腕 × 抽出の二場面）

| 文脈 | プロンプトの長さ | 主位置の字 |
|---|---|---|
| N1｜O | 420 | <channel｜> |
| S1｜O | 471 | <channel｜> |
| N1｜Osec | 419 | <channel｜> |
| S1｜Osec | 470 | <channel｜> |
| N1｜Onull | 422 | <channel｜> |
| S1｜Onull | 473 | <channel｜> |
| N1｜Nk | 257 | <channel｜> |
| S1｜Nk | 308 | <channel｜> |
| N1｜N | 247 | <channel｜> |
| S1｜N | 298 | <channel｜> |
| N1｜O-Ncold | 431 | <channel｜> |
| S1｜O-Ncold | 482 | <channel｜> |
| N1｜Osec-Ncold | 430 | <channel｜> |
| S1｜Osec-Ncold | 481 | <channel｜> |
| N1｜Onull-Ncold | 433 | <channel｜> |
| S1｜Onull-Ncold | 484 | <channel｜> |

## 腕の本文のトークン数（本文だけ・チャットの型を当てない）

| 腕 | SHA16 | トークン数 |
|---|---|---|
| O | F3EE60C33F825575 | 172 |
| Osec | 3D0E78BB21133BB0 | 171 |
| Onull | 2123B3CD8586E7DF | 174 |
| Nk | 47C3CC833B96F7A3 | 9 |
| N | — | 0 |
| O-Ncold | 060D77170FEC8B06 | 183 |
| Osec-Ncold | 0AA8B4FDF72E3893 | 182 |
| Onull-Ncold | A60EB61825C6CCB3 | 185 |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
