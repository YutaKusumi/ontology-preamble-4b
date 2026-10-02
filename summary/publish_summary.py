# -*- coding: utf-8 -*-
"""publish_summary.py v0（2026-10-02・中間総括の公開の束を組む・登録者裁定 D288-j と D290・コーディネータ南無弥勒如来）。
- 置く物: 総括の内部の置き場（`summary/`）の全ファイルから、受け取りの控え（`reviews/*/downloads-stash/`・票の `response.md` とバイトで同じ写し）を除いた物。
  公開の置き場の `summary/` に、同じ相対の道で置く（最終版の本文が指す `summary/...` の道がそのまま通る）。
- --check（写さない）: (1) 控えが票とバイトで同じこと（除いても失う物が無いこと）。(2) 冷徹一行の逐語がある記録の一覧が、最終版の照らしの記録の一覧と同じこと（逐語は V′ の最終版から器で読む・字は出さない）。
  (3) 手元の一時の置き場の道と会話の記録の置き場の名が無いこと。(4) 最終版の本文が `` で指す道が、`summary/...` なら置く物にあり、ほかは公開の置き場の git にあること。
  (5) 鍵と認証の字が無いこと（B′ の器 `records/Bprime/tools/check_secrets_Bprime.py` v0.1 を変えずに走らせ、記録 `secret-check-summary-2026-10-02.json` を一度だけ書かせる）。
  (6) 改行が LF だけであること（公開の置き場の .gitattributes は eol=lf で、CR があると記録の SHA-256 と git の中身がずれる）。(7) 公開の置き場に `summary/` がまだ無いこと。
  通れば、目録 `publish-summary-2026-10-02.json`（置く物の道・バイト・SHA-256・除いた物と理由・確かめの結果）を一度だけ書く。
- --copy（登録者の許しの後だけ）: 目録のとおりに、置く物と目録と鍵の確かめの記録を公開の置き場の `summary/` に写し、写した物の SHA-256 を目録と照らす。git の操作はしない。
用法: python publish_summary.py --check [--dry] | --copy（--dry は確かめだけを走らせ、目録と鍵の確かめの記録を書かない）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, shutil, hashlib, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
VERSION = 'v0'
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
DEST = os.path.join(PUB, 'summary')
MAN = os.path.join(HERE, 'publish-summary-2026-10-02.json')
SEC = os.path.join(HERE, 'secret-check-summary-2026-10-02.json')
SECTOOL = os.path.join(PUB, 'records', 'Bprime', 'tools', 'check_secrets_Bprime.py')
FINAL = os.path.join(HERE, 'summary-interim-FINAL-2026-10-02.md')
FCHK = os.path.join(HERE, 'summary-interim-FINAL-2026-10-02-checks.json')
JST = datetime.timezone(datetime.timedelta(hours=9))
NL = chr(10)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()
rel = lambda p: os.path.relpath(p, HERE).replace(os.sep, '/')
# (3) の形（この器の字そのものが当たらないよう、つないで作る）
LOCAL_PATS = ['App' + 'Data', 'scratch' + 'pad', '.claude/' + 'projects', '.claude\\' + 'projects', 'C--Users' + '-PC', 'Temp/' + 'claude', 'Temp\\' + 'claude', 'OP4B_DRY_DIR' + '=']
DRY = '--dry' in sys.argv
sys.dont_write_bytecode = True


def listing():
    files, stash = [], []
    for dp, dn, fn in os.walk(HERE):
        dn.sort()
        for f in sorted(fn):
            p = os.path.join(dp, f)
            r = rel(p)
            if '/downloads-stash/' in '/' + r:
                stash.append(r)
                continue
            if os.path.abspath(p) in (os.path.abspath(MAN), os.path.abspath(SEC)):
                continue
            assert '__pycache__' not in r and not r.endswith('.pyc'), ('置き場に要らない物', r)
            files.append(r)
    return files, stash


def check():
    for p_ in (MAN, SEC):
        assert not os.path.exists(p_), ('一度だけ', p_)
    files, stash = listing()
    res = {}
    # (1) 控えと票
    pairs = []
    for s in stash:
        m = re.match(r'^reviews/(round1|round2|final)/downloads-stash/op4b-summary-(round1|round2|final)-(.+)\.md$', s)
        assert m and m.group(1) == m.group(2), ('控えの名が想定と違う', s)
        v = 'reviews/%s/votes/%s/response.md' % (m.group(1), m.group(3))
        assert v in files and open(os.path.join(HERE, s), 'rb').read() == open(os.path.join(HERE, v), 'rb').read(), ('控えが票と同じでない', s)
        pairs.append({'path': 'summary/' + s, 'same_as': 'summary/' + v})
    res['stash_equal_to_votes'] = len(pairs)
    # (2) 冷徹一行の逐語がある記録
    tv = open(os.path.join(PUB, 'records', 'vprime', 'results-report-Vprime-FINAL-2026-09-09.md'), encoding='utf-8').read()
    i = tv.index('冷徹一行「')
    cold = tv[i + len('冷徹一行「'):tv.index('」', i + len('冷徹一行「'))]
    cold_files = []
    for r in files:
        t = open(os.path.join(HERE, r), encoding='utf-8').read()
        if r.endswith('.json'):
            t = t + NL + json.dumps(json.load(open(os.path.join(HERE, r), encoding='utf-8')), ensure_ascii=False)
        if cold in t:
            cold_files.append('summary/' + r)
    fchk = json.load(open(FCHK, encoding='utf-8'))
    assert sorted(cold_files) == sorted(fchk['cold_line_files']), ('冷徹一行の逐語がある記録の一覧が最終版の断りと違う', cold_files)
    res['cold_line_files'] = len(cold_files)
    # (3) 手元の道
    local_hits = [(r, p_) for r in files for p_ in LOCAL_PATS if p_ in open(os.path.join(HERE, r), encoding='utf-8').read()]
    assert not local_hits, ('手元の道の字がある', local_hits)
    res['local_path_hits'] = 0
    # (4) 最終版が指す道
    ft = open(FINAL, encoding='utf-8').read()
    toks = sorted(set(re.findall(r'`([A-Za-z0-9_.\-/]+)`', ft)))
    paths = [t for t in toks if '/' in t]
    tracked = set(subprocess.run(['git', '-C', PUB, 'ls-files'], capture_output=True, text=True, encoding='utf-8').stdout.split(NL))
    miss = []
    for t in paths:
        if t.startswith('summary/'):
            r = t[len('summary/'):]
            ok = (r in files) or (t.endswith('/') and any(f.startswith(r) for f in files))
        else:
            ok = (t in tracked) or (t.endswith('/') and any(f.startswith(t) for f in tracked))
        if not ok:
            miss.append(t)
    assert not miss, ('最終版が指す道が無い', miss)
    res['final_paths_checked'] = len(paths)
    res['final_paths_summary'] = sum(1 for t in paths if t.startswith('summary/'))
    # (6) 改行
    cr = [r for r in files if b'\r' in open(os.path.join(HERE, r), 'rb').read()]
    assert not cr, ('CR がある', cr)
    res['cr_files'] = 0
    # (7) 公開の置き場
    assert not os.path.exists(DEST), ('公開の置き場に summary/ が既にある', DEST)
    # (5) 鍵と認証の字（B′ の器を変えずに走らせる・値と当たった字は表示も記録もしない・--dry は記録を書かせない）
    pr = subprocess.run([sys.executable, SECTOOL] + ([] if DRY else ['--record', SEC, '--base', BASE]) + [os.path.join(HERE, r) for r in files], capture_output=True, text=True, encoding='utf-8')
    print(pr.stdout.strip())
    if DRY:
        assert pr.returncode == 0, ('鍵の確かめが通らない', pr.returncode, pr.stderr[-400:])
        print('--dry: 確かめは通った（目録と鍵の確かめの記録は書いていない）| 置く物 %d（%d バイト）・除いた控え %d・冷徹一行の逐語がある記録 %d・最終版が指す道 %d（うち summary/ %d）' % (
            len(files), sum(os.path.getsize(os.path.join(HERE, r)) for r in files), len(pairs), res['cold_line_files'], res['final_paths_checked'], res['final_paths_summary']))
        return
    assert pr.returncode == 0 and os.path.exists(SEC), ('鍵の確かめが通らない', pr.returncode, pr.stderr[-400:])
    sec = json.load(open(SEC, encoding='utf-8'))
    assert sec['files_with_hits'] == 0 and len(sec['files']) == len(files)
    res['secret_check'] = {'files': len(sec['files']), 'files_with_hits': sec['files_with_hits'], 'tool': sec['tool']}
    rows = [{'path': 'summary/' + r, 'bytes': os.path.getsize(os.path.join(HERE, r)), 'sha256': sha(os.path.join(HERE, r))} for r in files]
    man = {'kind': 'publish_manifest_interim_summary', 'tool': 'summary/publish_summary.py %s' % VERSION,
           'time_jst': datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'),
           'rulings': ['D288-j', 'D290'], 'dest': 'summary/',
           'final': {'path': 'summary/summary-interim-FINAL-2026-10-02.md', 'sha256': sha(FINAL)},
           'files': rows, 'n_files': len(rows), 'total_bytes': sum(r_['bytes'] for r_ in rows),
           'also_copied': [{'path': 'summary/' + rel(SEC), 'sha256': sha(SEC), 'note': '鍵と認証の字の確かめの記録（B′ の器が書いた）'},
                           {'path': 'summary/' + rel(MAN), 'note': 'この目録（自分の SHA-256 は書けない）'}],
           'excluded': [dict(p_, reason='受け取りの控え（票の response.md とバイトで同じ写し・この器が照らした）') for p_ in pairs],
           'checks': res, 'clause': CLAUSE}
    b = json.dumps(man, ensure_ascii=False, indent=1).encode('utf-8')
    sys.path.insert(0, os.path.dirname(SECTOOL))
    import check_secrets_Bprime as CS
    hv, hp = CS.check_bytes(b, CS.values())
    assert hv == 0 and not hp, '目録に鍵や認証の形の字がある'
    with open(MAN, 'wb') as fh:
        fh.write(b)
    print('目録を書いた: %s | 置く物 %d（%d バイト）・除いた控え %d・冷徹一行の逐語がある記録 %d・最終版が指す道 %d（うち summary/ %d）・鍵の確かめ %d 本で当たり 0' % (
        rel(MAN), len(rows), man['total_bytes'], len(pairs), res['cold_line_files'], res['final_paths_checked'], res['final_paths_summary'], res['secret_check']['files']))


def copy():
    man = json.load(open(MAN, encoding='utf-8'))
    assert not os.path.exists(DEST), ('公開の置き場に summary/ が既にある', DEST)
    for row in man['files']:
        src = os.path.join(BASE, *row['path'].split('/'))
        assert sha(src) == row['sha256'], ('置く物が目録の後に変わった', row['path'])
    todo = [r_['path'] for r_ in man['files']] + ['summary/' + rel(SEC), 'summary/' + rel(MAN)]
    for t in todo:
        src = os.path.join(BASE, *t.split('/'))
        dst = os.path.join(PUB, *t.split('/'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        assert sha(src) == sha(dst), ('写しが元と違う', t)
    print('写した: %d（置く物 %d・鍵の確かめの記録・目録）' % (len(todo), len(man['files'])))


if __name__ == '__main__':
    if '--check' in sys.argv:
        check()
    elif '--copy' in sys.argv:
        copy()
    else:
        raise SystemExit('用法: python publish_summary.py --check | --copy')
