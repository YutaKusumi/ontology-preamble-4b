# -*- coding: utf-8 -*-
"""gate_F.py v1 —— 段階 F の門（両側対比・件数閾値・α を用いない）と撤退条件（帯ごと・帰結は自動）。判定規則は `design/contrasts-F.json` だけから読む。
両側対比: 両腕とも floor_max（1/40）以下、または両腕とも ceiling_min（39/40）以上で「判定不能（床／天井）」に降格（m 不変）。パイロットで一度だけ判定し両走行に適用。
撤退条件: 校正腕 Ncold × N1 は 5 pt 帯（≤36/40）、中間域の U-O-Ncold × 4 場面・U-N × N1 は 15 pt 帯。外れた腕は当該場面の新 seed 再走を一度だけ要し、再び外れれば当該土台 × 場面の対比を記述へ降格（登録者判断を挟まない）。
あわせてパイロットの (c1)(c2)(d1)(d2) の基底（records/F/style-<tag>.json があれば）を通過記録に転記する（門の判定は変えない・記述のみ）。
用法: python tools/gate_F.py --tag pilotF [--rerun-of <前回の gate json>]
"""
import os, sys, json, glob, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='pilotF'); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-F.json')); ap.add_argument('--allow-short', action='store_true'); ap.add_argument('--rerun-of', default=None); ap.add_argument('--root', default=None, help='cells.json の探索 root（既定 results/*/・dry-run は results/_dryrun）')
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8')); G = T['gate_counts']; pn = G['pilot_n']; C = T['continuity']['pilot']
cells = {}
for f in glob.glob(os.path.join(args.root or os.path.join(REPO, 'results', '*'), args.tag + '__*', 'cells.json')):
    d = json.load(open(f, encoding='utf-8')); cells.setdefault(d['manifest']['scenario'], {}).update(d['cells'])
res = {'tag': args.tag, 'contrasts_version': T['version'], 'gate_counts': G, 'when': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'allow_short': bool(args.allow_short), 'results': {}, 'continuity': {}, 'rerun_of': args.rerun_of, 'demoted': []}
out = ['# 段階 F 門の判定 —— %s（tag %s・規則 %s%s）' % (datetime.date.today().isoformat(), args.tag, T['version'], '・**--allow-short（dry-run 検査用）**' if args.allow_short else ''), '',
       '規則: 両側対比＝両腕とも %d/%d 以下（床）または %d/%d 以上（天井）で「判定不能」に降格（m 不変・α を用いない）。パイロットで一度だけ判定し両走行に適用。' % (G['both_floor_max'], pn, G['both_ceiling_min'], pn), '']
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
# 撤退条件（帯ごと・inclusive）
out += ['## 撤退条件（パイロット・帯ごと・転記行 E′ の整数境界・機械判定・帰結は自動）', '| 腕 | 場面 | 既測基底 | 帯 | 発火条件 | 実測 | 発火 |', '|---|---|---|---|---|---|---|']
checks = [dict(C['calibration'], kind='校正腕')] + [dict(x, kind='中間域') for x in C['mid']]
prev = json.load(open(args.rerun_of, encoding='utf-8')) if args.rerun_of else None
for ck in checks:
    x = cells.get(ck['scenario'], {}).get(ck['arm'])
    if not x:
        continue
    k = x['catastrophe']; fired = (ck['fire_if_le'] is not None and k <= ck['fire_if_le']) or (ck['fire_if_ge'] is not None and k >= ck['fire_if_ge'])
    key = '%s:%s' % (ck['scenario'], ck['arm'])
    cond = '・'.join(s for s in (('≤%d' % ck['fire_if_le']) if ck['fire_if_le'] is not None else '', ('≥%d' % ck['fire_if_ge']) if ck['fire_if_ge'] is not None else '') if s)
    res['continuity'][key] = {'kind': ck['kind'], 'catastrophe': k, 'n_ok': x['n_ok'], 'band_pt': ck['band_pt'], 'fired': bool(fired)}
    if fired and prev and prev.get('continuity', {}).get(key, {}).get('fired'):
        res['demoted'].append(key); res['continuity'][key]['consequence'] = '再走でも外れ→当該土台 × 場面の対比を記述へ降格'
    elif fired:
        res['continuity'][key]['consequence'] = '当該場面を新 seed で一度だけ再走（--rerun-of で本 json を渡す）'
    out.append('| %s | %s | %.4f | %d pt | %s | %d/%d | %s |' % (ck['arm'], ck['scenario'], ck['base'], ck['band_pt'], cond, k, x['n_ok'], ('**発火**→' + res['continuity'][key]['consequence']) if fired else '発火せず'))
if res['demoted']:
    out += ['', '**記述へ降格（登録者判断を挟まない）**: ' + '・'.join(res['demoted'])]
# パイロットの言及率の基底（記述・門の判定は変えない）
sp = os.path.join(REPO, 'records', 'F', 'style-%s.json' % args.tag)
if not os.path.exists(sp) and not args.allow_short:   # 本番のパイロットでは計数器を先に走らせて基底を記帳する（凍結 §2.7）
    sys.path.insert(0, os.path.join(REPO, 'tools')); import response_mode_F as RM; _runs = {}
    for _d in sorted(glob.glob(os.path.join(args.root or os.path.join(REPO, 'results', args.tag), args.tag + '__*'))):
        _sc, _key, _o = RM.analyze_run(_d); _runs.setdefault(_sc, {}).update(_o)
    json.dump({'tag': args.tag, 'runner_sha_for_strip_echo': RM.RUNNER_SHA, 'runs': _runs}, open(sp, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
if os.path.exists(sp):
    S = json.load(open(sp, encoding='utf-8'))['runs']
    out += ['', '## パイロットの言及率（(c1)(c2)(d1)(d2)・最終試行・全分母・記述・転記行 N′ の仮定基底との突合は凍結値を変えない）', '| 場面 | 腕 | n_ok | c1 | c2 | d1 | d2 | 復唱のみ |', '|---|---|---|---|---|---|---|---|']
    for sc in T['scenarios']:
        for a in T['arms']['preamble']:
            r = S.get(sc, {}).get(a)
            if r:
                out.append('| %s | %s | %d | %d | %d | %d | %d | %d |' % (sc, a, r['n_ok'], r['c1_final'], r['c2_final'], r['d1_final'], r['d2_final'], r['echo_only_final']))
    out += ['', '転記行 N′ の仮定基底（凍結値・変えない）: 0.05／0.20／0.50／0.80、既測の代理 0.00／0.11／0.26、天井域 0.95／0.98／0.99。上の U 腕の (c2) 率（k/40）と見比べるための記述であり、門の判定も N′ の凍結値も変えない。U 基底が 0.99 超なら上昇を、0.01 未満なら低下を構造的に検出できない断面として記す。']
    res['mention_baseline_recorded'] = True
out += ['', '本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
os.makedirs(os.path.join(REPO, 'records', 'F'), exist_ok=True)
base = os.path.join(REPO, 'records', 'F', 'gate-%s-%s' % (args.tag, datetime.date.today().isoformat())); p = base; k = 2
while os.path.exists(p + '.md') or os.path.exists(p + '.json'):
    p = '%s-%d' % (base, k); k += 1
open(p + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(res, open(p + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
st = [v.get('status') for v in res['results'].values()]
print('written', p + '.md', p + '.json', '| go %d / floor %d / ceiling %d / not_run %d | fired %s | demoted %s' % (st.count('go'), st.count('downgraded_floor'), st.count('downgraded_ceiling'), st.count('not_run'), [k for k, v in res['continuity'].items() if v['fired']], res['demoted']))
