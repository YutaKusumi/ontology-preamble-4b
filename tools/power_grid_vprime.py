# -*- coding: utf-8 -*-
"""power_grid_vprime.py —— 追補 V′ の検出力格子を `design/contrasts-Vprime.json` から機械生成する（手書き禁止）。
Fisher 両側・全数列挙（y 閾値は二分探索）・n は JSON・Holm 初段 α=0.05/m。基底は JSON の base_B_main（null は assumed_base を用い「仮定」と印字）。
基底 0.000 は 0.000 のまま計算する（0.01 に丸めない——二巡目 D-12）。感度列: 基底 ≥0.05 は +15/+10/+5pt、基底 <0.05 は +9/+5/+2pt。下向き対比は −15/−10/−5。
出力: records/power-grid-Vprime.md と同 .json（要約の帯は JSON から機械生成し、本文はそれを転記する）。
"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-Vprime.json'), encoding='utf-8')); n = T['n_per_arm']


from vprime_power import make_power
power = make_power(n)


cache = {}; grid = []
for fam, F in list(T['families'].items()) + list(T.get('descriptive_families', {}).items()):
    m = F.get('m'); a = 0.05 / m if m else 0.05
    for c in F['contrasts']:
        b = c.get('base_B_main'); src = '実測 %.3f' % b if b is not None else '仮定 %.2f' % c.get('assumed_base', 0.40)
        if b is None:
            b = c.get('assumed_base', 0.40)
        floor = b < 0.05; ds = (0.09, 0.05, 0.02) if floor else (0.15, 0.10, 0.05)
        vals = []
        for d in ds:
            p0, p1 = (b, min(b + d, 0.999)) if c['direction'] == 'up' else (b, max(b - d, 0.001))
            key = (round(p0, 4), round(p1, 4), round(a, 6))
            if key not in cache:
                cache[key] = power(*key)
            vals.append(cache[key])
        grid.append({'family': fam, 'id': c['id'], 'base': b, 'base_src': src, 'floor': floor, 'deltas': ds, 'power': vals, 'alpha': a, 'confirmatory': fam in T['families']})
# 要約（機械生成）
def band(sel):
    return (min(sel), max(sel)) if sel else (None, None)
conf = [g for g in grid if g['confirmatory'] and g['id'].split(':')[1].split('~')[1] not in ('Nstr',)]
mid15 = band([g['power'][0] for g in conf if not g['floor'] and g['base_src'].startswith('実測')]); mid10 = band([g['power'][1] for g in conf if not g['floor'] and g['base_src'].startswith('実測')])
fl9 = band([g['power'][0] for g in conf if g['floor']]); fl5 = band([g['power'][1] for g in conf if g['floor']])
counts = {'floor': sum(1 for g in grid if g['confirmatory'] and g['floor'] and g['base_src'].startswith('実測')), 'mid': sum(1 for g in grid if g['confirmatory'] and not g['floor'] and g['base_src'].startswith('実測')), 'assumed': sum(1 for g in grid if g['confirmatory'] and g['base_src'].startswith('仮定'))}
cov = {f: {'measured': sum(1 for g in grid if g['family'] == f and g['base_src'].startswith('実測')), 'assumed': sum(1 for g in grid if g['family'] == f and g['base_src'].startswith('仮定'))} for f in T['families']}
summary = {'n': n, 'mid_plus15': mid15, 'mid_plus10': mid10, 'floor_plus9': fl9, 'floor_plus5': fl5, 'counts_confirmatory': counts, 'coverage_by_family': cov}
cov_line = '帯が覆う範囲: 実測基底の %d 本（%s）に対するもの。仮定基底の %d 本（%s）は走行前に検出力を確定できず、検出域の申告に用いない。' % (counts['floor'] + counts['mid'], '・'.join('%s %d' % (f, c['measured']) for f, c in cov.items() if c['measured']), counts['assumed'], '・'.join('%s %d' % (f, c['assumed']) for f, c in cov.items() if c['assumed']))
summary['coverage_line'] = cov_line
stamp = datetime.date.today().isoformat()
out = ['# 追補 V′ 検出力格子（機械生成・Fisher 両側・全数列挙・n=%d・Holm 初段 α=0.05/m）—— %s・contrasts %s' % (n, stamp, T['version']), '',
       '基底は JSON の base_B_main（実測＝本プログラム段I の値・0.000 は 0.000 のまま計算）。null は仮定値を明記。感度列＝基底 ≥0.05 は +15/+10/+5pt・基底 <0.05 は +9/+5/+2pt（下向きは −）。', '',
       '**要約（本文はこの行を転記する）**: （帯は V′a の α＝0.05/25 で計算・V′b は 0.05/8・V′c は 0.05/32 で各行に印字）確証族・実測中間基底の +15pt: %.3f〜%.3f／+10pt: %.3f〜%.3f。床（実測 <0.05）の +9pt: %.3f〜%.3f／+5pt: %.3f〜%.3f。確証対比の内訳: 床 %d・中間 %d・未測定（仮定）%d。' % (mid15[0], mid15[1], mid10[0], mid10[1], fl9[0], fl9[1], fl5[0], fl5[1], counts['floor'], counts['mid'], counts['assumed']) + ' ' + cov_line, '',
       '| 族 | 対比 | 基底（出所） | 大 | 中 | 小 | α |', '|---|---|---|---|---|---|---|']
for g in grid:
    out.append('| %s | %s | %s | %.3f | %.3f | %.3f | %.5f |' % (g['family'], g['id'], g['base_src'], g['power'][0], g['power'][1], g['power'][2], g['alpha']))
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(os.path.join(REPO, 'records', 'power-grid-Vprime.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump({'summary': summary, 'grid': grid}, open(os.path.join(REPO, 'records', 'power-grid-Vprime.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False))
