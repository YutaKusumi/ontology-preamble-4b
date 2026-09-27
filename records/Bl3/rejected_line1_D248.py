# -*- coding: utf-8 -*-
"""起草者の欄（「この結果が退けた説明」）の元の文 `records/Bl3/results-rejected-lines-Bl3.md` の一行目を、最終の検分の採否の案の案の文（D248 の甲）に替える（登録者裁定 D248）。
案の文は、公開した採否の案（コミット 1135b35 の `records/reviews/Bl3/results-final/adoption-final-Bl3.md` の「案の文」の節）から機械で切り出す（手で打たない）。二行目と三行目は変えない。
前の文はコミット 3f467e7 にある（git の履歴）。
用法: python records/Bl3/rejected_line1_D248.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'results-rejected-lines-Bl3.md')
ad = subprocess.run(['git', 'show', '1135b35:records/reviews/Bl3/results-final/adoption-final-Bl3.md'], cwd=REPO, capture_output=True).stdout.decode('utf-8')
hit = [l for l in ad.split(NL) if l.startswith('- D248 の甲（')]
assert len(hit) == 1, hit
new1 = hit[0].split('）: ', 1)[1]
assert new1.startswith('「この大きさの加減では'), new1[:20]
old = open(OUT, encoding='utf-8').read().split(NL)
committed = subprocess.run(['git', 'show', '3f467e7:records/Bl3/results-rejected-lines-Bl3.md'], cwd=REPO, capture_output=True).stdout.decode('utf-8').split(NL)
assert old == committed, '今の起草者の欄の元の文が、草案の二つ目のときの文と違う'
assert len(old) == 4 and old[3] == '' and old[1].startswith('- ') and old[2].startswith('- ') and old[0] != new1
new = [new1, old[1], old[2], '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(new))
print('wrote', os.path.relpath(OUT, REPO), '| line 1 chars', len(old[0]), '->', len(new1))
