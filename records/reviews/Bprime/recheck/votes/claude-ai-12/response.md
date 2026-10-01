Now the manifest SHA check.Now the selftests, as the request specifies.模型: Claude Opus 5.5・作り手: Anthropic

先にお断りします。この巡では道具の呼び出しの上限に達したため、検分は途中で終えています。見た所と見ていない所は、下の 3 と 5 に分けて書きました。ウェブ検索などの外の道具は使っていません。

## 2. 所見の一覧

### RC-01 止めたときの報告（K26）が本番の入口で走査の当たりになる
- **重さ**: それ以外。ただし凍結の前に直す側に入ります。報告の数・札・門には触れず、最後の確かめの取り直しで覆えます。一方、`build_report_Bprime.py` は `LOCK_EXCLUDED` に無く錠（U03）の対象なので、凍結の後は台帳に記しても直せません。
- **器と行**: `tools/build_report_Bprime.py` の `main_build`（`meta['judge'] = A.get('judge_record_sha16')`）と `build`（`D.b('shas', {…'判定': meta['judge']})`）。`tools/analyze_Bprime.py` の `open_stopped` は `judge_record_sha16` を `None` で書きます。
- **何が起きるか**: 下見の決定が「止める」だと、`analyze_Bprime.py stopped` → `build_report_Bprime.py build` と進みます。このとき報告の頭の SHA の行が「一致だけを見る段の記録 SHA16 None」になり、走査が `fill_value '[None]'` で当たります。`main_build` は報告を書いた後に 1 で終わります。自己検査の止まった下見の枝は、合成の `meta`（判定の値あり）を使うので、この形を通りません。
- **直し方の案**: 次の三つです。
  - `build` で判定の値が無いときは「なし」を埋める（「なし」は許す句にあります）。
  - `open_stopped` の実の出力と `main_build` と同じ組み方の `meta` で `build` と `scan` を通す例を、自己検査に足す。
  - 五に「止める下見 → 本の凍結 → 集計 stopped → 報告 build」の枝か行を足す（RC-02）。
- **確信度**: 高。
- **確かめ方**: `build` と `scan` を走らせて確かめました（4 に貼りました）。`main_build` の終わり方は読んで推しました。

### RC-02 K26 の直しを覆う正式の確かめの行が無い
- **重さ**: それ以外（行を足せば取り直しで覆えます）。
- **器と行**: `tools/dry_run_Bprime.py` の五（`part_freeze_path`）。通るのは「続ける」の道だけです。
- **何が起きるか**: 段 stopped と、報告の本番の入口とのつなぎを、どの行も通りません。RC-01 が今の記録で見えていないのはこのためです。
- **直し方の案**: 五で、`PILOT_SYN_CODE` の写しを「止める」にした枝を足します（本の凍結 → `analyze stopped --runs` → `build_report build` の返りが 0）。
- **確信度**: 高。
- **確かめ方**: 読んで推しました。

### RC-03 抽出の記録の形の項目の落ちる形が、直した部分を一つずつ覆っていない（U02）
- **重さ**: それ以外。器の実装は、読んだかぎり表のとおりです。落ちる形の行を足せば覆えます。
- **器と行**: `tools/dry_run_Bprime.py` の `form_items_cases`。
- **何が起きるか**: 項目ごとに、直しが無くても落ちる行が残ります。
  - **項目 2**: 落ちる形は手元の npz の違いだけです。U02 の芯である「相 extract の起動の記録の器の SHA を台帳の差分でつなぐ」（`ledger_chain_bad`・`deviations_n` 無し）は、どの落ちる形も通りません。出力の SHA の記録との違い・正本の SHA16・閉包の集合・重みの SHA も同じです。
  - **項目 5**: 「封印より前」の側だけで、「行動の下見の起動より後」の側がありません。
  - **項目 6**: 落ちる形（`n_starts=2`）は「器の誤りの記録が無い」と「台帳のやり直しの行が無い」の二つが同時に外れます。そのため、片方の照らしを消しても行は落ちます。「最後の走行を指す」の照らしの落ちる形もありません。
