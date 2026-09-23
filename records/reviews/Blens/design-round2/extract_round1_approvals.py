# -*- coding: utf-8 -*-
"""設計の巡・第一巡の四票から、是認と総括（総合の判定・草案1 の §13 の六件への意見・【確認】の行）を逐語で切り出す（裁定 D178 の注）。
採用済みの手順の「合も次の巡に渡す」に当たる。切り出しは器が行い、手で打たない。行の番号は票のファイルの行。
用法: python records/reviews/Blens/design-round2/extract_round1_approvals.py"""
import os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.join(HERE, '..', 'design-round1')
NL = chr(10)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
VOTES = [  # (名, 札, 総合の判定の行の型, §13 の節の始まり, 終わり)
    ('gemini-1', 'G1', [r'^\*\*判定', r'^- \*\*判定\*\*'], r'^### 10\. 草案 §13', r'^### 11\.'),
    ('gemini-2', 'G2', [r'^### 総合判定', r'^- \*\*判定\*\*'], r'^#### 10\. 草案 §13', r'^#### 11\.'),
    ('claude-ai-1', 'C1', [r'^問十一　総合'], r'^問十　§13', r'^問十一'),
    ('claude-ai-2', 'C2', [r'^総合の判定'], r'^### 問10 §13', r'^### 問11'),
]
out = ['# 設計の巡・第一巡の四票の是認と総括の抜き書き（逐語・器 `records/reviews/Blens/design-round2/extract_round1_approvals.py`・2026-09-23）', '',
       '- 採用済みの手順の「合も次の巡に渡す」に当たる（裁定 D178 の注）。四票の判定の行（総合と問いごと）・草案1 の §13 の六件への意見・【確認】の行を、票のファイルから器で切り出した。行の頭の数は票のファイルの行の番号。',
       '- 切り出しは是認だけでなく、条件つきの意見と反対もそのまま含む（§13 の六件への意見は、賛成と条件と反対を一続きに書いているため）。', '']
total = 0
for name, tag, verdict_pats, s_pat, e_pat in VOTES:
    p = os.path.join(R1, name, 'review.md')
    L = open(p, encoding='utf-8').read().split(NL)
    out += ['## %s（%s・`records/reviews/Blens/design-round1/%s/review.md`・SHA16 %s）' % (tag, name, name, s16(p)), '', '**判定の行（総合と問いごと）**:', '']
    v = [(i + 1, l) for i, l in enumerate(L) if any(re.search(q, l) for q in verdict_pats)]
    assert v, (name, '総合の判定の行が無い')
    out += ['- %d: %s' % (i, l.strip()) for i, l in v]
    si = [i for i, l in enumerate(L) if re.search(s_pat, l)]
    assert len(si) == 1, (name, '§13 の節の始まり', si)
    ei = [i for i, l in enumerate(L) if i > si[0] and re.search(e_pat, l)]
    assert ei, (name, '§13 の節の終わり')
    sec = [(i + 1, L[i]) for i in range(si[0], ei[0]) if L[i].strip()]
    out += ['', '**草案1 の §13 の六件への意見**（%d〜%d 行）:' % (si[0] + 1, ei[0]), '']
    out += ['- %d: %s' % (i, l.strip()) for i, l in sec]
    conf = [(i + 1, l) for i, l in enumerate(L) if '【確認】' in l]
    if conf:
        out += ['', '**【確認】の行**:', ''] + ['- %d: %s' % (i, l.strip()) for i, l in conf]
    out.append('')
    total += len(v) + len(sec) + len(conf)
out += ['## この抜き書きが確認していないこと', '',
        '- 票の本文の是認は、ここに切り出した型の行のほかにも散らばっている（例えば問いごとの「妥当」の判定や、所見の中の「賛成」）。切り出しの型は器の頭に書いたとおりで、全ての是認を拾ってはいない。票の全文は第一巡の置き場にある。',
        '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
dst = os.path.join(HERE, 'round1-approvals-extract.md')
assert not os.path.exists(dst), '既にある: ' + dst
open(dst, 'w', encoding='utf-8', newline=NL).write(NL.join(out))
print('lines extracted', total)
