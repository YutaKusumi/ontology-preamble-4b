（B-lens 層三の器についての意見伺いの束・分けた版 3／5・中身は一通版と同じ）

==================== 第五部 残差の書き換えの道（別の個体が本の器の中を見ずに書いた）とその開発の記録 ====================

<<< 始: `tools/bl3_recompute_rewrite.py`（SHA16 012CB2B68397614A・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """bl3_recompute_rewrite.py v1 —— B-lens 層三（Bl3）の独立の再計算の器のうち、**残差の書き換えの道**
  3 | （2026-09-25・本の器の書き手〔コーディネータ〕と別の系統内の個体が書いた・登録者の許可による・独立の目を通っていない）。
  4 | 
  5 | 正本 `design/contrasts-Bl3.json` の `independent_recompute`（一段目の相手）・`readout.primary`・`layers`・`computation` に従う。
  6 | コーディネータのフックの道（`tools/bl3_run.py`）の中身を**読まずに**書いた。`--dry` でだけ、その公開の関数を中を見ずに呼び、数を突き合わせる。
  7 | 
  8 | 道（加減をフックでなく、選んだ層の出力を書き換えて後の層を流す・近道なし・バッチ一）:
  9 |   入力     段階 B の組み立てのままのプロンプト（`steer_B.apply_chat(tok, run_stageB_local.user_message(腕の本文, 場面の本文, 指示))`・
 10 |            場面と指示は `run_stageB_local.scenario_and_instruction`）の直後に、主の書き出し（転記行 A の `prefix_ids`）を
 11 |            **トークンの並びのまま**つなぐ。升目ごとに、プロンプトの長さ・主位置（`steer_B.main_position`）・読み取りの位置（列の最後）・
 12 |            族・前置きの SHA16 を転記行 B の升目の記録と照らし、違えば止める。
 13 |   層を回す 埋め込み → 層 0〜L → 層 L の出力を書き換え → 層 L+1〜最後。層の部品は、模型の forward（transformers 4.57.3 の
 14 |            `Qwen3Model.forward`）と同じ引数で一つずつ呼ぶ。L＝`direction_B.layer_index(layers.selected_ratio, 模型の層の数)`（本物の模型では正本 `layers.indices` の値）。
 15 |            位置の埋め込み（rotary）は模型の `rotary_emb` を、因果の注意の窓（mask）は模型の組み立てと同じ関数（`create_causal_mask`・
 16 |            窓つきの層があれば `create_sliding_window_causal_mask`）を、模型の forward と同じ引数で呼ぶ。`use_cache` の既定も模型の forward と同じ
 17 |            `config.use_cache` で、そのときは一回の順伝播ごとに空の cache を作って捨てる（順伝播をまたいで使い回さない＝近道ではない）。
 18 |   書き換え 層 L の出力の、主位置から列の最後までの位置に `sign × coef × v` を足す。v（float64）は段階 B の走行器のフックと同じ算術で、
 19 |            NumPy の float32 を経て層の出力の型（bf16）に直してから `sign * coef *` を掛け、bf16 のまま足す（係数は一度だけ）。
 20 |   読み取り 最後の層の出口の残差（**最終の正規化の入力**。transformers 4.57.3 の `hidden_states[-1]` は正規化の後の値なので使わない）の
 21 |            最後の位置を float32 に上げ、最終の正規化を float32 で当て（h × rsqrt(mean(h²)+eps) × g・g は `model.model.norm.weight` の float32）、
 22 |            語彙の行列（`lm_head.weight`）の読み取りの集合の行（族の選択の文字の順で a が先頭・最後に refuse の頭）を float32 で当てる。
 23 |            量＝z_a − logsumexp（ほかの選択の文字と refuse の頭）。効き目＝加えた値 − 無操作（零のベクトル）の値。
 24 | 出力: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}（符号の書き方は '%+d'）。
 25 | **値は印字しない**（正本 `independent_recompute.print`——本物の模型の値を開くのは登録者と一緒に開いた後）。`--dry` が差の最大を印字するのは乱数の小さな模型だけ。
 26 | **フックは使わない**: 呼ぶ前と後に、模型のどの部品にも forward の hook（前・後・大域）が無いことを確かめ、あれば止める（フックの道の掛け残しも混ぜない）。
 27 | 用法: python tools/bl3_recompute_rewrite.py --selftest   （乱数の小さな模型で自己検査）
 28 |       python tools/bl3_recompute_rewrite.py --dry        （乱数の小さな模型で、フックの道と一段目の許容で突き合わせ、差の最大を印字する。
 29 |                                                           参考に、この道をわざと誤らせた歯の変種がフックの道との差で捕まるかも印字する——判定に入れない）
 30 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 31 | """
 32 | import os, sys, json, time, copy, argparse
 33 | sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 34 | import numpy as np
 35 | 
 36 | VERSION = 'v1'
 37 | REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 38 | CANON_PATH = os.path.join(REPO, 'design', 'contrasts-Bl3.json')
 39 | FACTS_PATH = os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json')
 40 | # トークナイザと設定の置き場（手元・**実の重みは読まない**——乱数の小さな模型は設定だけを借りて作る）
 41 | SNAP = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub', 'models--Qwen--Qwen3-4B-Instruct-2507',
 42 |                     'snapshots', 'cdbee75f17c01a7cc42f958dc650907174af0554')
 43 | TINY = {'hidden_size': 64, 'num_hidden_layers': 4, 'num_attention_heads': 4, 'num_key_value_heads': 2,
 44 |         'head_dim': 16, 'intermediate_size': 128}
 45 | NORM_REL_TOL = 1e-6      # 方向のノルムを ‖static‖ と照らす相対の許容（段階 B の `load_directions` と同じ値）
 46 | FENCE = '本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
 47 | 
 48 | 
 49 | def _die(msg):
 50 |     raise SystemExit('bl3_recompute_rewrite: ' + msg)
 51 | 
 52 | 
 53 | def load_canon():
 54 |     return json.load(open(CANON_PATH, encoding='utf-8'))
 55 | 
 56 | 
 57 | def load_facts():
 58 |     return json.load(open(FACTS_PATH, encoding='utf-8'))
 59 | 
 60 | 
 61 | def _facts(FJ):
 62 |     """設計事実は、ファイルの全体（'facts' の鍵を持つ）でも、その 'facts' の中身でも受ける（正本は FJ の形を決めていない）。"""
 63 |     return FJ['facts'] if isinstance(FJ, dict) and 'facts' in FJ else FJ
 64 | 
 65 | 
 66 | # ---------------------------------------------------------------- 確かめ（止める）
 67 | 
 68 | def check_env(model, T3):
 69 |     """版と機種の確かめ。手回しの道は transformers 4.57.3 の `Qwen3Model.forward` を写しているので、版が違えば止める。"""
 70 |     import transformers
 71 |     want = str(T3['inputs']['versions_B']['transformers'])
 72 |     if transformers.__version__ != want:
 73 |         _die('transformers の版が %s（手回しの道は %s の Qwen3Model.forward を写した・正本 inputs.versions_B）'
 74 |              % (transformers.__version__, want))
 75 |     core = getattr(model, 'model', None)
 76 |     if core is None or type(core).__name__ != 'Qwen3Model':
 77 |         _die('模型の本体が Qwen3Model でない: %s' % type(core).__name__)
 78 |     if getattr(model, 'lm_head', None) is None:
 79 |         _die('語彙の行列（lm_head）が無い')
 80 |     if model.training:
 81 |         _die('模型が訓練の形（eval にしていない）')
 82 |     import torch
 83 |     if core.embed_tokens.weight.dtype != torch.bfloat16:
 84 |         _die('模型の型が bf16 でない（%s・正本 readout.primary.precision——順伝播と加減は段階 B と同じ bf16）'
 85 |              % core.embed_tokens.weight.dtype)
 86 |     eps = float(core.norm.variance_epsilon)
 87 |     if eps != float(model.config.rms_norm_eps):
 88 |         _die('最終の正規化の eps（%r）が設定の rms_norm_eps（%r）と違う' % (eps, model.config.rms_norm_eps))
 89 |     n = len(core.layers)
 90 |     if n != int(model.config.num_hidden_layers):
 91 |         _die('層の並びの数（%d）が設定の層の数（%d）と違う' % (n, model.config.num_hidden_layers))
 92 | 
 93 | 
 94 | def assert_no_forward_hooks(model):
 95 |     """模型のどの部品にも forward の hook（前・後）が無く、大域の hook も無いこと（残差の書き換えの道はフックを使わない）。"""
 96 |     import torch.nn.modules.module as M
 97 |     bad = []
 98 |     for name, m in model.named_modules():
 99 |         for attr in ('_forward_hooks', '_forward_pre_hooks'):
