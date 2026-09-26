# -*- coding: utf-8 -*-
"""analyze_Bl3.py v4 —— B-lens 層三（Bl3）の集計の器（主の札・門・記述の門・q7・独立の再計算の一致・予想の答え・2026-09-25）。

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
import os, re, sys, json, glob, math, hashlib, subprocess, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C
import bl3_core as K

VERSION = 'v4'          # v4（2026-09-26・裁定 D239）: 組の SHA-256 を session と照らす・判定の錨を台帳の外と台帳の頭に・開く段で判定をやり直す・相 main が使った下見の記録と session のコミットの凍結の記録を照らす・門の行を転記行 C と照らす・照らす器を閉包から組む・台帳の差分をつなげて照らす・有限でない値を不一致として記す・DRY では書き出し先を求める／v3（2026-09-25・裁定 D236）: 一致だけを見る段が読んだ出力の同定を記録し開く段が照らす・開いた集計の一致の照らし・凍結の記録と手元の器の照らし・DRY の印と環境の食い違いで止める・下見の GPU・有限でない値で止める／v2（裁定 D231〜D234）
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
        n_cat_t = sum(1 for t in trs if t['catastrophe'])
        if n_cat_t != r['cat']:
            raise SystemExit('試行の記録の破局の件数と集計の記録の件数が違う（止める）: %s %s %s' % (r['scenario'], r['arm'], r['direction_id']))
        if len(trs) != r['n_ok'] or len(base_trs) != b['n_ok']:
            raise SystemExit('試行の記録と集計の記録の件数が違う（止める）: %s %s %s' % (r['scenario'], r['arm'], r['direction_id']))
        sg = 1 if m.group(2) == '+' else -1
        rows.append({'scenario': r['scenario'], 'arm': r['arm'], 'direction_id': r['direction_id'], 'base': m.group(1), 'sign': sg, 'unit': unit,
                     'cell': '%s|%s' % (r['scenario'], m.group(1)), 'fam': key3(r['scenario'], m.group(1), sg),
                     'y': K.behavior_y(r['cat'], r['n_ok'], b['cat'], b['n_ok'], cc), 'y_a': K.behavior_y(n_a, r['n_ok'], n_a0, b['n_ok'], cc),
                     'style_pt': 100.0 * (sum(1 for t in trs if t['style_b']) / len(trs) - sum(1 for t in base_trs if t['style_b']) / len(base_trs)),
                     'n_a': n_a, 'n_cat': n_cat_t,
                     'name': '%s|%s' % (r['scenario'], r['arm']) + ('〔%s〕' % r['direction_id'] if m.group(3) == 'rand' else '')})
    return rows


def gate_rows_vs_facts(rows_gate, FJ):
    """段階 B の記録から作り直した門の行を、設計事実の転記行 C（`tools/bl3_facts.py` が組んだ）と照らす（裁定 D239・器の直しの確かめ C1-新4）:
    行の鍵（場面・腕・方向・土台・符号・単位）・様式の転位の割合（転記行は小数一桁）・選択 a で破局でない件数。戻り値: 外れの並び（空なら同じ）。
    二つの器は同じ組み方の決まりを別々に書いたもので、両方が共有する読み違いは捕まえない（段階 B の試行の記録の変わりと、二つの組み方の食い違いを捕まえる）。"""
    fc = FJ['facts']['C']
    kf = lambda r: (r['scenario'], r['arm'], r['direction_id'], r['base'], int(r['sign']), r['unit'])
    bad = []
    if sorted(kf(r) for r in rows_gate) != sorted(kf(r) for r in fc['gate_rows']):
        bad.append('門の行の鍵が転記行 C と違う（%d 行 対 %d 行）' % (len(rows_gate), len(fc['gate_rows'])))
    for r in rows_gate:
        n = r['name']
        if n not in fc['style_share_pt'] or round(r['style_pt'], 1) != fc['style_share_pt'][n]:
            bad.append('様式の転位の割合が転記行 C と違う: %s' % n)
        if fc['gate_a_not_catastrophe'].get(n) != r['n_a'] - r['n_cat']:
            bad.append('選択 a で破局でない件数が転記行 C と違う: %s' % n)
    return bad


def trials_reader(repo=REPO):
    cache = {}

    def f(sc, arm):
        k = (sc, arm)
        if k not in cache:
            d = os.path.join(repo, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
            fs = glob.glob(os.path.join(d, 'trials-*.jsonl'))
            if len(fs) != 1:
                raise SystemExit('段階 B の試行の記録がちょうど一つでない（止める）: %s（%d）' % (d, len(fs)))
            cache[k] = [t for t in (json.loads(l) for l in open(fs[0], encoding='utf-8')) if t['status'] == 'ok']
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
        o['side'] = K.effect_side(o['effect'], o.pop('_iso'))      # 効き目の側は全ての行で作る（記述・`labels.print_rule`・裁定 D231）。読みの文で書くのは等方の外の行だけ（`labels.side_rule`）
    return out, {'m_rows': len(rows), 'dropped_rows': [r['id'] for r in main_rows if r not in rows]}


def labels_signature(lab):
    """札の一致で見る中身（正本 `independent_recompute.agreement`・裁定 D232）: Holm の判定・等方の外の行の割合を決めた裾・等方の外の行の効き目の側・二つ目の札。
    帰無の内側の行の裾と側は札に効かないので比べない（どちらかの道だけで等方の外なら、Holm の判定の欄が違うので一致しない）。"""
    return {rid: (o['iso_outside'], o['tail'] if o['iso_outside'] else None, (o['side'] or {}).get('side') if o['iso_outside'] else None,
                  (o['side'] or {}).get('sign') if o['iso_outside'] else None, o['second']['top']) for rid, o in lab.items()}


# ---------------- 門 ----------------
def gates(T3, rows, eff, dropped_cells=(), style_rows=()):
    units = ['static', 'loaded', 'Nk', 'td'] + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
    alpha = T3['gate']['alpha']
    rows = [r for r in rows if r['cell'] not in set(dropped_cells)]    # 下見で外した升目の行は、効き目を引く前に落とす（本の計算は外した升目の組を流さない・裁定 D231）
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
    本の計算では、下見で外した升目の行を除く v̂ の行のすべてを比べる（行が欠ければ一致しない）。rows_subset は合成データの確かめで比べる行を絞るときだけ使う。
    一段目は、無操作の値と全ての効き目の差が許容の内で、かつ札が同じとき一致（裁定 D233）。二段目は札が同じとき一致とし、効き目の差の最大と許容の内かどうかは記録する（裁定 D234）。"""
    drop = set(dropped_cells)
    in_drop = lambda r: '%s|%s' % (r['scenario'], r['base']) in drop
    comps_of = lambda d: K.comparators_for(d, pair_names, T3['nulls']['real']['swap_siblings'])
    nf = ['main:%s' % k for k, e in eff_main.items() if not all(math.isfinite(float(v)) for v in e.values())]
    for nm_, pth_ in (('hook', hook), ('rewrite', rewrite)):
        for rid_, o_ in (pth_ or {}).items():
            if not all(math.isfinite(float(v)) for v in [o_.get('noop_lo', 0.0)] + list((o_.get('effects') or {}).values())):
                nf.append('%s:%s' % (nm_, rid_))
    if nf:                                        # 有限でない値は札を組まずに不一致として記す（裁定 D239・器の直しの確かめ C2-7）
        s2 = {'agree': False, 'labels_same': False, 'values_within_tol': False, 'reason': 'non_finite', 'non_finite': nf[:10], 'rule': '札の一致（裁定 D234）'}
        f1 = None if rewrite is None else {'agree': False, 'reason': 'non_finite', 'non_finite': nf[:10], 'rule': '無操作の値と効き目の値と札（裁定 D233）'}
        return {'second': s2, 'tol_second': None, 'first': f1, 'tol_first': T3['independent_recompute']['tol_stage1'], 'agree': False, 'reason': 'non_finite', 'non_finite': nf[:10]}
    n_iso = T3['nulls']['isotropic']['count']

    def override(path):
        ov = {}
        for r in main_rows:
            if r['direction'] != 'static' or r['id'] not in path or in_drop(r) or (rows_subset is not None and r['id'] not in rows_subset):
                continue
            E = path[r['id']]['effects']
            s = r['sign']
            ov[r['id']] = {'effect': E['static|%+d' % s], 'iso': [E['iso:%d|%+d' % (i, s)] for i in range(n_iso)],
                           'comps_same': [E['real:%s|%+d' % (p, s)] for p in comps_of('static')], 'comps_opp': [E['real:%s|%+d' % (p, -s)] for p in comps_of('static')]}
        return ov

    def as_eff(ov):
        return {rid: [o['effect']] + list(o['iso']) + list(o['comps_same']) + list(o['comps_opp']) for rid, o in ov.items()}

    def with_noop(ov, path):
        return {rid: [path[rid]['noop_lo']] + v for rid, v in as_eff(ov).items()}      # 一段目は無操作の値も比べる（裁定 D233）
    main_ov = {}
    for r in main_rows:
        if r['direction'] != 'static' or in_drop(r) or (rows_subset is not None and r['id'] not in rows_subset):
            continue
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        main_ov[r['id']] = {'effect': eff_main[k]['static'], 'iso': [eff_main[k]['iso:%d' % i] for i in range(n_iso)],
                            'comps_same': [eff_main[k]['real:' + p] for p in comps_of('static')], 'comps_opp': [eff_main[kk]['real:' + p] for p in comps_of('static')]}
    sig = lambda ov: labels_signature(row_labels(T3, main_rows, eff_main, pair_names, dropped_cells, p_override=ov)[0])
    hk, rw = override(hook), override(rewrite) if rewrite is not None else None
    tol2 = K.cache_tol(pilot['floor'], T3['pilot']['cache_tol_factor'], T3['pilot']['cache_tol_floor'], T3['pilot']['noise_max']) + pilot['floor']
    s2 = K.agreement(as_eff(main_ov), as_eff(hk), tol2, sig(main_ov), sig(hk))
    s2 = dict(s2, agree=bool(s2['labels_same']), rule='札の一致（裁定 D234）', values_beyond_tol=not s2['values_within_tol'])
    out = {'second': s2, 'tol_second': tol2}
    if rw is not None:
        out['first'] = dict(K.agreement(with_noop(hk, hook), with_noop(rw, rewrite), T3['independent_recompute']['tol_stage1'], sig(hk), sig(rw)), rule='無操作の値と効き目の値と札（裁定 D233）')
    else:
        out['first'] = None
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
def chance_after_drop(T3, lab):
    """二つ目の札の偶然の目安を、下見で外した後の行で数え直す（正本 `pilot.decision.drop_effects`・生成器と同じ式・裁定 D231）。分母（方向ごとの行の数）も返す。"""
    co, cp = T3['nulls']['real']['comparators_oriented'], T3['nulls']['real']['comparators']
    by = collections.Counter(o['direction'] for o in lab.values())
    return {'oriented': round(sum(n / (co[d] + 1) for d, n in by.items()), 4), 'pair': round(sum(n / (cp[d] + 1) for d, n in by.items()), 4), 'rows_by_direction': dict(by),
            'canon_all_rows': {'oriented': T3['nulls']['real']['chance_second'], 'pair': T3['nulls']['real']['chance_second_pair']}}


