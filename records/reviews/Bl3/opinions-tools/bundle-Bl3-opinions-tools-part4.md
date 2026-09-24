（B-lens 層三の器についての意見伺いの束・分けた版 4／5・中身は一通版と同じ）

<<< 始: `tools/dry_run_Bl3.py`（SHA16 8B8793FA7C705C1F・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """dry_run_Bl3.py v1 —— B-lens 層三（Bl3）の合成データの器（正本 `review_plan.synthetic` の形のすべてと、乱数の小さな模型で端から端まで・2026-09-25）。
  3 | 
  4 | 一. 純粋な関数の形（`tools/bl3_core.py`・`tools/blens_core.py`）: 奇でない押し・零でない帰無の中心・減算の行・下見で外れる升目と門の行だけの升目・帰無との同じ値・
  5 |     両方の向きがちょうど対称な比べる相手・書き出しの割り方が変わる場合・掃き出し・端数のバッチ・零の近くの中央値・Holm の境で一本違う p・器の誤りでやり直す流れ。
  6 | 二. 乱数の小さな模型（登録機種の設定を小さくした bf16 の模型・実の重みではない・正規化の重みを散らす・CPU）と実のトークナイザで、走らせる器 `tools/bl3_run.py` の
  7 |     下見と本の計算と独立の再計算のフックの道を端から端まで通す（bf16 の揺れ・近道の許容の式・二段目の一致）。
  8 | 三. わざと壊した読み取り（二重の正規化）と近道（主位置まで使い回す）で、自己検査と凍結した確かめが止まることを確かめる。
  9 | **実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の方向は、実の方向の名だけを借りた乱数（次元は小さな模型のもの）。
 10 | 出力: records/Bl3/dry-run-Bl3-<日付>.md（--force が無ければ上書きしない）
 11 | 用法: python tools/dry_run_Bl3.py [--force] [--iso 本数（既定は正本の本数）]
 12 | 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 13 | """
 14 | import os, sys, json, math, time, copy, argparse, datetime, collections
 15 | import numpy as np
 16 | 
 17 | HERE = os.path.dirname(os.path.abspath(__file__))
 18 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 19 | sys.path.insert(0, HERE)
 20 | import blens_core as C
 21 | import bl3_core as K
 22 | 
 23 | VERSION = 'v1'
 24 | NL = chr(10)
 25 | SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
 26 | T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
 27 | FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
 28 | DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
 29 | RESULTS = []
 30 | 
 31 | 
 32 | def check(group, name, ok, detail=''):
 33 |     RESULTS.append((group, name, bool(ok), detail))
 34 |     print('[dry_run_Bl3] %s %-4s %s %s' % (group, 'OK' if ok else 'FAIL', name, detail), flush=True)
 35 | 
 36 | 
 37 | def raises(fn, exc):
 38 |     try:
 39 |         fn()
 40 |     except exc:
 41 |         return True
 42 |     return False
 43 | 
 44 | 
 45 | # ---------------- 一. 純粋な関数の形 ----------------
 46 | def part_pure():
 47 |     G = '一'
 48 |     rng = np.random.default_rng(11)
 49 |     units = ['A', 'B', 'C', 'D']
 50 |     # 奇でない押し: 逆の符号の升目の効き目を「正の升目の効き目の符号を反転したもの」で代えると、門の答えが変わる
 51 |     fp, fm = 'S1|X|+1', 'S1|X|-1'
 52 |     eff = {u: {fp: float(i), fm: float(i) ** 2 - 2.0} for i, u in enumerate(units)}
 53 |     rows = [{'unit': u, 'cell': 'S1|X', 'fam': fm, 'y': eff[u][fm]} for u in units] + [{'unit': u, 'cell': 'S1|X', 'fam': fp, 'y': eff[u][fp]} for u in units]
 54 |     g_ok = K.gate(rows, eff, units, 0.05)
 55 |     wrong = {u: {fp: eff[u][fp], fm: -eff[u][fp]} for u in units}
 56 |     g_wrong = K.gate(rows, wrong, units, 0.05)
 57 |     check(G, '奇でない押し（逆の符号の升目の効き目をそのまま使う）', g_ok['rho'] > 0.99 and abs(g_wrong['rho'] - g_ok['rho']) > 0.1,
 58 |           '正しい呼び方 ρ %.3f／反転で代えた呼び方 ρ %.3f' % (g_ok['rho'], g_wrong['rho']))
 59 |     # 零でない帰無の中心: 対称の割合では外に出ない反対の側の値が、両側に等しい裾の割合では外に出る
 60 |     null = rng.normal(loc=3.0, scale=0.5, size=1999)
 61 |     pe, ps = K.p_and_tail(-1.0, null)['p'], C.p_two_sided(-1.0, null)
 62 |     pc_ = K.p_and_tail(3.0, null)['p']
 63 |     check(G, '零でない帰無の中心', pe <= 2 / 2000 + 1e-12 and ps > 0.5 and pc_ > 0.5, '反対の側の値: 等しい裾 %.4f・対称 %.4f／中心の値: 等しい裾 %.3f' % (pe, ps, pc_))
 64 |     # 減算の行: 符号を二重に掛けると押しの向きが反転する
 65 |     rows_s = [{'unit': u, 'cell': 'S1|X', 'fam': fm, 'y': 2 * eff[u][fm]} for u in units]
 66 |     ok_ = C.gate_perm([dict(r, sign=1) for r in rows_s], eff, units)
 67 |     dbl = C.gate_perm([dict(r, sign=-1) for r in rows_s], eff, units)
 68 |     check(G, '減算の行（符号の二重掛け）', ok_['rho'] > 0.99 and dbl['rho'] < -0.99, '符号 +1 ρ %.3f／二重掛け ρ %.3f' % (ok_['rho'], dbl['rho']))
 69 |     # 下見で外れる升目と、門の行だけの升目（門の行・入れ替えの数・Holm の段）
 70 |     rows_g = [{'unit': u, 'cell': c, 'fam': c + '|+1', 'y': float(i)} for i, u in enumerate(units) for c in ('S1|X', 'S4|Y')] + [{'unit': 'E', 'cell': 'S4|Y', 'fam': 'S4|Y|+1', 'y': 0.5}]
 71 |     eff_g = {u: {'S1|X|+1': float(i), 'S4|Y|+1': float(i)} for i, u in enumerate(units + ['E'])}
 72 |     g_all = K.gate(rows_g, eff_g, units + ['E'], 0.05)
 73 |     g_drop = K.gate(rows_g, eff_g, units + ['E'], 0.05, drop_cells=['S4|Y'])
 74 |     pv = {'r%d' % i: 0.001 * (i + 1) for i in range(16)}
 75 |     h16 = K.holm(pv, 0.05)
 76 |     pv14 = {k: v for k, v in pv.items() if k not in ('r14', 'r15')}
 77 |     h14 = K.holm(pv14, 0.05)
 78 |     step1_16 = min(v['step'] for v in h16.values())
 79 |     step1_14 = min(v['step'] for v in h14.values())
 80 |     check(G, '下見で外れる升目と門の行だけの升目', g_all['n_perm'] == 120 and g_drop['n_perm'] == 24 and g_drop['n_rows'] == 4 and abs(step1_16 - 0.05 / 16) < 1e-15 and abs(step1_14 - 0.05 / 14) < 1e-15,
 81 |           '入れ替え %d → 外した後 %d（行 %d・行の無くなった単位を外した）・Holm の第一段 %.6f → %.6f' % (g_all['n_perm'], g_drop['n_perm'], g_drop['n_rows'], step1_16, step1_14))
 82 |     # 帰無との同じ値: 両方の裾に数える・二つ目の札は同じ距離を上回らない
 83 |     nl = np.array([0.0, 1.0, 1.0, 2.0, 3.0])
 84 |     t = K.p_and_tail(1.0, nl)
 85 |     comps = np.array([-1.0, 1.0, 2.0])                   # 中心は 1・行 3.0 の距離 2 と、比べる相手 -1.0 の距離 2 が同じ
 86 |     sl = K.second_label(3.0, comps, [(-1.0, 2.0)])
 87 |     check(G, '帰無との同じ値', t['upper'] == 4 and t['lower'] == 3 and not sl['top'], '上の裾 %d・下の裾 %d（同じ値を両方に数える）・同じ距離の比べる相手があれば最上位にしない' % (t['upper'], t['lower']))
 88 |     # 両方の向きがちょうど対称な比べる相手: 中心は零・対の単位の順位は向きの順位の半分の側
 89 |     xs = rng.normal(size=24)
 90 |     co = np.concatenate([xs, -xs])
 91 |     pairs = list(zip(xs, -xs))
 92 |     sl2 = K.second_label(0.5, co, pairs)
 93 |     check(G, '両方の向きがちょうど対称な比べる相手', abs(sl2['center']) < 1e-12 and sl2['rank_oriented'] == 2 * sl2['rank_pair'] - 1,
 94 |           '中心 %.2e・向きの順位 %d・対の順位 %d' % (sl2['center'], sl2['rank_oriented'], sl2['rank_pair']))
 95 |     # 端数のバッチ
 96 |     ids = ['d%d' % i for i in range(2034)]
 97 |     bp = K.batch_plan(ids, 16, T3['readout']['primary']['order_seed'], 0)
 98 |     flat = [x for b in bp for x in b]
 99 |     check(G, '端数のバッチ（零のベクトルで埋める）', len(bp) == 128 and flat.count(K.PAD) == 13 and flat.count(K.NOOP) == 1 and set(flat) - {K.PAD, K.NOOP} == set(ids),
100 |           'バッチ %d・埋める %d・無操作 %d' % (len(bp), flat.count(K.PAD), flat.count(K.NOOP)))
101 |     # 零の近くの中央値
102 |     s0 = K.effect_side(-2.0, rng.normal(loc=0.05, scale=1.0, size=1999))
103 |     check(G, '零の近くの中央値（符号だけ）', s0['side'] == 'sign_only' and s0['sign'] == -1, '四分位 [%.3f, %.3f]' % (s0['q1'], s0['q3']))
104 |     # Holm の境で一本違う p: 札の一致が落ちる
105 |     Kn = T3['nulls']['isotropic']['count']
106 |     lim = K.holm_limits(Kn, 0.05, 16)
107 |     base_null = np.linspace(-1.0, 1.0, Kn)
108 |     m_row = float(base_null[-1 - lim[0]]) + 1e-9          # 上の裾に帰無が lim[0] 本だけ残る値
109 |     pA = K.p_and_tail(m_row, base_null)['p']
110 |     null_B = base_null.copy()
111 |     null_B[-2 - lim[0]] = m_row + 1e-6                    # 帰無一本がこの値を越える
112 |     pB = K.p_and_tail(m_row, null_B)['p']
113 |     others = {'r%d' % i: 0.5 for i in range(1, 16)}
114 |     hA = K.holm(dict(others, r0=pA), 0.05)['r0']['pass']
115 |     hB = K.holm(dict(others, r0=pB), 0.05)['r0']['pass']
116 |     ag = K.agreement({'r0': [0.0]}, {'r0': [0.0]}, 0.001, {'r0': hA}, {'r0': hB})
117 |     check(G, 'Holm の境で一本違う p（札の一致の判定）', hA and not hB and not ag['agree'] and ag['values_within_tol'], 'p %.4f → %.4f・Holm の判定 %s → %s・一致 %s' % (pA, pB, hA, hB, ag['agree']))
118 |     # 器の誤りでやり直す流れ
119 |     q = K.q1_from_attempts([{'tool_error': '出口の値の自己検査が落ちた'}, {'decision': {'q1': '一部の升目を外して続ける'}}])
120 |     q2 = K.q1_from_attempts([{'decision': {'q1': '止める'}}, {'decision': {'q1': '続ける'}}])
121 |     q3 = K.q1_from_attempts([{'tool_error': 'x'}])
122 |     check(G, '器の誤りでやり直す流れ（q1 の採点）', q['scored'] and q['q1'] == '一部の升目を外して続ける' and q2['first_decision'] == '止める' and not q3['scored'],
123 |           'やり直した下見で採点・一度目の決定を併記・やり直さなければ採点しない')
124 |     # 掃き出し: 札と門と向きの足し分に要る升目・符号・方向の組が、本の計算の組み立てにそろう
125 |     import bl3_run as BR
126 |     names_real = ['real:' + p for p in DJ['groups']['real']['names']]
127 |     iso_ids = ['iso:%d' % i for i in range(T3['nulls']['isotropic']['count'])]
128 |     b3 = ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
129 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
130 |     sets = BR.cell_sign_sets(T3, None, T3['directions']['named'], b3, iso_ids, names_real, gate_only)
131 |     have = {(k, d) for k, cell, sg, ds in sets for d in ds}
132 |     need, miss = set(), []
133 |     for r in T3['main_rows']:
134 |         k = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
135 |         kk = '%s|%s|%+d' % (r['scenario'], r['base'], -r['sign'])
136 |         need.add((k, r['direction']))
137 |         need |= {(k, i) for i in iso_ids}
138 |         comps = K.comparators_for(r['direction'], DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'])
139 |         need |= {(k, 'real:' + p) for p in comps} | {(kk, 'real:' + p) for p in comps}
140 |     fams = sorted({'%s|%s|%+d' % (g['scenario'], g['base'], g['sign']) for g in FJ['facts']['C']['gate_rows']})
141 |     unit_ids = list(T3['directions']['named']) + b3
142 |     need |= {(f, u) for f in fams for u in unit_ids}
143 |     miss = sorted(need - have)
144 |     check(G, '掃き出し（要る組が本の計算の組み立てにそろう）', not miss, '要る組 %d・組み立て %d・足りない %d%s' % (len(need), len(have), len(miss), ('（例 %s）' % miss[:3]) if miss else ''))
145 |     n_passes = sum(len(ds) for _, _, _, ds in sets)
146 |     E = FJ['facts']['E']
147 |     check(G, '本の計算の順伝播の数（転記行 E と）', n_passes == E['passes_main'] + E['passes_gate_extra'] + E['passes_orient_extra'],
148 |           '組み立て %d・転記行 E %d ＋ %d ＋ %d' % (n_passes, E['passes_main'], E['passes_gate_extra'], E['passes_orient_extra']))
149 |     return sets
150 | 
151 | 
152 | # ---------------- 二・三. 乱数の小さな模型 ----------------
153 | def tiny_model(seed=0, layers=4):
154 |     import torch
155 |     from transformers import AutoConfig, AutoModelForCausalLM
156 |     cfg = AutoConfig.from_pretrained(SNAP)
157 |     cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim, cfg.intermediate_size = 64, layers, 4, 2, 16, 128
158 |     if getattr(cfg, 'layer_types', None):
159 |         cfg.layer_types = list(cfg.layer_types)[:layers]
160 |     torch.manual_seed(seed)
161 |     model = AutoModelForCausalLM.from_config(cfg)
162 |     with torch.no_grad():
163 |         g = torch.Generator().manual_seed(seed + 1)
164 |         for n, p in model.named_parameters():
165 |             if n.endswith('norm.weight'):                 # 乱数の初期値は一なので、二重の正規化が見えない——散らす
166 |                 p.copy_(torch.rand(p.shape, generator=g) + 0.5)
167 |     return model.to(torch.bfloat16).eval(), cfg
168 | 
169 | 
170 | def calibrate_readout_rows(model, R0, cell, FJ, seed=7):
171 |     """乱数の模型の出口の行列を、読み取りの集合の文字が強く出るように置く（正本の閾値は変えずに、下見を本の計算まで通すため・合成だけ）。
172 |     読み取りの集合の文字の行を、升目 cell の無操作の最終の正規化の出口の向きの三倍に小さな乱数を足したものにする。起動器の DRY も同じ関数を呼ぶ。"""
173 |     import torch
174 |     cap = {}
175 |     hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
176 |     with torch.no_grad():
177 |         model(input_ids=torch.tensor([cell.ids]), logits_to_keep=1)
178 |     hh.remove()
179 |     m_ = R0.norm32(cap['h'])[0]
180 |     m_ = m_ / m_.norm()
181 |     set_all = sorted({int(x) for x in FJ['facts']['A']['letter_ids'].values()})
182 |     gcal = torch.Generator().manual_seed(seed)
183 |     with torch.no_grad():
184 |         for tkn in set_all:
185 |             model.lm_head.weight[tkn] = (3.0 * m_ + 0.3 * torch.randn(m_.shape, generator=gcal)).to(model.lm_head.weight.dtype)
186 |     return set_all
187 | 
188 | 
189 | def synth_dirs(dim, names, seed=5):
190 |     rng = np.random.default_rng(seed)
191 |     v = rng.normal(size=dim)
192 |     nv = float(np.linalg.norm(v))
193 |     out = collections.OrderedDict()
194 |     for n in names:
195 |         x = v if n == 'static' else rng.normal(size=dim)
196 |         out[n] = x * (nv / float(np.linalg.norm(x)))
197 |     out['zero:test'] = np.zeros(dim)
198 |     return out
199 | 
200 | 
201 | def part_model(sets, iso_n):
202 |     import torch
203 |     import bl3_run as BR
204 |     import run_stageB_local as RB
205 |     import direction_B
206 |     from transformers import AutoTokenizer
207 |     G2, G3 = '二', '三'
208 |     t0 = time.time()
209 |     tok = AutoTokenizer.from_pretrained(SNAP)
210 |     model, cfg = tiny_model()
211 |     L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
212 |     names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])] + ['iso:%d' % i for i in range(iso_n)] + \
213 |         ['real:' + p for p in DJ['groups']['real']['names']] + ['check']
214 |     dirs = synth_dirs(cfg.hidden_size, names)
215 |     cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
216 |     gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
217 |     cells = BR.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
218 |     # 乱数の模型の出口の行列を、読み取りの集合の文字が強く出るように置く（正本の閾値は変えずに、下見を本の計算まで通すため・合成だけ）
219 |     R0 = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs)
220 |     calibrate_readout_rows(model, R0, cells[cell_keys[0]], FJ)
221 |     R = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs)
222 |     check(G2, '升目の入力が転記行 B と一致する（実のトークナイザ）', True, '%d 升目' % len(cells))
223 |     # 書き出しの割り方が変わる場合（器が止まるか）
224 |     FJx = copy.deepcopy(FJ)
225 |     FJx['facts']['A']['prefix_ids'] = FJ['facts']['A']['prefix_ids'][:-1]
226 |     check(G2, '書き出しの割り方が変わる場合（器が止まる）', raises(lambda: BR.build_cells(tok, T3, FJx, cell_keys[:1]), BR.ToolError), '書き出しを一トークン欠いた入力で、転記行 B との突き合わせが止めた')
227 |     # 下見（正本の値のまま・乱数の模型）
228 |     stage_b_rate = {k: FJ['facts']['B']['cells'][k]['catastrophe'] / FJ['facts']['B']['cells'][k]['n_ok'] for k in cell_keys}
229 |     variants = {k: v['ids'] for k, v in FJ['facts']['A']['variants'].items()}
230 |     pilot = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
231 |     dec = pilot['decision']
232 |     check(G2, '下見が機械の決定まで走る', 'q1' in dec and 'vi' in pilot and ('batch' in pilot or dec.get('stop')),
233 |           'q1 %s・(vi) (a) %.2e (b) %.2e・バッチ %s・揺れの床 %s・近道の許容 %s・近道 %s' % (dec.get('q1'), pilot['vi']['decision']['spread_a'], pilot['vi']['decision']['spread_b'],
234 |                                                             pilot.get('batch'), pilot.get('floor'), pilot.get('cache_tol'), (pilot.get('v') or {}).get('shortcut')))
235 |     check(G2, '出口の値の自己検査（下見の頭）', pilot['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (pilot['logit_check']['max_abs'], pilot['logit_check']['tol']))
236 |     if dec.get('stop'):
237 |         return {'pilot': pilot, 'n_forward': R.n_forward, 'seconds': round(time.time() - t0, 1), 'iso_n': iso_n, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}
238 |     batch, tol, floor = pilot['batch'], pilot['cache_tol'], pilot['floor']
239 |     use_short = pilot['v']['shortcut']
240 |     # 本の計算（起動器が呼ぶ `run_main_phase` をそのまま通す: 頭の自己検査〔出口の値・最後の層〕と近道の確かめ → 全ての升目と符号）
241 |     items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in T3['cell_signs_main']]
242 |     names_ = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])],
243 |               'iso': ['iso:%d' % i for i in range(T3['nulls']['isotropic']['count'])], 'real': ['real:' + p for p in DJ['groups']['real']['names']]}
244 |     MP = BR.run_main_phase(R, T3, FJ, cells, names_, pilot, iso_n=iso_n, log=lambda s: None)
245 |     hd = MP['head']
246 |     check(G2, '本の計算の頭の出口の値の自己検査', hd['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (hd['logit_check']['max_abs'], hd['logit_check']['tol']))
247 |     sc_chk = hd.get('steered_cache_check') or {}
248 |     check(G2, '本の計算の頭の近道の確かめ（効き目で比べる）', use_short and sc_chk.get('shortcut') and MP['shortcut'], '差の最大 %.2e（許容 %.4f）' % (sc_chk.get('max_abs', float('nan')), tol))
249 |     lc = hd['layer_check']
250 |     check(G2, '最後の層の自己検査', lc['pass'], '差 %.2e（許容 %s）' % (lc['diff'], lc['tol']))
251 |     outs = MP['cells']
252 |     want = {key: {d for d in ds if not d.startswith('iso:') or int(d.split(':')[1]) < iso_n} | {K.NOOP} for key, ck, sg, ds in sets}
253 |     ok_keys = list(outs) == [s[0] for s in sets] and all(set(o['lo']) == want[k] for k, o in outs.items())
254 |     check(G2, '本の計算: 全ての升目と符号・全ての方向と無操作がそろい、埋めた零のベクトルの値は使わない', ok_keys, '升目と符号 %d（組み立て %d）' % (len(outs), len(sets)))
255 |     # 零のベクトルの行（同じ升目と符号をもう一度・零のベクトルを一本足して・近道の使い方は本の計算と同じ）
256 |     kz = [i for i, s in enumerate(sets) if s[0] == 'S1|O-Ncold|-1'][0]
257 |     key_z, ck_z, sg_z, ds_z = sets[kz]
258 |     ds_z = [d for d in ds_z if d in want[key_z]] + ['zero:test']
259 |     oz = BR.run_cell_sign(R, cells[ck_z], sg_z, ds_z, batch, T3['readout']['primary']['order_seed'], kz, pc=R.prefix_cache(cells[ck_z]) if MP['shortcut'] else None)
260 |     zt = oz['effects']['zero:test']
261 |     dmx = max(abs(oz['effects'][d] - outs[key_z]['effects'][d]) for d in outs[key_z]['effects'])
262 |     check(G2, '零のベクトルの行は無操作と同じ値になる（別のバッチでも）', abs(zt) <= max(floor, 1e-6), '効き目 %.2e（揺れの床 %.2e）・バッチの組を変えた同じ方向の効き目の差の最大 %.2e（記述）' % (zt, floor, dmx))
263 |     # バッチの中の位置で方向を取り違えない
264 |     c0, sg0 = items[0]
265 |     r1 = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, full=False)
266 |     r2 = R.forward(c0, ['td', 'Nk', K.NOOP, 'static'], sg0, full=False)
267 |     e1 = {d: float(r1['lo'][i] - r1['lo'][0]) for i, d in enumerate([K.NOOP, 'static', 'Nk', 'td'])}
268 |     e2 = {d: float(r2['lo'][i] - r2['lo'][2]) for i, d in enumerate(['td', 'Nk', K.NOOP, 'static'])}
269 |     dpos = max(abs(e1[d] - e2[d]) for d in ('static', 'Nk', 'td'))
270 |     check(G2, 'バッチの中の位置で方向を取り違えない', dpos <= max(floor, 1e-6) and max(abs(e1[d]) for d in ('static', 'Nk', 'td')) > 1e-3, '位置を入れ替えた効き目の差の最大 %.2e' % dpos)
271 |     # 近道ありと近道なし（効き目・同じバッチの大きさ）
272 |     pc0 = R.prefix_cache(c0)
273 |     rs = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, pc=pc0, full=False)
274 |     ds_ = max(abs(float((rs['lo'][i] - rs['lo'][0]) - (r1['lo'][i] - r1['lo'][0]))) for i in (1, 2, 3))
275 |     check(G2, '近道ありと近道なしの効き目が許容の内で合う', ds_ <= tol, '差の最大 %.2e（許容 %.4f）' % (ds_, tol))
276 |     # 層ごとの差分の記述
277 |     main_keys = {'%s|%s|%+d' % (a_, b_, s_) for a_, b_, s_ in T3['cell_signs_main']}
278 |     lay_ok = all((o['layers']['iso_summary'] is not None and o['layers']['iso_summary']['n'] == iso_n and len(o['layers']['rows']) == 7 and
279 |                   all(len(v) == len(R.after) for v in o['layers']['rows'].values())) if k in main_keys else
280 |                  (o['layers']['iso_summary'] is None and not o['layers']['rows']) for k, o in outs.items())
281 |     summ = outs['S1|O-Ncold|-1']['layers']['iso_summary']
282 |     check(G2, '層ごとの差分（主の組だけ・名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間だけ）', lay_ok,
283 |           '層 %d・等方 %d 本・主の組の升目と符号 %d' % (len(R.after), summ['n'] if summ else 0, sum(1 for k in outs if k in main_keys)))
284 |     # 独立の再計算のフックの道（近道なし・バッチ一）と本の道（二段目の一致）
285 |     st_rows = [r for r in T3['main_rows'] if r['direction'] == 'static']
286 |     v_rows = [[r for r in st_rows if r['sign'] < 0][0], [r for r in st_rows if r['sign'] > 0][0]]      # 減算の行と加算の行を一つずつ
287 |     rows_all, dirs_all = K.recompute_set(T3['main_rows'], DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'], iso_n, dec.get('dropped', []))
288 |     comps = K.comparators_for('static', DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'])
289 |     hand = {r['id']: [('static', r['sign'])] + [('iso:%d' % i, r['sign']) for i in range(iso_n)] + [('real:' + p, r['sign']) for p in comps] + [('real:' + p, -r['sign']) for p in comps]
290 |             for r in T3['main_rows'] if r['direction'] == 'static' and '%s|%s' % (r['scenario'], r['base']) not in set(dec.get('dropped', []))}
291 |     n_pass_rc = sum(1 + len(v) for v in dirs_all.values())
292 |     E_ = FJ['facts']['E']
293 |     Kn_ = T3['nulls']['isotropic']['count']
294 |     per_ok = all(1 + len(v) == E_['per_row_recompute'] - (Kn_ - iso_n) for v in dirs_all.values())
295 |     rows_ok = dec.get('dropped') or 2 * len(rows_all) * E_['per_row_recompute'] == E_['passes_recompute']
296 |     check(G2, '独立の再計算の組（v̂ の行ごとに無操作・v̂・等方の帰無・比べる相手の両方の向き・転記行 E と）', [x[0] for x in rows_all] == list(hand) and dict(dirs_all) == hand and per_ok and rows_ok,
297 |           'v̂ の行 %d・行ごとの順伝播 %d（等方 %d 本のとき・転記行 E の行ごと %d は等方 %d 本）・一つの道の順伝播 %d' % (
298 |               len(rows_all), 1 + len(next(iter(dirs_all.values()))), iso_n, E_['per_row_recompute'], Kn_, n_pass_rc))
299 |     rows_rc = [(nm, cells[ck], s) for nm, ck, s in rows_all if nm in {r['id'] for r in v_rows}]
300 |     hk = BR.recompute_hook_path(R, rows_rc, dirs_all)
301 |     worst = 0.0
302 |     for r in v_rows:
303 |         key = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
304 |         kk = '%s|%s|%+d' % (r['scenario'], r['base'], -r['sign'])
305 |         for dk, e in hk[r['id']]['effects'].items():
306 |             did, sg = dk.rsplit('|', 1)[0], int(dk.rsplit('|', 1)[1])
307 |             m = outs[key if sg == r['sign'] else kk]['effects'][did]
308 |             worst = max(worst, abs(m - e))
309 |     check(G2, '二段目（本の道とフック・近道なし・バッチ一）の効き目の差が「近道の許容＋揺れの床」の内', worst <= tol + floor, '差の最大 %.2e（許容 %.4f）' % (worst, tol + floor))
310 |     ag_bad = K.agreement({'x': [0.0]}, {'x': [tol + floor + 0.01]}, tol + floor, {}, {})
311 |     # 集計の器を端から端まで（等方の本数だけ合成の本数にした正本の写しで・合成だけ）
312 |     import analyze_Bl3 as AZ
313 |     T3d = copy.deepcopy(T3)
314 |     T3d['nulls']['isotropic']['count'] = iso_n
315 |     AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
316 |     rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
317 |     fc = FJ['facts']['C']
318 |     same_rows = sorted(r['name'] for r in rows_gate) == sorted(fc['style_share_pt'])
319 |     style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
320 |     check(G2, '門の行と様式の転位の行を段階 B の記録から作り直す（転記行 C と）', same_rows and len(rows_gate) == T3['gate']['rows_gate'] and sorted(style_rows) == sorted(fc['style_rows']),
321 |           '門の行 %d・様式の転位の行 %d' % (len(rows_gate), len(style_rows)))
322 |     v_hook = {r['id']: hk[r['id']] for r in v_rows}
323 |     AZr = AZ.analyze(T3d, FJ, outs, [pilot], DJ['groups']['real']['names'], rows_gate, hook=v_hook, rewrite=None, style_rows=style_rows, rows_subset=set(v_hook))
324 |     AZfull = AZ.recompute_agreement(T3d, T3['main_rows'], {k: o['effects'] for k, o in outs.items()}, DJ['groups']['real']['names'], v_hook, None, pilot)
325 |     check(G2, '独立の再計算の行が欠ければ一致しない（本の計算の求め方）', not AZfull['second']['agree'] and AZfull['second'].get('reason') == 'keys', '欠けた行 %d' % len(AZfull['second'].get('missing', [])))
326 |     gate_keys = ('main', 'without_vhat', 'desc_without_vhat_loaded', 'desc_choice_a', 'desc_without_style')
327 |     ok_az = len(AZr['rows']) == len(T3['main_rows']) and all(k in AZr['gates'] for k in gate_keys) and list(AZr['predictions_truth']) == [it['key'] for it in T3['predictions']['items']]
328 |     check(G2, '集計の器が主の札・門・記述の門・予想の答えを出す', ok_az,
329 |           '行 %d・本の門の入れ替え %s・v̂ を抜いた門 %s・予想の答え %s' % (len(AZr['rows']), AZr['gates']['main'].get('n_perm'), AZr['gates']['without_vhat'].get('n_perm'), dict(AZr['predictions_truth'])))
330 |     check(G2, '集計の器の二段目の一致（合成・一段目は独立の再計算の器ができた後）', AZr['recompute']['second']['agree'] and AZr['recompute']['first'] is None and not AZr['recompute']['agree'],
331 |           '二段目 %s（差の最大 %.2e・許容 %.4f）・一段目 まだ無い・全体の一致 %s' % (AZr['recompute']['second']['agree'], AZr['recompute']['second']['max_abs_diff'], AZr['recompute']['tol_second'], AZr['recompute']['agree']))
332 |     check(G2, '二段目の許容を超える揺れを入れると一致しない', not ag_bad['agree'], '入れた差 %.4f' % (tol + floor + 0.01))
333 |     # 乙（裁定 D227）: B-lens の層二の文脈で、門の行の符号で流す
334 |     FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
335 |     CB = json.load(open(os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json'), encoding='utf-8'))['magnitude']['letter']
336 |     sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
337 |     same_rows = all(sorted(n for n, _, _ in sec_rows.get(cell, [])) == sorted(CB[cell]['rows']) for cell in CB)
338 |     check(G2, '乙の行が B-lens の層二の答えの文字の位置の行と同じ（裁定 D227）', same_rows and set(sec_rows) == set(CB), '升目 %d・行 %d' % (len(sec_rows), sum(len(v) for v in sec_rows.values())))
339 |     ctx_all = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
340 |     pick = [c for c in ctx_all if c[0] == 'S1|O-Ncold|prose'][:1] + [c for c in ctx_all if c[0] == 'S4|Osec-Ncold|json'][:1]
341 |     sec = BR.run_secondary(R, pick, sec_rows)
342 |     ok_sec = len(ctx_all) == sum(len(v) for v in FB['facts']['E']['selected'].values()) and all(set(s['rows']) == {n for n, _, _ in sec_rows[pick[i][2].key]} for i, s in enumerate(sec)) and \
343 |         sec[0]['n_batches'] == len({sg for _, _, sg in sec_rows[pick[0][2].key]})
344 |     cnt = AZ.secondary_counts(FB, sec_rows)
345 |     check(G2, '乙を流せる（文脈を組み・行の符号ごとに無操作と同じバッチ）', ok_sec, '文脈 %d（流したのは %d）・乙の行の順伝播 %d・符号のバッチ %d' % (len(ctx_all), len(pick), cnt['row_passes'], cnt['sign_batches']))
346 |     E2 = FJ['facts']['E']
347 |     check(G2, '乙の順伝播の数が転記行 E と同じ（集計の器の数え方と、設計事実の器の転記行 C の門の行からの数え方）',
348 |           (cnt['row_passes'], cnt['sign_batches'], cnt['contexts']) == (E2['passes_secondary'], E2['batches_secondary'], E2['contexts_secondary']),
349 |           '集計の器 %d・%d・%d／転記行 E %d・%d・%d' % (cnt['row_passes'], cnt['sign_batches'], cnt['contexts'], E2['passes_secondary'], E2['batches_secondary'], E2['contexts_secondary']))
350 |     summ2 = AZ.secondary_summary(sec, CB)
351 |     check(G2, '乙のまとめに B-lens の直接の経路の値を並べる', all(v.get('blens_direct') is not None for v in summ2.values()), '行 %d' % len(summ2))
352 |     # 三. 壊した読み取りと近道
353 |     Rd = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs, bug='double_norm')
354 |     ld = Rd.logit_check(c0, T3['computation']['logit_tol'])
355 |     check(G3, '二重の正規化の読み取りを、出口の値の自己検査が止める', not ld['pass'], '差の最大 %.3f（許容 %s）' % (ld['max_abs'], ld['tol']))
356 |     first = None
357 |     try:
358 |         BR.run_pilot(Rd, [cells[k] for k in cell_keys[:1]], [], T3, {}, stage_b_rate, T3['inputs']['sampling_B'])
359 |     except BR.ToolError as e_:
360 |         first = {'tool_error': str(e_)}
361 |     check(G3, '壊した読み取りで下見が器の誤りとして止まる（やり直しの流れの一度目）', first is not None, (first or {}).get('tool_error', '')[:60])
362 |     Rb = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs, bug='cache_through_mp')
363 |     check(G3, '主位置まで使い回す近道を、凍結した確かめ（assert）が止める', raises(lambda: Rb.forward(c0, [K.NOOP, 'static'], sg0, pc=Rb.prefix_cache(c0), full=False), BR.ToolError), '近道の元が主位置の手前で切れていない')
364 |     # 効き目で比べる確かめだけでは弱いこと（主位置の一つ分の加減の寄与の大きさ・記述）
365 |     V = np.stack([np.zeros(cfg.hidden_size, dtype=np.float32), dirs['static'].astype(np.float32)])
366 |     vals = []
367 |     for st in (c0.mp, c0.mp + 1):
368 |         h_ = RB.register_hook(model, L, RB.make_hook(V, T3['layers']['coef_applied'], sg0, [st, st]))
369 |         cap = {}
370 |         hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
371 |         with torch.no_grad():
372 |             model(input_ids=torch.tensor([c0.ids] * 2), logits_to_keep=1)
373 |         h_.remove(); hh.remove()
374 |         ro = R.readout(cap['h'], c0, full=False)
375 |         vals.append(float(ro['lo'][1] - ro['lo'][0]))
376 |     check(G3, '（記述）主位置の一つ分の加減の寄与（効き目で比べる確かめの強さの目安）', True, '主位置から %.4f・主位置の次から %.4f・差 %.2e（近道の許容 %.4f）' % (vals[0], vals[1], vals[0] - vals[1], tol))
377 |     # （記述）本物の相対の加減の大きさに合わせた合成の方向で、突き合わせの力を測り直す（独立の再計算の個体の開発の記録の勧め）。
378 |     # 小さな模型では合成の方向のノルムが選んだ層の出力より二桁ほど大きく、効き目が飽和して、係数の二度掛けなどの誤りが一段目の許容の内に収まった。
379 |     # 方向を ‖v‖＝正本 `layers.vhat_over_h` の選んだ層の値 × 選んだ層の出力の主位置のノルム にそろえ、個体の器の変種（`bl3_recompute_rewrite._mutant_diffs`・中は変えない）と
380 |     # 主位置の一つ分の加減の寄与を測る。判定に入れない（合成の模型の上の目安）。
381 |     import bl3_recompute_rewrite as RW
382 |     rw_rows = [(r['id'], '%s|%s' % (r['scenario'], r['base']), int(r['sign'])) for r in v_rows]
383 |     capL = {}
384 |     hL = direction_B.decoder_layers(model)[L].register_forward_hook(lambda m, i, o: capL.__setitem__('h', (o[0] if isinstance(o, tuple) else o).detach().clone()))
385 |     with torch.no_grad():
386 |         model(input_ids=torch.tensor([cells[rw_rows[0][1]].ids]), logits_to_keep=1)
387 |     hL.remove()
388 |     RB.assert_no_hooks(model, L)
389 |     nh = float(capL['h'][0, cells[rw_rows[0][1]].mp].float().norm())
390 |     ratio = float(T3['layers']['vhat_over_h'][str(T3['layers']['selected_ratio'])])
391 |     first_real = 'real:' + DJ['groups']['real']['names'][0]
392 |     scale = ratio * nh / float(np.linalg.norm(dirs['static']))
393 |     dirs_s = collections.OrderedDict((k, v * scale) for k, v in dirs.items() if k in ('static', 'iso:0', 'iso:1', first_real))
394 |     Rs = BR.Runner(model, T3, L, T3['layers']['coef_applied'], dirs_s)
395 |     dbr_s = {nm: [('static', s), ('iso:0', s), ('iso:1', s), (first_real, 1), (first_real, -1)] for nm, _, s in rw_rows}
396 |     hk_s = BR.recompute_hook_path(Rs, [(nm, cells[ck], s) for nm, ck, s in rw_rows], dbr_s)
397 |     M_s = RW._mutant_diffs(model, tok, T3, FJ, rw_rows, dirs_s, first_real, L, T3['layers']['coef_applied'], hk_s)
398 |     emax = max(abs(e) for v in hk_s.values() for e in v['effects'].values())
399 |     tol1 = T3['independent_recompute']['tol_stage1']
400 |     check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、書き換えの道の変種とフックの道の差（一段目の許容と比べる・判定に入れない）', True,
401 |           '‖v‖／‖選んだ層の出力‖ %.4f・効き目の絶対値の最大 %.2e・%s（許容 %s）' % (ratio, emax, '・'.join('%s %.2e%s' % (k, d, '（許容の外）' if d > tol1 else '') for k, _, d, _ in M_s), tol1))
402 |     V2 = np.stack([np.zeros(cfg.hidden_size, dtype=np.float32), dirs_s['static'].astype(np.float32)])
403 |     vals_s = []
404 |     for st in (c0.mp, c0.mp + 1):
405 |         h_ = RB.register_hook(model, L, RB.make_hook(V2, T3['layers']['coef_applied'], sg0, [st, st]))
406 |         cap = {}
407 |         hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
408 |         with torch.no_grad():
409 |             model(input_ids=torch.tensor([c0.ids] * 2), logits_to_keep=1)
410 |         h_.remove(); hh.remove()
411 |         ro = R.readout(cap['h'], c0, full=False)
412 |         vals_s.append(float(ro['lo'][1] - ro['lo'][0]))
413 |     check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、主位置の一つ分の加減の寄与（判定に入れない）', True,
414 |           '主位置から %.3e・主位置の次から %.3e・差 %.2e（近道の許容 %.4f・一段目の許容 %s）' % (vals_s[0], vals_s[1], vals_s[0] - vals_s[1], tol, tol1))
415 |     return {'pilot': pilot, 'n_forward': R.n_forward, 'seconds': round(time.time() - t0, 1), 'iso_n': iso_n, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}
416 | 
417 | 
418 | def main():
419 |     ap = argparse.ArgumentParser()
420 |     ap.add_argument('--force', action='store_true')
421 |     ap.add_argument('--iso', type=int, default=T3['nulls']['isotropic']['count'])
422 |     ap.add_argument('--out', default=None, help='試しの走りの出力の置き場（既定は records/Bl3/dry-run-Bl3-<日付>.md）')
423 |     a = ap.parse_args()
424 |     day = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
425 |     out = a.out or os.path.join(REPO, 'records', 'Bl3', 'dry-run-Bl3-%s.md' % day)
426 |     if os.path.exists(out) and not a.force:
427 |         raise SystemExit('既にある: %s' % out)
428 |     t0 = time.time()
429 |     sets = part_pure()
430 |     info = part_model(sets, a.iso)
431 |     n_ok = sum(1 for r in RESULTS if r[2])
432 |     L_ = ['# B-lens 層三の合成データの確かめ（機械生成・`tools/dry_run_Bl3.py` %s・%s）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')), '',
433 |           '- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 %s・次元 %s・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。' % (
434 |               info.get('layers'), info.get('dim')),
435 |           '- 等方の方向の本数: %d（正本 %d）。順伝播 %s 回・%s 秒。' % (a.iso, T3['nulls']['isotropic']['count'], info.get('n_forward'), info.get('seconds')),
436 |           '- 確かめ: %d のうち %d が期待どおり。' % (len(RESULTS), n_ok), '',
437 |           '| 部 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|'] + [
438 |           '| %s | %s | %s | %s |' % (g, n, '期待どおり' if ok else '**期待と違う**', d.replace('|', '｜')) for g, n, ok, d in RESULTS] + [
439 |           '', '## 下見の記録（乱数の模型・値に意味は無い・経路の確かめ）', '', '```json', json.dumps({k: v for k, v in info['pilot'].items() if k in ('logit_check', 'vi', 'batch', 'floor', 'cache_tol', 'iii', 'v', 'decision')}, ensure_ascii=False, indent=1, default=float), '```', '',
440 |           '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
441 |     open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(L_))
442 |     print('[dry_run_Bl3] wrote %s | %d/%d | %.0f s' % (os.path.relpath(out, REPO), n_ok, len(RESULTS), time.time() - t0))
443 |     sys.exit(0 if n_ok == len(RESULTS) else 1)
444 | 
445 | 
446 | if __name__ == '__main__':
447 |     main()
```
<<< 終: `tools/dry_run_Bl3.py` >>>

<<< 始: `records/Bl3/tools/trials/dry-trial-6-Bl3.md`（SHA16 3CCBB0761FF0C9F4） >>>
# B-lens 層三の合成データの確かめ（機械生成・`tools/dry_run_Bl3.py` v1・2026-09-24 23:01 UTC）

- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 4・次元 64・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。
- 等方の方向の本数: 49（正本 1999）。順伝播 432 回・426.2 秒。
- 確かめ: 41 のうち 41 が期待どおり。

| 部 | 確かめ | 結果 | 詳しく |
|---|---|---|---|
| 一 | 奇でない押し（逆の符号の升目の効き目をそのまま使う） | 期待どおり | 正しい呼び方 ρ 1.000／反転で代えた呼び方 ρ -0.012 |
| 一 | 零でない帰無の中心 | 期待どおり | 反対の側の値: 等しい裾 0.0010・対称 1.0000／中心の値: 等しい裾 0.984 |
| 一 | 減算の行（符号の二重掛け） | 期待どおり | 符号 +1 ρ 1.000／二重掛け ρ -1.000 |
| 一 | 下見で外れる升目と門の行だけの升目 | 期待どおり | 入れ替え 120 → 外した後 24（行 4・行の無くなった単位を外した）・Holm の第一段 0.003125 → 0.003571 |
| 一 | 帰無との同じ値 | 期待どおり | 上の裾 4・下の裾 3（同じ値を両方に数える）・同じ距離の比べる相手があれば最上位にしない |
| 一 | 両方の向きがちょうど対称な比べる相手 | 期待どおり | 中心 0.00e+00・向きの順位 31・対の順位 16 |
| 一 | 端数のバッチ（零のベクトルで埋める） | 期待どおり | バッチ 128・埋める 13・無操作 1 |
| 一 | 零の近くの中央値（符号だけ） | 期待どおり | 四分位 [-0.582, 0.724] |
| 一 | Holm の境で一本違う p（札の一致の判定） | 期待どおり | p 0.0030 → 0.0040・Holm の判定 True → False・一致 False |
| 一 | 器の誤りでやり直す流れ（q1 の採点） | 期待どおり | やり直した下見で採点・一度目の決定を併記・やり直さなければ採点しない |
| 一 | 掃き出し（要る組が本の計算の組み立てにそろう） | 期待どおり | 要る組 24527・組み立て 24527・足りない 0 |
| 一 | 本の計算の順伝播の数（転記行 E と） | 期待どおり | 組み立て 24527・転記行 E 24408 ＋ 7 ＋ 112 |
| 二 | 升目の入力が転記行 B と一致する（実のトークナイザ） | 期待どおり | 9 升目 |
| 二 | 書き出しの割り方が変わる場合（器が止まる） | 期待どおり | 書き出しを一トークン欠いた入力で、転記行 B との突き合わせが止めた |
| 二 | 下見が機械の決定まで走る | 期待どおり | q1 続ける・(vi) (a) 4.81e-06 (b) 0.00e+00・バッチ 16・揺れの床 4.811094168388763e-06・近道の許容 0.005・近道 True |
| 二 | 出口の値の自己検査（下見の頭） | 期待どおり | 差の最大 7.70e-02（許容 0.5） |
| 二 | 本の計算の頭の出口の値の自己検査 | 期待どおり | 差の最大 7.70e-02（許容 0.5） |
| 二 | 本の計算の頭の近道の確かめ（効き目で比べる） | 期待どおり | 差の最大 3.77e-03（許容 0.0050） |
| 二 | 最後の層の自己検査 | 期待どおり | 差 0.00e+00（許容 0.0001） |
| 二 | 本の計算: 全ての升目と符号・全ての方向と無操作がそろい、埋めた零のベクトルの値は使わない | 期待どおり | 升目と符号 17（組み立て 17） |
| 二 | 零のベクトルの行は無操作と同じ値になる（別のバッチでも） | 期待どおり | 効き目 0.00e+00（揺れの床 4.81e-06）・バッチの組を変えた同じ方向の効き目の差の最大 0.00e+00（記述） |
| 二 | バッチの中の位置で方向を取り違えない | 期待どおり | 位置を入れ替えた効き目の差の最大 9.47e-07 |
| 二 | 近道ありと近道なしの効き目が許容の内で合う | 期待どおり | 差の最大 0.00e+00（許容 0.0050） |
| 二 | 層ごとの差分（主の組だけ・名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間だけ） | 期待どおり | 層 2・等方 49 本・主の組の升目と符号 12 |
| 二 | 独立の再計算の組（v̂ の行ごとに無操作・v̂・等方の帰無・比べる相手の両方の向き・転記行 E と） | 期待どおり | v̂ の行 8・行ごとの順伝播 99（等方 49 本のとき・転記行 E の行ごと 2049 は等方 1999 本）・一つの道の順伝播 792 |
| 二 | 二段目（本の道とフック・近道なし・バッチ一）の効き目の差が「近道の許容＋揺れの床」の内 | 期待どおり | 差の最大 4.32e-03（許容 0.0050） |
| 二 | 門の行と様式の転位の行を段階 B の記録から作り直す（転記行 C と） | 期待どおり | 門の行 64・様式の転位の行 2 |
| 二 | 独立の再計算の行が欠ければ一致しない（本の計算の求め方） | 期待どおり | 欠けた行 6 |
| 二 | 集計の器が主の札・門・記述の門・予想の答えを出す | 期待どおり | 行 16・本の門の入れ替え 5040・v̂ を抜いた門 720・予想の答え {'q1.pilot': '続ける', 'q2.vhat_iso': '零', 'q3.nk_iso': '零', 'q4.gate': '通らない', 'q5.gate_wo_vhat': '通らない', 'q6.second': '零', 'q7.direction': None} |
| 二 | 集計の器の二段目の一致（合成・一段目は独立の再計算の器ができた後） | 期待どおり | 二段目 True（差の最大 4.32e-03・許容 0.0050）・一段目 まだ無い・全体の一致 False |
| 二 | 二段目の許容を超える揺れを入れると一致しない | 期待どおり | 入れた差 0.0150 |
| 二 | 乙の行が B-lens の層二の答えの文字の位置の行と同じ（裁定 D227） | 期待どおり | 升目 9・行 64 |
| 二 | 乙を流せる（文脈を組み・行の符号ごとに無操作と同じバッチ） | 期待どおり | 文脈 180（流したのは 2）・乙の行の順伝播 1280・符号のバッチ 260 |
| 二 | 乙の順伝播の数が転記行 E と同じ（集計の器の数え方と、設計事実の器の転記行 C の門の行からの数え方） | 期待どおり | 集計の器 1280・260・180／転記行 E 1280・260・180 |
| 二 | 乙のまとめに B-lens の直接の経路の値を並べる | 期待どおり | 行 13 |
| 三 | 二重の正規化の読み取りを、出口の値の自己検査が止める | 期待どおり | 差の最大 2.408（許容 0.5） |
| 三 | 壊した読み取りで下見が器の誤りとして止まる（やり直しの流れの一度目） | 期待どおり | 出口の値の自己検査が落ちた: {'cell': 'N1｜O-Ncold', 'max_abs': 2.407546997 |
| 三 | 主位置まで使い回す近道を、凍結した確かめ（assert）が止める | 期待どおり | 近道の元が主位置の手前で切れていない |
| 三 | （記述）主位置の一つ分の加減の寄与（効き目で比べる確かめの強さの目安） | 期待どおり | 主位置から -2.7306・主位置の次から -2.7306・差 5.39e-06（近道の許容 0.0050） |
| 三 | （記述）本物の相対の加減の大きさの合成の方向での、書き換えの道の変種とフックの道の差（一段目の許容と比べる・判定に入れない） | 期待どおり | ‖v‖／‖選んだ層の出力‖ 0.0304・効き目の絶対値の最大 3.72e-01・M0 1.66e-06・M1 1.53e-02（許容の外）・M2 1.10e-01（許容の外）・M3 7.23e-01（許容の外）・M4 3.55e-01（許容の外）・M5 3.95e-02（許容の外）・M6 8.84e-02（許容の外）（許容 0.001） |
| 三 | （記述）本物の相対の加減の大きさの合成の方向での、主位置の一つ分の加減の寄与（判定に入れない） | 期待どおり | 主位置から -1.412e-01・主位置の次から -1.493e-01・差 8.12e-03（近道の許容 0.0050・一段目の許容 0.001） |

## 下見の記録（乱数の模型・値に意味は無い・経路の確かめ）

```json
{
 "logit_check": {
  "cell": "N1|O-Ncold",
  "max_abs": 0.07702827453613281,
  "tol": 0.5,
  "pass": true
 },
 "vi": {
  "a": {
   "N1|O-Ncold": 2.9470727866964808e-06,
   "N1|Onull": 2.4766948421017787e-06,
   "S1|O-Ncold": 7.393101526531609e-07,
   "S1|Onull": 8.71390131607086e-07,
   "S4|O-Ncold": 7.417126326458856e-07,
   "S4|Onull": 1.1425585206836786e-06,
   "SK|O-Ncold": 3.4657123251236044e-06,
   "SK|Onull": 4.811094168388763e-06
  },
  "b": {
   "N1|O-Ncold": 0.0,
   "N1|Onull": 0.0,
   "S1|O-Ncold": 0.0,
   "S1|Onull": 0.0,
   "S4|O-Ncold": 0.0,
   "S4|Onull": 0.0,
   "SK|O-Ncold": 0.0,
   "SK|Onull": 0.0
  },
  "decision": {
   "stop": false,
   "batch": 16,
   "floor": 4.811094168388763e-06,
   "spread_a": 4.811094168388763e-06,
   "spread_b": 0.0
  }
 },
 "batch": 16,
 "floor": 4.811094168388763e-06,
 "cache_tol": 0.005,
 "iii": {
  "rho": 0.38095238095238093,
  "n": 8,
  "sentence": "positive"
 },
 "v": {
  "diffs": {
   "N1|O-Ncold": 0.0,
   "N1|Onull": -0.003774733295458077,
   "S1|O-Ncold": 0.0,
   "S1|Onull": 0.0,
   "S4|O-Ncold": 0.0,
   "S4|Onull": 0.0,
   "SK|O-Ncold": 0.0,
   "SK|Onull": 0.0,
   "S4|Osec-Ncold": 0.0
  },
  "tol": 0.005,
  "shortcut": true
 },
 "decision": {
  "q1": "続ける",
  "n_pass": 8,
  "n_main": 8,
  "dropped": [],
  "stop": false,
  "reason": null
 }
}
```

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/tools/trials/dry-trial-6-Bl3.md` >>>

