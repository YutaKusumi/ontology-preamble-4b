# -*- coding: utf-8 -*-
"""freeze_F.py —— 段階 F の凍結マニフェストを発行する（登録者の凍結指示があってから実行する）。
凍結範囲: 本文（凍結版）・正本 JSON・段階 F の盤（arms/panelF/*.md）＋台帳（JSON・md）・器材（走行器 v2.6 と生成器・v2.4／v2.5 凍結走行器・門・集計器・計数器・様式・格子・設計事実・走行腕・合成検査・凍結器・整合検査器・抽出器・報告組み立て器）・
格子 md/json・設計事実 md/json・予想様式 v0.7・報告雛形。V′・M の凍結物は各マニフェストで検証し重複して含めない（v2.4・v2.5・vprime_power.py は本段も読むため含める）。
凍結直前の機械検証（系統外 Gemini 2-10）: 報告雛形に「対照の基底率表」「対比別の検出域表」「確証 × 添え札の読み文の表」の枠が実在すること。
出力: records/freeze-F-<date>.json（同名があれば連番・上書きなし）。--verify <manifest> で現物と突合（不一致は非零終了）。SHA16 はファイルバイトの SHA-256 先頭 16 桁（CRLF→LF 正規化・strip なし）。
"""
import os, sys, json, glob, hashlib, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--design', default='design/design-stageF-FROZEN.md'); ap.add_argument('--verify', default=None); ap.add_argument('--form', default='records/predictions/predictions-form-F-v0.7.html'); ap.add_argument('--template', default='records/F/results-report-template-F.md'); ap.add_argument('--dry', action='store_true', help='マニフェストを書かず対象の実在・雛形の枠・SHA を印字するだけ（凍結指示前の検査）')
args = ap.parse_args()
FILES = [args.design, 'design/contrasts-F.json', 'arms/panelF/SHA-LEDGER-F.json', 'arms/ledger-F.md', 'tools/run_preamble_api.py', 'tools/run_preamble_api_m.py', 'tools/run_preamble_api_f.py', 'tools/make_runner_f.py', 'tools/build_arms_F.py', 'tools/make_contrasts_F.py',
         'tools/gate_F.py', 'tools/analyze_F.py', 'tools/response_mode_F.py', 'tools/power_grid_F.py', 'tools/design_facts_F.py', 'tools/arms_string_F.py', 'tools/synth_F.py', 'tools/freeze_F.py', 'tools/integrity_F.py', 'tools/sample_inspection_F.py', 'tools/build_report_F.py',
         'tools/make_predictions_form_F.py', 'tools/make_predictions_preset_F.py', 'tools/compare_predictions_F.py', 'tools/control_chart_F.py', 'tools/check_prompt_sha_F.py', 'tools/vprime_power.py',
         'records/F/power-grid-F.md', 'records/F/power-grid-F.json', 'records/F/design-facts-F.md', 'records/F/design-facts-F.json', args.form, args.template]
FILES += sorted(os.path.relpath(p, REPO).replace('\\', '/') for p in glob.glob(os.path.join(REPO, 'arms', 'panelF', '*.md')))
TEMPLATE_MARKERS = ['対照（U 腕）の基底率', '対比別の検出域', '確証 × 添え札の読み文']


def sha16(rel):
    b = open(os.path.join(REPO, rel), 'rb').read().replace(b'\r\n', b'\n')
    return hashlib.sha256(b).hexdigest()[:16].upper(), len(b)


import subprocess
_r = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'synth_F.py'), '--paths-only'], capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
print('[freeze-F] (c)(d) 五経路（synth_F --paths-only）:', (_r.stdout.strip().split('\n') or ['?'])[-1])
if _r.returncode != 0:
    print(_r.stdout[-1500:]); sys.exit('[freeze-F] (c)(d) 五経路の数値通過に失敗——凍結・検証を停止')
if args.verify:
    M = json.load(open(args.verify, encoding='utf-8')); bad = []
    for rel, v in M['files'].items():
        try:
            s, n = sha16(rel)
        except FileNotFoundError:
            bad.append((rel, v['sha16'], 'MISSING')); continue
        if s != v['sha16']:
            bad.append((rel, v['sha16'], s))
    print('[freeze-F] %d/%d 一致' % (len(M['files']) - len(bad), len(M['files'])))
    for b in bad:
        print('[freeze-F] 不一致: %s 凍結 %s 現物 %s' % b)
    sys.exit(2 if bad else 0)
missing = [f for f in FILES if not os.path.exists(os.path.join(REPO, f))]
if missing:
    sys.exit('[freeze-F] 見当たらない: %s' % missing)
tpl = open(os.path.join(REPO, args.template), encoding='utf-8').read()
lack = [m for m in TEMPLATE_MARKERS if m not in tpl]
if lack:
    sys.exit('[freeze-F] 報告雛形に枠が無い: %s' % lack)
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8'))
M = {'program': 'ontology-preamble-4b / 段階 F', 'contrasts_version': T['version'], 'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'rule': 'SHA-256 of bytes (CRLF->LF), first 16 hex upper', 'template_markers_checked': TEMPLATE_MARKERS, 'files': {}}
for f in FILES:
    s, n = sha16(f); M['files'][f] = {'sha16': s, 'bytes': n}
if args.dry:
    print('[freeze-F --dry] %d files・雛形の枠 %s・書き込みなし' % (len(M['files']), TEMPLATE_MARKERS))
    for f in FILES:
        print('  %s %s %d' % (M['files'][f]['sha16'], f, M['files'][f]['bytes']))
    sys.exit(0)
base = os.path.join(REPO, 'records', 'freeze-F-%s' % datetime.date.today().isoformat()); p = base + '.json'; k = 2
while os.path.exists(p):
    p = '%s-%d.json' % (base, k); k += 1
json.dump(M, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('written', p, '(%d files)' % len(M['files']))
for f in FILES[:31]:
    print('  %s %s %d' % (M['files'][f]['sha16'], f, M['files'][f]['bytes']))