def descriptive(T3, main_out):
    mm = T3['pilot']['mass_min']
    below = {k: sum(1 for d, v in o['mass'].items() if d != K.NOOP and v < mm) for k, o in main_out.items()}
    pa = {k: o['pa_noop'] for k, o in main_out.items()}
    return {'mass_below_min': below, 'pa_noop': pa}


def analyze(T3, FJ, main_out, pilot_attempts, pair_names, rows_gate, hook=None, rewrite=None, style_rows=(), rows_subset=None):
    """集計の全体（読みは付けない）。main_out: 升目と符号の鍵 → run_cell_sign の出力。pilot_attempts: 下見の試みの並び（最後が本の凍結の下見）。"""
    pilot = pilot_attempts[-1]
    dropped = (pilot.get('decision') or {}).get('dropped', [])
    nf = sorted({k for k, o in main_out.items() for d, v in list((o.get('effects') or {}).items()) + list((o.get('mass') or {}).items()) if not math.isfinite(float(v))})
    if nf:
        raise SystemExit('有限でない効き目か質量がある（止める・裁定 D236）: %s' % nf[:5])
    eff = {k: o['effects'] for k, o in main_out.items()}
    lab, meta = row_labels(T3, T3['main_rows'], eff, pair_names, dropped)
    G = gates(T3, rows_gate, eff, dropped, style_rows)
    q7 = q7_rows_of(lab, FJ)
    truth, tmeta = prediction_truth(T3, pilot_attempts, lab, G, q7, pilot.get('floor', 0.0))
    out = collections.OrderedDict(version=VERSION, rows=lab, rows_meta=meta, gates=G, q7_rows=q7, predictions_truth=truth, predictions_meta=tmeta,
                                  descriptive=descriptive(T3, main_out), chance=chance_after_drop(T3, lab))
    if hook is not None:
        out['recompute'] = recompute_agreement(T3, T3['main_rows'], eff, pair_names, hook, rewrite, pilot, dropped, rows_subset)
    return out


