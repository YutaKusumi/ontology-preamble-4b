# -*- coding: utf-8 -*-
"""起動器の DRY の出力（JSON）を手元の集計の器にそのまま読ませる（往復の形の確かめ・合成だけ・記録用ではない）。値は印字しない。"""
import os, sys, json, glob, copy
REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
SP = r'C:\Users\PC\AppData\Local\Temp\claude\C--Users-PC\e815e703-8cfe-466b-b434-54ac55be02b1\scratchpad\boot-dry'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import analyze_Bl3 as AZ

T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
md = sorted(glob.glob(os.path.join(SP, 'main-*')))
md = [d for d in md if os.path.isdir(d)][-1]
pd = [d for d in sorted(glob.glob(os.path.join(SP, 'pilot-*'))) if os.path.isdir(d)][-1]
M = json.load(open(os.path.join(md, 'main.json'), encoding='utf-8'))
RC = json.load(open(os.path.join(md, 'recompute.json'), encoding='utf-8'))
SC = json.load(open(os.path.join(md, 'secondary.json'), encoding='utf-8'))
S = json.load(open(os.path.join(md, 'session.json'), encoding='utf-8'))
P = json.load(open(os.path.join(pd, 'pilot.json'), encoding='utf-8'))['pilot']
n_iso = RC['n_iso']
T3d = copy.deepcopy(T3)
T3d['nulls']['isotropic']['count'] = n_iso
AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
hook = RC['hook']
out = AZ.analyze(T3d, FJ, M['cells'], [P], DJ['groups']['real']['names'], rows_gate, hook=hook, rewrite=None, style_rows=style_rows, rows_subset=set(hook))
print('keys', list(out))
print('rows', len(out['rows']), 'gates', list(out['gates']), 'truth keys', list(out['predictions_truth']))
print('recompute second agree', out['recompute']['second']['agree'], 'first', out['recompute']['first'])
print('session parts', S['parts'], 'pilot_used', {k: (type(v).__name__) for k, v in S['pilot_used'].items()})
print('main head keys', list(M['head']), 'cells', len(M['cells']), 'layers keys', list(next(iter(M['cells'].values()))['layers']))
print('secondary', SC['counts'], len(SC['contexts']), list(SC['contexts'][0]))
calib = json.load(open(os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json'), encoding='utf-8'))['magnitude']['letter']
summ = AZ.secondary_summary(SC['contexts'], calib)
print('secondary summary rows', len(summ), 'with blens_direct', sum(1 for v in summ.values() if v.get('blens_direct')))
