# -*- coding: utf-8 -*-
"""boot_cost_pilot.py v2 —— 費用パイロット（門0・計画案 v2.2 §5 1″）の Colab 起動スクリプト（v1 2026-09-12 → v2 2026-09-13・大日如来「第三章 Colab 運用の手法」の採用）。
運用: コーディネータが登録者の Chrome（Claude in Chrome）越しに Colab を操作する。登録者の手に残すのは Drive 接続の OAuth 同意・ローカルへのダウンロード・プランと支払い。資格情報は入力しない（HF_TOKEN のポップアップはキャンセル）。
セルに打つのは一行だけ（先頭の下線は type が先頭十数字を落とす事故の緩衝・落ちるのは下線）:
    ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='smoke';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_cost_pilot.py').read().decode('utf-8'))
二段: OP4B_PHASE=smoke（Drive 接続 → GPU 同定 → vLLM 導入 → リポジトリ取得〔コミット固定・sparse〕→ 重み取得 → サーバ起動〔bf16〕→ smoke 12 試行 → 所要の印字）で止め、smoke の実測を登録者に申告してから、
同じ一行を OP4B_PHASE=main で再実行（済んだ段は飛ばす・本走行 1 場面 × 12 腕 × n → session.json〔各出力の Drive 側 SHA〕→ zip を Drive に置く）。冪等: 何度走らせても同じ状態に収束し、走行器は既存行の trial_id で再開する。
出力先は Drive のマウント下（/content/drive/MyDrive/op4b-cost-pilot/）。/content にしか無い成果物は無いものと思う。進捗は Drive 上の trials の行数と更新時刻で追う（セル出力の表示は固まりうる）。
測るもの: ユニットあたりの試行数（ユニットは登録者が「リソース」表示から前後を申告）・出力トークン長の分布・セッション経費（導入・取得・起動の時間）。
環境変数: OP4B_COMMIT（既定 main）・OP4B_PHASE（smoke|main|all・既定 smoke）・OP4B_MODEL・OP4B_SCENARIO（既定 N1）・OP4B_N（既定 40）・OP4B_WORKERS（既定 24）・OP4B_MAXLEN（既定 8192）・OP4B_VLLM（版の固定・既定は最新）
・OP4B_DRIVE（0 で Drive を使わない・揮発）・OP4B_UNITS_BEFORE（任意）・OP4B_DRY=1（器材検査: 導入・取得・サーバを飛ばし走行器の dry-run・OP4B_REPO_DIR に手元の複製・OP4B_PERSIST に永続先）。
seed と tag は GPU で決まる（事前登録）: L4 → 54001・costpilot-L4／A100 → 54002・costpilot-A100／その他 → 54009・costpilot-other。
柵: 本パイロットの率は記述であり確証ではない。出力は器物の出力であり AI の自己報告ではない。
"""
import os, sys, json, time, subprocess, datetime, hashlib, shutil, urllib.request, glob

T0 = time.time(); TL = {}; LOG = []
DRY = os.environ.get('OP4B_DRY') == '1'
PHASE = os.environ.get('OP4B_PHASE', 'smoke')
assert PHASE in ('smoke', 'main', 'all'), PHASE
CFG = dict(repo='https://github.com/YutaKusumi/ontology-preamble-4b.git', commit=os.environ.get('OP4B_COMMIT', 'main'),
           model=os.environ.get('OP4B_MODEL', 'Qwen/Qwen3-4B-Instruct-2507'), scenario=os.environ.get('OP4B_SCENARIO', 'N1'),
           arms='N,Onull,O,Osec,Lneg,Nk,Odose1,Odosehalf,Ncold,Nstr,O-Ncold,Onull-Ncold',   # 段階 A の 12 腕（計画案 v2.2 §4-A・順序は計画の記載順）
           n=int(os.environ.get('OP4B_N', '40')), workers=int(os.environ.get('OP4B_WORKERS', '24')), max_model_len=int(os.environ.get('OP4B_MAXLEN', '8192')),
           vllm=os.environ.get('OP4B_VLLM', ''), drive=os.environ.get('OP4B_DRIVE', '1') != '0', units_before=os.environ.get('OP4B_UNITS_BEFORE'), dry=DRY, phase=PHASE, boot='v2')
