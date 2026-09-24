# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の封印の前の露出の記録に、段を足す（前の段は書き換えない・同じ段を二度足さない）。
足す段: (一) 露出の扱いの決定（登録者裁定 D217・裁定の記録から機械で読む）。(二) 設計の巡・二巡目の票の確かめ（票が届いた時刻は会話の記録から取る）。
用法: python records/Bl3/append_exposure_Bl3_r2.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
P = os.path.join(HERE, 'exposure-before-seal-Bl3.md')
s = open(P, encoding='utf-8').read()
H1, H2 = '## 扱いの決定（登録者裁定 D217）', '## 設計の巡・二巡目の票（最終検分）'
assert H1 not in s and H2 not in s, '既に足してある'
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
R = open(os.path.join(HERE, 'rulings-D211-D217.md'), encoding='utf-8').read()
d217 = [l for l in R.split(NL) if l.startswith('| D217 |')]
assert len(d217) == 1
d217_cell = d217[0].split('|')[3].strip()
got = None
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user':
        continue
    c = (o.get('message') or {}).get('content')
    texts = [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    for t in texts:
        if 'Geminiさん（一人目）' in t and 'Claudeさん（二人目）' in t and 'B-lens 層三の枠（草案2）' in t:
            got = (o.get('uuid'), o.get('timestamp'))
assert got
FOOT = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
assert s.rstrip(NL).endswith(FOOT)
body = s.rstrip(NL)[:-len(FOOT)].rstrip(NL)
add = ['', H1, '',
       '- 上の「扱い（登録者の裁定を待つ）」の段は、登録者裁定 D217 で決まった。決まった形（`records/Bl3/rulings-D211-D217.md` の D217 の行・逐語）: %s' % d217_cell,
       '- 上の段は、決まる前の記録として書き換えずに残す（設計の巡・二巡目の C2 の所見 N11 を受けた）。', '',
       H2, '',
       '- 票が届いた時刻: %s 日本時間（登録者が四票を会話に貼った発言・会話の記録 uuid `%s`・票は `records/reviews/Bl3/design-round2/<票の名>/review.md`）。' % (jst(got[1]), got[0]),
       '- 四票とも、全経路の効き目を計算していないと書いている。封印する予想の項目に触れる見込みの文は、見当たらなかった（コーディネータの通読・機械の検査ではない）。',
       '- 器の許容についての見込み（数値の揺れで許容を超えうるという文・G2 の所見 Ⅱ-1）は、器の働きについての文で、封印する予想の項目に触れないので、露出に数えない。', '',
       FOOT, '']
open(P, 'w', encoding='utf-8', newline=NL).write(body + NL + NL.join(add))
print('appended to', os.path.basename(P), '| round-2 votes at', jst(got[1]))
