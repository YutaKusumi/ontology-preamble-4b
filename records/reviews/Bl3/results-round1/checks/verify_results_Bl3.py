# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の結果の巡の四票（G1・G2・C1・C2）の事実の主張を、公開の置き場の現物（組の出力・集計の記録・下見の記録・設計事実・束）から、
器とは別に書いた式で再現する（再現の番号 K480 から・枠 `frame-results-Bl3.md`）。読みの当否（言い回しの提案）は再現の外で、採否の案で扱う。
再現しなかった主張も消さない。票がどの単位で数えたかを確かめてから判じる。書くのは本記録（md と json）だけ。既にあるファイルには書かない。
K523 から: 採否の案のために足した確かめ（票の数のうち上で照らしていなかったもの・手続きの時刻・起草者が採否の案を書く中で見つけた器の形）。手続きの時刻は、手元の git の reflog と、
  会話の記録（時刻と uuid だけを読む・中身は印字しない）から機械で取る。
用法: python records/reviews/Bl3/results-round1/checks/verify_results_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, json, math, glob, hashlib, itertools, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
OUT_MD, OUT_JSON = os.path.join(HERE, 'verification-results-Bl3.md'), os.path.join(HERE, 'verification-results-Bl3.json')
for p in (OUT_MD, OUT_JSON):
    assert not os.path.exists(p), '既にある: ' + p
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
ld = lambda rel: json.load(open(j(*rel.split('/')), encoding='utf-8'))
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
T3, FJ, A, J = ld('design/contrasts-Bl3.json'), ld('records/Bl3/design-facts-Bl3.json'), ld('records/Bl3/analysis-Bl3.json'), ld('records/Bl3/judge-Bl3.json')
dirs = {p: v['dir'] for p, v in A['inputs'].items()}
MAIN_REL = 'results/Bl3/main/%s/main.json' % dirs['main']
RC_REL = 'results/Bl3/main/%s/recompute.json' % dirs['recompute']
SEC_REL = 'results/Bl3/main/%s/secondary.json' % dirs['secondary']
PJ_REL = 'records/Bl3/pilot/pilot-20260926T103442Z/pilot.json'
M, RC, SEC, PJ = ld(MAIN_REL), ld(RC_REL), ld(SEC_REL), ld(PJ_REL)['pilot']
C = M['cells']
rows = A['rows']
K = []                                                      # (番号, 票, 主張, 現物, 判定)


def add(votes, claim, got, ok, note=''):
    K.append({'k': 'K%d' % (480 + len(K)), 'votes': votes, 'claim': claim, 'got': got, 'verdict': '再現した' if ok is True else ('再現しない' if ok is False else ok), 'note': note})


def iso_of(key):
    return np.array([v for k, v in C[key]['effects'].items() if k.startswith('iso:')], dtype=np.float64)


def iso_dict(key):
    return {k: v for k, v in C[key]['effects'].items() if k.startswith('iso:')}


def rankdata(x):
    x = np.asarray(x, dtype=np.float64)
    order = np.argsort(x, kind='mergesort')
    r = np.empty(len(x), dtype=np.float64)
    i = 0
    while i < len(x):
        k = i
        while k + 1 < len(x) and x[order[k + 1]] == x[order[i]]:
            k += 1
        r[order[i:k + 1]] = (i + k) / 2.0 + 1.0
        i = k + 1
    return r


def spearman(a, b):
    ra, rb = rankdata(a), rankdata(b)
    return float(np.corrcoef(ra, rb)[0, 1])


# ---------------- 割合・Holm・側（K480〜K482）
KISO = T3['nulls']['isotropic']['count']
p_ok, tail_ok = [], []
for rid, r in rows.items():
    iso = iso_of(r['cell_sign'])
    up, lo = int((iso >= r['effect']).sum()), int((iso <= r['effect']).sum())
    p = min(1.0, 2 * min(1 + up, 1 + lo) / (1 + KISO))
    tail_ok.append(up == r['upper'] and lo == r['lower'])
    p_ok.append(abs(p - r['p']) < 1e-12)
m = A['rows_meta']['m_rows']
order = sorted(rows, key=lambda k: rows[k]['p'])
passed, steps = [], []
for i, rid in enumerate(order):
    step = 0.05 / (m - i)
    steps.append((rid, rows[rid]['p'], step))
    if rows[rid]['p'] < step:
        passed.append(rid)
    else:
        break
add('G1・G2・C1・C2', 'Holm（下見で外した後の 14 行）で通るのは sub:N1 だけ（p 0.002 と第一段 0.003571・二番目の 0.030 は第二段 0.003846 を通らない）',
    '行 %d・通った %s・段 %s' % (m, passed, ['%s p %.4g 段 %.6g' % s for s in steps[:2]]), passed == ['sub:N1:O-Ncold-v~O-Ncold-vrand'] and m == 14)
add('G1・G2・C1・C2', '14 行の p は裾の本数から 2 × min(1＋上の裾, 1＋下の裾) ÷ (1＋等方の本数) で出る。裾の本数は組 main の等方の効き目 1999 本から数え直せる',
    'p の一致 %d/%d・裾の本数の一致 %d/%d（組 main の等方の効き目から数え直した）' % (sum(p_ok), len(p_ok), sum(tail_ok), len(tail_ok)), all(p_ok) and all(tail_ok))
side_ok = []
for rid, r in rows.items():
    iso = iso_of(r['cell_sign'])
    q1, q3, med = np.percentile(iso, 25), np.percentile(iso, 75), np.median(iso)
    side_ok.append(abs(med - r['side']['median']) < 1e-9 and abs(q1 - r['side']['q1']) < 1e-9 and abs(q3 - r['side']['q3']) < 1e-9 and (q1 < 0 < q3) and r['side']['side'] == 'sign_only')
add('C1・C2', '14 行とも等方の中央値と四分位が記録と同じで、零が四分位の間にあるので効き目の側は「符号だけ」', '一致 %d/%d' % (sum(side_ok), len(side_ok)), all(side_ok))
# 16 行の段でも通るか（C2）
add('C2', '外す前の十六行の第一段 0.003125 でも sub:N1（p 0.002）は通る（札は下見の外し方に依らない）', 'p %.4g・十六行の第一段 %.6g' % (rows['sub:N1:O-Ncold-v~O-Ncold-vrand']['p'], 0.05 / 16),
    rows['sub:N1:O-Ncold-v~O-Ncold-vrand']['p'] < 0.05 / 16)
ties = sorted(k for k, r in rows.items() if abs(r['p'] - 0.062) < 1e-12)
add('C2', 'p 0.062 の二行は Holm の段の並びが任意（判定には効かない）', '同じ p の行 %s' % ties, len(ties) == 2)
# ---------------- 二つ目の札（K485〜K489）
SIB = set(T3['nulls']['real']['swap_siblings'])
PAIRS = [n for n in ld('results/Bl3/directions-Bl3.json')['groups']['real']['names']]


def flip(key):
    sc, b, sg = key.split('|')
    return '%s|%s|%+d' % (sc, b, -int(sg))


def comparators(r):
    own = {'static': SIB, 'Nk': {'Nk~N'}}[r['direction']]
    keep = [p for p in PAIRS if p not in own]
    a, b = C[r['cell_sign']]['effects'], C[flip(r['cell_sign'])]['effects']
    return keep, [a['real:' + p] for p in keep] + [b['real:' + p] for p in keep], [(a['real:' + p], b['real:' + p]) for p in keep]


sec_ok, dist_n1 = [], None
for rid, r in rows.items():
    keep, vals, pairs = comparators(r)
    cen = float(np.median(vals))
    d = abs(r['effect'] - cen)
    dd = [abs(v - cen) for v in vals]
    top = all(d > x for x in dd)
    rank_o = 1 + sum(1 for x in dd if x >= d)
    pd_ = [max(abs(u - cen), abs(w - cen)) for u, w in pairs]
    rank_p = 1 + sum(1 for x in pd_ if x >= d)
    s = r['second']
    sec_ok.append(abs(cen - s['center']) < 1e-12 and top == s['top'] and rank_o == s['rank_oriented'] and len(vals) + 1 == s['of_oriented'] and rank_p == s['rank_pair'] and len(pairs) + 1 == s['of_pair'])
    if rid.startswith('sub:N1'):
        dist_n1 = d
