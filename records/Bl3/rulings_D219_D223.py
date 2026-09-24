# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D219〜D223 の記録を書く（2026-09-24・設計の巡・二巡目〔最終検分〕の後・草案3 の前）。
登録者の言葉と、裁定の前にコーディネータが示した推奨の段は、会話の記録から機械で切り出す（手で打たない）。
採られた案（各裁定の一つ目の案）と推奨の理由は、採否表 `records/reviews/Bl3/design-round2/adoption-table-Bl3-design-r2.md` の §2 から機械で読む。
既にある記録には書かない。
用法: python records/Bl3/rulings_D219_D223.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D219-D223.md')
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and 'D219〜D223はご推奨どおりで' in m[3] and 'f2b55dc' in m[3])
H0, H1 = '## ご裁定をお願いしたいこと（一つ目が私の推奨）', '## 枠の予想の当たり外れ'
rec = one(lambda m: m[0] == 'assistant' and H0 in m[3] and H1 in m[3] and 'D219' in m[3] and m[2] < appr[2])
excerpt = rec[3][rec[3].index(H0):rec[3].index(H1)].rstrip()
AT = 'records/reviews/Bl3/design-round2/adoption-table-Bl3-design-r2.md'
A = open(os.path.join(REPO, *AT.split('/')), encoding='utf-8').read()
sec = A[A.index('## 2. 登録者の裁定の候補'):A.index('## 3. 票を見る前の枠の予想')]
DEC = []
for m in re.finditer(r'^### (D2(?:19|2[0-3])) (.+)$', sec, flags=re.M):
    body = sec[m.end():]
    nxt = re.search(r'^### ', body, flags=re.M)
    body = body[:nxt.start()] if nxt else body
    first = re.search(r'^1\. (.+)$', body, flags=re.M).group(1).strip()
    why = re.search(r'^- 推奨と理由: (.+)$', body, flags=re.M).group(1).strip()
    DEC.append((m.group(1), m.group(2).strip(), first, why))
assert [d[0] for d in DEC] == ['D219', 'D220', 'D221', 'D222', 'D223'], [d[0] for d in DEC]
pushed = git('rev-parse', '--short', 'origin/main')
w = lambda m: m[3].strip().replace(NL, ' ')
cell = lambda s: str(s).replace('|', '｜')
R = ['# 登録者裁定 D219〜D223（2026-09-24・B-lens 層三・設計の巡・二巡目〔最終検分〕の後・草案3 の前）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), w(appr)),
     '- 「ご推奨」は、各裁定の候補の一つ目の案（採否表 `%s`〔SHA16 %s〕の §2）。裁定の前にコーディネータが示した推奨の段を下に逐語で置く（会話の記録 uuid `%s`・%s 日本時間）。' % (AT, s16(AT), rec[1], jst(rec[2])),
     '- 前提: 設計の巡・二巡目（最終検分・裁定 D218）の四票（`records/reviews/Bl3/design-round2/<票の名>/review.md`）・事実の確かめ（`verification-Bl3-design-r2.md`）・封印の前の露出の記録（`records/Bl3/exposure-before-seal-Bl3.md`）。', '',
     '| 裁定 | 何を決めたか | 採られた案（採否表の一つ目の案・逐語） | 推奨の理由（採否表・逐語） |', '|---|---|---|---|'] + [
     '| %s | %s | %s | %s |' % tuple(cell(x) for x in d) for d in DEC] + [
     '', '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）', '', '````text', excerpt, '````', '',
     '## 注（事実のみ）', '',
     '- 抜き書きは、同じ返信の「ご裁定をお願いしたいこと」の段の見出しから次の段の見出しの前までを、器が切り出したもの。',
     '- 同じ言葉で、登録者はコミット f2b55dc の push と、草案3 の起草を許可し、草案3 の起草の後に登録者が最終確認をする（そこで一旦見せる）とした。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 採否表のほかの行（採用・是認・記録）は、案のまま草案3 で受ける。受け方の対応は草案3 の対応の記録に置く。最終検分の後なので、草案3 の後に設計の巡は置かない（裁定 D218）。',
     '- 記帳の置き場: 正本の `decisions` への D218〜D223 の記帳は草案3 の正本で行う。',
     '- 番号: 次の裁定は D224 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), '| excerpt', len(excerpt), '字 | origin/main', pushed)
