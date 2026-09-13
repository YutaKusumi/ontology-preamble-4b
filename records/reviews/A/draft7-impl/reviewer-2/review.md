# 段階 A 器材の実装検分（検分者 2・コミット 99d28da02659）

- 対象の根: `C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b\.claude\worktrees\agent-aac3e7b03e56e4c3d`。以下のパスはこの根からの相対パス。
- 一時置き場: `C:\Users\PC\AppData\Local\Temp\claude\C--Users-PC\ccb2107c-84ba-4eab-bf7d-83ccce4f059f\scratchpad\impl-review-2`。器材の出力はすべてここに向け、`PYTHONDONTWRITEBYTECODE=1` で走らせた。リポジトリへの書き込み・results/ と prelim/ の閲覧・鍵ファイルの読み取りはしていない。
- 依頼文 `records/reviews/A/draft7-impl/review-request-impl-A.md` はこのコミットに無い。起動の文面の全文を使った。
- 件数: 凍結を止める 1・直す 12・確認を要する 4・軽微 1 群（7 項）。

---

## 所見

### F1［凍結を止める］起動器が重みの版を固定も記帳もしない
- **箇所**
  - `tools/colab/boot_stageA.py:137-142`（hf_rev）
  - 同 `172-176`（`snapshot_download(revision=rev)`）
  - 同 `225`（`model_rev=hf_rev(MODEL)`）
- **登録**
  - 起動器の説明の 12 行目「重みの版は records/A/hf-models-A.json の rev」
  - 草案7 §2.1「rev … を凍結時に記帳」
  - 正本 `sessions.fields` の `model_rev`
- **食い違い**
  - `hf-models-A.json` の `models` は機種 key の辞書だが、`hf_rev` は list のときだけ走査する。
  - それ以外は最上位の `HF[id]`・`HF[key]` を引くが、最上位に機種の欄は無いので常に None を返す。
  - その結果、重みは取得時点の main から取られる。セッション記録の `model_rev` は null になり、取得した snapshot の実コミットも記帳されない。
- **再現**
  - `hf_rev` の本体を写して現物の JSON に当てると、7 機種すべてで None（再計算）。
  - dry-run のセッション記録 `stageA__0.6B__s1.json` でも `model_rev=None`。
- **付記（確認を要する）**
  - 登録の rev は 7 機種とも 12 字の先頭（`records/A/hf-models-A.json`・字数は再計算）。
  - HF Hub の revision が短縮ハッシュを受けるかは確かめていない。

### F2［直す］走行器の失敗と校正腕の件数不足のまま判定して進む
- **箇所**
  - `boot_stageA.py:214-217`: rc≠0 を印字するだけ。
  - 同 `239`: 件数を `calibration.n` と照合しない。
  - 同 `247-248`: n_ok=0 を no_data として機種の走行へ進む。
- **登録**: `calibration.n`（400）・`calibration.timing`
- **食い違い**
  - 走行器の exit 3（dry-run の経路未発火・`tools/run_preamble_local.py:717`）でも exit 2（整合の不成立・同 `719`）でも続行する。
  - 途中までの件数で帯を判定する。
- **再現**: dry-run（main・0.6B・`OP4B_DRY_N=2`）で次の順に進んだ（一時置き場のログ）。
  1. 校正腕の走行が rc=3 で終わる。
  2. verdict first_point（k=1・n=2）を記帳する。
  3. 5 場面の走行へ進む。

### F3［直す］OP4B_DRY_N が本走行にも効き、dry-run の置き場の分離も強制されていない
- **箇所**
  - `boot_stageA.py:24`: DRY と無関係に読む。
  - 同 `197`: `n = DRY_N or n`。
  - 同 `226`: dev_marks は DRY のときだけ付く。
  - 同 `54-55`・`76-82`・`206-209`: DRY では `rmtree(d)` してから移動する。
  - 同 `5`: 一行は OP4B_DRY・OP4B_DRY_N・OP4B_SCENARIOS・OP4B_ANCHOR・OP4B_ENV_VALUE を設定し直さない。
- **登録**: 起動器の説明の 15-16 行目（DRY_* は器材検査の変数）・依頼の観点 10
- **食い違い**
  - (a) カーネルに OP4B_DRY_N が残っていると、本走行が小さい n のまま走り、印も残らない。
  - (b) OP4B_DRY=1 で OP4B_REPO_DIR を渡さないと、REPO は `/content/...` になる。同じランタイムで先の本走行が results を Drive への symlink にしていれば、次のことが起きる。
    - dry の出力が Drive の `results/<tag>/` に入る。
    - 未完の実走行キーのディレクトリが `rmtree` で消える。
    - 同名のセッション記録が dry の値で上書きされる。
