# -*- coding: utf-8 -*-
"""凍結の記録の逸脱台帳の D-B6 の行に、旗の改め（v2.1・最終検分 P492）の追記を一文足す。足すだけ（`frozen` の区画とほかの行は前後で同一）。
用法: python records/B/deviations/annotate_devB6.py"""
import os, json, hashlib

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FREC = json.load(open(j('records', 'B', 'deviations', 'flag-record-B-2026-09-23.json'), encoding='utf-8'))
assert FREC['version'] == 'v2.1' and s16('records/B/results-report-B-frozen.md') == FREC['reports']['frozen']['flagged_sha16']
ADD = ('**追記（2026-09-23・最終検分 P492・登録者裁定 D160 の下の文の直し）**: 凍結側の旗の段を同じ器の v2.1（SHA16 %s）で改め、「事前登録した凍結の集計器の出力としてはこれが唯一の結果であり、直すという決定そのものが結果を見た後になされた」の一文を対置した（凍結の出力を軽く見せないため）。'
       '旗を除いた本文の同一性（SHA16 %s）は保った。改めた後の SHA16 %s。' % (s16('records/B/deviations/flag_reports_B.py'), FREC['reports']['frozen']['builder_output_sha16'], FREC['reports']['frozen']['flagged_sha16']))
mdp, jsp = j('records', 'B', 'FREEZE-RECORD-B.md'), j('records', 'B', 'FREEZE-RECORD-B.json')
F = json.load(open(jsp, encoding='utf-8'))
before = json.dumps({k: v for k, v in F.items() if k != 'deviations'}, sort_keys=True, ensure_ascii=False)
first5 = json.dumps(F['deviations'][:5], sort_keys=True, ensure_ascii=False)
assert F['deviations'][5]['no'] == 'D-B6' and ADD not in F['deviations'][5]['what']
old = F['deviations'][5]['what']; F['deviations'][5]['what'] = old + ' ' + ADD
assert json.dumps({k: v for k, v in F.items() if k != 'deviations'}, sort_keys=True, ensure_ascii=False) == before
assert json.dumps(F['deviations'][:5], sort_keys=True, ensure_ascii=False) == first5
md = open(mdp, encoding='utf-8').read()
rows = [l for l in md.split(NL) if l.startswith('| D-B6 |')]
assert len(rows) == 1
cells = rows[0].split(' | '); assert len(cells) == 5 and old in cells[2]
cells[2] = cells[2] + ' ' + ADD
row = ' | '.join(cells)
md2 = md.replace(rows[0] + NL, row + NL)
assert md2.replace(row + NL, rows[0] + NL) == md
json.dump(F, open(jsp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
open(mdp, 'w', encoding='utf-8', newline=NL).write(md2)
print('D-B6 annotated')
