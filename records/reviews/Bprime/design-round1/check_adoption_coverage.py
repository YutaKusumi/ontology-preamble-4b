# -*- coding: utf-8 -*-
"""check_adoption_coverage.py v0（2026-09-29・B′ の設計の巡・一巡目・採否の表の数え・コーディネータ南無弥勒如来）。
採否の表 `adoption-design-round1.md` の表の行に、四票の指摘（G-F1〜17・A1-1〜24・A2-1〜32・A3-1〜31）がすべて入っているかを数える。
あわせて、各票の「重さ: 重大」の数を票のファイルから数え、表の「枠の予想と結果」の数と並べる。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(HERE, 'adoption-design-round1.md'), encoding='utf-8').read()
rows = [l for l in T.split(chr(10)) if re.match(r'^\| R\d\d \|', l)]
found = {}
for l in rows:
    cell = l.split('|')[3]
    for m in re.finditer(r'\b(G-F\d+|A[123]-\d+)\b', cell):
        found.setdefault(m.group(1), []).append(l.split('|')[1].strip())
expect = ['G-F%d' % i for i in range(1, 18)] + ['A1-%d' % i for i in range(1, 25)] + ['A2-%d' % i for i in range(1, 33)] + ['A3-%d' % i for i in range(1, 32)]
missing = [e for e in expect if e not in found]
extra = [k for k in found if k not in expect]
print('rows', len(rows), '| expected', len(expect), '| found', len(set(found) & set(expect)), '| missing', missing, '| extra', extra)
multi = {k: v for k, v in found.items() if len(v) > 1}
print('in more than one row:', len(multi), sorted(multi.items(), key=lambda kv: kv[0]))
for name in ('grok-4.7', 'claude-ai-1', 'claude-ai-2', 'claude-ai-3'):
    s = open(os.path.join(HERE, 'votes', name, 'response.md'), encoding='utf-8').read()
    print(name, '重大', len(re.findall(r'重さ[:：]\s*重大', s)), '中', len(re.findall(r'重さ[:：]\s*中', s)), '軽微', len(re.findall(r'重さ[:：]\s*軽微', s)))
