<!-- 逐語保全: 器の直しの確かめ（登録者裁定 D238・正本 review_plan.impl_recheck）・系統外・一人目（札 G1）。本文の中の機種の申告は「（機種の申告の行が無い）」、系統の申告は「系統外（Google）・Gemini」。登録者の言葉では「新規のGemini 3.8 Flash 二名」（登録者の言葉は逐語・下の出所）。
     登録者（楠見優太）が会話で渡した票を、会話の記録から機械で切り出した（登録者の言葉・uuid 00d8febf-a092-40e6-a21f-e057bafead53・2026-09-26 05:34 日本時間）。
     この枠の外は一字も変えていない。本票のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->
# B-lens 層三の器の直しの確かめ（下見の前の凍結の前・登録者裁定 D238）検分票

- **系統**: 系統外（Google）・Gemini
- **検分者**: 系統外の個体（Gemini）
- **対象**: 束 `bundle-fixcheck-Bl3-all-in-one.md`（コミット `b77dd22` の中身から組まれたもの）に含まれる直した器、差分、正本 v8、設計事実、二体の票、採否の案、合成データの正式の記録、器の段の記録。
- **遵守事項**: 本物の模型での効き目計算は行っていません。結果の見込み（札や門の成否等）に関する記述は一切含みません。

---

## 0. 本検分が確認したこと・確認していないこと

### 確認したファイルと関数
1. `tools/bl3_core.py`（v3 全文）: `p_and_tail`, `agreement`, `effect_side`, `second_label`, `iso_top_share`, `comparators_for`, `comparator_anchor`, `gate`, `cells_decision`, `_selftest`
2. `tools/bl3_run.py`（v3 全文）: `require_finite`, `ids_sha16`, `Runner.forward`, `Runner.prefix_cache`, `run_pilot`, `run_cell_sign`, `recompute_hook_path`, `build_cells`, `load_dirs`, `secondary_contexts`, `run_secondary`, `run_main_phase`
3. `tools/colab/boot_Bl3.py`（v3 全文）: `package`, `stop`, `verify_frozen`, `run`（相 check の guard と forward_calls、相 pilot / main の予想照合、組ごと zip 出力、例外ハンドリング）
4. `tools/analyze_Bl3.py`（v3 全文）: `load_outputs`, `env_same`, `frozen_versions_bad`, `judge`, `open_results`, `open_checked`, `row_labels`, `labels_signature`, `gates`, `recompute_agreement`, `main`
5. `tools/sweep_Bl3.py`（v3 全文）: `sweep`（層ごと差分の中身、等方本数の検証）
6. `tools/build_report_Bl3.py`（v3 全文）: `dropped_split`, `reading_types`, `pilot_lines`, `build`, `sealed_and_frozen_bad`, `load_inputs`, `_selftest`, `_selftest_sealed`
7. `tools/seal_Bl3.py`（v2 全文）: `info_empty`, `registrant`, `record`, `_selftest`
8. `tools/make_frozen_Bl3.py`（v3 全文）: `build_frozen`, `rebuild_and_check`, `main`, `_selftest`
9. `tools/freeze_Bl3.py`（v3 全文）: `local_ids_sha16`, `latest_dry_run`, `prepilot_checks`, `prepilot`, `main_freeze_checks`, `main_freeze`
10. `tools/dry_run_Bl3.py`（v3 全文）: `answer_labels`, `synth_effects`, `part_pure`, `part_model`, `part_boot`, `main`
11. `design/contrasts-Bl3.json`（v8 全文）および `records/Bl3/frozen-diff-Bl3.md`、`records/Bl3/design-facts-Bl3.md`
12. 記録類: `records/Bl3/dry-run-Bl3-2026-09-25.md`、`records/Bl3/tools/trials/dry-trial-9-Bl3.md`、`records/Bl3/tools/tools-log-Bl3.md`

