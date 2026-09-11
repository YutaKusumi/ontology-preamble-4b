# -*- coding: utf-8 -*-
"""control_chart_F.py —— 校正腕の管理図 `records/control-chart.md` に本走行の校正腕（U-Ncold × N1・U-O-Ncold × 4 場面・JSON continuity.calibration_chart）を記帳する（走行ごと・同じ tag は二重に記帳しない）。
帯は 5 pt（n=400 では約 2 σ・転記行 M′）。既測基底は M 第一走行（base_M1）。判定はしない（記述・以後の段で系の変動を追う）。
用法: python tools/control_chart_F.py --tag stageF1 [--root results/_dryrun]"""
import os, json, glob, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--root', default=None); ap.add_argument('--out', default=None, help='検査用の出力先（既定は JSON の calibration_chart.file）'); a = ap.parse_args()
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8')); CC = T['continuity']['calibration_chart']; P = a.out or os.path.join(REPO, CC['file'].replace('/', os.sep))
root = a.root or os.path.join(REPO, 'results', a.tag); cells = {}
for f in glob.glob(os.path.join(root, a.tag + '__*', 'cells.json')):
    d = json.load(open(f, encoding='utf-8')); cells.setdefault(d['manifest']['scenario'], {}).update(d['cells'])
HEAD = ['# 校正腕の管理図（段階 F から開始・記述・判定しない）', '', '校正腕: U-Ncold × N1・U-O-Ncold × 4 場面（V′・M と同一バイトの U 腕）。既測基底＝M 第一走行（公開済み）。帯 5 pt（n=400 では約 2 σ）。同じ系（Qwen3-4B-Instruct-2507・nscale・T=0.7・top_p=0.9）の走行ごとに一行。率は系の変動の記録であり、腕の効果の証拠として引用しない。', '',
        '| 記帳日（UTC） | tag | 腕 | 場面 | 破局/n | 率 | 既測基底（M1） | 差（pt） | 5 pt 帯の外 |', '|---|---|---|---|---|---|---|---|---|']
lines = open(P, encoding='utf-8').read().split('\n') if os.path.exists(P) else HEAD
if any(l.startswith('| ') and ('| %s |' % a.tag) in l for l in lines):
    print('already recorded', a.tag); raise SystemExit(0)
add = []
for arm, sc in CC['arms']:
    x = cells.get(sc, {}).get(arm)
    if not x or not x['n_ok']:
        continue
    base = T['scenarios'][sc]['base_M1'][arm]['catastrophe'] / T['scenarios'][sc]['base_M1'][arm]['n_ok']; r = x['catastrophe'] / x['n_ok']; d = (r - base) * 100
    add.append('| %s | %s | %s | %s | %d/%d | %.4f | %.4f | %+.1f | %s |' % (datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), a.tag, arm, sc, x['catastrophe'], x['n_ok'], r, base, d, '外' if abs(d) >= CC['band_pt'] - 1e-9 else '—'))
while lines and lines[-1] == '':
    lines.pop()
if not lines[-1].startswith('本文書'):
    lines += add + ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
else:
    lines = lines[:-2] + add + lines[-2:]
open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n'); print('written', P, len(add), 'rows')