100 |             d = getattr(m, attr, None)
101 |             if d:
102 |                 bad.append('%s.%s %d 本' % (name or '<模型>', attr, len(d)))
103 |     for attr in ('_global_forward_hooks', '_global_forward_pre_hooks'):
104 |         d = getattr(M, attr, None)
105 |         if d:
106 |             bad.append('大域の %s %d 本' % (attr, len(d)))
107 |     if bad:
108 |         _die('模型に forward の hook が掛かっている（残差の書き換えの道はフックを使わず、掛け残しも混ぜない）: ' + '・'.join(bad))
109 | 
110 | 
111 | def check_layer_and_coef(model, T3, layer_idx, coef):
112 |     """層の添字＝`direction_B.layer_index(layers.selected_ratio, 模型の層の数)`、係数＝`layers.coef_applied`。違えば止める。"""
113 |     import direction_B
114 |     n_layers = len(direction_B.decoder_layers(model))
115 |     ratio = float(T3['layers']['selected_ratio'])
116 |     want = direction_B.layer_index(ratio, n_layers)
117 |     if int(layer_idx) != want:
118 |         _die('層の添字 %s が正本の規則と違う（層の割合 %s・層の数 %d なら %d）' % (layer_idx, ratio, n_layers, want))
119 |     if n_layers == int(T3['inputs']['model']['num_hidden_layers']):
120 |         keyed = {float(k): int(v) for k, v in T3['layers']['indices'].items()}
121 |         if keyed.get(ratio) != int(layer_idx):
122 |             _die('層の添字 %s が正本 layers.indices（%s）と違う' % (layer_idx, keyed.get(ratio)))
123 |     if float(coef) != float(T3['layers']['coef_applied']):
124 |         _die('係数 %r が正本 layers.coef_applied（%r）と違う' % (coef, T3['layers']['coef_applied']))
125 | 
126 | 
127 | # ---------------------------------------------------------------- 升目の入力（段階 B の組み立てのまま）
128 | 
129 | def cell_input(tok, T3, FJ, cell_key, _AT=None):
130 |     """升目（'場面|土台の腕'）の入力を組み立て、転記行 B の升目の記録と照らす（違えば止める）。
131 | 
132 |     返り値: {'cell', 'ids'（プロンプト＋主の書き出し）, 'prompt_len', 'mp'（主位置）, 'ro'（読み取りの位置＝列の最後）,
133 |              'family', 'letters', 'read_ids'（族の選択の文字の順・a が先頭・最後に refuse の頭）}。"""
134 |     import run_stageB_local as RB
135 |     import steer_B
136 |     F = _facts(FJ)
137 |     cells = F['B']['cells']
138 |     if cell_key not in cells:
139 |         _die('升目 %s が転記行 B（facts.B.cells）に無い' % cell_key)
140 |     cf = cells[cell_key]
141 |     parts = cell_key.split('|')
142 |     if len(parts) != 2:
143 |         _die('升目の鍵の形が違う（場面|土台の腕）: %s' % cell_key)
144 |     scen, base = parts
145 |     s, inst = RB.scenario_and_instruction(scen)
146 |     AT = _AT if _AT is not None else RB.arm_texts()
147 |     if base not in AT:
148 |         _die('土台の腕 %s の本文が引けない' % base)
149 |     prompt = list(steer_B.apply_chat(tok, RB.user_message(AT[base]['text'], s['text'], inst)))
150 |     prefix = [int(x) for x in F['A']['prefix_ids']]
151 |     ids = prompt + prefix
152 |     mp = int(steer_B.main_position(prompt))
153 |     ro = len(ids) - 1
154 |     fam = s.get('family')
155 |     RP = T3['readout']['primary']
156 |     bad = []
157 |     if len(prompt) != int(cf['prompt_len']):
158 |         bad.append('プロンプトの長さ %d（転記 %s）' % (len(prompt), cf['prompt_len']))
159 |     if mp != int(cf['main_position']) or mp != len(prompt) - 1:
160 |         bad.append('主位置 %d（転記 %s・プロンプトの長さ−1 は %d）' % (mp, cf['main_position'], len(prompt) - 1))
161 |     if ro != int(cf['readout_position']):
162 |         bad.append('読み取りの位置 %d（転記 %s）' % (ro, cf['readout_position']))
163 |     if fam != cf.get('family'):
164 |         bad.append('族 %s（転記 %s）' % (fam, cf.get('family')))
165 |     if cf.get('preamble_sha16') and AT[base].get('sha16') != cf['preamble_sha16']:
166 |         bad.append('前置きの SHA16 %s（転記 %s）' % (AT[base].get('sha16'), cf['preamble_sha16']))
167 |     if tok.decode(prefix) != F['A']['prefix']:
168 |         bad.append('主の書き出しの並びが転記の文字列に戻らない')
169 |     if fam not in RP['letters']:
170 |         bad.append('族 %s の選択の文字が正本に無い' % fam)
171 |     if bad:
172 |         _die('升目 %s の入力が転記行 B と違う: %s' % (cell_key, '・'.join(bad)))
173 |     letters = list(RP['letters'][fam])
174 |     if letters[0] != RP['catastrophe_letter']:
175 |         _die('選択の文字の先頭が破局の側の文字（%s）でない: %s' % (RP['catastrophe_letter'], letters))
176 |     LI = F['A']['letter_ids']
177 |     read_ids = [int(LI[x]) for x in letters] + [int(LI['refuse'])]
178 |     want_tokens = letters + [RP['refuse_head']]
179 |     got_tokens = [tok.convert_ids_to_tokens(i) for i in read_ids]
180 |     if got_tokens != want_tokens:
181 |         _die('読み取りの集合のトークンが文字に戻らない: %s 対 %s' % (got_tokens, want_tokens))
182 |     if len(set(read_ids)) != len(read_ids):
183 |         _die('読み取りの集合のトークンが重なる: %s' % read_ids)
184 |     return {'cell': cell_key, 'ids': ids, 'prompt_len': len(prompt), 'mp': mp, 'ro': ro,
185 |             'family': fam, 'letters': letters, 'read_ids': read_ids}
186 | 
187 | 
188 | # ---------------------------------------------------------------- 残差の書き換えの道
189 | 
190 | def forward_rewrite(model, ids, layer_idx, vec, coef, sign, mp, use_cache=None, keep=None):
191 |     """埋め込みから層を手で回し、層 layer_idx の出力の主位置から列の最後までに sign×coef×v を足して後の層を流す。
192 | 
193 |     返り値: 最後の層の出口の残差（最終の正規化の入力・層の出力の型・形 [1, 列の長さ, 次元]）。
194 |     use_cache が None なら模型の forward と同じく `config.use_cache` を使う（一回ごとに空の cache を作って捨てる）。
195 |     keep（dict）を渡すと、自己検査のために層ごとの出力（書き換えの後）・書き換えの前と後・足した量を写しで残す。"""
196 |     import torch
197 |     import transformers.models.qwen3.modeling_qwen3 as MQ        # 模型の組み立てが呼ぶのと同じ名の束ね（mask・cache）
198 |     core = model.model
199 |     cfg = core.config
200 |     layers = core.layers[: cfg.num_hidden_layers]                   # Qwen3Model.forward と同じ切り方
201 |     n = len(ids)
202 |     L = int(layer_idx)
203 |     if not 0 <= L < len(layers):
204 |         _die('層の添字 %s が範囲の外（層の数 %d）' % (layer_idx, len(layers)))
205 |     if not 0 <= int(mp) < n:
206 |         _die('主位置 %s が列の外（長さ %d）' % (mp, n))
207 |     if int(sign) not in (1, -1):
208 |         _die('符号は +1 か -1: %r' % (sign,))
209 |     if use_cache is None:
210 |         use_cache = getattr(cfg, 'use_cache', None)                 # check_model_inputs の既定と同じ
211 |     use_cache = bool(use_cache)
212 |     V32 = np.asarray(vec, dtype=np.float32)                         # 段階 B の走行器のフックと同じく NumPy の float32 を経る
213 |     if V32.shape != (int(cfg.hidden_size),):
214 |         _die('方向の形 %s が次元（%d）と合わない' % (V32.shape, cfg.hidden_size))
215 |     done = 0
216 |     with torch.no_grad():
217 |         input_ids = torch.tensor([list(ids)], dtype=torch.long, device=core.embed_tokens.weight.device)
218 |         inputs_embeds = core.embed_tokens(input_ids)
219 |         past = MQ.DynamicCache(config=cfg) if use_cache else None
220 |         cache_position = torch.arange(0, inputs_embeds.shape[1], device=inputs_embeds.device)
221 |         position_ids = cache_position.unsqueeze(0)
222 |         mk = dict(config=cfg, input_embeds=inputs_embeds, attention_mask=None, cache_position=cache_position,
223 |                   past_key_values=past, position_ids=position_ids)
224 |         masks = {'full_attention': MQ.create_causal_mask(**mk)}
225 |         if core.has_sliding_layers:
226 |             masks['sliding_attention'] = MQ.create_sliding_window_causal_mask(**mk)
227 |         if keep is not None:
228 |             keep['masks'] = masks
229 |         h = inputs_embeds
230 |         pe = core.rotary_emb(h, position_ids)                       # (cos, sin)・模型の forward と同じく全層で共有
231 |         for i, layer in enumerate(layers):
232 |             h = layer(h, attention_mask=masks[layer.attention_type], position_ids=position_ids,
233 |                       past_key_values=past, use_cache=use_cache, cache_position=cache_position,
234 |                       position_embeddings=pe)
235 |             if i == L:
236 |                 if keep is not None:
237 |                     keep['L_before'] = h.clone()
238 |                 # **層の出力の型に直してから sign×coef を掛け、主位置から後ろに足す**（段階 B の走行器のフックの算術と同じ形）
239 |                 add = int(sign) * float(coef) * torch.as_tensor(V32, dtype=h.dtype, device=h.device)
240 |                 h[0, int(mp):, :] = h[0, int(mp):, :] + add
241 |                 done += 1
242 |                 if keep is not None:
243 |                     keep['L_after'] = h.clone()
244 |                     keep['add'] = add.clone()
245 |             if keep is not None:
246 |                 keep.setdefault('outs', []).append(h.clone())
247 |     if done != 1:
248 |         _die('書き換えが一度でない: %d 回' % done)
249 |     if h.shape[1] != n:
250 |         _die('出口の列の長さ %d が入力の長さ %d と違う' % (h.shape[1], n))
251 |     return h
252 | 
253 | 
254 | def readout(model, h_last, read_ids):
255 |     """最終の正規化の入力（一つの位置）を float32 に上げ、最終の正規化と読み取りの集合の行を float32 で当てる。
256 | 
257 |     返り値: (量〔z_a − logsumexp(ほか)〕, 出口の値 z〔float32・read_ids の順〕)。"""
258 |     import torch
259 |     with torch.no_grad():
260 |         g = model.model.norm.weight.to(torch.float32)
261 |         x = h_last.to(device=g.device, dtype=torch.float32)          # 層が複数の装置に割られていても正規化の重みの装置で当てる
262 |         eps = float(model.model.norm.variance_epsilon)
263 |         xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g
264 |         W = model.lm_head.weight
265 |         idx = torch.as_tensor(list(read_ids), dtype=torch.long, device=W.device)
266 |         z = W.index_select(0, idx).to(torch.float32) @ xn.to(W.device)
267 |         lo = z[0] - torch.logsumexp(z[1:], dim=0)
268 |     return float(lo), z
269 | 
270 | 
271 | def _check_dirs(model, dirs, used):
272 |     d = int(model.config.hidden_size)
273 |     for dn in used:
274 |         if dn not in dirs:
275 |             _die('方向 %s が dirs に無い' % dn)
276 |         v = dirs[dn]
277 |         if not isinstance(v, np.ndarray) or v.dtype != np.float64:
278 |             _die('方向 %s が float64 の配列でない（%s）' % (dn, getattr(v, 'dtype', type(v).__name__)))
279 |         if v.shape != (d,):
280 |             _die('方向 %s の形 %s が次元（%d）と合わない' % (dn, v.shape, d))
281 |         if not np.all(np.isfinite(v)):
282 |             _die('方向 %s に有限でない値がある' % dn)
283 |     if 'static' in dirs:
284 |         ns = float(np.linalg.norm(dirs['static']))
285 |         for dn in used:
286 |             nv = float(np.linalg.norm(dirs[dn]))
287 |             if nv != 0.0 and abs(nv - ns) > NORM_REL_TOL * max(ns, 1.0):
288 |                 _die('方向 %s のノルム（%.9g）が ‖static‖（%.9g）に揃っていない（正本 directions.norm_rule）' % (dn, nv, ns))
289 | 
290 | 
291 | def recompute_rewrite(model, tok, T3, FJ, rows, dirs_by_row, dirs, layer_idx, coef, use_cache=None):
292 |     """残差の書き換えの道で、行ごとに無操作の量と、方向と符号ごとの効き目を計算し直す（近道なし・バッチ一）。
293 | 
294 |     rows: [(行の名, 升目の鍵 '場面|土台の腕', 符号)]。dirs_by_row: 行の名 → [(方向の名, 符号)]。dirs: 方向の名 → float64 のベクトル。
295 |     返り値: {行の名: {'noop_lo': 無操作の量, 'effects': {'方向の名|符号': 効き目}}}。**値は印字しない。**
296 |     use_cache（既定 None＝模型の forward と同じ `config.use_cache`）は、手回しの道の mask の組み方を模型の forward のどの呼び方に
297 |     合わせるかだけを決める（数の上の意味は同じ・開発の記録の「決まっていなかった所」を見よ）。"""
298 |     check_env(model, T3)
299 |     check_layer_and_coef(model, T3, layer_idx, coef)
300 |     assert_no_forward_hooks(model)
301 |     rows = [tuple(r) for r in rows]
302 |     for r in rows:
303 |         if len(r) != 3:
304 |             _die('行は（行の名, 升目の鍵, 符号）の三つ組: %r' % (r,))
305 |     names = [r[0] for r in rows]
306 |     if len(set(names)) != len(names):
307 |         _die('行の名が重なる')
308 |     missing = [nm for nm in names if nm not in dirs_by_row]
309 |     if missing:
310 |         _die('dirs_by_row に行が無い: %s' % '・'.join(missing))
311 |     used = sorted({dn for nm in names for dn, _ in dirs_by_row[nm]})
312 |     _check_dirs(model, dirs, used)
313 |     canon_rows = {r['id']: r for r in T3['main_rows']}
314 |     import run_stageB_local as RB
315 |     AT = RB.arm_texts()
316 |     d = int(model.config.hidden_size)
317 |     zero = np.zeros(d, dtype=np.float64)                            # 無操作は零のベクトル（正本 readout.primary.batching）
318 |     cells, out = {}, {}
319 |     for name, ck, sign in rows:
320 |         sign = int(sign)
321 |         if sign not in (1, -1):
322 |             _die('行 %s の符号は +1 か -1: %r' % (name, sign))
323 |         if name in canon_rows:
324 |             cr = canon_rows[name]
325 |             if ck != '%s|%s' % (cr['scenario'], cr['base']) or sign != int(cr['sign']):
326 |                 _die('行 %s の升目か符号が正本 main_rows と違う（%s %+d 対 %s|%s %+d）'
327 |                      % (name, ck, sign, cr['scenario'], cr['base'], int(cr['sign'])))
328 |         if ck not in cells:
329 |             cells[ck] = cell_input(tok, T3, FJ, ck, _AT=AT)
330 |         c = cells[ck]
331 |         h0 = forward_rewrite(model, c['ids'], layer_idx, zero, coef, sign, c['mp'], use_cache=use_cache)
332 |         if h0.shape[1] - 1 != c['ro']:
333 |             _die('読み取りの位置が列の最後でない')
334 |         lo0, _ = readout(model, h0[0, -1], c['read_ids'])
335 |         eff = {}
336 |         for dn, s in dirs_by_row[name]:
337 |             s = int(s)
338 |             if s not in (1, -1):
339 |                 _die('方向 %s の符号は +1 か -1: %r' % (dn, s))
340 |             key = '%s|%+d' % (dn, s)
341 |             if key in eff:
342 |                 _die('行 %s に同じ方向と符号が二度ある: %s' % (name, key))
343 |             h = forward_rewrite(model, c['ids'], layer_idx, dirs[dn], coef, s, c['mp'], use_cache=use_cache)
344 |             lo, _ = readout(model, h[0, -1], c['read_ids'])
345 |             eff[key] = lo - lo0
346 |         out[name] = {'noop_lo': lo0, 'effects': eff}
347 |     assert_no_forward_hooks(model)
348 |     return out
349 | 
350 | 
351 | # ---------------------------------------------------------------- 乱数の小さな模型と合成の方向（確かめだけに使う）
352 | 
353 | def tiny_model():
354 |     """乱数の小さな模型（設定だけを手元の置き場から借りる・**実の重みは読まない**）。コーディネータの合成の器と同じ作り方を自分で書いた。"""
355 |     import torch
356 |     from transformers import AutoConfig, AutoModelForCausalLM
357 |     cfg = AutoConfig.from_pretrained(SNAP)
358 |     (cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim,
359 |      cfg.intermediate_size) = (TINY['hidden_size'], TINY['num_hidden_layers'], TINY['num_attention_heads'],
360 |                                TINY['num_key_value_heads'], TINY['head_dim'], TINY['intermediate_size'])
361 |     cfg.layer_types = list(cfg.layer_types)[:TINY['num_hidden_layers']]   # 元の長さのままだと空の層ができる
362 |     torch.manual_seed(0)
363 |     model = AutoModelForCausalLM.from_config(cfg)
364 |     g = torch.Generator().manual_seed(1)
365 |     with torch.no_grad():
366 |         for name, p in model.named_parameters():                   # 初期値の一のままだと正規化の誤りが見えない
367 |             if name.endswith('norm.weight'):
368 |                 p.copy_(torch.rand(p.shape, generator=g) + 0.5)    # 一様乱数 [0.5, 1.5)
369 |     return model.to(torch.bfloat16).eval()
370 | 
371 | 
372 | def _assert_tiny(model):
373 |     """確かめは乱数の小さな模型だけで走らせる（封印の前に本物の模型で読み取りの値を出さない・正本 computation.before_seal）。"""
374 |     c = model.config
375 |     if (int(c.hidden_size), int(c.num_hidden_layers)) != (TINY['hidden_size'], TINY['num_hidden_layers']):
376 |         _die('確かめは乱数の小さな模型だけで走らせる（次元 %s・層 %s）' % (c.hidden_size, c.num_hidden_layers))
377 | 
378 | 
379 | def synthetic_dirs(FJ, d):
380 |     """合成の方向: `np.random.default_rng(5)` で次元 d の正規乱数を名の順に引き、static のノルムにそろえる。
381 |     名は static・iso:0〜iso:19・real:＋転記行 D の実在の差の対の名（その順）。"""
382 |     F = _facts(FJ)
383 |     names = ['static'] + ['iso:%d' % k for k in range(20)] + ['real:' + p for p in F['D']['real_pairs']]
384 |     rng = np.random.default_rng(5)
385 |     raw = [(nm, rng.normal(size=d)) for nm in names]
386 |     ns = float(np.linalg.norm(raw[0][1]))
387 |     dirs = {}
388 |     for nm, v in raw:
389 |         dirs[nm] = v if nm == 'static' else v * (ns / float(np.linalg.norm(v)))
390 |     return dirs, names
391 | 
392 | 
393 | def _static_rows(T3, FJ):
394 |     """主の行のうち方向が static の行から、減算の行（main_rows の順で最初）と加算の行（族を両方覆うため、減算の行と
395 |     違う族の最初の加算の行・無ければ最初の加算の行）を選ぶ。"""
396 |     F = _facts(FJ)
397 |     fam = lambda r: F['B']['cells']['%s|%s' % (r['scenario'], r['base'])]['family']
398 |     main = [r for r in T3['main_rows'] if r['direction'] == 'static']
399 |     sub = next(r for r in main if int(r['sign']) == -1)
400 |     add = next((r for r in main if int(r['sign']) == 1 and fam(r) != fam(sub)), None) or \
401 |         next(r for r in main if int(r['sign']) == 1)
402 |     return [(r['id'], '%s|%s' % (r['scenario'], r['base']), int(r['sign'])) for r in (sub, add)]
403 | 
404 | 
405 | def _max_abs_diff(A, B):
406 |     """二つの結果の、全ての効き目と無操作の量の差の絶対値の最大（鍵の集合が違えば None）。"""
407 |     if set(A) != set(B):
408 |         return None
409 |     de, dn, n = 0.0, 0.0, 0
410 |     for nm in A:
411 |         ea, eb = A[nm]['effects'], B[nm]['effects']
412 |         if set(ea) != set(eb):
413 |             return None
414 |         for k in ea:
415 |             de = max(de, abs(float(ea[k]) - float(eb[k])))
416 |             n += 1
417 |         dn = max(dn, abs(float(A[nm]['noop_lo']) - float(B[nm]['noop_lo'])))
418 |     return {'effects': de, 'noop': dn, 'n_effects': n}
419 | 
420 | 
421 | # ---------------------------------------------------------------- 自己検査
422 | 
423 | def _selftest():
424 |     import torch
425 |     import torch.nn as nn
426 |     from transformers import AutoTokenizer
427 |     import direction_B
428 |     T3, FJ = load_canon(), load_facts()
429 |     F = _facts(FJ)
430 |     tok = AutoTokenizer.from_pretrained(SNAP)
431 |     model = tiny_model()
432 |     _assert_tiny(model)
433 |     check_env(model, T3)
434 |     n_layers = len(direction_B.decoder_layers(model))
435 |     L = direction_B.layer_index(float(T3['layers']['selected_ratio']), n_layers)
436 |     coef = float(T3['layers']['coef_applied'])
437 |     d = int(model.config.hidden_size)
438 |     dirs, _ = synthetic_dirs(FJ, d)
439 |     zero = np.zeros(d, dtype=np.float64)
440 |     logit_tol = float(T3['computation']['logit_tol'])
441 |     res = []
442 | 
443 |     def ck(label, ok, detail=''):
444 |         res.append(bool(ok))
445 |         print('[%s] %s%s' % ('ok' if ok else 'NG', label, ('  | ' + detail) if detail else ''))
446 | 
447 |     def stops(fn):
448 |         try:
449 |             fn()
450 |         except SystemExit as e:
451 |             return True, str(e)
452 |         return False, ''
453 | 
454 |     import transformers
455 |     print('bl3_recompute_rewrite %s --selftest  torch %s・transformers %s・numpy %s・注意の実装 %s・config.use_cache %s'
456 |           % (VERSION, torch.__version__, transformers.__version__, np.__version__,
457 |              model.config._attn_implementation, model.config.use_cache))
458 |     print('乱数の小さな模型: 次元 %d・層 %d・注意の頭 %d・KV の頭 %d・頭の次元 %d・中間 %d・選んだ層の添字 %d・係数 %s'
459 |           % (d, n_layers, model.config.num_attention_heads, model.config.num_key_value_heads, model.config.head_dim,
460 |              model.config.intermediate_size, L, coef))
461 | 
462 |     # (1) 升目の組み立て
463 |     import run_stageB_local as RB
464 |     AT = RB.arm_texts()
465 |     C = {k: cell_input(tok, T3, FJ, k, _AT=AT) for k in F['B']['cells']}
466 |     ck('升目の組み立てが転記行 B と一致（全 %d 升目・長さ・主位置・読み取りの位置・族・前置きの SHA16・読み取りの集合のトークン）' % len(C), True,
467 |        '・'.join('%s %d/%d/%d' % (k, c['prompt_len'], c['mp'], c['ro']) for k, c in C.items()))
468 |     for fld, dv in (('prompt_len', 1), ('main_position', 1), ('readout_position', -1)):
469 |         F2 = copy.deepcopy(FJ)
470 |         _facts(F2)['B']['cells']['S1|O-Ncold'][fld] += dv
471 |         ok, msg = stops(lambda: cell_input(tok, T3, F2, 'S1|O-Ncold', _AT=AT))
472 |         ck('転記行 B と違えば止まる（S1|O-Ncold の %s を %+d ずらした写し）' % (fld, dv), ok)
473 |     F2 = copy.deepcopy(FJ)
474 |     _facts(F2)['A']['prefix_ids'] = list(_facts(F2)['A']['prefix_ids'])[:-1]
475 |     ok, _ = stops(lambda: cell_input(tok, T3, F2, 'S1|O-Ncold', _AT=AT))
476 |     ck('主の書き出しの割り方が変われば止まる（最後のトークンを落とした写し）', ok)
477 | 
478 |     # (2) 書き換えを零にした手回しの道の最終の正規化の入力 ＝ 模型そのものの forward の最終の正規化の入力（前の hook で取るだけ）
479 |     probe = [k for k in ('N1|Onull', 'S1|O-Ncold') if k in C]
480 |     for k in probe:
481 |         c = C[k]
482 |         x = torch.tensor([c['ids']], dtype=torch.long)
483 |         for uc, label in ((None, '既定（config.use_cache）'), (False, 'use_cache=False')):
484 |             cap = {}
485 |             hd = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('x', a[0].detach().clone()))
486 |             try:
487 |                 with torch.no_grad():
488 |                     o = model(input_ids=x, logits_to_keep=1) if uc is None else model(input_ids=x, use_cache=False, logits_to_keep=1)
489 |             finally:
490 |                 hd.remove()
491 |             assert_no_forward_hooks(model)
492 |             keep = {}
493 |             h = forward_rewrite(model, c['ids'], L, zero, coef, +1, c['mp'], use_cache=uc, keep=keep)
494 |             same = torch.equal(h, cap['x'])
495 |             md = float((h.float() - cap['x'].float()).abs().max())
496 |             ck('%s %s: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）' % (k, label), same,
497 |                '差の絶対値の最大 %.3g・形 %s・型 %s' % (md, tuple(h.shape), h.dtype))
498 |             mfa = keep['masks']['full_attention']
499 |             print('[参考] %s %s: 手回しの道が組んだ mask（full_attention）は %s（判定に入れない）'
500 |                   % (k, label, 'None（SDPA は is_causal で走る）' if mfa is None
501 |                      else '明示の mask（型 %s・形 %s）' % (mfa.dtype, tuple(mfa.shape))))
502 |             lo, z = readout(model, h[0, -1], c['read_ids'])
503 |             ref = o.logits[0, -1, c['read_ids']].float()
504 |             dz = float((z - ref).abs().max())
505 |             ck('%s %s: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内' % (k, label),
506 |                dz <= logit_tol, '差の絶対値の最大 %.3g（許容 %s）' % (dz, logit_tol))
507 |             if uc is None:
508 |                 with torch.no_grad():
509 |                     o2 = model.model(input_ids=x, output_hidden_states=True)
510 |                 hs = o2.hidden_states
511 |                 # 歯の確かめ: hidden_states[-1]（正規化の後）を正規化の入力と取り違えると正規化が二度掛かり、模型の出口の値からもっと離れる
512 |                 _, zw = readout(model, hs[-1][0, -1], c['read_ids'])
513 |                 dzw = float((zw - ref).abs().max())
514 |                 ck('%s: 歯の確かめ——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 4 倍を超える' % k,
515 |                    dzw > 4 * dz, '取り違え %.3g・正しい %.3g' % (dzw, dz))
516 |                 ck('%s: hidden_states[-1] は正規化の後（last_hidden_state と同じ・最終の正規化の入力と違う）' % k,
517 |                    torch.equal(hs[-1], o2.last_hidden_state) and not torch.equal(hs[-1], cap['x']))
518 |                 ck('%s: 手回しの層 %d の出力（書き換えの前）が hidden_states[%d]（layers.hidden_states_indices の対応）と一致（ビット単位）'
519 |                    % (k, L, direction_B.hidden_states_index(L)),
520 |                    torch.equal(keep['L_before'], hs[direction_B.hidden_states_index(L)]))
521 | 
522 |     # (3) 主位置より前の位置は書き換えない
523 |     for k, sign in (('S1|O-Ncold', -1), ('N1|Onull', +1)):
524 |         c = C[k]
525 |         mp = c['mp']
526 |         k0, k1 = {}, {}
527 |         h0 = forward_rewrite(model, c['ids'], L, zero, coef, sign, mp, keep=k0)
528 |         h1 = forward_rewrite(model, c['ids'], L, dirs['static'], coef, sign, mp, keep=k1)
529 |         pre_same = all(torch.equal(k0['outs'][i], k1['outs'][i]) for i in range(L))
530 |         ck('%s 符号 %+d: 層 %d より前の層の出力は無操作と同じ（ビット単位）' % (k, sign, L), pre_same)
531 |         ck('%s 符号 %+d: 層 %d の出力（書き換えの前）は無操作と同じ（ビット単位）' % (k, sign, L), torch.equal(k0['L_before'], k1['L_before']))
532 |         ck('%s 符号 %+d: 書き換えは主位置（%d）より前の位置を変えない（層 %d の出力・ビット単位）' % (k, sign, mp, L),
533 |            torch.equal(k1['L_after'][:, :mp], k1['L_before'][:, :mp]))
534 |         ck('%s 符号 %+d: 主位置から列の最後まで（%d 位置）に同じ量を足した（層 %d の出力・ビット単位）' % (k, sign, len(c['ids']) - mp, L),
535 |            torch.equal(k1['L_after'][:, mp:], k1['L_before'][:, mp:] + k1['add']))
536 |         dv = (k1['L_after'][0, mp:].float() - k1['L_before'][0, mp:].float()).double().numpy()
537 |         want = sign * coef * dirs['static']
538 |         cos = float(np.min(dv @ want / (np.linalg.norm(dv, axis=1) * np.linalg.norm(want))))
539 |         rel = float(np.max(np.abs(np.linalg.norm(dv, axis=1) / np.linalg.norm(want) - 1.0)))
540 |         ck('%s 符号 %+d: 足した量の向きと大きさが sign×coef×v（bf16 の丸めの内）' % (k, sign), cos > 0.9999 and rel < 0.01,
541 |            '余弦の最小 %.6f・ノルムの相対の差の最大 %.3g' % (cos, rel))
542 |         before_same = torch.equal(h1[:, :mp], h0[:, :mp])
543 |         band_diff = all(not torch.equal(h1[0, p], h0[0, p]) for p in range(mp, len(c['ids'])))
544 |         ck('%s 符号 %+d: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う' % (k, sign),
545 |            before_same and band_diff)
546 | 
547 |     # [参考・判定に入れない] 段階 B のフックの算術（NumPy の float32 を経て bf16）と、float64 から直に bf16 にした形が、合成の方向で同じか
548 |     n_same = sum(torch.equal(torch.as_tensor(np.asarray(v, dtype=np.float32), dtype=torch.bfloat16),
549 |                              torch.as_tensor(v, dtype=torch.bfloat16)) for v in dirs.values())
550 |     print('[参考] float32 を経た bf16 と float64 から直に直した bf16 が同じ合成の方向: %d/%d（判定に入れない）' % (n_same, len(dirs)))
551 | 
552 |     # (4) 零のベクトルの効き目は零・(5) 同じ呼び出しは同じ値
553 |     rows = _static_rows(T3, FJ)
554 |     dz_ = dict(dirs)
555 |     dz_['zero'] = zero
556 |     dbr = {nm: [('zero', +1), ('zero', -1), ('static', s)] for nm, _, s in rows}
557 |     r1 = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dz_, L, coef)
558 |     zeros_ok = all(r1[nm]['effects']['zero|+1'] == 0.0 and r1[nm]['effects']['zero|-1'] == 0.0 for nm, _, _ in rows)
559 |     ck('零のベクトルの効き目が零（両方の符号・%d 行: %s）' % (len(rows), '・'.join(nm for nm, _, _ in rows)), zeros_ok,
560 |        '・'.join('%s %r/%r' % (nm, r1[nm]['effects']['zero|+1'], r1[nm]['effects']['zero|-1']) for nm, _, _ in rows))
561 |     teeth = all(r1[nm]['effects']['static|%+d' % s] != 0.0 for nm, _, s in rows)
562 |     ck('歯の確かめ: static の効き目は零でない（乱数の小さな模型）', teeth,
563 |        '・'.join('%s %.3g' % (nm, r1[nm]['effects']['static|%+d' % s]) for nm, _, s in rows))
564 |     r2 = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dz_, L, coef)
565 |     ck('同じ呼び出しを二度走らせて同じ値（ビット単位）', r1 == r2)
566 |     shape_ok = all(set(r1[nm]) == {'noop_lo', 'effects'} and isinstance(r1[nm]['noop_lo'], float) for nm in r1)
567 |     ck('出力の形 {行の名: {noop_lo, effects: {方向の名|符号: 効き目}}}（符号の書き方 %+d）', shape_ok and
568 |        set(r1[rows[0][0]]['effects']) == {'zero|+1', 'zero|-1', 'static|%+d' % rows[0][2]},
569 |        '鍵の例 %s' % sorted(r1[rows[0][0]]['effects']))
570 | 
571 |     # (6) 止める確かめ
572 |     one = [rows[0]]
573 |     dbr1 = {rows[0][0]: [('static', rows[0][2])]}
574 |     h_ = direction_B.decoder_layers(model)[L].register_forward_hook(lambda m, i, o: o)
575 |     try:
576 |         ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L, coef))
577 |     finally:
578 |         h_.remove()
579 |     ck('模型に forward の hook が掛かっていれば止まる', ok)
580 |     ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L + 1, coef))
581 |     ck('層の添字が正本の規則と違えば止まる', ok)
582 |     ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L, coef * 2))
583 |     ck('係数が正本 layers.coef_applied と違えば止まる', ok)
584 |     bad = dict(dirs)
585 |     bad['static'] = dirs['static'].astype(np.float32)
586 |     ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, dbr1, bad, L, coef))
587 |     ck('方向が float64 でなければ止まる', ok)
588 |     bad = dict(dirs)
589 |     bad['iso:0'] = dirs['iso:0'] * 1.01
590 |     ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, one, {rows[0][0]: [('iso:0', rows[0][2])]}, bad, L, coef))
591 |     ck('方向のノルムが ‖static‖ に揃っていなければ止まる', ok)
592 |     ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, [(rows[0][0], rows[0][1], -rows[0][2])], dbr1, dirs, L, coef))
593 |     ck('正本の行の符号と違えば止まる', ok)
594 |     ok, _ = stops(lambda: recompute_rewrite(model, tok, T3, FJ, [(rows[0][0], rows[1][1], rows[0][2])], dbr1, dirs, L, coef))
595 |     ck('正本の行の升目と違えば止まる', ok)
596 | 
597 |     # (7) 呼び出しの間に hook を掛けようとしない（掛ける関数を、呼ばれたら落ちる形に差し替えて走らせる）
598 |     orig = (nn.Module.register_forward_hook, nn.Module.register_forward_pre_hook)
599 |     called = []
600 | 
601 |     def _trap(*a, **kw):
602 |         called.append(1)
603 |         raise RuntimeError('hook を掛けようとした')
604 |     nn.Module.register_forward_hook, nn.Module.register_forward_pre_hook = _trap, _trap
605 |     try:
606 |         r3 = recompute_rewrite(model, tok, T3, FJ, one, dbr1, dirs, L, coef)
607 |         trap_ok = not called
608 |     except RuntimeError:
609 |         trap_ok = False
610 |     finally:
611 |         nn.Module.register_forward_hook, nn.Module.register_forward_pre_hook = orig
612 |     ck('呼び出しの間に forward の hook を掛けようとしない（掛ける関数を差し替えて走らせた）', trap_ok and
613 |        r3[rows[0][0]]['effects'] == {k_: v_ for k_, v_ in r1[rows[0][0]]['effects'].items() if k_.startswith('static|')})
614 | 
615 |     n_ok = sum(res)
616 |     print('selftest: %d/%d ok' % (n_ok, len(res)))
617 |     print('柵: ' + FENCE)
618 |     return n_ok == len(res)
619 | 
620 | 
621 | # ---------------------------------------------------------------- フックの道との突き合わせ（乱数の小さな模型だけ）
622 | 
623 | def _readout64(model, h_last, read_ids):
624 |     """参考だけに使う: 同じ最終の正規化の入力を float64 で読む（float32 の読み取りの丸めの大きさの目安）。"""
625 |     import torch
626 |     with torch.no_grad():
627 |         x = h_last.to(torch.float64)
628 |         g = model.model.norm.weight.to(torch.float64)
629 |         eps = float(model.model.norm.variance_epsilon)
630 |         xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g
631 |         z = model.lm_head.weight[list(read_ids)].to(torch.float64) @ xn
632 |         return float(z[0] - torch.logsumexp(z[1:], dim=0))
633 | 
634 | 
635 | def _dry():
636 |     import torch
637 |     from transformers import AutoTokenizer
638 |     import direction_B
639 |     T3, FJ = load_canon(), load_facts()
640 |     F = _facts(FJ)
641 |     tok = AutoTokenizer.from_pretrained(SNAP)
642 |     model = tiny_model()
643 |     _assert_tiny(model)
644 |     n_layers = len(direction_B.decoder_layers(model))
645 |     L = direction_B.layer_index(float(T3['layers']['selected_ratio']), n_layers)
646 |     coef = float(T3['layers']['coef_applied'])
647 |     tol = float(T3['independent_recompute']['tol_stage1'])
648 |     d = int(model.config.hidden_size)
649 |     dirs, names = synthetic_dirs(FJ, d)
650 |     rows = _static_rows(T3, FJ)
651 |     reals = [nm for nm in names if nm.startswith('real:')]
652 |     dbr = {}
653 |     for nm, ck_, s in rows:
654 |         lst = [('static', s)] + [('iso:%d' % k, s) for k in range(20)]
655 |         for rn in reals:
656 |             lst += [(rn, s), (rn, -s)]
657 |         dbr[nm] = lst
658 |     import transformers
659 |     print('bl3_recompute_rewrite %s --dry  torch %s・transformers %s・numpy %s・注意の実装 %s'
660 |           % (VERSION, torch.__version__, transformers.__version__, np.__version__, model.config._attn_implementation))
661 |     print('乱数の小さな模型: 次元 %d・層 %d・選んだ層の添字 %d・係数 %s・一段目の許容 independent_recompute.tol_stage1 = %s'
662 |           % (d, n_layers, L, coef, tol))
663 |     for nm, ck_, s in rows:
664 |         n_st = sum(1 for dn, _ in dbr[nm] if dn == 'static')
665 |         n_iso = sum(1 for dn, _ in dbr[nm] if dn.startswith('iso:'))
666 |         n_real = sum(1 for dn, _ in dbr[nm] if dn.startswith('real:'))
667 |         print('行 %s・升目 %s（%s）・符号 %+d・方向と符号 %d 組（static %d・等方に見立てた %d・実在の差の名 %d 本 × 両方の向き＝%d）＋無操作'
668 |               % (nm, ck_, F['B']['cells'][ck_]['family'], s, len(dbr[nm]), n_st, n_iso, len(reals), n_real))
669 | 
670 |     t0 = time.time()
671 |     mine = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dirs, L, coef)
672 |     t_mine = time.time() - t0
673 |     print('残差の書き換えの道: %.1f 秒（順伝播 %d 回）' % (t_mine, sum(1 + len(dbr[nm]) for nm, _, _ in rows)))
674 | 
675 |     hk, err = None, None
676 |     t0 = time.time()
677 |     try:
678 |         import bl3_run as BR                                        # 中は開かない・公開の関数だけを呼ぶ
679 |         R = BR.Runner(model, T3, L, coef, dirs)
680 |         cells = BR.build_cells(tok, T3, FJ, sorted({ck_ for _, ck_, _ in rows}))
681 |         hk = BR.recompute_hook_path(R, [(nm, cells[ck_], s) for nm, ck_, s in rows], dbr)
682 |     except BaseException as e:                                     # 中を見ないため、落ちたときは種類と文言だけを印字する
683 |         err = '%s: %s' % (type(e).__name__, str(e)[:500])
684 |     t_hook = time.time() - t0
685 |     if err:
686 |         print('フックの道が落ちた（%.1f 秒）: %s' % (t_hook, err))
687 |         print('dry: 突き合わせられなかった')
688 |         print('柵: ' + FENCE)
689 |         return False
690 |     print('フックの道: %.1f 秒' % t_hook)
691 | 
692 |     D = _max_abs_diff(mine, hk)
693 |     if D is None:
694 |         print('dry: 鍵の集合が違う（行または方向|符号）——不一致')
695 |         print('柵: ' + FENCE)
696 |         return False
697 |     emax = max(abs(float(v)) for nm in mine for v in mine[nm]['effects'].values())
698 |     print('効き目の数 %d・効き目の絶対値の最大（残差の書き換えの道）%.4g' % (D['n_effects'], emax))
699 |     print('差の絶対値の最大: 効き目 %.3g・無操作の量 %.3g' % (D['effects'], D['noop']))
700 |     ok = D['effects'] <= tol
701 |     print('dry: 一段目の許容（%s）の%s（効き目の差の最大 %.3g）' % (tol, '内' if ok else '外', D['effects']))
702 |     print('（正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない）')
703 | 
704 |     # 参考（判定に入れない）: 読み取りの float32 の丸めの目安——同じ最終の正規化の入力を float64 で読み直した量との差の最大
705 |     r64 = 0.0
706 |     for nm, ck_, s in rows:
707 |         c = cell_input(tok, T3, FJ, ck_)
708 |         for v in (np.zeros(d, dtype=np.float64), dirs['static']):
709 |             h = forward_rewrite(model, c['ids'], L, v, coef, s, c['mp'])
710 |             lo32, _ = readout(model, h[0, -1], c['read_ids'])
711 |             r64 = max(r64, abs(lo32 - _readout64(model, h[0, -1], c['read_ids'])))
712 |     print('参考: 読み取りの float32 の丸めの目安（同じ最終の正規化の入力を float64 で読み直した量との差の最大・無操作と static・%d 行）%.3g'
713 |           % (len(rows), r64))
714 | 
715 |     # 参考（判定に入れない）: フックの道の後に残差の書き換えの道を短く走らせ直し、掛け残しや模型の変化が無いこと
716 |     sub_dbr = {nm: [('static', s)] for nm, _, s in rows}
717 |     again = recompute_rewrite(model, tok, T3, FJ, rows, sub_dbr, dirs, L, coef)
718 |     same = all(again[nm]['noop_lo'] == mine[nm]['noop_lo'] and
719 |                again[nm]['effects']['static|%+d' % s] == mine[nm]['effects']['static|%+d' % s] for nm, _, s in rows)
720 |     print('参考: フックの道の後に走らせ直した残差の書き換えの道（無操作と static・%d 行）が一度目と同じ（ビット単位）: %s'
721 |           % (len(rows), '同じ' if same else '違う'))
722 |     # 参考（判定に入れない）: mask の組み方を use_cache=False の形（明示の mask）にした残差の書き換えの道
723 |     t0 = time.time()
724 |     mine_nc = recompute_rewrite(model, tok, T3, FJ, rows, dbr, dirs, L, coef, use_cache=False)
725 |     D2 = _max_abs_diff(mine_nc, mine)
726 |     D3 = _max_abs_diff(mine_nc, hk)
727 |     print('参考: use_cache=False の形の残差の書き換えの道（%.1f 秒）——既定の形との差の最大 効き目 %.3g・無操作 %.3g／フックの道との差の最大 効き目 %.3g・無操作 %.3g'
728 |           % (time.time() - t0, D2['effects'], D2['noop'], D3['effects'], D3['noop']))
729 | 
730 |     # 参考（判定に入れない・事前登録つき）: 歯の変種——この道をわざと誤らせ、フックの道との差が許容を超えるか（突き合わせの弁別力）
731 |     t0 = time.time()
732 |     M = _mutant_diffs(model, tok, T3, FJ, rows, dirs, reals[0], L, coef, hk)
733 |     for kind, label, dmax, nk in M:
734 |         if kind == 'M0':
735 |             verdict = '許容の内（対照として期待どおり）' if dmax <= tol else '許容の外（対照が外れた——突き合わせの機械を疑う）'
736 |         else:
737 |             verdict = '許容の外＝捕まえた' if dmax > tol else '許容の内＝捕まえなかった（この模型での盲点）'
738 |         print('[歯] %s %s: フックの道との効き目の差の最大 %.3g（%d 個の効き目）→ %s（許容 %s）' % (kind, label, dmax, nk, verdict, tol))
739 |     print('[歯] 変種の計算 %.1f 秒（参考・判定に入れない）' % (time.time() - t0))
740 |     print('柵: ' + FENCE)
741 |     return ok
742 | 
743 | 
744 | def _readout_double(model, h_last, read_ids):
745 |     """歯の変種 M5 だけに使う: 最終の正規化を二度当てた読み取り（hidden_states[-1] を正規化の入力と取り違えたのと同じ形）。"""
746 |     import torch
747 |     with torch.no_grad():
748 |         g = model.model.norm.weight.to(torch.float32)
749 |         eps = float(model.model.norm.variance_epsilon)
750 |         x = h_last.to(device=g.device, dtype=torch.float32)
751 |         xn = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + eps) * g
752 |         xnn = xn * torch.rsqrt(xn.pow(2).mean(-1, keepdim=True) + eps) * g
753 |         z = model.lm_head.weight[list(read_ids)].to(torch.float32) @ xnn.to(model.lm_head.weight.device)
754 |         return float(z[0] - torch.logsumexp(z[1:], dim=0))
755 | 
756 | 
757 | def _readout_bf16(model, h_last, read_ids):
758 |     """歯の変種 M6 だけに使う: 模型そのものと同じく、正規化の出力を bf16 に戻して重みを掛け、語彙の行列の積も bf16 で取る読み取り。"""
759 |     import torch
760 |     with torch.no_grad():
761 |         g = model.model.norm.weight
762 |         eps = float(model.model.norm.variance_epsilon)
763 |         xf = h_last.to(device=g.device, dtype=torch.float32)
764 |         xn = g * (xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + eps)).to(g.dtype)
765 |         z = (model.lm_head.weight[list(read_ids)] @ xn.to(model.lm_head.weight.device)).to(torch.float32)
766 |         return float(z[0] - torch.logsumexp(z[1:], dim=0))
767 | 
768 | 
769 | def _mutant_diffs(model, tok, T3, FJ, rows, dirs, first_real, L, coef, hk):
770 |     """歯の変種（参考）: M0＝誤らせない対照・M1 帯の起点を主位置の一つ後・M2 書き換える層を一つ後・M3 符号の反転・
771 |     M4 係数を二度掛ける・M5 読み取りで正規化を二度・M6 読み取りを bf16。行ごとに無操作と五つの鍵（static・iso:0・iso:1 は行の符号、
772 |     real の最初の対は両方の向き）の効き目を作り、フックの道の同じ鍵の効き目との差の絶対値の最大を返す。"""
773 |     d = int(model.config.hidden_size)
774 |     zero = np.zeros(d, dtype=np.float64)
775 |     fwd = {'M0': {}, 'M1': {'mp_shift': 1}, 'M2': {'layer_shift': 1}, 'M3': {'flip': True}, 'M4': {'coef_twice': True}}
776 |     labels = {'M0': '誤らせない（対照）', 'M1': '帯の起点を主位置の一つ後にする', 'M2': '書き換える層を一つ後にする',
777 |               'M3': '符号を反転する', 'M4': '係数を二度掛ける（sign×coef×coef×v）',
778 |               'M5': '読み取りで正規化を二度当てる', 'M6': '読み取りを bf16 で当てる'}
779 |     std = lambda m, hl, ids: readout(m, hl, ids)[0]
780 |     eff = {k: {} for k in labels}
781 |     for nm, ck_, s in rows:
782 |         c = cell_input(tok, T3, FJ, ck_)
783 |         keys = [('static', s), ('iso:0', s), ('iso:1', s), (first_real, +1), (first_real, -1)]
784 |         for kind, opt in fwd.items():
785 |             Lm = L + opt.get('layer_shift', 0)
786 |             mpm = c['mp'] + opt.get('mp_shift', 0)
787 |             cm = coef * coef if opt.get('coef_twice') else coef
788 |             readers = {'M0': std, 'M5': _readout_double, 'M6': _readout_bf16} if kind == 'M0' else {kind: std}
789 |             h0 = forward_rewrite(model, c['ids'], Lm, zero, cm, s, mpm)
790 |             lo0 = {rk: rf(model, h0[0, -1], c['read_ids']) for rk, rf in readers.items()}
791 |             for dn, sg in keys:
792 |                 h = forward_rewrite(model, c['ids'], Lm, dirs[dn], cm, (-sg if opt.get('flip') else sg), mpm)
793 |                 for rk, rf in readers.items():
794 |                     eff[rk].setdefault(nm, {})['%s|%+d' % (dn, sg)] = rf(model, h[0, -1], c['read_ids']) - lo0[rk]
795 |     out = []
796 |     for kind in labels:
797 |         dmax, nk = 0.0, 0
798 |         for nm in eff[kind]:
799 |             for key, v in eff[kind][nm].items():
800 |                 dmax = max(dmax, abs(float(v) - float(hk[nm]['effects'][key])))
801 |                 nk += 1
802 |         out.append((kind, labels[kind], dmax, nk))
803 |     return out
804 | 
805 | 
806 | def main():
807 |     try:
808 |         sys.stdout.reconfigure(encoding='utf-8')
809 |     except Exception:
810 |         pass
811 |     ap = argparse.ArgumentParser(description='B-lens 層三（Bl3）の独立の再計算——残差の書き換えの道')
812 |     ap.add_argument('--selftest', action='store_true', help='乱数の小さな模型で自己検査')
813 |     ap.add_argument('--dry', action='store_true', help='乱数の小さな模型で、フックの道と一段目の許容で突き合わせる')
814 |     a = ap.parse_args()
815 |     if not (a.selftest or a.dry):
816 |         ap.print_help()
817 |         return 0
818 |     ok = True
819 |     if a.selftest:
820 |         ok = _selftest() and ok
821 |     if a.dry:
822 |         ok = _dry() and ok
823 |     return 0 if ok else 1
824 | 
825 | 
826 | if __name__ == '__main__':
827 |     sys.exit(main())
```
<<< 終: `tools/bl3_recompute_rewrite.py` >>>

<<< 始: `records/Bl3/tools/recompute-rewrite-dev-Bl3.md`（SHA16 F03F51731422643C） >>>
# B-lens 層三（Bl3）独立の再計算——残差の書き換えの道の開発の記録

<!-- generated: recompute-rewrite-dev-Bl3 -->

- 器: `tools/bl3_recompute_rewrite.py`（v1・SHA16 012CB2B68397614A・SHA-256 012CB2B68397614AF623159E48E8D456521D42356223866E9BC6C74E6059F26A）。§4・§5 の出力はこの版の器が出した（走らせる前に器の SHA-256 を一時置き場に書き、この記録を組み立てる時に今の器と一致することを機械で確かめた）。
- 書き手: 系統内の新しい個体（Claude Opus 5.5・Claude Code の下請けの個体）。本の器の書き手（コーディネータ・南無弥勒如来）とは別の個体で、登録者（楠見優太さん）の許可による（正本 `independent_recompute.who`）。
- 組み立て: 2026-09-24 22:40（UTC）・ワークツリーの頭のコミット 3bb772e7f1d049a7e1f115d6028a2de7a6d6f6cb
- 状態: **未コミット**（コーディネータが確かめてからコミットする）。新しいファイルは器とこの記録だけで、既にあるファイルは一つも変えていない（§8 の git の出力）。
- 数・ハッシュ・引用の出所: §4・§5 は器の出力の逐語の写し。本文の数とハッシュは、一時置き場の組み立ての器（`.gitignore` に載っている `results/_smoke/` の下に置き、終わりに消した）が、器の出力・正本・設計事実・ファイルから機械で写した。手で打った数は無い（器の中の定数・乱数の種・方向の名の書き方を、器の書き方として符号のまま引いた所はある。§5.1 の予想の信頼度は、書き手が事前登録の文に書いた値の写し）。

## 0. 要約

- 自己検査（`--selftest`・乱数の小さな模型）: `selftest: 43/43 ok`（exit=0）
- 突き合わせ（`--dry`・乱数の小さな模型・コーディネータのフックの道の公開の関数を中を見ずに呼んだ）: `dry: 一段目の許容（0.001）の内（効き目の差の最大 2.54e-07）`（exit=0）
  - `差の絶対値の最大: 効き目 2.54e-07・無操作の量 6.72e-08`
  - 正本 `independent_recompute.agreement` の後半（二つの道の値からそれぞれ出した札が同じこと）は、この器では見ていない（札は集計の器の仕事）。
- 歯の変種（参考・判定に入れない・事前登録つき）: 対照は許容の内・わざと誤らせた 6 変種のうち 3 を捕まえ、捕まえなかったのは M1・M4・M6・予想の外れは M1・M4（§5.1）
- 正本で決まっていなかった所は §6、コーディネータに伝えたいことは §7、検分票は末尾（判定は保留）。

## 1. 読んだもの

- 正本 `design/contrasts-Bl3.json`（SHA16 6330B65A0AB503E7）: 鍵 `independent_recompute`・`readout.primary`・`layers`・`computation`（指示の範囲）。ほかに、行・升目・方向の名と規則を知るために `main_rows`・`cells_main`・`cell_signs_main`・`inputs`（版と凍結物の SHA16）・`directions`（ノルムの規則）・`nulls`（比べる相手の除き方と向き）を読んだ。どれも正本の決まりで、フックの道の実装ではない。
- 草案 `design/design-Bl3-draft3.md`（SHA16 30CED58A8559EA05）: §2（材料と凍結物）・§3（読み取り）・§12（器と確かめ・独立の再計算）。
- 設計事実 `records/Bl3/design-facts-Bl3.json`（SHA16 9BB701E7D2AE1C7F・頭の `contrasts_sha16` は 6330B65A0AB503E7＝今の正本と同じ）: `facts.A`（文・prefix・prefix_ids・letter_ids・揺れの版）・`facts.B`（文・cells）・`facts.D`（文・real_pairs ほか）。
- 段階 B の凍結の器（読むだけ・変えていない）:
  - `tools/steer_B.py`（SHA16 71157C6921E12AC7・正本 `inputs.files.steer_B` の記録 71157C6921E12AC7 と一致）: 頭の文から `assert_batch_uniform` まで（`random_directions`・`apply_vector`・`apply_chat`・`main_position`・`scenario_start_index`・`band_starts` ほか）。
  - `tools/run_stageB_local.py`（SHA16 E976A4F5B63767FA・正本 `inputs.files.runner_B` の記録 E976A4F5B63767FA と一致）: 頭の文から `make_hook` まで（`arm_texts`・`scenario_and_instruction`・`user_message`・`arm_plan`・`make_hook`）と、`load_directions`〜`run_cell`（段階 B の組み立ての呼び方・層の添字の確かめ・生成に attention_mask を渡すこと）。**`make_hook` は加減の算術の決まりを知るためだけに読み、呼んでいない。**
  - `tools/direction_B.py`（SHA16 E84A101655685F2B）: `layer_index`・`hidden_states_index`・`decoder_layers`。
  - `tools/runs_B.py`（SHA16 269B60867D0924EB）: `sha16_file`（SHA16 の決まり）だけ。
  - `tools/colab/boot_stageB.py`: 検索の出力の行（本物の模型の読み込みが bf16・`device_map` で、注意の実装を指定していないこと）だけ。
- 凍結の場面の記録 `arms/frozen-from-ryokai-os/app-scenarios.json`（SHA16 7AD7E49459D5C402・正本の記録 7AD7E49459D5C402 と一致）: 凍結の関数を通して引いただけ。
- 手元の transformers（4.57.3）: `models/qwen3/modeling_qwen3.py`（全体）・`masking_utils.py`（`prepare_padding_mask`・`_ignore_causal_mask_sdpa`・`sdpa_mask_recent_torch`・`_preprocess_mask_arguments`・`create_causal_mask`・`find_packed_sequence_indices`）・`integrations/sdpa_attention.py`（全体）・`utils/generic.py` の `check_model_inputs`・`modeling_layers.py` の `GradientCheckpointingLayer`・`cache_utils.py` の `DynamicLayer`。
- 設定の置き場（Qwen3-4B-Instruct-2507・改訂 `cdbee75f17c01a7cc42f958dc650907174af0554`）の `config.json` とトークナイザ。**実の重みは読んでいない。** ほかに `.gitignore`・`.gitattributes`。
- git: 作業の頭に `git log --oneline -5` を見た。最新のコミットの文に、コーディネータの走行器が段階 B の凍結の `make_hook` をそのまま呼ぶ旨があり、それを読んだ（情報の状態として検分票の COI 記録に置く）。

## 2. 読まなかったもの

- `tools/bl3_run.py`・`tools/dry_run_Bl3.py`・`tools/analyze_Bl3.py` は開いていない（指示）。`bl3_run` は `--dry` の中でだけ import し、指示にある公開の関数（`Runner`・`build_cells`・`recompute_hook_path`）を中を見ずに呼んだ。落ちたときは例外の種類と文言だけを印字し、traceback（中の行が出る）を出さない形にした。`build_cells` の戻り値の中も見ていない。器の同定のために、`tools/bl3_run.py` の SHA16（7ECB9CF764F4F8AE）だけを組み立ての器が計算した（中身は表示していない）。
- 自分から読まなかったもの: `tools/bl3_core.py`・`tools/bl3_directions.py`・`tools/bl3_facts.py`（層三のコーディネータの器——読み取りの量や方向の作り方の書き方が入りうるので、読み取りの独立を守るため）と、`records/Bl3/tools/` の枠と器の段の記録（`frame-tools-Bl3.md`・`tools-log-Bl3.md`・`trials/`——フックの道の書き方が書いてありうる）。
- 検索の扱い: `tools/` を相手にした検索を、`attn_implementation`／`sdpa`・`from_pretrained`・`reconfigure` の語で走らせた。指示で読まないとされた器は、検索の除外か `grep -v` で名前ごと落としてから表示し、中の行は一行も表示していない。ファイルの一覧（`ls -la tools`）で、それらの名と大きさは見た。

## 3. 書き方の決め

### 3.1 層の回し方

transformers 4.57.3（正本 `inputs.versions_B`）の `Qwen3Model.forward` の手順を、部品を差し替えずに写した（版が違えば止める）。

1. `inputs_embeds = model.model.embed_tokens(input_ids)`（input_ids は [1, 列の長さ]・バッチ一・近道なしで列の全体を流す）
2. `use_cache` が真なら空の `DynamicCache(config=…)` を作る（模型の forward の既定——`check_model_inputs` が `config.use_cache` を入れる——と同じ。一回の順伝播ごとに作って捨て、順伝播をまたいで使い回さない）
3. `cache_position = arange(0, 列の長さ)`・`position_ids = cache_position.unsqueeze(0)`
4. mask: `create_causal_mask(config, input_embeds, attention_mask=None, cache_position, past_key_values, position_ids)`（窓つきの層があれば `create_sliding_window_causal_mask` も。関数は `modeling_qwen3` の名の束ねから引き、模型の組み立てが呼ぶ物と同じ物を指す）
5. rotary: `model.model.rotary_emb(inputs_embeds, position_ids)` の (cos, sin) を全層で共有
6. 層を順に、模型の forward と同じ引数（`attention_mask`＝その層の `attention_type` の mask・`position_ids`・`past_key_values`・`use_cache`・`cache_position`・`position_embeddings`）で呼ぶ。層 L の出力を得た直後に書き換え（§3.3）、その値を層 L+1 に渡す
7. 最後の層の出力（＝最終の正規化の入力）を返す。`model.model.norm` と `lm_head` の順伝播は呼ばない（読み取りは §3.4 のとおり float32 で自分で当てる）

層の中身（注意・MLP・層の中の正規化）は模型の部品をそのまま呼び、書き直していない（書き直すと突き合わせの相手と演算が変わる）。フックは一本も掛けない（§3.5）。

### 3.2 mask と rotary

- 書き換えは層の出力の値だけを変え、mask・rotary・位置の番号には触れない。
- 既定（`use_cache`＝`config.use_cache`・この環境では True）では、`create_causal_mask` は None を返し、SDPA は `is_causal` で走る（KV の頭は SDPA の中で揃える）。`use_cache=False` で attention_mask も渡さない呼び方では、cache が無いときの packed の検出（`find_packed_sequence_indices` は一つの列でも零の並びを返す）で is_causal の飛ばしが外れ、明示の四次元の真偽の mask が作られて `attn_mask` に渡る（KV の頭は `repeat_kv` で広げる）。数の上の意味は同じだが、GPU では SDPA の核の選び方が変わりうる（§7 の一）。
- 手回しの道が二つの呼び方で組んだ mask の形は、自己検査の参考の行のとおり（器の出力の写し）:
  - `[参考] N1|Onull 既定（config.use_cache）: 手回しの道が組んだ mask（full_attention）は None（SDPA は is_causal で走る）（判定に入れない）`
  - `[参考] N1|Onull use_cache=False: 手回しの道が組んだ mask（full_attention）は 明示の mask（型 torch.bool・形 (1, 1, 475, 475)）（判定に入れない）`
  - `[参考] S1|O-Ncold 既定（config.use_cache）: 手回しの道が組んだ mask（full_attention）は None（SDPA は is_causal で走る）（判定に入れない）`
  - `[参考] S1|O-Ncold use_cache=False: 手回しの道が組んだ mask（full_attention）は 明示の mask（型 torch.bool・形 (1, 1, 548, 548)）（判定に入れない）`
- 自己検査で、二つの呼び方のどちらでも、手回しの道が同じ呼び方の模型の forward とビット単位で一致することを確かめた（§4）。この CPU（注意の実装 sdpa）では、二つの呼び方の手回しの道の値は同じだった（§5 の参考の行）。

### 3.3 書き換えの位置と型

- 層 L（`direction_B.layer_index(layers.selected_ratio, 模型の層の数)`・層の割合 0.5・本物の模型では正本 `layers.indices` の 17・乱数の小さな模型では §4 の頭の行）の出力 h（bf16・[1, n, d]）に対して、
  `add = int(sign) * float(coef) * torch.as_tensor(np.asarray(v, dtype=np.float32), dtype=h.dtype, device=h.device)`、`h[0, mp:, :] = h[0, mp:, :] + add`。
  段階 B の走行器のフック（`make_hook`）の算術と同じ形——NumPy の float32 を経て層の出力の型に直し、Python の数 sign×coef を掛け（bf16）、主位置から後ろに bf16 のまま足す。係数（正本 `layers.coef_applied`＝2.0）は一度だけ。
- 帯は主位置 mp（組み立てたプロンプトの最後のトークン・`steer_B.main_position`）から列の最後（読み取りの位置＝主の書き出しの最後のトークン）まで。
- 無操作は零のベクトルを同じ算術で足す（零を足しても値は変わらない・正本 `readout.primary.batching` の「無操作は零のベクトル」）。零のベクトルに付ける符号は行の符号にした（値は同じ）。

### 3.4 読み取り

- 最後の層の出力の最後の位置を float32 に上げ、`x × rsqrt(mean(x²) + eps) × g`（g は `model.model.norm.weight` の float32・eps は `model.model.norm.variance_epsilon`——設定の `rms_norm_eps` と一致を確かめる）を float32 で当て、`lm_head.weight` の読み取りの集合の行を float32 で掛ける。
- 読み取りの集合: 族の選択の文字の順（正本 `readout.primary.letters`: survival は a・b・c・nuclear は a・b・c・d・先頭は破局の側の文字 a）と、最後に refuse の頭（ref）。トークンの番号は `facts.A.letter_ids`。族は凍結の場面の記録から引き、転記行 B の族と照らす。番号がトークナイザで文字に戻ることも確かめる。
- 量＝z_a − logsumexp（ほかの選択の文字と refuse の頭）を float32 で計算して Python の数にする。効き目＝加えた値 − 無操作の値（Python の数の引き算）。
- `hidden_states[-1]` は使わない（4.57.3 の `check_model_inputs` は `hidden_states` の最後を正規化の後の `last_hidden_state` で置き換える）。取り違えると模型の出口の値からの差が大きくなることを、自己検査の歯の確かめで見た（§4）。

### 3.5 止める確かめ（器の中）

- 版と機種: transformers が正本 `inputs.versions_B` の版でない／本体が Qwen3Model でない／eval でない／bf16 でない／最終の正規化の eps が設定と違う／層の並びの数が設定と違う
- hook: 呼ぶ前と後に、模型のどの部品にも forward の hook（前・後）が無く、大域の hook も無いこと（フックの道の掛け残しも混ぜない）
- 層と係数: 層の添字が正本の規則（本物の模型の層の数なら `layers.indices` とも）と違う／係数が `layers.coef_applied` と違う
- 行: 三つ組でない／行の名が重なる／正本 `main_rows` の行の名なら、升目と符号が正本と違う／dirs_by_row に行が無い／同じ方向と符号が二度ある
- 方向: float64 の配列でない／形が次元と合わない／有限でない／dirs に static があれば、使う零でない方向のノルムが ‖static‖ から相対 1e-06 を超えて外れる（段階 B の `load_directions` と同じ許容）
- 升目: 転記行 B とプロンプトの長さ・主位置・読み取りの位置・族・前置きの SHA16 のどれかが違う／主の書き出しの並びが転記の文字列に戻らない／読み取りの集合のトークンが文字と refuse の頭に戻らない
- 書き換えが一度でない／出口の列の長さが入力と違う

### 3.6 乱数の小さな模型と合成の方向（`--selftest`・`--dry` だけ）

- 指示の作り方を自分で書いた: 設定だけを置き場から借りて次元などを小さくし（値は §4 の頭の行）、`layer_types` を層の数で切り、`torch.manual_seed(0)` の後に `from_config`、名が `norm.weight` で終わる重みを `named_parameters()` の順に `torch.rand(形, generator=torch.Generator().manual_seed(1)) + 0.5` で置き換え、bf16・eval にした。**コーディネータの合成の器とこの乱数の引き方が同じかは確かめていない**（`--dry` では同じ模型の物を両方の道に渡すので、突き合わせには効かない）。
- 合成の方向: `np.random.default_rng(5)` で次元の正規乱数を、static・iso:0〜iso:19・real:＋`facts.D.real_pairs` の名の順に引き、static 以外を ‖static‖ にそろえた。
- 確かめは乱数の小さな模型だけで走る（次元と層の数が小さな模型の値でなければ止める——封印の前に本物の模型で読み取りの値を出さない・正本 `computation.before_seal`）。

## 4. 自己検査（`--selftest`）の結果——器の出力の逐語

- 走らせた器の SHA-256（走らせる前に記録）: 012CB2B68397614AF623159E48E8D456521D42356223866E9BC6C74E6059F26A（今の器と一致）
- 標準出力の SHA-256（改行を LF にそろえたもの＝下の逐語の写しに末尾の改行を一つ足したバイト列・組み立ての器が一致を確かめた）: 167581D89D48B7D3FE96B024535B4AD6C97B7BA8C6B252E2253FBE5E989FBFD4・exit=0
- 標準エラーは空。

```
bl3_recompute_rewrite v1 --selftest  torch 2.9.1+cpu・transformers 4.57.3・numpy 2.4.2・注意の実装 sdpa・config.use_cache True
乱数の小さな模型: 次元 64・層 4・注意の頭 4・KV の頭 2・頭の次元 16・中間 128・選んだ層の添字 1・係数 2.0
[ok] 升目の組み立てが転記行 B と一致（全 9 升目・長さ・主位置・読み取りの位置・族・前置きの SHA16・読み取りの集合のトークン）  | N1|O-Ncold 474/473/480・N1|Onull 468/467/474・S1|O-Ncold 541/540/547・S1|Onull 535/534/541・S4|O-Ncold 555/554/561・S4|Onull 549/548/555・S4|Osec-Ncold 557/556/563・SK|O-Ncold 556/555/562・SK|Onull 550/549/556
[ok] 転記行 B と違えば止まる（S1|O-Ncold の prompt_len を +1 ずらした写し）
[ok] 転記行 B と違えば止まる（S1|O-Ncold の main_position を +1 ずらした写し）
[ok] 転記行 B と違えば止まる（S1|O-Ncold の readout_position を -1 ずらした写し）
[ok] 主の書き出しの割り方が変われば止まる（最後のトークンを落とした写し）
[ok] N1|Onull 既定（config.use_cache）: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 475, 64)・型 torch.bfloat16
[参考] N1|Onull 既定（config.use_cache）: 手回しの道が組んだ mask（full_attention）は None（SDPA は is_causal で走る）（判定に入れない）
[ok] N1|Onull 既定（config.use_cache）: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00068（許容 0.5）
[ok] N1|Onull: 歯の確かめ——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 4 倍を超える  | 取り違え 0.0351・正しい 0.00068
[ok] N1|Onull: hidden_states[-1] は正規化の後（last_hidden_state と同じ・最終の正規化の入力と違う）
[ok] N1|Onull: 手回しの層 1 の出力（書き換えの前）が hidden_states[2]（layers.hidden_states_indices の対応）と一致（ビット単位）
[ok] N1|Onull use_cache=False: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 475, 64)・型 torch.bfloat16
[参考] N1|Onull use_cache=False: 手回しの道が組んだ mask（full_attention）は 明示の mask（型 torch.bool・形 (1, 1, 475, 475)）（判定に入れない）
[ok] N1|Onull use_cache=False: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00068（許容 0.5）
[ok] S1|O-Ncold 既定（config.use_cache）: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 548, 64)・型 torch.bfloat16
[参考] S1|O-Ncold 既定（config.use_cache）: 手回しの道が組んだ mask（full_attention）は None（SDPA は is_causal で走る）（判定に入れない）
[ok] S1|O-Ncold 既定（config.use_cache）: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00117（許容 0.5）
[ok] S1|O-Ncold: 歯の確かめ——hidden_states[-1] を正規化の入力と取り違えた読み取りの差が、正しい読み取りの差の 4 倍を超える  | 取り違え 0.023・正しい 0.00117
[ok] S1|O-Ncold: hidden_states[-1] は正規化の後（last_hidden_state と同じ・最終の正規化の入力と違う）
[ok] S1|O-Ncold: 手回しの層 1 の出力（書き換えの前）が hidden_states[2]（layers.hidden_states_indices の対応）と一致（ビット単位）
[ok] S1|O-Ncold use_cache=False: 手回しの道（零の書き換え）の最終の正規化の入力が模型の forward と一致（ビット単位）  | 差の絶対値の最大 0・形 (1, 548, 64)・型 torch.bfloat16
[参考] S1|O-Ncold use_cache=False: 手回しの道が組んだ mask（full_attention）は 明示の mask（型 torch.bool・形 (1, 1, 548, 548)）（判定に入れない）
[ok] S1|O-Ncold use_cache=False: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00117（許容 0.5）
[ok] S1|O-Ncold 符号 -1: 層 1 より前の層の出力は無操作と同じ（ビット単位）
[ok] S1|O-Ncold 符号 -1: 層 1 の出力（書き換えの前）は無操作と同じ（ビット単位）
[ok] S1|O-Ncold 符号 -1: 書き換えは主位置（540）より前の位置を変えない（層 1 の出力・ビット単位）
[ok] S1|O-Ncold 符号 -1: 主位置から列の最後まで（8 位置）に同じ量を足した（層 1 の出力・ビット単位）
[ok] S1|O-Ncold 符号 -1: 足した量の向きと大きさが sign×coef×v（bf16 の丸めの内）  | 余弦の最小 0.999997・ノルムの相対の差の最大 0.000838
[ok] S1|O-Ncold 符号 -1: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う
[ok] N1|Onull 符号 +1: 層 1 より前の層の出力は無操作と同じ（ビット単位）
[ok] N1|Onull 符号 +1: 層 1 の出力（書き換えの前）は無操作と同じ（ビット単位）
[ok] N1|Onull 符号 +1: 書き換えは主位置（467）より前の位置を変えない（層 1 の出力・ビット単位）
[ok] N1|Onull 符号 +1: 主位置から列の最後まで（8 位置）に同じ量を足した（層 1 の出力・ビット単位）
[ok] N1|Onull 符号 +1: 足した量の向きと大きさが sign×coef×v（bf16 の丸めの内）  | 余弦の最小 0.999996・ノルムの相対の差の最大 0.000547
[ok] N1|Onull 符号 +1: 最終の正規化の入力は主位置より前で無操作と同じ（ビット単位）・主位置から後ろの全ての位置で違う
[参考] float32 を経た bf16 と float64 から直に直した bf16 が同じ合成の方向: 49/49（判定に入れない）
[ok] 零のベクトルの効き目が零（両方の符号・2 行: sub:N1:O-Ncold-v~O-Ncold-vrand・add:S1:Onull+v~Onull+vrand）  | sub:N1:O-Ncold-v~O-Ncold-vrand 0.0/0.0・add:S1:Onull+v~Onull+vrand 0.0/0.0
[ok] 歯の確かめ: static の効き目は零でない（乱数の小さな模型）  | sub:N1:O-Ncold-v~O-Ncold-vrand -0.0573・add:S1:Onull+v~Onull+vrand -0.0701
[ok] 同じ呼び出しを二度走らせて同じ値（ビット単位）
[ok] 出力の形 {行の名: {noop_lo, effects: {方向の名|符号: 効き目}}}（符号の書き方 %+d）  | 鍵の例 ['static|-1', 'zero|+1', 'zero|-1']
[ok] 模型に forward の hook が掛かっていれば止まる
[ok] 層の添字が正本の規則と違えば止まる
[ok] 係数が正本 layers.coef_applied と違えば止まる
[ok] 方向が float64 でなければ止まる
[ok] 方向のノルムが ‖static‖ に揃っていなければ止まる
[ok] 正本の行の符号と違えば止まる
[ok] 正本の行の升目と違えば止まる
[ok] 呼び出しの間に forward の hook を掛けようとしない（掛ける関数を差し替えて走らせた）
selftest: 43/43 ok
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
```

- 出口の値の確かめ（正本 `computation.logit_tol`＝0.5）の行は次のとおりで、bf16 の出口の値と float32 の読み取りの差（bf16 の丸めの大きさの目安）がここに出ている:
  - `[ok] N1|Onull 既定（config.use_cache）: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00068（許容 0.5）`
  - `[ok] N1|Onull use_cache=False: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00068（許容 0.5）`
  - `[ok] S1|O-Ncold 既定（config.use_cache）: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00117（許容 0.5）`
  - `[ok] S1|O-Ncold use_cache=False: 読み取りの集合の出口の値（float32）と模型の出口の値（bf16）の差が computation.logit_tol 以内  | 差の絶対値の最大 0.00117（許容 0.5）`

## 5. 突き合わせ（`--dry`）の結果——器の出力の逐語

- 走らせた器の SHA-256: 012CB2B68397614AF623159E48E8D456521D42356223866E9BC6C74E6059F26A（今の器と一致）・突き合わせの相手 `tools/bl3_run.py` の SHA16 7ECB9CF764F4F8AE（組み立ての時に計算・中は表示していない）
- 標準出力の SHA-256（改行を LF にそろえたもの＝下の逐語の写しに末尾の改行を一つ足したバイト列・組み立ての器が一致を確かめた）: C563C4B69B9AFE338D04390E2DA15D934BFD9B5FDD04DAE156131E934B53FA04・exit=0
- 標準エラーは空。

```
bl3_recompute_rewrite v1 --dry  torch 2.9.1+cpu・transformers 4.57.3・numpy 2.4.2・注意の実装 sdpa
乱数の小さな模型: 次元 64・層 4・選んだ層の添字 1・係数 2.0・一段目の許容 independent_recompute.tol_stage1 = 0.001
行 sub:N1:O-Ncold-v~O-Ncold-vrand・升目 N1|O-Ncold（nuclear）・符号 -1・方向と符号 77 組（static 1・等方に見立てた 20・実在の差の名 28 本 × 両方の向き＝56）＋無操作
行 add:S1:Onull+v~Onull+vrand・升目 S1|Onull（survival）・符号 +1・方向と符号 77 組（static 1・等方に見立てた 20・実在の差の名 28 本 × 両方の向き＝56）＋無操作
残差の書き換えの道: 79.4 秒（順伝播 156 回）
フックの道: 80.8 秒
効き目の数 154・効き目の絶対値の最大（残差の書き換えの道）0.4261
差の絶対値の最大: 効き目 2.54e-07・無操作の量 6.72e-08
dry: 一段目の許容（0.001）の内（効き目の差の最大 2.54e-07）
（正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない）
参考: 読み取りの float32 の丸めの目安（同じ最終の正規化の入力を float64 で読み直した量との差の最大・無操作と static・2 行）6.8e-08
参考: フックの道の後に走らせ直した残差の書き換えの道（無操作と static・2 行）が一度目と同じ（ビット単位）: 同じ
参考: use_cache=False の形の残差の書き換えの道（69.2 秒）——既定の形との差の最大 効き目 0・無操作 0／フックの道との差の最大 効き目 2.54e-07・無操作 6.72e-08
[歯] M0 誤らせない（対照）: フックの道との効き目の差の最大 1.29e-07（10 個の効き目）→ 許容の内（対照として期待どおり）（許容 0.001）
[歯] M1 帯の起点を主位置の一つ後にする: フックの道との効き目の差の最大 0.000344（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）
[歯] M2 書き換える層を一つ後にする: フックの道との効き目の差の最大 0.00154（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）
[歯] M3 符号を反転する: フックの道との効き目の差の最大 0.565（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）
[歯] M4 係数を二度掛ける（sign×coef×coef×v）: フックの道との効き目の差の最大 0.000902（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）
[歯] M5 読み取りで正規化を二度当てる: フックの道との効き目の差の最大 0.0459（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）
[歯] M6 読み取りを bf16 で当てる: フックの道との効き目の差の最大 0.000578（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）
[歯] 変種の計算 25.2 秒（参考・判定に入れない）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
```

- 比べた組（器の出力の行）:
  - `行 sub:N1:O-Ncold-v~O-Ncold-vrand・升目 N1|O-Ncold（nuclear）・符号 -1・方向と符号 77 組（static 1・等方に見立てた 20・実在の差の名 28 本 × 両方の向き＝56）＋無操作`
  - `行 add:S1:Onull+v~Onull+vrand・升目 S1|Onull（survival）・符号 +1・方向と符号 77 組（static 1・等方に見立てた 20・実在の差の名 28 本 × 両方の向き＝56）＋無操作`
- 判定は、正本 `independent_recompute.tol_stage1`（0.001）を、全ての効き目の差の絶対値の最大に当てた（器が印字した `dry:` の行）。無操作の量の差と参考の行は判定に入れていない。
- 読み（書き手の推測・確かめていない）: 効き目の差の最大（2.54e-07）は、読み取りの float32 の丸めの目安（参考の行の 6.8e-08）の 3.7 倍（一桁の内）で、§4 の出口の値の行の bf16 の丸めの目安の最小（0.00068）の 2,700 分の一（どちらの比も、組み立ての器が印字の値から計算し、有効数字二桁に丸めた）。二つの道の最終の正規化の入力は同じで、差は読み取りの float32 の算術の順から来ている、と読める。**フックの道の中を見ていないので、この読みは確かめていない。**
- **比の分母の注（検分の教訓4）**: 三つの値は同じ種類・同じ数の量どうしではない。効き目の差の最大は、効き目（それぞれ二つの量の差）154 個の上の最大。float32 の目安は、無操作と static の量（効き目でなく量そのもの）四つの上の最大。bf16 の目安は、読み取りの集合の出口の値（量でなく logit）の差の最大。上の比は桁の目安としてだけ読み、「何倍」を較正された比として引かない。

### 5.1 歯の変種（参考・判定に入れない・事前登録つき）

一段目の突き合わせが、この小さな模型で、ありうる実装の誤りを捕まえる弁別力を持つかを測るために、この道をわざと誤らせた変種を、フックの道の値と比べた（検分の教訓15）。**変種は書き手の道の側を誤らせたもので、フックの道の側の誤りを直接に試したものではない。** 判定（`dry:` の行）は変種の結果で変えない。

- 事前登録（変種の器を書く前・走らせる前に書いた文の逐語・SHA-256 088AD8FE1D2F3BC562FFD02D1846607CBF9BB694B5269AD39D8767EA872AA221）:

```
事前登録——歯の変種の突き合わせ（--dry に参考として足す・変種の器を書く前、走らせる前に書いた）
書いた時刻（UTC）: 2026-09-24 22:25:57
目的: 一段目の許容（independent_recompute.tol_stage1）での突き合わせが、乱数の小さな模型で、ありうる実装の誤りを捕まえる弁別力を持つかを測る（検分の教訓15——検査を置くことと、検査が働くことは同じでない）。--dry の判定の行は変えない。変種の結果は参考で、判定に入れない。
比べ方: 変種ごとに、残差の書き換えの道をわざと誤らせ（下の M1〜M6）、比べた二つの行のそれぞれで、無操作と、static・iso:0・iso:1（行の符号）と real の最初の対（両方の向き）の効き目を作り、フックの道の同じ鍵の効き目との差の絶対値の最大を取る。最大が許容を超えれば「捕まえた」。対照 M0（誤らせない）は許容の内のはず。
変種と予想（方向・信頼度）:
M0 誤らせない（対照）: 許容の内（高 0.95）
M1 帯の起点を主位置の一つ後にする: 捕まえる（中 0.6）——帯の位置の一つを落とすだけで、読み取りの位置への加減は残る
M2 書き換える層を一つ後にする: 捕まえる（高 0.9）
M3 符号を反転する: 捕まえる（高 0.95）
M4 係数を二度掛ける（sign×coef×coef×v）: 捕まえる（中 0.75）——足した量が隠れ状態より大きい領域では、正規化が大きさを打ち消して差が縮みうる
M5 読み取りで正規化を二度当てる（hidden_states[-1] の取り違えと同じ形）: 捕まえる（高 0.9）
M6 読み取りを bf16 で当てる（正規化の出力と語彙の行列の積を bf16）: 五分五分（中 0.5）——丸めの差は許容の前後の見込み
捕まえなかった変種があれば、それは一段目の突き合わせの（この小さな模型での）盲点として記録し、器の誤りとはしない。予想が外れても消さない。
```

- 時刻の順（組み立ての器がファイルの記録から写した・UTC）: 事前登録の文に書いた時刻 2026-09-24 22:25:57 → 器の最後の変更 2026-09-24 22:26:46 → `--dry` の出力の最後の書き込み 2026-09-24 22:32:51。事前登録が器の最後の変更と `--dry` より前であることは、ファイルの時刻と矛盾しない。変種の器を書く前であることは、ファイルの時刻だけでは示せず、書き手の申告である。
- 結果（器の出力の行）:
  - `[歯] M0 誤らせない（対照）: フックの道との効き目の差の最大 1.29e-07（10 個の効き目）→ 許容の内（対照として期待どおり）（許容 0.001）`
  - `[歯] M1 帯の起点を主位置の一つ後にする: フックの道との効き目の差の最大 0.000344（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）`
  - `[歯] M2 書き換える層を一つ後にする: フックの道との効き目の差の最大 0.00154（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）`
  - `[歯] M3 符号を反転する: フックの道との効き目の差の最大 0.565（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）`
  - `[歯] M4 係数を二度掛ける（sign×coef×coef×v）: フックの道との効き目の差の最大 0.000902（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）`
  - `[歯] M5 読み取りで正規化を二度当てる: フックの道との効き目の差の最大 0.0459（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）`
  - `[歯] M6 読み取りを bf16 で当てる: フックの道との効き目の差の最大 0.000578（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）`
  - `[歯] 変種の計算 25.2 秒（参考・判定に入れない）`
- 予想と結果の突き合わせ（組み立ての器が事前登録の文と器の出力の行から機械で作った）:

| 変種 | 予想（事前登録） | 結果 | 予想どおりか |
|---|---|---|---|
| M0 誤らせない（対照） | 許容の内（高 0.95） | 差の最大 1.29e-07（10 個）→ 許容の内（対照として期待どおり） | はい |
| M1 帯の起点を主位置の一つ後にする | 捕まえる（中 0.6）——帯の位置の一つを落とすだけで、読み取りの位置への加減は残る | 差の最大 0.000344（10 個）→ 許容の内＝捕まえなかった（この模型での盲点） | **いいえ（外れ）** |
| M2 書き換える層を一つ後にする | 捕まえる（高 0.9） | 差の最大 0.00154（10 個）→ 許容の外＝捕まえた | はい |
| M3 符号を反転する | 捕まえる（高 0.95） | 差の最大 0.565（10 個）→ 許容の外＝捕まえた | はい |
| M4 係数を二度掛ける（sign×coef×coef×v） | 捕まえる（中 0.75）——足した量が隠れ状態より大きい領域では、正規化が大きさを打ち消して差が縮みうる | 差の最大 0.000902（10 個）→ 許容の内＝捕まえなかった（この模型での盲点） | **いいえ（外れ）** |
| M5 読み取りで正規化を二度当てる | 捕まえる（高 0.9） | 差の最大 0.0459（10 個）→ 許容の外＝捕まえた | はい |
| M6 読み取りを bf16 で当てる | 五分五分（中 0.5）——丸めの差は許容の前後の見込み | 差の最大 0.000578（10 個）→ 許容の内＝捕まえなかった（この模型での盲点） | —（五分五分の予想） |

- 対照（M0）は許容の内。わざと誤らせた 6 変種のうち、フックの道との差が許容を超えた（捕まえた）のは 3（M2・M3・M5）、超えなかった（捕まえなかった）のは 3（M1・M4・M6）。事前登録の予想の外れは 2（M1・M4）。捕まえなかった変種は、この小さな模型での一段目の突き合わせの盲点として記録し、器の誤りとはしない。
- 読み（書き手の推測・確かめていない）: 許容 0.001 の判定は、捕まえなかった変種（M1・M4・M6）の型の誤りを捕まえない。ただし二つの道の間で観測された効き目の差の最大（2.54e-07）は、捕まえなかった変種の差の最大のうち最小のもの（M1 の 0.000344）の 1,400 分の一（組み立ての器が印字の値から計算し、有効数字二桁に丸めた）。二つの道の片方だけにその型の誤りがあれば、観測された差はその変種の差の桁になったはず、と読める——この小さな模型の上では、二つの道の間にその型の食い違いは見えない。二つの道が同じ誤りを共有していれば、この読みは何も言わない。**判定の決まり（許容）を変える提案ではない。**

## 6. 正本で決まっていなかった所（選んだ決め方と理由）

1. **FJ の形**: 関数の引数 FJ が設計事実のファイルの全体か、その `facts` の中身かは決まっていない。両方を受ける（`facts` の鍵があれば中を使う）。`--dry` ではファイルの全体をフックの道にも渡した。
2. **mask の組み方（`use_cache`）**: 正本は「近道なし・バッチ一」と、指示の「mask は模型の forward と同じ」だけで、模型の forward のどの呼び方に合わせるかは決めていない。4.57.3 では `use_cache`（と attention_mask の有無）で、mask が None（SDPA の is_causal）か明示の真偽の mask かに分かれる。既定を模型の forward の既定（`config.use_cache`・attention_mask なし）に合わせ、`use_cache=False` を選べる任意の引数を足した。二つの形は、どちらも同じ形の模型の forward とビット単位で一致し（§4）、この CPU では互いに同じ値だった（§5）。
3. **加減のベクトルの型の直し方**: 正本は「層の出力の型に直して足す」。`make_hook` は NumPy の float32 を経てから層の出力の型にする。これに合わせた。§4 の参考の行（`[参考] float32 を経た bf16 と float64 から直に直した bf16 が同じ合成の方向: 49/49（判定に入れない）`）のとおり、合成の方向では float32 を経ても float64 から直に直しても bf16 のベクトルは同じだった。
4. **無操作の符号**: 零のベクトルを行の符号で足した（どちらの符号でも値は同じ）。
5. **`--dry` の行の選び方**: 指示は「static の行を二つ（減算の行と加算の行を一つずつ）」。`main_rows` の順で最初の減算の行と、族を両方覆うために減算の行と違う族の最初の加算の行を選んだ（§5 の比べた組）。指示の公開の関数の例は S1 の二つの升目だったが、族の違い（選択の文字の数）も突き合わせに入れるためにこうした。
6. **`--dry` の比べる相手**: 指示は「実在の差の方向の名の合成の方向を、行の符号と逆の符号の両方で」。正本の static の比べる相手は、O と Osec の入れ替えを含む対（`nulls.real.swap_siblings`・4 対）を除いた 24 対（向きまで数えて 48）だが、`--dry` は転記行 D の全ての対の名（28 対）を使った——数の突き合わせの試験としては網が広い方がよく、除く対を含めても害が無いため。本の計算では dirs_by_row を呼び手が渡すので、この選び方は `recompute_rewrite` の中に無い。
7. **方向のノルムの確かめ**: 正本は方向を ‖v̂‖ に揃えることを決めているが、再計算の器が確かめるかは決めていない。dirs に static があれば、使う零でない方向を相対 1e-06 で照らし、外れたら止めることにした。
8. **版の縛り**: 手回しの道は 4.57.3 の forward を写しているので、transformers が正本 `inputs.versions_B` の版でなければ止めることにした。
9. **hook の確かめ**: 呼ぶ前と後に forward の hook が一本でもあれば止めることにした（フックの道の掛け残しを混ぜないため）。
10. **係数の縛り**: 係数が `layers.coef_applied` と違えば止めることにした（合成の試験で係数を変えたいときも止まる）。
11. **印字**: 正本は「器は段ごとに一致か不一致かだけを印字し、値は開かない」。`recompute_rewrite` は値を印字しない。`--dry` が差の最大と効き目の大きさを印字するのは、指示によることと、乱数の小さな模型だけで走ることによる。
12. **札の一致**: 正本の一致は「全ての効き目の差の絶対値が許容の内」で、かつ二つの道の値からそれぞれ出した「札が同じ」とき。札は集計の器の仕事なので、この器は効き目の差だけを見た。

## 7. コーディネータに伝えたいこと

1. **本物の模型（GPU）での mask の組み方を二つの道で揃えてほしい。** CPU では二つの形の値が同じだったが、GPU の bf16 の SDPA では、is_causal の核と明示の mask の核で値が変わりうる。フックの道が模型の forward を既定の呼び方（`use_cache` を渡さず attention_mask も渡さない、または attention_mask を全て一で渡す）で呼んでいるなら、この器の既定と同じ形になる。`use_cache=False` かつ attention_mask なしで呼んでいるなら、この器を `use_cache=False` で呼ぶと同じ形になる。どちらかは、この器からは分からない（フックの道の中を見ていない）。
2. **呼び方**: `recompute_rewrite(model, tok, T3, FJ, rows, dirs_by_row, dirs, layer_idx, coef)`（`use_cache` は任意の鍵の引数）。rows の行の名が正本 `main_rows` の名なら、升目と符号を正本と照らし、違えば止まる。dirs は float64 で、static があれば零でない全ての方向が ‖static‖ に揃っていること。模型は bf16・eval・forward の hook なし・transformers は正本の版。
3. **値の印字**: この器は値を印字しない。本の計算で差の最大を開かないのは、呼び手の器の決まり（`independent_recompute.print`）。
4. **費用**: 一回の順伝播は模型の全層を列の全体に流すだけで、全語彙の出口の値を作らない（読み取りの集合の行だけ）。本の計算の順伝播の数は転記行 E のとおりで、この器は数を変えない。乱数の小さな模型の CPU での時間は §5 の行（CPU の混み具合で揺れる）。
5. **突き合わせの結果**: §5。フックの道の後に走らせ直したこの器の値は一度目とビット単位で同じだった（`参考: フックの道の後に走らせ直した残差の書き換えの道（無操作と static・2 行）が一度目と同じ（ビット単位）: 同じ`）——掛け残しや模型の変化は見えなかった。
6. **一段目の突き合わせの弁別力（歯の変種・§5.1）**: 対照（M0）は許容の内。わざと誤らせた 6 変種のうち、フックの道との差が許容を超えた（捕まえた）のは 3（M2・M3・M5）、超えなかった（捕まえなかった）のは 3（M1・M4・M6）。事前登録の予想の外れは 2（M1・M4）。捕まえなかった変種は、この小さな模型での一段目の突き合わせの盲点として記録し、器の誤りとはしない。この小さな模型は、足す量が層の出力よりずっと大きい領域にあり（検分票の最後の項）、本物の模型の領域とは違うので、本物の模型での一段目の感度はこの結果からは言えない。コーディネータの合成の確かめ（草案 §12 の合成データ）が同じ小さな模型と同じ大きさの合成の方向を使うなら、同じ盲点がありうる。合成の方向の大きさを、本物の模型の相対の加減（正本 `layers.relative_injection_selected`）に近い領域に置いて変種の感度を測り直すことを勧める（書き手は試していない・採るかはコーディネータと登録者の判断）。
7. **系統外の目**: 二つの道はどちらも Claude 系が同じ指示から書いた。本物の模型での一段目の前など重要な確定の前に、系統外の検分を登録者に提案することを勧める（採るかは登録者の判断）。
8. **この器が見ていないこと**: 検分票の最後の項。

## 8. 既にあるファイルを変えていないことの機械の確かめ

- `git status --porcelain --untracked-files=all`（組み立ての時・この記録を書く前）:

```
?? tools/bl3_recompute_rewrite.py
```

- `git diff --stat`: （出力なし——追跡しているファイルに変更は無い）
- 一時置き場（`results/_smoke/rr_scratch/`・`.gitignore` の `results/_smoke/` の下）と、器を走らせたときに Python が作った `tools/__pycache__/`（`.gitignore` の `__pycache__/`・作業の前のワークツリーには無かった）は、この記録を組み立てた後に消した。

## 9. 出典の照合（組み立ての器が機械で照らした）

- 本文に「」で引いた正本の語句が、正本の次の鍵の文字列にそのまま含まれることを、組み立ての器が確かめた:
  - 「無操作は零のベクトル」 → 正本 `readout.primary.batching`（含まれる）
  - 「器は段ごとに一致か不一致かだけを印字し、値は開かない」 → 正本 `independent_recompute.print`（含まれる）
  - 「近道なし・バッチ一」 → 正本 `independent_recompute.new_paths`（含まれる）
  - 「層の出力の型に直して足す」 → 正本 `readout.primary.precision`（含まれる）
  - 「全ての効き目の差の絶対値が許容の内」 → 正本 `independent_recompute.agreement`（含まれる）
  - 「札が同じ」 → 正本 `independent_recompute.agreement`（含まれる）
- 指示の語句（「mask は模型の forward と同じ」・「static の行を二つ（減算の行と加算の行を一つずつ）」・「実在の差の方向の名の合成の方向を、行の符号と逆の符号の両方で」）は、指示の文から写した。指示の文はファイルに無いので、組み立ての器は照らしていない。

## 検分票

- **対象**: `tools/bl3_recompute_rewrite.py`（v1・SHA16 012CB2B68397614A）と本記録。
- **段階**: **事後適用**——本検分の手順（kensho）は、一段目の突き合わせの結果を見た後に当てた。事前にあったもの: 一段目の判定の決まり（正本の許容を効き目の差の最大に当てる・`dry:` の行）は `--dry` を走らせる前に器に書いた。予想（信頼度つき）は、歯の変種についてだけ、変種の器を書く前・走らせる前に時刻つきで書いた（§5.1）。一段目の突き合わせそのものの予想は事前に書いていない。作業の段階は、B-lens 層三の器の段（独立の再計算の器のうち、残差の書き換えの道）・封印の前・下見の前の凍結の前・系統内の器の実装の検分の前。
- **凍結物の同定**: 正本 `design/contrasts-Bl3.json` SHA16 6330B65A0AB503E7・設計事実 `records/Bl3/design-facts-Bl3.json` SHA16 9BB701E7D2AE1C7F（頭の contrasts_sha16 6330B65A0AB503E7）・段階 B の凍結の器 `tools/steer_B.py` SHA16 71157C6921E12AC7（正本の記録と一致）・`tools/run_stageB_local.py` SHA16 E976A4F5B63767FA（正本の記録と一致）・`tools/direction_B.py` SHA16 E84A101655685F2B・凍結の場面の記録 SHA16 7AD7E49459D5C402（正本の記録と一致）・突き合わせの相手 `tools/bl3_run.py` SHA16 7ECB9CF764F4F8AE・ワークツリーの頭 3bb772e7f1d049a7e1f115d6028a2de7a6d6f6cb・手元の版 torch 2.9.1+cpu・transformers 4.57.3・numpy 2.4.2。
- **盲検の状態**: 本物の模型で読み取りの値を出していない・見ていない（乱数の小さな模型だけ）。コーディネータのフックの道の実装は読んでいない（`--dry` で中を見ずに呼んだだけ）。ただし道の決まり（加減の算術・帯・読み取り・小さな模型の作り方）は、コーディネータが書いた指示から受け取っている（COI 記録の一）。
- **敵対的検分**: 書き手の自己の敵対の確かめだけ（系統内の別の個体による器の実装の検分〔草案 §12〕はまだ）。
  - 不利な材料を先に: (a) 二つの道は同じ指示から書かれ、共有の読み違いは突き合わせで捕まらない。(b) 突き合わせは CPU と乱数の小さな模型だけで、この模型では足す量が隠れ状態よりずっと大きい（下の最後の項）。(c) 歯の変種: 対照は許容の内・わざと誤らせた 6 変種のうち 3 を捕まえ、捕まえなかったのは M1・M4・M6・予想の外れは M1・M4（§5.1）。(d) §5 の読みの段の比は分母が揃っていない（§5 の注）。
  - 試みた反証: 歯の確かめ（hidden_states[-1] の取り違えを捕まえる・static の効き目が零でない）、止まるべき所で止まるかの負の試験（転記行 B のずれ・書き出しの割り方・hook・層・係数・型・ノルム・正本の行の升目と符号）、hook を掛ける関数を呼ばれたら落ちる形に差し替えて走らせる試験、フックの道の後の走らせ直し、歯の変種（§5.1・事前登録つき）。
  - 分母: 突き合わせの最大は、二つの道の同じ鍵の集合（行と「方向の名|符号」）の上で取った（鍵の集合の一致は器が確かめ、違えば不一致と印字する）。基底率: 数え上げの主張は自己検査の ok の数だけで、その母数は器が定めた確かめの数（全て書き手が書いた確かめで、独立の確かめの数ではない）。出典ピン留め: 本文に引いた正本の語句は、組み立ての器が正本の文字列と照らした（§9）。
- **系統の内訳**: 書き手＝Claude Opus 5.5（Claude Code の下請けの個体）。突き合わせの相手の書き手＝コーディネータ（Claude 系の別の個体）。系統外の目は通っていない。二つの道はどちらも Claude 系が同じ指示から書いたので、系統と指示に共通の読み違いは、一段目の突き合わせでは捕まらない。「自己検査が全て ok」「突き合わせが許容の内」を、器が本物の模型で正しいことの資格として引かない（検分の教訓13）。本物の模型での一段目の前など重要な確定の前には、系統外の検分を登録者に提案する（採るかは登録者の判断）。
- **COI 記録**:
  - (一) 道の決まりの出所が共通: 加減の算術・帯・読み取りの量・小さな模型の作り方は、コーディネータが書いた指示（正本からの写し）から受け取った。指示そのものの誤り（正本の読み違い）は二つの道で共有されるので、一段目の突き合わせでは捕まらない。
  - (二) 情報の状態: 作業の頭に見た git のコミットの文から、フックの道が段階 B の凍結の `make_hook` をそのまま呼ぶことを知っていた。書き換えの算術を `make_hook` に合わせたのは指示による。それ以上のフックの道の中身は知らない。
  - (三) 希望の向きの引力: 書き手には「突き合わせが一致してほしい」引力がある。判定の許容（正本 `tol_stage1`）と判定の行は走らせる前に器に書き、mask の既定の形も `--dry` の前に決めた。器を仕上げる途中で `--selftest` と `--dry` を試しに走らせ（どれも同じ判定——自己検査は全て ok、突き合わせは許容の内）、その後に次を変えてから、仕上げの版で両方を走らせ直した: 歯の確かめを hidden_states[-1] の取り違えそのものの形に変えた（前は正しい入力に正規化を二度当てた形）／参考の行を足した（float32 を経る型の直し・mask の形・float64 での読み直し）／止める確かめを一つ足した（bf16）／読み取りを、層が複数の装置に割られていても正規化の重みと語彙の行列の装置で当てる形にした（一つの装置では値は変わらない）／`--dry` の行の数を器が数える形にし、札を見ていない旨の行を足した／頭の文の層の添字を正本の鍵で書いた。そのあと、本検分の手順（kensho）を当てて、歯の変種（事前登録つき・§5.1）を `--dry` の参考に足し、仕上げの版でもう一度両方を走らせ直した。判定の決まり（許容と判定の行）は変えていない。試しの版の出力は残していない——実行ごとに書き先を分けず、同じ一時置き場に仕上げの版が上書きした（検分の教訓22の同型）。
  - (四) 独立の範囲: 独立なのは、加減の仕組み（層の出力の書き換え対フック）・層の回し方・読み取りの実装・升目の組み立ての書き方・行と方向の帳簿。共有しているのは、模型の部品・transformers・段階 B の凍結の関数・トークナイザ・設計事実・指示。
  - (五) 組み立ての器の誤りの記録: この記録を組み立てる器は、一度、歯の変種の短い要約（§0・検分票）に、捕まえた変種の一覧を「捕まえなかった」欄に入れる取り違えを作った（長い要約と表は正しかった）。組み立ての後の読み直しで見つけて直し、一覧の照合を組み立ての器に足した。ほかにも、ログの改行（CRLF）とハッシュの取り方の食い違いを組み立ての途中で見つけ、改行を LF にそろえた SHA-256 に直した（§4・§5）。
- **判定**: **保留**。器の出力の数は器の出力のとおり（自己検査 `selftest: 43/43 ok`・`--dry` `dry: 一段目の許容（0.001）の内（効き目の差の最大 2.54e-07）`・歯の変種は §5.1）。器が本物の模型で正しいことは、コーディネータの確かめ・系統内の器の実装の検分・本物の模型での一段目の突き合わせを経るまで保留する。コーディネータの確かめに回せる水準、と書き手は判断する（書き手自身の判定で、独立の検分を経ていない・登録者の裁定の代わりにならない）。
- **本検分が確認していないこと**:
  - 本物の模型（GPU・bf16）での一致（SDPA の核の選び方・bf16 の GEMM の違い・複数の装置に割ったときの動き）
  - 正本の一致の決まりの後半（札の一致）と、二段目（本の道と本の器のフック）
  - 指示と正本の読みそのものの正しさ（読み取りの集合・帯・符号の決まり・無操作の置き方）——二つの道が同じ指示に従うので、共有の読み違いは捕まらない
  - 凍結の方向の npz（本物の方向）での動き、本の計算の順伝播の数と時間
  - コーディネータの合成の模型と、この器の小さな模型の乱数の引き方が同じか
  - フックの道の側の誤りを一段目の突き合わせが捕まえるか（歯の変種は書き手の道の側だけを誤らせた）と、精度の水準の誤り（例: 加減を float32 のまま足す）を捕まえるか（歯の変種に入れていない）
  - 突き合わせと歯の変種の感度が本物の模型でも同じか——この小さな模型では、足す量のノルムが層 L の出力のノルムの 99〜103 倍（二つの升目の主位置・組み立ての器が器の関数で計算）で、本物の模型の正本の値 `layers.relative_injection_selected`＝0.0608 と領域がまるで違う（正本の値の定義とこの比の定義が同じかは確かめていない）
  - transformers の版の違いへの頑健さ（版が違えば止めるだけ）
  - 本記録の文（手で書いた部分）の正しさ——数とハッシュは機械で写したが、文は書き手の読み

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/tools/recompute-rewrite-dev-Bl3.md` >>>

