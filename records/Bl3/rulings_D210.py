# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D210（封印の時）の記録を書く（2026-09-24・草案1 の push の後・設計の巡の一巡目の前）。
登録者の言葉と、裁定の前にコーディネータが示した推奨（同じ返信の「封印の時」の段だけ）は、会話の記録から機械で切り出す（手で打たない）。
承認された形の正本の文（草案1 の正本の `predictions.when`・`predictions.if_stopped`・`review_plan.order`）は正本から機械で読む。
既にある記録には書かない。
用法: python records/Bl3/rulings_D210.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D210.md')
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
appr = one(lambda m: m[0] == 'user' and len(m[3]) < 800 and '封印の時はご推奨どおりで' in m[3] and '1323c82' in m[3])
A0, A1 = '**1. 封印の時（D210 として裁定をお願いしたい点）**', '**2. B-lens から改めた三つの数え方'
rec = one(lambda m: m[0] == 'assistant' and A0 in m[3] and A1 in m[3] and m[2] < appr[2])
assert rec[3].count(A0) == 1 and rec[3].count(A1) == 1
excerpt = rec[3][rec[3].index(A0):rec[3].index(A1)].rstrip()
T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
P = T3['predictions']
q1 = P['items'][0]['key']
order = T3['review_plan']['order']
i_fr, i_seal, i_pilot, i_main = [order.index(x) for x in order if x.startswith(('下見の前の凍結', '封印', '下見（', '本の凍結'))]
assert i_fr < i_seal < i_pilot < i_main, order
pushed = git('rev-parse', '--short', 'origin/main')
w = lambda m: m[3].strip().replace(NL, ' ')
RUL = ('D210', '**封印の時**: 予想の封印は下見の前に置く（封印の順——コーディネータが先に封印して SHA だけを伝え、登録者はそれを開かずに封印する——は裁定 D148 のまま）。'
       '正本の凍結は二つに分ける。下見の前の凍結で、正本のすべて・方向の npz・器を凍結して記録先行で公開し、本の凍結で、下見の記録と機械の決定（外した行・近道を使うか）を凍結の記録に足す。'
       '`%s` は残す。下見で止まったときは `%s` だけを採点し、ほかの項目は開いて並べるだけにする（採点しない）。形は草案1 の正本のとおり（下の逐語）' % (q1, q1))
R = ['# 登録者裁定 D210（2026-09-24・B-lens 層三・封印の時）', '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (appr[1], jst(appr[2]), w(appr)),
     '- 「ご推奨」は、草案1 の報告の返信（会話の記録 uuid `%s`・%s 日本時間）の「封印の時」の段で、コーディネータが推奨した形（下の抜き書き）。' % (rec[1], jst(rec[2])),
     '- 前提: 登録者裁定 D205（下見は凍結の前・手順と止める条件は下見の前に凍結）と D209（封印の順は B-lens と同じ・返信に予想の中身を書かない・登録者の予想は固まった時点で SHA）は、封印と下見の前後を決めていなかった（草案1 の §16）。', '',
     '| 裁定 | 中身 |', '|---|---|', '| %s | %s |' % RUL, '',
     '## 承認された形の正本の文（草案1 の正本 `design/contrasts-Bl3.json`・SHA16 %s・機械で読んだ逐語）' % s16('design/contrasts-Bl3.json'), '',
     '- `predictions.when`: %s' % P['when'],
     '- `predictions.if_stopped`: %s' % P['if_stopped'],
     '- `review_plan.order` の該当の四つ（この順）: %s' % ' → '.join(order[k] for k in (i_fr, i_seal, i_pilot, i_main)), '',
     '## 裁定の前にコーディネータが示した推奨（抜き書き・逐語・会話の記録 uuid `%s`）' % rec[1], '', '````text', excerpt, '````', '',
     '## 注（事実のみ）', '',
     '- 抜き書きは、同じ返信の「封印の時」の段の見出しから次の段の見出しの前までを、器が切り出したもの。同じ返信のほかの段は、この裁定の中身ではないので抜いた（会話の記録の uuid で全体を辿れる）。',
     '- 同じ言葉で、登録者は草案1 のコミット 1323c82 の push と、設計の巡（一巡目）の依頼の束の準備を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 記帳の置き場: 正本の `decisions` への D210 の記帳は草案2 で行う。草案1 は、設計の巡（一巡目）の束に入れたまま変えない。',
     '- 番号: 次の裁定は D211 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| approval', jst(appr[2]), appr[1], '| recommendation', jst(rec[2]), rec[1], '| excerpt', len(excerpt), '字 | origin/main', pushed)