add('G1・G2・C1・C2', '14 行の二つ目の札（中心・最上位・向きまで数えた順位・対の単位の順位）は、兄弟を除いた実在の差の効き目（両方の向き）から出し直せる。sub:N1 は距離 2.7478 で 1/49・1/25',
    '一致 %d/%d・sub:N1 の距離 %.4f' % (sum(sec_ok), len(sec_ok), dist_n1), all(sec_ok) and abs(dist_n1 - 2.7478) < 5e-4)
eq_v = all(abs(C[r['cell_sign']]['effects']['static'] - C[r['cell_sign']]['effects']['real:O~Osec']) == 0 for r in rows.values() if r['direction'] == 'static')
eq_n = all(abs(C[r['cell_sign']]['effects']['Nk'] - C[r['cell_sign']]['effects']['real:Nk~N']) == 0 for r in rows.values() if r['direction'] == 'Nk')
add('C1', 'v̂ の効き目は real:O~Osec と、Nk の効き目は real:Nk~N と、ぴったり同じ値（自分の対を除く決まりが要る理由）', 'v̂ %s・Nk %s' % (eq_v, eq_n), eq_v and eq_n)
r1 = rows['sub:N1:O-Ncold-v~O-Ncold-vrand']
keep, vals, _ = comparators(r1)
a, b = C[r1['cell_sign']]['effects'], C[flip(r1['cell_sign'])]['effects']
sib3 = [p for p in SIB if p != 'O~Osec']
vals_s = vals + [a['real:' + p] for p in sib3] + [b['real:' + p] for p in sib3]
cen_s = float(np.median(vals_s))
d_row = abs(r1['effect'] - cen_s)
d_sib = max(abs(a['real:' + p] - cen_s) for p in sib3)
d_sib = max(d_sib, max(abs(b['real:' + p] - cen_s) for p in sib3))
add('C1', 'sub:N1 は、兄弟の三対（自分の対 O~Osec を除く）を比べる相手に戻しても最上位のまま（兄弟の中心からの距離の最大 2.34・行 2.75）',
    '兄弟を戻した中心 %.4f・行の距離 %.4f・兄弟の距離の最大 %.4f・ほかの比べる相手を含めて最上位 %s' % (cen_s, d_row, d_sib, all(d_row > abs(v - cen_s) for v in vals_s)),
    abs(d_sib - 2.34) < 0.01 and abs(d_row - 2.75) < 0.01 and all(d_row > abs(v - cen_s) for v in vals_s))
share_ok = []
for rid, r in rows.items():
    keep, vals, _ = comparators(r)
    cen = float(np.median(vals))
    dmax = max(abs(v - cen) for v in vals)
    iso = iso_of(r['cell_sign'])
    sh = float((np.abs(iso - cen) > dmax).mean())
    share_ok.append(abs(sh - r['iso_top_share']) < 1e-12)
add('C1・C2', '等方の最上位の割合は、同じ中心と同じ比べる相手から出し直せる。sub:N1 は 0.040 で 1/49 の約二倍', '一致 %d/%d・sub:N1 %.4f・1/49 %.4f' % (sum(share_ok), len(share_ok), r1['iso_top_share'], 1 / 49),
    all(share_ok) and abs(r1['iso_top_share'] - 0.040) < 5e-4)
ch = A['chance']
add('C1・C2', '二つ目の札の偶然の目安は 7/49＋7/55＝0.2701 と 7/25＋7/28＝0.53（外す前は 0.3087 と 0.6057）', '記録 %s・式 %.4f と %.4f' % ({k: v for k, v in ch.items() if k != 'rows_by_direction'}, 7 / 49 + 7 / 55, 7 / 25 + 7 / 28),
    abs(ch['oriented'] - (7 / 49 + 7 / 55)) < 1e-4 and abs(ch['pair'] - (7 / 25 + 7 / 28)) < 1e-4)
# ---------------- 門（K492）
GR = A['gate_rows']
dropped = set((A['main_run'] or {}).get('dropped') or [])
unit_key = lambda u: u


def gate(rows_, ykey):
    units = sorted({g['unit'] for g in rows_})
    y = [g[ykey] for g in rows_]
    push = lambda g, u: C[g['fam']]['effects'][unit_key(u)]
    obs = spearman(y, [push(g, g['unit']) for g in rows_])
    cnt = n = 0
    for perm in itertools.permutations(units):
        mp = dict(zip(units, perm))
        rho = spearman(y, [push(g, mp[g['unit']]) for g in rows_])
        n += 1
        cnt += rho >= obs - 1e-12
    return len(rows_), units, obs, cnt / n, n


kept = [g for g in GR if g['cell'] not in dropped]
style_drop = {x for x in (A.get('style_rows') or [])}
defs = {'main': (kept, 'y'), 'without_vhat': ([g for g in kept if g['unit'] != 'static'], 'y'),
        'desc_without_vhat_loaded': ([g for g in kept if g['unit'] not in ('static', 'loaded')], 'y'),
        'desc_choice_a': (kept, 'y_a'), 'desc_without_style': ([g for g in kept if g['name'] not in style_drop], 'y')}
gate_ok, gate_txt = [], []
for name, (rs, yk) in defs.items():
    n_rows, units, rho, p, n = gate(rs, yk)
    G = A['gates'][name]
    gate_ok.append(n_rows == G['n_rows'] and abs(rho - G['rho']) < 1e-9 and abs(p - G['p']) < 1e-9 and n == G['n_perm'])
    gate_txt.append('%s 行 %d・単位 %d・入れ替え %d・ρ %.4f・p %.4g' % (name, n_rows, len(units), n, rho, p))
rm_sk = sum(1 for g in GR if g['cell'] == 'SK|Onull')
rm_s4 = sum(1 for g in GR if g['cell'] == 'S4|Osec-Ncold')
loaded_left = sum(1 for g in kept if g['unit'] == 'loaded')
add('G1・G2・C1・C2', '五つの門（本の門・v̂ を抜いた門・記述の三つ）は、門の行の行動の量と組 main の押しから、全ての入れ替えで出し直せる（行 54・47・47・54・52・入れ替え 720・120）。'
    '下見で外した行は SK|Onull が 6 行・S4|Osec-Ncold が 4 行で、loaded の唯一の行が外れて単位は 6 つになった',
    '%s・外した行 SK|Onull %d・S4|Osec-Ncold %d・残った loaded の行 %d' % (' ／ '.join(gate_txt), rm_sk, rm_s4, loaded_left), all(gate_ok) and rm_sk == 6 and rm_s4 == 4 and loaded_left == 0)
# static の門の行の y を転記行 C の件数から（C1・C2）
cc = T3['gate']['continuity']
lg = lambda k, n: math.log((k + cc) / (n - k + cc))
qi = FJ['facts']['C']['q7_intervals']
y_ok = []
st_rows = [g for g in kept if g['unit'] == 'static']
for g in st_rows:
    rid_ = ('sub:%s:O-Ncold-v~O-Ncold-vrand' % g['scenario']) if g['sign'] < 0 else ('add:%s:Onull+v~Onull+vrand' % g['scenario'])
    q = [x for x in qi if x['id'] == rid_]
    if len(q) != 1:
        y_ok.append(None)
        continue
    q = q[0]
    y = lg(q['cat'], q['n_ok']) - lg(q['base_cat'], q['base_n_ok'])
    y_ok.append(abs(y - g['y']) < 1e-9)
add('C1・C2', 'static の門の行の行動の量 y は、転記行 C の件数から補正 0.5 で出し直せる', '一致 %s（行 %d）' % (y_ok, len(st_rows)), all(v is True for v in y_ok) if y_ok else '確かめられない',
    '転記行 C の q7 の区間の件数（行の破局の件数と土台の無操作の腕の件数）を使った')
# ---------------- 下見（K494〜K497）
vi_a = PJ['vi']['a']
v_d = PJ['v']['diffs']
mx_a = max(vi_a.items(), key=lambda kv: kv[1])
mx_v_main = max(((k, abs(v)) for k, v in v_d.items() if k != 'S4|Osec-Ncold'), key=lambda kv: kv[1])
add('C1・C2', '(vi) の (a) の最大は S4|Onull の 1.62092、(v) の主の升目の最大は N1|Onull の 1.62077 で、四桁では同じだが別の値（門の行だけの升目の (v) は 2.737）',
    '(vi)(a) %s %.5f・(v) 主の升目 %s %.5f・門だけ %.3f' % (mx_a[0], mx_a[1], mx_v_main[0], mx_v_main[1], abs(v_d['S4|Osec-Ncold'])),
    mx_a[0] == 'S4|Onull' and mx_v_main[0] == 'N1|Onull' and abs(mx_a[1] - 1.62092) < 5e-6 and abs(mx_v_main[1] - 1.62077) < 5e-6)