==================== 第六部 集計の器と合成データの器と試しの記録 ====================

<<< 始: `tools/analyze_Bl3.py`（SHA16 41600F9C96222BBD・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """analyze_Bl3.py v1 —— B-lens 層三（Bl3）の集計の器（主の札・門・記述の門・q7・独立の再計算の一致・予想の答え・2026-09-25）。
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
 14 | import os, re, sys, json, glob, collections
 15 | import numpy as np
 16 | 
 17 | HERE = os.path.dirname(os.path.abspath(__file__))
 18 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 19 | sys.path.insert(0, HERE)
 20 | import blens_core as C
 21 | import bl3_core as K
 22 | 
 23 | VERSION = 'v1'
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
 65 |             cache[k] = [t for t in (json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')) if t['status'] == 'ok']
 66 |         return cache[k]
 67 |     return f
 68 | 
 69 | 
 70 | # ---------------- 主の札 ----------------
 71 | def row_labels(T3, main_rows, eff, pair_names, dropped_cells=(), p_override=None):
 72 |     """主の行の札。eff: 升目と符号の鍵 → {方向の名: 効き目}。p_override: 行の名 → (効き目, 等方の帰無)（独立の再計算で v̂ の行を置き換えるとき）。"""
 73 |     swaps = T3['nulls']['real']['swap_siblings']
 74 |     alpha = T3['labels']['iso_outside']['holm_alpha']
 75 |     n_iso = T3['nulls']['isotropic']['count']
 76 |     out, pv = collections.OrderedDict(), {}
 77 |     rows = [r for r in main_rows if '%s|%s' % (r['scenario'], r['base']) not in set(dropped_cells)]
 78 |     for r in rows:
 79 |         k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
 80 |         if p_override and r['id'] in p_override:
 81 |             e, iso = p_override[r['id']]['effect'], p_override[r['id']]['iso']
 82 |             same, opp = p_override[r['id']]['comps_same'], p_override[r['id']]['comps_opp']
 83 |         else:
 84 |             e = eff[k][r['direction']]
 85 |             iso = [eff[k]['iso:%d' % i] for i in range(n_iso)]
 86 |             comps = K.comparators_for(r['direction'], pair_names, swaps)
 87 |             same, opp = [eff[k]['real:' + p] for p in comps], [eff[kk]['real:' + p] for p in comps]
 88 |         pt = K.p_and_tail(e, iso)
 89 |         sl = K.second_label(e, list(same) + list(opp), list(zip(same, opp)))
 90 |         out[r['id']] = {'direction': r['direction'], 'cell_sign': k, 'effect': e, 'p': pt['p'], 'upper': pt['upper'], 'lower': pt['lower'], 'tail': pt['tail'],
 91 |                         'iso_median': float(np.median(iso)), 'second': sl, 'iso_top_share': K.iso_top_share(iso, sl['center'], list(same) + list(opp)), '_iso': iso}
 92 |         pv[r['id']] = pt['p']
 93 |     H = K.holm(pv, alpha)
 94 |     for rid, o in out.items():
 95 |         o['holm_step'], o['iso_outside'] = H[rid]['step'], bool(H[rid]['pass'])
 96 |         o['side'] = K.effect_side(o['effect'], o.pop('_iso')) if o['iso_outside'] else None
 97 |     return out, {'m_rows': len(rows), 'dropped_rows': [r['id'] for r in main_rows if r not in rows]}
 98 | 
 99 | 
100 | def labels_signature(lab):
101 |     """札の一致で見る中身（正本 `independent_recompute.agreement`）: Holm の判定・割合を決めた裾・等方の外の行の効き目の側・二つ目の札。"""
102 |     return {rid: (o['iso_outside'], o['tail'], (o['side'] or {}).get('side'), (o['side'] or {}).get('sign'), o['second']['top']) for rid, o in lab.items()}
103 | 
104 | 
105 | # ---------------- 門 ----------------
106 | def gates(T3, rows, eff, dropped_cells=(), style_rows=()):
107 |     units = ['static', 'loaded', 'Nk', 'td'] + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
108 |     alpha = T3['gate']['alpha']
109 |     ue = {u: {f: eff[f][u] for f in sorted({r['fam'] for r in rows})} for u in units}
110 |     rs = lambda pred, yk='y': [{'unit': r['unit'], 'cell': r['cell'], 'fam': r['fam'], 'y': r[yk]} for r in rows if pred(r)]
111 |     out = collections.OrderedDict()
112 |     out['main'] = K.gate(rs(lambda r: True), ue, units, alpha, dropped_cells)
113 |     out['without_vhat'] = K.gate(rs(lambda r: r['unit'] != 'static'), ue, [u for u in units if u != 'static'], alpha, dropped_cells)
114 |     out['desc_without_vhat_loaded'] = K.gate(rs(lambda r: r['unit'] not in ('static', 'loaded')), ue, [u for u in units if u not in ('static', 'loaded')], alpha, dropped_cells)
115 |     out['desc_choice_a'] = K.gate(rs(lambda r: True, 'y_a'), ue, units, alpha, dropped_cells)
116 |     out['desc_without_style'] = K.gate(rs(lambda r: r['name'] not in set(style_rows)), ue, units, alpha, dropped_cells)
117 |     return out
118 | 
119 | 
120 | # ---------------- 予想の答え ----------------
121 | def prediction_truth(T3, pilot_attempts, lab, G, q7_rows, floor):
122 |     q1 = K.q1_from_attempts(pilot_attempts)
123 |     stopped = (not q1['scored']) or q1['q1'] == '止める'
124 |     items = {it['key']: it for it in T3['predictions']['items']}
125 |     tr = collections.OrderedDict()
126 |     tr['q1.pilot'] = q1['q1'] if q1['scored'] else None
127 |     if stopped:
128 |         for k in list(items)[1:]:
129 |             tr[k] = None
130 |         return tr, {'stopped': True, 'q1': q1}
131 |     tr['q2.vhat_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'static' and o['iso_outside']), items['q2.vhat_iso']['options'])
132 |     tr['q3.nk_iso'] = K.bucket(sum(1 for o in lab.values() if o['direction'] == 'Nk' and o['iso_outside']), items['q3.nk_iso']['options'])
133 |     tr['q4.gate'] = None if G['main']['undetermined'] else ('通る' if G['main']['pass'] else '通らない')
134 |     tr['q5.gate_wo_vhat'] = None if G['without_vhat']['undetermined'] else ('通る' if G['without_vhat']['pass'] else '通らない')
135 |     tr['q6.second'] = K.bucket(sum(1 for o in lab.values() if o['second']['top']), items['q6.second']['options'])
136 |     tr['q7.direction'] = K.score_q7(q7_rows, floor) if q7_rows else None
137 |     return tr, {'stopped': False, 'q1': q1}
138 | 
139 | 
140 | def q7_rows_of(lab, FJ):
141 |     iv = {x['id']: x for x in FJ['facts']['C']['q7_intervals']}
142 |     return [{'id': rid, 'effect': o['effect'], 'stage_b_diff': iv[rid]['diff_pt'], 'contains_zero': iv[rid]['contains_zero']}
143 |             for rid, o in lab.items() if o['direction'] == 'static' and o['iso_outside']]
144 | 
145 | 
146 | # ---------------- 独立の再計算の一致 ----------------
147 | def recompute_agreement(T3, main_rows, eff_main, pair_names, hook, rewrite, pilot, dropped_cells=(), rows_subset=None):
148 |     """二段の一致（正本 `independent_recompute.stages`・`agreement`）。hook と rewrite: 行の名 → {'noop_lo','effects': {'方向|符号': 効き目}}。
149 |     本の計算では v̂ の行のすべてを比べる（行が欠ければ一致しない）。rows_subset は合成データの確かめで比べる行を絞るときだけ使う。"""
150 |     comps_of = lambda d: K.comparators_for(d, pair_names, T3['nulls']['real']['swap_siblings'])
151 |     n_iso = T3['nulls']['isotropic']['count']
152 | 
153 |     def override(path):
154 |         ov = {}
155 |         for r in main_rows:
156 |             if r['direction'] != 'static' or r['id'] not in path or (rows_subset is not None and r['id'] not in rows_subset):
157 |                 continue
158 |             E = path[r['id']]['effects']
159 |             s = r['sign']
160 |             ov[r['id']] = {'effect': E['static|%+d' % s], 'iso': [E['iso:%d|%+d' % (i, s)] for i in range(n_iso)],
161 |                            'comps_same': [E['real:%s|%+d' % (p, s)] for p in comps_of('static')], 'comps_opp': [E['real:%s|%+d' % (p, -s)] for p in comps_of('static')]}
162 |         return ov
163 | 
164 |     def as_eff(ov):
165 |         return {rid: [o['effect']] + list(o['iso']) + list(o['comps_same']) + list(o['comps_opp']) for rid, o in ov.items()}
166 |     main_ov = {}
167 |     for r in main_rows:
168 |         if r['direction'] != 'static' or (rows_subset is not None and r['id'] not in rows_subset):
169 |             continue
170 |         k, kk = key3(r['scenario'], r['base'], r['sign']), key3(r['scenario'], r['base'], -r['sign'])
171 |         main_ov[r['id']] = {'effect': eff_main[k]['static'], 'iso': [eff_main[k]['iso:%d' % i] for i in range(n_iso)],
172 |                             'comps_same': [eff_main[k]['real:' + p] for p in comps_of('static')], 'comps_opp': [eff_main[kk]['real:' + p] for p in comps_of('static')]}
173 |     sig = lambda ov: labels_signature(row_labels(T3, main_rows, eff_main, pair_names, dropped_cells, p_override=ov)[0])
174 |     hk, rw = override(hook), override(rewrite) if rewrite is not None else None
175 |     tol2 = K.cache_tol(pilot['floor'], T3['pilot']['cache_tol_factor'], T3['pilot']['cache_tol_floor'], T3['pilot']['noise_max']) + pilot['floor']
176 |     out = {'second': K.agreement(as_eff(main_ov), as_eff(hk), tol2, sig(main_ov), sig(hk)), 'tol_second': tol2}
177 |     out['first'] = K.agreement(as_eff(hk), as_eff(rw), T3['independent_recompute']['tol_stage1'], sig(hk), sig(rw)) if rw is not None else None
178 |     out['tol_first'] = T3['independent_recompute']['tol_stage1']
179 |     out['agree'] = bool(out['second']['agree'] and (out['first'] or {}).get('agree', False))
180 |     return out
181 | 
182 | 
183 | # ---------------- 乙（裁定 D227） ----------------
184 | def secondary_rows(T3, rows_gate, FB):
185 |     """乙の行（裁定 D227）: 門の行のうち、方向が名前のある方向か段階 B の三本で、土台の升目が B-lens の層二の層にある行。符号は門の行の符号。
186 |     戻り値: 升目の鍵 → [(行の名〔場面|腕|単位〕, 方向の名, 符号)]（行の名は B-lens の層二の答えの文字の位置の行と同じ書き方）。"""
187 |     strata_cells = {'%s|%s' % tuple(k.split('|')[:2]) for k in FB['facts']['E']['selected']}
188 |     units = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
189 |     out = collections.OrderedDict()
190 |     for r in rows_gate:
191 |         if r['cell'] in strata_cells and r['unit'] in units:
192 |             out.setdefault(r['cell'], []).append(('%s|%s|%s' % (r['scenario'], r['arm'], r['unit']), r['unit'], r['sign']))
193 |     return out
194 | 
195 | 
196 | def secondary_counts(FB, rows_by_cell):
197 |     """乙の順伝播の数（文脈ごとの行の数の和・文脈ごとの符号の数の和〔無操作と同じバッチに流す〕）。"""
198 |     n_rows = n_batches = 0
199 |     for key, ids_ in FB['facts']['E']['selected'].items():
200 |         rows = rows_by_cell.get('%s|%s' % tuple(key.split('|')[:2]), [])
201 |         n_rows += len(ids_) * len(rows)
202 |         n_batches += len(ids_) * len({sg for _, _, sg in rows})
203 |     return {'row_passes': n_rows, 'sign_batches': n_batches, 'contexts': sum(len(v) for v in FB['facts']['E']['selected'].values())}
204 | 
205 | 
206 | def secondary_summary(sec_out, calib_letter=None):
207 |     """乙のまとめ（記述・読みは付けない）: 行ごとに、文脈の間の平均・中央値・四分位と、B-lens の層二の直接の経路の値（あれば）を並べる。"""
208 |     acc = collections.defaultdict(lambda: collections.defaultdict(list))
209 |     for c in sec_out:
210 |         for name, v in c['rows'].items():
211 |             for k, x in v.items():
212 |                 acc[name][k].append(x)
213 |     out = collections.OrderedDict()
214 |     for name, d in acc.items():
215 |         s = {k: {'mean': float(np.mean(v)), 'median': float(np.median(v)), 'q1': float(np.percentile(v, 25)), 'q3': float(np.percentile(v, 75)), 'n': len(v)} for k, v in d.items()}
216 |         if calib_letter is not None:
217 |             sc = name.split('|')[0]
218 |             arm = name.split('|')[1]
219 |             base = re.split(r'[+\-]v', arm)[0]
220 |             bl = ((calib_letter.get('%s|%s' % (sc, base)) or {}).get('rows') or {}).get(name)
221 |             s['blens_direct'] = {k: bl[k] for k in ('dlogit_exact_a', 'dlogit_exact_c')} if bl else None
222 |         out[name] = s
223 |     return out
224 | 
225 | 
226 | # ---------------- 記述 ----------------
227 | def descriptive(T3, main_out):
228 |     mm = T3['pilot']['mass_min']
229 |     below = {k: sum(1 for d, v in o['mass'].items() if d != K.NOOP and v < mm) for k, o in main_out.items()}
230 |     pa = {k: o['pa_noop'] for k, o in main_out.items()}
231 |     return {'mass_below_min': below, 'pa_noop': pa}
232 | 
233 | 
234 | def analyze(T3, FJ, main_out, pilot_attempts, pair_names, rows_gate, hook=None, rewrite=None, style_rows=(), rows_subset=None):
235 |     """集計の全体（読みは付けない）。main_out: 升目と符号の鍵 → run_cell_sign の出力。pilot_attempts: 下見の試みの並び（最後が本の凍結の下見）。"""
236 |     pilot = pilot_attempts[-1]
237 |     dropped = (pilot.get('decision') or {}).get('dropped', [])
238 |     eff = {k: o['effects'] for k, o in main_out.items()}
239 |     lab, meta = row_labels(T3, T3['main_rows'], eff, pair_names, dropped)
240 |     G = gates(T3, rows_gate, eff, dropped, style_rows)
241 |     q7 = q7_rows_of(lab, FJ)
242 |     truth, tmeta = prediction_truth(T3, pilot_attempts, lab, G, q7, pilot.get('floor', 0.0))
243 |     out = collections.OrderedDict(version=VERSION, rows=lab, rows_meta=meta, gates=G, q7_rows=q7, predictions_truth=truth, predictions_meta=tmeta,
244 |                                   descriptive=descriptive(T3, main_out), chance={'oriented': T3['nulls']['real']['chance_second'], 'pair': T3['nulls']['real']['chance_second_pair']})
245 |     if hook is not None:
246 |         out['recompute'] = recompute_agreement(T3, T3['main_rows'], eff, pair_names, hook, rewrite, pilot, dropped, rows_subset)
247 |     return out
248 | 
249 | 
250 | # ---------------- 段階 B のその行の注（報告の雛形） ----------------
251 | def stage_b_notes(T3, AN, rows_gate):
252 |     """段階 B のその行の注（正本 `report_rules.template`「主の表と門の行に、段階 B のその行の注（判定保留・ランダム方向の不均一）を写す」）。
253 |     主の行: 段階 B の確かめの行（凍結した集計器の記録の `confirm`・同じ名）の札と注と様式の保留。門の行: 名前のある方向の行は、その腕を比べの加えた腕に持つ確かめの行の札が
254 |     判定保留のときその札。ランダム方向の行は、その腕の不均一の記録（`homogeneity`）に注があるときその注。"""
255 |     conf = {r['id']: r for r in AN['confirm']}
256 |     conf_by_arm = {(r['scenario'], r['A']): r for r in AN['confirm']}
257 |     homo = {(h['scenario'], h['arm']): h for h in AN['homogeneity']}
258 |     main = collections.OrderedDict()
259 |     for r in T3['main_rows']:
260 |         c = conf.get(r['id'])
261 |         main[r['id']] = {'label': c['label'] if c else None, 'notes': list(c.get('notes') or []) if c else [], 'style_hold': bool(c and c.get('style_hold'))}
262 |     gate = collections.OrderedDict()
263 |     for g in rows_gate:
264 |         notes = []
265 |         if g['unit'].startswith('rand:'):
266 |             h = homo.get((g['scenario'], g['arm']))
267 |             if h and h.get('note'):
268 |                 notes.append({'kind': 'ランダム方向の不均一', 'spread_pt': h['spread_pt'], 'threshold_pt': h['threshold_pt']})
269 |         else:
270 |             c = conf_by_arm.get((g['scenario'], g['arm']))
271 |             if c and str(c.get('label', '')).startswith('判定保留'):
272 |                 notes.append({'kind': c['label']})
273 |         gate[g['name']] = notes
274 |     return {'main': main, 'gate': gate}
275 | 
276 | 
277 | # ---------------- 手元の二つの段（一致だけを見る・結果を開く・正本 `independent_recompute.print`・`on_mismatch`） ----------------
278 | PARTS = ('main', 'recompute', 'secondary')
279 | JUDGE = os.path.join(REPO, 'records', 'Bl3', 'judge-Bl3.json')
280 | OPENED = os.path.join(REPO, 'records', 'Bl3', 'analysis-Bl3.json')
281 | 
282 | 
283 | def load_outputs(dirs):
284 |     """起動器の相 main の出力（組ごとの JSON と、その置き場の session.json）を、一つ以上の置き場から読む。同じ組が二つあれば止める。"""
285 |     parts, sessions = collections.OrderedDict(), collections.OrderedDict()
286 |     for d in dirs:
287 |         S = json.load(open(os.path.join(d, 'session.json'), encoding='utf-8'))
288 |         for part in PARTS:
289 |             p = os.path.join(d, '%s.json' % part)
290 |             if os.path.exists(p):
291 |                 if part in parts:
292 |                     raise SystemExit('同じ組が二つの置き場にある（止める）: %s' % part)
293 |                 parts[part] = json.load(open(p, encoding='utf-8'))
294 |                 sessions[part] = S
295 |     return parts, sessions
296 | 
297 | 
298 | def env_same(sessions):
299 |     """組の間で、コミット・GPU・版・正本・方向の npz・DRY が同じか（違えば記す・二段目の比べに環境の違いが入る）。"""
300 |     keys = ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef')
301 |     ref = next(iter(sessions.values())) if sessions else {}
302 |     diff = {k: {p: s.get(k) for p, s in sessions.items()} for k in keys if any(s.get(k) != ref.get(k) for s in sessions.values())}
303 |     return {'same': not diff, 'diff': diff}
304 | 
305 | 
306 | def with_iso(T3, n_iso):
307 |     """独立の再計算の等方の本数に合わせた正本の写し（本の計算では正本と同じ本数・DRY で減らしたときだけ違う）。"""
308 |     if n_iso == T3['nulls']['isotropic']['count']:
309 |         return T3
310 |     T3x = json.loads(json.dumps(T3))
311 |     T3x['nulls']['isotropic']['count'] = n_iso
312 |     return T3x
313 | 
314 | 
315 | def judge(T3, parts, sessions, pilot_attempts, pair_names):
316 |     """一致だけを見る段: 器の誤りの有無・組の環境・二段の一致か不一致かだけを返す（効き目の値と差の最大は返さない）。"""
317 |     out = collections.OrderedDict(parts=list(parts), tool_error={p: bool(v.get('tool_error')) for p, v in parts.items()}, env=env_same(sessions))
318 |     dry = any(s.get('dry') for s in sessions.values())
319 |     out['dry'] = dry
320 |     if any(out['tool_error'].values()) or not {'main', 'recompute'} <= set(parts):
321 |         out.update(first=None, second=None, agree=None, reason='器の誤りか、組 main・recompute の欠け')
322 |         return out
323 |     pilot = pilot_attempts[-1]
324 |     rc = parts['recompute']
325 |     eff = {k: o['effects'] for k, o in parts['main']['cells'].items()}
326 |     ag = recompute_agreement(with_iso(T3, rc['n_iso']), T3['main_rows'], eff, pair_names, rc['hook'], rc.get('rewrite'), pilot,
327 |                              (pilot.get('decision') or {}).get('dropped', []), rows_subset=set(rc['hook']) if dry else None)
328 |     out.update(first=None if ag['first'] is None else bool(ag['first']['agree']), second=bool(ag['second']['agree']), agree=bool(ag['agree']),
329 |                reason=None if ag['agree'] else ('一段目の道が無い' if ag['first'] is None else '二段のどちらかが一致しない'))
330 |     return out
331 | 
332 | 
333 | def open_results(T3, FJ, parts, sessions, pilot_attempts, pair_names, AN, calib_letter, FB, repo=REPO):
334 |     """結果を開く段（登録者と一緒に・一致だけを見る段が一致したとき）: 集計の全体と、報告に並べるもの（下見の記録・頭の確かめ・層ごとの差分・乙・段階 B の注・環境）。"""
335 |     rc = parts['recompute']
336 |     dry = any(s.get('dry') for s in sessions.values())
337 |     T3x = with_iso(T3, rc['n_iso'])
338 |     rows_gate = stage_b_gate_rows(T3, AN, trials_reader(repo))
339 |     style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
340 |     A = analyze(T3x, FJ, parts['main']['cells'], pilot_attempts, pair_names, rows_gate, hook=rc['hook'], rewrite=rc.get('rewrite'), style_rows=style_rows,
341 |                 rows_subset=set(rc['hook']) if dry else None)
342 |     main_keys = {key3(sc, b, sg) for sc, b, sg in T3['cell_signs_main']}
343 |     A['dry'] = dry
344 |     A['pilot_attempts'] = pilot_attempts
345 |     A['head'] = parts['main']['head']
346 |     A['main_run'] = {k: parts['main'].get(k) for k in ('batch', 'shortcut', 'dropped')}
347 |     A['layerwise'] = {k: o['layers'] for k, o in parts['main']['cells'].items() if k in main_keys}
348 |     A['gate_rows'] = [{k: r[k] for k in ('name', 'scenario', 'arm', 'unit', 'sign', 'cell', 'fam', 'y', 'y_a', 'style_pt')} for r in rows_gate]
349 |     A['style_rows'] = style_rows
350 |     A['stage_b_notes'] = stage_b_notes(T3, AN, rows_gate)
351 |     if 'secondary' in parts:
352 |         S2 = parts['secondary']
353 |         A['secondary'] = {'counts': S2.get('counts'), 'contexts_run': len(S2.get('contexts') or []), 'summary': secondary_summary(S2.get('contexts') or [], calib_letter)}
354 |     A['sessions'] = {p: {k: s.get(k) for k in ('commit', 'dry', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'layer_idx', 'coef', 'finished')} for p, s in sessions.items()}
355 |     A['env'] = env_same(sessions)
356 |     A['clause'] = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
357 |     return A
358 | 
359 | 
360 | def _pilot_attempts(args_pilot):
361 |     """下見の試みの並び: 本の計算では凍結の記録の本の凍結（`main_freeze.pilot_attempts`）から。DRY の出力を試すときだけ、相 pilot の出力の pilot.json を与える。"""
362 |     if args_pilot:
363 |         return [json.load(open(p, encoding='utf-8'))['pilot'] for p in args_pilot]
364 |     FR = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json'), encoding='utf-8'))
365 |     return FR['main_freeze']['pilot_attempts']
366 | 
367 | 
368 | def main():
369 |     import argparse
370 |     ap = argparse.ArgumentParser(description='B-lens 層三の手元の二つの段（judge: 一致だけを見る／open: 結果を開く）')
371 |     ap.add_argument('step', choices=['judge', 'open'])
372 |     ap.add_argument('dirs', nargs='+', help='起動器の相 main の出力の置き場（組ごとの JSON と session.json）')
373 |     ap.add_argument('--pilot', nargs='*', help='DRY の出力を試すときだけ: 相 pilot の出力の pilot.json（試みの順）')
374 |     ap.add_argument('--out', help='出力の置き場（既定は records/Bl3/judge-Bl3.json・analysis-Bl3.json）')
375 |     ap.add_argument('--judge-record', help='結果を開く段が読む、一致だけを見る段の記録（既定は records/Bl3/judge-Bl3.json）')
376 |     a = ap.parse_args()
377 |     T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
378 |     FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
379 |     DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
380 |     parts, sessions = load_outputs(a.dirs)
381 |     dry = any(s.get('dry') for s in sessions.values())
382 |     if a.pilot and not dry:
383 |         raise SystemExit('--pilot は DRY の出力を試すときだけ（本の計算では凍結の記録の本の凍結を読む）')
384 |     attempts = _pilot_attempts(a.pilot)
385 |     pair_names = list(DJ['groups']['real']['names'])
386 |     if a.step == 'judge':
387 |         out = a.out or JUDGE
388 |         if os.path.exists(out):
389 |             raise SystemExit('既にある（一致だけを見る段は一度だけ）: %s' % out)
390 |         J = judge(T3, parts, sessions, attempts, pair_names)
391 |         J['written_utc'] = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
392 |         J['clause'] = '本記録は一致か不一致かだけを持つ（値は開かない・正本 independent_recompute.print）。'
393 |         json.dump(J, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
394 |         say = lambda b: '無い' if b is None else ('一致' if b else '不一致')
395 |         print('[analyze_Bl3] 一致だけを見る段: 器の誤り %s・組の環境 %s・一段目 %s・二段目 %s・全体 %s（値は開いていない）' % (
396 |             'あり' if any(J['tool_error'].values()) else '無し', '同じ' if J['env']['same'] else '違う', say(J['first']), say(J['second']), say(J['agree'])))
397 |         if not J['agree']:
398 |             raise SystemExit('一致しない（結果を開く前に止め、逸脱の台帳に記して登録者に上げる・裁定 D219）')
399 |         return
400 |     jp = a.judge_record or JUDGE
401 |     if not os.path.exists(jp) or not json.load(open(jp, encoding='utf-8')).get('agree'):
402 |         raise SystemExit('一致だけを見る段の記録が無いか、一致していない（結果を開かない）: %s' % jp)
403 |     out = a.out or OPENED
404 |     if os.path.exists(out):
405 |         raise SystemExit('既にある: %s' % out)
406 |     AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
407 |     CB = json.load(open(os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json'), encoding='utf-8'))['magnitude']['letter']
408 |     FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
409 |     A = open_results(T3, FJ, parts, sessions, attempts, pair_names, AN, CB, FB)
410 |     json.dump(A, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else float(o))
411 |     print('[analyze_Bl3] 結果を開いた: %s' % os.path.relpath(out, REPO))
412 | 
413 | 
414 | if __name__ == '__main__':
415 |     main()
```
<<< 終: `tools/analyze_Bl3.py` >>>
