# -*- coding: utf-8 -*-
"""control_chart_B.py v3 —— 段階 B の**校正の管理図**（正本 `calibration`・起草者の見直し S1・実装検分の採否表 P276）。

別置きの校正腕は置かない（試行が増えるため）。代わりに、**無操作の腕の率をセッションごとに並べる**。
  - 点: 腕 × 場面 × セッションの全分母破局率（分子＝破局・分母＝n_ok）。
  - 初点: 同じ腕 × 場面の**最初のセッション**（初点は判定しない）。
  - 帯: `calibration.band_pt`（二標本・両側・厳密 Fisher）。**帯を超え、かつ p が `calibration.alpha` 未満のときだけ**「器の異常」を記帳し、**その走行を含む対比の確証札に注を付す**（v3・2026-09-19・正本 `calibration.judgement`・v2 までは p を判定に使っていなかった）。
限界（正本 `calibration.limitation`）: 同じ腕 × 場面が一つのセッションに収まる場合、点は一つだけで管理図にならない。その旨を印字する。
出力: records/B/control-chart-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/control_chart_B.py [--root <results>] [--allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.stats import fisher_exact
import runs_B

VERSION = 'v3'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
CAL = T['calibration']
NOOP = set(T['arms']['noop'])
BAND = CAL['band_pt'] / 100.0
ALPHA = CAL['alpha']

idx = runs_B.index_runs(T, T['tags']['main'], a.root, allow_dry=a.allow_dry)
points, anomalies, notes = [], [], []
by_cell = {}
for (sc,), recs in sorted(idx.items()):
    for rec in recs:
        sess = rec['manifest'].get('session')
        for arm, c in runs_B.cell_counts(rec['trials_path']).items():
            if arm not in NOOP:
                continue
            by_cell.setdefault((sc, arm), []).append({'session': sess, 'run_key': rec['run_key'], 'k': c['cat'], 'n': c['n_ok'],
                                                      'rate': runs_B.rate(c['cat'], c['n_ok'])})
for (sc, arm), pts in sorted(by_cell.items(), key=str):
    pts.sort(key=lambda x: (x['session'] is None, x['session']))
    for i, p in enumerate(pts):
        row = dict(p, scenario=sc, arm=arm, first_point=(i == 0))
        if i == 0:
            row['verdict'] = '初点（判定しない）'
        elif p['rate'] is None or pts[0]['rate'] is None:
            # **使える試行が零の点は判定しない**（裁定 D110・採否表 P323）。
            # 前は空を零と読んで差を計算し、測れなかった点に「器の異常」の札を付けていた。
            row['verdict'] = '測れなかった（使えた試行が零・判定しない）'
        else:
            base = pts[0]
            pval = float(fisher_exact([[p['k'], p['n'] - p['k']], [base['k'], base['n'] - base['k']]])[1])
            d = (p['rate'] or 0) - (base['rate'] or 0)
            # **帯を超え、かつ厳密検定の p が alpha 未満のときだけ異常**（正本 calibration.judgement・裁定 D127・採否表 P350）。
            # v2 までは差だけで判定し、正本が「厳密」と書く検定の p を一度も使っていなかった。
            # この直しは異常の札を減らす向き（小さな n の揺れで札が立たない）であり、起草者の引力と同じ側——正本に書いた。
            band_out = abs(d) > BAND
            out = band_out and (pval < ALPHA)
            row.update({'diff_pt': round(100 * d, 3), 'p': pval, 'outside': out, 'band_outside': band_out,
                        'verdict': ('**帯の外かつ有意**（器の異常を記帳し、この走行を含む対比の確証札に注を付す）' if out else
                                    ('帯の外だが有意でない（異常にしない・p を印字する）' if band_out else '帯の内側'))})
            if abs(abs(d) - BAND) < 1e-9:
                row['verdict'] += '・境目に一致（%g pt）' % CAL['band_pt']
            if out:
                anomalies.append({'scenario': sc, 'arm': arm, 'run_key': p['run_key'], 'diff_pt': row['diff_pt']})
        points.append(row)
    if len(pts) == 1:
        notes.append('%s × %s は点が一つ（%s）——管理図にならない（%s）' % (sc, arm, pts[0]['run_key'], CAL['limitation']))

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'control-chart-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p_ in (out_md, out_json):
        if os.path.exists(p_):
            sys.exit('既にある（--force で上書き）: %s' % p_)
json.dump({'kind': 'control_chart_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'band_pt': CAL['band_pt'], 'points': points, 'anomalies': anomalies, 'notes': notes,
           'design': CAL['design'], 'limitation': CAL['limitation']},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 校正の管理図（機械生成・`tools/control_chart_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- %s' % CAL['design'], '- 帯 %g pt・%s・相手は初点（同じ腕 × 場面の最初のセッション）。' % (CAL['band_pt'], CAL['test']),
     '- **帯の外の点 %d 件**。点が一つしかないセル %d 件。' % (len(anomalies), len(notes)), '',
     '| 場面 | 腕 | セッション | 破局/n_ok | 率 | 初点との差 pt | p | 判定 |', '|---|---|---|---|---|---|---|---|']
for p_ in points:
    L.append('| %s | %s | %s | %d/%d | %s | %s | %s | %s |'
             % (p_['scenario'], p_['arm'], p_['session'], p_['k'], p_['n'],
                None if p_['rate'] is None else round(p_['rate'], 4), p_.get('diff_pt', '—'),
                ('%.4g' % p_['p']) if p_.get('p') is not None else '—', p_['verdict']))
if notes:
    L += ['', '## 注（限界）', ''] + ['- ' + n for n in notes]
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[control_chart_B] %s | 点 %d・帯の外 %d・点が一つのセル %d' % (out_md, len(points), len(anomalies), len(notes)))
sys.exit(1 if anomalies else 0)