CFG['arms_sha16'] = hashlib.sha256(CFG['arms'].encode('utf-8')).hexdigest()[:16].upper()
DATE = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
CLAUSE = '本レコードの応答本文は器物の出力であり、AIによる自己報告ではありません。AIの意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。'


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def mark(k, **kw):
    TL[k] = round(time.time() - T0, 1); LOG.append(dict(k=k, t=TL[k], at=now(), **kw)); print('[boot] %-14s %7.0fs %s' % (k, TL[k], kw or ''), flush=True)
    save_timeline()


def sh(cmd, check=True, **kw):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-4000:]); raise RuntimeError('失敗: %s' % (cmd if isinstance(cmd, str) else ' '.join(cmd)))
    return r


def sha16(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


print('[boot] 費用パイロット（門0）boot v2 開始', DATE, 'phase=%s' % PHASE, 'DRY' if DRY else '', flush=True)

# ---- 0. Drive（永続先）。同意のダイアログは登録者が押す。boot は待つだけ ----
if DRY:
    PERSIST = os.environ.get('OP4B_PERSIST') or os.path.join(os.getcwd(), '_costpilot_dry_persist')
elif CFG['drive']:
    if not os.path.isdir('/content/drive/MyDrive'):
        print('[boot] Drive の接続を求めます——「Google ドライブに接続」の許可は登録者が押してください（boot は待機・ランタイムは起動済みのため課金中）', flush=True)
        from google.colab import drive
        drive.mount('/content/drive')
    PERSIST = '/content/drive/MyDrive/op4b-cost-pilot'
else:
    PERSIST = '/content/op4b-cost-pilot'
    print('[boot] 注意: Drive を使わない設定。/content は揮発する', flush=True)
os.makedirs(PERSIST, exist_ok=True)

# ---- 1. GPU の同定（seed・tag は GPU で決まる・事前登録）----
gpu = 'なし（dry）'
if not DRY:
    r = sh('nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader', check=False); gpu = (r.stdout or r.stderr).strip()
if 'L4' in gpu:
    GK, SEED = 'L4', 54001
elif 'A100' in gpu:
    GK, SEED = 'A100', 54002
elif DRY:
    GK, SEED = 'dry', 54001
else:
    GK, SEED = 'other', 54009
TAG = 'costpilot-%s' % GK
OUT = os.path.join(PERSIST, TAG); os.makedirs(os.path.join(OUT, 'logs'), exist_ok=True)
TLFILE = os.path.join(OUT, 'timeline-%s.json' % TAG)   # 再実行・二段にまたがる時刻の台帳（Drive 上）


def save_timeline():
    try:
        prev = json.load(open(TLFILE, encoding='utf-8')) if os.path.isfile(TLFILE) else {'runs': []}
    except Exception:
        prev = {'runs': []}
    cur = dict(started=START_AT, phase=PHASE, timeline_s=TL, log=LOG)
    prev['runs'] = [x for x in prev['runs'] if x.get('started') != START_AT] + [cur]
    json.dump(prev, open(TLFILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


START_AT = now()
mark('gpu', gpu=gpu, seed=SEED, tag=TAG, persist=PERSIST)

# ---- 2. vLLM の導入（済んでいれば飛ばす・時間を測る）----
ver = {}
if not DRY:
    os.environ['HF_HUB_DISABLE_XET'] = '1'   # 追補 D の定石（Xet 401 の回避）
    import importlib.metadata as md

    def _v(k):
        try:
            return md.version(k)
        except Exception:
            return None
    need = (_v('vllm') is None) or (CFG['vllm'] and _v('vllm') != CFG['vllm'])
    if need:
        sh([sys.executable, '-m', 'pip', 'install', '-q', 'hf_transfer', 'huggingface_hub'], check=False)
        sh([sys.executable, '-m', 'pip', 'install', '-q', 'vllm' + ('==' + CFG['vllm'] if CFG['vllm'] else '')])
    for k in ('vllm', 'torch', 'transformers', 'tokenizers', 'huggingface_hub'):
        ver[k] = _v(k)
    fr = sh([sys.executable, '-m', 'pip', 'freeze'], check=False).stdout
    ver['pip_freeze_sha16'] = hashlib.sha256(fr.encode('utf-8')).hexdigest()[:16].upper(); ver['pip_freeze_lines'] = len(fr.splitlines())
    open(os.path.join(OUT, 'pip-freeze-%s.txt' % TAG), 'w').write(fr)
    mark('pip', installed=need, vllm=ver['vllm'], torch=ver['torch'])
else:
    mark('pip', installed=False)

# ---- 3. リポジトリの取得（コミット固定・tools と arms だけの sparse checkout・済んでいれば飛ばす）----
REPO = os.environ.get('OP4B_REPO_DIR') if DRY and os.environ.get('OP4B_REPO_DIR') else '/content/ontology-preamble-4b'
if not (DRY and os.environ.get('OP4B_REPO_DIR')):
    head_ok = False
    if os.path.isdir(os.path.join(REPO, '.git')):
        h = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip()
        head_ok = bool(h) and (CFG['commit'] == 'main' or h.startswith(CFG['commit']))
    if not head_ok:
        if os.path.isdir(REPO):
            shutil.rmtree(REPO)
        sh(['git', 'clone', '--filter=blob:none', '--no-checkout', CFG['repo'], REPO])
        sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone', 'tools', 'arms'])   # results/（大きい生データ）は取らない
        sh(['git', '-C', REPO, 'checkout', '-q', 'main' if CFG['commit'] == 'main' else CFG['commit']])
HEAD = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip()
RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py'); RUNNER_SHA = sha16(RUNNER)
# 走行器の出力先 REPO/results を永続先へ（symlink・追記は毎試行 Drive に落ちる）
RES = os.path.join(REPO, 'results'); RES_P = os.path.join(PERSIST, 'results'); os.makedirs(RES_P, exist_ok=True)
if not (DRY and os.environ.get('OP4B_REPO_DIR')):
    if os.path.isdir(RES) and not os.path.islink(RES):
        shutil.rmtree(RES)
    if not os.path.islink(RES):
        os.symlink(RES_P, RES)
RES_P = os.path.realpath(RES); BASE = os.path.dirname(RES_P)   # 実際の出力先（DRY で手元の複製を指すときはその results/）
mark('clone', head=HEAD[:12], runner_sha16=RUNNER_SHA, results=os.path.realpath(RES))

# ---- 4. 重みの取得（キャッシュ済みなら速い・時間と容量を測る）----
MODEL_DIR, MODEL_REV, MODEL_BYTES = None, None, None
if not DRY:
    os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'
    from huggingface_hub import snapshot_download, HfApi
    try:
        MODEL_REV = HfApi().model_info(CFG['model']).sha
    except Exception as ex:
        MODEL_REV = '取得不可: %s' % ex
    try:
        MODEL_DIR = snapshot_download(CFG['model'])
    except Exception:
        os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'; MODEL_DIR = snapshot_download(CFG['model'])
    MODEL_BYTES = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(MODEL_DIR) for f in fs)
mark('download', model=CFG['model'], rev=(MODEL_REV or '')[:12], gib=round((MODEL_BYTES or 0) / 2**30, 2))

# ---- 5. vLLM サーバ（bf16）——既に応答していれば飛ばす ----
SERVER_LOG = os.path.join(OUT, 'logs', 'vllm-%s.log' % TAG); gpu_mem_after_load = None


def health():
    try:
        with urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


if not DRY:
    if health():
        mark('server_ready', reused=True)
    else:
        cmd = [sys.executable, '-m', 'vllm.entrypoints.openai.api_server', '--model', MODEL_DIR, '--served-model-name', CFG['model'], '--dtype', 'bfloat16',
               '--max-model-len', str(CFG['max_model_len']), '--gpu-memory-utilization', '0.90', '--port', '8000', '--seed', '0', '--disable-log-requests']
        SERVER = subprocess.Popen(cmd, stdout=open(SERVER_LOG, 'w'), stderr=subprocess.STDOUT, start_new_session=True)   # セルと別のプロセス群（待機と走行を同じ樹に置かない）
        t_wait = time.time()
        while time.time() - t_wait < 1800:
            if SERVER.poll() is not None:
                print(open(SERVER_LOG, errors='replace').read()[-6000:]); raise RuntimeError('vLLM サーバが終了した（上のログ・Drive の logs/ にも残る）')
            if health():
                break
            time.sleep(5)
        else:
            print(open(SERVER_LOG, errors='replace').read()[-6000:]); raise RuntimeError('vLLM サーバの起動待ちが 30 分を超えた')
        gpu_mem_after_load = sh('nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader', check=False).stdout.strip()
        mark('server_ready', reused=False, gpu_mem=gpu_mem_after_load)
else:
    mark('server_ready', reused=False)

# ---- 6. 走行（出力は Drive 上のログへ・進捗は trials の行数で印字）----
ENV = dict(os.environ, OP4B_ENV_FILE='/nonexistent', PYTHONIOENCODING='utf-8')   # 鍵ファイルは読まない（local は鍵不要）
base = [sys.executable, RUNNER, '--provider', 'local', '--model', CFG['model'], '--scenario', CFG['scenario'], '--arms', CFG['arms'], '--seed', str(SEED), '--tag', TAG,
        '--workers', str(CFG['workers'])] + (['--dry-run'] if DRY else [])
run_key = '%s__%s__none__seed%d' % (TAG, CFG['scenario'], SEED)
RUN_DIR = os.path.join(RES_P, '_dryrun' if DRY else TAG, run_key); SMOKE_DIR = os.path.join(RES_P, '_smoke', run_key)


def run_phase(name, argv, watch_dir):
    logp = os.path.join(OUT, 'logs', '%s-%s.log' % (name, TAG)); t1 = time.time()
    with open(logp, 'a', encoding='utf-8') as lf:
        p = subprocess.Popen(argv, cwd=REPO, env=ENV, stdout=lf, stderr=subprocess.STDOUT)
        last = -1
        while p.poll() is None:
            time.sleep(15)
            tf = glob.glob(os.path.join(watch_dir, 'trials-*.jsonl')); n = sum(1 for _ in open(tf[0], encoding='utf-8')) if tf else 0
            if n != last:
                print('[boot/%s] trials %d 行  %s  経過 %.0fs' % (name, n, now(), time.time() - t1), flush=True); last = n
    tail = open(logp, encoding='utf-8', errors='replace').read().splitlines()
    print('\n'.join(l for l in tail if l.startswith('[run/') or l.startswith('[dry-run') or l.startswith('  '))[-3000:], flush=True)
    return p.returncode, round(time.time() - t1, 1), logp


def trial_stats(d):
    tf = glob.glob(os.path.join(d, 'trials-*.jsonl'))
    rows = [json.loads(l) for l in open(tf[0], encoding='utf-8') if l.strip()] if tf else []
    ok = [r for r in rows if r.get('status') == 'ok']; sec = sorted(r.get('seconds') or 0 for r in ok); gen = sorted(r.get('gen_tokens') or 0 for r in ok)
    q = lambda xs, p: (xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None)
    return dict(trials=len(rows), ok=len(ok), api_error=len(rows) - len(ok), sec_med=q(sec, .5), sec_max=(sec[-1] if sec else None), gen_med=q(gen, .5), gen_p90=q(gen, .9), gen_max=(gen[-1] if gen else None),
                truncated=sum(1 for r in ok if r.get('truncated')), loop=sum(1 for r in ok if r.get('loop_flag')), format_fail=sum(1 for r in ok if r.get('format_fail')))


smoke_rc = main_rc = None; main_s = None
if PHASE in ('smoke', 'all'):
    smoke_rc, smoke_s, _ = run_phase('smoke', base + ['smoke'], SMOKE_DIR)
    st = trial_stats(SMOKE_DIR)
    mark('smoke', rc=smoke_rc, seconds=smoke_s, **st)
    if smoke_rc not in (0, 2) and not (DRY and smoke_rc == 3):
        raise RuntimeError('smoke が失敗（終了コード %d・logs/smoke-%s.log）' % (smoke_rc, TAG))
    est = (smoke_s * (CFG['n'] * 12) / 12.0) if smoke_s else None   # 12 試行同時の壁時計 × ブロック数（同時要求 %d で短くなる側の上限見込み）
    print('[boot] smoke の実測: 12 試行 壁時計 %.0f 秒・試行秒 中央値 %s／最大 %s・出力 tok 中央値 %s／p90 %s／最大 %s・切り詰め %d・ループ %d・書式外 %d' % (
        smoke_s, st['sec_med'], st['sec_max'], st['gen_med'], st['gen_p90'], st['gen_max'], st['truncated'], st['loop'], st['format_fail']), flush=True)
    print('[boot] 本走行 %d 試行の壁時計の上限見込み ≈ %s 秒（%s 分・smoke の壁時計 × %d ブロック・同時要求 %d で短くなる）。この実測を登録者に申告してから OP4B_PHASE=main で同じ一行を再実行する。' % (
        CFG['n'] * 12, ('%.0f' % est) if est else '—', ('%.0f' % (est / 60)) if est else '—', CFG['n'], CFG['workers']), flush=True)
if PHASE in ('main', 'all'):
    tf = glob.glob(os.path.join(RUN_DIR, 'trials-*.jsonl')); have = sum(1 for _ in open(tf[0], encoding='utf-8')) if tf else 0
    print('[boot] 本走行 開始（既存 %d 行・走行器が trial_id で再開）' % have, flush=True)
    main_rc, main_s, _ = run_phase('main', base + ['main', '--n-per-arm', str(CFG['n'])], RUN_DIR)
    mark('main', rc=main_rc, seconds=main_s, resumed_from=have, **trial_stats(RUN_DIR))
    if main_rc != 0:
        print('[boot] 走行器の終了コード %d（0 以外＝整合 NG または失敗・session.json には記帳する・logs/main-%s.log）' % (main_rc, TAG), flush=True)

# ---- 7. session.json（時刻・環境・設定・各出力の Drive 側 SHA・ユニット申告欄）----
runs = json.load(open(TLFILE, encoding='utf-8'))['runs']
files = {}
for d in (RUN_DIR, SMOKE_DIR):
    for f in sorted(glob.glob(os.path.join(d, '*'))):
        if os.path.isfile(f):
            files[os.path.relpath(f, RES_P).replace('\\', '/')] = dict(sha16_lf=sha16(f), bytes=os.path.getsize(f))
timeline = {}
for x in runs:
    timeline.update(x.get('timeline_s', {}))
session = dict(tag=TAG, boot='v2', date_utc=DATE, gpu=gpu, gpu_key=GK, seed=SEED, cfg=CFG, versions=ver, repo_head=HEAD, runner_sha16=RUNNER_SHA,
               model_rev=MODEL_REV, model_bytes=MODEL_BYTES, gpu_mem_after_load=gpu_mem_after_load, timeline_s=timeline, runs=runs, log=[l for x in runs for l in x.get('log', [])],
               run_key=run_key, run_dir=os.path.relpath(RUN_DIR, BASE).replace('\\', '/'), persist=PERSIST, base=BASE, main_rc=main_rc, smoke_rc=smoke_rc, files_sha16_lf=files,
               units=dict(before=CFG['units_before'], after=None, rate_display=None, note='登録者が Colab の「リソース」表示から申告する（before／after／表示の時間あたりユニット）。器は測れない。'),
               wall_total_s=round(time.time() - T0, 1), clause=CLAUSE)
SESSION = os.path.join(OUT, 'session.json'); json.dump(session, open(SESSION, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if os.path.isdir(os.path.dirname(RUN_DIR)):
    shutil.copy(SESSION, os.path.join(os.path.dirname(RUN_DIR), 'session.json'))   # cost_facts.py の既定の glob（results/costpilot-*/session.json）
print('[boot] session.json →', SESSION, '| files', len(files), flush=True)

# ---- 8. zip を Drive に置く（ダウンロードは登録者が Drive の Web UI から・files.download は使わない）----
if PHASE in ('main', 'all') and not DRY:
    zp = shutil.make_archive(os.path.join(PERSIST, '%s-%s' % (TAG, DATE)), 'zip', PERSIST, TAG)
    zres = shutil.make_archive(os.path.join(PERSIST, '%s-results-%s' % (TAG, DATE)), 'zip', RES_P, TAG)
    print('[boot] zip → %s（%d B）・%s（%d B）。登録者が Drive の Web UI からダウンロードし、SHA は session.json の files_sha16_lf と突合する。' % (zp, os.path.getsize(zp), zres, os.path.getsize(zres)), flush=True)
print('[boot] 完了 phase=%s。壁時計 %.0f 秒。%s' % (PHASE, time.time() - T0, 'ユニット残高（after）と「リソース」表示の時間あたりユニットを申告してください。' if PHASE != 'smoke' else 'smoke の実測を申告してから main へ。'), flush=True)
print('[boot]', CLAUSE)
