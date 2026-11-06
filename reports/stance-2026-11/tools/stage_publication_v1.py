# -*- coding: utf-8 -*-
# stage_publication_v1.py : 版 1.1 の公開の写し。既に公開した reports/stance-2026-11/ に、作業の置き場の新しいファイルを一字も変えずに足す
#   - v0 は行き先が在れば止まる（最初の公開の用）。v1 は行き先が在ることを求め、次の決まりで足す。
#   - 作業の置き場の README.md（地図）は MAP.md の名で、報告（public-draft/stance-brief-ja-v1-1.md）は README.md の名で置く。
#   - 替えてよいのは MAP.md・README.md・SHA256SUMS の三つだけ。ほかに、公開済みのファイルと字の違うものがあれば、何も書かずに止まる。
#   - 公開の側にだけ在るファイルは .gitattributes と SHA256SUMS のほかには認めない。あれば、何も書かずに止まる。
#   - 書く前に、公開の側の全部のファイルを今の SHA256SUMS と照らす。
#   - 書いた後に、全部のファイルの SHA-256 を元と照らし、SHA256SUMS を作り直す。
# 使い方: python -I stage_publication_v1.py <work_dir> <repo_dir> [--dry]
import sys, os, hashlib
sys.stdout.reconfigure(encoding='utf-8')
W, R = sys.argv[1], sys.argv[2]
DRY = '--dry' in sys.argv[3:]
DST = os.path.join(R, 'reports', 'stance-2026-11')
NL = chr(10)
REPLACEABLE = {'MAP.md', 'README.md'}
PUBLIC_ONLY = {'.gitattributes', 'SHA256SUMS'}
if not os.path.isdir(DST):
    print('STOP missing', DST); raise SystemExit(1)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


# ---- 今の公開の側を、今の SHA256SUMS と照らす ----
sums_old = {}
for line in open(os.path.join(DST, 'SHA256SUMS'), encoding='utf-8'):
    line = line.rstrip(NL)
    if line:
        h, rel = line.split('  ', 1)
        sums_old[rel] = h
present = set()
for dp, dns, fns in os.walk(DST):
    rd = os.path.relpath(dp, DST).replace(chr(92), '/')
    for fn in fns:
        present.add(fn if rd == '.' else rd + '/' + fn)
bad_now = [r for r, h in sums_old.items() if r not in present or sha(os.path.join(DST, *r.split('/'))) != h]
if bad_now:
    print('STOP published differs from SHA256SUMS', bad_now[:5]); raise SystemExit(1)

# ---- 写す計画 ----
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
report_src = os.path.join(W, 'public-draft', 'stance-brief-ja-v1-1.md')
assert os.path.exists(report_src), 'report v1.1 missing'
plan.append((report_src, 'README.md'))
rels = [r for _, r in plan]
assert len(rels) == len(set(rels)), 'duplicate destination'

add, replace, same, refuse = [], [], [], []
for src, rel in plan:
    dst = os.path.join(DST, *rel.split('/'))
    if not os.path.exists(dst):
        add.append((src, rel))
    elif sha(src) == sha(dst):
        same.append(rel)
    elif rel in REPLACEABLE:
        replace.append((src, rel))
    else:
        refuse.append(rel)
extra = sorted(present - set(rels) - PUBLIC_ONLY)
if refuse or extra:
    print('STOP changed published files', refuse[:10], 'public only', extra[:10]); raise SystemExit(1)
print('same', len(same), 'add', len(add), 'replace', [r for _, r in replace])
print('add bytes', sum(os.path.getsize(s) for s, _ in add))
if DRY:
    for _, r in add:
        print('  add', r)
    print('dry run: nothing written')
    raise SystemExit(0)

# ---- 書く ----
for src, rel in add:
    dst = os.path.join(DST, *rel.split('/'))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, 'rb') as f:
        b = f.read()
    with open(dst, 'xb') as g:
        g.write(b)
for src, rel in replace:
    dst = os.path.join(DST, *rel.split('/'))
    with open(src, 'rb') as f:
        b = f.read()
    with open(dst, 'wb') as g:
        g.write(b)
lines = []
bad = []
for src, rel in plan:
    dst = os.path.join(DST, *rel.split('/'))
    a, b = sha(src), sha(dst)
    if a != b:
        bad.append(rel)
    lines.append('%s  %s' % (b, rel))
with open(os.path.join(DST, 'SHA256SUMS'), 'w', encoding='utf-8', newline=NL) as f:
    f.write(NL.join(sorted(lines, key=lambda s: s.split('  ', 1)[1])) + NL)
print('files', len(plan), 'mismatch', len(bad), bad[:5])
print('README.md SHA-256', sha(os.path.join(DST, 'README.md')))
print('SHA256SUMS SHA-256', sha(os.path.join(DST, 'SHA256SUMS')))
raise SystemExit(1 if bad else 0)