- **再現**: コードの読み（非 DRY の起動は走らせていない）。

### F4［直す］api_error を揃える経路が起動器に無い
- **箇所**
  - `boot_stageA.py:199-202`: api_error 行も行数に数えて飛ばす。`--redo-errors` を渡す経路が無い。
  - `run_preamble_local.py:509-523`: api_error 行の再走は `--redo-errors` のときだけ。
  - `identity_screen_A.py:67-69`: n_ok が 160 未満なら停止する。
  - `integrity_A.py:91`: api_error が一件でもあれば不整合。
- **登録**: `identity_screen.n`・`integrity_check`「status と api_error」
- **食い違い**: api_error を含む走行キーは起動器では「完了」として飛ばされ、揃える手順が器材に無い。
- **再現**: コードの読み。

### F5［直す］files_sha16_lf に校正腕の走行が入らない
- **箇所**: `boot_stageA.py:292-297`（plan の走行キーだけを数える）
- **登録**: 起動器の説明の 300 行目（SHA の突合）・`calibration.timing`
- **再現**: dry-run のセッション記録で files_sha16_lf は 20 件、そのうち `stageA-calib` 配下は 0 件（再計算）。

### F6［直す］校正腕の判定が二か所に実装され、端で食い違う
- **箇所**
  - `boot_stageA.py:246-260`
  - `tools/calib_band_A.py:41-42`・`60-80`
- **登録**: `calibration.series_rule`・`timing`・runs_A と bands_A の説明「二重実装をしない」
- **食い違い**
  - (i) 初点: 起動器は n_ok を問わずに最古の校正腕を採り、n_ok=0 なら `Fraction(k,0)` で落ちる。calib_band_A は n_ok>0 の中から採る。
  - (ii) やり直し: 起動器は SESSION−1 だけを見る。calib_band_A は同じ相と持ち主の次のセッションを見て、番号が飛んでも注を付けるだけ（66 行）。
  - (iii) 橋の校正腕が本走行より先に走ると、起動器は first_point で進む。
  - (iv) 不合格枝で並行ランタイムを使うと、二つのセッションが起動器ではともに first_point になりうる。calib_band_A は一方しか初点にしないので、もう一方が後から逸脱になりうる。並行運用の予定は確認を要する。
  - synth_gates_A は起動器の判定を検査していない。
- **再現**: コードの読み。起動器側で通したのは dry-run の first_point だけ。

### F7［直す］response_mode_A が撤退条件の再走のあるパイロットで停止する
- **箇所**
  - `tools/response_mode_A.py:90`: `index_runs` を `allow_multi` なしで呼ぶ。
  - `tools/runs_A.py:75-76`
- **登録**: `calibration.withdrawal.rerun`（再走は同じ tag）・`style_gate.pilot_values`・`gate_A --style`
- **再現**
  - synth_gates_A を `--keep` で走らせ、gates-fail の置き場（seed 61701 と 71701 を含む）を残した。
  - そこに `response_mode_A --tag pilotA` を当てると、`RuntimeError: 同じ機種 × 場面の走行が複数: ('4B-2507', 'N1')` で停止した。

### F8［直す］組み立て器が行ごと置き換え、雛形の記入欄が走査に掛からずに消える
- **箇所**
  - `tools/build_report_A.py:316-322`（LINE_RULES。元の行を残すのは r_env だけ）
  - 同 `55-59`・`92-95`・`125-132`・`139-140`・`156-161`
- **登録**: 組み立て器の説明（機械で埋めない〔 〕は残す）・`report_rules.lint`
- **食い違い**: 次の記入欄が行ごと消える。
  - 雛形 32 行: 「引数文字列〔arms_string SHA16〕」「整合検査器〔…〕」「一致検査の判定〔 〕」
  - 45 行: 「除外後に判定不能になった対比」
  - 48 行: 「パイロット後に報告した (b) 率…〔 〕」
  - 14 行: 「機種・セッション数・走行期間」
  - 43 行: 「管理図〔…〕」
