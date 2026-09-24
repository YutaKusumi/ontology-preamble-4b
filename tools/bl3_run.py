# -*- coding: utf-8 -*-
"""bl3_run.py v1 —— B-lens 層三（Bl3）の教師強制の順伝播を走らせる器（2026-09-25・正本 `readout.primary`・`pilot`・`computation`・`descriptive`）。

走らせ方（正本のとおり・値は器の出力に置き、読みは付けない）:
  - 入力: 段階 B の組み立てのままのプロンプト（凍結の `steer_B.apply_chat`・`run_stageB_local.user_message`）の直後に、主の書き出し（設計事実の転記行 A の
    トークンの並び）を置く。主位置は凍結の `steer_B.main_position`、読み取りの位置は列の最後（主位置 ＋ 書き出しの長さ）。
  - 加減: 凍結の `run_stageB_local.make_hook`（行ごとの方向の行列を受ける形・層の出力の型に直して足す・係数は一度だけ）を、選んだ層（凍結の
    `direction_B.layer_index`）に凍結の `register_hook` で掛ける。帯は主位置から読み取りの位置まで。零のベクトルの行が無操作。
  - 近道: 主位置より前（添字 0〜主位置−1）の計算を加減なしで一度だけ作り、バッチの大きさに写して、主位置から後ろだけを流す（帯の起点は写した後の 0）。
  - 読み取り: 最終の正規化の入力（最後の層の出口の残差）を前の hook で取り、`float32` に上げて最終の正規化と語彙の行列の読み取りの集合の行を `float32` で当てる。
    全語彙の softmax は質量にだけ使う（`float32`）。層ごとの差分は、選んだ層の後の各層の出口の hook で取る（`hidden_states` は使わない）。
  - 自己検査: 出口の値（読み取りの集合の `float32` の出口の値と、模型そのものの出口の値〔bf16〕の差の最大・許容 `computation.logit_tol`）と、
    最後の層（層ごとの差分の最後の層の行と読み取りの効き目の差・許容 `computation.layer_tol`）。落ちたら止める（器の誤り・正本 `pilot.decision.tool_error`・
    `computation.tool_error`）。
関数は Colab の起動器 `tools/colab/boot_Bl3.py` と合成データの器 `tools/dry_run_Bl3.py` が import して呼ぶ（この器だけでは模型を読まない）。
DRY（乱数の小さな模型）の確かめのために、壊した読み取り（二重の正規化）と壊した近道（主位置まで使い回す）を、引数 `bug` で入れられる（本の計算では入れない）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, time, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bl3_core as K

VERSION = 'v1'
BUGS = (None, 'double_norm', 'cache_through_mp')


class ToolError(Exception):
    """凍結した確かめが機械で落ちた（器の誤り・正本 `pilot.decision.tool_error.what`）。"""


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
    rec['iii'] = {'rho': rho, 'n': len(raw), 'sentence': K.iii_sentence(rho)}
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
                u = R.torch.tensor(R.vec(d), device=R.dev).float()
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
    eff = {d: lo[d] - lo[K.NOOP] for d in lo if d != K.NOOP}
    return {'lo': lo, 'effects': eff, 'mass': mass, 'pa_noop': pa[K.NOOP], 'layers': lay, 'n_batches': len(plan)}


def steered_cache_check(R, items, batch, tol):
    """本の計算の頭の近道の確かめ（正本 `computation.steered_cache_check`）: 近道の確かめの一本と零のベクトルを、主の組の全ての升目と符号で、
    近道ありと近道なしの両方の道に同じバッチの大きさで流し、効き目の差の絶対値の最大を返す（許容の外なら近道を使わない）。items: [(升目, 符号)]。"""
    worst, per = 0.0, {}
    for cell, sign in items:
        pc = R.prefix_cache(cell)
        if batch >= 2:
            ids_ = [K.NOOP, 'check'] + [K.PAD] * (batch - 2)
            rf, rs = R.forward(cell, ids_, sign, full=False), R.forward(cell, ids_, sign, pc=pc, full=False)
            ef, es = float(rf['lo'][1] - rf['lo'][0]), float(rs['lo'][1] - rs['lo'][0])
        else:
            ef = float(R.forward(cell, ['check'], sign, full=False)['lo'][0] - R.forward(cell, [K.NOOP], sign, full=False)['lo'][0])
            es = float(R.forward(cell, ['check'], sign, pc=pc, full=False)['lo'][0] - R.forward(cell, [K.NOOP], sign, pc=pc, full=False)['lo'][0])
        per['%s|%+d' % (cell.key, sign)] = es - ef
        worst = max(worst, abs(es - ef))
    return {'max_abs': worst, 'tol': tol, 'shortcut': worst <= tol, 'per': per}


def recompute_hook_path(R, rows, dirs_by_row):
    """独立の再計算の本の器のフックの道（正本 `independent_recompute.new_paths` の一つ目・近道なし・バッチ一）。
    rows: [(行の名, 升目, 符号)]・dirs_by_row: 行の名 → [(方向の名, 符号)]（比べる相手の逆の向きは符号を反転して流す）。戻り値: 行の名 → {'noop_lo', 'effects': {'方向の名|符号': 効き目}}。"""
    out = {}
    for name, cell, sign in rows:
        base = float(R.forward(cell, [K.NOOP], sign, full=False)['lo'][0])
        eff = {}
        for did, sg in dirs_by_row[name]:
            eff['%s|%+d' % (did, sg)] = float(R.forward(cell, [did], sg, full=False)['lo'][0]) - base
        out[name] = {'noop_lo': base, 'effects': eff}
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


def load_dirs(npz_path, json_path):
    """方向の npz（`tools/bl3_directions.py`）を名で引ける形にする。SHA-256 は記録と突き合わせる（違えば止める）。"""
    import hashlib
    J = json.load(open(json_path, encoding='utf-8'))
    if hashlib.sha256(open(npz_path, 'rb').read()).hexdigest().upper() != J['npz_sha256']:
        raise ToolError('方向の npz の SHA-256 が記録と違う')
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


def layer_summary(lay, band):
    """等方の帰無の層ごとの中央値と中央の区間（正本 `descriptive.layerwise.directions`・`band`）。"""
    if not lay['iso']:
        return None
    A = np.array(list(lay['iso'].values()), dtype=np.float64)       # 方向 × 層 × 三つ
    lo_q, hi_q = 100 * (1 - band) / 2, 100 * (1 + band) / 2
    return {'median': np.median(A, axis=0).tolist(), 'lo': np.percentile(A, lo_q, axis=0).tolist(), 'hi': np.percentile(A, hi_q, axis=0).tolist(), 'n': int(A.shape[0])}


if __name__ == '__main__':
    print(__doc__)
