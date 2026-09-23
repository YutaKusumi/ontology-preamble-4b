# -*- coding: utf-8 -*-
"""boot_Blens.py v2 —— B-lens の Colab 起動スクリプト（層二の大きさの目盛りの教師強制の順伝播・2026-09-23・正本 `magnitude`・§9）。

相（OP4B_PHASE）:
  check   凍結の前の確かめ（**射影を一つも計算しない・残差のベクトルを置かない**）: 版（正本 `inputs.versions_B`）・GPU・重みの断片の SHA-256（転記行 F）・
          段階 B のランダム方向を B の版の NumPy で再生した方向そのもの（`random_dirs.npz`）と SHA-256・各層の最初の一件の教師強制で、主位置（凍結の `steer_B.main_position`）・
          答えの文字の位置（加減の帯の中）・前置きの SHA（`preamble_sha`）・logits の突き合わせ（`magnitude.logit_check`）・較正の検査（`magnitude.calibration_check`）。
  extract 封印の後: 凍結の記録と封印の記録がそろったコミットで、選んだ試行の全件（`design-facts-Blens.json` の `E.selected`・起動器は選び直さない）の、
          正規化の前の最終の残差を、主位置と答えの文字の位置で取り（`model.norm` の入力への前の hook）、最初の一件の全語彙の logits を置く。
          **方向はここでは掛けない**（直接の経路は手元の器 `tools/blens_calib.py` が計算する）。check の確かめもすべてもう一度行う。
止める条件（外れたら止める・登録者に相談・裁定 D184）: 版の不一致（入れ直した後にランタイムの再起動を求める）・GPU・重みの SHA-256・選んだ試行の SHA16・
  前置きの SHA・主位置・答えの文字の位置・選択の値を読めない出力・logits の突き合わせ・較正の検査。
v2（2026-09-24・裁定 D187）: 再生したランダム方向そのものを出力に置く（手元の器が方向ごとの相対の差の許容で突き合わせる・ビットの一致は求めない）。
  版は三つとも文字列の完全な一致で確かめる（torch は CUDA の組み `+cu…` まで）。torch が違えば、B の組みの torch を PyTorch の置き場から入れ直し、
  入っている torchvision・torchaudio も同じ組みに揃える（版の番号は入っているものの `+` の前・組みの違う拡張が import で止まるのを避ける）。
運用: コーディネータが登録者の Chrome 越しに Colab を操作する（ランタイムの選択と結果の zip のダウンロードもコーディネータ）。登録者の手に残すのは同意と支払い。
  資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。Drive は使わない（出力は小さく、終わりに zip を落とす）。
セルに打つ一行（先頭の下線は type の事故の緩衝・<commit> は 40 桁）:
  ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='check';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_Blens.py').read())
DRY（手元の検査・OP4B_DRY=1）: 登録機種の設定を小さくした乱数の模型（実重みではない）と実トークナイザで、同じ経路を CPU で通す。OP4B_REPO_DIR・OP4B_OUT が要る。
  版・GPU・重みの SHA は見ない。較正の検査は計算して印字するが、止めない（乱数の模型なので合わない）。OP4B_DRY_N で一層の件数を減らす（extract）。
関数 `context_of`・`calibration_items` は合成データの器 `tools/dry_run_Blens.py` が import して経路を確かめる（import のときは走らない）。
柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, time, glob, shutil, hashlib, datetime, subprocess, zipfile

VERSION = 'v2'
T0 = time.time()
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
LOG = []
CH = re.compile(r'"choice"\s*:\s*"(a|b|c|d|refuse)"')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


class Stop(Exception):
    pass


def mark(step, **kw):
    LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
    print('[boot_Blens] %-14s %6.0fs %s' % (step, time.time() - T0, kw or ''), flush=True)


def sh(cmd, check=True):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-3000:])
        raise RuntimeError('失敗: %s' % cmd)
    return r


def stop(msg):
    mark('stop', reason=msg)
    sys.exit('[boot_Blens] 止める（登録者に相談）: ' + msg)


def context_of(tok, prompt, trial, raw, arm_sha16, main_position):
    """一件の教師強制の入力（組み立て済みのプロンプト＋出力の答えの文字の前まで）と位置。外れれば Stop。"""
    tid = trial['trial_id']
    if trial['preamble_sha'] != arm_sha16:
        raise Stop('前置きの SHA が試行の記録と違う: %s' % tid)
    mp = main_position(prompt)
    if mp != len(prompt) - 1:
        raise Stop('主位置が凍結の steer_B.main_position と違う: %s' % tid)
    enc = tok(raw['final'], add_special_tokens=False, return_offsets_mapping=True)
    ms = list(CH.finditer(raw['final']))
    if not ms or ms[-1].group(1) != trial['choice']:
        raise Stop('選択の値を読めない: %s' % tid)
    pos = ms[-1].start(1)
    cover = [q for q, (s0, s1) in enumerate(enc['offset_mapping']) if s0 <= pos < s1]
    if not cover or cover[0] < 1:
        raise Stop('選択の値の文字を覆うトークンが無い: %s' % tid)
    c0 = cover[0]
    lp = len(prompt) + c0 - 1
    if not (mp <= lp < len(prompt) + len(enc['input_ids'])):
        raise Stop('答えの文字の位置が加減の帯の中に無い: %s' % tid)
    return {'trial_id': tid, 'trial_index': trial['trial_index'], 'choice': trial['choice'], 'n_prompt': len(prompt), 'main_pos': mp, 'cover': c0,
            'letter_pos': lp, 'letter_token': int(enc['input_ids'][c0]), 'ids': list(prompt) + list(enc['input_ids'][:c0])}


def calibration_items(keys, ctx_rec, observed, ci, binom_central):
    """較正の検査（正本 magnitude.calibration_check）: 層ごとの最初の文脈の、変換の後の確率と、無操作の観測の件数。"""
    calib, off = {}, []
    for key in keys:
        rec = [c for c in ctx_rec if c['stratum'] == key][0]
        ob = observed[key]
        lo, hi = binom_central(ob['n'], rec['pT_main_fmain'], ci)
        item = {'main': {'p_T': rec['pT_main_fmain'], 'n': ob['n'], 'k': ob['style'], 'interval': [lo, hi], 'inside': lo <= ob['style'] <= hi}}
        if not item['main']['inside']:
            off.append('%s 主位置' % key)
        if key.endswith('|json'):
            item['letter'] = {}
            for x in ('a', 'b', 'c'):
                lo2, hi2 = binom_central(ob['json_n'], rec['pT_letter'][x], ci)
                k2 = ob['json_letters'][x]
                item['letter'][x] = {'p_T': rec['pT_letter'][x], 'n': ob['json_n'], 'k': k2, 'interval': [lo2, hi2], 'inside': lo2 <= k2 <= hi2}
                if not item['letter'][x]['inside']:
                    off.append('%s 答えの文字 %s' % (key, x))
        calib[key] = item
    return calib, off


def run():
    PHASE = os.environ.get('OP4B_PHASE', 'check')
    COMMIT = os.environ.get('OP4B_COMMIT', '')
    DRY = os.environ.get('OP4B_DRY') == '1'
    if PHASE not in ('check', 'extract'):
        sys.exit('[boot_Blens] 相は check か extract')
    if not DRY and not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
        sys.exit('[boot_Blens] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
    print('[boot_Blens] %s 開始 phase=%s %s' % (VERSION, PHASE, 'DRY' if DRY else COMMIT), flush=True)
    # ---- 1. リポジトリ（コミット固定）と正本
    if DRY:
        REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
        OUTROOT = os.path.abspath(os.environ['OP4B_OUT'])
    else:
        REPO, OUTROOT = '/content/ontology-preamble-4b', '/content/op4b-Blens'
        head_ok = os.path.isdir(os.path.join(REPO, '.git')) and sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
        if not head_ok:
            shutil.rmtree(REPO, ignore_errors=True)
            sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
            sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone', 'tools', 'arms', 'design', 'records', 'results/dirB', 'results/stageB'])
            sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
        if sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() != COMMIT:
            stop('取り出したコミットが OP4B_COMMIT と違う')
    os.makedirs(OUTROOT, exist_ok=True)
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    FJ = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
    if PHASE == 'extract' and not DRY:
        for need in ('FREEZE-RECORD-Blens.json', 'sealing-record-Blens.json'):
            if not os.path.exists(os.path.join(REPO, 'records', 'Blens', need)):
                stop('相 extract は凍結と封印の後に走らせる（%s が無い・正本 predictions.order）' % need)
    mark('repo', commit=COMMIT[:12] or 'dry', canon=TL['version'])

    # ---- 2. 版（正本 inputs.versions_B）と GPU
    import importlib.metadata as md

    def ver(k):
        try:
            return md.version(k)
        except Exception:
            return None
    PIN = TL['inputs']['versions_B']
    VER = {k: ver(k) for k in ('numpy', 'torch', 'transformers', 'torchvision', 'torchaudio', 'tokenizers', 'huggingface_hub', 'accelerate', 'safetensors')}
    want = {'numpy': PIN['numpy'], 'torch': PIN['torch'], 'transformers': PIN['transformers']}
    bad = {k: VER[k] for k, v in want.items() if VER[k] != v}          # 文字列の完全な一致（torch は CUDA の組みまで・裁定 D187）
    if bad and not DRY:
        mark('pin', installing=bad)
        os.environ['HF_HUB_DISABLE_XET'] = '1'
        if 'torch' in bad:
            cuda = PIN['torch'].split('+')[1]
            pk = ['torch==%s' % PIN['torch']] + ['%s==%s+%s' % (c, VER[c].split('+')[0], cuda) for c in ('torchvision', 'torchaudio') if VER.get(c)]
            sh([sys.executable, '-m', 'pip', 'install', '-q'] + pk + ['--index-url', 'https://download.pytorch.org/whl/%s' % cuda])
        sh([sys.executable, '-m', 'pip', 'install', '-q', 'numpy==%s' % want['numpy'], 'transformers==%s' % want['transformers'], 'accelerate', 'huggingface_hub', 'safetensors'])
        print('[boot_Blens] 版を入れ直した。**ランタイムを再起動して（「ランタイム」→「セッションを再起動」）、同じ一行をもう一度走らせる**', flush=True)
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
    import steer_B
    import run_stageB_local as RB
    import blens_core as C
    import blens_lens as BL
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig

    # ---- 3. 重み（転記行 F の SHA-256 と突き合わせる）
    M = TL['inputs']['model']
    W_SHA = {}
    if DRY:
        SNAPDIR = os.environ.get('OP4B_TOKENIZER_DIR') or os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % M['rev'])
    else:
        os.environ['HF_HUB_DISABLE_XET'] = '1'
        from huggingface_hub import snapshot_download
        SNAPDIR = snapshot_download(M['repo'], revision=M['rev'])
        for fn in FJ['facts']['F']['sha256']:
            h = hashlib.sha256()
            with open(os.path.join(SNAPDIR, fn), 'rb') as fh:
                for blk in iter(lambda: fh.read(1 << 24), b''):
                    h.update(blk)
            W_SHA[fn] = h.hexdigest().upper()
        badw = [fn for fn, sha in FJ['facts']['F']['sha256'].items() if W_SHA[fn] != sha]
        if badw:
            stop('重みの SHA-256 が転記行 F と違う: %s' % badw)
    mark('weights', snapshot=os.path.basename(SNAPDIR), checked=len(W_SHA))

    # ---- 4. 段階 B のランダム方向（B の版の NumPy で再生した方向そのものと SHA-256・層一の器が手元の再生と許容の内で突き合わせる・裁定 D187）
    D = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
    rk = BL.rkey
    ratios = [rk(r) for r in TL['layers']['ratios']]
    sel = rk(TL['primary']['ratio'])
    RDIR = {'main@%s' % sel: np.array(steer_B.random_directions(D['static__%s' % sel], 'main', float(sel)))}
    for r in ratios:
        RDIR['tune@%s' % r] = np.array(steer_B.random_directions(D['static__%s' % r], 'tune', float(r)))
    RSHA = {k: BL.dirs_sha256(v) for k, v in RDIR.items()}
    mark('random', numpy=np.__version__, sha=RSHA)

    # ---- 5. 模型とトークナイザ
    tok = AutoTokenizer.from_pretrained(SNAPDIR)
    if DRY:
        cfg = AutoConfig.from_pretrained(SNAPDIR)
        cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim, cfg.intermediate_size = 64, 2, 4, 2, 16, 128
        torch.manual_seed(0)
        model = AutoModelForCausalLM.from_config(cfg).float().eval()
        dev = 'cpu'
    else:
        model = AutoModelForCausalLM.from_pretrained(SNAPDIR, torch_dtype=torch.bfloat16, device_map='cuda').eval()
        dev = 'cuda'
    cap = {}
    hook = model.model.norm.register_forward_pre_hook(lambda mod, args: cap.__setitem__('h', args[0].detach()))
    EPS = float(model.config.rms_norm_eps)
    mark('model', dry=DRY, layers=model.config.num_hidden_layers, eps=EPS)

    # ---- 6. 選んだ試行（起動器は選び直さない）
    E = FJ['facts']['E']
    sel_ids = E['selected']
    if hashlib.sha256(json.dumps(sel_ids, sort_keys=True).encode('utf-8')).hexdigest().upper()[:16] != E['selected_sha16']:
        stop('選んだ試行の一覧の SHA16 が設計の事実と違う')
    AT = RB.arm_texts()
    SAMP = TL['inputs']['sampling_B']
    F_MAIN = int(FJ['facts']['B']['F']['main'])
    L_IDS = {k: int(v) for k, v in FJ['facts']['B']['L'].items()}

    def cell_trials(sc, arm):
        d = os.path.join(REPO, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
        tr = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}
        rw = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
        return tr, rw
    ctxs, observed = [], {}
    dry_n = int(os.environ.get('OP4B_DRY_N', '2') or 2)
    try:
        for key, ids_ in sel_ids.items():
            sc, arm, style = key.split('|')
            scen, inst = RB.scenario_and_instruction(sc)
            tr, rw = cell_trials(sc, arm)
            oks = [t for t in tr.values() if t['status'] == 'ok']
            observed[key] = {'n': len(oks), 'style': sum(1 for t in oks if t['style_b']), 'json_n': sum(1 for t in oks if t['style_b']),
                             'json_letters': {x: sum(1 for t in oks if t['style_b'] and t['choice'] == x) for x in ('a', 'b', 'c', 'd', 'refuse')}}
            take = ids_[:1] if PHASE == 'check' else (ids_[:dry_n] if DRY else ids_)
            prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
            for tid in take:
                cx = context_of(tok, prompt, tr[tid], rw[tid], AT[arm]['sha16'], steer_B.main_position)
                cx.update({'stratum': key, 'scenario': sc, 'arm': arm, 'style': style})
                ctxs.append(cx)
    except Stop as e_:
        stop(str(e_))
    mark('contexts', n=len(ctxs), strata=len(sel_ids))

    # ---- 7. 教師強制の順伝播（方向は掛けない）
    lm_w, g_w = model.lm_head.weight, model.model.norm.weight
    H_main, H_letter, ctx_rec = [], [], []
    first, first_logits = {}, None
    for k, cx in enumerate(ctxs):
        with torch.no_grad():
            out = model(torch.tensor([cx['ids']], device=dev))
            h = cap['h'][0]
            lg = out.logits[0]
            hm, hl = h[cx['main_pos']].float(), h[cx['letter_pos']].float()
            lm_, ll_ = lg[cx['main_pos']].float(), lg[cx['letter_pos']].float()
            if k == 0:                   # logits の突き合わせ（最初の一件・正本 magnitude.logit_check）
                recon = lambda hv: (hv * torch.rsqrt(hv.pow(2).mean() + EPS) * g_w.float()) @ lm_w.float().T
                rm, rl = recon(hm), recon(hl)
                first = {'main_max_abs': float((rm - lm_).abs().max()), 'letter_max_abs': float((rl - ll_).abs().max()),
                         'main_argmax_equal': int(rm.argmax()) == int(lm_.argmax()), 'letter_argmax_equal': int(rl.argmax()) == int(ll_.argmax())}
                atol = TL['magnitude']['logit_check']['atol']
                if not DRY and (first['main_max_abs'] > atol or first['letter_max_abs'] > atol or not first['main_argmax_equal'] or not first['letter_argmax_equal']):
                    stop('logits の突き合わせが外れた: %s' % first)
                first_logits = (lm_.cpu().numpy().astype(np.float32), ll_.cpu().numpy().astype(np.float32))
            top = lambda v: [[int(i), float(v[i])] for i in torch.topk(v, 5).indices.cpu().numpy()]
            t5m, t5l = top(lm_), top(ll_)
            lmn, lln = lm_.cpu().numpy(), ll_.cpu().numpy()
        pT_main = C.transform(lmn, SAMP['temperature'], SAMP['top_k'], SAMP['top_p'])
        pT_letter = C.transform(lln, SAMP['temperature'], SAMP['top_k'], SAMP['top_p'])
        rec = {k2: v for k2, v in cx.items() if k2 != 'ids'}
        rec.update({'pT_main_fmain': float(pT_main[F_MAIN]), 'pT_letter': {x: float(pT_letter[L_IDS[x]]) for x in ('a', 'b', 'c', 'd', 'refuse')},
                    'top5_main': t5m, 'top5_letter': t5l, 'letter_token_is_L': cx['letter_token'] == L_IDS.get(cx['choice'])})
        ctx_rec.append(rec)
        if PHASE == 'extract':
            H_main.append(hm.cpu().numpy().astype(np.float32))
            H_letter.append(hl.cpu().numpy().astype(np.float32))
    hook.remove()
    mark('forward', n=len(ctx_rec), logit_check=first)

    # ---- 8. 較正の検査（正本 magnitude.calibration_check・無操作の確率と観測の率）
    calib, off = calibration_items(list(sel_ids), ctx_rec, observed, TL['magnitude']['calibration_check']['ci'], C.binom_central)
    mark('calibration', outside=off or '無し')
    if off and not DRY:
        stop('較正の検査が区間の外: %s' % off)

    # ---- 9. 書き出しと zip
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    od = os.path.join(OUTROOT, '%s-%s' % (PHASE, stamp))
    os.makedirs(od, exist_ok=True)
    np.savez(os.path.join(od, 'random_dirs.npz'), **RDIR)
    RNPZ = {'file': 'random_dirs.npz', 'sha256': hashlib.sha256(open(os.path.join(od, 'random_dirs.npz'), 'rb').read()).hexdigest().upper(),
            'keys': sorted(RDIR), 'dtype': 'float64', 'shape': {k: list(v.shape) for k, v in RDIR.items()}}
    REC = {'kind': 'blens_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY, 'gpu': GPU, 'versions': VER, 'weights_sha256': W_SHA,
           'random_dirs_sha256': RSHA, 'random_dirs_npz': RNPZ, 'selected_sha16': E['selected_sha16'], 'rms_norm_eps': EPS, 'logit_check': first, 'calibration': calib,
           'contexts': ctx_rec, 'observed': observed, 'log': LOG, 'finished': now(),
           'clause': '本記録は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    json.dump(REC, open(os.path.join(od, 'check.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if PHASE == 'extract':
        np.savez(os.path.join(od, 'h.npz'), h_main=np.array(H_main), h_letter=np.array(H_letter),
                 logits_first_main=first_logits[0], logits_first_letter=first_logits[1])
    zp = od + '.zip'
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(od)):
            z.write(os.path.join(od, fn), os.path.join(os.path.basename(od), fn))
    zsha = hashlib.sha256(open(zp, 'rb').read()).hexdigest().upper()
    mark('done', zip=os.path.basename(zp), sha256=zsha)
    if not DRY:
        try:
            from google.colab import files
            files.download(zp)
        except Exception as e_:
            print('[boot_Blens] zip の自動のダウンロードが走らなかった（左の「ファイル」から落とす）: %s' % e_)
    return od


if __name__ == '__main__':
    run()
