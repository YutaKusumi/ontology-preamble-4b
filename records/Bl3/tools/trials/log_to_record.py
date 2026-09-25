# -*- coding: utf-8 -*-
"""合成データの器の走りの印字（確かめの行）から、試しの記録を機械で組む（記録を書く前に器が止まった試しのため）。確かめの行は一字も変えずに表にし、
印字の終わりの数行（止まった所）を並べる。手元の置き場の道筋は決まった言い方に置き換える。既にある記録には書かない。
用法: python records/Bl3/tools/trials/log_to_record.py <走りの印字> <記録の置き場> <試しの名> <注の一行>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
log, out, name, note = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert not os.path.exists(out), '既にある: ' + out
NL = chr(10)
raw = open(log, encoding='utf-8', errors='replace').read()
home = os.path.expanduser('~')
for x in sorted({REPO, REPO.replace('\\', '/'), home, home.replace('\\', '/')}, key=len, reverse=True):
    raw = raw.replace(x, '〈リポジトリ〉' if x.startswith(REPO[:len(REPO)]) and 'GitHub' in x else '〈手元の置き場〉')
lines = raw.split(NL)
rows = []
for l in lines:
    m = re.match(r'^\[dry_run_Bl3\] (\S+) (OK|FAIL)\s+(.*)$', l)
    if m:
        rows.append((m.group(1), m.group(2), m.group(3)))
tail = [l for l in lines if l.strip()][-6:]
n_ok = sum(1 for r in rows if r[1] == 'OK')
L = ['# %s（機械生成・`records/Bl3/tools/trials/log_to_record.py`・走りの印字から切り出した）' % name, '',
     '- 注: %s' % note,
     '- 走りの印字の SHA-256（手元の置き場の道筋を置き換える前）: %s' % hashlib.sha256(open(log, 'rb').read()).hexdigest().upper(),
     '- 確かめの行: %d のうち %d が期待どおり（印字の行をそのまま並べた・部と結果の札のほかは一字も変えていない）。' % (len(rows), n_ok), '',
     '| 部 | 結果 | 確かめと詳しく（印字のまま） |', '|---|---|---|'] + ['| %s | %s | %s |' % (g, '期待どおり' if r == 'OK' else '**期待と違う**', t.replace('|', '｜')) for g, r, t in rows] + [
     '', '## 印字の終わり（止まった所・手元の置き場の道筋は置き換えた）', '', '```text'] + tail + ['```', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('[log_to_record] wrote %s（確かめ %d・期待どおり %d）' % (os.path.relpath(out, REPO), len(rows), n_ok))
