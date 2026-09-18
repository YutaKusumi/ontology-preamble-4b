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
    # **正本の語彙で書く**（裁定 D121・2026-09-18）。前は集計器の内部の記号で書いていたので、
    # 「正本どおりに封印すると確証がすべて逆向きになる」食い違いが合成データでは一度も発火しなかった。
    seal = {'sub:N1:O-Ncold-v~O-Ncold-vrand': '上昇',          # データは低下——逆向きの枝
            'add:N1:Onull+v~Onull+vrand': '低下'}              # データも低下——一致の枝
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


def case_s4_up():
    """S4 の「**上がった（封印は当たり）**」の枝（裁定 D130・採否表 P371）。

    (6b) の腕のほうが破局率が高く、区間が零を外す場合。正本 `three_way.labels` の四つのうち
    この一つだけが合成データで一度も発火しておらず、経路の表は「零件」と印字していた
    （系統内の検分で捕まった）。"""
    m = base_main_spec()
    m[('S4', 'Osec-Ncold+v6b')] = {'cat': 90, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
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
         's4_floor': case_s4_floor, 's4_up': case_s4_up, 'dilution_causal': case_dilution_causal}


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
        json.dump({'kind': 'seal_B', 'signs': spec['seal'], 's4': 'どちらでもない', 'dry_run': True},
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
