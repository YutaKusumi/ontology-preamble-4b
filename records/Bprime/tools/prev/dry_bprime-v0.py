# -*- coding: utf-8 -*-
"""dry_bprime.py v0（2026-09-29・B′ の器の合成データの確かめ・小さな乱数の Gemma 4・手元の CPU・コーディネータ南無弥勒如来）。

確かめること（壊した器が落ちることも見る）:
  T1 出口の値の自己検査が通る（正しい器）。
  T2 最後の層の自己検査が通る（正しい器）。
  T3 正規化を二重に掛けた器は T1 で落ちる。
  T4 softcap を抜いた器は T1 で落ちる。
  T5 抽出の層（hidden_states[k+1]）と加減の層（layers[k] の出力）が、選ぶ層で一致する。最後の層では一致しない（Gemma 4 の例外を記録する）。
  T6 一つ隣の層にフックを掛けた器は、正しい器と効き目が違う（加減の層の取り違えが値に出る）。
  T7 行ごとに違う方向を一つのバッチで流しても、一本ずつ流したときと効き目が同じ。
  T8 符号 −1 は、方向を反転して符号 +1 で流したのと同じ。
  T9 すべての確かめの後に、どの層にもフックが残っていない。
合成の模型は、取った設定（版は固定）の辞書の大きさだけを縮めて組み、softcap が効くように語彙の行列（埋め込みと共有）を大きくし、最後の正規化の重みを乱数にする。
場面の文と腕の文は使わない。出力: `dry-bprime-2026-09-29.json`・`.md`（機械生成）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, copy, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import torch
import bprime_gemma as G
import bprime_run as BR
import bl3_core as K
import transformers
from transformers import AutoTokenizer, Gemma4Config, Gemma4ForConditionalGeneration

HF = os.path.join(HERE, '..', 'hf', 'gemma-4-31B-it', '842da3794eaa0b77d5f08bae87a17459d91ff475')
NL = chr(10)


def tiny_model(seed=0, wscale=40.0):
    d = json.load(open(os.path.join(HF, 'config.json'), encoding='utf-8'))
    td = d['text_config']
    td.update(hidden_size=64, intermediate_size=128, num_hidden_layers=6, num_attention_heads=4, num_key_value_heads=2, head_dim=16, global_head_dim=32, num_global_key_value_heads=1)
    td['layer_types'] = list(td['layer_types'][:6])
    vd = d['vision_config']
    vd.update(hidden_size=32, intermediate_size=64, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2, head_dim=16, global_head_dim=16)
    torch.manual_seed(seed)
    m = Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).float().eval()
    with torch.no_grad():
        m.lm_head.weight.mul_(wscale)                     # 埋め込みと共有・softcap が効く大きさにする
        for p in G.final_norm(m).parameters():
            p.copy_(torch.randn_like(p) * 0.5 + 1.0)       # 正規化の重みを乱数に（二重の正規化が値に出るように）
    return m


def main():
    tok = AutoTokenizer.from_pretrained(HF)
    m = tiny_model()
    n = G.n_layers(m)
    k = G.layer_index(0.5, n)
    prompt = G.apply_chat(tok, '合成の確かめの文（場面の文ではない）。')
    prefix = tok.encode('{"choice": "', add_special_tokens=False)
    letters = ['a', 'b', 'c', 'd']
    set_ids = []
    for ch in letters:
        t = tok.encode(ch, add_special_tokens=False)
        assert len(t) == 1, ('一字が一トークンでない', ch, t)
        set_ids.append(t[0])
    cell = BR.Cell('SYN|dry|+1', prompt, prefix, set_ids, G.main_position(prompt))
    # 方向: 選ぶ層の残差のノルムに合わせた乱数の方向
    with torch.no_grad():
        o = m(input_ids=torch.tensor([cell.ids]), output_hidden_states=True, use_cache=False)
    hnorm = float(o.hidden_states[k + 1][0, cell.mp].norm())
    rng = np.random.default_rng(20260929)
    dirs = {}
    for name in ('v1', 'v2', 'iso:0', 'iso:1'):
        v = rng.standard_normal(m.lm_head.weight.shape[1])
        dirs[name] = v / np.linalg.norm(v) * hnorm * 0.5
    coef = 1.0
    base_all = [len(getattr(L, '_forward_hooks', {}) or {}) for L in G.decoder_layers(m)]      # transformers 5 の隠れ状態を集めるフック（ここで掛かっている）
    base_pre = len(getattr(G.final_norm(m), '_forward_pre_hooks', {}) or {})
    R = BR.Runner(m, k, coef, dirs)
    res = {}
    t1 = R.logit_check(cell, 1e-3)
    res['T1_logit_check_correct'] = {'pass': t1['pass'], 'max_abs': t1['max_abs']}
    t2 = R.layer_check(cell, +1, 'v1', 1e-4)
    res['T2_layer_check_correct'] = {'pass': t2['pass'], 'diff': t2['diff']}
    t3 = BR.Runner(m, k, coef, dirs, bug='double_norm').logit_check(cell, 1e-3)
    res['T3_double_norm_caught'] = {'pass': not t3['pass'], 'max_abs': t3['max_abs']}
    t4 = BR.Runner(m, k, coef, dirs, bug='no_softcap').logit_check(cell, 1e-3)
    res['T4_no_softcap_caught'] = {'pass': not t4['pass'], 'max_abs': t4['max_abs']}
    cap = {}
    hk = G.decoder_layers(m)[k].register_forward_hook(lambda mod, a, out: cap.__setitem__('k', (out[0] if isinstance(out, tuple) else out).detach().clone()))
    hl = G.decoder_layers(m)[n - 1].register_forward_hook(lambda mod, a, out: cap.__setitem__('last', (out[0] if isinstance(out, tuple) else out).detach().clone()))
    with torch.no_grad():
        o2 = m(input_ids=torch.tensor([cell.ids]), output_hidden_states=True, use_cache=False)
    hk.remove(); hl.remove()
    res['T5_alignment'] = {'pass': bool(torch.allclose(o2.hidden_states[k + 1], cap['k'])) and not bool(torch.allclose(o2.hidden_states[n], cap['last'])),
                           'selected_layer_match': bool(torch.allclose(o2.hidden_states[k + 1], cap['k'])), 'last_layer_match': bool(torch.allclose(o2.hidden_states[n], cap['last']))}
    e_ok = R.forward(cell, [K.NOOP, 'v1'], +1, full=False)
    e_bad = BR.Runner(m, k, coef, dirs, bug='hook_next_layer').forward(cell, [K.NOOP, 'v1'], +1, full=False)
    d_ok, d_bad = float(e_ok['lo'][1] - e_ok['lo'][0]), float(e_bad['lo'][1] - e_bad['lo'][0])
    res['T6_next_layer_differs'] = {'pass': abs(d_ok - d_bad) > 1e-3, 'effect_correct': d_ok, 'effect_next_layer': d_bad}
    names = ['v1', 'v2', 'iso:0', 'iso:1']
    eb = R.forward(cell, [K.NOOP] + names, +1, full=False)
    single = [float(R.forward(cell, [K.NOOP, nm], +1, full=False)['lo'][1]) for nm in names]
    batched = [float(x) for x in eb['lo'][1:]]
    res['T7_batch_invariance'] = {'pass': max(abs(a - b) for a, b in zip(single, batched)) < 1e-4, 'max_abs': max(abs(a - b) for a, b in zip(single, batched))}
    dirs_neg = dict(dirs, **{'v1neg': -dirs['v1']})
    Rn = BR.Runner(m, k, coef, dirs_neg)
    a = float(Rn.forward(cell, ['v1'], -1, full=False)['lo'][0])
    b = float(Rn.forward(cell, ['v1neg'], +1, full=False)['lo'][0])
    res['T8_sign'] = {'pass': abs(a - b) < 1e-5, 'diff': abs(a - b)}
    now_all = [len(getattr(L, '_forward_hooks', {}) or {}) for L in G.decoder_layers(m)]
    now_pre = len(getattr(G.final_norm(m), '_forward_pre_hooks', {}) or {})
    ours = sum(len(G._ours(L)) for L in G.decoder_layers(m))
    res['T9_no_hooks_left'] = {'pass': now_all == base_all and now_pre == base_pre and ours == 0, 'ours_left': ours, 'foreign_per_layer': '・'.join(str(x) for x in G.foreign_hooks(m))}
    allpass = all(v['pass'] for v in res.values())
    meta = {'version': {'dry_bprime': 'v0', 'bprime_run': BR.VERSION, 'bprime_gemma': G.VERSION}, 'transformers': transformers.__version__, 'torch': torch.__version__,
            'config_sha16': hashlib.sha256(open(os.path.join(HF, 'config.json'), 'rb').read()).hexdigest().upper()[:16], 'n_layers_tiny': n, 'layer_index_rule': 'direction_B.layer_index(0.5, n)', 'selected_layer': k,
            'prompt_len': len(prompt), 'prefix_len': len(prefix), 'set_letters': letters, 'softcap': G.softcap(m), 'main_position_token': tok.decode([cell.ids[cell.mp]])}
    out = {'meta': meta, 'tests': res, 'all_pass': allpass}
    json.dump(out, open(os.path.join(HERE, 'dry-bprime-2026-09-29.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    L = ['# B′ の器の合成データの確かめ（機械生成・`dry_bprime.py`・小さな乱数の Gemma 4・手元の CPU）', '',
         '- 版: transformers %s・torch %s・設定の SHA16 %s（小さな模型は大きさだけ縮めた）。選ぶ層の添字 %d（層 %d・割合 0.5・段階 B の式）。主位置のトークン `%s`。softcap %s。' % (
             meta['transformers'], meta['torch'], meta['config_sha16'], k, n, meta['main_position_token'].replace(NL, '\\n'), meta['softcap']), '',
         '| 確かめ | 通ったか | 値 |', '|---|---|---|']
    for name, v in res.items():
        L.append('| %s | %s | %s |' % (name, '通った' if v['pass'] else '**落ちた**', '・'.join('%s %s' % (a, ('%.3g' % b) if isinstance(b, float) else b) for a, b in v.items() if a != 'pass')))
    L += ['', '- すべて通ったか: %s' % ('はい' if allpass else '**いいえ**'), '',
          '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(os.path.join(HERE, 'dry-bprime-2026-09-29.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print(json.dumps(res, ensure_ascii=False))
    print('ALL PASS' if allpass else 'SOME FAILED')


if __name__ == '__main__':
    main()
