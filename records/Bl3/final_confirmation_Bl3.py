# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者最終確認の記録を書き、確認していただいた案を一字違わず残す（登録者裁定 D252 の甲・二度目の見直しの R-h で補った文・B-lens の D199 の型）。
登録者の言葉と時刻と uuid は、会話の記録から機械で切り出す（手で打たない）。確認していただいた案は、push したコミット 1ac0e4b の最終版の案のバイトをそのまま写す。
書くもの（どちらも一度だけ）:
  records/Bl3/final-confirmation-Bl3.json（凍結した組み立ての器が読む鍵 when_jst・uuid・words と、確認していただいた案の置き場と SHA16）
  records/Bl3/results-Bl3-proposal-confirmed-2026-09-27.md（確認していただいた案の写し）
用法: python records/Bl3/final_confirmation_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT_J = os.path.join(HERE, 'final-confirmation-Bl3.json')
OUT_C = os.path.join(HERE, 'results-Bl3-proposal-confirmed-2026-09-27.md')
for o_ in (OUT_J, OUT_C):
    assert not os.path.exists(o_), '既にある（一度だけ）: ' + o_
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True)
FINAL, C_PROP = 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', '1ac0e4b'
U = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))
hits = [m for m in U if 'それでは、D252 のとおりに進めてください' in m[2]]
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, words = hits[0]
words = words.strip()
assert NL not in words, '登録者の言葉に改行がある（状態の行は一行）'
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'AppData', 'Users', 'Temp', '「', '」'):
    assert bad not in words, '登録者の言葉に印か道筋か鉤括弧が入っている: %s' % bad
raw = git('show', '%s:%s' % (C_PROP, FINAL)).stdout
assert raw, '確認していただいた案がコミットに無い'
now = open(os.path.join(REPO, *FINAL.split('/')), 'rb').read()
assert now == raw, '置き場の最終版の案が、push したコミットの案と違う（止める）'
s16 = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
rl = git('reflog', 'show', 'refs/remotes/origin/main', '--date=iso').stdout.decode('utf-8')
m_push = re.search(r'^%s refs/remotes/origin/main@\{(\S+ \S+) \+0900\}: update by push' % C_PROP, rl, re.M)
assert m_push and m_push.group(1) < jst(ts) + ':59', '確認していただいた案の push が、登録者の言葉の前に無い'
J = {'kind': 'bl3_final_confirmation', 'when_jst': jst(ts), 'uuid': uuid, 'words': words,
     'proposal_path': FINAL, 'proposal_commit': C_PROP, 'proposal_sha16': s16, 'proposal_pushed_jst': m_push.group(1),
     'proposal_copy': 'records/Bl3/results-Bl3-proposal-confirmed-2026-09-27.md',
     'source': '登録者の発言（会話の記録から機械で切り出した）・登録者裁定 D252',
     'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
open(OUT_C, 'wb').write(raw)
json.dump(J, open(OUT_J, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('wrote', os.path.basename(OUT_J), '|', jst(ts), uuid, '| words', len(words), '| proposal', C_PROP, s16, 'pushed', m_push.group(1), '| copy', os.path.basename(OUT_C))
