# -*- coding: utf-8 -*-
"""check_adoption_coverage.py v0（2026-09-29・B′ の設計の巡・三巡目〔最終の検分〕・採否の表の数えと引用の確かめ・二巡目の器の型・コーディネータ南無弥勒如来）。
(1) 採否の表 `adoption-design-round3.md` の表の行（T01〜）に、四票の指摘（G3-1〜17・A7-1〜18・A8-1〜15・A9-1〜20）がすべて入っているかを数え、各票の「重さ」の数を票のファイルから数える。欄は「 | 」で割る。
(2) 表のファイルの中の「」の引用（外側の組）が、出所の候補（草案6・束・事実の記録・票と追い問いの答え・枠と裁定）のどれかに一字違わずあるかを確かめ、無いものを並べる（見出しの名や語の引きもあるので、無いものは人が読む）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.normpath(os.path.join(HERE, '..', '..'))
NL = chr(10)
LQ, RQ = chr(0x300C), chr(0x300D)
T = open(os.path.join(HERE, 'adoption-design-round3.md'), encoding='utf-8').read()
rows = [l for l in T.split(NL) if re.match(r'^\| T\d\d \|', l)]
found = {}
for l in rows:
    cells = [c.strip() for c in l.strip().strip('|').split(' | ')]
    assert len(cells) == 6, (cells[0], len(cells))
    for m in re.finditer(r'(G3-\d+|A[789]-\d+)', cells[2]):
        found.setdefault(m.group(1), []).append(cells[0])
expect = ['G3-%d' % i for i in range(1, 18)] + ['A7-%d' % i for i in range(1, 19)] + ['A8-%d' % i for i in range(1, 16)] + ['A9-%d' % i for i in range(1, 21)]
missing = [e for e in expect if e not in found]
extra = sorted(k for k in found if k not in expect)
print('rows', len(rows), '| expected', len(expect), '| found', len(set(found) & set(expect)), '| missing', missing, '| extra', extra)
for name in ('grok-4.7', 'claude-ai-7', 'claude-ai-8', 'claude-ai-9'):
    s = open(os.path.join(HERE, 'votes', name, 'response.md'), encoding='utf-8').read()
    print(name, '重大', len(re.findall(r'重さ[:：]\s*重大', s)), '中', len(re.findall(r'重さ[:：]\s*中', s)), '軽微', len(re.findall(r'重さ[:：]\s*軽微', s)))

srcs = [os.path.join(BP, 'design', 'design-Bprime-draft6.md'), os.path.join(BP, 'design', 'design-Bprime-draft7.md'), os.path.join(HERE, 'facts-round3.md'), os.path.join(HERE, 'facts-round2.md'),
        os.path.join(HERE, 'round2-verdicts-extract.md'), os.path.join(HERE, 'event-2026-09-29-grok-self-report.md'), os.path.join(BP, 'rulings-D266.md')]
srcs += glob.glob(os.path.join(HERE, 'kit', '**', '*.*'), recursive=True)
srcs += glob.glob(os.path.join(HERE, 'votes', '*', 'response.md'))
corpus = []
for p in srcs:
    try:
        corpus.append(open(p, encoding='utf-8').read())
    except Exception:
        pass
out, depth, start = [], 0, None
for i, ch in enumerate(T):
    if ch == LQ:
        if depth == 0:
            start = i + 1
        depth += 1
    elif ch == RQ and depth > 0:
        depth -= 1
        if depth == 0:
            out.append(T[start:i])
nf = [q for q in out if not any(q in c for c in corpus)]
print('quotes', len(out), '| not found anywhere', len(nf))
for q in nf:
    print('  NF:', q[:120])
