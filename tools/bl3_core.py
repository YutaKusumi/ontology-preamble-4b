# -*- coding: utf-8 -*-
"""bl3_core.py v4 —— B-lens 層三（Bl3）の計算の芯（numpy だけ・重みも試行も読まない・2026-09-25）。

正本 `design/contrasts-Bl3.json` の決まりを、重みや試行を読まない純粋な関数に置く。走らせる器 `tools/bl3_run.py`・集計の器 `tools/analyze_Bl3.py`・
合成データの器 `tools/dry_run_Bl3.py` が同じ関数を呼ぶ（同じ式を二度書かない）。B-lens の芯 `tools/blens_core.py` の関数は読み取りだけで呼ぶ。

置くもの:
  - 読み取りの量（`readout.primary.quantity`）: 選択肢 a の文字の対数オッズ z_a − logsumexp（ほかの選択の文字と refuse の頭）・集合の中の a の確率・全語彙の質量。
  - 割合と裾（`labels.p_rule`）: `blens_core.p_equal_tailed` と、上の裾と下の裾の本数・割合を決めた裾。Holm（`blens_core.holm`・p が段を下回る）。
  - 効き目の側（`labels.side_rule`）: 等方の帰無の中央値と四分位・零が四分位の間なら符号だけ。
  - 二つ目の札（`labels.second`）: 比べる相手の中央値を中心にした最上位（`blens_core.top_rank` に中心を引いた値を渡す）・向きまで数えた順位と対の単位の順位・等方の最上位の割合。
  - 門（`gate`）: 行の符号を +1 にし、家族の鍵を「升目|符号」にして `blens_core.gate_perm` を呼ぶ。外した升目の行と、行の無くなった単位を除く。
  - 下見の機械の決定（`pilot`）: (vi) の (a)(b)・揺れの床・近道の許容・(i)(ii) の升目の決定・q1 との対応・(iii) の文の選び方・(iv) の印・(v) の近道の決定。
  - 独立の再計算の一致（`independent_recompute.agreement`）と、予想の採点（`predictions`・q7 の決まり・門が判定不能のとき）。
  - 比べる相手の除き方の錨（裁定 D231）: `comparators_for` の除く対を、B-lens の凍結の器 `tools/blens_lens.py` の `OWN_PAIR` と正本の兄弟の対に照らす。
  - 逸脱の台帳の器の差分の照らし（裁定 D239）: 路ごとに台帳の差分（path・before・after）を記した順につなげ、凍結の値から今の値まで前後がつながるときだけ許す。
  - バッチの組み方（`readout.primary.batching`）: 升目と符号ごとの方向の並び（`readout.primary.order_seed` の種）・零のベクトルの無操作・端数を零のベクトルで埋める。
用法: python tools/bl3_core.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, math, json, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import blens_core as C

VERSION = 'v4'          # v4（2026-09-26・裁定 D239）: 逸脱の台帳の器の差分を路ごとにつなげて照らす関数／v3（2026-09-25・裁定 D236）: 有限でない値で割合と裾は止め、一致の関数は一致しないと答える／v2（裁定 D231）: 比べる相手の除き方の錨
NOOP, PAD = 'noop', 'pad'


# ---------------- 読み取りの量 ----------------
def lse(x, axis=-1):
    x = np.asarray(x, dtype=np.float64)
    m = np.max(x, axis=axis, keepdims=True)
    return (m + np.log(np.sum(np.exp(x - m), axis=axis, keepdims=True))).squeeze(axis)


def log_odds_a(Z, i_a, i_others):
    """選択肢 a の文字の対数オッズ（行ごと）: z_a − logsumexp（ほかの選択の文字と refuse の頭）。Z は読み取りの集合の出口の値（行 × 集合）。"""
    Z = np.atleast_2d(np.asarray(Z, dtype=np.float64))
    return Z[:, i_a] - lse(Z[:, list(i_others)], axis=-1)


def prob_a_in_set(Z, i_a, i_set):
    """選択の文字と refuse の頭の中での選択肢 a の文字の確率（生の softmax）。"""
    Z = np.atleast_2d(np.asarray(Z, dtype=np.float64))
    return np.exp(Z[:, i_a] - lse(Z[:, list(i_set)], axis=-1))


def mass_of_set(Z_full, set_ids):
    """全語彙の生の softmax での、読み取りの集合の確率の和（行ごと）。"""
    Z_full = np.atleast_2d(np.asarray(Z_full, dtype=np.float64))
    return np.exp(lse(Z_full[:, list(set_ids)], axis=-1) - lse(Z_full, axis=-1))


# ---------------- 割合と裾・Holm ----------------
def p_and_tail(m, null):
    """両側に等しい裾の割合（`blens_core.p_equal_tailed`）と、上の裾と下の裾の本数・割合を決めた裾（上・下・同じ）。"""
    null = np.asarray(null, dtype=np.float64)
    if not (np.isfinite(m) and np.all(np.isfinite(null))):
        raise ValueError('有限でない値に割合と裾を当てようとした（裁定 D236）')
    up, lo = int(np.sum(null >= m)), int(np.sum(null <= m))
    tail = 'upper' if up < lo else ('lower' if lo < up else 'tie')
    return {'p': C.p_equal_tailed(m, null), 'upper': up, 'lower': lo, 'tail': tail, 'K': int(len(null))}


def holm(pvals, alpha):
    return C.holm(pvals, alpha)


def holm_limits(K, alpha, m_rows):
    """Holm の各段を通れる外側の帰無の本数の上限（両側に等しい裾の割合 2(1+e)/(1+K) が段を下回る e の最大・下回らなければ -1）。"""
    out = []
    for step in range(1, m_rows + 1):
        thr = alpha / (m_rows - step + 1)
        es = [e for e in range(0, K) if 2 * (1 + e) / (1 + K) < thr]
        out.append(max(es) if es else -1)
    return out


# ---------------- 効き目の側 ----------------
def effect_side(e, iso_null):
    """等方の外の行の効き目の側（正本 `labels.side_rule`）。零が等方の帰無の下の四分位と上の四分位の間なら、中央値を零とみなし符号だけを書く。
    それ以外は、中央値と同じ向きで中央値より零から遠い（stronger）・零と中央値の間（weaker・零と中央値の値そのものを含む）・零を越えて反対の向き（opposite）。"""
    null = np.asarray(iso_null, dtype=np.float64)
    m0 = float(np.median(null))
    q1, q3 = float(np.percentile(null, 25)), float(np.percentile(null, 75))
    out = {'median': m0, 'q1': q1, 'q3': q3}
    if q1 <= 0.0 <= q3:
        out.update({'side': 'sign_only', 'sign': int(np.sign(e))})
        return out
    s0 = 1.0 if m0 > 0 else -1.0
    if e * s0 > 0 and abs(e) > abs(m0):
        out['side'] = 'stronger'
    elif e * s0 >= 0:
        out['side'] = 'weaker'
    else:
        out['side'] = 'opposite'
    return out


# ---------------- 二つ目の札 ----------------
def second_label(e_row, comps_oriented, comps_pairs):
    """二つ目の札（正本 `labels.second`）。comps_oriented: 比べる相手の効き目（両方の向き）・comps_pairs: 対ごとの (向き一, 向き二)。
    中心＝比べる相手の中央値。最上位は、行の中心からの距離が比べる相手の距離のすべてを上回ること（同じ値は上回らない・`blens_core.top_rank` に中心を引いた値を渡す）。
    順位: 向きまで数えた順位（1 ＋ 距離が行の距離以上の比べる相手の数）と、対の単位の順位（対の値＝両方の向きの距離の大きい方）。"""
    co = np.asarray(comps_oriented, dtype=np.float64)
    center = float(np.median(co))
    tr = C.top_rank(float(e_row) - center, co - center)
    d_row = abs(float(e_row) - center)
    pv = np.array([max(abs(a - center), abs(b - center)) for a, b in comps_pairs], dtype=np.float64)
    return {'center': center, 'top': tr['top'], 'rank_oriented': tr['rank'], 'of_oriented': tr['of'],
            'rank_pair': int(1 + np.sum(pv >= d_row)), 'of_pair': int(len(pv) + 1), 'distance': d_row}


def iso_top_share(iso_effects, center, comps_oriented):
    """等方の最上位の割合（正本 `labels.second.iso_top_share`）: 等方の方向のうち、同じ中心と同じ比べる相手で最上位の条件を満たす割合。"""
    iso = np.asarray(iso_effects, dtype=np.float64)
    dmax = float(np.max(np.abs(np.asarray(comps_oriented, dtype=np.float64) - center)))
    return float(np.mean(np.abs(iso - center) > dmax))


def comparators_for(direction, pair_names, swap_siblings):
    """比べる相手の対（正本 `nulls.real.rule`）: v̂ と (6b) は入れ替えの対（自分と兄弟）を除き、Nk と td は自分の対だけを除く。"""
    own = {'Nk': 'Nk~N', 'td': 'Onull~N'}
    if direction in ('static', 'loaded'):
        drop = set(swap_siblings)
    elif direction in own:
        drop = {own[direction]}
    else:
        raise ValueError('比べる相手を決められない方向: %s' % direction)
    missing = drop - set(pair_names)
    if missing:
        raise ValueError('除く対が対の名の並びに無い: %s' % sorted(missing))
    return [p for p in pair_names if p not in drop]


def blens_own_pair():
    """B-lens の凍結の器 `tools/blens_lens.py` の `OWN_PAIR`（方向ごとの自分の対）を、import せずに文から読む（二つの道の外の凍結物を錨にする・裁定 D231）。"""
    import ast
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blens_lens.py'), encoding='utf-8').read()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == 'OWN_PAIR' for t in n.targets):
            return ast.literal_eval(n.value)
    raise ValueError('blens_lens.py に OWN_PAIR が無い')


def comparator_anchor(pair_names, swap_siblings, own_pair):
    """比べる相手の除き方の錨（裁定 D231）: `comparators_for` の除く対が、v̂ と (6b) では正本の兄弟の対（自分の対を含む）、Nk と td では B-lens の自分の対だけであること。
    戻り値: 方向ごとの除いた対の並び。違えば ValueError。"""
    out = {}
    for d in ('static', 'loaded', 'Nk', 'td'):
        dropped = sorted(set(pair_names) - set(comparators_for(d, pair_names, swap_siblings)))
        want = sorted(swap_siblings) if d in ('static', 'loaded') else [own_pair[d]]
        if dropped != want or (d in ('static', 'loaded') and own_pair[d] not in swap_siblings):
            raise ValueError('比べる相手の除き方が錨と違う: %s %s（錨 %s）' % (d, dropped, want))
        out[d] = dropped
    return out


# ---------------- 門 ----------------
def behavior_y(k, n, k0, n0, cc):
    return C.logit_cc(k, n, cc) - C.logit_cc(k0, n0, cc)


def gate(rows, unit_effects, units, alpha, drop_cells=()):
    """門（正本 `gate`）。rows: [{'unit','cell','fam','y'}]（fam は「升目|符号」）・unit_effects: 単位 → {fam: 効き目}。
    外した升目（drop_cells）の行を除き、行の無くなった単位を入れ替えから外す（入れ替えの数は残った単位の数の階乗）。符号はすべて +1 で呼ぶ（二重に掛けない）。
    行が残らなければ判定不能。通るのは p が水準を下回るとき。"""
    rs = [dict(r, sign=1) for r in rows if r['cell'] not in set(drop_cells)]
    us = [u for u in units if any(r['unit'] == u for r in rs)]
    if not rs or len(us) < 2:
        return {'undetermined': True, 'n_rows': len(rs), 'units': us}
    g = C.gate_perm(rs, unit_effects, us)
    g.update({'undetermined': False, 'units': us, 'pass': bool(g['p'] < alpha), 'alpha': alpha})
    return g


# ---------------- 下見の機械の決定 ----------------
def vi_decision(spread_a, spread_b, noise_max, batch_default):
    """(vi) の決め（正本 `pilot.checks.vi`）: (b) が上限を超えたら止める。(a) が上限を超えたらバッチ一。揺れの床は本の計算のバッチの組み方に合わせる。"""
    if spread_b > noise_max:
        return {'stop': True, 'reason': 'vi_b', 'spread_a': spread_a, 'spread_b': spread_b}
    batch = 1 if spread_a > noise_max else int(batch_default)
    return {'stop': False, 'batch': batch, 'floor': float(spread_b if batch == 1 else spread_a), 'spread_a': spread_a, 'spread_b': spread_b}


def cache_tol(floor, factor, lower, cap):
    """近道の許容（正本 `pilot.cache_tol_rule`）＝ 揺れの床の倍率倍と下限の大きい方を、上限で頭打ちにした値。"""
    return float(min(max(factor * floor, lower), cap))


def spread(values):
    v = np.asarray(values, dtype=np.float64)
    return float(np.max(v) - np.min(v))


def cells_decision(pass_main, pass_gate_only, cells_min_pass):
    """(i)(ii) の升目の決め（正本 `pilot.decision`）: 満たす主の升目が最小の数に満たなければ止める。満たさない升目は外す。"""
    n_pass = sum(1 for v in pass_main.values() if v)
    dropped = sorted(c for c, v in pass_main.items() if not v) + sorted(c for c, v in pass_gate_only.items() if not v)
    if n_pass < cells_min_pass:
        q1 = '止める'
    elif n_pass == len(pass_main):
        q1 = '続ける'
    else:
        q1 = '一部の升目を外して続ける'
    return {'q1': q1, 'n_pass': n_pass, 'n_main': len(pass_main), 'dropped': dropped, 'stop': q1 == '止める', 'reason': 'i_ii' if q1 == '止める' else None}


def pass_i_ii(mass, p_a, mass_min, p_bounds):
    return bool(mass >= mass_min and p_bounds[0] <= p_a <= p_bounds[1])


def iii_sentence(rho):
    """(iii) の文の選び方（正本 `pilot.checks.iii`）: 相関が正なら positive・零か負なら not_positive・定まらなければ undefined。"""
    if rho is None or (isinstance(rho, float) and math.isnan(rho)):
        return 'undefined'
    return 'positive' if rho > 0 else 'not_positive'


def variant_flags(lo_main, lo_variant, flag):
    return {c: bool(abs(lo_variant[c] - lo_main[c]) > flag) for c in lo_main}


def shortcut_ok(diffs, tol):
    """(v) と本の計算の頭の近道の確かめ: 差の絶対値がすべて許容の内なら近道を使う。"""
    return bool(max(abs(float(x)) for x in diffs) <= tol)


def q1_from_attempts(attempts):
    """下見のやり直しの流れ（正本 `pilot.decision.tool_error`）。attempts: 下見の試みの並び [{'decision': {...}} か {'tool_error': 文}]（登録者の裁定でやり直した順）。
    q1 はやり直した下見（最後の試み）で採点し、一度目の決定（出たとき）を併記する。最後の試みが器の誤りで終わったら（やり直さないと決めたとき）、q1 は採点しない。"""
    if not attempts:
        raise ValueError('下見の試みが無い')
    last, first = attempts[-1], attempts[0]
    first_dec = (first.get('decision') or {}).get('q1')
    if 'tool_error' in last:
        return {'scored': False, 'q1': None, 'first_decision': first_dec, 'n_attempts': len(attempts), 'closed': '器の誤りで下見を終えられなかった'}
    return {'scored': True, 'q1': last['decision']['q1'], 'first_decision': first_dec if len(attempts) > 1 else None, 'n_attempts': len(attempts)}


# ---------------- 独立の再計算の一致 ----------------
def agreement(eff_a, eff_b, tol, labels_a, labels_b):
    """段ごとの一致（正本 `independent_recompute.agreement`）: 全ての効き目の差の絶対値が許容の内で、二つの道の値からそれぞれ出した札が同じ。
    有限でない値が一つでもあれば一致しない（鍵の順に依らない・`non_finite` に鍵を並べる・裁定 D236）。"""
    keys = sorted(eff_a)
    if sorted(eff_b) != keys:
        return {'agree': False, 'reason': 'keys', 'values_within_tol': False, 'labels_same': False, 'max_abs_diff': None,
                'missing': sorted(set(eff_a) ^ set(eff_b))}
    finite = lambda v: bool(np.all(np.isfinite(np.asarray(v, dtype=np.float64))))
    nf = [k for k in keys if not (finite(eff_a[k]) and finite(eff_b[k]))]
    if nf:
        return {'agree': False, 'reason': 'non_finite', 'values_within_tol': False, 'labels_same': False, 'max_abs_diff': None, 'non_finite': nf}
    dmax = max(float(np.max(np.abs(np.asarray(eff_a[k], dtype=np.float64) - np.asarray(eff_b[k], dtype=np.float64)))) for k in keys)
    same = labels_a == labels_b
    return {'agree': bool(dmax <= tol and same), 'values_within_tol': bool(dmax <= tol), 'labels_same': bool(same), 'max_abs_diff': dmax}


# ---------------- 予想の採点 ----------------
def bucket(n, options):
    """零／一から三／四以上・零／一か二／三以上。"""
    if options == ['零', '一から三', '四以上']:
        return '零' if n == 0 else ('一から三' if n <= 3 else '四以上')
    if options == ['零', '一か二', '三以上']:
        return '零' if n == 0 else ('一か二' if n <= 2 else '三以上')
    raise ValueError('選択肢の形が決まっていない: %s' % options)


def score_q7(rows, floor):
    """q7（正本 `predictions.q7_rule`）。rows: 等方の外の v̂ の行 [{'effect','stage_b_diff','contains_zero'}]。
    区間が零を含む行と、効き目の絶対値が揺れの床以下の行は数えない。数えられる行が残らなければ採点しない（None）。"""
    use = [r for r in rows if not r['contains_zero'] and abs(r['effect']) > floor]
    if not use:
        return None
    same = [np.sign(r['effect']) == np.sign(r['stage_b_diff']) for r in use]
    return 'すべて同じ' if all(same) else ('すべて逆' if not any(same) else '混ざる')


# ---------------- 独立の再計算の組 ----------------
def recompute_set(main_rows, pair_names, swap_siblings, n_iso, dropped_cells=()):
    """独立の再計算で流す組（正本 `independent_recompute.what`）: v̂ の行ごとに、無操作・v̂・等方の帰無のすべて・比べる相手のすべて（両方の向き）。
    下見で外した升目の行は除く。戻り値: rows [(行の名, 升目の鍵, 符号)]・dirs_by_row {行の名: [(方向の名, 符号)]}。"""
    rows, dirs_by_row = [], collections.OrderedDict()
    comps = comparators_for('static', pair_names, swap_siblings)
    for r in main_rows:
        cell = '%s|%s' % (r['scenario'], r['base'])
        if r['direction'] != 'static' or cell in set(dropped_cells):
            continue
        s = int(r['sign'])
        rows.append((r['id'], cell, s))
        dirs_by_row[r['id']] = [('static', s)] + [('iso:%d' % i, s) for i in range(n_iso)] + [('real:' + p, s) for p in comps] + [('real:' + p, -s) for p in comps]
    return rows, dirs_by_row


# ---------------- バッチの組み方 ----------------
def batch_plan(dir_ids, batch, seed, key):
    """升目と符号ごとのバッチ（正本 `readout.primary.batching`）。方向の並びを種（`order_seed`）と升目と符号の番号（key）で混ぜ、零のベクトルの無操作を一つ入れ、
    最後のバッチの端数を零のベクトル（PAD・値は使わない）で埋める。戻り値: バッチの並び（各バッチは方向の名の並び・長さはすべて batch）。"""
    ids = list(dir_ids) + [NOOP]
    if len(set(ids)) != len(ids):
        raise ValueError('方向の名が重なる')
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(key)]))
    order = [ids[i] for i in rng.permutation(len(ids))]
    n_b = -(-len(order) // batch)
    order = order + [PAD] * (n_b * batch - len(order))
    return [order[i * batch:(i + 1) * batch] for i in range(n_b)]


def ledger_chain_bad(base, now, deviations, paths=None):
    """凍結物の SHA16 の違いを、逸脱の台帳の器の差分（`tool_diffs` の path・before・after）で許すかを照らす（裁定 D239・器の直しの確かめ C1-新6・C2-11）。
    路ごとに台帳の差分を記した順に並べ、凍結の値（base）から今の値（now）まで前後がつながるときだけ許す（同じファイルを二度直しても通る）。
    deviations には base を決めた後に記した台帳の行だけを与える。paths を与えると、その路だけを照らす（ほかの路の差分は見ない）。
    外れ: 台帳に差分が無いのに値が違う・差分の前後がつながらない・最後の差分と今の値が違う・差分を記したのに今の値が凍結の値と同じ・台帳に記した路が凍結物に無い。"""
    chains = collections.OrderedDict()
    for d in deviations or []:
        for td in d.get('tool_diffs') or []:
            chains.setdefault(td.get('path'), []).append(td)
    check = list(base) if paths is None else list(paths)
    bad = []
    for pth in sorted(set(check) | (set(chains) if paths is None else set(chains) & set(check))):
        want, got, ch = base.get(pth), now.get(pth), chains.get(pth, [])
        if pth not in base:
            bad.append('%s（凍結物に無い%s）' % (pth, '・台帳に記した' if ch else ''))
        elif not ch:
            if got != want:
                bad.append('%s（凍結 %s・今 %s・台帳に差分が無い）' % (pth, want, got))
        elif not all(ch[i].get('before') == (want if i == 0 else ch[i - 1].get('after')) for i in range(len(ch))):
            bad.append('%s（台帳の差分の前後がつながらない）' % pth)
        elif ch[-1].get('after') != got:
            bad.append('%s（台帳の最後の差分 %s と今 %s が違う）' % (pth, ch[-1].get('after'), got))
        elif got == want:
            bad.append('%s（台帳に差分を記したが、今の値が凍結の値と同じ）' % pth)
    return bad


# ---------------- 自己検査 ----------------
def _selftest():
    rng = np.random.default_rng(0)
    # 読み取りの量: 手で計算した値と合う・全語彙の正規化が打ち消し合う
    Z = np.array([[2.0, 0.5, -1.0, 0.0]])
    want = 2.0 - math.log(math.exp(0.5) + math.exp(-1.0) + math.exp(0.0))
    assert abs(log_odds_a(Z, 0, [1, 2, 3])[0] - want) < 1e-12
    assert abs(log_odds_a(Z + 7.0, 0, [1, 2, 3])[0] - want) < 1e-12
    pa = prob_a_in_set(Z, 0, [0, 1, 2, 3])[0]
    assert abs(math.log(pa / (1 - pa)) - want) < 1e-12
    Zf = rng.normal(size=(3, 50))
    ms = mass_of_set(Zf, [1, 5, 7])
    ref = np.exp(Zf[:, [1, 5, 7]]).sum(1) / np.exp(Zf).sum(1)
    assert np.allclose(ms, ref)
    # 割合と裾
    null = np.arange(-10, 11, dtype=float)
    r = p_and_tail(9.5, null)
    assert r['upper'] == 1 and r['lower'] == 20 and r['tail'] == 'upper' and abs(r['p'] - 2 * 2 / 22) < 1e-12
    assert p_and_tail(0.0, null)['tail'] == 'tie'
    # Holm の段の上限（二巡目の確かめ K456 の値の形）
    lim = holm_limits(1999, 0.05, 16)
    assert lim[:4] == [2, 2, 2, 2] and lim[-1] == 48, lim
    # 効き目の側
    nul = rng.normal(loc=3.0, scale=0.5, size=999)
    assert effect_side(5.0, nul)['side'] == 'stronger' and effect_side(1.0, nul)['side'] == 'weaker' and effect_side(-1.0, nul)['side'] == 'opposite'
    assert effect_side(0.0, nul)['side'] == 'weaker'
    nz = rng.normal(loc=0.1, scale=1.0, size=999)
    s = effect_side(-2.0, nz)
    assert s['side'] == 'sign_only' and s['sign'] == -1
    # 二つ目の札: 中心を引く・同じ値は上回らない・対の単位の順位
    comps = np.array([1.0, 1.2, 0.8, 1.1, 0.9, 1.05])
    pairs = [(1.0, 1.2), (0.8, 1.1), (0.9, 1.05)]
    sl = second_label(2.0, comps, pairs)
    assert sl['top'] and sl['rank_oriented'] == 1 and sl['rank_pair'] == 1 and abs(sl['center'] - float(np.median(comps))) < 1e-12
    edge = float(np.median(comps)) + float(np.max(np.abs(comps - np.median(comps))))
    assert not second_label(edge, comps, pairs)['top']
    assert not second_label(1.0, comps, pairs)['top']
    assert abs(iso_top_share(np.array([0.0, 5.0, 1.0]), float(np.median(comps)), comps) - 2 / 3) < 1e-12
    names = ['O~Osec', 'O~Onull', 'Nk~N', 'Onull~N', 'O~Osec-Ncold', 'Osec~O-Ncold', 'O-Ncold~Osec-Ncold']
    sw = ['O~Osec', 'O~Osec-Ncold', 'Osec~O-Ncold', 'O-Ncold~Osec-Ncold']
    assert comparators_for('static', names, sw) == ['O~Onull', 'Nk~N', 'Onull~N']
    assert comparators_for('Nk', names, sw) == [n for n in names if n != 'Nk~N']
    # 門: 奇でない押し・減算の行・外した升目と行の無くなった単位
    units = ['A', 'B', 'C', 'D']
    fams = ['S1|X|+', 'S1|X|-']
    eff = {u: {f: float(i) + (0.3 if f.endswith('-') else 0.0) for f in fams} for i, u in enumerate(units)}
    rows = [{'unit': u, 'cell': 'S1|X', 'fam': f, 'y': eff[u][f] * 2} for u in units for f in fams]
    g = gate(rows, eff, units, 0.05)
    assert g['n_perm'] == 24 and g['rho'] > 0.9
    rows2 = rows + [{'unit': 'E', 'cell': 'S4|Y', 'fam': 'S4|Y|+', 'y': 0.0}]
    eff2 = dict(eff, E={'S4|Y|+': 0.0, 'S1|X|+': 0.0, 'S1|X|-': 0.0})
    for u in units:
        eff2[u] = dict(eff2[u], **{'S4|Y|+': 0.0})
    g2 = gate(rows2, eff2, units + ['E'], 0.05, drop_cells=['S4|Y'])
    assert g2['units'] == units and g2['n_perm'] == 24, g2
    assert gate(rows, eff, units, 0.05, drop_cells=['S1|X'])['undetermined']
    # 下見の決め
    assert vi_decision(0.001, 0.02, 0.01, 16)['stop']
    d = vi_decision(0.02, 0.003, 0.01, 16)
    assert not d['stop'] and d['batch'] == 1 and d['floor'] == 0.003
    d = vi_decision(0.004, 0.0, 0.01, 16)
    assert d['batch'] == 16 and d['floor'] == 0.004
    assert cache_tol(0.0, 2, 0.005, 0.01) == 0.005 and cache_tol(0.004, 2, 0.005, 0.01) == 0.008 and cache_tol(0.009, 2, 0.005, 0.01) == 0.01
    pm = {'c%d' % i: True for i in range(8)}
    assert cells_decision(pm, {}, 6)['q1'] == '続ける'
    pm['c0'] = pm['c1'] = False
    cd = cells_decision(pm, {'g0': False}, 6)
    assert cd['q1'] == '一部の升目を外して続ける' and cd['dropped'] == ['c0', 'c1', 'g0']
    pm['c2'] = False
    assert cells_decision(pm, {}, 6)['q1'] == '止める'
    assert pass_i_ii(0.95, 0.5, 0.9, [0.0001, 0.9999]) and not pass_i_ii(0.85, 0.5, 0.9, [0.0001, 0.9999]) and not pass_i_ii(0.95, 0.99995, 0.9, [0.0001, 0.9999])
    assert iii_sentence(0.3) == 'positive' and iii_sentence(0.0) == 'not_positive' and iii_sentence(float('nan')) == 'undefined'
    assert shortcut_ok([0.001, -0.004], 0.005) and not shortcut_ok([0.006], 0.005)
    # 下見のやり直しの流れ: やり直した下見で採点し、一度目の決定を併記する・やり直さずに閉じたら採点しない
    r_ = q1_from_attempts([{'tool_error': 'x'}, {'decision': {'q1': '続ける'}}])
    assert r_['scored'] and r_['q1'] == '続ける' and r_['first_decision'] is None and r_['n_attempts'] == 2
    assert q1_from_attempts([{'decision': {'q1': '止める'}}, {'decision': {'q1': '続ける'}}])['first_decision'] == '止める'
    assert not q1_from_attempts([{'tool_error': 'x'}])['scored']
    # 再計算の一致: 値の許容と札の両方
    a_ = {'r': [0.1, 0.2]}
    assert agreement(a_, {'r': [0.1005, 0.2]}, 0.001, {'x': 1}, {'x': 1})['agree']
    assert not agreement(a_, {'r': [0.1005, 0.2]}, 0.0001, {'x': 1}, {'x': 1})['agree']
    assert not agreement(a_, a_, 0.001, {'x': 1}, {'x': 2})['agree']
    # 有限でない値（裁定 D236）: 割合と裾は止まり、一致の関数は鍵の順に依らず一致しない
    for bad_ in (float('nan'), float('inf')):
        try:
            p_and_tail(bad_, null)
            raise AssertionError('有限でない値の割合を通した')
        except ValueError:
            pass
    for order_ in (('a', 'b'), ('b', 'a')):
        ea = {order_[0]: [0.0], order_[1]: [float('nan')]}
        nf_ = agreement(ea, {'a': [0.0], 'b': [0.0]}, 0.001, {}, {})
        assert not nf_['agree'] and nf_['reason'] == 'non_finite' and nf_['non_finite'] == [order_[1]], nf_
    # 予想の採点
    assert bucket(0, ['零', '一から三', '四以上']) == '零' and bucket(3, ['零', '一から三', '四以上']) == '一から三' and bucket(4, ['零', '一から三', '四以上']) == '四以上'
    assert bucket(2, ['零', '一か二', '三以上']) == '一か二' and bucket(3, ['零', '一か二', '三以上']) == '三以上'
    q7rows = [{'effect': 0.5, 'stage_b_diff': 17.0, 'contains_zero': False}, {'effect': -0.4, 'stage_b_diff': -11.0, 'contains_zero': False},
              {'effect': 0.3, 'stage_b_diff': -2.0, 'contains_zero': True}]
    assert score_q7(q7rows, 0.0) == 'すべて同じ' and score_q7(q7rows[2:], 0.0) is None and score_q7(q7rows[:1], 0.6) is None
    assert score_q7([{'effect': -0.5, 'stage_b_diff': 17.0, 'contains_zero': False}], 0.0) == 'すべて逆'
    # バッチの組み方: 端数を零のベクトルで埋め、全ての方向と無操作が一度ずつ入り、種で決まる
    ids = ['d%d' % i for i in range(2034)]
    bp = batch_plan(ids, 16, 91002, 0)
    flat = [x for b in bp for x in b]
    assert len(bp) == 128 and all(len(b) == 16 for b in bp) and flat.count(PAD) == 13 and flat.count(NOOP) == 1
    assert sorted(x for x in flat if x not in (PAD, NOOP)) == sorted(ids)
    assert batch_plan(ids, 16, 91002, 0) == bp and batch_plan(ids, 16, 91002, 1) != bp
    assert flat.index(PAD) >= len(flat) - 13
    # 逸脱の台帳の器の差分の照らし（裁定 D239）
    bs = {'a': '1', 'b': '2'}
    dv = lambda *tds: [{'no': 'x', 'tool_diffs': [{'path': p_, 'before': b_, 'after': a_} for p_, b_, a_ in tds]}]
    assert ledger_chain_bad(bs, dict(bs), []) == []
    assert ledger_chain_bad(bs, {'a': '3', 'b': '2'}, []) and ledger_chain_bad(bs, {'a': '3', 'b': '2'}, dv(('a', '1', '3'))) == []
    assert ledger_chain_bad(bs, {'a': '4', 'b': '2'}, dv(('a', '1', '3')) + dv(('a', '3', '4'))) == []            # 同じファイルを二度直す
    assert ledger_chain_bad(bs, {'a': '4', 'b': '2'}, dv(('a', '1', '3')) + dv(('a', '5', '4')))                    # 前後がつながらない
    assert ledger_chain_bad(bs, {'a': '9', 'b': '2'}, dv(('a', '1', '3')))                                         # 最後の差分と今が違う
    assert ledger_chain_bad(bs, dict(bs), dv(('a', '1', '1')))                                                      # 記したのに今が凍結の値と同じ
    assert ledger_chain_bad(bs, dict(bs), dv(('c', '0', '1')))                                                      # 凍結物に無い路
    assert ledger_chain_bad(bs, {'a': '3', 'b': '2'}, dv(('a', '1', '3')), paths=['b']) == []                        # 与えた路だけを照らす
    assert ledger_chain_bad(bs, {'a': '1', 'b': None}, [], paths=['b'])                                              # 無いファイル
    print('[bl3_core] 自己検査 OK（%s）' % VERSION)


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest()
    else:
        print(__doc__)