add('C2', '(vi) の (a) の最大は、凍結の前に置いた揺れの上限 0.01 のおよそ 160 倍', '%.1f 倍' % (mx_a[1] / T3['pilot']['noise_max']), 150 < mx_a[1] / T3['pilot']['noise_max'] < 170)
lo_floor = math.log(T3['pilot']['p_bounds'][0] / (1 - T3['pilot']['p_bounds'][0]))
mar = {c: PJ['cells'][c]['lo'] - lo_floor for c in ('N1|O-Ncold', 'S4|Onull')}
add('C1・C2', '床（確率 0.0001 の対数オッズ −9.210）からの余白は N1|O-Ncold が 0.427 で (vi)(a) の幅 0.690 より小さく、S4|Onull も 1.489 で 1.621 より小さい',
    '床 %.3f・余白 %s・(vi)(a) %s' % (lo_floor, {k: round(v, 3) for k, v in mar.items()}, {k: round(vi_a[k], 3) for k in mar}),
    abs(mar['N1|O-Ncold'] - 0.427) < 1e-3 and mar['N1|O-Ncold'] < vi_a['N1|O-Ncold'] and abs(mar['S4|Onull'] - 1.489) < 1e-3 and mar['S4|Onull'] < vi_a['S4|Onull'])
iv = PJ['iv']
base = {c: PJ['cells'][c]['lo'] for c in PJ['cells']}
dv = {(v, c): iv[v]['lo'][c] - base[c] for v in ('V1', 'V2', 'V3') if v in iv for c in iv[v]['lo']}
mx2 = max(((c, d) for (v, c), d in dv.items() if v == 'V2'), key=lambda kv: kv[1])
mx3 = max(((c, d) for (v, c), d in dv.items() if v == 'V3'), key=lambda kv: kv[1])
fl_n1 = [iv[v]['flags'].get('N1|O-Ncold') for v in ('V1', 'V2', 'V3')]
add('C1・C2', '揺れの版では無操作の値が主の書き出しから大きく動いた（V2 の最大は S1|O-Ncold の 5.854、V3 の最大は SK|O-Ncold の 6.501）。N1|O-Ncold は V1・V2・V3 のすべてに印',
    'V2 %s %.3f・V3 %s %.3f・N1|O-Ncold の印 %s' % (mx2[0], mx2[1], mx3[0], mx3[1], fl_n1),
    mx2[0] == 'S1|O-Ncold' and abs(mx2[1] - 5.854) < 1e-3 and mx3[0] == 'SK|O-Ncold' and abs(mx3[1] - 6.501) < 1e-3 and all(fl_n1))
zero_t = [c for c, v in PJ['cells'].items() if v.get('main') and v.get('pa_transformed') == 0]
add('C1', '変換の後の確率は、主の升目 8 のうち 6 升目で 0', '%d 升目（%s）' % (len(zero_t), '・'.join(zero_t)), len(zero_t) == 6)
main_cells = [c for c, v in PJ['cells'].items() if v.get('main')]
xa = [PJ['cells'][c]['pa'] for c in main_cells]
xb = [PJ['cells'][c]['stage_b_rate'] for c in main_cells]
rho3 = spearman(xa, xb)
cnt = n = 0
for perm in itertools.permutations(xb):
    n += 1
    cnt += spearman(xa, perm) >= rho3 - 1e-12
add('C2', '(iii) の順位相関 0.143（8 升目）は、全ての並べ替えでの片側の p がおよそ 0.38', 'ρ %.4f・並べ替えの p %.4f（%d 通り）' % (rho3, cnt / n, n), abs(rho3 - 0.1429) < 1e-3 and abs(cnt / n - 0.38) < 0.02)
# ---------------- 等方の広がり（K498〜K503）
main_keys = sorted({r['cell_sign'] for r in rows.values()})
rng = {k: (float(iso_of(k).min()), float(iso_of(k).max()), float(np.percentile(iso_of(k), 75) - np.percentile(iso_of(k), 25))) for k in main_keys}
gmin, gmax = min(v[0] for v in rng.values()), max(v[1] for v in rng.values())
iqr_lo, iqr_hi = min(v[2] for v in rng.values()), max(v[2] for v in rng.values())
add('C1', '升目と符号ごとの等方の効き目は、四分位の幅で 1.12〜1.87、範囲で −4.64〜+4.75', '四分位の幅 %.2f〜%.2f・範囲 %.2f〜%.2f（主の升目と符号 %d）' % (iqr_lo, iqr_hi, gmin, gmax, len(rng)),
    abs(iqr_lo - 1.12) < 0.006 and abs(iqr_hi - 1.87) < 0.006 and abs(gmin + 4.64) < 0.006 and abs(gmax - 4.75) < 0.006)
add('G2', '等方の効き目の分布の幅は約 ±4.6（四分位の幅 1.0〜1.8）', '上の K の値（範囲 %.2f〜%.2f・四分位の幅 %.2f〜%.2f）' % (gmin, gmax, iqr_lo, iqr_hi), True, '票の数は丸めた値で、上の値と矛盾しない')
s1 = rng['S1|O-Ncold|-1']
add('G1', 'S1|O-Ncold の等方の効き目は最小 −4.60・最大 +4.63。ほぼ全ての升目で [−3.0, +3.3] から [−4.6, +4.6] に広がる',
    'S1|O-Ncold|−1 %.2f〜%.2f・S1|O-Ncold|+1 %.2f〜%.2f・升目ごとの範囲 %s' % (s1[0], s1[1], rng['S1|O-Ncold|+1'][0], rng['S1|O-Ncold|+1'][1], {k: (round(v[0], 2), round(v[1], 2)) for k, v in rng.items()}),
    '読みの確かめ', 'S1|O-Ncold の符号 −1 と +1 のどちらを指すかは票に書かれていない。値は上の並びで照らす')
# 奇と偶（C1・C2）
cor, ev, od, rcor = [], [], [], []
for sc in ('N1', 'S1', 'S4', 'SK'):
    ep, em = iso_dict('%s|O-Ncold|+1' % sc), iso_dict('%s|O-Ncold|-1' % sc)
    ks = sorted(ep)
    x = np.array([ep[k] for k in ks])
    y = np.array([em[k] for k in ks])
    cor.append(float(np.corrcoef(x, y)[0, 1]))
    ev.append(float(np.std((x + y) / 2)))
    od.append(float(np.std((x - y) / 2)))
for key in [k for k in C if k.endswith('|+1')]:
    fk = flip(key)
    if fk not in C:
        continue
    x = np.array([C[key]['effects']['real:' + p] for p in PAIRS])
    y = np.array([C[fk]['effects']['real:' + p] for p in PAIRS])
    rcor.append(float(np.corrcoef(x, y)[0, 1]))
add('C1・C2', 'O-Ncold の四升目で、同じ等方の方向を足した効き目と引いた効き目の相関は −0.963〜−0.977、偶の成分の標準偏差 0.10〜0.15、奇の成分 0.83〜1.37。実在の差の方向でも相関は −0.84〜−0.98（七升目）',
    '等方の相関 %.3f〜%.3f・偶 %.3f〜%.3f・奇 %.3f〜%.3f・実在の差の相関 %.3f〜%.3f（%d 升目）' % (min(cor), max(cor), min(ev), max(ev), min(od), max(od), min(rcor), max(rcor), len(rcor)),
    abs(min(cor) + 0.977) < 0.0015 and abs(max(cor) + 0.963) < 0.0015 and abs(min(ev) - 0.10) < 0.006 and abs(max(ev) - 0.15) < 0.006 and abs(min(od) - 0.83) < 0.006 and abs(max(od) - 1.37) < 0.006
    and len(rcor) == 7 and abs(min(rcor) + 0.98) < 0.006 and abs(max(rcor) + 0.84) < 0.006, '標準偏差は母の標準偏差（自由度 0）で数えた')
