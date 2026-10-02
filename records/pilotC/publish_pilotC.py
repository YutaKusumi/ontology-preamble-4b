# -*- coding: utf-8 -*-
"""publish_pilotC.py v0（2026-10-02・段階 C の下見を「登録外の下見」として公開する束を組む・登録者の言葉「公開をしてください」2026-10-02・コーディネータ南無弥勒如来）。
- 置く物: (1) 内部の置き場 `pilotC/` の全ファイル → 公開の置き場の `records/pilotC/`、(2) 走行器の出力 `results/pilotC/`（公開の置き場にすでにある）、
  (3) 試し走りの発火の記録 `records/dryrun/firing-pilotC__*.json`（公開の置き場にすでにある）。
- --check（写さない）: 手元の一時の置き場の道が無いこと・改行が LF だけであること・地の文の md の禁止の語（柵の条項を除く）・
  B′ の鍵の確かめの器（`records/Bprime/tools/check_secrets_Bprime.py` v0.1・変えずに走らせる）で鍵と認証の字が無いこと（--record で記録を一度だけ書かせる）、を確かめ、目録を一度だけ書く。--dry は書かない。
- --copy: (1) を `records/pilotC/` に写して SHA-256 を照らす（git の操作はしない）。
用法: python publish_pilotC.py --check [--dry] | --copy
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, glob, shutil, hashlib, subprocess, datetime
sys.dont_write_bytecode = True
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
DEST = os.path.join(PUB, 'records', 'pilotC')
MAN = os.path.join(HERE, 'publish-pilotC-2026-10-02.json')
SEC = os.path.join(HERE, 'secret-check-pilotC-2026-10-02.json')
SECTOOL = os.path.join(PUB, 'records', 'Bprime', 'tools', 'check_secrets_Bprime.py')
DRY = '--dry' in sys.argv
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
LOCAL = ['App' + 'Data', 'scratch' + 'pad', '.claude/' + 'projects', '.claude\\' + 'projects', 'C--Users' + '-PC', 'Temp/' + 'claude', 'Temp\\' + 'claude']
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


def sha_git(p):
    """git に入る中身の SHA-256（公開の置き場の .gitattributes: 既定は text=auto eol=lf・*.jsonl は -text）。
    走行器は Windows で書くので、json と txt の改行は CRLF で、git が LF にそろえて入れる。jsonl はそのまま入る。"""
    b = open(p, 'rb').read()
    if not (p.endswith('.jsonl') or p.endswith('.gz')):
        b = b.replace(b'\r\n', b'\n')
    return hashlib.sha256(b).hexdigest().upper()


def internal_files():
    out = []
    for f in sorted(os.listdir(HERE)):
        p = os.path.join(HERE, f)
        if os.path.isfile(p) and os.path.abspath(p) not in (os.path.abspath(MAN), os.path.abspath(SEC)):
            out.append(f)
    return out


def public_files():
    res = sorted(glob.glob(os.path.join(PUB, 'results', 'pilotC', '**', '*'), recursive=True))
    res = [p for p in res if os.path.isfile(p)]
    fire = sorted(glob.glob(os.path.join(PUB, 'records', 'dryrun', 'firing-pilotC__*.json')))
    assert len(fire) == 5 and len(res) == 20, ('公開の置き場の下見の出力の数が想定と違う', len(res), len(fire))
    return [os.path.relpath(p, PUB).replace(os.sep, '/') for p in res + fire]


def check():
    if not DRY:
        for p_ in (MAN, SEC):
            assert not os.path.exists(p_), ('一度だけ', p_)
    assert not os.path.exists(DEST), ('公開の置き場に records/pilotC/ が既にある', DEST)
    ins, pubs = internal_files(), public_files()
    paths = [os.path.join(HERE, f) for f in ins] + [os.path.join(PUB, *r.split('/')) for r in pubs]
    loc = [(p, x) for p in paths for x in LOCAL if x in open(p, encoding='utf-8', errors='replace').read()]
    assert not loc, ('手元の道の字がある', loc)
    cr = [p for p in paths if b'\r\n' in open(p, 'rb').read()]
    bare_cr = [p for p in paths if b'\r' in open(p, 'rb').read().replace(b'\r\n', b'')]
    assert not bare_cr, ('CRLF でない CR がある', bare_cr)
    print('CRLF の改行のファイル %d（走行器と画面の記録が Windows で書いた物・git が jsonl のほかを LF にそろえて入れる・目録の SHA-256 は git に入る中身で数える）' % len(cr))
    sys.path.insert(0, os.path.join(PUB, 'tools'))
    import build_report_Bprime as BR
    CB = json.load(open(os.path.join(PUB, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    EXTRA = ['証明', '効いた', '耐えた', '頑健', '守った', '防いだ', '特定した', '一般化', '機種の違いで', '働いた', '多いものと少ないもの']
    BANS = sorted(set(BR.bans_of(CB)) | set(EXTRA))
    ban_hits = {}
    for f in ins:
        if f.endswith('.md'):
            t = open(os.path.join(HERE, f), encoding='utf-8').read().replace(CLAUSE, '')
            h = sorted({w for w in BANS if w in t})
            if h:
                ban_hits[f] = h
    print('禁止の語（柵の条項を除く）の当たり:', ban_hits or 'なし')
    pr = subprocess.run([sys.executable, SECTOOL] + ([] if DRY else ['--record', SEC, '--base', os.path.dirname(HERE)]) + paths, capture_output=True, text=True, encoding='utf-8')
    print(pr.stdout.strip())
    assert pr.returncode == 0, ('鍵の確かめが通らない', pr.stderr[-300:])
    if DRY:
        print('--dry: 確かめは通った（何も書いていない）| 内部 %d・公開の置き場の出力 %d' % (len(ins), len(pubs)))
        return
    rows = [{'path': 'records/pilotC/' + f, 'source': 'internal pilotC/' + f, 'bytes_worktree': os.path.getsize(os.path.join(HERE, f)), 'sha256_worktree': sha(os.path.join(HERE, f)),
             'sha256_git': sha_git(os.path.join(HERE, f)), 'crlf_in_worktree': b'\r\n' in open(os.path.join(HERE, f), 'rb').read()} for f in ins]
    rows += [{'path': r, 'source': 'public working tree', 'bytes_worktree': os.path.getsize(os.path.join(PUB, *r.split('/'))), 'sha256_worktree': sha(os.path.join(PUB, *r.split('/'))),
              'sha256_git': sha_git(os.path.join(PUB, *r.split('/'))), 'crlf_in_worktree': b'\r\n' in open(os.path.join(PUB, *r.split('/')), 'rb').read()} for r in pubs]
    man = {'kind': 'publish_manifest_pilotC', 'tool': 'records/pilotC/publish_pilotC.py v0', 'time_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
           'what': '段階 C の下見（登録外・記述だけ・札なし）', 'files': rows, 'n_files': len(rows), 'total_bytes_worktree': sum(r['bytes_worktree'] for r in rows),
           'sha_rule': 'sha256_git は git に入る中身（jsonl と gz のほかは CRLF を LF にそろえた物）の SHA-256。sha256_worktree は手元の作業の木の物。',
           'also_copied': ['records/pilotC/' + os.path.basename(SEC), 'records/pilotC/' + os.path.basename(MAN)],
           'ban_hits_in_md_excluding_clause': ban_hits, 'not_published': '内部の置き場の pilotC の外にある記録（登録者の私的な事柄を含む所）は置かない。',
           'clause': CLAUSE}
    json.dump(man, open(MAN, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print('目録を書いた | 置く物 %d（作業の木で %d バイト）' % (len(rows), man['total_bytes_worktree']))


def copy():
    man = json.load(open(MAN, encoding='utf-8'))
    assert not os.path.exists(DEST)
    os.makedirs(DEST)
    n = 0
    for r in man['files']:
        if r['source'].startswith('internal'):
            src = os.path.join(HERE, r['path'].split('/')[-1])
            assert sha(src) == r['sha256_worktree'], ('目録の後に変わった', src)
            shutil.copyfile(src, os.path.join(PUB, *r['path'].split('/')))
            assert sha(os.path.join(PUB, *r['path'].split('/'))) == r['sha256_worktree']
            n += 1
        else:
            assert sha(os.path.join(PUB, *r['path'].split('/'))) == r['sha256_worktree'], ('公開の置き場の出力が目録の後に変わった', r['path'])
    for p in (SEC, MAN):
        shutil.copyfile(p, os.path.join(DEST, os.path.basename(p)))
        assert sha(p) == sha(os.path.join(DEST, os.path.basename(p)))
        n += 1
    print('写した: %d（内部の記録・鍵の確かめの記録・目録）' % n)


if __name__ == '__main__':
    if '--check' in sys.argv:
        check()
    elif '--copy' in sys.argv:
        copy()
    else:
        raise SystemExit('用法: python publish_pilotC.py --check [--dry] | --copy')
