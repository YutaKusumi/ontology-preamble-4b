# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D236・D237 の記録を書く（器の実装の検分〔二体〕の採否の後）。
登録者の言葉と、裁定の前にコーディネータが示した推奨の段は、会話の記録から機械で切り出す（手で打たない）。
採られた案: 抜き書きの D236 と D237 の一つ目の案（登録者の言葉「D236とD237は、ご推奨の案を承認します」）。D238 は、同じ言葉で登録者が別の形を示して意見を求めたので、まだ決まっていない。
既にある記録には書かない。
用法: python records/Bl3/rulings_D236_D237.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D236-D237.md')
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'D236とD237は、ご推奨の案を承認します' in m[3])
H0 = '## ご裁定のお願い（一つ目が推奨）'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and all(d in m[3] for d in ('D236', 'D237', 'D238')) and m[2] < appr[2])
excerpt = rec[3][rec[3].index(H0):].rstrip()
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for s in (appr[3], excerpt):
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
        assert bad not in s, '貼り付けの印か系統の印が入っている'
    assert '````' not in s


def option(d, k):
    """抜き書きの裁定 d の k 番目の案（字下げの改行は空白にした）。"""
    seg = excerpt[excerpt.index('**%s' % d):]
    nxt = [seg.find('- **D%d' % n) for n in range(int(d[1:]) + 1, int(d[1:]) + 3) if seg.find('- **D%d' % n) > 0] + [p for p in [seg.find('- **push')] if p > 0]
    seg = seg[:min(nxt)] if nxt else seg
    m = re.search(r'^  %d\. (.+?)(?=^  %d\. |\n\n|\n\S|\Z)' % (k, k + 1), seg, flags=re.M | re.S)
    assert m, (d, k)
    return ' '.join(x.strip() for x in m.group(1).strip().split(NL))


taken = {d: option(d, 1) for d in ('D236', 'D237')}
pushed = git('rev-parse', '--short', 'origin/main')
cell = lambda s: str(s).replace('|', '｜')
R = ['# 登録者裁定 D236・D237（%s・B-lens 層三・器の実装の検分〔二体〕の採否の後）' % jst(appr[2])[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), appr[3].strip().replace(NL, ' ')),
     '- 裁定の前にコーディネータが示した推奨の段を下に逐語で置く（会話の記録 uuid `%s`・%s 日本時間）。' % (rec[1], jst(rec[2])), '',
     '| 裁定 | 採られた案（抜き書きから機械で切り出した・字下げの改行は空白にした） |', '|---|---|'] + ['| %s | 一つ目の案（ご推奨どおり）: %s |' % (d, cell(taken[d])) for d in ('D236', 'D237')] + [
     '', '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）', '', '````text', excerpt, '````', '',
     '## 注（事実のみ）', '',
     '- 前提: 器の実装の検分（二体）の採否の案 `records/reviews/Bl3/impl/adoption-table-impl-Bl3.md`（A の表 凍結の前に直す・B の表 記録に置く・C 採らない 無し）と確かめ `records/reviews/Bl3/impl/checks/`。',
     '- D236 の一つ目の案のとおり、走っていた合成データの正式の記録（検分の版 87ce664）を止めた。記録は書かれていない（途中の値は使わない）。',
     '- D238（直した後の外の目）は、同じ言葉で登録者が「新規の Gemini と claude.ai の Opus 5.5 に検分」という形を示して意見を求めたので、まだ決まっていない（次の言葉で決める）。',
     '- 同じ言葉には、ローカルのコミットの push の許可は無い（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 記帳の置き場: 正本の `decisions` への D236・D237 の記帳は、直しの後の正本（生成器 v8）で行う。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), rec[1], '| origin/main', pushed)
