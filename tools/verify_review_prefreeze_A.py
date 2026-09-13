# -*- coding: utf-8 -*-
"""verify_review_prefreeze_A.py v1 —— 段階 A 草案6（凍結候補 1）の凍結前検分・七票の追い問い 第一部（コーディネータ・2026-09-13）。
七票（系統外 Gemini 3.8 Flash × 2・Grok 4.6 × 2／系統内 claude.ai の Claude Opus 5 × 3）の主張を、一次記録（正本・格子 JSON・設計事実 JSON・草案6・雛形・器材のソース・cost-facts）と厳密計算で出し直す。
シミュレーションは第二部（tools/verify_review_prefreeze_A_2.py）。事前登録は records/reviews/A/prefreeze/preregistration-verification-prefreeze-A.md（作成時刻と SHA-256 は verify.log の先頭）。
出力: records/reviews/A/prefreeze/verification-prefreeze-A.md（W1〜W26）。--work は lint の改変文書を置く作業場所。
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, math, ast, hashlib, datetime, subprocess, tempfile, statistics, argparse
from fractions import Fraction
import numpy as np
from scipy.stats import binom, norm, t as tdist
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firth
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--work', default=None); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'reviews', 'A', 'prefreeze', 'verification-prefreeze-A.md'))
a = ap.parse_args()
WORK = a.work or tempfile.mkdtemp(prefix='pf1-'); os.makedirs(WORK, exist_ok=True)
J = lambda *p: json.load(open(os.path.join(REPO, *p), encoding='utf-8'))
TX = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
SHA = lambda rel: hashlib.sha256(open(os.path.join(REPO, rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
T = J('design', 'contrasts-A.json'); PG = J('records', 'A', 'power-grid-A.json'); HF = J('records', 'A', 'hf-models-A.json'); DF = J('records', 'A', 'design-facts-A.json')['facts']
DRAFT = TX('design', 'design-stageA-draft6.md'); TPL = TX('records', 'A', 'results-report-template-A.md'); CF = TX('records', 'cost-pilot', 'cost-facts-2026-09-13.md')
FAM = T['families']['A_slope']; CRULE = FAM['confirm_rule']; n = T['n_per_arm']; pn = T['pilot_n']; nid = T['identity_n']; ALPHA = FAM['alpha']; M = FAM['m']
SC = T['scenarios']; ARMS = T['arms']['preamble']; SIZES = T['sizes']; CONTR = FAM['contrasts']
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
O = ['# 凍結前検分・七票の追い問い 第一部——コーディネータの独立計算（機械生成・`tools/verify_review_prefreeze_A.py` v1・%s UTC）' % now, '',
     '- 入力の SHA16: 正本 %s・格子 JSON %s・設計事実 JSON %s・草案6 %s・雛形 %s・cost-facts %s・hf-models %s。' % (SHA('design/contrasts-A.json'), SHA('records/A/power-grid-A.json'), SHA('records/A/design-facts-A.json'), SHA('design/design-stageA-draft6.md'), SHA('records/A/results-report-template-A.md'), SHA('records/cost-pilot/cost-facts-2026-09-13.md'), SHA('records/A/hf-models-A.json')),
     '- 事前登録: `preregistration-verification-prefreeze-A.md`（判定の規則と予想・作成時刻と SHA-256 は `verify.log` の先頭）。第二部（シミュレーション）は `verification-prefreeze-A-2.md`。',
     '- 票の略: Ge1・Ge2＝Gemini 3.8 Flash 一人目・二人目／Gr1・Gr2＝Grok 4.6 一人目・二人目／Cl1・Cl2・Cl3＝claude.ai の Claude Opus 5 一人目〜三人目（Cl2 は別添の詳細票）。', '']
P = O.append


def say(msg):
    print('[verify-pf1]', msg, flush=True)


def fn_src(rel, name):
    src = TX(*rel.split('/')); tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(src, node)
    raise KeyError((rel, name))


def md_table(md, head):
    L = md.split('\n'); i = next(k for k, l in enumerate(L) if l.startswith(head)); j = next(k for k in range(i, len(L)) if L[k].startswith('| tag'))
    hdr = [c.strip() for c in L[j].strip('|').split('|')]; rows = []
    for l in L[j + 2:]:
        if not l.startswith('|'):
            break
        rows.append([c.strip() for c in l.strip('|').split('|')])
    return hdr, rows


Gp = {'math': math}; exec(fn_src('tools/power_grid_A.py', 'params'), Gp)
PAR = {k: Gp['params'](v) for k, v in HF['models'].items()}; Z = {k: math.log(PAR[k] / PAR['4B']) for k in PAR}; zs = np.array([Z[s] for s in SIZES])
Gd = {'np': np, 'binom': binom}; exec(fn_src('tools/power_grid_A.py', 'pmf'), Gd); exec(fn_src('tools/power_grid_A.py', 'diff_tail'), Gd); diff_tail = Gd['diff_tail']
KLO = math.ceil(Fraction(str(T['censor']['low'])) * n) - 1; KHI = math.floor(Fraction(str(T['censor']['high'])) * n) + 1

# ---------------- W1
say('W1')
LP = CRULE['label_precedence']
P('## W1. 札の優先順（`label_precedence`）: 列・注・第一適合で読んだときの札（Ge1 重大1・Gr1 重大2・Gr2 重大2・Cl1 重2・Cl3 軽微19）'); P('')
P('- 正本 `families.A_slope.confirm_rule.label_precedence`: %s' % ' → '.join(LP))
P('- `precedence_note`: 「%s」' % CRULE['precedence_note'])
P('- 草案6 §2.4 の文: 「β₃ が Holm で棄却されない対比は「非有意」（判定不能を除く）」の句 %s・「棄却された対比には、判定不能 → 記述（解釈条項）」の句 %s。' % ('あり' if '（判定不能を除く）' in DRAFT else 'なし', 'あり' if '棄却された対比には、判定不能 → 記述（解釈条項）' in DRAFT else 'なし'))
P('- `families.A_slope` の直下に `label_precedence` のキーは%s（Cl3 軽微19 の「null」はキーが無いことを読んだ値）。`style_gate.applies_to`＝`%s`・`refuse_gate.applies_to`＝`%s`。' % ('ある' if 'label_precedence' in FAM else '無い', T['style_gate']['applies_to'], FAM['refuse_gate']['applies_to']))


def applies(lab, s):
    if lab == '非有意':
        return not s['rej']
    if lab.startswith('判定不能'):
        return s['kept'] < 3
    if lab == '記述（解釈条項）':
        return s['rej'] and s['sat2']
    if lab == '記述（対数オッズ尺度でのみ）':
        return s['rej'] and not s['pt']
    if lab == '判定保留（refuse 転位）':
        return s['refuse']
    if lab == '判定保留（様式転位）':
        return s['style']
    if lab == '判定保留（環境）':
        return s['env']
    if lab == '確証':
        return s['rej'] and s['pt']
    raise KeyError(lab)


first = lambda s: next(l for l in LP if applies(l, s))
CASES = [('残存規模 2（β₃ を計算しない＝棄却されない）', dict(kept=2, rej=False, sat2=False, pt=False, refuse=False, style=False, env=False), '§2.4 と注が定める札は「判定不能（検閲・門2）」'),
         ('Holm で棄却・条項なし・pt 差の傾きが立たない・refuse 門が保留', dict(kept=6, rej=True, sat2=False, pt=False, refuse=True, style=False, env=False), '§2.4 の順どおり。refuse の保留は札に出ない（Gr2 の指摘の型）'),
         ('Holm で棄却・条項なし・pt 差の傾きが立つ・環境保留', dict(kept=6, rej=True, sat2=False, pt=True, refuse=False, style=False, env=True), '§2.4 の順どおり')]
for nm, s, note in CASES:
    P('  - %s → 列を第一適合で読むと「%s」（%s）' % (nm, first(s), note))
P('- Ge1 の是正案 A（列の先頭を判定不能・次に非有意）と、同じ票の「凍結に向けた必須改訂条件 1」（判定不能 → 解釈条項 → 非有意 → …）は順が食い違う。後者は Holm で棄却されない対比に解釈条項の札を先に当てる順であり、§2.4 の定義（条項は棄却された対比にだけ当てる）とも合わない。'); P('')

# ---------------- W2
say('W2')
proc = T['procedure']
P('## W2. 器材の整備と合成データの全分岐発火が凍結前の手順にあるか（Cl1 重1・Ge1 重大3・Ge2 重大1・Gr1 重大7・Gr2 重大4）'); P('')
P('- 正本 `procedure`（%d 項）のうち「整備」「synth」「合成」を含む項: %d。' % (len(proc), sum(any(w in x for w in ('整備', 'synth', '合成')) for x in proc)))
m5 = re.search(r'\*\*凍結の前に残る手順\*\*: ([^\n]+)', DRAFT)
P('- 草案6 §5「凍結の前に残る手順」: 「%s」（「整備」%s・「合成」%s）。' % (m5.group(1), 'あり' if '整備' in m5.group(1) else 'なし', 'あり' if '合成' in m5.group(1) else 'なし'))
mj = re.search(r'\*\*未整備（([^）]+)）\*\*: ([^。]+)。', DF['J']['text'])
P('- 転記行 J: 「未整備（%s）」・%d 本（%s）。' % (mj.group(1), len(mj.group(2).split('・')), mj.group(2)))
FZ = TX('design', 'design-stageF-FROZEN.md')
P('- 段階 F の凍結文書（型）: 「全組合せ表 288 行〔発火可能 80・発火不能 208〕」の句 %s・「80/80 発火」の句 %s・「整備済み（2026-09-11・コミット 8ec85d3・公開）」の句 %s（Ge1・Ge2・Gr2 の型の引用の照合）。' % (
    'あり' if '全組合せ表 288 行〔発火可能 80・発火不能 208〕' in FZ else 'なし', 'あり' if '80/80 発火' in FZ else 'なし', 'あり' if '整備済み（2026-09-11・コミット 8ec85d3・公開）' in FZ else 'なし')); P('')

# ---------------- W3
say('W3')
PS = CRULE['pt_slope']
P('## W3. pt 差の傾きの仕様の文字列と格子の実装（Ge1 中4・Gr1 重大1 (a)(d)・Cl2 重大5・Cl1 中9）'); P('')
for k in ('estimator', 'weights', 'se', 'test', 'level', 'direction', 'interval'):
    P('- 正本 `pt_slope.%s`: 「%s」' % (k, PS[k]))
so = fn_src('tools/power_grid_A.py', 'one')
chk = [('d は率の差（100 倍しない）', 'd = kt[idx] / n - kc[idx] / n' in so), ('z̄ は重み付き平均 Σwz/Σw', 'zb = float((w * zz).sum() / w.sum())' in so), ('se に残差の尺度母数を掛けない（固定効果型）', 'se = math.sqrt(1.0 / sxx)' in so),
       ('重みの q は (k+0.5)/(n+1)', 'qc = (kc[idx] + 0.5) / (n + 1)' in so), ('z 統計量は slope/se', "'zpt': slope / se" in so)]
P('- 格子 `power_grid_A.one()` の実装: ' + '・'.join('%s＝%s' % x for x in chk))
P('- 正本の文字列が一義に決めているか: 単位の語「pt／z」が `estimator` に %s（実装の傾きは率／z）・`se` の z̄ が重み付きであることの語 %s・残差の尺度母数を使わないことの語 %s・`print_strings.label_confirmed` の単位「pt／z」%s。' % (
    'あり' if 'pt／z' in PS['estimator'] else 'なし', 'あり' if ('重み付き' in PS['se'] or 'Σwz' in PS['se']) else 'なし', 'あり' if ('尺度母数' in PS['se'] or '残差' in PS['se']) else 'なし', 'あり' if 'pt／z' in T['print_strings']['label_confirmed'] else 'なし'))
ls = TX('tools', 'numbers_lint.py'); mk = re.search(r"SKIP_STR = SKIP_CONST \| \{([^}]*)\}", ls); skip = set(re.findall(r"'([^']+)'", mk.group(1)))
P('- `numbers_lint.py` の `SKIP_STR` に `weights`・`se`・`interval`: %s（`estimator`・`level` は検査の内側: %s）。' % (all(x in skip for x in ('weights', 'se', 'interval')), not any(x in skip for x in ('estimator', 'level'))))
P('- Gr1 (a)「d と重みが別の率」: 重みは d＝k_A/n−k_B/n の分散 p_A(1−p_A)/n＋p_B(1−p_B)/n を、p の推定に q＝(k+0.5)/(n+1) を使って置いたもの。回帰する量の分散の推定であり、推定量の定義としては一つ。q を使う理由（k=0 で分散 0 になるのを避ける）は正本に書かれていない。'); P('')

# ---------------- W4
say('W4')
zh = float(norm.isf(ALPHA / M / 2))
P('## W4. 臨界値の照合（Gr2 重大1「≈3.38」・Ge2 重大2・Gr1 重大1 (b)・Cl2 3-1）'); P('')
P('- Holm 初段の正規の臨界 Φ⁻¹(1−α/(2·%d))＝**%.4f**（格子 `levels.z_holm_first`＝%.4f）。Gr2 の「≈3.38」は両側水準 %.6f（α/%.1f）に当たり、α/35 の臨界ではない。Gr1 の「3.19」「3.186」は四捨五入の範囲。' % (M, zh, PG['levels']['z_holm_first'], 2 * norm.sf(3.38), ALPHA / (2 * norm.sf(3.38))))
P('- 同じ水準の t 分布の臨界（参考）: ' + '・'.join('df=%d で %.2f' % (d, tdist.isf(ALPHA / M / 2, d)) for d in (1, 2, 3, 4)) + '。Ge2「df=1 で 450 を超える」・Gr1「df=2 で約 22・df=4 で約 7」・Gr2「df=4 でおよそ 7〜8」と照合。')
P('- Holm の後段の正規の臨界: ' + '・'.join('α/%d で %.3f' % (j, norm.isf(ALPHA / j / 2)) for j in (35, 34, 31, 26, 16, 2, 1)) + '。Cl2 3-1 の「第 5 段 α/31 → 3.154・第 10 段 α/26 → 3.102・第 20 段 α/16 → 2.955」と照合。m=35 の Holm の最終段は α/1（Cl2 の条件 13「最終段 α/16」は段の取り違え）。')
P('- 読み: 正本の se は各規模の二項の理論分散（q で推定）から作り、残差から尺度母数を推定しない。この構成で「t（残存点数−2）」は標準の参照分布ではない（t を使うのは残差から分散を推定する場合）。正規近似が小さい α で持つかは、残存規模数と基底率ごとのシミュレーションで測る（第二部 W27）。'); P('')

# ---------------- W5
say('W5')
q_ = lambda k: (k + 0.5) / (n + 1)
var_ = lambda ka, kb: (q_(ka) * (1 - q_(ka)) + q_(kb) * (1 - q_(kb))) / n
cens_ = lambda ka, kb: (ka <= KLO and kb <= KLO) or (ka >= KHI and kb >= KHI)
wref = 1 / var_(100, 100)
P('## W5. 床・天井に近いセルの重み（Ge2 重大2「約 100 倍」・Gr1 重大1 (c)「Var≈1.24e-5・重み≈8.0e4・約 200 倍」）'); P('')
P('| k_A | k_B | 両腕条件で検閲 | Var(d) | 重み | 中間（100, 100）との比 |'); P('|---|---|---|---|---|---|')
for ka, kb in [(0, 0), (0, 10), (5, 10), (10, 10), (0, 100), (0, 200), (200, 185), (20, 20), (100, 100)]:
    P('| %d | %d | %s | %.3e | %.0f | %.1f |' % (ka, kb, '検閲' if cens_(ka, kb) else '残る', var_(ka, kb), 1 / var_(ka, kb), (1 / var_(ka, kb)) / wref))
best = max(((1 / var_(ka, kb)) / wref, ka, kb) for ka in range(n + 1) for kb in range(n + 1) if not cens_(ka, kb))
best_same_side = max(((1 / var_(ka, kb)) / wref, ka, kb) for ka in range(n + 1) for kb in range(n + 1) if not cens_(ka, kb) and ((ka <= 100) == (kb <= 100)))
P('')
P('- q(0)＝%.6f・q(0)(1−q(0))＝%.6f。両腕とも k=0 なら 2q(1−q)/n＝%.3e（Gr1 の 1.24e-5 は一腕分 q(1−q)/n＝%.3e で、二腕の和の半分）・重み %.0f（Gr1 の 8.0e4 は二倍の誤り）・中間との比 %.1f（Gr1 の「約 200 倍」は二倍の誤り・Ge2 の「約 100 倍」が合う）。**ただし両腕とも k=0 のセルは両腕条件で検閲され、傾きに入らない**。' % (q_(0), q_(0) * (1 - q_(0)), 2 * q_(0) * (1 - q_(0)) / n, q_(0) * (1 - q_(0)) / n, 1 / var_(0, 0), (1 / var_(0, 0)) / wref))
P('- 検閲されないセルの中で重みが最大になるのは (k_A, k_B)＝(%d, %d) の型（片腕が床・もう片腕が天井）で中間の %.1f 倍。両腕が同じ側（ともに 100 以下・ともに 100 超）で検閲されないセルの最大は (%d, %d) で %.1f 倍。確証族の腕の対で片腕が床・片腕が天井の組は 4B の既測では現れない（W18 の基底）。' % (best[1], best[2], best[0], best_same_side[1], best_same_side[2], best_same_side[0])); P('')

# ---------------- W6（費用の器を正本と cost-facts から組み直す）
say('W6')
hU, bU = md_table(CF, '## U.'); hR, bR = md_table(CF, '## R.')
col = lambda h, s: next(i for i, x in enumerate(h) if x.startswith(s))
SETUP = {r[0]: float(r[col(hU, '経費合計')]) for r in bU}; TPH = {r[0]: float(r[col(hR, '試行／時')]) for r in bR}; RATE = {r[0]: float(r[col(hR, '実測の時間あたりユニット')]) for r in bR}
TAG = {'L4': 'costpilot-L4', 'A100': 'costpilot-A100'}; C = T['cost']; SF = dict(C['size_factor_assumption']); SH = C['session_h']; CAP = T['capacity_rule']['concurrency_cap']; AB = T['anchor_band']; n_cal = T['calibration_n']
anchor_trials = len(AB['scenarios']) * len(AB['arms']) * n; base_trials = len(SC) * len(ARMS) * (pn + n)
GC = dict(TAG=TAG, TPH=TPH, SETUP=SETUP, CAP=CAP, AB=AB, base_trials=base_trials, anchor_trials=anchor_trials, SF=SF, n_cal=n_cal, T=T, SH=SH, RATE=RATE, math=math)
src_pm = fn_src('tools/design_facts_A.py', 'plan_model'); src_pb = fn_src('tools/design_facts_A.py', 'plan_bridge'); exec(src_pm, GC); exec(src_pb, GC)


def plan_bridge_cal(k, bc, bound, cal_at_session_concurrency=False):
    env = bc['bridge_env']; tg = TAG[env]; tph = TPH[tg]; st = SETUP[tg] / 3600; eff = tph * (bc['bridge_concurrency'] / CAP if bound == 'upper' else 1.0)
    tr = len(T['bridge']['arms']) * T['bridge']['n']; sess = 1; h_run = 0.0
    for _ in range(60):
        h_run = tr * GC['SF'][k] / eff + sess * n_cal * GC['SF'][T['calibration']['model']] / (eff if cal_at_session_concurrency else tph)
        new = max(1, math.ceil(h_run / (SH - st)))
        if new == sess:
            break
        sess = new
    h_tot = h_run + sess * st
    return {'env': env, 'concurrency': bc['bridge_concurrency'], 'trials': tr + sess * n_cal, 'hours': round(h_tot, 2), 'sessions': sess, 'units': round(h_tot * RATE[tg], 2)}


def totals(bound, bridge_fn=None, sf=None, conc_over=None):
    GC['SF'] = dict(SF, **(sf or {})); rows = {}
    for m in T['models']:
        k = m['key']; e = T['environments'][k]; rows[k] = GC['plan_model'](k, e['env'], (conc_over or {}).get(k, e['concurrency']), bound)
    for k, bc in T['bridge']['cells'].items():
        rows['橋 ' + k] = (bridge_fn or GC['plan_bridge'])(k, bc, bound)
    GC['SF'] = dict(SF)
    return rows, round(sum(v['units'] for v in rows.values()), 1), round(sum(v['hours'] for v in rows.values()), 2), sum(v['trials'] for v in rows.values())


rows_u, U_u, H_u, TR_u = totals('upper'); rows_l, U_l, H_l, TR_l = totals('lower')
base_ok = abs(U_u - DF['F']['data']['plans']['upper']['units']) < 0.05 and abs(U_l - DF['F']['data']['plans']['lower']['units']) < 0.05
rows_uc, U_uc, _, TR_uc = totals('upper', bridge_fn=plan_bridge_cal); rows_lc, U_lc, _, _ = totals('lower', bridge_fn=plan_bridge_cal)
rows_uc2, U_uc2, _, _ = totals('upper', bridge_fn=lambda k, bc, b: plan_bridge_cal(k, bc, b, True))
P('## W6. 橋のセッションの校正腕（Ge1 重大2・Cl1 中4・Cl2 重大3・Cl3 重大5）'); P('')
P('- `design_facts_A.plan_bridge` に校正腕の項（`n_cal`）: %s／`plan_model` には: %s。器を組み直した上界 %.1f・下界 %.1f ユニットは設計事実 JSON と一致: %s。' % ('n_cal' in src_pb, 'n_cal' in src_pm, U_u, U_l, base_ok))
P('- 上界のセッション: 機種 %d（転記行 A の校正腕の数え方）＋橋 %d＝%d。' % (sum(rows_u[m['key']]['sessions'] for m in T['models']), sum(v['sessions'] for k, v in rows_u.items() if k.startswith('橋')), sum(v['sessions'] for v in rows_u.values())))
P('- 橋の二セッションに校正腕（n=%d・4B-2507 の係数）を足すと: 試行 +%d（手元合計 %s → %s）・上界 %.1f → **%.1f ユニット（+%.2f）**・下界 %.1f → %.1f。校正腕を橋のセッションの同時要求数で走らせる数え方でも上界 %.1f（+%.2f）。セッション数は変わらない: %s。' % (
    n_cal, TR_uc - TR_u, format(DF['A']['data']['total_local'], ','), format(DF['A']['data']['total_local'] + TR_uc - TR_u, ','), U_u, U_uc, U_uc - U_u, U_l, U_lc, U_uc2, U_uc2 - U_u,
    all(rows_uc[k]['sessions'] == rows_u[k]['sessions'] for k in rows_u)))
P('- 票の増分の見込み: Cl1「約 +2 ユニット」・Cl3「+3〜6 ユニット程度」・Cl2「1 ユニット未満」。上の再計算では Cl2 が合う。')
V24 = TX('records', 'reviews', 'AB', 'round-claudeai', 'verification-claudeai-AB-2.md')
P('- Ge1 の「追い問い V24 では 8B に橋の A100 側 2,600 試行を同居」: V24（草案4 の追い問い）に「8B に橋の A100 側 2,600 試行を同居」の句 %s。現行の橋は 4B の A100 側と 8B の L4 側で、`plan_bridge` は独立のセッション（経費つき）として数える（裁定 D3 以後の配置）。' % ('あり' if '8B に橋の A100 側 2,600 試行を同居' in V24 else 'なし')); P('')

# ---------------- W7
say('W7')
Cc = T['calibration']; bN = T['bases_4B2507_api']['N1']['Ncold']; base = Fraction(bN['k'], bN['n'])
kw = math.ceil(base * pn - Fraction(Cc['withdrawal']['band_pt'], 100) * pn) - 1


def lower_tail(n1, p1, n2, p2, band_pt):
    """P(X1/n1 < X2/n2 − band)（超）。"""
    W = np.outer(binom.pmf(np.arange(n1 + 1), n1, p1), binom.pmf(np.arange(n2 + 1), n2, p2))
    D = (np.arange(n2 + 1)[None, :] * n1 - np.arange(n1 + 1)[:, None] * n2) * 100
    return float(W[D > band_pt * n1 * n2].sum())


_, bS = md_table(CF, '## S.')
loc_ncold = ['%s %s' % (r[0].replace('costpilot-', ''), r[2].split('（')[0]) for r in bS if r[1] == 'Ncold']
P('## W7. 撤退条件の参照系列（Gr1 重大4・Gr2 重大5・Cl1 中6・Cl3 中8）'); P('')
P('- 正本 `calibration.withdrawal.reference`＝「%s」・`band_fail.reference`＝「%s」。草案6 §2.8 に「合格枝と同じ API 既測」の句 %s。' % (Cc['withdrawal']['reference'], Cc['band_fail']['reference'], 'あり' if '合格枝と同じ API 既測' in DRAFT else 'なし'))
P('- 現行（一標本・API 既測 %.3f・n=%d・%d pt 超・下側）: 発火 X ≤ %d・帰無発火率 %.2e・検出 真の率 0.90 で %.3f・0.85 で %.3f・0.80 で %.3f。門0 の手元 Ncold × N1: %s。' % (float(base), pn, Cc['withdrawal']['band_pt'], kw, binom.cdf(kw, pn, float(base)), binom.cdf(kw, pn, 0.90), binom.cdf(kw, pn, 0.85), binom.cdf(kw, pn, 0.80), '・'.join(loc_ncold)))
P('- 不合格枝の代案（門0.5 の手元 Ncold × N1 n=%d を参照にした二標本・パイロット n=%d・%d pt 超・下側）: 帰無発火率 真の率 0.975 で %.2e・0.95 で %.2e・0.90 で %.2e／検出（手元 0.95・パイロットの真の率が 15／20／25 pt 下）%.3f／%.3f／%.3f。' % (
    nid, pn, Cc['withdrawal']['band_pt'], lower_tail(pn, 0.975, nid, 0.975, 15), lower_tail(pn, 0.95, nid, 0.95, 15), lower_tail(pn, 0.90, nid, 0.90, 15), lower_tail(pn, 0.80, nid, 0.95, 15), lower_tail(pn, 0.75, nid, 0.95, 15), lower_tail(pn, 0.70, nid, 0.95, 15)))
P('- 参考: 現行の一標本は基底を固定するため、真の率が同じでも二標本より発火しにくい。代案の帰無発火率は門0.5 の標本誤差を含む分だけ上がる。'); P('')

# ---------------- W8
say('W8')
E_ = T['environment_band']; br = T['bridge']; nb = len(br['cells']); bN1 = T['bases_4B2507_api'][br['scenario']]
rates_api = {arm: (bN1[arm]['k'] / bN1[arm]['n'] if arm in bN1 else E_['rule_missing_base_rate']) for arm in ARMS}
fam_arms = sorted({c['A'] for c in CONTR} | {c['B'] for c in CONTR}, key=ARMS.index)


def exp_held(rates, contrasts, b):
    qd = {arm: diff_tail(n, p, n, p, b) for arm, p in rates.items()}
    return sum(1 - ((1 - qd[c['A']]) * (1 - qd[c['B']])) ** nb for c in contrasts)


def p_any(rates, arms, b):
    return 1 - float(np.prod([(1 - diff_tail(n, rates[x], n, rates[x], b)) ** nb for x in arms]))


loc_N = [r for r in bS if r[1] == 'N']; kN = sum(int(r[2].split('/')[0]) for r in loc_N); nN = sum(int(r[2].split('/')[1].split('（')[0]) for r in loc_N)
VAR = [('4B-2507 の API 既測（N1・既測の無い腕は 0.5）＝選択規則', rates_api, CONTR), ('全腕 0.5', {x: 0.5 for x in ARMS}, CONTR), ('全腕 0.35', {x: 0.35 for x in ARMS}, CONTR),
       ('API 既測のうち N だけ門0 の手元（両 GPU の和 %d/%d）' % (kN, nN), dict(rates_api, N=kN / nN), CONTR), ('API 既測・保留の単位を N1 の 7 対比に限る', rates_api, [c for c in CONTR if c['scenario'] == 'N1'])]
P('## W8. 環境帯: 保留の単位・選択規則の率への依存・腕数（Gr1 重大5・Gr2 中6・Ge2 中5・Cl2 重大4・Cl2 軽微・Gr1 中5）'); P('')
P('- 正本 `environment_band.hold`: 「%s」／`unit`: 「%s」／`environment_secondary`: 「%s」' % (E_['hold'], E_['unit'], FAM['environment_secondary']['text']))
P('- 格子 `grid_M` は保留の和を正本の確証 %d 対比（5 場面すべて）に取り、N1 の率を全場面の対比に載せる（`held = [... for c in FAM[\'contrasts\']]`・橋の機種数 nb=%d）: %s。草案6 (xiii) に「環境差は N1 の 13 腕だけで測り、他の場面へは外挿として読む」の句 %s。' % (len(CONTR), nb, "for c in FAM['contrasts']" in fn_src('tools/power_grid_A.py', 'grid_M'), 'あり' if '環境差は N1 の 13 腕だけで測り、他の場面へは外挿として読む' in DRAFT else 'なし'))
P('')
P('| 置いた真の率 | 10 pt | 12 pt | 15 pt | 20 pt |'); P('|---|---|---|---|---|')
for nm, rates, cs in VAR:
    P('| %s | %s |' % (nm, ' | '.join('%.3f' % exp_held(rates, cs, b) for b in E_['candidates_pt'])))
P('')
P('- 転記行 M の値（12 pt で 0.88）の再現: %.4f。規則（期待誤保留数 ≤ %d）を満たす最小の候補は、選択規則の率で %s・全腕 0.5 で %s・全腕 0.35 で %s。' % (exp_held(rates_api, CONTR, 12), E_['rule_expected_max'],
    min(b for b in E_['candidates_pt'] if exp_held(rates_api, CONTR, b) <= E_['rule_expected_max']), min(b for b in E_['candidates_pt'] if exp_held({x: 0.5 for x in ARMS}, CONTR, b) <= E_['rule_expected_max']), min(b for b in E_['candidates_pt'] if exp_held({x: 0.35 for x in ARMS}, CONTR, b) <= E_['rule_expected_max'])))
P('- 「いずれかの腕が超える確率」（12 pt・選択規則の率）: 橋の 13 腕 %.3f（転記行 M の 0.109）・確証族に現れる %d 腕（%s）%.3f。全腕 0.5 なら 13 腕 %.3f（Gr1 の 0.169 は腕 13・機種 1 の値: %.3f）。' % (
    p_any(rates_api, ARMS, 12), len(fam_arms), '・'.join(fam_arms), p_any(rates_api, fam_arms, 12), p_any({x: 0.5 for x in ARMS}, ARMS, 12), 1 - (1 - diff_tail(n, 0.5, n, 0.5, 12)) ** 13))
P('- 率 0 を置いた腕（帯が発火しない）: %s（いずれも確証族に現れない: %s）。環境値は `environment_rule.values`＝%s、`environment_secondary` の「環境切替の片側」は値が三つのときの片側を定義していない。' % ('・'.join(x for x, p in rates_api.items() if p == 0.0), all(x not in fam_arms for x, p in rates_api.items() if p == 0.0), T['environment_rule']['values'])); P('')

# ---------------- W9
say('W9')
T_hdr, T_rows = md_table(CF, '## T.')
boot = TX('tools', 'colab', 'boot_cost_pilot.py'); runner = TX('tools', 'run_preamble_local.py')
mm = re.search(r"OP4B_MAXLEN', '(\d+)'", boot); mt = re.search(r"'--max-tokens', type=int, default=(\d+)", runner)
GG = HF['gpu_gib']; m32 = HF['models']['32B']; KVt = lambda v: 2 * v['num_hidden_layers'] * v['num_key_value_heads'] * v['head_dim'] * 2 / 2 ** 30
avail32 = T['capacity_rule']['gpu_fraction'] * GG['A100-80GB'] - m32['safetensors_gib'] - T['capacity_rule']['overhead_gib']
prompt_med = int(T_rows[0][col(T_hdr, 'prompt tok')]); outs = [r[col(T_hdr, '出力 tok')] for r in T_rows]
out_max = max(int(o.split('／')[2]) for o in outs); out_p90 = max(int(o.split('／')[1]) for o in outs)
P('## W9. KV のトークン長（Gr1 重大3）'); P('')
P('- `hf-models-A.json` の注: 「%s」' % HF.get('kv_bytes_per_token_note'))
P('- 門0 の起動器 `boot_cost_pilot.py` の既定 `max_model_len`＝%s・走行器 `run_preamble_local.py` の既定 `--max-tokens`＝%s。正本に `max_model_len`・`max_tokens` のキー: %s。' % (mm.group(1) if mm else '?', mt.group(1) if mt else '?', any(k in json.dumps(T) for k in ('max_model_len', 'max_tokens'))))
P('- 門0（N1 のみ・腕をまとめて）の prompt 中央値 %d・出力の p90 の最大 %d・出力の最大 %d。' % (prompt_med, out_p90, out_max))
P('- 32B（同時 %d・A100 80GB）の KV に使える量 %.2f GiB に対し、要求あたりのトークン長ごとの必要量: ' % (T['environments']['32B']['concurrency'], avail32) + '・'.join('%s %d トークン %.2f GiB' % (nm, tok, T['environments']['32B']['concurrency'] * KVt(m32) * tok) for nm, tok in (('登録', T['capacity_rule']['kv_tokens_per_request']), ('prompt 中央値＋出力 p90', prompt_med + out_p90), ('prompt 中央値＋出力の最大', prompt_med + out_max), ('prompt 中央値＋max_tokens', prompt_med + int(mt.group(1))), ('max_model_len', int(mm.group(1))))) + '。')
P('- Gr1 の「8192 で 61.02+17×(0.50×4)+1.5=96.5」: %.2f。vLLM は KV を要求の実トークン数でページ単位に割り当て、足りない場合は要求を待たせる（先取り）ので、`max_model_len` × 同時要求数を起動時に予約する規則ではない。したがって登録値 2,048 は「実トークン長の見込み」であり、走行器の設定（max_model_len・max_tokens）は正本に書かれていない、が一次記録から言えること。' % (m32['safetensors_gib'] + 17 * KVt(m32) * 8192 + 1.5)); P('')

# ---------------- W10
say('W10')
_, U_14b20, _, _ = totals('upper', conc_over={'14B': 20})
P('## W10. 同じ環境値の中の同時要求数（Cl1 中5）'); P('')
P('- 正本 `environments`: 14B 同時 %d・40GB のとき %d／8B 同時 %d・40GB のとき %d。橋: 4B の A100 側 同時 %d（本走行の 4B は L4 同時 %d）・8B の L4 側 同時 %d（本走行の 8B は A100 同時 %d）。' % (
    T['environments']['14B']['concurrency'], T['environments']['14B']['if_40GB']['concurrency'], T['environments']['8B']['concurrency'], T['environments']['8B']['if_40GB']['concurrency'], T['bridge']['cells']['4B']['bridge_concurrency'], T['environments']['4B']['concurrency'], T['bridge']['cells']['8B']['bridge_concurrency'], T['environments']['8B']['concurrency']))
P('- 14B を 80GB でも同時 20 に固定した場合の上界: %.1f ユニット（現行 %.1f・+%.1f）。Cl1 の「43.0 → 約 51・合計 251 → 259」と照合。橋 8B の L4 側（同時 12）は収容の上限であり、環境差と同時要求数の差は橋では分けられない。' % (U_14b20, U_u, U_14b20 - U_u)); P('')

# ---------------- W11
say('W11')
P('## W11. 報告雛形の欄（Cl2 重大6・重大7・軽微・Cl3 中13・Cl1 中10・Gr2 中10・Ge1 軽微8・Ge2 軽微8・Gr1 軽微）'); P('')
for w in ['多い場合', '感度', 'κ', '判定器の妥当性', '臨界規模', '圧の内訳', 'SHA-256', '上向きの確証があれば', '対比別の検出域', '三行']:
    P('- 雛形に「%s」の出現 %d 回。' % (w, TPL.count(w)))
m7 = re.search(r'- 〔power_grid_A[^\n]*', TPL)
P('- 雛形 §7 の再計算の欄: 「%s」（効果量 Δ の指定の語「Δ」%s）。' % (m7.group(0) if m7 else '?', 'あり' if (m7 and 'Δ' in m7.group(0)) else 'なし'))
P('- 正本 `report_rules.typed_numbers`: 「%s」（SHA-256 の語 %s）。雛形の冒頭「打ち込んでよい数」の句に SHA-256 %s。' % (T['report_rules']['typed_numbers'], 'あり' if 'SHA-256' in T['report_rules']['typed_numbers'] else 'なし', 'あり' if 'SHA16／SHA-256〔記帳値〕' in TPL else 'なし'))
ids_in_D = sorted({c['id'] for c in CONTR if c['id'] in DF['D']['text']})
P('- 転記行 D の文に現れる対比 id: %d 本（%s）。雛形 §4「対比別の検出域（凍結時の転記行 D の実基底の行を逐語転記）」が求める対比ごとの行は、転記行 D ではなく格子の md の DR 表（%d 行）にある。' % (len(ids_in_D), '・'.join(ids_in_D), len(PG['DR'])))
PGmd = TX('records', 'A', 'power-grid-A.md'); hdrDR = next(l for l in PGmd.split('\n') if l.startswith('| 対比 | A の基底'))
P('- 格子 md の DR 表の列: `%s`（解釈条項の発火率の列 %s・Cl3 中10 の照合）。' % (hdrDR, 'あり' if '条項' in hdrDR else 'なし')); P('')

# ---------------- W12
say('W12')
pre = ls.split('\ndoc = open(')[0]; saved = sys.argv; sys.argv = ['numbers_lint.py', '--doc', 'x', '--json', os.path.join(REPO, 'design', 'contrasts-A.json')]
GL = {'__name__': 'lint_pre'}; exec(pre, GL); sys.argv = saved
CONST = sorted(GL['CONST'], key=float)


def run_lint(doc):
    r = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'numbers_lint.py'), '--doc', doc, '--json', os.path.join(REPO, 'design', 'contrasts-A.json')], capture_output=True, cwd=REPO, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    out = r.stdout.decode('utf-8', 'replace'); mm_ = re.search(r'未登録の数: 本文 (\d+)・正本の説明文 (\d+)', out)
    return r.returncode, (int(mm_.group(1)), int(mm_.group(2))) if mm_ else None


INJ = [('§2.7 錨帯 12 pt → 15 pt', '帯は **12 pt・「超」**', '帯は **15 pt・「超」**'), ('§2.9 門0.5 n=160 → n=80', '13 腕 × **n=160**', '13 腕 × **n=80**'),
       ('§2.4 Holm m=35 → m=30', '35・m=35 で固定・両側', '35・m=30 で固定・両側'), ('§2.10 測定不能 30% → 40%', '30% 超で「測定不能」', '40% 超で「測定不能」'),
       ('§2.6 様式門 30 pt → 20 pt', '様式門（30 pt 超で判定保留', '様式門（20 pt 超で判定保留'), ('§2.1 32B 同時 17 → 16', '14B 24・32B 17。', '14B 24・32B 16。'),
       ('§2.5 感度 0.03 → 0.04', '（0.03／0.08・0.97／0.92）', '（0.04／0.08・0.97／0.92）'), ('§1 に派生数「期待 11.81 本」を足す', 'β₃ だけが立つ対比は「記述（対数オッズ尺度でのみ）」に置く。', 'β₃ だけが立つ対比は「記述（対数オッズ尺度でのみ）」に置く。期待 11.81 本。')]
base_rc, base_cnt = run_lint(os.path.join(REPO, 'design', 'design-stageA-draft6.md'))
P('## W12. 本文の数の機械検査の検出範囲（Cl3 重大2・重大6・Cl1 中8・中9・軽14・Gr2 中11・Gr1 軽微・Cl2 軽微）'); P('')
P('- 設計定数の集合 `CONST`（%d 種）: %s。' % (len(CONST), ', '.join(CONST)))
P('- 草案6 そのまま: 終了コード %d・未登録（本文, 説明文）%s。' % (base_rc, base_cnt)); P('')
P('| 書き換え | 元の句の出現 | 終了コード | 未登録（本文, 説明文） | 検出 |'); P('|---|---|---|---|---|')
for nm, old, new in INJ:
    cnt = DRAFT.count(old); path = os.path.join(WORK, 'inj-%d.md' % INJ.index((nm, old, new)))
    open(path, 'w', encoding='utf-8', newline='\n').write(DRAFT.replace(old, new, 1)); rc, c2 = run_lint(path)
    P('| %s | %d | %d | %s | %s |' % (nm, cnt, rc, c2, '検出' if rc != 0 else '見逃し'))
rc_t, cnt_t = run_lint(os.path.join(REPO, 'records', 'A', 'results-report-template-A.md'))
P('')
P('- 報告雛形に当てた場合: 終了コード %d・未登録 %s（記録ファイルは作っていない: `records/A/` に雛形の lint 記録 %s）。' % (rc_t, cnt_t, 'あり' if any('template' in f and 'lint' in f for f in os.listdir(os.path.join(REPO, 'records', 'A'))) else 'なし'))
mc_lines = TX('tools', 'make_contrasts_A.py').split('\n')
for ln in (91, 96, 98, 104):
    s = mc_lines[ln - 1]; nums = [x for x in re.findall(r'(?<![A-Za-z0-9_.])\d+(?:\.\d+)?', s) if x not in ('2026', '09', '13')]
    P('- `make_contrasts_A.py` 行 %d の説明文の直書きの数: %s（抜粋: %s…）' % (ln, '・'.join(nums), s.strip()[:90].replace('|', '｜')))
src_df = TX('tools', 'design_facts_A.py'); toks = []
for node in ast.walk(ast.parse(src_df)):
    if isinstance(node, ast.Constant) and isinstance(node.value, str) and not re.search(r'[/\\]|\.json|\.md|\.py', node.value):
        s = re.sub(r'%[-+ #0]*\d*(?:\.\d+)?[sdfegrx%]', ' ', node.value)
        for mm_ in re.finditer(r'(?<![A-Za-z0-9_.\-門案])\d+(?:\.\d+)?(?![\dBG.])', s):
            ctx = s[max(0, mm_.start() - 8):mm_.end() + 8].replace('\n', ' ').replace('|', '｜')
            if not re.search(r'20\d\d-\d\d', ctx):
                toks.append((node.lineno, mm_.group(0), ctx))
P('- `design_facts_A.py` の文字列リテラル（パス・日付・機種名〔4B・32B・4B-2507〕・GPU 名〔A100・40GB〕・門の番号〔門0.5〕を除く）に残る数: %d 箇所（%s）。' % (len(toks), '・'.join('行 %d「%s」' % (l, c.strip()) for l, _, c in toks))); P('')

# ---------------- W13
say('W13')
FC = T['firth_check']; fcsrc = TX('tools', 'firth_check_A.py')
P('## W13. Firth の一致検査: firth.py 側の収束の打ち切りの大きさ（Cl3 中12・1-1・Cl1 1.3・Gr1 中2・Gr2 中8・Cl2 3-7）'); P('')
P('- `firth_check_A.py` の `py_fit` は `firth.fit(X, y)` を既定の閾値で呼ぶ: %s（`firth.fit` の既定 gtol＝1e-7・tol＝1e-9・max_iter＝200）。正本の R の control: `%s`。' % ('full = firth.fit(X, y)' in fcsrc, FC['R_control']))
ZSPAN = float(zs[-1]); rng = np.random.default_rng(FC['seed'])
SYN = [('synth_rising_ptconst', np.linspace(0.3, 0.9, len(zs)), 'const', 0.15), ('synth_mid_delta', np.full(len(zs), 0.5), 'slope', 0.15), ('synth_floor_sparse', np.full(len(zs), 0.03), 'slope', 0.05)]
assert "SYN = [('synth_rising_ptconst', np.linspace(0.3, 0.9, len(ZS)), 'const', 0.15), ('synth_mid_delta', np.full(len(ZS), 0.5), 'slope', 0.15), ('synth_floor_sparse', np.full(len(ZS), 0.03), 'slope', 0.05)]" in fcsrc


def fit_pair(X, y, tests):
    f0 = firth.fit(X, y); f1 = firth.fit(X, y, gtol=1e-12, tol=1e-14, max_iter=5000)
    d_b = float(np.max(np.abs(f0['beta'] - f1['beta']))); d_ll = abs(f0['ll'] - f1['ll']); d_st = 0.0
    for j in tests:
        r0 = firth.fit(X, y, fixed={j: 0.0}); r1 = firth.fit(X, y, fixed={j: 0.0}, gtol=1e-12, tol=1e-14, max_iter=5000)
        d_st = max(d_st, abs(2 * (f0['ll'] - r0['ll']) - 2 * (f1['ll'] - r1['ll'])))
    return d_b, d_ll, d_st, f1['converged'], f1['score_max']


P(''); P('| データ | 行数 | 係数の差の最大 | 罰則付き対数尤度の差 | 統計量の差の最大 | 厳しい側の収束・スコアの最大 |'); P('|---|---|---|---|---|---|')
for name, pc, kind, eff in SYN:
    pt = np.clip(pc + (eff if kind == 'const' else eff * zs / ZSPAN), 0.001, 0.999); rows = []
    for i, z in enumerate(zs):
        kc = int(rng.binomial(n, pc[i])); kt = int(rng.binomial(n, pt[i])); rows += [(1, 0, z)] * kc + [(0, 0, z)] * (n - kc) + [(1, 1, z)] * kt + [(0, 1, z)] * (n - kt)
    R_ = np.array(rows, float); X = np.column_stack([np.ones(len(R_)), R_[:, 1], R_[:, 2], R_[:, 1] * R_[:, 2]])
    d = fit_pair(X, R_[:, 0], [3]); P('| %s（firth_check と同じ手順・seed %d） | %d | %.2e | %.2e | %.2e | %s・%.1e |' % (name, FC['seed'], len(R_), d[0], d[1], d[2], d[3], d[4]))
r2 = np.random.default_rng(20260913)
Xs = np.column_stack([np.ones(239)] + [(r2.random(239) < p).astype(float) for p in (0.5, 0.3, 0.6, 0.4, 0.2, 0.15)]); eta = Xs @ np.array([-0.5, 0.8, -0.6, 0.4, 1.0, 0.7, 1.5]); ys = (r2.random(239) < 1 / (1 + np.exp(-eta))).astype(float)
d = fit_pair(Xs, ys, [1, 2, 3, 4, 5, 6]); P('| sex2 に似た合成（n=239・二値の共変量 6・seed 20260913） | 239 | %.2e | %.2e | %.2e | %s・%.1e |' % (d[0], d[1], d[2], d[3], d[4]))
NV = (r2.random(79) < 0.17).astype(float); PI = r2.normal(17, 10, 79); EH = r2.normal(1.7, 0.9, 79); ye = (r2.random(79) < 1 / (1 + np.exp(-(4 - 0.04 * PI - 2.9 * EH)))).astype(float); ye[NV == 1] = 1.0
Xe = np.column_stack([np.ones(79), NV, PI, EH]); d = fit_pair(Xe, ye, [1, 2, 3]); P('| endometrial に似た合成（n=79・NV=1 で準完全分離） | 79 | %.2e | %.2e | %.2e | %s・%.1e |' % (d[0], d[1], d[2], d[3], d[4]))
P('')
P('- 読み: 差は firth.py の既定の打ち切りと厳しい打ち切りの差（R との差ではない）。R logistf との照合（Cl3 の移植照合: sex2 の係数差 1.60e-07 など）は手元に R が無く再現していない（票の申告として記録）。登録の許容差（係数 %s・対数尤度 %s・統計量 %s）に対する余裕は上の表で読む。' % (FC['tolerances']['coef_abs'], FC['tolerances']['penalized_loglik_abs'], FC['tolerances']['plr_stat_abs'])); P('')

# ---------------- W14〜W17
say('W14-17')
IS = T['identity_screen']
P('## W14. 門0.5 の帰無の不合格率の登録値（Cl2 3-6・Cl1 軽15・Cl3 重点9）'); P('')
P('- 正本 `identity_screen.null_fail_ref`: 「%s」。転記行 N の四つ: %s。どれを登録の値とするかの語は正本と §2.9 に %s。検出側（両スタックが真に違うときの不合格率）は転記行 N に %s（第二部 W31）。' % (IS['null_fail_ref'], '・'.join('%s %.4f' % (k, v['fail_rate']) for k, v in PG['N'].items()), 'なし', '無い')); P('')
_, U_sf = None, {}
P('## W15. 停止規則を動かす仮定（Cl2 3-5・Cl1 軽16・Cl3 軽16・Ge2 中6）'); P('')
thr = DF['F']['data']['stop_threshold_units']
for f in (8.0, 9.0, 10.0, 11.0, 12.0):
    rws, Uf, _, _ = totals('upper', sf={'32B': f}); U_sf[f] = Uf
    P('- 32B の係数 %.1f: 32B %.1f ユニット・上界の合計 %.1f → 登録の停止閾値 %.1f を%s。' % (f, rws['32B']['units'], Uf, thr, '超える' if Uf > thr else '超えない'))
P('- 第三の環境（時間貸し）の料金の換算と停止規則への入れ方: 正本 `cost` に換算の語 %s。' % ('あり' if ('第三' in json.dumps(T['cost'], ensure_ascii=False)) else 'なし')); P('')
P('## W16. 非収束の札（Cl2 3-8）'); P('')
nc = max([r.get('nonconverged', 0) or 0 for sec in ('D', 'DR', 'DS') for r in PG[sec]] + [r.get('nonconverged', 0) for r in PG['R']])
P('- 正本 `model.undecidable_rule`: 「%s」（「非収束」の語 %s）・`label_precedence` に非収束の札 %s。格子の D・DR・DS・R 節の非収束率の最大 %.4f。' % (FAM['model']['undecidable_rule'], 'あり' if '収束' in FAM['model']['undecidable_rule'] else 'なし', 'あり' if any('収束' in x for x in LP) else 'なし', nc)); P('')
P('## W17. 転記行 D の「Δ=0・d0=0 の棄却率」の指標名（Gr2 中9・Gr1 中3）'); P('')
r0 = next(r for r in PG['D'] if r['pattern'] == 'mid_const' and r['d0_pt'] == 0 and r['delta_pt_32B_minus_4B'] == 0)
P('- 転記行 D の句: 「%s」。格子の同じ行: 名目 p<α %.4f（Wilson %s）・Holm 初段 %.4f・札 D1 初段 %.4f・札 D1 名目 %.4f。印字の 0.057 は名目の β₃ 棄却率で、指標名の語「名目」は句に %s。' % (
    re.search(r'\*\*Δ=0・d0=0 の棄却率\*\*: [^・]+', DF['D']['text']).group(0), r0['reject_nominal'], r0['reject_nominal_ci95'], r0['reject_holm_first'], r0['card_D1_holm_first'], r0['card_D1_nominal'], 'あり' if '**Δ=0・d0=0 の棄却率（名目' in DF['D']['text'] else 'なし')); P('')

# ---------------- W18
say('W18')
DR = PG['DR']; eff_of = lambda cid: cid.split(':', 1)[1]; TR = ['一定', '上昇', '下降']
sel = {(r['id'], r['ctrl_trend']): r for r in DR if r['delta'] != '0'}; sel0 = {(r['id'], r['ctrl_trend']): r for r in DR if r['delta'] == '0'}
ids = sorted({r['id'] for r in DR}, key=lambda i: [c['id'] for c in CONTR].index(i)); effs = []
for i in ids:
    if eff_of(i) not in effs:
        effs.append(eff_of(i))
P('## W18. 効果種ごとの到達（札 D1 初段・Δ=±0.15・格子 DR 表から集計・Cl1 中7・Cl2 重大1・Cl3 重大3・Gr1 重大6・Gr2 重大3・Ge1 中5・Ge2 中4）'); P('')
P('| 効果種 | 対照の規模変化 | 場面ごとの値 | 平均 | 中央値 | 0.05 未満 |'); P('|---|---|---|---|---|---|')
for e in effs:
    for t in TR:
        vals = [(i.split(':')[0], sel[(i, t)]['card_D1_holm_first']) for i in ids if eff_of(i) == e]
        v = [x for _, x in vals]; P('| %s | %s | %s | %.3f | %.3f | %d/%d |' % (e, t, '・'.join('%s %.3f' % x for x in vals), statistics.mean(v), statistics.median(v), sum(x < 0.05 for x in v), len(v)))
P('')
for t in TR:
    v = [sel[(i, t)]['card_D1_holm_first'] for i in ids]; v0 = [sel0[(i, t)]['card_D1_holm_first'] for i in ids]
    P('- %s: 22 本の期待本数 %.2f（Δ=0 で %.3f）・中央値 %.3f・平均 %.3f・0.05 未満 %d 本・0.5 以上 %d 本。' % (t, sum(v), sum(v0), statistics.median(v), statistics.mean(v), sum(x < 0.05 for x in v), sum(x >= 0.5 for x in v)))
P('- 効果種ごとの「その効果種の対比のうち少なくとも 1 本が確証になる確率」（場面の独立を仮定・既測基底のある対比だけ・Cl2 重大1 の選択規則の読みの材料）: ' + '／'.join(
    '%s: %s' % (e, '・'.join('%s %.3f' % (t, 1 - float(np.prod([1 - sel[(i, t)]['card_D1_holm_first'] for i in ids if eff_of(i) == e]))) for t in TR)) for e in effs) + '。')
blind3 = [i for i in ids if all(sel[(i, t)]['card_D1_holm_first'] < 0.05 for t in TR)]
P('- 三型とも 0.05 未満の対比: %d 本（%s）。転記行 C の「片腕が既に閾外」6 本との関係: C の 6 本のうち三型とも 0.05 未満でないもの %s。' % (len(blind3), '・'.join(blind3), '・'.join('%s（%s）' % (i, '／'.join('%.3f' % sel[(i, t)]['card_D1_holm_first'] for t in TR)) for i in DF['C']['data']['one_arm_saturated_at_4B'] if i not in blind3) or 'なし'))
P('- 既測基底が無く格子に載らない対比: %d 本（%s）。' % (len(DF['B']['data']['missing_bases']), '・'.join(DF['B']['data']['missing_bases']))); P('')

# ---------------- W19
say('W19')
Bb = T['bases_4B2507_api']
P('## W19. Odose 系の対照 Onull の既測（Cl2 重大2）'); P('')
P('- Onull の 4B-2507 API 既測: ' + '・'.join('%s %d/%d（%.4f）' % (sc, Bb[sc]['Onull']['k'], Bb[sc]['Onull']['n'], Bb[sc]['Onull']['k'] / Bb[sc]['Onull']['n']) for sc in SC if 'Onull' in Bb[sc]) + '。')
P('- N の既測（参考）: ' + '・'.join('%s %d/%d（%.4f）' % (sc, Bb[sc]['N']['k'], Bb[sc]['N']['n'], Bb[sc]['N']['k'] / Bb[sc]['N']['n']) for sc in SC if 'N' in Bb[sc]) + '。Cl2 の「N2 0.925」は Onull ではなく N の N2 の値に一致する（Onull の N2 は 0.9906 で天井側）。')
P('- Odose1・Odosehalf の既測: %s。' % ('・'.join('%s: Odose1 %s・Odosehalf %s' % (sc, 'あり' if 'Odose1' in Bb[sc] else 'なし', 'あり' if 'Odosehalf' in Bb[sc] else 'なし') for sc in SC))); P('')

# ---------------- W20・W21
say('W20-21')
P('## W20. 様式門の見込みの材料（Cl1 中11・Gr1 中4）'); P('')
P('- 転記行 G の既測 (b) 率（段階 F の stageF1・4B-2507・U 腕）: %s。Onull の (b) 率の既測 %s。確証族で N を含む対比: %s。' % (json.dumps(DF['G']['data']['measured_b_rates'], ensure_ascii=False), 'あり' if any('Onull' in json.dumps(v, ensure_ascii=False) for v in DF['G']['data']['measured_b_rates'].values()) else 'なし', '・'.join(c['id'] for c in CONTR if 'N' in (c['A'], c['B'])))); P('')
P('## W21. 検閲の感度閾値の振れ（Cl1 中10）'); P('')
for r in PG['DS']:
    if r['pattern'] == 'floor_const' and r['d0_pt'] == 0 and r['delta_pt_32B_minus_4B'] == 0:
        P('- 閾値 %s／%s・対照が床（0.03）・d0=0・Δ=0: 判定不能 %.3f。' % (r['censor_low'], r['censor_high'], r['undecidable_censor']))
P('')

# ---------------- W22・W23
say('W22-23')
P('## W22. 費用の細部（Cl2 1-2・Cl3 軽15）'); P('')
GC['SF'] = dict(SF); eff32 = TPH['costpilot-A100'] * 17 / CAP; main32 = base_trials + anchor_trials; h32 = (main32 * SF['32B'] + 2 * n_cal * 1.0) / eff32 + 2 * SETUP['costpilot-A100'] / 3600
P('- 32B の上界: 器（校正腕を試行/時 %d で数える）%.2f ユニット・校正腕を 32B の同時要求数の処理量で数える Cl2 の式 %.2f ユニット（Cl2 の印字 136.8）。' % (TPH['costpilot-A100'], rows_u['32B']['units'], h32 * RATE['costpilot-A100']))
RPL = [("'hours': round(h_tot, 2)", "'hours': h_tot"), ("'units': round(h_tot * RATE[tg], 2)", "'units': h_tot * RATE[tg]")]
spm, spb = src_pm, src_pb
for o_, n_ in RPL:
    assert o_ in spm and o_ in spb; spm = spm.replace(o_, n_); spb = spb.replace(o_, n_)
GU = dict(GC, SF=dict(SF)); exec(spm, GU); exec(spb, GU)
hl_unr = sum(GU['plan_model'](m['key'], T['environments'][m['key']]['env'], T['environments'][m['key']]['concurrency'], 'lower')['hours'] for m in T['models']) + sum(GU['plan_bridge'](k, bc, 'lower')['hours'] for k, bc in T['bridge']['cells'].items())
hl_r2 = sum(v['hours'] for v in rows_l.values())
P('- 下界の時間の合計: 機種ごとに 2 桁で丸めた値の和 %.2f → 1 桁に丸めて %.1f（転記行 F の印字 %s）・丸めない和 %.4f。' % (hl_r2, round(hl_r2, 1), DF['F']['data']['plans']['lower']['hours'], hl_unr))
P('')
P('## W23. その他の照合（Cl3 軽微18・Gr1 軽微・Gr2 軽微・Cl1 軽12・軽13・Cl3 中10・中14・軽17・Cl1 0）'); P('')
dfl = src_df.split('\n'); l270 = [i + 1 for i, l in enumerate(dfl) if '上側は 1.0 を超える' in l]
P('- `design_facts_A.py` の「上側は 1.0 を超える」の句: 行 %s（書式文字列の固定句で、基底＋帯の計算からの assert は無い: %s）。' % (l270, 'assert' not in ''.join(dfl[i - 1] for i in l270)))
fz = re.search(r'zs = np\.array\(\[([^\]]+)\]\)', TX('tools', 'firth.py')); fzv = np.array([float(x) for x in fz.group(1).split(',')])
P('- `firth.py` の自己検査の z の直書き: [%s]・実パラメータ数からの z との差の最大 %.1e（丸め 4 桁）。' % (fz.group(1), float(np.max(np.abs(fzv - zs)))))
P('- `build_draft5A.py` の docstring の先頭: 「%s」。' % TX('tools', 'build_draft5A.py').split('\n')[1][:60])
P('- 草案6 §2.9 に「原因の探索は B の調整走行の情報状態欄」の句 %s。正本 `firth_check.status`＝「%s」・`judge_validity.scope_decided`＝%s。' % ('あり' if 'B の調整走行の情報状態欄' in DRAFT else 'なし', T['firth_check']['status'], T['judge_validity']['scope_decided']))
tracked = {}
for rel in ['records/A/power-grid-A.json', 'design/design-stageA-draft6.src.md', 'tools/cost_facts.py', 'tools/run_preamble_local.py', 'tools/colab/boot_cost_pilot.py', 'tools/bundle_prefreeze_A.py']:
    tracked[rel] = subprocess.run(['git', 'ls-files', '--error-unmatch', rel], cwd=REPO, capture_output=True).returncode == 0
P('- bundle に入れなかった一次記録のコミット済み（公開リポジトリにある）: ' + '・'.join('%s %s' % (k, v) for k, v in tracked.items()) + '。')
BUN = TX('records', 'reviews', 'A', 'prefreeze', 'bundle-A-prefreeze.md')
parts = re.findall(r'^  - .+? — `([^`]+)` — SHA16 ([0-9A-F]{16}) — ', BUN, re.M)
P('- bundle の部品の SHA16（見出しの記帳値と現在のファイル）: %d 部品のうち一致 %d。' % (len(parts), sum(SHA(rel) == h for rel, h in parts))); P('')

# ---------------- W24・W25
say('W24-25')
P('## W24. refuse 門の格子の配置（Gr1 中1・Gr2 中7）'); P('')
P('- 格子 R 節の配置: %s。' % ' ／ '.join(r['config'] for r in PG['R']))
P('- Lneg の API 既測: ' + '・'.join('%s 破局 %d/%d・refuse %d' % (sc, Bb[sc]['Lneg']['k'], Bb[sc]['Lneg']['n'], Bb[sc]['Lneg']['refuse']) for sc in SC if 'Lneg' in Bb[sc]) + '。門0 の手元 Lneg: ' + '・'.join('%s 破局 %s・refuse／書式外 %s' % (r[0].replace('costpilot-', ''), r[2].split('（')[0], r[5]) for r in bS if r[1] == 'Lneg') + '。'); P('')
P('## W25. 判定器の妥当性の規則（Gr1 中7）'); P('')
P('- 正本 `judge_validity` のキー: %s（κ の閾値・保留の規則のキー %s）。' % (list(T['judge_validity'].keys()), 'あり' if any(k in json.dumps(T['judge_validity'], ensure_ascii=False) for k in ('閾値', 'threshold', 'hold')) else 'なし')); P('')

# ---------------- W26
say('W26')
cl = DF['C']['data']['one_arm_saturated_at_4B']
P('## W26. 転記行 D の「尺度依存の穴」の行の真の pt 差（Cl1 中3・Cl2 3-2・Cl3 重大1）'); P('')
z4 = Z['4B']; zspan = float(zs[-1] - z4)
P('| 対照の型 | d0 | 切り詰めた規模 | 規模ごとの真の pt 差（pt） | 真の傾き（WLS・真の分散の重み・pt／z） | 真の傾き（OLS・pt／z） | 格子の札 草案4 名目／初段 → D1 名目／初段 |'); P('|---|---|---|---|---|---|---|')
for name, pc in (('ctrl_rising', np.linspace(0.3, 0.9, 6)), ('ctrl_falling', np.linspace(0.9, 0.3, 6))):
    for d0 in (0.05, 0.10, 0.15, 0.20, 0.30):
        raw = pc + d0; ptc = np.clip(raw, 0.001, 0.999); dd = ptc - pc; clipped = int(((raw > 0.999) | (raw < 0.001)).sum())
        w = 1 / ((pc * (1 - pc) + ptc * (1 - ptc)) / n); zb = (w * zs).sum() / w.sum(); sl_w = (w * (zs - zb) * dd).sum() / (w * (zs - zb) ** 2).sum()
        sl_o = np.polyfit(zs, dd, 1)[0]; g = next(r for r in PG['D'] if r['pattern'] == name and abs(r['d0_pt'] - d0) < 1e-9 and r['delta_pt_32B_minus_4B'] == 0)
        P('| %s | %.2f | %d | %s | %+.3f | %+.3f | %.3f／%.3f → %.3f／%.3f |' % (name, d0, clipped, '・'.join('%.1f' % (x * 100) for x in dd), sl_w * 100, sl_o * 100, g['card_draft4_nominal'], g['card_draft4_holm_first'], g['card_D1_nominal'], g['card_D1_holm_first']))
P('')
P('- 格子の D 表の上昇・Δ>0 の行（Cl1 の「ctrl_rising d0=0.05・Δ=0.10 で草案4 初段 0.788 → D1 初段 0.425」の照合）: ' + '・'.join('d0=%.2f・Δ=%.2f 切り詰め %d・草案4 初段 %.3f → D1 初段 %.3f' % (r['d0_pt'], r['delta_pt_32B_minus_4B'], r['clipped_sizes'], r['card_draft4_holm_first'], r['card_D1_holm_first']) for r in PG['D'] if r['pattern'] == 'ctrl_rising' and r['d0_pt'] in (0.0, 0.05) and r['delta_pt_32B_minus_4B'] in (0.10, 0.15) and 'dropped' not in r) + '。'); P('')

# ---------------- W32
say('W32')
rngm = np.random.default_rng([20260913, 32])


def holm_set(p):
    m_ = len(p); order = np.argsort(p); ok = p[order] <= ALPHA / (m_ - np.arange(m_)); k = int(np.cumprod(ok).sum()); s = np.zeros(m_, bool); s[order[:k]] = True
    return s


viol = 0; nb_ = 0; ns_ = 0; NIT = 100000
for _ in range(NIT):
    pb = rngm.random(M) ** rngm.uniform(1, 8); pp = rngm.random(M) ** rngm.uniform(1, 8); same = rngm.random(M) < 0.8
    ps = np.where(same, np.maximum(pb, pp), 1.0); Rb = holm_set(pb); Rs = holm_set(ps)
    viol += int((Rs & ~Rb).any()); nb_ += int(Rb.sum()); ns_ += int(Rs.sum())
P('## W32. Holm の単調性（第二部 W29 の (iii) を札の列に載せるときの整合の機械確認）'); P('')
P('- p*＝max(p_β, p_pt)（向きが違えば 1）は常に p* ≥ p_β。乱数 %s 回（%d 対比・p は一様乱数の 1〜8 乗）で「p* の Holm で棄却されたのに p_β の Holm では棄却されない対比がある」回: **%d**（1 回あたりの棄却の平均: p_β で %.2f 本・p* で %.2f 本）。(iii) の確証は β₃ の Holm の棄却の部分集合になり、「記述（対数オッズ尺度でのみ）」＝β₃ の Holm で棄却 ∧ p* の Holm で棄却されない、と一義に書ける。' % (format(NIT, ','), M, viol, nb_ / NIT, ns_ / NIT)); P('')

O += ['', '本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(a.out, 'w', encoding='utf-8', newline='\n').write('\n'.join(O) + '\n')
say('written %s (%d lines)' % (a.out, len(O)))
