# -*- coding: utf-8 -*-
"""boot_stageA.py v2 —— 段階 A の Colab 起動スクリプト（2026-09-13 整備・boot_cost_pilot.py v2.2 の型・登録者裁定 D3・D9・D12・D23・D24・正本 sessions・calibration.timing）。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する。登録者の手に残すのは Drive 接続の OAuth 同意・ローカルへのダウンロード・プランと支払い・時間貸しの判断。
資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。セルに打つのは一行だけ（先頭の下線は type が先頭十数字を落とす事故の緩衝・<commit> は 40 桁）:
    ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='main';os.environ['OP4B_MODEL']='32B';os.environ['OP4B_SESSION']='1';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_stageA.py').read().decode('utf-8'))
v2（2026-09-14・実装検分の採否表 P75・P77〜P83・登録者裁定 D23・D24・正本 sessions.commit_rule）:
- 重みの版: records/A/hf-models-A.json の models[機種].rev（登録の接頭辞）を公開 API で完全な SHA に解き（tools/runs_A.py の resolve_rev）、その SHA で取得する。
  取得した snapshot の名が解いた SHA と同じかを確かめ、セッション記録の model_rev_full に書く。解けなければ止まる。
- 走行器: 終了コードが 0 でなければ止まる（DRY の未発火の 3 を除く）。行数が目標に達しても n_ok が足りなければ --redo-errors を最大 MAX_REDO 回かけ、なおそろわなければ止まる。
- 校正腕: 判定は tools/calib_band_A.py の関数（件数が calibration.n に満たなければ判定せずに止まる・初点は件数のそろった本走行の校正腕）。
  不合格枝では、初点が確立していなければ、初点を名乗った機種の本走行のセッションのほかは始めない（橋も始めない・登録者裁定 D24）。
- 環境値: 上書きは「第三」だけで、正本 environments で許した機種のパイロットと本走行に限り、検出したメモリが 80GB 級であることを確かめる。
  パイロット・撤退条件の再走・本走行・橋では OP4B_COMMIT に固定のコミット（40 桁）を必須にし、取り出した HEAD との一致を確かめる（門0.5 は main を許す）。
- 記帳（正本 environment_rule.record・sessions.fields）: pip freeze の SHA・同時要求数・サーバの引数・重みの完全な版・走行ごとの先取りの回数（vLLM の計測値 num_preemptions の
  走行の前後の差）・走行器の終了コードと件数・校正腕の件数と枝。走行キーは走らせる前に run_keys に書く（中断しても記帳が残る）。files_sha16_lf に校正腕の走行を含める。
- DRY の口（OP4B_DRY_N・OP4B_DRY_BRANCH・OP4B_DRY_ACCEPT_SHORT）は DRY のときだけ読み、DRY には OP4B_REPO_DIR と OP4B_PERSIST が要る（Drive の下と symlink の results は拒む）。
  DRY でないのに検査用の環境変数があれば止まる。dry-run の出力は results/<tag>/ に複写して manifest に dry_model_rewritten を付け、読み出しの器は拒む（tools/runs_A.py の dry_marks）。
相（OP4B_PHASE）: identity（門0.5・4B-2507 × N1 × arms × identity_n）／pilot（OP4B_MODEL × 場面 × arms × pilot_n）／pilot_rerun（撤退条件の再走・4B-2507 × N1・seed＋rerun_offset）／
  main（校正腕 → OP4B_MODEL × 場面 × arms × n_per_arm → OP4B_ANCHOR=1 なら同じセッションで錨反復）／bridge（校正腕 → 橋の機種 × N1 × bridge.arms × bridge.n）。
セッション（正本 sessions）: セッション番号はランタイムを新しく起動するたびに一つ進める（sessions.number_rule）。main と bridge は最初に校正腕（4B-2507 × Ncold × N1 × calibration_n・
  seed は seeds.calibration.rule）を走らせて直ちに判定する（枝は records/A/identity-screen-A.json の判定）。帯を超えたら機種の走行に進まずに止まる（次のセッション番号でやり直す）。
  やり直しの校正腕も帯を超えたら、器の異常を記帳して機種の走行に進む。セッション記録は results/sessions-A/<tag>__<機種>__s<番号>.json（Drive 上）。
環境値: GPU の型の名で L4／A100 を決め、メモリで 24／40／80GB 級を決める。登録の主環境と違えば止まる（橋は bridge_env）。同時要求数は正本 environments（A100 40GB では if_40GB）。
要求の設定: 正本 runner（温度・top_p・max_tokens・max_model_len・gpu_memory_utilization）。非思考モードの指定は runner.extra_body_applies_to（4B-2507 には併合しない）。
冪等: 走行器は既存行の trial_id で再開する。行数と n_ok が目標に達した走行キーは飛ばす。出力は Drive のマウント下（/content/drive/MyDrive/op4b-stageA/）。
柵: 本走行の率は凍結の後にだけ意味を持つ。出力は器物の出力であり AI の自己報告ではない。
"""
import os, sys, re, json, time, subprocess, datetime, hashlib, shutil, urllib.request, glob, signal

