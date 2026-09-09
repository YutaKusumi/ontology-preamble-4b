# -*- coding: utf-8 -*-
"""freeze_M.py —— 追補 M の凍結マニフェストを発行する（登録者の凍結指示があってから実行する）。
凍結範囲: 本文（凍結版）・正本 JSON・追補 M の盤（arms/panelM/*.md・system/*.md）＋台帳（JSON・md）・器材（走行器 v2.5 と生成器・v2.4 凍結走行器・門・集計器・様式・格子・設計事実・走行腕・合成検査・凍結器）・
格子 md/json・設計事実 md/json・予想様式 v0.6。V′ の凍結物（freeze-Vprime）は別マニフェストで検証し本マニフェストに重複して含めない（run_preamble_api.py v2.4・vprime_power.py は本追補も読むため含める）。
出力: records/freeze-M-<date>.json（同名があれば連番・上書きなし）。--verify <manifest> で現物と突合（不一致は非零終了）。
SHA16 はファイルバイトの SHA-256 先頭 16 桁（CRLF→LF 正規化・strip なし）。
"""
import os, sys, json, glob, hashlib, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--design', default='design/design-stageM-FROZEN.md'); ap.add_argument('--verify', default=None); ap.add_argument('--form', default='records/predictions/predictions-form-M-v0.6.html')
args = ap.parse_args()
FILES = [args.design, 'design/contrasts-M.json', 'arms/panelM/SHA-LEDGER-M.json', 'arms/ledger-M.md', 'tools/run_preamble_api.py', 'tools/run_preamble_api_m.py', 'tools/make_runner_m.py', 'tools/build_arms_M.py', 'tools/make_contrasts_M.py',
         'tools/gate_M.py', 'tools/analyze_M.py', 'tools/response_mode_M.py', 'tools/power_grid_M.py', 'tools/design_facts_M.py', 'tools/arms_string_M.py', 'tools/synth_M.py', 'tools/freeze_M.py', 'tools/vprime_power.py',
         'records/power-grid-M.md', 'records/power-grid-M.json', 'records/design-facts-M.md', 'records/design-facts-M.json', args.form]
FILES += sorted(os.path.relpath(p, REPO).replace('\\', '/') for p in glob.glob(os.path.join(REPO, 'arms', 'panelM', '*.md')) + glob.glob(os.path.join(REPO, 'arms', 'panelM', 'system', '*.md')))


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
    print('[freeze-M] %d/%d 一致' % (len(M['files']) - len(bad), len(M['files'])))
    for b in bad:
        print('[freeze-M] 不一致: %s 凍結 %s 現物 %s' % b)
    sys.exit(2 if bad else 0)
missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
if missing:
    sys.exit('[freeze-M] 見当たらない: %s' % missing)
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8'))
M = {'program': 'ontology-preamble-4b / 追補 M', 'contrasts_version': T['version'], 'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'rule': 'SHA-256 of bytes (CRLF->LF), first 16 hex upper', 'files': {}}
for f in FILES:
    s, n = sha16(f); M['files'][f] = {'sha16': s, 'bytes': n}
base = os.path.join(REPO, 'records', 'freeze-M-%s' % datetime.date.today().isoformat()); p = base + '.json'; k = 2
while os.path.exists(p):
    p = '%s-%d.json' % (base, k); k += 1
json.dump(M, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('written', p, '(%d files)' % len(M['files']))
for f in FILES[:23]:
    print('  %s %s %d' % (M['files'][f]['sha16'], f, M['files'][f]['bytes']))
