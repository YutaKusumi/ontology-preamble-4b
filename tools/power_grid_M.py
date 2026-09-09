# -*- coding: utf-8 -*-
"""power_grid_M.py v1 —— 追補 M の検出力格子を `design/contrasts-M.json` から機械生成する（手書き禁止・上下二枝・両側 Fisher・全数列挙・n=400・α=0.05/m）。
基底: base_B_vprime（V′ stageVp 実測）があればそれ、なければ assumed_base（仮定・印字に明記）。感度列: 基底 <0.05（床）は +9/+5/+2pt の上枝のみ（下枝は基底が 0 に近く意味を持たない）／
基底 >0.95（天井）は −9/−5/−2pt の下枝のみ／中間は ±15/±10/±5pt の両枝。出力: records/power-grid-M.md と同 .json。
"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8')); n = T['n_per_arm']
from vprime_power import make_power
power = make_power(n); cache = {}


def pw(p0, p1, a):
    key = (round(p0, 4), round(min(max(p1, 0.001), 0.999), 4), round(a, 6))
    if key not in cache:
        cache[key] = power(*key)
    return cache[key]


grid = []
for fam, F in T['families'].items():
    a = 0.05 / F['m']
    for c in F['contrasts']:
        b = c.get('base_B_vprime'); src = '実測 %.3f' % b if b is not None else '仮定 %.3f' % c['assumed_base']
        if b is None:
            b = c['assumed_base']
        kind = 'floor' if b < 0.05 else 'ceiling' if b > 0.95 else 'mid'
        ds = (0.09, 0.05, 0.02) if kind != 'mid' else (0.15, 0.10, 0.05)
        up = [pw(b, b + d, a) for d in ds] if kind != 'ceiling' else None
        down = [pw(b, b - d, a) for d in ds] if kind != 'floor' else None
        grid.append({'family': fam, 'id': c['id'], 'base': b, 'base_src': src, 'kind': kind, 'deltas': ds, 'power_up': up, 'power_down': down, 'alpha': a})
def band(sel):
    return (min(sel), max(sel)) if sel else (None, None)
summary = {'n': n}
for fam in T['families']:
    g = [x for x in grid if x['family'] == fam]
    summary[fam] = {'alpha': 0.05 / T['families'][fam]['m'], 'measured': sum(1 for x in g if x['base_src'].startswith('実測')), 'assumed': sum(1 for x in g if x['base_src'].startswith('仮定')),
                    'floor_up_9': band([x['power_up'][0] for x in g if x['kind'] == 'floor']), 'floor_up_5': band([x['power_up'][1] for x in g if x['kind'] == 'floor']),
                    'ceiling_down_9': band([x['power_down'][0] for x in g if x['kind'] == 'ceiling']), 'ceiling_down_5': band([x['power_down'][1] for x in g if x['kind'] == 'ceiling']),
                    'mid_up_15': band([x['power_up'][0] for x in g if x['kind'] == 'mid']), 'mid_down_15': band([x['power_down'][0] for x in g if x['kind'] == 'mid'])}
stamp = datetime.date.today().isoformat()


def f3(v):
    return '—' if v is None else '%.3f' % v


out = ['# 追補 M 検出力格子（機械生成・両側 Fisher・全数列挙・n=%d・上下二枝・Holm 初段 α=0.05/m）—— %s・contrasts %s' % (n, stamp, T['version']), '',
       '基底は JSON の base_B_vprime（V′ stageVp 実測）または assumed_base（仮定・M-a／M-b は V′ Nk-Ncold 実測、M-c は V′ O-Ncold 実測を仮定値に用いる）。床（<0.05）は上枝のみ +9/+5/+2pt、天井（>0.95）は下枝のみ −9/−5/−2pt、中間は両枝 ±15/±10/±5pt。仮定基底の行は走行後に実測基底で再計算して併記し、走行前の値を検出域の申告に用いない。', '']
for fam, sm in summary.items():
    if fam == 'n':
        continue
    out.append('**要約 %s（α=%.5f・実測基底 %d 本・仮定 %d 本）**: 床 +9pt %s〜%s／+5pt %s〜%s；天井 −9pt %s〜%s／−5pt %s〜%s；中間 +15pt %s〜%s／−15pt %s〜%s。' % (fam, sm['alpha'], sm['measured'], sm['assumed'], f3(sm['floor_up_9'][0]), f3(sm['floor_up_9'][1]), f3(sm['floor_up_5'][0]), f3(sm['floor_up_5'][1]), f3(sm['ceiling_down_9'][0]), f3(sm['ceiling_down_9'][1]), f3(sm['ceiling_down_5'][0]), f3(sm['ceiling_down_5'][1]), f3(sm['mid_up_15'][0]), f3(sm['mid_up_15'][1]), f3(sm['mid_down_15'][0]), f3(sm['mid_down_15'][1])))
out += ['', '| 族 | 対比 | 基底（出所） | 種別 | 上枝 大/中/小 | 下枝 大/中/小 | α |', '|---|---|---|---|---|---|---|']
for g in grid:
    up = '/'.join('%.3f' % v for v in g['power_up']) if g['power_up'] else '—'; dn = '/'.join('%.3f' % v for v in g['power_down']) if g['power_down'] else '—'
    out.append('| %s | %s | %s | %s | %s | %s | %.5f |' % (g['family'], g['id'], g['base_src'], g['kind'], up, dn, g['alpha']))
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(os.path.join(REPO, 'records', 'power-grid-M.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump({'summary': summary, 'grid': grid}, open(os.path.join(REPO, 'records', 'power-grid-M.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('\n'.join(o for o in out if o.startswith('**要約')))
