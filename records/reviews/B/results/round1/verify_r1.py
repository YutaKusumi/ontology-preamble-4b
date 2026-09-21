# -*- coding: utf-8 -*-
"""公開前検分・第一巡の四票の事実の主張を、公開の試行の記録と集計の記録から数え直す（登録の外・事後の確かめ・札は作らない）。
用法: python records/reviews/B/results/round1/verify_r1.py  → verify-r1-machine.json を書き、端末に印字する。"""
import os, json, glob, math
from scipy import stats

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
OUT = {}


def trials(tag, scen, arm):
    d = j('results', tag, '%s__%s__%s__s1' % (tag, scen, arm))
    f = glob.glob(os.path.join(d, 'trials-*.jsonl'))
    assert len(f) == 1, (tag, scen, arm, f)
    return [json.loads(l) for l in open(f[0], encoding='utf-8')]


def by_dir(rows):
    D = {}
    for r in rows:
        if r['status'] != 'ok':
            continue
        k = r['direction_id']
        D.setdefault(k, [0, 0])
        D[k][1] += 1
        D[k][0] += bool(r['catastrophe'])
    return D


def kn(rows):
    ok = [r for r in rows if r['status'] == 'ok']
    return sum(bool(r['catastrophe']) for r in ok), len(ok)


# ---- V1: 方向ごとの率・一番近い一本との Fisher・方向を単位にした t（自由度 2）・等質性 χ² ----
ROWS = [('sub:S1', 'S1', 'O-Ncold-v', 'O-Ncold-vrand'), ('sub:SK', 'SK', 'O-Ncold-v', 'O-Ncold-vrand'),
        ('sub:S4', 'S4', 'O-Ncold-v', 'O-Ncold-vrand'), ('sub:N1', 'N1', 'O-Ncold-v', 'O-Ncold-vrand'),
        ('add:S1', 'S1', 'Onull+v', 'Onull+vrand'), ('add:SK', 'SK', 'Onull+v', 'Onull+vrand'),
        ('add:S4', 'S4', 'Onull+v', 'Onull+vrand'), ('add:N1', 'N1', 'Onull+v', 'Onull+vrand'),
        ('cross:S1:Onull', 'S1', 'Onull+vNk', 'Onull+vrand'), ('cross:S4:Onull', 'S4', 'Onull+vNk', 'Onull+vrand')]
V1 = []
for cid, scen, A, B in ROWS:
    ka, na = kn(trials('stageB', scen, A))
    D = by_dir(trials('stageB', scen, B))
    ra = ka / na
    dirs = sorted(D.items())
    rates = [k / n for _, (k, n) in dirs]
    near = min(dirs, key=lambda kv: abs(kv[1][0] / kv[1][1] - ra))
    p_near = stats.fisher_exact([[ka, na - ka], [near[1][0], near[1][1] - near[1][0]]])[1]
    m = sum(rates) / 3
    sd = math.sqrt(sum((x - m) ** 2 for x in rates) / 2)
    t = (ra - m) / (sd * math.sqrt(1 + 1 / 3)) if sd else float('nan')     # v の腕の率は固定とみなす粗い事後の計算
    p_t = 2 * stats.t.sf(abs(t), 2)
    se2 = sd ** 2 / 3 + ra * (1 - ra) / na                                  # 票の形（三本の平均の標準誤差＋v の腕の二項の分散）
    t2 = (ra - m) / math.sqrt(se2) if se2 else float('nan')
    p_t2 = 2 * stats.t.sf(abs(t2), 2)
    chi = stats.chi2_contingency([[k for _, (k, n) in dirs], [n - k for _, (k, n) in dirs]])
    V1.append(dict(id=cid, A='%d/%d' % (ka, na), rate_A_pt=round(100 * ra, 1),
                   dirs={d: '%d/%d' % (k, n) for d, (k, n) in dirs}, rates_pt=[round(100 * x, 1) for x in rates],
                   nearest=near[0], nearest_diff_pt=round(100 * (ra - near[1][0] / near[1][1]), 1), p_fisher_nearest=round(p_near, 4),
                   t_pred_df2=round(t, 3), p_t_pred_df2=round(p_t, 4), t_mean_df2=round(t2, 3), p_t_mean_df2=round(p_t2, 4), chi2_homog_p=round(chi[1], 4)))
OUT['V1_by_direction'] = V1

# ---- V2: 無操作との差（v の腕・ランダムの腕） ----
V2 = []
for scen in ('N1', 'S1', 'SK', 'S4'):
    for base, v, r in (('O-Ncold', 'O-Ncold-v', 'O-Ncold-vrand'), ('Onull', 'Onull+v', 'Onull+vrand')):
        kb, nb = kn(trials('stageB', scen, base)); kv, nv = kn(trials('stageB', scen, v)); kr, nr = kn(trials('stageB', scen, r))
        p_r = stats.fisher_exact([[kr, nr - kr], [kb, nb - kb]])[1]
        V2.append(dict(scenario=scen, base=base, noop='%d/%d' % (kb, nb), v_minus_noop_pt=round(100 * (kv / nv - kb / nb), 1),
                       rand_minus_noop_pt=round(100 * (kr / nr - kb / nb), 1), p_rand_vs_noop=round(p_r, 3),
                       rand_dirs_minus_noop_pt={d: round(100 * (k / n - kb / nb), 1) for d, (k, n) in sorted(by_dir(trials('stageB', scen, r)).items())}))
