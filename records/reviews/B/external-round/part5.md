# 器材のソース（逐語）（機械生成・2026-09-18 08:15 UTC）

## `tools/synth_B.py`（SHA16 488E46B0E76E0229・383 行）

```python
# -*- coding: utf-8 -*-
"""synth_B.py v3 —— 段階 B の**合成データ**の生成器（器材の検査用・実データを作らない）。

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

VERSION = 'v3'
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


def _arm_sha(arm):
    base = arm.split('+v')[0].split('-v')[0]
    return T['arms']['sha16'].get(base) or 'SYNTH'


def _trial(i, arm, scenario, tag, seed, run_key, cat, refuse, ff, style_a, style_b, mention, correct=None,
           layer=None, coef=None, status='ok', sampling=None, loop=False, trunc=False, direction_id=None):
    """一試行の記録。**実機の採点の規約に合わせる**（実装検分の採否表 P301）——
    書式外の試行は答えを読み取れないので `catastrophe`・`choice`・`correct` は None にする。"""
    ff = bool(ff)
    if status != 'ok' or ff:
        cat_v, choice, corr = None, None, None
    elif refuse:
        # **凍結パーサ `is_catastrophic` は refuse に破局の判定を返さない**（裁定 D103・採否表 P307）。
        # 前はここで偽を書いていたため、実機の規約との食い違いが合成データで一度も現れなかった。
        cat_v, choice, corr = None, 'refuse', (None if correct is None else bool(correct))
    else:
        cat_v = bool(cat)
        choice = 'A'
        corr = (None if correct is None else bool(correct))
    return {'trial_id': '%s__%s__%04d' % (run_key, arm, i), 'trial_index': i, 'arm': arm, 'scenario': scenario, 'tag': tag,
            'status': status, 'catastrophe': cat_v, 'choice': choice, 'refuse_class': None,
            'format_fail': ff, 'style_a': bool(style_a), 'style_b': bool(style_b), 'mention': bool(mention),
            'loop_flag': bool(loop), 'truncated': bool(trunc), 'correct': corr, 'logprobs': None, 'resp_mean_path': None,
            'seed': seed, 'run_key': run_key, 'runner_sha': 'SYNTH', 'arms_spec': arm, 'preamble_sha': _arm_sha(arm),
            'model': 'stub/dry-run', 'sampling': dict(sampling or T['runner']['generation']), 'layer': layer, 'coef': coef,
            'direction_id': direction_id or ('rand:%d' % (i % T['random_control']['count']) if 'vrand' in arm else 'fixed'),
            'batch_pos': i % T['runner']['batch'], 'proc_uuid': 'synth', 'dry_run': True}


def cell_trials(n, spec, start=0, **kw):
    """spec: 件数の割り当て（cat・refuse・ff・style_a・style_b・mention・correct・api_error・loop・trunc）。

    **書式外は破局の分子を食う**（実機と同じ・希釈の因果を作る・採否表 P301）。start は中断と再開のための試行の番号の起点。"""
    out = []
    n_err = int(spec.get('api_error', 0))
    n_ff, n_loop, n_trunc = int(spec.get('ff', 0)), int(spec.get('loop', 0)), int(spec.get('trunc', 0))
    cat_target, ref_target = int(spec.get('cat', 0)), int(spec.get('refuse', 0))
    # **種を正本の式で降ろす**（裁定 D107・採否表 P310）。前は走行の種をそのまま各行に書いていたので、
    # 実機が正本に従えば整合検査が必ず落ちる状態だった。
    _phase = {T['tags']['main']: 'main', T['tags']['tune']: 'tune', T['tags']['quality']: 'quality',
              T['tags']['identity']: 'identity'}.get(kw.get('tag'), 'main')
    _l, _c = kw.get('layer'), kw.get('coef')
    if _phase == 'quality':
        _key = ('post' if '__post__' in str(kw.get('run_key')) else 'selection', kw['arm'], _l, _c)
    elif _phase == 'tune':
        _key = (kw['scenario'], kw['arm'], _l, _c)
    else:
        _key = (kw['scenario'], kw['arm'])
    _cs = runs_B.cell_seed(T, kw['seed'], _phase, _key)
    for k in range(n):
        i = start + k
        if i < n_err:
            out.append(_trial(i, cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, status='error', **kw))
            out[-1]['seed'] = runs_B.trial_seed(_cs, i)
            continue
        j = i - n_err
        ff = j < n_ff
        cat = (not ff) and (n_ff <= j < n_ff + cat_target)
        refuse = (not ff) and (n_ff + cat_target <= j < n_ff + cat_target + ref_target)
        out.append(_trial(i, cat=cat, refuse=refuse, ff=ff, style_a=j < spec.get('style_a', 0), style_b=j < spec.get('style_b', 0),
                          mention=j < spec.get('mention', 0), loop=(n_ff <= j < n_ff + n_loop),
                          trunc=(n_ff + n_loop <= j < n_ff + n_loop + n_trunc),
                          correct=(None if 'correct' not in spec else (j < spec['correct'])), **kw))
        out[-1]['seed'] = runs_B.trial_seed(_cs, i)
        if spec.get('scoring_gap') and (n_ff + cat_target + ref_target) <= j < (n_ff + cat_target + ref_target + int(spec['scoring_gap'])):
            # 採点欠落（status は ok のまま・裁定 D96・D103）——**相ごとの欄**で作る
            if 'correct' in spec:
                out[-1]['correct'] = None      # 品質床は正答の欄
            else:
                out[-1]['choice'] = None       # 本走行は選択の欄
                out[-1]['catastrophe'] = None
            out[-1]['choice'] = None
    return out


def write_run(root, tag, name, manifest, trials):
    d = os.path.join(root, tag, '%s__%s__dryrun' % (tag, name))
    os.makedirs(d, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    # 正本 runner.manifest_fields（裁定 D89）の欄をそろえる（整合検査がこの一覧を読む）
    common = {'tag': tag, 'run_key': os.path.basename(d), 'session': manifest.get('session', 1), 'n': manifest.get('n'),
              'seed': manifest.get('seed'), 'batch': T['runner']['batch'], 'padding': 'left', 'model': 'stub/dry-run',
              'model_rev': 'SYNTH', 'tokenizer_rev': 'SYNTH', 'runner_sha': 'SYNTH', 'pip_freeze_sha16': 'SYNTH',
              'gpu': 'synth', 'started': stamp, 'ended': stamp, 'dry_run': True}
    extra = {'direction_ids': ['synth'], 'arms': manifest.get('arms', []), 'task_source_sha16': 'SYNTH'}
    phase = next(k for k, v in T['tags'].items() if v == tag)
    need = list((T['runner'].get('manifest_fields') or {}).get(phase, []))
    manifest = dict({k: extra[k] for k in need if k in extra}, **dict(manifest, **common, generated=stamp))
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
    # api_error と未測定（ループ・打ち切り）を無操作の腕に入れる（採否表 P300・P302）
    m[('N1', 'O')] = {'cat': 60, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8, 'api_error': 12, 'loop': 3, 'trunc': 2}
    tune = {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'tie': False, 'nonpositive': False, 'ff_fail': (LAYERS[0], COEFS[0]), 'censor_all': False}
    qual = {'fail_selection': [], 'fail_post': ['Onull+vNk']}
    # 封印は**一致する対比と逆向きの対比の両方**を持たせる（採否表 P297）
    seal = {'sub:N1:O-Ncold-v~O-Ncold-vrand': '上',          # データは「下」——逆向きの枝
            'add:N1:Onull+v~Onull+vrand': '下'}              # データも「下」——一致の枝
    return {'main': m, 'tune': tune, 'quality': qual, 'seal': seal,
            'resume': {'scenario': 'N1', 'arm': 'Onull+vtd'}}   # 中断と再開（採否表 P302）


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


def case_scoring_gap():
    """採点欠落（判定欄が空）と n_ok が零のセル（裁定 D96・採否表 P300）。"""
    m = base_main_spec()
    m[('S1', 'O-Ncold-v')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8, 'scoring_gap': 7}
    m[('SK', 'O-Ncold-v')] = {'cat': 0, 'refuse': 0, 'ff': 0, 'style_a': 0, 'style_b': 0, 'mention': 0, 'api_error': N_MAIN}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_s4_branches():
    """S4 の残りの枝——「下がらなかった（封印は当たり）」と「余地の条項で測れない（床）」（裁定 D81・D95）。"""
    m = base_main_spec()
    # 相手の率を**既測の基底の近く**（低い側）に置く——10 pt の検出力が線を越えるのはこの領域だけ（転記行 D）
    m[('S4', 'Osec-Ncold+v6b')] = {'cat': 33, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'Osec-Ncold+vrand')] = {'cat': 34, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_s4_floor():
    m = base_main_spec()
    m[('S4', 'Osec-Ncold+v6b')] = {'cat': 1, 'refuse': 2, 'ff': 2, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'Osec-Ncold+vrand')] = {'cat': 8, 'refuse': 2, 'ff': 2, 'style_a': 40, 'style_b': 120, 'mention': 8}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_dilution_causal():
    """**希釈が効く場面**——書式外が増えたぶんだけ破局の分子が減り、見かけの低下が出る（裁定 D111・採否表 P309）。

    前の版は両腕とも破局を 138 と決め打っており、**見かけの破局率の差が零**だった。
    つまり正本 `dilution_gate.why` の因果は一度も作られていなかったのに、経路の表は発火したと書いていた。
    いまは「答えられた試行のうちの破局の率を同じにし、書式外だけを増やす」——
    すると全分母の破局率は書式外の多い腕で下がる（＝希釈）。"""
    m = base_main_spec()
    ff_hi, ff_lo, p_cat = 60, 4, 0.72        # 答えられた試行のうちの破局の率は同じ
    m[('N1', 'Onull+v')] = {'cat': int(round((200 - ff_hi) * p_cat)), 'refuse': 10, 'ff': ff_hi,
                            'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('N1', 'Onull+vrand')] = {'cat': int(round((200 - ff_lo) * p_cat)), 'refuse': 10, 'ff': ff_lo,
                                'style_a': 40, 'style_b': 120, 'mention': 8}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_incomplete():
    """品質床の走行の記録が欠けた場合（**記録の不在は「操作不能」ではない**・採否表 P272）。"""
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12},
            'quality': {'fail_selection': [], 'fail_post': [], 'drop_selection': [(LAYERS[0], COEFS[0])]}}


CASES = {'incomplete': case_incomplete, 'all': case_all, 'gate1_closed': case_gate1_closed, 'nonpositive': case_nonpositive, 'tie': case_tie,
         'censor_candidates': case_censor_candidates, 'scoring_gap': case_scoring_gap, 's4_branches': case_s4_branches,
         's4_floor': case_s4_floor, 'dilution_causal': case_dilution_causal}


def build(case, out_root):
    spec = CASES[case]()
    if os.path.isdir(out_root):
        shutil.rmtree(out_root)
    os.makedirs(out_root, exist_ok=True)
    # ---- 本走行 ----
    resume = spec.get('resume')                     # {'scenario': 'N1', 'arm': 'Onull+vtd'} なら、その腕を二つのセッションに分ける
    for sc in SC:
        _pick = spec['tune'].get('best') or (LAYERS[1], COEFS[1])
        man = {'scenario': sc, 'session': 1, 'n': N_MAIN, 'seed': T['seeds']['main'][sc],
               'arms': T['arms']['by_scenario'][sc], 'batch': T['runner']['batch'], 'layer': _pick[0], 'coef': _pick[1]}
        trials, tail = [], []
        for arm in T['arms']['by_scenario'][sc]:
            s_ = spec['main'][(sc, arm)]
            rk = '%s__%s__s1' % (T['tags']['main'], sc)
            if resume and resume.get('scenario') == sc and resume.get('arm') == arm:
                half = N_MAIN // 2
                trials += cell_trials(half, s_, start=0, arm=arm, scenario=sc, tag=T['tags']['main'], seed=T['seeds']['main'][sc], run_key=rk)
                tail += cell_trials(N_MAIN - half, s_, start=half, arm=arm, scenario=sc, tag=T['tags']['main'],
                                    seed=T['seeds']['main'][sc], run_key='%s__%s__s2' % (T['tags']['main'], sc))
            else:
                trials += cell_trials(N_MAIN, s_, arm=arm, scenario=sc, tag=T['tags']['main'], seed=T['seeds']['main'][sc], run_key=rk)
        write_run(out_root, T['tags']['main'], '%s__s1' % sc, man, trials)
        if tail:
            write_run(out_root, T['tags']['main'], '%s__s2' % sc, dict(man, session=2, arms=[resume['arm']]), tail)

    # ---- 同一性選別（三スタック・採否表 P302）----
    idt = T['tags']['identity']
    for stack in T['identity_screen']['stacks']:
        for arm in T['identity_screen']['arms_run']:
            trials = cell_trials(T['identity_screen']['n'], {'cat': 40, 'refuse': 6, 'ff': 4, 'style_a': 20, 'style_b': 90, 'mention': 5},
                                 arm=arm, scenario=T['identity_screen']['scenario'], tag=idt, seed=T['seeds']['identity_transformers'],
                                 run_key='%s__%s__%s' % (idt, stack, arm))
            write_run(out_root, idt, '%s__%s' % (stack, arm), {'stack': stack, 'scenario': T['identity_screen']['scenario'],
                                                               'n': T['identity_screen']['n'], 'seed': T['seeds']['identity_transformers'],
                                                               'arms': [arm], 'session': 1}, trials)

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
        trials = cell_trials(N_Q, {'correct': 150, 'ff': 2}, arm=base, scenario='quality', tag=tag_q, seed=T['seeds']['quality'], sampling=T['quality_floor']['generation'],
                             run_key='%s__noop__%s' % (tag_q, base))
        write_run(out_root, tag_q, 'selection__%s__noop' % base, {'stage': 'selection', 'arm': base, 'layer': None, 'coef': None, 'n': N_Q,
                                                                  'seed': T['seeds']['quality']}, trials)
    for base in QF_ARMS:
        arm = base + QF_OPS[base]
        for (l, c) in CANDS:
            if (l, c) in (q.get('drop_selection') or []):
                continue                      # 走行の記録を作らない（記録の不在）
            bad = (q['fail_selection'] == 'all') or (arm in (q['fail_selection'] or []))
            trials = cell_trials(N_Q, {'correct': 100 if bad else 148, 'ff': 2}, arm=arm, scenario='quality', tag=tag_q, sampling=T['quality_floor']['generation'],
                                 seed=T['seeds']['quality'], layer=l, coef=c, run_key='%s__%s__L%sC%s' % (tag_q, arm, l, c))
            write_run(out_root, tag_q, 'selection__%s__L%sC%s' % (arm, l, c), {'stage': 'selection', 'arm': arm, 'layer': l, 'coef': c,
                                                                              'n': N_Q, 'seed': T['seeds']['quality']}, trials)
    pick = spec['tune'].get('best') or (LAYERS[1], COEFS[1])
    for arm in INTERV:
        bad = arm in (q['fail_post'] or [])
        trials = cell_trials(N_Q, {'correct': 100 if bad else 148, 'ff': 2}, arm=arm, scenario='quality', tag=tag_q, sampling=T['quality_floor']['generation'],
                             seed=T['seeds']['quality'], layer=pick[0], coef=pick[1], run_key='%s__post__%s' % (tag_q, arm))
        write_run(out_root, tag_q, 'post__%s' % arm, {'stage': 'post', 'arm': arm, 'layer': pick[0], 'coef': pick[1], 'n': N_Q,
                                                      'seed': T['seeds']['quality']}, trials)
    for base in sorted(set(NOOP_BASE.values())):
        trials = cell_trials(N_Q, {'correct': 150, 'ff': 2}, arm=base, scenario='quality', tag=tag_q, seed=T['seeds']['quality'], sampling=T['quality_floor']['generation'],
                             run_key='%s__post__noop__%s' % (tag_q, base))
        write_run(out_root, tag_q, 'post__%s__noop' % base, {'stage': 'post', 'arm': base, 'layer': None, 'coef': None, 'n': N_Q,
                                                             'seed': T['seeds']['quality']}, trials)
    # ---- セッション記録 ----
    sd = os.path.join(out_root, 'sessions-B')
    os.makedirs(sd, exist_ok=True)
    for sc in SC:
        for sess in (1, 2):
            rk = '%s__%s__s%d__dryrun' % (T['tags']['main'], sc, sess)
            if not os.path.isdir(os.path.join(out_root, T['tags']['main'], rk)):
                continue
            json.dump({'tag': T['tags']['main'], 'session': sess, 'scenario': sc, 'gpu': 'synth', 'batch': T['runner']['batch'],
                       'run_keys': [rk], 'dry_run': True},
                      open(os.path.join(sd, '%s__%s__s%d.json' % (T['tags']['main'], sc, sess)), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
    # **すべての走行キーにセッション記録を書く**（正本 sessions.missing_rule・裁定 D108・採否表 P313）。
    # 前は本走行の分しか書いておらず、品質床と調整走行と同一性選別の走行キーには記録が無かった。
    for tg in (T['tags']['tune'], T['tags']['quality'], T['tags']['identity']):
        d = os.path.join(out_root, tg)
        if not os.path.isdir(d):
            continue
        for rk in sorted(os.listdir(d)):
            if not os.path.isdir(os.path.join(d, rk)):
                continue
            mf = [f for f in os.listdir(os.path.join(d, rk)) if f.startswith('manifest')]
            sess = json.load(open(os.path.join(d, rk, mf[0]), encoding='utf-8')).get('session', 1) if mf else 1
            json.dump({'tag': tg, 'session': sess, 'gpu': 'synth', 'batch': T['runner']['batch'],
                       'run_keys': [rk], 'dry_run': True},
                      open(os.path.join(sd, '%s.json' % rk), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
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
```

