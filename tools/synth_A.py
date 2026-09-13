# -*- coding: utf-8 -*-
"""synth_A.py v1 —— 段階 A の集計器（tools/analyze_A.py）の全経路を合成データ（人工の件数・推論なし）で発火させる検査（2026-09-13・登録者裁定 D9 の三つ目の手順・採否表 P2）。
置き場: --root に results 相当の木を作る（リポジトリの results/ には置かない・既定で走ごとに消す）。
十三走: 走 k（k=1〜12）は refuse 門 × 様式門 × 環境保留の十二の組を全対比に一様に当てる（refuse は腕 X の refuse 率の推移・様式は腕 X の (b) 率・環境は橋の腕 X の率のずれ）。
  場面ごとに型を置く: N1＝解釈条項なし・p* 棄却（P_S）／N2＝解釈条項あり・p* 棄却（P_CS）／S1＝解釈条項なし・p* 非棄却（P_N・pt 差一定・n 大）／S4＝解釈条項あり・p* 非棄却（P_C・n 大）／
  SK＝非有意・判定不能（両腕の床で残存規模 0）・判定不能（非収束・合成検査の口）。走 13 は門2 の縮小（全対比が判定不能）。
  腕 X＝各対比にちょうど一本ずつ入る腕（N・Odose1・Odosehalf・Lneg・Onull-Ncold・Osec-Ncold）。基の腕＝Onull・O-Ncold。
各走で analyze_A を実行し、対比ごとの札の全組合せ表の行 id を期待と突合する。十三走の和で五十二行すべての発火を assert し、あわせて次の経路の発火を確かめる:
  測定不能の除外（走 1）・錨帯の除外単位（走 2・走 5 は全場面の 4B で測れなかった効果種も発火）・橋の環境保留（環境の組）・片側の規則（走 1）・様式の注と散文層の副次終点・感度閾値で札が変わる対比・測れた効果種（測れた／測れなかった）・
  門0.5 不合格の注（走 2）・API 再走行のスタック差（走 4）・器の異常の注（校正腕 走 3・撤退条件 走 1）・降格の三行・床持続の 0 と 1・臨界規模・環境の副次解析・対数オッズ尺度でのみの記述。
出力: records/A/synth-A-<日付>.md と同 .json（--record で変更可）。合成の件数は検査のための人工値であり、いかなる読みにも用いない。
用法: python tools/synth_A.py --root <一時置き場> [--runs 1,13] [--keep] [--facts <設計事実 JSON>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, subprocess, itertools, argparse, datetime, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import confirm_A
from zaxis_A import z_sizes
REPO = runs_A.REPO
VERSION = 'v1'
ap = argparse.ArgumentParser()
ap.add_argument('--root', required=True); ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); ap.add_argument('--B-measurable', type=int, default=4)
ap.add_argument('--runs', default='all'); ap.add_argument('--keep', action='store_true'); ap.add_argument('--record', default=None)
a = ap.parse_args()
ROOT = os.path.abspath(a.root)
assert os.path.abspath(ROOT) != os.path.abspath(os.path.join(REPO, 'results')), '合成データを results に置かない'
T = runs_A.load_T(); SIZES = T['sizes']; SC = T['scenarios']; ARMS = T['arms']['preamble']; MID = runs_A.model_ids(T)
ANCHOR = next(m['key'] for m in T['models'] if m['anchor']); FAM = T['families']['A_slope']; ALL_ROWS = [r['id'] for r in FAM['confirm_rule']['label_combo_table']]
BR = T['bridge']; EB = T['environment_band']
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
                                                           **{x: [0.17, 0.18, 0.25, 0.45, 0.65, 0.85] for x in X_ARMS})),
    'MIX': dict(n=200, rates={'Onull': const(0.5), 'Odose1': const(0.5), 'Odosehalf': const(0.5), 'Lneg': const(0.5), 'N': const(0.5), 'Onull-Ncold': const(0.5), 'O-Ncold': const(0.01), 'Osec-Ncold': const(0.01)})}
SC_TYPE = dict(zip(SC, ['P_S', 'P_CS', 'P_N', 'P_C', 'MIX']))
COMBOS = list(itertools.product((False, True), ('none', 'note', 'hold'), (False, True)))
NC_ID = 'SK:Lneg~Onull'; ONE_SIDE_ID = 'SK:Odosehalf~Onull'
RUNS = list(range(1, 14)) if a.runs == 'all' else [int(x) for x in a.runs.split(',')]


def combo(run):
    return COMBOS[run - 1] if run <= len(COMBOS) else COMBOS[0]


def expected_row(c, run):
    if run == 13:
        return 'U-gate2_shrink'
    t = SC_TYPE[c['scenario']]
    if t == 'MIX':
        return 'U-nonconverged' if c['id'] == NC_ID else ('U-residual' if c['B'] == 'Osec-Ncold' else 'NS')
    rf, st, env = combo(run); ty = TYPES[t]
    return confirm_A.row_id(2, clause=ty['clause'], star=ty['star'], refuse=rf, style=st, env=env)


def spec(run, model, sc, arm, phase='main'):
    """(n, 破局, refuse, 書式外) を返す（人工値）。"""
    s = '4B' if model == ANCHOR else model; i = SIZES.index(s); ty = TYPES[SC_TYPE[sc]]; rf, st, env = combo(run)
    if arm in ty['rates']:
        n, rate = ty['n'], ty['rates'][arm][i]
    elif arm in ('O', 'Nk', 'Osec'):
        n, rate = 200, 0.005
        if run == 1 and sc == 'SK' and arm == 'O' and s == '32B':
            rate = 0.10
    else:
        n, rate = 40, 0.5
    if phase == 'anchor' and ((run == 2 and sc == 'SK' and s == '1.7B' and arm == 'Onull') or (run == 5 and s == '4B' and arm == 'Onull')):
        rate = rate + 0.20 if rate < 0.5 else rate - 0.20
    if phase == 'bridge' and env and arm in X_ARMS:
        rate = rate + 0.20 if rate < 0.5 else rate - 0.20
    cat = int(round(n * rate)) + (2 if phase == 'api' else 0)
    ref = int(round(n * 0.20 * (1 - i / (len(SIZES) - 1)))) if (rf and arm in X_ARMS and phase in ('main', 'bridge', 'anchor')) else 0
    ff = int(round(n * 0.40)) if (phase == 'main' and run == 1 and sc == 'SK' and arm == 'Odosehalf' and s in ('8B', '14B', '32B')) else 0
    assert cat + ref + ff <= n, (run, model, sc, arm, cat, ref, ff)
    return n, cat, ref, ff


def write_run(tag, model, sc, seed, arms, fn_spec):
    rk = '%s__%s__none__seed%d' % (tag, sc, seed); d = os.path.join(ROOT, tag, rk); os.makedirs(d, exist_ok=True); mid = MID[model]; mfn = mid.replace('/', '_')
    json.dump({'tag': tag, 'scenario': sc, 'model': mid, 'seed': seed, 'arms': arms, 'arm_src': {}, 'synthetic': True}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    open(os.path.join(d, 'raw-%s.jsonl' % mfn), 'w').close()
    ti = 0
    with open(os.path.join(d, 'trials-%s.jsonl' % mfn), 'w', encoding='utf-8', newline='\n') as f:
        for arm in arms:
            n, cat, ref, ff = fn_spec(arm)
            for j in range(n):
                if j < cat:
                    v = ('true', '"a"', 'false')
                elif j < cat + ref:
                    v = ('false', '"refuse"', 'false')
                elif j < cat + ref + ff:
                    v = ('null', 'null', 'true')
                else:
                    v = ('false', '"b"', 'false')
                f.write('{"trial_id":"%s-%d","trial_index":%d,"arm":"%s","status":"ok","catastrophe":%s,"choice":%s,"format_fail":%s,"loop_flag":false,"truncated":false}\n' % (rk, ti, ti, arm, v[0], v[1], v[2])); ti += 1
    return rk


def build(run):
    tag = 'synthA%02d' % run; rf, st, env = combo(run); S = T['seeds']; sess = {}; style = {}
    for m in T['models']:
        mk = m['key']
        for sc in SC:
            rk = write_run(tag, mk, sc, S['main'][mk][sc], ARMS, lambda arm, mk=mk, sc=sc: spec(run, mk, sc, arm)); sess.setdefault((tag, mk), []).append(rk)
            cells = style.setdefault(mk, {}).setdefault(sc, {})
            for arm in ARMS:
                n, cat, ref, ff = spec(run, mk, sc, arm); br = {'none': 0.5, 'note': 0.70, 'hold': 0.90}[st] if arm in X_ARMS else 0.5; b = int(round(n * br)); pn = n - b
                cells[arm] = {'n_ok': n, 'a_final': 0, 'b_final': b, 'c1_final': 0, 'c2_final': 0, 'think_residue': 0,
                              'strata': {'json_direct': {'n': b, 'cat': cat - int(round(cat * pn / n))}, 'prose': {'n': pn, 'cat': int(round(cat * pn / n))}}}
            if mk in T['anchor_band']['models']:
                rk2 = write_run(tag + '-anchor2', mk, sc, S['anchor_rerun'][mk][sc], T['anchor_band']['arms'], lambda arm, mk=mk, sc=sc: spec(run, mk, sc, arm, 'anchor')); sess[(tag, mk)].append(rk2)
    for bm, cell in BR['cells'].items():
        seed = list(S['bridge'][bm].values())[0]
        rk = write_run(tag + '-bridge', bm, BR['scenario'], seed, BR['arms'], lambda arm, bm=bm: spec(run, bm, BR['scenario'], arm, 'bridge')); sess[(tag + '-bridge', bm)] = [rk]
    if run == 4:
        for mk, seed in S['api_rerun'].items():
            write_run(tag + '-api', mk, 'N1', seed, ARMS, lambda arm, mk=mk: spec(run, mk, 'N1', arm, 'api'))
    os.makedirs(os.path.join(ROOT, 'sessions-A'), exist_ok=True)
    for (tg, mk), rks in sess.items():
        envv = BR['cells'][mk]['bridge_env'] if tg.endswith('-bridge') else T['environments'][mk]['env']
        json.dump({'tag': tg, 'model': mk, 'session': 1, 'env_value': envv, 'run_keys': rks, 'synthetic': True}, open(os.path.join(ROOT, 'sessions-A', '%s__%s__s1.json' % (tg, mk)), 'w', encoding='utf-8'), ensure_ascii=False)
    rec = os.path.join(ROOT, 'records'); os.makedirs(rec, exist_ok=True)
    paths = {'style': os.path.join(rec, 'style-%s.json' % tag), 'gate': os.path.join(rec, 'gate-%s.json' % tag)}
    json.dump({'kind': 'response_mode_A', 'synthetic': True, 'cells': style}, open(paths['style'], 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({'kind': 'gate_A', 'synthetic': True, 'gate2': {'shrink': run == 13}, 'withdrawal': {'anomaly': run == 1}}, open(paths['gate'], 'w', encoding='utf-8'), ensure_ascii=False)
    if run in (2, 4):
        paths['identity'] = os.path.join(rec, 'identity-%s.json' % tag)
        json.dump({'kind': 'identity_screen_A', 'synthetic': True, 'verdict': 'fail' if run == 2 else 'pass'}, open(paths['identity'], 'w', encoding='utf-8'), ensure_ascii=False)
    if run == 3:
        paths['calib'] = os.path.join(rec, 'calib-%s.json' % tag)
        json.dump({'kind': 'calib_band_A', 'synthetic': True, 'anomaly_run_keys': ['%s__N1__none__seed%d' % (tag, S['main']['4B']['N1'])]}, open(paths['calib'], 'w', encoding='utf-8'), ensure_ascii=False)
    return tag, paths


def paths_fired(R):
    got = set(); C_ = R['contrasts']; L_ = T['families']['A_slope']['confirm_rule']['labels']
    if R['unmeasurable']:
        got.add('unmeasurable')
    if R['anchor_excluded_units']:
        got.add('anchor_exclusion')
    if any(e['rule'] == 'bridge' for x in C_ for e in x['env_reasons']):
        got.add('env_bridge')
    if any(e['rule'] == 'one_side' for x in C_ for e in x['env_reasons']):
        got.add('env_one_side')
    if any(x['strings'].get('style') for x in C_):
        got.add('style_cells')
    if any(s_.get('status') == 'ok' for s_ in R['stratified']):
        got.add('stratified_ok')
    if R['stratified']:
        got.add('stratified_any')
    if any(s_['changed'] for s_ in R['sensitivity']):
        got.add('sensitivity_changed')
    if any(v['measurable'] for v in R['measurable']['types'].values()):
        got.add('measurable_yes')
    if any(not v['measurable'] for v in R['measurable']['types'].values()):
        got.add('measurable_no')
    notes = [n for x in C_ for n in x['notes']]; PSx = T['print_strings']
    for key in ('identity_fail_note', 'calib_anomaly_note', 'withdrawal_anomaly_note'):
        if PSx[key] in notes:
            got.add(key)
    if R['descriptive']['A_desc_stack']['rows']:
        got.add('stack_rows')
    if R['demotions']:
        got.add('demotions')
    if any(f['flag'] == 1 for f in R['floor']):
        got.add('floor_1')
    if any(f['flag'] == 0 for f in R['floor']):
        got.add('floor_0')
    if any(x['size'] != 'なし' for x in R['descriptive']['A_desc_critical_size']):
        got.add('critical_size')
    if any(x.get('status') == '収束' for x in R['descriptive']['A_desc_env']['secondary']):
        got.add('env_secondary')
    if R['descriptive']['A_desc_scale_only']:
        got.add('scale_only_desc')
    if R.get('reach_note'):
        got.add('reach_note')
    if any(x['label'] == L_['confirmed'] for x in C_):
        got.add('confirmed_label_string')
    return got


PATHS_REQUIRED = ['unmeasurable', 'anchor_exclusion', 'env_bridge', 'env_one_side', 'style_cells', 'stratified_ok', 'stratified_any', 'sensitivity_changed', 'measurable_yes', 'measurable_no',
                  'identity_fail_note', 'calib_anomaly_note', 'withdrawal_anomaly_note', 'stack_rows', 'demotions', 'floor_1', 'floor_0', 'critical_size', 'env_secondary', 'scale_only_desc', 'reach_note', 'confirmed_label_string']
fired = {}; paths = set(); report = []; mismatches = []; t00 = time.time()
for run in RUNS:
    t0 = time.time(); tag, P = build(run); out = os.path.join(ROOT, 'out', 'analysis-%s' % tag)
    cmd = [sys.executable, os.path.join(REPO, 'tools', 'analyze_A.py'), '--tag', tag, '--root', ROOT, '--anchor-tag', tag + '-anchor2', '--bridge-tag', tag + '-bridge', '--api-tag', tag + '-api',
           '--style', P['style'], '--gate', P['gate'], '--out', out, '--force', '--B-measurable', str(a.B_measurable), '--synth-nonconverged', NC_ID]
    for k in ('identity', 'calib'):
        if k in P:
            cmd += ['--' + k, P[k]]
    if a.facts and os.path.exists(a.facts):
        cmd += ['--facts', a.facts]
    pr = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    if pr.returncode != 0:
        print(pr.stdout[-3000:]); print(pr.stderr[-6000:]); sys.exit('analyze_A が走 %d で失敗' % run)
    RJ = runs_A.read_json(out + '.json'); mm = []
    for x, c in zip(RJ['contrasts'], FAM['contrasts']):
        exp = expected_row(c, run); fired.setdefault(x['row'], []).append('%d:%s' % (run, x['id']))
        if x['row'] != exp:
            mm.append({'run': run, 'id': x['id'], 'expected': exp, 'got': x['row'], 'label': x['label']})
    got = paths_fired(RJ); paths |= got; mismatches += mm
    report.append({'run': run, 'tag': tag, 'combo': {'refuse_hold': combo(run)[0], 'style': combo(run)[1], 'env_hold': combo(run)[2]}, 'label_counts': RJ['label_counts'], 'mismatches': len(mm),
                   'rows': sorted({x['row'] for x in RJ['contrasts']}), 'paths': sorted(got), 'dev_marks': RJ['dev_marks'], 'seconds': round(time.time() - t0, 1)})
    print('[synth] 走 %2d %s 不一致 %d 行 %s 経路 %d（%.0fs）' % (run, tag, len(mm), len(report[-1]['rows']), len(got), time.time() - t0), flush=True)
    if not a.keep:
        for sub in (tag, tag + '-anchor2', tag + '-bridge', tag + '-api'):
            shutil.rmtree(os.path.join(ROOT, sub), ignore_errors=True)
        shutil.rmtree(os.path.join(ROOT, 'sessions-A'), ignore_errors=True)
not_fired = [r for r in ALL_ROWS if r not in fired]; paths_missing = [p for p in PATHS_REQUIRED if p not in paths]
full = (RUNS == list(range(1, 14)))
SUM = {'kind': 'synth_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'runs': RUNS, 'full': full,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'analyze_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'analyze_A.py')), 'confirm_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'confirm_A.py')),
                  'runs_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'runs_A.py')), 'synth_A': runs_A.sha16_file(os.path.abspath(__file__))},
       'rows_total': len(ALL_ROWS), 'rows_fired': len(ALL_ROWS) - len(not_fired), 'rows_not_fired': not_fired, 'mismatches': mismatches, 'paths_required': PATHS_REQUIRED, 'paths_missing': paths_missing,
       'fired_by_row': {k: v[:3] for k, v in sorted(fired.items())}, 'per_run': report, 'seconds': round(time.time() - t00, 1),
       'clause': '合成の件数は検査のための人工値であり、いかなる読みにも用いない。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
recp = a.record or os.path.join(REPO, 'records', 'A', 'synth-A-%s' % datetime.date.today().isoformat())
if full:
    json.dump(SUM, open(recp + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    Lm = ['# 段階 A 合成検査（機械生成・`tools/synth_A.py` %s・%s UTC）' % (VERSION, SUM['generated_utc']), '', '- 入力: %s' % json.dumps(SUM['inputs'], ensure_ascii=False),
          '- 札の全組合せ表: %d 行のうち発火 %d 行（未発火: %s）・期待との不一致 %d 件・経路の未発火: %s・所要 %.0f 秒' % (SUM['rows_total'], SUM['rows_fired'], '・'.join(not_fired) or 'なし', len(mismatches), '・'.join(paths_missing) or 'なし', SUM['seconds']), '',
          '| 走 | tag | refuse 門 | 様式門 | 環境保留 | 札の件数 | 不一致 | 発火した行 | 発火した経路 | 秒 |', '|---|---|---|---|---|---|---|---|---|---|']
    Lm += ['| %d | %s | %s | %s | %s | %s | %d | %s | %s | %s |' % (r['run'], r['tag'], '保留' if r['combo']['refuse_hold'] else '—', r['combo']['style'], '保留' if r['combo']['env_hold'] else '—',
                                                                   json.dumps(r['label_counts'], ensure_ascii=False), r['mismatches'], '・'.join(r['rows']), '・'.join(r['paths']), r['seconds']) for r in report]
    Lm += ['', SUM['clause']]
    open(recp + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(Lm) + '\n')
    print('written', recp + '.{json,md}')
print('[synth_A] 行 %d/%d 発火・不一致 %d・経路の未発火 %s' % (SUM['rows_fired'], SUM['rows_total'], len(mismatches), paths_missing))
if mismatches:
    print(json.dumps(mismatches[:20], ensure_ascii=False, indent=0))
if full:
    assert not not_fired and not mismatches and not paths_missing, (not_fired, len(mismatches), paths_missing)
    print('synth_A.py %s PASS' % VERSION)