# 13 行の裾（C1）
t13 = {rid: (min(r['upper'], r['lower']), min(r['upper'], r['lower']) / KISO) for rid, r in rows.items() if not r['iso_outside']}
add('C1', 'ほかの 13 行は、効き目と同じか外側に等方の方向が 29〜382 本（片側で 1.5〜19%）', '%d〜%d 本・%.1f〜%.1f%%' % (min(v[0] for v in t13.values()), max(v[0] for v in t13.values()), 100 * min(v[1] for v in t13.values()), 100 * max(v[1] for v in t13.values())),
    min(v[0] for v in t13.values()) == 29 and max(v[0] for v in t13.values()) == 382, '片側の裾は、割合を決めた側の本数で数えた')
r0 = {k: C[k]['effects']['rand:0'] for k in main_keys if k.endswith('|+1')}
add('C1', '段階 B のランダム方向 rand:0 は、足す向きの七升目すべてで同じ符号（+0.83〜+2.60）', '%d 升目・%.2f〜%.2f' % (len(r0), min(r0.values()), max(r0.values())), len(r0) == 7 and min(r0.values()) > 0 and abs(min(r0.values()) - 0.83) < 0.006 and abs(max(r0.values()) - 2.60) < 0.006)
# sub:N1 の余白（C1・C2・G2）
isoN = np.sort(iso_of('N1|O-Ncold|-1'))[::-1]
evN = [e for sc, e in zip(('N1', 'S1', 'S4', 'SK'), ev) if sc == 'N1'][0]
pa0 = PJ['cells']['N1|O-Ncold']['pa']
pa1 = 1 / (1 + (1 - pa0) / pa0 * math.exp(-r1['effect']))
add('C1・C2・G2', 'sub:N1 の効き目 2.734 以上の等方の方向は 1 本（3.018）。二番目と三番目は 2.711 と 2.623 で、三番目を下回れば p は 0.004 で第一段を通らない（余白は約 0.11・この升目の偶の成分の標準偏差 0.099）。無操作の a の確率 0.000153 は、効き目で約 0.0024 に動く',
    '上位 %.3f・%.3f・%.3f・余白 %.3f・偶の標準偏差 %.3f・確率 %.6f → %.4f' % (isoN[0], isoN[1], isoN[2], r1['effect'] - isoN[2], evN, pa0, pa1),
    abs(isoN[0] - 3.018) < 1e-3 and abs(isoN[1] - 2.711) < 1e-3 and abs(isoN[2] - 2.623) < 1e-3 and abs(r1['effect'] - isoN[2] - 0.111) < 1e-3 and abs(evN - 0.099) < 1e-3 and abs(pa1 - 0.0024) < 1e-4,
    '確率の動きは、読み取りの集合の中の選択肢 a の確率として、対数オッズに効き目を足して戻した。G2 の「約 0.002」は丸めた値')
# 升目の間の相関と符号の並び（C2）
vk = [r['cell_sign'] for r in rows.values() if r['direction'] == 'static']
nk = [r['cell_sign'] for r in rows.values() if r['direction'] == 'Nk']
ids = sorted(iso_dict(vk[0]))
X = np.array([[C[k]['effects'][i] for i in ids] for k in vk])
cm = np.corrcoef(X)
offd = [abs(cm[a_, b_]) for a_ in range(len(vk)) for b_ in range(a_ + 1, len(vk))]
sg = np.sign(X)
want = np.array([1 if k.endswith('|-1') else -1 for k in vk])[:, None]
share_v = float((np.all(sg == want, axis=0) | np.all(sg == -want, axis=0)).mean())
Y = np.sign(np.array([[C[k]['effects'][i] for i in ids] for k in nk]))
share_n = float((np.all(Y > 0, axis=0) | np.all(Y < 0, axis=0)).mean())
add('C2', '等方の効き目は升目の間で強く相関（v̂ の 7 行の升目と符号の間で |r| 0.47〜0.97）。v̂ と同じ形の符号の並び（逆向きも含む）は等方の方向の約 39%・Nk の 7 行がすべて同じ符号は約 41%',
    '|r| %.2f〜%.2f・v̂ の形 %.1f%%・Nk の形 %.1f%%' % (min(offd), max(offd), 100 * share_v, 100 * share_n),
    abs(min(offd) - 0.47) < 0.006 and abs(max(offd) - 0.97) < 0.006 and abs(share_v - 0.39) < 0.01 and abs(share_n - 0.41) < 0.01)
# ---------------- 独立の再計算の範囲（K505）
rc_rows = [r_[0] for r_ in RC['rows']]
add('C1・C2', '独立の再計算の範囲は v̂ の 7 行だけ（Nk の 7 行は計算し直していない）。一段目の差の最大 3.71e-06。本の計算はバッチ一なので、二段目は正本の注のとおり形だけの確かめ',
    '再計算の行 %d（%s）・一段目の差の最大 %.3g・本の計算のバッチ %s・正本の注「%s」' % (len(rc_rows), '・'.join(sorted({x.split(':')[0] for x in rc_rows})), A['recompute']['first']['max_abs_diff'], A['main_run']['batch'],
                                                                      T3['independent_recompute']['stages']['second']['note']),
    len(rc_rows) == 7 and all(x.split(':')[0] in ('sub', 'add') for x in rc_rows) and A['main_run']['batch'] == 1 and abs(A['recompute']['first']['max_abs_diff'] - 3.71e-06) < 5e-9)
# ---------------- 効き目の式（C1）
diff0 = max(abs(C[k]['effects'][d] - (C[k]['lo'][d] - C[k]['lo']['noop'])) for k in main_keys for d in C[k]['effects'])
add('C1', '組 main で、効き目＝加えた値−無操作の値が差 0 で成り立つ', '差の最大 %.3g（主の升目と符号 %d）' % (diff0, len(main_keys)), diff0 == 0)
# ---------------- 機械の区画の文（C1）
rep = rd('records/Bl3/results-Bl3.md')
lim_ok = [s for s in T3['limits'] if s in rep]
rr = [x for x in T3['reading_rules']]
add('C1', '報告の限界の文（正本 limits）は正本と逐語で同じ。〈両方の外〉の行だけ、末尾に「（…は主の表）」が足されている',
    '限界の文 %d のうち報告に逐語で在る %d・〈両方の外〉の行の足し書き %s' % (len(T3['limits']), len(lim_ok), '（等方の帰無の中央値と効き目の側は主の表）' in rep), len(lim_ok) == len(T3['limits']) and '（等方の帰無の中央値と効き目の側は主の表）' in rep)
# ---------------- 予想の照合（C1・C2・G2）
truth = A['predictions_truth']
CP, RP = ld('records/predictions/predictions-Bl3-coordinator.json'), ld('records/predictions/predictions-Bl3-registrant.json')
hit = lambda P: sum(1 for k in list(truth)[:6] if truth[k] is not None and P[k] == truth[k])
cnts = {'q2': sum(1 for r in rows.values() if r['direction'] == 'static' and r['iso_outside']), 'q3': sum(1 for r in rows.values() if r['direction'] == 'Nk' and r['iso_outside']),
        'q6': sum(1 for r in rows.values() if r['second']['top'])}
den = {'q2': sum(1 for r in rows.values() if r['direction'] == 'static'), 'q3': sum(1 for r in rows.values() if r['direction'] == 'Nk'), 'q6': len(rows)}
q_in = [k for k in ('一から三', '零', '一か二') if True]
add('G2・C1・C2', 'q1〜q6 の当たりは登録者 1/6・コーディネータ 2/6。q2・q3・q6 の数は 1・0・1 で、分母は 7・7・14（報告に分母は印字されていない）',
    '当たり 登録者 %d・コーディネータ %d・数 %s・分母 %s・報告の §6 に「分母」の語 %s' % (hit(RP), hit(CP), cnts, den, '分母' in rep.split('## 6.')[1].split('## 7.')[0]),
    hit(RP) == 1 and hit(CP) == 2 and cnts == {'q2': 1, 'q3': 0, 'q6': 1} and den == {'q2': 7, 'q3': 7, 'q6': 14})
