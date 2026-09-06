# -*- coding: utf-8 -*-
"""arms_string_vprime.py —— 走行器 run_preamble_api.py に渡す --arms の一行を `design/contrasts-Vprime.json` から機械生成する（手打ち禁止・三巡目検器身条件8／破器身 H2）。
用法: python tools/arms_string_vprime.py            → 一行を標準出力に印字し、SHA16 を標準エラーに出す
      python tools/arms_string_vprime.py --check X   → 文字列 X が正本と一致するか検査（不一致は非零終了）
"""
import os, sys, json, hashlib, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-Vprime.json')); ap.add_argument('--check', default=None)
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8'))
arms = T['arms']['singles'] + T['arms']['combos']
assert len(arms) == len(set(arms)), '腕名の重複'
ledger = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8'))
missing = [a for a in arms if a != 'N' and a not in ledger and a not in ('O', 'Onull')]
assert not missing, '台帳に無い腕: %s' % missing
s = ','.join(arms); sha = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
if args.check is not None:
    if args.check != s:
        sys.exit('[arms] 不一致: 正本 %d 腕 SHA16 %s' % (len(arms), sha))
    print('[arms] 一致 (%d 腕・SHA16 %s)' % (len(arms), sha)); sys.exit(0)
print(s); print('[arms] %d 腕・%d 字・SHA16 %s（contrasts %s）' % (len(arms), len(s), sha, T['version']), file=sys.stderr)
