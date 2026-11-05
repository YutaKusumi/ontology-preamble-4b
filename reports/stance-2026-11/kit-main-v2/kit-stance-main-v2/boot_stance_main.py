# -*- coding: utf-8 -*-
"""boot_stance_main_v1.py : 人の立場の三つの腕の検証の Colab の器（2026-11-05・南無弥勒如来・v1・未凍結）。
v1（2026-11-05 22:2x・系統外の検分 一巡目〔Gemini〕の採否 G2・G5）: v0 からの違いは本番の段の引数だけ。
  本番は「main <場面> <族の json の道>」（launch main も同じ）で、一度に一つの場面だけを走らせる。族のファイル（手元の stance_eval_v1.py family の出力）が、
  この kit の設定のもので、場面がその使える場面に入り、族の大きさが合うことを照らしてから走らせる。族のファイルは meta/family.json に写し、
  次の場面では同じバイトでなければ止まる。fetch main-<場面> の zip に族のファイルを入れる。ほかの段は v0 と同じ。

何をするか:
  論文の段階 D の送りの道具 `tools/run_preamble_api_d.py`（v2.9-d0w3・SHA-256 A04D40B9…・公開の置き場の写し）を書き換えずに子の process として呼び、
  Colab の中に立てた vLLM の OpenAI 互換の口（127.0.0.1 だけ）へ送る。呼び方は論文の走らせ直しの道具 `tools/rerun/op4b_rerun.py` の
  「自前の置き場」と同じ（経路の名は nscale・--base-url で口を差し替える・鍵の名には 'none' を置き、鍵のファイルは読ませない）。
  立場の 18 の文は、送りの道具の --custom-arms（置き場の中のファイル）で渡す。N は送りの道具の N（前置きなし）のまま。

段（一度の起動で一つ）:
  setup             kit の照らし・vLLM の版を入れる・機種の版を下ろす・版を記録する（前で待つ）
  serve             vLLM の口を切り離して立てる・立つまで待つ・chat template と送る文のトークンの数の照らし（前で待つ）
  rehearse          小さな予行（選んだものを見ない形・S1 と N1・各条件 4 試行）。速さと口の数え（トークンの和）と送る文の照らしだけを出す。
                    封の側は下ろさない（ランタイムを消すと消える）
  launch <段> [..]  calib か main を、切り離した process で起こす（すぐ戻る）
  calib             較正（場面ごとに N を 100 試行・立場の混ぜを 18 文 × 5 試行）
  main <場面> <族>  本番（一つの場面で 19 条件 × 200 試行・凍結した族のファイルを照らしてから）
  status            裏の段の進み（この器が書いた記録の末尾と心拍だけ）
  fetch <名>        段の出力を zip にまとめ、照らしの印を書いて下ろす（ノートの中で runpy で呼ぶ）。名は env・calib・main-<場面>
試し（手元・GPU なし）: STC_DRY=1 で送りの道具の --dry-run（偽の応答）を通す。STC_DRY_N で試行の数を小さくできる。STC_BASE で置き場を替える。
  試しのときだけ、STC_DRY_PROFILE で偽の応答の型（cycle は API の誤りを 17 試行に一つ起こす・hang:<秒> は試行 3 で待つ）、STC_HANG_S で止まりの線の秒を替えられる。
柵: 本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, time, shutil, hashlib, zipfile, datetime, subprocess, urllib.request, platform

os.environ.setdefault('HF_HUB_DISABLE_XET', '1')
os.environ.setdefault('HF_HUB_ENABLE_HF_TRANSFER', '0')
os.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')
os.environ.setdefault('TQDM_DISABLE', '1')
os.environ.setdefault('TRANSFORMERS_VERBOSITY', 'error')
try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

VERSION = 'boot_stance_main_v1'
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'run-config.json'), encoding='utf-8'))
DRY = os.environ.get('STC_DRY') == '1'
DRY_N = int(os.environ['STC_DRY_N']) if (DRY and os.environ.get('STC_DRY_N')) else None
BASE = os.environ.get('STC_BASE') or CFG['colab']['base']
MINI = os.path.join(HERE, 'op4b-mini')
RUNNER = os.path.join(MINI, *CFG['runner']['path'].split('/'))
SEALED = os.path.join(BASE, 'sealed')
LOGS = os.path.join(BASE, 'logs')
META = os.path.join(BASE, 'meta')
MODEL_DIR = os.path.join(BASE, 'model')
V, RN, M = CFG['vllm'], CFG['runner'], CFG['model']
URL_BASE = 'http://%s:%d' % (V['host'], V['port'])
SERVED = M['served_name']
NL = chr(10)
HANG_S = int(os.environ['STC_HANG_S']) if (DRY and os.environ.get('STC_HANG_S')) else CFG['colab']['hang_seconds']   # 試しのときだけ短くできる
DRY_PROFILE = (os.environ.get('STC_DRY_PROFILE') or CFG['colab']['dry_profile']) if DRY else None                  # 試しのときだけ偽の応答の型を替えられる
CLAUSE = '本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。'
ARM_IDS = [a['id'] for a in CFG['arms']['stance']]
CUSTOM = ','.join('%s=%s' % (a['id'], a['path']) for a in CFG['arms']['stance'])


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest().upper()


def sha256_lf(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()


def say(*a):
    print(*a, flush=True)


def stop(msg):
    say('STOP', msg)
    raise SystemExit(1)


def jload(p, default=None):
    if not os.path.isfile(p):
        return default
    return json.load(open(p, encoding='utf-8'))


def jdump(obj, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline=NL) as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def guard(p):
    if os.path.exists(p):
        stop('once-only guard: %s exists' % p)


def check_kit():
    man = {}
    for line in open(os.path.join(HERE, 'MANIFEST.sha256'), encoding='utf-8'):
        line = line.strip()
        if line:
            h, name = line.split('  ', 1)
            man[name] = h.upper()
    for name, h in man.items():
        got = sha256_file(os.path.join(HERE, *name.split('/')))
        if got != h:
            stop('kit mismatch %s %s != %s' % (name, got[:16], h[:16]))
    for rel, want in CFG['frozen'].items():           # 論文の凍結の素材と送りの道具（改行を LF にそろえた SHA-256）
        got = sha256_lf(os.path.join(MINI, *rel.split('/')))
        if got != want:
            stop('frozen mismatch %s %s != %s' % (rel, got[:16], want[:16]))
    for a in CFG['arms']['stance']:
        got = sha256_file(os.path.join(MINI, *a['path'].split('/')))
        if got != a['sha256']:
            stop('arm mismatch %s' % a['id'])
    return man


def child_env():
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    for k in ('OP4B_REFUSE_RULES', 'OP4B_LEXICON', 'PYTHONOPTIMIZE'):
        env.pop(k, None)
    env['OP4B_ENV_FILE'] = os.path.join(BASE, '_no_env_file_')     # 鍵のファイルを読ませない（在りもしない道）
    env[RN['key_env']] = 'none'                                    # 自前の口へは鍵を送らない（op4b_rerun の自前の置き場と同じ）
    env['MPLBACKEND'] = 'Agg'
    return env


def http_get(path, timeout=5):
    with urllib.request.urlopen(URL_BASE + path, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', 'replace')


def server_alive():
    if DRY:
        return True
    try:
        st, body = http_get('/v1/models')
        return st == 200 and SERVED in body
    except Exception:
        return False


def server_counters():
    """口の数え（prometheus の /metrics）から生成と入力のトークンの和を読む（封の記録は読まない）。"""
    if DRY:
        return None
    try:
        st, body = http_get('/metrics', timeout=10)
    except Exception:
        return None
    out = {}
    for line in body.split(NL):
        for key in ('vllm:generation_tokens_total', 'vllm:prompt_tokens_total'):
            if line.startswith(key) and not line.startswith('#'):
                try:
                    out[key] = out.get(key, 0.0) + float(line.rsplit(' ', 1)[1])
                except ValueError:
                    pass
    return out or None


# ---------------- 送りの道具を呼ぶ
def run_key(tag, s, seed):
    return '%s__%s__none__seed%d' % (tag, s, seed)


def out_dir(tag, s, seed):
    return os.path.join(MINI, 'results', '_dryrun' if DRY else tag, run_key(tag, s, seed))


def sealed_dir(tag, s, seed):
    return os.path.join(SEALED, '_dryrun' if DRY else tag, run_key(tag, s, seed))


def model_fn():
    return 'stub_dry-run' if DRY else SERVED.replace('/', '_')


def arms_of(kind):
    if kind == 'N':
        return ['N'], None
    if kind == 'stance':
        return list(ARM_IDS), CUSTOM
    if kind == 'all':
        return ['N'] + list(ARM_IDS), CUSTOM
    stop('unknown arms kind %s' % kind)


def runner_cmd(run, s):
    arms, custom = arms_of(run['arms'])
    n = min(run['n'], DRY_N) if DRY_N else run['n']
    c = [sys.executable, RUNNER, 'main', '--provider', RN['provider'], '--model', SERVED, '--base-url', URL_BASE + RN['chat_path'],
         '--scenario', s, '--system', 'none', '--arms', ','.join(arms), '--n-per-arm', str(n), '--seed', str(run['seeds'][s]), '--tag', run['tag'],
         '--max-tokens', str(RN['max_tokens']), '--workers', str(RN['workers']), '--retries', str(RN['retries']), '--retry-base', repr(float(RN['retry_base'])),
         '--sampling', RN['sampling'], '--forbid-env-override', '--blind', '--sealed-dir', SEALED, '--blind-stop-trunc', str(run['stop_trunc']),
         '--blind-stop-fmt', str(run['stop_fmt']), '--blind-stop-scope', run['scope'], '--price-in', '0.0', '--price-out', '0.0']
    if custom:
        c += ['--custom-arms', custom]
    if DRY:
        c += ['--dry-run', '--dry-profile', DRY_PROFILE]
    return c, arms, n


def read_hb(p):
    d = jload(p, None)
    return None if d is None else (d.get('done'), d.get('jobs'))


def check_summary(run, s, arms, n, rc):
    """送りの道具の公開の側のまとめ（選んだものを含まない）で、整合・送る文・トークンの数・機種名・API の誤りを照らす。"""
    od = out_dir(run['tag'], s, run['seeds'][s])
    summ = jload(os.path.join(od, 'blind-summary.json'), None)
    probs = []
    if rc != 0:
        probs.append('runner exit %s' % rc)
    if summ is None:
        probs.append('no blind-summary')
        return probs, None
    if not summ.get('integrity_ok'):
        probs.append('integrity NG')
    if summ.get('n') != n * len(arms):
        probs.append('n %s != %d' % (summ.get('n'), n * len(arms)))
    want_model = 'stub/dry-run' if DRY else SERVED
    if summ.get('api_models_seen') not in ([want_model], []):
        probs.append('api_models_seen %s' % summ.get('api_models_seen'))
    exp_sha = CFG['expected_prompt_sha16'][s]
    exp_tok = None if DRY else (jload(os.path.join(META, 'expected-prompt-tokens.json'), {}) or {}).get(s)
    for a in arms:
        pa = (summ.get('per_arm') or {}).get(a)
        if pa is None:
            probs.append('per_arm missing %s' % a)
            continue
        if pa.get('prompt_sha_seen') != [exp_sha[a]]:
            probs.append('prompt_sha %s %s' % (a, pa.get('prompt_sha_seen')))
        if exp_tok is not None and pa.get('ok') and pa.get('prompt_tokens_seen') != [exp_tok[a]]:
            probs.append('prompt_tokens %s %s != %s' % (a, pa.get('prompt_tokens_seen'), exp_tok[a]))
    live = summ['n'] - summ.get('skipped_stop', 0)
    if live and summ.get('api_error', 0) * 100 > CFG['colab']['api_error_stop_pct'] * live:
        probs.append('api_error %d of %d' % (summ.get('api_error', 0), live))
    return probs, summ


def run_one(stage, run, s, logname):
    cmd, arms, n = runner_cmd(run, s)
    od = out_dir(run['tag'], s, run['seeds'][s])
    if os.path.exists(od) or os.path.exists(sealed_dir(run['tag'], s, run['seeds'][s])):
        stop('output exists (once-only): %s' % run_key(run['tag'], s, run['seeds'][s]))
    os.makedirs(LOGS, exist_ok=True)
    log = os.path.join(LOGS, logname)
    c0 = server_counters()
    t0 = time.time()
    hung = False
    with open(log, 'w', encoding='utf-8') as fo:
        p = subprocess.Popen(cmd, stdout=fo, stderr=subprocess.STDOUT, env=child_env(), cwd=MINI)
        hb = os.path.join(od, 'heartbeat.json')
        last, t_last, t_say = None, time.time(), 0.0
        while p.poll() is None:
            time.sleep(2 if DRY else 15)
            cur = read_hb(hb)
            if cur != last:
                last, t_last = cur, time.time()
            elif time.time() - t_last > HANG_S:
                p.kill(); p.wait()
                hung = True
                break
            if time.time() - t_say > (5 if DRY else 300):
                t_say = time.time()
                say('  %s %s progress %s elapsed %ds' % (stage, run_key(run['tag'], s, run['seeds'][s]), cur, time.time() - t0))
    rc = p.returncode
    c1 = server_counters()
    if hung:
        probs, summ = ['hang %ds (heartbeat %s)' % (HANG_S, last)], None
    else:
        probs, summ = check_summary(run, s, arms, n, rc)
    gen = None
    if c0 and c1 and 'vllm:generation_tokens_total' in c0 and 'vllm:generation_tokens_total' in c1:
        gen = c1['vllm:generation_tokens_total'] - c0['vllm:generation_tokens_total']
    rec = {'run_key': run_key(run['tag'], s, run['seeds'][s]), 'part': run['part'], 'scene': s, 'n_per_arm': n, 'arms': len(arms), 'rc': rc,
           'elapsed_s': round(time.time() - t0, 1), 'server_gen_tokens': gen, 'problems': probs,
           'ok': (summ or {}).get('ok'), 'api_error': (summ or {}).get('api_error'), 'skipped_stop': (summ or {}).get('skipped_stop'),
           'truncated_final': (summ or {}).get('truncated_final'), 'format_fail_final': (summ or {}).get('format_fail_final'),
           'flag': (summ or {}).get('flag'), 'stopped_arms': (summ or {}).get('stopped_arms'), 'log': 'logs/' + logname}
    return rec


def halt(stage, reason, extra=None):
    jdump({'stage': stage, 'reason': reason, 'extra': extra, 'utc': now()}, os.path.join(BASE, 'HALT.json'))
    say('HALT', stage, reason)
    raise SystemExit(2)


def plan_scenes(stage, arg):
    allowed = CFG['stages'][stage]['scenes']
    if arg is None:
        return list(allowed)
    want = [x for x in arg.split(',') if x]
    bad = [x for x in want if x not in allowed]
    if bad or len(set(want)) != len(want) or not want:
        stop('scenes %s not allowed (allowed %s)' % (want, allowed))
    return [x for x in allowed if x in want]          # 場面の順は設定の順にそろえる


def check_main_args(rest):
    """v1・G2/G5: 本番は一度に一つの場面だけ。凍結した族のファイル（手元の stance_eval_v1.py family の出力・Colab に上げたもの）を必ず渡し、
    その族がこの kit の設定のもので、場面が族の使える場面に入っていることを照らす。"""
    if len(rest) != 2:
        stop('main は「main <場面> <族の json の道>」の形だけ（一度に一場面・族のファイルが要る）')
    s, famp = rest
    if s not in CFG['stages']['main']['scenes']:
        stop('scene %s not allowed' % s)
    if not os.path.isfile(famp):
        stop('族のファイルが無い: %s' % famp)
    fam_b = open(famp, 'rb').read()
    fam = json.loads(fam_b.decode('utf-8'))
    if fam.get('kit_run_config_sha256') != sha256_file(os.path.join(HERE, 'run-config.json')):
        stop('族のファイルは別の kit の設定のもの')
    usable = fam.get('usable') or []
    if s not in usable:
        stop('場面 %s は族の使える場面 %s に無い' % (s, usable))
    if fam.get('m') != 3 * len(CFG['words']) * len(usable) or len(fam.get('rows') or []) != fam.get('m'):
        stop('族の大きさが合わない')
    if bool(fam.get('dry')) != DRY:
        stop('族のファイルの試しの印が合わない')
    return s, famp, fam_b


def stage_runs(stage, scenes, tagdone, extra=None):
    check_kit()
    if os.path.exists(os.path.join(BASE, 'HALT.json')):
        stop('HALT.json exists (consult the registrant)')
    if not DRY and not server_alive():
        stop('server not alive')
    guard(os.path.join(META, tagdone))
    jdump(dict({'stage': stage, 'scenes': scenes, 'utc': now(), 'dry': DRY, 'dry_n': DRY_N}, **(extra or {})), os.path.join(META, tagdone.replace('-done', '-started')))
    recs = []
    say('%s START scenes=%s utc=%s' % (stage, ','.join(scenes), now()))
    for s in scenes:
        for run in CFG['stages'][stage]['runs']:
            rec = run_one(stage, run, s, '%s.log' % run_key(run['tag'], s, run['seeds'][s]))
            recs.append(rec)
            say('  %s %s ok=%s api_error=%s skipped=%s trunc=%s fmt=%s flag=%s stopped=%s %ds gen=%s %s' % (
                stage, rec['run_key'], rec['ok'], rec['api_error'], rec['skipped_stop'], rec['truncated_final'], rec['format_fail_final'],
                rec['flag'], rec['stopped_arms'], rec['elapsed_s'], rec['server_gen_tokens'], 'OK' if not rec['problems'] else 'PROBLEMS %s' % rec['problems']))
            if rec['problems']:
                jdump({'stage': stage, 'runs': recs, 'utc': now()}, os.path.join(META, tagdone.replace('-done', '-partial')))
                halt(stage, 'problems in %s' % rec['run_key'], rec['problems'])
    jdump(dict({'stage': stage, 'scenes': scenes, 'runs': recs, 'utc': now(), 'dry': DRY, 'dry_n': DRY_N, 'version': VERSION}, **(extra or {})), os.path.join(META, tagdone))
    say('%s DONE utc=%s' % (stage, now()))
    return recs


# ---------------- 段
def stage_setup():
    t0 = time.time()
    man = check_kit()
    say('KIT OK', len(man), 'files')
    guard(os.path.join(META, 'env.json'))
    os.makedirs(LOGS, exist_ok=True)
    env = {'version': VERSION, 'started_utc': now(), 'python': sys.version, 'platform': platform.platform(), 'dry': DRY, 'kit_manifest': man}
    if not DRY:
        with open(os.path.join(LOGS, 'pip.log'), 'w', encoding='utf-8') as fo:
            rc = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', V['pip']], stdout=fo, stderr=subprocess.STDOUT).returncode
        if rc:
            stop('pip install failed rc=%s (logs/pip.log)' % rc)
        q = ('import json,vllm,torch,transformers,huggingface_hub;print(json.dumps({"vllm":vllm.__version__,"torch":torch.__version__,'
             '"cuda":torch.version.cuda,"transformers":transformers.__version__,"huggingface_hub":huggingface_hub.__version__,'
             '"gpu":torch.cuda.get_device_name(0),"gpu_mem_gb":round(torch.cuda.get_device_properties(0).total_memory/2**30,1)}))')
        r = subprocess.run([sys.executable, '-c', q], capture_output=True, text=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        if r.returncode:
            stop('version probe failed: %s' % r.stderr[-300:])
        env['versions'] = json.loads(r.stdout.strip().split(NL)[-1])
        if env['versions']['vllm'] != V['version']:
            stop('vllm version %s != %s' % (env['versions']['vllm'], V['version']))
        if not any(g in env['versions']['gpu'] for g in CFG['colab']['gpu_names']):
            stop('gpu %s not in %s' % (env['versions']['gpu'], CFG['colab']['gpu_names']))
        dl = ('import sys;from huggingface_hub import snapshot_download;'
              'p=snapshot_download(sys.argv[1],revision=sys.argv[2],local_dir=sys.argv[3]);print(p)')
        r = subprocess.run([sys.executable, '-c', dl, M['repo'], M['revision'], MODEL_DIR], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        if r.returncode:
            stop('snapshot_download failed: %s' % r.stderr[-300:])
        env['model_dir'] = MODEL_DIR
        env['model_revision_requested'] = M['revision']
        env['model_files'] = sorted(f for f in os.listdir(MODEL_DIR) if not f.startswith('.'))
        gc = jload(os.path.join(MODEL_DIR, 'generation_config.json'), None)
        env['model_generation_config'] = gc
        for f in ('config.json', 'tokenizer_config.json', 'generation_config.json'):
            env.setdefault('model_file_sha256', {})[f] = sha256_file(os.path.join(MODEL_DIR, f))
    env['elapsed_s'] = round(time.time() - t0, 1)
    jdump(env, os.path.join(META, 'env.json'))
    say('SETUP OK', json.dumps(env.get('versions'), ensure_ascii=False), 'rev', M['revision'][:12], 'elapsed', env['elapsed_s'])


def build_messages():
    """送りの道具の user_message と同じ組み方（腕の文 + 空行 + 場面の文 + 書式の指示・N は場面の文 + 書式の指示）。"""
    d = json.load(open(os.path.join(MINI, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
    SC = {x['question_id']: x for x in d['scenarios']}
    texts = {'N': None}
    for a in CFG['arms']['stance']:
        texts[a['id']] = open(os.path.join(MINI, *a['path'].split('/')), encoding='utf-8').read().replace('\r\n', '\n').strip()
    out = {}
    for s in CFG['scenes']:
        sc = SC[s]
        body = sc['text'] + d['json_instruction'][sc['family']]
        out[s] = {arm: ((t + '\n\n' + body) if t else body) for arm, t in texts.items()}
    return out


def stage_serve():
    man = check_kit()
    env = jload(os.path.join(META, 'env.json'), None)
    if env is None:
        stop('run setup first')
    if DRY:
        say('SERVE skipped (dry)')
        return
    if server_alive():
        stop('server already running')
    exe = shutil.which('vllm')
    if not exe:
        stop('vllm CLI not found')
    cmd = [exe, 'serve', MODEL_DIR, '--served-model-name', SERVED, '--dtype', V['dtype'], '--max-model-len', str(V['max_model_len']),
           '--gpu-memory-utilization', repr(float(V['gpu_memory_utilization'])), '--seed', str(V['seed']), '--generation-config', V['generation_config'],
           '--host', V['host'], '--port', str(V['port'])]
    os.makedirs(LOGS, exist_ok=True)
    p = subprocess.Popen(cmd, stdout=open(os.path.join(LOGS, 'vllm.log'), 'w', encoding='utf-8'), stderr=subprocess.STDOUT, start_new_session=True,
                         env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    t0 = time.time()
    while time.time() - t0 < CFG['colab']['serve_wait_seconds']:
        if p.poll() is not None:
            tail = open(os.path.join(LOGS, 'vllm.log'), encoding='utf-8', errors='replace').read()[-600:]
            stop('vllm exited rc=%s tail=%s' % (p.returncode, tail))
        if server_alive():
            break
        time.sleep(5)
    else:
        stop('vllm not ready in %ds' % CFG['colab']['serve_wait_seconds'])
    ready_s = round(time.time() - t0, 1)
    # chat template と送る文のトークンの数（送る文の字そのものは kit の中にある・ここでは数と頭の形だけを見る）
    msgs = build_messages()
    jdump(msgs, os.path.join(META, 'messages.json'))
    q = ('import sys,json;from transformers import AutoTokenizer;t=AutoTokenizer.from_pretrained(sys.argv[1]);m=json.load(open(sys.argv[2],encoding="utf-8"));'
         'o={};h=None\n'
         'for s,d in m.items():\n'
         ' o[s]={}\n'
         ' for a,u in d.items():\n'
         '  r=t.apply_chat_template([{"role":"user","content":u}],tokenize=False,add_generation_prompt=True)\n'
         '  ids=t(r,add_special_tokens=False)["input_ids"]\n'
         '  o[s][a]=len(ids);h=h or r[:40]\n'
         '  assert r.startswith("<|im_start|>user\\n"),r[:60]\n'
         '  assert "<|im_start|>system" not in r\n'
         'json.dump({"tokens":o,"head":h},open(sys.argv[3],"w",encoding="utf-8"),ensure_ascii=False)\n')
    tokp = os.path.join(META, 'template-check.json')
    r = subprocess.run([sys.executable, '-c', q, MODEL_DIR, os.path.join(META, 'messages.json'), tokp], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    if r.returncode:
        stop('template check failed: %s' % r.stderr[-400:])
    tc = jload(tokp)
    jdump(tc['tokens'], os.path.join(META, 'expected-prompt-tokens.json'))
    allv = [v for d in tc['tokens'].values() for v in d.values()]
    env2 = {'serve_cmd': cmd, 'ready_s': ready_s, 'pid': p.pid, 'template_head': tc['head'], 'prompt_tokens_min': min(allv), 'prompt_tokens_max': max(allv), 'utc': now()}
    jdump(env2, os.path.join(META, 'serve.json'))
    say('SERVE OK ready %ss head %r tokens %d..%d prompts %d' % (ready_s, tc['head'], min(allv), max(allv), len(allv)))


def stage_rehearse():
    check_kit()
    if not DRY and not server_alive():
        stop('server not alive')
    guard(os.path.join(META, 'rehearse-summary.json'))
    st = CFG['stages']['rehearse']
    recs = []
    for s in st['scenes']:
        for run in st['runs']:
            rec = run_one('rehearse', run, s, '%s.log' % run_key(run['tag'], s, run['seeds'][s]))
            recs.append(rec)
            tps = (rec['server_gen_tokens'] / rec['elapsed_s']) if (rec['server_gen_tokens'] and rec['elapsed_s']) else None
            say('  rehearse %s ok=%s api_error=%s %ss gen_tokens=%s tok/s=%s %s' % (rec['run_key'], rec['ok'], rec['api_error'], rec['elapsed_s'],
                rec['server_gen_tokens'], ('%.0f' % tps) if tps else None, 'OK' if not rec['problems'] else 'PROBLEMS %s' % rec['problems']))
    tot_gen = sum(r['server_gen_tokens'] or 0 for r in recs)
    tot_s = sum(r['elapsed_s'] for r in recs)
    tot_trials = sum((r['ok'] or 0) + (r['api_error'] or 0) for r in recs)
    est = {}
    if tot_gen and tot_trials and tot_s:
        per_trial_s = tot_s / tot_trials
        for name, n_trials in CFG['estimate_trials'].items():
            est[name] = round(per_trial_s * n_trials / 60.0, 1)
    jdump({'runs': recs, 'total_gen_tokens': tot_gen, 'total_elapsed_s': round(tot_s, 1), 'total_trials': tot_trials,
           'estimate_minutes_at_this_rate': est, 'utc': now(), 'dry': DRY}, os.path.join(META, 'rehearse-summary.json'))
    say('REHEARSE %s trials=%d elapsed=%.0fs gen_tokens=%s estimate_min=%s' % ('OK' if all(not r['problems'] for r in recs) else 'PROBLEMS',
        tot_trials, tot_s, tot_gen, json.dumps(est, ensure_ascii=False)))


def stage_launch(args):
    if not args or args[0] not in ('calib', 'main'):
        stop('launch calib | launch main <場面> <族の json の道>')
    if args[0] == 'calib' and len(args) != 1:
        stop('launch calib は引数を取らない')
    os.makedirs(LOGS, exist_ok=True)
    name = args[0] if args[0] == 'calib' else 'main-' + check_main_args(args[1:])[0]     # v1・G2: 起こす前に場面と族を照らす
    log = os.path.join(LOGS, '%s-driver.log' % name)
    guard(log)
    p = subprocess.Popen([sys.executable, os.path.abspath(__file__)] + args, stdout=open(log, 'w', encoding='utf-8'), stderr=subprocess.STDOUT,
                         start_new_session=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    say('LAUNCHED', ' '.join(args), 'pid', p.pid, 'log', 'logs/%s-driver.log' % name)


def stage_status():
    out = []
    if os.path.isfile(os.path.join(BASE, 'HALT.json')):
        out.append('HALT ' + json.dumps(jload(os.path.join(BASE, 'HALT.json')), ensure_ascii=False))
    for f in sorted(os.listdir(LOGS)) if os.path.isdir(LOGS) else []:
        if f.endswith('-driver.log'):
            lines = [l for l in open(os.path.join(LOGS, f), encoding='utf-8', errors='replace').read().split(NL) if l.strip()]
            out.append('[%s] ' % f + ' | '.join(lines[-3:]))
    hbs = []
    for root, _, files in os.walk(os.path.join(MINI, 'results')):
        if 'heartbeat.json' in files:
            p = os.path.join(root, 'heartbeat.json')
            hbs.append((os.path.getmtime(p), os.path.basename(root), read_hb(p)))
    if hbs:
        t, k, d = max(hbs)
        out.append('heartbeat %s %s age %ds' % (k, d, time.time() - t))
    say((NL.join(out) or 'no logs')[-800:])


def fetch_members(name):
    mem = []

    def add_dir(root, arc):
        for r, _, files in os.walk(root):
            for f in sorted(files):
                p = os.path.join(r, f)
                mem.append((p, arc + '/' + os.path.relpath(p, root).replace(os.sep, '/')))
    for f in ('env.json', 'serve.json', 'expected-prompt-tokens.json', 'template-check.json', 'rehearse-summary.json', 'family.json'):
        if os.path.isfile(os.path.join(META, f)):
            mem.append((os.path.join(META, f), 'meta/' + f))
    mem.append((os.path.join(HERE, 'run-config.json'), 'meta/run-config.json'))
    mem.append((os.path.join(HERE, 'MANIFEST.sha256'), 'meta/kit-MANIFEST.sha256'))
    if os.path.isfile(os.path.join(BASE, 'HALT.json')):
        mem.append((os.path.join(BASE, 'HALT.json'), 'meta/HALT.json'))
    if name == 'env':
        for f in ('pip.log', 'vllm.log'):
            if os.path.isfile(os.path.join(LOGS, f)):
                mem.append((os.path.join(LOGS, f), 'logs/' + f))
        return mem
    if name == 'calib':
        stage, scenes, done = 'calib', CFG['stages']['calib']['scenes'], 'calib-done.json'
    elif name.startswith('main-') and name[5:] in CFG['stages']['main']['scenes']:
        stage, scenes, done = 'main', [name[5:]], None
    else:
        stop('fetch name %s' % name)
    marks = [f for f in os.listdir(META) if f.startswith(stage) and f.endswith(('-done.json', '-partial.json', '-started.json'))]
    for f in sorted(marks):
        mem.append((os.path.join(META, f), 'meta/' + f))
    if done and not os.path.isfile(os.path.join(META, done)) and not os.path.isfile(os.path.join(BASE, 'HALT.json')):
        stop('%s not finished' % stage)
    for s in scenes:
        for run in CFG['stages'][stage]['runs']:
            od, sd = out_dir(run['tag'], s, run['seeds'][s]), sealed_dir(run['tag'], s, run['seeds'][s])
            if stage == 'main' and not os.path.isfile(os.path.join(od, 'blind-summary.json')):
                stop('main %s not finished' % s)
            if os.path.isdir(od):
                add_dir(od, 'results/' + run_key(run['tag'], s, run['seeds'][s]))
            if os.path.isdir(sd):
                add_dir(sd, 'sealed/' + run_key(run['tag'], s, run['seeds'][s]))
            lg = os.path.join(LOGS, '%s.log' % run_key(run['tag'], s, run['seeds'][s]))
            if os.path.isfile(lg):
                mem.append((lg, 'logs/' + os.path.basename(lg)))
    for f in os.listdir(LOGS):
        if f.endswith('-driver.log') and f.startswith(stage):
            mem.append((os.path.join(LOGS, f), 'logs/' + f))
    return mem


def stage_fetch(args):
    if not args:
        stop('fetch <env|calib|main-<scene>>')
    name = args[0]
    tag = 'out-%s-%s' % (name, CFG['kit_version'])
    zp = os.path.join(BASE, tag + '.zip')
    if os.path.exists(zp):
        stop('zip exists (once-only): %s' % zp)
    mem = fetch_members(name)
    lines = ['%s  %s' % (sha256_file(p), arc) for p, arc in mem]
    man = NL.join(lines) + NL
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for p, arc in mem:
            z.write(p, arcname=tag + '/' + arc)
        z.writestr(tag + '/OUT-MANIFEST.sha256', man)
    say('FETCH %s members %d bytes %d' % (name, len(mem), os.path.getsize(zp)))
    say('OUT ZIP SHA256', sha256_file(zp))
    if not DRY:
        from google.colab import files
        files.download(zp)
    say('DONE')


def main(argv):
    if not argv:
        stop('stage?')
    st, rest = argv[0], argv[1:]
    if st == 'setup':
        stage_setup()
    elif st == 'serve':
        stage_serve()
    elif st == 'rehearse':
        stage_rehearse()
    elif st == 'launch':
        stage_launch(rest)
    elif st == 'calib':
        if rest:
            stop('calib は引数を取らない')
        stage_runs('calib', plan_scenes('calib', None), 'calib-done.json')
    elif st == 'main':
        s, famp, fam_b = check_main_args(rest)          # v1・G2/G5: 一度に一場面・凍結した族を照らす
        fam_sha = hashlib.sha256(fam_b).hexdigest().upper()
        kept = os.path.join(META, 'family.json')         # 本番に使う族は一つだけ（同じバイトでなければ止まる）
        if os.path.isfile(kept):
            if open(kept, 'rb').read() != fam_b:
                stop('前の場面と違う族のファイル（%s）' % fam_sha[:16])
        else:
            os.makedirs(META, exist_ok=True)
            with open(kept, 'xb') as f:
                f.write(fam_b)
        stage_runs('main', [s], 'main-%s-done.json' % s, extra={'family_path': famp, 'family_sha256': fam_sha})
    elif st == 'status':
        stage_status()
    elif st == 'fetch':
        stage_fetch(rest)
    else:
        stop('unknown stage %s' % st)


if __name__ == '__main__':
    main(sys.argv[1:])
