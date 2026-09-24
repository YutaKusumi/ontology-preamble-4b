# -*- coding: utf-8 -*-
"""freeze_Bl3.py v1 —— B-lens 層三（Bl3）の凍結の記帳（2026-09-25・正本 `predictions.when`・`computation.main_freeze_check`・裁定 D210・D222・`tools/freeze_Blens.py` の型）。

相:
  prepilot  下見の前の凍結（正本のすべて・方向の npz・器・裁定 D210）。確かめてから記帳する（外れたら止める・登録者に相談）:
    - 凍結の本文: `tools/make_frozen_Bl3.py` の確かめ（草案3 との差は、題名・凍結の一行・組み立ての記録・正本と設計事実から来る行・原稿の直しだけ）と、数の検査の違反が零。
    - 正本: `decisions` に D226・D227 がある。設計事実の `contrasts_sha16` と方向の記録の `contrasts_sha16` が正本の SHA16 と同じ。
    - 方向の npz: 記録の SHA-256 と同じ・組ごとの SHA-256 が転記行 D と同じ・作り直してバイトで同じ（`tools/bl3_directions.py --check` を走らせる）。
    - 合成データの正式の記録（`records/Bl3/dry-run-Bl3-*.md` の最新）: 等方の本数が正本と同じで、確かめがすべて期待どおり。
    - 器の自己検査（`bl3_core`・`bl3_directions`・`make_predictions_form_Bl3`・`seal_Bl3`・`build_report_Bl3`・`make_frozen_Bl3`・`bl3_recompute_rewrite`）がすべて通る。
    - 予想の書式が組めて欄の確かめを通り、書式の正本の版が正本の版と同じ。封印はまだ無い（正本 predictions.when）。
    - Colab の起動器の相 check の出力（`--colab-check` の置き場の session.json と check.json）: DRY でない・順伝播を呼んでいない・版が正本 `inputs.versions_B` と文字列で同じ・
      GPU が L4 か A100・重みの SHA-256 が転記行 F と同じ・方向の npz の SHA-256 が記録と同じ・組ごとの SHA-256 が転記行 D と同じ・升目の入力が転記行 B と同じ・
      残差の書き換えの器を import できた・取り出したコミットの正本の SHA16 が今の正本と同じ。
    - 器の実装の検分の記録がある（`records/reviews/Bl3/impl/` の採否表・正本 `review_plan.impl`）。
    記帳: `records/Bl3/FREEZE-RECORD-Bl3.json`・`.md`（凍結物の SHA16・器の閉包・読む記録・方向の npz の SHA-256・確かめ）と、全体の台帳（`records/FREEZE-RECORD.md`）の一行。
    Colab の確かめの出力は `records/Bl3/colab-check-Bl3-session.json`・`colab-check-Bl3.json` に写す。
  main      本の凍結（下見の記録と機械の決定を凍結の記録に足す・正本 `computation.main_freeze_check`・裁定 D222）。確かめ:
    - 正本の SHA16 が下見の前の凍結と同じ（正本を変える直しはこの決まりの外で、登録者に上げる）。
    - 凍結物の SHA16 の違いが、凍結の記録の逸脱（`deviations` の `tool_diffs`: 置き場・前・後の SHA16）に記した差とすべて一致する。
    - 下見の試み（`--pilot` の置き場の pilot.json と session.json・試みの順）の session のコミットが、凍結の記録と封印の記録を含む（`git cat-file`）。
      下見の試みの session が DRY でない。最後の試みが本の凍結の下見（器の誤りの試みは、やり直したときの一度目として残す）。
    - 凍結の記録に足すのは `main_freeze` の鍵だけ（ほかの鍵は一字も変えない）。
    記帳: 凍結の記録の `main_freeze`（下見の試み・最後の試みの記録と機械の決定・session・凍結物の SHA16・器の差分・登録者の言葉と時刻）と、全体の台帳の一行。
用法: python tools/freeze_Bl3.py prepilot --words "<登録者の逐語>" --when "<日時（日本時間）>" --colab-check <相 check の出力の置き場> ／ prepilot --check-only
      python tools/freeze_Bl3.py main --words "<登録者の逐語>" --when "<日時（日本時間）>" --pilot <相 pilot の出力の置き場> [<二つ目> …]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, glob, json, shutil, hashlib, argparse, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)

VERSION = 'v1'
NL = chr(10)
FR_JSON = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
FR_MD = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.md')
CC_SESSION = os.path.join(REPO, 'records', 'Bl3', 'colab-check-Bl3-session.json')
CC_CHECK = os.path.join(REPO, 'records', 'Bl3', 'colab-check-Bl3.json')
LEDGER = os.path.join(REPO, 'records', 'FREEZE-RECORD.md')
SEAL = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
TOOLS = ['tools/bl3_core.py', 'tools/bl3_run.py', 'tools/bl3_directions.py', 'tools/analyze_Bl3.py', 'tools/dry_run_Bl3.py', 'tools/colab/boot_Bl3.py',
         'tools/bl3_recompute_rewrite.py', 'tools/build_report_Bl3.py', 'tools/sweep_Bl3.py', 'tools/make_predictions_form_Bl3.py', 'tools/seal_Bl3.py',
         'tools/make_frozen_Bl3.py', 'tools/freeze_Bl3.py', 'tools/bl3_facts.py', 'tools/make_contrasts_Bl3.py', 'tools/build_draft_Bl3.py']
SELFTESTS = [('tools/bl3_core.py', ['--selftest']), ('tools/bl3_directions.py', ['--selftest']), ('tools/make_predictions_form_Bl3.py', ['--selftest']),
             ('tools/seal_Bl3.py', ['--selftest']), ('tools/build_report_Bl3.py', ['--selftest']), ('tools/make_frozen_Bl3.py', ['--selftest']),
             ('tools/bl3_recompute_rewrite.py', ['--selftest'])]
rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
P = lambda r: os.path.join(REPO, *r.split('/'))
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 24), b''):
            h.update(blk)
    return h.hexdigest().upper()


def import_closure(tools):
    """器が import する（関数の中の import も含む）手元の器の閉包。"""
    out, todo = set(), list(tools)
    while todo:
        t = todo.pop()
        if t in out:
            continue
        out.add(t)
        for node in ast.walk(ast.parse(open(P(t), encoding='utf-8').read())):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split('.')[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = [node.module.split('.')[0]]
            for n in names:
                for cand in ('tools/%s.py' % n, 'tools/colab/%s.py' % n):
                    if os.path.exists(P(cand)) and cand not in out:
                        todo.append(cand)
    return sorted(out)


def frozen_files(T3):
    """凍結物（器の閉包を除く）: 正本・凍結の本文・設計事実・書式・方向・裁定と器の段の記録・読む記録（正本 `inputs.files`）。"""
    files = ['design/contrasts-Bl3.json', 'design/design-Bl3-FROZEN.md', 'design/design-Bl3-FROZEN.src.md', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md',
             'records/Bl3/numbers-lint-FROZEN-Bl3.md', 'records/Bl3/frozen-diff-Bl3.md', 'records/predictions/predictions-form-Bl3-v1.html', 'results/Bl3/directions-Bl3.json',
             'records/Bl3/tools/tools-log-Bl3.md', 'records/Bl3/tools/recompute-rewrite-dev-Bl3.md', 'records/Bl3/exposure-before-seal-Bl3.md']
    files += sorted(rel(p) for p in glob.glob(P('records/Bl3/rulings-D*.md')))
    files += sorted(rel(p) for p in glob.glob(P('records/reviews/Bl3/impl/*.md')))
    files += [v['path'] for v in T3['inputs']['files'].values()]
    out = []
    for f in files:
        if f not in out:
            out.append(f)
    return out


def latest_dry_run(T3):
    dr = sorted(glob.glob(P('records/Bl3/dry-run-Bl3-*.md')))
    if not dr:
        return None, ['合成データの正式の記録が無い（records/Bl3/dry-run-Bl3-<日付>.md）']
    txt = open(dr[-1], encoding='utf-8').read()
    m = re.search(r'確かめ: (\d+) のうち (\d+) が期待どおり', txt)
    n_iso = re.search(r'等方の方向の本数: (\d+)（正本 (\d+)）', txt)
    res = {'path': rel(dr[-1]), 'checks': int(m.group(1)) if m else None, 'as_expected': int(m.group(2)) if m else None, 'iso': int(n_iso.group(1)) if n_iso else None}
    bad = []
    if not m or m.group(1) != m.group(2) or '**期待と違う**' in txt:
        bad.append('合成データの記録に期待と違う確かめがある')
    if not n_iso or int(n_iso.group(1)) != T3['nulls']['isotropic']['count']:
        bad.append('合成データの正式の記録の等方の本数が正本と違う（正式の記録は正本の本数で走らせる）')
    return res, bad


def prepilot_checks(colab_dir=None):
    import make_frozen_Bl3 as MFB
    import make_predictions_form_Bl3 as FORM
    import bl3_directions as BD
    import numpy as np
    T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
    FJ = json.load(open(P('records/Bl3/design-facts-Bl3.json'), encoding='utf-8'))
    DJ = json.load(open(P('results/Bl3/directions-Bl3.json'), encoding='utf-8'))
    res, bad = {}, []
    canon16 = sha16f(P('design/contrasts-Bl3.json'))
    # 凍結の本文
    if not os.path.exists(MFB.FOUT):
        bad.append('凍結の本文が無い（make_frozen_Bl3 を先に走らせる）')
    else:
        r_, b_ = MFB.rebuild_and_check(MFB.FSRC, MFB.FOUT)
        res['frozen_text'] = {'canon_driven_lines': len(r_['canon_driven']), 'residual': None if r_['residual'] is None else len(r_['residual']), 'literal_fixes': len(MFB.LITERAL_FIXES)}
        bad += b_
        if '違反の合計: 0' not in open(MFB.LINT, encoding='utf-8').read():
            bad.append('凍結の本文の数の検査に違反がある')
    # 正本と設計事実と方向の記録
    res['canon'] = {'version': T3['version'], 'sha16': canon16, 'decisions_D226_D227': all(k in T3['decisions'] for k in ('D226', 'D227'))}
    if not res['canon']['decisions_D226_D227']:
        bad.append('正本の decisions に D226・D227 が無い')
    if FJ['contrasts_sha16'] != canon16 or DJ['contrasts_sha16'] != canon16:
        bad.append('設計事実か方向の記録の正本の SHA16 が今の正本と違う（作り直す）')
    # 方向の npz
    npz = P(DJ['npz'])
    npz_sha = sha256f(npz)
    Z = np.load(npz)
    try:
        grp = BD.verify_against_facts({g: Z[g] for g in BD.GROUPS}, FJ)
    except SystemExit as e_:
        bad.append(str(e_))
        grp = {}
    rchk = subprocess.run([sys.executable, P('tools/bl3_directions.py'), '--check'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO)
    res['directions'] = {'npz': DJ['npz'], 'sha256': npz_sha, 'groups': grp, 'rebuild_bytes_equal': rchk.returncode == 0}
    if npz_sha != DJ['npz_sha256'] or rchk.returncode != 0:
        bad.append('方向の npz の SHA-256 が記録と違うか、作り直してバイトで同じにならない')
    # 合成データ
    res['dry_run'], b_ = latest_dry_run(T3)
    bad += b_
    # 器の自己検査
    st = {}
    for t, args in SELFTESTS:
        r = subprocess.run([sys.executable, P(t)] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        st[t] = r.returncode == 0
    res['selftests'] = st
    bad += ['器の自己検査が落ちた: %s' % t for t, ok in st.items() if not ok]
    # 予想の書式・封印はまだ無い
    if not os.path.exists(FORM.OUT):
        bad.append('予想の書式が無い（make_predictions_form_Bl3 を先に走らせる）')
    else:
        h = open(FORM.OUT, encoding='utf-8').read()
        res['form'] = FORM.check(T3, h)
        if ("contrasts:'%s'" % T3['version']) not in h:
            bad.append('予想の書式の正本の版が今の正本と違う（組み直す）')
    for p in ('records/predictions/predictions-Bl3-coordinator.json', 'records/predictions/predictions-Bl3-registrant.json', 'records/Bl3/sealing-record-Bl3.json'):
        if os.path.exists(P(p)):
            bad.append('封印が凍結より先にある（正本 predictions.when と違う）: %s' % p)
    # 器の実装の検分
    impl = sorted(glob.glob(P('records/reviews/Bl3/impl/adoption-table-*.md')))
    res['impl_review'] = [rel(x) for x in impl]
    if not impl:
        bad.append('器の実装の検分の採否表が無い（records/reviews/Bl3/impl/・正本 review_plan.impl）')
    # Colab の確かめ
    if colab_dir is not None:
        S = json.load(open(os.path.join(colab_dir, 'session.json'), encoding='utf-8'))
        CK = json.load(open(os.path.join(colab_dir, 'check.json'), encoding='utf-8'))
        pins = T3['inputs']['versions_B']
        c = {'kind_check': S.get('kind') == 'bl3_colab_check', 'not_dry': S.get('dry') is False, 'no_forward': CK.get('forward_calls') == 0,
             'versions': all((S.get('versions') or {}).get(k) == pins[k] for k in ('numpy', 'torch', 'transformers')),
             'gpu': any(g in str(S.get('gpu')) for g in ('L4', 'A100')), 'weights': S.get('weights_sha256') == FJ['facts']['F']['sha256'],
             'npz': S.get('directions_npz_sha256') == npz_sha, 'groups': (S.get('directions_group_sha256') or {}) == grp and bool(grp),
             'cells': all((CK['cells'].get(k) or {}).get(x) == v[y] for k, v in FJ['facts']['B']['cells'].items() for x, y in (('prompt_len', 'prompt_len'), ('main_position', 'main_position'), ('readout_position', 'readout_position'), ('family', 'family'))),
             'rewrite_importable': CK.get('rewrite_importable') is True, 'canon_at_commit': S.get('canon_sha16') == canon16}
        res['colab_check'] = dict(c, commit=S.get('commit'), gpu_name=S.get('gpu'), versions_seen=S.get('versions'))
        bad += ['Colab の確かめ: %s' % k for k, v in c.items() if not v]
    return T3, res, bad


def prepilot(words, when, colab_dir, force=False):
    T3, res, bad = prepilot_checks(colab_dir)
    print(json.dumps({k: v for k, v in res.items() if k != 'selftests'}, ensure_ascii=False, indent=1, default=str)[:6000])
    if bad:
        raise SystemExit('下見の前の凍結の確かめが外れた（止める・登録者に相談）: %s' % bad)
    if colab_dir is None:
        print('[freeze_Bl3] 確かめだけ（Colab の確かめを除く）: 外れ無し')
        return
    if os.path.exists(FR_JSON) and not force:
        raise SystemExit('既にある: %s' % rel(FR_JSON))
    shutil.copyfile(os.path.join(colab_dir, 'session.json'), CC_SESSION)
    shutil.copyfile(os.path.join(colab_dir, 'check.json'), CC_CHECK)
    tools = import_closure(TOOLS)
    files = frozen_files(T3) + [res['dry_run']['path'], rel(CC_SESSION), rel(CC_CHECK)]
    frozen = {r: sha16f(P(r)) for r in files + tools}
    R = {'kind': 'bl3_freeze_record', 'version': VERSION, 'stage': 'prepilot', 'frozen_jst': when, 'registrant_words': words, 'rulings': sorted(k for k in T3['decisions'] if k >= 'D204'),
         'frozen_sha16': frozen, 'tools_import_closure': tools, 'directions_npz_sha256': res['directions']['sha256'], 'checks': res,
         'deviation_rule': '凍結の後の変更は、逸脱として番号・日付・理由・登録者の承認を台帳（この記録の deviations）に記す。器の差分は tool_diffs に置き場・前・後の SHA16 を記す（正本 computation.main_freeze_check）',
         'deviations': [],
         'next': '記録先行の公開（push）→ 予想の封印（コーディネータが先・SHA だけを伝える → 登録者）→ Colab の相 pilot → 本の凍結（下見の記録と機械の決定を足す）→ Colab の相 main → 一致だけを見る段 → 結果を登録者と一緒に開く',
         'clause': CLAUSE}
    json.dump(R, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    md = ['# B-lens 層三の下見の前の凍結の記録（機械生成・`tools/freeze_Bl3.py` %s）' % VERSION, '',
          '- 凍結: %s（日本時間）・登録者の言葉は逐語で「%s」。' % (when, words),
          '- 本文: `design/design-Bl3-FROZEN.md`（SHA16 %s）・草案3 との差は `records/Bl3/frozen-diff-Bl3.md`。' % frozen['design/design-Bl3-FROZEN.md'],
          '- 正本: 版 %s（SHA16 %s）。方向の npz: `%s`（SHA-256 %s）。' % (T3['version'], frozen['design/contrasts-Bl3.json'], res['directions']['npz'], res['directions']['sha256']),
          '- Colab の確かめ（相 check・コミット %s・%s）: %s。' % (res['colab_check']['commit'], res['colab_check']['gpu_name'], '・'.join('%s %s' % (k, '合う' if v else '外れ') for k, v in res['colab_check'].items() if isinstance(v, bool))),
          '- 合成データ: `%s`（確かめ %s・期待どおり %s）。' % (res['dry_run']['path'], res['dry_run']['checks'], res['dry_run']['as_expected']),
          '- 次: ' + R['next'], '', '## 凍結物の SHA16', '', '| 置き場 | SHA16 |', '|---|---|'] + ['| `%s` | %s |' % kv for kv in sorted(frozen.items())] + ['', CLAUSE, '']
    open(FR_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(md))
    row = ('| %s | **B-lens 層三 下見の前の凍結**（登録者「%s」%s 日本時間・裁定 D210）: 草案3 の原稿に裁定 D226・D227 の直しを入れて design/design-Bl3-FROZEN.md を組み、正本・方向の npz・器を凍結した。'
           '凍結の記録 records/Bl3/FREEZE-RECORD-Bl3.json（凍結物 %d 件・器の閉包 %d）。封印はこの後（コーディネータが先）。 | design/design-Bl3-FROZEN.md | %s | 凍結の後の変更は逸脱として台帳に記す |'
           % (when.split(' ')[0], words, when, len(frozen), len(tools), frozen['design/design-Bl3-FROZEN.md']))
    led = open(LEDGER, encoding='utf-8').read()
    if 'B-lens 層三 下見の前の凍結' not in led:
        open(LEDGER, 'a', encoding='utf-8', newline=NL).write(('' if led.endswith(NL) else NL) + row + NL)
    print('[freeze_Bl3] 下見の前の凍結を記帳した: %s・%s（凍結物 %d）' % (rel(FR_JSON), rel(FR_MD), len(frozen)))


def in_commit(commit, path):
    return subprocess.run(['git', '-C', REPO, 'cat-file', '-e', '%s:%s' % (commit, path)], capture_output=True).returncode == 0


def main_freeze_checks(FR, pilot_dirs):
    bad, res = [], {}
    frozen = FR['frozen_sha16']
    canon = 'design/contrasts-Bl3.json'
    if sha16f(P(canon)) != frozen[canon]:
        bad.append('正本の SHA16 が下見の前の凍結から変わった（正本を変える直しは本の凍結の決まりの外・登録者に上げる）')
    ledgered = {}
    for d in FR.get('deviations') or []:
        for td in d.get('tool_diffs') or []:
            ledgered[td['path']] = td
    now_sha = {}
    for pth, want in frozen.items():
        got = sha16f(P(pth)) if os.path.exists(P(pth)) else None
        now_sha[pth] = got
        if got != want:
            td = ledgered.get(pth)
            if not td or td.get('before') != want or td.get('after') != got:
                bad.append('凍結物の SHA16 の違いが逸脱の台帳の器の差分と合わない: %s（凍結 %s・今 %s）' % (pth, want, got))
    res['changed'] = sorted(p for p in frozen if now_sha[p] != frozen[p])
    res['ledgered_not_changed'] = sorted(p for p in ledgered if now_sha.get(p) == frozen.get(p))
    if res['ledgered_not_changed']:
        bad.append('台帳に記した器の差分が凍結物に現れない: %s' % res['ledgered_not_changed'])
    atts, sessions = [], []
    for d in pilot_dirs:
        PJ = json.load(open(os.path.join(d, 'pilot.json'), encoding='utf-8'))
        S = json.load(open(os.path.join(d, 'session.json'), encoding='utf-8'))
        if S.get('dry') or S.get('kind') != 'bl3_colab_pilot':
            bad.append('下見の試みの出力が DRY か、相 pilot の出力でない: %s' % d)
        c = S.get('commit') or ''
        if not (re.fullmatch(r'[0-9a-f]{40}', c) and in_commit(c, 'records/Bl3/FREEZE-RECORD-Bl3.json') and in_commit(c, 'records/Bl3/sealing-record-Bl3.json')):
            bad.append('下見の試みのコミットが、凍結の記録と封印の記録を含むコミットでない: %s' % c)
        atts.append(PJ['pilot'])
        sessions.append({k: S.get(k) for k in ('commit', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'finished')})
    if not atts:
        bad.append('下見の試みが無い')
    elif atts[-1].get('tool_error'):
        bad.append('最後の下見の試みが器の誤り（本の凍結の前に登録者の裁定を仰ぐ）')
    res['n_attempts'] = len(atts)
    return atts, sessions, now_sha, res, bad


def main_freeze(words, when, pilot_dirs):
    FR = json.load(open(FR_JSON, encoding='utf-8'))
    if 'main_freeze' in FR:
        raise SystemExit('本の凍結は既にある')
    if not os.path.exists(SEAL):
        raise SystemExit('封印の記録が無い（本の凍結は封印と下見の後）')
    atts, sessions, now_sha, res, bad = main_freeze_checks(FR, pilot_dirs)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if bad:
        raise SystemExit('本の凍結の確かめが外れた（止める・登録者に相談）: %s' % bad)
    before = {k: v for k, v in FR.items()}
    FR['main_freeze'] = {'frozen_jst': when, 'registrant_words': words, 'pilot_attempts': atts, 'pilot': atts[-1], 'decision': atts[-1].get('decision'),
                         'sessions': sessions, 'frozen_sha16': now_sha, 'tool_diffs_applied': res['changed'], 'freeze_tool': 'tools/freeze_Bl3.py %s' % VERSION}
    assert all(FR[k] == before[k] for k in before), '本の凍結でほかの鍵が変わった'
    assert set(FR) - set(before) == {'main_freeze'}
    json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    dec = atts[-1].get('decision') or {}
    add = ['', '## 本の凍結（下見の記録と機械の決定を足した・正本 computation.main_freeze_check）', '',
           '- 本の凍結: %s（日本時間）・登録者の言葉は逐語で「%s」。' % (when, words),
           '- 下見の試み %d・最後の試みの機械の決定: %s（外した升目: %s）。' % (len(atts), dec.get('q1'), '・'.join(dec.get('dropped') or []) or 'なし'),
           '- 凍結物の SHA16 の違い（逸脱の台帳の器の差分と一致）: %s。' % ('・'.join(res['changed']) or '無し'), '', CLAUSE, '']
    md = open(FR_MD, encoding='utf-8').read().rstrip(NL)
    if md.endswith(CLAUSE):
        md = md[: -len(CLAUSE)].rstrip(NL)
    open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md + NL + NL.join(add))
    row = ('| %s | **B-lens 層三 本の凍結**（登録者「%s」%s 日本時間・裁定 D210・D222）: 下見の記録と機械の決定（%s）を凍結の記録に足した。器の差分 %d（逸脱の台帳と一致）。 | records/Bl3/FREEZE-RECORD-Bl3.json | %s | 以後の変更は逸脱として台帳に記す |'
           % (when.split(' ')[0], words, when, dec.get('q1'), len(res['changed']), sha16f(FR_JSON)))
    led = open(LEDGER, encoding='utf-8').read()
    if 'B-lens 層三 本の凍結' not in led:
        open(LEDGER, 'a', encoding='utf-8', newline=NL).write(('' if led.endswith(NL) else NL) + row + NL)
    print('[freeze_Bl3] 本の凍結を記帳した: %s（下見の試み %d）' % (rel(FR_JSON), len(atts)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=['prepilot', 'main'])
    ap.add_argument('--words')
    ap.add_argument('--when')
    ap.add_argument('--colab-check', help='相 check の出力の置き場（session.json と check.json）')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--pilot', nargs='*', help='相 pilot の出力の置き場（試みの順）')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if a.stage == 'prepilot':
        if a.check_only:
            return prepilot(None, None, None)
        if not (a.words and a.when and a.colab_check):
            raise SystemExit('--words・--when・--colab-check が要る')
        return prepilot(a.words, a.when, a.colab_check, a.force)
    if not (a.words and a.when and a.pilot):
        raise SystemExit('--words・--when・--pilot が要る')
    main_freeze(a.words, a.when, a.pilot)


if __name__ == '__main__':
    main()
