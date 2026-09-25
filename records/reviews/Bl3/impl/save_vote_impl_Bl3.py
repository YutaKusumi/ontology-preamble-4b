# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器の実装の検分（正本 `review_plan.impl`）の票を、検分者の記録（検分者の会話の記録の JSONL）の最後の本文から機械で切り出して逐語で保全する。
- 本文は一字も変えない。頭の注（機械の書き足し）と本文を `<札>/review.md` に一度だけ書く（既にあれば書かない）。
- 会話の記録に届いた終わりの通知の本文（XML の文字の置き換えを戻したもの）と突き合わせ、同じかを頭の注と付けの記録に書く。
- 検分者の記録の機種の欄と、通知の使った量（トークン・時間）を付けの記録 `<札>/meta.json` に書く。検分者の内部の番号は記録に書かない。
用法: python records/reviews/Bl3/impl/save_vote_impl_Bl3.py <札 R1|R2> <検分者の記録 jsonl> <会話の記録 jsonl> <検分者の内部の番号（通知を探すためだけに使う）>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, html, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
tag, sub_path, sess_path, agent_ref = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert tag in ('R1', 'R2')
ROLE = {'R1': '計算の側', 'R2': '流れと記録の側'}
last, models = None, set()
for line in open(sub_path, encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'assistant':
        continue
    msg = o.get('message') or {}
    if msg.get('model'):
        models.add(msg['model'])
    parts = [x.get('text') for x in (msg.get('content') or []) if isinstance(x, dict) and x.get('type') == 'text' and x.get('text')]
    if parts:
        last = (o.get('uuid'), o.get('timestamp'), ''.join(parts))
assert last, '検分者の記録に本文が無い'
uuid, ts, body = last
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
    assert bad not in body, '貼り付けの印か系統の印が入っている'
# 終わりの通知の本文と突き合わせる
notes = []


def walk(v):
    if isinstance(v, str):
        if '<task-id>%s</task-id>' % agent_ref in v and '<result>' in v:
            notes.append(v)
    elif isinstance(v, dict):
        for x in v.values():
            walk(x)
    elif isinstance(v, list):
        for x in v:
            walk(x)


for line in open(sess_path, encoding='utf-8'):
    try:
        walk(json.loads(line))
    except Exception:
        continue
res = sorted({html.unescape(n.split('<result>', 1)[1].split('</result>', 1)[0]) for n in notes})
usage = {}
for n in notes:
    for k in ('subagent_tokens', 'tool_uses', 'duration_ms'):
        m = re.search(r'<%s>(\d+)</%s>' % (k, k), n)
        if m:
            usage[k] = int(m.group(1))
match = bool(res) and all(r.strip() == body.strip() for r in res)
d = os.path.join(HERE, tag.lower())
os.makedirs(d, exist_ok=True)
p = os.path.join(d, 'review.md')
assert not os.path.exists(p), '既にある（一度だけ）: ' + p
hdr = ['<!-- 逐語保全: 器の実装の検分（正本 review_plan.impl）・系統内の新しい個体（機種の欄 %s）・検分者 %s（%s）。' % ('・'.join(sorted(models)) or '記録に無い', tag, ROLE[tag]),
       '     検分者の会話の記録の最後の本文（uuid %s・%s 日本時間）から機械で切り出した（`save_vote_impl_Bl3.py`）。会話の記録に届いた終わりの通知の本文（XML の文字の置き換えを戻したもの）と%s。' % (
           uuid, jst(ts), '同じ' if match else ('違う（通知 %d 件）' % len(res))),
       '     この枠の外は一字も変えていない。本検分のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->']
open(p, 'w', encoding='utf-8', newline=NL).write(NL.join(hdr) + NL + body)
meta = {'tag': tag, 'role': ROLE[tag], 'final_message_uuid': uuid, 'final_message_utc': ts, 'models': sorted(models), 'body_chars': len(body),
        'body_sha256': sha256b(body.encode('utf-8')), 'notification_count': len(res), 'notification_body_same': match, 'usage': usage,
        'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
mp = os.path.join(d, 'meta.json')
assert not os.path.exists(mp)
json.dump(meta, open(mp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('[save_vote_impl_Bl3] %s: %d 字・本文の SHA-256 の頭 %s・通知と%s・機種 %s・使った量 %s' % (tag, len(body), meta['body_sha256'][:16], '同じ' if match else '違う', sorted(models), usage))