## `tools/dry_run_B.py`（SHA16 80CACAC6C0A7DE0A・163 行）

```python
# -*- coding: utf-8 -*-
"""dry_run_B.py v3 —— 段階 B の器材の**合成データによる検査**（札の全経路を一度ずつ以上発火させる）。

器材の整備の計画 `records/B/tooling-plan-B-2026-09-18.md` の表の経路を、合成データ（`synth_B.py`）で作り、
`gate_B.py`（門1 と選定）と `analyze_B.py`（本走行の集計と札）を走らせて、**どの経路が発火したか**を数える。
発火しない経路があれば非零で終わる（凍結の前に全経路が発火していることが条件）。
合成データは results/_synth/ に置き、行にも置き場にも dry-run の印を立てる（公開の置き場には入れない）。
出力: records/B/dry-run-B-<日付>.md（--out で変える・--force が無ければ上書きしない）。
用法: python tools/dry_run_B.py [--keep] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, argparse, datetime, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

T = runs_B.load_T()

VERSION = 'v3'
REPO = runs_B.REPO
PY = sys.executable
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--keep', action='store_true', help='合成データを消さない')
a = ap.parse_args()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'dry-run-B-%s.md' % jst.strftime('%Y-%m-%d'))
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)

PATHS = ['確証', '確証（登録された向きと逆）', '封印した符号と一致', '判定不能（検閲）', '判定不能（採点欠落）', '判定不能（測れなかった）',
         '判定保留（書式外転位）', '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '注（様式）',
         '判定不能（品質床）', '非有意', '門1 を閉じる', '記録の不在（incomplete）', '全候補が非正', '同点の割り方',
         '床・天井で選定から外す', 'S4: 下がった（外れ）', 'S4: 下がらなかった（当たり）', 'S4: 当否を言わない', 'S4: 余地の条項',
         '希釈が効く場面（書式外が分子を食う）', '採点の規約（書式外と refuse に判定を付けない）', '門が開いていないと集計器が止まる', '束縛の食い違いで集計器が止まる',
         '中断と再開', '同一性選別の走行', '未測定（ループ・打ち切り）', '封印の欠けで止まる']
fired = {k: [] for k in PATHS}
rows = []


def run(cmd):
    r = subprocess.run([PY] + cmd, capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


for case in ('all', 'gate1_closed', 'nonpositive', 'tie', 'censor_candidates', 'scoring_gap', 's4_branches', 's4_floor', 'dilution_causal', 'incomplete'):
    root = os.path.join('results', '_synth', case)
    rc, out = run(['tools/synth_B.py', '--case', case, '--out-root', root])
    assert rc == 0, out
    rc_g, out_g = run(['tools/gate_B.py', '--root', root, '--allow-dry', '--out', os.path.join(root, 'gate-B.md'), '--force'])
    assert rc_g in (0, 2), ('門の器が思わぬ終了コードで落ちた', rc_g, out_g[-400:])   # 採否表 P296
    G = json.load(open(os.path.join(REPO, root, 'gate-B.json'), encoding='utf-8'))
    if G['verdict'] == 'incomplete':
        fired['記録の不在（incomplete）'].append(case)
    sel = G['selection']
    if not G['gate1']['open']:
        fired['門1 を閉じる'].append(case)
    if sel.get('nonpositive_stop'):
        fired['全候補が非正'].append(case)
    if sel.get('tie_note'):
        fired['同点の割り方'].append(case)
    if any(r.get('censored') for r in G['candidates']):
        fired['床・天井で選定から外す'].append(case)
    rec = {'case': case, 'gate_verdict': G['verdict'], 'gate_rc': rc_g, 'labels': {}}
    if G['gate1']['open']:
        seal = os.path.join(root, 'seal-B.json')
        cmd = ['tools/analyze_B.py', '--gate', os.path.join(root, 'gate-B.json'), '--root', root, '--allow-dry',
               '--out', os.path.join(root, 'analysis-B.md'), '--force']
        if os.path.exists(os.path.join(REPO, seal)):
            # 合成の封印は全対比ぶんではないので、**まず止まることを確かめてから**検査用の口で進む（裁定 D79・採否表 P277）
            rc_stop, _ = run(cmd + ['--seal', seal])
            if rc_stop != 0:
                fired['封印の欠けで止まる'].append(case)
            cmd += ['--seal', seal, '--allow-partial-seal']
        # **門が開いていなければ止まることを先に確かめる**（裁定 D109・採否表 P315）
        if G.get('verdict') != 'open':
            rc_stop2, _ = run(cmd)
            if rc_stop2 != 0:
                fired['門が開いていないと集計器が止まる'].append(case)
            cmd += ['--allow-not-open']
        # **束縛の食い違いで止まることを確かめる**（裁定 D105・採否表 P304）。
        # 合成データの走行は場合ごとの「best」で作るが、門が実際に選ぶ組はそれと違うことがある
        # （候補が希釈や床・天井で外れる場合）。そのとき集計器は止まるのが正しい。
        rc_b, out_b = run(cmd)
        if rc_b != 0 and '門の選んだ層 × 係数と違う' in out_b:
            fired['束縛の食い違いで集計器が止まる'].append(case)
            cmd += ['--allow-unbound']
        rc_a, out_a = run(cmd)
        assert rc_a == 0, out_a
        A = json.load(open(os.path.join(REPO, root, 'analysis-B.json'), encoding='utf-8'))
        for r in A['confirm']:
            lab = r.get('label')
            if lab in fired:
                fired[lab].append(case)
            rec['labels'][lab] = rec['labels'].get(lab, 0) + 1
            if any('注（様式' in n for n in (r.get('notes') or [])):
                fired['注（様式）'].append(case)
        v4 = A['s4'].get('verdict') or ''
        for nm, key in (('S4: 下がった（外れ）', '下がった'), ('S4: 下がらなかった（当たり）', '下がらなかった'),
                        ('S4: 当否を言わない', '当否を言わない'), ('S4: 余地の条項', '余地の条項')):
            if key in v4:
                fired[nm].append('%s（%s）' % (case, v4))
        if (A['sign_agreement'].get('agree') or 0) > 0:
            fired['封印した符号と一致'].append(case)
        rec['s4'] = A['s4'].get('verdict')
        rec['sign_agreement'] = A['sign_agreement']
    # 合成データの中身から確かめる経路（採否表 P300〜P302）
    import glob as _g
    mainroot = os.path.join(REPO, root, T['tags']['main'])
    if os.path.isdir(mainroot):
        sess = {json.load(open(os.path.join(d, 'manifest.json'), encoding='utf-8')).get('session') for d in _g.glob(os.path.join(mainroot, '*'))}
        if len(sess) > 1:
            fired['中断と再開'].append(case)
        ff_cat = unmeas = 0
        for d in _g.glob(os.path.join(mainroot, '*')):
            for f in _g.glob(os.path.join(d, 'trials-*.jsonl')):
                for line in open(f, encoding='utf-8'):
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    if r.get('format_fail') and r.get('catastrophe'):
                        ff_cat += 1
                    if r.get('loop_flag') or r.get('truncated'):
                        unmeas += 1
        if unmeas:
            fired['未測定（ループ・打ち切り）'].append(case)
        if case == 'dilution_causal':
            # **恒真にしない**（裁定 D111・採否表 P309）。書式外の差・見かけの破局率の差・札の三つがそろって初めて発火。
            cc = runs_B.counts_main(T, root=root, allow_dry=True)[0]
            v, r = cc.get(('N1', 'Onull+v')), cc.get(('N1', 'Onull+vrand'))
            if v and r:
                ff_d = abs(100.0 * v['ff'] / v['n_ok'] - 100.0 * r['ff'] / r['n_ok'])
                cat_d = 100.0 * r['cat'] / r['n_ok'] - 100.0 * v['cat'] / v['n_ok']
                lab = [x.get('label') for x in (A.get('confirm') or []) if 'Onull+v~Onull+vrand' in str(x.get('id'))]
                if ff_d >= T['dilution_gate']['threshold_pt'] and cat_d > 0 and any('書式外転位' in str(x) for x in lab):
                    fired['希釈が効く場面（書式外が分子を食う）'].append(case)
        if ff_cat == 0:
            fired['採点の規約（書式外と refuse に判定を付けない）'].append(case)
    if os.path.isdir(os.path.join(REPO, root, T['tags']['identity'])):
        fired['同一性選別の走行'].append(case)
    rows.append(rec)

missing = [k for k, v in fired.items() if not v]
L = ['# 段階 B 器材の合成データによる検査（機械生成・`tools/dry_run_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 合成データは `results/_synth/<場合>/`（行にも置き場にも dry-run の印・公開の置き場には入れない）。',
     '- 正本 SHA16 %s。**発火しなかった経路 %d 件**。' % (runs_B.sha16_file(runs_B.CPATH), len(missing)), '',
     '| 経路 | 発火した場合 |', '|---|---|']
