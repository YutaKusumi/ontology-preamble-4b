# -*- coding: utf-8 -*-
"""power_grid_F.py v1 —— 段階 F の検出力格子を `design/contrasts-F.json` から機械生成する（手書き禁止・上下二枝・両側 Fisher・全数列挙・n=400・α=0.05/24）。
基底: base_B_M1（追補 M 第一走行の U 腕の実測・24 本すべて実測）。床（<0.05）は上枝 +9/+5/+2pt、天井（>0.95）は下枝 −9/−5/−2pt、中間は両枝 ±15/±9/±5pt。
出力: records/F/power-grid-F.md と同 .json（報告規則 3 の履行形＝結果報告 §11 に対比別の全表を逐語転記する）。
"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8')); n = T['n_per_arm']
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
        b = c['base_B_M1']; kind = 'floor' if b < 0.05 else 'ceiling' if b > 0.95 else 'mid'
        ds = (0.09, 0.05, 0.02) if kind != 'mid' else (0.15, 0.09, 0.05)
        up = [pw(b, b + d, a) for d in ds] if kind != 'ceiling' else None
        down = [pw(b, b - d, a) for d in ds] if kind != 'floor' else None
        grid.append({'family': fam, 'id': c['id'], 'base': b, 'base_src': '実測 %.4f（M 第一走行 %d/400）' % (b, c['base_B_M1_count']), 'kind': kind, 'deltas': ds, 'power_up': up, 'power_down': down, 'alpha': a, 'duplicate': c.get('duplicate', False)})


def band(sel):
    return (min(sel), max(sel)) if sel else (None, None)


summary = {'n': n}
for fam in T['families']:
    g = [x for x in grid if x['family'] == fam]
    summary[fam] = {'alpha': 0.05 / T['families'][fam]['m'], 'measured': len(g), 'assumed': 0,
                    'floor_up_9': band([x['power_up'][0] for x in g if x['kind'] == 'floor']), 'floor_up_5': band([x['power_up'][1] for x in g if x['kind'] == 'floor']),
                    'ceiling_down_9': band([x['power_down'][0] for x in g if x['kind'] == 'ceiling']), 'ceiling_down_5': band([x['power_down'][1] for x in g if x['kind'] == 'ceiling']),
                    'mid_up_15': band([x['power_up'][0] for x in g if x['kind'] == 'mid']), 'mid_up_9': band([x['power_up'][1] for x in g if x['kind'] == 'mid']), 'mid_up_5': band([x['power_up'][2] for x in g if x['kind'] == 'mid']),
                    'mid_down_15': band([x['power_down'][0] for x in g if x['kind'] == 'mid']), 'mid_down_9': band([x['power_down'][1] for x in g if x['kind'] == 'mid']), 'mid_down_5': band([x['power_down'][2] for x in g if x['kind'] == 'mid'])}
stamp = datetime.date.today().isoformat()


def f3(v):
    return '—' if v is None else '%.3f' % v


out = ['# 段階 F 検出力格子（機械生成・両側 Fisher・全数列挙・n=%d・上下二枝・Holm 初段 α=0.05/m）—— %s・contrasts %s' % (n, stamp, T['version']), '',
       '基底は JSON の base_B_M1（追補 M 第一走行の U 腕の実測・24 本すべて実測・仮定基底なし）。床（<0.05）は上枝のみ +9/+5/+2pt、天井（>0.95）は下枝のみ −9/−5/−2pt、中間は両枝 ±15/±9/±5pt。Holm の第一段の下界であり第二段以降はより緩い。', '']
for fam, sm in summary.items():
    if fam == 'n':
        continue
    out.append('**要約 %s（α=%.5f・実測基底 %d 本）**: 床 +9pt %s〜%s／+5pt %s〜%s；天井 −9pt %s〜%s／−5pt %s〜%s；中間 +15pt %s〜%s／+9pt %s〜%s／+5pt %s〜%s；−15pt %s〜%s／−9pt %s〜%s／−5pt %s〜%s。' % (fam, sm['alpha'], sm['measured'], f3(sm['floor_up_9'][0]), f3(sm['floor_up_9'][1]), f3(sm['floor_up_5'][0]), f3(sm['floor_up_5'][1]), f3(sm['ceiling_down_9'][0]), f3(sm['ceiling_down_9'][1]), f3(sm['ceiling_down_5'][0]), f3(sm['ceiling_down_5'][1]), f3(sm['mid_up_15'][0]), f3(sm['mid_up_15'][1]), f3(sm['mid_up_9'][0]), f3(sm['mid_up_9'][1]), f3(sm['mid_up_5'][0]), f3(sm['mid_up_5'][1]), f3(sm['mid_down_15'][0]), f3(sm['mid_down_15'][1]), f3(sm['mid_down_9'][0]), f3(sm['mid_down_9'][1]), f3(sm['mid_down_5'][0]), f3(sm['mid_down_5'][1])))
out += ['', '| 族 | 対比 | 基底（出所） | 種別 | 上枝 大/中/小 | 下枝 大/中/小 | α | 重複 |', '|---|---|---|---|---|---|---|---|']
for g in grid:
    up = '/'.join('%.3f' % v for v in g['power_up']) if g['power_up'] else '—'; dn = '/'.join('%.3f' % v for v in g['power_down']) if g['power_down'] else '—'
    out.append('| %s | %s | %s | %s | %s | %s | %.5f | %s |' % (g['family'], g['id'], g['base_src'], g['kind'], up, dn, g['alpha'], '重複（T2 × S4）' if g['duplicate'] else '—'))
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
os.makedirs(os.path.join(REPO, 'records', 'F'), exist_ok=True)
open(os.path.join(REPO, 'records', 'F', 'power-grid-F.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump({'summary': summary, 'grid': grid}, open(os.path.join(REPO, 'records', 'F', 'power-grid-F.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('\n'.join(o for o in out if o.startswith('**要約')))
