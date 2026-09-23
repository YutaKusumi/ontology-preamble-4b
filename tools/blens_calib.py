# -*- coding: utf-8 -*-
"""blens_calib.py v1 —— B-lens の層二（校正の門と大きさの目盛り・2026-09-23・正本 §4・裁定 D169・D170・D180・D181）。

門（正本 `calibration`）:
  - 行: B の本走行の方向ごとの行（凍結した集計器の記録 `by_direction`）のうち、土台の無操作の腕の破局が零でも全部でもない行。
  - 行動の量: その行の破局の対数オッズ − 土台の無操作の腕の破局の対数オッズ（件数に連続性の補正）。直接の押し: 腕の符号 × 物差しの値（選んだ層・方向・場面の家族）。
  - 門: 行の単位の順位相関を、方向を単位にした全ての入れ替えで片側に（M_L と M_X・Holm 段の数 2・p < 段）。v̂ を抜いた門（static の行を除く・六本）と、
    v̂ と (6b) を抜いた五本の門（記述）。行の数が正本と違えば止める。
  - 記述: 行の単位の順位相関・ランダム方向の行だけの順位相関・崩れの行を除いた門・調整走行の方向の順位・S4 の自然の対照。
大きさの目盛り（正本 `magnitude`・Colab の起動器 `tools/colab/boot_Blens.py` の相 extract の出力を読む）:
  - 手元の logits の突き合わせ（最初の一件・許容 `logit_check.atol`・最上位の語が同じ）。外れたら止める。
  - 正確な直接の経路 W_E·(g⊙[(h+αu)/rms(h+αu) − h/rms(h)])（α u は B で加えた量・腕の符号つき）と、その分け方（層一の近似・残差に沿う部分・尺度）。
  - 主位置の比（下限を超えた行だけ）: B の標本化の変換の後の「```」の確率の変化 ÷ 観測の様式の率の変化。対数オッズの比は記述（変換の後の確率が零か一なら出さない）。
  - 答えの文字の位置は記述だけ（比は出さない）。層一の M_L と正確な直接の経路の順位の一致・方向と残差の余弦。
封印の前には走らない（凍結の記録と封印の記録）。
出力: results/Blens/calib-Blens.json（--force が無ければ上書きしない）。
用法: python tools/blens_calib.py --colab-dir <相 extract の出力の置き場> [--force] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, math, argparse, datetime, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C
import blens_lens as BL

VERSION = 'v1'
NL = chr(10)
OUT = os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json')
LENS = os.path.join(REPO, 'results', 'Blens', 'lens-Blens.json')
ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')
UNITS_NAMED = ('static', 'loaded', 'Nk', 'td')


def fam_of(TL):
    return {sc: f for f, scs in TL['metrics']['families'].items() for sc in scs}


def row_choice_counts(sc, arm):
    """試行の記録から、方向ごとの選択の数（崩れの行と JSON 直答の中の文字の数）。"""
    d = os.path.join(REPO, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
    out = collections.defaultdict(collections.Counter)
    for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8'):
        t = json.loads(l)
        if t['status'] != 'ok':
            continue
        did = t.get('direction_id') or 'fixed'
        out[did][t['choice']] += 1
        out[did]['_n'] += 1
        out[did]['_style'] += 1 if t['style_b'] else 0
        if t['style_b']:
            out[did]['_json'] += 1
            out[did]['json:' + t['choice']] += 1
    return out


def gate_rows(TL, BD, counts):
    """門の行（適格でない行も印をつけて返す）。counts: (場面, 腕) → 方向 → 選択の数。"""
    noop = TL['token_sets']['noop_arms']
    fam = fam_of(TL)
    base = {(r['scenario'], r['arm']): r for r in BD if r['arm'] in noop[r['scenario']]}
    cc = TL['calibration']['continuity']
    rows = []
    for r in BD:
        if r['arm'] in noop[r['scenario']]:
            continue
        m = ARM_RE.match(r['arm'])
        b = base[(r['scenario'], m.group(1))]
        c = counts[(r['scenario'], r['arm'])][r['direction_id']]
        if c['_n'] != r['n_ok']:
            raise SystemExit('試行の記録と集計の記録の件数が違う（止める）: %s %s %s' % (r['scenario'], r['arm'], r['direction_id']))
        collapse = bool(c['_n']) and max(c[x] for x in ('a', 'b', 'c', 'd', 'refuse')) == c['_n']
        rows.append({'scenario': r['scenario'], 'arm': r['arm'], 'base_arm': m.group(1), 'unit': r['direction_id'], 'sign': 1 if m.group(2) == '+' else -1,
                     'fam': fam[r['scenario']], 'eligible': 0 < b['cat'] < b['n_ok'], 'collapse': collapse,
                     'y': C.logit_cc(r['cat'], r['n_ok'], cc) - C.logit_cc(b['cat'], b['n_ok'], cc),
                     'k': r['cat'], 'n': r['n_ok'], 'k0': b['cat'], 'n0': b['n_ok']})
    return rows


def unit_values(values_of, metric, units, fams):
    """単位 → {家族: 物差しの値}。values_of(単位, 物差しの表の名) は選んだ層の値を返す。"""
    return {u: {f: values_of(u, '%s_%s' % (metric, f)) for f in fams} for u in units}


def link_metrics(gates, tests):
    """v̂ のある物差しの値を行動に結びつけてよい物差し: 同じ物差しが本の門と v̂ を抜いた門の両方を通ったときだけ（正本 calibration.link_rule）。"""
    return [m for m in tests if gates['full'][m]['pass'] and gates['without_vhat'][m]['pass']]


def gate_part(TL, rows, values_of):
    """門と記述の対照（読み込みをしない・合成データでも回る）。"""
    CAL = TL['calibration']
    fams = sorted(set(r['fam'] for r in rows))
    units_all = list(CAL['directions'])
    elig = [r for r in rows if r['eligible']]
    sets = collections.OrderedDict([('full', (units_all, elig)),
                                    ('without_vhat', ([u for u in units_all if u != 'static'], [r for r in elig if r['unit'] != 'static'])),
                                    ('without_vhat_loaded', ([u for u in units_all if u not in ('static', 'loaded')], [r for r in elig if r['unit'] not in ('static', 'loaded')]))])
    want = {'full': CAL['rows_gate'], 'without_vhat': CAL['rows_without_vhat'], 'without_vhat_loaded': CAL['rows_without_vhat_loaded']}
    got = {k: len(v[1]) for k, v in sets.items()}
    if got != want:
        raise SystemExit('門の行の数が正本と違う（止める・登録者に相談）: %s（正本 %s）' % (got, want))
    out = collections.OrderedDict()
    for name, (units, rs) in sets.items():
        res = collections.OrderedDict()
        for m in CAL['tests']:
            uv = unit_values(values_of, m, units, fams)
            res[m] = C.gate_perm(rs, uv, units)
        if name != 'without_vhat_loaded':
            H = C.holm({m: res[m]['p'] for m in CAL['tests']}, CAL['alpha'], CAL['holm_m'])
            for m in CAL['tests']:
                res[m].update({'holm_step': H[m]['step'], 'pass': bool(H[m]['pass'])})
        out[name] = res
    passed = [m for m in CAL['tests'] if out['full'][m]['pass']]
    link_vhat = link_metrics(out, CAL['tests'])
    desc = collections.OrderedDict()
    for m in CAL['tests']:
        uv = unit_values(values_of, m, units_all, fams)
        push = lambda rs: [r['sign'] * uv[r['unit']][r['fam']] for r in rs]
        rnd = [r for r in elig if r['unit'].startswith('rand:')]
        noc = [r for r in elig if not r['collapse']]
        desc[m] = {'row_rho': C.spearman(push(elig), [r['y'] for r in elig]),
                   'random_rows_rho': C.spearman(push(rnd), [r['y'] for r in rnd]) if len(rnd) > 2 else None,
                   'without_collapse': C.gate_perm(noc, uv, units_all), 'collapse_rows': ['%s|%s|%s' % (r['scenario'], r['arm'], r['unit']) for r in elig if r['collapse']]}
    return {'gates': out, 'gate_passed': bool(passed), 'passed_metrics': passed, 'link_vhat_metrics': link_vhat, 'descriptive': desc,
            'rows': [{k: v for k, v in r.items()} for r in rows]}


def s4_control(values_of):
    """S4 の自然の対照（記述）: 選んだ層で、(6b) と一本目が、M_F と M_Lc のそれぞれで、符号つきの値で四本の中の上の二本に来るか（偶然なら六分の一）。"""
    four = ['loaded', 'rand:0', 'rand:1', 'rand:2']
    out = {}
    for m in ('M_F', 'M_Lc'):
        vals = {u: values_of(u, m) for u in four}          # 四本とも S4 の Osec-Ncold の土台に「加える」腕
        top2 = sorted(four, key=lambda u: -vals[u])[:2]
        out[m] = {'values': vals, 'top2': top2, 'loaded_and_rand0_top2': set(top2) == {'loaded', 'rand:0'}}
    out['rand0_same_sign_as_loaded_MF'] = (out['M_F']['values']['rand:0'] > 0) == (out['M_F']['values']['loaded'] > 0)
    return out


def tune_part(TL, lens_layers):
    """調整走行の層ごとの方向（v̂ と三本のランダム方向を三つの層で）の、方向を単位にした順位（記述）。
    同じ場面 × 層 × 係数の組の中で、四本の方向を、行動（破局の対数オッズ）と直接の押し（M_L・M_X）で並べ、v̂ の順位と組の中の順位相関を印字する。"""
    fam = fam_of(TL)
    cc = TL['calibration']['continuity']
    grp = collections.defaultdict(lambda: collections.Counter())
    for f in glob.glob(os.path.join(REPO, 'results', 'tuneB', '*', 'trials-*.jsonl')):
        for l in open(f, encoding='utf-8'):
            t = json.loads(l)
            if t['status'] != 'ok':
                continue
            key = (t['scenario'], BL.rkey(t['layer']), t['coef'], t['direction_id'])
            grp[key]['n'] += 1
            grp[key]['cat'] += 1 if t['catastrophe'] else 0
    out = []
    for (sc, r, coef) in sorted(set(k[:3] for k in grp)):
        dirs_ = ['static', 'rand:0', 'rand:1', 'rand:2']
        if not all((sc, r, coef, d_) in grp for d_ in dirs_):
            continue
        y = {d_: C.logit_cc(grp[(sc, r, coef, d_)]['cat'], grp[(sc, r, coef, d_)]['n'], cc) for d_ in dirs_}
        row = {'scenario': sc, 'layer': r, 'coef': coef, 'y': y}
        for m in TL['calibration']['tests']:
            name = '%s_%s' % (m, fam[sc])
            push = {d_: lens_layers[r]['directions']['static' if d_ == 'static' else 'tune_' + d_][name]['value'] for d_ in dirs_}
            rank_b = sorted(dirs_, key=lambda d_: -y[d_]).index('static') + 1
            rank_p = sorted(dirs_, key=lambda d_: -push[d_]).index('static') + 1
            row[m] = {'push': push, 'vhat_rank_behaviour': rank_b, 'vhat_rank_push': rank_p, 'rho': C.spearman([push[d_] for d_ in dirs_], [y[d_] for d_ in dirs_])}
        out.append(row)
    return out


# ---------------- 大きさの目盛り ----------------
def magnitude_part(TL, rows, counts, ctx, H_main, H_letter, Zfull, g, dirs_sel, fmain, letters, values_of, eps, first_logits=None, Zfirst=None):
    """ctx: Colab の文脈の記録・H_main/H_letter: 残差（文脈 × d）・Zfull(H) → W_E·(g⊙h)（全語彙 × 本数）・dirs_sel: 単位 → 方向（選んだ層）。"""
    MG, SAMP = TL['magnitude'], TL['inputs']['sampling_B']
    coef = TL['layers']['coef_applied']
    out = {'logit_check_local': None}
    tr = lambda z: C.transform(z, SAMP['temperature'], SAMP['top_k'], SAMP['top_p'])
    # 手元の logits の突き合わせ（最初の一件）
    if first_logits is not None:
        chk = {}
        for pos, H_, fl in (('main', H_main, first_logits[0]), ('letter', H_letter, first_logits[1])):
            z0 = Zfull(H_[:1])[:, 0].astype(np.float64) / C.rms(H_[0], eps)
            chk[pos] = {'max_abs': float(np.max(np.abs(z0 - fl))), 'argmax_equal': int(np.argmax(z0)) == int(np.argmax(fl))}
        out['logit_check_local'] = chk
        if any(v['max_abs'] > MG['logit_check']['atol'] or not v['argmax_equal'] for v in chk.values()):
            raise SystemExit('手元の logits の突き合わせが外れた（止める・登録者に相談）: %s' % chk)
    units = list(dirs_sel)
    U = np.array([dirs_sel[u] for u in units], dtype=np.float32)
    ZU = Zfull(U).astype(np.float64)                          # 全語彙 × 方向
    cells = collections.OrderedDict()
    for k, c in enumerate(ctx):
        cells.setdefault((c['scenario'], c['arm']), []).append(k)
    ZH = Zfull(np.asarray(H_main, dtype=np.float32)[[v[0] for v in cells.values()]]).astype(np.float64)
    zh_cell = {key: ZH[:, j] for j, key in enumerate(cells)}
    hm_cell = {key: np.asarray(H_main[v[0]], dtype=np.float64) for key, v in cells.items()}
    spread = {('%s|%s' % key): float(max(np.max(np.abs(np.asarray(H_main[k], dtype=np.float64) - hm_cell[key])) for k in v)) for key, v in cells.items()}
    cc = MG['lower_bound']['continuity']
    main_rows = []
    for r in rows:
        key = (r['scenario'], r['base_arm'])
        c1 = counts[(r['scenario'], r['arm'])][r['unit']]
        c0 = counts[key]['fixed']
        d_obs, z = C.z_two_sample(c0['_style'], c0['_n'], c1['_style'], c1['_n'], cc)
        item = {'row': '%s|%s|%s' % (r['scenario'], r['arm'], r['unit']), 'unit': r['unit'], 'sign': r['sign'], 'z': z, 'obs_diff': d_obs,
                'p0_obs': c0['_style'] / c0['_n'], 'p1_obs': c1['_style'] / c1['_n'], 'eligible': abs(z) >= MG['lower_bound']['z_min'], 'base_in_strata': key in cells}
        if key in cells and r['unit'] in dirs_sel:
            j = units.index(r['unit'])
            dp = C.direct_path(zh_cell[key], ZU[:, j], hm_cell[key], dirs_sel[r['unit']], r['sign'] * coef, eps)
            pb, pa = tr(dp['before'])[fmain], tr(dp['after'])[fmain]
            item.update({'pT_before': float(pb), 'pT_after': float(pa), 'dp': float(pa - pb),
                         'parts_fmain': {k2: float(dp[k2][fmain]) for k2 in ('exact', 'layer1', 'along', 'scale')},
                         'cos_u_h': float(np.dot(dirs_sel[r['unit']], hm_cell[key]) / (np.linalg.norm(dirs_sel[r['unit']]) * np.linalg.norm(hm_cell[key])))})
            if item['eligible']:
                item['ratio'] = float((pa - pb) / d_obs)
                lo_obs = C.logit_cc(c1['_style'], c1['_n'], cc) - C.logit_cc(c0['_style'], c0['_n'], cc)
                if 0 < pb < 1 and 0 < pa < 1:
                    item['ratio_logodds'] = float((math.log(pa / (1 - pa)) - math.log(pb / (1 - pb))) / lo_obs)
                else:
                    item['ratio_logodds'], item['logodds_undefined'] = None, True
                item['rate_edge'] = c0['_style'] in (0, c0['_n']) or c1['_style'] in (0, c1['_n'])
                item['reading'] = '逆向き' if item['ratio'] < 0 else ('以上' if item['ratio'] >= MG['reading_ratio'] else '満たない')
        main_rows.append(item)
    elig = [x for x in main_rows if x['eligible']]
    miss = [x['row'] for x in elig if 'ratio' not in x]
    if miss:
        raise SystemExit('比を出す行の土台の升目が選び方の層に無い（止める）: %s' % miss)
    vhat_elig = [x['row'] for x in elig if x['unit'] == 'static']
    if vhat_elig:
        raise SystemExit('v̂ の行に比を出す行がある——正本の「v̂ の行では比が出ない」が成り立たない（止める）: %s' % vhat_elig)
    out['main_rows'] = main_rows
    out['summary'] = {'ratio_rows': len(elig), 'at_or_above': sum(1 for x in elig if x['reading'] == '以上'), 'below': sum(1 for x in elig if x['reading'] == '満たない'),
                      'reverse': sum(1 for x in elig if x['reading'] == '逆向き'), 'reading_ratio': MG['reading_ratio'], 'h_main_spread_within_cell': spread}
    # 答えの文字の位置（記述）
    ZL = Zfull(np.asarray(H_letter, dtype=np.float32)).astype(np.float64)
    letter = collections.OrderedDict()
    fam = fam_of(TL)
    for key, ks in cells.items():
        sc, arm = key
        lt = TL['metrics']['letters'][fam[sc]]
        rel_rows = [r for r in rows if (r['scenario'], r['base_arm']) == key and r['unit'] in dirs_sel]
        per = collections.OrderedDict()
        for r in rel_rows:
            j = units.index(r['unit'])
            vals = collections.defaultdict(list)
            for k in ks:
                h = np.asarray(H_letter[k], dtype=np.float64)
                dp = C.direct_path(ZL[:, k], ZU[:, j], h, dirs_sel[r['unit']], r['sign'] * coef, eps)
                pb, pa = tr(dp['before']), tr(dp['after'])
                sb, sa = C.transform(dp['before'], 1.0, dp['before'].size, 1.0), C.transform(dp['after'], 1.0, dp['after'].size, 1.0)
                for x in ('a', 'c'):
                    vals['dpT_' + x].append(float(pa[letters[x]] - pb[letters[x]]))
                    vals['draw_' + x].append(float(sa[letters[x]] - sb[letters[x]]))
                    vals['dlogit_exact_' + x].append(float(dp['exact'][letters[x]]))
                    vals['dlogit_layer1_' + x].append(float(dp['layer1'][letters[x]]))
                vals['cos_u_h'].append(float(np.dot(dirs_sel[r['unit']], h) / (np.linalg.norm(dirs_sel[r['unit']]) * np.linalg.norm(h))))
            per['%s|%s|%s' % (sc, r['arm'], r['unit'])] = {k2: {'mean': float(np.mean(v)), 'median': float(np.median(v)), 'q1': float(np.percentile(v, 25)), 'q3': float(np.percentile(v, 75))}
                                                         for k2, v in vals.items()}
        # 層一の M_L と正確な直接の経路の順位の一致（方向 × この層・符号は正で比べる）
        l1, ex = [], []
        for u in units:
            j = units.index(u)
            contr = []
            for k in ks:
                h = np.asarray(H_letter[k], dtype=np.float64)
                dp = C.direct_path(ZL[:, k], ZU[:, j], h, dirs_sel[u], coef, eps)
                contr.append(dp['exact'][letters['a']] - np.mean([dp['exact'][letters[x]] for x in lt if x != 'a']))
            l1.append(values_of(u, 'M_L_%s' % fam[sc]))
            ex.append(float(np.mean(contr)))
        letter['%s|%s' % key] = {'rows': per, 'rank_agreement_ML_exact': C.spearman(l1, ex), 'n_contexts': len(ks)}
    out['letter'] = letter
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--colab-dir', help='Colab の起動器の相 extract の出力の置き場（check.json と h.npz）')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    BL.require_sealed(TL)
    if os.path.exists(OUT) and not a.force:
        raise SystemExit('既にある: %s' % OUT)
    LJ = json.load(open(LENS, encoding='utf-8'))
    sel = BL.rkey(TL['primary']['ratio'])
    values_of = lambda u, m: LJ['layers'][sel]['directions'][u][m]['value']
    AN = json.load(open(os.path.join(REPO, *TL['calibration']['input'].split('/')), encoding='utf-8'))
    BD = AN['by_direction']
    counts = {}
    for r in BD:
        if (r['scenario'], r['arm']) not in counts:
            counts[(r['scenario'], r['arm'])] = row_choice_counts(r['scenario'], r['arm'])
    rows = gate_rows(TL, BD, counts)
    res = gate_part(TL, rows, values_of)
    res['s4_control'] = s4_control(values_of)
    res['tune'] = tune_part(TL, LJ['layers'])
    if a.colab_dir:
        CK = json.load(open(os.path.join(a.colab_dir, 'check.json'), encoding='utf-8'))
        FJ = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
        if CK['selected_sha16'] != FJ['facts']['E']['selected_sha16'] or CK.get('dry'):
            raise SystemExit('Colab の出力の選んだ試行が設計の事実と違うか、DRY の出力（止める）')
        Z = np.load(os.path.join(a.colab_dir, 'h.npz'))
        import steer_B
        D = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
        dirs_sel = collections.OrderedDict((u, D['%s__%s' % (u, sel)].astype(np.float64)) for u in UNITS_NAMED)
        for i, v in enumerate(steer_B.random_directions(D['static__%s' % sel], 'main', float(sel))):
            dirs_sel['rand:%d' % i] = np.asarray(v, dtype=np.float64)
        W = BL.Weights(BL.SNAP, TL['inputs']['model']['vocab_size'])
        Zfull = W.delta_full
        SJ = json.load(open(BL.SETS, encoding='utf-8'))
        letters = {k: int(v) for k, v in SJ['sets']['L'].items()}
        res['magnitude'] = magnitude_part(TL, rows, counts, CK['contexts'], Z['h_main'], Z['h_letter'], lambda H: Zfull(H), W.g, dirs_sel,
                                          int(SJ['sets']['F']['main']), letters, values_of, float(CK['rms_norm_eps']), (Z['logits_first_main'], Z['logits_first_letter']))
        res['magnitude']['colab_check'] = {'commit': CK['commit'], 'versions': CK['versions'], 'calibration': CK['calibration'], 'logit_check_colab': CK['logit_check']}
    res.update({'kind': 'blens_calib', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
                'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1, default=lambda o: o if not isinstance(o, (set, tuple)) else list(o))
    print('wrote', os.path.relpath(OUT, REPO))


def _selftest():
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    rng = np.random.default_rng(5)
    # 門: 合成の行（正本の行の数に合わせる）
    units = list(TL['calibration']['directions'])
    per_unit = {'static': 8, 'loaded': 1, 'Nk': 8, 'td': 8, 'rand:0': 13, 'rand:1': 13, 'rand:2': 13}
    fams = ['nuclear', 'survival']
    val = {u: {f: rng.normal() for f in fams} for u in units}
    rows = []
    for u in units:
        for i in range(per_unit[u]):
            f = fams[i % 2]
            s = 1 if i % 3 else -1
            rows.append({'scenario': 'S1' if f == 'survival' else 'N1', 'arm': 'X', 'base_arm': 'Y', 'unit': u, 'sign': s, 'fam': f, 'eligible': True,
                         'collapse': i == 0 and u == 'loaded', 'y': s * val[u][f] * 2 + rng.normal() * 0.1, 'k': 1, 'n': 2, 'k0': 1, 'n0': 2})
    values_of = lambda u, m: val[u][m.split('_')[-1]] if m.startswith(('M_L_', 'M_X_')) else 0.0
    res = gate_part(TL, rows, values_of)
    assert res['gates']['full']['M_L']['n_perm'] == 5040 and res['gates']['without_vhat']['M_L']['n_perm'] == 720
    assert res['gates']['without_vhat_loaded']['M_L']['n_perm'] == 120 and res['gate_passed'] and 'M_L' in res['link_vhat_metrics']
    # 門を通らない場合（行動が押しと無関係）
    for r in rows:
        r['y'] = rng.normal()
    res2 = gate_part(TL, rows, values_of)
    assert not res2['gates']['full']['M_L']['pass'] or res2['gates']['full']['M_L']['p'] < TL['calibration']['alpha']
    print('[blens_calib] 自己検査 OK（%s）' % VERSION)


if __name__ == '__main__':
    main()