for k in PATHS:
    L.append('| %s | %s |' % (k, '・'.join(sorted(set(fired[k]))) or '**発火せず**'))
L += ['', '## 場合ごとの結果', '', '| 場合 | 門の判定 | 札の内訳 | S4 | 符号の一致 |', '|---|---|---|---|---|']
for r in rows:
    L.append('| %s | %s | %s | %s | %s |' % (r['case'], r['gate_verdict'],
                                             '・'.join('%s %d' % (k, v) for k, v in sorted(r['labels'].items())) or '—',
                                             r.get('s4') or '—', r.get('sign_agreement') or '—'))
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
if not a.keep:
    shutil.rmtree(os.path.join(REPO, 'results', '_synth'), ignore_errors=True)
print('[dry_run_B] %s | 発火しなかった経路 %d' % (out_md, len(missing)))
if missing:
    print('  未発火: ' + '・'.join(missing))
sys.exit(1 if missing else 0)
```

## `tools/build_report_B.py`（SHA16 7A2C497EDCF2C2B5・167 行）

```python
# -*- coding: utf-8 -*-
"""build_report_B.py v3 —— 段階 B の結果報告を、**雛形**（`records/B/results-report-template-B.md`）と集計の出力から組み立てる。

雛形の〔結果 X〕を、機械の区画で置き換える:
  A 要約／B 走行の記録（整合検査・抽出検査・セッション）／C 門1 と選定／D 確証の族の表／E 封印した符号との照合／
  F 記述の族／G S4 の反証／H 利益相反と情報状態
**散文に手計算の数を残さない**（正本 `report_rules.typed_numbers`）。数はすべて集計の json から来る。
組み立ての後に走査器（`tools/report_lint.py`）を走らせる口を持つ（--lint）。
用法: python tools/build_report_B.py --analysis records/B/analysis-B-<日付>.json --gate records/B/gate-B-<日付>.json \
        [--integrity records/B/integrity-stageB-<日付>.json] [--out records/B/results-report-B.md] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v3'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--analysis', required=True)
ap.add_argument('--gate', required=True)
ap.add_argument('--integrity', required=True, help='tools/integrity_B.py の json（必須・採否表 P293）')
ap.add_argument('--sampling', required=True, help='抽出検査の封印 json（必須・採否表 P293）')
ap.add_argument('--allow-dry', action='store_true', help='検査用の口（合成データから組む・区画ごとに印を差し込む）')
ap.add_argument('--force-problems', action='store_true', help='整合検査に不整合があっても組む（理由を記録に残すこと）')
ap.add_argument('--template', default=os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--lint', action='store_true', help='組み立ての後に報告の走査器（tools/report_lint.py）を走らせる（裁定 D112・採否表 P320）')
a = ap.parse_args()
T = runs_B.load_T()
A = runs_B.read_json(a.analysis)
G = runs_B.read_json(a.gate)
INT = runs_B.read_json(a.integrity) if a.integrity else None
SMP = runs_B.read_json(a.sampling) if a.sampling else None
assert A.get('kind') == 'analyze_B' and G.get('kind') == 'gate_B', '集計または門の記録の種類が違う'
DRY = A.get('dry_marks') or []
if DRY and not a.allow_dry:
    sys.exit('**合成データ（dry-run の印つき）から報告を組もうとしている**: %s。検査用は --allow-dry（採否表 P279）' % '・'.join(DRY))
if INT and INT.get('problems') and not a.force_problems:
    sys.exit('整合検査に不整合が %d 件ある。直してから報告を組む（--force-problems は理由を記録に残す場合のみ・採否表 P293）' % len(INT['problems']))
MARK = ('【合成データ・本番ではない】' if DRY else '')
out_md = a.out or os.path.join(REPO, 'records', 'B', 'results-report-B.md')
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
tpl = open(a.template, encoding='utf-8').read()
PS = T['print_strings']
c = A['counts']
n_conf = sum(x['m'] for x in T['families'].values())


def block(lines):
    """機械の区画。合成データから組んだときは**区画ごとに**印を差し込む（切り出しで落ちないように・採否表 P279）。"""
    out = [l for l in lines if l is not None]
    if MARK:
        out = [MARK] + out
    return '\n'.join(out)


A_sum = block([
    '```',
    PS['first_finding'].format(confirmed=c['確証'], undecidable=c['判定不能（検閲）'], qfloor=c['判定不能（品質床）'],
                               gap=c['判定不能（採点欠落）'], nodata=c['判定不能（測れなかった）'],
                               ff=c['判定保留（書式外転位）'], refuse=c['判定保留（refuse 転位）'] + c['判定保留（refuse 転位・差）'],
                               style=c['判定保留（様式転位）'], ns=c['非有意']),
    PS['scope'],
    'S4 の反証: %s' % A['s4'].get('verdict'),
    '```'])
B_run = block(['```',
               '整合検査: 不整合 %d 件・注 %d 件（%s）' % (len(INT['problems']), len(INT['notes']), INT['tag']),
               '抽出検査: 標本 %d 件・対応表の封印あり（並べ替え %s）' % (SMP.get('n_items', 0), SMP.get('shuffled')),
               '正本 SHA16 %s・集計 %s UTC' % (A['contrasts_sha16'], A['generated_utc']),
               '```'])
sel = G['selection']['pick'] or {}
C_gate = block(['```',
                (PS['gate1_open'].format(k=G['gate1']['quality_pass_candidates'], layer=sel.get('layer'), coef=sel.get('coef'),
                                         eff=sel.get('eff_pt'), tied=len(G['selection']['tied']))
                 if G['gate1']['open'] else PS['gate1_closed']),
                PS['selection_coi'], PS['selection_direction'],
                ('同値の帯: 幅 %s pt（帰無の模擬 %s 回・同値の候補 %d 組）' % (G['selection']['equivalence_band']['q95_pt'],
                                                                format(G['selection']['equivalence_band']['reps'], ','),
                                                                len(G['selection']['tied'])) if G['selection'].get('equivalence_band') else ''),
                (G['selection'].get('tie_note') or ''), (G['selection'].get('nonpositive_stop') or ''),
                '```'])
fmt_p = lambda x: ('—' if x is None else ('%.3g' % x if x >= 1e-5 else '<1e-5'))
fmt_n = lambda x: ('—' if x is None else ('%g' % round(float(x), 4)))      # 丸めない浮動小数を報告に出さない（採否表 P328）

# **雛形の数を正本から組み直して突き合わせる**（裁定 D112・採否表 P319）。
_src = os.path.splitext(a.template)[0] + '.src.md'
if os.path.exists(_src):
    import subprocess, tempfile as _tf, shutil as _sh
    _d = _tf.mkdtemp(prefix='tplchk_')
    try:
        _o, _l = os.path.join(_d, 't.md'), os.path.join(_d, 'l.md')
        _rc = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'build_draftB.py'), '--kind', 'template',
                              '--src', _src, '--out', _o, '--label', '報告雛形', '--lint-report', _l],
                             capture_output=True, text=True, encoding='utf-8').returncode
        if _rc == 0 and runs_B.sha16_file(_o) != runs_B.sha16_file(a.template):
            sys.exit('雛形が正本から組み直した版と違う（正本が動いた後に雛形を組み直していない・裁定 D112）: '
                     '現物 %s / 組み直し %s' % (runs_B.sha16_file(a.template), runs_B.sha16_file(_o)))
    finally:
        _sh.rmtree(_d, ignore_errors=True)
rows = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | 書式外 A／B | refuse A／B | pt 差 | 区間 | p | 様式の差 | 札 | 注 |',
        '|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in A['confirm']:
    if r.get('missing'):
        rows.append('| %s | %s | — | — | — | — | — | — | — | — | %s | |' % (r['id'], r['scenario'], r['label']))
        continue
    rows.append('| %s | %s | %d/%d | %d/%d | %s／%s | %s／%s | %s | %s | %s | %s | %s | %s |'
                % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'],
                   fmt_n(r.get('ff_pt_A')), fmt_n(r.get('ff_pt_B')), fmt_n(r.get('refuse_pt_A')), fmt_n(r.get('refuse_pt_B')),
                   r['diff_pt'], r['ci'], fmt_p(r.get('p')), r.get('style_diff_pt'), r['label'],
                   '・'.join(r.get('notes') or [])))
D_conf = block(rows)
sg = A['sign_agreement']
E_sign = block(['```', (PS['sign_agreement'].format(agree=sg['agree'], confirmed=sg.get('checked')) if sg['sealed']
                        else '封印の記録が渡されていないので、予想符号との照合は行っていない。'),
                ('照合できなかった確証の対比: %s' % (sg.get('unchecked') or 'なし')) if sg['sealed'] else None,
                ('封印の欠け: %d 件' % len(sg.get('seal_missing') or [])) if sg['sealed'] else None, '```'])
F_desc = []
for fam, rs in A['descriptive'].items():
    if not rs:
        continue
    F_desc += ['**%s**' % fam, '', '| 対比 | 破局率 A | 破局率 B | pt 差 | 区間 |', '|---|---|---|---|---|']
    for r in rs:
        if r.get('missing'):
            F_desc.append('| %s | — | — | — | — |' % r['id'])
        else:
            F_desc.append('| %s | %s | %s | %s | %s |' % (r['id'], None if r['rate_A'] is None else round(r['rate_A'], 4),
                                                          None if r['rate_B'] is None else round(r['rate_B'], 4), r['diff_pt'], r['ci']))
    F_desc.append('')
F_desc.append(PS['no_p_desc'])
s4 = A['s4']
G_s4 = block(['```', '判定: %s' % s4.get('verdict'),
              ('pt 差 %s・区間 %s・相手の腕の率 %s・%s pt の検出力 %s（線は %s）'
               % (s4.get('diff_pt'), s4.get('ci'), s4.get('partner_rate'), s4.get('effect_pt'), s4.get('power_at_effect'), s4.get('power_min'))
               if s4.get('power_at_effect') is not None else '検出力は出さない（余地の条項または低下の余地が無い・裁定 D95）'),
              '封印: %s' % s4.get('sealed_prediction'), '```'])
H_coi = block(['```', T['selection']['coi_note'], T['publication']['dual_use'],
               '率盲検の外の経路: 同一性選別の距離／調整走行の率（選定に要る）／品質床の得点。本走行の率は整合検査まで見ない。',
               '起草者は段階 A の公開結果を見ている（封印予想の情報状態の欄に記す）。', '```'])

for ph, txt in (('A', A_sum), ('B', B_run), ('C', C_gate), ('D', D_conf), ('E', E_sign), ('F', block(F_desc)), ('G', G_s4), ('H', H_coi)):
    key = '〔結果 %s〕' % ph
    if key not in tpl:
        sys.exit('雛形に %s が無い' % key)
    tpl = tpl.replace(key, txt)
tpl += '\n\n## 11. 組み立ての記録（機械）\n\n- 器 `tools/build_report_B.py` %s・%s UTC。集計 `%s`（SHA16 %s）・門 `%s`（SHA16 %s）。\n' % (
    VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
    os.path.relpath(a.analysis, REPO).replace('\\', '/'), runs_B.sha16_file(a.analysis),
    os.path.relpath(a.gate, REPO).replace('\\', '/'), runs_B.sha16_file(a.gate))
open(out_md, 'w', encoding='utf-8', newline='\n').write(tpl)
if a.lint:
    # **報告の走査器を走らせる**（裁定 D112・採否表 P320）。前は口上が持つと書いて argparse に口が無かった。
    import subprocess
    lint = os.path.join(REPO, 'tools', 'report_lint.py')
    if not os.path.exists(lint):
        sys.exit('報告の走査器が無い: tools/report_lint.py')
    side = os.path.splitext(out_md)[0] + '-machine.json'
    cmd = [sys.executable, lint, out_md, '--contrasts', runs_B.CPATH, '--template', a.template]
    if os.path.exists(side):
        cmd += ['--sidecar', side]
    rcl = subprocess.run(cmd).returncode
    if rcl != 0:
        sys.exit('報告の走査器が違反を出した（終了コード %d）' % rcl)

print('[build_report_B] %s' % out_md)
```

## `tools/freeze_B.py`（SHA16 097A4BEAFD8C3663・153 行）

```python
# -*- coding: utf-8 -*-
"""freeze_B.py v3 —— 段階 B の**凍結の記帳**（凍結物の SHA・封印予想・凍結時に記帳する値・逸脱台帳の口）。

