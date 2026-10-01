# -*- coding: utf-8 -*-
"""dry_run_Bprime.py v0.7 —— B′ の合成データの確かめの正式の記録（正本 `computation.synthetic_checks`・草案11 §12・層三の `tools/dry_run_Bl3.py` v4 の型・2026-09-30・
コーディネータ南無弥勒如来）。

走らせる置き場: 移す器（`publish_Bprime.py`）で作業の置き場から写した、公開の置き場の形の一時の置き場（凍結するのと同じ形・`hf/` と `pylib/` は写さない）。
凍結の器（層三・B-lens・段階 B）は公開の置き場の版を読む。トークナイザと設定は作業の置き場の `hf/`（OP4B_HF_DIR）。transformers は `pylib/`（PYTHONPATH）。
〇. 器の閉包と SHA16 の表は、公開の形の一時の置き場で、その置き場の凍結の器（`freeze_Bprime`）を別のプロセスで呼んで取る（作業の置き場で取ると別の個体の二つの器が落ちた・v0.6・U01）。
    別の個体の二つの器が、作業の置き場（`tools/independent/`）と公開の形（`tools/`）で同じバイトであることを、走りの始めと終わりで照らす（v0.6・U01）。
一. 器の自己検査（`--selftest` を持つ器のすべて・別のプロセス）。
二. 小さな乱数の Gemma 4 の確かめ（`dry_bprime.py`）と、行動の下見の合成の応答の確かめ（`dry_bprime_behavior.py`）を別のプロセスで走らせ、項目ごとの合否を写す。
三. 書き手と別の個体の器（`bprime_recompute_rewrite.py`・`bprime_reextract.py`・中は変えない）の `--selftest` と `--dry`。
四. 起動器（`tools/colab/boot_bprime.py`）の相を DRY で別のプロセスとして順に通す: check → extract → behavior → 閉じる（合成の返事）→ pilot（閉じた記録を起動の記録に）→
    main → recompute（hook・rewrite・reextract）→ 集計の一致だけを見る段と結果を開く段 → 掃き出し → 報告の組み立て。枝: 続ける・N1 を外す（D214）・バッチ一（道の違い）・
    行動の下見が器の誤りで閉じた（器の誤りの三つのファイルを合成して閉じる器に渡す・v0.6・U07）・出口の値を大きくした（語彙の行列を大きくした小さな模型・v0.6・U46）。
    一致だけを見る段の後に組の出力を差し替えると結果を開く段が止まる。抽出の記録の形の項目は関数（`form_items_check`）を通る形と六つの落ちる形で直に呼ぶ（v0.6・U02）。
    小さな模型の層の出力の倍率が 1 から離れていること（U45）と、出口の値の大きさ（cap と見分けの下限・U46）を記録する。
五. 凍結と錠の道（v0.6・U05）: 公開の置き場の凍結の層と一時の置き場を重ねた git の置き場で、凍結の本文と予想の書式を組み、合成の Colab の確かめで下見の前の凍結 → 合成の予想の封印 →
    起動器の錠の関数（通る形と止まる形）→ 等方を正本の本数にした DRY の起動器で相を通し、段と組ごとに起動の記録と出力の SHA の記録をコミットする → 下見の記録を正本の門で出し直した
    合成の写しと、session を DRY でない形（本物のコミット）に書き換えた写しで本の凍結 → 集計の DRY でない枝（--freeze・組ごとに違うコミット）→ 報告の本番の入口（build）。
    五は、一〜四の記録を書いた後に走り、その記録を凍結の器が読む（別の記録 `records/Bprime/freeze-path-dry-Bprime-<日付>.md`・`.json`）。書き換えはすべて記録に書く。
**実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の値は、実の値の見込みに使わない。
記録: 作業の置き場の `records/Bprime/dry-run-Bprime-<日付>.md`・`.json`（--force が無ければ上書きしない）。末尾に、走らせた器と正本と台帳の SHA16 を、走りの始めと終わりで同じことを確かめて並べる
（下見の前の凍結の器が今の版と突き合わせる）。部の途中で器が例外で止まったときは、その部に「期待と違う」の行（例外の末尾）を置き、次の部へ進んで記録を書く（v0.3）。
用法: python tools/dry_run_Bprime.py [--force] [--skip-tiny] [--only 一四五] [--keep 置き場]（--skip-tiny と --only は作業の確かめだけで、記録の名に work が付く）
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, time, uuid, shutil, hashlib, argparse, datetime, tempfile, traceback, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G
import publish_Bprime as PUBL
import freeze_Bprime as FZ

VERSION = 'v0.7'        # v0.7（2026-09-30）: Colab の一度目の走り（v0.6・一〜四 143 のうち 137・五は始めで止まった）で見つけた三つを直した——四の報告の確かめが並びの鍵（combo の行）を集合に入れて止まった（確かめの側の誤り）・五の置き場で前の正式の記録を外すときにフォルダ（Colab の記録の置き場）をファイルとして消そうとして止まった・出口の値を大きくした枝は、小さな模型が埋め込みと語彙の行列を共有するので活性も変わり、抽出の記録を同じ模型で取り直さないと独立の再抽出が一致しない（抽出も語彙の行列 40 倍で取る）。前の版は `prev/dry_run_Bprime-v0.6.py`／v0.6（2026-09-30・器の実装の検分の後）: 閉包と SHA の表を公開の形の置き場で取る・別の個体の器のバイトの照らし（U01）・形の項目の関数の七つの形（U02）・凍結と錠の道の部〔五〕（U05）・器の誤りで閉じた行動の下見の枝（U07）・下見の起動に閉じた記録（U12）・層の倍率の行（U45）・出口の値を大きくした枝と大きさの行（U46）。前の版は `prev/dry_run_Bprime-v0.5.py`／v0.5（2026-09-30）: 合成の返事の模型の名と system_fingerprint を識別子の形にした。前の版は `prev/dry_run_Bprime-v0.4.py`／v0.4: 本の計算から報告までを三つの枝で通す。／v0.3: 部の途中の例外を記録の行にする。／v0.2: 別の個体の器の自己検査と --dry を作業の置き場の形で走らせる。／v0.1: 固定の版の置き場と設定とトークナイザの置き場を環境の変数で与えられる
NL = chr(10)
PUB = G.REPO
PYLIB = os.environ.get('OP4B_PYLIB') or os.path.join(BP, 'pylib')            # 固定の版の transformers と numpy の置き場（Colab では入れた置き場を与える）
REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'
HF_DIR = os.environ.get('OP4B_HF_DIR') or os.path.join(BP, 'hf', 'gemma-4-31B-it', REV)
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
ROWS = []
DRY_EXTRA_TOOLS = ['tools/dry_run_Bprime.py', 'tools/dry_bprime.py', 'tools/dry_bprime_behavior.py', 'tools/publish_Bprime.py']
PUB_LAYERS = ('tools', 'design', 'arms', 'records', 'results/dirB')        # 五: 公開の置き場から重ねる凍結の層（Colab の束の sparse の形と同じ）
WSCALE_BIG = '40.0'                                                         # 四: 出口の値を大きくした枝の語彙の行列の倍率（v0.6・U46）


def check(group, name, ok, detail=''):
    ROWS.append({'group': group, 'name': name, 'ok': bool(ok), 'detail': str(detail)[:400]})
    print('[dry_run_Bprime] %s %-28s %s %s' % (group, name[:28], '期待どおり' if ok else '**期待と違う**', str(detail)[:160]), flush=True)


def sha16f(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 22), b''):
            h.update(blk)
    return h.hexdigest().upper()


def wj(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    return path


def env_for(T, extra=None, repo=None):
    R = repo or PUB
    e = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONPATH=PYLIB, OP4B_REPO=R, OP4B_PUBLIC_REPO=R, OP4B_PUB_TOOLS=os.path.join(R, 'tools'), OP4B_HF_DIR=HF_DIR)
    for k in [k for k in e if k.startswith('OP4B_DRY') or k in ('OP4B_PHASE', 'OP4B_STEP', 'OP4B_PART', 'OP4B_COMMIT', 'OP4B_NPZ', 'OP4B_OUT', 'OP4B_REPO_DIR', 'OP4B_BPRIME_DIR')]:
        e.pop(k)
    e.update(extra or {})
    return e


def run(T, args, extra=None, timeout=7200, repo=None):
    t0 = time.time()
    r = subprocess.run([sys.executable, '-W', 'ignore'] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=T, env=env_for(T, extra, repo), timeout=timeout)
    return r, round(time.time() - t0, 1)


def run_json(T, code, repo=None, timeout=7200, args=()):
    """一時の置き場で小さな台本を別のプロセスで走らせ、「@@」で始まる行の JSON を返す（v0.6）。"""
    fd, path = tempfile.mkstemp(suffix='.py', prefix='dryhelper-')
    with os.fdopen(fd, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(code)
    try:
        r, s = run(T, [path] + list(args), timeout=timeout, repo=repo)
    finally:
        os.remove(path)
    line = [l for l in r.stdout.splitlines() if l.startswith('@@')]
    if r.returncode != 0 or not line:
        raise RuntimeError('台本が止まった: %s' % (r.stdout + r.stderr)[-600:])
    return json.loads(line[-1][2:])


TABLE_CODE = r'''# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, 'tools')
import freeze_Bprime as FZ
tools = FZ.import_closure(FZ.TOOLS + %r)
files = tools + ['design/contrasts-Bprime.json', 'tools/ledger-bprime.json']
print('@@' + json.dumps({'table': {f: FZ.sha16f(FZ.P(f)) for f in files if os.path.exists(FZ.P(f))}, 'closure': FZ.import_closure(FZ.TOOLS), 'closure_map': FZ.closure_sha_map()}))
''' % DRY_EXTRA_TOOLS


def t_table(T, repo=None):
    """公開の形の置き場の器の閉包と SHA16 の表（その置き場の凍結の器を別のプロセスで呼ぶ・v0.6・U01）。"""
    return run_json(T, TABLE_CODE, repo=repo)


INDEPENDENT_WS = ('tools/independent/bprime_recompute_rewrite.py', 'tools/independent/bprime_reextract.py')   # 三: 作業の置き場の形で走らせる（器は置き場から二つ上を B′ の置き場とみなす・中は変えない）


def indep_same(T):
    """別の個体の二つの器が、作業の置き場（tools/independent/）と公開の形（tools/）で同じバイトか（v0.6・U01）。"""
    return {os.path.basename(w): os.path.exists(os.path.join(T, 'tools', os.path.basename(w))) and sha256f(os.path.join(BP, *w.split('/'))) == sha256f(os.path.join(T, 'tools', os.path.basename(w)))
            for w in INDEPENDENT_WS}


# ---------------- 一・二・三 ----------------
WORKSPACE_SELFTESTS = ('tools/bprime_publish_map.py', 'tools/publish_Bprime.py')      # 作業の置き場の形を見る器（作業の置き場で走らせる）
INDEPENDENT = ('tools/bprime_recompute_rewrite.py', 'tools/bprime_reextract.py')     # 一では走らせない（三で走らせる）


def part_selftests(T):
    tools = sorted((set(t for t, _ in FZ.SELFTESTS) | set(WORKSPACE_SELFTESTS)) - set(INDEPENDENT))
    for t in tools:
        where = BP if t in WORKSPACE_SELFTESTS else T
        if not os.path.exists(os.path.join(where, *t.split('/'))):
            check('一', '自己検査 ' + os.path.basename(t), False, '器が無い')
            continue
        r, s = run(where, [t, '--selftest'], timeout=3600)
        line = [l for l in r.stdout.splitlines() if 'SELFTEST PASS' in l or 'PASS' in l]
        check('一', '自己検査 ' + os.path.basename(t), r.returncode == 0, (line[-1] if line else (r.stdout + r.stderr)[-300:]) + '（%s 秒）' % s)


def part_tiny(T):
    for t, jf in (('tools/dry_bprime_behavior.py', 'tools/dry-bprime-behavior-2026-09-30.json'), ('tools/dry_bprime.py', 'tools/dry-bprime-2026-09-30.json')):
        r, s = run(T, [t], timeout=14400)
        p = os.path.join(T, *jf.split('/'))
        if r.returncode != 0 or not os.path.exists(p):
            check('二', os.path.basename(t), False, (r.stdout + r.stderr)[-400:])
            continue
        with open(p, encoding='utf-8') as fh:
            R = json.load(fh)
        tests = R.get('tests') or R.get('cases') or {}
        for name, v in tests.items():
            check('二', '%s: %s' % (os.path.basename(t).replace('.py', ''), name), bool(v.get('pass')), {k: v[k] for k in list(v)[:4] if k not in ('pass', 'trace')})
        check('二', '%s の全体（%s 秒）' % (os.path.basename(t), s), bool(R.get('all_pass', all(v.get('pass') for v in tests.values()))), 'all_pass')


def part_independent(T):
    for t in INDEPENDENT_WS:
        if not os.path.exists(os.path.join(BP, *t.split('/'))):
            check('三', os.path.basename(t), False, '別の個体の器が無い')
            continue
        for flag in ('--selftest', '--dry'):
            r, s = run(BP, [t, flag], timeout=14400)
            tail = [l for l in r.stdout.splitlines() if l.strip()][-3:]
            check('三', '%s %s' % (os.path.basename(t), flag), r.returncode == 0, ' / '.join(tail) + '（%s 秒）' % s)


# ---------------- 四 ----------------
def boot(T, OUT, phase, step=None, part=None, extra=None, repo=None):
    R = repo or PUB
    e = {'OP4B_DRY': '1', 'OP4B_REPO_DIR': R, 'OP4B_BPRIME_DIR': T, 'OP4B_OUT': OUT, 'OP4B_PHASE': phase, 'OP4B_DRY_ISO': '9', 'OP4B_DRY_MAX_NEW': '12', 'OP4B_SMOKE_TOKENS': '8'}
    if step:
        e['OP4B_STEP'] = step
    if part:
        e['OP4B_PART'] = part
    e.update(extra or {})
    before = set(glob.glob(os.path.join(OUT, '*')))
    r, s = run(T, ['tools/colab/boot_bprime.py'], e, timeout=14400, repo=repo)
    new = sorted(set(glob.glob(os.path.join(OUT, '*'))) - before)
    dirs = [d for d in new if os.path.isdir(d)]
    return r, s, (dirs[-1] if dirs else None)


PROBE_CODE = r'''# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, 'tools')
import torch
import dry_bprime as DR
import bprime_gemma as G
out = {}
for ws in (4.0, %s):
    m, k, base = DR.tiny_model(5, ws, torch.float32)
    ids = torch.tensor([list(range(2, 42))])
    with torch.no_grad():
        z = m(input_ids=ids, use_cache=False).logits[0, -1].float()
    out[str(ws)] = {'max_abs_z': float(z.abs().max()), 'layer_scalar': [float(l.layer_scalar.reshape(-1)[0]) for l in G.decoder_layers(m)]}
    out['cap'] = float(G.softcap(m))
print('@@' + json.dumps(out))
''' % WSCALE_BIG


def form_items_cases(BOOT, T, OUT, C, EX, npz, table):
    """抽出の記録の形の項目の関数（起動器の `form_items_check`）を、通る形と六つの落ちる形で直に呼ぶ（v0.6・U02）。値は合成（DRY の抽出の記録を土台にした）。"""
    canon16 = table['table']['design/contrasts-Bprime.json']
    tools_now = table['closure_map']
    W = {'model-00001-of-00002.safetensors': 'AB' * 32}
    V = {'transformers': '5.16.1', 'numpy': '2.0.0'}

    def build(tag, mut_ex=None, n_starts=1, tool_error_end=False, ledger_rerun=0):
        R = os.path.join(OUT, 'form-items', tag, 'records', 'Bprime')
        runs = os.path.join(R, 'runs')
        os.makedirs(runs, exist_ok=True)
        sids = [str(uuid.uuid4()) for _ in range(n_starts)]
        t_ = ['2026-10-02T0%d:00:00Z' % (i + 1) for i in range(n_starts)]
        last = None
        for i, sid in enumerate(sids):
            st = {'kind': 'bprime_start_record', 'phase': 'extract', 'part': None, 'session': sid, 'time_utc': t_[i], 'contract_sha16': canon16, 'tools_sha16': tools_now, 'deviations_n': 0}
            sp = wj(os.path.join(runs, 'start-extract-%s.json' % sid[:8]), st)
            last = (sid, sha256f(sp), t_[i])
            if i < n_starts - 1:
                ep = os.path.join(OUT, 'form-items', tag, 'err.json')
                wj(ep, {'tool_error': '合成'})
                outs = {'extract-tool-error.json': sha256f(ep)} if tool_error_end else {'extraction-record-Bprime.json': '0' * 64}
                wj(os.path.join(runs, 'end-extract-%s.json' % sid[:8]), {'kind': 'bprime_end_record', 'phase': 'extract', 'session': sid, 'outputs_sha256': outs})
        X = dict(EX, start_record_sha256=last[1], session=last[0], time_utc='2026-10-02T09:30:00Z', versions=V, weights_sha256=W, checks={k: True for k in EX['checks']})
        if mut_ex:
            mut_ex(X)
        xp = wj(os.path.join(R, 'extract', 'extraction-record-Bprime.json'), X)
        wj(os.path.join(runs, 'end-extract-%s.json' % last[0][:8]), {'kind': 'bprime_end_record', 'phase': 'extract', 'session': last[0],
                                                                     'outputs_sha256': {'extraction-record-Bprime.json': sha256f(xp), 'directions-Bprime.npz': EX['npz_sha256']}})
        return R, {'deviations': [{'kind': 'extract_rerun'}] * ledger_rerun}

    S = {'versions': V, 'weights_sha256': W}
    SR = {'sealed_at_utc': '2026-10-01T12:00:00+00:00'}
    START = {'time_utc': '2026-10-03T00:00:00Z'}
    bad_npz = os.path.join(OUT, 'form-items', 'bad.npz')
    os.makedirs(os.path.dirname(bad_npz), exist_ok=True)
    shutil.copyfile(npz, bad_npz)
    with open(bad_npz, 'ab') as fh:
        fh.write(b'x')
    got = {}
    R0, F0 = build('pass')
    got['通る形'] = BOOT.form_items_check(R0, S, SR, F0, START, npz, tools_now, canon16)[1] == []
    R2, F2 = build('rerun-ok', n_starts=2, tool_error_end=True, ledger_rerun=1)
    got['二つの起動の記録（器の誤りの記録と台帳のやり直しの行あり）は通る'] = BOOT.form_items_check(R2, S, SR, F2, START, npz, tools_now, canon16)[1] == []
    cases = [
        (1, 'item1', lambda: BOOT.form_items_check(build('i1', mut_ex=lambda X: X.pop('row_D'))[0], S, SR, F0, START, npz, tools_now, canon16)),
        (2, 'item2', lambda: BOOT.form_items_check(R0, S, SR, F0, START, bad_npz, tools_now, canon16)),
        (3, 'item3', lambda: BOOT.form_items_check(R0, dict(S, versions=dict(V, numpy='x')), SR, F0, START, npz, tools_now, canon16)),
        (4, 'item4', lambda: BOOT.form_items_check(build('i4', mut_ex=lambda X: X['checks'].update(g_match=False))[0], S, SR, F0, START, npz, tools_now, canon16)),
        (5, 'item5', lambda: BOOT.form_items_check(R0, S, {'sealed_at_utc': '2026-10-02T10:00:00+00:00'}, F0, START, npz, tools_now, canon16)),
        (6, 'item6', lambda: BOOT.form_items_check(build('i6', n_starts=2)[0], S, SR, F0, START, npz, tools_now, canon16)),
    ]
    for n, key, fn in cases:
        items, bad = fn()
        got['項目 %d の落ちる形' % n] = bool(bad) and items[key]['pass'] is False
    return got


def part_boot(T, OUT, table):
    import numpy as np
    sys.path.insert(0, os.path.join(T, 'tools'))
    C = json.load(open(os.path.join(T, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    res = {}
    # check
    r, s, od = boot(T, OUT, 'check')
    ck = os.path.join(od or '', 'check.json')
    ok = r.returncode == 0 and os.path.exists(ck)
    CK = json.load(open(ck, encoding='utf-8')) if ok else {}
    check('四', '相 check（DRY）', ok, ('項目 %d・通らなかった %s' % (len(CK.get('items') or {}), [k for k, v in (CK.get('items') or {}).items() if not v.get('pass')])) if ok else (r.stdout + r.stderr)[-400:])
    # 小さな模型の層の出力の倍率と出口の値の大きさ（v0.6・U45・U46）
    try:
        pr = run_json(T, PROBE_CODE)
        ls = pr['4.0']['layer_scalar']
        check('四', '小さな模型の層の出力の倍率が 1 から離れている（U45）', min(abs(x - 1.0) for x in ls) >= 0.02, '倍率 %s' % [round(x, 3) for x in ls])
        kk = (CK.get('items') or {}).get('logit_tolerance_k') or {}
        Lg = C['computation']['self_checks']['logit']
        zf = FZ.z_floor(float(kk.get('k') or 1.0), float(kk.get('z0') or 4), pr['cap'], float(Lg['discrimination_factor']))
        check('四', '出口の値の大きさ（U46）', zf is not None and pr[WSCALE_BIG]['max_abs_z'] >= zf,
              '語彙の行列 4 倍の最大 %.2f・%s 倍の最大 %.2f・cap %.1f・測った k %s での見分けの下限 %s（4 倍の模型は下限に届かないので、%s 倍の枝で一段目を通す）'
              % (pr['4.0']['max_abs_z'], WSCALE_BIG, pr[WSCALE_BIG]['max_abs_z'], pr['cap'], kk.get('k'), zf, WSCALE_BIG))
    except Exception as e_:
        check('四', '小さな模型の層の倍率と出口の値の大きさ（U45・U46）', False, str(e_)[-300:])
    # extract（DRY の写しの等方の本数と小さな模型の次元で g を引いた SHA を与える）
    import bprime_directions as BD
    I = C['nulls']['isotropic']
    g = BD.iso_g(I['seed'], C['layers']['ratio'], 9, I['layer_key_scale'], 64)
    g_sha = BD.g_record(g, I['seed'], C['layers']['ratio'], 9, I['layer_key_scale'])['g_sha256']
    r1, s1, _ = boot(T, OUT, 'extract', 'start')
    r, s, od_x = boot(T, OUT, 'extract', 'run', extra={'OP4B_DRY_G': g_sha})
    exj = os.path.join(od_x or '', 'extraction-record-Bprime.json')
    npz = os.path.join(od_x or '', 'directions-Bprime.npz')
    ok = r1.returncode == 0 and r.returncode == 0 and os.path.exists(exj) and os.path.exists(npz)
    check('四', '相 extract（start と run）', ok, ('npz %s' % sha256f(npz)[:16]) if ok else (r1.stdout + r1.stderr + r.stdout + r.stderr)[-400:])
    if not ok:
        return res
    EX = json.load(open(exj, encoding='utf-8'))
    check('四', '抽出の記録の確かめ（g との一致ほか）', all(EX['checks'].values()), EX['checks'])
    # 抽出の記録の形の項目（DRY では起動器が飛ばすので、関数を直に呼ぶ・通る形と六つの落ちる形・v0.6・U02）
    sys.path.insert(0, os.path.join(T, 'tools', 'colab'))
    import boot_bprime as BOOT
    try:
        fi = form_items_cases(BOOT, T, OUT, C, EX, npz, table)
        check('四', '抽出の記録の形の項目（通る形・二つの起動の記録・六つの落ちる形・U02）', all(fi.values()), fi)
    except Exception as e_:
        check('四', '抽出の記録の形の項目（U02）', False, traceback.format_exc()[-300:])
    # behavior
    boot(T, OUT, 'behavior', 'start')
    r, s, od_b = boot(T, OUT, 'behavior', 'run', extra={'OP4B_DRY_BATCH': '8'})
    ok = r.returncode == 0 and os.path.exists(os.path.join(od_b or '', 'behavior-scored.json'))
    check('四', '相 behavior（生成と採点・%s 秒）' % s, ok, '' if ok else (r.stdout + r.stderr)[-400:])
    if not ok:
        return res
    # 閉じる（束 → 合成の返事 → 閉じた記録）
    import close_behavior_Bprime as CBx
    bd, rd, cd = os.path.join(OUT, 'bundle'), os.path.join(OUT, 'reply'), os.path.join(OUT, 'closed')
    b = CBx.do_bundle(C, od_b, bd, allow_dry=True)
    items = json.load(open(os.path.join(bd, 'items.json'), encoding='utf-8'))['items']
    PV = json.load(open(os.path.join(bd, 'private.json'), encoding='utf-8'))['private']
    SC = json.load(open(os.path.join(od_b, 'behavior-scored.json'), encoding='utf-8'))['scored']
    os.makedirs(rd, exist_ok=True)
    lines = []
    for it in items:
        key, ti = PV[it['id']]
        s_ = SC[key][ti]['score']
        lines.append(json.dumps({'id': it['id'], 'format': '書式外' if (s_ is None or s_['format_fail']) else 'ok', 'choice': None if s_ is None else s_['choice'],
                                 'catastrophe': None if s_ is None else s_['catastrophe']}, ensure_ascii=False))
    with open(os.path.join(rd, 'response.md'), 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(lines) + NL)
    with open(os.path.join(rd, 'meta.json'), 'w', encoding='utf-8', newline=NL) as fh:
        json.dump({'model_requested': 'grok-4.7', 'model_returned': 'grok-4.7-dry', 'system_fingerprint': 'fp_dry', 'request_sha16': b['request_sha16']}, fh, ensure_ascii=False)     # 合成の返事の模型の名は識別子の形（報告の走査の埋めた値の決まり・v0.5）
    jp, _ = CBx.do_close(C, od_b, bd, rd, out_dir=cd, allow_dry=True)
    CL = json.load(open(jp, encoding='utf-8'))
    check('四', '行動の下見を閉じた（合成の返事）', CL['external']['agree'] == CL['external']['n'] and CL['tool_error'] is False, 'iii %s' % CL['iii_status']['status'])
    # pilot（閉じた記録を start の段から与える・起動の記録に閉じた記録の SHA16 が入る・v0.6・U12）
    boot(T, OUT, 'pilot', 'start', extra={'OP4B_DRY_CLOSED': jp})
    r, s, od_p = boot(T, OUT, 'pilot', 'run', extra={'OP4B_DRY_CLOSED': jp})
    pj = os.path.join(od_p or '', 'pilot-Bprime.json')
    ok = r.returncode == 0 and os.path.exists(pj)
    PJ = json.load(open(pj, encoding='utf-8')) if ok else {}
    check('四', '相 pilot（%s 秒）' % s, ok and not PJ.get('tool_error'), ('決定 %s・バッチ %s' % ((PJ.get('decision') or {}).get('q1'), PJ.get('batch'))) if ok else (r.stdout + r.stderr)[-400:])
    if not ok or PJ.get('tool_error') or (PJ.get('decision') or {}).get('stop'):
        check('四', '本の計算に進める下見の決定', False, PJ.get('decision'))
        return res
    # 起動の記録の閉じた記録の照らしが外れると相 pilot が止まる（閉じた記録を差し替える・v0.6・U12）
    jp_x = os.path.join(OUT, 'closed-swapped.json')
    X_ = json.load(open(jp, encoding='utf-8'))
    X_['closed_jst'] = '2000-01-01T00:00:00+09:00'
    wj(jp_x, X_)
    boot(T, OUT, 'pilot', 'start', extra={'OP4B_DRY_CLOSED': jp})
    r, s, _ = boot(T, OUT, 'pilot', 'run', extra={'OP4B_DRY_CLOSED': jp_x})
    check('四', '閉じた記録が起動の記録と違えば相 pilot が止まる（U12）', r.returncode != 0 and '閉じた記録の照らしが外れた' in (r.stdout + r.stderr), (r.stdout + r.stderr).strip()[-160:])
    # 本の計算から報告まで: 枝ごとに通す（起動器の下見の記録のまま〔続ける〕・N1 を外す〔D214〕・バッチ一〔道の違い〕・器の誤りで閉じた行動の下見〔U07〕・出口の値を大きくした〔U46〕）
    import build_report_Bprime as BRP
    import bl3_core as K3
    facts = json.load(open(os.path.join(T, 'records', 'Bprime', 'facts-Bprime-pre.json'), encoding='utf-8'))
    bl3 = BRP.bl3_values(C, PUB)

    def e2e(tag, OUT_e, pj_e, PJ_e, drop, jp_e=jp, CL_e=CL, extra_e=None, expect_tool_error=False, exj_e=exj, npz_e=npz):
        os.makedirs(OUT_e, exist_ok=True)
        base = dict({'OP4B_DRY_PILOT': pj_e, 'OP4B_DRY_EXTRACT': exj_e, 'OP4B_NPZ': npz_e}, **(extra_e or {}))
        outs = []
        parts = [('main', 'main')] + ([('main', 'pathdiff')] if int(PJ_e.get('batch') or 0) == 1 else []) + [('recompute', 'hook'), ('recompute', 'rewrite'), ('recompute', 'reextract')]
        for ph, pt in parts:
            boot(T, OUT_e, ph, 'start', pt, extra=extra_e)
            r, s, od_ = boot(T, OUT_e, ph, 'run', pt, extra=base)
            fn = os.path.join(od_ or '', '%s-%s.json' % (ph, pt))
            ok = r.returncode == 0 and os.path.exists(fn) and 'tool_error' not in json.load(open(fn, encoding='utf-8'))
            check('四', '%s相 %s の組 %s（%s 秒）' % (tag, ph, pt, s), ok, '' if ok else (r.stdout + r.stderr)[-400:])
            if ok:
                outs.append(od_)
        if len(outs) != len(parts):
            return None
        jj, aj = os.path.join(OUT_e, 'judge.json'), os.path.join(OUT_e, 'analysis.json')
        r, s = run(T, ['tools/analyze_Bprime.py', 'judge', '--dirs'] + outs + ['--extract', exj_e, '--pilot', pj_e, '--out', jj])
        J = json.load(open(jj, encoding='utf-8')) if (r.returncode == 0 and os.path.exists(jj)) else {}
        check('四', tag + '一致だけを見る段', bool(J.get('agree')), r.stdout.strip()[-300:] or r.stderr[-300:])
        r, s = run(T, ['tools/analyze_Bprime.py', 'open', '--dirs'] + outs + ['--extract', exj_e, '--pilot', pj_e, '--judge', jj, '--closed', jp_e, '--out', aj])
        ok = r.returncode == 0 and os.path.exists(aj)
        check('四', tag + '結果を開く段', ok, r.stdout.strip()[-300:] or r.stderr[-300:])
        if not ok:
            return None
        r, s = run(T, ['tools/sweep_Bprime.py', aj])
        check('四', tag + '掃き出し（欠け零）', r.returncode == 0, r.stdout.strip()[-300:])
        A = json.load(open(aj, encoding='utf-8'))
        mr = A.get('main_run') or {}
        n1_rows = [rid for rid, o in (A.get('rows') or {}).items() if str(o.get('cell_sign', '')).startswith('N1|')]
        pd_ = A.get('path_difference') or {}
        check('四', tag + '集計の出力の枝の形（バッチ・外した升目・道の違い）',
              mr.get('batch') == PJ_e.get('batch') and sorted(mr.get('dropped') or []) == sorted(drop) and (not drop or not n1_rows) and (bool(pd_.get('comparable')) == (int(PJ_e.get('batch') or 0) == 1)),
              {'batch': mr.get('batch'), 'dropped': mr.get('dropped'), 'N1 の行': len(n1_rows), '道の違い': pd_.get('comparable')})
        preds = {'registrant': {'q1.pilot': PJ_e['decision']['q1']}, 'coordinator': {'q1.pilot': PJ_e['decision']['q1']}}
        meta = {'canon': '0' * 16, 'freeze': '1' * 16, 'seal': '2' * 16, 'analysis': sha16f(aj), 'judge': sha16f(jj)}
        try:
            D = BRP.build(C, A, preds, meta, CL_e, facts, bl3)
            hits = BRP.scan(C, D.lines)
            nuc = [L['section'] for L in D.lines if L['kind'] == 'fixed' and L['src'] == 'B' and L['key'] == 'p_nuclear']
            pdl = [L for L in D.lines if L['kind'] == 'fixed' and L['src'] == 'C' and str(L['key']).startswith(BRP.rule_quote(C, '道の違い（B′ で足した）')[0])]
            ok_n = ('summary' in nuc and len(nuc) == 2) if len([c for c in drop if c.startswith('N1|')]) >= 2 else not nuc
            ok_p = bool(pdl) == (int(PJ_e.get('batch') or 0) == 1)
            keys_ = {(L['section'], str(L['key'])) for L in D.lines if L['kind'] == 'fixed'}     # 並びの鍵（combo の行）は文字列にして集める（v0.6 の直し・Colab の一度目で TypeError）
            ok_t = (('summary', 'fixed_sentences.root_counts.tool_error') in keys_ and ('behavior', 'b_tool') in keys_) == bool(expect_tool_error)
            check('四', tag + '報告の組み立てと走査（当たり零）', not hits and ok_n and ok_p and ok_t,
                  '行 %d・当たり %s・nuclear の族の行の節 %s・道の違いの行 %d・器の誤りの行 %s' % (len(D.lines), hits[:3], nuc, len(pdl), ok_t))
        except (SystemExit, Exception) as e_:
            check('四', tag + '報告の組み立てと走査（当たり零）', False, ('%s: %s' % (type(e_).__name__, e_))[:300])
        return outs, jj, aj, J

    got = e2e('', OUT, pj, PJ, [])
    if got is None:
        return res
    outs, jj, aj, J0 = got
    # 一致だけを見る段の後に組の出力を差し替えると、結果を開く段が止まる
    tgt = [o for o in outs if glob.glob(os.path.join(o, 'recompute-rewrite.json'))][0]
    fj = os.path.join(tgt, 'recompute-rewrite.json')
    X = json.load(open(fj, encoding='utf-8'))
    rid = next(iter(X['result']))
    X['result'][rid]['noop_lo'] = float(X['result'][rid]['noop_lo']) + 0.5
    with open(fj, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(X, fh, ensure_ascii=False, indent=1)
    endp = glob.glob(os.path.join(tgt, 'end-*.json'))[0]
    E = json.load(open(endp, encoding='utf-8'))
    E['outputs_sha256']['recompute-rewrite.json'] = sha256f(fj)
    with open(endp, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(E, fh, ensure_ascii=False, indent=1)
    r, s = run(T, ['tools/analyze_Bprime.py', 'open', '--dirs'] + outs + ['--extract', exj, '--pilot', pj, '--judge', jj, '--closed', jp, '--out', aj + '.2'])
    check('四', '判定の後の差し替えで結果を開く段が止まる', r.returncode != 0 and not os.path.exists(aj + '.2'), (r.stdout + r.stderr).strip()[-200:])
    # 写しの枝: N1 の二つの升目を外した写しと、(vi) の決定だけをバッチ一にした写し
    drop = sorted('%s|%s' % tuple(c) for c in C['cells_main'] if c[0] == 'N1')
    PJd = json.loads(json.dumps(PJ))
    for c in drop:
        PJd['cells'][c]['pass_i_ii'] = False
    PJd['decision'] = K3.cells_decision({c: v['pass_i_ii'] for c, v in PJd['cells'].items()}, {}, C['pilot']['decision']['cells_min_pass'])
    if isinstance(PJd.get('iii'), dict) and 'n' in PJd['iii']:
        PJd['iii'].update(n=len(PJd['cells']) - len(drop), dropped_n=len(drop))
    PJd['dry_synthetic'] = '合成データの確かめだけの写し: 起動器の下見の記録の N1 の二つの升目の (i)(ii) を「満たさない」に置き換え、決定を凍結の芯の cells_decision で出し直した（正本 pilot.decision.family・裁定 D214 の枝）'
    pjd = wj(os.path.join(OUT, 'pilot-dry-dropN1.json'), PJd)
    check('四', '〔N1 を外す〕写しの下見の決定', PJd['decision']['q1'] == '一部の升目を外して続ける' and PJd['decision']['dropped'] == drop, PJd['decision'])
    e2e('〔N1 を外す〕', OUT + '-dropN1', pjd, PJd, drop)
    PJ1 = json.loads(json.dumps(PJ))
    sa1 = 10.0 * float(C['pilot']['noise_max'])
    vi1 = K3.vi_decision(sa1, float(PJ['vi']['decision']['spread_b']), C['pilot']['noise_max'], C['readout']['primary']['batch'])
    PJ1['vi']['a'] = {c: sa1 for c in PJ1['vi']['a']}
    PJ1['vi']['decision'] = vi1
    PJ1['batch'], PJ1['floor'] = vi1.get('batch'), vi1.get('floor')
    PJ1['dry_synthetic'] = '合成データの確かめだけの写し: 起動器の下見の記録の (vi) の (a) の揺れを上限の十倍に置き換え、(vi) の決定を凍結の芯の vi_decision で出し直した（本の計算がバッチ一に移る枝・道の違いの組）'
    pj1 = wj(os.path.join(OUT, 'pilot-dry-batch1.json'), PJ1)
    check('四', '〔バッチ一〕写しの (vi) の決定', vi1.get('batch') == 1 and not vi1.get('stop'), vi1)
    if vi1.get('batch') == 1 and not vi1.get('stop'):
        e2e('〔バッチ一〕', OUT + '-batch1', pj1, PJ1, [])
    # 行動の下見が器の誤りで閉じた枝（器の誤りの三つのファイルを合成して閉じる器に渡す・起動器に試しの口は作らない・v0.6・U07）
    try:
        od_te = os.path.join(OUT, 'behavior-tool-error-syn')
        sid = str(uuid.uuid4())
        ep = wj(os.path.join(od_te, 'behavior-tool-error.json'), {'tool_error': '合成の器の誤り（DRY）', 'clause': CLAUSE})
        spp = wj(os.path.join(od_te, 'start-behavior-%s.json' % sid[:8]), {'kind': 'bprime_start_record', 'phase': 'behavior', 'session': sid})
        wj(os.path.join(od_te, 'session.json'), {'kind': 'bprime_colab_behavior', 'dry': True, 'session_id': sid, 'start_sha256': sha256f(spp)})
        wj(os.path.join(od_te, 'end-behavior-%s.json' % sid[:8]), {'kind': 'bprime_end_record', 'phase': 'behavior', 'session': sid, 'outputs_sha256': {'behavior-tool-error.json': sha256f(ep)}})
        jp_te, _ = CBx.do_close_tool_error(C, od_te, out_dir=os.path.join(OUT, 'closed-te'), allow_dry=True)
        CL_te = json.load(open(jp_te, encoding='utf-8'))
        check('四', '〔器の誤りで閉じた行動の下見〕閉じた記録（系統外の採点ができなかった文）', CL_te['tool_error'] is True and bool((CL_te.get('external') or {}).get('reason')), CL_te['external'].get('fail'))
        boot(T, OUT + '-te', 'pilot', 'start', extra={'OP4B_DRY_CLOSED': jp_te})
        r, s, od_pt = boot(T, OUT + '-te', 'pilot', 'run', extra={'OP4B_DRY_CLOSED': jp_te})
        pj_te = os.path.join(od_pt or '', 'pilot-Bprime.json')
        PJ_te = json.load(open(pj_te, encoding='utf-8')) if (r.returncode == 0 and os.path.exists(pj_te)) else {}
        ok = bool(PJ_te) and not PJ_te.get('tool_error') and not (PJ_te.get('decision') or {}).get('stop')
        check('四', '〔器の誤りで閉じた行動の下見〕相 pilot', ok, ('(iii) %s' % (PJ_te.get('iii') or {}).get('fail')) if PJ_te else (r.stdout + r.stderr)[-300:])
        if ok:
            e2e('〔器の誤りで閉じた行動の下見〕', OUT + '-te', pj_te, PJ_te, [], jp_e=jp_te, CL_e=CL_te, expect_tool_error=True)
    except Exception:
        check('四', '〔器の誤りで閉じた行動の下見〕の枝', False, traceback.format_exc()[-300:])
    # 出口の値を大きくした枝（語彙の行列を大きくした小さな模型で、一段目の二つの道が softcap の効く大きさで一致する・v0.6・U46）
    try:
        big = {'OP4B_DRY_WSCALE': WSCALE_BIG}
        boot(T, OUT + '-bigz', 'extract', 'start', extra=big)
        r, s, od_xb = boot(T, OUT + '-bigz', 'extract', 'run', extra=dict(big, OP4B_DRY_G=g_sha))
        exj_b, npz_b = os.path.join(od_xb or '', 'extraction-record-Bprime.json'), os.path.join(od_xb or '', 'directions-Bprime.npz')
        ok = r.returncode == 0 and os.path.exists(exj_b) and os.path.exists(npz_b)
        check('四', '〔出口の値を大きく〕相 extract（同じ模型で抽出の記録を取り直す）', ok, '' if ok else (r.stdout + r.stderr)[-300:])
        if ok:
            e2e('〔出口の値を大きく〕', OUT + '-bigz', pj, PJ, [], extra_e=big, exj_e=exj_b, npz_e=npz_b)
    except Exception:
        check('四', '〔出口の値を大きく〕の枝', False, traceback.format_exc()[-300:])
    res.update(outs=outs, judge=jj, analysis=aj, exj=exj, npz=npz, pj=pj, jp=jp, CK=CK)
    return res


# ---------------- 五: 凍結と錠の道 ----------------
GATE_CODE = r'''# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, os.path.join('tools', 'colab'))
sys.path.insert(0, 'tools')
import boot_bprime as B
C = json.load(open(os.path.join('design', 'contrasts-Bprime.json'), encoding='utf-8'))
ph, frp, srp, now = sys.argv[1:5]
FR = json.load(open(frp, encoding='utf-8'))
SR = json.load(open(srp, encoding='utf-8'))
print('@@' + json.dumps(B.gate_bad(C, os.getcwd(), ph, FR, SR, now), ensure_ascii=False))
'''
INFO_CODE = r'''# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, 'tools')
import freeze_Bprime as FZ
C = FZ.load(FZ.R_('design', 'contrasts-Bprime.json'))
print('@@' + json.dumps({'closure_map': FZ.closure_sha_map(), 'g': FZ.g_local(C)['g_sha256'], 'canon16': FZ.sha16f(FZ.R_('design', 'contrasts-Bprime.json')),
                         'manifest': FZ.load(FZ.MANIFEST)}, ensure_ascii=False))
'''
PILOT_SYN_CODE = r'''# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, 'tools')
import bprime_gemma as G
import bl3_core as K
C = json.load(open(os.path.join('design', 'contrasts-Bprime.json'), encoding='utf-8'))
PJ = json.load(open(sys.argv[1], encoding='utf-8'))
PL = C['pilot']
for c, v in PJ['cells'].items():
    v['mass'], v['pa'] = 0.95, 0.5
    v['pass_i_ii'] = bool(K.pass_i_ii(v['mass'], v['pa'], PL['mass_min'], PL['p_bounds']))
vi = K.vi_decision(max(float(x) for x in PJ['vi']['a'].values()), max(float(x) for x in PJ['vi']['b'].values()), PL['noise_max'], C['readout']['primary']['batch'])
PJ['batch'], PJ['floor'] = vi.get('batch'), vi.get('floor')
PJ['decision'] = K.cells_decision({c: v['pass_i_ii'] for c, v in PJ['cells'].items()}, {}, PL['decision']['cells_min_pass'])
PJ['dry_synthetic'] = ('合成データの確かめの五だけの写し: 起動器の DRY の下見の記録（小さな乱数の模型・DRY の写しの門）の升目の質量と確率を正本の門を満たす合成の値に置き換え、'
                       '(i)(ii) と決定とバッチを凍結の芯（pass_i_ii・cells_decision・vi_decision）で出し直した（本の凍結の器が正本の門で出し直すため）')
with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(PJ, fh, ensure_ascii=False, indent=1)
print('@@' + json.dumps({'q1': PJ['decision'].get('q1'), 'batch': PJ['batch'], 'stop': bool(vi.get('stop'))}, ensure_ascii=False))
'''


def git(T5, *args):
    r = subprocess.run(['git', '-C', T5] + list(args), capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(args), r.stderr[-300:]))
    return r.stdout.strip()


def commit(T5, msg):
    git(T5, 'add', '-A')
    if git(T5, 'status', '--porcelain'):
        git(T5, 'commit', '-q', '-m', msg)
    return git(T5, 'rev-parse', 'HEAD')


def part_freeze_path(T, rec_md, rec_js, work):
    """五: 凍結と錠の道（v0.6・U05）。戻り値: 行の並び（別の記録に書く）。"""
    ROWS5 = []

    def ck(name, ok, detail=''):
        ROWS5.append({'group': '五', 'name': name, 'ok': bool(ok), 'detail': str(detail)[:400]})
        print('[dry_run_Bprime] 五 %-28s %s %s' % (name[:28], '期待どおり' if ok else '**期待と違う**', str(detail)[:160]), flush=True)
    base = os.path.dirname(T)
    T5, OUT5, W5 = (os.path.join(base, x) for x in ('freeze-tree', 'boot-out-5', 'work-5'))
    for d in (OUT5, W5):
        os.makedirs(d, exist_ok=True)
    # 0. 置き場: 公開の置き場の凍結の層 ＋ 一時の置き場（B′ の移した形）を重ねた git の置き場
    for d in PUB_LAYERS:
        if os.path.isdir(os.path.join(PUB, *d.split('/'))):
            shutil.copytree(os.path.join(PUB, *d.split('/')), os.path.join(T5, *d.split('/')), dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(T, T5, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
    for old in glob.glob(os.path.join(T5, 'records', 'Bprime', 'dry-run-Bprime-*')):   # 移した形に入った前の正式の記録（と Colab の記録の置き場）を外し、今の走りの記録だけを凍結の器に読ませる
        shutil.rmtree(old) if os.path.isdir(old) else os.remove(old)
    day_ = datetime.datetime.now(JST).strftime('%Y-%m-%d')
    for p, ext in ((rec_md, '.md'), (rec_js, '.json')):
        shutil.copyfile(p, os.path.join(T5, 'records', 'Bprime', 'dry-run-Bprime-%s%s' % (day_, ext)))
    with open(os.path.join(T5, 'records', 'Bprime', 'exposure-before-seal-Bprime.md'), 'w', encoding='utf-8', newline=NL) as fh:
        fh.write('# 封印の前の露出の記録（合成・DRY の五だけ・本物ではない）' + NL + NL + CLAUSE + NL)
    git(T5, 'init', '-q')
    git(T5, 'config', 'user.email', 'dry@localhost')
    git(T5, 'config', 'user.name', 'dry')
    git(T5, 'config', 'core.autocrlf', 'false')
    c0 = commit(T5, 'DRY 五: 公開の形')
    ck('公開の形の git の置き場', bool(re.fullmatch(r'[0-9a-f]{40}', c0)), c0[:12])
    C = json.load(open(os.path.join(T5, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    now_jst = lambda: datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M')
    W = '合成データの確かめの五の凍結（DRY・本物ではない）'
    # 1. 凍結の本文と予想の書式（組む器で）
    r, s = run(T5, ['tools/make_frozen_Bprime.py', '--words', W, '--date', now_jst()], repo=T5)
    ck('凍結の本文を組む', r.returncode == 0 and os.path.exists(os.path.join(T5, 'design', 'design-Bprime-FROZEN.md')), (r.stdout + r.stderr).strip()[-200:])
    r, s = run(T5, ['tools/make_predictions_form_Bprime.py'], repo=T5)
    ck('予想の書式を組む', r.returncode == 0, (r.stdout + r.stderr).strip()[-200:])
    c1 = commit(T5, 'DRY 五: 凍結の本文と書式')
    # 2. 合成の Colab の確かめ（相 check の出力の形・値は合成）→ 下見の前の凍結（凍結の器の確かめをすべて通す・自己検査と合成データの記録の照らしを含む）
    info = run_json(T5, INFO_CODE, repo=T5)
    V = C['inputs']['versions']
    cc = os.path.join(W5, 'colab-check')
    wj(os.path.join(cc, 'session.json'), {'kind': 'bprime_colab_check', 'dry': False, 'commit': c1, 'gpu': C['inputs']['gpu']['name'],
                                          'versions': {'transformers': V['transformers'], 'torch': V['torch'], 'numpy': '合成'},
                                          'weights_sha256': {k: v['sha256'].upper() for k, v in info['manifest']['files'].items()}, 'canon_sha16': info['canon16'],
                                          'tools_sha16': info['closure_map'], 'dry_synthetic': 'DRY の五の合成の Colab の確かめ（本物ではない）'})
    wj(os.path.join(cc, 'check.json'), {'all_pass': True, 'items': {'isotropic_g': {'g': {'g_sha256': info['g']}}, 'logit_tolerance_k': {'pass': True, 'k': 5.0, 'z0': 4}},
                                        'determinism': {'allow_tf32_matmul': False, 'allow_tf32_cudnn': False, 'float32_matmul_precision': 'highest', 'attn_implementation': 'sdpa'},
                                        'dry_synthetic': 'DRY の五の合成（本物ではない）'})
    bsz = str(C['behavior_pilot']['seeds']['batch_size'])
    r, s = run(T5, ['tools/freeze_Bprime.py', 'prefreeze', '--words', W, '--when', now_jst(), '--colab-check', cc, '--behavior-batch', bsz], repo=T5, timeout=14400)
    FRP = os.path.join(T5, 'records', 'Bprime', 'FREEZE-RECORD-Bprime.json')
    ok = r.returncode == 0 and os.path.exists(FRP)
    ck('下見の前の凍結（合成の Colab の確かめ・凍結の器の確かめをすべて通す・%s 秒）' % s, ok, (r.stdout + r.stderr).strip()[-300:])
    if not ok:
        return ROWS5
    c2 = commit(T5, 'DRY 五: 下見の前の凍結')
    # 3. 封印（合成の予想）
    choices = {it['key']: it['options'][0] for it in C['predictions']['items']}
    choices['free'] = '合成の情報状態（DRY の五）'
    chp = wj(os.path.join(W5, 'choices.json'), choices)
    r1, _ = run(T5, ['tools/seal_Bprime.py', 'coordinator', '--choices', chp, '--date', now_jst()[:10]], repo=T5)
    cp = os.path.join(T5, 'records', 'predictions', 'predictions-Bprime-coordinator.json')
    ok = r1.returncode == 0 and os.path.exists(cp)
    if ok:
        v = json.load(open(cp, encoding='utf-8'))
        v['who'], v['free'] = '登録者', '合成の登録者の情報状態（DRY の五）'
        rb = json.dumps(v, ensure_ascii=False, indent=1).encode('utf-8')
        rp = os.path.join(W5, 'registrant.json')
        open(rp, 'wb').write(rb)
        r2, _ = run(T5, ['tools/seal_Bprime.py', 'registrant', '--json', rp, '--sha', hashlib.sha256(rb).hexdigest().upper()], repo=T5)
        r3, _ = run(T5, ['tools/seal_Bprime.py', 'record'], repo=T5)
        ok = r2.returncode == 0 and r3.returncode == 0
    SRP = os.path.join(T5, 'records', 'Bprime', 'sealing-record-Bprime.json')
    ck('封印（合成の予想・コーディネータが先）', ok and os.path.exists(SRP), (r1.stdout + r1.stderr).strip()[-200:])
    if not os.path.exists(SRP):
        return ROWS5
    c3 = commit(T5, 'DRY 五: 封印')
    # 4. 起動器の錠の関数（本番と同じ関数）: 通る形と止まる形
    FR = json.load(open(FRP, encoding='utf-8'))
    SR = json.load(open(SRP, encoding='utf-8'))
    gate = lambda ph, fr, sr, now: run_json(T5, GATE_CODE, repo=T5, args=(ph, fr, sr, now))
    nowS = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
    ck('錠が通る（相 extract）', gate('extract', FRP, SRP, nowS) == [], '')
    tgt = os.path.join(T5, 'tools', 'sweep_Bprime.py')
    orig = open(tgt, 'rb').read()
    try:
        open(tgt, 'ab').write(b'\n# DRY \xe3\x81\xae\xe6\x9b\xb8\xe3\x81\x8d\xe6\x8f\x9b\xe3\x81\x88\n')
        ck('錠が止まる（凍結物の SHA16 の違い）', bool(gate('extract', FRP, SRP, nowS)))
    finally:
        open(tgt, 'wb').write(orig)
    frx = wj(os.path.join(W5, 'fr-ledger.json'), dict(FR, deviations=[{'no': 'X', 'tool_diffs': [{'path': 'tools/sweep_Bprime.py', 'before': 'A' * 16, 'after': 'B' * 16}]}]))
    ck('錠が止まる（台帳のつながらない差分）', bool(gate('extract', frx, SRP, nowS)))
    SRx = json.loads(json.dumps(SR))
    SRx['predictions']['coordinator']['sha256'] = '0' * 64
    ck('錠が止まる（予想の SHA の違い）', bool(gate('extract', FRP, wj(os.path.join(W5, 'sr-x.json'), SRx), nowS)))
    far = (datetime.datetime.now(JST) + datetime.timedelta(days=int(C['computation']['stops']['calendar']['days']) + 2)).strftime('%Y-%m-%d %H:%M:%S')
    ck('錠が止まる（暦の期限・今の時刻を与える口）', bool(gate('extract', FRP, SRP, far)))
    ck('錠が止まる（本の凍結が無い）', any('本の凍結' in x for x in gate('main', FRP, SRP, nowS)))
    stp = os.path.join(T5, 'records', 'Bprime', 'stops', 'closed-g4-Bprime.json')
    wj(stp, {'kind': 'synthetic'})
    ck('錠が止まる（閉じた記録・U16）', any('閉じた' in x for x in gate('extract', FRP, SRP, nowS)))
    shutil.rmtree(os.path.dirname(stp))
    # 5. 相を DRY の起動器で通す（等方は正本の本数・凍結の記録を与える）。段と組ごとに起動の記録と出力の SHA の記録を runs に置いてコミットする（v0.6・U05 (2)）
    runs = os.path.join(T5, 'records', 'Bprime', 'runs')
    os.makedirs(runs, exist_ok=True)
    iso = str(C['nulls']['isotropic']['count'])
    common = {'OP4B_DRY_FREEZE': FRP, 'OP4B_DRY_ISO': iso}
    rewrites = []

    def phase(ph, pt=None, extra=None, rewrite_end=None):
        e = dict(common, **(extra or {}))
        r, s, od_s = boot(T5, OUT5, ph, 'start', pt, extra=e, repo=T5)
        S_ = json.load(open(os.path.join(od_s, 'session.json'), encoding='utf-8')) if od_s else {}
        sn = S_.get('start_record')
        if r.returncode != 0 or not sn:
            raise RuntimeError('start %s %s: %s' % (ph, pt, (r.stdout + r.stderr)[-300:]))
        shutil.copyfile(os.path.join(od_s, sn), os.path.join(runs, sn))
        c_s = commit(T5, 'DRY 五: 起動の記録 %s %s' % (ph, pt or ''))
        r, s, od_r = boot(T5, OUT5, ph, 'run', pt, extra=e, repo=T5)
        ends = glob.glob(os.path.join(od_r or '', 'end-%s*.json' % ph))
        if r.returncode != 0 or len(ends) != 1:
            raise RuntimeError('run %s %s: %s' % (ph, pt, (r.stdout + r.stderr)[-300:]))
        cp_ = os.path.join(W5, 'copy-' + os.path.basename(od_r))
        shutil.copytree(od_r, cp_)
        if rewrite_end:
            rewrite_end(cp_)
        S2 = json.load(open(os.path.join(cp_, 'session.json'), encoding='utf-8'))
        S2.update(dry=False, commit=c_s, dry_rewritten='DRY の五の写し: session の dry を偽に、commit を起動の記録を置いたコミットに書き換えた（凍結の器と集計の器の DRY でない枝を通すため・U05）')
        wj(os.path.join(cp_, 'session.json'), S2)
        rewrites.append('%s %s: session の dry を偽に・commit を %s に' % (ph, pt or '', c_s[:12]))
        shutil.copyfile(glob.glob(os.path.join(cp_, 'end-%s*.json' % ph))[0], os.path.join(runs, os.path.basename(ends[0])))
        c_e = commit(T5, 'DRY 五: 出力の SHA の記録 %s %s' % (ph, pt or ''))
        return cp_, s, c_e
    try:
        I = C['nulls']['isotropic']
        import bprime_directions as BD
        g = BD.iso_g(I['seed'], C['layers']['ratio'], int(iso), I['layer_key_scale'], 64)
        g_sha = BD.g_record(g, I['seed'], C['layers']['ratio'], int(iso), I['layer_key_scale'])['g_sha256']
        od_x, s, _ = phase('extract', extra={'OP4B_DRY_G': g_sha})
        exd = os.path.join(T5, 'records', 'Bprime', 'extract')
        os.makedirs(exd, exist_ok=True)
        shutil.copyfile(os.path.join(od_x, 'extraction-record-Bprime.json'), os.path.join(exd, 'extraction-record-Bprime.json'))
        npz = os.path.join(od_x, 'directions-Bprime.npz')
        commit(T5, 'DRY 五: 抽出の記録')
        ck('相 extract（等方 %s・起動の記録と出力の SHA の記録をコミット・%s 秒）' % (iso, s), True, '')
        od_b, s, _ = phase('behavior', extra={'OP4B_DRY_BATCH': bsz})
        import close_behavior_Bprime as CBx
        bd5 = os.path.join(W5, 'bundle')
        CBx.do_bundle(C, od_b, bd5, allow_dry=True)
        closed_dir = os.path.join(T5, 'records', 'Bprime', 'behavior')
        jp5, _ = CBx.do_close(C, od_b, bd5, None, fail='呼び出しの失敗', out_dir=closed_dir, allow_dry=True)
        commit(T5, 'DRY 五: 行動の下見の閉じた記録')
        ck('相 behavior と閉じた記録（系統外の採点は合成の失敗の理由で閉じる・%s 秒）' % s, os.path.exists(jp5), '')
        pjs = os.path.join(W5, 'pilot-syn.json')

        def pilot_rewrite(cp_):
            got = run_json(T5, PILOT_SYN_CODE, repo=T5, args=(os.path.join(cp_, 'pilot-Bprime.json'), pjs))
            shutil.copyfile(pjs, os.path.join(cp_, 'pilot-Bprime.json'))
            ep_ = glob.glob(os.path.join(cp_, 'end-pilot*.json'))[0]
            E_ = json.load(open(ep_, encoding='utf-8'))
            E_['outputs_sha256']['pilot-Bprime.json'] = sha256f(os.path.join(cp_, 'pilot-Bprime.json'))
            wj(ep_, E_)
            rewrites.append('pilot: 升目の質量と確率を正本の門を満たす合成の値に・(i)(ii) と決定とバッチを凍結の芯で出し直した（決定 %s・バッチ %s）・出力の SHA の記録を合わせた' % (got['q1'], got['batch']))
        od_p, s, c_p = phase('pilot', extra={'OP4B_DRY_CLOSED': jp5}, rewrite_end=pilot_rewrite)
        ck('相 pilot（閉じた記録を照らして進む・%s 秒）' % s, True, '')
        # 6. 本の凍結（DRY でない形の写しの下見の出力で・凍結の器の確かめをすべて通す）
        S_p = json.load(open(os.path.join(od_p, 'session.json'), encoding='utf-8'))
        S_p['commit'] = c_p                                              # 凍結と封印と閉じた記録と抽出の記録を含むコミット（下見の出力の SHA の記録まで置いた後）
        wj(os.path.join(od_p, 'session.json'), S_p)
        r, s = run(T5, ['tools/freeze_Bprime.py', 'main', '--words', W, '--when', now_jst(), '--pilot', od_p, '--npz', npz], repo=T5, timeout=7200)
        FR2 = json.load(open(FRP, encoding='utf-8'))
        ok = r.returncode == 0 and 'main_freeze' in FR2 and bool(FR2.get('main_freeze_sha16'))
        ck('本の凍結（DRY でない形の写しの下見の出力・%s 秒）' % s, ok, (r.stdout + r.stderr).strip()[-300:])
        if not ok:
            return ROWS5
        commit(T5, 'DRY 五: 本の凍結')
        ck('錠が通る（相 main・本の凍結の節の SHA16）', gate('main', FRP, SRP, nowS) == [], '')
        FRm = json.loads(json.dumps(FR2))
        FRm['main_freeze']['decision'] = {'q1': '合成の書き換え'}
        ck('錠が止まる（本の凍結の節の書き換え・U10）', any('本の凍結の節' in x for x in gate('main', wj(os.path.join(W5, 'fr-mf.json'), FRm), SRP, nowS)))
        # 7. 本の計算と独立の再計算（組ごとに違うコミット）→ 集計の DRY でない枝 → 報告の本番の入口
        mains = {'OP4B_DRY_PILOT': pjs, 'OP4B_DRY_EXTRACT': os.path.join(exd, 'extraction-record-Bprime.json'), 'OP4B_NPZ': npz}
        outs, commits = [], []
        for ph, pt in (('main', 'main'), ('recompute', 'hook'), ('recompute', 'rewrite'), ('recompute', 'reextract')):
            cp_, s, c_ = phase(ph, pt, extra=mains)
            outs.append(cp_)
            commits.append(json.load(open(os.path.join(cp_, 'session.json'), encoding='utf-8'))['commit'])
            ck('相 %s の組 %s（等方 %s・%s 秒）' % (ph, pt, iso, s), True, '')
        ck('組ごとに違うコミット（集計は中身で照らす・U08）', len(set(commits)) == len(commits), [c[:12] for c in commits])
        jj5, aj5 = os.path.join(W5, 'judge.json'), os.path.join(T5, 'records', 'Bprime', 'analysis-Bprime.json')
        exr = os.path.join(exd, 'extraction-record-Bprime.json')
        r, s = run(T5, ['tools/analyze_Bprime.py', 'judge', '--dirs'] + outs + ['--extract', exr, '--freeze', FRP, '--out', jj5], repo=T5)
        J5 = json.load(open(jj5, encoding='utf-8')) if os.path.exists(jj5) else {}
        ck('一致だけを見る段（DRY でない枝・--freeze・錠と本の凍結の照らしを通る）', r.returncode == 0 and J5.get('agree') is True and J5.get('dry') is False,
           (r.stdout + r.stderr).strip()[-300:])
        r, s = run(T5, ['tools/analyze_Bprime.py', 'open', '--dirs'] + outs + ['--extract', exr, '--freeze', FRP, '--judge', jj5, '--closed', jp5, '--runs', runs, '--out', aj5], repo=T5)
        A5 = json.load(open(aj5, encoding='utf-8')) if os.path.exists(aj5) else {}
        ck('結果を開く段（DRY でない枝・走行の表を照らす・U04）', r.returncode == 0 and bool((A5.get('runs') or {}).get('table')) and not (A5.get('runs') or {}).get('bad'),
           (r.stdout + r.stderr).strip()[-300:])
        commit(T5, 'DRY 五: 集計の出力')
        r, s = run(T5, ['tools/build_report_Bprime.py', 'build', '--runs', runs], repo=T5)
        ck('報告の本番の入口（錠・走行の表を読み直して照らす・走査の当たり零・U03・U04）', r.returncode == 0 and os.path.exists(os.path.join(T5, 'records', 'Bprime', 'results-Bprime.md')),
           (r.stdout + r.stderr).strip()[-300:])
    except Exception:
        ck('五の途中で器が例外で止まった', False, traceback.format_exc()[-400:])
    ck('書き換えの記録（DRY でない形にした写し・合成の値）', True, '・'.join(rewrites))
    return ROWS5


def write_record(out_md, out_js, rows, title, head_lines, table, extra_js=None):
    n, k = len(rows), sum(1 for r in rows if r['ok'])
    L = ['# %s（機械生成・`tools/dry_run_Bprime.py` %s・%s 日本時間）' % (title, VERSION, datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M')), ''] + head_lines + [
         '- 確かめ: %d のうち %d が期待どおり。' % (n, k), '', '| 部 | 確かめ | 結果 | 値 |', '|---|---|---|---|']
    for r in rows:
        L.append('| %s | %s | %s | %s |' % (r['group'], r['name'].replace('|', '\\|'), '期待どおり' if r['ok'] else '**期待と違う**', r['detail'].replace('|', '\\|').replace(NL, ' ')))
    if table is not None:
        L += ['', '## 走らせた器と正本と台帳の SHA16（公開の形の置き場で取った・走りの始めと終わりで同じ）', '', '| 置き場 | SHA16 |', '|---|---|'] + ['| %s | %s |' % kv for kv in table.items()]
    L += ['', CLAUSE, '']
    with open(out_md, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(L))
    js = dict({'kind': 'bprime_dry_run', 'version': VERSION, 'rows': rows, 'n': n, 'as_expected': k, 'sha16': table, 'clause': CLAUSE}, **(extra_js or {}))
    with open(out_js, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(js, fh, ensure_ascii=False, indent=1)
    return n, k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--skip-tiny', action='store_true')
    ap.add_argument('--keep', help='一時の置き場を残す（作業の確かめ用）')
    ap.add_argument('--only', help='走らせる部（例: 一四五）。作業の確かめだけで、正式の記録には使わない（記録の名に work が付く）')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    day = datetime.datetime.now(JST).strftime('%Y-%m-%d')
    work = bool(a.only or a.skip_tiny)
    out_md = os.path.join(BP, 'records', 'Bprime', ('dry-run-work-Bprime-%s.md' if work else 'dry-run-Bprime-%s.md') % day)
    out_js = out_md[:-3] + '.json'
    out5_md = os.path.join(BP, 'records', 'Bprime', ('freeze-path-dry-work-Bprime-%s.md' if work else 'freeze-path-dry-Bprime-%s.md') % day)
    if (os.path.exists(out_md) or os.path.exists(out5_md)) and not a.force:
        raise SystemExit('既にある（--force で上書き）: %s' % os.path.basename(out_md))
    t0 = time.time()
    td = a.keep or tempfile.mkdtemp(prefix='bprime-dry-')
    T, OUT = os.path.join(td, 'tree'), os.path.join(td, 'boot-out')
    os.makedirs(OUT, exist_ok=True)
    rows, P = PUBL.publish(T)
    check('〇', '公開の形の一時の置き場', len(rows) == len(P['publish']), '写した %d' % len(rows))
    tab0 = t_table(T)
    ws_tab0 = {f: sha16f(FZ.P(f)) for f in tab0['table']}                 # 作業の置き場の同じ道筋（別の個体の器は読み替え）
    check('〇', '公開の形で取った閉包の表が作業の置き場のバイトと同じ（別の個体の二つの器を含む・U01）',
          ws_tab0 == tab0['table'] and all(t in tab0['table'] for t in INDEPENDENT), '器 %d・別の個体の器 %s' % (len(tab0['table']), [t in tab0['table'] for t in INDEPENDENT]))
    ind0 = indep_same(T)
    check('〇', '別の個体の二つの器が作業の置き場と公開の形で同じバイト（始め・U01）', all(ind0.values()), ind0)
    want = lambda g: (a.only is None) or (g in a.only)
    parts = (('一', lambda: part_selftests(T)), ('二', lambda: None if a.skip_tiny else part_tiny(T)), ('三', lambda: part_independent(T)), ('四', lambda: part_boot(T, OUT, tab0)))
    for g, fn in parts:
        if not want(g):
            continue
        try:
            fn()
        except Exception:
            tb = traceback.format_exc()
            print(tb, flush=True)
            check(g, '部の途中で器が例外で止まった（次の部へ進む）', False, tb[-400:])
    tab1 = t_table(T)
    same = tab0['table'] == tab1['table']
    check('〇', '走りの始めと終わりで器と正本と台帳の SHA16 が同じ（公開の形の置き場）', same, '' if same else sorted(k for k in set(tab0['table']) | set(tab1['table']) if tab0['table'].get(k) != tab1['table'].get(k)))
    ind1 = indep_same(T)
    check('〇', '別の個体の二つの器が作業の置き場と公開の形で同じバイト（終わり・U01）', all(ind1.values()), ind1)
    head = ['- 走らせた置き場: 移す器で作業の置き場から写した公開の形の一時の置き場（写した %d 本）。凍結の器は公開の置き場の版。transformers は分けた置き場の版。**実の重みは読まない**。' % len(rows),
            '- 部: %s（%.0f 秒）。五（凍結と錠の道）は別の記録 `records/Bprime/%s`。' % ('二の小さな模型の確かめを飛ばした作業の走り' if a.skip_tiny else ('の'.join(a.only) if a.only else '一〜四のすべて'),
                                                                               time.time() - t0, os.path.basename(out5_md))]
    n, k = write_record(out_md, out_js, ROWS, 'B′ の合成データの確かめの正式の記録', head, tab1['table'], {'skip_tiny': a.skip_tiny})
    print('[dry_run_Bprime] %d のうち %d が期待どおり・記録 %s' % (n, k, os.path.relpath(out_md, BP)), flush=True)
    if want('五'):
        t5 = time.time()
        try:
            R5 = part_freeze_path(T, out_md, out_js, work)
        except Exception:
            R5 = [{'group': '五', 'name': '五の途中で器が例外で止まった', 'ok': False, 'detail': traceback.format_exc()[-400:]}]
        head5 = ['- 走らせた置き場: 公開の置き場の凍結の層（%s）と、移した形の一時の置き場を重ねた一時の git の置き場。**実の重みは読まない**。合成の値と書き換えは行ごとに書いた。' % '・'.join(PUB_LAYERS),
                 '- 読んだ合成データの正式の記録: `records/Bprime/%s`（SHA16 %s）。五は %.0f 秒。' % (os.path.basename(out_md), sha16f(out_md), time.time() - t5)]
        n5, k5 = write_record(out5_md, out5_md[:-3] + '.json', R5, 'B′ の合成データの確かめの五（凍結と錠の道）の記録', head5, None,
                              {'dry_record': os.path.basename(out_md), 'dry_record_sha16': sha16f(out_md)})
        print('[dry_run_Bprime] 五: %d のうち %d が期待どおり・記録 %s' % (n5, k5, os.path.relpath(out5_md, BP)), flush=True)
    if not a.keep:
        shutil.rmtree(td, ignore_errors=True)


if __name__ == '__main__':
    main()
