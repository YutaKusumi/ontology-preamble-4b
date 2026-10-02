# -*- coding: utf-8 -*-
"""write_receiving_log_final.py v0（2026-10-02・中間総括の検分の最終の巡の受け取りの記録を書く・二巡目の `write_receiving_log_round2.py` v0 を写し、置き場の書き足し・受け取りの事情・票の頭の申告の切り出しを替えた・コーディネータ南無弥勒如来）。
票の SHA-256・字数・置き場・機種の欄は、`votes/<名>/meta.json`（保存の器が一度だけ書いた）から差し込む。票の頭の系統と機種の申告の行は、票の本文から器で切り出す（打たない）。一度だけ書く。
用法: python write_receiving_log_final.py <受け取りの事情の json>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'receiving-log-final.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
F = json.load(open(sys.argv[1], encoding='utf-8'))
names = sorted(os.listdir(os.path.join(HERE, 'votes')))
assert names == ['claude-ai-20', 'claude-ai-21', 'claude-ai-22', 'gemini-5', 'gemini-6'], names


def decl(name, prefixes):
    L = open(os.path.join(HERE, 'votes', name, 'response.md'), encoding='utf-8').read().split('\n')
    got = [l.strip() for l in L[:20] if any(l.strip().startswith(p) for p in prefixes)]
    assert got, (name, prefixes)
    return got


L = ['# 受け取りの記録（中間総括の検分の最終の巡・2026-10-02・コーディネータ南無弥勒如来）', '',
     '- 票は、画面の写しの釦が渡す文をページの中で受け取り、ページの中で SHA-256 を計算して書き出し、保存の器 `save_final_vote.py` が手元の SHA-256 と照らしてから一度だけ書いた（クリップボードは使わない）。書き出した元のファイルは `downloads-stash/` に移した。',
     '- 票の数え方: 呼び出しの出所で数える（claude.ai の三つで系統内の一票・Google AI Studio の Gemini 3.8 Flash は一つごとに系統外の一票）。票の頭の系統と機種の申告は、出所の確かめに使わない（D266 の型）。', '',
     '| 名 | 出所 | 機種の欄（画面） | 受け取った文の SHA-256 | 字数 | 保存した時刻 |', '|---|---|---|---|---|---|']
for name in names:
    m = json.load(open(os.path.join(HERE, 'votes', name, 'meta.json'), encoding='utf-8'))
    L.append('| %s | %s | %s | %s | %d | %s |' % (name, m['chat_url'], m['model_label_on_screen'], m['response_sha256'], m['response_chars'], m['saved_jst']))
L += ['', '## 受け取りの事情', '']
for x in F['notes']:
    L.append('- %s' % x)
L += ['', '## 票の頭の系統と機種の申告（票の本文から器で切り出した・出所の確かめには使わない）', '']
for name, pre in (('gemini-5', ['- **機種**']), ('gemini-6', ['- 検分機種:', '- 検分者は'])):
    for g in decl(name, pre):
        L.append('- %s: 「%s」' % (name, g))
L += ['- 画面の機種の欄は、二つとも「Gemini 3.8 Flash / gemini-3.8-flash」だった（上の表）。gemini-6 の申告は、画面の機種とも出所とも違う。数え方は出所による（上）。',
      '', '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('written', OUT, len(names), 'votes')