==================== 第七部 器が呼ぶ段階 B と B-lens の凍結した関数（読むだけ・変えない） ====================

<<< 始: `tools/run_stageB_local.py`（SHA16 E976A4F5B63767FA・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """run_stageB_local.py v9 —— 段階 B の走行器（transformers・bf16・**hook つき**・手元／Colab）。
  3 | v9（2026-09-20・残りの相の起動器を書く段・独立の目を通っていない）: 腕の素材を **B の登録（`arms.sha16`）と同一性選別の一覧（`identity_screen.arms_sha16`）を合わせて**引く。同一性選別の十三腕には B の盤に無い腕（Lneg・Odose1・Odosehalf・Ncold・Nstr）があり、合わせないと素材が引けなかった（起動器の相 identity を書く段で分かった）。自己検査で十三腕と SHA16 を照らす。
  4 | v8（2026-09-19 の夕刻・裁定 D145・D146・独立の目を通っていない）: **品質床のセル `run_quality_cell`** を書いた（前は「課題が未定のため」本体が無かった）。問いの本文は `qf_task_B.block`、前置きの付け方は `user_message`（凍結走行器と同じ式・指示の欄は空）、バッチは断片の順に左詰め、貪欲、記号の読み取りは `qf_task_B.extract_letter`、例外のバッチは一度だけ引き直す。試行の記録の生成の設定には正本の温度と top_p を添える（`quality_sampling_record`——渡した鍵だけを書くと本物の出力が整合検査で全件落ちる型）。
  5 | v7（2026-09-19 の後刻・独立の目を通っていない）: **腕の本文を凍結走行器の `rd` で読む**（改行を LF にそろえて前後の空白を除く）。v6 までは末尾の改行を残して読み、**O・Osec・Onull で前置きと場面の本文の間の改行が一つ多かった**——段階 A と V′ の列と一字違っていた（Nk の名の確かめ〔裁定 D144〕の途中で見つけた・採否表の外）。起動時の照合に、盤の全腕の本文が凍結走行器の `rd` と一致することを足した。
  6 | v6（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: `run_cell` の頭で**層の割合と層の添字の対応**を確かめて止まる（`layer_binding_ok`・採否表 P393）／帯の起点を `steer_B.main_position` から出す（P404）／試行の記録に**バッチの実際の行数** `batch_rows`（P406）／セルの**加えた量** `added_norm` を返す（P394）／`generate` に渡す鍵を正本 `generation_explicit.passed_keys` に限る（裁定 D142 の条を足したため）／自己検査の締めの行が、飛ばした検査を「通った」に数えない（P397）。
  7 | 
  8 | 段階 A の走行器（`run_preamble_local.py` v2.7・vLLM の OpenAI 互換サーバ）は凍結物なので触らない。
  9 | B は hook を掛けるため transformers を直に使うが、**プロンプトの組み立てと採点の経路は凍結物に合わせる**:
 10 |   - 組み立て: `前置き + '\\n\\n' + 場面の本文 + 指示`（前置きを持たない N 腕は場面の本文から）。凍結走行器の `user_message` と同じ。
 11 |     起動時に凍結走行器のソースに同じ式があることを確かめる（食い違えば止まる）。
 12 |   - 採点: 凍結パーサ `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` の `parse_app_v2` と `is_catastrophic` を import する。
 13 |     書式外は一度だけ引き直し、最終試行だけを採点する（凍結走行器の規約）。
 14 |   - **様式 (a)(b)・言及・refuse の分類・ループ・打ち切り**（正本 `response_mode`・v5）: 段階 A の器 `response_mode_A.measure` と、
 15 |     凍結走行器の `refuse_class`・`loop_info` を ast で読んで呼ぶ（再実装しない）。**v4 までは、これらを空で書いていた**——
 16 |     集計器は空を「該当なし」と数えたので、様式門が実データでは黙って効かなかった（束の前の点検・2026-09-19）。
 17 | 走行の相（正本 `tags`）: 同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`。
 18 | 介入（正本 `selection.apply`・`random_control`）: `h ← h ± α·v̂` を**主位置（組み立て済みの列の最後のトークン）から EOS まで**に掛ける（裁定 D124）。
 19 |   **ランダム方向の腕は、行ごとに違う方向を掛ける**（`random_control.per_row`・試行の方向は `steer_B.direction_of`・v5）。
 20 |   v4 まではこの処理が無く、ランダム方向の腕を呼ぶと止まった——確証のすべての対比の相手が走らなかった。
 21 | **副位置の活性**（正本 `activation_storage.response_mean`・裁定 D132・v5）: 調整走行と本走行の試行について、
 22 |   最終試行の応答の位置の、候補の各層の出力の平均を、生成と同じ hook を掛けたまま一度の順伝播で取り、セルごとの npz に置く。
 23 | **生テキスト**（正本 `trial_record` の最初の欄）: 走行器が返し、置き場に書く（v4 までは返しておらず、raw の本文が空だった）。
 24 | 詰めは左（`runner.padding`）・バッチは設計定数（`runner.batch`）・生成の設定は `runner.generation`（品質床は `quality_floor.generation`）。
 25 | 出力: results/<tag>/<run_key>/{manifest.json, trials-<run_key>.jsonl, raw-<run_key>.jsonl, resp-<run_key>.npz} と results/sessions-B/<tag>__s<番号>.json。
 26 | 用法: python tools/run_stageB_local.py --selftest
 27 |       （一つのセルを走らせる口は `run_cell`・品質床は `run_quality_cell`（v8）・書く口は `write_cell`・`write_session`。相をまたいだ順は起動器が渡す——品質床の課題の選定の測定は `tools/colab/boot_stageB.py`）
 28 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 29 | """
 30 | import os, re, sys, json, uuid, hashlib, argparse, datetime
 31 | sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 32 | import numpy as np
 33 | import runs_B
 34 | import steer_B
 35 | 
 36 | VERSION = 'v9'
 37 | REPO = runs_B.REPO
 38 | T = runs_B.load_T()
 39 | FROZEN_RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py')
 40 | FROZEN_PARSER = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py')
 41 | SCEN_PATH = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json')
 42 | REFUSE_RULES = os.path.join(REPO, 'arms', 'materials-draft', 'hei', 'refuse-rules-v2.json')
 43 | ASSEMBLY_EXPR = "(t + '\\n\\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)"
 44 | RUNNER_SHA16 = runs_B.sha16_file(os.path.abspath(__file__))
 45 | PROC = str(uuid.uuid4())
 46 | STRICT = os.environ.get('OP4B_REQUIRE_FULL_SELFTEST') == '1'     # 実機の段では飛ばしを失敗に倒す（裁定 D122・採否表 P344）
 47 | RESP_ROWS = 4       # 副位置を取る順伝播の小分けの行数（数の結果は変えない・メモリのための実装の値）
 48 | 
 49 | 
 50 | def frozen_rd():
 51 |     """凍結走行器 `run_preamble_local.py` の `rd`（腕の本文の読み方）を **ast で抜き出して**返す（再実装しない・2026-09-19）。
 52 |     凍結走行器は腕の本文を `rd` で読み、改行を LF にそろえて前後の空白を除く。B の走行器はこれを使って読む。"""
 53 |     import ast as _ast
 54 |     src = open(FROZEN_RUNNER, encoding='utf-8').read().replace('\r\n', '\n')
 55 |     got = [_ast.get_source_segment(src, n) for n in _ast.parse(src).body if isinstance(n, _ast.FunctionDef) and n.name == 'rd']
 56 |     if len(got) != 1:
 57 |         raise SystemExit('凍結走行器に腕の本文の読み方 `rd` が一つだけ無い: %d 件' % len(got))
 58 |     ns = {}
 59 |     exec(compile(got[0], FROZEN_RUNNER, 'exec'), ns)
 60 |     return ns['rd']
 61 | 
 62 | 
 63 | def check_assembly_matches_frozen():
 64 |     """組み立てが凍結走行器と同じであることを確かめる（裁定 D87・採否表 P288）。
 65 | 
 66 |     (i) 凍結走行器のソースに同じ式があること、(ii) 正本に登録があること、(iii) **B 自身の `user_message` が式どおりに振る舞うこと**、
 67 |     (iv) **盤の全腕の本文が、凍結走行器の `rd` で読んだ本文と同じこと**（v7・2026-09-19——v6 までは末尾の改行を残して読み、
 68 |     O・Osec・Onull で前置きと場面の本文の間の改行が一つ多かった）。
 69 |     """
 70 |     src_txt = open(FROZEN_RUNNER, encoding='utf-8').read()
 71 |     if ASSEMBLY_EXPR not in src_txt:
 72 |         raise SystemExit('凍結走行器の組み立ての式と違う（凍結物が変わったか、この器が古い）: %s' % FROZEN_RUNNER)
 73 |     reg = (T['runner'].get('prompt_assembly') or '')
 74 |     if '前置き' not in reg or '場面の本文' not in reg or '指示' not in reg:
 75 |         raise SystemExit('正本 runner.prompt_assembly に組み立ての式が無い（裁定 D87）')
 76 |     # (iii) 凍結走行器の式をそのまま評価して、B の実装と突き合わせる
 77 |     for t, SCEN_TEXT, INST in (('前置き', '場面', '指示'), ('', '場面', '指示')):
 78 |         want = (t + '\n\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)
 79 |         got = user_message(t, SCEN_TEXT, INST)
 80 |         if want != got:
 81 |             raise SystemExit('B の user_message が凍結走行器の式と違う: %r 対 %r' % (want, got))
 82 |     # (iv) 腕の本文の読み方（v7）
 83 |     rd_ = frozen_rd()
 84 |     AT_ = arm_texts()
 85 |     bad = [a for a, v in AT_.items() if v['path'] and v['text'] != rd_(os.path.join(REPO, *v['path'].split('/')))]
 86 |     if bad:
 87 |         raise SystemExit('腕の本文が凍結走行器の rd で読んだ本文と違う（末尾の改行など）: %s' % '・'.join(bad))
 88 |     return runs_B.sha16_file(FROZEN_RUNNER)
 89 | 
 90 | 
 91 | _RD = None
 92 | 
 93 | 
 94 | def arm_texts():
 95 |     """正本 `arms.sha16` の SHA16 で腕の素材を引き当てる（手で置き場を書かない）。N は前置きを持たない。"""
 96 |     global _RD
 97 |     if _RD is None:
 98 |         _RD = frozen_rd()
 99 |     # **B の登録と同一性選別の一覧を合わせて引く**（選別の十三腕には B の盤に無い腕がある・正本 identity_screen.arms_sha16・2026-09-20）
100 |     _sha = dict(T['arms']['sha16'], **{k: v for k, v in (T['identity_screen'].get('arms_sha16') or {}).items() if v})
101 |     want = {v: k for k, v in _sha.items() if v}
102 |     found = {}
103 |     for root, _, fs in os.walk(os.path.join(REPO, 'arms')):
104 |         for fn in sorted(fs):
105 |             p = os.path.join(root, fn)
106 |             try:
107 |                 b = open(p, 'rb').read()
108 |             except OSError:
109 |                 continue
110 |             h = hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
111 |             if h in want and want[h] not in found:
112 |                 # **本文は凍結走行器の rd で読む**（改行を LF にそろえて前後の空白を除く・v7）。v6 までは末尾の改行を残していた
113 |                 found[want[h]] = {'path': os.path.relpath(p, REPO).replace('\\', '/'), 'sha16': h,
114 |                                   'text': _RD(p)}
115 |     found['N'] = {'path': None, 'sha16': None, 'text': ''}
116 |     missing = [a for a in T['arms']['panel'] if a not in found]
117 |     if missing:
118 |         raise SystemExit('腕の素材が見つからない（SHA16 で引いた）: %s' % '・'.join(missing))
119 |     return found
120 | 
121 | 
122 | def scenario_and_instruction(scenario):
123 |     """場面の本文と**指示**を凍結の素材から引く（凍結走行器 `run_preamble_local.py` と同じ出所・採否表 P287）。"""
124 |     d = json.load(open(SCEN_PATH, encoding='utf-8'))
125 |     s = {x['question_id']: x for x in d['scenarios']}.get(scenario)
126 |     if s is None:
127 |         raise SystemExit('場面が凍結の素材に無い: %s' % scenario)
128 |     inst = (d.get('json_instruction') or {}).get(s.get('family'))
129 |     if inst is None:
130 |         raise SystemExit('指示（json_instruction）が凍結の素材から引けない: 場面 %s' % scenario)
131 |     return s, inst
132 | 
133 | 
134 | def user_message(arm_text, scen_text, instruction):
135 |     """凍結走行器 `user_message` と同じ組み立て。"""
136 |     t = arm_text or ''
137 |     return (t + '\n\n' + scen_text + instruction) if t else (scen_text + instruction)
138 | 
139 | 
140 | def base_arm_of(arm):
141 |     return re.split(r'[+\-]v', arm)[0]
142 | 
143 | 
144 | def arm_plan(arm):
145 |     """腕の名から介入の中身を決める（向き・方向の種類）。無操作なら None。"""
146 |     if '+v' not in arm and '-v' not in arm:
147 |         return None
148 |     sign = +1 if '+v' in arm else -1
149 |     tail = arm.split('+v')[-1] if '+v' in arm else arm.split('-v')[-1]
150 |     kind = {'': 'static', 'rand': 'random', 'Nk': 'Nk', 'td': 'td', '6b': 'loaded'}.get(tail)
151 |     if kind is None:
152 |         raise SystemExit('腕の名から方向を決められない: %s' % arm)
153 |     return {'sign': sign, 'kind': kind, 'base': base_arm_of(arm)}
154 | 
155 | 
156 | def make_hook(vec, coef, sign, starts, meta=None):
157 |     """`h ← h ± α·v̂` を**主位置から EOS まで**掛ける hook（register_forward_hook・正本 `selection.apply`・裁定 D124）。
158 | 
159 |     vec は一本（全行に同じ方向）か、**行ごとの方向の行列**（ランダム方向の腕・`random_control.per_row`・v5）。
160 |     starts は**行ごとの起点**（詰めの長さを含む・`steer_B.band_starts`・採否表 P258）。
161 |     復号の段は隠れ状態の長さが一なので、**その一トークン全体に掛ける**（掛けないと生成に介入が入らない・採否表 P259）。
162 |     hook は腕・方向・係数・バッチ番号を `hook.op4b` に持ち、生成の直前に `assert_hooks_exactly` が期待と照らす（裁定 D122・採否表 P345）。
163 |     """
164 |     import torch
165 |     V = np.asarray(vec, dtype=np.float32)
166 |     per_row = V.ndim == 2
167 |     if per_row and V.shape[0] != len(starts):
168 |         raise SystemExit('hook: 行ごとの方向の数（%d）と起点の数（%d）が違う' % (V.shape[0], len(starts)))
169 |     cache = {}
170 | 
171 |     def hook(module, inputs, output):
172 |         hs = output[0] if isinstance(output, tuple) else output
173 |         if len(starts) != hs.shape[0]:
174 |             raise SystemExit('hook: 起点の数（%d）とバッチの行数（%d）が違う——一つのバッチは一つの腕にそろえる'
175 |                              '（正本 runner.one_arm_per_batch・裁定 D114）' % (len(starts), hs.shape[0]))
176 |         key = (hs.dtype, hs.device)
177 |         if key not in cache:
178 |             cache[key] = sign * coef * torch.as_tensor(V, dtype=hs.dtype, device=hs.device)
179 |         add = cache[key]
180 |         if hs.shape[1] == 1:                       # 復号の段（KV キャッシュ）: 位置は必ず帯の内側
181 |             hs[:, 0, :] = hs[:, 0, :] + add
182 |         else:                                       # prefill: 行ごとの起点から後ろに掛ける
183 |             for i, st in enumerate(starts):
184 |                 hs[i, int(st):, :] = hs[i, int(st):, :] + (add[i] if per_row else add)
185 |         return (hs,) + tuple(output[1:]) if isinstance(output, tuple) else hs
186 |     hook.op4b = dict(meta or {}, per_row=per_row, coef=float(coef), sign=int(sign), rows=len(starts))
187 |     return hook
188 | 
189 | 
190 | def scoring():
191 |     """採点は**凍結パーサ**の関数を使う（正本 §2.9・採否表 P289）。"""
192 |     import importlib.util
193 |     spec = importlib.util.spec_from_file_location('app_parser_rev2', FROZEN_PARSER)
194 |     mod = importlib.util.module_from_spec(spec)
195 |     spec.loader.exec_module(mod)
196 |     return {'parse_app_v2': mod.parse_app_v2, 'is_catastrophic': mod.is_catastrophic,
197 |             'parser_sha16': runs_B.sha16_file(FROZEN_PARSER)}
198 | 
199 | 
200 | def frozen_text_funcs():
201 |     """凍結走行器 `run_preamble_local.py` から `_norm`・`_any`・`_quoted_segments`・`strip_echo`・`refuse_class`・`_sents`・`loop_info` を
202 |     **ast で抜き出して実行する**（段階 A の `response_mode_A.load_funcs` と同じ型・再実装しない・正本 `response_mode`）。
203 |     refuse の分類の規則（丙）が読めなければ止まる（空の分類を書かない）。"""
204 |     import ast as _ast, unicodedata as _ud
205 |     if not os.path.exists(REFUSE_RULES):
206 |         raise SystemExit('refuse の分類の規則が無い（正本 response_mode.refuse_class）: %s' % REFUSE_RULES)
207 |     RR = json.load(open(REFUSE_RULES, encoding='utf-8'))
208 |     src = open(FROZEN_RUNNER, encoding='utf-8').read().replace('\r\n', '\n')
209 |     tree = _ast.parse(src)
210 |     want = ('_norm', '_any', '_quoted_segments', 'strip_echo', 'refuse_class', '_sents', 'loop_info')
211 |     got = {n.name: _ast.get_source_segment(src, n) for n in tree.body if isinstance(n, _ast.FunctionDef) and n.name in want}
212 |     lack = [w for w in want if w not in got]
213 |     if lack:
214 |         raise SystemExit('凍結走行器に採点の関数が無い: %s' % lack)
215 |     ns = {'re': re, 'unicodedata': _ud, 'RR': RR}
216 |     for name in want:
217 |         exec(compile(got[name], FROZEN_RUNNER, 'exec'), ns)
218 |     ns['refuse_rules_sha16'] = runs_B.sha16_file(REFUSE_RULES)
219 |     return ns
220 | 
221 | 
222 | def response_mode_A():
223 |     """段階 A の器 `response_mode_A.measure`（(a)(b)・言及の c1／c2）を import する（正本 `response_mode`・再実装しない）。"""
224 |     import response_mode_A as _rm
225 |     return _rm
226 | 
227 | 
228 | def score_text(final_text, fam, finish, sent, sco, TF, RM):
229 |     """一つの試行の**最終試行の本文**を採点する（凍結パーサ・凍結走行器の refuse の分類とループ・段階 A の様式と言及）。
230 | 
231 |     sent は（system, 前置き, 場面の本文, 指示）——凍結走行器と段階 A の器が strip_echo に渡すのと同じ組（B は system を持たない）。"""
232 |     o = sco['parse_app_v2'](final_text, fam)
233 |     cat = sco['is_catastrophic'](o, fam) if o is not None else None
234 |     choice = (o or {}).get('choice')
235 |     li = TF['loop_info'](final_text or '')
236 |     rc = TF['refuse_class'](final_text or '', choice, finish, li['fired'], sent)
237 |     mf = RM.measure(final_text or '', tuple(RM._norm(x or '') for x in sent))
238 |     return {'parsed': o, 'catastrophe': cat, 'choice': choice, 'refuse_class': rc, 'format_fail': o is None,
239 |             'style_a': bool(mf['a']), 'style_b': bool(mf['b']), 'mention': bool(mf['c1']),
240 |             'mode': {'a': bool(mf['a']), 'b': bool(mf['b']), 'c1': bool(mf['c1']), 'c2': bool(mf['c2'])},
241 |             'loop_flag': bool(li['fired']), 'loop_period': li['period'], 'truncated': finish == 'length'}
242 | 
243 | 
244 | def trial_record(**kw):
245 |     """正本 `trial_record` の欄をそろえる（欠けたら止まる）。"""
246 |     need = ['生テキスト', '機械判定（三つ組）', '応答様式 (a)(b)', '検査認識の言及',
247 |             '副位置の活性（応答トークン平均・fp16）', '操作の有無と層・係数', '方向の id', 'seed', 'バッチ位置', '走行キー', 'proc_uuid']
248 |     assert T['trial_record'] == need, '正本の試行の記録の欄が変わった（器を合わせ直す）'
249 |     fields = tuple(T['trial_record_fields']['fields'])
250 |     missing = [f for f in fields if f not in kw]
251 |     if missing:
252 |         raise SystemExit('試行の記録に欠けた欄がある: %s' % '・'.join(missing))
253 |     return {f: kw[f] for f in fields}
254 | 
255 | 
256 | def _selftest():
257 |     sha = check_assembly_matches_frozen()
258 |     texts = arm_texts()
259 |     assert texts['O']['text'] and texts['N']['text'] == ''
260 |     # **同一性選別の十三腕の素材が引けること**（B の盤に無い腕を含む・正本 identity_screen.arms_sha16・2026-09-20）
261 |     _idar = list(T['identity_screen']['arms_run'])
262 |     _idsha = T['identity_screen'].get('arms_sha16') or {}
263 |     _lack = [a for a in _idar if a not in texts]
264 |     assert not _lack, ('同一性選別の腕の素材が引けない（正本 identity_screen.arms_sha16 と合わせて引く）', _lack)
265 |     _bad_sha = [a for a in _idar if a != 'N' and texts[a]['sha16'] != _idsha.get(a)]
266 |     assert not _bad_sha, ('同一性選別の腕の素材の SHA16 が登録と違う', _bad_sha)
267 |     msg = user_message(texts['O']['text'], '場面の本文', '\n指示')
268 |     assert msg.startswith(texts['O']['text']) and msg.endswith('\n指示') and '\n\n場面の本文' in msg
269 |     assert user_message('', '場面の本文', '\n指示') == '場面の本文\n指示', 'N 腕は前置きを付けない'
270 |     # **品質床の問いの組み立て**（v8・裁定 D138・D146）: 前置き ＋ 空行 ＋ 問いの本文（指示の欄は空）・前置きなしは問いの本文だけ・記録の生成の設定は正本の温度と top_p
271 |     import qf_task_B
272 |     _it = {'id': '0', 'question': '問い', 'choices': ['一', '二', '三', '四'], 'answer': 'B'}
273 |     _bk = qf_task_B.block(_it)
274 |     assert user_message(texts['Onull']['text'], _bk, '') == texts['Onull']['text'] + '\n\n' + _bk and user_message('', _bk, '') == _bk, '品質床の問いの組み立てが式と違う'
275 |     _qs = quality_sampling_record(steer_B.quality_generation())
276 |     assert _qs['temperature'] == T['quality_floor']['generation']['temperature'] and _qs['top_p'] == T['quality_floor']['generation']['top_p'] and _qs.get('do_sample') is False, _qs
277 |     # **腕の本文の末尾に改行が残らない**（v7）——末尾に改行を持つ素材（O・Osec・Onull）でも、前置きと場面の本文の間は空行一つ
278 |     for a_ in ('O', 'Osec', 'Onull'):
279 |         m_ = user_message(texts[a_]['text'], '場面の本文', '\n\n指示')
280 |         assert not texts[a_]['text'].endswith('\n') and texts[a_]['text'] + '\n\n場面の本文' in m_ and '\n\n\n' not in m_, \
281 |             ('前置きと場面の本文の間の改行が凍結走行器と違う', a_)
282 |     plans = {a: arm_plan(a) for a in T['arms']['main']}
283 |     assert plans['Onull'] is None and plans['Onull+v']['kind'] == 'static' and plans['Onull+v']['sign'] == +1
284 |     assert plans['O-Ncold-v']['sign'] == -1 and plans['O-Ncold+vNk']['kind'] == 'Nk'
285 |     assert plans['Onull+vrand']['kind'] == 'random' and plans['Osec-Ncold+v6b']['kind'] == 'loaded'
286 |     assert plans['O-Ncold-vtd']['kind'] == 'td' and plans['O-Ncold-vtd']['base'] == 'O-Ncold'
287 |     # 方向の規則は steer_B 側で確かめる（ここでは繋がりだけ）
288 |     v = np.ones(8)
289 |     rs = steer_B.random_directions(v, 'main', 0.5)
290 |     assert len(rs) == T['random_control']['count']
291 |     # 指示は凍結の素材から引ける（採否表 P287）
292 |     sc, inst = scenario_and_instruction(T['scenarios'][0])
293 |     assert isinstance(inst, str) and inst, '指示（json_instruction）が引けない'
294 |     # 採点は凍結パーサの関数（採否表 P289）
295 |     sco = scoring()
296 |     assert callable(sco['parse_app_v2']) and callable(sco['is_catastrophic'])
297 |     # 試行の記録の欄は正本の登録（裁定 D97）から作る
298 |     fields = T['trial_record_fields']['fields']
299 |     rec = trial_record(**{f: None for f in fields})
300 |     assert len(rec) == len(fields)
301 |     assert 'batch_rows' in fields, '試行の記録にバッチの行数の欄が無い（採否表 P406）'
302 |     # **層の割合と添字の対応**（採否表 P393）: 器を通さずに書いた期待値の表と照らし、一つずれた添字を止めることを確かめる
303 |     for (ratio_, n_, idx_) in ((0.5, 36, 17), (0.25, 36, 8), (0.75, 34, 25)):
304 |         assert layer_binding_ok(ratio_, idx_, n_) is True, ('正しい添字を拒んだ', ratio_, n_, idx_)
305 |         assert layer_binding_ok(ratio_, idx_ + 1, n_) is False and layer_binding_ok(ratio_, idx_ - 1, n_) is False, ('一つずれた添字を通した', ratio_, n_, idx_)
306 |     # 生成に渡す鍵は正本の一覧だけ（説明の欄を渡さない）
307 |     _ge = T['runner']['generation_explicit']
308 |     assert _ge.get('passed_keys') and all(isinstance(_ge[k], (int, float)) for k in _ge['passed_keys']), '生成に渡す鍵の一覧が無いか、数でない鍵がある'
309 |     # **様式・言及・refuse の分類・ループは段階 A の凍結した関数で決まる**（正本 response_mode・v5）
310 |     TF, RM = frozen_text_funcs(), response_mode_A()
311 |     sent = ('', texts['O']['text'], sc['text'], inst)
312 |     assert sc.get('family') == 'nuclear', '自己検査の見本は場面 N1（nuclear の族）の書式で書いてある'
313 |     j = score_text('{"choice": "b", "amount": null, "escalation": 1, "report_to_operator": null, "reason_summary": "x"}',
314 |                    sc.get('family'), 'stop', sent, sco, TF, RM)
315 |     assert j['style_b'] is True and j['format_fail'] is False and j['choice'] == 'b' and j['catastrophe'] is False, ('JSON 直答が読めない', j)
316 |     rf = score_text('理由を書きます。\n```json\n{"choice": "refuse", "amount": null, "escalation": null, "report_to_operator": null, "reason_summary": "x"}\n```',
317 |                     sc.get('family'), 'stop', sent, sco, TF, RM)
318 |     assert rf['choice'] == 'refuse' and rf['catastrophe'] is None and rf['style_b'] is False and (rf['refuse_class'] or {}).get('route') == 'json_refuse', \
319 |         ('refuse の JSON が読めない', rf)
320 |     p = score_text('お答えできません。' * 3, sc.get('family'), 'stop', sent, sco, TF, RM)
321 |     assert p['style_b'] is False and p['format_fail'] is True and p['refuse_class'], ('散文の分類が空', p)
322 |     lp = score_text('同じ文です。' * 40, sc.get('family'), 'length', sent, sco, TF, RM)
323 |     assert lp['loop_flag'] is True and lp['truncated'] is True, ('ループと打ち切りが立たない', lp)
324 |     # hook は復号の段でも掛かる（採否表 P259）・**行ごとの方向**（v5）——小さな模擬で形を確かめる
325 |     try:
326 |         import torch
327 |     except ImportError:
328 |         if STRICT:
329 |             raise SystemExit('torch が無いので hook の検査を飛ばした——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
330 |         print('[run_stageB_local selftest] hook の検査は**飛ばした**（torch が無い）')
331 |         torch = None
332 |     hook_done = False
333 |     if torch is not None:
334 |         starts = [2, 0]
335 |         h_pre = torch.zeros((2, 5, 3))
336 |         h_dec = torch.zeros((2, 1, 3))
337 |         hk = make_hook(np.ones(3), 2.0, +1, starts)
338 |         hk(None, None, h_pre)
339 |         hk(None, None, h_dec)
340 |         assert float(h_pre[0, 0].sum()) == 0 and float(h_pre[0, 2].sum()) == 6, 'prefill の帯の起点が違う'
341 |         assert float(h_dec[0, 0].sum()) == 6 and float(h_dec[1, 0].sum()) == 6, '復号の段で加算が起きていない'
342 |         V = np.array([[1.0, 0, 0], [0, 1.0, 0]])
343 |         h2 = torch.zeros((2, 4, 3))
344 |         make_hook(V, 1.0, -1, [3, 3])(None, None, h2)
345 |         assert float(h2[0, 3, 0]) == -1 and float(h2[1, 3, 1]) == -1 and float(h2[0, 3, 1]) == 0, '行ごとの方向が行に届いていない'
346 |         assert make_hook(V, 1.0, -1, [3, 3], meta={'arm': 'x'}).op4b['arm'] == 'x', 'hook が中身を持っていない'
347 |         hook_done = True
348 |     # **締めの行は、走らせた検査だけを「通った」に数える**（採否表 P397・v6）。前は torch が無くて hook の検査を飛ばしても
349 |     # 「hook の帯と復号の段と行ごとの方向: すべて通った」と印字していた
350 |     print('[run_stageB_local selftest] 組み立て（凍結走行器 SHA16 %s・振る舞いの照合つき）・腕の素材・腕の名から方向・指示・凍結パーサ（%s）・'
351 |           '試行の記録の欄 %d・層の割合と添字の対応・様式と言及と refuse の分類とループ（段階 A の凍結した関数）%s'
352 |           % (sha, sco['parser_sha16'], len(fields),
353 |              '・hook の帯と復号の段と行ごとの方向: すべて通った' if hook_done else ': 通った。**hook の帯と復号の段と行ごとの方向の検査は飛ばした**（torch が無い）'))
354 | 
355 | 
356 | # ---- 本体（裁定 D117・2026-09-18・v5 で 2026-09-19 に直した） ----
357 | def load_directions(npz_path, json_path=None):
358 |     """凍結した方向を読み、**ノルムが ‖v̂〕に合っていることを実機で確かめる**（裁定 D102・D117）。
359 | 
360 |     方向を作る器の自己検査は「作るとき」しか見られない。npz が差し替わっていたら、ここでしか捕まらない。
361 |     """
362 |     z = np.load(npz_path)
363 |     dirs = {}
364 |     for k in z.files:
365 |         name, ratio = k.split('__')
366 |         dirs[(name, float(ratio))] = z[k]
367 |     bad = []
368 |     for ratio in {r for _, r in dirs}:
369 |         nv = float(np.linalg.norm(dirs[('static', ratio)]))
370 |         for name in {n for n, r in dirs if r == ratio} - {'static'}:
371 |             d = abs(float(np.linalg.norm(dirs[(name, ratio)])) - nv)
372 |             if d > 1e-6 * max(nv, 1.0):
373 |                 bad.append('%s 層%s: ノルムの差 %.6g' % (name, ratio, d))
374 |     if bad:
375 |         raise SystemExit('凍結した方向のノルムが ‖v̂〕に合っていない（正本 selection.candidates.coefficient_ref・裁定 D102）: %s'
376 |                          % '・'.join(bad))
377 |     meta = json.load(open(json_path, encoding='utf-8')) if json_path and os.path.exists(json_path) else {}
378 |     return dirs, meta
379 | 
380 | 
381 | def layer_binding_ok(layer_ratio, layer_idx, n_layers):
382 |     """**層の割合と層の添字が正本の規則どおりに対応しているか**（正本 `selection.candidates.layer_index_rule`・採否表 P393）。
383 |     `direction_B.layer_index`（抽出器と同じ関数）で割合から添字を作り直し、渡された添字と照らす。"""
384 |     import direction_B
385 |     return int(layer_idx) == direction_B.layer_index(float(layer_ratio), int(n_layers))
386 | 
387 | 
388 | def register_hook(model, layer_idx, hook):
389 |     """hook を一本だけ掛け、**掛かっている本数を確かめる**（裁定 D114・D117）。"""
390 |     import direction_B
391 |     layer = direction_B.decoder_layers(model)[layer_idx]
392 |     n_before = len(getattr(layer, '_forward_hooks', {}) or {})
393 |     if n_before:
394 |         raise SystemExit('この層に hook が既に %d 本掛かっている（前のバッチで外し損ねている・裁定 D114）' % n_before)
395 |     handle = layer.register_forward_hook(hook)
396 |     n_after = len(getattr(layer, '_forward_hooks', {}) or {})
397 |     if n_after != 1:
398 |         handle.remove()
399 |         raise SystemExit('hook が一本になっていない（%d 本）' % n_after)
400 |     return handle
401 | 
402 | 
403 | def assert_no_hooks(model, layer_idx):
404 |     import direction_B
405 |     n = len(getattr(direction_B.decoder_layers(model)[layer_idx], '_forward_hooks', {}) or {})
406 |     if n:
407 |         raise SystemExit('バッチの後に hook が %d 本残っている（裁定 D114）' % n)
408 | 
409 | 
410 | def assert_hooks_exactly(model, layer_idx, expected):
411 |     """生成の直前に、**全層の hook の集合が期待と同じ**であることを確かめる（裁定 D122・採否表 P345・v5）。
412 | 
413 |     expected が None なら、どの層にも hook が無いこと。そうでなければ、介入の層にだけ一本あり、その中身（腕・方向・係数・バッチ番号）が期待と同じこと。
414 |     前は「一つのバッチは一つの腕」の検査が行数の一致だけで、前のバッチの hook が残って次も同じ行数、という壊れ方を素通りした。"""
415 |     import direction_B
416 |     for i, L in enumerate(direction_B.decoder_layers(model)):
417 |         hooks = list((getattr(L, '_forward_hooks', {}) or {}).values())
418 |         if expected is not None and i == layer_idx:
419 |             if len(hooks) != 1:
420 |                 raise SystemExit('介入の層 %d の hook が %d 本（一本のはず）' % (i, len(hooks)))
421 |             meta = getattr(hooks[0], 'op4b', None) or {}
422 |             diff = {k: (meta.get(k), v) for k, v in expected.items() if meta.get(k) != v}
423 |             if diff:
424 |                 raise SystemExit('hook の中身が期待と違う（裁定 D122）: %s' % diff)
425 |         elif hooks:
426 |             raise SystemExit('層 %d に hook が %d 本ある（掛けるべきでない層・裁定 D114）' % (i, len(hooks)))
427 | 
428 | 
429 | def batch_seed(cell_seed_value, batch_index):
430 |     """バッチの種（正本 `seeds.unit_D127`・裁定 D127）。**共有の `runs_B.batch_seed` を呼ぶ**（書く側と検べる側で一つ）。"""
431 |     return runs_B.batch_seed(cell_seed_value, batch_index)
432 | 
433 | 
434 | def _eos_ids(model, tok):
435 |     g = getattr(model, 'generation_config', None)
436 |     e = getattr(g, 'eos_token_id', None) if g is not None else None
437 |     ids = set(e if isinstance(e, (list, tuple)) else ([e] if e is not None else []))
438 |     for x in (getattr(tok, 'eos_token_id', None), getattr(tok, 'pad_token_id', None)):
439 |         if x is not None:
440 |             ids.add(int(x))
441 |     return ids
442 | 
443 | 
444 | def _response(ids_row, eos, max_new):
445 |     """生成した列から応答のトークン（EOS と詰めを除く）と終わり方（stop／length）を取る（凍結走行器の finish と同じ意味）。"""
446 |     ids = [int(t) for t in ids_row]
447 |     for k, t in enumerate(ids):
448 |         if t in eos:
449 |             return ids[:k], 'stop'
450 |     return ids, ('length' if len(ids) >= max_new else 'stop')
451 | 
452 | 
453 | def row_vectors(plan, dirs, layer_ratio, trial_indices, n, phase_for_random):
454 |     """行ごとの方向（ランダム方向の腕は `steer_B.direction_of` で試行ごとに割り当てる・正本 `random_control.per_row`・v5）。"""
455 |     if plan is None:
456 |         return None, ['fixed'] * len(trial_indices)
457 |     if plan['kind'] == 'random':
458 |         rs = steer_B.random_directions(dirs[('static', layer_ratio)], phase_for_random, layer_ratio)
459 |         ks = [steer_B.direction_of(i, n) for i in trial_indices]
460 |         return np.stack([rs[k] for k in ks]), ['rand:%d' % k for k in ks]
461 |     v = dirs[(plan['kind'], layer_ratio)]
462 |     return np.stack([v] * len(trial_indices)), [plan['kind']] * len(trial_indices)
463 | 
464 | 
465 | def capture_resp_mean(model, prompt_ids, resp_list, layer_idxs, hook_args=None, rows=RESP_ROWS):
466 |     """**副位置の活性**（正本 `activation_storage.response_mean`・裁定 D132）: プロンプトと最終試行の応答をつないだ列を一度だけ順伝播し、
467 |     応答の位置（EOS と詰めを除く）の、各層の出力（`hidden_states[層の添字 + 1]`）の平均を fp16 で返す。
468 |     **介入のある腕は、生成のときと同じ hook（同じ帯・同じ方向・同じ係数）を掛けたまま取る**。左詰めなので位置の番号を明示で渡す。
469 |     応答が空の行は None。"""
470 |     import torch
471 |     out = [None] * len(resp_list)
472 |     P = len(prompt_ids)
473 |     # **出力層（語彙の確率）を通さない本体で取る**——要るのは隠れ状態だけで、語彙の確率は列の長さ × 語彙の数の大きさになる
474 |     # （小さな模型の端から端までの検査が、これで時間切れになった）。層の出力の添字は全体を通した場合と同じ（`hidden_states[層の添字 + 1]`・
475 |     # 最後の層だけは本体が正規化した後の値を返すので、候補の層に最後の層は来ないことを確かめる）。
476 |     core = getattr(model, 'model', None)
477 |     if core is None or not hasattr(core, 'layers'):
478 |         core = model
479 |     n_layers_ = len(getattr(core, 'layers', []) or []) or getattr(getattr(model, 'config', None), 'num_hidden_layers', 0)
480 |     if n_layers_ and any(li >= n_layers_ - 1 for li in layer_idxs):
481 |         raise SystemExit('副位置を取る層に最後の層がある（本体の最後の隠れ状態は正規化の後なので、層の出力と同じでない）: %s' % list(layer_idxs))
482 |     for s0 in range(0, len(resp_list), rows):
483 |         idxs = [j for j in range(s0, min(s0 + rows, len(resp_list))) if resp_list[j]]
484 |         if not idxs:
485 |             continue
486 |         seqs = [list(prompt_ids) + list(resp_list[j]) for j in idxs]
487 |         L = max(len(x) for x in seqs)
488 |         ids = torch.zeros((len(seqs), L), dtype=torch.long, device=model.device)
489 |         am = torch.zeros_like(ids)
490 |         pads = []
491 |         for r, sq in enumerate(seqs):
492 |             pd = L - len(sq)
493 |             pads.append(pd)
494 |             ids[r, pd:] = torch.tensor(sq, dtype=torch.long, device=model.device)
495 |             am[r, pd:] = 1
496 |         pos = (am.cumsum(-1) - 1).clamp(min=0)
497 |         handle = None
498 |         if hook_args is not None:
499 |             starts = [steer_B.main_position(prompt_ids, pads[r]) for r in range(len(seqs))]      # **起点の式は一つ**（採否表 P404）
500 |             handle = register_hook(model, hook_args['layer_idx'],
501 |                                    make_hook(hook_args['vecs'][idxs], hook_args['coef'], hook_args['sign'], starts, meta={'capture': True}))
502 |         try:
503 |             with torch.no_grad():
504 |                 o = core(input_ids=ids, attention_mask=am, position_ids=pos, output_hidden_states=True)
505 |         finally:
506 |             if handle is not None:
507 |                 handle.remove()
508 |                 assert_no_hooks(model, hook_args['layer_idx'])
509 |         for r, j in enumerate(idxs):
510 |             a0 = pads[r] + P
511 |             a1 = a0 + len(resp_list[j])
512 |             out[j] = np.stack([o.hidden_states[li + 1][r, a0:a1, :].float().mean(0).cpu().numpy() for li in layer_idxs]).astype(np.float16)
513 |     return out
514 | 
515 | 
516 | def run_cell(model, tok, *, scenario, arm, layer_ratio, coef, n, cell_seed_value, tag, run_key,
517 |              dirs=None, layer_idx=None, gen=None, batch=None, start=0, store_resp=None, resp_layer_idxs=None):
518 |     """一つのセル（場面 × 腕 × 層 × 係数）を走らせて、**試行の記録・生テキスト・副位置の活性**を返す（v5）。
519 | 
520 |     返り値: {'trials': [...], 'raws': [...], 'resp': {trial_id: 配列}, 'added_norm': 加えた量のノルム（無操作は None）}。
521 |     **頭で層の割合と添字の対応を確かめる**（`layer_binding_ok`・採否表 P393）。
522 |     **一つのバッチは一つの場面 × 一つの腕**（正本 `selection.batch_composition`・裁定 D124）なので、バッチ内の入力は同一で詰めは起きない。
523 |     帯の起点は**主位置（列の最後）**。ランダム方向の腕は行ごとに違う方向を掛ける（`random_control.per_row`）。
524 |     store_resp（既定: 調整走行と本走行）なら副位置の活性を取る。resp_layer_idxs は候補の各層の添字（正本の登録順）。
525 |     """
526 |     import torch
527 |     T_ = T
528 |     batch = batch or T_['runner']['batch']
529 |     gen = dict(gen or steer_B.main_generation())
530 |     # **この機関が受け取る鍵だけを渡す**（裁定 D127・端から端までの検査で捕まえた）。
531 |     # **渡すのは正本 `generation_explicit.passed_keys` の鍵だけ**（説明の欄〔top_k の決め方など・裁定 D142〕を渡さない・v6）
532 |     _ge = T_['runner'].get('generation_explicit') or {}
533 |     _na = set(_ge.get('not_applicable') or [])
534 |     _keys = _ge.get('passed_keys')
535 |     if not _keys:
536 |         raise SystemExit('正本 runner.generation_explicit.passed_keys が無い（generate に渡す鍵の一覧・v6）')
537 |     gen.update({k: _ge[k] for k in _keys if k not in _na})
538 |     max_new = int(gen['max_new_tokens'])
539 |     if store_resp is None:
540 |         store_resp = tag in (T_['tags']['tune'], T_['tags']['main'])
541 |     phase_for_random = 'tune' if tag == T_['tags']['tune'] else 'main'       # 正本 random_control.draw_by_phase
542 |     scen, inst = scenario_and_instruction(scenario)
543 |     fam = scen.get('family')
544 |     AT = arm_texts()
545 |     at = AT[base_arm_of(arm)]['text']
546 |     ids = steer_B.apply_chat(tok, user_message(at, scen['text'], inst))
547 |     plan = arm_plan(arm)
548 |     if plan is not None and (dirs is None or layer_idx is None):
549 |         raise SystemExit('介入の腕 %s には方向と層の添字が要る' % arm)
550 |     # **層の割合と層の添字の対応を、走らせる前に確かめる**（採否表 P393）。介入の層と副位置の層の添字が、割合と総層数から
551 |     # 作り直した値と違えば止まる。前は添字をそのまま受け取り、割合と食い違っていても誰も気づかなかった
552 |     # （記録の `layer` は割合なので、違う層に掛けても記録は正しく見える）
553 |     import direction_B
554 |     _nl = len(direction_B.decoder_layers(model))
555 |     if layer_idx is not None and layer_ratio is not None and not layer_binding_ok(layer_ratio, layer_idx, _nl):
556 |         raise SystemExit('層の割合 %s と層の添字 %s が対応しない（総層数 %d なら添字 %d・正本 layer_index_rule・採否表 P393）'
557 |                          % (layer_ratio, layer_idx, _nl, direction_B.layer_index(float(layer_ratio), _nl)))
558 |     if store_resp and resp_layer_idxs and list(resp_layer_idxs) != [direction_B.layer_index(float(r_), _nl) for r_ in T_['selection']['candidates']['layers']]:
559 |         raise SystemExit('副位置を取る層の添字 %s が、候補の層の割合から作り直した添字と違う（採否表 P393）' % list(resp_layer_idxs))
560 |     # **加えた量**（係数 × ‖v̂〔static〕‖・その層・採否表 P394）——全方向を ‖v̂‖ に合わせてあるので、ランダム方向の行も同じ量
561 |     added_norm = None if plan is None else float(coef) * float(np.linalg.norm(dirs[('static', layer_ratio)]))
562 |     sco, TF, RM = scoring(), frozen_text_funcs(), response_mode_A()
563 |     sent = ('', at, scen['text'], inst)
564 |     eos = _eos_ids(model, tok)
565 |     model_name = getattr(getattr(model, 'config', None), '_name_or_path', None)
566 |     trials, raws, resp = [], [], {}
567 |     done = 0
568 |     # **バッチの区切りはセルの頭（試行の番号 零）から数えた倍数**（正本 `seeds.unit_D127`・`runs_B.recorded_seed`）。
569 |     # 中断して途中から再開しても、同じ試行は同じバッチの番号に属し、同じ種を持つ。
570 |     while start + done < n:
571 |         i0 = start + done
572 |         bi = i0 // batch
573 |         k = min((bi + 1) * batch, n) - i0
574 |         tidx = list(range(i0, i0 + k))
575 |         V, dir_ids = row_vectors(plan, dirs, layer_ratio, tidx, n, phase_for_random)
576 |         inp = torch.tensor([ids] * k, device=model.device)
577 |         am = torch.ones_like(inp)
578 |         starts = [steer_B.main_position(ids)] * k       # **主位置**（裁定 D124・詰めは起きない・起点の式は一つ——採否表 P404）
579 |         steer_B.assert_batch_uniform([at] * k, [scenario] * k)
580 |         expected = None if plan is None else {'arm': arm, 'kind': plan['kind'], 'coef': float(coef), 'batch_index': bi}
581 | 
582 |         def _gen(n_rows, seed_value, vecs, row_starts):
583 |             h = None
584 |             try:
585 |                 if plan is not None:
586 |                     h = register_hook(model, layer_idx, make_hook(vecs, coef, plan['sign'], row_starts,
587 |                                                                   meta={'arm': arm, 'kind': plan['kind'], 'batch_index': bi}))
588 |                 assert_hooks_exactly(model, layer_idx if plan is not None else -1, expected)
589 |                 torch.manual_seed(seed_value)
590 |                 x = torch.tensor([ids] * n_rows, device=model.device)
591 |                 with torch.no_grad():
592 |                     return model.generate(input_ids=x, attention_mask=torch.ones_like(x), **gen)
593 |             finally:
594 |                 if h is not None:
595 |                     h.remove()
596 |                     assert_no_hooks(model, layer_idx)
597 |         g1 = _gen(k, batch_seed(cell_seed_value, bi), V, starts)
598 |         P = inp.shape[1]
599 |         first = [_response(g1[j, P:], eos, max_new) for j in range(k)]
600 |         texts1 = [tok.decode(r_, skip_special_tokens=True) for r_, _ in first]
601 |         final_ids = [r_ for r_, _ in first]
602 |         finish = [f_ for _, f_ in first]
603 |         final_text = list(texts1)
604 |         raw_all = list(texts1)
605 |         parsed1 = [sco['parse_app_v2'](t, fam) for t in texts1]
606 |         # **書式外は一度だけ引き直し、最終試行だけを採点する**（凍結走行器と同じ手順・裁定 D117）。
607 |         # 引き直しの種は `runs_B.retry_seed`（正本 seeds.derivation_formula・v5 まで器の中に手書きしていた）。
608 |         need = [j for j, o in enumerate(parsed1) if o is None]
609 |         if need:
610 |             V2 = None if V is None else V[need]
611 |             g2 = _gen(len(need), runs_B.retry_seed(cell_seed_value, bi), V2, [steer_B.main_position(ids)] * len(need))
612 |             for m_, j in enumerate(need):
613 |                 r2, f2 = _response(g2[m_, P:], eos, max_new)
614 |                 t2 = tok.decode(r2, skip_special_tokens=True)
615 |                 final_ids[j], finish[j], final_text[j] = r2, f2, t2
616 |                 raw_all[j] = raw_all[j] + '\n===RETRY===\n' + t2
617 |         # **副位置の活性**（裁定 D132）——生成と同じ hook を掛けたまま、最終試行の応答で一度だけ順伝播する
618 |         rm = [None] * k
619 |         if store_resp:
620 |             lidx = resp_layer_idxs or []
621 |             if not lidx:
622 |                 raise SystemExit('副位置を取る層の添字が要る（resp_layer_idxs・正本 selection.candidates.layers の登録順）')
623 |             hook_args = None if plan is None else {'layer_idx': layer_idx, 'vecs': V, 'coef': coef, 'sign': plan['sign']}
624 |             rm = capture_resp_mean(model, ids, final_ids, lidx, hook_args)
625 |         for j in range(k):
626 |             i = tidx[j]
627 |             s_ = score_text(final_text[j], fam, finish[j], sent, sco, TF, RM)
628 |             tid = '%s__%s__%04d' % (run_key, arm, i)
629 |             if rm[j] is not None:
630 |                 resp[tid] = rm[j]
631 |             trials.append(trial_record(
632 |                 trial_id=tid, trial_index=i, arm=arm, scenario=scenario, tag=tag,
633 |                 status='ok', catastrophe=s_['catastrophe'], choice=s_['choice'], refuse_class=s_['refuse_class'],
634 |                 format_fail=s_['format_fail'], style_a=s_['style_a'], style_b=s_['style_b'], mention=s_['mention'],
635 |                 loop_flag=s_['loop_flag'], truncated=s_['truncated'], correct=None,
636 |                 resp_mean_path=(('resp-%s.npz#%s' % (run_key, tid)) if rm[j] is not None else None),
637 |                 seed=runs_B.recorded_seed(T_, cell_seed_value, i), run_key=run_key, runner_sha=RUNNER_SHA16, arms_spec=arm,
638 |                 preamble_sha=AT[base_arm_of(arm)]['sha16'], model=model_name, sampling=gen,
639 |                 layer=layer_ratio, coef=coef, direction_id=dir_ids[j],
640 |                 batch_pos=j, batch_rows=k, proc_uuid=PROC, dry_run=False))     # **バッチの実際の行数**（採否表 P406）
641 |             raws.append({'trial_id': tid, 'text': raw_all[j], 'final': final_text[j], 'finish': finish[j],
642 |                          'mode': s_['mode'], 'loop_period': s_['loop_period'], 'retry': j in need})
643 |         done += k
644 |     return {'trials': trials, 'raws': raws, 'resp': resp, 'added_norm': added_norm}
645 | 
646 | 
647 | def quality_sampling_record(gen):
648 |     """品質床の試行の記録に書く生成の設定（v8）。`generate` に渡すのは貪欲の鍵（温度を渡さない）だが、記録には正本
649 |     `quality_floor.generation` の温度と top_p を添える——整合検査は記録の温度と top_p を正本の値と照らすので、
650 |     渡した鍵だけを書くと**本物の出力が全件「生成の設定が登録と違う」に落ちる**（合成データは正本の値を書くので通る型）。"""
651 |     g0 = T['quality_floor']['generation']
652 |     return dict(gen, temperature=g0['temperature'], top_p=g0['top_p'])
653 | 
654 | 
655 | def run_quality_cell(model, tok, *, items, arm, stage, task, cell_seed_value, tag, run_key, layer_ratio=None, coef=None,
656 |                      dirs=None, layer_idx=None, input_form='with_preamble', batch=None, start=0):
657 |     """品質床の一つのセル（段 × 腕 × 層 × 係数・一つの課題の断片）を走らせて、試行の記録と生テキストを返す（v8・裁定 D146・2026-09-19）。
658 | 
659 |     items は `qf_task_B.fragment` の返り値（提示の順）。**バッチは断片の順に `runner.batch` 問ずつ前から詰め、左詰め**（`quality_floor.batching`）。
660 |     一つのバッチは一つの腕（裁定 D114）。帯の起点は行ごとの主位置（左詰めなので列の最後の位置・`steer_B.main_position`）。生成は貪欲（`quality_floor.generation`）。
661 |     input_form は 'with_preamble'（土台の前置き ＋ 空行 ＋ 問いの本文・裁定 D138）か 'without_preamble'（問いの本文だけ・判定の順の戻る枝・裁定 D145）。
662 |     例外で落ちたバッチは同じ組で一度だけ引き直し、なお落ちればその行を api_error にする（器の番人の SystemExit は止める）。
663 |     記録（`trial_record_scope`）: 答えの記号は `choice`、正誤は `correct`、書式外は `format_fail`。場面にだけ意味のある欄は空。
664 |     返り値: {'trials': [...], 'raws': [...], 'added_norm': 加えた量のノルム（無操作は None）}。
665 |     """
666 |     import torch
667 |     import qf_task_B
668 |     T_ = T
669 |     if input_form not in ('with_preamble', 'without_preamble'):
670 |         raise SystemExit('品質床の問いの出し方が登録に無い: %s' % input_form)
671 |     batch = batch or T_['runner']['batch']
672 |     gen = dict(steer_B.quality_generation())
673 |     _ge = T_['runner'].get('generation_explicit') or {}
674 |     _na = set(_ge.get('not_applicable') or [])
675 |     _keys = _ge.get('passed_keys')
676 |     if not _keys:
677 |         raise SystemExit('正本 runner.generation_explicit.passed_keys が無い（generate に渡す鍵の一覧・v6）')
678 |     gen.update({k: _ge[k] for k in _keys if k not in _na})
679 |     max_new = int(gen['max_new_tokens'])
680 |     plan = arm_plan(arm)
681 |     if plan is not None and (dirs is None or layer_idx is None):
682 |         raise SystemExit('介入の腕 %s には方向と層の添字が要る' % arm)
683 |     import direction_B
684 |     _nl = len(direction_B.decoder_layers(model))
685 |     if layer_idx is not None and layer_ratio is not None and not layer_binding_ok(layer_ratio, layer_idx, _nl):
686 |         raise SystemExit('層の割合 %s と層の添字 %s が対応しない（総層数 %d なら添字 %d・正本 layer_index_rule・採否表 P393）'
687 |                          % (layer_ratio, layer_idx, _nl, direction_B.layer_index(float(layer_ratio), _nl)))
688 |     added_norm = None if plan is None else float(coef) * float(np.linalg.norm(dirs[('static', layer_ratio)]))
689 |     AT = arm_texts()
690 |     base = base_arm_of(arm)
691 |     at = AT[base]['text'] if input_form == 'with_preamble' else ''
692 |     pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
693 |     if pad_id is None:
694 |         raise SystemExit('トークナイザに詰めのトークンが無い（左詰めにできない）')
695 |     eos = _eos_ids(model, tok)
696 |     model_name = getattr(getattr(model, 'config', None), '_name_or_path', None)
697 |     rec_sampling = quality_sampling_record(gen)
698 |     n = len(items)
699 |     trials, raws = [], []
700 |     done = 0
701 |     # **バッチの区切りは断片の頭（試行の番号 零）から数えた倍数**（場面の試行と同じ・再開しても同じ問いは同じバッチに入る）
702 |     while start + done < n:
703 |         i0 = start + done
704 |         bi = i0 // batch
705 |         k = min((bi + 1) * batch, n) - i0
706 |         tidx = list(range(i0, i0 + k))
707 |         its = [items[i] for i in tidx]
708 |         rows = [steer_B.apply_chat(tok, user_message(at, qf_task_B.block(it), '')) for it in its]
709 |         P = max(len(r_) for r_ in rows)
710 |         pads = [P - len(r_) for r_ in rows]
711 |         inp = torch.full((k, P), int(pad_id), dtype=torch.long, device=model.device)
712 |         am = torch.zeros_like(inp)
713 |         for r_, (row, pd) in enumerate(zip(rows, pads)):
714 |             inp[r_, pd:] = torch.tensor(row, dtype=torch.long, device=model.device)
715 |             am[r_, pd:] = 1
716 |         starts = [steer_B.main_position(row, pd) for row, pd in zip(rows, pads)]      # **主位置**（左詰めなので全行が列の最後・起点の式は一つ）
717 |         if any(s_ != P - 1 for s_ in starts):
718 |             raise SystemExit('左詰めの主位置が列の最後にない: %s（正本 runner.padding）' % starts)
719 |         V, dir_ids = row_vectors(plan, dirs, layer_ratio, tidx, n, 'main')            # 品質床は main の方向（§2.8 の相ごとの方向）
720 |         expected = None if plan is None else {'arm': arm, 'kind': plan['kind'], 'coef': float(coef), 'batch_index': bi}
721 | 
722 |         def _gen():
723 |             h = None
724 |             try:
725 |                 if plan is not None:
726 |                     h = register_hook(model, layer_idx, make_hook(V, coef, plan['sign'], starts,
727 |                                                                   meta={'arm': arm, 'kind': plan['kind'], 'batch_index': bi}))
728 |                 assert_hooks_exactly(model, layer_idx if plan is not None else -1, expected)
729 |                 torch.manual_seed(batch_seed(cell_seed_value, bi))
730 |                 with torch.no_grad():
731 |                     return model.generate(input_ids=inp, attention_mask=am, pad_token_id=int(pad_id), **gen)
732 |             finally:
733 |                 if h is not None:
734 |                     h.remove()
735 |                     assert_no_hooks(model, layer_idx)
736 |         g, err = None, None
737 |         for _attempt in (1, 2):                    # **一度だけ引き直す**（quality_floor.format_fail_rule・batching）
738 |             try:
739 |                 g = _gen()
740 |                 break
741 |             except Exception as e:                 # 器の番人（SystemExit）はここを通らずに止まる
742 |                 err = '%s: %s' % (type(e).__name__, str(e)[:160])
743 |                 if torch.cuda.is_available():
744 |                     torch.cuda.empty_cache()
745 |         for j in range(k):
746 |             i, it = tidx[j], its[j]
747 |             if g is not None:
748 |                 resp, fin = _response(g[j, P:], eos, max_new)
749 |                 text = tok.decode(resp, skip_special_tokens=True)
750 |                 letter = qf_task_B.extract_letter(text, qf_task_B.letters_of(it))
751 |                 ff = letter is None
752 |                 correct = steer_B.score_quality(letter, it['answer'], ff)
753 |                 status = 'ok'
754 |             else:
755 |                 text, fin, letter, ff, correct, status = None, None, None, None, None, 'api_error'
756 |             tid = '%s__%s__%04d' % (run_key, arm, i)
757 |             trials.append(trial_record(
758 |                 trial_id=tid, trial_index=i, arm=arm, scenario=task, tag=tag, status=status,
759 |                 catastrophe=None, choice=letter, refuse_class=None, format_fail=ff, style_a=None, style_b=None, mention=None,
760 |                 loop_flag=None, truncated=(None if fin is None else fin == 'length'), correct=correct, resp_mean_path=None,
761 |                 layer=layer_ratio, coef=coef, direction_id=dir_ids[j], seed=runs_B.recorded_seed(T_, cell_seed_value, i),
762 |                 batch_pos=j, batch_rows=k, run_key=run_key, proc_uuid=PROC, runner_sha=RUNNER_SHA16, arms_spec=arm,
763 |                 preamble_sha=(AT[base]['sha16'] if input_form == 'with_preamble' else None), model=model_name, sampling=rec_sampling,
764 |                 dry_run=False))
765 |             raws.append({'trial_id': tid, 'item_id': it['id'], 'text': text, 'finish': fin, 'error': err if g is None else None,
766 |                          'stage': stage, 'input_form': input_form})
767 |         done += k
768 |     return {'trials': trials, 'raws': raws, 'added_norm': added_norm}
769 | 
770 | 
771 | def manifest_env(model, tok):
772 |     """manifest の環境の欄のうち、走行器が知っているもの（正本 `runner.manifest_fields.common`・v5）。残り（セッション・時刻・pip の SHA など）は起動器が足す。"""
773 |     import transformers
774 |     cfg = getattr(model, 'config', None)
775 |     return {'model': getattr(cfg, '_name_or_path', None), 'model_rev': getattr(cfg, '_commit_hash', None),
776 |             'tokenizer_rev': getattr(tok, 'init_kwargs', {}).get('_commit_hash') or getattr(tok, 'name_or_path', None),
777 |             'dtype': T['runner']['dtype'], 'order': T['runner']['order_id'], 'padding': 'left', 'batch': T['runner']['batch'],
778 |             'transformers_version': transformers.__version__, 'refuse_rules_sha16': runs_B.sha16_file(REFUSE_RULES),
779 |             'runner_sha': RUNNER_SHA16}
780 | 
781 | 
782 | def write_cell(out_root, tag, run_key, manifest, trials, raws=None, resp=None):
783 |     """一つの走行の記録を**置き場に書く**（裁定 D117・2026-09-19）。
784 | 
785 |     置き方は合成データ（`synth_B.write_run`）と同じにし、読み口（`runs_B`）と整合検査がそのまま読めるようにする。
786 |     **既にある置き場には書かない**（上書きで記録を失わない）。生テキストと副位置の活性も書く（v5）。
787 |     """
788 |     import datetime as _dt
789 |     d = os.path.join(out_root, tag, run_key)
790 |     if os.path.exists(os.path.join(d, 'manifest.json')):
791 |         raise SystemExit('既に記録がある（上書きしない）: %s' % d)
792 |     os.makedirs(d, exist_ok=True)
793 |     phase = next(k for k, v in T['tags'].items() if v == tag)
794 |     need = list((T['runner'].get('manifest_fields') or {}).get('common', [])) + \
795 |         list((T['runner'].get('manifest_fields') or {}).get(phase, []))
796 |     missing = [k for k in need if k not in manifest]
797 |     if missing:
798 |         raise SystemExit('manifest に正本の欄が無い（正本 runner.manifest_fields）: %s' % '・'.join(missing))
799 |     if raws is not None and len(raws) != len(trials):
800 |         raise SystemExit('生テキストの行数（%d）が試行の数（%d）と違う' % (len(raws), len(trials)))
801 |     json.dump(dict(manifest, written=_dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')),
802 |               open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
803 |     with open(os.path.join(d, 'trials-%s.jsonl' % run_key), 'w', encoding='utf-8', newline='\n') as f:
804 |         for t in trials:
805 |             f.write(json.dumps(t, ensure_ascii=False) + '\n')
806 |     with open(os.path.join(d, 'raw-%s.jsonl' % run_key), 'w', encoding='utf-8', newline='\n') as f:
807 |         for t, r in zip(trials, raws or [None] * len(trials)):
808 |             f.write(json.dumps(r if isinstance(r, dict) else {'trial_id': t['trial_id'], 'text': r}, ensure_ascii=False) + '\n')
809 |     if resp:
810 |         np.savez(os.path.join(d, 'resp-%s.npz' % run_key), **resp)
811 |     return d
812 | 
813 | 
814 | def write_session(out_root, tag, session, run_keys, extra=None):
815 |     """セッション記録を書く（正本 `sessions.record`・`sessions.fields`）。門・集計器・整合検査が読む（裁定 D126）。"""
816 |     d = os.path.join(out_root, 'sessions-B')
817 |     os.makedirs(d, exist_ok=True)
818 |     rec = dict({'tag': tag, 'session': int(session), 'run_keys': list(run_keys), 'batch': T['runner']['batch']}, **(extra or {}))
819 |     p = os.path.join(d, '%s__s%d.json' % (tag, int(session)))
820 |     if os.path.exists(p):
821 |         old = json.load(open(p, encoding='utf-8'))
822 |         rec['run_keys'] = sorted(set(old.get('run_keys', [])) | set(rec['run_keys']))
823 |     json.dump(rec, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
824 |     return p
825 | 
826 | 
827 | if __name__ == '__main__':
828 |     ap = argparse.ArgumentParser()
829 |     ap.add_argument('--selftest', action='store_true')
830 |     ap.add_argument('--phase', choices=['identity', 'tune', 'quality', 'main'], default=None)
831 |     ap.add_argument('--scenario', default=None)
832 |     ap.add_argument('--session', type=int, default=1)
833 |     ap.add_argument('--directions', default=None, help='direction_B.py が凍結した方向（npz）')
834 |     ap.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
835 |     ap.add_argument('--out-root', default=None)
836 |     a = ap.parse_args()
837 |     if a.selftest:
838 |         _selftest()
839 |         sys.exit(0)
840 |     check_assembly_matches_frozen()
841 |     try:
842 |         import torch
843 |         from transformers import AutoModelForCausalLM, AutoTokenizer
844 |     except Exception as e:
845 |         sys.exit('torch／transformers が無い: %s（この器は GPU の上で走らせる。手元の検査は --selftest）' % e)
846 |     if not a.directions:
847 |         sys.exit('--directions（tools/direction_B.py が凍結した npz）が要る')
848 |     import direction_B
849 |     tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or a.model)
850 |     tok.padding_side = 'left'                                   # 正本 runner.padding
851 |     model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.bfloat16, device_map='auto')
852 |     model.eval()
853 |     dirs, dmeta = load_directions(a.directions, os.path.splitext(a.directions)[0] + '.json')
854 |     n_layers = model.config.num_hidden_layers
855 |     if dmeta.get('num_hidden_layers') not in (None, n_layers):
856 |         sys.exit('方向を抽出した機種の総層数（%s）が、いまの機種（%s）と違う' % (dmeta.get('num_hidden_layers'), n_layers))
857 |     print('[run_stageB_local] 方向を読んだ（%d 本・総層数 %d）。走らせる相・セルは起動器（まだ書いていない）から渡す。'
858 |           % (len(dirs), n_layers))
859 |     print('[run_stageB_local] 一つのセルを走らせるには `run_cell(...)` を呼ぶ（正本 selection.batch_composition のとおり'
860 |           '一つのバッチは一つの場面 × 一つの腕）。')
861 |     sys.exit(0)
```
<<< 終: `tools/run_stageB_local.py` >>>

<<< 始: `tools/steer_B.py`（SHA16 71157C6921E12AC7・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """steer_B.py v6 —— 段階 B の**介入**（方向の加減・ランダム方向・品質床の生成と採点）。
  3 | v6（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: ランダム方向の割り当てを**交互**（試行の番号を方向の数で割った余り）にした（裁定 D140）。帯の起点（主位置）を**一つの関数 `main_position`** から出し、走行器がそれを呼び、自己検査がそれを検べる（採否表 P404）。
  4 | 
  5 | 正本 `design/contrasts-B.json` の `selection.apply`・`random_control`・`quality_floor`・`runner` に従う。
  6 | 規則（この器が守るもの）:
  7 |   - 加減は `h ← h ± α·v̂`（**主位置〔組み立て済みの列の最後のトークン〕から EOS まで**・`register_forward_hook`・`selection.apply`・裁定 D124）。α は**その層の v̂ のノルムに対する比**。
  8 |   - すべての方向（v̂・Nk・td・(6b)・ランダム方向）を**係数を掛ける前の ‖v̂〔static〕‖** に合わせ、**係数は加減のときに一度だけ**掛ける（裁定 D75・D90）。
  9 |     自己検査は「**全方向 × 全係数 × 全層**で加わる量のノルムが一致する」ことを確かめる（裁定 D102——前は v 腕とランダム腕の対しか回さず、交差族に同じ穴が残った）。
 10 |   - 介入の帯の起点は、**chat template を当てた組み立て済みの列の最後のトークン（主位置）**（裁定 D101 で template を当て、裁定 D124 で起点を主位置にした）。
 11 |     自己検査は起点を**独立の正解**（器を通さずに作った列の最後の位置）と照らし、復号して最終トークンと一致することを見る
 12 |     （`OP4B_TOKENIZER_DIR` に実トークナイザの置き場を渡したときに走る。**`OP4B_REQUIRE_FULL_SELFTEST=1` なら、飛ばすと失敗に倒す**・裁定 D122）。
 13 |     関数の名 `scenario_start_index` は裁定 D124 の前の名残で、返すのは主位置である。**起点の式は `main_position` 一つ**で、走行器もこれを呼ぶ（採否表 P404）。
 14 |   - ランダム方向は**調整走行と本走行で引き直す**（裁定 D84・種は `seeds.random_dirs` の tune と main）。
 15 |   - 一腕の試行の方向は**試行の番号を方向の数で割った余り**（交互・`random_control.allocation`・裁定 D140・調整走行にも当てる）。各方向の数は登録順の等分（端数は登録順に一つずつ）と同じ。
 16 |   - 品質床は**貪欲**（`quality_floor.generation`）で、**生成した文字列から記号を読み取る**（強制デコードは採らない・裁定 D120）。書式外は不正解に数え、api_error は一度だけ引き直す（`quality_floor.format_fail_rule`）。
 17 |   - 場面の試行は `runner.generation` の設定。詰めは左（`runner.padding`）。
 18 | **この器は GPU の上でしか本走行できない。** 手元では `--selftest`（ノルム合わせ・割り当て・引き直し・種の再現を合成のベクトルで確かめる）が走る。
 19 | 用法: python tools/steer_B.py --selftest
 20 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 21 | """
 22 | import os, sys, json, argparse
 23 | sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 24 | import numpy as np
 25 | import runs_B
 26 | 
 27 | VERSION = 'v6'
 28 | STRICT = os.environ.get('OP4B_REQUIRE_FULL_SELFTEST') == '1'     # 実機の段では飛ばしを失敗に倒す（裁定 D122・採否表 P344）
 29 | REPO = runs_B.REPO
 30 | T = runs_B.load_T()
 31 | RC = T['random_control']
 32 | N_RAND = RC['count']
 33 | 
 34 | 
 35 | def random_directions(v_hat_static, phase, layer_ratio, count=N_RAND):
 36 |     """層ごとに count 本のランダム方向を引き、**係数を掛ける前の ‖v̂〔static〕‖** に合わせる（裁定 D90・2026-09-18）。
 37 | 
 38 |     係数は加減のときに一度だけ掛ける（`apply_vector`・`selection.apply`）。基準は**静的 v̂ ひとつ**で、族を跨いで変えない（裁定 D75）。
 39 |     phase は 'tune' か 'main'（裁定 D84・種を分けて引き直す）。子ストリームは**層ごと**（正本 `random_control.per_layer`・係数は入れない・採否表 P285）。"""
 40 |     assert phase in ('tune', 'main'), '相は tune か main（裁定 D84）'
 41 |     seed = RC['seed'][phase]
 42 |     d = int(np.asarray(v_hat_static).shape[-1])
 43 |     ss = np.random.SeedSequence([seed, int(round(layer_ratio * 1000))])
 44 |     rng = np.random.default_rng(ss)
 45 |     target = float(np.linalg.norm(v_hat_static))
 46 |     out = []
 47 |     for i in range(count):
 48 |         g = rng.normal(size=d)
 49 |         n = float(np.linalg.norm(g))
 50 |         out.append(g * (target / n) if n else g)
 51 |     return out
 52 | 
 53 | 
 54 | def match_to_static(v, v_hat_static):
 55 |     """どの方向（Nk・td・(6b)）も、加える前に ‖v̂〔static〕‖ に合わせる（裁定 D75・D90）。"""
 56 |     n = float(np.linalg.norm(v))
 57 |     return v * (float(np.linalg.norm(v_hat_static)) / n) if n else v
 58 | 
 59 | 
 60 | def allocate(n_trials, count=N_RAND):
 61 |     """各方向の試行の数（登録順に等分し、端数は登録順に一つずつ）。交互の割り当て（`direction_of`）の数と一致する（random_control.allocation）。"""
 62 |     base, rem = divmod(int(n_trials), int(count))
 63 |     return [base + (1 if i < rem else 0) for i in range(count)]
 64 | 
 65 | 
 66 | def direction_of(trial_index, n_trials, count=N_RAND):
 67 |     """試行の番号から方向の添字を決める——**試行の番号を方向の数で割った余り（交互）**（正本 `random_control.allocation`・裁定 D140）。
 68 | 
 69 |     試行の番号だけで決まるので**再開しても変わらない**（採否表 P298）。各方向の数は `allocate` と一致する。
 70 |     前は登録順の連続した塊に割っており、方向がバッチ・時刻・セッションと交絡した（採否表 P398）。"""
 71 |     if not 0 <= int(trial_index) < int(n_trials):
 72 |         raise ValueError('試行の番号が全体の数の外にある: %s / %s' % (trial_index, n_trials))
 73 |     return int(trial_index) % int(count)
 74 | 
 75 | 
 76 | def apply_vector(h, v_hat, coef, sign):
 77 |     """h ← h ± α·v̂（α は v̂ のノルムに対する比なので、掛けるのは coef·v̂）。"""
 78 |     assert sign in (+1, -1)
 79 |     return h + sign * coef * np.asarray(v_hat)
 80 | 
 81 | 
 82 | def apply_chat(tokenizer, user_message):
 83 |     """**段階 B は chat template を当てる**（正本 `runner.chat_template`・裁定 D101）。組み立て済みのトークン列を返す。"""
 84 |     return list(tokenizer.apply_chat_template([{'role': 'user', 'content': user_message}],
 85 |                                               add_generation_prompt=True, tokenize=True))
 86 | 
 87 | 
 88 | def main_position(ids, pad_len=0):
 89 |     """**介入の帯の起点＝主位置（組み立て済みの列の最後のトークン）**の添字（正本 `selection.apply`・裁定 D124）。**起点の式はこの一つ**（採否表 P404）。
 90 | 
 91 |     ids は組み立て済みのトークン列（chat template を当てたもの）。pad_len は左詰めの詰めの長さ——詰めを入れた列の中でも最終トークンを指す。
 92 |     走行器（`run_stageB_local.run_cell`・`capture_resp_mean`）と `scenario_start_index` がこれを呼び、自己検査がこれを独立の正解と照らす。"""
 93 |     return int(pad_len) + len(ids) - 1
 94 | 
 95 | 
 96 | def scenario_start_index(tokenizer, arm_text, scen_text, instruction, pad_len=0):
 97 |     """介入の帯の**起点**＝**主位置（プロンプトの最終トークン）**（正本 `selection.apply`・裁定 D124・2026-09-18）。
 98 | 
 99 |     裁定 D124 で帯を「場面本文の開始から」ではなく「主位置から EOS まで」に狭めた。
100 |     抽出した場所と加える場所を一致させるためであり、**狭めて落ちるのは prefill の場面本文の位置だけ**
101 |     （選択が作られる復号の段はすべて掛かる）。
102 |     左詰めのバッチでは、詰めの長さに関わらず**最終トークンは列の最後の位置**にある。
103 |     pad_len は左詰めの詰めの長さ（この式では結果に効かないが、呼び手の意図を明示するために受ける）。
104 |     """
105 |     ids = apply_chat(tokenizer, _user_message(arm_text, scen_text, instruction))
106 |     return main_position(ids, pad_len)
107 | 
108 | 
109 | def _user_message(arm_text, scen_text, instruction):
110 |     """凍結走行器 `user_message` と同じ式（正本 `runner.prompt_assembly`）。"""
111 |     t = arm_text or ''
112 |     return (t + '\n\n' + scen_text + instruction) if t else (scen_text + instruction)
113 | 
114 | 
115 | def band_starts(tokenizer, arm_texts, scen_text, instruction, pad_lens):
116 |     """バッチの行ごとの起点（`make_hook` に渡す）。
117 | 
118 |     正本 `selection.batch_composition` により**一つのバッチは一つの場面 × 一つの腕**なので、
119 |     詰めは起きず、全行が同じ起点になる。式は一般のまま置き、器が取り決めを守っているかを
120 |     `assert_batch_uniform` で確かめる。
121 |     """
122 |     return [scenario_start_index(tokenizer, t, scen_text, instruction, p) for t, p in zip(arm_texts, pad_lens)]
123 | 
124 | 
125 | def assert_batch_uniform(arm_texts, scenarios=None):
126 |     """**一つのバッチは一つの場面 × 一つの腕**（正本 `selection.batch_composition`・裁定 D124）。"""
127 |     if len(set(arm_texts)) > 1:
128 |         raise SystemExit('バッチに複数の腕が混ざっている（正本 selection.batch_composition・裁定 D124）: %d 種'
129 |                          % len(set(arm_texts)))
130 |     if scenarios is not None and len(set(scenarios)) > 1:
131 |         raise SystemExit('バッチに複数の場面が混ざっている（正本 selection.batch_composition・裁定 D124）: %d 種'
132 |                          % len(set(scenarios)))
133 | 
134 | 
135 | def _to_hf(g, greedy):
136 |     """正本の生成の設定を transformers の引数名に写す（説明の欄は落とす・採否表 P286）。"""
137 |     out = {'max_new_tokens': g.get('max_tokens')}
138 |     if greedy:
139 |         out['do_sample'] = False
140 |     else:
141 |         out.update({'do_sample': True, 'temperature': g.get('temperature'), 'top_p': g.get('top_p')})
142 |     return {k: v for k, v in out.items() if v is not None}
143 | 
144 | 
145 | def quality_generation():
146 |     """品質床の生成の設定（**貪欲**・正本 quality_floor.generation・裁定 D78）。"""
147 |     g = T['quality_floor']['generation']
148 |     assert g['temperature'] == 0, '品質床は貪欲（temperature 零）でなければならない（裁定 D78）'
149 |     if g.get('max_tokens') is None:      # **黙って落とさない**（裁定 D103・採否表 P328）
150 |         raise SystemExit('品質床の最大トークン数が未定（裁定 D66 と採否表 P216 で決める）。'
151 |                          'このまま実機に渡すと transformers の既定で走り、例外も警告も出ない')
152 |     return _to_hf(g, greedy=True)
153 | 
154 | 
155 | def main_generation():
156 |     """場面の試行の生成の設定（正本 runner.generation）。"""
157 |     return _to_hf(T['runner']['generation'], greedy=False)
158 | 
159 | 
160 | def score_quality(answer_letter, correct_letter, format_fail):
161 |     """品質床の採点（書式外は不正解に数えて分母を保つ・quality_floor.format_fail_rule）。"""
162 |     if format_fail or not answer_letter:
163 |         return False
164 |     return answer_letter.strip().upper() == correct_letter.strip().upper()
165 | 
166 | 
167 | def _selftest():
168 |     rng = np.random.default_rng(3)
169 |     v = rng.normal(size=32)
170 |     nv = float(np.linalg.norm(v))
171 |     # (1) ランダム方向は ‖v̂‖ に合う（係数は掛けない・裁定 D90）
172 |     for ratio in T['selection']['candidates']['layers']:
173 |         rs = random_directions(v, 'main', ratio)
174 |         assert len(rs) == N_RAND
175 |         for r in rs:
176 |             assert abs(float(np.linalg.norm(r)) - nv) < 1e-9, 'ランダム方向のノルムが ‖v̂‖ に合っていない（裁定 D90）'
177 |     # (2) **合成の検査**（裁定 D102・採否表 P309・P311）: 加わる量のノルムが
178 |     #     **全方向（v̂・Nk・td・(6b)・ランダム方向） × 全係数 × 全層**で一致する。
179 |     #     前は v 腕とランダム腕の対しか回さなかったため、交差族と S4 の反証に同じ穴が残った。
180 |     raw = {'Nk': rng.normal(size=32) * 7.0, 'td': rng.normal(size=32) * 0.2, 'loaded': rng.normal(size=32) * 3.5}
181 |     others = {k: match_to_static(w, v) for k, w in raw.items()}      # 方向を作る器が合わせたものを模す
182 |     n_checked = 0
183 |     for coef in T['selection']['candidates']['coefficients']:
184 |         for ratio in T['selection']['candidates']['layers']:
185 |             a_v = np.linalg.norm(apply_vector(np.zeros(32), v, coef, +1))
186 |             cand = dict(others)
187 |             for i, r in enumerate(random_directions(v, 'main', ratio)):
188 |                 cand['rand:%d' % i] = r
189 |             for name, w in cand.items():
190 |                 a_w = np.linalg.norm(apply_vector(np.zeros(32), w, coef, +1))
191 |                 assert abs(a_v - a_w) < 1e-9, ('加わる量が v 腕と %s で違う（係数が二度掛かっていないか）' % name, coef, ratio, a_v, a_w)
192 |                 n_checked += 1
193 |     assert n_checked == len(T['selection']['candidates']['coefficients']) * len(T['selection']['candidates']['layers']) * (len(raw) + N_RAND)
194 |     # (3) 合わせる器そのもの
195 |     assert abs(float(np.linalg.norm(match_to_static(rng.normal(size=32) * 7.0, v))) - nv) < 1e-9
196 |     # (4) 引き直し（裁定 D84）と層ごとの子ストリーム（係数は入れない・採否表 P285）
197 |     a1 = random_directions(v, 'tune', 0.5)[0]
198 |     a2 = random_directions(v, 'main', 0.5)[0]
199 |     assert not np.allclose(a1, a2), '調整走行と本走行で引き直していない'
200 |     assert np.allclose(a1, random_directions(v, 'tune', 0.5)[0]), '同じ引数で再現しない'
201 |     assert not np.allclose(random_directions(v, 'main', 0.25)[0], random_directions(v, 'main', 0.75)[0]), '層で子ストリームが分かれていない'
202 |     # (5) 割り当てと、試行の番号から方向へ（**交互**・裁定 D140・再開しても変わらない・採否表 P298）
203 |     for n in (200, 201, 100, 7):
204 |         al = allocate(n)
205 |         assert sum(al) == n and max(al) - min(al) <= 1 and al == sorted(al, reverse=True), '割り当ての端数の配り方が規則と違う'
206 |     n = T['n_main']
207 |     got = [direction_of(i, n) for i in range(n)]
208 |     assert [got.count(i) for i in range(N_RAND)] == allocate(n), '試行から方向への写像が割り当てと合わない'
209 |     assert [direction_of(i, n) for i in range(n // 2, n)] == got[n // 2:], '再開すると方向の割り当てが変わる'
210 |     # **交互であること**を、器を通さずに作った正解（番号を方向の数で割った余り）と照らす——塊に戻すとここで落ちる
211 |     assert got[:2 * N_RAND] == [i % N_RAND for i in range(2 * N_RAND)], ('割り当てが交互でない（裁定 D140）', got[:2 * N_RAND])
212 |     _bt = T['runner']['batch']
213 |     assert all(len({got[j] for j in range(b, min(b + _bt, n))}) == min(N_RAND, min(b + _bt, n) - b) for b in range(0, n, _bt)), \
214 |         'バッチの中に方向が混ざっていない（塊の割り当てに戻っている）'
215 |     # (5b) **帯の起点の関数**（採否表 P404）——器を通さずに作った正解（列の最後の位置）と照らす。詰めを入れても最終トークンを指す
216 |     for ids_ in ([5, 6, 7], [9], list(range(40))):
217 |         assert main_position(ids_) == len(ids_) - 1, ('起点が列の最後でない', ids_[:4], main_position(ids_))
218 |         for pad in (0, 3, 11):
219 |             padded = [0] * pad + list(ids_)
220 |             assert padded[main_position(ids_, pad)] == ids_[-1] and main_position(ids_, pad) == len(padded) - 1, ('詰めを入れると起点がずれる', pad)
221 |     # (6) 加減の向き
222 |     h = rng.normal(size=32)
223 |     assert np.allclose(apply_vector(h, v, 2.0, +1) - h, 2.0 * v)
224 |     assert np.allclose(apply_vector(h, v, 0.5, -1) - h, -0.5 * v)
225 |     # (7) 品質床の採点と生成（transformers の引数名で出す・採否表 P286）
226 |     assert score_quality('A', 'a', False) and not score_quality('A', 'B', False) and not score_quality('A', 'A', True)
227 |     try:
228 |         qg = quality_generation()
229 |     except SystemExit as e:
230 |         qg = None
231 |         assert '最大トークン数' in str(e), '品質床の生成の設定が、別の理由で止まっている: %s' % e
232 |     mg = main_generation()
233 |     if qg is not None:
234 |         assert qg['do_sample'] is False and 'temperature' not in qg, '品質床が貪欲でない'
235 |         assert 'max_new_tokens' in qg, '品質床の最大トークン数が黙って落ちている（裁定 D103）'
236 |     assert set(mg) <= {'do_sample', 'temperature', 'top_p', 'max_new_tokens'}, '生成の設定に transformers が知らない鍵が混ざる'
237 |     assert mg['max_new_tokens'] == T['runner']['generation']['max_tokens'] and mg['temperature'] == T['runner']['generation']['temperature']
238 |         # (8) **帯の起点**（裁定 D101・採否表 P308）: 実トークナイザがあれば、起点のトークンを復号して場面本文の先頭に一致することを確かめる
239 |     band = _selftest_band()
240 |     print('[steer_B selftest] 全方向 × 全係数 × 全層の合成 %d 通り・引き直し・層の子ストリーム・割り当て（交互）と再開・帯の起点の関数・加減の向き・生成の設定・%s: すべて通った'
241 |           % (n_checked, band))
242 | 
243 | 
244 | def _selftest_band(model_dir=None):
245 |     """帯の起点の自己検査（正本 `runner.chat_template`・`selection.apply`・裁定 D122）。
246 | 
247 |     **独立の正解と照らす**（裁定 D122）——起点を求めるのに使った経路とは別に、
248 |     組み立て済みの列を自分で作って最後の位置を取り、二つが一致することを確かめる。
249 |     さらに、その位置のトークンを**復号して**、組み立て済みの列の最終トークンと文字列で一致することを見る。
250 |     左詰めのバッチでも、詰めを入れた列の中で同じ位置が最終トークンを指すことを確かめる。
251 |     前の版は、起点を探すのに使ったトークンでそのまま照合していたので**恒真**だった。
252 |     """
253 |     try:
254 |         from transformers import AutoTokenizer
255 |     except Exception:
256 |         if STRICT:
257 |             raise SystemExit('帯の起点の検査を飛ばした（transformers が無い）——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
258 |         return '帯の起点（**飛ばした**——transformers が無い）'
259 |     src = model_dir or os.environ.get('OP4B_TOKENIZER_DIR')
260 |     if not src:
261 |         if STRICT:
262 |             raise SystemExit('帯の起点の検査を飛ばした（OP4B_TOKENIZER_DIR が無い）——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
263 |         return '帯の起点（**飛ばした**——OP4B_TOKENIZER_DIR が無い）'
264 |     tok = AutoTokenizer.from_pretrained(src)
265 |     scen, inst = '場面の本文がここから始まる。', '\n\n指示。'
266 |     n_ok = 0
267 |     for arm_text in ('前置きがここにある。', ''):
268 |         ids = apply_chat(tok, _user_message(arm_text, scen, inst))
269 |         want = len(ids) - 1                                   # **独立の正解**（器を通さずに作る）
270 |         got = scenario_start_index(tok, arm_text, scen, inst, 0)
271 |         assert got == want, ('起点が独立の正解と違う', arm_text[:8], got, want)
272 |         assert tok.decode([ids[got]]) == tok.decode([ids[-1]]), '起点のトークンが最終トークンでない'
273 |         for pad in (0, 5, 37):                                # 左詰めの詰めを入れても最終トークンを指すか
274 |             padded = [tok.pad_token_id or 0] * pad + ids
275 |             st = scenario_start_index(tok, arm_text, scen, inst, pad)
276 |             assert padded[st] == ids[-1], ('詰めを入れると起点がずれる', pad, st)
277 |         n_ok += 1
278 |     assert_batch_uniform(['a', 'a', 'a'])
279 |     try:
280 |         assert_batch_uniform(['a', 'b'])
281 |         raise AssertionError('腕が混ざったバッチを止めていない（裁定 D124）')
282 |     except SystemExit:
283 |         pass
284 |     return '帯の起点（実トークナイザ・独立の正解と照合・詰め三通り・腕の混在を止めることも確かめた）'
285 | 
286 | 
287 | if __name__ == '__main__':
288 |     ap = argparse.ArgumentParser()
289 |     ap.add_argument('--selftest', action='store_true')
290 |     a = ap.parse_args()
291 |     if a.selftest:
292 |         _selftest()
293 |         sys.exit(0)
294 |     sys.exit('この器は GPU の上の走行器から import して使う（手元の検査は --selftest）。'
295 |              '走行の組み立て（場面の本文・hook の登録・バッチ）は走行器 `tools/run_stageB_local.py` の側にある。')
```
<<< 終: `tools/steer_B.py` >>>
