# -*- coding: utf-8 -*-
"""design_facts_A.py v1 —— 段階 A の設計事実（転記行 A〜M）を `design/contrasts-A.json`・`records/A/power-grid-A.json`・`records/A/hf-models-A.json`・`records/cost-pilot/cost-facts-2026-09-13.md` の係数から機械生成する（2026-09-13）。
本文（草案4／凍結文書）はこの出力を転記するだけで、散文中に手計算の数を書かない。出力: records/A/design-facts-A.md と同 .json。
転記行: A 規模／B 対比／C 検閲の誤判率と残り方の偏り／D 傾きの検出力と実サイズ／E 床持続の三段／F 費用と時間／G 様式門の一斉保留の見込み／H 錨帯の帰無発火率／I 校正腕と撤退条件／J 凍結射程と器材の対応表／K 引数文字列の SHA・seed・tag／L 機種別の容量・実パラメータ数・収容／M 環境差の帯と手元系列の校正帯。
"""
import os, sys, json, math, hashlib, datetime
from scipy.stats import binom
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-A.json'), encoding='utf-8')); n, pn, n_id, n_cal = T['n_per_arm'], T['pilot_n'], T['identity_n'], T['calibration_n']
PG = json.load(open(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'), encoding='utf-8'))
HF = json.load(open(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), encoding='utf-8'))
SC = T['scenarios']; ARMS = T['arms']['preamble']; SIZES = T['sizes']; MODELS = T['models']; F = {}
sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
# ---- 費用の係数（門0 の実測・cost-facts §R: 料率と試行/時・経費）
COST = {'L4': {'units_per_h': 2.67, 'trials_per_h': 3839, 'setup_s': 512}, 'A100': {'units_per_h': 12.82, 'trials_per_h': 19200, 'setup_s': 465}}   # cost-facts-2026-09-13.md U／R の転記
SIZE_FACTOR = {'0.6B': 0.25, '1.7B': 0.5, '4B': 1.0, '4B-2507': 1.0, '8B': 2.0, '14B': 3.5, '32B': 8.0}   # 4B 比の試行時間の仮定（◐・パイロットで置換）
SESSION_H = 8.0
# ---- L: 実パラメータ数・容量・収容
def params(c):
    h, L, i, nh, nkv, hd, V = c['hidden_size'], c['num_hidden_layers'], c['intermediate_size'], c['num_attention_heads'], c['num_key_value_heads'], c['head_dim'], c['vocab_size']
    attn = h * nh * hd + 2 * h * nkv * hd + nh * hd * h + 2 * hd; mlp = 3 * h * i; per = attn + mlp + 2 * h
    return V * h * (1 if c.get('tie_word_embeddings') else 2) + L * per + h
P = {k: params(v) for k, v in HF['models'].items()}; z = {k: round(math.log(P[k] / P['4B']), 4) for k in SIZES}
KV_TOK = 2048
kv_tok = {k: 2 * v['num_hidden_layers'] * v['num_key_value_heads'] * v['head_dim'] * 2 for k, v in HF['models'].items()}
fit = {}
for k, v in HF['models'].items():
    need = v['safetensors_gib'] + kv_tok[k] * KV_TOK * 24 / 2**30 + 1.5   # KV は同時 24 要求 × 実効トークン（門0 の実測: prompt 中央値 462＋出力 p90 660 → 2,048 を上限の目安に）
    fit[k] = {'params_M': round(P[k] / 1e6, 1), 'z': z.get(k, 0.0), 'weights_gib': v['safetensors_gib'], 'kv_24x2048_gib': round(kv_tok[k] * KV_TOK * 24 / 2**30, 2), 'need_gib': round(need, 2),
              'fits_L4': need <= HF['gpu_gib']['L4'] * 0.90, 'fits_A100_40': need <= HF['gpu_gib']['A100-40GB'] * 0.90, 'fits_A100_80': need <= HF['gpu_gib']['A100-80GB'] * 0.90, 'rev': v['rev']}
bridge = ['4B'] + (['8B'] if fit['8B']['fits_L4'] else [])
F['L'] = {'text': '機種別（HF 2026-09-13・実パラメータ数は config.json から機械計算・収容＝重み＋KV〔2,048 トークン × 同時 24〕＋1.5 GiB が GPU の 90% 以内・4B の L4 収容は門0 で実測済み）: ' + '／'.join(
    '%s: rev %s・%s M params・z=%.4f・重み %.2f GiB・要 %.2f GiB・L4 %s・A100-40 %s・A100-80 %s' % (k, fit[k]['rev'], fit[k]['params_M'], fit[k]['z'], fit[k]['weights_gib'], fit[k]['need_gib'], '可' if fit[k]['fits_L4'] else '不可', '可' if fit[k]['fits_A100_40'] else '不可', '可' if fit[k]['fits_A100_80'] else '不可') for k in ['0.6B', '1.7B', '4B', '8B', '14B', '32B', '4B-2507']) + '。**橋のセルの機種＝%s**（8B は L4 に%s）。**14B は A100-40GB に載らず 80GB の割当が要る。32B は同時要求 24 では 80GB にも載らず、同時要求 8 なら要 %.2f GiB で 80GB に載る（同時要求数は機種の環境列に記帳・処理量は落ちる）。**' % ('・'.join(bridge), '収容できる' if fit['8B']['fits_L4'] else '収容できない', HF['models']['32B']['safetensors_gib'] + kv_tok['32B'] * KV_TOK * 8 / 2**30 + 1.5), 'data': fit, 'bridge': bridge}
# ---- A: 規模
n_models = len(MODELS); n_arms = len(ARMS); n_sc = len(SC)
t_id = n_id * n_arms; t_pilot = n_models * n_sc * n_arms * pn; t_main = n_models * n_sc * n_arms * n; t_anchor = n_models * n_sc * 2 * n
t_calib = n_models * n_cal * 2; t_bridge = len(bridge) * n_arms * n * 2; t_api = 3 * n_arms * n
t_total_local = t_id + t_pilot + t_main + t_anchor + t_calib + t_bridge
F['A'] = {'text': '規模: 門0.5 同一性選別 %s（N1 × 13 腕 × n=80）／パイロット %s（7 機種 × 5 場面 × 13 腕 × n=40）／本走行 %s（7 機種 × 5 場面 × 13 腕 × n=200）／錨反復 %s（7 機種 × 5 場面 × 2 腕 × n=200）／校正腕 %s（7 機種 × 2 セッション想定 × n=400・セッション数は実走で置換）／橋のセル %s（%s × 13 腕 × n=200 × 2 環境）＝**手元合計 %s 試行**。API 再走行（門0.5 合格時のみ）%s（8B・14B・32B × N1 × 13 腕 × n=200）。' % (
    format(t_id, ','), format(t_pilot, ','), format(t_main, ','), format(t_anchor, ','), format(t_calib, ','), format(t_bridge, ','), '・'.join(bridge), format(t_total_local, ','), format(t_api, ',')),
    'data': {'identity': t_id, 'pilot': t_pilot, 'main': t_main, 'anchor_rerun': t_anchor, 'calibration': t_calib, 'bridge': t_bridge, 'total_local': t_total_local, 'api_rerun': t_api}}
# ---- B: 対比
fam = T['families']['A_slope']; desc = T['descriptive_families']; conf_n = len(fam['contrasts']); desc_n = sum(len(v.get('contrasts', [])) for v in desc.values()) + len(desc['A_desc_floor']['cells'])
ids = [c['id'] for c in fam['contrasts']] + [c['id'] for v in desc.values() for c in v.get('contrasts', [])]; assert len(ids) == len(set(ids))
measured = sum(1 for c in fam['contrasts'] if c['base_A_4B2507'] is not None and c['base_B_4B2507'] is not None)
F['B'] = {'text': '対比: 確証 %d（傾きの族・7 効果種 × 5 場面・m=%d 固定・両側）・記述 %d（Nstr−Onull 5・Ncold−N 5・床持続 15 セル列・レシピ対 65・様式／錨差／スタック差／環境差は走行後に生成）・id の重複 0・対比が要求する腕の不在 0・登録対比を持たない腕 0。確証 35 本のうち 4B-2507 の API 既測で両腕の基底を持つもの %d（Odose1・Odosehalf を含む 10 本と N2 の Ncold 系 5 本は既測なし・仮定基底）。' % (conf_n, fam['m'], desc_n, measured),
          'data': {'confirmed': conf_n, 'm': fam['m'], 'descriptive': desc_n, 'measured_bases': measured}}
# ---- C: 検閲の誤判率（4B 既測基底＋仮定基底・両腕条件・規模単位・n=200）
lo, hi = T['censor']['low'], T['censor']['high']
def p_out(p):   # 1 セルが <lo または >hi に落ちる確率（n=200）
    return float(binom.cdf(math.ceil(lo * n) - 1, n, p) + binom.sf(math.floor(hi * n), n, p))
def p_censored_pair(pc, pt):   # 両腕条件で落ちる確率（両方 <lo または 両方 >hi）
    a = float(binom.cdf(math.ceil(lo * n) - 1, n, pc)) * float(binom.cdf(math.ceil(lo * n) - 1, n, pt)); b = float(binom.sf(math.floor(hi * n), n, pc)) * float(binom.sf(math.floor(hi * n), n, pt)); return a + b
grid = [0.02, 0.05, 0.20, 0.50, 0.80, 0.95, 0.98]; rows = []
for pc in grid:
    for eff in (0.0, 0.09, -0.09, 0.15, -0.15):
        pt = min(max(pc + eff, 0.001), 0.999); rows.append({'ctrl': pc, 'effect_pt': eff, 'p_censor': round(p_censored_pair(pc, pt), 4)})
meas = []
for c in fam['contrasts']:
    if c['base_A_4B2507'] is not None and c['base_B_4B2507'] is not None:
        pa, pb = c['base_A_4B2507'] / c['base_n_A'], c['base_B_4B2507'] / c['base_n_B']; meas.append({'id': c['id'], 'p_censor_at_4B_bases': round(p_censored_pair(pb, pa), 4)})
n_cens_4b = sum(1 for m in meas if m['p_censor_at_4B_bases'] > 0.5)
F['C'] = {'text': '検閲の誤判率（両腕条件・n=200・規模単位・二項）: 帰無（効果 0）で両腕が同じ基底 p にあるとき落ちる確率は p=0.02 で %.3f・0.05 で %.3f・0.20 で %.3f・0.50 で %.3f・0.80 で %.3f・0.95 で %.3f・0.98 で %.3f。真の効果 +9pt（床側）・−9pt（天井側）・±15pt（中間）を持つ対比が落ちる確率は格子の表（design-facts-A.json C.grid）。4B-2507 の API 既測の基底では、確証 35 本のうち 4B の規模で検閲される見込み（>0.5）の対比は %d 本（%s）。**残り方の偏り**: 検閲は両腕が同時に床（O 族・Nk・Osec-Ncold の床側）または天井（N・Ncold・Onull-Ncold の天井側）に落ちる規模で起き、小規模では書式外による測定不能が、大規模では天井が先に立つ見込み——上端・下端のどちらを欠くかは効果種で異なり、報告は残った規模の一覧を機械印字する。' % (
    tuple(round(p_censored_pair(p, p), 3) for p in grid) + (n_cens_4b, '・'.join(m['id'] for m in meas if m['p_censor_at_4B_bases'] > 0.5) or 'なし')), 'grid': rows, 'measured': meas}
# ---- D: 傾きの検出力と実サイズ
D = PG['D']; sel = lambda pat, d0, D_: next(r for r in D if r['pattern'] == pat and r['d0_pt'] == d0 and r['delta_pt_32B_minus_4B'] == D_)
size_rows = [r for r in D if r['delta_pt_32B_minus_4B'] == 0.0]
F['D'] = {'text': '傾きの族の検出力と実サイズ（Firth PPLRT 両側・n=200 × 6 規模・両腕条件の検閲後・B=%d・seed %d・z は転記行 L の実値）: 型 I 誤りの実サイズ（Δ=0）は対照中間 %.3f・床 %.3f・天井 %.3f・対照が規模で動く %.3f（名目 0.05）。検出力（p<0.05／Holm 初段 p<0.05/35）: 対照中間で Δ=10pt %.2f／%.2f・15pt %.2f／%.2f・20pt %.2f／%.2f・30pt %.2f／%.2f。対照が床（0.03）では Δ=15pt %.2f／%.2f（解釈条項の発火率 %.2f・判定不能率 %.2f）、対照が天井（0.97）では Δ=−15pt 相当の設定で %.2f／%.2f（発火率 %.2f）。**対照が規模で動く（0.3→0.9）とき処置が平坦なら（d0=0.15・Δ=0）の実サイズ %.3f・解釈条項の発火率 %.2f**。検出できるのは 4B〜32B 間で 15〜20 pt 級以上の pt 差の変化であり、10 pt 級は検出域外。**尺度依存の先置**: β₃ は対数オッズ尺度の交互作用であり、対照の基底が規模で動くとき処置との pt 差が一定でも β₃≠0 になる（上の 0.407 はその型で、偽陽性ではなく尺度の違い）。確証札の隣に pt 差の規模傾向（記述・傾向検定）を機械印字し、pt 差の傾きの区間が 0 を含む対比には「尺度依存」の注を付す（読み条項 (xiv)）。' % (
    PG['B'], PG['seed'], sel('mid_const', 0.0, 0.0)['reject_005'], sel('floor_const', 0.0, 0.0)['reject_005'], sel('ceiling_const', 0.0, 0.0)['reject_005'], sel('ctrl_rising', 0.0, 0.0)['reject_005'],
    sel('mid_const', 0.0, 0.10)['reject_005'], sel('mid_const', 0.0, 0.10)['reject_holm_first'], sel('mid_const', 0.0, 0.15)['reject_005'], sel('mid_const', 0.0, 0.15)['reject_holm_first'], sel('mid_const', 0.0, 0.20)['reject_005'], sel('mid_const', 0.0, 0.20)['reject_holm_first'], sel('mid_const', 0.0, 0.30)['reject_005'], sel('mid_const', 0.0, 0.30)['reject_holm_first'],
    sel('floor_const', 0.0, 0.15)['reject_005'], sel('floor_const', 0.0, 0.15)['reject_holm_first'], sel('floor_const', 0.0, 0.15)['interp_clause_rate'], sel('floor_const', 0.0, 0.15)['undecidable_rate'],
    sel('ceiling_const', 0.0, 0.15)['reject_005'], sel('ceiling_const', 0.0, 0.15)['reject_holm_first'], sel('ceiling_const', 0.0, 0.15)['interp_clause_rate'], sel('ctrl_rising', 0.15, 0.0)['reject_005'], sel('ctrl_rising', 0.15, 0.0)['interp_clause_rate']), 'data': D}
# ---- E
E = PG['E']; er = {str(r['true_rate']): r for r in E['rows']}
F['E'] = {'text': '床持続（記述）の到達可能性（n=200・棄却域 k≤%d〔CP 95%% 片側上限 <0.05・H0 での実サイズ %.4f〕）: 真の率 0.005／0.01／0.02／0.03 で 単一セル %.3f／%.3f／%.3f／%.3f・6 規模同時 %.3f／%.3f／%.3f／%.4f・Holm 初段（k≤%d・m=15 のとき）%.3f／%.3f／%.5f／%.6f。記述に降格したため多重補正は課さず、各セルの CP 上限と全規模 0/1 を印字する。0/1 が 0 であることを「床を離れた」と読まない。' % (
    E['k_max_cp95_n200'], E['p_size_k_le_4'], er['0.005']['single_cell_k_le_4'], er['0.01']['single_cell_k_le_4'], er['0.02']['single_cell_k_le_4'], er['0.03']['single_cell_k_le_4'],
    er['0.005']['six_sizes_joint'], er['0.01']['six_sizes_joint'], er['0.02']['six_sizes_joint'], er['0.03']['six_sizes_joint'], E['k_max_holm_first_n200'], er['0.005']['holm_first_stage_k_le_2'], er['0.01']['holm_first_stage_k_le_2'], er['0.02']['holm_first_stage_k_le_2'], er['0.03']['holm_first_stage_k_le_2']), 'data': E}
# ---- F: 費用（cost_facts §P の形・料率 × 本走行時間 ＋ セッション数 × 経費・機種比は仮定 ◐）
def hours_for(model_key, trials):
    return trials * SIZE_FACTOR[model_key] / COST[T['environments'][model_key]]['trials_per_h']
per_model = {}
for m in MODELS:
    k = m['key']; env = T['environments'][k]; tr = n_sc * n_arms * (pn + n) + n_sc * 2 * n + n_cal * 2 + (n_arms * n * 2 if k in bridge else 0)
    h = hours_for(k, tr); sess = math.ceil(h / (SESSION_H - COST[env]['setup_s'] / 3600)); h_tot = h + sess * COST[env]['setup_s'] / 3600; u = h_tot * COST[env]['units_per_h']
    per_model[k] = {'env': env, 'trials': tr, 'hours_run': round(h, 2), 'sessions': sess, 'hours_total': round(h_tot, 2), 'units': round(u, 1)}
u_tot = sum(v['units'] for v in per_model.values()); h_tot = sum(v['hours_total'] for v in per_model.values())
F['F'] = {'text': '費用と時間（門0 の実測係数〔L4 2.67 ユニット/h・3,839 試行/h・経費 512 s／A100 12.82・19,200・465 s〕× 4B 比の試行時間の仮定 %s ◐・セッション 8 時間・機種別の環境）: ' % json.dumps(SIZE_FACTOR, ensure_ascii=False) + '／'.join('%s: %s 試行・%.1f h・%d セッション・%.1f ユニット' % (k, format(v['trials'], ','), v['hours_total'], v['sessions'], v['units']) for k, v in per_model.items()) + '。**合計 ≈%.0f ユニット・≈%.0f 時間**（v2.3 §6 の見込み A ≈84〜81 と同じ桁・32B の係数 8 と A100 80GB の割当は仮定）。門0.5・API 再走行・判定器の断片は含まない。パイロットで機種ごとの実測に置き換える。' % (u_tot, h_tot), 'data': per_model, 'total_units': round(u_tot, 1), 'total_hours': round(h_tot, 1)}
# ---- G: 様式門の一斉保留の見込み（既測の (b) JSON 直答率・F の style 記録から取れる腕のみ）
G = {}
for tag in ('style-stageF1.json',):
    p = os.path.join(REPO, 'records', 'F', tag)
    if os.path.isfile(p):
        S = json.load(open(p, encoding='utf-8'))
        for sc, runs in S['runs'].items():
            for arm, v in runs.items():
                if arm in ARMS and isinstance(v, dict) and 'b' in v:
                    G.setdefault(sc, {})[arm] = v['b'].get('rate') if isinstance(v['b'], dict) else v['b']
F['G'] = {'text': '様式門の一斉保留の見込み: 既測の (b) JSON 直答率は段階 F の様式記録（4B-2507・U 腕 N・Ncold・O-Ncold・4 場面）にのみあり、他の 10 腕と N2 は既測なし。取れた値: %s。腕別・規模別の (b) 率はパイロットで転記し、30 pt 超の見込み本数を凍結前に置き換える（この転記行は仮）。' % (json.dumps(G, ensure_ascii=False) if G else '様式記録の形式が想定と異なり取得できず（パイロットで置換）'), 'data': G}
# ---- H・I・M
H = PG['H']; F['H'] = {'text': '錨帯の帰無発火率（n=200 × 2 走行・二項の差・真の率 0.1／0.3／0.5／0.7／0.9）: 帯 10 pt で %s・12 pt で %s・15 pt で %s。対 %d 本（5 場面 × 6 規模 × 2 腕）で真の率 0.5 のときの帰無での除外の期待本数は 10 pt %.1f・12 pt %.1f・15 pt %.1f。**帯の既定 10 pt は真の率 0.5 で片側 5%% を超える（両側 %.3f）ため、凍結前に 12 pt または 15 pt を裁定する**。' % (
    H['per_pair_null_fire']['10'], H['per_pair_null_fire']['12'], H['per_pair_null_fire']['15'], H['n_pairs'], H['expected_false_exclusions_at_p05']['10'], H['expected_false_exclusions_at_p05']['12'], H['expected_false_exclusions_at_p05']['15'], H['per_pair_null_fire']['10']['0.5']), 'data': H}
I = PG['I']; F['I'] = {'text': '校正腕（4B-2507 × Ncold × N1・n=400・API 既測 %.3f・5 pt 帯）: 発火境界 ≤%s または ≥%s・帰無発火率 %.3f。撤退条件（パイロット n=40・15 pt 帯・同じ基底）: 発火境界 ≤%s または ≥%s・帰無発火率 %.3f。門2 の誤判率は転記行 C の検閲確率と検出力格子から: n=40 では両腕条件の閾値が 2/40・38/40 に相当し、帰無で落ちる確率は転記行 C の p=0.02・0.98 の行を n=40 で引き直した値（design-facts-A.json I.gate2）。' % (
    I['calibration']['base_api'], I['calibration']['fire_if_le'], I['calibration']['fire_if_ge'], I['calibration']['null_fire'], I['withdrawal_pilot']['fire_if_le'], I['withdrawal_pilot']['fire_if_ge'], I['withdrawal_pilot']['null_fire']),
    'data': I, 'gate2': {str(p): round(float(binom.cdf(math.ceil(lo * pn) - 1, pn, p) ** 2 + binom.sf(math.floor(hi * pn), pn, p) ** 2), 4) for p in grid}}
M = PG['M']; F['M'] = {'text': '環境差の帯（橋のセル・n=200 × 2 環境・腕ごと・真の率 0.1〜0.9）: 帯 10 pt で %s・12 pt で %s・15 pt で %s（13 腕 × %d 機種）。手元系列の校正帯（門0.5 不合格時・n=400 同士・同じ二項の差）は帯 5 pt で真の率 0.95 のとき帰無発火率 %.3f。帯の値は凍結前に裁定。' % (
    M['per_arm_null_fire_two_env']['10'], M['per_arm_null_fire_two_env']['12'], M['per_arm_null_fire_two_env']['15'], len(bridge), float((abs(__import__('numpy').random.default_rng(1).binomial(400, 0.95, 20000) - __import__('numpy').random.default_rng(2).binomial(400, 0.95, 20000)) / 400 >= 0.05).mean())), 'data': M}
# ---- J・K
F['J'] = {'text': '凍結射程と器材の対応表: 腕・場面・環境→contrasts-A.json／走行→run_preamble_local.py v2.7・boot_stageA.py／門0.5→identity_screen_A.py／検閲・解釈条項・refuse 門・様式門・錨帯・測定不能・環境副次→analyze_A.py／校正帯・撤退→calib_band_A.py・gate_A.py／管理図→control_chart_A.py／転記行→design_facts_A.py・power_grid_A.py・cost_facts.py／整合→integrity_A.py・sample_inspection_A.py／報告→template・build_report_A.py・report_lint／凍結→freeze_A.py。**本草案4 時点で実在する器材: make_contrasts_A.py・firth.py・power_grid_A.py・design_facts_A.py・cost_facts.py・run_preamble_local.py・boot_cost_pilot.py（boot_stageA の型）。残りは凍結前に整備し dry-run と合成データで検査する。**'}
F['K'] = {'text': '引数文字列 `--arms %s`（SHA16 %s・13 腕）。seed: 門0.5 %d／パイロット 61xxx（機種 × 場面）／本走行 62xxx／錨反復 63xxx／橋 %s／校正 %d／API 再走行 %s／dry-run %d。tag: %s。' % (
    T['arms']['arms_string'], sha(T['arms']['arms_string']), T['seeds']['identity'], json.dumps(T['seeds']['bridge']), T['seeds']['calibration'], json.dumps(T['seeds']['api_rerun']), T['seeds']['dryrun'], json.dumps(T['tags'], ensure_ascii=False))}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
os.makedirs(os.path.join(REPO, 'records', 'A'), exist_ok=True)
json.dump({'generated_utc': now, 'contrasts_sha16': sha(open(os.path.join(REPO, 'design', 'contrasts-A.json'), encoding='utf-8').read()), 'z': z, 'facts': F}, open(os.path.join(REPO, 'records', 'A', 'design-facts-A.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 A 設計事実（機械生成・`tools/design_facts_A.py` v1・%s UTC・正本 contrasts-A.json SHA16 %s）' % (now, sha(open(os.path.join(REPO, 'design', 'contrasts-A.json'), encoding='utf-8').read())), '']
for k in 'ABCDEFGHIJKLM':
    L.append('- **転記行 %s** — %s' % (k, F[k]['text'])); L.append('')
L.append('本ファイルのいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
open(os.path.join(REPO, 'records', 'A', 'design-facts-A.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[design_facts_A] written records/A/design-facts-A.{md,json}')
