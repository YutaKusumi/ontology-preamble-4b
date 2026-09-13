# -*- coding: utf-8 -*-
"""design_facts_A.py v2 —— 段階 A の設計事実（転記行 A〜N）を機械生成する（2026-09-13）。
入力: design/contrasts-A.json（正本）・records/A/power-grid-A.json（v2）・records/A/hf-models-A.json・records/cost-pilot/cost-facts-2026-09-13.md（U 表・R 表・G 行を解析）・records/F/style-stageF1.json（(b) 率の既測・記述）。
v2 の変更（claude.ai 三票の採否表 C12・C24〜C36・C45〜C46・登録者裁定 D1〜D3・D6・D7）: 書式文字列に手計算の数や評価語を置かない（数はスロット・設計定数も正本から読む）／格子の入力 SHA16 と z を assert／費用の係数は cost-facts を解析して読む／登録した同時要求数の収容を assert／費用は処理量の上界と下界・校正腕はセッションごと・橋は二機種の片側だけ／転記行 N（門0.5 の帰無の不合格率）を追加。
出力: records/A/design-facts-A.md と同 .json。
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, math, hashlib, datetime, argparse, statistics
from fractions import Fraction
from scipy.stats import binom
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--pg', default=os.path.join(REPO, 'records', 'A', 'power-grid-A.json')); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'design-facts-A'))
ap.add_argument('--allow-quick', action='store_true')
a = ap.parse_args()
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json')
J = lambda p: json.load(open(p, encoding='utf-8'))
T = J(CPATH); PG = J(a.pg); HF = J(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'))
sha_file = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
sha_str = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
assert PG.get('version') == 'v2', '格子は v2 が要る'
assert PG['inputs']['contrasts_sha16'] == sha_file(CPATH), ('格子の入力 SHA16 と現行の正本が不一致', PG['inputs']['contrasts_sha16'], sha_file(CPATH))
assert a.allow_quick or not PG.get('quick'), 'quick の格子は転記に使わない'
n, pn, n_id, n_cal = T['n_per_arm'], T['pilot_n'], T['identity_n'], T['calibration_n']
SC = T['scenarios']; ARMS = T['arms']['preamble']; SIZES = T['sizes']; MODELS = T['models']; FAM = T['families']['A_slope']; CONTR = FAM['contrasts']
lo, hi = T['censor']['low'], T['censor']['high']
F = {}
f3 = lambda v: '—' if v is None else '%.3f' % v
sci = lambda v: '%.2e' % v
CENSOR_LIKELY = 0.5   # 転記行 C の「検閲される見込み」の閾（記述の区切り）
CLAUSE_MAJORITY = 0.5   # 転記行 D: 解釈条項が当てはめの多数で発火する対比を数える区切り（記述）
LOSS_MARGIN = 0.1   # 転記行 D: 二尺度の規則で草案4 の規則より到達が下がる対比を数える区切り（記述）


# ---- z（格子と一致を assert）
def params(v):
    V, h, L, i, nh, nkv, hd = v['vocab_size'], v['hidden_size'], v['num_hidden_layers'], v['intermediate_size'], v['num_attention_heads'], v['num_key_value_heads'], v['head_dim']
    return V * h * (1 if v.get('tie_word_embeddings', False) else 2) + L * (h * nh * hd + 2 * h * nkv * hd + nh * hd * h + 2 * hd + 3 * h * i + 2 * h) + h


PAR = {k: params(v) for k, v in HF['models'].items()}
Z = {k: math.log(PAR[k] / PAR['4B']) for k in PAR}
for k in SIZES:
    assert abs(PG['z'][k] - Z[k]) < 1e-9, ('格子の z が実パラメータ数の z と不一致', k)

# ---- L: 容量と収容（登録値を assert）
CR = T['capacity_rule']; ENVS = T['environments']; GG = HF['gpu_gib']
KV = {k: 2 * v['num_hidden_layers'] * v['num_key_value_heads'] * v['head_dim'] * 2 * CR['kv_tokens_per_request'] / 2**30 for k, v in HF['models'].items()}
cmax = lambda k, G: int(math.floor((CR['gpu_fraction'] * G - HF['models'][k]['safetensors_gib'] - CR['overhead_gib']) / KV[k]))
GPUS = [('L4', GG['L4']), ('A100 40GB', GG['A100-40GB']), ('A100 80GB', GG['A100-80GB'])]; GMAP = {24: GG['L4'], 40: GG['A100-40GB'], 80: GG['A100-80GB']}
Ld = {}; parts = []
for m in MODELS:
    k = m['key']; e = ENVS[k]; c = {nm: max(0, min(CR['concurrency_cap'], cmax(k, G))) for nm, G in GPUS}
    assert 0 < e['concurrency'] <= min(CR['concurrency_cap'], cmax(k, GMAP[e['memory_class_gb']])), ('登録の同時要求数が収容を超える', k)
    extra = ''
    if 'if_40GB' in e:
        if e['if_40GB'] is None:
            extra += '・40GB では走らせない'
        else:
            assert e['if_40GB']['concurrency'] <= cmax(k, GMAP[e['if_40GB']['memory_class_gb']]), ('40GB の同時要求数が収容を超える', k); extra += '・40GB では同時 %d' % e['if_40GB']['concurrency']
    if e.get('if_not_80GB'):
        g = e['if_not_80GB']; assert g['concurrency'] <= cmax(k, GMAP[g['memory_class_gb']]), ('第三の環境の同時要求数が収容を超える', k)
        extra += '・80GB が割り当てられなければ環境値「%s」（%s・同時 %d）' % (g['env'], g['gpu'], g['concurrency'])
    Ld[k] = {'rev': HF['models'][k]['rev'], 'params_M': round(PAR[k] / 1e6, 1), 'z': round(Z[k], 4), 'weights_gib': HF['models'][k]['safetensors_gib'], 'kv_per_request_gib': round(KV[k], 4), 'max_concurrency': c, 'registered': e}
    parts.append('%s: rev %s・%s M params・z=%+.4f・重み %.2f GiB・KV／要求 %.4f GiB・最大同時（L4／A100 40GB／A100 80GB）%d／%d／%d・登録 %s %dGB 同時 %d%s' % (
        k, HF['models'][k]['rev'], Ld[k]['params_M'], Z[k], HF['models'][k]['safetensors_gib'], KV[k], c['L4'], c['A100 40GB'], c['A100 80GB'], e['env'], e['memory_class_gb'], e['concurrency'], extra))
bparts = []
for k, bc in T['bridge']['cells'].items():
    G = GG['L4'] if bc['bridge_env'] == 'L4' else GG['A100-40GB']
    assert bc['bridge_concurrency'] <= min(CR['concurrency_cap'], cmax(k, G)), ('橋の同時要求数が収容を超える', k)
    bparts.append('%s の %s 側 同時 %d（最大 %d・A100 側は 40GB で検査）' % (k, bc['bridge_env'], bc['bridge_concurrency'], min(CR['concurrency_cap'], cmax(k, G))))
F['L'] = {'text': '機種別の容量と収容（HF 取得 %s・実パラメータ数は config.json から機械計算・収容規則＝重み＋KV〔要求あたり %s トークン × 同時要求数〕＋%s GiB が GPU メモリの %s 以内・GPU メモリは hf-models-A.json の gpu_gib〔L4 %s・A100 40GB %s・A100 80GB %s GiB〕・同時要求数の上限 %d・登録値の収容は assert 済み）: ' % (
    HF['fetched_utc'], format(CR['kv_tokens_per_request'], ','), CR['overhead_gib'], CR['gpu_fraction'], GG['L4'], GG['A100-40GB'], GG['A100-80GB'], CR['concurrency_cap']) + '／'.join(parts) + '。橋: ' + '・'.join(bparts) + '。', 'data': Ld}

# ---- F: 費用（cost-facts を解析）
CF_PATH = os.path.join(REPO, re.search(r'records/[\w\-./]+\.md', T['cost']['source']).group(0)); CFt = open(CF_PATH, encoding='utf-8').read()


def md_table(text, prefix):
    lines = text.split('\n'); i0 = next(j for j, l in enumerate(lines) if l.startswith(prefix)); rows = []; started = False
    for l in lines[i0 + 1:]:
        if l.startswith('|'):
            started = True; rows.append([x.strip() for x in l.strip().strip('|').split('|')])
        elif started:
            break
    return rows[0], rows[2:]


hU, bU = md_table(CFt, '## U.'); hR, bR = md_table(CFt, '## R.')
col = lambda h, s: next(i for i, x in enumerate(h) if x.startswith(s))
SETUP = {r[0]: float(r[col(hU, '経費合計')]) for r in bU}; GPUN = {r[0]: r[col(hU, 'GPU')] for r in bU}
TPH = {r[0]: float(r[col(hR, '試行／時')]) for r in bR}; WORK = {r[0]: int(r[col(hR, 'workers')]) for r in bR}; RATE = {r[0]: float(r[col(hR, '実測の時間あたりユニット')]) for r in bR}
TAG = {'L4': 'costpilot-L4', 'A100': 'costpilot-A100'}
for env, tg in TAG.items():
    assert WORK[tg] == CR['concurrency_cap'], ('門0 の同時要求数と上限が不一致', tg)
EST = [int(x) for x in re.findall(r'A＋B 見込み (\d+) ユニット', CFt)]
C = T['cost']; SF = C['size_factor_assumption']; SH = C['session_h']; CAP = CR['concurrency_cap']; AB = T['anchor_band']
anchor_trials = len(AB['scenarios']) * len(AB['arms']) * n; base_trials = len(SC) * len(ARMS) * (pn + n)


def plan_model(k, env, conc, bound):
    tg = TAG[env]; tph = TPH[tg]; st = SETUP[tg] / 3600; eff = tph * (conc / CAP if bound == 'upper' else 1.0)
    main = base_trials + (anchor_trials if k in AB['models'] else 0); sess = 1; h_run = 0.0
    for _ in range(60):
        h_run = main * SF[k] / eff + sess * n_cal * SF[T['calibration']['model']] / tph
        new = max(1, math.ceil(h_run / (SH - st)))
        if new == sess:
            break
        sess = new
    h_tot = h_run + sess * st
    return {'env': env, 'concurrency': conc, 'trials': main + sess * n_cal, 'hours': round(h_tot, 2), 'sessions': sess, 'units': round(h_tot * RATE[tg], 2), 'last_session_margin': round((sess * (SH - st) - h_run) / (SH - st), 3)}


def plan_bridge(k, bc, bound):
    env = bc['bridge_env']; tg = TAG[env]; tph = TPH[tg]; st = SETUP[tg] / 3600; eff = tph * (bc['bridge_concurrency'] / CAP if bound == 'upper' else 1.0)
    tr = len(T['bridge']['arms']) * T['bridge']['n']; h_run = tr * SF[k] / eff; sess = max(1, math.ceil(h_run / (SH - st))); h_tot = h_run + sess * st
    return {'env': env, 'concurrency': bc['bridge_concurrency'], 'trials': tr, 'hours': round(h_tot, 2), 'sessions': sess, 'units': round(h_tot * RATE[tg], 2)}


plans = {}
for bound in ('upper', 'lower'):
    rows = {m['key']: plan_model(m['key'], ENVS[m['key']]['env'], ENVS[m['key']]['concurrency'], bound) for m in MODELS}
    for k, bc in T['bridge']['cells'].items():
        rows['橋 %s（%s 側）' % (k, bc['bridge_env'])] = plan_bridge(k, bc, bound)
    plans[bound] = {'rows': rows, 'units': round(sum(v['units'] for v in rows.values()), 1), 'hours': round(sum(v['hours'] for v in rows.values()), 1), 'trials': sum(v['trials'] for v in rows.values())}
alt40 = {}
for m in MODELS:
    e = ENVS[m['key']]
    if 'if_40GB' in e:
        alt40[m['key']] = None if e['if_40GB'] is None else plan_model(m['key'], e['env'], e['if_40GB']['concurrency'], 'upper')
tgL = TAG['L4']; g05_tr = n_id * len(ARMS); g05_h = g05_tr / TPH[tgL] + SETUP[tgL] / 3600
margin = min((v['last_session_margin'], k) for k, v in plans['upper']['rows'].items() if 'last_session_margin' in v)
stop_thr = plans['upper']['units'] * C['stop_rule']['multiplier']
row_txt = lambda k, v: '%s（%s・同時 %d）%s 試行・%.1f h・%d セッション・%.1f ユニット' % (k, v['env'], v['concurrency'], format(v['trials'], ','), v['hours'], v['sessions'], v['units'])
F['F'] = {'text': ('費用と時間（門0 の実測: L4 %.2f ユニット/h・%s 試行/h・経費 %d s／A100〔%s〕%.2f ユニット/h・%s 試行/h・経費 %d s・門0 の同時要求 %d・4B 比の試行時間の仮定 %s ◐・セッション %s 時間・校正腕は %s の係数）: '
                   '**上界**（処理量 ∝ 同時要求数）: %s。**上界の合計 %s 試行・%.1f 時間・%.1f ユニット**。下界（同時要求数で処理量が落ちない）の合計 %.1f 時間・%.1f ユニット。'
                   'A100 40GB が割り当てられた場合（上界）: %s。最後のセッションの余裕の最小 %.3f（%s）。停止規則: パイロット後の見込みが上界の %s 倍（%.1f ユニット）を超えたら本走行の前に登録者が再裁定。'
                   '門0 の判定時の A＋B 見込み %s ユニットに対し、A の上界は %.2f 倍。門0.5（n=%d × %d 腕・L4・vLLM）%s 試行・%.2f h・%.2f ユニット。API 再走行・判定器の断片・機種の切替の経費は含まない。パイロットで機種ごとの実測に置き換える。') % (
    RATE[TAG['L4']], format(int(TPH[TAG['L4']]), ','), SETUP[TAG['L4']], GPUN[TAG['A100']], RATE[TAG['A100']], format(int(TPH[TAG['A100']]), ','), SETUP[TAG['A100']], WORK[TAG['L4']], json.dumps(SF, ensure_ascii=False), SH, T['calibration']['model'],
    '／'.join(row_txt(k, v) for k, v in plans['upper']['rows'].items()), format(plans['upper']['trials'], ','), plans['upper']['hours'], plans['upper']['units'], plans['lower']['hours'], plans['lower']['units'],
    '／'.join(('%s は走らせない' % k) if v is None else row_txt(k, v) for k, v in alt40.items()), margin[0], margin[1], C['stop_rule']['multiplier'], stop_thr,
    '〜'.join(str(x) for x in sorted(set(EST))), plans['upper']['units'] / max(EST), n_id, len(ARMS), format(g05_tr, ','), g05_h, g05_h * RATE[tgL]),
    'data': {'plans': plans, 'alt_40GB_upper': alt40, 'stop_threshold_units': round(stop_thr, 1), 'gate05': {'trials': g05_tr, 'hours': round(g05_h, 2), 'units': round(g05_h * RATE[tgL], 2)}, 'gate0_estimates_AB': EST}}

# ---- A: 規模
t_id = n_id * len(ARMS); t_pilot = len(MODELS) * len(SC) * len(ARMS) * pn; t_main = len(MODELS) * len(SC) * len(ARMS) * n
t_anchor = len(AB['models']) * anchor_trials; sess_up = sum(plans['upper']['rows'][m['key']]['sessions'] for m in MODELS); t_cal = sess_up * n_cal
t_bridge = len(T['bridge']['cells']) * len(T['bridge']['arms']) * T['bridge']['n']; t_api = len(T['seeds']['api_rerun']) * len(ARMS) * n
t_total = t_id + t_pilot + t_main + t_anchor + t_cal + t_bridge
F['A'] = {'text': '規模: 門0.5 同一性選別 %s（%s × %d 腕 × n=%d）／パイロット %s（%d 機種 × %d 場面 × %d 腕 × n=%d）／本走行 %s（%d 機種 × %d 場面 × %d 腕 × n=%d）／錨反復 %s（%d 規模 × %d 場面 × %d 腕 × n=%d）／校正腕 %s（機種のセッションごとに n=%d・転記行 F の上界のセッション数の合計 %d）／橋 %s（%s × %d 腕 × n=%d・場面 %s・各機種の本走行の %s と対にする）＝**手元合計 %s 試行**。API 再走行（門0.5 合格時のみ）%s（%s × %s × %d 腕 × n=%d）。' % (
    format(t_id, ','), T['identity_screen']['scenario'], len(ARMS), n_id, format(t_pilot, ','), len(MODELS), len(SC), len(ARMS), pn, format(t_main, ','), len(MODELS), len(SC), len(ARMS), n,
    format(t_anchor, ','), len(AB['models']), len(AB['scenarios']), len(AB['arms']), n, format(t_cal, ','), n_cal, sess_up,
    format(t_bridge, ','), '・'.join('%s の %s 側' % (k, v['bridge_env']) for k, v in T['bridge']['cells'].items()), len(T['bridge']['arms']), T['bridge']['n'], T['bridge']['scenario'], T['bridge']['scenario'],
    format(t_total, ','), format(t_api, ','), '・'.join(T['seeds']['api_rerun']), T['bridge']['scenario'], len(ARMS), n),
    'data': {'identity': t_id, 'pilot': t_pilot, 'main': t_main, 'anchor_rerun': t_anchor, 'calibration': t_cal, 'bridge': t_bridge, 'total_local': t_total, 'api_rerun': t_api}}

# ---- B: 対比と整合
D_ = T['descriptive_families']; I_ = T['integrity']
meas = [c for c in CONTR if c['base_A_4B2507'] is not None and c['base_B_4B2507'] is not None]; miss = [c for c in CONTR if c not in meas]
dose = [c for c in miss if c['A'].startswith('Odose')]; other = [c for c in miss if not c['A'].startswith('Odose')]
used = {c['A'] for c in CONTR} | {c['B'] for c in CONTR}; not_in = [x for x in ARMS if x not in used]
assert {'O', 'Osec', 'Nk'} <= set(not_in), '床持続の腕が確証族に現れている'
F['B'] = {'text': '対比: 確証 %d（傾きの族・%d 効果種 × %d 場面・m=%d 固定・両側・二尺度の IUT）・記述（Nstr−Onull %d・Ncold−N %d・床持続 %d セル列〔%d セル〕・レシピ対 %d・様式／錨差／スタック差／環境差／対数オッズ尺度でのみ立った対比は走行後に生成）。整合検査（正本の生成時）: id の重複 %d・対比が要求する腕の台帳での不在 %d・登録対比を持たない腕 %d・台帳に無い腕 %d。確証 %d 本のうち 4B-2507 の API 既測で両腕の基底を持つもの %d・欠くもの %d（Odose1・Odosehalf 系 %d 本＋その他 %d 本: %s）。確証族に一度も現れない腕: %s（O・Osec・Nk は床持続の記述降格の帰結・Ncold と Nstr は記述の設計）。' % (
    len(CONTR), FAM['effect_types'], len(SC), FAM['m'], len(D_['A_desc_nstr']['contrasts']), len(D_['A_desc_ncold']['contrasts']), D_['A_desc_floor']['cell_series'], len(D_['A_desc_floor']['cells']), len(D_['A_desc_recipe']['contrasts']),
    I_['id_duplicates'], len(I_['arms_required_missing']), len(I_['arms_without_contrast']), len(I_['arms_not_in_ledger']), len(CONTR), len(meas), len(miss), len(dose), len(other), '・'.join(c['id'] for c in other), '・'.join(not_in)),
    'data': {'confirmed': len(CONTR), 'measured_bases': len(meas), 'missing_bases': [c['id'] for c in miss], 'arms_not_in_confirm_family': not_in}}

# ---- C: 検閲
klo = math.ceil(Fraction(str(lo)) * n) - 1; khi = math.floor(Fraction(str(hi)) * n) + 1
cens2 = lambda pa, pb: float(binom.cdf(klo, n, pa) * binom.cdf(klo, n, pb) + binom.sf(khi - 1, n, pa) * binom.sf(khi - 1, n, pb))
GRID_P = [0.02, 0.05, 0.20, 0.50, 0.80, 0.95, 0.98]
sat_ids = []; cens_hi = []
for c in meas:
    ra = c['base_A_4B2507'] / c['base_n_A']; rb = c['base_B_4B2507'] / c['base_n_B']
    if ra < lo or ra > hi or rb < lo or rb > hi:
        sat_ids.append(c['id'])
    if cens2(ra, rb) > CENSOR_LIKELY:
        cens_hi.append(c['id'])
F['C'] = {'text': '検閲の誤判率（両腕条件・n=%d・規模単位・率 <%s は X ≤ %d・率 >%s は X ≥ %d・厳密二項）: 帰無（両腕が同じ基底 p）で落ちる確率は %s。4B-2507 の API 既測の基底で、4B の規模で検閲される確率が %s を超える確証対比 %d 本%s。**片腕が既に閾外（<%s または >%s）にある確証対比 %d 本**: %s（ほかに %d 規模で同じ腕が閾外になれば解釈条項が発火する）。残った規模の一覧は報告で機械印字する。' % (
    n, lo, klo, hi, khi, '・'.join('p=%s で %.3f' % (p, cens2(p, p)) for p in GRID_P), CENSOR_LIKELY, len(cens_hi), ('（' + '・'.join(cens_hi) + '）') if cens_hi else '', lo, hi, len(sat_ids), '・'.join(sat_ids),
    FAM['interpretation_clause']['min_sizes'] - 1), 'data': {'one_arm_saturated_at_4B': sat_ids, 'censor_likely_at_4B': cens_hi}}

# ---- D: 傾きの族の格子
PL = {'mid_const': '対照中間', 'floor_const': '対照が床', 'ceiling_const': '対照が天井', 'ctrl_rising': '対照が上昇', 'ctrl_falling': '対照が下降'}


def sel(pat, d0, D):
    for r in PG['D']:
        if r['pattern'] == pat and abs(r['d0_pt'] - d0) < 1e-9 and abs(r['delta_pt_32B_minus_4B'] - D) < 1e-9:
            return r
    raise KeyError((pat, d0, D))


def pdesc(nm):
    v = PG['patterns'][nm]['ctrl']; return '%s（%s）' % (PL[nm], ('%g' % v[0]) if v[0] == v[-1] else '%g→%g' % (v[0], v[-1]))


D0V = PG['d0_values']; DV = PG['delta_values']; DREF = PG['real_base']['delta']
s_size = '・'.join('%s %.3f〔条件付き %s・n_fit %d・判定不能 %.3f・非収束 %.3f〕' % (pdesc(nm), r['reject_nominal'], f3(r['reject_nominal_conditional']), r['n_fit'], r['undecidable_censor'], r['nonconverged']) for nm in PG['patterns'] for r in [sel(nm, 0.0, 0.0)])
rm = [sel('mid_const', 0.0, D) for D in DV if D > 0]
s_pow = '%s・Δ=%s pt の札 D1（初段）%s・札 D1（名目）%s・草案4 の規則の初段 %s' % (pdesc('mid_const'), '／'.join('%g' % (D * 100) for D in DV if D > 0), '／'.join('%.3f' % r['card_D1_holm_first'] for r in rm), '／'.join('%.3f' % r['card_D1_nominal'] for r in rm), '／'.join('%.3f' % r['card_draft4_holm_first'] for r in rm))


def ptconst(nm):
    out = []
    for d0 in D0V:
        if d0 == 0:
            continue
        r = sel(nm, d0, 0.0)
        out.append(('d0=%g pt は外した' % (d0 * 100)) if 'dropped' in r else ('d0=%g pt で %.3f／%.3f → %.3f／%.3f' % (d0 * 100, r['card_draft4_nominal'], r['card_draft4_holm_first'], r['card_D1_nominal'], r['card_D1_holm_first'])))
    return '・'.join(out)


s_hole = 'pt 差が全規模で一定（Δ=0）の配置での札（草案4 の規則の名目／初段 → 裁定 D1 の名目／初段）は、%s: %s、%s: %s' % (pdesc('ctrl_rising'), ptconst('ctrl_rising'), pdesc('ctrl_falling'), ptconst('ctrl_falling'))
fr = sel('floor_const', 0.0, DREF); cr = sel('ceiling_const', 0.0, DREF)
s_fc = '%s・Δ=%g pt の札 D1（初段）%s（判定不能 %s・解釈条項 %s）／%s・Δ=%g pt（処置が下がる向き）の札 D1（初段）%s（判定不能 %s・解釈条項 %s）' % (
    pdesc('floor_const'), DREF * 100, f3(fr.get('card_D1_holm_first')), f3(fr.get('undecidable_censor')), f3(fr.get('clause_rate_among_fit')), pdesc('ceiling_const'), DREF * 100, f3(cr.get('card_D1_holm_first')), f3(cr.get('undecidable_censor')), f3(cr.get('clause_rate_among_fit')))
dropped = [r for r in PG['D'] if 'dropped' in r]
s_drop = '全規模が上限・下限に切り詰められて格子から外した行 %d（%s）' % (len(dropped), '・'.join('%s d0=%g Δ=%g' % (PL[r['pattern']], r['d0_pt'] * 100, r['delta_pt_32B_minus_4B'] * 100) for r in dropped) or 'なし')
DRr = PG['DR']; dl1 = sorted({r['delta'] for r in DRr} - {'0'})[0]; nDR = len({r['id'] for r in DRr}); dparts = []
for tr in ('一定', '上昇', '下降'):
    r0 = [r for r in DRr if r['ctrl_trend'] == tr and r['delta'] == '0']; r1 = [r for r in DRr if r['ctrl_trend'] == tr and r['delta'] == dl1]
    mx = max(r0, key=lambda r: r['card_D1_holm_first']); mx4 = max(r0, key=lambda r: r['card_draft4_nominal']); mn = min(r1, key=lambda r: r['card_D1_holm_first'])
    dparts.append('対照の規模変化 %s（32B−4B %+g pt）: Δ=0 で札 D1（初段）の最大 %.3f（%s）・期待本数 %.3f・少なくとも 1 本 %.3f（独立を仮定）・草案4 の規則（名目）の最大 %.3f（%s）・期待本数 %.3f・判定不能の期待本数 %.2f／Δ=%s で札 D1（初段）の中央値 %.3f・平均 %.3f（草案4 の規則の初段の平均 %.3f）・最小 %.3f（%s）・解釈条項が当てはめの %s 以上で発火する対比 %d 本・草案4 の規則の初段から %s 以上下がる対比 %d 本' % (
        tr, r0[0]['ctrl_change_32B_minus_4B'] * 100, mx['card_D1_holm_first'], mx['id'], sum(r['card_D1_holm_first'] for r in r0), 1 - math.prod(1 - r['card_D1_holm_first'] for r in r0),
        mx4['card_draft4_nominal'], mx4['id'], sum(r['card_draft4_nominal'] for r in r0), sum(r['undecidable_censor'] for r in r0), dl1, statistics.median(r['card_D1_holm_first'] for r in r1), statistics.mean(r['card_D1_holm_first'] for r in r1), statistics.mean(r['card_draft4_holm_first'] for r in r1), mn['card_D1_holm_first'], mn['id'],
        CLAUSE_MAJORITY, sum(1 for r in r1 if (r['clause_rate_among_fit'] or 0) >= CLAUSE_MAJORITY), LOSS_MARGIN, sum(1 for r in r1 if r['card_draft4_holm_first'] - r['card_D1_holm_first'] >= LOSS_MARGIN)))
s_dr = '両腕の既測基底を持つ %d 本の 4B の実基底を入力にすると（B=%d）、%s。既測基底の無い %d 本は格子に載せない' % (nDR, PG['B']['DR'], '／'.join(dparts), len(CONTR) - nDR)
DSr = PG['DS']; sparts = []
for slo_, shi_ in zip(T['censor']['sensitivity']['low'], T['censor']['sensitivity']['high']):
    g = lambda nm, d0, D: next((r for r in DSr if abs(r['censor_low'] - slo_) < 1e-9 and abs(r['censor_high'] - shi_) < 1e-9 and r['pattern'] == nm and abs(r['d0_pt'] - d0) < 1e-9 and abs(r['delta_pt_32B_minus_4B'] - D) < 1e-9), {})
    sparts.append('閾値 %g／%g で %s・Δ=%g pt の札 D1（初段）%s・%s・d0=%g pt・Δ=0 の札 D1（名目）%s・%sの判定不能 %s' % (slo_, shi_, PL['mid_const'], DREF * 100, f3(g('mid_const', 0.0, DREF).get('card_D1_holm_first')), PL['ctrl_rising'], DREF * 100, f3(g('ctrl_rising', DREF, 0.0).get('card_D1_nominal')), PL['floor_const'], f3(g('floor_const', 0.0, 0.0).get('undecidable_censor'))))
s_ds = '検閲の感度閾値（B=%d）: %s' % (PG['B']['DS'], '／'.join(sparts))
s_r = 'refuse 門（B=%d）: %s' % (PG['B']['R'], '／'.join('%s: 名目有意 %.3f・そのうち保留 %s（(a) %s・(b) %s・(c) %s・(d) %s）・札 D1（初段）は門の前 %.3f・門のあと %.3f' % (
    r['config'], r['nominal_significant'], f3(r['hold_among_nominal']), f3(r['hold_a_among_nominal']), f3(r['hold_b_among_nominal']), f3(r['hold_c_among_nominal']), f3(r['hold_d_among_nominal']), r['card_D1_holm_first_without_gate'], r['card_D1_holm_first_after_gate']) for r in PG['R']))
F['D'] = {'text': '傾きの族（Firth PPLRT 両側・n=%d × %d 規模・両腕条件の検閲・率は B 回あたりの無条件率・B=%d・seed %d・子ストリーム %d・z は転記行 L の実値〔一致を assert〕・札 D1＝β₃ と pt 差の傾きが同じ水準で同じ向き〔二尺度の IUT・登録者裁定 D1〕・初段＝Holm 初段 α/%d）。**Δ=0・d0=0 の棄却率**: %s。**検出力**: %s。**尺度依存の穴**: %s。%s。%s。**実基底**: %s。%s。%s。' % (
    n, len(SIZES), PG['B']['D'], PG['seed'], PG['streams']['D'], FAM['m'], s_size, s_pow, s_hole, s_fc, s_drop, s_dr, s_ds, s_r), 'data_ref': 'records/A/power-grid-A.json'}

# ---- E: 床持続
E = PG['E']; cs = D_['A_desc_floor']['cell_series']
F['E'] = {'text': '床持続（記述）の到達可能性（n=%d・棄却域 k≤%d〔CP 片側上限 <%s・境界での実サイズ %.4f〕）: 真の率 %s で 単一セル %s・%d 規模同時 %s・Holm 初段（k≤%d・m=%d のとき）%s。記述に降格したため多重補正は課さず、各セルの CP 上限と全規模 0/1 を印字する。0/1 が 0 であることを「床を離れた」と読まない。' % (
    n, E['k_max_cp95'], lo, E['size_at_k_max'], '／'.join('%g' % r['true_rate'] for r in E['rows']), '／'.join('%.3f' % r['single_cell'] for r in E['rows']), len(SIZES), '／'.join('%.4f' % r['six_sizes_joint'] for r in E['rows']),
    E['k_max_holm_first_m15'], cs, '／'.join('%.6f' % r['holm_first_six'] for r in E['rows'])), 'data': E}

# ---- G: 様式門
G_ = PG['G']; SG = T['style_gate']; style_meas = {}
sp = os.path.join(REPO, 'records', 'F', 'style-stageF1.json')
if os.path.isfile(sp):
    S = J(sp)
    for scn, arms_ in S['runs'].items():
        for arm, v in arms_.items():
            if arm in ARMS and isinstance(v, dict) and v.get('b_rate_final') is not None:
                style_meas.setdefault(scn, {})[arm] = v['b_rate_final']
F['G'] = {'text': '様式門（(a)(b) の差・二項の差・n=%d 同士・「超」・厳密）の帰無発火率: 注（%d pt 超）%s・判定保留（%d pt 超）%s。既測の (b) JSON 直答率（段階 F の stageF1・4B-2507・U 腕・記述）: %s。腕別・規模別の (b) 率と一斉保留の見込み本数はパイロット後に記述として報告し、閾値は動かさない（登録者裁定 D6）。' % (
    n, SG['note_pt'], '・'.join('p=%s で %s' % (p, sci(v)) for p, v in G_['bands'][str(SG['note_pt'])].items()), SG['hold_pt'], '・'.join('p=%s で %s' % (p, sci(v)) for p, v in G_['bands'][str(SG['hold_pt'])].items()),
    '／'.join('%s: %s' % (scn, '・'.join('%s %.3f' % (arm, r) for arm, r in d.items())) for scn, d in style_meas.items()) or '取得できず'), 'data': {'null': G_, 'measured_b_rates': style_meas}}

# ---- H: 錨帯
H = PG['H']; bands = sorted(H['bands'], key=int); rt = str(AB['rule_true_rate'])
F['H'] = {'text': '錨帯（%s × %d 規模 × %d 場面 × %d 走行・n=%d・「超」・厳密）: 腕あたりの帰無発火率（真の率 %s・超／以上）%s。除外単位（規模 × 場面＝%d）あたり %s、期待誤除外数 %s、少なくとも 1 単位 %s、4B-2507 の API 既測の基底での期待誤除外数 %s。検出側（走行間の真の drift・真の率 %s 付近）: %s。**登録値 %d pt**。規則（真の率 %s で期待誤除外数 %s 以下）を満たす最小の帯 %s pt・登録値は規則を満たす: %s（値は登録者確認 2026-09-13・規約と根拠は登録者裁定 D2）。' % (
    '・'.join(AB['arms']), len(AB['models']), len(AB['scenarios']), AB['runs'], n, rt, '・'.join('%s pt %s／%s' % (b, sci(H['bands'][b]['per_pair'][rt]['strict']), sci(H['bands'][b]['per_pair'][rt]['ge'])) for b in bands), H['units'],
    '／'.join('%s pt %.4f' % (b, H['bands'][b]['per_unit_at_05']) for b in bands), '／'.join('%s pt %.2f' % (b, H['bands'][b]['expected_false_exclusions_at_05']) for b in bands),
    '／'.join('%s pt %.3f' % (b, H['bands'][b]['p_any_false_exclusion_at_05']) for b in bands), '／'.join('%s pt %.2f' % (b, H['bands'][b]['expected_false_exclusions_at_measured_bases']) for b in bands), rt,
    '・'.join('%s pt の帯で %s' % (b, '／'.join('drift %s pt %.3f' % (dl, v) for dl, v in H['bands'][b]['detection_by_drift_pt'].items())) for b in bands), AB['band_pt'], rt, AB['rule_expected_max'], H['smallest_band_meeting_rule'], H['registered_meets_rule']), 'data': H}

# ---- I: 校正腕・撤退条件・門2
I2 = PG['I']; cp = I2['calibration_pass']; cf = I2['calibration_fail_local']; wd = I2['withdrawal']; g2 = I2['gate2']; CAL = T['calibration']
F['I'] = {'text': '校正腕（%s × %s × %s・n=%d・「超」・厳密）: 合格枝＝API 既測 %.3f に対し下側 %d pt（上側は 1.0 を超える）→ 発火 X ≤ %d・帰無発火率 %s・検出 %s。不合格枝＝手元系列の初点を本走行の最初のセッションの校正腕（n=%d）とする二標本・両側 %d pt → 帰無発火率 %s・検出 %s（参考: 初点を門0.5 の n=%d にした場合の帰無発火率 %s）。撤退条件（パイロット n=%d・%d pt・同じ API 既測）: 発火 X ≤ %d・帰無発火率 %s・検出 %s。門2（n=%d）の検閲の整数境界: 率 <%s は X ≤ %d・率 >%s は X ≥ %d・両腕が同じ p のとき落ちる確率 %s。' % (
    CAL['model'], CAL['arm'], CAL['scenario'], cp['n'], cp['base_api'], cp['band_pt'], cp['fire_if_le'], sci(cp['null']), '・'.join('真の率 %s で %.3f' % (p, v) for p, v in cp['detection'].items()),
    cf['n_first'], cf['band_pt'], '・'.join('真の率 %s で %s' % (p, sci(v)) for p, v in cf['null'].items()), '・'.join('0.95 から %s pt 下で %.3f' % (dl, v) for dl, v in cf['detection_from_095'].items()),
    cf['if_first_point_were_gate05']['n_first'], '・'.join('真の率 %s で %s' % (p, sci(v)) for p, v in cf['if_first_point_were_gate05']['null'].items()),
    wd['n'], wd['band_pt'], wd['fire_if_le'], sci(wd['null']), '・'.join('真の率 %s で %.3f' % (p, v) for p, v in wd['detection'].items()),
    g2['n'], lo, g2['censor_low_if_le'], hi, g2['censor_high_if_ge'], '・'.join('p=%s で %s' % (p, sci(v)) for p, v in g2['null_both_arms_same_p'].items())), 'data': I2}

# ---- J: 器材
TOOLS_NOW = [('make_contrasts_A.py', 'tools/make_contrasts_A.py'), ('firth.py', 'tools/firth.py'), ('power_grid_A.py', 'tools/power_grid_A.py'), ('design_facts_A.py', 'tools/design_facts_A.py'),
             ('numbers_lint.py', 'tools/numbers_lint.py'), ('build_draft5A.py', 'tools/build_draft5A.py'), ('firth_check_A.py', 'tools/firth_check_A.py'), ('firth_check_A.R', 'tools/firth_check_A.R'),
             ('cost_facts.py', 'tools/cost_facts.py'), ('run_preamble_local.py', 'tools/run_preamble_local.py'), ('boot_cost_pilot.py', 'tools/colab/boot_cost_pilot.py')]
PLANNED = ['boot_stageA.py', 'identity_screen_A.py', 'analyze_A.py', 'calib_band_A.py', 'gate_A.py', 'control_chart_A.py', 'integrity_A.py', 'sample_inspection_A.py', 'synth_A.py', 'build_report_A.py', 'report_lint.py', 'freeze_A.py']
exist = [(nm, sha_file(os.path.join(REPO, p))) for nm, p in TOOLS_NOW if os.path.isfile(os.path.join(REPO, p))]
still = [nm for nm, p in TOOLS_NOW if not os.path.isfile(os.path.join(REPO, p))] + [nm for nm in PLANNED if not os.path.isfile(os.path.join(REPO, 'tools', nm))] + ['報告雛形']
F['J'] = {'text': '凍結射程と器材の対応表: 腕・場面・環境・同時要求数・帯・規則→contrasts-A.json／走行→run_preamble_local.py v2.7・boot_stageA.py／門0.5→identity_screen_A.py／検閲・解釈条項・二尺度の確証規則・refuse 門・様式門・錨帯・測定不能・環境副次→analyze_A.py／校正帯・撤退→calib_band_A.py・gate_A.py／管理図→control_chart_A.py／転記行→design_facts_A.py・power_grid_A.py・cost_facts.py／Firth の基準実装と R logistf との一致検査→firth.py・firth_check_A.py・firth_check_A.R／本文の数の検査→numbers_lint.py／草案の組み立て→build_draft5A.py／整合→integrity_A.py・sample_inspection_A.py・synth_A.py／報告→報告雛形・build_report_A.py・report_lint.py／凍結→freeze_A.py。**実在（SHA16）**: %s。**未整備（凍結前に整備し dry-run と合成データで検査）**: %s。' % (
    '・'.join('%s %s' % e for e in exist), '・'.join(still)), 'data': {'exist': dict(exist), 'not_yet': still}}

# ---- K: 引数・seed・tag
S_ = T['seeds']
F['K'] = {'text': '引数文字列 `--arms %s`（SHA16 %s・%d 腕）。seed: 門0.5 %d／パイロット %d〜（機種 × 場面）／本走行 %d〜／錨反復 %d〜（規模 × 場面）／橋 %s／校正 %d を基に %s／API 再走行 %s／Firth 一致検査 %d／dry-run %d。tag: %s。' % (
    T['arms']['arms_string'], sha_str(T['arms']['arms_string']), len(ARMS), S_['identity'], min(v for d in S_['pilot'].values() for v in d.values()), min(v for d in S_['main'].values() for v in d.values()),
    min(v for d in S_['anchor_rerun'].values() for v in d.values()), json.dumps(S_['bridge']), S_['calibration']['base'], S_['calibration']['rule'], json.dumps(S_['api_rerun']), S_['firth_check'], S_['dryrun'], json.dumps(T['tags'], ensure_ascii=False))}

# ---- M: 環境帯
M = PG['M']; EB = T['environment_band']; cands = sorted(M['candidates'], key=int)
F['M'] = {'text': '環境帯（橋の %s・本走行の %s 対 橋・n=%d 同士・腕ごと・「超」・厳密・真の率は 4B-2507 の API 既測〔%s〕・既測の無い腕は %s）: %s。**選択規則（確証 %d 対比の期待誤保留数が %s 以下となる最小の候補）で選ばれる候補 %s pt**（値は登録者最終確認で確定・正本の band_pt は未設定）。' % (
    '・'.join(M['bridge_models']), T['bridge']['scenario'], M['n'], T['bridge']['scenario'], EB['rule_missing_base_rate'],
    '／'.join('%s pt: 腕あたり（真の率 0.5）%s・いずれかの腕が超える確率 %.3f・期待誤保留数 %.2f・検出 %s' % (b, sci(M['candidates'][b]['per_arm_at_05']), M['candidates'][b]['p_any_arm_any_model'], M['candidates'][b]['expected_false_held_contrasts'],
                                                                   '・'.join('差 %s pt で %.3f' % (s_, v) for s_, v in M['candidates'][b]['detection_by_shift_pt'].items())) for b in cands),
    len(CONTR), EB['rule_expected_max'], M['selected_by_rule']), 'data': M}

# ---- N: 門0.5 の帰無の不合格率
N_ = PG['N']; IS = T['identity_screen']
F['N'] = {'text': '門0.5 同一性選別の帰無の不合格率（両スタックが同じ分布でも主判定〔%d 個の絶対差の平均 %d 超または最大 %d 超〕に落ちる確率・%s の API 既測を真の分布とする・B=%d）: %s。登録値 n=%d（登録者裁定 D7）。' % (
    IS['n_differences'], IS['mean_pt'], IS['max_pt'], IS['scenario'], PG['B']['N'], '・'.join('手元 n=%d・%s: %.3f（最大絶対差の 95 パーセンタイル %.1f pt）' % (v['n_local'], {'api_fixed': 'API を固定', 'api_resampled': 'API も再標本'}[v['mode']], v['fail_rate'], v['max_abs_diff_p95']) for v in N_.values()), n_id), 'data': N_}

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
outj = {'generated_utc': now, 'generator': 'tools/design_facts_A.py v2', 'contrasts_sha16': sha_file(CPATH), 'power_grid_json_sha16': sha_file(a.pg), 'z': {k: round(Z[k], 6) for k in SIZES}, 'facts': F}
os.makedirs(os.path.dirname(a.out), exist_ok=True)
json.dump(outj, open(a.out + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
L = ['# 段階 A 設計事実（機械生成・`tools/design_facts_A.py` v2・%s UTC・正本 contrasts-A.json SHA16 %s・格子 power-grid-A.json SHA16 %s）' % (now, outj['contrasts_sha16'], outj['power_grid_json_sha16']), '']
for k in 'ABCDEFGHIJKLMN':
    L.append('- **転記行 %s** — %s' % (k, F[k]['text'])); L.append('')
L.append('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[design_facts_A v2] written %s.{md,json}' % a.out)
