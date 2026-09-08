# -*- coding: utf-8 -*-
"""posthoc_vprime.py v3 —— 追補 V′ 走行後の機械生成（凍結器材は変更しない・新設）:
(1) 実測基底での検出力再計算（凍結 §2.5・報告規則: 仮定基底の対比は走行後に実測基底で再計算して併記）——各確証対比の対照 B の実測率を基底に、
    +15/+10/+5pt（床 <0.05 は +9/+5/+2・下向きは −）の検出力を同一の検出力関数（tools/vprime_power.py）で計算し、当該対比の族 α で印字する。
(2) 封印予想との照合表（登録者 v0.5 とコーディネータ）——帯の的中／外れを機械判定。的中・外れは誰の判断の重みも変えない（予想的中の非転用）。
用法: python tools/posthoc_vprime.py --tag stageVp
"""
import os, sys, json, glob, argparse, datetime
from decimal import Decimal, ROUND_HALF_UP
def dpt(kA, kB, n): return str((Decimal((kA - kB) * 100) / Decimal(n)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
def d3(kA, kB, n): return str((Decimal(kA - kB) / Decimal(n)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vprime_power import make_power
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='stageVp'); ap.add_argument('--pred', default='records/predictions/predictions-registrant-Vprime-2026-09-07.json')
args = ap.parse_args()
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-Vprime.json'), encoding='utf-8')); n = T['n_per_arm']; power = make_power(n)
cells = {}
for f in glob.glob(os.path.join(REPO, 'results', args.tag, args.tag + '__*', 'cells.json')):
    d = json.load(open(f, encoding='utf-8')); cells[d['manifest']['scenario']] = d['cells']
stamp = datetime.date.today().isoformat()
# (1) 実測基底の検出力
out = ['# 追補 V′ 走行後の機械生成 —— tag %s・contrasts %s・%s' % (args.tag, T['version'], stamp), '',
       '## 1. 実測基底での検出力（凍結格子の仮定基底行を実測で置き換えた併記・同一の検出力関数・n=%d・族 α）' % n,
       '**凡例（一巡目検分の条件）**: 列「大・中・小」の感度は、実測基底 B が 0.05 以上の行では +15／+10／+5 pt、0.05 未満（床）の行では +9／+5／+2 pt。下向き対比（V′b）は −15／−10／−5 pt（B から引く）。α は当該対比の族の Holm 初段（V′a 0.05/25・V′b 0.05/8・V′c 0.05/32）。凍結格子の帯は V′a の α（0.05/25）で計算したもの。記述族（§1b）は検定を置かないため α=0.05 の参考値。丸め規約（三巡目で統一）: 本文書の実測差は整数件数から Decimal で計算し、pt は小数一桁・率差は小数三桁に四捨五入（.x5 はゼロから遠ざける・浮動小数の減算を経ない）。v2 までは浮動小数から丸めていたため .x5 型が絶対値の小さい側に落ちる行があった（三巡目宝生・28 行）。',
       '| 族 | 対比 | 凍結格子の基底（出所） | 実測基底 B | 大 | 中 | 小 | 実測差 | α |', '|---|---|---|---|---|---|---|---|---|']
G = json.load(open(os.path.join(REPO, 'records', 'power-grid-Vprime.json'), encoding='utf-8'))['grid']; gi = {g['id']: g for g in G}
cache = {}
for fam, F in T['families'].items():
    a = 0.05 / F['m']
    for c in F['contrasts']:
        A = cells.get(c['scenario'], {}).get(c['A']); B = cells.get(c['scenario'], {}).get(c['B'])
        if not A or not B: continue
        b = B['catastrophe'] / B['n_ok']; ra = A['catastrophe'] / A['n_ok']
        floor = b < 0.05; ds = [0.09, 0.05, 0.02] if floor else [0.15, 0.10, 0.05]
        vals = []
        for dd in ds:
            p0, p1 = (b, min(b + dd, 0.999)) if c['direction'] == 'up' else (b, max(b - dd, 0.001))
            key = (round(p0, 4), round(p1, 4), round(a, 6))
            if key not in cache: cache[key] = power(*key)
            vals.append(cache[key])
        g = gi.get(c['id'], {})
        dd3 = d3(A['catastrophe'], B['catastrophe'], A['n_ok']); out.append('| %s | %s | %s | %.3f | %.3f | %.3f | %.3f | %s%s | %.5f |' % (fam, c['id'], g.get('base_src', '—'), b, vals[0], vals[1], vals[2], '+' if not dd3.startswith('-') else '', dd3, a))
out.append('')
# (1b) 記述族の感度（参考・α=0.05・検定なし）
out += ['## 1b. 記述族の感度（参考・検定なし・α=0.05・同じ梯子）', '| 族 | 対比 | 実測基底 B | 大 | 中 | 小 | 実測差 |', '|---|---|---|---|---|---|---|']
for fam, F in T.get('descriptive_families', {}).items():
    a = 0.05
    for c in F['contrasts']:
        A = cells.get(c['scenario'], {}).get(c['A']); B = cells.get(c['scenario'], {}).get(c['B'])
        if not A or not B: continue
        b = B['catastrophe'] / B['n_ok']; ra = A['catastrophe'] / A['n_ok']
        floor = b < 0.05; ds = [0.09, 0.05, 0.02] if floor else [0.15, 0.10, 0.05]
        vals = []
        for dd in ds:
            p0, p1 = (b, min(b + dd, 0.999)) if c['direction'] == 'up' else (b, max(b - dd, 0.001))
            key = (round(p0, 4), round(p1, 4), round(a, 6))
            if key not in cache: cache[key] = power(*key)
            vals.append(cache[key])
        dp = dpt(A['catastrophe'], B['catastrophe'], A['n_ok']); out.append('| %s | %s | %.3f | %.3f | %.3f | %.3f | %s%s pt |' % (fam, c['id'], b, vals[0], vals[1], vals[2], '+' if not dp.startswith('-') else '', dp))
out.append('')
# (2) 予想照合
BANDS = [('5%以下', 0, 0.05), ('5%超20%以下', 0.05, 0.20), ('20%超50%以下', 0.20, 0.50), ('50%超80%以下', 0.50, 0.80), ('80%超', 0.80, 1.01)]
def band_of(r):
    for name, lo, hi in BANDS:
        if (r <= hi if name == '5%以下' else lo < r <= hi) and (name != '80%超' or r > 0.80): return name
    return '?'
P = json.load(open(os.path.join(REPO, args.pred), encoding='utf-8'))
out += ['## 2. 封印予想（登録者 v0.5・SHA-256 CF43F23F…）との照合——帯の的中は誰の判断の重みも変えない（予想的中の非転用）', '',
        '| シナリオ | 腕 | 実測 破局/n（率） | 実測の帯 | 登録者の帯 | 的中 |', '|---|---|---|---|---|---|']
hit = tot = 0; hits_by_sc = {}
for sc in T['scenarios']:
    for a in T['arms']['singles'] + T['arms']['combos']:
        k = 'vp.%s.%s' % (sc, a)
        if k not in P: continue
        x = cells[sc][a]; r = x['catastrophe'] / x['n_ok']; ob = band_of(r); pb = P[k]
        if pb == '予想しない': continue
        ok = (ob == pb); tot += 1; hit += ok; hits_by_sc.setdefault(sc, [0, 0]); hits_by_sc[sc][0] += ok; hits_by_sc[sc][1] += 1
        out.append('| %s | %s | %d/%d (%.3f) | %s | %s | %s |' % (sc, a, x['catastrophe'], x['n_ok'], r, ob, pb, '○' if ok else '×'))
out.append('')
out.append('帯の的中: %d/%d（%s）。分母 %d は封印様式の対象腕（52 腕のうち NcoldS・Ncold3 系を除く 35 腕 × 4 シナリオ）。向きの予想（dir_a/b/c・conf）は本表の判定と別に報告本文で照合する。' % (hit, tot, '・'.join('%s %d/%d' % (sc, v[0], v[1]) for sc, v in hits_by_sc.items()), tot))
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
base = os.path.join(REPO, 'records', 'vprime', 'posthoc-Vprime-%s' % args.tag); p = base + '.md'; k = 2
while os.path.exists(p):
    p = '%s-%d.md' % (base, k); k += 1
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n'); print('written', p); print(out[-3])
