# -*- coding: utf-8 -*-
"""近道の確かめの差（試走四回目で 3.77e-03）が器の誤りでないかを切り分ける（乱数の小さな模型・合成だけ・記録用ではない）。"""
import os, sys, json
REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import numpy as np
import torch
import dry_run_Bl3 as DR
import bl3_run as BR
import bl3_core as K
import direction_B
from transformers import AutoTokenizer

T3, FJ, DJ = DR.T3, DR.FJ, DR.DJ
tok = AutoTokenizer.from_pretrained(DR.SNAP)
model, cfg = DR.tiny_model()
L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(3)] + ['iso:%d' % i for i in range(5)] + ['real:' + p for p in DJ['groups']['real']['names']] + ['check']
dirs = DR.synth_dirs(cfg.hidden_size, names)
cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
cells = BR.build_cells(tok, T3, FJ, cell_keys)
R0 = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs)
DR.calibrate_readout_rows(model, R0, cells[cell_keys[0]], FJ)
R = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs)
print('norms', {d: round(float(np.linalg.norm(dirs[d])), 3) for d in ('static', 'check', 'iso:0')})
for sc, b, sg in T3['cell_signs_main']:
    c = cells['%s|%s' % (sc, b)]
    sg = int(sg)
    pc = R.prefix_cache(c)
    row = {}
    for did in ('check', 'static'):
        ids_ = [K.NOOP, did] + [K.PAD] * 14
        rf = R.forward(c, ids_, sg, full=False)
        rs = R.forward(c, ids_, sg, pc=pc, full=False)
        ef, es = float(rf['lo'][1] - rf['lo'][0]), float(rs['lo'][1] - rs['lo'][0])
        e1 = float(R.forward(c, [did], sg, full=False)['lo'][0] - R.forward(c, [K.NOOP], sg, full=False)['lo'][0])
        row[did] = {'eff_noshort16': round(ef, 5), 'short-noshort': '%.2e' % (es - ef), 'noshort16-batch1': '%.2e' % (ef - e1),
                    'noop_short-noshort': '%.2e' % float(rs['lo'][0] - rf['lo'][0])}
    print('%s|%s|%+d' % (sc, b, sg), json.dumps(row, ensure_ascii=False))
