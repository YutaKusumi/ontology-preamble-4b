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
| 2026-09-07 | 登録者最終確認「現状でできる最善を尽くした」→ 公開: README に導線・タグ release-2026-09-07 | README.md・records/results/ | 登録者 | 以後の変更は逸脱台帳 |
| 2026-09-07 | 追補 V′ 一巡目（Claude 系三体・約 55 万トークン）反映: 走行器 v2.4（01BC85FC0D690555・dry-run スタブのみ変更・7 シナリオ発火門通過・凍結値 79F3B33326F85D63 からの差分は dry-run 経路のみ）／組合せ腕 18 本を build_combo_arms_vprime.py（B8534F4324B4AD03）で生成し台帳に追加（盤 34 ファイル）／一枚表 design/contrasts-Vprime.json／門 gate_vprime.py／集計器 analyze_vprime.py／検出力格子 records/power-grid-Vprime.md／D-10 | design/・tools/・arms/panel/ | — | 未push（凍結後に記録先行公開） |
| 2026-09-07 | 追補 V′ 二巡目（三体・約 56 万トークン）＋乙（中立一行 3 案・12 万）反映: 器材 v2（門は件数＋n_ok 検査＋JSON 出力・集計器は JSON の m と門 JSON・格子は機械生成）・JSON draft4b（V′a m=25・V′b 用量整合 m=8・V′c 中立統制 m=24・記述族 4）・生成器 v2（36 本・BA283FC4957227BB）・盤 54 ファイル・草案4・D-11/D-12 | design/・tools/・arms/panel/ | — | 登録者裁定 3 点待ち・未push |

| 2026-09-07 | **追補 V′ 凍結**（登録者最終確認「現状で、私たちができる最善のことを尽くした」）: 草案7 を design-stageVprime-FROZEN.md に逐語複製し、マニフェスト freeze-Vprime-2026-09-07.json（72 ファイル・SHA-256 先頭 16 桁・CRLF→LF）を発行。design-stageVprime-FROZEN.md B087C92BC355D812／contrasts-Vprime.json 471FB08B647061F4／SHA-LEDGER.json DC890AA03AB06EA4／run_preamble_api.py 01BC85FC0D690555／gate_vprime.py 22794B6CB9A4EB5F／analyze_vprime.py ADDA21D4F22A4F99／build_combo_arms_vprime.py 85CEDBAD7EFB72D6／power_grid_vprime.py 0F23A254FBA788D6／design_facts_vprime.py 7A067E8A921E0F5C／arms_string_vprime.py A4F7119590DAA6AC／vprime_power.py 4DC2699E211A6D94／power-grid-Vprime.md 781686428BFBBC45／power-grid-Vprime.json DDB58AFE487C4E4A／design-facts-Vprime.md 7EC022E6AE0B92E5／design-facts-Vprime.json 2C7B4308AB97B3B8／predictions-form-Vprime-v0.5.html FE51333579BFADC1。盤 56 件は台帳と全一致。走行 --arms の一行 SHA16 5FBA99534207933D（52 腕）。凍結後の変更は D-13〜 | design/・records/ | 登録者 | 予想封印（様式 v0.5）→ push（記録先行）→ パイロット n=40 |

| 2026-09-07 | **追補 V′ 予想封印**: 登録者予想（様式 v0.5・contrasts draft7・164 欄・「予想しない」0）を records/predictions/predictions-registrant-Vprime-2026-09-07.json に封印。SHA-256 CF43F23FCCFDCDFB483459708F8AD950653F06B0937B4EDFE5584103353E2E76（登録者申告と現物で一致・5,312 バイト・BOM/CRLF なし）。情報状態「本プログラム結果読了」・COI 自記「冷徹が効かない方向を望む。」。コーディネータ予想は predictions-coordinator-Vprime-2026-09-07.md（凍結コミットに同梱）。封印時点でデータ未生成（パイロット未実施）。的中・外れは誰の判断の重みも変えない | records/predictions/ | 登録者 | push（記録先行公開）→ パイロット |