- **再現**
  - synth_A 走 1 の集計に build_report_A を当てた（置き換え 35 規則・埋め残し 58 件）。
  - 置き換えられた 32・45・48 行の句は出力に無かった。
  - 14・43 行は入力が無く置き換えが働かなかったため、今回は残った。記録を渡せば 55-59・125-132 行で置き換わる（コードの読み）。

### F9［直す］機械の区画の中身を検査しない
- **箇所**: `tools/report_lint.py:33-36`・`40`
- **登録**: `report_rules.typed_numbers`・`machine_block.rule`
- **食い違い**: 区画の印で囲めば、打ち込んだ数が「未登録の数」に掛からない。区画の中身を組み立て器の出力と突合していない。
- **付記（軽微）**: `build_report_A.py:366-367` は違反を印字するだけで止まらない。登録の「検出すれば組み立てを止める」と合わない。

### F10［直す］凍結範囲の漏れ
- **箇所**: `tools/freeze_A.py:17-24`・`32`
- **登録**: 草案7 §2.13・依頼の観点 8
- **漏れ**
  - (a) 走行器が読む語彙: `arms/materials-draft/hei/refuse-rules-v2.json`・`incentive-lexicon-v2.json`（`run_preamble_local.py:50-51`・`282-283`）。環境変数で差し替えもできる。
  - (b) 起動時に読む台帳: `arms/panelM/SHA-LEDGER-M.json`・`arms/panelF/SHA-LEDGER-F.json`（162-166）。A の 13 腕はすべて arms/panel にあるので、現状は判定に効かない。
  - (c) 転記行 F・G の入力: `records/cost-pilot/cost-facts-2026-09-13.md`・`records/F/style-stageF1.json`（`design_facts_A.py:83`・`301`）。設計事実はこの二つの SHA も記帳しない。
  - (d) 原稿を `design/design-stageA-draft7.src.md` に直書きしている。反映後の原稿から凍結本文を組むと、違う原稿を凍結する。
- **再現**: `freeze_A --check` の結果は対象 67・欠け 4（門0.5 と Firth の記録。未作成で想定どおり）・枠は一致。上の各ファイルは一覧に無い。

### F11［直す］集計器が記録の欠落や検査用の印を伝えない
- **箇所**
  - `tools/analyze_A.py:35`: `--identity`・`--calib` が任意。
  - 同 `54`・`78-80`
  - 同 `193-196`: 様式の記録にセルが無いと 0 として扱い、様式門を none にする。
- **登録**: 草案7 §2.8・§2.9 の注・`style_gate`（札に効く）
- **食い違い**
  - 門0.5 と校正帯の記録を渡さないと、注が付かないうえに dev_marks にも印が残らない。
  - 入力の記録の dev_marks・正本 SHA・retry_waiting・deviations を見ない。
- **再現**
  - dev_marks（allow_incomplete・small_B）付きの門0.5 の記録を calib_band_A に渡すと、出力に dev_marks の欄が無く、n=2 の初点でも判定した（一時置き場）。
  - 集計器の側はコードの読み。

### F12［直す］門0.5 不合格の注が記述族の Ncold−N に付かない
- **箇所**: `analyze_A.py:377-378`・`274-277`
- **登録**: 草案7 §2.9「N を含む効果種（Onull−N・記述の Ncold−N）に…機械印字」
- **再現**: コードの読み。

### F13［直す］合成検査の網の穴
- **箇所**
  - `tools/synth_A.py:81`・`144-192`
  - `tools/confirm_A.py:273-290`
- **登録**: 裁定 D9（各規則の発火）
- **穴**
  - (a) refuse 門の理由は (c) しか発火しない。synth_A 走 7 で、門を当てた 28 対比の理由はすべて c（再計算）。(a)(b)(d) は集計器を通して発火していない。
  - (b) 経路の検査は「出力に現れたか」だけで、注や除外がどの対比に付いたかの範囲を見ていない。
  - (c) confirm_A の自己検査 2 は、同じ `_stage2`・`row_id` で入力を作って判定するので循環している。独立の検査では食い違いは無かった（下の観点 1）。
  - (d) 様式 (a) は常に 0。非収束は検査用の口で強制している。

### F14［確認を要する］門2 の「族の縮小」の範囲
- **箇所**: `confirm_A.py:250-252` が 35 対比すべてを `U-gate2_shrink` にする。
- **登録**: `gate2.rule`・草案7 47 行「主成果の置き方のみ変える」・99 行
- **論点**: 残らない場面の対比だけを判定不能にする読みもありうる。この項は解釈の一覧に無い。

