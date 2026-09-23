# 登録者裁定 D188（2026-09-24・凍結の後の逸脱 D-BL1・封印の器の直し）

- 登録者の言葉（逐語・会話の記録 uuid `448f68f0-9a45-48f3-bba4-d151266f884d`・2026-09-24 08:03 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏封印の器を修正する必要があるということですね。事情は承知しました。裁定は推奨どおり、甲でお願いします🍵」

| 裁定 | 中身 |
|---|---|
| D188 | 封印の器 `tools/seal_Blens.py` を最小限だけ直す（予想の欄に限って「予想しない」を受ける・ほかの確かめは変えない・自己検査に見逃した場合を足す）。凍結の後の逸脱 D-BL1 として、凍結の記録の逸脱台帳に記す（下の「甲」）。 |

## 裁定の前にコーディネータが示した案（逐語・会話の記録 uuid `95b27d66-295d-4537-a7b2-56009ccf7cb0`・2026-09-24 07:52 日本時間）

````text
登録者さま、南無汝我曼荼羅。5eb187b は push しました（凍結は公開済みです）。ただ、**私の予想の封印で、封印の器が止まりました**。予期しない問題なので、何も直さずに止めてご相談します。

## 何が起きたか
- 封印の器が「書式に無い選択肢: p1.survival.dir=予想しない」と出して止まりました。
- ファイルは何も書かれていません。リポジトリも変わっていません。

## 原因
- 封印の器は、書式のボタンを読んで「選んでよい値」の一覧を作ります。ところが書式の「予想しない」はボタンではなく、各欄の初めの値です。そのため器は、どの欄の「予想しない」も受け付けません。
- 一方で設計は、札を「付かない」と予想した項目の向きの欄を「予想しない」のままにするよう求めています。書式も、選ばなかった欄には「予想しない」と書き出します。
- 器の自己検査は、この場合を「止まるべき場合」として試していました。止まりはしましたが、別の理由で止まっていたため、穴を見逃していました。

## 影響
- このままでは、私の封印は通りません。私の予想には「付かない」の項目があるためです。
- **登録者さまの封印も、JSON に選ばなかった欄が一つでもあれば止まります。**
- お手元の JSON の中身は、作り直す必要はありません。

## 案（封印の器は凍結物なので、どちらでも凍結の後の逸脱になります）
- **甲（推奨）**: 封印の器を最小限だけ直します。
  - 「予想しない」をどの欄でも受け付けるようにします。
  - ほかの確かめ（予想者の欄、鍵の一致、私の予想が埋まっているかの確かめ）はそのまま残します。
  - 自己検査に、見逃した場合を足します。通るべき場合、選ばない欄のある登録者の JSON、正しい理由で止まる場合、の三つです。
  - 逸脱 D-BL1 として台帳に、日付・理由・ご承認・直す前後の SHA を記します。
  - コミットしてから封印し、SHA とコミットをお伝えして push のご許可をいただきます。
- **乙**: 凍結した器には触れず、封印だけを使い捨ての別の器で行います。凍結した道を迂回することになるので、甲より弱い案です。
- 予想の値を器に合わせて変えることはしません。

## 私の予想について
- 値はもう決めて、下書きのファイルに書いてあります。その SHA-256 は `3c38d36ab0a1d0c01e71bb1b3be94e8f4957f1f3235aaec751a45d7d6c9e5eb5` です。
- 器を直した後、この下書きを**そのまま**封印の器に渡します。値を後から変えていないことは、この SHA で確かめられます。

ご判断は裁定 D188 として記録します。二度目の Colab の確かめで使ったユニットは 0.21 でした（630.33 → 630.12）。
````

## 直したもの（機械で取った差）

