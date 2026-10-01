Case only; comparing case-insensitively.模型: Claude Opus 5.5・作り手: Anthropic

R2（流れと記録）の検分を、束の展開・SHA の照らし・自己検査の走り・器の読み・小さな試し（器の関数を合成の入力で直接呼ぶ）で行いました。道具の回数の上限で途中までになったので、読めなかった所は 5. に分けて書きます。ウェブ検索と外への呼び出しはしていません。

全体の見立てを先に書きます。自己検査と合成データの正式の記録は、書かれた範囲では通ります。ただし、下見の前の凍結（prefreeze）を公開の置き場で走らせると、少なくとも二つの理由で止まる形です（R2-01・R2-12）。また、錠と形の確かめのいくつかが正本の字より弱く（R2-02・R2-03・R2-04）、それらの道は合成データの確かめで一度も通っていません（R2-08）。

## 2. 所見の一覧

### 重い

**R2-01　重い｜合成データの正式の記録の SHA 表が、凍結の器の閉包を覆わない（凍結の前の凍結が止まる）**
- 所: `tools/dry_run_Bprime.py` 行 ~72–82 の `closure_table(BP)` と、`tools/freeze_Bprime.py` の `dry_record_check`（行 ~185–205）。
- 何が起きるか:
  - `closure_table` は作業の置き場の形（BP）で閉包を取ります。作業の置き場では別の個体の二つの器が `tools/independent/` にあるので、`FZ.P('tools/bprime_recompute_rewrite.py')` が見つからず、閉包から落ちます。
  - 公開の形では、凍結の器の閉包は 42 で、この二つを含みます。
  - その結果、正式の記録（`dry-run-Bprime-2026-09-30.md`・表 44 行）に対して `dry_record_check` が `lack ['tools/bprime_recompute_rewrite.py', 'tools/bprime_reextract.py']` を返し、prefreeze は「版の SHA16 の表が、器の閉包と正本と台帳を覆わない」で止まります（走らせて確かめた・4. に出力）。
  - 逆に prefreeze を作業の置き場の形で走らせる積もりなら、二つの器が凍結の閉包から黙って落ち、錠の外になります（こちらの方が悪い）。
- 直し方の案:
  - `closure_table` を公開の形の一時の置き場 T で取るか、publish_map で公開の道筋に写してから取る。
  - 合成データの確かめの中で、書いた記録に `FZ.dry_record_check` を当てる行を足す。
- 確信度: 高。走らせて確かめた。

**R2-02　重い｜抽出の記録の形の項目（T01）の機械の確かめが、正本の六項目のうち二つ半を見ていない**
- 所: `tools/colab/boot_bprime.py` の `PH_form_items`（末尾近く）と、相 behavior の呼び出し。
- 何が起きるか:
  - 正本 `computation.extraction_record.form_items` の次の三つが確かめられていません。
    - 項目 5「時刻が封印の後で行動の下見の起動の前」
    - 項目 6「相 extract の起動の記録が一つで、抽出の記録が指す走行と同じ」
    - 項目 2 のうち「正本と器の SHA」
  - 鍵がそろっているか（time_utc・start_record_sha256 の在るなし）しか見ません。
  - 小さな試しで、time_utc が 1999 年で、start_record_sha256 がどの起動の記録とも合わない記録を渡すと `[]`（通る）でした。両方を None にしても `[]` でした。
  - 封印の後に人の判断を置かない代わりの機械の門（T01）なので、ここが弱いと人が確かめない穴になります。
- 直し方の案:
  - `R['time_utc']` を `SR['sealed_at_utc']` より後、かつ行動の下見の `START['time_utc']` より前と照らす。
  - `records/Bprime/runs/start-extract*.json` がちょうど一つで、その SHA-256 が `R['start_record_sha256']` と同じことを確かめる。
  - その起動の記録の `contract_sha16`・`tools_sha16` を今と照らす。
  - 合成データの確かめに、落ちるべき二つの形（時刻と起動の記録）を足す。
