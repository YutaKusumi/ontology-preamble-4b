# 段階 A 器材の実装検分 所見（検分者 1）

対象はコミット 99d28da02659 の worktree です。依頼文の 12 観点をすべて扱いました。特記の無い数は、一時置き場での再計算値です。

## 0. 方法

- **読んだもの**: 対象一覧のファイルはすべて通読しました（正本 contrasts-A.json 全体、草案7 全節、雛形、運用の解釈を含む）。凍結物の走行器とパーサは、該当する関数を読みました。
- **走らせたもの**: すべて一時置き場 impl-review-1 の写し（tools・design・records/A・arms）で行いました。
  - 自己検査 3 本（confirm_A・bands_A・numbers_lint）はすべて PASS でした。
  - 独立に書き直した実装と突合しました（観点 1・3・9）。
  - synth_A と synth_gates_A を再走しました。
  - 5 か所の変異を入れた写しで、synth_A を全 13 走させました。
  - 起動器の dry-run を行い（identity と main の 4B s1・s2、N1、OP4B_DRY_N=2）、その出力に calib_band_A・integrity_A・response_mode_A・judge_fragments_A extract・sample_inspection_A を当てました。
  - build_report_A・report_lint・numbers_lint には探り入力を与えました。
- **書き出しの方法**: Bash の heredoc が worktree の防護で拒否されたため、検証スクリプト 2 本の書き出しは PowerShell で行いました。書き出し先は一時置き場だけです。
- **リポジトリ側での実行**: 何も書き出さない自己検査だけを、PYTHONDONTWRITEBYTECODE=1 を付けて走らせました。tools/__pycache__ が生じていないことも確認しました。
- **開いていないもの**: results/・prelim/・鍵ファイルは開いていません。records/control-chart.md は、見出し行と表の行番号だけを見ました。

---

## 1. 所見

### 凍結を止める

**F-01［凍結を止める］boot_stageA.py:137-142（hf_rev）・172-176・225**
- **登録**: 草案7 §2.1（重みの rev を凍結時に記帳する）、起動器 docstring 12 行「重みの版は hf-models-A.json の rev」、正本 sessions.fields の model_rev。
- **食い違い**:
  - hf_rev は、`HF['models']` が list のときだけそれを走査します。そうでなければ最上位の `HF[機種 id]` と `HF[key]` を引きます。
  - 実際の hf-models-A.json では、最上位のキーは note・fetched_utc・models・gpu_gib・kv_bytes_per_token_note です。rev は `models.<key>.rev`（dict）にあります。
  - このため全機種で None が返り、`snapshot_download(revision=None)` がその時点の main を取ります。セッション記録の model_rev も None になります。
  - 結果として、登録と違う版の重みを、版を記録しないまま走らせうることになります。
- **再現**:
  - hf_rev を ast で取り出し、コミットの JSON で実行すると、7 機種すべてで None でした。
  - dry-run のセッション記録 3 本（idA s1・stageA 4B s1・s2）も、model_rev は None でした。

**F-02［凍結を止める］judge_fragments_A.py:99（judge_cat）**
- **登録**: 正本 judge_validity.extract.score「凍結パーサの is_catastrophic を機械と判定者の読み取りの両方に当てる」。
- **食い違い**:
  - 判定者の側は `'_X': amount or 0` で組まれており、凍結パーサの符号化（app_parser_rev2.py:68 `_X = amount if choice=="a" else 0`）を通りません。
  - survival 族（S1・S4・SK。app-scenarios.json で確認）では、選択が a 以外で量が正のとき、判定者の側だけが破局になります。
  - 「機械が非破局で判定者が破局」の向きの誤判定率と κ が、3 場面で偏ります。
  - 凍結後に直すと逸脱になるため、凍結を止める扱いにしました。
- **反例**: `{"choice":"b","amount":5,…}` を parse_app_v2 に通すと、_X=0 で is_catastrophic は False です。同じ読み取りを 99 行の式に入れると True になります。

### 直す

