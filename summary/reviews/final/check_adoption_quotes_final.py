# -*- coding: utf-8 -*-
"""check_adoption_quotes_final.py v0（2026-10-02・二巡目の `check_adoption_quotes_round2.py` v0 を写し、照らしの集まりを最終の巡の物に替えた・採否の表の「」の中身と数を、草案・枠・追記・依頼文・記録・票・各段の最終版と凍結の本文と裁定に照らす・コーディネータ南無弥勒如来）。
用法: python check_adoption_quotes_final.py <採否の表の md>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.dirname(os.path.dirname(HERE))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
T = open(sys.argv[1], encoding='utf-8').read()
files = [os.path.join(SUM, 'summary-interim-draft3-2026-10-02.md'), os.path.join(SUM, 'summary-interim-draft2-2026-10-02.md'), os.path.join(SUM, 'summary-interim-draft1-2026-10-02.md'),
         os.path.join(SUM, '00-frame-interim-summary-2026-10-02.md'), os.path.join(SUM, '00-frame-addendum1-2026-10-02.md'), os.path.join(SUM, '00-frame-addendum2-2026-10-02.md'),
         os.path.join(HERE, 'request-final.md'), os.path.join(HERE, 'sending-log-final.md'), os.path.join(HERE, 'receiving-log-final.md'), os.path.join(HERE, 'repro-final.md'),
         os.path.join(SUM, 'calc', 'calc-interim-v0.3.md'), os.path.join(SUM, 'reviews', 'round1', 'adoption-table-round1.md'), os.path.join(SUM, 'reviews', 'round2', 'adoption-table-round2.md'),
         os.path.join(SUM, 'reviews', 'round2', 'repro-round2.md'), os.path.join(SUM, 'reviews', 'round1', 'rulings-D287.md'), os.path.join(SUM, 'reviews', 'round2', 'rulings-D288.md')]
files += glob.glob(os.path.join(HERE, 'votes', '*', 'response.md')) + sorted(set(glob.glob(PUB + '/records/*/*FINAL*.md')))
files += [PUB + '/design/design-stageA-FROZEN.md', PUB + '/design/design-Bprime-FROZEN.md', PUB + '/design/design-stageF-FROZEN.md', PUB + '/records/Bprime/rulings-D257.md',
          PUB + '/records/Bprime/rulings-D258.md']
files += [PUB + '/design/contrasts-Bprime.json']
CORP = '\n'.join(open(f, encoding='utf-8').read().replace('\r\n', '\n') for f in files)
CNB = CORP.replace('**', '')
qs = sorted(set(re.findall(r'「([^「」]+)」', T)))
qm = [q for q in qs if q not in CORP and q not in CNB]
body = T.split('## 検分票')[0]
nums = sorted(set(re.findall(r'(?<![A-Za-z0-9_.\-])(\d+(?:[./]\d+)*)(?![A-Za-z0-9_])', body)))
nm = [n for n in nums if n not in CORP]
print('files', len(files), '| quotes', len(qs), '| missing quotes:', qm)
print('numbers', len(nums), '| missing numbers:', nm)
