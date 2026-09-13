# -*- coding: utf-8 -*-
"""integrity_A.py v1 —— 段階 A の走行の整合検査（率盲検・許可表方式・正本 integrity_check・2026-09-13・登録者裁定 D9 の三つ目の手順）。
判定欄（catastrophe・choice・refuse_class・incentive 等）は読まない。trials から許可した欄（ALLOW）だけを取り出し、manifest と正本の登録（腕・n・seed・機種・走行器・要求の設定）と突合する。
相（tag から正本 tags で決める・--phase で上書き）ごとの期待:
  identity＝4B-2507 × N1 × arms.preamble × identity_n・seeds.identity／pilot＝全機種 × 全場面 × arms.preamble × pilot_n・seeds.pilot（再走は＋rerun_offset）／
  main＝全機種 × 全場面 × arms.preamble × n_per_arm・seeds.main／anchor_rerun＝sizes × 全場面 × anchor_band.arms × n_per_arm・seeds.anchor_rerun／
  bridge＝bridge.cells × N1 × bridge.arms × bridge.n・seeds.bridge／calibration＝4B-2507 × N1 × calibration.arm × calibration_n・seeds.calibration.rule／
  api_rerun＝api_rerun.models × N1 × arms.preamble × n_per_arm・seeds.api_rerun（provider は local 以外・要求の設定は突合しない）。
検査: 行数と目標・n_ok と api_error・format_fail の件数（書式外・破局率ではない）・trial_id の重複と trial_index の欠落・腕ごとの n の揃い・runner_sha が runner.sha16 と一致・
  arms_spec が登録の腕の並び・preamble_sha が arms.sha16 と一致・機種と seed が登録の表と一致・sampling が runner の登録と一致（extra_body は runner.extra_body_applies_to）・manifest の local_env の記帳。
出力: records/A/integrity-<tag>-<日付>.md と同 .json（既存は --force なしでは上書きしない）。不整合があれば非零で終わる。
用法: python tools/integrity_A.py --tag stageA [--phase main] [--root <results の代わり>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
ALLOW = ('status', 'trial_id', 'trial_index', 'arm', 'run_key', 'runner_sha', 'arms_spec', 'preamble_sha', 'format_fail', 'seed', 'model', 'sampling', 'tag', 'scenario', 'timestamp', 'timestamp_end')

ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--phase', default=None); ap.add_argument('--root', default=None); ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true')
a = ap.parse_args()
T = runs_A.load_T(a.contrasts); TAGS = T['tags']; PHASE = a.phase or next((k for k, v in TAGS.items() if v == a.tag), None)
if PHASE is None:
    sys.exit('tag %s の相が正本 tags に無い（--phase で指定）' % a.tag)
ANCHOR = next(m['key'] for m in T['models'] if m['anchor']); ARMS = T['arms']['preamble']; S = T['seeds']; RUN = T['runner']; MIDS = runs_A.model_ids(T)
INITIAL = [m['key'] for m in T['models'] if not m['anchor']]


def expected(mk, sc):
    """(腕の並び, n, 登録の seed の集合)。登録に無い組なら None。"""
    if PHASE == 'identity':
        return (ARMS, T['identity_n'], {S['identity']}) if (mk, sc) == (ANCHOR, T['identity_screen']['scenario']) else None
    if PHASE == 'pilot':
        s0 = S['pilot'].get(mk, {}).get(sc); return (ARMS, T['pilot_n'], {s0, s0 + S['rerun_offset']}) if s0 else None
    if PHASE == 'main':
        s0 = S['main'].get(mk, {}).get(sc); return (ARMS, T['n_per_arm'], {s0}) if s0 else None
    if PHASE == 'anchor_rerun':
        s0 = S['anchor_rerun'].get(mk, {}).get(sc); return (T['anchor_band']['arms'], T['n_per_arm'], {s0}) if s0 else None
    if PHASE == 'bridge':
        return (T['bridge']['arms'], T['bridge']['n'], set(S['bridge'][mk].values())) if (mk in T['bridge']['cells'] and sc == T['bridge']['scenario']) else None
    if PHASE == 'calibration':
        return ([T['calibration']['arm']], T['calibration']['n'], None) if (mk, sc) == (ANCHOR, T['calibration']['scenario']) else None
    if PHASE == 'api_rerun':
        s0 = S['api_rerun'].get(mk); return (ARMS, T['n_per_arm'], {s0}) if (s0 and sc == T['api_rerun']['scenario']) else None
    if PHASE == 'dryrun':
        return (ARMS, None, None)
    return None


def want_sampling(mk):
    return {'temperature': RUN['temperature'], 'top_p': RUN['top_p'], 'max_tokens': RUN['max_tokens'], 'extra_body': ({} if mk == ANCHOR else RUN['extra_body'])}


OUT = a.out or os.path.join(REPO, 'records', 'A', 'integrity-%s-%s' % (a.tag, datetime.date.today().isoformat()))
if (os.path.exists(OUT + '.md') or os.path.exists(OUT + '.json')) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUT)
rows = []; bad = 0
for recs in runs_A.index_runs(T, a.tag, a.root, allow_multi=True).values():
    for rec in recs:
        m = rec['manifest']; mk = rec['model']; sc = rec['scenario']; exp = expected(mk, sc); problems = []
        recs_t = list(runs_A.iter_jsonl(rec['trials_path'], ALLOW))
        if exp is None:
            problems.append('登録に無い機種 × 場面（相 %s）' % PHASE); arms, n, seeds = sorted({r['arm'] for r in recs_t}), None, None
        else:
            arms, n, seeds = exp
        if PHASE == 'calibration':
            try:
                owner, ph, num, sess = runs_A.decode_calibration_seed(T, rec['seed'])
            except RuntimeError as e:
                problems.append(str(e))
        elif seeds is not None and rec['seed'] not in seeds:
            problems.append('seed %d が登録と違う' % rec['seed'])
        ids = [r['trial_id'] for r in recs_t]; dup = len(ids) - len(set(ids)); idx = sorted({r['trial_index'] for r in recs_t})
        missing_idx = (idx[-1] - idx[0] + 1 - len(idx)) if idx else 0
        n_ok = sum(1 for r in recs_t if r['status'] == 'ok'); err = len(recs_t) - n_ok; ff = sum(1 for r in recs_t if r['status'] == 'ok' and r['format_fail'])
        per = collections.Counter(r['arm'] for r in recs_t); target = (len(arms) * n) if n else None
        even = (set(per) == set(arms)) and (n is None or all(v == n for v in per.values()))
        rs = {r['runner_sha'] for r in recs_t}; runner_ok = rs == {RUN['sha16']}
        aspec_ok = all(r['arms_spec'] == ','.join(arms) for r in recs_t) and m.get('arms') == list(arms)
        led = T['arms']['sha16']; ps = collections.defaultdict(set)
        for r in recs_t:
            ps[r['arm']].add(r['preamble_sha'])
        mism = ['%s %s≠%s' % (arm, sorted(map(str, v)), led.get(arm)) for arm, v in ps.items() if v != {led.get(arm)}]
        model_ok = m.get('model') == MIDS.get(mk) and all(r['model'] == m.get('model') for r in recs_t)
        samp = [r['sampling'] for r in recs_t[:1]] + [m.get('sampling')]
        samp_ok = True if PHASE == 'api_rerun' else all(x == want_sampling(mk) for x in samp)
        env = m.get('local_env') or {}; env_ok = True if PHASE == 'api_rerun' else bool(env.get('gpu') and env.get('versions'))
        checks = {'rows': target is None or len(recs_t) == target, 'api_error': err == 0, 'duplicates': dup == 0, 'missing_index': missing_idx == 0, 'per_arm_even': even, 'runner_sha': runner_ok,
                  'arms_spec': aspec_ok, 'preamble_sha': not mism, 'model': model_ok, 'sampling': samp_ok, 'local_env': env_ok}
        ok = all(checks.values()) and not problems
        bad += 0 if ok else 1
        rows.append({'run_key': rec['run_key'], 'model': mk, 'scenario': sc, 'seed': rec['seed'], 'rows': len(recs_t), 'target': target, 'n_ok': n_ok, 'api_error': err, 'format_fail': ff, 'duplicates': dup,
                     'missing_index': missing_idx, 'arms': len(per), 'runner_sha': sorted(map(str, rs)), 'preamble_mismatch': mism, 'checks': checks, 'problems': problems, 'ok': ok,
                     'local_env_gpu': env.get('gpu'), 'vllm': (env.get('versions') or {}).get('vllm')})
RES = {'kind': 'integrity_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'tag': a.tag, 'phase': PHASE, 'root': a.root, 'allow_fields': ALLOW,
       'runs': rows, 'bad_runs': bad, 'verdict': ('全走行 整合' if (bad == 0 and rows) else ('走行なし' if not rows else '不整合または未完 %d 走行' % bad)),
       'note': '判定欄（catastrophe・choice・refuse_class 等）を読まない。format_fail は書式外の件数（破局率ではない）。',
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(RES, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# 整合検査 %s（率盲検・許可表方式・相 %s・`tools/integrity_A.py` %s・%s UTC）' % (a.tag, PHASE, VERSION, RES['generated_utc']), '',
     '| run_key | 機種 | 場面 | seed | 行数 | 目標 | n_ok | api_error | format_fail | 重複 | 欠落 | 腕数 | 腕ごと n | runner_sha | arms_spec | 盤 SHA | 機種 | 要求の設定 | local_env | 問題 |',
     '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
ox = lambda b: '○' if b else '×'
for r in rows:
    c = r['checks']
    M.append('| %s | %s | %s | %d | %d | %s | %d | %d | %d | %d | %d | %d | %s | %s | %s | %s | %s | %s | %s | %s |' % (r['run_key'], r['model'], r['scenario'], r['seed'], r['rows'], r['target'], r['n_ok'], r['api_error'], r['format_fail'], r['duplicates'], r['missing_index'], r['arms'],
             ox(c['per_arm_even']), ox(c['runner_sha']), ox(c['arms_spec']), ox(c['preamble_sha']), ox(c['model']), ox(c['sampling']), ox(c['local_env']), '・'.join(r['problems'] + r['preamble_mismatch'][:3]) or '—'))
M += ['', '判定: %s' % RES['verdict'], '', RES['note'], '', RES['clause']]
open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[integrity_A] %s（%d 走行）written %s.{md,json}' % (RES['verdict'], len(rows), OUT))
sys.exit(0 if (bad == 0 and rows) else 1)