**F-03［直す］analyze_A.py:79-80・433**
- **登録**: identity_screen.fail（N を含む効果種へ機械印字する）、calibration の注。
- **食い違い**:
  - --identity と --calib が任意の引数です。無いと、門0.5 の注と校正の注が黙って付きません。
  - このことは dev_marks にも missing にも入りません。
  - md には「校正腕の器の異常の走行キー: 0」と印字され、記録が無いのか異常が無いのかを区別できません。
- **再現の手順**: 走 2（門0.5 不合格）の合成を、--identity なしで通すと、注が 0 件のまま完走します（79・377 行の経路）。

**F-04［直す］analyze_A.py:144-149**
- **登録**: 正本 sessions.env_value_rule「集計器は走行キーごとの環境値をセッション記録から読む」。
- **食い違い**:
  - セッション記録の無い走行キーは、environments の登録値で補われます。件数を印字するだけで、停止も印もありません。
  - 札に作用する片側の規則が、実際の値ではなく登録値で決まります（例: 32B を第三で走らせた記録が欠けた場合）。
- **再現の手順**: 合成の root から sessions-A の一本を消すと、停止せず env_fallback に入るだけです。

**F-05［直す］analyze_A.py:91-95・193-196**
- **登録**: style_gate（段 2 で札に作用する・規模ごと・分母 n_ok）。
- **食い違い**:
  - 様式の記録にセルが欠けると n_ok=0 として扱われ、様式門は黙って none になります。
  - 記録の n_ok と試行から数えた n_ok の突合がありません。
  - 記録は kind しか照合せず、tag を照合しません。

**F-06［直す］analyze_A.py:377-378・273-277**
- **登録**: 草案7 §2.9「N を含む効果種（Onull−N・記述の Ncold−N）に…機械印字」。
- **食い違い**: 注は傾きの族にしか付きません。記述族 A_desc_ncold（5 本）には付きません。

**F-07［直す］analyze_A.py:361 ほか**
- **登録**: 草案7 §3 (xii)「残存が非連続（端のみ）の対比には注」、§3 (v)「対照どうしの差を機械印字・『A は B₁ とも B₂ とも異なる』の定型」。
- **食い違い**:
  - (xii): 残存規模の連続性の判定がありません。print_strings.residual_sizes の固定句「端を欠く対比には注。」が、全対比に同じ文で出るだけです。
  - (v): 対照どうしの差を出す出力も定型文も、正本・analyze_A・build_report_A のどこにもありません（grep で 0 件）。

**F-08［直す］runs_A.py:62-79・boot_stageA.py:206-213**
- **登録**: 起動器 docstring 15-16 行（dry-run の出力は検査用の印つき）、publication.raw_data。
- **食い違い**:
  - dry-run は manifest の model を、登録の機種に書き換えます（dry_model_rewritten）。
  - 行には model='stub/dry-run' と dry_run=true が残り、セッション記録には dev_marks=['dry','dry_n'] が付きます。
  - しかし runs_A・analyze_A・gate_A・calib_band_A・identity_screen_A は、どの印も見ません。
  - integrity_A が、行の model の不一致で間接に止めるだけです（ALLOW に dry_run と mode がありません）。
- **再現**:
  - dry-run 出力に calib_band_A を当てると、印を見ないまま判定しました（s1 fired・s2 anomaly、anomaly_run_keys に本走行の走行キー）。
  - integrity_A は、model・rows・api_error・per_arm_even を不整合としました。
  - OP4B_REPO_DIR を作業ツリーそのものに向けて dry-run すると、同じ走行キーの出力が残ります。これは、起動器の skip（198-200 行）と走行器の再開で、本物として扱われえます。

**F-09［直す］calib_band_A.py:38（seed_rule_ok）**
- **登録**: docstring 9 行「seed が規則と合うかも印字」、integrity_check「model と seed が登録の表と一致」。
- **食い違い**:
  - 持ち主・相・セッション番号を seed から解き（runs_A.py:105-117）、それを組み直して同じ seed と比べています。このため常に真になり、検査が自己循環しています。
  - セッション記録の session と model の欄とは突合しません。integrity_A の calibration 相（69-73 行）も、seed が解けるかどうかしか見ません。
