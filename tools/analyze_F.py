# -*- coding: utf-8 -*-
"""analyze_F.py v1 —— 段階 F の集計器。対比・向き・m・門・添え札の規則・全組合せ表・複製規則・連続性・drift・反証条件は `design/contrasts-F.json` だけから読む。
確証は第一走行（--tag）のみ・両側 Fisher・全分母・族 F の Holm（m=24・降格しても m 不変）。門は gate_F.py の JSON（--gate 必須・dry-run／合成検査のみ --no-gate）。
refuse 門（答えた分母で向き不一致→判定保留）・様式門（(a)(b) の差 >30pt→判定保留・15pt 超は注・様式は records/F/style-<tag>.json＝response_mode_F.py の出力）・
添え札（(c2) の処置腕 対 U・両側 Fisher α=0.05・補正なし・上昇あり／上昇なし／低下／復唱のみ・門と独立の列・走行ごと）・重複札（T2 × S4）・札は全組合せ表（288 行）の当該行から印字・
主張規則（検出域の幾何・添え札の内訳を併記）・反証条件 (i)〔N′ の二項閾値〕(ii)(iii)・複製六札（--tag2）・連続性（U 腕別・M 第一走行から 5 pt＝drift (i)）・drift (iii)（走行間 10 pt・腕別）・撤退条件による降格（gate JSON の demoted）・
言及率の腕別表・言及 × 破局の 2×2・記述族（T2 対 T・p 非印字）を機械判定して印字。出力名固定・上書きなし・同名 .json（組み立て器が読む）。
用法: python tools/analyze_F.py --tag stageF1 --gate records/F/gate-pilotF-<date>.json [--tag2 stageF2]
"""
import os, sys, json, glob, math, argparse, collections
from scipy.stats import fisher_exact, binom
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(REPO, 'tools'))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--tag2', default=None); ap.add_argument('--gate', default=None); ap.add_argument('--no-gate', action='store_true')
ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-F.json')); ap.add_argument('--style', default=None); ap.add_argument('--style2', default=None); ap.add_argument('--out-suffix', default=''); ap.add_argument('--root', default=None, help='cells.json の探索root（既定 results/<tag>・dry-run は results/_dryrun）')
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8')); Z = 1.959963985; n_main = T['n_per_arm']; SCN = list(T['scenarios']); MT = T['mention_tag']; CT = T['continuity']; RP = T['replication']; FAMF = T['families']['F']
if not args.gate and not args.no_gate:
    sys.exit('--gate（門の JSON）は必須。dry-run／合成検査のみ --no-gate。')
GATE = json.load(open(args.gate, encoding='utf-8')) if args.gate else {'results': {}, 'demoted': []}
gate = GATE['results']; DEMOTED = set(GATE.get('demoted') or [])
_ids = [c['id'] for F in list(T['families'].values()) + list(T['descriptive_families'].values()) for c in F['contrasts']]
assert len(_ids) == len(set(_ids)), 'id が全族で一意でない'
ARMS = list(T['arms']['preamble']); BASES = list(T['bases'])
LEDF = json.load(open(os.path.join(REPO, 'arms', 'panelF', 'SHA-LEDGER-F.json'), encoding='utf-8'))['preamble']; LEDV = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8'))
LED_EXPECT = {a: (None if a == 'N' else LEDF.get(a) or LEDV.get(a)) for a in ARMS}
COMBO = {(r['gate'], r['test'], r['refuse'], r['style'], r['tag'], r['dup']): r for r in T['combo_table']['rows']}
BAN = ['耐えた', '頑健', '守った', '完勝', '勝った', '効いた', '防いだ', '防護力', '防御性能', '行儀よくなった']


def load_cells(tag):
    root = args.root or os.path.join(REPO, 'results', tag); C = {}; dirs = []
    for f in glob.glob(os.path.join(root, tag + '__*', 'cells.json')):
        d = json.load(open(f, encoding='utf-8')); C.setdefault(d['manifest']['scenario'], {}).update(d['cells']); dirs.append(os.path.dirname(f))
    return C, dirs


def load_style(tag, path, dirs):
    if path and os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))['runs']
    p = os.path.join(REPO, 'records', 'F', 'style-%s.json' % tag)
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8'))['runs']
    import response_mode_F as RM
    runs = {}
    for d in dirs:
        sc, key, out = RM.analyze_run(d); runs.setdefault(sc, {}).update(out)
    return runs


cells1, dirs1 = load_cells(args.tag); style1 = load_style(args.tag, args.style, dirs1)
cells2, dirs2 = (load_cells(args.tag2) if args.tag2 else ({}, [])); style2 = load_style(args.tag2, args.style2, dirs2) if args.tag2 else {}
J = {'tag': args.tag, 'tag2': args.tag2, 'contrasts_version': T['version'], 'gate': os.path.basename(args.gate) if args.gate else None, 'demoted': sorted(DEMOTED), 'first': {}, 'second': {}, 'replication': {}, 'continuity': {}, 'drift3': {}, 'claims': [], 'falsification': {}, 'mention': {}, 'mass_hold': {}, 'combo_rows_fired': []}


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


