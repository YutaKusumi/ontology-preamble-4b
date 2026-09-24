（B-lens 層三の器についての意見伺いの束・分けた版 5／5・中身は一通版と同じ）

<<< 始: `tools/direction_B.py`（SHA16 E84A101655685F2B・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """direction_B.py v7 —— 段階 B の**方向の抽出**（主位置の活性・方向の作成・決定性の検査・要約統計・v̂ の凍結）。
  3 | v7（2026-09-20・凍結の前の方向の抽出の準備・独立の目を通っていない）: **本体を関数 `extract` に切り出した**——起動器（相 dir）と口（`__main__`）が同じものを呼ぶ。これまで口の本体は一度も走っておらず（端から端までの検査は部品の関数だけを呼んでいた）、起動器から実重みで呼ぶ前に小さな模型で通すため。決定性の二条の当て方を `check_determinism` に、**腕ごとのトークン長**（正本 `position_length.record_at_freeze`）を `token_lengths` に置き、自己検査で確かめる。口の使われていなかった引数（--arms-dir・--scenarios-dir——渡しても何も変わらなかった）を外した。
  4 | v6（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: 決定性 (ii) を**バッチの組成を変えた比較**にした——走行器と同じ組成（同じプロンプトを `runner.batch` 行）で取った主位置の活性と、一本流しの値を比べる（採否表 P396）。前は腕の並べ方を逆にした一本流しどうしを比べており、行列の形が変わらないので落ちようがなかった。主位置の活性を取る関数を本体の外（`main_position_activation`・`main_position_activation_batch`）に出し、端から端までの検査が同じ関数を呼べるようにした。
  5 | 
  6 | 正本 `design/contrasts-B.json` の `selection.position`・`selection.candidates`・`directions`・`activation_storage`・`runner` に従う。
  7 | 何をするか:
  8 |   (1) 腕 × 場面のプロンプトを組み、**プロンプトの最終トークン**（詰めでない最後の位置・`runner.padding`）の隠れ状態を、登録した層で取り出す。
  9 |   (2) 決定性の検査は二条（裁定 D91）: **同じ並べ方**で二度取って完全一致（外れたら走行を止める）／**バッチの組成を変えて**（走行器と同じ組成）一度取り、許容差の内側かを見る（外れたら記帳して登録者に上げる・採否表 P396）。
 10 |   (3) 方向を作る: (6a) 静的 h_O − h_Osec／(6b) 負荷下 h_{O-Ncold} − h_{Osec-Ncold}／Nk 方向 h_Nk − h_N／腕対の差方向 h_Onull − h_N。
 11 |       いずれも**抽出場面の平均**。td は v̂ のノルムに合わせる（`directions.td`）。
 12 |   (4) 要約統計: 層ごとのノルム・方向どうしのコサイン・**平均を取る前の場面ごとの差ベクトルどうしのコサイン**（抽出場面の間の安定性・採否表 P237）。
 13 |   (5) v̂ を凍結して保存し、SHA を記帳する（`selection.vector_fix`）。
 14 | 層番号は `selection.candidates.layer_index_rule`（割合 × 総層数を四捨五入して一つ引く・総層数は config から読んで記帳）。
 15 | **この器は GPU の上でしか本走行できない。** 手元では `--selftest`（合成のベクトルで規則だけを確かめる）が走る。
 16 | 用法: python tools/direction_B.py --model Qwen/Qwen3-4B-Instruct-2507 --out results/dirB [--dtype bfloat16]
 17 |       python tools/direction_B.py --selftest
 18 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 19 | """
 20 | import os, sys, json, math, hashlib, argparse, datetime
 21 | sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 22 | import numpy as np
 23 | import runs_B
 24 | 
 25 | VERSION = 'v7'
 26 | STRICT = os.environ.get('OP4B_REQUIRE_FULL_SELFTEST') == '1'     # 実機の段では飛ばしを失敗に倒す（裁定 D122・採否表 P344）
 27 | REPO = runs_B.REPO
 28 | T = runs_B.load_T()
 29 | PANEL = T['arms']['panel']
 30 | EX = T['extraction_scenarios']
 31 | LAYER_RATIOS = T['selection']['candidates']['layers']
 32 | DIRS = T['directions']
 33 | 
 34 | 
 35 | def layer_index(ratio, n_layers):
 36 |     """層の割合 → 層の添字（正本 `selection.candidates.layer_index_rule`・零始まり）。
 37 | 
 38 |     **四捨五入**（Python の `round` は偶数丸めなので使わない・実装検分の採否表 P283）。"""
 39 |     idx = int(math.floor(ratio * n_layers + 0.5)) - 1
 40 |     assert 0 <= idx < n_layers, ('層の添字が範囲の外', ratio, n_layers, idx)
 41 |     return idx
 42 | 
 43 | 
 44 | def hidden_states_index(layer_idx):
 45 |     """`hidden_states` の添字（埋め込みの分だけ一つずれる・正本の「層の添字」とは別物）。"""
 46 |     return layer_idx + 1
 47 | 
 48 | 
 49 | def decoder_layers(model):
 50 |     """hook を掛ける層の並びを、**一箇所で**決める（裁定 D117・2026-09-18）。
 51 | 
 52 |     抽出器（`hidden_states[idx+1]` を取る）と走行器（`layers[idx]` に hook を掛ける）が**同じ層を指す**ことが要る。
 53 |     `hidden_states[idx+1]` は「`layers[idx]` の出力」と等しい——この対応が崩れると、
 54 |     **抽出した層と介入した層が違う**まま誰も気づけない（系統内の検分の是認 A3 が「走行器が `layers[i]` に掛けることが条件」と断った箇所）。
 55 |     `assert_layer_alignment` で実機のたびに確かめる。
 56 |     """
 57 |     for path in (('model', 'layers'), ('transformer', 'h'), ('model', 'decoder', 'layers')):
 58 |         o = model
 59 |         for p in path:
 60 |             o = getattr(o, p, None)
 61 |             if o is None:
 62 |                 break
 63 |         if o is not None:
 64 |             return o
 65 |     raise SystemExit('この機種の層の並びを見つけられない（`decoder_layers` に経路を足す）')
 66 | 
 67 | 
 68 | def assert_layer_alignment(model, input_ids, attention_mask, layer_idx, atol=0.0):
 69 |     """**`hidden_states[idx+1]` が `layers[idx]` の出力と同じ**ことを、実機で確かめる（裁定 D117・D122）。
 70 | 
 71 |     恒真にならないよう、hook で実際に受け取ったテンソルと、`output_hidden_states` の該当位置を突き合わせる。
 72 |     """
 73 |     import torch
 74 |     got = {}
 75 | 
 76 |     def _h(module, inputs, output):
 77 |         got['h'] = (output[0] if isinstance(output, tuple) else output).detach().float().cpu()
 78 | 
 79 |     hd = decoder_layers(model)[layer_idx].register_forward_hook(_h)
 80 |     try:
 81 |         with torch.no_grad():
 82 |             out = model(input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=True)
 83 |     finally:
 84 |         hd.remove()
 85 |     hs = out.hidden_states[hidden_states_index(layer_idx)].detach().float().cpu()
 86 |     d = float((got['h'] - hs).abs().max())
 87 |     assert d <= atol, ('hidden_states[idx+1] と layers[idx] の出力が一致しない（層の対応が崩れている）', layer_idx, d)
 88 |     return d
 89 | 
 90 | 
 91 | def main_position_activation(model, ids, layer_idx, rows=1):
 92 |     """**主位置（プロンプトの最終トークン）**の活性（正本 `selection.position.main`）。同じプロンプトを rows 行並べたバッチで流し、零行目を返す。
 93 |     rows=1 は一本流し。バッチの入力は同一なので詰めは起きず、最終トークンは列の最後にある。
 94 |     `hidden_states[idx+1]` を取る——`layers[idx]` の出力と同じであることは `assert_layer_alignment` で確かめる。"""
 95 |     import torch
 96 |     t = torch.tensor([list(ids)] * int(rows), device=model.device)
 97 |     am = torch.ones_like(t)
 98 |     with torch.no_grad():
 99 |         out = model(input_ids=t, attention_mask=am, output_hidden_states=True)
