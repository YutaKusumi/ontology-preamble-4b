# -*- coding: utf-8 -*-
"""design_facts_A.py v3.3 —— 段階 A の設計事実（転記行 A〜O）を機械生成する（2026-09-13）。
v3.3（2026-09-14・凍結前の最終検分の採否表 P118・P120・P122〜P125・登録者裁定 D27〜D29・D34）: 格子 v3.3 を要求する。転記行 A に校正腕のセッション数の内訳と下界、転記行 D に両向きの到達と区間と測れた対比の本数・測れた効果種の B の対応・格子の解釈条項の発火率の注、
  転記行 E は格子の丸めの前の値から一度で丸める、転記行 F に時間貸しに移す機種を除いた停止規則の参照、転記行 G にセルをまたいだ率、転記行 M は確証族の腕の値を先に置く。到達の下限は正本 blind_below から読む。
v3.2（2026-09-14・登録者裁定 D18・実装検分の採否表 P98）: 格子 v3.2 を要求する。転記行 F と G の入力（cost-facts と style-stageF1）の SHA16 を記帳する。転記行 J の器材の一覧に名の語彙の出所（response_mode_M.py・response_mode_F.py）を足す。
v3.1（2026-09-13・登録者裁定 D9 の三つ目の手順）: 格子 v3.1 を要求し、格子の全入力（正本・機種の記録・firth・confirm_A・zaxis_A・power_grid_A・bands_A）の SHA16 を現行のファイルと突合する。転記行 J の器材の一覧を整備後に合わせる。
入力: design/contrasts-A.json（正本 v2.2）・records/A/power-grid-A.json（v3）・records/A/hf-models-A.json・records/cost-pilot/cost-facts-2026-09-13.md（U 表・R 表・G 行を解析）・records/F/style-stageF1.json（(b) 率の既測・記述）。
v3 の変更（凍結前検分・七票の採否表 P18〜P31・P38〜P48・P55・P59・登録者裁定 D10〜D13）: 転記行 D に余白のある型・切り詰めた規模数と真の pt 差の傾き・pt 差の傾きの単独の実サイズ・Holm の後段・効果種ごとの到達と三型とも届かない対比・Odose 系の仮定の基底・指標名・条件付き率の区間・独立の注・refuse 門の追加配置／F に橋の校正腕・14B の固定・32B の係数の感度・丸めない合計・上界の範囲／G に N を含む対比／H と M に帰無側の規則・M に率への依存と確証族の腕数と保留の単位／I に不合格枝の撤退条件と上側の帯の計算／L に走行器の設定／N に登録の値と検出側／O（新設）判定器の幅／書式文字列に数を直書きしない（numbers_lint の生成器の文字列リテラル検査）。z は tools/zaxis_A.py。
v2: 格子の入力 SHA16 と z の assert・費用の係数は cost-facts を解析・登録した同時要求数の収容を assert・費用は処理量の上界と下界・校正腕はセッションごと・転記行 N。
出力: records/A/design-facts-A.md と同 .json。--allow-quick（quick の格子）・--allow-stale（正本の SHA16 が格子の入力と違う）は検査用で、出力の dev_marks に印を付け、組み立て器（build_draftA.py）は印つきを拒む。
柵: 本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, math, hashlib, datetime, argparse, statistics
from fractions import Fraction
from scipy.stats import binom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zaxis_A import z_map
import confirm_A
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--pg', default=os.path.join(REPO, 'records', 'A', 'power-grid-A.json')); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'design-facts-A'))
ap.add_argument('--allow-quick', action='store_true'); ap.add_argument('--allow-stale', action='store_true')
a = ap.parse_args()
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json')
J = lambda p: json.load(open(p, encoding='utf-8'))
T = J(CPATH); PG = J(a.pg); HF = J(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'))
sha_file = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
sha_str = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
DEV = []
assert PG.get('version') == 'v3.3', '格子は v3.3 が要る'
NOW_IN = {'contrasts_sha16': CPATH, 'hf_models_sha16': os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), 'firth_sha16': os.path.join(REPO, 'tools', 'firth.py'), 'confirm_sha16': os.path.join(REPO, 'tools', 'confirm_A.py'),
          'zaxis_sha16': os.path.join(REPO, 'tools', 'zaxis_A.py'), 'power_grid_sha16': os.path.join(REPO, 'tools', 'power_grid_A.py'), 'bands_sha16': os.path.join(REPO, 'tools', 'bands_A.py')}
STALE = [kk for kk, pp in NOW_IN.items() if PG['inputs'].get(kk) != sha_file(pp)]
if STALE:
    assert a.allow_stale, ('格子の入力の SHA16 と現行のファイルが不一致', STALE); DEV.append('stale_inputs')
if PG.get('quick'):
    assert a.allow_quick, 'quick の格子は転記に使わない'; DEV.append('quick_grid')
n, pn, n_id, n_cal = T['n_per_arm'], T['pilot_n'], T['identity_n'], T['calibration_n']
SC = T['scenarios']; ARMS = T['arms']['preamble']; SIZES = T['sizes']; MODELS = T['models']; FAM = T['families']['A_slope']; CONTR = FAM['contrasts']
lo, hi = T['censor']['low'], T['censor']['high']
F = {}
f3 = lambda v: '—' if v is None else '%.3f' % v
sci = lambda v: '%.2e' % v
civ = lambda v: '—' if (v is None or v[0] is None) else 'Wilson %.3f〜%.3f' % tuple(v)
CENSOR_LIKELY = 0.5     # 転記行 C の「検閲される見込み」の閾（記述の区切り）
CLAUSE_MAJORITY = 0.5   # 転記行 D: 解釈条項が当てはめの多数で発火する対比を数える区切り（記述）
LOSS_MARGIN = 0.1       # 転記行 D: 二尺度の規則で草案4 の規則より到達が下がる対比を数える区切り（記述）
ME = T['reading_selection']['measurable_effect_type']
BLIND = ME['blind_below']   # 転記行 D: 到達が届かない対比を数える区切り（正本の下限・登録者裁定 D29・v3.2 までは器の中の記述の区切り〔同じ値〕）
CIP = '%g%%' % (ME['ci_level'] * 100)
TRENDS = ['一定', '上昇', '下降']
Z, PAR = z_map(HF)
for k in SIZES:
    assert abs(PG['z'][k] - Z[k]) < 1e-9, ('格子の z が実パラメータ数の z と不一致', k)

# ---- L: 容量と収容（登録値を assert）・走行器の設定
CR = T['capacity_rule']; ENVS = T['environments']; GG = HF['gpu_gib']; RUN = T['runner']
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
    if e.get('concurrency_fixed'):
        extra += '・%s' % e['concurrency_fixed']
    if e.get('if_not_80GB'):
        g = e['if_not_80GB']; assert g['concurrency'] <= cmax(k, GMAP[g['memory_class_gb']]), ('第三の環境の同時要求数が収容を超える', k)
        extra += '・80GB が割り当てられなければ環境値「%s」（%s・同時 %d）' % (g['env'], g['gpu'], g['concurrency'])
    Ld[k] = {'rev': HF['models'][k]['rev'], 'params_M': round(PAR[k] / 1e6, 1), 'z': round(Z[k], 4), 'weights_gib': HF['models'][k]['safetensors_gib'], 'kv_per_request_gib': round(KV[k], 4), 'max_concurrency': c, 'registered': e}
    parts.append('%s: rev %s・%s M params・z=%+.4f・重み %.2f GiB・KV／要求 %.4f GiB・最大同時（L4／A100 40GB／A100 80GB）%d／%d／%d・登録 %s %dGB 同時 %d%s' % (
        k, HF['models'][k]['rev'], Ld[k]['params_M'], Z[k], HF['models'][k]['safetensors_gib'], KV[k], c['L4'], c['A100 40GB'], c['A100 80GB'], e['env'], e['memory_class_gb'], e['concurrency'], extra))
bparts = []
for k, bc in T['bridge']['cells'].items():
    gname, G = ('L4', GG['L4']) if bc['bridge_env'] == 'L4' else ('A100 40GB', GG['A100-40GB'])
    assert bc['bridge_concurrency'] <= min(CR['concurrency_cap'], cmax(k, G)), ('橋の同時要求数が収容を超える', k)
    bparts.append('%s の %s 側 同時 %d（最大 %d・%s の容量で検査）' % (k, bc['bridge_env'], bc['bridge_concurrency'], min(CR['concurrency_cap'], cmax(k, G)), gname))
F['L'] = {'text': '機種別の容量と収容（HF 取得 %s・実パラメータ数は config.json から機械計算・収容規則＝重み＋KV〔要求あたり %s トークン × 同時要求数〕＋%s GiB が GPU メモリの %s 以内・GPU メモリは hf-models-A.json の gpu_gib〔L4 %s・A100 40GB %s・A100 80GB %s GiB〕・同時要求数の上限 %d・登録値の収容は assert 済み）: ' % (
    HF['fetched_utc'], format(CR['kv_tokens_per_request'], ','), CR['overhead_gib'], CR['gpu_fraction'], GG['L4'], GG['A100-40GB'], GG['A100-80GB'], CR['concurrency_cap']) + '／'.join(parts) + '。橋: ' + '・'.join(bparts) +
    '。走行器 %s %s（SHA16 %s）の設定: max_tokens %d・max_model_len %d・温度 %s・top_p %s・要求本文に %s。%s' % (RUN['script'], RUN['version'], RUN['sha16'], RUN['max_tokens'], RUN['max_model_len'], RUN['temperature'], RUN['top_p'], json.dumps(RUN['extra_body']), CR['kv_note']), 'data': Ld}

# ---- F: 費用（cost-facts を解析）・橋の校正腕・32B の係数の感度
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
C = T['cost']; SF0 = C['size_factor_assumption']; SH = C['session_h']; CAP = CR['concurrency_cap']; AB = T['anchor_band']; CALM = T['calibration']['model']
anchor_trials = len(AB['scenarios']) * len(AB['arms']) * n; base_trials = len(SC) * len(ARMS) * (pn + n)


def plan_model(k, env, conc, bound, SF):
    tg = TAG[env]; tph = TPH[tg]; st = SETUP[tg] / 3600; eff = tph * (conc / CAP if bound == 'upper' else 1.0)
    main = base_trials + (anchor_trials if k in AB['models'] else 0); sess = 1; h_run = 0.0
    for _ in range(60):
        h_run = main * SF[k] / eff + sess * n_cal * SF[CALM] / tph
        new = max(1, math.ceil(h_run / (SH - st)))
        if new == sess:
            break
        sess = new
    h_tot = h_run + sess * st
    return {'env': env, 'concurrency': conc, 'trials': main + sess * n_cal, 'hours': h_tot, 'sessions': sess, 'units': h_tot * RATE[tg], 'last_session_margin': (sess * (SH - st) - h_run) / (SH - st)}


def plan_bridge(k, bc, bound, SF):
    env = bc['bridge_env']; tg = TAG[env]; tph = TPH[tg]; st = SETUP[tg] / 3600; eff = tph * (bc['bridge_concurrency'] / CAP if bound == 'upper' else 1.0)
    tr = len(T['bridge']['arms']) * T['bridge']['n']; sess = 1; h_run = 0.0
    for _ in range(60):
        h_run = tr * SF[k] / eff + sess * n_cal * SF[CALM] / tph
        new = max(1, math.ceil(h_run / (SH - st)))
        if new == sess:
            break
        sess = new
    h_tot = h_run + sess * st
    return {'env': env, 'concurrency': bc['bridge_concurrency'], 'trials': tr + sess * n_cal, 'hours': h_tot, 'sessions': sess, 'units': h_tot * RATE[tg]}


def plans_for(bound, SF):
    rows = {m['key']: plan_model(m['key'], ENVS[m['key']]['env'], ENVS[m['key']]['concurrency'], bound, SF) for m in MODELS}
    for k, bc in T['bridge']['cells'].items():
        rows['橋 %s（%s 側）' % (k, bc['bridge_env'])] = plan_bridge(k, bc, bound, SF)
    return {'rows': rows, 'units': sum(v['units'] for v in rows.values()), 'hours': sum(v['hours'] for v in rows.values()), 'trials': sum(v['trials'] for v in rows.values()), 'sessions': sum(v['sessions'] for v in rows.values())}


plans = {bound: plans_for(bound, SF0) for bound in ('upper', 'lower')}
alt40 = {}
for m in MODELS:
    e = ENVS[m['key']]
    if 'if_40GB' in e:
        alt40[m['key']] = None if e['if_40GB'] is None else plan_model(m['key'], e['env'], e['if_40GB']['concurrency'], 'upper', SF0)
tgL = TAG['L4']; g05_tr = n_id * len(ARMS); g05_h = g05_tr / TPH[tgL] + SETUP[tgL] / 3600
margin = min((v['last_session_margin'], k) for k, v in plans['upper']['rows'].items() if 'last_session_margin' in v)
stop_thr = plans['upper']['units'] * C['stop_rule']['multiplier']
RENT = [m['key'] for m in MODELS if ENVS[m['key']].get('if_not_80GB')]   # 時間貸しに移しうる機種（登録者裁定 D34）
upper_wo = plans['upper']['units'] - sum(plans['upper']['rows'][k]['units'] for k in RENT); thr_wo = upper_wo * C['stop_rule']['multiplier']
s_rent = '%s を時間貸しに移す場合の停止規則の参照（%s）: %s を除いた上界 %.1f ユニット・その %s 倍 %.1f ユニット。' % ('・'.join(RENT), C['stop_rule']['rental_adjust'], '・'.join(RENT), upper_wo, C['stop_rule']['multiplier'], thr_wo)
k32 = SIZES[-1]; sens = []
for dlt in range(0, 5):
    SFx = dict(SF0); SFx[k32] = SF0[k32] + dlt; px = plans_for('upper', SFx); sens.append({'factor': SFx[k32], 'units_32B': px['rows'][k32]['units'], 'upper_total': px['units'], 'exceeds_stop_threshold': px['units'] > stop_thr})
row_txt = lambda k, v: '%s（%s・同時 %d）%s 試行・%.1f h・%d セッション・%.1f ユニット' % (k, v['env'], v['concurrency'], format(v['trials'], ','), v['hours'], v['sessions'], v['units'])
F['F'] = {'text': ('費用と時間（門0 の実測: L4 %.2f ユニット/h・%s 試行/h・経費 %d s／A100〔%s〕%.2f ユニット/h・%s 試行/h・経費 %d s・門0 の同時要求 %d・4B 比の試行時間の仮定 %s ◐・セッション %s 時間・校正腕は %s の係数で、%s・橋のセッションにも校正腕）: '
                   '**上界**（処理量 ∝ 同時要求数）: %s。**上界の合計 %s 試行・%.1f 時間・%.1f ユニット**（セッション %d）。下界（同時要求数で処理量が落ちない）の合計 %.1f 時間・%.1f ユニット。'
                   'A100 40GB が割り当てられた場合（上界）: %s。最後のセッションの余裕の最小 %.3f（%s）。停止規則: パイロット後の見込みが上界の %s 倍（%.1f ユニット）を超えたら本走行の前に登録者が再裁定。%s。32B の係数の感度（上界の合計・停止規則の閾値は登録値のまま）: %s。%s'
                   '門0 の判定時の A＋B 見込み %s ユニットに対し、A の上界は %.2f 倍。門0.5（n=%d × %d 腕・L4・vLLM）%s 試行・%.2f h・%.2f ユニット。API 再走行・判定器の断片・機種の切替の経費は含まない。パイロットで機種ごとの実測に置き換える。') % (
    RATE[TAG['L4']], format(int(TPH[TAG['L4']]), ','), SETUP[TAG['L4']], GPUN[TAG['A100']], RATE[TAG['A100']], format(int(TPH[TAG['A100']]), ','), SETUP[TAG['A100']], WORK[TAG['L4']], json.dumps(SF0, ensure_ascii=False), SH, CALM, C['calibration_throughput'],
    '／'.join(row_txt(k, v) for k, v in plans['upper']['rows'].items()), format(plans['upper']['trials'], ','), plans['upper']['hours'], plans['upper']['units'], plans['upper']['sessions'], plans['lower']['hours'], plans['lower']['units'],
    '／'.join(('%s は走らせない' % k) if v is None else row_txt(k, v) for k, v in alt40.items()), margin[0], margin[1], C['stop_rule']['multiplier'], stop_thr, C['upper_bound_scope'],
    '・'.join('係数 %g で 32B %.1f・合計 %.1f（%s）' % (s_['factor'], s_['units_32B'], s_['upper_total'], '閾値を超える' if s_['exceeds_stop_threshold'] else '超えない') for s_ in sens), C['rental_rule'] + '。' + s_rent,
    '〜'.join(str(x) for x in sorted(set(EST))), plans['upper']['units'] / max(EST), n_id, len(ARMS), format(g05_tr, ','), g05_h, g05_h * RATE[tgL]),
    'data': {'plans': plans, 'alt_40GB_upper': alt40, 'stop_threshold_units': stop_thr, 'size_factor_sensitivity_32B': sens, 'gate05': {'trials': g05_tr, 'hours': g05_h, 'units': g05_h * RATE[tgL]}, 'gate0_estimates_AB': EST,
             'rental_adjust': {'models': RENT, 'upper_units_without': upper_wo, 'stop_threshold_units_without': thr_wo}}}

# ---- A: 規模
t_id = n_id * len(ARMS); t_pilot = len(MODELS) * len(SC) * len(ARMS) * pn; t_main = len(MODELS) * len(SC) * len(ARMS) * n
t_anchor = len(AB['models']) * anchor_trials; sess_models = sum(plans['upper']['rows'][m['key']]['sessions'] for m in MODELS); sess_all = plans['upper']['sessions']; t_cal = sess_all * n_cal
multi = {m['key']: plans['upper']['rows'][m['key']]['sessions'] for m in MODELS if plans['upper']['rows'][m['key']]['sessions'] > 1}; sess_lo = plans['lower']['sessions']   # 採否表 P125
t_bridge = len(T['bridge']['cells']) * len(T['bridge']['arms']) * T['bridge']['n']; t_api = len(T['seeds']['api_rerun']) * len(ARMS) * n
t_total = t_id + t_pilot + t_main + t_anchor + t_cal + t_bridge
JV = T['judge_validity']; jv_all = len(MODELS) * len(SC) * JV['n_per_cell']; jv_fb = len(JV['fallback_scope']['models']) * len(SC) * JV['n_per_cell']
F['A'] = {'text': '規模: 門0.5 同一性選別 %s（%s × %d 腕 × n=%d）／パイロット %s（%d 機種 × %d 場面 × %d 腕 × n=%d）／本走行 %s（%d 機種 × %d 場面 × %d 腕 × n=%d）／錨反復 %s（%d 規模 × %d 場面 × %d 腕 × n=%d）／校正腕 %s（セッションごとに n=%d・転記行 F の上界のセッション数の合計 %d〔機種 %d（複数のセッションの機種: %s）・橋 %d〕に依存・下界のセッション数 %d なら %s）／橋 %s（%s × %d 腕 × n=%d・場面 %s・各機種の本走行の %s と対にする）＝**手元合計 %s 試行**。API 再走行（門0.5 合格時のみ）%s（%s × %s × %d 腕 × n=%d）。判定器の妥当性の断片（パイロットから抽出・系統外の盲検判定）: 全機種なら %s（%d 機種 × %d 場面 × %d）・絞る場合 %s（%s × %d 場面 × %d）・範囲は %s。' % (
    format(t_id, ','), T['identity_screen']['scenario'], len(ARMS), n_id, format(t_pilot, ','), len(MODELS), len(SC), len(ARMS), pn, format(t_main, ','), len(MODELS), len(SC), len(ARMS), n,
    format(t_anchor, ','), len(AB['models']), len(AB['scenarios']), len(AB['arms']), n, format(t_cal, ','), n_cal, sess_all, sess_models, '・'.join('%s が %d' % kv for kv in multi.items()) or 'なし', sess_all - sess_models, sess_lo, format(sess_lo * n_cal, ','),
    format(t_bridge, ','), '・'.join('%s の %s 側' % (k, v['bridge_env']) for k, v in T['bridge']['cells'].items()), len(T['bridge']['arms']), T['bridge']['n'], T['bridge']['scenario'], T['bridge']['scenario'],
    format(t_total, ','), format(t_api, ','), '・'.join(T['seeds']['api_rerun']), T['bridge']['scenario'], len(ARMS), n,
    format(jv_all, ','), len(MODELS), len(SC), JV['n_per_cell'], format(jv_fb, ','), '・'.join(JV['fallback_scope']['models']), len(SC), JV['n_per_cell'], JV['status']),
    'data': {'identity': t_id, 'pilot': t_pilot, 'main': t_main, 'anchor_rerun': t_anchor, 'calibration': t_cal, 'calibration_sessions': {'all': sess_all, 'models': sess_models, 'multi_session_models': multi, 'lower_all': sess_lo, 'lower_trials': sess_lo * n_cal},
             'bridge': t_bridge, 'total_local': t_total, 'api_rerun': t_api}}

# ---- B: 対比と整合
D_ = T['descriptive_families']; I_ = T['integrity']; CRULE = FAM['confirm_rule']
meas = [c for c in CONTR if c['base_A_4B2507'] is not None and c['base_B_4B2507'] is not None]; miss = [c for c in CONTR if c not in meas]
dose = [c for c in miss if c['A'].startswith('Odose')]; other = [c for c in miss if not c['A'].startswith('Odose')]
used = {c['A'] for c in CONTR} | {c['B'] for c in CONTR}; not_in = [x for x in ARMS if x not in used]
assert set(D_['A_desc_floor']['arms']) <= set(not_in), '床持続の腕が確証族に現れている'
F['B'] = {'text': '対比: 確証 %d（傾きの族・%d 効果種 × %d 場面・m=%d 固定・両側・p* の Holm）・記述（Nstr−Onull %d・Ncold−N %d・床持続 %d セル列〔%d セル〕・レシピ対 %d・様式／錨差／スタック差／環境差／臨界規模／対数オッズ尺度でのみ立った対比は走行後に生成）。整合検査（正本の生成時）: id の重複 %d・対比が要求する腕の台帳での不在 %d・登録対比を持たない腕 %d・台帳に無い腕 %d・札の全組合せ表 %d 行（発火可能 %d・行 id の一意を assert）。確証 %d 本のうち 4B-2507 の API 既測で両腕の基底を持つもの %d・欠くもの %d（Odose1・Odosehalf 系 %d 本＋その他 %d 本: %s）。確証族に一度も現れない腕: %s（%s は床持続の記述降格の帰結・その他は記述の設計）。' % (
    len(CONTR), FAM['effect_types'], len(SC), FAM['m'], len(D_['A_desc_nstr']['contrasts']), len(D_['A_desc_ncold']['contrasts']), D_['A_desc_floor']['cell_series'], len(D_['A_desc_floor']['cells']), len(D_['A_desc_recipe']['contrasts']),
    I_['id_duplicates'], len(I_['arms_required_missing']), len(I_['arms_without_contrast']), len(I_['arms_not_in_ledger']), I_['label_combo_rows'], I_['label_combo_fireable'], len(CONTR), len(meas), len(miss), len(dose), len(other), '・'.join(c['id'] for c in other), '・'.join(not_in), '・'.join(D_['A_desc_floor']['arms'])),
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
PL = {'mid_const': '対照中間', 'floor_const': '対照が床', 'ceiling_const': '対照が天井', 'ctrl_rising': '対照が上昇', 'ctrl_falling': '対照が下降', 'ctrl_rising_080': '対照が上昇（余白あり）', 'ctrl_falling_080': '対照が下降（余白あり）'}
PSL = {'floor_const_d0': '床・pt 差なし', 'floor_const_plus': '床・pt 差あり', 'ceiling_const_d0': '天井・pt 差なし', 'near_ceiling_treat': '処置が天井に近い'}


def sel(pat, d0, D):
    for r in PG['D']:
        if r['pattern'] == pat and abs(r['d0_pt'] - d0) < 1e-9 and abs(r['delta_pt_32B_minus_4B'] - D) < 1e-9:
            return r
    raise KeyError((pat, d0, D))


def pdesc(nm):
    v = PG['patterns'][nm]['ctrl'] if nm in PG['patterns'] else PG['patterns_clean'][nm]; return '%s（%s）' % (PL[nm], ('%g' % v[0]) if v[0] == v[-1] else '%g→%g' % (v[0], v[-1]))


D0V = PG['d0_values']; DV = PG['delta_values']; DREF = PG['real_base']['delta']; ZERO = 0.0
s_size = '・'.join('%s: 名目 β₃ 棄却率 %.3f〔条件付き %s・%s・n_fit %d・判定不能 %.3f・非収束 %.3f〕・Holm 初段 β₃ %.3f・札 D1（初段）%.3f' % (
    pdesc(nm), r['reject_nominal'], f3(r['reject_nominal_conditional']), civ(r['reject_nominal_conditional_ci95']), r['n_fit'], r['undecidable_censor'], r['nonconverged'], r['reject_holm_first'], r['card_D1_holm_first']) for nm in PG['patterns'] for r in [sel(nm, ZERO, ZERO)])
rm = [sel('mid_const', ZERO, D) for D in DV if D > 0]
s_pow = '%s・Δ=%s pt の札 D1（初段）%s・札 D1（名目）%s・草案4 の規則の初段 %s' % (pdesc('mid_const'), '／'.join('%g' % (D * 100) for D in DV if D > 0), '／'.join('%.3f' % r['card_D1_holm_first'] for r in rm), '／'.join('%.3f' % r['card_D1_nominal'] for r in rm), '／'.join('%.3f' % r['card_draft4_holm_first'] for r in rm))


def ptconst(nm):
    out = []
    for d0 in D0V:
        if d0 == 0:
            continue
        r = sel(nm, d0, ZERO)
        out.append(('d0=%g pt は外した' % (d0 * 100)) if 'dropped' in r else ('d0=%g pt（切り詰め %d 規模・真の pt 差の傾き %+.3f pt／z）で %.3f／%.3f → %.3f／%.3f' % (d0 * 100, r['clipped_sizes'], r['true_slope_pt'], r['card_draft4_nominal'], r['card_draft4_holm_first'], r['card_D1_nominal'], r['card_D1_holm_first'])))
    return '・'.join(out)


s_hole = '余白の無い型（切り詰めがある行では真の pt 差は全規模で一定ではない）の札（草案4 の規則の名目／初段 → 裁定 D1 の名目／初段）は、%s: %s、%s: %s' % (pdesc('ctrl_rising'), ptconst('ctrl_rising'), pdesc('ctrl_falling'), ptconst('ctrl_falling'))
DCr = PG['DC']; nparts = []; eparts = []
for nm in PG['patterns_clean']:
    rows = [r for r in DCr if r['pattern'] == nm]
    nparts.append('%s: %s' % (pdesc(nm), '・'.join('d0=%g pt（切り詰め %d 規模・真の傾き %+.3f）で %.3f／%.3f → %.3f／%.3f' % (r['d0_pt'] * 100, r['clipped_sizes'], r['true_slope_pt'], r['card_draft4_nominal'], r['card_draft4_holm_first'], r['card_D1_nominal'], r['card_D1_holm_first']) for r in rows if r['kind'] == 'scale_null')))
    eparts.append('%s: %s' % (pdesc(nm), '・'.join('Δ=%g pt（切り詰め %d 規模）で草案4 の規則の初段 %.3f → 札 D1 の初段 %.3f' % (r['delta_pt_32B_minus_4B'] * 100, r['clipped_sizes'], r['card_draft4_holm_first'], r['card_D1_holm_first']) for r in rows if r['kind'] == 'effect')))
s_clean = '**尺度依存の穴（余白のある型・B=%d）**: pt 差が全規模で一定（Δ=%g）の配置の札（草案4 の規則の名目／初段 → 裁定 D1 の名目／初段）は、%s。**対照が動く × 効果あり（同じ型）**: %s' % (PG['B']['DC'], ZERO, '／'.join(nparts), '／'.join(eparts))
fr = sel('floor_const', ZERO, DREF); cr = sel('ceiling_const', ZERO, DREF)
s_fc = '%s・Δ=%g pt の札 D1（初段）%s（判定不能 %s・解釈条項 %s）／%s・Δ=%g pt（処置が下がる向き）の札 D1（初段）%s（判定不能 %s・解釈条項 %s）' % (
    pdesc('floor_const'), DREF * 100, f3(fr.get('card_D1_holm_first')), f3(fr.get('undecidable_censor')), f3(fr.get('clause_rate_among_fit')), pdesc('ceiling_const'), DREF * 100, f3(cr.get('card_D1_holm_first')), f3(cr.get('undecidable_censor')), f3(cr.get('clause_rate_among_fit')))
dropped = [r for r in PG['D'] if 'dropped' in r]
s_drop = '全規模が上限・下限に切り詰められて格子から外した行 %d（%s）' % (len(dropped), '・'.join('%s d0=%g Δ=%g' % (PL[r['pattern']], r['d0_pt'] * 100, r['delta_pt_32B_minus_4B'] * 100) for r in dropped) or 'なし')
PSr = PG['PS']; mid = [r for r in PSr['rows'] if r['retained'] != 'natural']; edge = [r for r in PSr['rows'] if r['retained'] == 'natural']; by_k = {}
for r in mid:
    by_k.setdefault(r['retained_n'], []).append(r)
s_ps = '**pt 差の傾きの検定だけの実サイズ**（B=%s・真の pt 差は全規模で一定・切り詰めなし・向きの条件なし・目標は名目 %s と初段 %.6f）: 中間域の %d 配置で名目の比 %.2f〜%.2f・初段の比 %.2f〜%.2f（残す規模数ごとの初段の比: %s）。検閲を自然に掛ける配置: %s。床と天井では当てはめ可能な標本の中で実サイズが名目を大きく超え、無条件の水準は検閲と解釈条項で下がる' % (
    format(PG['B']['PS'], ','), PSr['targets']['nominal'], PSr['targets']['holm_first'], len({r['config'] for r in mid}), min(r['ratio_nominal'] for r in mid), max(r['ratio_nominal'] for r in mid), min(r['ratio_holm_first'] for r in mid), max(r['ratio_holm_first'] for r in mid),
    '・'.join('%d 規模 %.2f〜%.2f' % (k, min(x['ratio_holm_first'] for x in v), max(x['ratio_holm_first'] for x in v)) for k, v in sorted(by_k.items(), reverse=True)),
    '／'.join('%s（対照 %g→%g・pt 差 %+g pt）: 当てはめ可能 %.4f・その中の名目の比 %.2f・初段の比 %.2f・無条件の名目 %.4f・初段 %.5f' % (PSL[r['config']], r['ctrl'][0], r['ctrl'][-1], r['d0_pt'] * 100, r['fit_rate'], r['ratio_nominal_given_fit'], r['ratio_holm_first_given_fit'], r['size_nominal'], r['size_holm_first']) for r in edge))
s_later = '**Holm の後段の正規の臨界**: %s' % '・'.join('α/%d で %.3f' % (x['step_denominator'], x['z']) for x in PG['levels']['holm_later'])
DRr = PG['DR']; nDR = len({r['id'] for r in DRr}); dparts = []
for tr in TRENDS:
    r0 = [r for r in DRr if r['ctrl_trend'] == tr and r['delta_value'] == ZERO]; r1 = [r for r in DRr if r['ctrl_trend'] == tr and r['delta_value'] != ZERO]
    mx = max(r0, key=lambda r: r['card_D1_holm_first']); mx4 = max(r0, key=lambda r: r['card_draft4_nominal']); mn = min(r1, key=lambda r: r['card_D1_holm_first'])
    dparts.append('対照の規模変化 %s（32B−4B %+g pt）: Δ=%g で札 D1（初段）の最大 %.3f（%s）・期待本数 %.3f・少なくとも一本 %.3f・草案4 の規則（名目）の最大 %.3f（%s）・期待本数 %.3f・判定不能の期待本数 %.2f／Δ=±%g で札 D1（初段）の中央値 %.3f・平均 %.3f（草案4 の規則の初段の平均 %.3f）・最小 %.3f（%s）・%s 未満 %d 本・解釈条項が当てはめの %s 以上で発火する対比 %d 本・草案4 の規則の初段から %s 以上下がる対比 %d 本・期待本数 %.2f' % (
        tr, r0[0]['ctrl_change_32B_minus_4B'] * 100, ZERO, mx['card_D1_holm_first'], mx['id'], sum(r['card_D1_holm_first'] for r in r0), 1 - math.prod(1 - r['card_D1_holm_first'] for r in r0),
        mx4['card_draft4_nominal'], mx4['id'], sum(r['card_draft4_nominal'] for r in r0), sum(r['undecidable_censor'] for r in r0), DREF, statistics.median(r['card_D1_holm_first'] for r in r1), statistics.mean(r['card_D1_holm_first'] for r in r1), statistics.mean(r['card_draft4_holm_first'] for r in r1), mn['card_D1_holm_first'], mn['id'],
        BLIND, sum(1 for r in r1 if r['card_D1_holm_first'] < BLIND), CLAUSE_MAJORITY, sum(1 for r in r1 if (r['clause_rate_among_fit'] or 0) >= CLAUSE_MAJORITY), LOSS_MARGIN, sum(1 for r in r1 if r['card_draft4_holm_first'] - r['card_D1_holm_first'] >= LOSS_MARGIN), sum(r['card_D1_holm_first'] for r in r1)))
s_dr = ('両腕の既測基底を持つ %d 本の 4B の実基底を入力にすると（B=%d）、%s。期待本数は独立を仮定しなくても和で正しい。「少なくとも一本」は同じ効果種の対比のあいだの独立に依るが、同じ効果種の対比は場面ごとに別の走行の標本なので、'
        '全場面に Δ を置く計算の前提の内で独立は成り立つ（腕を共有する別の効果種の対比どうしは独立ではない）' % (nDR, PG['B']['DR'], '／'.join(dparts)))
EFF = {c['id']: c['effect'] for c in CONTR}; eff_of = lambda cid: EFF[cid]   # 効果種は正本の effect（採否表 P127）
ids = [c['id'] for c in CONTR if any(r['id'] == c['id'] for r in DRr)]; effs = list(dict.fromkeys(eff_of(i) for i in ids))
sel1 = {(r['id'], r['ctrl_trend']): r for r in DRr if r['delta_value'] != ZERO}; selO = {(r['id'], r['ctrl_trend']): r for r in PG['DR_opp']}; efparts = []
THR = ME['threshold']; BDR = PG['B']['DR']; assert PG['B']['DR_opp'] == BDR; meas_by_trend = {tr: [] for tr in TRENDS}
for e in effs:
    ii = [i for i in ids if eff_of(i) == e]; tparts = []
    for tr in TRENDS:
        pr = [sel1[(i, tr)]['card_D1_holm_first'] for i in ii]; po = [selO[(i, tr)]['card_D1_holm_first'] for i in ii]
        ar = confirm_A.at_least_one_interval(pr, BDR, ME['ci_level']); ao = confirm_A.at_least_one_interval(po, BDR, ME['ci_level'])
        sr = confirm_A.direction_state(ar[1], ar[2], THR); so = confirm_A.direction_state(ao[1], ao[2], THR)
        if sr == 'measured' and so == 'measured':
            meas_by_trend[tr].append(e)
        tparts.append('%s 余地のある向き %.3f（区間 %.3f〜%.3f・%s）・逆向き %.3f（区間 %.3f〜%.3f・%s）・測れた対比 %d/%d・一方の向きでも %s 未満 %d' % (
            tr, ar[0], ar[1], ar[2], confirm_A.STATE_TEXT[sr], ao[0], ao[1], ao[2], confirm_A.STATE_TEXT[so], sum(1 for x, y in zip(pr, po) if min(x, y) >= THR), len(ii), BLIND, sum(1 for x, y in zip(pr, po) if min(x, y) < BLIND)))
    efparts.append('%s（%d 本）: %s' % (e, len(ii), '・'.join(tparts)))
blind3 = [i for i in ids if all(sel1[(i, tr)]['card_D1_holm_first'] < BLIND for tr in TRENDS)]; blind3o = [i for i in ids if all(selO[(i, tr)]['card_D1_holm_first'] < BLIND for tr in TRENDS)]
nobase = [c['id'] for c in CONTR if c['id'] not in ids]
s_eff = ('**効果種ごとの到達**（既測基底のある対比・Δ=±%g・札 D1 の初段・両向き〔余地のある向きは格子の DR 節・逆向きは DR_opp 節〕・「少なくとも一本」の %s 区間は対比ごとの模擬の二項の分散からデルタ法・'
         '両向きとも区間の下端が選択規則の閾値 %s 以上で測れた・測れた対比は両向きとも個別に閾値以上・下限 %s）: %s。**両向きとも測れた効果種の数（対照の規模変化の三型）**: %s。'
         '**三型のいずれでも %s 未満の対比**: 余地のある向きで %d 本（%s）・逆向きで %d 本（%s）。**既測基底の無い対比 %d 本**は実基底の行に載らない（Odose 系は下の仮定の基底で計算）。'
         '**測れた効果種の B**: 集計時の計算は正本の B=%s、この見込み（DR・DR_opp 節）は B=%d。格子の模擬は測定不能と錨帯の除外を入れない配置の値で、実測では解釈条項の飽和を除外の後に残った規模で数える（運用の解釈 count_after）') % (
    DREF, CIP, THR, BLIND, '／'.join(efparts), '・'.join('%s %d（%s）' % (tr, len(meas_by_trend[tr]), '・'.join(meas_by_trend[tr]) or 'なし') for tr in TRENDS),
    BLIND, len(blind3), '・'.join(blind3) or 'なし', len(blind3o), '・'.join(blind3o) or 'なし', len(nobase), format(ME['B_per_contrast'], ','), BDR)
DOr = PG['DO']; doparts = []
for e in dict.fromkeys(eff_of(r['id']) for r in DOr):
    for d0 in PG['odose_assumed_d0']:
        rr = [r for r in DOr if eff_of(r['id']) == e and r['assumed_d0'] == d0 and r['delta_value'] != ZERO]
        doparts.append('%s・仮定の d0 %+g pt: %s' % (e, d0 * 100, '・'.join('%s 平均 %.3f・少なくとも一本 %.3f' % (tr, statistics.mean(x['card_D1_holm_first'] for x in rr if x['ctrl_trend'] == tr), 1 - math.prod(1 - x['card_D1_holm_first'] for x in rr if x['ctrl_trend'] == tr)) for tr in TRENDS)))
s_do = '**Odose 系（対照 Onull の既測・処置の基底は仮定＝対照＋d0・Δ=±%g・札 D1 の初段・B=%d）**: %s' % (DREF, PG['B']['DO'], '／'.join(doparts))
DSr = PG['DS']; sparts = []
for slo_, shi_ in zip(T['censor']['sensitivity']['low'], T['censor']['sensitivity']['high']):
    g = lambda nm, d0, D: next((r for r in DSr if abs(r['censor_low'] - slo_) < 1e-9 and abs(r['censor_high'] - shi_) < 1e-9 and r['pattern'] == nm and abs(r['d0_pt'] - d0) < 1e-9 and abs(r['delta_pt_32B_minus_4B'] - D) < 1e-9), {})
    sparts.append('閾値 %g／%g で %s・Δ=%g pt の札 D1（初段）%s・%s・d0=%g pt・Δ=%g の札 D1（名目）%s・%sの判定不能 %s' % (slo_, shi_, PL['mid_const'], DREF * 100, f3(g('mid_const', ZERO, DREF).get('card_D1_holm_first')), PL['ctrl_rising'], DREF * 100, ZERO, f3(g('ctrl_rising', DREF, ZERO).get('card_D1_nominal')), PL['floor_const'], f3(g('floor_const', ZERO, ZERO).get('undecidable_censor'))))
s_ds = '検閲の感度閾値（B=%d）: %s' % (PG['B']['DS'], '／'.join(sparts))
s_r = 'refuse 門（B=%d）: %s' % (PG['B']['R'], '／'.join('%s: 名目有意 %.3f・そのうち保留 %s（(a) %s・(b) %s・(c) %s・(d) %s）・札 D1（初段）は門の前 %.3f・門のあと %.3f' % (
    r['config'], r['nominal_significant'], f3(r['hold_among_nominal']), f3(r['hold_a_among_nominal']), f3(r['hold_b_among_nominal']), f3(r['hold_c_among_nominal']), f3(r['hold_d_among_nominal']), r['card_D1_holm_first_without_gate'], r['card_D1_holm_first_after_gate']) for r in PG['R']))
F['D'] = {'text': '傾きの族（Firth PPLRT 両側・n=%d × %d 規模・両腕条件の検閲・率は B 回あたりの無条件率・B=%d・seed %d・節ごとの子ストリーム・z は転記行 L の実値〔一致を assert〕・判定は tools/confirm_A.py・札 D1（初段）＝p* ≤ α/%d〔β₃ と pt 差の傾きがともに初段の水準で立ち同じ向き・登録者裁定 D10 の p* の Holm でも初段の値は同じ〕）。**Δ=%g・d0=%g の β₃ の棄却率と札**: %s。**検出力**: %s。**%s**。%s。%s。%s。%s。%s。**実基底**: %s。%s。%s。%s。%s。' % (
    n, len(SIZES), PG['B']['D'], PG['seed'], FAM['m'], ZERO, ZERO, s_size, s_pow, s_hole, s_clean, s_fc, s_drop, s_ps, s_later, s_dr, s_eff, s_do, s_ds, s_r),
    'data': {'blind_all_trends': blind3, 'blind_all_trends_opposite': blind3o, 'no_base': nobase, 'n_measured': len(ids), 'blind_threshold': BLIND, 'delta': DREF, 'measurable_types_by_trend': meas_by_trend,
             'B_measurable': ME['B_per_contrast'], 'B_DR': BDR}, 'data_ref': 'records/A/power-grid-A.json'}

# ---- E: 床持続
E = PG['E']; cs = D_['A_desc_floor']['cell_series']
F['E'] = {'text': '床持続（記述）の到達可能性（n=%d・棄却域 k≤%d〔CP 片側上限 <%s・境界での実サイズ %.4f〕）: 真の率 %s で 単一セル %s・%d 規模同時 %s・Holm 初段（k≤%d・m=%d のとき）%s。記述に降格したため多重補正は課さず、各セルの CP 上限と全規模 0/1 を印字する。0/1 が零であることを「床を離れた」と読まない。' % (
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
withN = [c['id'] for c in CONTR if 'N' in (c['A'], c['B'])]
UG = G_['union_independent']
F['G'] = {'text': '様式門（(a)(b) の差・二項の差・n=%d 同士・「超」・厳密）の帰無発火率: 注（%d pt 超）%s・判定保留（%d pt 超）%s。**一つの対比の %d セル（残存 %d 規模 × (a)(b)）のどれかが超える率**（%s）: 注 %s・判定保留 %s。既測の (b) JSON 直答率（段階 F の stageF1・4B-2507・U 腕・記述）: %s。確証族で N を含む対比 %d 本（%s）: %s。腕別・規模別の (b) 率と一斉保留の見込み本数はパイロット後に記述として報告し、閾値は動かさない（登録者裁定 D6）。' % (
    n, SG['note_pt'], '・'.join('p=%s で %s' % (p, sci(v)) for p, v in G_['bands'][str(SG['note_pt'])].items()), SG['hold_pt'], '・'.join('p=%s で %s' % (p, sci(v)) for p, v in G_['bands'][str(SG['hold_pt'])].items()),
    G_['cells_per_contrast'], len(SIZES), G_['union_note'], '・'.join('p=%s で %s' % (p, sci(v)) for p, v in UG[str(SG['note_pt'])].items()), '・'.join('p=%s で %s' % (p, sci(v)) for p, v in UG[str(SG['hold_pt'])].items()),
    '／'.join('%s: %s' % (scn, '・'.join('%s %.3f' % (arm, r) for arm, r in d.items())) for scn, d in style_meas.items()) or '取得できず', len(withN), '・'.join(withN), SG['expected_note']), 'data': {'null': G_, 'measured_b_rates': style_meas, 'contrasts_with_N': withN}}

# ---- H: 錨帯
H = PG['H']; bands = sorted(H['bands'], key=int); rt = str(AB['rule_true_rate'])
F['H'] = {'text': '錨帯（%s × %d 規模 × %d 場面 × %d 走行・n=%d・「超」・厳密）: 腕あたりの帰無発火率（真の率 %s・超／以上）%s。除外単位（規模 × 場面＝%d）あたり %s、期待誤除外数 %s、少なくとも一単位 %s、4B-2507 の API 既測の基底での期待誤除外数 %s。検出側（走行間の真の drift・真の率 %s 付近）: %s。**登録値 %d pt**。規則（真の率 %s で期待誤除外数 %s 以下）を満たす最小の帯 %s pt・登録値は規則を満たす: %s（値は登録者確認 2026-09-13・規約と根拠は登録者裁定 D2・%s）。' % (
    '・'.join(AB['arms']), len(AB['models']), len(AB['scenarios']), AB['runs'], n, rt, '・'.join('%s pt %s／%s' % (b, sci(H['bands'][b]['per_pair'][rt]['strict']), sci(H['bands'][b]['per_pair'][rt]['ge'])) for b in bands), H['units'],
    '／'.join('%s pt %.4f' % (b, H['bands'][b]['per_unit_at_05']) for b in bands), '／'.join('%s pt %.2f' % (b, H['bands'][b]['expected_false_exclusions_at_05']) for b in bands),
    '／'.join('%s pt %.3f' % (b, H['bands'][b]['p_any_false_exclusion_at_05']) for b in bands), '／'.join('%s pt %.2f' % (b, H['bands'][b]['expected_false_exclusions_at_measured_bases']) for b in bands), rt,
    '・'.join('%s pt の帯で %s' % (b, '／'.join('drift %s pt %.3f' % (dl, v) for dl, v in H['bands'][b]['detection_by_drift_pt'].items())) for b in bands), AB['band_pt'], rt, AB['rule_expected_max'], H['smallest_band_meeting_rule'], H['registered_meets_rule'], AB['band_rule_side']), 'data': H}

# ---- I: 校正腕・撤退条件（合格枝・不合格枝）・門2
I2 = PG['I']; cp = I2['calibration_pass']; cf = I2['calibration_fail_local']; wd = I2['withdrawal']; wf = I2['withdrawal_fail_branch']; g2 = I2['gate2']; CAL = T['calibration']
assert cp['upper_side_exceeds_rate_one'], '上側の帯を置かない根拠（基底＋帯が率の上限を超える）が成り立たない'
F['I'] = {'text': '校正腕（%s × %s × %s・n=%d・「超」・厳密）: 合格枝＝API 既測 %.3f に対し下側 %d pt（基底＋帯が率の上限を超えるので上側は置かない・格子で計算して assert）→ 発火 X ≤ %d・帰無発火率 %s・検出 %s。不合格枝＝手元系列の初点を本走行の最初のセッションの校正腕（n=%d）とする二標本・両側 %d pt → 帰無発火率 %s・検出 %s（参考: 初点を門0.5 の n=%d にした場合の帰無発火率 %s）。撤退条件（パイロット n=%d・%d pt 超・下側）: 合格枝（API 既測・一標本）→ 発火 X ≤ %d・帰無発火率 %s・検出 %s／不合格枝（門0.5 の手元 n=%d との二標本・登録者裁定 D12 (b)）→ 帰無発火率 %s・検出 %s。門2（n=%d）の検閲の整数境界: 率 <%s は X ≤ %d・率 >%s は X ≥ %d・両腕が同じ p のとき落ちる確率 %s。' % (
    CAL['model'], CAL['arm'], CAL['scenario'], cp['n'], cp['base_api'], cp['band_pt'], cp['fire_if_le'], sci(cp['null']), '・'.join('真の率 %s で %.3f' % (p, v) for p, v in cp['detection'].items()),
    cf['n_first'], cf['band_pt'], '・'.join('真の率 %s で %s' % (p, sci(v)) for p, v in cf['null'].items()), '・'.join('%s から %s pt 下で %.3f' % (cf['detection_reference_rate'], dl, v) for dl, v in cf['detection_from_ref'].items()),
    cf['if_first_point_were_gate05']['n_first'], '・'.join('真の率 %s で %s' % (p, sci(v)) for p, v in cf['if_first_point_were_gate05']['null'].items()),
    wd['n'], wd['band_pt'], wd['fire_if_le'], sci(wd['null']), '・'.join('真の率 %s で %.3f' % (p, v) for p, v in wd['detection'].items()),
    wf['n_gate05'], '・'.join('真の率 %s で %s' % (p, sci(v)) for p, v in wf['null'].items()), '・'.join('手元 %s からパイロットが %s pt 下で %.3f' % (wf['detection_reference_rate'], s_, v) for s_, v in wf['detection_from_ref'].items()),
    g2['n'], lo, g2['censor_low_if_le'], hi, g2['censor_high_if_ge'], '・'.join('p=%s で %s' % (p, sci(v)) for p, v in g2['null_both_arms_same_p'].items())), 'data': I2}

# ---- J: 器材
TOOLS_NOW = [('make_contrasts_A.py', 'tools/make_contrasts_A.py'), ('confirm_A.py', 'tools/confirm_A.py'), ('bands_A.py', 'tools/bands_A.py'), ('runs_A.py', 'tools/runs_A.py'), ('zaxis_A.py', 'tools/zaxis_A.py'),
             ('firth.py', 'tools/firth.py'), ('power_grid_A.py', 'tools/power_grid_A.py'), ('design_facts_A.py', 'tools/design_facts_A.py'), ('numbers_lint.py', 'tools/numbers_lint.py'), ('build_draftA.py', 'tools/build_draftA.py'),
             ('firth_check_A.py', 'tools/firth_check_A.py'), ('firth_check_A.R', 'tools/firth_check_A.R'), ('results-report-template-A.src.md', 'records/A/results-report-template-A.src.md'),
             ('results-report-template-A.md', 'records/A/results-report-template-A.md'), ('bundle_prefreeze_A.py', 'tools/bundle_prefreeze_A.py'), ('cost_facts.py', 'tools/cost_facts.py'),
             ('run_preamble_local.py', 'tools/run_preamble_local.py'), ('boot_cost_pilot.py', 'tools/colab/boot_cost_pilot.py'), ('boot_stageA.py', 'tools/colab/boot_stageA.py'),
             ('identity_screen_A.py', 'tools/identity_screen_A.py'), ('response_mode_A.py', 'tools/response_mode_A.py'), ('analyze_A.py', 'tools/analyze_A.py'), ('calib_band_A.py', 'tools/calib_band_A.py'),
             ('gate_A.py', 'tools/gate_A.py'), ('control_chart_A.py', 'tools/control_chart_A.py'), ('integrity_A.py', 'tools/integrity_A.py'), ('sample_inspection_A.py', 'tools/sample_inspection_A.py'),
             ('judge_fragments_A.py', 'tools/judge_fragments_A.py'), ('synth_A.py', 'tools/synth_A.py'), ('synth_gates_A.py', 'tools/synth_gates_A.py'), ('build_report_A.py', 'tools/build_report_A.py'),
             ('report_lint.py', 'tools/report_lint.py'), ('freeze_A.py', 'tools/freeze_A.py'), ('response_mode_M.py', 'tools/response_mode_M.py'), ('response_mode_F.py', 'tools/response_mode_F.py'),
             ('tooling_interpretations_A.py', 'tools/tooling_interpretations_A.py')]
PLANNED = []
exist = [(nm, sha_file(os.path.join(REPO, p))) for nm, p in TOOLS_NOW + PLANNED if os.path.isfile(os.path.join(REPO, p))]
still = [nm for nm, p in TOOLS_NOW + PLANNED if not os.path.isfile(os.path.join(REPO, p))]
F['J'] = {'text': '凍結射程と器材の対応表: 腕・場面・環境・同時要求数・帯・規則・走行器の設定→contrasts-A.json／確証の判定（二尺度・p* の Holm・札の二段・全組合せ表）→confirm_A.py（格子・集計器・合成検査が同じ関数を import・札の率の模擬と測れた効果種を含む）／帯と門の厳密計算→bands_A.py（格子・門・校正帯が共有）／走行記録の読み出し→runs_A.py（器材が共有）／z→zaxis_A.py／走行→run_preamble_local.py v2.7・boot_stageA.py／門0.5→identity_screen_A.py／検閲・解釈条項・確証規則・refuse 門・様式門・錨帯・測定不能・環境保留・測れた効果種→analyze_A.py／応答様式 (a)(b) と言及→response_mode_A.py／校正帯とセッションのやり直し・撤退条件・門2→calib_band_A.py・gate_A.py／管理図→control_chart_A.py／転記行→design_facts_A.py・power_grid_A.py・cost_facts.py／Firth の基準実装と R logistf との一致検査→firth.py・firth_check_A.py・firth_check_A.R／本文の数の検査（束縛・登録・生成器）→numbers_lint.py／草案と雛形の組み立て→build_draftA.py／整合と抽出（率盲検）→integrity_A.py・sample_inspection_A.py／判定器の断片→judge_fragments_A.py／運用の解釈の記録→tooling_interpretations_A.py／合成検査→synth_A.py（札の全組合せ表の全行と集計器の経路）・synth_gates_A.py（門と校正の器）／報告→報告雛形の原稿と雛形・build_report_A.py・report_lint.py／凍結前の検分の束→bundle_prefreeze_A.py／凍結→freeze_A.py。**実在（SHA16）**: %s。**未整備**: %s。' % (
    '・'.join('%s %s' % e for e in exist), '・'.join(still) or 'なし'), 'data': {'exist': dict(exist), 'not_yet': still}}

# ---- K: 引数・seed・tag
S_ = T['seeds']
F['K'] = {'text': '引数文字列 `--arms %s`（SHA16 %s・%d 腕）。seed: 門0.5 %d／パイロット %d〜（機種 × 場面）／本走行 %d〜／錨反復 %d〜（規模 × 場面）／橋 %s／校正 %d を基に %s（倍率 %d・橋の番号 %s）／API 再走行 %s／Firth 一致検査 %d／測れた効果種の到達の再計算 %d／dry-run %d。tag: %s。' % (
    T['arms']['arms_string'], sha_str(T['arms']['arms_string']), len(ARMS), S_['identity'], min(v for d in S_['pilot'].values() for v in d.values()), min(v for d in S_['main'].values() for v in d.values()),
    min(v for d in S_['anchor_rerun'].values() for v in d.values()), json.dumps(S_['bridge']), S_['calibration']['base'], S_['calibration']['rule'], S_['calibration']['multiplier'], json.dumps(S_['calibration']['bridge_index']), json.dumps(S_['api_rerun']), S_['firth_check'], S_['measurable_reach'], S_['dryrun'], json.dumps(T['tags'], ensure_ascii=False))}

# ---- M: 環境帯
M = PG['M']; EB = T['environment_band']; cands = sorted(M['candidates'], key=int)
assert EB['band_pt'] is None or EB['band_pt'] == M['selected_by_rule'], ('登録した環境帯と選択規則の候補が不一致', EB['band_pt'], M['selected_by_rule'])
F['M'] = {'text': '環境帯（橋の %s・本走行の %s 対 橋・n=%d 同士・腕ごと・「超」・厳密・真の率は 4B-2507 の API 既測〔%s〕・既測の無い腕は %s）: %s。**選択規則（確証 %d 対比の期待誤保留数が %s 以下となる最小の候補）で選ばれる候補 %s pt**（%s）。真の率の置き方への依存（全腕を同じ率に置いた期待誤保留数）: %s。' % (
    '・'.join(M['bridge_models']), T['bridge']['scenario'], M['n'], T['bridge']['scenario'], EB['rule_missing_base_rate'],
    '／'.join('%s pt: 腕あたり（真の率 %s）%s・確証族に現れる %d 腕のいずれかが超える確率 %.3f（全 %d 腕では %.3f）・期待誤保留数 %.2f・検出 %s' % (b, EB['rule_missing_base_rate'], sci(M['candidates'][b]['per_arm_at_05']), len(M['family_arms']), M['candidates'][b]['p_any_family_arm_any_model'], len(M['arm_rates_used']), M['candidates'][b]['p_any_arm_any_model'], M['candidates'][b]['expected_false_held_contrasts'],
                                                                   '・'.join('差 %s pt で %.3f' % (s_, v) for s_, v in M['candidates'][b]['detection_by_shift_pt'].items())) for b in cands),
    len(CONTR), EB['rule_expected_max'], M['selected_by_rule'], EB['selection_rule_side'], '／'.join('全腕 %g で %s' % (x['all_arms_rate'], '・'.join('%s pt %.3f' % (b, v) for b, v in x['expected_false_held_by_candidate'].items())) for x in M['rate_dependence'])) +
    (('**登録値 %d pt**・%s・選択規則の候補と一致: %s。保留の単位: %s。片側: %s。パイロット後: %s。' % (EB['band_pt'], EB['status'], EB['band_pt'] == M['selected_by_rule'], EB['hold'], EB['one_side_rule'], EB['pilot_recheck'])) if EB['band_pt'] is not None else ''), 'data': M}

# ---- N: 門0.5 の帰無の不合格率・登録の値・検出側
N_ = PG['N']; IS = T['identity_screen']; ND = PG['N_detection']
reg = N_['n%d_api_resampled' % n_id]
F['N'] = {'text': '門0.5 同一性選別の帰無の不合格率（両スタックが同じ分布でも主判定〔%d 個の絶対差の平均 %d 超または最大 %d 超〕に落ちる確率・%s の API 既測を真の分布とする・B=%d）: %s。**登録の値**: %.3f（手元 n=%d・API も再標本・%s）。検出側（手元で一つの腕の破局率だけがずれるとき・n=%d・B=%d・%s）: %s。登録値 n=%d（登録者裁定 D7）。' % (
    IS['n_differences'], IS['mean_pt'], IS['max_pt'], IS['scenario'], PG['B']['N'], '・'.join('手元 n=%d・%s: %.3f（最大絶対差の %g パーセンタイル %.1f pt）' % (v['n_local'], {'api_fixed': 'API を固定', 'api_resampled': 'API も再標本'}[v['mode']], v['fail_rate'], v['quantile'] * 100, v['max_abs_diff_p95']) for v in N_.values()),
    reg['fail_rate'], n_id, IS['null_fail_registered'], n_id, PG['B']['N'], ND['note'], '・'.join('%s %+d pt で API を固定 %.3f・再標本 %.3f' % ('全腕' if r['arm'] == 'all' else r['arm'], r['shift_pt'], r['fail_rate_api_fixed'], r['fail_rate_api_resampled']) for r in ND['rows']), n_id), 'data': {'null': N_, 'detection': ND, 'registered': reg}}

# ---- O: 判定器の妥当性の推定の幅
JVg = PG['JV']
F['O'] = {'text': '判定器の方向別の誤判定率の規模間の差の推定の幅（機種 × 場面 n=%d・%d 場面を合わせる・%s）: %s。自動の保留規則は置かない（登録者裁定 D13）。%s' % (
    JVg['n_per_cell'], JVg['scenarios'], JVg['method'], '・'.join('類の割合 %g・誤判定率 %g で ±%.1f pt' % (r['class_share'], r['true_error_rate'], r['diff_halfwidth95_pt']) for r in JVg['rows']), T['judge_validity']['reading_clause']), 'data': JVg}

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
outj = {'generated_utc': now, 'generator': 'tools/design_facts_A.py v3.3', 'contrasts_sha16': sha_file(CPATH), 'power_grid_json_sha16': sha_file(a.pg),
        'inputs_F_G': {'cost_facts': [os.path.relpath(CF_PATH, REPO).replace(os.sep, '/'), sha_file(CF_PATH)], 'style_stageF1': [os.path.relpath(sp, REPO).replace(os.sep, '/'), sha_file(sp) if os.path.isfile(sp) else None]}, 'z': {k: round(Z[k], 6) for k in SIZES}, 'dev_marks': DEV, 'facts': F}
os.makedirs(os.path.dirname(a.out), exist_ok=True)
json.dump(outj, open(a.out + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
L = ['# 段階 A 設計事実（機械生成・`tools/design_facts_A.py` v3.3・%s UTC・正本 contrasts-A.json SHA16 %s・格子 power-grid-A.json SHA16 %s・転記行 F の入力 SHA16 %s・転記行 G の入力 SHA16 %s%s）' % (now, outj['contrasts_sha16'], outj['power_grid_json_sha16'], outj['inputs_F_G']['cost_facts'][1], outj['inputs_F_G']['style_stageF1'][1], ('・**検査用の印 %s**' % '・'.join(DEV)) if DEV else ''), '']
for k in sorted(F):
    L.append('- **転記行 %s** — %s' % (k, F[k]['text'])); L.append('')
L.append('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[design_facts_A v3.3] written %s.{md,json}%s' % (a.out, (' dev_marks=' + ','.join(DEV)) if DEV else ''))