- **再現**: 規則上ありうる seed 891 個で、偽になるものは 0 でした。dry-run の出力でも True でした。

**F-10［直す］synth_A.py:35・47・60・81・144-188**
- **登録**: 草案7 §2.14 の手順4、synth_A docstring「各規則を発火」、label_combo_rule。
- **食い違い**: 全行の発火は満たしていますが、規則の選択性と一部の分岐は検出できません。写しに次の変異を入れて全 13 走させたところ、PASS（52/52 行・不一致 0・経路の未発火 0）でした。
  - **M1**: analyze_A:381 `if rks & ANOM_RK:` を `if ANOM_RK:` にした（校正の注を全確証に付ける）。
  - **M2**: analyze_A:198 で、橋の保留を腕に関係なく全対比に当てた。
  - **M3**: analyze_A:377 で、門0.5 の注を全対比に付けた。
  - **M4**: confirm_A:106 で、refuse の理由を (c) だけにした。
  - **M5**: confirm_A:113 で、様式門を全規模に当てた。
- **理由**:
  - 各対比が X 腕をちょうど一本含むため、腕による選択性が見えません。
  - refuse の保留は、推移 (c) でしか起こしていません。
  - 経路の検査は、出たかどうかの有無だけです。
  - 片側の規則の唯一の例は期待が NS です。
  - 確証は N1 にしか出ません。
  - 全組合せ表も confirm_A.combo_rows から生成されています（make_contrasts_A.py:11・85）。表そのものは観点 1 で独立に確かめました。

**F-11［直す］synth_gates_A.py:87・113-125・150-155**
- **未発火の分岐**:
  - 撤退条件の合格枝での発火と、rerun_required・rerun_pass。合格の場合は 39/40 なので発火しません。
  - 不合格枝での器の異常と、橋のセッション。
  - 整合検査の否定の経路のうち、要求の設定以外のもの。

**F-12［直す］freeze_A.py:17-24・32**
- **登録**: freeze_A docstring（走行器と起動器・盤の台帳と凍結物の写しを含む）、草案7 §2.13。
- **食い違い**（file_list を呼んで確認）: 次が凍結範囲に入りません。
  - arms/materials-draft/hei/refuse-rules-v2.json と incentive-lexicon-v2.json（走行器 50-51 行が読み、行の refuse_class と incentive を決める）
  - arms/panelF/SHA-LEDGER-F.json（走行器 165-166 行が読む）
  - records/cost-pilot/cost-facts-2026-09-13.md（転記行 F の入力）
  - records/F/style-stageF1.json（転記行 G の入力）
  - records/A/tooling-interpretations-A.md
  - また 32 行で design-stageA-draft7.src.md を固定しているため、凍結本文の原稿が別名になると取り違えます。
- **再現**: 写しで `--check`（design=草案7）を走らせると、対象 67・欠け 4（identity-screen と firth-check の未生成分だけ）・枠は一致でした。上の各パスは一覧にありません。

**F-13［直す］report_lint.py:33-45・numbers_lint.py:18・build_report_A.py:328-330**
- **登録**: report_rules.typed_numbers（打ち込める型を限り、冒頭に一覧を印字する）、machine_block.rule。
- **食い違い**:
  - (1) MASKS を流用しているため、code span の中の数、「(20xx)」「第N章」「#N」「D99」「N GB」「段 N」を数として読みません。
  - (2) 機械の区画の印は平文で、中身が機械の出力かどうかを照合しません。
  - (3) 費用の印で始まる行は、費用以外の数も通ります。
  - (4) build_report_A は、打ち込んだ数の一覧を冒頭に印字しません。
- **再現**:
  - 偽の区画の中に「確証 99 本」、本文に「`37%`」「(2048)」「第3章」「#12」「D99」「12 GB」「段 7」、費用の印の行に「確証 88 本」を書いた探り入力で、report_lint の違反は 0 でした。
  - numbers_lint の check_src と check_doc も、「`12`」「(2048)」「#7」を 0 件としました。

