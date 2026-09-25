# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器の実装の検分の起動の許可の記録を書く（正本 `review_plan.impl.budget`）。
登録者の言葉と、その前にコーディネータが示した申告の段（体数・機種・費用・時機）は、会話の記録から機械で切り出す（手で打たない）。既にある記録には書かない。
用法: python records/reviews/Bl3/impl/cut_permission_impl_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'permission-impl-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
M = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    t = o.get('type')
    c = (o.get('message') or {}).get('content')
    items = [{'type': 'text', 'text': c}] if isinstance(c, str) else [x for x in (c or []) if isinstance(x, dict)]
    for x in items:
        if x.get('type') == 'text' and t in ('user', 'assistant'):
            M.append((t, o.get('uuid'), o.get('timestamp'), x.get('text') or ''))
one = lambda f: (lambda h: (h[0] if len(h) == 1 else (_ for _ in ()).throw(SystemExit('一つに決まらない: %d' % len(h)))))([m for m in M if f(m)])
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and '器の実装の検分を起動してください' in m[3])
H0 = '## ご判断をお願いしたいこと'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and '87ce664' in m[3] and m[2] < appr[2])
ask = rec[3][rec[3].index(H0):].rstrip()
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for s in (appr[3], ask):
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
        assert bad not in s, '貼り付けの印か系統の印が入っている'
    assert '````' not in s
pushed = subprocess.run(['git', 'rev-parse', '--short', 'origin/main'], cwd=REPO, capture_output=True, text=True).stdout.strip()
R = ['# 器の実装の検分の起動の許可（%s・B-lens 層三・正本 `review_plan.impl.budget`）' % jst(appr[2])[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), appr[3].strip().replace(NL, ' ')),
     '- その前にコーディネータが示した申告の段（逐語・会話の記録 uuid `%s`・%s 日本時間）を下に置く。' % (rec[1], jst(rec[2])), '',
     '## コーディネータの申告の段（逐語）', '', '````text', ask, '````', '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者は四回目の区切りのコミット 87ce664 の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 同じ言葉の「実行中のタスク」の二件は、正式の合成データの記録の走り（途中）と、その見張りだった。見張りは止め、走りは続けた（「実行済み」ではないため）。',
     '- 起動の時機について、登録者の言葉は時機を指定していない。コーディネータは、検分者の合成の走りを少ない糸で走らせる形にして、正式の記録と並べて起動した（依頼文）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('[cut_permission_impl_Bl3] wrote %s' % os.path.relpath(OUT, REPO))
