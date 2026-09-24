# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D218（設計の巡・二巡目の組み立てと、最終検分とすること）の記録を書く（2026-09-24・草案2 の push の後・二巡目の束の前）。
登録者の言葉と、裁定の前にコーディネータが示した推奨の段は、会話の記録から機械で切り出す（手で打たない）。既にある記録には書かない。
用法: python records/Bl3/rulings_D218.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D218.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'D218はご推奨どおり' in m[3] and '最終検分' in m[3])
A0, A1 = '2. **D218: 二巡目', 'ご判断をいただければ、二巡目の束と'
rec = one(lambda m: m[0] == 'assistant' and A0 in m[3] and A1 in m[3] and m[2] < appr[2])
assert rec[3].count(A0) == 1 and rec[3].count(A1) == 1
excerpt = rec[3][rec[3].index(A0):rec[3].index(A1)].rstrip()
T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
pushed = git('rev-parse', '--short', 'origin/main')
w = lambda m: m[3].strip().replace(NL, ' ')
RUL = ('D218', '**設計の巡・二巡目の組み立て**: 二巡目は、第一巡と同じ四名（Gemini 3.8 Flash 二名・claude.ai の Claude Opus 5.5 二名）に依頼する。'
       '第一巡は差し戻しではなかったので、検分の巡の繰り返しを防ぐため、二巡目を下見の前の凍結の前の**最終検分**とし、依頼文にその旨を明記する（段階 B の裁定 D160・B-lens の裁定 D194 の型）。'
       'この巡のあとに設計の巡は置かない。所見は裁定で受け、草案3・器と合成データの確かめ・器の実装の検分・下見の前の凍結へ進む')
R = ['# 登録者裁定 D218（2026-09-24・B-lens 層三・設計の巡・二巡目）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), w(appr)),
     '- 「ご推奨」は、草案2 の報告の返信（会話の記録 uuid `%s`・%s 日本時間）の D218 の段で、コーディネータが推奨した組み立て（第一巡と同じ四名・下の抜き書き）。「最終検分とする」は登録者が同じ言葉で足した。' % (rec[1], jst(rec[2])), '',
     '| 裁定 | 中身 |', '|---|---|', '| %s | %s |' % RUL, '',
     '## 正本との関係（機械で読んだ逐語）', '',
     '- `review_plan.design.round2`: %s' % T3['review_plan']['design']['round2'],
     '- `review_plan.no_more`: %s' % T3['review_plan']['no_more'], '',
     '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語・会話の記録 uuid `%s`）' % rec[1], '', '````text', excerpt, '````', '',
     '## 注（事実のみ）', '',
     '- 抜き書きは、同じ返信の D218 の段の頭から次の段の頭の前までを、器が切り出したもの。',
     '- 同じ言葉で、登録者はコミット f4f7135 と 662c589 の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 記帳の置き場: 正本の `decisions` への D218 の記帳は草案3 の正本で行う。草案2 は、二巡目の束に入れたまま変えない。',
     '- 番号: 次の裁定は D219 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), '| excerpt', len(excerpt), '字 | origin/main', pushed)