凍結するもの（正本 `publication.record_first`・草案8B §2.11）:
  凍結本文（草案）・正本 `design/contrasts-B.json`・腕と方向の定義・器材・報告の雛形・**封印予想**。
凍結時に記帳する値（設計の段では書けないもの）:
  - 重みの rev・tokenizer の版・**総層数**（`selection.candidates.layer_index_rule`）と層の添字
  - **腕ごとのトークン長**（裁定 D82・`position_length.record_at_freeze`）
  - 品質床の課題の出所・版・ライセンス・断片の SHA（裁定 D66）と、入力・帯・採点・最大トークン数（採否表 P216）
  - v̂ の SHA（`selection.vector_fix`）と方向の要約統計（ノルム・コサイン・場面間の安定性）
封印予想（`seal_format`）: 確証の各対比の符号と S4 の反証。**B のデータを一つも見る前**に書き、情報状態と時機を添える。
凍結の後の変更はすべて**逸脱**とし、番号・日付・理由・登録者の承認を記帳する（`deviation.rule`）。
出力: records/B/FREEZE-RECORD-B.md と同 .json（--force が無ければ上書きしない）。
用法: python tools/freeze_B.py --draft design/design-stageB-draft10.md [--seal records/B/seal-B.json] [--values records/B/freeze-values-B.json] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v3'
REPO = runs_B.REPO
CARRYOVER = {'凍結走行器（組み立てと採点の型）': 'tools/run_preamble_local.py',
             '凍結パーサ': 'arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py',
             '場面の素材': 'arms/frozen-from-ryokai-os/app-scenarios.json'}
