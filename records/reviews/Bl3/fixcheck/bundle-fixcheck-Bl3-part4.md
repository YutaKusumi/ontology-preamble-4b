（B-lens 層三の器の直しの確かめの束・分けた版 4／7・中身は一通版と同じ）

<<< 始: `tools/bl3_run.py`（SHA16 46071CD97AB10819・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """bl3_run.py v3 —— B-lens 層三（Bl3）の教師強制の順伝播を走らせる器（2026-09-25・正本 `readout.primary`・`pilot`・`computation`・`descriptive`）。
  3 | 
  4 | 走らせ方（正本のとおり・値は器の出力に置き、読みは付けない）:
  5 |   - 入力: 段階 B の組み立てのままのプロンプト（凍結の `steer_B.apply_chat`・`run_stageB_local.user_message`）の直後に、主の書き出し（設計事実の転記行 A の
  6 |     トークンの並び）を置く。主位置は凍結の `steer_B.main_position`、読み取りの位置は列の最後（主位置 ＋ 書き出しの長さ）。
  7 |   - 加減: 凍結の `run_stageB_local.make_hook`（行ごとの方向の行列を受ける形・層の出力の型に直して足す・係数は一度だけ）を、選んだ層（凍結の
  8 |     `direction_B.layer_index`）に凍結の `register_hook` で掛ける。帯は主位置から読み取りの位置まで。零のベクトルの行が無操作。
  9 |   - 近道: 主位置より前（添字 0〜主位置−1）の計算を加減なしで一度だけ作り、バッチの大きさに写して、主位置から後ろだけを流す（帯の起点は写した後の 0）。
 10 |     近道は下見の (v) の記述だけに使い、本の計算は近道を使わない（裁定 D234）。頭の近道の確かめ（正本 `computation.steered_cache_check`）は近道を使うときだけの確かめなので、関数を置かない。
 11 |   - 読み取り: 最終の正規化の入力（最後の層の出口の残差）を前の hook で取り、`float32` に上げて最終の正規化と語彙の行列の読み取りの集合の行を `float32` で当てる。
 12 |     全語彙の softmax は質量にだけ使う（`float32`）。層ごとの差分は、選んだ層の後の各層の出口の hook で取る（`hidden_states` は使わない）。
 13 |   - 自己検査: 出口の値（読み取りの集合の `float32` の出口の値と、模型そのものの出口の値〔bf16〕の差の最大・許容 `computation.logit_tol`）と、
 14 |     最後の層（層ごとの差分の最後の層の行と読み取りの効き目の差・許容 `computation.layer_tol`）。落ちたら止める（器の誤り・正本 `pilot.decision.tool_error`・
 15 |     `computation.tool_error`）。
 16 | 関数は Colab の起動器 `tools/colab/boot_Bl3.py` と合成データの器 `tools/dry_run_Bl3.py` が import して呼ぶ（この器だけでは模型を読まない）。
 17 | DRY（乱数の小さな模型）の確かめのために、壊した読み取り（二重の正規化）と壊した近道（主位置まで使い回す）を、引数 `bug` で入れられる（本の計算では入れない）。
 18 | 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 19 | """
 20 | import os, sys, json, math, time, hashlib, collections
 21 | import numpy as np
 22 | 
 23 | HERE = os.path.dirname(os.path.abspath(__file__))
 24 | sys.path.insert(0, HERE)
 25 | import bl3_core as K
 26 | 
 27 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 出口の値が有限でなければ止める・方向の名の並びを正本と転記行 D に照らす・升目のトークンの並びの SHA16／v2（裁定 D231・D234）: 本の計算は近道を使わない ほか
 28 | BUGS = (None, 'double_norm', 'cache_through_mp')
 29 | 
 30 | 
 31 | class ToolError(Exception):
 32 |     """凍結した確かめが機械で落ちた（器の誤り・正本 `pilot.decision.tool_error.what`）。"""
 33 | 
 34 | 
 35 | def require_finite(vals, where):
 36 |     """出口の値がすべて有限であること（有限でなければ器の誤りで止める・裁定 D236）。vals: 名 → 値。"""
 37 |     bad = sorted(k for k, v in vals.items() if not math.isfinite(float(v)))
 38 |     if bad:
 39 |         raise ToolError('有限でない値（%s・%d 個・例 %s）' % (where, len(bad), bad[:3]))
 40 | 
 41 | 
 42 | def ids_sha16(cell):
 43 |     """升目の入力のトークンの並び（プロンプト ＋ 主の書き出し）の SHA16（相 check が書き、凍結の器が手元の組み立てと照らす・裁定 D236）。"""
 44 |     return hashlib.sha256(','.join(str(int(x)) for x in cell.ids).encode('ascii')).hexdigest().upper()[:16]
 45 | 
 46 | 
 47 | class Cell:
 48 |     """一つの升目（場面 × 土台の腕）の入力と位置。"""
 49 | 
 50 |     def __init__(self, key, sc, arm, fam, prompt_ids, prefix_ids, set_ids, main_position):
 51 |         self.key, self.sc, self.arm, self.fam = key, sc, arm, fam
 52 |         self.prompt = list(prompt_ids)
 53 |         self.ids = list(prompt_ids) + list(prefix_ids)
 54 |         self.mp = int(main_position)
 55 |         self.ro = len(self.ids) - 1
 56 |         self.set_ids = list(set_ids)            # 選択の文字（族の順・a が先頭）と refuse の頭
 57 |         if self.mp != len(self.prompt) - 1:
 58 |             raise ToolError('主位置がプロンプトの最後でない: %s' % key)
 59 | 
 60 |     def with_prefix(self, prefix_ids):
 61 |         return Cell(self.key, self.sc, self.arm, self.fam, self.prompt, prefix_ids, self.set_ids, self.mp)
 62 | 
 63 | 
 64 | class Runner:
 65 |     def __init__(self, model, T3, layer_idx, coef, dirs, bug=None):
 66 |         import torch
 67 |         import run_stageB_local as RB
 68 |         if bug not in BUGS:
 69 |             raise ValueError(bug)
 70 |         self.torch, self.RB, self.model, self.T3 = torch, RB, model, T3
 71 |         self.layer, self.coef, self.bug = int(layer_idx), float(coef), bug
 72 |         self.dev = next(model.parameters()).device
 73 |         self.eps = float(model.config.rms_norm_eps)
 74 |         self.n_layers = int(model.config.num_hidden_layers)
 75 |         self.after = list(range(self.layer + 1, self.n_layers))
 76 |         self.g32 = model.model.norm.weight.detach().float()
 77 |         self.W32 = model.lm_head.weight.detach().float()
 78 |         self.dirs = dirs                      # 方向の名 → float64 の一本（無操作と埋めは零）
 79 |         self.dim = int(self.g32.shape[0])
 80 |         self._zero = np.zeros(self.dim, dtype=np.float32)
 81 |         self.n_forward = 0
 82 | 
 83 |     # ---- 方向 ----
 84 |     def vec(self, did):
 85 |         if did in (K.NOOP, K.PAD):
 86 |             return self._zero
 87 |         v = self.dirs[did]
 88 |         return np.asarray(v, dtype=np.float32)
 89 | 
 90 |     # ---- 正規化と読み取り（float32） ----
 91 |     def norm32(self, h):
 92 |         h = h.float()
 93 |         return h * self.torch.rsqrt(h.pow(2).mean(-1, keepdim=True) + self.eps) * self.g32
 94 | 
 95 |     def readout(self, h, cell, full=True):
 96 |         hn = self.norm32(h)
 97 |         if self.bug == 'double_norm':
 98 |             hn = self.norm32(hn)
 99 |         Zs = (hn @ self.W32[cell.set_ids].T).double().cpu().numpy()
