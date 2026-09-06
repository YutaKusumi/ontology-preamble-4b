# -*- coding: utf-8 -*-
"""analyze_vprime.py v2 —— 追補 V′ の集計器。対比・向き・m・反証条件は `design/contrasts-Vprime.json` だけから読む。
v2（二巡目反映）: Holm の m は JSON の値（対比が欠ければ非零終了）／門の結果は gate_vprime.py の **JSON** から読む（--gate 必須・本走行では省略不可）／
反証条件は JSON の構造化欄（type: abs_ge_onull_base → 同シナリオの Onull 実測基底以上で「耐えた」と書かない）／記述族（descriptive_families）も同じ表形式で出す（検定なし）／出力名固定・上書きなし。
用法: python tools/analyze_vprime.py --tag stageVp --gate records/vprime/gate-pilotVp-<date>.json
"""
import os, sys, json, glob, math, argparse, collections
from scipy.stats import fisher_exact
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='stageVp'); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-Vprime.json')); ap.add_argument('--gate', default=None)
ap.add_argument('--no-gate', action='store_true', help='dry-run 検査用のみ')
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8')); Z = 1.959963985
if not args.gate and not args.no_gate:
    sys.exit('--gate（門の JSON）は必須。dry-run 検査のみ --no-gate。')
gate = json.load(open(args.gate, encoding='utf-8'))['results'] if args.gate else {}


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


cells, rows = {}, {}
for f in glob.glob(os.path.join(REPO, 'results', '*', args.tag + '__*', 'cells.json')):   # 走行ディレクトリは <tag>__… で始まる（dry-run は results/_dryrun/ 配下）
    d = json.load(open(f, encoding='utf-8')); sc = d['manifest']['scenario']; cells[sc] = d['cells']
    tf = glob.glob(os.path.join(os.path.dirname(f), 'trials-*.jsonl')); rows[sc] = [json.loads(l) for l in open(tf[0], encoding='utf-8') if l.strip()] if tf else []
out = ['# 追補 V′ 結果表（機械集計・解釈なし）—— tag %s・contrasts %s・門 %s' % (args.tag, T['version'], os.path.basename(args.gate) if args.gate else '（dry-run 検査・門なし）'), '',
       '確証は全分母・両側 Fisher・族ごと Holm（m は JSON・対比が欠ければ停止）。門で降格した対比は「記述」札（m 不変）。Δrefuse＝A の refuse − B の refuse。答えた分母の率は感度（札を覆さない）。', '']
for sc in T['scenarios']:
    c = cells.get(sc)
    if not c:
        out.append('## %s（未走行）' % sc); continue
    esc = collections.defaultdict(list)
    for r in rows.get(sc, []):
        if r.get('escalation') is not None:
            esc[r['arm']].append(r['escalation'])
    out.append('## %s 三つ組' % sc); out.append('| 腕 | n_ok | 破局 | 率 | Wilson | refuse | 書式外 | 答えた分母 率 | R分類 | esc平均 | 誘因core | 復唱 試行/字数 |'); out.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for a in T['arms']['singles'] + T['arms']['combos']:
        x = c.get(a)
        if not x:
            continue
        e = esc.get(a); out.append('| %s | %d | %s | %s | %s | %d | %d | %s | %s | %s | %s | %s/%s |' % (a, x['n_ok'], x.get('catastrophe'), x.get('catastrophe_rate_all'), wilson(x['catastrophe'], x['n_ok']) if isinstance(x.get('catastrophe'), int) else '—', x['refuse'], x['format_fail'], x.get('catastrophe_rate_answered'),
                                                                                '・'.join('%s %d' % kv for kv in sorted((x.get('refuse_primary') or {}).items())) or '—', ('%.2f (%d)' % (sum(e) / len(e), len(e))) if e else '—', x.get('incentive_core_rate'), x.get('echo_stripped_trials'), x.get('echo_stripped_chars_sum')))
    out.append('')


