# -*- coding: utf-8 -*-
"""逸脱 D-BLT1（報告の表し方・結果の巡の後）を、凍結の記録の逸脱台帳に記す（登録者裁定 D243・D246・2026-09-27・B-lens の `records/Blens/ledger_DBL3_DBL4.py` の型）。
- 承認の言葉は裁定 D243〜D246 の記録から機械で写す（手で打たない）。台帳は後ろに足すだけで、前の行を書き換えない（凍結の記録 deviation_rule）。
- 凍結の記録の SHA16 は報告の頭に印字されるので、逸脱の器と草案の二つ目の SHA16 は台帳に入れない（入れると互いに決まらない）。二つの SHA16 は草案の二つ目の頭の区画と確かめの記録に置く。
- 凍結した組み立ての器の逸脱の印の口（`--marks`）に渡す印の JSON（`records/Bl3/report-marks-Bl3.json`）も書く（印の区画を足す節の鍵）。
- 既に記してあれば止める。
用法: python records/Bl3/ledger_DBLT1.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
sys.path.insert(0, os.path.join(REPO, 'tools'))
import build_report_Bl3 as BR

FR_JSON, FR_MD = os.path.join(HERE, 'FREEZE-RECORD-Bl3.json'), os.path.join(HERE, 'FREEZE-RECORD-Bl3.md')
MARKS = os.path.join(HERE, 'report-marks-Bl3.json')
assert not os.path.exists(MARKS), '既にある: ' + MARKS
FR = json.load(open(FR_JSON, encoding='utf-8'))
assert FR['deviations'] == [], ('台帳が空でない', [d.get('no') for d in FR['deviations']])
rul = open(os.path.join(HERE, 'rulings-D243-D246.md'), encoding='utf-8').read()
m = re.search(r'- 登録者の言葉（逐語・会話の記録 uuid `([^`]+)`・([^ ]+ [^ ]+) 日本時間）: 「(.*)」', rul)
assert m, '裁定の記録の登録者の言葉が読めない'
approval = '登録者裁定 D243・D246（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」・記録 `records/Bl3/rulings-D243-D246.md`）' % (m.group(2), m.group(1), m.group(3))
dev = {'no': 'D-BLT1', 'date': m.group(2).split(' ')[0],
       'what': ('**報告の表し方（結果の巡の後）**。凍結した組み立ての器 `tools/build_report_Bl3.py` の出力は、升目の名の縦棒が表の区切りと重なって表示で列がずれ、見出しと状態の行が結果の巡の後の状態と合わず、'
                '四票が求めた注（起草者の欄の数・唯一の等方の外の行の升目の事情と札の余白・§3・§5・§6・§7 の注）を置く口を持たない（結果の巡の採否の案 `records/reviews/Bl3/results-round1/adoption-results-Bl3.md`）。'
                '逸脱の下の器 `tools/build_report_Bl3_devBLT1.py` は、凍結した器を読み込み、同じ入力で凍結の報告を作り直して置き場の報告とバイトで同じことを確かめてから、見出しと状態の行を改め、'
                '印を付けた機械の区画（表の前の断りと並べ直しの表・注・検分票）を足す。凍結の報告の文と区画は、見出しと状態の行のほか変えない。出力 `records/Bl3/results-Bl3-draft2.md`'),
       'scope': '報告の表し方だけ（札・門・読みの型・予想の照合の判定と、凍結した器・正本・凍結の本文・凍結物は変えない）',
       'approval': approval,
       'files': [{'path': 'tools/build_report_Bl3_devBLT1.py'}, {'path': 'records/Bl3/results-Bl3-draft2.md'}]}
FR['deviations'].append(dev)
json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
fence = [l for l in md.split(NL) if l.startswith('本記録のいかなる数値も')]
assert len(fence) == 1 and '## 凍結の後の逸脱の台帳' not in md, '台帳の節が既にあるか、柵の行が一つでない'
sec = NL.join(['## 凍結の後の逸脱の台帳（凍結の記録 `deviations` の写し・台帳は後ろに足すだけ）', '',
               '| 番号 | 日付 | 何を | 範囲 | 承認 |', '|---|---|---|---|---|',
               '| %s | %s | %s | %s | %s |' % (dev['no'], dev['date'], dev['what'].replace('|', '｜'), dev['scope'], dev['approval'].replace('|', '｜')), '', ''])
md = md.replace(fence[0], sec + fence[0], 1)
open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md)
marks = {k: [dev['no']] for k in ('summary', 'pilot', 'main', 'gate', 'recompute', 'predictions', 'limits')}
assert set(marks) <= set(BR.SECTIONS), set(marks) - set(BR.SECTIONS)
json.dump(marks, open(MARKS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('ledgered', dev['no'], dev['date'], '| marks', sorted(marks), '| approval words', m.group(2), m.group(1))