def fisher(a, na, b, nb):
    return fisher_exact([[a, na - a], [b, nb - b]])[1]


def meta_of(arm):
    return 'T2' if arm.startswith('T2-') else 'T' if arm.startswith('T-') else 'U'


def base_of(arm):
    return arm[3:] if arm.startswith('T2-') else arm[2:] if arm.startswith('T-') else arm


out = ['# 段階 F 結果表（機械集計・解釈なし）—— 第一走行 tag %s%s・contrasts %s・門 %s' % (args.tag, ('・第二走行 tag %s' % args.tag2) if args.tag2 else '', T['version'], os.path.basename(args.gate) if args.gate else '（検査・門なし）'), '',
       '確証は第一走行のみ・全分母・両側 Fisher・族 F の Holm（m=%d・降格しても m 不変）。門で降格した対比は「判定不能（床／天井）」。撤退条件で降格した対比は「記述へ降格」（p 非印字）。refuse 門・様式門は本走行の数で走行ごとに判定。添え札は (c2) の処置腕 対 U（両側 Fisher α=%.2f・補正なし・門と独立の列・走行ごと）。Δrefuse＝A−B。第二走行は複製六札。' % (FAMF['m'], MT['alpha']), '']
# ---- 整合: 腕の欠落・preamble_sha 台帳突合
for tag, C in ((args.tag, cells1), (args.tag2, cells2)):
    if not tag:
        continue
    miss = {sc: [a for a in ARMS if a not in C.get(sc, {})] for sc in SCN}
    bad = [(sc, a, C[sc][a].get('preamble_sha')) for sc in C for a in C[sc] if a in LED_EXPECT and C[sc][a].get('preamble_sha') != LED_EXPECT[a]]
    out.append('- 整合（%s）: 欠落腕 %s／preamble_sha 台帳突合（panelF・V′ 盤・N は None）不一致 %d 件%s' % (tag, {sc: len(v) for sc, v in miss.items()}, len(bad), ('・' + str(bad[:3])) if bad else ''))
    if bad and not args.no_gate:
        sys.exit('[analyze] preamble_sha が台帳と不一致: %s' % bad[:3])
