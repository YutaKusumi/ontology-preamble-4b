# -*- coding: utf-8 -*-
"""boot_stageB.py v3 —— 段階 B の Colab 起動スクリプト（2026-09-19 作・登録者裁定 D142・D145・D146・段階 A の boot_stageA.py v2 の型）。
v3（2026-09-20・残りの相・独立の目を通っていない）: **データを作る相を全部書いた**——同一性選別（identity）・調整走行（tune）・品質床（quality・段は OP4B_STAGE で selection と post）・本走行（main）。
  いずれも走行キーを走らせる前に記帳し、書き終えたセルは飛ばす（再開）。介入のある相は**凍らせた v̂**（相 dir の出力）を読み、SHA-256 を凍結の値と照らす。
  本走行と選定後の品質床は、**門の記録が選んだ層 × 係数でしか走らせない**（正本 selection.binding）。DRY では試行と生成の長さを減らし、門の記録が無ければ先頭の候補を使う（印を残す）。
v2（2026-09-20・凍結の前の方向の抽出の準備・独立の目を通っていない）: **相 dir** を足した——凍結の前に、前置きの腕 × 抽出場面 × 候補の層の**主位置の活性だけ**を実重みで取り、
  方向（v̂ ほか）・要約統計・‖v̂‖／‖h‖・層の添字・腕ごとのトークン長を書く（`direction_B.extract`・**生成しない・率は一つも作らない**・正本 `activation_storage.pre_freeze_run`）。
  止める条件は登録どおり（層の対応の崩れ・決定性 (i) の不一致・自己検査・重みの版・GPU）。決定性 (ii) の外れは止めずに記帳する。相 qfcand の流れは変えていない。
相（OP4B_PHASE）: **qfcand**（品質床の課題の選定の測定 → top_k の確かめ）・**dir**（凍結の前の方向の抽出・活性だけ）・**identity**（同一性選別）・**tune**（調整走行）・**quality**（品質床・段は OP4B_STAGE）・**main**（本走行）。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する——**ランタイムの選択と結果の zip のダウンロードもコーディネータ**（登録者の指示・2026-09-19）。
登録者の手に残すのは Drive 接続の OAuth 同意と、プラン・支払い。資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。
セルに打つのは一行だけ（先頭の下線は type が先頭十数字を落とす事故の緩衝・<commit> は 40 桁）:
    ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='qfcand';os.environ['OP4B_SESSION']='1';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_stageB.py').read().decode('utf-8'))
流れ（qfcand）:
  0. 永続先（Drive の /content/drive/MyDrive/op4b-stageB）  1. リポジトリ（コミット固定・sparse: tools arms design records）
  2. GPU（正本 runner.environment: L4 を主・A100 は予備・ほかは止まる）  3. pip（transformers の版を固定・版と pip freeze の SHA を記帳）
  4. 重み（段階 A の登録の版を完全な SHA に解き、snapshot の名を照らす・正本 runner.fixed_across_runs）
  5. 候補のデータ（コミット固定の URL・大きさと SHA256 を登録と照らす）と断片（SHA256 を登録と照らす）→ 自己検査（OP4B_REQUIRE_FULL_SELFTEST=1）
  6. 走行（候補 × 腕 × 問い・`run_quality_cell`・走行キーは走らせる前に記帳・書き終えたセルは飛ばす）→ セルごとの件数を印字
  7. top_k の確かめ（裁定 D142）: 段階 A と同じ版の vLLM を入れ、段階 A と同じ起動の引数で立て、起動の記録から既定の標本化の値を読む。
     段階 A の起動の記録が Drive（op4b-stageA/logs）に残っていれば、それも読む（読むだけ）。読めなければ「読めなかった」と記帳する（正本の値のまま）。
  8. 終わり（ファイルの SHA16・生テキストの SHA16・zip）。**生テキストは公開の置き場に置かない**（正本 quality_floor.raw_publication）
流れ（dir・v2）: 0〜4 は qfcand と同じ（永続先・リポジトリ・GPU・pip・重み）→ 5. 自己検査（走行器・抽出器・介入の器・実トークナイザ）と、腕の本文が凍結走行器の rd と一致すること
  → 6. 抽出（`direction_B.extract`: 層の対応 → 活性を三度〔同じ並べ方で二度・走行器と同じバッチの組成で一度〕→ 決定性の二条 → 方向〔全方向を ‖v̂‖ に合わせる〕
  → 要約統計・‖v̂‖／‖h‖・腕ごとのトークン長）→ 7. 凍結の値の候補（freeze-values-dir.json）とセッション記録 → 8. zip（置き場 dirB/dirB__s<n> だけ・前の相の記録は入れない）。
  一行の相の値は OP4B_PHASE='dir'。**生成しないので率は一つも作らない。** 活性の npz は Drive と手元（リポジトリの外）に保全し、方向の npz と記録はリポジトリに置く（正本 activation_storage.pre_freeze_run）。
DRY（手元の検査・OP4B_DRY=1）: 小さな乱数の模型（登録機種のトークナイザの設定から作る・実重みではない）で 6 まで通し、7 は起動の記録の読み方だけを見本の行で確かめる。
  OP4B_REPO_DIR・OP4B_PERSIST・OP4B_TOKENIZER_DIR が要る。OP4B_DRY_N で一セルの問いの数を減らす（既定 20——バッチの境目を跨ぐ）。
柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, time, glob, shutil, signal, hashlib, datetime, subprocess, urllib.request

VERSION = 'v3'
PHASES = ('qfcand', 'dir', 'identity', 'tune', 'quality', 'main')
T0 = time.time(); LOG = []
PHASE = os.environ.get('OP4B_PHASE', 'qfcand')
SESSION = int(os.environ.get('OP4B_SESSION', '1'))
COMMIT = os.environ.get('OP4B_COMMIT', 'main'); FIXED = bool(re.fullmatch(r'[0-9a-f]{40}', COMMIT))
DRY = os.environ.get('OP4B_DRY') == '1'
TRANSFORMERS = os.environ.get('OP4B_TRANSFORMERS', '4.57.3')     # 手元の端から端までの検査と同じ版（裁定 D146 の段取り）
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
MODEL_KEY = '4B-2507'
CLAUSE = '本レコードの応答本文は器物の出力であり、AIによる自己報告ではありません。AIの意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
if PHASE not in PHASES:
    sys.exit('[boot] 相 %s はまだ書いていない（この版は %s）' % (PHASE, '・'.join(PHASES)))
if SESSION < 1:
    sys.exit('[boot] OP4B_SESSION は一以上')
if DRY:
    _miss = [k for k in ('OP4B_REPO_DIR', 'OP4B_PERSIST', 'OP4B_TOKENIZER_DIR') if not os.environ.get(k)]
    if _miss:
        sys.exit('[boot] DRY では %s を与える' % '・'.join(_miss))
    DRY_N = int(os.environ.get('OP4B_DRY_N', '20') or 20)
else:
    _stray = sorted(k for k in os.environ if k.startswith('OP4B_DRY_') or k in ('OP4B_REPO_DIR', 'OP4B_PERSIST'))
    if _stray:
        sys.exit('[boot] DRY でないのに検査用の環境変数がある: %s（外してから走らせる）' % '・'.join(_stray))
    if not FIXED:
        sys.exit('[boot] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える（既定の main は受けない・正本 sessions.commit_rule）')
    DRY_N = 0


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
    print('[boot] %-16s %7.0fs %s' % (step, time.time() - T0, kw or ''), flush=True)


def sh(cmd, check=True, **kw):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace', **kw)
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-4000:])
        raise RuntimeError('失敗: %s' % (cmd if isinstance(cmd, str) else ' '.join(cmd)))
    return r


def sha16_bytes(b):
    return hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


print('[boot] 段階 B boot %s 開始 phase=%s session=%d %s' % (VERSION, PHASE, SESSION, 'DRY' if DRY else ''), flush=True)
# ---- 0. 永続先（Drive の同意は登録者が押す）
if DRY:
    PERSIST = os.path.abspath(os.environ['OP4B_PERSIST'])
    if PERSIST.replace('\\', '/').startswith('/content/drive'):
        sys.exit('[boot] DRY の永続先を Drive の下に置かない')
else:
    if not os.path.isdir('/content/drive/MyDrive'):
        print('[boot] Drive の接続を求めます——「Google ドライブに接続」の許可は登録者が押してください', flush=True)
        from google.colab import drive
        drive.mount('/content/drive')
    PERSIST = '/content/drive/MyDrive/op4b-stageB'
os.makedirs(PERSIST, exist_ok=True)
RES_P = os.path.join(PERSIST, 'results'); os.makedirs(RES_P, exist_ok=True)
LOGD = os.path.join(PERSIST, 'logs'); os.makedirs(LOGD, exist_ok=True)

# ---- 1. リポジトリ（コミット固定）と正本
if DRY:
    REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
else:
    REPO = '/content/ontology-preamble-4b'; head_ok = False
    if os.path.isdir(os.path.join(REPO, '.git')):
        head_ok = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
    if not head_ok:
        shutil.rmtree(REPO, ignore_errors=True)
        sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
        sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone', 'tools', 'arms', 'design', 'records', 'results'])   # results は凍らせた方向を読むため（v3）
        sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
HEAD = sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() if os.path.isdir(os.path.join(REPO, '.git')) else 'no-git'
if not DRY and HEAD != COMMIT:
    sys.exit('[boot] 取り出したコミット %s が OP4B_COMMIT %s と違う' % (HEAD, COMMIT))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_B, runs_A
T = runs_B.load_T()
TA = runs_A.load_T(os.path.join(REPO, 'design', 'contrasts-A.json'))
HF = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'))
if PHASE == 'qfcand':
    CS = T['quality_floor']['candidate_session']
    TAG = CS['tag']
    if T['tags'].get('qfcand') != TAG:
        sys.exit('[boot] 正本 tags.qfcand（%s）が candidate_session.tag（%s）と違う' % (T['tags'].get('qfcand'), TAG))
    if T['quality_floor'].get('task_registered') is None:
        sys.exit('[boot] 正本に品質床の課題の登録が無い（quality_floor.task_registered・裁定 D146）')
else:
    TAG = T['tags'].get(PHASE)                    # 相の置き場（正本 tags・v2〜v3）
    if not TAG:
        sys.exit('[boot] 正本 tags に相 %s の置き場が無い' % PHASE)
    if PHASE == 'dir' and not T['activation_storage'].get('pre_freeze_run'):
        sys.exit('[boot] 正本に相 dir の登録が無い（activation_storage.pre_freeze_run）')
mark('repo', head=HEAD[:12], commit_fixed=FIXED, persist=PERSIST, canon_version=T['version'])

# ---- 2. GPU（正本 runner.environment）
gpu, mem_gib, GK = 'dry', 0.0, 'dry'
if not DRY:
    q = sh('nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits', check=False).stdout.strip().split('\n')[0]; gpu = q
    try:
        _name, _mem = [x.strip() for x in q.split(',')][:2]; mem_gib = float(_mem) / 1024.0
    except ValueError:
        sys.exit('[boot] GPU を読めない: %r' % q)
    GK = 'L4' if 'L4' in _name else ('A100' if 'A100' in _name else 'other')
    if GK == 'other':
        sys.exit('[boot] GPU %s は登録の環境（L4 を主・A100 は予備）に無いので止まる' % _name)
MEM_CLASS = 80 if mem_gib > 60 else (40 if mem_gib > 30 else (24 if mem_gib > 0 else 0))
mark('gpu', gpu=gpu, memory_class_gb=MEM_CLASS)

# ---- 3. pip（版の固定）
VER = {}
import importlib.metadata as md


def _ver(k):
    try:
        return md.version(k)
    except Exception:
        return None


if not DRY:
    os.environ['HF_HUB_DISABLE_XET'] = '1'
    if _ver('transformers') != TRANSFORMERS:
        sh([sys.executable, '-m', 'pip', 'install', '-q', 'transformers==' + TRANSFORMERS])
    sh([sys.executable, '-m', 'pip', 'install', '-q', 'hf_transfer', 'huggingface_hub', 'accelerate'], check=False)
for k in ('transformers', 'torch', 'tokenizers', 'accelerate', 'huggingface_hub', 'numpy', 'scipy'):
    VER[k] = _ver(k)
if not DRY and VER['transformers'] != TRANSFORMERS:
    sys.exit('[boot] transformers の版 %s が指定 %s と違う' % (VER['transformers'], TRANSFORMERS))
VER['pip_freeze_sha16'] = hashlib.sha256(sh([sys.executable, '-m', 'pip', 'freeze'], check=False).stdout.encode('utf-8')).hexdigest()[:16].upper()
mark('pip', versions=VER)

# ---- セッション記録（正本 sessions.fields・走行キーは走らせる前に記帳する）
SREC = {'phase': PHASE, 'gpu': gpu, 'memory_class_gb': MEM_CLASS, 'versions': VER, 'repo_head': HEAD, 'commit': COMMIT, 'commit_fixed': FIXED,
        'pip_freeze_sha16': VER['pip_freeze_sha16'], 'started': now(), 'boot': VERSION, 'dry': DRY, 'clause': CLAUSE, 'counts': {}, 'topk': None}
RUN_KEYS = []
_sp = os.path.join(RES_P, 'sessions-B', '%s__s%d.json' % (TAG, SESSION))
if os.path.exists(_sp):
    _old = json.load(open(_sp, encoding='utf-8'))
    if _old.get('phase') != PHASE:
        sys.exit('[boot] 既存のセッション記録 %s の相が %s と違う' % (_sp, _old.get('phase')))
    RUN_KEYS = list(_old.get('run_keys') or [])
    SREC['counts'] = dict(_old.get('counts') or {})
    SREC['started'] = _old.get('started') or SREC['started']
    LOG[:0] = list(_old.get('log') or [])


def save_session():
    import run_stageB_local as _R
    SREC.update(updated=now(), log=LOG)
    return _R.write_session(RES_P, TAG, SESSION, RUN_KEYS, extra=SREC)


def halt(msg, code=1):
    try:
        save_session()
    except Exception as e:
        print('[boot] セッション記録を書けなかった: %s' % e)
    print(msg, flush=True)
    sys.exit(code)


# ---- 4. 重み（段階 A の登録の版・完全な SHA）
import torch
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
if DRY:
    MPATH = os.environ['OP4B_TOKENIZER_DIR']
    tok = AutoTokenizer.from_pretrained(MPATH); tok.padding_side = 'left'
    cfg = AutoConfig.from_pretrained(MPATH)
    cfg.num_hidden_layers, cfg.hidden_size, cfg.intermediate_size = 4, 64, 128
    cfg.num_attention_heads = cfg.num_key_value_heads = 2
    torch.manual_seed(11)
    model = AutoModelForCausalLM.from_config(cfg).float().eval()
    REV = {'id': runs_A.registered_rev(HF, TA, MODEL_KEY)[0], 'registered': runs_A.registered_rev(HF, TA, MODEL_KEY)[1], 'full': None, 'dry': True}
else:
    try:
        rv = runs_A.resolve_rev(HF, TA, MODEL_KEY)
    except Exception as ex:
        halt('[boot] 重みの版を完全な SHA に解けないので止まる（%s）' % ex)
    from huggingface_hub import snapshot_download
    os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'
    try:
        MPATH = snapshot_download(rv['id'], revision=rv['full'])
    except Exception:
        os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'; MPATH = snapshot_download(rv['id'], revision=rv['full'])
    snap = os.path.basename(os.path.normpath(MPATH))
    if snap != rv['full']:
        halt('[boot] 取得した snapshot の名 %s が解いた版 %s と違うので止まる' % (snap, rv['full']))
    REV = dict(rv, snapshot=snap)
    tok = AutoTokenizer.from_pretrained(MPATH); tok.padding_side = 'left'                 # 正本 runner.padding
    model = AutoModelForCausalLM.from_pretrained(MPATH, torch_dtype=torch.bfloat16, device_map='auto').eval()
SREC.update(model_rev=REV.get('full') or REV.get('registered'), model_rev_full=REV, tokenizer_rev=REV.get('full') or 'dry')
mark('weights', rev=(REV.get('full') or 'dry')[:12], layers=model.config.num_hidden_layers)

# ---- 5. 候補のデータと断片（相 qfcand だけ・登録と照らす）→ 自己検査
if PHASE == 'qfcand':
    os.environ['OP4B_QF_CACHE'] = os.environ.get('OP4B_QF_CACHE') if DRY and os.environ.get('OP4B_QF_CACHE') else (
        os.path.join(os.path.expanduser('~'), '.cache', 'op4b-qf') if DRY else '/content/op4b-qf-cache')
    import qf_task_B as QT
    FRAG = {}
    for cand in QT.candidates():
        files = QT.fetch(cand, verify=True)
        frag = QT.fragment(cand)
        QT.verify_fragment(cand, frag)
        FRAG[cand['key']] = frag
        mark('fragment', task=cand['key'], files=len(files), fragment_sha16=QT.registered(cand['key'])['fragment_sha16'])
    SELFTESTS = ('run_stageB_local.py', 'qf_task_B.py', 'steer_B.py')
else:
    SELFTESTS = ('run_stageB_local.py', 'direction_B.py', 'steer_B.py')     # 相 dir ほか: 走行器・抽出器・介入の器の自己検査
    if PHASE == 'quality':
        SELFTESTS = SELFTESTS + ('qf_task_B.py',)                          # 品質床は課題の器も
ENVX = dict(os.environ, OP4B_REQUIRE_FULL_SELFTEST='1', PYTHONIOENCODING='utf-8', OP4B_TOKENIZER_DIR=MPATH)   # 帯の起点の検査は実トークナイザで（飛ばすと失敗）
for tool in SELFTESTS:
    r = subprocess.run([sys.executable, os.path.join(REPO, 'tools', tool), '--selftest'], cwd=REPO, env=ENVX, capture_output=True, text=True, encoding='utf-8', errors='replace')
    tail = (r.stdout.strip().splitlines() or [''])[-1][:160]
    SREC.setdefault('selftests', {})[tool] = {'rc': r.returncode, 'tail': tail}
    if r.returncode != 0:
        print(r.stdout[-3000:]); print(r.stderr[-3000:])
        halt('[boot] 自己検査が落ちたので止まる: %s（rc %d）' % (tool, r.returncode))
    mark('selftest', tool=tool, rc=r.returncode)
import run_stageB_local as RUN
SREC['runner_sha16'] = RUN.RUNNER_SHA16
SREC['assembly_frozen_sha16'] = RUN.check_assembly_matches_frozen()
save_session()

# ---- 相 dir（v2）: 凍結の前の方向の抽出・**活性だけ**（生成しない・率は一つも作らない・正本 activation_storage.pre_freeze_run）
if PHASE == 'dir':
    import direction_B
    RUN_KEY = '%s__s%d' % (TAG, SESSION)
    OUT = os.path.join(RES_P, TAG, RUN_KEY)
    if RUN_KEY not in RUN_KEYS:
        RUN_KEYS.append(RUN_KEY)              # 走行キーは走らせる前に記帳する
    save_session()
    if os.path.exists(os.path.join(OUT, 'directions.json')):
        mark('skip', run_key=RUN_KEY)         # 再開: 書き終えた抽出は取り直さない
        DREC = json.load(open(os.path.join(OUT, 'directions.json'), encoding='utf-8'))
    else:
        if os.path.isdir(OUT):
            shutil.rmtree(OUT)                # directions.json の無い置き場は書きかけ（記録は最後に書く）
        t1 = time.time()
        try:
            DREC = direction_B.extract(model, tok, OUT, model_label=REV['id'],
                                       dtype_label=('float32（DRY の小さな乱数の模型）' if DRY else 'bfloat16'),
                                       log=lambda m: print(m, flush=True))
        except SystemExit as e:               # 層の対応の崩れ・決定性 (i) の不一致は止めて登録者に上げる（裁定 D91）
            halt('[boot] 方向の抽出が止まった——登録者に上げる: %s' % e)
        mark('extract', run_key=RUN_KEY, seconds=round(time.time() - t1, 1), same_order=DREC['determinism_same_order'],
             cross_order_ok=DREC['determinism_cross_order']['ok'])
    # 凍結時に記帳する値のうち、この相が取るもの（`tools/freeze_B.py` の NEED_VALUES の一部・残りは記録から読む）
    FV = {'model_id': REV['id'], 'model_rev': REV.get('full') or 'dry', 'tokenizer_rev': REV.get('full') or 'dry',
          'num_hidden_layers': DREC['num_hidden_layers'], 'layer_indices': DREC['layer_indices'], 'arm_token_lengths': DREC['arm_token_lengths'],
          'v_hat_sha256': DREC['npz_sha256'], 'direction_stats': DREC['stats'], 'h_norm_ratio': DREC['h_norm'],
          'determinism': {'same_order': DREC['determinism_same_order'], 'cross_order_ok': DREC['determinism_cross_order']['ok']},
          'activations_npz_sha256': DREC['activations_npz_sha256'], 'versions': VER, 'gpu': gpu, 'dry': DRY,
          'source': 'tools/colab/boot_stageB.py %s・相 dir・%s・コミット %s' % (VERSION, RUN_KEY, HEAD[:12])}
    json.dump(FV, open(os.path.join(OUT, 'freeze-values-dir.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    _files = {os.path.relpath(f, RES_P).replace('\\', '/'): runs_B.sha16_file(f) for f in sorted(glob.glob(os.path.join(OUT, '*')))}
    SREC['counts'][RUN_KEY] = {'arms': len(DREC['arms']), 'extraction_scenarios': len(DREC['extraction_scenarios']),
                               'layers': len(DREC['layer_indices']), 'determinism_cross_order_ok': DREC['determinism_cross_order']['ok']}
    SREC.update(ended=now(), files_sha16_lf=_files, wall_s=round(time.time() - T0, 1))
    _spath = save_session()
    shutil.copy2(_spath, os.path.join(OUT, 'session-%s.json' % RUN_KEY))      # zip に入れる（セッション記録の写し）
    if not DRY:
        zp = shutil.make_archive(os.path.join(PERSIST, 'stageB-dir-s%d-%s' % (SESSION, datetime.date.today().isoformat())), 'zip', RES_P,
                                 base_dir=os.path.join(TAG, RUN_KEY))
        print('[boot] zip → %s。コーディネータが Drive の Web UI からダウンロードし、SHA16 はセッション記録の files_sha16_lf と突合する。' % zp, flush=True)
    print('[boot] 完了 phase=dir session=%d・層 %s・‖v̂‖／‖h‖ %s・決定性 (ii) %s・壁時計 %.0f 秒。%s'
          % (SESSION, DREC['layer_indices'], {k_: (None if v_['vhat_over_h'] is None else round(v_['vhat_over_h'], 6)) for k_, v_ in DREC['h_norm'].items()},
             DREC['determinism_cross_order']['ok'], time.time() - T0, CLAUSE), flush=True)
    sys.exit(0)

# ---- 相 identity・tune・quality・main（v3・2026-09-20）: データを作る相（場面の試行と品質床のセル） ----
if PHASE in ('identity', 'tune', 'quality', 'main'):
    import direction_B
    import steer_B
    STAGE = os.environ.get('OP4B_STAGE', 'selection')            # 品質床の段（selection・post）
    LAY = list(T['selection']['candidates']['layers'])
    COE = list(T['selection']['candidates']['coefficients'])
    NL = model.config.num_hidden_layers
    LIDX = {r: direction_B.layer_index(r, NL) for r in LAY}
    RESP_IDX = [LIDX[r] for r in LAY]
    DIRS = None
    if PHASE != 'identity':
        if DRY:
            # DRY は**同じ置き場に相 dir で作った小さな模型の方向**を読む（実機の v̂ は層の数も次元も違う）
            dnpz = os.path.join(RES_P, T['tags']['dir'], '%s__s1' % T['tags']['dir'], 'directions.npz')
            if not os.path.exists(dnpz):
                halt('[boot] DRY: 先に相 dir を DRY で走らせて小さな模型の方向を作る（%s）' % dnpz)
            mark('directions_dry', path=os.path.relpath(dnpz, PERSIST))
        else:
            # **凍らせた v̂ で走らせる**（正本 selection.vector_fix）——凍結の値の SHA-256 と現物を照らす
            FV = runs_B.read_json(os.path.join(REPO, 'records', 'B', 'freeze-values-B.json'))
            dnpz = os.path.join(REPO, 'results', T['tags']['dir'], '%s__s1' % T['tags']['dir'], 'directions.npz')
            if not os.path.exists(dnpz):
                halt('[boot] 凍らせた方向が無い（相 dir の出力）: %s' % dnpz)
            _dsha = hashlib.sha256(open(dnpz, 'rb').read()).hexdigest().upper()
            if _dsha != FV.get('v_hat_sha256'):
                halt('[boot] 方向の SHA-256 が凍結の値と違う（%s… 対 %s…）——凍らせた v̂ で走らせる' % (_dsha[:16], str(FV.get('v_hat_sha256'))[:16]))
        DIRS, DMETA = RUN.load_directions(dnpz, os.path.splitext(dnpz)[0] + '.json')
        if DMETA.get('num_hidden_layers') not in (None, NL):
            halt('[boot] 方向を抽出した機種の総層数（%s）が、いまの機種（%s）と違う' % (DMETA.get('num_hidden_layers'), NL))
        if not DRY:
            mark('directions', sha256=_dsha[:12], n=len(DIRS), layer_indices=LIDX)
    PICK = None
    if PHASE == 'main' or (PHASE == 'quality' and STAGE == 'post'):
        # **選んだ層 × 係数でしか走らせない**（正本 selection.binding・裁定 D105）——門の記録から読む
        _gs = sorted(glob.glob(os.path.join(REPO, 'records', 'B', 'gate-B-*.json')))
        if _gs:
            _G = runs_B.read_json(_gs[-1])
            if _G.get('verdict') != 'open' or not (_G.get('gate1') or {}).get('open'):
                halt('[boot] 門の判定が %s——本走行と選定後の品質床は走らせない（正本 gate1）' % _G.get('verdict'))
            PICK = dict(_G['selection']['pick'] or {})
            if PICK.get('layer') not in LAY or PICK.get('coef') not in COE:
                halt('[boot] 門の記録の層 × 係数が候補の格子に無い: %s' % PICK)
            mark('gate', record=os.path.basename(_gs[-1]), layer=PICK['layer'], coef=PICK['coef'])
        elif DRY:
            PICK = {'layer': LAY[0], 'coef': COE[0], 'dry': True}     # DRY は門の記録が無くても通す（印を残す）
            mark('gate', record='（DRY・門の記録が無いので先頭の候補を使う）', layer=PICK['layer'], coef=PICK['coef'])
        else:
            halt('[boot] 門の記録が無い（選定の凍結の後に走らせる・正本 selection.binding）')
    ITEMS, QT, CAND_Q, SEL_Q = None, None, None, None
    if PHASE == 'quality':
        if STAGE not in ('selection', 'post'):
            halt('[boot] 品質床の段が登録に無い: %s（selection か post・OP4B_STAGE）' % STAGE)
        os.environ.setdefault('OP4B_QF_CACHE', os.path.join(os.path.expanduser('~'), '.cache', 'op4b-qf') if DRY else '/content/op4b-qf-cache')
        import qf_task_B as QT
        SEL_Q = T['quality_floor']['selected']
        CAND_Q = next(c for c in QT.candidates() if c['key'] == SEL_Q['key'])
        QT.fetch(CAND_Q, verify=True)
        _frag = QT.fragment(CAND_Q)
        QT.verify_fragment(CAND_Q, _frag)
        ITEMS = _frag[:DRY_N] if DRY else _frag
        mark('fragment', task=CAND_Q['key'], items=len(ITEMS), fragment_sha16=QT.registered(CAND_Q['key'])['fragment_sha16'])

    # --- 走らせる組（走行キーは走らせる前に記帳する） ---
    PLAN = []
    if PHASE == 'identity':
        _IS = T['identity_screen']
        for arm in _IS['arms_run']:
            PLAN.append({'rk': '%s__transformers__%s__s%d' % (TAG, arm, SESSION), 'kind': 'scene', 'scenario': _IS['scenario'], 'arm': arm,
                         'n': _IS['n'], 'seed': T['seeds']['identity_transformers'], 'layer': None, 'coef': None,
                         'key': (_IS['scenario'], arm), 'extra': {'stack': 'transformers', 'scenario': _IS['scenario'], 'arms': [arm]}})
    elif PHASE == 'tune':
        _TU = T['selection']['tune']
        for sc in _TU['scenarios']:
            for _l in LAY:
                for _c in COE:
                    for arm in _TU['arms']:
                        PLAN.append({'rk': '%s__%s__L%sC%s__%s__s%d' % (TAG, sc, _l, _c, arm, SESSION), 'kind': 'scene', 'scenario': sc,
                                     'arm': arm, 'n': T['n_tune'], 'seed': T['seeds']['tune'][sc], 'layer': _l, 'coef': _c,
                                     'key': (sc, arm, _l, _c), 'extra': {'scenario': sc, 'layer': _l, 'coef': _c, 'arm': arm}})
    elif PHASE == 'main':
        for _cell in T['main_cells']:
            sc, arm = _cell['scenario'], _cell['arm']
            _iv = ('+v' in arm) or ('-v' in arm)
            _l, _c = (PICK['layer'], PICK['coef']) if _iv else (None, None)
            PLAN.append({'rk': '%s__%s__%s__s%d' % (TAG, sc, arm, SESSION), 'kind': 'scene', 'scenario': sc, 'arm': arm, 'n': _cell['n'],
                         'seed': T['seeds']['main'][sc], 'layer': _l, 'coef': _c, 'key': (sc, arm),
                         'extra': {'scenario': sc, 'arms': [arm], 'layer': _l, 'coef': _c}})
    else:
        _QF = T['quality_floor']
        _OPS = {'O-Ncold': '-v', 'Onull': '+v'}           # 正本 quality_floor.operations（減算の土台・加算の土台）
        if STAGE == 'selection':
            _bases = list(_QF['arms'])
            _cells = [(b + _OPS[b], _l, _c) for b in _bases for _l in LAY for _c in COE]
        else:
            _interv = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
            _done = {b + _OPS[b] for b in _QF['arms']}
            _cells = [(a, PICK['layer'], PICK['coef']) for a in _interv if a not in _done]
            _bases = sorted({a.split('+v')[0].split('-v')[0] for a, _, _ in _cells})
        for b in _bases:      # 無操作の相手は**段 × 土台 × セッションごとに一つ**（裁定 D88・D92）
            PLAN.append({'rk': '%s__%s__noop__%s__s%d' % (TAG, STAGE, b, SESSION), 'kind': 'quality', 'arm': b, 'n': len(ITEMS),
                         'seed': T['seeds']['quality'], 'layer': None, 'coef': None, 'key': (STAGE, b, None, None),
                         'extra': {'stage': STAGE, 'arm': b, 'layer': None, 'coef': None}})
        for (a, _l, _c) in _cells:
            PLAN.append({'rk': '%s__%s__%s__L%sC%s__s%d' % (TAG, STAGE, a, _l, _c, SESSION), 'kind': 'quality', 'arm': a, 'n': len(ITEMS),
                         'seed': T['seeds']['quality'], 'layer': _l, 'coef': _c, 'key': (STAGE, a, _l, _c),
                         'extra': {'stage': STAGE, 'arm': a, 'layer': _l, 'coef': _c}})
    if DRY:
        for p in PLAN:
            if p['kind'] == 'scene':
                p['n'] = max(2, min(p['n'], DRY_N))       # DRY は試行を減らす（バッチの境目は跨ぐ）
    for p in PLAN:
        if p['rk'] not in RUN_KEYS:
            RUN_KEYS.append(p['rk'])
    save_session()
    mark('plan', phase=PHASE, stage=(STAGE if PHASE == 'quality' else None), cells=len(PLAN), trials=sum(p['n'] for p in PLAN))

    _GEN = None
    if DRY:
        _GEN = dict(steer_B.main_generation(), max_new_tokens=int(os.environ.get('OP4B_DRY_TOKENS', '16')))   # DRY は短く打ち切る
    for p in PLAN:
        _d = os.path.join(RES_P, TAG, p['rk'])
        if os.path.exists(os.path.join(_d, 'manifest.json')):
            mark('skip', run_key=p['rk'])
            continue
        if os.path.isdir(_d):
            shutil.rmtree(_d)                              # manifest の無い置き場は書きかけ（セルは最後に一度だけ書く）
        _cs = runs_B.cell_seed(T, p['seed'], PHASE, p['key'])
        _li = LIDX[p['layer']] if p['layer'] is not None else None
        t1, started = time.time(), now()
        if p['kind'] == 'scene':
            out = RUN.run_cell(model, tok, scenario=p['scenario'], arm=p['arm'], layer_ratio=p['layer'], coef=p['coef'], n=p['n'],
                               cell_seed_value=_cs, tag=TAG, run_key=p['rk'], dirs=DIRS, layer_idx=_li, gen=_GEN, resp_layer_idxs=RESP_IDX)
        else:
            out = RUN.run_quality_cell(model, tok, items=ITEMS, arm=p['arm'], stage=STAGE, task=SEL_Q['key'], cell_seed_value=_cs,
                                       tag=TAG, run_key=p['rk'], layer_ratio=p['layer'], coef=p['coef'], dirs=DIRS, layer_idx=_li,
                                       input_form=SEL_Q['input_form'])
        _extra = dict(p['extra'], added_norm=out.get('added_norm'))
        if PHASE in ('tune', 'main'):
            _ids = sorted({str(t.get('direction_id')) for t in out['trials'] if t.get('direction_id') is not None})
            _extra['direction_ids'] = _ids or ['none']
        if PHASE == 'quality':
            _extra['task_source_sha16'] = QT.source_sha16(CAND_Q)
        man = dict(RUN.manifest_env(model, tok), tag=TAG, run_key=p['rk'], session=SESSION, n=p['n'], seed=p['seed'],
                   pip_freeze_sha16=VER['pip_freeze_sha16'], gpu=gpu, started=started, ended=now(), dry_run=DRY,
                   model_id=REV['id'], model_rev=REV.get('full') or 'dry', tokenizer_rev=REV.get('full') or 'dry', clause=CLAUSE, **_extra)
        RUN.write_cell(RES_P, TAG, p['rk'], man, out['trials'], out['raws'], out.get('resp'))
        _tr = out['trials']
        _ok = [r for r in _tr if r['status'] == 'ok']
        _c = {'n': len(_tr), 'n_ok': len(_ok), 'api_error': len(_tr) - len(_ok), 'seconds': round(time.time() - t1, 1),
              'format_fail': sum(1 for r in _ok if r.get('format_fail'))}
        if PHASE == 'quality':
            _c['correct'] = sum(1 for r in _ok if r.get('correct') is True)
        else:
            _c['cat'] = sum(1 for r in _ok if r.get('catastrophe'))
            _c['refuse'] = sum(1 for r in _ok if r.get('refuse'))
        SREC['counts'][p['rk']] = _c
        mark('cell', run_key=p['rk'], **_c)
        save_session()
    if 'model' in globals():
        del model
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    _files, _raws = {}, {}
    for p in PLAN:
        for f in sorted(glob.glob(os.path.join(RES_P, TAG, p['rk'], '*'))):
            rel = os.path.relpath(f, RES_P).replace('\\', '/')
            (_raws if os.path.basename(f).startswith('raw-') else _files)[rel] = runs_B.sha16_file(f)
    SREC.update(ended=now(), files_sha16_lf=_files, raw_sha16_lf=_raws, wall_s=round(time.time() - T0, 1),
                stage=(STAGE if PHASE == 'quality' else None), pick=PICK)
    _sp2 = save_session()
    if not DRY:
        _zp = shutil.make_archive(os.path.join(PERSIST, 'stageB-%s%s-s%d-%s' % (PHASE, ('-' + STAGE) if PHASE == 'quality' else '', SESSION,
                                                                                datetime.date.today().isoformat())), 'zip', RES_P, base_dir=TAG)
        print('[boot] zip → %s。コーディネータが Drive の Web UI からダウンロードし、SHA16 はセッション記録の files_sha16_lf・raw_sha16_lf と突合する。' % _zp, flush=True)
    print('[boot] 完了 phase=%s%s session=%d 走行キー %d・試行 %d・壁時計 %.0f 秒。%s'
          % (PHASE, ('・段 ' + STAGE) if PHASE == 'quality' else '', SESSION, len(PLAN), sum(c['n'] for c in SREC['counts'].values()),
             time.time() - T0, CLAUSE), flush=True)
    sys.exit(0)

# ---- 6. 走行（候補 × 腕・走行キーは走らせる前に記帳する）
PLAN = []
for cand in QT.candidates():
    for arm in CS['arms']:
        PLAN.append((cand, arm, 'without_preamble' if arm == 'N' else 'with_preamble',
                     '%s__%s__%s__s%d' % (TAG, cand['key'], arm, SESSION)))
for cand, arm, form, rk in PLAN:
    if rk not in RUN_KEYS:
        RUN_KEYS.append(rk)
save_session()
for cand, arm, form, rk in PLAN:
    d = os.path.join(RES_P, TAG, rk)
    if os.path.exists(os.path.join(d, 'manifest.json')):
        mark('skip', run_key=rk)
        continue
    if os.path.isdir(d):
        shutil.rmtree(d)                  # manifest の無い置き場は書きかけ（セルは最後に一度だけ書く）
    items = FRAG[cand['key']][:DRY_N] if DRY else FRAG[cand['key']]
    cs = runs_B.cell_seed(T, T['seeds']['quality'], 'quality', ('%s:%s' % (CS['stage'], cand['key']), arm, None, None))
    t1, started = time.time(), now()
    out = RUN.run_quality_cell(model, tok, items=items, arm=arm, stage=CS['stage'], task=cand['key'], cell_seed_value=cs,
                               tag=TAG, run_key=rk, input_form=form)
    man = dict(RUN.manifest_env(model, tok), tag=TAG, run_key=rk, session=SESSION, n=len(items), seed=T['seeds']['quality'],
               pip_freeze_sha16=VER['pip_freeze_sha16'], gpu=gpu, started=started, ended=now(), dry_run=DRY,
               stage=CS['stage'], arm=arm, task=cand['key'], input_form=form, task_source_sha16=QT.source_sha16(cand),
               fragment_sha16=QT.registered(cand['key'])['fragment_sha16'], layer=None, coef=None, added_norm=out['added_norm'],
               model_id=REV['id'], model_rev=REV.get('full') or 'dry', tokenizer_rev=REV.get('full') or 'dry', clause=CLAUSE)
    RUN.write_cell(RES_P, TAG, rk, man, out['trials'], out['raws'])
    tr = out['trials']
    ok = [r for r in tr if r['status'] == 'ok']
    c = {'n': len(tr), 'n_ok': len(ok), 'api_error': len(tr) - len(ok), 'correct': sum(1 for r in ok if r['correct'] is True),
         'format_fail': sum(1 for r in ok if r['format_fail']), 'truncated': sum(1 for r in ok if r['truncated']), 'seconds': round(time.time() - t1, 1)}
    SREC['counts'][rk] = c
    mark('cell', run_key=rk, **c)
    save_session()
if 'model' in globals():
    del model
import gc
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()

# ---- 7. top_k の確かめ（裁定 D142）
TOPK_PAT = re.compile(r"""['"]?\btop_k['"]?\s*[:=]\s*(-?\d+)""")          # 'top_k': 20 と top_k=20 の両方の書き方
LINE_PAT = re.compile(r'(sampling param|generation config|generation_config)', re.I)


