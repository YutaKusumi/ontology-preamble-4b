# -*- coding: utf-8 -*-
"""逸脱 D-BL3（報告の草案の二つ目の組み立ての器）と D-BL4（事後の計算の器）を、凍結の記録の逸脱台帳に記す（登録者裁定 D191・D192・2026-09-24）。
器と出力の SHA16 は器が計算し、承認の言葉は裁定 D189〜D193 の記録から機械で写す（手で打たない）。既に記してあれば止める。
用法: python records/Blens/ledger_DBL3_DBL4.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda r: hashlib.sha256(open(P(r), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FR_JSON, FR_MD = os.path.join(HERE, 'FREEZE-RECORD-Blens.json'), os.path.join(HERE, 'FREEZE-RECORD-Blens.md')
FR = json.load(open(FR_JSON, encoding='utf-8'))
assert [d['no'] for d in FR['deviations']] == ['D-BL1', 'D-BL2'], [d['no'] for d in FR['deviations']]
rul = open(os.path.join(HERE, 'rulings-D189-D193.md'), encoding='utf-8').read()
m = re.search(r'- 登録者の言葉（逐語・会話の記録 uuid `([^`]+)`・([^ ]+ [^ ]+) 日本時間）: 「(.*)」', rul)
approval = lambda d: '登録者裁定 %s（%s 日本時間・会話の記録 uuid `%s`・逐語「%s」）' % (d, m.group(2), m.group(1), m.group(3))
PH = json.load(open(P('results/Blens/posthoc-Blens.json'), encoding='utf-8'))
dev3 = {'no': 'D-BL3', 'date': m.group(2).split(' ')[0],
        'what': ('**報告の草案の二つ目の組み立て**。凍結した組み立ての器 `tools/build_report_Blens.py` の出力は、凍結の本文が並べるとした記述の多く（兄弟の三対・八腕の値・対の距離・感度の集合・狙いの度合い・'
                 '上位の次元を零にした感度・大きさの目盛りの部分と余弦・答えの文字の位置のまとめ）を載せず、予想の照合の条件つきの向きの欄を「不一致」と印字した（結果の巡・第一巡の所見）。'
                 '逸脱の下の器 `tools/build_report_Blens_devBL3.py`（SHA16 %s）は、凍結した器を読み込み、同じ入力で凍結の報告を作り直して置き場の報告とバイトで同じことを確かめてから、'
                 '見出しと状態の行を改め、印を付けた機械の区画を足す（凍結の報告の文と区画は一字も変えない）。出力 `records/Blens/results-Blens-draft2.md`（SHA16 %s・走査の違反 0）。'
                 '採否表 `records/reviews/Blens/results-round1/adoption-table-Blens-results-r1.md` の区分（三）の行') % (s16('tools/build_report_Blens_devBL3.py'), s16('records/Blens/results-Blens-draft2.md')),
        'scope': '報告の表し方だけ（札・門・大きさの目盛りの判定と、凍結した器の出力は変えない）',
        'approval': approval('D191'),
        'files': [{'path': 'tools/build_report_Blens_devBL3.py', 'sha16': s16('tools/build_report_Blens_devBL3.py')}, {'path': 'records/Blens/results-Blens-draft2.md', 'sha16': s16('records/Blens/results-Blens-draft2.md')}]}
dev4 = {'no': 'D-BL4', 'date': m.group(2).split(' ')[0],
        'what': ('**事後の計算**。凍結した層二の器 `tools/blens_calib.py` は、正本が記述として求めた主位置の生の全語彙の softmax の確率（`magnitude.quantity`）と、異なる文の頭の数'
                 '（`magnitude.aggregate`）を計算していなかった。事後の器 `tools/posthoc_Blens.py`（SHA16 %s）が、同じ芯の関数と層二と同じ入力で計算した（出力 `results/Blens/posthoc-Blens.json`・SHA16 %s）。'
                 '変換の後の確率は層二の記録と %d 行すべてで一致し、答えの文字を覆うトークンの位置は %d 件すべてで Colab の記録と一致した') % (
            s16('tools/posthoc_Blens.py'), s16('results/Blens/posthoc-Blens.json'), PH['checks']['pT_reproduced_rows'], PH['checks']['cover_reproduced']),
        'scope': '事後の区画の記述だけ（札を新しく作らず、付いた札と読みの比を変えない）',
        'approval': approval('D192'),
        'files': [{'path': 'tools/posthoc_Blens.py', 'sha16': s16('tools/posthoc_Blens.py')}, {'path': 'results/Blens/posthoc-Blens.json', 'sha16': s16('results/Blens/posthoc-Blens.json')}]}
FR['deviations'] += [dev3, dev4]
json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = open(FR_MD, encoding='utf-8').read()
anchor = [l for l in md.split(NL) if l.startswith('| D-BL2 |')][0]
rows = NL.join('| %s | %s | %s | %s | %s |' % (d['no'], d['date'], d['what'].replace('|', '｜'), d['scope'], d['approval'].replace('|', '｜')) for d in (dev3, dev4))
md = md.replace(anchor, anchor + NL + rows, 1)
open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md)
print('ledgered D-BL3 and D-BL4 |', dev3['files'], dev4['files'])
