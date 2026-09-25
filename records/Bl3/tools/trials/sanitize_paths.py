# -*- coding: utf-8 -*-
"""試しの走りの記録の写し（進みの印字・session・一致だけを見る段の記録・まとめ）から、手元の置き場の道筋（利用者の名・会話の番号を含む）を決まった言い方に置き換える。
置き換えた置き場と数を、まとめの末尾に一行で書く（値は変えない）。
用法: python records/Bl3/tools/trials/sanitize_paths.py <記録の置き場> <一時の置き場> [<一時の置き場> …]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
REC = os.path.abspath(sys.argv[1])
roots = [(os.path.abspath(p), '〈一時の置き場〉') for p in sys.argv[2:]] + [(REPO, '〈リポジトリ〉')]


def forms(p):
    return [p, p.replace('\\', '\\\\'), p.replace('\\', '/'), json.dumps(p)[1:-1]]


n = 0
for f in sorted(glob.glob(os.path.join(REC, '*'))):
    t = open(f, encoding='utf-8').read()
    t0 = t
    for p, lab in roots:
        for x in sorted(set(forms(p)), key=len, reverse=True):
            n += t.count(x)
            t = t.replace(x, lab)
    if t != t0:
        open(f, 'w', encoding='utf-8', newline='\n').write(t)
left = [f for f in glob.glob(os.path.join(REC, '*')) if 'AppData' in open(f, encoding='utf-8').read() or 'Users\\PC' in open(f, encoding='utf-8').read() or 'Users/PC' in open(f, encoding='utf-8').read()]
assert not left, ('手元の道筋が残った', left)
sm = os.path.join(REC, 'summary.md')
if os.path.exists(sm):
    s = open(sm, encoding='utf-8').read().rstrip('\n').split('\n')
    s.insert(len(s) - 1, '- この置き場の写し（進みの印字・session・一致だけを見る段の記録・このまとめ）では、手元の置き場の道筋 %d か所を〈一時の置き場〉・〈リポジトリ〉に置き換えた（`records/Bl3/tools/trials/sanitize_paths.py`・値は変えていない）。' % n)
    s.insert(len(s) - 1, '')
    open(sm, 'w', encoding='utf-8', newline='\n').write('\n'.join(s) + '\n')
print('[sanitize_paths] %d か所を置き換えた（%s）' % (n, os.path.relpath(REC, REPO)))