### 確認していないこと
- 本物の重み（`Qwen/Qwen3-4B-Instruct-2507`）を用いた GPU 上での全経路の順伝播および効き目の数値計算全般（予想封印前のため一切行っていません）。
- 実際の Google Colab / GPU 環境（L4 / A100）における CUDA 版 torch の自動再インストールと再起動、およびブラウザ経由の `files.download()` の実機動作。
- 実重みの Safetensors からの疎な取り出しの実機ネットワーク動作。
- 段階 B および B-lens の過去の凍結物の中身そのものの妥当性（読み取りのみとし、所与のものとして扱いました）。

---

## 1. 伺いたいことへの回答

### (1) 直しが所見を閉じたか（第二部 採否の案 Aの表 26項目）

採否の案 A の表の26項目すべてについて、第三部の所見（R1・R2）および第四部の差分・第六部・第七部のコード全文を突き合わせました。**26項目すべてが所見の指摘した問題を閉じています。**

特に、単に指摘された通りに塞ぐだけでなく、より堅牢な形へと昇華させて閉じている箇所が確認できました：

- **R2-重大1（封印予想の照合）**:
  - `build_report_Bl3.py:320-337`（`sealed_and_frozen_bad`）で、予想ファイル本体の SHA-256、封印記録の SHA16、本の凍結記録（`main_freeze.seal`）に写されたハッシュの三重照合を導入。
  - `boot_Bl3.py:207-212` で、相 pilot および相 main の実行開始時に封印記録とコミット内の予想ファイルの SHA-256 を照合して停止する柵を設置。
  - `build_report_Bl3.py:_selftest_sealed` で予想改ざん時に確実に停止することを自己検査で実証。完全に閉じています。
- **R2-重大2・R1-m2・R2-中5（一致段と結果開く段の結びつき・環境・DRY）**:
  - `analyze_Bl3.py:330-344`（`load_outputs`）で、各組の JSON ファイルおよび `session.json` の SHA-256 を含む `files` 同定辞書を作成。
  - `judge` でこれを記録し、`open_checked`（`:457-464`）で `J.get('inputs') != files` による厳密な一致判定を実施。
  - 組間の DRY 混在の停止（`:399`）、strict な環境差分（commit, dry, canon_sha16, directions_npz_sha256, layer_idx, coef）での停止（`:401`）、非DRY時の等方本数（1999本）チェック（`:407`）、手元器・正本の凍結記録照合（`frozen_versions_bad`）を網羅。完全に閉じています。
- **R2-中3（相 check のコミット照合・ガード抜け）**:
  - `freeze_Bl3.py:249-253` で相 check が走ったコミットの器・正本・設計事実・方向記録の SHA16 を `git show <commit>:<path>` で検証。
  - `boot_Bl3.py:51, 347-353` で `Stop` 例外を `BaseException` 派生とし、`model`, `model.model`, `lm_head`, 各層すべてに pre-hook ガードを設置して呼び出し回数をカウント（`:398`）。完全に閉じています。
- **R1-M1（本の計算の近道不使用の振る舞い検証）**:
  - `dry_run_Bl3.py:457-481` で、定数フラグの確認にとどまらず、全順伝播（1547回）において `model.register_forward_pre_hook(..., with_kwargs=True)` により `past_key_values is None`、`use_cache is False`、入力長が全長であることを動的に検証し、`prefix_cache` の呼出回数 0 を確認。完全に閉じています。
- **R1-m1（非有限値 NaN/Inf の取り扱い）**:
  - `bl3_core.py:60-61`（`p_and_tail`）で非有限値に対して即時 `ValueError` を送出。
  - `bl3_core.py:252-254`（`agreement`）で非有限値が存在すれば鍵順に依らず `agree: False`, `reason: 'non_finite'` を返却。
  - `bl3_run.py:36-39`（`require_finite`）で各計算出口で `ToolError` 送出。
  - `analyze_Bl3.py:263-265` で集計入口でも即時停止。完全に閉じています。
- **R1-m4（正本文から独立した札・門の検証）**:
  - `dry_run_Bl3.py:96-139`（`answer_labels`）で集計器の芯の関数を呼ばずに正本文から直接ロジックを再実装し、等方1999本の合成データで突合。
  - 行 333-351 で行動量 $y$ そのものを効き目に置いた場合に本の門の順位相関が数学的に厳密に 1.0 になることを利用した「答えの分かる合成」による門組み立て検証を実装。完全に閉じています。