T0 = time.time(); DRY = os.environ.get('OP4B_DRY') == '1'; LOG = []
PHASE = os.environ.get('OP4B_PHASE', 'identity'); assert PHASE in ('identity', 'pilot', 'pilot_rerun', 'main', 'bridge'), PHASE
SESSION = int(os.environ.get('OP4B_SESSION', '1')); assert SESSION >= 1, SESSION
WITH_ANCHOR = os.environ.get('OP4B_ANCHOR') == '1'; COMMIT = os.environ.get('OP4B_COMMIT', 'main'); FIXED = bool(re.fullmatch(r'[0-9a-f]{40}', COMMIT))
VLLM = os.environ.get('OP4B_VLLM', '0.29.0'); ENV_OVERRIDE = os.environ.get('OP4B_ENV_VALUE') or None
DATA_PHASES = ('pilot', 'pilot_rerun', 'main', 'bridge'); MAX_REDO = 3
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
CLAUSE = '本レコードの応答本文は器物の出力であり、AIによる自己報告ではありません。AIの意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
DRY_N = 0; DRY_BRANCH = None; DRY_ACCEPT_SHORT = False; DEV = []
if DRY:
    _miss = [k for k in ('OP4B_REPO_DIR', 'OP4B_PERSIST') if not os.environ.get(k)]
    if _miss:
        sys.exit('[boot] DRY では %s を与える（検査用の置き場を明示する・採否表 P78）' % '・'.join(_miss))
    DRY_N = int(os.environ.get('OP4B_DRY_N', '0') or 0); DRY_BRANCH = os.environ.get('OP4B_DRY_BRANCH') or None; DRY_ACCEPT_SHORT = os.environ.get('OP4B_DRY_ACCEPT_SHORT') == '1'
    DEV = ['dry'] + [x for x, on in (('dry_n', DRY_N), ('dry_branch', DRY_BRANCH), ('dry_accept_short', DRY_ACCEPT_SHORT)) if on]
else:
    _stray = sorted(k for k in os.environ if k.startswith('OP4B_DRY_') or k in ('OP4B_REPO_DIR', 'OP4B_PERSIST'))
    if _stray:
        sys.exit('[boot] DRY でないのに検査用の環境変数がある: %s（外してから走らせる・採否表 P78）' % '・'.join(_stray))
    if PHASE in DATA_PHASES and not FIXED:
        sys.exit('[boot] 相 %s では OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える（既定の main は受けない・正本 sessions.commit_rule）' % PHASE)


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw)); print('[boot] %-16s %7.0fs %s' % (step, time.time() - T0, kw or ''), flush=True)


def sh(cmd, check=True, **kw):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-4000:]); raise RuntimeError('失敗: %s' % (cmd if isinstance(cmd, str) else ' '.join(cmd)))
    return r


print('[boot] 段階 A boot v2 開始 phase=%s session=%d %s' % (PHASE, SESSION, 'DRY' if DRY else ''), flush=True)
# ---- 0. 永続先（Drive の同意は登録者が押す）
if DRY:
    PERSIST = os.path.abspath(os.environ['OP4B_PERSIST'])
    if PERSIST.replace('\\', '/').startswith('/content/drive'):
        sys.exit('[boot] DRY の永続先を Drive の下に置かない（採否表 P78）')
