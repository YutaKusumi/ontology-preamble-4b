# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の最終の系統外の検分（正本 `review_plan.final`）で、登録者が会話で渡した票を、会話の記録から機械で切り出して逐語で保全する
（結果の巡の保全の器 `records/reviews/Bl3/results-round1/save_votes_results_Bl3.py` の型）。
- 登録者の言葉（会話の記録の `user` の行・中身は文字列）を、呼び名の区切り（「Geminiさん（一人目）」「Geminiさん（二人目）」）で割る。区切りはちょうど一度ずつ当たること。
  結果の巡の言葉（四名の呼び名を持つ）と取り違えないよう、claude.ai の呼び名を持たない言葉だけを拾う。
- 各票は `<札>/vote.md` に、頭の注（機械の書き足し）と逐語の本文で書く。本文は一字も変えない。既にあるファイルには書かない（一度だけ）。
- 票の本文の中の機種と系統の申告は本文から機械で拾い、登録者の言葉の機種の段と並べて頭の注に書く（機種は登録者の言葉を正とする・前の巡と同じ）。
- 正本 `review_plan.final.external` は一票。登録者は二名に依頼したので、票の数は枠と正本と違う（採否の案と裁定で扱う・B-lens の逸脱 D-BL5 の型）。
用法: python records/reviews/Bl3/results-final/save_votes_final_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
NAMES = ['Geminiさん（一人目）', 'Geminiさん（二人目）']
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user' or 'toolUseResult' in o:
        continue
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str) and all(n in c for n in NAMES) and 'モデルの申告がGemini 3.8 Flash' in c and 'Claudeさん（一人目）' not in c:
        hits.append((o.get('uuid'), o.get('timestamp'), c))
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, text = hits[0]
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
    assert bad not in text, ('貼り付けの印か系統の印が入っている', bad)
MK = [('F1', NAMES[0] + NL + '「'), ('F2', '」' + NL + NAMES[1] + NL + '「')]
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
m = re.search(r'新規のGemini [^二]*二名（[^）]*）', head)
reg_model = m.group(0) if m else None
assert reg_model, '登録者の言葉の機種の段が見つからない'
out = {}
for lab in ('F1', 'F2'):
    d = os.path.join(HERE, lab.lower())
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'vote.md')
    assert not os.path.exists(p), '既にある（一度だけ）: ' + p
    mm = re.search(r'\*\*機種\*\*: ([^\n]+)', seg[lab])
    ml = re.search(r'\*\*系統\*\*: ([^\n]+)', seg[lab])
    note = '本文の中の機種の申告は「%s」、系統の申告は「%s」。登録者の言葉では「%s」（機種は登録者の言葉を正とする・逐語は下の出所）。' % (
        (mm.group(1).strip() if mm else '（機種の申告の行が無い）'), (ml.group(1).strip() if ml else '（系統の申告の行が無い）'), reg_model)
    hdr = ['<!-- 逐語保全: 最終の系統外の検分（正本 review_plan.final・新しい個体）・系統外・%s（札 %s）。%s' % ('一人目' if lab == 'F1' else '二人目', lab, note),
           '     登録者（楠見優太）が会話で渡した票を、会話の記録から機械で切り出した（登録者の言葉・uuid %s・%s 日本時間）。' % (uuid, jst(ts)),
           '     この枠の外は一字も変えていない。本票のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。 -->']
    open(p, 'w', encoding='utf-8', newline=NL).write(NL.join(hdr) + NL + seg[lab])
    assert open(p, encoding='utf-8').read().split(NL, len(hdr))[-1] == seg[lab]
    out[lab] = {'path': os.path.relpath(p, HERE).replace(os.sep, '/'), 'chars': len(seg[lab]), 'sha16_body': sha256b(seg[lab].encode('utf-8'))[:16]}
hp = os.path.join(HERE, 'registrant-message-head.md')
assert not os.path.exists(hp)
open(hp, 'w', encoding='utf-8', newline=NL).write('<!-- 逐語保全: 登録者の言葉の頭（票の前の段・uuid %s・%s 日本時間）。この枠の外は一字も変えていない。 -->' % (uuid, jst(ts)) + NL + head)
idx = ['# 最終の系統外の検分の票の保全の索引（機械生成・`save_votes_final_Bl3.py`）', '',
       '- 出所: 会話の記録の登録者の言葉（uuid %s・%s 日本時間）。本文は区切りで割っただけで、一字も変えていない（割った後に組み直すと元の言葉になることを確かめた）。' % (uuid, jst(ts)),
       '- 数え方: 正本 `review_plan.final.external` は系統外の一票。登録者は新しい個体の二名に依頼し、二票になった（F1・F2・扱いは採否の案と裁定）。機種は登録者の言葉を正とする（本文の申告は各票の頭の注）。', '',
       '| 札 | 置き場 | 字数 | 本文の SHA16 |', '|---|---|---|---|'] + ['| %s | `%s` | %d | %s |' % (lab, v['path'], v['chars'], v['sha16_body']) for lab, v in out.items()] + [
       '', '- 登録者の言葉の頭: `registrant-message-head.md`。', '',
       '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
ip = os.path.join(HERE, 'votes-index.md')
assert not os.path.exists(ip)
open(ip, 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('saved', {k: (v['chars'], v['sha16_body']) for k, v in out.items()}, '| words', jst(ts), uuid, '| model note', reg_model)
