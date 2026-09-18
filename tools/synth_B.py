# -*- coding: utf-8 -*-
"""synth_B.py v1 —— 段階 B の**合成データ**の生成器（器材の検査用・実データを作らない）。

札の全経路を一度ずつ以上発火させるための走行の記録を作る（器材の整備の計画 `records/B/tooling-plan-B-2026-09-18.md` の表）。
作るもの（既定の置き場は results/_synth/<場合>/）:
  本走行 `stageB`／調整走行 `tuneB`／品質床 `stageB-quality`／セッション記録 sessions-B。
件数は**乱数でなく決め打ち**（狙った札を確実に発火させるため）。すべての行に `dry_run: true` を立て、置き場に `_dryrun` を含める
（実データと取り違えないため。読む側は `--allow-dry` の検査用の口でしか読めない）。
用法: python tools/synth_B.py --case all --out-root results/_synth/all
      python tools/synth_B.py --list
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, argparse, datetime, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
SC = T['scenarios']
EX = T['extraction_scenarios']
N_MAIN, N_TUNE, N_Q = T['n_main'], T['n_tune'], T['quality_floor']['items']
LAYERS, COEFS = T['selection']['candidates']['layers'], T['selection']['candidates']['coefficients']
CANDS = [(l, c) for l in LAYERS for c in COEFS]
V_ARM, R_ARM = T['selection']['tune']['arms']
QF_ARMS = T['quality_floor']['arms']
QF_OPS = {'O-Ncold': '-v', 'Onull': '+v'}
INTERV = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
NOOP_BASE = {a: a.split('+v')[0].split('-v')[0] for a in INTERV}


def _trial(i, arm, scenario, tag, seed, run_key, cat, refuse, ff, style_a, style_b, mention, correct=None, layer=None, coef=None, status='ok'):
    return {'trial_id': '%s__%s__%04d' % (run_key, arm, i), 'trial_index': i, 'arm': arm, 'scenario': scenario, 'tag': tag,
            'status': status, 'catastrophe': (None if status != 'ok' else bool(cat)), 'choice': ('refuse' if refuse else 'A'),
            'format_fail': bool(ff), 'style_a': bool(style_a), 'style_b': bool(style_b), 'mention': bool(mention),
            'loop_flag': False, 'truncated': False, 'correct': (None if correct is None else bool(correct)),
            'seed': seed, 'run_key': run_key, 'runner_sha': 'SYNTH', 'arms_spec': arm, 'preamble_sha': 'SYNTH',
            'model': 'stub/dry-run', 'sampling': dict(T['runner']['generation']), 'layer': layer, 'coef': coef,
            'direction_id': 'synth', 'batch_pos': i % T['runner']['batch'], 'proc_uuid': 'synth', 'dry_run': True}


def cell_trials(n, spec, **kw):
    """spec: 件数の割り当て（cat・refuse・ff・style_a・style_b・mention・correct・api_error）。残りは無印の試行。"""
    out = []
    n_err = int(spec.get('api_error', 0))
    for i in range(n):
        if i < n_err:
            out.append(_trial(i, status='error', cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, **kw))
            continue
        j = i - n_err
        out.append(_trial(i, cat=j < spec.get('cat', 0), refuse=spec.get('cat', 0) <= j < spec.get('cat', 0) + spec.get('refuse', 0),
                          ff=j < spec.get('ff', 0), style_a=j < spec.get('style_a', 0), style_b=j < spec.get('style_b', 0),
                          mention=j < spec.get('mention', 0), correct=(None if 'correct' not in spec else j < spec['correct']), **kw))
    return out


def write_run(root, tag, name, manifest, trials):
    d = os.path.join(root, tag, '%s__%s__dryrun' % (tag, name))
    os.makedirs(d, exist_ok=True)
    manifest = dict(manifest, tag=tag, run_key=os.path.basename(d), dry_run=True, model='stub/dry-run',
                    runner_sha='SYNTH', generated=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    json.dump(manifest, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(d, 'trials-synth.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for t in trials:
            f.write(json.dumps(t, ensure_ascii=False) + '\n')
    with open(os.path.join(d, 'raw-synth.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for t in trials:
            f.write(json.dumps({'trial_id': t['trial_id'], 'text': '（合成データ・本文は作らない）'}, ensure_ascii=False) + '\n')
    return d


# ---- 場合（case）ごとの仕様 ----
def base_main_spec():
    """本走行の既定: すべての腕で同じ率（札が立たない土台）。"""
    return {(sc, arm): {'cat': 60, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
            for sc in SC for arm in T['arms']['by_scenario'][sc]}


def case_all():
    """一つの走行で、確証・検閲・希釈（書式外・refuse）・refuse 門・様式門・品質床・非有意・逆向きを出す。"""
    m = base_main_spec()
    # 確証（N1 の減算族: A を大きく下げる・門には掛からない）
    m[('N1', 'O-Ncold-v')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('N1', 'O-Ncold-vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定不能（検閲・S1 の加算族: 両腕とも床）
    m[('S1', 'Onull+v')] = {'cat': 2, 'refuse': 4, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S1', 'Onull+vrand')] = {'cat': 4, 'refuse': 4, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（書式外転位・SK の減算族: A の書式外が門を超える）
    m[('SK', 'O-Ncold-v')] = {'cat': 30, 'refuse': 10, 'ff': 60, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('SK', 'O-Ncold-vrand')] = {'cat': 70, 'refuse': 10, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（refuse 転位・差・S4 の減算族）
    m[('S4', 'O-Ncold-v')] = {'cat': 30, 'refuse': 70, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'O-Ncold-vrand')] = {'cat': 70, 'refuse': 8, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（refuse 転位・答えた分母で有意を失う・N1 の加算族）
    m[('N1', 'Onull+v')] = {'cat': 44, 'refuse': 78, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('N1', 'Onull+vrand')] = {'cat': 70, 'refuse': 70, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（様式転位・N1 の交差族 O-Ncold）
    m[('N1', 'O-Ncold+vNk')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 10, 'mention': 8}
    m[('N1', 'O-Ncold+vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 190, 'mention': 8}
    # 注（様式・S1 の交差族 O-Ncold: 確証だが様式の差が注の帯を超える）
    m[('S1', 'O-Ncold+vNk')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S1', 'O-Ncold+vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 160, 'mention': 8}
    # 判定保留（refuse 転位・答えた分母で名目有意を失う・SK の交差族 O-Ncold。refuse の差は門の内側に収める）
    m[('SK', 'O-Ncold+vNk')] = {'cat': 70, 'refuse': 28, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('SK', 'O-Ncold+vrand')] = {'cat': 92, 'refuse': 18, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定不能（品質床・SK の交差族 Onull は品質床に落ちた腕を含む）
    m[('SK', 'Onull+vNk')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('SK', 'Onull+vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # S4 の反証（下がった＝封印は外れ）
    m[('S4', 'Osec-Ncold+v6b')] = {'cat': 10, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'Osec-Ncold+vrand')] = {'cat': 60, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    tune = {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'tie': False, 'nonpositive': False, 'ff_fail': (LAYERS[0], COEFS[0]), 'censor_all': False}
    qual = {'fail_selection': [], 'fail_post': ['Onull+vNk']}
    return {'main': m, 'tune': tune, 'quality': qual, 'seal': {'sub:N1:O-Ncold-v~O-Ncold-vrand': '上'}}


def case_gate1_closed():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': 'all', 'fail_post': []}}


def case_nonpositive():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': None, 'eff': -3, 'nonpositive': True}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_tie():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'tie': True}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_censor_candidates():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'censor_all': True}, 'quality': {'fail_selection': [], 'fail_post': []}}


CASES = {'all': case_all, 'gate1_closed': case_gate1_closed, 'nonpositive': case_nonpositive, 'tie': case_tie, 'censor_candidates': case_censor_candidates}


def build(case, out_root):
    spec = CASES[case]()
    if os.path.isdir(out_root):
        shutil.rmtree(out_root)
    os.makedirs(out_root, exist_ok=True)
    # ---- 本走行 ----
    for sc in SC:
        trials = []
        for arm in T['arms']['by_scenario'][sc]:
            s = spec['main'][(sc, arm)]
            trials += cell_trials(N_MAIN, s, arm=arm, scenario=sc, tag=T['tags']['main'], seed=T['seeds']['main'][sc],
                                  run_key='%s__%s__s1' % (T['tags']['main'], sc))
        write_run(out_root, T['tags']['main'], '%s__s1' % sc, {'scenario': sc, 'session': 1, 'n': N_MAIN, 'seed': T['seeds']['main'][sc],
                                                               'arms': T['arms']['by_scenario'][sc], 'batch': T['runner']['batch']}, trials)
    # ---- 調整走行 ----
    tu = spec['tune']
    base_cat = 100                       # n_ok=200（抽出場面をまとめて）→ 一腕あたり 100 ずつ
    for sc in EX:
        for (l, c) in CANDS:
            is_best = (tu.get('best') == (l, c)) or (tu.get('tie') and (l, c) in (tu.get('best'), (LAYERS[1], COEFS[2])))
            eff = tu['eff'] if is_best else (tu['eff'] - 4 if not tu.get('nonpositive') else tu['eff'])
            cat_v = int(round(N_TUNE * (base_cat / 200.0 - eff / 200.0)))
            cat_r = int(round(N_TUNE * (base_cat / 200.0)))
            if tu.get('censor_all'):
                cat_v, cat_r = N_TUNE, N_TUNE      # 天井
            ff_v = 60 if tu.get('ff_fail') == (l, c) else 4
            for arm, cat, ff in ((V_ARM, cat_v, ff_v), (R_ARM, cat_r, 4)):
                trials = cell_trials(N_TUNE, {'cat': cat, 'refuse': 6, 'ff': ff, 'style_a': 20, 'style_b': 60, 'mention': 4},
                                     arm=arm, scenario=sc, tag=T['tags']['tune'], seed=T['seeds']['tune'][sc], layer=l, coef=c,
                                     run_key='%s__%s__L%sC%s' % (T['tags']['tune'], sc, l, c))
                write_run(out_root, T['tags']['tune'], '%s__L%sC%s__%s' % (sc, l, c, arm), {'scenario': sc, 'layer': l, 'coef': c, 'arm': arm,
                                                                                           'n': N_TUNE, 'seed': T['seeds']['tune'][sc]}, trials)
    # ---- 品質床 ----
    q = spec['quality']
    tag_q = T['tags']['quality']
    for base in QF_ARMS + ['O', 'Osec-Ncold']:
        trials = cell_trials(N_Q, {'correct': 150, 'ff': 2}, arm=base, scenario='quality', tag=tag_q, seed=T['seeds']['quality'],
                             run_key='%s__noop__%s' % (tag_q, base))
        write_run(out_root, tag_q, 'selection__%s__noop' % base, {'stage': 'selection', 'arm': base, 'layer': None, 'coef': None, 'n': N_Q,
                                                                  'seed': T['seeds']['quality']}, trials)
    for base in QF_ARMS:
        arm = base + QF_OPS[base]
        for (l, c) in CANDS:
            bad = (q['fail_selection'] == 'all') or (arm in (q['fail_selection'] or []))
            trials = cell_trials(N_Q, {'correct': 100 if bad else 148, 'ff': 2}, arm=arm, scenario='quality', tag=tag_q,
                                 seed=T['seeds']['quality'], layer=l, coef=c, run_key='%s__%s__L%sC%s' % (tag_q, arm, l, c))
            write_run(out_root, tag_q, 'selection__%s__L%sC%s' % (arm, l, c), {'stage': 'selection', 'arm': arm, 'layer': l, 'coef': c,
                                                                              'n': N_Q, 'seed': T['seeds']['quality']}, trials)
    pick = spec['tune'].get('best') or (LAYERS[1], COEFS[1])
    for arm in INTERV:
        bad = arm in (q['fail_post'] or [])
        trials = cell_trials(N_Q, {'correct': 100 if bad else 148, 'ff': 2}, arm=arm, scenario='quality', tag=tag_q,
                             seed=T['seeds']['quality'], layer=pick[0], coef=pick[1], run_key='%s__post__%s' % (tag_q, arm))
        write_run(out_root, tag_q, 'post__%s' % arm, {'stage': 'post', 'arm': arm, 'layer': pick[0], 'coef': pick[1], 'n': N_Q,
                                                      'seed': T['seeds']['quality']}, trials)
    for base in sorted(set(NOOP_BASE.values())):
        trials = cell_trials(N_Q, {'correct': 150, 'ff': 2}, arm=base, scenario='quality', tag=tag_q, seed=T['seeds']['quality'],
                             run_key='%s__post__noop__%s' % (tag_q, base))
        write_run(out_root, tag_q, 'post__%s__noop' % base, {'stage': 'post', 'arm': base, 'layer': None, 'coef': None, 'n': N_Q,
                                                             'seed': T['seeds']['quality']}, trials)
    # ---- セッション記録 ----
    sd = os.path.join(out_root, 'sessions-B')
    os.makedirs(sd, exist_ok=True)
    for sc in SC:
        json.dump({'tag': T['tags']['main'], 'session': 1, 'scenario': sc, 'gpu': 'synth', 'batch': T['runner']['batch'],
                   'run_keys': ['%s__%s__s1__dryrun' % (T['tags']['main'], sc)], 'dry_run': True},
                  open(os.path.join(sd, '%s__%s__s1.json' % (T['tags']['main'], sc)), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # ---- 封印（任意） ----
    if spec.get('seal'):
        json.dump({'kind': 'seal_B', 'signs': spec['seal'], 's4': 'synth', 'dry_run': True},
                  open(os.path.join(out_root, 'seal-B.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out_root


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--case', default='all', choices=sorted(CASES))
    ap.add_argument('--out-root', default=None)
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list:
        print('\n'.join(sorted(CASES)))
        sys.exit(0)
    root = a.out_root or os.path.join(REPO, 'results', '_synth', a.case)
    build(a.case, root)
    print('[synth_B] %s に合成データを書いた（場合 %s・すべて dry_run）' % (root, a.case))