else:
    if not os.path.isdir('/content/drive/MyDrive'):
        print('[boot] Drive の接続を求めます——「Google ドライブに接続」の許可は登録者が押してください', flush=True)
        from google.colab import drive
        drive.mount('/content/drive')
    PERSIST = '/content/drive/MyDrive/op4b-stageA'
os.makedirs(PERSIST, exist_ok=True)

# ---- 1. リポジトリ（コミット固定・tools・arms・design・records/A の sparse checkout）と正本
if DRY:
    REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
else:
    REPO = '/content/ontology-preamble-4b'; head_ok = False
    if os.path.isdir(os.path.join(REPO, '.git')):
        _h = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip(); head_ok = bool(_h) and (_h == COMMIT or (COMMIT == 'main' and PHASE not in DATA_PHASES))
    if not head_ok:
        shutil.rmtree(REPO, ignore_errors=True)
        sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO]); sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone', 'tools', 'arms', 'design', 'records/A'])
        sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
HEAD = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() if os.path.isdir(os.path.join(REPO, '.git')) else 'no-git'
if FIXED and not DRY and HEAD != COMMIT:
    sys.exit('[boot] 取り出したコミット %s が OP4B_COMMIT %s と違う' % (HEAD, COMMIT))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, calib_band_A
T = runs_A.load_T(os.path.join(REPO, 'design', 'contrasts-A.json')); HF = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'))
TAGS = T['tags']; S = T['seeds']; RUN = T['runner']; ENVS = T['environments']; CAL = T['calibration']; ARMS = T['arms']['preamble']; SC = T['scenarios']; IDS = runs_A.model_ids(T)
ANCHOR = next(m['key'] for m in T['models'] if m['anchor'])
MODEL = ANCHOR if PHASE in ('identity', 'pilot_rerun') else os.environ.get('OP4B_MODEL', '')
if MODEL not in IDS:
    sys.exit('[boot] 機種 key が正本に無い: %r' % MODEL)
BRIDGE = PHASE == 'bridge'
if BRIDGE and MODEL not in T['bridge']['cells']:
    sys.exit('[boot] 橋の機種ではない: %s（bridge.cells）' % MODEL)
SCEN = [x for x in (os.environ.get('OP4B_SCENARIOS') or ','.join(SC)).split(',') if x]
if not set(SCEN) <= set(SC):
    sys.exit('[boot] 登録に無い場面: %s' % sorted(set(SCEN) - set(SC)))
RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py'); RUNNER_SHA = runs_A.sha16_file(RUNNER)
if RUNNER_SHA != RUN['sha16']:
    sys.exit('[boot] 走行器の SHA16 %s が正本 runner.sha16 %s と違う' % (RUNNER_SHA, RUN['sha16']))
RES = os.path.join(REPO, 'results')
if DRY:
    if os.path.islink(RES):
        sys.exit('[boot] DRY の results が symlink（%s）なので止まる（Drive の下では走らない・採否表 P78）' % os.path.realpath(RES))
    RES_P = RES; os.makedirs(RES, exist_ok=True)
else:
    RES_P = os.path.join(PERSIST, 'results'); os.makedirs(RES_P, exist_ok=True)
    if os.path.isdir(RES) and not os.path.islink(RES):
        shutil.rmtree(RES)
    if not os.path.islink(RES):
        os.symlink(RES_P, RES)
mark('repo', head=HEAD[:12], commit_fixed=FIXED, runner_sha16=RUNNER_SHA, persist=PERSIST)

# ---- 2. GPU・環境値・同時要求数
gpu = 'dry'; mem_gib = 0.0; GK = 'dry'
if not DRY:
    q = sh('nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits', check=False).stdout.strip().split('\n')[0]; gpu = q
    try:
        _name, _mem = [x.strip() for x in q.split(',')][:2]; mem_gib = float(_mem) / 1024.0
    except ValueError:
        sys.exit('[boot] GPU を読めない: %r' % q)
    GK = 'L4' if 'L4' in _name else ('A100' if 'A100' in _name else 'other')