- **R2-軽微10（門の行だけの升目除外時の読み型）**:
  - `build_report_Bl3.py:73-77`（`dropped_split`）で主升目と門行専用升目を分離し、門行専用升目のみの除外では `〈下見で一部を外した〉` を当てず、§0 に機械行を出力するよう修正。完全に閉じています。
- **R2-軽微14（凍結一行の登録者逐語の数値検査）**:
  - `make_frozen_Bl3.py:80-94`（`build_frozen`）で、組み立て時には一時的にプレースホルダー `STANDIN` を配置して `numbers_lint` を通し、その後に逐語行を戻す形に修正。逐語を変更する誘因を完全に排除して閉じています。

---

### (2) 直しが入れた新しい誤り（厳しい・甘い・止まらない）

足された照合・柵・例外処理について、「厳しい（正常な流れで止まる）」「甘い（何も捕まえない）」「止まらない（抜けている）」の観点から精査した結果、**1件の「止まるべき所で止まらない（照合の鎖の終端抜け）」** と、**2件の記録・注記レベルの挙動** を見出しました。

#### 【所見 2-1】（重さ: 中 / 凍結前に直すことを推奨）`build_report_Bl3.py` が `judge-Bl3.json` の存在および `analysis-Bl3.json` に記録された `judge_record_sha16` を照合していない（照合の鎖の終端抜け）
- **根拠**:
  - `tools/build_report_Bl3.py:320-337`（`sealed_and_frozen_bad`）
  - `tools/build_report_Bl3.py:338-368`（`load_inputs`）
  - `tools/analyze_Bl3.py:477`（`open_checked` 内の `A['judge_record_sha16'] = judge_sha16`）
  - `tools/sweep_Bl3.py:28-105`（`sweep`）
- **現象と壊れる筋書き**:
  - 裁定 D236（R2-重大2の直し）において、`analyze_Bl3.py open_checked` は `judge` 段の記録ファイルの SHA16 を受け取り、開かれた結果辞書に `A['judge_record_sha16'] = judge_sha16` として正しく記録しています（`analyze_Bl3.py:477`）。
  - しかし、その出力を受け取って最終報告書を組み立てる `build_report_Bl3.py` の `load_inputs` では、正本・凍結記録・封印記録・予想ファイルの照合（`sealed_and_frozen_bad`）や `sweep` による欠け検査は行っているものの、**手元の `records/Bl3/judge-Bl3.json` の存在確認や、`analysis-Bl3.json` 内の `judge_record_sha16` が手元の `judge-Bl3.json` の SHA16 と一致しているかの照合が一切行われていません**（`meta` 辞書にも `judge` の SHA16 は収集されていません）。
  - また、`sweep_Bl3.py` の `sweep` 関数も `judge_record_sha16` キーの存在をチェックしていません。
  - このため、もし何らかの誤操作（あるいは事後的な差し替え）によって `judge-Bl3.json` が失われていたり、別の一致段の記録が存在していたり、あるいは `open_checked` を通さずに直接手作業で作成・編集された `analysis-Bl3.json` が置かれていた場合でも、`build_report_Bl3.py` は何ら警告も停止も発せずに報告書草案を組み上げてしまいます。
  - 「一致だけを見る段（judge）→ 結果を開く段（open）→ 報告の組み立て（build_report）」という一連の保証の鎖において、open から report への受け渡し部分で照合が抜け落ちています（止まるべき所で止まらない）。
- **確かめ方**:
  - `records/Bl3/judge-Bl3.json` を削除するか、別の内容に書き換えた状態で `python tools/build_report_Bl3.py` を実行する（あるいは `_selftest_sealed` と同様の一時環境で `A['judge_record_sha16']` をダミーにして実行する）。現行コードでは停止せずに完了することを確認できます。