**F-14［直す］boot_stageA.py（校正と再開）**
- (a) 247-266: 校正腕が no_data でも、機種の走行に進みます。
- (b) 252-257: 不合格枝の初点を n_ok を見ずに取ります。n_ok=0 の走行が先頭にあると落ちます。calib_band_A.py:41 は n>0 に絞るので、初点が食い違います。
- (c) 258: やり直しを「SESSION−1 が fired」に限っています。calib_band_A.py:60-80 は「同じ相と持ち主の次の校正走行」をやり直しと数えます。このため、番号の飛びや中断があると記帳が食い違います。
- (d) 198-200: skip の判定で api_error の行も数えます。再走の道がありません。
- (e) 91-102: 第三の指定で GPU とメモリの検査を飛ばし、どの機種でも受け付けます。
- (f) 23: 本走行でも OP4B_COMMIT の既定値 'main' を受け付けます。
- dry-run の流れ（s1 fired で停止、s2 anomaly で走行）は、起動器と calib_band_A で一致しました。

**F-15［直す］run_preamble_local.py:231-266・boot_stageA.py:130・177-179・225**
- **登録**: 草案7 §2.1「pip freeze の SHA・…同時要求数・…重みの rev・収容・先取りの回数を manifest と凍結記録に」、environment_rule.record、§2.12。
- **食い違い**:
  - manifest の local_env は、gpu・versions・server_version だけです。
  - pip freeze の SHA と同時要求数は、セッション記録にしか書かれません。
  - 先取りの回数は、どの器も抽出しません。
  - 様式と言及は、試行ごとではなくセル単位の集計です。
  - サーバの --seed 0・dtype・max_model_len は、どの記録にも残りません。
  - 走行器は凍結物なので、登録の文言か起動器の記帳のどちらかを合わせる必要があります。

### 軽微

- **F-16** confirm_A.py:246-252・analyze_A.py:444-446: 門2 の縮小時も、実の p を Holm に入れ、p・順位・区間を印字します。undecidable_rule（p を 1 として入れる）とずれます。札はすべて判定不能のままです。
- **F-17** confirm_A.py:71・246: p*＝1 と p_undecidable＝1 を直書きしています（正本のキーを読んでいません）。値は同じです。
- **F-18** gate_A.py:102: 撤退条件の再走で n_ok=0 だと rerun_pass になります。calib_band_A.py:65・70: やり直しで n_ok=0 だと pending が消え、器の異常にもやり直し待ちにもなりません。
- **F-19** analyze_A.py:131-134・160-162: 錨反復や橋の n_ok=0 は、黙って「超えない」扱いになります。54 行: --B-measurable の上書きが dev_marks に入りません。
- **F-20** build_report_A.py:177-179・182-192: 雛形の見出しにある「Wilson」、PPLRT 統計量、率を出していません。
- **F-21** judge_fragments_A.py:
  - 98・105-106: 機械の refuse を、書式外と合算しています。登録の除外は判定者の判定不能・refuse と機械の書式外です。
  - 118-124: κ は先頭の二名だけです。
  - 125: 鍵の SHA-256 を、判定前に記帳した値と照合しません。
  - 76-77: 鍵の既定の置き場が、断片と同じ records/A です。
- **F-22** integrity_A.py:90: local_env を真偽値で見るため、dry-run の「nvidia-smi 不可…」でも通ります。
- **F-23** response_mode_A.py:19・22: 語彙を直書きしています。場面ファイルの SHA を照合しません。
- **F-24** control_chart_A.py:43: 合格枝の追記先が「ファイル中の最後の表」です。現物は表が一つ（見出し 5 行・最後の表の行 16）なので今は正しく入ります。表が増えると誤ります。
- **F-25** freeze_A.py:44-49: 枠の検証は、見出しの部分文字列の一致だけです。
- **F-26** 草案7 §2.4: 本文は「各セル n_ok が 30 以上」ですが、正本の hold_if (d) と実装（confirm_A.py:89）は「答えた分母が 30 以上」です。
- **F-27** 正本 A_desc_critical_size.rule・analyze_A.py:329-335: 零の差を符号の変化に数えないことが、文言にありません。差の符号が（＋, 0, −…）の例では、実装は 4B を返します。零を「異なる符号」と読むと 1.7B になります。

