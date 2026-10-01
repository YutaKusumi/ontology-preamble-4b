# -*- coding: utf-8 -*-
"""dry_bprime.py v1（2026-09-30・B′ の読み取りの器 `bprime_run`・方向の器 `bprime_directions`・行動の下見の器 `bprime_behavior` の生成の設定の部分を、
小さな乱数の Gemma 4（手元の CPU・transformers の固定の版）で確かめる・コーディネータ南無弥勒如来）。前の版は `prev/dry_bprime-v0.py`（v0 の器の API のもの）。

正本 `computation.synthetic_checks` のうち、この器で見るもの（ほかは芯の自己検査と、後の器の合成データの確かめで見る）:
  - 出口の値を cap の近くまで大きくした場合と、小さい値だけの場合（見分ける力の無い位置の印字）の自己検査（R05・S13）→ L 群
  - bf16 の丸めの道の自己検査（正しい実装が「あり」を通り、抜けと二重が落ちる・T04）→ L 群（丸めを模すのでなく、小さな模型を bf16 で動かして実際に丸める）
  - 窓を列より短くした小さな模型（R37）→ すべての群（窓 8・列はそれより長い）
  - 正規化の重みを 0 と 1 から離した値（R37）→ すべての群（最後の正規化の重みを 2〜3 の一様乱数に）・L4（1＋重みの取り違えと重みの掛け忘れが落ちる）
  - 両方の向きの組み方と比べる相手の数（重なりが無い・R23・S20）→ M1
  - (iii) の変換を `generate` と同じ処理の並びで出し、合成の分布で標本の頻度と突き合わせる（S21）→ G 群
  - 止める印が段階 B の値になっている誤りで器が止まる（R17）→ G4
群:
  L（出口の値の自己検査・bf16）: L1 意味のない列の代わりの合成の列で k を測る（バッチ 16 と 1・assert）・L2 正しい器が「合」・L3 正規化の二重と softcap の抜けが「否」・
     L4 1＋重みの取り違えと重みの掛け忘れが「否」・L5 小さい値だけの模型で z₀ が切り替わり、「見分ける力無し」を数えて止めない。
  S（つくり・float32）: S1 選ぶ層の抽出と加減の層の一致（最後の層は一致しない）・S2 最後の層の自己検査（正しい器が通り、一つ隣の層にフックを掛けた器は効き目が違う）・
     S3 行ごとの方向の一つのバッチと一本ずつの一致・S4 符号・S5 抽出が選んだ層で打ち切られ、最後の正規化が呼ばれず、値が hidden_states と一致・
     S6 方向の組（等方は数を減らす・g と一致・npz の同一バイト・読み込みの SHA の確かめ）。
  P（下見・float32）: P1 閾値を緩めた写しで下見が最後まで走り、(vi)・(i)(ii)(iv)・(iii) の値と決めが出る・P2 正本の閾値で決めが出る（止まる側も含む）・
     P3 行動の下見が器の誤りで終わったときに (iii) の相関を計算せず失敗の鍵を置く・P4 行動の下見の状態が決まりの外なら止まる。
  M（本の計算・float32・等方を減らす）: M1 升目と符号の組の数（主の組・逆の向きの組・重なり無し）・M2 すべての組の効き目が有限で、組ごとの方向の数が正本どおり・
     M3 バッチ一の本の計算と、道の違いの記述（バッチ 16 の道）・M4 独立の再計算のフックの道が本の計算の効き目と一致。
  G（生成の設定と (iii)・float32）: G1 `generate` の中で解決された設定と処理の並びが正本と見込みのとおり・G2 取った並びを `generate` の生の値に当てると `generate` の処理後の値と
     一字違わず同じ・G3 合成の分布（語彙の行列の四十行を並べて作る）で、(iii) の変換の値と `generate` の標本の頻度が合う・G4 止める印が別の値で止まる・G5 top_k を渡し忘れると止まる・
     G6 包みが外れる（打ち切り・普通の生成・例外のどれでも）。
  Z: すべての確かめの後に、どの模型のどの層にも B′ のフックが残らず、`generate` の包みも残っていない。
float32 の模型の P・M 群では、出口の値の自己検査の許容に k＝1・z₀＝4 を当てる（許容の測りは L 群・bf16 で見る）。
場面の文と腕の文は使わない（升目の鍵は正本の升目の名を借りるが、プロンプトは合成の文）。書き出しと読み取りの集合の番号は台帳（`ledger-bprime.json`）の値。
出力: `dry-bprime-2026-09-30.json`・`.md`（機械生成・値は器の出力）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, copy, gc, glob, math, hashlib, tempfile, traceback, collections, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import torch
import bprime_gemma as G
import bprime_run as BR
import bprime_directions as BD
import bprime_behavior as BB
import bprime_core as P
import bl3_core as K
import transformers
from transformers import AutoTokenizer, Gemma4Config, Gemma4ForConditionalGeneration, GenerationConfig

VERSION = 'v1.2'        # v1.2（2026-09-30）: 小さな模型の層の出力の倍率 layer_scalar を 0.5〜1.5 の一様乱数にした（K16・別の個体の申し送り）／v1.1: 設定とトークナイザの置き場を環境の変数 OP4B_HF_DIR で与えられるようにした（公開の形の置き場で走らせるため・hf/ は移さない）
BP = os.path.dirname(HERE)
C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
LEDGER = json.load(open(os.path.join(HERE, 'ledger-bprime.json'), encoding='utf-8'))
REV = C['inputs']['model']['revision']
HF = os.environ.get('OP4B_HF_DIR') or os.path.join(BP, 'hf', 'gemma-4-31B-it', REV)
NL = chr(10)
N_TINY = 6
WINDOW = 8
DRY_SEED = 20260930
G3_CALLS, G3_ROWS = 125, 32
KW = BB.sampling_kwargs(C)
RES = collections.OrderedDict()


def check(name, fn):
    """一つの確かめを走らせ、通ったかと値を記録する（例外は落ちたとして記録し、ほかの確かめは続ける）。"""
    t0 = time.time()
    try:
        out = fn()
        out = dict(out)
        out.setdefault('pass', False)
    except Exception as e:                      # 確かめの中の例外は記録して続ける
        out = {'pass': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:300]), 'trace': traceback.format_exc()[-600:]}
    out['sec'] = round(time.time() - t0, 1)
    RES[name] = out
    print('[dry_bprime] %s %s（%.1f 秒）' % (name, '通った' if out['pass'] else '落ちた', out['sec']), flush=True)
    return out


def expect_error(fn, cls=Exception):
    try:
        fn()
    except cls as e:
        return '%s: %s' % (type(e).__name__, str(e)[:160])
    return None


# ---------------- 小さな模型と合成の入力 ----------------
def tiny_model(seed, wscale, dtype):
    """取った設定（版は固定）の大きさだけを縮めた Gemma 4。選ぶ層（割合 0.5 の式）と最後の層を全体の注意、ほかを窓つきの注意にし、窓を列より短くする（R37）。
    語彙の行列（埋め込みと共有）を wscale 倍にし、最後の正規化の重みを 2〜3 の一様乱数にする（0 と 1 から離す・R37）。生成の設定は取った `generation_config.json`。"""
    d = json.load(open(os.path.join(HF, 'config.json'), encoding='utf-8'))
    td = d['text_config']
    k = G.layer_index(C['layers']['ratio'], N_TINY)
    types = ['sliding_attention'] * N_TINY
    types[k] = 'full_attention'
    types[N_TINY - 1] = 'full_attention'
    td.update(hidden_size=64, intermediate_size=128, num_hidden_layers=N_TINY, num_attention_heads=4, num_key_value_heads=2, head_dim=16, global_head_dim=32,
              num_global_key_value_heads=1, sliding_window=WINDOW)
    td['layer_types'] = types
    vd = d['vision_config']
    vd.update(hidden_size=32, intermediate_size=64, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2, head_dim=16, global_head_dim=16)
    torch.manual_seed(seed)
    m = Gemma4ForConditionalGeneration(Gemma4Config.from_dict(d)).eval()
    with torch.no_grad():
        m.lm_head.weight.mul_(wscale)
        w = G.final_norm(m).weight
        w.copy_(torch.empty(w.shape, dtype=torch.float32).uniform_(2.0, 3.0))
        gen_ls = torch.Generator().manual_seed(int(seed) + 7)            # 層の出力の倍率 layer_scalar を 1 から離す（v1.2・足す所がその前か後かの食い違いを見えるように・K16）
        for lay in G.decoder_layers(m):
            lay.layer_scalar.copy_(torch.empty(lay.layer_scalar.shape, dtype=torch.float32).uniform_(0.5, 1.5, generator=gen_ls))
    m = m.to(dtype)
    m.generation_config = GenerationConfig.from_pretrained(HF)
    with torch.no_grad():                      # transformers 5 の隠れ状態を集めるフックを先に掛けさせる（数の基準を取るため・下調べ 10）
        m(input_ids=torch.tensor([[2, 1000, 1001]]), output_hidden_states=True, use_cache=False)
    base = {'pre': len(getattr(G.final_norm(m), '_forward_pre_hooks', {}) or {}), 'foreign': G.foreign_hooks(m)}
    return m, k, base


def set_ids_of(fam):
    heads = LEDGER['heads']
    return [int(heads[x]['next']) for x in C['readout']['primary']['letters'][fam]] + [int(heads['refuse']['next'])]


def syn_cells(tok, keys, tag):
    """升目の鍵ごとの合成の升目（プロンプトは合成の文・書き出しと集合の番号は台帳）。"""
    out = collections.OrderedDict()
    for i, key in enumerate(keys):
        sc, arm = key.split('|')
        fam = LEDGER['cells_main'][key]['family'] if key in LEDGER['cells_main'] else ('nuclear' if sc == 'N1' else 'survival')
        sids = set_ids_of(fam)
        if key in LEDGER['cells_main']:
            assert sids == [int(x) for x in LEDGER['cells_main'][key]['set_ids']], ('台帳の集合の番号と違う', key)
        prompt = G.apply_chat(tok, '合成の確かめの文 %s %d 番（場面の文ではない・%s）。' % (tag, i, key))
        out[key] = BR.Cell(key, sc, arm, fam, prompt, LEDGER['prefix_ids'], sids, G.main_position(prompt))
    return out


def syn_sequences(n_len=8, seed=DRY_SEED):
    """意味のない列の代わりの合成の列（長さ 8 通り × 平らと自信の二種類 × 中身二つ・本物の列の作り方は別の器）。"""
    rng = np.random.default_rng(seed)
    seqs = collections.OrderedDict()
    for L in [12 + 4 * i for i in range(n_len)]:
        for kind in ('flat', 'confident'):
            for c in (0, 1):
                if kind == 'flat':
                    ids = rng.integers(1000, 200000, size=L)
                else:
                    ids = np.resize(rng.integers(1000, 200000, size=3), L)
                seqs['%s-%d-%d' % (kind, L, c)] = [2] + [int(x) for x in ids]
    return seqs


def rand_dirs(m, cell, k, names, scale=0.5, seed=DRY_SEED):
    with torch.no_grad():
        o = m(input_ids=torch.tensor([cell.ids]), output_hidden_states=True, use_cache=False)
    hn = float(o.hidden_states[k + 1][0, cell.mp].float().norm())
    rng = np.random.default_rng(seed)
    out = {}
    for n in names:
        v = rng.standard_normal(int(m.lm_head.weight.shape[1]))
        out[n] = v / np.linalg.norm(v) * hn * scale
    return out


def hooks_clean(m, base):
    ours = sum(len(G._ours(L)) for L in G.decoder_layers(m))
    pre = len(getattr(G.final_norm(m), '_forward_pre_hooks', {}) or {})
    wrapped = [n for n in BB.WRAPPED if n in vars(m)]
    return {'ours': ours, 'pre': pre, 'pre_base': base['pre'], 'foreign': G.foreign_hooks(m), 'foreign_base': base['foreign'], 'wrapped': wrapped,
            'pass': ours == 0 and pre == base['pre'] and G.foreign_hooks(m) == base['foreign'] and not wrapped}


# ---------------- 群 ----------------
def group_L(tok):
    Mb, k, base = tiny_model(1, 40.0, torch.bfloat16)
    L = C['computation']['self_checks']['logit']
    seqs = syn_sequences()
    sids = set_ids_of('nuclear')
    Rb = BR.Runner(Mb, C, k, 1.0, {})
    st = {}

    def L1():
        mk = BR.measure_k(Rb, seqs, sids, L['measure']['batches'])
        st['mk'] = mk
        return {'pass': (not mk['fallback']) and mk['k'] <= L['measure']['asserts']['k_max'] and mk['big_rows'] >= L['measure']['asserts']['big_z_rows_min'],
                'k': mk['k'], 'z0': mk['z0'], 'k_by_batch': {str(b): v for b, v in mk['k_by_batch'].items()}, 'big_rows': mk['big_rows'], 'n_rows': mk['n_rows'], 'positions': len(seqs)}
    check('L1_measure_k_bf16', L1)
    mk = st.get('mk') or {'k': float(L['measure']['asserts']['k_max']), 'z0': L['z0']}
    cells = syn_cells(tok, ['N1|O-Ncold', 'S1|Onull'], 'L')

    def L2():
        s = {c.key: Rb.logit_check(c, mk['k'], mk['z0']) for c in cells.values()}
        return {'pass': all(v['state'] == '合' for v in s.values()), 'states': {c: v['state'] for c, v in s.items()}, 'off': {c: v['off'] for c, v in s.items()}, 'dbl': {c: v['dbl'] for c, v in s.items()}}
    check('L2_correct_passes', L2)

    def L3():
        out = {}
        for bug in ('double_norm', 'no_softcap'):
            Rx = BR.Runner(Mb, C, k, 1.0, {}, bug=bug)
            out[bug] = {c.key: Rx.logit_check(c, mk['k'], mk['z0'])['state'] for c in cells.values()}
        return {'pass': all(v == '否' for d in out.values() for v in d.values()), 'states': out}
    check('L3_bugs_caught', L3)

    def L4():
        out = {}
        for name, f in (('one_plus_weight', lambda g: 1.0 + g), ('weight_missing', lambda g: torch.ones_like(g))):
            Rx = BR.Runner(Mb, C, k, 1.0, {})
            Rx.g32 = f(Rx.g32)
            out[name] = {c.key: Rx.logit_check(c, mk['k'], mk['z0'])['state'] for c in cells.values()}
        w = G.final_norm(Mb).weight.float()
        return {'pass': all(v == '否' for d in out.values() for v in d.values()), 'states': out, 'norm_weight_min': float(w.min()), 'norm_weight_max': float(w.max())}
    check('L4_norm_weight_confusions_caught', L4)
    RES['L_hooks_clean'] = hooks_clean(Mb, base)
    del Rb, Mb
    gc.collect()
    Ms, k, base_s = tiny_model(2, 0.05, torch.bfloat16)
    Rs = BR.Runner(Ms, C, k, 1.0, {})
    cells_s = syn_cells(tok, ['N1|O-Ncold', 'N1|Onull', 'S1|O-Ncold'], 'L5')

    def L5():
        mks = BR.measure_k(Rs, seqs, sids, L['measure']['batches'])
        head = BR.head_logit_checks(Rs, list(cells_s.values()), mks['k'], mks['z0'])
        return {'pass': mks['fallback'] and mks['z0'] == L['z0_fallback'] and head['n_no_discrimination'] >= 1, 'k': mks['k'], 'z0': mks['z0'], 'fallback': mks['fallback'],
                'big_rows': mks['big_rows'], 'states': head['states'], 'n_no_discrimination': head['n_no_discrimination'],
                'off': {c: v['off'] for c, v in head['detail'].items()}, 'dbl': {c: v['dbl'] for c, v in head['detail'].items()}}
    check('L5_small_values_no_discrimination', L5)
    RES['L5_hooks_clean'] = hooks_clean(Ms, base_s)
    del Rs, Ms
    gc.collect()


def group_SPM(tok):
    M, k, base = tiny_model(3, 4.0, torch.float32)
    n = G.n_layers(M)
    st = {}
    cell = syn_cells(tok, ['S1|O-Ncold'], 'S')['S1|O-Ncold']
    dirs = rand_dirs(M, cell, k, ['v1', 'v2', 'iso:0', 'iso:1'])
    R = BR.Runner(M, C, k, 1.0, dirs)

    def S1():
        cap = {}
        hk = G.decoder_layers(M)[k].register_forward_hook(lambda mod, a, out: cap.__setitem__('k', (out[0] if isinstance(out, tuple) else out).detach().clone()))
        hl = G.decoder_layers(M)[n - 1].register_forward_hook(lambda mod, a, out: cap.__setitem__('last', (out[0] if isinstance(out, tuple) else out).detach().clone()))
        try:
            with torch.no_grad():
                o = M(input_ids=torch.tensor([cell.ids]), output_hidden_states=True, use_cache=False)
        finally:
            hk.remove(); hl.remove()
        sel = bool(torch.equal(o.hidden_states[k + 1], cap['k']))
        last = bool(torch.allclose(o.hidden_states[n], cap['last']))
        return {'pass': sel and not last, 'selected_layer_equal': sel, 'last_layer_close': last, 'selected_layer': k, 'layer_types': ''.join('F' if t == 'full_attention' else 's' for t in M.config.get_text_config().layer_types),
                'window': WINDOW, 'seq_len': len(cell.ids)}
    check('S1_alignment', S1)

    def S2():
        ok = R.layer_check(cell, +1, 'v1', C['computation']['layer_tol'])
        e_ok = R.forward(cell, [K.NOOP, 'v1'], +1, full=False)
        e_bad = BR.Runner(M, C, k, 1.0, dirs, bug='hook_next_layer').forward(cell, [K.NOOP, 'v1'], +1, full=False)
        d_ok, d_bad = float(e_ok['lo'][1] - e_ok['lo'][0]), float(e_bad['lo'][1] - e_bad['lo'][0])
        return {'pass': ok['pass'] and abs(d_ok - d_bad) > 1e-3, 'layer_check_diff': ok['diff'], 'layer_tol': ok['tol'], 'effect': d_ok, 'effect_next_layer': d_bad}
    check('S2_layer_check_and_next_layer', S2)

    def S3():
        names = ['v1', 'v2', 'iso:0', 'iso:1']
        eb = R.forward(cell, [K.NOOP] + names, +1, full=False)
        single = [float(R.forward(cell, [K.NOOP, nm], +1, full=False)['lo'][1]) for nm in names]
        batched = [float(x) for x in eb['lo'][1:]]
        d = max(abs(a - b) for a, b in zip(single, batched))
        return {'pass': d < 1e-4, 'max_abs': d}
    check('S3_batch_invariance', S3)

    def S4():
        Rn = BR.Runner(M, C, k, 1.0, dict(dirs, v1neg=-dirs['v1']))
        a = float(Rn.forward(cell, ['v1'], -1, full=False)['lo'][0])
        b = float(Rn.forward(cell, ['v1neg'], +1, full=False)['lo'][0])
        return {'pass': abs(a - b) < 1e-5, 'diff': abs(a - b)}
    check('S4_sign', S4)

    ctx = collections.OrderedDict()
    for sc in BD.EXTRACT_SCENES:
        for arm in BD.REAL_ARMS:
            ctx['%s|%s' % (sc, arm)] = G.apply_chat(tok, '合成の抽出の文（場面 %s・腕 %s の名を借りた合成の文）。' % (sc, arm))

    def S5():
        acts, norms, _ = BD.activations(M, ctx, k)
        worst = 0.0
        for key, ids in ctx.items():
            with torch.no_grad():
                o = M(input_ids=torch.tensor([ids]), output_hidden_states=True, use_cache=False)
            ref = o.hidden_states[k + 1][0, G.main_position(ids)].double().numpy()
            worst = max(worst, float(np.max(np.abs(ref - acts[key]))))
        st['acts'], st['norms'] = acts, norms
        return {'pass': worst == 0.0, 'max_abs_vs_hidden_states': worst, 'contexts': len(ctx)}
    check('S5_extraction_stops_and_matches', S5)

    Cs = copy.deepcopy(C)
    Cs['nulls']['isotropic']['count'] = 25

    def S6():
        acts = st['acts']
        d = int(next(iter(acts.values())).shape[0])
        g = BD.iso_g(Cs['nulls']['isotropic']['seed'], Cs['layers']['ratio'], 25, Cs['nulls']['isotropic']['layer_key_scale'], d)
        arrays, names, meta = BD.build(acts, Cs, g=g)
        b1, b2 = BD.npz_bytes(arrays), BD.npz_bytes(arrays)
        tmp = tempfile.mkdtemp(prefix='dry_bprime_')
        npz = os.path.join(tmp, 'dirs.npz')
        open(npz, 'wb').write(b1)
        rec = {'npz_sha256': hashlib.sha256(b1).hexdigest().upper(), 'groups': {'named': {'names': names['named']}, 'iso': {'count': len(names['iso'])}, 'real': {'names': names['real']}}}
        js = os.path.join(tmp, 'dirs.json')
        json.dump(rec, open(js, 'w', encoding='utf-8'))
        dirs2, names2 = BR.load_dirs(npz, js, Cs)
        st['dirs'], st['names'] = dirs2, names2
        bad = open(npz, 'rb').read()
        open(npz, 'wb').write(bad[:-1] + bytes([bad[-1] ^ 1]))
        err = expect_error(lambda: BR.load_dirs(npz, js, Cs), P.ToolError)
        open(npz, 'wb').write(b1)
        return {'pass': meta['iso_check']['pass'] and b1 == b2 and len(dirs2) == 4 + 25 + 28 + 1 and err is not None and list(names2['named']) == list(C['directions']['named']),
                'iso_rel_max': meta['iso_check']['rel_max'], 'check_cos_max': meta['check_cos_max'], 'npz_same_bytes': b1 == b2, 'n_dirs': len(dirs2), 'sha_mismatch_stops': err}
    check('S6_directions_build_and_load', S6)

    # ---- P 群 ----
    cells = syn_cells(tok, ['%s|%s' % tuple(x) for x in C['cells_main']], 'P')
    variants = {n: tok.encode(s, add_special_tokens=False) for n, s in P.variant_strings(LEDGER['prefix_text']).items() if n != '主'}
    procs = {}

    def P0():
        p, s = BB.chain_for_readout(M, list(cells.values())[0].ids, C, tok, None)
        procs['p'], procs['s'] = p, s
        return {'pass': True, 'chain': [x['type'] for x in s['fixed']['processors']]}
    check('P0_chain_for_readout', P0)
    rates = {key: round(0.05 + 0.1 * i, 2) for i, key in enumerate(cells)}
    Cp = copy.deepcopy(C)
    Cp['pilot']['mass_min'] = 0.0
    Cp['pilot']['p_bounds'] = [0.0, 1.0]

    def P1():
        rec = BR.run_pilot(R, list(cells.values()), Cp, variants, {'status': 'ok', 'rate': rates}, procs['p'], 1.0, 4)
        st['pilot'] = rec
        tr = [rec['cells'][c]['pa_transformed'] for c in cells]
        return {'pass': rec['decision']['q1'] == '続ける' and all(0.0 <= x <= 1.0 for x in tr) and rec['iii']['sentence_key'] in ('positive', 'not_positive', 'undefined') and set(rec['iv']) == {'V1', 'V2', 'V3'},
                'q1': rec['decision']['q1'], 'batch': rec['batch'], 'floor': rec['floor'], 'vi': rec['vi']['decision'], 'iii': rec['iii'], 'logit_states': rec['logit_check']['states'],
                'variant_lens': {n: len(v) for n, v in variants.items()}, 'n_forward': rec['n_forward']}
    check('P1_pilot_full_path', P1)

    def P2():
        rec = BR.run_pilot(R, list(cells.values()), C, variants, {'status': 'ok', 'rate': rates}, procs['p'], 1.0, 4)
        return {'pass': rec['decision']['q1'] in ('続ける', '一部の升目を外して続ける', '止める') and 'iii' in rec, 'q1': rec['decision']['q1'], 'n_pass': rec['decision']['n_pass'],
                'dropped_n': len(rec['decision']['dropped']), 'iii': rec['iii']}
    check('P2_pilot_contract_thresholds', P2)

    def P3():
        rec = BR.run_pilot(R, list(cells.values()), Cp, variants, {'status': 'tool_error', 'rate': None}, procs['p'], 1.0, 4)
        rec2 = BR.run_pilot(R, list(cells.values()), Cp, variants, {'status': 'unscorable', 'rate': rates}, procs['p'], 1.0, 4)
        return {'pass': rec['iii'].get('fail') == 'tool_error' and rec['iii']['sentence_key'] is None and 'rho' not in rec['iii'] and rec2['iii'].get('fail') == 'unscorable' and 'rho' not in rec2['iii'],
                'iii_tool_error': rec['iii'], 'iii_unscorable': rec2['iii']}
    check('P3_pilot_behavior_not_ok', P3)

    def P4():
        e1 = expect_error(lambda: BR.run_pilot(R, list(cells.values()), Cp, variants, {'status': 'closed?', 'rate': rates}, procs['p'], 1.0, 4), P.ToolError)
        r2 = dict(rates)
        r2.pop(next(iter(r2)))
        e2 = expect_error(lambda: BR.run_pilot(R, list(cells.values()), Cp, variants, {'status': 'ok', 'rate': r2}, procs['p'], 1.0, 4), P.ToolError)
        return {'pass': e1 is not None and e2 is not None, 'bad_status': e1, 'missing_rate': e2}
    check('P4_pilot_behavior_guards', P4)

    # ---- M 群 ----
    def M1():
        names = st['names']
        sets = BR.cell_sign_sets(Cs, names['named'], names['iso'][:3], names['real'])
        main = [s for s in sets if s[4]]
        rev = [s for s in sets if not s[4]]
        overlap = [s[0] for s in rev if any(s[1] == m_[1] and s[2] == m_[2] for m_ in main)]
        return {'pass': len(main) == len(C['cell_signs_main']) and len(rev) == C['nulls']['real']['onull_combos'] and not overlap and all(s[3] == list(names['real']) for s in rev),
                'main': len(main), 'reverse': len(rev), 'overlap': overlap}
    check('M1_cell_sign_sets', M1)
    pilot16 = {'batch': C['readout']['primary']['batch'], 'decision': {'dropped': []}}
    pilot1 = {'batch': 1, 'decision': {'dropped': []}}

    def M2():
        Rm = BR.Runner(M, Cs, k, 1.0, st['dirs'])
        out = BR.run_main_phase(Rm, Cs, cells, st['names'], pilot16, 1.0, 4, iso_n=3, log=lambda s: None)
        st['main16'] = out
        n_main = 4 + 3 + C['nulls']['real']['pairs']
        counts = {key: len(o['effects']) for key, o in out['cells'].items()}
        fin = all(math.isfinite(v) for o in out['cells'].values() for v in o['effects'].values())
        want = {key: (n_main if key.split('|')[1] + '|' + key.split('|')[2] in {'%s|%+d' % (b, s) for _, b, s in C['cell_signs_main'] if _ == key.split('|')[0]} else C['nulls']['real']['pairs']) for key in counts}
        return {'pass': fin and counts == want and out['head']['layer_check']['pass'] and len(out['cells']) == len(C['cell_signs_main']) + C['nulls']['real']['onull_combos'],
                'n_combos': len(out['cells']), 'effects_per_combo': sorted(set(counts.values())), 'head_states': out['head']['logit_check']['states'], 'layer_check_diff': out['head']['layer_check']['diff']}
    check('M2_main_phase', M2)

    def M3():
        Rm = BR.Runner(M, Cs, k, 1.0, st['dirs'])
        o1 = BR.run_main_phase(Rm, Cs, cells, st['names'], pilot1, 1.0, 4, iso_n=3, log=lambda s: None)
        o16 = BR.run_main_phase(Rm, Cs, cells, st['names'], pilot1, 1.0, 4, iso_n=3, batch_override=16, log=lambda s: None)
        d_path = max(abs(o1['cells'][key]['effects'][d] - o16['cells'][key]['effects'][d]) for key in o1['cells'] for d in o1['cells'][key]['effects'])
        d_same = max(abs(o16['cells'][key]['effects'][d] - st['main16']['cells'][key]['effects'][d]) for key in o16['cells'] for d in o16['cells'][key]['effects'])
        return {'pass': o1['batch'] == 1 and o16['batch'] == 16 and not o16['head'] and d_path < 1e-4 and d_same == 0.0, 'max_abs_batch1_vs_batch16': d_path, 'max_abs_override_vs_main16': d_same}
    check('M3_batch1_and_path_difference', M3)

    def M4():
        Rm = BR.Runner(M, Cs, k, 1.0, st['dirs'])
        rows = [('r1', cells['S1|O-Ncold'], +1), ('r2', cells['N1|Onull'], +1)]
        dbr = {'r1': [('static', +1), ('iso:0', +1)], 'r2': [('loaded', +1), (st['names']['real'][0], +1)]}
        rc = BR.recompute_hook_path(Rm, rows, dbr)
        main = st['main16']['cells']
        diffs = []
        for name, cell_, sg in rows:
            key = '%s|%+d' % (cell_.key, sg)
            for did, s2 in dbr[name]:
                diffs.append(abs(rc[name]['effects']['%s|%+d' % (did, s2)] - main[key]['effects'][did]))
        return {'pass': max(diffs) < 1e-4, 'max_abs': max(diffs), 'n': len(diffs)}
    check('M4_recompute_hook_path', M4)
    RES['SPM_hooks_clean'] = hooks_clean(M, base)
    del R, M
    gc.collect()


def stageB_model_eos():
    """段階 B の模型（Qwen3-4B-Instruct-2507）の config.json の止める印（手元の Hugging Face の控えから読む・無ければ None）。"""
    hits = sorted(glob.glob(os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub', 'models--Qwen--Qwen3-4B-Instruct-2507', 'snapshots', '*', 'config.json')))
    if not hits:
        return None, None
    e = json.load(open(hits[-1], encoding='utf-8')).get('eos_token_id')
    return ([int(x) for x in e] if isinstance(e, list) else [int(e)]), os.path.basename(os.path.dirname(hits[-1]))


def group_G(tok):
    M, k, base = tiny_model(4, 0.5, torch.float32)
    heads = LEDGER['heads']
    prompt = G.apply_chat(tok, '合成の分布の確かめの文（場面の文ではない）。')
    sids = set_ids_of('survival')
    cell = BR.Cell('SYN|G', 'SYN', 'G', 'survival', prompt, [], sids, G.main_position(prompt))
    R = BR.Runner(M, C, k, 1.0, {})
    a_id = int(heads['a']['next'])
    avoid = set(prompt) | set(C['behavior_pilot']['sampling']['eos_token_id']) | {0, 2, a_id}
    others = [t for t in range(3000, 3200) if t not in avoid][:39]
    designed = others[:3] + [a_id] + others[3:]
    assert a_id not in prompt and len(designed) == 40
    targets = {t: 12.0 - 0.25 * r for r, t in enumerate(designed)}
    h = R.forward(cell, [K.NOOP], +1, full=False)['h'][0:1]
    hn = R.norm32(h)[0]
    with torch.no_grad():
        W = M.lm_head.weight
        for t, a in targets.items():
            W[t] = (a / float(hn @ hn)) * hn
    R = BR.Runner(M, C, k, 1.0, {})
    x = torch.tensor([prompt])
    st = {}
    ver = transformers.__version__

    def G1():
        p, s = BB.chain_for_readout(M, prompt, C, tok, None)
        st['p'], st['s'] = p, s
        return {'pass': True, 'chain': [(q['type'], {kk: vv for kk, vv in q['params'].items() if kk != 'filter_value'}) for q in s['fixed']['processors']], 'eos_tokens': s['fixed']['eos_tokens'],
                'values': s['fixed']['values'], 'stopping': [q['type'] for q in s['fixed']['stopping']]}
    check('G1_resolved_config_and_chain', G1)

    def G2():
        with BB.Capture(M) as cap:
            out = M.generate(input_ids=x, attention_mask=torch.ones_like(x), output_scores=True, output_logits=True, return_dict_in_generate=True, **dict(KW, max_new_tokens=1))
        lp = cap.calls[0]['processors']
        raw, proc = out.logits[0], out.scores[0]
        same_call = bool(torch.equal(lp(x, raw.clone()), proc))
        same_abort = bool(torch.equal(st['p'](x, raw.clone()), proc))
        s2 = BB.summarize(cap.calls[0], tok, list(KW))
        same_desc = s2['fixed']['processors'] == st['s']['fixed']['processors']
        Z = R.forward(cell, [K.NOOP], +1, full=True)['Zfull'][0].float()
        dz = float((Z - raw[0]).abs().max())
        st['Z'] = Z
        return {'pass': same_call and same_abort and same_desc and dz < 1e-4, 'processed_equal_call': same_call, 'processed_equal_abort_chain': same_abort, 'chain_desc_equal': same_desc,
                'max_abs_readout_vs_model_logits': dz}
    check('G2_chain_equals_generate', G2)

    def G3():
        Z = st['Z']
        ptr = {t: BR.transformed_prob(Z, t, st['p'], prompt) for t in designed}
        full = torch.softmax(st['p'](x, Z.unsqueeze(0).clone()).double(), dim=-1)[0]
        kept = [t for t in designed if ptr[t] > 0]
        outside = float(full.sum() - sum(ptr.values()))
        ranks = sorted(designed, key=lambda t: -targets[t])
        zpre = Z.unsqueeze(0).clone()
        for proc in list(st['p'])[:2]:                      # 温度と top_k だけを当てた値（top_p の切れ目の余白を見るため）
            zpre = proc(x, zpre)
        ppre = torch.softmax(zpre.double(), dim=-1)[0]
        cum = np.cumsum([float(ppre[t]) for t in ranks])
        counts = collections.Counter()
        for i in range(G3_CALLS):
            torch.manual_seed(DRY_SEED + i)
            xb = x.repeat(G3_ROWS, 1)
            g_ = M.generate(input_ids=xb, attention_mask=torch.ones_like(xb), **dict(KW, max_new_tokens=1))
            counts.update(int(t) for t in g_[:, -1].tolist())
        N = G3_CALLS * G3_ROWS
        stray = {t: c for t, c in counts.items() if ptr.get(t, 0.0) == 0.0}
        z = {t: (counts.get(t, 0) / N - ptr[t]) / math.sqrt(ptr[t] * (1 - ptr[t]) / N) for t in kept}
        tv = 0.5 * sum(abs(counts.get(t, 0) / N - ptr.get(t, 0.0)) for t in set(kept) | set(counts))
        return {'pass': not stray and max(abs(v) for v in z.values()) <= 5.0 and abs(outside) < 1e-9 and 1 < len(kept) < C['inputs']['generation_explicit_B']['top_k'],
                'N': N, 'kept': len(kept), 'a_rank': designed.index(a_id), 'p_a_transformed': ptr[a_id], 'freq_a': counts.get(a_id, 0) / N, 'max_abs_z': max(abs(v) for v in z.values()),
                'tv': tv, 'stray': stray, 'mass_outside_designed': outside, 'cum_at_cut': [float(cum[len(kept) - 2]), float(cum[len(kept) - 1])]}
    check('G3_transformed_vs_sampling_frequency', G3)

    def G4():
        saved = list(M.generation_config.eos_token_id)
        out = {}
        eb, rev = stageB_model_eos()
        cases = [('without_turn_end', [t for t in saved if t != tok.convert_tokens_to_ids(BB.TURN_END)])]
        if eb is not None:
            cases.append(('stageB_model_config', eb))
        try:
            for name, e in cases:
                M.generation_config.eos_token_id = e
                out[name] = {'eos': e, 'error': expect_error(lambda: BB.chain_for_readout(M, prompt, C, tok, None), P.ToolError)}
        finally:
            M.generation_config.eos_token_id = saved
        restored = list(M.generation_config.eos_token_id) == saved
        return {'pass': all(v['error'] is not None for v in out.values()) and restored and eb is not None, 'cases': out, 'stageB_snapshot': rev, 'restored': restored}
    check('G4_foreign_stop_tokens_stop', G4)

    def G5():
        with BB.Capture(M, abort=True) as cap:
            M.generate(input_ids=x, attention_mask=torch.ones_like(x), **{kk: vv for kk, vv in KW.items() if kk != 'top_k'})
        s = BB.summarize(cap.calls[0], tok, list(KW))
        err = expect_error(lambda: BB.check_resolved(s, C, tok, ver), P.ToolError)
        return {'pass': err is not None and s['fixed']['values']['top_k'] != KW['top_k'], 'resolved_top_k': s['fixed']['values']['top_k'], 'error': err}
    check('G5_forgotten_top_k_stops', G5)

    def G6():
        e = expect_error(lambda: _raise_inside(M, x))
        left = [n for n in BB.WRAPPED if n in vars(M)]
        again = expect_error(lambda: BB.chain_for_readout(M, prompt, C, tok, st['s']['fixed']))
        bad_row = copy.deepcopy(st['s']['fixed'])
        bad_row['values']['temperature'] = 0.8
        e2 = expect_error(lambda: BB.chain_for_readout(M, prompt, C, tok, bad_row), P.ToolError)
        left2 = [n for n in BB.WRAPPED if n in vars(M)]
        return {'pass': e is not None and not left and again is None and e2 is not None and not left2, 'exception_inside': e, 'left_after_exception': left, 'row_c_equal_ok': again is None,
                'row_c_mismatch_stops': e2, 'left_after_all': left2}
    check('G6_wrappers_removed_and_row_c_match', G6)
    RES['G_hooks_clean'] = hooks_clean(M, base)
    del R, M
    gc.collect()


def _raise_inside(M, x):
    with BB.Capture(M):
        M.generate(input_ids=x, attention_mask=torch.ones_like(x), not_a_generation_key=1, **dict(KW, max_new_tokens=1))


def main():
    t0 = time.time()
    assert transformers.__version__ == C['inputs']['versions']['transformers'], ('transformers の版が固定の版でない（PYTHONPATH に pylib を置く）', transformers.__version__)
    tok = AutoTokenizer.from_pretrained(HF)
    group_L(tok)
    group_SPM(tok)
    group_G(tok)
    allpass = all(v.get('pass') for v in RES.values())
    cfg = json.load(open(os.path.join(HF, 'config.json'), encoding='utf-8'))['text_config']
    meta = {'version': {'dry_bprime': VERSION, 'bprime_run': BR.VERSION, 'bprime_directions': BD.VERSION, 'bprime_behavior': BB.VERSION, 'bprime_gemma': G.VERSION, 'bprime_core': P.VERSION},
            'transformers': transformers.__version__, 'torch': torch.__version__, 'numpy': np.__version__,
            'contract_sha16': hashlib.sha256(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16],
            'config_sha16': hashlib.sha256(open(os.path.join(HF, 'config.json'), 'rb').read()).hexdigest().upper()[:16], 'n_layers_tiny': N_TINY, 'window_tiny': WINDOW,
            'real_full_attention_layers': [i for i, t in enumerate(cfg['layer_types']) if t == 'full_attention'], 'sampling_kwargs': KW, 'seconds': round(time.time() - t0, 1)}
    out = {'meta': meta, 'tests': RES, 'all_pass': allpass}
    for v in RES.values():
        v.pop('trace', None) if v.get('pass') else None
    json.dump(out, open(os.path.join(HERE, 'dry-bprime-2026-09-30.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1, default=str)
    L = ['# B′ の器の合成データの確かめ（機械生成・`dry_bprime.py` %s・小さな乱数の Gemma 4・手元の CPU）' % VERSION, '',
         '- 版: transformers %s・torch %s・numpy %s・正本の SHA16 %s・設定の SHA16 %s（小さな模型は大きさだけ縮め、層 %d・窓 %d）。器の版: %s。' % (
             meta['transformers'], meta['torch'], meta['numpy'], meta['contract_sha16'], meta['config_sha16'], N_TINY, WINDOW, '・'.join('%s %s' % kv for kv in meta['version'].items())),
         '- 標本化の鍵（正本の段階 B の値の写し）: %s。' % '・'.join('%s %s' % kv for kv in KW.items()), '',
         '| 確かめ | 通ったか | 値 |', '|---|---|---|']
    for name, v in RES.items():
        vals = '・'.join('%s %s' % (a, ('%.4g' % b) if isinstance(b, float) else json.dumps(b, ensure_ascii=False, default=str)) for a, b in v.items() if a not in ('pass', 'trace'))
        L.append('| %s | %s | %s |' % (name, '通った' if v.get('pass') else '**落ちた**', vals.replace('|', '\\|').replace(NL, ' ')))
    L += ['', '- すべて通ったか: %s（%d 項目・%.0f 秒）' % ('はい' if allpass else '**いいえ**', len(RES), meta['seconds']), '',
          '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(os.path.join(HERE, 'dry-bprime-2026-09-30.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('ALL PASS' if allpass else 'SOME FAILED: ' + ', '.join(n for n, v in RES.items() if not v.get('pass')))


if __name__ == '__main__':
    main()