- 確信度: 高。走らせて確かめた（4. に出力）。

**R2-03　重い｜本の凍結の確かめの七つ目（集計・札・読みの規則・報告の組み立ての器が下見の前の凍結のまま）が無い**
- 所: `tools/freeze_Bprime.py` の `main_freeze_checks`。説明の文には「正本 `computation.main_freeze.checks` の八つ」とあります。
- 何が起きるか:
  - SHA の違いは `bl3_core.ledger_chain_bad` だけで照らしています。
  - この関数は、台帳に差分を記せばどの道筋の違いでも許します。`analyze_Bprime.py`・`build_report_Bprime.py`・`sweep_Bprime.py`・`bl3_core.py`・`bprime_core.py` の違いも、台帳に記せば本の凍結を通ります。
  - 正本は、この種類の器は「違えば止める」と別に定めています。grep でこの確かめが器に無いことを見ました。
- 直し方の案: 集計・札・読み・報告の器の閉じた一覧を器（か正本）に置き、`res['changed']` と重なれば止める。自己検査にも止まる例を足す。
- 確信度: 高。読んで推した（grep で確かめた）。

**R2-04　重い｜報告の組み立ての器に、段ごとの起動の記録の数と報告の頭の走行の数の照らし（T13）が無い**
- 所: `tools/build_report_Bprime.py`（全体）。`analyze_Bprime.py`・`sweep_Bprime.py` も同じ。
- 何が起きるか:
  - 正本 `computation.start_records.rule` は、本の凍結の器と報告の組み立ての器の両方に照らしを求めています。
  - 報告の器には、起動の記録・`runs`・T13 に当たる字がありません（grep で零件）。報告の頭に走行の一覧を並べる型もありません。
  - 報告の器は下見の前の凍結で固まり、後から直せない（R2-03 の決まり）ので、凍結の前に足す要があります。
- 直し方の案: `records/Bprime/runs/` の start と end を段ごとに数えて報告の頭に並べ、下見の試みの数・逸脱の台帳の行と照らして、合わなければ止める。掃き出しの鍵にも足す。
- 確信度: 高。読んで推した（grep）。

**R2-08　重い｜正本 `computation.synthetic_checks[8]`（本の凍結の器の三つの止まり方）の二つが無く、凍結と錠の道が一度も通っていない**
- 所: `freeze_Bprime._selftest`（13 項目）と、`dry_run_Bprime.py` の四。
- 何が起きるか:
  - 「決定の出し直しの不一致で止まる」はあります。
  - 「足してよい鍵の外が増えると止まる」は正の例だけです（R2-07 も見てください）。
  - 「SHA の違いで止まる」は凍結の器の自己検査にありません。
  - 正式の記録の四は、prefreeze・封印・本の凍結の器を走らせていません。
  - 起動器の錠（行 ~170–194・凍結と封印の記録・台帳のつながり・暦の期限）と形の項目は、DRY では飛ばす形で、どこでも実行されていません。
  - R2-01・R2-12 が見つからなかったのはこのためです。
- 直し方の案:
  - 公開の形の一時の置き場で `git init` と commit をし、次を通す部を足す。
    - prefreeze（Colab の確かめは合成）
    - 封印（合成の予想）
    - runs の置き
    - DRY の出力を印をつけて本の凍結に当てる
  - 起動器の錠の塊を関数に切り出し、DRY で呼べる形にする。
- 確信度: 高。読んで推した（記録の表と自己検査の項目を照らした）。

