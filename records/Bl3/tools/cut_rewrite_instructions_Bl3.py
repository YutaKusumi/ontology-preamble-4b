# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の独立の再計算の、残差の書き換えの道の書き手（系統内の新しい個体）に渡した指示の文を、会話の記録から機械で切り出して記録に置く
（器についての意見伺いの C1-A2・裁定 D231）。手で打たない。既にある記録には書かない。
用法: python records/Bl3/tools/cut_rewrite_instructions_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
OUT = os.path.join(HERE, 'recompute-rewrite-instructions-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'assistant':
        continue
    for c in (o.get('message') or {}).get('content') or []:
        if isinstance(c, dict) and c.get('type') == 'tool_use' and c.get('name') == 'Agent':
            hits.append((o, c))
if len(hits) != 1:
    raise SystemExit('書き手を呼んだ記録が一つに決まらない: %d' % len(hits))
o, c = hits[0]
inp = c['input']
pr = inp['prompt']
tg, sr = 'pasted' + '_content', 'system' + '-reminder'           # 印の字面を器の文に残さない
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
    assert bad not in pr, '貼り付けの印か系統の印が入っている'
assert '````' not in pr
sha = hashlib.sha256(pr.encode('utf-8')).hexdigest().upper()
R = ['# 残差の書き換えの道の書き手に渡した指示の文（機械で切り出した・B-lens 層三・%s）' % jst(o['timestamp'])[:10], '',
     '- 出所: 会話の記録の uuid `%s`・呼び出しの番号 `%s`・%s 日本時間（%s）。' % (o['uuid'], c['id'], jst(o['timestamp']), o['timestamp']),
     '- 呼び出しの引数（指示の文のほか・逐語）: %s。' % '・'.join('%s = %s' % (k, inp[k]) for k in sorted(inp) if k != 'prompt'),
     '- 指示の文の SHA-256（UTF-8）: %s・%d 字。' % (sha, len(pr)),
     '- 書き手が書いたもの: `tools/bl3_recompute_rewrite.py`・`records/Bl3/tools/recompute-rewrite-dev-Bl3.md`（コーディネータの取り込みと確かめは `records/Bl3/tools/tools-log-Bl3.md` の 7）。',
     '- 置いた理由: 器についての意見伺いの C1-A2（書き手に渡した指示の文が記録に無い）を採った（裁定 D231）。器の実装の検分者が、指示と正本と書き手の器を突き合わせられるように。', '',
     '## 指示の文（逐語）', '', '````text', pr, '````', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('[cut_rewrite_instructions_Bl3] wrote %s（指示の文 %d 字・SHA-256 の頭 %s）' % (os.path.relpath(OUT, os.path.dirname(os.path.dirname(os.path.dirname(HERE)))), len(pr), sha[:16]))
