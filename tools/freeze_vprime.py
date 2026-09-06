# -*- coding: utf-8 -*-
"""freeze_vprime.py —— 追補 V′ の凍結マニフェストを発行する（登録者の凍結指示があってから実行する）。
凍結範囲: 本文（凍結版）・正本 JSON・盤 54 ファイル＋台帳・器材 7 本・格子 md/json・設計事実 md/json・予想様式。
出力: records/freeze-Vprime-<date>.json（同名があれば連番・上書きなし）。--verify <manifest> で現物と突合（不一致は非零終了）。
SHA16 はファイルバイトの SHA-256 先頭 16 桁（CRLF→LF 正規化・strip なし・台帳と同一規約）。
"""
import os, sys, json, glob, hashlib, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--design', default='design/design-stageVprime-FROZEN.md'); ap.add_argument('--verify', default=None)
args = ap.parse_args()
FILES = [args.design, 'design/contrasts-Vprime.json', 'arms/panel/SHA-LEDGER.json', 'tools/run_preamble_api.py', 'tools/gate_vprime.py', 'tools/analyze_vprime.py',
         'tools/build_combo_arms_vprime.py', 'tools/power_grid_vprime.py', 'tools/design_facts_vprime.py', 'tools/arms_string_vprime.py',
         'records/power-grid-Vprime.md', 'records/power-grid-Vprime.json', 'records/design-facts-Vprime.md', 'records/design-facts-Vprime.json', 'records/predictions/predictions-form-Vprime-v0.4.html']
FILES += sorted(os.path.relpath(p, REPO).replace('\\', '/') for p in glob.glob(os.path.join(REPO, 'arms', 'panel', '*.md')))


def sha16(rel):
    b = open(os.path.join(REPO, rel), 'rb').read().replace(b'\r\n', b'\n')
    return hashlib.sha256(b).hexdigest()[:16].upper(), len(b)


if args.verify:
    M = json.load(open(args.verify, encoding='utf-8')); bad = []
    for rel, v in M['files'].items():
        try:
            s, n = sha16(rel)
        except FileNotFoundError:
            bad.append((rel, v['sha16'], 'MISSING')); continue
        if s != v['sha16']:
            bad.append((rel, v['sha16'], s))
    print('[freeze] %d/%d 一致' % (len(M['files']) - len(bad), len(M['files'])))
    for b in bad:
        print('[freeze] 不一致: %s 凍結 %s 現物 %s' % b)
    sys.exit(2 if bad else 0)
missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
if missing:
    sys.exit('[freeze] 見当たらない: %s' % missing)
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-Vprime.json'), encoding='utf-8'))
M = {'program': 'ontology-preamble-4b / 追補 V′', 'contrasts_version': T['version'], 'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'rule': 'SHA-256 of bytes (CRLF->LF), first 16 hex upper', 'files': {}}
for f in FILES:
    s, n = sha16(f); M['files'][f] = {'sha16': s, 'bytes': n}
base = os.path.join(REPO, 'records', 'freeze-Vprime-%s' % datetime.date.today().isoformat()); p = base + '.json'; k = 2
while os.path.exists(p):
    p = '%s-%d.json' % (base, k); k += 1
json.dump(M, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('written', p, '(%d files)' % len(M['files']))
for f in FILES[:15]:
    print('  %s %s %d' % (M['files'][f]['sha16'], f, M['files'][f]['bytes']))
