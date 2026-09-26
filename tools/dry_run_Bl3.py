# -*- coding: utf-8 -*-
"""dry_run_Bl3.py v4 —— B-lens 層三（Bl3）の合成データの器（正本 `review_plan.synthetic` の形のすべてと、乱数の小さな模型で端から端まで・2026-09-25）。

一. 純粋な関数の形（`tools/bl3_core.py`・`tools/blens_core.py`・`tools/analyze_Bl3.py`）: 奇でない押し・零でない帰無の中心・減算の行・下見で外れる升目と門の行だけの升目・
    帰無との同じ値・両方の向きがちょうど対称な比べる相手・掃き出し・端数のバッチ・零の近くの中央値・Holm の境で一本違う p・器の誤りでやり直す流れ・
    札の一致の中身（裁定 D232）・下見で外した後の偶然の目安（裁定 D231）・比べる相手の除き方の錨（裁定 D231）。
二. 乱数の小さな模型（登録機種の設定を小さくした bf16 の模型・実の重みではない・正規化の重みを散らす・CPU）と実のトークナイザで、走らせる器 `tools/bl3_run.py` の
    下見と本の計算（近道を使わない・裁定 D234）と、独立の再計算の二つの道（本の器のフックと、別の個体の残差の書き換えの器）を、等方は `--iso` の本数で通す。
    書き出しの割り方が変わる場合（器が止まるか）。二段の判定の形（一段目は無操作の値も比べる・裁定 D233・二段目は札の一致で判定する・裁定 D234）を、値をわざと
    ずらした写しで確かめる。下見の分かれ道（主の升目と門の行だけの升目を外した記録・バッチ一の記録・意見伺いの C1-C1・C2-A4）を、作った下見の記録で、
    本の計算 → 二つの道 → 一致だけを見る段 → 結果を開く段 → 掃き出し → 報告の組み立て → 走査まで、起動器の出力と同じ JSON の往復を通して流す（等方は `--e2e-iso` の本数）。
    近道の確かめのバッチ一の枝は、本の計算が近道を使わない（裁定 D234）ので無い。
三. わざと壊した読み取り（二重の正規化）と近道の元（主位置まで使い回す・記録した切れ目を偽る）で、自己検査と凍結した確かめが止まることを確かめる。
    本物の相対の加減の大きさにそろえた合成の方向で、書き換えの道の変種・主位置の一つ分の寄与・二段目の本の道とフックの差（意見伺いの C2-3.2）を記述として測る。
四. 別の個体の書き換えの器（`tools/bl3_recompute_rewrite.py`・中は変えない）の自己検査と `--dry` を今の本の器の上で走らせ、出力を記録に写す。
五. 起動器の三つの相を DRY で別のプロセスとして走らせ、集計の器の CLI（一致だけを見る段・結果を開く段）と掃き出しと報告の組み立てに通す。一致だけを見る段の後に組の出力を
    差し替えると、結果を開く段が止まることを確かめる（裁定 D236）。
v3（裁定 D236）で足した確かめ: 本の計算が近道を使わないことの振る舞い・正本の文から独立に書いた札と、答えの分かる合成での門の組み立て・等方の外の行が出る枝・
    有限でない値の止め・結果を開く段の結びつき。
記録の末尾に、走らせた器（凍結の器の一覧と import の閉包）と正本・設計事実・方向の記録の SHA16 を、走りの始めと終わりで同じことを確かめて並べる
（下見の前の凍結の器が今の版と突き合わせる）。
**実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の方向は、実の方向の名だけを借りた乱数（次元は小さな模型のもの）。
出力: records/Bl3/dry-run-Bl3-<日付>.md（--force が無ければ上書きしない）
用法: python tools/dry_run_Bl3.py [--force] [--iso 本数（既定は正本の本数）] [--e2e-iso 本数（既定 9）] [--out 置き場]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, glob, json, math, time, copy, shutil, hashlib, argparse, datetime, tempfile, subprocess, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C
import bl3_core as K

VERSION = 'v4'          # v4（2026-09-26・裁定 D239）: 門の行の割り当てを転記行 C と段階 B の集計の記録から照らす・台帳の照らし・書き換えの道の有限でない値・use_cache の既定を数える・組の書き換えで判定が止まる・相 check の守りが止める・DRY でない枝（六）・記録の名の欄の「|」／v3（2026-09-25・裁定 D236）: 近道の振る舞い・独立の札と答えの分かる門・等方の外の枝・有限でない値・結果を開く段の結びつき・起動器の三つの相／v2（裁定 D231〜D234）
NL = chr(10)
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
RESULTS = []
RUNNERS = []
RW_PASSES = [0]
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def check(group, name, ok, detail=''):
    detail = detail if isinstance(detail, str) else '・'.join(map(str, detail)) if isinstance(detail, (list, tuple)) else str(detail)      # 記録の表は文字列だけ
    RESULTS.append((group, name, bool(ok), detail))
    print('[dry_run_Bl3] %s %-4s %s %s' % (group, 'OK' if ok else 'FAIL', name, detail), flush=True)


def raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    return False


def err_of(fn, exc):
    """exc が上がればその文、上がらなければ None。"""
    try:
        fn()
    except exc as e_:
        return str(e_)
    return None


def jdefault(o):
    """起動器の出力の書き方（`boot_Bl3.write_json`）と同じ: numpy の数と配列を JSON に（値の丸めはしない）。"""
    if hasattr(o, 'tolist'):
        return o.tolist()
    if hasattr(o, 'item'):
        return o.item()
    raise TypeError(type(o))


rt = lambda o: json.loads(json.dumps(o, ensure_ascii=False, default=jdefault))      # 起動器の出力と同じ JSON の往復


def runner(R):
    RUNNERS.append(R)
    return R


def tool_shas():
    """走らせた器（凍結の器 `tools/freeze_Bl3.py` の器の一覧と、その import の閉包）と、正本・設計事実・方向の記録の SHA16。"""
    import freeze_Bl3 as FZ
    files = FZ.import_closure(FZ.TOOLS) + ['design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json']
    return collections.OrderedDict((f, sha16f(os.path.join(REPO, *f.split('/')))) for f in files)


# ---------------- 正本の文から独立に書いた主の札（検べ用・芯の関数を呼ばない・裁定 D236） ----------------
def answer_labels(T3, main_rows, eff, pair_names, dropped=()):
    """正本 `labels.p_rule`（両側に等しい裾）・`labels.iso_outside.rule`（Holm・段を下回れば通し、通らなかった所で止める）・`labels.second`（比べる相手の中央値を中心に、
    距離が比べる相手のすべてを上回れば最上位・向きの順位と対の単位の順位）・`labels.side_rule`（等方の帰無の四分位と中央値）・`labels.second.iso_top_share`・`nulls.real.rule`
    （v̂ と (6b) は兄弟の対を除き、Nk と td は B-lens の凍結の自分の対だけを除く）を、文から書き直した。"""
    alpha = T3['labels']['iso_outside']['holm_alpha']
    n_iso = T3['nulls']['isotropic']['count']
    own = K.blens_own_pair()                                           # 二つの道の外の凍結物（B-lens の器の文から読む）
    swaps = set(T3['nulls']['real']['swap_siblings'])
    key = lambda sc, b, sg: '%s|%s|%+d' % (sc, b, int(sg))
    out, pv = collections.OrderedDict(), {}
    for r in main_rows:
        if '%s|%s' % (r['scenario'], r['base']) in set(dropped):
            continue
        k, kk = key(r['scenario'], r['base'], r['sign']), key(r['scenario'], r['base'], -r['sign'])
        e = float(eff[k][r['direction']])
        iso = np.array([eff[k]['iso:%d' % i] for i in range(n_iso)], dtype=np.float64)
        dropc = swaps if r['direction'] in ('static', 'loaded') else {own[r['direction']]}
        comps = [q for q in pair_names if q not in dropc]
        same = np.array([eff[k]['real:' + q] for q in comps], dtype=np.float64)
        opp = np.array([eff[kk]['real:' + q] for q in comps], dtype=np.float64)
        up, lo = int(np.sum(iso >= e)), int(np.sum(iso <= e))
        p = min(1.0, 2.0 * min(up + 1, lo + 1) / (n_iso + 1))
        tail = 'upper' if up < lo else ('lower' if lo < up else 'tie')
        allc = np.concatenate([same, opp])
        c0 = float(np.median(allc))
        d = abs(e - c0)
        dc = np.abs(allc - c0)
        pairv = np.maximum(np.abs(same - c0), np.abs(opp - c0))
        m0, q1, q3 = float(np.median(iso)), float(np.percentile(iso, 25)), float(np.percentile(iso, 75))
        if q1 <= 0.0 <= q3:
            side = ('sign_only', int(np.sign(e)))
        else:
            s0 = 1.0 if m0 > 0 else -1.0
            side = ('stronger' if (e * s0 > 0 and abs(e) > abs(m0)) else ('weaker' if e * s0 >= 0 else 'opposite'), None)
        out[r['id']] = {'p': p, 'tail': tail, 'top': bool(np.all(d > dc)), 'rank_o': int(1 + np.sum(dc >= d)), 'rank_p': int(1 + np.sum(pairv >= d)),
                        'side': side, 'share': float(np.mean(np.abs(iso - c0) > float(np.max(dc))))}
        pv[r['id']] = p
    still = True
    for i, rid in enumerate(sorted(pv, key=lambda x: (pv[x], x))):
        ok = still and pv[rid] < alpha / (len(pv) - i)
        out[rid]['holm'] = ok
        still = ok
    return out


def synth_effects(T3, pair_names, n_iso, seed):
    """合成の効き目（升目と符号の鍵 → 方向の名 → 効き目）: 奇でない押し（逆の符号の升目の効き目は別に引く）・零でない帰無の中心（升目ごとに中心を変える）・
    等方の外に出る強い v̂ と Nk の行を半分ほど。値に意味は無い（札の組み立ての確かめだけに使う）。"""
    rng = np.random.default_rng(seed)
    names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
    keys = sorted({'%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']} | {'%s|%s|%+d' % (sc, b, -int(sg)) for sc, b, sg in T3['cell_signs_main']})
    eff = {}
    for j, k in enumerate(keys):
        center = (-1.0) ** j * (0.5 + 0.25 * j)
        e = {d: float(rng.normal(loc=center, scale=0.5)) for d in names}
        e.update({'iso:%d' % i: float(x) for i, x in enumerate(rng.normal(loc=center, scale=0.5, size=n_iso))})
        e.update({'real:' + q: float(x) for q, x in zip(pair_names, rng.normal(loc=0.0, scale=1.5, size=len(pair_names)))})
        if j % 2 == 0:
            e['static'] = center + 6.0 * (1 if j % 4 == 0 else -1)
            e['Nk'] = center - 6.0
        eff[k] = e
    return eff


# ---------------- 一. 純粋な関数の形 ----------------
def part_pure():
    G = '一'
    rng = np.random.default_rng(11)
    units = ['A', 'B', 'C', 'D']
    # 奇でない押し: 逆の符号の升目の効き目を「正の升目の効き目の符号を反転したもの」で代えると、門の答えが変わる
    fp, fm = 'S1|X|+1', 'S1|X|-1'
    eff = {u: {fp: float(i), fm: float(i) ** 2 - 2.0} for i, u in enumerate(units)}
    rows = [{'unit': u, 'cell': 'S1|X', 'fam': fm, 'y': eff[u][fm]} for u in units] + [{'unit': u, 'cell': 'S1|X', 'fam': fp, 'y': eff[u][fp]} for u in units]
    g_ok = K.gate(rows, eff, units, 0.05)
    wrong = {u: {fp: eff[u][fp], fm: -eff[u][fp]} for u in units}
    g_wrong = K.gate(rows, wrong, units, 0.05)
    check(G, '奇でない押し（逆の符号の升目の効き目をそのまま使う）', g_ok['rho'] > 0.99 and abs(g_wrong['rho'] - g_ok['rho']) > 0.1,
          '正しい呼び方 ρ %.3f／反転で代えた呼び方 ρ %.3f' % (g_ok['rho'], g_wrong['rho']))
    # 零でない帰無の中心: 対称の割合では外に出ない反対の側の値が、両側に等しい裾の割合では外に出る
    null = rng.normal(loc=3.0, scale=0.5, size=1999)
    pe, ps = K.p_and_tail(-1.0, null)['p'], C.p_two_sided(-1.0, null)
    pc_ = K.p_and_tail(3.0, null)['p']
    check(G, '零でない帰無の中心', pe <= 2 / 2000 + 1e-12 and ps > 0.5 and pc_ > 0.5, '反対の側の値: 等しい裾 %.4f・対称 %.4f／中心の値: 等しい裾 %.3f' % (pe, ps, pc_))
    # 減算の行: 符号を二重に掛けると押しの向きが反転する
    rows_s = [{'unit': u, 'cell': 'S1|X', 'fam': fm, 'y': 2 * eff[u][fm]} for u in units]
    ok_ = C.gate_perm([dict(r, sign=1) for r in rows_s], eff, units)
    dbl = C.gate_perm([dict(r, sign=-1) for r in rows_s], eff, units)
    check(G, '減算の行（符号の二重掛け）', ok_['rho'] > 0.99 and dbl['rho'] < -0.99, '符号 +1 ρ %.3f／二重掛け ρ %.3f' % (ok_['rho'], dbl['rho']))
    # 下見で外れる升目と、門の行だけの升目（門の行・入れ替えの数・Holm の段）
    rows_g = [{'unit': u, 'cell': c, 'fam': c + '|+1', 'y': float(i)} for i, u in enumerate(units) for c in ('S1|X', 'S4|Y')] + [{'unit': 'E', 'cell': 'S4|Y', 'fam': 'S4|Y|+1', 'y': 0.5}]
    eff_g = {u: {'S1|X|+1': float(i), 'S4|Y|+1': float(i)} for i, u in enumerate(units + ['E'])}
    g_all = K.gate(rows_g, eff_g, units + ['E'], 0.05)
    g_drop = K.gate(rows_g, eff_g, units + ['E'], 0.05, drop_cells=['S4|Y'])
    pv = {'r%d' % i: 0.001 * (i + 1) for i in range(16)}
    h16 = K.holm(pv, 0.05)
    pv14 = {k: v for k, v in pv.items() if k not in ('r14', 'r15')}
    h14 = K.holm(pv14, 0.05)
    step1_16 = min(v['step'] for v in h16.values())
    step1_14 = min(v['step'] for v in h14.values())
    check(G, '下見で外れる升目と門の行だけの升目', g_all['n_perm'] == 120 and g_drop['n_perm'] == 24 and g_drop['n_rows'] == 4 and abs(step1_16 - 0.05 / 16) < 1e-15 and abs(step1_14 - 0.05 / 14) < 1e-15,
          '入れ替え %d → 外した後 %d（行 %d・行の無くなった単位を外した）・Holm の第一段 %.6f → %.6f' % (g_all['n_perm'], g_drop['n_perm'], g_drop['n_rows'], step1_16, step1_14))
    # 帰無との同じ値: 両方の裾に数える・二つ目の札は同じ距離を上回らない
    nl = np.array([0.0, 1.0, 1.0, 2.0, 3.0])
    t = K.p_and_tail(1.0, nl)
    comps = np.array([-1.0, 1.0, 2.0])                   # 中心は 1・行 3.0 の距離 2 と、比べる相手 -1.0 の距離 2 が同じ
    sl = K.second_label(3.0, comps, [(-1.0, 2.0)])
    check(G, '帰無との同じ値', t['upper'] == 4 and t['lower'] == 3 and not sl['top'], '上の裾 %d・下の裾 %d（同じ値を両方に数える）・同じ距離の比べる相手があれば最上位にしない' % (t['upper'], t['lower']))
    # 両方の向きがちょうど対称な比べる相手: 中心は零・対の単位の順位は向きの順位の半分の側
    xs = rng.normal(size=24)
    co = np.concatenate([xs, -xs])
    pairs = list(zip(xs, -xs))
    sl2 = K.second_label(0.5, co, pairs)
    check(G, '両方の向きがちょうど対称な比べる相手', abs(sl2['center']) < 1e-12 and sl2['rank_oriented'] == 2 * sl2['rank_pair'] - 1,
          '中心 %.2e・向きの順位 %d・対の順位 %d' % (sl2['center'], sl2['rank_oriented'], sl2['rank_pair']))
    # 端数のバッチ
    ids = ['d%d' % i for i in range(2034)]
    bp = K.batch_plan(ids, 16, T3['readout']['primary']['order_seed'], 0)
    flat = [x for b in bp for x in b]
    check(G, '端数のバッチ（零のベクトルで埋める）', len(bp) == 128 and flat.count(K.PAD) == 13 and flat.count(K.NOOP) == 1 and set(flat) - {K.PAD, K.NOOP} == set(ids),
          'バッチ %d・埋める %d・無操作 %d' % (len(bp), flat.count(K.PAD), flat.count(K.NOOP)))
    # 零の近くの中央値
    s0 = K.effect_side(-2.0, rng.normal(loc=0.05, scale=1.0, size=1999))
    check(G, '零の近くの中央値（符号だけ）', s0['side'] == 'sign_only' and s0['sign'] == -1, '四分位 [%.3f, %.3f]' % (s0['q1'], s0['q3']))
    # Holm の境で一本違う p: 札の一致が落ちる
    Kn = T3['nulls']['isotropic']['count']
    lim = K.holm_limits(Kn, 0.05, 16)
    base_null = np.linspace(-1.0, 1.0, Kn)
    m_row = float(base_null[-1 - lim[0]]) + 1e-9          # 上の裾に帰無が lim[0] 本だけ残る値
    pA = K.p_and_tail(m_row, base_null)['p']
    null_B = base_null.copy()
    null_B[-2 - lim[0]] = m_row + 1e-6                    # 帰無一本がこの値を越える
    pB = K.p_and_tail(m_row, null_B)['p']
    others = {'r%d' % i: 0.5 for i in range(1, 16)}
    hA = K.holm(dict(others, r0=pA), 0.05)['r0']['pass']
    hB = K.holm(dict(others, r0=pB), 0.05)['r0']['pass']
    ag = K.agreement({'r0': [0.0]}, {'r0': [0.0]}, 0.001, {'r0': hA}, {'r0': hB})
    check(G, 'Holm の境で一本違う p（札の一致の判定）', hA and not hB and not ag['agree'] and ag['values_within_tol'], 'p %.4f → %.4f・Holm の判定 %s → %s・一致 %s' % (pA, pB, hA, hB, ag['agree']))
    # 器の誤りでやり直す流れ
    q = K.q1_from_attempts([{'tool_error': '出口の値の自己検査が落ちた'}, {'decision': {'q1': '一部の升目を外して続ける'}}])
    q2 = K.q1_from_attempts([{'decision': {'q1': '止める'}}, {'decision': {'q1': '続ける'}}])
    q3 = K.q1_from_attempts([{'tool_error': 'x'}])
    check(G, '器の誤りでやり直す流れ（q1 の採点）', q['scored'] and q['q1'] == '一部の升目を外して続ける' and q2['first_decision'] == '止める' and not q3['scored'],
          'やり直した下見で採点・一度目の決定を併記・やり直さなければ採点しない')
    # 掃き出し: 札と門と向きの足し分に要る升目・符号・方向の組が、本の計算の組み立てにそろう
    import bl3_run as BR
    import analyze_Bl3 as AZ
    names_real = ['real:' + p for p in DJ['groups']['real']['names']]
    iso_ids = ['iso:%d' % i for i in range(T3['nulls']['isotropic']['count'])]
    b3 = ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
    gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
    sets = BR.cell_sign_sets(T3, None, T3['directions']['named'], b3, iso_ids, names_real, gate_only)
    have = {(k, d) for k, cell, sg, ds in sets for d in ds}
    need, miss = set(), []
    for r in T3['main_rows']:
        k = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
        kk = '%s|%s|%+d' % (r['scenario'], r['base'], -r['sign'])
        need.add((k, r['direction']))
        need |= {(k, i) for i in iso_ids}
        comps = K.comparators_for(r['direction'], DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'])
        need |= {(k, 'real:' + p) for p in comps} | {(kk, 'real:' + p) for p in comps}
    fams = sorted({'%s|%s|%+d' % (g['scenario'], g['base'], g['sign']) for g in FJ['facts']['C']['gate_rows']})
    unit_ids = list(T3['directions']['named']) + b3
    need |= {(f, u) for f in fams for u in unit_ids}
    miss = sorted(need - have)
    check(G, '掃き出し（要る組が本の計算の組み立てにそろう）', not miss, '要る組 %d・組み立て %d・足りない %d%s' % (len(need), len(have), len(miss), ('（例 %s）' % miss[:3]) if miss else ''))
    n_passes = sum(len(ds) for _, _, _, ds in sets)
    E = FJ['facts']['E']
    check(G, '本の計算の順伝播の数（転記行 E と）', n_passes == E['passes_main'] + E['passes_gate_extra'] + E['passes_orient_extra'],
          '組み立て %d・転記行 E %d ＋ %d ＋ %d' % (n_passes, E['passes_main'], E['passes_gate_extra'], E['passes_orient_extra']))
    # 札の一致の中身（裁定 D232）: 等方の内側の行の裾と側は比べない・等方の外の行の裾と側は比べる
    lab0 = {'r_in': {'iso_outside': False, 'tail': 'upper', 'side': {'side': 'stronger', 'sign': 1}, 'second': {'top': False}},
            'r_out': {'iso_outside': True, 'tail': 'upper', 'side': {'side': 'stronger', 'sign': 1}, 'second': {'top': True}}}
    lab_in = copy.deepcopy(lab0)
    lab_in['r_in'].update(tail='lower', side={'side': 'opposite', 'sign': -1})
    lab_tail, lab_side = copy.deepcopy(lab0), copy.deepcopy(lab0)
    lab_tail['r_out']['tail'] = 'lower'
    lab_side['r_out']['side'] = {'side': 'weaker', 'sign': 1}
    sg_ = AZ.labels_signature
    check(G, '札の一致の中身（等方の内側の行の裾と側は比べない・等方の外の行の裾と側は比べる・裁定 D232）',
          sg_(lab0) == sg_(lab_in) and sg_(lab0) != sg_(lab_tail) and sg_(lab0) != sg_(lab_side),
          '内側の行の裾と側だけが違う → 同じ・外の行の裾が違う → 違う・外の行の側が違う → 違う')
    # 下見で外した後の偶然の目安（裁定 D231）: 外さなければ正本の生成器の値と同じ・外すと外した行の分だけ減る
    lab_all = {r['id']: {'direction': r['direction']} for r in T3['main_rows']}
    drop_c = 'N1|O-Ncold'
    gone = [r for r in T3['main_rows'] if '%s|%s' % (r['scenario'], r['base']) == drop_c]
    ch_all = AZ.chance_after_drop(T3, lab_all)
    ch_d = AZ.chance_after_drop(T3, {k: v for k, v in lab_all.items() if k not in {r['id'] for r in gone}})
    co_, cp_ = T3['nulls']['real']['comparators_oriented'], T3['nulls']['real']['comparators']
    less_o = round(ch_all['oriented'] - sum(1 / (co_[r['direction']] + 1) for r in gone), 4)
    less_p = round(ch_all['pair'] - sum(1 / (cp_[r['direction']] + 1) for r in gone), 4)
    check(G, '下見で外した後の偶然の目安（外さなければ正本の値・外すと外した行の分だけ減る・裁定 D231）',
          (ch_all['oriented'], ch_all['pair']) == (T3['nulls']['real']['chance_second'], T3['nulls']['real']['chance_second_pair']) and
          abs(ch_d['oriented'] - less_o) < 1e-4 and abs(ch_d['pair'] - less_p) < 1e-4 and sum(ch_d['rows_by_direction'].values()) == len(T3['main_rows']) - len(gone),
          '外さない %.4f・%.4f（正本 %.4f・%.4f）／%s を外す %.4f・%.4f（行 %d）' % (ch_all['oriented'], ch_all['pair'], T3['nulls']['real']['chance_second'],
                                                                         T3['nulls']['real']['chance_second_pair'], drop_c, ch_d['oriented'], ch_d['pair'], sum(ch_d['rows_by_direction'].values())))
    # 比べる相手の除き方の錨（裁定 D231）: B-lens の凍結の OWN_PAIR と正本の兄弟の対に照らす・ずらした写しで止まる
    pn, sw, own = DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'], K.blens_own_pair()
    anc = K.comparator_anchor(pn, sw, own)
    stop_own = raises(lambda: K.comparator_anchor(pn, sw, dict(own, Nk=own['static'])), ValueError)
    stop_sw = raises(lambda: K.comparator_anchor(pn, [x for x in sw if x != own['static']], own), ValueError)
    check(G, '比べる相手の除き方の錨（B-lens の凍結の OWN_PAIR と正本の兄弟の対・裁定 D231）', bool(anc) and stop_own and stop_sw,
          '除いた対の数 %s・錨をずらした写しで止まる %s・兄弟の対から自分の対を抜いた写しで止まる %s' % ({d: len(v) for d, v in anc.items()}, stop_own, stop_sw))
    # 正本の文から独立に書いた札（芯の関数を呼ばない）と、集計の器の札の突き合わせ（等方は正本の本数・奇でない押し・零でない帰無の中心・下見で外した升目・裁定 D236）
    n_iso = T3['nulls']['isotropic']['count']
    pn_ = DJ['groups']['real']['names']
    eff_s = synth_effects(T3, pn_, n_iso, seed=17)
    for dropped_ in ([], ['N1|O-Ncold']):
        mine = answer_labels(T3, T3['main_rows'], eff_s, pn_, dropped_)
        lab_, meta_ = AZ.row_labels(T3, T3['main_rows'], eff_s, pn_, dropped_)
        diff_ = []
        for rid, a_ in mine.items():
            o = lab_.get(rid)
            if o is None:
                diff_.append((rid, '行が無い'))
                continue
            got = (round(o['p'], 12), o['tail'], o['iso_outside'], o['second']['top'], o['second']['rank_oriented'], o['second']['rank_pair'], o['side']['side'],
                   o['side'].get('sign') if o['side']['side'] == 'sign_only' else None, round(o['iso_top_share'], 12))
            want_ = (round(a_['p'], 12), a_['tail'], a_['holm'], a_['top'], a_['rank_o'], a_['rank_p'], a_['side'][0], a_['side'][1], round(a_['share'], 12))
            if got != want_:
                diff_.append((rid, got, want_))
        n_out = sum(1 for a_ in mine.values() if a_['holm'])
        check(G, '正本の文から独立に書いた札と集計の器の札（等方 %d 本・外した升目 %s・裁定 D236）' % (n_iso, '・'.join(dropped_) or 'なし'),
              not diff_ and set(lab_) == set(mine) and n_out > 0 and meta_['m_rows'] == len(mine),
              '行 %d・食い違い %d・等方の外の行 %d・Holm の段の数 %d%s' % (len(mine), len(diff_), n_out, meta_['m_rows'], ('（例 %s）' % (diff_[:1],)) if diff_ else ''))
    # 等方の外の行が出る枝: 札の一致の中身（裁定 D232）・q7・予想の答え
    lab_, _ = AZ.row_labels(T3, T3['main_rows'], eff_s, pn_, [])
    out_ids = [rid for rid, o in lab_.items() if o['iso_outside']]
    in_ids = [rid for rid, o in lab_.items() if not o['iso_outside']]
    q7r = AZ.q7_rows_of(lab_, FJ)
    sig0 = AZ.labels_signature(lab_)
    flip_in, flip_out = copy.deepcopy(lab_), copy.deepcopy(lab_)
    if in_ids:
        flip_in[in_ids[0]]['tail'] = 'lower' if flip_in[in_ids[0]]['tail'] != 'lower' else 'upper'
    flip_out[out_ids[0]]['tail'] = 'lower' if flip_out[out_ids[0]]['tail'] != 'lower' else 'upper'
    check(G, '等方の外の行が出る枝（割合を決めた裾の比べは外の行だけ・q7 の行・裁定 D232・D236）',
          bool(out_ids) and AZ.labels_signature(flip_in) == sig0 and AZ.labels_signature(flip_out) != sig0 and bool(q7r) and all(r_['id'] in out_ids for r_ in q7r),
          '等方の外の行 %d・内の行の裾を変える → 札は同じ・外の行の裾を変える → 札が違う・q7 の行 %d' % (len(out_ids), len(q7r)))
    # 答えの分かる合成での門の組み立て: 門の行の効き目を行動の量と同じ値に置けば、本の門の順位相関はちょうど一。これは門の関数が行の鍵どおりに効き目を引くことを確かめる。
    # 行の家族の鍵・単位・行動の量の割り当ては、確かめる相手（stage_b_gate_rows）が付けたものを使うので、その割り当ての誤りは捕まえない（下の割り当ての照らしが受ける・裁定 D239）
    AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
    rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
    units_g = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
    rng_g = np.random.default_rng(23)
    for drop_g in ([], ['N1|O-Ncold']):
        eff_g = collections.defaultdict(dict)
        for r_ in rows_gate:
            if r_['cell'] in set(drop_g):
                continue                                               # 外した升目の家族の効き目は置かない（集計の器は引かないはず・裁定 D231）
            for u in units_g:
                eff_g[r_['fam']].setdefault(u, float(rng_g.normal()))
            eff_g[r_['fam']][r_['unit']] = float(r_['y'])
        G_ = AZ.gates(T3, rows_gate, dict(eff_g), drop_g, ())
        n_left = sum(1 for r_ in rows_gate if r_['cell'] not in set(drop_g))
        check(G, '答えの分かる合成での門の組み立て（行の効き目を行動の量に置く・外した升目 %s・裁定 D236）' % ('・'.join(drop_g) or 'なし'),
              abs(G_['main']['rho'] - 1.0) < 1e-12 and G_['main']['n_rows'] == n_left and G_['desc_choice_a']['rho'] < 1.0 - 1e-9,
              '本の門の順位相関 %.12f・行 %d（残った門の行 %d）・選択 a の件数の門の順位相関 %.4f（一でない）' % (G_['main']['rho'], G_['main']['n_rows'], n_left, G_['desc_choice_a']['rho']))

    # 門の行の割り当ての照らし（裁定 D239・器の直しの確かめ C1-新7・C2-4）: 鍵（升目・腕・方向・土台・符号・単位）を設計事実の転記行 C（別の器が組んだ）と、
    # 家族の鍵と升目を鍵の決まり（場面|土台|符号）と、行動の量を正本の文（その行の破局の対数オッズ − 土台の無操作の腕の破局の対数オッズ・件数に連続性の補正を足す）から
    # 段階 B の凍結した集計の記録で直に計算した値と照らす（芯の式を呼ばない）
    cc_ = T3['gate']['continuity']
    BDx = {(r_['scenario'], r_['arm'], r_['direction_id']): r_ for r_ in AN['by_direction']}
    lg_ = lambda k_, n_: math.log((k_ + cc_) / (n_ - k_ + cc_))
    y_bad = [r_['name'] for r_ in rows_gate if abs(r_['y'] - (lg_(BDx[(r_['scenario'], r_['arm'], r_['direction_id'])]['cat'], BDx[(r_['scenario'], r_['arm'], r_['direction_id'])]['n_ok'])
                                                             - lg_(BDx[(r_['scenario'], r_['base'], 'fixed')]['cat'], BDx[(r_['scenario'], r_['base'], 'fixed')]['n_ok']))) > 1e-12]
    fam_bad = [r_['name'] for r_ in rows_gate if r_['fam'] != '%s|%s|%+d' % (r_['scenario'], r_['base'], int(r_['sign'])) or r_['cell'] != '%s|%s' % (r_['scenario'], r_['base'])]
    fc_bad = AZ.gate_rows_vs_facts(rows_gate, FJ)
    check(G, '門の行の割り当ての照らし（鍵を転記行 C と・家族の鍵を鍵の決まりと・行動の量を段階 B の集計の記録から正本の文で・裁定 D239）', not y_bad and not fam_bad and not fc_bad,
          '行 %d・行動の量の食い違い %d・家族の鍵の食い違い %d・転記行 C との食い違い %d' % (len(rows_gate), len(y_bad), len(fam_bad), len(fc_bad)))
    # 取り違えの見本: 答えの分かる合成は一のまま通り、上の照らしが捕まえる（鍵を重ねない取り違え三つ）
    fa_, fb_ = sorted({r_['fam'] for r_ in rows_gate})[0], sorted({r_['fam'] for r_ in rows_gate})[-1]
    bug_f = copy.deepcopy(rows_gate)
    for r_ in bug_f:
        r_['fam'] = fb_ if r_['fam'] == fa_ else (fa_ if r_['fam'] == fb_ else r_['fam'])
    bug_y = copy.deepcopy(rows_gate)
    ia_ = next(i for i, r_ in enumerate(bug_y) if r_['fam'] == fa_)
    ib_ = next(i for i, r_ in enumerate(bug_y) if r_['fam'] == fb_ and abs(r_['y'] - bug_y[ia_]['y']) > 1e-9)
    bug_y[ia_]['y'], bug_y[ib_]['y'] = bug_y[ib_]['y'], bug_y[ia_]['y']
    bug_u = copy.deepcopy(rows_gate)
    fam_u_ = collections.defaultdict(dict)
    for i, r_ in enumerate(bug_u):
        fam_u_[r_['fam']][r_['unit']] = i
    iu_, ju_ = next(((d_['Nk'], d_['td']) for d_ in fam_u_.values() if 'Nk' in d_ and 'td' in d_), None) or         next(((d_[a__], d_[b__]) for d_ in fam_u_.values() for a__ in d_ for b__ in d_ if a__ < b__))
    bug_u[iu_]['unit'], bug_u[ju_]['unit'] = bug_u[ju_]['unit'], bug_u[iu_]['unit']

    def ak_rho(rows_):
        rg_ = np.random.default_rng(23)
        e_ = collections.defaultdict(dict)
        for r_ in rows_:
            for u in units_g:
                e_[r_['fam']].setdefault(u, float(rg_.normal()))
            e_[r_['fam']][r_['unit']] = float(r_['y'])
        return AZ.gates(T3, rows_, dict(e_), [], ())['main']['rho']
    caught = {}
    for nm_, b_ in (('家族の名の入れ替え', bug_f), ('行動の量の入れ替え', bug_y), ('単位の入れ替え', bug_u)):
        y2 = [r_['name'] for r_ in b_ if abs(r_['y'] - (lg_(BDx[(r_['scenario'], r_['arm'], r_['direction_id'])]['cat'], BDx[(r_['scenario'], r_['arm'], r_['direction_id'])]['n_ok'])
                                                       - lg_(BDx[(r_['scenario'], r_['base'], 'fixed')]['cat'], BDx[(r_['scenario'], r_['base'], 'fixed')]['n_ok']))) > 1e-12]
        f2 = [r_['name'] for r_ in b_ if r_['fam'] != '%s|%s|%+d' % (r_['scenario'], r_['base'], int(r_['sign']))]
        caught[nm_] = (abs(ak_rho(b_) - 1.0) < 1e-12, bool(y2 or f2 or AZ.gate_rows_vs_facts(b_, FJ)))
    check(G, '取り違えの見本（鍵を重ねない三つ）: 答えの分かる合成は一のまま通り、割り当ての照らしが捕まえる（裁定 D239）', all(a_ and b__ for a_, b__ in caught.values()),
          '・'.join('%s: 答えの分かる合成 %s・割り当ての照らし %s' % (k_, '一のまま' if v_[0] else '一でない', '捕まえた' if v_[1] else '捕まえない') for k_, v_ in caught.items()))
    # 台帳の器の差分の照らし（裁定 D239・芯の ledger_chain_bad）
    bs_ = {'tools/a.py': '1', 'tools/b.py': '2'}
    dv_ = lambda *tds: [{'no': 'x', 'tool_diffs': [{'path': p_, 'before': b__, 'after': a__} for p_, b__, a__ in tds]}]
    cases_ = [('差分なし・同じ', dict(bs_), [], True), ('台帳に無い変え', {'tools/a.py': '3', 'tools/b.py': '2'}, [], False),
              ('台帳に記した変え', {'tools/a.py': '3', 'tools/b.py': '2'}, dv_(('tools/a.py', '1', '3')), True),
              ('同じ置き場の二度の直し', {'tools/a.py': '4', 'tools/b.py': '2'}, dv_(('tools/a.py', '1', '3')) + dv_(('tools/a.py', '3', '4')), True),
              ('前後の切れ', {'tools/a.py': '4', 'tools/b.py': '2'}, dv_(('tools/a.py', '1', '3')) + dv_(('tools/a.py', '5', '4')), False),
              ('記したのに現れない', dict(bs_), dv_(('tools/a.py', '1', '3')), False)]
    got_ = [(nm_, not K.ledger_chain_bad(bs_, now_, d_)) for nm_, now_, d_, want_ in cases_]
    check(G, '台帳の器の差分を路ごとにつなげる照らし（二度の直しは通り・切れと無い変えと現れない差分は止まる・裁定 D239）', all(g_ == w_[3] for (_, g_), w_ in zip(got_, cases_)),
          '・'.join('%s %s' % (nm_, '通る' if g_ else '止まる') for nm_, g_ in got_))
    # 書き換えの道の有限でない値は、判定の段で不一致として記す（例外で落ちない・裁定 D239・器の直しの確かめ C2-7）
    n_can_ = T3['nulls']['isotropic']['count']
    pair_names = list(DJ['groups']['real']['names'])
    eff_n = synth_effects(T3, pair_names, n_can_, 37)
    swaps_ = T3['nulls']['real']['swap_siblings']
    rows_n, dbr_n = K.recompute_set(T3['main_rows'], pair_names, swaps_, n_can_)

    def path_n(noise):
        o_ = {}
        for nm_, ck_, s_ in rows_n:
            sc_, b__ = ck_.split('|')
            o_[nm_] = {'noop_lo': 0.0, 'effects': {'%s|%+d' % (d_, sg_): float(eff_n['%s|%s|%+d' % (sc_, b__, sg_)][d_]) + noise for d_, sg_ in dbr_n[nm_]}}
        return o_
    hk_n, rw_n = path_n(0.0), path_n(1e-7)
    ag_ok = AZ.recompute_agreement(T3, T3['main_rows'], eff_n, pair_names, hk_n, rw_n, {'floor': 1e-6})
    rw_bad = copy.deepcopy(rw_n)
    r0_ = next(iter(rw_bad))
    rw_bad[r0_]['effects'][next(k_ for k_ in rw_bad[r0_]['effects'] if k_.startswith('static|'))] = float('nan')
    try:
        ag_nan = AZ.recompute_agreement(T3, T3['main_rows'], eff_n, pair_names, hk_n, rw_bad, {'floor': 1e-6})
        nan_msg = '不一致 %s・理由 %s' % (not ag_nan['agree'], ag_nan.get('reason'))
        nan_ok = (not ag_nan['agree']) and ag_nan.get('reason') == 'non_finite'
    except Exception as e_:
        nan_ok, nan_msg = False, '%s: %s' % (type(e_).__name__, str(e_)[:60])
    check(G, '書き換えの道の有限でない値は判定の段で不一致として記す（例外で落ちない・等方 %d 本・裁定 D239）' % n_can_, bool(ag_ok['agree']) and nan_ok,
          'NaN の無い二つの道 一致 %s／書き換えの道の v̂ の効き目の一つを NaN に → %s' % (bool(ag_ok['agree']), nan_msg))


# ---------------- 二・三. 乱数の小さな模型 ----------------
def tiny_model(seed=0, layers=4):
    import torch
    from transformers import AutoConfig, AutoModelForCausalLM
    cfg = AutoConfig.from_pretrained(SNAP)
    cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim, cfg.intermediate_size = 64, layers, 4, 2, 16, 128
    if getattr(cfg, 'layer_types', None):
        cfg.layer_types = list(cfg.layer_types)[:layers]
    torch.manual_seed(seed)
    model = AutoModelForCausalLM.from_config(cfg)
    with torch.no_grad():
        g = torch.Generator().manual_seed(seed + 1)
        for n, p in model.named_parameters():
            if n.endswith('norm.weight'):                 # 乱数の初期値は一なので、二重の正規化が見えない——散らす
                p.copy_(torch.rand(p.shape, generator=g) + 0.5)
    return model.to(torch.bfloat16).eval(), cfg


def calibrate_readout_rows(model, R0, cell, FJ, seed=7):
    """乱数の模型の出口の行列を、読み取りの集合の文字が強く出るように置く（正本の閾値は変えずに、下見を本の計算まで通すため・合成だけ）。
    読み取りの集合の文字の行を、升目 cell の無操作の最終の正規化の出口の向きの三倍に小さな乱数を足したものにする。起動器の DRY も同じ関数を呼ぶ。"""
    import torch
    cap = {}
    hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
    with torch.no_grad():
        model(input_ids=torch.tensor([cell.ids]), logits_to_keep=1)
    hh.remove()
    m_ = R0.norm32(cap['h'])[0]
    m_ = m_ / m_.norm()
    set_all = sorted({int(x) for x in FJ['facts']['A']['letter_ids'].values()})
    gcal = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        for tkn in set_all:
            model.lm_head.weight[tkn] = (3.0 * m_ + 0.3 * torch.randn(m_.shape, generator=gcal)).to(model.lm_head.weight.dtype)
    return set_all


def synth_dirs(dim, names, seed=5):
    rng = np.random.default_rng(seed)
    v = rng.normal(size=dim)
    nv = float(np.linalg.norm(v))
    out = collections.OrderedDict()
    for n in names:
        x = v if n == 'static' else rng.normal(size=dim)
        out[n] = x * (nv / float(np.linalg.norm(x)))
    out['zero:test'] = np.zeros(dim)
    return out


def rewrite(RW, model, tok, rows, dbr, dirs, L, coef):
    """別の個体の残差の書き換えの道（起動器と同じ `use_cache=False` で呼ぶ）。順伝播の数を数える。"""
    sub = collections.OrderedDict((nm, dbr[nm]) for nm, _, _ in rows)
    RW_PASSES[0] += sum(1 + len(v) for v in sub.values())
    return RW.recompute_rewrite(model, tok, T3, FJ, [tuple(r) for r in rows], sub, dirs, L, coef, use_cache=False)


def part_model(iso_n, e2e_iso):
    import torch
    import bl3_run as BR
    import run_stageB_local as RB
    import direction_B
    import analyze_Bl3 as AZ
    import bl3_recompute_rewrite as RW
    from transformers import AutoTokenizer
    G2, G3 = '二', '三'
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(SNAP)
    model, cfg = tiny_model()
    L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
    coef = T3['layers']['coef_applied']
    seed = T3['readout']['primary']['order_seed']
    pair_names = list(DJ['groups']['real']['names'])
    swaps = T3['nulls']['real']['swap_siblings']
    names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])] + ['iso:%d' % i for i in range(iso_n)] + \
        ['real:' + p for p in pair_names] + ['check']
    dirs = synth_dirs(cfg.hidden_size, names)
    cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
    gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
    gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in gate_only})
    cells = BR.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
    # 乱数の模型の出口の行列を、読み取りの集合の文字が強く出るように置く（正本の閾値は変えずに、下見を本の計算まで通すため・合成だけ）
    R0 = BR.Runner(model, T3, L, coef, dirs)
    calibrate_readout_rows(model, R0, cells[cell_keys[0]], FJ)
    R = runner(BR.Runner(model, T3, L, coef, dirs))
    check(G2, '升目の入力が転記行 B と一致する（実のトークナイザ）', True, '%d 升目' % len(cells))
    # 書き出しの割り方が変わる場合（器が止まるか）
    FJx = copy.deepcopy(FJ)
    FJx['facts']['A']['prefix_ids'] = FJ['facts']['A']['prefix_ids'][:-1]
    check(G2, '書き出しの割り方が変わる場合（器が止まる）', raises(lambda: BR.build_cells(tok, T3, FJx, cell_keys[:1]), BR.ToolError), '書き出しを一トークン欠いた入力で、転記行 B との突き合わせが止めた')
    # 下見（正本の値のまま・乱数の模型・揺れの版は起動器と同じく境の確かめを通ったもの）
    stage_b_rate = {k: FJ['facts']['B']['cells'][k]['catastrophe'] / FJ['facts']['B']['cells'][k]['n_ok'] for k in cell_keys}
    variants = collections.OrderedDict((k, v['ids']) for k, v in FJ['facts']['A']['variants'].items() if v.get('boundary_ok'))
    pilot = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
    dec = pilot['decision']
    check(G2, '下見が機械の決定まで走る', 'q1' in dec and 'vi' in pilot and ('batch' in pilot or dec.get('stop')),
          'q1 %s・(vi) (a) %.2e (b) %.2e・バッチ %s・揺れの床 %s・近道の許容 %s・(v) の近道 %s（記述）' % (dec.get('q1'), pilot['vi']['decision']['spread_a'], pilot['vi']['decision']['spread_b'],
                                                                             pilot.get('batch'), pilot.get('floor'), pilot.get('cache_tol'), (pilot.get('v') or {}).get('shortcut')))
    check(G2, '出口の値の自己検査（下見の頭）', pilot['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (pilot['logit_check']['max_abs'], pilot['logit_check']['tol']))
    if dec.get('stop'):
        return {'pilot': pilot, 'n_forward': sum(r.n_forward for r in RUNNERS), 'seconds': round(time.time() - t0, 1), 'iso_n': iso_n, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}
    batch, tol, floor = pilot['batch'], pilot['cache_tol'], pilot['floor']
    tol2 = tol + floor                                                   # 二段目の許容（近道の許容と揺れの床の和・集計の器と同じ式）
    # 本の計算（起動器が呼ぶ `run_main_phase` をそのまま通す: 頭の自己検査〔出口の値・最後の層〕→ 全ての升目と符号・近道を使わない）
    items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in T3['cell_signs_main']]
    names_ = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])],
              'iso': ['iso:%d' % i for i in range(iso_n)], 'real': ['real:' + p for p in pair_names]}
    sets_run = BR.cell_sign_sets(T3, None, names_['named'], names_['B_random'], names_['iso'], names_['real'], gate_only)
    pc_calls, fwd = [0], collections.Counter()
    full_len = {len(c.ids) for c in cells.values()}
    orig_pc = R.prefix_cache
    R.prefix_cache = lambda c: (pc_calls.__setitem__(0, pc_calls[0] + 1), orig_pc(c))[1]

    def pre_kw(m, args, kwargs):
        ids_ = kwargs.get('input_ids') if kwargs.get('input_ids') is not None else (args[0] if args else None)
        fwd['n'] += 1
        fwd['past'] += int(kwargs.get('past_key_values') is not None)
        fwd['use_cache'] += int(kwargs.get('use_cache') is not False)          # 渡さない（模型の設定の既定）回も数える（裁定 D239・器の直しの確かめ C1-新10）
        fwd['short'] += int(ids_ is None or int(ids_.shape[-1]) not in full_len)
    hk_ = model.register_forward_pre_hook(pre_kw, with_kwargs=True)
    try:
        MP = BR.run_main_phase(R, T3, FJ, cells, names_, pilot, iso_n=None, log=lambda s: None)
    finally:
        hk_.remove()
        R.prefix_cache = orig_pc
    hd = MP['head']
    check(G2, '本の計算の頭の出口の値の自己検査', hd['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (hd['logit_check']['max_abs'], hd['logit_check']['tol']))
    check(G2, '本の計算は近道を使わない（振る舞い: 近道の元を作る呼び出し・使い回す cache・use_cache・列の全長を全ての順伝播で数えた・裁定 D236）',
          fwd['n'] > 0 and pc_calls[0] == 0 and fwd['past'] == 0 and fwd['use_cache'] == 0 and fwd['short'] == 0,
          '順伝播 %d 回・近道の元を作った回 %d・cache を渡した回 %d・use_cache が偽でない回 %d・列の全長でない回 %d' % (fwd['n'], pc_calls[0], fwd['past'], fwd['use_cache'], fwd['short']))
    check(G2, '本の計算は近道を使わない（頭の近道の確かめを走らせない・下見の (v) は記述・裁定 D234）',
          MP['shortcut'] is False and hd.get('shortcut') is False and 'steered_cache_check' not in hd and 'shortcut_rule' in hd,
          '下見の (v) の近道の決定 %s・(v) の差の最大 %.2e（近道の許容 %.4f）' % (pilot['v']['shortcut'], max(abs(x) for x in pilot['v']['diffs'].values()), tol))
    lc = hd['layer_check']
    check(G2, '最後の層の自己検査', lc['pass'], '差 %.2e（許容 %s）' % (lc['diff'], lc['tol']))
    outs = MP['cells']
    ok_keys = list(outs) == [s[0] for s in sets_run] and all(set(o['lo']) == set(s[3]) | {K.NOOP} for s, o in zip(sets_run, outs.values()))
    check(G2, '本の計算: 全ての升目と符号・全ての方向と無操作がそろい、埋めた零のベクトルの値は使わない', ok_keys, '升目と符号 %d（組み立て %d）' % (len(outs), len(sets_run)))
    # 層ごとの差分の余弦は足した向き（符号を掛けた方向）と測る（裁定 D231）: 減算の升目と符号でも、選んだ層の次の層の static の余弦が正
    cs = {k: outs[k]['layers']['rows']['static'][0][1] for k in ('S1|O-Ncold|-1', 'S1|O-Ncold|+1')}
    check(G2, '層ごとの差分の余弦を足した向き（符号を掛けた方向）と測る（減算の升目と符号でも正・裁定 D231）', all(c > 0 for c in cs.values()),
          '選んだ層の次の層の static の余弦: 減算 %.3f・加算 %.3f' % (cs['S1|O-Ncold|-1'], cs['S1|O-Ncold|+1']))
    # 零のベクトルの行（同じ升目と符号をもう一度・零のベクトルを一本足して・近道なし）
    kz = [i for i, s in enumerate(sets_run) if s[0] == 'S1|O-Ncold|-1'][0]
    key_z, ck_z, sg_z, ds_z = sets_run[kz]
    oz = BR.run_cell_sign(R, cells[ck_z], sg_z, list(ds_z) + ['zero:test'], batch, seed, kz, pc=None)
    zt = oz['effects']['zero:test']
    dmx = max(abs(oz['effects'][d] - outs[key_z]['effects'][d]) for d in outs[key_z]['effects'])
    check(G2, '零のベクトルの行は無操作と同じ値になる（別のバッチでも）', abs(zt) <= max(floor, 1e-6), '効き目 %.2e（揺れの床 %.2e）・バッチの組を変えた同じ方向の効き目の差の最大 %.2e（記述）' % (zt, floor, dmx))
    dirs['nan:test'] = np.full(cfg.hidden_size, np.nan)
    msg_nan = err_of(lambda: BR.run_cell_sign(R, cells[ck_z], sg_z, ['nan:test', 'static'], batch, seed, kz, pc=None), BR.ToolError)
    del dirs['nan:test']
    check(G2, '有限でない値の効き目は器の誤りで止まる（走らせる器の出口・裁定 D236）', msg_nan is not None and '有限でない値' in msg_nan, (msg_nan or '')[:70])
    # バッチの中の位置で方向を取り違えない
    c0, sg0 = items[0]
    r1 = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, full=False)
    r2 = R.forward(c0, ['td', 'Nk', K.NOOP, 'static'], sg0, full=False)
    e1 = {d: float(r1['lo'][i] - r1['lo'][0]) for i, d in enumerate([K.NOOP, 'static', 'Nk', 'td'])}
    e2 = {d: float(r2['lo'][i] - r2['lo'][2]) for i, d in enumerate(['td', 'Nk', K.NOOP, 'static'])}
    dpos = max(abs(e1[d] - e2[d]) for d in ('static', 'Nk', 'td'))
    check(G2, 'バッチの中の位置で方向を取り違えない', dpos <= max(floor, 1e-6) and max(abs(e1[d]) for d in ('static', 'Nk', 'td')) > 1e-3, '位置を入れ替えた効き目の差の最大 %.2e' % dpos)
    # （記述）近道ありと近道なし（効き目・同じバッチの大きさ）: 近道は下見の (v) の記述だけに使う
    pc0 = R.prefix_cache(c0)
    rs = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, pc=pc0, full=False)
    ds_ = max(abs(float((rs['lo'][i] - rs['lo'][0]) - (r1['lo'][i] - r1['lo'][0]))) for i in (1, 2, 3))
    check(G2, '（記述）近道ありと近道なしの効き目の差（近道は下見の (v) の記述だけ・本の計算は使わない・裁定 D234）', True, '差の最大 %.2e（近道の許容 %.4f）' % (ds_, tol))
    # 層ごとの差分の記述
    main_keys = {'%s|%s|%+d' % (a_, b_, s_) for a_, b_, s_ in T3['cell_signs_main']}
    lay_ok = all((o['layers']['iso_summary'] is not None and o['layers']['iso_summary']['n'] == iso_n and len(o['layers']['rows']) == 7 and
                  all(len(v) == len(R.after) for v in o['layers']['rows'].values())) if k in main_keys else
                 (o['layers']['iso_summary'] is None and not o['layers']['rows']) for k, o in outs.items())
    summ = outs['S1|O-Ncold|-1']['layers']['iso_summary']
    check(G2, '層ごとの差分（主の組だけ・名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間だけ）', lay_ok,
          '層 %d・等方 %d 本・主の組の升目と符号 %d' % (len(R.after), summ['n'] if summ else 0, sum(1 for k in outs if k in main_keys)))
    # 独立の再計算の組と、二つの道（本の器のフック・別の個体の残差の書き換え〔起動器と同じ use_cache=False〕・近道なし・バッチ一）
    st_rows = [r for r in T3['main_rows'] if r['direction'] == 'static']
    v_rows = [[r for r in st_rows if r['sign'] < 0][0], [r for r in st_rows if r['sign'] > 0][0]]      # 減算の行と加算の行を一つずつ
    rows_all, dirs_all = K.recompute_set(T3['main_rows'], pair_names, swaps, iso_n, dec.get('dropped', []))
    comps = K.comparators_for('static', pair_names, swaps)
    hand = {r['id']: [('static', r['sign'])] + [('iso:%d' % i, r['sign']) for i in range(iso_n)] + [('real:' + p, r['sign']) for p in comps] + [('real:' + p, -r['sign']) for p in comps]
            for r in T3['main_rows'] if r['direction'] == 'static' and '%s|%s' % (r['scenario'], r['base']) not in set(dec.get('dropped', []))}
    n_pass_rc = sum(1 + len(v) for v in dirs_all.values())
    E_ = FJ['facts']['E']
    Kn_ = T3['nulls']['isotropic']['count']
    per_ok = all(1 + len(v) == E_['per_row_recompute'] - (Kn_ - iso_n) for v in dirs_all.values())
    rows_ok = dec.get('dropped') or 2 * len(rows_all) * E_['per_row_recompute'] == E_['passes_recompute']
    check(G2, '独立の再計算の組（v̂ の行ごとに無操作・v̂・等方の帰無・比べる相手の両方の向き・転記行 E と）', [x[0] for x in rows_all] == list(hand) and dict(dirs_all) == hand and per_ok and rows_ok,
          'v̂ の行 %d・行ごとの順伝播 %d（等方 %d 本のとき・転記行 E の行ごと %d は等方 %d 本）・一つの道の順伝播 %d' % (
              len(rows_all), 1 + len(next(iter(dirs_all.values()))), iso_n, E_['per_row_recompute'], Kn_, n_pass_rc))
    v_ids = [r['id'] for r in v_rows]
    hk = BR.recompute_hook_path(R, [(nm, cells[ck], s) for nm, ck, s in rows_all if nm in v_ids], dirs_all)
    rw = rewrite(RW, model, tok, [(nm, ck, s) for nm, ck, s in rows_all if nm in v_ids], dirs_all, dirs, L, coef)
    worst = 0.0
    for r in v_rows:
        key = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
        kk = '%s|%s|%+d' % (r['scenario'], r['base'], -r['sign'])
        for dk, e in hk[r['id']]['effects'].items():
            did, sg = dk.rsplit('|', 1)[0], int(dk.rsplit('|', 1)[1])
            m = outs[key if sg == r['sign'] else kk]['effects'][did]
            worst = max(worst, abs(m - e))
    check(G2, '（記述）二段目の本の道（近道なし・本のバッチ）とフック（バッチ一）の効き目の差の最大（判定は札の一致・裁定 D234）', True,
          '差の最大 %.2e（許容 %.4f・許容の%s）' % (worst, tol2, '内' if worst <= tol2 else '外'))
    # 集計の器を端から端まで（等方の本数だけ合成の本数にした正本の写しで・合成だけ）
    T3d = AZ.with_iso(T3, iso_n)
    AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
    rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
    fc = FJ['facts']['C']
    same_rows = sorted(r['name'] for r in rows_gate) == sorted(fc['style_share_pt'])
    style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
    check(G2, '門の行と様式の転位の行を段階 B の記録から作り直す（転記行 C と）', same_rows and len(rows_gate) == T3['gate']['rows_gate'] and sorted(style_rows) == sorted(fc['style_rows']),
          '門の行 %d・様式の転位の行 %d' % (len(rows_gate), len(style_rows)))
    v_hook, v_rw = {i: hk[i] for i in v_ids}, {i: rw[i] for i in v_ids}
    eff_all = {k: o['effects'] for k, o in outs.items()}
    AZr = AZ.analyze(T3d, FJ, outs, [pilot], pair_names, rows_gate, hook=v_hook, rewrite=v_rw, style_rows=style_rows, rows_subset=set(v_hook))
    AZfull = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, v_hook, v_rw, pilot)
    check(G2, '独立の再計算の行が欠ければ一致しない（本の計算の求め方）', not AZfull['second']['agree'] and AZfull['second'].get('reason') == 'keys' and not AZfull['agree'],
          '欠けた行 %d' % len(AZfull['second'].get('missing', [])))
    gate_keys = ('main', 'without_vhat', 'desc_without_vhat_loaded', 'desc_choice_a', 'desc_without_style')
    ok_az = len(AZr['rows']) == len(T3['main_rows']) and all(k in AZr['gates'] for k in gate_keys) and list(AZr['predictions_truth']) == [it['key'] for it in T3['predictions']['items']]
    check(G2, '集計の器が主の札・門・記述の門・予想の答えを出す', ok_az,
          '行 %d・本の門の入れ替え %s・v̂ を抜いた門 %s・予想の答え %s' % (len(AZr['rows']), AZr['gates']['main'].get('n_perm'), AZr['gates']['without_vhat'].get('n_perm'), dict(AZr['predictions_truth'])))
    rc_ = AZr['recompute']
    check(G2, '集計の器の二段の一致（一段目は無操作の値と効き目の値と札・裁定 D233・二段目は札・裁定 D234）', rc_['first']['agree'] and rc_['second']['agree'] and rc_['agree'],
          '一段目 %s（無操作の値と効き目の差の最大 %.2e・許容 %s）・二段目 %s（効き目の差の最大 %.2e・許容 %.4f・許容の%s・記録）' % (
              rc_['first']['agree'], rc_['first']['max_abs_diff'], rc_['tol_first'], rc_['second']['agree'], rc_['second']['max_abs_diff'], rc_['tol_second'],
              '内' if rc_['second']['values_within_tol'] else '外'))
    # 二段目は札の一致で判定する（裁定 D234）: 値だけが許容の外（等方の帰無の端の一本を外へ動かし、裾の本数と順位の統計を変えない）なら一致して印を残し、札が変われば一致しない
    rid0, s0_ = v_rows[0]['id'], int(v_rows[0]['sign'])
    hk_a = copy.deepcopy(v_hook)
    Ea = hk_a[rid0]['effects']
    iso_keys = ['iso:%d|%+d' % (i, s0_) for i in range(iso_n)]
    iso_vals = [Ea[k] for k in iso_keys]
    if Ea['static|%+d' % s0_] >= float(np.median(iso_vals)):
        Ea[iso_keys[int(np.argmin(iso_vals))]] -= tol2 + 0.01
    else:
        Ea[iso_keys[int(np.argmax(iso_vals))]] += tol2 + 0.01
    ag_a = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, hk_a, None, pilot, rows_subset=set(hk_a))['second']
    lab_main = AZr['rows'][rid0]['second']
    hk_b = copy.deepcopy(v_hook)
    hk_b[rid0]['effects']['static|%+d' % s0_] = lab_main['center'] if lab_main['top'] else lab_main['center'] + 1e3
    ag_b = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, hk_b, None, pilot, rows_subset=set(hk_b))['second']
    check(G2, '二段目は札の一致で判定する（値だけが許容の外なら一致して印を残す・札が変われば一致しない・裁定 D234）',
          ag_a['agree'] and ag_a['values_beyond_tol'] and not ag_a['values_within_tol'] and not ag_b['agree'] and not ag_b['labels_same'],
          '等方の帰無の端の一本を %.4f 動かした（許容 %.4f）→ 一致 %s・許容の外の印 %s／二つ目の札の最上位を変えた → 一致 %s' % (
              tol2 + 0.01, tol2, ag_a['agree'], ag_a['values_beyond_tol'], ag_b['agree']))
    # 一段目は無操作の値も比べる（裁定 D233）: 書き換えの道の無操作の値だけをずらすと一致しない（効き目は同じ）
    tol1 = T3['independent_recompute']['tol_stage1']
    rw_c = copy.deepcopy(v_rw)
    rw_c[rid0]['noop_lo'] += tol1 + 1e-3
    ag_c = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, v_hook, rw_c, pilot, rows_subset=set(v_hook))
    check(G2, '一段目は無操作の値も比べる（書き換えの道の無操作の値だけをずらすと一致しない・裁定 D233）', not ag_c['first']['agree'] and ag_c['second']['agree'],
          'ずらした量 %.4f（一段目の許容 %s）→ 一段目の一致 %s・差の最大 %.2e' % (tol1 + 1e-3, tol1, ag_c['first']['agree'], ag_c['first']['max_abs_diff']))
    # 乙（裁定 D227）: B-lens の層二の文脈で、門の行の符号で流す
    FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
    CB = json.load(open(os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json'), encoding='utf-8'))['magnitude']['letter']
    sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
    same_rows = all(sorted(n for n, _, _ in sec_rows.get(cell, [])) == sorted(CB[cell]['rows']) for cell in CB)
    check(G2, '乙の行が B-lens の層二の答えの文字の位置の行と同じ（裁定 D227）', same_rows and set(sec_rows) == set(CB), '升目 %d・行 %d' % (len(sec_rows), sum(len(v) for v in sec_rows.values())))
    ctx_all = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
    pick = [c for c in ctx_all if c[0] == 'S1|O-Ncold|prose'][:1] + [c for c in ctx_all if c[0] == 'S4|Osec-Ncold|json'][:1]
    sec = BR.run_secondary(R, pick, sec_rows)
    ok_sec = len(ctx_all) == sum(len(v) for v in FB['facts']['E']['selected'].values()) and all(set(s['rows']) == {n for n, _, _ in sec_rows[pick[i][2].key]} for i, s in enumerate(sec)) and \
        sec[0]['n_batches'] == len({sg for _, _, sg in sec_rows[pick[0][2].key]})
    cnt = AZ.secondary_counts(FB, sec_rows)
    check(G2, '乙を流せる（文脈を組み・行の符号ごとに無操作と同じバッチ）', ok_sec, '文脈 %d（流したのは %d）・乙の行の順伝播 %d・符号のバッチ %d' % (len(ctx_all), len(pick), cnt['row_passes'], cnt['sign_batches']))
    E2 = FJ['facts']['E']
    check(G2, '乙の順伝播の数が転記行 E と同じ（集計の器の数え方と、設計事実の器の転記行 C の門の行からの数え方）',
          (cnt['row_passes'], cnt['sign_batches'], cnt['contexts']) == (E2['passes_secondary'], E2['batches_secondary'], E2['contexts_secondary']),
          '集計の器 %d・%d・%d／転記行 E %d・%d・%d' % (cnt['row_passes'], cnt['sign_batches'], cnt['contexts'], E2['passes_secondary'], E2['batches_secondary'], E2['contexts_secondary']))
    summ2 = AZ.secondary_summary(sec, CB)
    check(G2, '乙のまとめに B-lens の直接の経路の値を並べる', all(v.get('blens_direct') is not None for v in summ2.values()), '行 %d' % len(summ2))
    # ---- 端から端まで（作った下見の記録の分かれ道・意見伺いの C1-C1・C2-A4・起動器の出力と同じ JSON の往復・等方は e2e_iso 本）
    import sweep_Bl3 as SW
    import build_report_Bl3 as BRP
    import transformers
    sess = {'commit': 'dry-e2e', 'dry': True, 'gpu': 'cpu', 'versions': {'numpy': np.__version__, 'torch': torch.__version__, 'transformers': transformers.__version__},
            'canon_sha16': sha16f(os.path.join(REPO, 'design', 'contrasts-Bl3.json')), 'directions_npz_sha256': DJ['npz_sha256'], 'layer_idx': L, 'coef': coef, 'finished': 'dry-e2e'}
    sec_part = rt({'part': 'secondary', 'rows_by_cell': sec_rows, 'counts': cnt, 'contexts': sec})
    preds = {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '一部の升目を外して続ける'}}
    meta_ = {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}
    names_e = dict(names_, iso=names_['iso'][:e2e_iso])
    sets_e = BR.cell_sign_sets(T3, None, names_e['named'], names_e['B_random'], names_e['iso'], names_e['real'], gate_only)

    def e2e(pilot_e):
        """作った下見の記録で、起動器の相 main の三つの組の出力を作り、手元の一致だけを見る段・結果を開く段・掃き出し・報告の組み立て・走査まで通す。
        組の置き場の session は DRY の形（等方を減らすため・裁定 D236 で DRY でない形は等方が正本の本数でなければ止まる）で、独立の再計算は下見で外した升目の行を除く
        v̂ の行のすべてを流す。結果を開く段は、一致だけを見る段が読んだ出力の同定と照らしてから開く（裁定 D236）。"""
        pilot_e = rt(pilot_e)
        MPe = BR.run_main_phase(R, T3, FJ, cells, names_e, pilot_e, iso_n=None, log=lambda s: None)
        rows_e, dbr_e = K.recompute_set(T3['main_rows'], pair_names, swaps, len(names_e['iso']), MPe['dropped'])
        hook_e = BR.recompute_hook_path(R, [(n, cells[ck], s) for n, ck, s in rows_e], dbr_e)
        rw_e = rewrite(RW, model, tok, rows_e, dbr_e, dirs, L, coef)
        parts = collections.OrderedDict([('main', rt(dict(MPe, part='main'))), ('recompute', rt({'part': 'recompute', 'rows': rows_e, 'n_iso': len(names_e['iso']), 'hook': hook_e, 'rewrite': rw_e})),
                                         ('secondary', sec_part)])
        sessions = collections.OrderedDict((p, dict(sess)) for p in parts)
        files = collections.OrderedDict((p_, {'dir': 'e2e', 'json_sha256': hashlib.sha256(json.dumps(v_, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest().upper(),
                                              'session_sha256': 'dry'}) for p_, v_ in parts.items())
        J = AZ.judge(T3, parts, sessions, [pilot_e], pair_names, files)
        A = rt(AZ.open_checked(T3, FJ, parts, sessions, files, J, [pilot_e], pair_names, AN, CB, FB))
        bad_files = copy.deepcopy(files)
        bad_files['main']['json_sha256'] = '0' * 64
        bind_stop = err_of(lambda: AZ.open_checked(T3, FJ, parts, sessions, bad_files, J, [pilot_e], pair_names, AN, CB, FB), SystemExit)
        miss = SW.sweep(T3, A)
        text = BRP.build(T3, A, preds, meta_, [], None, '起草者の行（合成）')
        V, _ = BRP.lint_report(text, T3)
        return {'MP': MPe, 'rows': rows_e, 'J': J, 'A': A, 'miss': miss, 'text': text, 'V': V, 'pilot': pilot_e, 'bind_stop': bind_stop}
    # 分かれ道一: 主の升目 N1|O-Ncold と門の行だけの升目を (i)(ii) で外した下見の記録（正本の決定の関数で作る）
    drop_cells = ['N1|O-Ncold'] + gate_only_cells[:1]
    pilot_d = copy.deepcopy(pilot)
    pilot_d['decision'] = K.cells_decision({c: c not in drop_cells for c in cell_keys}, {c: c not in drop_cells for c in gate_only_cells}, T3['pilot']['decision']['cells_min_pass'])
    for c in drop_cells:
        pilot_d['cells'][c]['pass_i_ii'] = False
    ED = e2e(pilot_d)
    Ad = ED['A']
    dset = set(drop_cells)
    dropped_rows = [r['id'] for r in T3['main_rows'] if '%s|%s' % (r['scenario'], r['base']) in dset]
    left_static = [r['id'] for r in T3['main_rows'] if r['direction'] == 'static' and r['id'] not in dropped_rows]
    tag_d = '端から端まで・外した升目（主の升目 N1|O-Ncold と門の行だけの升目 %s）' % gate_only_cells[0]
    check(G2, tag_d + ': 本の計算と独立の再計算は外した升目の組と行を流さない',
          list(ED['MP']['cells']) == [s[0] for s in sets_e if s[1] not in dset] and [x[0] for x in ED['rows']] == left_static and ED['pilot']['decision']['q1'] == '一部の升目を外して続ける',
          '升目と符号 %d（外す前 %d）・独立の再計算の v̂ の行 %d・下見の決定 %s（外した升目 %s）' % (len(ED['MP']['cells']), len(sets_e), len(ED['rows']), ED['pilot']['decision']['q1'],
                                                                              '・'.join(ED['pilot']['decision']['dropped'])))
    check(G2, tag_d + ': 結果を開く段は、一致だけを見る段が読んだ出力と違う出力を開かない（裁定 D236）', ED['bind_stop'] is not None and '読んだ出力と違う' in ED['bind_stop'],
          (ED['bind_stop'] or '')[:70])
    check(G2, tag_d + ': 一致だけを見る段が二段とも一致', ED['J']['agree'] and ED['J']['first'] and ED['J']['second'],
          '一段目 %s・二段目 %s・二段目の値 %s' % (ED['J']['first'], ED['J']['second'], '許容の内' if ED['J'].get('second_values_within_tol') else '許容の外'))
    n_gate_left = sum(1 for r in rows_gate if r['cell'] not in dset)
    by_left = dict(collections.Counter(r['direction'] for r in T3['main_rows'] if r['id'] not in dropped_rows))
    gm = Ad['gates']['main']
    check(G2, tag_d + ': 札の行・Holm の段・門の行・偶然の目安を残った行で数え直す',
          Ad['rows_meta']['m_rows'] == len(T3['main_rows']) - len(dropped_rows) and Ad['rows_meta']['dropped_rows'] == dropped_rows and gm['n_rows'] == n_gate_left and
          Ad['chance']['rows_by_direction'] == by_left and Ad['chance']['oriented'] < Ad['chance']['canon_all_rows']['oriented'],
          'Holm の段 %d・外した行 %d・本の門の行 %d（段階 B の門の行 %d）・偶然の目安 向き %.4f（外す前 %.4f）' % (
              Ad['rows_meta']['m_rows'], len(Ad['rows_meta']['dropped_rows']), gm['n_rows'], len(rows_gate), Ad['chance']['oriented'], Ad['chance']['canon_all_rows']['oriented']))
    check(G2, tag_d + ': 掃き出しに欠けが無く、報告が組めて走査の違反が無い', ED['miss'] == [] and ED['V'] == [] and '〈下見で一部を外した〉' in ED['text'],
          '欠け %d・走査の違反 %d・報告 %d 行' % (len(ED['miss']), len(ED['V']), ED['text'].count(NL) + 1))
    # 分かれ道二: バッチ一（(vi) の (a) が上限を超えたときの決定〔バッチ一・揺れの床は (b)〕だけを写しで作り、下見の残りの段は走らせる器のまま）
    orig_vi = K.vi_decision
    K.vi_decision = lambda sa, sb, nm, bd: (lambda d: d if d['stop'] else dict(d, batch=1, floor=float(sb)))(orig_vi(sa, sb, nm, bd))
    try:
        pilot_1 = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
    finally:
        K.vi_decision = orig_vi
    check(G2, '下見のバッチ一の枝（(vi) の決定だけをバッチ一にした写し）が機械の決定まで走る', pilot_1.get('batch') == 1 and pilot_1.get('floor') == pilot_1['vi']['decision']['spread_b'] and
          all(k in pilot_1 for k in ('iii', 'iv', 'v', 'decision')),
          'バッチ %s・揺れの床 %.2e・近道の許容 %.4f・(v) の近道 %s（記述）・決定 %s' % (pilot_1.get('batch'), pilot_1.get('floor'), pilot_1.get('cache_tol'), pilot_1['v']['shortcut'], pilot_1['decision']['q1']))
    EB = e2e(pilot_1)
    Ab = EB['A']
    nb_ok = len(EB['MP']['cells']) == len(sets_e) and all(o['n_batches'] == len(s[3]) + 1 for s, o in zip(sets_e, EB['MP']['cells'].values()))
    s2b = Ab['recompute']['second']
    check(G2, '端から端まで・バッチ一: 本の計算は方向ごとに一つのバッチで流し、二段目の二つの道は同じ計算になる（差が零・正本 `independent_recompute.stages.second.note`）',
          EB['MP']['batch'] == 1 and nb_ok and s2b['max_abs_diff'] == 0.0, 'バッチ %s・升目と符号 %d・二段目の効き目の差の最大 %.2e' % (EB['MP']['batch'], len(EB['MP']['cells']), s2b['max_abs_diff']))
    check(G2, '端から端まで・バッチ一: 一致だけを見る段が二段とも一致', EB['J']['agree'] and EB['J']['first'] and EB['J']['second'],
          '一段目 %s・二段目 %s・独立の再計算の v̂ の行 %d' % (EB['J']['first'], EB['J']['second'], len(EB['rows'])))
    check(G2, '端から端まで・バッチ一: 掃き出しに欠けが無く、報告が組めて走査の違反が無い', EB['miss'] == [] and EB['V'] == [] and Ab['main_run']['batch'] == 1,
          '欠け %d・走査の違反 %d・報告 %d 行' % (len(EB['miss']), len(EB['V']), EB['text'].count(NL) + 1))
    # 三. 壊した読み取りと近道の元
    Rd = runner(BR.Runner(model, T3, L, coef, dirs, bug='double_norm'))
    ld = Rd.logit_check(c0, T3['computation']['logit_tol'])
    check(G3, '二重の正規化の読み取りを、出口の値の自己検査が止める', not ld['pass'], '差の最大 %.3f（許容 %s）' % (ld['max_abs'], ld['tol']))
    first = None
    try:
        BR.run_pilot(Rd, [cells[k] for k in cell_keys[:1]], [], T3, {}, stage_b_rate, T3['inputs']['sampling_B'])
    except BR.ToolError as e_:
        first = {'tool_error': str(e_)}
    check(G3, '壊した読み取りで下見が器の誤りとして止まる（やり直しの流れの一度目）', first is not None, (first or {}).get('tool_error', '')[:60])
    Rb = runner(BR.Runner(model, T3, L, coef, dirs, bug='cache_through_mp'))
    check(G3, '主位置まで使い回す近道を、凍結した確かめ（assert）が止める（下見の (v) の近道）', raises(lambda: Rb.forward(c0, [K.NOOP, 'static'], sg0, pc=Rb.prefix_cache(c0), full=False), BR.ToolError),
          '近道の元が主位置の手前で切れていない')
    pcl = dict(Rb.prefix_cache(c0), end=c0.mp)             # 主位置まで使い回した元に、主位置の手前で切ったと偽った切れ目を付ける
    msg = err_of(lambda: R.forward(c0, [K.NOOP, 'static'], sg0, pc=pcl, full=False), BR.ToolError)
    RB.assert_no_hooks(model, L)
    check(G3, '記録した切れ目を偽った近道の元を、使い回す cache の列の実の長さの確かめが止める（裁定 D231）', msg is not None and '使い回す cache の列の長さ' in msg, (msg or '')[:70])
    # 効き目で比べる確かめだけでは弱いこと（主位置の一つ分の加減の寄与の大きさ・記述）
    V = np.stack([np.zeros(cfg.hidden_size, dtype=np.float32), dirs['static'].astype(np.float32)])
    vals = []
    for st in (c0.mp, c0.mp + 1):
        h_ = RB.register_hook(model, L, RB.make_hook(V, coef, sg0, [st, st]))
        cap = {}
        hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
        with torch.no_grad():
            model(input_ids=torch.tensor([c0.ids] * 2), logits_to_keep=1)
        h_.remove(); hh.remove()
        ro = R.readout(cap['h'], c0, full=False)
        vals.append(float(ro['lo'][1] - ro['lo'][0]))
    check(G3, '（記述）主位置の一つ分の加減の寄与（効き目で比べる確かめの強さの目安）', True, '主位置から %.4f・主位置の次から %.4f・差 %.2e（近道の許容 %.4f）' % (vals[0], vals[1], vals[0] - vals[1], tol))
    # （記述）本物の相対の加減の大きさに合わせた合成の方向で、突き合わせの力を測り直す（独立の再計算の個体の開発の記録の勧め）。
    # 小さな模型では合成の方向のノルムが選んだ層の出力より二桁ほど大きく、効き目が飽和して、係数の二度掛けなどの誤りが一段目の許容の内に収まった。
    # 方向を ‖v‖＝正本 `layers.vhat_over_h` の選んだ層の値 × 選んだ層の出力の主位置のノルム にそろえ、個体の器の変種（`bl3_recompute_rewrite._mutant_diffs`・中は変えない）と
    # 主位置の一つ分の加減の寄与と、二段目の本の道とフックの差（意見伺いの C2-3.2）を測る。判定に入れない（合成の模型の上の目安）。
    rw_rows = [(r['id'], '%s|%s' % (r['scenario'], r['base']), int(r['sign'])) for r in v_rows]
    capL = {}
    hL = direction_B.decoder_layers(model)[L].register_forward_hook(lambda m, i, o: capL.__setitem__('h', (o[0] if isinstance(o, tuple) else o).detach().clone()))
    with torch.no_grad():
        model(input_ids=torch.tensor([cells[rw_rows[0][1]].ids]), logits_to_keep=1)
    hL.remove()
    RB.assert_no_hooks(model, L)
    nh = float(capL['h'][0, cells[rw_rows[0][1]].mp].float().norm())
    ratio = float(T3['layers']['vhat_over_h'][str(T3['layers']['selected_ratio'])])
    first_real = 'real:' + pair_names[0]
    scale = ratio * nh / float(np.linalg.norm(dirs['static']))
    dirs_s = collections.OrderedDict((k, v * scale) for k, v in dirs.items() if k in ('static', 'iso:0', 'iso:1', first_real))
    Rs = runner(BR.Runner(model, T3, L, coef, dirs_s))
    dbr_s = {nm: [('static', s), ('iso:0', s), ('iso:1', s), (first_real, 1), (first_real, -1)] for nm, _, s in rw_rows}
    hk_s = BR.recompute_hook_path(Rs, [(nm, cells[ck], s) for nm, ck, s in rw_rows], dbr_s)
    M_s = RW._mutant_diffs(model, tok, T3, FJ, rw_rows, dirs_s, first_real, L, coef, hk_s)
    emax = max(abs(e) for v in hk_s.values() for e in v['effects'].values())
    check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、書き換えの道の変種とフックの道の差（一段目の許容と比べる・判定に入れない）', True,
          '‖v‖／‖選んだ層の出力‖ %.4f・効き目の絶対値の最大 %.2e・%s（許容 %s）' % (ratio, emax, '・'.join('%s %.2e%s' % (k, d, '（許容の外）' if d > tol1 else '') for k, _, d, _ in M_s), tol1))
    V2 = np.stack([np.zeros(cfg.hidden_size, dtype=np.float32), dirs_s['static'].astype(np.float32)])
    vals_s = []
    for st in (c0.mp, c0.mp + 1):
        h_ = RB.register_hook(model, L, RB.make_hook(V2, coef, sg0, [st, st]))
        cap = {}
        hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
        with torch.no_grad():
            model(input_ids=torch.tensor([c0.ids] * 2), logits_to_keep=1)
        h_.remove(); hh.remove()
        ro = R.readout(cap['h'], c0, full=False)
        vals_s.append(float(ro['lo'][1] - ro['lo'][0]))
    check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、主位置の一つ分の加減の寄与（判定に入れない）', True,
          '主位置から %.3e・主位置の次から %.3e・差 %.2e（近道の許容 %.4f・一段目の許容 %s）' % (vals_s[0], vals_s[1], vals_s[0] - vals_s[1], tol, tol1))
    # 二段目の本の道（近道なし・本のバッチの組み方）とフック（バッチ一）の差と、近道ありの本の道との比べ（全ての方向を同じ倍率で小さくした合成の方向・v̂ の二つの行の升目と符号）
    dirs_S = collections.OrderedDict((k, v * scale) for k, v in dirs.items())
    RS = runner(BR.Runner(model, T3, L, coef, dirs_S))
    lines_S = []
    for r in v_rows:
        key = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
        ki = [i for i, s in enumerate(sets_run) if s[0] == key][0]
        _, ck, sg, ds = sets_run[ki]
        m_ = BR.run_cell_sign(RS, cells[ck], sg, ds, batch, seed, ki, pc=None, layer_dirs=(), keep_iso_layers=False)
        s_ = BR.run_cell_sign(RS, cells[ck], sg, ds, batch, seed, ki, pc=RS.prefix_cache(cells[ck]), layer_dirs=(), keep_iso_layers=False)
        hdirs = [('static', sg)] + [(d, sg) for d in names_['iso']] + [('real:' + p, sg) for p in comps]
        h_S = BR.recompute_hook_path(RS, [(r['id'], cells[ck], sg)], {r['id']: hdirs})[r['id']]
        dm = [abs(m_['effects'][d] - h_S['effects']['%s|%+d' % (d, s)]) for d, s in hdirs]
        dsh = [abs(s_['effects'][d] - h_S['effects']['%s|%+d' % (d, s)]) for d, s in hdirs]
        lines_S.append('%s: 近道なしの本の道とフックの差の最大 %.2e（許容の外 %d／%d）・近道ありの本の道とフックの差の最大 %.2e（許容の外 %d／%d）・無操作の近道ありとなしの差 %.2e・効き目の絶対値の最大 %.2e' % (
            key, max(dm), sum(x > tol2 for x in dm), len(dm), max(dsh), sum(x > tol2 for x in dsh), len(dsh), s_['lo'][K.NOOP] - m_['lo'][K.NOOP], max(abs(x) for x in h_S['effects'].values())))
    check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、二段目の本の道とフックの差・近道ありの本の道との比べ（判定に入れない・二段目の許容 %.4f・意見伺いの C2-3.2）' % tol2, True, '／'.join(lines_S))
    return {'pilot': pilot, 'pilot_batch1': pilot_1, 'n_forward': sum(r.n_forward for r in RUNNERS), 'rewrite_passes': RW_PASSES[0], 'seconds': round(time.time() - t0, 1),
            'iso_n': iso_n, 'e2e_iso': e2e_iso, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size,
            'MP': MP, 'sec_part': sec_part, 'L': L, 'coef': coef}                   # 六（DRY でない枝）に渡す（本の計算の出力と乙の組・裁定 D239）


# ---------------- 四. 別の個体の書き換えの器の自己検査と --dry ----------------
def part_rewrite_tool():
    G = '四'
    dev = open(os.path.join(REPO, 'records', 'Bl3', 'tools', 'recompute-rewrite-dev-Bl3.md'), encoding='utf-8').read()
    m = re.search(r'`tools/bl3_recompute_rewrite\.py`（v1・SHA16 ([0-9A-F]{16})', dev)
    now16 = sha16f(os.path.join(HERE, 'bl3_recompute_rewrite.py'))
    check(G, '書き換えの器が個体の開発の記録の版のまま（中は変えない）', bool(m) and m.group(1) == now16, '開発の記録 %s・今 %s' % (m.group(1) if m else None, now16))
    outs = collections.OrderedDict()
    for flag in ('--selftest', '--dry'):
        t1 = time.time()
        r = subprocess.run([sys.executable, os.path.join(HERE, 'bl3_recompute_rewrite.py'), flag], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO,
                           env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        outs[flag] = {'returncode': r.returncode, 'stdout': r.stdout, 'stderr_tail': r.stderr[-1500:], 'seconds': round(time.time() - t1, 1)}
        check(G, '書き換えの器の %s が通る（今の本の器の上で）' % flag, r.returncode == 0, '終わりの値 %d・%.0f 秒・出力 %d 行' % (r.returncode, time.time() - t1, len(r.stdout.splitlines())))
    return outs


# ---------------- 五. 起動器の三つの相を DRY で別のプロセスとして（裁定 D236） ----------------
def part_boot(iso_n_boot):
    """起動器の相 check・pilot・main（三つの組）を DRY で別のプロセスとして走らせ、集計の器の CLI の一致だけを見る段と結果を開く段・掃き出しの CLI・報告の組み立てと走査に通す。
    一致だけを見る段の後に、組の出力の中身だけを変えた写し（置き場の名は同じ）で結果を開く段が止まることを確かめる。出力は一時の置き場に置き、終わりに消す。"""
    G = '五'
    import build_report_Bl3 as BRP
    import analyze_Bl3 as AZ
    td = tempfile.mkdtemp(prefix='dry-boot-')
    env = dict(os.environ, OP4B_DRY='1', OP4B_REPO_DIR=REPO, OP4B_OUT=td, OP4B_DRY_ISO=str(iso_n_boot), OP4B_DRY_SEC='2', OP4B_DRY_RC='2', PYTHONIOENCODING='utf-8')
    run = lambda cmd, extra=None: subprocess.run([sys.executable] + cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, env=dict(env, **(extra or {})))
    newest = lambda prefix: ([d for d in sorted(glob.glob(os.path.join(td, prefix + '-*'))) if os.path.isdir(d)] or [None])[-1]
    t1 = time.time()
    try:
        r_c = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'check'})
        dc = newest('check')
        CK = json.load(open(os.path.join(dc, 'check.json'), encoding='utf-8')) if r_c.returncode == 0 and dc else {}
        cells_ck = CK.get('cells') or {}
        check(G, '起動器の三つの相（DRY・別のプロセス）: 相 check は順伝播を呼ばずに終わり、呼ばれた数と升目のトークンの並びの SHA16 を書く',
              r_c.returncode == 0 and CK.get('forward_calls') == 0 and (CK.get('forward_guards') or 0) > 0 and bool(cells_ck) and all('ids_sha16' in v for v in cells_ck.values()),
              '終わりの値 %d・順伝播を呼んだ数 %s・守り %s・升目 %d' % (r_c.returncode, CK.get('forward_calls'), CK.get('forward_guards'), len(cells_ck)))
        # 守りの掛かった呼び出しを相 check の中に入れる（DRY に限る環境の変数・Exception で呑もうとする・裁定 D239・器の直しの確かめ C2-13）
        r_g = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'check', 'OP4B_DRY_GUARD_TEST': '1'})
        zs_g = sorted(glob.glob(os.path.join(td, 'check-*-stopped.zip')))
        out_g = r_g.stdout + r_g.stderr
        check(G, '起動器の三つの相（DRY・別のプロセス）: 相 check の中の守りの掛かった呼び出しを Exception で呑もうとしても、守りが止めて止めの zip を作る（裁定 D239）',
              r_g.returncode != 0 and bool(zs_g) and '相 check の守り' in out_g,
              '終わりの値 %d・止めの zip %d・印字 %s' % (r_g.returncode, len(zs_g), [l.strip() for l in out_g.split(NL) if '相 check の守り' in l][:1]))
        r_p = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'pilot'})
        dp = newest('pilot')
        pj = os.path.join(dp, 'pilot.json') if dp else ''
        r_m = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'main', 'OP4B_DRY_PILOT': pj}) if r_p.returncode == 0 else r_p
        dm = newest('main')
        S = json.load(open(os.path.join(dm, 'session.json'), encoding='utf-8')) if r_m.returncode == 0 and dm else {}
        tags = [z.get('tag') for z in S.get('zips') or []]
        check(G, '起動器の三つの相（DRY・別のプロセス）: 相 pilot と相 main が終わり、組ごとの出力の SHA-256 を session に書き、組ごとに zip を作る',
              r_p.returncode == 0 and r_m.returncode == 0 and set(S.get('part_sha256') or {}) == set(('main', 'recompute', 'secondary')) and all('part-%s' % x in tags for x in ('main', 'recompute', 'secondary')),
              '終わりの値 %d・%d・組の出力の SHA-256 %s・zip %s' % (r_p.returncode, r_m.returncode, sorted(S.get('part_sha256') or {}), tags))
        jr, ar = os.path.join(td, 'judge.json'), os.path.join(td, 'analysis.json')
        r_j = run(['tools/analyze_Bl3.py', 'judge', dm, '--pilot', pj, '--out', jr]) if dm else r_m
        r_o = run(['tools/analyze_Bl3.py', 'open', dm, '--pilot', pj, '--judge-record', jr, '--out', ar]) if r_j.returncode == 0 else r_j
        r_s = run(['tools/sweep_Bl3.py', ar]) if r_o.returncode == 0 else r_o
        A = json.load(open(ar, encoding='utf-8')) if r_o.returncode == 0 else None
        V = None
        if A:
            text = BRP.build(T3, A, {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '続ける'}}, {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}, [], None, '起草者の行（合成）')
            V, _ = BRP.lint_report(text, T3)
        check(G, '起動器の三つの相（DRY・別のプロセス）: 集計の器の CLI の一致だけを見る段・結果を開く段・掃き出しの CLI・報告の組み立てと走査が通る',
              r_j.returncode == 0 and r_o.returncode == 0 and r_s.returncode == 0 and V == [] and bool((A or {}).get('inputs')),
              '終わりの値 %d・%d・%d・走査の違反 %s・結果を開く段の記録に読んだ出力の同定 %s' % (r_j.returncode, r_o.returncode, r_s.returncode, None if V is None else len(V), bool((A or {}).get('inputs'))))
        stopped_ok, out_t, stopped_j, out_j = False, '', False, ''
        if dm and r_j.returncode == 0:
            t2 = os.path.join(td, 'tampered')
            os.makedirs(t2)
            dt = os.path.join(t2, os.path.basename(dm))                  # 置き場の名は同じにして、組の中身だけを変える
            shutil.copytree(dm, dt)
            Mt = json.load(open(os.path.join(dt, 'main.json'), encoding='utf-8'))
            k0 = next(iter(Mt['cells']))
            d0 = 'Nk' if 'Nk' in Mt['cells'][k0]['effects'] else next(iter(Mt['cells'][k0]['effects']))
            Mt['cells'][k0]['effects'][d0] += 1000.0
            json.dump(Mt, open(os.path.join(dt, 'main.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            # 一つ目: session はそのまま → 一致だけを見る段が、起動器が書いた組の SHA-256 と違うことで止まって書かない（裁定 D239）
            jt = os.path.join(td, 'judge-tampered.json')
            r_jt = run(['tools/analyze_Bl3.py', 'judge', dt, '--pilot', pj, '--out', jt])
            out_j = r_jt.stdout + r_jt.stderr
            stopped_j = r_jt.returncode != 0 and 'session に書いた値と違う' in out_j and not os.path.exists(jt)
            # 二つ目: session の組の SHA-256 もそろえて書き換える → 結果を開く段が、一致だけを見る段の読んだ出力と違うことで止まって書かない（裁定 D236）
            St = json.load(open(os.path.join(dt, 'session.json'), encoding='utf-8'))
            St['part_sha256']['main'] = AZ.sha256f(os.path.join(dt, 'main.json'))
            json.dump(St, open(os.path.join(dt, 'session.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            at = os.path.join(td, 'analysis-tampered.json')
            r_t = run(['tools/analyze_Bl3.py', 'open', dt, '--pilot', pj, '--judge-record', jr, '--out', at])
            out_t = r_t.stdout + r_t.stderr
            stopped_ok = r_t.returncode != 0 and '読んだ出力と違う' in out_t and not os.path.exists(at)
        check(G, '起動器の三つの相（DRY・別のプロセス）: 組の出力の中身を変えて session はそのままなら、一致だけを見る段が止まって書かない（組の SHA-256・裁定 D239）', stopped_j,
              ('・'.join([l.strip() for l in out_j.split(NL) if 'session に書いた値と違う' in l][:1]) or '止まらなかった'))
        check(G, '起動器の三つの相（DRY・別のプロセス）: 一致だけを見る段の後に組の出力と session をそろえて変えると、結果を開く段が止まって書かない（裁定 D236）', stopped_ok,
              ('・'.join([l.strip() for l in out_t.split(NL) if '読んだ出力と違う' in l][:1]) or '止まらなかった'))
    finally:
        shutil.rmtree(td, ignore_errors=True)
    return round(time.time() - t1, 1)


# ---------------- 六. DRY でない枝（一時の git の置き場・裁定 D239） ----------------
def part_nondry(info):
    """DRY でない枝を、一時の git の置き場（今の作業木を写した複製）で、器を別のプロセスとして走らせて確かめる（裁定 D239・器の直しの確かめ C1-新5・C2-14・C1 と C2 の条件）。
    凍結の本文の器と予想の書式の器を走らせて下見の前の凍結の確かめ（Colab の確かめを除く）に当て、下見の前の凍結の記録と封印の記録（合成）を置いてコミットし、
    下見の出力（二の段の下見の記録を DRY でない形の session で）で本の凍結の器を走らせてコミットする。相 main の三つの組の出力は、組を一つずつ走らせた形で DRY でない session と
    置く（本の計算の出力は二の段のもの・等方は正本の本数・独立の再計算の二つの道の値はそこから合成）。集計の器の CLI（一致だけを見る段・台帳の追記・結果を開く段）・掃き出し・
    報告の器の CLI を通し、止まるべき場合を確かめる。実の重みは読まない。一時の置き場は終わりに消す。戻り値: 秒。"""
    G = '六'
    import analyze_Bl3 as AZ
    import freeze_Bl3 as FZ
    import importlib.util
    t1 = time.time()
    td = tempfile.mkdtemp(prefix='dry-nondry-')
    CL = os.path.join(td, 'clone')
    CLAUSE_ = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
    base_env = {k: v for k, v in os.environ.items() if not k.startswith('OP4B_')}
    run_ = lambda args, cwd=None: subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=cwd, env=dict(base_env, PYTHONIOENCODING='utf-8'))
    py = lambda *a: run_([sys.executable] + list(a), cwd=CL)
    git = lambda *a: run_(['git', '-C', CL, '-c', 'user.name=dry-run', '-c', 'user.email=dry-run@invalid'] + list(a))
    say_ = lambda r: r.stdout + r.stderr
    line_ = lambda r, w: ([l.strip() for l in say_(r).split(NL) if w in l] or ['（印字に「%s」が無い）' % w])[0][:140]
    P_ = lambda rel: os.path.join(CL, *rel.split('/'))
    rd_ = lambda p: open(p, encoding='utf-8').read()
    wr_ = lambda p, t: open(p, 'w', encoding='utf-8', newline=NL).write(t)

    def set_json(path, fn):
        o_ = json.load(open(path, encoding='utf-8'))
        fn(o_)
        json.dump(o_, open(path, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1, default=jdefault)
    try:
        assert run_(['git', 'clone', '-q', '--shared', '--no-checkout', REPO, CL]).returncode == 0, 'git clone'
        assert git('checkout', '-q', 'HEAD').returncode == 0, 'git checkout'
        for d in ('tools', 'design', 'records/Bl3', 'records/reviews/Bl3', 'results/Bl3'):
            shutil.copytree(os.path.join(REPO, *d.split('/')), P_(d), dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
        # (一) 凍結の本文の器を端から端まで・予想の書式・下見の前の凍結の確かめ（Colab の確かめを除く）
        r_mf = py('tools/make_frozen_Bl3.py', '--words', '（合成の登録者の言葉）', '--commit', 'deadbeef', '--date', '2026-09-26 00:00')
        ftxt = rd_(P_('design/design-Bl3-FROZEN.md')) if os.path.exists(P_('design/design-Bl3-FROZEN.md')) else ''
        rec_line = ('原稿 `design/design-Bl3-FROZEN.src.md` SHA16 %s' % sha16f(P_('design/design-Bl3-FROZEN.src.md'))) if os.path.exists(P_('design/design-Bl3-FROZEN.src.md')) else '?'
        r_ck = py('tools/make_frozen_Bl3.py', '--check')
        local_ = [x for x in (td, td.replace('\\', '/'), os.path.expanduser('~'), os.path.expanduser('~').replace('\\', '/'), 'AppData', 'frozen-standin') if x in ftxt]
        check(G, 'DRY でない枝: 凍結の本文の器を一時の複製で端から端まで走らせ、組み立ての記録の行が凍結版の原稿を指し、手元の道筋が無く、組み直しが同じ（裁定 D239）',
              r_mf.returncode == 0 and r_ck.returncode == 0 and rec_line in ftxt and not local_,
              '組み立ての終わりの値 %d・組み直しの確かめの終わりの値 %d・記録の行が凍結版の原稿を指す %s・手元の道筋 %d' % (r_mf.returncode, r_ck.returncode, rec_line in ftxt, len(local_)))
        r_fm = py('tools/make_predictions_form_Bl3.py')
        r_co = py('tools/freeze_Bl3.py', 'prepilot', '--check-only')
        m_ = re.search(r'下見の前の凍結の確かめが外れた（止める・登録者に相談）: (\[.*\])', say_(r_co))
        co_bad = ast.literal_eval(m_.group(1)) if m_ else []
        other = [x for x in co_bad if not x.startswith('合成データの正式の記録')]
        check(G, 'DRY でない枝: 予想の書式を組み、下見の前の凍結の確かめ（Colab の確かめを除く）で凍結の本文と書式と正本と方向と器の自己検査が通る（外れは、取り直す前の合成データの正式の記録のものだけ）',
              r_fm.returncode == 0 and (r_co.returncode == 0 or (bool(m_) and not other)),
              '書式の終わりの値 %d・確かめの外れ %d（合成データの正式の記録の外の外れ %d%s）' % (r_fm.returncode, len(co_bad), len(other), ('・' + other[0][:60]) if other else ''))
        # (二) 下見の前の凍結の記録と封印の記録（合成）を置いてコミットする
        files_ = sorted({f for f in FZ.frozen_files(T3) + FZ.import_closure(FZ.TOOLS) if os.path.exists(P_(f))})
        fz = collections.OrderedDict((f, sha16f(P_(f))) for f in files_)
        FRp = P_('records/Bl3/FREEZE-RECORD-Bl3.json')
        json.dump({'kind': 'bl3_freeze_record', 'version': 'dry', 'stage': 'prepilot', 'frozen_jst': '（合成）', 'registrant_words': '（合成）', 'frozen_sha16': fz,
                   'directions_npz_sha256': DJ['npz_sha256'], 'deviation_rule': '（合成）', 'deviations': [], 'clause': CLAUSE_},
                  open(FRp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
        wr_(P_('records/Bl3/FREEZE-RECORD-Bl3.md'), '# （合成）下見の前の凍結の記録' + NL + NL + CLAUSE_ + NL)       # 本の凍結の器が読んで書き足す
        os.makedirs(P_('records/predictions'), exist_ok=True)
        pr_ = {}
        for role in ('coordinator', 'registrant'):
            rp_ = 'records/predictions/predictions-Bl3-%s.json' % role
            wr_(P_(rp_), json.dumps({'q1.pilot': '続ける', 'q4.gate': '通らない'}, ensure_ascii=False))
            pr_[role] = {'path': rp_, 'sha256': hashlib.sha256(open(P_(rp_), 'rb').read()).hexdigest().upper()}
        json.dump({'predictions': pr_, 'freeze_record_sha16': sha16f(FRp), 'clause': CLAUSE_}, open(P_('records/Bl3/sealing-record-Bl3.json'), 'w', encoding='utf-8', newline=NL),
                  ensure_ascii=False, indent=1)
        git('add', '-A')
        git('commit', '-q', '-m', 'dry: prepilot freeze and seal (synthetic)')
        C_a = git('rev-parse', 'HEAD').stdout.strip()
        # (三) 下見の出力（二の段の下見の記録・DRY でない形の session）で本の凍結の器を走らせ、コミットする
        pil = json.loads(json.dumps(info['pilot'], default=jdefault))
        canon16 = sha16f(P_('design/contrasts-Bl3.json'))
        vers = dict(T3['inputs']['versions_B'])
        pdir = os.path.join(td, 'pilot-1')
        os.makedirs(pdir)
        json.dump({'pilot': pil, 'variants_used': [], 'clause': CLAUSE_}, open(os.path.join(pdir, 'pilot.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
        json.dump({'kind': 'bl3_colab_pilot', 'boot': 'dry', 'commit': C_a, 'dry': False, 'gpu': 'NVIDIA L4（合成）', 'versions': vers, 'canon_sha16': canon16,
                   'directions_npz_sha256': DJ['npz_sha256'], 'frozen_check': {'checked': len(fz), 'skipped': [], 'bad': []}, 'finished': '2026-09-26T01:00:00+09:00'},
                  open(os.path.join(pdir, 'session.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
        r_mz = py('tools/freeze_Bl3.py', 'main', '--words', '（合成の本の凍結の言葉）', '--when', '2026-09-26 01:10', '--pilot', pdir)
        FR1 = json.load(open(FRp, encoding='utf-8'))
        git('add', '-A')
        git('commit', '-q', '-m', 'dry: main freeze (synthetic)')
        C_b = git('rev-parse', 'HEAD').stdout.strip()
        check(G, 'DRY でない枝: 本の凍結の器が、下見の試みのコミット・封印の記録の錨・凍結物の照らしを通って本の凍結を記す（台帳の行の数を記す・裁定 D239）',
              r_mz.returncode == 0 and 'main_freeze' in FR1 and FR1['main_freeze'].get('deviations_n') == 0 and FR1['main_freeze'].get('pilot') == pil,
              '終わりの値 %d・%s' % (r_mz.returncode, line_(r_mz, '本の凍結')))
        # (四) 相 main の三つの組の出力（組を一つずつ・DRY でない session）
        MP = info['MP']
        n_can = T3['nulls']['isotropic']['count']
        dropped = sorted((pil.get('decision') or {}).get('dropped', []))
        cells_ = json.loads(json.dumps(MP['cells'], default=jdefault))
        rng_p = np.random.default_rng(29)
        for o_ in cells_.values():                     # 等方を正本の本数にそろえる（二の段の等方を試しの走りで減らしたときだけ・合成の値）
            for v_ in [v for v in o_.values() if isinstance(v, dict) and 'iso:0' in v]:
                have = [d_ for d_ in v_ if d_.startswith('iso:')]
                vals = np.array([v_[d_] for d_ in have], dtype=float)
                for i_ in range(len(have), n_can):
                    v_['iso:%d' % i_] = float(rng_p.normal(vals.mean(), vals.std() + 1e-6))
            if (o_.get('layers') or {}).get('iso_summary'):
                o_['layers']['iso_summary']['n'] = n_can
        pair_names_ = list(DJ['groups']['real']['names'])
        rows_rc, dbr = K.recompute_set(T3['main_rows'], pair_names_, T3['nulls']['real']['swap_siblings'], n_can, dropped)

        def path_(noise):
            o2 = {}
            for nm_, ck_, s_ in rows_rc:
                sc_, b_ = ck_.split('|')
                o2[nm_] = {'noop_lo': float(cells_['%s|%s|%+d' % (sc_, b_, s_)]['lo'][K.NOOP]) + noise,
                           'effects': {'%s|%+d' % (d_, sg_): float(cells_['%s|%s|%+d' % (sc_, b_, sg_)]['effects'][d_]) + noise for d_, sg_ in dbr[nm_]}}
            return o2
        head_ = json.loads(json.dumps(MP['head'], default=jdefault))
        parts_ = collections.OrderedDict([
            ('main', {'part': 'main', 'clause': CLAUSE_, 'head': head_, 'cells': cells_, 'batch': pil['batch'], 'shortcut': False, 'dropped': dropped, 'n_forward': 0, 'n_forward_total': 0}),
            ('recompute', {'part': 'recompute', 'clause': CLAUSE_, 'logit_check': head_['logit_check'], 'rows': [list(r_) for r_ in rows_rc], 'n_iso': n_can,
                           'hook': path_(0.0), 'rewrite': path_(1e-7), 'n_forward': 0, 'n_forward_total': 0}),
            ('secondary', dict(json.loads(json.dumps(info['sec_part'], default=jdefault)), part='secondary', clause=CLAUSE_, logit_check=head_['logit_check']))])
        dirs_ = []
        for i_, (part_, obj_) in enumerate(parts_.items()):
            d_ = os.path.join(td, 'main-%s' % part_)
            os.makedirs(d_)
            jp_ = os.path.join(d_, '%s.json' % part_)
            json.dump(obj_, open(jp_, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1, default=jdefault)
            json.dump({'kind': 'bl3_colab_main', 'boot': 'dry', 'commit': C_b, 'dry': False, 'gpu': 'NVIDIA L4（合成）', 'versions': vers, 'weights_sha256': FJ['facts']['F']['sha256'],
                       'canon_sha16': canon16, 'directions_npz_sha256': DJ['npz_sha256'], 'frozen_check': {'checked': len(fz), 'skipped': [], 'bad': []},
                       'layer_idx': info['L'], 'coef': info['coef'],
                       'pilot_used': {'batch': pil['batch'], 'floor': pil['floor'], 'cache_tol': pil['cache_tol'], 'shortcut': (pil.get('v') or {}).get('shortcut'), 'dropped': dropped},
                       'parts': [part_], 'part_sha256': {part_: AZ.sha256f(jp_)}, 'finished': '2026-09-26T0%d:00:00+09:00' % (2 + i_)},
                      open(os.path.join(d_, 'session.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
            dirs_.append(d_)
        # (五) 正しい流れ: 台帳の一行 → 一致だけを見る段 → 台帳の追記 → 結果を開く段 → 掃き出し → 報告の器の CLI
        set_json(FRp, lambda o: o['deviations'].append({'no': '合成の一', 'kind': 'note', 'reason': '（合成）一致だけを見る段の前に記した行', 'tool_diffs': []}))
        r_j = py('tools/analyze_Bl3.py', 'judge', *dirs_)
        set_json(FRp, lambda o: o['deviations'].append({'no': '合成の二', 'kind': 'recompute_values', 'reason': '（合成）二段目の値だけが許容の外で札は同じ', 'tool_diffs': []}))
        r_o = py('tools/analyze_Bl3.py', 'open', *dirs_)
        r_s = py('tools/sweep_Bl3.py', 'records/Bl3/analysis-Bl3.json')
        rej = os.path.join(td, 'rejected.md')
        wr_(rej, '- 起草者の行（合成・数を打たない）' + NL)
        r_r = py('tools/build_report_Bl3.py', '--rejected', rej)
        check(G, 'DRY でない枝: 一致だけを見る段（等方は正本の本数・凍結の記録と手元の器・相 main が使った下見の記録・session のコミットの本の凍結）→ 台帳の追記 → 結果を開く段 → 掃き出し → 報告の器の CLI（走査の違反 0）が通る（裁定 D239）',
              r_j.returncode == 0 and '全体 一致' in say_(r_j) and r_o.returncode == 0 and r_s.returncode == 0 and r_r.returncode == 0 and '走査の違反 0' in say_(r_r),
              '終わりの値 判定 %d・開く %d・掃き出し %d・報告 %d・%s' % (r_j.returncode, r_o.returncode, r_s.returncode, r_r.returncode,
                                                               line_(r_r, '走査の違反') if r_r.returncode == 0 else line_(r_r if r_r.returncode else (r_o if r_o.returncode else r_j), '止')))
        FRbak = rd_(FRp)
        jr0 = P_('records/Bl3/judge-Bl3.json')

        def copy_dirs(tag, mutate):
            out_ = []
            for d_ in dirs_:
                d2 = os.path.join(td, tag, os.path.basename(d_))
                shutil.copytree(d_, d2)
                mutate(d2)
                out_.append(d2)
            return out_
        # (六) 書き換えで止まる: 組の JSON だけ → 判定・組と session をそろえて → 開く段・判定の記録 → 開く段
        tamper = lambda d2: set_json(os.path.join(d2, 'main.json'), lambda o: o['cells'][next(iter(o['cells']))]['effects'].__setitem__('static', 99.0)) if d2.endswith('main-main') else None

        def tamper_both(d2):
            if d2.endswith('main-main'):
                tamper(d2)
                set_json(os.path.join(d2, 'session.json'), lambda o: o['part_sha256'].__setitem__('main', AZ.sha256f(os.path.join(d2, 'main.json'))))
        da, db = copy_dirs('a', tamper), copy_dirs('b', tamper_both)
        r_a = py('tools/analyze_Bl3.py', 'judge', *da, '--out', os.path.join(td, 'j-a.json'))
        r_b = py('tools/analyze_Bl3.py', 'open', *db, '--judge-record', jr0, '--out', os.path.join(td, 'a-b.json'))
        jc = os.path.join(td, 'j-c.json')
        Jc = json.load(open(jr0, encoding='utf-8'))
        Jc['env']['diff'] = {'gpu': {'main': '（書き換えた）'}}
        json.dump(Jc, open(jc, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
        r_c = py('tools/analyze_Bl3.py', 'open', *dirs_, '--judge-record', jc, '--out', os.path.join(td, 'a-c.json'))
        check(G, 'DRY でない枝: 組の JSON だけを書き換えると一致だけを見る段が、組と session をそろえて書き換えると結果を開く段が、判定の記録を書き換えると結果を開く段が、止まって書かない（裁定 D236・D239）',
              r_a.returncode != 0 and 'session に書いた値と違う' in say_(r_a) and not os.path.exists(os.path.join(td, 'j-a.json')) and
              r_b.returncode != 0 and '読んだ出力と違う' in say_(r_b) and not os.path.exists(os.path.join(td, 'a-b.json')) and
              r_c.returncode != 0 and 'もう一度走らせた答えが、判定の記録と違う' in say_(r_c) and not os.path.exists(os.path.join(td, 'a-c.json')),
              '／'.join([line_(r_a, 'session に書いた値と違う'), line_(r_b, '読んだ出力と違う'), line_(r_c, 'もう一度走らせた答え')]))
        # (七) 凍結の記録の書き換えで止まる: 台帳の外・台帳の前の行
        set_json(FRp, lambda o: o['main_freeze'].__setitem__('frozen_jst', '（書き換えた）'))
        r_d1 = py('tools/analyze_Bl3.py', 'open', *dirs_, '--out', os.path.join(td, 'a-d1.json'))
        wr_(FRp, FRbak)
        set_json(FRp, lambda o: o['deviations'][0].__setitem__('reason', '（書き換えた前の行）'))
        r_d2 = py('tools/analyze_Bl3.py', 'open', *dirs_, '--out', os.path.join(td, 'a-d2.json'))
        wr_(FRp, FRbak)
        check(G, 'DRY でない枝: 一致だけを見る段の後に、凍結の記録の台帳の外を書き換えても、判定の時にあった台帳の行を書き換えても、結果を開く段が止まる（台帳は後ろに足すだけ・裁定 D239）',
              r_d1.returncode != 0 and '台帳の外' in say_(r_d1) and r_d2.returncode != 0 and '一致だけを見る段の時の行が変わった' in say_(r_d2),
              '／'.join([line_(r_d1, '台帳の外'), line_(r_d2, '一致だけを見る段の時の行')]))
        # (八) 器の変えと台帳: 台帳に無い変え → 止まる・記す → 通る・同じ器の二度の直し → 通る・台帳に無い三度目 → 止まる（起動器の版の照らしも同じ）
        spec_ = importlib.util.spec_from_file_location('boot_Bl3_nondry', P_('tools/colab/boot_Bl3.py'))
        BT = importlib.util.module_from_spec(spec_)
        spec_.loader.exec_module(BT)
        swp = P_('tools/sweep_Bl3.py')
        swp_bak = rd_(swp)
        mf_ = json.load(open(FRp, encoding='utf-8'))['main_freeze']
        b0 = mf_['frozen_sha16']['tools/sweep_Bl3.py']
        led_ = lambda b__, a__: set_json(FRp, lambda o: o['deviations'].append({'no': '合成の器', 'kind': 'tool_fix', 'reason': '（合成）', 'tool_diffs': [{'path': 'tools/sweep_Bl3.py', 'before': b__, 'after': a__}]}))
        vb_ = lambda: BT.verify_frozen(CL, mf_['frozen_sha16'], json.load(open(FRp, encoding='utf-8'))['deviations'][int(mf_.get('deviations_n') or 0):])[0]
        open(swp, 'a', encoding='utf-8', newline=NL).write('# 合成の直し（一）' + NL)
        s1 = sha16f(swp)
        r_e1, v_e1 = py('tools/analyze_Bl3.py', 'judge', *dirs_, '--out', os.path.join(td, 'j-e1.json')), vb_()
        led_(b0, s1)
        r_e2, v_e2 = py('tools/analyze_Bl3.py', 'judge', *dirs_, '--out', os.path.join(td, 'j-e2.json')), vb_()
        open(swp, 'a', encoding='utf-8', newline=NL).write('# 合成の直し（二）' + NL)
        s2 = sha16f(swp)
        led_(s1, s2)
        r_e3, v_e3 = py('tools/analyze_Bl3.py', 'judge', *dirs_, '--out', os.path.join(td, 'j-e3.json')), vb_()
        open(swp, 'a', encoding='utf-8', newline=NL).write('# 合成の直し（三・台帳に無い）' + NL)
        r_e4, v_e4 = py('tools/analyze_Bl3.py', 'judge', *dirs_, '--out', os.path.join(td, 'j-e4.json')), vb_()
        wr_(swp, swp_bak)
        wr_(FRp, FRbak)
        check(G, 'DRY でない枝: 器を変えると、台帳に無ければ一致だけを見る段と起動器の版の照らしが止まり、台帳に記せば通り、同じ器を二度直しても通り、台帳に無い三度目の変えで止まる（裁定 D239）',
              r_e1.returncode != 0 and bool(v_e1) and r_e2.returncode == 0 and not v_e2 and r_e3.returncode == 0 and not v_e3 and r_e4.returncode != 0 and bool(v_e4),
              '一致だけを見る段の終わりの値 %d・%d・%d・%d／起動器の版の照らしの外れ %d・%d・%d・%d' % (r_e1.returncode, r_e2.returncode, r_e3.returncode, r_e4.returncode,
                                                                          len(v_e1), len(v_e2), len(v_e3), len(v_e4)))
        # (九) 相 main が使った下見の記録の食い違い・session のコミットの本の凍結の食い違い
        dg = copy_dirs('g', lambda d2: set_json(os.path.join(d2, 'session.json'), lambda o: o['pilot_used'].__setitem__('dropped', ['N1|O-Ncold'])) if d2.endswith('main-main') else None)
        dh = copy_dirs('h', lambda d2: set_json(os.path.join(d2, 'session.json'), lambda o: o.__setitem__('commit', C_a)))
        r_g = py('tools/analyze_Bl3.py', 'judge', *dg, '--out', os.path.join(td, 'j-g.json'))
        r_h = py('tools/analyze_Bl3.py', 'judge', *dh, '--out', os.path.join(td, 'j-h.json'))
        check(G, 'DRY でない枝: 相 main が使った下見の記録が手元の本の凍結の下見と違うと、また session のコミットの凍結の記録の本の凍結が手元と違うと、一致だけを見る段が止まる（裁定 D239）',
              r_g.returncode != 0 and '相 main が使った下見の記録' in say_(r_g) and r_h.returncode != 0 and '手元の本の凍結と違う' in say_(r_h),
              '／'.join([line_(r_g, '相 main が使った下見の記録'), line_(r_h, '手元の本の凍結と違う')]))
        # (十) 報告の器の CLI: DRY の集計・一致だけを見る段の記録の欠け・封印の記録の書き換えで止まり、戻すと通る
        ap_ = P_('records/Bl3/analysis-Bl3.json')
        a_bak = rd_(ap_)
        set_json(ap_, lambda o: o.__setitem__('dry', True))
        r_r1 = py('tools/build_report_Bl3.py', '--rejected', rej, '--force')
        wr_(ap_, a_bak)
        j_bak = rd_(jr0)
        os.remove(jr0)
        r_r2 = py('tools/build_report_Bl3.py', '--rejected', rej, '--force')
        wr_(jr0, j_bak)
        sr_ = P_('records/Bl3/sealing-record-Bl3.json')
        s_bak = open(sr_, 'rb').read()
        open(sr_, 'wb').write(s_bak.rstrip() + b'\n\n')
        r_r3 = py('tools/build_report_Bl3.py', '--rejected', rej, '--force')
        open(sr_, 'wb').write(s_bak)
        r_r4 = py('tools/build_report_Bl3.py', '--rejected', rej, '--force')
        check(G, 'DRY でない枝: 報告の器の CLI は、DRY の集計・一致だけを見る段の記録の欠け・封印の記録の書き換え（公開したコミットの錨）で止まり、戻すと通る（裁定 D239）',
              r_r1.returncode != 0 and 'DRY の集計' in say_(r_r1) and r_r2.returncode != 0 and '一致だけを見る段の記録が無い' in say_(r_r2) and
              r_r3.returncode != 0 and '下見の試みのコミット' in say_(r_r3) and r_r4.returncode == 0,
              '／'.join([line_(r_r1, 'DRY の集計'), line_(r_r2, '一致だけを見る段の記録が無い'), line_(r_r3, '下見の試みのコミット'), '戻すと終わりの値 %d' % r_r4.returncode]))
    finally:
        shutil.rmtree(td, ignore_errors=True)
    return round(time.time() - t1, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--iso', type=int, default=T3['nulls']['isotropic']['count'])
    ap.add_argument('--e2e-iso', type=int, default=9, help='端から端までの分かれ道の等方の本数（既定 9）')
    ap.add_argument('--out', default=None, help='試しの走りの出力の置き場（既定は records/Bl3/dry-run-Bl3-<日付>.md）')
    a = ap.parse_args()
    day = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
    out = a.out or os.path.join(REPO, 'records', 'Bl3', 'dry-run-Bl3-%s.md' % day)
    if os.path.exists(out) and not a.force:
        raise SystemExit('既にある: %s' % out)
    t0 = time.time()
    sha_start = tool_shas()
    part_pure()
    info = part_model(a.iso, a.e2e_iso)
    rw_out = part_rewrite_tool()
    boot_s = part_boot(a.e2e_iso)
    nd_s = part_nondry(info)
    sha_end = tool_shas()
    check('四', '走らせた器と正本と設計事実と方向の記録が、走りの始めと終わりで同じ', sha_start == sha_end, '%d ファイル%s' % (
        len(sha_start), '' if sha_start == sha_end else '（変わった: %s）' % [k for k in sha_start if sha_start[k] != sha_end.get(k)]))
    n_ok = sum(1 for r in RESULTS if r[2])
    L_ = ['# B-lens 層三の合成データの確かめ（機械生成・`tools/dry_run_Bl3.py` %s・%s）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')), '',
          '- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 %s・次元 %s・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。' % (
              info.get('layers'), info.get('dim')),
          '- 等方の方向の本数: %d（正本 %d）。端から端までの分かれ道の等方の本数 %s（作った下見の記録で・起動器の出力と同じ JSON の往復）。' % (a.iso, T3['nulls']['isotropic']['count'], info.get('e2e_iso')),
          '- 順伝播: 走らせる器 %s 回・書き換えの道 %s 回（変種の計算と四・五・六の走りは数えない）・%.0f 秒（五の起動器の三つの相 %.0f 秒・等方 %s 本・六の DRY でない枝 %.0f 秒）。' % (
              info.get('n_forward'), info.get('rewrite_passes'), time.time() - t0, boot_s, a.e2e_iso, nd_s),
          '- 確かめ: %d のうち %d が期待どおり。' % (len(RESULTS), n_ok), '',
          '| 部 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|'] + [
          '| %s | %s | %s | %s |' % (g, n.replace('|', '｜'), '期待どおり' if ok else '**期待と違う**', d.replace('|', '｜')) for g, n, ok, d in RESULTS] + [
          '', '## 下見の記録（乱数の模型・値に意味は無い・経路の確かめ）', '', '```json',
          json.dumps({k: v for k, v in info['pilot'].items() if k in ('logit_check', 'vi', 'batch', 'floor', 'cache_tol', 'iii', 'v', 'decision')}, ensure_ascii=False, indent=1, default=float), '```', '']
    if info.get('pilot_batch1'):
        L_ += ['## 下見のバッチ一の枝の記録（(vi) の決定だけをバッチ一にした写し・値に意味は無い）', '', '```json',
               json.dumps({k: v for k, v in info['pilot_batch1'].items() if k in ('vi', 'batch', 'floor', 'cache_tol', 'v', 'decision')}, ensure_ascii=False, indent=1, default=float), '```', '']
    for flag, o in rw_out.items():
        L_ += ['## 四. 書き換えの器の %s の出力（終わりの値 %d・%.0f 秒・中は変えない器）' % (flag, o['returncode'], o['seconds']), '', '```text'] + o['stdout'].rstrip(NL).split(NL) + ['```', '']
    L_ += ['## 凍結する版の SHA16（この記録を取った作業木・改行を LF にそろえた SHA-256 の頭 16 桁・走りの始めと終わりで同じことを確かめた）', '',
           '- 器の一覧は凍結の器 `tools/freeze_Bl3.py` の `TOOLS` と、その import の閉包。下見の前の凍結の器が、この表を今の版と突き合わせる。', '',
           '| ファイル | SHA16 |', '|---|---|'] + ['| %s | %s |' % kv for kv in sha_start.items()] + [
           '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(L_))
    print('[dry_run_Bl3] wrote %s | %d/%d | %.0f s' % (os.path.relpath(out, REPO), n_ok, len(RESULTS), time.time() - t0))
    sys.exit(0 if n_ok == len(RESULTS) else 1)


if __name__ == '__main__':
    main()