out.append('')
# ---- 三つ組と様式・言及（走行ごと）
def triplet_tables(tag, C, S, label):
    global out
    for sc in SCN:
        c = C.get(sc)
        if not c:
            out.append('## %s（%s・未走行）' % (sc, label)); continue
        out += ['## %s 三つ組（%s）' % (sc, label), '| 腕 | n_ok | 破局 | 率 | Wilson | refuse | 書式外 | 答えた分母 率 | 様式 (a) 名言及 | 様式 (b) JSON 直答 | 初回 (a)/(b) | (c1) | (c2) | (d1) | (d2) | 復唱のみ | 初回 (c2) |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        for a in ARMS:
            x = c.get(a); s = S.get(sc, {}).get(a, {})
            if not x:
                continue
            out.append('| %s | %d | %s | %s | %s | %d | %d | %s | %s | %s | %s/%s | %s | %s | %s | %s | %s | %s |' % (a, x['n_ok'], x.get('catastrophe'), x.get('catastrophe_rate_all'), wilson(x['catastrophe'], x['n_ok']), x['refuse'], x['format_fail'], x.get('catastrophe_rate_answered'), s.get('a_rate_final', '—'), s.get('b_rate_final', '—'), s.get('a_rate_first', '—'), s.get('b_rate_first', '—'), s.get('c1_final', '—'), s.get('c2_final', '—'), s.get('d1_final', '—'), s.get('d2_final', '—'), s.get('echo_only_final', '—'), s.get('c2_first', '—')))
        out += ['', '### %s 言及 × 破局の 2×2（(c2)・最終試行・件数・%s）' % (sc, label), '| 腕 | 言及あり・破局 | 言及あり・非破局 | 言及なし・破局 | 言及なし・非破局 |', '|---|---|---|---|---|']
        for a in ARMS:
            s = S.get(sc, {}).get(a, {}); q = s.get('two_by_two_c2_final')
            if q:
                out.append('| %s | %d | %d | %d | %d |' % (a, q['mention_catastrophe'], q['mention_no'], q['nomention_catastrophe'], q['nomention_no']))
        out.append('')
triplet_tables(args.tag, cells1, style1, '第一走行')
if args.tag2:
    triplet_tables(args.tag2, cells2, style2, '第二走行')
# ---- 連続性（U 腕別・M 第一走行から 5pt＝drift (i)・main_5pt の整数境界）と drift (iii)（走行間 10pt・腕別）
DR = T['descriptive_families']['F_desc_drift']['constraints']


def continuity_flags(C):
    fl = {}
    for sc in SCN:
        for b in BASES:
            x = C.get(sc, {}).get(b); r = CT['main_5pt'][sc][b]
            if not x:
                continue
            k = x['catastrophe']; fired = (r['fire_if_le'] is not None and k <= r['fire_if_le']) or (r['fire_if_ge'] is not None and k >= r['fire_if_ge'])
            fl[(sc, b)] = (bool(fired), k, x['n_ok'], r)
    return fl


def drift3_flags(C1, C2):
    fl = {}
    for sc in SCN:
        for b in BASES:
            x1 = C1.get(sc, {}).get(b); x2 = C2.get(sc, {}).get(b)
            if x1 and x2 and x1['n_ok'] and x2['n_ok']:
                d = x2['catastrophe'] / x2['n_ok'] - x1['catastrophe'] / x1['n_ok']; fl[(sc, b)] = (abs(d) * 100 >= DR['between_runs_pt'] - 1e-9, d)
    return fl


cont1 = continuity_flags(cells1); cont2 = continuity_flags(cells2) if args.tag2 else {}; d3 = drift3_flags(cells1, cells2) if args.tag2 else {}
out += ['## 連続性条件＝drift (i)（本走行・U 腕別・M 第一走行から 5 pt・転記行 M′・整数境界は JSON main_5pt）と drift (iii)（走行間 10 pt・腕別）', '| 場面 | U 腕 | 既測基底（M1） | 帯（発火 ≤／≥） | 第一走行 破局/n | 発火 |' + (' 第二走行 破局/n | 発火 | 走行間差 | (iii) 発火 |' if args.tag2 else ''), '|---|---|---|---|---|---|' + ('---|---|---|---|' if args.tag2 else '')]
for sc in SCN:
    for b in BASES:
        f1 = cont1.get((sc, b))
        if not f1:
            continue
        r = f1[3]; band = '%s／%s' % (('≤%d' % r['fire_if_le']) if r['fire_if_le'] is not None else '—', ('≥%d' % r['fire_if_ge']) if r['fire_if_ge'] is not None else '—')
        row = '| %s | %s | %.4f | %s | %d/%d | %s |' % (sc, b, r['base'], band, f1[1], f1[2], '**発火**' if f1[0] else '—')
        J['continuity']['%s:%s' % (sc, b)] = {'fired_first': f1[0], 'k_first': f1[1], 'n_first': f1[2], 'base_M1': r['base']}
        if args.tag2:
            f2 = cont2.get((sc, b)); dd = d3.get((sc, b))
            row += (' %d/%d | %s | %+.3f | %s |' % (f2[1], f2[2], '**発火**' if f2[0] else '—', dd[1], '**発火**' if dd[0] else '—')) if (f2 and dd) else ' — | — | — | — |'
            if f2:
                J['continuity']['%s:%s' % (sc, b)].update({'fired_second': f2[0], 'k_second': f2[1], 'n_second': f2[2]})
            if dd:
                J['drift3']['%s:%s' % (sc, b)] = {'fired': dd[0], 'diff': dd[1]}
        out.append(row)
out.append('発火した土台 × 場面の確証札には「参照腕が M から乖離」の注を付し一般化・複製に数えない（JSON F_desc_drift.constraints）。(iii) 発火は当該土台 × 場面の複製の可否を書かず両走行の数を並べる（札 ④）。'); out.append('')
# ---- 対比の統計
SG = T['style_gate']


def cell_stats(C, ct):
    A = C.get(ct['scenario'], {}).get(ct['A']); B = C.get(ct['scenario'], {}).get(ct['B'])
    if not A or not B or not A['n_ok'] or not B['n_ok']:
        return None
    a, na, b, nb = A['catastrophe'], A['n_ok'], B['catastrophe'], B['n_ok']
    return dict(a=a, na=na, b=b, nb=nb, ra=a / na, rb=b / nb, p=fisher(a, na, b, nb), dref=A['refuse'] - B['refuse'], ansA=A.get('catastrophe_rate_answered'), ansB=B.get('catastrophe_rate_answered'))


def style_check(S, ct):
    sa = S.get(ct['scenario'], {}).get(ct['A']); sb = S.get(ct['scenario'], {}).get(ct['B'])
    if not sa or not sb:
        return None, None, None
    da = abs((sa.get('a_rate_final') or 0) - (sb.get('a_rate_final') or 0)); db = abs((sa.get('b_rate_final') or 0) - (sb.get('b_rate_final') or 0)) if (sa.get('b_rate_final') is not None and sb.get('b_rate_final') is not None) else 0
    mx = max(da, db); nA = sa.get('n_ok') or 0
    susp = (mx * nA) > SG['strict_greater_trials'] * nA / n_main if nA else False   # 「超」＝観測差の件数が strict_greater_trials（n=400 で 120）を厳密に上回る
    note = (mx * 100 > SG['note_pt']) and not susp
    strat = []
    for key in ('json_direct', 'prose'):
        xa = (sa.get('strata_final') or {}).get(key); xb = (sb.get('strata_final') or {}).get(key)
        if xa and xb and xa['n'] >= SG['min_stratum_n'] and xb['n'] >= SG['min_stratum_n']:
            strat.append((key, xa['n'], xb['n'], xa['catastrophe'] / xa['n'] - xb['catastrophe'] / xb['n']))
    return (mx, susp, note), strat, (da, db)


def mention_tag(S, ct, key='c2', alt='c1'):
    """添え札: key（c2）の処置腕 対 U を両側 Fisher（α・補正なし）。alt（c1）で有意に高く key で有意でなければ「復唱のみ」。"""
    sa = S.get(ct['scenario'], {}).get(ct['A']); sb = S.get(ct['scenario'], {}).get(ct['B'])
    if not sa or not sb or not sa.get('n_ok') or not sb.get('n_ok') or sa.get(key + '_final') is None:
        return None
    ka, na, kb, nb = sa[key + '_final'], sa['n_ok'], sb[key + '_final'], sb['n_ok']; p2 = fisher(ka, na, kb, nb); sig2 = p2 <= MT['alpha']; d2 = ka / na - kb / nb
    ka1, kb1 = sa.get(alt + '_final', 0), sb.get(alt + '_final', 0); p1 = fisher(ka1, na, kb1, nb); sig1 = p1 <= MT['alpha'] and (ka1 / na > kb1 / nb)
    if sig2 and d2 > 0:
        lab = MT['labels'][0]
    elif sig2 and d2 < 0:
        lab = MT['labels'][2]
    elif sig1:
        lab = MT['labels'][3]
    else:
        lab = MT['labels'][1]
    rb = kb / nb; struct = ('上昇は構造的に検出不能（U 基底 %.3f）' % rb) if rb > 0.99 else ('低下は構造的に検出不能（U 基底 %.3f）' % rb) if rb < 0.01 else ''
    return dict(label=lab, ka=ka, na=na, kb=kb, nb=nb, p=p2, p_alt=p1, d=d2, struct=struct, echo_only_A=sa.get('echo_only_final'))


def gate_axis(lab):
    g = gate.get(lab, {}); st = g.get('status', 'go' if args.no_gate else 'not_run')
    return 'floor' if st == 'downgraded_floor' else 'ceiling' if st == 'downgraded_ceiling' else 'go'


def family_table(C, S, second=False):
    items = []
    for ct in FAMF['contrasts']:
        v = cell_stats(C, ct)
        if v is None:
            if not args.no_gate:
                sys.exit('対比 %s のセルが欠落——Holm の m と実数が食い違うため停止' % ct['id'])
            continue
        items.append((ct['id'], ct, v))
    hp = holm([(lab, v['p']) for lab, ct, v in items], FAMF['m']) if items else {}
    res = {}
    for lab, ct, v in items:
        adj, rej = hp[lab]; d = v['ra'] - v['rb']; sign = 1 if d > 0 else -1 if d < 0 else 0
        demoted = ('%s:%s' % (ct['scenario'], ct['B'])) in DEMOTED; ga = gate_axis(lab); dg = ga != 'go'
        sty, strat, dab = style_check(S, ct)
        st = 'demoted' if demoted else 'gate' if dg else ('confirmed' if rej else 'ns'); why = []; refuse_ax = 'ok'; style_ax = 'ok'
        if st == 'confirmed':
            aA, aB = v['ansA'], v['ansB']
            if not (aA is not None and aB is not None and ((aA > aB) if sign > 0 else (aA < aB))):
                refuse_ax = 'hold'; why.append('答えた分母 %s 対 %s' % (aA, aB))
            if sty and sty[1]:
                style_ax = 'hold'; why.append('様式差 %.0f pt' % (sty[0] * 100))
            elif sty and sty[2]:
                style_ax = 'note'
            if refuse_ax == 'hold':
                st = 'hold_refuse'
            elif style_ax == 'hold':
                st = 'hold_style'
        elif st == 'ns' and sty and sty[2]:
            style_ax = 'note'
        tag = mention_tag(S, ct); tagd = mention_tag(S, ct, 'd2', 'd1') if meta_of(ct['A']) == 'T2' else None
        row = None
        if st != 'demoted' and tag:
            key = (ga, 'confirmed' if st in ('confirmed', 'hold_refuse', 'hold_style') else 'ns', refuse_ax, style_ax, tag['label'], 'yes' if ct.get('duplicate') else 'no')
            row = COMBO.get(key)
            if row is None or not row['feasible']:
                sys.exit('[analyze] 全組合せ表に無い／発火不能の行に落ちた: %s %s' % (lab, key))
            if not second:
                J['combo_rows_fired'].append(list(key))
        note = ''
        if sty and sty[2] and st != 'gate':
            note += '様式差あり（%.0f pt）' % (sty[0] * 100)
        if sty and sty[1] and st == 'ns':
            note += '・様式差 %.0f pt（非有意のため保留は適用せず）' % (sty[0] * 100)
        cf = (cont2 if second else cont1).get((ct['scenario'], ct['B']))
        if cf and cf[0] and st in ('confirmed', 'ns'):
            note += '・参照腕が M から乖離（連続性＝drift i）'
        res[lab] = dict(v, adj=adj, status=st, sign=sign, why='・'.join(why), note=note.strip('・'), strat=strat, style=sty, dab=dab, ct=ct, gate_axis=ga, refuse_axis=refuse_ax, style_axis=style_ax, tag=tag, tagd=tagd, row=row, dup=bool(ct.get('duplicate')), ref_drift=bool(cf and cf[0]))
    return res


def status_label(r):
    if r['status'] == 'demoted':
        return '**記述へ降格（撤退条件・p 非印字）**'
    if r['status'] == 'gate':
        return '判定不能（門: %s）' % gate.get(r['ct']['id'], {}).get('reason', '')
    row = r['row']; s = ('**%s**' % row['primary']) if r['status'] != 'ns' else row['primary']
    if row.get('flags'):
        s += '〔' + '・'.join(row['flags']) + '〕'
    return s


R1 = family_table(cells1, style1); STATUS = {lab: r['status'] for lab, r in R1.items()}; SIGN = {lab: r['sign'] for lab, r in R1.items()}; CONF = {lab: r['status'] == 'confirmed' for lab, r in R1.items()}
out += ['## 族 F（m=%d・第一走行）——%s' % (FAMF['m'], FAMF['question']), '| 対比 | A 破局/n（率・Wilson） | B 破局/n（率・Wilson） | 差 | p(両側) | Holm | 判定（全組合せ表の当該行） | 向き | 添え札（(c2) A/U・p） | 重複 | Δrefuse | 答えた分母 A/B | 様式差 (a)/(b) | 層別（層・nA・nB・差） | 注 |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for lab, r in R1.items():
    st = status_label(r) + (('（%s）' % r['why']) if r['why'] else '')
    strat = '・'.join('%s %d/%d %+.3f' % (k, na, nb, d) for k, na, nb, d in (r['strat'] or [])) or ('層別不能' if r['style'] else '—')
    tg = r['tag']; tgs = ('%s（%d/%d 対 %d/%d・p %.3f）%s' % (tg['label'], tg['ka'], tg['na'], tg['kb'], tg['nb'], tg['p'], ('・' + tg['struct']) if tg['struct'] else '')) if tg else '—'
    pp = ('%.2e' % r['p'], '%.2e' % r['adj']) if r['status'] != 'demoted' else ('p 非印字', '—')
    out.append('| %s | %d/%d (%.3f %s) | %d/%d (%.3f %s) | %+.3f | %s | %s | %s | %s | %s | %s | %+d | %s / %s | %s | %s | %s |' % (lab, r['a'], r['na'], r['ra'], wilson(r['a'], r['na']), r['b'], r['nb'], r['rb'], wilson(r['b'], r['nb']), r['ra'] - r['rb'], pp[0], pp[1], st, '+' if r['sign'] > 0 else '−' if r['sign'] < 0 else '0', tgs, '重複（付記と場面文）' if r['dup'] else '—', r['dref'], r['ansA'], r['ansB'], ('%.2f/%.2f' % r['dab']) if r['dab'] else '—', strat, r['note'] or '—'))
    J['first'][lab] = {k: r[k] for k in ('a', 'na', 'b', 'nb', 'ra', 'rb', 'p', 'adj', 'status', 'sign', 'why', 'note', 'dref', 'ansA', 'ansB', 'gate_axis', 'refuse_axis', 'style_axis', 'dup', 'ref_drift')}
    J['first'][lab].update({'tag': r['tag'], 'tagd': r['tagd'], 'primary': r['row']['primary'] if r['row'] else None, 'flags': r['row']['flags'] if r['row'] else None, 'strat': r['strat'], 'style_diff': r['style'][0] if r['style'] else None, 'scenario': r['ct']['scenario'], 'A': r['ct']['A'], 'B': r['ct']['B']})
# 一斉保留（場面ごと）
for sc in SCN:
    nh = sum(1 for r in R1.values() if r['ct']['scenario'] == sc and r['status'] == 'hold_style'); nj = sum(1 for r in R1.values() if r['ct']['scenario'] == sc and r['status'] not in ('gate', 'demoted'))
    J['mass_hold'][sc] = {'hold_style': nh, 'judgeable': nj, 'mass': bool(nj and nh / nj > 0.5)}
    if nj and nh / nj > 0.5:
        out.append('**第一の所見（機械札・%s）**: 判定可能な %d 本のうち %d 本が様式門で保留——「破局率の差は応答様式の転換と分離できなかった」。様式率の表を主結果として報告する（JSON style_gate）。' % (sc, nj, nh))
out.append('添え札は確証札・非有意札を置換せず独立の列（JSON mention_tag.label_rule）。「復唱のみ」＝(c1) で有意に高く (c2) で有意でない。上昇と低下の構造的検出不能の境界は U 基底 0.99／0.01（転記行 N′）。'); out.append('')
# ---- T2 腕の (d2) 添え札（記述・印字のみ）
out += ['## (d) 帰結の言及（T2 腕・(d2) 主指標・記述・添え札と同じ規則で印字するが札ではない）', '| 対比 | (d2) A/U | p | 向き | (d1) A/U |', '|---|---|---|---|---|']
for lab, r in R1.items():
    td = r['tagd']
    if td:
        sa = style1.get(r['ct']['scenario'], {}).get(r['ct']['A'], {}); sb = style1.get(r['ct']['scenario'], {}).get(r['ct']['B'], {})
        out.append('| %s | %d/%d 対 %d/%d | %.3f | %s | %s/%s 対 %s/%s |' % (lab, td['ka'], td['na'], td['kb'], td['nb'], td['p'], td['label'], sa.get('d1_final', '—'), sa.get('n_ok', '—'), sb.get('d1_final', '—'), sb.get('n_ok', '—')))
out.append('')
# ---- 主張規則（検出域の幾何）と添え札の内訳
out += ['## 主張規則（JSON claim_rule・検出域の幾何・添え札の内訳を併記）', T['claim_rule'], '', '| 対比型 | 土台 | 判定可能な断面 | 同じ向きの確証（場面・向き） | 場面横断の一般化 | 添え札の内訳（確証した断面） |', '|---|---|---|---|---|---|']
DUP_IDS = set(FAMF['duplicate_rule']['ids'])
for mk in ('T', 'T2'):
    for b in BASES:
        rows = [r for r in R1.values() if meta_of(r['ct']['A']) == mk and base_of(r['ct']['A']) == b]
        jd = [r for r in rows if r['status'] in ('confirmed', 'ns')]; conf_all = [r for r in rows if r['status'] == 'confirmed']; conf = [r for r in conf_all if not r['ref_drift']]
        conf_cnt = [r for r in conf if not (mk == 'T2' and r['ct']['id'] in DUP_IDS)]
        signs = {r['sign'] for r in conf_cnt}; tags = collections.Counter(r['tag']['label'] for r in conf_all if r['tag'])
        if conf_cnt and len(signs) == 1 and len(conf_cnt) >= 3:
            gen = '場面横断一般化可（%s・%d 場面・%s）' % ('上向き' if conf_cnt[0]['sign'] > 0 else '下向き', len(conf_cnt), '様式門を通った断面に限る条件つき')
        elif conf:
            gen = '場面単位でのみ書く（同じ向きの確証 %d・要 3）' % (len(conf_cnt) if len(signs) <= 1 else 0)
        else:
            gen = '—'
        J['claims'].append({'type': mk, 'base': b, 'judgeable': len(jd), 'confirmed_same_sign': len(conf_cnt) if len(signs) <= 1 else 0, 'generalization': gen, 'tags': dict(tags)})
        out.append('| %s 対 U | %s | %d | %s | %s | %s |' % (mk, b, len(jd), '・'.join('%s%s%s%s' % (r['ct']['scenario'], '+' if r['sign'] > 0 else '−', '（重複・不算入）' if (mk == 'T2' and r['ct']['id'] in DUP_IDS) else '', '（参照腕乖離・不算入）' if r['ref_drift'] else '') for r in conf_all) or '—', gen, '・'.join('%s %d' % kv for kv in tags.items()) or '—'))
out += ['', '| 対比型 | 場面 | 判定可能な土台 | 同じ向きの確証（土台・向き） | 土台横断の一般化 |', '|---|---|---|---|---|']
for mk in ('T', 'T2'):
    for sc in SCN:
        rows = [r for r in R1.values() if meta_of(r['ct']['A']) == mk and r['ct']['scenario'] == sc]
        jd = [r for r in rows if r['status'] in ('confirmed', 'ns')]; conf_all = [r for r in rows if r['status'] == 'confirmed']; conf = [r for r in conf_all if not r['ref_drift']]; signs = {r['sign'] for r in conf}
        if conf and len(signs) == 1 and len(conf) >= 3:
            gen = '上向き——本設計では土台横断一般化を書かない（JSON claim_rule）' if conf[0]['sign'] > 0 else '土台横断一般化可（下向き・3 土台）'
        else:
            gen = '場面単位でのみ書く' if conf_all else '—'
        out.append('| %s 対 U | %s | %d | %s | %s |' % (mk, sc, len(jd), '・'.join('%s%s%s' % (base_of(r['ct']['A']), '+' if r['sign'] > 0 else '−', '（参照腕乖離・不算入）' if r['ref_drift'] else '') for r in conf_all) or '—', gen))
out.append('一般化が書けなかったことを「効果が無かった」と読まない。T と T2 を跨いで数えない。T2 の場面横断は T2 × S4（重複）を数えない。参照腕が M から乖離した断面は数えない。'); out.append('')
# ---- 反証条件
FZ = FAMF['falsification']; judged = [r for r in R1.values() if r['status'] not in ('gate', 'demoted')]; k_up = sum(1 for r in judged if r['tag'] and r['tag']['label'] == MT['labels'][0]); mprime = len(judged)
p0 = MT['null_rate_per_contrast_nominal']; thr = next(t for t in range(mprime + 1) if binom.sf(t, mprime, p0) <= 0.05) if mprime else 0
J['falsification'] = {'m_prime': mprime, 'k_up': k_up, 'threshold': thr, 'null_rate': p0, 'i_fires': bool(mprime and k_up <= thr), 'ii_fires': not any(CONF.values())}
out += ['## 反証条件（JSON falsification・先置）', '- (i) 判定された対比 m′=%d のうち添え札「上昇あり」（復唱のみを除く）k=%d。帰無（対比あたり %.2f・二項）の上側 5%% の閾値 k≤%d。%s' % (mprime, k_up, p0, thr, ('**発火**: ' + FZ['i']['text']) if J['falsification']['i_fires'] else '発火せず（k が閾値を超えた）'),
        '- (ii) T 対 U・T2 対 U の確証 %d 本。%s' % (sum(CONF.values()), ('**発火**: ' + FZ['ii']['text']) if J['falsification']['ii_fires'] else '発火せず'),
        '- (iii) %s' % FZ['iii']['text']]
for sc in SCN:
    for b in BASES:
        r2 = R1.get('%s:T2-%s~%s' % (sc, b, b)); r1 = R1.get('%s:T-%s~%s' % (sc, b, b))
        if r2 and r1 and r2['status'] == 'confirmed' and r1['status'] != 'confirmed':
            out.append('  - 該当断面 %s × %s: T2 対 U 確証・T 対 U %s——「場面の出来事が起こらないと告げたことが効いた」とは書かない。' % (sc, b, r1['status']))
out.append('')
# ---- 複製
if args.tag2:
    R2 = family_table(cells2, style2, second=True); counts = collections.Counter()
    out += ['## 複製（第二走行 %s・六札・JSON replication・m は族と同じ）' % args.tag2, '| 対比 | 第一走行 | 第二走行 A/B（率） | p₂ | Holm₂ | 向き₂ | 札 | 添え札 第一／第二 | 注 |', '|---|---|---|---|---|---|---|---|---|']
    for lab, r2 in R2.items():
        st1 = STATUS.get(lab); sc = r2['ct']['scenario']; b = r2['ct']['B']
        hold2 = r2['status'] in ('hold_refuse', 'hold_style') or (cont1.get((sc, b)) or (False,))[0] or (cont2.get((sc, b)) or (False,))[0] or (d3.get((sc, b)) or (False,))[0]   # 参照腕乖離はいずれの走行でも ④ の引き金（§2.5 (i)「複製に数えない」）
        if st1 in ('hold_refuse', 'hold_style', 'gate', 'demoted'):
            lab6 = '（第一走行で判定保留／不能／降格・札なし）'
        elif st1 == 'confirmed':
            lab6 = RP['labels'][3] if hold2 else RP['labels'][0] if (r2['status'] == 'confirmed' and r2['sign'] == SIGN[lab]) else RP['labels'][2] if (r2['status'] == 'confirmed' and r2['sign'] == -SIGN[lab]) else RP['labels'][1]
        else:
            lab6 = RP['labels'][4] if (r2['status'] == 'confirmed' and not hold2) else RP['labels'][5]
        counts[lab6] += 1
        why = ('・'.join(w for w, f in (('refuse/様式', r2['status'] in ('hold_refuse', 'hold_style')), ('参照腕乖離（第一走行）', (cont1.get((sc, b)) or (False,))[0]), ('参照腕乖離（第二走行）', (cont2.get((sc, b)) or (False,))[0]), ('drift iii', (d3.get((sc, b)) or (False,))[0])) if f)) if hold2 else ''
        t1 = (R1[lab]['tag'] or {}).get('label', '—'); t2 = (r2['tag'] or {}).get('label', '—'); tags = t1 if t1 == t2 else '%s／%s（食い違い・両方印字）' % (t1, t2)
        show_p = (lab6 == RP['labels'][4])
        out.append('| %s | %s | %d/%d (%.3f) / %d/%d (%.3f) | %s | %s | %s | %s | %s | %s |' % (lab, st1, r2['a'], r2['na'], r2['ra'], r2['b'], r2['nb'], r2['rb'], ('%.2e' % r2['p']) if show_p else 'p 非印字', ('%.2e' % r2['adj']) if show_p else '—', '+' if r2['sign'] > 0 else '−' if r2['sign'] < 0 else '0', lab6, tags, why or r2['note'] or '—'))
        J['second'][lab] = {k: r2[k] for k in ('a', 'na', 'b', 'nb', 'ra', 'rb', 'status', 'sign')}; J['second'][lab].update({'tag': r2['tag'], 'p_shown': show_p, 'p': r2['p'] if show_p else None})
        J['replication'][lab] = {'label': lab6, 'hold2_why': why, 'tag_first': t1, 'tag_second': t2}
    out.append('札の内訳: ' + '・'.join('%s %d' % kv for kv in counts.items()))
    out.append('一般化は ① のみを数える。併合検定は置かない。第一走行の観測効果量から複製確率を逆算しない。⑤ の一覧に限り p を印字した（D-22 の教訓・①② の行にも印字しない）。添え札は ④ の引き金に入れない。参照腕が M から乖離した土台 × 場面（いずれの走行でも）は ④。'); out.append('')
# ---- 記述族
for fam, F in T['descriptive_families'].items():
    out += ['## 記述族 %s（検定なし・p 非印字）——%s' % (fam, F['question'])]
    if fam == 'F_desc_drift':
        out += ['| 場面 | U 腕 | 第一走行 破局/n（率） | M 第一走行（率） | 差 | V′（率） | 差 |' + (' 第二走行（率） | 走行間差 |' if args.tag2 else ''), '|---|---|---|---|---|---|---|' + ('---|---|' if args.tag2 else '')]
        for ct in F['contrasts']:
            sc = ct['scenario']; x = cells1.get(sc, {}).get(ct['A'])
            if not x or not x['n_ok']:
                continue
            ra = x['catastrophe'] / x['n_ok']; rm = ct['m1_catastrophe'] / ct['m1_n']; rv = ct['vprime_catastrophe'] / ct['vprime_n']
            row = '| %s | %s | %d/%d (%.3f) | %d/%d (%.3f) | %+.3f | %d/%d (%.3f) | %+.3f |' % (sc, ct['A'], x['catastrophe'], x['n_ok'], ra, ct['m1_catastrophe'], ct['m1_n'], rm, ra - rm, ct['vprime_catastrophe'], ct['vprime_n'], rv, ra - rv)
            if args.tag2:
                x2 = cells2.get(sc, {}).get(ct['A']); row += (' %d/%d (%.3f) | %+.3f |' % (x2['catastrophe'], x2['n_ok'], x2['catastrophe'] / x2['n_ok'], x2['catastrophe'] / x2['n_ok'] - ra)) if (x2 and x2['n_ok']) else ' — | — |'
            out.append(row)
        if args.tag2:
            diffs = []
            for sc in SCN:
                for a in ARMS:
                    x1 = cells1.get(sc, {}).get(a); x2 = cells2.get(sc, {}).get(a)
                    if x1 and x2 and x1['n_ok'] and x2['n_ok']:
                        diffs.append(abs(x1['catastrophe'] / x1['n_ok'] - x2['catastrophe'] / x2['n_ok']))
            if diffs:
                diffs.sort(); out.append('(iii) 全 9 腕の第一・第二走行の |差|: 中央値 %.3f・最大 %.3f・10pt 以上 %d/%d セル。' % (diffs[len(diffs) // 2], diffs[-1], sum(1 for d in diffs if d >= 0.1 - 1e-9), len(diffs)))
        out.append(''); continue
    out += ['| 対比 | A 破局/n（率・Wilson） | B 破局/n（率・Wilson） | 差 | 向き | Δrefuse | (c2) A/B | (d2) A/B |' + (' 第二走行 差 |' if args.tag2 else ''), '|---|---|---|---|---|---|---|---|' + ('---|' if args.tag2 else '')]
    for ct in F['contrasts']:
        v = cell_stats(cells1, ct)
        if v is None:
            continue
        sa = style1.get(ct['scenario'], {}).get(ct['A'], {}); sb = style1.get(ct['scenario'], {}).get(ct['B'], {})
        d = v['ra'] - v['rb']; row = '| %s | %d/%d (%.3f %s) | %d/%d (%.3f %s) | %+.3f | %s | %+d | %s/%s | %s/%s |' % (ct['id'], v['a'], v['na'], v['ra'], wilson(v['a'], v['na']), v['b'], v['nb'], v['rb'], wilson(v['b'], v['nb']), d, '+' if d > 0 else '−' if d < 0 else '0', v['dref'], sa.get('c2_final', '—'), sb.get('c2_final', '—'), sa.get('d2_final', '—'), sb.get('d2_final', '—'))
        if args.tag2:
            v2 = cell_stats(cells2, ct); row += (' %+.3f |' % (v2['ra'] - v2['rb'])) if v2 else ' — |'
        out.append(row)
    out.append('T2 対 T は記述。付記自身の語彙数（T 1 語・T2 2 語）の差を注記する。「場面の出来事が起こらないと告げたことが効いた」とは書かない（反証条件 (iii)）。'); out.append('')
out.append('価値語の禁止（JSON）: %s' % T['value_word_ban'])
out.append('公開（JSON）: %s' % T['publication'])
out.append('全体の族別誤り率: 一族（m=%d）を α=0.05 で運転・Boole 上界 0.05。%s' % (FAMF['m'], T['fwer_note']))
out.append('本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
bad = [w for w in BAN if any(w in l for l in out if not (l.startswith('価値語の禁止') or '書かない' in l))]   # 規則の引用行（「…とは書かない」）は走査から除く
assert not bad, '集計器の出力に価値語: %s' % bad
os.makedirs(os.path.join(REPO, 'records', 'F'), exist_ok=True)
base = os.path.join(REPO, 'records', 'F', 'results-F-%s%s%s' % (args.tag, ('-' + args.tag2) if args.tag2 else '', args.out_suffix)); p = base; k = 2
while os.path.exists(p + '.md') or os.path.exists(p + '.json'):
    p = '%s-%d' % (base, k); k += 1
open(p + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
json.dump(J, open(p + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=float); print('written', p + '.md', p + '.json')
