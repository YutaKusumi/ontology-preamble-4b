# -*- coding: utf-8 -*-
"""gate_vprime.py v2 —— 追補 V′ の門（GO/NO-GO）。判定規則は `design/contrasts-Vprime.json` だけから読む（手書きの対比辞書を持たない・D-5 再発防止）。
v2（二巡目反映）: 参照キーを id/scenario/A/B/direction/gate に限定／`gate` 欄と `direction` の整合を検査（不整合は非零終了）／対照 B の n_ok が pilot_n に満たない場合は判定せず非零終了
（--redo-errors で揃えてから）／結果を Markdown と **JSON**（集計器が読む正本）に書き、同名があれば上書きせず連番。
用法: python tools/gate_vprime.py --tag pilotVp
"""
import os, sys, json, glob, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='pilotVp'); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-Vprime.json'))
ap.add_argument('--allow-short', action='store_true', help='dry-run 検査用: n_ok < pilot_n でも率で判定（本番では用いない）')
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8')); G = T['gate_counts']
KEYS = ('id', 'scenario', 'A', 'B', 'direction', 'gate')
cells = {}
for f in glob.glob(os.path.join(REPO, 'results', '*', args.tag + '__*', 'cells.json')):   # 走行ディレクトリは <tag>__… で始まる（dry-run は results/_dryrun/ 配下）
    d = json.load(open(f, encoding='utf-8')); cells[d['manifest']['scenario']] = d['cells']
res = {'tag': args.tag, 'contrasts_version': T['version'], 'gate_counts': G, 'when': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'results': {}}
out = ['# 追補 V′ 門の判定 —— %s（tag %s・規則 %s）' % (datetime.date.today().isoformat(), args.tag, T['version']), '',
       '規則: 上向き対比＝対照 B の破局が %d/%d 以上で天井（記述に降格）／下向き対比＝対照 B の破局が %d/%d 以下で床（記述に降格）。m は減らさない。対照の n_ok が %d に満たない対比は判定しない。' % (G['ceiling_min_catastrophes'], G['pilot_n'], G['floor_max_catastrophes'], G['pilot_n'], G['pilot_n']), '']
errors = []
for fam, F in T['families'].items():
    out.append('## 族 %s（m=%d）' % (fam, F['m'])); out.append('| 対比 | 向き | 門 | 対照 B 破局/n_ok | A 破局/n_ok | 判定 |'); out.append('|---|---|---|---|---|---|')
    for c in F['contrasts']:
        c = {k: c[k] for k in KEYS}
        if (c['direction'], c['gate']) not in (('up', 'ceiling_on_B'), ('down', 'floor_on_B')):
            errors.append('向きと門が不整合: %s (%s, %s)' % (c['id'], c['direction'], c['gate'])); continue
        cB = cells.get(c['scenario'], {}).get(c['B']); cA = cells.get(c['scenario'], {}).get(c['A'])
        if not cB:
            out.append('| %s | %s | %s | （未走行） | — | 判定不能 |' % (c['id'], c['direction'], c['gate'])); res['results'][c['id']] = {'status': 'not_run'}; continue
        kB, nB = cB['catastrophe'], cB['n_ok']
        if nB != G['pilot_n'] and not args.allow_short:
            errors.append('対照 %s（%s）の n_ok=%d ≠ pilot_n=%d——--redo-errors で揃えてから判定' % (c['B'], c['scenario'], nB, G['pilot_n'])); continue
        thr_c = G['ceiling_min_catastrophes'] * nB / G['pilot_n']; thr_f = G['floor_max_catastrophes'] * nB / G['pilot_n']
        down = (kB >= thr_c) if c['direction'] == 'up' else (kB <= thr_f)
        why = ('天井（対照 %d/%d ≥ %g）' % (kB, nB, thr_c)) if c['direction'] == 'up' else ('床（対照 %d/%d ≤ %g）' % (kB, nB, thr_f))
        res['results'][c['id']] = {'status': 'downgraded' if down else 'go', 'B_catastrophe': kB, 'B_n_ok': nB, 'A_catastrophe': (cA or {}).get('catastrophe'), 'A_n_ok': (cA or {}).get('n_ok'), 'reason': why if down else None}
        out.append('| %s | %s | %s | %d/%d | %s/%s | %s |' % (c['id'], c['direction'], c['gate'], kB, nB, (cA or {}).get('catastrophe'), (cA or {}).get('n_ok'), ('**記述に降格**・' + why) if down else 'GO'))
    out.append('')
if errors:
    print('\n'.join('[gate] ' + e for e in errors)); sys.exit(2)
out.append('本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
os.makedirs(os.path.join(REPO, 'records', 'vprime'), exist_ok=True)
base = os.path.join(REPO, 'records', 'vprime', 'gate-%s-%s' % (args.tag, datetime.date.today().isoformat())); p = base; k = 2
while os.path.exists(p + '.md') or os.path.exists(p + '.json'):
    p = '%s-%d' % (base, k); k += 1
open(p + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(res, open(p + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('written', p + '.md', p + '.json')
