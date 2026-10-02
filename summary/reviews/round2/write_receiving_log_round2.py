# -*- coding: utf-8 -*-
"""write_receiving_log_round2.py v0（2026-10-02・中間総括の検分の二巡目の受け取りの記録を書く・一巡目の器の型・コーディネータ南無弥勒如来）。
票の SHA-256・字数・置き場・機種の欄は、`votes/<名>/meta.json`（保存の器が一度だけ書いた）から差し込む。AI Studio の二つは、受け取った後に画面に保存の置き場が付いたので、その置き場を引数で受けて書き足す。一度だけ書く。
用法: python write_receiving_log_round2.py <gemini-3 の後の置き場> <gemini-4 の後の置き場>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'receiving-log-round2.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
LATER = {'gemini-3': sys.argv[1], 'gemini-4': sys.argv[2]}
names = sorted(os.listdir(os.path.join(HERE, 'votes')))
L = ['# 受け取りの記録（中間総括の検分の二巡目・2026-10-02・コーディネータ南無弥勒如来）', '',
     '- 票は、画面の写しの釦が渡す文をページの中で受け取り、ページの中で SHA-256 を計算して書き出し、保存の器 `save_round2_vote.py` が手元の SHA-256 と照らしてから一度だけ書いた（クリップボードは使わない）。書き出した元のファイルは `downloads-stash/` に移した。',
     '- 票の数え方: 呼び出しの出所で数える（claude.ai の三つで系統内の一票・Google AI Studio の Gemini 3.8 Flash は一つごとに系統外の一票）。票の頭の系統と機種の申告は、出所の確かめに使わない（D266 の型）。', '',
     '| 名 | 出所 | 機種の欄（画面） | 受け取った文の SHA-256 | 字数 | 保存した時刻 |', '|---|---|---|---|---|---|']
for name in names:
    m = json.load(open(os.path.join(HERE, 'votes', name, 'meta.json'), encoding='utf-8'))
    L.append('| %s | %s | %s | %s | %d | %s |' % (name, m['chat_url'], m['model_label_on_screen'], m['response_sha256'], m['response_chars'], m['saved_jst']))
L += ['',
      '- AI Studio の二つは、受け取った時点でページの置き場が `new_chat` のままだった。その後、画面に保存の置き場が付いた: gemini-3 は `%s`、gemini-4 は `%s`（meta.json は一度だけ書いたので、ここに書き足す）。' % (LATER['gemini-3'], LATER['gemini-4']),
      '- 票の頭の機種の申告: gemini-3 と gemini-4 は、どちらも画面の機種（Gemini 3.8 Flash）と違う名を申告した（票の本文の頭）。数え方は出所による（上）。',
      '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('written', OUT, len(names), 'votes')