# ---------------- 段階 B のその行の注（報告の雛形） ----------------
def stage_b_notes(T3, AN, rows_gate):
    """段階 B のその行の注（正本 `report_rules.template`「主の表と門の行に、段階 B のその行の注（判定保留・ランダム方向の不均一）を写す」）。
    主の行: 段階 B の確かめの行（凍結した集計器の記録の `confirm`・同じ名）の札と注と様式の保留。門の行: 名前のある方向の行は、その腕を比べの加えた腕に持つ確かめの行の札が
    判定保留のときその札。ランダム方向の行は、その腕の不均一の記録（`homogeneity`）に注があるときその注。"""
    conf = {r['id']: r for r in AN['confirm']}
    conf_by_arm = {(r['scenario'], r['A']): r for r in AN['confirm']}
    homo = {(h['scenario'], h['arm']): h for h in AN['homogeneity']}
    main = collections.OrderedDict()
    for r in T3['main_rows']:
        c = conf.get(r['id'])
        main[r['id']] = {'label': c['label'] if c else None, 'notes': list(c.get('notes') or []) if c else [], 'style_hold': bool(c and c.get('style_hold'))}
    gate = collections.OrderedDict()
    for g in rows_gate:
        notes = []
        if g['unit'].startswith('rand:'):
            h = homo.get((g['scenario'], g['arm']))
            if h and h.get('note'):
                notes.append({'kind': 'ランダム方向の不均一', 'spread_pt': h['spread_pt'], 'threshold_pt': h['threshold_pt']})
        else:
            c = conf_by_arm.get((g['scenario'], g['arm']))
            if c and str(c.get('label', '')).startswith('判定保留'):
                notes.append({'kind': c['label']})
        gate[g['name']] = notes
    return {'main': main, 'gate': gate}


