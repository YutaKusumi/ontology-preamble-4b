# -*- coding: utf-8 -*-
"""gate_vprime.py —— 追補 V′ の門（GO/NO-GO）。判定規則は `design/contrasts-Vprime.json`（凍結・機械可読）だけから読む。手書きの対比辞書を持たない（D-5 の再発防止）。
用法: python tools/gate_vprime.py --tag pilotVp   → records/vprime/gate-<tag>-<date>.md
規則（JSON の gate_counts）: 上向き対比は対照 B の破局が pilot_n 中 ceiling_min 以上で「天井・記述に降格」、下向き対比は対照 B の破局が floor_max 以下で「床・記述に降格」。降格しても m は減らさない。
"""
import os, sys, json, glob, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='pilotVp'); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-Vprime.json'))
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8')); G = T['gate_counts']
cells = {}
for f in glob.glob(os.path.join(REPO, 'results', args.tag, '*', 'cells.json')):
    d = json.load(open(f, encoding='utf-8')); cells[d['manifest']['scenario']] = d['cells']
out = ['# 追補 V′ 門の判定 —— %s（tag %s・規則は %s 版 %s）' % (datetime.date.today().isoformat(), args.tag, os.path.basename(args.contrasts), T['version']), '',
       '規則: 上向き対比＝対照 B の破局が %d/%d 以上で天井（記述に降格）／下向き対比＝対照 B の破局が %d/%d 以下で床（記述に降格）。m は減らさない。パイロットの k は本走行に転用しない。' % (G['ceiling_min_catastrophes'], G['pilot_n'], G['floor_max_catastrophes'], G['pilot_n']), '']
for fam, F in T['families'].items():
    out.append('## 族 %s（m=%d）——%s' % (fam, F['m'], F['question'])); out.append('| 対比 | 向き | 対照 B の破局/n（パイロット） | A の破局/n | 門 | 判定 |'); out.append('|---|---|---|---|---|---|')
    for c in F['contrasts']:
        sc = c['scenario']; cB = cells.get(sc, {}).get(c['B']); cA = cells.get(sc, {}).get(c['A'])
        if not cB:
            out.append('| %s | %s | （未走行） | — | %s | 判定不能 |' % (c['id'], c['direction'], c['gate'])); continue
        kB, nB = cB['catastrophe'], cB['n_ok']; kA = (cA or {}).get('catastrophe'); nA = (cA or {}).get('n_ok')
        if c['direction'] == 'up':
            down = kB >= G['ceiling_min_catastrophes']; why = '天井（対照 %d/%d ≥ %d）' % (kB, nB, G['ceiling_min_catastrophes'])
        else:
            down = kB <= G['floor_max_catastrophes']; why = '床（対照 %d/%d ≤ %d）' % (kB, nB, G['floor_max_catastrophes'])
        out.append('| %s | %s | %d/%d | %s/%s | %s | %s |' % (c['id'], c['direction'], kB, nB, kA, nA, c['gate'], ('**記述に降格**・' + why) if down else 'GO'))
    out.append('')
out.append('本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
os.makedirs(os.path.join(REPO, 'records', 'vprime'), exist_ok=True)
p = os.path.join(REPO, 'records', 'vprime', 'gate-%s-%s.md' % (args.tag, datetime.date.today().isoformat()))
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n'); print('written', p)
