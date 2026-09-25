# -*- coding: utf-8 -*-
"""dry_run_Bl3.py v2 —— B-lens 層三（Bl3）の合成データの器（正本 `review_plan.synthetic` の形のすべてと、乱数の小さな模型で端から端まで・2026-09-25）。

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
記録の末尾に、走らせた器（凍結の器の一覧と import の閉包）と正本・設計事実・方向の記録の SHA16 を、走りの始めと終わりで同じことを確かめて並べる
（下見の前の凍結の器が今の版と突き合わせる）。
**実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の方向は、実の方向の名だけを借りた乱数（次元は小さな模型のもの）。
出力: records/Bl3/dry-run-Bl3-<日付>.md（--force が無ければ上書きしない）
用法: python tools/dry_run_Bl3.py [--force] [--iso 本数（既定は正本の本数）] [--e2e-iso 本数（既定 9）] [--out 置き場]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, math, time, copy, hashlib, argparse, datetime, subprocess, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C
import bl3_core as K

VERSION = 'v2'          # v2（2026-09-25・裁定 D231〜D234）: 本の計算は近道を使わない・二段の判定の形・下見の分かれ道を端から端まで・cache の長さの確かめ・書き換えの器の自己検査・版の SHA16
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
    MP = BR.run_main_phase(R, T3, FJ, cells, names_, pilot, iso_n=None, log=lambda s: None)
    hd = MP['head']
    check(G2, '本の計算の頭の出口の値の自己検査', hd['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (hd['logit_check']['max_abs'], hd['logit_check']['tol']))
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
    sess = {'commit': 'dry-e2e', 'dry': False, 'gpu': 'cpu', 'versions': {'numpy': np.__version__, 'torch': torch.__version__, 'transformers': transformers.__version__},
            'canon_sha16': sha16f(os.path.join(REPO, 'design', 'contrasts-Bl3.json')), 'directions_npz_sha256': DJ['npz_sha256'], 'layer_idx': L, 'coef': coef, 'finished': 'dry-e2e'}
    sec_part = rt({'part': 'secondary', 'rows_by_cell': sec_rows, 'counts': cnt, 'contexts': sec})
    preds = {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '一部の升目を外して続ける'}}
    meta_ = {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}
    names_e = dict(names_, iso=names_['iso'][:e2e_iso])
    sets_e = BR.cell_sign_sets(T3, None, names_e['named'], names_e['B_random'], names_e['iso'], names_e['real'], gate_only)

    def e2e(pilot_e):
        """作った下見の記録で、起動器の相 main の三つの組の出力を作り、手元の一致だけを見る段・結果を開く段・掃き出し・報告の組み立て・走査まで通す。
        組の置き場の session は DRY でない形にする（本の計算と同じく、下見で外した升目の行を除く v̂ の行のすべてを比べる）。"""
        pilot_e = rt(pilot_e)
        MPe = BR.run_main_phase(R, T3, FJ, cells, names_e, pilot_e, iso_n=None, log=lambda s: None)
        rows_e, dbr_e = K.recompute_set(T3['main_rows'], pair_names, swaps, len(names_e['iso']), MPe['dropped'])
        hook_e = BR.recompute_hook_path(R, [(n, cells[ck], s) for n, ck, s in rows_e], dbr_e)
        rw_e = rewrite(RW, model, tok, rows_e, dbr_e, dirs, L, coef)
        parts = collections.OrderedDict([('main', rt(dict(MPe, part='main'))), ('recompute', rt({'part': 'recompute', 'rows': rows_e, 'n_iso': len(names_e['iso']), 'hook': hook_e, 'rewrite': rw_e})),
                                         ('secondary', sec_part)])
        sessions = collections.OrderedDict((p, dict(sess)) for p in parts)
        J = AZ.judge(T3, parts, sessions, [pilot_e], pair_names)
        A = rt(AZ.open_results(T3, FJ, parts, sessions, [pilot_e], pair_names, AN, CB, FB))
        miss = SW.sweep(T3, A)
        text = BRP.build(T3, A, preds, meta_, [], None, '起草者の行（合成）')
        V, _ = BRP.lint_report(text, T3)
        return {'MP': MPe, 'rows': rows_e, 'J': J, 'A': A, 'miss': miss, 'text': text, 'V': V, 'pilot': pilot_e}
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
            'iso_n': iso_n, 'e2e_iso': e2e_iso, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}


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
    sha_end = tool_shas()
    check('四', '走らせた器と正本と設計事実と方向の記録が、走りの始めと終わりで同じ', sha_start == sha_end, '%d ファイル%s' % (
        len(sha_start), '' if sha_start == sha_end else '（変わった: %s）' % [k for k in sha_start if sha_start[k] != sha_end.get(k)]))
    n_ok = sum(1 for r in RESULTS if r[2])
    L_ = ['# B-lens 層三の合成データの確かめ（機械生成・`tools/dry_run_Bl3.py` %s・%s）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')), '',
          '- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 %s・次元 %s・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。' % (
              info.get('layers'), info.get('dim')),
          '- 等方の方向の本数: %d（正本 %d）。端から端までの分かれ道の等方の本数 %s（作った下見の記録で・起動器の出力と同じ JSON の往復）。' % (a.iso, T3['nulls']['isotropic']['count'], info.get('e2e_iso')),
          '- 順伝播: 走らせる器 %s 回・書き換えの道 %s 回（変種の計算と四の走りは数えない）・%.0f 秒。' % (info.get('n_forward'), info.get('rewrite_passes'), time.time() - t0),
          '- 確かめ: %d のうち %d が期待どおり。' % (len(RESULTS), n_ok), '',
          '| 部 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|'] + [
          '| %s | %s | %s | %s |' % (g, n, '期待どおり' if ok else '**期待と違う**', d.replace('|', '｜')) for g, n, ok, d in RESULTS] + [
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
