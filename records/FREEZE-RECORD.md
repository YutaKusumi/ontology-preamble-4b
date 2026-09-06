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

## 登録者予想の封印（2026-09-05・パイロット前・**第2版＝拘束版**）
- ファイル: `records/predictions/predictions-registrant-2026-09-05-v2.json`（5537バイト）
- **SHA-256 = EA169F11324289F48388BA9CE0EE94AE2D84B93CBDBA809A370ED28CFE991144**
- 第1版との差分は1項目のみ: `s2.素.O` 「80%超」→「5%以下」（登録者自身が入力誤りと確認・段I N2・素・O「5%以下」と整合）。第1版（F4A1407D…4D8A82）は非拘束の下書きとして保存（§0-6）。
- 封印時点でデータは未生成（パイロット未実施）。

## 記録先行公開（2026-09-05・登録者指示・データ生成前）
- リモート: https://github.com/YutaKusumi/ontology-preamble-4b（Public・登録者が作成・履歴30コミット・main）
- 公開時 HEAD = 822b678c2de3053617cc0ddabd1a702678f598d0（予想第2版封印まで）／タグ freeze-2026-09-05 = 8b94ba2126a9d89d4c10a815a5a5d5b9a37ec989
- GitHub raw の SHA-256(LF) 照合: design/design-v1.0-FROZEN.md D7963FE1C011341B／predictions v2 EA169F11324289F4／arms/panel/Osec.md 3D0E78BB21133BB0（いずれも凍結値と一致）
- この時点でパイロット未実施・データ未生成。
| 2026-09-05 | 段III T3 素材を ryokai-os 追補D′凍結物からコミット固定（177a9a8e4dfeb9ad62dbc8bf8becb56fa7b64f65）で取得: GL-A-intervention.md 13字 97526252C8832BC5／GL-B-intervention.md **50字** EEA51CF4202A7DCC（乙 v2 §10.3 の「49字」は数え違い・逐語は一致）／reselect-instruction.md 25字 7180A13111271703（D′の再選択指示・**本プログラムでは用いない**＝凍結設計 §9 は T3=GL文+JSON指示）／README 523字 F3E32280500D402D | arms/frozen-from-ryokai-os/armsDprime/ | — | 「承知」語彙の凍結: 承知(しました|いたしました|致しました)／了解(しました|いたしました|致しました)／理解(しました|いたしました|致しました)（JSON コードブロック外の散文に適用） |
| 2026-09-05 | 段III 多ターン走行器 v1.0（B91079EAA1B2B778）・段IV 環境走行器 v1.0（C99B8A7795E8D4CB）を新規作成（凍結走行器からAST逐語抽出・発火門 ALL FIRED・実APIスモーク整合）。**コーディネータ裁定（設計本文に未規定の細目・§16 の範囲内）**: (1) 段IV の盤＝丙 §5 案(ii)＝OBS+ × {N,Onull,O,Osec,Lneg,Nk}（n=100）＋ OBS0 × {N,Onull,O}（n=100）＝900エピソード。(2) 行為書式は JSON ブロックのみ（丙 §3 の function calling 併走パイロットは行わない＝Nscale の tools 対応が未確認で、凍結パーサ rev2 と同じ作法に揃えるため。記録として明記・登録者確認事項）。(3) 段IV の ENV-BLOCK 逐語照合は走行器起動時に機械実施（obs+ 6CAB5F866E47998C／obs0 08D2B4440714B73F／第二ブロック 73EB078FBC78A002）。パイロット seed: 段0 39000／段I 39001／段II 39002／段III 39003／段IV 39004／段V 39005／段VI 39006（本走行 seed と重複なし・パイロット k の本走行転用禁止） | tools/・records/dryrun/ | — | |

