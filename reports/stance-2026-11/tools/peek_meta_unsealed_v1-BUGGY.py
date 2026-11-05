# -*- coding: utf-8 -*-
# peek_meta_unsealed.py : 本番の zip の「封の外」の名と meta/*.json だけを読む（sealed/ で始まる名は開かない・読まない）
# 使い方: python -I peek_meta_unsealed.py <zip> [<zip> ...]
import sys, zipfile, hashlib, json
sys.stdout.reconfigure(encoding='utf-8')
for zp in sys.argv[1:]:
    b = open(zp, 'rb').read()
    print('=== ' + zp.split('/')[-1] + '  SHA-256 ' + hashlib.sha256(b).hexdigest().upper())
    z = zipfile.ZipFile(zp)
    names = z.namelist()
    sealed = [n for n in names if n.startswith('sealed/')]
    other = [n for n in names if not n.startswith('sealed/')]
    print('members', len(names), 'sealed', len(sealed), '(not opened)', 'unsealed', len(other))
    for n in other:
        print('  -', n, z.getinfo(n).file_size)
    for n in other:
        if n.startswith('meta/') and n.endswith('.json') and z.getinfo(n).file_size < 20000:
            assert not n.startswith('sealed/')
            t = z.read(n).decode('utf-8')
            print('--- ' + n)
            print(t[:3000])
