# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D231〜D235 の記録を書く（器についての意見伺いの採否の後）。
登録者の言葉と、裁定の前にコーディネータが示した推奨の段は、会話の記録から機械で切り出す（手で打たない）。
採られた案: 抜き書きの各裁定の一つ目の案（登録者の言葉「いずれもご推奨の案を承認いたします」）。
既にある記録には書かない。
用法: python records/Bl3/rulings_D231_D235.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D231-D235.md')
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'いずれもご推奨の案を承認いたします' in m[3])
H0, H1 = '## ご裁定をお願いしたいこと（一つ目が私の推奨）', '## 次に進む前のお願い'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and H1 in m[3] and all(d in m[3] for d in ('D231', 'D232', 'D233', 'D234', 'D235')) and m[2] < appr[2])
excerpt = rec[3][rec[3].index(H0):rec[3].index(H1)].rstrip()
ask = rec[3][rec[3].index(H1):].rstrip()


def option(d, k):
    """抜き書きの裁定 d の k 番目の案（字下げの改行は空白にした）。"""
    seg = excerpt[excerpt.index('**%s' % d):]
    nxt = [seg.find('- **D%d' % n) for n in range(int(d[1:]) + 1, int(d[1:]) + 3) if seg.find('- **D%d' % n) > 0]
    seg = seg[:min(nxt)] if nxt else seg
    m = re.search(r'^  %d\. (.+?)(?=^  %d\. |\n\n|\n\S|\Z)' % (k, k + 1), seg, flags=re.M | re.S)
    assert m, (d, k)
    return ' '.join(x.strip() for x in m.group(1).strip().split(NL))


taken = {d: option(d, 1) for d in ('D231', 'D232', 'D233', 'D234', 'D235')}
w = appr[3]
pushed = git('rev-parse', '--short', 'origin/main')
cell = lambda s: str(s).replace('|', '｜')
R = ['# 登録者裁定 D231〜D235（%s・B-lens 層三・器についての意見伺いの採否の後）' % jst(appr[2])[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), w.strip().replace(NL, ' ')),
     '- 裁定の前にコーディネータが示した推奨の段と、同じ返信の「次に進む前のお願い」の段を下に逐語で置く（会話の記録 uuid `%s`・%s 日本時間）。' % (rec[1], jst(rec[2])),
     '- 前提: 下の注のとおり。', '',
     '| 裁定 | 採られた案（抜き書きから機械で切り出した・字下げの改行は空白にした） |', '|---|---|'] + ['| %s | 一つ目の案（ご推奨どおり）: %s |' % (d, cell(taken[d])) for d in ('D231', 'D232', 'D233', 'D234', 'D235')] + [
     '',      '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）', '', '````text', excerpt, '````', '',
     '## 同じ返信の「次に進む前のお願い」（逐語）', '', '````text', ask, '````', '',
     '## 注（事実のみ）', '',
     '- 前提: 器についての意見伺い（裁定 D230）の採否の案 `records/reviews/Bl3/opinions-tools/adoption-proposal-opinions-tools-Bl3.md`（A〜F の表・確かめ `checks/verification-opinions-tools-Bl3.md`）。',
     '- 同じ言葉で、登録者は保全と確かめと採否の案のコミット 110a748 の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- D231 で採らない一つ（書き換えの道の既定の引数・案の E の表）は、採否の案のとおり採らない。',
     '- 記帳の置き場: 正本の `decisions` への D228〜D235 の記帳と、D232〜D235 の文の直しは、下見の前の凍結の正本（生成器 v7）で行う。',
     '- 番号: 次の裁定は D236 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), rec[1], '| origin/main', pushed)