- **直し方の案**: 次の落ちる形を一つずつ足します。
  - 項目 2: 台帳の行の数を外す／閉包の SHA を一つ変えて台帳に差分を書かない。
  - 項目 5: 行動の下見の起動を抽出の記録より前にする。
  - 項目 6: 器の誤りの記録はあるが台帳のやり直しの行が無い／台帳の行はあるが器の誤りの記録が無い／前の走行を指す。
- **確信度**: 高。
- **確かめ方**: 読んで推しました。

### RC-04 `recompute_done` が器の誤りの走行も「終えた」と数える
- **重さ**: それ以外。錠そのものは `gate_bad` が `done=False` で期限を当てるので、通してしまうことはありません。
- **器と行**: `tools/g4_attempts_Bprime.py` の `recompute_done`。
- **何が起きるか**: 起動器は、器の誤りの組でも `finish()` で end の記録を書いてから止めます。そのため `runs/` に end の記録がそろえば、本の計算と独立の再計算が器の誤りで終わっていても「終えた」になります。すると暦の期限の後に `close-calendar` が「終えた（閉じない）」で止まり、閉じた記録と定型の文が書けません。
- **直し方の案**: 次のどちらかです。
  - 終えたかどうかを、一致だけを見る段の記録（`agree`）か組の出力の `tool_error` の有無で見る。
  - 限界の文か注に、この形を書く。
- **確信度**: 中。
- **確かめ方**: 読んで推しました。

### RC-05 `runs/` の読み方が器によって違う（器どうしの口）
- **重さ**: それ以外。どの外れも音を立てて止まる形で、黙って通る形ではありません。
- **器と行**: 凍結の器 `runs_count_bad` だけが `.json` で絞ります。起動器 `form_items_check`・集計 `runs_info`・`g4_attempts.recompute_done` は `os.listdir` をそのまま `runs_table` に渡します。
- **何が起きるか**: `runs/` に `.json` でないファイル（`.gitkeep` など）があると、本の凍結は通ります。一方で相 behavior は形の項目 2 と 6 で止まり、集計は `ToolError` で落ち、G4 の器も落ちます。
- **直し方の案**: 芯に一つの読み方の関数を置き、四か所から呼びます。
- **確信度**: 高。
- **確かめ方**: 読んで推しました。

### RC-06 案16 の決め（D278）と正本 v5・草案11 の字の食い違い
- **重さ**: それ以外。書き手が K28 で把握済みです。
- **器と行**: 字がまだ前の決めのままです。
  - 正本 v5 `independent_recompute.nk_decision`: 「バッチ一の速さを測ってから決める・D263」。
  - `reading.nk_note` と `limits.bprime` の該当の文: 「…決め（案 16）になったときは」。
  - 草案11 §9.1・§10・§353 行・案16 の表の行も同じです。
- **何が起きるか**: 報告の組み立ての器 v0.4 は、`nk_decision` を読まずに印を無条件に置きます。正本の直しが漏れると、報告は「印あり」と「条件つきの限界の文」を同時に持つことになります。
- **直し方の案**: 最後の正本の直しで字をそろえます。あわせて、凍結の器か報告の器の自己検査で「`decisions` に D278 がある」か「`nk_decision` の字」を照らし、器の無条件の枝と正本を機械でつなぐことをお勧めします。
- **確信度**: 高。
- **確かめ方**: 読んで確かめました。

### RC-07 `open_stopped` の説明と本の凍結の器の決まりの食い違い
- **重さ**: それ以外（注）。
- **器と行**: `analyze_Bprime.open_stopped` の説明は「下見が器の誤りで終わり、やり直さないときを含む」です。一方、`freeze_Bprime.main_freeze_checks` は最後の試みが器の誤りなら本の凍結をしません。
- **何が起きるか**: そのときは `main_freeze` が無いので、`open_stopped` は止まります。報告を組む道がありません。
- **直し方の案**: 説明を直すか、登録者の裁定の道として注に書きます。
- **確信度**: 中から高。
- **確かめ方**: 読んで推しました。