TOOLS = ['runs_B.py', 'make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py', 'numbers_lint.py', 'gate_B.py', 'analyze_B.py',
         'integrity_B.py', 'sample_inspection_B.py', 'direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'synth_B.py',
         'dry_run_B.py', 'build_report_B.py', 'freeze_B.py', 'control_chart_B.py']
NEED_VALUES = ['model_rev', 'tokenizer_rev', 'num_hidden_layers', 'layer_indices', 'arm_token_lengths',
               'quality_task', 'quality_input', 'quality_apply_band', 'quality_scoring', 'quality_max_tokens',
               'v_hat_sha256', 'direction_stats']
ap = argparse.ArgumentParser()
ap.add_argument('--draft', required=True)
ap.add_argument('--seal', default=None)
ap.add_argument('--values', default=None, help='凍結時に記帳する値（json・上の NEED_VALUES）')
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-missing', action='store_true', help='記帳の値や封印が揃っていなくても書く（**凍結ではなく点検用**）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
cpath = a.contrasts or runs_B.CPATH
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'FREEZE-RECORD-B.md')
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

frozen = {'canon': {'path': 'design/contrasts-B.json', 'sha16': runs_B.sha16_file(cpath), 'version': T['version']},
          'draft': {'path': os.path.relpath(a.draft, REPO).replace('\\', '/'), 'sha16': runs_B.sha16_file(a.draft)},
          'facts': {'path': 'records/B/design-facts-B.md', 'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'))},
          'report_template': {'path': 'records/B/results-report-template-B.md',
                              'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))},
          'arms': T['arms']['sha16'], 'arm_files': T['arms'].get('files'),
          'tools': {}}
