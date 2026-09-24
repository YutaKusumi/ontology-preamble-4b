# -*- coding: utf-8 -*-
# 走らせる器の経路の手早い確かめ（乱数の小さな模型・実の重みではない・記録に残す確かめは dry_run_Bl3.py で行う）。
import os, sys, json, time
REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import numpy as np, torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
import bl3_run as BR, bl3_core as K, direction_B
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
tok = AutoTokenizer.from_pretrained(SNAP)
cfg = AutoConfig.from_pretrained(SNAP)
cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim, cfg.intermediate_size = 64, 4, 4, 2, 16, 128
if getattr(cfg, 'layer_types', None):
    cfg.layer_types = list(cfg.layer_types)[:cfg.num_hidden_layers]
torch.manual_seed(0)
model = AutoModelForCausalLM.from_config(cfg).to(torch.bfloat16).eval()
L = direction_B.layer_index(0.5, cfg.num_hidden_layers)
rng = np.random.default_rng(0)
dirs = {n: rng.normal(size=64) for n in ['static', 'loaded', 'Nk', 'td', 'rand:0', 'check']}
R = BR.Runner(model, T3, L, 2.0, dirs)
cells = BR.build_cells(tok, T3, FJ, ['S1|O-Ncold', 'N1|Onull'])
c = cells['S1|O-Ncold']
t0 = time.time()
print('logit check', R.logit_check(c, 0.5))
print('layer check', R.layer_check(c, -1, 'static', 1e-4))
r16 = R.forward(c, [K.NOOP] * 16, +1, full=False)
r1 = R.forward(c, [K.NOOP], +1, full=False)
print('spread 16 vs 1', float(np.max(r16['lo']) - np.min(r16['lo'])), float(r16['lo'][0] - r1['lo'][0]))
pc = R.prefix_cache(c)
rs = R.forward(c, [K.NOOP, 'static', 'Nk'], -1, pc=pc, full=False)
rf = R.forward(c, [K.NOOP, 'static', 'Nk'], -1, full=False)
print('short vs full lo', rs['lo'] - rf['lo'])
print('zero row effect (full)', rf['lo'] - rf['lo'][0])
print('steered', BR.steered_cache_check(R, [(c, -1), (cells['N1|Onull'], +1)], 16, 0.005))
Rb = BR.Runner(model, T3, L, 2.0, dirs, bug='cache_through_mp')
print('steered (bug cache_through_mp)', BR.steered_cache_check(Rb, [(c, -1)], 16, 0.005)['max_abs'])
Rd = BR.Runner(model, T3, L, 2.0, dirs, bug='double_norm')
print('logit check (bug double_norm)', Rd.logit_check(c, 0.5))
print('time', round(time.time() - t0, 1), 'n_forward', R.n_forward)
