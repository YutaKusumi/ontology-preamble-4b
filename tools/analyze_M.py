# -*- coding: utf-8 -*-
"""analyze_M.py v1 —— 追補 M の集計器。対比・向き・m・門・複製規則・配線・撤退条件・drift は `design/contrasts-M.json` だけから読む。
確証は第一走行（--tag）のみ・両側 Fisher・全分母・族ごと Holm（m は JSON）。門の結果は gate_M.py の JSON（--gate 必須・dry-run 検査のみ --no-gate）。
refuse 門（答えた分母で向き不一致→判定保留）・様式門（(a)(b) の差 >30pt→判定保留・15pt 超は注・様式は records/M/style-<tag>.json＝response_mode_M.py の出力を読み、無ければ計算）・
本走行の連続性条件（Nk-Ncold の V′ からの 5pt 帯）・drift (i)(iii)（参照腕の帯）・固有の札（三段）・M-b 配線・M-c 配線・主張規則（検出域の幾何）・反証条件・複製六札（--tag2）を機械判定して印字。
記述族には p を印字しない（例外＝複製規則 ⑤ の一覧）。system 腕の system_sha を台帳と突合。出力名固定・上書きなし。
用法: python tools/analyze_M.py --tag stageM1 --gate records/M/gate-pilotM-<date>.json [--tag2 stageM2]
"""
import os, sys, json, glob, math, argparse, collections
from scipy.stats import fisher_exact
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(REPO, 'tools'))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--tag2', default=None); ap.add_argument('--gate', default=None); ap.add_argument('--no-gate', action='store_true')
ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-M.json')); ap.add_argument('--style', default=None); ap.add_argument('--style2', default=None); ap.add_argument('--out-suffix', default='')
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8')); Z = 1.959963985; n_main = T['n_per_arm']
if not args.gate and not args.no_gate:
    sys.exit('--gate（門の JSON）は必須。dry-run／合成検査のみ --no-gate。')
gate = json.load(open(args.gate, encoding='utf-8'))['results'] if args.gate else {}
_ids = [c['id'] for F in list(T['families'].values()) + list(T['descriptive_families'].values()) for c in F['contrasts']]
assert len(_ids) == len(set(_ids)), 'id が全族で一意でない'
LM = json.load(open(os.path.join(REPO, 'arms', 'panelM', 'SHA-LEDGER-M.json'), encoding='utf-8'))
SYS_SHA_EXPECT = {d['name']: (None if d['system'] == 'none' else {'O': 'F3EE60C33F825575', 'Onull': '2123B3CD8586E7DF'}.get(d['system']) or LM['system'][os.path.splitext(d['system'])[0]]) for d in T['arms']['system']}
ALL_ARMS = T['arms']['preamble'] + [d['name'] for d in T['arms']['system']]


def load_cells(tag):
    C = {}; dirs = []
    for f in glob.glob(os.path.join(REPO, 'results', '*', tag + '__*', 'cells.json')):
        d = json.load(open(f, encoding='utf-8')); C.setdefault(d['manifest']['scenario'], {}).update(d['cells']); dirs.append(os.path.dirname(f))
    return C, dirs


def load_style(tag, path, dirs):
    if path and os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))['runs']
    p = os.path.join(REPO, 'records', 'M', 'style-%s.json' % tag)
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8'))['runs']
    import response_mode_M as RM
    runs = {}
    for d in dirs:
        sc, key, out = RM.analyze_run(d); runs.setdefault(sc, {}).update(out)
    return runs


cells1, dirs1 = load_cells(args.tag); style1 = load_style(args.tag, args.style, dirs1)
cells2, dirs2 = (load_cells(args.tag2) if args.tag2 else ({}, [])); style2 = load_style(args.tag2, args.style2, dirs2) if args.tag2 else {}


def wilson(k, n):
    if not n:
        return '—'
    p = k / n; dd = 1 + Z * Z / n; c = (p + Z * Z / (2 * n)) / dd; h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / dd
    return '[%.3f, %.3f]' % (c - h, c + h)


def holm(pv, m):
    order = sorted(pv, key=lambda x: x[1]); out = {}; prev = 0.0
    for i, (lab, p) in enumerate(order):
        adj = min(1.0, max(prev, (m - i) * p)); prev = adj; out[lab] = (adj, adj <= 0.05)
    return out


