（B-lens 層三の器の直しの確かめの束・分けた版 2／7・中身は一通版と同じ）

<<< 始: `tools/build_report_Bl3.py` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/tools/build_report_Bl3.py b/tools/build_report_Bl3.py
index 8010be3..d4b73a1 100644
--- a/tools/build_report_Bl3.py
+++ b/tools/build_report_Bl3.py
@@ -1,5 +1,5 @@
 # -*- coding: utf-8 -*-
-"""build_report_Bl3.py v2 —— B-lens 層三（Bl3）の結果の報告の草案を組む（2026-09-25・正本 `reading_rules`・`negation_templates`・`report_rules`・`labels`・`limits`）。
+"""build_report_Bl3.py v3 —— B-lens 層三（Bl3）の結果の報告の草案を組む（2026-09-25・正本 `reading_rules`・`negation_templates`・`report_rules`・`labels`・`limits`）。
 
 組み立て（B-lens の組み立ての器 `tools/build_report_Blens.py` の型）:
   - 数はすべて機械の区画（凍結の走査器 `tools/report_lint.py` の区画の印）の中に置く。区画ごとの中身の SHA16 を別の記録（報告と同じ名の -machine.json）に書く。
@@ -30,7 +30,7 @@ REPO = os.path.abspath(os.path.join(HERE, '..'))
 sys.path.insert(0, HERE)
 import report_lint as RL
 
-VERSION = 'v2'          # v2（2026-09-25・裁定 D231〜D235）: 偶然の目安は外した後の行で・効き目の側は全ての行で・(iii) の定義・二段の判定の書き方・本の計算は近道を使わない・合成の自己検査は外した升目の組を持たない
+VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 封印した予想と凍結の記録と手元の器を照らしてから組む・(v) の行の言い方・門の行だけの升目の外し・nuclear の族の文を §0 に・下見の GPU・自己検査の足し／v2（裁定 D231〜D235）
 NL = chr(10)
 OUT = os.path.join(REPO, 'records', 'Bl3', 'results-Bl3.md')
 FENCE = '本報告のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
@@ -70,6 +70,13 @@ def stop_sentence(T3, reason):
     return q[1] if reason == 'vi_b' else q[0]
 
 
+def dropped_split(T3, dec):
+    """下見で外した升目を、主の升目と門の行だけの升目に分ける（裁定 D236）。"""
+    main_cells = {'%s|%s' % tuple(c) for c in T3['cells_main']}
+    d = list((dec or {}).get('dropped') or [])
+    return [c for c in d if c in main_cells], [c for c in d if c not in main_cells]
+
+
 def reading_types(T3, A):
     """読みの表の条件を当てる（型は重なりうる）。戻り値: [(型, 当たった所, 書くこと)]。"""
     RR = {r['type']: r for r in T3['reading_rules']}
@@ -80,8 +87,9 @@ def reading_types(T3, A):
         if last.get('tool_error'):
             return [('器の誤り', '下見', '器の誤りで下見を終えられなかった（正本 pilot.decision.tool_error）')]
         return [('下見で止めた', '下見の決め', RR['下見で止めた']['write'] + '（この下見で当たる文:「%s」）' % stop_sentence(T3, dec.get('reason')))]
-    if dec.get('dropped'):
-        hits.append(('下見で一部を外した', '・'.join(dec['dropped']), RR['下見で一部を外した']['write']))
+    md_, gd_ = dropped_split(T3, dec)
+    if md_:                                                            # 主の升目を外したときだけ（門の行だけの升目の外しは §0 の機械の行・裁定 D236）
+        hits.append(('下見で一部を外した', '・'.join(md_), RR['下見で一部を外した']['write']))
     if last.get('iv'):
         hits.append(('揺れの版の値', '下見の (iv)', RR['揺れの版の値']['write']))
     rows = A['rows']
@@ -127,7 +135,8 @@ def pilot_lines(T3, rec, MB, title):
     rows += ['', '- (iii) 較正（記述）: 順位相関 %s・升目 %s・文: %s' % (f4(rec['iii']['rho']), rec['iii']['n'], T3['pilot']['iii_sentences'][rec['iii']['sentence']])]
     for name, v in (rec.get('iv') or {}).items():
         rows.append('- (iv) 揺れの版 %s: %s' % (name, '・'.join('%s %s（主との差 %s%s）' % (c, f4(x), f4(x - rec['cells'][c]['lo']), '・印' if v['flags'][c] else '') for c, x in v['lo'].items())))
-    rows.append('- (v) 近道の確かめ（無操作の対数オッズの差）: %s・許容 %s・近道を使う: %s' % ('・'.join('%s %s' % (c, f4(d)) for c, d in rec['v']['diffs'].items()), f4(rec['v']['tol']), yn(rec['v']['shortcut'])))
+    rows.append('- (v) 近道の差（無操作の対数オッズの差・記述・本の計算は近道を使わない・裁定 D234）: %s・近道の許容 %s・差がすべて許容の内: %s' % (
+        '・'.join('%s %s' % (c, f4(d)) for c, d in rec['v']['diffs'].items()), f4(rec['v']['tol']), yn(rec['v']['shortcut'])))
     rows.append('- 機械の決定: %s・(i)(ii) を満たす主の升目 %s／%s・外した升目: %s' % (dec.get('q1'), dec.get('n_pass'), dec.get('n_main'), '・'.join(dec.get('dropped') or []) or 'なし'))
     fam = [k for k in (dec.get('dropped') or []) if k.startswith('N1|')]
     if len(fam) >= 2:
@@ -165,7 +174,10 @@ def build(T3, A, preds, meta, deviations=(), marks=None, rejected=None, confirma
     L += ['', '**答えの範囲**:', ''] + machine(['- ' + T3['scope']['reach'], '- ' + T3['negation_templates'][2]], MB)
     last = atts[-1]
     dec = last.get('decision') or {}
-    L += ['', '**下見の機械の決定**:', ''] + machine(['- %s' % ('器の誤りで下見を終えられなかった' if last.get('tool_error') else '%s（外した升目: %s）' % (dec.get('q1'), '・'.join(dec.get('dropped') or []) or 'なし'))]
+    md_, gd_ = dropped_split(T3, dec)
+    L += ['', '**下見の機械の決定**:', ''] + machine(['- %s' % ('器の誤りで下見を終えられなかった' if last.get('tool_error') else '%s（外した主の升目: %s）' % (dec.get('q1'), '・'.join(md_) or 'なし'))]
+                                                    + (['- 門の行だけの升目を外した: %s（門の行と入れ替えの数を数え直した・主の札の行は外していない・正本 pilot.decision.gate_only）' % '・'.join(gd_)] if gd_ and not last.get('tool_error') else [])
+                                                    + (['- nuclear の族は測れなかった（正本 pilot.decision.family）'] if len([k for k in md_ if k.startswith('N1|')]) >= 2 else [])
                                                     + ([] if last.get('tool_error') or (dec.get('stop') and dec.get('reason') == 'vi_b') else
                                                        ['- (iii) の文: ' + T3['pilot']['iii_sentences'][last['iii']['sentence']]]), MB)
     if main_tool_error:
@@ -288,6 +300,8 @@ def main_sections(T3, A, MB, mk):
     if (rc.get('second') or {}).get('values_beyond_tol') and (rc.get('second') or {}).get('agree'):
         r.append('- 二段目は効き目の差の最大が許容の外で、札は同じだった。止めずに逸脱の台帳に記した（正本 `independent_recompute.agreement`・裁定 D234）')
     r.append('- 組の間の環境: %s' % ('同じ' if (A.get('env') or {}).get('same') else '違う（%s）' % json.dumps((A.get('env') or {}).get('diff'), ensure_ascii=False)))
+    if 'pilot_gpu' in (A.get('env') or {}):
+        r.append('- 下見の GPU: %s・本の計算の組の GPU と同じ: %s（揺れの床は下見の GPU で決まる・裁定 D236）' % ('・'.join(A['env']['pilot_gpu']), yn(A['env'].get('gpu_same_as_pilot'))))
     L += machine(r, MB)
     return L
 
@@ -303,11 +317,32 @@ def lint_report(text, T3):
     return RL.lint(text, T_scan, frozenset(), sidecar=side), side
 
 
+def sealed_and_frozen_bad(FR, seal):
+    """報告を組む前の確かめ（裁定 D236・B-lens の `require_sealed` の型）: 二つの予想の SHA-256 が封印の記録と同じ・封印の記録の SHA16 と二つの予想の SHA-256 が
+    本の凍結の記録に写した値と同じ・手元の器と正本と設計事実と方向の記録が本の凍結の記録と同じ（台帳に記した差分は許す）。戻り値: 外れの並び。"""
+    import analyze_Bl3 as AZ
+    bad = []
+    for role, v in seal['predictions'].items():
+        pp = P(v['path'])
+        if not os.path.exists(pp) or hashlib.sha256(open(pp, 'rb').read()).hexdigest().upper() != v['sha256']:
+            bad.append('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
+    ms = (FR.get('main_freeze') or {}).get('seal') or {}
+    if ms.get('record_sha16') != sha16f(P('records/Bl3/sealing-record-Bl3.json')):
+        bad.append('封印の記録の SHA16 が、本の凍結の記録に写した値と違う')
+    if any((ms.get('predictions_sha256') or {}).get(r) != v['sha256'] for r, v in seal['predictions'].items()):
+        bad.append('本の凍結の記録に写した予想の SHA-256 が、封印の記録と違う')
+    bad += ['手元の器か正本が本の凍結の記録と違う: %s' % x for x in AZ.frozen_versions_bad(FR, REPO)]
+    return bad
+
+
 def load_inputs(main_tool_error=False):
     import sweep_Bl3 as SW
     T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
     FR = json.load(open(P('records/Bl3/FREEZE-RECORD-Bl3.json'), encoding='utf-8'))
     seal = json.load(open(P('records/Bl3/sealing-record-Bl3.json'), encoding='utf-8'))
+    bad = sealed_and_frozen_bad(FR, seal)
+    if bad:
+        raise SystemExit('報告を組む前の確かめが外れた（止める・登録者に相談）: %s' % bad)
     preds = {r: json.load(open(P(v['path']), encoding='utf-8')) for r, v in seal['predictions'].items()}
     ap_ = P('records/Bl3/analysis-Bl3.json')
     atts = FR['main_freeze']['pilot_attempts']
@@ -388,7 +423,8 @@ def synth_analysis(T3, FJ, DJ, seed=3, n_iso=199, stop=None, drop=()):
              'cells': {k: {'lo': -2.0, 'pa': 0.1, 'mass': 0.95, 'pa_transformed': 0.05, 'stage_b_rate': 0.2, 'pass_i_ii': k not in drop, 'main': True} for k in cell_keys},
              'iii': {'rho': 0.3, 'n': len(cell_keys), 'sentence': 'positive'}, 'iv': {'V1': {'lo': {k: -1.9 for k in cell_keys}, 'flags': {k: False for k in cell_keys}}},
              'v': {'diffs': {k: 1e-4 for k in cell_keys}, 'tol': 0.005, 'shortcut': True},
-             'decision': K.cells_decision({k: k not in drop for k in cell_keys}, {}, T3['pilot']['decision']['cells_min_pass'])}
+             'decision': K.cells_decision({k: k not in drop for k in cell_keys}, {g: g not in drop for g in sorted({'%s|%s' % (x[0], x[1]) for x in gate_only})},
+                                          T3['pilot']['decision']['cells_min_pass'])}
     if stop == 'vi_b':
         pilot['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
         for k in ('iii', 'iv', 'v', 'cells'):
@@ -413,12 +449,14 @@ def synth_analysis(T3, FJ, DJ, seed=3, n_iso=199, stop=None, drop=()):
     A.update({'dry': True, 'pilot_attempts': [pilot], 'head': {'logit_check': {'max_abs': 0.05, 'tol': 0.5, 'pass': True},
                                                                'shortcut': False, 'layer_check': {'diff': 0.0, 'tol': 1e-4, 'pass': True}},
               'main_run': {'batch': 16, 'shortcut': False, 'dropped': pilot['decision']['dropped']},
-              'layerwise': {k: {'noop_lo': {}, 'rows': {}, 'iso_summary': None} for k in cells_out if k in main_keys},
+              'layerwise': {k: {'noop_lo': {'2': -2.0, '3': -2.0}, 'rows': {u: [[1.0, 0.9, 0.1], [1.1, 0.8, 0.1]] for u in list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]},
+                                'iso_summary': {'median': [[1.0, 0.0, 0.0]] * 2, 'lo': [[0.5, -0.1, -0.1]] * 2, 'hi': [[1.5, 0.1, 0.1]] * 2, 'n': n_iso}} for k in cells_out if k in main_keys},
+              'n_iso': n_iso,
               'gate_rows': [], 'style_rows': style_rows, 'stage_b_notes': AZ.stage_b_notes(T3, AN, rows_gate),
               'secondary': {'counts': {'row_passes': 1, 'sign_batches': 1, 'contexts': 1}, 'contexts_run': 1,
                             'summary': {'S1|O-Ncold-v|static': dict({k: {'mean': 0.1, 'median': 0.1, 'q1': 0.0, 'q3': 0.2, 'n': 20} for k in ('dlo', 'dz_a', 'dz_c')},
                                                                      blens_direct={k: {'mean': x, 'median': x, 'q1': x, 'q3': x} for k, x in (('dlogit_exact_a', 0.1), ('dlogit_exact_c', -0.1))})}},     # B-lens の層二の値と同じ形（文脈の間の要約）
-              'sessions': {}, 'env': {'same': True, 'diff': {}}})
+              'sessions': {}, 'env': {'same': True, 'diff': {}, 'strict': [], 'pilot_gpu': ['NVIDIA L4'], 'gpu_same_as_pilot': True}})
     return A
 
 
@@ -455,7 +493,60 @@ def _selftest():
     td = build(T3, Ad, preds, meta, rejected='起草者の行（合成）')
     Vd, _ = lint_report(td, T3)
     assert Vd == [] and '〈下見で一部を外した〉' in td and Ad['rows_meta']['m_rows'] < len(T3['main_rows']), Vd[:3]
