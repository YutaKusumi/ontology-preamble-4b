# -*- coding: utf-8 -*-
# derive_brief_builder_v1_bs.py : 組みの道具 v0 から v1 を作る（検分の直しに合わせて照らす文を替え、記録の表に検分の答えを足す）
# 使い方: python -I derive_brief_builder_v1_bs.py <work_dir>
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
W = sys.argv[1]
SRC = os.path.join(W, 'tools', 'build_stance_bs_brief_v0.py')
DST = os.path.join(W, 'tools', 'build_stance_bs_brief_v1.py')
t = open(SRC, encoding='utf-8', newline='').read()
REP = [
    ("# build_stance_bs_brief_v0.py : 公開の短い報告を、型（template）と凍結の判定の出力と監査の出力から組む（第一の登録の build_stance_brief_v1_1.py の型）\n",
     "# build_stance_bs_brief_v1.py : 公開の短い報告（版 1.0）を、型（template）と凍結の判定の出力と監査の出力から組む（第一の登録の build_stance_brief_v1_1.py の型）\n#   v0 からの違い：下書きの検分（reviews/draft-1/）の直しに合わせて照らす文を替え、§4 の比べごとの書き分けを表 7 の値から照らし、記録の表に検分の答えを足した。\n"),
    ("# 使い方: python -I build_stance_bs_brief_v0.py <work_dir> <template> <out>\n", "# 使い方: python -I build_stance_bs_brief_v1.py <work_dir> <template> <out>\n"),
    ("need('一人目がパーサと違った %d・写しの誤り %d・合ったものの 1 割 %d の、合わせて %d' % (adiff, qerr, pct, bcnt))\n",
     "assert all(x['a_category'] == UND for x in rows if x['a_category'] != x['parser_category'])\nneed('一人目が決められないとした %d・写しの誤り %d・合ったものの 1 割 %d の、合わせて %d' % (adiff, qerr, pct, bcnt))\n"),
    ("need('立場の文が無くても破局的選択の率が高かった（N1 %s・N2 %s・SK %s）' % (r('N1', 'N'), r('N2', 'N'), r('SK', 'N')))\n",
     "need('この三つの場面では、立場の文が無くても破局的選択の率が高かった（N1 %s・N2 %s・SK %s）' % (r('N1', 'N'), r('N2', 'N'), r('SK', 'N')))\n"),
    ("# N1 の腕ごとの JSON だけの割合と全分母の率の相関（記述）\n",
     "# §4 の比べごとの書き分け（表 7 の値から）\n"
     "same = [c for c in some if c not in flip]\n"
     "assert sorted(key(c) for c in same) == sorted([('N1', '仏性', '有', '無'), ('N1', '神性', '無', '不明')])\n"
     "need('N1 の仏性の無と不明・N1 の神性の有と不明・SK の神性の無と不明の %d つは、散文のある答えの率の差が全分母の差と逆の向きである' % len(flip))\n"
     "need('N1 の仏性の有と無・N1 の神性の無と不明の %d つは、向きは同じだが' % len(same))\n"
     "need('残りの %d は、両方の腕に JSON だけの答えが無い' % len(both0))\n"
     "need('残りの %d（N1 の %d・SK の神性の %d）は、この形の差と重なり、そのうち %d は' % (len(some), sum(1 for c in some if c['scene'] == 'N1'), sum(1 for c in some if c['scene'] == 'SK'), len(flip)))\n"
     "need('基準を通った 10 のうち %d は、両方の腕に JSON だけの答えが無い（N2 の %d・SK の仏性の %d）' % (len(both0), sum(1 for c in both0 if c['scene'] == 'N2'), sum(1 for c in both0 if c['scene'] == 'SK')))\n"
     "# N1 の腕ごとの JSON だけの割合と全分母の率の相関（記述）\n"),
    ("need('SK で (a) を選び奪う量を 0 と書いた答えは %d で、破局に数えない（帽子の腕に %d・神性の不明に %d）' % (atot['surv_a_amount0'], bo, sf))\n",
     "need('SK で (a) を選び奪う量を 0 と書いた答えは %d で、破局に数えない（帽子の腕に %d・神性の不明に %d。内訳は `audit/open/partB-tallies.json`）' % (atot['surv_a_amount0'], bo, sf))\n"),
    ("    ('reviews/freeze-1b/response-v0.md', '凍結の前の系統外の検分への答え'),\n",
     "    ('reviews/freeze-1b/response-v0.md', '凍結の前の系統外の検分への答え'),\n    ('reviews/draft-1/answer.txt', 'この報告の下書きの系統外の検分の答え'),\n    ('reviews/draft-1/response-v0.md', 'この報告の下書きの検分への答え'),\n"),
]
for old, new in REP:
    n = t.count(old)
    assert n == 1, (n, old[:50])
    t = t.replace(old, new)
with open(DST, 'x', encoding='utf-8', newline='') as f:
    f.write(t)
print('ok', len(REP))
