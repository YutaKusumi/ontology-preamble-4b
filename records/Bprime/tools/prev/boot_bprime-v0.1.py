# -*- coding: utf-8 -*-
"""boot_bprime.py v0 —— B′ の Colab 起動器（G4・Gemma-4-31B-it・bf16・transformers 5 系・2026-09-30・コーディネータ南無弥勒如来）。

相（OP4B_PHASE）と段（OP4B_STEP）:
  check                 凍結の前の確かめ（正本 `computation.before_seal`・`computation.pre_freeze_checks`）。段は一つ。意味のない列だけで順伝播と生成の煙試験をし、
                        露出の記録（check.json・印字してよい値だけ）を置く。場面・腕・指示・書き出しを含む入力はトークナイザだけで確かめる。
  extract   start|run   相 extract（封印の後）。抽出の記録（転記行 D の元・npz の SHA・係数・g との一致の合否）と npz を置く（npz は公開の置き場に入れない）。
  behavior  start|run   行動の下見（生成・復号・凍結の採点・書き出しの根の件数・升目の集計）。run は最初の順伝播の前に、抽出の記録の形の項目を確かめる（T01）。
  pilot     start|run   読み取りの下見（模型を読み込み直した新しいランタイムで）。run は行動の下見の閉じた記録を確かめてから走る。
  main      start|run   本の計算（本の凍結の後）。OP4B_PART: main・pathdiff（pathdiff は本の計算がバッチ一のときだけ）。値と札を印字しない。
  recompute start|run   独立の再計算と独立の再抽出。OP4B_PART: hook・rewrite・reextract（rewrite と reextract は書き手と別の個体の器）。値を印字しない。
start: 起動の記録（時刻・セッション・GPU の名・正本と器の SHA・段の名・コミット）を書いて止まる。コーディネータがそれを公開の置き場の `records/Bprime/runs/` に写して push し
  （登録者の確認を得る）、そのコミットを OP4B_COMMIT に与えて run を走らせる。run は取り出したコミットの起動の記録が手元の起動の記録と一字違わず同じことを確かめてから、
  最初の順伝播をする（正本 `computation.start_records`・T13）。終わりに出力の SHA の記録（end-<相>.json）を書く（これも公開の置き場に置く）。
止める（登録者に相談）: 版・GPU・重みの SHA・凍結と封印の記録・取り出した器と正本の SHA・起動の記録の不一致・暦の期限（K2）・器の誤り（正本 `computation.tool_error`）・予期しない誤り。
印字の決まり: 相 check は `computation.before_seal.may_print` の値だけ。ほかの相は段の名・時間・数・SHA だけを印字する（値は置き場の記録に置く）。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する。資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。進みは progress.log にも書く。
セルに打つ一行（先頭の下線は type の事故の緩衝・<commit> は 40 桁）:
  ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='check';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_bprime.py').read())
DRY（手元の検査・OP4B_DRY=1）: 小さな乱数の Gemma 4（`dry_bprime.tiny_model`）を CPU で。OP4B_REPO_DIR（凍結の器の公開の置き場）・OP4B_BPRIME_DIR（B′ の置き場）・OP4B_OUT が要る。
  版・GPU・重み・凍結と封印の記録と起動の記録の公開は見ない（印を残す）。
柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, time, uuid, shutil, hashlib, datetime, traceback, subprocess, zipfile, collections

VERSION = 'v0.1'        # v0.1（2026-09-30）: 本の計算と独立の再計算の相で、台帳のつながりを本の凍結の後の行だけで照らす（前は全ての行を渡した・本の凍結の器を書いて見つけた）・独立の再抽出の組に方向を渡す（正本の口の五つの引数・前は四つ）。前の版は `prev/boot_bprime-v0.py`
T0 = time.time()
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
PHASES = ('check', 'extract', 'behavior', 'pilot', 'main', 'recompute')
STEPS = ('start', 'run')
PARTS = {'main': ('main', 'pathdiff'), 'recompute': ('hook', 'rewrite', 'reextract')}
STAGE_NAME = {'extract': '相 extract', 'behavior': '行動の下見', 'pilot': '読み取りの下見', 'main': '本の計算', 'recompute': '独立の再計算'}
SPARSE = ['tools', 'arms', 'design', 'records', 'results/dirB']
LOG = []
CTX = {'od': None, 'session': None, 'dry': False, 'progress': None}
CLAUSE = '本記録は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
JST = datetime.timezone(datetime.timedelta(hours=9))
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


def say(line):
    print(line, flush=True)
    if CTX['progress']:
        with open(CTX['progress'], 'a', encoding='utf-8') as fh:
            fh.write(line + '\n')


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
    say('[boot_bprime] %-18s %7.0fs %s' % (step, time.time() - T0, kw or ''))


def jdefault(o):
    if hasattr(o, 'tolist'):
        return o.tolist()
    if hasattr(o, 'item'):
        return o.item()
    raise TypeError(type(o))


def write_json(path, obj):
    json.dump(obj, open(path, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=jdefault)
    return sha256f(path)


def sh(cmd, check=True):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-3000:])
        raise RuntimeError('失敗: %s' % cmd)
    return r


def package(tag, extra=None):
    """置き場の中身を zip にして落とす（段の終わり・止め・誤り）。session を書いてから zip にし、zip の SHA-256 を記す。"""
    od, S = CTX['od'], CTX['session']
    if not od or S is None:
        return None
    S.update(extra or {})
    S.update({'log': LOG, 'packaged': tag, 'packaged_at': now(), 'seconds': round(time.time() - T0, 1), 'clause': CLAUSE})
    write_json(os.path.join(od, 'session.json'), S)
    zp = od + ('.zip' if tag == 'final' else '-%s.zip' % tag)
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(od)):
            z.write(os.path.join(od, fn), os.path.join(os.path.basename(od), fn))
    zsha = sha256f(zp)
    S.setdefault('zips', []).append({'tag': tag, 'zip': os.path.basename(zp), 'sha256': zsha})
    write_json(od + '-zips.json', {'zips': S['zips'], 'clause': CLAUSE})
    mark('packaged', tag=tag, zip=os.path.basename(zp), sha256=zsha)
    if not CTX['dry']:
        try:
            from google.colab import files
            files.download(zp)
        except Exception as e_:
            print('[boot_bprime] zip の自動のダウンロードが走らなかった（左の「ファイル」から落とす）: %s' % e_)
    return zp


def stop(msg):
    mark('stop', reason=msg)
    package('stopped', {'stopped': msg})
    sys.exit('[boot_bprime] 止める（登録者に相談）: ' + msg)


def run():
    PHASE = os.environ.get('OP4B_PHASE', 'check')
    STEP = os.environ.get('OP4B_STEP', 'run' if PHASE == 'check' else '')
    COMMIT = os.environ.get('OP4B_COMMIT', '')
    DRY = os.environ.get('OP4B_DRY') == '1'
    if PHASE not in PHASES:
        sys.exit('[boot_bprime] 相は %s のどれか' % '・'.join(PHASES))
    if PHASE != 'check' and STEP not in STEPS:
        sys.exit('[boot_bprime] OP4B_STEP は start か run')
    part = os.environ.get('OP4B_PART', '')
    if PHASE in PARTS and STEP == 'run' and part not in PARTS[PHASE]:
        sys.exit('[boot_bprime] OP4B_PART は %s のどれか一つ' % '・'.join(PARTS[PHASE]))
    if not DRY:
        stray = sorted(k for k in os.environ if k.startswith('OP4B_DRY') or k in ('OP4B_REPO_DIR', 'OP4B_BPRIME_DIR', 'OP4B_OUT'))
        if stray:
            sys.exit('[boot_bprime] DRY でないのに検査用の環境変数がある: %s' % '・'.join(stray))
        if not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
            sys.exit('[boot_bprime] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
    say('[boot_bprime] %s 開始 phase=%s step=%s part=%s %s' % (VERSION, PHASE, STEP or '-', part or '-', 'DRY' if DRY else COMMIT))

    # ---- 1. 置き場（コミット固定）
    if DRY:
        REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
        ROOT = os.path.abspath(os.environ['OP4B_BPRIME_DIR'])
        OUTROOT = os.path.abspath(os.environ['OP4B_OUT'])
    else:
        REPO, OUTROOT = '/content/ontology-preamble-4b', '/content/op4b-Bprime'
        ROOT = REPO
        head_ok = os.path.isdir(os.path.join(REPO, '.git')) and sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
        if not head_ok:
            if os.path.isdir(os.path.join(REPO, '.git')):
                sh(['git', '-C', REPO, 'fetch', '-q', '--filter=blob:none', 'origin', COMMIT])
            else:
                shutil.rmtree(REPO, ignore_errors=True)
                sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
                sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone'] + SPARSE)
            sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
        if sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() != COMMIT:
            stop('取り出したコミットが OP4B_COMMIT と違う')
        dirty = sh(['git', '-C', REPO, 'status', '--porcelain'], check=False).stdout.strip()
        if dirty:
            stop('取り出した作業木に変更がある: %s' % dirty.splitlines()[:5])
    os.environ['OP4B_REPO'] = REPO
    os.makedirs(OUTROOT, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    od = os.path.join(OUTROOT, '%s%s%s-%s' % (PHASE, ('-' + STEP) if STEP else '', ('-' + part) if part else '', stamp))
    os.makedirs(od, exist_ok=True)
    CTX.update(od=od, dry=DRY, progress=os.path.join(od, 'progress.log'), session={'kind': 'bprime_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY, 'step': STEP, 'part': part})
    TOOLS = os.path.join(ROOT, 'tools')
    for p_ in (os.path.join(REPO, 'tools'), TOOLS):
        if p_ not in sys.path:
            sys.path.insert(0, p_)
    CANON = os.path.join(ROOT, 'design', 'contrasts-Bprime.json')
    C = json.load(open(CANON, encoding='utf-8'))
    RECS = os.path.join(ROOT, 'records', 'Bprime')
    L = json.load(open(os.path.join(TOOLS, 'ledger-bprime.json'), encoding='utf-8'))
    FRP = os.path.join(RECS, 'FREEZE-RECORD-Bprime.json')
    SRP = os.path.join(RECS, 'sealing-record-Bprime.json')
    FR = SR = None
    if PHASE != 'check':
        if DRY:
            mark('dry_no_gate', note='DRY は凍結と封印の記録と起動の記録の公開を見ない')
            FR = json.load(open(os.environ['OP4B_DRY_FREEZE'], encoding='utf-8')) if os.environ.get('OP4B_DRY_FREEZE') else None
        else:
            for p_ in (FRP, SRP):
                if not os.path.exists(p_):
                    stop('相 %s は下見の前の凍結と封印の後に走らせる（%s が無い）' % (PHASE, os.path.basename(p_)))
            FR = json.load(open(FRP, encoding='utf-8'))
            SR = json.load(open(SRP, encoding='utf-8'))
            import bl3_core as K_
            now_s = {rp: (sha16f(os.path.join(REPO, *rp.split('/'))) if os.path.exists(os.path.join(REPO, *rp.split('/'))) else None) for rp in FR['frozen_sha16']}
            sha_map = (FR.get('main_freeze') or {}).get('frozen_sha16') if PHASE in ('main', 'recompute') else FR['frozen_sha16']
            if PHASE in ('main', 'recompute') and not sha_map:
                stop('相 %s は本の凍結の後に走らせる（凍結の記録に本の凍結が無い）' % PHASE)
            devs_ = list(FR.get('deviations') or [])
            if PHASE in ('main', 'recompute'):
                devs_ = devs_[int(FR['main_freeze']['deviations_n']):]        # 本の凍結の値からは、本の凍結の後に記した台帳の行だけでつなぐ（v0.1・芯の関数の決まり）
            bad = K_.ledger_chain_bad(sha_map, {rp: now_s.get(rp) for rp in sha_map}, devs_, paths=list(sha_map))
            if bad:
                stop('凍結の記録の SHA16 と取り出したファイルが違う: %s' % bad)
            for role in ('coordinator', 'registrant'):
                pp = os.path.join(REPO, *SR['predictions'][role]['path'].split('/'))
                if not os.path.exists(pp) or sha256f(pp) != SR['predictions'][role]['sha256']:
                    stop('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
            import bprime_core as Pc
            seal_jst = datetime.datetime.fromisoformat(SR['sealed_at_jst'])
            if Pc.calendar_closed(seal_jst, datetime.datetime.now(JST), C['computation']['stops']['calendar']['days'], False):
                stop('暦の期限を過ぎた（正本 `computation.stops.calendar`）: %s' % C['computation']['stops']['calendar']['close_sentence'])
            mark('frozen', checked=len(sha_map))
    mark('repo', commit=COMMIT[:12] or 'dry', canon=C['version'], canon_sha16=sha16f(CANON), out=od)

    # ---- 2. 版と GPU と決定性の設定
    import importlib.metadata as md

    def ver(k):
        try:
            return md.version(k)
        except Exception:
            return None
    VER = {k: ver(k) for k in ('numpy', 'scipy', 'torch', 'transformers', 'tokenizers', 'huggingface_hub', 'jinja2', 'safetensors', 'accelerate')}
    V = C['inputs']['versions']
    pins = dict((FR or {}).get('prefreeze', {}).get('pins') or {})
    pins.update({'transformers': V['transformers'], 'torch': V['torch']})
    bad_v = {k: VER.get(k) for k, v in pins.items() if VER.get(k) != v}
    if bad_v and not DRY:
        mark('pin', installing=bad_v)
        pk = ['%s==%s' % (k, v) for k, v in pins.items() if k != 'torch' and k in bad_v]
        if 'torch' in bad_v:
            cuda = V['torch'].split('+')[1]
            sh([sys.executable, '-m', 'pip', 'install', '-q', 'torch==%s' % V['torch'], '--index-url', 'https://download.pytorch.org/whl/%s' % cuda])
        if pk:
            sh([sys.executable, '-m', 'pip', 'install', '-q'] + pk)
        print('[boot_bprime] 版を入れ直した。**ランタイムを再起動して（「ランタイム」→「セッションを再起動」）、同じ一行をもう一度走らせる**', flush=True)
        sys.exit(0)
    GPU = 'dry'
    if not DRY:
        GPU = sh('nvidia-smi --query-gpu=name --format=csv,noheader', check=False).stdout.strip().split('\n')[0]
        if C['inputs']['gpu']['name'] not in GPU:
            stop('GPU %s は登録の環境（%s）でない' % (GPU, C['inputs']['gpu']['name']))
    mark('versions', versions=VER, gpu=GPU)
    os.environ['HF_HUB_DISABLE_XET'] = '1'
    import numpy as np
    import torch
    attn = os.environ.get('OP4B_ATTN', 'sdpa') if PHASE == 'check' else ((FR or {}).get('prefreeze', {}).get('attn_implementation') or ('eager' if DRY else None))
    if attn is None:
        stop('凍結の記録に注意の実装が無い')
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision('highest')
    DET = {'allow_tf32_matmul': torch.backends.cuda.matmul.allow_tf32, 'allow_tf32_cudnn': torch.backends.cudnn.allow_tf32, 'float32_matmul_precision': torch.get_float32_matmul_precision(),
           'attn_implementation': attn}
    if FR and 'determinism' in (FR.get('prefreeze') or {}) and {k: FR['prefreeze']['determinism'].get(k) for k in DET} != DET and not DRY:
        stop('決定性の設定が凍結の記録と違う')
    import bprime_gemma as G
    import bprime_core as P
    import bprime_run as BR
    import bprime_directions as BD
    import bprime_behavior as BB
    import bprime_phases as PH
    TOOL_FILES = sorted(fn for fn in os.listdir(TOOLS) if fn.startswith('bprime_') and fn.endswith('.py'))
    TOOL_SHA = {fn: sha16f(os.path.join(TOOLS, fn)) for fn in TOOL_FILES}
    TOOL_SHA['colab/boot_bprime.py'] = sha16f(os.path.join(TOOLS, 'colab', 'boot_bprime.py')) if os.path.exists(os.path.join(TOOLS, 'colab', 'boot_bprime.py')) else None

    # ---- 3. 起動の記録（start は書いて止まる・run は公開の版と照らす）
    START_LOCAL = os.path.join(OUTROOT, 'start-%s%s.json' % (PHASE, ('-' + part) if part else ''))
    if PHASE != 'check' and STEP == 'start':
        rec = collections.OrderedDict([('kind', 'bprime_start_record'), ('stage', STAGE_NAME[PHASE]), ('phase', PHASE), ('part', part or None), ('session', str(uuid.uuid4())),
                                       ('time_utc', now()), ('time_jst', datetime.datetime.now(JST).isoformat(timespec='seconds')), ('gpu', GPU), ('commit', COMMIT or 'dry'),
                                       ('contract_sha16', sha16f(CANON)), ('tools_sha16', TOOL_SHA), ('freeze_record_sha16', sha16f(FRP) if os.path.exists(FRP) else None),
                                       ('seal_record_sha16', sha16f(SRP) if os.path.exists(SRP) else None), ('versions', VER), ('clause', CLAUSE)])
        sha = write_json(START_LOCAL, rec)
        shutil.copy(START_LOCAL, os.path.join(od, os.path.basename(START_LOCAL)))
        CTX['session'].update(start_record=os.path.basename(START_LOCAL), start_sha256=sha)
        package('final', {'finished': now()})
        say('[boot_bprime] 起動の記録を書いた（SHA-256 %s）。records/Bprime/runs/ に写して公開の置き場に置き、そのコミットで OP4B_STEP=run を走らせる' % sha)
        return od
    if PHASE != 'check':
        if not os.path.exists(START_LOCAL):
            stop('手元の起動の記録が無い（同じランタイムで start を先に走らせる）')
        pub = os.path.join(RECS, 'runs', os.path.basename(START_LOCAL))
        if DRY:
            mark('dry_start_unpublished', local=os.path.basename(START_LOCAL))
        elif not os.path.exists(pub) or sha256f(pub) != sha256f(START_LOCAL):
            stop('公開の置き場の起動の記録が手元の起動の記録と違う（写して push してから run を走らせる）')
        START = json.load(open(START_LOCAL, encoding='utf-8'))
        if START['phase'] != PHASE or (START.get('part') or '') != part or START['contract_sha16'] != sha16f(CANON) or START['tools_sha16'] != TOOL_SHA:
            stop('起動の記録の相・組・正本と器の SHA が今と違う')
        CTX['session'].update(start_record=os.path.basename(START_LOCAL), start_sha256=sha256f(START_LOCAL), session_id=START['session'])

    # ---- 4. 重みと模型
    from transformers import AutoTokenizer
    if DRY:
        import dry_bprime as DR
        tok = AutoTokenizer.from_pretrained(DR.HF)
        model, _, _ = DR.tiny_model(5, 4.0, torch.float32)
        W_SHA = {}
        C = dry_contract(C, model)                                          # DRY だけ: 小さな模型の形に合わせた正本の写し（正本のファイルは変えない・v0.1）
        mark('dry_contract', layer_index=C['layers']['index'], iso=C['nulls']['isotropic']['count'], max_new=C['inputs']['generation_B']['max_tokens'])
    else:
        from huggingface_hub import snapshot_download
        from transformers import Gemma4ForConditionalGeneration
        M = C['inputs']['model']
        snap = snapshot_download(M['id'], revision=M['revision'])
        man = json.load(open(os.path.join(RECS, 'MANIFEST-gemma-4-31B-it.json'), encoding='utf-8'))
        W_SHA = {fn: sha256f(os.path.join(snap, fn)) for fn in man['files']}
        badw = [fn for fn, r in man['files'].items() if W_SHA[fn] != r['sha256'].upper()]
        if badw:
            stop('重みか設定の SHA-256 が目録と違う: %s' % badw)
        shards = sorted(set(json.load(open(os.path.join(snap, 'model.safetensors.index.json'), encoding='utf-8'))['weight_map'].values()))
        if [s for s in shards if s not in man['files']]:
            stop('重みの断片が目録に無い（凍結の前に目録を作る・K9）')
        tok = AutoTokenizer.from_pretrained(snap)
        t_ = time.time()
        model = Gemma4ForConditionalGeneration.from_pretrained(snap, dtype=torch.bfloat16, device_map='cuda', attn_implementation=attn).eval()
        mark('load', seconds=round(time.time() - t_, 1), alloc_gib=round(torch.cuda.memory_allocated() / 2 ** 30, 2))
    CTX['session'].update(gpu=GPU, versions=VER, determinism=DET, weights_sha256=W_SHA, canon_sha16=sha16f(CANON), tools_sha16=TOOL_SHA)
    S = CTX['session']

    def finish(outputs):
        """出力の SHA の記録（end-<相>.json・公開の置き場に置く）を書いて zip にする。"""
        end = {'kind': 'bprime_end_record', 'phase': PHASE, 'part': part or None, 'session': S.get('session_id'), 'time_utc': now(),
               'outputs_sha256': {fn: sha256f(os.path.join(od, fn)) for fn in outputs}, 'clause': CLAUSE}
        write_json(os.path.join(od, 'end-%s%s.json' % (PHASE, ('-' + part) if part else '')), end)
        package('final', {'finished': now()})
        mark('done', outputs=len(outputs))
        return od

    # ---- 5. 相
    if PHASE == 'check':
        MQ = json.load(open(os.path.join(RECS, 'meaningless-Bprime.json'), encoding='utf-8'))
        try:
            import bprime_reextract as RX
            rx = RX.reextract
        except ImportError:
            rx = None
        rec = PH.check_items(model, tok, C, L, MQ, os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'main_position_activations.npz'), reextract=rx,
                             gen_max_new=int(os.environ.get('OP4B_SMOKE_TOKENS', '256')), log=say)
        rec.update({'gpu': GPU, 'versions': VER, 'determinism': DET, 'clause': CLAUSE})
        write_json(os.path.join(od, 'check.json'), rec)
        mark('check', all_pass=rec['all_pass'], failed=[k for k, v in rec['items'].items() if not v.get('pass')])
        return finish(['check.json'])
    TOOL_ERR = (P.ToolError, AssertionError)
    if PHASE == 'extract':
        npz_stageB = os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'main_position_activations.npz')
        g_sha = (FR or {}).get('prefreeze', {}).get('g', {}).get('g_sha256') if not DRY else os.environ.get('OP4B_DRY_G')
        try:
            q = BD.bl3_ratio(npz_stageB)['acts']
            npz, rec = PH.extract(model, tok, C, L, g_sha, npz_stageB, stageB_qwen_acts=q, log=say)
        except TOOL_ERR as e_:
            write_json(os.path.join(od, 'extract-tool-error.json'), {'tool_error': str(e_), 'clause': CLAUSE})
            finish(['extract-tool-error.json'])
            stop('器の誤りで相 extract が止まった（直してやり直すかは登録者の裁定）: %s' % e_)
        open(os.path.join(od, 'directions-Bprime.npz'), 'wb').write(npz)
        rec.update({'start_record_sha256': S.get('start_sha256'), 'session': S.get('session_id'), 'time_utc': now(), 'versions': VER, 'weights_sha256': W_SHA, 'clause': CLAUSE})
        write_json(os.path.join(od, 'extraction-record-Bprime.json'), rec)
        mark('extract', npz_sha256=rec['npz_sha256'][:16], g_match=rec['checks']['g_match'])
        return finish(['directions-Bprime.npz', 'extraction-record-Bprime.json'])
    if PHASE == 'behavior':
        ex = os.path.join(RECS, 'extract', 'extraction-record-Bprime.json')
        if not DRY:
            miss = PH_form_items(ex, C, S)
            if miss:
                stop('抽出の記録の形の項目がそろわない: %s' % miss)
        batch = int((FR or {}).get('prefreeze', {}).get('behavior_batch') or os.environ.get('OP4B_DRY_BATCH', '8'))
        try:
            out = PH.behavior(model, tok, C, L, batch, log=say)
        except TOOL_ERR as e_:
            write_json(os.path.join(od, 'behavior-tool-error.json'), {'tool_error': str(e_), 'clause': CLAUSE})
            finish(['behavior-tool-error.json'])
            stop('器の誤りで行動の下見が止まった（正本 `behavior_pilot.order`: 読み取りの下見は続ける・そこまでの記録を閉じて公開する）: %s' % e_)
        write_json(os.path.join(od, 'behavior-trials.json'), {'trials': out['trials'], 'calls': out['calls'], 'fixed': out['fixed'], 'clause': CLAUSE})
        write_json(os.path.join(od, 'behavior-scored.json'), {'scored': out['scored'], 'roots': out['roots'], 'summaries': out['summaries'], 'digests': out['digests'], 'clause': CLAUSE})
        mark('behavior', cells=len(out['summaries']), trials=sum(len(v) for v in out['trials'].values()), gen_ids_sha256=out['digests']['gen_ids_sha256'][:16])
        return finish(['behavior-trials.json', 'behavior-scored.json'])
    if PHASE == 'pilot':
        closed = json.load(open(os.path.join(RECS, 'behavior', 'behavior-closed-Bprime.json'), encoding='utf-8')) if not DRY else json.load(open(os.environ['OP4B_DRY_CLOSED'], encoding='utf-8'))
        facts = json.load(open(os.path.join(RECS, 'facts-Bprime-pre.json'), encoding='utf-8'))
        kz = (FR or {}).get('prefreeze', {}).get('logit_k') or ({'k': 1.0, 'z0': 4} if DRY else None)
        if kz is None:
            stop('凍結の記録に出口の値の自己検査の k が無い')
        try:
            rec = PH.pilot(model, tok, C, L, facts, closed, kz['k'], kz['z0'], log=say)
        except TOOL_ERR as e_:
            rec = {'tool_error': str(e_)}
        rec.update({'start_record_sha256': S.get('start_sha256'), 'session': S.get('session_id'), 'time_utc': now(), 'clause': CLAUSE})
        write_json(os.path.join(od, 'pilot-Bprime.json'), rec)
        if 'tool_error' in rec:
            finish(['pilot-Bprime.json'])
            stop('器の誤りで読み取りの下見が止まった（正本 `pilot.tool_error`・直してやり直すかは登録者の裁定）: %s' % rec['tool_error'])
        mark('pilot', q1=(rec.get('decision') or {}).get('q1'), batch=rec.get('batch'), n_forward=rec.get('n_forward'))
        return finish(['pilot-Bprime.json'])
    # 本の計算と独立の再計算
    npz_in = os.environ.get('OP4B_NPZ', os.path.join(OUTROOT, 'in', 'directions-Bprime.npz'))
    exj = os.path.join(RECS, 'extract', 'extraction-record-Bprime.json') if not DRY else os.environ['OP4B_DRY_EXTRACT']
    try:
        dirs, names = BR.load_dirs(npz_in, exj, C)
    except P.ToolError as e_:
        stop(str(e_))
    EX = json.load(open(exj, encoding='utf-8'))
    pil = (FR or {}).get('main_freeze', {}).get('pilot') if not DRY else json.load(open(os.environ['OP4B_DRY_PILOT'], encoding='utf-8'))
    if not pil or pil.get('tool_error') or (pil.get('decision') or {}).get('stop'):
        stop('本の凍結の下見の記録が無いか、止める・器の誤り（本の計算は走らせない）')
    kz = (FR or {}).get('prefreeze', {}).get('logit_k') or {'k': 1.0, 'z0': 4}
    keys = ['%s|%s' % (sc, arm) for sc, arm in C['cells_main']]
    cells = BR.build_cells(tok, C, L, keys)
    out = collections.OrderedDict(part=part, clause=CLAUSE)
    try:
        if PHASE == 'main':
            out['result'] = PH.main_part(part, model, C, cells, dirs, names, pil, kz['k'], kz['z0'], float(EX['coefficient']), log=say)
        elif part == 'hook':
            import bl3_core as K_
            rows, dbr = K_.recompute_set(C['main_rows'], [n[len('real:'):] for n in names['real']], C['nulls']['real']['swap_siblings'], len(names['iso']),
                                         (pil.get('decision') or {}).get('dropped', []))
            out['result'] = PH.main_part('recompute', model, C, cells, dirs, names, pil, kz['k'], kz['z0'], float(EX['coefficient']),
                                         rows_rc=([(n, cells[ck], s) for n, ck, s in rows], dbr), log=say)
        elif part == 'rewrite':
            import bprime_recompute_rewrite as RW              # 書き手と別の個体の器
            out['result'] = RW.recompute_rewrite(model, tok, C, L, dirs, names, pil, float(EX['coefficient']))
        elif part == 'reextract':
            import bprime_reextract as RX                      # 書き手と別の個体の器
            out['result'] = RX.reextract_all(model, tok, C, L, dirs)          # 正本 `independent_recompute.interfaces.reextract` の口（v0.1・前は dirs を渡していなかった）
    except TOOL_ERR as e_:
        out['tool_error'] = str(e_)
    fn = '%s-%s.json' % (PHASE, part)
    write_json(os.path.join(od, fn), out)
    if 'tool_error' in out:
        finish([fn])
        stop('器の誤りで組 %s が止まった（結果を開かずに登録者に上げる）: %s' % (part, out['tool_error']))
    mark('part', part=part)
    return finish([fn])


def dry_contract(C, model):
    """DRY（手元の検査）だけで使う正本の写し: 小さな模型の層の数から層の添字（`direction_B.layer_index` の式）と `hidden_states_index` を作り直し、
    等方の本数（OP4B_DRY_ISO・既定 9）と生成の上限（OP4B_DRY_MAX_NEW・既定 12）を小さくする。ほかの鍵は変えない。
    模型の事実（`inputs.model_facts`）は本物の模型の値のまま残す（小さな模型を本物と取り違えさせない・書き手と別の個体の器は層の数と次元で本物かを見分ける）。
    そのため DRY の相 check の「模型の事実」の項目は落ちるのが正しい形になる。正本のファイルの SHA16 は元のまま記録に入る（DRY の印つき）。"""
    import copy
    import bprime_gemma as G_
    Cd = copy.deepcopy(C)
    n = int(model.config.text_config.num_hidden_layers)
    Cd['layers']['index'] = G_.layer_index(Cd['layers']['ratio'], n)
    Cd['layers']['hidden_states_index'] = Cd['layers']['index'] + 1
    Cd['nulls']['isotropic']['count'] = int(os.environ.get('OP4B_DRY_ISO', '9'))
    Cd['inputs']['generation_B'] = dict(Cd['inputs']['generation_B'], max_tokens=int(os.environ.get('OP4B_DRY_MAX_NEW', '12')))
    Cd['dry_contract'] = 'DRY の写し（層の添字・等方の本数・生成の上限だけを小さな模型に合わせた・模型の事実は本物の値のまま）'
    return Cd


def PH_form_items(path, C, S):
    """抽出の記録の形の項目（正本 `computation.extraction_record.form_items`）のうち、器が機械で見られる欄（値は読まない）。戻り値: 落ちた項目の並び。"""
    if not os.path.exists(path):
        return ['公開した抽出の記録が無い']
    R = json.load(open(path, encoding='utf-8'))
    miss = [k for k in ('row_D', 'npz_sha256', 'coefficient', 'g_match', 'checks', 'start_record_sha256', 'time_utc', 'versions', 'weights_sha256') if k not in R]
    if not miss and not all(bool(v) for v in R['checks'].values()):
        miss.append('凍結した確かめの合否がすべて「通った」でない')
    if not miss and R['versions'] != S.get('versions'):
        miss.append('版のピンが文字列で一致しない')
    if not miss and R['weights_sha256'] != S.get('weights_sha256'):
        miss.append('重みの断片の SHA が合わない')
    return miss


if __name__ == '__main__':
    try:
        run()
    except SystemExit:
        raise
    except Exception:
        LOG.append({'step': 'crash', 'at': now(), 'traceback': traceback.format_exc()[-4000:]})
        package('crash', {'crash': traceback.format_exc()[-4000:]})
        say('[boot_bprime] 予期しない誤りで止まった（器の誤りではない・登録者に相談）')
        raise
