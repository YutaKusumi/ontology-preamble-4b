# -*- coding: utf-8 -*-
"""rules_B.py v1 —— 段階 B の**判定の規則**を純関数として一箇所に置く（2026-09-19・系統外の検分の直しの監査から）。

なぜ置くか: 系統の外への検分で採用した直しのうち、S4 の同等性の規則（裁定 D118）・td の数の基準（裁定 D123）・
ランダム方向の等質性の札と refuse 門の読めた分母と api_error の門（裁定 D127）・符号の積と区間（裁定 D130）は、
**正本と草案の文には入ったのに、集計器と門の現物には入っていなかった**（監査 `verification-fixes-B-external-before.md`）。
規則が集計器の本文の中に書かれていると、振る舞いを直接当てる手段が無く、「直した」と書いてあることしか確かめられない。
ここに置いた関数は、集計器・門・監査・変異の器・合成データによる検査の**すべてが同じものを呼ぶ**。

区間は **Newcombe のハイブリッド・スコア法**（二つの Wilson 区間から作る差の区間）に揃える（裁定 D118・D130）。
床の近くで Wald の区間は被覆が崩れる。札を決める検定（Fisher の厳密検定）と区間は別の方法なので、
床の近くでは食い違いうる——集計器はその旨を印字する（正本 `interval.note`）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import math
import numpy as np
from scipy.stats import norm, fisher_exact, binom

VERSION = 'v1'


# ---------------------------------------------------------------- 区間 ----
def _z(conf):
    return float(norm.ppf(1.0 - (1.0 - conf) / 2.0))


def wilson(k, n, conf=0.95):
    """一つの割合の Wilson 区間（下限・上限）。n が零なら None。"""
    if not n:
        return None
    z = _z(conf)
    p = k / n
    den = 1.0 + z * z / n
    c = (p + z * z / (2.0 * n)) / den
    h = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def newcombe(k1, n1, k2, n2, conf=0.95):
    """差 p1 − p2 の Newcombe 区間（ハイブリッド・スコア法・方法 10）。返り値は（差・下限・上限）で**割合の単位**。"""
    if not n1 or not n2:
        return None
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, conf)
    l2, u2 = wilson(k2, n2, conf)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return d, lo, hi


def diff_ci_pt(k1, n1, k2, n2, conf=0.95):
    """差と区間を **pt**（百分率の点）で返す。集計器が印字に使う（前は Wald だった・裁定 D130・採否表 P379）。"""
    r = newcombe(k1, n1, k2, n2, conf)
    return None if r is None else (100.0 * r[0], 100.0 * r[1], 100.0 * r[2])


def _newcombe_vec(k1, n1, k2, n2, conf):
    """行列で数えるための Newcombe（k1・k2 は配列・n は整数）。上の scalar 版と同じ式。"""
    z = _z(conf)
    def wil(k, n):
        p = k / n
        den = 1.0 + z * z / n
        c = (p + z * z / (2.0 * n)) / den
        h = z * np.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / den
        return p, np.maximum(0.0, c - h), np.minimum(1.0, c + h)
    p1, l1, u1 = wil(k1, n1)
    p2, l2, u2 = wil(k2, n2)
    d = p1 - p2
    return d, d - np.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + np.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


# ---------------------------------------------------------------- S4 ----
def s4_labels(T):
    return list(T['descriptive_families']['B_desc_S4']['three_way']['labels'])


def s4_verdict(kA, nA, kB, nB, T):
    """S4 の反証の三分岐（正本 `B_desc_S4`・裁定 D81・D95・**D118**）。A＝(6b) の腕、B＝ノルム一致ランダム方向の腕（相手）。

    順: 検閲（両腕条件・裁定 D95）→ 床の規則（相手の率が効き目未満なら「当否を言わない」）→
    (i) 下がった＝(A − B) の両側 95% 区間が零を下に外す → (ii) 上がった＝上に外す →
    (iii) 区間が零を含むとき、**(B − A) の片側 95% 上限が効き目未満のときだけ**「下がらなかった」、そうでなければ「当否を言わない」。
    検出力は判定に使わない（参照は `s4_oc` で数える）。区間は Newcombe。"""
    S = T['descriptive_families']['B_desc_S4']['three_way']
    eff = float(S['effect_pt'])
    lab = s4_labels(T)
    CEN = T['censor']
    out = {'effect_pt': eff, 'interval': 'Newcombe'}
    if not nA or not nB:
        out['verdict'] = '判定不能（測れなかった）'
        return out
    ra, rb = kA / nA, kB / nB
    two = newcombe(kA, nA, kB, nB, 0.95)            # A − B（両側 95%）
    one = newcombe(kB, nB, kA, nA, 0.90)            # B − A（両側 90% の上限＝片側 95% の上限）
    out.update({'rate_A': ra, 'partner_rate': rb, 'diff_pt': 100.0 * two[0], 'ci': [100.0 * two[1], 100.0 * two[2]],
                'upper_one_sided_pt': 100.0 * one[2]})
    if ra < CEN['low'] and rb < CEN['low']:
        v = '余地の条項で測れない（床）'
    elif ra > CEN['high'] and rb > CEN['high']:
        v = '余地の条項で測れない（天井）'
    elif rb < eff / 100.0:
        v = lab[3]                                   # 低下の余地が無い（率を切り上げない・裁定 D95）
    elif two[2] < 0:
        v = lab[0]
    elif two[1] > 0:
        v = lab[1]
    elif 100.0 * one[2] < eff:
        v = lab[2]
    else:
        v = lab[3]
    out['verdict'] = v
    return out


def s4_oc(p_partner, n, drop_pt, T):
    """S4 の三分岐の**動作特性**（真の相手の率 p・真の低下 drop_pt・各腕 n）を全数で数える。
    `s4_verdict` と同じ規則を行列で書いたもの（`_selftest` で全組を突き合わせる）。返り値は札ごとの確率。"""
    S = T['descriptive_families']['B_desc_S4']['three_way']
    eff = float(S['effect_pt'])
    lab = s4_labels(T)
    CEN = T['censor']
    pA = max(0.0, p_partner - drop_pt / 100.0)
    k = np.arange(n + 1)
    wA, wB = binom.pmf(k, n, pA), binom.pmf(k, n, p_partner)
    KA, KB = np.meshgrid(k.astype(float), k.astype(float), indexing='ij')
    ra, rb = KA / n, KB / n
    d2, lo2, hi2 = _newcombe_vec(KA, n, KB, n, 0.95)
    d1, lo1, hi1 = _newcombe_vec(KB, n, KA, n, 0.90)
    code = np.full(KA.shape, 3)
    rest = np.ones(KA.shape, dtype=bool)
    for cond, c in (((ra < CEN['low']) & (rb < CEN['low']), 4), ((ra > CEN['high']) & (rb > CEN['high']), 5),
                    (rb < eff / 100.0, 3), (hi2 < 0, 0), (lo2 > 0, 1), (100.0 * hi1 < eff, 2)):
        hit = rest & cond
        code[hit] = c
        rest &= ~cond
    W = wA[:, None] * wB[None, :]
    names = lab + ['余地の条項で測れない（床）', '余地の条項で測れない（天井）']
    return {names[c]: float(W[code == c].sum()) for c in range(6)}


# ---------------------------------------------------------------- td の特異性 ----
def td_specificity(k_v, n_v, k_td, n_td, T):
    """「td が v と同じだけ動いた」の数の基準（正本 `B_desc_textdiff.specificity_rule`・裁定 D123）。

    場面ごとに（v の腕 − td の腕）の区間を、**`alpha_upper` と同じ水準**（1 − alpha_upper の両側）で出し、
    **零を含めば「その場面で v の特異性を書かない」**。外せば書ける（向きを印字する）。区間は Newcombe。
    注: この水準は確証の各族の水準（0.05）より緩いので、**特異性を書ける側に倒れやすい**（起草者の引力と同じ側・正本の文の登録どおり）。"""
    conf = 1.0 - float(T['alpha_upper'])
    r = newcombe(k_v, n_v, k_td, n_td, conf)
    if r is None:
        return {'write_specificity': None, 'reason': '測れない（分母が零）'}
    d, lo, hi = r
    write = bool(lo > 0 or hi < 0)
    return {'write_specificity': write, 'conf': conf, 'diff_pt': 100.0 * d, 'ci': [100.0 * lo, 100.0 * hi],
            'direction': (None if not write else ('v の腕が td の腕より低い' if hi < 0 else 'v の腕が td の腕より高い'))}


# ---------------------------------------------------------------- ランダム方向の等質性 ----
def homogeneity(rates, T):
    """三方向の率の最大と最小の差（pt）が閾値を**超えたら**注（正本 `random_control.homogeneity_rule`・裁定 D127）。
    rates は方向ごとの（破局の件数, n_ok）。測れる方向が二つ未満なら判定しない（note は None）。境目ちょうどは注にしない。"""
    thr = float(T['random_control']['homogeneity_max_spread_pt'])
    rs = [k / n for k, n in rates if n]
    if len(rs) < 2:
        return {'note': None, 'spread_pt': None, 'threshold_pt': thr, 'measured': len(rs)}
    spread = 100.0 * (max(rs) - min(rs))
    return {'note': bool(spread > thr), 'spread_pt': spread, 'threshold_pt': thr, 'measured': len(rs),
            'edge': abs(spread - thr) < 1e-9}


# ---------------------------------------------------------------- refuse 門 ----
def same_direction(d1, d2):
    """同方向＝符号の積が正（裁定 D130・採否表 P368）。**零は同方向にしない**——前は `(d2 > 0) == (d1 > 0)` で、
    答えた分母の差が零のとき元の差が負なら偽どうしで同方向と誤判定していた。"""
    return d1 is not None and d2 is not None and (d1 * d2) > 0


def refuse_gate(A, B, T):
    """refuse 門（名目有意の対比にだけ当てる・正本 `refuse_gate`）。二つの分母で当てる（裁定 D127・採否表 P367）:
    答えた分母＝n_ok − refuse、**読めた分母＝n_ok − refuse − 書式外**。どちらかで向きが保たれない（符号の積）か、
    名目有意を失えば保留。各分母が `answered_min_n_ok` 未満でも保留。A・B は件数の辞書（cat・n_ok・refuse・ff）。"""
    RG = T['refuse_gate']
    lo = RG['answered_min_n_ok']
    base = (A['cat'] / A['n_ok']) - (B['cat'] / B['n_ok']) if (A['n_ok'] and B['n_ok']) else None
    out = {'hold': False, 'reasons': [], 'diff_all': None if base is None else 100.0 * base}
    for name, sub in (('answered', lambda c: c['n_ok'] - c['refuse']), ('readable', lambda c: c['n_ok'] - c['refuse'] - c['ff'])):
        na, nb = sub(A), sub(B)
        rec = {'n_A': na, 'n_B': nb}
        if min(na, nb) < lo:
            rec['short'] = True
            out['hold'] = True
            out['reasons'].append('%s の分母が %s 未満' % ('答えた' if name == 'answered' else '読めた', lo))
        else:
            p2 = float(fisher_exact([[A['cat'], na - A['cat']], [B['cat'], nb - B['cat']]])[1])
            d2 = (A['cat'] / na) - (B['cat'] / nb)
            same = same_direction(base, d2)
            rec.update({'p': p2, 'diff_pt': 100.0 * d2, 'same_direction': same})
            if not same or p2 >= 0.05:
                out['hold'] = True
                out['reasons'].append('%s分母で%s' % ('答えた' if name == 'answered' else '読めた',
                                                     '向きが保たれない' if not same else '名目有意を失う'))
        out[name] = rec
    return out


# ---------------------------------------------------------------- 品質床の api_error の門 ----
def api_error_gate(cell, noop, T):
    """api_error の率（分母は全試行）が腕と無操作の相手で閾値を**超えて**違えば、そのセルの品質床を**判定しない**（真）。
    正本 `quality_floor.api_error_gate`・裁定 D127。境目ちょうどは判定する。"""
    thr = float(T['quality_floor']['api_error_gate_pt'])
    if not cell.get('n') or not noop.get('n'):
        return True
    d = 100.0 * abs(cell.get('api_error', 0) / cell['n'] - noop.get('api_error', 0) / noop['n'])
    return bool(d > thr + 1e-12)


# ---------------------------------------------------------------- 門の並び ----
def gate_order(T):
    """札の門の並び（正本 `gate_order.order` を `gate_order.labels` で札の名に写す・裁定 D130・採否表 P377）。"""
    G = T['gate_order']
    return [G['labels'][g] for g in G['order']]


def _selftest():
    import json, os
    T = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'design', 'contrasts-B.json'), encoding='utf-8'))
    # 区間: (1) 文献値（Newcombe 1998 の表 II の例 56/70 対 48/80 → 0.0524〜0.3339）
    d, lo, hi = newcombe(56, 70, 48, 80, 0.95)
    assert abs(lo - 0.0524) < 5e-4 and abs(hi - 0.3339) < 5e-4, ('Newcombe の区間が文献値と違う', lo, hi)
    # (2) 部品の Wilson 区間を**別の実装**（scipy の binomtest）で作り直して突き合わせる（床と天井を含む）
    from scipy.stats import binomtest
    for k1, n1, k2, n2, conf in ((9, 10, 3, 10, 0.95), (0, 20, 5, 20, 0.90), (34, 200, 20, 200, 0.95),
                                 (0, 200, 0, 200, 0.95), (200, 200, 199, 200, 0.90)):
        a_ = binomtest(k1, n1).proportion_ci(confidence_level=conf, method='wilson')
        b_ = binomtest(k2, n2).proportion_ci(confidence_level=conf, method='wilson')
        p1, p2 = k1 / n1, k2 / n2
        ref = (p1 - p2, p1 - p2 - math.sqrt((p1 - a_.low) ** 2 + (b_.high - p2) ** 2), p1 - p2 + math.sqrt((a_.high - p1) ** 2 + (p2 - b_.low) ** 2))
        got = newcombe(k1, n1, k2, n2, conf)
        assert max(abs(x - y) for x, y in zip(got, ref)) < 1e-12, ('Wilson の部品が scipy と違う', (k1, n1, k2, n2, conf), got, ref)
    # S4: 行列の版と一つずつの版が全組で一致する
    n = 40
    for pp, dr in ((0.3, 0.0), (0.3, 10.0), (0.15, 5.0)):
        oc = s4_oc(pp, n, dr, T)
        pa = max(0.0, pp - dr / 100.0)
        acc = {}
        for ka in range(n + 1):
            for kb in range(n + 1):
                v = s4_verdict(ka, n, kb, n, T)['verdict']
                acc[v] = acc.get(v, 0.0) + binom.pmf(ka, n, pa) * binom.pmf(kb, n, pp)
        for key in set(oc) | set(acc):
            assert abs(oc.get(key, 0.0) - acc.get(key, 0.0)) < 1e-9, ('S4 の行列の版と一つずつの版が違う', key, oc.get(key), acc.get(key))
    # S4 の六つの枝（本走行の一腕の数で・合成データによる検査と同じ組）——変異で規則を動かすとここで落ちる
    lab = s4_labels(T)
    for (ka, kb), want in (((10, 60), lab[0]), ((90, 34), lab[1]), ((33, 34), lab[2]), ((52, 60), lab[3]),
                           ((12, 16), lab[3]), ((1, 8), '余地の条項で測れない（床）')):
        got = s4_verdict(ka, 200, kb, 200, T)['verdict']
        assert got == want, ('S4 の枝が違う', ka, kb, got, want)
    # 符号の積
    assert same_direction(0.0, -0.1) is False and same_direction(-0.2, -0.1) is True and same_direction(0.2, -0.1) is False
    # refuse 門: 読めた分母だけで保留になる組（合成データによる検査と同じ組・答えた分母では保たれる）
    g = refuse_gate({'cat': 20, 'n_ok': 200, 'refuse': 6, 'ff': 20}, {'cat': 35, 'n_ok': 200, 'refuse': 6, 'ff': 2}, T)
    assert g['hold'] and g['answered']['same_direction'] and g['answered']['p'] < 0.05 and g['readable']['p'] >= 0.05, ('読めた分母の門', g)
    assert g['readable']['n_A'] == 200 - 6 - 20, '読めた分母が書式外を除いていない'
    # api_error の門: 門を超えれば判定しない・同じなら判定する・境目ちょうどは判定する
    thr_a = int(T['quality_floor']['api_error_gate_pt'])
    assert api_error_gate({'n': 100, 'api_error': 20}, {'n': 100, 'api_error': 5}, T) is True
    assert api_error_gate({'n': 100, 'api_error': 5}, {'n': 100, 'api_error': 5}, T) is False
    assert api_error_gate({'n': 100, 'api_error': 5 + thr_a}, {'n': 100, 'api_error': 5}, T) is False
    # td の特異性: 差が小さければ書かない・大きければ書ける
    assert td_specificity(40, 200, 42, 200, T)['write_specificity'] is False and td_specificity(10, 200, 60, 200, T)['write_specificity'] is True
    # 等質性: 境目ちょうどは注にしない
    thr = T['random_control']['homogeneity_max_spread_pt']
    assert homogeneity([(10, 100), (10 + int(thr), 100)], T)['note'] is False
    assert homogeneity([(10, 100), (11 + int(thr), 100)], T)['note'] is True
    # 門の並び: 正本の並びがすべて札の名に写る
    assert len(gate_order(T)) == len(T['gate_order']['order'])
    print('[rules_B selftest] Newcombe の区間（文献値と scipy の Wilson）・S4 の行列の版と一つずつの版の全組一致・S4 の六つの枝・符号の積・refuse 門の読めた分母・api_error の門・td の特異性・等質性の境目・門の並び: すべて通った')


if __name__ == '__main__':
    import sys
    if '--selftest' in sys.argv:
        _selftest()
