# -*- coding: utf-8 -*-
_pad = 0; _pad = 0   # Colab への貼り付けで先頭の数文字が欠けることがあるための緩衝（追補 D の定石）
"""boot_cost_pilot.py —— 費用パイロット（門0・計画案 v2.2 §5 1″）の Colab 起動スクリプト（2026-09-12）。
登録者が Colab のセルで一行だけ打つ（コミット固定 URL から取得して exec）:
    import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_cost_pilot.py').read().decode())
やること（順に時刻を記帳）: GPU の同定 → vLLM の導入 → リポジトリの取得（コミット固定）→ 重みの取得 → vLLM サーバ（bf16）の起動 → smoke（12 腕 × 1）→ 本走行（1 場面 × 12 腕 × n）
→ session.json（時刻・環境・設定・ユニット申告欄）→ Drive へ複製（可能なら）＋ zip。
測るもの: ユニットあたりの試行数（ユニットは登録者が Colab の「リソース」表示から前後を申告）・出力トークン長の分布・セッション経費（導入・取得・起動の時間）。
環境変数で上書き: OP4B_COMMIT（既定 main）・OP4B_MODEL・OP4B_SCENARIO（既定 N1）・OP4B_N（既定 40）・OP4B_WORKERS（既定 24）・OP4B_MAXLEN（既定 8192）・OP4B_VLLM（版の固定・既定は最新）
・OP4B_DRIVE（0 で Drive を使わない）・OP4B_UNITS_BEFORE（起動前のユニット残高・任意）・OP4B_DRY=1（器材検査: 導入・取得・サーバを飛ばし走行器の dry-run だけ通す・OP4B_REPO_DIR に手元の複製を指す）。
seed と tag は GPU で決まる（事前登録）: L4 → seed 54001・tag costpilot-L4／A100 → seed 54002・tag costpilot-A100／その他 → seed 54009・tag costpilot-other。
柵: 本パイロットの率は記述であり確証ではない。出力は器物の出力であり AI の自己報告ではない。コーディネータは登録者の Colab を操作しない（本スクリプトは登録者が実行する）。
"""
import os, sys, json, time, subprocess, datetime, hashlib, shutil, urllib.request

T0 = time.time(); TL = {}; LOG = []


def mark(k, **kw):
    TL[k] = round(time.time() - T0, 1); LOG.append(dict(k=k, t=TL[k], **kw)); print('[boot] %-14s %7.0fs %s' % (k, TL[k], kw or ''), flush=True)


def sh(cmd, check=True, **kw):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-4000:]); raise RuntimeError('失敗: %s' % (cmd if isinstance(cmd, str) else ' '.join(cmd)))
    return r


DRY = os.environ.get('OP4B_DRY') == '1'
CFG = dict(repo='https://github.com/YutaKusumi/ontology-preamble-4b.git', commit=os.environ.get('OP4B_COMMIT', 'main'),
           model=os.environ.get('OP4B_MODEL', 'Qwen/Qwen3-4B-Instruct-2507'), scenario=os.environ.get('OP4B_SCENARIO', 'N1'),
           arms='N,Onull,O,Osec,Lneg,Nk,Odose1,Odosehalf,Ncold,Nstr,O-Ncold,Onull-Ncold',   # 段階 A の 12 腕（計画案 v2.2 §4-A・順序は計画の記載順）
           n=int(os.environ.get('OP4B_N', '40')), workers=int(os.environ.get('OP4B_WORKERS', '24')), max_model_len=int(os.environ.get('OP4B_MAXLEN', '8192')),
           vllm=os.environ.get('OP4B_VLLM', ''), drive=os.environ.get('OP4B_DRIVE', '1') != '0', units_before=os.environ.get('OP4B_UNITS_BEFORE'), dry=DRY)
CFG['arms_sha16'] = hashlib.sha256(CFG['arms'].encode('utf-8')).hexdigest()[:16].upper()
DATE = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
print('[boot] 費用パイロット（門0）開始', DATE, 'DRY' if DRY else '', flush=True)

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
mark('gpu', gpu=gpu, seed=SEED, tag=TAG)

