# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の下見の走りの記録（Colab・相 pilot）を書く。数・時刻・SHA は、写した下見の出力（session・下見の記録）と、落とした zip と、
会話の記録の道具の結果（コーディネータが Colab の画面の文を機械で読んだユニットの読み）から、機械で切り出す（手で打たない）。既にある記録には書かない。
用法: python records/Bl3/pilot/pilot_run_record_Bl3.py <会話の記録 jsonl> <落とした zip>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
NL = chr(10)
OUT = os.path.join(HERE, 'pilot-run-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
ZP = sys.argv[2]
zname = os.path.basename(ZP)
DIR = os.path.join(HERE, zname[:-4])
S = json.load(open(os.path.join(DIR, 'session.json'), encoding='utf-8'))
P = json.load(open(os.path.join(DIR, 'pilot.json'), encoding='utf-8'))['pilot']
FR = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json'), encoding='utf-8'))
zb = open(ZP, 'rb').read()
zsha = hashlib.sha256(zb).hexdigest().upper()
Z = zipfile.ZipFile(ZP)
entries = [(i.filename, i.file_size) for i in Z.infolist()]
same = all(Z.read(n) == open(os.path.join(HERE, *n.split('/')), 'rb').read() for n, _ in entries)
assert same, '写した出力が zip の中身と違う'
t0 = S['log'][0]['at']
t1 = S['finished']
# ユニットの読み（道具の結果の {at, found}）
reads = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and isinstance(c, list):
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'tool_result':
                cc = x.get('content')
                txt = cc if isinstance(cc, str) else ''.join(y.get('text', '') for y in (cc or []) if isinstance(y, dict))
                if '利用可能なコンピューティング ユニット数' in txt and '"at"' in txt:
                    try:
                        j = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
                    except Exception:
                        continue
                    u = [f for f in j.get('found') or [] if f.startswith('利用可能なコンピューティング ユニット数')]
                    if u:
                        reads.append((j['at'], u[0], [f for f in j['found'] if not f.startswith('利用可能')]))
pre = [r for r in reads if r[0] < t0]
post = [r for r in reads if r[0] > t1]
assert pre and post, ('ユニットの読みが走りの前後に無い', len(pre), len(post))
b4, af = max(pre), min(post)
dec = P['decision']
fc = S['frozen_check']
R = ['# B-lens 層三の下見の走りの記録（Colab の相 pilot・機械生成・`pilot_run_record_Bl3.py`）', '',
     '- 走り: GPU %s・コミット %s・起動器 %s・始め %s・終わり %s（協定世界時・session の記録）・%s 秒。版: %s。' % (
         S['gpu'], S['commit'], S['boot'], t0, t1, S['seconds'], '・'.join('%s %s' % kv for kv in S['versions'].items())),
     '- 手順: 相 check と同じノートブックに、相 pilot の一行（コミット固定）を置いて走らせた。最初の走りは版を入れ直して止まり（transformers）、セッションを再起動して同じ一行を走らせ直した。'
     'HF_TOKEN の画面はキャンセルした（公開の重み・資格情報は使わない）。前の相 check のセル（相 check の一行と出力）はノートブックに残し、走らせていない。',
     '- 打ち直し: 最初に打った一行は、フォーカスがセルのエディタに入る前に打ち始めたため、頭の字が落ちた形で、新しくできたセルに入った。走らせる前に、エディタの中身を期待の一行と字ごとに照らす確かめで見つけ、'
     'エディタにフォーカスがあることを確かめてから打ち直し、期待の一行とちょうど同じになったことを確かめてから走らせた。壊れた一行は走らせていない。',
     '- 凍結の照らし（session）: 照らした凍結物 %d・取り出しの外で飛ばした %d（%s）・外れ %d。封印した二つの予想の SHA-256 は、起動器が封印の記録と照らした（外れれば止まる）。' % (
         fc['checked'], len(fc['skipped']), '・'.join('`%s`' % x for x in fc['skipped']), len(fc['bad'])),
     '- 重み・方向・正本: 重みの SHA-256 %d 件・方向の npz の SHA-256 の頭 %s・正本の SHA16 %s（session の記録）。' % (len(S['weights_sha256']), S['directions_npz_sha256'][:16], S['canon_sha16']),
     '- 機械の決定（下見の記録）: q1「%s」・主の升目 %d のうち (i)(ii) を満たす升目 %d・外した升目 %s・バッチの大きさ %s・揺れの床 %s・近道の許容 %s・順伝播の数 %s。' % (
         dec['q1'], dec['n_main'], dec['n_pass'], '・'.join(dec['dropped']), P['batch'], P['floor'], P['cache_tol'], P['n_forward']),
     '- 出力の zip: `%s`（%d バイト・SHA-256 %s）。起動器が印字した zip の SHA-256 の末尾と、画面で目で照らして一致した（機械の照らしではない）。中身: %s。この置き場の `%s/` に写した（zip の中身とバイトで同じ）。' % (
         zname, len(zb), zsha, '・'.join('%s（%d バイト）' % (n.split('/')[-1], s) for n, s in entries), zname[:-4]),
     '- ユニット（コーディネータが Colab の画面の文を機械で読んだ道具の出力）: 走りの前「%s」（%s）・走りの後「%s」（%s・%s）。' % (b4[1], b4[0], af[1], af[0], '・'.join(af[2])),
     '- ランタイムは、zip を落として照らした後に、接続を解除して削除した。',
     '- 本の凍結: %s（日本時間・凍結の記録の `main_freeze`・登録者の言葉は `records/Bl3/main-freeze-words-Bl3.md`）。下見の試みは %d。' % (FR['main_freeze']['frozen_jst'], len(FR['main_freeze']['pilot_attempts'])), '',
     '## 検分票', '',
     '- 対象: Colab の相 pilot の走り（L4）と、その出力。',
     '- 段階: 下見の手順と止める条件と機械の決定の規則は、下見の前の凍結で先に凍結した（事前）。この走りの記録は事後。',
     '- 凍結物の同定: 下見の前の凍結の記録（凍結物 %d 件）・下見のコミット %s・session の凍結の照らし。' % (len(FR['frozen_sha16']), S['commit'][:7]),
     '- 盲検の状態: 該当しない（無操作だけで、方向を足した効き目は計算していない）。',
     '- 敵対的検分: zip の SHA-256 と中身・session の版と GPU と重みと方向と正本を照らした。打った一行を走らせる前に字ごとに照らし、打ち損じを見つけて直した。本の凍結の確かめは、記帳の前に書かずに照らした（外れ無し）。',
     '- 系統の内訳: コーディネータ（Claude 系）一名。',
     '- COI記録: 下見が通る側に引かれる。機械の決定（凍結した規則）をそのまま採り、升目の外し方に手を入れていない。',
     '- 判定: 下見の記録として確定（機械の決定は凍結した規則のとおり）。',
     '- 本検分が確認していないこと: 下見の値を別の環境（別の GPU や版）で再現していない。zip の SHA-256 の末尾の照らしは画面での目の照らし。最初の走り（版の入れ直し）の出力の置き場はランタイムとともに消え、落としていない。'
     'バッチの大きさや近道で無操作の値が動いた理由は調べていない。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
text = NL.join(R)
for bad in ('Users', 'AppData', 'Downloads'):
    assert bad not in text, '手元の道筋が入る'
open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
print('wrote', os.path.basename(OUT), '| units before', b4[0], b4[1], '| after', af[0], af[1], '| zip', zname, len(zb))
