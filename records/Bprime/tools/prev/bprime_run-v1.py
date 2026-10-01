# -*- coding: utf-8 -*-
"""bprime_run.py v1（2026-09-30・B′ の教師強制の順伝播を走らせる器・層三の `bl3_run.py` v3 を Gemma 4 と B′ の正本に移したもの・コーディネータ南無弥勒如来）。

走らせ方（正本 `design/contrasts-Bprime.json` のとおり・値は器の出力に置き、読みは付けない）:
  - 入力: 段階 B の組み立て（凍結の `run_stageB_local.arm_texts`・`scenario_and_instruction`・`user_message`）に B′ のチャットの型（`bprime_gemma.apply_chat`）を当て、
    直後に主の書き出し（台帳の番号の並び）を置く。主位置は列の最後のトークン（Gemma では `<channel|>`）、読み取りの位置は列の最後（`readout.primary`）。
  - 加減: 凍結の `run_stageB_local.make_hook`（行ごとの方向の行列・層の出力の型に直して足す・係数は一度だけ）を、選んだ層（`layers.index`）に B′ の `register_hook` で掛ける。
    帯は主位置から読み取りの位置まで。零のベクトルの行が無操作。近道は使わない（`computation.shortcut`）。
  - 読み取り: 最終の正規化の入力を前のフックで取り、`float32` に上げて最終の正規化・語彙の行列・softcap（cap × tanh(z/cap)）を当てる（`readout.primary.quantity`）。
    質量（全語彙の softmax）と層ごとの差分（選んだ層の後の各層の出口をフックで取る・`hidden_states` は使わない）も softcap の後の値で出す。
  - 出口の値の自己検査（`computation.self_checks.logit`）: 読み取りの集合の行と、その位置の模型の出口の上位の行に、softcap あり（器の道）・なし・正規化の二重の三つを当て、
    模型の出口の値（bf16）と `bprime_core.logit_self_check` で突き合わせる（合・否・見分ける力無し）。k は凍結の前に意味のない列で測る（`measure_positions`）。
  - 最後の層の自己検査（`computation.self_checks.layer`）: 自己検査の一本と零のベクトルで、層ごとの差分の最後の層の行と読み取りの効き目の差。
  - 下見（`pilot`）: 出口の値の自己検査 → (vi) → (i)(ii)(iv) → 決め → (iii)（行動の下見の主の率・外した升目を除く・`generate` と同じ処理の並びの変換を添える）。(v) は置かない。
  - 本の計算（`readout.primary.batching`）: 升目と符号の組ごとに、名前のある方向・等方・実在の差（組の符号の向き）と零のベクトル。Onull の組には逆の向きの実在の差を足す（`nulls.real.combos`）。
  - 道の違いの記述（`descriptive.path_difference`）: 本の計算がバッチ一に移ったときに、同じ組をバッチ 16 の道で流す。
関数は起動器と合成データの器が import して呼ぶ（この器だけでは模型を読まない）。
DRY のために壊した器を引数 `bug` で入れられる（本の計算では入れない）: double_norm・no_softcap・hook_next_layer。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, time, hashlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G          # 先に読む（凍結の器の置き場を sys.path に足す）
import bl3_core as K              # 層三の凍結の芯（対数オッズ・集合の中の確率・零と埋めの名・バッチの組み方・下見の決め）
import bprime_core as P           # B′ の芯（許容の式と判定・床の余白の印ほか）

VERSION = 'v1'          # v1（2026-09-30）: 正本 v2 に合わせた（出口の値の自己検査の新しい許容・意味のない列での k の測り・下見・本の計算・道の違い・独立の再計算のフックの道・升目の組み立て・方向の読み込み）
BUGS = (None, 'double_norm', 'no_softcap', 'hook_next_layer')
ToolError = P.ToolError


def require_finite(vals, where):
    """値がすべて有限であること（有限でなければ器の誤りで止める・層三の裁定 D236 の型）。vals: 名 → 値。"""
    bad = sorted(k for k, v in vals.items() if not math.isfinite(float(v)))
    if bad:
        raise ToolError('有限でない値（%s・%d 個・例 %s）' % (where, len(bad), bad[:3]))


def ids_sha16(ids):
    return hashlib.sha256(','.join(str(int(x)) for x in ids).encode('ascii')).hexdigest().upper()[:16]


class Cell:
    """一つの升目（場面 × 土台の腕）の入力と位置（層三の `bl3_run.Cell` と同じ決まり）。"""

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
    def __init__(self, model, C, layer_idx, coef, dirs, bug=None):
        import torch
        import run_stageB_local as RB           # 凍結の段階 B の走行器（make_hook だけ使う）
        if bug not in BUGS:
            raise ValueError(bug)
        self.torch, self.RB, self.model, self.C, self.bug = torch, RB, model, C, bug
        self.layer, self.coef = int(layer_idx), float(coef)
        self.dev = next(model.parameters()).device
        self.eps = G.rms_eps(model)
        self.n_layers = G.n_layers(model)
        self.after = list(range(self.layer + 1, self.n_layers))
        self.g32 = G.final_norm(model).weight.detach().float()
        self.W32 = model.lm_head.weight.detach().float()
        self.cap = G.softcap(model)
        if self.cap is None:
            raise ToolError('softcap が設定に無い（正本 `inputs.model_facts.final_logit_softcapping`）')
        self.dirs = dirs
        self.dim = int(self.g32.shape[0])
        self._zero = np.zeros(self.dim, dtype=np.float32)
        self.n_forward = 0

    # ---- 方向 ----
    def vec(self, did):
        if did in (K.NOOP, K.PAD):
            return self._zero
        return np.asarray(self.dirs[did], dtype=np.float32)

    # ---- 正規化と読み取り（float32） ----
    def norm32(self, h):
        h = h.float()
        return h * self.torch.rsqrt(h.pow(2).mean(-1, keepdim=True) + self.eps) * self.g32

    def capz(self, z, force=False):
        """softcap（器の道）。bug='no_softcap' の器は掛けない（force=True は正しい式を強いる）。"""
        if self.bug == 'no_softcap' and not force:
            return z
        return self.torch.tanh(z / self.cap) * self.cap

    def ours(self, h):
        """器の道の正規化（bug='double_norm' の器は二重に掛ける）。"""
        hn = self.norm32(h)
        return self.norm32(hn) if self.bug == 'double_norm' else hn

    def readout(self, h, cell, full=True):
        hn = self.ours(h)
        Zs = self.capz(hn @ self.W32[cell.set_ids].T).double().cpu().numpy()
        out = {'Zset': Zs, 'lo': K.log_odds_a(Zs, 0, list(range(1, len(cell.set_ids)))), 'pa': K.prob_a_in_set(Zs, 0, list(range(len(cell.set_ids))))}
        if full:
            Zf = self.capz(hn @ self.W32.T).double()
            lse_f = self.torch.logsumexp(Zf, dim=-1)
            out['mass'] = self.torch.exp(self.torch.logsumexp(Zf[:, cell.set_ids], dim=-1) - lse_f).cpu().numpy()
            out['Zfull'] = Zf
        return out

    # ---- 一回の順伝播（行ごとの方向・同じ升目・同じ符号・近道なし） ----
    def forward(self, cell, dir_ids, sign, want_layers=False, want_model_logits=False, full=True):
        torch, RB = self.torch, self.RB
        B = len(dir_ids)
        V = np.stack([self.vec(d) for d in dir_ids]).astype(np.float32)
        inp = torch.tensor([cell.ids] * B, device=self.dev)
        starts = [cell.mp] * B
        cap, hs = {}, []
        hs.append(G.final_norm(self.model).register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone())))
        layers = G.decoder_layers(self.model)
        if want_layers:
            for j in self.after:
                hs.append(layers[j].register_forward_hook(lambda m, a, o, j=j: cap.__setitem__(j, (o[0] if isinstance(o, tuple) else o)[:, -1, :].detach().clone())))
        at = self.layer + 1 if self.bug == 'hook_next_layer' else self.layer
        handle = G.register_hook(self.model, at, RB.make_hook(V, self.coef, int(sign), starts, meta={'bprime': True, 'cell': cell.key}))
        try:
            with torch.no_grad():
                out = self.model(input_ids=inp, use_cache=False, logits_to_keep=1)
        finally:
            handle.remove()
            for h_ in hs:
                h_.remove()
            G.assert_no_hooks(self.model, at)
        self.n_forward += 1
        r = self.readout(cap['h'], cell, full=full)
        require_finite({'%d:%d' % (i, j): v for i, row in enumerate(r['Zset']) for j, v in enumerate(row)}, '読み取りの集合の出口の値 ' + cell.key)
        res = {'lo': r['lo'], 'pa': r['pa'], 'Zset': r['Zset'], 'h': cap['h']}
        if full:
            res['mass'] = r['mass']
            res['Zfull'] = r['Zfull']
        if want_model_logits:
            res['model_logits'] = out.logits[:, -1, :].float()
        if want_layers:
            res['layers'] = {j: cap[j].float() for j in self.after}
            res['layer_lo'] = {j: K.log_odds_a(self.capz(self.ours(cap[j]) @ self.W32[cell.set_ids].T).double().cpu().numpy(), 0, list(range(1, len(cell.set_ids)))) for j in self.after}
        return res

    # ---- 出口の値の自己検査 ----
    def three_paths(self, h_row, rows):
        """一つの位置の三つの道（行 rows だけ）: 器の道（softcap あり）・softcap なし（softcap の前の値）・正規化の二重（softcap あり）。"""
        hn = self.norm32(h_row)
        W = self.W32[rows]
        ours = self.capz(self.ours(h_row) @ W.T)
        raw = hn @ W.T
        dbl = self.capz(self.norm32(hn) @ W.T, force=True)
        return ours.double().cpu().numpy(), raw.double().cpu().numpy(), dbl.double().cpu().numpy()

    def check_rows(self, model_logits_row, set_ids, top_rows):
        """掛ける行（正本 `computation.self_checks.logit.rows`）: 読み取りの集合の行と、その位置の模型の出口の値の大きい上位の行（重なりは一度）。"""
        top = self.torch.topk(model_logits_row, int(top_rows)).indices.cpu().tolist()
        rows = list(set_ids) + [int(t) for t in top if int(t) not in set(set_ids)]
        return rows

    def logit_check(self, cell, k, z0):
        """出口の値の自己検査（無操作・近道なし・バッチ一）: 戻り値 {'cell','state','on','off','dbl','n_rows'}。"""
        L = self.C['computation']['self_checks']['logit']
        r = self.forward(cell, [K.NOOP], +1, want_model_logits=True, full=False)
        rows = self.check_rows(r['model_logits'][0], cell.set_ids, L['top_rows'])
        zm = r['model_logits'][0][rows].double().cpu().numpy()
        z_ours, z_raw, z_dbl = self.three_paths(r['h'][0:1], rows)
        s = P.logit_self_check(zm, z_ours[0], z_raw[0], z_dbl[0], k, z0, L['discrimination_factor'])
        return dict(s, cell=cell.key, n_rows=len(rows))

    def measure_positions(self, seqs, set_ids, batch):
        """k の測り（正本 `computation.self_checks.logit.measure`）: 意味のない列（名 → トークンの並び）の最後の位置で、読み取りの集合の行と上位の行について、
        模型の出口の値と器の道（softcap あり）の差の絶対値と、模型の出口の値を集める。batch はバッチの大きさ（同じ列を零のベクトルで並べる）。"""
        L = self.C['computation']['self_checks']['logit']
        diffs, zs = [], []
        for name, ids in seqs.items():
            c = Cell('meaningless|' + name, 'X', 'X', 'X', ids, [], set_ids, len(ids) - 1)
            r = self.forward(c, [K.NOOP] * int(batch), +1, want_model_logits=True, full=False)
            rows = self.check_rows(r['model_logits'][0], set_ids, L['top_rows'])
            zm = r['model_logits'][0][rows].double().cpu().numpy()
            z_ours, _, _ = self.three_paths(r['h'][0:1], rows)
            diffs.append(np.abs(zm - z_ours[0]))
            zs.append(zm)
        return np.concatenate(diffs), np.concatenate(zs)

    def layer_check(self, cell, sign, did, tol):
        """最後の層の自己検査（正本 `computation.self_checks.layer`）: 層ごとの差分の最後の層の行と、読み取りの効き目の差。"""
        r = self.forward(cell, [K.NOOP, did], sign, want_layers=True, full=False)
        last = self.after[-1]
        eff_read = float(r['lo'][1] - r['lo'][0])
        eff_layer = float(r['layer_lo'][last][1] - r['layer_lo'][last][0])
        d = abs(eff_read - eff_layer)
        return {'cell': cell.key, 'sign': sign, 'direction': did, 'diff': d, 'tol': tol, 'pass': d <= tol}


def measure_k(R, seqs, set_ids, batches):
    """k の測りと assert（正本 `computation.self_checks.logit.measure`）。バッチの大きさごとに差を集め、z₀ の決め（大きい行の数）はバッチ一の値で行い、
    同じ z₀ で両方の k を出して大きい方を使う。assert が落ちたら ToolError。戻り値: {'z0','k','k_by_batch','big_rows','fallback','n_rows'}。"""
    L = R.C['computation']['self_checks']['logit']
    got = {int(b): R.measure_positions(seqs, set_ids, b) for b in batches}
    if 1 not in got:
        raise ToolError('バッチ一の測りが無い')
    base = P.k_with_asserts(got[1][0], got[1][1], L)
    z0 = base['z0']
    kmax = L['measure']['asserts']['k_max'] if not base['fallback'] else L['measure']['asserts']['k_max_fallback']
    kb = {b: P.measure_k(d, z, z0, L['tolerance_factor']) for b, (d, z) in got.items()}
    k = max(kb.values())
    if not k <= kmax:
        raise ToolError('許容の k が上限を超えた（バッチの大きさごと %s・上限 %s）' % (kb, kmax))
    return {'z0': z0, 'k': k, 'k_by_batch': kb, 'big_rows': base['big_rows'], 'fallback': base['fallback'], 'n_rows': int(len(got[1][0]))}


def head_logit_checks(R, cells, k, z0):
    """頭の出口の値の自己検査（下見の頭と本の計算の頭）: 升目ごとの状態。否が一つでもあれば ToolError。見分ける力無しの位置は数えて返す（止めない・T05）。"""
    states = collections.OrderedDict((c.key, R.logit_check(c, k, z0)) for c in cells)
    bad = [c for c, s in states.items() if s['state'] == '否']
    if bad:
        raise ToolError('出口の値の自己検査が落ちた: %s' % bad)
    no_disc = [c for c, s in states.items() if s['state'] == '見分ける力無し']
    return {'states': {c: s['state'] for c, s in states.items()}, 'no_discrimination': no_disc, 'n_no_discrimination': len(no_disc), 'detail': states}


# ---------------- 下見（無操作だけ） ----------------
def transformed_prob(Zfull_row, set_id, processors):
    """(iii) の変換を通した値（正本 `pilot.checks.iii.transformed_def`）: 全語彙の出口の値に `generate` と同じ処理の並び（processors）を当てた後の選択肢 a の文字の確率。"""
    import torch
    z = Zfull_row.float().unsqueeze(0)
    z = processors(torch.zeros((1, 1), dtype=torch.long, device=z.device), z)
    p = torch.softmax(z.double(), dim=-1)
    return float(p[0, set_id])


def run_pilot(R, cells_main, C, variant_prefixes, behavior_rate, processors, k, z0):
    """正本 `pilot`: 出口の値の自己検査 → (vi) → (i)(ii)(iv) → 決め → (iii)。値の記録と機械の決定を返す（読みは付けない）。
    behavior_rate: 升目 → 行動の下見の主の率（閉じた記録から）・processors: `generate` と同じ処理の並び（転記行 C に解決した設定）。"""
    PL = C['pilot']
    batch_default = C['readout']['primary']['batch']
    rec = collections.OrderedDict(version=VERSION)
    rec['logit_check'] = head_logit_checks(R, cells_main, k, z0)
    a_vals, b_vals = {}, {}
    for c in cells_main:
        r16 = R.forward(c, [K.NOOP] * batch_default, +1, full=False)
        r1 = R.forward(c, [K.NOOP], +1, full=False)
        a_vals[c.key] = list(map(float, r16['lo'])) + [float(r1['lo'][0])]
        b_vals[c.key] = [float(r1['lo'][0])] + [float(R.forward(c, [K.NOOP], +1, full=False)['lo'][0]) for _ in range(PL['repeat_n'] - 1)]
    sa = max(K.spread(v) for v in a_vals.values())
    sb = max(K.spread(v) for v in b_vals.values())
    vi = K.vi_decision(sa, sb, PL['noise_max'], batch_default)
    rec['vi'] = {'a': {k_: K.spread(v) for k_, v in a_vals.items()}, 'b': {k_: K.spread(v) for k_, v in b_vals.items()}, 'decision': vi}
    if vi['stop']:
        rec['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
        return rec
    batch = vi['batch']
    rec['batch'], rec['floor'] = batch, vi['floor']

    def noop_at_config(c, prefix=None):
        cc = c if prefix is None else c.with_prefix(prefix)
        r = R.forward(cc, [K.NOOP] * batch, +1, full=True)
        return {'lo': float(r['lo'][0]), 'pa': float(r['pa'][0]), 'mass': float(r['mass'][0]), 'Zfull0': r['Zfull'][0]}
    nv = {c.key: noop_at_config(c) for c in cells_main}
    ok_main = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], PL['mass_min'], PL['p_bounds']) for c in cells_main}
    rec['cells'] = {c.key: {'lo': nv[c.key]['lo'], 'pa': nv[c.key]['pa'], 'mass': nv[c.key]['mass'], 'pass_i_ii': ok_main[c.key]} for c in cells_main}
    iv = {}
    for name, pref in variant_prefixes.items():
        lv = {c.key: noop_at_config(c, pref)['lo'] for c in cells_main}
        iv[name] = {'lo': lv, 'flags': K.variant_flags({c.key: nv[c.key]['lo'] for c in cells_main}, lv, PL['variant_flag'])}
    rec['iv'] = iv
    cd = K.cells_decision(ok_main, {}, PL['decision']['cells_min_pass'])
    rec['decision'] = cd
    import blens_core as CB
    keep = [c for c in cells_main if c.key not in set(cd['dropped'])]
    for c in keep:
        rec['cells'][c.key]['pa_transformed'] = transformed_prob(nv[c.key]['Zfull0'], c.set_ids[0], processors)
        rec['cells'][c.key]['behavior_rate'] = behavior_rate.get(c.key)
    if behavior_rate is None or any(behavior_rate.get(c.key) is None for c in keep):
        rec['iii'] = {'sentence_key': None, 'reason': 'behavior_not_closed', 'n': len(keep), 'dropped_n': len(cells_main) - len(keep)}
    else:
        raw = [nv[c.key]['pa'] for c in keep]
        obs = [behavior_rate[c.key] for c in keep]
        rho = CB.spearman(raw, obs) if len(keep) >= 2 else float('nan')
        rec['iii'] = {'rho': rho, 'n': len(keep), 'dropped_n': len(cells_main) - len(keep), 'sentence_key': K.iii_sentence(rho)}
    rec['n_forward'] = R.n_forward
    return rec


# ---------------- 本の計算 ----------------
def cell_sign_sets(C, named, iso, real):
    """升目と符号の組ごとの方向の集まり（正本 `nulls.real.combos`・`readout.primary.batching`）。戻り値: [(組の鍵, 升目の鍵, 符号, 方向の名の並び, 主の組か)]。"""
    main = [(sc, base, int(sg)) for sc, base, sg in C['cell_signs_main']]
    out = []
    for sc, base, sg in main:
        out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(iso) + list(real), True))
    for sc, base, sg in main:
        if (sc, base, -sg) not in main:
            out.append(('%s|%s|%+d' % (sc, base, -sg), '%s|%s' % (sc, base), -sg, list(real), False))
    keys = [o[0] for o in out]
    if len(keys) != len(set(keys)):
        raise ToolError('組の鍵が重なる')
    if sum(1 for o in out if not o[4]) != C['nulls']['real']['onull_combos']:
        raise ToolError('逆の向きの組の数が正本と違う')
    return out


def run_cell_sign(R, cell, sign, dir_ids, batch, seed, key_index, layer_dirs=(), keep_iso_layers=True):
    """一つの升目と符号の全ての方向（零のベクトルの無操作を含む・端数は零のベクトルで埋める）。無操作の入ったバッチを先に流す（層ごとの差分のため）。"""
    plan = K.batch_plan(dir_ids, batch, seed, key_index)
    first = [i for i, b in enumerate(plan) if K.NOOP in b]
    if len(first) != 1:
        raise ToolError('無操作の入ったバッチがちょうど一つでない')
    order = first + [i for i in range(len(plan)) if i != first[0]]
    lo, mass, pa = {}, {}, {}
    lay = {'noop_lo': None, 'rows': {}, 'iso': collections.defaultdict(list)}
    noop_h = None
    for bi in order:
        ids_ = plan[bi]
        want_layers = any((d == K.NOOP) or (d in layer_dirs) or (keep_iso_layers and d.startswith('iso:')) for d in ids_)
        r = R.forward(cell, ids_, sign, want_layers=want_layers, full=True)
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
                u = float(sign) * R.torch.tensor(R.vec(d), device=R.dev).float()
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


def layer_summary(lay, band):
    """等方の帰無の層ごとの中央値と中央の区間（正本 `descriptive.layerwise`）。"""
    if not lay['iso']:
        return None
    A = np.array(list(lay['iso'].values()), dtype=np.float64)
    lo_q, hi_q = 100 * (1 - band) / 2, 100 * (1 + band) / 2
    return {'median': np.median(A, axis=0).tolist(), 'lo': np.percentile(A, lo_q, axis=0).tolist(), 'hi': np.percentile(A, hi_q, axis=0).tolist(), 'n': int(A.shape[0])}


def run_main_phase(R, C, cells, names, pilot, k, z0, iso_n=None, batch_override=None, log=print):
    """本の計算の全体（正本 `computation`・`readout.primary.batching`）: 頭の自己検査（出口の値・最後の層）→ 全ての升目と符号の組。近道は使わない。
    pilot: 本の凍結で凍結した読み取りの下見の記録（バッチの大きさ・外した升目）。names: {'named','iso','real'} の名の並び。
    iso_n は合成データの確かめで等方の本数を減らすときだけ使う。batch_override は道の違いの記述（バッチ 16 の道）だけに使う。
    戻り値: {'head': 頭の確かめ, 'cells': 組の鍵 → 出力, 'batch', 'dropped'}。log には組の鍵と時間だけを渡す（値は渡さない）。"""
    dropped = set((pilot.get('decision') or {}).get('dropped', []))
    batch = int(batch_override or pilot['batch'])
    items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in C['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
    head = collections.OrderedDict()
    if batch_override is None:
        head['logit_check'] = head_logit_checks(R, [cells[k_] for k_ in cells if k_ not in dropped], k, z0)
        head['layer_check'] = R.layer_check(items[0][0], items[0][1], 'check', C['computation']['layer_tol'])
        if not head['layer_check']['pass']:
            raise ToolError('最後の層の自己検査が落ちた（本の計算の頭）')
    iso = names['iso'] if iso_n is None else names['iso'][:iso_n]
    sets = cell_sign_sets(C, names['named'], iso, names['real'])
    layer_dirs = list(names['named'])
    band = C['descriptive']['layerwise']['band']
    out = collections.OrderedDict()
    t0 = time.time()
    for ki, (key, ck, sg, ds, main_cs) in enumerate(sets):
        if ck in dropped:
            continue
        o = run_cell_sign(R, cells[ck], sg, ds, batch, C['readout']['primary']['order_seed'], ki, layer_dirs=layer_dirs if main_cs else (), keep_iso_layers=main_cs)
        o['layers'] = {'noop_lo': o['layers']['noop_lo'], 'rows': o['layers']['rows'], 'iso_summary': layer_summary(o['layers'], band) if main_cs else None}
        out[key] = o
        log('[bprime_run] 升目と符号 %s（%d/%d）・%.0f 秒' % (key, ki + 1, len(sets), time.time() - t0))
    return {'head': head, 'cells': out, 'batch': batch, 'dropped': sorted(dropped)}


def recompute_hook_path(R, rows, dirs_by_row, log=None):
    """独立の再計算の本の器のフックの道（正本 `independent_recompute.new_paths` の一つ目・近道なし・バッチ一）。層三の `bl3_run.recompute_hook_path` と同じ。"""
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
            log('[bprime_run] 独立の再計算のフックの道 %s（%d/%d・順伝播 %d）・%.0f 秒' % (name, i + 1, len(rows), 1 + len(eff), time.time() - t0))
    return out


def build_cells(tok, C, ledger, keys):
    """升目の入力（凍結の組み立ての関数と台帳の書き出し）を作り、台帳のプロンプトの長さ・主位置・読み取りの位置・族・並びの SHA16 と突き合わせる（違えば止める）。"""
    import run_stageB_local as RB
    AT = RB.arm_texts()
    fam_letters = C['readout']['primary']['letters']
    heads = ledger['heads']
    out = collections.OrderedDict()
    for key in keys:
        sc, arm = key.split('|')
        scen, inst = RB.scenario_and_instruction(sc)
        prompt = G.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
        fam = scen['family']
        set_ids = [int(heads[x]['next']) for x in fam_letters[fam]] + [int(heads['refuse']['next'])]
        c = Cell(key, sc, arm, fam, prompt, ledger['prefix_ids'], set_ids, G.main_position(prompt))
        b = ledger['cells_main'][key]
        if (len(prompt), c.mp, c.ro, fam, set_ids) != (b['prompt_len'], b['main_position'], b['readout_position'], b['family'], b['set_ids']) or ids_sha16(c.ids) != b['ids_sha16']:
            raise ToolError('升目の入力が台帳と違う: %s' % key)
        out[key] = c
    return out


def load_dirs(npz_path, json_path, C):
    """方向の npz（`bprime_directions.py`）を名で引ける形にする。SHA-256 を記録と突き合わせ、名前のある方向の名の並びが正本と同じこと・組の本数を確かめる（違えば止める）。"""
    J = json.load(open(json_path, encoding='utf-8'))
    if hashlib.sha256(open(npz_path, 'rb').read()).hexdigest().upper() != J['npz_sha256']:
        raise ToolError('方向の npz の SHA-256 が記録と違う')
    if list(J['groups']['named']['names']) != list(C['directions']['named']):
        raise ToolError('方向の記録の名前のある方向の名の並びが正本と違う')
    if J['groups']['iso']['count'] != C['nulls']['isotropic']['count'] or len(J['groups']['real']['names']) != C['nulls']['real']['pairs']:
        raise ToolError('方向の組の本数が正本と違う')
    Z = np.load(npz_path)
    names = {'named': J['groups']['named']['names'], 'iso': ['iso:%d' % i for i in range(J['groups']['iso']['count'])],
             'real': ['real:' + p for p in J['groups']['real']['names']], 'check': ['check']}
    d = collections.OrderedDict()
    for g, ns in names.items():
        A = Z[g]
        if len(A) != len(ns):
            raise ToolError('方向の組の本数が記録と違う: %s' % g)
        for n, v in zip(ns, A):
            d[n] = np.asarray(v, dtype=np.float64)
    return d, names


if __name__ == '__main__':
    print(__doc__)
