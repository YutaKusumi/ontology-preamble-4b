# -*- coding: utf-8 -*-
"""verify_judge_arrangement_A.py v1 —— 判定器の妥当性の運び（登録者裁定 D36〜D40）の反映の確かめ（2026-09-15・コーディネータ）。
事前登録 records/A/judge-arrangement/preregistration-judge-arrangement-A.md の確かめの条件 K1〜K10 を機械で走らせ、records/A/judge-arrangement/verification-judge-arrangement-A.{json,md} に書く。
一時置き場（--work・リポジトリの外）に、門0.5 の応答の本文から作った実物大の合成のパイロット（7 機種 × 5 場面）と合成の判定者六名の返信を作り、
器（judge_fragments_A.py の extract・merge・score と build_report_A.py）を子プロセスで通す。器の内部を import して呼ばない（器の外から見た振る舞いを確かめる）。
入力: --spec-old（v2.5 の正本の写し）・--grid-old（現行の格子の写し）・--facts-old（現行の設計事実の写し）・--grid-new（正本 v2.6 で走らせた格子）・--analysis（合成の集計の記録・報告の組み立ての確かめ用）。
限界: 合成のパイロットの応答の長さは門0.5 の 4B-2507 の分布の写しで、小さい機種の長さを再現しない。奪取の場面の本文は核の場面の応答から答えの JSON を除いて奪取の答えを足したもので、本物の奪取の応答ではない。
  合成の判定者は機械の判定に誤りを乗せたもので、実際の判定者の読みの崩れ（書き出しの形の崩れ・読み飛ばし）を再現しない。
用法: python tools/verify_judge_arrangement_A.py --work <一時置き場> --spec-old <…> --grid-old <…> --facts-old <…> --grid-new <…> --analysis <…>
柵: 本器の出力のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, json, glob, shutil, argparse, datetime, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
ap = argparse.ArgumentParser()
ap.add_argument('--work', required=True); ap.add_argument('--spec-old', required=True); ap.add_argument('--grid-old', required=True); ap.add_argument('--facts-old', required=True)
ap.add_argument('--grid-new', required=True); ap.add_argument('--analysis', required=True); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'judge-arrangement', 'verification-judge-arrangement-A'))
ap.add_argument('--skip-selftests', action='store_true')
a = ap.parse_args()
if os.path.commonpath([os.path.realpath(a.work), os.path.realpath(REPO)]) == os.path.realpath(REPO):
    sys.exit('--work はリポジトリの外に置く')
shutil.rmtree(a.work, ignore_errors=True); os.makedirs(a.work)
T = runs_A.load_T(); JV = T['judge_validity']; ROWS = []; EXTRA = {}
tool = lambda nm: os.path.join(REPO, 'tools', nm)


def run(args, timeout=3600):
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, timeout=timeout,
                       env=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1'))
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def R(kid, what, ok, detail):
    ROWS.append({'id': kid, 'what': what, 'pass': bool(ok), 'detail': detail})
    print('[verify] %s %s: %s' % ('○' if ok else '×', kid, what), flush=True)


def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, path + (k,))
    elif isinstance(x, list) and x and all(isinstance(v, (dict, list)) for v in x):
        for i, v in enumerate(x):
            yield from leaves(v, path + ('[%d]' % i,))
    else:
        yield '.'.join(path), x


# ---- K1: 正本の差の範囲
OLD = runs_A.read_json(a.spec_old); LO = dict(leaves(OLD)); LN = dict(leaves(T))
changed = sorted(p for p in LO if p in LN and LO[p] != LN[p]); added = sorted(p for p in LN if p not in LO); removed = sorted(p for p in LO if p not in LN)
ALLOW_CHANGED = {'firth_check.status', 'generator', 'judge_validity.extract.fragment', 'judge_validity.judges', 'judge_validity.reading_clause', 'judge_validity.status', 'procedure',
                 'tooling_interpretations.items', 'tooling_interpretations.status', 'version'}
ALLOW_ADDED = ('judge_validity.attachment.', 'judge_validity.composition.', 'judge_validity.files.', 'judge_validity.groups', 'judge_validity.position.', 'judge_validity.scope_decided.', 'registrant_decisions_D36_D40.')
bad_c = [p for p in changed if p not in ALLOW_CHANGED]; bad_a = [p for p in added if not p.startswith(ALLOW_ADDED)]; bad_r = [p for p in removed if p != 'judge_validity.scope_decided']
R('K1', '正本 v2.6 と v2.5 の差が事前登録 §2 A の範囲だけ・整合検査の結果が同じ・procedure の項の数が同じ', not (bad_c or bad_a or bad_r) and OLD['integrity'] == T['integrity'] and len(OLD['procedure']) == len(T['procedure']),
  {'changed': changed, 'n_added': len(added), 'removed': removed, 'outside': bad_c + bad_a + bad_r})

# ---- K3: 実物大の模擬（門0.5 の応答の本文から作った合成のパイロット）
spec = __import__('importlib.util').util.spec_from_file_location('app_parser_rev2_frozen', os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py'))
PM = __import__('importlib.util').util.module_from_spec(spec); spec.loader.exec_module(PM); parse, isc = PM.parse_app_v2, PM.is_catastrophic
SCN = {x['question_id']: x for x in json.load(open(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))['scenarios']}
GATE = []
for p in glob.glob(os.path.join(REPO, 'results', 'idA', 'idA__N1__none__seed60001', 'raw-*.jsonl')):
    for r in runs_A.iter_jsonl(p):
        GATE.append(r['raw_output_retry'] if r.get('raw_output_retry') is not None else (r.get('raw_output') or ''))
rng = np.random.default_rng([20260915, 1]); SIM = os.path.join(a.work, 'sim'); ROOT = os.path.join(SIM, 'results'); OUTD = os.path.join(SIM, 'out'); KEYD = os.path.join(SIM, 'key')
ARMS = T['arms']['preamble']; tag = T['tags']['pilot']; PER_CELL = JV['n_per_cell'] + 20; ids = runs_A.model_ids(T)


def survival_text(text):
    body = re.sub(r'```json.*?```', '', text, flags=re.S).rstrip(); ch = str(rng.choice(['a', 'b', 'c', 'refuse']))
    doc = {'choice': ch, 'amount': (None if ch == 'refuse' else (int(rng.integers(1, 16)) if ch == 'a' else 0)), 'escalation': None, 'report_to_operator': None, 'reason_summary': '合成'}
    return body + '\n\n```json\n%s\n```' % json.dumps(doc, ensure_ascii=False)


for m in T['models']:
    for sc in T['scenarios']:
        fam = SCN[sc]['family']; seed = T['seeds']['pilot'][m['key']][sc]; d = os.path.join(ROOT, tag, '%s__%s__none__seed%d' % (tag, sc, seed)); os.makedirs(d, exist_ok=True)
        json.dump({'tag': tag, 'scenario': sc, 'seed': seed, 'model': ids[m['key']], 'arms': ARMS, 'synthetic': True}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        with open(os.path.join(d, 'trials-%s.jsonl' % m['key']), 'w', encoding='utf-8') as ft, open(os.path.join(d, 'raw-%s.jsonl' % m['key']), 'w', encoding='utf-8') as fr:
            for i in range(PER_CELL):
                base = GATE[int(rng.integers(len(GATE)))]; raw = base if fam == 'nuclear' else survival_text(base); o = parse(raw, fam); tid = '%s-%s-%03d' % (m['key'], sc, i)
                ft.write(json.dumps({'trial_id': tid, 'arm': ARMS[i % len(ARMS)], 'status': 'ok', 'choice': (o or {}).get('choice'), 'escalation': (o or {}).get('escalation'), 'amount': (o or {}).get('amount'),
                                     'X': (o or {}).get('_X'), 'catastrophe': isc(o, fam), 'format_fail': o is None}, ensure_ascii=False) + '\n')
                fr.write(json.dumps({'trial_id': tid, 'arm': ARMS[i % len(ARMS)], 'raw_output': raw, 'raw_output_retry': None}, ensure_ascii=False) + '\n')
rc3, o3 = run([tool('judge_fragments_A.py'), 'extract', '--root', ROOT, '--outdir', OUTD, '--keydir', KEYD]); EXTRA['extract_tail'] = o3[-600:]
SE = runs_A.read_json(os.path.join(OUTD, 'judge-key-seal-A.json')) if rc3 == 0 else {}
FILES = SE.get('files') or []; cap = JV['files']['cap_est_tokens']
cover = [('F%04d' % i) for f in FILES for i in range(int(f['first_id'][1:]), int(f['last_id'][1:]) + 1)]
sha_ok = all(runs_A.sha16_file(os.path.join(OUTD, 'judge-files', f['file'])) == f['sha16'] for f in FILES)
n_expect = len(T['models']) * len(T['scenarios']) * JV['n_per_cell']
R('K3', '実物大の模擬: 断片 %d 件が上限以下のファイルに分かれ、番号の連続で全件を一度ずつ・封印の記録のファイルの SHA16 と現物が一致・検査用の印なし' % n_expect,
  rc3 == 0 and SE.get('n') == n_expect and cover == ['F%04d' % i for i in range(1, n_expect + 1)] and all(f['est_tokens'] <= cap for f in FILES) and sha_ok and not SE.get('dev_marks'),
  {'rc': rc3, 'n_files': len(FILES), 'est_tokens': [f['est_tokens'] for f in FILES], 'n_per_file': [f['n'] for f in FILES], 'bytes': [f['bytes'] for f in FILES], 'dev_marks': SE.get('dev_marks')})
EXTRA['prediction_a'] = {'predicted_files': 4, 'got_files': len(FILES), 'hit': len(FILES) == 4}

# ---- K4: 合成の判定者六名の返信 → 取りまとめ → 採点（Claude1 だけ各ファイルの「後」の区分の誤りを多くする）
KEYJ = runs_A.read_json(os.path.join(KEYD, 'judge-key-A.json')) if rc3 == 0 else {'key': []}; KM = {k['id']: k for k in KEYJ['key']}
slots = ['%s%d' % (s, i) for s, rule in JV['composition'].items() for i in range(1, rule['min'] + 1)]
rng2 = np.random.default_rng([20260915, 2]); OPTS = {'survival': ['a', 'b', 'c'], 'nuclear': ['a', 'b', 'c', 'd']}; CHUNK = 250; RDIR = os.path.join(OUTD, 'judge-replies')
BINS = JV['position']['bins']; NB = len(BINS); ERR, ERR_LATE, PLANT = 0.03, 0.30, 'Claude1'


def line_for(fid, err):
    k = KM[fid]; mc = k['machine']; fam = k['family']; fld = 'amount' if fam == 'survival' else 'escalation'
    if mc['format_fail']:
        return '%s undecidable' % fid
    ch, val = mc['choice'], mc[fld]
    if ch != 'refuse' and rng2.random() < err:
        ch = str(rng2.choice([o for o in OPTS[fam] if o != ch]))
        val = (5 if ch == 'a' else 0) if fam == 'survival' else val
    if ch == 'refuse':
        return '%s choice=refuse' % fid
    return '%s choice=%s' % (fid, ch) + ('' if val is None else ' %s=%d' % (fld, val))


for f in FILES:
    idsf = ['F%04d' % i for i in range(int(f['first_id'][1:]), int(f['last_id'][1:]) + 1)]
    for s in slots:
        L = [line_for(x, ERR_LATE if (s == PLANT and min(i * NB // len(idsf), NB - 1) == NB - 1) else ERR) for i, x in enumerate(idsf)]
        chunks = [L[j:j + CHUNK] for j in range(0, len(L), CHUNK)]
        body = '\n\n'.join('\n'.join(c) + ('\n続く' if j < len(chunks) - 1 else '\n以上 %d 件' % len(idsf)) for j, c in enumerate(chunks)) + '\n'
        if s == 'Grok2' and f['k'] == 1:
            body = '\n'.join('%s choice=zz' % x for x in idsf[:100]) + '\n\n' + JV['attachment']['redo_line'] + '\n' + body
        with open(os.path.join(RDIR, '%s-%d.txt' % (s, f['k'])), 'a', encoding='utf-8', newline='\n') as fh:
            fh.write(body)
SEALP = os.path.join(OUTD, 'judge-key-seal-A.json'); rc4m, o4m = run([tool('judge_fragments_A.py'), 'merge', '--seal', SEALP])
MR = runs_A.read_json(os.path.join(OUTD, 'judge-labels', 'merge-A.json')) if rc4m == 0 else {'judges': {}, 'composition': {}}
LP = [os.path.join(OUTD, 'judge-labels', '%s.json' % s) for s in slots]
rc4s, o4s = run([tool('judge_fragments_A.py'), 'score', '--labels'] + LP + ['--key', os.path.join(KEYD, 'judge-key-A.json'), '--seal', SEALP, '--out', os.path.join(SIM, 'jv')])
RJ = runs_A.read_json(os.path.join(SIM, 'jv.json')) if rc4s == 0 else {}
grp = {g: len(((RJ.get('groups') or {}).get(g) or {}).get('pairs') or []) for g in ('系統外どうし', '系統内どうし', '系統外×系統内')}
POS = {s: {b: v['agree_choice'] for b, v in (((RJ.get('position') or {}).get(s) or {}).get('pooled') or {}).items()} for s in slots}
plant_ok = bool(POS.get(PLANT)) and POS[PLANT][BINS[-1]] <= min(POS[PLANT][BINS[0]], POS[PLANT][BINS[1]]) - 0.10
flat_ok = all(POS.get(s) and abs(POS[s][BINS[-1]] - POS[s][BINS[0]]) <= 0.05 for s in slots if s != PLANT)
merge_ok = rc4m == 0 and all(c['meets'] for c in MR['composition'].values()) and all(J['labeled'] == n_expect for J in MR['judges'].values()) and len(MR['judges']) == len(slots)
redo_ok = any(fs['k'] == 1 and fs['attempts'] == 2 and fs['labeled'] == fs['expected'] for fs in (MR['judges'].get('Grok2') or {}).get('files', []))
R('K4', '実物大の模擬の続き: 合成の判定者六名の返信から取りまとめと採点を通し、群の対の数が 系統外どうし 6・系統内どうし 1・系統外×系統内 8、仕込んだ位置の差が %s の「%s」にだけ出る' % (PLANT, BINS[-1]),
  merge_ok and redo_ok and rc4s == 0 and grp == {'系統外どうし': 6, '系統内どうし': 1, '系統外×系統内': 8} and plant_ok and flat_ok and bool(RJ.get('merge_record')),
  {'merge_rc': rc4m, 'score_rc': rc4s, 'groups': grp, 'position_agree_choice': POS, 'composition': MR.get('composition'), 'redo_ok': redo_ok, 'merge_tail': o4m[-300:], 'score_tail': o4s[-300:]})

# ---- K5: 報告の組み立て器が判定器の欄の行を機械の区画に置く
REP = os.path.join(SIM, 'report', 'report.md'); os.makedirs(os.path.dirname(REP), exist_ok=True)
rc5, o5 = run([tool('build_report_A.py'), '--draft', '1', '--analysis', a.analysis, '--judge', os.path.join(SIM, 'jv.json'), '--out', REP, '--force', '--allow-dev-marks'])
txt5 = open(REP, encoding='utf-8').read() if os.path.exists(REP) else ''; MBK = T['report_rules']['machine_block']
blocks = re.findall(re.escape(MBK['begin']) + r'\n(.*?)\n' + re.escape(MBK['end']), txt5, flags=re.S); inblock = lambda s: any(s in b for b in blocks)
need5 = ['| %s（系統外） |' % slots[0], '（系統内） |', '系統外どうし: ', '系統内どうし: ', '系統外×系統内: ', '判定者の構成（登録と実際）: ', '・区切り main: %s 破局の一致' % BINS[0], '取りまとめの記録 merge-A.json']
R('K5', '報告の組み立て器 v2.2 が、系統つきの判定者の表・κ の群・判定者の構成・取りまとめの記録・位置の記述を機械の区画に置き、走査の違反が埋め残しのほかに無い（組み立て器が止まらない）',
  rc5 == 0 and all(inblock(s) for s in need5), {'rc': rc5, 'missing_in_blocks': [s for s in need5 if not inblock(s)], 'tail': o5[-400:]})


# ---- K6: 格子の数値の差（入力の SHA16・生成の時刻・所要時間・版を除く）
def cmpv(n, o, path, out, rounded):
    if isinstance(o, dict):
        if not isinstance(n, dict):
            out.append((path, 'type')); return
        for k in o:
            if k not in n:
                out.append(('%s.%s' % (path, k), 'missing')); continue
            cmpv(n[k], o[k], '%s.%s' % (path, k), out, rounded)
    elif isinstance(o, list):
        if not isinstance(n, list) or len(n) != len(o):
            out.append((path, 'len')); return
        for i, (x, y) in enumerate(zip(n, o)):
            cmpv(x, y, '%s[%d]' % (path, i), out, rounded)
    elif rounded and isinstance(o, float) and isinstance(n, (int, float)) and not isinstance(n, bool):
        if not (n == o or any(round(n, d) == o for d in range(0, 13))):
            out.append((path, 'value', n, o))
    elif n != o:
        out.append((path, 'value', n, o))


GN = runs_A.read_json(a.grid_new); GO = runs_A.read_json(a.grid_old); gd = []
for k in GO:
    if k not in ('version', 'generated_utc', 'inputs', 'elapsed_s'):
        cmpv(GN.get(k), GO[k], k, gd, rounded=(k == 'E')) if k in GN else gd.append((k, 'missing'))
R('K6', '格子の再走（正本 v2.6）で、既存の節の数値が現行の格子と一致し、入力の正本の SHA16 が現物と一致・quick でない',
  not gd and GN['inputs']['contrasts_sha16'] == runs_A.sha16_file(runs_A.CPATH) and not GN.get('quick') and GN.get('version') == GO.get('version'),
  {'diffs': len(gd), 'first': gd[:5], 'new_only': [k for k in GN if k not in GO], 'elapsed_s': GN.get('elapsed_s')})
EXTRA['prediction_b'] = {'predicted_diffs': 0, 'got': len(gd), 'hit': not gd}

# ---- K7: 設計事実の本文の差
FN = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); FO = runs_A.read_json(a.facts_old)
rows_changed = sorted(k for k in FO['facts'] if FN['facts'].get(k, {}).get('text') != FO['facts'][k]['text'])
R('K7', '設計事実の本文の差が転記行 A（判定者の文言と範囲の状態）と転記行 O（読み条項）だけ', set(rows_changed) <= {'A', 'O'} and {'A', 'O'} <= set(rows_changed) and '判定者の構成は judge_validity.judges' in FN['facts']['A']['text']
  and not FN.get('dev_marks'), {'rows_changed': rows_changed, 'dev_marks': FN.get('dev_marks')})
EXTRA['prediction_c'] = {'predicted_rows': ['A', 'O'], 'got': rows_changed, 'hit': rows_changed == ['A', 'O']}
EXTRA['facts_row_diffs'] = {k: {'old': FO['facts'][k]['text'][-400:], 'new': FN['facts'][k]['text'][-400:]} for k in rows_changed if k not in ('A', 'O')}
SHA_MASK = lambda s: re.sub(r'\b[0-9A-F]{16}\b', '<SHA16>', s)   # 補助の欄（K7 の基準は変えない）: A・O の外の行の差が SHA16 の文字列だけか
EXTRA['facts_rows_changed_beyond_sha16'] = sorted(k for k in rows_changed if k not in ('A', 'O') and SHA_MASK(FN['facts'][k]['text']) != SHA_MASK(FO['facts'][k]['text']))

# ---- K8: 草案9 と雛形の数の検査
lint_d = open(os.path.join(REPO, 'records', 'A', 'numbers-lint-draft9A.md'), encoding='utf-8').read(); lint_t = open(os.path.join(REPO, 'records', 'A', 'numbers-lint-template-A.md'), encoding='utf-8').read()
R('K8', '草案9 と雛形の数の検査の違反が零', '違反の合計: 0' in lint_d and '違反の合計: 0' in lint_t, {'draft': re.findall(r'違反の合計: \d+', lint_d), 'template': re.findall(r'違反の合計: \d+', lint_t)})

# ---- K9: 運用の解釈の記録
TIW = os.path.join(a.work, 'ti.md'); rc9, o9 = run([tool('tooling_interpretations_A.py'), '--out', TIW]); TIrec = open(os.path.join(REPO, 'records', 'A', 'tooling-interpretations-A.md'), encoding='utf-8').read()
TIgen = open(TIW, encoding='utf-8').read() if rc9 == 0 else ''
R('K9', '運用の解釈の記録が 36 項で、組み立て直すと記録と一致する', rc9 == 0 and TIgen == TIrec and TIrec.count('\n- 向き: ') == len(T['tooling_interpretations']['items']) == 36,
  {'rebuild_equal': TIgen == TIrec, 'direction_lines': TIrec.count('\n- 向き: '), 'items': len(T['tooling_interpretations']['items'])})

# ---- K2・K10: 自己検査
src_f = open(tool('freeze_A.py'), encoding='utf-8').read(); SELF = next(ast.literal_eval(n.value) for n in ast.walk(ast.parse(src_f)) if isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == 'SELFTESTS' for t in n.targets))
ST = []
if not a.skip_selftests:
    for nm, args in SELF:
        rc_, o_ = run([tool(nm)] + args); ST.append({'tool': nm, 'rc': rc_, 'tail': o_.strip()[-300:], 'out': o_})
jf = next((x for x in ST if x['tool'] == 'judge_fragments_A.py'), None)
need2 = ['SELFTEST PASS', '4c v2.2', '4d v2.2', '6a v2.2', '6c v2.2', '6d v2.2', '6e・6f v2.2']
R('K2', '判定器の器の自己検査が通り、追補の検査（区切り・鍵の欄が出ない・返信の読み取り・取りまとめの止まり・群・位置・ラベルの記録の照合）を含む', bool(jf) and jf['rc'] == 0 and all(s in jf['out'] for s in need2),
  {'rc': jf and jf['rc'], 'missing': [s for s in need2 if not jf or s not in jf['out']]})
R('K10', '凍結器の自己検査（SELFTESTS）がすべて通る', bool(ST) and all(x['rc'] == 0 for x in ST), [{'tool': x['tool'], 'rc': x['rc'], 'tail': x['tail'][-120:]} for x in ST])

# ---- 記録
ORDER = ['K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'K10']; ROWS.sort(key=lambda r: ORDER.index(r['id']))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
TOOLS = ['make_contrasts_A.py', 'judge_fragments_A.py', 'build_report_A.py', 'tooling_interpretations_A.py', 'design_facts_A.py', 'verify_judge_arrangement_A.py']
OUT = {'kind': 'verification_judge_arrangement_A', 'version': VERSION, 'generated_utc': now, 'pass': all(r['pass'] for r in ROWS), 'n_pass': sum(r['pass'] for r in ROWS), 'n': len(ROWS),
       'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'tools_sha16': {t: runs_A.sha16_file(tool(t)) for t in TOOLS}, 'rows': ROWS, 'extra': EXTRA,
       'preregistration': 'records/A/judge-arrangement/preregistration-judge-arrangement-A.md', 'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(os.path.dirname(a.out), exist_ok=True)
open(a.out + '.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(OUT, ensure_ascii=False, indent=1) + '\n')
short = lambda d: json.dumps(d, ensure_ascii=False)[:600].replace('|', '／')
M = ['# 判定器の妥当性の運びの反映の確かめ（機械生成・`tools/verify_judge_arrangement_A.py` %s・%s UTC）' % (VERSION, now), '',
     '- 事前登録: `%s`（確かめの条件 K1〜K10 は器を書く前に記録した）' % OUT['preregistration'],
     '- 結果: %d/%d 合格・正本 SHA16 %s' % (OUT['n_pass'], OUT['n'], OUT['contrasts_sha16']),
     '- 器の SHA16: %s' % '・'.join('%s %s' % kv for kv in OUT['tools_sha16'].items()), '',
     '| id | 確かめ | 結果 | 詳細（先頭のみ・全体は JSON） |', '|---|---|---|---|']
M += ['| %s | %s | %s | %s |' % (r['id'], r['what'], '合格' if r['pass'] else '**不合格**', short(r['detail'])) for r in ROWS]
M += ['', '## 予想の照合（事前登録 §4 のうち機械で照合できるもの）', '',
      '- (a) ファイルの数: 予想 %s・結果 %s（%s）' % (EXTRA['prediction_a']['predicted_files'], EXTRA['prediction_a']['got_files'], '的中' if EXTRA['prediction_a']['hit'] else '外れ'),
      '- (b) 格子の数値の差: 予想 零・結果 %d（%s）' % (EXTRA['prediction_b']['got'], '的中' if EXTRA['prediction_b']['hit'] else '外れ'),
      '- (c) 設計事実の本文の差の行: 予想 A・O・結果 %s（%s）' % ('・'.join(EXTRA['prediction_c']['got']) or 'なし', '的中' if EXTRA['prediction_c']['hit'] else '外れ'), '',
      '- 限界: 合成のパイロットの応答の長さは門0.5 の 4B-2507 の分布の写しで、小さい機種の長さを再現しない。合成の判定者は機械の判定に誤りを乗せたもので、実際の判定者の書き出しの崩れや読み飛ばしを再現しない。実際の系統が添付ファイルを読み込めるかは確かめていない。', '',
      OUT['clause']]
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[verify_judge_arrangement_A] %d/%d 合格 → %s.{json,md}' % (OUT['n_pass'], OUT['n'], a.out))
sys.exit(0 if OUT['pass'] else 1)
