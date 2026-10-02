# -*- coding: utf-8 -*-
"""write_sending_log_final.py v0（2026-10-02・中間総括の検分の最終の巡の送りの記録を書く・二巡目の `write_sending_log_round2.py` v0 を写し、裁定・刻印・添えたもの・二つ目のタブの件・Gemini の送りの順の書き方を替えた・コーディネータ南無弥勒如来）。
登録者の裁定は `../round2/rulings-D288.md` を指す（逐語は裁定の記録にある）。添えたファイルと欄の一文の SHA-256 は器で計算する。URL と時刻は、ページの中で走らせた式が返した値を写した。一度だけ書く。
用法: python write_sending_log_final.py <送りの事実の json>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'sending-log-final.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
sha = lambda f: hashlib.sha256(open(os.path.join(HERE, f), 'rb').read()).hexdigest().upper()
F = json.load(open(sys.argv[1], encoding='utf-8'))
REQ, BUN, LINE = sha('request-final.md'), sha('bundle-final-all-in-one.md'), sha('chat-line-final.txt')
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
L = ['# 送りの記録（中間総括の検分の最終の巡・2026-10-02・コーディネータ南無弥勒如来）', '',
     '- 登録者の裁定: D288-i（最終の検分も、これまでどおり claude.ai の三名と Gemini の二名に丁寧に依頼する・`../round2/rulings-D288.md`）。巡の上限: これが最後の巡（枠の追記二 §5）。',
     '- 送る前に刻印した: `frame-stamp-final.txt`（枠の追記二〔最終の巡の予想 §6〕・裁定 D288・草案3 と照らしの記録・草案3 の器・計算の器 v0.3 と出力・束の器・依頼文・束・索引・欄の一文・票の保存の器・器の記録）。',
     '- 添えたもの（五つとも同じ）: 依頼文 `request-final.md`（SHA-256 %s）・束 `bundle-final-all-in-one.md`（SHA-256 %s）。' % (REQ, BUN),
     '- 欄の一文（`chat-line-final.txt`・SHA-256 %s）: 五つとも、ページの中で差し込み、欄の中身の SHA-256 がファイルと同じことをページの中で確かめてから送った。' % LINE,
     '- 操作: 登録者の Chrome をコーディネータが操作した（新しいタブで新しいチャットを開いた）。確かめはページの中で走らせた式で行った。', '',
     '## claude.ai（系統内・三つで一票・新しい個体）', '',
     '- 機種の欄は、三つとも、送りの式の中（送りの釦を押す直前）で、画面の要素の名が「モデル: Opus 5.5 超高」だった。添付の札が二つとも欄に出たことを確かめた。送った後、送った発話の本文の SHA-256 が欄の一文のファイルと同じこと、利用者の発話が一つであること、停止の釦が出たことを確かめた。']
for c in F['claude']:
    L.append('- **%s**: `%s`（送りの釦を押した直後のページの時計 %s）。' % (c['name'], c['url'], c['t']))
L.append('- %s' % F['claude_note'])
L += ['', '## Google AI Studio（系統外・二票・新しい個体）', '',
      '- 機種の欄（画面の文）: 「Gemini 3.8 Flash / gemini-3.8-flash」。Run settings は既定のまま（Thinking level は Medium）。API の鍵は選んでいない。',
      '- 枠の追記二 §5 のとおり、Gemini の二つ目は、一つ目の返事を受け取って保存してから送った。']
for g in F['gemini']:
    L.append('- **%s**: 新しいチャットにファイルを添え、二つの札が %s になったことを確かめてから、一文を入れて Run を押した（押して数秒後のページの時計 %s）。%s' % (
        g['name'], g['tokens'], g['t'], g.get('note', '')))
L += ['', '- この記録を書いた時刻: %s（日本時間）。' % now, '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('written', OUT)