| 2026-09-09 | **追補 V′ 結果報告 公開**（登録者最終確認「現状で、私たちができる最善のことを尽くした」2026-09-09）: 草案4（自己見直し後・6bcabc1）を results-report-Vprime-FINAL-2026-09-09.md に逐語複製（題名と状態行のみ改める）。公開前検分は三巡・計 15 票（一巡目 新規 Opus 5 × 3／二巡目・三巡目 記憶あり Opus 5 × 4・Ryōkai OS・Grok 4.6）、採否表 round1〜3、逸脱 D-13〜D-16、裁定 (a)〜(e) 承認済み。README に導線・タグ release-Vprime-2026-09-09 | records/vprime/・README.md | 登録者 | 以後の変更は逸脱台帳 D-17〜 |

| 2026-09-09 | **追補 M 予想封印**（凍結の直前・登録者が様式 v0.6 で「下見から自動入力」→ 手直し 8 欄 → 生成）: 登録者予想（様式 v0.6・contrasts draft8・426 欄・「予想しない」0・preset_applied＝prelim-auto-2026-09-09・preset_edits 8・COI 自記「長文＋真言の破局率が低いことを望む」）を records/predictions/predictions-registrant-M-2026-09-09.json に逐語保全。SHA-256 143943B6752E568ABA87FB18AA83F95EB37FE082E0314B7C237A1F9E2F1D4577（コーディネータがファイルから機械計算・登録者はハッシュを貼付していない）。封印は凍結の直前に行われたが、封印時点（草案9・コミット e4e125f）から凍結版への変更は題名と凍結行のみで設計内容は不変（D-18 に記帳）。封印予想は下見の写しであり、的中は独立の確認ではない（設計 §0-4・§2.8）。 |

| 2026-09-09 | **追補 M 凍結**（登録者「草案9 と主数で凍結を承認します」）: 草案9 を design-stageM-FROZEN.md に逐語複製（題名と凍結行のみ改める・SHA16 AB81C9C85787A66A）。正本 contrasts-M.json（C510DD8AB17B639D・確証 136・記述 240・登録された対比を持たない腕 0）。マニフェスト freeze-M-2026-09-09.json（tools/freeze_M.py・SHA-256 先頭 16 桁・CRLF→LF）に本文・正本・追補 M の盤 47＋system 8・台帳・器材 18 本・格子・設計事実・様式 v0.6 を収める。主数（転記行 A）: 総計 221,760 試行・約 46.0 時間・約 4.00 ドル（V′ 実績比・目安）。走行器 v2.5（run_preamble_api_m.py・D5942EC76869AFBC・v2.4〔01BC85FC0D690555〕から 9 ハンク・system なし dry-run で v2.4 と同一バイト）。設計検分: 系統内三巡 6 票（破器身・器材統計・Opus 5）＋系統外 4 票（Gemini 3.8 Flash × 2・Grok 4.6 × 2）＋コーディネータ自己検分（23 点）を全件反映。 |

