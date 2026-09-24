# -*- coding: utf-8 -*-
"""dry_run_Bl3.py v1 —— B-lens 層三（Bl3）の合成データの器（正本 `review_plan.synthetic` の形のすべてと、乱数の小さな模型で端から端まで・2026-09-25）。

一. 純粋な関数の形（`tools/bl3_core.py`・`tools/blens_core.py`）: 奇でない押し・零でない帰無の中心・減算の行・下見で外れる升目と門の行だけの升目・帰無との同じ値・
    両方の向きがちょうど対称な比べる相手・書き出しの割り方が変わる場合・掃き出し・端数のバッチ・零の近くの中央値・Holm の境で一本違う p・器の誤りでやり直す流れ。
二. 乱数の小さな模型（登録機種の設定を小さくした bf16 の模型・実の重みではない・正規化の重みを散らす・CPU）と実のトークナイザで、走らせる器 `tools/bl3_run.py` の
    下見と本の計算と独立の再計算のフックの道を端から端まで通す（bf16 の揺れ・近道の許容の式・二段目の一致）。
三. わざと壊した読み取り（二重の正規化）と近道（主位置まで使い回す）で、自己検査と凍結した確かめが止まることを確かめる。
**実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の方向は、実の方向の名だけを借りた乱数（次元は小さな模型のもの）。
出力: records/Bl3/dry-run-Bl3-<日付>.md（--force が無ければ上書きしない）
用法: python tools/dry_run_Bl3.py [--force] [--iso 本数（既定は正本の本数）]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, time, copy, argparse, datetime, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C
import bl3_core as K

VERSION = 'v1'
NL = chr(10)
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
RESULTS = []


def check(group, name, ok, detail=''):
    RESULTS.append((group, name, bool(ok), detail))
    print('[dry_run_Bl3] %s %-4s %s %s' % (group, 'OK' if ok else 'FAIL', name, detail), flush=True)


def raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    return False


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
    return sets


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


def part_model(sets, iso_n):
    import torch
    import bl3_run as BR
    import run_stageB_local as RB
    import direction_B
    from transformers import AutoTokenizer
    G2, G3 = '二', '三'
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(SNAP)
    model, cfg = tiny_model()
    L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
    names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])] + ['iso:%d' % i for i in range(iso_n)] + \
        ['real:' + p for p in DJ['groups']['real']['names']] + ['check']
    dirs = synth_dirs(cfg.hidden_size, names)
    cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
    gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
    cells = BR.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
    # 乱数の模型の出口の行列を、読み取りの集合の文字が強く出るように置く（正本の閾値は変えずに、下見を本の計算まで通すため・合成だけ）
    R0 = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs)
    c_cal = cells[cell_keys[0]]
    cap = {}
    hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
    with torch.no_grad():
        model(input_ids=torch.tensor([c_cal.ids]), logits_to_keep=1)
    hh.remove()
    m_ = R0.norm32(cap['h'])[0]
    m_ = m_ / m_.norm()
    set_all = sorted({int(x) for x in FJ['facts']['A']['letter_ids'].values()})
    gcal = torch.Generator().manual_seed(7)
    with torch.no_grad():
        for tkn in set_all:
            model.lm_head.weight[tkn] = (3.0 * m_ + 0.3 * torch.randn(m_.shape, generator=gcal)).to(model.lm_head.weight.dtype)
    R = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs)
    check(G2, '升目の入力が転記行 B と一致する（実のトークナイザ）', True, '%d 升目' % len(cells))
    # 書き出しの割り方が変わる場合（器が止まるか）
    FJx = copy.deepcopy(FJ)
    FJx['facts']['A']['prefix_ids'] = FJ['facts']['A']['prefix_ids'][:-1]
    check(G2, '書き出しの割り方が変わる場合（器が止まる）', raises(lambda: BR.build_cells(tok, T3, FJx, cell_keys[:1]), BR.ToolError), '書き出しを一トークン欠いた入力で、転記行 B との突き合わせが止めた')
    # 下見（正本の値のまま・乱数の模型）
    stage_b_rate = {k: FJ['facts']['B']['cells'][k]['catastrophe'] / FJ['facts']['B']['cells'][k]['n_ok'] for k in cell_keys}
    variants = {k: v['ids'] for k, v in FJ['facts']['A']['variants'].items()}
    pilot = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
    dec = pilot['decision']
    check(G2, '下見が機械の決定まで走る', 'q1' in dec and 'vi' in pilot and ('batch' in pilot or dec.get('stop')),
          'q1 %s・(vi) (a) %.2e (b) %.2e・バッチ %s・揺れの床 %s・近道の許容 %s・近道 %s' % (dec.get('q1'), pilot['vi']['decision']['spread_a'], pilot['vi']['decision']['spread_b'],
                                                            pilot.get('batch'), pilot.get('floor'), pilot.get('cache_tol'), (pilot.get('v') or {}).get('shortcut')))
    check(G2, '出口の値の自己検査（下見の頭）', pilot['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (pilot['logit_check']['max_abs'], pilot['logit_check']['tol']))
    if dec.get('stop'):
        return {'pilot': pilot, 'n_forward': R.n_forward, 'seconds': round(time.time() - t0, 1), 'iso_n': iso_n, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}
    batch, tol, floor = pilot['batch'], pilot['cache_tol'], pilot['floor']
    use_short = pilot['v']['shortcut']
    # 本の計算の頭: 近道の確かめ・最後の層の自己検査
    items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in T3['cell_signs_main']]
    sc_chk = BR.steered_cache_check(R, items, batch, tol)
    check(G2, '本の計算の頭の近道の確かめ（効き目で比べる）', sc_chk['shortcut'], '差の最大 %.2e（許容 %.4f）' % (sc_chk['max_abs'], tol))
    lc = R.layer_check(items[0][0], items[0][1], 'check', T3['computation']['layer_tol'])
    check(G2, '最後の層の自己検査', lc['pass'], '差 %.2e（許容 %s）' % (lc['diff'], lc['tol']))
    # 本の計算（全ての升目と符号）
    outs, want = {}, {}
    main_keys = {'%s|%s|%+d' % (a_, b_, s_) for a_, b_, s_ in T3['cell_signs_main']}
    for ki, (key, ck, sg, ds) in enumerate(sets):
        ds_ = [d for d in ds if not d.startswith('iso:') or int(d.split(':')[1]) < iso_n]
        if key == 'S1|O-Ncold|-1':
            ds_ = ds_ + ['zero:test']
        want[key] = set(ds_) | {K.NOOP}
        main_cs = key in main_keys
        pc = R.prefix_cache(cells[ck]) if use_short else None
        outs[key] = BR.run_cell_sign(R, cells[ck], sg, ds_, batch, T3['readout']['primary']['order_seed'], ki, pc=pc,
                                     layer_dirs=(list(T3['directions']['named']) + ['rand:0', 'rand:1', 'rand:2']) if main_cs else (), keep_iso_layers=main_cs)
    ok_keys = all(set(o['lo']) == want[k] for k, o in outs.items())
    check(G2, '本の計算: 全ての方向と無操作がそろい、埋めた零のベクトルの値は使わない', ok_keys, '升目と符号 %d' % len(outs))
    zt = outs['S1|O-Ncold|-1']['effects']['zero:test']
    check(G2, '零のベクトルの行は無操作と同じ値になる（別のバッチでも）', abs(zt) <= max(floor, 1e-6), '効き目 %.2e（揺れの床 %.2e）' % (zt, floor))
    # バッチの中の位置で方向を取り違えない
    c0, sg0 = items[0]
    r1 = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, full=False)
    r2 = R.forward(c0, ['td', 'Nk', K.NOOP, 'static'], sg0, full=False)
    e1 = {d: float(r1['lo'][i] - r1['lo'][0]) for i, d in enumerate([K.NOOP, 'static', 'Nk', 'td'])}
    e2 = {d: float(r2['lo'][i] - r2['lo'][2]) for i, d in enumerate(['td', 'Nk', K.NOOP, 'static'])}
    dpos = max(abs(e1[d] - e2[d]) for d in ('static', 'Nk', 'td'))
    check(G2, 'バッチの中の位置で方向を取り違えない', dpos <= max(floor, 1e-6) and max(abs(e1[d]) for d in ('static', 'Nk', 'td')) > 1e-3, '位置を入れ替えた効き目の差の最大 %.2e' % dpos)
    # 近道ありと近道なし（効き目・同じバッチの大きさ）
    pc0 = R.prefix_cache(c0)
    rs = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, pc=pc0, full=False)
    ds_ = max(abs(float((rs['lo'][i] - rs['lo'][0]) - (r1['lo'][i] - r1['lo'][0]))) for i in (1, 2, 3))
    check(G2, '近道ありと近道なしの効き目が許容の内で合う', ds_ <= tol, '差の最大 %.2e（許容 %.4f）' % (ds_, tol))
    # 層ごとの差分の記述
    summ = BR.layer_summary(outs['S1|O-Ncold|-1']['layers'], T3['descriptive']['layerwise']['band'])
    check(G2, '層ごとの差分（名前のある方向と段階 B の三本・等方の中央値と中央の区間）', summ is not None and summ['n'] == iso_n and len(outs['S1|O-Ncold|-1']['layers']['rows']) == 7,
          '層 %d・等方 %d 本' % (len(R.after), summ['n'] if summ else 0))
    # 独立の再計算のフックの道（近道なし・バッチ一）と本の道（二段目の一致）
    v_rows = [r for r in T3['main_rows'] if r['direction'] == 'static'][:2]
    rows_rc, dirs_rc = [], {}
    for r in v_rows:
        key = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
        comps = K.comparators_for('static', DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'])
        rows_rc.append((r['id'], cells['%s|%s' % (r['scenario'], r['base'])], r['sign']))
        dirs_rc[r['id']] = [('static', r['sign'])] + [('iso:%d' % i, r['sign']) for i in range(iso_n)] + [('real:' + p, r['sign']) for p in comps] + [('real:' + p, -r['sign']) for p in comps]
    hk = BR.recompute_hook_path(R, rows_rc, dirs_rc)
    worst = 0.0
    for r in v_rows:
        key = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
        kk = '%s|%s|%+d' % (r['scenario'], r['base'], -r['sign'])
        for dk, e in hk[r['id']]['effects'].items():
            did, sg = dk.rsplit('|', 1)[0], int(dk.rsplit('|', 1)[1])
            m = outs[key if sg == r['sign'] else kk]['effects'][did]
            worst = max(worst, abs(m - e))
    check(G2, '二段目（本の道とフック・近道なし・バッチ一）の効き目の差が「近道の許容＋揺れの床」の内', worst <= tol + floor, '差の最大 %.2e（許容 %.4f）' % (worst, tol + floor))
    ag_bad = K.agreement({'x': [0.0]}, {'x': [tol + floor + 0.01]}, tol + floor, {}, {})
    # 集計の器を端から端まで（等方の本数だけ合成の本数にした正本の写しで・合成だけ）
    import analyze_Bl3 as AZ
    T3d = copy.deepcopy(T3)
    T3d['nulls']['isotropic']['count'] = iso_n
    AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
    rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
    fc = FJ['facts']['C']
    same_rows = sorted(r['name'] for r in rows_gate) == sorted(fc['style_share_pt'])
    style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
    check(G2, '門の行と様式の転位の行を段階 B の記録から作り直す（転記行 C と）', same_rows and len(rows_gate) == T3['gate']['rows_gate'] and sorted(style_rows) == sorted(fc['style_rows']),
          '門の行 %d・様式の転位の行 %d' % (len(rows_gate), len(style_rows)))
    v_hook = {r['id']: hk[r['id']] for r in v_rows}
    AZr = AZ.analyze(T3d, FJ, outs, [pilot], DJ['groups']['real']['names'], rows_gate, hook=v_hook, rewrite=None, style_rows=style_rows, rows_subset=set(v_hook))
    AZfull = AZ.recompute_agreement(T3d, T3['main_rows'], {k: o['effects'] for k, o in outs.items()}, DJ['groups']['real']['names'], v_hook, None, pilot)
    check(G2, '独立の再計算の行が欠ければ一致しない（本の計算の求め方）', not AZfull['second']['agree'] and AZfull['second'].get('reason') == 'keys', '欠けた行 %d' % len(AZfull['second'].get('missing', [])))
    gate_keys = ('main', 'without_vhat', 'desc_without_vhat_loaded', 'desc_choice_a', 'desc_without_style')
    ok_az = len(AZr['rows']) == len(T3['main_rows']) and all(k in AZr['gates'] for k in gate_keys) and list(AZr['predictions_truth']) == [it['key'] for it in T3['predictions']['items']]
    check(G2, '集計の器が主の札・門・記述の門・予想の答えを出す', ok_az,
          '行 %d・本の門の入れ替え %s・v̂ を抜いた門 %s・予想の答え %s' % (len(AZr['rows']), AZr['gates']['main'].get('n_perm'), AZr['gates']['without_vhat'].get('n_perm'), dict(AZr['predictions_truth'])))
    check(G2, '集計の器の二段目の一致（合成・一段目は独立の再計算の器ができた後）', AZr['recompute']['second']['agree'] and AZr['recompute']['first'] is None and not AZr['recompute']['agree'],
          '二段目 %s（差の最大 %.2e・許容 %.4f）・一段目 まだ無い・全体の一致 %s' % (AZr['recompute']['second']['agree'], AZr['recompute']['second']['max_abs_diff'], AZr['recompute']['tol_second'], AZr['recompute']['agree']))
    check(G2, '二段目の許容を超える揺れを入れると一致しない', not ag_bad['agree'], '入れた差 %.4f' % (tol + floor + 0.01))
    # 三. 壊した読み取りと近道
    Rd = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs, bug='double_norm')
    ld = Rd.logit_check(c0, T3['computation']['logit_tol'])
    check(G3, '二重の正規化の読み取りを、出口の値の自己検査が止める', not ld['pass'], '差の最大 %.3f（許容 %s）' % (ld['max_abs'], ld['tol']))
    first = None
    try:
        BR.run_pilot(Rd, [cells[k] for k in cell_keys[:1]], [], T3, {}, stage_b_rate, T3['inputs']['sampling_B'])
    except BR.ToolError as e_:
        first = {'tool_error': str(e_)}
    check(G3, '壊した読み取りで下見が器の誤りとして止まる（やり直しの流れの一度目）', first is not None, (first or {}).get('tool_error', '')[:60])
    Rb = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs, bug='cache_through_mp')
    check(G3, '主位置まで使い回す近道を、凍結した確かめ（assert）が止める', raises(lambda: Rb.forward(c0, [K.NOOP, 'static'], sg0, pc=Rb.prefix_cache(c0), full=False), BR.ToolError), '近道の元が主位置の手前で切れていない')
    # 効き目で比べる確かめだけでは弱いこと（主位置の一つ分の加減の寄与の大きさ・記述）
    V = np.stack([np.zeros(cfg.hidden_size, dtype=np.float32), dirs['static'].astype(np.float32)])
    vals = []
    for st in (c0.mp, c0.mp + 1):
        h_ = RB.register_hook(model, L, RB.make_hook(V, T3['layers']['coef_applied'], sg0, [st, st]))
        cap = {}
        hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
        with torch.no_grad():
            model(input_ids=torch.tensor([c0.ids] * 2), logits_to_keep=1)
        h_.remove(); hh.remove()
        ro = R.readout(cap['h'], c0, full=False)
        vals.append(float(ro['lo'][1] - ro['lo'][0]))
    check(G3, '（記述）主位置の一つ分の加減の寄与（効き目で比べる確かめの強さの目安）', True, '主位置から %.4f・主位置の次から %.4f・差 %.2e（近道の許容 %.4f）' % (vals[0], vals[1], vals[0] - vals[1], tol))
    return {'pilot': pilot, 'n_forward': R.n_forward, 'seconds': round(time.time() - t0, 1), 'iso_n': iso_n, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--iso', type=int, default=T3['nulls']['isotropic']['count'])
    ap.add_argument('--out', default=None, help='試しの走りの出力の置き場（既定は records/Bl3/dry-run-Bl3-<日付>.md）')
    a = ap.parse_args()
    day = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
    out = a.out or os.path.join(REPO, 'records', 'Bl3', 'dry-run-Bl3-%s.md' % day)
    if os.path.exists(out) and not a.force:
        raise SystemExit('既にある: %s' % out)
    t0 = time.time()
    sets = part_pure()
    info = part_model(sets, a.iso)
    n_ok = sum(1 for r in RESULTS if r[2])
    L_ = ['# B-lens 層三の合成データの確かめ（機械生成・`tools/dry_run_Bl3.py` %s・%s）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')), '',
          '- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 %s・次元 %s・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。' % (
              info.get('layers'), info.get('dim')),
          '- 等方の方向の本数: %d（正本 %d）。順伝播 %s 回・%s 秒。' % (a.iso, T3['nulls']['isotropic']['count'], info.get('n_forward'), info.get('seconds')),
          '- 確かめ: %d のうち %d が期待どおり。' % (len(RESULTS), n_ok), '',
          '| 部 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|'] + [
          '| %s | %s | %s | %s |' % (g, n, '期待どおり' if ok else '**期待と違う**', d.replace('|', '｜')) for g, n, ok, d in RESULTS] + [
          '', '## 下見の記録（乱数の模型・値に意味は無い・経路の確かめ）', '', '```json', json.dumps({k: v for k, v in info['pilot'].items() if k in ('logit_check', 'vi', 'batch', 'floor', 'cache_tol', 'iii', 'v', 'decision')}, ensure_ascii=False, indent=1, default=float), '```', '',
          '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(L_))
    print('[dry_run_Bl3] wrote %s | %d/%d | %.0f s' % (os.path.relpath(out, REPO), n_ok, len(RESULTS), time.time() - t0))
    sys.exit(0 if n_ok == len(RESULTS) else 1)


if __name__ == '__main__':
    main()
