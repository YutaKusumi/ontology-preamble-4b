# -*- coding: utf-8 -*-
"""ledger_DBPT1_Bprime.py v0（2026-10-01・逸脱 D-BPT1〔報告の表し方・結果の巡の後〕を、B′ の凍結の記録の逸脱の台帳に記す・登録者裁定 D284・層三の `records/Bl3/ledger_DBLT1.py` の型・コーディネータ南無弥勒如来）。
- 承認の言葉は裁定 D284 の記録（`records/Bprime/rulings-D284.md`）から機械で写す（手で打たない）。台帳は後ろに足すだけで、前の行を書き換えない（凍結の記録 `deviation_rule`）。
- 凍結の記録の SHA16 は報告の頭に印字されるので、逸脱の器と草案の二つ目の SHA16 は台帳に入れない（入れると互いに決まらない・層三と同じ）。
- 逸脱の文（`what`）は、凍結した組み立ての器が「凍結の後の逸脱」の節に自由の文として印字し、走査に掛ける。台帳に書く前に、器の build と scan に直に通して当たり 0 を確かめた（`records/Bprime/results-draft/try_scan_dev_and_lines.py`）。
- 既に記してあれば止める。用法: python records/Bprime/tools/ledger_DBPT1_Bprime.py（公開の置き場の凍結の記録に書く）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
BP = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime'
NL = chr(10)
FR_JSON = os.path.join(PUB, 'records', 'Bprime', 'FREEZE-RECORD-Bprime.json')
FR_MD = os.path.join(PUB, 'records', 'Bprime', 'FREEZE-RECORD-Bprime.md')
RUL = os.path.join(BP, 'rulings-D284.md')
FR = json.load(open(FR_JSON, encoding='utf-8'))
assert FR['deviations'] == [], ('台帳が空でない', [d.get('no') for d in FR['deviations']])
rul = open(RUL, encoding='utf-8').read()
m = re.search(r'- \*\*D284\*\*（登録者・会話の記録 uuid `([^`]+)`・([^ ]+ [^ ]+) 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「(.*)」', rul)
assert m, '裁定の記録の登録者の言葉が読めない'
approval = '登録者裁定 D284（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」・記録 `records/Bprime/rulings-D284.md`）' % (m.group(2), m.group(1), m.group(3))
cand = json.load(open(os.path.join(BP, 'records', 'Bprime', 'results-draft', 'dev-candidate-DBPT1.json'), encoding='utf-8'))
assert cand['no'] == 'D-BPT1' and cand['date'] == m.group(2).split(' ')[0]
dev = {'no': 'D-BPT1', 'date': cand['date'], 'what': cand['what'],
       'scope': '報告の表し方だけ（下見の決定・予想の照合・凍結した器・正本・凍結の本文・凍結物は変えない）',
       'approval': approval,
       'files': [{'path': 'tools/build_report_Bprime_devBPT1.py'}, {'path': 'records/Bprime/results-Bprime-draft2.md'}]}
FR['deviations'].append(dev)
with open(FR_JSON, 'w', encoding='utf-8', newline=NL) as fh:
    json.dump(FR, fh, ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
fence = [l for l in md.split(NL) if l.startswith('本記録のいかなる数値も')]
assert '## 凍結の後の逸脱の台帳' not in md and len(fence) >= 1, ('台帳の節が既にあるか、柵の行が無い', len(fence))
last = fence[-1]
i = md.rindex(last)
sec = NL.join(['## 凍結の後の逸脱の台帳（凍結の記録 `deviations` の写し・台帳は後ろに足すだけ）', '',
               '| 番号 | 日付 | 何を | 範囲 | 承認 |', '|---|---|---|---|---|',
               '| %s | %s | %s | %s | %s |' % (dev['no'], dev['date'], dev['what'].replace('|', '｜'), dev['scope'], dev['approval'].replace('|', '｜')), '', ''])
md = md[:i] + sec + md[i:]
with open(FR_MD, 'w', encoding='utf-8', newline=NL) as fh:
    fh.write(md)
print('ledgered', dev['no'], dev['date'], '| approval', m.group(2), m.group(1))
