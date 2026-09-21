# -*- coding: utf-8 -*-
"""四票を会話の記録（jsonl）から機械で切り出し、逐語で保全する（手で打ち直さない・既にあるファイルには書かない）。
用法: python extract_votes_qpost.py <会話の記録 jsonl>"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1]
MARKS = [('Geminiさん（一人目）', 'gemini-1', 'Gemini 3.8 Flash（系統外）・一人目'),
         ('Geminiさん（二人目）', 'gemini-2', 'Gemini 3.8 Flash（系統外）・二人目'),
         ('Claudeさん（一人目）', 'claude-ai-1', 'claude.ai の Claude Opus 5（起草者と同一系列）・一人目'),
         ('Claudeさん（二人目）', 'claude-ai-2', 'claude.ai の Claude Opus 5（起草者と同一系列）・二人目')]
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
        if all(m[0] in t for m in MARKS) and '選定後の品質床' in t:
            best = (t, o.get('uuid'), o.get('timestamp'))
assert best, '四票を含む登録者の発言が見つからない'
text, uuid, ts = best
pos = [text.index(m[0]) for m in MARKS]
assert pos == sorted(pos)
NL = chr(10)
for i, (mark, d, who) in enumerate(MARKS):
    seg = text[pos[i] + len(mark):(pos[i + 1] if i + 1 < len(MARKS) else len(text))].strip()
    assert seg.startswith('「') and seg.endswith('」'), (d, seg[:20], seg[-20:])
    body = seg[1:-1].strip(NL)
    out_dir = os.path.join(HERE, d)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, 'review.md')
    assert not os.path.exists(out), '既にある（逐語保全のファイルには上書きしない）: %s' % out
    head = ['<!-- 逐語保全: %s。登録者（楠見優太）が会話で渡した票を、会話の記録から機械で切り出した（uuid %s・%s）。' % (who, uuid, ts),
            '     この枠の外は一字も変えていない。本票のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->', '']
    open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(head) + body + NL)
    print('%-12s %6d 字  SHA16 %s' % (d, len(body), hashlib.sha256(body.encode('utf-8')).hexdigest().upper()[:16]))
print('uuid', uuid, ts)