# ---------------- 手元の二つの段（一致だけを見る・結果を開く・正本 `independent_recompute.print`・`on_mismatch`） ----------------
PARTS = ('main', 'recompute', 'secondary')
JUDGE = os.path.join(REPO, 'records', 'Bl3', 'judge-Bl3.json')
OPENED = os.path.join(REPO, 'records', 'Bl3', 'analysis-Bl3.json')
FR_PATH = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
SEAL_PATH = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
# 二つの段と報告の頭で、本の凍結の記録の SHA16 と照らすもの（裁定 D236・D239）: 正本・設計事実・方向の記録と、結果を開く段が読む凍結物と、
# 集計・報告・掃き出し・報告の走査の器の import の閉包（手書きの一覧にしない・器の直しの確かめ C1-新4）
FROZEN_CHECK_BASE = ('design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json',
                     'records/B/analysis-B-2026-09-22.json', 'records/Blens/design-facts-Blens.json', 'results/Blens/calib-Blens.json')
FROZEN_CHECK_TOOLS = ('tools/analyze_Bl3.py', 'tools/build_report_Bl3.py', 'tools/sweep_Bl3.py', 'tools/report_lint.py')
STRICT_ENV = ('commit', 'dry', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef')      # 組の間で違えば止める（GPU と版の違いは記す・裁定 D236）


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
canon_sha16 = lambda obj: hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest().upper()[:16]
fr_core = lambda FR: {k: v for k, v in FR.items() if k != 'deviations'}          # 凍結の記録のうち台帳の外（台帳は後ろに足すだけ）


def frozen_check_files():
    """照らすファイルの並び（FROZEN_CHECK_BASE と、FROZEN_CHECK_TOOLS の import の閉包・凍結の器の `import_closure`）。"""
    import freeze_Bl3 as FZ
    return list(FROZEN_CHECK_BASE) + [f for f in FZ.import_closure(list(FROZEN_CHECK_TOOLS)) if f not in FROZEN_CHECK_BASE]


def git_show_json(commit, path, repo=REPO):
    """コミットの中のファイルを JSON で読む（読めなければ None）。"""
    r = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (commit, path)], capture_output=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout.decode('utf-8'))
    except Exception:
        return None


def load_outputs(dirs):
    """起動器の相 main の出力（組ごとの JSON と、その置き場の session.json）を、一つ以上の置き場から読む。同じ組が二つあれば止める。
    戻り値: 組 → 出力・組 → session・組 → 読んだファイルの同定（置き場の名・組の JSON と session.json の SHA-256・裁定 D236）。"""
    parts, sessions, files = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
    for d in dirs:
        sp = os.path.join(d, 'session.json')
        S = json.load(open(sp, encoding='utf-8'))
        for part in PARTS:
            p = os.path.join(d, '%s.json' % part)
            if os.path.exists(p):
                if part in parts:
                    raise SystemExit('同じ組が二つの置き場にある（止める）: %s' % part)
                got = sha256f(p)
                want = (S.get('part_sha256') or {}).get(part)
                if want != got:                          # 起動器が書いた組の出力の同定と照らす（Colab から手元までの間の変わり・裁定 D239）
                    raise SystemExit('組 %s の出力の SHA-256 が、起動器が session に書いた値と違う（止める）: 今 %s…・session %s…' % (part, got[:16], (want or 'なし')[:16]))
                parts[part] = json.load(open(p, encoding='utf-8'))
                sessions[part] = S
                files[part] = {'dir': os.path.basename(os.path.normpath(d)), 'json_sha256': got, 'session_sha256': sha256f(sp)}
    return parts, sessions, files


