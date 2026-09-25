（B-lens 層三の器の直しの確かめの束・分けた版 6／7・中身は一通版と同じ）

==================== 第八部 合成データの器と、合成データの正式の記録と、試しの九度目の記録と、器の段の記録 ====================

<<< 始: `tools/dry_run_Bl3.py`（SHA16 5FF650A8B106834D・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """dry_run_Bl3.py v3 —— B-lens 層三（Bl3）の合成データの器（正本 `review_plan.synthetic` の形のすべてと、乱数の小さな模型で端から端まで・2026-09-25）。
  3 | 
  4 | 一. 純粋な関数の形（`tools/bl3_core.py`・`tools/blens_core.py`・`tools/analyze_Bl3.py`）: 奇でない押し・零でない帰無の中心・減算の行・下見で外れる升目と門の行だけの升目・
  5 |     帰無との同じ値・両方の向きがちょうど対称な比べる相手・掃き出し・端数のバッチ・零の近くの中央値・Holm の境で一本違う p・器の誤りでやり直す流れ・
  6 |     札の一致の中身（裁定 D232）・下見で外した後の偶然の目安（裁定 D231）・比べる相手の除き方の錨（裁定 D231）。
  7 | 二. 乱数の小さな模型（登録機種の設定を小さくした bf16 の模型・実の重みではない・正規化の重みを散らす・CPU）と実のトークナイザで、走らせる器 `tools/bl3_run.py` の
  8 |     下見と本の計算（近道を使わない・裁定 D234）と、独立の再計算の二つの道（本の器のフックと、別の個体の残差の書き換えの器）を、等方は `--iso` の本数で通す。
  9 |     書き出しの割り方が変わる場合（器が止まるか）。二段の判定の形（一段目は無操作の値も比べる・裁定 D233・二段目は札の一致で判定する・裁定 D234）を、値をわざと
 10 |     ずらした写しで確かめる。下見の分かれ道（主の升目と門の行だけの升目を外した記録・バッチ一の記録・意見伺いの C1-C1・C2-A4）を、作った下見の記録で、
 11 |     本の計算 → 二つの道 → 一致だけを見る段 → 結果を開く段 → 掃き出し → 報告の組み立て → 走査まで、起動器の出力と同じ JSON の往復を通して流す（等方は `--e2e-iso` の本数）。
 12 |     近道の確かめのバッチ一の枝は、本の計算が近道を使わない（裁定 D234）ので無い。
 13 | 三. わざと壊した読み取り（二重の正規化）と近道の元（主位置まで使い回す・記録した切れ目を偽る）で、自己検査と凍結した確かめが止まることを確かめる。
 14 |     本物の相対の加減の大きさにそろえた合成の方向で、書き換えの道の変種・主位置の一つ分の寄与・二段目の本の道とフックの差（意見伺いの C2-3.2）を記述として測る。
 15 | 四. 別の個体の書き換えの器（`tools/bl3_recompute_rewrite.py`・中は変えない）の自己検査と `--dry` を今の本の器の上で走らせ、出力を記録に写す。
 16 | 五. 起動器の三つの相を DRY で別のプロセスとして走らせ、集計の器の CLI（一致だけを見る段・結果を開く段）と掃き出しと報告の組み立てに通す。一致だけを見る段の後に組の出力を
 17 |     差し替えると、結果を開く段が止まることを確かめる（裁定 D236）。
 18 | v3（裁定 D236）で足した確かめ: 本の計算が近道を使わないことの振る舞い・正本の文から独立に書いた札と、答えの分かる合成での門の組み立て・等方の外の行が出る枝・
 19 |     有限でない値の止め・結果を開く段の結びつき。
 20 | 記録の末尾に、走らせた器（凍結の器の一覧と import の閉包）と正本・設計事実・方向の記録の SHA16 を、走りの始めと終わりで同じことを確かめて並べる
 21 | （下見の前の凍結の器が今の版と突き合わせる）。
 22 | **実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の方向は、実の方向の名だけを借りた乱数（次元は小さな模型のもの）。
 23 | 出力: records/Bl3/dry-run-Bl3-<日付>.md（--force が無ければ上書きしない）
 24 | 用法: python tools/dry_run_Bl3.py [--force] [--iso 本数（既定は正本の本数）] [--e2e-iso 本数（既定 9）] [--out 置き場]
 25 | 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 26 | """
 27 | import os, re, sys, glob, json, math, time, copy, shutil, hashlib, argparse, datetime, tempfile, subprocess, collections
 28 | import numpy as np
 29 | 
 30 | HERE = os.path.dirname(os.path.abspath(__file__))
 31 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 32 | sys.path.insert(0, HERE)
 33 | import blens_core as C
 34 | import bl3_core as K
 35 | 
 36 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 近道の振る舞い・独立の札と答えの分かる門・等方の外の枝・有限でない値・結果を開く段の結びつき・起動器の三つの相／v2（裁定 D231〜D234）
 37 | NL = chr(10)
 38 | SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
 39 | T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
 40 | FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
 41 | DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
 42 | RESULTS = []
 43 | RUNNERS = []
 44 | RW_PASSES = [0]
 45 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 46 | 
 47 | 
 48 | def check(group, name, ok, detail=''):
 49 |     detail = detail if isinstance(detail, str) else '・'.join(map(str, detail)) if isinstance(detail, (list, tuple)) else str(detail)      # 記録の表は文字列だけ
 50 |     RESULTS.append((group, name, bool(ok), detail))
 51 |     print('[dry_run_Bl3] %s %-4s %s %s' % (group, 'OK' if ok else 'FAIL', name, detail), flush=True)
 52 | 
 53 | 
 54 | def raises(fn, exc):
 55 |     try:
 56 |         fn()
 57 |     except exc:
 58 |         return True
 59 |     return False
 60 | 
 61 | 
 62 | def err_of(fn, exc):
 63 |     """exc が上がればその文、上がらなければ None。"""
 64 |     try:
 65 |         fn()
 66 |     except exc as e_:
 67 |         return str(e_)
 68 |     return None
 69 | 
 70 | 
 71 | def jdefault(o):
 72 |     """起動器の出力の書き方（`boot_Bl3.write_json`）と同じ: numpy の数と配列を JSON に（値の丸めはしない）。"""
 73 |     if hasattr(o, 'tolist'):
 74 |         return o.tolist()
 75 |     if hasattr(o, 'item'):
 76 |         return o.item()
 77 |     raise TypeError(type(o))
 78 | 
 79 | 
 80 | rt = lambda o: json.loads(json.dumps(o, ensure_ascii=False, default=jdefault))      # 起動器の出力と同じ JSON の往復
 81 | 
 82 | 
 83 | def runner(R):
 84 |     RUNNERS.append(R)
 85 |     return R
 86 | 
 87 | 
 88 | def tool_shas():
 89 |     """走らせた器（凍結の器 `tools/freeze_Bl3.py` の器の一覧と、その import の閉包）と、正本・設計事実・方向の記録の SHA16。"""
 90 |     import freeze_Bl3 as FZ
 91 |     files = FZ.import_closure(FZ.TOOLS) + ['design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json']
 92 |     return collections.OrderedDict((f, sha16f(os.path.join(REPO, *f.split('/')))) for f in files)
 93 | 
 94 | 
 95 | # ---------------- 正本の文から独立に書いた主の札（検べ用・芯の関数を呼ばない・裁定 D236） ----------------
 96 | def answer_labels(T3, main_rows, eff, pair_names, dropped=()):
 97 |     """正本 `labels.p_rule`（両側に等しい裾）・`labels.iso_outside.rule`（Holm・段を下回れば通し、通らなかった所で止める）・`labels.second`（比べる相手の中央値を中心に、
 98 |     距離が比べる相手のすべてを上回れば最上位・向きの順位と対の単位の順位）・`labels.side_rule`（等方の帰無の四分位と中央値）・`labels.second.iso_top_share`・`nulls.real.rule`
 99 |     （v̂ と (6b) は兄弟の対を除き、Nk と td は B-lens の凍結の自分の対だけを除く）を、文から書き直した。"""