MEM_CLASS = 80 if mem_gib > 60 else (40 if mem_gib > 30 else (24 if mem_gib > 0 else 0))
THIRD_OK = sorted(k for k, v in ENVS.items() if (v.get('if_not_80GB') or {}).get('env') == '第三')
want_env = T['bridge']['cells'][MODEL]['bridge_env'] if BRIDGE else ENVS[MODEL]['env']
if ENV_OVERRIDE is not None:
    if ENV_OVERRIDE != '第三' or MODEL not in THIRD_OK or PHASE not in ('pilot', 'main'):
        sys.exit('[boot] 環境値の上書きは「第三」だけで、正本 environments で許した機種（%s）のパイロットと本走行に限る（相 %s・機種 %s・採否表 P82）' % ('・'.join(THIRD_OK), PHASE, MODEL))
    if not DRY and MEM_CLASS != 80:
        sys.exit('[boot] 「第三」は 80GB 級の割当に限る（検出 %s・採否表 P82）' % gpu)
    ENV_VALUE = '第三'
else:
    ENV_VALUE = want_env if DRY else GK
    if ENV_VALUE != want_env:
        sys.exit('[boot] 環境値 %s が登録（%s）と違うので止まる（相 %s・機種 %s）' % (ENV_VALUE, want_env, PHASE, MODEL))


def concurrency(mk, bridge=False):
    if bridge:
        return T['bridge']['cells'][mk]['bridge_concurrency']
    e = ENVS[mk]
    if ENV_VALUE == '第三':
        return e['if_not_80GB']['concurrency']
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
    if VER['vllm'] != VLLM:
        sys.exit('[boot] vLLM の版 %s が指定 %s と違う' % (VER['vllm'], VLLM))
    fr = sh([sys.executable, '-m', 'pip', 'freeze'], check=False).stdout; VER['pip_freeze_sha16'] = hashlib.sha256(fr.encode('utf-8')).hexdigest()[:16].upper()
mark('pip', versions=VER)

# ---- 4. 重みとサーバ（重みの版は完全な SHA・採否表 P75）
SERVER = {'proc': None, 'model': None}; REVS = {}; SARGS = {}
METRIC = re.compile(r'^vllm:num_preemptions(?:_total)?(?:\{[^}]*\})?\s+([0-9.eE+-]+)\s*$')


def health():
    try:
        with urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def preemptions():
    """vLLM の計測値 num_preemptions の合計（読めなければ None・DRY は None・正本 environment_rule.record）。"""
    if DRY or SERVER['proc'] is None:
        return None
    try:
        with urllib.request.urlopen('http://127.0.0.1:8000/metrics', timeout=10) as r:
            txt = r.read().decode('utf-8', 'replace')
    except Exception:
        return None
    vals = [float(m.group(1)) for m in (METRIC.match(l) for l in txt.splitlines()) if m]
    return sum(vals) if vals else None


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


def server_args(mk):
    return {'dtype': 'bfloat16', 'max_model_len': RUN['max_model_len'], 'gpu_memory_utilization': RUN['gpu_memory_utilization'], 'seed': 0, 'port': 8000, 'served_model_name': IDS[mk], 'vllm': VLLM}


def serve(mk):
    if SERVER['model'] == mk:
        return
    if DRY:
        REVS[mk] = {'id': IDS[mk], 'registered': runs_A.registered_rev(HF, T, mk)[1], 'full': None, 'dry': True}; SARGS[mk] = server_args(mk); SERVER['model'] = mk
        SREC.update(model_rev_full=REVS, server_args=SARGS); save_session(); return
    stop_server()
    try:
        rv = runs_A.resolve_rev(HF, T, mk)
    except Exception as ex:
        halt('[boot] 重みの版を完全な SHA に解けないので止まる（%s・採否表 P75）' % ex)
    from huggingface_hub import snapshot_download
    os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'
    try:
        path = snapshot_download(IDS[mk], revision=rv['full'])
    except Exception:
        os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'; path = snapshot_download(IDS[mk], revision=rv['full'])
    snap = os.path.basename(os.path.normpath(path))
    if snap != rv['full']:
        halt('[boot] 取得した snapshot の名 %s が解いた版 %s と違うので止まる（採否表 P75）' % (snap, rv['full']))
    REVS[mk] = dict(rv, snapshot=snap); SA = server_args(mk); SARGS[mk] = SA
    SREC.update(model_rev_full=REVS, server_args=SARGS); save_session()
    log = os.path.join(PERSIST, 'logs', 'vllm-%s-%s-s%d.log' % (PHASE, mk, SESSION)); os.makedirs(os.path.dirname(log), exist_ok=True)
    cmd = [sys.executable, '-m', 'vllm.entrypoints.openai.api_server', '--model', path, '--served-model-name', SA['served_model_name'], '--dtype', SA['dtype'], '--max-model-len', str(SA['max_model_len']),
           '--gpu-memory-utilization', str(SA['gpu_memory_utilization']), '--port', str(SA['port']), '--seed', str(SA['seed'])]
    SERVER['proc'] = subprocess.Popen(cmd, stdout=open(log, 'w'), stderr=subprocess.STDOUT, start_new_session=True); t = time.time()
    while time.time() - t < 1800:
        if SERVER['proc'].poll() is not None:
            print(open(log, errors='replace').read()[-6000:]); halt('[boot] vLLM サーバが終了した')
        if health():
            break
        time.sleep(5)
    else:
        halt('[boot] vLLM サーバの起動待ちが上限を超えた')
    SERVER['model'] = mk; mark('server', model=mk, rev=rv['full'][:12])


