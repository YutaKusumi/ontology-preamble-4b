# -*- coding: utf-8 -*-
"""make_facts_round1.py v0（2026-09-29・B′ の設計の巡・二巡目の束のため・一巡目の採否で確かめた事実を出所から機械で抜き出す・コーディネータ南無弥勒如来）。
出所のファイルの SHA16 と行の番号を添え、値は出所から読んだものだけを書く（手で打たない）。出力 `facts-round1.md` は一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, math, hashlib
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'facts-round1.md')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b/'
INT = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime/'
HF = INT + 'hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475/'
NL = chr(10)


def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]


def lines_of(p, nums):
    L = open(p, encoding='utf-8').read().split(NL)
    return [(n, L[n - 1]) for n in nums]


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    out = ['# 一巡目の採否で確かめた事実（機械で抜き出した・B′ の設計の巡・二巡目の束・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
           '- 何か: 一巡目の採否の表（`adoption-design-round1.md`）の「確かめ」の欄の事実を、出所のファイルから器 `make_facts_round1.py` が抜き出したもの。値は出所から読み、手で打っていない。出所の置き場の名は、公開の置き場（`ontology-preamble-4b` の版 0a45688 の後の手元の写し）と、非公開の作業場（B′）。', '']
    # 1. 層三の最終版の行
    p = PUB + 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'
    out += ['## 1. 層三の最終版（公開の置き場 `records/Bl3/results-Bl3-FINAL-2026-09-27.md`・SHA16 %s）の行（逐語）' % sha16(p), '']
    for n, l in lines_of(p, [146, 470, 471]):
        out.append('- %d 行目: %s' % (n, l.lstrip('- ').strip()))
    out.append('')
    # 2. Gemma の設定（固定の版）
    cfg, gen, tok = HF + 'config.json', HF + 'generation_config.json', HF + 'tokenizer.json'
    c = json.load(open(cfg, encoding='utf-8'))
    tc = c['text_config']
    g = json.load(open(gen, encoding='utf-8'))
    t = json.load(open(tok, encoding='utf-8'))
    added = {a['id']: a['content'] for a in t.get('added_tokens', [])}
    lt = tc['layer_types']
    full = [i for i, x in enumerate(lt) if x == 'full_attention']
    out += ['## 2. Gemma-4-31B-it の設定（固定の版 `842da3794eaa0b77d5f08bae87a17459d91ff475`・`config.json` SHA16 %s・`generation_config.json` SHA16 %s・`tokenizer.json` SHA16 %s）' % (sha16(cfg), sha16(gen), sha16(tok)), '',
            '- 上の階層の `final_logit_softcapping`: %s・`text_config` の中: %s' % (json.dumps(c.get('final_logit_softcapping')), json.dumps(tc.get('final_logit_softcapping'))),
            '- `text_config` の `num_hidden_layers` %s・`hidden_size` %s・`sliding_window` %s・`attention_k_eq_v` %s・`global_head_dim` %s' % (tc['num_hidden_layers'], tc['hidden_size'], tc['sliding_window'], json.dumps(tc['attention_k_eq_v']), tc['global_head_dim']),
            '- `layer_types` の全体の注意（full_attention）の層の添字: %s（添字 29 の種類: %s）' % ('・'.join(str(i) for i in full), lt[29]),
            '- 止める印: 上の階層の `eos_token_id` %s・`text_config` の `eos_token_id` %s・`generation_config.json` の `eos_token_id` %s' % (json.dumps(c.get('eos_token_id')), json.dumps(tc.get('eos_token_id')), json.dumps(g.get('eos_token_id'))),
            '- トークンの字（`tokenizer.json` の added_tokens）: %s' % '・'.join('%d＝`%s`' % (i, added.get(i)) for i in (1, 50, 106)),
            '- `generation_config.json` の既定の標本化: temperature %s・top_p %s・top_k %s・do_sample %s（B′ は使わない・11-A）' % (g.get('temperature'), g.get('top_p'), g.get('top_k'), json.dumps(g.get('do_sample'))), '']
    # 3. 段階 B の正本
    pB = PUB + 'design/contrasts-B.json'
    T = json.load(open(pB, encoding='utf-8'))
    gg, ge = T['runner']['generation'], T['runner']['generation_explicit']
    out += ['## 3. 段階 B の正本（公開の置き場 `design/contrasts-B.json`・SHA16 %s）' % sha16(pB), '',
            '- `runner.generation`: temperature %s・top_p %s・max_tokens %s' % (gg.get('temperature'), gg.get('top_p'), gg.get('max_tokens')),
            '- `runner.generation_explicit`: top_k %s・min_p %s・repetition_penalty %s・no_repeat_ngram_size %s・`passed_keys` %s' % (ge.get('top_k'), ge.get('min_p'), ge.get('repetition_penalty'), ge.get('no_repeat_ngram_size'), json.dumps(ge.get('passed_keys'), ensure_ascii=False)),
            '- `arms.panel`: %s・`extraction_scenarios`: %s（段階 B の `direction_B.h_norm_record` の ‖h‖ はこの八腕 × 二場面の平均）' % ('・'.join(T['arms']['panel']), '・'.join(T['extraction_scenarios'])), '']
    # 4. 比の出し直し
    pa = PUB + 'results/dirB/dirB__s1/main_position_activations.npz'
    pl = PUB + 'results/dirB/dirB__s1/layers.json'
    z = np.load(pa)
    arms, scs, r = T['arms']['panel'], T['extraction_scenarios'], '0.5'
    H = {(a, s): z['same_order__%s__%s__%s' % (a, s, r)].astype(np.float64) for a in arms for s in scs}
    hn = float(np.mean([np.linalg.norm(v) for v in H.values()]))
    M = {a: np.mean([H[(a, s)] for s in scs], axis=0) for a in arms}
    vn = float(np.linalg.norm(M['O'] - M['Osec']))
    rec = json.load(open(pl, encoding='utf-8'))['h_norm'][r]
    out += ['## 4. 層三の比の出し直し（段階 B の凍結の活性から・コーディネータの計算）', '',
            '- 活性 `results/dirB/dirB__s1/main_position_activations.npz`（SHA16 %s）の割合 0.5 の `same_order` の十六文脈から: 次元 %d・‖h‖ の平均 %.9f・‖v̂‖ %.9f・比 %.9f' % (sha16(pa), H[(arms[0], scs[0])].shape[0], hn, vn, vn / hn),
            '- 記録 `results/dirB/dirB__s1/layers.json`（SHA16 %s）の割合 0.5: `h_norm_main` %.9f・`vhat_norm` %.9f・`vhat_over_h` %.9f・差（出し直し − 記録）%.2e' % (sha16(pl), rec['h_norm_main'], rec['vhat_norm'], rec['vhat_over_h'], vn / hn - rec['vhat_over_h']), '']
    # 5. 費用の見込みの式と等方の方向の器
    pc = INT + 'tools/boot_bprime_cost.py'
    pb = PUB + 'tools/blens_core.py'
    out += ['## 5. 器の行（逐語）', '',
            '- `Bprime/tools/boot_bprime_cost.py`（SHA16 %s）の費用の見込みの式:' % sha16(pc)]
    for n, l in lines_of(pc, [139, 140, 141]):
        out.append('  - %d 行目: `%s`' % (n, l.strip()))
    out.append('- 公開の置き場 `tools/blens_core.py`（SHA16 %s）の `iso_directions`（乱数は種・層の割合・次元だけで引き、ノルムは後で合わせる）:' % sha16(pb))
    for n, l in lines_of(pb, list(range(99, 111))):
        out.append('  - %d 行目: `%s`' % (n, l.rstrip()))
    out.append('')
    # 6. 計算の値
    f = lambda zz: zz - 30 * math.tanh(zz / 30)
    lo, hi = 5.0, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0.5 else (lo, mid)
    out += ['## 6. 式から出した値（コーディネータの計算）', '',
            '- softcap の抜けの差 z − 30·tanh(z/30): z＝10 で %.4f・11 で %.4f・12 で %.4f・差が 0.5 に届く z は %.3f' % (f(10), f(11), f(12), (lo + hi) / 2),
            '- softcap の傾き sech²(z/30): z＝20 で %.4f・30 で %.4f' % (1 / math.cosh(20 / 30) ** 2, 1 / math.cosh(1) ** 2),
            '- `p_bounds` [0.0001, 0.9999] の両端の対数オッズ: %.4f・%.4f' % (math.log(0.0001 / 0.9999), math.log(0.9999 / 0.0001)),
            '- 層三の偶然の目安: 8/49 ＋ 8/55 ＝ %.4f（正本 `nulls.real.chance_second` と同じか: %s）・8/25 ＋ 8/28 ＝ %.4f（`chance_second_pair` と同じか: %s）' % (8 / 49 + 8 / 55, round(8 / 49 + 8 / 55, 4) == 0.3087, 8 / 25 + 8 / 28, round(8 / 25 + 8 / 28, 4) == 0.6057),
            '- 隠れの次元の比: √(5376/2560) ＝ %.4f・2560/5376 ＝ %.4f' % (math.sqrt(5376 / 2560), 2560 / 5376), '',
            '## この記録が確認していないこと', '',
            '- 公開の置き場の写しが GitHub の上の版と同じか（手元の写しの版 0a45688 の後に push は無い）。',
            '- 固定の版の Gemma の設定が、実物の重みの読み込みで同じ値になるか（凍結の前の確かめで見る）。',
            '',
            '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(out))
    print(NL.join(out))


if __name__ == '__main__':
    main()
