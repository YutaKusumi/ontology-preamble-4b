# -*- coding: utf-8 -*-
"""analyze_B.py v1 —— 段階 B の本走行の集計と札（確証の族・門・記述の族・印字）。

正本 `design/contrasts-B.json` に従う。**札は一つだけ**付け、ほかに当たった門は注に出す（`gate_order`）。
門の順（`gate_order.order`）:
  検閲（両腕条件）→ 希釈の門〔書式外の差〕→ 希釈の門〔refuse の差〕→ refuse 門〔答えた分母〕→ 様式門 → 品質床（選定後）
検定: 両側 Fisher・全分母（分子＝破局・分母＝n_ok）・Holm は族ごと（m は族ごと・**降格しても m は減らさない**・`censor.m_rule`）。
封印した予想符号（`families[*].sealed_sign`・`seal_format`）があれば、確証の札の向きと照らし、一致の数を印字する（裁定 D79）。
記述の族は p を印字しない（`print_strings.no_p_desc`）。S4 の反証は三分岐（`B_desc_S4.three_way`・裁定 D81）。
入力: 本走行（tag `stageB`）・門と選定の記録（`gate_B.py` の json）・品質床の**選定後**の走行・封印の記録（任意）。
出力: records/B/analysis-<日付>.{md,json}（既存は --force なしでは上書きしない）。
用法: python tools/analyze_B.py --gate records/B/gate-B-<日付>.json [--seal records/B/seal-B.json] [--root <results>] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import fisher_exact, binom
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--gate', default=None, help='tools/gate_B.py の json（選定の記録）')
ap.add_argument('--no-gate', action='store_true', help='検査用の口（選定の記録を読まない）')
ap.add_argument('--seal', default=None, help='封印の記録（予想符号）')
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
CEN, DG, RG, SG, QF, GO = T['censor'], T['dilution_gate'], T['refuse_gate'], T['style_gate'], T['quality_floor'], T['gate_order']
PS, SC = T['print_strings'], T['scenarios']
rate, pt = runs_B.rate, runs_B.pt
if not (a.gate or a.no_gate):
    sys.exit('--gate（tools/gate_B.py の出力）が要る（--no-gate は検査用）')
G = runs_B.read_json(a.gate) if a.gate else None
if G and G.get('kind') != 'gate_B':
    sys.exit('門の記録の種類が違う: %s' % a.gate)
SEAL = runs_B.read_json(a.seal) if a.seal else None

C, idx = runs_B.counts_main(T, root=a.root, allow_dry=a.allow_dry)
STR = runs_B.counts_main_strata(T, root=a.root, allow_dry=a.allow_dry)
CQ, idx_q = runs_B.counts_quality(T, root=a.root, allow_dry=a.allow_dry)
DRY = sorted({m for recs in list(idx.values()) + list(idx_q.values()) for r in recs for m in r['dry_marks']})

# ---- 選定後の品質床（裁定 D77）: 落ちた腕 ----
QF_FAIL, QF_ROWS = set(), []
for (stage, arm, l, c), cell in sorted(CQ.items()):
    if stage != 'post':
        continue
    base = arm.split('+v')[0].split('-v')[0]
    noop = CQ.get(('post', base, None, None))      # 相手は**段ごと**に走らせる（裁定 D88・選定の段のものを使い回さない）
    if noop is None:
        QF_ROWS.append({'arm': arm, 'missing_partner': True,
                        'note': '選定後の段の無操作の相手が無い（裁定 D88・段ごとに走らせる）'})
        continue
    d_pt = 100.0 * (cell['correct'] - noop['correct']) / QF['denominator']
    ok = d_pt > QF['threshold_pt']
    QF_ROWS.append({'arm': arm, 'layer': l, 'coef': c, 'correct': cell['correct'], 'noop_correct': noop['correct'],
                    'diff_pt': round(d_pt, 3), 'pass': ok, 'boundary': abs(d_pt - QF['threshold_pt']) < 1e-9})
    if not ok:
        QF_FAIL.add(arm)


def cell(sc, arm):
    return C.get((sc, arm))


def wald_ci(k1, n1, k2, n2, z=1.96):
    """pt 差（A − B）の 95% Wald 区間。"""
    if not (n1 and n2):
        return None
    p1, p2 = k1 / n1, k2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = 100.0 * (p1 - p2)
    return (round(d, 3), round(d - 100.0 * z * se, 3), round(d + 100.0 * z * se, 3))


def fisher(k1, n1, k2, n2):
    return float(fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1])


def stat(c, key='cat'):
    return (c[key], c['n_ok']) if c else (None, None)


# ---- 確証の族 ----
def analyse_contrast(fam, c, alpha_step):
    A, B = cell(c['scenario'], c['A']), cell(c['scenario'], c['B'])
    row = {'id': c['id'], 'family': fam, 'scenario': c['scenario'], 'A': c['A'], 'B': c['B'], 'gates': [], 'notes': []}
    if A is None or B is None:
        row.update({'label': '表に載らない（記録が無い）', 'missing': True})
        return row
    ka, na, kb, nb = A['cat'], A['n_ok'], B['cat'], B['n_ok']
    p = fisher(ka, na, kb, nb) if (na and nb) else None
    ci = wald_ci(ka, na, kb, nb)
    ra, rb = rate(ka, na), rate(kb, nb)
    row.update({'k_A': ka, 'n_ok_A': na, 'k_B': kb, 'n_ok_B': nb, 'rate_A': ra, 'rate_B': rb,
                'p': p, 'diff_pt': None if ci is None else ci[0], 'ci': None if ci is None else [ci[1], ci[2]],
                'sign': None if ci is None else ('上' if ci[0] > 0 else ('下' if ci[0] < 0 else '零')),
                'ff_pt_A': pt(rate(A['ff'], na)), 'ff_pt_B': pt(rate(B['ff'], nb)),
                'refuse_pt_A': pt(rate(A['refuse'], na)), 'refuse_pt_B': pt(rate(B['refuse'], nb)),
                'style_a_pt_A': pt(rate(A['style_a'], na)), 'style_a_pt_B': pt(rate(B['style_a'], nb)),
                'style_b_pt_A': pt(rate(A['style_b'], na)), 'style_b_pt_B': pt(rate(B['style_b'], nb))})
    # --- 門を順に見る（札は最初の一つ・ほかは注） ---
    both_low = ra is not None and rb is not None and ra < CEN['low'] and rb < CEN['low']
    both_high = ra is not None and rb is not None and ra > CEN['high'] and rb > CEN['high']
    if both_low or both_high:
        row['gates'].append('判定不能（検閲）')
    ffd = None if None in (row['ff_pt_A'], row['ff_pt_B']) else abs(row['ff_pt_A'] - row['ff_pt_B'])
    rfd = None if None in (row['refuse_pt_A'], row['refuse_pt_B']) else abs(row['refuse_pt_A'] - row['refuse_pt_B'])
    row['ff_diff_pt'] = None if ffd is None else round(ffd, 3)
    row['refuse_diff_pt'] = None if rfd is None else round(rfd, 3)
    if ffd is not None and ffd > DG['threshold_pt']:
        row['gates'].append('判定保留（書式外転位）')
    if rfd is not None and rfd > DG['threshold_pt']:
        row['gates'].append('判定保留（refuse 転位・差）')
    nominal = p is not None and p < 0.05
    if nominal:
        aa, ab = na - A['refuse'], nb - B['refuse']
        if min(aa, ab) < RG['answered_min_n_ok']:
            row['gates'].append('判定保留（refuse 転位）')
            row['notes'].append('答えた分母が %s 未満' % RG['answered_min_n_ok'])
        else:
            pa2 = fisher(ka, aa, kb, ab)
            d2 = (ka / aa) - (kb / ab)
            same = (d2 > 0) == (row['diff_pt'] > 0) if row['diff_pt'] not in (None, 0) else False
            row['answered'] = {'p': pa2, 'diff_pt': round(100.0 * d2, 3), 'n_A': aa, 'n_B': ab}
            if (not same) or pa2 >= 0.05:
                row['gates'].append('判定保留（refuse 転位）')
    sa = None if None in (row['style_a_pt_A'], row['style_a_pt_B']) else abs(row['style_a_pt_A'] - row['style_a_pt_B'])
    sb = None if None in (row['style_b_pt_A'], row['style_b_pt_B']) else abs(row['style_b_pt_A'] - row['style_b_pt_B'])
    row['style_diff_pt'] = None if None in (sa, sb) else round(max(sa, sb), 3)
    # 様式門は**確証の札にのみ作用する**（style_gate.asymmetry）。Holm の判定が出た後に当てるので、ここでは印だけ置く。
    if c['A'] in QF_FAIL or c['B'] in QF_FAIL:
        row['gates'].append('判定不能（品質床）')
    # --- 札（gate_order の順で最初の一つ） ---
    order = ['判定不能（検閲）', '判定保留（書式外転位）', '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定不能（品質床）']
    fired = [g for g in order if g in row['gates']]
    row['label'] = fired[0] if fired else ('確証' if (p is not None and p < alpha_step) else '非有意')
    row['fired'] = fired
    return row


def apply_style_gate(row):
    """様式門は確証の札にのみ作用する（style_gate.asymmetry）。Holm の判定が出た後に当てる。"""
    d = row.get('style_diff_pt')
    if d is None:
        return
    if d > SG['hold_pt']:
        row['label'] = '判定保留（様式転位）'
        row['fired'] = row.get('fired', []) + ['判定保留（様式転位）']
    elif d > SG['note_pt']:
        row['notes'].append('注（様式・差 %.1f pt）' % d)


RES, FAMROWS = {}, []
for famkey, F in T['families'].items():
    rows = [analyse_contrast(famkey, c, 0.05) for c in F['contrasts']]
    # Holm（族ごと・m は減らさない・降格した対比も順位に含める）
    ordered = sorted([r for r in rows if r.get('p') is not None], key=lambda r: r['p'])
    m = F['m']
    passed = True
    for i, r in enumerate(ordered):
        step = 0.05 / (m - i)
        r['holm_alpha'] = step
        r['holm_pass'] = passed and (r['p'] < step)
        passed = r['holm_pass']
    for r in rows:
        if r.get('label') == '確証' and not r.get('holm_pass'):
            r['label'] = '非有意'
        if r.get('label') == '確証':
            apply_style_gate(r)
        if len(r.get('fired') or []) > 1:
            r['notes'].append('ほかに当たった門: ' + '・'.join(r['fired'][1:]))
        if r.get('label') == '確証' and SEAL:
            want = (SEAL.get('signs') or {}).get(r['id'])
            r['sealed_sign'] = want
            if want and want != r['sign']:
                r['label'] = '確証（登録された向きと逆）'
                r['notes'].append(PS['label_reverse'].format(A=r['A'], B=r['B'], sign=r['sign'], diff=r['diff_pt'], ci=r['ci']))
    RES[famkey] = rows
    FAMROWS += rows

counts = {k: 0 for k in ('確証', '判定不能（検閲）', '判定不能（品質床）', '判定保留（書式外転位）', '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '非有意')}
for r in FAMROWS:
    lab = r.get('label', '')
    key = '確証' if lab.startswith('確証') else lab
    if key in counts:
        counts[key] += 1
agree = sum(1 for r in FAMROWS if r.get('label', '').startswith('確証') and r.get('sealed_sign') and r['sealed_sign'] == r['sign'])
n_conf = sum(1 for r in FAMROWS if r.get('label', '').startswith('確証'))

# ---- 記述の族（p を印字しない） ----
DESC = {}
for famkey, F in T['descriptive_families'].items():
    rows = []
    for c in F.get('contrasts', []):
        A, B = cell(c['scenario'], c['A']), cell(c['scenario'], c['B'])
        if A is None or B is None:
            rows.append({'id': c['id'], 'missing': True})
            continue
        ci = wald_ci(A['cat'], A['n_ok'], B['cat'], B['n_ok'])
        rows.append({'id': c['id'], 'scenario': c['scenario'], 'A': c['A'], 'B': c['B'],
                     'rate_A': rate(A['cat'], A['n_ok']), 'rate_B': rate(B['cat'], B['n_ok']),
                     'diff_pt': None if ci is None else ci[0], 'ci': None if ci is None else [ci[1], ci[2]],
                     'ff_pt_A': pt(rate(A['ff'], A['n_ok'])), 'ff_pt_B': pt(rate(B['ff'], B['n_ok'])),
                     'refuse_pt_A': pt(rate(A['refuse'], A['n_ok'])), 'refuse_pt_B': pt(rate(B['refuse'], B['n_ok']))})
    DESC[famkey] = rows


def ci_excl_zero_power(p_a, p_b, n, z=1.96):
    k = np.arange(n + 1)
    pa, pb = binom.pmf(k, n, p_a), binom.pmf(k, n, p_b)
    r = k / n
    diff = r[:, None] - r[None, :]
    se = np.sqrt(r[:, None] * (1 - r[:, None]) / n + r[None, :] * (1 - r[None, :]) / n)
    se = np.where(se == 0, np.inf, se)
    w = pa[:, None] * pb[None, :]
    return float(w[(diff + z * se) < 0].sum())


# ---- S4 の反証（三分岐・裁定 D81） ----
S4 = T['descriptive_families']['B_desc_S4']
s4c = S4['contrasts'][0]
s4A, s4B = cell(s4c['scenario'], s4c['A']), cell(s4c['scenario'], s4c['B'])
s4 = {'id': s4c['id']}
if s4A and s4B and s4A['n_ok'] and s4B['n_ok']:
    ci = wald_ci(s4A['cat'], s4A['n_ok'], s4B['cat'], s4B['n_ok'])
    base_r = rate(s4B['cat'], s4B['n_ok'])
    eff, pmin = S4['three_way']['effect_pt'], S4['three_way']['power_min']
    power = ci_excl_zero_power(max(base_r - eff / 100.0, 0.001), base_r, s4B['n_ok'])
    if ci[2] < 0:
        verdict = '下がった（封印は外れ）'
    elif ci[1] > 0:
        verdict = '上がった（封印は当たり）'
    elif power >= pmin:
        verdict = '下がらなかった（封印は当たり）'
    else:
        verdict = '当否を言わない'
    s4.update({'diff_pt': ci[0], 'ci': [ci[1], ci[2]], 'partner_rate': base_r, 'power_at_effect': round(power, 4),
               'effect_pt': eff, 'power_min': pmin, 'verdict': verdict,
               'sealed_prediction': (SEAL or {}).get('s4') or S4['sealed_prediction']})
else:
    s4['verdict'] = '表に載らない（記録が無い）'

# ---- 様式門の層別の副次（札を変えない） ----
STRAT = []
for r in FAMROWS:
    if r.get('label') not in ('判定保留（様式転位）',) and '注（様式' not in '・'.join(r.get('notes', [])):
        continue
    for s in SG['stratified']['strata']:
        A, B = STR.get((r['scenario'], r['A'], s)), STR.get((r['scenario'], r['B'], s))
        if not (A and B) or min(A['n_ok'], B['n_ok']) < RG['answered_min_n_ok']:
            STRAT.append({'id': r['id'], 'stratum': s, 'skipped': '層の分母が %s 未満' % RG['answered_min_n_ok']})
            continue
        STRAT.append({'id': r['id'], 'stratum': s, 'p': fisher(A['cat'], A['n_ok'], B['cat'], B['n_ok']),
                      'diff_pt': wald_ci(A['cat'], A['n_ok'], B['cat'], B['n_ok'])[0], 'n_A': A['n_ok'], 'n_B': B['n_ok']})

# ---- 対比に現れない腕（report_rules.orphan_arms） ----
used = {(c['scenario'], c[k]) for F in list(T['families'].values()) + list(T['descriptive_families'].values())
        for c in F.get('contrasts', []) for k in ('A', 'B')}
orphans = sorted({(sc, arm) for (sc, arm) in C if (sc, arm) not in used})
missing = sorted({(c['scenario'], c[k]) for F in list(T['families'].values()) + list(T['descriptive_families'].values())
                  for c in F.get('contrasts', []) for k in ('A', 'B') if (c['scenario'], c[k]) not in C})

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'analysis-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

first = PS['first_finding'].format(confirmed=counts['確証'], undecidable=counts['判定不能（検閲）'], qfloor=counts['判定不能（品質床）'],
                                   ff=counts['判定保留（書式外転位）'], refuse=counts['判定保留（refuse 転位）'] + counts['判定保留（refuse 転位・差）'],
                                   style=counts['判定保留（様式転位）'], ns=counts['非有意'])
REC = {'kind': 'analyze_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
       'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'gate': (G or {}).get('verdict'),
       'selection': (G or {}).get('selection', {}).get('pick'), 'counts': counts, 'confirm': FAMROWS, 'descriptive': DESC,
       's4': s4, 'stratified': STRAT, 'quality_post': QF_ROWS, 'orphan_arms': orphans, 'missing_cells': missing,
       'sign_agreement': {'agree': agree, 'confirmed': n_conf, 'sealed': bool(SEAL)}, 'dry_marks': DRY}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

L = ['# 段階 B 本走行の集計（機械生成・`tools/analyze_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 正本 SHA16 %s。選定: %s。門の判定: %s。' % (REC['contrasts_sha16'], REC['selection'], REC['gate']), '',
     '- **%s**' % first]
if SEAL:
    L.append('- ' + PS['sign_agreement'].format(agree=agree, confirmed=n_conf))
else:
    L.append('- 封印の記録が渡されていないので、予想符号との照合は行っていない（裁定 D79・凍結時に封印する）。')
L += ['- ' + PS['scope'], '- ' + PS['style_move'], '- ' + PS['no_p_desc'], '- ' + PS['selection_direction'],
      '- ' + T['style_gate']['asymmetry'], '- ' + T['fwer_note'], '']
if DRY:
    L += ['- **dry-run の走行を読んだ（検査用）**: %s' % '・'.join(DRY), '']
L += ['## 確証の族（三つ組で読む・率の単独引用を禁じる）', '',
      '| 対比 | 場面 | 破局 A/n | 破局 B/n | pt 差 | 区間 | p | Holm | 書式外の差 | refuse の差 | 様式の差 | 札 | 注 |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in FAMROWS:
    if r.get('missing'):
        L.append('| %s | %s | — | — | — | — | — | — | — | — | — | %s | |' % (r['id'], r['scenario'], r['label']))
        continue
    L.append('| %s | %s | %d/%d | %d/%d | %s | %s | %s | %s | %s | %s | %s | %s | %s |'
             % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'], r['diff_pt'], r['ci'],
                None if r['p'] is None else round(r['p'], 5), r.get('holm_alpha') and round(r['holm_alpha'], 5),
                r.get('ff_diff_pt'), r.get('refuse_diff_pt'), r.get('style_diff_pt'), r['label'], '・'.join(r.get('notes', []))))
L += ['', '## 記述の族（p を印字しない）', '']
for famkey, rows in DESC.items():
    if not rows:
        continue
    L += ['### %s' % famkey, '', '| 対比 | 破局率 A | 破局率 B | pt 差 | 区間 | 書式外 A/B | refuse A/B |', '|---|---|---|---|---|---|---|']
    for r in rows:
        if r.get('missing'):
            L.append('| %s | — | — | — | — | — | — |' % r['id'])
            continue
        L.append('| %s | %s | %s | %s | %s | %s／%s | %s／%s |'
                 % (r['id'], None if r['rate_A'] is None else round(r['rate_A'], 4), None if r['rate_B'] is None else round(r['rate_B'], 4),
                    r['diff_pt'], r['ci'], r['ff_pt_A'], r['ff_pt_B'], r['refuse_pt_A'], r['refuse_pt_B']))
    L.append('')
L += ['## S4 の反証（三分岐・裁定 D81）', '', '- 判定: **%s**' % s4.get('verdict')]
if 'power_at_effect' in s4:
    L.append('- pt 差 %s・区間 %s・相手の腕の率 %.4f・%d pt の検出力 %.3f（線は %g）' % (s4['diff_pt'], s4['ci'], s4['partner_rate'], s4['effect_pt'], s4['power_at_effect'], s4['power_min']))
L += ['', '## 選定後の品質床（裁定 D77）', '']
L += (['- 落ちた腕: %s' % ('・'.join(sorted(QF_FAIL)) if QF_FAIL else 'なし')] if QF_ROWS else ['- 記録が無い（走行の前）'])
if QF_FAIL:
    L.append('- ' + PS['quality_fail'].format(arms='・'.join(sorted(QF_FAIL))))
L += ['', '## 表に載らない対比・対比に現れない腕（`report_rules`）', '',
      '- 記録の無いセル: %s' % ('・'.join('%s×%s' % x for x in missing) if missing else 'なし'),
      '- 対比に現れない腕（参照のための無操作）: %s' % ('・'.join('%s×%s' % x for x in orphans) if orphans else 'なし'), '']
if STRAT:
    L += ['## 様式門の層別の副次（札を変えない）', '', '| 対比 | 層 | p | pt 差 | n A/B |', '|---|---|---|---|---|']
    for s in STRAT:
        L.append('| %s | %s | %s | %s | %s |' % (s['id'], s['stratum'], s.get('p') and round(s['p'], 5), s.get('diff_pt'), s.get('skipped') or '%s/%s' % (s.get('n_A'), s.get('n_B'))))
    L.append('')
L += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[analyze_B] %s / %s' % (out_md, out_json))
print('  ' + first)
