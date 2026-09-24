# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D224・D225 の記録を書く（草案3 の起草者の見直しの後）。
登録者の言葉と、裁定の前にコーディネータが示した推奨の段は、会話の記録から機械で切り出す（手で打たない）。
採られた案（各裁定の一つ目の案）と推奨の理由は、見直しの記録 `records/Bl3/draft3-review/review-draft3-Bl3.md` の「裁定の候補」の段から機械で読む。
既にある記録には書かない。
用法: python records/Bl3/rulings_D224_D225.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D224-D225.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
s16 = lambda rel: hashlib.sha256(open(os.path.join(REPO, *rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'D224とD225のいずれも、ご推奨の案を承認します' in m[3])
H0, H1 = '## ご裁定をお願いしたいこと（一つ目が私の推奨）', '## 直しの案と今の状態'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and H1 in m[3] and 'D224' in m[3] and 'D225' in m[3] and m[2] < appr[2])
excerpt = rec[3][rec[3].index(H0):rec[3].index(H1)].rstrip()
RV = 'records/Bl3/draft3-review/review-draft3-Bl3.md'
A = open(os.path.join(REPO, *RV.split('/')), encoding='utf-8').read()
sec = A[A.index('## 裁定の候補（一つ目が起草者の推奨）'):A.index('## 検分票')]
DEC = []
for m in re.finditer(r'^### (D22[45]) (.+)$', sec, flags=re.M):
    body = sec[m.end():]
    nxt = re.search(r'^### ', body, flags=re.M)
    body = body[:nxt.start()] if nxt else body
    first = re.search(r'^1\. (.+)$', body, flags=re.M).group(1).strip()
    why = re.search(r'^- 推奨と理由: (.+)$', body, flags=re.M).group(1).strip()
    DEC.append((m.group(1), m.group(2).strip(), first, why))
assert [d[0] for d in DEC] == ['D224', 'D225'], [d[0] for d in DEC]
pushed = git('rev-parse', '--short', 'origin/main')
head = git('rev-parse', '--short', 'HEAD')
w = lambda m: m[3].strip().replace(NL, ' ')
cell = lambda s: str(s).replace('|', '｜')
R = ['# 登録者裁定 D224・D225（%s・B-lens 層三・草案3 の起草者の見直しの後）' % jst(appr[2])[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), w(appr)),
     '- 「ご推奨」は、各裁定の候補の一つ目の案（見直しの記録 `%s`〔SHA16 %s〕の「裁定の候補」の段）。裁定の前にコーディネータが示した推奨の段を下に逐語で置く（会話の記録 uuid `%s`・%s 日本時間）。' % (RV, s16(RV), rec[1], jst(rec[2])),
     '- 前提: 草案3（コミット 3a0da45）の起草者の見直し（枠 `records/Bl3/draft3-review/frame-draft3-review-Bl3.md`・器の検査 `records/Bl3/draft3-review/check-draft3-Bl3.md`・見直しの記録）と、置き場の中の直しの案。', '',
     '| 裁定 | 何を決めたか | 採られた案（見直しの記録の一つ目の案・逐語） | 推奨の理由（見直しの記録・逐語） |', '|---|---|---|---|'] + [
     '| %s | %s | %s | %s |' % tuple(cell(x) for x in d) for d in DEC] + [
     '', '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）', '', '````text', excerpt, '````', '',
     '## 注（事実のみ）', '',
     '- 抜き書きは、同じ返信の「ご裁定をお願いしたいこと」の段の見出しから次の段の見出しの前までを、器が切り出したもの。',
     '- この言葉には、push と登録者最終確認についての指示は無い。この記録を書いた時点で、origin/main は %s、手元の HEAD は %s（草案3 と見直しの記録のコミットは push していない）。' % (pushed, head),
     '- 記帳の置き場: 正本の `decisions` への D224・D225 の記帳は、直しの案を確定する正本（生成器 v5）で行う。',
     '- 番号: 次の裁定は D226 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), '| excerpt', len(excerpt), '字 | origin/main', pushed, '| HEAD', head)
