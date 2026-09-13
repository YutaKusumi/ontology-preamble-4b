# -*- coding: utf-8 -*-
"""boot_stageA.py v1 —— 段階 A の Colab 起動スクリプト（2026-09-13 整備・boot_cost_pilot.py v2.2 の型・登録者裁定 D3・D9・D12・正本 sessions・calibration.timing）。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する。登録者の手に残すのは Drive 接続の OAuth 同意・ローカルへのダウンロード・プランと支払い・時間貸しの判断。
資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。セルに打つのは一行だけ（先頭の下線は type が先頭十数字を落とす事故の緩衝）:
    ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='main';os.environ['OP4B_MODEL']='32B';os.environ['OP4B_SESSION']='1';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_stageA.py').read().decode('utf-8'))
相（OP4B_PHASE）: identity（門0.5・4B-2507 × N1 × arms × identity_n）／pilot（OP4B_MODEL × 場面 × arms × pilot_n）／pilot_rerun（撤退条件の再走・4B-2507 × N1・seed＋rerun_offset）／
  main（校正腕 → OP4B_MODEL × 場面 × arms × n_per_arm → OP4B_ANCHOR=1 なら同じセッションで錨反復）／bridge（校正腕 → 橋の機種 × N1 × bridge.arms × bridge.n）。
セッション（正本 sessions・calibration.timing）: main と bridge は最初に校正腕（4B-2507 × Ncold × N1 × calibration_n・seed は seeds.calibration.rule）を走らせ、tools/bands_A.py で直ちに判定する
  （枝は records/A/identity-screen-A.json の判定。不合格枝の初点は本走行の最初のセッションの校正腕）。帯を超えたら機種の走行に進まずにセッション記録を書いて止まる（次のランタイムで OP4B_SESSION を一つ進める）。
  前のセッションの校正腕が帯を超えていた（やり直し）ときに再び超えたら、器の異常を記帳して機種の走行に進む。セッション記録は results/sessions-A/<tag>__<機種>__s<番号>.json（Drive 上）。
環境値: GPU の型とメモリで L4／A100 を決め、OP4B_ENV_VALUE=第三（時間貸し・登録者の指定）で上書き。登録の主環境と違えば止まる（橋は bridge_env）。同時要求数は正本 environments（A100 40GB の割当では if_40GB・32B は 80GB を待つ）。
要求の設定: 正本 runner（温度・top_p・max_tokens・max_model_len・gpu_memory_utilization）。非思考モードの指定は runner.extra_body_applies_to（4B-2507 には併合しない）。重みの版は records/A/hf-models-A.json の rev。
冪等: 走行器は既存行の trial_id で再開する。行数が目標に達した走行キーは飛ばす。出力は Drive のマウント下（/content/drive/MyDrive/op4b-stageA/）。
環境変数: OP4B_COMMIT・OP4B_PHASE・OP4B_MODEL（機種 key）・OP4B_SESSION（一始まり）・OP4B_SCENARIOS（既定は全場面）・OP4B_ANCHOR・OP4B_ENV_VALUE・OP4B_VLLM（版・既定は門0 と同じ）・
  OP4B_DRY=1（器材検査: 導入・取得・サーバを飛ばし走行器の dry-run・OP4B_REPO_DIR に手元の複製・OP4B_PERSIST に永続先・OP4B_DRY_N で n を小さく・OP4B_DRY_BRANCH で門0.5 の枝を与える・
  dry-run の出力は results/<tag>/ に移し manifest の機種を登録の機種に書き換える〔検査用の印つき〕）。
柵: 本走行の率は凍結の後にだけ意味を持つ。出力は器物の出力であり AI の自己報告ではない。
"""
import os, sys, json, time, subprocess, datetime, hashlib, shutil, urllib.request, glob, signal

T0 = time.time(); DRY = os.environ.get('OP4B_DRY') == '1'; LOG = []
PHASE = os.environ.get('OP4B_PHASE', 'identity'); assert PHASE in ('identity', 'pilot', 'pilot_rerun', 'main', 'bridge'), PHASE
SESSION = int(os.environ.get('OP4B_SESSION', '1')); WITH_ANCHOR = os.environ.get('OP4B_ANCHOR') == '1'; COMMIT = os.environ.get('OP4B_COMMIT', 'main')
VLLM = os.environ.get('OP4B_VLLM', '0.29.0'); ENV_OVERRIDE = os.environ.get('OP4B_ENV_VALUE'); DRY_N = int(os.environ.get('OP4B_DRY_N', '0') or 0)
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
CLAUSE = '本レコードの応答本文は器物の出力であり、AIによる自己報告ではありません。AIの意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw)); print('[boot] %-16s %7.0fs %s' % (step, time.time() - T0, kw or ''), flush=True)