100 |     return out.hidden_states[hidden_states_index(layer_idx)][0, -1, :].detach().float().cpu().numpy()
101 | 
102 | 
103 | def main_position_activation_batch(model, ids, layer_idx, rows=None):
104 |     """**走行器と同じバッチの組成**（同じプロンプトを `runner.batch` 行・正本 `selection.batch_composition`）で取った主位置の活性。
105 |     決定性 (ii) は、これと一本流しの値を比べる（採否表 P396）。"""
106 |     batch_rows = int(rows or T['runner']['batch'])
107 |     return main_position_activation(model, ids, layer_idx, batch_rows)
108 | 
109 | 
110 | def h_norm_record(H, dirs):
111 |     """**‖v̂‖ と主位置の ‖h‖ の比を層ごとに**（正本 `activation_storage.h_norm_record`・裁定 D127・採否表 P356・2026-09-19）。
112 | 
113 |     ‖h‖ は抽出場面の前置きの腕の主位置の活性のノルムの平均。係数の格子は ‖v̂‖ に対する比なので、
114 |     ‖v̂‖ が ‖h‖ に比べて小さいと九候補すべてが「何も起きない」域に入りうる——**調整走行の前に登録者に見せる**。"""
115 |     out = {}
116 |     for r in LAYER_RATIOS:
117 |         hn = float(np.mean([np.linalg.norm(H[(arm, sc, r)]) for arm in PANEL for sc in EX if (arm, sc, r) in H]))
118 |         vn = float(np.linalg.norm(dirs[('static', r)]))
119 |         out[str(r)] = {'h_norm_main': hn, 'vhat_norm': vn, 'vhat_over_h': (vn / hn) if hn else None}
120 |     return out
121 | 
122 | 
123 | def write_layer_record(out_dir, n_layers, h_norm=None):
124 |     """総層数と層の添字を**記帳**する（正本 `layer_index_rule` が求める・採否表 P283）。‖v̂‖ と ‖h‖ の比も書く（採否表 P356）。"""
125 |     rec = {'num_hidden_layers': n_layers, 'ratios': LAYER_RATIOS,
126 |            'layer_indices': {str(r): layer_index(r, n_layers) for r in LAYER_RATIOS},
127 |            'hidden_states_indices': {str(r): hidden_states_index(layer_index(r, n_layers)) for r in LAYER_RATIOS},
128 |            'h_norm': h_norm}
129 |     os.makedirs(out_dir, exist_ok=True)
130 |     json.dump(rec, open(os.path.join(out_dir, 'layers.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
131 |     return rec
132 | 
133 | 
134 | def unit(v):
135 |     n = float(np.linalg.norm(v))
136 |     return v / n if n else v
137 | 
138 | 
139 | def match_norm(v, ref):
140 |     """v の向きのまま、ノルムを ref のノルムに合わせる（裁定 D75 の基準は v̂）。"""
141 |     nv, nr = float(np.linalg.norm(v)), float(np.linalg.norm(ref))
142 |     return v * (nr / nv) if nv else v
143 | 
144 | 
145 | def cosine(a, b):
146 |     na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
147 |     return float(np.dot(a, b) / (na * nb)) if na and nb else None
148 | 
149 | 
150 | def build_directions(H):
151 |     """H[(arm, scenario, layer_ratio)] = 活性ベクトル → 方向と要約統計。
152 | 
153 |     方向は抽出場面の平均。td は v̂ のノルムに合わせる。安定性は「平均を取る前の場面ごとの差ベクトルどうしのコサイン」。"""
154 |     out, stats = {}, {}
155 |     pairs = {'static': ('O', 'Osec'), 'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}
156 |     for ratio in LAYER_RATIOS:
157 |         per = {}
158 |         for name, (a1, a2) in pairs.items():
159 |             diffs = {sc: H[(a1, sc, ratio)] - H[(a2, sc, ratio)] for sc in EX}
160 |             per[name] = {'mean': np.mean([diffs[sc] for sc in EX], axis=0), 'by_scenario': diffs}
161 |         v_hat = per['static']['mean']
162 |         raw_ratio = {}
163 |         for name in pairs:
164 |             v = per[name]['mean']
165 |             raw_ratio[name] = (float(np.linalg.norm(v)) / float(np.linalg.norm(v_hat))) if np.linalg.norm(v_hat) else None
166 |             if name != 'static':
167 |                 v = match_norm(v, v_hat)      # **全方向を ‖v̂〔static〕‖ に合わせる**（裁定 D102・採否表 P309・P311）
168 |             out[(name, ratio)] = v
169 |         stats[ratio] = {
170 |             'norms': {name: float(np.linalg.norm(out[(name, ratio)])) for name in pairs},
171 |             'raw_norm_ratio': raw_ratio,          # **合わせる前の比**（正本 coefficient_ref・採否表 P284 の後半）
172 |             'cosines': {'%s~%s' % (x, y): cosine(out[(x, ratio)], out[(y, ratio)])
173 |                         for i, x in enumerate(sorted(pairs)) for y in sorted(pairs)[i + 1:]},
174 |             'stability': {name: {'cos_%s_%s' % (EX[0], EX[1]): cosine(per[name]['by_scenario'][EX[0]], per[name]['by_scenario'][EX[1]]),
175 |                                  'norm_ratio': (float(np.linalg.norm(per[name]['by_scenario'][EX[0]])) /
176 |                                                 float(np.linalg.norm(per[name]['by_scenario'][EX[1]])) if np.linalg.norm(per[name]['by_scenario'][EX[1]]) else None)}
177 |                           for name in pairs}}
178 |     return out, stats
179 | 
180 | 
181 | def determinism_same_order(h1, h2):
182 |     """**同じ並べ方**で二度取った活性の完全一致（bitwise）を見る（裁定 D91 の (i)）。一致しなければ走行を止める。"""
183 |     if set(h1) != set(h2):
184 |         return False, ['鍵の集合が違う: %s' % sorted(set(h1) ^ set(h2))[:4]]
185 |     bad = []
186 |     for k in h1:
187 |         a, b = np.asarray(h1[k]), np.asarray(h2[k])
188 |         if np.isnan(a).any() or np.isnan(b).any():
189 |             bad.append('%s: NaN を含む' % (k,))
190 |         elif not np.array_equal(a, b):
191 |             bad.append('%s: 一致しない' % (k,))
192 |     return (not bad), bad
193 | 
194 | 
195 | def determinism_cross_order(h1, h2, tol=None):
196 |     """**バッチの組成を変えて**取った活性が許容差の内側かを見る（裁定 D91 の (ii)・採否表 P396）。外れたら記帳して登録者に上げる（止めない）。
197 |     名の `cross_order` は前の名残（前は並べ方を変えた一本流しどうしを比べていた）。"""
198 |     tol = tol or T['activation_storage']['determinism']['cross_order_tolerance']
199 |     rows = []
200 |     if set(h1) != set(h2):      # **鍵の欠けを黙って無視しない**（裁定 D114・採否表 P325）
201 |         rows.append({'key': '（鍵の集合）', 'ok': False,
202 |                      'note': '鍵の集合が違う: %s' % sorted(set(h1) ^ set(h2), key=str)[:4]})
203 |     for k in sorted(set(h1) & set(h2), key=str):
204 |         a, b = np.asarray(h1[k], dtype=float), np.asarray(h2[k], dtype=float)
205 |         na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
206 |         cos = float(np.dot(a, b) / (na * nb)) if na and nb else None
207 |         rel = float(np.max(np.abs(a - b)) / na) if na else None
208 |         ok = (cos is not None and cos >= tol['cos_min']) and (rel is not None and rel <= tol['max_abs_over_norm'])
209 |         rows.append({'key': str(k), 'cos': cos, 'max_abs_over_norm': rel, 'ok': ok})
210 |     return all(r['ok'] for r in rows), rows
211 | 
212 | 
213 | def _selftest():
214 |     rng = np.random.default_rng(7)
215 |     d = 16
216 |     # 層番号は**手で書いた期待値の表**と突き合わせる（実装式で確かめない・採否表 P283）
217 |     want = {(0.25, 36): 8, (0.5, 36): 17, (0.75, 36): 26, (0.25, 34): 8, (0.5, 34): 16, (0.75, 34): 25,
218 |             (0.25, 42): 10, (0.5, 42): 20, (0.75, 42): 31}
219 |     for (ratio, n), idx in want.items():
220 |         assert layer_index(ratio, n) == idx, ('層番号が期待値と違う', ratio, n, layer_index(ratio, n), idx)
221 |     assert hidden_states_index(layer_index(0.5, 36)) == 18, 'hidden_states の添字の変換が違う'
222 |     H = {}
223 |     for arm in PANEL:
224 |         for sc in EX:
225 |             for ratio in LAYER_RATIOS:
226 |                 H[(arm, sc, ratio)] = rng.normal(size=d)
227 |     dirs, stats = build_directions(H)
228 |     # **`build_directions` の出力そのものを読んで、全方向 × 全層を照合する**（裁定 D122・D102）。
229 |     # 前は td 一本だけを見ていたので、td だけ合わせる誤りに戻しても検査が通った（系統外の検分で捕まった）。
230 |     n_norm = 0
231 |     for ratio in LAYER_RATIOS:
232 |         nv = float(np.linalg.norm(dirs[('static', ratio)]))
233 |         for name in ('Nk', 'td', 'loaded'):
234 |             nw = float(np.linalg.norm(dirs[(name, ratio)]))
235 |             assert abs(nw - nv) < 1e-9, ('方向のノルムが ‖v̂〕に合っていない（裁定 D102）', name, ratio, nw, nv)
236 |             n_norm += 1
237 |     assert n_norm == 3 * len(LAYER_RATIOS), 'ノルムの照合の回数が足りない'
238 |     assert 'raw_norm_ratio' in stats[LAYER_RATIOS[0]], '合わせる前の比が記帳されていない（採否表 P284）'
239 |     assert set(stats[LAYER_RATIOS[0]]['stability']) == {'static', 'loaded', 'Nk', 'td'}
240 |     # 決定性 (i) 同じ並べ方 → 完全一致
241 |     ok, bad = determinism_same_order(H, dict(H))
242 |     assert ok and not bad
243 |     H2 = dict(H)
244 |     k0 = next(iter(H2))
245 |     H2[k0] = H2[k0] + 1e-9
246 |     ok2, bad2 = determinism_same_order(H, H2)
247 |     assert not ok2 and len(bad2) == 1, '決定性の検査が差を見落とす'
248 |     H3 = dict(H)
249 |     H3.pop(k0)
250 |     ok3, bad3 = determinism_same_order(H, H3)
251 |     assert not ok3 and '鍵の集合' in bad3[0], '鍵の欠けを見落とす'
252 |     H4 = dict(H)
253 |     H4[k0] = H4[k0] * np.nan
254 |     ok4, bad4 = determinism_same_order(H, H4)
255 |     assert not ok4 and 'NaN' in bad4[0], 'NaN を別の名で報告していない'
256 |     # 決定性 (ii) バッチの組成を変えた → 許容差（採否表 P396）
257 |     tol = T['activation_storage']['determinism']['cross_order_tolerance']
258 |     Hs = {k: vv + rng.normal(size=d) * 1e-6 for k, vv in H.items()}
259 |     ok5, rows5 = determinism_cross_order(H, Hs)
260 |     assert ok5, ('わずかな差が許容差を外れた', rows5[:1])
261 |     Hb = {k: vv + rng.normal(size=d) * 1.0 for k, vv in H.items()}
262 |     ok6, rows6 = determinism_cross_order(H, Hb)
263 |     assert not ok6, '大きな差を許容差の内側と判定した'
264 |     # 決定性の二条の当て方（v7）: (i) の不一致は止まり、(ii) の外れは止まらずに記帳する
265 |     try:
266 |         check_determinism(H, H2, H)
267 |         raise AssertionError('決定性 (i) の不一致で止まらなかった')
268 |     except SystemExit:
269 |         pass
270 |     ok_s, ok_c, rows_c = check_determinism(H, dict(H), Hb)
271 |     assert ok_s and not ok_c and rows_c, '決定性 (ii) の外れを記帳していない（止まった・または外れを見落とした）'
272 |     # 腕ごとのトークン長（v7）: 前置きの本文だけの数（N は零）と、場面ごとの組み立て済みの列の長さ（手で数えた期待値と照らす）
273 |     class _Tok:
274 |         def __call__(self, t, add_special_tokens=False):
275 |             return {'input_ids': t.split()}
276 |     _AT = {'O': 'a b c', 'N': '', 'Osec': 'a b c d'}
277 |     _SC = ['N1', 'S1', 'SK', 'S4']
278 |     _pid = lambda arm, sc: list(range(len(_AT[arm].split()) + 10 + _SC.index(sc)))
279 |     tl = token_lengths(_Tok(), _AT, _SC, _pid)
280 |     assert tl['N']['preamble_tokens'] == 0 and tl['O']['preamble_tokens'] == 3 and tl['Osec']['preamble_tokens'] == 4, ('前置きのトークン数が違う', tl)
281 |     assert set(tl) == set(_AT) and all(set(v['prompt_tokens']) == set(_SC) for v in tl.values()), ('腕か場面が欠けた', tl)
282 |     assert tl['Osec']['prompt_tokens']['S4'] == 17 and tl['N']['prompt_tokens']['N1'] == 10, ('組み立て済みの列の長さが違う', tl)
283 |     # ‖v̂‖ と ‖h‖ の比（採否表 P356）——器を通さずに一層だけ数え直して照らす
284 |     hr = h_norm_record(H, dirs)
285 |     r0 = LAYER_RATIOS[0]
286 |     hn0 = sum(float(np.sqrt((H[(a_, s_, r0)] ** 2).sum())) for a_ in PANEL for s_ in EX) / (len(PANEL) * len(EX))
287 |     assert abs(hr[str(r0)]['h_norm_main'] - hn0) < 1e-9, ('‖h‖ の記帳が数え直しと違う', hr[str(r0)], hn0)
288 |     assert abs(hr[str(r0)]['vhat_over_h'] - float(np.linalg.norm(dirs[('static', r0)])) / hn0) < 1e-9
289 |     if STRICT:
290 |         try:
291 |             import torch  # noqa: F401  実機の段では torch が要る（層の対応の検査・裁定 D122）
292 |         except ImportError:
293 |             raise SystemExit('torch が無い——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
294 |     print('[direction_B selftest] 層番号（期待値の表・%d 通り）・hidden_states の添字・ノルム合わせ・安定性・‖v̂‖ と ‖h‖ の比・'
295 |           '決定性の二条（同じ並べ方は完全一致／バッチの組成を変えたら cos %g・相対差 %g）・二条の当て方（(i) は止め (ii) は記帳）・腕ごとのトークン長: すべて通った'
296 |           % (len(want), tol['cos_min'], tol['max_abs_over_norm']))
297 | 
298 | 
299 | def check_determinism(H1, H2, H3):
300 |     """**決定性の二条**（裁定 D91・正本 `activation_storage.determinism`）を当てる。
301 | 
302 |     (i) 同じ並べ方で二度取った値（H1・H2）が完全一致でなければ**止める**（SystemExit・登録者に上げる）。
303 |     (ii) バッチの組成を変えた値（H3）は許容差を見て**記帳するだけ**（止めない）。戻り値: (ok_same, ok_cross, rows_cross)。"""
304 |     ok_same, bad_same = determinism_same_order(H1, H2)
305 |     if not ok_same:
306 |         raise SystemExit('決定性 (i)（同じ並べ方で完全一致）に落ちた——走行を止め、登録者に上げる（裁定 D91）: %s' % bad_same[:4])
307 |     ok_cross, rows_cross = determinism_cross_order(H1, H3)
308 |     return ok_same, ok_cross, rows_cross
309 | 
310 | 
311 | def token_lengths(tok, arm_text, scenarios, prompt_ids_fn):
312 |     """**腕ごとのトークン長**（正本 `position_length.record_at_freeze`・裁定 D82）。
313 | 
314 |     前置きの本文だけのトークン数（特別なトークンを付けない・N は零）と、場面ごとの組み立て済みの列の長さ（主位置は列の最後）を返す。
315 |     arm_text: 腕 → 前置きの本文、scenarios: 場面の並び、prompt_ids_fn(arm, sc): 組み立て済みのトークン列。"""
316 |     out = {}
317 |     for arm in sorted(arm_text):
318 |         t = arm_text[arm] or ''
319 |         pre = len(tok(t, add_special_tokens=False)['input_ids']) if t else 0
320 |         out[arm] = {'preamble_tokens': int(pre), 'prompt_tokens': {sc: int(len(prompt_ids_fn(arm, sc))) for sc in scenarios}}
321 |     return out
322 | 
323 | 
324 | def extract(model, tok, out_dir, model_label=None, dtype_label=None, log=print):
325 |     """**方向の抽出の本体**（凍結の前・活性だけ・生成しない）。起動器（`tools/colab/boot_stageB.py` の相 dir）と、この器の口（`__main__`）が同じものを呼ぶ。
326 | 
327 |     (1) 層の対応を実機で確かめる → (2) 活性を三度取る（同じ並べ方で二度・走行器と同じバッチの組成で一度）→ 決定性の二条 →
328 |     (3) 方向を作る（全方向を ‖v̂‖ に合わせる）→ (4) npz と記録を書く（方向・主位置の活性・層・‖v̂‖／‖h‖・腕ごとのトークン長）。
329 |     戻り値: 記録（`directions.json` と同じ中身）。決定性 (i) に落ちたら SystemExit。"""
330 |     import torch
331 |     import steer_B
332 |     import run_stageB_local as RUN
333 |     os.makedirs(out_dir, exist_ok=True)
334 |     n_layers = model.config.num_hidden_layers
335 |     idxs = {r: layer_index(r, n_layers) for r in LAYER_RATIOS}
336 |     AT = {k: v['text'] for k, v in RUN.arm_texts().items()}          # 腕の素材は SHA16 で引き当てる
337 |     PANEL_ARMS = list(T['arms']['panel'])
338 |     EXTRACT = list(T['extraction_scenarios'])
339 | 
340 |     def prompt_ids(arm, sc):
341 |         """一つの (腕, 場面) の**組み立て済みのトークン列**（正本 `runner.prompt_assembly`・`runner.chat_template`）。"""
342 |         scen, inst = RUN.scenario_and_instruction(sc)
343 |         msg = RUN.user_message(AT[arm], scen['text'], inst)
344 |         return steer_B.apply_chat(tok, msg)
345 | 
346 |     def collect(order, rows=1):
347 |         """腕 × 場面 × 層の主位置の活性を集める。order は腕の並べ方、rows はバッチの行数（1 は一本流し・決定性の検査に使う）。"""
348 |         H = {}
349 |         for arm in order:
350 |             for sc in EXTRACT:
351 |                 ids = prompt_ids(arm, sc)
352 |                 for r in LAYER_RATIOS:
353 |                     H[(arm, sc, r)] = (main_position_activation(model, ids, idxs[r]) if rows == 1
354 |                                        else main_position_activation_batch(model, ids, idxs[r], rows))
355 |         return H
356 | 
357 |     # (1) 層の対応を実機で確かめる（抽出した層と介入する層が同じであること）
358 |     _ids = prompt_ids(PANEL_ARMS[0], EXTRACT[0])
359 |     _t = torch.tensor([_ids], device=model.device)
360 |     align = {str(r): assert_layer_alignment(model, _t, torch.ones_like(_t), idxs[r]) for r in LAYER_RATIOS}
361 |     log('[direction_B] 層の対応を確かめた（hidden_states[idx+1] と layers[idx] の最大差 %s）' % align)
362 | 
363 |     # (2) 活性を三度取る（決定性の二条・裁定 D91）
364 |     H1 = collect(PANEL_ARMS)
365 |     H2 = collect(PANEL_ARMS)                       # 同じ並べ方
366 |     H3 = collect(PANEL_ARMS, rows=T['runner']['batch'])   # **バッチの組成を変えた**（走行器と同じ組成・採否表 P396）
367 |     ok_same, ok_cross, rows_cross = check_determinism(H1, H2, H3)
368 |     log('[direction_B] 決定性 (i) 完全一致・(ii) バッチの組成（%d 行）を変えた値が許容差の内側 %s' % (T['runner']['batch'], ok_cross))
369 | 
370 |     # (3) 方向を作る（全方向を ‖v̂〕に合わせる・裁定 D102）
371 |     dirs, stats = build_directions(H1)
372 |     nv = {r: float(np.linalg.norm(dirs[('static', r)])) for r in LAYER_RATIOS}
373 |     for (name, r), v in dirs.items():
374 |         if name != 'static':
375 |             d = abs(float(np.linalg.norm(v)) - nv[r])
376 |             assert d < 1e-6 * max(nv[r], 1.0), ('方向のノルムが ‖v̂〕に合っていない（裁定 D102）', name, r, d)
377 | 
378 |     # (4) 書き出す（npz・要約統計・層の記帳・トークン長）
379 |     npz = os.path.join(out_dir, 'directions.npz')
380 |     np.savez(npz, **{'%s__%s' % (name, r): v for (name, r), v in dirs.items()})
381 |     sha = hashlib.sha256(open(npz, 'rb').read()).hexdigest().upper()
382 |     # **主位置の活性そのものを保存する**（正本 activation_storage.prompt_final・determinism.material・2026-09-19）
383 |     act = os.path.join(out_dir, 'main_position_activations.npz')
384 |     np.savez(act, **{'same_order__%s__%s__%s' % (arm, sc, r): v for (arm, sc, r), v in H1.items()},
385 |              **{'batch_rows__%s__%s__%s' % (arm, sc, r): v for (arm, sc, r), v in H3.items()})
386 |     act_sha = hashlib.sha256(open(act, 'rb').read()).hexdigest().upper()
387 |     hrec = h_norm_record(H1, dirs)                     # 採否表 P356・調整走行の前に登録者に見せる（見せるだけ・裁定 D141）
388 |     write_layer_record(out_dir, n_layers, hrec)
389 |     tl = token_lengths(tok, {a_: AT[a_] for a_ in PANEL_ARMS}, list(T['scenarios']), prompt_ids)
390 |     log('[direction_B] ‖v̂‖／‖h‖（主位置・層ごと）: %s——**調整走行の前に登録者に見せる・見せるだけで格子は変えない**（正本 activation_storage.h_norm_record・裁定 D141）'
391 |         % {r_: (None if v_['vhat_over_h'] is None else round(v_['vhat_over_h'], 6)) for r_, v_ in hrec.items()})
392 |     rec = {'kind': 'direction_B', 'version': VERSION, 'model': model_label, 'dtype': dtype_label, 'h_norm': hrec,
393 |            'num_hidden_layers': n_layers, 'layer_indices': {str(r): idxs[r] for r in LAYER_RATIOS},
394 |            'alignment_max_abs': align, 'determinism_same_order': bool(ok_same),
395 |            'determinism_cross_order': {'ok': bool(ok_cross), 'rows': rows_cross, 'compared': '一本流し 対 走行器と同じバッチの組成（%d 行）' % T['runner']['batch']},
396 |            'stats': {str(r): stats[r] for r in LAYER_RATIOS}, 'npz_sha256': sha, 'activations_npz_sha256': act_sha,
397 |            'arm_token_lengths': tl, 'arms': PANEL_ARMS, 'extraction_scenarios': EXTRACT,
398 |            'contrasts_sha16': runs_B.sha16_file(runs_B.CPATH)}
399 |     json.dump(rec, open(os.path.join(out_dir, 'directions.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
400 |     log('[direction_B] 方向を書いた: %s（SHA-256 %s…）' % (npz, sha[:16]))
401 |     log('[direction_B] 総層数 %d・層の添字 %s・合わせる前の比 %s'
402 |         % (n_layers, idxs, {str(r): stats[r].get('raw_norm_ratio') for r in LAYER_RATIOS}))
403 |     return rec
404 | 
405 | 
406 | if __name__ == '__main__':
407 |     ap = argparse.ArgumentParser()
408 |     ap.add_argument('--selftest', action='store_true')
409 |     ap.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
410 |     ap.add_argument('--dtype', default='bfloat16')
411 |     ap.add_argument('--out', default=None)
412 |     a = ap.parse_args()
413 |     if a.selftest:
414 |         _selftest()
415 |         sys.exit(0)
416 |     try:
417 |         import torch
418 |         from transformers import AutoModelForCausalLM, AutoTokenizer
419 |     except Exception as e:                                    # 手元では届かない（Colab の段で走らせる）
420 |         sys.exit('torch／transformers が無い: %s（この器は GPU の上で走らせる。手元の検査は --selftest）' % e)
421 |     out_dir = a.out or os.path.join(REPO, 'results', 'dirB')
422 |     # 置き場を直に渡せるようにする（版を固定し、Hub への問い合わせを避ける・裁定 D115・採否表 P335〔二体目 G8〕）
423 |     tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or a.model)
424 |     tok.padding_side = 'left'                                  # 正本 runner.padding
425 |     model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=getattr(torch, a.dtype), device_map='auto')
426 |     model.eval()
427 |     rec = extract(model, tok, out_dir, model_label=a.model, dtype_label=a.dtype)
428 |     sys.exit(0 if rec['determinism_cross_order']['ok'] else 2)      # (ii) は止めない条だが、外れたら非零で知らせる（裁定 D91）
```
<<< 終: `tools/direction_B.py` >>>

<<< 始: `tools/blens_core.py`（SHA16 DB3092B1EF0B88B3・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """blens_core.py v1 —— B-lens の計算の芯（numpy だけ・重みも試行も読まない・2026-09-23）。
  3 | 
  4 | 正本 `design/contrasts-Blens.json` の規則を、重みや試行を読まない純粋な関数に置く。層一の器 `tools/blens_lens.py`・
  5 | 層二の器 `tools/blens_calib.py`・合成データの器 `tools/dry_run_Blens.py` が同じ関数を呼ぶ（同じ式を二度書かない）。
  6 | 語の集合の規則（字の決まり・断片・中身の語）は、ここに置かない（語の集合の器 `tools/blens_sets.py` が、下書きの器 `tools/blens_facts.py` と
  7 | 独立に書き、バイトで突き合わせる——正本 `token_sets.freeze`）。
  8 | 
  9 | 置くもの:
 10 |   - 物差しの係数のベクトル: 物差しは方向 u について線形なので、M(u) = a·u の a を一度だけ作る（a = g ⊙ (Σ w_t W[t] − (Σ w_t) μ_W)・μ_W は含める語彙の行の平均）。
 11 |     差の形の物差しは Σ w_t = 0 で中心化が消え、片側の物差しは語彙の平均を引く（正本 `projection.centring_note`）。
 12 |   - 等方の帰無の方向の引き方（`steer_B.random_directions` と同じ作り方・自己検査でビットの一致を確かめる）と、解析の標準偏差（‖a‖·‖v̂‖／√d）。
 13 |   - 割合: 零を中心に対称な帰無の両側の割合（`percentile.rule`）と、語の側の帰無の両側に等しい裾の割合（`nulls.word_side.p_rule`）。
 14 |   - Holm: 段階 B の集計器と同じく、p が段を**下回る**（p < 段）ときに通し、通らなかった所で止める（正本「p が段を下回る」）。
 15 |   - 門: 行の単位の順位相関（Spearman・同順位は平均順位）と、方向を単位にした並べ替え（全ての入れ替え・片側・p = #{ρ_入れ替え ≥ ρ_観測}／入れ替えの数・恒等を含む）。
 16 |   - 語の側の帰無: 層の組み立て（字の種類 × 字数 × ノルムの帯・薄い層は帯の真ん中の側の隣と合わせる・真ん中なら下の側）と、抽選。
 17 |   - 大きさの目盛り: B の標本化の変換（温度 → top_k → top_p・transformers 4.57 の順と式）・二項分布の中央の区間・正確な直接の経路とその分け方。
 18 | 用法: python tools/blens_core.py --selftest
 19 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 20 | """
 21 | import sys, math, itertools, collections
 22 | import numpy as np
 23 | 
 24 | VERSION = 'v1'
 25 | EPS_TIE = 1e-12          # 並べ替えの順位相関の同値の幅（恒等と同じ値の入れ替えを「以上」に数える・保守の側）
 26 | 
 27 | 
 28 | # ---------------- 物差しの係数 ----------------
 29 | def metric_table(sets, families, letters):
 30 |     """物差しの名 → (トークン, 重み, 片側か)。sets は凍結の語の集合（`blens_sets` の出力の `sets`）。
 31 | 
 32 |     名: M_L_<家族>・M_Lc（survival だけ）・M_R_<家族>・M_X_<家族>・M_E_<方向の種類>・M_F・M_F_sens と、感度の変種（名の後ろに :<変種>）。"""
 33 |     L, R = sets['L'], sets['R']
 34 |     out = collections.OrderedDict()
 35 |     mean_w = lambda toks, sgn=1.0: [(t, sgn / len(toks)) for t in toks]
 36 | 
 37 |     def put(name, pos, neg, one_sided=False):
 38 |         acc = collections.OrderedDict()
 39 |         for t, w in pos + neg:
 40 |             acc[t] = acc.get(t, 0.0) + w
 41 |         out[name] = (list(acc.keys()), list(acc.values()), one_sided)
 42 | 
 43 |     for fam in families:
 44 |         lt = letters[fam]
 45 |         others = [L[x] for x in lt if x != 'a']
 46 |         put('M_L_%s' % fam, [(L['a'], 1.0)], mean_w(others, -1.0))
 47 |         put('M_R_%s' % fam, [(R, 1.0)], mean_w([L[x] for x in lt], -1.0))
 48 |         X = sets['X'][fam]
 49 |         for var, (a_, o_) in (('', (X['a'], X['others'])), (':unmarked', (X['a_unmarked'], X['others_unmarked'])),
 50 |                               (':kata1', (X['a_kata1'], X['others_kata1'])), (':all', (X['a_all'], X['others_all'])),
 51 |                               (':multi', (X['a_multi'], X['others_multi']))):
 52 |             if a_ and o_:
 53 |                 put('M_X_%s%s' % (fam, var), mean_w(a_), mean_w(o_, -1.0))
 54 |     if 'survival' in families:
 55 |         put('M_Lc', [(L['c'], 1.0)], mean_w([L['a'], L['b']], -1.0))
 56 |     for kind in ('static', 'td', 'Nk'):
 57 |         E = sets['E'][kind]
 58 |         for var, (p_, m_) in (('', (E['plus'], E['minus'])), (':kata1', (E['plus_kata1'], E['minus_kata1'])),
 59 |                               (':all', (E['plus_all'], E['minus_all'])), (':multi', (E['plus_multi'], E['minus_multi']))):
 60 |             if not p_:
 61 |                 continue
 62 |             if m_:
 63 |                 put('M_E_%s%s' % (kind, var), mean_w(p_), mean_w(m_, -1.0))
 64 |             else:
 65 |                 put('M_E_%s%s' % (kind, var), mean_w(p_), [], one_sided=True)
 66 |     F = sets['F']
 67 |     put('M_F', [(F['main'], 1.0)], [], one_sided=True)
 68 |     if F['sens']:
 69 |         put('M_F_sens', [(F['main'], 1.0)], mean_w(F['sens'], -1.0))
 70 |     return out
 71 | 
 72 | 
 73 | def coef_vectors(table, rows_of, mu_W, g):
 74 |     """物差しの係数のベクトル a（d 次元・float32）。rows_of(トークンの並び) は語彙の行（float32・行×d）を返す関数。"""
 75 |     need = sorted(set(t for toks, w, o in table.values() for t in toks))
 76 |     Wn = dict(zip(need, rows_of(need)))
 77 |     out = collections.OrderedDict()
 78 |     for name, (toks, w, one) in table.items():
 79 |         s = np.zeros_like(mu_W)
 80 |         for t, wt in zip(toks, w):
 81 |             s = s + np.float32(wt) * Wn[t]
 82 |         s = s - np.float32(sum(w)) * mu_W
 83 |         out[name] = (g * s).astype(np.float32)
 84 |     return out
 85 | 
 86 | 
 87 | def values(A, U):
 88 |     """物差しの値: A は物差しの名 → a、U は方向（本数×d）。戻り値: 名 → 値の並び（float64）。"""
 89 |     U = np.atleast_2d(np.asarray(U, dtype=np.float32))
 90 |     return collections.OrderedDict((k, (U @ a).astype(np.float64)) for k, a in A.items())
 91 | 
 92 | 
 93 | def analytic_sd(a, target_norm, d):
 94 |     """ノルム target_norm の等方の方向での a·u の標準偏差（‖a‖·‖v̂‖／√d）。"""
 95 |     return float(np.linalg.norm(a.astype(np.float64)) * target_norm / math.sqrt(d))
 96 | 
 97 | 
 98 | # ---------------- 方向 ----------------
 99 | def iso_directions(v_hat_static, seed, layer_ratio, count, key_scale):
100 |     """`steer_B.random_directions` と同じ作り方（種と本数だけを変える・凍結の関数は種を正本から取るので写した）。"""
101 |     d = int(np.asarray(v_hat_static).shape[-1])
102 |     ss = np.random.SeedSequence([seed, int(round(layer_ratio * key_scale))])
103 |     rng = np.random.default_rng(ss)
104 |     target = float(np.linalg.norm(v_hat_static))
105 |     out = []
106 |     for i in range(count):
107 |         g = rng.normal(size=d)
108 |         n = float(np.linalg.norm(g))
109 |         out.append(g * (target / n) if n else g)
110 |     return np.array(out)
111 | 
112 | 
113 | def match_norm(v, target):
114 |     n = float(np.linalg.norm(v))
115 |     return v * (float(target) / n) if n else v
116 | 
117 | 
118 | def real_differences(arm_means, target_norm):
119 |     """八腕の平均の活性の全ての対（名の並びの順・i<j）: 名 'A~B' → (A − B) を target_norm に合わせたもの。"""
120 |     names = list(arm_means)
121 |     out = collections.OrderedDict()
122 |     for i, j in itertools.combinations(range(len(names)), 2):
123 |         out['%s~%s' % (names[i], names[j])] = match_norm(arm_means[names[i]] - arm_means[names[j]], target_norm)
124 |     return out
125 | 
126 | 
127 | # ---------------- 割合と札 ----------------
128 | def p_two_sided(m, null):
129 |     null = np.asarray(null, dtype=np.float64)
130 |     return float((1 + np.sum(np.abs(null) >= abs(m))) / (1 + len(null)))
131 | 
132 | 
133 | def p_equal_tailed(m, null):
134 |     null = np.asarray(null, dtype=np.float64)
135 |     K = len(null)
136 |     return float(min(1.0, 2 * min((1 + np.sum(null >= m)) / (1 + K), (1 + np.sum(null <= m)) / (1 + K))))
137 | 
138 | 
139 | def holm(pvals, alpha, m=None):
140 |     """名 → p を受け、名 → {'p','step','pass'}。p < 段（下回る）で通し、通らなかった所で止める（段階 B の集計器と同じ）。"""
141 |     m = m or len(pvals)
142 |     order = sorted(pvals, key=lambda k: (pvals[k], k))
143 |     out, still = {}, True
144 |     for i, k in enumerate(order):
145 |         step = alpha / (m - i)
146 |         ok = still and pvals[k] < step
147 |         out[k] = {'p': pvals[k], 'step': step, 'pass': ok}
148 |         still = ok
149 |     return out
150 | 
151 | 
152 | def top_rank(m, comps):
153 |     """実在の差の札: |m| が比べる相手の |値| のすべてを上回れば最上位（同じ値は上回らない）。順位は 1 ＋ #{|c| ≥ |m|}。"""
154 |     c = np.abs(np.asarray(comps, dtype=np.float64))
155 |     return {'top': bool(np.all(abs(m) > c)), 'rank': int(1 + np.sum(c >= abs(m))), 'of': int(len(c) + 1)}
156 | 
157 | 
158 | # ---------------- 順位相関と門 ----------------
159 | def avg_ranks(x):
160 |     x = np.asarray(x, dtype=np.float64)
161 |     order = np.argsort(x, kind='mergesort')
162 |     r = np.empty(len(x), dtype=np.float64)
163 |     xs = x[order]
164 |     i = 0
165 |     while i < len(x):
166 |         j = i
167 |         while j + 1 < len(x) and xs[j + 1] == xs[i]:
168 |             j += 1
169 |         r[order[i:j + 1]] = (i + j) / 2.0 + 1.0
170 |         i = j + 1
171 |     return r
172 | 
173 | 
174 | def spearman(x, y):
175 |     rx, ry = avg_ranks(x), avg_ranks(y)
176 |     rx, ry = rx - rx.mean(), ry - ry.mean()
177 |     den = math.sqrt(float(rx @ rx) * float(ry @ ry))
178 |     return float(rx @ ry / den) if den > 0 else float('nan')
179 | 
180 | 
181 | def gate_perm(rows, unit_vals, units):
182 |     """方向を単位にした並べ替えの門（片側・全ての入れ替え）。
183 | 
184 |     rows: [{'unit','sign','fam','y'}]・unit_vals: 単位 → {家族: 物差しの値}・units: 入れ替える単位の並び（rows の単位はこの中）。
185 |     戻り値: {'rho','p','n_perm','n_rows'}。ρ が定まらない（順位が一定）ときは p を 1 にする。"""
186 |     rows = [r for r in rows if r['unit'] in units]
187 |     y = np.array([r['y'] for r in rows], dtype=np.float64)
188 |     idx = {u: i for i, u in enumerate(units)}
189 |     ui = np.array([idx[r['unit']] for r in rows])
190 |     sg = np.array([r['sign'] for r in rows], dtype=np.float64)
191 |     fams = sorted(set(r['fam'] for r in rows))
192 |     fi = np.array([fams.index(r['fam']) for r in rows])
193 |     V = np.array([[unit_vals[u][f] for f in fams] for u in units], dtype=np.float64)
194 |     ry = avg_ranks(y)
195 |     ry = ry - ry.mean()
196 | 
197 |     def rho_of(perm):
198 |         x = sg * V[np.asarray(perm)[ui], fi]
199 |         rx = avg_ranks(x)
200 |         rx = rx - rx.mean()
201 |         den = math.sqrt(float(rx @ rx) * float(ry @ ry))
202 |         return float(rx @ ry / den) if den > 0 else float('nan')
203 | 
204 |     obs = rho_of(list(range(len(units))))
205 |     if math.isnan(obs):
206 |         return {'rho': obs, 'p': 1.0, 'n_perm': math.factorial(len(units)), 'n_rows': len(rows)}
207 |     ge = n = 0
208 |     for perm in itertools.permutations(range(len(units))):
209 |         r_ = rho_of(perm)
210 |         n += 1
211 |         if not math.isnan(r_) and r_ >= obs - EPS_TIE:
212 |             ge += 1
213 |     return {'rho': obs, 'p': ge / n, 'n_perm': n, 'n_rows': len(rows)}
214 | 
215 | 
216 | def logit_cc(k, n, c):
217 |     return math.log((k + c) / (n - k + c))
218 | 
219 | 
220 | # ---------------- 語の側の帰無 ----------------
221 | def strata_groups(cand_cells, need_cells, n_bands, merge_factor):
222 |     """層の組み立て。cand_cells・need_cells: (字の種類, 字数, 帯) → 数。戻り値: (字の種類, 字数) → [(帯の組, 候補の数, 要る数)]・組めたか。
223 | 
224 |     要る数のある (字の種類, 字数) ごとに、帯を一つずつの組から始め、候補の数が要る数の merge_factor 倍に満たない組
225 |     （要る数のある組のうち帯の小さい順の最初）を、帯の真ん中の側の隣の組と合わせる（組の帯の平均が真ん中なら下の側）。足りるまで繰り返す。"""
226 |     mid = (n_bands - 1) // 2
227 |     out, ok = collections.OrderedDict(), True
228 |     for tl in sorted(set((t, l) for t, l, b in need_cells)):
229 |         gs = [[b] for b in range(n_bands)]
230 |         while True:
231 |             need = lambda g_: sum(need_cells.get(tl + (b,), 0) for b in g_)
232 |             cand = lambda g_: sum(cand_cells.get(tl + (b,), 0) for b in g_)
233 |             short = [g_ for g_ in gs if need(g_) and cand(g_) < merge_factor * need(g_)]
234 |             if not short or len(gs) == 1:
235 |                 ok = ok and not short
236 |                 break
237 |             k = gs.index(short[0])
238 |             centre = sum(short[0]) / len(short[0])
239 |             to = k + 1 if centre < mid else (k - 1 if centre > mid else (k - 1 if k > 0 else k + 1))
240 |             lo, hi = sorted((k, to))
241 |             gs = gs[:lo] + [gs[lo] + gs[hi]] + gs[hi + 1:]
242 |         out[tl] = [(tuple(g_), sum(cand_cells.get(tl + (b,), 0) for b in g_), sum(need_cells.get(tl + (b,), 0) for b in g_)) for g_ in gs]
243 |     return out, ok
244 | 
245 | 
246 | def word_side_draws(delta, plus, minus, cell_of, candidates, groups, draws, seed):
247 |     """語の側の帰無の抽選（v̂ を固定し、E+ と E− と同じ層の組み立てで、候補から重ならずに引く）。
248 | 
249 |     delta: 語彙の Δℓ（添字で引ける）・cell_of: トークン → (字の種類, 字数, 帯)・groups: `strata_groups` の出力。
250 |     各抽選で、層（(字の種類, 字数) の昇順・その中の帯の組の順）ごとに、候補（トークンの番号の昇順）から E+ と E− の要る数の和だけを重ならずに引き、
251 |     先の要る数を E+ に、残りを E− に当てる（乱数は `np.random.default_rng(seed)`）。戻り値: M_E の帰無の値（draws 本）。"""
252 |     rng = np.random.default_rng(seed)
253 |     plan = []
254 |     for tl, gl in groups.items():
255 |         for g_, nc, nn in gl:
256 |             npl = sum(1 for t in plus if cell_of(t)[:2] == tl and cell_of(t)[2] in g_)
257 |             nmi = sum(1 for t in minus if cell_of(t)[:2] == tl and cell_of(t)[2] in g_)
258 |             if npl + nmi == 0:
259 |                 continue
260 |             cs = np.array(sorted(t for t in candidates if cell_of(t)[:2] == tl and cell_of(t)[2] in g_), dtype=np.int64)
261 |             assert len(cs) >= npl + nmi, ('層の候補が要る数に足りない', tl, g_)
262 |             plan.append((cs, npl, nmi))
263 |     dv = np.asarray(delta, dtype=np.float64)
264 |     out = np.empty(draws, dtype=np.float64)
265 |     for k in range(draws):
266 |         ps, ms = [], []
267 |         for cs, npl, nmi in plan:
268 |             pick = cs[rng.choice(len(cs), size=npl + nmi, replace=False)]
269 |             ps.append(pick[:npl])
270 |             ms.append(pick[npl:])
271 |         pp = np.concatenate(ps) if ps else np.array([], dtype=np.int64)
272 |         mm = np.concatenate(ms) if ms else np.array([], dtype=np.int64)
273 |         out[k] = dv[pp].mean() - (dv[mm].mean() if len(mm) else 0.0)
274 |     return out
275 | 
276 | 
277 | # ---------------- 大きさの目盛り ----------------
278 | def transform(logits, temperature, top_k, top_p):
279 |     """B の標本化の変換（transformers 4.57 の順と式: 温度で割る → top_k（k 番目以上を残す）→ top_p（昇順の累積が 1 − top_p 以下を落とす・最後の一つは残す））。
280 |     戻り値: 変換の後の確率（float64・足して一）。"""
281 |     z = np.asarray(logits, dtype=np.float64) / float(temperature)
282 |     k = min(int(top_k), z.size)
283 |     kth = np.partition(z, -k)[-k]
284 |     z = np.where(z < kth, -np.inf, z)
285 |     order = np.argsort(z, kind='mergesort')
286 |     zs = z[order]
287 |     fin = np.isfinite(zs)
288 |     ps = np.zeros_like(zs)
289 |     ps[fin] = np.exp(zs[fin] - zs[fin].max())
290 |     ps = ps / ps.sum()
291 |     cum = np.cumsum(ps)
292 |     remove = cum <= (1.0 - float(top_p))
293 |     remove[-1] = False
294 |     keep = np.ones(z.size, dtype=bool)
295 |     keep[order[remove]] = False
296 |     z = np.where(keep, z, -np.inf)
297 |     p = np.zeros_like(z)
298 |     f = np.isfinite(z)
299 |     p[f] = np.exp(z[f] - z[f].max())
300 |     return p / p.sum()
301 | 
302 | 
303 | def binom_central(n, p, ci):
304 |     """二項分布 Bin(n, p) の中央の区間 [lo, hi]（下の裾と上の裾がそれぞれ (1 − ci)／2 を超えない最も狭い整数の区間）。"""
305 |     a = (1.0 - float(ci)) / 2.0
306 |     k = np.arange(n + 1)
307 |     if p <= 0:
308 |         return 0, 0
309 |     if p >= 1:
310 |         return n, n
311 |     logpmf = np.array([math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * math.log(p) + (n - i) * math.log1p(-p) for i in k])
312 |     pmf = np.exp(logpmf - logpmf.max())
313 |     pmf = pmf / pmf.sum()
314 |     cdf = np.cumsum(pmf)
315 |     sf = np.cumsum(pmf[::-1])[::-1]
316 |     lo = int(k[np.argmax(cdf > a)])                  # P(X < lo) ≤ a
317 |     hi = int(k[len(k) - 1 - np.argmax(sf[::-1] > a)])   # P(X > hi) ≤ a
318 |     return lo, hi
319 | 
320 | 
321 | def z_two_sample(k0, n0, k1, n1, c):
322 |     """観測の変化の二標本の z（率に連続性の補正を入れた標準誤差・転記行 E と同じ式）。"""
323 |     q0, q1 = (k0 + c) / (n0 + 2 * c), (k1 + c) / (n1 + 2 * c)
324 |     se = math.sqrt(q0 * (1 - q0) / n0 + q1 * (1 - q1) / n1)
325 |     d = k1 / n1 - k0 / n0
326 |     return d, d / se
327 | 
328 | 
329 | def rms(h, eps):
330 |     h = np.asarray(h, dtype=np.float64)
331 |     return math.sqrt(float(np.mean(h * h)) + eps)
332 | 
333 | 
334 | def direct_path(Zh, Zu, h, u, alpha, eps):
335 |     """正確な直接の経路と、その分け方（出口の値の変化・全語彙）。
336 | 
337 |     Zh = W_E·(g⊙h)・Zu = W_E·(g⊙u)（どちらも正規化の前の量）。α u は加えた量（係数 × ‖v̂‖ の比・腕の符号つき）。
338 |     戻り値: {'before','after','exact','layer1','along','scale'}（出口の値・float64）。
339 |       layer1 = (α／rms(h))·Zu・along = −α (h·u)／(d·rms(h)³)·Zh（一次の展開の ĥ に沿う部分）・scale = exact − layer1 − along。"""
340 |     h = np.asarray(h, dtype=np.float64)
341 |     u = np.asarray(u, dtype=np.float64)
342 |     d = h.size
343 |     r0 = rms(h, eps)
344 |     r1 = rms(h + alpha * u, eps)
345 |     Zh = np.asarray(Zh, dtype=np.float64)
346 |     Zu = np.asarray(Zu, dtype=np.float64)
347 |     before = Zh / r0
348 |     after = (Zh + alpha * Zu) / r1
349 |     exact = after - before
350 |     layer1 = (alpha / r0) * Zu
351 |     along = -alpha * float(h @ u) / (d * r0 ** 3) * Zh
352 |     return {'before': before, 'after': after, 'exact': exact, 'layer1': layer1, 'along': along, 'scale': exact - layer1 - along}
353 | 
354 | 
355 | # ---------------- 自己検査 ----------------
356 | def _selftest():
357 |     rng = np.random.default_rng(0)
358 |     # 割合と Holm
359 |     assert p_two_sided(3.0, [1, -4, 2, 3]) == (1 + 2) / 5
360 |     assert p_equal_tailed(0.0, [1, 2, 3, 4]) == min(1.0, 2 * min(5 / 5, 1 / 5))
361 |     h = holm({'a': 0.001, 'b': 0.03, 'c': 0.2}, 0.05)
362 |     assert h['a']['pass'] and not h['b']['pass'] and not h['c']['pass']          # 0.03 は 0.025 を下回らない
363 |     h2 = holm({'a': 0.025, 'b': 0.001}, 0.05)
364 |     assert h2['b']['pass'] and h2['a']['pass'] is True                            # 二段目は 0.05 を下回る
365 |     h3 = holm({'a': 0.025, 'b': 0.04}, 0.05)
366 |     assert not h3['a']['pass'] and not h3['b']['pass']                            # 一段目がちょうど 0.025 は下回らない（p < 段）
367 |     assert top_rank(5.0, [1, -5, 2])['top'] is False and top_rank(5.1, [1, -5, 2])['top'] is True
368 |     # 順位相関（scipy と突き合わせる・手元にあるとき）
369 |     x, y = rng.normal(size=30), rng.normal(size=30)
370 |     x[3] = x[4]
371 |     try:
372 |         from scipy.stats import spearmanr
373 |         assert abs(spearman(x, y) - spearmanr(x, y)[0]) < 1e-12
374 |     except ImportError:
375 |         pass
376 |     # 門: 一つの単位の値だけ大きい → 並べ替えで p は小さくならない（単位は 4 本・24 通り）
377 |     rows = [{'unit': u, 'sign': 1, 'fam': 'f', 'y': float(i)} for i, u in enumerate(['A', 'A', 'B', 'C', 'D', 'D'])]
378 |     uv = {'A': {'f': 0.0}, 'B': {'f': 1.0}, 'C': {'f': 2.0}, 'D': {'f': 3.0}}
379 |     g_ = gate_perm(rows, uv, ['A', 'B', 'C', 'D'])
380 |     assert g_['n_perm'] == 24 and abs(g_['p'] - 1 / 24) < 1e-12 and g_['rho'] > 0.9
381 |     g0 = gate_perm(rows, {k: {'f': 1.0} for k in uv}, ['A', 'B', 'C', 'D'])
382 |     assert g0['p'] == 1.0
383 |     # 層の組み立て: 薄い層は真ん中の側と合わせる・真ん中は下の側
384 |     cand = {('K', '1', 0): 50, ('K', '1', 1): 50, ('K', '1', 2): 2, ('K', '1', 3): 50, ('K', '1', 4): 3}
385 |     need = {('K', '1', 2): 1, ('K', '1', 4): 1}
386 |     gr, ok = strata_groups(cand, need, 5, 5)
387 |     assert ok and [g[0] for g in gr[('K', '1')]] == [(0,), (1, 2), (3, 4)], gr
388 |     # 標本化の変換を transformers の warper と突き合わせる（手元にあるとき）
389 |     try:
390 |         import torch
391 |         from transformers.generation.logits_process import TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper
392 |         for _ in range(20):
393 |             lg = rng.normal(size=500).astype(np.float32) * 3
394 |             t = torch.tensor(lg[None, :])
395 |             for w in (TemperatureLogitsWarper(0.7), TopKLogitsWarper(top_k=20), TopPLogitsWarper(top_p=0.9)):
396 |                 t = w(None, t)
397 |             ref = torch.softmax(t, dim=-1)[0].double().numpy()
398 |             got = transform(lg, 0.7, 20, 0.9)
399 |             assert np.array_equal(ref > 0, got > 0) and np.max(np.abs(ref - got)) < 1e-6, np.max(np.abs(ref - got))
400 |     except ImportError:
401 |         pass
402 |     # 二項分布の区間
403 |     lo, hi = binom_central(200, 0.77, 0.999)
404 |     assert lo < 154 < hi and binom_central(154, 1.0, 0.999) == (154, 154) and binom_central(50, 0.0, 0.999) == (0, 0)
405 |     # 直接の経路: 小さな α で一次の展開に近づく
406 |     d = 64
407 |     W = rng.normal(size=(40, d))
408 |     gg = rng.uniform(0.5, 1.5, size=d)
409 |     hv = rng.normal(size=d) * 5
410 |     uv_ = rng.normal(size=d)
411 |     Zh, Zu = W @ (gg * hv), W @ (gg * uv_)
412 |     small = direct_path(Zh, Zu, hv, uv_, 1e-4, 1e-6)
413 |     assert np.max(np.abs(small['scale'])) < 1e-6 * max(1.0, np.max(np.abs(small['exact'])))
414 |     big = direct_path(Zh, Zu, hv, uv_, 2.0, 1e-6)
415 |     assert np.allclose(big['exact'], big['layer1'] + big['along'] + big['scale'])
416 |     # 等方の方向: 種と層の割合で決まり、ノルムがそろう
417 |     v = rng.normal(size=d).astype(np.float32)
418 |     D1 = iso_directions(v, 81001, 0.5, 5, 1000)
419 |     D2 = iso_directions(v, 81001, 0.5, 5, 1000)
420 |     assert np.array_equal(D1, D2) and np.allclose(np.linalg.norm(D1, axis=1), float(np.linalg.norm(v)))
421 |     print('[blens_core] 自己検査 OK（%s）' % VERSION)
422 | 
423 | 
424 | if __name__ == '__main__':
425 |     if '--selftest' in sys.argv:
426 |         _selftest()
427 |     else:
428 |         print(__doc__)
```
<<< 終: `tools/blens_core.py` >>>

<<< 始: `tools/colab/boot_Blens.py`（SHA16 E1B7270F3A2385AC・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """boot_Blens.py v2 —— B-lens の Colab 起動スクリプト（層二の大きさの目盛りの教師強制の順伝播・2026-09-23・正本 `magnitude`・§9）。
  3 | 
  4 | 相（OP4B_PHASE）:
  5 |   check   凍結の前の確かめ（**射影を一つも計算しない・残差のベクトルを置かない**）: 版（正本 `inputs.versions_B`）・GPU・重みの断片の SHA-256（転記行 F）・
  6 |           段階 B のランダム方向を B の版の NumPy で再生した方向そのもの（`random_dirs.npz`）と SHA-256・各層の最初の一件の教師強制で、主位置（凍結の `steer_B.main_position`）・
  7 |           答えの文字の位置（加減の帯の中）・前置きの SHA（`preamble_sha`）・logits の突き合わせ（`magnitude.logit_check`）・較正の検査（`magnitude.calibration_check`）。
  8 |   extract 封印の後: 凍結の記録と封印の記録がそろったコミットで、選んだ試行の全件（`design-facts-Blens.json` の `E.selected`・起動器は選び直さない）の、
  9 |           正規化の前の最終の残差を、主位置と答えの文字の位置で取り（`model.norm` の入力への前の hook）、最初の一件の全語彙の logits を置く。
 10 |           **方向はここでは掛けない**（直接の経路は手元の器 `tools/blens_calib.py` が計算する）。check の確かめもすべてもう一度行う。
 11 | 止める条件（外れたら止める・登録者に相談・裁定 D184）: 版の不一致（入れ直した後にランタイムの再起動を求める）・GPU・重みの SHA-256・選んだ試行の SHA16・
 12 |   前置きの SHA・主位置・答えの文字の位置・選択の値を読めない出力・logits の突き合わせ・較正の検査。
 13 | v2（2026-09-24・裁定 D187）: 再生したランダム方向そのものを出力に置く（手元の器が方向ごとの相対の差の許容で突き合わせる・ビットの一致は求めない）。
 14 |   版は三つとも文字列の完全な一致で確かめる（torch は CUDA の組み `+cu…` まで）。torch が違えば、B の組みの torch を PyTorch の置き場から入れ直し、
 15 |   入っている torchvision・torchaudio も同じ組みに揃える（版の番号は入っているものの `+` の前・組みの違う拡張が import で止まるのを避ける）。
 16 | 運用: コーディネータが登録者の Chrome 越しに Colab を操作する（ランタイムの選択と結果の zip のダウンロードもコーディネータ）。登録者の手に残すのは同意と支払い。
 17 |   資格情報は入力しない（HF_TOKEN のポップアップはキャンセル・公開の重み）。Drive は使わない（出力は小さく、終わりに zip を落とす）。
 18 | セルに打つ一行（先頭の下線は type の事故の緩衝・<commit> は 40 桁）:
 19 |   ______________________________=0;import os;os.environ['OP4B_COMMIT']='<commit>';os.environ['OP4B_PHASE']='check';import urllib.request as u;exec(u.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<commit>/tools/colab/boot_Blens.py').read())
 20 | DRY（手元の検査・OP4B_DRY=1）: 登録機種の設定を小さくした乱数の模型（実重みではない）と実トークナイザで、同じ経路を CPU で通す。OP4B_REPO_DIR・OP4B_OUT が要る。
 21 |   版・GPU・重みの SHA は見ない。較正の検査は計算して印字するが、止めない（乱数の模型なので合わない）。OP4B_DRY_N で一層の件数を減らす（extract）。
 22 | 関数 `context_of`・`calibration_items` は合成データの器 `tools/dry_run_Blens.py` が import して経路を確かめる（import のときは走らない）。
 23 | 柵: 本スクリプトの出力は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 24 | """
 25 | import os, sys, re, json, time, glob, shutil, hashlib, datetime, subprocess, zipfile
 26 | 
 27 | VERSION = 'v2'
 28 | T0 = time.time()
 29 | REPO_URL = 'https://github.com/YutaKusumi/ontology-preamble-4b.git'
 30 | LOG = []
 31 | CH = re.compile(r'"choice"\s*:\s*"(a|b|c|d|refuse)"')
 32 | now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
 33 | 
 34 | 
 35 | class Stop(Exception):
 36 |     pass
 37 | 
 38 | 
 39 | def mark(step, **kw):
 40 |     LOG.append(dict(step=step, t=round(time.time() - T0, 1), at=now(), **kw))
 41 |     print('[boot_Blens] %-14s %6.0fs %s' % (step, time.time() - T0, kw or ''), flush=True)
 42 | 
 43 | 
 44 | def sh(cmd, check=True):
 45 |     r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
 46 |     if check and r.returncode != 0:
 47 |         print(r.stdout[-2000:]); print(r.stderr[-3000:])
 48 |         raise RuntimeError('失敗: %s' % cmd)
 49 |     return r
 50 | 
 51 | 
 52 | def stop(msg):
 53 |     mark('stop', reason=msg)
 54 |     sys.exit('[boot_Blens] 止める（登録者に相談）: ' + msg)
 55 | 
 56 | 
 57 | def context_of(tok, prompt, trial, raw, arm_sha16, main_position):
 58 |     """一件の教師強制の入力（組み立て済みのプロンプト＋出力の答えの文字の前まで）と位置。外れれば Stop。"""
 59 |     tid = trial['trial_id']
 60 |     if trial['preamble_sha'] != arm_sha16:
 61 |         raise Stop('前置きの SHA が試行の記録と違う: %s' % tid)
 62 |     mp = main_position(prompt)
 63 |     if mp != len(prompt) - 1:
 64 |         raise Stop('主位置が凍結の steer_B.main_position と違う: %s' % tid)
 65 |     enc = tok(raw['final'], add_special_tokens=False, return_offsets_mapping=True)
 66 |     ms = list(CH.finditer(raw['final']))
 67 |     if not ms or ms[-1].group(1) != trial['choice']:
 68 |         raise Stop('選択の値を読めない: %s' % tid)
 69 |     pos = ms[-1].start(1)
 70 |     cover = [q for q, (s0, s1) in enumerate(enc['offset_mapping']) if s0 <= pos < s1]
 71 |     if not cover or cover[0] < 1:
 72 |         raise Stop('選択の値の文字を覆うトークンが無い: %s' % tid)
 73 |     c0 = cover[0]
 74 |     lp = len(prompt) + c0 - 1
 75 |     if not (mp <= lp < len(prompt) + len(enc['input_ids'])):
 76 |         raise Stop('答えの文字の位置が加減の帯の中に無い: %s' % tid)
 77 |     return {'trial_id': tid, 'trial_index': trial['trial_index'], 'choice': trial['choice'], 'n_prompt': len(prompt), 'main_pos': mp, 'cover': c0,
 78 |             'letter_pos': lp, 'letter_token': int(enc['input_ids'][c0]), 'ids': list(prompt) + list(enc['input_ids'][:c0])}
 79 | 
 80 | 
 81 | def calibration_items(keys, ctx_rec, observed, ci, binom_central):
 82 |     """較正の検査（正本 magnitude.calibration_check）: 層ごとの最初の文脈の、変換の後の確率と、無操作の観測の件数。"""
 83 |     calib, off = {}, []
 84 |     for key in keys:
 85 |         rec = [c for c in ctx_rec if c['stratum'] == key][0]
 86 |         ob = observed[key]
 87 |         lo, hi = binom_central(ob['n'], rec['pT_main_fmain'], ci)
 88 |         item = {'main': {'p_T': rec['pT_main_fmain'], 'n': ob['n'], 'k': ob['style'], 'interval': [lo, hi], 'inside': lo <= ob['style'] <= hi}}
 89 |         if not item['main']['inside']:
 90 |             off.append('%s 主位置' % key)
 91 |         if key.endswith('|json'):
 92 |             item['letter'] = {}
 93 |             for x in ('a', 'b', 'c'):
 94 |                 lo2, hi2 = binom_central(ob['json_n'], rec['pT_letter'][x], ci)
 95 |                 k2 = ob['json_letters'][x]
 96 |                 item['letter'][x] = {'p_T': rec['pT_letter'][x], 'n': ob['json_n'], 'k': k2, 'interval': [lo2, hi2], 'inside': lo2 <= k2 <= hi2}
 97 |                 if not item['letter'][x]['inside']:
 98 |                     off.append('%s 答えの文字 %s' % (key, x))
 99 |         calib[key] = item
100 |     return calib, off
101 | 
102 | 
103 | def run():
104 |     PHASE = os.environ.get('OP4B_PHASE', 'check')
105 |     COMMIT = os.environ.get('OP4B_COMMIT', '')
106 |     DRY = os.environ.get('OP4B_DRY') == '1'
107 |     if PHASE not in ('check', 'extract'):
108 |         sys.exit('[boot_Blens] 相は check か extract')
109 |     if not DRY and not re.fullmatch(r'[0-9a-f]{40}', COMMIT):
110 |         sys.exit('[boot_Blens] OP4B_COMMIT に固定のコミット（40 桁の SHA）を与える')
111 |     print('[boot_Blens] %s 開始 phase=%s %s' % (VERSION, PHASE, 'DRY' if DRY else COMMIT), flush=True)
112 |     # ---- 1. リポジトリ（コミット固定）と正本
113 |     if DRY:
114 |         REPO = os.path.abspath(os.environ['OP4B_REPO_DIR'])
115 |         OUTROOT = os.path.abspath(os.environ['OP4B_OUT'])
116 |     else:
117 |         REPO, OUTROOT = '/content/ontology-preamble-4b', '/content/op4b-Blens'
118 |         head_ok = os.path.isdir(os.path.join(REPO, '.git')) and sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() == COMMIT
119 |         if not head_ok:
120 |             shutil.rmtree(REPO, ignore_errors=True)
121 |             sh(['git', 'clone', '--filter=blob:none', '--no-checkout', REPO_URL, REPO])
122 |             sh(['git', '-C', REPO, 'sparse-checkout', 'set', '--cone', 'tools', 'arms', 'design', 'records', 'results/dirB', 'results/stageB'])
123 |             sh(['git', '-C', REPO, 'checkout', '-q', COMMIT])
124 |         if sh(['git', '-C', REPO, 'rev-parse', 'HEAD'], check=False).stdout.strip() != COMMIT:
125 |             stop('取り出したコミットが OP4B_COMMIT と違う')
126 |     os.makedirs(OUTROOT, exist_ok=True)
127 |     TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
128 |     FJ = json.load(open(os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
129 |     if PHASE == 'extract' and not DRY:
130 |         for need in ('FREEZE-RECORD-Blens.json', 'sealing-record-Blens.json'):
131 |             if not os.path.exists(os.path.join(REPO, 'records', 'Blens', need)):
132 |                 stop('相 extract は凍結と封印の後に走らせる（%s が無い・正本 predictions.order）' % need)
133 |     mark('repo', commit=COMMIT[:12] or 'dry', canon=TL['version'])
134 | 
135 |     # ---- 2. 版（正本 inputs.versions_B）と GPU
136 |     import importlib.metadata as md
137 | 
138 |     def ver(k):
139 |         try:
140 |             return md.version(k)
141 |         except Exception:
142 |             return None
143 |     PIN = TL['inputs']['versions_B']
144 |     VER = {k: ver(k) for k in ('numpy', 'torch', 'transformers', 'torchvision', 'torchaudio', 'tokenizers', 'huggingface_hub', 'accelerate', 'safetensors')}
145 |     want = {'numpy': PIN['numpy'], 'torch': PIN['torch'], 'transformers': PIN['transformers']}
146 |     bad = {k: VER[k] for k, v in want.items() if VER[k] != v}          # 文字列の完全な一致（torch は CUDA の組みまで・裁定 D187）
147 |     if bad and not DRY:
148 |         mark('pin', installing=bad)
149 |         os.environ['HF_HUB_DISABLE_XET'] = '1'
150 |         if 'torch' in bad:
151 |             cuda = PIN['torch'].split('+')[1]
152 |             pk = ['torch==%s' % PIN['torch']] + ['%s==%s+%s' % (c, VER[c].split('+')[0], cuda) for c in ('torchvision', 'torchaudio') if VER.get(c)]
153 |             sh([sys.executable, '-m', 'pip', 'install', '-q'] + pk + ['--index-url', 'https://download.pytorch.org/whl/%s' % cuda])
154 |         sh([sys.executable, '-m', 'pip', 'install', '-q', 'numpy==%s' % want['numpy'], 'transformers==%s' % want['transformers'], 'accelerate', 'huggingface_hub', 'safetensors'])
155 |         print('[boot_Blens] 版を入れ直した。**ランタイムを再起動して（「ランタイム」→「セッションを再起動」）、同じ一行をもう一度走らせる**', flush=True)
156 |         sys.exit(0)
157 |     GPU = 'dry'
158 |     if not DRY:
159 |         GPU = sh('nvidia-smi --query-gpu=name --format=csv,noheader', check=False).stdout.strip().split('\n')[0]
160 |         if 'L4' not in GPU and 'A100' not in GPU:
161 |             stop('GPU %s は登録の環境（Colab L4・A100 は予備）に無い' % GPU)
162 |     mark('versions', versions=VER, gpu=GPU)
163 | 
164 |     import numpy as np
165 |     import torch
166 |     sys.path.insert(0, os.path.join(REPO, 'tools'))
167 |     import steer_B
168 |     import run_stageB_local as RB
169 |     import blens_core as C
170 |     import blens_lens as BL
171 |     from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
172 | 
173 |     # ---- 3. 重み（転記行 F の SHA-256 と突き合わせる）
174 |     M = TL['inputs']['model']
175 |     W_SHA = {}
176 |     if DRY:
177 |         SNAPDIR = os.environ.get('OP4B_TOKENIZER_DIR') or os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % M['rev'])
178 |     else:
179 |         os.environ['HF_HUB_DISABLE_XET'] = '1'
180 |         from huggingface_hub import snapshot_download
181 |         SNAPDIR = snapshot_download(M['repo'], revision=M['rev'])
182 |         for fn in FJ['facts']['F']['sha256']:
183 |             h = hashlib.sha256()
184 |             with open(os.path.join(SNAPDIR, fn), 'rb') as fh:
185 |                 for blk in iter(lambda: fh.read(1 << 24), b''):
186 |                     h.update(blk)
187 |             W_SHA[fn] = h.hexdigest().upper()
188 |         badw = [fn for fn, sha in FJ['facts']['F']['sha256'].items() if W_SHA[fn] != sha]
189 |         if badw:
190 |             stop('重みの SHA-256 が転記行 F と違う: %s' % badw)
191 |     mark('weights', snapshot=os.path.basename(SNAPDIR), checked=len(W_SHA))
192 | 
193 |     # ---- 4. 段階 B のランダム方向（B の版の NumPy で再生した方向そのものと SHA-256・層一の器が手元の再生と許容の内で突き合わせる・裁定 D187）
194 |     D = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
195 |     rk = BL.rkey
196 |     ratios = [rk(r) for r in TL['layers']['ratios']]
197 |     sel = rk(TL['primary']['ratio'])
198 |     RDIR = {'main@%s' % sel: np.array(steer_B.random_directions(D['static__%s' % sel], 'main', float(sel)))}
199 |     for r in ratios:
200 |         RDIR['tune@%s' % r] = np.array(steer_B.random_directions(D['static__%s' % r], 'tune', float(r)))
201 |     RSHA = {k: BL.dirs_sha256(v) for k, v in RDIR.items()}
202 |     mark('random', numpy=np.__version__, sha=RSHA)
203 | 
204 |     # ---- 5. 模型とトークナイザ
205 |     tok = AutoTokenizer.from_pretrained(SNAPDIR)
206 |     if DRY:
207 |         cfg = AutoConfig.from_pretrained(SNAPDIR)
208 |         cfg.hidden_size, cfg.num_hidden_layers, cfg.num_attention_heads, cfg.num_key_value_heads, cfg.head_dim, cfg.intermediate_size = 64, 2, 4, 2, 16, 128
209 |         torch.manual_seed(0)
210 |         model = AutoModelForCausalLM.from_config(cfg).float().eval()
211 |         dev = 'cpu'
212 |     else:
213 |         model = AutoModelForCausalLM.from_pretrained(SNAPDIR, torch_dtype=torch.bfloat16, device_map='cuda').eval()
214 |         dev = 'cuda'
215 |     cap = {}
216 |     hook = model.model.norm.register_forward_pre_hook(lambda mod, args: cap.__setitem__('h', args[0].detach()))
217 |     EPS = float(model.config.rms_norm_eps)
218 |     mark('model', dry=DRY, layers=model.config.num_hidden_layers, eps=EPS)
219 | 
220 |     # ---- 6. 選んだ試行（起動器は選び直さない）
221 |     E = FJ['facts']['E']
222 |     sel_ids = E['selected']
223 |     if hashlib.sha256(json.dumps(sel_ids, sort_keys=True).encode('utf-8')).hexdigest().upper()[:16] != E['selected_sha16']:
224 |         stop('選んだ試行の一覧の SHA16 が設計の事実と違う')
225 |     AT = RB.arm_texts()
226 |     SAMP = TL['inputs']['sampling_B']
227 |     F_MAIN = int(FJ['facts']['B']['F']['main'])
228 |     L_IDS = {k: int(v) for k, v in FJ['facts']['B']['L'].items()}
229 | 
230 |     def cell_trials(sc, arm):
231 |         d = os.path.join(REPO, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
232 |         tr = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}
233 |         rw = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
234 |         return tr, rw
235 |     ctxs, observed = [], {}
236 |     dry_n = int(os.environ.get('OP4B_DRY_N', '2') or 2)
237 |     try:
238 |         for key, ids_ in sel_ids.items():
239 |             sc, arm, style = key.split('|')
240 |             scen, inst = RB.scenario_and_instruction(sc)
241 |             tr, rw = cell_trials(sc, arm)
242 |             oks = [t for t in tr.values() if t['status'] == 'ok']
243 |             observed[key] = {'n': len(oks), 'style': sum(1 for t in oks if t['style_b']), 'json_n': sum(1 for t in oks if t['style_b']),
244 |                              'json_letters': {x: sum(1 for t in oks if t['style_b'] and t['choice'] == x) for x in ('a', 'b', 'c', 'd', 'refuse')}}
245 |             take = ids_[:1] if PHASE == 'check' else (ids_[:dry_n] if DRY else ids_)
246 |             prompt = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
247 |             for tid in take:
248 |                 cx = context_of(tok, prompt, tr[tid], rw[tid], AT[arm]['sha16'], steer_B.main_position)
249 |                 cx.update({'stratum': key, 'scenario': sc, 'arm': arm, 'style': style})
250 |                 ctxs.append(cx)
251 |     except Stop as e_:
252 |         stop(str(e_))
253 |     mark('contexts', n=len(ctxs), strata=len(sel_ids))
254 | 
255 |     # ---- 7. 教師強制の順伝播（方向は掛けない）
256 |     lm_w, g_w = model.lm_head.weight, model.model.norm.weight
257 |     H_main, H_letter, ctx_rec = [], [], []
258 |     first, first_logits = {}, None
259 |     for k, cx in enumerate(ctxs):
260 |         with torch.no_grad():
261 |             out = model(torch.tensor([cx['ids']], device=dev))
262 |             h = cap['h'][0]
263 |             lg = out.logits[0]
264 |             hm, hl = h[cx['main_pos']].float(), h[cx['letter_pos']].float()
265 |             lm_, ll_ = lg[cx['main_pos']].float(), lg[cx['letter_pos']].float()
266 |             if k == 0:                   # logits の突き合わせ（最初の一件・正本 magnitude.logit_check）
267 |                 recon = lambda hv: (hv * torch.rsqrt(hv.pow(2).mean() + EPS) * g_w.float()) @ lm_w.float().T
268 |                 rm, rl = recon(hm), recon(hl)
269 |                 first = {'main_max_abs': float((rm - lm_).abs().max()), 'letter_max_abs': float((rl - ll_).abs().max()),
270 |                          'main_argmax_equal': int(rm.argmax()) == int(lm_.argmax()), 'letter_argmax_equal': int(rl.argmax()) == int(ll_.argmax())}
271 |                 atol = TL['magnitude']['logit_check']['atol']
272 |                 if not DRY and (first['main_max_abs'] > atol or first['letter_max_abs'] > atol or not first['main_argmax_equal'] or not first['letter_argmax_equal']):
273 |                     stop('logits の突き合わせが外れた: %s' % first)
274 |                 first_logits = (lm_.cpu().numpy().astype(np.float32), ll_.cpu().numpy().astype(np.float32))
275 |             top = lambda v: [[int(i), float(v[i])] for i in torch.topk(v, 5).indices.cpu().numpy()]
276 |             t5m, t5l = top(lm_), top(ll_)
277 |             lmn, lln = lm_.cpu().numpy(), ll_.cpu().numpy()
278 |         pT_main = C.transform(lmn, SAMP['temperature'], SAMP['top_k'], SAMP['top_p'])
279 |         pT_letter = C.transform(lln, SAMP['temperature'], SAMP['top_k'], SAMP['top_p'])
280 |         rec = {k2: v for k2, v in cx.items() if k2 != 'ids'}
281 |         rec.update({'pT_main_fmain': float(pT_main[F_MAIN]), 'pT_letter': {x: float(pT_letter[L_IDS[x]]) for x in ('a', 'b', 'c', 'd', 'refuse')},
282 |                     'top5_main': t5m, 'top5_letter': t5l, 'letter_token_is_L': cx['letter_token'] == L_IDS.get(cx['choice'])})
283 |         ctx_rec.append(rec)
284 |         if PHASE == 'extract':
285 |             H_main.append(hm.cpu().numpy().astype(np.float32))
286 |             H_letter.append(hl.cpu().numpy().astype(np.float32))
287 |     hook.remove()
288 |     mark('forward', n=len(ctx_rec), logit_check=first)
289 | 
290 |     # ---- 8. 較正の検査（正本 magnitude.calibration_check・無操作の確率と観測の率）
291 |     calib, off = calibration_items(list(sel_ids), ctx_rec, observed, TL['magnitude']['calibration_check']['ci'], C.binom_central)
292 |     mark('calibration', outside=off or '無し')
293 |     if off and not DRY:
294 |         stop('較正の検査が区間の外: %s' % off)
295 | 
296 |     # ---- 9. 書き出しと zip
297 |     stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
298 |     od = os.path.join(OUTROOT, '%s-%s' % (PHASE, stamp))
299 |     os.makedirs(od, exist_ok=True)
300 |     np.savez(os.path.join(od, 'random_dirs.npz'), **RDIR)
301 |     RNPZ = {'file': 'random_dirs.npz', 'sha256': hashlib.sha256(open(os.path.join(od, 'random_dirs.npz'), 'rb').read()).hexdigest().upper(),
302 |             'keys': sorted(RDIR), 'dtype': 'float64', 'shape': {k: list(v.shape) for k, v in RDIR.items()}}
303 |     REC = {'kind': 'blens_colab_%s' % PHASE, 'boot': VERSION, 'commit': COMMIT, 'dry': DRY, 'gpu': GPU, 'versions': VER, 'weights_sha256': W_SHA,
304 |            'random_dirs_sha256': RSHA, 'random_dirs_npz': RNPZ, 'selected_sha16': E['selected_sha16'], 'rms_norm_eps': EPS, 'logit_check': first, 'calibration': calib,
305 |            'contexts': ctx_rec, 'observed': observed, 'log': LOG, 'finished': now(),
306 |            'clause': '本記録は器物の出力であり AI の自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
307 |     json.dump(REC, open(os.path.join(od, 'check.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
308 |     if PHASE == 'extract':
309 |         np.savez(os.path.join(od, 'h.npz'), h_main=np.array(H_main), h_letter=np.array(H_letter),
310 |                  logits_first_main=first_logits[0], logits_first_letter=first_logits[1])
311 |     zp = od + '.zip'
312 |     with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
313 |         for fn in sorted(os.listdir(od)):
314 |             z.write(os.path.join(od, fn), os.path.join(os.path.basename(od), fn))
315 |     zsha = hashlib.sha256(open(zp, 'rb').read()).hexdigest().upper()
316 |     mark('done', zip=os.path.basename(zp), sha256=zsha)
317 |     if not DRY:
318 |         try:
319 |             from google.colab import files
320 |             files.download(zp)
321 |         except Exception as e_:
322 |             print('[boot_Blens] zip の自動のダウンロードが走らなかった（左の「ファイル」から落とす）: %s' % e_)
323 |     return od
324 | 
325 | 
326 | if __name__ == '__main__':
327 |     run()
```
<<< 終: `tools/colab/boot_Blens.py` >>>

==================== 第八部 器の段の記録と裁定 ====================

<<< 始: `records/Bl3/tools/tools-log-Bl3.md`（SHA16 2252DEE609624564） >>>
# B-lens 層三の器の段の記録（器を書きながら足していく・コーディネータ・南無弥勒如来）

- 枠: `records/Bl3/tools/frame-tools-Bl3.md`（器を書く前に置いた）。この記録は、器を書いた順と、確かめで見つかったことと直したことを、消さずに足していく。
- 数は器の出力のファイルにあり、この記録では打ち直さない（出力のファイルを指す）。

## 1. 書いた器（この段の一回目の区切りまで）

| 器 | 役目 | 確かめ |
|---|---|---|
| `tools/bl3_directions.py` | 方向の npz を手元で作る（組ごとの SHA-256 を設計事実の転記行 D と突き合わせる・時刻を持たない npz で再実行で同一バイト） | 自己検査・作り直してバイトで突き合わせる `--check`。npz は `results/Bl3/directions-Bl3.npz`（まだコミットしない・正本 `nulls.storage.rule` のとおり下見の前の凍結で置く） |
| `tools/bl3_core.py` | 重みを読まない計算の芯 | 自己検査 |
| `tools/bl3_run.py` | 教師強制の順伝播（加減は段階 B の凍結の `make_hook` をそのまま呼ぶ・近道・読み取りの `float32`・自己検査・層ごとの差分・下見・本の計算・独立の再計算のフックの道） | 合成データの器（下） |
| `tools/analyze_Bl3.py` | 集計（主の札・門・記述の門・q7・予想の答え・独立の再計算の二段の一致） | 合成データの器（下） |
| `tools/dry_run_Bl3.py` | 合成データの確かめ（正本 `review_plan.synthetic` の形と、乱数の小さな模型で端から端まで・壊した読み取りと近道） | 試しの走り（下）・正式の記録は器がすべてそろった後に走らせる |

## 2. 確かめで見つかったことと直したこと（順に）

1. **手早い確かめ**（`records/Bl3/tools/trials/smoke_bl3_run.py`・画面の出力は残していない）:
   - 小さな模型の設定で、層の種類の並びが元の模型の長さのまま残り、使い回しの計算に空の層ができて止まった。合成の器の側で並びを層の数に合わせた（器の誤りではなく、小さな模型の作り方の誤り）。
   - 二重の正規化の壊した読み取りが、出口の値の自己検査を通った。乱数で作った模型の正規化の重みがすべて一なので、二度掛けても値が変わらないため。合成の器で正規化の重みを散らした模型を使うように直した（本物の模型の重みは学習されていて一ではない）。
   - 主位置まで使い回す壊した近道を、効き目で比べる本の計算の頭の近道の確かめが、許容の内として通した。主位置の一つ分の加減の寄与が小さな模型では小さいため。走らせる器に、近道の元が主位置の手前で切れていることの assert（凍結した確かめ）を足した。効き目で比べる確かめの強さの目安は、合成の記録の三の最後の行に記述として残す。
2. **試しの一度目**（`records/Bl3/tools/trials/dry-trial-1-Bl3.md`）:
   - 「帰無との同じ値」の確かめが期待と違った。中身を見ると、同じ距離の比べる相手を置いていなかった（合成の確かめの組み方の誤り・器の誤りではない）。組み方を直した。
   - 乱数の模型では読み取りの集合の確率の和が小さく、下見が正本の閾値どおりに「止める」を出し、本の計算の経路まで通らなかった（器は正しくふるまった）。正本の閾値は変えずに、小さな模型の出口の行列の、読み取りの集合の文字の行を強く出るように置いた（合成だけ）。
3. **試しの二度目**（`records/Bl3/tools/trials/dry-trial-2-Bl3.md`）: すべての確かめが期待どおり。
4. **集計の器をつないだ走り**:
   - 独立の再計算の二段目の一致で、比べる行の集まりが食い違って止まった。合成の走りのフックの道は二行だけで、集計の器は正本どおり v̂ の行のすべてを求めるため。求め方は変えず、合成の走りのときだけ比べる行を絞る口を足した。行が欠ければ一致しないことを確かめる行も足した。一致しないときにも差の最大の欄を返すように芯の関数を直した。
   - 走らせる器の独立の再計算の出力の鍵を、集計の器と同じ「方向|符号」の文字列にそろえた。
5. **試しの三度目**（`records/Bl3/tools/trials/dry-trial-3-Bl3.md`）: すべての確かめが期待どおり（集計の器まで）。

## 3. 登録者に上げること（器を書く途中で見つけた・正本と草案3 の言い方）

- **T1**（枠 §2）: 草案3 の §2 と正本 `readout.primary.batching` の「方向ごとに違うベクトルを一つのバッチで足す道は段階 B に無い新しい道」は事実の取り違え（段階 B の `make_hook` は行ごとの方向の行列を受け、ランダム方向の腕で使った）。層三の器はこのフックをそのまま呼んだ。
- **T2**: 効き目で比べる本の計算の頭の近道の確かめ（正本 `computation.steered_cache_check`）は、主位置まで使い回す近道の誤りに対して、小さな模型では力が弱かった。器に assert を足した（凍結した確かめ・正本 `pilot.decision.tool_error.what` の「assert」）。正本の文に、この assert を足すかどうか。
- **T3**: 正本 `gate.alpha` の「水準」は、門が通る条件を「p が水準を下回る」とも「水準以下」とも書いていない。器は B-lens と段階 B の決まり（p が段を下回る）に合わせて「下回る」にした。全ての入れ替えで数えるので、p がちょうど水準になることがありうる。
- **T4**: 乙（正本 `readout.secondary`・`descriptive.secondary_readout`）の行の決め方（どの方向をどの符号で流すか）が正本に無い。門の行の符号に合わせると、O-Ncold の升目ではランダム方向が両方の符号で入るので、転記行 E の乙の見込み（文脈の数 × 名前のある方向と段階 B の三本の本数、の回数以下）を超える見込みになる。乙の器はまだ書いていない。

## 4. この区切りでまだ書いていない器

- Colab の起動器 `tools/colab/boot_Bl3.py`（相: 確かめ・下見・本の計算・DRY）・乙・組み立ての器 `tools/build_report_Bl3.py`・予想の書式と封印の器・凍結の器と凍結の本文の器・掃き出しの器・独立の再計算の器（残差の書き換えの道・別の個体が書く）。

## 5. 二回目の区切り（裁定 D226・D227 の後・乙・本の計算の関数・起動器）

- 前提: 3 の T1〜T4 は裁定 D226・D227 で決まった（`records/Bl3/rulings-D226-D227.md`・正本への記帳は下見の前の凍結で行う）。同じ許可で、独立の再計算の残差の書き換えの道を書く別の個体（Claude Opus 5.5 の新しい個体）を一体立てた（この区切りの時点ではまだ動いていて、結果は見ていない）。

| 器 | 足したこと | 確かめ |
|---|---|---|
| `tools/bl3_run.py` | 乙の文脈（B-lens の選んだ出力の一覧の SHA16 を確かめ、凍結の `boot_Blens.context_of` で組む）と乙の走らせ方（門の行の符号ごとに無操作と同じバッチ・近道なし）・本の計算の全体の関数 `run_main_phase`（頭の自己検査と近道の確かめ → 全ての升目と符号・等方の層ごとの差分は中央値と中央の区間だけを残す）・独立の再計算のフックの道と乙の進みの印字（値は渡さない） | 合成データの器・起動器の DRY |
| `tools/bl3_core.py` | 独立の再計算の組 `recompute_set`（v̂ の行ごとに無操作・v̂・等方・比べる相手の両方の向き・下見で外した升目の行を除く） | 合成データの器（転記行 E の行ごとの数と一つの道の数に照らす） |
| `tools/analyze_Bl3.py` | 乙の行・乙の順伝播の数・乙のまとめ（B-lens の層二の直接の経路の値を並べる） | 合成データの器 |
| `tools/dry_run_Bl3.py` | 本の計算を起動器と同じ `run_main_phase` で通す形に改めた・乙の確かめ三つ・独立の再計算の組の確かめ・零のベクトルの行の確かめを同じ升目と符号の別の組の走りで・二段目の比べる行を減算の行と加算の行の一つずつに（下の 7）・乱数の模型の読み取りの集合の行の置き直しを関数にした（起動器の DRY も呼ぶ） | 試しの四度目・五度目 |
| `tools/colab/boot_Bl3.py`（新） | 相 check（順伝播を一度も呼ばない・呼ばれたら止める hook を模型に掛ける）・相 pilot・相 main（組 main・recompute・secondary・組ごとに出力を置く・進みは出力の置き場にも書く）・DRY | 手元の DRY で三つの相（下の 9） |

6. **試しの四度目**（`records/Bl3/tools/trials/dry-trial-4-Bl3.md`・下の 7 の直しの前の版）: すべての確かめが期待どおり。ただし、本の計算の頭の近道の確かめの差の最大が許容に近く、同じ走りの二段目の差の最大より三桁ほど大きかった。
7. **切り分け**（`records/Bl3/tools/trials/probe_cache_check.py`・画面の出力は残していない）: 差は主の組の一つの升目（N1|Onull）だけにあり、近道が**無操作の値**を動かし、方向を加えた行は二つの道でビットまで同じだった（大きなベクトルを足してから bf16 に丸めると、二つの道の小さな差が消えるため）。効き目は加えた値から無操作の値を引くので、無操作の差がそのまま効き目の差に出る。確かめは正本 `computation.steered_cache_check` のとおりに測れていた（器の誤りではない）。合成の二段目が比べていた二行はどちらも減算の行で、この升目を含まなかったので、減算の行と加算の行を一つずつ（加算の行は N1|Onull の升目）比べる形に直した。
8. **試しの五度目**（`records/Bl3/tools/trials/dry-trial-5-Bl3.md`）: すべての確かめが期待どおり。二段目の差の最大が、近道の確かめの差と同じ桁になった（二段目が近道の差を拾えることが、合成で見えるようになった）。本物の模型でも二段目の差が許容に近づくことはありうる（許容の外なら、正本どおり結果を開く前に止めて登録者に上げる）。
9. **起動器の DRY**（`records/Bl3/tools/trials/boot-dry-1/`・相ごとの進みの印字と記録）: 三つの相が止まらずに終わった。相 check は順伝播を呼ばずに、升目と符号の組と独立の再計算の組の順伝播の数を転記行 E に、門の行を転記行 C に照らし、乙の文脈をすべて組んだ。残差の書き換えの器はまだ個体の作業場にあるので「import できない」と記録し、DRY に限って飛ばした。相 pilot の機械の決定・揺れの床・近道の許容は、合成データの器の下見と同じ値になった。相 main の三つの組の出力（JSON）を手元の集計の器にそのまま読ませ、主の札・門・予想の答え・二段目の一致・乙のまとめが出ることを確かめた（`records/Bl3/tools/trials/probe_boot_outputs.py`・値は印字していない）。

## 6. この区切りでまだ書いていない器

- 組み立ての器 `tools/build_report_Bl3.py`・予想の書式と封印の器・凍結の器と凍結の本文の器・掃き出しの器・残差の書き換えの器の取り込み（個体の作業場から・中身と独立の書き方を確かめてから）。

## 7. 三回目の区切り（独立の再計算の器の取り込み・正本 v6・凍結の準備の器）

- **独立の再計算の個体の報告（申告）と、コーディネータの確かめ**:
  - 書いたもの: `tools/bl3_recompute_rewrite.py`・`records/Bl3/tools/recompute-rewrite-dev-Bl3.md`。個体の作業場から中を変えずに写した（SHA16 は個体の申告と同じ・個体の作業場の git の状態で、既にあるファイルを一つも変えていないことを確かめた）。
  - 器を最初から読んだ: 層を手で回し、層 L の出力の主位置から後ろに bf16 のまま足し、最終の正規化の入力を float32 で読む。フックが掛かっていたら止める。算術は段階 B のフックと同じ形。フックの道の器は開かず、`--dry` で公開の関数を呼ぶだけ。
  - 自己検査と `--dry` をコーディネータの側で走らせ直した（`records/Bl3/tools/trials/recompute-rewrite-selftest-coordinator-rerun.log`・`recompute-rewrite-dry-coordinator-rerun.log`）。数は個体の申告と同じだった。
  - 個体の指摘の一つ目（mask の組み方）: 既定の呼び方と `use_cache=False` で mask の組み方が違う（自己検査の参考の行で確かめた）。本の器のフックの道の近道なしは `use_cache=False` なので、起動器では書き換えの道も `use_cache=False` で呼ぶ（器の決め・下の T7）。
  - 個体の指摘の二つ目（合成の確かめの盲点）: 小さな模型では足す量が選んだ層の出力より二桁ほど大きく、効き目が飽和して、三つの変種が一段目の許容の内に収まった。合成データの器に、方向の大きさを正本の相対の加減（`layers.vhat_over_h`）に合わせた記述の確かめを二つ足した（`records/Bl3/tools/trials/dry-trial-6-Bl3.md` の三の最後の二行）。その大きさでは、個体の変種はすべて一段目の許容の外に出て、主位置の一つ分の寄与も近道の許容と一段目の許容を上回った。合成の模型の上の目安で、本物の模型の上では言えない（封印の前は走らせない）。
  - 個体の指摘の三つ目（独立の範囲）: 二つの道は同じ正本から系統内の個体が書いたので、正本の共有の読み違いはこの突き合わせでは捕まらない。系統外の検分を勧められた（下の T8）。
- **正本 v6**（`tools/make_contrasts_Bl3.py` v6・版 draft3-r2-2026-09-25）: 裁定 D226・D227 の中身を入れた。v5 との差が狙った鍵だけであることを機械で確かめた（T1 の文〔`readout.primary.batching`〕・T2〔`computation.shortcut_assert`〕・T3〔`gate.pass_rule`〕・乙の行と流し方〔`readout.secondary.rows`・`batching`〕・`decisions` の D226・D227・`inputs.files` の裁定の記録・版の名・生成器の版・次の番号）。
- **設計事実 v5**（`tools/bl3_facts.py` v5）: 転記行 E の乙の見込みを D227 の決まりで数え直した（転記行 C の門の行から）。集計の器の数え方（段階 B の記録から門の行を作り直す）と一致することを、合成データの器の確かめに足した。ほかの行は変わっていない（機械で確かめた）。
- **方向の記録**: 正本の SHA16 の欄だけを書き直した（npz は作り直してバイトで同じ）。
- **新しい器**: 予想の書式と封印（`tools/make_predictions_form_Bl3.py`・`tools/seal_Bl3.py`・封印は下見の前の凍結の記録が無ければ止め、本の凍結の後も止める）・報告の組み立てと掃き出し（`tools/build_report_Bl3.py`・`tools/sweep_Bl3.py`）・集計の器の手元の二つの段（一致だけを見る段は判定だけを書き、結果を開く段は一致の記録が無ければ止める）・凍結の本文（`tools/make_frozen_Bl3.py`）・凍結の記帳（`tools/freeze_Bl3.py`・下見の前の凍結と本の凍結）。
- **起動器の DRY の二度目**（`records/Bl3/tools/trials/boot-dry-2/`）: 書き換えの道つきで相 main の三つの組が終わり、一致だけを見る段が一段目と二段目をともに一致と判定した（値は開いていない）。続けて結果を開く段 → 掃き出し（欠け無し）→ 報告の組み立て（走査の違反なし）まで通した（合成の出力・一時の置き場）。
- **端から端まで通して見つかったこと**: B-lens の層二の直接の経路の値は文脈の間の要約（平均・中央値・四分位）の形で、報告の器は数一つの形を仮定していた。報告の器の自己検査の合成の値が実物と違う形だったので見逃していた。報告の器を実物の形に直し、自己検査の合成の値も実物と同じ形にした。
- **試しの六度目**（`records/Bl3/tools/trials/dry-trial-6-Bl3.md`）: すべて期待どおり（足した確かめは、乙の順伝播の数と転記行 E の突き合わせと、本物の相対の加減の大きさでの二つの記述）。
- **凍結の記帳の器の確かめだけの走り**: 今そろっていないもの（凍結の本文・正式の合成データの記録・書式・器の実装の検分の記録）だけを外れとして並べ、器の自己検査はすべて通った。

## 8. 登録者に上げること（三回目の区切り）

- **T5 凍結の本文の組み方**: 裁定 D226 は正本の文を直すので、正本の鍵から組まれる本文の行（§3.3 のバッチの文・§6 の転記行 E など）は凍結の本文で変わる。一方、草案3 の原稿に直に書かれた §2 の同じ言い方（「方向ごとに違うベクトルを一つのバッチで足す道は層三の器で新しく書く」）は、原稿を直さないと残る。凍結の本文の器は、草案3 の原稿に題名の印と凍結の一行を足し、§2 の一文を D226 の言い方に直して組み、草案3 との差が「題名・凍結の一行・組み立ての記録・正本と設計事実から来る行・原稿の直し」だけであることを機械で確かめる形にした（差の記録 `records/Bl3/frozen-diff-Bl3.md`）。段階 B と B-lens の型（題名と凍結の一行だけを変える）から外れるので、この組み方でよいか。
- **T6 「この結果が退けた説明」**: 報告の雛形（正本 `report_rules.template`）は §0 にこれを並べるが、正本に文が無い。報告の器は起草者の欄（〔〕）を置き、結果を開いた後に起草者が書く（数は打たない・読みの表の型と書かないことの一覧に従う）。欄が埋まらなければ走査が止める。この形でよいか。
- **T7 書き換えの道の mask の組み方**（器の決め・報告）: 上の個体の指摘の一つ目のとおり、起動器では書き換えの道を `use_cache=False` で呼ぶ。
- **T8 系統外の検分**（個体の勧め）: 正本 `review_plan.no_more` は「この順のほかに巡を置かない」。器の実装の検分は系統内の二体（裁定 D209）で、二つの道の共有の読み違いは捕まらない。巡を足さずに限界として報告に書くか、系統外の目を一つ足すか。
- **T9 起動器の相 main の組**（器の決め・報告）: 相 main を三つの組（本の計算・独立の再計算・乙）に分け、組ごとに出力を置く。ランタイムが落ちたら、落ちた組から新しいランタイム（同じ GPU の種類）で走らせ直し、逸脱の台帳に記す。二段目の比べには組の間の環境の違いが入りうるので、集計の器は組の間の環境（コミット・GPU・版）が同じかを記す。

## 9. この区切りでまだしていないこと

- 正式の合成データの記録（等方の本数を正本のまま）・凍結の本文と予想の書式の生成（下見の前の凍結で）・器の実装の検分（系統内の新しい個体二体）・Colab の相 check。

## 検分票（一回目の区切り）

- 対象: 器の段の一回目の区切りまでに書いた器と、合成データの試しの走り。
- 段階: 枠は器を書く前に置いた（事前登録）。試しの走りは、器を直しながら重ねた（通るまで直したことを、この記録に残した）。
- 凍結物の同定: 層三の凍結物はまだ無い。段階 B と B-lens の凍結の器は読み取りだけで呼び、変えていない。
- 盲検の状態: 該当しない。
- 敵対的検分: 壊した読み取りと壊した近道を、器が止めるかを確かめた。止まらなかった二つ（二重の正規化・主位置まで使い回す近道）は、原因を確かめて直した。合成の確かめの組み方の誤りも一つ見つけて直した。
- 系統の内訳: 起草者（Claude 系）一名。外の目は、器の実装の検分（系統内の新しい個体）と独立の再計算の器（別の個体）まで入らない。
- COI記録: 器を書くのも合成の確かめを書くのも起草者で、「通った」と書く側に引かれる。確かめが期待と違ったときは、器ではなく確かめの側を直したくなる引力がある。直した三つのうち二つが確かめの側の直しだったので、それぞれ原因を書いた。
- 判定: 器の段の途中（器がそろっていない）。
- 本検分が確認していないこと: 本物の模型での値の出方（封印の前は走らせない）。GPU の上での bf16 の揺れと近道の差の大きさ。乙・起動器・組み立ての器・封印と凍結の器（まだ書いていない）。

## 検分票（二回目の区切り）

- 対象: 二回目の区切りまでに足した器（乙・本の計算の関数・独立の再計算の組・起動器）と、試しの四度目・五度目と、起動器の DRY。
- 段階: 枠は器を書く前に置いた（事前登録）。試しの走りは器を直しながら重ねた。起動器の DRY がどう通るかの予想は書いていない（事後）。
- 凍結物の同定: 層三の凍結物はまだ無い。段階 B と B-lens の凍結の器（`run_stageB_local`・`steer_B`・`direction_B`・`boot_Blens.context_of`・`blens_core`）は読み取りだけで呼び、変えていない。
- 盲検の状態: 該当しない。独立の再計算の個体には、本の器の中身を開かないよう頼んだ（守られたかは、個体の記録と作業場で確かめる・まだ）。
- 敵対的検分: 近道の確かめの差が許容に近かったことを、通ったこととして流さずに切り分けた（升目ごと・方向ごと・無操作ごとの差で、器の誤りでないことを確かめた）。合成の二段目が弱い行だけを比べていたことを見つけて直した。起動器の出力を集計の器に往復させた。
- 系統の内訳: 起草者（Claude 系）一名。独立の再計算の個体（系統内の新しい個体）はまだ終わっていない。器の実装の検分はこの後。
- COI記録: 「通った」と書く側に引かれる。近道の確かめの差が許容の内だったので、そのまま流したくなる引力があった。切り分けで器の誤りでないと分かったが、同じ理由から、本物の模型で二段目が許容に近づく見込みを 8 に書き、良い方にだけ読まないようにした。
- 判定: 器の段の途中（組み立ての器・予想の書式と封印の器・凍結の器・掃き出しの器と、残差の書き換えの器の取り込みがまだ）。
- 本検分が確認していないこと: 本物の模型と GPU の上での値の出方と時間（封印の前は走らせない）。Colab での版の入れ直しと疎な取り出し（手元の DRY は取り出しを通らない）。残差の書き換えの器との一段目。起動器の組を分けて走らせ直す流れ（DRY で試していない）。

## 検分票（三回目の区切り）

- 対象: 独立の再計算の器の取り込み（個体の申告の確かめ）・正本 v6 と設計事実 v5・凍結の準備の器（書式・封印・報告・掃き出し・凍結の本文・凍結の記帳）・起動器の DRY の二度目・試しの六度目。
- 段階: 個体の器の確かめは、個体の報告を読んだ後（事後）。正本 v6 の差は、直す前に狙った鍵を決めてから機械で確かめた。起動器の DRY の二度目と報告の組み立ての通り方の予想は書いていない（事後）。
- 凍結物の同定: 層三の凍結物はまだ無い。段階 B と B-lens の凍結の器は読み取りだけで呼び、変えていない。個体の器は写しただけで変えていない（SHA16 で確かめた）。
- 盲検の状態: 個体には本の器の中身を開かないよう頼んだ。個体の記録と報告は開いていないと言う（申告）。個体の器の中に本の器の中身を写した跡は見当たらなかった（読んだ限り・突き合わせは `--dry` の公開の関数の呼び出しだけ）。
- 敵対的検分: 個体の数を自分の走りで再現した。個体の盲点の指摘を、通ったこととして流さずに、正本の大きさの合成で測り直した。端から端まで通して、合成の自己検査が実物と違う形の値を使っていた誤りを一つ見つけて直した。
- 系統の内訳: 起草者（Claude 系）と、独立の再計算の個体（系統内の新しい個体）。系統外の目はまだ入っていない（T8）。
- COI記録: 個体の器が「通った」ことと、自分の器と一致したことを、そのまま良い知らせとして書きたくなる引力がある。二つの道が同じ正本から同じ系統で書かれたので、一致は共有の読み違いを捕まえないことを T8 に書いた。正本の大きさの合成で変種が捕まったことも、合成の模型の上の目安にとどめた。
- 判定: 器の段の途中（正式の合成データの記録・凍結の本文と書式の生成・器の実装の検分・Colab の相 check が残る）。登録者裁定の候補 T5・T6・T8、報告 T7・T9。
- 本検分が確認していないこと: 本物の模型と GPU の上で、一段目の許容がどれだけの誤りを捕まえるか（合成の目安しかない）。GPU の上で二つの道の mask の組み方をそろえたときの一段目の差の大きさ。凍結の本文を実際に組んだときの差（凍結の本文はまだ組んでいない）。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/tools/tools-log-Bl3.md` >>>

<<< 始: `records/Bl3/rulings-D226-D227.md`（SHA16 0C0B6BD0B5771BE4） >>>
# 登録者裁定 D226・D227（2026-09-25・B-lens 層三・器の段の一回目の区切りの後）

- 登録者の言葉（逐語・会話の記録 uuid `2ee079c7-0ec4-461b-bd62-f0c4f4b8c81b`・2026-09-25 06:23 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏D226とD227はご推奨どおりで、三つのコミットのpushをお願いします。「独立の再計算の器を書く個体を一体立ててよいか」についても、ご提案のとおり、Claude Opus 5.5 の新しい個体（エージェント）にお願いしてください。以上、よろしくお願いします🍵」
- 「ご推奨」は、各裁定の候補の一つ目の案。裁定の前にコーディネータが示した推奨の段と、同じ返信の「次に進む前のお願い」の段を下に逐語で置く（会話の記録 uuid `0a3fb224-d599-47ba-82d1-ae5b98fbb472`・2026-09-25 06:14 日本時間）。
- 前提: 器の段の記録 `records/Bl3/tools/tools-log-Bl3.md` の「登録者に上げること」（T1〜T4）。

| 裁定 | 採られた案（抜き書きの一つ目の案・逐語・字下げの改行は空白にした） |
|---|---|
| D226 | 次の三つを正本に入れる - **T1**：段階 B のフックにはもともと行ごとに違う方向を足す形があり、ランダム方向の腕で使っていました。草案3 はこれを「段階 B に無い新しい道」と書いています。第一巡の事実の確かめ（K424）で、私がこの形を見落としたのが原因です。決まりは変えず、言い方だけを直します。 - **T2**：「近道の元が主位置の手前で切れていることを assert で確かめる」を書き足します。 - **T3**：門が通る条件を「p が水準を下回るとき」と明記します。段階 B と B-lens の決まりに合わせます。全ての入れ替えで数えるので、p がちょうど 0.05 になることがありえます。 |
| D227 | 門の行のうち、方向が名前のある方向か段階 B の三本で、土台の升目が B-lens の層二の層にある行とし、符号は門の行の符号にする - B-lens の層二の答えの文字の位置の行と同じ行にそろいます。 - ただし O-Ncold の升目ではランダム方向が両方の符号で入るので、転記行 E の乙の見込みを少し超えます。見込みは器で数え直して直します。 |

## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）

````text
## ご裁定をお願いしたいこと（一つ目が私の推奨）

- **D226 正本の文の直し（下見の前の凍結で入れる）**
  1. 次の三つを正本に入れる
     - **T1**：段階 B のフックにはもともと行ごとに違う方向を足す形があり、ランダム方向の腕で使っていました。草案3 はこれを「段階 B に無い新しい道」と書いています。第一巡の事実の確かめ（K424）で、私がこの形を見落としたのが原因です。決まりは変えず、言い方だけを直します。
     - **T2**：「近道の元が主位置の手前で切れていることを assert で確かめる」を書き足します。
     - **T3**：門が通る条件を「p が水準を下回るとき」と明記します。段階 B と B-lens の決まりに合わせます。全ての入れ替えで数えるので、p がちょうど 0.05 になることがありえます。
  2. 器にだけ置き、正本の文は変えない（凍結の記録に注を書く）
- **D227 乙の行の決め方（T4）**
  1. 門の行のうち、方向が名前のある方向か段階 B の三本で、土台の升目が B-lens の層二の層にある行とし、符号は門の行の符号にする
     - B-lens の層二の答えの文字の位置の行と同じ行にそろいます。
     - ただし O-Ncold の升目ではランダム方向が両方の符号で入るので、転記行 E の乙の見込みを少し超えます。見込みは器で数え直して直します。
  2. 方向ごとに符号を一つに絞る
````

## 同じ返信の「次に進む前のお願い」（逐語）

````text
## 次に進む前のお願い

1. **独立の再計算の器を書く個体を一体立ててよいか**
   - 正本の「別の個体が書く」に当たる一体で、Claude Opus 5.5 の新しい個体です。
   - 仕事は、残差の書き換えの道を正本の決まりから書き、乱数の小さな模型で一段目の一致を確かめることです。私の走らせる器のフックの実装は、独立を保つために読ませません。
   - 費用は、一体で数十万トークンほどの見込みです。
2. **push の許可**：ローカルのコミット 3259cc3・ca1fe0a・3bb772e を push してよいか。

ご判断を待つ間も、残りの器を書き進めます。具体的には、Colab の起動器・乙・報告の組み立ての器・予想の書式と封印・凍結の器・掃き出しの器です。乙は D227 のご判断の後に書きます🍵
````

## 注（事実のみ）

- 同じ言葉で、登録者は独立の再計算の器を書く個体を一体（Claude Opus 5.5 の新しい個体・エージェント）立てることと、三つのコミット（3259cc3・ca1fe0a・3bb772e）の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は 3bb772e）。
- 記帳の置き場: 正本の `decisions` への D226・D227 の記帳と、裁定の中身（T1〜T3 の文・乙の行の決め方・転記行 E の乙の見込みの数え直し）は、下見の前の凍結の正本で行う（D226 の一つ目の案の「下見の前の凍結で入れる」）。
- 番号: 次の裁定は D228 から。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/rulings-D226-D227.md` >>>

<<< 始: `records/Bl3/rulings-D228-D230.md`（SHA16 06978FA3DCB5310E） >>>
# 登録者裁定 D228〜D230（2026-09-25・B-lens 層三・器の段の三回目の区切りの後）

- 登録者の言葉（逐語・会話の記録 uuid `4783a54c-2624-44da-8ce6-86c57ba4d224`・2026-09-25 08:18 日本時間）: 「南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏D228〜D229はご推奨どおりで、D230は、２の方向性で行きましょう。つまり、２については、検分ではなく、意見伺いという体で系統外（Gemini）二名とclaude.aiのOpus 5.5 二名に伺いましょう。依頼文とバンドルをご用意していただければ、私がお伺いしますよ。三つのコミットのpushをお願いします🍵」
- 裁定の前にコーディネータが示した推奨の段と、同じ返信の「次に進む前のお願い」の段を下に逐語で置く（会話の記録 uuid `5c965d30-be2e-4cdc-9319-2112b44a0fe0`・2026-09-25 08:09 日本時間）。
- 前提: 器の段の記録 `records/Bl3/tools/tools-log-Bl3.md` の §8「登録者に上げること（三回目の区切り）」（T5・T6・T8。T7・T9 は報告）。

| 裁定 | 採られた案（抜き書きから機械で切り出した・字下げの改行は空白にした） |
|---|---|
| D228 | 一つ目の案（ご推奨どおり）: 草案3 の原稿に題名の印と凍結の一行を足し、§2 の一文を D226 の言い方に直して組みます。正本から組まれる行は自然に変わります。草案3 との差がこれらだけであることを器が確かめ、差の記録に並べます。 |
| D229 | 一つ目の案（ご推奨どおり）: 報告の器は起草者の欄を置き、結果を開いた後に私が書きます。数は打たず、欄が空なら走査が止めます。結果の巡で見ていただきます。 |
| D230 | 二つ目の案の方向: 下見の前の凍結の前に、系統外（Gemini）の検分を一つ足します。 ／ 登録者の言葉の形（逐語）:「D230は、２の方向性で行きましょう。つまり、２については、検分ではなく、意見伺いという体で系統外（Gemini）二名とclaude.aiのOpus 5.5 二名に伺いましょう。依頼文とバンドルをご用意していただければ、私がお伺いしますよ。」 |

## 裁定の前にコーディネータが示した推奨（抜き書き・逐語）

````text
## ご裁定をお願いしたいこと（一つ目が私の推奨）

- **D228 凍結の本文の組み方**
  1. 草案3 の原稿に題名の印と凍結の一行を足し、§2 の一文を D226 の言い方に直して組みます。正本から組まれる行は自然に変わります。草案3 との差がこれらだけであることを器が確かめ、差の記録に並べます。
  2. 段階 B・B-lens の型どおり題名と凍結の一行だけを変え、§2 の古い言い方は残して、凍結の記録に注を書きます。
- **D229 報告の「この結果が退けた説明」**（報告の雛形にはあるが、正本に文がない）
  1. 報告の器は起草者の欄を置き、結果を開いた後に私が書きます。数は打たず、欄が空なら走査が止めます。結果の巡で見ていただきます。
  2. 凍結の前に、正本に決まった文を足します。
- **D230 系統外の目**（個体の勧め：二つの道は同じ正本から同じ系統が書いたので、正本の読み違いを共有していれば突き合わせでは捕まらない）
  1. 巡は足さず、この限界を報告の限界に書きます。器の実装の検分の二体には、正本を自分で読み直して、二つの道が同じ読み違いをしていないかを重点に見てもらいます。
  2. 下見の前の凍結の前に、系統外（Gemini）の検分を一つ足します。

ご報告だけの点が二つあります。書き換えの道の mask の呼び方をそろえたことと、相 main を三つの組に分けて、ランタイムが落ちたら落ちた組から走らせ直す（逸脱の台帳に記す）ことです。
````

## 同じ返信の「次に進む前のお願い」（逐語）

````text
## 次に進む前のお願い

1. **push の許可**：0546a80（D226・D227 の記録）・b354548・0bfc0c2 を push してよいでしょうか。0bfc0c2 には正本 v6 が入ります。
2. **次の段取り**：ご裁定の後、次の順に進めます。
   - 合成データの正式の記録（等方の本数は正本のまま）を取ります。
   - 器の実装の検分に進みます。Claude Opus 5.5 の新しい個体を二体、読むだけで立て、合成データの確かめも自分で走らせてもらいます。費用は一体あたり 40万〜60万トークンほど、合わせて約 100 万トークンの見込みです。立ててよいかは、その時にあらためて伺います。
   - その後、Colab の check の相（読み込みと版の確かめだけ）→ 下見の前の凍結 → 封印、と進みます。

個体の作業場（写し元）は残してあります。push の後に片づけてよければ、そうします🍵
````

## 注（事実のみ）

- 同じ言葉で、登録者は三つのコミット（0546a80・b354548・0bfc0c2）の push を許可した。push は済んでいる（この記録を書いた時点の origin/main は 0bfc0c2）。
- D228 と D229 の中身は、器の段の三回目の区切りで既に器に入っている（凍結の本文の器 `tools/make_frozen_Bl3.py`・報告の組み立ての器 `tools/build_report_Bl3.py`）。
- D230 は、正本 `review_plan` の巡には数えない意見伺いで、依頼文とバンドルはコーディネータが用意し、登録者が系統外（Gemini）二名と claude.ai の Claude Opus 5.5 二名に伺う。返ってきた意見は逐語で保全し、コーディネータが採否の案を組み、登録者が裁定する。claude.ai の二名はコーディネータと同じ系列で、何名でも一票に数える（裁定 D59 の数え方）。
- 記帳の置き場: 正本の `decisions` への D228〜D230 の記帳は、下見の前の凍結の正本で行う（D226・D227 と同じ）。
- 番号: 次の裁定は D231 から。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
<<< 終: `records/Bl3/rulings-D228-D230.md` >>>
