# -*- coding: utf-8 -*-
"""dry_bprime_directions.py v0（2026-09-29・B′ の方向の器の合成データの確かめ・小さな乱数の Gemma 4・手元の CPU・コーディネータ南無弥勒如来）。

実物の升目のトークンの並び（凍結の腕と場面から組んだもの）を、小さな乱数の模型に流す（乱数の模型の値に意味は無い・実物の模型の値は見ない）。
確かめること:
  D1 抽出の文脈は 16（八腕 × 二場面）で、主位置の字はどれも `<channel|>`。
  D2 フックで取った主位置の値が、同じ順伝播の `hidden_states[k+1]` の主位置の値と一致する（抽出の層の取り違えが無い）。
  D3 名前のある方向・等方・実在の差の方向のノルムが、どれも ‖static‖ にそろう。
  D4 実在の差の方向は 28 本で、名の並びは八腕の順の i<j。
  D5 同じ入力から二度作った npz が同一バイト（時刻を持たない）。
  D6 等方の方向は種で決まる（同じ種で同一・違う種で違う）。
出力: `dry-bprime-directions-2026-09-29.md`・`.json`（機械生成）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import torch
import bprime_gemma as G
import bprime_cells as BC
import bprime_directions as BD
import dry_bprime as DB
from transformers import AutoTokenizer
NL = chr(10)


def main():
    tok = AutoTokenizer.from_pretrained(DB.HF)
    m = DB.tiny_model()
    n = G.n_layers(m)
    k = G.layer_index(0.5, n)
    X = BC.ids_for(tok)
    ctx = X['extract']
    res = {}
    res['D1_contexts'] = {'pass': len(ctx) == 16 and all(tok.decode([ids[-1]]) == '<channel|>' for ids in ctx.values()), 'n': len(ctx)}
    acts, norms = BD.activations(m, ctx, k)
    key0 = next(iter(ctx))
    ids0 = ctx[key0]
    with torch.no_grad():
        o = m(input_ids=torch.tensor([ids0]), output_hidden_states=True, use_cache=False)
    hs = o.hidden_states[k + 1][0, G.main_position(ids0)].double().numpy()
    res['D2_alignment'] = {'pass': bool(np.allclose(hs, acts[key0], atol=1e-6)), 'max_abs': float(np.max(np.abs(hs - acts[key0])))}
    arrays, names, meta = BD.build(acts, 0.5, 92001, 50)
    nv = meta['vhat_norm']
    rel = max(float(np.max(np.abs(np.linalg.norm(arrays[g], axis=1) / nv - 1.0))) for g in arrays)
    res['D3_norms'] = {'pass': rel < 1e-12, 'max_rel_dev': rel}
    import itertools
    want = ['%s~%s' % (BD.REAL_ARMS[i], BD.REAL_ARMS[j]) for i, j in itertools.combinations(range(len(BD.REAL_ARMS)), 2)]
    res['D4_real_pairs'] = {'pass': names['real'] == want and len(want) == 28, 'n': len(names['real'])}
    a2, _, _ = BD.build(acts, 0.5, 92001, 50)
    b1, b2 = BD.npz_bytes(arrays), BD.npz_bytes(a2)
    res['D5_npz_bytes_same'] = {'pass': b1 == b2, 'sha16': hashlib.sha256(b1).hexdigest().upper()[:16]}
    a3, _, _ = BD.build(acts, 0.5, 92002, 50)
    res['D6_iso_seeded'] = {'pass': np.array_equal(arrays['iso'], a2['iso']) and not np.array_equal(arrays['iso'], a3['iso'])}
    allpass = all(v['pass'] for v in res.values())
    out = {'tests': res, 'all_pass': allpass, 'meta': {'selected_layer_tiny': k, 'n_layers_tiny': n, 'iso_count_dry': 50, 'iso_seed_dry': 92001, 'note': '種と本数は枠で決める（ここでは合成の確かめの値）'}}
    json.dump(out, open(os.path.join(HERE, 'dry-bprime-directions-2026-09-29.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    L = ['# B′ の方向の器の合成データの確かめ（機械生成・`dry_bprime_directions.py`・小さな乱数の Gemma 4・実物の升目のトークンの並び）', '',
         '| 確かめ | 通ったか | 値 |', '|---|---|---|']
    for name, v in res.items():
        L.append('| %s | %s | %s |' % (name, '通った' if v['pass'] else '**落ちた**', '・'.join('%s %s' % (a, ('%.3g' % b) if isinstance(b, float) else b) for a, b in v.items() if a != 'pass') or '—'))
    L += ['', '- すべて通ったか: %s' % ('はい' if allpass else '**いいえ**'), '- 種と本数（92001・50 本）は合成の確かめのための値で、本の値は枠で決める。', '',
          '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(os.path.join(HERE, 'dry-bprime-directions-2026-09-29.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print(json.dumps(res, ensure_ascii=False))
    print('ALL PASS' if allpass else 'SOME FAILED')


if __name__ == '__main__':
    main()
