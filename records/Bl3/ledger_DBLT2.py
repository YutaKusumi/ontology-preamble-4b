# -*- coding: utf-8 -*-
"""逸脱 D-BLT2（最終の系統外の検分の票の数）を、凍結の記録の逸脱台帳に記す（登録者裁定 D247・2026-09-27・B-lens の逸脱 D-BL5 の型）。
承認の言葉は裁定 D247〜D250 の記録から機械で写す（手で打たない）。台帳は後ろに足すだけで、前の行を書き換えない（凍結の記録 deviation_rule）。既に記してあれば止める。
用法: python records/Bl3/ledger_DBLT2.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
FR_JSON, FR_MD = os.path.join(HERE, 'FREEZE-RECORD-Bl3.json'), os.path.join(HERE, 'FREEZE-RECORD-Bl3.md')
FR = json.load(open(FR_JSON, encoding='utf-8'))
assert [d['no'] for d in FR['deviations']] == ['D-BLT1'], [d['no'] for d in FR['deviations']]
rul = open(os.path.join(HERE, 'rulings-D247-D250.md'), encoding='utf-8').read()
m = re.search(r'- 登録者の言葉（逐語・会話の記録 uuid `([^`]+)`・([^ ]+ [^ ]+) 日本時間）: 「(.*)」', rul)
assert m, '裁定の記録の登録者の言葉が読めない'
dev = {'no': 'D-BLT2', 'date': m.group(2).split(' ')[0],
       'what': ('**最終の系統外の検分の票の数**。正本 `review_plan.final.external` と枠（`records/reviews/Bl3/results-final/frame-results-final-Bl3.md`）は、最終を系統外の一票とした。'
                '登録者は最終検分を新しい個体の二名（Google AI Studio で Gemini 3.8 Flash を選んだ）に依頼し、二票になった（F1 は条件つき可・F2 は公開可）。二票をともに最終検分とし、所見は和集合で受けた。'
                '記録 `records/Bl3/rulings-D247-D250.md`・採否の案 `records/reviews/Bl3/results-final/adoption-final-Bl3.md`'),
       'scope': '最終検分の組み立てだけ（同じ機種を選んだ二票は、会話が別でも相関しうるので、独立の重みを二倍には数えない）。報告の札と数は変えない',
       'approval': '登録者裁定 D247（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」・記録 `records/Bl3/rulings-D247-D250.md`）' % (m.group(2), m.group(1), m.group(3))}
FR['deviations'].append(dev)
json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
anchor = [l for l in md.split(NL) if l.startswith('| D-BLT1 |')]
assert len(anchor) == 1 and '| D-BLT2 |' not in md, '台帳の行の形が想定と違う'
row = '| %s | %s | %s | %s | %s |' % (dev['no'], dev['date'], dev['what'].replace('|', '｜'), dev['scope'], dev['approval'].replace('|', '｜'))
md = md.replace(anchor[0], anchor[0] + NL + row, 1)
open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md)
print('ledgered', dev['no'], dev['date'], '| approval words', m.group(2), m.group(1))
