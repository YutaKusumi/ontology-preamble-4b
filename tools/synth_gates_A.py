# -*- coding: utf-8 -*-
"""synth_gates_A.py v1 —— 段階 A の門と校正の器（identity_screen_A・gate_A・calib_band_A・control_chart_A・integrity_A）を合成データで発火させる検査（synth_A.py の門の部・2026-09-13・登録者裁定 D9 の三つ目の手順）。
二つの場合:
 合格の場合（門0.5 合格）: 門0.5＝API 既測に比例した件数／パイロット＝門2 は縮小なし・撤退条件は帯の内／校正腕＝帯の内・帯を超えてやり直しも超える（器の異常）・帯を超えてやり直し待ち・
   帯を超えたのに機種の走行が記帳（逸脱）とやり直しの合格・橋の帯の内／管理図は既存の表に追記（二度走らせて二重に記帳しない）／整合検査は門0.5・パイロット・校正腕で整合、要求の設定を違えた走行で不整合。
 不合格の場合（門0.5 不合格）: 門0.5＝N の破局を上にずらす／パイロット＝四場面で族の腕が床（門2 の縮小）・撤退条件は門0.5 の手元に対し帯を超え再走も超える（器の異常）／
   校正腕＝初点・帯の内・帯を超えてやり直しの合格／管理図は手元系列を新設。
各器の出力の判定欄を期待と突合し、すべて一致で PASS。合成の件数は検査のための人工値であり、いかなる読みにも用いない。
出力: records/A/synth-gates-A-<日付>.md と同 .json（--record で変更可）。
用法: python tools/synth_gates_A.py --root <一時置き場> [--B <門0.5 の補助の MC の B・既定 200>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, subprocess, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
ap = argparse.ArgumentParser(); ap.add_argument('--root', required=True); ap.add_argument('--B', type=int, default=200); ap.add_argument('--record', default=None); ap.add_argument('--keep', action='store_true')
a = ap.parse_args()
ROOT = os.path.abspath(a.root)
assert ROOT != os.path.abspath(os.path.join(REPO, 'results')), '合成データを results に置かない'
T = runs_A.load_T(); ARMS = T['arms']['preamble']; SC = T['scenarios']; SIZES = T['sizes']; MID = runs_A.model_ids(T); ANCHOR = next(m['key'] for m in T['models'] if m['anchor'])
SHA = T['arms']['sha16']; RUN = T['runner']; S = T['seeds']; CAL = T['calibration']; BASE = T['bases_4B2507_api']; TAGS = T['tags']
samp = lambda mk: {'temperature': RUN['temperature'], 'top_p': RUN['top_p'], 'max_tokens': RUN['max_tokens'], 'extra_body': ({} if mk == ANCHOR else RUN['extra_body'])}
PY = [sys.executable]; ENV = dict(os.environ, PYTHONIOENCODING='utf-8')


def write_run(root, tag, mk, sc, seed, arms, cells, created, n, sampling=None):
    """cells: {腕: (書式外, refuse, 破局, その他)}。走行器と同じ欄名で trials と manifest を書く（整合検査の欄を含む）。"""
    rk = '%s__%s__none__seed%d' % (tag, sc, seed); d = os.path.join(root, tag, rk); os.makedirs(d, exist_ok=True); mid = MID[mk]; mfn = mid.replace('/', '_'); sp = sampling or samp(mk)
    json.dump({'tag': tag, 'scenario': sc, 'model': mid, 'seed': seed, 'arms': arms, 'n_per_arm': n, 'arm_sha': {x: SHA.get(x) for x in arms}, 'arm_src': {}, 'sampling': sp, 'runner_sha': RUN['sha16'],
               'created': created, 'local_env': {'gpu': 'synthetic', 'versions': {'vllm': 'synthetic'}}, 'synthetic': True}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    open(os.path.join(d, 'raw-%s.jsonl' % mfn), 'w').close()
    ti = 0
    with open(os.path.join(d, 'trials-%s.jsonl' % mfn), 'w', encoding='utf-8', newline='\n') as f:
        for j in range(n):
            for arm in arms:
                F, Rf, Ca, O = cells[arm]; assert F + Rf + Ca + O == n, (arm, cells[arm], n)
                if j < F:
                    cat, ch, ff = None, None, True
                elif j < F + Rf:
                    cat, ch, ff = False, 'refuse', False
                elif j < F + Rf + Ca:
                    cat, ch, ff = True, 'a', False
                else:
                    cat, ch, ff = False, 'b', False
                f.write(json.dumps({'trial_id': '%s-%05d-%s' % (rk, ti, arm), 'trial_index': ti, 'arm': arm, 'run_key': rk, 'status': 'ok', 'catastrophe': cat, 'choice': ch, 'format_fail': ff,
                                    'loop_flag': False, 'truncated': False, 'runner_sha': RUN['sha16'], 'arms_spec': ','.join(arms), 'preamble_sha': SHA.get(arm), 'seed': seed, 'model': mid,
                                    'sampling': sp, 'tag': tag, 'scenario': sc, 'timestamp': created}, ensure_ascii=False) + '\n'); ti += 1
    return rk


def tool(args):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=ENV)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def mid_cells(n, cat):
    return (0, 0, cat, n - cat)


CHECKS = []


def check(name, cond, detail=''):
    CHECKS.append({'check': name, 'ok': bool(cond), 'detail': str(detail)[:300]}); print('[gates] %s %s %s' % ('○' if cond else '×', name, '' if cond else str(detail)[:300]), flush=True)


def case(name, fail):
    root = os.path.join(ROOT, name); shutil.rmtree(root, ignore_errors=True); rec = os.path.join(root, 'records'); os.makedirs(rec)
    # ---- 門0.5
    n = T['identity_n']; cells = {}
    for arm in ARMS:
        b = BASE['N1'].get(arm)
        if b:
            ff = round(n * b['format_fail'] / b['n']); rf = round(n * b['refuse'] / b['n']); ca = round(n * b['k'] / b['n'])
            if fail and arm == 'N':
                ca = min(n - ff - rf, ca + round(n * 0.20))
            cells[arm] = (ff, rf, ca, n - ff - rf - ca)
        else:
            cells[arm] = mid_cells(n, n // 2)
    write_run(root, TAGS['identity'], ANCHOR, 'N1', S['identity'], ARMS, cells, '2026-09-14T00:00:00', n)
    rc, out = tool(['tools/identity_screen_A.py', '--root', root, '--out', os.path.join(rec, 'identity'), '--B', str(a.B), '--force'])
    ID = runs_A.read_json(os.path.join(rec, 'identity.json')) if rc == 0 else {}
    check('%s: 門0.5 の判定' % name, rc == 0 and ID.get('verdict') == ('fail' if fail else 'pass'), out[-300:])
    # ---- パイロット（門2・撤退条件）
    pn = T['pilot_n']; k_wd = 30 if fail else 39
    for m in T['models']:
        for sc in SC:
            cells = {arm: mid_cells(pn, 0 if (fail and sc != 'N1' and m['key'] in SIZES) else pn // 2) for arm in ARMS}
            if m['key'] == ANCHOR and sc == CAL['scenario']:
                cells[CAL['arm']] = mid_cells(pn, k_wd)
            write_run(root, TAGS['pilot'], m['key'], sc, S['pilot'][m['key']][sc], ARMS, cells, '2026-09-14T01:00:00', pn)
    if fail:
        cells = {arm: mid_cells(pn, pn // 2) for arm in ARMS}; cells[CAL['arm']] = mid_cells(pn, k_wd)
        write_run(root, TAGS['pilot'], ANCHOR, CAL['scenario'], S['pilot'][ANCHOR][CAL['scenario']] + S['rerun_offset'], ARMS, cells, '2026-09-14T02:00:00', pn)
    rc, out = tool(['tools/gate_A.py', '--root', root, '--identity', os.path.join(rec, 'identity.json'), '--out', os.path.join(rec, 'gate'), '--force'])
    G = runs_A.read_json(os.path.join(rec, 'gate.json')) if rc == 0 else {}
    check('%s: 門2 の縮小' % name, rc == 0 and G.get('gate2', {}).get('shrink') == fail, out[-300:])
    check('%s: 撤退条件' % name, rc == 0 and G.get('withdrawal', {}).get('status') == ('anomaly' if fail else 'pass') and G['withdrawal']['anomaly'] == fail, json.dumps(G.get('withdrawal'), ensure_ascii=False))
    check('%s: 環境帯の引き直しの印字' % name, rc == 0 and G.get('env_band_recheck', {}).get('candidates'), '')
    # ---- 校正腕とセッション記録
    tag_c = TAGS['calibration']; cn = CAL['n']; sdir = os.path.join(root, 'sessions-A'); os.makedirs(sdir)
    mrk = lambda mk: '%s__N1__none__seed%d' % (TAGS['main'], S['main'][mk]['N1'])

    def calib(owner, phase, session, k, created, run_keys, env):
        seed = runs_A.calibration_seed(T, owner, phase, session)
        rk = write_run(root, tag_c, ANCHOR, CAL['scenario'], seed, [CAL['arm']], {CAL['arm']: mid_cells(cn, k)}, created, cn)
        stag = TAGS['bridge'] if phase == 'bridge' else TAGS['main']
        json.dump({'tag': stag, 'model': owner, 'session': session, 'env_value': env, 'run_keys': run_keys, 'calibration_run_key': rk, 'synthetic': True},
                  open(os.path.join(sdir, '%s__%s__s%d.json' % (stag, owner, session)), 'w', encoding='utf-8'), ensure_ascii=False)
        return rk
    if not fail:
        calib('0.6B', 'main', 1, 390, '2026-09-15T00:00:01', [mrk('0.6B')], 'L4')
        calib('32B', 'main', 1, 350, '2026-09-15T00:00:02', [], 'A100')
        calib('32B', 'main', 2, 350, '2026-09-15T00:00:03', [mrk('32B')], 'A100')
        calib('14B', 'main', 1, 350, '2026-09-15T00:00:04', [], 'A100')
        calib('8B', 'main', 1, 350, '2026-09-15T00:00:05', [mrk('8B')], 'A100')
        calib('8B', 'main', 2, 392, '2026-09-15T00:00:06', [mrk('8B')], 'A100')
        calib('4B', 'bridge', 1, 391, '2026-09-15T00:00:07', ['%s__N1__none__seed%d' % (TAGS['bridge'], S['bridge']['4B']['A100'])], 'A100')
    else:
        calib('0.6B', 'main', 1, 380, '2026-09-15T00:00:01', [mrk('0.6B')], 'L4')
        calib('1.7B', 'main', 1, 381, '2026-09-15T00:00:02', [mrk('1.7B')], 'L4')
        calib('4B', 'main', 1, 340, '2026-09-15T00:00:03', [], 'L4')
        calib('4B', 'main', 2, 378, '2026-09-15T00:00:04', [mrk('4B')], 'L4')
    rc, out = tool(['tools/calib_band_A.py', '--root', root, '--identity', os.path.join(rec, 'identity.json'), '--out', os.path.join(rec, 'calib'), '--force'])
    CB = runs_A.read_json(os.path.join(rec, 'calib.json')) if rc == 0 else {'sessions': []}
    v = {(x['phase'], x['owner'], x['session']): x.get('verdict') for x in CB['sessions']}
    if not fail:
        want = {('main', '0.6B', 1): 'pass', ('main', '32B', 1): 'fired', ('main', '32B', 2): 'anomaly', ('main', '14B', 1): 'fired', ('main', '8B', 1): 'fired', ('main', '8B', 2): 'retry_pass', ('bridge', '4B', 1): 'pass'}
        check('%s: 校正腕の判定' % name, rc == 0 and v == want, json.dumps({'%s|%s|%s' % k: x for k, x in v.items()}, ensure_ascii=False))
        check('%s: 器の異常の走行キー' % name, rc == 0 and CB.get('anomaly_run_keys') == [mrk('32B')], CB.get('anomaly_run_keys'))
        check('%s: やり直し待ち' % name, rc == 0 and [(x['owner'], x['session']) for x in CB.get('retry_waiting', [])] == [('14B', 1)], CB.get('retry_waiting'))
        check('%s: 手順の逸脱' % name, rc == 0 and [d['run_key'].split('seed')[-1] for d in CB.get('deviations', [])] == [str(runs_A.calibration_seed(T, '8B', 'main', 1))], CB.get('deviations'))
    else:
        want = {('main', '0.6B', 1): 'first_point', ('main', '1.7B', 1): 'pass', ('main', '4B', 1): 'fired', ('main', '4B', 2): 'retry_pass'}
        check('%s: 校正腕の判定（初点と両側）' % name, rc == 0 and v == want and CB.get('first_point', {}).get('run_key', '').endswith('seed%d' % runs_A.calibration_seed(T, '0.6B', 'main', 1)), json.dumps({'%s|%s|%s' % k: x for k, x in v.items()}, ensure_ascii=False))
        check('%s: 器の異常なし' % name, rc == 0 and CB.get('anomaly_run_keys') == [], CB.get('anomaly_run_keys'))
    # ---- 管理図（二度走らせて二重に記帳しない）
    chart = os.path.join(rec, 'control-chart.md')
    rc1, out1 = tool(['tools/control_chart_A.py', '--calib', os.path.join(rec, 'calib.json'), '--identity', os.path.join(rec, 'identity.json'), '--out', chart])
    rc2, out2 = tool(['tools/control_chart_A.py', '--calib', os.path.join(rec, 'calib.json'), '--identity', os.path.join(rec, 'identity.json'), '--out', chart])
    txt = open(chart, encoding='utf-8').read() if os.path.exists(chart) else ''
    n_rows = sum(1 for x in CB['sessions'] if x['n']) + 1
    check('%s: 管理図の記帳（%s）' % (name, '手元系列を新設' if fail else '既存の表に追記'), rc1 == 0 and rc2 == 0 and ('%d 行を記帳' % n_rows) in out1 and '0 行を記帳' in out2 and (('手元系列' in txt) == fail), out1[-200:] + out2[-200:])
    # ---- 整合検査
    for tg, ph in ((TAGS['identity'], 'identity'), (TAGS['pilot'], 'pilot'), (tag_c, 'calibration')):
        rc, out = tool(['tools/integrity_A.py', '--tag', tg, '--phase', ph, '--root', root, '--out', os.path.join(rec, 'integrity-' + ph), '--force'])
        check('%s: 整合検査（%s）' % (name, ph), rc == 0, out[-300:])
    if not fail:
        write_run(root, TAGS['main'], '0.6B', 'N1', S['main']['0.6B']['N1'], ARMS, {arm: mid_cells(T['n_per_arm'], 100) for arm in ARMS}, '2026-09-15T01:00:00', T['n_per_arm'],
                  sampling=dict(samp('0.6B'), extra_body={}))
        rc, out = tool(['tools/integrity_A.py', '--tag', TAGS['main'], '--phase', 'main', '--root', root, '--out', os.path.join(rec, 'integrity-main-bad'), '--force'])
        R_ = runs_A.read_json(os.path.join(rec, 'integrity-main-bad.json'))
        check('%s: 整合検査が要求の設定の違いを検出' % name, rc == 1 and R_['runs'][0]['checks']['sampling'] is False, out[-300:])
    if not a.keep:
        for sub in (TAGS['identity'], TAGS['pilot'], tag_c, TAGS['main'], 'sessions-A'):
            shutil.rmtree(os.path.join(root, sub), ignore_errors=True)


case('gates-pass', False)
case('gates-fail', True)
ok = all(c['ok'] for c in CHECKS)
SUM = {'kind': 'synth_gates_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'checks': CHECKS, 'pass': ok, 'B_identity_mc': a.B,
       'inputs': {nm: runs_A.sha16_file(os.path.join(REPO, 'tools', nm)) for nm in ('identity_screen_A.py', 'gate_A.py', 'calib_band_A.py', 'control_chart_A.py', 'integrity_A.py', 'runs_A.py', 'bands_A.py', 'synth_gates_A.py')},
       'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH),
       'clause': '合成の件数は検査のための人工値であり、いかなる読みにも用いない。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
recp = a.record or os.path.join(REPO, 'records', 'A', 'synth-gates-A-%s' % datetime.date.today().isoformat())
json.dump(SUM, open(recp + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# 段階 A 門と校正の器の合成検査（機械生成・`tools/synth_gates_A.py` %s・%s UTC）' % (VERSION, SUM['generated_utc']), '', '- 入力: %s・正本 SHA16 %s' % (json.dumps(SUM['inputs'], ensure_ascii=False), SUM['contrasts_sha16']),
     '- 判定: %s（%d 項目中 %d 一致）' % ('PASS' if ok else 'FAIL', len(CHECKS), sum(c['ok'] for c in CHECKS)), '', '| 項目 | 一致 | 詳細（不一致のとき） |', '|---|---|---|']
M += ['| %s | %s | %s |' % (c['check'], '○' if c['ok'] else '×', '' if c['ok'] else c['detail'].replace('|', '／')) for c in CHECKS] + ['', SUM['clause']]
open(recp + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('written', recp + '.{json,md}'); print('synth_gates_A.py %s %s' % (VERSION, 'PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
