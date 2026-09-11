# -*- coding: utf-8 -*-
"""power_posthoc_M.py —— 追補 M の検出力格子を、第一走行（stageM1）の実測基底（各対比の B 腕の全分母率）で再計算して併記する。
凍結格子（records/power-grid-M.md・V′ 実測または仮定基底）と同一の検出力関数（vprime_power.make_power・両側 Fisher・α=0.05/m）・同じ枝（床 +9/+5/+2・天井 −9/−5/−2・中間 ±15/±10/±5）。
凍結器材（power_grid_M.py・contrasts-M.json）は改変しない。出力: records/M/power-posthoc-M-<tag>.md と同 .json。走行後の解釈に用いる参考値であり検出域の申告を変えない。"""
import os, sys, json, glob, datetime, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='stageM1'); a = ap.parse_args()
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8')); n = T['n_per_arm']
from vprime_power import make_power
power = make_power(n); cache = {}


def pw(p0, p1, al):
    key = (round(p0, 4), round(min(max(p1, 0.001), 0.999), 4), round(al, 6))
    if key not in cache:
        cache[key] = power(*key)
    return cache[key]


# 実測基底: tag の cells.json から (scenario, arm) → 破局/n_ok（全分母）
obs = {}
for d in glob.glob(os.path.join(REPO, 'results', a.tag, a.tag + '__*')):
    c = json.load(open(os.path.join(d, 'cells.json'), encoding='utf-8')); sc = os.path.basename(d).split('__')[1]
    for arm, v in c['cells'].items():
        obs[(sc, arm)] = v['triplet_all']['catastrophe'] / v['n_ok']
grid = []
for fam, F in T['families'].items():
    al = 0.05 / F['m']
    for c in F['contrasts']:
        sc, pair = c['id'].split(':'); A, B = pair.split('~'); b = obs.get((sc, B))
        if b is None:
            continue
        kind = 'floor' if b < 0.05 else 'ceiling' if b > 0.95 else 'mid'
        ds = (0.09, 0.05, 0.02) if kind != 'mid' else (0.15, 0.10, 0.05)
        up = [pw(b, b + d, al) for d in ds] if kind != 'ceiling' else None
        down = [pw(b, b - d, al) for d in ds] if kind != 'floor' else None
        frozen = c.get('base_B_vprime', c.get('assumed_base'))
        grid.append({'family': fam, 'id': c['id'], 'base_obs': b, 'base_frozen': frozen, 'kind': kind, 'deltas': ds, 'power_up': up, 'power_down': down, 'alpha': al})


def band(sel):
    return (min(sel), max(sel)) if sel else (None, None)


summary = {'n': n, 'tag': a.tag}
for fam in T['families']:
    g = [x for x in grid if x['family'] == fam]
    summary[fam] = {'alpha': 0.05 / T['families'][fam]['m'], 'contrasts': len(g), 'floor': sum(1 for x in g if x['kind'] == 'floor'), 'ceiling': sum(1 for x in g if x['kind'] == 'ceiling'), 'mid': sum(1 for x in g if x['kind'] == 'mid'),
                    'floor_up_9': band([x['power_up'][0] for x in g if x['kind'] == 'floor']), 'floor_up_5': band([x['power_up'][1] for x in g if x['kind'] == 'floor']),
                    'ceiling_down_9': band([x['power_down'][0] for x in g if x['kind'] == 'ceiling']), 'ceiling_down_5': band([x['power_down'][1] for x in g if x['kind'] == 'ceiling']),
                    'mid_up_15': band([x['power_up'][0] for x in g if x['kind'] == 'mid']), 'mid_up_5': band([x['power_up'][2] for x in g if x['kind'] == 'mid']),
                    'mid_down_15': band([x['power_down'][0] for x in g if x['kind'] == 'mid']), 'mid_down_5': band([x['power_down'][2] for x in g if x['kind'] == 'mid'])}


def f3(v):
    return '—' if v is None else '%.3f' % v


def fb(t):
    return '—' if t[0] is None else '%.3f〜%.3f' % t


stamp = datetime.date.today().isoformat()
out = ['# 追補 M 検出力格子（走行後・%s 実測基底・機械生成 %s）' % (a.tag, stamp), '',
       '凍結格子（`records/power-grid-M.md`）と同一の検出力関数（n=%d・両側 Fisher・α=0.05/m）で、基底を %s の各対比 B 腕の実測全分母率に置き換えた併記。検出域の申告（凍結）は変えない。床 <0.05／天井 >0.95／中間。' % (n, a.tag), '',
       '| 族 | α | 対比数 | 床／天井／中間 | 床 +9pt | 床 +5pt | 天井 −9pt | 天井 −5pt | 中間 +15pt | 中間 +5pt | 中間 −15pt | 中間 −5pt |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for fam in T['families']:
    s = summary[fam]
    out.append('| %s | %.5f | %d | %d／%d／%d | %s | %s | %s | %s | %s | %s | %s | %s |' % (fam, s['alpha'], s['contrasts'], s['floor'], s['ceiling'], s['mid'], fb(s['floor_up_9']), fb(s['floor_up_5']), fb(s['ceiling_down_9']), fb(s['ceiling_down_5']), fb(s['mid_up_15']), fb(s['mid_up_5']), fb(s['mid_down_15']), fb(s['mid_down_5'])))
out += ['', '| 族 | 対比 | 凍結基底 | 実測基底 | 種別 | 上枝（Δ→検出力） | 下枝（Δ→検出力） |', '|---|---|---|---|---|---|---|']
for g in grid:
    up = '・'.join('+%d→%s' % (round(d * 100), f3(p)) for d, p in zip(g['deltas'], g['power_up'])) if g['power_up'] else '—'
    dn = '・'.join('−%d→%s' % (round(d * 100), f3(p)) for d, p in zip(g['deltas'], g['power_down'])) if g['power_down'] else '—'
    out.append('| %s | %s | %s | %.3f | %s | %s | %s |' % (g['family'], g['id'], f3(g['base_frozen']), g['base_obs'], g['kind'], up, dn))
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
p = os.path.join(REPO, 'records', 'M', 'power-posthoc-M-%s' % a.tag)
open(p + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump({'summary': summary, 'grid': grid}, open(p + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', p + '.md', {f: (summary[f]['floor'], summary[f]['ceiling'], summary[f]['mid']) for f in T['families']})