**R2-12　重い｜凍結の器の自己検査の一覧に、公開の置き場では通らない器が入っている**
- 所: `freeze_Bprime.SELFTESTS`（行 ~58–61）と `prefreeze_checks`（行 ~285–295）。
- 何が起きるか: `P(t)` と `cwd=ROOT` で公開の置き場の器を走らせるので、次の器が落ちます。
  - `bprime_publish_map.py --selftest`: 置き場の全体（`.git` を含む）を歩いて、当たらないファイルがあれば rc=1 です。束（公開の形）で走らせると rc=1・当たらない 207・重なり 1 でした。`publish_Bprime.py --selftest` も rc=1 でした。
  - 別の個体の二つの器の `--selftest`: 器の置き場から二つ上を B′ の置き場とみなすので、公開の形では正本を見つけられません（README と器の段の記録の申告）。
  - 合成データの確かめの一は、この三つを作業の置き場で走らせるか外していたので、凍結の器の一覧とずれていました。
  - prefreeze が「器の自己検査が落ちた」で止まります（凍結は公開の置き場で行う・本の凍結が `git -C ROOT` を呼ぶ、から推した）。
- 直し方の案: publish_map の自己検査を、例だけの閉じた検査と置き場の全体の振り分けとに分ける。凍結の器は、作業の置き場の形の器を作業の置き場の道筋で呼ぶか、一覧から外して合成データの記録の合否で代える。
- 確信度: publish_map は高（走らせた）。独立の器は中（読んで推した・torch が無く走らせていない）。

### 中

**R2-05　中｜起動の記録と出力の SHA の記録の名が固定で、やり直しの走行が公開の置き場で重なる**
- 所: `boot_bprime.py` の `START_LOCAL = start-<相>[-組].json` と end の名、`freeze_Bprime.runs_count_bad`。
- 何が起きるか:
  - 正本は、器の誤りでのやり直し（extract・behavior・pilot・main）を認め、二つの記録を報告の頭に並べる形です。
  - しかし二度目の start を公開すると `records/Bprime/runs/start-pilot.json` を上書きします。
  - `runs_count_bad` は start と end の数どうし（どちらも 1）を比べるだけで、試みの数（`len(pilot_dirs)`）と比べません。
  - Colab のランタイムが start の後の push を待つ間に切れたときも、start を取り直すので同じ重なりが起きます。
- 直し方の案: 名にセッションの頭 8 字を入れ、run は自分のセッションの名で照らす。段ごとに start・end・試みの数・台帳の `pilot_rerun` の行を照らす。
- 確信度: 中〜高。読んで推した。

**R2-06　中｜錠の「公開の記録に印字された SHA と照らす」が起動器に無い**
- 所: `boot_bprime.py` の run の段（行 ~248–262）と、相 main・recompute。
- 何が起きるか:
  - 起動の記録は `freeze_record_sha16`・`seal_record_sha16` を持ちますが、run の段は照らしません（正本と器の SHA だけ照らします）。
  - 本の計算が使う `FR['main_freeze']['pilot']`（バッチと外した升目）は、凍結の記録の中身そのもので、凍結物の SHA の照らし（`ledger_chain_bad`）の外です。
  - start のコミットから run のコミットの間に凍結の記録が変わっても、機械では捕まりません（git の履歴には残ります）。
- 直し方の案:
  - run の段で START の二つの SHA16 を今と照らす。
  - 本の凍結の器が `FR['main_freeze']` の正準の JSON の SHA16 を全体の台帳の行に印字し、起動器がそれと照らす。凍結の記録そのものの SHA は、後の逸脱の行で変わるので、節の SHA にする方が保ちます。
- 確信度: 高（事実）、中（重さ）。登録の文を残すなら、器との食い違いになります。

**R2-07　中｜本の凍結の「足してよい鍵」の確かめが空回りしている**
- 所: `freeze_Bprime.main_freeze_content` と `main_freeze`、`bprime_core.main_freeze_keys_ok`。
- 何が起きるか:
  - `added` は器に書き込んだ名（正本の一覧と同じ字）から作るので、`main_freeze_keys_ok` は落ちようがありません。
  - 実際に足す物は照らしていません。`pilot_attempts`・`pilot`（下見の記録の全体: `iv`・`chain`・`variants_used`・`behavior_state`・`n_forward`・`pa_transformed`・`behavior_rate` など）・`sessions`・`seal`・`runs` などです。
  - 正本の「これら以外の鍵が増えたら止める」が効いていません。