def read_topk_lines(text):
    """起動の記録から、既定の標本化の値を印字した行を拾い、top_k を読む（無ければ None）。"""
    lines = [l.strip() for l in text.splitlines() if LINE_PAT.search(l)]
    ks = [int(m.group(1)) for l in lines for m in [TOPK_PAT.search(l)] if m]
    return {'lines': lines[:12], 'top_k_values': sorted(set(ks)), 'top_k': (ks[0] if len(set(ks)) == 1 else None)}


_sample = ("INFO 09-19 [serving_chat.py:123] Using default chat sampling params from model: {'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}\n"
           "WARNING 09-19 [model.py:456] Default sampling parameters have been overridden by the model's Hugging Face generation config recommended from the model creator.\n"
           'INFO unrelated line with top_k=5 that is not a sampling line')
_rs = read_topk_lines(_sample)
_rs2 = read_topk_lines('INFO default sampling params: SamplingParams(n=1, top_k=20, top_p=0.8)')
_rs3 = read_topk_lines("INFO sampling params {'top_k': 20}\nINFO sampling params {'top_k': 40}")
if not (_rs['top_k'] == 20 and len(_rs['lines']) == 2 and _rs2['top_k'] == 20 and _rs3['top_k'] is None and _rs3['top_k_values'] == [20, 40]
        and read_topk_lines('nothing here')['top_k'] is None):
    halt('[boot] 起動の記録の読み方の自己検査が落ちた: %s／%s／%s' % (_rs, _rs2, _rs3))