- **対処案**:
  - `tools/build_report_Bl3.py` の `load_inputs` 内（行 353 付近）に、以下の検証を追加する：
    ```python
    jp_ = P('records/Bl3/judge-Bl3.json')
    if not os.path.exists(jp_) or sha16f(jp_) != A.get('judge_record_sha16'):
        raise SystemExit('一致だけを見る段の記録が無いか、集計の記録に写した SHA16 と違う（止める）: %s' % jp_)
    ```
    あわせて `meta` に `'judge': sha16f(jp_)` を含め、報告書の冒頭メタデータ区画にも印字すると、監査性が完全に閉じます。

---

#### 【所見 2-2】（重さ: 軽微 / 記録に置けば足りる）`boot_Bl3.py` の `package('final')` で生成された `final.zip` のハッシュがディスク上の `session.json` に反映されない
- **根拠**: `tools/colab/boot_Bl3.py:83-104`（`package`）および `:337-340`（`finish`）
- **現象**:
  - `package(tag, extra)` 関数は、まずディスク上の `session.json` に `S` を書き出した後、`od` 内の全ファイルを zip 化（`zp`）し、その zip の SHA-256 をメモリ上の `S['zips']` に追記します（`:96`）。
  - 相 main の各組（`part-main`, `part-recompute`, `part-secondary`）の zip ハッシュは、次の組の処理や最後の `finish()` で `write_json` が呼ばれるため、ディスク上の `session.json` に記録されます。
  - しかし、全体の終了時に呼ばれる `finish()` 内の `package('final', ...)` では、`final.zip` を作成してメモリ上の `S['zips']` に追記した後に、再度 `session.json` をディスクに書き出す処理がありません。
  - そのため、実行完了後にディレクトリ `od` に残る `session.json` には、`final.zip` 自体の SHA-256 が記録されません（もちろん `final.zip` の内部に含まれる `session.json` に自身のハッシュを入れることは不可能ですが、ディスクに残る session に最終 zip の情報が残らない非対称性があります）。
- **影響**:
  - `analyze_Bl3.py` や `freeze_Bl3.py` は `session.json` 内の `zips` リストを検証キーとして使っておらず、`progress.log` には `[boot_Bl3] packaged final ...` として正しい SHA-256 が刻まれているため、後続の判定を止める誤りにはなりません。
- **対処案**:
  - `package` の最後、または `finish` の return 前に `write_json(os.path.join(od, 'session.json'), S)` を一度呼ぶようにすれば綺麗に収まりますが、必須ではなく記録の注記で足ります。

---

#### 【所見 2-3】（重さ: 軽微〜中 / 記録に置けば足りる）下見が「器の誤り」で終了し「やり直さない」と裁定した場合に、本の凍結・報告組み立てを通過させる例外フラグがない
- **根拠**:
  - `tools/freeze_Bl3.py:372-373`（`main_freeze_checks`）
  - `tools/build_report_Bl3.py:348`（`load_inputs` の `atts = FR['main_freeze']['pilot_attempts']`）
  - 正本 `pilot.decision.tool_error.rerun`（「やり直さないときは、q1 を採点せず、『器の誤りで下見を終えられなかった』と記録して閉じる」）
- **現象**:
  - 本の計算の器の誤りについては、裁定 D225 および `build_report_Bl3.py` の `--main-tool-error` フラグにより、結果を開かずに閉じて報告書を組む経路が用意されています。
  - 一方、下見（相 pilot）の段階で器の誤り（`tool_error`）が発生し、登録者が「やり直さない」と裁定した場合、`freeze_Bl3.py main` は `:372-373` で `bad.append('最後の下見の試みが器の誤り（本の凍結の前に登録者の裁定を仰ぐ）')` となり `SystemExit` で停止します。
  - そのため `FREEZE-RECORD-Bl3.json` に `main_freeze` が書き込まれず、`build_report_Bl3.py` は `FR['main_freeze']` の参照で `KeyError` となり、報告書を組むことができません。
- **影響**:
  - 本器の記述にもある通り「登録者の裁定を仰ぐ」ことが大前提の非常停止であるため、この事態が発生した場合は登録者とコーディネータが手動で例外台帳を記帳して対応する運用となっており、正常な実験フローを妨げるものではありません。