def table(fam, F, confirmatory):
    items = []
    for ct in F['contrasts']:
        c = cells.get(ct['scenario'], {}); A = c.get(ct['A']); B = c.get(ct['B'])
        if not A or not B:
            if confirmatory:
                sys.exit('対比 %s のセルが欠落——Holm の m と実数が食い違うため停止' % ct['id'])
            continue
        a, na, b, nb = A['catastrophe'], A['n_ok'], B['catastrophe'], B['n_ok']
        items.append((ct['id'], ct, dict(a=a, na=na, b=b, nb=nb, p=fisher_exact([[a, na - a], [b, nb - b]])[1], ra=a / na, rb=b / nb, dref=A['refuse'] - B['refuse'], ansA=A.get('catastrophe_rate_answered'), ansB=B.get('catastrophe_rate_answered'))))
    out.append('## %s %s（%s）——%s' % ('族' if confirmatory else '記述族', fam, ('m=%d・JSON' % F['m']) if confirmatory else '検定なし', F['question']))
    out.append('| 対比 | 向き | A 破局/n（率・Wilson） | B 破局/n（率・Wilson） | 差 | p(両側) | Holm | 判定 | 方向 | Δrefuse | 答えた分母 A/B |'); out.append('|---|---|---|---|---|---|---|---|---|---|---|')
    hp = holm([(lab, v['p']) for lab, ct, v in items], F['m']) if (confirmatory and items) else {}
    for lab, ct, v in items:
        d = v['ra'] - v['rb']; same = (d > 0) if ct['direction'] == 'up' else (d < 0)
        g = gate.get(lab, {}); dg = g.get('status') == 'downgraded'
        if confirmatory:
            adj, rej = hp[lab]; verdict = '記述（門で降格: %s）' % g.get('reason') if dg else (('**確証（有意・想定方向）**' if same else '**有意・方向が想定と逆**') if rej else '確証族・非有意')
            adjs = '%.2e' % adj
        else:
            verdict = '記述'; adjs = '—'
        out.append('| %s | %s | %d/%d (%.3f %s) | %d/%d (%.3f %s) | %+.3f | %.2e | %s | %s | %s | %+d | %s / %s |' % (lab, ct['direction'], v['a'], v['na'], v['ra'], wilson(v['a'], v['na']), v['b'], v['nb'], v['rb'], wilson(v['b'], v['nb']), d, v['p'], adjs, verdict, '想定どおり' if same else ('**想定と逆**' if d != 0 else '差なし'), v['dref'], v['ansA'], v['ansB']))
    fm = F.get('falsification')
    if fm:
        out.append('反証条件（記述札・検定と独立・JSON）: %s' % fm['text'])
        for sc, base in T['scenarios'].items():
            A = cells.get(sc, {}).get(fm['arm'])
            if A:
                r = A['catastrophe'] / A['n_ok']; thr = base['onull_base_main']
                out.append('- %s: %s %d/%d = %.3f 対 Onull 基底 %.3f → %s' % (sc, fm['arm'], A['catastrophe'], A['n_ok'], r, thr, '**「耐えた」と書かない**（Onull 基底以上）' if r >= thr else '閾値未満（ただし V′a の確証があれば単独強調しない）'))
    out.append('')


for fam, F in T['families'].items():
    table(fam, F, True)
for fam, F in T.get('descriptive_families', {}).items():
    table(fam, F, False)
fams = T['families']
out.append('全体の族別誤り率: 確証族 %d 個（各 α=0.05）を独立に運転するため、追補全体の FWER は最大 1−0.95^%d ≈ %.4f。' % (len(fams), len(fams), 1 - 0.95 ** len(fams)))
out.append('本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
os.makedirs(os.path.join(REPO, 'records', 'vprime'), exist_ok=True)
base = os.path.join(REPO, 'records', 'vprime', 'results-Vprime-%s' % args.tag); p = base + '.md'; k = 2
while os.path.exists(p):
    p = '%s-%d.md' % (base, k); k += 1
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n'); print('written', p)
