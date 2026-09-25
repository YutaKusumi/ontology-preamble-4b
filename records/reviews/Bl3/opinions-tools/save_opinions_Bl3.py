# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器についての意見伺い（登録者裁定 D230）で、登録者が会話で渡した四名のご意見を、会話の記録から機械で切り出して逐語で保全する。
- 登録者の言葉（作業の途中に届いた形・会話の記録の `attachment` の `queued_command`）を、呼び名の区切り（「Geminiさん（一人目）」など）で四つに割る。区切りはちょうど一度ずつ当たること。
- 各ご意見は `<札>/opinion.md` に、頭の注（機械の書き足し）と逐語の本文で書く。本文は一字も変えない。既にあるファイルには書かない（一度だけ）。
- Gemini の二名の本文の中の機種の申告は本文から機械で拾い、登録者の言葉の機種名（登録者が Google AI Studio のモデル選択で確かめた）と並べて頭の注に書く。
- C2 の方の確かめの台本（登録者の添付・`C:/Users/PC/Downloads/opinion_checks_Bl3.py`）は、バイトのまま `c2/opinion_checks_Bl3.py` に写す。
用法: python records/reviews/Bl3/opinions-tools/save_opinions_Bl3.py <会話の記録 jsonl> <添付の台本>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, shutil, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
KEY = '「Gemini 1.5 Pro」「Gemini 2.5 Pro」'
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    a = o.get('attachment') if o.get('type') == 'attachment' else None
    if isinstance(a, dict) and a.get('type') == 'queued_command' and (a.get('origin') or {}).get('kind') == 'human' and KEY in str(a.get('prompt')):
        hits.append((o.get('uuid'), a.get('source_uuid'), a.get('timestamp'), a['prompt']))
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, src_uuid, ts, text = hits[0]
MK = [('G1', 'Geminiさん（一人目）' + NL + '「'), ('G2', '」' + NL + 'Geminiさん（二人目）' + NL + '「'), ('C1', '」' + NL + 'Claudeさん（一人目）' + NL + '「'),
      ('C2', '」' + NL + 'Claudeさん（二人目\u3000確かめに使った台本は、別添に付けた opinion_checks_Bl3.py です）' + NL + '「')]
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
m = re.search(r'Gemini 3\.8 Flash 二名（[^）]*）', head)
reg_model = m.group(0) if m else None
assert reg_model, '登録者の言葉の機種の段が見つからない'
WHO = {'G1': ('系統外', '一人目'), 'G2': ('系統外', '二人目'), 'C1': ('起草者と同じ Claude 系・claude.ai の Claude Opus 5.5', '一人目'), 'C2': ('起草者と同じ Claude 系・claude.ai の Claude Opus 5.5', '二人目')}
out = {}
for lab in ('G1', 'G2', 'C1', 'C2'):
    d = os.path.join(HERE, lab.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'opinion.md')
    assert not os.path.exists(p), '既にある（一度だけ）: ' + p
    note = ''
    if lab.startswith('G'):
        mm = re.search(r'\*\*機種\*\*: ([^\n（]+)', seg[lab])
        note = '本文の中の機種の申告は「%s」。登録者の言葉では「%s」（登録者の言葉は逐語・下の出所）。' % ((mm.group(1).strip() if mm else '（申告の行が無い）'), reg_model)
    hdr = ['<!-- 逐語保全: 器についての意見伺い（登録者裁定 D230・巡に数えない）・%s・%s（呼び名 %s）。%s' % (WHO[lab][0], WHO[lab][1], lab, note),
           '     登録者（楠見優太）が会話で渡したご意見を、会話の記録から機械で切り出した（作業の途中に届いた形の登録者の言葉・uuid %s・元の uuid %s・%s 日本時間）。' % (uuid, src_uuid, jst(ts)),
           '     この枠の外は一字も変えていない。本意見のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->']
    open(p, 'w', encoding='utf-8', newline=NL).write(NL.join(hdr) + NL + seg[lab])
    out[lab] = {'path': os.path.relpath(p, HERE).replace(os.sep, '/'), 'chars': len(seg[lab]), 'sha16_body': sha256b(seg[lab].encode('utf-8'))[:16]}
hp = os.path.join(HERE, 'registrant-message-head.md')
assert not os.path.exists(hp)
open(hp, 'w', encoding='utf-8', newline=NL).write('<!-- 逐語保全: 登録者の言葉の頭（ご意見の前の段・uuid %s・%s 日本時間）。この枠の外は一字も変えていない。 -->' % (uuid, jst(ts)) + NL + head)
sp = os.path.join(HERE, 'c2', 'opinion_checks_Bl3.py')
assert not os.path.exists(sp)
shutil.copyfile(sys.argv[2], sp)
assert open(sp, 'rb').read() == open(sys.argv[2], 'rb').read()
idx = ['# 器についての意見伺い（登録者裁定 D230）の保全の索引（機械生成・`save_opinions_Bl3.py`）', '',
       '- 出所: 会話の記録の登録者の言葉（uuid %s・%s 日本時間）。本文は区切りで割っただけで、一字も変えていない。' % (uuid, jst(ts)), '',
       '| 札 | 置き場 | 字数 | 本文の SHA16 |', '|---|---|---|---|'] + ['| %s | `%s` | %d | %s |' % (lab, v['path'], v['chars'], v['sha16_body']) for lab, v in out.items()] + [
       '', '- 登録者の言葉の頭: `registrant-message-head.md`。', '- C2 の方の確かめの台本（登録者の添付）: `c2/opinion_checks_Bl3.py`（SHA-256 %s・バイトのまま写した）。' % sha256b(open(sp, 'rb').read()),
       '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
ip = os.path.join(HERE, 'opinions-index.md')
assert not os.path.exists(ip)
open(ip, 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('saved', {k: (v['chars'], v['sha16_body']) for k, v in out.items()}, '| model note', reg_model)
