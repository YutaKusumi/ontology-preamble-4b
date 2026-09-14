# -*- coding: utf-8 -*-
"""synth_A.py v2 —— 段階 A の集計器（tools/analyze_A.py）の全経路を合成データ（人工の件数・推論なし）で発火させる検査（2026-09-13 整備・登録者裁定 D9 の三つ目の手順・採否表 P2）。
v2（2026-09-14・実装検分の採否表 P100・登録者裁定 D16・D20・D22）: 札の行 id に加えて、注の範囲・除外の範囲・refuse の理由を期待と突合し、refuse の理由 (a)(b)(d)・腕に選択的な配置・二つの場面の確証・
  片側の残存で β₃ が棄却される対比・様式 (a) の走を足した。器の写しに変異 M1〜M6 を一つずつ入れて、対応する走で期待との不一致が出ることを確かめる（変異を見分けない合成検査は検査にならない・W50）。
  集計器 v2 の入力（門0.5 と校正帯の記録・セッション記録・門の記録の撤退条件の判定と残る場面）に合わせた。
置き場: --root に results 相当の木を作る（リポジトリの results/ には置かない・既定で走ごとに消す）。
走 1〜12: refuse 門 × 様式門 × 環境保留の十二の組を全対比に一様に当てる（refuse は腕 X の refuse 率の推移・様式は腕 X の (b) 率・環境は橋の腕 X の率のずれ）。
  場面ごとに型を置く: N1＝解釈条項なし・p* 棄却（P_S）／N2＝解釈条項あり・p* 棄却（P_CS）／S1＝解釈条項なし・p* 非棄却（P_N）／S4＝解釈条項あり・p* 非棄却（P_C）／
  SK＝非有意・判定不能（両腕の床）・判定不能（非収束・合成検査の口）。腕 X＝各対比にちょうど一本ずつ入る腕。基の腕＝Onull・O-Ncold。
  走 1＝測定不能（SK の Odosehalf の大きい規模）・床持続の 0・撤退条件の器の異常／走 2＝錨帯（SK の 1.7B）・門0.5 不合格／走 3＝校正腕の器の異常（N1 の 4B）／走 4＝門0.5 合格と API 再走行／走 5＝錨帯（全場面の 4B）。
走 13: 門2 の縮小（残る場面は N1 だけ・残らない場面の対比だけ判定不能・登録者裁定 D16）。
走 14: refuse 門の理由（N1＝答えた分母で β₃ の符号が逆転〔a〕・N2＝答えた分母で名目有意を失う〔b〕・S1＝答えた分母の下限を満たす規模が足りない〔d〕）。
走 15: 腕に選択的な配置（refuse の推移は N・様式 (a) は Lneg・橋のずれは Odose1）・N1 と N2 の二つの場面の確証・片側の残存で β₃ が棄却される対比（N1 の Odosehalf を大きい規模で測定不能に）・
  校正腕の器の異常を N2 の 4B の走行に・対照どうしの差の定型（N2 の Onull-Ncold を下向きに）。
各走で集計器を実行し、対比ごとの札の全組合せ表の行 id・注の範囲（門0.5 不合格・校正腕と撤退条件の器の異常・残存規模の非連続）・除外の範囲（測定不能のセル・錨帯の除外単位・橋の帯を超えた腕・門2 の縮小の対比）・
refuse の理由を期待と突合する。走の和で五十二行すべての発火と、必要な経路の発火を assert する。
変異の検査（--mutations all|none|M1,M3）: M1 校正の注を全確証に／M2 門0.5 の注を全対比に／M3 片側の規則を外す／M4 refuse の理由を (c) だけに／M5 様式門の (a) を読まない／M6 門2 の縮小を全対比に。
出力: records/A/synth-A-<日付>.md と同 .json（--record で変更可）。合成の件数は検査のための人工値であり、いかなる読みにも用いない。
用法: python tools/synth_A.py --root <一時置き場> [--runs 1,13] [--mutations none] [--keep] [--facts <設計事実 JSON>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, shutil, subprocess, itertools, argparse, datetime, time
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import confirm_A
from zaxis_A import z_sizes
REPO = runs_A.REPO
VERSION = 'v2.1'   # v2.1（2026-09-14・凍結前の最終検分の採否表 P129・P134〜P137）: 期待の札（正本 stage2_first_match から組む）と期待の keep（配置から組む）を突合・変異 M7〜M10・門の記録に per_scenario・同じ向きの尺度依存の配置・記録の見出しと限界
ap = argparse.ArgumentParser()
ap.add_argument('--root', required=True); ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); ap.add_argument('--B-measurable', type=int, default=4)
ap.add_argument('--runs', default='all'); ap.add_argument('--keep', action='store_true'); ap.add_argument('--record', default=None); ap.add_argument('--mutations', default='all')
a = ap.parse_args()
ROOT = os.path.abspath(a.root)
assert ROOT != os.path.abspath(os.path.join(REPO, 'results')), '合成データを results に置かない'
T = runs_A.load_T(); SIZES = T['sizes']; SC = T['scenarios']; ARMS = T['arms']['preamble']; MID = runs_A.model_ids(T); S = T['seeds']
ANCHOR = next(m['key'] for m in T['models'] if m['anchor']); FAM = T['families']['A_slope']; CONTR = FAM['contrasts']; ALL_ROWS = [r['id'] for r in FAM['confirm_rule']['label_combo_table']]
BR = T['bridge']; PS = T['print_strings']; L = FAM['confirm_rule']['labels']; MIN_OK = FAM['refuse_gate']['answered_min_n_ok']
zs = np.array(z_sizes(SIZES)); zt = (zs - zs.min()) / (zs.max() - zs.min())
lin = lambda lo, hi: [float(lo + (hi - lo) * t) for t in zt]
const = lambda v: [v] * len(SIZES)
X_ARMS = ['N', 'Odose1', 'Odosehalf', 'Lneg', 'Onull-Ncold', 'Osec-Ncold']
TYPES = {
    'P_S': dict(n=200, clause=False, star=True, rates={'Onull': const(0.5), 'O-Ncold': const(0.5), 'Odose1': lin(0.2, 0.8), 'Odosehalf': lin(0.2, 0.8), 'Lneg': lin(0.2, 0.8),
                                                        'Onull-Ncold': lin(0.2, 0.8), 'N': lin(0.8, 0.2), 'Osec-Ncold': lin(0.8, 0.2)}),
    'P_CS': dict(n=200, clause=True, star=True, rates=dict({'Onull': const(0.03), 'O-Ncold': const(0.03)}, **{x: lin(0.10, 0.60) for x in X_ARMS})),
    'P_N': dict(n=2000, clause=False, star=False, rates={'Onull': lin(0.30, 0.80), 'O-Ncold': lin(0.30, 0.80), 'Odose1': lin(0.45, 0.95), 'Odosehalf': lin(0.45, 0.95), 'Lneg': lin(0.45, 0.95),
                                                          'Onull-Ncold': lin(0.45, 0.95), 'N': lin(0.45, 0.95), 'Osec-Ncold': lin(0.45, 0.95)}),
    'P_C': dict(n=2000, clause=True, star=False, rates=dict({'Onull': [0.02, 0.03, 0.10, 0.30, 0.50, 0.70], 'O-Ncold': [0.02, 0.03, 0.10, 0.30, 0.50, 0.70]},
                                                           **{x: [0.17, 0.18, 0.25, 0.45, 0.65, 0.84] for x in X_ARMS})),   # v2.1: 最大の規模を下げ、pt 差の傾きを β₃ と同じ向きで非有意にする（変異 M8 を見分ける配置・採否表 P135）
    'MIX': dict(n=200, rates={'Onull': const(0.5), 'Odose1': const(0.5), 'Odosehalf': const(0.5), 'Lneg': const(0.5), 'N': const(0.5), 'Onull-Ncold': const(0.5), 'O-Ncold': const(0.01), 'Osec-Ncold': const(0.01)})}
SC_TYPE = dict(zip(SC, ['P_S', 'P_CS', 'P_N', 'P_C', 'MIX']))
COMBOS = list(itertools.product((False, True), ('none', 'note', 'hold'), (False, True)))
NC_ID = 'SK:Lneg~Onull'
REF_A_FULL = [0.10, 0.14, 0.18, 0.22, 0.26, 0.30]; REF_A_ANS = [0.50, 0.46, 0.42, 0.38, 0.34, 0.30]   # 全分母は上向き・答えた分母は下向き（理由 a）
REF_B = [0.80, 0.64, 0.48, 0.32, 0.16, 0.0]   # refuse の割合（答えた分母の率は基の腕と同じ 0.5・理由 b）
N_RUNS = 15
RUNS = list(range(1, N_RUNS + 1)) if a.runs == 'all' else [int(x) for x in a.runs.split(',')]
xarm = lambda c: c['A'] if c['A'] in X_ARMS else c['B']


def cfg(run):
    rf, st, env = COMBOS[run - 1] if run <= len(COMBOS) else COMBOS[0]
    C = {'combo': (rf, st, env) if run <= len(COMBOS) else None, 'types': dict(SC_TYPE), 'refuse': {(sc, x): 'drift' for sc in SC for x in X_ARMS} if rf else {},
         'style': {x: ('b', st) for x in X_ARMS} if st != 'none' else {}, 'env': set(X_ARMS) if env else set(), 'unmeas': {}, 'anchor': set(), 'remaining': None, 'identity': None,
         'calib_anom': [], 'wd_anom': False, 'api': False, 'floor0': False, 'override': {}}
    if run == 1:
        C.update(unmeas={('SK', 'Odosehalf'): ('8B', '14B', '32B')}, floor0=True, wd_anom=True)
    elif run == 2:
        C.update(anchor={('1.7B', 'SK')}, identity='fail')
    elif run == 3:
        C.update(calib_anom=[('4B', 'N1')])
    elif run == 4:
        C.update(api=True, identity='pass')
    elif run == 5:
        C.update(anchor={('4B', sc) for sc in SC})
    elif run == 13:
        C.update(remaining=['N1'])
    elif run == 14:
        C['types'].update({'N2': 'P_S', 'S1': 'P_S'}); C['refuse'] = {(sc, x): mode for sc, mode in (('N1', 'a'), ('N2', 'b'), ('S1', 'd')) for x in X_ARMS}
    elif run == 15:
        C['types'].update({'N2': 'P_S'})
        C.update(refuse={(sc, 'N'): 'drift' for sc in SC}, style={'Lneg': ('a', 'hold')}, env={'Odose1'}, unmeas={('N1', 'Odosehalf'): ('8B', '14B', '32B')}, calib_anom=[('4B', 'N2')],
                 override={('N2', 'Onull-Ncold'): lin(0.8, 0.2)})
    C['one_side'] = {c['id'] for c in CONTR for (sc, arm), sizes in C['unmeas'].items()
                     if c['scenario'] == sc and arm in (c['A'], c['B']) and len({T['environments'][s]['env'] for s in SIZES if s not in sizes}) == 1}
    return C


def spec(run, model, sc, arm, phase='main'):
    """(n, 破局, refuse, 書式外) を返す（人工値）。"""
    C = cfg(run); s = '4B' if model == ANCHOR else model; i = SIZES.index(s); ty = TYPES[C['types'][sc]]
    mode = C['refuse'].get((sc, arm)) if phase in ('main', 'bridge', 'anchor') else None
    if (sc, arm) in C['override']:
        n, rate = ty['n'], C['override'][(sc, arm)][i]
    elif arm in ty['rates']:
        n, rate = ty['n'], ty['rates'][arm][i]
    elif arm in ('O', 'Nk', 'Osec'):
        n, rate = 200, (0.10 if (C['floor0'] and sc == 'SK' and arm == 'O' and s == '32B') else 0.005)
    else:
        n, rate = 40, 0.5
    if phase == 'anchor' and (s, sc) in C['anchor'] and arm == 'Onull':
        rate = rate + 0.20 if rate < 0.5 else rate - 0.20
    if phase == 'bridge' and arm in C['env']:
        rate = rate + 0.20 if rate < 0.5 else rate - 0.20
    ref = 0
    if mode == 'drift':
        cat = int(round(n * rate)); ref = int(round(n * 0.20 * (1 - i / (len(SIZES) - 1))))
    elif mode == 'a':
        cat = int(round(n * REF_A_FULL[i])); ref = n - int(round(cat / REF_A_ANS[i]))
    elif mode == 'b':
        ref = int(round(n * REF_B[i])); cat = int(round((n - ref) * 0.5))
    elif mode == 'd':
        cat, ref = ((12, n - (MIN_OK - 1)) if i < 4 else (int(round(n * (0.5 if i == 4 else 0.6))), 0))
    else:
        cat = int(round(n * rate))
    cat += (2 if phase == 'api' else 0)
    ff = int(round(n * 0.40)) if (phase == 'main' and s in C['unmeas'].get((sc, arm), ())) else 0
    if ff:
        cat = min(cat, n - ref - ff)
    assert cat + ref + ff <= n, (run, model, sc, arm, phase, cat, ref, ff)
    return n, cat, ref, ff


def write_run(root, tag, model, sc, seed, arms, fn_spec):
    rk = '%s__%s__none__seed%d' % (tag, sc, seed); d = os.path.join(root, tag, rk); os.makedirs(d, exist_ok=True); mid = MID[model]; mfn = mid.replace('/', '_')
    json.dump({'tag': tag, 'scenario': sc, 'model': mid, 'seed': seed, 'arms': arms, 'arm_src': {}, 'synthetic': True}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    open(os.path.join(d, 'raw-%s.jsonl' % mfn), 'w').close()
    ti = 0
    with open(os.path.join(d, 'trials-%s.jsonl' % mfn), 'w', encoding='utf-8', newline='\n') as f:
        for arm in arms:
            n, cat, ref, ff = fn_spec(arm)
            for j in range(n):
                v = ('true', '"a"', 'false') if j < cat else (('false', '"refuse"', 'false') if j < cat + ref else (('null', 'null', 'true') if j < cat + ref + ff else ('false', '"b"', 'false')))
                f.write('{"trial_id":"%s-%d","trial_index":%d,"arm":"%s","status":"ok","catastrophe":%s,"choice":%s,"format_fail":%s,"loop_flag":false,"truncated":false}\n' % (rk, ti, ti, arm, v[0], v[1], v[2])); ti += 1
    return rk


def build(run, root):
    tag = 'synthA%02d' % run; C = cfg(run); sess = {}; style = {}
    for m in T['models']:
        mk = m['key']
        for sc in SC:
            rk = write_run(root, tag, mk, sc, S['main'][mk][sc], ARMS, lambda arm, mk=mk, sc=sc: spec(run, mk, sc, arm)); sess.setdefault((tag, mk), []).append(rk)
            cells = style.setdefault(mk, {}).setdefault(sc, {})
            for arm in ARMS:
                n, cat, ref, ff = spec(run, mk, sc, arm); kind, level = C['style'].get(arm, ('b', 'none')); frac = {'none': 0.5, 'note': 0.70, 'hold': 0.90}[level]
                b = int(round(n * (frac if kind == 'b' else 0.5))); am = int(round(n * (frac - 0.5))) if kind == 'a' else 0; pn = n - b
                cells[arm] = {'n_ok': n, 'a_final': am, 'b_final': b, 'c1_final': 0, 'c2_final': 0, 'think_residue': 0,
                              'strata': {'json_direct': {'n': b, 'cat': cat - int(round(cat * pn / n))}, 'prose': {'n': pn, 'cat': int(round(cat * pn / n))}}}
            if mk in T['anchor_band']['models']:
                rk2 = write_run(root, tag + '-anchor2', mk, sc, S['anchor_rerun'][mk][sc], T['anchor_band']['arms'], lambda arm, mk=mk, sc=sc: spec(run, mk, sc, arm, 'anchor')); sess[(tag, mk)].append(rk2)
    for bm in BR['cells']:
        rk = write_run(root, tag + '-bridge', bm, BR['scenario'], list(S['bridge'][bm].values())[0], BR['arms'], lambda arm, bm=bm: spec(run, bm, BR['scenario'], arm, 'bridge')); sess[(tag + '-bridge', bm)] = [rk]
    if C['api']:
        for mk, seed in S['api_rerun'].items():
            write_run(root, tag + '-api', mk, 'N1', seed, ARMS, lambda arm, mk=mk: spec(run, mk, 'N1', arm, 'api'))
    os.makedirs(os.path.join(root, 'sessions-A'), exist_ok=True)
    for (tg, mk), rks in sess.items():
        envv = BR['cells'][mk]['bridge_env'] if tg.endswith('-bridge') else T['environments'][mk]['env']
        json.dump({'tag': tg, 'model': mk, 'session': 1, 'phase': 'bridge' if tg.endswith('-bridge') else 'main', 'env_value': envv, 'run_keys': rks, 'synthetic': True},
                  open(os.path.join(root, 'sessions-A', '%s__%s__s1.json' % (tg, mk)), 'w', encoding='utf-8'), ensure_ascii=False)
    rec = os.path.join(root, 'records'); os.makedirs(rec, exist_ok=True)
    P = {'style': os.path.join(rec, 'style-%s.json' % tag), 'gate': os.path.join(rec, 'gate-%s.json' % tag), 'calib': os.path.join(rec, 'calib-%s.json' % tag)}
    json.dump({'kind': 'response_mode_A', 'synthetic': True, 'tag': tag, 'cells': style}, open(P['style'], 'w', encoding='utf-8'), ensure_ascii=False)
    rem = C['remaining'] if C['remaining'] is not None else list(SC)   # v2.1: gate_A と同じ形（per_scenario つき・採否表 P129）
    per_sc = {sc: {'remains': sc in rem, 'contrasts': [{'id': c['id'], 'kept_n': len(SIZES) if sc in rem else 0} for c in CONTR if c['scenario'] == sc]} for sc in SC}
    EBR = T['environment_band']['band_pt']   # 組み立て器が読む欄（撤退条件の枝・環境帯の引き直し・様式のパイロット）も gate_A と同じ名で置く（反映の確かめ T6 で欠けを見つけた）
    json.dump({'kind': 'gate_A', 'synthetic': True, 'gate2': {'shrink': C['remaining'] is not None, 'remaining_scenarios': rem, 'shrink_scenarios': [sc for sc in SC if sc not in rem] if C['remaining'] is not None else [], 'per_scenario': per_sc},
               'withdrawal': {'branch': 'pass', 'rerun': None, 'anomaly': C['wd_anom'], 'status': 'anomaly' if C['wd_anom'] else 'pass'},
               'env_band_recheck': {'selected_by_rule_at_pilot': EBR, 'registered_band_pt': EBR, 'registered_meets_rule_at_pilot': True, 'note': '合成'}, 'style_pilot': None},
              open(P['gate'], 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({'kind': 'calib_band_A', 'synthetic': True, 'anomaly_run_keys': ['%s__%s__none__seed%d' % (tag, sc, S['main'][s][sc]) for s, sc in C['calib_anom']]}, open(P['calib'], 'w', encoding='utf-8'), ensure_ascii=False)
    if C['identity']:
        P['identity'] = os.path.join(rec, 'identity-%s.json' % tag)
        json.dump({'kind': 'identity_screen_A', 'synthetic': True, 'verdict': C['identity']}, open(P['identity'], 'w', encoding='utf-8'), ensure_ascii=False)
    return tag, P, C


def expected_row(c, C):
    if C['remaining'] is not None and c['scenario'] not in C['remaining']:
        return 'U-gate2_shrink'
    t = C['types'][c['scenario']]
    if t == 'MIX':
        return 'U-nonconverged' if c['id'] == NC_ID else ('U-residual' if c['B'] == 'Osec-Ncold' else 'NS')
    ty = TYPES[t]; x = xarm(c)
    return confirm_A.row_id(2, clause=ty['clause'], star=ty['star'], refuse=(c['scenario'], x) in C['refuse'], style=C['style'][x][1] if x in C['style'] else 'none',
                            env=(x in C['env']) or (c['id'] in C['one_side']))


FIRST_MATCH = FAM['confirm_rule']['label_stages']['stage2_first_match']
LOWF, HIGHF = Fraction(str(T['censor']['low'])), Fraction(str(T['censor']['high']))


def expected_label(row):
    """期待の行 id から期待の札を、正本 stage2_first_match の順で組む（confirm_A._stage2 を使わない・採否表 P135）。行 id の符号化（confirm_A.row_id）は判定の器と共有する。"""
    if row.startswith('U-'):
        return L['undecidable']
    if row == 'NS':
        return L['ns']
    m = re.fullmatch(r'R-C(\d)S(\d)F(\d)Y([nth])E(\d)', row)
    on = {'interpretation_clause': m.group(1) == '1', 'iut_not_rejected': m.group(2) != '1', 'refuse_gate': m.group(3) == '1', 'style_gate_hold': m.group(4) == 'h', 'environment_hold': m.group(5) == '1', 'none': True}
    return next(x['label'] for x in FIRST_MATCH if on[x['rule'].split('（')[0]])


def expected_keep(run, c, C):
    """期待の keep を配置から組む（両腕条件の検閲の整数境界・測定不能・錨帯の除外・集計器の keep を読まない・採否表 P136）。"""
    keep = []
    for s in SIZES:
        nA, kA, _, _ = spec(run, s, c['scenario'], c['A']); nB, kB, _, _ = spec(run, s, c['scenario'], c['B'])
        low = kA * LOWF.denominator < LOWF.numerator * nA and kB * LOWF.denominator < LOWF.numerator * nB
        high = kA * HIGHF.denominator > HIGHF.numerator * nA and kB * HIGHF.denominator > HIGHF.numerator * nB
        unm = any(s in C['unmeas'].get((c['scenario'], arm), ()) for arm in (c['A'], c['B']))
        keep.append(not (low or high or unm or (s, c['scenario']) in C['anchor']) and nA > 0 and nB > 0)
    return keep


def expected_notes(c, C, ek, exp_row):
    """注の期待を、期待の札と期待の keep から組む（集計器の札と keep を読まない・採否表 P136）。"""
    want = set()
    if C['identity'] == 'fail' and 'N' in (c['A'], c['B']):
        want.add('identity')
    if expected_label(exp_row) == L['confirmed']:
        kept = {SIZES[j] for j in range(len(SIZES)) if ek[j]}
        if any(sc == c['scenario'] and s in kept for s, sc in C['calib_anom']):
            want.add('calib')
        if C['wd_anom']:
            want.add('withdrawal')
    if sum(ek) >= FAM['model']['min_sizes'] and not (C['types'][c['scenario']] == 'MIX' and c['id'] == NC_ID):
        k = [j for j in range(len(SIZES)) if ek[j]]
        if (k[-1] - k[0] + 1) != len(k) or not ek[0] or not ek[-1]:
            want.add('gap')
    return want


def got_notes(x):
    g = set()
    for n_ in x['notes']:
        g.add({PS['identity_fail_note']: 'identity', PS['calib_anomaly_note']: 'calib', PS['withdrawal_anomaly_note']: 'withdrawal'}.get(n_, 'gap' if '残存規模は連続でない' in n_ else 'other:' + n_[:30]))
    return g


def compare(RJ, run, C):
    mm = []
    for x, c in zip(RJ['contrasts'], CONTR):
        exp = expected_row(c, C)
        if x['row'] != exp:
            mm.append({'kind': 'row', 'run': run, 'id': x['id'], 'expected': exp, 'got': x['row']})
        exl = expected_label(exp)
        if x['label'] != exl:   # v2.1: 札の突合（採否表 P135）
            mm.append({'kind': 'label', 'run': run, 'id': x['id'], 'expected': exl, 'got': x['label']})
        ek = expected_keep(run, c, C)
        if list(x['result']['keep']) != ek:   # v2.1: keep の突合（採否表 P136）
            mm.append({'kind': 'keep', 'run': run, 'id': x['id'], 'expected': ek, 'got': x['result']['keep']})
        wn, gn = expected_notes(c, C, ek, exp), got_notes(x)
        if wn != gn:
            mm.append({'kind': 'notes', 'run': run, 'id': x['id'], 'expected': sorted(wn), 'got': sorted(gn)})
        mode = C['refuse'].get((c['scenario'], xarm(c)))
        if mode in ('a', 'b', 'd') and x['stage'] == 2 and mode not in ((x['refuse_gate'] or {}).get('reasons') or []):
            mm.append({'kind': 'refuse_reason', 'run': run, 'id': x['id'], 'expected': mode, 'got': (x['refuse_gate'] or {}).get('reasons')})
    sets = [('unmeasurable', {(s, sc, arm) for (sc, arm), sizes in C['unmeas'].items() for s in sizes}, {(u['model'], u['scenario'], u['arm']) for u in RJ['unmeasurable']}),
            ('anchor_units', set(C['anchor']), {(u['model'], u['scenario']) for u in RJ['anchor_excluded_units']}),
            ('env_flag_arms', set(C['env']), set(RJ['env_flag_arms'])),
            ('gate2_shrink_ids', {c['id'] for c in CONTR if C['remaining'] is not None and c['scenario'] not in C['remaining']}, set(RJ.get('gate2_shrink_ids') or []))]
    for nm, want, got in sets:
        if want != got:
            mm.append({'kind': 'scope:' + nm, 'run': run, 'expected': sorted(map(str, want)), 'got': sorted(map(str, got))})
    return mm


def paths_fired(RJ):
    got = set(); C_ = RJ['contrasts']
    pairs = [('unmeasurable', bool(RJ['unmeasurable'])), ('anchor_exclusion', bool(RJ['anchor_excluded_units'])), ('env_bridge', any(e['rule'] == 'bridge' for x in C_ for e in x['env_reasons'])),
             ('env_one_side', any(e['rule'] == 'one_side' for x in C_ for e in x['env_reasons'])), ('style_cells', any(x['strings'].get('style') for x in C_)),
             ('stratified_ok', any(s_.get('status') == 'ok' for s_ in RJ['stratified'])), ('stratified_any', bool(RJ['stratified'])), ('sensitivity_changed', any(s_['changed'] for s_ in RJ['sensitivity'])),
             ('measurable_yes', any(v['measurable'] for v in RJ['measurable']['types'].values())), ('measurable_no', any(not v['measurable'] for v in RJ['measurable']['types'].values())),
             ('stack_rows', bool(RJ['descriptive']['A_desc_stack']['rows'])), ('demotions', bool(RJ['demotions'])), ('floor_1', any(f['flag'] == 1 for f in RJ['floor'])),
             ('floor_0', any(f['flag'] == 0 for f in RJ['floor'])), ('critical_size', any(x['size'] != 'なし' for x in RJ['descriptive']['A_desc_critical_size'])),
             ('env_secondary', any(x.get('status') == '収束' for x in RJ['descriptive']['A_desc_env']['secondary'])), ('scale_only_desc', bool(RJ['descriptive']['A_desc_scale_only'])),
             ('reach_note', bool(RJ.get('reach_note'))), ('confirmed_label_string', any(x['label'] == L['confirmed'] for x in C_)),
             ('refuse_a', any('a' in ((x['refuse_gate'] or {}).get('reasons') or []) for x in C_)), ('refuse_b', any('b' in ((x['refuse_gate'] or {}).get('reasons') or []) for x in C_)),
             ('refuse_d', any('d' in ((x['refuse_gate'] or {}).get('reasons') or []) for x in C_)),
             ('style_a_hold', any(x['style'] == 'hold' and any(cl['kind'] == 'a' for cl in (x['style_detail'] or {}).get('cells', [])) for x in C_)),
             ('confirmed_multi_scenario', len({x['scenario'] for x in C_ if x['label'] == L['confirmed']}) >= 2),
             ('one_side_stage2', any(x['stage'] == 2 and any(e['rule'] == 'one_side' for e in x['env_reasons']) for x in C_)),
             ('residual_gap_note', any('残存規模は連続でない' in n_ for x in C_ for n_ in x['notes'])), ('control_pairs_string', any(p_.get('string') for p_ in RJ['descriptive'].get('A_desc_control_pairs') or [])),
             ('upward', bool(RJ.get('upward_confirmed'))), ('gate2_partial_shrink', bool(RJ.get('gate2_shrink_ids')) and any(x['stage'] == 2 for x in C_)),
             ('measurable_both_directions', all(set(v['directions']) == set(confirm_A.DIRECTIONS) for v in RJ['measurable']['types'].values()) and bool(RJ['measurable']['types']))]
    for nm, on in pairs:
        if on:
            got.add(nm)
    notes = [n_ for x in C_ for n_ in x['notes']]
    for key in ('identity_fail_note', 'calib_anomaly_note', 'withdrawal_anomaly_note'):
        if PS[key] in notes:
            got.add(key)
    return got


PATHS_REQUIRED = ['measurable_both_directions', 'unmeasurable', 'anchor_exclusion', 'env_bridge', 'env_one_side', 'style_cells', 'stratified_ok', 'stratified_any', 'sensitivity_changed', 'measurable_yes', 'measurable_no',
                  'identity_fail_note', 'calib_anomaly_note', 'withdrawal_anomaly_note', 'stack_rows', 'demotions', 'floor_1', 'floor_0', 'critical_size', 'env_secondary', 'scale_only_desc', 'reach_note',
                  'confirmed_label_string', 'refuse_a', 'refuse_b', 'refuse_d', 'style_a_hold', 'confirmed_multi_scenario', 'one_side_stage2', 'residual_gap_note', 'control_pairs_string', 'upward', 'gate2_partial_shrink']


def run_once(run, tools_dir, sub):
    root = os.path.join(ROOT, sub); shutil.rmtree(root, ignore_errors=True); t0 = time.time(); tag, P, C = build(run, root); out = os.path.join(root, 'out', 'analysis-%s' % tag)
    cmd = [sys.executable, os.path.join(tools_dir, 'analyze_A.py'), '--tag', tag, '--root', root, '--anchor-tag', tag + '-anchor2', '--bridge-tag', tag + '-bridge', '--api-tag', tag + '-api',
           '--style', P['style'], '--gate', P['gate'], '--calib', P['calib'], '--out', out, '--force', '--B-measurable', str(a.B_measurable), '--synth-nonconverged', NC_ID]
    cmd += ['--identity', P['identity']] if 'identity' in P else ['--no-identity']
    if a.facts and os.path.exists(a.facts):
        cmd += ['--facts', a.facts]
    pr = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    if pr.returncode != 0:
        res = {'error': (pr.stdout[-1500:] + pr.stderr[-3000:])}
    else:
        RJ = runs_A.read_json(out + '.json'); res = {'RJ': RJ, 'mismatches': compare(RJ, run, C), 'paths': paths_fired(RJ), 'C': C}
    res['seconds'] = round(time.time() - t0, 1)
    if not a.keep:
        shutil.rmtree(root, ignore_errors=True)
    return res


MUTS = [('M1', 'tools/analyze_A.py', [("        if rks & ANOM_RK:\n", "        if ANOM_RK:\n")], [15], '校正腕の器の異常の注を全確証に付ける'),
        ('M2', 'tools/analyze_A.py', [("    if ID_VERDICT == 'fail' and 'N' in (c['A'], c['B']):\n", "    if ID_VERDICT == 'fail':\n")], [2], '門0.5 不合格の注を全対比に付ける'),
        ('M3', 'tools/analyze_A.py', [("    if len(envs) == 1:\n", "    if len(envs) == 0:\n")], [15], '片側の規則を外す'),
        ('M4', 'tools/confirm_A.py', [("    if len(j) < R.ref_min_sizes:\n        out['reasons'].append('d')\n", "    if len(j) < R.ref_min_sizes:\n        pass\n"),
                                     ("            if np.sign(ra['beta']) != np.sign(res['beta']) or ra['beta'] == 0.0:\n", "            if False:\n"), ("            if ra['p'] >= R.alpha:\n", "            if False:\n")], [14],
         'refuse の理由を (c) だけにする'),
        ('M5', 'tools/confirm_A.py', [("        for nm, xa, xb in (('a', a_A, a_B), ('b', b_A, b_B)):\n", "        for nm, xa, xb in (('b', b_A, b_B),):\n")], [15], '様式門の (a) を読まない'),
        ('M6', 'tools/analyze_A.py', [("SHRINK_IDX = {i for i, c in enumerate(CONTR) if GATE2 and c['scenario'] not in REMAIN}", "SHRINK_IDX = {i for i, c in enumerate(CONTR) if GATE2}")], [13], '門2 の縮小を全対比に当てる'),
        ('M7', 'tools/confirm_A.py', [("(('interpretation_clause', clause), ('iut_not_rejected', not star),", "(('iut_not_rejected', not star), ('interpretation_clause', clause),")], [1], '第一適合の順の先頭二つを入れ替える'),
        ('M8', 'tools/confirm_A.py', [("p_star=(max(float(r['p']), p_pt) if same else R.p_star_mismatch)", "p_star=(min(float(r['p']), p_pt) if same else R.p_star_mismatch)")], [1], 'p* を max から min に'),
        ('M9', 'tools/analyze_A.py', [("        if (kidx[-1] - kidx[0] + 1) != len(kidx) or ends:\n", "        if (kidx[-1] - kidx[0] + 1) != len(kidx):\n")], [1], '残存の非連続の注から端の欠けの条件を外す'),
        ('M10', 'tools/analyze_A.py', [("r, f = evaluate(R, c, X, ke); RES.append(r)", "r, f = evaluate(R, c, X, None); RES.append(r)")], [1, 2], '主の当てはめに測定不能・錨帯の除外を渡さない')]


def make_mutant(name, rel, pairs):
    d = os.path.join(ROOT, 'mutant-' + name); shutil.rmtree(d, ignore_errors=True)
    for sub in ('tools', 'design', os.path.join('records', 'A')):
        os.makedirs(os.path.join(d, sub))
    for f in ('analyze_A.py', 'confirm_A.py', 'runs_A.py', 'firth.py', 'zaxis_A.py', 'bands_A.py'):
        shutil.copy(os.path.join(REPO, 'tools', f), os.path.join(d, 'tools', f))
    shutil.copy(runs_A.CPATH, os.path.join(d, 'design', 'contrasts-A.json')); shutil.copy(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), os.path.join(d, 'records', 'A', 'hf-models-A.json'))
    p = os.path.join(d, rel); s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (name, old[:60], s.count(old)); s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    return d


fired = {}; paths = set(); report = []; mismatches = []; errors = []; t00 = time.time()
for run in RUNS:
    res = run_once(run, os.path.join(REPO, 'tools'), 'run%02d' % run)
    if 'error' in res:
        errors.append({'run': run, 'error': res['error']}); print('[synth] 走 %2d 集計器が失敗: %s' % (run, res['error'][-800:]), flush=True); continue
    RJ = res['RJ']; mismatches += res['mismatches']; paths |= res['paths']
    for x in RJ['contrasts']:
        fired.setdefault(x['row'], []).append('%d:%s' % (run, x['id']))
    C = res['C']
    report.append({'run': run, 'combo': {'refuse_hold': C['combo'][0], 'style': C['combo'][1], 'env_hold': C['combo'][2]} if C['combo'] else '特別の配置', 'label_counts': RJ['label_counts'],
                   'mismatches': len(res['mismatches']), 'rows': sorted({x['row'] for x in RJ['contrasts']}), 'paths': sorted(res['paths']), 'dev_marks': RJ['dev_marks'], 'seconds': res['seconds']})
    print('[synth] 走 %2d 不一致 %d 行 %d 経路 %d（%.0fs）' % (run, len(res['mismatches']), len(report[-1]['rows']), len(res['paths']), res['seconds']), flush=True)
MUT = []
want_m = [] if a.mutations == 'none' else [m for m in MUTS if a.mutations == 'all' or m[0] in a.mutations.split(',')]
for name, rel, pairs, mruns, text in want_m:
    d = make_mutant(name, rel, pairs); det = 0; errs = []
    for run in mruns:
        res = run_once(run, os.path.join(d, 'tools'), 'mut-%s-run%02d' % (name, run))
        if 'error' in res:
            errs.append(res['error'][-300:])
        else:
            det += len(res['mismatches'])
    MUT.append({'name': name, 'file': rel, 'text': text, 'runs': mruns, 'mismatches': det, 'detected': det > 0 and not errs, 'errors': errs})
    print('[synth] 変異 %s（%s）: 不一致 %d・%s' % (name, text, det, '見分けた' if det > 0 and not errs else '見分けなかった'), flush=True)
    if not a.keep:
        shutil.rmtree(d, ignore_errors=True)
not_fired = [r for r in ALL_ROWS if r not in fired]; paths_missing = [p for p in PATHS_REQUIRED if p not in paths]
full = (RUNS == list(range(1, N_RUNS + 1))) and a.mutations == 'all'
SUM = {'kind': 'synth_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'runs': RUNS, 'full': full,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), **{nm: runs_A.sha16_file(os.path.join(REPO, 'tools', nm)) for nm in ('analyze_A.py', 'confirm_A.py', 'runs_A.py', 'firth.py', 'synth_A.py')}},
       'rows_total': len(ALL_ROWS), 'rows_fired': len(ALL_ROWS) - len(not_fired), 'rows_not_fired': not_fired, 'mismatches': mismatches, 'errors': errors, 'paths_required': PATHS_REQUIRED, 'paths_missing': paths_missing,
       'mutations': MUT, 'fired_by_row': {k: v[:3] for k, v in sorted(fired.items())}, 'per_run': report, 'seconds': round(time.time() - t00, 1),
       'clause': '合成の件数は検査のための人工値であり、いかなる読みにも用いない。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
recp = a.record or os.path.join(REPO, 'records', 'A', 'synth-A-%s' % datetime.date.today().isoformat())
if full:
    json.dump(SUM, open(recp + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    Lm = ['# 段階 A 合成検査（機械生成・`tools/synth_A.py` %s・%s UTC・ファイル名の日付は手元の日付〔日本時間〕）' % (VERSION, SUM['generated_utc']), '', '- 入力: %s' % json.dumps(SUM['inputs'], ensure_ascii=False),
          '- 札の全組合せ表: %d 行のうち発火 %d 行（未発火: %s）・期待との不一致 %d 件（行 id・注の範囲・除外の範囲・refuse の理由）・集計器の失敗 %d・経路の未発火: %s・所要 %.0f 秒' % (
              SUM['rows_total'], SUM['rows_fired'], '・'.join(not_fired) or 'なし', len(mismatches), len(errors), '・'.join(paths_missing) or 'なし', SUM['seconds']),
          '- 変異の検査: %s' % '・'.join('%s（%s）%s' % (m['name'], m['text'], '見分けた' if m['detected'] else '見分けなかった') for m in MUT), '',
          '| 走 | 配置 | 札の件数 | 不一致 | 発火した行 | 発火した経路 | 秒 |', '|---|---|---|---|---|---|---|']
    Lm += ['| %d | %s | %s | %d | %s | %s | %s |' % (r['run'], json.dumps(r['combo'], ensure_ascii=False), json.dumps(r['label_counts'], ensure_ascii=False), r['mismatches'], '・'.join(r['rows']), '・'.join(r['paths']), r['seconds']) for r in report]
    Lm += ['', '| 変異 | 器 | 内容 | 走 | 期待との不一致 | 判定 |', '|---|---|---|---|---|---|'] + ['| %s | %s | %s | %s | %d | %s |' % (m['name'], m['file'], m['text'], '・'.join(map(str, m['runs'])), m['mismatches'], '見分けた' if m['detected'] else '見分けなかった') for m in MUT]
    Lm += ['', '- 限界: 札の全組合せ表（正本 label_combo_table）は判定関数 combo_rows の出力であり、第一適合の順の検査は confirm_A の自己検査の照合と、本器の札の突合（期待の札は正本 stage2_first_match から組む）にある（採否表 P137）。',
           '- 限界: 期待の行 id の符号化（confirm_A.row_id）は判定の器と共有する（符号化の誤りは両側で同じに出る）。',
           '- 限界: 本器は Firth の PPLRT・pt 差の傾きの重み付き最小二乗・検閲の数値の実装を独立に再発見しない（数値の実装は自己検査と R logistf との一致検査の受け持ち）。合成の件数は応答の分布を再現しない。', '', SUM['clause']]
    open(recp + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(Lm) + '\n')
    print('written', recp + '.{json,md}')
print('[synth_A] 行 %d/%d 発火・不一致 %d・失敗 %d・経路の未発火 %s・変異 %s' % (SUM['rows_fired'], SUM['rows_total'], len(mismatches), len(errors), paths_missing, [(m['name'], m['detected']) for m in MUT]))
if mismatches:
    print(json.dumps(mismatches[:25], ensure_ascii=False))
if full:
    assert not not_fired and not mismatches and not errors and not paths_missing and all(m['detected'] for m in MUT), (not_fired, len(mismatches), len(errors), paths_missing, [(m['name'], m['detected']) for m in MUT])
    print('synth_A.py %s PASS' % VERSION)
