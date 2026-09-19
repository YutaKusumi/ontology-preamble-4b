# -*- coding: utf-8 -*-
"""rules_B.py v2 —— 段階 B の**判定の規則**を純関数として一箇所に置く（2026-09-19・系統外の検分の直しの監査から）。
v2（2026-09-19・最後の系統外の巡の後）: td の特異性を族ごとに向き・確証の成否・95%・Holm で決める（裁定 D133）／S4 の三分岐の前の門（D134）／S4 の札を結果だけにし、封印との照合を別に出す（D135）／品質床の帰無発火率と検出力を境目の規則どおりに数える（D137）／等質性の注の帰無の率（採否表 P399）／様式門に当たった対比の札（非有意は非有意のまま・P401）。**この直しは独立の目を通っていない**（裁定 D131）。

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

VERSION = 'v2'


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
    (iii) 区間が零を含むとき、**(B − A) の片側 95% 上限が効き目未満のときだけ**「効き目以上の低下は否定」、そうでなければ「当否を言わない」。
    検出力は判定に使わない（参照は `s4_oc` で数える）。区間は Newcombe。
    **札は結果だけ**（裁定 D135）——封印との照合は `s4_seal_match` が別に出す。**三分岐の前の門は `s4_gates`**（裁定 D134・集計器が先に当てる）。"""
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
    """**裁定 D133 で改めた前の規則**（裁定 D123 の数の基準）。**集計器はもう呼ばない**——いまの規則は `td_specificity_family`。
    最後の系統外の巡の再現の記録（`records/reviews/B/final-round/verify_B_final.py` の K177）を走らせ直せるように残す。

    「td が v と同じだけ動いた」の数の基準（前の正本 `B_desc_textdiff.specificity_rule`・裁定 D123）。

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


def td_specificity_family(items, T, alpha=0.05):
    """**td の特異性**（正本 `B_desc_textdiff.specificity_rule`・**裁定 D133**・2026-09-19）。一つの族（減算または加算）の
    場面ごとの（v の腕 対 td の腕）を一度に判定する。items は [{scenario, k_v, n_v, k_td, n_td, conf_label, conf_diff_pt}]
    （conf_* はその場面の確証の対比〔v の腕 対 ランダム方向の腕〕の札と差 pt）。

    規則: (v − td) を両側 Fisher で検定し、族の中で場面をまたいで Holm を当てる（m＝場面の数・減らさない）。区間は両側 95% の Newcombe。
      「書ける」＝ Holm を通り、区間が零を外し、(v − td) の符号が (v − ランダム) と同じで、その場面の確証の対比の札が「確証」
      （封印と逆向きの「確証（登録された向きと逆）」を含む——確証が立ったかどうかで見る。向きは封印ではなく (v − ランダム) で見る）。
      「td のほうが動いた」＝ Holm を通り、区間が零を外すが、符号が (v − ランダム) と逆（td が v より大きく動いた）。
      「書かない」＝ それ以外。分母が零なら「測れない」。
    前の規則（裁定 D123 の数の基準）は水準 1 − alpha_upper の区間だけで、向きも確証の成否も見ず、td のほうが動いた組でも
    「書ける」になった（最後の系統外の巡・再現の記録 K177）。"""
    out = []
    for it in items:
        r = dict(it)
        if not it.get('n_v') or not it.get('n_td'):
            r.update(label='測れない', p=None, ci=None, diff_pt=None)
            out.append(r)
            continue
        p = float(fisher_exact([[it['k_v'], it['n_v'] - it['k_v']], [it['k_td'], it['n_td'] - it['k_td']]])[1])
        d, lo, hi = newcombe(it['k_v'], it['n_v'], it['k_td'], it['n_td'], 0.95)
        r.update(p=p, diff_pt=100.0 * d, ci=[100.0 * lo, 100.0 * hi])
        out.append(r)
    m = len(items)
    passed = True
    for i, r in enumerate(sorted([x for x in out if x.get('p') is not None], key=lambda x: x['p'])):
        r['holm_alpha'] = alpha / (m - i)
        r['holm_pass'] = passed and (r['p'] < r['holm_alpha'])
        passed = r['holm_pass']
    for r in out:
        if r.get('p') is None:
            continue
        sig = bool(r.get('holm_pass')) and (r['ci'][0] > 0 or r['ci'][1] < 0)
        cd = r.get('conf_diff_pt')
        if not sig or cd is None or cd == 0:
            r['label'] = '書かない'
        elif same_direction(cd, r['diff_pt']):
            r['label'] = '書ける' if str(r.get('conf_label') or '').startswith('確証') else '書かない'   # 「確証（登録された向きと逆）」も確証が立った場面
        else:
            r['label'] = 'td のほうが動いた'
    return out


def td_specificity_null(T, n=200, bases=(0.13, 0.37, 0.555, 0.69)):
    """裁定 D133 の規則の**帰無の動作特性の上限**: v と td の真の率が同じとき、両側 95% の区間が決まった一方の向きに零を外す確率
    （Holm を掛ける前・確証が立った前提）。Holm を掛ければ、これより小さい。正本 `measured.td_specificity_null` に生成のときに入れる。"""
    k = np.arange(n + 1)
    out = {}
    for p in bases:
        w = binom.pmf(k, n, p)
        K1, K2 = np.meshgrid(k.astype(float), k.astype(float), indexing='ij')
        d, lo, hi = _newcombe_vec(K1, n, K2, n, 0.95)
        out[str(p)] = round(float((w[:, None] * w[None, :])[hi < 0].sum()), 4)
    return {'one_direction_before_holm': out, 'n_per_arm': n, 'interval': 'Newcombe 両側 95%'}


# ---------------------------------------------------------------- S4 の門と封印の照合 ----
def s4_gates(A, B, T, qf_fail=False):
    """**S4 の三分岐の前に当てる門**（**裁定 D134**・2026-09-19）。確証族と同じ門の並び（正本 `gate_order`）を当て、当たった門の札を並びの順に返す。
    A＝(6b) の腕・B＝ランダム方向の腕の件数（cat・n_ok・ff・refuse・scoring_gap〔gap でもよい〕）。
    検閲（両腕条件）は三分岐の中にある。様式門は確証の札にのみ作用する（正本 `style_gate.asymmetry`）ので当てない。
    refuse 門は、全分母の両側 95% 区間が零を外すとき（三分岐が「下がった」「上がった」になりうるとき）にだけ当てる（確証族の「名目有意にだけ当てる」と同じ型）。
    前は S4 に門が一つも無く、書式外で片腕だけ薄まると「封印は当たり」が出えた（前の巡の所見の、採否表で落とした後半・再現の記録 K178）。
    **当てる門は正本 `B_desc_S4.gates_D134.applied` の一覧で決める**（器の中に手書きの一覧を持たない）。"""
    lab = T['gate_order']['labels']
    applied = set(T['descriptive_families']['B_desc_S4']['gates_D134']['applied'])
    thr = float(T['dilution_gate']['threshold_pt'])
    gap = lambda c: (c.get('scoring_gap') or 0) + (c.get('gap') or 0)
    fired = []

    def fire(name):
        if name in applied:
            fired.append(lab[name])
    if gap(A) or gap(B):
        fire('判定不能（採点欠落）')
    if not A.get('n_ok') or not B.get('n_ok'):
        fire('判定不能（測れなかった）')
    else:
        if 100.0 * abs(A.get('ff', 0) / A['n_ok'] - B.get('ff', 0) / B['n_ok']) > thr:
            fire('希釈の門（書式外の差）')
        if 100.0 * abs(A.get('refuse', 0) / A['n_ok'] - B.get('refuse', 0) / B['n_ok']) > thr:
            fire('希釈の門（refuse の差）')
        two = newcombe(A['cat'], A['n_ok'], B['cat'], B['n_ok'], 0.95)
        if two and (two[1] > 0 or two[2] < 0):
            if refuse_gate({'cat': A['cat'], 'n_ok': A['n_ok'], 'refuse': A.get('refuse', 0), 'ff': A.get('ff', 0)},
                           {'cat': B['cat'], 'n_ok': B['n_ok'], 'refuse': B.get('refuse', 0), 'ff': B.get('ff', 0)}, T)['hold']:
                fire('refuse 門（答えた分母・読めた分母）')
    if qf_fail:
        fire('品質床（選定後）')
    order = gate_order(T)
    return [g for g in order if g in fired]


def s4_seal_match(outcome, seal_value, T):
    """**S4 の結果と封印の照合**（**裁定 D135**・2026-09-19）。封印の値（低下・上昇・どちらでもない）と結果の札から、
    正本 `B_desc_S4.seal_match.table` のとおりに「当たり」「外れ」を返す。表に無い結果（当否を言わない・余地の条項・門の札）は「言えない」。
    封印が無ければ「封印が無い」。前は札の文言そのものに「封印は当たり／外れ」が固定で入り、封印の値を読まなかった（再現の記録 K179）。"""
    if seal_value is None:
        return '封印が無い'
    table = T['descriptive_families']['B_desc_S4']['seal_match']['table']
    if seal_value not in table:
        raise ValueError('S4 の封印の値が正本の対応表に無い: %s' % seal_value)
    return table[seal_value].get(outcome, '言えない')


# ---------------------------------------------------------------- 品質床の帰無発火率と検出力 ----
def qf_fail_questions(T, n):
    """品質床で「不合格」とする差の問い数。境目ちょうど（threshold_pt）は不合格（正本 `quality_floor.boundary_rule`）。"""
    return int(math.ceil(abs(float(T['quality_floor']['threshold_pt'])) / 100.0 * n - 1e-9))


def qf_null_rate(p, n, T):
    """**品質床の一セルの帰無発火率**（二標本・無操作と腕の真の正答率が同じ p・各 n 問）。境目の規則どおりに全数で数える（裁定 D137）。
    二標本は同じ問いの対の見方より保守側の上限である（正本 `quality_floor.two_sample_note`）。"""
    k = np.arange(n + 1)
    w = binom.pmf(k, n, p)
    D = k[:, None] - k[None, :]
    return float((w[:, None] * w[None, :])[D >= qf_fail_questions(T, n)].sum())


def qf_power(p, drop_pt, n, T):
    """品質床が真の低下 drop_pt を捕まえる確率（二標本・境目の規則どおり）。"""
    k = np.arange(n + 1)
    wN, wA = binom.pmf(k, n, p), binom.pmf(k, n, max(p - drop_pt / 100.0, 0.0))
    D = k[:, None] - k[None, :]
    return float((wN[:, None] * wA[None, :])[D >= qf_fail_questions(T, n)].sum())


def qf_multiplicity(T, cells, n=None, bases=(0.5, 0.7, 0.85), drop_pt=15):
    """選定後の品質床の多重性（**生成のときに数える**・裁定 D137）。一セルの帰無発火率・cells セルで一つ以上（独立の近似）・
    真の低下 drop_pt の捕捉率を、正答率ごとに返す。前は生成器に手で打った数で、境目の規則と合わなかった（再現の記録 K184）。"""
    n = int(n or T['quality_floor']['denominator'])
    out = {'post_cells': int(cells), 'n_per_arm': n, 'drop_pt': drop_pt,
           'rule': '二標本・境目ちょうどは不合格・%d セルは独立の近似' % int(cells)}
    for p in bases:
        key = '%03d' % int(round(p * 100))
        c = qf_null_rate(p, n, T)
        out['cell_at_%s' % key] = round(c, 4)
        out['any_at_%s' % key] = round(1 - (1 - c) ** int(cells), 3)
        out['power_at_%s' % key] = round(qf_power(p, drop_pt, n, T), 3)
    return out


# ---------------------------------------------------------------- 様式門の札 ----
def style_hold_label(p, nominal=0.05):
    """様式門に当たり、ほかの門に当たらなかった対比の札（採否表 P401・正本 `style_gate.asymmetry`）。
    名目の p が nominal 以上なら「非有意」（様式門は確証の札にのみ作用する——非有意の対比に保留も注も付けない）。
    nominal 未満なら「判定保留（様式転位）」（Holm の順位から外すので確証かどうかを決めない・裁定 D125）。
    前は p に関わらずすべて「判定保留（様式転位）」にし、非有意が保留に化けていた（再現の記録 K194・起草者に有利な向き）。"""
    return '判定保留（様式転位）' if (p is not None and p < nominal) else '非有意'


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


def homog_null_rate(p, T, ns=None):
    """**等質性の注の帰無の率**（採否表 P399）: 三方向の真の率が同じ p のとき、注（最大と最小の差が閾値を超える）が立つ確率（全数）。
    ns は方向ごとの試行の数（既定は本走行の一腕の等分）。"""
    thr = float(T['random_control']['homogeneity_max_spread_pt'])
    if ns is None:
        n_main = int(T['n_main'])
        cnt = int(T['random_control']['count'])
        ns = [n_main // cnt + (1 if i < n_main % cnt else 0) for i in range(cnt)]
    ks = [np.arange(n + 1) for n in ns]
    ws = [binom.pmf(k, n, p) for k, n in zip(ks, ns)]
    rs = [100.0 * k / n for k, n in zip(ks, ns)]
    grids = np.meshgrid(*rs, indexing='ij')
    W = ws[0]
    for w in ws[1:]:
        W = np.multiply.outer(W, w)
    spread = np.maximum.reduce(grids) - np.minimum.reduce(grids)
    return float(W[spread > thr + 1e-12].sum())


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
    # td の特異性（裁定 D133）: 一つの試験には一つの食い違いだけを入れる
    fam = td_specificity_family([dict(scenario='a', k_v=70, n_v=200, k_td=100, n_td=200, conf_label='確証', conf_diff_pt=-20.0),
                                 dict(scenario='b', k_v=100, n_v=200, k_td=70, n_td=200, conf_label='確証', conf_diff_pt=-20.0),
                                 dict(scenario='c', k_v=70, n_v=200, k_td=100, n_td=200, conf_label='非有意', conf_diff_pt=-5.0),
                                 dict(scenario='d', k_v=90, n_v=200, k_td=95, n_td=200, conf_label='確証', conf_diff_pt=-20.0)], T)
    assert [x['label'] for x in fam] == ['書ける', 'td のほうが動いた', '書かない', '書かない'], ('td の特異性の札', [x['label'] for x in fam])
    # td のほうが強い組（前の規則では「書ける」になった組）は、向きが逆なので「書ける」にならない
    one = td_specificity_family([dict(scenario='a', k_v=100, n_v=200, k_td=70, n_td=200, conf_label='確証', conf_diff_pt=-20.0)], T)[0]
    assert one['label'] != '書ける', ('td のほうが強い組で書けると言った', one)
    # S4 の門（裁定 D134）
    g1 = s4_gates(dict(cat=20, n_ok=200, ff=0, refuse=0, scoring_gap=0), dict(cat=24, n_ok=200, ff=80, refuse=0, scoring_gap=0), T)
    assert g1 == [T['gate_order']['labels']['希釈の門（書式外の差）']], ('S4 の書式外の門', g1)
    g2 = s4_gates(dict(cat=20, n_ok=200, ff=0, refuse=0, scoring_gap=2), dict(cat=24, n_ok=200, ff=0, refuse=0, scoring_gap=0), T)
    assert g2 == [T['gate_order']['labels']['判定不能（採点欠落）']], ('S4 の採点欠落の門', g2)
    assert s4_gates(dict(cat=20, n_ok=200, ff=0, refuse=0), dict(cat=24, n_ok=200, ff=0, refuse=0), T) == [], 'S4 の門が理由なく当たった'
    # S4 の封印の照合（裁定 D135）
    lab = s4_labels(T)
    for (o, sv), want in (((lab[0], '低下'), '当たり'), ((lab[0], 'どちらでもない'), '外れ'), ((lab[2], 'どちらでもない'), '当たり'),
                          ((lab[1], '上昇'), '当たり'), ((lab[3], '低下'), '言えない'), ((T['gate_order']['labels']['希釈の門（書式外の差）'], '低下'), '言えない')):
        assert s4_seal_match(o, sv, T) == want, ('S4 の封印の照合', o, sv, s4_seal_match(o, sv, T), want)
    assert not any('封印' in x for x in lab), ('S4 の札に封印の語が残っている', lab)
    # S4 の門の並び: 正本の一覧（applied）は gate_order の部分で、並びが同じ
    _ap = T['descriptive_families']['B_desc_S4']['gates_D134']['applied']
    assert _ap == [g for g in T['gate_order']['order'] if g in _ap], ('S4 の門の一覧が gate_order の並びと違う', _ap)
    # 品質床（裁定 D137）: 境目ちょうどは不合格——**不合格の問い数を器の外で数え直して**照らし（器の式を使わない）、
    # その上で閾値ちょうどの差の組を一つずつ数えた値と照らす
    fq = qf_fail_questions(T, 200)
    want_fq = next(d for d in range(201) if 100.0 * d / 200 >= abs(float(T['quality_floor']['threshold_pt'])) - 1e-12)
    assert fq == want_fq, ('品質床の不合格の問い数が境目の規則と違う', fq, want_fq)
    ref = sum(binom.pmf(i, 200, 0.85) * binom.pmf(j, 200, 0.85) for i in range(201) for j in range(201) if i - j >= fq)
    assert abs(qf_null_rate(0.85, 200, T) - ref) < 1e-12, ('品質床の帰無発火率', qf_null_rate(0.85, 200, T), ref)
    assert qf_null_rate(0.85, 200, T) > sum(binom.pmf(i, 200, 0.85) * binom.pmf(j, 200, 0.85) for i in range(201) for j in range(201) if i - j >= fq + 1), '境目を合格に数えている'
    # 等質性の帰無の率: 閾値を零にすればほぼ一、極端に大きくすれば零
    assert homog_null_rate(0.4, dict(T, random_control=dict(T['random_control'], homogeneity_max_spread_pt=1000))) == 0.0
    # 様式門の札（採否表 P401）
    assert style_hold_label(0.2) == '非有意' and style_hold_label(0.01) == '判定保留（様式転位）' and style_hold_label(None) == '非有意'
    print('[rules_B selftest] Newcombe の区間（文献値と scipy の Wilson）・S4 の行列の版と一つずつの版の全組一致・S4 の六つの枝・符号の積・refuse 門の読めた分母・api_error の門・td の特異性・等質性の境目・門の並び・td の特異性の族の規則（向き・確証・Holm）・S4 の門と封印の照合・品質床の境目・等質性の帰無の率・様式門の札: すべて通った')


if __name__ == '__main__':
    import sys
    if '--selftest' in sys.argv:
        _selftest()