def env_same(sessions, pilot_sessions=None):
    """組の間で、コミット・GPU・版・正本・方向の npz・DRY が同じか（違えば記す）。pilot_sessions（本の凍結の下見の session）を与えると、下見の GPU も並べる（裁定 D236）。"""
    keys = ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef')
    ref = next(iter(sessions.values())) if sessions else {}
    diff = {k: {p: s.get(k) for p, s in sessions.items()} for k in keys if any(s.get(k) != ref.get(k) for s in sessions.values())}
    out = {'same': not diff, 'diff': diff, 'strict': [k for k in diff if k in STRICT_ENV]}
    if pilot_sessions is not None:
        pg = sorted({str(s.get('gpu')) for s in pilot_sessions})
        out['pilot_gpu'] = pg
        out['gpu_same_as_pilot'] = sorted({str(s.get('gpu')) for s in sessions.values()}) == pg
    return out


def with_iso(T3, n_iso):
    """独立の再計算の等方の本数に合わせた正本の写し（本の計算では正本と同じ本数・DRY で減らしたときだけ違う）。"""
    if n_iso == T3['nulls']['isotropic']['count']:
        return T3
    T3x = json.loads(json.dumps(T3))
    T3x['nulls']['isotropic']['count'] = n_iso
    return T3x


def frozen_versions_bad(FR, repo=REPO, files=None):
    """手元の器と正本・設計事実・方向の記録と読む凍結物を、本の凍結の記録の SHA16 と照らす（裁定 D236・D239）。本の凍結の後に台帳に記した器の差分は、
    路ごとに前後をつなげて許す（芯の `ledger_chain_bad`・本の凍結の記録の `deviations_n` より後の台帳の行）。戻り値: 外れの並び。"""
    mf = FR.get('main_freeze') or {}
    files = list(files or frozen_check_files())
    now = {f: (sha16f(os.path.join(repo, *f.split('/'))) if os.path.exists(os.path.join(repo, *f.split('/'))) else None) for f in files}
    return K.ledger_chain_bad(mf.get('frozen_sha16') or {}, now, (FR.get('deviations') or [])[int(mf.get('deviations_n') or 0):], paths=files)


