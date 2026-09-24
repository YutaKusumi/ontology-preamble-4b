# -*- coding: utf-8 -*-
"""B-lens の登録者裁定 D200（README の案内の一行と、公開の後のタグ）の記録を書く（2026-09-24・公開の仕上げ）。
登録者の言葉と、裁定の前にコーディネータが示した案は、会話の記録から機械で切り出す（手で打たない）。push したコミットとタグは git から読み、
GitHub の上にあることは git ls-remote で確かめる。既にある記録には書かない。
用法: python records/Blens/rulings_D200.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D200.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
TAG = 'release-Blens-2026-09-24'
FINAL = 'records/Blens/results-Blens-FINAL-2026-09-24.md'
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True).stdout
MSGS = []
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
            MSGS.append((t, o.get('uuid'), o.get('timestamp'), x.get('text') or ''))
rul = [m for m in MSGS if m[0] == 'user' and len(m[3]) < 800 and 'D200' in m[3] and 'タグ' in m[3] and 'push' in m[3]]
assert len(rul) == 1, len(rul)
rul = rul[0]
opts = [m for m in MSGS if m[0] == 'assistant' and 'D200 のご確認' in m[3] and 'release-Blens-2026-09-24' in m[3] and m[2] < rul[2]]
assert opts, '裁定の前の案が見つからない'
opts = opts[-1]
words = rul[3].strip().replace(NL, ' ')
target = git('rev-parse', '%s^{commit}' % TAG).decode().strip()
tag_obj = git('rev-parse', TAG).decode().strip()
tag_msg = git('tag', '-l', '--format=%(contents:subject)', TAG).decode().strip()
remote = git('ls-remote', '--tags', 'origin', TAG + '*').decode().split(NL)
assert any(l.startswith(tag_obj) and l.endswith('refs/tags/%s' % TAG) for l in remote) and any(l.startswith(target) and l.endswith('^{}') for l in remote), 'タグが GitHub の上に無い（止める）'
main_remote = [l.split()[0] for l in git('ls-remote', 'origin', 'refs/heads/main').decode().split(NL) if l.strip()][0]
assert main_remote == target, ('GitHub の main がタグのコミットと違う', main_remote, target)
pushed = git('log', '--format=%h %s', 'd90c56b..%s' % target).decode().strip().split(NL)
fin = git('show', '%s:%s' % (target, FINAL)).replace(b'\r\n', b'\n')
fin16 = hashlib.sha256(fin).hexdigest().upper()[:16]
short = lambda h: git('rev-parse', '--short', h).decode().strip()
R = ['# 登録者裁定 D200（2026-09-24・公開の仕上げ）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (rul[1], jst(rul[2]), words), '',
     '| 裁定 | 中身 |', '|---|---|',
     '| D200 | README の段階 B の節に、B-lens の案内の一行（最終版・凍結の本文・台帳・露出の記録・検分の置き場）を載せる。公開の後に、最終版の入ったコミットに注釈つきのタグ `%s` を付ける（段階 B の型） |' % TAG, '',
     '## 裁定の前にコーディネータが示した案（逐語・会話の記録 uuid `%s`・%s 日本時間）' % (opts[1], jst(opts[2])), '', '````text', opts[3].rstrip(), '````', '',
     '## 注（事実のみ・git から読んだ）', '',
     '- 登録者の許可を受けて push したコミット（d90c56b の後の %d つ・古い順）: %s。GitHub の main は %s。' % (len(pushed), '・'.join(reversed([p.split(' ')[0] for p in pushed])), short(main_remote)),
     '- タグ `%s`（注釈つき・注釈「%s」）は %s を指し、GitHub の上にある（git ls-remote で確かめた）。' % (TAG, tag_msg, short(target)),
     '- そのコミットの最終版 `%s` の SHA16 は %s（登録者最終確認の後に組み直した版・`records/Blens/rulings-D198-D199.md`）。' % (FINAL, fin16),
     '- 番号: 次の裁定は D201 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '|', jst(rul[2]), rul[1], '| options', jst(opts[2]), opts[1], '| tag ->', short(target), '| main', short(main_remote), '| FINAL', fin16, '| pushed', len(pushed))
