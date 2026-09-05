# -*- coding: utf-8 -*-
"""監査回付用の束（bundle）を作る: 引数=出力パス・以降=ファイル一覧（相対）"""
import sys, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]; files = sys.argv[2:]
with open(os.path.join(REPO, out), 'w', encoding='utf-8', newline='\n') as w:
    w.write('# bundle: %s\n\n' % out)
    for f in files:
        p = os.path.join(REPO, f)
        if not os.path.isfile(p):
            w.write('\n===== MISSING: %s =====\n' % f); continue
        w.write('\n===== FILE: %s =====\n' % f)
        w.write(open(p, encoding='utf-8', errors='replace').read()); w.write('\n')
print('bundle written', out, len(files))