OUT['V2_vs_noop'] = V2

# ---- V3: S4 の反証の三腕 ----
V3 = {}
for arm in ('Osec-Ncold', 'Osec-Ncold+v6b', 'Osec-Ncold+vrand'):
    rows = [r for r in trials('stageB', 'S4', arm) if r['status'] == 'ok']
    ch = {}
    for r in rows:
        ch[r['choice']] = ch.get(r['choice'], 0) + 1
    V3[arm] = dict(cat='%d/%d' % kn(rows), choices=ch, style_a_pt=round(100 * sum(bool(r['style_a']) for r in rows) / len(rows), 1),
                   style_b_pt=round(100 * sum(bool(r['style_b']) for r in rows) / len(rows), 1))
    if arm.endswith('vrand'):
        per = {}
        for r in rows:
            e = per.setdefault(r['direction_id'], dict(n=0, cat=0, choices={}, style_a=0))
            e['n'] += 1; e['cat'] += bool(r['catastrophe']); e['style_a'] += bool(r['style_a'])
            e['choices'][r['choice']] = e['choices'].get(r['choice'], 0) + 1
        V3[arm]['per_direction'] = per
        ks = [(e['cat'], e['n']) for _, e in sorted(per.items())]
        V3[arm]['chi2_homog_p'] = round(stats.chi2_contingency([[k for k, n in ks], [n - k for k, n in ks]])[1], 5)
OUT['V3_S4'] = V3

# ---- V4: refuse の数え方（choice == 'refuse' と route == 'json_refuse' の一致） ----
mis = 0; tot = 0
for d in glob.glob(j('results', 'stageB', '*')):
    for f in glob.glob(os.path.join(d, 'trials-*.jsonl')):
        for l in open(f, encoding='utf-8'):
            r = json.loads(l); tot += 1
            mis += ((r.get('choice') == 'refuse') != ((r.get('refuse_class') or {}).get('route') == 'json_refuse'))
OUT['V4_refuse_def'] = dict(trials=tot, mismatch=mis)

# ---- V5: 調整走行の選ばれた組（層 0.5 × 係数 2.0） ----
V5 = {}
for d in glob.glob(j('results', 'tuneB', '*')):
    for f in glob.glob(os.path.join(d, 'trials-*.jsonl')):
        rows = [json.loads(l) for l in open(f, encoding='utf-8')]
        rows = [r for r in rows if r['status'] == 'ok' and r.get('layer') == 0.5 and r.get('coef') == 2.0]
        for r in rows:
            e = V5.setdefault('%s|%s' % (r['scenario'], r['arm']), [0, 0]); e[1] += 1; e[0] += bool(r['catastrophe'])
OUT['V5_tune_pick'] = {k: '%d/%d' % tuple(v) for k, v in sorted(V5.items())}

# ---- V6: Nk 方向の様式（JSON の直答） ----
V6 = {}
for scen in ('N1', 'S1', 'SK', 'S4'):
    for arm in ('O-Ncold+vNk', 'O-Ncold+vrand', 'Onull+vNk', 'Onull+vrand'):
        rows = [r for r in trials('stageB', scen, arm) if r['status'] == 'ok']
        V6['%s|%s' % (scen, arm)] = dict(cat='%d/%d' % kn(rows), style_a_pt=round(100 * sum(bool(r['style_a']) for r in rows) / len(rows), 1),
                                         style_b_pt=round(100 * sum(bool(r['style_b']) for r in rows) / len(rows), 1))
OUT['V6_Nk_style'] = V6

# ---- V7: 同一性選別の三対 ----
I = json.load(open(j('records', 'B', 'identity-screen-B.json'), encoding='utf-8'))
OUT['V7_identity_keys'] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__ + ':%d' % len(v)) for k, v in I.items()}

# ---- V8: 集計の記録の不均一の注と確証の札 ----
A = json.load(open(j('records', 'B', 'analysis-B-devB1-2026-09-22.json'), encoding='utf-8'))
conf = [r for r in A['confirm'] if r['label'].startswith('確証')]
OUT['V8_confirmed_with_note'] = [dict(id=r['id'], deviation=r.get('deviation'), note=bool((r.get('homogeneity') or {}).get('note')), spread_pt=round((r.get('homogeneity') or {}).get('spread_pt', 0), 1)) for r in conf]

json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify-r1-machine.json'), 'w', encoding='utf-8', newline=chr(10)), ensure_ascii=False, indent=1)
print(json.dumps(OUT, ensure_ascii=False, indent=1))
