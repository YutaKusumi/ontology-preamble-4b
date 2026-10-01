# -*- coding: utf-8 -*-
"""bprime_phases.py v0.2（2026-09-30・B′ の相ごとの計算の手順・起動器 `colab/boot_bprime.py` が呼ぶ・模型は呼ぶ側が読む・コーディネータ南無弥勒如来）。

相ごとの関数（正本 `stage_order`・`computation`・`directions`・`behavior_pilot`・`pilot`・`independent_recompute` のとおり・値を読まない）:
  - `check_items`（凍結の前の確かめ・正本 `computation.before_seal`・`computation.pre_freeze_checks`）: 意味のない列だけで順伝播と生成の煙試験をする。場面・腕・指示・書き出しを含む入力は
    トークナイザだけで確かめ、模型に通さない。戻り値は露出の記録（`computation.before_seal.may_print` の値だけ・合否と数と SHA と時間）。
  - `extract`（相 extract）: 抽出の文脈（八腕 × 二場面）の主位置と、主の升目の帯の八つの位置の、選んだ層の出力（選んだ層より後を流さない）→ 方向の組（g との一致）→ 係数 → npz →
    抽出の記録（転記行 D の元）。効き目は一つも計算しない。
  - `behavior`（行動の下見）: 升目ごとに生成 → 復号 → 凍結の採点 → 書き出しの根の件数 → 升目の集計（`bprime_behavior`）。
  - `pilot`（読み取りの下見）: 出口の値の自己検査 → (vi) → (i)(ii)(iv) → (iii) → 決め（`bprime_run.run_pilot`）。(iii) の処理の並びは `generate` から取り、転記行 C の要約と照らす。
  - `main_part`（本の計算の組）: main（`bprime_run.run_main_phase`）・recompute（独立の再計算の一段目の本の器のフックの道）・pathdiff（道の違いの記述・本の計算がバッチ一のときだけ）。
    残差の書き換えの道と独立の再抽出の道は、書き手と別の個体が書く器（`bprime_recompute_rewrite`・`bprime_reextract`）を起動器が呼ぶ（この器には置かない）。
印字の決まり: この器は値を印字しない（log には段の名と時間と数だけを渡す）。値は戻り値の記録に置き、起動器が置き場に書く。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, time, math, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import bprime_gemma as G
import bprime_core as P
import bprime_run as BR
import bprime_directions as BD
import bprime_behavior as BB
import bprime_cells as BC
import bl3_core as K

VERSION = 'v0.2'        # v0.2（2026-09-30・器の実装の検分の後）: 書き出しの根の件数に升目の選択の字を渡す（U22・R1-12）・抽出の記録の確かめのうちノルムと次元を値から計算する（前は定数の真・U27・R2-17）。前の版は `prev/bprime_phases-v0.1.py`／v0.1（2026-09-30）: 凍結の前の確かめの台帳の作り直しの照らしで、腕の置き場の名を照らさない（K18・Colab の DRY で見つけた）。前の版は `prev/bprime_phases-v0.py`
ToolError = P.ToolError
BINS = (0.0, 1.0, 4.0, 16.0, float('inf'))            # 出口の値の大きさの区間（|z|・凍結の前の確かめの印字）


def _t():
    return time.time()


def set_ids_of(C, L, fam):
    heads = L['heads']
    return [int(heads[x]['next']) for x in C['readout']['primary']['letters'][fam]] + [int(heads['refuse']['next'])]


def meaningless_cells(C, L, seqs):
    """意味のない列を升目の形にする（読み取りの位置は列の最後・読み取りの集合は nuclear の族の集合〔選択の文字四つと refuse の頭〕）。"""
    sids = set_ids_of(C, L, 'nuclear')
    return [BR.Cell('meaningless|' + n, 'X', 'X', 'X', ids, [], sids, len(ids) - 1) for n, ids in seqs.items()], sids


def bin_stats(d_on, zs, d_off, d_dbl):
    """区間ごとの行の数・「あり」と出口の差の最大・「なし」「二重」との差の最小（正本 `computation.before_seal.may_print`）。"""
    a = np.abs(np.asarray(zs, dtype=np.float64))
    out = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        m = (a >= lo) & (a < hi)
        n = int(m.sum())
        out.append({'bin': [lo, None if math.isinf(hi) else hi], 'rows': n, 'on_max': float(np.max(d_on[m])) if n else None,
                    'off_min': float(np.min(d_off[m])) if n else None, 'dbl_min': float(np.min(d_dbl[m])) if n else None})
    return out


# ---------------- 凍結の前の確かめ ----------------
def check_items(model, tok, C, L, MQ, stageB_npz, reextract=None, gen_max_new=256, log=None):
    """凍結の前の確かめ（正本 `computation.pre_freeze_checks`）。MQ: 意味のない列の記録（`bprime_meaningless` の出力）。stageB_npz: 段階 B の凍結の活性（係数の確かめ）。
    reextract: 独立の再抽出の道の関数（別の個体の器・None なら落とした項目として記録する）。戻り値: 露出の記録（印字してよい値だけ）。"""
    import torch
    import bprime_facts as BF
    import bprime_meaningless as BM
    import blens_core as CB
    log = log or (lambda s: None)
    rec = collections.OrderedDict(version=VERSION, items=collections.OrderedDict())
    k_layer = int(C['layers']['index'])
    dev = next(model.parameters()).device

    def item(name, fn):
        t0 = _t()
        try:
            out = dict(fn())
        except Exception as e:                           # 項目の落ちは記録して続ける（凍結しない・登録者に上げる）
            out = {'pass': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:300])}
        out['sec'] = round(_t() - t0, 2)
        rec['items'][name] = out
        log('[bprime_phases] 確かめ %s %s（%.1f 秒）' % (name, '通った' if out.get('pass') else '落ちた', out['sec']))
        return out

    ids = BC.ids_for(tok)

    def ledger():
        Lb = BC.build(tok)
        keys = ['prefix_text', 'prefix_ids', 'prefix_pieces', 'heads', 'cells_main', 'extract_contexts', 'arms']
        # 腕の「置き場」は照らさない（v0.1・K18）: 凍結の段階 B の走行器は arms/ の木を歩いて SHA16 の合う最初のファイルを選ぶので、同じ本文のファイルが二か所にある腕
        # （O・Osec・Nk）は、木を歩く順（Windows と Linux で違う）で置き場の名が変わる。本文の SHA16 とトークンの数は照らす
        strip = lambda k, v: ({a: {kk: vv for kk, vv in d.items() if kk != 'path'} for a, d in v.items()} if k == 'arms' else v)
        bad = [k for k in keys if json.dumps(strip(k, Lb[k]), sort_keys=True, ensure_ascii=False) != json.dumps(strip(k, L[k]), sort_keys=True, ensure_ascii=False)]
        paths_differ = sorted(a for a in L['arms'] if (Lb['arms'].get(a) or {}).get('path') != L['arms'][a].get('path'))
        return {'pass': not bad, 'differs': bad, 'arm_paths_differ': paths_differ}
    item('ledger_rebuild', ledger)

    def tokenizer_only():
        A = BF.row_A(tok, C, L, ids)
        bos = [sum(1 for t in ids['main'][k]['prompt'] if t == int(tok.bos_token_id)) for k in ids['main']]
        return {'pass': all(b == 1 for b in bos) and ids['main'][next(iter(ids['main']))]['prompt'][0] == int(tok.bos_token_id), 'variants_kept': A['variants_kept'],
                'v3_checks': A['v3_checks'], 'bos_per_prompt': sorted(set(bos))}
    item('tokenizer_only', tokenizer_only)

    def meaningless():
        seqs, meta = BM.build(tok, C, L)
        return {'pass': BM.ids_sha16([x for v in seqs.values() for x in v]) == MQ['all_sha16'], 'n': len(seqs), 'lengths': meta['lengths']}
    item('meaningless_rebuild', meaningless)
    seqs = collections.OrderedDict((k, list(v)) for k, v in MQ['sequences'].items())
    cells_m, sids = meaningless_cells(C, L, seqs)

    def model_facts():
        tc = G.text_cfg(model)
        mf = C['inputs']['model_facts']
        got = {'num_hidden_layers': int(tc.num_hidden_layers), 'hidden_size': int(tc.hidden_size), 'vocab_size': int(tc.vocab_size), 'final_logit_softcapping': float(tc.final_logit_softcapping),
               'sliding_window': int(tc.sliding_window), 'layer_type': tc.layer_types[k_layer], 'n_decoder_layers': len(G.decoder_layers(model)),
               'lm_head_rows': int(model.lm_head.weight.shape[0])}
        ok = (got['num_hidden_layers'] == mf['num_hidden_layers'] == got['n_decoder_layers'] and got['hidden_size'] == mf['hidden_size'] and got['vocab_size'] == mf['vocab_size'] == got['lm_head_rows']
              and got['final_logit_softcapping'] == mf['final_logit_softcapping'] and getattr(model.config, 'final_logit_softcapping', None) is None
              and got['sliding_window'] == mf['sliding_window'] and got['layer_type'] == C['layers']['layer_type'] and G.layer_index(C['layers']['ratio'], got['num_hidden_layers']) == k_layer)
        return dict(got, **{'pass': ok, 'layer_index': k_layer, 'layer_path': C['layers']['layer_path']})
    item('model_facts', model_facts)
    R = BR.Runner(model, C, k_layer, 1.0, {})

    def norm_form():
        cap = {}
        fn = G.final_norm(model)
        h1 = fn.register_forward_pre_hook(lambda m, a: cap.__setitem__('in', a[0][:, -1, :].detach().clone()))
        h2 = fn.register_forward_hook(lambda m, a, o: cap.__setitem__('out', o[:, -1, :].detach().clone()))
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([cells_m[0].ids], device=dev), use_cache=False, logits_to_keep=1)
        finally:
            h1.remove(); h2.remove()
        x = cap['in'].float()
        w = fn.weight.detach().float()
        base = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + R.eps)
        y = cap['out'].float()
        d_w = float((y - base * w).abs().max())
        d_1w = float((y - base * (1.0 + w)).abs().max())
        return {'pass': d_w < d_1w and d_w <= 0.02 * float(y.abs().max())}                      # 値は印字しない（活性に当たる）
    item('rmsnorm_not_one_plus_weight', norm_form)

    def alignment():
        cap = {}
        n = G.n_layers(model)
        hk = G.decoder_layers(model)[k_layer].register_forward_hook(lambda m, a, o: cap.__setitem__('k', (o[0] if isinstance(o, tuple) else o).detach().clone()))
        hl = G.decoder_layers(model)[n - 1].register_forward_hook(lambda m, a, o: cap.__setitem__('last', (o[0] if isinstance(o, tuple) else o).detach().clone()))
        try:
            with torch.no_grad():
                o = model(input_ids=torch.tensor([cells_m[0].ids], device=dev), output_hidden_states=True, use_cache=False, logits_to_keep=1)
        finally:
            hk.remove(); hl.remove()
        sel = bool(torch.equal(o.hidden_states[k_layer + 1], cap['k']))
        last = bool(torch.equal(o.hidden_states[n], cap['last']))
        return {'pass': sel and not last, 'selected_equal': sel, 'last_equal': last}
    item('layer_alignment', alignment)

    st = {}

    def measure():
        L_ = C['computation']['self_checks']['logit']
        mk = BR.measure_k(R, seqs, sids, L_['measure']['batches'])
        d_on, zs, d_off, d_dbl = R.measure_positions(seqs, sids, 1, wrong=True)
        st['mk'] = mk
        return {'pass': True, 'k': mk['k'], 'z0': mk['z0'], 'k_by_batch': {str(b): v for b, v in mk['k_by_batch'].items()}, 'big_rows': mk['big_rows'], 'fallback': mk['fallback'],
                'n_rows': mk['n_rows'], 'bins_batch1': bin_stats(d_on, zs, d_off, d_dbl)}
    item('logit_tolerance_k', measure)
    mk = st.get('mk')

    def bugs():
        if mk is None:
            raise ToolError('k が無い（前の項目が落ちた）')
        out = {}
        for bug in (None, 'double_norm', 'no_softcap'):
            Rx = R if bug is None else BR.Runner(model, C, k_layer, 1.0, {}, bug=bug)
            states = [Rx.logit_check(c, mk['k'], mk['z0'])['state'] for c in cells_m]
            out[bug or 'correct'] = dict(collections.Counter(states))
        ok = out['correct'].get('否', 0) == 0 and all(out[b].get('否', 0) >= 1 and out[b].get('合', 0) == 0 for b in ('double_norm', 'no_softcap'))
        return {'pass': ok, 'states': out}
    item('bugs_caught', bugs)

    def no_hidden_states():
        cfg = G.text_cfg(model)
        old = getattr(cfg, 'output_hidden_states', False)
        cfg.output_hidden_states = True
        try:
            err = None
            try:
                R.forward(cells_m[0], [K.NOOP], +1, full=False)
            except ToolError as e:
                err = str(e)
        finally:
            cfg.output_hidden_states = old
        return {'pass': err is not None}
    item('no_output_hidden_states_in_add', no_hidden_states)

    def hook_order():
        """集めるフック（transformers が層に掛けたもの）が加減のフックより先か後かで、読み取りと層ごとの取り出しの値が変わらない（R37）。"""
        import run_stageB_local as RB
        c = cells_m[0]
        with torch.no_grad():
            o = model(input_ids=torch.tensor([c.ids], device=dev), output_hidden_states=True, use_cache=False, logits_to_keep=1)
        v = np.random.default_rng(int(C['computation']['before_seal']['meaningless']['seed'])).standard_normal(R.dim)
        v = (v / np.linalg.norm(v) * 0.1 * float(o.hidden_states[k_layer + 1][0, c.mp].float().norm())).astype(np.float32)
        layer = G.decoder_layers(model)[k_layer]

        def run(order):
            cap = {}
            hs = [G.final_norm(model).register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))]
            for j in R.after:
                hs.append(G.decoder_layers(model)[j].register_forward_hook(lambda m, a, oo, j=j: cap.__setitem__(j, (oo[0] if isinstance(oo, tuple) else oo)[:, -1, :].detach().clone())))
            h_add = G.register_hook(model, k_layer, RB.make_hook(v[None, :], 1.0, +1, [c.mp], meta={'bprime': 'hook_order'}))
            foreign = [hid for hid, fn_ in layer._forward_hooks.items() if not hasattr(fn_, 'op4b')]
            if order == 'foreign_after':
                for hid in foreign:
                    layer._forward_hooks.move_to_end(hid)
            try:
                with torch.no_grad():
                    model(input_ids=torch.tensor([c.ids], device=dev), use_cache=False, logits_to_keep=1)
            finally:
                h_add.remove()
                for h_ in hs:
                    h_.remove()
                G.assert_no_hooks(model, k_layer)
            return cap, len(foreign)
        a, nf = run('foreign_before')
        b, _ = run('foreign_after')
        same = all(torch.equal(a[x], b[x]) for x in a)
        return {'pass': same and nf >= 1, 'foreign_hooks_on_layer': nf}
    item('collecting_hook_order', hook_order)

    def determinism_speed():
        c = cells_m[0]
        r1 = R.forward(c, [K.NOOP], +1, want_model_logits=True, full=False)
        r2 = R.forward(c, [K.NOOP], +1, want_model_logits=True, full=False)
        same = bool(torch.equal(r1['model_logits'], r2['model_logits']))
        sp = {}
        for b in (1, int(C['readout']['primary']['batch'])):
            ts = []
            for _ in range(3):
                if dev.type == 'cuda':
                    torch.cuda.synchronize()
                t0 = _t()
                R.forward(c, [K.NOOP] * b, +1, full=True)
                if dev.type == 'cuda':
                    torch.cuda.synchronize()
                ts.append(_t() - t0)
            sp[str(b)] = round(float(np.median(ts)), 4)
        return {'pass': same, 'batch1_repeat_bitwise_equal': same, 'sec_median_by_batch': sp, 'seq_len': len(c.ids)}
    item('determinism_and_speed', determinism_speed)

    def memory():
        if dev.type != 'cuda':
            return {'pass': True, 'skipped': 'cpu'}
        c = cells_m[-1]
        b = int(C['readout']['primary']['batch'])
        torch.cuda.reset_peak_memory_stats()
        peaks = []
        for i in range(30):
            R.forward(c, [K.NOOP] * b, +1, want_layers=True, full=True)
            if i in (4, 29):
                torch.cuda.synchronize()
                peaks.append(torch.cuda.max_memory_allocated() / 2 ** 30)
        return {'pass': peaks[1] <= peaks[0] * 1.001 + 0.01, 'peak_gib_after_5': round(peaks[0], 3), 'peak_gib_after_30': round(peaks[1], 3)}
    item('memory_not_growing', memory)

    def generation_smoke():
        pre, post = BM.template(tok)
        texts, strings = BM.source_texts(C, L)
        vocab, _ = BM.pool(tok, texts, strings)
        rng = np.random.default_rng(int(C['computation']['before_seal']['meaningless']['seed']) + 1)
        chunk = [int(vocab[i]) for i in rng.integers(0, len(vocab), size=64)]
        prompt = list(pre) + chunk + list(post)
        bos_ok = sum(1 for t in prompt if t == int(tok.bos_token_id)) == 1 and prompt[0] == int(tok.bos_token_id)
        _, summ = BB.chain_for_readout(model, prompt, C, tok, None)
        kw = dict(BB.sampling_kwargs(C), max_new_tokens=int(gen_max_new))
        eos = set(int(x) for x in C['behavior_pilot']['sampling']['eos_token_id'])
        think = tok.convert_tokens_to_ids('<|channel>')
        runs = []
        for s in (1, 2):
            x = torch.tensor([prompt], device=dev)
            torch.manual_seed(s)
            t0 = _t()
            out = model.generate(input_ids=x, attention_mask=torch.ones_like(x), **kw)
            sec = _t() - t0
            ids_, finish, stop = BB.cut_response(out[0].tolist(), prompt, eos, kw['max_new_tokens'])
            runs.append({'finish': finish, 'stop_token': stop, 'n_tokens': len(ids_), 'think_token': bool(think in ids_), 'sec': round(sec, 2),
                         'tok_per_sec': round(len(ids_) / sec, 2) if sec > 0 else None, 'sha16': BR.ids_sha16(ids_)})
        differ = runs[0]['sha16'] != runs[1]['sha16']
        return {'pass': bos_ok and differ and all(r['finish'] in ('stop', 'length') for r in runs), 'bos_one': bos_ok, 'sampling_differs': differ,
                'runs': [{k_: v_ for k_, v_ in r.items() if k_ != 'sha16'} for r in runs], 'resolved': summ['fixed'], 'max_new_tokens_smoke': int(gen_max_new)}
    item('generation_smoke', generation_smoke)

    def extraction_stop():
        ctx = collections.OrderedDict(('m%d' % i, list(v)) for i, v in enumerate(list(seqs.values())[:2]))
        BD.activations(model, ctx, k_layer)
        return {'pass': True}
    item('extraction_stops_at_layer', extraction_stop)

    def reextract_path():
        if reextract is None:
            return {'pass': False, 'error': '独立の再抽出の道の器が無い'}
        ctx = collections.OrderedDict(('m%d' % i, list(v)) for i, v in enumerate(list(seqs.values())[:4]))
        a, na, _ = BD.activations(model, ctx, k_layer)
        b = reextract(model, ctx, k_layer)
        RX = C['independent_recompute']['reextract']
        rel = max(abs(float(np.linalg.norm(b[k_])) - na[k_]) / na[k_] for k_ in ctx)
        cos = min(float(np.dot(a[k_], b[k_]) / (np.linalg.norm(a[k_]) * np.linalg.norm(b[k_]))) for k_ in ctx)
        return {'pass': rel <= RX['rel_tol'] and cos >= RX['cos_min']}
    item('reextract_path', reextract_path)

    def coefficient():
        cc = BD.coefficient_checks(stageB_npz, C)
        return {'pass': cc['check_bl3_pass'] and cc['check_B_record_pass'], 'qwen_ratio': cc['bl3_ratio'], 'coef_on_bl3': cc['coef_on_bl3'], 'rel_h': cc['rel_h'], 'rel_v': cc['rel_v']}
    item('coefficient_on_bl3', coefficient)

    def g_check():
        d = int(G.text_cfg(model).hidden_size)
        I = C['nulls']['isotropic']
        g = BD.iso_g(I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'], d)
        v = np.random.default_rng(int(I['seed']) + 7).standard_normal(d)
        iso = np.asarray(CB.iso_directions(v, int(I['seed']), float(C['layers']['ratio']), int(I['count']), int(I['layer_key_scale'])), dtype=np.float64)
        chk = BD.check_iso_against_g(iso, g, float(np.linalg.norm(v)), I['g_rel_tol'])
        return {'pass': chk['pass'], 'rel_max': chk['rel_max'], 'g': BD.g_record(g, I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'])}
    item('isotropic_g', g_check)
    rec['n_forward'] = R.n_forward
    rec['all_pass'] = all(v.get('pass') for v in rec['items'].values())
    return rec


# ---------------- 相 extract ----------------
def extract(model, tok, C, L, g_sha256, stageB_npz, stageB_qwen_acts=None, log=None):
    """相 extract（正本 `directions`・`nulls`・`coefficient`・`transcription_rows.D`）。g_sha256: 下見の前の凍結で記録した g の SHA-256（引き直した g と照らす）。
    戻り値: (npz のバイト, 抽出の記録)。効き目は一つも計算しない（選んだ層の出力だけを取る）。"""
    import torch
    log = log or (lambda s: None)
    k_layer = int(C['layers']['index'])
    ids = BC.ids_for(tok)
    for key, v in ids['extract'].items():
        if BR.ids_sha16(v) != L['extract_contexts'][key]['ids_sha16']:
            raise ToolError('抽出の文脈の並びが台帳と違う: %s' % key)
    t0 = _t()
    acts, norms, _ = BD.activations(model, ids['extract'], k_layer)
    band_ctx, band_pos = collections.OrderedDict(), collections.OrderedDict()
    for key, d in ids['main'].items():
        seq = list(d['prompt']) + list(d['prefix'])
        if BR.ids_sha16(seq) != L['cells_main'][key]['ids_sha16']:
            raise ToolError('主の升目の並びが台帳と違う: %s' % key)
        band_ctx[key] = seq
        band_pos[key] = list(range(len(d['prompt']) - 1, len(seq)))
    _, _, band = BD.activations(model, band_ctx, k_layer, positions=band_pos)
    log('[bprime_phases] 抽出 %d 文脈と帯 %d 升目（%.0f 秒）' % (len(acts), len(band), _t() - t0))
    I = C['nulls']['isotropic']
    d = int(next(iter(acts.values())).shape[0])
    g = BD.iso_g(I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'], d)
    g_rec = BD.g_record(g, I['seed'], C['layers']['ratio'], I['count'], I['layer_key_scale'])
    if g_rec['g_sha256'] != g_sha256:
        raise ToolError('引き直した g の SHA-256 が下見の前の凍結の値と違う')
    arrays, names, meta = BD.build(acts, C, g=g)
    npz = BD.npz_bytes(arrays)
    cc = BD.coefficient_checks(stageB_npz, C)
    h_mean = BD.h_norm_mean(norms)
    coef = BD.coefficient(cc['bl3_ratio'], meta['vhat_norm'], h_mean)
    D = row_D_values(C, acts, norms, band, arrays, names, meta, coef, stageB_qwen_acts, ids)
    rec = collections.OrderedDict([
        ('kind', 'bprime_extraction_record'), ('version', VERSION), ('layer_index', k_layer), ('npz_sha256', hashlib.sha256(npz).hexdigest().upper()),
        ('groups', {'named': {'names': names['named']}, 'iso': {'count': len(names['iso'])}, 'real': {'names': names['real']}, 'check': {'count': 1}}),
        ('group_sha256', meta['sha256']), ('coefficient', coef), ('bl3_ratio', cc['bl3_ratio']), ('h_norm_mean', h_mean), ('vhat_norm', meta['vhat_norm']),
        ('g', g_rec), ('g_match', meta['iso_check']),
        ('checks', {'g_match': bool(meta['iso_check']['pass']),
                    'norms_finite_nonzero': bool(all(np.isfinite(float(v)) and float(v) > 0 for v in norms.values())),                    # 文脈ごとの ‖h‖（v0.2・U27）
                    'dim_match': bool(d == int(G.text_cfg(model).hidden_size) and all(np.asarray(a).shape[-1] == d for a in arrays.values())),   # 活性と方向の次元が模型の次元（v0.2・U27）
                    'no_readout': True,                                                                                            # 作りの上の性質（この相は選んだ層の出力だけを取り、読み取りの値を作らない・U27 の注）
                    'coefficient_checks': bool(cc['check_bl3_pass'] and cc['check_B_record_pass'])}),
        ('checks_note', 'no_readout は作りの上の性質（相 extract は選んだ層の出力だけを取り、読み取りの値を作らない）で、値から計算した確かめではない'),
        ('row_D', D)])
    return npz, rec


def row_D_values(C, acts, norms, band, arrays, names, meta, coef, qwen_acts, ids):
    """転記行 D の値（正本 `transcription_rows.D`・草案9 の転記行 D の記述の決め）。数（上位の次元の数・実効の押しの比を見る方向）は正本 `transcription_rows.counts`。"""
    import torch
    cnt = C['transcription_rows'].get('counts')
    if not cnt:
        raise ToolError('正本 `transcription_rows.counts`（上位の次元の数・実効の押しの比を見る方向）が無い')
    top = int(cnt['top_dims'])
    H = np.array(list(acts.values()), dtype=np.float64)
    mean = H.mean(axis=0)
    spread = float(np.sqrt(np.mean(np.sum((H - mean) ** 2, axis=1))))

    def top_share(h):
        s = np.sort(np.asarray(h, dtype=np.float64) ** 2)[::-1]
        return float(s[:top].sum() / s.sum())
    vn = float(meta['vhat_norm'])
    band_rows = collections.OrderedDict()
    for key, B in band.items():
        nrm = [float(np.linalg.norm(x)) for x in B]
        band_rows[key] = {'h_norm': nrm, 'push_ratio': [coef * vn / x for x in nrm]}
    pick = []
    for grp, n in (('named', cnt['push_dirs']['named']), ('real', cnt['push_dirs']['real']), ('iso', cnt['push_dirs']['iso'])):
        pick += [(grp, i) for i in range(min(int(n), len(arrays[grp])))]
    ratios = []
    for key, B in band.items():
        hb = torch.tensor(np.asarray(B), dtype=torch.bfloat16)
        for grp, i in pick:
            v = np.asarray(arrays[grp][i], dtype=np.float64)
            add = float(coef) * torch.as_tensor(v.astype(np.float32), dtype=torch.bfloat16)
            eff = (hb + add).float() - hb.float()
            ratios += [float(eff[p].norm()) / (float(coef) * float(np.linalg.norm(v))) for p in range(hb.shape[0])]
    r = np.array(ratios)
    qs = [0.0, 0.05, 0.5, 0.95, 1.0]
    real_pairs = collections.OrderedDict()
    for pn, nat in meta['natural_norms_real'].items():
        a, b = pn.split('~')
        dl = [len(ids['extract']['%s|%s' % (sc, a)]) - len(ids['extract']['%s|%s' % (sc, b)]) for sc in BD.EXTRACT_SCENES]
        real_pairs[pn] = {'len_diff': dl, 'natural_norm': nat}
    unit = lambda X: X / np.linalg.norm(X, axis=-1, keepdims=True)
    out = collections.OrderedDict([
        ('h_norm_by_context', dict(norms)), ('vhat_norm', vn), ('vhat_over_h', {k: vn / v for k, v in norms.items()}), ('coefficient', coef),
        ('group_sha256', meta['sha256']), ('check_cos_max', meta['check_cos_max']),
        ('band', band_rows), ('context_spread_rms', spread),
        ('top_dims', top), ('top_dims_share', {k: top_share(v) for k, v in acts.items()}),
        ('push_dirs', {'named': cnt['push_dirs']['named'], 'real': cnt['push_dirs']['real'], 'iso': cnt['push_dirs']['iso'], 'n': len(pick)}),
        ('effective_push_ratio_quantiles', {str(q): float(np.quantile(r, q)) for q in qs}), ('effective_push_ratio_n', int(r.size)),
        ('real_pairs', real_pairs),
        ('natural_norms_named', meta['natural_norms_named']),
    ])
    if qwen_acts is not None:
        out['qwen_top_dims_share'] = {k: top_share(v) for k, v in qwen_acts.items()}
    return out


# ---------------- 行動の下見 ----------------
def behavior(model, tok, C, L, batch, log=None):
    """行動の下見の生成と採点（正本 `behavior_pilot`）。戻り値: {'trials','scored','roots','summaries','fixed','calls','digests'}。値は印字しない。"""
    log = log or (lambda s: None)
    ids = BC.ids_for(tok)
    env = BB.scorer_env()
    strings = P.variant_strings(L['prefix_text'])
    window = C['behavior_pilot']['root_counts']['b']['window_chars']
    trials, scored, roots, summaries, calls = (collections.OrderedDict() for _ in range(5))
    fixed = None
    for sc, arm in C['cells_main']:
        key = '%s|%s' % (sc, arm)
        prompt = ids['main'][key]['prompt']
        if BR.ids_sha16(list(prompt) + list(ids['main'][key]['prefix'])) != L['cells_main'][key]['ids_sha16']:
            raise ToolError('升目の並びが台帳と違う: %s' % key)
        g = BB.generate_cell(model, tok, C, key, prompt, batch, row_c_fixed=fixed, log=log)
        fixed = g['fixed']
        sent, fam = BB.sent_of(key)
        sids = [int(x) for x in L['cells_main'][key]['set_ids']]
        trials[key] = g['trials']
        scored[key] = [BB.score_trial(t, fam, sent, env) for t in g['trials']]
        roots[key] = [BB.root_counts_trial(t, prompt, sids, L['prefix_ids'], strings, window, env['parser_mod'], letters=L['cells_main'][key]['letters']) for t in g['trials']]
        summaries[key] = BB.cell_summary(C, key, g['trials'], scored[key], roots[key])
        calls[key] = g['calls']
    return {'trials': trials, 'scored': scored, 'roots': roots, 'summaries': summaries, 'fixed': fixed, 'calls': calls, 'digests': BB.closing_digests(trials, scored, env)}


# ---------------- 読み取りの下見 ----------------
def pilot(model, tok, C, L, facts_pre, closed, k, z0, log=None):
    """読み取りの下見（正本 `pilot`）。facts_pre: 凍結の前の転記行（揺れの版の割り方）。closed: 行動の下見の閉じた記録（升目の集計・解決された設定の要約・器の誤りの印）。"""
    log = log or (lambda s: None)
    k_layer = int(C['layers']['index'])
    keys = ['%s|%s' % (sc, arm) for sc, arm in C['cells_main']]
    cells = BR.build_cells(tok, C, L, keys)
    variants = collections.OrderedDict((n, v['ids']) for n, v in facts_pre['facts']['A']['variants'].items() if v['keep'])
    behavior_state = BB.iii_status(C, closed.get('summaries') or {}, tool_error=bool(closed.get('tool_error')))
    procs, summ = BB.chain_for_readout(model, cells[keys[0]].ids, C, tok, closed.get('fixed'))
    R = BR.Runner(model, C, k_layer, 1.0, {})
    t0 = _t()
    rec = BR.run_pilot(R, [cells[k_] for k_ in keys], C, variants, behavior_state, procs, k, z0)
    rec['behavior_state'] = {k_: v for k_, v in behavior_state.items() if k_ != 'rate'}
    rec['chain'] = summ['fixed']['processors']
    rec['variants_used'] = list(variants)
    log('[bprime_phases] 読み取りの下見（%.0f 秒・順伝播 %d）' % (_t() - t0, R.n_forward))
    return rec


# ---------------- 本の計算の組 ----------------
def main_part(part, model, C, cells, dirs, names, pilot_rec, k, z0, coef, rows_rc=None, log=None):
    """本の計算の組（正本 `computation`・`independent_recompute`・`descriptive.path_difference`）。値は印字しない。"""
    log = log or (lambda s: None)
    R = BR.Runner(model, C, int(C['layers']['index']), coef, dirs)
    if part == 'main':
        return BR.run_main_phase(R, C, cells, names, pilot_rec, k, z0, log=log)
    if part == 'pathdiff':
        if int(pilot_rec['batch']) != 1:
            raise ToolError('道の違いの記述は、本の計算がバッチ一に移ったときだけ走らせる')
        return BR.run_main_phase(R, C, cells, names, pilot_rec, k, z0, batch_override=int(C['readout']['primary']['batch']), log=log)
    if part == 'recompute':
        if not rows_rc:
            raise ToolError('独立の再計算の行が無い')
        rows, dbr = rows_rc
        return {'hook': BR.recompute_hook_path(R, rows, dbr, log=log), 'rows': [[n, c.key, s] for n, c, s in rows]}
    raise ToolError('組の名が決まりの外: %s' % part)