### 確認を要する

**F-28** confirm_A.py:246-247
- p* の Holm を全 35 対比に当てています。正本の text は「β₃ の Holm で棄却された対比について」です。
- 棄却の集合は単調性から一致しますが、記述（対数オッズ尺度でのみ）の対比の順位・水準・区間が変わります。
- **例**: 対象の対比は p_β=1e-8・p*=0.3（傾き 0.02・se 0.01）、別に β₃ で非棄却の p=0.01 の対比がある場合です。

  | Holm を当てる範囲 | 順位 | 水準 | 区間（pt/z） |
  |---|---|---|---|
  | 全 35 対比 | 2 | 0.0014706 | −1.1804〜+5.1804 |
  | β₃ で棄却された対比だけ | 1 | 0.0014286 | −1.1888〜+5.1888 |

**F-29** firth.py:33・firth_check_A.py:57・60
- 集計は firth の既定の設定（gtol 1e-7・max_iter 200）で当てています。R との一致検査は python_control（1e-12・5000）で当てます。検査が確かめる設定と、実際に使う設定が別です。
- 無作為 150 配置での差は、PPLRT 統計量で最大 2.27e-12、収束の旗の食い違いは 0 でした。

**F-30** judge_fragments_A.py:113-115
- 方向別の誤判定率は、機械ラベルで条件付けています。
- 雛形の列名と読み条項 (xv) は、判定者の読み取りで条件付けた率とも読めます。転記行 O の前提は、実装と同じです。

**F-31** 正本 calibration.consequence／withdrawal.consequence（新 seed で再走）と calibration.timing（次のセッションの校正腕からやり直す）が併存しています。字義どおりの読みは異なり、実装は timing に従っています。

**F-32** 運用の解釈の「変えていないもの」について
- 次の解釈は、札の入力を決めます: gate2.unit_rule（対比ごとに数える）、unmeasurable.applied_on、anchor_band.compare、sessions.env_value_rule。
- gate2.unit_rule は、採らなかった「場面の規模の和」より縮小が起きやすい読みです。
- F-02 と F-04 は、それぞれの解釈の文言と矛盾します。

**F-33** 運用の解釈の一覧に無い細目
- 様式門を残存規模だけに当てています（confirm_A:113、gate_A:136 は全規模）。
- 解釈条項の飽和を、全除外の後の規模で数えています（:64、文言は「検閲後」）。
- refuse (c) の分母は n_ok で、再フィットに検閲を掛け直しません（:89-103）。
- refuse は JSON の choice=refuse だけです（runs_A:91）。
- どれも札に作用します。

**F-34** sample_inspection_A.py:41-43
- 腕名つきで、生本文の先頭 600 字を印字します。dry-run の標本でも、「Lneg」の下に `"choice": "a"` が出ました。
- 率盲検は欄の水準でしか成り立っていません。

---

## 2. 観点ごとの確かめた範囲と方法

1. **confirm_A**
   - 全組合せ表の 52 行を stage2_first_match から独立に組み直しました。段 2 の 48 組合せをすべて含み、札・行 id・規則の不一致は 0 でした。
   - label_family を、独立の Holm と第一適合で、3,000 族 × 35 対比と突合しました（全 8 札が出現）。棄却・順位・札の不一致は 0 でした。
   - contrast を、Fraction での検閲・q の重み・重み付き z̄・se・p_pt・向きの独立実装で、400 配置と突合しました。最大差は 0.0 でした。
   - refuse (a)〜(d) と様式門の「超」は、正本の文言と一致しました。