def sh(cmd, check=True, **kw):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-4000:]); raise RuntimeError('失敗: %s' % (cmd if isinstance(cmd, str) else ' '.join(cmd)))
    return r


print('[boot] 段階 A boot v1 開始 phase=%s session=%d %s' % (PHASE, SESSION, 'DRY' if DRY else ''), flush=True)
# ---- 0. 永続先（Drive の同意は登録者が押す）
if DRY:
    PERSIST = os.environ.get('OP4B_PERSIST') or os.path.join(os.getcwd(), '_stageA_dry_persist')
else:
    if not os.path.isdir('/content/drive/MyDrive'):
        print('[boot] Drive の接続を求めます——「Google ドライブに接続」の許可は登録者が押してください', flush=True)
        from google.colab import drive
        drive.mount('/content/drive')
    PERSIST = '/content/drive/MyDrive/op4b-stageA'
os.makedirs(PERSIST, exist_ok=True)

# ---- 1. リポジトリ（コミット固定・tools・arms・design・records/A の sparse checkout）と正本
REPO = os.environ.get('OP4B_REPO_DIR') if DRY and os.environ.get('OP4B_REPO_DIR') else '/content/ontology-preamble-4b'
if not (DRY and os.environ.get('OP4B_REPO_DIR')):
    head_ok = False
    if os.path.isdir(os.path.join(REPO, '.git')):
        h = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip(); head_ok = bool(h) and (COMMIT == 'main' or h.startswith(COMMIT))
    if not head_ok:
        shutil.rmtree(REPO, ignore_errors=True)
        sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO]); sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone', 'tools', 'arms', 'design', 'records/A'])
        sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
HEAD = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() if os.path.isdir(os.path.join(REPO, '.git')) else 'no-git'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, bands_A
from fractions import Fraction
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-A.json'), encoding='utf-8')); HF = json.load(open(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), encoding='utf-8'))
TAGS = T['tags']; S = T['seeds']; RUN = T['runner']; ENVS = T['environments']; CAL = T['calibration']; ARMS = T['arms']['preamble']; SC = T['scenarios']; IDS = runs_A.model_ids(T)
ANCHOR = next(m['key'] for m in T['models'] if m['anchor'])
MODEL = ANCHOR if PHASE in ('identity', 'pilot_rerun') else os.environ.get('OP4B_MODEL', '')
assert MODEL in IDS, '機種 key が正本に無い: %r' % MODEL
SCEN = [x for x in (os.environ.get('OP4B_SCENARIOS') or ','.join(SC)).split(',') if x]
RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py'); RUNNER_SHA = runs_A.sha16_file(RUNNER)
assert RUNNER_SHA == RUN['sha16'], ('走行器の SHA16 が正本 runner.sha16 と違う', RUNNER_SHA, RUN['sha16'])
RES = os.path.join(REPO, 'results'); RES_P = os.path.join(PERSIST, 'results'); os.makedirs(RES_P, exist_ok=True)
if not DRY:
    if os.path.isdir(RES) and not os.path.islink(RES):
        shutil.rmtree(RES)
    if not os.path.islink(RES):
        os.symlink(RES_P, RES)
else:
    RES = os.path.join(REPO, 'results')
mark('repo', head=HEAD[:12], runner_sha16=RUNNER_SHA, persist=PERSIST)

# ---- 2. GPU・環境値・同時要求数
gpu = 'dry'; mem_gib = 0.0; GK = 'dry'
if not DRY:
    q = sh('nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits', check=False).stdout.strip().split('\n')[0]; gpu = q
    name, mem = [x.strip() for x in q.split(',')]; mem_gib = float(mem) / 1024.0; GK = 'L4' if 'L4' in name else ('A100' if 'A100' in name else 'other')
MEM_CLASS = 80 if (GK == 'A100' and mem_gib > 60) else (40 if GK == 'A100' else 24)
ENV_VALUE = ENV_OVERRIDE or (GK if not DRY else (T['bridge']['cells'][MODEL]['bridge_env'] if PHASE == 'bridge' else ENVS[MODEL]['env']))
want_env = T['bridge']['cells'][MODEL]['bridge_env'] if PHASE == 'bridge' else ENVS[MODEL]['env']
if ENV_VALUE not in (want_env, '第三'):
    sys.exit('[boot] 環境値 %s が登録（%s）と違うので止まる（相 %s・機種 %s）' % (ENV_VALUE, want_env, PHASE, MODEL))


