# -*- coding: utf-8 -*-
"""analyze_Bprime.py v0.4（2026-09-30・B′ の集計の器・層三の `tools/analyze_Bl3.py` v4 を B′ の正本に移したもの・コーディネータ南無弥勒如来）。

入力: 本の計算の出力（升目と符号ごとの効き目・質量・層ごとの差分）・下見の記録（本の凍結で凍結したもの）・独立の再計算の二つの道の出力と独立の再抽出の出力・
      道の違いの記述の出力（本の計算がバッチ一に移ったときだけ）・抽出の記録・行動の下見の閉じた記録・正本。重みは読まない。**読みは付けない**
      （読みの型の当てはめと文は報告の組み立ての器が正本の読みの表から行う）。
計算（正本のとおり・層三の凍結の芯 `bl3_core` と B-lens の凍結の芯 `blens_core` を呼ぶ）:
  - 主の札: 行ごとの割合と裾の本数（等方の帰無・同じ升目と符号）・Holm（下見で外した升目の行を除いた数）・効き目の側・二つ目の札（中心・最上位・二つの順位）・等方の最上位の割合。
  - 予想の答え（q1〜q4・q5〜q7 は欠番）・偶然の目安の数え直し・独立の再計算の二段の一致（二段目の許容は正本 `independent_recompute.stages.second` の鍵）・独立の再抽出の一致。
  - 記述: 質量が `pilot.mass_min` を下回った方向の数と割合（名前のある方向・等方・実在の差に分けて）・升目ごとの無操作の選択肢 a の文字の確率・等方の張り付きの量・
    等方の効き目の広がり（四分位の幅・95% の中央の区間の幅・標準偏差・中央値）と、実在の差の方向の四分位の幅で割った値・道の違いの記述（札の違う行の数と効き目の差の最大）。
層三の門・乙・q5〜q7 は B′ に無い（正本 `gate.status`・`predictions.missing`）。手元の二つの段（一致だけを見る／結果を開く）は層三の型（凍結と封印の記録の錨・組の SHA・環境）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, math, hashlib, subprocess, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G          # 凍結の器の置き場を sys.path に足す
import bl3_core as K
import bprime_core as P

VERSION = 'v0.4'        # v0.4（2026-09-30・器の実装の検分の後）: 組の間で違えば止める鍵を中身にした（DRY の印・正本・器の閉包・本の凍結の節・方向の npz の SHA。コミットは組ごとに記述・U08）・DRY でない一致だけを見る段に層三の照らしを戻した（本の凍結の節の SHA16・組ごとの正本と npz の SHA が本の凍結の値・本の計算のバッチと外した升目・手元の凍結物の台帳のつながり・U08・U10）・下見の前の凍結から動かせない器の錠（U03）・二段の一致で比べる行と二つの道の鍵の集合を照らす（U44・G-03）・走行の表を集計の出力に置く（U04）・器の誤りで閉じた行動の下見とやり直しの前の閉じた記録を受ける（U07・U09）・床の余白の印を升目の二つの組のどちらかで付ける（保守側・二つの値を置く・U17）・下見が止めたときの集計の出力を書く段 stopped を足す（前は止めたときの報告を組む入口が無かった・K26）。前の版は `prev/analyze_Bprime-v0.3.py`／v0.3（2026-09-30）: 手元の二つの段の口で、DRY の出力だけ等方の本数を抽出の記録の名の数に合わせた正本の写しで集計する（起動器の DRY の写しは等方の本数を減らすので、正本の本数では鍵が足りずに止まった・Colab の合成データの確かめで見つけた・K21）。前の版は `prev/analyze_Bprime-v0.2.py`／v0.2（2026-09-30）: 手元の二つの段の口（judge・open）を足した・抽出の記録の組の名から方向の名を作る／v0.1: 結果を開く段の出力に独立の再抽出の一致（`reextract`）を足した（報告の組み立ての器が読むのに書いていなかった・掃き出しの器を書いて見つけた）。前の版は `prev/analyze_Bprime-v0.py`
key3 = lambda sc, base, sg: '%s|%s|%+d' % (sc, base, int(sg))
RECS = os.path.join(ROOT, 'records', 'Bprime')
PARTS_MAIN = ('main', 'pathdiff')
PARTS_RC = ('hook', 'rewrite', 'reextract')
STRICT_ENV = ('dry', 'canon_sha16', 'tools_sha16', 'main_freeze_sha16', 'directions_npz_sha256')     # 組の間で違えば止める（中身・v0.4・U08）。コミット・GPU・版は記述
ENV_KEYS = ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism', 'tools_sha16', 'main_freeze_sha16', 'directions_npz_sha256')
CANON_PATH = 'design/contrasts-Bprime.json'
NEED_STAGES = ('extract', 'behavior', 'pilot', 'main', 'recompute')


# ---------------- 主の札 ----------------
def row_labels(C, main_rows, eff, pair_names, dropped_cells=(), p_override=None):
    """主の行の札（層三の `analyze_Bl3.row_labels` と同じ決まり）。eff: 升目と符号の鍵 → {方向の名: 効き目}。p_override: 行の名 → 効き目の組（独立の再計算で置き換えるとき）。"""
    swaps = C['nulls']['real']['swap_siblings']
    alpha = C['labels']['iso_outside']['holm_alpha']
    n_iso = C['nulls']['isotropic']['count']
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
        o['side'] = K.effect_side(o['effect'], o.pop('_iso'))
    return out, {'m_rows': len(rows), 'dropped_rows': [r['id'] for r in main_rows if r not in rows]}


def labels_signature(lab):
    """札の一致で見る中身（正本 `independent_recompute.agreement`）: Holm の判定・等方の外の行の割合を決めた裾・等方の外の行の効き目の側・二つ目の札。"""
    return {rid: (o['iso_outside'], o['tail'] if o['iso_outside'] else None, (o['side'] or {}).get('side') if o['iso_outside'] else None,
                  (o['side'] or {}).get('sign') if o['iso_outside'] else None, o['second']['top']) for rid, o in lab.items()}


# ---------------- 予想の答え ----------------
def prediction_truth(C, pilot_attempts, lab):
    q1 = K.q1_from_attempts(pilot_attempts)
    stopped = (not q1['scored']) or q1['q1'] == '止める'
    items = {it['key']: it for it in C['predictions']['items']}
    tr = collections.OrderedDict()
    tr['q1.pilot'] = q1['q1'] if q1['scored'] else None
    if stopped:
        for k in list(items)[1:]:
            tr[k] = None
        return tr, {'stopped': True, 'q1': q1}
    tr['q2.vhat_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'static' and o['iso_outside']), items['q2.vhat_iso']['options'])
    tr['q3.nk_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'Nk' and o['iso_outside']), items['q3.nk_iso']['options'])
    tr['q4.second'] = K.bucket(sum(1 for o in lab.values() if o['second']['top']), items['q4.second']['options'])
    return tr, {'stopped': False, 'q1': q1}


def chance_after_drop(C, lab):
    """二つ目の札の偶然の目安を、下見で外した後の行で数え直す（正本 `pilot.decision_more.drop_effects`）。分母（方向ごとの行の数）も返す。"""
    co, cp = C['nulls']['real']['comparators_oriented'], C['nulls']['real']['comparators']
    by = collections.Counter(o['direction'] for o in lab.values())
    return {'oriented': round(sum(n / (co[d] + 1) for d, n in by.items()), 4), 'pair': round(sum(n / (cp[d] + 1) for d, n in by.items()), 4), 'rows_by_direction': dict(by),
            'canon_all_rows': {'oriented': C['nulls']['real']['chance_second'], 'pair': C['nulls']['real']['chance_second_pair']}}


# ---------------- 独立の再計算の一致 ----------------
def tol_second(C, floor):
    """二段目の許容（正本 `independent_recompute.stages.second`: 揺れの床の factor 倍と floor の大きい方・上限 `pilot.noise_max`・それに揺れの床を足す）。"""
    S = C['independent_recompute']['stages']['second']
    return K.cache_tol(floor, S['factor'], S['floor'], C['pilot']['noise_max']) + floor


def recompute_agreement(C, main_rows, eff_main, pair_names, hook, rewrite, pilot, dropped_cells=(), rows_subset=None):
    """二段の一致（正本 `independent_recompute.stages`・`agreement`）。hook と rewrite: 行の名 → {'noop_lo','effects': {'方向|符号': 効き目}}。v̂ の行（Nk の行を入れるかは案 16 の決め）。"""
    drop = set(dropped_cells)
    in_drop = lambda r: '%s|%s' % (r['scenario'], r['base']) in drop
    comps_of = lambda d: K.comparators_for(d, pair_names, C['nulls']['real']['swap_siblings'])
    nf = ['main:%s' % k for k, e in eff_main.items() if not all(math.isfinite(float(v)) for v in e.values())]
    for nm_, pth_ in (('hook', hook), ('rewrite', rewrite)):
        for rid_, o_ in (pth_ or {}).items():
            if not all(math.isfinite(float(v)) for v in [o_.get('noop_lo', 0.0)] + list((o_.get('effects') or {}).values())):
                nf.append('%s:%s' % (nm_, rid_))
    if nf:
        s2 = {'agree': False, 'labels_same': False, 'values_within_tol': False, 'reason': 'non_finite', 'non_finite': nf[:10]}
        f1 = None if rewrite is None else {'agree': False, 'reason': 'non_finite', 'non_finite': nf[:10]}
        return {'second': s2, 'tol_second': None, 'first': f1, 'tol_first': C['independent_recompute']['tol_stage1'], 'agree': False, 'reason': 'non_finite', 'non_finite': nf[:10]}
    n_iso = C['nulls']['isotropic']['count']

    def use(r):
        return r['direction'] == 'static' and not in_drop(r) and (rows_subset is None or r['id'] in rows_subset)

    want = {r['id'] for r in main_rows if use(r)}                        # 比べる行と二つの道の鍵の集合が一致しなければ不一致（DRY でも外さない・v0.4・U44・G-03）
    kd = {nm_: {'missing': sorted(want - set(pth_))[:10], 'extra': sorted(set(pth_) - want)[:10]} for nm_, pth_ in (('hook', hook or {}), ('rewrite', rewrite))
          if pth_ is not None and set(pth_) != want}
    if kd:
        s2 = {'agree': False, 'labels_same': False, 'values_within_tol': False, 'reason': 'key_set', 'key_set': kd}
        f1 = None if rewrite is None else {'agree': False, 'reason': 'key_set', 'key_set': kd}
        return {'second': s2, 'tol_second': None, 'first': f1, 'tol_first': C['independent_recompute']['tol_stage1'], 'agree': False, 'reason': 'key_set', 'key_set': kd}

    def override(path):
        ov = {}
        for r in main_rows:
            if not use(r) or r['id'] not in path:
                continue
            E = path[r['id']]['effects']
            s = r['sign']
            ov[r['id']] = {'effect': E['static|%+d' % s], 'iso': [E['iso:%d|%+d' % (i, s)] for i in range(n_iso)],
                           'comps_same': [E['real:%s|%+d' % (p, s)] for p in comps_of('static')], 'comps_opp': [E['real:%s|%+d' % (p, -s)] for p in comps_of('static')]}
        return ov

    def as_eff(ov):
        return {rid: [o['effect']] + list(o['iso']) + list(o['comps_same']) + list(o['comps_opp']) for rid, o in ov.items()}

    def with_noop(ov, path):
        return {rid: [path[rid]['noop_lo']] + v for rid, v in as_eff(ov).items()}
    main_ov = {}
    for r in main_rows:
        if not use(r):
            continue
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        main_ov[r['id']] = {'effect': eff_main[k]['static'], 'iso': [eff_main[k]['iso:%d' % i] for i in range(n_iso)],
                            'comps_same': [eff_main[k]['real:' + p] for p in comps_of('static')], 'comps_opp': [eff_main[kk]['real:' + p] for p in comps_of('static')]}
    sig = lambda ov: labels_signature(row_labels(C, main_rows, eff_main, pair_names, dropped_cells, p_override=ov)[0])
    hk, rw = override(hook), (override(rewrite) if rewrite is not None else None)
    t2 = tol_second(C, pilot['floor'])
    s2 = K.agreement(as_eff(main_ov), as_eff(hk), t2, sig(main_ov), sig(hk))
    s2 = dict(s2, agree=bool(s2['labels_same']), values_beyond_tol=not s2['values_within_tol'])
    out = {'second': s2, 'tol_second': t2, 'second_formal': int(pilot['batch']) == 1}
    out['first'] = None if rw is None else K.agreement(with_noop(hk, hook), with_noop(rw, rewrite), C['independent_recompute']['tol_stage1'], sig(hk), sig(rw))
    out['tol_first'] = C['independent_recompute']['tol_stage1']
    out['agree'] = bool(out['second']['agree'] and (out['first'] or {}).get('agree', False))
    return out


def reextract_agreement(C, EX, RX):
    """独立の再抽出の一致（正本 `independent_recompute.reextract`）: ‖h‖ と ‖v̂‖ の相対の差が `rel_tol` 以内・名前のある方向の余弦が `cos_min` 以上。
    EX: 抽出の記録（転記行 D の値）・RX: 再抽出の道の出力 {'h_norm_by_context': …, 'vhat_norm': …, 'named_cos': {名: 余弦}}。値は開かない（一致か不一致かだけ）。"""
    R = C['independent_recompute']['reextract']
    hn = EX['row_D']['h_norm_by_context']
    rel_h = max(abs(float(RX['h_norm_by_context'][k]) - float(v)) / float(v) for k, v in hn.items())
    rel_v = abs(float(RX['vhat_norm']) - float(EX['vhat_norm'])) / float(EX['vhat_norm'])
    cos = min(float(x) for x in RX['named_cos'].values())
    same_keys = sorted(RX['h_norm_by_context']) == sorted(hn) and sorted(RX['named_cos']) == sorted(C['directions']['named'])
    return {'agree': bool(same_keys and rel_h <= R['rel_tol'] and rel_v <= R['rel_tol'] and cos >= R['cos_min']), 'keys_same': same_keys,
            'rel_h_max': rel_h, 'rel_v': rel_v, 'cos_min': cos}


# ---------------- 記述 ----------------
def descriptive(C, main_out, names):
    mm = C['pilot']['mass_min']
    groups = {'named': set(names['named']), 'iso': set(names['iso']), 'real': set(names['real'])}
    mass = collections.OrderedDict()
    for k, o in main_out.items():
        m = {}
        for g, s in groups.items():
            vals = [v for d, v in o['mass'].items() if d in s]
            n_below = sum(1 for v in vals if v < mm)
            m[g] = {'below': n_below, 'n': len(vals), 'share': (n_below / len(vals)) if vals else None}
        mass[k] = m
    ties, spread = collections.OrderedDict(), collections.OrderedDict()
    for k, o in main_out.items():
        iso = np.array([v for d, v in o['effects'].items() if d.startswith('iso:')], dtype=np.float64)
        real = np.array([v for d, v in o['effects'].items() if d.startswith('real:')], dtype=np.float64)
        if iso.size:
            u, c = np.unique(iso, return_counts=True)
            ties[k] = float(c[c > 1].sum() / iso.size)
            q1, q3 = np.percentile(iso, 25), np.percentile(iso, 75)
            lo, hi = np.percentile(iso, 2.5), np.percentile(iso, 97.5)
            iqr_real = float(np.percentile(real, 75) - np.percentile(real, 25)) if real.size else None
            spread[k] = {'iqr': float(q3 - q1), 'central95': float(hi - lo), 'std': float(np.std(iso)), 'median': float(np.median(iso)), 'iqr_real': iqr_real,
                         'iqr_over_real': (float(q3 - q1) / iqr_real) if iqr_real else None}
    pa = {k: o['pa_noop'] for k, o in main_out.items()}
    return {'mass_below_min': mass, 'pa_noop': pa, 'iso_ties_share': ties, 'iso_spread': spread}


def path_difference(C, main_out, pd_out, pair_names, dropped_cells=()):
    """道の違いの記述（正本 `descriptive.path_difference`）: バッチ一の本の計算とバッチ 16 の道の札の違う行の数と効き目の差の最大（止める条件にせず、本の札も変えない）。"""
    eff_a = {k: o['effects'] for k, o in main_out.items()}
    eff_b = {k: o['effects'] for k, o in pd_out.items()}
    if sorted(eff_a) != sorted(eff_b) or any(sorted(eff_a[k]) != sorted(eff_b[k]) for k in eff_a):
        return {'comparable': False}
    la = labels_signature(row_labels(C, C['main_rows'], eff_a, pair_names, dropped_cells)[0])
    lb = labels_signature(row_labels(C, C['main_rows'], eff_b, pair_names, dropped_cells)[0])
    dmax = max(abs(float(eff_a[k][d]) - float(eff_b[k][d])) for k in eff_a for d in eff_a[k])
    return {'comparable': True, 'rows_label_differs': sorted(r for r in la if la[r] != lb[r]), 'n_rows_label_differs': sum(1 for r in la if la[r] != lb[r]), 'max_abs_diff': dmax}


def analyze(C, main_out, pilot_attempts, pair_names, names, hook=None, rewrite=None, rows_subset=None):
    """集計の全体（読みは付けない）。main_out: 升目と符号の鍵 → run_cell_sign の出力。pilot_attempts: 下見の試みの並び（最後が本の凍結の下見）。"""
    pilot = pilot_attempts[-1]
    dropped = (pilot.get('decision') or {}).get('dropped', [])
    nf = sorted({k for k, o in main_out.items() for d, v in list((o.get('effects') or {}).items()) + list((o.get('mass') or {}).items()) if not math.isfinite(float(v))})
    if nf:
        raise SystemExit('有限でない効き目か質量がある（止める）: %s' % nf[:5])
    eff = {k: o['effects'] for k, o in main_out.items()}
    lab, meta = row_labels(C, C['main_rows'], eff, pair_names, dropped)
    meta['floor'] = floor_marks(C, main_out, pilot, lab)
    truth, tmeta = prediction_truth(C, pilot_attempts, lab)
    out = collections.OrderedDict(version=VERSION, rows=lab, rows_meta=meta, predictions_truth=truth, predictions_meta=tmeta,
                                  descriptive=descriptive(C, main_out, names), chance=chance_after_drop(C, lab),
                                  summary_numbers=P.summary_numbers(summary_rows(C, lab)) if not tmeta['stopped'] else None)
    if hook is not None:
        out['recompute'] = recompute_agreement(C, C['main_rows'], eff, pair_names, hook, rewrite, pilot, dropped, rows_subset)
    return out


def floor_marks(C, main_out, pilot, lab):
    """床の余白の印（正本 `floor_margin`）: 行の升目の、本の計算の無操作の対数オッズの床と天井からの余白の近い方が、〈その升目の (vi) の (a) の値と、
    (vi) の (b) の升目の間の最大の、大きい方〉より小さいとき印。行は外さず、Holm は印の前の行で一度だけ掛けたまま（印で掛け直さない）。行の札に 'floor_mark' を足す。"""
    vi = pilot['vi']
    vb = max(float(v) for v in vi['b'].values())
    for rid, o in lab.items():
        cell = o['cell_sign'].rsplit('|', 1)[0]
        fm = collections.OrderedDict((k, P.floor_mark(main_out[k]['lo'][K.NOOP], C['pilot']['p_bounds'], vi['a'][cell], vb))
                                     for k in sorted(k for k in main_out if k.rsplit('|', 1)[0] == cell))
        o['floor_mark'] = dict(fm[o['cell_sign']], mark=any(v['mark'] for v in fm.values()), by_group=fm)     # 升目の二つの組のどちらかで印（保守側・二つの値を置く・v0.4・U17）
    return {'vi_a_max': max(float(v) for v in vi['a'].values()), 'vi_b_max': vb}


def summary_rows(C, lab):
    """要約の型の数（正本 `reading.summary`・`bprime_core.summary_numbers` に渡す行）: 方向・等方の外・二つ目の札・床の余白の印・効き目の側（等方の外の行だけ）。"""
    return [{'id': rid, 'direction': o['direction'], 'iso_outside': o['iso_outside'], 'second': o['second']['top'], 'mark': o['floor_mark']['mark'],
             'side': (o['side'] or {}).get('side') if o['iso_outside'] else None} for rid, o in lab.items()]


# ---------------- 手元の二つの段（一致だけを見る・結果を開く） ----------------
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
canon_sha16 = lambda obj: hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest().upper()[:16]
fr_core = lambda FR: {k: v for k, v in FR.items() if k != 'deviations'}


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


def load_outputs(dirs):
    """起動器の相 main と相 recompute の出力（組ごとの JSON・end の記録・session.json）を読む。同じ組が二つあれば止める。組の JSON の SHA-256 を end の記録と照らす。"""
    parts, sessions, files = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
    for d in dirs:
        S = json.load(open(os.path.join(d, 'session.json'), encoding='utf-8'))
        ends = glob.glob(os.path.join(d, 'end-*.json'))
        if len(ends) != 1:
            raise SystemExit('出力の置き場に end の記録がちょうど一つでない: %s' % d)
        E = json.load(open(ends[0], encoding='utf-8'))
        for fn, want in E['outputs_sha256'].items():
            m = re.fullmatch(r'(main|recompute)-(\w+)\.json', fn)
            if not m:
                continue
            part = m.group(2)
            if part in parts:
                raise SystemExit('同じ組が二つの置き場にある（止める）: %s' % part)
            p = os.path.join(d, fn)
            got = sha256f(p)
            if got != want:
                raise SystemExit('組 %s の出力の SHA-256 が end の記録と違う（止める）' % part)
            parts[part] = json.load(open(p, encoding='utf-8'))
            sessions[part] = S
            files[part] = {'dir': os.path.basename(os.path.normpath(d)), 'json_sha256': got, 'session_sha256': sha256f(os.path.join(d, 'session.json')), 'end_sha256': sha256f(ends[0])}
    return parts, sessions, files


def env_same(sessions):
    keys = ENV_KEYS
    ref = next(iter(sessions.values())) if sessions else {}
    diff = {k: {p: s.get(k) for p, s in sessions.items()} for k in keys if any(s.get(k) != ref.get(k) for s in sessions.values())}
    return {'same': not diff, 'diff': diff, 'strict': [k for k in diff if k in STRICT_ENV]}


def main_freeze_bad(C, FR, sessions, parts, pilot, EX, lock_now=None, frozen_now=None):
    """DRY でない一致だけを見る段の照らし（層三の一致の段の型を戻した・v0.4・U03・U08・U10）。戻り値: 外れの文の並び（空なら通る）。
    lock_now: (今の器の閉包, 今の SHA16 の表)・frozen_now: 本の凍結の凍結物の今の SHA16 の表。与えなければ凍結の器の関数で今の置き場から取る（自己検査は与える）。"""
    mf = FR.get('main_freeze') or {}
    if not mf:
        return ['凍結の記録に本の凍結が無い']
    bad = []
    if not FR.get('main_freeze_sha16') or FR.get('main_freeze_sha16') != P.main_freeze_sha16(FR):
        bad.append('本の凍結の節の正準の SHA16 が、節から出る値と違う（U10）')
    if (mf.get('pilot') or {}) != pilot:
        bad.append('本の凍結の下見の記録と、集計に渡した下見の記録が違う')
    canon_f = (mf.get('frozen_sha16') or {}).get(CANON_PATH)
    npz_f = ((mf.get('added') or {}).get('extraction') or {}).get('npz の SHA')
    if not npz_f or npz_f != EX.get('npz_sha256'):
        bad.append('抽出の記録の npz の SHA が本の凍結の値と違う')
    for p_, s_ in sessions.items():
        if s_.get('main_freeze_sha16') != FR.get('main_freeze_sha16'):
            bad.append('組 %s の session の本の凍結の節の SHA16 が凍結の記録と違う' % p_)
        if s_.get('canon_sha16') != canon_f or s_.get('directions_npz_sha256') != npz_f:
            bad.append('組 %s の session の正本か方向の npz の SHA が、本の凍結の値と違う' % p_)
    res = (parts.get('main') or {}).get('result') or {}
    if res.get('batch') != pilot.get('batch') or sorted(res.get('dropped') or []) != sorted((pilot.get('decision') or {}).get('dropped') or []):
        bad.append('組 main の出力のバッチか外した升目が、本の凍結の下見の記録と違う')
    if lock_now is None or frozen_now is None:
        import freeze_Bprime as FZ
        if lock_now is None:
            lock_now = (FZ.import_closure(FZ.TOOLS), FZ.closure_sha_map())
        if frozen_now is None:
            frozen_now = {f: (FZ.sha16f(FZ.P(f)) if os.path.exists(FZ.P(f)) else None) for f in (mf.get('frozen_sha16') or {})}
    bad += ['錠: %s' % x for x in P.lock_bad(FR.get('tools_import_closure') or [], FR.get('frozen_sha16') or {}, lock_now[0], lock_now[1])]     # 台帳を見ない（U03）
    bad += ['手元の凍結物が本の凍結の記録と違う: %s' % x for x in K.ledger_chain_bad(mf.get('frozen_sha16') or {}, frozen_now,
                                                                             (FR.get('deviations') or [])[int(mf.get('deviations_n') or 0):], paths=list(mf.get('frozen_sha16') or {}))]
    return bad


def runs_info(runs_dir, FR, pilot_attempts, need_stages=NEED_STAGES):
    """走行の表（正本 `computation.start_records`・T13・U04）: runs の起動の記録と出力の SHA の記録を段・組・セッションで並べ、コミットを起動の記録から取り、
    芯の `runs_bad`（組がそろう・要る段がそろう・下見の試みの数・台帳のやり直しの行）で照らす。本の凍結の器と同じ芯の関数。"""
    names = {fn: sha256f(os.path.join(runs_dir, fn)) for fn in sorted(os.listdir(runs_dir))} if os.path.isdir(runs_dir) else {}
    table = P.runs_table(names)
    for r in table:
        r['commit'] = json.load(open(os.path.join(runs_dir, r['start']['file']), encoding='utf-8')).get('commit') if r['start'] else None
    bad = P.runs_bad(table, need_stages, attempts={'pilot': len(pilot_attempts)}, reruns=P.reruns_of((FR or {}).get('deviations') or []))
    return {'table': table, 'bad': bad, 'need_stages': list(need_stages)}


def dry_view(C, names):
    """DRY の出力だけに使う正本の写し（v0.3・K21）: 等方の本数を抽出の記録の等方の名の数（起動器の DRY の写しの本数）に合わせる。ほかの鍵は変えない。"""
    Cd = json.loads(json.dumps(C, ensure_ascii=False))
    Cd['nulls']['isotropic']['count'] = len(names['iso'])
    return Cd


def judge(C, parts, sessions, pilot_attempts, pair_names, EX, files=None, FR=None, lock_now=None, frozen_now=None):
    """一致だけを見る段: 器の誤りの有無・組の環境・二段の一致と独立の再抽出の一致か不一致かだけを返す（効き目の値と差の最大は返さない）。"""
    out = collections.OrderedDict(parts=list(parts), tool_error={p: bool(v.get('tool_error')) for p, v in parts.items()}, env=env_same(sessions))
    dry = any(bool(s.get('dry')) for s in sessions.values())
    out['dry'] = dry
    out['inputs'] = files
    if FR is not None:
        devs_ = FR.get('deviations') or []
        out['freeze_record_core_sha16'] = canon_sha16(fr_core(FR))
        out['deviations_n'] = len(devs_)
        out['deviations_sha16'] = canon_sha16(devs_)
    stop = lambda why: (out.update(first=None, second=None, reextract=None, agree=None, reason=why), out)[1]
    need = {'main', 'hook', 'rewrite', 'reextract'}
    if any(out['tool_error'].values()) or not need <= set(parts):
        return stop('器の誤りか、組の欠け（%s）' % sorted(need - set(parts)))
    drys = {p: bool(s.get('dry')) for p, s in sessions.items()}
    if len(set(drys.values())) > 1:
        return stop('組の間で DRY の印が違う: %s' % drys)
    if out['env']['strict']:
        return stop('組の間の環境（中身）が違う（組の間で器が違えばすべての組をやり直す・U08）: %s' % out['env']['strict'])
    pilot = pilot_attempts[-1]
    if not dry:
        if FR is None:
            return stop('DRY でないのに凍結の記録が無い')
        mb = main_freeze_bad(C, FR, sessions, parts, pilot, EX, lock_now=lock_now, frozen_now=frozen_now)
        if mb:
            return stop('本の凍結の照らしが外れた: %s' % mb)
        n_can = C['nulls']['isotropic']['count']
        n_main = {k: sum(1 for d in o['effects'] if d.startswith('iso:')) for k, o in parts['main']['result']['cells'].items()}
        if any(v not in (n_can,) for k, v in n_main.items() if parts['main']['result']['cells'][k]['effects'].get('static') is not None):
            return stop('DRY でないのに等方の本数が正本と違う')
    eff = {k: o['effects'] for k, o in parts['main']['result']['cells'].items()}
    hook = parts['hook']['result']['hook']
    rewrite = parts['rewrite']['result']
    ag = recompute_agreement(C, C['main_rows'], eff, pair_names, hook, rewrite, pilot, (pilot.get('decision') or {}).get('dropped', []), rows_subset=set(hook) if dry else None)
    rx = reextract_agreement(C, EX, parts['reextract']['result'])
    out.update(first=None if ag['first'] is None else bool(ag['first']['agree']), second=bool(ag['second']['agree']), reextract=bool(rx['agree']),
               agree=bool(ag['agree'] and rx['agree']), second_values_within_tol=bool(ag['second']['values_within_tol']),
               reason=None if (ag['agree'] and rx['agree']) else ('独立の再抽出が一致しない' if not rx['agree'] else
                                                                  ('比べる行と道の鍵の集合が違う: %s' % ag.get('key_set') if ag.get('reason') == 'key_set' else
                                                                   ('一段目の道が無い' if ag['first'] is None else '二段のどちらかが一致しない'))))
    return out


def open_results(C, parts, sessions, pilot_attempts, pair_names, names, closed, runs=None):
    """結果を開く段（登録者と一緒に・一致だけを見る段が一致したとき）: 集計の全体と、報告に並べるもの（下見の記録・頭の確かめ・層ごとの差分・道の違い・行動の下見・環境）。"""
    rc = {'hook': parts['hook']['result']['hook'], 'rewrite': parts['rewrite']['result']}
    dry = any(bool(s.get('dry')) for s in sessions.values())
    A = analyze(C, parts['main']['result']['cells'], pilot_attempts, pair_names, names, hook=rc['hook'], rewrite=rc['rewrite'], rows_subset=set(rc['hook']) if dry else None)
    pil = pilot_attempts[-1]
    if 'pathdiff' in parts:
        A['path_difference'] = path_difference(C, parts['main']['result']['cells'], parts['pathdiff']['result']['cells'], pair_names, (pil.get('decision') or {}).get('dropped', []))
    A['dry'] = dry
    A['pilot_attempts'] = pilot_attempts
    A['head'] = parts['main']['result']['head']
    A['main_run'] = {k: parts['main']['result'].get(k) for k in ('batch', 'dropped')}
    A['layerwise'] = {k: o['layers'] for k, o in parts['main']['result']['cells'].items()}
    A['behavior'] = {'summaries': closed.get('summaries'), 'row_C': closed.get('row_C'), 'external': closed.get('external'),
                     'tool_error': bool(closed.get('tool_error')), 'tool_error_message': closed.get('tool_error_message'),     # 器の誤りで閉じた行動の下見（v0.4・U07）
                     'prior_closed': closed.get('prior_closed') or []}                                                      # やり直しの前の閉じた記録（報告の頭に並べる・v0.4・U09）
    A['sessions'] = {p: {k: s.get(k) for k in ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'determinism', 'packaged_at', 'session_id', 'start_record', 'start_sha256',
                                               'main_freeze_sha16', 'directions_npz_sha256')} for p, s in sessions.items()}
    A['runs'] = runs                                                       # 走行の表（段・組・セッション・起動の記録と end の記録の SHA・コミット・v0.4・U04）
    A['env'] = env_same(sessions)
    A['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
    return A


def open_checked(C, parts, sessions, files, J, pilot_attempts, pair_names, names, EX, closed, FR=None, judge_sha16=None, runs_dir=None, lock_now=None, frozen_now=None):
    """結果を開く段の確かめ（層三の型）: 一致だけを見る段の記録が一致で、読む出力の同定が同じで、凍結の記録の台帳の外が判定の時と同じ・台帳の頭が同じ。
    同じ入力で一致だけを見る段をもう一度走らせ、判定の記録と同じこと。開いた集計の一致が判定と違えば止める。"""
    if not J.get('agree'):
        raise SystemExit('一致だけを見る段の記録が一致していない（結果を開かない）')
    if J.get('inputs') != files:
        raise SystemExit('結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）')
    dry = any(bool(s.get('dry')) for s in sessions.values())
    if not dry:
        if FR is None:
            raise SystemExit('DRY でないのに凍結の記録が無い（開かない）')
        devs_ = FR.get('deviations') or []
        n_ = J.get('deviations_n')
        if canon_sha16(fr_core(FR)) != J.get('freeze_record_core_sha16'):
            raise SystemExit('凍結の記録（台帳の外）が一致だけを見る段の後に変わった（開かない）')
        if n_ is None or len(devs_) < n_ or canon_sha16(devs_[:n_]) != J.get('deviations_sha16'):
            raise SystemExit('凍結の記録の台帳の、一致だけを見る段の時の行が変わった（開かない）')
    J2 = json.loads(json.dumps(judge(C, parts, sessions, pilot_attempts, pair_names, EX, files, FR, lock_now=lock_now, frozen_now=frozen_now), ensure_ascii=False, default=float))
    skip_ = ('written_utc', 'clause', 'deviations_n', 'deviations_sha16')
    diff_ = sorted(k for k in set(J) | set(J2) if k not in skip_ and J.get(k) != J2.get(k))
    if diff_:
        raise SystemExit('一致だけを見る段を同じ入力でもう一度走らせた答えが、判定の記録と違う（開かない）: %s' % diff_)
    runs = None
    if runs_dir is not None or not dry:                                     # DRY でないときは走行の表を必ず照らす（外れは止める・v0.4・U04）
        runs = runs_info(runs_dir or os.path.join(RECS, 'runs'), FR, pilot_attempts)
        if runs['bad']:
            raise SystemExit('走行の表の照らしが外れた（開かない・T13）: %s' % runs['bad'])
    A = open_results(C, parts, sessions, pilot_attempts, pair_names, names, closed, runs=runs)
    rc = A.get('recompute') or {}
    got = (None if rc.get('first') is None else bool(rc['first']['agree']), bool((rc.get('second') or {}).get('agree')))
    if got != (J.get('first'), J.get('second')):
        raise SystemExit('開いた集計の二段の一致が、一致だけを見る段と違う（書かない）')
    rx = reextract_agreement(C, EX, parts['reextract']['result'])
    if bool(rx['agree']) != J.get('reextract'):
        raise SystemExit('開いた独立の再抽出の一致が、一致だけを見る段と違う（書かない）')
    A['reextract'] = rx                                                   # 報告の組み立ての器が読む（v0.1・掃き出しで見つけた欠け）
    A['inputs'] = files
    A['judge_record_sha16'] = judge_sha16
    return A


def open_stopped(C, FR, closed, runs_dir=None, lock_now=None):
    """下見が「止める」になったとき（下見が器の誤りで終わり、やり直さないときを含む）の集計の出力（v0.4・K26）。本の計算を走らせないので、
    下見の試みと予想の答え（q1 だけ）・走行の表・行動の下見を置く。本の凍結の節の SHA16 と、下見の前の凍結から動かせない器の錠を照らす（U03・U10）。報告の組み立ての器が読む。"""
    mf = FR.get('main_freeze') or {}
    atts = mf.get('pilot_attempts')
    if not atts:
        raise SystemExit('凍結の記録に本の凍結の下見の試みが無い')
    tr, tm = prediction_truth(C, atts, {})
    if not tm['stopped']:
        raise SystemExit('下見の決定が「止める」でない（結果は一致だけを見る段と結果を開く段で開く）')
    bad = []
    if not FR.get('main_freeze_sha16') or FR.get('main_freeze_sha16') != P.main_freeze_sha16(FR):
        bad.append('本の凍結の節の正準の SHA16 が、節から出る値と違う（U10）')
    if lock_now is None:
        import freeze_Bprime as FZ
        lock_now = (FZ.import_closure(FZ.TOOLS), FZ.closure_sha_map())
    bad += ['錠: %s' % x for x in P.lock_bad(FR.get('tools_import_closure') or [], FR.get('frozen_sha16') or {}, lock_now[0], lock_now[1])]
    if bad:
        raise SystemExit('止めたときの集計の照らしが外れた: %s' % bad)
    runs = runs_info(runs_dir or os.path.join(RECS, 'runs'), FR, atts, need_stages=('extract', 'behavior', 'pilot'))     # 本の計算は走らせない
    if runs['bad']:
        raise SystemExit('走行の表の照らしが外れた（T13）: %s' % runs['bad'])
    return collections.OrderedDict([
        ('version', VERSION), ('pilot_attempts', atts), ('predictions_truth', tr), ('predictions_meta', tm), ('dry', False), ('runs', runs),
        ('behavior', {'summaries': closed.get('summaries'), 'row_C': closed.get('row_C'), 'external': closed.get('external'), 'tool_error': bool(closed.get('tool_error')),
                      'tool_error_message': closed.get('tool_error_message'), 'prior_closed': closed.get('prior_closed') or []}),
        ('judge_record_sha16', None), ('inputs', None),
        ('clause', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')])


def _selftest():
    """合成の効き目で、札・予想の答え・二段の一致・記述・道の違いを通す（等方を減らした正本の写し）。"""
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    Cs = json.loads(json.dumps(C))
    n_iso = 999                                            # 等方の本数を減らしても、割合の最小（2 ÷ 1000）が Holm の一段目（0.05 ÷ 16）を下回る数
    Cs['nulls']['isotropic']['count'] = n_iso
    rng = np.random.default_rng(3)
    pairs = []
    arms = C['nulls']['real']['arms']
    for i in range(len(arms)):
        for j in range(i + 1, len(arms)):
            pairs.append('%s~%s' % (arms[i], arms[j]))
    names = {'named': list(C['directions']['named']), 'iso': ['iso:%d' % i for i in range(n_iso)], 'real': ['real:' + p for p in pairs]}
    main_out = collections.OrderedDict()
    cs = [(sc, b, g) for sc, b, g in C['cell_signs_main']]
    rev = [(sc, b, -g) for sc, b, g in cs if (sc, b, -g) not in cs]
    for sc, b, g in cs + rev:
        k = key3(sc, b, g)
        eff = {d: float(rng.normal(0, 0.1)) for d in names['iso'] + names['real']}
        if (sc, b, g) in cs:
            eff.update({d: float(rng.normal(0, 0.1)) for d in names['named']})
            if b == 'O-Ncold' and g == -1:
                eff['static'] = 5.0                        # 等方の外になる行（合成）
        mass = {d: 0.95 for d in eff}
        mass[names['iso'][0]] = 0.5
        main_out[k] = {'effects': eff, 'mass': mass, 'pa_noop': 0.4, 'lo': {K.NOOP: (9.2 if sc == 'SK' else 0.0)}}
    cells = sorted({'%s|%s' % (sc, b) for sc, b, _ in cs})
    pilot = {'decision': {'q1': '続ける', 'dropped': []}, 'batch': 16, 'floor': 0.001,
             'vi': {'a': {c: (0.05 if c.startswith('SK|') else 0.002) for c in cells}, 'b': {c: 0.001 for c in cells}}}
    A = analyze(Cs, main_out, [pilot], pairs, names)
    n_out = sum(1 for o in A['rows'].values() if o['iso_outside'])
    assert A['rows_meta']['m_rows'] == len(C['main_rows']) and n_out >= 1, (A['rows_meta'], n_out)
    marks = {rid: o['floor_mark']['mark'] for rid, o in A['rows'].items()}
    # SK の升目は天井の近く（logit(0.9999) ≒ 9.2102・余白 ≒ 0.0102 が (a) の 0.05 より小さい → 印）・ほかの升目は余白 ≒ 9.21 で印なし
    assert all(marks[rid] == (A['rows'][rid]['cell_sign'].startswith('SK|')) for rid in marks), marks
    assert A['summary_numbers']['n'] == len(C['main_rows']) and A['summary_numbers']['k'] == n_out
    assert A['predictions_truth']['q1.pilot'] == '続ける' and A['predictions_truth']['q2.vhat_iso'] in ('一から三', '四以上')
    assert A['descriptive']['mass_below_min'][key3(*cs[0])]['iso']['below'] == 1
    stop_tr, _ = prediction_truth(Cs, [dict(pilot, decision={'q1': '止める', 'dropped': []})], A['rows'])
    assert stop_tr['q1.pilot'] == '止める' and stop_tr['q2.vhat_iso'] is None
    hook = collections.OrderedDict()
    for r in C['main_rows']:
        if r['direction'] != 'static':
            continue
        k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
        s = r['sign']
        comps = K.comparators_for('static', pairs, C['nulls']['real']['swap_siblings'])
        E = {'static|%+d' % s: main_out[k]['effects']['static']}
        E.update({'iso:%d|%+d' % (i, s): main_out[k]['effects']['iso:%d' % i] for i in range(n_iso)})
        E.update({'real:%s|%+d' % (p, s): main_out[k]['effects']['real:' + p] for p in comps})
        E.update({'real:%s|%+d' % (p, -s): main_out[kk]['effects']['real:' + p] for p in comps})
        hook[r['id']] = {'noop_lo': 0.0, 'effects': E}
    ag = recompute_agreement(Cs, C['main_rows'], {k: o['effects'] for k, o in main_out.items()}, pairs, hook, hook, pilot)
    assert ag['agree'] and ag['first']['agree'] and ag['second']['agree'], ag
    bad = json.loads(json.dumps(hook))
    rid0 = next(iter(bad))
    bad[rid0]['effects'][next(iter(bad[rid0]['effects']))] += 1.0
    ag2 = recompute_agreement(Cs, C['main_rows'], {k: o['effects'] for k, o in main_out.items()}, pairs, hook, bad, pilot)
    assert not ag2['first']['agree'], ag2
    # 比べる行と道の鍵の集合（v0.4・U44・G-03）
    short = json.loads(json.dumps(hook))
    short.pop(rid0)
    ag3 = recompute_agreement(Cs, C['main_rows'], {k: o['effects'] for k, o in main_out.items()}, pairs, hook, short, pilot)
    ag4 = recompute_agreement(Cs, C['main_rows'], {k: o['effects'] for k, o in main_out.items()}, pairs, short, short, pilot)
    assert not ag3['agree'] and ag3['reason'] == 'key_set' and not ag4['agree'] and ag4['reason'] == 'key_set', (ag3.get('reason'), ag4.get('reason'))
    # 組の間の環境: コミットの違いは記述・器の違いは止める（v0.4・U08）
    s_a = {'commit': 'a' * 40, 'dry': False, 'canon_sha16': 'C', 'tools_sha16': {'t': '1'}, 'main_freeze_sha16': 'M', 'directions_npz_sha256': 'N'}
    e1 = env_same({'main': s_a, 'hook': dict(s_a, commit='b' * 40)})
    e2 = env_same({'main': s_a, 'hook': dict(s_a, tools_sha16={'t': '2'})})
    assert not e1['same'] and e1['strict'] == [] and e2['strict'] == ['tools_sha16'], (e1, e2)
    # DRY でない照らし（層三の型・錠・本の凍結の節の SHA16・v0.4）
    mf = {'pilot': pilot, 'frozen_sha16': {CANON_PATH: 'C', 'tools/analyze_Bprime.py': 'A'}, 'added': {'extraction': {'npz の SHA': 'N'}}, 'deviations_n': 0}
    FRs = {'frozen_sha16': {CANON_PATH: 'C', 'tools/analyze_Bprime.py': 'A'}, 'tools_import_closure': ['tools/analyze_Bprime.py'], 'main_freeze': mf, 'deviations': []}
    FRs['main_freeze_sha16'] = P.main_freeze_sha16(FRs)
    ss = {'main': dict(s_a, main_freeze_sha16=FRs['main_freeze_sha16']), 'hook': dict(s_a, main_freeze_sha16=FRs['main_freeze_sha16'])}
    pm = {'main': {'result': {'batch': 16, 'dropped': []}}}
    lk, fz = (['tools/analyze_Bprime.py'], {'tools/analyze_Bprime.py': 'A'}), {CANON_PATH: 'C', 'tools/analyze_Bprime.py': 'A'}
    assert main_freeze_bad(Cs, FRs, ss, pm, pilot, {'npz_sha256': 'N'}, lock_now=lk, frozen_now=fz) == []
    for why_, args_ in (('器の錠', dict(lock_now=(lk[0], {'tools/analyze_Bprime.py': 'B'}), frozen_now=fz)),
                        ('手元の凍結物', dict(lock_now=lk, frozen_now=dict(fz, **{CANON_PATH: 'X'})))):
        assert main_freeze_bad(Cs, FRs, ss, pm, pilot, {'npz_sha256': 'N'}, **args_), why_
    assert main_freeze_bad(Cs, FRs, ss, pm, pilot, {'npz_sha256': 'Z'}, lock_now=lk, frozen_now=fz)                                  # npz の SHA
    assert main_freeze_bad(Cs, FRs, dict(ss, hook=dict(ss['hook'], main_freeze_sha16='Q')), pm, pilot, {'npz_sha256': 'N'}, lock_now=lk, frozen_now=fz)   # 組の節の SHA16
    assert main_freeze_bad(Cs, FRs, ss, {'main': {'result': {'batch': 1, 'dropped': []}}}, pilot, {'npz_sha256': 'N'}, lock_now=lk, frozen_now=fz)    # バッチ
    FRt = json.loads(json.dumps(FRs))
    FRt['main_freeze']['deviations_n'] = 1
    assert main_freeze_bad(Cs, FRt, ss, pm, pilot, {'npz_sha256': 'N'}, lock_now=lk, frozen_now=fz)                                 # 節を書き換えると SHA16 が合わない
    # 床の余白の印は升目の二つの組のどちらかで（v0.4・U17）
    mo2 = json.loads(json.dumps(main_out))
    kS = next(k for k in mo2 if k.startswith('S1|O-Ncold|'))
    kS2 = next(k for k in mo2 if k.startswith('S1|O-Ncold|') and k != kS)
    mo2[kS2]['lo'] = {K.NOOP: 9.21}                                         # 天井からの余白 ≒ 0.0002 が S1 の (a) の 0.002 より小さい → 印
    lab2, _ = row_labels(Cs, C['main_rows'], {k: o['effects'] for k, o in mo2.items()}, pairs, [])
    floor_marks(Cs, mo2, pilot, lab2)
    assert all(o['floor_mark']['mark'] and len(o['floor_mark']['by_group']) == 2 for o in lab2.values() if o['cell_sign'].startswith('S1|O-Ncold|'))
    # 止めたときの集計の出力（v0.4・K26）
    import tempfile
    stop_p = dict(pilot, decision={'q1': '止める', 'stop': True, 'reason': 'i_ii', 'dropped': []})
    FRst = json.loads(json.dumps(FRs))
    FRst['main_freeze']['pilot_attempts'] = [stop_p]
    FRst['main_freeze']['pilot'] = stop_p
    FRst['main_freeze_sha16'] = P.main_freeze_sha16(FRst)
    with tempfile.TemporaryDirectory() as td_:
        for ph in ('extract', 'behavior', 'pilot'):
            for kd in ('start', 'end'):
                with open(os.path.join(td_, '%s-%s-0123abcd.json' % (kd, ph)), 'w', encoding='utf-8') as fh:
                    json.dump({'kind': 'x', 'commit': 'c' * 40}, fh)
        Ast = open_stopped(Cs, FRst, {'summaries': None, 'tool_error': False}, runs_dir=td_, lock_now=lk)
        assert Ast['predictions_meta']['stopped'] and Ast['predictions_truth']['q1.pilot'] == '止める' and len(Ast['runs']['table']) == 3 and not Ast['runs']['bad']
        try:
            open_stopped(Cs, FRst, {}, runs_dir=td_, lock_now=(lk[0], {'tools/analyze_Bprime.py': 'B'}))
            raise AssertionError('錠が外れても止まらない')
        except SystemExit:
            pass
        try:
            open_stopped(Cs, FRs, {}, runs_dir=td_, lock_now=lk)
            raise AssertionError('続けるの決定でも止めたときの段が書く')
        except SystemExit:
            pass
    pd = path_difference(Cs, main_out, main_out, pairs)
    assert pd['comparable'] and pd['n_rows_label_differs'] == 0 and pd['max_abs_diff'] == 0.0
    print('analyze_Bprime.py %s SELFTEST PASS（主の行 %d・等方の外 %d・二段の一致・壊した一段目の不一致・鍵の集合の不一致・組の環境・本の凍結の照らし 7・升目の二つの組の印・止めたときの段・道の違い 0）'
          % (VERSION, A['rows_meta']['m_rows'], n_out))


def names_of(EX):
    """抽出の記録の組の名から方向の名（名前のある方向・等方・実在の差）と実在の差の対の名を作る（npz は読まない）。"""
    G_ = EX['groups']
    names = {'named': list(G_['named']['names']), 'iso': ['iso:%d' % i for i in range(int(G_['iso']['count']))], 'real': ['real:' + p for p in G_['real']['names']]}
    return names, [n[len('real:'):] for n in names['real']]


def cli(argv):
    """手元の二つの段の口（v0.2）: judge（一致だけを見る段・値を印字しない）と open（結果を開く段・登録者と一緒に）。
    DRY の出力は `--pilot <下見の記録の JSON>` で下見の記録を与える。DRY でない出力は `--freeze <凍結の記録>` の本の凍結の下見の試みを使う。"""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['judge', 'open', 'stopped'])
    ap.add_argument('--dirs', nargs='+', help='相 main と相 recompute の出力の置き場（judge と open）')
    ap.add_argument('--extract', help='抽出の記録（extraction-record-Bprime.json・judge と open）')
    ap.add_argument('--pilot', help='DRY のときの下見の記録（pilot-Bprime.json）')
    ap.add_argument('--freeze', help='凍結の記録（DRY でないとき）')
    ap.add_argument('--judge', help='open のとき: 一致だけを見る段の記録')
    ap.add_argument('--closed', help='open のとき: 行動の下見の閉じた記録')
    ap.add_argument('--runs', help='open のとき: 起動の記録と出力の SHA の記録の置き場（DRY でないときの既定は records/Bprime/runs・v0.4）')
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    if a.stage == 'stopped':                                              # 下見が止めたときの集計の出力（v0.4・K26）
        if not (a.freeze and a.closed):
            raise SystemExit('stopped には --freeze と --closed が要る')
        if os.path.exists(a.out):
            raise SystemExit('既にある（一度だけ書く）: %s' % a.out)
        A = open_stopped(C, json.load(open(a.freeze, encoding='utf-8')), json.load(open(a.closed, encoding='utf-8')), runs_dir=a.runs)
        with open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(A, fh, ensure_ascii=False, indent=1, default=float)
        print('[analyze_Bprime] 止めたときの集計の出力: 書いた %s（SHA16 %s）' % (os.path.basename(a.out), sha16f(a.out)))
        return A
    if not (a.dirs and a.extract):
        raise SystemExit('judge と open には --dirs と --extract が要る')
    parts, sessions, files = load_outputs(a.dirs)
    EX = json.load(open(a.extract, encoding='utf-8'))
    names, pair_names = names_of(EX)
    if sessions and all(bool(s.get('dry')) for s in sessions.values()):
        C = dry_view(C, names)                     # DRY の出力だけ: 等方の本数を抽出の記録に合わせる（v0.3・K21・DRY でない出力は正本のまま）
    FR = json.load(open(a.freeze, encoding='utf-8')) if a.freeze else None
    if FR is not None:
        atts = (FR.get('main_freeze') or {}).get('pilot_attempts')
        if not atts:
            raise SystemExit('凍結の記録に本の凍結の下見の試みが無い')
    elif a.pilot:
        atts = [json.load(open(a.pilot, encoding='utf-8'))]
    else:
        raise SystemExit('--freeze か（DRY のとき）--pilot が要る')
    if os.path.exists(a.out):
        raise SystemExit('既にある（一度だけ書く）: %s' % a.out)
    if a.stage == 'judge':
        J = json.loads(json.dumps(judge(C, parts, sessions, atts, pair_names, EX, files, FR), ensure_ascii=False, default=float))
        J['written_utc'] = datetime_utc()
        J['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
        with open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(J, fh, ensure_ascii=False, indent=1)
        print('[analyze_Bprime] 一致だけを見る段: 一致 %s（一段目 %s・二段目 %s・再抽出 %s）・理由 %s' % (J.get('agree'), J.get('first'), J.get('second'), J.get('reextract'), J.get('reason')))
        return J
    if not (a.judge and a.closed):
        raise SystemExit('open には --judge と --closed が要る')
    J = json.load(open(a.judge, encoding='utf-8'))
    closed = json.load(open(a.closed, encoding='utf-8'))
    A = open_checked(C, parts, sessions, files, J, atts, pair_names, names, EX, closed, FR=FR, judge_sha16=sha16f(a.judge), runs_dir=a.runs)
    with open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(A, fh, ensure_ascii=False, indent=1, default=float)
    print('[analyze_Bprime] 結果を開く段: 書いた %s（SHA16 %s）' % (os.path.basename(a.out), sha16f(a.out)))
    return A


def datetime_utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] in ('judge', 'open', 'stopped'):
        sys.stdout.reconfigure(encoding='utf-8')
        cli(sys.argv[1:]); sys.exit(0)
    print(__doc__)