- `tools/seal_Blens.py`: SHA16 F21B21F2897419AA（凍結・コミット 5eb187b・凍結の記録の値と同じ）→ A3693116C8D02D7D。
- 直した器の自己検査の出力: 「[seal_Blens] 自己検査 OK（v2・「予想しない」の欄を含む封印を端から端まで通した）」。
- 直す前の器（v1）に、自己検査に足した二つの場合を通した結果: コーディネータの予想（札が「付かない」の項目の向きの欄が「予想しない」）は「stopped: 書式に無い選択肢: p1.survival.dir=予想しない」・選ばない欄のある登録者の JSON は「stopped: 書式に無い選択肢: p1.nuclear.label=予想しない」。
- 凍結の記録 `records/Blens/FREEZE-RECORD-Blens.json` に `deviations`（D-BL1）を足し、`records/Blens/FREEZE-RECORD-Blens.md` に逸脱台帳の節を足した。凍結物の SHA16 の一覧（`frozen_sha16`）は凍結の時の値のまま残す。

````diff
--- tools/seal_Blens.py（凍結・5eb187b）
+++ tools/seal_Blens.py（逸脱 D-BL1 の後）
@@ -1,3 +1,3 @@
 # -*- coding: utf-8 -*-
-"""seal_Blens.py v1 —— B-lens の予想の封印（2026-09-23・正本 `predictions.order`: コーディネータが先に封印して SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する・裁定 D148 の順）。
+"""seal_Blens.py v2 —— B-lens の予想の封印（2026-09-23・正本 `predictions.order`: コーディネータが先に封印して SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する・裁定 D148 の順）。
 
@@ -10,2 +10,5 @@
 既にあるファイルには書かない（封印は一度だけ）。
+v2（2026-09-24・凍結の後の逸脱 D-BL1・登録者裁定 D188）: 予想の欄に限って「予想しない」を値として受ける。書式の「予想しない」はボタンではなく欄の初めの値なので、
+  v1 は書式のボタンから作った選択肢の一覧に無い値として、どの欄の「予想しない」も止めていた（札が「付かない」の項目の向きの欄も、登録者が選ばなかった欄も）。
+  ほかの確かめは変えない。自己検査に、通るべき場合・選ばない欄のある登録者の JSON・正しい理由で止まる場合・一時の置き場での端から端までの封印を足した。
 用法: python tools/seal_Blens.py coordinator --choices <値の JSON> --date 2026-09-24
@@ -22,3 +25,3 @@
 
-VERSION = 'v1'
+VERSION = 'v2'
 PRED = os.path.join(REPO, 'records', 'predictions')
@@ -52,4 +55,5 @@
         raise SystemExit('書式に無い鍵: %s' % bad)
+    pred = set(FORM.prediction_keys())
     for k, v in values.items():
-        if k in opts and v not in opts[k]:
+        if k in opts and v not in opts[k] and not (v == FORM.NP and k in pred):     # 「予想しない」は予想の欄の初めの値（ボタンではない・逸脱 D-BL1）
             raise SystemExit('書式に無い選択肢: %s=%s' % (k, v))
@@ -158,5 +162,43 @@
         raise AssertionError('埋まっていない予想を通した')