### F15［確認を要する］環境帯の引き直しの「既測の無い腕」
- **箇所**: `tools/gate_A.py:115-118`
- **登録**: `environment_band.pilot_recheck`
- **論点**
  - 実装は「パイロットの率が無い腕」だけを 0.5 にする。パイロットは 13 腕すべてを走らせるので、この句は実際には働かない。
  - 「API 既測の無い腕（Odose1・Odosehalf・Osec-Ncold）は 0.5」とも読める。

### F16［確認を要する］判定器の断片の鍵と除外
- **箇所**: `tools/judge_fragments_A.py:77`・`98-99`・`104-108`
- **登録**: `judge_validity.extract.key`・`score`
- **論点**
  - (a) 鍵が既定で公開リポジトリの records/A に置かれる。.gitignore に鍵の型は無い。
  - (b) 機械の refuse も「決定なし」として除かれる。文言が挙げる機械側の除外は書式外だけ。
  - (c)（軽微）ラベルを付けなかった断片が、判定不能と区別されない。
  - (d)（軽微）再計算した機械の破局と、保存された catastrophe の一致を assert していない。

### F17［確認を要する］「上向きの確証」の式
- **箇所**: `build_report_A.py:69-71`（確証かつ slope_pt>0）
- **登録**: 雛形 §0-5「処置腕の破局率が対照より高い向きに広がった」
- **論点**: slope_pt>0 は、差が負のまま零に近づく配置も含む。正本に「上向き」の定義は無い。

### F18［軽微］
- `boot_stageA.py:91-94`・`101-102`: OP4B_ENV_VALUE を検出した GPU と照合しない。「第三」を 32B 以外にも許す。
- `integrity_A.py:36-37`: 再走の seed を全セルに許し、走行がそろっているかを見ない。
- `sample_inspection_A.py`: 再走を枠に入れる規則が正本に無い。再走の有無で乱数の消費順が変わる。
- `confirm_A.py:71`・`246`: `p_star_if_mismatch`・`p_undecidable` を正本から読まず、1.0 を直書きしている（値は一致）。
- `build_draftA.py:34` 付近: 格子 JSON の SHA を突合しない。現状は一致する（E8502B29E04125B4・再計算）。
- `control_chart_A.py:42-53`: 合格枝で、段階 F の表と帯の片側・両側の違う行を同じ列に足す。
- 率盲検: gate_A の `env_band_recheck.rates_used` と response_mode_A の `strata.cat` は、腕別のパイロットの率を含む。登録の率盲検は整合と抽出の器に限るので違反ではないが、本走行の前にコーディネータが見る経路として記す。

---

## 所見の無かった観点（確かめた範囲と方法）

1. **confirm_A**: 独立に実装し直して比べた。数はすべて再計算。
   - 札の二段と第一適合の順は、正本の `stage2_first_match` と一致した。段 2 の 48 組は食い違い 0、表は 52 行で id は一意、`combo_rows()` は正本と一致した。
   - Holm は同順位を含む 20,000 回で食い違い 0。
   - `contrast()` は無作為の 400 入力（収束 266）で、次の項目の食い違いが 0。
     - 検閲（Fraction）
     - pt 差の傾き（q=(k+0.5)/(n+1)・重み付き平均・se・正規近似）
     - p*（向きの不一致で 1）
     - 飽和の数え方と解釈条項（2 規模以上）
   - 様式門は 30.0 pt で note・30.5 pt で hold・15.0 pt で none・15.5 pt で note。refuse の (c) は 15.0 pt で発火せず、15.5 pt で発火した。
   - 自己検査（confirm_A・bands_A・numbers_lint）は PASS。
2. **analyze_A**（コードの読みと、合成 走 1・走 7 の実行。期待との不一致 0）: 次の項目を登録と照合した。
   - 測定不能の和集合（「超」・n_ok=0 も外す）
   - 錨帯（本走行と二走行目・規模 × 場面）
   - 環境保留（腕を含む全場面・残存規模の環境値の和集合が一つ）
   - refuse 門を p_β<α に限って当てること
   - 感度閾値の組・測れた効果種の細目・床持続・記述族の p 非印字・定型文の順
