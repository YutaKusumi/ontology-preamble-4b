# -*- coding: utf-8 -*-
"""boot_bprime_cost.py v0（2026-09-29・B′ の費用の下見〔門0′〕の Colab の起動器・コーディネータ南無弥勒如来）。

測るもの: Gemma-4-31B-it（bf16）を GPU 一枚に載せたときの記憶の使い方と、読み取りの順伝播（層三の型・行ごとの方向・バッチ）と抽出の順伝播の速さ。
場面の文と腕の文は使わない。升目と同じ長さの、意味のないトークン列（種を固定した乱数の字・頭に BOS・主位置に `<channel|>`・後ろに書き出しの 7 トークン）で測る。
読み取りの値は記録しない（速さと記憶だけ）。方向は乱数（大きさは測った残差のノルムの目安で決めるが、値は記録しない）。
段取り: 包みの中身の SHA を確かめる → transformers の版を確かめる → 公開の置き場を版を固定して浅く取る（凍結の段階 B・層三の器） → 模型を載せる →
        記憶を測る → 読み取りの順伝播の速さ（バッチ 16・32、層ごとの取り出しの有無） → 抽出の順伝播の速さ → 記録を書いてダウンロードする。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, time, hashlib, subprocess, importlib.metadata

KIT = '/content/kit'
REPO_DIR = '/content/op4b'
REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b'
REPO_SHA = '0a456884810681127b6b051da76cd3913cd14f59'
MODEL = 'google/gemma-4-31B-it'
MODEL_REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'
WANT_TF = '5.16.1'
OUT = '/content/cost-bprime.json'
REC = {'what': 'B′ cost pilot (gate 0′)', 'boot': 'v0', 'times': {}, 'mem': {}, 'forward': [], 'extract': {}}


def log(*a):
    print('[boot_bprime_cost]', *a, flush=True)


def stamp(k, t0):
    REC['times'][k] = round(time.time() - t0, 2)
    log(k, REC['times'][k], 's')


T0 = time.time()
# 1. 包みの中身
man = [l.split() for l in open(os.path.join(KIT, 'MANIFEST.sha256'), encoding='utf-8').read().split('\n') if l.strip()]
for h, name in man:
    got = hashlib.sha256(open(os.path.join(KIT, name), 'rb').read()).hexdigest()
    if got != h:
        raise SystemExit('包みの中身の SHA が違う: %s' % name)
REC['kit'] = {name: h[:16].upper() for h, name in man}
log('kit OK', len(man), 'files')
# 2. transformers の版
tf = importlib.metadata.version('transformers')
if tf != WANT_TF:
    log('transformers', tf, '-> installing', WANT_TF)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'transformers==' + WANT_TF], check=True)
    tf = importlib.metadata.version('transformers')
REC['env'] = {'transformers': tf}
# 3. 公開の置き場（凍結の器）
if not os.path.isdir(REPO_DIR):
    subprocess.run(['git', 'clone', '-q', '--depth', '1', REPO_URL, REPO_DIR], check=True)
head = subprocess.run(['git', '-C', REPO_DIR, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
if head != REPO_SHA:
    subprocess.run(['git', '-C', REPO_DIR, 'fetch', '-q', '--depth', '1', 'origin', REPO_SHA], check=True)
    subprocess.run(['git', '-C', REPO_DIR, 'checkout', '-q', REPO_SHA], check=True)
    head = subprocess.run(['git', '-C', REPO_DIR, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
if head != REPO_SHA:
    raise SystemExit('公開の置き場の版が違う: %s' % head)
REC['repo_sha'] = head
stamp('setup', T0)
os.environ['OP4B_REPO'] = REPO_DIR
os.environ['HF_HUB_DISABLE_XET'] = '1'
sys.path.insert(0, KIT)
import numpy as np
import torch
import transformers
from transformers import Gemma4ForConditionalGeneration
import bprime_gemma as G
import bprime_run as BR
import bl3_core as K
REC['env'].update({'torch': torch.__version__, 'cuda': torch.version.cuda, 'gpu': torch.cuda.get_device_name(0),
                   'gpu_total_gib': round(torch.cuda.get_device_properties(0).total_memory / 2**30, 2), 'bprime_gemma': G.VERSION, 'bprime_run': BR.VERSION})
log('env', REC['env'])
# 4. 模型を載せる
t = time.time()
model = Gemma4ForConditionalGeneration.from_pretrained(MODEL, revision=MODEL_REV, dtype=torch.bfloat16, device_map='cuda').eval()
torch.cuda.synchronize()
stamp('load', t)
REC['mem']['after_load_alloc_gib'] = round(torch.cuda.memory_allocated() / 2**30, 2)
REC['mem']['after_load_reserved_gib'] = round(torch.cuda.memory_reserved() / 2**30, 2)
n = G.n_layers(model)
k = G.layer_index(0.5, n)
REC['model'] = {'n_layers': n, 'selected_layer': k, 'softcap': G.softcap(model), 'dim': int(G.final_norm(model).weight.shape[0])}
log('model', REC['model'], REC['mem'])
# 5. 意味のない升目（長さは台帳から）
L = json.load(open(os.path.join(KIT, 'ledger-bprime.json'), encoding='utf-8'))
prefix = L['prefix_ids']
rng = np.random.default_rng(20260929)


def junk(length):
    ids = [2] + [int(x) for x in rng.integers(1000, 250000, size=length - 2)] + [101]
    assert len(ids) == length
    return ids


lens_main = sorted({c['prompt_len'] for c in L['cells_main'].values()})
lens_ext = [c['prompt_len'] for c in L['extract_contexts'].values()]
Lp = max(lens_main)
set_ids = next(iter(L['cells_main'].values()))['set_ids']
cell = BR.Cell('JUNK|cost|%d' % Lp, junk(Lp), prefix, set_ids, Lp - 1)
dim = REC['model']['dim']
with torch.no_grad():
    cap = {}
    hk = G.decoder_layers(model)[k].register_forward_hook(lambda m, a, o: cap.__setitem__('h', (o[0] if isinstance(o, tuple) else o)[0, -1].float().norm().item()))
    model(input_ids=torch.tensor([cell.ids], device='cuda'), use_cache=False, logits_to_keep=1)
    hk.remove()
scale = 0.03 * cap['h']
dirs = {}
for i in range(64):
    v = rng.standard_normal(dim)
    dirs['r%d' % i] = v / np.linalg.norm(v) * scale
R = BR.Runner(model, k, 2.0, dirs)
R.forward(cell, [K.NOOP] + ['r%d' % i for i in range(15)], +1, full=False)      # 温め
torch.cuda.synchronize()
for B in (16, 32):
    for layers_on in (False, True):
        torch.cuda.reset_peak_memory_stats()
        ts = []
        for rep in range(5):
            ids_ = [K.NOOP] + ['r%d' % ((rep * B + j) % 64) for j in range(B - 1)]
            t = time.time()
            R.forward(cell, ids_, +1, want_layers=layers_on, full=layers_on)
            torch.cuda.synchronize()
            ts.append(time.time() - t)
        rec = {'batch': B, 'layers': layers_on, 'len': len(cell.ids), 'sec_median': round(float(np.median(ts)), 4), 'sec_all': [round(x, 4) for x in ts],
               'peak_alloc_gib': round(torch.cuda.max_memory_allocated() / 2**30, 2)}
        REC['forward'].append(rec)
        log('forward', rec)
# 6. 抽出の順伝播（バッチ一・長さは台帳の抽出の文脈）
import bprime_directions as BD
ctx = {'junk%d' % i: junk(l) for i, l in enumerate(lens_ext)}
t = time.time()
BD.activations(model, ctx, k)
torch.cuda.synchronize()
REC['extract'] = {'n_contexts': len(ctx), 'sec_total': round(time.time() - t, 3)}
log('extract', REC['extract'])
# 7. 見込み（式だけ・方向の本数は枠で決める。層三と同じなら升目と符号 12 × 方向 2060 本 ÷ バッチ 16）
per = {r['batch']: r for r in REC['forward'] if r['layers']}
n_dir = 1 + 4 + 1999 + 56
n_fwd16 = 12 * int(np.ceil(n_dir / 16)) + 3 * int(np.ceil((1 + 56) / 16))
REC['estimate_if_Bl3_shape'] = {'directions_per_cellsign': n_dir, 'forwards_batch16': n_fwd16, 'hours_batch16_layers_on': round(n_fwd16 * per[16]['sec_median'] / 3600, 3)}
stamp('total', T0)
json.dump(REC, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sha = hashlib.sha256(open(OUT, 'rb').read()).hexdigest().upper()[:16]
log('COST-DONE sha16=%s load_s=%s total_s=%s gpu=%s est_h=%s' % (sha, REC['times'].get('load'), REC['times'].get('total'), REC['env']['gpu'], REC['estimate_if_Bl3_shape']['hours_batch16_layers_on']))
from google.colab import files
files.download(OUT)