## 3. 是認

**直しが表のとおりだと確かめた行**（読んで照らしたもの。自己検査の通過で補ったものを含みます）:
- **錠・凍結・時刻まわり**: U01（〇の部）・U03・U05（K25 を含む。通る形が本番と同じ字の形の時刻で `gate_bad` を呼ぶので、K25 が戻れば落ちます）・U10・U11・U12・U16（RC-04 の注つき）・U19・U20・U24・U42・U43・U50。
- **組と走行**: U04（RC-05 の注つき）・U08・U09。
- **集計**: U17・U44。
- **報告**: U14・U15・U29（自己検査）。
- **小さな模型の確かめ**: U45・U46（行の組み方）。
- **器の段の所見**: K27。K28 は、報告の器 v0.4 の印の形と、確かめの器 v1.0 の行の両方です。印が無ければ Nk の側が落ち、static に付けば static の側が落ち、文の無い行があれば集合で落ちます。

**一部だけ見た行**:
- U02: 器は表のとおりですが、確かめの行は RC-03 のとおり覆いが足りません。
- U06: 凍結の器の一覧だけを見ました。
- U07: 集計・掃き出し・報告の側だけを見ました。閉じる器の側は見ていません。

**是認しない行**: K26（RC-01・RC-02）。

**見ていない行**: U13・U18・U21〜U23・U25〜U28・U30〜U41・U47〜U49・U51・U52。

## 4. 走らせた記録

**束をつないで照らした**（添えられたファイルの名は `recheck-bundle-Bprime_zip.001` と `_zip.002` でした）:
```
cat recheck-bundle-Bprime_zip.001 recheck-bundle-Bprime_zip.002 > recheck-bundle-Bprime.zip
sha256sum → 0a3226ad10f30987ec9d87f911e2875a625e3768536408d840b1a6ddecc57838（依頼の値と一致）
```

**版を固定した**（Python 3.12.3）:
```
pip install numpy==2.4.6 transformers==5.16.1 --break-system-packages
… Successfully installed … numpy-2.4.6 … tokenizers-0.23.2 … transformers-5.16.1 …
python3 -c "import torch" → ModuleNotFoundError: No module named 'torch'
```

**自己検査**（`export OP4B_REPO="$PWD" OP4B_PUBLIC_REPO="$PWD" OP4B_PUB_TOOLS="$PWD/tools" PYTHONIOENCODING=utf-8`・11 個すべて返り 0）:
```
bprime_core.py v0.2 SELFTEST PASS（14 群・床の無い形の k 61042.0・床つきの k 5.779・z₀ 1）
bprime_external.py v1.1 SELFTEST PASS（抜き取り 40・見せる順の先頭 SK|Onull#17・S1|O-Ncold#20・S1|Onull#2・一致 40/40 と一件違いで 39）
analyze_Bprime.py v0.4 SELFTEST PASS（主の行 16・等方の外 4・二段の一致・壊した一段目の不一致・鍵の集合の不一致・組の環境・本の凍結の照らし 7・升目の二つの組の印・止めたときの段・道の違い 0）
sweep_Bprime.py v0.1 SELFTEST PASS（出所の鍵 41・欠けのない合成の出力で欠け零・止まるべき形 16・止まったときと器の誤りで閉じたときの形 4）
build_report_Bprime.py v0.4 SELFTEST PASS（行 390・決まった行 322・自由の文 1・外す行 6・止まるべき当たり 4 通り・読みの表の型の名 8・…・独立の再計算なしの印）
make_frozen_Bprime.py v0.1 SELFTEST PASS（11 項目・止まるべき形 5）
send_external_Bprime.py v0.1 SELFTEST PASS（鍵を読むが印字しない・送る本文・依頼の文を改行を訳さずに読む・--go が無ければ送らない・送る操作はしていない）
freeze_Bprime.py v0.2 SELFTEST PASS（29 項目・器の閉包 43・凍結物の型 57・全体の走りは合成データの正式の確かめで見る）
bprime_behavior.py v1.1 SELFTEST PASS（標本化の鍵 8・確かめ 9 項目・止まる例 9）
g4_attempts_Bprime.py v0 SELFTEST PASS（11 項目・封印の後の試みだけを数える・期限で閉じる・錠が見る・一度だけ・つながり・暦の期限）
[transformers] PyTorch was not found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
close_behavior_Bprime.py v0.2 SELFTEST PASS（24 項目）
```