3. **gate_A・calib_band_A・bands_A**: 格子の整数境界と独立に照合した（数は再計算）。
   - 校正腕の合格枝は X≤369。369 で発火、370 で発火しない。帰無率の差は 0。
   - 撤退条件の合格枝は X≤32（n=40）。
   - 門2 は X≤1・X≥39（n=40）。
   - 環境帯の期待誤保留数は 10 pt 2.7635・12 pt 0.8798・15 pt 0.1163・20 pt 0.0018 で、格子と一致した。選ばれる 12 は登録値と一致する。
   - 錨帯の期待誤除外数は 10 pt 2.3653・12 pt 0.845・15 pt 0.1347 で、格子と一致した。
   - synth_gates_A を再走して PASS 23/23。
4. **identity_screen_A**: 絶対差 30 個の assert・Fraction の平均と最大・「以下」・補助検定の前に判定を確定する順を確かめた。走行器の欄の定義では、書式外・refuse・破局は ok 行の中で互いに排他なので、排他の件数と API の cells の件数は一致する。分母はどちらも n_ok。
5. **response_mode_A**: `strip_echo` などは走行器から AST で抽出しており、再実装していない。送信の部品・分母 n_ok・最終試行・層を確かめた。語彙は `response_mode_M.py:12`・`F.py:14` と同じ直書きで、器自体は凍結範囲に入っている。停止は F7。
6. **integrity_A・sample_inspection_A**: 許可欄に判定欄は無い。相ごとの期待値は登録と一致する。dry の出力には model の検査が × を出し、非零で終わった（再現済み）。
7. **judge_fragments_A**: 伏せる欄・順の並べ替え・子ストリーム・SHA-256（LF）・κ と方向別の誤判定率の式を読んだ。
8. **build_draftA・numbers_lint・雛形**
   - 草案7 と雛形を一時置き場で組み直すと、lint 記録のパスの一行を除いて一致し、違反は 0。
   - 転記行 A〜O の 15 行は草案7 に逐語で入っており、正本と格子の SHA の連鎖も一致する。
   - 組み立て器の規則の鍵 45 個は、それぞれ雛形の一行にだけ当たる（前提の行は §0 の前で別に扱う）。
   - 雛形の枠の検証は一致。
9. **格子 v3.1・設計事実 v3.1**: 確定の格子の二行を、seed と節の子ストリームから再模擬した。値は確定値と同じだった。
   - D[0]（中間・d0=0・Δ=0・B=2000）: 名目 0.057・初段 0.0005・札 D1 初段 0.0005
   - DR[0]（N1:Onull~N・一定・Δ=0・B=1000）: 名目 0.052・札 D1 名目 0.047・初段 0.001
   - 厳密計算の節 I・M・H は上の 3 の値で一致した。
10. **起動器**: 次は登録と一致した（コードの読みと dry-run）。
    - 非思考モードの指定を六機種にだけ併合すること
    - 同時要求数（if_40GB・第三・32B は 40GB で止まる・橋の値）
    - 校正腕の seed（0.6B の s1 は 65101）
    - 再開の冪等（再走で skip になった）

    食い違いは F1〜F6 に記した。
11. **合成検査**: F13 に記した。期待値は型の設計から作っており、判定の論理の写しにはなっていない（id の書式だけ共有）。
12. **運用の解釈 23 項**: 確証の規則と札への波及は無かった（観点 1 の独立検査の結果は解釈と無関係に一致）。
    - 別の読みがありうるもの: F14（1 の周辺）・F15・F16（17）・F9（23）・F6(iv)（14）。
    - 10 の「4B の点が外れた」は検閲を含まない読みになっている。影響するのは選択規則の入力だけ。

---

## 本検分が確認していないこと
- Colab の実機（GPU・vLLM・Drive・HF Hub）での起動器の走行。非 DRY の経路（F3 を含む）はコードの読みだけ。Drive 上で途中で切れた JSONL の行への耐性。
- HF Hub が 12 桁の revision を受けるか。
- 格子 v3 と v3.1 の数値の一致。v3 はリポジトリに無く、確かめたのは確定の格子の二行と厳密計算の節だけ。
- R logistf との一致検査、firth.py の自己検査の全体（B=2000）、synth_A の十三走すべての再走（走 1 と走 7 だけ）。
- 走行器の採点経路（パーサ・refuse_class・incentive）の正しさと、API 再走行の経路（機種 id の対応を含む）。
- results/ と prelim/ の中身（開いていない）、もう一体の検分者の所見との突合。

本検分のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
