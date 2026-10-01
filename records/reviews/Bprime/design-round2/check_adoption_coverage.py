# -*- coding: utf-8 -*-
"""check_adoption_coverage.py v0（2026-09-29・B′ の設計の巡・二巡目・採否の表の数え・コーディネータ南無弥勒如来）。
採否の表 `adoption-design-round2.md` の表の行（S01〜）に、四票の指摘（G2-1〜17・A4-1〜21・A5-1〜22・A6-1〜24）がすべて入っているかを数え、各票の「重さ」の数を票のファイルから数える。欄は「 | 」で割る（一巡目の対応の器の v0 の失敗から）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(HERE, 'adoption-design-round2.md'), encoding='utf-8').read()
rows = [l for l in T.split(chr(10)) if re.match(r'^\| S\d\d \|', l)]
found = {}
for l in rows:
    cells = [c.strip() for c in l.strip().strip('|').split(' | ')]
    assert len(cells) == 6, (cells[0], len(cells))
    for m in re.finditer(r'\b(G2-\d+|A[456]-\d+)\b', cells[2]):
        found.setdefault(m.group(1), []).append(cells[0])
expect = ['G2-%d' % i for i in range(1, 18)] + ['A4-%d' % i for i in range(1, 22)] + ['A5-%d' % i for i in range(1, 23)] + ['A6-%d' % i for i in range(1, 25)]
missing = [e for e in expect if e not in found]
extra = [k for k in found if k not in expect]
print('rows', len(rows), '| expected', len(expect), '| found', len(set(found) & set(expect)), '| missing', missing, '| extra', extra)
for name in ('grok-4.7', 'claude-ai-4', 'claude-ai-5', 'claude-ai-6'):
    s = open(os.path.join(HERE, 'votes', name, 'response.md'), encoding='utf-8').read()
    print(name, '重大', len(re.findall(r'重さ[:：]\s*重大', s)), '中', len(re.findall(r'重さ[:：]\s*中', s)), '軽微', len(re.findall(r'重さ[:：]\s*軽微', s)))
