# -*- coding: utf-8 -*-
"""最終検分（登録者裁定 D194）の二票（新しい Gemini 3.8 Flash の二つの会話）を、会話の記録（jsonl）から機械で切り出し、逐語で保全する
（手で打ち直さない・既にあるファイルには書かない）。結果の巡・第一巡の器 `records/reviews/Blens/results-round1/extract_votes_Blens_results_r1.py` を写し、
発言を見分ける語と票の数だけを改めた。
用法: python extract_votes_Blens_results_final.py <会話の記録 jsonl>"""
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]
MARKS = [('Geminiさん（一人目）', 'gemini-final-1', 'Gemini 3.8 Flash（系統外・登録者の言葉で新規の個体）・最終検分の一人目'),
         ('Geminiさん（二人目）', 'gemini-final-2', 'Gemini 3.8 Flash（系統外・登録者の言葉で新規の個体）・最終検分の二人目')]
best = None
for line in open(src, encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user':
        continue
    c = (o.get('message') or {}).get('content')
    texts = [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    for t in texts:
        if all(m[0] in t for m in MARKS) and '新規のGemini 3.8 Flash 二名' in t and '最終検分票' in t:
            best = (t, o.get('uuid'), o.get('timestamp'))
assert best, '二票を含む登録者の発言が見つからない'
text, uuid, ts = best
pos = [text.index(m[0]) for m in MARKS]
assert pos == sorted(pos)
NL = chr(10)
for i, (mark, d, who) in enumerate(MARKS):
    seg = text[pos[i] + len(mark):(pos[i + 1] if i + 1 < len(MARKS) else len(text))].strip()
    seg = re.sub(r'</pasted_content[^>]*>\s*$', '', seg).strip()      # 会話の記録で貼り付けの末尾に付く閉じ印を外す
    assert seg.startswith('「') and seg.endswith('」'), (d, seg[:20], seg[-20:])
    body = seg[1:-1].strip(NL)
    out_dir = os.path.join(HERE, d)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, 'review.md')
    head = ['<!-- 逐語保全: %s。登録者（楠見優太）が会話で渡した票を、会話の記録から機械で切り出した（uuid %s・%s）。' % (who, uuid, ts),
            '     この枠の外は一字も変えていない。本票のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->', '']
    content = NL.join(head) + body + NL
    if os.path.exists(out):                                   # 逐語保全は上書きしない。既にあれば中身が同じことだけを確かめる
        assert open(out, encoding='utf-8').read() == content, '既にあるファイルと中身が違う（上書きしない）: %s' % out
        print('%-15s 既にある・同一を確認' % d)
        continue
    open(out, 'w', encoding='utf-8', newline=NL).write(content)
    print('%-15s %6d 字  SHA16 %s' % (d, len(body), hashlib.sha256(body.encode('utf-8')).hexdigest().upper()[:16]))
print('uuid', uuid, ts)