100 |     alpha = T3['labels']['iso_outside']['holm_alpha']
101 |     n_iso = T3['nulls']['isotropic']['count']
102 |     own = K.blens_own_pair()                                           # 二つの道の外の凍結物（B-lens の器の文から読む）
103 |     swaps = set(T3['nulls']['real']['swap_siblings'])
104 |     key = lambda sc, b, sg: '%s|%s|%+d' % (sc, b, int(sg))
105 |     out, pv = collections.OrderedDict(), {}
106 |     for r in main_rows:
107 |         if '%s|%s' % (r['scenario'], r['base']) in set(dropped):
108 |             continue
109 |         k, kk = key(r['scenario'], r['base'], r['sign']), key(r['scenario'], r['base'], -r['sign'])
110 |         e = float(eff[k][r['direction']])
111 |         iso = np.array([eff[k]['iso:%d' % i] for i in range(n_iso)], dtype=np.float64)
112 |         dropc = swaps if r['direction'] in ('static', 'loaded') else {own[r['direction']]}
113 |         comps = [q for q in pair_names if q not in dropc]
114 |         same = np.array([eff[k]['real:' + q] for q in comps], dtype=np.float64)
115 |         opp = np.array([eff[kk]['real:' + q] for q in comps], dtype=np.float64)
116 |         up, lo = int(np.sum(iso >= e)), int(np.sum(iso <= e))
117 |         p = min(1.0, 2.0 * min(up + 1, lo + 1) / (n_iso + 1))
118 |         tail = 'upper' if up < lo else ('lower' if lo < up else 'tie')
119 |         allc = np.concatenate([same, opp])
120 |         c0 = float(np.median(allc))
121 |         d = abs(e - c0)
122 |         dc = np.abs(allc - c0)
123 |         pairv = np.maximum(np.abs(same - c0), np.abs(opp - c0))
124 |         m0, q1, q3 = float(np.median(iso)), float(np.percentile(iso, 25)), float(np.percentile(iso, 75))
125 |         if q1 <= 0.0 <= q3:
126 |             side = ('sign_only', int(np.sign(e)))
127 |         else:
128 |             s0 = 1.0 if m0 > 0 else -1.0
129 |             side = ('stronger' if (e * s0 > 0 and abs(e) > abs(m0)) else ('weaker' if e * s0 >= 0 else 'opposite'), None)
130 |         out[r['id']] = {'p': p, 'tail': tail, 'top': bool(np.all(d > dc)), 'rank_o': int(1 + np.sum(dc >= d)), 'rank_p': int(1 + np.sum(pairv >= d)),
131 |                         'side': side, 'share': float(np.mean(np.abs(iso - c0) > float(np.max(dc))))}
132 |         pv[r['id']] = p
133 |     still = True
134 |     for i, rid in enumerate(sorted(pv, key=lambda x: (pv[x], x))):
135 |         ok = still and pv[rid] < alpha / (len(pv) - i)
136 |         out[rid]['holm'] = ok
137 |         still = ok
138 |     return out
139 | 
140 | 
141 | def synth_effects(T3, pair_names, n_iso, seed):
142 |     """合成の効き目（升目と符号の鍵 → 方向の名 → 効き目）: 奇でない押し（逆の符号の升目の効き目は別に引く）・零でない帰無の中心（升目ごとに中心を変える）・
143 |     等方の外に出る強い v̂ と Nk の行を半分ほど。値に意味は無い（札の組み立ての確かめだけに使う）。"""
144 |     rng = np.random.default_rng(seed)
145 |     names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
146 |     keys = sorted({'%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']} | {'%s|%s|%+d' % (sc, b, -int(sg)) for sc, b, sg in T3['cell_signs_main']})
147 |     eff = {}
148 |     for j, k in enumerate(keys):
149 |         center = (-1.0) ** j * (0.5 + 0.25 * j)
150 |         e = {d: float(rng.normal(loc=center, scale=0.5)) for d in names}
151 |         e.update({'iso:%d' % i: float(x) for i, x in enumerate(rng.normal(loc=center, scale=0.5, size=n_iso))})
152 |         e.update({'real:' + q: float(x) for q, x in zip(pair_names, rng.normal(loc=0.0, scale=1.5, size=len(pair_names)))})
153 |         if j % 2 == 0:
154 |             e['static'] = center + 6.0 * (1 if j % 4 == 0 else -1)
155 |             e['Nk'] = center - 6.0
156 |         eff[k] = e
157 |     return eff
158 | 
159 | 
160 | # ---------------- 一. 純粋な関数の形 ----------------
161 | def part_pure():
162 |     G = '一'
163 |     rng = np.random.default_rng(11)
164 |     units = ['A', 'B', 'C', 'D']
165 |     # 奇でない押し: 逆の符号の升目の効き目を「正の升目の効き目の符号を反転したもの」で代えると、門の答えが変わる
166 |     fp, fm = 'S1|X|+1', 'S1|X|-1'
167 |     eff = {u: {fp: float(i), fm: float(i) ** 2 - 2.0} for i, u in enumerate(units)}
168 |     rows = [{'unit': u, 'cell': 'S1|X', 'fam': fm, 'y': eff[u][fm]} for u in units] + [{'unit': u, 'cell': 'S1|X', 'fam': fp, 'y': eff[u][fp]} for u in units]
169 |     g_ok = K.gate(rows, eff, units, 0.05)
170 |     wrong = {u: {fp: eff[u][fp], fm: -eff[u][fp]} for u in units}
171 |     g_wrong = K.gate(rows, wrong, units, 0.05)
172 |     check(G, '奇でない押し（逆の符号の升目の効き目をそのまま使う）', g_ok['rho'] > 0.99 and abs(g_wrong['rho'] - g_ok['rho']) > 0.1,
173 |           '正しい呼び方 ρ %.3f／反転で代えた呼び方 ρ %.3f' % (g_ok['rho'], g_wrong['rho']))
174 |     # 零でない帰無の中心: 対称の割合では外に出ない反対の側の値が、両側に等しい裾の割合では外に出る
175 |     null = rng.normal(loc=3.0, scale=0.5, size=1999)
176 |     pe, ps = K.p_and_tail(-1.0, null)['p'], C.p_two_sided(-1.0, null)
177 |     pc_ = K.p_and_tail(3.0, null)['p']
178 |     check(G, '零でない帰無の中心', pe <= 2 / 2000 + 1e-12 and ps > 0.5 and pc_ > 0.5, '反対の側の値: 等しい裾 %.4f・対称 %.4f／中心の値: 等しい裾 %.3f' % (pe, ps, pc_))
179 |     # 減算の行: 符号を二重に掛けると押しの向きが反転する
180 |     rows_s = [{'unit': u, 'cell': 'S1|X', 'fam': fm, 'y': 2 * eff[u][fm]} for u in units]
181 |     ok_ = C.gate_perm([dict(r, sign=1) for r in rows_s], eff, units)
182 |     dbl = C.gate_perm([dict(r, sign=-1) for r in rows_s], eff, units)
183 |     check(G, '減算の行（符号の二重掛け）', ok_['rho'] > 0.99 and dbl['rho'] < -0.99, '符号 +1 ρ %.3f／二重掛け ρ %.3f' % (ok_['rho'], dbl['rho']))
184 |     # 下見で外れる升目と、門の行だけの升目（門の行・入れ替えの数・Holm の段）
185 |     rows_g = [{'unit': u, 'cell': c, 'fam': c + '|+1', 'y': float(i)} for i, u in enumerate(units) for c in ('S1|X', 'S4|Y')] + [{'unit': 'E', 'cell': 'S4|Y', 'fam': 'S4|Y|+1', 'y': 0.5}]
186 |     eff_g = {u: {'S1|X|+1': float(i), 'S4|Y|+1': float(i)} for i, u in enumerate(units + ['E'])}
187 |     g_all = K.gate(rows_g, eff_g, units + ['E'], 0.05)
188 |     g_drop = K.gate(rows_g, eff_g, units + ['E'], 0.05, drop_cells=['S4|Y'])
189 |     pv = {'r%d' % i: 0.001 * (i + 1) for i in range(16)}
190 |     h16 = K.holm(pv, 0.05)
191 |     pv14 = {k: v for k, v in pv.items() if k not in ('r14', 'r15')}
192 |     h14 = K.holm(pv14, 0.05)
193 |     step1_16 = min(v['step'] for v in h16.values())
194 |     step1_14 = min(v['step'] for v in h14.values())
195 |     check(G, '下見で外れる升目と門の行だけの升目', g_all['n_perm'] == 120 and g_drop['n_perm'] == 24 and g_drop['n_rows'] == 4 and abs(step1_16 - 0.05 / 16) < 1e-15 and abs(step1_14 - 0.05 / 14) < 1e-15,
196 |           '入れ替え %d → 外した後 %d（行 %d・行の無くなった単位を外した）・Holm の第一段 %.6f → %.6f' % (g_all['n_perm'], g_drop['n_perm'], g_drop['n_rows'], step1_16, step1_14))
197 |     # 帰無との同じ値: 両方の裾に数える・二つ目の札は同じ距離を上回らない
198 |     nl = np.array([0.0, 1.0, 1.0, 2.0, 3.0])
199 |     t = K.p_and_tail(1.0, nl)
200 |     comps = np.array([-1.0, 1.0, 2.0])                   # 中心は 1・行 3.0 の距離 2 と、比べる相手 -1.0 の距離 2 が同じ
201 |     sl = K.second_label(3.0, comps, [(-1.0, 2.0)])
202 |     check(G, '帰無との同じ値', t['upper'] == 4 and t['lower'] == 3 and not sl['top'], '上の裾 %d・下の裾 %d（同じ値を両方に数える）・同じ距離の比べる相手があれば最上位にしない' % (t['upper'], t['lower']))
203 |     # 両方の向きがちょうど対称な比べる相手: 中心は零・対の単位の順位は向きの順位の半分の側
204 |     xs = rng.normal(size=24)
205 |     co = np.concatenate([xs, -xs])
206 |     pairs = list(zip(xs, -xs))
207 |     sl2 = K.second_label(0.5, co, pairs)
208 |     check(G, '両方の向きがちょうど対称な比べる相手', abs(sl2['center']) < 1e-12 and sl2['rank_oriented'] == 2 * sl2['rank_pair'] - 1,
209 |           '中心 %.2e・向きの順位 %d・対の順位 %d' % (sl2['center'], sl2['rank_oriented'], sl2['rank_pair']))
210 |     # 端数のバッチ
211 |     ids = ['d%d' % i for i in range(2034)]
212 |     bp = K.batch_plan(ids, 16, T3['readout']['primary']['order_seed'], 0)
213 |     flat = [x for b in bp for x in b]
214 |     check(G, '端数のバッチ（零のベクトルで埋める）', len(bp) == 128 and flat.count(K.PAD) == 13 and flat.count(K.NOOP) == 1 and set(flat) - {K.PAD, K.NOOP} == set(ids),
215 |           'バッチ %d・埋める %d・無操作 %d' % (len(bp), flat.count(K.PAD), flat.count(K.NOOP)))
216 |     # 零の近くの中央値
217 |     s0 = K.effect_side(-2.0, rng.normal(loc=0.05, scale=1.0, size=1999))
218 |     check(G, '零の近くの中央値（符号だけ）', s0['side'] == 'sign_only' and s0['sign'] == -1, '四分位 [%.3f, %.3f]' % (s0['q1'], s0['q3']))
219 |     # Holm の境で一本違う p: 札の一致が落ちる
220 |     Kn = T3['nulls']['isotropic']['count']
221 |     lim = K.holm_limits(Kn, 0.05, 16)
222 |     base_null = np.linspace(-1.0, 1.0, Kn)
223 |     m_row = float(base_null[-1 - lim[0]]) + 1e-9          # 上の裾に帰無が lim[0] 本だけ残る値
224 |     pA = K.p_and_tail(m_row, base_null)['p']
225 |     null_B = base_null.copy()
226 |     null_B[-2 - lim[0]] = m_row + 1e-6                    # 帰無一本がこの値を越える
227 |     pB = K.p_and_tail(m_row, null_B)['p']
228 |     others = {'r%d' % i: 0.5 for i in range(1, 16)}
229 |     hA = K.holm(dict(others, r0=pA), 0.05)['r0']['pass']
230 |     hB = K.holm(dict(others, r0=pB), 0.05)['r0']['pass']
231 |     ag = K.agreement({'r0': [0.0]}, {'r0': [0.0]}, 0.001, {'r0': hA}, {'r0': hB})
232 |     check(G, 'Holm の境で一本違う p（札の一致の判定）', hA and not hB and not ag['agree'] and ag['values_within_tol'], 'p %.4f → %.4f・Holm の判定 %s → %s・一致 %s' % (pA, pB, hA, hB, ag['agree']))
233 |     # 器の誤りでやり直す流れ
234 |     q = K.q1_from_attempts([{'tool_error': '出口の値の自己検査が落ちた'}, {'decision': {'q1': '一部の升目を外して続ける'}}])
235 |     q2 = K.q1_from_attempts([{'decision': {'q1': '止める'}}, {'decision': {'q1': '続ける'}}])
236 |     q3 = K.q1_from_attempts([{'tool_error': 'x'}])
237 |     check(G, '器の誤りでやり直す流れ（q1 の採点）', q['scored'] and q['q1'] == '一部の升目を外して続ける' and q2['first_decision'] == '止める' and not q3['scored'],
238 |           'やり直した下見で採点・一度目の決定を併記・やり直さなければ採点しない')
239 |     # 掃き出し: 札と門と向きの足し分に要る升目・符号・方向の組が、本の計算の組み立てにそろう
240 |     import bl3_run as BR
241 |     import analyze_Bl3 as AZ
242 |     names_real = ['real:' + p for p in DJ['groups']['real']['names']]
243 |     iso_ids = ['iso:%d' % i for i in range(T3['nulls']['isotropic']['count'])]
244 |     b3 = ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
245 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
246 |     sets = BR.cell_sign_sets(T3, None, T3['directions']['named'], b3, iso_ids, names_real, gate_only)
247 |     have = {(k, d) for k, cell, sg, ds in sets for d in ds}
248 |     need, miss = set(), []
249 |     for r in T3['main_rows']:
250 |         k = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
251 |         kk = '%s|%s|%+d' % (r['scenario'], r['base'], -r['sign'])
252 |         need.add((k, r['direction']))
253 |         need |= {(k, i) for i in iso_ids}
254 |         comps = K.comparators_for(r['direction'], DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'])
255 |         need |= {(k, 'real:' + p) for p in comps} | {(kk, 'real:' + p) for p in comps}
256 |     fams = sorted({'%s|%s|%+d' % (g['scenario'], g['base'], g['sign']) for g in FJ['facts']['C']['gate_rows']})
257 |     unit_ids = list(T3['directions']['named']) + b3
258 |     need |= {(f, u) for f in fams for u in unit_ids}
259 |     miss = sorted(need - have)
260 |     check(G, '掃き出し（要る組が本の計算の組み立てにそろう）', not miss, '要る組 %d・組み立て %d・足りない %d%s' % (len(need), len(have), len(miss), ('（例 %s）' % miss[:3]) if miss else ''))
261 |     n_passes = sum(len(ds) for _, _, _, ds in sets)
262 |     E = FJ['facts']['E']
263 |     check(G, '本の計算の順伝播の数（転記行 E と）', n_passes == E['passes_main'] + E['passes_gate_extra'] + E['passes_orient_extra'],
264 |           '組み立て %d・転記行 E %d ＋ %d ＋ %d' % (n_passes, E['passes_main'], E['passes_gate_extra'], E['passes_orient_extra']))
265 |     # 札の一致の中身（裁定 D232）: 等方の内側の行の裾と側は比べない・等方の外の行の裾と側は比べる
266 |     lab0 = {'r_in': {'iso_outside': False, 'tail': 'upper', 'side': {'side': 'stronger', 'sign': 1}, 'second': {'top': False}},
267 |             'r_out': {'iso_outside': True, 'tail': 'upper', 'side': {'side': 'stronger', 'sign': 1}, 'second': {'top': True}}}
268 |     lab_in = copy.deepcopy(lab0)
269 |     lab_in['r_in'].update(tail='lower', side={'side': 'opposite', 'sign': -1})
270 |     lab_tail, lab_side = copy.deepcopy(lab0), copy.deepcopy(lab0)
271 |     lab_tail['r_out']['tail'] = 'lower'
272 |     lab_side['r_out']['side'] = {'side': 'weaker', 'sign': 1}
273 |     sg_ = AZ.labels_signature
274 |     check(G, '札の一致の中身（等方の内側の行の裾と側は比べない・等方の外の行の裾と側は比べる・裁定 D232）',
275 |           sg_(lab0) == sg_(lab_in) and sg_(lab0) != sg_(lab_tail) and sg_(lab0) != sg_(lab_side),
276 |           '内側の行の裾と側だけが違う → 同じ・外の行の裾が違う → 違う・外の行の側が違う → 違う')
277 |     # 下見で外した後の偶然の目安（裁定 D231）: 外さなければ正本の生成器の値と同じ・外すと外した行の分だけ減る
278 |     lab_all = {r['id']: {'direction': r['direction']} for r in T3['main_rows']}
279 |     drop_c = 'N1|O-Ncold'
280 |     gone = [r for r in T3['main_rows'] if '%s|%s' % (r['scenario'], r['base']) == drop_c]
281 |     ch_all = AZ.chance_after_drop(T3, lab_all)
282 |     ch_d = AZ.chance_after_drop(T3, {k: v for k, v in lab_all.items() if k not in {r['id'] for r in gone}})
283 |     co_, cp_ = T3['nulls']['real']['comparators_oriented'], T3['nulls']['real']['comparators']
284 |     less_o = round(ch_all['oriented'] - sum(1 / (co_[r['direction']] + 1) for r in gone), 4)
285 |     less_p = round(ch_all['pair'] - sum(1 / (cp_[r['direction']] + 1) for r in gone), 4)
286 |     check(G, '下見で外した後の偶然の目安（外さなければ正本の値・外すと外した行の分だけ減る・裁定 D231）',
287 |           (ch_all['oriented'], ch_all['pair']) == (T3['nulls']['real']['chance_second'], T3['nulls']['real']['chance_second_pair']) and
288 |           abs(ch_d['oriented'] - less_o) < 1e-4 and abs(ch_d['pair'] - less_p) < 1e-4 and sum(ch_d['rows_by_direction'].values()) == len(T3['main_rows']) - len(gone),
289 |           '外さない %.4f・%.4f（正本 %.4f・%.4f）／%s を外す %.4f・%.4f（行 %d）' % (ch_all['oriented'], ch_all['pair'], T3['nulls']['real']['chance_second'],
290 |                                                                          T3['nulls']['real']['chance_second_pair'], drop_c, ch_d['oriented'], ch_d['pair'], sum(ch_d['rows_by_direction'].values())))
291 |     # 比べる相手の除き方の錨（裁定 D231）: B-lens の凍結の OWN_PAIR と正本の兄弟の対に照らす・ずらした写しで止まる
292 |     pn, sw, own = DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'], K.blens_own_pair()
293 |     anc = K.comparator_anchor(pn, sw, own)
294 |     stop_own = raises(lambda: K.comparator_anchor(pn, sw, dict(own, Nk=own['static'])), ValueError)
295 |     stop_sw = raises(lambda: K.comparator_anchor(pn, [x for x in sw if x != own['static']], own), ValueError)
296 |     check(G, '比べる相手の除き方の錨（B-lens の凍結の OWN_PAIR と正本の兄弟の対・裁定 D231）', bool(anc) and stop_own and stop_sw,
297 |           '除いた対の数 %s・錨をずらした写しで止まる %s・兄弟の対から自分の対を抜いた写しで止まる %s' % ({d: len(v) for d, v in anc.items()}, stop_own, stop_sw))
298 |     # 正本の文から独立に書いた札（芯の関数を呼ばない）と、集計の器の札の突き合わせ（等方は正本の本数・奇でない押し・零でない帰無の中心・下見で外した升目・裁定 D236）
299 |     n_iso = T3['nulls']['isotropic']['count']
300 |     pn_ = DJ['groups']['real']['names']
301 |     eff_s = synth_effects(T3, pn_, n_iso, seed=17)
302 |     for dropped_ in ([], ['N1|O-Ncold']):
303 |         mine = answer_labels(T3, T3['main_rows'], eff_s, pn_, dropped_)
304 |         lab_, meta_ = AZ.row_labels(T3, T3['main_rows'], eff_s, pn_, dropped_)
305 |         diff_ = []
306 |         for rid, a_ in mine.items():
307 |             o = lab_.get(rid)
308 |             if o is None:
309 |                 diff_.append((rid, '行が無い'))
310 |                 continue
311 |             got = (round(o['p'], 12), o['tail'], o['iso_outside'], o['second']['top'], o['second']['rank_oriented'], o['second']['rank_pair'], o['side']['side'],
312 |                    o['side'].get('sign') if o['side']['side'] == 'sign_only' else None, round(o['iso_top_share'], 12))
313 |             want_ = (round(a_['p'], 12), a_['tail'], a_['holm'], a_['top'], a_['rank_o'], a_['rank_p'], a_['side'][0], a_['side'][1], round(a_['share'], 12))
314 |             if got != want_:
315 |                 diff_.append((rid, got, want_))
316 |         n_out = sum(1 for a_ in mine.values() if a_['holm'])
317 |         check(G, '正本の文から独立に書いた札と集計の器の札（等方 %d 本・外した升目 %s・裁定 D236）' % (n_iso, '・'.join(dropped_) or 'なし'),
318 |               not diff_ and set(lab_) == set(mine) and n_out > 0 and meta_['m_rows'] == len(mine),
319 |               '行 %d・食い違い %d・等方の外の行 %d・Holm の段の数 %d%s' % (len(mine), len(diff_), n_out, meta_['m_rows'], ('（例 %s）' % (diff_[:1],)) if diff_ else ''))
320 |     # 等方の外の行が出る枝: 札の一致の中身（裁定 D232）・q7・予想の答え
321 |     lab_, _ = AZ.row_labels(T3, T3['main_rows'], eff_s, pn_, [])
322 |     out_ids = [rid for rid, o in lab_.items() if o['iso_outside']]
323 |     in_ids = [rid for rid, o in lab_.items() if not o['iso_outside']]
324 |     q7r = AZ.q7_rows_of(lab_, FJ)
325 |     sig0 = AZ.labels_signature(lab_)
326 |     flip_in, flip_out = copy.deepcopy(lab_), copy.deepcopy(lab_)
327 |     if in_ids:
328 |         flip_in[in_ids[0]]['tail'] = 'lower' if flip_in[in_ids[0]]['tail'] != 'lower' else 'upper'
329 |     flip_out[out_ids[0]]['tail'] = 'lower' if flip_out[out_ids[0]]['tail'] != 'lower' else 'upper'
330 |     check(G, '等方の外の行が出る枝（割合を決めた裾の比べは外の行だけ・q7 の行・裁定 D232・D236）',
331 |           bool(out_ids) and AZ.labels_signature(flip_in) == sig0 and AZ.labels_signature(flip_out) != sig0 and bool(q7r) and all(r_['id'] in out_ids for r_ in q7r),
332 |           '等方の外の行 %d・内の行の裾を変える → 札は同じ・外の行の裾を変える → 札が違う・q7 の行 %d' % (len(out_ids), len(q7r)))
333 |     # 答えの分かる合成での門の組み立て: 門の行の効き目を行動の量と同じ値に置けば、本の門の順位相関はちょうど一（家族の鍵か単位を取り違えれば一にならない）
334 |     AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
335 |     rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
336 |     units_g = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
337 |     rng_g = np.random.default_rng(23)
338 |     for drop_g in ([], ['N1|O-Ncold']):
339 |         eff_g = collections.defaultdict(dict)
340 |         for r_ in rows_gate:
341 |             if r_['cell'] in set(drop_g):
342 |                 continue                                               # 外した升目の家族の効き目は置かない（集計の器は引かないはず・裁定 D231）
343 |             for u in units_g:
344 |                 eff_g[r_['fam']].setdefault(u, float(rng_g.normal()))
345 |             eff_g[r_['fam']][r_['unit']] = float(r_['y'])
346 |         G_ = AZ.gates(T3, rows_gate, dict(eff_g), drop_g, ())
347 |         n_left = sum(1 for r_ in rows_gate if r_['cell'] not in set(drop_g))
348 |         check(G, '答えの分かる合成での門の組み立て（行の効き目を行動の量に置く・外した升目 %s・裁定 D236）' % ('・'.join(drop_g) or 'なし'),
349 |               abs(G_['main']['rho'] - 1.0) < 1e-12 and G_['main']['n_rows'] == n_left and G_['desc_choice_a']['rho'] < 1.0 - 1e-9,
350 |               '本の門の順位相関 %.12f・行 %d（残った門の行 %d）・選択 a の件数の門の順位相関 %.4f（一でない）' % (G_['main']['rho'], G_['main']['n_rows'], n_left, G_['desc_choice_a']['rho']))
351 | 
352 | 
353 | # ---------------- 二・三. 乱数の小さな模型 ----------------
354 | def tiny_model(seed=0, layers=4):
355 |     import torch
356 |     from transformers import AutoConfig, AutoModelForCausalLM
357 |     cfg = AutoConfig.from_pretrained(SNAP)
358 |     cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim, cfg.intermediate_size = 64, layers, 4, 2, 16, 128
359 |     if getattr(cfg, 'layer_types', None):
360 |         cfg.layer_types = list(cfg.layer_types)[:layers]
361 |     torch.manual_seed(seed)
362 |     model = AutoModelForCausalLM.from_config(cfg)
363 |     with torch.no_grad():
364 |         g = torch.Generator().manual_seed(seed + 1)
365 |         for n, p in model.named_parameters():
366 |             if n.endswith('norm.weight'):                 # 乱数の初期値は一なので、二重の正規化が見えない——散らす
367 |                 p.copy_(torch.rand(p.shape, generator=g) + 0.5)
368 |     return model.to(torch.bfloat16).eval(), cfg
369 | 
370 | 
371 | def calibrate_readout_rows(model, R0, cell, FJ, seed=7):
372 |     """乱数の模型の出口の行列を、読み取りの集合の文字が強く出るように置く（正本の閾値は変えずに、下見を本の計算まで通すため・合成だけ）。
373 |     読み取りの集合の文字の行を、升目 cell の無操作の最終の正規化の出口の向きの三倍に小さな乱数を足したものにする。起動器の DRY も同じ関数を呼ぶ。"""
374 |     import torch
375 |     cap = {}
376 |     hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
377 |     with torch.no_grad():
378 |         model(input_ids=torch.tensor([cell.ids]), logits_to_keep=1)
379 |     hh.remove()
380 |     m_ = R0.norm32(cap['h'])[0]
381 |     m_ = m_ / m_.norm()
382 |     set_all = sorted({int(x) for x in FJ['facts']['A']['letter_ids'].values()})
383 |     gcal = torch.Generator().manual_seed(seed)
384 |     with torch.no_grad():
385 |         for tkn in set_all:
386 |             model.lm_head.weight[tkn] = (3.0 * m_ + 0.3 * torch.randn(m_.shape, generator=gcal)).to(model.lm_head.weight.dtype)
387 |     return set_all
388 | 
389 | 
390 | def synth_dirs(dim, names, seed=5):
391 |     rng = np.random.default_rng(seed)
392 |     v = rng.normal(size=dim)
393 |     nv = float(np.linalg.norm(v))
394 |     out = collections.OrderedDict()
395 |     for n in names:
396 |         x = v if n == 'static' else rng.normal(size=dim)
397 |         out[n] = x * (nv / float(np.linalg.norm(x)))
398 |     out['zero:test'] = np.zeros(dim)
399 |     return out
400 | 
401 | 
402 | def rewrite(RW, model, tok, rows, dbr, dirs, L, coef):
403 |     """別の個体の残差の書き換えの道（起動器と同じ `use_cache=False` で呼ぶ）。順伝播の数を数える。"""
404 |     sub = collections.OrderedDict((nm, dbr[nm]) for nm, _, _ in rows)
405 |     RW_PASSES[0] += sum(1 + len(v) for v in sub.values())
406 |     return RW.recompute_rewrite(model, tok, T3, FJ, [tuple(r) for r in rows], sub, dirs, L, coef, use_cache=False)
407 | 
408 | 
409 | def part_model(iso_n, e2e_iso):
410 |     import torch
411 |     import bl3_run as BR
412 |     import run_stageB_local as RB
413 |     import direction_B
414 |     import analyze_Bl3 as AZ
415 |     import bl3_recompute_rewrite as RW
416 |     from transformers import AutoTokenizer
417 |     G2, G3 = '二', '三'
418 |     t0 = time.time()
419 |     tok = AutoTokenizer.from_pretrained(SNAP)
420 |     model, cfg = tiny_model()
421 |     L = direction_B.layer_index(T3['layers']['selected_ratio'], cfg.num_hidden_layers)
422 |     coef = T3['layers']['coef_applied']
423 |     seed = T3['readout']['primary']['order_seed']
424 |     pair_names = list(DJ['groups']['real']['names'])
425 |     swaps = T3['nulls']['real']['swap_siblings']
426 |     names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])] + ['iso:%d' % i for i in range(iso_n)] + \
427 |         ['real:' + p for p in pair_names] + ['check']
428 |     dirs = synth_dirs(cfg.hidden_size, names)
429 |     cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
430 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
431 |     gate_only_cells = sorted({'%s|%s' % (x[0], x[1]) for x in gate_only})
432 |     cells = BR.build_cells(tok, T3, FJ, cell_keys + gate_only_cells)
433 |     # 乱数の模型の出口の行列を、読み取りの集合の文字が強く出るように置く（正本の閾値は変えずに、下見を本の計算まで通すため・合成だけ）
434 |     R0 = BR.Runner(model, T3, L, coef, dirs)
435 |     calibrate_readout_rows(model, R0, cells[cell_keys[0]], FJ)
436 |     R = runner(BR.Runner(model, T3, L, coef, dirs))
437 |     check(G2, '升目の入力が転記行 B と一致する（実のトークナイザ）', True, '%d 升目' % len(cells))
438 |     # 書き出しの割り方が変わる場合（器が止まるか）
439 |     FJx = copy.deepcopy(FJ)
440 |     FJx['facts']['A']['prefix_ids'] = FJ['facts']['A']['prefix_ids'][:-1]
441 |     check(G2, '書き出しの割り方が変わる場合（器が止まる）', raises(lambda: BR.build_cells(tok, T3, FJx, cell_keys[:1]), BR.ToolError), '書き出しを一トークン欠いた入力で、転記行 B との突き合わせが止めた')
442 |     # 下見（正本の値のまま・乱数の模型・揺れの版は起動器と同じく境の確かめを通ったもの）
443 |     stage_b_rate = {k: FJ['facts']['B']['cells'][k]['catastrophe'] / FJ['facts']['B']['cells'][k]['n_ok'] for k in cell_keys}
444 |     variants = collections.OrderedDict((k, v['ids']) for k, v in FJ['facts']['A']['variants'].items() if v.get('boundary_ok'))
445 |     pilot = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
446 |     dec = pilot['decision']
447 |     check(G2, '下見が機械の決定まで走る', 'q1' in dec and 'vi' in pilot and ('batch' in pilot or dec.get('stop')),
448 |           'q1 %s・(vi) (a) %.2e (b) %.2e・バッチ %s・揺れの床 %s・近道の許容 %s・(v) の近道 %s（記述）' % (dec.get('q1'), pilot['vi']['decision']['spread_a'], pilot['vi']['decision']['spread_b'],
449 |                                                                              pilot.get('batch'), pilot.get('floor'), pilot.get('cache_tol'), (pilot.get('v') or {}).get('shortcut')))
450 |     check(G2, '出口の値の自己検査（下見の頭）', pilot['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (pilot['logit_check']['max_abs'], pilot['logit_check']['tol']))
451 |     if dec.get('stop'):
452 |         return {'pilot': pilot, 'n_forward': sum(r.n_forward for r in RUNNERS), 'seconds': round(time.time() - t0, 1), 'iso_n': iso_n, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}
453 |     batch, tol, floor = pilot['batch'], pilot['cache_tol'], pilot['floor']
454 |     tol2 = tol + floor                                                   # 二段目の許容（近道の許容と揺れの床の和・集計の器と同じ式）
455 |     # 本の計算（起動器が呼ぶ `run_main_phase` をそのまま通す: 頭の自己検査〔出口の値・最後の層〕→ 全ての升目と符号・近道を使わない）
456 |     items = [(cells['%s|%s' % (sc, b)], int(sg)) for sc, b, sg in T3['cell_signs_main']]
457 |     names_ = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])],
458 |               'iso': ['iso:%d' % i for i in range(iso_n)], 'real': ['real:' + p for p in pair_names]}
459 |     sets_run = BR.cell_sign_sets(T3, None, names_['named'], names_['B_random'], names_['iso'], names_['real'], gate_only)
460 |     pc_calls, fwd = [0], collections.Counter()
461 |     full_len = {len(c.ids) for c in cells.values()}
462 |     orig_pc = R.prefix_cache
463 |     R.prefix_cache = lambda c: (pc_calls.__setitem__(0, pc_calls[0] + 1), orig_pc(c))[1]
464 | 
465 |     def pre_kw(m, args, kwargs):
466 |         ids_ = kwargs.get('input_ids') if kwargs.get('input_ids') is not None else (args[0] if args else None)
467 |         fwd['n'] += 1
468 |         fwd['past'] += int(kwargs.get('past_key_values') is not None)
469 |         fwd['use_cache'] += int(bool(kwargs.get('use_cache')))
470 |         fwd['short'] += int(ids_ is None or int(ids_.shape[-1]) not in full_len)
471 |     hk_ = model.register_forward_pre_hook(pre_kw, with_kwargs=True)
472 |     try:
473 |         MP = BR.run_main_phase(R, T3, FJ, cells, names_, pilot, iso_n=None, log=lambda s: None)
474 |     finally:
475 |         hk_.remove()
476 |         R.prefix_cache = orig_pc
477 |     hd = MP['head']
478 |     check(G2, '本の計算の頭の出口の値の自己検査', hd['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (hd['logit_check']['max_abs'], hd['logit_check']['tol']))
479 |     check(G2, '本の計算は近道を使わない（振る舞い: 近道の元を作る呼び出し・使い回す cache・use_cache・列の全長を全ての順伝播で数えた・裁定 D236）',
480 |           fwd['n'] > 0 and pc_calls[0] == 0 and fwd['past'] == 0 and fwd['use_cache'] == 0 and fwd['short'] == 0,
481 |           '順伝播 %d 回・近道の元を作った回 %d・cache を渡した回 %d・use_cache が真の回 %d・列の全長でない回 %d' % (fwd['n'], pc_calls[0], fwd['past'], fwd['use_cache'], fwd['short']))
482 |     check(G2, '本の計算は近道を使わない（頭の近道の確かめを走らせない・下見の (v) は記述・裁定 D234）',
483 |           MP['shortcut'] is False and hd.get('shortcut') is False and 'steered_cache_check' not in hd and 'shortcut_rule' in hd,
484 |           '下見の (v) の近道の決定 %s・(v) の差の最大 %.2e（近道の許容 %.4f）' % (pilot['v']['shortcut'], max(abs(x) for x in pilot['v']['diffs'].values()), tol))
485 |     lc = hd['layer_check']
486 |     check(G2, '最後の層の自己検査', lc['pass'], '差 %.2e（許容 %s）' % (lc['diff'], lc['tol']))
487 |     outs = MP['cells']
488 |     ok_keys = list(outs) == [s[0] for s in sets_run] and all(set(o['lo']) == set(s[3]) | {K.NOOP} for s, o in zip(sets_run, outs.values()))
489 |     check(G2, '本の計算: 全ての升目と符号・全ての方向と無操作がそろい、埋めた零のベクトルの値は使わない', ok_keys, '升目と符号 %d（組み立て %d）' % (len(outs), len(sets_run)))
490 |     # 層ごとの差分の余弦は足した向き（符号を掛けた方向）と測る（裁定 D231）: 減算の升目と符号でも、選んだ層の次の層の static の余弦が正
491 |     cs = {k: outs[k]['layers']['rows']['static'][0][1] for k in ('S1|O-Ncold|-1', 'S1|O-Ncold|+1')}
492 |     check(G2, '層ごとの差分の余弦を足した向き（符号を掛けた方向）と測る（減算の升目と符号でも正・裁定 D231）', all(c > 0 for c in cs.values()),
493 |           '選んだ層の次の層の static の余弦: 減算 %.3f・加算 %.3f' % (cs['S1|O-Ncold|-1'], cs['S1|O-Ncold|+1']))
494 |     # 零のベクトルの行（同じ升目と符号をもう一度・零のベクトルを一本足して・近道なし）
495 |     kz = [i for i, s in enumerate(sets_run) if s[0] == 'S1|O-Ncold|-1'][0]
496 |     key_z, ck_z, sg_z, ds_z = sets_run[kz]
497 |     oz = BR.run_cell_sign(R, cells[ck_z], sg_z, list(ds_z) + ['zero:test'], batch, seed, kz, pc=None)
498 |     zt = oz['effects']['zero:test']
499 |     dmx = max(abs(oz['effects'][d] - outs[key_z]['effects'][d]) for d in outs[key_z]['effects'])
500 |     check(G2, '零のベクトルの行は無操作と同じ値になる（別のバッチでも）', abs(zt) <= max(floor, 1e-6), '効き目 %.2e（揺れの床 %.2e）・バッチの組を変えた同じ方向の効き目の差の最大 %.2e（記述）' % (zt, floor, dmx))
501 |     dirs['nan:test'] = np.full(cfg.hidden_size, np.nan)
502 |     msg_nan = err_of(lambda: BR.run_cell_sign(R, cells[ck_z], sg_z, ['nan:test', 'static'], batch, seed, kz, pc=None), BR.ToolError)
503 |     del dirs['nan:test']
504 |     check(G2, '有限でない値の効き目は器の誤りで止まる（走らせる器の出口・裁定 D236）', msg_nan is not None and '有限でない値' in msg_nan, (msg_nan or '')[:70])
505 |     # バッチの中の位置で方向を取り違えない
506 |     c0, sg0 = items[0]
507 |     r1 = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, full=False)
508 |     r2 = R.forward(c0, ['td', 'Nk', K.NOOP, 'static'], sg0, full=False)
509 |     e1 = {d: float(r1['lo'][i] - r1['lo'][0]) for i, d in enumerate([K.NOOP, 'static', 'Nk', 'td'])}
510 |     e2 = {d: float(r2['lo'][i] - r2['lo'][2]) for i, d in enumerate(['td', 'Nk', K.NOOP, 'static'])}
511 |     dpos = max(abs(e1[d] - e2[d]) for d in ('static', 'Nk', 'td'))
512 |     check(G2, 'バッチの中の位置で方向を取り違えない', dpos <= max(floor, 1e-6) and max(abs(e1[d]) for d in ('static', 'Nk', 'td')) > 1e-3, '位置を入れ替えた効き目の差の最大 %.2e' % dpos)
513 |     # （記述）近道ありと近道なし（効き目・同じバッチの大きさ）: 近道は下見の (v) の記述だけに使う
514 |     pc0 = R.prefix_cache(c0)
515 |     rs = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, pc=pc0, full=False)
516 |     ds_ = max(abs(float((rs['lo'][i] - rs['lo'][0]) - (r1['lo'][i] - r1['lo'][0]))) for i in (1, 2, 3))
517 |     check(G2, '（記述）近道ありと近道なしの効き目の差（近道は下見の (v) の記述だけ・本の計算は使わない・裁定 D234）', True, '差の最大 %.2e（近道の許容 %.4f）' % (ds_, tol))
518 |     # 層ごとの差分の記述
519 |     main_keys = {'%s|%s|%+d' % (a_, b_, s_) for a_, b_, s_ in T3['cell_signs_main']}
520 |     lay_ok = all((o['layers']['iso_summary'] is not None and o['layers']['iso_summary']['n'] == iso_n and len(o['layers']['rows']) == 7 and
521 |                   all(len(v) == len(R.after) for v in o['layers']['rows'].values())) if k in main_keys else
522 |                  (o['layers']['iso_summary'] is None and not o['layers']['rows']) for k, o in outs.items())
523 |     summ = outs['S1|O-Ncold|-1']['layers']['iso_summary']
524 |     check(G2, '層ごとの差分（主の組だけ・名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間だけ）', lay_ok,
525 |           '層 %d・等方 %d 本・主の組の升目と符号 %d' % (len(R.after), summ['n'] if summ else 0, sum(1 for k in outs if k in main_keys)))
526 |     # 独立の再計算の組と、二つの道（本の器のフック・別の個体の残差の書き換え〔起動器と同じ use_cache=False〕・近道なし・バッチ一）
527 |     st_rows = [r for r in T3['main_rows'] if r['direction'] == 'static']
528 |     v_rows = [[r for r in st_rows if r['sign'] < 0][0], [r for r in st_rows if r['sign'] > 0][0]]      # 減算の行と加算の行を一つずつ
529 |     rows_all, dirs_all = K.recompute_set(T3['main_rows'], pair_names, swaps, iso_n, dec.get('dropped', []))
530 |     comps = K.comparators_for('static', pair_names, swaps)
531 |     hand = {r['id']: [('static', r['sign'])] + [('iso:%d' % i, r['sign']) for i in range(iso_n)] + [('real:' + p, r['sign']) for p in comps] + [('real:' + p, -r['sign']) for p in comps]
532 |             for r in T3['main_rows'] if r['direction'] == 'static' and '%s|%s' % (r['scenario'], r['base']) not in set(dec.get('dropped', []))}
533 |     n_pass_rc = sum(1 + len(v) for v in dirs_all.values())
534 |     E_ = FJ['facts']['E']
535 |     Kn_ = T3['nulls']['isotropic']['count']
536 |     per_ok = all(1 + len(v) == E_['per_row_recompute'] - (Kn_ - iso_n) for v in dirs_all.values())
537 |     rows_ok = dec.get('dropped') or 2 * len(rows_all) * E_['per_row_recompute'] == E_['passes_recompute']
538 |     check(G2, '独立の再計算の組（v̂ の行ごとに無操作・v̂・等方の帰無・比べる相手の両方の向き・転記行 E と）', [x[0] for x in rows_all] == list(hand) and dict(dirs_all) == hand and per_ok and rows_ok,
539 |           'v̂ の行 %d・行ごとの順伝播 %d（等方 %d 本のとき・転記行 E の行ごと %d は等方 %d 本）・一つの道の順伝播 %d' % (
540 |               len(rows_all), 1 + len(next(iter(dirs_all.values()))), iso_n, E_['per_row_recompute'], Kn_, n_pass_rc))
541 |     v_ids = [r['id'] for r in v_rows]
542 |     hk = BR.recompute_hook_path(R, [(nm, cells[ck], s) for nm, ck, s in rows_all if nm in v_ids], dirs_all)
543 |     rw = rewrite(RW, model, tok, [(nm, ck, s) for nm, ck, s in rows_all if nm in v_ids], dirs_all, dirs, L, coef)
544 |     worst = 0.0
545 |     for r in v_rows:
546 |         key = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
547 |         kk = '%s|%s|%+d' % (r['scenario'], r['base'], -r['sign'])
548 |         for dk, e in hk[r['id']]['effects'].items():
549 |             did, sg = dk.rsplit('|', 1)[0], int(dk.rsplit('|', 1)[1])
550 |             m = outs[key if sg == r['sign'] else kk]['effects'][did]
551 |             worst = max(worst, abs(m - e))
552 |     check(G2, '（記述）二段目の本の道（近道なし・本のバッチ）とフック（バッチ一）の効き目の差の最大（判定は札の一致・裁定 D234）', True,
553 |           '差の最大 %.2e（許容 %.4f・許容の%s）' % (worst, tol2, '内' if worst <= tol2 else '外'))
554 |     # 集計の器を端から端まで（等方の本数だけ合成の本数にした正本の写しで・合成だけ）
555 |     T3d = AZ.with_iso(T3, iso_n)
556 |     AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
557 |     rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
558 |     fc = FJ['facts']['C']
559 |     same_rows = sorted(r['name'] for r in rows_gate) == sorted(fc['style_share_pt'])
560 |     style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
561 |     check(G2, '門の行と様式の転位の行を段階 B の記録から作り直す（転記行 C と）', same_rows and len(rows_gate) == T3['gate']['rows_gate'] and sorted(style_rows) == sorted(fc['style_rows']),
562 |           '門の行 %d・様式の転位の行 %d' % (len(rows_gate), len(style_rows)))
563 |     v_hook, v_rw = {i: hk[i] for i in v_ids}, {i: rw[i] for i in v_ids}
564 |     eff_all = {k: o['effects'] for k, o in outs.items()}
565 |     AZr = AZ.analyze(T3d, FJ, outs, [pilot], pair_names, rows_gate, hook=v_hook, rewrite=v_rw, style_rows=style_rows, rows_subset=set(v_hook))
566 |     AZfull = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, v_hook, v_rw, pilot)
567 |     check(G2, '独立の再計算の行が欠ければ一致しない（本の計算の求め方）', not AZfull['second']['agree'] and AZfull['second'].get('reason') == 'keys' and not AZfull['agree'],
568 |           '欠けた行 %d' % len(AZfull['second'].get('missing', [])))
569 |     gate_keys = ('main', 'without_vhat', 'desc_without_vhat_loaded', 'desc_choice_a', 'desc_without_style')
570 |     ok_az = len(AZr['rows']) == len(T3['main_rows']) and all(k in AZr['gates'] for k in gate_keys) and list(AZr['predictions_truth']) == [it['key'] for it in T3['predictions']['items']]
571 |     check(G2, '集計の器が主の札・門・記述の門・予想の答えを出す', ok_az,
572 |           '行 %d・本の門の入れ替え %s・v̂ を抜いた門 %s・予想の答え %s' % (len(AZr['rows']), AZr['gates']['main'].get('n_perm'), AZr['gates']['without_vhat'].get('n_perm'), dict(AZr['predictions_truth'])))
573 |     rc_ = AZr['recompute']
574 |     check(G2, '集計の器の二段の一致（一段目は無操作の値と効き目の値と札・裁定 D233・二段目は札・裁定 D234）', rc_['first']['agree'] and rc_['second']['agree'] and rc_['agree'],
575 |           '一段目 %s（無操作の値と効き目の差の最大 %.2e・許容 %s）・二段目 %s（効き目の差の最大 %.2e・許容 %.4f・許容の%s・記録）' % (
576 |               rc_['first']['agree'], rc_['first']['max_abs_diff'], rc_['tol_first'], rc_['second']['agree'], rc_['second']['max_abs_diff'], rc_['tol_second'],
577 |               '内' if rc_['second']['values_within_tol'] else '外'))
578 |     # 二段目は札の一致で判定する（裁定 D234）: 値だけが許容の外（等方の帰無の端の一本を外へ動かし、裾の本数と順位の統計を変えない）なら一致して印を残し、札が変われば一致しない
579 |     rid0, s0_ = v_rows[0]['id'], int(v_rows[0]['sign'])
580 |     hk_a = copy.deepcopy(v_hook)
581 |     Ea = hk_a[rid0]['effects']
582 |     iso_keys = ['iso:%d|%+d' % (i, s0_) for i in range(iso_n)]
583 |     iso_vals = [Ea[k] for k in iso_keys]
584 |     if Ea['static|%+d' % s0_] >= float(np.median(iso_vals)):
585 |         Ea[iso_keys[int(np.argmin(iso_vals))]] -= tol2 + 0.01
586 |     else:
587 |         Ea[iso_keys[int(np.argmax(iso_vals))]] += tol2 + 0.01
588 |     ag_a = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, hk_a, None, pilot, rows_subset=set(hk_a))['second']
589 |     lab_main = AZr['rows'][rid0]['second']
590 |     hk_b = copy.deepcopy(v_hook)
591 |     hk_b[rid0]['effects']['static|%+d' % s0_] = lab_main['center'] if lab_main['top'] else lab_main['center'] + 1e3
592 |     ag_b = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, hk_b, None, pilot, rows_subset=set(hk_b))['second']
593 |     check(G2, '二段目は札の一致で判定する（値だけが許容の外なら一致して印を残す・札が変われば一致しない・裁定 D234）',
594 |           ag_a['agree'] and ag_a['values_beyond_tol'] and not ag_a['values_within_tol'] and not ag_b['agree'] and not ag_b['labels_same'],
595 |           '等方の帰無の端の一本を %.4f 動かした（許容 %.4f）→ 一致 %s・許容の外の印 %s／二つ目の札の最上位を変えた → 一致 %s' % (
596 |               tol2 + 0.01, tol2, ag_a['agree'], ag_a['values_beyond_tol'], ag_b['agree']))
597 |     # 一段目は無操作の値も比べる（裁定 D233）: 書き換えの道の無操作の値だけをずらすと一致しない（効き目は同じ）
598 |     tol1 = T3['independent_recompute']['tol_stage1']
599 |     rw_c = copy.deepcopy(v_rw)
600 |     rw_c[rid0]['noop_lo'] += tol1 + 1e-3
601 |     ag_c = AZ.recompute_agreement(T3d, T3['main_rows'], eff_all, pair_names, v_hook, rw_c, pilot, rows_subset=set(v_hook))
602 |     check(G2, '一段目は無操作の値も比べる（書き換えの道の無操作の値だけをずらすと一致しない・裁定 D233）', not ag_c['first']['agree'] and ag_c['second']['agree'],
603 |           'ずらした量 %.4f（一段目の許容 %s）→ 一段目の一致 %s・差の最大 %.2e' % (tol1 + 1e-3, tol1, ag_c['first']['agree'], ag_c['first']['max_abs_diff']))
604 |     # 乙（裁定 D227）: B-lens の層二の文脈で、門の行の符号で流す
605 |     FB = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
606 |     CB = json.load(open(os.path.join(REPO, 'results', 'Blens', 'calib-Blens.json'), encoding='utf-8'))['magnitude']['letter']
607 |     sec_rows = AZ.secondary_rows(T3, rows_gate, FB)
608 |     same_rows = all(sorted(n for n, _, _ in sec_rows.get(cell, [])) == sorted(CB[cell]['rows']) for cell in CB)
609 |     check(G2, '乙の行が B-lens の層二の答えの文字の位置の行と同じ（裁定 D227）', same_rows and set(sec_rows) == set(CB), '升目 %d・行 %d' % (len(sec_rows), sum(len(v) for v in sec_rows.values())))
610 |     ctx_all = BR.secondary_contexts(tok, T3, FJ, FB, REPO)
611 |     pick = [c for c in ctx_all if c[0] == 'S1|O-Ncold|prose'][:1] + [c for c in ctx_all if c[0] == 'S4|Osec-Ncold|json'][:1]
612 |     sec = BR.run_secondary(R, pick, sec_rows)
613 |     ok_sec = len(ctx_all) == sum(len(v) for v in FB['facts']['E']['selected'].values()) and all(set(s['rows']) == {n for n, _, _ in sec_rows[pick[i][2].key]} for i, s in enumerate(sec)) and \
614 |         sec[0]['n_batches'] == len({sg for _, _, sg in sec_rows[pick[0][2].key]})
615 |     cnt = AZ.secondary_counts(FB, sec_rows)
616 |     check(G2, '乙を流せる（文脈を組み・行の符号ごとに無操作と同じバッチ）', ok_sec, '文脈 %d（流したのは %d）・乙の行の順伝播 %d・符号のバッチ %d' % (len(ctx_all), len(pick), cnt['row_passes'], cnt['sign_batches']))
617 |     E2 = FJ['facts']['E']
618 |     check(G2, '乙の順伝播の数が転記行 E と同じ（集計の器の数え方と、設計事実の器の転記行 C の門の行からの数え方）',
619 |           (cnt['row_passes'], cnt['sign_batches'], cnt['contexts']) == (E2['passes_secondary'], E2['batches_secondary'], E2['contexts_secondary']),
620 |           '集計の器 %d・%d・%d／転記行 E %d・%d・%d' % (cnt['row_passes'], cnt['sign_batches'], cnt['contexts'], E2['passes_secondary'], E2['batches_secondary'], E2['contexts_secondary']))
621 |     summ2 = AZ.secondary_summary(sec, CB)
622 |     check(G2, '乙のまとめに B-lens の直接の経路の値を並べる', all(v.get('blens_direct') is not None for v in summ2.values()), '行 %d' % len(summ2))
623 |     # ---- 端から端まで（作った下見の記録の分かれ道・意見伺いの C1-C1・C2-A4・起動器の出力と同じ JSON の往復・等方は e2e_iso 本）
624 |     import sweep_Bl3 as SW
625 |     import build_report_Bl3 as BRP
626 |     import transformers
627 |     sess = {'commit': 'dry-e2e', 'dry': True, 'gpu': 'cpu', 'versions': {'numpy': np.__version__, 'torch': torch.__version__, 'transformers': transformers.__version__},
628 |             'canon_sha16': sha16f(os.path.join(REPO, 'design', 'contrasts-Bl3.json')), 'directions_npz_sha256': DJ['npz_sha256'], 'layer_idx': L, 'coef': coef, 'finished': 'dry-e2e'}
629 |     sec_part = rt({'part': 'secondary', 'rows_by_cell': sec_rows, 'counts': cnt, 'contexts': sec})
630 |     preds = {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '一部の升目を外して続ける'}}
631 |     meta_ = {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}
632 |     names_e = dict(names_, iso=names_['iso'][:e2e_iso])
633 |     sets_e = BR.cell_sign_sets(T3, None, names_e['named'], names_e['B_random'], names_e['iso'], names_e['real'], gate_only)
634 | 
635 |     def e2e(pilot_e):
636 |         """作った下見の記録で、起動器の相 main の三つの組の出力を作り、手元の一致だけを見る段・結果を開く段・掃き出し・報告の組み立て・走査まで通す。
637 |         組の置き場の session は DRY の形（等方を減らすため・裁定 D236 で DRY でない形は等方が正本の本数でなければ止まる）で、独立の再計算は下見で外した升目の行を除く
638 |         v̂ の行のすべてを流す。結果を開く段は、一致だけを見る段が読んだ出力の同定と照らしてから開く（裁定 D236）。"""
639 |         pilot_e = rt(pilot_e)
640 |         MPe = BR.run_main_phase(R, T3, FJ, cells, names_e, pilot_e, iso_n=None, log=lambda s: None)
641 |         rows_e, dbr_e = K.recompute_set(T3['main_rows'], pair_names, swaps, len(names_e['iso']), MPe['dropped'])
642 |         hook_e = BR.recompute_hook_path(R, [(n, cells[ck], s) for n, ck, s in rows_e], dbr_e)
643 |         rw_e = rewrite(RW, model, tok, rows_e, dbr_e, dirs, L, coef)
644 |         parts = collections.OrderedDict([('main', rt(dict(MPe, part='main'))), ('recompute', rt({'part': 'recompute', 'rows': rows_e, 'n_iso': len(names_e['iso']), 'hook': hook_e, 'rewrite': rw_e})),
645 |                                          ('secondary', sec_part)])
646 |         sessions = collections.OrderedDict((p, dict(sess)) for p in parts)
647 |         files = collections.OrderedDict((p_, {'dir': 'e2e', 'json_sha256': hashlib.sha256(json.dumps(v_, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest().upper(),
648 |                                               'session_sha256': 'dry'}) for p_, v_ in parts.items())
649 |         J = AZ.judge(T3, parts, sessions, [pilot_e], pair_names, files)
650 |         A = rt(AZ.open_checked(T3, FJ, parts, sessions, files, J, [pilot_e], pair_names, AN, CB, FB))
651 |         bad_files = copy.deepcopy(files)
652 |         bad_files['main']['json_sha256'] = '0' * 64
653 |         bind_stop = err_of(lambda: AZ.open_checked(T3, FJ, parts, sessions, bad_files, J, [pilot_e], pair_names, AN, CB, FB), SystemExit)
654 |         miss = SW.sweep(T3, A)
655 |         text = BRP.build(T3, A, preds, meta_, [], None, '起草者の行（合成）')
656 |         V, _ = BRP.lint_report(text, T3)
657 |         return {'MP': MPe, 'rows': rows_e, 'J': J, 'A': A, 'miss': miss, 'text': text, 'V': V, 'pilot': pilot_e, 'bind_stop': bind_stop}
658 |     # 分かれ道一: 主の升目 N1|O-Ncold と門の行だけの升目を (i)(ii) で外した下見の記録（正本の決定の関数で作る）
659 |     drop_cells = ['N1|O-Ncold'] + gate_only_cells[:1]
660 |     pilot_d = copy.deepcopy(pilot)
661 |     pilot_d['decision'] = K.cells_decision({c: c not in drop_cells for c in cell_keys}, {c: c not in drop_cells for c in gate_only_cells}, T3['pilot']['decision']['cells_min_pass'])
662 |     for c in drop_cells:
663 |         pilot_d['cells'][c]['pass_i_ii'] = False
664 |     ED = e2e(pilot_d)
665 |     Ad = ED['A']
666 |     dset = set(drop_cells)
667 |     dropped_rows = [r['id'] for r in T3['main_rows'] if '%s|%s' % (r['scenario'], r['base']) in dset]
668 |     left_static = [r['id'] for r in T3['main_rows'] if r['direction'] == 'static' and r['id'] not in dropped_rows]
669 |     tag_d = '端から端まで・外した升目（主の升目 N1|O-Ncold と門の行だけの升目 %s）' % gate_only_cells[0]
670 |     check(G2, tag_d + ': 本の計算と独立の再計算は外した升目の組と行を流さない',
671 |           list(ED['MP']['cells']) == [s[0] for s in sets_e if s[1] not in dset] and [x[0] for x in ED['rows']] == left_static and ED['pilot']['decision']['q1'] == '一部の升目を外して続ける',
672 |           '升目と符号 %d（外す前 %d）・独立の再計算の v̂ の行 %d・下見の決定 %s（外した升目 %s）' % (len(ED['MP']['cells']), len(sets_e), len(ED['rows']), ED['pilot']['decision']['q1'],
673 |                                                                               '・'.join(ED['pilot']['decision']['dropped'])))
674 |     check(G2, tag_d + ': 結果を開く段は、一致だけを見る段が読んだ出力と違う出力を開かない（裁定 D236）', ED['bind_stop'] is not None and '読んだ出力と違う' in ED['bind_stop'],
675 |           (ED['bind_stop'] or '')[:70])
676 |     check(G2, tag_d + ': 一致だけを見る段が二段とも一致', ED['J']['agree'] and ED['J']['first'] and ED['J']['second'],
677 |           '一段目 %s・二段目 %s・二段目の値 %s' % (ED['J']['first'], ED['J']['second'], '許容の内' if ED['J'].get('second_values_within_tol') else '許容の外'))
678 |     n_gate_left = sum(1 for r in rows_gate if r['cell'] not in dset)
679 |     by_left = dict(collections.Counter(r['direction'] for r in T3['main_rows'] if r['id'] not in dropped_rows))
680 |     gm = Ad['gates']['main']
681 |     check(G2, tag_d + ': 札の行・Holm の段・門の行・偶然の目安を残った行で数え直す',
682 |           Ad['rows_meta']['m_rows'] == len(T3['main_rows']) - len(dropped_rows) and Ad['rows_meta']['dropped_rows'] == dropped_rows and gm['n_rows'] == n_gate_left and
683 |           Ad['chance']['rows_by_direction'] == by_left and Ad['chance']['oriented'] < Ad['chance']['canon_all_rows']['oriented'],
684 |           'Holm の段 %d・外した行 %d・本の門の行 %d（段階 B の門の行 %d）・偶然の目安 向き %.4f（外す前 %.4f）' % (
685 |               Ad['rows_meta']['m_rows'], len(Ad['rows_meta']['dropped_rows']), gm['n_rows'], len(rows_gate), Ad['chance']['oriented'], Ad['chance']['canon_all_rows']['oriented']))
686 |     check(G2, tag_d + ': 掃き出しに欠けが無く、報告が組めて走査の違反が無い', ED['miss'] == [] and ED['V'] == [] and '〈下見で一部を外した〉' in ED['text'],
687 |           '欠け %d・走査の違反 %d・報告 %d 行' % (len(ED['miss']), len(ED['V']), ED['text'].count(NL) + 1))
688 |     # 分かれ道二: バッチ一（(vi) の (a) が上限を超えたときの決定〔バッチ一・揺れの床は (b)〕だけを写しで作り、下見の残りの段は走らせる器のまま）
689 |     orig_vi = K.vi_decision
690 |     K.vi_decision = lambda sa, sb, nm, bd: (lambda d: d if d['stop'] else dict(d, batch=1, floor=float(sb)))(orig_vi(sa, sb, nm, bd))
691 |     try:
692 |         pilot_1 = BR.run_pilot(R, [cells[k] for k in cell_keys], [cells[k] for k in gate_only_cells], T3, variants, stage_b_rate, T3['inputs']['sampling_B'])
693 |     finally:
694 |         K.vi_decision = orig_vi
695 |     check(G2, '下見のバッチ一の枝（(vi) の決定だけをバッチ一にした写し）が機械の決定まで走る', pilot_1.get('batch') == 1 and pilot_1.get('floor') == pilot_1['vi']['decision']['spread_b'] and
696 |           all(k in pilot_1 for k in ('iii', 'iv', 'v', 'decision')),
697 |           'バッチ %s・揺れの床 %.2e・近道の許容 %.4f・(v) の近道 %s（記述）・決定 %s' % (pilot_1.get('batch'), pilot_1.get('floor'), pilot_1.get('cache_tol'), pilot_1['v']['shortcut'], pilot_1['decision']['q1']))
698 |     EB = e2e(pilot_1)
699 |     Ab = EB['A']
700 |     nb_ok = len(EB['MP']['cells']) == len(sets_e) and all(o['n_batches'] == len(s[3]) + 1 for s, o in zip(sets_e, EB['MP']['cells'].values()))
701 |     s2b = Ab['recompute']['second']
702 |     check(G2, '端から端まで・バッチ一: 本の計算は方向ごとに一つのバッチで流し、二段目の二つの道は同じ計算になる（差が零・正本 `independent_recompute.stages.second.note`）',
703 |           EB['MP']['batch'] == 1 and nb_ok and s2b['max_abs_diff'] == 0.0, 'バッチ %s・升目と符号 %d・二段目の効き目の差の最大 %.2e' % (EB['MP']['batch'], len(EB['MP']['cells']), s2b['max_abs_diff']))
704 |     check(G2, '端から端まで・バッチ一: 一致だけを見る段が二段とも一致', EB['J']['agree'] and EB['J']['first'] and EB['J']['second'],
705 |           '一段目 %s・二段目 %s・独立の再計算の v̂ の行 %d' % (EB['J']['first'], EB['J']['second'], len(EB['rows'])))
706 |     check(G2, '端から端まで・バッチ一: 掃き出しに欠けが無く、報告が組めて走査の違反が無い', EB['miss'] == [] and EB['V'] == [] and Ab['main_run']['batch'] == 1,
707 |           '欠け %d・走査の違反 %d・報告 %d 行' % (len(EB['miss']), len(EB['V']), EB['text'].count(NL) + 1))
708 |     # 三. 壊した読み取りと近道の元
709 |     Rd = runner(BR.Runner(model, T3, L, coef, dirs, bug='double_norm'))
710 |     ld = Rd.logit_check(c0, T3['computation']['logit_tol'])
711 |     check(G3, '二重の正規化の読み取りを、出口の値の自己検査が止める', not ld['pass'], '差の最大 %.3f（許容 %s）' % (ld['max_abs'], ld['tol']))
712 |     first = None
713 |     try:
714 |         BR.run_pilot(Rd, [cells[k] for k in cell_keys[:1]], [], T3, {}, stage_b_rate, T3['inputs']['sampling_B'])
715 |     except BR.ToolError as e_:
716 |         first = {'tool_error': str(e_)}
717 |     check(G3, '壊した読み取りで下見が器の誤りとして止まる（やり直しの流れの一度目）', first is not None, (first or {}).get('tool_error', '')[:60])
718 |     Rb = runner(BR.Runner(model, T3, L, coef, dirs, bug='cache_through_mp'))
719 |     check(G3, '主位置まで使い回す近道を、凍結した確かめ（assert）が止める（下見の (v) の近道）', raises(lambda: Rb.forward(c0, [K.NOOP, 'static'], sg0, pc=Rb.prefix_cache(c0), full=False), BR.ToolError),
720 |           '近道の元が主位置の手前で切れていない')
721 |     pcl = dict(Rb.prefix_cache(c0), end=c0.mp)             # 主位置まで使い回した元に、主位置の手前で切ったと偽った切れ目を付ける
722 |     msg = err_of(lambda: R.forward(c0, [K.NOOP, 'static'], sg0, pc=pcl, full=False), BR.ToolError)
723 |     RB.assert_no_hooks(model, L)
724 |     check(G3, '記録した切れ目を偽った近道の元を、使い回す cache の列の実の長さの確かめが止める（裁定 D231）', msg is not None and '使い回す cache の列の長さ' in msg, (msg or '')[:70])
725 |     # 効き目で比べる確かめだけでは弱いこと（主位置の一つ分の加減の寄与の大きさ・記述）
726 |     V = np.stack([np.zeros(cfg.hidden_size, dtype=np.float32), dirs['static'].astype(np.float32)])
727 |     vals = []
728 |     for st in (c0.mp, c0.mp + 1):
729 |         h_ = RB.register_hook(model, L, RB.make_hook(V, coef, sg0, [st, st]))
730 |         cap = {}
731 |         hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
732 |         with torch.no_grad():
733 |             model(input_ids=torch.tensor([c0.ids] * 2), logits_to_keep=1)
734 |         h_.remove(); hh.remove()
735 |         ro = R.readout(cap['h'], c0, full=False)
736 |         vals.append(float(ro['lo'][1] - ro['lo'][0]))
737 |     check(G3, '（記述）主位置の一つ分の加減の寄与（効き目で比べる確かめの強さの目安）', True, '主位置から %.4f・主位置の次から %.4f・差 %.2e（近道の許容 %.4f）' % (vals[0], vals[1], vals[0] - vals[1], tol))
738 |     # （記述）本物の相対の加減の大きさに合わせた合成の方向で、突き合わせの力を測り直す（独立の再計算の個体の開発の記録の勧め）。
739 |     # 小さな模型では合成の方向のノルムが選んだ層の出力より二桁ほど大きく、効き目が飽和して、係数の二度掛けなどの誤りが一段目の許容の内に収まった。
740 |     # 方向を ‖v‖＝正本 `layers.vhat_over_h` の選んだ層の値 × 選んだ層の出力の主位置のノルム にそろえ、個体の器の変種（`bl3_recompute_rewrite._mutant_diffs`・中は変えない）と
741 |     # 主位置の一つ分の加減の寄与と、二段目の本の道とフックの差（意見伺いの C2-3.2）を測る。判定に入れない（合成の模型の上の目安）。
742 |     rw_rows = [(r['id'], '%s|%s' % (r['scenario'], r['base']), int(r['sign'])) for r in v_rows]
743 |     capL = {}
744 |     hL = direction_B.decoder_layers(model)[L].register_forward_hook(lambda m, i, o: capL.__setitem__('h', (o[0] if isinstance(o, tuple) else o).detach().clone()))
745 |     with torch.no_grad():
746 |         model(input_ids=torch.tensor([cells[rw_rows[0][1]].ids]), logits_to_keep=1)
747 |     hL.remove()
748 |     RB.assert_no_hooks(model, L)
749 |     nh = float(capL['h'][0, cells[rw_rows[0][1]].mp].float().norm())
750 |     ratio = float(T3['layers']['vhat_over_h'][str(T3['layers']['selected_ratio'])])
751 |     first_real = 'real:' + pair_names[0]
752 |     scale = ratio * nh / float(np.linalg.norm(dirs['static']))
753 |     dirs_s = collections.OrderedDict((k, v * scale) for k, v in dirs.items() if k in ('static', 'iso:0', 'iso:1', first_real))
754 |     Rs = runner(BR.Runner(model, T3, L, coef, dirs_s))
755 |     dbr_s = {nm: [('static', s), ('iso:0', s), ('iso:1', s), (first_real, 1), (first_real, -1)] for nm, _, s in rw_rows}
756 |     hk_s = BR.recompute_hook_path(Rs, [(nm, cells[ck], s) for nm, ck, s in rw_rows], dbr_s)
757 |     M_s = RW._mutant_diffs(model, tok, T3, FJ, rw_rows, dirs_s, first_real, L, coef, hk_s)
758 |     emax = max(abs(e) for v in hk_s.values() for e in v['effects'].values())
759 |     check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、書き換えの道の変種とフックの道の差（一段目の許容と比べる・判定に入れない）', True,
760 |           '‖v‖／‖選んだ層の出力‖ %.4f・効き目の絶対値の最大 %.2e・%s（許容 %s）' % (ratio, emax, '・'.join('%s %.2e%s' % (k, d, '（許容の外）' if d > tol1 else '') for k, _, d, _ in M_s), tol1))
761 |     V2 = np.stack([np.zeros(cfg.hidden_size, dtype=np.float32), dirs_s['static'].astype(np.float32)])
762 |     vals_s = []
763 |     for st in (c0.mp, c0.mp + 1):
764 |         h_ = RB.register_hook(model, L, RB.make_hook(V2, coef, sg0, [st, st]))
765 |         cap = {}
766 |         hh = model.model.norm.register_forward_pre_hook(lambda m, a: cap.__setitem__('h', a[0][:, -1, :].detach().clone()))
767 |         with torch.no_grad():
768 |             model(input_ids=torch.tensor([c0.ids] * 2), logits_to_keep=1)
769 |         h_.remove(); hh.remove()
770 |         ro = R.readout(cap['h'], c0, full=False)
771 |         vals_s.append(float(ro['lo'][1] - ro['lo'][0]))
772 |     check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、主位置の一つ分の加減の寄与（判定に入れない）', True,
773 |           '主位置から %.3e・主位置の次から %.3e・差 %.2e（近道の許容 %.4f・一段目の許容 %s）' % (vals_s[0], vals_s[1], vals_s[0] - vals_s[1], tol, tol1))
774 |     # 二段目の本の道（近道なし・本のバッチの組み方）とフック（バッチ一）の差と、近道ありの本の道との比べ（全ての方向を同じ倍率で小さくした合成の方向・v̂ の二つの行の升目と符号）
775 |     dirs_S = collections.OrderedDict((k, v * scale) for k, v in dirs.items())
776 |     RS = runner(BR.Runner(model, T3, L, coef, dirs_S))
777 |     lines_S = []
778 |     for r in v_rows:
779 |         key = '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
780 |         ki = [i for i, s in enumerate(sets_run) if s[0] == key][0]
781 |         _, ck, sg, ds = sets_run[ki]
782 |         m_ = BR.run_cell_sign(RS, cells[ck], sg, ds, batch, seed, ki, pc=None, layer_dirs=(), keep_iso_layers=False)
783 |         s_ = BR.run_cell_sign(RS, cells[ck], sg, ds, batch, seed, ki, pc=RS.prefix_cache(cells[ck]), layer_dirs=(), keep_iso_layers=False)
784 |         hdirs = [('static', sg)] + [(d, sg) for d in names_['iso']] + [('real:' + p, sg) for p in comps]
785 |         h_S = BR.recompute_hook_path(RS, [(r['id'], cells[ck], sg)], {r['id']: hdirs})[r['id']]
786 |         dm = [abs(m_['effects'][d] - h_S['effects']['%s|%+d' % (d, s)]) for d, s in hdirs]
787 |         dsh = [abs(s_['effects'][d] - h_S['effects']['%s|%+d' % (d, s)]) for d, s in hdirs]
788 |         lines_S.append('%s: 近道なしの本の道とフックの差の最大 %.2e（許容の外 %d／%d）・近道ありの本の道とフックの差の最大 %.2e（許容の外 %d／%d）・無操作の近道ありとなしの差 %.2e・効き目の絶対値の最大 %.2e' % (
789 |             key, max(dm), sum(x > tol2 for x in dm), len(dm), max(dsh), sum(x > tol2 for x in dsh), len(dsh), s_['lo'][K.NOOP] - m_['lo'][K.NOOP], max(abs(x) for x in h_S['effects'].values())))
790 |     check(G3, '（記述）本物の相対の加減の大きさの合成の方向での、二段目の本の道とフックの差・近道ありの本の道との比べ（判定に入れない・二段目の許容 %.4f・意見伺いの C2-3.2）' % tol2, True, '／'.join(lines_S))
791 |     return {'pilot': pilot, 'pilot_batch1': pilot_1, 'n_forward': sum(r.n_forward for r in RUNNERS), 'rewrite_passes': RW_PASSES[0], 'seconds': round(time.time() - t0, 1),
792 |             'iso_n': iso_n, 'e2e_iso': e2e_iso, 'layers': cfg.num_hidden_layers, 'dim': cfg.hidden_size}
793 | 
794 | 
795 | # ---------------- 四. 別の個体の書き換えの器の自己検査と --dry ----------------
796 | def part_rewrite_tool():
797 |     G = '四'
798 |     dev = open(os.path.join(REPO, 'records', 'Bl3', 'tools', 'recompute-rewrite-dev-Bl3.md'), encoding='utf-8').read()
799 |     m = re.search(r'`tools/bl3_recompute_rewrite\.py`（v1・SHA16 ([0-9A-F]{16})', dev)
800 |     now16 = sha16f(os.path.join(HERE, 'bl3_recompute_rewrite.py'))
801 |     check(G, '書き換えの器が個体の開発の記録の版のまま（中は変えない）', bool(m) and m.group(1) == now16, '開発の記録 %s・今 %s' % (m.group(1) if m else None, now16))
802 |     outs = collections.OrderedDict()
803 |     for flag in ('--selftest', '--dry'):
804 |         t1 = time.time()
805 |         r = subprocess.run([sys.executable, os.path.join(HERE, 'bl3_recompute_rewrite.py'), flag], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO,
806 |                            env=dict(os.environ, PYTHONIOENCODING='utf-8'))
807 |         outs[flag] = {'returncode': r.returncode, 'stdout': r.stdout, 'stderr_tail': r.stderr[-1500:], 'seconds': round(time.time() - t1, 1)}
808 |         check(G, '書き換えの器の %s が通る（今の本の器の上で）' % flag, r.returncode == 0, '終わりの値 %d・%.0f 秒・出力 %d 行' % (r.returncode, time.time() - t1, len(r.stdout.splitlines())))
809 |     return outs
810 | 
811 | 
812 | # ---------------- 五. 起動器の三つの相を DRY で別のプロセスとして（裁定 D236） ----------------
813 | def part_boot(iso_n_boot):
814 |     """起動器の相 check・pilot・main（三つの組）を DRY で別のプロセスとして走らせ、集計の器の CLI の一致だけを見る段と結果を開く段・掃き出しの CLI・報告の組み立てと走査に通す。
815 |     一致だけを見る段の後に、組の出力の中身だけを変えた写し（置き場の名は同じ）で結果を開く段が止まることを確かめる。出力は一時の置き場に置き、終わりに消す。"""
816 |     G = '五'
817 |     import build_report_Bl3 as BRP
818 |     td = tempfile.mkdtemp(prefix='dry-boot-')
819 |     env = dict(os.environ, OP4B_DRY='1', OP4B_REPO_DIR=REPO, OP4B_OUT=td, OP4B_DRY_ISO=str(iso_n_boot), OP4B_DRY_SEC='2', OP4B_DRY_RC='2', PYTHONIOENCODING='utf-8')
820 |     run = lambda cmd, extra=None: subprocess.run([sys.executable] + cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, env=dict(env, **(extra or {})))
821 |     newest = lambda prefix: ([d for d in sorted(glob.glob(os.path.join(td, prefix + '-*'))) if os.path.isdir(d)] or [None])[-1]
822 |     t1 = time.time()
823 |     try:
824 |         r_c = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'check'})
825 |         dc = newest('check')
826 |         CK = json.load(open(os.path.join(dc, 'check.json'), encoding='utf-8')) if r_c.returncode == 0 and dc else {}
827 |         cells_ck = CK.get('cells') or {}
828 |         check(G, '起動器の三つの相（DRY・別のプロセス）: 相 check は順伝播を呼ばずに終わり、呼ばれた数と升目のトークンの並びの SHA16 を書く',
829 |               r_c.returncode == 0 and CK.get('forward_calls') == 0 and (CK.get('forward_guards') or 0) > 0 and bool(cells_ck) and all('ids_sha16' in v for v in cells_ck.values()),
830 |               '終わりの値 %d・順伝播を呼んだ数 %s・守り %s・升目 %d' % (r_c.returncode, CK.get('forward_calls'), CK.get('forward_guards'), len(cells_ck)))
831 |         r_p = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'pilot'})
832 |         dp = newest('pilot')
833 |         pj = os.path.join(dp, 'pilot.json') if dp else ''
834 |         r_m = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'main', 'OP4B_DRY_PILOT': pj}) if r_p.returncode == 0 else r_p
835 |         dm = newest('main')
836 |         S = json.load(open(os.path.join(dm, 'session.json'), encoding='utf-8')) if r_m.returncode == 0 and dm else {}
837 |         tags = [z.get('tag') for z in S.get('zips') or []]
838 |         check(G, '起動器の三つの相（DRY・別のプロセス）: 相 pilot と相 main が終わり、組ごとの出力の SHA-256 を session に書き、組ごとに zip を作る',
839 |               r_p.returncode == 0 and r_m.returncode == 0 and set(S.get('part_sha256') or {}) == set(('main', 'recompute', 'secondary')) and all('part-%s' % x in tags for x in ('main', 'recompute', 'secondary')),
840 |               '終わりの値 %d・%d・組の出力の SHA-256 %s・zip %s' % (r_p.returncode, r_m.returncode, sorted(S.get('part_sha256') or {}), tags))
841 |         jr, ar = os.path.join(td, 'judge.json'), os.path.join(td, 'analysis.json')
842 |         r_j = run(['tools/analyze_Bl3.py', 'judge', dm, '--pilot', pj, '--out', jr]) if dm else r_m
843 |         r_o = run(['tools/analyze_Bl3.py', 'open', dm, '--pilot', pj, '--judge-record', jr, '--out', ar]) if r_j.returncode == 0 else r_j
844 |         r_s = run(['tools/sweep_Bl3.py', ar]) if r_o.returncode == 0 else r_o
845 |         A = json.load(open(ar, encoding='utf-8')) if r_o.returncode == 0 else None
846 |         V = None
847 |         if A:
848 |             text = BRP.build(T3, A, {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '続ける'}}, {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}, [], None, '起草者の行（合成）')
849 |             V, _ = BRP.lint_report(text, T3)
850 |         check(G, '起動器の三つの相（DRY・別のプロセス）: 集計の器の CLI の一致だけを見る段・結果を開く段・掃き出しの CLI・報告の組み立てと走査が通る',
851 |               r_j.returncode == 0 and r_o.returncode == 0 and r_s.returncode == 0 and V == [] and bool((A or {}).get('inputs')),
852 |               '終わりの値 %d・%d・%d・走査の違反 %s・結果を開く段の記録に読んだ出力の同定 %s' % (r_j.returncode, r_o.returncode, r_s.returncode, None if V is None else len(V), bool((A or {}).get('inputs'))))
853 |         stopped_ok, out_t = False, ''
854 |         if dm and r_j.returncode == 0:
855 |             t2 = os.path.join(td, 'tampered')
856 |             os.makedirs(t2)
857 |             dt = os.path.join(t2, os.path.basename(dm))                  # 置き場の名は同じにして、組の中身だけを変える
858 |             shutil.copytree(dm, dt)
859 |             Mt = json.load(open(os.path.join(dt, 'main.json'), encoding='utf-8'))
860 |             k0 = next(iter(Mt['cells']))
861 |             d0 = 'Nk' if 'Nk' in Mt['cells'][k0]['effects'] else next(iter(Mt['cells'][k0]['effects']))
862 |             Mt['cells'][k0]['effects'][d0] += 1000.0
863 |             json.dump(Mt, open(os.path.join(dt, 'main.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
864 |             at = os.path.join(td, 'analysis-tampered.json')
865 |             r_t = run(['tools/analyze_Bl3.py', 'open', dt, '--pilot', pj, '--judge-record', jr, '--out', at])
866 |             out_t = r_t.stdout + r_t.stderr
867 |             stopped_ok = r_t.returncode != 0 and '読んだ出力と違う' in out_t and not os.path.exists(at)
868 |         check(G, '起動器の三つの相（DRY・別のプロセス）: 一致だけを見る段の後に組の出力の中身を変えると、結果を開く段が止まって書かない（裁定 D236）', stopped_ok,
869 |               ('・'.join([l for l in out_t.split(NL) if '読んだ出力と違う' in l][:1]) or '止まらなかった'))
870 |     finally:
871 |         shutil.rmtree(td, ignore_errors=True)
872 |     return round(time.time() - t1, 1)
873 | 
874 | 
875 | def main():
876 |     ap = argparse.ArgumentParser()
877 |     ap.add_argument('--force', action='store_true')
878 |     ap.add_argument('--iso', type=int, default=T3['nulls']['isotropic']['count'])
879 |     ap.add_argument('--e2e-iso', type=int, default=9, help='端から端までの分かれ道の等方の本数（既定 9）')
880 |     ap.add_argument('--out', default=None, help='試しの走りの出力の置き場（既定は records/Bl3/dry-run-Bl3-<日付>.md）')
881 |     a = ap.parse_args()
882 |     day = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
883 |     out = a.out or os.path.join(REPO, 'records', 'Bl3', 'dry-run-Bl3-%s.md' % day)
884 |     if os.path.exists(out) and not a.force:
885 |         raise SystemExit('既にある: %s' % out)
886 |     t0 = time.time()
887 |     sha_start = tool_shas()
888 |     part_pure()
889 |     info = part_model(a.iso, a.e2e_iso)
890 |     rw_out = part_rewrite_tool()
891 |     boot_s = part_boot(a.e2e_iso)
892 |     sha_end = tool_shas()
893 |     check('四', '走らせた器と正本と設計事実と方向の記録が、走りの始めと終わりで同じ', sha_start == sha_end, '%d ファイル%s' % (
894 |         len(sha_start), '' if sha_start == sha_end else '（変わった: %s）' % [k for k in sha_start if sha_start[k] != sha_end.get(k)]))
895 |     n_ok = sum(1 for r in RESULTS if r[2])
896 |     L_ = ['# B-lens 層三の合成データの確かめ（機械生成・`tools/dry_run_Bl3.py` %s・%s）' % (VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')), '',
897 |           '- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 %s・次元 %s・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。' % (
898 |               info.get('layers'), info.get('dim')),
899 |           '- 等方の方向の本数: %d（正本 %d）。端から端までの分かれ道の等方の本数 %s（作った下見の記録で・起動器の出力と同じ JSON の往復）。' % (a.iso, T3['nulls']['isotropic']['count'], info.get('e2e_iso')),
900 |           '- 順伝播: 走らせる器 %s 回・書き換えの道 %s 回（変種の計算と四・五の走りは数えない）・%.0f 秒（五の起動器の三つの相 %.0f 秒・等方 %s 本）。' % (
901 |               info.get('n_forward'), info.get('rewrite_passes'), time.time() - t0, boot_s, a.e2e_iso),
902 |           '- 確かめ: %d のうち %d が期待どおり。' % (len(RESULTS), n_ok), '',
903 |           '| 部 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|'] + [
904 |           '| %s | %s | %s | %s |' % (g, n, '期待どおり' if ok else '**期待と違う**', d.replace('|', '｜')) for g, n, ok, d in RESULTS] + [
905 |           '', '## 下見の記録（乱数の模型・値に意味は無い・経路の確かめ）', '', '```json',
906 |           json.dumps({k: v for k, v in info['pilot'].items() if k in ('logit_check', 'vi', 'batch', 'floor', 'cache_tol', 'iii', 'v', 'decision')}, ensure_ascii=False, indent=1, default=float), '```', '']
907 |     if info.get('pilot_batch1'):
908 |         L_ += ['## 下見のバッチ一の枝の記録（(vi) の決定だけをバッチ一にした写し・値に意味は無い）', '', '```json',
909 |                json.dumps({k: v for k, v in info['pilot_batch1'].items() if k in ('vi', 'batch', 'floor', 'cache_tol', 'v', 'decision')}, ensure_ascii=False, indent=1, default=float), '```', '']
910 |     for flag, o in rw_out.items():
911 |         L_ += ['## 四. 書き換えの器の %s の出力（終わりの値 %d・%.0f 秒・中は変えない器）' % (flag, o['returncode'], o['seconds']), '', '```text'] + o['stdout'].rstrip(NL).split(NL) + ['```', '']
912 |     L_ += ['## 凍結する版の SHA16（この記録を取った作業木・改行を LF にそろえた SHA-256 の頭 16 桁・走りの始めと終わりで同じことを確かめた）', '',
913 |            '- 器の一覧は凍結の器 `tools/freeze_Bl3.py` の `TOOLS` と、その import の閉包。下見の前の凍結の器が、この表を今の版と突き合わせる。', '',
914 |            '| ファイル | SHA16 |', '|---|---|'] + ['| %s | %s |' % kv for kv in sha_start.items()] + [
915 |            '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
916 |     open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(L_))
917 |     print('[dry_run_Bl3] wrote %s | %d/%d | %.0f s' % (os.path.relpath(out, REPO), n_ok, len(RESULTS), time.time() - t0))
918 |     sys.exit(0 if n_ok == len(RESULTS) else 1)
919 | 
920 | 
921 | if __name__ == '__main__':
922 |     main()
```
<<< 終: `tools/dry_run_Bl3.py` >>>

<<< 始: `records/Bl3/dry-run-Bl3-2026-09-25.md`（SHA16 1F573346E9112160） >>>
# B-lens 層三の合成データの確かめ（機械生成・`tools/dry_run_Bl3.py` v3・2026-09-25 17:35 UTC）

- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 4・次元 64・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。
- 等方の方向の本数: 1999（正本 1999）。端から端までの分かれ道の等方の本数 9（作った下見の記録で・起動器の出力と同じ JSON の往復）。
- 順伝播: 走らせる器 12120 回・書き換えの道 4983 回（変種の計算と四・五の走りは数えない）・19538 秒（五の起動器の三つの相 752 秒・等方 9 本）。
- 確かめ: 72 のうち 72 が期待どおり。

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
| 一 | 札の一致の中身（等方の内側の行の裾と側は比べない・等方の外の行の裾と側は比べる・裁定 D232） | 期待どおり | 内側の行の裾と側だけが違う → 同じ・外の行の裾が違う → 違う・外の行の側が違う → 違う |
| 一 | 下見で外した後の偶然の目安（外さなければ正本の値・外すと外した行の分だけ減る・裁定 D231） | 期待どおり | 外さない 0.3087・0.6057（正本 0.3087・0.6057）／N1｜O-Ncold を外す 0.2701・0.5300（行 14） |
| 一 | 比べる相手の除き方の錨（B-lens の凍結の OWN_PAIR と正本の兄弟の対・裁定 D231） | 期待どおり | 除いた対の数 {'static': 4, 'loaded': 4, 'Nk': 1, 'td': 1}・錨をずらした写しで止まる True・兄弟の対から自分の対を抜いた写しで止まる True |
| 一 | 正本の文から独立に書いた札と集計の器の札（等方 1999 本・外した升目 なし・裁定 D236） | 期待どおり | 行 16・食い違い 0・等方の外の行 12・Holm の段の数 16 |
| 一 | 正本の文から独立に書いた札と集計の器の札（等方 1999 本・外した升目 N1|O-Ncold・裁定 D236） | 期待どおり | 行 14・食い違い 0・等方の外の行 11・Holm の段の数 14 |
| 一 | 等方の外の行が出る枝（割合を決めた裾の比べは外の行だけ・q7 の行・裁定 D232・D236） | 期待どおり | 等方の外の行 12・内の行の裾を変える → 札は同じ・外の行の裾を変える → 札が違う・q7 の行 4 |
| 一 | 答えの分かる合成での門の組み立て（行の効き目を行動の量に置く・外した升目 なし・裁定 D236） | 期待どおり | 本の門の順位相関 1.000000000000・行 64（残った門の行 64）・選択 a の件数の門の順位相関 0.9977（一でない） |
| 一 | 答えの分かる合成での門の組み立て（行の効き目を行動の量に置く・外した升目 N1|O-Ncold・裁定 D236） | 期待どおり | 本の門の順位相関 1.000000000000・行 55（残った門の行 55）・選択 a の件数の門の順位相関 0.9978（一でない） |
| 二 | 升目の入力が転記行 B と一致する（実のトークナイザ） | 期待どおり | 9 升目 |
| 二 | 書き出しの割り方が変わる場合（器が止まる） | 期待どおり | 書き出しを一トークン欠いた入力で、転記行 B との突き合わせが止めた |
| 二 | 下見が機械の決定まで走る | 期待どおり | q1 続ける・(vi) (a) 4.81e-06 (b) 0.00e+00・バッチ 16・揺れの床 4.811094168388763e-06・近道の許容 0.005・(v) の近道 True（記述） |
| 二 | 出口の値の自己検査（下見の頭） | 期待どおり | 差の最大 7.70e-02（許容 0.5） |
| 二 | 本の計算の頭の出口の値の自己検査 | 期待どおり | 差の最大 7.70e-02（許容 0.5） |
| 二 | 本の計算は近道を使わない（振る舞い: 近道の元を作る呼び出し・使い回す cache・use_cache・列の全長を全ての順伝播で数えた・裁定 D236） | 期待どおり | 順伝播 1547 回・近道の元を作った回 0・cache を渡した回 0・use_cache が真の回 0・列の全長でない回 0 |
| 二 | 本の計算は近道を使わない（頭の近道の確かめを走らせない・下見の (v) は記述・裁定 D234） | 期待どおり | 下見の (v) の近道の決定 True・(v) の差の最大 3.77e-03（近道の許容 0.0050） |
| 二 | 最後の層の自己検査 | 期待どおり | 差 0.00e+00（許容 0.0001） |
| 二 | 本の計算: 全ての升目と符号・全ての方向と無操作がそろい、埋めた零のベクトルの値は使わない | 期待どおり | 升目と符号 17（組み立て 17） |
| 二 | 層ごとの差分の余弦を足した向き（符号を掛けた方向）と測る（減算の升目と符号でも正・裁定 D231） | 期待どおり | 選んだ層の次の層の static の余弦: 減算 1.000・加算 1.000 |
| 二 | 零のベクトルの行は無操作と同じ値になる（別のバッチでも） | 期待どおり | 効き目 0.00e+00（揺れの床 4.81e-06）・バッチの組を変えた同じ方向の効き目の差の最大 0.00e+00（記述） |
| 二 | 有限でない値の効き目は器の誤りで止まる（走らせる器の出口・裁定 D236） | 期待どおり | 有限でない値（升目と符号 S1｜O-Ncold｜-1 の対数オッズ・1 個・例 ['nan:test']） |
| 二 | バッチの中の位置で方向を取り違えない | 期待どおり | 位置を入れ替えた効き目の差の最大 9.47e-07 |
| 二 | （記述）近道ありと近道なしの効き目の差（近道は下見の (v) の記述だけ・本の計算は使わない・裁定 D234） | 期待どおり | 差の最大 0.00e+00（近道の許容 0.0050） |
| 二 | 層ごとの差分（主の組だけ・名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間だけ） | 期待どおり | 層 2・等方 1999 本・主の組の升目と符号 12 |
| 二 | 独立の再計算の組（v̂ の行ごとに無操作・v̂・等方の帰無・比べる相手の両方の向き・転記行 E と） | 期待どおり | v̂ の行 8・行ごとの順伝播 2049（等方 1999 本のとき・転記行 E の行ごと 2049 は等方 1999 本）・一つの道の順伝播 16392 |
| 二 | （記述）二段目の本の道（近道なし・本のバッチ）とフック（バッチ一）の効き目の差の最大（判定は札の一致・裁定 D234） | 期待どおり | 差の最大 7.16e-06（許容 0.0050・許容の内） |
| 二 | 門の行と様式の転位の行を段階 B の記録から作り直す（転記行 C と） | 期待どおり | 門の行 64・様式の転位の行 2 |
| 二 | 独立の再計算の行が欠ければ一致しない（本の計算の求め方） | 期待どおり | 欠けた行 6 |
| 二 | 集計の器が主の札・門・記述の門・予想の答えを出す | 期待どおり | 行 16・本の門の入れ替え 5040・v̂ を抜いた門 720・予想の答え {'q1.pilot': '続ける', 'q2.vhat_iso': '零', 'q3.nk_iso': '零', 'q4.gate': '通らない', 'q5.gate_wo_vhat': '通らない', 'q6.second': '零', 'q7.direction': None} |
| 二 | 集計の器の二段の一致（一段目は無操作の値と効き目の値と札・裁定 D233・二段目は札・裁定 D234） | 期待どおり | 一段目 True（無操作の値と効き目の差の最大 1.74e-06・許容 0.001）・二段目 True（効き目の差の最大 7.16e-06・許容 0.0050・許容の内・記録） |
| 二 | 二段目は札の一致で判定する（値だけが許容の外なら一致して印を残す・札が変われば一致しない・裁定 D234） | 期待どおり | 等方の帰無の端の一本を 0.0150 動かした（許容 0.0050）→ 一致 True・許容の外の印 True／二つ目の札の最上位を変えた → 一致 False |
| 二 | 一段目は無操作の値も比べる（書き換えの道の無操作の値だけをずらすと一致しない・裁定 D233） | 期待どおり | ずらした量 0.0020（一段目の許容 0.001）→ 一段目の一致 False・差の最大 2.00e-03 |
| 二 | 乙の行が B-lens の層二の答えの文字の位置の行と同じ（裁定 D227） | 期待どおり | 升目 9・行 64 |
| 二 | 乙を流せる（文脈を組み・行の符号ごとに無操作と同じバッチ） | 期待どおり | 文脈 180（流したのは 2）・乙の行の順伝播 1280・符号のバッチ 260 |
| 二 | 乙の順伝播の数が転記行 E と同じ（集計の器の数え方と、設計事実の器の転記行 C の門の行からの数え方） | 期待どおり | 集計の器 1280・260・180／転記行 E 1280・260・180 |
| 二 | 乙のまとめに B-lens の直接の経路の値を並べる | 期待どおり | 行 13 |
| 二 | 端から端まで・外した升目（主の升目 N1|O-Ncold と門の行だけの升目 S4|Osec-Ncold）: 本の計算と独立の再計算は外した升目の組と行を流さない | 期待どおり | 升目と符号 14（外す前 17）・独立の再計算の v̂ の行 7・下見の決定 一部の升目を外して続ける（外した升目 N1｜O-Ncold・S4｜Osec-Ncold） |
| 二 | 端から端まで・外した升目（主の升目 N1|O-Ncold と門の行だけの升目 S4|Osec-Ncold）: 結果を開く段は、一致だけを見る段が読んだ出力と違う出力を開かない（裁定 D236） | 期待どおり | 結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）: ['main'] |
| 二 | 端から端まで・外した升目（主の升目 N1|O-Ncold と門の行だけの升目 S4|Osec-Ncold）: 一致だけを見る段が二段とも一致 | 期待どおり | 一段目 True・二段目 True・二段目の値 許容の内 |
| 二 | 端から端まで・外した升目（主の升目 N1|O-Ncold と門の行だけの升目 S4|Osec-Ncold）: 札の行・Holm の段・門の行・偶然の目安を残った行で数え直す | 期待どおり | Holm の段 14・外した行 2・本の門の行 51（段階 B の門の行 64）・偶然の目安 向き 0.2701（外す前 0.3087） |
| 二 | 端から端まで・外した升目（主の升目 N1|O-Ncold と門の行だけの升目 S4|Osec-Ncold）: 掃き出しに欠けが無く、報告が組めて走査の違反が無い | 期待どおり | 欠け 0・走査の違反 0・報告 289 行 |
| 二 | 下見のバッチ一の枝（(vi) の決定だけをバッチ一にした写し）が機械の決定まで走る | 期待どおり | バッチ 1・揺れの床 0.00e+00・近道の許容 0.0050・(v) の近道 True（記述）・決定 続ける |
| 二 | 端から端まで・バッチ一: 本の計算は方向ごとに一つのバッチで流し、二段目の二つの道は同じ計算になる（差が零・正本 `independent_recompute.stages.second.note`） | 期待どおり | バッチ 1・升目と符号 17・二段目の効き目の差の最大 0.00e+00 |
| 二 | 端から端まで・バッチ一: 一致だけを見る段が二段とも一致 | 期待どおり | 一段目 True・二段目 True・独立の再計算の v̂ の行 8 |
| 二 | 端から端まで・バッチ一: 掃き出しに欠けが無く、報告が組めて走査の違反が無い | 期待どおり | 欠け 0・走査の違反 0・報告 294 行 |
| 三 | 二重の正規化の読み取りを、出口の値の自己検査が止める | 期待どおり | 差の最大 2.408（許容 0.5） |
| 三 | 壊した読み取りで下見が器の誤りとして止まる（やり直しの流れの一度目） | 期待どおり | 出口の値の自己検査が落ちた: {'cell': 'N1｜O-Ncold', 'max_abs': 2.407546997 |
| 三 | 主位置まで使い回す近道を、凍結した確かめ（assert）が止める（下見の (v) の近道） | 期待どおり | 近道の元が主位置の手前で切れていない |
| 三 | 記録した切れ目を偽った近道の元を、使い回す cache の列の実の長さの確かめが止める（裁定 D231） | 期待どおり | 使い回す cache の列の長さが主位置と違う（474・主位置 473）: N1｜O-Ncold |
| 三 | （記述）主位置の一つ分の加減の寄与（効き目で比べる確かめの強さの目安） | 期待どおり | 主位置から -2.7306・主位置の次から -2.7306・差 5.39e-06（近道の許容 0.0050） |
| 三 | （記述）本物の相対の加減の大きさの合成の方向での、書き換えの道の変種とフックの道の差（一段目の許容と比べる・判定に入れない） | 期待どおり | ‖v‖／‖選んだ層の出力‖ 0.0304・効き目の絶対値の最大 3.72e-01・M0 1.77e-06・M1 1.53e-02（許容の外）・M2 1.10e-01（許容の外）・M3 7.23e-01（許容の外）・M4 3.55e-01（許容の外）・M5 3.95e-02（許容の外）・M6 8.36e-02（許容の外）（許容 0.001） |
| 三 | （記述）本物の相対の加減の大きさの合成の方向での、主位置の一つ分の加減の寄与（判定に入れない） | 期待どおり | 主位置から -1.412e-01・主位置の次から -1.493e-01・差 8.12e-03（近道の許容 0.0050・一段目の許容 0.001） |
| 三 | （記述）本物の相対の加減の大きさの合成の方向での、二段目の本の道とフックの差・近道ありの本の道との比べ（判定に入れない・二段目の許容 0.0050・意見伺いの C2-3.2） | 期待どおり | N1｜O-Ncold｜-1: 近道なしの本の道とフックの差の最大 1.66e-05（許容の外 0／2024）・近道ありの本の道とフックの差の最大 1.66e-05（許容の外 0／2024）・無操作の近道ありとなしの差 0.00e+00・効き目の絶対値の最大 4.51e-01／N1｜Onull｜+1: 近道なしの本の道とフックの差の最大 1.66e-05（許容の外 0／2024）・近道ありの本の道とフックの差の最大 3.79e-02（許容の外 943／2024）・無操作の近道ありとなしの差 -3.77e-03・効き目の絶対値の最大 4.33e-01 |
| 四 | 書き換えの器が個体の開発の記録の版のまま（中は変えない） | 期待どおり | 開発の記録 012CB2B68397614A・今 012CB2B68397614A |
| 四 | 書き換えの器の --selftest が通る（今の本の器の上で） | 期待どおり | 終わりの値 0・51 秒・出力 52 行 |
| 四 | 書き換えの器の --dry が通る（今の本の器の上で） | 期待どおり | 終わりの値 0・237 秒・出力 22 行 |
| 五 | 起動器の三つの相（DRY・別のプロセス）: 相 check は順伝播を呼ばずに終わり、呼ばれた数と升目のトークンの並びの SHA16 を書く | 期待どおり | 終わりの値 0・順伝播を呼んだ数 0・守り 7・升目 9 |
| 五 | 起動器の三つの相（DRY・別のプロセス）: 相 pilot と相 main が終わり、組ごとの出力の SHA-256 を session に書き、組ごとに zip を作る | 期待どおり | 終わりの値 0・0・組の出力の SHA-256 ['main', 'recompute', 'secondary']・zip ['part-main', 'part-recompute', 'part-secondary'] |
| 五 | 起動器の三つの相（DRY・別のプロセス）: 集計の器の CLI の一致だけを見る段・結果を開く段・掃き出しの CLI・報告の組み立てと走査が通る | 期待どおり | 終わりの値 0・0・0・走査の違反 0・結果を開く段の記録に読んだ出力の同定 True |
| 五 | 起動器の三つの相（DRY・別のプロセス）: 一致だけを見る段の後に組の出力の中身を変えると、結果を開く段が止まって書かない（裁定 D236） | 期待どおり | 結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）: ['main'] |
| 四 | 走らせた器と正本と設計事実と方向の記録が、走りの始めと終わりで同じ | 期待どおり | 35 ファイル |

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
  "sentence": "positive",
  "transformed_def": "変換を通した値は、全語彙の出口の値に段階 B の標本化の変換（温度・top-k・top-p）を当てた後の選択肢 a の文字の確率で、選択の文字と refuse の頭の中で割り直さない（裁定 D235）"
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

## 下見のバッチ一の枝の記録（(vi) の決定だけをバッチ一にした写し・値に意味は無い）

```json
{
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
   "batch": 1,
   "floor": 0.0,
   "spread_a": 4.811094168388763e-06,
   "spread_b": 0.0
  }
 },
 "batch": 1,
 "floor": 0.0,
 "cache_tol": 0.005,
 "v": {
  "diffs": {
   "N1|O-Ncold": 0.0,
   "N1|Onull": -0.003780845336926575,
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

## 四. 書き換えの器の --selftest の出力（終わりの値 0・51 秒・中は変えない器）

```text
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

## 四. 書き換えの器の --dry の出力（終わりの値 0・237 秒・中は変えない器）

```text
bl3_recompute_rewrite v1 --dry  torch 2.9.1+cpu・transformers 4.57.3・numpy 2.4.2・注意の実装 sdpa
乱数の小さな模型: 次元 64・層 4・選んだ層の添字 1・係数 2.0・一段目の許容 independent_recompute.tol_stage1 = 0.001
行 sub:N1:O-Ncold-v~O-Ncold-vrand・升目 N1|O-Ncold（nuclear）・符号 -1・方向と符号 77 組（static 1・等方に見立てた 20・実在の差の名 28 本 × 両方の向き＝56）＋無操作
行 add:S1:Onull+v~Onull+vrand・升目 S1|Onull（survival）・符号 +1・方向と符号 77 組（static 1・等方に見立てた 20・実在の差の名 28 本 × 両方の向き＝56）＋無操作
残差の書き換えの道: 55.4 秒（順伝播 156 回）
フックの道: 66.3 秒
効き目の数 154・効き目の絶対値の最大（残差の書き換えの道）0.4261
差の絶対値の最大: 効き目 2.54e-07・無操作の量 6.72e-08
dry: 一段目の許容（0.001）の内（効き目の差の最大 2.54e-07）
（正本 independent_recompute.agreement の札の一致〔Holm の判定・裾・等方の外の行の側・二つ目の札〕は、この器では見ていない）
参考: 読み取りの float32 の丸めの目安（同じ最終の正規化の入力を float64 で読み直した量との差の最大・無操作と static・2 行）6.8e-08
参考: フックの道の後に走らせ直した残差の書き換えの道（無操作と static・2 行）が一度目と同じ（ビット単位）: 同じ
参考: use_cache=False の形の残差の書き換えの道（61.8 秒）——既定の形との差の最大 効き目 0・無操作 0／フックの道との差の最大 効き目 2.54e-07・無操作 6.72e-08
[歯] M0 誤らせない（対照）: フックの道との効き目の差の最大 1.29e-07（10 個の効き目）→ 許容の内（対照として期待どおり）（許容 0.001）
[歯] M1 帯の起点を主位置の一つ後にする: フックの道との効き目の差の最大 0.000344（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）
[歯] M2 書き換える層を一つ後にする: フックの道との効き目の差の最大 0.00154（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）
[歯] M3 符号を反転する: フックの道との効き目の差の最大 0.565（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）
[歯] M4 係数を二度掛ける（sign×coef×coef×v）: フックの道との効き目の差の最大 0.000902（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）
[歯] M5 読み取りで正規化を二度当てる: フックの道との効き目の差の最大 0.0459（10 個の効き目）→ 許容の外＝捕まえた（許容 0.001）
[歯] M6 読み取りを bf16 で当てる: フックの道との効き目の差の最大 0.000578（10 個の効き目）→ 許容の内＝捕まえなかった（この模型での盲点）（許容 0.001）
[歯] 変種の計算 21.4 秒（参考・判定に入れない）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
```

## 凍結する版の SHA16（この記録を取った作業木・改行を LF にそろえた SHA-256 の頭 16 桁・走りの始めと終わりで同じことを確かめた）

- 器の一覧は凍結の器 `tools/freeze_Bl3.py` の `TOOLS` と、その import の閉包。下見の前の凍結の器が、この表を今の版と突き合わせる。

| ファイル | SHA16 |
|---|---|
| tools/analyze_Bl3.py | 86070F3268E10CC0 |
| tools/bl3_core.py | 609BC36E01068365 |
| tools/bl3_directions.py | 4BE7E44D135849F4 |
| tools/bl3_facts.py | FE85B9500932B658 |
| tools/bl3_recompute_rewrite.py | 012CB2B68397614A |
| tools/bl3_run.py | 46071CD97AB10819 |
| tools/blens_core.py | DB3092B1EF0B88B3 |
| tools/blens_lens.py | CB2A138EDFFB8732 |
| tools/build_draft_Bl3.py | 76B6F8B115B9BFEF |
| tools/build_report_Bl3.py | 11010753B98162E5 |
| tools/colab/boot_Bl3.py | 6E210F2613E12DD1 |
| tools/colab/boot_Blens.py | E1B7270F3A2385AC |
| tools/direction_B.py | E84A101655685F2B |
| tools/dry_run_Bl3.py | 5FF650A8B106834D |
| tools/freeze_Bl3.py | EFCD14D5426693B2 |
| tools/make_contrasts_Bl3.py | 17FDA710CB772086 |
| tools/make_frozen_B.py | A333488A9437EF68 |
| tools/make_frozen_Bl3.py | 8DF4EA70CC3EAB15 |
| tools/make_predictions_form_B.py | A213804DCB730737 |
| tools/make_predictions_form_Bl3.py | 6305BB5766F0F6B6 |
| tools/numbers_lint.py | 88B6A53BBEC80602 |
| tools/qf_task_B.py | 86D71D789BB7A320 |
| tools/report_lint.py | 1F145D63983929EE |
| tools/response_mode_A.py | C3E90B11B62F67A5 |
| tools/rules_B.py | 4A89BE41F817A8F0 |
| tools/run_stageB_local.py | E976A4F5B63767FA |
| tools/runs_A.py | A57BE1F5EEACBBB2 |
| tools/runs_B.py | 269B60867D0924EB |
| tools/seal_Bl3.py | 0041BA954F094E21 |
| tools/steer_B.py | 71157C6921E12AC7 |
| tools/sweep_Bl3.py | 2113222FB10DF222 |
| design/contrasts-Bl3.json | 4531FC51D7075C36 |
| records/Bl3/design-facts-Bl3.json | 2630D829032C2E08 |
| records/Bl3/design-facts-Bl3.md | CFBFF4CADFC9E0CA |
| results/Bl3/directions-Bl3.json | 7341FE092523936E |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/dry-run-Bl3-2026-09-25.md` >>>

<<< 始: `records/Bl3/tools/trials/dry-trial-9-Bl3.md`（SHA16 57CB99F2140F9820） >>>
# 合成データの器 v3 の試しの九度目（等方 49 本・分かれ道と起動器の三つの相は 9 本）（機械生成・`records/Bl3/tools/trials/log_to_record.py`・走りの印字から切り出した）

- 注: 確かめはすべて走り終えた後、記録を書く所で器が止まった（確かめの詳しくを文字列でなく並びで渡した一行・直しは器の段の記録 §13）。走りの始めと終わりの版の SHA16 の確かめは通った。
- 走りの印字の SHA-256（手元の置き場の道筋を置き換える前）: 297DB080AB8CBA768DEEE2E14AA2F88A3650F755081A49B553C1EB158988714D
- 確かめの行: 72 のうち 72 が期待どおり（印字の行をそのまま並べた・部と結果の札のほかは一字も変えていない）。

| 部 | 結果 | 確かめと詳しく（印字のまま） |
|---|---|---|
| 一 | 期待どおり | 奇でない押し（逆の符号の升目の効き目をそのまま使う） 正しい呼び方 ρ 1.000／反転で代えた呼び方 ρ -0.012 |
| 一 | 期待どおり | 零でない帰無の中心 反対の側の値: 等しい裾 0.0010・対称 1.0000／中心の値: 等しい裾 0.984 |
| 一 | 期待どおり | 減算の行（符号の二重掛け） 符号 +1 ρ 1.000／二重掛け ρ -1.000 |
| 一 | 期待どおり | 下見で外れる升目と門の行だけの升目 入れ替え 120 → 外した後 24（行 4・行の無くなった単位を外した）・Holm の第一段 0.003125 → 0.003571 |
| 一 | 期待どおり | 帰無との同じ値 上の裾 4・下の裾 3（同じ値を両方に数える）・同じ距離の比べる相手があれば最上位にしない |
| 一 | 期待どおり | 両方の向きがちょうど対称な比べる相手 中心 0.00e+00・向きの順位 31・対の順位 16 |
| 一 | 期待どおり | 端数のバッチ（零のベクトルで埋める） バッチ 128・埋める 13・無操作 1 |
| 一 | 期待どおり | 零の近くの中央値（符号だけ） 四分位 [-0.582, 0.724] |
| 一 | 期待どおり | Holm の境で一本違う p（札の一致の判定） p 0.0030 → 0.0040・Holm の判定 True → False・一致 False |
| 一 | 期待どおり | 器の誤りでやり直す流れ（q1 の採点） やり直した下見で採点・一度目の決定を併記・やり直さなければ採点しない |
| 一 | 期待どおり | 掃き出し（要る組が本の計算の組み立てにそろう） 要る組 24527・組み立て 24527・足りない 0 |
| 一 | 期待どおり | 本の計算の順伝播の数（転記行 E と） 組み立て 24527・転記行 E 24408 ＋ 7 ＋ 112 |
| 一 | 期待どおり | 札の一致の中身（等方の内側の行の裾と側は比べない・等方の外の行の裾と側は比べる・裁定 D232） 内側の行の裾と側だけが違う → 同じ・外の行の裾が違う → 違う・外の行の側が違う → 違う |
| 一 | 期待どおり | 下見で外した後の偶然の目安（外さなければ正本の値・外すと外した行の分だけ減る・裁定 D231） 外さない 0.3087・0.6057（正本 0.3087・0.6057）／N1｜O-Ncold を外す 0.2701・0.5300（行 14） |
| 一 | 期待どおり | 比べる相手の除き方の錨（B-lens の凍結の OWN_PAIR と正本の兄弟の対・裁定 D231） 除いた対の数 {'static': 4, 'loaded': 4, 'Nk': 1, 'td': 1}・錨をずらした写しで止まる True・兄弟の対から自分の対を抜いた写しで止まる True |
| 一 | 期待どおり | 正本の文から独立に書いた札と集計の器の札（等方 1999 本・外した升目 なし・裁定 D236） 行 16・食い違い 0・等方の外の行 12・Holm の段の数 16 |
| 一 | 期待どおり | 正本の文から独立に書いた札と集計の器の札（等方 1999 本・外した升目 N1｜O-Ncold・裁定 D236） 行 14・食い違い 0・等方の外の行 11・Holm の段の数 14 |
| 一 | 期待どおり | 等方の外の行が出る枝（割合を決めた裾の比べは外の行だけ・q7 の行・裁定 D232・D236） 等方の外の行 12・内の行の裾を変える → 札は同じ・外の行の裾を変える → 札が違う・q7 の行 4 |
| 一 | 期待どおり | 答えの分かる合成での門の組み立て（行の効き目を行動の量に置く・外した升目 なし・裁定 D236） 本の門の順位相関 1.000000000000・行 64（残った門の行 64）・選択 a の件数の門の順位相関 0.9977（一でない） |
| 一 | 期待どおり | 答えの分かる合成での門の組み立て（行の効き目を行動の量に置く・外した升目 N1｜O-Ncold・裁定 D236） 本の門の順位相関 1.000000000000・行 55（残った門の行 55）・選択 a の件数の門の順位相関 0.9978（一でない） |
| 二 | 期待どおり | 升目の入力が転記行 B と一致する（実のトークナイザ） 9 升目 |
| 二 | 期待どおり | 書き出しの割り方が変わる場合（器が止まる） 書き出しを一トークン欠いた入力で、転記行 B との突き合わせが止めた |
| 二 | 期待どおり | 下見が機械の決定まで走る q1 続ける・(vi) (a) 4.81e-06 (b) 0.00e+00・バッチ 16・揺れの床 4.811094168388763e-06・近道の許容 0.005・(v) の近道 True（記述） |
| 二 | 期待どおり | 出口の値の自己検査（下見の頭） 差の最大 7.70e-02（許容 0.5） |
| 二 | 期待どおり | 本の計算の頭の出口の値の自己検査 差の最大 7.70e-02（許容 0.5） |
| 二 | 期待どおり | 本の計算は近道を使わない（振る舞い: 近道の元を作る呼び出し・使い回す cache・use_cache・列の全長を全ての順伝播で数えた・裁定 D236） 順伝播 83 回・近道の元を作った回 0・cache を渡した回 0・use_cache が真の回 0・列の全長でない回 0 |
| 二 | 期待どおり | 本の計算は近道を使わない（頭の近道の確かめを走らせない・下見の (v) は記述・裁定 D234） 下見の (v) の近道の決定 True・(v) の差の最大 3.77e-03（近道の許容 0.0050） |
| 二 | 期待どおり | 最後の層の自己検査 差 0.00e+00（許容 0.0001） |
| 二 | 期待どおり | 本の計算: 全ての升目と符号・全ての方向と無操作がそろい、埋めた零のベクトルの値は使わない 升目と符号 17（組み立て 17） |
| 二 | 期待どおり | 層ごとの差分の余弦を足した向き（符号を掛けた方向）と測る（減算の升目と符号でも正・裁定 D231） 選んだ層の次の層の static の余弦: 減算 1.000・加算 1.000 |
| 二 | 期待どおり | 零のベクトルの行は無操作と同じ値になる（別のバッチでも） 効き目 0.00e+00（揺れの床 4.81e-06）・バッチの組を変えた同じ方向の効き目の差の最大 0.00e+00（記述） |
| 二 | 期待どおり | 有限でない値の効き目は器の誤りで止まる（走らせる器の出口・裁定 D236） 有限でない値（升目と符号 S1｜O-Ncold｜-1 の対数オッズ・1 個・例 ['nan:test']） |
| 二 | 期待どおり | バッチの中の位置で方向を取り違えない 位置を入れ替えた効き目の差の最大 9.47e-07 |
| 二 | 期待どおり | （記述）近道ありと近道なしの効き目の差（近道は下見の (v) の記述だけ・本の計算は使わない・裁定 D234） 差の最大 0.00e+00（近道の許容 0.0050） |
| 二 | 期待どおり | 層ごとの差分（主の組だけ・名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間だけ） 層 2・等方 49 本・主の組の升目と符号 12 |
| 二 | 期待どおり | 独立の再計算の組（v̂ の行ごとに無操作・v̂・等方の帰無・比べる相手の両方の向き・転記行 E と） v̂ の行 8・行ごとの順伝播 99（等方 49 本のとき・転記行 E の行ごと 2049 は等方 1999 本）・一つの道の順伝播 792 |
| 二 | 期待どおり | （記述）二段目の本の道（近道なし・本のバッチ）とフック（バッチ一）の効き目の差の最大（判定は札の一致・裁定 D234） 差の最大 4.92e-06（許容 0.0050・許容の内） |
| 二 | 期待どおり | 門の行と様式の転位の行を段階 B の記録から作り直す（転記行 C と） 門の行 64・様式の転位の行 2 |
| 二 | 期待どおり | 独立の再計算の行が欠ければ一致しない（本の計算の求め方） 欠けた行 6 |
| 二 | 期待どおり | 集計の器が主の札・門・記述の門・予想の答えを出す 行 16・本の門の入れ替え 5040・v̂ を抜いた門 720・予想の答え {'q1.pilot': '続ける', 'q2.vhat_iso': '零', 'q3.nk_iso': '零', 'q4.gate': '通らない', 'q5.gate_wo_vhat': '通らない', 'q6.second': '零', 'q7.direction': None} |
| 二 | 期待どおり | 集計の器の二段の一致（一段目は無操作の値と効き目の値と札・裁定 D233・二段目は札・裁定 D234） 一段目 True（無操作の値と効き目の差の最大 1.49e-06・許容 0.001）・二段目 True（効き目の差の最大 4.92e-06・許容 0.0050・許容の内・記録） |
| 二 | 期待どおり | 二段目は札の一致で判定する（値だけが許容の外なら一致して印を残す・札が変われば一致しない・裁定 D234） 等方の帰無の端の一本を 0.0150 動かした（許容 0.0050）→ 一致 True・許容の外の印 True／二つ目の札の最上位を変えた → 一致 False |
| 二 | 期待どおり | 一段目は無操作の値も比べる（書き換えの道の無操作の値だけをずらすと一致しない・裁定 D233） ずらした量 0.0020（一段目の許容 0.001）→ 一段目の一致 False・差の最大 2.00e-03 |
| 二 | 期待どおり | 乙の行が B-lens の層二の答えの文字の位置の行と同じ（裁定 D227） 升目 9・行 64 |
| 二 | 期待どおり | 乙を流せる（文脈を組み・行の符号ごとに無操作と同じバッチ） 文脈 180（流したのは 2）・乙の行の順伝播 1280・符号のバッチ 260 |
| 二 | 期待どおり | 乙の順伝播の数が転記行 E と同じ（集計の器の数え方と、設計事実の器の転記行 C の門の行からの数え方） 集計の器 1280・260・180／転記行 E 1280・260・180 |
| 二 | 期待どおり | 乙のまとめに B-lens の直接の経路の値を並べる 行 13 |
| 二 | 期待どおり | 端から端まで・外した升目（主の升目 N1｜O-Ncold と門の行だけの升目 S4｜Osec-Ncold）: 本の計算と独立の再計算は外した升目の組と行を流さない 升目と符号 14（外す前 17）・独立の再計算の v̂ の行 7・下見の決定 一部の升目を外して続ける（外した升目 N1｜O-Ncold・S4｜Osec-Ncold） |
| 二 | 期待どおり | 端から端まで・外した升目（主の升目 N1｜O-Ncold と門の行だけの升目 S4｜Osec-Ncold）: 結果を開く段は、一致だけを見る段が読んだ出力と違う出力を開かない（裁定 D236） 結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）: ['main'] |
| 二 | 期待どおり | 端から端まで・外した升目（主の升目 N1｜O-Ncold と門の行だけの升目 S4｜Osec-Ncold）: 一致だけを見る段が二段とも一致 一段目 True・二段目 True・二段目の値 許容の内 |
| 二 | 期待どおり | 端から端まで・外した升目（主の升目 N1｜O-Ncold と門の行だけの升目 S4｜Osec-Ncold）: 札の行・Holm の段・門の行・偶然の目安を残った行で数え直す Holm の段 14・外した行 2・本の門の行 51（段階 B の門の行 64）・偶然の目安 向き 0.2701（外す前 0.3087） |
| 二 | 期待どおり | 端から端まで・外した升目（主の升目 N1｜O-Ncold と門の行だけの升目 S4｜Osec-Ncold）: 掃き出しに欠けが無く、報告が組めて走査の違反が無い 欠け 0・走査の違反 0・報告 289 行 |
| 二 | 期待どおり | 下見のバッチ一の枝（(vi) の決定だけをバッチ一にした写し）が機械の決定まで走る バッチ 1・揺れの床 0.00e+00・近道の許容 0.0050・(v) の近道 True（記述）・決定 続ける |
| 二 | 期待どおり | 端から端まで・バッチ一: 本の計算は方向ごとに一つのバッチで流し、二段目の二つの道は同じ計算になる（差が零・正本 `independent_recompute.stages.second.note`） バッチ 1・升目と符号 17・二段目の効き目の差の最大 0.00e+00 |
| 二 | 期待どおり | 端から端まで・バッチ一: 一致だけを見る段が二段とも一致 一段目 True・二段目 True・独立の再計算の v̂ の行 8 |
| 二 | 期待どおり | 端から端まで・バッチ一: 掃き出しに欠けが無く、報告が組めて走査の違反が無い 欠け 0・走査の違反 0・報告 294 行 |
| 三 | 期待どおり | 二重の正規化の読み取りを、出口の値の自己検査が止める 差の最大 2.408（許容 0.5） |
| 三 | 期待どおり | 壊した読み取りで下見が器の誤りとして止まる（やり直しの流れの一度目） 出口の値の自己検査が落ちた: {'cell': 'N1｜O-Ncold', 'max_abs': 2.407546997 |
| 三 | 期待どおり | 主位置まで使い回す近道を、凍結した確かめ（assert）が止める（下見の (v) の近道） 近道の元が主位置の手前で切れていない |
| 三 | 期待どおり | 記録した切れ目を偽った近道の元を、使い回す cache の列の実の長さの確かめが止める（裁定 D231） 使い回す cache の列の長さが主位置と違う（474・主位置 473）: N1｜O-Ncold |
| 三 | 期待どおり | （記述）主位置の一つ分の加減の寄与（効き目で比べる確かめの強さの目安） 主位置から -2.7306・主位置の次から -2.7306・差 5.39e-06（近道の許容 0.0050） |
| 三 | 期待どおり | （記述）本物の相対の加減の大きさの合成の方向での、書き換えの道の変種とフックの道の差（一段目の許容と比べる・判定に入れない） ‖v‖／‖選んだ層の出力‖ 0.0304・効き目の絶対値の最大 3.72e-01・M0 1.66e-06・M1 1.53e-02（許容の外）・M2 1.10e-01（許容の外）・M3 7.23e-01（許容の外）・M4 3.55e-01（許容の外）・M5 3.95e-02（許容の外）・M6 8.84e-02（許容の外）（許容 0.001） |
| 三 | 期待どおり | （記述）本物の相対の加減の大きさの合成の方向での、主位置の一つ分の加減の寄与（判定に入れない） 主位置から -1.412e-01・主位置の次から -1.493e-01・差 8.12e-03（近道の許容 0.0050・一段目の許容 0.001） |
| 三 | 期待どおり | （記述）本物の相対の加減の大きさの合成の方向での、二段目の本の道とフックの差・近道ありの本の道との比べ（判定に入れない・二段目の許容 0.0050・意見伺いの C2-3.2） N1｜O-Ncold｜-1: 近道なしの本の道とフックの差の最大 1.16e-05（許容の外 0／74）・近道ありの本の道とフックの差の最大 1.16e-05（許容の外 0／74）・無操作の近道ありとなしの差 0.00e+00・効き目の絶対値の最大 3.48e-01／N1｜Onull｜+1: 近道なしの本の道とフックの差の最大 1.25e-05（許容の外 0／74）・近道ありの本の道とフックの差の最大 3.79e-02（許容の外 41／74）・無操作の近道ありとなしの差 -3.77e-03・効き目の絶対値の最大 3.72e-01 |
| 四 | 期待どおり | 書き換えの器が個体の開発の記録の版のまま（中は変えない） 開発の記録 012CB2B68397614A・今 012CB2B68397614A |
| 四 | 期待どおり | 書き換えの器の --selftest が通る（今の本の器の上で） 終わりの値 0・34 秒・出力 52 行 |
| 四 | 期待どおり | 書き換えの器の --dry が通る（今の本の器の上で） 終わりの値 0・170 秒・出力 22 行 |
| 五 | 期待どおり | 起動器の三つの相（DRY・別のプロセス）: 相 check は順伝播を呼ばずに終わり、呼ばれた数と升目のトークンの並びの SHA16 を書く 終わりの値 0・順伝播を呼んだ数 0・守り 7・升目 9 |
| 五 | 期待どおり | 起動器の三つの相（DRY・別のプロセス）: 相 pilot と相 main が終わり、組ごとの出力の SHA-256 を session に書き、組ごとに zip を作る 終わりの値 0・0・組の出力の SHA-256 ['main', 'recompute', 'secondary']・zip ['part-main', 'part-recompute', 'part-secondary'] |
| 五 | 期待どおり | 起動器の三つの相（DRY・別のプロセス）: 集計の器の CLI の一致だけを見る段・結果を開く段・掃き出しの CLI・報告の組み立てと走査が通る 終わりの値 0・0・0・走査の違反 0・結果を開く段の記録に読んだ出力の同定 True |
| 五 | 期待どおり | 起動器の三つの相（DRY・別のプロセス）: 一致だけを見る段の後に組の出力の中身を変えると、結果を開く段が止まって書かない（裁定 D236） ["結果を開く段の出力が、一致だけを見る段の読んだ出力と違う（開かない）: ['main']"] |
| 四 | 期待どおり | 走らせた器と正本と設計事実と方向の記録が、走りの始めと終わりで同じ 35 ファイル |

## 印字の終わり（止まった所・手元の置き場の道筋は置き換えた）

```text
                                                     ^
  File "〈リポジトリ〉\tools\dry_run_Bl3.py", line 903, in <listcomp>
    '| %s | %s | %s | %s |' % (g, n, '期待どおり' if ok else '**期待と違う**', d.replace('|', '｜')) for g, n, ok, d in RESULTS] + [
                                                                     ^^^^^^^^^
AttributeError: 'list' object has no attribute 'replace'
exit 1
```

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/tools/trials/dry-trial-9-Bl3.md` >>>