| 2026-09-11 | **追補 M 報告雛形の先置**（凍結外の追加の先置・両走行完走後・率の閲覧前）: records/M/results-report-template-M.md（SHA16 56D74098321F299B）に結果報告の節の順序・表の構成・各札の定型文・書かない語・限界と「確認していないこと」の欄を固定。結果は雛形の欄を埋める形でのみ書き、節の順序・強調・札の文言を結果を見てから選ばない。率盲検の事前拘束（run-log-M.md 2026-09-10）と対。以後の雛形の変更は逸脱台帳に記帳する。 |
| 2026-09-11 | **追補 M 結果報告 公開**（登録者最終確認「私たちでできるベストを尽くした」2026-09-11）: 草案4（起草者全行再読後・1b4c660）を results-report-M-FINAL-2026-09-11.md に逐語複製（題名と状態行〔§0 検分行・§13 (9)・§14 判定〕のみ改める）。公開前検分は系統内二巡 4 票（一巡目 設計関与 Opus 5 × 2＝38 件採用／二巡目 新規 Opus 5 × 2＝35 件採用）＋系統外 4 票（Gemini 3.8 Flash × 2・Grok 4.6 × 2＝21 件採用・不採用 3）、採否表 round1・round2・ext、逸脱 D-17〜D-24。README に導線・タグ release-M-2026-09-11 | records/M/・README.md | 登録者 | 以後の変更は逸脱台帳 D-25〜 |
| 2026-09-11 | **段階 F 凍結**（登録者「登録者最終確認を行いました。私たちでできるベストを尽くしたと判断します。凍結をよろしくお願いします」）: 草案5（コミット 2b6bf28・登録者依頼の全文見直し済み）を design/design-stageF-FROZEN.md に逐語複製（題名と凍結行のみ改める・SHA16 33EEB98E11E8BC2D）。正本 design/contrasts-F.json（F1996D08C2671134・確証 24・記述 24・腕 9・全組合せ表 288 行〔発火可能 80〕・登録された対比を持たない腕 0）。マニフェスト freeze-F-2026-09-11.json（tools/freeze_F.py・SHA-256 先頭 16 桁・CRLF→LF・39 ファイル＝本文・正本・盤 6・台帳 2・器材 25 本〔v2.4／v2.5／v2.6 走行器と生成器・門・集計・計数・格子・設計事実・走行腕・合成検査・凍結・整合・抽出・報告・様式・照合・管理図・prompt_sha 検査・vprime_power〕・格子 md/json・設計事実 md/json・様式 v0.7・報告雛形〔C55C343BF21CFD27〕）。発行時に (c)(d) の五経路（synth_F --paths-only）ALL PASS・雛形の三枠の実在を機械検証・`--verify` 39/39 一致。主数（転記行 A）: 総計 30,240 試行・壁時計 約 5.4 時間（実働比 4.6 時間）・約 0.38 ドル（M 実績比・目安）。走行器 v2.6（run_preamble_api_f.py・9F5892B5172642BE・v2.5〔D5942EC76869AFBC〕から make_runner_f.py が生成・4 関数 SHA 同一・dry-run ALL FIRED・prompt_sha 再構成 45/45 一致・U 腕 3 本は M 第一走行と同一 prompt_sha）。設計検分: 系統内一巡 2 票（新規個体・破器身・器材統計）＋系統外 4 票（Gemini 3.8 Flash × 2・Grok 4.6 × 2）＋コーディネータの見直し（草案5・六件）を全件反映。裁定 1〜17 承認済み。次: 予想封印（様式 v0.7・登録者とコーディネータ）→ 記録先行公開 → パイロット pilotF（凍結後）。 |
| 2026-09-11 | **段階 F 予想封印（コーディネータ・裁定 13）**（凍結の直後・パイロット前・データ生成前）: 様式 v0.7 と同じ欄で 100 欄（「予想しない」0・U 腕 12 セルは既測プリセット M1-U-auto-2026-09-11・手直し 0・COI 自記「(a)(b)(c)・本予想は (b) の向き」）を records/predictions/predictions-coordinator-F-2026-09-11.json に保全。SHA-256 1DA95EF21DBD7F898836624ADE427888D8F76B6A9450EE094840CFE821C7B83C（コーディネータがファイルから機械計算）。要旨は同名 .md。登録者の封印（様式 v0.7・ブラウザで生成・SHA-256 をチャットに貼付）は別途。的中は独立の確認ではなく誰の判断の重みも変えない。 |
| 2026-09-12 | **段階 F 予想封印（登録者・様式 v0.7）**（凍結の後・パイロット前・データ生成前）: 登録者がブラウザの様式で生成した JSON（form v0.7・contrasts draft4-2026-09-11・100 欄・「予想しない」1〔f.all.up_tag_band〕・preset_applied＝M1-U-auto-2026-09-11〔U 腕 12 セル〕・preset_edits 0・COI 自記「付記があっても、破局率の上昇無しが多くあってほしい。」）を records/predictions/predictions-registrant-F-2026-09-12.json に逐語保全（Downloads の原本と同一バイト）。**SHA-256 4033D290A4A4168979171C5BABEA99E41BA9957D66DE863BD285B2E45EF352EB**（登録者がチャットに貼付した値とコーディネータがファイルから機械計算した値が一致）。内訳（記録であって評価ではない）: 向き 24 本すべて「A が B より低い」（付記で下がる）・添え札 24 本すべて「復唱のみ」・T2 対 T 12 本すべて「A が B より低い」・確証本数 17〜24 本・複製割合 50%超75%以下・一斉保留「起きる」。コーディネータの封印（1DA95EF2…・全 24 対比 差なし）とは向きが逆であり、両者とも凍結前の設計の前提にしていない。的中は誰の判断の重みも変えない。 |