def concurrency(mk, bridge=False):
    if bridge:
        return T['bridge']['cells'][mk]['bridge_concurrency']
    e = ENVS[mk]
    if ENV_VALUE == '第三':
        return (e.get('if_not_80GB') or e)['concurrency']
    if GK == 'A100' and MEM_CLASS == 40:
        if not e.get('if_40GB'):
            sys.exit('[boot] %s は A100 40GB では走らせない（80GB の割当を待つ・environment_rule）' % mk)
        return e['if_40GB']['concurrency']
    return e['concurrency']


mark('gpu', gpu=gpu, env_value=ENV_VALUE, memory_class_gb=MEM_CLASS)

# ---- 3. vLLM の導入（版の固定）
VER = {}
if not DRY:
    os.environ['HF_HUB_DISABLE_XET'] = '1'
    import importlib.metadata as md
    _v = lambda k: (lambda: md.version(k))() if k else None

    def _ver(k):
        try:
            return md.version(k)
        except Exception:
            return None
    if _ver('vllm') != VLLM:
        sh([sys.executable, '-m', 'pip', 'install', '-q', 'hf_transfer', 'huggingface_hub'], check=False); sh([sys.executable, '-m', 'pip', 'install', '-q', 'vllm==' + VLLM])
    if _ver('torchaudio') is not None:
        sh([sys.executable, '-m', 'pip', 'uninstall', '-y', '-q', 'torchaudio'], check=False)
    for k in ('vllm', 'torch', 'transformers', 'tokenizers', 'huggingface_hub'):
        VER[k] = _ver(k)
    fr = sh([sys.executable, '-m', 'pip', 'freeze'], check=False).stdout; VER['pip_freeze_sha16'] = hashlib.sha256(fr.encode('utf-8')).hexdigest()[:16].upper()
mark('pip', versions=VER)

# ---- 4. 重みとサーバ
SERVER = {'proc': None, 'model': None}


def hf_rev(mk):
    for rec in (HF.get('models') if isinstance(HF.get('models'), list) else []):
        if rec.get('key') == mk or rec.get('id') == IDS[mk]:
            return rec.get('rev') or rec.get('sha')
    v = HF.get(IDS[mk]) or HF.get(mk) or {}
    return v.get('rev') or v.get('sha') if isinstance(v, dict) else None


def health():
    try:
        with urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def stop_server():
    p = SERVER['proc']
    if p is not None:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except Exception:
            p.terminate()
        for _ in range(120):
            if not health() and p.poll() is not None:
                break
            time.sleep(1)
    SERVER.update(proc=None, model=None)


def serve(mk):
    if DRY or SERVER['model'] == mk:
        SERVER['model'] = mk; return
    stop_server()
    from huggingface_hub import snapshot_download
    os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'; rev = hf_rev(mk)
    try:
        path = snapshot_download(IDS[mk], revision=rev)
    except Exception:
        os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'; path = snapshot_download(IDS[mk], revision=rev)
    log = os.path.join(PERSIST, 'logs', 'vllm-%s-%s-s%d.log' % (PHASE, mk, SESSION)); os.makedirs(os.path.dirname(log), exist_ok=True)
    cmd = [sys.executable, '-m', 'vllm.entrypoints.openai.api_server', '--model', path, '--served-model-name', IDS[mk], '--dtype', 'bfloat16', '--max-model-len', str(RUN['max_model_len']),
           '--gpu-memory-utilization', str(RUN['gpu_memory_utilization']), '--port', '8000', '--seed', '0']
    SERVER['proc'] = subprocess.Popen(cmd, stdout=open(log, 'w'), stderr=subprocess.STDOUT, start_new_session=True); t = time.time()
    while time.time() - t < 1800:
        if SERVER['proc'].poll() is not None:
            print(open(log, errors='replace').read()[-6000:]); raise RuntimeError('vLLM サーバが終了した')
        if health():
            break
        time.sleep(5)
    else:
        raise RuntimeError('vLLM サーバの起動待ちが上限を超えた')
    SERVER['model'] = mk; mark('server', model=mk, rev=(rev or '')[:12])


# ---- 5. 走行器
ENVX = dict(os.environ, OP4B_ENV_FILE='/nonexistent', PYTHONIOENCODING='utf-8')


