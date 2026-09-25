# -*- coding: utf-8 -*-
"""bl3_run.py v3 —— B-lens 層三（Bl3）の教師強制の順伝播を走らせる器（2026-09-25・正本 `readout.primary`・`pilot`・`computation`・`descriptive`）。

走らせ方（正本のとおり・値は器の出力に置き、読みは付けない）:
  - 入力: 段階 B の組み立てのままのプロンプト（凍結の `steer_B.apply_chat`・`run_stageB_local.user_message`）の直後に、主の書き出し（設計事実の転記行 A の
    トークンの並び）を置く。主位置は凍結の `steer_B.main_position`、読み取りの位置は列の最後（主位置 ＋ 書き出しの長さ）。
  - 加減: 凍結の `run_stageB_local.make_hook`（行ごとの方向の行列を受ける形・層の出力の型に直して足す・係数は一度だけ）を、選んだ層（凍結の
    `direction_B.layer_index`）に凍結の `register_hook` で掛ける。帯は主位置から読み取りの位置まで。零のベクトルの行が無操作。
  - 近道: 主位置より前（添字 0〜主位置−1）の計算を加減なしで一度だけ作り、バッチの大きさに写して、主位置から後ろだけを流す（帯の起点は写した後の 0）。
    近道は下見の (v) の記述だけに使い、本の計算は近道を使わない（裁定 D234）。頭の近道の確かめ（正本 `computation.steered_cache_check`）は近道を使うときだけの確かめなので、関数を置かない。
  - 読み取り: 最終の正規化の入力（最後の層の出口の残差）を前の hook で取り、`float32` に上げて最終の正規化と語彙の行列の読み取りの集合の行を `float32` で当てる。
    全語彙の softmax は質量にだけ使う（`float32`）。層ごとの差分は、選んだ層の後の各層の出口の hook で取る（`hidden_states` は使わない）。
  - 自己検査: 出口の値（読み取りの集合の `float32` の出口の値と、模型そのものの出口の値〔bf16〕の差の最大・許容 `computation.logit_tol`）と、
    最後の層（層ごとの差分の最後の層の行と読み取りの効き目の差・許容 `computation.layer_tol`）。落ちたら止める（器の誤り・正本 `pilot.decision.tool_error`・
    `computation.tool_error`）。
関数は Colab の起動器 `tools/colab/boot_Bl3.py` と合成データの器 `tools/dry_run_Bl3.py` が import して呼ぶ（この器だけでは模型を読まない）。
DRY（乱数の小さな模型）の確かめのために、壊した読み取り（二重の正規化）と壊した近道（主位置まで使い回す）を、引数 `bug` で入れられる（本の計算では入れない）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, time, hashlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bl3_core as K

VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 出口の値が有限でなければ止める・方向の名の並びを正本と転記行 D に照らす・升目のトークンの並びの SHA16／v2（裁定 D231・D234）: 本の計算は近道を使わない ほか
BUGS = (None, 'double_norm', 'cache_through_mp')


class ToolError(Exception):
    """凍結した確かめが機械で落ちた（器の誤り・正本 `pilot.decision.tool_error.what`）。"""


def require_finite(vals, where):
    """出口の値がすべて有限であること（有限でなければ器の誤りで止める・裁定 D236）。vals: 名 → 値。"""
    bad = sorted(k for k, v in vals.items() if not math.isfinite(float(v)))
    if bad:
        raise ToolError('有限でない値（%s・%d 個・例 %s）' % (where, len(bad), bad[:3]))


def ids_sha16(cell):
    """升目の入力のトークンの並び（プロンプト ＋ 主の書き出し）の SHA16（相 check が書き、凍結の器が手元の組み立てと照らす・裁定 D236）。"""
    return hashlib.sha256(','.join(str(int(x)) for x in cell.ids).encode('ascii')).hexdigest().upper()[:16]


class Cell:
    """一つの升目（場面 × 土台の腕）の入力と位置。"""

    def __init__(self, key, sc, arm, fam, prompt_ids, prefix_ids, set_ids, main_position):
        self.key, self.sc, self.arm, self.fam = key, sc, arm, fam
        self.prompt = list(prompt_ids)
        self.ids = list(prompt_ids) + list(prefix_ids)
        self.mp = int(main_position)
        self.ro = len(self.ids) - 1
        self.set_ids = list(set_ids)            # 選択の文字（族の順・a が先頭）と refuse の頭
        if self.mp != len(self.prompt) - 1:
            raise ToolError('主位置がプロンプトの最後でない: %s' % key)

    def with_prefix(self, prefix_ids):
        return Cell(self.key, self.sc, self.arm, self.fam, self.prompt, prefix_ids, self.set_ids, self.mp)


class Runner:
    def __init__(self, model, T3, layer_idx, coef, dirs, bug=None):
        import torch
        import run_stageB_local as RB
        if bug not in BUGS:
            raise ValueError(bug)
        self.torch, self.RB, self.model, self.T3 = torch, RB, model, T3
        self.layer, self.coef, self.bug = int(layer_idx), float(coef), bug
        self.dev = next(model.parameters()).device
        self.eps = float(model.config.rms_norm_eps)
        self.n_layers = int(model.config.num_hidden_layers)
        self.after = list(range(self.layer + 1, self.n_layers))
        self.g32 = model.model.norm.weight.detach().float()
        self.W32 = model.lm_head.weight.detach().float()
        self.dirs = dirs                      # 方向の名 → float64 の一本（無操作と埋めは零）
        self.dim = int(self.g32.shape[0])
        self._zero = np.zeros(self.dim, dtype=np.float32)
        self.n_forward = 0

    # ---- 方向 ----
    def vec(self, did):
        if did in (K.NOOP, K.PAD):
            return self._zero
        v = self.dirs[did]
        return np.asarray(v, dtype=np.float32)

    # ---- 正規化と読み取り（float32） ----
    def norm32(self, h):
        h = h.float()
        return h * self.torch.rsqrt(h.pow(2).mean(-1, keepdim=True) + self.eps) * self.g32

    def readout(self, h, cell, full=True):
        hn = self.norm32(h)
        if self.bug == 'double_norm':
            hn = self.norm32(hn)
        Zs = (hn @ self.W32[cell.set_ids].T).double().cpu().numpy()
        out = {'Zset': Zs, 'lo': K.log_odds_a(Zs, 0, list(range(1, len(cell.set_ids)))), 'pa': K.prob_a_in_set(Zs, 0, list(range(len(cell.set_ids))))}
        if full:
            Zf = (hn @ self.W32.T).double()
            lse_f = self.torch.logsumexp(Zf, dim=-1)
            out['mass'] = self.torch.exp(self.torch.logsumexp(Zf[:, cell.set_ids], dim=-1) - lse_f).cpu().numpy()
            out['Zfull'] = Zf
        return out

    # ---- 近道の元（主位置より前・加減なし） ----
    def prefix_cache(self, cell):
        torch = self.torch
        end = cell.mp + 1 if self.bug == 'cache_through_mp' else cell.mp
        with torch.no_grad():
            out = self.model(input_ids=torch.tensor([cell.ids[:end]], device=self.dev), use_cache=True, logits_to_keep=1)
        self.n_forward += 1
        return {'legacy': out.past_key_values.to_legacy_cache(), 'end': end}

    def _expand(self, pc, B):
        from transformers.cache_utils import DynamicCache
        return DynamicCache.from_legacy_cache(tuple((k.expand(B, *k.shape[1:]).contiguous(), v.expand(B, *v.shape[1:]).contiguous()) for k, v in pc['legacy']))

    # ---- 一回の順伝播（行ごとの方向・同じ升目・同じ符号） ----
    def forward(self, cell, dir_ids, sign, pc=None, want_layers=False, want_model_logits=False, full=True):
        """pc（近道の元）があれば近道、無ければ近道なし。戻り値: 行ごとの対数オッズ・集合の中の a の確率・質量・（あれば）層ごとの残差と対数オッズ・模型の出口の値。"""
        torch, RB = self.torch, self.RB
        B = len(dir_ids)
        V = np.stack([self.vec(d) for d in dir_ids]).astype(np.float32)
        if pc is None:
            inp = torch.tensor([cell.ids] * B, device=self.dev)
            starts = [cell.mp] * B
            past = None
        else:
            if pc['end'] != cell.mp:        # 近道の元は主位置の手前で切る（主位置を帯に残す・凍結した確かめ・効き目の比べだけでは弱い: 合成の記録）
                raise ToolError('近道の元が主位置の手前で切れていない（%d・主位置 %d）: %s' % (pc['end'], cell.mp, cell.key))
            n_cached = int(pc['legacy'][0][0].shape[-2])      # 記録した切れ目だけでなく、使い回す cache の列の実の長さも見る（裁定 D231）
            if n_cached != cell.mp:
                raise ToolError('使い回す cache の列の長さが主位置と違う（%d・主位置 %d）: %s' % (n_cached, cell.mp, cell.key))
            inp = torch.tensor([cell.ids[pc['end']:]] * B, device=self.dev)
            starts = [0] * B
            past = self._expand(pc, B)
        cap, hs = {}, []
        hs.append(self.model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone())))
        if want_layers:
            layers = self.model.model.layers
            for j in self.after:
                hs.append(layers[j].register_forward_hook(lambda m, a, o, j=j: cap.__setitem__(j, (o[0] if isinstance(o, tuple) else o)[:, -1, :].detach().clone())))
        handle = RB.register_hook(self.model, self.layer, RB.make_hook(V, self.coef, int(sign), starts, meta={'bl3': True, 'cell': cell.key}))
        try:
            with torch.no_grad():
                out = self.model(input_ids=inp, past_key_values=past, use_cache=past is not None, logits_to_keep=1)
        finally:
            handle.remove()
            for h_ in hs:
                h_.remove()
            RB.assert_no_hooks(self.model, self.layer)
        self.n_forward += 1
        r = self.readout(cap['h'], cell, full=full)
        res = {'lo': r['lo'], 'pa': r['pa'], 'Zset': r['Zset']}
        if full:
            res['mass'] = r['mass']
            res['Zfull'] = r['Zfull']
        if want_model_logits:
            res['model_set_logits'] = out.logits[:, -1, :][:, cell.set_ids].float().double().cpu().numpy()
        if want_layers:
            res['layers'] = {j: cap[j].float() for j in self.after}
            res['layer_lo'] = {j: K.log_odds_a((self.norm32(cap[j]) @ self.W32[cell.set_ids].T).double().cpu().numpy(), 0, list(range(1, len(cell.set_ids)))) for j in self.after}
        return res

    # ---- 自己検査 ----
    def logit_check(self, cell, tol):
        """出口の値の自己検査（正本 `computation.self_checks.logit`）: 無操作・近道なし・バッチ一。"""
        r = self.forward(cell, [K.NOOP], +1, want_model_logits=True, full=False)
        d = float(np.max(np.abs(r['Zset'] - r['model_set_logits'])))
        return {'cell': cell.key, 'max_abs': d, 'tol': tol, 'pass': d <= tol}

    def layer_check(self, cell, sign, did, tol, pc=None):
        """最後の層の自己検査（正本 `computation.self_checks.layer`）: 層ごとの差分の最後の層の行と、読み取りの効き目の差。"""
        r = self.forward(cell, [K.NOOP, did], sign, pc=pc, want_layers=True, full=False)
        last = self.after[-1]
        eff_read = float(r['lo'][1] - r['lo'][0])
        eff_layer = float(r['layer_lo'][last][1] - r['layer_lo'][last][0])
        d = abs(eff_read - eff_layer)
        return {'cell': cell.key, 'sign': sign, 'direction': did, 'diff': d, 'tol': tol, 'pass': d <= tol}


# ---------------- 下見（無操作だけ） ----------------
def run_pilot(R, cells_main, cells_gate_only, T3, variant_prefixes, stage_b_rate, sampling):
    """正本 `pilot`: 出口の値の自己検査 → (vi) → (i)〜(iv) → (v) → 決め。値の記録と機械の決定を返す（読みは付けない）。"""
    P = T3['pilot']
    batch_default = T3['readout']['primary']['batch']
    rec = collections.OrderedDict(version=VERSION)
    lc = R.logit_check(cells_main[0], T3['computation']['logit_tol'])
    rec['logit_check'] = lc
    if not lc['pass']:
        raise ToolError('出口の値の自己検査が落ちた: %s' % lc)
    # (vi) (a) 零のベクトルだけで満たしたバッチ（全ての位置）と大きさ一 ・ (b) 大きさ一の繰り返し
    a_vals, b_vals, first16 = {}, {}, {}
    for c in cells_main:
        r16 = R.forward(c, [K.NOOP] * batch_default, +1, full=False)
        r1 = R.forward(c, [K.NOOP], +1, full=False)
        a_vals[c.key] = list(map(float, r16['lo'])) + [float(r1['lo'][0])]
        first16[c.key] = float(r16['lo'][0])
        b_vals[c.key] = [float(r1['lo'][0])] + [float(R.forward(c, [K.NOOP], +1, full=False)['lo'][0]) for _ in range(P['repeat_n'] - 1)]
    sa = max(K.spread(v) for v in a_vals.values())
    sb = max(K.spread(v) for v in b_vals.values())
    vi = K.vi_decision(sa, sb, P['noise_max'], batch_default)
    rec['vi'] = {'a': {k: K.spread(v) for k, v in a_vals.items()}, 'b': {k: K.spread(v) for k, v in b_vals.items()}, 'decision': vi}
    if vi['stop']:
        rec['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
        return rec
    batch = vi['batch']
    tol = K.cache_tol(vi['floor'], P['cache_tol_factor'], P['cache_tol_floor'], P['noise_max'])
    rec['batch'], rec['floor'], rec['cache_tol'] = batch, vi['floor'], tol

    def noop_at_config(c, prefix=None):
        cc = c if prefix is None else c.with_prefix(prefix)
        r = R.forward(cc, [K.NOOP] * batch, +1, full=True)
        return {'lo': float(r['lo'][0]), 'pa': float(r['pa'][0]), 'mass': float(r['mass'][0]), 'Zfull0': r['Zfull'][0].cpu().numpy()}
    # (i)(ii)(iii)
    cells_all = list(cells_main) + list(cells_gate_only)
    nv = {c.key: noop_at_config(c) for c in cells_all}
    ok_main = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], P['mass_min'], P['p_bounds']) for c in cells_main}
    ok_gate = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], P['mass_min'], P['p_bounds']) for c in cells_gate_only}
    import blens_core as C
    pT = {}
    for c in cells_main:
        pt = C.transform(nv[c.key]['Zfull0'], sampling['temperature'], sampling['top_k'], sampling['top_p'])
        pT[c.key] = float(pt[c.set_ids[0]])
    raw = [nv[c.key]['pa'] for c in cells_main]
    obs = [stage_b_rate[c.key] for c in cells_main]
    rho = C.spearman(raw, obs)
    rec['cells'] = {c.key: {'lo': nv[c.key]['lo'], 'pa': nv[c.key]['pa'], 'mass': nv[c.key]['mass'], 'pa_transformed': pT.get(c.key), 'stage_b_rate': stage_b_rate.get(c.key),
                            'pass_i_ii': (ok_main if c in cells_main else ok_gate)[c.key], 'main': c in cells_main} for c in cells_all}
    rec['iii'] = {'rho': rho, 'n': len(raw), 'sentence': K.iii_sentence(rho), 'transformed_def': P['checks']['iii']['transformed_def']}      # 変換を通した値の定義を記録にも置く（裁定 D231・D235）
    # (iv) 揺れの版
    iv = {}
    for name, pref in variant_prefixes.items():
        lv = {c.key: noop_at_config(c, pref)['lo'] for c in cells_main}
        iv[name] = {'lo': lv, 'flags': K.variant_flags({c.key: nv[c.key]['lo'] for c in cells_main}, lv, P['variant_flag'])}
    rec['iv'] = iv
    # (v) 近道（主の升目と門の行だけの升目）
    diffs = {}
    for c in cells_all:
        pc = R.prefix_cache(c)
        r = R.forward(c, [K.NOOP] * batch, +1, pc=pc, full=False)
        diffs[c.key] = float(r['lo'][0]) - nv[c.key]['lo']
    rec['v'] = {'diffs': diffs, 'tol': tol, 'shortcut': K.shortcut_ok(list(diffs.values()), tol)}
    cd = K.cells_decision(ok_main, ok_gate, P['decision']['cells_min_pass'])
    rec['decision'] = cd
    rec['n_forward'] = R.n_forward
    return rec


# ---------------- 本の計算 ----------------
def cell_sign_sets(T3, cells_by_key, named, b3, iso, real, gate_only_cells):
    """升目と符号ごとの方向の集まり（正本 `readout.primary.batching`・転記行 E の組み立て）。戻り値: [(升目と符号の鍵, 升目, 符号, 方向の名の並び)]。"""
    main = [(sc, base, int(sg)) for sc, base, sg in T3['cell_signs_main']]
    out = []
    for sc, base, sg in main:
        out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(b3) + list(iso) + list(real)))
    for key in gate_only_cells:
        sc, base, sg = key
        out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(b3)))
    for sc, base, sg in main:
        if (sc, base, -sg) not in main:
            out.append(('%s|%s|%+d' % (sc, base, -sg), '%s|%s' % (sc, base), -sg, list(real)))
    keys = [o[0] for o in out]
    assert len(keys) == len(set(keys))
    return out


def run_cell_sign(R, cell, sign, dir_ids, batch, seed, key_index, pc=None, layer_dirs=(), keep_iso_layers=True):
    """一つの升目と符号の全ての方向（零のベクトルの無操作を含む・端数は零のベクトルで埋める）。無操作の入ったバッチを先に流す（層ごとの差分のため）。"""
    plan = K.batch_plan(dir_ids, batch, seed, key_index)
    first = [i for i, b in enumerate(plan) if K.NOOP in b]
    assert len(first) == 1
    order = first + [i for i in range(len(plan)) if i != first[0]]
    lo, mass, pa = {}, {}, {}
    lay = {'noop_lo': None, 'rows': {}, 'iso': collections.defaultdict(list)}
    noop_h = None
    for bi in order:
        ids_ = plan[bi]
        want_layers = any((d == K.NOOP) or (d in layer_dirs) or (keep_iso_layers and d.startswith('iso:')) for d in ids_)
        r = R.forward(cell, ids_, sign, pc=pc, want_layers=want_layers, full=True)
        for k_, d in enumerate(ids_):
            if d == K.PAD:
                continue
            lo[d], mass[d], pa[d] = float(r['lo'][k_]), float(r['mass'][k_]), float(r['pa'][k_])
        if want_layers:
            if noop_h is None:
                k0 = ids_.index(K.NOOP)
                noop_h = {j: r['layers'][j][k0].clone() for j in R.after}
                lay['noop_lo'] = {j: float(r['layer_lo'][j][k0]) for j in R.after}
            for k_, d in enumerate(ids_):
                if d in (K.PAD, K.NOOP) or not ((d in layer_dirs) or (keep_iso_layers and d.startswith('iso:'))):
                    continue
                u = float(sign) * R.torch.tensor(R.vec(d), device=R.dev).float()      # 足した向き（符号を掛けた方向）との余弦（正本 `descriptive.layerwise.values`・裁定 D231）
                vals = []
                for j in R.after:
                    dh = r['layers'][j][k_] - noop_h[j]
                    nrm = float(dh.norm())
                    cos = float((dh @ u) / (dh.norm() * u.norm())) if nrm > 0 else 0.0
                    vals.append((nrm, cos, float(r['layer_lo'][j][k_]) - lay['noop_lo'][j]))
                if d in layer_dirs:
                    lay['rows'][d] = vals
                else:
                    lay['iso'][d] = vals
    require_finite(lo, '升目と符号 %s|%+d の対数オッズ' % (cell.key, sign))
    require_finite(mass, '升目と符号 %s|%+d の質量' % (cell.key, sign))
    require_finite(pa, '升目と符号 %s|%+d の集合の中の確率' % (cell.key, sign))
    eff = {d: lo[d] - lo[K.NOOP] for d in lo if d != K.NOOP}
    return {'lo': lo, 'effects': eff, 'mass': mass, 'pa_noop': pa[K.NOOP], 'layers': lay, 'n_batches': len(plan)}


def recompute_hook_path(R, rows, dirs_by_row, log=None):
    """独立の再計算の本の器のフックの道（正本 `independent_recompute.new_paths` の一つ目・近道なし・バッチ一）。
    rows: [(行の名, 升目, 符号)]・dirs_by_row: 行の名 → [(方向の名, 符号)]（比べる相手の逆の向きは符号を反転して流す）。戻り値: 行の名 → {'noop_lo', 'effects': {'方向の名|符号': 効き目}}。
    log があれば、行ごとに行の名と順伝播の数と時間だけを渡す（値は渡さない）。"""
    out = {}
    t0 = time.time()
    for i, (name, cell, sign) in enumerate(rows):
        base = float(R.forward(cell, [K.NOOP], sign, full=False)['lo'][0])
        eff = {}
        for did, sg in dirs_by_row[name]:
            eff['%s|%+d' % (did, sg)] = float(R.forward(cell, [did], sg, full=False)['lo'][0]) - base
        require_finite(dict(eff, noop=base), '独立の再計算のフックの道の行 %s' % name)
        out[name] = {'noop_lo': base, 'effects': eff}
        if log:
            log('[bl3_run] 独立の再計算のフックの道 %s（%d/%d・順伝播 %d）・%.0f 秒' % (name, i + 1, len(rows), 1 + len(eff), time.time() - t0))
    return out


def build_cells(tok, T3, FJ, keys):
    """升目の入力（凍結の組み立ての関数と転記行 A の書き出し）を作り、転記行 B のプロンプトの長さ・主位置・読み取りの位置と突き合わせる（違えば止める）。"""
    import steer_B
    import run_stageB_local as RB
    AT = RB.arm_texts()
    A, B = FJ['facts']['A'], FJ['facts']['B']['cells']
    L = A['letter_ids']
    fam_letters = T3['readout']['primary']['letters']
    out = collections.OrderedDict()
    for key in keys:
        sc, arm = key.split('|')
        scen, inst = RB.scenario_and_instruction(sc)
        prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
        fam = scen['family']
        set_ids = [int(L[x]) for x in fam_letters[fam]] + [int(L['refuse'])]
        c = Cell(key, sc, arm, fam, prompt, A['prefix_ids'], set_ids, steer_B.main_position(prompt))
        b = B[key]
        if (len(prompt), c.mp, c.ro, fam) != (b['prompt_len'], b['main_position'], b['readout_position'], b['family']):
            raise ToolError('升目の入力が転記行 B と違う: %s' % key)
        out[key] = c
    return out


def load_dirs(npz_path, json_path, T3=None, FJ=None):
    """方向の npz（`tools/bl3_directions.py`）を名で引ける形にする。SHA-256 は記録と突き合わせる（違えば止める）。
    T3 と FJ を与えると、名前のある方向の名の並びが正本と、実在の差の名の並びが転記行 D と同じことも確かめる（名と行を位置で結ぶので・裁定 D236）。"""
    import hashlib
    J = json.load(open(json_path, encoding='utf-8'))
    if hashlib.sha256(open(npz_path, 'rb').read()).hexdigest().upper() != J['npz_sha256']:
        raise ToolError('方向の npz の SHA-256 が記録と違う')
    if T3 is not None and list(J['groups']['named']['names']) != list(T3['directions']['named']):
        raise ToolError('方向の記録の名前のある方向の名の並びが正本と違う')
    if FJ is not None and list(J['groups']['real']['names']) != list(FJ['facts']['D']['real_pairs']):
        raise ToolError('方向の記録の実在の差の名の並びが転記行 D と違う')
    Z = np.load(npz_path)
    names = {'named': J['groups']['named']['names'], 'B_random': J['groups']['B_random']['names'],
             'iso': ['iso:%d' % i for i in range(J['groups']['iso']['count'])], 'real': ['real:' + p for p in J['groups']['real']['names']], 'check': ['check']}
    d = collections.OrderedDict()
    for g, ns in names.items():
        A = Z[g]
        if len(A) != len(ns):
            raise ToolError('方向の組の本数が記録と違う: %s' % g)
        for n, v in zip(ns, A):
            d[n] = np.asarray(v, dtype=np.float64)
    return d, names


def secondary_contexts(tok, T3, FJ, FB, repo):
    """乙の文脈（正本 `readout.secondary`・裁定 D227）: B-lens の層二で選んだ出力（B-lens の設計事実の転記行 E の `selected`・一覧の SHA16 を確かめる）の、
    プロンプトと出力の選択の文字を覆うトークンの前までの教師強制の入力（凍結の `boot_Blens.context_of`）。戻り値: [(層の鍵, 試行の番号, 升目の入力, 文脈の記録)]。"""
    import hashlib, glob
    import steer_B
    import run_stageB_local as RB
    sys.path.insert(0, os.path.join(HERE, 'colab'))
    import boot_Blens as BOOT
    E = FB['facts']['E']
    sel = E['selected']
    if hashlib.sha256(json.dumps(sel, sort_keys=True).encode('utf-8')).hexdigest().upper()[:16] != E['selected_sha16']:
        raise ToolError('乙の文脈の一覧の SHA16 が B-lens の設計事実と違う')
    AT = RB.arm_texts()
    L = FJ['facts']['A']['letter_ids']
    fam_letters = T3['readout']['primary']['letters']
    out = []
    for key, ids_ in sel.items():
        sc, arm, style = key.split('|')
        scen, inst = RB.scenario_and_instruction(sc)
        prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
        d = os.path.join(repo, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
        ft, fr = glob.glob(os.path.join(d, 'trials-*.jsonl')), glob.glob(os.path.join(d, 'raw-*.jsonl'))
        if len(ft) != 1 or len(fr) != 1:
            raise ToolError('段階 B の試行の記録か出力の記録がちょうど一つでない: %s（%d・%d）' % (d, len(ft), len(fr)))
        tr = {json.loads(l)['trial_id']: json.loads(l) for l in open(ft[0], encoding='utf-8')}
        rw = {json.loads(l)['trial_id']: json.loads(l) for l in open(fr[0], encoding='utf-8')}
        fam = scen['family']
        set_ids = [int(L[x]) for x in fam_letters[fam]] + [int(L['refuse'])]
        for tid in ids_:
            try:
                cx = BOOT.context_of(tok, prompt, tr[tid], rw[tid], AT[arm]['sha16'], steer_B.main_position)
            except BOOT.Stop as e_:
                raise ToolError('乙の文脈を組めない: %s' % e_)
            cell = Cell('%s|%s' % (sc, arm), sc, arm, fam, prompt, cx['ids'][len(prompt):], set_ids, steer_B.main_position(prompt))
            rec = {'stratum': key, 'trial_id': tid, 'choice': cx['choice'], 'letter_token': cx['letter_token'],
                   'letter_token_is_L': cx['letter_token'] == int(L.get(cx['choice'], -1)), 'n_ids': len(cx['ids'])}
            out.append((key, tid, cell, rec))
    return out


def run_secondary(R, contexts, rows_by_cell, log=None):
    """乙（正本 `descriptive.secondary_readout`・裁定 D227）: 文脈ごとに、その升目の門の行（名前のある方向と段階 B の三本）の方向を、行の符号で加える（近道なし）。
    符号ごとに零のベクトルの無操作と同じバッチに流す。戻り値: 文脈ごとに、行の名 → 対数オッズの変化と、選択肢 a と c の文字の出口の値の変化。
    log があれば、文脈ごとに層の鍵と試行の番号と時間だけを渡す（値は渡さない）。"""
    out = []
    t0 = time.time()
    for ci, (key, tid, cell, rec) in enumerate(contexts):
        if log:
            log('[bl3_run] 乙 %s %s（%d/%d）・%.0f 秒' % (key, tid, ci + 1, len(contexts), time.time() - t0))
        rows = rows_by_cell.get(cell.key, [])
        by_sign = collections.OrderedDict()
        for name, did, sg in rows:
            by_sign.setdefault(sg, []).append((name, did))
        i_c = 2                                                      # 読み取りの集合は族の選択の文字の順（a・b・c…）で、c は三つ目
        res = {}
        for sg, items in by_sign.items():
            r = R.forward(cell, [K.NOOP] + [d for _, d in items], sg, full=False)
            for k_, (name, did) in enumerate(items, start=1):
                res[name] = {'dlo': float(r['lo'][k_] - r['lo'][0]), 'dz_a': float(r['Zset'][k_, 0] - r['Zset'][0, 0]), 'dz_c': float(r['Zset'][k_, i_c] - r['Zset'][0, i_c])}
        require_finite({'%s|%s' % (n_, k_): v_ for n_, d_ in res.items() for k_, v_ in d_.items()}, '乙の文脈 %s %s' % (key, tid))
        out.append(dict(rec, rows=res, n_batches=len(by_sign)))
    return out


def run_main_phase(R, T3, FJ, cells, names, pilot, iso_n=None, log=print):
    """本の計算の全体（正本 `computation`・`readout.primary.batching`）: 頭の自己検査（出口の値・最後の層）→ 全ての升目と符号。本の計算は近道を使わない（裁定 D234・
    下見の (v) は記述として残す）ので、頭の近道の確かめは走らせない（正本 `computation.steered_cache_check` は「近道を使うときだけ」）。
    pilot: 本の凍結で凍結した下見の記録（バッチの大きさ・揺れの床・近道の許容・近道・外した升目）。names: {'named','B_random','iso','real'} の名の並び。
    iso_n は合成データの確かめで等方の本数を減らすときだけ使う。戻り値: {'head': 頭の確かめ, 'cells': 升目と符号の鍵 → 出力}。
    層ごとの差分は、名前のある方向と段階 B の三本の行と、等方の帰無の層ごとの中央値と中央の区間だけを残す（正本 `descriptive.layerwise.directions`）。"""
    dropped = set((pilot.get('decision') or {}).get('dropped', []))
    batch = pilot['batch']
    main_keys = ['%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']]
    items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in T3['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
    head = collections.OrderedDict()
    head['logit_check'] = R.logit_check(items[0][0], T3['computation']['logit_tol'])
    if not head['logit_check']['pass']:
        raise ToolError('出口の値の自己検査が落ちた（本の計算の頭）: %s' % head['logit_check'])
    shortcut = False                                                    # 本の計算は近道を使わない（裁定 D234）
    head['shortcut'] = shortcut
    head['shortcut_rule'] = '本の計算は近道を使わない（裁定 D234）・下見の (v) の近道: %s（記述）' % (pilot.get('v') or {}).get('shortcut')
    head['layer_check'] = R.layer_check(items[0][0], items[0][1], 'check', T3['computation']['layer_tol'])
    if not head['layer_check']['pass']:
        raise ToolError('最後の層の自己検査が落ちた（本の計算の頭）: %s' % head['layer_check'])
    iso = names['iso'] if iso_n is None else names['iso'][:iso_n]
    gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
    sets = cell_sign_sets(T3, None, names['named'], names['B_random'], iso, names['real'], gate_only)
    layer_dirs = list(names['named']) + list(names['B_random'])
    band = T3['descriptive']['layerwise']['band']
    out = collections.OrderedDict()
    t0 = time.time()
    for ki, (key, ck, sg, ds) in enumerate(sets):
        if ck in dropped:
            continue
        main_cs = key in main_keys
        pc = R.prefix_cache(cells[ck]) if shortcut else None
        o = run_cell_sign(R, cells[ck], sg, ds, batch, T3['readout']['primary']['order_seed'], ki, pc=pc, layer_dirs=layer_dirs if main_cs else (), keep_iso_layers=main_cs)
        o['layers'] = {'noop_lo': o['layers']['noop_lo'], 'rows': o['layers']['rows'], 'iso_summary': layer_summary(o['layers'], band) if main_cs else None}
        out[key] = o
        log('[bl3_run] 升目と符号 %s（%d/%d）・%.0f 秒' % (key, ki + 1, len(sets), time.time() - t0))
    return {'head': head, 'cells': out, 'batch': batch, 'shortcut': shortcut, 'dropped': sorted(dropped)}


def layer_summary(lay, band):
    """等方の帰無の層ごとの中央値と中央の区間（正本 `descriptive.layerwise.directions`・`band`）。"""
    if not lay['iso']:
        return None
    A = np.array(list(lay['iso'].values()), dtype=np.float64)       # 方向 × 層 × 三つ
    lo_q, hi_q = 100 * (1 - band) / 2, 100 * (1 + band) / 2
    return {'median': np.median(A, axis=0).tolist(), 'lo': np.percentile(A, lo_q, axis=0).tolist(), 'hi': np.percentile(A, hi_q, axis=0).tolist(), 'n': int(A.shape[0])}


if __name__ == '__main__':
    print(__doc__)