- 直し方の案: `FR['main_freeze']` の実際の鍵と、下見の記録の鍵を、閉じた一覧（付帯の鍵を含む）と照らす。自己検査に「外の鍵を一つ足すと止まる」を足す。
- 確信度: 高。読んで推した。

**R2-09　中｜読み取りの下見の起動器が、行動の下見の閉じた記録を確かめずに読む**
- 所: `boot_bprime.py` 相 pilot（行 ~372）。
- 何が起きるか:
  - 正本 `behavior_pilot.order` は「その記録の SHA を確かめてから進む」と定めていますが、器は `json.load` するだけです。
  - kind・`contract_sha16`・閉じた記録が指す start と end が `runs/` と合うか、を見ません。
  - ファイルが無ければ FileNotFoundError になり、「止める」でなく「予期しない誤り」の道に入ります。
- 直し方の案: 相 pilot の起動の記録に閉じた記録の SHA16 を入れて run で照らす。kind と正本の SHA を照らす。無ければ `stop()` にする。
- 確信度: 高。読んで推した。

### 軽い

**R2-10　軽い｜DRY のための既定の値が、DRY でないときにも黙って使われうる**
- 相 main・recompute の `kz = … or {'k': 1.0, 'z0': 4}` と、相 behavior のバッチの `… or '8'` です。
- 相 pilot は k が無ければ止まるので実害は小さいですが、既定は DRY のときだけにし、ほかは止める方がよいです。
- 確信度: 高。読んで推した。

**R2-11　軽い｜start の段が OP4B_PART を確かめない**
- 相 main・recompute の start を組なし（か誤った組）で走らせると、どの run とも合わない起動の記録が公開され、R2-05 の数を乱します。
- 確信度: 高。読んで推した。

**R2-13　軽い｜閉じる器が採点そのものを計算し直さない**
- `close_behavior_Bprime.read_outputs` は、数（`closing_digests`）と升目の集計だけを計算し直します。`score_trial` を試行に当て直していません。
- CPU で安いので、採点の器の環境の違いを捕まえるために足す案です。
- 確信度: 中。

**R2-14　軽い｜器の誤りで閉じる道に、系統外の模型による採点ができなかった文が入らない**
- `do_close_tool_error` は `external: None` です。T17・T27 の「採点ができなかった（理由）」を入れるかを決めておくのがよいです。
- 確信度: 低（意図かもしれない）。

**R2-15　軽い｜説明の文と記録の字の小さな食い違い**
- 説明の文の版が古いまま: 起動器の説明は v0（VERSION は v0.3）、凍結の器の説明は v0（v0.1）です。
- 凍結の器の説明は「八つ」ですが、実装は七つです（R2-03）。
- 器の段の記録の「781.0 秒」と、正式の記録の「776 秒」が違います（測り方の違いかもしれません）。

**R2-16　軽い｜改行の扱いがそろっていない**
- SHA16 は CRLF を LF に直してから取りますが、予想の JSON・起動の記録・閉じた記録は生のバイトの SHA-256 で照らします。
- Windows の公開の置き場の写しが autocrlf で取り出し直されると、本の凍結の器の予想の照らしが誤って落ちえます。
- `.gitattributes` で records と tools を `eol=lf` か `-text` にする案です。
- 確信度: 低。

**R2-17　軽い（役割の外）｜抽出の記録の確かめの三つが常に真**
- `bprime_phases.extract` の `checks` のうち、`norms_finite_nonzero`・`dim_match`・`no_readout` は常に True です。
- 形の項目 4 は、実質 g との一致と係数の確かめだけを見ることになります。中の関数が落ちるときに例外を出すなら害は無いので、R1 の見る所として申し送ります。
- 確信度: 低。

## 3. 是認