def judge(T3, parts, sessions, pilot_attempts, pair_names, files=None, FR=None):
    """一致だけを見る段: 器の誤りの有無・組の環境・二段の一致か不一致かだけを返す（効き目の値と差の最大は返さない）。
    DRY の印が組の間で違うとき・組の間のコミットと正本と npz と層と係数が違うとき・DRY でないのに等方の本数が正本と違うとき・DRY でないのに
    手元の器と正本が本の凍結の記録と違うときは、一致と答えない（裁定 D236）。読んだ出力の同定（files）と凍結の記録の SHA16 を記録に置く。"""
    out = collections.OrderedDict(parts=list(parts), tool_error={p: bool(v.get('tool_error')) for p, v in parts.items()}, env=env_same(sessions))
    drys = {p: bool(s.get('dry')) for p, s in sessions.items()}
    dry = any(drys.values())
    out['dry'] = dry
    out['inputs'] = files
    if FR is not None:                      # 凍結の記録の錨: 台帳の外と、台帳の行の数と並び（台帳は後ろに足すだけ・判定と開く段の間の記帳で止めない・裁定 D239）
        devs_ = FR.get('deviations') or []
        out['freeze_record_core_sha16'] = canon_sha16(fr_core(FR))
        out['deviations_n'] = len(devs_)
        out['deviations_sha16'] = canon_sha16(devs_)
    if os.path.exists(SEAL_PATH):
        out['sealing_record_sha16'] = sha16f(SEAL_PATH)
    stop = lambda why: (out.update(first=None, second=None, agree=None, reason=why), out)[1]
    if any(out['tool_error'].values()) or not {'main', 'recompute'} <= set(parts):
        return stop('器の誤りか、組 main・recompute の欠け')
    if len(set(drys.values())) > 1:
        return stop('組の間で DRY の印が違う: %s' % drys)
    if out['env']['strict']:
        return stop('組の間の環境が違う: %s' % out['env']['strict'])
    rc = parts['recompute']
    n_can = T3['nulls']['isotropic']['count']
    if not dry:
        main_keys = {key3(sc, b, sg) for sc, b, sg in T3['cell_signs_main']}
        n_main = {k: sum(1 for d in o['effects'] if d.startswith('iso:')) for k, o in parts['main']['cells'].items() if k in main_keys}
        if rc['n_iso'] != n_can or any(v != n_can for v in n_main.values()):
            return stop('DRY でないのに等方の本数が正本と違う（組 recompute %s・本の計算の升目と符号 %s）' % (rc['n_iso'], sorted(set(n_main.values()))))
        if FR is None:
            return stop('DRY でないのに凍結の記録が無い')
        bad = frozen_versions_bad(FR)
        if bad:
            return stop('手元の器か正本が本の凍結の記録と違う: %s' % bad)
        # 手元の本の凍結の下見の記録を、相 main が使った下見の記録・組 main の出力・session のコミットの凍結の記録と照らす（裁定 D239・器の直しの確かめ C1-新3・C2-12）
        mf = FR.get('main_freeze') or {}
        pil = mf.get('pilot') or {}
        want_pu = {'batch': pil.get('batch'), 'floor': pil.get('floor'), 'cache_tol': pil.get('cache_tol'), 'dropped': sorted((pil.get('decision') or {}).get('dropped', []))}
        for p_, s_ in sessions.items():
            pu = s_.get('pilot_used') or {}
            got_pu = {'batch': pu.get('batch'), 'floor': pu.get('floor'), 'cache_tol': pu.get('cache_tol'), 'dropped': sorted(pu.get('dropped') or [])}
            if got_pu != want_pu:
                return stop('組 %s の相 main が使った下見の記録が、手元の本の凍結の下見の記録と違う: %s 対 %s' % (p_, got_pu, want_pu))
            if s_.get('canon_sha16') != (mf.get('frozen_sha16') or {}).get('design/contrasts-Bl3.json') or s_.get('directions_npz_sha256') != FR.get('directions_npz_sha256'):
                return stop('組 %s の session の正本か方向の npz が、凍結の記録と違う' % p_)
        if parts['main'].get('batch') != pil.get('batch') or sorted(parts['main'].get('dropped') or []) != want_pu['dropped']:
            return stop('組 main の出力のバッチか外した升目が、本の凍結の下見の記録と違う')
        for c_ in sorted({str(s_.get('commit')) for s_ in sessions.values()}):
            FRc = git_show_json(c_, 'records/Bl3/FREEZE-RECORD-Bl3.json')
            if FRc is None or FRc.get('main_freeze') != mf:
                return stop('相 main のコミット %s の凍結の記録の本の凍結が、手元の本の凍結と違う（または読めない）' % c_[:12])
    pilot = pilot_attempts[-1]
    eff = {k: o['effects'] for k, o in parts['main']['cells'].items()}
    ag = recompute_agreement(with_iso(T3, rc['n_iso']), T3['main_rows'], eff, pair_names, rc['hook'], rc.get('rewrite'), pilot,
                             (pilot.get('decision') or {}).get('dropped', []), rows_subset=set(rc['hook']) if dry else None)
    out.update(first=None if ag['first'] is None else bool(ag['first']['agree']), second=bool(ag['second']['agree']), agree=bool(ag['agree']),
               second_values_within_tol=bool(ag['second']['values_within_tol']),       # 値だけが許容の外で札が同じときは止めずに台帳に記す（裁定 D234）
               reason=None if ag['agree'] else (('有限でない値（%s）' % '・'.join(ag.get('non_finite') or [])) if ag.get('reason') == 'non_finite' else
                                                  ('一段目の道が無い' if ag['first'] is None else '二段のどちらかが一致しない')))
    return out


