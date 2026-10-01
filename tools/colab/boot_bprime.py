# -*- coding: utf-8 -*-
"""boot_bprime.py v0.4 —— B′ の Colab 起動器（G4・Gemma-4-31B-it・bf16・transformers 5 系・2026-09-30・コーディネータ南無弥勒如来）。

相（OP4B_PHASE）と段（OP4B_STEP）:
  check                 凍結の前の確かめ（正本 `computation.before_seal`・`computation.pre_freeze_checks`）。段は一つ。意味のない列だけで順伝播と生成の煙試験をし、
                        露出の記録（check.json・印字してよい値だけ）を置く。場面・腕・指示・書き出しを含む入力はトークナイザだけで確かめる。
  extract   start|run   相 extract（封印の後）。抽出の記録（転記行 D の元・npz の SHA・係数・g との一致の合否）と npz を置く（npz は公開の置き場に入れない）。
  behavior  start|run   行動の下見（生成・復号・凍結の採点・書き出しの根の件数・升目の集計）。run は最初の順伝播の前に、抽出の記録の形の項目（六つ）を確かめる（T01）。
                        手元の方向の npz を OP4B_NPZ か `<出力の置き場>/in/directions-Bprime.npz` に置いておく（形の項目 2 が公開した記録と照らす・v0.4）。
  pilot     start|run   読み取りの下見（模型を読み込み直した新しいランタイムで）。run は行動の下見の閉じた記録を確かめてから走る。
  main      start|run   本の計算（本の凍結の後）。OP4B_PART: main・pathdiff（pathdiff は本の計算がバッチ一のときだけ）。値と札を印字しない。
  recompute start|run   独立の再計算と独立の再抽出。OP4B_PART: hook・rewrite・reextract（rewrite と reextract は書き手と別の個体の器）。値を印字しない。
start: 起動の記録（時刻・セッション・GPU の名・正本と器の SHA・段の名・コミット）を書いて止まる。記録の名は `start-<相>[-<組>]-<セッションの頭の 8 字>.json`（v0.4・やり直しが重ならない）。
  コーディネータがそれを公開の置き場の `records/Bprime/runs/` に写して push し
  （登録者の確認を得る）、そのコミットを OP4B_COMMIT に与えて run を走らせる。run は取り出したコミットの起動の記録が手元の起動の記録と一字違わず同じことを確かめてから、
  最初の順伝播をする（正本 `computation.start_records`・T13）。終わりに出力の SHA の記録（`end-<相>[-<組>]-<セッションの頭の 8 字>.json`）を書く（これも公開の置き場に置く）。
  組のある相（main・recompute）は、組ごとに start と run を走らせる（組ごとに起動の記録を置いたコミットで run が走るので、組の間でコミットは違ってよい・集計の器は中身〔正本・器の閉包・
  本の凍結の節・方向の npz の SHA〕で照らす・組の間で器が違えばすべての組をやり直す）。
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

VERSION = 'v0.4'        # v0.4（2026-09-30・器の実装の検分の後）: 錠を関数 `gate_bad` に切り出し、暦の期限の照らしに時刻の文字列を渡す（前は時刻のオブジェクトで、封印の後のどの相でも例外になる形だった・U05）・器の SHA16 を閉包で取る（U08）・起動の記録と出力の SHA の記録の名にセッションを入れる（U09）・run の段で起動の記録の凍結と封印の記録の SHA16 を照らす（U10）・session に本の凍結の節の SHA16 と方向の npz の SHA-256 を書く（U08・U10）・相 pilot で閉じた記録を照らす（U12）・k とバッチの既定の値は DRY だけ（U19）・start の段で組を照らす（U20）・本番でも OP4B_PUB_TOOLS を置く（U24）・別の個体の器の読み込みを始めに確かめ、止めの SystemExit を器の誤りとして受ける（U42・U43）・列の長さと窓を照らす（U50）・抽出の記録の形の項目の六つを全部照らす関数 `form_items_check`（前は三つと一部・U02）・起動の記録に台帳の行の数（`deviations_n`）を書く・錠が閉じた記録と G4 の期限を見る（U16）・DRY だけの語彙の行列の倍率の口（OP4B_DRY_WSCALE・合成データの確かめの出口の値を大きくした枝・U46）。前の版は `prev/boot_bprime-v0.3.py`／v0.3（2026-09-30）: DRY の正本の写しで、読み取りの下見の (i)(ii) の門を開ける（質量の下限 0・確率の幅 [0, 1]・`dry_bprime.py` の P1 と同じ・小さな乱数の模型では 8 升目とも落ちて本の計算の相へ進めなかった）。前の版は `prev/boot_bprime-v0.2.py`／v0.2（2026-09-30）: run の段で、出力の置き場に起動の記録の写しを置く（閉じる器と凍結の器が出力の置き場で読む・Colab の合成データの正式の確かめで、閉じる器が止まって見つけた・K19）。前の版は `prev/boot_bprime-v0.1.py`／v0.1（2026-09-30）: 本の計算と独立の再計算の相で、台帳のつながりを本の凍結の後の行だけで照らす（前は全ての行を渡した・本の凍結の器を書いて見つけた）・独立の再抽出の組に方向を渡す（正本の口の五つの引数・前は四つ）。前の版は `prev/boot_bprime-v0.py`
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


def gate_bad(C, REPO, PHASE, FR, SR, now_jst):
    """錠（凍結と封印の記録・台帳のつながり・予想の SHA・暦の期限・本の凍結とその節の SHA16）の照らし。戻り値: 外れの文の並び（空なら通る）。
    本番の run() と合成データの確かめが同じ関数を呼ぶ（v0.4・U05）。now_jst は日本時間の時刻の文字列（'YYYY-MM-DD HH:MM[:SS]'）。"""
    import bl3_core as K_
    import bprime_core as Pc
    bad = []
    now_s = {rp: (sha16f(os.path.join(REPO, *rp.split('/'))) if os.path.exists(os.path.join(REPO, *rp.split('/'))) else None) for rp in FR['frozen_sha16']}
    if PHASE in ('main', 'recompute'):
        mf = FR.get('main_freeze')
        if not mf:
            return ['相 %s は本の凍結の後に走らせる（凍結の記録に本の凍結が無い）' % PHASE]
        if FR.get('main_freeze_sha16') != Pc.main_freeze_sha16(FR):
            bad.append('本の凍結の節の正準の SHA16 が、凍結の器が記した値と違う（U10）')
        sha_map, devs_ = mf['frozen_sha16'], list(FR.get('deviations') or [])[int(mf['deviations_n']):]     # 本の凍結の後に記した台帳の行だけでつなぐ（v0.1）
    else:
        sha_map, devs_ = FR['frozen_sha16'], list(FR.get('deviations') or [])
    bad += ['凍結の記録の SHA16 と取り出したファイルが違う: %s' % x for x in K_.ledger_chain_bad(sha_map, {rp: now_s.get(rp) for rp in sha_map}, devs_, paths=list(sha_map))]
    for role in ('coordinator', 'registrant'):
        pp = os.path.join(REPO, *SR['predictions'][role]['path'].split('/'))
        if not os.path.exists(pp) or sha256f(pp) != SR['predictions'][role]['sha256']:
            bad.append('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
    if Pc.calendar_closed(SR['sealed_at_jst'], now_jst, C['computation']['stops']['calendar']['days'], False):
        bad.append('暦の期限を過ぎた（正本 `computation.stops.calendar`）: %s' % C['computation']['stops']['calendar']['close_sentence'])
    import g4_attempts_Bprime as G4T
    bad += G4T.closed_bad(REPO)                                               # 閉じた記録か G4 の期限で止める（再び始めない・正本 `computation.stops`・v0.4・U16）
    return bad


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
    if PHASE in PARTS and part not in PARTS[PHASE]:                          # start の段でも組を照らす（v0.4・U20）
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
    if not DRY:
        os.environ['OP4B_PUB_TOOLS'] = os.path.join(REPO, 'tools')              # 別の個体の器が凍結の器を読む置き場（合成データの確かめと同じ道・v0.4・U24）
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
    win = int(C['inputs']['model_facts']['sliding_window'])
    long_ = max([int(v['prompt_len']) for v in L['cells_main'].values()] + [int(v.get('prompt_len') or v.get('n_tokens') or 0) for v in L['extract_contexts'].values()])
    if not long_ < win:
        sys.exit('[boot_bprime] 列の長さ %d が窓 %d より短くない（正本 `layers.window_assert`・v0.4・U50）' % (long_, win))
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
            bad = gate_bad(C, REPO, PHASE, FR, SR, datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'))
            if bad:
                stop('錠の照らしが外れた: %s' % bad)
            sha_map = (FR.get('main_freeze') or {}).get('frozen_sha16') if PHASE in ('main', 'recompute') else FR['frozen_sha16']
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
    import freeze_Bprime as FZ
    TOOL_SHA = FZ.closure_sha_map()                                         # 器の閉包の SHA16（凍結の器と同じ関数・凍結の器を含む・v0.4・U08）

    # ---- 3. 起動の記録（start は書いて止まる・run は公開の版と照らす）
    START_LOCAL = os.path.join(OUTROOT, 'start-%s%s.json' % (PHASE, ('-' + part) if part else ''))       # 同じランタイムの start と run をつなぐ手元の置き場（公開の名はセッションつき）
    CLOSED_P = os.environ.get('OP4B_DRY_CLOSED') if DRY else os.path.join(RECS, 'behavior', 'behavior-closed-Bprime.json')
    if PHASE != 'check' and STEP == 'start':
        sess = str(uuid.uuid4())
        rec = collections.OrderedDict([('kind', 'bprime_start_record'), ('stage', STAGE_NAME[PHASE]), ('phase', PHASE), ('part', part or None), ('session', sess),
                                       ('time_utc', now()), ('time_jst', datetime.datetime.now(JST).isoformat(timespec='seconds')), ('gpu', GPU), ('commit', COMMIT or 'dry'),
                                       ('contract_sha16', sha16f(CANON)), ('tools_sha16', TOOL_SHA), ('freeze_record_sha16', sha16f(FRP) if os.path.exists(FRP) else None),
                                       ('seal_record_sha16', sha16f(SRP) if os.path.exists(SRP) else None),
                                       ('deviations_n', len(FR.get('deviations') or []) if FR else None), ('versions', VER), ('clause', CLAUSE)])     # 台帳の行の数（この後に記した行だけで器の SHA をつなぐ・v0.4・U02）
        if PHASE == 'pilot':
            rec['closed_record_sha16'] = sha16f(CLOSED_P) if (CLOSED_P and os.path.exists(CLOSED_P)) else None          # 行動の下見の閉じた記録（run で照らす・v0.4・U12）
        sha = write_json(START_LOCAL, rec)
        pub_name = P.run_record_name('start', PHASE, part or None, sess)
        shutil.copy(START_LOCAL, os.path.join(OUTROOT, pub_name))
        shutil.copy(START_LOCAL, os.path.join(od, pub_name))
        CTX['session'].update(start_record=pub_name, start_sha256=sha, session_id=sess)
        package('final', {'finished': now()})
        say('[boot_bprime] 起動の記録を書いた（%s・SHA-256 %s）。records/Bprime/runs/ に写して公開の置き場に置き、そのコミットで OP4B_STEP=run を走らせる' % (pub_name, sha))
        return od
    if PHASE != 'check':
        if not os.path.exists(START_LOCAL):
            stop('手元の起動の記録が無い（同じランタイムで start を先に走らせる）')
        START = json.load(open(START_LOCAL, encoding='utf-8'))
        pub_name = P.run_record_name('start', PHASE, part or None, START['session'])
        pub = os.path.join(RECS, 'runs', pub_name)
        if DRY:
            mark('dry_start_unpublished', local=pub_name)
        elif not os.path.exists(pub) or sha256f(pub) != sha256f(START_LOCAL):
            stop('公開の置き場の起動の記録（%s）が手元の起動の記録と違う（写して push してから run を走らせる）' % pub_name)
        if START['phase'] != PHASE or (START.get('part') or '') != part or START['contract_sha16'] != sha16f(CANON) or START['tools_sha16'] != TOOL_SHA:
            stop('起動の記録の相・組・正本と器の SHA が今と違う')
        if not DRY and (START.get('freeze_record_sha16') != sha16f(FRP) or START.get('seal_record_sha16') != sha16f(SRP)):
            stop('起動の記録の凍結と封印の記録の SHA16 が今と違う（start から run の間に記録が変わった・U10）')
        CTX['session'].update(start_record=pub_name, start_sha256=sha256f(START_LOCAL), session_id=START['session'])
        shutil.copy(START_LOCAL, os.path.join(od, pub_name))          # 出力の置き場に起動の記録の写し（閉じる器・凍結の器が出力の置き場で読む・v0.2・K19・名はセッションつき・v0.4）

    # ---- 4. 重みと模型
    from transformers import AutoTokenizer
    if DRY:
        import dry_bprime as DR
        tok = AutoTokenizer.from_pretrained(DR.HF)
        model, _, _ = DR.tiny_model(5, float(os.environ.get('OP4B_DRY_WSCALE', '4.0')), torch.float32)     # 語彙の行列の倍率（DRY だけ・出口の値を大きくした枝・v0.4・U46）
        W_SHA = {}
        C = dry_contract(C, model)                                          # DRY だけ: 小さな模型の形に合わせた正本の写し（正本のファイルは変えない・v0.1）
        mark('dry_contract', layer_index=C['layers']['index'], iso=C['nulls']['isotropic']['count'], max_new=C['inputs']['generation_B']['max_tokens'], wscale=os.environ.get('OP4B_DRY_WSCALE', '4.0'),
             mass_min=C['pilot']['mass_min'], p_bounds=C['pilot']['p_bounds'])
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
    CTX['session'].update(gpu=GPU, versions=VER, determinism=DET, weights_sha256=W_SHA, canon_sha16=sha16f(CANON), tools_sha16=TOOL_SHA,
                          main_freeze_sha16=P.main_freeze_sha16(FR) if FR else None)          # 本の凍結の節の正準の SHA16（集計の器が組の間で照らす・v0.4・U08・U10）
    S = CTX['session']

    def finish(outputs):
        """出力の SHA の記録（end-<相>.json・公開の置き場に置く）を書いて zip にする。"""
        end = {'kind': 'bprime_end_record', 'phase': PHASE, 'part': part or None, 'session': S.get('session_id'), 'time_utc': now(),
               'outputs_sha256': {fn: sha256f(os.path.join(od, fn)) for fn in outputs}, 'clause': CLAUSE}
        end_name = 'end-check.json' if PHASE == 'check' else P.run_record_name('end', PHASE, part or None, S['session_id'])     # 名にセッション（v0.4・U09）
        write_json(os.path.join(od, end_name), end)
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
        if not DRY:
            npz_b = os.environ.get('OP4B_NPZ', os.path.join(OUTROOT, 'in', 'directions-Bprime.npz'))
            items, miss = form_items_check(RECS, S, SR, FR, START, npz_b, TOOL_SHA, sha16f(CANON))
            CTX['session']['form_items'] = items                                  # 形の項目ごとの合否と照らした相（v0.4・U02）
            if miss:
                stop('抽出の記録の形の項目がそろわない（器の誤りとして止める・正本 `computation.extraction_record.check`）: %s' % miss)
        else:
            mark('dry_form_items', note='DRY の相 behavior は形の項目を照らさない（合成データの確かめの器が form_items_check を合成の置き場で直に呼ぶ・v0.4）')
        batch = (FR or {}).get('prefreeze', {}).get('behavior_batch') or (os.environ.get('OP4B_DRY_BATCH', '8') if DRY else None)
        if batch is None:
            stop('凍結の記録に行動の下見の生成のバッチの大きさが無い（既定の値は DRY だけ・U19）')
        batch = int(batch)
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
        if not (CLOSED_P and os.path.exists(CLOSED_P)):
            stop('行動の下見の閉じた記録が無い（正本 `behavior_pilot.order`・U12）')
        closed = json.load(open(CLOSED_P, encoding='utf-8'))
        cbad = [x for x, ok_ in (('種類', closed.get('kind') == 'bprime_behavior_closed'), ('起動の記録の SHA16', sha16f(CLOSED_P) == START.get('closed_record_sha16')),
                                 ('正本の SHA16', DRY or closed.get('contract_sha16') == sha16f(CANON))) if not ok_]
        if not DRY:
            for k_ in ('start_record', 'end_record'):
                r_ = closed.get(k_) or {}
                rp_ = os.path.join(RECS, 'runs', r_.get('file') or '-')
                if not os.path.exists(rp_) or sha256f(rp_) != r_.get('sha256'):
                    cbad.append('閉じた記録が指す %s が公開の置き場の runs と違う' % k_)
        if cbad:
            stop('行動の下見の閉じた記録の照らしが外れた（正本 `behavior_pilot.order`「その記録の SHA を確かめてから進む」・U12）: %s' % cbad)
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
    kz = (FR or {}).get('prefreeze', {}).get('logit_k') or ({'k': 1.0, 'z0': 4} if DRY else None)
    if kz is None:
        stop('凍結の記録に出口の値の自己検査の k が無い（既定の値は DRY だけ・U19）')
    CTX['session']['directions_npz_sha256'] = sha256f(npz_in)             # 方向の npz の SHA-256（集計の器が組の間と抽出の記録で照らす・v0.4・U08）
    keys = ['%s|%s' % (sc, arm) for sc, arm in C['cells_main']]
    if part in ('rewrite', 'reextract'):
        try:                                                                      # 別の個体の器が読めることを始めに確かめる（公開の置き場の tools/ に移し方の表が写す・v0.4・U42）
            import bprime_recompute_rewrite as RW
            import bprime_reextract as RX
        except ImportError as e_:
            stop('別の個体の器が読めない（公開の置き場の tools/ に無い・移し方の表を確かめる・U42）: %s' % e_)
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
        elif part in ('rewrite', 'reextract'):
            try:                                                                  # 別の個体の器は、止めを SystemExit で上げる（中は変えない）。器の誤りとして受けて記録を残す（v0.4・U43）
                if part == 'rewrite':
                    out['result'] = RW.recompute_rewrite(model, tok, C, L, dirs, names, pil, float(EX['coefficient']))
                else:
                    out['result'] = RX.reextract_all(model, tok, C, L, dirs)      # 正本 `independent_recompute.interfaces.reextract` の口（v0.1）
            except SystemExit as e_:
                out['tool_error'] = '別の個体の器が止めた（SystemExit）: %s' % e_
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
    等方の本数（OP4B_DRY_ISO・既定 9）と生成の上限（OP4B_DRY_MAX_NEW・既定 12）を小さくし、読み取りの下見の (i)(ii) の門（`pilot.mass_min`・`pilot.p_bounds`）を開ける
    （小さな乱数の模型は選択肢の質量が下限に届かないので、門がそのままでは下見が「止める」になり、本の計算の相から後を通せない・`dry_bprime.py` の P1 と同じ置き換え・v0.3）。ほかの鍵は変えない。
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
    Cd['pilot'] = dict(Cd['pilot'], mass_min=0.0, p_bounds=[0.0, 1.0])
    Cd['dry_contract'] = 'DRY の写し（層の添字・等方の本数・生成の上限・下見の (i)(ii) の門だけを小さな模型に合わせた・模型の事実は本物の値のまま）'
    return Cd


def _t(x):
    """時刻の文字列（ISO・'Z' か '+hh:mm' つき）→ 時刻（時差つき）。時差の無い文字列は止める（封印の記録は +09:00 と +00:00・起動器は Z でそろっていない・U02）。"""
    t = datetime.datetime.fromisoformat(str(x).replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('時差の無い時刻: %s' % x)
    return t


def form_items_check(RECS, S, SR, FR, START, npz_path, tools_now, canon16, phase='behavior'):
    """抽出の記録の形の項目（正本 `computation.extraction_record.form_items` の六つ）を機械で照らす。値（‖v̂‖・係数・転記行 D の記述）は読まない。
    RECS: 公開の置き場の records/Bprime・S: 今の session（版と重みの SHA）・SR: 封印の記録・FR: 凍結の記録（台帳）・START: 今の相の起動の記録・
    npz_path: 手元の方向の npz・tools_now: 今の器の閉包の SHA16 の表・canon16: 今の正本の SHA16。
    戻り値: (items, bad)。items は項目ごとの合否と照らした相（session に書く）・bad は外れの文の並び。本番の相 behavior と合成データの確かめが同じ関数を呼ぶ（v0.4・U02）。
    SHA はバイトで取る（改行を訳さない・U32）。"""
    import bl3_core as K_
    import bprime_core as Pc
    items, bad = collections.OrderedDict(), []

    def put(i, ok, why):
        items['item%d' % i] = collections.OrderedDict([('pass', bool(ok)), ('phase', phase), ('why', None if ok else why)])
        if not ok:
            bad.append('形の項目 %d: %s' % (i, why))

    exp = os.path.join(RECS, 'extract', 'extraction-record-Bprime.json')
    R = json.load(open(exp, encoding='utf-8')) if os.path.exists(exp) else None
    # 1. 公開した抽出の記録がそろい、転記行 D・npz の SHA・係数・g との一致の合否の欄がある
    need = ('row_D', 'npz_sha256', 'coefficient', 'g_match', 'checks', 'start_record_sha256', 'session', 'time_utc', 'versions', 'weights_sha256')
    miss = ['公開した抽出の記録が無い'] if R is None else [k for k in need if k not in R]
    put(1, not miss, '欄がそろわない: %s' % miss)
    if miss:
        for i in range(2, 7):
            put(i, False, '項目 1 が落ちたので照らせない')
        return items, bad
    # 相 extract の走行（runs の起動の記録と出力の SHA の記録）
    runs = os.path.join(RECS, 'runs')
    names = {fn: sha256f(os.path.join(runs, fn)) for fn in (sorted(os.listdir(runs)) if os.path.isdir(runs) else [])}
    try:
        tab = [r for r in Pc.runs_table(names) if r['phase'] == 'extract']
        terr = None
    except Pc.ToolError as e_:
        tab, terr = [], str(e_)
    starts = [r for r in tab if r['start']]
    point = [r for r in starts if r['start']['sha256'] == R['start_record_sha256']]
    st = json.load(open(os.path.join(runs, point[0]['start']['file']), encoding='utf-8')) if len(point) == 1 else None
    en = json.load(open(os.path.join(runs, point[0]['end']['file']), encoding='utf-8')) if (len(point) == 1 and point[0]['end']) else None
    # 2. 公開した記録と手元の npz と正本と器と重みの断片の SHA が合う
    w2 = []
    if not (npz_path and os.path.exists(npz_path) and sha256f(npz_path) == R['npz_sha256']):
        w2.append('手元の npz が無いか、SHA-256 が抽出の記録と違う')
    if en is None or (en.get('outputs_sha256') or {}).get('extraction-record-Bprime.json') != sha256f(exp) or (en.get('outputs_sha256') or {}).get('directions-Bprime.npz') != R['npz_sha256']:
        w2.append('公開した抽出の記録と npz の SHA-256 が、相 extract の出力の SHA の記録（runs/end-extract-*）と違う')
    if st is None or st.get('contract_sha16') != canon16:
        w2.append('相 extract の起動の記録の正本の SHA16 が今と違う')
    if st is None or set(st.get('tools_sha16') or {}) != set(tools_now or {}):
        w2.append('相 extract の起動の記録の器の閉包が今と違う')
    else:
        dn = st.get('deviations_n')
        ch = K_.ledger_chain_bad(st['tools_sha16'], tools_now, list((FR or {}).get('deviations') or [])[int(dn or 0):], paths=list(st['tools_sha16']))
        if dn is None or ch:
            w2.append('相 extract の起動の記録の器の SHA16 から今まで、台帳の器の差分でつながらない: %s' % (ch or '起動の記録に台帳の行の数が無い'))
    if not (R['weights_sha256'] and R['weights_sha256'] == S.get('weights_sha256')):
        w2.append('重みの断片の SHA が合わない')
    put(2, not w2, '・'.join(w2))
    # 3. 版のピンが文字列で完全に一致する
    put(3, R['versions'] == S.get('versions'), '版のピンが文字列で一致しない')
    # 4. 凍結した確かめの合否がすべて「通った」
    four = ('g_match', 'norms_finite_nonzero', 'dim_match', 'no_readout')
    put(4, isinstance(R['checks'], dict) and all(k in R['checks'] for k in four) and all(v is True for v in R['checks'].values()),
        '凍結した確かめの合否がすべて「通った」でない（欄が欠けるか、真でない値がある）')
    # 5. 時刻が封印の後で行動の下見の起動の前
    try:
        ok5 = _t(SR['sealed_at_utc']) < _t(R['time_utc']) < _t(START['time_utc'])
        w5 = '抽出の記録の時刻が封印の後で行動の下見の起動の前でない'
    except (KeyError, TypeError, ValueError) as e_:
        ok5, w5 = False, '時刻が読めない: %s' % e_
    put(5, ok5, w5)
    # 6. 相 extract の起動の記録が一つで、抽出の記録が指す走行と同じ（二つあるときは器の誤りの記録がある）
    if terr:
        ok6, w6 = False, terr
    elif len(point) != 1 or st is None or st.get('session') != R['session'] or st.get('phase') != 'extract':
        ok6, w6 = False, '抽出の記録が指す相 extract の起動の記録が runs に一つ無いか、セッションが違う'
    elif len(starts) == 1:
        ok6, w6 = True, None
    else:
        tm = {id(r): _t(json.load(open(os.path.join(runs, r['start']['file']), encoding='utf-8'))['time_utc']) for r in starts}
        others = [r for r in starts if r is not point[0]]
        err = [r for r in others if not (r['end'] and 'extract-tool-error.json' in (json.load(open(os.path.join(runs, r['end']['file']), encoding='utf-8')).get('outputs_sha256') or {}))]
        nre = Pc.reruns_of((FR or {}).get('deviations') or []).get('extract', 0)
        ok6 = max(starts, key=lambda r: tm[id(r)]) is point[0] and not err and nre >= len(starts) - 1
        w6 = '相 extract の起動の記録が %d あり、抽出の記録が最後の走行を指さないか、ほかの走行に器の誤りの記録が無いか、台帳のやり直しの行（extract_rerun）が %d で足りない' % (len(starts), nre)
    put(6, ok6, w6)
    return items, bad

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
