# -*- coding: utf-8 -*-
"""posthoc_by_direction_B.py v2 —— **登録の外・事後の計算**（登録者裁定 D155・D158・公開前検分の第一巡 K241〜K246 と第二巡 K275〜K277 を受けて）。
v2 で足したもの: 三本の率の範囲、モーメント法の方向の間のばらつき（三本の率の分散から一本の二項の分散の平均を引く）、**下限つきの形**（三本の分散に二項の期待を下限として置いた予測の形・自由度 2）、順位の下限（交換可能なら v̂ が三本の外に出る確率は両側 1/2）、突き合わせの範囲の拡張（全十六行を試行の記録から数え直し、件数・Fisher・形一・形二・χ²・下限つきの形を照合）。
確証の族の 16 対比について、ランダム方向の一本ごとの率（凍結した集計器の出力 `by_direction`）から、(a) v の腕に一番近い一本との両側 Fisher、
(b) 方向を単位にした t（自由度 2・二つの形）、(c) 三本の等質性の χ² を計算する。S4 の反証の三腕の選択の内訳と、調整走行の選ばれた組の場面ごとの件数も数える。
**札を作らず、札を取り下げもしない。** 三本では方向の間のばらつきは見積もれず、(b) は形で値が動くので二つの形を並べる。
用法: python records/B/posthoc_by_direction_B.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, json, glob, math, hashlib, datetime
from scipy import stats

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FZ = json.load(open(j('records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
DV = json.load(open(j('records', 'B', 'analysis-B-devB1-2026-09-22.json'), encoding='utf-8'))
assert FZ['by_direction'] == DV['by_direction'], '方向ごとの件数が二つの出力で違う'
BD = {}
for r in DV['by_direction']:
    BD.setdefault((r['scenario'], r['arm']), []).append(r)


def trials(tag, scen, arm):
    f = glob.glob(j('results', tag, '%s__%s__%s__s1' % (tag, scen, arm), 'trials-*.jsonl'))
    assert len(f) == 1, (tag, scen, arm)
    return [r for r in (json.loads(l) for l in open(f[0], encoding='utf-8')) if r['status'] == 'ok']


def per_direction(scen, arm, ka, na):
    rows = sorted(BD[(scen, arm)], key=lambda r: r['direction_id'])
    assert len(rows) == 3 and all(r['n_ok'] == r['n'] for r in rows), (scen, arm)
    ks = [(r['cat'], r['n_ok']) for r in rows]
    rates = [k / n for k, n in ks]
    ra = ka / na
    i = min(range(3), key=lambda x: abs(rates[x] - ra))
    p_near = stats.fisher_exact([[ka, na - ka], [ks[i][0], ks[i][1] - ks[i][0]]])[1]
    m = sum(rates) / 3
    sd = math.sqrt(sum((x - m) ** 2 for x in rates) / 2)
    se_mean = math.sqrt(sd ** 2 / 3 + ra * (1 - ra) / na)          # 形一: 三本の平均の標準誤差 ＋ v の腕の二項の分散
    se_pred = math.sqrt(sd ** 2 * (1 + 1 / 3) + ra * (1 - ra) / na)  # 形二: v の腕が同じ母集団からの一本か（予測の形）
    p_mean = 2 * stats.t.sf(abs((ra - m) / se_mean), 2) if se_mean else None
    p_pred = 2 * stats.t.sf(abs((ra - m) / se_pred), 2) if se_pred else None
    binom = sum(x * (1 - x) / n for x, n in zip(rates, [r['n_ok'] for r in rows])) / 3   # 一本の二項の分散の平均
    between = max(sd ** 2 - binom, 0.0)                                                    # モーメント法の方向の間の分散
    se_floor = math.sqrt(max(sd ** 2, binom) * (1 + 1 / 3) + ra * (1 - ra) / na)           # 下限つきの形（二項の期待を分散の下限に置く）
    p_floor = 2 * stats.t.sf(abs((ra - m) / se_floor), 2)
    outside = ra > max(rates) or ra < min(rates)
    chi = stats.chi2_contingency([[k for k, n in ks], [n - k for k, n in ks]])[1] if 0 < sum(k for k, n in ks) < sum(n for k, n in ks) else None
    return dict(directions=[dict(direction_id=r['direction_id'], cat=r['cat'], n_ok=r['n_ok'], rate_pt=round(100 * r['cat'] / r['n_ok'], 1), style_b=r['style_b']) for r in rows],
                nearest=rows[i]['direction_id'], nearest_diff_pt=round(100 * (ra - rates[i]), 1), p_fisher_nearest=p_near,
                p_t_mean_df2=p_mean, p_t_pred_df2=p_pred, p_chi2_homogeneity=chi,
                range_pt=[round(100 * min(rates), 1), round(100 * max(rates), 1)], outside_range=outside, sd_three_pt=round(100 * sd, 2),
                binom_expected_sd_pt=round(100 * math.sqrt(binom), 2), between_sd_pt=round(100 * math.sqrt(between), 2), p_t_floor_df2=p_floor)


OUT = dict(kind='posthoc_by_direction_B', version='v2', status='登録の外・事後の計算（札を作らない・札を取り下げない）', ruling='D155・D158',
           rank_bound=dict(one_sided=0.25, two_sided=0.5, note='四本が交換可能なら、v̂ が三本の外に出る確率は片側 1/4・両側 1/2。順位だけからは両側 0.5 より強いことは言えない'),
           generated_utc=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
           inputs={'analysis_devB1': s16(j('records', 'B', 'analysis-B-devB1-2026-09-22.json')), 'analysis_frozen': s16(j('records', 'B', 'analysis-B-2026-09-22.json'))},
           forms={'mean': '形一: 三本の率の平均と v の腕の率の差を、三本の平均の標準誤差と v の腕の二項の分散で割る（自由度 2）。問い「v̂ が分布から出た一本と見分けられるか」に対しては甘い側',
                  'pred': '形二: v の腕が三本と同じ母集団からの一本かを見る（予測の形・自由度 2）。三本の分散には一本の二項の揺れが既に入り、v の腕の二項の分散を重ねて数える',
                  'floor': '下限つきの形（表紙に載せる一列）: 形二の三本の分散に、一本の二項の分散の平均を下限として置く。三本が偶然よく揃った行で分散が小さく出ることを抑える。自由度 2'},
           contrasts=[])
for r in DV['confirm']:
    e = per_direction(r['scenario'], r['B'], r['k_A'], r['n_ok_A'])
    assert sum(d['cat'] for d in e['directions']) == r['k_B'] and sum(d['n_ok'] for d in e['directions']) == r['n_ok_B'], r['id']
    OUT['contrasts'].append(dict(id=r['id'], scenario=r['scenario'], A=r['A'], B=r['B'], k_A=r['k_A'], n_A=r['n_ok_A'], **e))

# S4 の反証の三腕（選択の内訳は集計の記録に無いので、試行の記録から数える）
s4 = DV['s4']
S4 = {}
for arm in ('Osec-Ncold', 'Osec-Ncold+v6b', 'Osec-Ncold+vrand'):
    rows = trials('stageB', 'S4', arm)
    ch = {}
    for t in rows:
        ch[t['choice']] = ch.get(t['choice'], 0) + 1
    S4[arm] = dict(cat=sum(bool(t['catastrophe']) for t in rows), n_ok=len(rows), choices=dict(sorted(ch.items())), style_b=sum(bool(t['style_b']) for t in rows))
    if arm.endswith('vrand'):
        per = {}
        for t in rows:
            q = per.setdefault(t['direction_id'], dict(cat=0, n_ok=0, choices={}, style_b=0))
            q['cat'] += bool(t['catastrophe']); q['n_ok'] += 1; q['style_b'] += bool(t['style_b']); q['choices'][t['choice']] = q['choices'].get(t['choice'], 0) + 1
        S4[arm]['per_direction'] = {k: dict(v, choices=dict(sorted(v['choices'].items()))) for k, v in sorted(per.items())}
assert S4['Osec-Ncold+v6b']['cat'] == s4['k_A'] and S4['Osec-Ncold+vrand']['cat'] == s4['k_B']
e = per_direction('S4', 'Osec-Ncold+vrand', s4['k_A'], s4['n_A'])
S4['p_chi2_homogeneity'] = e['p_chi2_homogeneity']
OUT['s4'] = S4

# 調整走行の選ばれた組の場面ごとの件数
G = json.load(open(j('records', 'B', 'gate-B-2026-09-21.json'), encoding='utf-8'))
pick = G['selection']['pick']
TU = {}
for d in glob.glob(j('results', 'tuneB', '*')):
    for f in glob.glob(os.path.join(d, 'trials-*.jsonl')):
        for t in (json.loads(l) for l in open(f, encoding='utf-8')):
            if t['status'] == 'ok' and t.get('layer') == pick['layer'] and t.get('coef') == pick['coef']:
                q = TU.setdefault(t['scenario'], {}).setdefault(t['arm'], [0, 0]); q[0] += bool(t['catastrophe']); q[1] += 1
assert sum(TU[s]['Onull+v'][0] for s in TU) == pick['cat_v'] and sum(TU[s]['Onull+vrand'][0] for s in TU) == pick['cat_r'], '調整走行の件数が門の記録と合わない'
OUT['tune_pick'] = dict(layer=pick['layer'], coef=pick['coef'], by_scenario={s: {a: dict(cat=v[0], n_ok=v[1]) for a, v in sorted(x.items())} for s, x in sorted(TU.items())})

# 第一巡の数え直し（試行の記録から）との突き合わせ
V = json.load(open(j('records', 'reviews', 'B', 'results', 'round1', 'verify-r1-machine.json'), encoding='utf-8'))
ours = {c['id']: c for c in OUT['contrasts']}
n_chk = 0
for v in V['V1_by_direction']:
    hit = [c for k, c in ours.items() if k.startswith(v['id'].split(':Onull')[0] + ':') and c['B'] == ('Onull+vrand' if (v['id'].startswith('add') or 'Onull' in v['id']) else 'O-Ncold-vrand')
           and (('vNk' in c['A']) == v['id'].startswith('cross'))]
    assert len(hit) == 1, v['id']
    c = hit[0]
    assert ['%d/%d' % (d['cat'], d['n_ok']) for d in c['directions']] == list(v['dirs'].values()), v['id']
    assert abs(c['p_fisher_nearest'] - v['p_fisher_nearest']) < 1e-4 and abs(c['p_t_mean_df2'] - v['p_t_mean_df2']) < 1e-4, v['id']
    n_chk += 1
n16 = 0
for c in OUT['contrasts']:
    D = {}
    for t in trials('stageB', c['scenario'], c['B']):
        q = D.setdefault(t['direction_id'], [0, 0]); q[0] += bool(t['catastrophe']); q[1] += 1
    assert {d['direction_id']: [d['cat'], d['n_ok']] for d in c['directions']} == D, c['id']
    ka, na = kn2 = (sum(bool(t['catastrophe']) for t in trials('stageB', c['scenario'], c['A'])), len(trials('stageB', c['scenario'], c['A'])))
    assert (ka, na) == (c['k_A'], c['n_A']), c['id']
    e2 = per_direction(c['scenario'], c['B'], ka, na)
    for f in ('p_fisher_nearest', 'p_t_mean_df2', 'p_t_pred_df2', 'p_chi2_homogeneity', 'p_t_floor_df2'):
        assert (e2[f] is None and c[f] is None) or abs(e2[f] - c[f]) < 1e-12, (c['id'], f)
    n16 += 1
OUT['crosscheck'] = dict(against='records/reviews/B/results/round1/verify-r1-machine.json', rows=n_chk, fields=['方向ごとの件数', '一番近い一本との Fisher', '形一'],
                         note='第一巡の数え直し（十行・交差族の O-Ncold の土台は含まない）との照合。形二は v の腕の二項の分散を足した形で、第一巡の形とは値が少し違うので照合の外',
                         trials_recount=dict(rows=n16, fields=['A の腕の件数', '方向ごとの件数', 'Fisher', '形一', '形二', 'χ²', '下限つきの形'], note='全十六行を試行の記録から数え直した。同じ関数を通すので、確かめているのは集計の記録の件数と試行の記録の一致であって、式の独立な再計算ではない（式の再計算は第二巡の四票が申告）'))
OUT['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
out = j('records', 'B', 'posthoc-by-direction-B-2026-09-22.json')
json.dump(OUT, open(out, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('wrote', out, s16(out), 'crosscheck rows', n_chk, 'trials recount rows', n16)
for c in OUT['contrasts']:
    print('%-40s range %s out=%s near %+6.1f pt  p_near %.4f  floor %.4f  between %.1f' % (c['id'], c['range_pt'], c['outside_range'], c['nearest_diff_pt'], c['p_fisher_nearest'], c['p_t_floor_df2'], c['between_sd_pt']))
