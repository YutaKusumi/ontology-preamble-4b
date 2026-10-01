# -*- coding: utf-8 -*-
"""check_table_pipes.py v0（2026-09-29・B′ の設計の巡・三巡目・表の縦棒の確かめ・層三の教訓 §0-48「表の縦棒と注の口」の型・コーディネータ南無弥勒如来）。
Markdown の表の各行の縦棒（逆斜線で逃がしていないもの）の数が、その表の見出しの行と同じかを確かめ、違う行を並べる。
使い方: python check_table_pipes.py <ファイル> [<ファイル> ...]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BS = chr(92)


def pipes(line):
    n, prev = 0, ''
    for ch in line:
        if ch == '|' and prev != BS:
            n += 1
        prev = ch
    return n


bad = 0
for p in sys.argv[1:]:
    L = open(p, encoding='utf-8').read().split(chr(10))
    head = None
    for i, l in enumerate(L, 1):
        if not l.startswith('|'):
            head = None
            continue
        if head is None:
            head = pipes(l)
            continue
        if pipes(l) != head:
            bad += 1
            print('%s:%d pipes %d expected %d | %s' % (p, i, pipes(l), head, l[:70]))
print('rows with wrong pipe count:', bad)
