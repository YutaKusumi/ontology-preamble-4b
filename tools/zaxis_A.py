# -*- coding: utf-8 -*-
"""zaxis_A.py v1 —— 段階 A の横軸 z（実パラメータ数の自然対数・中心は 4B 初版）の共通関数（凍結前検分の採否表 P3・P60・2026-09-13）。
records/A/hf-models-A.json の config.json の値から実パラメータ数を機械計算する。格子（power_grid_A）・設計事実（design_facts_A）・確証の判定（confirm_A）・Firth の自己検査（firth.py）と一致検査（firth_check_A）・集計器（analyze_A）が import し、式を一箇所に置く。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, json, math
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HPATH = os.path.join(REPO, 'records', 'A', 'hf-models-A.json')
CENTER = '4B'


def params(v):
    """config.json の値から実パラメータ数（埋め込み・層・最終正規化）。"""
    V, h, L, i, nh, nkv, hd = v['vocab_size'], v['hidden_size'], v['num_hidden_layers'], v['intermediate_size'], v['num_attention_heads'], v['num_key_value_heads'], v['head_dim']
    return V * h * (1 if v.get('tie_word_embeddings', False) else 2) + L * (h * nh * hd + 2 * h * nkv * hd + nh * hd * h + 2 * hd + 3 * h * i + 2 * h) + h


def load_hf(path=None):
    return json.load(open(path or HPATH, encoding='utf-8'))


def z_map(hf=None, center=CENTER):
    """{機種キー: z}・{機種キー: 実パラメータ数}。"""
    hf = hf or load_hf(); par = {k: params(v) for k, v in hf['models'].items()}
    return {k: math.log(par[k] / par[center]) for k in par}, par


def z_sizes(sizes, hf=None):
    Z, _ = z_map(hf)
    return [Z[s] for s in sizes]