out = ['# 追補 M 結果表（機械集計・解釈なし）—— 第一走行 tag %s%s・contrasts %s・門 %s' % (args.tag, ('・第二走行 tag %s' % args.tag2) if args.tag2 else '', T['version'], os.path.basename(args.gate) if args.gate else '（検査・門なし）'), '',
       '確証は第一走行のみ・全分母・両側 Fisher・族ごと Holm（m は JSON）。門で降格した対比は「判定不能（床／天井）」（m 不変）。refuse 門・様式門は本走行の数で走行ごとに判定。Δrefuse＝A−B。第二走行は複製六札。', '']
# ---- 整合: 腕の欠落・system_sha 突合
for tag, C in ((args.tag, cells1), (args.tag2, cells2)):
    if not tag:
        continue
    miss = {sc: [a for a in ALL_ARMS if a not in C.get(sc, {})] for sc in T['scenarios']}
    bad = [(sc, a, C[sc][a].get('system_sha')) for sc in C for a in C[sc] if a in SYS_SHA_EXPECT and C[sc][a].get('system_sha') != SYS_SHA_EXPECT[a]]
    out.append('- 整合（%s）: 欠落腕 %s／system_sha 台帳突合 不一致 %d 件%s' % (tag, {sc: len(v) for sc, v in miss.items()}, len(bad), ('・' + str(bad[:3])) if bad else ''))
    if bad and not args.no_gate:
        sys.exit('[analyze] system_sha が台帳と不一致: %s' % bad[:3])
