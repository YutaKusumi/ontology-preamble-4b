# -*- coding: utf-8 -*-
"""bprime_run.py v0（2026-09-29・B′ の教師強制の順伝播の器・層三の `bl3_run.Runner` を Gemma 4 に移したもの・コーディネータ南無弥勒如来）。

層三からの変更（器の移しの下調べと、Gemma 4 のつくりによる）:
  - 層・最後の正規化・設定の道を Gemma 4 に合わせた（`bprime_gemma`）。
  - 読み取りに softcap を入れた（模型の出口と同じ式: cap × tanh(z / cap)）。質量（全語彙の softmax）も softcap の後の値で出す。
  - 近道（主位置より前の KV を使い回す）は置かない（transformers 5 に古い KV の API が無い・層三でも本の計算は近道を使わなかった）。
  - 加減のフックは段階 B の凍結の `run_stageB_local.make_hook` をそのまま使う（層の出力の形を両方扱う・行ごとの方向の行列を受ける）。
読み取り: 最終の正規化の入力（最後の層の出口の残差）を前のフックで取り、float32 に上げて正規化と語彙の行列の読み取りの集合の行を当て、softcap を掛ける。
層ごとの差分: 選んだ層の後の各層の出口をフックで取る（`hidden_states` は使わない——Gemma 4 では最後の要素が正規化の後の値になる）。
自己検査: 出口の値（読み取りの集合の float32 の値と模型の出口の値の差の最大）と最後の層（層ごとの差分の最後の層の行と読み取りの効き目の差）。
DRY のために壊した読み取りを引数 `bug` で入れられる（本の計算では入れない）: double_norm・no_softcap・hook_next_layer。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, math, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G          # 先に読む（凍結の器の置き場を sys.path に足す）
import bl3_core as K              # 凍結の層三の芯（対数オッズ・集合の中の確率・零と埋めの名）

VERSION = 'v0'
BUGS = (None, 'double_norm', 'no_softcap', 'hook_next_layer')


class ToolError(Exception):
    """凍結した確かめが機械で落ちた（器の誤り）。"""


def require_finite(vals, where):
    bad = [i for i, v in enumerate(np.ravel(vals)) if not math.isfinite(float(v))]
    if bad:
        raise ToolError('有限でない値（%s・%d 個）' % (where, len(bad)))


class Cell:
    """一つの升目（場面 × 土台の腕）の入力と位置（層三の `bl3_run.Cell` と同じ決まり）。"""

    def __init__(self, key, prompt_ids, prefix_ids, set_ids, main_position):
        self.key = key
        self.prompt = list(prompt_ids)
        self.ids = list(prompt_ids) + list(prefix_ids)
        self.mp = int(main_position)
        self.ro = len(self.ids) - 1
        self.set_ids = list(set_ids)
        if self.mp != len(self.prompt) - 1:
            raise ToolError('主位置がプロンプトの最後でない: %s' % key)


class Runner:
    def __init__(self, model, layer_idx, coef, dirs, bug=None):
        import torch
        import run_stageB_local as RB           # 凍結の段階 B の走行器（make_hook だけ使う）
        if bug not in BUGS:
            raise ValueError(bug)
        self.torch, self.RB, self.model, self.bug = torch, RB, model, bug
        self.layer, self.coef = int(layer_idx), float(coef)
        self.dev = next(model.parameters()).device
        self.eps = G.rms_eps(model)
        self.n_layers = G.n_layers(model)
        self.after = list(range(self.layer + 1, self.n_layers))
        self.g32 = G.final_norm(model).weight.detach().float()
        self.W32 = model.lm_head.weight.detach().float()
        self.cap = G.softcap(model)
        self.dirs = dirs
        self.dim = int(self.g32.shape[0])
        self._zero = np.zeros(self.dim, dtype=np.float32)
        self.n_forward = 0

    def vec(self, did):
        if did in (K.NOOP, K.PAD):
            return self._zero
        return np.asarray(self.dirs[did], dtype=np.float32)

    def norm32(self, h):
        h = h.float()
        return h * self.torch.pow(h.pow(2).mean(-1, keepdim=True) + self.eps, -0.5) * self.g32

    def capz(self, z):
        if self.cap is None or self.bug == 'no_softcap':
            return z
        return self.torch.tanh(z / self.cap) * self.cap

    def readout(self, h, set_ids, full=True):
        hn = self.norm32(h)
        if self.bug == 'double_norm':
            hn = self.norm32(hn)
        Zs_t = self.capz(hn @ self.W32[set_ids].T)
        Zs = Zs_t.double().cpu().numpy()
        out = {'Zset': Zs, 'lo': K.log_odds_a(Zs, 0, list(range(1, len(set_ids)))), 'pa': K.prob_a_in_set(Zs, 0, list(range(len(set_ids))))}
        if full:
            Zf = self.capz(hn @ self.W32.T).double()
            lse_f = self.torch.logsumexp(Zf, dim=-1)
            out['mass'] = self.torch.exp(self.torch.logsumexp(Zf[:, set_ids], dim=-1) - lse_f).cpu().numpy()
        return out

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
        r = self.readout(cap['h'], cell.set_ids, full=full)
        require_finite(r['Zset'], 'readout ' + cell.key)
        res = {'lo': r['lo'], 'pa': r['pa'], 'Zset': r['Zset']}
        if full:
            res['mass'] = r['mass']
        if want_model_logits:
            res['model_set_logits'] = out.logits[:, -1, :][:, cell.set_ids].float().double().cpu().numpy()
        if want_layers:
            res['layer_lo'] = {j: K.log_odds_a(self.capz(self.norm32(cap[j]) @ self.W32[cell.set_ids].T).double().cpu().numpy(), 0, list(range(1, len(cell.set_ids)))) for j in self.after}
        return res

    def logit_check(self, cell, tol):
        r = self.forward(cell, [K.NOOP], +1, want_model_logits=True, full=False)
        d = float(np.max(np.abs(r['Zset'] - r['model_set_logits'])))
        return {'cell': cell.key, 'max_abs': d, 'tol': tol, 'pass': d <= tol}

    def layer_check(self, cell, sign, did, tol):
        r = self.forward(cell, [K.NOOP, did], sign, want_layers=True, full=False)
        last = self.after[-1]
        eff_read = float(r['lo'][1] - r['lo'][0])
        eff_layer = float(r['layer_lo'][last][1] - r['layer_lo'][last][0])
        d = abs(eff_read - eff_layer)
        return {'cell': cell.key, 'sign': sign, 'direction': did, 'diff': d, 'tol': tol, 'pass': d <= tol}
