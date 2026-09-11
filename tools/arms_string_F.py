# -*- coding: utf-8 -*-
"""arms_string_F.py —— 段階 F の走行器 run_preamble_api_f.py に渡す `--arms` の引数文字列を `design/contrasts-F.json` から機械生成する（手打ち禁止）。
9 腕（U-N＝N・T-N・T2-N・Ncold・T-Ncold・T2-Ncold・O-Ncold・T-O-Ncold・T2-O-Ncold）。SHA16 つきで印字。走行前の `--check X` は文字列一致を検査（不一致は非零終了）。
12 走行（パイロット 4・第一 4・第二 4）で共有。system 型は置かない（--system-arms は v2.6 のガードで停止）。
"""
import os, sys, json, hashlib, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-F.json')); ap.add_argument('--check', default=None); args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8'))
LV = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8')); LF = json.load(open(os.path.join(REPO, 'arms', 'panelF', 'SHA-LEDGER-F.json'), encoding='utf-8'))
pre = T['arms']['preamble']; missing = [a for a in pre if a != 'N' and a not in LV and a not in LF['preamble']]
if missing:
    sys.exit('[arms_string_F] 台帳に無い腕: %s' % missing)
s = ','.join(pre); h = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
if args.check is not None:
    ok = args.check == s; print('[arms_string_F] check', 'MATCH' if ok else 'MISMATCH'); sys.exit(0 if ok else 2)
print('--arms %s' % s); print('[arms_string_F] arms %d chars %d sha16 %s' % (len(pre), len(s), h))
