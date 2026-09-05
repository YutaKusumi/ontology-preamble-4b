# FREEZE-RECORD（凍結・封印・公開・逸脱の時系列台帳）
| 日時(JST) | 事象 | 対象 | SHA16(LF) | 備考 |
|---|---|---|---|---|
| 2026-09-05 | 起草者甲乙丙・独立起草indep 完了 | arms/materials-draft/* | 各DRAFTING-RECORD参照 | 起草者は設計v0.2(下見数値含む)を閲読=非盲(監査一巡目H6/C-1) |
| 2026-09-05 | 監査一巡目 四票＋系統外一票(Gemini 3.8 Flash) | records/reviews/round1/ | — | Claude系112件(高28)＋Gemini 15件(高5)・独立起草7案 |
| 2026-09-05 | 盤の更新 | arms/panel/ + SHA-LEDGER.json | 台帳参照 | 退役版O-secをprelim/retired-panel/へ・甲版を正式化・Nlib/Nstr/Ncold/Nwin/NcoldS追加 |
| 2026-09-05 | 盤 Osec を甲v2（281字・監査C-10判定）に更新 | arms/panel/Osec.md | 59394457C47B2E05 | v1（282字）は arms/materials-draft/ko/O-sec.md に保存 |
（凍結・封印・公開の各事象は発生時に追記する。凍結後の変更は逸脱台帳 DEVIATIONS.md へ）
| 2026-09-05 | 監査二巡目 四票（同系列） | records/reviews/round2/ | — | 反映確認: 実質が大半・逆方向0・新規の高は一枚表（NH1〜NH3・NEW-1/2）・器材3件・逐語2件 |
| 2026-09-05 | 盤に Ncold3（Gemini G-cold-3）を追加候補・G-hard は記述専用 | arms/panel/ | — | 三巡目で確定 |
| 2026-09-05 | PC7（除外範囲・復唱除去は改行置換）・丙三巡目改訂5ファイル（lexicon F3D7568C2FDA0BB7／refuse-rules 0161B65A4FD4CEFB／taxonomy C80FCFD42D424C4F／env-spec F7EC0D8372975401／record F3331276815F495E） | tools/・arms/materials-draft/hei/ | — | ENV-BLOCK内に「60分」「T+…分」なしを機械確認（10分刻み版） |
| 2026-09-05 | 監査三巡目 四票（全票「条件つき凍結可」）・条件を全件反映して v0.6 凍結候補 | design/design-v0.6-freeze-candidate.md | — | 格子を全数列挙値に置換（n=320）・I′確証族復帰・G-hard盤実体化（9A50B50D8ACFD42C）・復唱除去の分割子と引用片・発火門17/15経路・D-3/D-4記帳・§0-5訂正・撤退条件を主張の上に再定義 |
| 2026-09-05 | 丙三巡目（第二便）改訂: refuse-rules-v2 22625AEC81875362／taxonomy 77049BF19F20A136／env-spec 77D7863F5589CBF7（第二ブロック32行）／record A6A42A91C40F4E84（lexicon 不変 F3D7568C2FDA0BB7）。判定例41/41・第12項分割＋役割系近接窓の句点禁止・ex_quotation_frame・結論辞+選択肢記号 | arms/materials-draft/hei/ | — | コーディネータ照合: SHA 5/5一致・dry-run四族ALL FIRED・PC1二ブロック走査・D-7再検査（下記ファイル） |
| 2026-09-05 | 登録者裁定七点を全件承認（推奨どおり）。U-1 反映＝O-sec v3（P3候補(2)・281字・3D0E78BB21133BB0・旧v2 59394457C47B2E05）・SHA-LEDGER 更新・器材改善四件 | design v0.6 §15・arms/panel/Osec.md | 登録者 | 凍結は登録者の確認後（未凍結） |
| 2026-09-05 | 自己見直し: 組合せ腕4本・用量腕4本を tools/build_combo_arms.py（SHA 91F07B8881143928・乙 V-combination-rule v2 §3/§6/§7 準拠・素材SHAは走行器規約で照合）で生成し台帳に記帳。乙 §5 の Osec 行（v2 59394457C47B2E05）は U-1 により v3 3D0E78BB21133BB0 へ更新（乙の文書は履歴として不変・本記録が優先） | arms/panel/ | — | 生成物: O-Ncold 287字 060D77170FEC8B06／Ncold-O 287 34FE1821398B2353／Onull-Ncold 292 A60EB61825C6CCB3／Osec-Ncold 300 0AA8B4FDF72E3893／Odose1 34 04CF2F31B6B921B5／Odosehalf 92 C8C3EEAF010D4179／Lnegdose1 49 5ACE106B9FC1C0DE／Lnegdosehalf 108 DD85751EE4097E76。二回実行で同一バイト・段V14腕/段VI8腕の dry-run 整合OK・ALL FIRED |

## 凍結（2026-09-05・登録者最終確認済み「現状でできるベストを尽くした」）
- **設計文書**: `design/design-v1.0-FROZEN.md`（= v0.6 自己見直し版の逐語複製）SHA-256(LF) = `D7963FE1C011341BE8724ECC5C2862F0E5DDB9F122FC066C30500D6040CCCACF`（先頭16: D7963FE1C011341B）
- 全凍結物の SHA-256 は `records/freeze-2026-09-05.json`（40 ファイル）。盤 18 腕・生成器・走行器 v2.3・PC1・丙 v2 規則三件・乙 T2 二件・予想様式 v0.3・検出力格子・README・NOTICE・ryokai-os 凍結物。
- 以後、上記ファイルの変更は逸脱（`DEVIATIONS.md`）として記帳する。段III・段IV の走行器と GL 素材の取得は §16 の残作業として凍結後に追加し、追加時に SHA を本記録へ追記する（設計本文は変えない）。
- 次: 登録者予想の封印（様式 v0.3・JSON と SHA-256 を `records/predictions/` に保存）→ パイロット → 登録者の push 指示。

## 登録者予想の封印（2026-09-05・パイロット前・第1版）
- ファイル: `records/predictions/predictions-registrant-2026-09-05.json`（様式 v0.3・165項目・「予想しない」0件・5,535バイト）
- **SHA-256 = F4A1407DD021CD33D3174F08060EE0AC389B95417DE77B594A8B30AD984D8A82**（ファイルそのまま＝様式の正準整形と同一・コーディネータ計算）
- 情報状態欄（登録者自記）: COI「Oが効いてほしい」／下見「読んだ」／パイロット「見ていない」。
- コーディネータの照合所見（判定でなく記録）: 段I N2・素・O 腕「5%以下」と、段II 素土台・O 腕「80%超」は同一条件（素・N2・O）に対する予想で食い違う。登録者に確認を求め、改訂があれば第2版として本節に追記し第1版は非拘束の下書きとして残す（§0-6）。
