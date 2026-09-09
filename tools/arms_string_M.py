# -*- coding: utf-8 -*-
"""arms_string_M.py —— 追補 M の走行器 run_preamble_api_m.py に渡す引数文字列を `design/contrasts-M.json` から機械生成する（手打ち禁止・二巡目器材 I）。
前置き型走行: `--arms <52 腕の一行>`。system 型走行: `--arms - --system-arms <14 腕の spec>`（`-`＝前置き腕なし・v2.5 ハンク 9。既定値の 8 腕が黙って合流する事故を防ぐ）。
二種の文字列を SHA16 つきで印字する。走行前の `--check X` は文字列一致を検査（不一致は非零終了）。24 走行（パイロット 8・第一 8・第二 8）＋dry-run で共有。
用法: python tools/arms_string_M.py [--which preamble|system] [--check X]
"""
import os, sys, json, hashlib, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--contrasts', default=os.path.join(REPO, 'design', 'contrasts-M.json')); ap.add_argument('--which', choices=['preamble', 'system'], default='preamble'); ap.add_argument('--check', default=None)
args = ap.parse_args()
T = json.load(open(args.contrasts, encoding='utf-8'))
LV = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8')); LM = json.load(open(os.path.join(REPO, 'arms', 'panelM', 'SHA-LEDGER-M.json'), encoding='utf-8'))
if args.which == 'preamble':
    arms = T['arms']['preamble']; assert len(arms) == len(set(arms))
    missing = [a for a in arms if a != 'N' and a not in LV and a not in LM['preamble']]
    assert not missing, '台帳に無い腕: %s' % missing
    s = ','.join(arms)
else:
    s = T['arms']['system_spec']
    for d in T['arms']['system']:
        if d['system'] not in ('none', 'O', 'Onull'):
            assert os.path.splitext(d['system'])[0] in LM['system'], 'system 台帳に無い: %s' % d['system']
    assert s == ','.join('%s=%s:%s' % (d['name'], d['system'], d['prefix']) for d in T['arms']['system'])
sha = hashlib.sha256(s.encode('utf-8')).hexdigest()[:16].upper()
if args.check is not None:
    if args.check != s:
        sys.exit('[arms_M/%s] 不一致: 正本 SHA16 %s' % (args.which, sha))
    print('[arms_M/%s] 一致 (SHA16 %s)' % (args.which, sha)); sys.exit(0)
print(s); print('[arms_M/%s] %d 項・%d 字・SHA16 %s（contrasts %s）' % (args.which, s.count(',') + 1, len(s), sha, T['version']), file=sys.stderr)
