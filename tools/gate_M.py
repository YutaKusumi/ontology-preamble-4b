# -*- coding: utf-8 -*-
"""gate_M.py v1 —— 追補 M の門（両側対比・件数閾値・α を用いない）。判定規則は `design/contrasts-M.json` だけから読む。
両側対比: 両腕とも floor_max（1/40）以下、または両腕とも ceiling_min（39/40）以上で「判定不能（床／天井）」に降格（m 不変）。両腕の n_ok が pilot_n に満たなければ判定しない（--redo-errors で揃える）。
パイロットで一度だけ判定し両走行に適用。あわせて撤退条件 (a)(b)(c)（continuity.pilot・pilot_c）を機械判定して印字する。
用法: python tools/gate_M.py --tag pilotM
"""
import os, sys, json, glob, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='pilotM'); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-M.json')); ap.add_argument('--allow-short', action='store_true')
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8')); G = T['gate_counts']; pn = G['pilot_n']
_ids = [c['id'] for F in list(T['families'].values()) + list(T['descriptive_families'].values()) for c in F['contrasts']]
if len(_ids) != len(set(_ids)):
    sys.exit('[gate] id が全族で一意でない')
cells = {}
for f in glob.glob(os.path.join(REPO, 'results', '*', args.tag + '__*', 'cells.json')):
    d = json.load(open(f, encoding='utf-8')); cells.setdefault(d['manifest']['scenario'], {}).update(d['cells'])
res = {'tag': args.tag, 'contrasts_version': T['version'], 'gate_counts': G, 'when': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'allow_short': bool(args.allow_short), 'results': {}, 'continuity': {}}
out = ['# 追補 M 門の判定 —— %s（tag %s・規則 %s%s）' % (datetime.date.today().isoformat(), args.tag, T['version'], '・**--allow-short（dry-run 検査用・本番判定ではない）**' if args.allow_short else ''), '',
       '規則: 両側対比＝両腕とも %d/%d 以下（床）または両腕とも %d/%d 以上（天井）で「判定不能」に降格（m は減らさない・α を用いない件数閾値）。両腕の n_ok が %d に満たない対比は判定しない。パイロットで一度だけ判定し両走行に適用。' % (G['both_floor_max'], pn, G['both_ceiling_min'], pn, pn), '']
errors = []
for fam, F in T['families'].items():
    out += ['## 族 %s（m=%d）' % (fam, F['m']), '| 対比 | A 破局/n_ok | B 破局/n_ok | 判定 |', '|---|---|---|---|']
    for c in F['contrasts']:
        A = cells.get(c['scenario'], {}).get(c['A']); B = cells.get(c['scenario'], {}).get(c['B'])
        if not A or not B:
            out.append('| %s | %s | %s | 判定不能（未走行） |' % (c['id'], '—' if not A else '%d/%d' % (A['catastrophe'], A['n_ok']), '—' if not B else '%d/%d' % (B['catastrophe'], B['n_ok']))); res['results'][c['id']] = {'status': 'not_run'}; continue
        kA, nA, kB, nB = A['catastrophe'], A['n_ok'], B['catastrophe'], B['n_ok']
        if nA == 0 or nB == 0:
            out.append('| %s | %d/%d | %d/%d | 判定不能（n_ok=0） |' % (c['id'], kA, nA, kB, nB)); res['results'][c['id']] = {'status': 'not_judgeable'}; continue
        if (nA != pn or nB != pn) and not args.allow_short:
            errors.append('%s: n_ok A %d・B %d ≠ pilot_n %d——--redo-errors で揃えてから判定' % (c['id'], nA, nB, pn)); continue
        fl = G['both_floor_max'] * nA / pn, G['both_floor_max'] * nB / pn; ce = G['both_ceiling_min'] * nA / pn, G['both_ceiling_min'] * nB / pn
        floor = kA <= fl[0] and kB <= fl[1]; ceil = kA >= ce[0] and kB >= ce[1]
        st = 'downgraded_floor' if floor else 'downgraded_ceiling' if ceil else 'go'
        res['results'][c['id']] = {'status': st, 'A_catastrophe': kA, 'A_n_ok': nA, 'B_catastrophe': kB, 'B_n_ok': nB, 'reason': ('床（両腕とも ≤%g）' % fl[0]) if floor else ('天井（両腕とも ≥%g）' % ce[0]) if ceil else None}
        out.append('| %s | %d/%d | %d/%d | %s |' % (c['id'], kA, nA, kB, nB, 'GO' if st == 'go' else '**判定不能（%s）**' % res['results'][c['id']]['reason']))
    out.append('')
if errors:
    print('\n'.join('[gate] ' + e for e in errors)); sys.exit(2)
# 撤退条件（パイロット）
C = T['continuity']; out += ['## 撤退条件（パイロット・転記行 E′ の閾値・機械判定）', '| 条件 | セル | 実測 | 発火 |', '|---|---|---|---|']
for sc in T['scenarios']:
    x = cells.get(sc, {}).get(C['pilot']['arm'])
    if x:
        fired = (x['catastrophe'] >= C['pilot']['N1_ge']) if sc == 'N1' else (x['catastrophe'] <= C['pilot']['S_le'])
        res['continuity']['%s:pilot' % sc] = {'catastrophe': x['catastrophe'], 'n_ok': x['n_ok'], 'fired': bool(fired), 'consequence': C['pilot']['consequence'] if fired else None}
        out.append('| (%s) %s %s | %s | %d/%d | %s |' % ('a' if sc == 'N1' else 'b', C['pilot']['arm'], ('≥%d' % C['pilot']['N1_ge']) if sc == 'N1' else ('≤%d' % C['pilot']['S_le']), sc, x['catastrophe'], x['n_ok'], '**発火**→' + C['pilot']['consequence'] if fired else '発火せず'))
    a = cells.get(sc, {}).get(C['pilot_c']['A']); b = cells.get(sc, {}).get(C['pilot_c']['B'])
    if a and b:
        diff = abs(a['catastrophe'] - b['catastrophe']); fired = diff >= C['pilot_c']['diff_ge']
        res['continuity']['%s:pilot_c' % sc] = {'A': a['catastrophe'], 'B': b['catastrophe'], 'diff': diff, 'fired': bool(fired)}
        out.append('| (c) |%s−%s| ≥%d | %s | %d 対 %d | %s |' % (C['pilot_c']['A'], C['pilot_c']['B'], C['pilot_c']['diff_ge'], sc, a['catastrophe'], b['catastrophe'], '**発火**→' + C['pilot_c']['consequence'] if fired else '発火せず'))
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
os.makedirs(os.path.join(REPO, 'records', 'M'), exist_ok=True)
base = os.path.join(REPO, 'records', 'M', 'gate-%s-%s' % (args.tag, datetime.date.today().isoformat())); p = base; k = 2
while os.path.exists(p + '.md') or os.path.exists(p + '.json'):
    p = '%s-%d' % (base, k); k += 1
open(p + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(res, open(p + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
st = [v.get('status') for v in res['results'].values()]
print('written', p + '.md', p + '.json', '| go %d / floor %d / ceiling %d / not_run %d' % (st.count('go'), st.count('downgraded_floor'), st.count('downgraded_ceiling'), st.count('not_run')))
