# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D242 の記録を書く（下見の前の凍結の後の確かめで見つけた外れ〔凍結物の数の検査の記録の一行の一時の置き場の道筋〕の扱い）。
登録者の言葉と、裁定の候補の文（コーディネータの返信の「裁定 D242 のお伺い」の区画）は、会話の記録から機械で切り出す（手で打たない）。
候補の文は公開した記録に無く、コーディネータの返信にだけあったので、返信の区画をそのまま置く。採られた案: A（推奨の案）。既にある記録には書かない。
用法: python records/Bl3/rulings_D242.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D242.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout
U, A = [], []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))
    elif o.get('type') == 'assistant' and isinstance(c, list):
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'text':
                A.append((o.get('uuid'), o.get('timestamp'), x.get('text', '')))
hits = [m for m in U if '裁定 D242 は、ご推奨の A を承認いたします' in m[2]]
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, words = hits[0]
HEAD_ = '**裁定 D242 のお伺い（どう扱うか）**'
ah = [m for m in A if HEAD_ in m[2]]
assert len(ah) == 1, ('候補を書いた返信が一つに決まらない', len(ah))
a_uuid, a_ts, a_text = ah[0]
assert a_ts < ts, '候補の返信が登録者の言葉より後にある'
L = a_text.split(NL)
i0 = [i for i, l in enumerate(L) if l.strip() == HEAD_]
i1 = [i for i, l in enumerate(L) if l.startswith('**別件')]
assert len(i0) == 1 and len(i1) == 1 and i0[0] < i1[0], (i0, i1)
opts = [l for l in L[i0[0] + 1:i1[0]] if l.strip()]
assert [l[:7] for l in opts[:3]] == ['- **A（推', '- **B**', '- **C（勧'] and len(opts) == 5, opts
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for t in [words] + opts:
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
        assert bad not in t, '貼り付けの印か系統の印が入っている'
    for bad in ('AppData', 'Users', 'Temp'):
        assert bad not in t, '手元の道筋が入っている'
c_fz = git('log', '--diff-filter=A', '--format=%H', '-1', '--', 'records/Bl3/FREEZE-RECORD-Bl3.json').strip()
assert len(c_fz) == 40, '凍結の記録を足したコミットが無い'
pushed = git('rev-parse', '--short', 'origin/main').strip()
in_origin = subprocess.run(['git', 'merge-base', '--is-ancestor', c_fz, 'origin/main'], cwd=REPO).returncode == 0
R = ['# 登録者裁定 D242（%s・B-lens 層三・下見の前の凍結の後の確かめで見つけた外れの扱い）' % jst(ts)[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.strip().replace(NL, ' ')),
     '- 採られた案: A（推奨の案）。候補の文は公開した記録に無く、コーディネータの返信（会話の記録 uuid `%s`・%s 日本時間）の「裁定 D242 のお伺い」の区画にだけあったので、その区画を逐語で下に置く。'
     % (a_uuid, jst(a_ts)), '',
     '## 裁定の候補（逐語・コーディネータの返信の区画）', ''] + opts + ['',
     '## 裁定', '',
     '- **D242**: 下見の前の凍結の凍結物は、凍結したとおりにコミットし、逸脱は立てない。凍結物の数の検査の記録（`records/Bl3/numbers-lint-FROZEN-Bl3.md`）の一行に、'
     '代わりの原稿の一時の置き場の道筋が残ったこと（裁定 D239 の直しの漏れ）は、凍結の後の確かめの記録（`records/Bl3/prepilot-freeze-check-Bl3.md`）に書く。', '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者は、凍結の言葉の記録（`records/Bl3/prepilot-freeze-words-Bl3.md`）にある Colab のプランとユニットの数を公開して差し支えないとした。',
     '- 凍結したとおりのコミット: %s（この記録を書いた時点で origin/main %s に%s）。push は登録者のお許しの後。' % (c_fz, pushed, '入っている' if in_origin else 'まだ入っていない'),
     '- D242 は下見の前の凍結の後の裁定なので、凍結した正本の `decisions` には入らない（正本は凍結物）。凍結の前の確かめだけの走り（`tools/freeze_Bl3.py prepilot --check-only`）は、'
     '裁定の記録（`records/Bl3/rulings-D*.md`）の名にある番号が正本の `decisions` にあり、正本の次の裁定の番号がその次であることを照らすので、この記録を置いた後に走らせると、その二つを外れとして出す。'
     'この走りは凍結の前のためのもので、本の凍結の相（`main`）はこの照らしをしない（B-lens でも、凍結の後の裁定の記録を同じ名の型で置いた）。',
     '- 番号: 次の裁定は D243 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| words', jst(ts), uuid, '| options from reply', jst(a_ts), '| freeze commit', c_fz[:7], '| origin/main', pushed, '| in origin', in_origin)