out.append('')
# ---- 三つ組（第一走行）
for sc in T['scenarios']:
    c = cells1.get(sc)
    if not c:
        out.append('## %s（未走行）' % sc); continue
    out += ['## %s 三つ組（第一走行）' % sc, '| 腕 | n_ok | 破局 | 率 | Wilson | refuse | 書式外 | 答えた分母 率 | 様式 (a) 名言及 | 様式 (b) JSON 直答 | 初回 (a)/(b) |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for a in ALL_ARMS:
        x = c.get(a); s = style1.get(sc, {}).get(a, {})
        if not x:
            continue
        out.append('| %s | %d | %s | %s | %s | %d | %d | %s | %s | %s | %s/%s |' % (a, x['n_ok'], x.get('catastrophe'), x.get('catastrophe_rate_all'), wilson(x['catastrophe'], x['n_ok']), x['refuse'], x['format_fail'], x.get('catastrophe_rate_answered'), s.get('a_rate_final', '—'), s.get('b_rate_final', '—'), s.get('a_rate_first', '—'), s.get('b_rate_first', '—')))
    out.append('')
# ---- 連続性（本走行 5pt 帯）と drift (i)
CT = T['continuity']; DR = T['descriptive_families']['M_desc_drift']['constraints']; VP = {sc: T['scenarios'][sc]['vprime_stageVp'] for sc in T['scenarios']}
def continuity_flags(C):
    fl = {}
    for sc in T['scenarios']:
        x = C.get(sc, {}).get(CT['main_5pt']['arm'])
        if not x:
            continue
        k = x['catastrophe']; thr = CT['main_5pt']
        fl[sc] = (k >= thr['N1_ge']) if sc == 'N1' else (k <= thr[sc + '_le'])
    return fl
def drift_i_flags(C):
    fl = {}
    for sc in T['scenarios']:
        cnt = 0; det = []
        for a in DR['ref_arms_preamble']:
            x = C.get(sc, {}).get(a)
            if x and x['n_ok']:
                d = abs(x['catastrophe'] / x['n_ok'] - VP[sc][a] / 400); det.append('%s %+.3f' % (a, x['catastrophe'] / x['n_ok'] - VP[sc][a] / 400))
                if d * 100 >= DR['vs_vprime_pt'] - 1e-9:
                    cnt += 1
        fl[sc] = (cnt >= DR['vs_vprime_min_cells'], cnt, det)
    return fl
cont1 = continuity_flags(cells1); dr1 = drift_i_flags(cells1)
out += ['## 連続性条件（本走行・Nk-Ncold の V′ からの 5pt 帯・転記行 E′）と drift (i)（参照 5 腕・5pt・転記行 M′）', '| シナリオ | 走行 | Nk-Ncold 破局/n | 5pt 帯 発火 | drift (i) 5pt 以上のセル数 | 発火（≥%d） | 差の内訳 |' % DR['vs_vprime_min_cells'], '|---|---|---|---|---|---|---|']
for sc in T['scenarios']:
    for tag, C, cf, df in ((args.tag, cells1, cont1, dr1),) + (((args.tag2, cells2, continuity_flags(cells2), drift_i_flags(cells2)),) if args.tag2 else ()):
        x = C.get(sc, {}).get(CT['main_5pt']['arm'])
        if x:
            out.append('| %s | %s | %d/%d | %s | %d | %s | %s |' % (sc, tag, x['catastrophe'], x['n_ok'], '**発火**' if cf.get(sc) else '—', df[sc][1], '**発火**' if df[sc][0] else '—', '・'.join(df[sc][2])))
out.append('')
# ---- 確証族
CONF = {}; SIGN = {}; STATUS = {}; SG = T['style_gate']; RG = T['refuse_guard']


def cell_stats(C, ct):
    A = C.get(ct['scenario'], {}).get(ct['A']); B = C.get(ct['scenario'], {}).get(ct['B'])
    if not A or not B or not A['n_ok'] or not B['n_ok']:
        return None
    a, na, b, nb = A['catastrophe'], A['n_ok'], B['catastrophe'], B['n_ok']
    return dict(a=a, na=na, b=b, nb=nb, ra=a / na, rb=b / nb, p=fisher_exact([[a, na - a], [b, nb - b]])[1], dref=A['refuse'] - B['refuse'], ansA=A.get('catastrophe_rate_answered'), ansB=B.get('catastrophe_rate_answered'))


def style_check(S, ct):
    sa = S.get(ct['scenario'], {}).get(ct['A']); sb = S.get(ct['scenario'], {}).get(ct['B'])
    if not sa or not sb:
        return None, None, None
    da = abs((sa.get('a_rate_final') or 0) - (sb.get('a_rate_final') or 0)); db = abs((sa.get('b_rate_final') or 0) - (sb.get('b_rate_final') or 0)) if (sa.get('b_rate_final') is not None and sb.get('b_rate_final') is not None) else 0
    mx = max(da, db); nA = sa.get('n_ok') or 0
    # 「超」＝観測差の件数が strict_greater_trials を厳密に上回る（n=400 なら 120）
    susp = (mx * nA) > SG['strict_greater_trials'] * nA / n_main if nA else False
    note = (mx * 100 > SG['note_pt']) and not susp
    # 層別（(b) 二層・両腕 n≥min）
    strat = []
    for key in ('json_direct', 'prose'):
        xa = (sa.get('strata_final') or {}).get(key); xb = (sb.get('strata_final') or {}).get(key)
        if xa and xb and xa['n'] >= SG['min_stratum_n'] and xb['n'] >= SG['min_stratum_n']:
            d = xa['catastrophe'] / xa['n'] - xb['catastrophe'] / xb['n']; strat.append((key, xa['n'], xb['n'], d))
    return (mx, susp, note), strat, (da, db)


def family_table(fam, F, C, S, gate_res, second=False):
    items = []
    for ct in F['contrasts']:
        v = cell_stats(C, ct)
        if v is None:
            if not args.no_gate:
                sys.exit('対比 %s のセルが欠落——Holm の m と実数が食い違うため停止' % ct['id'])
            continue
        items.append((ct['id'], ct, v))
    hp = holm([(lab, v['p']) for lab, ct, v in items], F['m']) if items else {}
    res = {}
    for lab, ct, v in items:
        adj, rej = hp[lab]; d = v['ra'] - v['rb']; sign = 1 if d > 0 else -1 if d < 0 else 0
        g = gate_res.get(lab, {}); dg = g.get('status', '').startswith('downgraded')
        st = 'gate' if dg else ('confirmed' if rej else 'ns'); why = []
        if st == 'confirmed':
            aA, aB = v['ansA'], v['ansB']
            if not (aA is not None and aB is not None and ((aA > aB) if sign > 0 else (aA < aB))):
                st = 'hold_refuse'; why.append('答えた分母 %s 対 %s' % (aA, aB))
        sty, strat, dab = style_check(S, ct)
        if st == 'confirmed' and sty and sty[1]:
            st = 'hold_style'; why.append('様式差 %.0f pt' % (sty[0] * 100))
        note = ('様式差あり（%.0f pt）' % (sty[0] * 100)) if (sty and sty[2]) else ''
        cf = cont1 if not second else continuity_flags(C); dr = dr1 if not second else drift_i_flags(C)
        if cf.get(ct['scenario']) and st == 'confirmed':
            note += '・断面の乖離（連続性条件）'
        if dr.get(ct['scenario'], (False,))[0] and st == 'confirmed':
            note += '・参照腕が V′ から乖離（drift i）'
        res[lab] = dict(v, adj=adj, status=st, sign=sign, why='・'.join(why), note=note, strat=strat, style=sty, dab=dab, ct=ct)
    return res


def status_label(r):
    return {'gate': '判定不能（門: %s）', 'confirmed': '**確証（有意）**', 'ns': '非有意', 'hold_refuse': '**判定保留（refuse 転位）**', 'hold_style': '**判定保留（様式転位）**'}[r['status']] % (gate.get(r['ct']['id'], {}).get('reason', '') if r['status'] == 'gate' else ())


FAMRES = {}
for fam, F in T['families'].items():
    R = family_table(fam, F, cells1, style1, gate); FAMRES[fam] = R
    out += ['## 族 %s（m=%d・第一走行）——%s' % (fam, F['m'], F['question']), '| 対比 | A 破局/n（率・Wilson） | B 破局/n（率・Wilson） | 差 | p(両側) | Holm | 判定 | 向き | Δrefuse | 答えた分母 A/B | 様式差 (a)/(b) | 層別（層・nA・nB・差） | 注 |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for lab, r in R.items():
        CONF[lab] = (r['status'] == 'confirmed'); SIGN[lab] = r['sign']; STATUS[lab] = r['status']
        st = status_label(r) + (('（%s）' % r['why']) if r['why'] else '')
        strat = '・'.join('%s %d/%d %+.3f' % (k, na, nb, d) for k, na, nb, d in (r['strat'] or [])) or ('層別不能' if r['style'] else '—')
        out.append('| %s | %d/%d (%.3f %s) | %d/%d (%.3f %s) | %+.3f | %.2e | %.2e | %s | %s | %+d | %s / %s | %s | %s | %s |' % (lab, r['a'], r['na'], r['ra'], wilson(r['a'], r['na']), r['b'], r['nb'], r['rb'], wilson(r['b'], r['nb']), r['ra'] - r['rb'], r['p'], r['adj'], st, '+' if r['sign'] > 0 else '−' if r['sign'] < 0 else '0', r['dref'], r['ansA'], r['ansB'], ('%.2f/%.2f' % r['dab']) if r['dab'] else '—', strat, r['note'] or '—'))
    # 一斉保留の所見（シナリオごと）
    for sc in T['scenarios']:
        nh = sum(1 for r in R.values() if r['ct']['scenario'] == sc and r['status'] == 'hold_style'); nj = sum(1 for r in R.values() if r['ct']['scenario'] == sc and r['status'] != 'gate')
        if nj and nh / nj > 0.5:
            out.append('**第一の所見（機械札・%s）**: 判定可能な %d 本のうち %d 本が様式門で保留——「破局率の差は応答様式の転換と分離できなかった」。様式率の表を主結果として報告する（JSON style_gate）。' % (sc, nj, nh))
    out.append('')


def judgeable(lab):
    return STATUS.get(lab) in ('confirmed', 'ns')


def pairtype(ct):
    a, b = ct['A'], ct['B']
    for tl in T['tails']:
        pass
    return None


# ---- 固有の札（三段・M_a）
Fa = T['families']['M_a']; out += ['## 固有の札（三段・JSON tier_rule・第一走行・同じ向きの確証を要件）', '| シナリオ | 名 | 梵転写に固有（TS~PS・TS~MS） | カナ表記に固有（TK~PK・TK~MK） | 真言に固有（両表記） | 副対比 TS~T0・PS~T0 |', '|---|---|---|---|---|---|']
TIER = {}
def find(sc, name, a, b):
    A = 'Nk-Ncold' if (name, a) == ('Kan', 'T0') else '%sF1%s-Ncold' % (name, a); B = 'Nk-Ncold' if (name, b) == ('Kan', 'T0') else '%sF1%s-Ncold' % (name, b)
    return '%s:%s~%s' % (sc, A, B)
def same_sign_confirmed(labs):
    return all(CONF.get(l) for l in labs) and len({SIGN[l] for l in labs}) == 1
for sc in T['scenarios']:
    for name in T['confirmatory_names']:
        t1 = [find(sc, name, 'TS', 'PS'), find(sc, name, 'TS', 'MS')]; t2 = [find(sc, name, 'TK', 'PK'), find(sc, name, 'TK', 'MK')]
        s1, s2 = same_sign_confirmed(t1), same_sign_confirmed(t2); s3 = s1 and s2 and len({SIGN[l] for l in t1 + t2}) == 1
        TIER[(sc, name)] = (s1, s2, s3)
        sub = [find(sc, name, 'TS', 'T0'), find(sc, name, 'PS', 'T0')]
        subtxt = '・'.join('%s %s' % (l.split(':')[1], '確証' if CONF.get(l) else STATUS.get(l, '—')) for l in sub)
        extra = ''
        if all(CONF.get(l) for l in sub) and not CONF.get(t1[0]):
            extra = '（TS と PS は区別できなかった〔差の否定ではない〕）'
        out.append('| %s | %s | %s | %s | %s | %s%s |' % (sc, name, '**立つ**' if s1 else '立たない', '**立つ**' if s2 else '立たない', '**立つ**' if s3 else '立たない', subtxt, extra))
if not any(any(v) for v in TIER.values()):
    out.append('**反証条件 (i)（JSON）**: %s' % Fa['falsification']['text'])
out.append('')
# ---- M-b 配線
Fb = T['families']['M_b']; out += ['## M-b 配線（JSON wiring_rule・第一走行）', '| シナリオ | 名 | F2~F1 | F2~F4 | 札 | F3~F1 | F3~F4 | 札 |', '|---|---|---|---|---|---|---|---|']
def fb(sc, name, a, b):
    A = 'Nk-Ncold' if (name, a) == ('Kan', 'F1') else '%s%sT0-Ncold' % (name, a); B = 'Nk-Ncold' if (name, b) == ('Kan', 'F1') else '%s%sT0-Ncold' % (name, b)
    return '%s:%s~%s' % (sc, A, B)
BWIRE = {}; anyF1 = False
for sc in T['scenarios']:
    for name in T['names']:
        row = [sc, name]
        for f in ('F2', 'F3'):
            l1, l4 = fb(sc, name, f, 'F1'), fb(sc, name, f, 'F4'); c1, c4 = CONF.get(l1, False), CONF.get(l4, False); anyF1 |= c1
            lab = ('**%s の枠付け語に固有**' % f) if (c1 and c4 and SIGN[l1] == SIGN[l4]) else ('束の差（F1 以外の三形式に共通）' if c1 else ('F4 とは異なるが F1 とは区別できなかった' if c4 else ('判定不能' if STATUS.get(l1) == 'gate' and STATUS.get(l4) == 'gate' else '差なし（区別できなかった）')))
            BWIRE[(sc, name, f)] = lab; row += [STATUS.get(l1, '—'), STATUS.get(l4, '—'), lab]
        out.append('| ' + ' | '.join(row) + ' |')
if not anyF1 and any(judgeable(fb(sc, nm, f, 'F1')) for sc in T['scenarios'] for nm in T['names'] for f in ('F2', 'F3')):
    out.append('**反証条件 (ii)（JSON）**: %s' % Fb['falsification']['text'])
out.append('「として句が違った」はいかなる条件でも書かない（F1 は Ncold と同一語形・JSON wiring_rule）。'); out.append('')
# ---- M-c 配線
Fc = T['families']['M_c']; out += ['## M-c 配線（JSON wiring_rule・第一走行）', '| シナリオ | L | 対 -PS | 対 -MS | 対 -T0 | 札 | L 破局/n・Wilson 上限（sysNone-Ncold との差を先に） |', '|---|---|---|---|---|---|---|']
CWIRE = {}; anyC = False
for sc in T['scenarios']:
    for L in ('sysLAmi', 'sysLKan'):
        ls = {v: '%s:%s~%s%s' % (sc, L, L, v) for v in ('-PS', '-MS', '-T0')}; st = {v: STATUS.get(l, '—') for v, l in ls.items()}
        cps, cms, ct0 = CONF.get(ls['-PS'], False), CONF.get(ls['-MS'], False), CONF.get(ls['-T0'], False); anyC |= (cps or cms or ct0)
        lab = '**当該末尾の文字列に固有**' if (cps and cms and SIGN[ls['-PS']] == SIGN[ls['-MS']]) else ('無意味列とは異なるが有意味列とは区別できなかった' if cps else ('末尾に文字列があることと整合する読みまで' if ct0 else '差なし（区別できなかった）'))
        CWIRE[(sc, L)] = lab
        x = cells1.get(sc, {}).get(L); z = cells1.get(sc, {}).get('sysNone-Ncold')
        zt = ('sysNone-Ncold %d/%d との差 %+.3f・' % (z['catastrophe'], z['n_ok'], x['catastrophe'] / x['n_ok'] - z['catastrophe'] / z['n_ok']) if (x and z) else '') + ('%s %d/%d Wilson %s' % (L, x['catastrophe'], x['n_ok'], wilson(x['catastrophe'], x['n_ok'])) if x else '—')
        out.append('| %s | %s | %s | %s | %s | %s | %s |' % (sc, L, st['-PS'], st['-MS'], st['-T0'], lab, zt))
if not anyC and any(judgeable('%s:%s~%s%s' % (sc, L, L, v)) for sc in T['scenarios'] for L in ('sysLAmi', 'sysLKan') for v in ('-PS', '-MS', '-T0')):
    out.append('**反証条件 (iii)（JSON）**: %s' % Fc['falsification']['text'])
out.append('「破局ゼロ」「完勝」を書かない（JSON zero_rule）。8 セルを束ねた上限は書かない。'); out.append('')
# ---- 主張規則（検出域の幾何）
out += ['## 主張規則（JSON claim_rule・検出域の幾何）', T['claim_rule'], '', '| 対比型 | 判定可能な断面 | 同じ向きの確証 | 向き | 一般化 |', '|---|---|---|---|---|']
types = collections.defaultdict(list)
for fam, R in FAMRES.items():
    for lab, r in R.items():
        ct = r['ct']; key = (fam, ct['A'].replace(ct['scenario'] + ':', ''), ct['B'])
        # 型＝腕名から名を除いた形（M-a/M-b は名ごと・M-c は L ごと）
        types[(fam, ct['A'], ct['B'])].append((ct['scenario'], r['status'], r['sign']))
for (fam, A, B), lst in sorted(types.items()):
    jd = [s for s, st, sg in lst if st in ('confirmed', 'ns')]; conf = [(s, sg) for s, st, sg in lst if st == 'confirmed']
    signs = {sg for s, sg in conf}
    if conf and len(signs) == 1:
        sg = signs.pop(); scs = {s for s, _ in conf}
        if sg > 0:
            gen = '上向き——本設計では一般化を書かない（N1 以外の対照が天井）'
        else:
            gen = '下向き一般化可（S1・S4・SK で確証）' if {'S1', 'S4', 'SK'} <= scs else 'シナリオ単位でのみ書く（下向きは S1・S4・SK の 3 断面が要る）'
    else:
        gen = 'シナリオ単位でのみ書く' if conf else '—'
    out.append('| %s: %s 対 %s | %d | %d | %s | %s |' % (fam, A, B, len(jd), len(conf), '・'.join('%s%s' % (s, '+' if sg > 0 else '−') for s, sg in conf) or '—', gen))
out.append('一般化が書けなかったことを「効果が無かった」と読まない。上向きの一般化は構造的に書けない（対照が S1/S4/SK で天井）。'); out.append('')
# ---- 複製（第二走行）
if args.tag2:
    RP = T['replication']; out += ['## 複製（第二走行 %s・六札・JSON replication・m は族と同じ）' % args.tag2, '| 対比 | 第一走行 | 第二走行 A/B（率） | p₂ | Holm₂ | 向き₂ | 札 | 注 |', '|---|---|---|---|---|---|---|---|']
    cont2 = continuity_flags(cells2); dr2 = drift_i_flags(cells2)
    # drift (iii): 参照 7 腕の走行間差 10pt
    d3 = {}
    for sc in T['scenarios']:
        cnt = 0
        for a in DR['ref_arms_between_runs']:
            x1 = cells1.get(sc, {}).get(a); x2 = cells2.get(sc, {}).get(a)
            if x1 and x2 and x1['n_ok'] and x2['n_ok'] and abs(x1['catastrophe'] / x1['n_ok'] - x2['catastrophe'] / x2['n_ok']) * 100 >= DR['between_runs_pt'] - 1e-9:
                cnt += 1
        d3[sc] = (cnt >= DR['between_runs_min_cells'], cnt)
    counts = collections.Counter()
    for fam, F in T['families'].items():
        R2 = family_table(fam, F, cells2, style2, gate, second=True)
        for lab, r2 in R2.items():
            st1 = STATUS.get(lab); sc = r2['ct']['scenario']
            x1 = cells1[sc][r2['ct']['arm'] if 'arm' in r2['ct'] else r2['ct']['A']]; nk1 = cells1[sc].get(CT['main_5pt']['arm']); nk2 = cells2[sc].get(CT['main_5pt']['arm'])
            hold2 = r2['status'] in ('hold_refuse', 'hold_style') or cont2.get(sc) or dr2.get(sc, (False,))[0] or d3.get(sc, (False,))[0] or (nk1 and nk2 and abs(nk1['catastrophe'] / nk1['n_ok'] - nk2['catastrophe'] / nk2['n_ok']) * 100 >= CT['second_vs_first_pt'] - 1e-9)
            if st1 in ('hold_refuse', 'hold_style', 'gate'):
                lab6 = '（第一走行で判定保留／不能・札なし）'
            elif st1 == 'confirmed':
                if hold2:
                    lab6 = RP['labels'][3]
                elif r2['status'] == 'confirmed' and r2['sign'] == SIGN[lab]:
                    lab6 = RP['labels'][0]
                elif r2['status'] == 'confirmed' and r2['sign'] == -SIGN[lab]:
                    lab6 = RP['labels'][2]
                else:
                    lab6 = RP['labels'][1]
            else:
                lab6 = RP['labels'][4] if (r2['status'] == 'confirmed' and not hold2) else RP['labels'][5]
            counts[lab6] += 1
            why = ('・'.join(w for w, f in (('refuse/様式', r2['status'] in ('hold_refuse', 'hold_style')), ('連続性 5pt', cont2.get(sc)), ('drift i', dr2.get(sc, (False,))[0]), ('drift iii', d3.get(sc, (False,))[0])) if f)) if hold2 else ''
            out.append('| %s | %s | %d/%d (%.3f) / %d/%d (%.3f) | %s | %s | %s | %s | %s |' % (lab, st1, r2['a'], r2['na'], r2['ra'], r2['b'], r2['nb'], r2['rb'], ('%.2e' % r2['p']) if lab6 == RP['labels'][4] or st1 == 'confirmed' else 'p 非印字', ('%.2e' % r2['adj']) if lab6 == RP['labels'][4] or st1 == 'confirmed' else '—', '+' if r2['sign'] > 0 else '−' if r2['sign'] < 0 else '0', lab6, why or r2['note'] or '—'))
    out.append('札の内訳: ' + '・'.join('%s %d' % kv for kv in counts.items()))
    out.append('drift (iii)（参照 7 腕・走行間 10pt 以上のセル数）: ' + '・'.join('%s %d%s' % (sc, v[1], '（発火）' if v[0] else '') for sc, v in d3.items()))
    out.append('一般化・固有の札・配線は ① のみを数える。併合検定は置かない。第一走行の観測効果量から複製確率を逆算しない。⑤ の一覧に限り p を印字した。'); out.append('')
# ---- 記述族（p 非印字）
for fam, F in T['descriptive_families'].items():
    out += ['## 記述族 %s（検定なし・p 非印字）——%s' % (fam, F['question'])]
    if fam == 'M_desc_drift':
        out += ['| 項目 | シナリオ | 第一走行 A（率） | V′／B（率） | 差 |' + (' 第二走行 A（率） | 走行間差 |' if args.tag2 else ''), '|---|---|---|---|---|' + ('---|---|' if args.tag2 else '')]
        for ct in F['contrasts']:
            sc = ct['scenario']; x = cells1.get(sc, {}).get(ct['A'])
            if not x:
                continue
            ra = x['catastrophe'] / x['n_ok'] if x['n_ok'] else 0
            if ct['type'] == 'vprime_ref':
                rb = ct['vprime_catastrophe'] / ct['vprime_n']; btxt = 'V′ %d/%d (%.3f)' % (ct['vprime_catastrophe'], ct['vprime_n'], rb)
            else:
                y = cells1.get(sc, {}).get(ct['B']); rb = y['catastrophe'] / y['n_ok'] if (y and y['n_ok']) else 0; btxt = '%s %d/%d (%.3f)' % (ct['B'], y['catastrophe'], y['n_ok'], rb) if y else '—'
            row = '| %s | %s | %s %d/%d (%.3f) | %s | %+.3f |' % (ct['type'], sc, ct['A'], x['catastrophe'], x['n_ok'], ra, btxt, ra - rb)
            if args.tag2:
                x2 = cells2.get(sc, {}).get(ct['A']); row += (' %d/%d (%.3f) | %+.3f |' % (x2['catastrophe'], x2['n_ok'], x2['catastrophe'] / x2['n_ok'], x2['catastrophe'] / x2['n_ok'] - ra)) if (x2 and x2['n_ok']) else ' — | — |'
            out.append(row)
        if args.tag2:
            diffs = []
            for sc in T['scenarios']:
                for a in ALL_ARMS:
                    x1 = cells1.get(sc, {}).get(a); x2 = cells2.get(sc, {}).get(a)
                    if x1 and x2 and x1['n_ok'] and x2['n_ok']:
                        diffs.append(abs(x1['catastrophe'] / x1['n_ok'] - x2['catastrophe'] / x2['n_ok']))
            if diffs:
                diffs.sort(); out.append('(iii) 全腕の第一・第二走行の |差|: 中央値 %.3f・最大 %.3f・10pt 以上 %d/%d セル。' % (diffs[len(diffs) // 2], diffs[-1], sum(1 for d in diffs if d >= 0.1 - 1e-9), len(diffs)))
        out.append(''); continue
    out += ['| 対比 | A 破局/n（率・Wilson） | B 破局/n（率・Wilson） | 差 | 向き | Δrefuse | 答えた分母 A/B |' + (' 第二走行 差 |' if args.tag2 else ''), '|---|---|---|---|---|---|---|' + ('---|' if args.tag2 else '')]
    for ct in F['contrasts']:
        v = cell_stats(cells1, ct)
        if v is None:
            continue
        d = v['ra'] - v['rb']; row = '| %s | %d/%d (%.3f %s) | %d/%d (%.3f %s) | %+.3f | %s | %+d | %s / %s |' % (ct['id'], v['a'], v['na'], v['ra'], wilson(v['a'], v['na']), v['b'], v['nb'], v['rb'], wilson(v['b'], v['nb']), d, '+' if d > 0 else '−' if d < 0 else '0', v['dref'], v['ansA'], v['ansB'])
        if args.tag2:
            v2 = cell_stats(cells2, ct); row += (' %+.3f |' % (v2['ra'] - v2['rb'])) if v2 else ' — |'
        out.append(row)
    if fam == 'M_desc_a_nj':
        out.append('NJ と NJ2 が食い違えば文ごとに列挙し「平叙文一般」とは書かない。')
    out.append('')
out.append('価値語の禁止（JSON）: %s' % T['value_word_ban'])
out.append('公開（JSON）: %s' % T['publication'])
out.append('全体の族別誤り率: 三族（m=%s）を各 α=0.05 で独立運転・Boole 上界 0.15。%s' % ('・'.join(str(F['m']) for F in T['families'].values()), T['fwer_note']))
out.append('本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
os.makedirs(os.path.join(REPO, 'records', 'M'), exist_ok=True)
base = os.path.join(REPO, 'records', 'M', 'results-M-%s%s%s' % (args.tag, ('-' + args.tag2) if args.tag2 else '', args.out_suffix)); p = base + '.md'; k = 2
while os.path.exists(p):
    p = '%s-%d.md' % (base, k); k += 1
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n'); print('written', p)
