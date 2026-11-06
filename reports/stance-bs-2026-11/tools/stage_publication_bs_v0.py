# -*- coding: utf-8 -*-
# stage_publication_bs_v0.py : 作業の置き場を、論文の公開の置き場の reports/stance-bs-2026-11/ へ一字も変えずに写す（第一の登録の stage_publication_v0.py の型）
#   - 作業の置き場の README.md（地図）は MAP.md の名で、報告（public-draft/stance-bs-brief-ja-v1.md）は README.md の名で置く。
#   - .gitattributes（* -text）で、git の改行の書き替えを止める（記録の SHA-256 を保つため）。
#   - SHA256SUMS に、写したすべてのファイルの SHA-256 を書く。
#   - 行き先のフォルダが既にあれば止まる。写した後に、全部のファイルの SHA-256 を元と照らす。
#   - --dry を付けると、写す一覧と大きさだけを出して何も書かない。
# 使い方: python -I stage_publication_bs_v0.py <work_dir> <repo_dir> [--dry]
import sys, os, hashlib
sys.stdout.reconfigure(encoding='utf-8')
W, R = sys.argv[1], sys.argv[2]
DRY = '--dry' in sys.argv[3:]
DST = os.path.join(R, 'reports', 'stance-bs-2026-11')
NL = chr(10)
if os.path.exists(DST):
    print('STOP exists', DST); raise SystemExit(1)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


plan = []   # (src, rel_dst)
for dp, dns, fns in os.walk(W):
    dns[:] = sorted(d for d in dns if d not in ('__pycache__',))
    rel_dir = os.path.relpath(dp, W).replace(chr(92), '/')
    assert 'sealed' not in rel_dir.split('/')
    for fn in sorted(fns):
        src = os.path.join(dp, fn)
        rel = fn if rel_dir == '.' else rel_dir + '/' + fn
        if rel == 'README.md':
            rel = 'MAP.md'
        plan.append((src, rel))
report_src = os.path.join(W, 'public-draft', 'stance-bs-brief-ja-v1.md')
assert os.path.exists(report_src), 'report v1 missing'
plan.append((report_src, 'README.md'))
rels = [r for _, r in plan]
assert len(rels) == len(set(rels)), 'duplicate destination'
total = sum(os.path.getsize(s) for s, _ in plan)
print('files', len(plan), 'bytes', total)
if DRY:
    big = sorted(plan, key=lambda x: -os.path.getsize(x[0]))[:12]
    for s, r_ in big:
        print('  ', os.path.getsize(s), r_)
    print('dry run: nothing written')
    raise SystemExit(0)

os.makedirs(DST)
for src, rel in plan:
    dst = os.path.join(DST, *rel.split('/'))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, 'rb') as f:
        b = f.read()
    with open(dst, 'xb') as g:
        g.write(b)
with open(os.path.join(DST, '.gitattributes'), 'x', encoding='utf-8', newline=NL) as f:
    f.write('# このフォルダのファイルは、作業の置き場と一字も違わないように、git の改行の書き替えを止める（記録の SHA-256 を保つ）' + NL + '* -text' + NL)
lines = []
bad = []
for src, rel in plan:
    dst = os.path.join(DST, *rel.split('/'))
    a, b = sha(src), sha(dst)
    if a != b:
        bad.append(rel)
    lines.append('%s  %s' % (b, rel))
with open(os.path.join(DST, 'SHA256SUMS'), 'x', encoding='utf-8', newline=NL) as f:
    f.write(NL.join(sorted(lines, key=lambda s: s.split('  ', 1)[1])) + NL)
print('files', len(plan), 'mismatch', len(bad), bad[:5])
print('README.md SHA-256', sha(os.path.join(DST, 'README.md')))
print('SHA256SUMS SHA-256', sha(os.path.join(DST, 'SHA256SUMS')))
raise SystemExit(1 if bad else 0)
