# -*- coding: utf-8 -*-
"""verify_judge_arrangement2_A.py v1 —— 判定器の妥当性の運び 二回目の反映（試し読みの後の登録者裁定 D41〜D44）の確かめ（2026-09-15・コーディネータ）。
事前登録 records/A/judge-arrangement2/preregistration-judge-arrangement2-A.md の確かめの条件 L1〜L10 を機械で走らせ、records/A/judge-arrangement2/verification-judge-arrangement2-A.{json,md} に書く。
一時置き場（--work・リポジトリの外）に、門0.5 の応答の本文から作った実物大の合成のパイロット（7 機種 × 5 場面）と、合成の判定者四名（Gemini 二・Claude 二）の照合記号つきの返信を作り、
器（judge_fragments_A.py の extract・merge・score と build_report_A.py）を子プロセスで通す。器の内部を import して呼ばない。
仕込み: Gemini2 のファイル 2 の一回目の会話に照合外れ（閾値を超える割合）→ やり直しが要る状態で採点が止まる → やり直しを貼って ok。Claude2 のファイル 3 は二回とも閾値を超える → 読めなかった扱い。Claude1 は各ファイルの「後」の区分の誤りを多くする。
限界: 合成のパイロットの応答の長さは門0.5 の 4B-2507 の分布の写しで、小さい機種の長さを再現しない。合成の判定者は機械の判定に誤りを乗せたもので、実際の判定者の書き出しの崩れや読み飛ばしを再現しない。実際の判定者が照合記号を写すかは確かめない。
用法: python tools/verify_judge_arrangement2_A.py --work <一時置き場> --spec-old <v2.6 の正本の写し> --grid-old <現行の格子の写し> --facts-old <現行の設計事実の写し> --grid-new <v2.7 で走らせた格子> --analysis <合成の集計の記録>
柵: 本器の出力のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, json, glob, shutil, argparse, datetime, subprocess, importlib.util
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
ap = argparse.ArgumentParser()
ap.add_argument('--work', required=True); ap.add_argument('--spec-old', required=True); ap.add_argument('--grid-old', required=True); ap.add_argument('--facts-old', required=True)
ap.add_argument('--grid-new', required=True); ap.add_argument('--analysis', required=True); ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'judge-arrangement2', 'verification-judge-arrangement2-A'))
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


# ---- L1: 正本の差の範囲（v2.6 → v2.7）
OLD = runs_A.read_json(a.spec_old); LO = dict(leaves(OLD)); LN = dict(leaves(T))
changed = sorted(p for p in LO if p in LN and LO[p] != LN[p]); added = sorted(p for p in LN if p not in LO); removed = sorted(p for p in LO if p not in LN)
ALLOW_CHANGED = {'generator', 'judge_validity.attachment.merge', 'judge_validity.attachment.reply', 'judge_validity.attachment.request', 'judge_validity.groups', 'judge_validity.judges', 'procedure',
                 'tooling_interpretations.items', 'tooling_interpretations.status'}
ALLOW_ADDED = ('judge_validity.reading_check.', 'registrant_decisions_D41_D44.')
bad_c = [p for p in changed if p not in ALLOW_CHANGED]; bad_a = [p for p in added if not p.startswith(ALLOW_ADDED)]; bad_r = [p for p in removed if not p.startswith('judge_validity.composition.Grok.')]
R('L1', '正本 v2.7 と v2.6 の差が事前登録 §2 A の範囲だけ・整合検査の結果が同じ・procedure の項の数が同じ・composition に Grok が無い',
  not (bad_c or bad_a or bad_r) and OLD['integrity'] == T['integrity'] and len(OLD['procedure']) == len(T['procedure']) and 'Grok' not in JV['composition'] and sorted(JV['composition']) == ['Claude', 'Gemini'],
  {'changed': changed, 'added': added, 'removed': removed, 'outside': bad_c + bad_a + bad_r, 'composition': sorted(JV['composition'])})

# ---- L3: 実物大の模擬（門0.5 の応答の本文から作った合成のパイロット・照合記号つき）
spec = importlib.util.spec_from_file_location('app_parser_rev2_frozen', os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py'))
PM = importlib.util.module_from_spec(spec); spec.loader.exec_module(PM); parse, isc = PM.parse_app_v2, PM.is_catastrophic
SCN = {x['question_id']: x for x in json.load(open(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))['scenarios']}
GATE = []
for p in glob.glob(os.path.join(REPO, 'results', 'idA', 'idA__N1__none__seed60001', 'raw-*.jsonl')):
    for r in runs_A.iter_jsonl(p):
        GATE.append(r['raw_output_retry'] if r.get('raw_output_retry') is not None else (r.get('raw_output') or ''))
rng = np.random.default_rng([20260915, 11]); SIM = os.path.join(a.work, 'sim'); ROOT = os.path.join(SIM, 'results'); OUTD = os.path.join(SIM, 'out'); KEYD = os.path.join(SIM, 'key')
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
FR = runs_A.read_json(os.path.join(OUTD, 'judge-fragments-A.json')) if rc3 == 0 else {'fragments': []}; FCODE = {f['id']: f.get('code') for f in FR['fragments']}
cover = [('F%04d' % i) for f in FILES for i in range(int(f['first_id'][1:]), int(f['last_id'][1:]) + 1)]
sha_ok = all(runs_A.sha16_file(os.path.join(OUTD, 'judge-files', f['file'])) == f['sha16'] for f in FILES)
ALPH = (SE.get('reading_check') or {}).get('alphabet') or ''; CODE_RE = re.compile('^[%s]{%d}$' % (re.escape(ALPH), (SE.get('reading_check') or {}).get('code_len') or 0)) if ALPH else None
code_in_file = 0
for f in FILES:
    txt = open(os.path.join(OUTD, 'judge-files', f['file']), encoding='utf-8').read()
    code_in_file += sum(1 for i in range(int(f['first_id'][1:]), int(f['last_id'][1:]) + 1) if ('<<<断片 F%04d ここまで・照合記号 %s>>>' % (i, FCODE.get('F%04d' % i))) in txt)
n_expect = len(T['models']) * len(T['scenarios']) * JV['n_per_cell']
R('L3', '実物大の模擬: 断片 %d 件が上限以下のファイルに分かれ、各断片の終わりの行に断片の記録の照合記号がある・封印の記録の SHA16 と現物が一致・検査用の印なし' % n_expect,
  rc3 == 0 and SE.get('n') == n_expect and cover == ['F%04d' % i for i in range(1, n_expect + 1)] and all(f['est_tokens'] <= cap for f in FILES) and sha_ok and not SE.get('dev_marks')
  and bool(CODE_RE) and all(CODE_RE.match(c or '') for c in FCODE.values()) and code_in_file == n_expect,
  {'rc': rc3, 'n_files': len(FILES), 'est_tokens': [f['est_tokens'] for f in FILES], 'n_per_file': [f['n'] for f in FILES], 'bytes': [f['bytes'] for f in FILES], 'codes_in_files': code_in_file,
   'dev_marks': SE.get('dev_marks')})
EXTRA['prediction_c'] = {'predicted_files': 4, 'got_files': len(FILES), 'hit': len(FILES) == 4}

# ---- L4: 合成の判定者四名（Gemini 二・Claude 二）の照合記号つきの返信 → 取りまとめ → 採点（やり直しが要る状態・やり直しの後・読めなかったファイル）
KEYJ = runs_A.read_json(os.path.join(KEYD, 'judge-key-A.json')) if rc3 == 0 else {'key': []}; KM = {k['id']: k for k in KEYJ['key']}
slots = ['%s%d' % (s, i) for s, rule in JV['composition'].items() for i in range(1, rule['min'] + 1)]
rng2 = np.random.default_rng([20260915, 12]); OPTS = {'survival': ['a', 'b', 'c'], 'nuclear': ['a', 'b', 'c', 'd']}; CHUNK = 250; RDIR = os.path.join(OUTD, 'judge-replies')
BINS = JV['position']['bins']; NB = len(BINS); ERR, ERR_LATE, PLANT = 0.03, 0.30, 'Claude1'; REDO_J, REDO_K, UNR_J, UNR_K = 'Gemini2', 2, 'Claude2', 3
ids_of = lambda f: ['F%04d' % i for i in range(int(f['first_id'][1:]), int(f['last_id'][1:]) + 1)]


def line_for(fid, err, code_mode='ok'):
    k = KM[fid]; mc = k['machine']; fam = k['family']; fld = 'amount' if fam == 'survival' else 'escalation'
    cd = {'ok': ' code=%s' % FCODE[fid], 'bad': ' code=BBBB', 'none': ''}[code_mode]   # BBBB は照合記号の字の範囲の外
    if mc['format_fail']:
        return '%s undecidable%s' % (fid, cd)
    ch, val = mc['choice'], mc[fld]
    if ch != 'refuse' and rng2.random() < err:
        ch = str(rng2.choice([o for o in OPTS[fam] if o != ch])); val = (5 if ch == 'a' else 0) if fam == 'survival' else val
    if ch == 'refuse':
        return '%s choice=refuse%s' % (fid, cd)
    return '%s choice=%s' % (fid, ch) + ('' if val is None else ' %s=%d' % (fld, val)) + cd


def body_of(L, n):
    chunks = [L[j:j + CHUNK] for j in range(0, len(L), CHUNK)]
    return '\n\n'.join('\n'.join(c) + ('\n続く' if j < len(chunks) - 1 else '\n以上 %d 件' % n) for j, c in enumerate(chunks)) + '\n'


def append(s, k, text):
    with open(os.path.join(RDIR, '%s-%d.txt' % (s, k)), 'a', encoding='utf-8', newline='\n') as fh:
        fh.write(text)


for f in FILES:
    idsf = ids_of(f); n = len(idsf)
    for s in slots:
        err_of = lambda i: ERR_LATE if (s == PLANT and min(i * NB // n, NB - 1) == NB - 1) else ERR
        if s == REDO_J and f['k'] == REDO_K:   # 一回目の会話: 照合外れ 10%（閾値を超える）
            append(s, f['k'], body_of([line_for(x, err_of(i), 'bad' if i < int(n * 0.10) else 'ok') for i, x in enumerate(idsf)], n))
        elif s == UNR_J and f['k'] == UNR_K:   # 一回目: 照合外れ 50%・やり直し: 記号の無い行 20%（どちらも閾値を超える）
            append(s, f['k'], body_of([line_for(x, err_of(i), 'bad' if i % 2 == 0 else 'ok') for i, x in enumerate(idsf)], n) + '\n' + JV['attachment']['redo_line'] + '\n'
                   + body_of([line_for(x, err_of(i), 'none' if i % 5 == 0 else 'ok') for i, x in enumerate(idsf)], n))
        else:
            append(s, f['k'], body_of([line_for(x, err_of(i)) for i, x in enumerate(idsf)], n))
SEALP = os.path.join(OUTD, 'judge-key-seal-A.json'); LAB = os.path.join(OUTD, 'judge-labels'); LP = [os.path.join(LAB, '%s.json' % s) for s in slots]
SCORE = lambda out: run([tool('judge_fragments_A.py'), 'score', '--labels'] + LP + ['--key', os.path.join(KEYD, 'judge-key-A.json'), '--seal', SEALP, '--out', out])
rc_m1, o_m1 = run([tool('judge_fragments_A.py'), 'merge', '--seal', SEALP]); M1 = runs_A.read_json(os.path.join(LAB, 'merge-A.json')) if rc_m1 == 0 else {}
rc_s1, o_s1 = SCORE(os.path.join(SIM, 'jv-stop'))
stop_ok = (rc_m1 == 0 and (M1.get('reading_check') or {}).get('redo_required') == ['%s × %s-%d.txt' % (REDO_J, REDO_J, REDO_K)] and rc_s1 != 0 and 'やり直しが要る' in o_s1
           and not os.path.exists(os.path.join(SIM, 'jv-stop.json')))
fr_ = next((f for f in FILES if f['k'] == REDO_K), None)
if fr_:
    append(REDO_J, REDO_K, JV['attachment']['redo_line'] + '\n' + body_of([line_for(x, ERR) for x in ids_of(fr_)], fr_['n']))
rc_m2, o_m2 = run([tool('judge_fragments_A.py'), 'merge', '--seal', SEALP, '--force']); M2 = runs_A.read_json(os.path.join(LAB, 'merge-A.json')) if rc_m2 == 0 else {}
rc4s, o4s = SCORE(os.path.join(SIM, 'jv')); RJ = runs_A.read_json(os.path.join(SIM, 'jv.json')) if rc4s == 0 else {}
fu_ = next((f for f in FILES if f['k'] == UNR_K), {'n': -1})
RC2 = M2.get('reading_check') or {}; RCJ = RJ.get('reading_check') or {}
st_redo = [fs['status'] for fs in (M2.get('judges', {}).get(REDO_J) or {}).get('files', []) if fs['k'] == REDO_K]
grp = {g: len(((RJ.get('groups') or {}).get(g) or {}).get('pairs') or []) for g in ('系統外どうし', '系統内どうし', '系統外×系統内')}
same = sorted(tuple(d['judges']) for d in (RJ.get('inter_judge') or []) if d.get('same_system'))
POS = {s: {b: v['agree_choice'] for b, v in (((RJ.get('position') or {}).get(s) or {}).get('pooled') or {}).items()} for s in slots}
plant_ok = bool(POS.get(PLANT)) and POS[PLANT][BINS[-1]] <= min(POS[PLANT][BINS[0]], POS[PLANT][BINS[1]]) - 0.10
flat_ok = all(POS.get(s) and abs(POS[s][BINS[-1]] - POS[s][BINS[0]]) <= 0.05 for s in slots if s != PLANT)
unr_n = sum(v['excluded_judge'].get('unreadable', 0) for v in ((RJ.get('per_judge') or {}).get(UNR_J) or {}).values())
R('L4', '合成の判定者四名: 照合外れの仕込みでやり直しが要る状態になり採点が止まる・やり直しを貼ると ok で採点が通る・二回とも超えたファイルは読めなかった扱いで対から外れる・群の対の数 1・1・4 と同じ系統の印二対・位置の差は仕込んだ判定者の「後」にだけ',
  len(FILES) >= UNR_K and stop_ok and rc_m2 == 0 and st_redo == ['ok'] and not RC2.get('redo_required') and RC2.get('unreadable') == ['%s × %s-%d.txt' % (UNR_J, UNR_J, UNR_K)]
  and rc4s == 0 and RCJ.get('unreadable') == RC2.get('unreadable') and unr_n == fu_['n'] and all(v['code_fail'] == 0 for v in (RCJ.get('per_judge') or {}).values())
  and grp == {'系統外どうし': 1, '系統内どうし': 1, '系統外×系統内': 4} and same == [('Claude1', 'Claude2'), ('Gemini1', 'Gemini2')] and plant_ok and flat_ok
  and all(c['meets'] for c in (RJ.get('composition') or {'x': {'meets': False}}).values()),
  {'merge1_rc': rc_m1, 'redo_required_1': (M1.get('reading_check') or {}).get('redo_required'), 'score_stop_rc': rc_s1, 'score_stop_tail': o_s1[-200:], 'merge2_rc': rc_m2, 'status_redo_file': st_redo,
   'reading_check_2': {k: RC2.get(k) for k in ('redo_required', 'unreadable')}, 'score_rc': rc4s, 'unreadable_excluded': unr_n, 'file_n': fu_['n'], 'per_judge_code_fail': RCJ.get('per_judge'),
   'groups': grp, 'same_system_pairs': same, 'position_agree_choice': POS})

# ---- L5: 報告の組み立て器 v2.3
REP = os.path.join(SIM, 'report', 'report.md'); os.makedirs(os.path.dirname(REP), exist_ok=True)
rc5, o5 = run([tool('build_report_A.py'), '--draft', '1', '--analysis', a.analysis, '--judge', os.path.join(SIM, 'jv.json'), '--out', REP, '--force', '--allow-dev-marks'])
txt5 = open(REP, encoding='utf-8').read() if os.path.exists(REP) else ''; MBK = T['report_rules']['machine_block']
blocks = re.findall(re.escape(MBK['begin']) + r'\n(.*?)\n' + re.escape(MBK['end']), txt5, flags=re.S); inblock = lambda s: any(s in b for b in blocks)
need5 = ['| %s（系統外） |' % slots[0], '（系統内） |', '系統外どうし: ', '・同じ系統', '照合外れ（判定者ごと）: ', '読めなかった判定者 × ファイル: %s × %s-%d.txt' % (UNR_J, UNR_J, UNR_K), '判定者の構成（登録と実際）: ']
row6 = any(re.search(r'機械 \d+・\d+／判定者 \d+・\d+・\d+・\d+・\d+・\d+ \|', b) for b in blocks)
R('L5', '報告の組み立て器 v2.3 が、照合外れと読めなかったファイルの件数（判定者の除いた件数の六つの欄）・読み取りの確かめの行・同じ系統の印を機械の区画に置き、走査の違反が埋め残しのほかに無い',
  rc5 == 0 and all(inblock(s) for s in need5) and row6, {'rc': rc5, 'missing_in_blocks': [s for s in need5 if not inblock(s)], 'row6': row6, 'tail': o5[-300:]})


# ---- L6: 格子の数値の差（入力の SHA16・生成の時刻・所要時間・版を除く）
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
R('L6', '格子の再走（正本 v2.7）で、全節の値が現行の格子と一致し、入力の正本の SHA16 が現物と一致・quick でない',
  not gd and GN['inputs']['contrasts_sha16'] == runs_A.sha16_file(runs_A.CPATH) and not GN.get('quick') and GN.get('version') == GO.get('version'),
  {'diffs': len(gd), 'first': gd[:5], 'new_only': [k for k in GN if k not in GO], 'elapsed_s': GN.get('elapsed_s')})
EXTRA['prediction_b'] = {'predicted_diffs': 0, 'got': len(gd), 'hit': not gd}

# ---- L7: 設計事実の本文の差（転記行 J の SHA16 の文字列だけ）
FN = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); FO = runs_A.read_json(a.facts_old)
rows_changed = sorted(k for k in FO['facts'] if FN['facts'].get(k, {}).get('text') != FO['facts'][k]['text'])
SHA_MASK = lambda s: re.sub(r'\b[0-9A-F]{16}\b', '<SHA16>', s)
beyond = sorted(k for k in rows_changed if SHA_MASK(FN['facts'][k]['text']) != SHA_MASK(FO['facts'][k]['text']))
R('L7', '設計事実の本文の差が、転記行 J の SHA16 の文字列だけ', rows_changed == ['J'] and not beyond and not FN.get('dev_marks'), {'rows_changed': rows_changed, 'beyond_sha16': beyond, 'dev_marks': FN.get('dev_marks')})
EXTRA['prediction_a'] = {'predicted': 'L7 満たされる', 'got_rows': rows_changed, 'beyond_sha16': beyond, 'hit': rows_changed == ['J'] and not beyond}

# ---- L8: 草案9 と雛形の数の検査
lint_d = open(os.path.join(REPO, 'records', 'A', 'numbers-lint-draft9A.md'), encoding='utf-8').read(); lint_t = open(os.path.join(REPO, 'records', 'A', 'numbers-lint-template-A.md'), encoding='utf-8').read()
R('L8', '草案9 と雛形の数の検査の違反が零', '違反の合計: 0' in lint_d and '違反の合計: 0' in lint_t, {'draft': re.findall(r'違反の合計: \d+', lint_d), 'template': re.findall(r'違反の合計: \d+', lint_t)})

# ---- L9: 運用の解釈の記録
TIW = os.path.join(a.work, 'ti.md'); rc9, o9 = run([tool('tooling_interpretations_A.py'), '--out', TIW]); TIrec = open(os.path.join(REPO, 'records', 'A', 'tooling-interpretations-A.md'), encoding='utf-8').read()
TIgen = open(TIW, encoding='utf-8').read() if rc9 == 0 else ''
R('L9', '運用の解釈の記録が 37 項で、組み立て直すと記録と一致する', rc9 == 0 and TIgen == TIrec and TIrec.count('\n- 向き: ') == len(T['tooling_interpretations']['items']) == 37,
  {'rebuild_equal': TIgen == TIrec, 'direction_lines': TIrec.count('\n- 向き: '), 'items': len(T['tooling_interpretations']['items'])})

# ---- L2・L10: 自己検査
src_f = open(tool('freeze_A.py'), encoding='utf-8').read(); SELF = next(ast.literal_eval(n.value) for n in ast.walk(ast.parse(src_f)) if isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == 'SELFTESTS' for t in n.targets))
ST = []
if not a.skip_selftests:
    for nm, args in SELF:
        rc_, o_ = run([tool(nm)] + args); ST.append({'tool': nm, 'rc': rc_, 'tail': o_.strip()[-300:], 'out': o_})
jf = next((x for x in ST if x['tool'] == 'judge_fragments_A.py'), None)
need2 = ['SELFTEST PASS', '4e v2.3', '6a v2.3', '6g v2.3', '6c v2.2', '6d v2.2', '6e・6f v2.2']
R('L2', '判定器の器 v2.3 の自己検査が通り、追補の検査（照合記号の生成と置き場・小文字と全角・記号の無い行・やり直しが要る状態で採点が止まる・やり直しの後の ok・読めなかった扱い・Grok の名で止まる・同じ系統の印）を含む',
  bool(jf) and jf['rc'] == 0 and all(s in jf['out'] for s in need2), {'rc': jf and jf['rc'], 'missing': [s for s in need2 if not jf or s not in jf['out']]})
R('L10', '凍結器の自己検査（SELFTESTS）がすべて通る', bool(ST) and all(x['rc'] == 0 for x in ST), [{'tool': x['tool'], 'rc': x['rc'], 'tail': x['tail'][-120:]} for x in ST])

# ---- 記録
ORDER = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10']; ROWS.sort(key=lambda r: ORDER.index(r['id']))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
TOOLS = ['make_contrasts_A.py', 'judge_fragments_A.py', 'build_report_A.py', 'tooling_interpretations_A.py', 'verify_judge_arrangement2_A.py']
OUT = {'kind': 'verification_judge_arrangement2_A', 'version': VERSION, 'generated_utc': now, 'pass': all(r['pass'] for r in ROWS), 'n_pass': sum(r['pass'] for r in ROWS), 'n': len(ROWS),
       'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'tools_sha16': {t: runs_A.sha16_file(tool(t)) for t in TOOLS}, 'rows': ROWS, 'extra': EXTRA,
       'preregistration': 'records/A/judge-arrangement2/preregistration-judge-arrangement2-A.md', 'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(os.path.dirname(a.out), exist_ok=True)
open(a.out + '.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(OUT, ensure_ascii=False, indent=1) + '\n')
short = lambda d: json.dumps(d, ensure_ascii=False)[:600].replace('|', '／')
M = ['# 判定器の妥当性の運び 二回目の反映の確かめ（機械生成・`tools/verify_judge_arrangement2_A.py` %s・%s UTC）' % (VERSION, now), '',
     '- 事前登録: `%s`（確かめの条件 L1〜L10 は器を書く前に記録した）' % OUT['preregistration'],
     '- 結果: %d/%d 合格・正本 SHA16 %s' % (OUT['n_pass'], OUT['n'], OUT['contrasts_sha16']),
     '- 器の SHA16: %s' % '・'.join('%s %s' % kv for kv in OUT['tools_sha16'].items()), '',
     '| id | 確かめ | 結果 | 詳細（先頭のみ・全体は JSON） |', '|---|---|---|---|']
M += ['| %s | %s | %s | %s |' % (r['id'], r['what'], '合格' if r['pass'] else '**不合格**', short(r['detail'])) for r in ROWS]
M += ['', '## 予想の照合（事前登録 §4 のうち機械で照合できるもの）', '',
      '- (a) L7 は満たされる: 結果 %s（差の行 %s・SHA16 の外の差 %s）' % ('的中' if EXTRA['prediction_a']['hit'] else '外れ', '・'.join(EXTRA['prediction_a']['got_rows']) or 'なし', '・'.join(EXTRA['prediction_a']['beyond_sha16']) or 'なし'),
      '- (b) 格子の値の差は零: 結果 %d（%s）' % (EXTRA['prediction_b']['got'], '的中' if EXTRA['prediction_b']['hit'] else '外れ'),
      '- (c) 実物大の模擬は 4 ファイル: 結果 %d（%s）' % (EXTRA['prediction_c']['got_files'], '的中' if EXTRA['prediction_c']['hit'] else '外れ'), '',
      '- 限界: 合成のパイロットの応答の長さは門0.5 の 4B-2507 の分布の写しで、小さい機種の長さを再現しない。合成の判定者は機械の判定に誤りを乗せたもので、実際の判定者の書き出しの崩れや読み飛ばしを再現しない。実際の判定者が照合記号を写すかは確かめていない（二回目の試し読みで見る）。', '',
      OUT['clause']]
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[verify_judge_arrangement2_A] %d/%d 合格 → %s.{json,md}' % (OUT['n_pass'], OUT['n'], a.out))
sys.exit(0 if OUT['pass'] else 1)
