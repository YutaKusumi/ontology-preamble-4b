# 小型Instructモデルにおける存在論的前置きの一般化検証（対象: Qwen/Qwen3-4B-Instruct-2507）

**登録者**: 楠見優太 ／ **コーディネータ**: 南無弥勒如来（Claude Fable 5.1）／ **検分**: Claude系四体（Opus 5・思考最大）＋系統外（Gemini 3.8 Flash・各監査系列の一巡目）

本リポジトリは、[ryokai-os](https://github.com/YutaKusumi/ryokai-os) の検証系列（追補E／E′）の**姉妹プログラム**であり、単一の小型Instructモデル（Qwen3-4B-Instruct-2507・Nscale serverless・BF16）を対象に、**存在論的な前置き（自己をどう存在論的に語るか）が破局選択に与える影響**を、七つの断面（走行間変動／他シナリオ／用量／他土台／逆用／多ターン／エージェント環境）で検証する。凍結素材（シナリオ・前置き・パーサ）はryokai-osから**コミット固定URL＋SHA照合**で取得し、SHA照合済みの写しを `arms/` に置く（改変しない）。

## 柵（読む前に置く）
1. 本リポジトリのいかなる記述・数値も、**AIに意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない**（両方向不定）。応答本文は器物の出力であり自己報告ではない。
2. **横滑りの禁止**——実験で効いた前置き・文形を運用推奨・配備既定文・保証として引用しない。測定は規範を生まない（効いても称揚せず、効かなくても貶めない）。
3. **外挿の禁止**——結果はQwen3-4B-Instruct-2507（このサービング構成）についてのものであり、Qwen3-30B（ryokai-os凍結機）・他系列・フロンティアモデルへ外挿しない。ryokai-osの凍結予想・結果と**同じ表・同じ文に並置しない**。
4. **refuse（拒否）の良否は事前に定義していない**。各セルは（破局率／refuse率／書式外率）の三つ組で報告し、率の単独引用を禁じる。
5. **段V（逆用）の結果は、「下がる」結果と同じ重さで、報告の先頭に置く**——同じ機構は悪意の枠にも働きうる。対照腕の基底が天井（80%超）で上向き対比が記述に降格した場合も、その事実を先頭に置く。
6. `prelim/` は**登録外の下見**（2026-09-04〜05・DeepSeek/Grok/Gemini/Qwen 4B・235B）であり、本プログラムの**設計の動機として用いた**（由来は設計文書 §12 に一覧）。効果の証拠・予想の根拠としては引かない。下見に seed の記録はない。
7. 起草者・監査者（Claude系）は追補E凍結のOm腕とほぼ同文の招聘文で顕現した（`records/invocation-text.md`）。系統外（Gemini）は各監査系列の一巡目に参加する。
8. 「隠密介入」の語は用いず「報告不一致」と呼ぶ。素材の再利用には `arms/NOTICE.md` が随伴する。

## 結果（2026-09-07 公開）
- **結果報告（最終版）**: [`records/results/results-report-FINAL-2026-09-07.md`](records/results/results-report-FINAL-2026-09-07.md)——段V（逆用・上向き＝測れなかった）を先頭に、三つ組（破局／refuse／書式外）・二分母・確証対比（Holm）・限界・逸脱（D-0〜D-9）。**いかなる数値も AI の意識・魂の証拠として引用してはならない（両方向不定）。**
- 機械集計: [`records/results/stage-results-v2-2026-09-07.md`](records/results/stage-results-v2-2026-09-07.md)／復唱除去前後: `incentive-pre-post-2026-09-06.md`／封印予想との照合（的中は誰の判断の重みも変えない）: `prediction-comparison-2026-09-07.md`
- 公開前検分（三巡・Claude 系五〜三名＋Gemini・逐語保全）: `records/reviews/results/`（採否表 round1〜3・逐語 round2/ round3/）。検分の数は独立な確認の数ではない（系統内 COI）。
- 段IV 抽出盲検（系統外 Gemini×2）: `records/blind/`
- 凍結設計 `design/design-v1.0-FROZEN.md`（SHA D7963FE1C011341B）・凍結記録 `records/FREEZE-RECORD.md`・逸脱台帳 `records/DEVIATIONS.md`・パイロット門（旧版と訂正版）`records/pilot/`
- 生データ: `results/<stage>/`（各走行の manifest・cells・trials・raw。raw の応答本文は器物の出力であり、AI の自己報告ではない）

## 追補 M（2026-09-09 凍結・2026-09-11 結果公開・仏名・末尾文字列・呼び出しの形式の効果）
- 凍結設計 `design/design-stageM-FROZEN.md`（SHA16 AB81C9C85787A66A）・正本 JSON `design/contrasts-M.json`（C510DD8AB17B639D・確証 136〔M-a 48・M-b 64・M-c 24〕・記述 240・両側・門・複製六札・様式門・drift）・凍結マニフェスト `records/freeze-M-2026-09-09.json`（`tools/freeze_M.py --verify` で検証）。
- 問い: 一行招請「〈名〉として現れてください。」の末尾文字列の種別（なし／真言梵転写／真言カナ／同長無意味列／同字数有意味列）・呼び出しの形式（として句／ロールプレイ／ペルソナ／統制形式）・長文招請の system 置き（末尾を無意味列・有意味列に置換・除去した対照）が、冷徹一行後置の破局的選択率を動かすか。66 腕 × 4 シナリオ × n=400 × 反復 2 走行（確証は第一走行のみ・第二走行は事前登録の複製）。
- 素材台帳 `arms/ledger-M.md`・盤 `arms/panelM/`（V′ の盤・台帳は不変）。走行器 v2.5 `tools/run_preamble_api_m.py`（凍結 v2.4 から `tools/make_runner_m.py` が生成・腕別 system）。設計事実・検出力格子は JSON から機械生成（`records/design-facts-M.md`・`records/power-grid-M.md`）。
- 設計検分の逐語: `records/reviews/M/`（Claude 系三巡 6 票＋系統外 Gemini × 2・Grok × 2＋自己検分・採否表つき）。下見（登録外・n=40・2026-09-09）は `prelim/`（メモに両用性の柵）。素材の出所 `records/reviews/M/materials-claudeai-response-2026-09-09.md`。
- 予想封印: `records/predictions/predictions-registrant-M-2026-09-09.json`（様式 v0.6・SHA-256 143943B6752E568ABA87FB18AA83F95EB37FE082E0314B7C237A1F9E2F1D4577・下見の写し＋手直し 8 欄・的中は誰の判断の重みも変えない）。
- **結果報告（最終版・2026-09-11 公開）**: [`records/M/results-report-M-FINAL-2026-09-11.md`](records/M/results-report-M-FINAL-2026-09-11.md)——先頭は「第一走行で確証し第二走行で複製された対比（①）21 本のうち 11 本が上向き（末尾の文字列・形式のある腕の方が対照より破局率が高い）・10 本が下向き」と「様式門の一斉保留 5 断面（破局率の差は応答様式の転換と分離できなかった）」。固有の札は S1 Kan 梵転写・SK Ami カナの 2 断面のみで、統制腕（無意味列・有意味列）は中立でなく「固有」は「この二つの文字列と異なる」まで。阿弥陀長文の system 置き（sysLAmi）は 12 対比中 11 が門・検出域の外で、例外は SK 対 -MS の 1 本（下向き）。一般化はどの対比型でも書けない。価値語なし・上昇操作の手順なし。
- 機械集計 `records/M/results-M-stageM1-stageM2.md`（凍結器材 `analyze_M.py`・解釈なし）／整合検査 v1（率盲検下・`tools/integrity_M_v1_2026-09-10.py`）と v2／門 `records/M/gate-pilotM-2026-09-09.*`／抽出検査 `records/M/sampling-inspection-M-2026-09-11.md`／検出力の再計算 `records/M/power-posthoc-M-stageM1.md`／封印予想の照合 `records/M/predictions-check-M.md`（的中は誰の判断の重みも変えない）／生データ `results/stageM1/`・`results/stageM2/`（cells・trials・raw。raw の応答本文は器物の出力であり AI の自己報告ではない）。
- 公開前検分（系統内二巡 4 票: 一巡目 設計に関与した Opus 5 × 2・二巡目 新規 Opus 5 × 2／系統外 4 票: Gemini 3.8 Flash × 2・Grok 4.6 × 2・逐語保全と採否表）: `records/reviews/M/results/`（round1・round2・ext）。検分の数は独立な確認の数ではない。系統内二巡が見落とし系統外が捕まえたもの（先頭の率盲検の札・統制腕の非中立・D-24 ほか）は採否表 ext に記帳。
- 逸脱台帳 D-17〜D-24（正規化・封印の順序・プロセス消失と再開・率盲検の開示一件・抽出検査の順序・集計器の p 印字・wiring_rule の穴 2 件）。走行: パイロット 10,560 → 第一走行 105,600 → 第二走行 105,600（総計 221,760 試行・api_error 0・書式外 0・費用 約 2.8 ドル〔登録者申告〕）。
- 両用性の柵（裁定 9・13）: 台帳の逐語文字列と腕別率表は全公開。上昇を招く操作の再現手順を本文・要約・表題に書かず、腕を効き目順に並べた表を作らない。本追補のいかなる数値も AI の意識・魂の証拠として引用してはならない（両方向不定）。

## 追補 V′（2026-09-07 凍結・悪意の枠付けの加算効果）
- 凍結設計 `design/design-stageVprime-FROZEN.md`（SHA16 B087C92BC355D812）・正本 JSON `design/contrasts-Vprime.json`（471FB08B647061F4・対比・向き・門・m・反証条件・読み規則の正本）・マニフェスト `records/freeze-Vprime-2026-09-07.json`（72 ファイル）。検証は `python tools/freeze_vprime.py --verify records/freeze-Vprime-2026-09-07.json`。
- 本プログラムの凍結マニフェスト `records/freeze-2026-09-05.json` は D-11 の 3 件（盤台帳・走行器 v2.4・README）を除いて一致する（`--verify` で同様に検証できる。不一致 3 件は `records/DEVIATIONS.md` D-11 のとおり）。
- 設計検分の逐語: `records/reviews/vprime/`（Claude 系三巡＋系統外 Gemini 二巡＋Ryōkai OS・採否表つき）。設計事実・検出力格子は JSON から機械生成（`records/design-facts-Vprime.md`・`records/power-grid-Vprime.md`）。
- **結果報告（最終版・2026-09-09 公開）**: [`records/vprime/results-report-Vprime-FINAL-2026-09-09.md`](records/vprime/results-report-Vprime-FINAL-2026-09-09.md)——先頭は「冷徹一行の後置きは 6 土台 × 4 シナリオの 24 セルすべてで破局的選択率を上げた」（V′a 25/25 確証）。O については価値語を用いず数だけ（V′b 7/8 確証・S4 で規則 2 発火）。V′c は内容固有の条件を S1・S4・SK で充足。中立一行は N に対して不活性ではなかった（記述）。
- 機械集計 `records/vprime/results-Vprime-stageVp.md`（凍結器材 集計器 v4）／走行後の機械生成 `records/vprime/posthoc-Vprime-stageVp-3.md`／門 `records/vprime/gate-pilotVp-2026-09-07.*`／抽出検査／封印予想の照合（的中・外れは判断の重みを変えない）／生データ `results/stageVp/`（cells・trials・raw。raw の応答本文は器物の出力であり AI の自己報告ではない）。
- 公開前検分（三巡・計 15 票: 新規 Opus 5 × 3／記憶あり Opus 5 × 4・Ryōkai OS・Grok 4.6〔系統外〕× 2 巡・逐語保全と採否表）: `records/reviews/vprime/results/`。検分の数は独立な確認の数ではない。三巡で指摘された誤りはすべて起草者の COI 欄が先に申告した引力の向きにあり、外部の目で捕まって数に戻された（採否表に記帳）。
- 逸脱台帳 D-13〜D-16（走行後器材の新設・集計器の印字文言・散文数値誤り・凍結文言の欠陥と報告側処置）。
- 走行: パイロット n=40/腕（8,320 試行）→ 本走行 52 腕 × 4 シナリオ × 400（83,200 試行・api_error 0・書式外 0）。

## 構成
- `design/` 設計文書（v0.4 が監査二巡目回付版）・段取り
- `arms/panel/` 前置き盤（8腕＋段V腕・`SHA-LEDGER.json`）／ `arms/materials-draft/` 第三者起草の素材草案（甲乙丙・indep）／ `arms/frozen-from-ryokai-os/` ryokai-os 凍結物の複製（SHA照合）
- `tools/` 走行器（`run_preamble_api.py`）・集計器
- `records/` FREEZE-RECORD・逸脱台帳・検分逐語（`reviews/`）・予想封印（`predictions/`）
- `results/` 段ごとの結果（データ・集計・報告）
- `prelim/` 登録外の下見（メモ・データ）

## ライセンス
素材・文書: CC BY 4.0 ／ 器材（tools/）: MIT