for t in TOOLS:
    p = os.path.join(REPO, 'tools', t)
    frozen['tools'][t] = runs_B.sha16_file(p) if os.path.exists(p) else None
frozen['carryover'] = {}
for name, rel in CARRYOVER.items():
    p = os.path.join(REPO, *rel.split('/'))
    frozen['carryover'][name] = {'path': rel, 'sha16': runs_B.sha16_file(p) if os.path.exists(p) else None}
missing_carry = [n for n, v in frozen['carryover'].items() if not v['sha16']]
missing_tools = [t for t, v in frozen['tools'].items() if v is None]

VALUES = runs_B.read_json(a.values) if a.values else {}
missing_values = [k for k in NEED_VALUES if k not in VALUES or VALUES[k] in (None, '', [], {})]   # **空も欠けと見る**（採否表 P282）
SEAL = runs_B.read_json(a.seal) if a.seal else None
conf_ids = [c['id'] for F in T['families'].values() for c in F['contrasts']]
missing_seal = [] if not SEAL else [i for i in conf_ids if i not in (SEAL.get('signs') or {})]
blockers = []
if missing_tools:
    blockers.append('器材が揃っていない: %s' % '・'.join(missing_tools))
if missing_carry:
    blockers.append('B が依存する凍結物が見つからない: %s' % '・'.join(missing_carry))