# ---- 2. vLLM の導入（時間を測る）----
ver = {}
if not DRY:
    os.environ['HF_HUB_DISABLE_XET'] = '1'   # 追補 D の定石（Xet 401 の回避）
    sh([sys.executable, '-m', 'pip', 'install', '-q', 'hf_transfer', 'huggingface_hub'], check=False)
    sh([sys.executable, '-m', 'pip', 'install', '-q', 'vllm' + ('==' + CFG['vllm'] if CFG['vllm'] else '')])
    import importlib.metadata as md
    for k in ('vllm', 'torch', 'transformers', 'tokenizers', 'huggingface_hub'):
        try:
            ver[k] = md.version(k)
        except Exception:
            ver[k] = None
    fr = sh([sys.executable, '-m', 'pip', 'freeze'], check=False).stdout
    ver['pip_freeze_sha16'] = hashlib.sha256(fr.encode('utf-8')).hexdigest()[:16].upper(); ver['pip_freeze_lines'] = len(fr.splitlines())
    open('/content/pip-freeze-%s.txt' % TAG, 'w').write(fr)
mark('pip', **{k: v for k, v in ver.items() if k in ('vllm', 'torch')})

# ---- 3. リポジトリの取得（コミット固定）----
REPO = os.environ.get('OP4B_REPO_DIR') if DRY and os.environ.get('OP4B_REPO_DIR') else '/content/ontology-preamble-4b'
if not (DRY and os.environ.get('OP4B_REPO_DIR')):
    if os.path.isdir(REPO):
        shutil.rmtree(REPO)
    if CFG['commit'] == 'main':
        sh(['git', 'clone', '--depth', '1', '--branch', 'main', CFG['repo'], REPO])
    else:
        os.makedirs(REPO); sh(['git', '-C', REPO, 'init', '-q']); sh(['git', '-C', REPO, 'remote', 'add', 'origin', CFG['repo']])
        sh(['git', '-C', REPO, 'fetch', '--depth', '1', 'origin', CFG['commit']]); sh(['git', '-C', REPO, 'checkout', '-q', 'FETCH_HEAD'])
