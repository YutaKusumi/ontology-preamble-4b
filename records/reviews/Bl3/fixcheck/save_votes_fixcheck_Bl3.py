# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器の直しの確かめ（登録者裁定 D238・正本 `review_plan.impl_recheck`）で、登録者が会話で渡した四名の票を、会話の記録から機械で切り出して逐語で保全する
（意見伺いの保全の器 `records/reviews/Bl3/opinions-tools/save_opinions_Bl3.py` の型）。
- 登録者の言葉（会話の記録の `user` の行・中身は文字列）を、呼び名の区切り（「Geminiさん（一人目）」など）で四つに割る。区切りはちょうど一度ずつ当たること。
- 各票は `<札>/vote.md` に、頭の注（機械の書き足し）と逐語の本文で書く。本文は一字も変えない。既にあるファイルには書かない（一度だけ）。
- Gemini の二名の本文の中の機種と系統の申告は本文から機械で拾い、登録者の言葉の機種名と並べて頭の注に書く（枠: Gemini の方々の機種は登録者の確認を正とする）。
用法: python records/reviews/Bl3/fixcheck/save_votes_fixcheck_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
NAMES = ['Geminiさん（一人目）', 'Geminiさん（二人目）', 'Claudeさん（一人目）', 'Claudeさん（二人目）']
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user' or 'toolUseResult' in o:
        continue
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str) and all(n in c for n in NAMES) and '登録者裁定 D238' in c:
        hits.append((o.get('uuid'), o.get('timestamp'), c))
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, text = hits[0]
for bad in ('<pasted', 'pasted_content', '<system', 'antml'):
    assert bad not in text, ('貼り付けの印が入っている', bad)
MK = [('G1', NAMES[0] + NL + '「'), ('G2', '」' + NL + NAMES[1] + NL + '「'), ('C1', '」' + NL + NAMES[2] + NL + '「'), ('C2', '」' + NL + NAMES[3] + NL + '「')]
pos = []
for lab, mk in MK:
    assert text.count(mk) == 1, ('区切りがちょうど一度でない', lab, text.count(mk))
    pos.append((lab, text.index(mk), len(mk)))
assert [p for _, p, _ in pos] == sorted(p for _, p, _ in pos)
assert text.endswith('」')
head = text[:pos[0][1]]
seg = {}
for k, (lab, p, n) in enumerate(pos):
    end = pos[k + 1][1] if k + 1 < len(pos) else len(text) - 1
    seg[lab] = text[p + n:end]
    assert seg[lab].strip(), lab
assert head + ''.join(mk + seg[lab] for (lab, mk) in MK) + '」' == text, '割った後に組み直すと元の言葉にならない'
m = re.search(r'新規のGemini [^二]*二名', head)
reg_model = m.group(0) if m else None
assert reg_model, '登録者の言葉の機種の段が見つからない'
WHO = {'G1': ('系統外', '一人目'), 'G2': ('系統外', '二人目'),
       'C1': ('起草者と同じ Claude 系・claude.ai の Claude Opus 5.5（二名で一票）', '一人目'), 'C2': ('起草者と同じ Claude 系・claude.ai の Claude Opus 5.5（二名で一票）', '二人目')}
out = {}
for lab in ('G1', 'G2', 'C1', 'C2'):
    d = os.path.join(HERE, lab.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'vote.md')
    assert not os.path.exists(p), '既にある（一度だけ）: ' + p
    note = ''
    if lab.startswith('G'):
        mm = re.search(r'\*\*機種\*\*: ([^\n]+)', seg[lab])
        ml = re.search(r'\*\*系統\*\*: ([^\n]+)', seg[lab])
        note = '本文の中の機種の申告は「%s」、系統の申告は「%s」。登録者の言葉では「%s」（登録者の言葉は逐語・下の出所）。' % (
            (mm.group(1).strip() if mm else '（機種の申告の行が無い）'), (ml.group(1).strip() if ml else '（系統の申告の行が無い）'), reg_model)
    hdr = ['<!-- 逐語保全: 器の直しの確かめ（登録者裁定 D238・正本 review_plan.impl_recheck）・%s・%s（札 %s）。%s' % (WHO[lab][0], WHO[lab][1], lab, note),
           '     登録者（楠見優太）が会話で渡した票を、会話の記録から機械で切り出した（登録者の言葉・uuid %s・%s 日本時間）。' % (uuid, jst(ts)),
           '     この枠の外は一字も変えていない。本票のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->']
    open(p, 'w', encoding='utf-8', newline=NL).write(NL.join(hdr) + NL + seg[lab])
    assert open(p, encoding='utf-8').read().split(NL, len(hdr))[-1] == seg[lab]
    out[lab] = {'path': os.path.relpath(p, HERE).replace(os.sep, '/'), 'chars': len(seg[lab]), 'sha16_body': sha256b(seg[lab].encode('utf-8'))[:16]}
hp = os.path.join(HERE, 'registrant-message-head.md')
assert not os.path.exists(hp)
open(hp, 'w', encoding='utf-8', newline=NL).write('<!-- 逐語保全: 登録者の言葉の頭（票の前の段・uuid %s・%s 日本時間）。この枠の外は一字も変えていない。 -->' % (uuid, jst(ts)) + NL + head)
idx = ['# 器の直しの確かめ（登録者裁定 D238）の票の保全の索引（機械生成・`save_votes_fixcheck_Bl3.py`）', '',
       '- 出所: 会話の記録の登録者の言葉（uuid %s・%s 日本時間）。本文は区切りで割っただけで、一字も変えていない（割った後に組み直すと元の言葉になることを確かめた）。' % (uuid, jst(ts)),
       '- 数え方: claude.ai の二名（C1・C2）は起草者と同じ系列で、二名で一票に数える（裁定 D59 の数え方・枠 `frame-fixcheck-Bl3.md`）。', '',
       '| 札 | 置き場 | 字数 | 本文の SHA16 |', '|---|---|---|---|'] + ['| %s | `%s` | %d | %s |' % (lab, v['path'], v['chars'], v['sha16_body']) for lab, v in out.items()] + [
       '', '- 登録者の言葉の頭: `registrant-message-head.md`。', '',
       '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
ip = os.path.join(HERE, 'votes-index.md')
assert not os.path.exists(ip)
open(ip, 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('saved', {k: (v['chars'], v['sha16_body']) for k, v in out.items()}, '| model note', reg_model)