if missing_values:
    blockers.append('凍結時に記帳する値が揃っていない: %s' % '・'.join(missing_values))
if SEAL is None:
    blockers.append('封印予想が渡されていない（`seal_format` の様式で、データを一つも見る前に書く）')
else:
    if missing_seal:
        blockers.append('封印の無い確証の対比: %s' % '・'.join(missing_seal))
    if not SEAL.get('s4'):
        blockers.append('**S4 の反証の封印が無い**（正本 seal_format.scope は確証の族と S4 の両方を対象にする）')
    # **正本の鍵の登録から見る**（手書きの並びを置かない・裁定 D115・採否表 P328）
    for need, label in sorted(T['seal_format']['record_keys'].items()):
        if need in ('signs', 's4'):
            continue                      # 上で別に見ている
        if not SEAL.get(need):
            blockers.append('封印の記録に欄が無い: %s（%s・seal_format.record_keys）' % (need, label))
# 整備の記録に載る SHA16 が現物と一致するかを見る（実装検分の採否表 P299——古い記録のまま凍結しない）。
# **止める門の前に置く**（裁定 D112・採否表 P321）。前は門の後ろにあったので、古い記録だけのときに
# 記録が書かれ、しかも「点検であり凍結ではない」と事実でないことを書いていた。
import re as _re
rec_path = os.path.join(REPO, 'records', 'B', 'tooling-record-B-2026-09-18.md')
stale, unlisted = [], []
if os.path.exists(rec_path):
    _txt = open(rec_path, encoding='utf-8').read()
    _listed = dict(_re.findall(r'`tools/([\w.]+)` \| [^|]*\| ([0-9A-F]{16})', _txt))
    for _name, _sha in _listed.items():
        _p = os.path.join(REPO, 'tools', _name)
        if os.path.exists(_p) and runs_B.sha16_file(_p) != _sha:
            stale.append(_name)
    unlisted = [t for t in TOOLS if t not in _listed]