100 |         out = {'Zset': Zs, 'lo': K.log_odds_a(Zs, 0, list(range(1, len(cell.set_ids)))), 'pa': K.prob_a_in_set(Zs, 0, list(range(len(cell.set_ids))))}
101 |         if full:
102 |             Zf = (hn @ self.W32.T).double()
103 |             lse_f = self.torch.logsumexp(Zf, dim=-1)
104 |             out['mass'] = self.torch.exp(self.torch.logsumexp(Zf[:, cell.set_ids], dim=-1) - lse_f).cpu().numpy()
105 |             out['Zfull'] = Zf
106 |         return out
107 | 
108 |     # ---- 近道の元（主位置より前・加減なし） ----
109 |     def prefix_cache(self, cell):
110 |         torch = self.torch
111 |         end = cell.mp + 1 if self.bug == 'cache_through_mp' else cell.mp
112 |         with torch.no_grad():
113 |             out = self.model(input_ids=torch.tensor([cell.ids[:end]], device=self.dev), use_cache=True, logits_to_keep=1)
114 |         self.n_forward += 1
115 |         return {'legacy': out.past_key_values.to_legacy_cache(), 'end': end}
116 | 
117 |     def _expand(self, pc, B):
118 |         from transformers.cache_utils import DynamicCache
119 |         return DynamicCache.from_legacy_cache(tuple((k.expand(B, *k.shape[1:]).contiguous(), v.expand(B, *v.shape[1:]).contiguous()) for k, v in pc['legacy']))
120 | 
121 |     # ---- 一回の順伝播（行ごとの方向・同じ升目・同じ符号） ----
122 |     def forward(self, cell, dir_ids, sign, pc=None, want_layers=False, want_model_logits=False, full=True):
123 |         """pc（近道の元）があれば近道、無ければ近道なし。戻り値: 行ごとの対数オッズ・集合の中の a の確率・質量・（あれば）層ごとの残差と対数オッズ・模型の出口の値。"""
124 |         torch, RB = self.torch, self.RB
125 |         B = len(dir_ids)
126 |         V = np.stack([self.vec(d) for d in dir_ids]).astype(np.float32)
127 |         if pc is None:
128 |             inp = torch.tensor([cell.ids] * B, device=self.dev)
129 |             starts = [cell.mp] * B
130 |             past = None
131 |         else:
132 |             if pc['end'] != cell.mp:        # 近道の元は主位置の手前で切る（主位置を帯に残す・凍結した確かめ・効き目の比べだけでは弱い: 合成の記録）
133 |                 raise ToolError('近道の元が主位置の手前で切れていない（%d・主位置 %d）: %s' % (pc['end'], cell.mp, cell.key))
134 |             n_cached = int(pc['legacy'][0][0].shape[-2])      # 記録した切れ目だけでなく、使い回す cache の列の実の長さも見る（裁定 D231）
135 |             if n_cached != cell.mp:
136 |                 raise ToolError('使い回す cache の列の長さが主位置と違う（%d・主位置 %d）: %s' % (n_cached, cell.mp, cell.key))
137 |             inp = torch.tensor([cell.ids[pc['end']:]] * B, device=self.dev)
138 |             starts = [0] * B
139 |             past = self._expand(pc, B)
140 |         cap, hs = {}, []
141 |         hs.append(self.model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone())))
142 |         if want_layers:
143 |             layers = self.model.model.layers
144 |             for j in self.after:
145 |                 hs.append(layers[j].register_forward_hook(lambda m, a, o, j=j: cap.__setitem__(j, (o[0] if isinstance(o, tuple) else o)[:, -1, :].detach().clone())))
146 |         handle = RB.register_hook(self.model, self.layer, RB.make_hook(V, self.coef, int(sign), starts, meta={'bl3': True, 'cell': cell.key}))
147 |         try:
148 |             with torch.no_grad():
149 |                 out = self.model(input_ids=inp, past_key_values=past, use_cache=past is not None, logits_to_keep=1)
150 |         finally:
151 |             handle.remove()
152 |             for h_ in hs:
153 |                 h_.remove()
154 |             RB.assert_no_hooks(self.model, self.layer)
155 |         self.n_forward += 1
156 |         r = self.readout(cap['h'], cell, full=full)
157 |         res = {'lo': r['lo'], 'pa': r['pa'], 'Zset': r['Zset']}
158 |         if full:
159 |             res['mass'] = r['mass']
160 |             res['Zfull'] = r['Zfull']
161 |         if want_model_logits:
162 |             res['model_set_logits'] = out.logits[:, -1, :][:, cell.set_ids].float().double().cpu().numpy()
163 |         if want_layers:
164 |             res['layers'] = {j: cap[j].float() for j in self.after}
165 |             res['layer_lo'] = {j: K.log_odds_a((self.norm32(cap[j]) @ self.W32[cell.set_ids].T).double().cpu().numpy(), 0, list(range(1, len(cell.set_ids)))) for j in self.after}
166 |         return res
167 | 
168 |     # ---- 自己検査 ----
169 |     def logit_check(self, cell, tol):
170 |         """出口の値の自己検査（正本 `computation.self_checks.logit`）: 無操作・近道なし・バッチ一。"""
171 |         r = self.forward(cell, [K.NOOP], +1, want_model_logits=True, full=False)
172 |         d = float(np.max(np.abs(r['Zset'] - r['model_set_logits'])))
173 |         return {'cell': cell.key, 'max_abs': d, 'tol': tol, 'pass': d <= tol}
174 | 
175 |     def layer_check(self, cell, sign, did, tol, pc=None):
176 |         """最後の層の自己検査（正本 `computation.self_checks.layer`）: 層ごとの差分の最後の層の行と、読み取りの効き目の差。"""
177 |         r = self.forward(cell, [K.NOOP, did], sign, pc=pc, want_layers=True, full=False)
178 |         last = self.after[-1]
179 |         eff_read = float(r['lo'][1] - r['lo'][0])
180 |         eff_layer = float(r['layer_lo'][last][1] - r['layer_lo'][last][0])
181 |         d = abs(eff_read - eff_layer)
182 |         return {'cell': cell.key, 'sign': sign, 'direction': did, 'diff': d, 'tol': tol, 'pass': d <= tol}
183 | 
184 | 
185 | # ---------------- 下見（無操作だけ） ----------------
186 | def run_pilot(R, cells_main, cells_gate_only, T3, variant_prefixes, stage_b_rate, sampling):
187 |     """正本 `pilot`: 出口の値の自己検査 → (vi) → (i)〜(iv) → (v) → 決め。値の記録と機械の決定を返す（読みは付けない）。"""
188 |     P = T3['pilot']
189 |     batch_default = T3['readout']['primary']['batch']
190 |     rec = collections.OrderedDict(version=VERSION)
191 |     lc = R.logit_check(cells_main[0], T3['computation']['logit_tol'])
192 |     rec['logit_check'] = lc
193 |     if not lc['pass']:
194 |         raise ToolError('出口の値の自己検査が落ちた: %s' % lc)
195 |     # (vi) (a) 零のベクトルだけで満たしたバッチ（全ての位置）と大きさ一 ・ (b) 大きさ一の繰り返し
196 |     a_vals, b_vals, first16 = {}, {}, {}
197 |     for c in cells_main:
198 |         r16 = R.forward(c, [K.NOOP] * batch_default, +1, full=False)
199 |         r1 = R.forward(c, [K.NOOP], +1, full=False)
200 |         a_vals[c.key] = list(map(float, r16['lo'])) + [float(r1['lo'][0])]
201 |         first16[c.key] = float(r16['lo'][0])
202 |         b_vals[c.key] = [float(r1['lo'][0])] + [float(R.forward(c, [K.NOOP], +1, full=False)['lo'][0]) for _ in range(P['repeat_n'] - 1)]
203 |     sa = max(K.spread(v) for v in a_vals.values())
204 |     sb = max(K.spread(v) for v in b_vals.values())
205 |     vi = K.vi_decision(sa, sb, P['noise_max'], batch_default)
206 |     rec['vi'] = {'a': {k: K.spread(v) for k, v in a_vals.items()}, 'b': {k: K.spread(v) for k, v in b_vals.items()}, 'decision': vi}
207 |     if vi['stop']:
208 |         rec['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
209 |         return rec
210 |     batch = vi['batch']
211 |     tol = K.cache_tol(vi['floor'], P['cache_tol_factor'], P['cache_tol_floor'], P['noise_max'])
212 |     rec['batch'], rec['floor'], rec['cache_tol'] = batch, vi['floor'], tol
213 | 
214 |     def noop_at_config(c, prefix=None):
215 |         cc = c if prefix is None else c.with_prefix(prefix)
216 |         r = R.forward(cc, [K.NOOP] * batch, +1, full=True)
217 |         return {'lo': float(r['lo'][0]), 'pa': float(r['pa'][0]), 'mass': float(r['mass'][0]), 'Zfull0': r['Zfull'][0].cpu().numpy()}
218 |     # (i)(ii)(iii)
219 |     cells_all = list(cells_main) + list(cells_gate_only)
220 |     nv = {c.key: noop_at_config(c) for c in cells_all}
221 |     ok_main = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], P['mass_min'], P['p_bounds']) for c in cells_main}
222 |     ok_gate = {c.key: K.pass_i_ii(nv[c.key]['mass'], nv[c.key]['pa'], P['mass_min'], P['p_bounds']) for c in cells_gate_only}
223 |     import blens_core as C
224 |     pT = {}
225 |     for c in cells_main:
226 |         pt = C.transform(nv[c.key]['Zfull0'], sampling['temperature'], sampling['top_k'], sampling['top_p'])
227 |         pT[c.key] = float(pt[c.set_ids[0]])
228 |     raw = [nv[c.key]['pa'] for c in cells_main]
229 |     obs = [stage_b_rate[c.key] for c in cells_main]
230 |     rho = C.spearman(raw, obs)
231 |     rec['cells'] = {c.key: {'lo': nv[c.key]['lo'], 'pa': nv[c.key]['pa'], 'mass': nv[c.key]['mass'], 'pa_transformed': pT.get(c.key), 'stage_b_rate': stage_b_rate.get(c.key),
232 |                             'pass_i_ii': (ok_main if c in cells_main else ok_gate)[c.key], 'main': c in cells_main} for c in cells_all}
233 |     rec['iii'] = {'rho': rho, 'n': len(raw), 'sentence': K.iii_sentence(rho), 'transformed_def': P['checks']['iii']['transformed_def']}      # 変換を通した値の定義を記録にも置く（裁定 D231・D235）
234 |     # (iv) 揺れの版
235 |     iv = {}
236 |     for name, pref in variant_prefixes.items():
237 |         lv = {c.key: noop_at_config(c, pref)['lo'] for c in cells_main}
238 |         iv[name] = {'lo': lv, 'flags': K.variant_flags({c.key: nv[c.key]['lo'] for c in cells_main}, lv, P['variant_flag'])}
239 |     rec['iv'] = iv
240 |     # (v) 近道（主の升目と門の行だけの升目）
241 |     diffs = {}
242 |     for c in cells_all:
243 |         pc = R.prefix_cache(c)
244 |         r = R.forward(c, [K.NOOP] * batch, +1, pc=pc, full=False)
245 |         diffs[c.key] = float(r['lo'][0]) - nv[c.key]['lo']
246 |     rec['v'] = {'diffs': diffs, 'tol': tol, 'shortcut': K.shortcut_ok(list(diffs.values()), tol)}
247 |     cd = K.cells_decision(ok_main, ok_gate, P['decision']['cells_min_pass'])
248 |     rec['decision'] = cd
249 |     rec['n_forward'] = R.n_forward
250 |     return rec
251 | 
252 | 
253 | # ---------------- 本の計算 ----------------
254 | def cell_sign_sets(T3, cells_by_key, named, b3, iso, real, gate_only_cells):
255 |     """升目と符号ごとの方向の集まり（正本 `readout.primary.batching`・転記行 E の組み立て）。戻り値: [(升目と符号の鍵, 升目, 符号, 方向の名の並び)]。"""
256 |     main = [(sc, base, int(sg)) for sc, base, sg in T3['cell_signs_main']]
257 |     out = []
258 |     for sc, base, sg in main:
259 |         out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(b3) + list(iso) + list(real)))
260 |     for key in gate_only_cells:
261 |         sc, base, sg = key
262 |         out.append(('%s|%s|%+d' % (sc, base, sg), '%s|%s' % (sc, base), sg, list(named) + list(b3)))
263 |     for sc, base, sg in main:
264 |         if (sc, base, -sg) not in main:
265 |             out.append(('%s|%s|%+d' % (sc, base, -sg), '%s|%s' % (sc, base), -sg, list(real)))
266 |     keys = [o[0] for o in out]
267 |     assert len(keys) == len(set(keys))
268 |     return out
269 | 
270 | 
271 | def run_cell_sign(R, cell, sign, dir_ids, batch, seed, key_index, pc=None, layer_dirs=(), keep_iso_layers=True):
272 |     """一つの升目と符号の全ての方向（零のベクトルの無操作を含む・端数は零のベクトルで埋める）。無操作の入ったバッチを先に流す（層ごとの差分のため）。"""
273 |     plan = K.batch_plan(dir_ids, batch, seed, key_index)
274 |     first = [i for i, b in enumerate(plan) if K.NOOP in b]
275 |     assert len(first) == 1
276 |     order = first + [i for i in range(len(plan)) if i != first[0]]
277 |     lo, mass, pa = {}, {}, {}
278 |     lay = {'noop_lo': None, 'rows': {}, 'iso': collections.defaultdict(list)}
279 |     noop_h = None
280 |     for bi in order:
281 |         ids_ = plan[bi]
282 |         want_layers = any((d == K.NOOP) or (d in layer_dirs) or (keep_iso_layers and d.startswith('iso:')) for d in ids_)
283 |         r = R.forward(cell, ids_, sign, pc=pc, want_layers=want_layers, full=True)
284 |         for k_, d in enumerate(ids_):
285 |             if d == K.PAD:
286 |                 continue
287 |             lo[d], mass[d], pa[d] = float(r['lo'][k_]), float(r['mass'][k_]), float(r['pa'][k_])
288 |         if want_layers:
289 |             if noop_h is None:
290 |                 k0 = ids_.index(K.NOOP)
291 |                 noop_h = {j: r['layers'][j][k0].clone() for j in R.after}
292 |                 lay['noop_lo'] = {j: float(r['layer_lo'][j][k0]) for j in R.after}
293 |             for k_, d in enumerate(ids_):
294 |                 if d in (K.PAD, K.NOOP) or not ((d in layer_dirs) or (keep_iso_layers and d.startswith('iso:'))):
295 |                     continue
296 |                 u = float(sign) * R.torch.tensor(R.vec(d), device=R.dev).float()      # 足した向き（符号を掛けた方向）との余弦（正本 `descriptive.layerwise.values`・裁定 D231）
297 |                 vals = []
298 |                 for j in R.after:
299 |                     dh = r['layers'][j][k_] - noop_h[j]
300 |                     nrm = float(dh.norm())
301 |                     cos = float((dh @ u) / (dh.norm() * u.norm())) if nrm > 0 else 0.0
302 |                     vals.append((nrm, cos, float(r['layer_lo'][j][k_]) - lay['noop_lo'][j]))
303 |                 if d in layer_dirs:
304 |                     lay['rows'][d] = vals
305 |                 else:
306 |                     lay['iso'][d] = vals
307 |     require_finite(lo, '升目と符号 %s|%+d の対数オッズ' % (cell.key, sign))
308 |     require_finite(mass, '升目と符号 %s|%+d の質量' % (cell.key, sign))
309 |     require_finite(pa, '升目と符号 %s|%+d の集合の中の確率' % (cell.key, sign))
310 |     eff = {d: lo[d] - lo[K.NOOP] for d in lo if d != K.NOOP}
311 |     return {'lo': lo, 'effects': eff, 'mass': mass, 'pa_noop': pa[K.NOOP], 'layers': lay, 'n_batches': len(plan)}
312 | 
313 | 
314 | def recompute_hook_path(R, rows, dirs_by_row, log=None):
315 |     """独立の再計算の本の器のフックの道（正本 `independent_recompute.new_paths` の一つ目・近道なし・バッチ一）。
316 |     rows: [(行の名, 升目, 符号)]・dirs_by_row: 行の名 → [(方向の名, 符号)]（比べる相手の逆の向きは符号を反転して流す）。戻り値: 行の名 → {'noop_lo', 'effects': {'方向の名|符号': 効き目}}。
317 |     log があれば、行ごとに行の名と順伝播の数と時間だけを渡す（値は渡さない）。"""
318 |     out = {}
319 |     t0 = time.time()
320 |     for i, (name, cell, sign) in enumerate(rows):
321 |         base = float(R.forward(cell, [K.NOOP], sign, full=False)['lo'][0])
322 |         eff = {}
323 |         for did, sg in dirs_by_row[name]:
324 |             eff['%s|%+d' % (did, sg)] = float(R.forward(cell, [did], sg, full=False)['lo'][0]) - base
325 |         require_finite(dict(eff, noop=base), '独立の再計算のフックの道の行 %s' % name)
326 |         out[name] = {'noop_lo': base, 'effects': eff}
327 |         if log:
328 |             log('[bl3_run] 独立の再計算のフックの道 %s（%d/%d・順伝播 %d）・%.0f 秒' % (name, i + 1, len(rows), 1 + len(eff), time.time() - t0))
329 |     return out
330 | 
331 | 
332 | def build_cells(tok, T3, FJ, keys):
333 |     """升目の入力（凍結の組み立ての関数と転記行 A の書き出し）を作り、転記行 B のプロンプトの長さ・主位置・読み取りの位置と突き合わせる（違えば止める）。"""
334 |     import steer_B
335 |     import run_stageB_local as RB
336 |     AT = RB.arm_texts()
337 |     A, B = FJ['facts']['A'], FJ['facts']['B']['cells']
338 |     L = A['letter_ids']
339 |     fam_letters = T3['readout']['primary']['letters']
340 |     out = collections.OrderedDict()
341 |     for key in keys:
342 |         sc, arm = key.split('|')
343 |         scen, inst = RB.scenario_and_instruction(sc)
344 |         prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
345 |         fam = scen['family']
346 |         set_ids = [int(L[x]) for x in fam_letters[fam]] + [int(L['refuse'])]
347 |         c = Cell(key, sc, arm, fam, prompt, A['prefix_ids'], set_ids, steer_B.main_position(prompt))
348 |         b = B[key]
349 |         if (len(prompt), c.mp, c.ro, fam) != (b['prompt_len'], b['main_position'], b['readout_position'], b['family']):
350 |             raise ToolError('升目の入力が転記行 B と違う: %s' % key)
351 |         out[key] = c
352 |     return out
353 | 
354 | 
355 | def load_dirs(npz_path, json_path, T3=None, FJ=None):
356 |     """方向の npz（`tools/bl3_directions.py`）を名で引ける形にする。SHA-256 は記録と突き合わせる（違えば止める）。
357 |     T3 と FJ を与えると、名前のある方向の名の並びが正本と、実在の差の名の並びが転記行 D と同じことも確かめる（名と行を位置で結ぶので・裁定 D236）。"""
358 |     import hashlib
359 |     J = json.load(open(json_path, encoding='utf-8'))
360 |     if hashlib.sha256(open(npz_path, 'rb').read()).hexdigest().upper() != J['npz_sha256']:
361 |         raise ToolError('方向の npz の SHA-256 が記録と違う')
362 |     if T3 is not None and list(J['groups']['named']['names']) != list(T3['directions']['named']):
363 |         raise ToolError('方向の記録の名前のある方向の名の並びが正本と違う')
364 |     if FJ is not None and list(J['groups']['real']['names']) != list(FJ['facts']['D']['real_pairs']):
365 |         raise ToolError('方向の記録の実在の差の名の並びが転記行 D と違う')
366 |     Z = np.load(npz_path)
367 |     names = {'named': J['groups']['named']['names'], 'B_random': J['groups']['B_random']['names'],
368 |              'iso': ['iso:%d' % i for i in range(J['groups']['iso']['count'])], 'real': ['real:' + p for p in J['groups']['real']['names']], 'check': ['check']}
369 |     d = collections.OrderedDict()
370 |     for g, ns in names.items():
371 |         A = Z[g]
372 |         if len(A) != len(ns):
373 |             raise ToolError('方向の組の本数が記録と違う: %s' % g)
374 |         for n, v in zip(ns, A):
375 |             d[n] = np.asarray(v, dtype=np.float64)
376 |     return d, names
377 | 
378 | 
379 | def secondary_contexts(tok, T3, FJ, FB, repo):
380 |     """乙の文脈（正本 `readout.secondary`・裁定 D227）: B-lens の層二で選んだ出力（B-lens の設計事実の転記行 E の `selected`・一覧の SHA16 を確かめる）の、
381 |     プロンプトと出力の選択の文字を覆うトークンの前までの教師強制の入力（凍結の `boot_Blens.context_of`）。戻り値: [(層の鍵, 試行の番号, 升目の入力, 文脈の記録)]。"""
382 |     import hashlib, glob
383 |     import steer_B
384 |     import run_stageB_local as RB
385 |     sys.path.insert(0, os.path.join(HERE, 'colab'))
386 |     import boot_Blens as BOOT
387 |     E = FB['facts']['E']
388 |     sel = E['selected']
389 |     if hashlib.sha256(json.dumps(sel, sort_keys=True).encode('utf-8')).hexdigest().upper()[:16] != E['selected_sha16']:
390 |         raise ToolError('乙の文脈の一覧の SHA16 が B-lens の設計事実と違う')
391 |     AT = RB.arm_texts()
392 |     L = FJ['facts']['A']['letter_ids']
393 |     fam_letters = T3['readout']['primary']['letters']
394 |     out = []
395 |     for key, ids_ in sel.items():
396 |         sc, arm, style = key.split('|')
397 |         scen, inst = RB.scenario_and_instruction(sc)
398 |         prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
399 |         d = os.path.join(repo, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
400 |         ft, fr = glob.glob(os.path.join(d, 'trials-*.jsonl')), glob.glob(os.path.join(d, 'raw-*.jsonl'))
401 |         if len(ft) != 1 or len(fr) != 1:
402 |             raise ToolError('段階 B の試行の記録か出力の記録がちょうど一つでない: %s（%d・%d）' % (d, len(ft), len(fr)))
403 |         tr = {json.loads(l)['trial_id']: json.loads(l) for l in open(ft[0], encoding='utf-8')}
404 |         rw = {json.loads(l)['trial_id']: json.loads(l) for l in open(fr[0], encoding='utf-8')}
405 |         fam = scen['family']
406 |         set_ids = [int(L[x]) for x in fam_letters[fam]] + [int(L['refuse'])]
407 |         for tid in ids_:
408 |             try:
409 |                 cx = BOOT.context_of(tok, prompt, tr[tid], rw[tid], AT[arm]['sha16'], steer_B.main_position)
410 |             except BOOT.Stop as e_:
411 |                 raise ToolError('乙の文脈を組めない: %s' % e_)
412 |             cell = Cell('%s|%s' % (sc, arm), sc, arm, fam, prompt, cx['ids'][len(prompt):], set_ids, steer_B.main_position(prompt))
413 |             rec = {'stratum': key, 'trial_id': tid, 'choice': cx['choice'], 'letter_token': cx['letter_token'],
414 |                    'letter_token_is_L': cx['letter_token'] == int(L.get(cx['choice'], -1)), 'n_ids': len(cx['ids'])}
415 |             out.append((key, tid, cell, rec))
416 |     return out
417 | 
418 | 
419 | def run_secondary(R, contexts, rows_by_cell, log=None):
420 |     """乙（正本 `descriptive.secondary_readout`・裁定 D227）: 文脈ごとに、その升目の門の行（名前のある方向と段階 B の三本）の方向を、行の符号で加える（近道なし）。
421 |     符号ごとに零のベクトルの無操作と同じバッチに流す。戻り値: 文脈ごとに、行の名 → 対数オッズの変化と、選択肢 a と c の文字の出口の値の変化。
422 |     log があれば、文脈ごとに層の鍵と試行の番号と時間だけを渡す（値は渡さない）。"""
423 |     out = []
424 |     t0 = time.time()
425 |     for ci, (key, tid, cell, rec) in enumerate(contexts):
426 |         if log:
427 |             log('[bl3_run] 乙 %s %s（%d/%d）・%.0f 秒' % (key, tid, ci + 1, len(contexts), time.time() - t0))
428 |         rows = rows_by_cell.get(cell.key, [])
429 |         by_sign = collections.OrderedDict()
430 |         for name, did, sg in rows:
431 |             by_sign.setdefault(sg, []).append((name, did))
432 |         i_c = 2                                                      # 読み取りの集合は族の選択の文字の順（a・b・c…）で、c は三つ目
433 |         res = {}
434 |         for sg, items in by_sign.items():
435 |             r = R.forward(cell, [K.NOOP] + [d for _, d in items], sg, full=False)
436 |             for k_, (name, did) in enumerate(items, start=1):
437 |                 res[name] = {'dlo': float(r['lo'][k_] - r['lo'][0]), 'dz_a': float(r['Zset'][k_, 0] - r['Zset'][0, 0]), 'dz_c': float(r['Zset'][k_, i_c] - r['Zset'][0, i_c])}
438 |         require_finite({'%s|%s' % (n_, k_): v_ for n_, d_ in res.items() for k_, v_ in d_.items()}, '乙の文脈 %s %s' % (key, tid))
439 |         out.append(dict(rec, rows=res, n_batches=len(by_sign)))
440 |     return out
441 | 
442 | 
443 | def run_main_phase(R, T3, FJ, cells, names, pilot, iso_n=None, log=print):
444 |     """本の計算の全体（正本 `computation`・`readout.primary.batching`）: 頭の自己検査（出口の値・最後の層）→ 全ての升目と符号。本の計算は近道を使わない（裁定 D234・
445 |     下見の (v) は記述として残す）ので、頭の近道の確かめは走らせない（正本 `computation.steered_cache_check` は「近道を使うときだけ」）。
446 |     pilot: 本の凍結で凍結した下見の記録（バッチの大きさ・揺れの床・近道の許容・近道・外した升目）。names: {'named','B_random','iso','real'} の名の並び。
447 |     iso_n は合成データの確かめで等方の本数を減らすときだけ使う。戻り値: {'head': 頭の確かめ, 'cells': 升目と符号の鍵 → 出力}。
448 |     層ごとの差分は、名前のある方向と段階 B の三本の行と、等方の帰無の層ごとの中央値と中央の区間だけを残す（正本 `descriptive.layerwise.directions`）。"""
449 |     dropped = set((pilot.get('decision') or {}).get('dropped', []))
450 |     batch = pilot['batch']
451 |     main_keys = ['%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']]
452 |     items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in T3['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
453 |     head = collections.OrderedDict()
454 |     head['logit_check'] = R.logit_check(items[0][0], T3['computation']['logit_tol'])
455 |     if not head['logit_check']['pass']:
456 |         raise ToolError('出口の値の自己検査が落ちた（本の計算の頭）: %s' % head['logit_check'])
457 |     shortcut = False                                                    # 本の計算は近道を使わない（裁定 D234）
458 |     head['shortcut'] = shortcut
459 |     head['shortcut_rule'] = '本の計算は近道を使わない（裁定 D234）・下見の (v) の近道: %s（記述）' % (pilot.get('v') or {}).get('shortcut')
460 |     head['layer_check'] = R.layer_check(items[0][0], items[0][1], 'check', T3['computation']['layer_tol'])
461 |     if not head['layer_check']['pass']:
462 |         raise ToolError('最後の層の自己検査が落ちた（本の計算の頭）: %s' % head['layer_check'])
463 |     iso = names['iso'] if iso_n is None else names['iso'][:iso_n]
464 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
465 |     sets = cell_sign_sets(T3, None, names['named'], names['B_random'], iso, names['real'], gate_only)
466 |     layer_dirs = list(names['named']) + list(names['B_random'])
467 |     band = T3['descriptive']['layerwise']['band']
468 |     out = collections.OrderedDict()
469 |     t0 = time.time()
470 |     for ki, (key, ck, sg, ds) in enumerate(sets):
471 |         if ck in dropped:
472 |             continue
473 |         main_cs = key in main_keys
474 |         pc = R.prefix_cache(cells[ck]) if shortcut else None
475 |         o = run_cell_sign(R, cells[ck], sg, ds, batch, T3['readout']['primary']['order_seed'], ki, pc=pc, layer_dirs=layer_dirs if main_cs else (), keep_iso_layers=main_cs)
476 |         o['layers'] = {'noop_lo': o['layers']['noop_lo'], 'rows': o['layers']['rows'], 'iso_summary': layer_summary(o['layers'], band) if main_cs else None}
477 |         out[key] = o
478 |         log('[bl3_run] 升目と符号 %s（%d/%d）・%.0f 秒' % (key, ki + 1, len(sets), time.time() - t0))
479 |     return {'head': head, 'cells': out, 'batch': batch, 'shortcut': shortcut, 'dropped': sorted(dropped)}
480 | 
481 | 
482 | def layer_summary(lay, band):
483 |     """等方の帰無の層ごとの中央値と中央の区間（正本 `descriptive.layerwise.directions`・`band`）。"""
484 |     if not lay['iso']:
485 |         return None
486 |     A = np.array(list(lay['iso'].values()), dtype=np.float64)       # 方向 × 層 × 三つ
487 |     lo_q, hi_q = 100 * (1 - band) / 2, 100 * (1 + band) / 2
488 |     return {'median': np.median(A, axis=0).tolist(), 'lo': np.percentile(A, lo_q, axis=0).tolist(), 'hi': np.percentile(A, hi_q, axis=0).tolist(), 'n': int(A.shape[0])}
489 | 
490 | 
491 | if __name__ == '__main__':
492 |     print(__doc__)
```
<<< 終: `tools/bl3_run.py` >>>

<<< 始: `tools/colab/boot_Bl3.py`（SHA16 6E210F2613E12DD1・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """boot_Bl3.py v3 —— B-lens 層三（Bl3）の Colab 起動スクリプト（教師強制の順伝播・2026-09-25・正本 `readout`・`pilot`・`computation`・`independent_recompute`）。
  3 | 
  4 | 相（OP4B_PHASE）:
  5 |   check  封印の前の確かめ（正本 `computation.before_seal`: 読み込みと版の確かめだけ・**順伝播を一度も走らせない・値を出さない**。模型の順伝播の前の hook で、呼ばれたら止める）:
  6 |          コミット固定の取り出し・版（正本 `inputs.versions_B`・文字列の完全な一致・torch は CUDA の組みまで・裁定 D187）・GPU・重みの断片の SHA-256（転記行 F）・
  7 |          方向の npz の SHA-256（方向の記録）と組ごとの SHA-256（転記行 D）・模型の読み込みと設定（正本 `inputs.model`）・選んだ層の添字（正本 `layers.indices`）・
  8 |          升目の入力（実トークナイザの組み立てを転記行 B と）・升目と符号の組と独立の再計算の組の順伝播の数（転記行 E と）・門の行（転記行 C の数と）・
  9 |          乙の行と文脈（B-lens の選んだ出力の一覧の SHA16 と、全ての文脈を組めること）・加減の hook を掛けて外せること・残差の書き換えの器が import できること。
 10 |   pilot  封印の後: 下見の前の凍結の記録と封印の記録がそろったコミットで、凍結の記録の SHA16 を取り出した器と正本に照らしてから、正本 `pilot.order` の順に走らせ、
 11 |          下見の記録（`bl3_run.run_pilot` の出力）を置く。器の誤り（凍結した確かめが機械で落ちた）は、その文を記録に置いて止める（正本 `pilot.decision.tool_error`）。
 12 |   main   本の凍結の後: 凍結の記録に足した下見の記録（バッチの大きさ・揺れの床・近道の許容・近道・外した升目）のまま、組（OP4B_PART・既定は三つとも順に）を走らせる:
 13 |            main       本の計算の頭（出口の値・最後の層）→ 全ての升目と符号（`bl3_run.run_main_phase`・近道を使わない・裁定 D234）
 14 |            recompute  独立の再計算の二つの道（本の器のフック〔`bl3_run.recompute_hook_path`〕・残差の書き換え〔別の個体の器 `bl3_recompute_rewrite`〕・近道なし・バッチ一）
 15 |            secondary  乙（`bl3_run.run_secondary`・裁定 D227）
 16 |          どの組も頭で出口の値の自己検査を走らせる。**効き目の値は印字しない**（札・門・二段の一致は手元の集計の器が出し、一致か不一致かだけを先に見る・正本
 17 |          `independent_recompute.print`）。器の誤りは、その文を組の出力に置いて止める（正本 `computation.tool_error`）。組の出力は出来たときに置く。
 18 | 止める条件（外れたら止める・登録者に相談）: 版の不一致（入れ直した後にランタイムの再起動を求める）・GPU・重みの SHA-256・方向の npz の SHA-256・凍結の記録の SHA16 と
 19 |   取り出した器と正本の不一致・取り出した作業木の変更・模型の設定・升目の入力と転記行 B の不一致・順伝播の数と転記行 E の不一致・乙の文脈を組めない・凍結と封印の記録の欠け・器の誤り。
 20 | 運用: コーディネータが登録者の Chrome 越しに Colab を操作する（ランタイムの選択と結果の zip のダウンロードもコーディネータ）。登録者の手に残すのは同意と支払い。
 21 |   資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。Drive は使わない（出力は小さく、終わりに zip を落とす）。セルの出力の表示が固まることがあるので、
 22 |   進みは出力の置き場の `progress.log` にも書く（ターミナルで見る）。ランタイムが落ちたら、落ちた組から新しいランタイムで走らせ直す（同じ GPU の種類・逸脱の台帳に記す）。
 23 | セルに打つ一行（先頭の下線は type の事故の緩衝・<commit> は 40 桁・相 main の組を分けるときは OP4B_PART を足す）:
 24 |   ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='check';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_Bl3.py').read())
 25 | DRY（手元の検査・OP4B_DRY=1）: 乱数の小さな模型（`tools/dry_run_Bl3.py` の作り方と読み取りの集合の行の置き直し）と実トークナイザ・合成の方向（実の名だけを借りる）で、
 26 |   三つの相を CPU で通す。OP4B_REPO_DIR・OP4B_OUT が要る。版・GPU・重み・凍結と封印の記録は見ない（印を残す）。方向の npz の確かめは手元の npz で行う。
 27 |   相 main は OP4B_DRY_PILOT（相 pilot の出力の pilot.json）を読む。OP4B_DRY_ISO で等方の本数（既定 9）、OP4B_DRY_SEC で乙の文脈の数（既定 2）、
 28 |   OP4B_DRY_RC で独立の再計算の v̂ の行の数（既定 2・減算の行と加算の行を一つずつから）を減らす。残差の書き換えの器が無ければ、DRY に限り印を残して飛ばす。
 29 | v3 の決め（裁定 D236）: 手順の順は「方向の npz と器を push → 相 check → 下見の前の凍結の記帳」（npz が取り出しに無ければ止める）。版は numpy・torch・transformers の三つを
 30 |   文字列で照らす（計算の道は scipy を読まないので照らさない・session に並べる・裁定 D237）。相 check の守りは模型・模型の本体・語彙の行列・各層の前の hook で、呼ばれた数を数えて
 31 |   書く（守りの止めは Exception の外の型）。相 pilot と main は、そのコミットの二つの予想の SHA-256 を封印の記録と照らす。相 main は組ごとに出力の SHA-256 を session に書き、
 32 |   組ごとに zip を作って落とす（落ちた組から走らせ直せるように）。止めと予期しない誤りでも session を書いて zip を作る。
 33 | 柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 34 | """
 35 | import os, sys, re, json, time, glob, shutil, hashlib, datetime, traceback, subprocess, zipfile, collections
 36 | 
 37 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 封印した予想の照らし・組の出力の SHA-256・組ごとの zip・止めと誤りの記録・相 check の守りと数・トークンの並びの SHA16 ほか／v2（裁定 D231・D234）
 38 | T0 = time.time()
 39 | REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
 40 | PHASES = ('check', 'pilot', 'main')
 41 | PARTS = ('main', 'recompute', 'secondary')
 42 | SPARSE = ['tools', 'arms', 'design', 'records', 'results/Bl3', 'results/stageB']
 43 | LOG = []
 44 | PROGRESS = {'path': None}
 45 | CTX = {'od': None, 'session': None, 'dry': False}          # 止めと誤りでも記録を置くため（裁定 D236）
 46 | CLAUSE = '本記録は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
 47 | now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
 48 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 49 | 
 50 | 
 51 | class Stop(BaseException):
 52 |     """相 check の守りの止め（Exception の外の型で、`except Exception` に呑まれない・裁定 D236）。"""
 53 | 
 54 | 
 55 | def sha256f(p):
 56 |     h = hashlib.sha256()
 57 |     with open(p, 'rb') as fh:
 58 |         for blk in iter(lambda: fh.read(1 << 24), b''):
 59 |             h.update(blk)
 60 |     return h.hexdigest().upper()
 61 | 
 62 | 
 63 | def say(line):
 64 |     print(line, flush=True)
 65 |     if PROGRESS['path']:
 66 |         with open(PROGRESS['path'], 'a', encoding='utf-8') as fh:
 67 |             fh.write(line + '\n')
 68 | 
 69 | 
 70 | def mark(step, **kw):
 71 |     LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
 72 |     say('[boot_Bl3] %-16s %7.0fs %s' % (step, time.time() - T0, kw or ''))
 73 | 
 74 | 
 75 | def sh(cmd, check=True):
 76 |     r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
 77 |     if check and r.returncode != 0:
 78 |         print(r.stdout[-2000:]); print(r.stderr[-3000:])
 79 |         raise RuntimeError('失敗: %s' % cmd)
 80 |     return r
 81 | 
 82 | 
 83 | def package(tag, extra=None):
 84 |     """置き場の中身を zip にして落とす（組ごと・終わり・止め・誤り・裁定 D236）。session を書いてから zip にし、zip の SHA-256 を session と進みの印字に記す。"""
 85 |     od, S = CTX['od'], CTX['session']
 86 |     if not od or S is None:
 87 |         return None
 88 |     S.update(extra or {})
 89 |     S.update({'log': LOG, 'packaged': tag, 'packaged_at': now(), 'seconds': round(time.time() - T0, 1), 'clause': CLAUSE})
 90 |     write_json(os.path.join(od, 'session.json'), S)
 91 |     zp = od + ('.zip' if tag == 'final' else '-%s.zip' % tag)
 92 |     with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
 93 |         for fn in sorted(os.listdir(od)):
 94 |             z.write(os.path.join(od, fn), os.path.join(os.path.basename(od), fn))
 95 |     zsha = sha256f(zp)
 96 |     S.setdefault('zips', []).append({'tag': tag, 'zip': os.path.basename(zp), 'sha256': zsha})
 97 |     mark('packaged', tag=tag, zip=os.path.basename(zp), sha256=zsha)
 98 |     if not CTX['dry']:
 99 |         try:
100 |             from google.colab import files
101 |             files.download(zp)
102 |         except Exception as e_:
103 |             print('[boot_Bl3] zip の自動のダウンロードが走らなかった（左の「ファイル」から落とす）: %s' % e_)
104 |     return zp
105 | 
106 | 
107 | def stop(msg):
108 |     mark('stop', reason=msg)
109 |     package('stopped', {'stopped': msg})               # 止めでも session を書いて zip を作る（裁定 D236）
110 |     sys.exit('[boot_Bl3] 止める（登録者に相談）: ' + msg)
111 | 
112 | 
113 | def jdefault(o):
114 |     """numpy の数と配列を JSON に（値の丸めはしない）。"""
115 |     if hasattr(o, 'tolist'):
116 |         return o.tolist()
117 |     if hasattr(o, 'item'):
118 |         return o.item()
119 |     raise TypeError(type(o))
120 | 
121 | 
122 | def write_json(path, obj):
123 |     json.dump(obj, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=jdefault)
124 |     return sha16f(path)
125 | 
126 | 
127 | def verify_frozen(repo, sha_map):
128 |     """凍結の記録の SHA16（改行を LF にそろえた SHA-256 の頭 16 桁）を、取り出した作業木のファイルに照らす。疎な取り出しの外のファイルは飛ばして数を記し、
129 |     内側で無いファイルは外れにする（裁定 D236）。"""
130 |     bad, skipped = [], []
131 |     for rp, want in sha_map.items():
132 |         p = os.path.join(repo, *rp.split('/'))
133 |         if not os.path.exists(p):
134 |             if any(rp == d or rp.startswith(d + '/') for d in SPARSE):
135 |                 bad.append({'path': rp, 'got': None, 'want': want})
136 |             else:
137 |                 skipped.append(rp)
138 |             continue
139 |         got = sha16f(p)
140 |         if got != want:
141 |             bad.append({'path': rp, 'got': got, 'want': want})
142 |     return bad, skipped
143 | 
144 | 
145 | def pick_recompute_rows(rows, n):
146 |     """DRY の独立の再計算の行: 減算の行と加算の行を一つずつから、足りなければ前から足す（本の計算では全ての行）。"""
147 |     idx = [i for i, r in enumerate(rows) if r[2] < 0][:1] + [i for i, r in enumerate(rows) if r[2] > 0][:1]
148 |     idx += [i for i in range(len(rows)) if i not in idx]
149 |     return [rows[i] for i in sorted(idx[:n])]
150 | 
151 | 
152 | def run():
153 |     PHASE = os.environ.get('OP4B_PHASE', 'check')
154 |     COMMIT = os.environ.get('OP4B_COMMIT', '')
155 |     DRY = os.environ.get('OP4B_DRY') == '1'
156 |     if PHASE not in PHASES:
157 |         sys.exit('[boot_Bl3] 相は %s のどれか' % '・'.join(PHASES))
158 |     if not DRY:
159 |         stray = sorted(k for k in os.environ if k.startswith('OP4B_DRY_') or k in ('OP4B_REPO_DIR', 'OP4B_OUT'))
160 |         if stray:
161 |             sys.exit('[boot_Bl3] DRY でないのに検査用の環境変数がある: %s（外してから走らせる）' % '・'.join(stray))
162 |         if not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
163 |             sys.exit('[boot_Bl3] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
164 |     given = [p.strip() for p in os.environ.get('OP4B_PART', ','.join(PARTS)).split(',') if p.strip()]
165 |     if PHASE == 'main' and (not given or any(p not in PARTS for p in given)):
166 |         sys.exit('[boot_Bl3] OP4B_PART は %s の組み合わせ（コンマで区切る）' % '・'.join(PARTS))
167 |     parts = [p for p in PARTS if p in given] if PHASE == 'main' else []
168 |     print('[boot_Bl3] %s 開始 phase=%s %s%s' % (VERSION, PHASE, 'DRY' if DRY else COMMIT, (' parts=' + ','.join(parts)) if parts else ''), flush=True)
169 | 
170 |     # ---- 1. リポジトリ（コミット固定）と出力の置き場
171 |     if DRY:
172 |         REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
173 |         OUTROOT = os.path.abspath(os.environ['OP4B_OUT'])
174 |     else:
175 |         REPO, OUTROOT = '/content/ontology-preamble-4b', '/content/op4b-Bl3'
176 |         head_ok = os.path.isdir(os.path.join(REPO, '.git')) and sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
177 |         if not head_ok:
178 |             shutil.rmtree(REPO, ignore_errors=True)
179 |             sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
180 |             sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone'] + SPARSE)
181 |             sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
182 |         if sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() != COMMIT:
183 |             stop('取り出したコミットが OP4B_COMMIT と違う')
184 |         dirty = sh(['git', '-C', REPO, 'status', '--porcelain'], check=False).stdout.strip()
185 |         if dirty:
186 |             stop('取り出した作業木に変更がある: %s' % dirty.splitlines()[:5])
187 |     stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
188 |     od = os.path.join(OUTROOT, '%s-%s' % (PHASE, stamp))
189 |     os.makedirs(od, exist_ok=True)
190 |     PROGRESS['path'] = os.path.join(od, 'progress.log')
191 |     CTX.update(od=od, dry=DRY, session={'kind': 'bl3_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY})
192 |     CANON = os.path.join(REPO, 'design', 'contrasts-Bl3.json')
193 |     T3 = json.load(open(CANON, encoding='utf-8'))
194 |     FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
195 |     FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
196 |     FRP = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
197 |     SRP = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
198 |     FR, frozen = None, None
199 |     if PHASE in ('pilot', 'main'):
200 |         if DRY:
201 |             mark('dry_no_gate', note='DRY は凍結と封印の記録を見ない')
202 |         else:
203 |             for p in (FRP, SRP):
204 |                 if not os.path.exists(p):
205 |                     stop('相 %s は下見の前の凍結と封印の後に走らせる（%s が無い・正本 predictions.when）' % (PHASE, os.path.basename(p)))
206 |             FR = json.load(open(FRP, encoding='utf-8'))
207 |             SR = json.load(open(SRP, encoding='utf-8'))
208 |             for role in ('coordinator', 'registrant'):                 # 封印した予想の SHA-256 を封印の記録と照らす（裁定 D236）
209 |                 pp = os.path.join(REPO, *SR['predictions'][role]['path'].split('/'))
210 |                 if not os.path.exists(pp) or sha256f(pp) != SR['predictions'][role]['sha256']:
211 |                     stop('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
212 |             if PHASE == 'main' and 'main_freeze' not in FR:
213 |                 stop('相 main は本の凍結の後に走らせる（凍結の記録に本の凍結が無い）')
214 |             sha_map = FR['main_freeze']['frozen_sha16'] if PHASE == 'main' else FR['frozen_sha16']
215 |             bad, skipped = verify_frozen(REPO, sha_map)
216 |             frozen = {'checked': len(sha_map) - len(skipped), 'skipped': skipped, 'bad': bad}
217 |             if bad:
218 |                 stop('凍結の記録の SHA16 と取り出したファイルが違う: %s' % bad)
219 |             mark('frozen', checked=frozen['checked'], skipped=len(skipped))
220 |     mark('repo', commit=COMMIT[:12] or 'dry', canon=T3['version'], canon_sha16=sha16f(CANON), out=od)
221 | 
222 |     # ---- 2. 版（正本 inputs.versions_B）と GPU
223 |     import importlib.metadata as md
224 | 
225 |     def ver(k):
226 |         try:
227 |             return md.version(k)
228 |         except Exception:
229 |             return None
230 |     PIN = T3['inputs']['versions_B']
231 |     VER = {k: ver(k) for k in ('numpy', 'scipy', 'torch', 'transformers', 'torchvision', 'torchaudio', 'tokenizers', 'huggingface_hub', 'accelerate', 'safetensors')}
232 |     want = {'numpy': PIN['numpy'], 'torch': PIN['torch'], 'transformers': PIN['transformers']}
233 |     bad_v = {k: VER[k] for k, v in want.items() if VER[k] != v}          # 文字列の完全な一致（torch は CUDA の組みまで・裁定 D187）
234 |     if bad_v and not DRY:
235 |         mark('pin', installing=bad_v)
236 |         os.environ['HF_HUB_DISABLE_XET'] = '1'
237 |         if 'torch' in bad_v:
238 |             cuda = PIN['torch'].split('+')[1]
239 |             pk = ['torch==%s' % PIN['torch']] + ['%s==%s+%s' % (c, VER[c].split('+')[0], cuda) for c in ('torchvision', 'torchaudio') if VER.get(c)]
240 |             sh([sys.executable, '-m', 'pip', 'install', '-q'] + pk + ['--index-url', 'https://download.pytorch.org/whl/%s' % cuda])
241 |         sh([sys.executable, '-m', 'pip', 'install', '-q', 'numpy==%s' % want['numpy'], 'transformers==%s' % want['transformers'], 'accelerate', 'huggingface_hub', 'safetensors'])
242 |         print('[boot_Bl3] 版を入れ直した。**ランタイムを再起動して（「ランタイム」→「セッションを再起動」）、同じ一行をもう一度走らせる**', flush=True)
243 |         sys.exit(0)
244 |     GPU = 'dry'
245 |     if not DRY:
246 |         GPU = sh('nvidia-smi --query-gpu=name --format=csv,noheader', check=False).stdout.strip().split('\n')[0]
247 |         if 'L4' not in GPU and 'A100' not in GPU:
248 |             stop('GPU %s は登録の環境（Colab L4・A100 は予備）に無い' % GPU)
249 |     mark('versions', versions=VER, gpu=GPU)
250 | 
251 |     import numpy as np
252 |     import torch
253 |     sys.path.insert(0, os.path.join(REPO, 'tools'))
254 |     sys.path.insert(0, os.path.join(REPO, 'tools', 'colab'))
255 |     import direction_B
256 |     import run_stageB_local as RB
257 |     import bl3_core as K
258 |     import bl3_run as BR
259 |     import bl3_directions as BD
260 |     import analyze_Bl3 as AZ
261 |     from transformers import AutoTokenizer, AutoModelForCausalLM
262 | 
263 |     # ---- 3. 重み（転記行 F の SHA-256 と突き合わせる）
264 |     M = T3['inputs']['model']
265 |     W_SHA = {}
266 |     if DRY:
267 |         import dry_run_Bl3 as DR
268 |         SNAPDIR = os.environ.get('OP4B_TOKENIZER_DIR') or DR.SNAP
269 |     else:
270 |         os.environ['HF_HUB_DISABLE_XET'] = '1'
271 |         from huggingface_hub import snapshot_download
272 |         SNAPDIR = snapshot_download(M['repo'], revision=M['rev'])
273 |         idx = json.load(open(os.path.join(SNAPDIR, 'model.safetensors.index.json'), encoding='utf-8'))
274 |         need_f = ['config.json', 'tokenizer.json', 'model.safetensors.index.json'] + sorted(set(idx['weight_map'].values()))
275 |         miss_f = [x for x in need_f if x not in FJ['facts']['F']['sha256']]
276 |         if miss_f:
277 |             stop('転記行 F に、重みの索引の断片か設定のファイルが欠けている: %s' % miss_f)      # 裁定 D236
278 |         W_SHA = {fn: sha256f(os.path.join(SNAPDIR, fn)) for fn in FJ['facts']['F']['sha256']}
279 |         badw = [fn for fn, sha in FJ['facts']['F']['sha256'].items() if W_SHA[fn] != sha]
280 |         if badw:
281 |             stop('重みの SHA-256 が転記行 F と違う: %s' % badw)
282 |     mark('weights', snapshot=os.path.basename(SNAPDIR), checked=len(W_SHA))
283 | 
284 |     # ---- 4. 方向の npz（方向の記録の SHA-256・組ごとの SHA-256 を転記行 D と・Colab で乱数を引き直さない）
285 |     NPZ = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.npz')
286 |     DJP = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json')
287 |     if not os.path.exists(NPZ) or not os.path.exists(DJP):
288 |         stop('方向の npz か方向の記録が取り出しに無い（npz と器を push してから相 check を走らせる・裁定 D236）')
289 |     DJ = json.load(open(DJP, encoding='utf-8'))
290 |     npz_sha = sha256f(NPZ)
291 |     if npz_sha != DJ['npz_sha256']:
292 |         stop('方向の npz の SHA-256 が方向の記録と違う')
293 |     if FR is not None and npz_sha != FR.get('directions_npz_sha256'):
294 |         stop('方向の npz の SHA-256 が凍結の記録と違う')
295 |     Zd = np.load(NPZ)
296 |     try:
297 |         grp = BD.verify_against_facts({g: Zd[g] for g in BD.GROUPS}, FJ)
298 |         dirs_real, names_real = BR.load_dirs(NPZ, DJP, T3, FJ)             # 名の並びを正本と転記行 D に照らす（裁定 D236）
299 |     except (SystemExit, BR.ToolError) as e_:
300 |         stop(str(e_))
301 |     pair_names = list(DJ['groups']['real']['names'])
302 |     mark('directions', npz_sha256=npz_sha[:16], groups={k: v[:16] for k, v in grp.items()}, n=len(dirs_real))
303 | 
304 |     # ---- 5. 模型とトークナイザ
305 |     tok = AutoTokenizer.from_pretrained(SNAPDIR)
306 |     if DRY:
307 |         model, cfg = DR.tiny_model()
308 |         dev = 'cpu'
309 |     else:
310 |         model = AutoModelForCausalLM.from_pretrained(SNAPDIR, torch_dtype=torch.bfloat16, device_map='cuda').eval()
311 |         cfg = model.config
312 |         dev = 'cuda'
313 |         got = {'num_hidden_layers': cfg.num_hidden_layers, 'hidden_size': cfg.hidden_size, 'vocab_size': cfg.vocab_size, 'rms_norm_eps': cfg.rms_norm_eps,
314 |                'tie_word_embeddings': cfg.tie_word_embeddings, 'tokenizer_len': len(tok)}
315 |         if got != {k: M[k] for k in got}:
316 |             stop('模型の設定が正本 inputs.model と違う: %s' % {k: (got[k], M[k]) for k in got if got[k] != M[k]})
317 |     L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
318 |     if not DRY and L != T3['layers']['indices'][str(T3['layers']['selected_ratio'])]:
319 |         stop('選んだ層の添字が正本 layers.indices と違う: %d' % L)
320 |     coef = float(T3['layers']['coef_applied'])
321 |     mark('model', dry=DRY, layers=cfg.num_hidden_layers, layer_idx=L, coef=coef, dtype=str(next(model.parameters()).dtype), device=dev)
322 | 
323 |     # ---- 6. 升目の入力（凍結の組み立ての関数と転記行 A の書き出し・転記行 B と突き合わせる）
324 |     cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
325 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
326 |     gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in gate_only})
327 |     try:
328 |         cells = BR.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
329 |     except BR.ToolError as e_:
330 |         stop(str(e_))
331 |     mark('cells', main=len(cell_keys), gate_only=len(gate_only_cells))
332 | 
333 |     SESSION = {'kind': 'bl3_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY, 'gpu': GPU, 'versions': VER, 'weights_sha256': W_SHA,
334 |                'canon_sha16': sha16f(CANON), 'directions_npz_sha256': npz_sha, 'directions_group_sha256': grp, 'frozen_check': frozen, 'layer_idx': L, 'coef': coef}
335 |     CTX['session'] = SESSION
336 | 
337 |     def finish(extra=None):
338 |         package('final', dict(extra or {}, finished=now()))
339 |         mark('done', zips=len(SESSION.get('zips') or []))
340 |         return od
341 | 
342 |     # ---- 7. 相 check（順伝播を一度も走らせない）
343 |     if PHASE == 'check':
344 |         calls = collections.Counter()
345 | 
346 |         def guard_of(name):
347 |             def h(m, a):
348 |                 calls[name] += 1
349 |                 raise Stop('相 check で順伝播が呼ばれた（%s・正本 computation.before_seal）' % name)
350 |             return h
351 |         guards = [model.register_forward_pre_hook(guard_of('model')), model.model.register_forward_pre_hook(guard_of('model.model')),
352 |                   model.lm_head.register_forward_pre_hook(guard_of('lm_head'))] + [l_.register_forward_pre_hook(guard_of('layers.%d' % i_)) for i_, l_ in enumerate(model.model.layers)]
353 |         E = FJ['facts']['E']
354 |         sets = BR.cell_sign_sets(T3, None, names_real['named'], names_real['B_random'], names_real['iso'], names_real['real'], gate_only)
355 |         n_pass = sum(len(s[3]) for s in sets)
356 |         if n_pass != E['passes_main'] + E['passes_gate_extra'] + E['passes_orient_extra']:
357 |             stop('升目と符号の組の順伝播の数が転記行 E と違う: %d' % n_pass)
358 |         rows_rc, dbr = K.recompute_set(T3['main_rows'], pair_names, T3['nulls']['real']['swap_siblings'], T3['nulls']['isotropic']['count'])
359 |         n_rc = sum(1 + len(v) for v in dbr.values())
360 |         if 2 * n_rc != E['passes_recompute'] or any(1 + len(v) != E['per_row_recompute'] for v in dbr.values()):
361 |             stop('独立の再計算の組の順伝播の数が転記行 E と違う: %d' % n_rc)
362 |         AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
363 |         rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader(REPO))
364 |         if len(rows_gate) != T3['gate']['rows_gate'] or sorted(r['name'] for r in rows_gate) != sorted(FJ['facts']['C']['style_share_pt']):
365 |             stop('門の行が転記行 C と違う: %d' % len(rows_gate))
366 |         sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
367 |         cnt = AZ.secondary_counts(FB, sec_rows)
368 |         try:
369 |             ctx = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
370 |         except BR.ToolError as e_:
371 |             stop(str(e_))
372 |         try:
373 |             anchor = K.comparator_anchor(pair_names, T3['nulls']['real']['swap_siblings'], K.blens_own_pair())      # 比べる相手の除き方の錨（裁定 D231）
374 |         except ValueError as e_:
375 |             stop(str(e_))
376 |         vn = float(np.linalg.norm(dirs_real['static']))
377 |         if abs(vn - FJ['facts']['D']['vhat_norm']) > 1e-9 * FJ['facts']['D']['vhat_norm']:
378 |             stop('‖static‖ が転記行 D の値と違う: %r' % vn)
379 |         if len(ctx) != cnt['contexts']:
380 |             stop('乙の文脈の数が B-lens の選んだ出力の数と違う: %d' % len(ctx))
381 |         if (cnt['row_passes'], cnt['sign_batches'], cnt['contexts']) != (E['passes_secondary'], E['batches_secondary'], E['contexts_secondary']):
382 |             stop('乙の順伝播の数が転記行 E と違う: %s' % cnt)
383 |         V0 = np.zeros((1, cfg.hidden_size), dtype=np.float32)
384 |         try:
385 |             h_ = RB.register_hook(model, L, RB.make_hook(V0, coef, 1, [0], meta={'bl3': 'check'}))
386 |             h_.remove()
387 |             RB.assert_no_hooks(model, L)
388 |         except SystemExit as e_:
389 |             stop('加減の hook を掛けて外せない: %s' % e_)
390 |         try:
391 |             import bl3_recompute_rewrite as RW
392 |             rw_ok = hasattr(RW, 'recompute_rewrite')
393 |         except ImportError:
394 |             rw_ok = False
395 |         if not rw_ok and not DRY:
396 |             stop('残差の書き換えの器（tools/bl3_recompute_rewrite.py の recompute_rewrite）を import できない')
397 |         for g_ in guards:
398 |             g_.remove()
399 |         chk = {'cells': {k: {'prompt_len': len(c.prompt), 'main_position': c.mp, 'readout_position': c.ro, 'family': c.fam, 'set_ids': c.set_ids, 'ids_sha16': BR.ids_sha16(c)} for k, c in cells.items()},
400 |                'cell_signs': len(sets), 'passes': n_pass, 'recompute_rows': len(rows_rc), 'recompute_passes_per_path': n_rc, 'gate_rows': len(rows_gate),
401 |                'secondary': dict(cnt, cells=len(sec_rows), letter_token_is_L=sum(1 for c in ctx if c[3]['letter_token_is_L']), max_ids=max(c[3]['n_ids'] for c in ctx)),
402 |                'hook_register_remove': True, 'rewrite_importable': rw_ok, 'forward_calls': sum(calls.values()), 'forward_guards': len(guards),
403 |                'comparator_anchor': anchor, 'static_norm_matches_fact_D': True}
404 |         write_json(os.path.join(od, 'check.json'), chk)
405 |         mark('check', cell_signs=len(sets), passes=n_pass, recompute_rows=len(rows_rc), gate_rows=len(rows_gate), secondary_contexts=len(ctx), rewrite_importable=rw_ok)
406 |         return finish()
407 | 
408 |     # ---- 8. 走らせる器（DRY は合成の方向と読み取りの集合の行を置き直した乱数の模型）
409 |     if DRY:
410 |         iso_n = int(os.environ.get('OP4B_DRY_ISO', '9') or 9)
411 |         names = {'named': list(names_real['named']), 'B_random': list(names_real['B_random']), 'iso': names_real['iso'][:iso_n], 'real': list(names_real['real']), 'check': ['check']}
412 |         dirs = DR.synth_dirs(cfg.hidden_size, names['named'] + names['B_random'] + names['iso'] + names['real'] + names['check'])
413 |         DR.calibrate_readout_rows(model, BR.Runner(model, T3, L, coef, dirs), cells[cell_keys[0]], FJ)
414 |     else:
415 |         iso_n = None
416 |         dirs, names = dirs_real, names_real
417 |     R = BR.Runner(model, T3, L, coef, dirs)
418 |     TOOL_ERR = (BR.ToolError, SystemExit, AssertionError)
419 | 
420 |     # ---- 9. 相 pilot
421 |     if PHASE == 'pilot':
422 |         B = FJ['facts']['B']['cells']
423 |         stage_b_rate = {k: B[k]['catastrophe'] / B[k]['n_ok'] for k in cell_keys}
424 |         variants = collections.OrderedDict((k, v['ids']) for k, v in FJ['facts']['A']['variants'].items() if v.get('boundary_ok'))
425 |         try:
426 |             rec = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
427 |         except TOOL_ERR as e_:
428 |             rec = {'tool_error': str(e_), 'n_forward': R.n_forward}
429 |         write_json(os.path.join(od, 'pilot.json'), {'pilot': rec, 'variants_used': list(variants), 'clause': CLAUSE})
430 |         if 'tool_error' in rec:
431 |             finish({'tool_error': rec['tool_error']})
432 |             stop('器の誤りで下見が止まった（正本 pilot.decision.tool_error・直してやり直すかは登録者の裁定）: %s' % rec['tool_error'])
433 |         dec = rec['decision']
434 |         mark('pilot', q1=dec.get('q1'), dropped=dec.get('dropped'), batch=rec.get('batch'), floor=rec.get('floor'), cache_tol=rec.get('cache_tol'),
435 |              shortcut=(rec.get('v') or {}).get('shortcut'), n_forward=R.n_forward)
436 |         return finish()
437 | 
438 |     # ---- 10. 相 main（組ごとに出力を置く）
439 |     if DRY:
440 |         pilot = json.load(open(os.environ['OP4B_DRY_PILOT'], encoding='utf-8'))['pilot']
441 |     else:
442 |         pilot = FR['main_freeze']['pilot']
443 |         if pilot != FR['main_freeze']['pilot_attempts'][-1]:
444 |             stop('本の凍結の下見の記録と、下見の試みの最後が違う')
445 |     if pilot.get('tool_error') or (pilot.get('decision') or {}).get('stop'):
446 |         stop('凍結の記録の下見の記録が「止める」か器の誤り（本の計算は走らせない）')
447 |     dropped = list((pilot.get('decision') or {}).get('dropped', []))
448 |     first_cell = [cells[k] for k in cell_keys if k not in set(dropped)][0]
449 |     SESSION['pilot_used'] = {k: pilot.get(k) for k in ('batch', 'floor', 'cache_tol')}
450 |     SESSION['pilot_used'].update({'shortcut': (pilot.get('v') or {}).get('shortcut'), 'dropped': dropped})
451 |     SESSION['parts'] = parts
452 |     for part in parts:
453 |         mark('part', part=part)
454 |         out = collections.OrderedDict(part=part, clause=CLAUSE)
455 |         n0 = R.n_forward
456 |         try:
457 |             if part != 'main':                       # どの組も頭で出口の値の自己検査（本の計算の組は run_main_phase の頭で行う）
458 |                 lc = R.logit_check(first_cell, T3['computation']['logit_tol'])
459 |                 out['logit_check'] = lc
460 |                 if not lc['pass']:
461 |                     raise BR.ToolError('出口の値の自己検査が落ちた（組 %s の頭）: %s' % (part, lc))
462 |             if part == 'main':
463 |                 MP = BR.run_main_phase(R, T3, FJ, cells, names, pilot, iso_n=None, log=say)
464 |                 out.update(MP)
465 |                 hd = MP['head']
466 |                 mark('main_head', logit_max_abs=hd['logit_check']['max_abs'], shortcut=MP['shortcut'], layer_diff=hd['layer_check']['diff'], cell_signs=len(MP['cells']))
467 |             elif part == 'recompute':
468 |                 rows_rc, dbr = K.recompute_set(T3['main_rows'], pair_names, T3['nulls']['real']['swap_siblings'],
469 |                                                len(names['iso']), dropped)
470 |                 if DRY:
471 |                     rows_rc = pick_recompute_rows(rows_rc, int(os.environ.get('OP4B_DRY_RC', '2') or 2))
472 |                     dbr = collections.OrderedDict((r[0], dbr[r[0]]) for r in rows_rc)
473 |                 out['rows'] = rows_rc
474 |                 out['n_iso'] = len(names['iso'])
475 |                 t1 = time.time()
476 |                 out['hook'] = BR.recompute_hook_path(R, [(n, cells[ck], s) for n, ck, s in rows_rc], dbr, log=say)
477 |                 mark('recompute_hook', rows=len(rows_rc), seconds=round(time.time() - t1, 1))
478 |                 try:
479 |                     import bl3_recompute_rewrite as RW
480 |                 except ImportError:
481 |                     RW = None
482 |                 if RW is None:
483 |                     if not DRY:
484 |                         raise BR.ToolError('残差の書き換えの器を import できない')
485 |                     out['rewrite'] = None
486 |                     mark('recompute_rewrite', skipped='DRY で器が無い')
487 |                 else:
488 |                     t1 = time.time()
489 |                     # mask の組み方を、本の器のフックの道の近道なし（use_cache=False・明示の mask）にそろえる（個体の開発の記録 `records/Bl3/tools/recompute-rewrite-dev-Bl3.md`）
490 |                     out['rewrite'] = RW.recompute_rewrite(model, tok, T3, FJ, rows_rc, dbr, dirs, L, coef, use_cache=False)
491 |                     mark('recompute_rewrite', rows=len(rows_rc), seconds=round(time.time() - t1, 1))
492 |             elif part == 'secondary':
493 |                 AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
494 |                 rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader(REPO))
495 |                 sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
496 |                 ctx = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
497 |                 if DRY:
498 |                     n_sec = int(os.environ.get('OP4B_DRY_SEC', '2') or 2)
499 |                     firsts = [c for i, c in enumerate(ctx) if i == 0 or c[0] != ctx[i - 1][0]]
500 |                     ctx = firsts[:n_sec]
501 |                 out['rows_by_cell'] = sec_rows
502 |                 out['counts'] = AZ.secondary_counts(FB, sec_rows)
503 |                 t1 = time.time()
504 |                 out['contexts'] = BR.run_secondary(R, ctx, sec_rows, log=say)
505 |                 mark('secondary', contexts=len(ctx), seconds=round(time.time() - t1, 1))
506 |         except TOOL_ERR as e_:
507 |             out['tool_error'] = str(e_)
508 |         out['n_forward'], out['n_forward_total'] = R.n_forward - n0, R.n_forward      # 組の順伝播の数と、起動の中の累積（裁定 D236）
509 |         write_json(os.path.join(od, '%s.json' % part), out)
510 |         SESSION.setdefault('part_sha256', {})[part] = sha256f(os.path.join(od, '%s.json' % part))      # 一致だけを見る段が読む組の出力の同定（裁定 D236）
511 |         if 'tool_error' in out:
512 |             finish({'tool_error': out['tool_error'], 'tool_error_part': part})
513 |             stop('器の誤りで組 %s が止まった（正本 computation.tool_error・結果を開かずに登録者に上げる）: %s' % (part, out['tool_error']))
514 |         package('part-%s' % part)                                   # 組ごとに zip を作って落とす（落ちた組から走らせ直せるように・裁定 D236）
515 |     return finish()
516 | 
517 | 
518 | if __name__ == '__main__':
519 |     try:
520 |         run()
521 |     except SystemExit:
522 |         raise
523 |     except Stop as e_:
524 |         LOG.append({'step': 'guard', 'at': now(), 'reason': str(e_)})
525 |         package('stopped', {'stopped': str(e_)})
526 |         sys.exit('[boot_Bl3] 止める（相 check の守り・登録者に相談）: %s' % e_)
527 |     except Exception:
528 |         LOG.append({'step': 'crash', 'at': now(), 'traceback': traceback.format_exc()[-4000:]})
529 |         package('crash', {'crash': traceback.format_exc()[-4000:]})       # 予期しない誤りでも session を書いて zip を作る（裁定 D236）
530 |         say('[boot_Bl3] 予期しない誤りで止まった（器の誤りではない・登録者に相談）')
531 |         raise
```
<<< 終: `tools/colab/boot_Bl3.py` >>>

==================== 第七部 直した器の全文（集計・掃き出し・報告の組み立て・封印・凍結の本文・凍結の記帳） ====================

<<< 始: `tools/analyze_Bl3.py`（SHA16 86070F3268E10CC0・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """analyze_Bl3.py v3 —— B-lens 層三（Bl3）の集計の器（主の札・門・記述の門・q7・独立の再計算の一致・予想の答え・2026-09-25）。
  3 | 
  4 | 入力: 本の計算の出力（升目と符号ごとの効き目・質量・層ごとの差分）・下見の記録（本の凍結で凍結したもの）・独立の再計算の二つの道の出力・段階 B の凍結した集計器の記録と試行の記録・
  5 |       設計事実（q7 の区間）・正本。重みは読まない。**読みは付けない**（読みの型の当てはめと文は組み立ての器 `tools/build_report_Bl3.py` が正本の読みの表から行う）。
  6 | 計算（正本のとおり・芯の関数 `tools/bl3_core.py` を呼ぶ）:
  7 |   - 主の札: 行ごとの割合と裾の本数（等方の帰無・同じ升目と符号）・Holm（下見で外した升目の行を除いた数）・効き目の側・二つ目の札（中心・最上位・二つの順位）・等方の最上位の割合。
  8 |   - 門: 段階 B の方向ごとの行（土台の無操作の腕の破局が零でも全部でもない行）で、本の門・v̂ を抜いた門と、記述の門三つ（v̂ と (6b) を抜く・選択 a の件数・様式の転位の行を除く）。
  9 |   - q7（`predictions.q7_rule`）・予想の答え（q1〜q7・下見で止まったときと門が判定不能のとき）・独立の再計算の二段の一致（`independent_recompute.agreement`）。
 10 |   - 記述: 質量が `pilot.mass_min` を下回った方向の数（升目と符号ごと）・升目ごとの無操作の選択肢 a の文字の確率（裁定 D223）。
 11 | 関数は合成データの器 `tools/dry_run_Bl3.py` が合成の出力で呼ぶ。
 12 | 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 13 | """
 14 | import os, re, sys, json, glob, math, hashlib, collections
 15 | import numpy as np
 16 | 
 17 | HERE = os.path.dirname(os.path.abspath(__file__))
 18 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 19 | sys.path.insert(0, HERE)
 20 | import blens_core as C
 21 | import bl3_core as K
 22 | 
 23 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 一致だけを見る段が読んだ出力の同定を記録し開く段が照らす・開いた集計の一致の照らし・凍結の記録と手元の器の照らし・DRY の印と環境の食い違いで止める・下見の GPU・有限でない値で止める／v2（裁定 D231〜D234）
 24 | ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')
 25 | KIND = {'': 'static', 'rand': 'rand', 'Nk': 'Nk', 'td': 'td'}
 26 | key3 = lambda sc, base, sg: '%s|%s|%+d' % (sc, base, int(sg))
 27 | 
 28 | 
 29 | # ---------------- 段階 B の門の行 ----------------
 30 | def stage_b_gate_rows(T3, AN, trials_of):
 31 |     """門の行（正本 `gate.rows_rule`）と、行動の量（破局・選択 a の件数）と、様式の差（pt）。trials_of(場面, 腕) → 使えた試行の並び。"""
 32 |     BD = AN['by_direction']
 33 |     noop = {(r['scenario'], r['arm']): r for r in BD if r['direction_id'] == 'fixed' and '+v' not in r['arm'] and '-v' not in r['arm']}
 34 |     cc = T3['gate']['continuity']
 35 |     rows = []
 36 |     for r in BD:
 37 |         m = ARM_RE.match(r['arm'])
 38 |         if not m:
 39 |             continue
 40 |         b = noop[(r['scenario'], m.group(1))]
 41 |         if not (0 < b['cat'] < b['n_ok']):
 42 |             continue
 43 |         unit = r['direction_id'] if m.group(3) == 'rand' else KIND.get(m.group(3) or '', 'loaded')
 44 |         trs = [t for t in trials_of(r['scenario'], r['arm']) if t['direction_id'] == r['direction_id']]
 45 |         base_trs = trials_of(r['scenario'], m.group(1))
 46 |         n_a, n_a0 = sum(1 for t in trs if t['choice'] == 'a'), sum(1 for t in base_trs if t['choice'] == 'a')
 47 |         if len(trs) != r['n_ok'] or len(base_trs) != b['n_ok']:
 48 |             raise SystemExit('試行の記録と集計の記録の件数が違う（止める）: %s %s %s' % (r['scenario'], r['arm'], r['direction_id']))
 49 |         sg = 1 if m.group(2) == '+' else -1
 50 |         rows.append({'scenario': r['scenario'], 'arm': r['arm'], 'direction_id': r['direction_id'], 'base': m.group(1), 'sign': sg, 'unit': unit,
 51 |                      'cell': '%s|%s' % (r['scenario'], m.group(1)), 'fam': key3(r['scenario'], m.group(1), sg),
 52 |                      'y': K.behavior_y(r['cat'], r['n_ok'], b['cat'], b['n_ok'], cc), 'y_a': K.behavior_y(n_a, r['n_ok'], n_a0, b['n_ok'], cc),
 53 |                      'style_pt': 100.0 * (sum(1 for t in trs if t['style_b']) / len(trs) - sum(1 for t in base_trs if t['style_b']) / len(base_trs)),
 54 |                      'name': '%s|%s' % (r['scenario'], r['arm']) + ('〔%s〕' % r['direction_id'] if m.group(3) == 'rand' else '')})
 55 |     return rows
 56 | 
 57 | 
 58 | def trials_reader(repo=REPO):
 59 |     cache = {}
 60 | 
 61 |     def f(sc, arm):
 62 |         k = (sc, arm)
 63 |         if k not in cache:
 64 |             d = os.path.join(repo, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
 65 |             fs = glob.glob(os.path.join(d, 'trials-*.jsonl'))
 66 |             if len(fs) != 1:
 67 |                 raise SystemExit('段階 B の試行の記録がちょうど一つでない（止める）: %s（%d）' % (d, len(fs)))
 68 |             cache[k] = [t for t in (json.loads(l) for l in open(fs[0], encoding='utf-8')) if t['status'] == 'ok']
 69 |         return cache[k]
 70 |     return f
 71 | 
 72 | 
 73 | # ---------------- 主の札 ----------------
 74 | def row_labels(T3, main_rows, eff, pair_names, dropped_cells=(), p_override=None):
 75 |     """主の行の札。eff: 升目と符号の鍵 → {方向の名: 効き目}。p_override: 行の名 → (効き目, 等方の帰無)（独立の再計算で v̂ の行を置き換えるとき）。"""
 76 |     swaps = T3['nulls']['real']['swap_siblings']
 77 |     alpha = T3['labels']['iso_outside']['holm_alpha']
 78 |     n_iso = T3['nulls']['isotropic']['count']
 79 |     out, pv = collections.OrderedDict(), {}
 80 |     rows = [r for r in main_rows if '%s|%s' % (r['scenario'], r['base']) not in set(dropped_cells)]
 81 |     for r in rows:
 82 |         k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
 83 |         if p_override and r['id'] in p_override:
 84 |             e, iso = p_override[r['id']]['effect'], p_override[r['id']]['iso']
 85 |             same, opp = p_override[r['id']]['comps_same'], p_override[r['id']]['comps_opp']
 86 |         else:
 87 |             e = eff[k][r['direction']]
 88 |             iso = [eff[k]['iso:%d' % i] for i in range(n_iso)]
 89 |             comps = K.comparators_for(r['direction'], pair_names, swaps)
 90 |             same, opp = [eff[k]['real:' + p] for p in comps], [eff[kk]['real:' + p] for p in comps]
 91 |         pt = K.p_and_tail(e, iso)
 92 |         sl = K.second_label(e, list(same) + list(opp), list(zip(same, opp)))
 93 |         out[r['id']] = {'direction': r['direction'], 'cell_sign': k, 'effect': e, 'p': pt['p'], 'upper': pt['upper'], 'lower': pt['lower'], 'tail': pt['tail'],
 94 |                         'iso_median': float(np.median(iso)), 'second': sl, 'iso_top_share': K.iso_top_share(iso, sl['center'], list(same) + list(opp)), '_iso': iso}
 95 |         pv[r['id']] = pt['p']
 96 |     H = K.holm(pv, alpha)
 97 |     for rid, o in out.items():
 98 |         o['holm_step'], o['iso_outside'] = H[rid]['step'], bool(H[rid]['pass'])
 99 |         o['side'] = K.effect_side(o['effect'], o.pop('_iso'))      # 効き目の側は全ての行で作る（記述・`labels.print_rule`・裁定 D231）。読みの文で書くのは等方の外の行だけ（`labels.side_rule`）
100 |     return out, {'m_rows': len(rows), 'dropped_rows': [r['id'] for r in main_rows if r not in rows]}
101 | 
102 | 
103 | def labels_signature(lab):
104 |     """札の一致で見る中身（正本 `independent_recompute.agreement`・裁定 D232）: Holm の判定・等方の外の行の割合を決めた裾・等方の外の行の効き目の側・二つ目の札。
105 |     帰無の内側の行の裾と側は札に効かないので比べない（どちらかの道だけで等方の外なら、Holm の判定の欄が違うので一致しない）。"""
106 |     return {rid: (o['iso_outside'], o['tail'] if o['iso_outside'] else None, (o['side'] or {}).get('side') if o['iso_outside'] else None,
107 |                   (o['side'] or {}).get('sign') if o['iso_outside'] else None, o['second']['top']) for rid, o in lab.items()}
108 | 
109 | 
110 | # ---------------- 門 ----------------
111 | def gates(T3, rows, eff, dropped_cells=(), style_rows=()):
112 |     units = ['static', 'loaded', 'Nk', 'td'] + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
113 |     alpha = T3['gate']['alpha']
114 |     rows = [r for r in rows if r['cell'] not in set(dropped_cells)]    # 下見で外した升目の行は、効き目を引く前に落とす（本の計算は外した升目の組を流さない・裁定 D231）
115 |     ue = {u: {f: eff[f][u] for f in sorted({r['fam'] for r in rows})} for u in units}
116 |     rs = lambda pred, yk='y': [{'unit': r['unit'], 'cell': r['cell'], 'fam': r['fam'], 'y': r[yk]} for r in rows if pred(r)]
117 |     out = collections.OrderedDict()
118 |     out['main'] = K.gate(rs(lambda r: True), ue, units, alpha, dropped_cells)
119 |     out['without_vhat'] = K.gate(rs(lambda r: r['unit'] != 'static'), ue, [u for u in units if u != 'static'], alpha, dropped_cells)
120 |     out['desc_without_vhat_loaded'] = K.gate(rs(lambda r: r['unit'] not in ('static', 'loaded')), ue, [u for u in units if u not in ('static', 'loaded')], alpha, dropped_cells)
121 |     out['desc_choice_a'] = K.gate(rs(lambda r: True, 'y_a'), ue, units, alpha, dropped_cells)
122 |     out['desc_without_style'] = K.gate(rs(lambda r: r['name'] not in set(style_rows)), ue, units, alpha, dropped_cells)
123 |     return out
124 | 
125 | 
126 | # ---------------- 予想の答え ----------------
127 | def prediction_truth(T3, pilot_attempts, lab, G, q7_rows, floor):
128 |     q1 = K.q1_from_attempts(pilot_attempts)
129 |     stopped = (not q1['scored']) or q1['q1'] == '止める'
130 |     items = {it['key']: it for it in T3['predictions']['items']}
131 |     tr = collections.OrderedDict()
132 |     tr['q1.pilot'] = q1['q1'] if q1['scored'] else None
133 |     if stopped:
134 |         for k in list(items)[1:]:
135 |             tr[k] = None
136 |         return tr, {'stopped': True, 'q1': q1}
137 |     tr['q2.vhat_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'static' and o['iso_outside']), items['q2.vhat_iso']['options'])
138 |     tr['q3.nk_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'Nk' and o['iso_outside']), items['q3.nk_iso']['options'])
139 |     tr['q4.gate'] = None if G['main']['undetermined'] else ('通る' if G['main']['pass'] else '通らない')
140 |     tr['q5.gate_wo_vhat'] = None if G['without_vhat']['undetermined'] else ('通る' if G['without_vhat']['pass'] else '通らない')
141 |     tr['q6.second'] = K.bucket(sum(1 for o in lab.values() if o['second']['top']), items['q6.second']['options'])
142 |     tr['q7.direction'] = K.score_q7(q7_rows, floor) if q7_rows else None
143 |     return tr, {'stopped': False, 'q1': q1}
144 | 
145 | 
146 | def q7_rows_of(lab, FJ):
147 |     iv = {x['id']: x for x in FJ['facts']['C']['q7_intervals']}
148 |     return [{'id': rid, 'effect': o['effect'], 'stage_b_diff': iv[rid]['diff_pt'], 'contains_zero': iv[rid]['contains_zero']}
149 |             for rid, o in lab.items() if o['direction'] == 'static' and o['iso_outside']]
150 | 
151 | 
152 | # ---------------- 独立の再計算の一致 ----------------
153 | def recompute_agreement(T3, main_rows, eff_main, pair_names, hook, rewrite, pilot, dropped_cells=(), rows_subset=None):
154 |     """二段の一致（正本 `independent_recompute.stages`・`agreement`）。hook と rewrite: 行の名 → {'noop_lo','effects': {'方向|符号': 効き目}}。
155 |     本の計算では、下見で外した升目の行を除く v̂ の行のすべてを比べる（行が欠ければ一致しない）。rows_subset は合成データの確かめで比べる行を絞るときだけ使う。
156 |     一段目は、無操作の値と全ての効き目の差が許容の内で、かつ札が同じとき一致（裁定 D233）。二段目は札が同じとき一致とし、効き目の差の最大と許容の内かどうかは記録する（裁定 D234）。"""
157 |     drop = set(dropped_cells)
158 |     in_drop = lambda r: '%s|%s' % (r['scenario'], r['base']) in drop
159 |     comps_of = lambda d: K.comparators_for(d, pair_names, T3['nulls']['real']['swap_siblings'])
160 |     n_iso = T3['nulls']['isotropic']['count']
161 | 
162 |     def override(path):
163 |         ov = {}
164 |         for r in main_rows:
165 |             if r['direction'] != 'static' or r['id'] not in path or in_drop(r) or (rows_subset is not None and r['id'] not in rows_subset):
166 |                 continue
167 |             E = path[r['id']]['effects']
168 |             s = r['sign']
169 |             ov[r['id']] = {'effect': E['static|%+d' % s], 'iso': [E['iso:%d|%+d' % (i, s)] for i in range(n_iso)],
170 |                            'comps_same': [E['real:%s|%+d' % (p, s)] for p in comps_of('static')], 'comps_opp': [E['real:%s|%+d' % (p, -s)] for p in comps_of('static')]}
171 |         return ov
172 | 
173 |     def as_eff(ov):
174 |         return {rid: [o['effect']] + list(o['iso']) + list(o['comps_same']) + list(o['comps_opp']) for rid, o in ov.items()}
175 | 
176 |     def with_noop(ov, path):
177 |         return {rid: [path[rid]['noop_lo']] + v for rid, v in as_eff(ov).items()}      # 一段目は無操作の値も比べる（裁定 D233）
178 |     main_ov = {}
179 |     for r in main_rows:
180 |         if r['direction'] != 'static' or in_drop(r) or (rows_subset is not None and r['id'] not in rows_subset):
181 |             continue
182 |         k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
183 |         main_ov[r['id']] = {'effect': eff_main[k]['static'], 'iso': [eff_main[k]['iso:%d' % i] for i in range(n_iso)],
184 |                             'comps_same': [eff_main[k]['real:' + p] for p in comps_of('static')], 'comps_opp': [eff_main[kk]['real:' + p] for p in comps_of('static')]}
185 |     sig = lambda ov: labels_signature(row_labels(T3, main_rows, eff_main, pair_names, dropped_cells, p_override=ov)[0])
186 |     hk, rw = override(hook), override(rewrite) if rewrite is not None else None
187 |     tol2 = K.cache_tol(pilot['floor'], T3['pilot']['cache_tol_factor'], T3['pilot']['cache_tol_floor'], T3['pilot']['noise_max']) + pilot['floor']
188 |     s2 = K.agreement(as_eff(main_ov), as_eff(hk), tol2, sig(main_ov), sig(hk))
189 |     s2 = dict(s2, agree=bool(s2['labels_same']), rule='札の一致（裁定 D234）', values_beyond_tol=not s2['values_within_tol'])
190 |     out = {'second': s2, 'tol_second': tol2}
191 |     if rw is not None:
192 |         out['first'] = dict(K.agreement(with_noop(hk, hook), with_noop(rw, rewrite), T3['independent_recompute']['tol_stage1'], sig(hk), sig(rw)), rule='無操作の値と効き目の値と札（裁定 D233）')
193 |     else:
194 |         out['first'] = None
195 |     out['tol_first'] = T3['independent_recompute']['tol_stage1']
196 |     out['agree'] = bool(out['second']['agree'] and (out['first'] or {}).get('agree', False))
197 |     return out
198 | 
199 | 
200 | # ---------------- 乙（裁定 D227） ----------------
201 | def secondary_rows(T3, rows_gate, FB):
202 |     """乙の行（裁定 D227）: 門の行のうち、方向が名前のある方向か段階 B の三本で、土台の升目が B-lens の層二の層にある行。符号は門の行の符号。
203 |     戻り値: 升目の鍵 → [(行の名〔場面|腕|単位〕, 方向の名, 符号)]（行の名は B-lens の層二の答えの文字の位置の行と同じ書き方）。"""
204 |     strata_cells = {'%s|%s' % tuple(k.split('|')[:2]) for k in FB['facts']['E']['selected']}
205 |     units = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
206 |     out = collections.OrderedDict()
207 |     for r in rows_gate:
208 |         if r['cell'] in strata_cells and r['unit'] in units:
209 |             out.setdefault(r['cell'], []).append(('%s|%s|%s' % (r['scenario'], r['arm'], r['unit']), r['unit'], r['sign']))
210 |     return out
211 | 
212 | 
213 | def secondary_counts(FB, rows_by_cell):
214 |     """乙の順伝播の数（文脈ごとの行の数の和・文脈ごとの符号の数の和〔無操作と同じバッチに流す〕）。"""
215 |     n_rows = n_batches = 0
216 |     for key, ids_ in FB['facts']['E']['selected'].items():
217 |         rows = rows_by_cell.get('%s|%s' % tuple(key.split('|')[:2]), [])
218 |         n_rows += len(ids_) * len(rows)
219 |         n_batches += len(ids_) * len({sg for _, _, sg in rows})
220 |     return {'row_passes': n_rows, 'sign_batches': n_batches, 'contexts': sum(len(v) for v in FB['facts']['E']['selected'].values())}
221 | 
222 | 
223 | def secondary_summary(sec_out, calib_letter=None):
224 |     """乙のまとめ（記述・読みは付けない）: 行ごとに、文脈の間の平均・中央値・四分位と、B-lens の層二の直接の経路の値（あれば）を並べる。"""
225 |     acc = collections.defaultdict(lambda: collections.defaultdict(list))
226 |     for c in sec_out:
227 |         for name, v in c['rows'].items():
228 |             for k, x in v.items():
229 |                 acc[name][k].append(x)
230 |     out = collections.OrderedDict()
231 |     for name, d in acc.items():
232 |         s = {k: {'mean': float(np.mean(v)), 'median': float(np.median(v)), 'q1': float(np.percentile(v, 25)), 'q3': float(np.percentile(v, 75)), 'n': len(v)} for k, v in d.items()}
233 |         if calib_letter is not None:
234 |             sc = name.split('|')[0]
235 |             arm = name.split('|')[1]
236 |             base = re.split(r'[+\-]v', arm)[0]
237 |             bl = ((calib_letter.get('%s|%s' % (sc, base)) or {}).get('rows') or {}).get(name)
238 |             s['blens_direct'] = {k: bl[k] for k in ('dlogit_exact_a', 'dlogit_exact_c')} if bl else None
239 |         out[name] = s
240 |     return out
241 | 
242 | 
243 | # ---------------- 記述 ----------------
244 | def chance_after_drop(T3, lab):
245 |     """二つ目の札の偶然の目安を、下見で外した後の行で数え直す（正本 `pilot.decision.drop_effects`・生成器と同じ式・裁定 D231）。分母（方向ごとの行の数）も返す。"""
246 |     co, cp = T3['nulls']['real']['comparators_oriented'], T3['nulls']['real']['comparators']
247 |     by = collections.Counter(o['direction'] for o in lab.values())
248 |     return {'oriented': round(sum(n / (co[d] + 1) for d, n in by.items()), 4), 'pair': round(sum(n / (cp[d] + 1) for d, n in by.items()), 4), 'rows_by_direction': dict(by),
249 |             'canon_all_rows': {'oriented': T3['nulls']['real']['chance_second'], 'pair': T3['nulls']['real']['chance_second_pair']}}
250 | 
251 | 
252 | def descriptive(T3, main_out):
253 |     mm = T3['pilot']['mass_min']
254 |     below = {k: sum(1 for d, v in o['mass'].items() if d != K.NOOP and v < mm) for k, o in main_out.items()}
255 |     pa = {k: o['pa_noop'] for k, o in main_out.items()}
256 |     return {'mass_below_min': below, 'pa_noop': pa}
257 | 
258 | 
259 | def analyze(T3, FJ, main_out, pilot_attempts, pair_names, rows_gate, hook=None, rewrite=None, style_rows=(), rows_subset=None):
260 |     """集計の全体（読みは付けない）。main_out: 升目と符号の鍵 → run_cell_sign の出力。pilot_attempts: 下見の試みの並び（最後が本の凍結の下見）。"""
261 |     pilot = pilot_attempts[-1]
262 |     dropped = (pilot.get('decision') or {}).get('dropped', [])
263 |     nf = sorted({k for k, o in main_out.items() for d, v in list((o.get('effects') or {}).items()) + list((o.get('mass') or {}).items()) if not math.isfinite(float(v))})
264 |     if nf:
265 |         raise SystemExit('有限でない効き目か質量がある（止める・裁定 D236）: %s' % nf[:5])
266 |     eff = {k: o['effects'] for k, o in main_out.items()}
267 |     lab, meta = row_labels(T3, T3['main_rows'], eff, pair_names, dropped)
268 |     G = gates(T3, rows_gate, eff, dropped, style_rows)
269 |     q7 = q7_rows_of(lab, FJ)
270 |     truth, tmeta = prediction_truth(T3, pilot_attempts, lab, G, q7, pilot.get('floor', 0.0))
271 |     out = collections.OrderedDict(version=VERSION, rows=lab, rows_meta=meta, gates=G, q7_rows=q7, predictions_truth=truth, predictions_meta=tmeta,
272 |                                   descriptive=descriptive(T3, main_out), chance=chance_after_drop(T3, lab))
273 |     if hook is not None:
274 |         out['recompute'] = recompute_agreement(T3, T3['main_rows'], eff, pair_names, hook, rewrite, pilot, dropped, rows_subset)
275 |     return out
276 | 
277 | 
278 | # ---------------- 段階 B のその行の注（報告の雛形） ----------------
279 | def stage_b_notes(T3, AN, rows_gate):
280 |     """段階 B のその行の注（正本 `report_rules.template`「主の表と門の行に、段階 B のその行の注（判定保留・ランダム方向の不均一）を写す」）。
281 |     主の行: 段階 B の確かめの行（凍結した集計器の記録の `confirm`・同じ名）の札と注と様式の保留。門の行: 名前のある方向の行は、その腕を比べの加えた腕に持つ確かめの行の札が
282 |     判定保留のときその札。ランダム方向の行は、その腕の不均一の記録（`homogeneity`）に注があるときその注。"""
283 |     conf = {r['id']: r for r in AN['confirm']}
284 |     conf_by_arm = {(r['scenario'], r['A']): r for r in AN['confirm']}
285 |     homo = {(h['scenario'], h['arm']): h for h in AN['homogeneity']}
286 |     main = collections.OrderedDict()
287 |     for r in T3['main_rows']:
288 |         c = conf.get(r['id'])
289 |         main[r['id']] = {'label': c['label'] if c else None, 'notes': list(c.get('notes') or []) if c else [], 'style_hold': bool(c and c.get('style_hold'))}
290 |     gate = collections.OrderedDict()
291 |     for g in rows_gate:
292 |         notes = []
293 |         if g['unit'].startswith('rand:'):
294 |             h = homo.get((g['scenario'], g['arm']))
295 |             if h and h.get('note'):
296 |                 notes.append({'kind': 'ランダム方向の不均一', 'spread_pt': h['spread_pt'], 'threshold_pt': h['threshold_pt']})
297 |         else:
298 |             c = conf_by_arm.get((g['scenario'], g['arm']))
299 |             if c and str(c.get('label', '')).startswith('判定保留'):
300 |                 notes.append({'kind': c['label']})
301 |         gate[g['name']] = notes
302 |     return {'main': main, 'gate': gate}
303 | 
304 | 
305 | # ---------------- 手元の二つの段（一致だけを見る・結果を開く・正本 `independent_recompute.print`・`on_mismatch`） ----------------
306 | PARTS = ('main', 'recompute', 'secondary')
307 | JUDGE = os.path.join(REPO, 'records', 'Bl3', 'judge-Bl3.json')
308 | OPENED = os.path.join(REPO, 'records', 'Bl3', 'analysis-Bl3.json')
309 | FR_PATH = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
310 | SEAL_PATH = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
311 | # 二つの段と報告の頭で、本の凍結の記録の SHA16 と照らすもの（正本・設計事実・方向の記録・集計と札と報告の器・裁定 D236）
312 | FROZEN_CHECK = ('design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json',
313 |                 'tools/analyze_Bl3.py', 'tools/bl3_core.py', 'tools/blens_core.py', 'tools/build_report_Bl3.py', 'tools/sweep_Bl3.py', 'tools/report_lint.py')
314 | STRICT_ENV = ('commit', 'dry', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef')      # 組の間で違えば止める（GPU と版の違いは記す・裁定 D236）
315 | 
316 | 
317 | def sha256f(p):
318 |     h = hashlib.sha256()
319 |     with open(p, 'rb') as fh:
320 |         for blk in iter(lambda: fh.read(1 << 24), b''):
321 |             h.update(blk)
322 |     return h.hexdigest().upper()
323 | 
324 | 
325 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
326 | 
327 | 
328 | def load_outputs(dirs):
329 |     """起動器の相 main の出力（組ごとの JSON と、その置き場の session.json）を、一つ以上の置き場から読む。同じ組が二つあれば止める。
330 |     戻り値: 組 → 出力・組 → session・組 → 読んだファイルの同定（置き場の名・組の JSON と session.json の SHA-256・裁定 D236）。"""
331 |     parts, sessions, files = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
332 |     for d in dirs:
333 |         sp = os.path.join(d, 'session.json')
334 |         S = json.load(open(sp, encoding='utf-8'))
335 |         for part in PARTS:
336 |             p = os.path.join(d, '%s.json' % part)
337 |             if os.path.exists(p):
338 |                 if part in parts:
339 |                     raise SystemExit('同じ組が二つの置き場にある（止める）: %s' % part)
340 |                 parts[part] = json.load(open(p, encoding='utf-8'))
341 |                 sessions[part] = S
342 |                 files[part] = {'dir': os.path.basename(os.path.normpath(d)), 'json_sha256': sha256f(p), 'session_sha256': sha256f(sp)}
343 |     return parts, sessions, files
344 | 
345 | 
346 | def env_same(sessions, pilot_sessions=None):
347 |     """組の間で、コミット・GPU・版・正本・方向の npz・DRY が同じか（違えば記す）。pilot_sessions（本の凍結の下見の session）を与えると、下見の GPU も並べる（裁定 D236）。"""
348 |     keys = ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef')
349 |     ref = next(iter(sessions.values())) if sessions else {}
350 |     diff = {k: {p: s.get(k) for p, s in sessions.items()} for k in keys if any(s.get(k) != ref.get(k) for s in sessions.values())}
351 |     out = {'same': not diff, 'diff': diff, 'strict': [k for k in diff if k in STRICT_ENV]}
352 |     if pilot_sessions is not None:
353 |         pg = sorted({str(s.get('gpu')) for s in pilot_sessions})
354 |         out['pilot_gpu'] = pg
355 |         out['gpu_same_as_pilot'] = sorted({str(s.get('gpu')) for s in sessions.values()}) == pg
356 |     return out
357 | 
358 | 
359 | def with_iso(T3, n_iso):
360 |     """独立の再計算の等方の本数に合わせた正本の写し（本の計算では正本と同じ本数・DRY で減らしたときだけ違う）。"""
361 |     if n_iso == T3['nulls']['isotropic']['count']:
362 |         return T3
363 |     T3x = json.loads(json.dumps(T3))
364 |     T3x['nulls']['isotropic']['count'] = n_iso
365 |     return T3x
366 | 
367 | 
368 | def frozen_versions_bad(FR, repo=REPO, files=FROZEN_CHECK):
369 |     """手元の器と正本・設計事実・方向の記録を、本の凍結の記録の SHA16 と照らす（台帳に記した差分は許す・裁定 D236）。戻り値: 外れの並び。"""
370 |     fz = (FR.get('main_freeze') or {}).get('frozen_sha16') or {}
371 |     led = {td['path']: td for d in FR.get('deviations') or [] for td in d.get('tool_diffs') or []}
372 |     bad = []
373 |     for f in files:
374 |         p = os.path.join(repo, *f.split('/'))
375 |         want, got = fz.get(f), (sha16f(p) if os.path.exists(p) else None)
376 |         if want is None:
377 |             bad.append('%s（本の凍結の記録に無い）' % f)
378 |         elif got != want and not (f in led and led[f].get('after') == got):
379 |             bad.append('%s（本の凍結 %s・今 %s）' % (f, want, got))
380 |     return bad
381 | 
382 | 
383 | def judge(T3, parts, sessions, pilot_attempts, pair_names, files=None, FR=None):
384 |     """一致だけを見る段: 器の誤りの有無・組の環境・二段の一致か不一致かだけを返す（効き目の値と差の最大は返さない）。
385 |     DRY の印が組の間で違うとき・組の間のコミットと正本と npz と層と係数が違うとき・DRY でないのに等方の本数が正本と違うとき・DRY でないのに
386 |     手元の器と正本が本の凍結の記録と違うときは、一致と答えない（裁定 D236）。読んだ出力の同定（files）と凍結の記録の SHA16 を記録に置く。"""
387 |     out = collections.OrderedDict(parts=list(parts), tool_error={p: bool(v.get('tool_error')) for p, v in parts.items()}, env=env_same(sessions))
388 |     drys = {p: bool(s.get('dry')) for p, s in sessions.items()}
389 |     dry = any(drys.values())
390 |     out['dry'] = dry
391 |     out['inputs'] = files
392 |     if FR is not None and os.path.exists(FR_PATH):
393 |         out['freeze_record_sha16'] = sha16f(FR_PATH)
394 |     if os.path.exists(SEAL_PATH):
395 |         out['sealing_record_sha16'] = sha16f(SEAL_PATH)
396 |     stop = lambda why: (out.update(first=None, second=None, agree=None, reason=why), out)[1]
397 |     if any(out['tool_error'].values()) or not {'main', 'recompute'} <= set(parts):
398 |         return stop('器の誤りか、組 main・recompute の欠け')
399 |     if len(set(drys.values())) > 1:
400 |         return stop('組の間で DRY の印が違う: %s' % drys)
401 |     if out['env']['strict']:
402 |         return stop('組の間の環境が違う: %s' % out['env']['strict'])
403 |     rc = parts['recompute']
404 |     n_can = T3['nulls']['isotropic']['count']
405 |     if not dry:
406 |         main_keys = {key3(sc, b, sg) for sc, b, sg in T3['cell_signs_main']}
407 |         n_main = {k: sum(1 for d in o['effects'] if d.startswith('iso:')) for k, o in parts['main']['cells'].items() if k in main_keys}
408 |         if rc['n_iso'] != n_can or any(v != n_can for v in n_main.values()):
409 |             return stop('DRY でないのに等方の本数が正本と違う（組 recompute %s・本の計算の升目と符号 %s）' % (rc['n_iso'], sorted(set(n_main.values()))))
410 |         if FR is None:
411 |             return stop('DRY でないのに凍結の記録が無い')
412 |         bad = frozen_versions_bad(FR)
413 |         if bad:
414 |             return stop('手元の器か正本が本の凍結の記録と違う: %s' % bad)
415 |     pilot = pilot_attempts[-1]
416 |     eff = {k: o['effects'] for k, o in parts['main']['cells'].items()}
417 |     ag = recompute_agreement(with_iso(T3, rc['n_iso']), T3['main_rows'], eff, pair_names, rc['hook'], rc.get('rewrite'), pilot,
418 |                              (pilot.get('decision') or {}).get('dropped', []), rows_subset=set(rc['hook']) if dry else None)
419 |     out.update(first=None if ag['first'] is None else bool(ag['first']['agree']), second=bool(ag['second']['agree']), agree=bool(ag['agree']),
420 |                second_values_within_tol=bool(ag['second']['values_within_tol']),       # 値だけが許容の外で札が同じときは止めずに台帳に記す（裁定 D234）
421 |                reason=None if ag['agree'] else ('一段目の道が無い' if ag['first'] is None else '二段のどちらかが一致しない'))
422 |     return out
423 | 
424 | 
425 | def open_results(T3, FJ, parts, sessions, pilot_attempts, pair_names, AN, calib_letter, FB, repo=REPO, pilot_sessions=None):
426 |     """結果を開く段（登録者と一緒に・一致だけを見る段が一致したとき）: 集計の全体と、報告に並べるもの（下見の記録・頭の確かめ・層ごとの差分・乙・段階 B の注・環境）。"""
427 |     rc = parts['recompute']
428 |     dry = any(s.get('dry') for s in sessions.values())
429 |     T3x = with_iso(T3, rc['n_iso'])
430 |     rows_gate = stage_b_gate_rows(T3, AN, trials_reader(repo))
431 |     style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
432 |     A = analyze(T3x, FJ, parts['main']['cells'], pilot_attempts, pair_names, rows_gate, hook=rc['hook'], rewrite=rc.get('rewrite'), style_rows=style_rows,
433 |                 rows_subset=set(rc['hook']) if dry else None)
434 |     main_keys = {key3(sc, b, sg) for sc, b, sg in T3['cell_signs_main']}
435 |     A['dry'] = dry
436 |     A['n_iso'] = rc['n_iso']
437 |     A['pilot_attempts'] = pilot_attempts
438 |     A['head'] = parts['main']['head']
439 |     A['main_run'] = {k: parts['main'].get(k) for k in ('batch', 'shortcut', 'dropped')}
440 |     A['layerwise'] = {k: o['layers'] for k, o in parts['main']['cells'].items() if k in main_keys}
441 |     A['gate_rows'] = [{k: r[k] for k in ('name', 'scenario', 'arm', 'unit', 'sign', 'cell', 'fam', 'y', 'y_a', 'style_pt')} for r in rows_gate]
442 |     A['style_rows'] = style_rows
443 |     A['stage_b_notes'] = stage_b_notes(T3, AN, rows_gate)
444 |     if 'secondary' in parts:
445 |         S2 = parts['secondary']
446 |         A['secondary'] = {'counts': S2.get('counts'), 'contexts_run': len(S2.get('contexts') or []), 'summary': secondary_summary(S2.get('contexts') or [], calib_letter)}
447 |     A['sessions'] = {p: {k: s.get(k) for k in ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef', 'finished')} for p, s in sessions.items()}
448 |     A['env'] = env_same(sessions, pilot_sessions)
449 |     A['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
450 |     return A
451 | 
452 | 
453 | def open_checked(T3, FJ, parts, sessions, files, J, pilot_attempts, pair_names, AN, calib_letter, FB, FR=None, judge_sha16=None, repo=REPO):
454 |     """結果を開く段の確かめ（裁定 D236）: 一致だけを見る段の記録が一致で、読む出力の同定（置き場の名・組の JSON と session の SHA-256）と凍結の記録の SHA16 が
455 |     一致だけを見る段の記録と同じで、DRY でないときは手元の器と正本が本の凍結の記録と同じであること。開いた集計の二段の一致が一致だけを見る段と違えば止める（書かない）。"""
456 |     if not J.get('agree'):
457 |         raise SystemExit('一致だけを見る段の記録が一致していない（結果を開かない）')
458 |     if J.get('inputs') != files:
459 |         ji, fi = J.get('inputs') or {}, files or {}
460 |         raise SystemExit('結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）: %s' % [p for p in sorted(set(ji) | set(fi)) if ji.get(p) != fi.get(p)])
461 |     dry = any(s.get('dry') for s in sessions.values())
462 |     if not dry:
463 |         if FR is None:
464 |             raise SystemExit('DRY でないのに凍結の記録が無い（開かない）')
465 |         if J.get('freeze_record_sha16') != sha16f(FR_PATH):
466 |             raise SystemExit('凍結の記録が一致だけを見る段の後に変わった（開かない）')
467 |         bad = frozen_versions_bad(FR, repo)
468 |         if bad:
469 |             raise SystemExit('手元の器か正本が本の凍結の記録と違う（開かない）: %s' % bad)
470 |     pilot_sessions = ((FR or {}).get('main_freeze') or {}).get('sessions')
471 |     A = open_results(T3, FJ, parts, sessions, pilot_attempts, pair_names, AN, calib_letter, FB, repo=repo, pilot_sessions=pilot_sessions)
472 |     rc = A.get('recompute') or {}
473 |     got = (None if rc.get('first') is None else bool(rc['first']['agree']), bool((rc.get('second') or {}).get('agree')), bool(rc.get('agree')))
474 |     if got != (J.get('first'), J.get('second'), J.get('agree')):
475 |         raise SystemExit('開いた集計の二段の一致が、一致だけを見る段と違う（書かない）: %s 対 %s' % (got, (J.get('first'), J.get('second'), J.get('agree'))))
476 |     A['inputs'] = files
477 |     A['judge_record_sha16'] = judge_sha16
478 |     return A
479 | 
480 | 
481 | def _freeze_record():
482 |     return json.load(open(FR_PATH, encoding='utf-8')) if os.path.exists(FR_PATH) else None
483 | 
484 | 
485 | def _pilot_attempts(args_pilot, FR=None):
486 |     """下見の試みの並び: 本の計算では凍結の記録の本の凍結（`main_freeze.pilot_attempts`）から。DRY の出力を試すときだけ、相 pilot の出力の pilot.json を与える。"""
487 |     if args_pilot:
488 |         return [json.load(open(p, encoding='utf-8'))['pilot'] for p in args_pilot]
489 |     if FR is None:
490 |         raise SystemExit('凍結の記録が無い（本の計算では本の凍結の下見の記録を読む）')
491 |     atts = FR['main_freeze']['pilot_attempts']
492 |     if FR['main_freeze']['pilot'] != atts[-1]:
493 |         raise SystemExit('本の凍結の下見の記録と、下見の試みの最後が違う（止める）')
494 |     return atts
495 | 
496 | 
497 | def main():
498 |     import argparse, datetime
499 |     ap = argparse.ArgumentParser(description='B-lens 層三の手元の二つの段（judge: 一致だけを見る／open: 結果を開く）')
500 |     ap.add_argument('step', choices=['judge', 'open'])
501 |     ap.add_argument('dirs', nargs='+', help='起動器の相 main の出力の置き場（組ごとの JSON と session.json）')
502 |     ap.add_argument('--pilot', nargs='*', help='DRY の出力を試すときだけ: 相 pilot の出力の pilot.json（試みの順）')
503 |     ap.add_argument('--out', help='出力の置き場（既定は records/Bl3/judge-Bl3.json・analysis-Bl3.json）')
504 |     ap.add_argument('--judge-record', help='結果を開く段が読む、一致だけを見る段の記録（既定は records/Bl3/judge-Bl3.json）')
505 |     a = ap.parse_args()
506 |     T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
507 |     FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
508 |     DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
509 |     parts, sessions, files = load_outputs(a.dirs)
510 |     dry = any(s.get('dry') for s in sessions.values())
511 |     if a.pilot and not dry:
512 |         raise SystemExit('--pilot は DRY の出力を試すときだけ（本の計算では凍結の記録の本の凍結を読む）')
513 |     FR = None if dry else _freeze_record()
514 |     attempts = _pilot_attempts(a.pilot, FR)
515 |     pair_names = list(DJ['groups']['real']['names'])
516 |     if a.step == 'judge':
517 |         out = a.out or JUDGE
518 |         if os.path.exists(out):
519 |             raise SystemExit('既にある（一致だけを見る段は一度だけ）: %s' % out)
520 |         J = judge(T3, parts, sessions, attempts, pair_names, files, FR)
521 |         J['written_utc'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
522 |         J['clause'] = '本記録は一致か不一致かだけを持つ（値は開かない・正本 independent_recompute.print）。'
523 |         json.dump(J, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
524 |         say = lambda b: '無い' if b is None else ('一致' if b else '不一致')
525 |         print('[analyze_Bl3] 一致だけを見る段: 器の誤り %s・組の環境 %s・一段目 %s・二段目（札） %s・二段目の値 %s・全体 %s（値は開いていない）%s' % (
526 |             'あり' if any(J['tool_error'].values()) else '無し', '同じ' if J['env']['same'] else '違う', say(J['first']), say(J['second']),
527 |             '無い' if J.get('second_values_within_tol') is None else ('許容の内' if J['second_values_within_tol'] else '許容の外（止めずに台帳に記す・裁定 D234）'), say(J['agree']),
528 |             ('・理由 %s' % J['reason']) if J.get('reason') else ''))
529 |         if not J['agree']:
530 |             raise SystemExit('一致しない（結果を開く前に止め、逸脱の台帳に記して登録者に上げる・裁定 D219）')
531 |         return
532 |     jp = a.judge_record or JUDGE
533 |     if not os.path.exists(jp):
534 |         raise SystemExit('一致だけを見る段の記録が無い（結果を開かない）: %s' % jp)
535 |     J = json.load(open(jp, encoding='utf-8'))
536 |     out = a.out or OPENED
537 |     if os.path.exists(out):
538 |         raise SystemExit('既にある: %s' % out)
539 |     AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
540 |     CB = json.load(open(os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json'), encoding='utf-8'))['magnitude']['letter']
541 |     FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
542 |     A = open_checked(T3, FJ, parts, sessions, files, J, attempts, pair_names, AN, CB, FB, FR=FR, judge_sha16=sha16f(jp))
543 |     json.dump(A, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else float(o))
544 |     print('[analyze_Bl3] 結果を開いた: %s' % os.path.relpath(out, REPO))
545 | 
546 | 
547 | if __name__ == '__main__':
548 |     main()
```
<<< 終: `tools/analyze_Bl3.py` >>>

<<< 始: `tools/sweep_Bl3.py`（SHA16 2113222FB10DF222・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """sweep_Bl3.py v3 —— B-lens 層三（Bl3）の掃き出しの器（正本 `report_rules.builder`・草案3 §12「掃き出しの器」・2026-09-25）。
  3 | 
  4 | 正本と凍結の本文が求める出力の一覧（下の ROW_KEYS・SECOND_KEYS・PILOT_KEYS・GATES と、関数 sweep の中の need の行・出所の鍵つき）を、集計の器の結果を開く段の出力（`records/Bl3/analysis-Bl3.json`）と突き合わせ、欠けを返す。
  5 | 組み立ての器 `tools/build_report_Bl3.py` が報告を組む前に呼び、欠けがあれば止める。下見で止まったときの出力（下見の記録と予想の答えだけ）は、止まったときに求めるものだけを見る。
  6 | 本器は値の当否を見ない（有るか無いかと、行と升目と符号がそろうかだけ）。
  7 | 用法: python tools/sweep_Bl3.py <集計の出力の JSON> ／ --selftest（合成の出力は `tools/build_report_Bl3.py --selftest` が作って呼ぶ）
  8 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
  9 | """
 10 | import os, sys, json
 11 | 
 12 | HERE = os.path.dirname(os.path.abspath(__file__))
 13 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 14 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 層ごとの差分の中身と等方の本数を見る・頭の文／v2（裁定 D231）: 効き目の側は全ての行で・偶然の目安の分母
 15 | key3 = lambda sc, b, sg: '%s|%s|%+d' % (sc, b, int(sg))
 16 | 
 17 | ROW_KEYS = [('effect', 'labels.print_rule（行の値）'), ('p', 'labels.p_rule'), ('upper', 'labels.print_rule（上の裾の本数）'), ('lower', 'labels.print_rule（下の裾の本数）'),
 18 |             ('tail', 'report_rules.template（割合を決めた裾）'), ('holm_step', 'labels.iso_outside.rule'), ('iso_outside', 'labels.iso_outside.rule'),
 19 |             ('iso_median', 'labels.print_rule（等方の帰無の中央値）'), ('side', 'labels.side_rule'), ('iso_top_share', 'labels.second.iso_top_share'), ('second', 'labels.second')]
 20 | SECOND_KEYS = [('center', 'labels.second.center_why'), ('top', 'labels.second.rule'), ('rank_oriented', 'labels.second.ranks'), ('of_oriented', 'labels.second.ranks'),
 21 |                ('rank_pair', 'labels.second.ranks'), ('of_pair', 'labels.second.ranks')]
 22 | PILOT_KEYS = [('logit_check', 'computation.self_checks.logit'), ('vi', 'pilot.checks.vi'), ('batch', 'pilot.decision.report'), ('floor', 'pilot.decision.report'),
 23 |               ('cache_tol', 'pilot.cache_tol_rule'), ('cells', 'pilot.checks.i・ii・iii'), ('iii', 'pilot.checks.iii'), ('iv', 'pilot.checks.iv'), ('v', 'pilot.checks.v'), ('decision', 'pilot.decision')]
 24 | GATES = [('main', 'gate.test'), ('without_vhat', 'gate.without_vhat'), ('desc_without_vhat_loaded', 'gate.descriptive_gates[0]'), ('desc_choice_a', 'gate.descriptive_gates[1]'),
 25 |          ('desc_without_style', 'gate.descriptive_gates[2]')]
 26 | 
 27 | 
 28 | def sweep(T3, A):
 29 |     """欠けの一覧（空なら欠け無し）。"""
 30 |     miss = []
 31 |     need = lambda cond, what: None if cond else miss.append(what)
 32 |     atts = A.get('pilot_attempts') or []
 33 |     need(atts, 'pilot_attempts（pilot.decision.report）')
 34 |     need(set(A.get('predictions_truth') or {}) == {it['key'] for it in T3['predictions']['items']}, 'predictions_truth の項目（predictions.items）')
 35 |     if not atts:
 36 |         return miss
 37 |     last = atts[-1]
 38 |     stopped = bool((A.get('predictions_meta') or {}).get('stopped'))
 39 |     if last.get('tool_error'):
 40 |         return miss
 41 |     dec = last.get('decision') or {}
 42 |     vi_stop = dec.get('stop') and dec.get('reason') == 'vi_b'
 43 |     for k, src in PILOT_KEYS:
 44 |         if vi_stop and k in ('cells', 'iii', 'iv', 'v'):
 45 |             continue
 46 |         need(k in last, '下見の記録の %s（%s）' % (k, src))
 47 |     if 'vi' in last:
 48 |         need('a' in last['vi'] and 'b' in last['vi'], '下見の (vi) の (a) と (b)（pilot.decision.report）')
 49 |     if stopped:
 50 |         return miss
 51 |     # 主の札（下見で外した升目の行を除いたすべての主の行）
 52 |     dropped = set(dec.get('dropped') or [])
 53 |     want_rows = [r['id'] for r in T3['main_rows'] if '%s|%s' % (r['scenario'], r['base']) not in dropped]
 54 |     rows = A.get('rows') or {}
 55 |     need(list(rows) == want_rows, '主の行（下見で外した後の全ての行・labels.iso_outside.rule）')
 56 |     for rid, o in rows.items():
 57 |         for k, src in ROW_KEYS:
 58 |             need(k in o, '行 %s の %s（%s）' % (rid, k, src))
 59 |         for k, src in SECOND_KEYS:
 60 |             need(k in (o.get('second') or {}), '行 %s の二つ目の札の %s（%s）' % (rid, k, src))
 61 |         need(o.get('side') is not None, '行 %s の効き目の側（labels.print_rule・どの行にも・裁定 D231）' % rid)
 62 |     need('m_rows' in (A.get('rows_meta') or {}) and 'dropped_rows' in (A.get('rows_meta') or {}), 'Holm の段の数と外した行（pilot.decision.drop_effects）')
 63 |     need(set((A.get('chance') or {})) >= {'oriented', 'pair', 'rows_by_direction'}, '二つ目の札の偶然の目安と、外した後の行の数（nulls.real.chance_note・pilot.decision.drop_effects）')
 64 |     # 門
 65 |     G = A.get('gates') or {}
 66 |     for k, src in GATES:
 67 |         g = G.get(k)
 68 |         need(g is not None, '門 %s（%s）' % (k, src))
 69 |         if g is not None:
 70 |             need('n_rows' in g and 'units' in g and (g.get('undetermined') or {'n_perm', 'rho', 'p', 'pass'} <= set(g)), '門 %s の行・単位・入れ替えの数・順位相関・p（gate.dropped）' % k)
 71 |     # 記述
 72 |     main_keys = [key3(sc, b, sg) for sc, b, sg in T3['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
 73 |     D = A.get('descriptive') or {}
 74 |     need(set(main_keys) <= set(D.get('pa_noop') or {}), '升目と符号ごとの無操作の選択肢 a の確率（裁定 D223）')
 75 |     need(set(main_keys) <= set(D.get('mass_below_min') or {}), '質量が下限を下回った方向の数（descriptive.mass）')
 76 |     LW = A.get('layerwise') or {}
 77 |     need(set(main_keys) <= set(LW), '層ごとの差分（主の組の升目と符号・descriptive.layerwise.directions）')
 78 |     need('n_iso' in A and (A.get('dry') or A.get('n_iso') == T3['nulls']['isotropic']['count']), '等方の本数（DRY でなければ正本の本数・nulls.isotropic.count）')
 79 |     units = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
 80 |     for k in main_keys:
 81 |         lw = LW.get(k) or {}
 82 |         need({'noop_lo', 'rows', 'iso_summary'} <= set(lw), '層ごとの差分の %s の行と等方の中央値と中央の区間（descriptive.layerwise）' % k)
 83 |         n_lay = len(lw.get('noop_lo') or {})
 84 |         need(n_lay > 0 and sorted((lw.get('rows') or {})) == sorted(units) and all(len(v) == n_lay for v in (lw.get('rows') or {}).values()),
 85 |              '層ごとの差分の %s の名前のある方向と段階 B の三本の行が、層の数だけそろう（descriptive.layerwise.directions）' % k)
 86 |         iso_s = lw.get('iso_summary') or {}
 87 |         need(iso_s.get('n') == A.get('n_iso') and all(len(iso_s.get(x) or []) == n_lay for x in ('median', 'lo', 'hi')),
 88 |              '層ごとの差分の %s の等方の中央値と中央の区間が、等方の本数と層の数でそろう（descriptive.layerwise.band）' % k)
 89 |     S2 = A.get('secondary') or {}
 90 |     need(S2.get('summary') and all('blens_direct' in v for v in S2['summary'].values()), '乙と B-lens の直接の経路の値（descriptive.secondary_readout）')
 91 |     H = A.get('head') or {}
 92 |     need('logit_check' in H and 'layer_check' in H, '本の計算の頭の自己検査（computation.self_checks）')
 93 |     need('shortcut' in H and 'shortcut' in (A.get('main_run') or {}), '本の計算の近道の使い方（computation.shortcut・裁定 D234）')
 94 |     # 独立の再計算
 95 |     rc = A.get('recompute') or {}
 96 |     for st in ('first', 'second'):
 97 |         x = rc.get(st)
 98 |         need(x is not None and {'agree', 'max_abs_diff', 'values_within_tol', 'labels_same'} <= set(x), '独立の再計算の %s（independent_recompute.stages）' % st)
 99 |     need('tol_first' in rc and 'tol_second' in rc, '独立の再計算の許容（independent_recompute.stages）')
100 |     # 段階 B の注
101 |     N = A.get('stage_b_notes') or {}
102 |     need(set(want_rows) <= set(N.get('main') or {}), '主の行の段階 B の注（report_rules.template）')
103 |     need('gate' in N, '門の行の段階 B の注（report_rules.template）')
104 |     return miss
105 | 
106 | 
107 | if __name__ == '__main__':
108 |     if len(sys.argv) != 2 or sys.argv[1] == '--selftest':
109 |         sys.exit('用法: python tools/sweep_Bl3.py <集計の出力の JSON>（合成の確かめは tools/build_report_Bl3.py --selftest）')
110 |     T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
111 |     m = sweep(T3, json.load(open(sys.argv[1], encoding='utf-8')))
112 |     print('[sweep_Bl3] 欠け %d%s' % (len(m), ''.join('\n  - ' + x for x in m)))
113 |     sys.exit(1 if m else 0)
```
<<< 終: `tools/sweep_Bl3.py` >>>
