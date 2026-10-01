# -*- coding: utf-8 -*-
"""bprime_directions.py v0（2026-09-29・B′ の方向の抽出と帰無の方向の作り方・Gemma-4-31B-it・コーディネータ南無弥勒如来）。

段階 B と層三からの持ち越し:
  - 抽出の位置は主位置（組み立て済みの列の最後のトークン・Gemma では `<channel|>`）、層は選んだ層の出力（`layers[k]` の出力をフックで取る）。
  - 名前のある方向は段階 B と同じ定義: static（v̂）＝h_O − h_Osec・loaded（(6b)）＝h_{O-Ncold} − h_{Osec-Ncold}・Nk＝h_Nk − h_N・td＝h_Onull − h_N
    （h は抽出の二場面 N1・S1 の平均）。どれも ‖static‖ に合わせる（凍結の `steer_B.match_to_static`）。
  - 等方の方向は凍結の `blens_core.iso_directions`（種と層の割合から・‖static‖ に合わせる）、実在の差の方向は凍結の `blens_core.real_differences`（八腕の全ての対・名の並びは八腕の順の i<j）。
  - npz は凍結の `bl3_directions.write_npz_fixed`（時刻を持たない形・再実行で同一バイト）。
B′ で変えた所: 名前のある方向は Gemma から抽出する（段階 B の npz は Qwen のもので使えない）。段階 B のランダム方向の三本と、近道の確かめの一本は置かない。
種と本数は枠で決める（ここでは引数）。抽出の器は効き目を一つも計算しない（読み取りをしない）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, hashlib, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G

VERSION = 'v0'
REAL_ARMS = ['O', 'Osec', 'Onull', 'Nk', 'N', 'O-Ncold', 'Osec-Ncold', 'Onull-Ncold']
EXTRACT_SCENES = ['N1', 'S1']
NAMED = collections.OrderedDict([('static', ('O', 'Osec')), ('loaded', ('O-Ncold', 'Osec-Ncold')), ('Nk', ('Nk', 'N')), ('td', ('Onull', 'N'))])
sha_arr = lambda x: hashlib.sha256(np.ascontiguousarray(np.asarray(x, dtype=np.float64)).tobytes()).hexdigest().upper()


def activations(model, contexts, layer_idx):
    """文脈（名 → トークンの並び）ごとに、選んだ層の出力の主位置の値（float64）を返す。加減はしない。値の絶対の大きさ（ノルム）も返す。"""
    import torch
    dev = next(model.parameters()).device
    layer = G.decoder_layers(model)[layer_idx]
    out, norms = collections.OrderedDict(), collections.OrderedDict()
    for key, ids in contexts.items():
        mp = G.main_position(ids)
        cap = {}
        h = layer.register_forward_hook(lambda m, a, o: cap.__setitem__('h', (o[0] if isinstance(o, tuple) else o)[0, mp, :].detach().double().cpu().numpy()))
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([ids], device=dev), use_cache=False, logits_to_keep=1)
        finally:
            h.remove()
        out[key] = cap['h']
        norms[key] = float(np.linalg.norm(cap['h']))
    return out, norms


def arm_means(acts):
    """文脈の名（`場面|腕`）から、腕ごとの抽出の二場面の平均（八腕の順）。"""
    return collections.OrderedDict((arm, np.mean([acts['%s|%s' % (sc, arm)] for sc in EXTRACT_SCENES], axis=0)) for arm in REAL_ARMS)


def build(acts, layer_ratio, iso_seed, iso_count, layer_key_scale=1000):
    import steer_B
    import blens_core as C
    M = arm_means(acts)
    static = M['O'] - M['Osec']
    nv = float(np.linalg.norm(static))
    named = collections.OrderedDict((k, steer_B.match_to_static(M[a] - M[b], static)) for k, (a, b) in NAMED.items())
    iso = np.asarray(C.iso_directions(static, int(iso_seed), float(layer_ratio), int(iso_count), int(layer_key_scale)), dtype=np.float64)
    real = C.real_differences(M, nv)
    arrays = collections.OrderedDict([('named', np.array(list(named.values()), dtype=np.float64)), ('iso', iso), ('real', np.array(list(real.values()), dtype=np.float64))])
    names = collections.OrderedDict([('named', list(named)), ('iso', ['iso:%d' % i for i in range(len(iso))]), ('real', list(real))])
    meta = {'layer_ratio': float(layer_ratio), 'dim': int(static.shape[0]), 'vhat_norm': nv, 'iso_seed': int(iso_seed), 'iso_count': int(iso_count), 'layer_key_scale': int(layer_key_scale),
            'sha256': {k: sha_arr(v) for k, v in arrays.items()}}
    return arrays, names, meta


def npz_bytes(arrays):
    import bl3_directions as BD
    return BD.write_npz_fixed(None, arrays)
