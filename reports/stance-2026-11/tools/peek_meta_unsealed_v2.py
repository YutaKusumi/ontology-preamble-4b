# -*- coding: utf-8 -*-
# peek_meta_unsealed_v2.py : 本番の zip の meta/ の小さな json と logs/ の driver の記録だけを読む
#   v1 の誤り：名の頭に「out-main-XX-v2/」が付くのに「sealed/」で照らしたので、封の名（と大きさ）を一覧に出した（中身は読んでいない）。
#   v2：名を「/」で分け、二つ目の段が sealed の名は一覧にも出さず、決して読まない。読むのは下の WANT に合う名だけ。
# 使い方: python -I peek_meta_unsealed_v2.py <zip> [<zip> ...]
import sys, zipfile, hashlib
sys.stdout.reconfigure(encoding='utf-8')
def part(n, i):
    s = n.split('/')
    return s[i] if len(s) > i else ''
for zp in sys.argv[1:]:
    b = open(zp, 'rb').read()
    print('=== ' + zp.split('/')[-1] + '  SHA-256 ' + hashlib.sha256(b).hexdigest().upper())
    z = zipfile.ZipFile(zp)
    names = z.namelist()
    n_sealed = sum(1 for n in names if part(n, 1) == 'sealed')
    print('members', len(names), 'sealed (not listed, not read)', n_sealed)
    for n in names:
        if part(n, 1) == 'sealed':
            continue
        sec, base = part(n, 1), n.split('/')[-1]
        want = (sec == 'meta' and (base.endswith('-started.json') or base.endswith('-done.json'))) or (sec == 'logs' and base.endswith('-driver.log'))
        if not want:
            continue
        assert part(n, 1) != 'sealed'
        print('--- ' + n)
        print(z.read(n).decode('utf-8')[:2000])