**RC-01 の再現**（`tools/` で走らせました。`_synthetic` → 下見を「止める」にした `FR` → `open_stopped`（runs は合成の六本）→ `meta['judge']=A['judge_record_sha16']` → `build` → `scan`）:
```
sweep: []
hits: [{'line': 5, 'layer': 'fixed', 'kind': 'fill_value', 'token': '[None]'}]
['- 正本 SHA16 0000000000000000・…・集計の出力 SHA16 3333333333333333・一致だけを見る段の記録 SHA16 None。']
```

**SHA の照らし**:
- 目録の 691 本すべてで、SHA-256 が計算した値と合いました（`ok 691 bad 0`。目録に無いのは目録そのものだけ）。
- `recheck/diff/INDEX.md` の変わった 32 本と足した 27 本の今の SHA16 も、すべて合いました。

変わった器の SHA-256 の頭 16 字（目録と一致）:
```
analyze 135CE9DFD55467E1・behavior 03D41C1C78947057・core A1C2285856A4DA08・external C12A4931B85B1CE4・gemma B89384C82C3F92CC・phases 1F6B77917BAA7C72
publish_map 64C5E490620F86BD・run 8A37DE1CA759A491・build_report 7BDD342108A04084・close_behavior 42018C96F163B735・boot DD601F674E1DD2C8
make_colab_dry_kit 4F4989CD825FDE38・dry_bprime C7202DF71D8FBDA4・dry_bprime_behavior E568A627F4292D12・dry_run B62E4A2645982E29・freeze C0B98FB501199189
g4_attempts 6BBE082971844B59・make_contrasts 5ED8172E147EFEC2・make_frozen 868DEA78E8CCD0A8・make_impl_bundle 9C917D647A9F17FD・publish F74C0978352962C3
send_external 465E0627A34DCA9C・sweep 876C6F9EE7054EB8・正本 5899C06207666C21・草案11 1C8CF84AA14A31B8
```

## 5. 読んでいない所・走らせていない所

**読んでいない所**:
- **正式の記録**: `dry-run-Bprime-2026-09-30.md/.json`・`freeze-path-dry-…`・provenance は読んでいません。確かめの行の当否は、記録の行ではなく確かめの器 v1.0 の中身で判断しました。記録を作ったのは v0.9 なので、Nk の印の行はまだ記録にありません。
- **閉じる器のやり直しの道**: `close_behavior_Bprime.py` の差分は読んでいません。依頼の 3 の項目のうち、この一つは見ていません。
- **ほかの器の差分**: `bprime_run`・`bprime_phases`・`bprime_behavior`・`bprime_external`・`send_external`・`publish_Bprime`・`bprime_publish_map`・`make_frozen`・`make_contrasts`・`make_colab_dry_kit`・`make_impl_bundle` の差分も読んでいません。
- **凍結の器の一部**: `freeze_Bprime` の `colab_check_eval`（U52）と `dry_record_check` は読んでいません。
- **そのほか**: 裁定 D272〜D277、publish-map の差分、草案10 から草案11 への差分（grep の他）も見ていません。

**走らせていない所**:
- torch の要る器（`dry_bprime`・`dry_bprime_behavior`・`dry_run_Bprime`・`boot_bprime` の DRY）は、実行の場に torch が無いので走らせていません。五も走らせていません。
- 別の個体の二つの器は、束の形では自己検査が走らないので走らせていません。
- 実の重みは読み込んでいません。外への呼び出しもしていません。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。