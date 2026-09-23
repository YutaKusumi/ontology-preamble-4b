# -*- coding: utf-8 -*-
"""第二巡の四票の事実の主張を、事後の計算の記録・集計の記録・報告の現物から確かめる（登録の外・事後・札は作らない）。
用法: python records/reviews/B/results/round2/verify_r2.py → verify-r2-machine.json"""
import os, json, math, re
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
PH = json.load(open(j('records', 'B', 'posthoc-by-direction-B-2026-09-22.json'), encoding='utf-8'))
DV = json.load(open(j('records', 'B', 'analysis-B-devB1-2026-09-22.json'), encoding='utf-8'))
cover = open(j('records', 'B', 'results-B.md'), encoding='utf-8').read()
mrep = open(j('records', 'B', 'results-report-B-devB1.md'), encoding='utf-8').read()
frep = open(j('records', 'B', 'results-report-B-frozen.md'), encoding='utf-8').read()
OUT = {}
lab = {r['id']: r for r in DV['confirm']}
rows = []
for c in PH['contrasts']:
    ra = c['k_A'] / c['n_A']; rs = [d['cat'] / d['n_ok'] for d in c['directions']]; ns = [d['n_ok'] for d in c['directions']]
    outside = ra > max(rs) or ra < min(rs)
    m = sum(rs) / 3; sd2 = sum((x - m) ** 2 for x in rs) / 2
    binom = sum(x * (1 - x) / n for x, n in zip(rs, ns)) / 3            # 一本の二項の分散の平均
    between = max(sd2 - binom, 0.0)                                       # モーメント法の方向の間の分散
    floor_sd2 = max(sd2, binom)                                           # 二項の期待値を下限に置いた分散
    se_floor = math.sqrt(floor_sd2 * (1 + 1 / 3) + ra * (1 - ra) / c['n_A'])
    p_floor = 2 * stats.t.sf(abs(ra - m) / se_floor, 2)
    rows.append(dict(id=c['id'], label=lab[c['id']]['label'][:2], deviation=lab[c['id']].get('deviation'), rate_A_pt=round(100 * ra, 1),
                     range_pt=[round(100 * min(rs), 1), round(100 * max(rs), 1)], outside=outside, nearest_diff_pt=c['nearest_diff_pt'],
                     p_fisher_nearest=c['p_fisher_nearest'], p_form1=c['p_t_mean_df2'], p_form2=c['p_t_pred_df2'], p_chi2=c['p_chi2_homogeneity'],
                     sd_three_pt=round(100 * math.sqrt(sd2), 1), binom_expected_sd_pt=round(100 * math.sqrt(binom), 1),
                     between_sd_pt=round(100 * math.sqrt(between), 1), p_form2_floor=round(p_floor, 4)))
OUT['rows'] = rows
conf = [r for r in rows if r['label'] == '確証']
OUT['outside_count'] = dict(all=sum(r['outside'] for r in rows), of=len(rows), confirmed=sum(r['outside'] for r in conf), of_confirmed=len(conf))
# 事後の一番近い一本との Fisher に Holm（16 本）
ps = sorted((r['p_fisher_nearest'], r['id']) for r in rows)
holm = [(i, p * (16 - k) <= 0.05) for k, (p, i) in enumerate(ps)]
OUT['holm16_nearest'] = [i for i, ok in holm if ok]
OUT['form2_lt05'] = [r['id'] for r in rows if r['p_form2'] < 0.05]
OUT['all_three_lt05'] = [r['id'] for r in rows if r['p_fisher_nearest'] < 0.05 and r['p_form1'] < 0.05 and r['p_form2'] < 0.05]
OUT['rank_bound'] = dict(one_sided=0.25, two_sided=0.5, note='四本が交換可能なら、v̂ が三本の外に出る確率は片側 1/4・両側 1/2')
# 符号の一致の内訳
sa = [r for r in DV['confirm'] if r['label'].startswith('確証')]
agree = lambda rr: sum(1 for r in rr if r.get('fired') is not None and r.get('sign_agree'))
OUT['sign_agreement_keys'] = sorted(set(k for r in sa for k in r.keys() if 'seal' in k or 'agree' in k or 'sign' in k))
OUT['confirmed_split'] = dict(pre=[r['id'] for r in sa if not r.get('deviation')], dev=[r['id'] for r in sa if r.get('deviation')])
# 逸脱の下の機械の報告で、印の無い「確証」の本数がどこにあるか
OUT['devB1_report_unmarked_counts'] = [(m.start(), mrep[max(0, m.start() - 40):m.start() + 20].replace(chr(10), ' ')) for m in re.finditer(r'確証 ?\d', mrep)]
OUT['frozen_report_quality_floor_head'] = [(m.start(), frep[max(0, m.start() - 30):m.start() + 30].replace(chr(10), ' ')) for m in re.finditer(r'判定不能（品質床） ?8', frep)][:3]
# 表紙の現物: §6 に相手の腕の共有があるか／§0 に過半の文があるか／§0 の点に印があるか
sec6 = cover[cover.index('## 6.'):cover.index('## 7.')]; sec0 = cover[cover.index('## 0.'):cover.index('## 1.')]
OUT['cover_checks'] = dict(sec6_shared_arm='同じランダムの腕' in sec6 or '相手にして' in sec6, sec0_majority='過半' in sec0,
                           sec0_point_without_dev_mark=[l[:40] for l in sec0.split(chr(10)) if l.startswith('- **区別できた相手')],
                           sec6_conclusion=[l[-120:] for l in sec6.split(chr(10)) if '言えるのは' in l],
                           cover_says_family='家族' in sec0)
json.dump(OUT, open(os.path.join(HERE, 'verify-r2-machine.json'), 'w', encoding='utf-8', newline=chr(10)), ensure_ascii=False, indent=1)
for r in rows:
    print('%-38s %s out=%s near %+6.1f  sd3 %4.1f binom %4.1f between %4.1f  p2 %.3f floor %.3f' % (r['id'], r['label'], r['outside'], r['nearest_diff_pt'], r['sd_three_pt'], r['binom_expected_sd_pt'], r['between_sd_pt'], r['p_form2'], r['p_form2_floor']))
print({k: v for k, v in OUT.items() if k != 'rows'})