- **対処案**:
  - 運用の注記として「下見の器の誤りでやり直さない場合は、登録者裁定のもとで凍結記録を手動記帳する」旨を了解事項として記録に置いておけば足ります。

---

### (3) 器の決め（第二部 採否の案 Bの表「変えない」としたものの当否）

第二部の採否の案 B の表および器の段の記録 §13 に挙げられた「変えない」とした器の決め（R1: 13項目、R2: 11項目）について精査しました。

**結論: すべて「変えない」の判断で妥当です。凍結の前に変更を要するものはありません。**

主な判断根拠は以下の通りです：
- **R1-1（バッチ並びの種のキーに外した升目の組も数える）**: 升目と符号の並び順のインデックスを SeedSequence に渡す設計は決定論的であり、途中の升目が除外されても残った升目のシードが不変に保たれるため、再現性の観点から合理的です。
- **R1-2（無操作のバッチ揺れの混入）**: 効き目は同一バッチ内の無操作との差分 $lo[d] - lo[\text{NOOP}]$ として定義されており、バッチ共通の揺れは相殺されます。無操作自体の微小な揺れが残る可能性はありますが、下見 (vi) で測定される揺れの床の範囲内であり、モデルの振る舞いとして自然です。
- **R1-3（出口の値の自己検査が最初の升目のみ）**: `logit_check` は語彙射影行列（`lm_head`）と最終正規化層（`norm`）がモデル本来の出力と整合しているか（二重正規化等の実装ミスがないか）を確認する機構です。これはプロンプト内容に依存しないモデル構造の検証であるため、1升目で確認すれば目的を完全に達しています。
- **R1-4, 5, 6, 9（下見の各統計における主升目・外した升目の扱い）**: 正本 `pilot.checks` の定義および下見の目的（モデルが直答形式で健全に測定可能かの判定）に完全に合致しており、余計な複雑化を避ける意味でも現状のままで正当です。
- **R1-7, 8（境界値の扱い・tie）**: 境界をどちらに含めるかは定義の問題であり、正本に齟齬はなく一貫して実装されています。
- **R1-10（書き換え器の use_cache 既定）**: 起動器および合成データ器が明示的に `use_cache=False` を指定して呼び出しており、独立した別個体の器の内部デフォルトを無理に書き換えない方針は独立性の保全として妥当です。
- **R2-6 / 軽微15（版照合から scipy を除外）**: 計算の順伝播・hook・読み取りのクリティカルパスで scipy は一切 import されていません。Colab 環境での pip 依存関係の衝突によるクラッシュを防止する実務的判断として合理的であり、docstring への記載と session への実バージョンの記録で透明性も確保されています。
- **R2-9（||static|| 許容 1e-9）**: float64 のノルム突合として十分かつ厳密な値です。
- **R2-10（judge が secondary 欠損でも一致を出す）**: judge は裁定 D219 に基づく「独立の再計算（recompute）の一致」を判定する門であり、乙（secondary）は記述（descriptive）であるため、judge の責務外とするのは設計通りです。secondary の欠損は直後の `sweep_Bl3.py` で確実に捕捉・停止されます。

---

### (4) 合成データの正式の記録（第八部）の確かめ

第八部の正式な記録 `records/Bl3/dry-run-Bl3-2026-09-25.md`（72項目）および `tools/dry_run_Bl3.py` v3 の実装を詳細に検算しました。

**結論: すべての確かめが名通りのものを正しく検証しており、器と誤りを共有しておらず、答えを器から借りていません。**

具体的な検証結果：
1. **独立した答え合わせ（R1-m4 の解決）**:
   - `dry_run_Bl3.py:96-139` の `answer_labels` は、`bl3_core.py` や `analyze_Bl3.py` の内部関数（`row_labels` や `gates`）を一切呼び出さず、正本の定義文（`p_rule`, `iso_outside`, `second`, `side_rule`）から numpy を用いて完全にゼロから独立実装されています。
   - `synth_effects` で生成された奇でない押し・非ゼロ中心・等方外を含む効き目に対して、`AZ.row_labels` の出力と照合し、食い違い 0 件（等方外 12 行）であることが確かめられています。
   - 「答えの分かる合成での門の組み立て」（行 333-351）では、効き目に行動量 $y$ そのものを代入することで、門の順位相関が数学的必然として厳密に 1.0 になることを利用しており、集計器から答えを借りることなく、家族キーや符号・単位の紐付けミスがないことを完璧に証明しています。