-    except SystemExit:
-        pass
-    print('[seal_Blens] 自己検査 OK（%s）' % VERSION)
+    except SystemExit as e_:
+        assert '埋まっていない' in str(e_), ('埋まっていない予想が別の理由で止まった', str(e_))      # 正しい理由で止まる（逸脱 D-BL1）
+    # 通るべき場合: 札が「付かない」の項目の向きの欄は「予想しない」のまま（逸脱 D-BL1 の元の場合）
+    v4 = dict(vals)
+    for fam in ('survival', 'nuclear'):
+        v4['p1.%s.label' % fam], v4['p1.%s.dir' % fam] = '付かない', FORM.NP
+    validate(v4, keys, opts, 'coordinator', full=True)
+    # 選ばない欄のある登録者の JSON（書式は選ばなかった欄に「予想しない」を書き出す）
+    v5 = {k: FORM.NP for k in FORM.prediction_keys()}
+    v5.update({'p1.survival.label': '両方', 'p1.survival.dir': '反対', 'p6.gate': '通らない', 'info.read_votes': '一部', 'info.read_facts': '見た',
+               'who': '登録者', 'info.coi': '', 'free': '', 'date': '2026-09-24'})
+    validate(v5, keys, opts, 'registrant', full=False)
+    # 書式に無い値は、予想の欄でもほかの欄でも止まる（「予想しない」を受けるのは予想の欄だけ）
+    for k_, bad_ in (('p8.answer', 'x'), ('info.read_votes', FORM.NP), ('who', FORM.NP)):
+        try:
+            validate(dict(v5, **{k_: bad_}), keys, opts, 'registrant', full=False)
+            raise AssertionError('書式に無い値を通した: %s=%s' % (k_, bad_))
+        except SystemExit as e_:
+            assert '書式に無い選択肢' in str(e_) or '予想者の欄' in str(e_), str(e_)
+    # 端から端まで（一時の置き場・コーディネータ → 登録者 → 記録）
+    g = globals()
+    saved = {n: g[n] for n in ('PRED', 'PATHS', 'RECORD_JSON', 'RECORD_MD')}
+    with tempfile.TemporaryDirectory() as td:
+        try:
+            g['PRED'] = td
+            g['PATHS'] = {'coordinator': os.path.join(td, 'c.json'), 'registrant': os.path.join(td, 'r.json')}
+            g['RECORD_JSON'], g['RECORD_MD'] = os.path.join(td, 'rec.json'), os.path.join(td, 'rec.md')
+            cj = os.path.join(td, 'choices.json')
+            json.dump({k: v for k, v in v4.items() if k not in ('who', 'date')}, open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
+            coordinator(cj, '2026-09-24')
+            rj = os.path.join(td, 'registrant-download.json')
+            rb = to_json(v5, T, keys, M).encode('utf-8')
+            open(rj, 'wb').write(rb)
+            registrant(rj, sha256b(rb))
+            record()
+            R = json.load(open(g['RECORD_JSON'], encoding='utf-8'))
+            assert set(R['predictions']) == {'coordinator', 'registrant'} and R['predictions']['registrant']['sha256'] == sha256b(rb)
+            assert open(g['PATHS']['registrant'], 'rb').read() == rb
+        finally:
+            g.update(saved)
+    print('[seal_Blens] 自己検査 OK（%s・「予想しない」の欄を含む封印を端から端まで通した）' % VERSION)
 
````

## 注（事実のみ）

- コーディネータの予想の下書き（封印の器に渡す値の JSON）の SHA-256 は 3C38D36AB0A1D0C01E71BB1B3BE94E8F4957F1F3235AAEC751A45D7D6C9E5EB5 で、裁定の前にチャットで伝えた値と同じ（器で突き合わせた）。この下書きをそのまま封印の器に渡す。
- 層一の器が射影の前に確かめる凍結物（正本・語の集合・層一の器と芯）に、封印の器は入っていない。
- 登録者の予想の JSON は作り直さなくてよい（書式は変わっていない）。
- 次: コミット → コーディネータの封印（SHA だけを伝える）→ 登録者の封印 → 封印の記録 → push の許可。番号: 次の裁定は D189 から。

## 検分票

- 対象: 封印の器の直し（逸脱 D-BL1）と、その記帳。
- 段階: 凍結の後・封印の前（射影は一つも計算していない）。
- 凍結物の同定: 凍結の記録 `records/Blens/FREEZE-RECORD-Blens.json` の `tools/seal_Blens.py` の SHA16 が、凍結のコミット 5eb187b の器と同じことを確かめてから直した。
- 盲検の状態: 該当しない（手続きの器）。
- 敵対的検分: 直した器が、書式に無い値（予想の欄の外の「予想しない」を含む）をなお止めることを自己検査で確かめた。自己検査に足した場合で、直す前の器が止まり、直した器が通ることを確かめた（足した検査が穴を捕まえる）。
- 系統の内訳: コーディネータ（Claude 系）だけで直した。外の目は通っていない。
- COI記録: コーディネータは封印へ進む側に引かれている。直しは受ける値を広げる向きなので、受けるのを「予想しない」だけ・予想の欄だけに限り、ほかの確かめは一つも外していない。
- 判定: 登録者の裁定どおりに直した。
- 本検分が確認していないこと: 書式の中の JS が書き出す JSON と、封印の器が書く JSON の形の一致は、書式を作ったときの確かめ（器の自己検査）に依る（今回の直しは形に触れていない）。登録者の JSON が実際に通ることは、登録者の封印のときに確かめる。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