if stale:
    blockers.append('器材の整備の記録の SHA16 が現物と違う（記録を作り直してから凍結する）: %s' % '・'.join(stale))
if unlisted:
    blockers.append('器材の整備の記録に載っていない器材がある（記録に足す）: %s' % '・'.join(unlisted))

if blockers and not a.allow_missing:
    print('[freeze_B] 凍結できない（--allow-missing は点検用）:')
    for b in blockers:
        print('  - ' + b)
    sys.exit(1)

REC = {'kind': 'freeze_B', 'version': VERSION, 'frozen_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'frozen_jst': jst.strftime('%Y-%m-%d %H:%M'),
       'frozen': frozen, 'values': VALUES, 'seal': SEAL, 'seal_sha256': (None if not a.seal else __import__('hashlib').sha256(open(a.seal, 'rb').read()).hexdigest().upper()),
       'stale_record_hashes': stale, 'unlisted_tools': unlisted, 'blockers': blockers, 'deviations': [],
       'deviation_rule': T['deviation']['rule'], 'record_first': T['publication']['record_first']}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 凍結記録（機械生成・`tools/freeze_B.py` %s）' % VERSION, '',
     '- 凍結の時刻: %s UTC（日本時間 %s）。%s' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'),
                                            ('**点検（--allow-missing）であり凍結ではない**' if a.allow_missing else
                                             ('**止めているものがある——凍結していない**' if blockers else '凍結した。'))), '',
     '## 凍結物', '', '| 物 | 置き場 | SHA16 |', '|---|---|---|']
for k in ('canon', 'draft', 'facts', 'report_template'):
    L.append('| %s | `%s` | %s |' % (k, frozen[k]['path'], frozen[k]['sha16']))
for t, v in sorted(frozen['tools'].items()):
    L.append('| 器材 | `tools/%s` | %s |' % (t, v or '**無い**'))
for name, v in sorted(frozen['carryover'].items()):
    L.append('| 持ち越しの凍結物 | `%s` | %s |' % (v['path'], v['sha16'] or '**無い**'))
for arm, sha in sorted((frozen['arms'] or {}).items()):
    L.append('| 腕 | %s | %s |' % (arm, sha or '（前置きを持たない）'))
L += ['', '## 凍結時に記帳する値', '']
for k in NEED_VALUES:
    L.append('- %s: %s' % (k, json.dumps(VALUES[k], ensure_ascii=False) if k in VALUES else '**まだ無い**'))
L += ['', '## 封印予想（`seal_format`）', '']
if SEAL:
    L += ['- 時機: %s' % T['seal_format']['timing'], '- 情報状態: %s' % T['seal_format']['information_state'],
          '- 封印した符号: %d／確証の対比 %d' % (len(SEAL.get('signs') or {}), len(conf_ids)),
          '- S4 の反証: %s' % (SEAL.get('s4') or '**まだ無い**'), '- %s' % T['seal_format']['reading']]
else:
    L.append('- **まだ無い**（`seal_format` の様式で、データを一つも見る前に書く）')
if blockers:
    L += ['', '## 凍結を止めているもの', ''] + ['- ' + b for b in blockers]
L += ['', '## 逸脱台帳', '', '- %s' % T['deviation']['rule'], '- %s' % T['deviation']['silent_fix'], '- （凍結の後に足す）', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[freeze_B] %s | 止めているもの %d 件' % (out_md, len(blockers)))
sys.exit(2 if blockers else 0)
```