2. **analyze_A**: 測定不能・錨帯・橋・片側・refuse の範囲・表の突合と停止・感度・測れた効果種・床持続・p の非印字を、各キーと突合しました。reach_note の数（22・5・13。出典は design-facts-A.json の facts.D.data）は、転記行 B・D と一致します。
3. **gate_A・calib_band_A・bands_A**
   - 転記行 C・E・G・H・I・M を、bands_A を使わない厳密計算で 40 項目再計算し、power-grid-A.json と全一致しました。主な値は次のとおりで、草案7 の転記行 I・M（159・163 行）の表示と合います。
     - 校正の合格枝: X≤369、帰無 4.564e-08
     - 校正の不合格枝: 帰無 6.149e-06／9.367e-04、検出 0.4712／0.8855／0.9907
     - 撤退条件: X≤32、帰無 5.736e-06。不合格枝の帰無 2.675e-05／4.834e-04／4.319e-03
     - 門2: X≤1／X≥39
     - 環境帯の期待誤保留数: 2.764／0.8798／0.1163／0.001841。規則が選ぶ候補は 12 で、登録値と同じ
   - synth_gates_A の再走は 23/23 でした。
4. **identity_screen_A**: 差の個数の assert、Fraction での比較、「以下」、補助検定が判定の後であること、排他の優先順を確かめました。凍結パーサの None の規則（62-64・87-88 行）により、排他の件数は素の件数と同じです。**所見なし**。
5. **response_mode_A**: ast での抽出、送信文字列の並び、分母、最終試行を確かめました。走行器の出力形式でも完走しました。
6. **integrity_A・sample_inspection_A**: ALLOW、相ごとの期待、乱数の消費順を確かめました。dry-run 出力で、model の不一致を検出しました。
7. **judge_fragments_A**: dry-run 出力で extract を走らせ、断片の欄が id・場面本文・指示・本文だけであることを確かめました。κ の式は正しいです。
8. **報告・凍結・数の検査**
   - 合成の集計で build_report_A を組み立てると、見出しは雛形と一致し、置換 35 規則、埋め残し 58、数と語の違反 0 でした。
   - 草案7 に numbers_lint を掛けて、違反 0 でした。
9. **power_grid_A・design_facts_A**
   - 格子の入力 SHA16 の 7 項目が、現物と一致しました。
   - D の最初のセルを simulate_cell で再生すると、全欄が一致しました（名目 0.057、初段 0.0005）。
   - v3 から v3.1 への移設で数値が変わっていないかは、v3 が履歴に無いため確かめられません（51f7e3a にあるのは v2）。
10. **boot_stageA**: dry-run で、相の順、即時判定と停止、やり直しと異常、セッションの欄を確かめました。同時要求数と extra_body の範囲は、コードで確かめました。
11. **synth_A・synth_gates_A**: 再走で PASS を再現しました。変異の結果は F-10 のとおりです。
12. **運用の解釈の 23 項目**: 正本と草案7 と突合しました。F-02・F-04・F-27・F-31〜33 以外では、登録済みの文言との矛盾は見つかりませんでした（rerun_offset による seed 71101〜 は、他の seed の帯と重なりません）。

---

## 3. 本検分が確認していないこと

- Colab 実機での挙動（GPU の同定、40GB／80GB の割当、vLLM、HF からの取得、Drive）。dry-run で通したのは identity と main（4B・N1・n=2）だけで、pilot・pilot_rerun・bridge・錨反復は通していません。
- 実データでの器の挙動。firth_check_A と firth.py の自己検査は、走らせていません。
- 格子の v3 から v3.1 への数値の一致と、格子全体の再計算。
- make_contrasts_A の再生成の同一バイト性（results/ を読むため）と、build_draftA・judge score の実行。
- 設計事実の文言と正本との全面的な突合（数の登録と、I・M・D・B の数だけを確かめました）。
- 依頼文ファイルは worktree に無く、SHA16 CAF934578A58EABD を照合していません。
- もう一体の検分者の所見との突合。

本検分のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