2. **振る舞いによる検証（R1-M1 の解決）**:
   - 行 457-481 の「本の計算は近道を使わない（振る舞い:...）」では、単に `MP['shortcut'] is False` などの定数を見るのではなく、PyTorch の pre-hook（`pre_kw`）を用いて、本の計算の順伝播 1547 回のすべてにおいて：
     - `past_key_values` が渡されていないこと（`fwd['past'] == 0`）
     - `use_cache` が偽であること（`fwd['use_cache'] == 0`）
     - 入力長がプロンプト＋書き出しの全長であること（`fwd['short'] == 0`）
     - `prefix_cache` の呼出が 0 回であること（`pc_calls[0] == 0`）
     を実際に動的に計測して検証しています。名札だけの検証（教訓15の型）を完全に脱しています。
3. **等方の外が出る枝の網羅（R1-m5 の解決）**:
   - 正本と同じ等方 1999 本を用い、等方の外に出る行（12行）を実際に発生させ、裁定 D232（等方の外の行だけで裾と側を比べる）、q7、読みの型（`〈両方の外〉`、`〈埋もれる〉`）の全分岐が正常に機能することを確かめています。
4. **起動器のサブプロセス実行と改ざん検知（R2-中6・R2-重大2 の解決）**:
   - `part_boot`（行 809-873）において、実際に別プロセスとして `boot_Bl3.py` の相 check, pilot, main（DRY）を実行し、その出力を CLI 経由で `analyze_Bl3.py judge`, `open`, `sweep_Bl3.py`, `build_report_Bl3.py` に通す端から端までの往復が検証されています。
   - さらに、出力ファイル `main.json` の効き目を改ざん（+1000）した写しに対して `open` を実行した際、`結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）: ['main']` という正しいエラーメッセージで停止し、ファイルが書き出されないことを実証しています。

---

## 2. 判定

次の三つから、以下を選択します。

**「凍結の前に直すものがある（直した後の確かめは起草者の合成データの記録で足りる）」**

### 判定の理由
- 前回の二体による検分（R1, R2）で指摘された重大 2 件、中 5 件、軽微 15 件の計 22 件（R1の7件と合わせ計29件）の所見に対する直しは、極めて誠実かつ徹底的に実装されており、大半の防護柵が格段に強化されています。
- しかしながら、**【所見 2-1】（`build_report_Bl3.py` における `judge-Bl3.json` の SHA16 照合抜け）** は、裁定 D236 で意図された「一致段（judge）が見た出力を結果開く段（open）が開いているか、そしてその開かれた集計が正しく報告書に組まれるか」という「保証の鎖」の最後の終端において、照合が抜けている状態です。
- 直しは `build_report_Bl3.py` の `load_inputs` に手元の `records/Bl3/judge-Bl3.json` の SHA16 と `A.get('judge_record_sha16')` を突き合わせるチェックを 2〜3 行追加するだけの局所的なものです。
- この直しを入れると `build_report_Bl3.py` の SHA16 が変わるため、合成データの正式記録の再取得（約5.4時間）が必要になりますが、新たな外部レビュー巡を重ねるほどの構造的変更ではなく、**「直した後の確かめは起草者の合成データの記録（72/72合格および版照合の一致）で足りる」** と判断します。
- （注: もし登録者が、所見 2-1 について「`open_checked` において既に `files` 同定辞書による judge と open の入力完全一致が機械的に担保されているため、報告組み立てでの二重チェックは不要であり、記録（注記）に置けば足りる」と裁定される場合は、器をこれ以上変更せず「このまま下見の前の凍結の段に進めてよい」に移行することも論理的に許容されます。登録者の裁定を仰ぎます。）

---

本検分のいかなる記述も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。