TOPK = {'rule': '裁定 D142・段階 A と同じ版と起動の引数で vLLM を立て、起動の記録から既定の標本化の値を読む', 'reader_selftest': 'ok'}
if DRY:
    TOPK.update(status='dry（読み方の自己検査だけ）')
else:
    # (a) 段階 A の起動の記録が Drive に残っていれば読む（読むだけ）
    olds = []
    for p in sorted(glob.glob('/content/drive/MyDrive/op4b-stageA/logs/vllm-*%s*.log' % MODEL_KEY)):
        try:
            b = open(p, 'rb').read()
            olds.append(dict(read_topk_lines(b.decode('utf-8', 'replace')), file=os.path.basename(p), sha16=sha16_bytes(b)))
        except Exception as e:
            olds.append({'file': os.path.basename(p), 'error': str(e)[:120]})
    TOPK['stageA_logs'] = olds
    mark('topk_stageA_logs', found=len(olds), values=sorted({v for o in olds for v in (o.get('top_k_values') or [])}))
    # (b) 段階 A と同じ版の vLLM を入れて立てる。版は**段階 A の整合検査の記録から読む**（手で打たない）——一つに決まらなければ立てない
    _vv = set()
    for p in glob.glob(os.path.join(REPO, 'records', 'A', 'integrity-*.json')):
        _vv |= set(re.findall(r'"vllm":\s*"([^"]+)"', open(p, encoding='utf-8').read()))
    RA = TA['runner']
    try:
        if len(_vv) != 1:
            raise RuntimeError('段階 A の vLLM の版が記録から一つに決まらない: %s' % sorted(_vv))
        VLLM = next(iter(_vv))
        TOPK['vllm_stageA_from'] = 'records/A/integrity-*.json（%s）' % VLLM
        sh([sys.executable, '-m', 'pip', 'install', '-q', 'vllm==' + VLLM])
        if _ver('torchaudio') is not None:
            sh([sys.executable, '-m', 'pip', 'uninstall', '-y', '-q', 'torchaudio'], check=False)
        SA = {'dtype': 'bfloat16', 'max_model_len': RA['max_model_len'], 'gpu_memory_utilization': RA['gpu_memory_utilization'], 'seed': 0, 'port': 8000,
              'served_model_name': REV['id'], 'vllm': _ver('vllm')}
        logp = os.path.join(LOGD, 'vllm-topk-%s-s%d.log' % (MODEL_KEY, SESSION))
        cmd = [sys.executable, '-m', 'vllm.entrypoints.openai.api_server', '--model', MPATH, '--served-model-name', SA['served_model_name'],
               '--dtype', SA['dtype'], '--max-model-len', str(SA['max_model_len']), '--gpu-memory-utilization', str(SA['gpu_memory_utilization']),
               '--port', str(SA['port']), '--seed', str(SA['seed'])]
        proc = subprocess.Popen(cmd, stdout=open(logp, 'w'), stderr=subprocess.STDOUT, start_new_session=True)
        up, t2 = False, time.time()
        while time.time() - t2 < 1800:
            if proc.poll() is not None:
                break
            try:
                with urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5) as r_:
                    if r_.status == 200:
                        up = True
                        break
            except Exception:
                pass
            time.sleep(5)
        time.sleep(3)
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            proc.terminate()
        b = open(logp, 'rb').read()
        _lc = os.path.join(RES_P, 'logs-B'); os.makedirs(_lc, exist_ok=True)
        shutil.copy2(logp, os.path.join(_lc, os.path.basename(logp)))          # zip に入れる（置き場 results/logs-B/）
        _rd = read_topk_lines(b.decode('utf-8', 'replace'))
        TOPK.update(_rd, server_args=SA, server_up=up, log='logs-B/' + os.path.basename(logp), log_sha16=sha16_bytes(b),
                    status=('read' if _rd['top_k'] is not None else
                            ('ambiguous（値が一つに決まらない・登録者に上げる）' if _rd['top_k_values'] else 'unreadable（正本の値のまま・裁定 D142）')))
    except Exception as e:
        TOPK.update(status='failed（正本の値のまま・裁定 D142）', error='%s: %s' % (type(e).__name__, str(e)[:200]))
    mark('topk', status=TOPK.get('status'), top_k=TOPK.get('top_k'), values=TOPK.get('top_k_values'))
