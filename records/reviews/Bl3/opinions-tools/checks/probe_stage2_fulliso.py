# -*- coding: utf-8 -*-
"""全等方の試しで二段目が許容を超えた（6.72e-03 > 0.005）わけを切り分ける（乱数の小さな模型・合成だけ・記録用の切り分け）。
升目と符号ごとに、全ての方向を本の計算と同じバッチの組み方で、近道ありと近道なし（どちらもバッチ 16）で流し、効き目の差の分布を見る。
近道の確かめ（頭）は一本の方向だけを見るので、多くの方向の最大と比べる。値は合成の模型のもので意味は無い。"""
import os, sys, json, time
REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import numpy as np
import dry_run_Bl3 as DR
import bl3_run as BR
import bl3_core as K
import direction_B
from transformers import AutoTokenizer

T3, FJ, DJ = DR.T3, DR.FJ, DR.DJ
tok = AutoTokenizer.from_pretrained(DR.SNAP)
model, cfg = DR.tiny_model()
L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
iso_n = T3['nulls']['isotropic']['count']
names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(3)] + ['iso:%d' % i for i in range(iso_n)] + ['real:' + p for p in DJ['groups']['real']['names']] + ['check']
dirs = DR.synth_dirs(cfg.hidden_size, names)
cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
cells = BR.build_cells(tok, T3, FJ, cell_keys)
DR.calibrate_readout_rows(model, BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs), cells[cell_keys[0]], FJ)
R = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs)
gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
sets = BR.cell_sign_sets(T3, None, T3['directions']['named'], ['rand:%d' % i for i in range(3)], ['iso:%d' % i for i in range(iso_n)], ['real:' + p for p in DJ['groups']['real']['names']], gate_only)
want = ['N1|Onull|+1', 'S1|O-Ncold|-1']
out = {}
for ki, (key, ck, sg, ds) in enumerate(sets):
    if key not in want:
        continue
    t0 = time.time()
    pc = R.prefix_cache(cells[ck])
    s = BR.run_cell_sign(R, cells[ck], sg, ds, 16, T3['readout']['primary']['order_seed'], ki, pc=pc)
    f = BR.run_cell_sign(R, cells[ck], sg, ds, 16, T3['readout']['primary']['order_seed'], ki, pc=None)
    d_eff = np.array([s['effects'][d] - f['effects'][d] for d in ds])
    d_lo = np.array([s['lo'][d] - f['lo'][d] for d in ds])
    noop_shift = s['lo'][K.NOOP] - f['lo'][K.NOOP]
    out[key] = {'n': len(ds), 'noop_shift': float(noop_shift), 'eff_diff_max_abs': float(np.max(np.abs(d_eff))), 'eff_diff_median': float(np.median(d_eff)),
                'steered_lo_diff_max_abs': float(np.max(np.abs(d_lo))), 'steered_lo_diff_nonzero': int(np.sum(d_lo != 0.0)),
                'n_eff_over_0.005': int(np.sum(np.abs(d_eff) > 0.005)), 'check_dir_eff_diff': float(s['effects']['check'] - f['effects']['check']) if 'check' in s['effects'] else None,
                'q': [float(x) for x in np.percentile(np.abs(d_eff), [50, 90, 99, 100])], 'seconds': round(time.time() - t0, 1)}
    print(key, json.dumps(out[key], ensure_ascii=False), flush=True)
