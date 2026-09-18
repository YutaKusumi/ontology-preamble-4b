# -*- coding: utf-8 -*-
"""verify_B_design.py v1 —— 段階 B 設計の検分（一段目・エージェント二体）の所見を、一次記録から機械で出し直す（2026-09-18）。
事前登録 `preregistration-reproduction-B-design.md` の追い問い K1〜K22 に対応する。出力は verification-B-design.{md,json}。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, math, hashlib, datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda *p: hashlib.sha256(open(os.path.join(REPO, *p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
T = json.loads(rd('design', 'contrasts-B.json'))
DFJ = json.loads(rd('records', 'B', 'design-facts-B.json'))
DF = DFJ['facts']
FACTS_MD = rd('records', 'B', 'design-facts-B.md')
DRAFT = rd('design', 'design-stageB-draft6.md')
GEN = rd('tools', 'design_facts_B.py')
CAN_GEN = rd('tools', 'make_contrasts_B.py')
ADC = rd('records', 'reviews', 'AB', 'round-claudeai', 'adoption-table-AB-claudeai.md')
FROZEN_A = rd('design', 'design-stageA-FROZEN.md')
CAN_A = json.loads(rd('design', 'contrasts-A.json'))
REST = rd('records', 'B', 'stageB-restart-2026-09-18.md')
README = rd('README.md')
R = {}


def rec(k, verdict, detail):
    R[k] = {'verdict': verdict, 'detail': detail}


conf = [c for F in T['families'].values() for c in F['contrasts']]
desc = {name: v.get('contrasts', []) for name, v in T['descriptive_families'].items()}
desc_all = [c for v in desc.values() for c in v]

# ---- K1: 転記行 B の数 ----
row_b = re.search(r'^- \*\*転記行 B\*\* — (.+)$', FACTS_MD, re.M).group(1)
printed = {
    '確証': int(re.search(r'確証 (\d+)（', row_b).group(1)),
    '記述': int(re.search(r'・記述 (\d+)（', row_b).group(1)),
    '無操作との差': int(re.search(r'無操作との差 (\d+)', row_b).group(1)),
    'O 減算': int(re.search(r'O 減算 (\d+)', row_b).group(1)),
    '腕対の差方向': int(re.search(r'実在する腕対の差方向 (\d+)', row_b).group(1)),
    'S4 の反証': int(re.search(r'S4 の反証 (\d+)', row_b).group(1)),
    'ランダム方向': int(re.search(r'ランダム方向 (\d+) 本', row_b).group(1)),
    'id 重複': int(re.search(r'id 重複 (\d+)', row_b).group(1)),
}
ids = [c['id'] for c in conf + desc_all]
correct = {'確証': sum(f['m'] for f in T['families'].values()), '記述': len(desc_all),
           '無操作との差': len(desc['B_desc_vs_noop']), 'O 減算': len(desc['B_desc_O_sub']),
           '腕対の差方向': len(desc['B_desc_textdiff']), 'S4 の反証': len(desc['B_desc_S4']),
           'ランダム方向': T['random_control']['count'], 'id 重複': len(ids) - len(set(ids))}
wrong = {k: (printed[k], correct[k]) for k in correct if printed[k] != correct[k]}
fmt_count = len(re.findall(r'%[-+ #0]*\d*(?:\.\d+)?[sdfeg]', re.search(r"F\['B'\] = \{'text': '(.+?)'\n", GEN, re.S).group(1)))
rec('K1', '再現' if wrong else '再現しない',
    {'printed': printed, 'correct': correct, 'mismatched': wrong, 'n_mismatched': len(wrong),
     'format_fields_in_row_B': fmt_count,
     'note': '転記行 B の印字と、正本から数え直した値の突き合わせ。ずれた欄は %d／%d。' % (len(wrong), len(correct)),
     'lint_blind_spot': '数の機械検査は §6（転記行）を登録検査の対象から外している（`tools/numbers_lint.py` の限界の一文）。' if '§6 と §6-補 を除く' in rd('records', 'B', 'numbers-lint-draft6B.md') else '未確認'})

# ---- K2: 同値の帯 ----
FC = DF['C']['data']
n_t, base = FC['tune_n_per_arm'], FC['base']
se_single = 100 * math.sqrt(2 * base * (1 - base) / n_t)
se_diff = 100 * math.sqrt(4 * base * (1 - base) / n_t)
rec('K2', '再現',
    {'printed_band_pt': FC['band_pt'], 'se_single_pt': round(se_single, 3), 'se_diff_pt': round(se_diff, 3),
     'band_from_diff_pt': round(1.96 * se_diff, 3), 'ratio': round(se_diff / se_single, 4),
     'canon_definition': T['selection']['equivalence_band'],
     'note': '正本は「最大の候補との差」の区間と定義する。候補ごとに別の v 腕と vrand 腕があるので分散は 4pq/n で、帯は √2 倍広い。'})

# ---- K3: 正本どおりの選定規則の模擬 ----
rng = np.random.default_rng(20260918)
CAND = T['selection']['candidates']['count']
LAY = T['selection']['candidates']['layers']
COEF = T['selection']['candidates']['coefficients']
grid = [(l, c) for l in LAY for c in COEF]           # 層の浅い順・係数の小さい順に並べる
tie_pt = 1.96 * se_diff


def pick(effects_pt, reps=20000):
    eff = np.array(effects_pt) / 100.0
    pv = np.clip(base - eff, 0.001, 0.999)
    kv = rng.binomial(n_t, pv[None, :], size=(reps, CAND))
    kr = rng.binomial(n_t, base, size=(reps, CAND))
    obs = (kr - kv) / n_t * 100
    best_obs = obs.max(axis=1, keepdims=True)
    tied = obs >= best_obs - tie_pt                    # 同値の帯の内側
    idx = np.argmax(tied, axis=1)                      # 同値なら係数の小さい方・層の浅い方（grid の並び順で最初）
    counts = np.bincount(idx, minlength=CAND) / reps
    true_best = int(np.argmax(eff))
    return counts, float((idx == true_best).mean()), float((np.argmax(obs, axis=1) == true_best).mean())


null_counts, _, _ = pick([0.0] * CAND)
placements = {}
for pos in (0, CAND // 2, CAND - 1):        # 最良の候補を、同値の割り当ての先頭・中ほど・末尾に置いて比べる
    eff = [0.0] * CAND
    eff[pos] = 10.0
    _, pr_rule, pr_argmax = pick(eff)
    placements['best_at_%d（%s・係数 %s）' % (pos, grid[pos][0], grid[pos][1])] = {'canon_rule': round(pr_rule, 3), 'pure_argmax': round(pr_argmax, 3)}
gen_uses_argmax = 'np.argmax(obs, axis=1) == best' in GEN
rec('K3', '一部再現',
    {'tie_band_pt': round(tie_pt, 2), 'grid_order': ['層 %s・係数 %s' % (l, c) for l, c in grid],
     'null_pick_share_first_candidate': round(float(null_counts[0]), 3),
     'null_pick_share': [round(float(x), 3) for x in null_counts],
     'one_best_pick_prob_by_placement': placements,
     'generator_implements_pure_argmax': gen_uses_argmax,
     'note': '正本の規則（最大 → 同値の帯 → 係数の小さい方・層の浅い方）で模擬した。帰無では最も弱い組（層 %s・係数 %s）が選ばれる割合が大きい。真に効く組を格子のどこに置くかで、選べる確率が大きく変わる（同値の割り当ての先頭に置くと高く出る——最初の模擬はここを取り違えていた）。転記行 C の確率は純 argmax の値である。' % (grid[0][0], grid[0][1])})

# ---- K4: S4 の反証の配線 ----
s4 = T['descriptive_families']['B_desc_S4']
s4c = s4['contrasts'][0]
draft_s4 = re.search(r'\*\*S4 は反証の場\*\*（(.+?)）。', DRAFT).group(1)
adjud = [w for w in ('下がった', '判定の規則', '裁定') if w in json.dumps(s4, ensure_ascii=False)]
rec('K4', '再現',
    {'registered_contrast': {'A': s4c['A'], 'B': s4c['B']}, 'sealed_prediction_text': s4['question'],
     'draft_text': draft_s4, 'adjudication_words_found_in_canon': adjud,
     'noop_arm_in_contrast': 'Osec-Ncold' in (s4c['A'], s4c['B']),
     'note': '封印する予想の文は「加算しても下がらない、または上がる」で相手を指定しない。登録された対比の相手はランダム方向の腕である。「下がった」を判定する規則は正本に無い。'})

# ---- K5: ノルム一致の相手 ----
norm_hits = [(p, s) for p, s in [(k, json.dumps(v, ensure_ascii=False)) for k, v in T.items()] if 'ノルム' in s]
canon_norm_text = [x for x in (T['random_control'].get('norm_matched'), T['selection'].get('apply'), json.dumps(T['directions'], ensure_ascii=False)) ]
rec('K5', '再現',
    {'random_control': T['random_control'], 'norm_ratio_in_draft': 'ノルム比' in DRAFT,
     'norm_ratio_in_canon': 'ノルム比' in json.dumps(T, ensure_ascii=False),
     'reference_specified': bool(re.search(r'ノルム(?:は|を)[^、。]*に(?:合わせ|一致)', json.dumps(T, ensure_ascii=False))),
     'sections_mentioning_norm': [k for k, s in norm_hits],
     'note': '正本には「ノルム一致」「ノルムを v̂ に合わせる」の語はあるが、係数の「ノルム比」の定義（何に対する比か）と、ランダム方向が一致させる相手（どの方向のノルムか・層ごとか）を決める欄が無い。'})

# ---- K6: 品質床の射程 ----
op_arms = sorted({a for c in conf + desc_all for a in (c['A'], c['B']) if any(t in a for t in ('+v', '-v'))})
q = T['quality_floor']
rec('K6', '再現',
    {'quality_arms': q['arms'], 'quality_operations': q['operations'], 'quality_cells': q['cells'],
     'intervened_arms_in_run': op_arms, 'n_intervened_arms': len(op_arms),
     'covered': [a for a in op_arms if a in ('O-Ncold-v', 'Onull+v')],
     'uncovered': [a for a in op_arms if a not in ('O-Ncold-v', 'Onull+v')],
     'note': '品質床は確証族の土台への ±v だけを見る。ランダム方向・Nk 方向・腕対の差方向・(6b) の腕は品質床を通らない。'})

# ---- K7: 問い 3 に答える対比 ----
q3 = re.search(r'^3\. 【確証】(.+?)$', DRAFT, re.M).group(1)
cross = T['families']['B_cross']['contrasts']
compares_v_vs_vnk = [c for c in conf + desc_all if set((c['A'], c['B'])) & {'Onull+v'} and set((c['A'], c['B'])) & {'Onull+vNk'}]
rec('K7', '一部再現',
    {'question_3': q3, 'cross_pairs': [(c['A'], c['B']) for c in cross],
     'contrast_comparing_v_and_vNk': [(c['A'], c['B']) for c in compares_v_vs_vnk],
     'arms_exist': [a for a in ('Onull+v', 'Onull+vNk') if a in T['arms']['main']],
     'note': '交差族は「Nk 方向の加算がランダム方向と違うか」を問う。「O の方向と Nk の方向が同じか」を確証で答える対比（v と vNk を直接比べる対比、または方向の一致の検定）は登録されていない。コサイン類似は記述の族にある。'})

# ---- K8: 方向の標本の単位 ----
n_prompt_vecs = len(T['arms']['panel']) * len(T['scenarios']) * len(T['selection']['candidates']['layers'])
per_arm_layer_extract = len(T['extraction_scenarios'])
rec('K8', '再現',
    {'prompt_final_vectors_total': n_prompt_vecs, 'per_arm_layer_in_extraction_scenes': per_arm_layer_extract,
     'facts_I_says': DF['I']['data'], 'descriptive_promises': {k: T['descriptive_families'][k]['question'] for k in ('B_desc_direction', 'B_desc_layer')},
     'note': '主位置の活性は腕 × 場面 × 層で一つに決まる。方向は抽出場面の平均なので、一腕一層あたり抽出場面の点は %d 個しかない。「層ごとの分離」や「層別射影差」を分布の量として出す標本が無い。' % per_arm_layer_extract})

# ---- K9: 選定の指標と書式外 ----
rec('K9', '再現',
    {'selection_metric': T['selection']['metric'], 'censor_denominator': T['censor']['denominator'],
     'format_fail_rule': T['report_rules']['format_fail_denominator'],
     'note': '選定の指標は全分母（n_ok）の破局率の差である。書式外は分母に入り破局に数えないので、書式が崩れるだけで破局率は下がり、操作有効性は上がる側に動く。品質床は選択式の課題で、場面の出力の書式を見ない。'})

# ---- K10: D5 の統制の相手 ----
td = desc['B_desc_textdiff']
rec('K10', '再現',
    {'textdiff_contrasts': [(c['A'], c['B']) for c in td],
     'compares_with_v': [(c['A'], c['B']) for c in td if '+v' == c['B'][-2:] or c['B'].endswith('-v')],
     'note': '腕対の差方向は v_random と比べられている。v との差の差（v の効きが「実在するテキスト差の方向一般」を超えるか）は、正本のどの対比にもない。'})

# ---- K11: §0 の「置いた印」 ----
marks = re.search(r'置いた印（効果は未測）: (.+?)。この印が', DRAFT, re.S).group(1)
a_side_para = 'と同じ側' in FROZEN_A
rec('K11', '一部再現',
    {'marks_in_draft_B': marks, 'gate1_mark_present': '門1 を品質床だけにし' in marks,
     'stage_A_has_same_side_paragraph': a_side_para,
     'stage_A_quote': (re.search(r'^.*と同じ側.*$', FROZEN_A, re.M).group(0)[:200] if a_side_para else None),
     'note': '草案 B の印の一覧に「門1 を品質床だけにする」が入っている。門を緩める決定は、起草者の引かれる向き (a) と同じ側にある。段階 A の凍結本文には「同じ側」を名指す段落がある。'})

# ---- K12: C50 の反映 ----
c50 = re.search(r'^\| C50 \|(.+?)\|\n', ADC, re.M)
rec('K12', '一部再現',
    {'c50_row': c50.group(1).strip() if c50 else None,
     'canon_selection_mentions_exact': any(w in json.dumps(T['selection'], ensure_ascii=False) for w in ('厳密', '最大統計量', '置換')),
     'note': 'C50 は保留 AUC の帯の出し方（厳密分布・候補横断の最大統計量）についての採用である。再設計で AUC は廃したが、候補横断の最大統計量で水準を保つという趣旨は、同値の帯と選定にそのまま当てはまる。正本にはその趣旨が入っていない。'})

# ---- K13: 検閲の分母の語 ----
draft_censor = re.search(r'\*\*検閲（両腕条件）\*\*: (.+?)。', DRAFT).group(1)
rec('K13', '一部再現',
    {'draft_text': draft_censor, 'canon_censor': T['censor'],
     'stage_A_censor_text': CAN_A['censor']['text'][:120],
     'note': '草案の「全分母破局率」は、段階 A の正本と同じ用語法（分子＝破局・分母＝n_ok の率）である。食い違いではなく語の説明が草案に無いだけ、と読める。'})

# ---- K14: 導線と版 ----
now_can = s16('design', 'contrasts-B.json')
rest_can = re.search(r'### 2-1\. 正本 `design/contrasts-B\.json`（[^・]*・SHA16 ([0-9A-F]{16})', REST).group(1)
rest_24 = re.search(r'正本の SHA16 は [0-9A-F]{16} から \*\*([0-9A-F]{16})\*\* に変わった', REST).group(1)
readme_can = re.search(r'正本 JSON `design/contrasts-B\.json`（[^・]*・SHA16 ([0-9A-F]{16})', README).group(1)
rec('K14', '再現',
    {'canon_now': now_can, 'restart_record_2_1': rest_can, 'restart_record_2_4': rest_24, 'readme': readme_can,
     'canon_version_field': T['version'],
     'stale': {'restart_2_4': rest_24 != now_can, 'readme': readme_can != now_can, 'version_field': T['version'] != 'draft6-2026-09-18'},
     'note': '草案6B の組み立てで正本を作り直したので、再開の記録 §2-4 と README の SHA16 と、正本の version の文字列が古い。'})

# ---- K15: ランダム方向の割り当て ----
rec('K15', '再現',
    {'random_control': T['random_control'], 'n_main': T['n_main'],
     'divisible': T['n_main'] % T['random_control']['count'] == 0,
     'note': '正本は「%d 本の試行を合併して一腕とする」と書くが、n=%d をどう割るかは書かれていない（%d では割り切れない）。' % (T['random_control']['count'], T['n_main'], T['random_control']['count'])})

# ---- K16: 完全帰無で少なくとも一本 ----
alpha = T['families']['B_sub']['alpha']
p_any = 1 - (1 - alpha) ** len(T['families'])
rec('K16', '一部再現',
    {'alpha_per_family': alpha, 'n_families': len(T['families']), 'p_at_least_one_upper': round(p_any, 4),
     'canon_upper': T['alpha_upper'], 'fwer_note': T['fwer_note'],
     'print_strings_mentions': any('上界' in v for v in T['print_strings'].values() if isinstance(v, str)),
     'note': '族ごとに α を置くので、完全帰無で少なくとも一つの族が棄却する確率の上界は %.3f（正本の上界 %.2f は三族の和）。報告の定型にこの注意は入っていない。' % (p_any, T['alpha_upper'])})

# ---- K17: 品質床の境目 ----
gen_op = re.search(r'\(\(\(b - a\) / q\) (<=|<) -thr\)', GEN)
rec('K17', '再現',
    {'canon_threshold_word': T['quality_floor']['threshold_pt'], 'canon_pass_rule': T['quality_floor']['pass_rule'],
     'generator_operator': gen_op.group(1) if gen_op else None,
     'strict_flag_present': 'strict' in T['quality_floor'],
     'note': '正本は「threshold_pt の内側」と書き、境目（ちょうど -10 pt）が合格か不合格かを決めていない。転記行 E の計算は「以下」で発火させている。'})

# ---- K18: モンテカルロの記法 ----
reps = sorted(set(int(x) for x in re.findall(r'reps=(\d+)', GEN)))
rec('K18', '再現',
    {'reps_in_generator': reps, 'single_rng': GEN.count('default_rng') == 1,
     'row_C_mentions_reps': any(str(r) in DF['C']['text'] for r in reps),
     'row_E_mentions_reps': any(str(r) in DF['E']['text'] for r in reps),
     'note': '転記行 C・E はモンテカルロの値だが、反復数も区間も印字していない。乱数は一つの発生器を節をまたいで使っている（順序を変えると値が変わる）。'})

# ---- K19: 選定の外挿 ----
rec('K19', '再現',
    {'tune': T['selection']['tune'], 'families': {k: v['question'][:40] for k, v in T['families'].items()},
     'note': '選定は加算族の土台（Onull）・抽出場面だけで行い、選ばれた層 × 係数を減算族・交差族・SK・S4 にも使う。外挿であることが草案に書かれていない。'})

# ---- K20: 用量反応 ----
dose_arms = [a for a in T['arms']['main'] if 'dose' in a.lower()]
rec('K20', '再現',
    {'dose_family': T['descriptive_families']['B_desc_dose'], 'dose_contrasts': len(desc['B_desc_dose']),
     'dose_arms_in_main': dose_arms, 'no_new_preamble_rule': '新しい前置きを作らない' in DRAFT,
     'note': '用量反応（文単位の削除・入替）には、対比も腕も試行も無い。文を削る腕は新しい前置きに当たるので、§4 の「新しい前置きを作らない」と衝突する。'})

# ---- K21: 対比に現れない腕 ----
in_contrast = {a for c in conf + desc_all for a in (c['A'], c['B'])}
in_cells = {c['arm'] for c in T['main_cells']}
orphan = sorted(in_cells - in_contrast)
rec('K21', '再現',
    {'arms_in_cells': len(in_cells), 'arms_in_contrasts': len(in_contrast), 'arms_without_contrast': orphan,
     'trials_for_orphans': sum(c['n'] for c in T['main_cells'] if c['arm'] in orphan),
     'noop_declared': T['arms']['noop'], 'noop_by_scenario': T['arms'].get('noop_by_scenario'),
     'note': '無操作の腕は参照のために置いてあるが、対比に現れない腕が %d 本ある（%s 試行）。草案にその旨の断りが無い。' % (len(orphan), sum(c['n'] for c in T['main_cells'] if c['arm'] in orphan))})

# ---- K22: 主位置の決定性の確かめの範囲 ----
v11 = re.search(r'V11: (.+?)／V22', ADC)
rec('K22', '一部再現',
    {'v11_text': v11.group(1) if v11 else None,
     'scenarios_checked': len(re.findall(r'stage\w+ × (N1|N2|S1|S4|SK)', v11.group(1))) if v11 else 0,
     'note': 'V11 は一つの走行キー・一つの場面での確かめである。4 場面 × 8 腕で主位置の活性が試行に依らないことは、まだ確かめられていない。草案は主位置を試行ごとに保存しないので、後から確かめることもできない。'})

# ---- 出力 ----
counts = {}
for v in R.values():
    counts[v['verdict']] = counts.get(v['verdict'], 0) + 1
now = datetime.datetime.now(datetime.timezone.utc)
out = {'kind': 'verification_B_design', 'version': 'v1', 'generated_utc': now.strftime('%Y-%m-%d %H:%M'),
       'inputs': {'contrasts_B': s16('design', 'contrasts-B.json'), 'draft6B': s16('design', 'design-stageB-draft6.md'),
                  'design_facts_B_md': s16('records', 'B', 'design-facts-B.md'),
                  'agent1': s16('records', 'reviews', 'B', 'design-round1', 'agent-1', 'review.md'),
                  'agent2': s16('records', 'reviews', 'B', 'design-round1', 'agent-2', 'review.md'),
                  'prereg': s16('records', 'reviews', 'B', 'design-round1', 'preregistration-reproduction-B-design.md')},
       'counts': counts, 'items': R,
       'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(out, open(os.path.join(HERE, 'verification-B-design.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
L = ['# 段階 B 設計の検分（一段目）——再現の記録（機械生成・`verify_B_design.py` v1・%s UTC）' % out['generated_utc'], '',
     '- 入力の SHA16: %s' % '・'.join('%s %s' % (k, v) for k, v in out['inputs'].items()), '',
     '- 判定の内訳: %s' % '・'.join('%s %d' % (k, v) for k, v in sorted(counts.items())), '',
     '| K | 判定 | 要点 |', '|---|---|---|']
for k in sorted(R, key=lambda x: int(x[1:])):
    L.append('| %s | %s | %s |' % (k, R[k]['verdict'], R[k]['detail']['note'].replace('|', '／')))
L += ['', '詳細（値と一覧）は `verification-B-design.json`。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(os.path.join(HERE, 'verification-B-design.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[verify_B_design] %s' % ' '.join('%s=%d' % kv for kv in sorted(counts.items())))
for k in sorted(R, key=lambda x: int(x[1:])):
    print('  %-4s %s' % (k, R[k]['verdict']))