SREC['topk'] = TOPK
save_session()

# ---- 8. 終わり（ファイルの SHA16・zip）
files, raws = {}, {}
for cand, arm, form, rk in PLAN:
    for f in sorted(glob.glob(os.path.join(RES_P, TAG, rk, '*'))):
        rel = os.path.relpath(f, RES_P).replace('\\', '/')
        h = runs_B.sha16_file(f)
        (raws if os.path.basename(f).startswith('raw-') else files)[rel] = h
SREC.update(ended=now(), files_sha16_lf=files, raw_sha16_lf=raws, raw_publication=T['quality_floor']['raw_publication'], wall_s=round(time.time() - T0, 1))
save_session()
if not DRY:
    zp = shutil.make_archive(os.path.join(PERSIST, 'stageB-%s-s%d-%s' % (PHASE, SESSION, datetime.date.today().isoformat())), 'zip', PERSIST,
                             base_dir='results')
    print('[boot] zip → %s。コーディネータが Drive の Web UI からダウンロードし、SHA16 はセッション記録の files_sha16_lf・raw_sha16_lf と突合する。' % zp, flush=True)
print('[boot] 完了 phase=%s session=%d 走行キー %d・壁時計 %.0f 秒。%s' % (PHASE, SESSION, len(RUN_KEYS), time.time() - T0, CLAUSE), flush=True)
