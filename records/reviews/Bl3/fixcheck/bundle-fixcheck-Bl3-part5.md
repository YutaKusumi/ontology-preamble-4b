（B-lens 層三の器の直しの確かめの束・分けた版 5／7・中身は一通版と同じ）

<<< 始: `tools/build_report_Bl3.py`（SHA16 11010753B98162E5・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """build_report_Bl3.py v3 —— B-lens 層三（Bl3）の結果の報告の草案を組む（2026-09-25・正本 `reading_rules`・`negation_templates`・`report_rules`・`labels`・`limits`）。
  3 | 
  4 | 組み立て（B-lens の組み立ての器 `tools/build_report_Blens.py` の型）:
  5 |   - 数はすべて機械の区画（凍結の走査器 `tools/report_lint.py` の区画の印）の中に置く。区画ごとの中身の SHA16 を別の記録（報告と同じ名の -machine.json）に書く。
  6 |   - 頭に、凍結の後の逸脱の一覧（凍結の記録の `deviations`・台帳から器が読む）と、下見をやり直したときの一度目の下見の記録と機械の決定（裁定 D222）を置く。
  7 |   - 状態は機械の区画で、登録者最終確認の前と後の二つの型（確認の後は逐語と時刻・`records/Bl3/final-confirmation-Bl3.json`・裁定 D199 の型）。
  8 |   - §0 に「見ていない場所」（正本 `scope.not_answered`）と「この結果が退けた説明」を置く。後者は正本に文が無いので起草者の欄（〔〕）にし、`--rejected` で起草者の行を受ける
  9 |     （欄が埋まらなければ走査が埋め残しとして止める）。答えの言い方には読み取りの位置の範囲を添える（正本 `scope.reach` と打ち消しの定型）。
 10 |   - 読みの型は、正本の読みの表の条件を器が当て、当たった型の「書くこと」を並べる（型は重なりうる）。「下見で止めた」の二つの文は、止まった理由で器が選ぶ。
 11 |     等方の外の行には、等方の帰無の中央値と効き目の側（正本 `labels.side_rule` の〔〕の三つの言い方を器が切り出す）を添える。
 12 |   - 主の表に、行ごとの p と裾の本数・等方の中央値・効き目の側・二つ目の札の中心と順位・等方の最上位の割合と、段階 B のその行の札と注を並べる。
 13 |     升目と符号ごとの無操作の選択肢 a の文字の確率（裁定 D223）と、質量が `pilot.mass_min` を下回った方向の数を、主の表の隣に並べる。
 14 |   - 下見の記録（`pilot.decision.report` に並べるもの）・門（本の門・v̂ を抜いた門・記述の門・段階 B の注のある門の行）・記述（頭の確かめ・層ごとの差分の置き場・乙と
 15 |     B-lens の直接の経路）・独立の再計算の二段・予想の照合（記録であり評価ではない）・限界・情報状態。
 16 |   - 逸脱の印を受け取る口（`--marks`: 節の鍵 → 逸脱の番号の並び）。印は節の頭の機械の区画に置く。
 17 |   - 掃き出し（`tools/sweep_Bl3.py`）: 正本と凍結の本文が求める出力の一覧を、集計の出力と突き合わせ、欠けがあれば止める。
 18 | 走査: 凍結した走査器 `tools/report_lint.py` の関数 `lint` を、正本の禁止語（価値語・機序語）に `print_strings.added_ban` と `print_strings.reading_never_ban` を足して呼ぶ。
 19 |   違反があれば、報告を書いた後に非零で終わる。
 20 | 入力: 集計の器の結果を開く段の出力（`records/Bl3/analysis-Bl3.json`）・一致だけを見る段の記録・凍結の記録・封印の記録と二つの予想・正本。
 21 |   下見で止まったとき（または下見の器の誤りでやり直さなかったとき）は、集計の出力なしに凍結の記録の下見の記録だけで組む。
 22 | 出力: records/Bl3/results-Bl3.md・results-Bl3-machine.json・results-Bl3-lint.md（--force が無ければ上書きしない）。
 23 | 用法: python tools/build_report_Bl3.py [--force] [--rejected <起草者の行の md>] [--marks <印の JSON>] [--main-tool-error] ／ --selftest
 24 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 25 | """
 26 | import os, re, sys, json, hashlib, argparse, collections
 27 | 
 28 | HERE = os.path.dirname(os.path.abspath(__file__))
 29 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 30 | sys.path.insert(0, HERE)
 31 | import report_lint as RL
 32 | 
 33 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 封印した予想と凍結の記録と手元の器を照らしてから組む・(v) の行の言い方・門の行だけの升目の外し・nuclear の族の文を §0 に・下見の GPU・自己検査の足し／v2（裁定 D231〜D235）
 34 | NL = chr(10)
 35 | OUT = os.path.join(REPO, 'records', 'Bl3', 'results-Bl3.md')
 36 | FENCE = '本報告のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
 37 | SECTIONS = ('summary', 'pilot', 'main', 'gate', 'descriptive', 'recompute', 'predictions', 'limits')
 38 | REJECTED_BLANK = '〔この結果が退けた説明: 結果を登録者と一緒に開いた後に起草者が書く（読みの表の型と書かないことの一覧に従う・数は打たない）〕'
 39 | f4 = lambda x: 'なし' if x is None else ('%.4g' % x)
 40 | br = lambda s: str(s).replace('〔', '［').replace('〕', '］')     # 段階 B の行の名の〔〕は、走査が記入欄と読むので印字では［］に写す
 41 | yn = lambda b: 'はい' if b else 'いいえ'
 42 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 43 | P = lambda r: os.path.join(REPO, *r.split('/'))
 44 | 
 45 | 
 46 | def machine(lines, MB):
 47 |     return [MB['begin']] + list(lines) + [MB['end']]
 48 | 
 49 | 
 50 | def side_words(T3):
 51 |     """効き目の側の言い方（正本 `labels.side_rule` の〔〕の三つを器が切り出す）。"""
 52 |     q = re.findall(r'〔([^〕]*)〕', T3['labels']['side_rule'])
 53 |     assert len(q) == 3, q
 54 |     return {'stronger': q[0], 'weaker': q[1], 'opposite': q[2]}
 55 | 
 56 | 
 57 | def side_text(T3, s):
 58 |     if not s:
 59 |         return 'なし（等方の外でない）'
 60 |     if s['side'] == 'sign_only':
 61 |         return '符号だけ（零が等方の帰無の四分位の間）: %s' % ('正' if s['sign'] > 0 else ('負' if s['sign'] < 0 else '零'))
 62 |     return side_words(T3)[s['side']]
 63 | 
 64 | 
 65 | def stop_sentence(T3, reason):
 66 |     """「下見で止めた」の二つの文（正本の読みの表の「」の二つ・一つ目は (i)(ii)・二つ目は (vi) の (b)）を、止まった理由で選ぶ。"""
 67 |     w = [r for r in T3['reading_rules'] if r['type'] == '下見で止めた'][0]['write']
 68 |     q = re.findall(r'「([^」]*)」', w)
 69 |     assert len(q) == 2, q
 70 |     return q[1] if reason == 'vi_b' else q[0]
 71 | 
 72 | 
 73 | def dropped_split(T3, dec):
 74 |     """下見で外した升目を、主の升目と門の行だけの升目に分ける（裁定 D236）。"""
 75 |     main_cells = {'%s|%s' % tuple(c) for c in T3['cells_main']}
 76 |     d = list((dec or {}).get('dropped') or [])
 77 |     return [c for c in d if c in main_cells], [c for c in d if c not in main_cells]
 78 | 
 79 | 
 80 | def reading_types(T3, A):
 81 |     """読みの表の条件を当てる（型は重なりうる）。戻り値: [(型, 当たった所, 書くこと)]。"""
 82 |     RR = {r['type']: r for r in T3['reading_rules']}
 83 |     last = A['pilot_attempts'][-1]
 84 |     dec = last.get('decision') or {}
 85 |     hits = []
 86 |     if A['predictions_meta']['stopped']:
 87 |         if last.get('tool_error'):
 88 |             return [('器の誤り', '下見', '器の誤りで下見を終えられなかった（正本 pilot.decision.tool_error）')]
 89 |         return [('下見で止めた', '下見の決め', RR['下見で止めた']['write'] + '（この下見で当たる文:「%s」）' % stop_sentence(T3, dec.get('reason')))]
 90 |     md_, gd_ = dropped_split(T3, dec)
 91 |     if md_:                                                            # 主の升目を外したときだけ（門の行だけの升目の外しは §0 の機械の行・裁定 D236）
 92 |         hits.append(('下見で一部を外した', '・'.join(md_), RR['下見で一部を外した']['write']))
 93 |     if last.get('iv'):
 94 |         hits.append(('揺れの版の値', '下見の (iv)', RR['揺れの版の値']['write']))
 95 |     rows = A['rows']
 96 |     if not any(o['iso_outside'] for o in rows.values()):
 97 |         hits.append(('区別できない', '主の行', RR['区別できない']['write']))
 98 |     for rid, o in rows.items():
 99 |         if o['iso_outside']:
