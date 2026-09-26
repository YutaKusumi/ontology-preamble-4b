# -*- coding: utf-8 -*-
"""起草者の欄（「この結果が退けた説明」）の元の文 `records/Bl3/results-rejected-lines-Bl3.md` を、結果の巡の採否の案の案の文 1〜3 に替える（登録者裁定 D244・D246）。
案の文は、公開した採否の案（コミット 2eaa387 の `records/reviews/Bl3/results-round1/adoption-results-Bl3.md` の「案の文」の節）から機械で切り出す（手で打たない）。
一行目は頭に「- 」を付けない（凍結した組み立ての器の `--rejected` の受け方・器が一行目に「- 」を足す）。前の文はコミット 912fc47 にある（git の履歴）。
用法: python records/Bl3/rejected_lines_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'results-rejected-lines-Bl3.md')
ad = subprocess.run(['git', 'show', '2eaa387:records/reviews/Bl3/results-round1/adoption-results-Bl3.md'], cwd=REPO, capture_output=True).stdout.decode('utf-8')
L = ad.split(NL)
h = [i for i, l in enumerate(L) if l.startswith('## 案の文（起草者の欄の三行')]
assert len(h) == 1, h
body = []
for l in L[h[0] + 1:]:
    if l.startswith('## '):
        break
    mm = re.match(r'^([123])\. (.*)$', l)
    if mm:
        body.append((int(mm.group(1)), mm.group(2)))
assert [k for k, _ in body] == [1, 2, 3], body
old = open(OUT, encoding='utf-8').read()
assert old.startswith('「この大きさの加減では') and old.count(NL + '- ') == 2, '前の文の形が想定と違う'
new = NL.join([body[0][1], '- ' + body[1][1], '- ' + body[2][1]]) + NL
open(OUT, 'w', encoding='utf-8', newline=NL).write(new)
print('wrote', os.path.relpath(OUT, REPO), '| lines', [len(s) for _, s in body])