- 束の目録の 603 本すべてで、SHA-256（目録は大文字）とバイト数が合いました。目録の外は目録と README の二本だけです。
- README の 13 の自己検査は、固定の版（numpy 2.4.6・transformers 5.16.1・torch 無し）ですべて通りました。閉じる器も torch 無しで通りました。
- 自己検査は置き場に `__pycache__` のほかは何も書きませんでした（`find -newer` で確かめた）。
- 正式の記録の SHA 表 44 行は、束のファイルと一字違わず同じです（`differ` 空）。束は、合成データの確かめを走らせた版のままです。
- run の段の確かめは正本どおりに書かれています（読んで確かめた）:
  - 公開した起動の記録と手元の記録が同じこと
  - 相・組・正本・器の SHA が同じこと
  - DRY でないときの検査用の環境変数の締め出し
  - 40 桁のコミットと、汚れた作業木での停止
- K12 の直しは正しい形です。本の凍結の後の台帳の行だけでつなぎ、本の凍結の `frozen_sha16` の鍵は下見の前の鍵と同じなので、起動器の `now_s` が覆います。
- 器どうしの口は、名と形が合っていました（読んで確かめた）:
  - 閉じた記録の道筋（閉じる器と、起動器と凍結の器）
  - セッションの kind（`bprime_colab_pilot`）
  - 出力の SHA の記録の kind と相
  - 出力の置き場の起動の記録の写し（K19）
  - 封印の記録の `predictions.<役>.path/sha256` と `sealed_at_jst`
  - 抽出の記録の鍵（`row_D`・`npz_sha256`・`coefficient`・`g_match`）