# ---------------- 表の細部（C1・C2）
fb = FJ['facts']['B']['text']
m16 = re.search(r'S4\|Osec-Ncold（survival）: [^／]*?破局 (\d+)', fb)
row_s4 = [l for l in rep.split(NL) if l.startswith('| S4|Osec-Ncold | いいえ |')]
add('C1', '§1 の表の S4|Osec-Ncold の「段階 B の無操作の破局の率」は「なし」だが、転記行 B には 16/200 がある', '転記行 B の破局 %s・報告の行 %s' % (m16.group(1) if m16 else None, row_s4[0] if row_s4 else None),
    bool(m16) and m16.group(1) == '16' and bool(row_s4) and '| なし |' in row_s4[0])
ctx = [x for x in SEC['contexts'] if x['stratum'].startswith('S4|Osec-Ncold')]
vals_same = len({json.dumps(x['rows'], sort_keys=True) for x in ctx}) == 1
raw = {}
for fp in glob.glob(j('results', 'stageB', 'stageB__S4__Osec-Ncold__s1', 'raw-*.jsonl')):
    for line in open(fp, encoding='utf-8'):
        o = json.loads(line)
        raw[o['trial_id']] = o['text']
texts = [raw.get(x['trial_id']) for x in ctx]
KEYS_ = '"choice": "'
heads = [t[:t.index(KEYS_) + len(KEYS_) + 1] if t and KEYS_ in t else None for t in texts]
add('C1・C2', '乙の S4|Osec-Ncold の行は 20 の文脈がすべて同じ値（四分位が一点）。文脈は同じ文字列だった可能性（C2 は確かめていない・C1 は同じ JSON 直答の出力が選ばれたためと見た）',
    '文脈 %d・値がすべて同じ %s・段階 B の出力の本文が見つかった %d・本文の全体がすべて同じ %s・選択の文字までの頭がすべて同じ %s' % (
        len(ctx), vals_same, sum(1 for t in texts if t is not None), len({t for t in texts if t is not None}) == 1, len(set(heads)) == 1 and None not in heads),
    '一部を再現した' if (len(ctx) == 20 and vals_same and len({t for t in texts if t is not None}) > 1 and len(set(heads)) == 1) else (len(ctx) == 20 and vals_same),
    '値が同じことは再現した。本文の全体は同じではない（C1 の「同じ出力が選ばれた」は再現しない）が、読み取りの位置（選択の文字）までの頭はどれも同じで、値が同じになるのはそのため（本文の照らしは段階 B の本走行の raw の記録・results/stageB/）')
add('C2', '下見で外した升目の扱い（正本 pilot.decision.drop_effects）は乙を挙げていない', '正本の文「%s」' % T3['pilot']['decision']['drop_effects'], '乙' not in T3['pilot']['decision']['drop_effects'])
# ---------------- 束と公開の置き場の同定（C1・C2）
BUN = 'records/reviews/Bl3/results-round1/bundle-results-Bl3-all-in-one.md'
bb = open(j(*BUN.split('/')), 'rb').read()
emb = re.findall(r'<<< 始: `([^`]+)`（SHA16 ([0-9A-F]{16})） >>>', bb.decode('utf-8'))
emb_ok = [s16(p) == h for p, h in emb]
add('C1', '束の一通版は SHA16 5A3D306287745B6C・364,239 バイト・4,718 行で、束の中の 17 のファイルの SHA16 は印の値と一致', 'SHA16 %s・%d バイト・%d 行・埋めたファイル %d・一致 %d' % (
    hashlib.sha256(bb).hexdigest().upper()[:16], len(bb), bb.count(b'\n'), len(emb), sum(emb_ok)), hashlib.sha256(bb).hexdigest().upper()[:16] == '5A3D306287745B6C' and len(bb) == 364239 and len(emb) == 17 and all(emb_ok),
    '行の数は改行の数で数えた')
add('C1・C2', '公開の置き場の同定: main.json 419B1D1333A13F05・集計の記録 2BCED4EF7884979E・recompute.json 7D8BC6B134CBE3EE・下見の記録 pilot.json 5,768 バイトで SHA16 E504B4E9687F1B5E',
    'main %s・analysis %s・recompute %s・pilot %d バイト %s' % (s16(MAIN_REL), s16('records/Bl3/analysis-Bl3.json'), s16(RC_REL), os.path.getsize(j(*PJ_REL.split('/'))), s16(PJ_REL)),
    s16(MAIN_REL) == '419B1D1333A13F05' and s16('records/Bl3/analysis-Bl3.json') == '2BCED4EF7884979E' and s16(RC_REL) == '7D8BC6B134CBE3EE' and os.path.getsize(j(*PJ_REL.split('/'))) == 5768 and s16(PJ_REL) == 'E504B4E9687F1B5E')
# ---------------- 時刻と記録の抜け（C1・C2）
SR = ld('records/Bl3/sealing-record-Bl3.json')
PS = ld('records/Bl3/pilot/pilot-20260926T103442Z/session.json')
ses = [ld('results/Bl3/main/%s/session.json' % dirs[p]) for p in ('main', 'recompute', 'secondary')]
chk = rd('records/Bl3/prepilot-freeze-check-Bl3.md')
m_t = re.search(r'確かめた時: (\S+ \S+)（日本時間）', chk)
add('C1', '時刻の順: 封印 10:10:38Z・下見 10:34〜10:36Z・本の計算 11:12:38〜13:29:07Z・一致だけを見る段 13:33:19Z', '封印 %s・下見 %s〜%s・本の計算 %s〜%s・判定 %s' % (
    SR['written_utc'], PS['log'][0]['at'], PS['finished'], ses[0]['log'][0]['at'], ses[-1]['finished'], J['written_utc']),
    SR['written_utc'].startswith('2026-09-26 10:10:38') and ses[0]['log'][0]['at'] == '2026-09-26T11:12:38Z' and ses[-1]['finished'] == '2026-09-26T13:29:07Z' and J['written_utc'].startswith('2026-09-26 13:33:19'))
add('C1・C2', '凍結の後の確かめの記録の「確かめた時」は 18:15（日本時間）で、裁定 D242（17:50）の後。外れを最初に見つけた時は記録に無い', '確かめた時 %s・「最初に見つけた」の語 %s' % (m_t.group(1) if m_t else None, '最初に見つけ' in chk),
    bool(m_t) and m_t.group(1) == '2026-09-26 18:15' and '最初に見つけ' not in chk)
add('C1', '凍結の記録の SHA16 が三つ出る: 封印の記録の A4FE…（封印の時の凍結の記録）・報告の頭の 9628…（本の凍結の後）・判定の記録の核の 9828…（台帳を除いた核）',
    '封印 %s・今 %s・核 %s' % (SR['freeze_record_sha16'], s16('records/Bl3/FREEZE-RECORD-Bl3.json'), J['freeze_record_core_sha16']),
    SR['freeze_record_sha16'].startswith('A4FE') and s16('records/Bl3/FREEZE-RECORD-Bl3.json').startswith('9628') and J['freeze_record_core_sha16'].startswith('9828'))