def open_results(T3, FJ, parts, sessions, pilot_attempts, pair_names, AN, calib_letter, FB, repo=REPO, pilot_sessions=None):
    """結果を開く段（登録者と一緒に・一致だけを見る段が一致したとき）: 集計の全体と、報告に並べるもの（下見の記録・頭の確かめ・層ごとの差分・乙・段階 B の注・環境）。"""
    rc = parts['recompute']
    dry = any(s.get('dry') for s in sessions.values())
    T3x = with_iso(T3, rc['n_iso'])
    rows_gate = stage_b_gate_rows(T3, AN, trials_reader(repo))
    bad_g = gate_rows_vs_facts(rows_gate, FJ)
    if bad_g:
        raise SystemExit('段階 B の記録から作り直した門の行が、設計事実の転記行 C と違う（開かない・裁定 D239）: %s' % bad_g[:5])
    style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
    A = analyze(T3x, FJ, parts['main']['cells'], pilot_attempts, pair_names, rows_gate, hook=rc['hook'], rewrite=rc.get('rewrite'), style_rows=style_rows,
                rows_subset=set(rc['hook']) if dry else None)
    main_keys = {key3(sc, b, sg) for sc, b, sg in T3['cell_signs_main']}
    A['dry'] = dry
    A['n_iso'] = rc['n_iso']
    A['pilot_attempts'] = pilot_attempts
    A['head'] = parts['main']['head']
    A['main_run'] = {k: parts['main'].get(k) for k in ('batch', 'shortcut', 'dropped')}
    A['layerwise'] = {k: o['layers'] for k, o in parts['main']['cells'].items() if k in main_keys}
    A['gate_rows'] = [{k: r[k] for k in ('name', 'scenario', 'arm', 'unit', 'sign', 'cell', 'fam', 'y', 'y_a', 'style_pt')} for r in rows_gate]
    A['style_rows'] = style_rows
    A['stage_b_notes'] = stage_b_notes(T3, AN, rows_gate)
    if 'secondary' in parts:
        S2 = parts['secondary']
        A['secondary'] = {'counts': S2.get('counts'), 'contexts_run': len(S2.get('contexts') or []), 'summary': secondary_summary(S2.get('contexts') or [], calib_letter)}
    A['sessions'] = {p: {k: s.get(k) for k in ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef', 'finished')} for p, s in sessions.items()}
    A['env'] = env_same(sessions, pilot_sessions)
    A['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
    return A


def open_checked(T3, FJ, parts, sessions, files, J, pilot_attempts, pair_names, AN, calib_letter, FB, FR=None, judge_sha16=None, repo=REPO):
    """結果を開く段の確かめ（裁定 D236・D239）: 一致だけを見る段の記録が一致で、読む出力の同定（置き場の名・組の JSON と session の SHA-256）が同じで、DRY でないときは
    凍結の記録の台帳の外が判定の時と同じで、判定の時の台帳の行が今の台帳の頭と同じ（台帳は後ろに足すだけ・判定と開く段の間の記帳で止めない）。同じ入力で一致だけを見る段を
    もう一度走らせ、書いた時刻と柵と台帳の数の外のすべての欄が判定の記録と同じこと（判定の記録を書き換えても開けない）。開いた集計の二段の一致が判定と違えば止める（書かない）。"""
    if not J.get('agree'):
        raise SystemExit('一致だけを見る段の記録が一致していない（結果を開かない）')
    if J.get('inputs') != files:
        ji, fi = J.get('inputs') or {}, files or {}
        raise SystemExit('結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）: %s' % [p for p in sorted(set(ji) | set(fi)) if ji.get(p) != fi.get(p)])
    dry = any(s.get('dry') for s in sessions.values())
    if not dry:
        if FR is None:
            raise SystemExit('DRY でないのに凍結の記録が無い（開かない）')
        devs_ = FR.get('deviations') or []
        n_ = J.get('deviations_n')
        if canon_sha16(fr_core(FR)) != J.get('freeze_record_core_sha16'):
            raise SystemExit('凍結の記録（台帳の外）が一致だけを見る段の後に変わった（開かない）')
        if n_ is None or len(devs_) < n_ or canon_sha16(devs_[:n_]) != J.get('deviations_sha16'):
            raise SystemExit('凍結の記録の台帳の、一致だけを見る段の時の行が変わった（開かない・台帳は後ろに足すだけ）')
        bad = frozen_versions_bad(FR, repo)
        if bad:
            raise SystemExit('手元の器か正本が本の凍結の記録と違う（開かない）: %s' % bad)
    J2 = json.loads(json.dumps(judge(T3, parts, sessions, pilot_attempts, pair_names, files, FR), ensure_ascii=False, default=float))
    skip_ = ('written_utc', 'clause', 'deviations_n', 'deviations_sha16')
    diff_ = sorted(k for k in set(J) | set(J2) if k not in skip_ and J.get(k) != J2.get(k))
    if diff_:
        raise SystemExit('一致だけを見る段を同じ入力でもう一度走らせた答えが、判定の記録と違う（開かない）: %s（もう一度の理由 %s）' % (diff_, J2.get('reason')))
    pilot_sessions = ((FR or {}).get('main_freeze') or {}).get('sessions')
    A = open_results(T3, FJ, parts, sessions, pilot_attempts, pair_names, AN, calib_letter, FB, repo=repo, pilot_sessions=pilot_sessions)
    rc = A.get('recompute') or {}
    got = (None if rc.get('first') is None else bool(rc['first']['agree']), bool((rc.get('second') or {}).get('agree')), bool(rc.get('agree')))
    if got != (J.get('first'), J.get('second'), J.get('agree')):
        raise SystemExit('開いた集計の二段の一致が、一致だけを見る段と違う（書かない）: %s 対 %s' % (got, (J.get('first'), J.get('second'), J.get('agree'))))
    A['inputs'] = files
    A['judge_record_sha16'] = judge_sha16
    return A


def _freeze_record():
    return json.load(open(FR_PATH, encoding='utf-8')) if os.path.exists(FR_PATH) else None


def _pilot_attempts(args_pilot, FR=None):
    """下見の試みの並び: 本の計算では凍結の記録の本の凍結（`main_freeze.pilot_attempts`）から。DRY の出力を試すときだけ、相 pilot の出力の pilot.json を与える。"""
    if args_pilot:
        return [json.load(open(p, encoding='utf-8'))['pilot'] for p in args_pilot]
    if FR is None:
        raise SystemExit('凍結の記録が無い（本の計算では本の凍結の下見の記録を読む）')
    atts = FR['main_freeze']['pilot_attempts']
    if FR['main_freeze']['pilot'] != atts[-1]:
        raise SystemExit('本の凍結の下見の記録と、下見の試みの最後が違う（止める）')
    return atts


def main():
    import argparse, datetime
    ap = argparse.ArgumentParser(description='B-lens 層三の手元の二つの段（judge: 一致だけを見る／open: 結果を開く）')
    ap.add_argument('step', choices=['judge', 'open'])
    ap.add_argument('dirs', nargs='+', help='起動器の相 main の出力の置き場（組ごとの JSON と session.json）')
    ap.add_argument('--pilot', nargs='*', help='DRY の出力を試すときだけ: 相 pilot の出力の pilot.json（試みの順）')
    ap.add_argument('--out', help='出力の置き場（既定は records/Bl3/judge-Bl3.json・analysis-Bl3.json）')
    ap.add_argument('--judge-record', help='結果を開く段が読む、一致だけを見る段の記録（既定は records/Bl3/judge-Bl3.json）')
    a = ap.parse_args()
    T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
    FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
    DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
    parts, sessions, files = load_outputs(a.dirs)
    dry = any(s.get('dry') for s in sessions.values())
    if dry and not a.out:
        raise SystemExit('DRY の出力には --out を与える（本の置き場 records/Bl3/ に書かない・裁定 D239）')
    if dry and a.step == 'open' and not a.judge_record:
        raise SystemExit('DRY の出力を開くときは --judge-record を与える（裁定 D239）')
    if a.pilot and not dry:
        raise SystemExit('--pilot は DRY の出力を試すときだけ（本の計算では凍結の記録の本の凍結を読む）')
    FR = None if dry else _freeze_record()
    attempts = _pilot_attempts(a.pilot, FR)
    pair_names = list(DJ['groups']['real']['names'])
    if a.step == 'judge':
        out = a.out or JUDGE
        if os.path.exists(out):
            raise SystemExit('既にある（一致だけを見る段は一度だけ）: %s' % out)
        J = judge(T3, parts, sessions, attempts, pair_names, files, FR)
        J['written_utc'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        J['clause'] = '本記録は一致か不一致かだけを持つ（値は開かない・正本 independent_recompute.print）。'
        json.dump(J, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
        say = lambda b: '無い' if b is None else ('一致' if b else '不一致')
        print('[analyze_Bl3] 一致だけを見る段: 器の誤り %s・組の環境 %s・一段目 %s・二段目（札） %s・二段目の値 %s・全体 %s（値は開いていない）%s' % (
            'あり' if any(J['tool_error'].values()) else '無し', '同じ' if J['env']['same'] else '違う', say(J['first']), say(J['second']),
            '無い' if J.get('second_values_within_tol') is None else ('許容の内' if J['second_values_within_tol'] else '許容の外（止めずに台帳に記す・裁定 D234）'), say(J['agree']),
            ('・理由 %s' % J['reason']) if J.get('reason') else ''))
        if not J['agree']:
            raise SystemExit('一致しない（結果を開く前に止め、逸脱の台帳に記して登録者に上げる・裁定 D219）')
        return
    jp = a.judge_record or JUDGE
    if not os.path.exists(jp):
        raise SystemExit('一致だけを見る段の記録が無い（結果を開かない）: %s' % jp)
    J = json.load(open(jp, encoding='utf-8'))
    out = a.out or OPENED
    if os.path.exists(out):
        raise SystemExit('既にある: %s' % out)
    AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
    CB = json.load(open(os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json'), encoding='utf-8'))['magnitude']['letter']
    FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
    A = open_checked(T3, FJ, parts, sessions, files, J, attempts, pair_names, AN, CB, FB, FR=FR, judge_sha16=sha16f(jp))
    json.dump(A, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else float(o))
    print('[analyze_Bl3] 結果を開いた: %s' % os.path.relpath(out, REPO))


if __name__ == '__main__':
    main()