def run(tag, mk, sc, seed, arms, n, workers):
    n = DRY_N or n; rk = '%s__%s__none__seed%d' % (tag, sc, seed); d = os.path.join(RES, tag, rk)
    tf = glob.glob(os.path.join(d, 'trials-*.jsonl'))
    if tf and sum(1 for _ in open(tf[0], encoding='utf-8')) >= len(arms) * n:
        mark('skip', run_key=rk); return rk
    argv = [sys.executable, RUNNER, 'main', '--provider', 'local', '--model', IDS[mk], '--scenario', sc, '--arms', ','.join(arms), '--n-per-arm', str(n), '--seed', str(seed), '--tag', tag,
            '--workers', str(workers), '--max-tokens', str(RUN['max_tokens'])] + (['--extra-body', json.dumps(RUN['extra_body'])] if mk != ANCHOR else []) + (['--dry-run'] if DRY else [])
    logp = os.path.join(PERSIST, 'logs', 'run-%s.log' % rk); os.makedirs(os.path.dirname(logp), exist_ok=True); t = time.time()
    with open(logp, 'a', encoding='utf-8') as lf:
        rc = subprocess.run(argv, cwd=REPO, env=ENVX, stdout=lf, stderr=subprocess.STDOUT).returncode
    if DRY:
        src = os.path.join(REPO, 'results', '_dryrun', rk)
        if os.path.isdir(src):
            os.makedirs(os.path.join(RES, tag), exist_ok=True); shutil.rmtree(d, ignore_errors=True); shutil.move(src, d)
            mp = os.path.join(d, 'manifest.json'); m = json.load(open(mp, encoding='utf-8')); m.update(model=IDS[mk], dry_model_rewritten=True); json.dump(m, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            cp = os.path.join(d, 'cells.json')
            if os.path.exists(cp):
                c = json.load(open(cp, encoding='utf-8')); c['manifest'] = m; json.dump(c, open(cp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    mark('run', run_key=rk, rc=rc, seconds=round(time.time() - t, 1))
    if rc != 0:
        print('[boot] 走行器の終了コード %d（%s）' % (rc, logp), flush=True)
    return rk


# ---- 6. セッション記録
SESS_TAG = {'identity': TAGS['identity'], 'pilot': TAGS['pilot'], 'pilot_rerun': TAGS['pilot'], 'main': TAGS['main'], 'bridge': TAGS['bridge']}[PHASE]
SDIR = os.path.join(RES, 'sessions-A'); os.makedirs(SDIR, exist_ok=True)
SPATH = os.path.join(SDIR, '%s__%s__s%d.json' % (SESS_TAG, MODEL, SESSION))
SREC = json.load(open(SPATH, encoding='utf-8')) if os.path.exists(SPATH) else {'tag': SESS_TAG, 'model': MODEL, 'session': SESSION, 'phase': PHASE, 'run_keys': [], 'started': now()}
SREC.update(env_value=ENV_VALUE, gpu=gpu, memory_class_gb=MEM_CLASS, concurrency=concurrency(MODEL, PHASE == 'bridge'), versions=VER, repo_head=HEAD, runner_sha16=RUNNER_SHA, model_rev=hf_rev(MODEL),
            dev_marks=(['dry'] + (['dry_n'] if DRY_N else [])) if DRY else [], boot='v1', clause=CLAUSE)


def save_session():
    SREC['updated'] = now(); SREC['log'] = LOG; json.dump(SREC, open(SPATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


save_session()

# ---- 7. 校正腕（main・bridge）と直ちの判定
if PHASE in ('main', 'bridge'):
    cphase = 'bridge' if PHASE == 'bridge' else 'main'; cseed = runs_A.calibration_seed(T, MODEL, cphase, SESSION); cn = CAL['n']
    serve(ANCHOR); crk = run(TAGS['calibration'], ANCHOR, CAL['scenario'], cseed, [CAL['arm']], cn, T['capacity_rule']['concurrency_cap'])
    cc = runs_A.cell_counts(runs_A.one_file(os.path.join(RES, TAGS['calibration'], crk), 'trials')).get(CAL['arm']) or {'cat': 0, 'n_ok': 0}
    idp = os.path.join(REPO, 'records', 'A', 'identity-screen-A.json')
    branch = os.environ.get('OP4B_DRY_BRANCH') if DRY else None
    if branch is None:
        if not os.path.exists(idp):
            sys.exit('[boot] 門0.5 の記録（records/A/identity-screen-A.json）がコミットに無いので校正帯の枝を決められない')
        branch = json.load(open(idp, encoding='utf-8'))['verdict']
    bb = T['bases_4B2507_api'][CAL['scenario']][CAL['arm']]; verdict = None
    if cc['n_ok'] == 0:
        verdict = 'no_data'
    elif branch == 'pass':
        fired = bands_A.below_base(cc['cat'], cc['n_ok'], Fraction(bb['k'], bb['n']), CAL['band_pass']['pt'])
    else:
        prior = [r for r in runs_A.calibration_runs(T, RES) if r['phase'] == 'main' and r['run_key'] != crk]
        prior = sorted(prior, key=lambda r: r['manifest'].get('created') or '')
        if not prior:
            verdict = 'first_point'
        else:
            f0 = runs_A.cell_counts(prior[0]['trials_path']).get(CAL['arm']); fired = bands_A.over_band(cc['cat'], cc['n_ok'], f0['cat'], f0['n_ok'], CAL['band_fail']['pt'])
    prev = os.path.join(SDIR, '%s__%s__s%d.json' % (SESS_TAG, MODEL, SESSION - 1)); retry = os.path.exists(prev) and json.load(open(prev, encoding='utf-8')).get('calibration_verdict') == 'fired'
    if verdict is None:
        verdict = ('anomaly' if retry else 'fired') if fired else ('retry_pass' if retry else 'pass')
    SREC.update(calibration_run_key=crk, calibration_verdict=verdict, calibration_counts=[cc['cat'], cc['n_ok']], calibration_branch=branch); save_session(); mark('calibration', verdict=verdict, k=cc['cat'], n=cc['n_ok'], branch=branch)
    if verdict == 'fired':
        stop_server(); save_session()
        print('[boot] 校正腕が帯を超えた（%s）。機種の走行に進まずに止まる。新しいランタイムで OP4B_SESSION=%d として同じ一行を走らせる（calibration.timing）。' % (crk, SESSION + 1), flush=True)
        sys.exit(0)
    if verdict == 'anomaly':
        print('[boot] やり直しの校正腕も帯を超えた。器の異常を記帳して機種の走行に進む（機種は降格しない）。', flush=True)

# ---- 8. 機種の走行
plan = []
if PHASE == 'identity':
    plan = [(TAGS['identity'], ANCHOR, T['identity_screen']['scenario'], S['identity'], ARMS, T['identity_n'], concurrency(ANCHOR))]
elif PHASE == 'pilot':
    plan = [(TAGS['pilot'], MODEL, sc, S['pilot'][MODEL][sc], ARMS, T['pilot_n'], concurrency(MODEL)) for sc in SCEN]
elif PHASE == 'pilot_rerun':
    plan = [(TAGS['pilot'], ANCHOR, CAL['scenario'], S['pilot'][ANCHOR][CAL['scenario']] + S['rerun_offset'], ARMS, T['pilot_n'], concurrency(ANCHOR))]
elif PHASE == 'main':
    plan = [(TAGS['main'], MODEL, sc, S['main'][MODEL][sc], ARMS, T['n_per_arm'], concurrency(MODEL)) for sc in SCEN]
    if WITH_ANCHOR and MODEL in T['anchor_band']['models']:
        plan += [(TAGS['anchor_rerun'], MODEL, sc, S['anchor_rerun'][MODEL][sc], T['anchor_band']['arms'], T['n_per_arm'], concurrency(MODEL)) for sc in SCEN]
elif PHASE == 'bridge':
    plan = [(TAGS['bridge'], MODEL, T['bridge']['scenario'], list(S['bridge'][MODEL].values())[0], T['bridge']['arms'], T['bridge']['n'], concurrency(MODEL, bridge=True))]
serve(plan[0][1])
for tag, mk, sc, seed, arms, n, w in plan:
    rk = run(tag, mk, sc, seed, arms, n, w)
    if rk not in SREC['run_keys']:
        SREC['run_keys'].append(rk)
    save_session()
stop_server()

# ---- 9. 終わり（ファイルの SHA・zip）
files = {}
for tag, mk, sc, seed, arms, n, w in plan:
    d = os.path.join(RES, tag, '%s__%s__none__seed%d' % (tag, sc, seed))
    for f in sorted(glob.glob(os.path.join(d, '*'))):
        files[os.path.relpath(f, RES).replace('\\', '/')] = runs_A.sha16_file(f)
SREC.update(ended=now(), files_sha16_lf=files, wall_s=round(time.time() - T0, 1)); save_session()
if not DRY:
    zp = shutil.make_archive(os.path.join(PERSIST, 'stageA-%s-%s-s%d-%s' % (PHASE, MODEL, SESSION, datetime.date.today().isoformat())), 'zip', RES_P)
    print('[boot] zip → %s。登録者が Drive の Web UI からダウンロードし、SHA はセッション記録の files_sha16_lf と突合する。' % zp, flush=True)
print('[boot] 完了 phase=%s model=%s session=%d 走行キー %d・壁時計 %.0f 秒。%s' % (PHASE, MODEL, SESSION, len(SREC['run_keys']), time.time() - T0, CLAUSE), flush=True)