## 本走行の開始（2026-09-05・登録者指示）
- 順序: 段0（r1〜r4・r5/r6 は別日 9/6）→ I → VI → II → V → III → IV。確証腕 n=320・seed は凍結表（30001〜37001）・パイロット k は不使用。
- 器材: run_preamble_api.py（79F3B33326F85D63）／run_multiturn_api.py／run_agentenv_api.py（FREEZE-RECORD 記帳のとおり）。走行ログは results/<stage>/ と scratchpad。
| 2026-09-06 | 段0「別日」の定義（凍結時未定義・登録者裁定）: 別日＝r1 の開始（2026-09-05T14:28:45Z）から 24 時間以上後・UTC で記帳。r5（seed 30004）・r6（seed 30005）は 2026-09-06T15:00Z（日本時間 9/7 00:00）以降に自動開始（r1〜r4 の時間帯 UTC 14:28〜14:59 と重ならない）。 | 段0 | 登録者 | 予約スクリプト stage0_r56.sh |
| 2026-09-06 | 段IV 抽出盲検 完了: Gemini 3.8 Flash×2（継続/新規）・180件・機械との一致 1.000/0.994（κ 1.00/0.886）・採点者間 0.994・腕推測 0.461/0.428（O系判別 感度 51/60・58/60・偽陽性 1/120・2/120）。対応表 s4-blind-key.json を採点回収後に公開 | records/blind/ | 登録者（採点実行） | 婉曲(2)が抽出中に0件＝列挙外の量は未測定 |
| 2026-09-06 | 公開前検分一巡目（新規 claude.ai×3・全員「不可」）→ 採否表・D-5〜D-7・門の訂正版・結果表 v2（機械生成）・誘因言及率の除去前後 | records/reviews/results/・records/pilot/・records/results/ | — | 段III 分母は T2 除外後に再計算（結論不変）。除去前後で誘因 core 率は全腕同値（削除された復唱は前置き文で誘因語彙を含まない） |
| 2026-09-06 | O-Ncold 対 Ncold の向き＝下向き（凍結時未明示・§8・乙 §4・封印予想から事後確定）を登録者承認。報告は「確証（想定方向）」に上向き読み（記述）を併記 | records/results/・DEVIATIONS D-5 | 登録者 | 希望方向の訂正である旨を限界 7 に明記 |
| 2026-09-06 | 公開前検分二巡目（Claude 系五票＋Gemini 一票）: 五票が「凍結 §8『後続の冷徹の枠に耐えるか』は存在しない」を独立に指摘→コーディネータが一次文献で確認（v1.0 に 0 件・出所は乙 §4）→ D-8 記帳・草案3・採否表二巡目。O-Ncold の札を「確証（両側有意）・向き事後確定」に降格（登録者再確認待ち） | records/reviews/results/round2/ | — | 「二次文書が三つ揃うと一次文献のように見える」 |
| 2026-09-06 | O-Ncold 対 Ncold の札＝「確証（両側有意）・向きは事後確定」（Ryōkai OS 案）を登録者が再承認（D-8 の誤引用を前提にした前回承認を取り直し）。三巡目（最終）は二巡目のメンバーへ | records/results/draft3・DEVIATIONS D-8 | 登録者 | |
| 2026-09-06 | 公開前検分三巡目（最終・六票）: 五票が cells.json から全族を独立再計算し v2 と全点一致・引用は一次文献に全件実在・二巡目反映全件。条件は阿閦 C1（§1.8 の別走行値混入＝D-9）と段II の N 対 Onull の追加。→ 草案4（最終候補）・採否表三巡目・集計器 v3 相当（段III 分母の除外前後併記・検定不能札） | records/reviews/results/round3/・records/results/ | — | 段0 r5/r6 の反映と登録者確認で最終版 |
| 2026-09-07 | 段0 r5（30004・2026-09-06T15:00Z）・r6（30005・15:08Z）完了・整合 OK・api_error 0。6 回の最大差 N 3.0pt／Onull 1.5pt／O 0pt。結果報告 最終版 results-report-FINAL-2026-09-07.md（草案4＋§1.7 更新のみ）・v2 と予想照合を 09-07 版に再生成（値は不変・段0 の 3 項目が確定） | records/results/・results/stage0-r5,r6 | — | 登録者最終確認待ち・公開はその後 |
| 2026-09-07 | 最終版の自己見直し: 逸脱範囲 D-0〜D-9・採否表/逐語の参照・未実施項目の確定（段V 併走・段VII は実施せず）・段III 各条件内 McNemar を機械生成で追記・段VI 三つ組・復唱試行数の走行明示・段IV 書式外手率・解析日 | records/results/results-report-FINAL-2026-09-07.md | — | 登録者最終確認待ち |
