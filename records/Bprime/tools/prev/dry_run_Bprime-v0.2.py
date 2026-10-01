# -*- coding: utf-8 -*-
"""dry_run_Bprime.py v0 —— B′ の合成データの確かめの正式の記録（正本 `computation.synthetic_checks`・草案10 §12・層三の `tools/dry_run_Bl3.py` v4 の型・2026-09-30・
コーディネータ南無弥勒如来）。

走らせる置き場: 移す器（`publish_Bprime.py`）で作業の置き場から写した、公開の置き場の形の一時の置き場（凍結するのと同じ形・`hf/` と `pylib/` は写さない）。
凍結の器（層三・B-lens・段階 B）は公開の置き場の版を読む。トークナイザと設定は作業の置き場の `hf/`（OP4B_HF_DIR）。transformers は `pylib/`（PYTHONPATH）。
一. 器の自己検査（`--selftest` を持つ器のすべて・別のプロセス）。
二. 小さな乱数の Gemma 4 の確かめ（`dry_bprime.py`）と、行動の下見の合成の応答の確かめ（`dry_bprime_behavior.py`）を別のプロセスで走らせ、項目ごとの合否を写す。
三. 書き手と別の個体の器（`bprime_recompute_rewrite.py`・`bprime_reextract.py`・中は変えない）の `--selftest` と `--dry`。
四. 起動器（`tools/colab/boot_bprime.py`）の相を DRY で別のプロセスとして順に通す: check → extract → behavior → 閉じる（`close_behavior_Bprime`・合成の返事）→ pilot →
    main → recompute（hook・rewrite・reextract）→ 集計の一致だけを見る段と結果を開く段（`analyze_Bprime` の口）→ 掃き出し → 報告の組み立て。
    一致だけを見る段の後に組の出力を差し替えると、結果を開く段が止まることを確かめる。抽出の記録の形の項目（DRY では飛ばす）は関数を直接呼んで確かめる。
**実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の値は、実の値の見込みに使わない。
記録: 作業の置き場の `records/Bprime/dry-run-Bprime-<日付>.md`・`.json`（--force が無ければ上書きしない）。末尾に、走らせた器と正本と台帳の SHA16 を、走りの始めと終わりで同じことを確かめて並べる
（下見の前の凍結の器が今の版と突き合わせる）。凍結の器を公開の形の置き場で通す確かめは `dry_freeze_Bprime.py`（五）。
用法: python tools/dry_run_Bprime.py [--force] [--skip-tiny]（--skip-tiny は二の小さな模型の確かめを飛ばす・作業の確かめだけで、正式の記録には使わない）
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, time, shutil, hashlib, argparse, datetime, tempfile, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G
import publish_Bprime as PUBL
import freeze_Bprime as FZ

VERSION = 'v0.2'        # v0.2（2026-09-30）: 別の個体の器の自己検査と --dry を作業の置き場の形で走らせる・凍結の器の置き場を OP4B_PUB_TOOLS でも渡す／v0.1（2026-09-30）: 固定の版の置き場と設定とトークナイザの置き場を環境の変数（OP4B_PYLIB・OP4B_HF_DIR）で与えられる（Colab で走らせるため・D271）
NL = chr(10)
PUB = G.REPO
PYLIB = os.environ.get('OP4B_PYLIB') or os.path.join(BP, 'pylib')            # 固定の版の transformers と numpy の置き場（Colab では入れた置き場を与える）
REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'
HF_DIR = os.environ.get('OP4B_HF_DIR') or os.path.join(BP, 'hf', 'gemma-4-31B-it', REV)
JST = datetime.timezone(datetime.timedelta(hours=9))
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
ROWS = []


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


def env_for(T, extra=None):
    e = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONPATH=PYLIB, OP4B_REPO=PUB, OP4B_PUBLIC_REPO=PUB, OP4B_PUB_TOOLS=os.path.join(PUB, 'tools'), OP4B_HF_DIR=HF_DIR)
    for k in [k for k in e if k.startswith('OP4B_DRY') or k in ('OP4B_PHASE', 'OP4B_STEP', 'OP4B_PART', 'OP4B_COMMIT', 'OP4B_NPZ', 'OP4B_OUT', 'OP4B_REPO_DIR', 'OP4B_BPRIME_DIR')]:
        e.pop(k)
    e.update(extra or {})
    return e


def run(T, args, extra=None, timeout=7200):
    t0 = time.time()
    r = subprocess.run([sys.executable, '-W', 'ignore'] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=T, env=env_for(T, extra), timeout=timeout)
    return r, round(time.time() - t0, 1)


def closure_table(root):
    tools = FZ.import_closure(FZ.TOOLS + ['tools/dry_run_Bprime.py', 'tools/dry_bprime.py', 'tools/dry_bprime_behavior.py', 'tools/publish_Bprime.py'])
    files = tools + ['design/contrasts-Bprime.json', 'tools/ledger-bprime.json']
    out = collections.OrderedDict()
    for f in files:
        p = os.path.join(root, *f.split('/'))
        if not os.path.exists(p):
            p = os.path.join(PUB, *f.split('/'))
        if os.path.exists(p):
            out[f] = sha16f(p)
    return out


# ---------------- 一・二・三 ----------------
WORKSPACE_SELFTESTS = ('tools/bprime_publish_map.py', 'tools/publish_Bprime.py')      # 作業の置き場の形を見る器（作業の置き場で走らせる）
INDEPENDENT = ('tools/bprime_recompute_rewrite.py', 'tools/bprime_reextract.py')     # 一では走らせない（三で走らせる）
INDEPENDENT_WS = ('tools/independent/bprime_recompute_rewrite.py', 'tools/independent/bprime_reextract.py')   # 三: 作業の置き場の形で走らせる（器は置き場から二つ上を B′ の置き場とみなす・中は変えない）


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
def boot(T, OUT, phase, step=None, part=None, extra=None):
    e = {'OP4B_DRY': '1', 'OP4B_REPO_DIR': PUB, 'OP4B_BPRIME_DIR': T, 'OP4B_OUT': OUT, 'OP4B_PHASE': phase, 'OP4B_DRY_ISO': '9', 'OP4B_DRY_MAX_NEW': '12', 'OP4B_SMOKE_TOKENS': '8'}
    if step:
        e['OP4B_STEP'] = step
    if part:
        e['OP4B_PART'] = part
    e.update(extra or {})
    before = set(glob.glob(os.path.join(OUT, '*')))
    r, s = run(T, ['tools/colab/boot_bprime.py'], e, timeout=14400)
    new = sorted(set(glob.glob(os.path.join(OUT, '*'))) - before)
    dirs = [d for d in new if os.path.isdir(d)]
    return r, s, (dirs[-1] if dirs else None)


def part_boot(T, OUT):
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
        json.dump({'model_requested': 'grok-4.7', 'model_returned': '合成', 'system_fingerprint': '合成', 'request_sha16': b['request_sha16']}, fh, ensure_ascii=False)
    jp, _ = CBx.do_close(C, od_b, bd, rd, out_dir=cd, allow_dry=True)
    CL = json.load(open(jp, encoding='utf-8'))
    check('四', '行動の下見を閉じた（合成の返事）', CL['external']['agree'] == CL['external']['n'] and CL['tool_error'] is False, 'iii %s' % CL['iii_status']['status'])
    # pilot
    boot(T, OUT, 'pilot', 'start')
    r, s, od_p = boot(T, OUT, 'pilot', 'run', extra={'OP4B_DRY_CLOSED': jp})
    pj = os.path.join(od_p or '', 'pilot-Bprime.json')
    ok = r.returncode == 0 and os.path.exists(pj)
    PJ = json.load(open(pj, encoding='utf-8')) if ok else {}
    check('四', '相 pilot（%s 秒）' % s, ok and not PJ.get('tool_error'), ('決定 %s・バッチ %s' % ((PJ.get('decision') or {}).get('q1'), PJ.get('batch'))) if ok else (r.stdout + r.stderr)[-400:])
    if not ok or PJ.get('tool_error') or (PJ.get('decision') or {}).get('stop'):
        check('四', '本の計算に進める下見の決定', False, PJ.get('decision'))
        return res
    # main と recompute
    base = {'OP4B_DRY_PILOT': pj, 'OP4B_DRY_EXTRACT': exj, 'OP4B_NPZ': npz}
    outs = []
    parts = [('main', 'main')] + ([('main', 'pathdiff')] if int(PJ.get('batch') or 0) == 1 else []) + [('recompute', 'hook'), ('recompute', 'rewrite'), ('recompute', 'reextract')]
    for ph, pt in parts:
        boot(T, OUT, ph, 'start', pt)
        r, s, od_ = boot(T, OUT, ph, 'run', pt, extra=base)
        fn = os.path.join(od_ or '', '%s-%s.json' % (ph, pt))
        ok = r.returncode == 0 and os.path.exists(fn) and 'tool_error' not in json.load(open(fn, encoding='utf-8'))
        check('四', '相 %s の組 %s（%s 秒）' % (ph, pt, s), ok, '' if ok else (r.stdout + r.stderr)[-400:])
        if ok:
            outs.append(od_)
    if len(outs) != len(parts):
        return res
    # 集計の二つの段（別のプロセス）
    jj, aj = os.path.join(OUT, 'judge.json'), os.path.join(OUT, 'analysis.json')
    r, s = run(T, ['tools/analyze_Bprime.py', 'judge', '--dirs'] + outs + ['--extract', exj, '--pilot', pj, '--out', jj])
    J = json.load(open(jj, encoding='utf-8')) if (r.returncode == 0 and os.path.exists(jj)) else {}
    check('四', '一致だけを見る段', bool(J.get('agree')), r.stdout.strip()[-300:] or r.stderr[-300:])
    r, s = run(T, ['tools/analyze_Bprime.py', 'open', '--dirs'] + outs + ['--extract', exj, '--pilot', pj, '--judge', jj, '--closed', jp, '--out', aj])
    ok = r.returncode == 0 and os.path.exists(aj)
    check('四', '結果を開く段', ok, r.stdout.strip()[-300:] or r.stderr[-300:])
    if not ok:
        return res
    r, s = run(T, ['tools/sweep_Bprime.py', aj])
    check('四', '掃き出し（欠け零）', r.returncode == 0, r.stdout.strip()[-300:])
    # 報告の組み立て（合成の予想と SHA）
    import build_report_Bprime as BRP
    A = json.load(open(aj, encoding='utf-8'))
    preds = {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '続ける'}}
    meta = {'canon': '0' * 16, 'freeze': '1' * 16, 'seal': '2' * 16, 'analysis': sha16f(aj), 'judge': sha16f(jj)}
    facts = json.load(open(os.path.join(T, 'records', 'Bprime', 'facts-Bprime-pre.json'), encoding='utf-8'))
    bl3 = BRP.bl3_values(C, PUB)
    try:
        D = BRP.build(C, A, preds, meta, CL, facts, bl3)
        hits = BRP.scan(C, D.lines)
        check('四', '報告の組み立てと走査（当たり零）', not hits, '行 %d・当たり %s' % (len(D.lines), hits[:3]))
    except SystemExit as e_:
        check('四', '報告の組み立てと走査（当たり零）', False, str(e_)[:300])
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
    # 抽出の記録の形の項目（DRY では起動器が飛ばすので、関数を直接呼ぶ）
    sys.path.insert(0, os.path.join(T, 'tools', 'colab'))
    import boot_bprime as BOOT
    S = {'versions': EX['versions'], 'weights_sha256': EX['weights_sha256']}
    EXp = os.path.join(OUT, 'ex-form.json')
    EXf = dict(EX, checks={k: True for k in EX['checks']})
    json.dump(EXf, open(EXp, 'w', encoding='utf-8'), ensure_ascii=False)
    good = BOOT.PH_form_items(EXp, C, S)
    bad_v = BOOT.PH_form_items(EXp, C, dict(S, versions={'numpy': 'x'}))
    json.dump(dict(EXf, checks=dict(EXf['checks'], g_match=False)), open(EXp, 'w', encoding='utf-8'), ensure_ascii=False)
    bad_c = BOOT.PH_form_items(EXp, C, S)
    check('四', '抽出の記録の形の項目（そろう・版・合否）', good == [] and bool(bad_v) and bool(bad_c), {'good': good, 'versions': bad_v, 'checks': bad_c})
    res.update(outs=outs, judge=jj, analysis=aj)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--skip-tiny', action='store_true')
    ap.add_argument('--keep', help='一時の置き場を残す（作業の確かめ用）')
    ap.add_argument('--only', help='走らせる部（例: 一四）。作業の確かめだけで、正式の記録には使わない（記録の名に work が付く）')
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    day = datetime.datetime.now(JST).strftime('%Y-%m-%d')
    work = bool(a.only or a.skip_tiny)
    out_md = os.path.join(BP, 'records', 'Bprime', ('dry-run-work-Bprime-%s.md' if work else 'dry-run-Bprime-%s.md') % day)
    out_js = out_md[:-3] + '.json'
    if os.path.exists(out_md) and not a.force:
        raise SystemExit('既にある（--force で上書き）: %s' % os.path.basename(out_md))
    t0 = time.time()
    table0 = closure_table(BP)
    td = a.keep or tempfile.mkdtemp(prefix='bprime-dry-')
    T, OUT = os.path.join(td, 'tree'), os.path.join(td, 'boot-out')
    os.makedirs(OUT, exist_ok=True)
    rows, P = PUBL.publish(T)
    check('〇', '公開の形の一時の置き場', len(rows) == len(P['publish']), '写した %d' % len(rows))
    want = lambda g: (a.only is None) or (g in a.only)
    if want('一'):
        part_selftests(T)
    if want('二') and not a.skip_tiny:
        part_tiny(T)
    if want('三'):
        part_independent(T)
    if want('四'):
        part_boot(T, OUT)
    table1 = closure_table(BP)
    same = table0 == table1
    check('〇', '走りの始めと終わりで器と正本と台帳の SHA16 が同じ', same, '' if same else sorted(k for k in set(table0) | set(table1) if table0.get(k) != table1.get(k)))
    n, k = len(ROWS), sum(1 for r in ROWS if r['ok'])
    L = ['# B′ の合成データの確かめの正式の記録（機械生成・`tools/dry_run_Bprime.py` %s・%s 日本時間）' % (VERSION, datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M')), '',
         '- 走らせた置き場: 移す器で作業の置き場から写した公開の形の一時の置き場（写した %d 本）。凍結の器は公開の置き場の版。transformers は分けた置き場の版。**実の重みは読まない**。' % len(rows),
         '- 確かめ: %d のうち %d が期待どおり（%s・%.0f 秒）。' % (n, k, '二の小さな模型の確かめを飛ばした作業の走り' if a.skip_tiny else '一〜四のすべて', time.time() - t0), '',
         '| 部 | 確かめ | 結果 | 値 |', '|---|---|---|---|']
    for r in ROWS:
        L.append('| %s | %s | %s | %s |' % (r['group'], r['name'].replace('|', '\\|'), '期待どおり' if r['ok'] else '**期待と違う**', r['detail'].replace('|', '\\|').replace(NL, ' ')))
    L += ['', '## 走らせた器と正本と台帳の SHA16（走りの始めと終わりで同じ）', '', '| 置き場 | SHA16 |', '|---|---|'] + ['| %s | %s |' % kv for kv in table1.items()] + ['', CLAUSE, '']
    with open(out_md, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(L))
    with open(out_js, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump({'kind': 'bprime_dry_run', 'version': VERSION, 'rows': ROWS, 'n': n, 'as_expected': k, 'skip_tiny': a.skip_tiny, 'sha16': table1, 'clause': CLAUSE}, fh, ensure_ascii=False, indent=1)
    if not a.keep:
        shutil.rmtree(td, ignore_errors=True)
    print('[dry_run_Bprime] %d のうち %d が期待どおり・記録 %s' % (n, k, os.path.relpath(out_md, BP)))


if __name__ == '__main__':
    main()
