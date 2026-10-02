# -*- coding: utf-8 -*-
"""write_sending_log_round2.py v0（2026-10-02・中間総括の検分の二巡目の送りの記録を書く・一巡目の器の型・コーディネータ南無弥勒如来）。
登録者の裁定は `../round1/rulings-D287.md` を指す（逐語は裁定の記録にある）。添えたファイルと欄の一文の SHA-256 は器で計算する。URL と時刻は、ページの中で走らせた式が返した値を写した。一度だけ書く。
用法: python write_sending_log_round2.py <送りの事実の json>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sending-log-round2.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
sha = lambda f: hashlib.sha256(open(os.path.join(HERE, f), 'rb').read()).hexdigest().upper()
F = json.load(open(sys.argv[1], encoding='utf-8'))
REQ, BUN, LINE = sha('request-round2.md'), sha('bundle-round2-all-in-one.md'), sha('chat-line-round2.txt')
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
L = ['# 送りの記録（中間総括の検分の二巡目・2026-10-02・コーディネータ南無弥勒如来）', '',
     '- 登録者の裁定: D287-d（二巡目を置く・claude.ai の新しいチャット三つと Gemini 3.8 Flash の新しいチャット二つ・`../round1/rulings-D287.md`）。',
     '- 送る前に刻印した: `frame-stamp-round2.txt`（枠の追記一〔二巡目の予想 §7〕・裁定 D287・草案2 と照らしの記録・草案2 の器・計算の器 v0.2 と出力・束の器・依頼文・束・索引・欄の一文・票の保存の器・器の記録）。',
     '- 添えたもの（五つとも同じ）: 依頼文 `request-round2.md`（SHA-256 %s）・束 `bundle-round2-all-in-one.md`（SHA-256 %s）。' % (REQ, BUN),
     '- 欄の一文（`chat-line-round2.txt`・SHA-256 %s）: 五つとも、ページの中で差し込み、欄の中身の SHA-256 がファイルと同じことをページの中で確かめてから送った。' % LINE,
     '- 操作: 登録者の Chrome をコーディネータが操作した（新しいタブで新しいチャットを開いた）。確かめはページの中で走らせた式で行った。', '',
     '## claude.ai（系統内・三つで一票・新しい個体）', '',
     '- 機種の欄は、三つとも、新しいチャットを開いた時と送る直前に、画面の要素の名で「モデル: Opus 5.5 超高」だった。添付の札が二つとも欄に出たことを確かめた。送った後、送った発話の本文の SHA-256 が欄の一文のファイルと同じこと、停止の釦が出たことを確かめた。']
for c in F['claude']:
    L.append('- **%s**: `%s`（送りの釦を押した直後のページの時計 %s）。' % (c['name'], c['url'], c['t']))
L += ['', '## Google AI Studio（系統外・二票・新しい個体）', '',
      '- 機種の欄（画面の文）: 「Gemini 3.8 Flash / gemini-3.8-flash」。Run settings は既定のまま（Thinking level は Medium）。API の鍵は選んでいない。',
      '- 一巡目の二つ目で画面の誤りが出たので、二巡目は一つ目の返事が出そろってから二つ目を送った（起草者の段取り・登録者の裁定の範囲の内）。']
for g in F['gemini']:
    L.append('- **%s**: 新しいチャットにファイルを添え、二つの札が %s になったことを確かめてから、一文を入れて Run を押した（押して数秒後のページの時計 %s）。走った後に AI Studio がつけた置き場: `%s`。%s' % (
        g['name'], g['tokens'], g['t'], g['url'], g.get('note', '')))
L += ['', '- この記録を書いた時刻: %s（日本時間）。' % now, '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('written', OUT)
