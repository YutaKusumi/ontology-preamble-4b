# -*- coding: utf-8 -*-
"""器の実装の検分の R1 の票の事実の主張を、検分の版（コミット 87ce664）の一次の実物で確かめる（枠 `frame-impl-Bl3.md` §2・票を読んだ後・採否の案の前）。
器と正本は検分の版を git から一時の置き場に取り出して読む（作業木の版に頼らない）。値は純粋な関数と乱数の小さな模型だけで出す（実の重みを読まない）。
出力: records/reviews/Bl3/impl/checks/verification-impl-r1-Bl3.{json,md}（既にあれば書かない）
用法: python records/reviews/Bl3/impl/checks/verify_impl_r1_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, io, sys, json, math, shutil, tarfile, tempfile, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
AT = '87ce664'
NL = chr(10)
OUT_J, OUT_M = os.path.join(HERE, 'verification-impl-r1-Bl3.json'), os.path.join(HERE, 'verification-impl-r1-Bl3.md')
assert not os.path.exists(OUT_J) and not os.path.exists(OUT_M), '既にある'
V = collections.OrderedDict()


def show(path):
    return subprocess.run(['git', 'show', '%s:%s' % (AT, path)], cwd=REPO, capture_output=True).stdout.decode('utf-8')


def lines(path, a, b):
    L = show(path).split(NL)
    return L[a - 1:b]


def rec(k, claim, ok, how, detail):
    V[k] = {'claim': claim, 'reproduced': ok, 'how': how, 'detail': detail}
    print('[verify_impl_r1] %s %s %s' % (k, '再現' if ok else ('一部' if ok is None else '再現せず'), detail[:160]), flush=True)


# ---- 検分の版を一時の置き場に取り出す（tools と、読む記録と正本と設計事実）
TD = tempfile.mkdtemp(prefix='verify-impl-r1-')
WT = os.path.join(TD, 'wt')
tarfile.open(fileobj=io.BytesIO(subprocess.run(['git', 'archive', '--format=tar', AT], cwd=REPO, capture_output=True, check=True).stdout)).extractall(WT)
for f in ('results/Bl3/directions-Bl3.json', 'results/Bl3/directions-Bl3.npz'):
    os.makedirs(os.path.dirname(os.path.join(WT, f)), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, f), os.path.join(WT, f))
sys.path.insert(0, os.path.join(WT, 'tools'))
try:
    import bl3_core as K
    import blens_core as C
    T3 = json.load(open(os.path.join(WT, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
    FJ = json.load(open(os.path.join(WT, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
    DJ = json.load(open(os.path.join(WT, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))

    # M1: 合成データの器の「本の計算は近道を使わない」は定数を見るだけ
    L1 = lines('tools/dry_run_Bl3.py', 340, 342)
    L2 = lines('tools/bl3_run.py', 435, 437)
    L3 = lines('tools/bl3_run.py', 452, 452)
    expr_ok = ("MP['shortcut'] is False" in L1[1] and "hd.get('shortcut') is False" in L1[1] and "'steered_cache_check' not in hd" in L1[1] and "'shortcut_rule' in hd" in L1[1])
    const_ok = ('shortcut = False' in L2[0] and "head['shortcut'] = shortcut" in L2[1]) and ('R.prefix_cache(cells[ck]) if shortcut else None' in L3[0])
    # 振る舞いの突き合わせ: 近道の口を「いつも近道を使う」に変えた写し（印の定数はそのまま）でも、確かめの式が真になるか（乱数の小さな模型・等方 1 本）
    src = show('tools/bl3_run.py')
    assert src.count('pc = R.prefix_cache(cells[ck]) if shortcut else None') == 1
    mut = src.replace('pc = R.prefix_cache(cells[ck]) if shortcut else None', 'pc = R.prefix_cache(cells[ck])')
    mp = os.path.join(TD, 'bl3_run_mutant.py')
    open(mp, 'w', encoding='utf-8', newline=NL).write(mut)
    import importlib.util
    spec = importlib.util.spec_from_file_location('bl3_run_mutant', mp)
    BRm = importlib.util.module_from_spec(spec)
    sys.modules['bl3_run_mutant'] = BRm
    spec.loader.exec_module(BRm)
    import dry_run_Bl3 as DR
    import direction_B
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(DR.SNAP)
    model, cfg = DR.tiny_model()
    Lx = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
    pair_names = list(DJ['groups']['real']['names'])
    nm = list(T3['directions']['named']) + ['rand:%d' % i for i in range(3)] + ['iso:0'] + ['real:' + p for p in pair_names] + ['check']
    dirs = DR.synth_dirs(cfg.hidden_size, nm)
    cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
    gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
    cells = BRm.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
    DR.calibrate_readout_rows(model, BRm.Runner(model, T3, Lx, T3['layers']['coef_applied'], dirs), cells[cell_keys[0]], FJ)
    Rm = BRm.Runner(model, T3, Lx, T3['layers']['coef_applied'], dirs)
    calls = [0]
    orig_pc = Rm.prefix_cache
    Rm.prefix_cache = lambda c: (calls.__setitem__(0, calls[0] + 1), orig_pc(c))[1]
    pilot = {'batch': 16, 'floor': 0.0, 'cache_tol': 0.005, 'v': {'shortcut': True, 'diffs': {}}, 'decision': {'dropped': []}}
    names_ = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(3)], 'iso': ['iso:0'], 'real': ['real:' + p for p in pair_names]}
    MP = BRm.run_main_phase(Rm, T3, FJ, cells, names_, pilot, iso_n=None, log=lambda s: None)
    hd = MP['head']
    check_expr = MP['shortcut'] is False and hd.get('shortcut') is False and 'steered_cache_check' not in hd and 'shortcut_rule' in hd
    rec('M1', '合成データの器の「本の計算は近道を使わない」の確かめは、器が書いた定数を見るだけで振る舞いを見ない', expr_ok and const_ok and check_expr and calls[0] > 0,
        '引かれた行の文を検分の版で読み、近道の口を「いつも近道」に変えた写し（印の定数はそのまま）で本の計算の全体を乱数の小さな模型で走らせた',
        '確かめの式の四つの項 %s・本の器の定数と近道の口 %s・写しで近道の元を作った回 %d・そのときの確かめの式 %s' % (expr_ok, const_ok, calls[0], check_expr))

    # m1: 非有限の値
    null = list(range(1999))
    pt = K.p_and_tail(float('nan'), null)
    h = K.holm(dict({'r%d' % i: 0.5 for i in range(1, 16)}, r0=pt['p']), 0.05)['r0']
    ag2 = K.agreement({'a': [0.0], 'b': [float('nan')]}, {'a': [0.0], 'b': [0.0]}, 0.001, {}, {})
    ag1 = K.agreement({'a': [float('nan')], 'b': [0.0]}, {'a': [0.0], 'b': [0.0]}, 0.001, {}, {})
    ok_m1 = pt['upper'] == 0 and pt['lower'] == 0 and pt['tail'] == 'tie' and h['pass'] and ag2['agree']
    rec('m1', '効き目が NaN のとき、割合は最小・裾は tie で Holm を通り、一致の関数は二つ目以降の鍵の NaN を読み飛ばして一致と答える', ok_m1,
        '芯の関数に NaN を与えた（検分の版）',
        'p_and_tail(NaN): p %s・上 %d・下 %d・裾 %s・Holm の判定 %s／二つ目の鍵に NaN の一致 %s（差の最大 %s）／一つ目の鍵に NaN の一致 %s（差の最大 %s）' % (
            pt['p'], pt['upper'], pt['lower'], pt['tail'], h['pass'], ag2['agree'], ag2['max_abs_diff'], ag1['agree'], ag1['max_abs_diff']))

    # m2: 一致の段と開く段が組の申告を信じる
    A = show('tools/analyze_Bl3.py').split(NL)
    grab = lambda pat: [i + 1 for i, l in enumerate(A) if re.search(pat, l)]
    dry_any = grab(r"dry = any\(s\.get\('dry'\) for s in sessions\.values\(\)\)")
    subset = grab(r"rows_subset=set\(rc\['hook'\]\) if dry else None")
    env_only = grab(r"def env_same")
    with_iso = grab(r"def with_iso")
    judge_stop = grab(r"if any\(out\['tool_error'\]\.values\(\)\) or not \{'main', 'recompute'\} <= set\(parts\)")
    env_in_judge = [i for i in grab(r"env_same\(sessions\)")]
    stop_on_env = any(re.search(r"env.*same.*raise|raise.*env", l) for l in A)
    rec('m2', '一致の段と開く段は、組の一つの DRY の印で全体を絞り、組 recompute の n_iso で正本を写し、組の間の環境の違いは記すだけで止めない', bool(dry_any and subset and env_only and with_iso) and not stop_on_env,
        '検分の版の集計の器の行を読んだ',
        'DRY の判定の行 %s・行を絞る行 %s・環境を記す関数 %s・等方の本数の写し %s・環境の違いで止める行 %s' % (dry_any, subset, env_only, with_iso, '有る' if stop_on_env else '無い'))

    # m3: 升目の入力の突き合わせは長さと位置と族だけ
    B = show('tools/bl3_run.py').split(NL)
    bc = [i + 1 for i, l in enumerate(B) if "(len(prompt), c.mp, c.ro, fam) != (b['prompt_len'], b['main_position'], b['readout_position'], b['family'])" in l]
    boot = show('tools/colab/boot_Bl3.py')
    want_line = [l for l in boot.split(NL) if l.strip().startswith('want = {')]
    tok_pinned = any('tokenizers' in l for l in want_line)
    factB_keys = sorted(next(iter(FJ['facts']['B']['cells'].values())).keys())
    rec('m3', '升目の入力の突き合わせは、プロンプトの長さ・主位置・読み取りの位置・族だけで、トークンの並びそのものは照らさない。起動器は tokenizers の版を固定しない', bool(bc) and not tok_pinned,
        '検分の版の走らせる器・起動器・転記行 B の欄を読んだ',
        '突き合わせの行 %s・起動器の固定の行 %s・転記行 B の升目の欄 %s' % (bc, [l.strip()[:90] for l in want_line], factB_keys))

    # m4: 純粋な確かめは芯の関数を直に呼ぶ（集計の器の組み立ては答えのある形で当てていない）
    D = show('tools/dry_run_Bl3.py').split(NL)
    kgate = [i + 1 for i, l in enumerate(D) if 'K.gate(' in l]
    cgate = [i + 1 for i, l in enumerate(D) if 'C.gate_perm(' in l]
    az_gates = [i + 1 for i, l in enumerate(D) if 'AZ.gates(' in l]
    az_rowlab = [i + 1 for i, l in enumerate(D) if 'AZ.row_labels(' in l]
    rec('m4', '純粋な確かめは K.gate と blens_core.gate_perm を直に呼び、集計の器の gates・row_labels の組み立てを答えのある形で当てない', bool(kgate and cgate) and not az_gates and not az_rowlab,
        '検分の版の合成データの器の呼び出しを数えた', 'K.gate の行 %s・gate_perm の行 %s・AZ.gates の直の呼び出し %s・AZ.row_labels の直の呼び出し %s' % (kgate, cgate, az_gates, az_rowlab))

    # m5: 合成の確かめの等方の本数では Holm の第一段を下回れない
    m_rows = len(T3['main_rows'])
    first = 0.05 / m_rows
    pmin = lambda n: min(1.0, 2.0 / (n + 1))
    real_min = [K.p_and_tail(1e9, list(range(n)))['p'] for n in (9, 199, T3['nulls']['isotropic']['count'])]
    rec('m5', '等方 9 本と 199 本では最小の p が Holm の第一段を下回れず、等方の外の行の枝に届かない', real_min[0] > first and real_min[1] > first and real_min[2] < first,
        '芯の関数で、帰無のどれよりも大きい値の p を等方の本数ごとに出した',
        'Holm の第一段 %.6f（主の行 %d）・最小の p: 等方 9 本 %.4f・199 本 %.4f・正本の本数 %.4f' % (first, m_rows, real_min[0], real_min[1], real_min[2]))

    # m6: 方向の名と npz の行を位置で結ぶ（名の並びを正本と転記行 D に照らさない）
    Bd = show('tools/bl3_directions.py')
    names_check = ("T3['directions']['named']" in show('tools/bl3_run.py').split('def load_dirs')[1].split('def ')[0])
    named_eq = DJ['groups']['named']['names'] == list(T3['directions']['named'])
    real_eq = DJ['groups']['real']['names'] == [p if isinstance(p, str) else p for p in (FJ['facts']['D'].get('real_pairs') or [])]
    rec('m6', '方向の記録の名の並びと npz の行を位置で結び、名の並びを正本と転記行 D に照らさない（今の結び付きは正しい）', (not names_check) and named_eq,
        '検分の版の load_dirs の中に正本の名の並びとの照らしがあるかを見て、今の名の並びを正本と転記行 D と比べた',
        'load_dirs の中の正本の名との照らし %s・名前のある方向の並びが正本と同じ %s・実在の差の並びが転記行 D と同じ %s' % ('有る' if names_check else '無い', named_eq, real_eq))
finally:
    shutil.rmtree(TD, ignore_errors=True)

json.dump({'version_under_review': AT, 'checks': V, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'},
          open(OUT_J, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
L = ['# 器の実装の検分の R1 の票の事実の主張の確かめ（機械生成・`verify_impl_r1_Bl3.py`・検分の版 %s）' % AT, '',
     '- 検分の版を git から一時の置き場に取り出して確かめた。値は芯の関数と乱数の小さな模型で出した（実の重みを読まない）。', '',
     '| 番号 | 主張 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|---|'] + [
     '| %s | %s | %s | %s | %s |' % (k, v['claim'], v['how'], '再現した' if v['reproduced'] else ('一部' if v['reproduced'] is None else '再現しない'), v['detail'].replace('|', '｜')) for k, v in V.items()] + [
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_M, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('[verify_impl_r1] wrote %s' % os.path.relpath(OUT_M, REPO))