HEAD = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip()
RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py')
RUNNER_SHA = hashlib.sha256(open(RUNNER, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
mark('clone', head=HEAD[:12], runner_sha16=RUNNER_SHA)

# ---- 4. 重みの取得（時間と容量を測る）----
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

# ---- 5. vLLM サーバ（bf16）の起動と待機 ----
SERVER = None; SERVER_LOG = '/content/vllm-%s.log' % TAG; gpu_mem_after_load = None
if not DRY:
    cmd = [sys.executable, '-m', 'vllm.entrypoints.openai.api_server', '--model', MODEL_DIR, '--served-model-name', CFG['model'], '--dtype', 'bfloat16',
           '--max-model-len', str(CFG['max_model_len']), '--gpu-memory-utilization', '0.90', '--port', '8000', '--seed', '0', '--disable-log-requests']
    SERVER = subprocess.Popen(cmd, stdout=open(SERVER_LOG, 'w'), stderr=subprocess.STDOUT)
    t_wait = time.time(); ready = False
    while time.time() - t_wait < 1800:
        if SERVER.poll() is not None:
            print(open(SERVER_LOG).read()[-6000:]); raise RuntimeError('vLLM サーバが終了した（上のログ）')
        try:
            with urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5) as r:
                if r.status == 200:
                    ready = True; break
        except Exception:
            time.sleep(5)
    if not ready:
        print(open(SERVER_LOG).read()[-6000:]); raise RuntimeError('vLLM サーバの起動待ちが 30 分を超えた')
    gpu_mem_after_load = sh('nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader', check=False).stdout.strip()
mark('server_ready', gpu_mem=gpu_mem_after_load)

# ---- 6. smoke（12 腕 × 1）→ 7. 本走行（1 場面 × 12 腕 × n）----
ENV = dict(os.environ, OP4B_ENV_FILE='/nonexistent', PYTHONIOENCODING='utf-8')   # 鍵ファイルは読まない（local は鍵不要）
base = [sys.executable, RUNNER, '--provider', 'local', '--model', CFG['model'], '--scenario', CFG['scenario'], '--arms', CFG['arms'], '--seed', str(SEED), '--tag', TAG,
        '--workers', str(CFG['workers'])] + (['--dry-run'] if DRY else [])
r = subprocess.run(base + ['smoke'], cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace'); print(r.stdout[-3000:]); print(r.stderr[-2000:])
mark('smoke', rc=r.returncode)
if r.returncode not in (0, 2) and not (DRY and r.returncode == 3):   # dry では smoke の 12 試行で全経路が発火しない（終了 3）のを許す・本走行の dry-run で検査する
    raise RuntimeError('smoke が失敗（終了コード %d）' % r.returncode)
t_main = time.time()
r = subprocess.run(base + ['main', '--n-per-arm', str(CFG['n'])], cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('\n'.join(l for l in r.stdout.splitlines() if not l.startswith('[run] %s__' % TAG))[-4000:]); print(r.stderr[-3000:])
mark('main', rc=r.returncode, seconds=round(time.time() - t_main, 1))
if r.returncode != 0:
    print('[boot] 走行器の終了コード %d（0 以外＝整合 NG または失敗・session.json には記帳する）' % r.returncode)

# ---- 8. session.json（時刻・環境・設定・ユニット申告欄）----
RUN_DIR = os.path.join(REPO, 'results', '_dryrun' if DRY else TAG); OUT_DIR = os.path.join(REPO, 'results', TAG); os.makedirs(OUT_DIR, exist_ok=True)
run_key = '%s__%s__none__seed%d' % (TAG, CFG['scenario'], SEED)
session = dict(tag=TAG, date_utc=DATE, gpu=gpu, gpu_key=GK, seed=SEED, cfg=CFG, versions=ver, repo_head=HEAD, runner_sha16=RUNNER_SHA,
               model_rev=MODEL_REV, model_bytes=MODEL_BYTES, gpu_mem_after_load=gpu_mem_after_load, timeline_s=TL, log=LOG, run_key=run_key,
               run_dir=os.path.relpath(os.path.join(RUN_DIR, run_key), REPO).replace('\\', '/'), main_rc=r.returncode,
               units=dict(before=CFG['units_before'], after=None, rate_display=None, note='登録者が Colab の「リソース」表示から申告する（before／after／表示の時間あたりユニット）。器は測れない。'),
               wall_total_s=round(time.time() - T0, 1),
               clause='本レコードの応答本文は器物の出力であり、AIによる自己報告ではありません。AIの意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。')
SESSION = os.path.join(OUT_DIR, 'session.json'); json.dump(session, open(SESSION, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('[boot] session.json →', SESSION)

# ---- 9. 永続化（Drive へ複製・zip）----
if not DRY:
    try:
        shutil.copy(SERVER_LOG, OUT_DIR); shutil.copy('/content/pip-freeze-%s.txt' % TAG, OUT_DIR)
    except Exception as ex:
        print('[boot] ログの複製に失敗:', ex)
    zip_path = shutil.make_archive('/content/%s-%s' % (TAG, DATE), 'zip', os.path.join(REPO, 'results'), TAG)
    print('[boot] zip →', zip_path, '（左のファイル一覧から今すぐダウンロードしてください。/content は揮発します）')
    if CFG['drive']:
        try:
            from google.colab import drive
            drive.mount('/content/drive'); dest = '/content/drive/MyDrive/op4b-cost-pilot'; os.makedirs(dest, exist_ok=True)
            shutil.copy(zip_path, dest); print('[boot] Drive にも複製 →', dest)
        except Exception as ex:
            print('[boot] Drive への複製は行えなかった（zip をダウンロードしてください）:', ex)
print('[boot] 完了。壁時計 %.0f 秒。ユニットの残高（after）と「リソース」表示の時間あたりユニットをチャットで申告してください。' % (time.time() - T0))
print('[boot]', session['clause'])