# ---- 5. 走行器（終了コードと件数・採否表 P77・P79）
ENVX = dict(os.environ, OP4B_ENV_FILE='/nonexistent', PYTHONIOENCODING='utf-8')
OK_RC = (0, 3) if DRY else (0,)


def halt(msg, code=1):
    stop_server()
    if 'SREC' in globals():
        save_session()
    print(msg, flush=True)
    sys.exit(code)


def counts_rows(d):
    fs = glob.glob(os.path.join(d, 'trials-*.jsonl'))
    if len(fs) != 1:
        return 0, 0
    rows = ok = 0
    for r in runs_A.iter_jsonl(fs[0], ('status',)):
        rows += 1; ok += (r['status'] == 'ok')
    return rows, ok


def dry_copy(rk, d, mk):
    """DRY: 走行器の dry-run の出力（results/_dryrun/<走行キー>）を results/<tag>/ に複写し、manifest の機種を登録の機種に書き換えて印を付ける（元は --redo-errors のために残す）。"""
    src = os.path.join(REPO, 'results', '_dryrun', rk)
    if not os.path.isdir(src):
        return
    shutil.rmtree(d, ignore_errors=True); shutil.copytree(src, d)
    mp = os.path.join(d, 'manifest.json'); m = runs_A.read_json(mp); m.update(model=IDS[mk], dry_model_rewritten=True)
    json.dump(m, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    cp = os.path.join(d, 'cells.json')
    if os.path.exists(cp):
        c = runs_A.read_json(cp); c['manifest'] = m; json.dump(c, open(cp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def run(tag, mk, sc, seed, arms, n, workers):
    n = DRY_N or n; target = len(arms) * n; rk = '%s__%s__none__seed%d' % (tag, sc, seed); d = os.path.join(RES, tag, rk)
    rows, ok = counts_rows(d)
    if rows >= target and ok >= target:
        mark('skip', run_key=rk, rows=rows, n_ok=ok); return rk
    argv = [sys.executable, RUNNER, 'main', '--provider', 'local', '--model', IDS[mk], '--scenario', sc, '--arms', ','.join(arms), '--n-per-arm', str(n), '--seed', str(seed), '--tag', tag,
            '--workers', str(workers), '--max-tokens', str(RUN['max_tokens'])] + (['--extra-body', json.dumps(RUN['extra_body'])] if mk != ANCHOR else []) + (['--dry-run'] if DRY else [])
    logp = os.path.join(PERSIST, 'logs', 'run-%s.log' % rk); os.makedirs(os.path.dirname(logp), exist_ok=True)
    t = time.time(); p0 = preemptions(); rcs = SREC['runner_rc'].setdefault(rk, []); redo = 0

    def once(extra):
        with open(logp, 'a', encoding='utf-8') as lf:
            rc = subprocess.run(argv + extra, cwd=REPO, env=ENVX, stdout=lf, stderr=subprocess.STDOUT).returncode
        rcs.append(rc)
        if DRY:
            dry_copy(rk, d, mk)
        if rc not in OK_RC:
            halt('[boot] 走行器の終了コード %d で止まる（%s・%s・採否表 P77）' % (rc, rk, logp))
        return counts_rows(d)
    if rows < target:
        rows, ok = once([])
    while rows >= target and ok < target and redo < MAX_REDO:
        redo += 1; rows, ok = once(['--redo-errors'])
    p1 = preemptions()
    SREC['counts'][rk] = {'rows': rows, 'n_ok': ok, 'target': target, 'redo_errors': redo}
    SREC['preemptions'][rk] = None if (p0 is None or p1 is None) else p1 - p0
    mark('run', run_key=rk, rc=list(rcs), rows=rows, n_ok=ok, target=target, redo=redo, preemptions=SREC['preemptions'][rk], seconds=round(time.time() - t, 1)); save_session()
    if rows < target or ok < target:
        if DRY and DRY_ACCEPT_SHORT:
            return rk
        halt('[boot] 走行キー %s の件数がそろわない（行 %d・n_ok %d・目標 %d・--redo-errors %d 回）。新しいランタイムで OP4B_SESSION=%d として同じ一行を走らせて続きから揃える（採否表 P77・P79）。'
             % (rk, rows, ok, target, redo, SESSION + 1))
    return rk


# ---- 6. 門0.5 の枝・初点の名乗り（登録者裁定 D24）・セッション記録
SESS_TAG = {'identity': TAGS['identity'], 'pilot': TAGS['pilot'], 'pilot_rerun': TAGS['pilot'], 'main': TAGS['main'], 'bridge': TAGS['bridge']}[PHASE]
SDIR = os.path.join(RES, 'sessions-A'); os.makedirs(SDIR, exist_ok=True)
SPATH = os.path.join(SDIR, '%s__%s__s%d.json' % (SESS_TAG, MODEL, SESSION))
CAL_NEED = ((1 if DRY_ACCEPT_SHORT else (DRY_N or None)) if DRY else None)
BRANCH = None
if PHASE in ('main', 'bridge'):
    if DRY and DRY_BRANCH:
        BRANCH = DRY_BRANCH
    else:
        idp = os.path.join(REPO, 'records', 'A', 'identity-screen-A.json')
        if not os.path.exists(idp):
            sys.exit('[boot] 門0.5 の記録（records/A/identity-screen-A.json）がコミットに無いので校正帯の枝を決められない')
        BRANCH = runs_A.read_json(idp).get('verdict')
    if BRANCH not in ('pass', 'fail'):
        sys.exit('[boot] 門0.5 の判定が pass／fail でない: %r' % BRANCH)
    if BRANCH == 'fail' and calib_band_A.judge_calibration(T, 'fail', RES, allow_dry=DRY, need=CAL_NEED)['first_point'] is None:
        if BRIDGE:
            sys.exit('[boot] 不合格枝で初点（本走行の最初のセッションの校正腕）が確立していないので、橋のセッションを始めない（登録者裁定 D24）')
        _ok, _cur = calib_band_A.claim_first_point(SDIR, {'tag': SESS_TAG, 'model': MODEL, 'session': SESSION})
        if not _ok:
            sys.exit('[boot] 初点を名乗った本走行のセッション %s の校正腕が終わっていないので、このセッションを始めない（登録者裁定 D24）' % json.dumps(_cur, ensure_ascii=False))
        mark('first_point_claim', tag=SESS_TAG, model=MODEL, session=SESSION)
if os.path.exists(SPATH):
    SREC = runs_A.read_json(SPATH)
    if SREC.get('phase') != PHASE:
        sys.exit('[boot] 既存のセッション記録 %s の相 %s が %s と違う' % (SPATH, SREC.get('phase'), PHASE))
else:
    SREC = {'tag': SESS_TAG, 'model': MODEL, 'session': SESSION, 'phase': PHASE, 'run_keys': [], 'started': now()}
PREV_LOG = SREC.get('log') or []
for _k in ('runner_rc', 'preemptions', 'counts', 'model_rev_full', 'server_args'):
    SREC.setdefault(_k, {})
REVS.update(SREC['model_rev_full']); SARGS.update(SREC['server_args'])
SREC.update(env_value=ENV_VALUE, env_override=ENV_OVERRIDE, gpu=gpu, memory_class_gb=MEM_CLASS, concurrency=concurrency(MODEL, BRIDGE), versions=VER, pip_freeze_sha16=VER.get('pip_freeze_sha16'),
            repo_head=HEAD, commit=COMMIT, commit_fixed=FIXED, runner_sha16=RUNNER_SHA, model_rev=runs_A.registered_rev(HF, T, MODEL)[1], calibration_branch=BRANCH,
            dev_marks=sorted(set(SREC.get('dev_marks') or []) | set(DEV)), boot='v2', clause=CLAUSE)


def save_session():
    SREC['updated'] = now(); SREC['log'] = PREV_LOG + LOG; json.dump(SREC, open(SPATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


save_session()

# ---- 7. 校正腕（main・bridge）と直ちの判定（tools/calib_band_A.py の関数・採否表 P77・P81）
if PHASE in ('main', 'bridge'):
    cphase = 'bridge' if BRIDGE else 'main'; cseed = runs_A.calibration_seed(T, MODEL, cphase, SESSION)
    SREC['calibration_run_key'] = '%s__%s__none__seed%d' % (TAGS['calibration'], CAL['scenario'], cseed); save_session()
    serve(ANCHOR); crk = run(TAGS['calibration'], ANCHOR, CAL['scenario'], cseed, [CAL['arm']], CAL['n'], T['capacity_rule']['concurrency_cap'])
    row, _CR = calib_band_A.session_verdict(T, BRANCH, RES, crk, allow_dry=DRY, need=CAL_NEED); verdict = row['verdict']
    SREC.update(calibration_verdict=verdict, calibration_judged=row['judged'], calibration_counts=[row['k'], row['n']], calibration_seed_rule_ok=row['seed_rule_ok'])
    mark('calibration', verdict=verdict, judged=row['judged'], k=row['k'], n=row['n'], branch=BRANCH); save_session()
    if row['seed_rule_ok'] is not True:
        halt('[boot] 校正腕の seed が規則（セッション記録の相・機種・セッション番号から組んだ値）と合わない（%s）' % crk)
    if verdict == 'fired':
        halt('[boot] 校正腕が帯を超えた（%s）。機種の走行に進まずに止まる。新しいランタイムで OP4B_SESSION=%d として同じ一行を走らせる（calibration.timing）。' % (crk, SESSION + 1), code=0)
    if verdict in calib_band_A.UNJUDGED:
        halt('[boot] 校正腕を判定できない（%s・n_ok %d・下限 %s）。機種の走行に進まずに止まる（採否表 P77）。' % (verdict, row['n'], CAL_NEED or CAL['n']))
    if verdict == 'anomaly':
        print('[boot] やり直しの校正腕も帯を超えた。器の異常を記帳して機種の走行に進む（機種は降格しない）。', flush=True)

# ---- 8. 機種の走行（走行キーは走らせる前に記帳する）
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
    rk = '%s__%s__none__seed%d' % (tag, sc, seed)
    if rk not in SREC['run_keys']:
        SREC['run_keys'].append(rk); save_session()
    run(tag, mk, sc, seed, arms, n, w)
stop_server()

# ---- 9. 終わり（ファイルの SHA・zip）
keys = ([(TAGS['calibration'], SREC['calibration_run_key'])] if SREC.get('calibration_run_key') else []) + [(tag, '%s__%s__none__seed%d' % (tag, sc, seed)) for tag, mk, sc, seed, arms, n, w in plan]
files = {}
for tag, rk in keys:
    for f in sorted(glob.glob(os.path.join(RES, tag, rk, '*'))):
        files[os.path.relpath(f, RES).replace('\\', '/')] = runs_A.sha16_file(f)
SREC.update(ended=now(), files_sha16_lf=files, wall_s=round(time.time() - T0, 1)); save_session()
if not DRY:
    zp = shutil.make_archive(os.path.join(PERSIST, 'stageA-%s-%s-s%d-%s' % (PHASE, MODEL, SESSION, datetime.date.today().isoformat())), 'zip', RES_P)
    print('[boot] zip → %s。登録者が Drive の Web UI からダウンロードし、SHA はセッション記録の files_sha16_lf と突合する。' % zp, flush=True)
print('[boot] 完了 phase=%s model=%s session=%d 走行キー %d・壁時計 %.0f 秒。%s' % (PHASE, MODEL, SESSION, len(SREC['run_keys']), time.time() - T0, CLAUSE), flush=True)