100 |             t = '両方の外' if o['second']['top'] else '埋もれる'
101 |             hits.append((t, rid, RR[t]['write'] + '（等方の帰無の中央値と効き目の側は主の表）'))
102 |         else:
103 |             hits.append(('外でない行', rid, RR['外でない行']['write']))
104 |             if o['second']['top']:
105 |                 hits.append(('二つ目の札だけ', rid, RR['二つ目の札だけ']['write']))
106 |     G = A['gates']['main']
107 |     if not G.get('undetermined'):
108 |         t = '門を通った' if G['pass'] else '門を通らない'
109 |         hits.append((t, '本の門', RR[t]['write']))
110 |     return hits
111 | 
112 | 
113 | def pilot_lines(T3, rec, MB, title):
114 |     """下見の記録（正本 `pilot.decision.report` に並べるもの）。"""
115 |     P_ = T3['pilot']
116 |     L = ['', '**%s**' % title, '']
117 |     if rec.get('tool_error'):
118 |         return L + machine(['- 器の誤り: %s' % rec['tool_error']], MB)
119 |     rows = ['- 出口の値の自己検査（下見の頭）: 差の最大 %s（許容 %s）・%s' % (f4(rec['logit_check']['max_abs']), f4(rec['logit_check']['tol']), '通った' if rec['logit_check']['pass'] else '落ちた')]
120 |     vi = rec['vi']
121 |     rows.append('- (vi) (a) バッチの違いの揺れ（升目の間の最大）%s・(b) バッチ一の繰り返しの揺れ（升目の間の最大）%s・上限 %s' % (
122 |         f4(vi['decision']['spread_a']), f4(vi['decision']['spread_b']), f4(P_['noise_max'])))
123 |     rows += ['  - %s: (a) %s・(b) %s' % (k, f4(vi['a'][k]), f4(vi['b'][k])) for k in vi['a']]
124 |     dec = rec.get('decision') or {}
125 |     if dec.get('stop') and dec.get('reason') == 'vi_b':
126 |         rows.append('- (vi) の (b) で止めたので、(i)〜(v) は計算していない（正本 pilot.order）')
127 |         return L + machine(rows, MB)
128 |     rows.append('- バッチの大きさ %s・揺れの床 %s・近道の許容 %s' % (rec.get('batch'), f4(rec.get('floor')), f4(rec.get('cache_tol'))))
129 |     rows += ['- 変換の後の確率の定義（正本）: %s' % T3['pilot']['checks']['iii']['transformed_def'], '- 全語彙（正本）: %s' % T3['pilot']['checks']['i']['full_vocab']]
130 |     rows += ['', '| 升目 | 主の升目 | 無操作の対数オッズ | 選択肢 a の確率（集合の中） | 変換の後の確率 | 質量 | 段階 B の無操作の破局の率 | (i)(ii) |', '|---|---|---|---|---|---|---|---|']
131 |     for k, c in rec['cells'].items():
132 |         why = [] if c['pass_i_ii'] else [w for w, bad in (('質量が下限の下', c['mass'] < P_['mass_min']), ('確率が床か天井の外', not (P_['p_bounds'][0] <= c['pa'] <= P_['p_bounds'][1]))) if bad]
133 |         rows.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (k, yn(c['main']), f4(c['lo']), f4(c['pa']), f4(c.get('pa_transformed')), f4(c['mass']), f4(c.get('stage_b_rate')),
134 |                                                               '満たす' if c['pass_i_ii'] else '満たさない（%s）' % '・'.join(why)))
135 |     rows += ['', '- (iii) 較正（記述）: 順位相関 %s・升目 %s・文: %s' % (f4(rec['iii']['rho']), rec['iii']['n'], T3['pilot']['iii_sentences'][rec['iii']['sentence']])]
136 |     for name, v in (rec.get('iv') or {}).items():
137 |         rows.append('- (iv) 揺れの版 %s: %s' % (name, '・'.join('%s %s（主との差 %s%s）' % (c, f4(x), f4(x - rec['cells'][c]['lo']), '・印' if v['flags'][c] else '') for c, x in v['lo'].items())))
138 |     rows.append('- (v) 近道の差（無操作の対数オッズの差・記述・本の計算は近道を使わない・裁定 D234）: %s・近道の許容 %s・差がすべて許容の内: %s' % (
139 |         '・'.join('%s %s' % (c, f4(d)) for c, d in rec['v']['diffs'].items()), f4(rec['v']['tol']), yn(rec['v']['shortcut'])))
140 |     rows.append('- 機械の決定: %s・(i)(ii) を満たす主の升目 %s／%s・外した升目: %s' % (dec.get('q1'), dec.get('n_pass'), dec.get('n_main'), '・'.join(dec.get('dropped') or []) or 'なし'))
141 |     fam = [k for k in (dec.get('dropped') or []) if k.startswith('N1|')]
142 |     if len(fam) >= 2:
143 |         rows.append('- nuclear の族は測れなかった（正本 pilot.decision.family）')
144 |     return L + machine(rows, MB)
145 | 
146 | 
147 | def outcomes(A):
148 |     return dict(A['predictions_truth'])
149 | 
150 | 
151 | def build(T3, A, preds, meta, deviations=(), marks=None, rejected=None, confirmation=None, main_tool_error=False):
152 |     MB = RL.machine_block(T3)
153 |     marks = marks or {}
154 |     mk = lambda s: machine(['- 逸脱の印: %s' % '・'.join(marks[s])], MB) if marks.get(s) else []
155 |     L = ['# B-lens 層三の結果（報告の草案・機械の組み立て）', '']
156 |     if confirmation:
157 |         st = '- 状態: **最終版**（登録者最終確認 %s 日本時間・会話の記録 uuid `%s`・逐語「%s」）。' % (confirmation['when_jst'], confirmation['uuid'], confirmation['words'])
158 |     else:
159 |         st = '- 状態: **報告の草案（結果の巡の前）**。'
160 |     L += machine([st, '- 起草: 南無弥勒如来（コーディネータ）／登録者: 楠見優太。組み立ての器: `tools/build_report_Bl3.py` %s。' % VERSION,
161 |                   '- 正本 `design/contrasts-Bl3.json` SHA16 %s・凍結の記録 SHA16 %s・封印の記録 SHA16 %s・集計の出力 SHA16 %s。' % (meta['canon'], meta['freeze'], meta['seal'], meta['analysis'])], MB)
162 |     L += ['', '- 位置づけ: 段階 B と B-lens の後の登録（B-lens 層三）。段階 B と B-lens の札・報告・逸脱台帳には触れない。', '- 封印の前の露出の記録: `records/Bl3/exposure-before-seal-Bl3.md`。', '']
163 |     L += ['## 凍結の後の逸脱', ''] + machine(['- 【逸脱 %s】%s（%s）' % (d.get('no'), d.get('what'), d.get('date')) for d in deviations] or ['- 無し'], MB)
164 |     atts = A['pilot_attempts']
165 |     if len(atts) > 1:
166 |         L += ['', '## 一度目の下見の記録（やり直した下見の前・裁定 D222）']
167 |         for i, rec in enumerate(atts[:-1], start=1):
168 |             L += pilot_lines(T3, rec, MB, '試み %d の下見の記録と機械の決定' % i)
169 |     stopped = A['predictions_meta']['stopped']
170 |     # 0. 要約
171 |     L += ['', '## 0. 要約（できないことから）', ''] + mk('summary')
172 |     L += ['**見ていない場所**（正本の「この登録で答えられないこと」）:', ''] + machine(['- ' + x for x in T3['scope']['not_answered']], MB)
173 |     L += ['', '**この結果が退けた説明**:', '', '- ' + (rejected.strip() if rejected else REJECTED_BLANK)]
174 |     L += ['', '**答えの範囲**:', ''] + machine(['- ' + T3['scope']['reach'], '- ' + T3['negation_templates'][2]], MB)
175 |     last = atts[-1]
176 |     dec = last.get('decision') or {}
177 |     md_, gd_ = dropped_split(T3, dec)
178 |     L += ['', '**下見の機械の決定**:', ''] + machine(['- %s' % ('器の誤りで下見を終えられなかった' if last.get('tool_error') else '%s（外した主の升目: %s）' % (dec.get('q1'), '・'.join(md_) or 'なし'))]
179 |                                                     + (['- 門の行だけの升目を外した: %s（門の行と入れ替えの数を数え直した・主の札の行は外していない・正本 pilot.decision.gate_only）' % '・'.join(gd_)] if gd_ and not last.get('tool_error') else [])
180 |                                                     + (['- nuclear の族は測れなかった（正本 pilot.decision.family）'] if len([k for k in md_ if k.startswith('N1|')]) >= 2 else [])
181 |                                                     + ([] if last.get('tool_error') or (dec.get('stop') and dec.get('reason') == 'vi_b') else
182 |                                                        ['- (iii) の文: ' + T3['pilot']['iii_sentences'][last['iii']['sentence']]]), MB)
183 |     if main_tool_error:
184 |         L += ['', '**本の計算**:', ''] + machine(['- 器の誤りで計算を終えられなかった（正本 computation.tool_error・予想は q1 だけを採点する）'], MB)
185 |     if not stopped and not main_tool_error:
186 |         rows = A['rows']
187 |         cnt = lambda d: sum(1 for o in rows.values() if o['direction'] == d and o['iso_outside'])
188 |         G = A['gates']
189 |         gtxt = lambda g: '判定不能' if g.get('undetermined') else ('通った' if g['pass'] else '通らない')
190 |         rc = A.get('recompute') or {}
191 |         L += ['', '**主の記述の札と門**（機械の出力）:', ''] + machine([
192 |             '- 主の行 %d（下見で外した後）・等方の外の行: v̂ %d・Nk %d・二つ目の札が付く行 %d' % (A['rows_meta']['m_rows'], cnt('static'), cnt('Nk'), sum(1 for o in rows.values() if o['second']['top'])),
193 |             '- 本の門: %s・v̂ を抜いた門: %s' % (gtxt(G['main']), gtxt(G['without_vhat'])),
194 |             '- 独立の再計算: 一段目（無操作の値と効き目の値と札） %s・二段目（札の一致・裁定 D234） %s%s' % (
195 |                 ('一致' if (rc.get('first') or {}).get('agree') else '不一致') if rc.get('first') else '無い', '一致' if (rc.get('second') or {}).get('agree') else '不一致',
196 |                 '（二段目の効き目の差の最大は許容の外・札は同じで、台帳に記した）' if (rc.get('second') or {}).get('values_beyond_tol') and (rc.get('second') or {}).get('agree') else '')], MB)
197 |     L += ['', '**読みの型**（正本の読みの表の条件を器が当てた・型は重なりうる）:', ''] + machine(['- 〈%s〉（%s）: %s' % h for h in reading_types(T3, A)] if not main_tool_error else ['- 〈器の誤り〉（本の計算）: 器の誤りで計算を終えられなかった'], MB)
198 |     L += ['', '**打ち消しの定型**:', ''] + machine(['- ' + x for x in T3['negation_templates']], MB)
199 |     # 1. 下見の記録
200 |     L += ['', '## 1. 下見の記録（本の凍結で凍結した・無操作だけ）'] + mk('pilot')
201 |     L += pilot_lines(T3, last, MB, '下見の記録と機械の決定（主の札の隣に並べる）')
202 |     if not stopped and not main_tool_error:
203 |         L += main_sections(T3, A, MB, mk)
204 |     # 6. 予想の照合
205 |     L += ['', '## 6. 予想の照合（記録であり評価ではない）', ''] + mk('predictions')
206 |     L += ['- 的中は誰の判断の重みも変えない。照合は記録であり評価ではない。', '']
207 |     oc = outcomes(A)
208 |     items = [it['key'] for it in T3['predictions']['items']]
209 |     rows = ['| 項目 | 結果 | 登録者 | コーディネータ |', '|---|---|---|---|']
210 |     for k in items:
211 |         res = oc.get(k)
212 |         cell = lambda who: '%s（%s）' % (preds[who].get(k, '—'), '予想しない' if preds[who].get(k) == '予想しない' else ('採点しない' if res is None else ('一致' if preds[who].get(k) == res else '不一致')))
213 |         rows.append('| %s | %s | %s | %s |' % (k, '採点しない' if res is None else res, cell('registrant'), cell('coordinator')))
214 |     notes = []
215 |     if stopped:
216 |         notes.append('- ' + T3['predictions']['if_stopped'])
217 |     if main_tool_error:
218 |         notes.append('- 器の誤りで計算を終えられなかったので、q1 だけを採点する（正本 computation.tool_error）')
219 |     L += machine(rows + notes, MB)
220 |     # 7. 限界
221 |     L += ['', '## 7. 限界（正本の限界の文）', ''] + mk('limits') + machine(['- ' + x for x in T3['limits']], MB)
222 |     L += ['', '## 検分票', '', '- 対象: 本報告の草案（機械の組み立ての出力と、起草者の欄）。', '- 段階: 結果の後（封印の後・凍結した器で計算した）。',
223 |           '- 本検分が確認していないこと: 読みの型の当否と起草者の欄の文は、結果の巡で見る。', '', FENCE, '']
224 |     return NL.join(L)
225 | 
226 | 
227 | def main_sections(T3, A, MB, mk):
228 |     L = []
229 |     rows = A['rows']
230 |     notes = A.get('stage_b_notes') or {'main': {}, 'gate': {}}
231 |     # 2. 主の札
232 |     L += ['', '## 2. 主の札（等方の帰無・実在の差の方向）', ''] + mk('main')
233 |     t = ['| 行 | 方向 | 升目と符号 | 効き目 | p | 上の裾 | 下の裾 | 割合を決めた裾 | Holm の段 | 等方の外 | 等方の中央値 | 効き目の側 | 二つ目の札（中心・最上位・順位 向き／対） | 等方の最上位の割合 | 段階 B の札と注 |',
234 |          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
235 |     for rid, o in rows.items():
236 |         s = o['second']
237 |         nb = notes['main'].get(rid) or {}
238 |         nb_txt = '・'.join([x for x in [nb.get('label')] if x] + list(nb.get('notes') or []) + (['様式の保留'] if nb.get('style_hold') else [])) or 'なし'
239 |         t.append('| %s | %s | %s | %s | %s | %d | %d | %s | %s | %s | %s | %s | %s・%s・%d／%d・%d／%d | %s | %s |' % (
240 |             rid, o['direction'], o['cell_sign'], f4(o['effect']), f4(o['p']), o['upper'], o['lower'], {'upper': '上', 'lower': '下'}.get(o['tail'], o['tail']), f4(o['holm_step']),
241 |             yn(o['iso_outside']), f4(o['iso_median']), side_text(T3, o['side']), f4(s['center']), yn(s['top']), s['rank_oriented'], s['of_oriented'], s['rank_pair'], s['of_pair'],
242 |             f4(o['iso_top_share']), nb_txt.replace('|', '｜')))
243 |     meta = A['rows_meta']
244 |     t += ['', '- Holm の段の数（下見で外した後の主の行の数）%d・外した行: %s' % (meta['m_rows'], '・'.join(meta['dropped_rows']) or 'なし'),
245 |           '- 二つ目の札の偶然の目安（Holm を掛けない・下見で外した後の行で数えた）: 向きまで数えて %s・対の単位で %s（行の数 %s・外す前の全ての行では %s と %s）。%s' % (
246 |               f4(A['chance']['oriented']), f4(A['chance']['pair']), '・'.join('%s %d' % kv for kv in sorted((A['chance'].get('rows_by_direction') or {}).items())),
247 |               f4((A['chance'].get('canon_all_rows') or {}).get('oriented')), f4((A['chance'].get('canon_all_rows') or {}).get('pair')), T3['nulls']['real']['chance_note']),
248 |           '- 両方の札が付いたときの言い方（正本）: %s' % T3['labels']['print_rule']]
249 |     L += machine(t, MB)
250 |     D = A['descriptive']
251 |     L += ['', '**升目と符号ごとの無操作の選択肢 a の文字の確率と質量**（主の札の隣に並べる）:', '']
252 |     L += machine(['- 報告の雛形の決まり（裁定 D223）: 升目ごとの無操作の選択肢 a の文字の確率を、主の札の隣に並べる', '| 升目と符号 | 無操作の選択肢 a の確率（選択の文字と refuse の頭の中） | 質量が下限を下回った方向の数 |', '|---|---|---|'] +
253 |                  ['| %s | %s | %d |' % (k, f4(D['pa_noop'][k]), D['mass_below_min'][k]) for k in D['pa_noop']] + ['- ' + T3['descriptive']['mass']], MB)
254 |     # 3. 門
255 |     G = A['gates']
256 |     L += ['', '## 3. 門（段階 B の方向ごとの行動と、方向の単位で）', ''] + mk('gate')
257 |     g = ['| 門 | 行 | 入れ替える単位 | 入れ替えの数 | 順位相関 | p | 通る |', '|---|---|---|---|---|---|---|']
258 |     for name, lab in (('main', '本の門'), ('without_vhat', 'v̂ を抜いた門'), ('desc_without_vhat_loaded', '記述: v̂ と (6b) を抜いた門'), ('desc_choice_a', '記述: 選択 a の件数を行動の量にした門'),
259 |                       ('desc_without_style', '記述: 様式の転位の行を除いた門')):
260 |         x = G[name]
261 |         if x.get('undetermined'):
262 |             g.append('| %s | %d | %s | なし | なし | なし | 判定不能 |' % (lab, x['n_rows'], '・'.join(x['units'])))
263 |         else:
264 |             g.append('| %s | %d | %s | %d | %s | %s | %s |' % (lab, x['n_rows'], '・'.join(x['units']), x['n_perm'], f4(x['rho']), f4(x['p']), ('はい' if x['pass'] else 'いいえ') if not name.startswith('desc_') else '記述（型を当てない）'))
265 |     g += ['- 門が通る条件: p が水準（%s）を下回るとき。%s' % (f4(T3['gate']['alpha']), T3['gate']['power_note']), '- ' + T3['gate']['descriptive_rule'],
266 |           '- 様式の転位の行（除いた行）: %s' % ('・'.join(br(x) for x in (A.get('style_rows') or [])) or 'なし')]
267 |     gn = [(n, v) for n, v in (notes.get('gate') or {}).items() if v]
268 |     g += ['- 段階 B の注のある門の行: %s' % ('・'.join('%s［%s］' % (br(n), '・'.join('%s%s' % (x['kind'], ('（三本の率の差 %s pt・門 %s pt 超）' % (f4(x['spread_pt']), f4(x['threshold_pt']))) if 'spread_pt' in x else '') for x in v)) for n, v in gn) or 'なし')]
269 |     L += machine(g, MB)
270 |     # 4. 記述
271 |     H = A['head']
272 |     L += ['', '## 4. 記述（札を付けない）', ''] + mk('descriptive')
273 |     d = ['- 本の計算の頭の自己検査: 出口の値 差の最大 %s（許容 %s）・最後の層 差 %s（許容 %s）' % (f4(H['logit_check']['max_abs']), f4(H['logit_check']['tol']), f4(H['layer_check']['diff']), f4(H['layer_check']['tol']))]
274 |     sc = H.get('steered_cache_check')
275 |     d.append('- 本の計算の頭の近道の確かめ: %s・本の計算の近道: %s・バッチの大きさ %s' % (
276 |         ('二つの道の効き目の差の最大 %s（許容 %s）' % (f4(sc['max_abs']), f4(sc['tol']))) if sc else '走らせていない（本の計算は近道を使わない・裁定 D234）', yn(A['main_run']['shortcut']), A['main_run']['batch']))
277 |     d += ['- 層ごとの差分: 値は集計の出力の `layerwise` に置いた（名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間）。' + T3['descriptive']['layerwise']['note_no_reading'],
278 |           '- ' + T3['descriptive']['others']]
279 |     L += machine(d, MB)
280 |     S2 = A.get('secondary')
281 |     if S2:
282 |         s = ['', '**乙**（B-lens の層二の文脈・門の行の符号・裁定 D227）: 順伝播 %s・文脈 %s（流した文脈 %s）' % (S2['counts']['row_passes'], S2['counts']['contexts'], S2['contexts_run']), '',
283 |              '| 行 | 文脈の数 | 対数オッズの変化 中央値［四分位］ | a の出口の値の変化 中央値 | c の出口の値の変化 中央値 | B-lens の直接の経路 a（中央値） | B-lens の直接の経路 c（中央値） |', '|---|---|---|---|---|---|---|']
284 |         for name, v in S2['summary'].items():
285 |             bl = v.get('blens_direct') or {}
286 |             s.append('| %s | %d | %s［%s, %s］ | %s | %s | %s | %s |' % (br(name).replace('|', '｜'), v['dlo']['n'], f4(v['dlo']['median']), f4(v['dlo']['q1']), f4(v['dlo']['q3']), f4(v['dz_a']['median']),
287 |                                                               f4(v['dz_c']['median']), f4((bl.get('dlogit_exact_a') or {}).get('median')), f4((bl.get('dlogit_exact_c') or {}).get('median'))))
288 |         s += ['- ' + T3['readout']['secondary']['note'], '- ' + T3['descriptive']['secondary_readout']]
289 |         L += machine(s[1:], MB)
290 |     # 5. 独立の再計算
291 |     rc = A.get('recompute') or {}
292 |     L += ['', '## 5. 独立の再計算（二段）', ''] + mk('recompute')
293 |     r = []
294 |     for st, lab in (('first', '一段目（本の器のフック と 残差の書き換え・無操作の値と効き目の値と札で判定・裁定 D233）'), ('second', '二段目（本の道 と 本の器のフック・札の一致で判定・裁定 D234）')):
295 |         x = rc.get(st)
296 |         tol = rc.get('tol_first') if st == 'first' else rc.get('tol_second')
297 |         what = '無操作の値と効き目の差の最大' if st == 'first' else '効き目の差の最大（記録）'
298 |         r.append('- %s: %s' % (lab, ('%s・%s %s（許容 %s・許容の%s）・札 %s' % ('一致' if x['agree'] else '不一致', what, f4(x['max_abs_diff']), f4(tol), '内' if x['values_within_tol'] else '外',
299 |                                                                        '同じ' if x['labels_same'] else '違う')) if x else '無い'))
300 |     if (rc.get('second') or {}).get('values_beyond_tol') and (rc.get('second') or {}).get('agree'):
301 |         r.append('- 二段目は効き目の差の最大が許容の外で、札は同じだった。止めずに逸脱の台帳に記した（正本 `independent_recompute.agreement`・裁定 D234）')
302 |     r.append('- 組の間の環境: %s' % ('同じ' if (A.get('env') or {}).get('same') else '違う（%s）' % json.dumps((A.get('env') or {}).get('diff'), ensure_ascii=False)))
303 |     if 'pilot_gpu' in (A.get('env') or {}):
304 |         r.append('- 下見の GPU: %s・本の計算の組の GPU と同じ: %s（揺れの床は下見の GPU で決まる・裁定 D236）' % ('・'.join(A['env']['pilot_gpu']), yn(A['env'].get('gpu_same_as_pilot'))))
305 |     L += machine(r, MB)
306 |     return L
307 | 
308 | 
309 | def lint_report(text, T3):
310 |     T_scan = json.loads(json.dumps(T3))
311 |     ban = list(T_scan['print_strings']['mechanism_word_ban'])
312 |     for w in list(T3['print_strings']['added_ban']) + list(T3['print_strings']['reading_never_ban']):
313 |         if w not in ban:
314 |             ban.append(w)
315 |     T_scan['print_strings']['mechanism_word_ban'] = ban
316 |     side = {'blocks': RL.block_hashes(text, T3)}
317 |     return RL.lint(text, T_scan, frozenset(), sidecar=side), side
318 | 
319 | 
320 | def sealed_and_frozen_bad(FR, seal):
321 |     """報告を組む前の確かめ（裁定 D236・B-lens の `require_sealed` の型）: 二つの予想の SHA-256 が封印の記録と同じ・封印の記録の SHA16 と二つの予想の SHA-256 が
322 |     本の凍結の記録に写した値と同じ・手元の器と正本と設計事実と方向の記録が本の凍結の記録と同じ（台帳に記した差分は許す）。戻り値: 外れの並び。"""
323 |     import analyze_Bl3 as AZ
324 |     bad = []
325 |     for role, v in seal['predictions'].items():
326 |         pp = P(v['path'])
327 |         if not os.path.exists(pp) or hashlib.sha256(open(pp, 'rb').read()).hexdigest().upper() != v['sha256']:
328 |             bad.append('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
329 |     ms = (FR.get('main_freeze') or {}).get('seal') or {}
330 |     if ms.get('record_sha16') != sha16f(P('records/Bl3/sealing-record-Bl3.json')):
331 |         bad.append('封印の記録の SHA16 が、本の凍結の記録に写した値と違う')
332 |     if any((ms.get('predictions_sha256') or {}).get(r) != v['sha256'] for r, v in seal['predictions'].items()):
333 |         bad.append('本の凍結の記録に写した予想の SHA-256 が、封印の記録と違う')
334 |     bad += ['手元の器か正本が本の凍結の記録と違う: %s' % x for x in AZ.frozen_versions_bad(FR, REPO)]
335 |     return bad
336 | 
337 | 
338 | def load_inputs(main_tool_error=False):
339 |     import sweep_Bl3 as SW
340 |     T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
341 |     FR = json.load(open(P('records/Bl3/FREEZE-RECORD-Bl3.json'), encoding='utf-8'))
342 |     seal = json.load(open(P('records/Bl3/sealing-record-Bl3.json'), encoding='utf-8'))
343 |     bad = sealed_and_frozen_bad(FR, seal)
344 |     if bad:
345 |         raise SystemExit('報告を組む前の確かめが外れた（止める・登録者に相談）: %s' % bad)
346 |     preds = {r: json.load(open(P(v['path']), encoding='utf-8')) for r, v in seal['predictions'].items()}
347 |     ap_ = P('records/Bl3/analysis-Bl3.json')
348 |     atts = FR['main_freeze']['pilot_attempts']
349 |     if os.path.exists(ap_):
350 |         A = json.load(open(ap_, encoding='utf-8'))
351 |         miss = SW.sweep(T3, A)
352 |         if miss:
353 |             raise SystemExit('掃き出し: 集計の出力に、正本と凍結の本文が求める出力の欠けがある（止める）: %s' % miss)
354 |     else:
355 |         last = atts[-1]
356 |         if not (last.get('tool_error') or (last.get('decision') or {}).get('stop') or main_tool_error):
357 |             raise SystemExit('集計の出力が無い（下見で止まったときと器の誤りのときだけ、集計の出力なしに組む）')
358 |         import analyze_Bl3 as AZ
359 |         truth, tmeta = AZ.prediction_truth(T3, atts, {}, {'main': {'undetermined': True}, 'without_vhat': {'undetermined': True}}, [], 0.0)
360 |         if main_tool_error:
361 |             truth = collections.OrderedDict((k, v if k == 'q1.pilot' else None) for k, v in truth.items())
362 |         A = {'pilot_attempts': atts, 'predictions_truth': truth, 'predictions_meta': dict(tmeta, stopped=tmeta['stopped'] and not main_tool_error)}
363 |     meta = {'canon': sha16f(P('design/contrasts-Bl3.json')), 'freeze': sha16f(P('records/Bl3/FREEZE-RECORD-Bl3.json')), 'seal': sha16f(P('records/Bl3/sealing-record-Bl3.json')),
364 |             'analysis': sha16f(ap_) if os.path.exists(ap_) else 'なし'}
365 |     fc = P('records/Bl3/final-confirmation-Bl3.json')
366 |     confirmation = json.load(open(fc, encoding='utf-8')) if os.path.exists(fc) else None
367 |     return T3, FR, A, preds, meta, confirmation
368 | 
369 | 
370 | def main():
371 |     ap = argparse.ArgumentParser()
372 |     ap.add_argument('--force', action='store_true')
373 |     ap.add_argument('--selftest', action='store_true')
374 |     ap.add_argument('--rejected', help='「この結果が退けた説明」の起草者の行（md・数を打たない）')
375 |     ap.add_argument('--marks', help='逸脱の印の JSON（節の鍵 → 逸脱の番号の並び・節の鍵は %s）' % '・'.join(SECTIONS))
376 |     ap.add_argument('--main-tool-error', action='store_true', help='本の計算が器の誤りで終えられず、やり直さないと登録者が裁定したとき')
377 |     a = ap.parse_args()
378 |     if a.selftest:
379 |         return _selftest()
380 |     if os.path.exists(OUT) and not a.force:
381 |         raise SystemExit('既にある: %s' % OUT)
382 |     T3, FR, A, preds, meta, confirmation = load_inputs(a.main_tool_error)
383 |     marks = json.load(open(a.marks, encoding='utf-8')) if a.marks else None
384 |     if marks and any(k not in SECTIONS for k in marks):
385 |         raise SystemExit('印の節の鍵が違う: %s' % [k for k in marks if k not in SECTIONS])
386 |     rejected = open(a.rejected, encoding='utf-8').read() if a.rejected else None
387 |     text = build(T3, A, preds, meta, FR.get('deviations') or [], marks, rejected, confirmation, a.main_tool_error)
388 |     V, side = lint_report(text, T3)
389 |     open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
390 |     RL.write_sidecar(OUT, text, T3, 'tools/build_report_Bl3.py %s' % VERSION)
391 |     lint_path = OUT.replace('.md', '-lint.md')
392 |     open(lint_path, 'w', encoding='utf-8', newline=NL).write(NL.join(['# 報告の走査（凍結した `tools/report_lint.py` の lint・禁止語は正本の四つの一覧の和）', '', '- 違反 %d' % len(V)] +
393 |                                                                   ['- %s（%s 行目）: %s' % (v['kind'], v['line'], v['token']) for v in V] + ['', FENCE, '']))
394 |     print('wrote %s（走査の違反 %d）' % (os.path.relpath(OUT, REPO), len(V)))
395 |     if V:
396 |         raise SystemExit('報告の走査に違反がある（非零で終わる）')
397 | 
398 | 
399 | def synth_analysis(T3, FJ, DJ, seed=3, n_iso=199, stop=None, drop=()):
400 |     """合成の集計の出力（模型を読まない・乱数の効き目・自己検査だけに使う）。"""
401 |     import numpy as np
402 |     import bl3_core as K
403 |     import bl3_run as BR
404 |     import analyze_Bl3 as AZ
405 |     rng = np.random.default_rng(seed)
406 |     T3x = AZ.with_iso(T3, n_iso)
407 |     names = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])], 'iso': ['iso:%d' % i for i in range(n_iso)],
408 |              'real': ['real:' + p for p in DJ['groups']['real']['names']]}
409 |     gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
410 |     sets = BR.cell_sign_sets(T3, None, names['named'], names['B_random'], names['iso'], names['real'], gate_only)
411 |     cells_out = collections.OrderedDict()
412 |     for key, ck, sg, ds in sets:
413 |         if ck in set(drop):
414 |             continue                                   # 本の計算は下見で外した升目の組を流さない（本の器と同じ形・裁定 D231）
415 |         eff = {d: float(rng.normal(loc=0.3 * sg, scale=0.5)) for d in ds}
416 |         eff['static'] = eff.get('static', 0.0) + 2.5 * sg if 'static' in eff else eff.get('static')
417 |         eff = {k: v for k, v in eff.items() if v is not None}
418 |         cells_out[key] = {'effects': eff, 'mass': {d: 0.95 for d in ds}, 'pa_noop': float(rng.uniform(0.01, 0.2)), 'lo': dict(eff, **{K.NOOP: -2.0})}
419 |     cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
420 |     pilot = {'logit_check': {'max_abs': 0.05, 'tol': 0.5, 'pass': True},
421 |              'vi': {'a': {k: 1e-3 for k in cell_keys}, 'b': {k: 0.0 for k in cell_keys}, 'decision': {'stop': stop == 'vi_b', 'batch': 16, 'floor': 1e-3, 'spread_a': 1e-3, 'spread_b': 0.02 if stop == 'vi_b' else 0.0}},
422 |              'batch': 16, 'floor': 1e-3, 'cache_tol': 0.005,
423 |              'cells': {k: {'lo': -2.0, 'pa': 0.1, 'mass': 0.95, 'pa_transformed': 0.05, 'stage_b_rate': 0.2, 'pass_i_ii': k not in drop, 'main': True} for k in cell_keys},
424 |              'iii': {'rho': 0.3, 'n': len(cell_keys), 'sentence': 'positive'}, 'iv': {'V1': {'lo': {k: -1.9 for k in cell_keys}, 'flags': {k: False for k in cell_keys}}},
425 |              'v': {'diffs': {k: 1e-4 for k in cell_keys}, 'tol': 0.005, 'shortcut': True},
426 |              'decision': K.cells_decision({k: k not in drop for k in cell_keys}, {g: g not in drop for g in sorted({'%s|%s' % (x[0], x[1]) for x in gate_only})},
427 |                                           T3['pilot']['decision']['cells_min_pass'])}
428 |     if stop == 'vi_b':
429 |         pilot['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
430 |         for k in ('iii', 'iv', 'v', 'cells'):
431 |             pilot.pop(k)
432 |     AN = json.load(open(P('records/B/analysis-B-2026-09-22.json'), encoding='utf-8'))
433 |     rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
434 |     style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
435 |     if pilot['decision'].get('stop'):
436 |         truth, tmeta = AZ.prediction_truth(T3, [pilot], {}, {'main': {'undetermined': True}, 'without_vhat': {'undetermined': True}}, [], 0.0)
437 |         return {'pilot_attempts': [pilot], 'predictions_truth': truth, 'predictions_meta': tmeta}
438 |     rows_rc, dbr = K.recompute_set(T3['main_rows'], DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'], n_iso, pilot['decision']['dropped'])
439 |     ek = lambda did, sg: did if did.startswith(('static', 'iso:', 'real:')) else did
440 |     hook = {}
441 |     for nm, ck, s in rows_rc:
442 |         E = {}
443 |         for did, sg in dbr[nm]:
444 |             E['%s|%+d' % (did, sg)] = cells_out['%s|%+d' % (ck, sg)]['effects'][did]
445 |         hook[nm] = {'noop_lo': -2.0, 'effects': E}
446 |     A = AZ.analyze(T3x, FJ, cells_out, [pilot], DJ['groups']['real']['names'], rows_gate, hook=hook, rewrite=hook, style_rows=style_rows)
447 |     A = json.loads(json.dumps(A, default=lambda o: o.item() if hasattr(o, 'item') else float(o)))
448 |     main_keys = {'%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']}
449 |     A.update({'dry': True, 'pilot_attempts': [pilot], 'head': {'logit_check': {'max_abs': 0.05, 'tol': 0.5, 'pass': True},
450 |                                                                'shortcut': False, 'layer_check': {'diff': 0.0, 'tol': 1e-4, 'pass': True}},
451 |               'main_run': {'batch': 16, 'shortcut': False, 'dropped': pilot['decision']['dropped']},
452 |               'layerwise': {k: {'noop_lo': {'2': -2.0, '3': -2.0}, 'rows': {u: [[1.0, 0.9, 0.1], [1.1, 0.8, 0.1]] for u in list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]},
453 |                                 'iso_summary': {'median': [[1.0, 0.0, 0.0]] * 2, 'lo': [[0.5, -0.1, -0.1]] * 2, 'hi': [[1.5, 0.1, 0.1]] * 2, 'n': n_iso}} for k in cells_out if k in main_keys},
454 |               'n_iso': n_iso,
455 |               'gate_rows': [], 'style_rows': style_rows, 'stage_b_notes': AZ.stage_b_notes(T3, AN, rows_gate),
456 |               'secondary': {'counts': {'row_passes': 1, 'sign_batches': 1, 'contexts': 1}, 'contexts_run': 1,
457 |                             'summary': {'S1|O-Ncold-v|static': dict({k: {'mean': 0.1, 'median': 0.1, 'q1': 0.0, 'q3': 0.2, 'n': 20} for k in ('dlo', 'dz_a', 'dz_c')},
458 |                                                                      blens_direct={k: {'mean': x, 'median': x, 'q1': x, 'q3': x} for k, x in (('dlogit_exact_a', 0.1), ('dlogit_exact_c', -0.1))})}},     # B-lens の層二の値と同じ形（文脈の間の要約）
459 |               'sessions': {}, 'env': {'same': True, 'diff': {}, 'strict': [], 'pilot_gpu': ['NVIDIA L4'], 'gpu_same_as_pilot': True}})
460 |     return A
461 | 
462 | 
463 | def _selftest():
464 |     """合成の集計の出力で報告を組み、走査が通ること（起草者の欄を埋めたとき）・欄が空なら埋め残しで止まること・禁止語と未登録の数を入れた報告が止まること・
465 |     掃き出しが欠けを捕まえること・下見で止まったときと升目を外したときの組み立てを確かめる。"""
466 |     import sweep_Bl3 as SW
467 |     T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
468 |     FJ = json.load(open(P('records/Bl3/design-facts-Bl3.json'), encoding='utf-8'))
469 |     DJ = json.load(open(P('results/Bl3/directions-Bl3.json'), encoding='utf-8'))
470 |     preds = {'registrant': {'q1.pilot': '続ける', 'q4.gate': '通らない'}, 'coordinator': {'q1.pilot': '止める', 'q2.vhat_iso': '零'}}
471 |     meta = {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}
472 |     A = synth_analysis(T3, FJ, DJ)
473 |     miss = SW.sweep(T3, A)
474 |     assert miss == [], miss
475 |     A2 = json.loads(json.dumps(A))
476 |     A2['rows'][next(iter(A2['rows']))].pop('iso_top_share')
477 |     assert SW.sweep(T3, A2), '掃き出しが欠けを捕まえない'
478 |     text = build(T3, A, preds, meta, [{'no': 'D-BL3-X', 'what': '合成の逸脱', 'date': '2026-09-26'}], {'main': ['D-BL3-X']}, '起草者の行（合成）')
479 |     V, side = lint_report(text, T3)
480 |     assert V == [], V[:5]
481 |     t0 = build(T3, A, preds, meta)
482 |     V0, _ = lint_report(t0, T3)
483 |     assert any(v['kind'] == '埋め残し' for v in V0), V0[:3]
484 |     for bad_line, kind in (('（効いた）', '価値語'), ('（v̂ に特有）', None), (' 12 件', '未登録の数')):
485 |         bad = text.replace('## 7. 限界', '## 7. 限界' + bad_line, 1)
486 |         Vb, _ = lint_report(bad, T3)
487 |         assert Vb and (kind is None or any(v['kind'] == kind for v in Vb)), (bad_line, Vb[:3])
488 |     As = synth_analysis(T3, FJ, DJ, stop='vi_b')
489 |     ts = build(T3, As, preds, meta, rejected='起草者の行（合成）')
490 |     Vs, _ = lint_report(ts, T3)
491 |     assert Vs == [] and '数値が定まらず測れなかった' in ts and '## 2. 主の札' not in ts, Vs[:3]
492 |     Ad = synth_analysis(T3, FJ, DJ, drop=('N1|O-Ncold',))
493 |     td = build(T3, Ad, preds, meta, rejected='起草者の行（合成）')
494 |     Vd, _ = lint_report(td, T3)
495 |     assert Vd == [] and '〈下見で一部を外した〉' in td and Ad['rows_meta']['m_rows'] < len(T3['main_rows']), Vd[:3]
496 |     # 門の行だけの升目だけを外したとき: 〈下見で一部を外した〉は当たらず、§0 に門の行だけの升目の外しの行が出る（裁定 D236）
497 |     go_ = sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
498 |     Ag = synth_analysis(T3, FJ, DJ, drop=tuple(go_))
499 |     tg = build(T3, Ag, preds, meta, rejected='起草者の行（合成）')
500 |     Vg, _ = lint_report(tg, T3)
501 |     assert Vg == [] and '〈下見で一部を外した〉' not in tg and '門の行だけの升目を外した' in tg and SW.sweep(T3, Ag) == [], Vg[:3]
502 |     # 等方の外の行が出る枝（等方を正本の本数に・裁定 D236・器の実装の検分の R1-m5）: 掃き出し・走査・読みの型・q7
503 |     Ao = synth_analysis(T3, FJ, DJ, n_iso=T3['nulls']['isotropic']['count'])
504 |     to_ = build(T3, Ao, preds, meta, rejected='起草者の行（合成）')
505 |     Vo, _ = lint_report(to_, T3)
506 |     n_out = sum(1 for o in Ao['rows'].values() if o['iso_outside'])
507 |     assert n_out > 0 and Vo == [] and SW.sweep(T3, Ao) == [] and ('〈両方の外〉' in to_ or '〈埋もれる〉' in to_) and Ao['q7_rows'], (n_out, Vo[:3])
508 |     # 封印した予想を書き換えると、報告を組む前の確かめが止める（一時の置き場の写しで・裁定 D236・器の実装の検分の R2-重大1）
509 |     _selftest_sealed(T3, FJ, DJ)
510 |     print('[build_report_Bl3] 自己検査 OK（合成の報告の走査の違反 0・起草者の欄が空なら埋め残し・禁止語と未登録の数は止まる・掃き出しは欠けを捕まえる・止まった下見と外した升目の組み立て・'
511 |           '門の行だけの升目の外し・等方の外の行の枝 %d 行・書き換えた予想で止まる）' % n_out)
512 | 
513 | 
514 | def _selftest_sealed(T3, FJ, DJ):
515 |     """一時の置き場に、正本・設計事実・方向の記録・照らす器・予想・封印の記録・凍結の記録を置き、報告の入力を読む。予想を一字変えると止まることを確かめる。"""
516 |     import tempfile, shutil
517 |     import analyze_Bl3 as AZ
518 |     global REPO
519 |     keep = REPO
520 |     A = synth_analysis(T3, FJ, DJ)                                  # 段階 B の記録を読むので、置き場を切り替える前に作る
521 |     td = tempfile.mkdtemp(prefix='report-sealed-')
522 |     try:
523 |         for f in AZ.FROZEN_CHECK:
524 |             os.makedirs(os.path.dirname(os.path.join(td, *f.split('/'))), exist_ok=True)
525 |             shutil.copyfile(os.path.join(keep, *f.split('/')), os.path.join(td, *f.split('/')))
526 |         REPO = td
527 |         pdir = P('records/predictions')
528 |         os.makedirs(pdir, exist_ok=True)
529 |         pr = {}
530 |         for role in ('coordinator', 'registrant'):
531 |             pp = os.path.join(pdir, 'predictions-Bl3-%s.json' % role)
532 |             open(pp, 'w', encoding='utf-8', newline='\n').write(json.dumps({'q1.pilot': '続ける', 'q4.gate': '通らない'}, ensure_ascii=False))
533 |             pr[role] = {'path': 'records/predictions/predictions-Bl3-%s.json' % role, 'sha256': hashlib.sha256(open(pp, 'rb').read()).hexdigest().upper()}
534 |         json.dump({'predictions': pr}, open(P('records/Bl3/sealing-record-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
535 |         json.dump(A, open(P('records/Bl3/analysis-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
536 |         FR = {'main_freeze': {'pilot_attempts': A['pilot_attempts'], 'frozen_sha16': {f: sha16f(P(f)) for f in AZ.FROZEN_CHECK},
537 |                               'seal': {'record_sha16': sha16f(P('records/Bl3/sealing-record-Bl3.json')), 'predictions_sha256': {r: v['sha256'] for r, v in pr.items()}}}, 'deviations': []}
538 |         json.dump(FR, open(P('records/Bl3/FREEZE-RECORD-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
539 |         load_inputs()                                                  # 書き換える前は通る
540 |         pp = P('records/predictions/predictions-Bl3-coordinator.json')
541 |         open(pp, 'w', encoding='utf-8', newline='\n').write(json.dumps({'q1.pilot': '続ける', 'q4.gate': '通る'}, ensure_ascii=False))
542 |         try:
543 |             load_inputs()
544 |             raise AssertionError('書き換えた予想で報告を組もうとした')
545 |         except SystemExit as e_:
546 |             assert '封印した予想' in str(e_), e_
547 |     finally:
548 |         REPO = keep
549 |         shutil.rmtree(td, ignore_errors=True)
550 | 
551 | 
552 | if __name__ == '__main__':
553 |     main()
```
<<< 終: `tools/build_report_Bl3.py` >>>

<<< 始: `tools/seal_Bl3.py`（SHA16 0041BA954F094E21・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """seal_Bl3.py v2 —— B-lens 層三（Bl3）の予想の封印（2026-09-25・正本 `predictions.order`・`predictions.when`: 下見の前の凍結の後・下見の前に、コーディネータが先に封印して
  3 | SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する・裁定 D148・D210・`tools/seal_Blens.py` v2 の型）。
  4 | 
  5 | 相:
  6 |   coordinator  コーディネータの選んだ値（鍵 → 値の JSON）から、予想の JSON を書式（`records/predictions/predictions-form-Bl3-v1.html`）の JS と**同じ形**で書く
  7 |                （様式の名・プログラム・正本の版の三つの後に、書式の全ての欄の鍵を並べ替えて置く・字下げ一・末尾の改行なし）。書式と同じ鍵・同じ選択肢だけを受ける。
  8 |                下見の前の凍結の記録が無ければ止め、書式の SHA16 が凍結の記録と違えば止める（正本 `predictions.when`）。
  9 |                コーディネータは予想の欄を全て埋める。ただし q2 を「零」にしたときの q7 は「予想しない」のまま（q7 は等方の外の v̂ の行があるときだけの項目・
 10 |                `predictions.q7_rule`）。情報状態の欄（`free`）を空にしない（正本 `predictions.free`）。書いた JSON の SHA-256 を印字する（登録者には SHA だけを伝える）。
 11 |   registrant   登録者が書式で作った JSON（ダウンロードしたもの）を、チャットに貼られた SHA-256 と突き合わせてから、そのまま置き場に写す。書式の鍵と選択肢の内にあることを確かめる。
 12 |   record       封印の記録（両方の予想の JSON の置き場と SHA-256・順と時刻・情報状態の決まり・下見の前の凍結の記録の SHA16）を書く。Colab の起動器の相 pilot と相 main は、
 13 |                この記録が無ければ走らない。
 14 | 既にあるファイルには書かない（封印は一度だけ）。予想の欄は「予想しない」を値として受ける（書式の初めの値・B-lens の逸脱 D-BL1 の型）。
 15 | 用法: python tools/seal_Bl3.py coordinator --choices <値の JSON> --date <日付>
 16 |       python tools/seal_Bl3.py registrant --json <登録者の JSON> --sha <SHA-256>
 17 |       python tools/seal_Bl3.py record ／ --selftest
 18 | 柵: 本器のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 19 | """
 20 | import os, sys, json, hashlib, argparse, datetime
 21 | 
 22 | HERE = os.path.dirname(os.path.abspath(__file__))
 23 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 24 | sys.path.insert(0, HERE)
 25 | import make_predictions_form_Bl3 as FORM
 26 | 
 27 | VERSION = 'v2'          # v2（2026-09-25・裁定 D236）: 登録者の情報状態の欄が空なら、封印は止めずに印を置いて知らせる
 28 | PRED = os.path.join(REPO, 'records', 'predictions')
 29 | PATHS = {'coordinator': os.path.join(PRED, 'predictions-Bl3-coordinator.json'), 'registrant': os.path.join(PRED, 'predictions-Bl3-registrant.json')}
 30 | RECORD_JSON = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
 31 | RECORD_MD = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.md')
 32 | FREEZE = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
 33 | ROLE_WHO = {'coordinator': 'コーディネータ', 'registrant': '登録者'}
 34 | rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
 35 | sha256b = lambda b: hashlib.sha256(b).hexdigest().upper()
 36 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 37 | now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
 38 | 
 39 | 
 40 | def form_spec():
 41 |     T = FORM.load_T()
 42 |     h = open(FORM.OUT, encoding='utf-8').read()
 43 |     keys, opts = FORM.read_form(h)
 44 |     return T, keys, opts, FORM.meta(T)
 45 | 
 46 | 
 47 | def to_json(values, T, keys, M):
 48 |     """書式の JS（`gen`）と同じ形の JSON の文字列（JSON.stringify(sorted, null, 1)）。"""
 49 |     o = {'form': M['form'], 'program': M['program'], 'contrasts': M['contrasts']}
 50 |     for k in sorted(keys):
 51 |         o[k] = values.get(k, '')
 52 |     return json.dumps(o, ensure_ascii=False, indent=1)
 53 | 
 54 | 
 55 | def validate(values, keys, opts, role, T, full=False):
 56 |     bad = [k for k in values if k not in keys and k not in ('form', 'program', 'contrasts')]
 57 |     if bad:
 58 |         raise SystemExit('書式に無い鍵: %s' % bad)
 59 |     pred = set(FORM.prediction_keys(T))
 60 |     for k, v in values.items():
 61 |         if k in opts and v not in opts[k] and not (v == FORM.NP and k in pred):     # 「予想しない」は予想の欄の初めの値（ボタンではない）
 62 |             raise SystemExit('書式に無い選択肢: %s=%s' % (k, v))
 63 |     if values.get('who') != ROLE_WHO[role]:
 64 |         raise SystemExit('予想者の欄が役と合わない: %s' % values.get('who'))
 65 |     if full:
 66 |         miss = []
 67 |         q7_moot = values.get('q2.vhat_iso') == '零'
 68 |         for k in FORM.prediction_keys(T):
 69 |             v = values.get(k, FORM.NP)
 70 |             if k == 'q7.direction' and q7_moot:
 71 |                 if v != FORM.NP:
 72 |                     miss.append('%s（q2 が「零」なのに q7 がある）' % k)
 73 |             elif v == FORM.NP:
 74 |                 miss.append(k)
 75 |         if not (values.get('free') or '').strip():
 76 |             miss.append('free（情報状態）')
 77 |         if miss:
 78 |             raise SystemExit('コーディネータの予想に埋まっていない欄がある: %s' % miss)
 79 | 
 80 | 
 81 | def require_prepilot_freeze():
 82 |     """下見の前の凍結の記録があり、書式の SHA16 が凍結の記録と同じこと（正本 predictions.when）。"""
 83 |     if not os.path.exists(FREEZE):
 84 |         raise SystemExit('下見の前の凍結の記録が無い（封印は凍結の後・正本 predictions.when）: %s' % rel(FREEZE))
 85 |     FR = json.load(open(FREEZE, encoding='utf-8'))
 86 |     want = (FR.get('frozen_sha16') or {}).get(rel(FORM.OUT))
 87 |     if want is None or want != sha16f(FORM.OUT):
 88 |         raise SystemExit('書式の SHA16 が凍結の記録と違う（凍結の後に書式が変わった）: %s ≠ %s' % (sha16f(FORM.OUT), want))
 89 |     if 'main_freeze' in FR:
 90 |         raise SystemExit('凍結の記録に本の凍結がある（封印は下見の前・正本 predictions.when）')
 91 |     return FR
 92 | 
 93 | 
 94 | def coordinator(choices_path, date):
 95 |     if os.path.exists(PATHS['coordinator']):
 96 |         raise SystemExit('既にある（封印は一度だけ）: %s' % rel(PATHS['coordinator']))
 97 |     if os.path.exists(PATHS['registrant']):
 98 |         raise SystemExit('登録者の予想が先にある（正本の順はコーディネータが先）')
 99 |     require_prepilot_freeze()
100 |     T, keys, opts, M = form_spec()
101 |     vals = {k: FORM.NP for k in opts}
102 |     vals.update({k: '' for k in keys if k not in opts})
103 |     vals.update(json.load(open(choices_path, encoding='utf-8')))
104 |     vals['who'], vals['date'] = ROLE_WHO['coordinator'], date
105 |     validate(vals, keys, opts, 'coordinator', T, full=True)
106 |     s = to_json(vals, T, keys, M)
107 |     b = s.encode('utf-8')
108 |     os.makedirs(PRED, exist_ok=True)
109 |     open(PATHS['coordinator'], 'wb').write(b)
110 |     print('[seal_Bl3] コーディネータの予想を封印した: %s・SHA-256 %s（登録者には SHA だけを伝える）' % (rel(PATHS['coordinator']), sha256b(b)))
111 | 
112 | 
113 | def registrant(json_path, sha):
114 |     if not os.path.exists(PATHS['coordinator']):
115 |         raise SystemExit('コーディネータの封印がまだ無い（正本の順）')
116 |     if os.path.exists(PATHS['registrant']):
117 |         raise SystemExit('既にある（封印は一度だけ）: %s' % rel(PATHS['registrant']))
118 |     b = open(json_path, 'rb').read()
119 |     if sha256b(b) != sha.strip().upper():
120 |         raise SystemExit('登録者の JSON の SHA-256 がチャットの値と違う: %s ≠ %s' % (sha256b(b), sha))
121 |     T, keys, opts, M = form_spec()
122 |     vals = json.loads(b.decode('utf-8'))
123 |     if any(vals.get(k) != M[k] for k in ('form', 'program', 'contrasts')):
124 |         raise SystemExit('登録者の JSON の様式の名・プログラム・正本の版が書式と違う')
125 |     validate(vals, keys, opts, 'registrant', T, full=False)
126 |     empty = info_empty(vals)
127 |     if empty:
128 |         print('[seal_Bl3] 登録者の情報状態の欄が空です（%s）。封印は止めません。正本 predictions.free（裁定 D217）は両方が書くとするので、登録者にお知らせします' % '・'.join(empty))
129 |     open(PATHS['registrant'], 'wb').write(b)
130 |     print('[seal_Bl3] 登録者の予想を写した: %s・SHA-256 %s' % (rel(PATHS['registrant']), sha256b(b)))
131 | 
132 | 
133 | def info_empty(v):
134 |     """情報状態の欄（`info.coi`・`free`）のうち、空のものの名（正本 predictions.free・裁定 D217・D236）。"""
135 |     return [k for k in ('info.coi', 'free') if not str(v.get(k) or '').strip()]
136 | 
137 | 
138 | def record():
139 |     if os.path.exists(RECORD_JSON):
140 |         raise SystemExit('既にある（封印の記録は一度だけ）: %s' % rel(RECORD_JSON))
141 |     require_prepilot_freeze()
142 |     T, keys, opts, M = form_spec()
143 |     R = {'kind': 'bl3_sealing_record', 'version': VERSION, 'written_utc': now(), 'order': T['predictions']['order'], 'when': T['predictions']['when'],
144 |          'free_rule': T['predictions']['free'], 'freeze_record_sha16': sha16f(FREEZE),
145 |          'form': {'path': rel(FORM.OUT), 'sha256': sha256b(open(FORM.OUT, 'rb').read()), 'meta': M}, 'predictions': {}}
146 |     for role, p in PATHS.items():
147 |         if not os.path.exists(p):
148 |             raise SystemExit('予想の JSON が無い: %s' % rel(p))
149 |         b = open(p, 'rb').read()
150 |         v = json.loads(b.decode('utf-8'))
151 |         validate(v, keys, opts, role, T, full=(role == 'coordinator'))
152 |         R['predictions'][role] = {'path': rel(p), 'sha256': sha256b(b), 'date': v.get('date'), 'n_predicted': sum(1 for k in FORM.prediction_keys(T) if v.get(k) not in (None, '', FORM.NP)),
153 |                                   'info_empty': info_empty(v)}                 # 情報状態の欄が空なら、その欄の名（裁定 D236）
154 |     R['clause'] = '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
155 |     json.dump(R, open(RECORD_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
156 |     md = ['# B-lens 層三の予想の封印の記録（機械生成・`tools/seal_Bl3.py` %s・%s）' % (VERSION, R['written_utc']), '',
157 |           '- 順: %s' % R['order'], '- 時: %s' % R['when'], '- 情報状態の決まり: %s' % R['free_rule'],
158 |           '- 書式: `%s`（SHA-256 %s）' % (R['form']['path'], R['form']['sha256']), '- 下見の前の凍結の記録: `%s`（SHA16 %s）' % (rel(FREEZE), R['freeze_record_sha16'])]
159 |     md += ['- %s の予想: `%s`（SHA-256 %s・日付 %s・予想した欄 %d%s）' % (ROLE_WHO[r], x['path'], x['sha256'], x['date'], x['n_predicted'],
160 |                                                               ('・情報状態の欄が空: %s' % '・'.join(x['info_empty'])) if x['info_empty'] else '') for r, x in R['predictions'].items()]
161 |     md += ['- この記録が無ければ、Colab の起動器の相 pilot と相 main は走らない。', '', R['clause'], '']
162 |     open(RECORD_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(md))
163 |     print('[seal_Bl3] 封印の記録を書いた: %s' % rel(RECORD_JSON))
164 | 
165 | 
166 | def _selftest():
167 |     import tempfile
168 |     T = FORM.load_T()
169 |     h = FORM.build(T)
170 |     with tempfile.TemporaryDirectory() as td0:
171 |         g = globals()
172 |         saved = {n: g[n] for n in ('PRED', 'PATHS', 'RECORD_JSON', 'RECORD_MD', 'FREEZE')}
173 |         saved_out = FORM.OUT
174 |         try:
175 |             FORM.OUT = os.path.join(td0, 'form.html')
176 |             open(FORM.OUT, 'w', encoding='utf-8', newline='\n').write(h)
177 |             T, keys, opts, M = form_spec()
178 |             vals = {it['key']: it['options'][0] for it in FORM.items(T)}
179 |             vals.update({'q2.vhat_iso': '一から三', 'who': 'コーディネータ', 'info.coi': 'x', 'free': '露出の記録を読んだ', 'date': '2026-09-26'})
180 |             validate(vals, keys, opts, 'coordinator', T, full=True)
181 |             s = to_json(vals, T, keys, M)
182 |             o = json.loads(s)
183 |             assert list(o)[:3] == ['form', 'program', 'contrasts'] and list(o)[3:] == sorted(keys) and not s.endswith('\n')
184 |             # 止まるべき場合（正しい理由で）: 埋まっていない予想・q2 が零なのに q7 がある・情報状態が空・書式に無い値
185 |             for k_, v_, why in (('q5.gate_wo_vhat', FORM.NP, '埋まっていない'), ('q2.vhat_iso', '零', 'q7 がある'), ('free', '  ', '情報状態')):
186 |                 try:
187 |                     validate(dict(vals, **{k_: v_}), keys, opts, 'coordinator', T, full=True)
188 |                     raise AssertionError('通してはいけない予想を通した: %s=%s' % (k_, v_))
189 |                 except SystemExit as e_:
190 |                     assert why in str(e_), ('別の理由で止まった', k_, str(e_))
191 |             # 通るべき場合: q2 が零で q7 が「予想しない」
192 |             validate(dict(vals, **{'q2.vhat_iso': '零', 'q7.direction': FORM.NP}), keys, opts, 'coordinator', T, full=True)
193 |             # 選ばない欄のある登録者の JSON
194 |             v5 = {k: FORM.NP for k in FORM.prediction_keys(T)}
195 |             v5.update({'q1.pilot': '続ける', 'q4.gate': '通らない', 'who': '登録者', 'info.coi': '', 'free': '', 'date': '2026-09-26'})
196 |             validate(v5, keys, opts, 'registrant', T, full=False)
197 |             for k_, bad_ in (('q4.gate', 'x'), ('who', FORM.NP)):
198 |                 try:
199 |                     validate(dict(v5, **{k_: bad_}), keys, opts, 'registrant', T, full=False)
200 |                     raise AssertionError('書式に無い値を通した: %s=%s' % (k_, bad_))
201 |                 except SystemExit as e_:
202 |                     assert '書式に無い選択肢' in str(e_) or '予想者の欄' in str(e_), str(e_)
203 |             # 端から端まで（一時の置き場・凍結の記録が無い → 止まる・凍結の記録 → コーディネータ → 登録者 → 記録・本の凍結の後は止まる）
204 |             g['PRED'] = td0
205 |             g['PATHS'] = {'coordinator': os.path.join(td0, 'c.json'), 'registrant': os.path.join(td0, 'r.json')}
206 |             g['RECORD_JSON'], g['RECORD_MD'], g['FREEZE'] = os.path.join(td0, 'rec.json'), os.path.join(td0, 'rec.md'), os.path.join(td0, 'fr.json')
207 |             cj = os.path.join(td0, 'choices.json')
208 |             json.dump({k: v for k, v in vals.items() if k not in ('who', 'date')}, open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
209 |             try:
210 |                 coordinator(cj, '2026-09-26')
211 |                 raise AssertionError('凍結の記録が無いのに封印した')
212 |             except SystemExit as e_:
213 |                 assert '凍結の記録が無い' in str(e_), str(e_)
214 |             json.dump({'frozen_sha16': {rel(FORM.OUT): sha16f(FORM.OUT)}}, open(g['FREEZE'], 'w', encoding='utf-8'))
215 |             coordinator(cj, '2026-09-26')
216 |             rj = os.path.join(td0, 'registrant-download.json')
217 |             rb = to_json(v5, T, keys, M).encode('utf-8')
218 |             open(rj, 'wb').write(rb)
219 |             registrant(rj, sha256b(rb))
220 |             record()
221 |             R = json.load(open(g['RECORD_JSON'], encoding='utf-8'))
222 |             assert set(R['predictions']) == {'coordinator', 'registrant'} and R['predictions']['registrant']['sha256'] == sha256b(rb)
223 |             assert open(g['PATHS']['registrant'], 'rb').read() == rb
224 |             json.dump({'frozen_sha16': {rel(FORM.OUT): sha16f(FORM.OUT)}, 'main_freeze': {}}, open(g['FREEZE'], 'w', encoding='utf-8'))
225 |             try:
226 |                 require_prepilot_freeze()
227 |                 raise AssertionError('本の凍結の後の封印を通した')
228 |             except SystemExit as e_:
229 |                 assert '本の凍結' in str(e_), str(e_)
230 |         finally:
231 |             g.update(saved)
232 |             FORM.OUT = saved_out
233 |     print('[seal_Bl3] 自己検査 OK（%s・凍結の記録の確かめと「予想しない」の欄を含む封印を端から端まで通した）' % VERSION)
234 | 
235 | 
236 | if __name__ == '__main__':
237 |     ap = argparse.ArgumentParser()
238 |     ap.add_argument('phase', nargs='?', choices=['coordinator', 'registrant', 'record'])
239 |     ap.add_argument('--choices')
240 |     ap.add_argument('--date')
241 |     ap.add_argument('--json')
242 |     ap.add_argument('--sha')
243 |     ap.add_argument('--selftest', action='store_true')
244 |     a = ap.parse_args()
245 |     if a.selftest:
246 |         _selftest()
247 |     elif a.phase == 'coordinator':
248 |         coordinator(a.choices, a.date)
249 |     elif a.phase == 'registrant':
250 |         registrant(a.json, a.sha)
251 |     elif a.phase == 'record':
252 |         record()
253 |     else:
254 |         ap.print_help()
```
<<< 終: `tools/seal_Bl3.py` >>>

<<< 始: `tools/make_frozen_Bl3.py`（SHA16 8DF4EA70CC3EAB15・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """make_frozen_Bl3.py v3 —— B-lens 層三（Bl3）の凍結する本文（`design/design-Bl3-FROZEN.{src.md,md}`）を、草案3 の原稿から組む（B-lens の `make_frozen_Blens.py` の型・2026-09-25）。
  3 | 
  4 | 草案3 の登録者の確認の後に、正本の文を直す裁定（D226〜D238）があったので、凍結の本文は草案3 の本文と次の三つの差だけを持つ（ほかの差があれば止める）:
  5 |   (一) 題名の印・凍結の一行・組み立ての記録の行（段階 B の器 `make_frozen_B.other_diffs` が許す差）。
  6 |   (二) 正本の鍵と設計事実から組まれる行のうち、正本と設計事実の直しで変わった行。同じ原稿を今の正本と設計事実で組み直した本文（組み直し）と草案3 の本文の差として機械で出し、
  7 |        記録（`records/Bl3/frozen-diff-Bl3.md`）に並べる。原稿の SHA16 が草案3 の組み立ての記録と、組み立ての器の SHA16 が草案3 の本文を最後に変えたコミットの器と同じことを
  8 |        確かめるので、この差は正本と設計事実だけから来る。
  9 |   (三) 原稿の文の直し（`LITERAL_FIXES`・裁定ごと・原稿の中でちょうど一度ずつ当たる）。組み直しと凍結の本文の差が、(一) の行と、直しの前後の文を含む行だけであることを確かめる。
 10 | 凍結の一行は、題名と本行と、裁定で直した行（正本の鍵から組まれる行と、原稿の直し）だけを改めたことを書く（段階 B の型の一行の「題名と本行のみ改める」を、この登録の事実に合わせた）。
 11 | **本器は凍結そのものではない**——凍結の記帳は `tools/freeze_Bl3.py` が行う。
 12 | 用法: python tools/make_frozen_Bl3.py --words "<登録者の逐語>" --commit <草案の原稿のコミット> --date "<日時（日本時間）>" [--force] ／ --check（組み直しと差の記録だけ）／ --selftest
 13 | 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 14 | """
 15 | import os, re, sys, difflib, hashlib, argparse, subprocess, tempfile
 16 | 
 17 | HERE = os.path.dirname(os.path.abspath(__file__))
 18 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 19 | sys.path.insert(0, HERE)
 20 | import make_frozen_B as MF
 21 | 
 22 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 凍結の一行を組み立ての検査の外に置く・凍結版の原稿を組み直して本文と照らす／v2: 組み直しの記録の置き場の言い方・裁定の範囲
 23 | STANDIN = '- **凍結**: （凍結の一行・登録者の逐語と日時は組み立ての後に入れる）'      # 組み立ての間の代わりの行（裁定 D236）
 24 | REBUILD_LINT_LABEL = '（組み直しの一時の置き場の数の検査の記録）'      # 組み直しの本文の「束縛」の行の記録の置き場（一時の置き場の道筋を凍結物に残さない）
 25 | NL = chr(10)
 26 | SRC = os.path.join(REPO, 'design', 'design-Bl3-draft3.src.md')
 27 | DRAFT = os.path.join(REPO, 'design', 'design-Bl3-draft3.md')
 28 | FSRC = os.path.join(REPO, 'design', 'design-Bl3-FROZEN.src.md')
 29 | FOUT = os.path.join(REPO, 'design', 'design-Bl3-FROZEN.md')
 30 | LINT = os.path.join(REPO, 'records', 'Bl3', 'numbers-lint-FROZEN-Bl3.md')
 31 | DIFFREC = os.path.join(REPO, 'records', 'Bl3', 'frozen-diff-Bl3.md')
 32 | BUILDER = os.path.join(HERE, 'build_draft_Bl3.py')
 33 | FROZEN_LINE = ('- **凍結**: %s（日本時間・登録者の言葉は逐語で「%s」・草案3 の原稿〔コミット %s 時点〕を逐語複製し、題名と本行と、裁定 D226〜D238 で正本の文を直した行'
 34 |                '〔正本の鍵から組まれる行と、原稿の直し〕だけを改める・直した行は `records/Bl3/frozen-diff-Bl3.md`・以後の変更は逸脱台帳に記帳する）')
 35 | # 原稿の文の直し（裁定・直す前・直した後）。直す前の文は原稿の中でちょうど一度だけ当たること。
 36 | LITERAL_FIXES = [
 37 |     ('D226', '加減のベクトルの足し方は段階 B の走行器のフック（`tools/run_stageB_local.py`）と同じ形にし、方向ごとに違うベクトルを一つのバッチで足す道は層三の器で新しく書く（§3.3）。',
 38 |      '加減のベクトルの足し方は段階 B の走行器のフック（`tools/run_stageB_local.py`）をそのまま呼ぶ（方向ごとに違うベクトルを一つのバッチで足す形は、このフックがもともと持つ・§3.3・裁定 D226）。'),
 39 | ]
 40 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 41 | rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
 42 | 
 43 | 
 44 | def diffs(a_path, b_path):
 45 |     a = open(a_path, encoding='utf-8').read().split('\n')
 46 |     b = open(b_path, encoding='utf-8').read().split('\n')
 47 |     return [l for l in difflib.unified_diff(a, b, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]
 48 | 
 49 | 
 50 | def frozen_src(text, words, commit, date):
 51 |     """原稿の本文 → 凍結版の原稿の本文（題名に印・起草の行の次に凍結の一行・原稿の文の直し）。"""
 52 |     lines = text.split('\n')
 53 |     if not lines[0].startswith('# ') or MF.MARK in lines[0]:
 54 |         raise ValueError('題名の行が見つからないか、既に凍結版の題名になっている')
 55 |     head, sep, tail = lines[0].partition('）——')
 56 |     if not sep:
 57 |         raise ValueError('題名の形が違う（「）——」で分かれない）')
 58 |     lines[0] = head + '）' + MF.MARK + tail
 59 |     idx = [i for i, l in enumerate(lines) if l.startswith('- 起草:')]
 60 |     if not idx:
 61 |         raise ValueError('起草の行が見つからない')
 62 |     lines.insert(idx[0] + 1, FROZEN_LINE % (date, words, commit))
 63 |     out = '\n'.join(lines)
 64 |     for rid, old, new in LITERAL_FIXES:
 65 |         if out.count(old) != 1:
 66 |             raise ValueError('原稿の直しの前の文がちょうど一度だけ当たらない（%s・%d 回）' % (rid, out.count(old)))
 67 |         out = out.replace(old, new)
 68 |     return out
 69 | 
 70 | 
 71 | def build(src_path, out_path, label, lint_path):
 72 |     r = subprocess.run([sys.executable, BUILDER, '--src', src_path, '--out', out_path, '--label', label, '--lint-report', lint_path],
 73 |                        capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO)
 74 |     if r.returncode != 0:
 75 |         print(r.stdout[-2000:], r.stderr[-2000:])
 76 |         raise SystemExit('組み立てが止まった（%s）' % rel(src_path))
 77 |     return r
 78 | 
 79 | 
 80 | def build_frozen(src_path, out_path, lint_path):
 81 |     """凍結版の原稿を組む（裁定 D236）: 凍結の一行を決まった代わりの行にして組み立て（数の検査と禁止語の走査はこの本文で走る）、組み立ての後に逐語の一行に戻す。"""
 82 |     src = open(src_path, encoding='utf-8').read()
 83 |     fl = [l for l in src.split('\n') if l.startswith('- **凍結**:')]
 84 |     if len(fl) != 1:
 85 |         raise SystemExit('凍結版の原稿に凍結の一行がちょうど一つでない（%d）' % len(fl))
 86 |     with tempfile.TemporaryDirectory() as td:
 87 |         tmp = os.path.join(td, 'frozen-standin.src.md')
 88 |         open(tmp, 'w', encoding='utf-8', newline='\n').write(src.replace(fl[0], STANDIN))
 89 |         build(tmp, out_path, '凍結版', lint_path)
 90 |     out = open(out_path, encoding='utf-8').read()
 91 |     if out.count(STANDIN) != 1:
 92 |         raise SystemExit('組み立てた本文に代わりの行がちょうど一つでない')
 93 |     open(out_path, 'w', encoding='utf-8', newline='\n').write(out.replace(STANDIN, fl[0]))
 94 | 
 95 | 
 96 | def draft3_record():
 97 |     """草案3 の組み立ての記録の原稿の SHA16（本文の行）と、草案3 の本文を最後に変えたコミットの組み立ての器の SHA16（git から読む・草案3 の数の検査の記録は器の SHA16 を持たないため）。"""
 98 |     t = open(DRAFT, encoding='utf-8').read()
 99 |     m = re.search(r'原稿 `design/design-Bl3-draft3\.src\.md` SHA16 ([0-9A-F]{16})', t)
100 |     c = subprocess.run(['git', '-C', REPO, 'log', '-1', '--format=%H', '--', rel(DRAFT)], capture_output=True, text=True).stdout.strip()
101 |     b = subprocess.run(['git', '-C', REPO, 'show', '%s:%s' % (c, rel(BUILDER))], capture_output=True).stdout if c else b''
102 |     return (m.group(1) if m else None), (hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16] if b else None)
103 | 
104 | 
105 | def rebuild_and_check(fsrc=None, fout=None):
106 |     """組み直し（同じ原稿を今の正本と設計事実で）と草案3 の差（二）・組み直しと凍結の本文の差の残り（一と三の外）を返す。"""
107 |     src_sha, builder_sha = draft3_record()
108 |     res = {'src_sha16_record': src_sha, 'src_sha16_now': sha16f(SRC), 'builder_sha16_record': builder_sha, 'builder_sha16_now': sha16f(BUILDER)}
109 |     bad = []
110 |     if src_sha != res['src_sha16_now']:
111 |         bad.append('草案3 の原稿の SHA16 が草案3 の組み立ての記録と違う')
112 |     if builder_sha is None:
113 |         bad.append('草案3 の本文を最後に変えたコミットの組み立ての器を git から読めない')
114 |     elif builder_sha != res['builder_sha16_now']:
115 |         bad.append('組み立ての器の SHA16 が、草案3 の本文を最後に変えたコミットの器と違う')
116 |     with tempfile.TemporaryDirectory() as td:
117 |         rb = os.path.join(td, 'rebuilt.md')
118 |         build(SRC, rb, '草案3', os.path.join(td, 'lint.md'))
119 |         t_rb, tmp_lint = open(rb, encoding='utf-8').read(), rel(os.path.join(td, 'lint.md'))
120 |         if t_rb.count(tmp_lint) != 1:
121 |             raise SystemExit('組み直しの本文に、数の検査の記録の置き場がちょうど一度だけ現れない（止める）')
122 |         open(rb, 'w', encoding='utf-8', newline='\n').write(t_rb.replace(tmp_lint, REBUILD_LINT_LABEL))
123 |         canon_driven = diffs(DRAFT, rb)
124 |         residual = None
125 |         res['frozen_src_rebuilt_same'] = None
126 |         if fsrc and fout and os.path.exists(fsrc) and os.path.exists(fout):
127 |             fr = os.path.join(td, 'frozen-rebuilt.md')
128 |             build_frozen(fsrc, fr, os.path.join(td, 'lint-frozen.md'))
129 |             t_fr = open(fr, encoding='utf-8').read().replace(rel(os.path.join(td, 'lint-frozen.md')), rel(LINT))
130 |             res['frozen_src_rebuilt_same'] = (t_fr == open(fout, encoding='utf-8').read())
131 |             if not res['frozen_src_rebuilt_same']:
132 |                 bad.append('凍結版の原稿を組み直した本文が、凍結の本文と違う')
133 |         if fout and os.path.exists(fout):
134 |             d = MF.other_diffs(diffs(rb, fout))
135 |             olds = [o for _, o, _ in LITERAL_FIXES]
136 |             news = [n for _, _, n in LITERAL_FIXES]
137 |             residual = [l for l in d if not ((l.startswith('-') and any(o in l for o in olds)) or (l.startswith('+') and any(n in l for n in news)))]
138 |             hit_old = sum(1 for l in d if l.startswith('-') and any(o in l for o in olds))
139 |             hit_new = sum(1 for l in d if l.startswith('+') and any(n in l for n in news))
140 |             if residual:
141 |                 bad.append('凍結の本文と組み直しに、許す差でない差がある（%d 行）' % len(residual))
142 |             if hit_old != len(LITERAL_FIXES) or hit_new != len(LITERAL_FIXES):
143 |                 bad.append('原稿の直しの行が凍結の本文に現れない')
144 |     res.update({'canon_driven': canon_driven, 'residual': residual})
145 |     return res, bad
146 | 
147 | 
148 | def write_diffrec(res):
149 |     L = ['# B-lens 層三の凍結の本文と草案3 の差の記録（機械生成・`tools/make_frozen_Bl3.py` %s）' % VERSION, '',
150 |          '- 草案3 の原稿 `%s` SHA16 %s（草案3 の組み立ての記録 %s）・組み立ての器 `%s` SHA16 %s（草案3 の本文を最後に変えたコミットの器 %s）。' % (
151 |              rel(SRC), res['src_sha16_now'], res['src_sha16_record'], rel(BUILDER), res['builder_sha16_now'], res['builder_sha16_record']),
152 |          '- (二) 正本の鍵と設計事実から組まれる行の差（同じ原稿を今の正本と設計事実で組み直した本文と、草案3 の本文の差・行の頭の - が草案3・+ が組み直し）:', '', '```diff'] + \
153 |         res['canon_driven'] + ['```', '', '- (三) 原稿の文の直し（裁定・直す前 → 直した後）:', ''] + \
154 |         ['  - %s: 「%s」→「%s」' % (rid, o, n) for rid, o, n in LITERAL_FIXES] + \
155 |         ['', '- 組み直しと凍結の本文の差の残り（(一) と (三) の外）: %s' % ('無し' if res.get('residual') == [] else ('確かめていない' if res.get('residual') is None else '%d 行' % len(res['residual']))),
156 |          '- 凍結版の原稿を同じ手順で組み直した本文と凍結の本文: %s' % {True: '同じ', False: '違う', None: '確かめていない'}[res.get('frozen_src_rebuilt_same')],
157 |          '- 凍結の一行（登録者の逐語と日時）は、組み立ての数の検査と禁止語の走査の外に置いた（組み立ての間は決まった代わりの行を置き、組み立ての後に逐語の一行を入れた・裁定 D236）。', '',
158 |          '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
159 |     open(DIFFREC, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
160 | 
161 | 
162 | def main():
163 |     ap = argparse.ArgumentParser()
164 |     ap.add_argument('--words')
165 |     ap.add_argument('--commit')
166 |     ap.add_argument('--date')
167 |     ap.add_argument('--force', action='store_true')
168 |     ap.add_argument('--check', action='store_true')
169 |     ap.add_argument('--selftest', action='store_true')
170 |     a = ap.parse_args()
171 |     if a.selftest:
172 |         src = open(SRC, encoding='utf-8').read()
173 |         out = frozen_src(src, '（自己検査）', 'deadbee', '2026-09-26 10:00')
174 |         lines = out.split('\n')
175 |         assert MF.MARK in lines[0] and lines[3].startswith('- **凍結**:'), lines[:4]
176 |         d = [l for l in difflib.unified_diff(src.split('\n'), lines, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]
177 |         rest = MF.other_diffs(d)
178 |         assert len(rest) == 2 * len(LITERAL_FIXES) and all(any(x in l for _, o, n in LITERAL_FIXES for x in (o, n)) for l in rest), rest
179 |         try:
180 |             frozen_src(src.replace(LITERAL_FIXES[0][1], ''), 'x', 'y', 'z')
181 |             raise AssertionError('直しの前の文が無い原稿を通した')
182 |         except ValueError:
183 |             pass
184 |         # 凍結の一行に数のある逐語でも組める（組み立ての検査の外・裁定 D236）
185 |         with tempfile.TemporaryDirectory() as td:
186 |             fs, fo = os.path.join(td, 'f.src.md'), os.path.join(td, 'f.md')
187 |             words_ = '10時に凍結してください（自己検査）'
188 |             open(fs, 'w', encoding='utf-8', newline='\n').write(frozen_src(src, words_, 'deadbee', '2026-09-26 10:00'))
189 |             build_frozen(fs, fo, os.path.join(td, 'lint.md'))
190 |             t = open(fo, encoding='utf-8').read()
191 |             assert words_ in t and STANDIN not in t and t.count('- **凍結**:') == 1, '凍結の一行が本文に入らない'
192 |         print('[make_frozen_Bl3] 自己検査 OK（題名の印・凍結の一行・原稿の直しの %d 行だけが原稿の差・数のある逐語の凍結の一行でも組める）' % len(LITERAL_FIXES))
193 |         return
194 |     if a.check:
195 |         res, bad = rebuild_and_check(FSRC, FOUT)
196 |         write_diffrec(res)
197 |         print('[make_frozen_Bl3] 組み直しの差 %d 行（記録 %s）・凍結の本文の残りの差 %s・外れ %s' % (len(res['canon_driven']), rel(DIFFREC), res['residual'] if res['residual'] is None else len(res['residual']), bad or '無し'))
198 |         if bad:
199 |             raise SystemExit('確かめが外れた: %s' % bad)
200 |         return
201 |     if not (a.words and a.commit and a.date):
202 |         raise SystemExit('--words・--commit・--date が要る')
203 |     for p in (FSRC, FOUT):
204 |         if os.path.exists(p) and not a.force:
205 |             raise SystemExit('既にある（--force で上書き）: %s' % rel(p))
206 |     open(FSRC, 'w', encoding='utf-8', newline='\n').write(frozen_src(open(SRC, encoding='utf-8').read(), a.words, a.commit, a.date))
207 |     build_frozen(FSRC, FOUT, LINT)
208 |     res, bad = rebuild_and_check(FSRC, FOUT)
209 |     write_diffrec(res)
210 |     if bad:
211 |         raise SystemExit('凍結の本文の確かめが外れた: %s' % bad)
212 |     print('[make_frozen_Bl3] %s・%s・%s（正本と設計事実から来る差 %d 行・原稿の直し %d・ほかの差 無し）' % (rel(FSRC), rel(FOUT), rel(DIFFREC), len(res['canon_driven']), len(LITERAL_FIXES)))
213 | 
214 | 
215 | if __name__ == '__main__':
216 |     main()
```
<<< 終: `tools/make_frozen_Bl3.py` >>>

<<< 始: `tools/freeze_Bl3.py`（SHA16 EFCD14D5426693B2・行の頭の番号はこのファイルの行番号） >>>
```
  1 | # -*- coding: utf-8 -*-
  2 | """freeze_Bl3.py v3 —— B-lens 層三（Bl3）の凍結の記帳（2026-09-25・正本 `predictions.when`・`computation.main_freeze_check`・裁定 D210・D222・`tools/freeze_Blens.py` の型）。
  3 | 
  4 | 相:
  5 |   prepilot  下見の前の凍結（正本のすべて・方向の npz・器・裁定 D210）。確かめてから記帳する（外れたら止める・登録者に相談）:
  6 |     - 凍結の本文: `tools/make_frozen_Bl3.py` の確かめ（草案3 との差は、題名・凍結の一行・組み立ての記録・正本と設計事実から来る行・原稿の直しだけ）と、数の検査の違反が零。
  7 |     - 正本: `decisions` に、裁定の記録（`records/Bl3/rulings-D*.md`）の名にある番号がすべてあり、`numbering.rulings_next` がその次の番号。
  8 |       設計事実の `contrasts_sha16` と方向の記録の `contrasts_sha16` が正本の SHA16 と同じ。
  9 |     - 方向の npz: 記録の SHA-256 と同じ・組ごとの SHA-256 が転記行 D と同じ・作り直してバイトで同じ（`tools/bl3_directions.py --check` を走らせる）。
 10 |     - 合成データの正式の記録（`records/Bl3/dry-run-Bl3-*.md` の最新）: 等方の本数が正本と同じで、確かめがすべて期待どおり。記録の末尾の版の SHA16 の表が、
 11 |       器の一覧（下の TOOLS）の import の閉包と正本・設計事実・方向の記録を覆い、今の版とすべて同じ（違えば取り直す）。
 12 |     - 器の自己検査（`bl3_core`・`bl3_directions`・`make_predictions_form_Bl3`・`seal_Bl3`・`build_report_Bl3`・`make_frozen_Bl3`・`bl3_recompute_rewrite`）がすべて通る。
 13 |     - 予想の書式が組めて欄の確かめを通り、書式の正本の版が正本の版と同じ。封印はまだ無い（正本 predictions.when）。
 14 |     - Colab の起動器の相 check の出力（`--colab-check` の置き場の session.json と check.json）: DRY でない・順伝播を呼んでいない・版が正本 `inputs.versions_B` と文字列で同じ・
 15 |       GPU が L4 か A100・重みの SHA-256 が転記行 F と同じ・方向の npz の SHA-256 が記録と同じ・組ごとの SHA-256 が転記行 D と同じ・升目の入力が転記行 B と同じ・
 16 |       残差の書き換えの器を import できた・取り出したコミットの正本の SHA16 が今の正本と同じ・比べる相手の除き方の錨が手元と同じ・‖static‖ が転記行 D と同じ（裁定 D231）。
 17 |     - 器の実装の検分の記録がある（`records/reviews/Bl3/impl/` の採否表・正本 `review_plan.impl`）。
 18 |     記帳: `records/Bl3/FREEZE-RECORD-Bl3.json`・`.md`（凍結物の SHA16・器の閉包・読む記録・方向の npz の SHA-256・確かめ）と、全体の台帳（`records/FREEZE-RECORD.md`）の一行。
 19 |     Colab の確かめの出力は `records/Bl3/colab-check-Bl3-session.json`・`colab-check-Bl3.json` に写す。
 20 |   main      本の凍結（下見の記録と機械の決定を凍結の記録に足す・正本 `computation.main_freeze_check`・裁定 D222）。確かめ:
 21 |     - 正本の SHA16 が下見の前の凍結と同じ（正本を変える直しはこの決まりの外で、登録者に上げる）。
 22 |     - 凍結物の SHA16 の違いが、凍結の記録の逸脱（`deviations` の `tool_diffs`: 置き場・前・後の SHA16）に記した差とすべて一致する。
 23 |     - 下見の試み（`--pilot` の置き場の pilot.json と session.json・試みの順）の session のコミットが、凍結の記録と封印の記録を含む（`git cat-file`）。
 24 |       下見の試みの session が DRY でない。最後の試みが本の凍結の下見（器の誤りの試みは、やり直したときの一度目として残す）。
 25 |     - 凍結の記録に足すのは `main_freeze` の鍵だけ（ほかの鍵は一字も変えない）。
 26 |     記帳: 凍結の記録の `main_freeze`（下見の試み・最後の試みの記録と機械の決定・session・凍結物の SHA16・器の差分・登録者の言葉と時刻）と、全体の台帳の一行。
 27 | v3 の決め（裁定 D236）: 手順の順は「方向の npz と器を push → Colab の相 check → 下見の前の凍結の記帳」。相 check のコミットの器の閉包・正本・設計事実・方向の記録を
 28 |   `git show <コミット>:<置き場>` で今の版と照らし、順伝播を呼んだ数（守りが数えた値）が零で、升目のトークンの並びの SHA16 が手元で組んだ並びと同じことを見る。
 29 |   本の凍結は、下見の試みを session の終わりの時刻の順に並べ（与えた順と違えば止める）、試みごとに正本・npz・凍結の確かめを照らし、試みのコミットの凍結の記録と
 30 |   封印の記録の中身を今の記録と照らし、二つ以上の試みには逸脱の台帳のやり直しの記帳を求め、封印の記録の SHA16 と二つの予想の SHA-256 を本の凍結の記録に写す。
 31 | 用法: python tools/freeze_Bl3.py prepilot --words "<登録者の逐語>" --when "<日時（日本時間）>" --colab-check <相 check の出力の置き場> ／ prepilot --check-only
 32 |       python tools/freeze_Bl3.py main --words "<登録者の逐語>" --when "<日時（日本時間）>" --pilot <相 pilot の出力の置き場> [<二つ目> …]
 33 | 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 34 | """
 35 | import os, re, sys, ast, glob, json, shutil, hashlib, argparse, subprocess
 36 | 
 37 | HERE = os.path.dirname(os.path.abspath(__file__))
 38 | REPO = os.path.abspath(os.path.join(HERE, '..'))
 39 | sys.path.insert(0, HERE)
 40 | 
 41 | VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 相 check のコミットの版とトークンの並び・本の凍結の試みの順と由来・封印の写し・番号の数の比べ・inputs.files・転記行 F／v2（裁定 D231〜D235 の後）
 42 | NL = chr(10)
 43 | FR_JSON = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
 44 | FR_MD = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.md')
 45 | CC_SESSION = os.path.join(REPO, 'records', 'Bl3', 'colab-check-Bl3-session.json')
 46 | CC_CHECK = os.path.join(REPO, 'records', 'Bl3', 'colab-check-Bl3.json')
 47 | LEDGER = os.path.join(REPO, 'records', 'FREEZE-RECORD.md')
 48 | SEAL = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
 49 | TOOLS = ['tools/bl3_core.py', 'tools/bl3_run.py', 'tools/bl3_directions.py', 'tools/analyze_Bl3.py', 'tools/dry_run_Bl3.py', 'tools/colab/boot_Bl3.py',
 50 |          'tools/bl3_recompute_rewrite.py', 'tools/build_report_Bl3.py', 'tools/sweep_Bl3.py', 'tools/make_predictions_form_Bl3.py', 'tools/seal_Bl3.py',
 51 |          'tools/make_frozen_Bl3.py', 'tools/freeze_Bl3.py', 'tools/bl3_facts.py', 'tools/make_contrasts_Bl3.py', 'tools/build_draft_Bl3.py']
 52 | SELFTESTS = [('tools/bl3_core.py', ['--selftest']), ('tools/bl3_directions.py', ['--selftest']), ('tools/make_predictions_form_Bl3.py', ['--selftest']),
 53 |              ('tools/seal_Bl3.py', ['--selftest']), ('tools/build_report_Bl3.py', ['--selftest']), ('tools/make_frozen_Bl3.py', ['--selftest']),
 54 |              ('tools/bl3_recompute_rewrite.py', ['--selftest'])]
 55 | rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
 56 | P = lambda r: os.path.join(REPO, *r.split('/'))
 57 | sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 58 | CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
 59 | 
 60 | 
 61 | def sha256f(p):
 62 |     h = hashlib.sha256()
 63 |     with open(p, 'rb') as fh:
 64 |         for blk in iter(lambda: fh.read(1 << 24), b''):
 65 |             h.update(blk)
 66 |     return h.hexdigest().upper()
 67 | 
 68 | 
 69 | def import_closure(tools):
 70 |     """器が import する（関数の中の import も含む）手元の器の閉包。"""
 71 |     out, todo = set(), list(tools)
 72 |     while todo:
 73 |         t = todo.pop()
 74 |         if t in out:
 75 |             continue
 76 |         out.add(t)
 77 |         for node in ast.walk(ast.parse(open(P(t), encoding='utf-8').read())):
 78 |             names = []
 79 |             if isinstance(node, ast.Import):
 80 |                 names = [a.name.split('.')[0] for a in node.names]
 81 |             elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
 82 |                 names = [node.module.split('.')[0]]
 83 |             for n in names:
 84 |                 for cand in ('tools/%s.py' % n, 'tools/colab/%s.py' % n):
 85 |                     if os.path.exists(P(cand)) and cand not in out:
 86 |                         todo.append(cand)
 87 |     return sorted(out)
 88 | 
 89 | 
 90 | def frozen_files(T3):
 91 |     """凍結物（器の閉包を除く）: 正本・凍結の本文・設計事実・書式・方向・裁定と器の段の記録・読む記録（正本 `inputs.files`）。"""
 92 |     files = ['design/contrasts-Bl3.json', 'design/design-Bl3-FROZEN.md', 'design/design-Bl3-FROZEN.src.md', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md',
 93 |              'records/Bl3/numbers-lint-FROZEN-Bl3.md', 'records/Bl3/frozen-diff-Bl3.md', 'records/predictions/predictions-form-Bl3-v1.html', 'results/Bl3/directions-Bl3.json',
 94 |              'records/Bl3/tools/tools-log-Bl3.md', 'records/Bl3/tools/recompute-rewrite-dev-Bl3.md', 'records/Bl3/tools/recompute-rewrite-instructions-Bl3.md',
 95 |              'records/Bl3/exposure-before-seal-Bl3.md']
 96 |     files += sorted(rel(p) for p in glob.glob(P('records/Bl3/rulings-D*.md')))
 97 |     files += sorted(rel(p) for p in glob.glob(P('records/reviews/Bl3/impl/*.md')))
 98 |     files += [v['path'] for v in T3['inputs']['files'].values()]
 99 |     out = []
100 |     for f in files:
101 |         if f not in out:
102 |             out.append(f)
103 |     return out
104 | 
105 | 
106 | def latest_dry_run(T3):
107 |     dr = sorted(glob.glob(P('records/Bl3/dry-run-Bl3-*.md')))
108 |     if not dr:
109 |         return None, ['合成データの正式の記録が無い（records/Bl3/dry-run-Bl3-<日付>.md）']
110 |     txt = open(dr[-1], encoding='utf-8').read()
111 |     m = re.search(r'確かめ: (\d+) のうち (\d+) が期待どおり', txt)
112 |     n_iso = re.search(r'等方の方向の本数: (\d+)（正本 (\d+)）', txt)
113 |     res = {'path': rel(dr[-1]), 'checks': int(m.group(1)) if m else None, 'as_expected': int(m.group(2)) if m else None, 'iso': int(n_iso.group(1)) if n_iso else None}
114 |     bad = []
115 |     if not m or m.group(1) != m.group(2) or '**期待と違う**' in txt:
116 |         bad.append('合成データの記録に期待と違う確かめがある')
117 |     if not n_iso or int(n_iso.group(1)) != T3['nulls']['isotropic']['count']:
118 |         bad.append('合成データの正式の記録の等方の本数が正本と違う（正式の記録は正本の本数で走らせる）')
119 |     table = dict(re.findall(r'^\| ([^ |]+) \| ([0-9A-F]{16}) \|$', txt, flags=re.M))           # 記録の末尾の版の SHA16 の表（`tools/dry_run_Bl3.py` v2）
120 |     need = set(import_closure(TOOLS)) | {'design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json'}
121 |     lack = sorted(need - set(table))
122 |     differ = sorted(f for f, s16 in table.items() if not os.path.exists(P(f)) or sha16f(P(f)) != s16)
123 |     res['sha_table'] = {'files': len(table), 'lack': lack, 'differ': differ}
124 |     res['boot_phases'] = '起動器の三つの相' in txt
125 |     if not res['boot_phases']:
126 |         bad.append('合成データの正式の記録に、起動器の三つの相を別のプロセスで走らせた確かめが無い（裁定 D236）')
127 |     if lack:
128 |         bad.append('合成データの正式の記録の版の SHA16 の表が、器の閉包と正本・設計事実・方向の記録を覆わない: %s' % lack)
129 |     if differ:
130 |         bad.append('合成データの正式の記録を取った版と今の版が違う（取り直す）: %s' % differ)
131 |     return res, bad
132 | 
133 | 
134 | sha16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
135 | 
136 | 
137 | def local_ids_sha16(T3, FJ):
138 |     """手元のトークナイザで升目の入力を組み、トークンの並びの SHA16 を返す（相 check の値と照らす・裁定 D236）。"""
139 |     from transformers import AutoTokenizer
140 |     import bl3_run as BR
141 |     M_ = T3['inputs']['model']
142 |     tok = AutoTokenizer.from_pretrained(os.path.expanduser('~/.cache/huggingface/hub/models--%s/snapshots/%s' % (M_['repo'].replace('/', '--'), M_['rev'])))
143 |     keys = ['%s|%s' % tuple(c) for c in T3['cells_main']] + sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
144 |     return {k: BR.ids_sha16(c) for k, c in BR.build_cells(tok, T3, FJ, keys).items()}
145 | 
146 | 
147 | def prepilot_checks(colab_dir=None):
148 |     import make_frozen_Bl3 as MFB
149 |     import make_predictions_form_Bl3 as FORM
150 |     import bl3_core as K3
151 |     import bl3_directions as BD
152 |     import numpy as np
153 |     T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
154 |     FJ = json.load(open(P('records/Bl3/design-facts-Bl3.json'), encoding='utf-8'))
155 |     DJ = json.load(open(P('results/Bl3/directions-Bl3.json'), encoding='utf-8'))
156 |     res, bad = {}, []
157 |     canon16 = sha16f(P('design/contrasts-Bl3.json'))
158 |     # 凍結の本文
159 |     if not os.path.exists(MFB.FOUT):
160 |         bad.append('凍結の本文が無い（make_frozen_Bl3 を先に走らせる）')
161 |     else:
162 |         r_, b_ = MFB.rebuild_and_check(MFB.FSRC, MFB.FOUT)
163 |         res['frozen_text'] = {'canon_driven_lines': len(r_['canon_driven']), 'residual': None if r_['residual'] is None else len(r_['residual']), 'literal_fixes': len(MFB.LITERAL_FIXES)}
164 |         bad += b_
165 |         if '違反の合計: 0' not in open(MFB.LINT, encoding='utf-8').read():
166 |             bad.append('凍結の本文の数の検査に違反がある')
167 |     # 正本と設計事実と方向の記録
168 |     ruled = set()
169 |     for fp in glob.glob(P('records/Bl3/rulings-D*.md')):
170 |         m_ = re.fullmatch(r'rulings-D(\d+)(?:-D(\d+))?\.md', os.path.basename(fp))
171 |         if m_:
172 |             ruled |= {'D%d' % i for i in range(int(m_.group(1)), int(m_.group(2) or m_.group(1)) + 1)}
173 |     miss_d = sorted(ruled - set(T3['decisions']), key=lambda x: int(x[1:]))
174 |     nxt = ('D%d' % (max(int(x[1:]) for x in ruled) + 1)) if ruled else None
175 |     res['canon'] = {'version': T3['version'], 'sha16': canon16, 'rulings_recorded': len(ruled), 'missing_in_decisions': miss_d,
176 |                     'rulings_next': T3['numbering']['rulings_next'], 'rulings_next_expected': nxt}
177 |     if not ruled or miss_d:
178 |         bad.append('正本の decisions に、裁定の記録の番号が無い: %s' % miss_d)
179 |     if T3['numbering']['rulings_next'] != nxt:
180 |         bad.append('正本の次の裁定の番号 %s が、裁定の記録の次の番号 %s と違う' % (T3['numbering']['rulings_next'], nxt))
181 |     inp_bad = [k for k, v in T3['inputs']['files'].items() if v.get('sha16') and (not os.path.exists(P(v['path'])) or sha16f(P(v['path'])) != v['sha16'])]
182 |     res['inputs_files'] = {'checked': sum(1 for v in T3['inputs']['files'].values() if v.get('sha16')), 'bad': inp_bad}
183 |     if inp_bad:
184 |         bad.append('正本 inputs.files の SHA16 と今のファイルが違う: %s' % inp_bad)
185 |     M_ = T3['inputs']['model']
186 |     snap = os.path.expanduser('~/.cache/huggingface/hub/models--%s/snapshots/%s' % (M_['repo'].replace('/', '--'), M_['rev']))
187 |     if os.path.exists(os.path.join(snap, 'model.safetensors.index.json')):
188 |         shards = sorted(set(json.load(open(os.path.join(snap, 'model.safetensors.index.json'), encoding='utf-8'))['weight_map'].values()))
189 |         miss_f = [x for x in ['config.json', 'tokenizer.json', 'model.safetensors.index.json'] + shards if x not in FJ['facts']['F']['sha256']]
190 |         res['fact_F'] = {'shards': len(shards), 'missing': miss_f}
191 |         if miss_f:
192 |             bad.append('転記行 F に、重みの索引の断片か設定のファイルが欠けている: %s' % miss_f)
193 |     else:
194 |         bad.append('手元に重みの索引が無く、転記行 F の断片を確かめられない')
195 |     if FJ['contrasts_sha16'] != canon16 or DJ['contrasts_sha16'] != canon16:
196 |         bad.append('設計事実か方向の記録の正本の SHA16 が今の正本と違う（作り直す）')
197 |     # 方向の npz
198 |     npz = P(DJ['npz'])
199 |     npz_sha = sha256f(npz)
200 |     Z = np.load(npz)
201 |     try:
202 |         grp = BD.verify_against_facts({g: Z[g] for g in BD.GROUPS}, FJ)
203 |     except SystemExit as e_:
204 |         bad.append(str(e_))
205 |         grp = {}
206 |     rchk = subprocess.run([sys.executable, P('tools/bl3_directions.py'), '--check'], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO)
207 |     res['directions'] = {'npz': DJ['npz'], 'sha256': npz_sha, 'groups': grp, 'rebuild_bytes_equal': rchk.returncode == 0}
208 |     if npz_sha != DJ['npz_sha256'] or rchk.returncode != 0:
209 |         bad.append('方向の npz の SHA-256 が記録と違うか、作り直してバイトで同じにならない')
210 |     # 合成データ
211 |     res['dry_run'], b_ = latest_dry_run(T3)
212 |     bad += b_
213 |     # 器の自己検査
214 |     st = {}
215 |     for t, args in SELFTESTS:
216 |         r = subprocess.run([sys.executable, P(t)] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
217 |         st[t] = r.returncode == 0
218 |     res['selftests'] = st
219 |     bad += ['器の自己検査が落ちた: %s' % t for t, ok in st.items() if not ok]
220 |     # 予想の書式・封印はまだ無い
221 |     if not os.path.exists(FORM.OUT):
222 |         bad.append('予想の書式が無い（make_predictions_form_Bl3 を先に走らせる）')
223 |     else:
224 |         h = open(FORM.OUT, encoding='utf-8').read()
225 |         res['form'] = FORM.check(T3, h)
226 |         if ("contrasts:'%s'" % T3['version']) not in h:
227 |             bad.append('予想の書式の正本の版が今の正本と違う（組み直す）')
228 |     for p in ('records/predictions/predictions-Bl3-coordinator.json', 'records/predictions/predictions-Bl3-registrant.json', 'records/Bl3/sealing-record-Bl3.json'):
229 |         if os.path.exists(P(p)):
230 |             bad.append('封印が凍結より先にある（正本 predictions.when と違う）: %s' % p)
231 |     # 器の実装の検分
232 |     impl = sorted(glob.glob(P('records/reviews/Bl3/impl/adoption-table-*.md')))
233 |     res['impl_review'] = [rel(x) for x in impl]
234 |     if not impl:
235 |         bad.append('器の実装の検分の採否表が無い（records/reviews/Bl3/impl/・正本 review_plan.impl）')
236 |     # Colab の確かめ
237 |     if colab_dir is not None:
238 |         S = json.load(open(os.path.join(colab_dir, 'session.json'), encoding='utf-8'))
239 |         CK = json.load(open(os.path.join(colab_dir, 'check.json'), encoding='utf-8'))
240 |         pins = T3['inputs']['versions_B']
241 |         c = {'kind_check': S.get('kind') == 'bl3_colab_check', 'not_dry': S.get('dry') is False, 'no_forward': CK.get('forward_calls') == 0,
242 |              'versions': all((S.get('versions') or {}).get(k) == pins[k] for k in ('numpy', 'torch', 'transformers')),
243 |              'gpu': any(g in str(S.get('gpu')) for g in ('L4', 'A100')), 'weights': S.get('weights_sha256') == FJ['facts']['F']['sha256'],
244 |              'npz': S.get('directions_npz_sha256') == npz_sha, 'groups': (S.get('directions_group_sha256') or {}) == grp and bool(grp),
245 |              'cells': all((CK['cells'].get(k) or {}).get(x) == v[y] for k, v in FJ['facts']['B']['cells'].items() for x, y in (('prompt_len', 'prompt_len'), ('main_position', 'main_position'), ('readout_position', 'readout_position'), ('family', 'family'))),
246 |              'rewrite_importable': CK.get('rewrite_importable') is True, 'canon_at_commit': S.get('canon_sha16') == canon16,
247 |              'comparator_anchor': CK.get('comparator_anchor') == K3.comparator_anchor(DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'], K3.blens_own_pair()),
248 |              'static_norm': CK.get('static_norm_matches_fact_D') is True, 'forward_guards': (CK.get('forward_guards') or 0) > 0}
249 |         cm = S.get('commit') or ''
250 |         at_commit = [f for f in import_closure(TOOLS) + ['design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json']
251 |                      if sha16b(subprocess.run(['git', '-C', REPO, 'show', '%s:%s' % (cm, f)], capture_output=True).stdout) != sha16f(P(f))]
252 |         c['versions_at_commit'] = bool(re.fullmatch(r'[0-9a-f]{40}', cm)) and not at_commit
253 |         res['colab_check_versions_differ'] = at_commit
254 |         tok_local = local_ids_sha16(T3, FJ)
255 |         c['token_ids'] = all((CK['cells'].get(k) or {}).get('ids_sha16') == v for k, v in tok_local.items())
256 |         res['colab_check'] = dict(c, commit=S.get('commit'), gpu_name=S.get('gpu'), versions_seen=S.get('versions'))
257 |         bad += ['Colab の確かめ: %s' % k for k, v in c.items() if not v]
258 |     return T3, res, bad
259 | 
260 | 
261 | def prepilot(words, when, colab_dir, force=False):
262 |     T3, res, bad = prepilot_checks(colab_dir)
263 |     print(json.dumps({k: v for k, v in res.items() if k != 'selftests'}, ensure_ascii=False, indent=1, default=str)[:6000])
264 |     if bad:
265 |         raise SystemExit('下見の前の凍結の確かめが外れた（止める・登録者に相談）: %s' % bad)
266 |     if colab_dir is None:
267 |         print('[freeze_Bl3] 確かめだけ（Colab の確かめを除く）: 外れ無し')
268 |         return
269 |     if os.path.exists(FR_JSON) and not force:
270 |         raise SystemExit('既にある: %s' % rel(FR_JSON))
271 |     shutil.copyfile(os.path.join(colab_dir, 'session.json'), CC_SESSION)
272 |     shutil.copyfile(os.path.join(colab_dir, 'check.json'), CC_CHECK)
273 |     tools = import_closure(TOOLS)
274 |     files = frozen_files(T3) + [res['dry_run']['path'], rel(CC_SESSION), rel(CC_CHECK)]
275 |     frozen = {r: sha16f(P(r)) for r in files + tools}
276 |     R = {'kind': 'bl3_freeze_record', 'version': VERSION, 'stage': 'prepilot', 'frozen_jst': when, 'registrant_words': words, 'rulings': sorted((k for k in T3['decisions'] if int(k[1:]) >= 204), key=lambda x: int(x[1:])),
277 |          'frozen_sha16': frozen, 'tools_import_closure': tools, 'directions_npz_sha256': res['directions']['sha256'], 'checks': res,
278 |          'deviation_rule': '凍結の後の変更は、逸脱として番号・日付・理由・登録者の承認を台帳（この記録の deviations）に記す。器の差分は tool_diffs に置き場・前・後の SHA16 を記す（正本 computation.main_freeze_check）',
279 |          'deviations': [],
280 |          'next': '記録先行の公開（push）→ 予想の封印（コーディネータが先・SHA だけを伝える → 登録者）→ Colab の相 pilot → 本の凍結（下見の記録と機械の決定を足す）→ Colab の相 main → 一致だけを見る段 → 結果を登録者と一緒に開く',
281 |          'clause': CLAUSE}
282 |     json.dump(R, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
283 |     md = ['# B-lens 層三の下見の前の凍結の記録（機械生成・`tools/freeze_Bl3.py` %s）' % VERSION, '',
284 |           '- 凍結: %s（日本時間）・登録者の言葉は逐語で「%s」。' % (when, words),
285 |           '- 本文: `design/design-Bl3-FROZEN.md`（SHA16 %s）・草案3 との差は `records/Bl3/frozen-diff-Bl3.md`。' % frozen['design/design-Bl3-FROZEN.md'],
286 |           '- 正本: 版 %s（SHA16 %s）。方向の npz: `%s`（SHA-256 %s）。' % (T3['version'], frozen['design/contrasts-Bl3.json'], res['directions']['npz'], res['directions']['sha256']),
287 |           '- Colab の確かめ（相 check・コミット %s・%s）: %s。' % (res['colab_check']['commit'], res['colab_check']['gpu_name'], '・'.join('%s %s' % (k, '合う' if v else '外れ') for k, v in res['colab_check'].items() if isinstance(v, bool))),
288 |           '- 合成データ: `%s`（確かめ %s・期待どおり %s）。' % (res['dry_run']['path'], res['dry_run']['checks'], res['dry_run']['as_expected']),
289 |           '- 次: ' + R['next'], '', '## 凍結物の SHA16', '', '| 置き場 | SHA16 |', '|---|---|'] + ['| `%s` | %s |' % kv for kv in sorted(frozen.items())] + ['', CLAUSE, '']
290 |     open(FR_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(md))
291 |     row = ('| %s | **B-lens 層三 下見の前の凍結**（登録者「%s」%s 日本時間・裁定 D210）: 草案3 の原稿に裁定 D226 の §2 の直しを入れ、正本から来る行とともに design/design-Bl3-FROZEN.md を組み（裁定 D228）、正本・方向の npz・器を凍結した。'
292 |            '凍結の記録 records/Bl3/FREEZE-RECORD-Bl3.json（凍結物 %d 件・器の閉包 %d）。封印はこの後（コーディネータが先）。 | design/design-Bl3-FROZEN.md | %s | 凍結の後の変更は逸脱として台帳に記す |'
293 |            % (when.split(' ')[0], words, when, len(frozen), len(tools), frozen['design/design-Bl3-FROZEN.md']))
294 |     led = open(LEDGER, encoding='utf-8').read()
295 |     if 'B-lens 層三 下見の前の凍結' not in led:
296 |         open(LEDGER, 'a', encoding='utf-8', newline=NL).write(('' if led.endswith(NL) else NL) + row + NL)
297 |     print('[freeze_Bl3] 下見の前の凍結を記帳した: %s・%s（凍結物 %d）' % (rel(FR_JSON), rel(FR_MD), len(frozen)))
298 | 
299 | 
300 | def in_commit(commit, path):
301 |     return subprocess.run(['git', '-C', REPO, 'cat-file', '-e', '%s:%s' % (commit, path)], capture_output=True).returncode == 0
302 | 
303 | 
304 | def main_freeze_checks(FR, pilot_dirs):
305 |     bad, res = [], {}
306 |     frozen = FR['frozen_sha16']
307 |     canon = 'design/contrasts-Bl3.json'
308 |     if sha16f(P(canon)) != frozen[canon]:
309 |         bad.append('正本の SHA16 が下見の前の凍結から変わった（正本を変える直しは本の凍結の決まりの外・登録者に上げる）')
310 |     ledgered = {}
311 |     for d in FR.get('deviations') or []:
312 |         for td in d.get('tool_diffs') or []:
313 |             ledgered[td['path']] = td
314 |     now_sha = {}
315 |     for pth, want in frozen.items():
316 |         got = sha16f(P(pth)) if os.path.exists(P(pth)) else None
317 |         now_sha[pth] = got
318 |         if got != want:
319 |             td = ledgered.get(pth)
320 |             if not td or td.get('before') != want or td.get('after') != got:
321 |                 bad.append('凍結物の SHA16 の違いが逸脱の台帳の器の差分と合わない: %s（凍結 %s・今 %s）' % (pth, want, got))
322 |     res['changed'] = sorted(p for p in frozen if now_sha[p] != frozen[p])
323 |     res['ledgered_not_changed'] = sorted(p for p in ledgered if now_sha.get(p) == frozen.get(p))
324 |     if res['ledgered_not_changed']:
325 |         bad.append('台帳に記した器の差分が凍結物に現れない: %s' % res['ledgered_not_changed'])
326 |     atts, sessions, fin = [], [], []
327 |     for d in pilot_dirs:
328 |         PJ = json.load(open(os.path.join(d, 'pilot.json'), encoding='utf-8'))
329 |         S = json.load(open(os.path.join(d, 'session.json'), encoding='utf-8'))
330 |         if S.get('dry') or S.get('kind') != 'bl3_colab_pilot':
331 |             bad.append('下見の試みの出力が DRY か、相 pilot の出力でない: %s' % d)
332 |         c = S.get('commit') or ''
333 |         if not (re.fullmatch(r'[0-9a-f]{40}', c) and in_commit(c, 'records/Bl3/FREEZE-RECORD-Bl3.json') and in_commit(c, 'records/Bl3/sealing-record-Bl3.json')):
334 |             bad.append('下見の試みのコミットが、凍結の記録と封印の記録を含むコミットでない: %s' % c)
335 |         if S.get('canon_sha16') != frozen.get(canon) or S.get('directions_npz_sha256') != FR.get('directions_npz_sha256') or ((S.get('frozen_check') or {}).get('bad') or []):
336 |             bad.append('下見の試みの session の正本か npz か凍結の確かめが、凍結の記録と合わない: %s' % d)
337 |         if re.fullmatch(r'[0-9a-f]{40}', c):
338 |             # 封印の記録は封印の後に変わらないので、まるごと照らす。凍結の記録は台帳（deviations）が足されうるので、凍結物の SHA16 の表と npz の SHA-256 を照らす
339 |             if sha16b(subprocess.run(['git', '-C', REPO, 'show', '%s:records/Bl3/sealing-record-Bl3.json' % c], capture_output=True).stdout) != sha16f(SEAL):
340 |                 bad.append('下見の試みのコミットの封印の記録が、今の封印の記録と違う: %s' % c)
341 |             try:
342 |                 FRc = json.loads(subprocess.run(['git', '-C', REPO, 'show', '%s:records/Bl3/FREEZE-RECORD-Bl3.json' % c], capture_output=True).stdout.decode('utf-8'))
343 |             except Exception:
344 |                 FRc = {}
345 |             if FRc.get('frozen_sha16') != frozen or FRc.get('directions_npz_sha256') != FR.get('directions_npz_sha256'):
346 |                 bad.append('下見の試みのコミットの凍結の記録の凍結物か npz が、今の凍結の記録と違う: %s' % c)
347 |         atts.append(PJ['pilot'])
348 |         fin.append(S.get('finished') or '')
349 |         sessions.append({k: S.get(k) for k in ('commit', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'finished')})
350 |     if fin != sorted(fin) or not all(fin):
351 |         bad.append('下見の試みの与えた順が、session の終わりの時刻の順と違う（または時刻が無い）: %s' % fin)
352 |     reruns = [x for x in FR.get('deviations') or [] if x.get('kind') == 'pilot_rerun']
353 |     if len(atts) >= 2 and len(reruns) < len(atts) - 1:
354 |         bad.append('下見の試みが二つ以上あるのに、逸脱の台帳にやり直しの記帳（kind pilot_rerun）が足りない: 試み %d・記帳 %d' % (len(atts), len(reruns)))
355 |     SR = json.load(open(SEAL, encoding='utf-8')) if os.path.exists(SEAL) else {}
356 |     # 封印の記録にある凍結の記録の SHA16 は、封印の記録を足したコミットの凍結の記録と照らす（封印の後に逸脱を台帳に記すと、今の凍結の記録は変わりうるため）
357 |     sc_ = subprocess.run(['git', '-C', REPO, 'log', '--diff-filter=A', '--format=%H', '-1', '--', 'records/Bl3/sealing-record-Bl3.json'], capture_output=True, text=True).stdout.strip()
358 |     if not sc_:
359 |         bad.append('封印の記録を足したコミットが無い（封印の記録をコミットしてから本の凍結）')
360 |     elif sha16b(subprocess.run(['git', '-C', REPO, 'show', '%s:records/Bl3/FREEZE-RECORD-Bl3.json' % sc_], capture_output=True).stdout) != SR.get('freeze_record_sha16'):
361 |         bad.append('封印の記録にある凍結の記録の SHA16 が、封印の記録を足したコミットの凍結の記録と違う')
362 |     pre = {}
363 |     for role, v in (SR.get('predictions') or {}).items():
364 |         pre[role] = sha256f(P(v['path'])) if os.path.exists(P(v['path'])) else None
365 |         if pre[role] != v.get('sha256'):
366 |             bad.append('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
367 |     res['seal'] = {'record_sha16': sha16f(SEAL) if os.path.exists(SEAL) else None, 'predictions_sha256': pre}
368 |     if not atts:
369 |         bad.append('下見の試みが無い')
370 |     elif atts[-1].get('tool_error'):
371 |         bad.append('最後の下見の試みが器の誤り（本の凍結の前に登録者の裁定を仰ぐ）')
372 |     res['n_attempts'] = len(atts)
373 |     return atts, sessions, now_sha, res, bad
374 | 
375 | 
376 | def main_freeze(words, when, pilot_dirs):
377 |     FR = json.load(open(FR_JSON, encoding='utf-8'))
378 |     if 'main_freeze' in FR:
379 |         raise SystemExit('本の凍結は既にある')
380 |     if not os.path.exists(SEAL):
381 |         raise SystemExit('封印の記録が無い（本の凍結は封印と下見の後）')
382 |     atts, sessions, now_sha, res, bad = main_freeze_checks(FR, pilot_dirs)
383 |     print(json.dumps(res, ensure_ascii=False, indent=1))
384 |     if bad:
385 |         raise SystemExit('本の凍結の確かめが外れた（止める・登録者に相談）: %s' % bad)
386 |     before = {k: v for k, v in FR.items()}
387 |     FR['main_freeze'] = {'frozen_jst': when, 'registrant_words': words, 'pilot_attempts': atts, 'pilot': atts[-1], 'decision': atts[-1].get('decision'),
388 |                          'sessions': sessions, 'frozen_sha16': now_sha, 'tool_diffs_applied': res['changed'], 'seal': res['seal'], 'freeze_tool': 'tools/freeze_Bl3.py %s' % VERSION}
389 |     assert all(FR[k] == before[k] for k in before), '本の凍結でほかの鍵が変わった'
390 |     assert set(FR) - set(before) == {'main_freeze'}
391 |     json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
392 |     dec = atts[-1].get('decision') or {}
393 |     add = ['', '## 本の凍結（下見の記録と機械の決定を足した・正本 computation.main_freeze_check）', '',
394 |            '- 本の凍結: %s（日本時間）・登録者の言葉は逐語で「%s」。' % (when, words),
395 |            '- 下見の試み %d・最後の試みの機械の決定: %s（外した升目: %s）。' % (len(atts), dec.get('q1'), '・'.join(dec.get('dropped') or []) or 'なし'),
396 |            '- 凍結物の SHA16 の違い（逸脱の台帳の器の差分と一致）: %s。' % ('・'.join(res['changed']) or '無し'), '', CLAUSE, '']
397 |     md = open(FR_MD, encoding='utf-8').read().rstrip(NL)
398 |     if md.endswith(CLAUSE):
399 |         md = md[: -len(CLAUSE)].rstrip(NL)
400 |     open(FR_MD, 'w', encoding='utf-8', newline=NL).write(md + NL + NL.join(add))
401 |     row = ('| %s | **B-lens 層三 本の凍結**（登録者「%s」%s 日本時間・裁定 D210・D222）: 下見の記録と機械の決定（%s）を凍結の記録に足した。器の差分 %d（逸脱の台帳と一致）。 | records/Bl3/FREEZE-RECORD-Bl3.json | %s | 以後の変更は逸脱として台帳に記す |'
402 |            % (when.split(' ')[0], words, when, dec.get('q1'), len(res['changed']), sha16f(FR_JSON)))
403 |     led = open(LEDGER, encoding='utf-8').read()
404 |     if 'B-lens 層三 本の凍結' not in led:
405 |         open(LEDGER, 'a', encoding='utf-8', newline=NL).write(('' if led.endswith(NL) else NL) + row + NL)
406 |     print('[freeze_Bl3] 本の凍結を記帳した: %s（下見の試み %d）' % (rel(FR_JSON), len(atts)))
407 | 
408 | 
409 | def main():
410 |     ap = argparse.ArgumentParser()
411 |     ap.add_argument('stage', choices=['prepilot', 'main'])
412 |     ap.add_argument('--words')
413 |     ap.add_argument('--when')
414 |     ap.add_argument('--colab-check', help='相 check の出力の置き場（session.json と check.json）')
415 |     ap.add_argument('--check-only', action='store_true')
416 |     ap.add_argument('--pilot', nargs='*', help='相 pilot の出力の置き場（試みの順）')
417 |     ap.add_argument('--force', action='store_true')
418 |     a = ap.parse_args()
419 |     if a.stage == 'prepilot':
420 |         if a.check_only:
421 |             return prepilot(None, None, None)
422 |         if not (a.words and a.when and a.colab_check):
423 |             raise SystemExit('--words・--when・--colab-check が要る')
424 |         return prepilot(a.words, a.when, a.colab_check, a.force)
425 |     if not (a.words and a.when and a.pilot):
426 |         raise SystemExit('--words・--when・--pilot が要る')
427 |     main_freeze(a.words, a.when, a.pilot)
428 | 
429 | 
430 | if __name__ == '__main__':
431 |     main()
```
<<< 終: `tools/freeze_Bl3.py` >>>