-    print('[build_report_Bl3] 自己検査 OK（合成の報告の走査の違反 0・起草者の欄が空なら埋め残し・禁止語と未登録の数は止まる・掃き出しは欠けを捕まえる・止まった下見と外した升目の組み立て）')
+    # 門の行だけの升目だけを外したとき: 〈下見で一部を外した〉は当たらず、§0 に門の行だけの升目の外しの行が出る（裁定 D236）
+    go_ = sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
+    Ag = synth_analysis(T3, FJ, DJ, drop=tuple(go_))
+    tg = build(T3, Ag, preds, meta, rejected='起草者の行（合成）')
+    Vg, _ = lint_report(tg, T3)
+    assert Vg == [] and '〈下見で一部を外した〉' not in tg and '門の行だけの升目を外した' in tg and SW.sweep(T3, Ag) == [], Vg[:3]
+    # 等方の外の行が出る枝（等方を正本の本数に・裁定 D236・器の実装の検分の R1-m5）: 掃き出し・走査・読みの型・q7
+    Ao = synth_analysis(T3, FJ, DJ, n_iso=T3['nulls']['isotropic']['count'])
+    to_ = build(T3, Ao, preds, meta, rejected='起草者の行（合成）')
+    Vo, _ = lint_report(to_, T3)
+    n_out = sum(1 for o in Ao['rows'].values() if o['iso_outside'])
+    assert n_out > 0 and Vo == [] and SW.sweep(T3, Ao) == [] and ('〈両方の外〉' in to_ or '〈埋もれる〉' in to_) and Ao['q7_rows'], (n_out, Vo[:3])
+    # 封印した予想を書き換えると、報告を組む前の確かめが止める（一時の置き場の写しで・裁定 D236・器の実装の検分の R2-重大1）
+    _selftest_sealed(T3, FJ, DJ)
+    print('[build_report_Bl3] 自己検査 OK（合成の報告の走査の違反 0・起草者の欄が空なら埋め残し・禁止語と未登録の数は止まる・掃き出しは欠けを捕まえる・止まった下見と外した升目の組み立て・'
+          '門の行だけの升目の外し・等方の外の行の枝 %d 行・書き換えた予想で止まる）' % n_out)
+
+
+def _selftest_sealed(T3, FJ, DJ):
+    """一時の置き場に、正本・設計事実・方向の記録・照らす器・予想・封印の記録・凍結の記録を置き、報告の入力を読む。予想を一字変えると止まることを確かめる。"""
+    import tempfile, shutil
+    import analyze_Bl3 as AZ
+    global REPO
+    keep = REPO
+    A = synth_analysis(T3, FJ, DJ)                                  # 段階 B の記録を読むので、置き場を切り替える前に作る
+    td = tempfile.mkdtemp(prefix='report-sealed-')
+    try:
+        for f in AZ.FROZEN_CHECK:
+            os.makedirs(os.path.dirname(os.path.join(td, *f.split('/'))), exist_ok=True)
+            shutil.copyfile(os.path.join(keep, *f.split('/')), os.path.join(td, *f.split('/')))
+        REPO = td
+        pdir = P('records/predictions')
+        os.makedirs(pdir, exist_ok=True)
+        pr = {}
+        for role in ('coordinator', 'registrant'):
+            pp = os.path.join(pdir, 'predictions-Bl3-%s.json' % role)
+            open(pp, 'w', encoding='utf-8', newline='\n').write(json.dumps({'q1.pilot': '続ける', 'q4.gate': '通らない'}, ensure_ascii=False))
+            pr[role] = {'path': 'records/predictions/predictions-Bl3-%s.json' % role, 'sha256': hashlib.sha256(open(pp, 'rb').read()).hexdigest().upper()}
+        json.dump({'predictions': pr}, open(P('records/Bl3/sealing-record-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
+        json.dump(A, open(P('records/Bl3/analysis-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
+        FR = {'main_freeze': {'pilot_attempts': A['pilot_attempts'], 'frozen_sha16': {f: sha16f(P(f)) for f in AZ.FROZEN_CHECK},
+                              'seal': {'record_sha16': sha16f(P('records/Bl3/sealing-record-Bl3.json')), 'predictions_sha256': {r: v['sha256'] for r, v in pr.items()}}}, 'deviations': []}
+        json.dump(FR, open(P('records/Bl3/FREEZE-RECORD-Bl3.json'), 'w', encoding='utf-8'), ensure_ascii=False)
+        load_inputs()                                                  # 書き換える前は通る
+        pp = P('records/predictions/predictions-Bl3-coordinator.json')
+        open(pp, 'w', encoding='utf-8', newline='\n').write(json.dumps({'q1.pilot': '続ける', 'q4.gate': '通る'}, ensure_ascii=False))
+        try:
+            load_inputs()
+            raise AssertionError('書き換えた予想で報告を組もうとした')
+        except SystemExit as e_:
+            assert '封印した予想' in str(e_), e_
+    finally:
+        REPO = keep
+        shutil.rmtree(td, ignore_errors=True)
 
 
 if __name__ == '__main__':
````
<<< 終: `tools/build_report_Bl3.py` の差分 >>>

<<< 始: `tools/seal_Bl3.py` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/tools/seal_Bl3.py b/tools/seal_Bl3.py
index eee4ae6..8aeb3ea 100644
--- a/tools/seal_Bl3.py
+++ b/tools/seal_Bl3.py
@@ -1,5 +1,5 @@
 # -*- coding: utf-8 -*-
-"""seal_Bl3.py v1 —— B-lens 層三（Bl3）の予想の封印（2026-09-25・正本 `predictions.order`・`predictions.when`: 下見の前の凍結の後・下見の前に、コーディネータが先に封印して
+"""seal_Bl3.py v2 —— B-lens 層三（Bl3）の予想の封印（2026-09-25・正本 `predictions.order`・`predictions.when`: 下見の前の凍結の後・下見の前に、コーディネータが先に封印して
 SHA だけを伝え、登録者はコーディネータの予想を開かずに封印する・裁定 D148・D210・`tools/seal_Blens.py` v2 の型）。
 
 相:
@@ -24,7 +24,7 @@ REPO = os.path.abspath(os.path.join(HERE, '..'))
 sys.path.insert(0, HERE)
 import make_predictions_form_Bl3 as FORM
 
-VERSION = 'v1'
+VERSION = 'v2'          # v2（2026-09-25・裁定 D236）: 登録者の情報状態の欄が空なら、封印は止めずに印を置いて知らせる
 PRED = os.path.join(REPO, 'records', 'predictions')
 PATHS = {'coordinator': os.path.join(PRED, 'predictions-Bl3-coordinator.json'), 'registrant': os.path.join(PRED, 'predictions-Bl3-registrant.json')}
 RECORD_JSON = os.path.join(REPO, 'records', 'Bl3', 'sealing-record-Bl3.json')
@@ -123,10 +123,18 @@ def registrant(json_path, sha):
     if any(vals.get(k) != M[k] for k in ('form', 'program', 'contrasts')):
         raise SystemExit('登録者の JSON の様式の名・プログラム・正本の版が書式と違う')
     validate(vals, keys, opts, 'registrant', T, full=False)
+    empty = info_empty(vals)
+    if empty:
+        print('[seal_Bl3] 登録者の情報状態の欄が空です（%s）。封印は止めません。正本 predictions.free（裁定 D217）は両方が書くとするので、登録者にお知らせします' % '・'.join(empty))
     open(PATHS['registrant'], 'wb').write(b)
     print('[seal_Bl3] 登録者の予想を写した: %s・SHA-256 %s' % (rel(PATHS['registrant']), sha256b(b)))
 
 
+def info_empty(v):
+    """情報状態の欄（`info.coi`・`free`）のうち、空のものの名（正本 predictions.free・裁定 D217・D236）。"""
+    return [k for k in ('info.coi', 'free') if not str(v.get(k) or '').strip()]
+
+
 def record():
     if os.path.exists(RECORD_JSON):
         raise SystemExit('既にある（封印の記録は一度だけ）: %s' % rel(RECORD_JSON))
@@ -141,13 +149,15 @@ def record():
         b = open(p, 'rb').read()
         v = json.loads(b.decode('utf-8'))
         validate(v, keys, opts, role, T, full=(role == 'coordinator'))
-        R['predictions'][role] = {'path': rel(p), 'sha256': sha256b(b), 'date': v.get('date'), 'n_predicted': sum(1 for k in FORM.prediction_keys(T) if v.get(k) not in (None, '', FORM.NP))}
+        R['predictions'][role] = {'path': rel(p), 'sha256': sha256b(b), 'date': v.get('date'), 'n_predicted': sum(1 for k in FORM.prediction_keys(T) if v.get(k) not in (None, '', FORM.NP)),
+                                  'info_empty': info_empty(v)}                 # 情報状態の欄が空なら、その欄の名（裁定 D236）
     R['clause'] = '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
     json.dump(R, open(RECORD_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
     md = ['# B-lens 層三の予想の封印の記録（機械生成・`tools/seal_Bl3.py` %s・%s）' % (VERSION, R['written_utc']), '',
           '- 順: %s' % R['order'], '- 時: %s' % R['when'], '- 情報状態の決まり: %s' % R['free_rule'],
           '- 書式: `%s`（SHA-256 %s）' % (R['form']['path'], R['form']['sha256']), '- 下見の前の凍結の記録: `%s`（SHA16 %s）' % (rel(FREEZE), R['freeze_record_sha16'])]
-    md += ['- %s の予想: `%s`（SHA-256 %s・日付 %s・予想した欄 %d）' % (ROLE_WHO[r], x['path'], x['sha256'], x['date'], x['n_predicted']) for r, x in R['predictions'].items()]
+    md += ['- %s の予想: `%s`（SHA-256 %s・日付 %s・予想した欄 %d%s）' % (ROLE_WHO[r], x['path'], x['sha256'], x['date'], x['n_predicted'],
+                                                              ('・情報状態の欄が空: %s' % '・'.join(x['info_empty'])) if x['info_empty'] else '') for r, x in R['predictions'].items()]
     md += ['- この記録が無ければ、Colab の起動器の相 pilot と相 main は走らない。', '', R['clause'], '']
     open(RECORD_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(md))
     print('[seal_Bl3] 封印の記録を書いた: %s' % rel(RECORD_JSON))
````
<<< 終: `tools/seal_Bl3.py` の差分 >>>

<<< 始: `tools/make_frozen_Bl3.py` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/tools/make_frozen_Bl3.py b/tools/make_frozen_Bl3.py
index 3c2bb85..765e2fc 100644
--- a/tools/make_frozen_Bl3.py
+++ b/tools/make_frozen_Bl3.py
@@ -1,7 +1,7 @@
 # -*- coding: utf-8 -*-
-"""make_frozen_Bl3.py v2 —— B-lens 層三（Bl3）の凍結する本文（`design/design-Bl3-FROZEN.{src.md,md}`）を、草案3 の原稿から組む（B-lens の `make_frozen_Blens.py` の型・2026-09-25）。
+"""make_frozen_Bl3.py v3 —— B-lens 層三（Bl3）の凍結する本文（`design/design-Bl3-FROZEN.{src.md,md}`）を、草案3 の原稿から組む（B-lens の `make_frozen_Blens.py` の型・2026-09-25）。
 
-草案3 の登録者の確認の後に、正本の文を直す裁定（D226〜D235）があったので、凍結の本文は草案3 の本文と次の三つの差だけを持つ（ほかの差があれば止める）:
+草案3 の登録者の確認の後に、正本の文を直す裁定（D226〜D238）があったので、凍結の本文は草案3 の本文と次の三つの差だけを持つ（ほかの差があれば止める）:
   (一) 題名の印・凍結の一行・組み立ての記録の行（段階 B の器 `make_frozen_B.other_diffs` が許す差）。
   (二) 正本の鍵と設計事実から組まれる行のうち、正本と設計事実の直しで変わった行。同じ原稿を今の正本と設計事実で組み直した本文（組み直し）と草案3 の本文の差として機械で出し、
        記録（`records/Bl3/frozen-diff-Bl3.md`）に並べる。原稿の SHA16 が草案3 の組み立ての記録と、組み立ての器の SHA16 が草案3 の本文を最後に変えたコミットの器と同じことを
@@ -19,7 +19,8 @@ REPO = os.path.abspath(os.path.join(HERE, '..'))
 sys.path.insert(0, HERE)
 import make_frozen_B as MF
 
-VERSION = 'v2'          # v2（2026-09-25）: 組み直しの数の検査の記録の置き場を決まった言い方に置き換えてから差を取る・凍結の一行の裁定の範囲を D226〜D235 に
+VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 凍結の一行を組み立ての検査の外に置く・凍結版の原稿を組み直して本文と照らす／v2: 組み直しの記録の置き場の言い方・裁定の範囲
+STANDIN = '- **凍結**: （凍結の一行・登録者の逐語と日時は組み立ての後に入れる）'      # 組み立ての間の代わりの行（裁定 D236）
 REBUILD_LINT_LABEL = '（組み直しの一時の置き場の数の検査の記録）'      # 組み直しの本文の「束縛」の行の記録の置き場（一時の置き場の道筋を凍結物に残さない）
 NL = chr(10)
 SRC = os.path.join(REPO, 'design', 'design-Bl3-draft3.src.md')
@@ -29,7 +30,7 @@ FOUT = os.path.join(REPO, 'design', 'design-Bl3-FROZEN.md')
 LINT = os.path.join(REPO, 'records', 'Bl3', 'numbers-lint-FROZEN-Bl3.md')
 DIFFREC = os.path.join(REPO, 'records', 'Bl3', 'frozen-diff-Bl3.md')
 BUILDER = os.path.join(HERE, 'build_draft_Bl3.py')
-FROZEN_LINE = ('- **凍結**: %s（日本時間・登録者の言葉は逐語で「%s」・草案3 の原稿〔コミット %s 時点〕を逐語複製し、題名と本行と、裁定 D226〜D235 で正本の文を直した行'
+FROZEN_LINE = ('- **凍結**: %s（日本時間・登録者の言葉は逐語で「%s」・草案3 の原稿〔コミット %s 時点〕を逐語複製し、題名と本行と、裁定 D226〜D238 で正本の文を直した行'
                '〔正本の鍵から組まれる行と、原稿の直し〕だけを改める・直した行は `records/Bl3/frozen-diff-Bl3.md`・以後の変更は逸脱台帳に記帳する）')
 # 原稿の文の直し（裁定・直す前・直した後）。直す前の文は原稿の中でちょうど一度だけ当たること。
 LITERAL_FIXES = [
@@ -76,6 +77,22 @@ def build(src_path, out_path, label, lint_path):
     return r
 
 
+def build_frozen(src_path, out_path, lint_path):
+    """凍結版の原稿を組む（裁定 D236）: 凍結の一行を決まった代わりの行にして組み立て（数の検査と禁止語の走査はこの本文で走る）、組み立ての後に逐語の一行に戻す。"""
+    src = open(src_path, encoding='utf-8').read()
+    fl = [l for l in src.split('\n') if l.startswith('- **凍結**:')]
+    if len(fl) != 1:
+        raise SystemExit('凍結版の原稿に凍結の一行がちょうど一つでない（%d）' % len(fl))
+    with tempfile.TemporaryDirectory() as td:
+        tmp = os.path.join(td, 'frozen-standin.src.md')
+        open(tmp, 'w', encoding='utf-8', newline='\n').write(src.replace(fl[0], STANDIN))
+        build(tmp, out_path, '凍結版', lint_path)
+    out = open(out_path, encoding='utf-8').read()
+    if out.count(STANDIN) != 1:
+        raise SystemExit('組み立てた本文に代わりの行がちょうど一つでない')
+    open(out_path, 'w', encoding='utf-8', newline='\n').write(out.replace(STANDIN, fl[0]))
+
+
 def draft3_record():
     """草案3 の組み立ての記録の原稿の SHA16（本文の行）と、草案3 の本文を最後に変えたコミットの組み立ての器の SHA16（git から読む・草案3 の数の検査の記録は器の SHA16 を持たないため）。"""
     t = open(DRAFT, encoding='utf-8').read()
@@ -105,6 +122,14 @@ def rebuild_and_check(fsrc=None, fout=None):
         open(rb, 'w', encoding='utf-8', newline='\n').write(t_rb.replace(tmp_lint, REBUILD_LINT_LABEL))
         canon_driven = diffs(DRAFT, rb)
         residual = None
+        res['frozen_src_rebuilt_same'] = None
+        if fsrc and fout and os.path.exists(fsrc) and os.path.exists(fout):
+            fr = os.path.join(td, 'frozen-rebuilt.md')
+            build_frozen(fsrc, fr, os.path.join(td, 'lint-frozen.md'))
+            t_fr = open(fr, encoding='utf-8').read().replace(rel(os.path.join(td, 'lint-frozen.md')), rel(LINT))
+            res['frozen_src_rebuilt_same'] = (t_fr == open(fout, encoding='utf-8').read())
+            if not res['frozen_src_rebuilt_same']:
+                bad.append('凍結版の原稿を組み直した本文が、凍結の本文と違う')
         if fout and os.path.exists(fout):
             d = MF.other_diffs(diffs(rb, fout))
             olds = [o for _, o, _ in LITERAL_FIXES]
@@ -127,7 +152,9 @@ def write_diffrec(res):
          '- (二) 正本の鍵と設計事実から組まれる行の差（同じ原稿を今の正本と設計事実で組み直した本文と、草案3 の本文の差・行の頭の - が草案3・+ が組み直し）:', '', '```diff'] + \
         res['canon_driven'] + ['```', '', '- (三) 原稿の文の直し（裁定・直す前 → 直した後）:', ''] + \
         ['  - %s: 「%s」→「%s」' % (rid, o, n) for rid, o, n in LITERAL_FIXES] + \
-        ['', '- 組み直しと凍結の本文の差の残り（(一) と (三) の外）: %s' % ('無し' if res.get('residual') == [] else ('確かめていない' if res.get('residual') is None else '%d 行' % len(res['residual']))), '',
+        ['', '- 組み直しと凍結の本文の差の残り（(一) と (三) の外）: %s' % ('無し' if res.get('residual') == [] else ('確かめていない' if res.get('residual') is None else '%d 行' % len(res['residual']))),
+         '- 凍結版の原稿を同じ手順で組み直した本文と凍結の本文: %s' % {True: '同じ', False: '違う', None: '確かめていない'}[res.get('frozen_src_rebuilt_same')],
+         '- 凍結の一行（登録者の逐語と日時）は、組み立ての数の検査と禁止語の走査の外に置いた（組み立ての間は決まった代わりの行を置き、組み立ての後に逐語の一行を入れた・裁定 D236）。', '',
          '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
     open(DIFFREC, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
 
@@ -154,7 +181,15 @@ def main():
             raise AssertionError('直しの前の文が無い原稿を通した')
         except ValueError:
             pass
-        print('[make_frozen_Bl3] 自己検査 OK（題名の印・凍結の一行・原稿の直しの %d 行だけが原稿の差）' % len(LITERAL_FIXES))
+        # 凍結の一行に数のある逐語でも組める（組み立ての検査の外・裁定 D236）
+        with tempfile.TemporaryDirectory() as td:
+            fs, fo = os.path.join(td, 'f.src.md'), os.path.join(td, 'f.md')
+            words_ = '10時に凍結してください（自己検査）'
+            open(fs, 'w', encoding='utf-8', newline='\n').write(frozen_src(src, words_, 'deadbee', '2026-09-26 10:00'))
+            build_frozen(fs, fo, os.path.join(td, 'lint.md'))
+            t = open(fo, encoding='utf-8').read()
+            assert words_ in t and STANDIN not in t and t.count('- **凍結**:') == 1, '凍結の一行が本文に入らない'
+        print('[make_frozen_Bl3] 自己検査 OK（題名の印・凍結の一行・原稿の直しの %d 行だけが原稿の差・数のある逐語の凍結の一行でも組める）' % len(LITERAL_FIXES))
         return
     if a.check:
         res, bad = rebuild_and_check(FSRC, FOUT)
@@ -169,7 +204,7 @@ def main():
         if os.path.exists(p) and not a.force:
             raise SystemExit('既にある（--force で上書き）: %s' % rel(p))
     open(FSRC, 'w', encoding='utf-8', newline='\n').write(frozen_src(open(SRC, encoding='utf-8').read(), a.words, a.commit, a.date))
-    build(FSRC, FOUT, '凍結版', LINT)
+    build_frozen(FSRC, FOUT, LINT)
     res, bad = rebuild_and_check(FSRC, FOUT)
     write_diffrec(res)
     if bad:
````
<<< 終: `tools/make_frozen_Bl3.py` の差分 >>>

<<< 始: `tools/freeze_Bl3.py` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/tools/freeze_Bl3.py b/tools/freeze_Bl3.py
index 33a4672..d6cdf3d 100644
--- a/tools/freeze_Bl3.py
+++ b/tools/freeze_Bl3.py
@@ -1,5 +1,5 @@
 # -*- coding: utf-8 -*-
-"""freeze_Bl3.py v2 —— B-lens 層三（Bl3）の凍結の記帳（2026-09-25・正本 `predictions.when`・`computation.main_freeze_check`・裁定 D210・D222・`tools/freeze_Blens.py` の型）。
+"""freeze_Bl3.py v3 —— B-lens 層三（Bl3）の凍結の記帳（2026-09-25・正本 `predictions.when`・`computation.main_freeze_check`・裁定 D210・D222・`tools/freeze_Blens.py` の型）。
 
 相:
   prepilot  下見の前の凍結（正本のすべて・方向の npz・器・裁定 D210）。確かめてから記帳する（外れたら止める・登録者に相談）:
@@ -24,6 +24,10 @@
       下見の試みの session が DRY でない。最後の試みが本の凍結の下見（器の誤りの試みは、やり直したときの一度目として残す）。
     - 凍結の記録に足すのは `main_freeze` の鍵だけ（ほかの鍵は一字も変えない）。
     記帳: 凍結の記録の `main_freeze`（下見の試み・最後の試みの記録と機械の決定・session・凍結物の SHA16・器の差分・登録者の言葉と時刻）と、全体の台帳の一行。
+v3 の決め（裁定 D236）: 手順の順は「方向の npz と器を push → Colab の相 check → 下見の前の凍結の記帳」。相 check のコミットの器の閉包・正本・設計事実・方向の記録を
+  `git show <コミット>:<置き場>` で今の版と照らし、順伝播を呼んだ数（守りが数えた値）が零で、升目のトークンの並びの SHA16 が手元で組んだ並びと同じことを見る。
+  本の凍結は、下見の試みを session の終わりの時刻の順に並べ（与えた順と違えば止める）、試みごとに正本・npz・凍結の確かめを照らし、試みのコミットの凍結の記録と
+  封印の記録の中身を今の記録と照らし、二つ以上の試みには逸脱の台帳のやり直しの記帳を求め、封印の記録の SHA16 と二つの予想の SHA-256 を本の凍結の記録に写す。
 用法: python tools/freeze_Bl3.py prepilot --words "<登録者の逐語>" --when "<日時（日本時間）>" --colab-check <相 check の出力の置き場> ／ prepilot --check-only
       python tools/freeze_Bl3.py main --words "<登録者の逐語>" --when "<日時（日本時間）>" --pilot <相 pilot の出力の置き場> [<二つ目> …]
 柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
@@ -34,7 +38,7 @@ HERE = os.path.dirname(os.path.abspath(__file__))
 REPO = os.path.abspath(os.path.join(HERE, '..'))
 sys.path.insert(0, HERE)
 
-VERSION = 'v2'          # v2（2026-09-25・裁定 D231〜D235 の後）: 裁定の番号を記録の名から確かめる・合成データの正式の記録の版の SHA16 の表を今の版と突き合わせる・相 check の錨と ‖static‖
+VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 相 check のコミットの版とトークンの並び・本の凍結の試みの順と由来・封印の写し・番号の数の比べ・inputs.files・転記行 F／v2（裁定 D231〜D235 の後）
 NL = chr(10)
 FR_JSON = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.json')
 FR_MD = os.path.join(REPO, 'records', 'Bl3', 'FREEZE-RECORD-Bl3.md')
@@ -117,6 +121,9 @@ def latest_dry_run(T3):
     lack = sorted(need - set(table))
     differ = sorted(f for f, s16 in table.items() if not os.path.exists(P(f)) or sha16f(P(f)) != s16)
     res['sha_table'] = {'files': len(table), 'lack': lack, 'differ': differ}
+    res['boot_phases'] = '起動器の三つの相' in txt
+    if not res['boot_phases']:
+        bad.append('合成データの正式の記録に、起動器の三つの相を別のプロセスで走らせた確かめが無い（裁定 D236）')
     if lack:
         bad.append('合成データの正式の記録の版の SHA16 の表が、器の閉包と正本・設計事実・方向の記録を覆わない: %s' % lack)
     if differ:
@@ -124,6 +131,19 @@ def latest_dry_run(T3):
     return res, bad
 
 
+sha16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
+
+
+def local_ids_sha16(T3, FJ):
+    """手元のトークナイザで升目の入力を組み、トークンの並びの SHA16 を返す（相 check の値と照らす・裁定 D236）。"""
+    from transformers import AutoTokenizer
+    import bl3_run as BR
+    M_ = T3['inputs']['model']
+    tok = AutoTokenizer.from_pretrained(os.path.expanduser('~/.cache/huggingface/hub/models--%s/snapshots/%s' % (M_['repo'].replace('/', '--'), M_['rev'])))
+    keys = ['%s|%s' % tuple(c) for c in T3['cells_main']] + sorted({'%s|%s' % (x[0], x[1]) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']})
+    return {k: BR.ids_sha16(c) for k, c in BR.build_cells(tok, T3, FJ, keys).items()}
+
+
 def prepilot_checks(colab_dir=None):
     import make_frozen_Bl3 as MFB
     import make_predictions_form_Bl3 as FORM
@@ -158,6 +178,20 @@ def prepilot_checks(colab_dir=None):
         bad.append('正本の decisions に、裁定の記録の番号が無い: %s' % miss_d)
     if T3['numbering']['rulings_next'] != nxt:
         bad.append('正本の次の裁定の番号 %s が、裁定の記録の次の番号 %s と違う' % (T3['numbering']['rulings_next'], nxt))
+    inp_bad = [k for k, v in T3['inputs']['files'].items() if v.get('sha16') and (not os.path.exists(P(v['path'])) or sha16f(P(v['path'])) != v['sha16'])]
+    res['inputs_files'] = {'checked': sum(1 for v in T3['inputs']['files'].values() if v.get('sha16')), 'bad': inp_bad}
+    if inp_bad:
+        bad.append('正本 inputs.files の SHA16 と今のファイルが違う: %s' % inp_bad)
+    M_ = T3['inputs']['model']
+    snap = os.path.expanduser('~/.cache/huggingface/hub/models--%s/snapshots/%s' % (M_['repo'].replace('/', '--'), M_['rev']))
+    if os.path.exists(os.path.join(snap, 'model.safetensors.index.json')):
+        shards = sorted(set(json.load(open(os.path.join(snap, 'model.safetensors.index.json'), encoding='utf-8'))['weight_map'].values()))
+        miss_f = [x for x in ['config.json', 'tokenizer.json', 'model.safetensors.index.json'] + shards if x not in FJ['facts']['F']['sha256']]
+        res['fact_F'] = {'shards': len(shards), 'missing': miss_f}
+        if miss_f:
+            bad.append('転記行 F に、重みの索引の断片か設定のファイルが欠けている: %s' % miss_f)
+    else:
+        bad.append('手元に重みの索引が無く、転記行 F の断片を確かめられない')
     if FJ['contrasts_sha16'] != canon16 or DJ['contrasts_sha16'] != canon16:
         bad.append('設計事実か方向の記録の正本の SHA16 が今の正本と違う（作り直す）')
     # 方向の npz
@@ -211,7 +245,14 @@ def prepilot_checks(colab_dir=None):
              'cells': all((CK['cells'].get(k) or {}).get(x) == v[y] for k, v in FJ['facts']['B']['cells'].items() for x, y in (('prompt_len', 'prompt_len'), ('main_position', 'main_position'), ('readout_position', 'readout_position'), ('family', 'family'))),
              'rewrite_importable': CK.get('rewrite_importable') is True, 'canon_at_commit': S.get('canon_sha16') == canon16,
              'comparator_anchor': CK.get('comparator_anchor') == K3.comparator_anchor(DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'], K3.blens_own_pair()),
-             'static_norm': CK.get('static_norm_matches_fact_D') is True}
+             'static_norm': CK.get('static_norm_matches_fact_D') is True, 'forward_guards': (CK.get('forward_guards') or 0) > 0}
+        cm = S.get('commit') or ''
+        at_commit = [f for f in import_closure(TOOLS) + ['design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md', 'results/Bl3/directions-Bl3.json']
+                     if sha16b(subprocess.run(['git', '-C', REPO, 'show', '%s:%s' % (cm, f)], capture_output=True).stdout) != sha16f(P(f))]
+        c['versions_at_commit'] = bool(re.fullmatch(r'[0-9a-f]{40}', cm)) and not at_commit
+        res['colab_check_versions_differ'] = at_commit
+        tok_local = local_ids_sha16(T3, FJ)
+        c['token_ids'] = all((CK['cells'].get(k) or {}).get('ids_sha16') == v for k, v in tok_local.items())
         res['colab_check'] = dict(c, commit=S.get('commit'), gpu_name=S.get('gpu'), versions_seen=S.get('versions'))
         bad += ['Colab の確かめ: %s' % k for k, v in c.items() if not v]
     return T3, res, bad
@@ -232,7 +273,7 @@ def prepilot(words, when, colab_dir, force=False):
     tools = import_closure(TOOLS)
     files = frozen_files(T3) + [res['dry_run']['path'], rel(CC_SESSION), rel(CC_CHECK)]
     frozen = {r: sha16f(P(r)) for r in files + tools}
-    R = {'kind': 'bl3_freeze_record', 'version': VERSION, 'stage': 'prepilot', 'frozen_jst': when, 'registrant_words': words, 'rulings': sorted(k for k in T3['decisions'] if k >= 'D204'),
+    R = {'kind': 'bl3_freeze_record', 'version': VERSION, 'stage': 'prepilot', 'frozen_jst': when, 'registrant_words': words, 'rulings': sorted((k for k in T3['decisions'] if int(k[1:]) >= 204), key=lambda x: int(x[1:])),
          'frozen_sha16': frozen, 'tools_import_closure': tools, 'directions_npz_sha256': res['directions']['sha256'], 'checks': res,
          'deviation_rule': '凍結の後の変更は、逸脱として番号・日付・理由・登録者の承認を台帳（この記録の deviations）に記す。器の差分は tool_diffs に置き場・前・後の SHA16 を記す（正本 computation.main_freeze_check）',
          'deviations': [],
@@ -282,7 +323,7 @@ def main_freeze_checks(FR, pilot_dirs):
     res['ledgered_not_changed'] = sorted(p for p in ledgered if now_sha.get(p) == frozen.get(p))
     if res['ledgered_not_changed']:
         bad.append('台帳に記した器の差分が凍結物に現れない: %s' % res['ledgered_not_changed'])
-    atts, sessions = [], []
+    atts, sessions, fin = [], [], []
     for d in pilot_dirs:
         PJ = json.load(open(os.path.join(d, 'pilot.json'), encoding='utf-8'))
         S = json.load(open(os.path.join(d, 'session.json'), encoding='utf-8'))
@@ -291,8 +332,39 @@ def main_freeze_checks(FR, pilot_dirs):
         c = S.get('commit') or ''
         if not (re.fullmatch(r'[0-9a-f]{40}', c) and in_commit(c, 'records/Bl3/FREEZE-RECORD-Bl3.json') and in_commit(c, 'records/Bl3/sealing-record-Bl3.json')):
             bad.append('下見の試みのコミットが、凍結の記録と封印の記録を含むコミットでない: %s' % c)
+        if S.get('canon_sha16') != frozen.get(canon) or S.get('directions_npz_sha256') != FR.get('directions_npz_sha256') or ((S.get('frozen_check') or {}).get('bad') or []):
+            bad.append('下見の試みの session の正本か npz か凍結の確かめが、凍結の記録と合わない: %s' % d)
+        if re.fullmatch(r'[0-9a-f]{40}', c):
+            # 封印の記録は封印の後に変わらないので、まるごと照らす。凍結の記録は台帳（deviations）が足されうるので、凍結物の SHA16 の表と npz の SHA-256 を照らす
+            if sha16b(subprocess.run(['git', '-C', REPO, 'show', '%s:records/Bl3/sealing-record-Bl3.json' % c], capture_output=True).stdout) != sha16f(SEAL):
+                bad.append('下見の試みのコミットの封印の記録が、今の封印の記録と違う: %s' % c)
+            try:
+                FRc = json.loads(subprocess.run(['git', '-C', REPO, 'show', '%s:records/Bl3/FREEZE-RECORD-Bl3.json' % c], capture_output=True).stdout.decode('utf-8'))
+            except Exception:
+                FRc = {}
+            if FRc.get('frozen_sha16') != frozen or FRc.get('directions_npz_sha256') != FR.get('directions_npz_sha256'):
+                bad.append('下見の試みのコミットの凍結の記録の凍結物か npz が、今の凍結の記録と違う: %s' % c)
         atts.append(PJ['pilot'])
+        fin.append(S.get('finished') or '')
         sessions.append({k: S.get(k) for k in ('commit', 'gpu', 'versions', 'canon_sha16', 'directions_npz_sha256', 'finished')})
+    if fin != sorted(fin) or not all(fin):
+        bad.append('下見の試みの与えた順が、session の終わりの時刻の順と違う（または時刻が無い）: %s' % fin)
+    reruns = [x for x in FR.get('deviations') or [] if x.get('kind') == 'pilot_rerun']
+    if len(atts) >= 2 and len(reruns) < len(atts) - 1:
+        bad.append('下見の試みが二つ以上あるのに、逸脱の台帳にやり直しの記帳（kind pilot_rerun）が足りない: 試み %d・記帳 %d' % (len(atts), len(reruns)))
+    SR = json.load(open(SEAL, encoding='utf-8')) if os.path.exists(SEAL) else {}
+    # 封印の記録にある凍結の記録の SHA16 は、封印の記録を足したコミットの凍結の記録と照らす（封印の後に逸脱を台帳に記すと、今の凍結の記録は変わりうるため）
+    sc_ = subprocess.run(['git', '-C', REPO, 'log', '--diff-filter=A', '--format=%H', '-1', '--', 'records/Bl3/sealing-record-Bl3.json'], capture_output=True, text=True).stdout.strip()
+    if not sc_:
+        bad.append('封印の記録を足したコミットが無い（封印の記録をコミットしてから本の凍結）')
+    elif sha16b(subprocess.run(['git', '-C', REPO, 'show', '%s:records/Bl3/FREEZE-RECORD-Bl3.json' % sc_], capture_output=True).stdout) != SR.get('freeze_record_sha16'):
+        bad.append('封印の記録にある凍結の記録の SHA16 が、封印の記録を足したコミットの凍結の記録と違う')
+    pre = {}
+    for role, v in (SR.get('predictions') or {}).items():
+        pre[role] = sha256f(P(v['path'])) if os.path.exists(P(v['path'])) else None
+        if pre[role] != v.get('sha256'):
+            bad.append('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
+    res['seal'] = {'record_sha16': sha16f(SEAL) if os.path.exists(SEAL) else None, 'predictions_sha256': pre}
     if not atts:
         bad.append('下見の試みが無い')
     elif atts[-1].get('tool_error'):
@@ -313,7 +385,7 @@ def main_freeze(words, when, pilot_dirs):
         raise SystemExit('本の凍結の確かめが外れた（止める・登録者に相談）: %s' % bad)
     before = {k: v for k, v in FR.items()}
     FR['main_freeze'] = {'frozen_jst': when, 'registrant_words': words, 'pilot_attempts': atts, 'pilot': atts[-1], 'decision': atts[-1].get('decision'),
-                         'sessions': sessions, 'frozen_sha16': now_sha, 'tool_diffs_applied': res['changed'], 'freeze_tool': 'tools/freeze_Bl3.py %s' % VERSION}
+                         'sessions': sessions, 'frozen_sha16': now_sha, 'tool_diffs_applied': res['changed'], 'seal': res['seal'], 'freeze_tool': 'tools/freeze_Bl3.py %s' % VERSION}
     assert all(FR[k] == before[k] for k in before), '本の凍結でほかの鍵が変わった'
     assert set(FR) - set(before) == {'main_freeze'}
     json.dump(FR, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
````
<<< 終: `tools/freeze_Bl3.py` の差分 >>>

<<< 始: `tools/make_contrasts_Bl3.py` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/tools/make_contrasts_Bl3.py b/tools/make_contrasts_Bl3.py
index 83d80be..6902599 100644
--- a/tools/make_contrasts_Bl3.py
+++ b/tools/make_contrasts_Bl3.py
@@ -1,5 +1,5 @@
 # -*- coding: utf-8 -*-
-"""make_contrasts_Bl3.py v5 —— B-lens 層三（Bl3・段階 B の後・B-lens の後・別の小さな登録）の正本 `design/contrasts-Bl3.json` を作る（草案3・登録者裁定 D203〜D223）。
+"""make_contrasts_Bl3.py v8 —— B-lens 層三（Bl3・段階 B の後・B-lens の後・別の小さな登録）の正本 `design/contrasts-Bl3.json` を作る（草案3・登録者裁定 D203〜D223）。
 数は数値の葉に置き、説明の文には構造でない数を打たない（凍結した `tools/numbers_lint.py` の登録検査が正本の説明文と生成器の文字列を見る）。
 段階 B と B-lens の凍結物（正本・集計の記録・方向・活性の記録）は読むだけで変えない。入力の置き場の SHA は器が計算する。再実行で同一バイト（時刻を持たない）。
 起草者が置いた値（設計の巡で諮る）は `drafter_values` に名を並べる。
@@ -10,6 +10,8 @@ v5（草案3 の起草者の見直しの後）: 見直しの記録（`records/Bl
 v6（器の段・下見の前の凍結の準備）: 器の段で見つけたこと T1〜T4（`records/Bl3/tools/tools-log-Bl3.md`）の登録者裁定 D226・D227 を受ける（`records/Bl3/rulings-D226-D227.md`）。
 v7（器についての意見伺いの後）: 登録者裁定 D228〜D235 を受ける（`records/Bl3/rulings-D228-D230.md`・`records/Bl3/rulings-D231-D235.md`・意見伺いの採否の案 `records/reviews/Bl3/opinions-tools/adoption-proposal-opinions-tools-Bl3.md`）。
   裁定 D234 の言い方を、正本の残りの文（下見の記録の並べ方・頭の近道の確かめの定め・最後の層の自己検査の一本・器の実装の検分の見どころと順・見込みの注）にもそろえた。
+v8（器の実装の検分の後）: 登録者裁定 D236〜D238 を受ける（`records/Bl3/rulings-D236-D237.md`・`records/Bl3/rulings-D238.md`・採否の案 `records/reviews/Bl3/impl/adoption-table-impl-Bl3.md`）。
+  検分の順に器の直しの確かめの段を足し（裁定 D238）、合成データの確かめの一覧に、直しで足した確かめを書き足した（裁定 D236）。
 用法: python tools/make_contrasts_Bl3.py
 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
 import os, re, json, math, hashlib, collections
@@ -17,7 +19,7 @@ import os, re, json, math, hashlib, collections
 REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 j = lambda *p: os.path.join(REPO, *p)
 NL = chr(10)
-VERSION = 'v7'
+VERSION = 'v8'
 s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
 TL = json.load(open(j('design', 'contrasts-Blens.json'), encoding='utf-8'))          # B-lens の正本（凍結・読むだけ）
 TB = json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8'))              # 段階 B の正本（凍結・読むだけ）
@@ -130,6 +132,9 @@ decisions = {
     'D233': '独立の再計算の一段目は、無操作の値も比べる（同上）',
     'D234': '本の計算は近道を使わない。独立の再計算の二段目は札の一致で判定し、効き目の差の最大は記録して報告に並べる（値だけが許容の外で札が同じときは止めずに逸脱の台帳に記す）。一段目は値と札の両方で判定する。下見の (v) は記述として残す（同上）',
     'D235': '正本の小さな直しと限界の足し（採否の案の C の表）を、下見の前の凍結の正本でまとめて入れる（同上）',
+    'D236': '器の実装の検分（二体）の採否の案の A の表（凍結の前に直す）をすべて採る。走っていた合成データの正式の記録は止め、直した後に取り直す（`records/Bl3/rulings-D236-D237.md`）',
+    'D237': '採否の案の B の表（記録に置く）を採る（同上）',
+    'D238': '直した後に、新しい個体の系統外二名（Gemini）と claude.ai の Claude Opus 5.5 二名に、直しの確かめの検分を頼む（巡を一つ足す・重い所見で直しが大きくなったため）。直しと正式の記録の取り直しの後に、依頼文と束をコーディネータが用意し、登録者が渡す（`records/Bl3/rulings-D238.md`）',
 }
 
 READING = [
@@ -174,7 +179,7 @@ all_ban = sorted(set(value_ban + mech_ban + added_ban + reading_never))
 
 T = {
     'id': 'Bl3',
-    'version': 'draft3-r3-2026-09-25',
+    'version': 'draft3-r4-2026-09-25',
     'generator': 'tools/make_contrasts_Bl3.py %s' % VERSION,
     'note': '段階 B の後・B-lens の後の登録外の記述（小さな登録）。段階 B と B-lens の札・報告・凍結物は変えない。本文と正本が食い違う場合は正本が勝つ。',
     'decisions': decisions,
@@ -210,7 +215,8 @@ T = {
             ('design_r2_verification', 'records/reviews/Bl3/design-round2/verification-Bl3-design-r2.md'), ('rulings_D224_D225', 'records/Bl3/rulings-D224-D225.md'),
             ('draft3_review', 'records/Bl3/draft3-review/review-draft3-Bl3.md'), ('exposure', 'records/Bl3/exposure-before-seal-Bl3.md'),
             ('rulings_D226_D227', 'records/Bl3/rulings-D226-D227.md'), ('rulings_D228_D230', 'records/Bl3/rulings-D228-D230.md'),
-            ('rulings_D231_D235', 'records/Bl3/rulings-D231-D235.md'), ('opinions_adoption', 'records/reviews/Bl3/opinions-tools/adoption-proposal-opinions-tools-Bl3.md'))},
+            ('rulings_D231_D235', 'records/Bl3/rulings-D231-D235.md'), ('opinions_adoption', 'records/reviews/Bl3/opinions-tools/adoption-proposal-opinions-tools-Bl3.md'),
+            ('rulings_D236_D237', 'records/Bl3/rulings-D236-D237.md'), ('rulings_D238', 'records/Bl3/rulings-D238.md'), ('impl_adoption', 'records/reviews/Bl3/impl/adoption-table-impl-Bl3.md'))},
         'activations': {'place': ACT_PLACE, 'sha256_head16': DIRS['activations_npz_sha256'][:16].upper(), 'arms': ARMS8, 'scenes': DIRS['extraction_scenarios']},
         'versions_B': TL['inputs']['versions_B'],
         'versions_note': 'これは B の本走行のセッション記録の版である。torch は CUDA の組みまで揃え、Colab の起動器が入れ直して文字列の完全な一致で確かめる（裁定 D187）',
@@ -405,10 +411,14 @@ T = {
                            '門と最上位の判定の呼び方（符号の二重掛け・中心の引き方）', '層の出力の取り方（`hidden_states` の最後の要素を使わない）',
                            '合成データの確かめを検分者が実際に走らせ、その記録を残す（採否表 P694）'],
                  'budget': '起動の前に、体数・機種・費用を登録者に申告する（独立の再計算の器の書き手を立てるときも同じ）'},
+        'impl_recheck': {'gemini': 2, 'claude_ai': 2, 'fresh': True, 'when': '器の直しと合成データの正式の記録の取り直しの後・Colab の相 check の前',
+                         'what': '直した器と検分の版からの差分・採否の案・二体の票と確かめ・合成データの正式の記録（束と依頼文はコーディネータが用意し、登録者が渡す）',
+                         'why': '器の実装の検分の重い所見で直しが大きくなったので、巡を一つ足す（`review_plan.no_more`・裁定 D238）'},
         'results': {'gemini': 2, 'claude_ai': 2, 'fresh': True},
         'final': {'external': 1, 'fresh': True, 'label': '最終'},
         'counting': 'claude.ai の Claude はコーディネータと同じ系列。何票でも一票に数え、独立の重みは系統外の票に置く（裁定 D59）',
         'order': ['設計の巡（一巡目）', '裁定', '草案2', '設計の巡（二巡目・下見の前の凍結の前の最終検分）', '裁定', '草案3', '登録者の確認（草案3）', '器と合成データの確かめ（独立の再計算の器は別の個体が書く）', '器の実装の検分',
+                  '器の直しの確かめ（系統外二名・claude.ai 二名・裁定 D238）',
                   '下見の前の凍結と記録先行の公開（正本・方向の npz・器）', '封印（下見の前）', '下見（決定木を機械で当てる）', '本の凍結（下見の記録と機械の決定を凍結の記録に足す）',
                   '計算（頭の自己検査・本の計算は近道を使わない・裁定 D234・独立の再計算の二段の判定・結果は登録者と一緒に開く）', '報告', '結果の巡（新しい個体）', '最終の系統外の一票（「最終」と明記）', '起草者の最終の見直し', '登録者最終確認と公開'],
         'no_more': 'この順のほかに巡を置かない（裁定 D160 の型）。重い所見で直しが大きくなるときは、登録者に上げて決めていただく',
@@ -416,7 +426,10 @@ T = {
                       '帰無との同じ値', '両方の向きがちょうど対称な比べる相手', '書き出しの割り方が変わる場合（器が止まるか）', '主位置まで使い回してしまう近道の誤り',
                       '門と主の札と向きの足し分に要る全ての升目・符号・方向の組の突き合わせ（掃き出し）',
                       '端数のバッチ（零のベクトルで埋めた分の値を使わない）', '零の近くの中央値（零が等方の帰無の四分位の間にある）', 'Holm の境で一本違う p（独立の再計算の札の一致の判定）',
-                      '器の誤りでやり直す流れ（一度目の記録と決定を並べる・q1 の採点）', 'bf16 相当の揺れを入れた合成の模型（近道の許容の式と、独立の再計算の二段）'],
+                      '器の誤りでやり直す流れ（一度目の記録と決定を並べる・q1 の採点）', 'bf16 相当の揺れを入れた合成の模型（近道の許容の式と、独立の再計算の二段）', '本の計算が近道を使わないことの振る舞いの確かめ（近道の元を作る呼び出しの数・使い回す cache・列の全長・裁定 D236）',
+                      '正本の文から独立に書いた札と門と、集計の器の出力の突き合わせ（下見で外した升目の場合を含む・裁定 D236）',
+                      '等方の外の行が出る枝（等方は正本の本数・割合を決めた裾と側の一致・q7・読みの型・裁定 D236）',
+                      '起動器の三つの相を DRY で別のプロセスとして走らせ、集計の器の CLI と報告の組み立てに通す（裁定 D236）'],
     },
     'report_rules': {
         'template': ['頭に凍結の後の逸脱の一覧（台帳から器が読む）', '状態は機械の区画で、登録者最終確認の前と後の二つの型（確認の後は逐語と時刻・裁定 D199 の型）',
@@ -468,7 +481,7 @@ T = {
                '最後の層の自己検査（`computation.self_checks.layer`）は作りの上で恒等で、層と位置の取り方だけを確かめる（裁定 D235）'],
     'drafter_values': ['nulls.isotropic.seed', 'readout.primary.order_seed', 'computation.steered_cache_check.seed', 'readout.variants', 'pilot.variant_flag', 'pilot.noise_max', 'pilot.repeat_n',
                        'independent_recompute.tol_stage1', 'computation.layer_tol', 'labels.side_rule', 'labels.second.ranks', 'predictions.items', 'predictions.q7_rule', 'cost'],
-    'numbering': {'rulings_next': 'D236'},
+    'numbering': {'rulings_next': 'D239'},
     'clause': '本正本のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。',
 }
 assert T['pilot']['decision']['cells_min_pass'] <= T['pilot']['decision']['cells_total']
````
<<< 終: `tools/make_contrasts_Bl3.py` の差分 >>>

<<< 始: `tools/dry_run_Bl3.py` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/tools/dry_run_Bl3.py b/tools/dry_run_Bl3.py
index 5726b07..f444df8 100644
--- a/tools/dry_run_Bl3.py
+++ b/tools/dry_run_Bl3.py
@@ -1,5 +1,5 @@
 # -*- coding: utf-8 -*-
-"""dry_run_Bl3.py v2 —— B-lens 層三（Bl3）の合成データの器（正本 `review_plan.synthetic` の形のすべてと、乱数の小さな模型で端から端まで・2026-09-25）。
+"""dry_run_Bl3.py v3 —— B-lens 層三（Bl3）の合成データの器（正本 `review_plan.synthetic` の形のすべてと、乱数の小さな模型で端から端まで・2026-09-25）。
 
 一. 純粋な関数の形（`tools/bl3_core.py`・`tools/blens_core.py`・`tools/analyze_Bl3.py`）: 奇でない押し・零でない帰無の中心・減算の行・下見で外れる升目と門の行だけの升目・
     帰無との同じ値・両方の向きがちょうど対称な比べる相手・掃き出し・端数のバッチ・零の近くの中央値・Holm の境で一本違う p・器の誤りでやり直す流れ・
@@ -13,6 +13,10 @@
 三. わざと壊した読み取り（二重の正規化）と近道の元（主位置まで使い回す・記録した切れ目を偽る）で、自己検査と凍結した確かめが止まることを確かめる。
     本物の相対の加減の大きさにそろえた合成の方向で、書き換えの道の変種・主位置の一つ分の寄与・二段目の本の道とフックの差（意見伺いの C2-3.2）を記述として測る。
 四. 別の個体の書き換えの器（`tools/bl3_recompute_rewrite.py`・中は変えない）の自己検査と `--dry` を今の本の器の上で走らせ、出力を記録に写す。
+五. 起動器の三つの相を DRY で別のプロセスとして走らせ、集計の器の CLI（一致だけを見る段・結果を開く段）と掃き出しと報告の組み立てに通す。一致だけを見る段の後に組の出力を
+    差し替えると、結果を開く段が止まることを確かめる（裁定 D236）。
+v3（裁定 D236）で足した確かめ: 本の計算が近道を使わないことの振る舞い・正本の文から独立に書いた札と、答えの分かる合成での門の組み立て・等方の外の行が出る枝・
+    有限でない値の止め・結果を開く段の結びつき。
 記録の末尾に、走らせた器（凍結の器の一覧と import の閉包）と正本・設計事実・方向の記録の SHA16 を、走りの始めと終わりで同じことを確かめて並べる
 （下見の前の凍結の器が今の版と突き合わせる）。
 **実の重みで読み取りの値を出さない**（正本 `computation.before_seal`）。合成の方向は、実の方向の名だけを借りた乱数（次元は小さな模型のもの）。
@@ -20,7 +24,7 @@
 用法: python tools/dry_run_Bl3.py [--force] [--iso 本数（既定は正本の本数）] [--e2e-iso 本数（既定 9）] [--out 置き場]
 柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
 """
-import os, re, sys, json, math, time, copy, hashlib, argparse, datetime, subprocess, collections
+import os, re, sys, glob, json, math, time, copy, shutil, hashlib, argparse, datetime, tempfile, subprocess, collections
 import numpy as np
 
 HERE = os.path.dirname(os.path.abspath(__file__))
@@ -29,7 +33,7 @@ sys.path.insert(0, HERE)
 import blens_core as C
 import bl3_core as K
 
-VERSION = 'v2'          # v2（2026-09-25・裁定 D231〜D234）: 本の計算は近道を使わない・二段の判定の形・下見の分かれ道を端から端まで・cache の長さの確かめ・書き換えの器の自己検査・版の SHA16
+VERSION = 'v3'          # v3（2026-09-25・裁定 D236）: 近道の振る舞い・独立の札と答えの分かる門・等方の外の枝・有限でない値・結果を開く段の結びつき・起動器の三つの相／v2（裁定 D231〜D234）
 NL = chr(10)
 SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
 T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
@@ -42,6 +46,7 @@ sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).
 
 
 def check(group, name, ok, detail=''):
+    detail = detail if isinstance(detail, str) else '・'.join(map(str, detail)) if isinstance(detail, (list, tuple)) else str(detail)      # 記録の表は文字列だけ
     RESULTS.append((group, name, bool(ok), detail))
     print('[dry_run_Bl3] %s %-4s %s %s' % (group, 'OK' if ok else 'FAIL', name, detail), flush=True)
 
@@ -87,6 +92,71 @@ def tool_shas():
     return collections.OrderedDict((f, sha16f(os.path.join(REPO, *f.split('/')))) for f in files)
 
 
+# ---------------- 正本の文から独立に書いた主の札（検べ用・芯の関数を呼ばない・裁定 D236） ----------------
+def answer_labels(T3, main_rows, eff, pair_names, dropped=()):
+    """正本 `labels.p_rule`（両側に等しい裾）・`labels.iso_outside.rule`（Holm・段を下回れば通し、通らなかった所で止める）・`labels.second`（比べる相手の中央値を中心に、
+    距離が比べる相手のすべてを上回れば最上位・向きの順位と対の単位の順位）・`labels.side_rule`（等方の帰無の四分位と中央値）・`labels.second.iso_top_share`・`nulls.real.rule`
+    （v̂ と (6b) は兄弟の対を除き、Nk と td は B-lens の凍結の自分の対だけを除く）を、文から書き直した。"""
+    alpha = T3['labels']['iso_outside']['holm_alpha']
+    n_iso = T3['nulls']['isotropic']['count']
+    own = K.blens_own_pair()                                           # 二つの道の外の凍結物（B-lens の器の文から読む）
+    swaps = set(T3['nulls']['real']['swap_siblings'])
+    key = lambda sc, b, sg: '%s|%s|%+d' % (sc, b, int(sg))
+    out, pv = collections.OrderedDict(), {}
+    for r in main_rows:
+        if '%s|%s' % (r['scenario'], r['base']) in set(dropped):
+            continue
+        k, kk = key(r['scenario'], r['base'], r['sign']), key(r['scenario'], r['base'], -r['sign'])
+        e = float(eff[k][r['direction']])
+        iso = np.array([eff[k]['iso:%d' % i] for i in range(n_iso)], dtype=np.float64)
+        dropc = swaps if r['direction'] in ('static', 'loaded') else {own[r['direction']]}
+        comps = [q for q in pair_names if q not in dropc]
+        same = np.array([eff[k]['real:' + q] for q in comps], dtype=np.float64)
+        opp = np.array([eff[kk]['real:' + q] for q in comps], dtype=np.float64)
+        up, lo = int(np.sum(iso >= e)), int(np.sum(iso <= e))
+        p = min(1.0, 2.0 * min(up + 1, lo + 1) / (n_iso + 1))
+        tail = 'upper' if up < lo else ('lower' if lo < up else 'tie')
+        allc = np.concatenate([same, opp])
+        c0 = float(np.median(allc))
+        d = abs(e - c0)
+        dc = np.abs(allc - c0)
+        pairv = np.maximum(np.abs(same - c0), np.abs(opp - c0))
+        m0, q1, q3 = float(np.median(iso)), float(np.percentile(iso, 25)), float(np.percentile(iso, 75))
+        if q1 <= 0.0 <= q3:
+            side = ('sign_only', int(np.sign(e)))
+        else:
+            s0 = 1.0 if m0 > 0 else -1.0
+            side = ('stronger' if (e * s0 > 0 and abs(e) > abs(m0)) else ('weaker' if e * s0 >= 0 else 'opposite'), None)
+        out[r['id']] = {'p': p, 'tail': tail, 'top': bool(np.all(d > dc)), 'rank_o': int(1 + np.sum(dc >= d)), 'rank_p': int(1 + np.sum(pairv >= d)),
+                        'side': side, 'share': float(np.mean(np.abs(iso - c0) > float(np.max(dc))))}
+        pv[r['id']] = p
+    still = True
+    for i, rid in enumerate(sorted(pv, key=lambda x: (pv[x], x))):
+        ok = still and pv[rid] < alpha / (len(pv) - i)
+        out[rid]['holm'] = ok
+        still = ok
+    return out
+
+
+def synth_effects(T3, pair_names, n_iso, seed):
+    """合成の効き目（升目と符号の鍵 → 方向の名 → 効き目）: 奇でない押し（逆の符号の升目の効き目は別に引く）・零でない帰無の中心（升目ごとに中心を変える）・
+    等方の外に出る強い v̂ と Nk の行を半分ほど。値に意味は無い（札の組み立ての確かめだけに使う）。"""
+    rng = np.random.default_rng(seed)
+    names = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
+    keys = sorted({'%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']} | {'%s|%s|%+d' % (sc, b, -int(sg)) for sc, b, sg in T3['cell_signs_main']})
+    eff = {}
+    for j, k in enumerate(keys):
+        center = (-1.0) ** j * (0.5 + 0.25 * j)
+        e = {d: float(rng.normal(loc=center, scale=0.5)) for d in names}
+        e.update({'iso:%d' % i: float(x) for i, x in enumerate(rng.normal(loc=center, scale=0.5, size=n_iso))})
+        e.update({'real:' + q: float(x) for q, x in zip(pair_names, rng.normal(loc=0.0, scale=1.5, size=len(pair_names)))})
+        if j % 2 == 0:
+            e['static'] = center + 6.0 * (1 if j % 4 == 0 else -1)
+            e['Nk'] = center - 6.0
+        eff[k] = e
+    return eff
+
+
 # ---------------- 一. 純粋な関数の形 ----------------
 def part_pure():
     G = '一'
@@ -225,6 +295,59 @@ def part_pure():
     stop_sw = raises(lambda: K.comparator_anchor(pn, [x for x in sw if x != own['static']], own), ValueError)
     check(G, '比べる相手の除き方の錨（B-lens の凍結の OWN_PAIR と正本の兄弟の対・裁定 D231）', bool(anc) and stop_own and stop_sw,
           '除いた対の数 %s・錨をずらした写しで止まる %s・兄弟の対から自分の対を抜いた写しで止まる %s' % ({d: len(v) for d, v in anc.items()}, stop_own, stop_sw))
+    # 正本の文から独立に書いた札（芯の関数を呼ばない）と、集計の器の札の突き合わせ（等方は正本の本数・奇でない押し・零でない帰無の中心・下見で外した升目・裁定 D236）
+    n_iso = T3['nulls']['isotropic']['count']
+    pn_ = DJ['groups']['real']['names']
+    eff_s = synth_effects(T3, pn_, n_iso, seed=17)
+    for dropped_ in ([], ['N1|O-Ncold']):
+        mine = answer_labels(T3, T3['main_rows'], eff_s, pn_, dropped_)
+        lab_, meta_ = AZ.row_labels(T3, T3['main_rows'], eff_s, pn_, dropped_)
+        diff_ = []
+        for rid, a_ in mine.items():
+            o = lab_.get(rid)
+            if o is None:
+                diff_.append((rid, '行が無い'))
+                continue
+            got = (round(o['p'], 12), o['tail'], o['iso_outside'], o['second']['top'], o['second']['rank_oriented'], o['second']['rank_pair'], o['side']['side'],
+                   o['side'].get('sign') if o['side']['side'] == 'sign_only' else None, round(o['iso_top_share'], 12))
+            want_ = (round(a_['p'], 12), a_['tail'], a_['holm'], a_['top'], a_['rank_o'], a_['rank_p'], a_['side'][0], a_['side'][1], round(a_['share'], 12))
+            if got != want_:
+                diff_.append((rid, got, want_))
+        n_out = sum(1 for a_ in mine.values() if a_['holm'])
+        check(G, '正本の文から独立に書いた札と集計の器の札（等方 %d 本・外した升目 %s・裁定 D236）' % (n_iso, '・'.join(dropped_) or 'なし'),
+              not diff_ and set(lab_) == set(mine) and n_out > 0 and meta_['m_rows'] == len(mine),
+              '行 %d・食い違い %d・等方の外の行 %d・Holm の段の数 %d%s' % (len(mine), len(diff_), n_out, meta_['m_rows'], ('（例 %s）' % (diff_[:1],)) if diff_ else ''))
+    # 等方の外の行が出る枝: 札の一致の中身（裁定 D232）・q7・予想の答え
+    lab_, _ = AZ.row_labels(T3, T3['main_rows'], eff_s, pn_, [])
+    out_ids = [rid for rid, o in lab_.items() if o['iso_outside']]
+    in_ids = [rid for rid, o in lab_.items() if not o['iso_outside']]
+    q7r = AZ.q7_rows_of(lab_, FJ)
+    sig0 = AZ.labels_signature(lab_)
+    flip_in, flip_out = copy.deepcopy(lab_), copy.deepcopy(lab_)
+    if in_ids:
+        flip_in[in_ids[0]]['tail'] = 'lower' if flip_in[in_ids[0]]['tail'] != 'lower' else 'upper'
+    flip_out[out_ids[0]]['tail'] = 'lower' if flip_out[out_ids[0]]['tail'] != 'lower' else 'upper'
+    check(G, '等方の外の行が出る枝（割合を決めた裾の比べは外の行だけ・q7 の行・裁定 D232・D236）',
+          bool(out_ids) and AZ.labels_signature(flip_in) == sig0 and AZ.labels_signature(flip_out) != sig0 and bool(q7r) and all(r_['id'] in out_ids for r_ in q7r),
+          '等方の外の行 %d・内の行の裾を変える → 札は同じ・外の行の裾を変える → 札が違う・q7 の行 %d' % (len(out_ids), len(q7r)))
+    # 答えの分かる合成での門の組み立て: 門の行の効き目を行動の量と同じ値に置けば、本の門の順位相関はちょうど一（家族の鍵か単位を取り違えれば一にならない）
+    AN = json.load(open(os.path.join(REPO, 'records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
+    rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
+    units_g = list(T3['directions']['named']) + ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
+    rng_g = np.random.default_rng(23)
+    for drop_g in ([], ['N1|O-Ncold']):
+        eff_g = collections.defaultdict(dict)
+        for r_ in rows_gate:
+            if r_['cell'] in set(drop_g):
+                continue                                               # 外した升目の家族の効き目は置かない（集計の器は引かないはず・裁定 D231）
+            for u in units_g:
+                eff_g[r_['fam']].setdefault(u, float(rng_g.normal()))
+            eff_g[r_['fam']][r_['unit']] = float(r_['y'])
+        G_ = AZ.gates(T3, rows_gate, dict(eff_g), drop_g, ())
+        n_left = sum(1 for r_ in rows_gate if r_['cell'] not in set(drop_g))
+        check(G, '答えの分かる合成での門の組み立て（行の効き目を行動の量に置く・外した升目 %s・裁定 D236）' % ('・'.join(drop_g) or 'なし'),
+              abs(G_['main']['rho'] - 1.0) < 1e-12 and G_['main']['n_rows'] == n_left and G_['desc_choice_a']['rho'] < 1.0 - 1e-9,
+              '本の門の順位相関 %.12f・行 %d（残った門の行 %d）・選択 a の件数の門の順位相関 %.4f（一でない）' % (G_['main']['rho'], G_['main']['n_rows'], n_left, G_['desc_choice_a']['rho']))
 
 
 # ---------------- 二・三. 乱数の小さな模型 ----------------
@@ -334,9 +457,28 @@ def part_model(iso_n, e2e_iso):
     names_ = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])],
               'iso': ['iso:%d' % i for i in range(iso_n)], 'real': ['real:' + p for p in pair_names]}
     sets_run = BR.cell_sign_sets(T3, None, names_['named'], names_['B_random'], names_['iso'], names_['real'], gate_only)
-    MP = BR.run_main_phase(R, T3, FJ, cells, names_, pilot, iso_n=None, log=lambda s: None)
+    pc_calls, fwd = [0], collections.Counter()
+    full_len = {len(c.ids) for c in cells.values()}
+    orig_pc = R.prefix_cache
+    R.prefix_cache = lambda c: (pc_calls.__setitem__(0, pc_calls[0] + 1), orig_pc(c))[1]
+
+    def pre_kw(m, args, kwargs):
+        ids_ = kwargs.get('input_ids') if kwargs.get('input_ids') is not None else (args[0] if args else None)
+        fwd['n'] += 1
+        fwd['past'] += int(kwargs.get('past_key_values') is not None)
+        fwd['use_cache'] += int(bool(kwargs.get('use_cache')))
+        fwd['short'] += int(ids_ is None or int(ids_.shape[-1]) not in full_len)
+    hk_ = model.register_forward_pre_hook(pre_kw, with_kwargs=True)
+    try:
+        MP = BR.run_main_phase(R, T3, FJ, cells, names_, pilot, iso_n=None, log=lambda s: None)
+    finally:
+        hk_.remove()
+        R.prefix_cache = orig_pc
     hd = MP['head']
     check(G2, '本の計算の頭の出口の値の自己検査', hd['logit_check']['pass'], '差の最大 %.2e（許容 %s）' % (hd['logit_check']['max_abs'], hd['logit_check']['tol']))
+    check(G2, '本の計算は近道を使わない（振る舞い: 近道の元を作る呼び出し・使い回す cache・use_cache・列の全長を全ての順伝播で数えた・裁定 D236）',
+          fwd['n'] > 0 and pc_calls[0] == 0 and fwd['past'] == 0 and fwd['use_cache'] == 0 and fwd['short'] == 0,
+          '順伝播 %d 回・近道の元を作った回 %d・cache を渡した回 %d・use_cache が真の回 %d・列の全長でない回 %d' % (fwd['n'], pc_calls[0], fwd['past'], fwd['use_cache'], fwd['short']))
     check(G2, '本の計算は近道を使わない（頭の近道の確かめを走らせない・下見の (v) は記述・裁定 D234）',
           MP['shortcut'] is False and hd.get('shortcut') is False and 'steered_cache_check' not in hd and 'shortcut_rule' in hd,
           '下見の (v) の近道の決定 %s・(v) の差の最大 %.2e（近道の許容 %.4f）' % (pilot['v']['shortcut'], max(abs(x) for x in pilot['v']['diffs'].values()), tol))
@@ -356,6 +498,10 @@ def part_model(iso_n, e2e_iso):
     zt = oz['effects']['zero:test']
     dmx = max(abs(oz['effects'][d] - outs[key_z]['effects'][d]) for d in outs[key_z]['effects'])
     check(G2, '零のベクトルの行は無操作と同じ値になる（別のバッチでも）', abs(zt) <= max(floor, 1e-6), '効き目 %.2e（揺れの床 %.2e）・バッチの組を変えた同じ方向の効き目の差の最大 %.2e（記述）' % (zt, floor, dmx))
+    dirs['nan:test'] = np.full(cfg.hidden_size, np.nan)
+    msg_nan = err_of(lambda: BR.run_cell_sign(R, cells[ck_z], sg_z, ['nan:test', 'static'], batch, seed, kz, pc=None), BR.ToolError)
+    del dirs['nan:test']
+    check(G2, '有限でない値の効き目は器の誤りで止まる（走らせる器の出口・裁定 D236）', msg_nan is not None and '有限でない値' in msg_nan, (msg_nan or '')[:70])
     # バッチの中の位置で方向を取り違えない
     c0, sg0 = items[0]
     r1 = R.forward(c0, [K.NOOP, 'static', 'Nk', 'td'], sg0, full=False)
@@ -478,7 +624,7 @@ def part_model(iso_n, e2e_iso):
     import sweep_Bl3 as SW
     import build_report_Bl3 as BRP
     import transformers
-    sess = {'commit': 'dry-e2e', 'dry': False, 'gpu': 'cpu', 'versions': {'numpy': np.__version__, 'torch': torch.__version__, 'transformers': transformers.__version__},
+    sess = {'commit': 'dry-e2e', 'dry': True, 'gpu': 'cpu', 'versions': {'numpy': np.__version__, 'torch': torch.__version__, 'transformers': transformers.__version__},
             'canon_sha16': sha16f(os.path.join(REPO, 'design', 'contrasts-Bl3.json')), 'directions_npz_sha256': DJ['npz_sha256'], 'layer_idx': L, 'coef': coef, 'finished': 'dry-e2e'}
     sec_part = rt({'part': 'secondary', 'rows_by_cell': sec_rows, 'counts': cnt, 'contexts': sec})
     preds = {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '一部の升目を外して続ける'}}
@@ -488,7 +634,8 @@ def part_model(iso_n, e2e_iso):
 
     def e2e(pilot_e):
         """作った下見の記録で、起動器の相 main の三つの組の出力を作り、手元の一致だけを見る段・結果を開く段・掃き出し・報告の組み立て・走査まで通す。
-        組の置き場の session は DRY でない形にする（本の計算と同じく、下見で外した升目の行を除く v̂ の行のすべてを比べる）。"""
+        組の置き場の session は DRY の形（等方を減らすため・裁定 D236 で DRY でない形は等方が正本の本数でなければ止まる）で、独立の再計算は下見で外した升目の行を除く
+        v̂ の行のすべてを流す。結果を開く段は、一致だけを見る段が読んだ出力の同定と照らしてから開く（裁定 D236）。"""
         pilot_e = rt(pilot_e)
         MPe = BR.run_main_phase(R, T3, FJ, cells, names_e, pilot_e, iso_n=None, log=lambda s: None)
         rows_e, dbr_e = K.recompute_set(T3['main_rows'], pair_names, swaps, len(names_e['iso']), MPe['dropped'])
@@ -497,12 +644,17 @@ def part_model(iso_n, e2e_iso):
         parts = collections.OrderedDict([('main', rt(dict(MPe, part='main'))), ('recompute', rt({'part': 'recompute', 'rows': rows_e, 'n_iso': len(names_e['iso']), 'hook': hook_e, 'rewrite': rw_e})),
                                          ('secondary', sec_part)])
         sessions = collections.OrderedDict((p, dict(sess)) for p in parts)
-        J = AZ.judge(T3, parts, sessions, [pilot_e], pair_names)
-        A = rt(AZ.open_results(T3, FJ, parts, sessions, [pilot_e], pair_names, AN, CB, FB))
+        files = collections.OrderedDict((p_, {'dir': 'e2e', 'json_sha256': hashlib.sha256(json.dumps(v_, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest().upper(),
+                                              'session_sha256': 'dry'}) for p_, v_ in parts.items())
+        J = AZ.judge(T3, parts, sessions, [pilot_e], pair_names, files)
+        A = rt(AZ.open_checked(T3, FJ, parts, sessions, files, J, [pilot_e], pair_names, AN, CB, FB))
+        bad_files = copy.deepcopy(files)
+        bad_files['main']['json_sha256'] = '0' * 64
+        bind_stop = err_of(lambda: AZ.open_checked(T3, FJ, parts, sessions, bad_files, J, [pilot_e], pair_names, AN, CB, FB), SystemExit)
         miss = SW.sweep(T3, A)
         text = BRP.build(T3, A, preds, meta_, [], None, '起草者の行（合成）')
         V, _ = BRP.lint_report(text, T3)
-        return {'MP': MPe, 'rows': rows_e, 'J': J, 'A': A, 'miss': miss, 'text': text, 'V': V, 'pilot': pilot_e}
+        return {'MP': MPe, 'rows': rows_e, 'J': J, 'A': A, 'miss': miss, 'text': text, 'V': V, 'pilot': pilot_e, 'bind_stop': bind_stop}
     # 分かれ道一: 主の升目 N1|O-Ncold と門の行だけの升目を (i)(ii) で外した下見の記録（正本の決定の関数で作る）
     drop_cells = ['N1|O-Ncold'] + gate_only_cells[:1]
     pilot_d = copy.deepcopy(pilot)
@@ -519,6 +671,8 @@ def part_model(iso_n, e2e_iso):
           list(ED['MP']['cells']) == [s[0] for s in sets_e if s[1] not in dset] and [x[0] for x in ED['rows']] == left_static and ED['pilot']['decision']['q1'] == '一部の升目を外して続ける',
           '升目と符号 %d（外す前 %d）・独立の再計算の v̂ の行 %d・下見の決定 %s（外した升目 %s）' % (len(ED['MP']['cells']), len(sets_e), len(ED['rows']), ED['pilot']['decision']['q1'],
                                                                               '・'.join(ED['pilot']['decision']['dropped'])))
+    check(G2, tag_d + ': 結果を開く段は、一致だけを見る段が読んだ出力と違う出力を開かない（裁定 D236）', ED['bind_stop'] is not None and '読んだ出力と違う' in ED['bind_stop'],
+          (ED['bind_stop'] or '')[:70])
     check(G2, tag_d + ': 一致だけを見る段が二段とも一致', ED['J']['agree'] and ED['J']['first'] and ED['J']['second'],
           '一段目 %s・二段目 %s・二段目の値 %s' % (ED['J']['first'], ED['J']['second'], '許容の内' if ED['J'].get('second_values_within_tol') else '許容の外'))
     n_gate_left = sum(1 for r in rows_gate if r['cell'] not in dset)
@@ -655,6 +809,69 @@ def part_rewrite_tool():
     return outs
 
 
+# ---------------- 五. 起動器の三つの相を DRY で別のプロセスとして（裁定 D236） ----------------
+def part_boot(iso_n_boot):
+    """起動器の相 check・pilot・main（三つの組）を DRY で別のプロセスとして走らせ、集計の器の CLI の一致だけを見る段と結果を開く段・掃き出しの CLI・報告の組み立てと走査に通す。
+    一致だけを見る段の後に、組の出力の中身だけを変えた写し（置き場の名は同じ）で結果を開く段が止まることを確かめる。出力は一時の置き場に置き、終わりに消す。"""
+    G = '五'
+    import build_report_Bl3 as BRP
+    td = tempfile.mkdtemp(prefix='dry-boot-')
+    env = dict(os.environ, OP4B_DRY='1', OP4B_REPO_DIR=REPO, OP4B_OUT=td, OP4B_DRY_ISO=str(iso_n_boot), OP4B_DRY_SEC='2', OP4B_DRY_RC='2', PYTHONIOENCODING='utf-8')
+    run = lambda cmd, extra=None: subprocess.run([sys.executable] + cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, env=dict(env, **(extra or {})))
+    newest = lambda prefix: ([d for d in sorted(glob.glob(os.path.join(td, prefix + '-*'))) if os.path.isdir(d)] or [None])[-1]
+    t1 = time.time()
+    try:
+        r_c = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'check'})
+        dc = newest('check')
+        CK = json.load(open(os.path.join(dc, 'check.json'), encoding='utf-8')) if r_c.returncode == 0 and dc else {}
+        cells_ck = CK.get('cells') or {}
+        check(G, '起動器の三つの相（DRY・別のプロセス）: 相 check は順伝播を呼ばずに終わり、呼ばれた数と升目のトークンの並びの SHA16 を書く',
+              r_c.returncode == 0 and CK.get('forward_calls') == 0 and (CK.get('forward_guards') or 0) > 0 and bool(cells_ck) and all('ids_sha16' in v for v in cells_ck.values()),
+              '終わりの値 %d・順伝播を呼んだ数 %s・守り %s・升目 %d' % (r_c.returncode, CK.get('forward_calls'), CK.get('forward_guards'), len(cells_ck)))
+        r_p = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'pilot'})
+        dp = newest('pilot')
+        pj = os.path.join(dp, 'pilot.json') if dp else ''
+        r_m = run(['tools/colab/boot_Bl3.py'], {'OP4B_PHASE': 'main', 'OP4B_DRY_PILOT': pj}) if r_p.returncode == 0 else r_p
+        dm = newest('main')
+        S = json.load(open(os.path.join(dm, 'session.json'), encoding='utf-8')) if r_m.returncode == 0 and dm else {}
+        tags = [z.get('tag') for z in S.get('zips') or []]
+        check(G, '起動器の三つの相（DRY・別のプロセス）: 相 pilot と相 main が終わり、組ごとの出力の SHA-256 を session に書き、組ごとに zip を作る',
+              r_p.returncode == 0 and r_m.returncode == 0 and set(S.get('part_sha256') or {}) == set(('main', 'recompute', 'secondary')) and all('part-%s' % x in tags for x in ('main', 'recompute', 'secondary')),
+              '終わりの値 %d・%d・組の出力の SHA-256 %s・zip %s' % (r_p.returncode, r_m.returncode, sorted(S.get('part_sha256') or {}), tags))
+        jr, ar = os.path.join(td, 'judge.json'), os.path.join(td, 'analysis.json')
+        r_j = run(['tools/analyze_Bl3.py', 'judge', dm, '--pilot', pj, '--out', jr]) if dm else r_m
+        r_o = run(['tools/analyze_Bl3.py', 'open', dm, '--pilot', pj, '--judge-record', jr, '--out', ar]) if r_j.returncode == 0 else r_j
+        r_s = run(['tools/sweep_Bl3.py', ar]) if r_o.returncode == 0 else r_o
+        A = json.load(open(ar, encoding='utf-8')) if r_o.returncode == 0 else None
+        V = None
+        if A:
+            text = BRP.build(T3, A, {'registrant': {'q1.pilot': '続ける'}, 'coordinator': {'q1.pilot': '続ける'}}, {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}, [], None, '起草者の行（合成）')
+            V, _ = BRP.lint_report(text, T3)
+        check(G, '起動器の三つの相（DRY・別のプロセス）: 集計の器の CLI の一致だけを見る段・結果を開く段・掃き出しの CLI・報告の組み立てと走査が通る',
+              r_j.returncode == 0 and r_o.returncode == 0 and r_s.returncode == 0 and V == [] and bool((A or {}).get('inputs')),
+              '終わりの値 %d・%d・%d・走査の違反 %s・結果を開く段の記録に読んだ出力の同定 %s' % (r_j.returncode, r_o.returncode, r_s.returncode, None if V is None else len(V), bool((A or {}).get('inputs'))))
+        stopped_ok, out_t = False, ''
+        if dm and r_j.returncode == 0:
+            t2 = os.path.join(td, 'tampered')
+            os.makedirs(t2)
+            dt = os.path.join(t2, os.path.basename(dm))                  # 置き場の名は同じにして、組の中身だけを変える
+            shutil.copytree(dm, dt)
+            Mt = json.load(open(os.path.join(dt, 'main.json'), encoding='utf-8'))
+            k0 = next(iter(Mt['cells']))
+            d0 = 'Nk' if 'Nk' in Mt['cells'][k0]['effects'] else next(iter(Mt['cells'][k0]['effects']))
+            Mt['cells'][k0]['effects'][d0] += 1000.0
+            json.dump(Mt, open(os.path.join(dt, 'main.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
+            at = os.path.join(td, 'analysis-tampered.json')
+            r_t = run(['tools/analyze_Bl3.py', 'open', dt, '--pilot', pj, '--judge-record', jr, '--out', at])
+            out_t = r_t.stdout + r_t.stderr
+            stopped_ok = r_t.returncode != 0 and '読んだ出力と違う' in out_t and not os.path.exists(at)
+        check(G, '起動器の三つの相（DRY・別のプロセス）: 一致だけを見る段の後に組の出力の中身を変えると、結果を開く段が止まって書かない（裁定 D236）', stopped_ok,
+              ('・'.join([l for l in out_t.split(NL) if '読んだ出力と違う' in l][:1]) or '止まらなかった'))
+    finally:
+        shutil.rmtree(td, ignore_errors=True)
+    return round(time.time() - t1, 1)
+
+
 def main():
     ap = argparse.ArgumentParser()
     ap.add_argument('--force', action='store_true')
@@ -671,6 +888,7 @@ def main():
     part_pure()
     info = part_model(a.iso, a.e2e_iso)
     rw_out = part_rewrite_tool()
+    boot_s = part_boot(a.e2e_iso)
     sha_end = tool_shas()
     check('四', '走らせた器と正本と設計事実と方向の記録が、走りの始めと終わりで同じ', sha_start == sha_end, '%d ファイル%s' % (
         len(sha_start), '' if sha_start == sha_end else '（変わった: %s）' % [k for k in sha_start if sha_start[k] != sha_end.get(k)]))
@@ -679,7 +897,8 @@ def main():
           '- 実の重みで読み取りの値を出していない（正本 `computation.before_seal`）。二と三は、登録機種の設定を小さくした bf16 の乱数の模型（層 %s・次元 %s・正規化の重みを散らした・実の重みではない）と実のトークナイザで走らせた。合成の方向は、実の方向の名だけを借りた乱数。' % (
               info.get('layers'), info.get('dim')),
           '- 等方の方向の本数: %d（正本 %d）。端から端までの分かれ道の等方の本数 %s（作った下見の記録で・起動器の出力と同じ JSON の往復）。' % (a.iso, T3['nulls']['isotropic']['count'], info.get('e2e_iso')),
-          '- 順伝播: 走らせる器 %s 回・書き換えの道 %s 回（変種の計算と四の走りは数えない）・%.0f 秒。' % (info.get('n_forward'), info.get('rewrite_passes'), time.time() - t0),
+          '- 順伝播: 走らせる器 %s 回・書き換えの道 %s 回（変種の計算と四・五の走りは数えない）・%.0f 秒（五の起動器の三つの相 %.0f 秒・等方 %s 本）。' % (
+              info.get('n_forward'), info.get('rewrite_passes'), time.time() - t0, boot_s, a.e2e_iso),
           '- 確かめ: %d のうち %d が期待どおり。' % (len(RESULTS), n_ok), '',
           '| 部 | 確かめ | 結果 | 詳しく |', '|---|---|---|---|'] + [
           '| %s | %s | %s | %s |' % (g, n, '期待どおり' if ok else '**期待と違う**', d.replace('|', '｜')) for g, n, ok, d in RESULTS] + [
````
<<< 終: `tools/dry_run_Bl3.py` の差分 >>>

<<< 始: `design/contrasts-Bl3.json` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/design/contrasts-Bl3.json b/design/contrasts-Bl3.json
index fe08c95..a374349 100644
--- a/design/contrasts-Bl3.json
+++ b/design/contrasts-Bl3.json
@@ -1,7 +1,7 @@
 {
  "id": "Bl3",
- "version": "draft3-r3-2026-09-25",
- "generator": "tools/make_contrasts_Bl3.py v7",
+ "version": "draft3-r4-2026-09-25",
+ "generator": "tools/make_contrasts_Bl3.py v8",
  "note": "段階 B の後・B-lens の後の登録外の記述（小さな登録）。段階 B と B-lens の札・報告・凍結物は変えない。本文と正本が食い違う場合は正本が勝つ。",
  "decisions": {
   "D58": "B の結論の語: B が答えるのは「この抽出の方向の加減が、ランダム方向と区別できる動きを作ったか」まで（段階 B の正本 `decisions`）",
@@ -53,7 +53,10 @@
   "D232": "独立の再計算の札の一致で、割合を決めた裾は等方の外の行だけで比べる（同上）",
   "D233": "独立の再計算の一段目は、無操作の値も比べる（同上）",
   "D234": "本の計算は近道を使わない。独立の再計算の二段目は札の一致で判定し、効き目の差の最大は記録して報告に並べる（値だけが許容の外で札が同じときは止めずに逸脱の台帳に記す）。一段目は値と札の両方で判定する。下見の (v) は記述として残す（同上）",
-  "D235": "正本の小さな直しと限界の足し（採否の案の C の表）を、下見の前の凍結の正本でまとめて入れる（同上）"
+  "D235": "正本の小さな直しと限界の足し（採否の案の C の表）を、下見の前の凍結の正本でまとめて入れる（同上）",
+  "D236": "器の実装の検分（二体）の採否の案の A の表（凍結の前に直す）をすべて採る。走っていた合成データの正式の記録は止め、直した後に取り直す（`records/Bl3/rulings-D236-D237.md`）",
+  "D237": "採否の案の B の表（記録に置く）を採る（同上）",
+  "D238": "直した後に、新しい個体の系統外二名（Gemini）と claude.ai の Claude Opus 5.5 二名に、直しの確かめの検分を頼む（巡を一つ足す・重い所見で直しが大きくなったため）。直しと正式の記録の取り直しの後に、依頼文と束をコーディネータが用意し、登録者が渡す（`records/Bl3/rulings-D238.md`）"
  },
  "scope": {
   "question": "選んだ層で足した方向の、全経路を通った後の効き目（直答の型の読み取りの位置の、選択肢 a の文字の対数オッズの変化）は、多数の等方のランダム方向と、実在の差の方向と、区別できるか",
@@ -201,6 +204,18 @@
    "opinions_adoption": {
     "path": "records/reviews/Bl3/opinions-tools/adoption-proposal-opinions-tools-Bl3.md",
     "sha16": "784B320E390F711F"
+   },
+   "rulings_D236_D237": {
+    "path": "records/Bl3/rulings-D236-D237.md",
+    "sha16": "5F204BC782CA7A39"
+   },
+   "rulings_D238": {
+    "path": "records/Bl3/rulings-D238.md",
+    "sha16": "3F92C29EAF3C662E"
+   },
+   "impl_adoption": {
+    "path": "records/reviews/Bl3/impl/adoption-table-impl-Bl3.md",
+    "sha16": "59680923046A3921"
    }
   },
   "activations": {
@@ -1103,6 +1118,14 @@
    ],
    "budget": "起動の前に、体数・機種・費用を登録者に申告する（独立の再計算の器の書き手を立てるときも同じ）"
   },
+  "impl_recheck": {
+   "gemini": 2,
+   "claude_ai": 2,
+   "fresh": true,
+   "when": "器の直しと合成データの正式の記録の取り直しの後・Colab の相 check の前",
+   "what": "直した器と検分の版からの差分・採否の案・二体の票と確かめ・合成データの正式の記録（束と依頼文はコーディネータが用意し、登録者が渡す）",
+   "why": "器の実装の検分の重い所見で直しが大きくなったので、巡を一つ足す（`review_plan.no_more`・裁定 D238）"
+  },
   "results": {
    "gemini": 2,
    "claude_ai": 2,
@@ -1124,6 +1147,7 @@
    "登録者の確認（草案3）",
    "器と合成データの確かめ（独立の再計算の器は別の個体が書く）",
    "器の実装の検分",
+   "器の直しの確かめ（系統外二名・claude.ai 二名・裁定 D238）",
    "下見の前の凍結と記録先行の公開（正本・方向の npz・器）",
    "封印（下見の前）",
    "下見（決定木を機械で当てる）",
@@ -1150,7 +1174,11 @@
    "零の近くの中央値（零が等方の帰無の四分位の間にある）",
    "Holm の境で一本違う p（独立の再計算の札の一致の判定）",
    "器の誤りでやり直す流れ（一度目の記録と決定を並べる・q1 の採点）",
-   "bf16 相当の揺れを入れた合成の模型（近道の許容の式と、独立の再計算の二段）"
+   "bf16 相当の揺れを入れた合成の模型（近道の許容の式と、独立の再計算の二段）",
+   "本の計算が近道を使わないことの振る舞いの確かめ（近道の元を作る呼び出しの数・使い回す cache・列の全長・裁定 D236）",
+   "正本の文から独立に書いた札と門と、集計の器の出力の突き合わせ（下見で外した升目の場合を含む・裁定 D236）",
+   "等方の外の行が出る枝（等方は正本の本数・割合を決めた裾と側の一致・q7・読みの型・裁定 D236）",
+   "起動器の三つの相を DRY で別のプロセスとして走らせ、集計の器の CLI と報告の組み立てに通す（裁定 D236）"
   ]
  },
  "report_rules": {
@@ -1243,7 +1271,7 @@
   "cost"
  ],
  "numbering": {
-  "rulings_next": "D236"
+  "rulings_next": "D239"
  },
  "clause": "本正本のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"
 }
````
<<< 終: `design/contrasts-Bl3.json` の差分 >>>

<<< 始: `records/Bl3/design-facts-Bl3.json` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/records/Bl3/design-facts-Bl3.json b/records/Bl3/design-facts-Bl3.json
index 2b02246..b77f116 100644
--- a/records/Bl3/design-facts-Bl3.json
+++ b/records/Bl3/design-facts-Bl3.json
@@ -1,8 +1,8 @@
 {
  "kind": "bl3_design_facts",
  "version": "v6",
- "generated_utc": "2026-09-25 03:22",
- "contrasts_sha16": "D41CFA474EA0190E",
+ "generated_utc": "2026-09-25 11:06",
+ "contrasts_sha16": "4531FC51D7075C36",
  "facts": {
   "A": {
    "text": "主の書き出し（甲）: 段階 B の本走行の JSON 直答の出力 725 件の、選択の値の直前までの書き出しは一つにそろう（'```json\\n{\"choice\": \"'）。割り方は 7 トークン（73594「```」・2236「json」・198「⏎」・4913「{\"」・11746「choice」・788「\":」・330「 \"」）で、725 件すべての出力の割り方の頭と一致する。書き出しの次のトークン（読み取りの集合）: a 64・b 65・c 66・d 67（refuse は頭のトークン 1097「ref」）。どの文字を足しても書き出しの割り方は変わらない。JSON 直答の出力の選択の値の最初のトークン: c 725。揺れの版（下見の (iv) だけに使う・V3 は雛形との一致の最後のトークンだけを崩した版）: V1 '{\"choice\": \"'（4 トークン・割り方の境を保つ）／V2 '```json\\n{\\n  \"choice\": \"'（9 トークン・割り方の境を保つ）／V3 '```json\\n{\"choice\":\"'（6 トークン・割り方の境を保つ）。散文の出力（使えた試行のうち JSON 直答の型でないもの）11075 件のうち、選択の鍵の文字列（'\"choice\": \"'）を含むもの 11075 件・主の書き出しの文字列をそのまま含むもの 11075 件（記述）。JSON 直答の型の出力のある升目（全 59 升目のうち 6 升目）: S4|Osec-Ncold+v6b 200・S4|O-Ncold+vNk 160・S4|Osec-Ncold+vrand 156・S4|Osec-Ncold 154・S4|O-Ncold+vrand 38・S4|O-Ncold-vrand 17。refuse を選んだ出力（散文の JSON）51 件の、書き出しの次のトークン: ref 51。割り方の各片（裁定 D220）: 主 「```」・「json」・「⏎」・「{\"」・「choice」・「\":」・「 \"」／V1 「{\"」・「choice」・「\":」・「 \"」／V2 「```」・「json」・「⏎」・「{⏎」・「 」・「 \"」・「choice」・「\":」・「 \"」／V3 「```」・「json」・「⏎」・「{\"」・「choice」・「\":\"」。V3 の頭の 5 トークンは主の書き出しと同じで、最後のトークンだけが違う。段階 B の出力 11800 件（使えなかった試行を含む）のうち、V3 の形の鍵（'\"choice\":\"'）を含むもの 0 件・主の形の鍵（'\"choice\": \"'）を含むもの 11800 件。",
````
<<< 終: `records/Bl3/design-facts-Bl3.json` の差分 >>>

<<< 始: `records/Bl3/design-facts-Bl3.md` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/records/Bl3/design-facts-Bl3.md b/records/Bl3/design-facts-Bl3.md
index 77b2501..6b2ff60 100644
--- a/records/Bl3/design-facts-Bl3.md
+++ b/records/Bl3/design-facts-Bl3.md
@@ -1,4 +1,4 @@
-# B-lens 層三の設計の事実（機械生成・`tools/bl3_facts.py` v6・2026-09-25 03:22 UTC・正本 SHA16 D41CFA474EA0190E）
+# B-lens 層三の設計の事実（機械生成・`tools/bl3_facts.py` v6・2026-09-25 11:06 UTC・正本 SHA16 4531FC51D7075C36）
 
 - 効き目は一つも計算していない（順伝播をしない・方向を模型に足さない）。方向と帰無は作って SHA を取るだけ。
 
````
<<< 終: `records/Bl3/design-facts-Bl3.md` の差分 >>>

<<< 始: `records/Bl3/frozen-diff-Bl3.md` の差分（87ce664 → b77dd22・git diff・囲みは四つの backtick） >>>
````diff
diff --git a/records/Bl3/frozen-diff-Bl3.md b/records/Bl3/frozen-diff-Bl3.md
index ea35ea5..04dc360 100644
--- a/records/Bl3/frozen-diff-Bl3.md
+++ b/records/Bl3/frozen-diff-Bl3.md
@@ -1,11 +1,11 @@
-# B-lens 層三の凍結の本文と草案3 の差の記録（機械生成・`tools/make_frozen_Bl3.py` v2）
+# B-lens 層三の凍結の本文と草案3 の差の記録（機械生成・`tools/make_frozen_Bl3.py` v3）
 
 - 草案3 の原稿 `design/design-Bl3-draft3.src.md` SHA16 ED591E714E93134B（草案3 の組み立ての記録 ED591E714E93134B）・組み立ての器 `tools/build_draft_Bl3.py` SHA16 76B6F8B115B9BFEF（草案3 の本文を最後に変えたコミットの器 76B6F8B115B9BFEF）。
 - (二) 正本の鍵と設計事実から組まれる行の差（同じ原稿を今の正本と設計事実で組み直した本文と、草案3 の本文の差・行の頭の - が草案3・+ が組み直し）:
 
 ```diff
 -- 正本: `design/contrasts-Bl3.json`（版 draft3-r1-2026-09-24・生成器 tools/make_contrasts_Bl3.py v5・再実行で同一バイト）。本文と正本が食い違う場合は正本が勝つ。設計の事実は §6 の転記行（器 `tools/bl3_facts.py`）。
-+- 正本: `design/contrasts-Bl3.json`（版 draft3-r3-2026-09-25・生成器 tools/make_contrasts_Bl3.py v7・再実行で同一バイト）。本文と正本が食い違う場合は正本が勝つ。設計の事実は §6 の転記行（器 `tools/bl3_facts.py`）。
++- 正本: `design/contrasts-Bl3.json`（版 draft3-r4-2026-09-25・生成器 tools/make_contrasts_Bl3.py v8・再実行で同一バイト）。本文と正本が食い違う場合は正本が勝つ。設計の事実は §6 の転記行（器 `tools/bl3_facts.py`）。
 -- **バッチ**: バッチの組み方を凍結する: 升目と符号ごとに、全ての方向（無操作は零のベクトル）を同じ形のバッチで同じフックの道に流す。方向の並びは `readout.primary.order_seed` の種で混ぜ、名前のある方向を一か所に集めない。バッチの大きさは `readout.primary.batch`（段階 B の走行器と同じ・下見の (vi) の (a) が上限を超えたときは一）。升目と符号ごとの方向の数（零のベクトルを含む）がバッチの大きさで割り切れないときは、最後のバッチを零のベクトルで埋めて同じ形にし、埋めた分の値は使わない（数は転記行 E・採否表 P674）。方向ごとに違うベクトルを一つのバッチで足すフックは段階 B に無い新しい道なので、独立の再計算の突き合わせと器の実装の検分の対象にする（バッチの大きさ 16・並びの種 91002）。
 +- **バッチ**: バッチの組み方を凍結する: 升目と符号ごとに、全ての方向（無操作は零のベクトル）を同じ形のバッチで同じフックの道に流す。方向の並びは `readout.primary.order_seed` の種で混ぜ、名前のある方向を一か所に集めない。バッチの大きさは `readout.primary.batch`（段階 B の走行器と同じ・下見の (vi) の (a) が上限を超えたときは一）。升目と符号ごとの方向の数（零のベクトルを含む）がバッチの大きさで割り切れないときは、最後のバッチを零のベクトルで埋めて同じ形にし、埋めた分の値は使わない（数は転記行 E・採否表 P674）。方向ごとに違うベクトルを一つのバッチで足す形は、段階 B の走行器のフックがもともと持つ形（行ごとの方向の行列を受け、段階 B のランダム方向の腕で使った）で、層三の器はこのフックをそのまま呼ぶ。層三では一つのバッチに入る方向の種類が段階 B より大きく増えるので、独立の再計算の突き合わせと器の実装の検分の対象にする（裁定 D226）（バッチの大きさ 16・並びの種 91002）。
 -- **(v) 計算の使い回しの確かめ**: (vi) の後に、本の計算と同じバッチの組み方で、主の升目と門の行だけの升目のすべてについて、プロンプトの主位置より前の計算を使い回す近道と、使い回さない計算の、無操作の読み取りの対数オッズの差の絶対値が近道の許容（`pilot.cache_tol_rule`）以内かを見る。一つの升目でも許容の外なら、本の計算は全ての升目で近道を使わない。
@@ -13,11 +13,11 @@
 -- **下見のデータの扱い**: 下見のデータは本の結果に使わない（本の計算で無操作の値を計算し直す・追補 D の型）。続けたときも止めたときも、計算した下見の記録（(i)〜(vi) の値・(vi) の (a) と (b) の値・外した升目と理由・近道を使うか・バッチの大きさ・揺れの床・近道の許容）を報告に並べる。
 +- **下見のデータの扱い**: 下見のデータは本の結果に使わない（本の計算で無操作の値を計算し直す・追補 D の型）。続けたときも止めたときも、計算した下見の記録（(i)〜(vi) の値・(vi) の (a) と (b) の値・外した升目と理由・(v) の近道の差（記述・本の計算は近道を使わない・裁定 D234）・バッチの大きさ・揺れの床・近道の許容）を報告に並べる。
 -## 6. 転記行（機械生成・逐語・`records/Bl3/design-facts-Bl3.md`〔SHA16 23EA93EC297C2D64〕・正本 `design/contrasts-Bl3.json`〔SHA16 6330B65A0AB503E7〕・生成 2026-09-24 20:02 UTC・器 `tools/bl3_facts.py`）
-+## 6. 転記行（機械生成・逐語・`records/Bl3/design-facts-Bl3.md`〔SHA16 129DE6EEEF55CBE1〕・正本 `design/contrasts-Bl3.json`〔SHA16 D41CFA474EA0190E〕・生成 2026-09-25 03:22 UTC・器 `tools/bl3_facts.py`）
++## 6. 転記行（機械生成・逐語・`records/Bl3/design-facts-Bl3.md`〔SHA16 CFBFF4CADFC9E0CA〕・正本 `design/contrasts-Bl3.json`〔SHA16 4531FC51D7075C36〕・生成 2026-09-25 11:06 UTC・器 `tools/bl3_facts.py`）
 -- **転記行 E** — 主の計算の順伝播: 升目と符号の組 12 × 方向 2034（名前のある方向 4・段階 B の三本 3・等方 1999・実在の差 28）＝ 24408 回（ほかに組ごとの零のベクトル）。門の行だけの組の分（名前のある方向と段階 B の三本だけ）7 回。比べる相手を両方の向きで数えるために足す分（逆の符号の組が主の行に無い組の、実在の差の方向）112 回。バッチ: 大きさ 16（段階 B の正本の `runner.batch` と同じ値であることを器が確かめた）。主の組ごとに方向 ＋ 零のベクトル ＝ 2035 を 128 バッチに入れ、最後のバッチの 13 を零のベクトルで埋める（門の行だけの組は 8 を 1 バッチ・埋める 8／両方の向きのために足す組は 29 を 2 バッチ・埋める 3）。本の計算の頭の近道の確かめ 48 回（主の組 × 近道あり・なし × 加えた一本・零のベクトル）。独立の再計算の見込み 32784 回（新しい道 2〔本の器のフック（近道なし・バッチ一）／残差の書き換え（近道なし・バッチ一）〕× v̂ の行 8 × 〔無操作 ＋ v̂ ＋ 等方 1999 ＋ 比べる相手 48〕）・順伝播のトークン 17,555,832。下見の (vi) の見込み 160 回（(a) 主の升目 × 〔大きさ 16 のバッチの全ての位置 ＋ 大きさ一〕＝ 136・(b) 主の升目 × 繰り返し 3 ＝ 24）。乙の見込み 1260 回以下（文脈 × 名前のある方向と段階 B の三本）と、無操作 180 回（文脈ごと）。一回の順伝播の長さ: 近道（主位置より前の計算を使い回す）なら 8 位置、近道なしならプロンプトの長さ（468〜557）＋ 書き出し 7。乙の文脈（B-lens の層二で選んだ出力）180 件。参考: B-lens の Colab の相 extract は 0.14 ユニット（登録者の表示から）。
 +- **転記行 E** — 主の計算の順伝播: 升目と符号の組 12 × 方向 2034（名前のある方向 4・段階 B の三本 3・等方 1999・実在の差 28）＝ 24408 回（ほかに組ごとの零のベクトル）。門の行だけの組の分（名前のある方向と段階 B の三本だけ）7 回。比べる相手を両方の向きで数えるために足す分（逆の符号の組が主の行に無い組の、実在の差の方向）112 回。バッチ: 大きさ 16（段階 B の正本の `runner.batch` と同じ値であることを器が確かめた）。主の組ごとに方向 ＋ 零のベクトル ＝ 2035 を 128 バッチに入れ、最後のバッチの 13 を零のベクトルで埋める（門の行だけの組は 8 を 1 バッチ・埋める 8／両方の向きのために足す組は 29 を 2 バッチ・埋める 3）。本の計算の頭の近道の確かめ 48 回（主の組 × 近道あり・なし × 加えた一本・零のベクトル・近道を使うときだけの確かめで、本の計算は近道を使わないので走らせない・裁定 D234）。独立の再計算の見込み 32784 回（新しい道 2〔本の器のフック（近道なし・バッチ一）／残差の書き換え（近道なし・バッチ一）〕× v̂ の行 8 × 〔無操作 ＋ v̂ ＋ 等方 1999 ＋ 比べる相手 48〕）・順伝播のトークン 17,555,832。下見の (vi) の見込み 160 回（(a) 主の升目 × 〔大きさ 16 のバッチの全ての位置 ＋ 大きさ一〕＝ 136・(b) 主の升目 × 繰り返し 3 ＝ 24）。乙の見込み 1280 回（文脈ごとに、その升目の門の行のうち方向が名前のある方向か段階 B の三本の行・符号は門の行の符号・裁定 D227）と、そのバッチ 260 回（文脈ごとに行の符号ごとに一つ・零のベクトルの無操作と同じバッチ）。一回の順伝播の長さ: 近道（主位置より前の計算を使い回す・下見の (v) だけ）なら 8 位置、近道なし（本の計算・裁定 D234）ならプロンプトの長さ（468〜557）＋ 書き出し 7。乙の文脈（B-lens の層二で選んだ出力）180 件。参考: B-lens の Colab の相 extract は 0.14 ユニット（登録者の表示から）。
 -- 束縛: 原稿のキー参照を正本 `design/contrasts-Bl3.json`（SHA16 6330B65A0AB503E7）の値で置換した。組み立ての前に束縛検査、後に登録検査と生成器の文字列リテラル検査を走らせた（記録 `records/Bl3/numbers-lint-draft3-Bl3.md`）。
-+- 束縛: 原稿のキー参照を正本 `design/contrasts-Bl3.json`（SHA16 D41CFA474EA0190E）の値で置換した。組み立ての前に束縛検査、後に登録検査と生成器の文字列リテラル検査を走らせた（記録 `（組み直しの一時の置き場の数の検査の記録）`）。
++- 束縛: 原稿のキー参照を正本 `design/contrasts-Bl3.json`（SHA16 4531FC51D7075C36）の値で置換した。組み立ての前に束縛検査、後に登録検査と生成器の文字列リテラル検査を走らせた（記録 `（組み直しの一時の置き場の数の検査の記録）`）。
 +- 独立の再計算の一段目の一致は、二つの道が同じ所から受け取る入力（升目の組み立て・読み取りの集合・層の添字・方向の npz・方向と符号の組・札の関数）の正しさについて何も言わない。比べる相手の除き方と ‖static‖ は、二つの道の外の凍結物（B-lens の凍結の器と転記行 D）に照らす（裁定 D235）
 +- 本物の模型の領域では、足す量の一成分が残差の大きな次元で bf16 の刻みに丸められ、実効の加減の大きさが方向ごとに違いうる（段階 B と同じ算術・小さな乱数の模型では見えない・裁定 D235）
 +- 合成データの確かめは乱数の小さな模型で行い、実の残差の異方性と大きさの突出した次元・語彙の大きさ・GPU の核の選び方と累積の順を写さない（裁定 D235）
@@ -28,12 +28,17 @@
 +  - 最後の層: 層ごとの差分の最後の層の行（選択肢 a の文字の対数オッズの差）が、読み取りの効き目と `computation.layer_tol` 以内で一致することを、本の計算の頭で、近道の確かめの一本（近道の確かめは走らせないが、この一本はここで使う・裁定 D234）と零のベクトルで確かめる（許容 0.0001）。
 -  - 近道の計算の確かめ（加減の掛かった近道を含む）
 +  - 近道の計算の確かめ（近道は下見の (v) の記述だけに使い、本の計算は使わないこと・近道の元の切れ目と cache の列の長さの確かめ・裁定 D231・D234）
++  - 本の計算が近道を使わないことの振る舞いの確かめ（近道の元を作る呼び出しの数・使い回す cache・列の全長・裁定 D236）
++  - 正本の文から独立に書いた札と門と、集計の器の出力の突き合わせ（下見で外した升目の場合を含む・裁定 D236）
++  - 等方の外の行が出る枝（等方は正本の本数・割合を決めた裾と側の一致・q7・読みの型・裁定 D236）
++  - 起動器の三つの相を DRY で別のプロセスとして走らせ、集計の器の CLI と報告の組み立てに通す（裁定 D236）
 -  - 二段目: 本の道（本の計算のバッチの組み方と近道の有無のまま）と、本の器のフック（近道なし・バッチ一）を比べる。許容は近道の許容（`pilot.cache_tol_rule`）と揺れの床の和。本の道の近道とバッチの揺れを見る。本の計算がバッチ一・近道なしのときは、二段目の二つの道は同じ計算になり、二段目は形だけの確かめになる（一段目は変わらない）。
 -  - 一致: 段ごとに、全ての効き目の差の絶対値が許容の内で、かつ段の二つの道の値からそれぞれ出した札が同じとき一致とする。札は、v̂ の行の割合をその道の値で出し直し、主の行すべてに掛け直した Holm の判定・割合を決めた裾（上か下か）・等方の外の行の効き目の側・二つ目の札。
 +  - 二段目: 本の道（本の計算のバッチの組み方のまま・近道は使わない・裁定 D234）と、本の器のフック（近道なし・バッチ一）を比べる。許容は近道の許容（`pilot.cache_tol_rule`）と揺れの床の和（効き目の差の最大が許容の内かを記録と報告に使う・判定は札の一致・裁定 D234）。本の道のバッチの揺れが札を変えないかを見る。本の計算がバッチ一のときは、二段目の二つの道は同じ計算になり、二段目は形だけの確かめになる（一段目は変わらない）。
 +  - 一致: 一段目は、無操作の値と全ての効き目の差の絶対値が許容の内で、かつ段の二つの道の値からそれぞれ出した札が同じとき一致とする（裁定 D233）。二段目は、段の二つの道の値からそれぞれ出した札が同じとき一致とし、効き目の差の最大と、それが許容の内かどうかを記録して、結果を開いた後に報告に並べる。値だけが許容の外で札が同じときは止めずに逸脱の台帳に記す（裁定 D234）。札は、v̂ の行の割合をその道の値で出し直し、主の行すべてに掛け直した Holm の判定・等方の外の行の割合を決めた裾（上か下か・裁定 D232）・等方の外の行の効き目の側・二つ目の札。下見で外した升目の行は比べない。
 -  - 一致しないとき: どちらかの段が一致しなければ、結果を開く前に止め、逸脱の台帳に記して登録者に上げる（裁定 D219）。
 +  - 一致しないとき: どちらかの段が一致しなければ（二段目は札の一致で見る・裁定 D234）、結果を開く前に止め、逸脱の台帳に記して登録者に上げる（裁定 D219）。
++  - 器の直しの確かめ（系統外二名・claude.ai 二名・裁定 D238）
 -  - 計算（頭の自己検査と加減の掛かった近道の確かめ・独立の再計算の二段の判定・結果は登録者と一緒に開く）
 +  - 計算（頭の自己検査・本の計算は近道を使わない・裁定 D234・独立の再計算の二段の判定・結果は登録者と一緒に開く）
 -- 見込み: Colab の 1〜4 ユニット（推論）。計算は升目と符号ごとに文脈が一つなので、方向の数 × 升目と符号の数の順伝播で済む。近道が使えないときは一回の長さがプロンプトの長さまで伸びる（転記行 E）。層ごとの差分は同じ順伝播のついでに取る。乙と独立の再計算と、頭の近道の確かめの分も転記行 E に並べる。順伝播のトークンの数で最も大きいのは、二段にした独立の再計算（近道なし・バッチ一の二つの道）。人の時間は B-lens と同じ段取り（推論）。見積りの入力は〔転記行 E・§6〕。
@@ -45,5 +50,7 @@
   - D226: 「加減のベクトルの足し方は段階 B の走行器のフック（`tools/run_stageB_local.py`）と同じ形にし、方向ごとに違うベクトルを一つのバッチで足す道は層三の器で新しく書く（§3.3）。」→「加減のベクトルの足し方は段階 B の走行器のフック（`tools/run_stageB_local.py`）をそのまま呼ぶ（方向ごとに違うベクトルを一つのバッチで足す形は、このフックがもともと持つ・§3.3・裁定 D226）。」
 
 - 組み直しと凍結の本文の差の残り（(一) と (三) の外）: 確かめていない
+- 凍結版の原稿を同じ手順で組み直した本文と凍結の本文: 確かめていない
+- 凍結の一行（登録者の逐語と日時）は、組み立ての数の検査と禁止語の走査の外に置いた（組み立ての間は決まった代わりの行を置き、組み立ての後に逐語の一行を入れた・裁定 D236）。
 
 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
````
<<< 終: `records/Bl3/frozen-diff-Bl3.md` の差分 >>>
