# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の登録者裁定 D239〜D241 の記録を書く（器の直しの確かめ〔裁定 D238〕の採否の案への裁定）。
登録者の言葉は会話の記録から、裁定の候補の文は公開した採否の案（コミット d78d33d の `records/reviews/Bl3/fixcheck/adoption-fixcheck-Bl3.md` の §4）から、機械で切り出す（手で打たない）。
採られた案: どれも甲（推奨の案）。既にある記録には書かない。
用法: python records/Bl3/rulings_D239_D241.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
OUT = os.path.join(HERE, 'rulings-D239-D241.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout
M = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        M.append((o.get('uuid'), o.get('timestamp'), c))
hits = [m for m in M if 'ご推奨の案を承認いたします' in m[2] and 'D241（直した後の外の目）' in m[2] and 'd78d33d' in m[2]]
assert len(hits) == 1, ('登録者の言葉が一つに決まらない', len(hits))
uuid, ts, words = hits[0]
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>'):
    assert bad not in words, '貼り付けの印か系統の印が入っている'
SRC = 'd78d33d'
ad = git('show', '%s:records/reviews/Bl3/fixcheck/adoption-fixcheck-Bl3.md' % SRC)
opts = [l for l in ad.split(NL) if l.startswith(('- **D239', '- **D240', '- **D241', '- 利益相反の記録: 私は進める側'))]
assert [l[:9] for l in opts[:3]] == ['- **D239（', '- **D240（', '- **D241（'] and len(opts) == 4, opts
pushed = git('rev-parse', '--short', 'origin/main').strip()
R = ['# 登録者裁定 D239〜D241（%s・B-lens 層三・器の直しの確かめの採否の案への裁定）' % jst(ts)[:10], '',
     '- 登録者の言葉（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.strip().replace(NL, ' ')),
     '- 採られた案: D239・D240・D241 のどれも甲（推奨の案）。候補の文は、公開した採否の案（コミット %s の `records/reviews/Bl3/fixcheck/adoption-fixcheck-Bl3.md` の §4）から逐語で下に置く。' % SRC, '',
     '## 裁定の候補（逐語・採否の案の §4）', ''] + opts + ['',
     '## 裁定', '',
     '- **D239**: 採否の案の A の表（凍結の前に器を直す）をすべて直す。直すと器と正本の SHA16 が変わるので、合成データの正式の記録を取り直す（C1 と C2 の条件の確かめを入れる）。',
     '- **D240**: 採否の案の B の表（記録に置く）と C の表（採らない）を案のとおりにする。下見が器の誤りで終わり、やり直さないと決めたときの閉じ方は、器に道を作らず記録に置く（そのときは登録者の裁定のもとで、閉じる記録を逸脱として記す）。',
     '- **D241**: 直した後に、さらなる検分の巡を置かない。直して正式の記録を取り直し、Colab の相 check の段へ進む。理由は上の登録者の言葉のとおり（逐語）。', '',
     '## 注（事実のみ）', '',
     '- 同じ言葉で、登録者はローカルのコミット d78d33d の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は %s）。' % pushed,
     '- 記帳の置き場: 正本の `decisions` への D239〜D241 の記帳は、直しの後の正本（生成器 v9）で行う。', '- 番号: 次の裁定は D242 から。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote', os.path.basename(OUT), '| words', jst(ts), uuid, '| options from', SRC, '| origin/main', pushed)
