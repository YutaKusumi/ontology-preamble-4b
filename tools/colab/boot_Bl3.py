# -*- coding: utf-8 -*-
"""boot_Bl3.py v4 —— B-lens 層三（Bl3）の Colab 起動スクリプト（教師強制の順伝播・2026-09-25・正本 `readout`・`pilot`・`computation`・`independent_recompute`）。

相（OP4B_PHASE）:
  check  封印の前の確かめ（正本 `computation.before_seal`: 読み込みと版の確かめだけ・**順伝播を一度も走らせない・値を出さない**。模型の順伝播の前の hook で、呼ばれたら止める）:
         コミット固定の取り出し・版（正本 `inputs.versions_B`・文字列の完全な一致・torch は CUDA の組みまで・裁定 D187）・GPU・重みの断片の SHA-256（転記行 F）・
         方向の npz の SHA-256（方向の記録）と組ごとの SHA-256（転記行 D）・模型の読み込みと設定（正本 `inputs.model`）・選んだ層の添字（正本 `layers.indices`）・
         升目の入力（実トークナイザの組み立てを転記行 B と）・升目と符号の組と独立の再計算の組の順伝播の数（転記行 E と）・門の行（転記行 C の数と）・
         乙の行と文脈（B-lens の選んだ出力の一覧の SHA16 と、全ての文脈を組めること）・加減の hook を掛けて外せること・残差の書き換えの器が import できること。
  pilot  封印の後: 下見の前の凍結の記録と封印の記録がそろったコミットで、凍結の記録の SHA16 を取り出した器と正本に照らしてから、正本 `pilot.order` の順に走らせ、
         下見の記録（`bl3_run.run_pilot` の出力）を置く。器の誤り（凍結した確かめが機械で落ちた）は、その文を記録に置いて止める（正本 `pilot.decision.tool_error`）。
  main   本の凍結の後: 凍結の記録に足した下見の記録（バッチの大きさ・揺れの床・近道の許容・近道・外した升目）のまま、組（OP4B_PART・DRY でないときは組を一つずつ与える・裁定 D239・DRY の既定は三つとも順に）を走らせる:
           main       本の計算の頭（出口の値・最後の層）→ 全ての升目と符号（`bl3_run.run_main_phase`・近道を使わない・裁定 D234）
           recompute  独立の再計算の二つの道（本の器のフック〔`bl3_run.recompute_hook_path`〕・残差の書き換え〔別の個体の器 `bl3_recompute_rewrite`〕・近道なし・バッチ一）
           secondary  乙（`bl3_run.run_secondary`・裁定 D227）
         どの組も頭で出口の値の自己検査を走らせる。**効き目の値は印字しない**（札・門・二段の一致は手元の集計の器が出し、一致か不一致かだけを先に見る・正本
         `independent_recompute.print`）。器の誤りは、その文を組の出力に置いて止める（正本 `computation.tool_error`）。組の出力は出来たときに置く。
止める条件（外れたら止める・登録者に相談）: 版の不一致（入れ直した後にランタイムの再起動を求める）・GPU・重みの SHA-256・方向の npz の SHA-256・凍結の記録の SHA16 と
  取り出した器と正本の不一致・取り出した作業木の変更・模型の設定・升目の入力と転記行 B の不一致・順伝播の数と転記行 E の不一致・乙の文脈を組めない・凍結と封印の記録の欠け・器の誤り。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する（ランタイムの選択と結果の zip のダウンロードもコーディネータ）。登録者の手に残すのは同意と支払い。
  資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。Drive は使わない（出力は小さく、終わりに zip を落とす）。セルの出力の表示が固まることがあるので、
  進みは出力の置き場の `progress.log` にも書く（ターミナルで見る）。ランタイムが落ちたら、落ちた組から新しいランタイムで走らせ直す（同じ GPU の種類・逸脱の台帳に記す）。
セルに打つ一行（先頭の下線は type の事故の緩衝・<commit> は 40 桁・相 main の組を分けるときは OP4B_PART を足す）:
  ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='check';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_Bl3.py').read())
DRY（手元の検査・OP4B_DRY=1）: 乱数の小さな模型（`tools/dry_run_Bl3.py` の作り方と読み取りの集合の行の置き直し）と実トークナイザ・合成の方向（実の名だけを借りる）で、
  三つの相を CPU で通す。OP4B_REPO_DIR・OP4B_OUT が要る。版・GPU・重み・凍結と封印の記録は見ない（印を残す）。方向の npz の確かめは手元の npz で行う。
  相 main は OP4B_DRY_PILOT（相 pilot の出力の pilot.json）を読む。OP4B_DRY_ISO で等方の本数（既定 9）、OP4B_DRY_SEC で乙の文脈の数（既定 2）、
  OP4B_DRY_RC で独立の再計算の v̂ の行の数（既定 2・減算の行と加算の行を一つずつから）を減らす。残差の書き換えの器が無ければ、DRY に限り印を残して飛ばす。
v3 の決め（裁定 D236）: 手順の順は「方向の npz と器を push → 相 check → 下見の前の凍結の記帳」（npz が取り出しに無ければ止める）。版は numpy・torch・transformers の三つを
  文字列で照らす（計算の道は scipy を読まないので照らさない・session に並べる・裁定 D237）。相 check の守りは模型・模型の本体・語彙の行列・各層の前の hook で、呼ばれた数を数えて
  書く（守りの止めは Exception の外の型）。相 pilot と main は、そのコミットの二つの予想の SHA-256 を封印の記録と照らす。相 main は組ごとに出力の SHA-256 を session に書き、
  組ごとに zip を作って落とす（落ちた組から走らせ直せるように）。止めと予期しない誤りでも session を書いて zip を作る。
柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, time, glob, shutil, hashlib, datetime, traceback, subprocess, zipfile, collections

VERSION = 'v4'          # v4（2026-09-26・裁定 D239）: 版の照らしで台帳の器の差分をつなげて許す・相 main で封印の記録を本の凍結の記録と照らす・zip の SHA-256 の並びを別のファイルに書く・DRY でない相 main は組を一つずつ・DRY に限る守りの試し／v3（2026-09-25・裁定 D236）: 封印した予想の照らし・組の出力の SHA-256・組ごとの zip・止めと誤りの記録・相 check の守りと数・トークンの並びの SHA16 ほか／v2（裁定 D231・D234）
T0 = time.time()
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
PHASES = ('check', 'pilot', 'main')
PARTS = ('main', 'recompute', 'secondary')
SPARSE = ['tools', 'arms', 'design', 'records', 'results/Bl3', 'results/stageB']
LOG = []
PROGRESS = {'path': None}
CTX = {'od': None, 'session': None, 'dry': False}          # 止めと誤りでも記録を置くため（裁定 D236）
CLAUSE = '本記録は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


class Stop(BaseException):
    """相 check の守りの止め（Exception の外の型で、`except Exception` に呑まれない・裁定 D236）。"""


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


def say(line):
    print(line, flush=True)
    if PROGRESS['path']:
        with open(PROGRESS['path'], 'a', encoding='utf-8') as fh:
            fh.write(line + '\n')


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
    say('[boot_Bl3] %-16s %7.0fs %s' % (step, time.time() - T0, kw or ''))


def sh(cmd, check=True):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-3000:])
        raise RuntimeError('失敗: %s' % cmd)
    return r


def package(tag, extra=None):
    """置き場の中身を zip にして落とす（組ごと・終わり・止め・誤り・裁定 D236）。session を書いてから zip にし、zip の SHA-256 を session と進みの印字に記す。"""
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
    write_json(od + '-zips.json', {'zips': S['zips'], 'clause': CLAUSE})      # 最後の zip の SHA-256 も手元に残す（zip の外の小さなファイル・裁定 D239）
    mark('packaged', tag=tag, zip=os.path.basename(zp), sha256=zsha)
    if not CTX['dry']:
        try:
            from google.colab import files
            files.download(zp)
        except Exception as e_:
            print('[boot_Bl3] zip の自動のダウンロードが走らなかった（左の「ファイル」から落とす）: %s' % e_)
    return zp


def stop(msg):
    mark('stop', reason=msg)
    package('stopped', {'stopped': msg})               # 止めでも session を書いて zip を作る（裁定 D236）
    sys.exit('[boot_Bl3] 止める（登録者に相談）: ' + msg)


def jdefault(o):
    """numpy の数と配列を JSON に（値の丸めはしない）。"""
    if hasattr(o, 'tolist'):
        return o.tolist()
    if hasattr(o, 'item'):
        return o.item()
    raise TypeError(type(o))


def write_json(path, obj):
    json.dump(obj, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=jdefault)
    return sha16f(path)


def verify_frozen(repo, sha_map, deviations=()):
    """凍結の記録の SHA16（改行を LF にそろえた SHA-256 の頭 16 桁）を、取り出した作業木のファイルに照らす。疎な取り出しの外のファイルは飛ばして数を記し、
    内側で無いファイルは外れにする（裁定 D236）。凍結の後に台帳に記した器の差分は、路ごとに前後をつなげて許す（芯の `ledger_chain_bad`・裁定 D239）。
    deviations には sha_map を決めた後に記した台帳の行だけを与える。戻り値: 外れの並び（文字列）と、飛ばした置き場の並び。"""
    if os.path.join(repo, 'tools') not in sys.path:
        sys.path.insert(0, os.path.join(repo, 'tools'))
    import bl3_core as K_
    now, skipped = {}, []
    for rp in sha_map:
        p = os.path.join(repo, *rp.split('/'))
        if os.path.exists(p):
            now[rp] = sha16f(p)
        elif any(rp == d or rp.startswith(d + '/') for d in SPARSE):
            now[rp] = None
        else:
            skipped.append(rp)
    return K_.ledger_chain_bad(sha_map, now, list(deviations), paths=[rp for rp in sha_map if rp not in skipped]), skipped


def pick_recompute_rows(rows, n):
    """DRY の独立の再計算の行: 減算の行と加算の行を一つずつから、足りなければ前から足す（本の計算では全ての行）。"""
    idx = [i for i, r in enumerate(rows) if r[2] < 0][:1] + [i for i, r in enumerate(rows) if r[2] > 0][:1]
    idx += [i for i in range(len(rows)) if i not in idx]
    return [rows[i] for i in sorted(idx[:n])]


def run():
    PHASE = os.environ.get('OP4B_PHASE', 'check')
    COMMIT = os.environ.get('OP4B_COMMIT', '')
    DRY = os.environ.get('OP4B_DRY') == '1'
    if PHASE not in PHASES:
        sys.exit('[boot_Bl3] 相は %s のどれか' % '・'.join(PHASES))
    if not DRY:
        stray = sorted(k for k in os.environ if k.startswith('OP4B_DRY_') or k in ('OP4B_REPO_DIR', 'OP4B_OUT'))
        if stray:
            sys.exit('[boot_Bl3] DRY でないのに検査用の環境変数がある: %s（外してから走らせる）' % '・'.join(stray))
        if not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
            sys.exit('[boot_Bl3] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
    given = [p.strip() for p in os.environ.get('OP4B_PART', ','.join(PARTS)).split(',') if p.strip()]
    if PHASE == 'main' and (not given or any(p not in PARTS for p in given)):
        sys.exit('[boot_Bl3] OP4B_PART は %s の組み合わせ（コンマで区切る）' % '・'.join(PARTS))
    if PHASE == 'main' and not DRY and ('OP4B_PART' not in os.environ or len(given) != 1):
        sys.exit('[boot_Bl3] DRY でない相 main は組を一つずつ走らせる（OP4B_PART に組を一つ与える・裁定 D239）')
    parts = [p for p in PARTS if p in given] if PHASE == 'main' else []
    print('[boot_Bl3] %s 開始 phase=%s %s%s' % (VERSION, PHASE, 'DRY' if DRY else COMMIT, (' parts=' + ','.join(parts)) if parts else ''), flush=True)

    # ---- 1. リポジトリ（コミット固定）と出力の置き場
    if DRY:
        REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
        OUTROOT = os.path.abspath(os.environ['OP4B_OUT'])
    else:
        REPO, OUTROOT = '/content/ontology-preamble-4b', '/content/op4b-Bl3'
        head_ok = os.path.isdir(os.path.join(REPO, '.git')) and sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
        if not head_ok:
            shutil.rmtree(REPO, ignore_errors=True)
            sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
            sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone'] + SPARSE)
            sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
        if sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() != COMMIT:
            stop('取り出したコミットが OP4B_COMMIT と違う')
        dirty = sh(['git', '-C', REPO, 'status', '--porcelain'], check=False).stdout.strip()
        if dirty:
            stop('取り出した作業木に変更がある: %s' % dirty.splitlines()[:5])
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    od = os.path.join(OUTROOT, '%s-%s' % (PHASE, stamp))
    os.makedirs(od, exist_ok=True)
    PROGRESS['path'] = os.path.join(od, 'progress.log')
    CTX.update(od=od, dry=DRY, session={'kind': 'bl3_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY})
    CANON = os.path.join(REPO, 'design', 'contrasts-Bl3.json')
    T3 = json.load(open(CANON, encoding='utf-8'))
    FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
    FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
    FRP = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
    SRP = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
    FR, frozen = None, None
    if PHASE in ('pilot', 'main'):
        if DRY:
            mark('dry_no_gate', note='DRY は凍結と封印の記録を見ない')
        else:
            for p in (FRP, SRP):
                if not os.path.exists(p):
                    stop('相 %s は下見の前の凍結と封印の後に走らせる（%s が無い・正本 predictions.when）' % (PHASE, os.path.basename(p)))
            FR = json.load(open(FRP, encoding='utf-8'))
            SR = json.load(open(SRP, encoding='utf-8'))
            for role in ('coordinator', 'registrant'):                 # 封印した予想の SHA-256 を封印の記録と照らす（裁定 D236）
                pp = os.path.join(REPO, *SR['predictions'][role]['path'].split('/'))
                if not os.path.exists(pp) or sha256f(pp) != SR['predictions'][role]['sha256']:
                    stop('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
            if PHASE == 'main' and 'main_freeze' not in FR:
                stop('相 main は本の凍結の後に走らせる（凍結の記録に本の凍結が無い）')
            if PHASE == 'main' and sha16f(SRP) != ((FR['main_freeze'].get('seal') or {}).get('record_sha16')):
                stop('封印の記録の SHA16 が、本の凍結の記録に写した値と違う（裁定 D239）')
            sha_map = FR['main_freeze']['frozen_sha16'] if PHASE == 'main' else FR['frozen_sha16']
            devs = (FR.get('deviations') or [])[int(FR['main_freeze'].get('deviations_n') or 0):] if PHASE == 'main' else (FR.get('deviations') or [])
            bad, skipped = verify_frozen(REPO, sha_map, devs)
            frozen = {'checked': len(sha_map) - len(skipped), 'skipped': skipped, 'bad': bad}
            if bad:
                stop('凍結の記録の SHA16 と取り出したファイルが違う: %s' % bad)
            mark('frozen', checked=frozen['checked'], skipped=len(skipped))
    mark('repo', commit=COMMIT[:12] or 'dry', canon=T3['version'], canon_sha16=sha16f(CANON), out=od)

    # ---- 2. 版（正本 inputs.versions_B）と GPU
    import importlib.metadata as md

    def ver(k):
        try:
            return md.version(k)
        except Exception:
            return None
    PIN = T3['inputs']['versions_B']
    VER = {k: ver(k) for k in ('numpy', 'scipy', 'torch', 'transformers', 'torchvision', 'torchaudio', 'tokenizers', 'huggingface_hub', 'accelerate', 'safetensors')}
    want = {'numpy': PIN['numpy'], 'torch': PIN['torch'], 'transformers': PIN['transformers']}
    bad_v = {k: VER[k] for k, v in want.items() if VER[k] != v}          # 文字列の完全な一致（torch は CUDA の組みまで・裁定 D187）
    if bad_v and not DRY:
        mark('pin', installing=bad_v)
        os.environ['HF_HUB_DISABLE_XET'] = '1'
        if 'torch' in bad_v:
            cuda = PIN['torch'].split('+')[1]
            pk = ['torch==%s' % PIN['torch']] + ['%s==%s+%s' % (c, VER[c].split('+')[0], cuda) for c in ('torchvision', 'torchaudio') if VER.get(c)]
            sh([sys.executable, '-m', 'pip', 'install', '-q'] + pk + ['--index-url', 'https://download.pytorch.org/whl/%s' % cuda])
        sh([sys.executable, '-m', 'pip', 'install', '-q', 'numpy==%s' % want['numpy'], 'transformers==%s' % want['transformers'], 'accelerate', 'huggingface_hub', 'safetensors'])
        print('[boot_Bl3] 版を入れ直した。**ランタイムを再起動して（「ランタイム」→「セッションを再起動」）、同じ一行をもう一度走らせる**', flush=True)
        sys.exit(0)
    GPU = 'dry'
    if not DRY:
        GPU = sh('nvidia-smi --query-gpu=name --format=csv,noheader', check=False).stdout.strip().split('\n')[0]
        if 'L4' not in GPU and 'A100' not in GPU:
            stop('GPU %s は登録の環境（Colab L4・A100 は予備）に無い' % GPU)
    mark('versions', versions=VER, gpu=GPU)

    import numpy as np
    import torch
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    sys.path.insert(0, os.path.join(REPO, 'tools', 'colab'))
    import direction_B
    import run_stageB_local as RB
    import bl3_core as K
    import bl3_run as BR
    import bl3_directions as BD
    import analyze_Bl3 as AZ
    from transformers import AutoTokenizer, AutoModelForCausalLM

    # ---- 3. 重み（転記行 F の SHA-256 と突き合わせる）
    M = T3['inputs']['model']
    W_SHA = {}
    if DRY:
        import dry_run_Bl3 as DR
        SNAPDIR = os.environ.get('OP4B_TOKENIZER_DIR') or DR.SNAP
    else:
        os.environ['HF_HUB_DISABLE_XET'] = '1'
        from huggingface_hub import snapshot_download
        SNAPDIR = snapshot_download(M['repo'], revision=M['rev'])
        idx = json.load(open(os.path.join(SNAPDIR, 'model.safetensors.index.json'), encoding='utf-8'))
        need_f = ['config.json', 'tokenizer.json', 'model.safetensors.index.json'] + sorted(set(idx['weight_map'].values()))
        miss_f = [x for x in need_f if x not in FJ['facts']['F']['sha256']]
        if miss_f:
            stop('転記行 F に、重みの索引の断片か設定のファイルが欠けている: %s' % miss_f)      # 裁定 D236
        W_SHA = {fn: sha256f(os.path.join(SNAPDIR, fn)) for fn in FJ['facts']['F']['sha256']}
        badw = [fn for fn, sha in FJ['facts']['F']['sha256'].items() if W_SHA[fn] != sha]
        if badw:
            stop('重みの SHA-256 が転記行 F と違う: %s' % badw)
    mark('weights', snapshot=os.path.basename(SNAPDIR), checked=len(W_SHA))

    # ---- 4. 方向の npz（方向の記録の SHA-256・組ごとの SHA-256 を転記行 D と・Colab で乱数を引き直さない）
    NPZ = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.npz')
    DJP = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json')
    if not os.path.exists(NPZ) or not os.path.exists(DJP):
        stop('方向の npz か方向の記録が取り出しに無い（npz と器を push してから相 check を走らせる・裁定 D236）')
    DJ = json.load(open(DJP, encoding='utf-8'))
    npz_sha = sha256f(NPZ)
    if npz_sha != DJ['npz_sha256']:
        stop('方向の npz の SHA-256 が方向の記録と違う')
    if FR is not None and npz_sha != FR.get('directions_npz_sha256'):
        stop('方向の npz の SHA-256 が凍結の記録と違う')
    Zd = np.load(NPZ)
    try:
        grp = BD.verify_against_facts({g: Zd[g] for g in BD.GROUPS}, FJ)
        dirs_real, names_real = BR.load_dirs(NPZ, DJP, T3, FJ)             # 名の並びを正本と転記行 D に照らす（裁定 D236）
    except (SystemExit, BR.ToolError) as e_:
        stop(str(e_))
    pair_names = list(DJ['groups']['real']['names'])
    mark('directions', npz_sha256=npz_sha[:16], groups={k: v[:16] for k, v in grp.items()}, n=len(dirs_real))

    # ---- 5. 模型とトークナイザ
    tok = AutoTokenizer.from_pretrained(SNAPDIR)
    if DRY:
        model, cfg = DR.tiny_model()
        dev = 'cpu'
    else:
        model = AutoModelForCausalLM.from_pretrained(SNAPDIR, torch_dtype=torch.bfloat16, device_map='cuda').eval()
        cfg = model.config
        dev = 'cuda'
        got = {'num_hidden_layers': cfg.num_hidden_layers, 'hidden_size': cfg.hidden_size, 'vocab_size': cfg.vocab_size, 'rms_norm_eps': cfg.rms_norm_eps,
               'tie_word_embeddings': cfg.tie_word_embeddings, 'tokenizer_len': len(tok)}
        if got != {k: M[k] for k in got}:
            stop('模型の設定が正本 inputs.model と違う: %s' % {k: (got[k], M[k]) for k in got if got[k] != M[k]})
    L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
    if not DRY and L != T3['layers']['indices'][str(T3['layers']['selected_ratio'])]:
        stop('選んだ層の添字が正本 layers.indices と違う: %d' % L)
    coef = float(T3['layers']['coef_applied'])
    mark('model', dry=DRY, layers=cfg.num_hidden_layers, layer_idx=L, coef=coef, dtype=str(next(model.parameters()).dtype), device=dev)

    # ---- 6. 升目の入力（凍結の組み立ての関数と転記行 A の書き出し・転記行 B と突き合わせる）
    cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
    gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
    gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in gate_only})
    try:
        cells = BR.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
    except BR.ToolError as e_:
        stop(str(e_))
    mark('cells', main=len(cell_keys), gate_only=len(gate_only_cells))

    SESSION = {'kind': 'bl3_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY, 'gpu': GPU, 'versions': VER, 'weights_sha256': W_SHA,
               'canon_sha16': sha16f(CANON), 'directions_npz_sha256': npz_sha, 'directions_group_sha256': grp, 'frozen_check': frozen, 'layer_idx': L, 'coef': coef}
    CTX['session'] = SESSION

    def finish(extra=None):
        package('final', dict(extra or {}, finished=now()))
        mark('done', zips=len(SESSION.get('zips') or []))
        return od

    # ---- 7. 相 check（順伝播を一度も走らせない）
    if PHASE == 'check':
        calls = collections.Counter()

        def guard_of(name):
            def h(m, a):
                calls[name] += 1
                raise Stop('相 check で順伝播が呼ばれた（%s・正本 computation.before_seal）' % name)
            return h
        guards = [model.register_forward_pre_hook(guard_of('model')), model.model.register_forward_pre_hook(guard_of('model.model')),
                  model.lm_head.register_forward_pre_hook(guard_of('lm_head'))] + [l_.register_forward_pre_hook(guard_of('layers.%d' % i_)) for i_, l_ in enumerate(model.model.layers)]
        if DRY and os.environ.get('OP4B_DRY_GUARD_TEST') == '1':      # 守りが止めることの確かめ（DRY に限る・合成データの器が使う・Exception で呑めない・裁定 D239）
            try:
                model.model(input_ids=torch.zeros((1, 2), dtype=torch.long))
            except Exception:
                pass
        E = FJ['facts']['E']
        sets = BR.cell_sign_sets(T3, None, names_real['named'], names_real['B_random'], names_real['iso'], names_real['real'], gate_only)
        n_pass = sum(len(s[3]) for s in sets)
        if n_pass != E['passes_main'] + E['passes_gate_extra'] + E['passes_orient_extra']:
            stop('升目と符号の組の順伝播の数が転記行 E と違う: %d' % n_pass)
        rows_rc, dbr = K.recompute_set(T3['main_rows'], pair_names, T3['nulls']['real']['swap_siblings'], T3['nulls']['isotropic']['count'])
        n_rc = sum(1 + len(v) for v in dbr.values())
        if 2 * n_rc != E['passes_recompute'] or any(1 + len(v) != E['per_row_recompute'] for v in dbr.values()):
            stop('独立の再計算の組の順伝播の数が転記行 E と違う: %d' % n_rc)
        AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
        rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader(REPO))
        if len(rows_gate) != T3['gate']['rows_gate'] or sorted(r['name'] for r in rows_gate) != sorted(FJ['facts']['C']['style_share_pt']):
            stop('門の行が転記行 C と違う: %d' % len(rows_gate))
        sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
        cnt = AZ.secondary_counts(FB, sec_rows)
        try:
            ctx = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
        except BR.ToolError as e_:
            stop(str(e_))
        try:
            anchor = K.comparator_anchor(pair_names, T3['nulls']['real']['swap_siblings'], K.blens_own_pair())      # 比べる相手の除き方の錨（裁定 D231）
        except ValueError as e_:
            stop(str(e_))
        vn = float(np.linalg.norm(dirs_real['static']))
        if abs(vn - FJ['facts']['D']['vhat_norm']) > 1e-9 * FJ['facts']['D']['vhat_norm']:
            stop('‖static‖ が転記行 D の値と違う: %r' % vn)
        if len(ctx) != cnt['contexts']:
            stop('乙の文脈の数が B-lens の選んだ出力の数と違う: %d' % len(ctx))
        if (cnt['row_passes'], cnt['sign_batches'], cnt['contexts']) != (E['passes_secondary'], E['batches_secondary'], E['contexts_secondary']):
            stop('乙の順伝播の数が転記行 E と違う: %s' % cnt)
        V0 = np.zeros((1, cfg.hidden_size), dtype=np.float32)
        try:
            h_ = RB.register_hook(model, L, RB.make_hook(V0, coef, 1, [0], meta={'bl3': 'check'}))
            h_.remove()
            RB.assert_no_hooks(model, L)
        except SystemExit as e_:
            stop('加減の hook を掛けて外せない: %s' % e_)
        try:
            import bl3_recompute_rewrite as RW
            rw_ok = hasattr(RW, 'recompute_rewrite')
        except ImportError:
            rw_ok = False
        if not rw_ok and not DRY:
            stop('残差の書き換えの器（tools/bl3_recompute_rewrite.py の recompute_rewrite）を import できない')
        for g_ in guards:
            g_.remove()
        chk = {'cells': {k: {'prompt_len': len(c.prompt), 'main_position': c.mp, 'readout_position': c.ro, 'family': c.fam, 'set_ids': c.set_ids, 'ids_sha16': BR.ids_sha16(c)} for k, c in cells.items()},
               'cell_signs': len(sets), 'passes': n_pass, 'recompute_rows': len(rows_rc), 'recompute_passes_per_path': n_rc, 'gate_rows': len(rows_gate),
               'secondary': dict(cnt, cells=len(sec_rows), letter_token_is_L=sum(1 for c in ctx if c[3]['letter_token_is_L']), max_ids=max(c[3]['n_ids'] for c in ctx)),
               'hook_register_remove': True, 'rewrite_importable': rw_ok, 'forward_calls': sum(calls.values()), 'forward_guards': len(guards),
               'comparator_anchor': anchor, 'static_norm_matches_fact_D': True}
        write_json(os.path.join(od, 'check.json'), chk)
        mark('check', cell_signs=len(sets), passes=n_pass, recompute_rows=len(rows_rc), gate_rows=len(rows_gate), secondary_contexts=len(ctx), rewrite_importable=rw_ok)
        return finish()

    # ---- 8. 走らせる器（DRY は合成の方向と読み取りの集合の行を置き直した乱数の模型）
    if DRY:
        iso_n = int(os.environ.get('OP4B_DRY_ISO', '9') or 9)
        names = {'named': list(names_real['named']), 'B_random': list(names_real['B_random']), 'iso': names_real['iso'][:iso_n], 'real': list(names_real['real']), 'check': ['check']}
        dirs = DR.synth_dirs(cfg.hidden_size, names['named'] + names['B_random'] + names['iso'] + names['real'] + names['check'])
        DR.calibrate_readout_rows(model, BR.Runner(model, T3, L, coef, dirs), cells[cell_keys[0]], FJ)
    else:
        iso_n = None
        dirs, names = dirs_real, names_real
    R = BR.Runner(model, T3, L, coef, dirs)
    TOOL_ERR = (BR.ToolError, SystemExit, AssertionError)

    # ---- 9. 相 pilot
    if PHASE == 'pilot':
        B = FJ['facts']['B']['cells']
        stage_b_rate = {k: B[k]['catastrophe'] / B[k]['n_ok'] for k in cell_keys}
        variants = collections.OrderedDict((k, v['ids']) for k, v in FJ['facts']['A']['variants'].items() if v.get('boundary_ok'))
        try:
            rec = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
        except TOOL_ERR as e_:
            rec = {'tool_error': str(e_), 'n_forward': R.n_forward}
        write_json(os.path.join(od, 'pilot.json'), {'pilot': rec, 'variants_used': list(variants), 'clause': CLAUSE})
        if 'tool_error' in rec:
            finish({'tool_error': rec['tool_error']})
            stop('器の誤りで下見が止まった（正本 pilot.decision.tool_error・直してやり直すかは登録者の裁定）: %s' % rec['tool_error'])
        dec = rec['decision']
        mark('pilot', q1=dec.get('q1'), dropped=dec.get('dropped'), batch=rec.get('batch'), floor=rec.get('floor'), cache_tol=rec.get('cache_tol'),
             shortcut=(rec.get('v') or {}).get('shortcut'), n_forward=R.n_forward)
        return finish()

    # ---- 10. 相 main（組ごとに出力を置く）
    if DRY:
        pilot = json.load(open(os.environ['OP4B_DRY_PILOT'], encoding='utf-8'))['pilot']
    else:
        pilot = FR['main_freeze']['pilot']
        if pilot != FR['main_freeze']['pilot_attempts'][-1]:
            stop('本の凍結の下見の記録と、下見の試みの最後が違う')
    if pilot.get('tool_error') or (pilot.get('decision') or {}).get('stop'):
        stop('凍結の記録の下見の記録が「止める」か器の誤り（本の計算は走らせない）')
    dropped = list((pilot.get('decision') or {}).get('dropped', []))
    first_cell = [cells[k] for k in cell_keys if k not in set(dropped)][0]
    SESSION['pilot_used'] = {k: pilot.get(k) for k in ('batch', 'floor', 'cache_tol')}
    SESSION['pilot_used'].update({'shortcut': (pilot.get('v') or {}).get('shortcut'), 'dropped': dropped})
    SESSION['parts'] = parts
    for part in parts:
        mark('part', part=part)
        out = collections.OrderedDict(part=part, clause=CLAUSE)
        n0 = R.n_forward
        try:
            if part != 'main':                       # どの組も頭で出口の値の自己検査（本の計算の組は run_main_phase の頭で行う）
                lc = R.logit_check(first_cell, T3['computation']['logit_tol'])
                out['logit_check'] = lc
                if not lc['pass']:
                    raise BR.ToolError('出口の値の自己検査が落ちた（組 %s の頭）: %s' % (part, lc))
            if part == 'main':
                MP = BR.run_main_phase(R, T3, FJ, cells, names, pilot, iso_n=None, log=say)
                out.update(MP)
                hd = MP['head']
                mark('main_head', logit_max_abs=hd['logit_check']['max_abs'], shortcut=MP['shortcut'], layer_diff=hd['layer_check']['diff'], cell_signs=len(MP['cells']))
            elif part == 'recompute':
                rows_rc, dbr = K.recompute_set(T3['main_rows'], pair_names, T3['nulls']['real']['swap_siblings'],
                                               len(names['iso']), dropped)
                if DRY:
                    rows_rc = pick_recompute_rows(rows_rc, int(os.environ.get('OP4B_DRY_RC', '2') or 2))
                    dbr = collections.OrderedDict((r[0], dbr[r[0]]) for r in rows_rc)
                out['rows'] = rows_rc
                out['n_iso'] = len(names['iso'])
                t1 = time.time()
                out['hook'] = BR.recompute_hook_path(R, [(n, cells[ck], s) for n, ck, s in rows_rc], dbr, log=say)
                mark('recompute_hook', rows=len(rows_rc), seconds=round(time.time() - t1, 1))
                try:
                    import bl3_recompute_rewrite as RW
                except ImportError:
                    RW = None
                if RW is None:
                    if not DRY:
                        raise BR.ToolError('残差の書き換えの器を import できない')
                    out['rewrite'] = None
                    mark('recompute_rewrite', skipped='DRY で器が無い')
                else:
                    t1 = time.time()
                    # mask の組み方を、本の器のフックの道の近道なし（use_cache=False・明示の mask）にそろえる（個体の開発の記録 `records/Bl3/tools/recompute-rewrite-dev-Bl3.md`）
                    out['rewrite'] = RW.recompute_rewrite(model, tok, T3, FJ, rows_rc, dbr, dirs, L, coef, use_cache=False)
                    mark('recompute_rewrite', rows=len(rows_rc), seconds=round(time.time() - t1, 1))
            elif part == 'secondary':
                AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
                rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader(REPO))
                sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
                ctx = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
                if DRY:
                    n_sec = int(os.environ.get('OP4B_DRY_SEC', '2') or 2)
                    firsts = [c for i, c in enumerate(ctx) if i == 0 or c[0] != ctx[i - 1][0]]
                    ctx = firsts[:n_sec]
                out['rows_by_cell'] = sec_rows
                out['counts'] = AZ.secondary_counts(FB, sec_rows)
                t1 = time.time()
                out['contexts'] = BR.run_secondary(R, ctx, sec_rows, log=say)
                mark('secondary', contexts=len(ctx), seconds=round(time.time() - t1, 1))
        except TOOL_ERR as e_:
            out['tool_error'] = str(e_)
        out['n_forward'], out['n_forward_total'] = R.n_forward - n0, R.n_forward      # 組の順伝播の数と、起動の中の累積（裁定 D236）
        write_json(os.path.join(od, '%s.json' % part), out)
        SESSION.setdefault('part_sha256', {})[part] = sha256f(os.path.join(od, '%s.json' % part))      # 一致だけを見る段が読む組の出力の同定（裁定 D236）
        if 'tool_error' in out:
            finish({'tool_error': out['tool_error'], 'tool_error_part': part})
            stop('器の誤りで組 %s が止まった（正本 computation.tool_error・結果を開かずに登録者に上げる）: %s' % (part, out['tool_error']))
        package('part-%s' % part)                                   # 組ごとに zip を作って落とす（落ちた組から走らせ直せるように・裁定 D236）
    return finish()


if __name__ == '__main__':
    try:
        run()
    except SystemExit:
        raise
    except Stop as e_:
        LOG.append({'step': 'guard', 'at': now(), 'reason': str(e_)})
        package('stopped', {'stopped': str(e_)})
        sys.exit('[boot_Bl3] 止める（相 check の守り・登録者に相談）: %s' % e_)
    except Exception:
        LOG.append({'step': 'crash', 'at': now(), 'traceback': traceback.format_exc()[-4000:]})
        package('crash', {'crash': traceback.format_exc()[-4000:]})       # 予期しない誤りでも session を書いて zip を作る（裁定 D236）
        say('[boot_Bl3] 予期しない誤りで止まった（器の誤りではない・登録者に相談）')
        raise