- 決定の出し直しは、`run_pilot` の記録の形（vi の a と b・cells の mass と pa と pass_i_ii・batch・floor・`cells_decision` の出力・vi で止まるときの三つの鍵）と合っています。
- `calendar_closed` は、封印の日を 0 日目とし、60 日目の終わりまで開いています。K2 の字のとおりです。
- 封印の器は、コーディネータが先・一度だけ・凍結の記録の書式の SHA16・本の凍結の後は封印しない、を守っています。
- 閉じる器は次を確かめてから閉じます: 一度だけ書く・数と集計の計算し直し・束と依頼の文の作り直しの一致・呼び出しの記録の依頼の文の SHA16。
- 系統外の模型による採点の依頼の文は、K6 の塊の選び方（最初の閉じた ```json の塊、無ければ最後の平らな {…}）と、二つの族の破局の決まりを文にしていて、合成の例（量零の a・escalation 4・大文字の札が平らな道）と合っていました。
- 移し方の表の自己検査の例 18 件は通りました（置き場の全体の振り分けの部分は R2-12）。

## 4. 走らせた記録

環境: Python 3.12.3・scipy 1.17.1（元から在った）・torch 無し。

```
pip install numpy==2.4.6 transformers==5.16.1 --break-system-packages
…Successfully installed … numpy-2.4.6 … tokenizers-0.23.2 transformers-5.16.1 …
huggingface_hub 1.33.0 / numpy 2.4.6 / safetensors 0.8.0 / scipy 1.17.1 / tokenizers 0.23.2 / transformers 5.16.1
export OP4B_REPO="$PWD" OP4B_PUBLIC_REPO="$PWD" OP4B_PUB_TOOLS="$PWD/tools" PYTHONIOENCODING=utf-8
```

自己検査（README の 13 本・すべて rc=0）:

```
bprime_core.py v0.1 SELFTEST PASS（11 群・床の無い形の k 61042.0・床つきの k 5.779・z₀ 1）
bprime_typo.py v0 SELFTEST PASS（12 例・冪等・ラベルと検分の印と鍵の道は触れない）
bprime_external.py v1 SELFTEST PASS（抜き取り 40・見せる順の先頭 SK|Onull#17・S1|O-Ncold#20・S1|Onull#2・一致 40/40 と一件違いで 39）
analyze_Bprime.py v0.3 SELFTEST PASS（主の行 16・等方の外 4・二段の一致・壊した一段目の不一致・道の違い 0）
sweep_Bprime.py v0 SELFTEST PASS（出所の鍵 38・欠けのない合成の出力で欠け零・止まるべき形 12・止まったときの形 3）
build_report_Bprime.py v0.2 SELFTEST PASS（行 376・決まった行 313・自由の文 1・外す行 6・止まるべき当たり 4 通り・読みの表の型の名 8・質量と道の違いの枝・N1 を外して続けた報告の頭の行・止まった下見の報告）
make_frozen_Bprime.py v0 SELFTEST PASS（10 項目・止まるべき形 4）
[make_predictions_form_Bprime] 自己検査 OK（欄 8・予想の欄 4）
[seal_Bprime] 登録者の予想を写した: ../../../../tmp/tmp1umug7s4/r.json・SHA-256 7BBB5090E00288E5C0D2BEEC06E754541C074E6298E26B944E2275DA15AA7613
[seal_Bprime] 封印の記録を書いた: ../../../../tmp/tmp1umug7s4/rec.json
[seal_Bprime] 自己検査 OK（v0・凍結の記録の確かめと「予想しない」の欄を含む封印を端から端まで通した）
send_external_Bprime.py v0 SELFTEST PASS（鍵を読むが印字しない・送る本文・--go が無ければ送らない・送る操作はしていない）
make_manifest_Bprime.py v0 SELFTEST PASS（断片の名は索引から・手元と目録の違いで止まる・断片の欠けで止まる・外には問い合わせていない）
freeze_Bprime.py v0.1 SELFTEST PASS（13 項目・器の閉包 42・凍結物の型 49・全体の走りは合成データの正式の確かめで見る）
[transformers] PyTorch was not found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
close_behavior_Bprime.py v0.1 SELFTEST PASS（14 項目）
```

README の外で走らせたもの（束の公開の形で）。一度目は私のシェルが /bin/sh で `PIPESTATUS` が「Bad substitution」になったので、bash で取り直しました。

```
python tools/publish_Bprime.py --selftest   → rc=1
移し方の表に当たらないファイルか、行き先の重なりがある: ['MANIFEST-impl-bundle-Bprime.json', 'README-impl-bundle-Bprime.md', 'arms/NOTICE.md', 'arms/ledger-F.md', 'arms/ledger-M.md'] ['records/Bprime/MANIFEST-local-gemma-4-31B-it.json']
python tools/bprime_publish_map.py --selftest   → rc=1
bprime_publish_map.py v0.1 SELFTEST PASS（例 18・作業の置き場 630 ファイル: 移す 391・移さない 32・登録者の決め 0・当たらない 207・行き先の重なり 1）
重なり: ['records/Bprime/MANIFEST-local-gemma-4-31B-it.json']
```

630 は、束の 605 本に自己検査が作った `__pycache__` を足した数です。

小さな試し（器の関数を直接呼んだ）:

```
freeze_Bprime.import_closure(TOOLS) → 42（tools/bprime_recompute_rewrite.py・tools/bprime_reextract.py を含む）
freeze_Bprime.dry_record_check(C, closure) →
{"checks": 119, "as_expected": 119, "sha_table": {"files": 44, "lack": ["tools/bprime_recompute_rewrite.py", "tools/bprime_reextract.py"], "differ": []}}
["合成データの正式の記録の版の SHA16 の表が、器の閉包と正本と台帳を覆わない: ['tools/bprime_recompute_rewrite.py', 'tools/bprime_reextract.py']"]
boot_bprime.PH_form_items（time_utc 1999・起動の記録の SHA が合わない）→ []
boot_bprime.PH_form_items（二つとも None）→ []
```

SHA の照らしは、目録の 603 本すべてが合いました（sha_ok 603・bytes_bad 0）。R2 の器（計算した値＝目録の値）は次のとおりです。

```
2D332F457D1E8733FE475FB9F506FD2441F107762CD3D0FDE1C813FC0A332B8F tools/colab/boot_bprime.py
1CEBF15AAFFD703B37080093A85E1ED92769EA4D60BD875C8294F399D0F2AFFA tools/close_behavior_Bprime.py
59DA607142488D552CF8AEA4E0E4C83B5D740A664DCD38BAAE333EE6CC9F1790 tools/bprime_external.py
24553FE3BBFE08CAB81AF71F25A1764C47968A7D5049F1EA2236946B2DCFB9C5 tools/send_external_Bprime.py
C71E5860E81124452E6B9100401CC0F7234856B0F21CBD193A2881AEFBDB6287 tools/freeze_Bprime.py
0719E21A6EBFD2C741B54E07A050AAD23C66EA6D1B4C7BA7514961F38B7DFD8E tools/seal_Bprime.py
9C400361140944E230C97660468F22B6CFA1A62666C6C03F54A04A50A2E1044D tools/make_predictions_form_Bprime.py
8E738F9C940243E6CE4AFEFB516C096E3C851DEEAA75B17D106E89AF4B57A95A tools/make_frozen_Bprime.py
EA73E482D4EBF6CC06FD413364FCAEC45C6EB0BA8ACF7EFA55FA656FEFD27051 tools/publish_Bprime.py
62BD73DEBF7622AF7D71A199E53AEA0201AD7AAD838AC0A1C19ADF23B23CEEE3 tools/bprime_publish_map.py
E07C3AE97D44395ED9B15D2BAF2283FBF977408E84829971750001F968C14E77 tools/sweep_Bprime.py
0344831C134513F4C7EE3B30580358F5CF6775CDC9093C25D9FCDF3E4C812BBA tools/build_report_Bprime.py
2B9ED84FB2D7FC7286320FC3639223A84670A2009E4A4F78D9B772B4FBBCF35B tools/dry_run_Bprime.py
```

## 5. 読んでいない所・走らせていない所

- **走らせていない（torch が無い）**: `bprime_behavior`・`bprime_directions`・`dry_bprime`・`dry_bprime_behavior`・`dry_run_Bprime`・`bprime_recompute_rewrite`・`bprime_reextract`・`colab/boot_bprime`。起動器は、関数の読み込みと `PH_form_items` の直接の呼び出しだけです。
- **全文を読んだ**: 器の段の記録（K1〜K24）・`boot_bprime.py`・`bprime_publish_map.py`・`seal_Bprime.py`。
- **ほぼ全文を読んだ**: `freeze_Bprime.py`（末尾の `main()` の引数の扱いは読んでいません）・`close_behavior_Bprime.py`（`render_md` の後半と `main` は読んでいません）。
- **一部だけ読んだ**:
  - `dry_run_Bprime.py`（一〜三と閉包の表だけ・四の本体は読んでいない）
  - `bprime_phases.py`（extract・behavior・pilot・main_part）
  - `bprime_run.run_pilot`
  - 草案10 の §2・§4・§11・§12
  - 正本の該当の鍵
- **読んでいない**:
  - `build_report_Bprime.py` の走査の二つの層と要約の型の実装（見出しと grep と自己検査だけ）
  - `sweep_Bprime.py`・`make_frozen_Bprime.py`・`make_predictions_form_Bprime.py`・`publish_Bprime.py`・`send_external_Bprime.py`・`analyze_Bprime.py` の本体
  - `bprime_external.py` の `parse_reply` と `agreement`（上限で切れた応答を一致でどう数えるかは確かめていません）
  - `run_stageB_local.score_text`
  - Colab の走りの記録（`dry-progress.log`・`provenance.json`）
- **束に無かった**: 三巡目の採否の表（`reviews/design-round3/adoption-design-round3.md`）。T01〜T33 は、草案10 の〔T〕の印と正本の字でだけ照らしました。このため、読みの規則の走査・要約の型・二つの機種の節（T07〜T11）は、自己検査の合格のほかは見ていません。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。