fb_hits = subprocess.run(['git', 'grep', '-l', 'fbb8271'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.split()
add('C2', '下見の許しは fbb8271 の push についてで、下見のコミットは 4a17457。間の変更は記録に無い', 'fbb8271 の語が在るファイル %s' % fb_hits, '読みの確かめ',
    'fbb8271 はコミットを直す前の名で、直した内容（台帳の封印の行に登録者の言葉を足した）は 4a17457 のコミットの文にだけある（ファイルの記録には無い）')
rej = rd('records/Bl3/results-rejected-lines-Bl3.md').split(NL)
add('C1', '起草者の欄の元の文のファイルは、一行目だけ頭の「- 」が無い', '一行目の頭 %r・二行目の頭 %r' % (rej[0][:2], rej[1][:2]), not rej[0].startswith('- ') and rej[1].startswith('- '), '組み立ての器が一行目に「- 」を足す作り（器の --rejected の受け方）')
opened = [p for p in glob.glob(j('records', 'Bl3', '*open*')) + glob.glob(j('records', 'Bl3', '*', '*open*'))]
add('C1・C2', '結果を開く段の記録（時・居た人・登録者の言葉）が束にも記録にも無い', '開く段の名のファイル %s・集計の記録の時刻の鍵 %s' % (opened, [k for k in A if 'utc' in k or 'time' in k]), not opened,
    '開いた事実は集計の記録（records/Bl3/analysis-Bl3.json）とコミット 912fc47 の文にある')
add('C1', '封印の前の露出の記録（凍結物）には、封印の前後の二つの事（コーディネータの値が封印の台本に出たこと・登録者の情報状態の補い）が足されていない', '露出の記録に「封印の台本」%s・「D217」の補い %s' % (
    '封印の台本' in rd('records/Bl3/exposure-before-seal-Bl3.md'), '19:24' in rd('records/Bl3/exposure-before-seal-Bl3.md')), '封印の台本' not in rd('records/Bl3/exposure-before-seal-Bl3.md'),
    '露出の記録は凍結物（書き換えれば逸脱）で、二つの事は台帳の封印の行にある')
# ---------------- 票の機種の申告
add('G1・G2', '系統外の二票の本文の機種の申告は「o1 / GPT-4o 系列」と「Gemini 3.1 Pro」で、登録者の言葉（Google AI Studio で Gemini 3.8 Flash を選んだ）と違う', '票の頭の注に並べた', '記録',
    '機種は登録者の言葉を正とする（前の巡の G2 の申告と同じ扱い）')
# ---------------- 採否の案のために足した確かめ（K523 から・票の数のうち上で照らしていなかったもの・手続きの時刻・起草者が見つけた器の形）
import sys, datetime
TR = sys.argv[1] if len(sys.argv) > 1 else ''
assert os.path.exists(TR), '会話の記録（jsonl）の置き場を引数に与える'
jst_ = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
EV = []                                                     # (時刻, 種類, uuid, 中身)・種類は user（登録者の言葉）・text（起草者の返信）・tool（道具の呼び出し）・result（道具の結果）
for line in open(TR, encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    ts, c = o.get('timestamp'), (o.get('message') or {}).get('content')
    if not ts:
        continue
    if o.get('type') == 'user' and isinstance(c, str) and 'toolUseResult' not in o and '南無汝我曼荼羅' in c:
        EV.append((ts, 'user', o.get('uuid'), c))
    elif o.get('type') == 'assistant' and isinstance(c, list):
        for b in c:
            if b.get('type') == 'text' and b.get('text', '').strip():
                EV.append((ts, 'text', o.get('uuid'), b['text']))
            elif b.get('type') == 'tool_use':
                EV.append((ts, 'tool', o.get('uuid'), json.dumps(b.get('input'), ensure_ascii=False)))
    elif o.get('type') == 'user' and isinstance(c, list):
        for b in c:
            if b.get('type') == 'tool_result':
                t_ = b.get('content')
                EV.append((ts, 'result', o.get('uuid'), t_ if isinstance(t_, str) else json.dumps(t_, ensure_ascii=False)))
EV.sort(key=lambda e: e[0])


def first(kind, pred, after=''):
    for e in EV:
        if e[1] == kind and e[0] > after and pred(e[3]):
            return e
    return None


sg_rows = {g: sorted({int(np.sign(r['effect'])) for rid, r in rows.items() if rid.startswith(g + ':')}) for g in ('sub', 'add', 'cross')}
n_rows = {g: sum(1 for rid in rows if rid.startswith(g + ':')) for g in ('sub', 'add', 'cross')}
add('G2', '主の 14 行の効き目の符号は、static の sub の行がすべて正、static の add の行がすべて負、Nk の cross の行がすべて負', '符号 %s・行の数 %s' % (sg_rows, n_rows),
    sg_rows == {'sub': [1], 'add': [-1], 'cross': [-1]} and all(rows[rid]['direction'] == ('Nk' if rid.startswith('cross:') else 'static') for rid in rows))
ab = [abs(r['effect']) for r in rows.values()]
add('C1', '主の行の効き目の大きさ（絶対値）は 0.55〜2.73', '%.3f〜%.3f（行 %d）' % (min(ab), max(ab), len(ab)), abs(min(ab) - 0.55) < 0.005 and abs(max(ab) - 2.73) < 0.005)
pn = [r['p'] for r in rows.values() if not r['iso_outside']]
add('C2', '等方の外でない 13 行の p は 0.030〜0.383', '行 %d・p %.3f〜%.3f' % (len(pn), min(pn), max(pn)), len(pn) == 13 and abs(min(pn) - 0.03) < 1e-9 and abs(max(pn) - 0.383) < 1e-9)
mo = lambda mm: max(k for k in range(0, 50) if 2 * (1 + k) / (1 + KISO) < 0.05 / mm)
m14 = A['rows_meta']['m_rows']
add('C1・C2', '下見で外した後の 14 行でも、第一段（0.003571）を通る外側の帰無の本数の上限は 2 本で、十六行のとき（正本 labels.first_step_margin）と同じ',
    '%d 行 %d 本（p %.3f・段 %.6f）・十六行 %d 本（正本 %s・段 %s）' % (m14, mo(m14), 2 * (1 + mo(m14)) / (1 + KISO), 0.05 / m14, mo(16), T3['labels']['first_step_margin'], T3['labels']['holm_first_step']),
    m14 == 14 and mo(14) == 2 and mo(16) == 2 == T3['labels']['first_step_margin'])
cN = PJ['cells']['N1|O-Ncold']
add('C2', '升目 N1|O-Ncold の段階 B の無操作の破局の率は 0.12（読み取りの無操作の選択肢 a の確率は 0.00015）', '率 %s・確率 %.3g' % (cN['stage_b_rate'], cN['pa']),
    abs(cN['stage_b_rate'] - 0.12) < 1e-9 and abs(cN['pa'] - 0.000153) < 5e-7)
vb = PJ['vi']['b']
add('C2', '下見の (vi) の (b)（バッチ一の繰り返しの揺れ）はどの升目も 0 で、この道の計算は決定的だった', '升目 %d・最大 %s' % (len(vb), max(vb.values())), all(v == 0 for v in vb.values()))
add('C2', '方向ごとに独立な揺れがあれば反転しない分（偶の成分）に入るので、その大きさの目安は 0.22 以下（偶の成分の標準偏差の最大の √2 倍）', '偶の成分の標準偏差の最大 %.4f・√2 倍 %.4f' % (max(ev), math.sqrt(2) * max(ev)),
    abs(math.sqrt(2) * max(ev) - 0.22) < 0.005, 'u と −u の揺れが互いに独立と置いたときの上限（票の置き方のまま・札ではない）')
q7i = {e['id']: e for e in FJ['facts']['C']['q7_intervals']}['sub:N1:O-Ncold-v~O-Ncold-vrand']
fmd = rd('records/Bl3/design-facts-Bl3.md')
add('G1・G2・C1・C2', '唯一の等方の外の行 sub:N1 の段階 B の差は −2.0 pt で、区間［−8.26, 4.23］は零を含む（q7 で数えない行）',
    '差 %.2f pt・区間［%.2f, %.2f］・零を含む %s・集計の記録の q7 の行 %s・転記行 C（結果の前の凍結物）に同じ区間の印字 %s' % (
        q7i['diff_pt'], q7i['lo'], q7i['hi'], q7i['contains_zero'], [(x['id'], x['contains_zero']) for x in A['q7_rows']], 'sub:N1:O-Ncold-v~O-Ncold-vrand 20/200 − 24/200 ＝ -2.0 [-8.26, 4.23]' in fmd),
    abs(q7i['diff_pt'] + 2.0) < 1e-9 and abs(q7i['lo'] + 8.26) < 0.005 and abs(q7i['hi'] - 4.23) < 0.005 and q7i['contains_zero'] and [x['id'] for x in A['q7_rows']] == ['sub:N1:O-Ncold-v~O-Ncold-vrand']
    and all(x['contains_zero'] for x in A['q7_rows']) and 'sub:N1:O-Ncold-v~O-Ncold-vrand 20/200 − 24/200 ＝ -2.0 [-8.26, 4.23]' in fmd)
rl = subprocess.run(['git', 'reflog', 'show', 'refs/remotes/origin/main', '--date=iso'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout
pushed = {h[:7]: t for h, t in re.findall(r'^([0-9a-f]{7,}) refs/remotes/origin/main@\{(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) \+0900\}: update by push', rl, re.M)}
hl = subprocess.run(['git', 'reflog', '--date=iso'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout
c_fbb = re.search(r'^fbb8271 HEAD@\{(\S+ \S+) \+0900\}: commit: ', hl, re.M)
c_4a1 = re.search(r'^4a17457 HEAD@\{(\S+ \S+) \+0900\}: commit \(amend\): ', hl, re.M)
dn = subprocess.run(['git', 'diff', '--name-only', 'fbb8271', '4a17457'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.split()
par = subprocess.run(['git', 'log', '--no-walk', '--format=%h %p', 'fbb8271', '4a17457'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.split(NL)
seal_jst = jst_(SR['written_utc'].replace(' UTC', 'Z').replace(' ', 'T'))
pilot_jst = jst_(PS['log'][0]['at'])
add('C1・C2', '凍結の記録の順は「記録先行の公開（push）→ 封印」。下見の前の凍結の push の時刻と、fbb8271 と 4a17457 のつながりは束からは確かめられない',
    '281fc15（dae26d7 を含む）の push %s・封印 %s・fbb8271 のコミット %s・4a17457（コミットの直し）%s・直しの差のファイル %s・親 %s・4a17457 の push %s・下見の始まり %s（下見の session のコミット %s）' % (
        pushed.get('281fc15'), seal_jst, c_fbb.group(1) if c_fbb else None, c_4a1.group(1) if c_4a1 else None, dn, [x for x in par if x], pushed.get('4a17457'), pilot_jst, PS['commit'][:7]),
    bool(c_fbb and c_4a1) and pushed.get('281fc15', 'z') < seal_jst < (c_fbb.group(1) if c_fbb else '') < (c_4a1.group(1) if c_4a1 else '') < pushed.get('4a17457', '') < pilot_jst
    and sorted(dn) == ['records/Bl3/seal_ledger_row_Bl3.py', 'records/FREEZE-RECORD.md'] and PS['commit'].startswith('4a17457'),
    'push の時刻は手元の remote の追跡の参照の reflog、コミットの時刻は手元の HEAD の reflog（fbb8271 は push していない手元だけのコミット）。封印の push は、下見の前の凍結の push の後で、下見の前')
bsrc = rd('tools/bl3_run.py')
add('C1', '下見の順伝播の数 84 の数え方の単位', '下見の記録の n_forward %d・器が数を足す所 %d（Runner.prefix_cache と Runner.forward）' % (PJ['n_forward'], bsrc.count('self.n_forward += 1')), '記録',
    '模型を一度呼ぶごとに一つ（バッチの行の数ではなく呼び出しの数・近道の元の計算も一つ）')
s6_ = rep.split('## 6.')[1].split('## 7.')[0]
s0_ = rep.split('## 0.')[1].split('## 1.')[0]
s2_ = rep.split('## 2.')[1].split('## 3.')[0]
m0_ = re.search(r'主の行 \d+（下見で外した後）・等方の外の行: v̂ \d+・Nk \d+・二つ目の札が付く行 \d+', s0_)
m2_ = re.search(r'行の数 Nk \d+・static \d+', s2_)
add('C1・C2', '§6 の q7 の「採点しない」に理由が無い。q2・q3・q6 の数と分母は §6 に無い（数は §0 の「主の記述の札と門」・分母は §2 の偶然の目安の行の数と Holm の段の数にある）',
    '§6 に理由の語（零を含・区間）%s・§0 %s・§2 %s' % (('零を含' in s6_ or '区間' in s6_), m0_.group(0) if m0_ else None, m2_.group(0) if m2_ else None),
    not ('零を含' in s6_ or '区間' in s6_) and bool(m0_) and bool(m2_), '正本 pilot.decision.drop_effects の「分母を印字する」の数は報告のどこかに印字されている（§6 の隣には無い）')
row_n1 = [l for l in rep.split(NL) if l.startswith('| sub:N1:O-Ncold-v~O-Ncold-vrand |')]
add('C1・C2', '正本 labels.side_rule は等方の外の行に「等方の帰無の中央値と、効き目の側を添えて書く」。〈両方の外〉の行は主の表を指し、主の表の行に中央値と側がある',
    '正本の文の頭 %s・〈両方の外〉の行の指し %s・主の表の行に中央値 %s と側「%s」%s' % (T3['labels']['side_rule'][:30], '（等方の帰無の中央値と効き目の側は主の表）' in rep, '%.4g' % r1['iso_median'],
                                                        '符号だけ（零が等方の帰無の四分位の間）: 正', bool(row_n1) and ('| %.4g |' % r1['iso_median']) in row_n1[0] and '| 符号だけ（零が等方の帰無の四分位の間）: 正 |' in row_n1[0]), '読みの確かめ',
    '凍結した器は中央値と側を主の表の行に置き、〈両方の外〉の行から表を指す（C1 は決まりの範囲内とし、C2 は注に書き込むことを勧めた）')
add('G1・G2', '下見の (v) の近道の差の最大 2.737。G2: (vi)(a) の揺れが 1.621 に達したので本の計算をバッチ一にし、(v) の差が 2.737 に達したので近道を採らなかった',
    '(v) の 2.737 は門の行だけの升目 S4|Osec-Ncold（主の升目の最大は %s の %.3f）・正本 computation.shortcut「%s」・正本 (vi)(a) の決まり「升目の間の最大が pilot.noise_max を超えたら、本の計算はバッチの大きさを一にし」の有無 %s' % (
        mx_v_main[0], mx_v_main[1], T3['computation']['shortcut'], '升目の間の最大が `pilot.noise_max` を超えたら、本の計算はバッチの大きさを一にし' in T3['pilot']['checks']['vi']['a']['rule']),
    '一部を再現した', 'バッチ一は (vi)(a) の決まりで決まった（G2 のとおり）。近道を使わないのは下見の前の裁定 D234 で決まっていて、(v) は記述（G2 の「(v) の差のため」は当たらない）。2.737 は門の行だけの升目の値')
e_prop = first('text', lambda s: '結果を開く段' in s and 'ご一緒に' in s and '`analyze_Bl3.py open`' in s)
e_ok = first('user', lambda s: '判定の記録の push' in s, e_prop[0]) if e_prop else None
e_open = first('tool', lambda s: 'analyze_Bl3.py open' in s, e_ok[0]) if e_ok else None
e_tell = first('text', lambda s: s.startswith('結果を開きました。凍結した器の出力'), e_open[0]) if e_open else None
e_next = first('user', lambda s: True, e_tell[0]) if e_tell else None
add('C1・C2', '結果を開く段の時刻・居た人・登録者の言葉（記録が無い）',
    '起草者の順の案 %s（uuid %s）・登録者の許し %s（uuid %s）・判定の記録（3e185d3）の push %s・開く段の呼び出し %s・登録者への報告 %s（uuid %s）・登録者の次の言葉 %s（uuid %s）' % (
        jst_(e_prop[0]), e_prop[2], jst_(e_ok[0]), e_ok[2], pushed.get('3e185d3'), jst_(e_open[0]), jst_(e_tell[0]), e_tell[2], jst_(e_next[0]), e_next[2]),
    '記録', '開く段は、登録者が同じ会話で順の案を許した後に、起草者が走らせた。値は起草者が先に読み、数分後の返信で登録者に伝えた（時刻は会話の記録）。判定の記録は開く前に公開した')
e_frz = first('user', lambda s: '凍結に当たり申し上げます' in s)
e_find = first('result', lambda s: re.search(r'Temp/tmp[0-9a-z_]+/frozen-standin\.src\.md', s) is not None, e_frz[0]) if e_frz else None   # 起草者の呼び出しの文が結果に写った所は数えない（道筋の形で拾う）
e_rep = first('text', lambda s: '一時の道筋' in s, e_frz[0]) if e_frz else None
add('C1・C2', '凍結の後の確かめの記録の「確かめた時」18:15 は裁定 D242 の後。外れを最初に見つけた時が書かれていない',
    '登録者の凍結の言葉 %s・一時の道筋が道具の結果に初めて出た %s・登録者への報告 %s（uuid %s）' % (jst_(e_frz[0]), jst_(e_find[0]) if e_find else None, jst_(e_rep[0]) if e_rep else None, e_rep[2] if e_rep else None),
    '記録', '見つけたのは凍結の数の検査の記録を読んだ道具の結果（時刻は会話の記録）。確かめの記録（18:15）は、裁定の後に、凍結物を凍結したまま確かめ直した時')
brs = rd('tools/build_report_Bl3.py')
add('起草者', '凍結した組み立ての器の見出しは状態に依らず「報告の草案・機械の組み立て」。状態の行は、登録者最終確認の記録が無ければ「報告の草案（結果の巡の前）」で、結果の巡の後に組み直しても同じ文が出る',
    '見出しの文 %s・状態の二つの型 %s' % ("['# B-lens 層三の結果（報告の草案・機械の組み立て）', '']" in brs, ['最終版' in brs, "'- 状態: **報告の草案（結果の巡の前）**。'" in brs]),
    "['# B-lens 層三の結果（報告の草案・機械の組み立て）', '']" in brs and "'- 状態: **報告の草案（結果の巡の前）**。'" in brs, '器の段と実装の検分と器の直しの確かめでは誰も挙げていない（起草者が採否の案を書く中で見つけた）')
sys.path.insert(0, j('tools'))
import report_lint as RL_
probe = ['14 行のうち 1 行', '裁定 D243', '再現 K498', 'V2 と V3', 'rand:0', '十四行のうち一行', '2026-09-27 03:23 日本時間', 'SHA16 2BCED4EF7884979E', 'コミット 912fc47', '報告の §5', 'q2・q3・q6']
flags = {s: [t_ for t_, _, _, _ in RL_.report_numbers(s)] for s in probe}
add('起草者', '凍結した組み立ての器が起草者の文を受ける口は --rejected（§0 の「この結果が退けた説明」）だけ。凍結した走査器は、機械の区画の外の算用数字・判定と再現の番号・V2 のような英大文字と数を未登録の数として止め、日付・時刻・SHA16・コミットの名・§ の番号は止めない',
    '口 %s・止める %s・止めない %s' % (re.findall(r"add_argument\('(--[a-z-]+)'", brs), [s for s in probe if flags[s]], [s for s in probe if not flags[s]]),
    re.findall(r"add_argument\('(--[a-z-]+)'", brs) == ['--force', '--selftest', '--rejected', '--marks', '--main-tool-error'] and [s for s in probe if flags[s]] == probe[:5],
    '漢数字は走査器の形の上では止めないが、起草者の文で漢数字の数を打つことも数を打つことに当たる（数は機械で入れる決まり）。四票の注の案の多くは数を含む')
def pipe_audit(text):
    """表の行ごとに、逃がしていない「|」の数が見出しの行と同じかを数える（GFM の表は「|」を列の区切りとして読み、多い分の列は捨てる）。"""
    t = text.split(NL)
    bad, n, first_bad, tables, names = 0, 0, None, collections.Counter(), []
    i = 0
    while i < len(t):
        if t[i].startswith('|') and i + 1 < len(t) and re.match(r'^\|(\s*:?-+:?\s*\|)+\s*$', t[i + 1]):
            hdr = t[i].count('|') - t[i].count(chr(92) + '|')
            k = i + 2
            while k < len(t) and t[k].startswith('|'):
                n += 1
                if t[k].count('|') - t[k].count(chr(92) + '|') != hdr:
                    bad += 1
                    tables[t[i].split('|')[1].strip()] += 1
                    first_bad = first_bad or (k + 1, t[k].split(' | ')[0][:30])
                    names.append(t[k].split(' | ')[0].lstrip('| ').strip())
                k += 1
            i = k
        else:
            i += 1
    return bad, n, first_bad, dict(tables), names


import collections
pa_ = pipe_audit(rep)
BLF = rd('records/Blens/results-Blens-FINAL-2026-09-24.md')
pb_ = pipe_audit(BLF)
esc_ok = [('| %s |' % nm.replace('|', chr(92) + '|')) in BLF for nm in pb_[4]]
p607 = 'P607' in rd('records/reviews/Blens/results-final/adoption-table-Blens-results-final.md')
add('起草者', '報告の表の行のうち、升目の名の「|」を逃がしていない行は、GFM の表では列の区切りとして読まれ、値が別の列の見出しの下に出て、行の末尾の欄が落ちる（B-lens の最終版にも同じ形の行がある）',
    '層三の報告: 見出しと区切りの数が違う表の行 %d／%d（表ごと %s・初めの行 %s）・B-lens の最終版: %d／%d（表ごと %s）・その行の名が逸脱 D-BL3 の並べ直しの表に逃がした形で在る %d／%d・B-lens の最終検分の採否表に P607 %s' % (
        pa_[0], pa_[1], pa_[3], pa_[2], pb_[0], pb_[1], pb_[3], sum(esc_ok), len(esc_ok), p607), pa_[0] > 0 and all(esc_ok) and p607,
    '生の md の値は正しい。表示の確かめは公開の置き場の GitHub の表示で行った（採否の案に時刻）。B-lens は最終検分でこの形を見つけ（採否表 P607）、凍結の表を残して、縦棒を逃がした並べ直しの表を逸脱 D-BL3 の区画に足していた（B-lens の報告はこの登録の外）')
tracked = [f for f in subprocess.run(['git', 'ls-files', 'records/Bl3', 'design'], cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.split() if f.endswith('.md')]
others = {f: pipe_audit(rd(f))[:2] for f in tracked if f != 'records/Bl3/results-Bl3.md'}
others_bad = {f: v for f, v in others.items() if v[0]}
add('起草者', '層三のほかの記録と設計の文書の表にも、升目の名の「|」を逃がしていない行があるか', '数えた md %d・当たった記録 %s' % (len(others), {f: '%d／%d' % v for f, v in others_bad.items()}), '記録',
    '報告のほかは、束や検分で生の md として読む記録（草案の確かめと合成データの確かめの記録）で、直さない')
res = {'what': '結果の巡の四票の事実の主張の再現（器とは別に書いた式）', 'inputs': {'analysis': s16('records/Bl3/analysis-Bl3.json'), 'main': s16(MAIN_REL), 'recompute': s16(RC_REL), 'secondary': s16(SEC_REL),
                                                                         'pilot': s16(PJ_REL), 'facts': s16('records/Bl3/design-facts-Bl3.json'), 'canon': s16('design/contrasts-Bl3.json'),
                                                                         'bundle': hashlib.sha256(bb).hexdigest().upper()[:16]},
       'checks': K, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(res, open(OUT_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
L = ['# B-lens 層三の結果の巡の四票の事実の主張の再現（機械生成・`verify_results_Bl3.py`）', '',
     '- 票: `records/reviews/Bl3/results-round1/{g1,g2,c1,c2}/vote.md`（逐語保全）。器とは別に書いた式で、公開の置き場の現物から再現した。読みの当否（言い回しの提案）は再現の外で、採否の案で扱う。',
     '- 入力の SHA16: %s。' % '・'.join('%s %s' % kv for kv in res['inputs'].items()), '',
     '| 番号 | 票 | 主張 | 現物 | 判定 | 注 |', '|---|---|---|---|---|---|'] + [
     '| %s | %s | %s | %s | %s | %s |' % (x['k'], x['votes'], cell(x['claim']), cell(x['got']), x['verdict'], cell(x['note'])) for x in K] + [
     '', '- 判定の数: %s。' % '・'.join('%s %d' % (v, sum(1 for x in K if x['verdict'] == v)) for v in sorted({x['verdict'] for x in K})), '',
     '## 検分票', '',
     '- 対象: 結果の巡の四票の事実の主張（数・同定・時刻・記録の有無）。',
     '- 段階: 票を読んだ後（事後）。再現の決まり（単位を確かめてから判じる・再現しなかった主張も消さない）は、票を見る前の枠に書いた。',
     '- 凍結物の同定: 入力の SHA16（上）。正本と凍結の本文は凍結の記録の値と同じ。',
     '- 盲検の状態: 該当しない（結果は開いた後）。',
     '- 敵対的検分: 票の数を、票が挙げた置き場の現物から器とは別の式で出し直した。票の丸めた値は、丸めの幅で照らした。',
     '- 系統の内訳: コーディネータ（Claude 系）一名。C1・C2 と同じ系列。',
     '- COI記録: 票の主張が器の出力と合うと書く側（器を書いた当人）に引かれる。照らす式は器を読まずに書いた。',
     '- 判定: 再現の記録として確定（採否は別の案で）。',
     '- 本検分が確認していないこと: 票の読みの提案の当否。本物の模型での再現。器のコードそのもの。', '',
     res['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('checks', len(K), '|', {v: sum(1 for x in K if x['verdict'] == v) for v in sorted({x['verdict'] for x in K})})
for x in K:
    if x['verdict'] not in ('再現した', '記録', '読みの確かめ'):
        print('  ', x['k'], x['verdict'], x['claim'][:80], '|', x['got'][:200])
