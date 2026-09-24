# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の設計の巡・第一巡の四票から、総括（総合の判定の行・§16 の論点への意見・総合の節）を逐語で切り出す（B-lens の二巡目の型・「問題なし」も次の巡に渡す）。
切り出しは器が行い、手で打たない。行の番号は票のファイルの行。是認だけでなく、条件つきの意見と反対もそのまま含む。
用法: python records/reviews/Bl3/design-round2/extract_round1_verdicts.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.join(HERE, '..', 'design-round1')
NL = chr(10)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
END = r'^(本検分票|本検分の|本票|本依頼|採否表に取り込みやすい|この票を、記録に)'
VOTES = [  # (名, 札, 総合の判定の行の型, §16 の節の始まり, 総合の節の始まり, 総合の節の終わり)
    ('gemini-1', 'G1', [r'^- \*\*総合判定\*\*', r'^- \*\*判定\*\*'], r'^### 11\. §16 の論点への意見', r'^### 12\. 総合判定', END),
    ('gemini-2', 'G2', [r'^- 判定: ', r'^- \*\*判定\*\*'], r'^### 11\. §16 の論点への意見', r'^### 12\. 総合判定', END),
    ('claude-ai-1', 'C1', [r'^12\. 総合'], r'^11\. §16 の論点', r'^12\. 総合', END),
    ('claude-ai-2', 'C2', [r'^\*\*総合\*\*', r'^12\. \*\*総合\*\*'], r'^11\. \*\*§16\*\*', r'^12\. \*\*総合\*\*', r'^## 確認していないこと'),
]
out = ['# 設計の巡・第一巡の四票の総括の抜き書き（逐語・器 `records/reviews/Bl3/design-round2/extract_round1_verdicts.py`・2026-09-24）', '',
       '- 第一巡の四票の、総合の判定の行・§16 の論点への意見の節・総合の節を、票のファイルから器が切り出した（「問題なし」も次の巡に渡す手順）。行の番号は票のファイルの行。',
       '- 切り出しは是認だけでなく、条件つきの意見と反対もそのまま含む。所見の本文は各票のファイルにある。', '']
total = 0
for name, tag, vp, s16p, sop, eop in VOTES:
    p = os.path.join(R1, name, 'review.md')
    L = open(p, encoding='utf-8').read().split(NL)
    out += ['## %s（%s・`records/reviews/Bl3/design-round1/%s/review.md`・SHA16 %s）' % (tag, name, name, s16(p)), '', '**総合の判定の行**:', '']
    v = [(i + 1, l) for i, l in enumerate(L) if any(re.search(q, l) for q in vp)]
    assert v, (name, '総合の判定の行が無い')
    out += ['- %d: %s' % (i, l.strip()) for i, l in v]
    si = [i for i, l in enumerate(L) if re.search(s16p, l)]
    so = [i for i, l in enumerate(L) if re.search(sop, l)]
    assert len(si) == 1 and len(so) == 1 and si[0] < so[0], (name, si, so)
    eo = [i for i, l in enumerate(L) if i > so[0] and re.search(eop, l)]
    e_ = eo[0] if eo else len(L)
    sec16 = [(i + 1, L[i]) for i in range(si[0], so[0]) if L[i].strip() and L[i].strip() != '---']
    secT = [(i + 1, L[i]) for i in range(so[0], e_) if L[i].strip() and L[i].strip() != '---']
    out += ['', '**§16 の論点への意見**（%d〜%d 行）:' % (si[0] + 1, so[0]), ''] + ['- %d: %s' % (i, l.strip()) for i, l in sec16]
    out += ['', '**総合の節**（%d〜%d 行）:' % (so[0] + 1, e_), ''] + ['- %d: %s' % (i, l.strip()) for i, l in secT] + ['']
    total += len(v) + len(sec16) + len(secT)
out += ['## この抜き書きが確認していないこと', '',
        '- 票の本文の他の所にある是認（所見の中の「評価できる」など）は切り出していない。票の全文は各票のファイル。', '',
        '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'round1-verdicts-extract.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(out))
print('wrote round1-verdicts-extract.md | lines', total)
