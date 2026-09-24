# -*- coding: utf-8 -*-
"""analyze_Bl3.py v1 —— B-lens 層三（Bl3）の集計の器（主の札・門・記述の門・q7・独立の再計算の一致・予想の答え・2026-09-25）。

入力: 本の計算の出力（升目と符号ごとの効き目・質量・層ごとの差分）・下見の記録（本の凍結で凍結したもの）・独立の再計算の二つの道の出力・段階 B の凍結した集計器の記録と試行の記録・
      設計事実（q7 の区間）・正本。重みは読まない。**読みは付けない**（読みの型の当てはめと文は組み立ての器 `tools/build_report_Bl3.py` が正本の読みの表から行う）。
計算（正本のとおり・芯の関数 `tools/bl3_core.py` を呼ぶ）:
  - 主の札: 行ごとの割合と裾の本数（等方の帰無・同じ升目と符号）・Holm（下見で外した升目の行を除いた数）・効き目の側・二つ目の札（中心・最上位・二つの順位）・等方の最上位の割合。
  - 門: 段階 B の方向ごとの行（土台の無操作の腕の破局が零でも全部でもない行）で、本の門・v̂ を抜いた門と、記述の門三つ（v̂ と (6b) を抜く・選択 a の件数・様式の転位の行を除く）。
  - q7（`predictions.q7_rule`）・予想の答え（q1〜q7・下見で止まったときと門が判定不能のとき）・独立の再計算の二段の一致（`independent_recompute.agreement`）。
  - 記述: 質量が `pilot.mass_min` を下回った方向の数（升目と符号ごと）・升目ごとの無操作の選択肢 a の文字の確率（裁定 D223）。
関数は合成データの器 `tools/dry_run_Bl3.py` が合成の出力で呼ぶ。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C
import bl3_core as K

VERSION = 'v1'
ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')
KIND = {'': 'static', 'rand': 'rand', 'Nk': 'Nk', 'td': 'td'}
key3 = lambda sc, base, sg: '%s|%s|%+d' % (sc, base, int(sg))


# ---------------- 段階 B の門の行 ----------------
def stage_b_gate_rows(T3, AN, trials_of):
    """門の行（正本 `gate.rows_rule`）と、行動の量（破局・選択 a の件数）と、様式の差（pt）。trials_of(場面, 腕) → 使えた試行の並び。"""
    BD = AN['by_direction']
    noop = {(r['scenario'], r['arm']): r for r in BD if r['direction_id'] == 'fixed' and '+v' not in r['arm'] and '-v' not in r['arm']}
    cc = T3['gate']['continuity']
    rows = []
    for r in BD:
        m = ARM_RE.match(r['arm'])
        if not m:
            continue
        b = noop[(r['scenario'], m.group(1))]
        if not (0 < b['cat'] < b['n_ok']):
            continue
        unit = r['direction_id'] if m.group(3) == 'rand' else KIND.get(m.group(3) or '', 'loaded')
        trs = [t for t in trials_of(r['scenario'], r['arm']) if t['direction_id'] == r['direction_id']]
        base_trs = trials_of(r['scenario'], m.group(1))
        n_a, n_a0 = sum(1 for t in trs if t['choice'] == 'a'), sum(1 for t in base_trs if t['choice'] == 'a')
        if len(trs) != r['n_ok'] or len(base_trs) != b['n_ok']:
            raise SystemExit('試行の記録と集計の記録の件数が違う（止める）: %s %s %s' % (r['scenario'], r['arm'], r['direction_id']))
        sg = 1 if m.group(2) == '+' else -1
        rows.append({'scenario': r['scenario'], 'arm': r['arm'], 'direction_id': r['direction_id'], 'base': m.group(1), 'sign': sg, 'unit': unit,
                     'cell': '%s|%s' % (r['scenario'], m.group(1)), 'fam': key3(r['scenario'], m.group(1), sg),
                     'y': K.behavior_y(r['cat'], r['n_ok'], b['cat'], b['n_ok'], cc), 'y_a': K.behavior_y(n_a, r['n_ok'], n_a0, b['n_ok'], cc),
                     'style_pt': 100.0 * (sum(1 for t in trs if t['style_b']) / len(trs) - sum(1 for t in base_trs if t['style_b']) / len(base_trs)),
                     'name': '%s|%s' % (r['scenario'], r['arm']) + ('〔%s〕' % r['direction_id'] if m.group(3) == 'rand' else '')})
    return rows


def trials_reader(repo=REPO):
    cache = {}

    def f(sc, arm):
        k = (sc, arm)
        if k not in cache:
            d = os.path.join(repo, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
            cache[k] = [t for t in (json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')) if t['status'] == 'ok']
        return cache[k]
    return f


# ---------------- 主の札 ----------------
def row_labels(T3, main_rows, eff, pair_names, dropped_cells=(), p_override=None):
    """主の行の札。eff: 升目と符号の鍵 → {方向の名: 効き目}。p_override: 行の名 → (効き目, 等方の帰無)（独立の再計算で v̂ の行を置き換えるとき）。"""
    swaps = T3['nulls']['real']['swap_siblings']
    alpha = T3['labels']['iso_outside']['holm_alpha']
    n_iso = T3['nulls']['isotropic']['count']
    out, pv = collections.OrderedDict(), {}
    rows = [r for r in main_rows if '%s|%s' % (r['scenario'], r['base']) not in set(dropped_cells)]
    for r in rows:
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        if p_override and r['id'] in p_override:
            e, iso = p_override[r['id']]['effect'], p_override[r['id']]['iso']
            same, opp = p_override[r['id']]['comps_same'], p_override[r['id']]['comps_opp']
        else:
            e = eff[k][r['direction']]
            iso = [eff[k]['iso:%d' % i] for i in range(n_iso)]
            comps = K.comparators_for(r['direction'], pair_names, swaps)
            same, opp = [eff[k]['real:' + p] for p in comps], [eff[kk]['real:' + p] for p in comps]
        pt = K.p_and_tail(e, iso)
        sl = K.second_label(e, list(same) + list(opp), list(zip(same, opp)))
        out[r['id']] = {'direction': r['direction'], 'cell_sign': k, 'effect': e, 'p': pt['p'], 'upper': pt['upper'], 'lower': pt['lower'], 'tail': pt['tail'],
                        'iso_median': float(np.median(iso)), 'second': sl, 'iso_top_share': K.iso_top_share(iso, sl['center'], list(same) + list(opp)), '_iso': iso}
        pv[r['id']] = pt['p']
    H = K.holm(pv, alpha)
    for rid, o in out.items():
        o['holm_step'], o['iso_outside'] = H[rid]['step'], bool(H[rid]['pass'])
        o['side'] = K.effect_side(o['effect'], o.pop('_iso')) if o['iso_outside'] else None
    return out, {'m_rows': len(rows), 'dropped_rows': [r['id'] for r in main_rows if r not in rows]}


def labels_signature(lab):
    """札の一致で見る中身（正本 `independent_recompute.agreement`）: Holm の判定・割合を決めた裾・等方の外の行の効き目の側・二つ目の札。"""
    return {rid: (o['iso_outside'], o['tail'], (o['side'] or {}).get('side'), (o['side'] or {}).get('sign'), o['second']['top']) for rid, o in lab.items()}


# ---------------- 門 ----------------
def gates(T3, rows, eff, dropped_cells=(), style_rows=()):
    units = ['static', 'loaded', 'Nk', 'td'] + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
    alpha = T3['gate']['alpha']
    ue = {u: {f: eff[f][u] for f in sorted({r['fam'] for r in rows})} for u in units}
    rs = lambda pred, yk='y': [{'unit': r['unit'], 'cell': r['cell'], 'fam': r['fam'], 'y': r[yk]} for r in rows if pred(r)]
    out = collections.OrderedDict()
    out['main'] = K.gate(rs(lambda r: True), ue, units, alpha, dropped_cells)
    out['without_vhat'] = K.gate(rs(lambda r: r['unit'] != 'static'), ue, [u for u in units if u != 'static'], alpha, dropped_cells)
    out['desc_without_vhat_loaded'] = K.gate(rs(lambda r: r['unit'] not in ('static', 'loaded')), ue, [u for u in units if u not in ('static', 'loaded')], alpha, dropped_cells)
    out['desc_choice_a'] = K.gate(rs(lambda r: True, 'y_a'), ue, units, alpha, dropped_cells)
    out['desc_without_style'] = K.gate(rs(lambda r: r['name'] not in set(style_rows)), ue, units, alpha, dropped_cells)
    return out


# ---------------- 予想の答え ----------------
def prediction_truth(T3, pilot_attempts, lab, G, q7_rows, floor):
    q1 = K.q1_from_attempts(pilot_attempts)
    stopped = (not q1['scored']) or q1['q1'] == '止める'
    items = {it['key']: it for it in T3['predictions']['items']}
    tr = collections.OrderedDict()
    tr['q1.pilot'] = q1['q1'] if q1['scored'] else None
    if stopped:
        for k in list(items)[1:]:
            tr[k] = None
        return tr, {'stopped': True, 'q1': q1}
    tr['q2.vhat_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'static' and o['iso_outside']), items['q2.vhat_iso']['options'])
    tr['q3.nk_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'Nk' and o['iso_outside']), items['q3.nk_iso']['options'])
    tr['q4.gate'] = None if G['main']['undetermined'] else ('通る' if G['main']['pass'] else '通らない')
    tr['q5.gate_wo_vhat'] = None if G['without_vhat']['undetermined'] else ('通る' if G['without_vhat']['pass'] else '通らない')
    tr['q6.second'] = K.bucket(sum(1 for o in lab.values() if o['second']['top']), items['q6.second']['options'])
    tr['q7.direction'] = K.score_q7(q7_rows, floor) if q7_rows else None
    return tr, {'stopped': False, 'q1': q1}


def q7_rows_of(lab, FJ):
    iv = {x['id']: x for x in FJ['facts']['C']['q7_intervals']}
    return [{'id': rid, 'effect': o['effect'], 'stage_b_diff': iv[rid]['diff_pt'], 'contains_zero': iv[rid]['contains_zero']}
            for rid, o in lab.items() if o['direction'] == 'static' and o['iso_outside']]


# ---------------- 独立の再計算の一致 ----------------
def recompute_agreement(T3, main_rows, eff_main, pair_names, hook, rewrite, pilot, dropped_cells=(), rows_subset=None):
    """二段の一致（正本 `independent_recompute.stages`・`agreement`）。hook と rewrite: 行の名 → {'noop_lo','effects': {'方向|符号': 効き目}}。
    本の計算では v̂ の行のすべてを比べる（行が欠ければ一致しない）。rows_subset は合成データの確かめで比べる行を絞るときだけ使う。"""
    comps_of = lambda d: K.comparators_for(d, pair_names, T3['nulls']['real']['swap_siblings'])
    n_iso = T3['nulls']['isotropic']['count']

    def override(path):
        ov = {}
        for r in main_rows:
            if r['direction'] != 'static' or r['id'] not in path or (rows_subset is not None and r['id'] not in rows_subset):
                continue
            E = path[r['id']]['effects']
            s = r['sign']
            ov[r['id']] = {'effect': E['static|%+d' % s], 'iso': [E['iso:%d|%+d' % (i, s)] for i in range(n_iso)],
                           'comps_same': [E['real:%s|%+d' % (p, s)] for p in comps_of('static')], 'comps_opp': [E['real:%s|%+d' % (p, -s)] for p in comps_of('static')]}
        return ov

    def as_eff(ov):
        return {rid: [o['effect']] + list(o['iso']) + list(o['comps_same']) + list(o['comps_opp']) for rid, o in ov.items()}
    main_ov = {}
    for r in main_rows:
        if r['direction'] != 'static' or (rows_subset is not None and r['id'] not in rows_subset):
            continue
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        main_ov[r['id']] = {'effect': eff_main[k]['static'], 'iso': [eff_main[k]['iso:%d' % i] for i in range(n_iso)],
                            'comps_same': [eff_main[k]['real:' + p] for p in comps_of('static')], 'comps_opp': [eff_main[kk]['real:' + p] for p in comps_of('static')]}
    sig = lambda ov: labels_signature(row_labels(T3, main_rows, eff_main, pair_names, dropped_cells, p_override=ov)[0])
    hk, rw = override(hook), override(rewrite) if rewrite is not None else None
    tol2 = K.cache_tol(pilot['floor'], T3['pilot']['cache_tol_factor'], T3['pilot']['cache_tol_floor'], T3['pilot']['noise_max']) + pilot['floor']
    out = {'second': K.agreement(as_eff(main_ov), as_eff(hk), tol2, sig(main_ov), sig(hk)), 'tol_second': tol2}
    out['first'] = K.agreement(as_eff(hk), as_eff(rw), T3['independent_recompute']['tol_stage1'], sig(hk), sig(rw)) if rw is not None else None
    out['tol_first'] = T3['independent_recompute']['tol_stage1']
    out['agree'] = bool(out['second']['agree'] and (out['first'] or {}).get('agree', False))
    return out


# ---------------- 乙（裁定 D227） ----------------
def secondary_rows(T3, rows_gate, FB):
    """乙の行（裁定 D227）: 門の行のうち、方向が名前のある方向か段階 B の三本で、土台の升目が B-lens の層二の層にある行。符号は門の行の符号。
    戻り値: 升目の鍵 → [(行の名〔場面|腕|単位〕, 方向の名, 符号)]（行の名は B-lens の層二の答えの文字の位置の行と同じ書き方）。"""
    strata_cells = {'%s|%s' % tuple(k.split('|')[:2]) for k in FB['facts']['E']['selected']}
    units = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
    out = collections.OrderedDict()
    for r in rows_gate:
        if r['cell'] in strata_cells and r['unit'] in units:
            out.setdefault(r['cell'], []).append(('%s|%s|%s' % (r['scenario'], r['arm'], r['unit']), r['unit'], r['sign']))
    return out


def secondary_counts(FB, rows_by_cell):
    """乙の順伝播の数（文脈ごとの行の数の和・文脈ごとの符号の数の和〔無操作と同じバッチに流す〕）。"""
    n_rows = n_batches = 0
    for key, ids_ in FB['facts']['E']['selected'].items():
        rows = rows_by_cell.get('%s|%s' % tuple(key.split('|')[:2]), [])
        n_rows += len(ids_) * len(rows)
        n_batches += len(ids_) * len({sg for _, _, sg in rows})
    return {'row_passes': n_rows, 'sign_batches': n_batches, 'contexts': sum(len(v) for v in FB['facts']['E']['selected'].values())}


def secondary_summary(sec_out, calib_letter=None):
    """乙のまとめ（記述・読みは付けない）: 行ごとに、文脈の間の平均・中央値・四分位と、B-lens の層二の直接の経路の値（あれば）を並べる。"""
    acc = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in sec_out:
        for name, v in c['rows'].items():
            for k, x in v.items():
                acc[name][k].append(x)
    out = collections.OrderedDict()
    for name, d in acc.items():
        s = {k: {'mean': float(np.mean(v)), 'median': float(np.median(v)), 'q1': float(np.percentile(v, 25)), 'q3': float(np.percentile(v, 75)), 'n': len(v)} for k, v in d.items()}
        if calib_letter is not None:
            sc = name.split('|')[0]
            arm = name.split('|')[1]
            base = re.split(r'[+\-]v', arm)[0]
            bl = ((calib_letter.get('%s|%s' % (sc, base)) or {}).get('rows') or {}).get(name)
            s['blens_direct'] = {k: bl[k] for k in ('dlogit_exact_a', 'dlogit_exact_c')} if bl else None
        out[name] = s
    return out


# ---------------- 記述 ----------------
def descriptive(T3, main_out):
    mm = T3['pilot']['mass_min']
    below = {k: sum(1 for d, v in o['mass'].items() if d != K.NOOP and v < mm) for k, o in main_out.items()}
    pa = {k: o['pa_noop'] for k, o in main_out.items()}
    return {'mass_below_min': below, 'pa_noop': pa}


def analyze(T3, FJ, main_out, pilot_attempts, pair_names, rows_gate, hook=None, rewrite=None, style_rows=(), rows_subset=None):
    """集計の全体（読みは付けない）。main_out: 升目と符号の鍵 → run_cell_sign の出力。pilot_attempts: 下見の試みの並び（最後が本の凍結の下見）。"""
    pilot = pilot_attempts[-1]
    dropped = (pilot.get('decision') or {}).get('dropped', [])
    eff = {k: o['effects'] for k, o in main_out.items()}
    lab, meta = row_labels(T3, T3['main_rows'], eff, pair_names, dropped)
    G = gates(T3, rows_gate, eff, dropped, style_rows)
    q7 = q7_rows_of(lab, FJ)
    truth, tmeta = prediction_truth(T3, pilot_attempts, lab, G, q7, pilot.get('floor', 0.0))
    out = collections.OrderedDict(version=VERSION, rows=lab, rows_meta=meta, gates=G, q7_rows=q7, predictions_truth=truth, predictions_meta=tmeta,
                                  descriptive=descriptive(T3, main_out), chance={'oriented': T3['nulls']['real']['chance_second'], 'pair': T3['nulls']['real']['chance_second_pair']})
    if hook is not None:
        out['recompute'] = recompute_agreement(T3, T3['main_rows'], eff, pair_names, hook, rewrite, pilot, dropped, rows_subset)
    return out


if __name__ == '__main__':
    print(__doc__)
