# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D226・D227 の記録を書く（器の段の一回目の区切りの後）。
登録者の言葉と、裁定の前にコーディネータが示した推奨の段は、会話の記録から機械で切り出す（手で打たない）。
採られた案は、抜き書きの各裁定の一つ目の案（抜き書きから機械で切り出す）。既にある記録には書かない。
用法: python records/Bl3/rulings_D226_D227.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D226-D227.md')
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'D226とD227はご推奨どおりで' in m[3])
H0, H1 = '## ご裁定をお願いしたいこと（一つ目が私の推奨）', '## 次に進む前のお願い'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and H1 in m[3] and 'D226' in m[3] and 'D227' in m[3] and m[2] < appr[2])
excerpt = rec[3][rec[3].index(H0):rec[3].index(H1)].rstrip()
ask = rec[3][rec[3].index(H1):].rstrip()
first = {}
for d in ('D226', 'D227'):
    seg = excerpt[excerpt.index('**%s' % d):]
    nxt = [seg.find('- **D%d' % n) for n in range(int(d[1:]) + 1, int(d[1:]) + 3) if seg.find('- **D%d' % n) > 0]
    seg = seg[:min(nxt)] if nxt else seg
    m1 = re.search(r'^  1\. (.+?)(?=^  2\. )', seg, flags=re.M | re.S)
    assert m1, d
    first[d] = ' '.join(x.strip() for x in m1.group(1).strip().split(NL))
pushed = git('rev-parse', '--short', 'origin/main')
w = lambda m: m[3].strip().replace(NL, ' ')
cell = lambda s: str(s).replace('|', '｜')
R = ['# 登録者裁定 D226・D227（%s・B-lens 層三・器の段の一回目の区切りの後）' % jst(appr[2])[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), w(appr)),
     '- 「ご推奨」は、各裁定の候補の一つ目の案。裁定の前にコーディネータが示した推奨の段と、同じ返信の「次に進む前のお願い」の段を下に逐語で置く（会話の記録 uuid `%s`・%s 日本時間）。' % (rec[1], jst(rec[2])),
     '- 前提: 器の段の記録 `records/Bl3/tools/tools-log-Bl3.md` の「登録者に上げること」（T1〜T4）。', '',
     '| 裁定 | 採られた案（抜き書きの一つ目の案・逐語・字下げの改行は空白にした） |', '|---|---|'] + [
     '| %s | %s |' % (d, cell(first[d])) for d in ('D226', 'D227')] + [
     '', '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）', '', '````text', excerpt, '````', '',
     '## 同じ返信の「次に進む前のお願い」（逐語）', '', '````text', ask, '````', '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者は独立の再計算の器を書く個体を一体（Claude Opus 5.5 の新しい個体・エージェント）立てることと、三つのコミット（3259cc3・ca1fe0a・3bb772e）の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 記帳の置き場: 正本の `decisions` への D226・D227 の記帳と、裁定の中身（T1〜T3 の文・乙の行の決め方・転記行 E の乙の見込みの数え直し）は、下見の前の凍結の正本で行う（D226 の一つ目の案の「下見の前の凍結で入れる」）。',
     '- 番号: 次の裁定は D228 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), '| origin/main', pushed)
