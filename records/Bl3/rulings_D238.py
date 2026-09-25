# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D238 の記録を書く（器の実装の検分の直しの後の外の目）。
登録者の言葉と、その前にコーディネータが示した提案の段は、会話の記録から機械で切り出す（手で打たない）。既にある記録には書かない。
採られた案: コーディネータの提案の段のとおり（登録者の言葉「ご提案の内容で進めましょう」）。
用法: python records/Bl3/rulings_D238.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D238.md')
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'D238（直した後の外の目）については、ご提案の内容で進めましょう' in m[3])
H0, H1 = '## D238（直した後の外の目）についての私の考え', '## push のお願い'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and H1 in m[3] and m[2] < appr[2])
excerpt = rec[3][rec[3].index(H0):rec[3].index(H1)].rstrip()
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for s in (appr[3], excerpt):
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
        assert bad not in s, '貼り付けの印か系統の印が入っている'
    assert '````' not in s
pushed = git('rev-parse', '--short', 'origin/main')
R = ['# 登録者裁定 D238（%s・B-lens 層三・器の実装の検分の直しの後の外の目）' % jst(appr[2])[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), appr[3].strip().replace(NL, ' ')),
     '- 採られた案: その前にコーディネータが示した提案の段のとおり（下に逐語で置く・会話の記録 uuid `%s`・%s 日本時間）。' % (rec[1], jst(rec[2])), '',
     '## コーディネータの提案の段（逐語）', '', '````text', excerpt, '````', '',
     '## 注（事実のみ）', '',
     '- 位置づけ: 正本 `review_plan.no_more` は「この順のほかに巡を置かない」とし、重い所見で直しが大きくなるときは登録者に上げて決めていただくとする。D238 は、器の実装の検分（重大 2 を含む）の直しの確かめの巡を一つ足す裁定である。',
     '- 同じ言葉で、登録者はローカルのコミット c1a759c・f5930f1・a98ee0e・01b8c75・6e72adc の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 記帳の置き場: 正本の `decisions` への D236〜D238 の記帳は、直しの後の正本（生成器 v8）で行う。', '- 番号: 次の裁定は D239 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| proposal', jst(rec[2]), rec[1], '| origin/main', pushed)
