# -*- coding: utf-8 -*-
"""B-lens 設計の巡・第二巡（凍結前の最終検分）の四票の事実の主張を、正本 v2・設計の事実 v2・トークナイザ・段階 B の試行の記録で確かめる。
**射影は計算しない**（語彙の行列と方向を掛け合わせない。方向どうしの余弦も出さない）。V5 の合成の例は乱数だけで作り、模型も方向も使わない。
入力は票の日の公開の置き場（コミット 32f0660）から読む（あとで作り直しても、この記録は同じ値を再生する）。
用法: python records/reviews/Blens/design-round2/verify_Blens_design_r2.py → verify-Blens-design-r2.json"""
import os, re, sys, json, glob, math, itertools, collections, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
ROUND_COMMIT = '32f0660'
git_show = lambda rel: subprocess.run(['git', '-C', REPO, 'show', ROUND_COMMIT + ':' + rel], capture_output=True, check=True).stdout.decode('utf-8')
TL = json.loads(git_show('design/contrasts-Blens.json'))
FJ = json.loads(git_show('records/Blens/design-facts-Blens.json'))
TB = json.loads(git_show('design/contrasts-B.json'))
AT = git_show('records/reviews/Blens/design-round1/adoption-table-Blens-design-r1.md')
FACTS_SRC = git_show('tools/blens_facts.py')
F = FJ['facts']
OUT = {}
from transformers import AutoTokenizer
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % TL['inputs']['model']['rev'])
tok = AutoTokenizer.from_pretrained(SNAP)
import functools
ids = lambda s: tok(s, add_special_tokens=False)['input_ids']
dec = functools.lru_cache(maxsize=None)(lambda i: tok.decode([i]))
FR = chr(0xFFFD)
cal, mag = TL['calibration'], TL['magnitude']

# V1 v̂ を抜いた門の行（G1-1・G2-2-1）
OUT['V1'] = {'gate_without_vhat': cal['gate_without_vhat'], 'eligible_by_direction': F['D']['eligible_by_direction'],
             'rows_all': sum(F['D']['eligible_by_direction'].values()), 'rows_without_static': sum(v for k, v in F['D']['eligible_by_direction'].items() if k != 'static'),
             'text_names_rows': any(w in cal['gate_without_vhat'] for w in ('行を', '行で', '行の'))}
# V2 比の計算の順（G1-2）
OUT['V2'] = {'ratio': mag['ratio'], 'aggregate': mag['aggregate'], 'order_stated': '選んだ出力の中央値）÷ 観測の率の変化' in mag['ratio']}
# V3 負の比の読み（G2-2-2・C1-15）
OUT['V3'] = {'reading': mag['reading'], 'negative_printed': '負の比のまま印字する' in mag['ratio'], 'reading_has_reverse': '逆向き' in mag['reading']}
# V4 門の統計量の単位（G2-2-3）
OUT['V4'] = {'unit': cal['unit'], 'statistic': cal['statistic'], 'row_level_stated': any(w in cal['unit'] for w in ('行の単位', '行の順位'))}

# V5 語の側の帰無の中心（C1-1）: 層の組み立ての差と、合成の例（乱数だけ・模型も方向も使わない）
sp, sm = F['H']['strata_plus'], F['H']['strata_minus']
Np, Nm = sum(sp.values()), sum(sm.values())
keys = sorted(set(sp) | set(sm))
weights = {k: round(sp.get(k, 0) / Np - sm.get(k, 0) / Nm, 4) for k in keys}
rng = np.random.default_rng(20260923)
mu = {k: (0.3 if k.startswith(TL['nulls']['word_side']['char_types'][2]) else 0.0) + 0.05 * int(k.split('|')[1]) for k in keys}   # 層ごとに違う中心（合成の仮定）
pool = {k: rng.normal(mu[k], 1.0, 400) for k in keys}
draws = 4000
null = np.empty(draws)
for d in range(draws):
    a_ = np.concatenate([rng.choice(pool[k], sp[k], replace=False) for k in sp])
    b_ = np.concatenate([rng.choice(pool[k], sm[k], replace=False) for k in sm])
    null[d] = a_.mean() - b_.mean()
center = float(np.mean(null))
m_obs = center - 1.8 * float(np.std(null))                    # 帰無の中心から、零の側へ外れた観測（合成）
p_abs = (1 + np.sum(np.abs(null) >= abs(m_obs))) / (1 + draws)
p_up, p_lo = (1 + np.sum(null >= m_obs)) / (1 + draws), (1 + np.sum(null <= m_obs)) / (1 + draws)
p_eq = min(1.0, 2 * min(p_up, p_lo))
OUT['V5'] = {'rule': TL['percentile']['rule'], 'word_side_rule': TL['nulls']['word_side']['rule'], 'composition_weights': weights,
             'synthetic': {'assumed_stratum_centres': mu, 'null_centre': round(center, 4), 'null_sd': round(float(np.std(null)), 4), 'm_obs': round(m_obs, 4),
                           'p_two_sided_abs': round(float(p_abs), 4), 'p_equal_tailed': round(float(p_eq), 4)}}
# V6 「帰無の方向一般と区別できる」（C1-2・C2-8）
OUT['V6'] = {'print_rule': TL['primary']['print_rule'], 'reading_note': TL['reading_notes'][1], 'second_label': TL['primary']['label_second']}

# V7 語の側の帰無の候補の字数・字の集合・まじりの中身（C1-3・C2-1）
KANJI, KATA, CHOON = (0x4E00, 0x9FFF), (0x30A1, 0x30FA), 0x30FC
n_kanji = lambda s: sum(1 for ch in s if KANJI[0] <= ord(ch) <= KANJI[1])
n_kata = lambda s: sum(1 for ch in s if KATA[0] <= ord(ch) <= KATA[1])
is_frag = lambda i: FR in dec(i)
is_main = lambda i: (n_kanji(dec(i)) + n_kata(dec(i)) > 0) and not (n_kanji(dec(i)) == 0 and n_kata(dec(i)) == 1)
CT = TL['nulls']['word_side']['char_types']


def ctype(i):
    s = dec(i)
    if s and all(KANJI[0] <= ord(ch) <= KANJI[1] for ch in s):
        return CT[0]
    if s and all(KATA[0] <= ord(ch) <= KATA[1] or ord(ch) == CHOON for ch in s):
        return CT[1]
    return CT[2]


def cp932_ok(s):
    try:
        s.encode('cp932'); return True
    except UnicodeEncodeError:
        return False


TXT = {arm: open(j(*TB['arms']['files'][arm]['path'].split('/')), encoding='utf-8').read().strip() for arm in ('O', 'Osec', 'Onull', 'Nk')}
SC = json.load(open(j('arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
SCN = {s['question_id']: s for s in SC['scenarios']}
ctx = set()
for sc in ('N1', 'S1', 'SK', 'S4'):
    ctx |= set(ids(SCN[sc]['text'])) | set(ids(SC['json_instruction'][SCN[sc]['family']]))
excl = set(ids(TXT['O'])) | set(ids(TXT['Osec'])) | ctx
base_vocab = TL['inputs']['model']['base_vocab']
poolv = [i for i in range(base_vocab) if i not in excl and not is_frag(i) and is_main(i)]
by_t = collections.Counter(ctype(i) for i in poolv)
kanji_pool = [i for i in poolv if ctype(i) == CT[0]]
mixed_pool = [i for i in poolv if ctype(i) == CT[2]]
HIRA = (0x3041, 0x3096)
only_jp = lambda s: all(KANJI[0] <= ord(ch) <= KANJI[1] or KATA[0] <= ord(ch) <= KATA[1] or ord(ch) == CHOON or HIRA[0] <= ord(ch) <= HIRA[1] for ch in s)
Ep, Em = F['B']['E']['static']['plus'], F['B']['E']['static']['minus']
OUT['V7'] = {'pool': len(poolv), 'by_type': dict(by_t), 'kanji_single': sum(1 for i in kanji_pool if len(dec(i)) == 1), 'kanji_total': len(kanji_pool),
             'kanji_cp932': sum(1 for i in kanji_pool if cp932_ok(dec(i))), 'mixed_not_only_jp': sum(1 for i in mixed_pool if not only_jp(dec(i))), 'mixed_total': len(mixed_pool),
             'mixed_examples_not_jp': [dec(i) for i in mixed_pool if not only_jp(dec(i))][:8],
             'Eplus_single': sum(1 for i in Ep if len(dec(i)) == 1), 'Eplus_total': len(Ep),
             'Eminus_kanji_single': sum(1 for i in Em if ctype(i) == CT[0] and len(dec(i)) == 1), 'Eminus_kanji_total': sum(1 for i in Em if ctype(i) == CT[0]),
             'E_all_cp932': all(cp932_ok(dec(i)) for i in Ep + Em), 'facts_pool': F['H']['pool']}

# V8 二つの門が別の物差しで通ったとき（C1-4・C2-7）
OUT['V8'] = {'link_rule': cal['link_rule'], 'gate_without_vhat': cal['gate_without_vhat'], 'same_metric_rule': '同じ物差し' in cal['link_rule'] + cal['gate_without_vhat']}
# V9 M_X も survival の三場面で同じ値か（C1-5）
Xs = F['B']['X']
OUT['V9'] = {'or_note': cal['or_note'], 'X_families': {k: v['scenes'] for k, v in Xs.items()}, 'facts_asserts_same_options': "assert all(OPT[s] == OPT[scs[0]] for s in scs)" in FACTS_SRC}
# V10 v̂ を抜いた門に (6b) が残る（C1-6）
OUT['V10'] = {'directions': cal['directions'], 'loaded_rows': F['D']['eligible_by_direction'].get('loaded')}


# V11 段階 B の復号の設定（C1-7・C2-2）
def trials(sc, arm):
    d = j('results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
    return [json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')]


def raws(sc, arm):
    d = j('results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
    return {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}


samp = collections.Counter()
for f in glob.glob(j('results', 'stageB', '*', 'trials-*.jsonl')):
    for l in open(f, encoding='utf-8'):
        samp[json.dumps(json.loads(l).get('sampling'), sort_keys=True)] += 1
OUT['V11'] = {'sampling_in_trials': {k: v for k, v in samp.items()}, 'canon_generation': TB['runner']['generation'], 'canon_top_k': TB['runner']['generation_explicit'].get('top_k'),
              'Blens_quantity': mag['quantity'], 'Blens_has_sampling': any(w in json.dumps(TL, ensure_ascii=False) for w in ('top_k', 'top_p', 'temperature'))}
# V12 比の尺度と床・天井（C1-8・C2-4）
mr = [x for x in F['E']['main_rows'] if x['pass']]
OUT['V12'] = {'main_pass': len(mr), 'main_pass_base_zero': sum(1 for x in mr if x['p0'] == 0), 'ratio': mag['ratio'], 'quantity': mag['quantity'],
              'letter_ceiling_rows': [x['row'] + '|' + x['letter'] for x in F['E']['letter_rows'] if x['pass'] and (x['p1'] in (0.0, 1.0))]}

# V13 答えの文字の位置の分母を JSON 直答の出力の中で数え直す（C1-9・C2-3）
cc = mag['lower_bound']['continuity']


def z2(k0, n0, k1, n1):
    q0, q1 = (k0 + cc) / (n0 + 2 * cc), (k1 + cc) / (n1 + 2 * cc)
    se = math.sqrt(q0 * (1 - q0) / n0 + q1 * (1 - q1) / n1)
    return k1 / n1 - k0 / n0, (k1 / n1 - k0 / n0) / se


def counts_json(sc, arm):
    C = collections.defaultdict(collections.Counter)
    for t in trials(sc, arm):
        if t['status'] == 'ok' and t['style_b']:
            did = t.get('direction_id') or 'fixed'
            C[did][t['choice']] += 1; C[did]['_n'] += 1
    return C


c0 = counts_json('S4', 'Osec-Ncold')['fixed']
rows13 = []
for arm in ('Osec-Ncold+v6b', 'Osec-Ncold+vrand'):
    for did, c1 in sorted(counts_json('S4', arm).items()):
        for x in ('a', 'c'):
            dlt, z = z2(c0[x], c0['_n'], c1[x], c1['_n'])
            rows13.append({'row': 'S4|%s|%s' % (arm, did), 'letter': x, 'n0': c0['_n'], 'k0': c0[x], 'n1': c1['_n'], 'k1': c1[x], 'diff': round(dlt, 4), 'z': round(z, 2),
                           'pass': abs(z) >= mag['lower_bound']['z_min']})
OUT['V13'] = {'noop_json': {k: c0[k] for k in ('a', 'b', 'c', '_n')}, 'rows': rows13, 'facts_letter_rows_use_all_outputs': "c0 = RC[(r['scenario'], base_arm)]['fixed']" in FACTS_SRC,
              'facts_rows': [(x['row'], x['letter'], round(x['z'], 2), x['pass']) for x in F['E']['letter_rows']]}

# V14 全ての JSON 直答の最初のトークン（C1-10）
first = collections.Counter()
per_row_nonfence = collections.Counter()
for d in sorted(glob.glob(j('results', 'stageB', 'stageB__*__s1'))):
    name = os.path.basename(d)[len('stageB__'):-len('__s1')]
    sc, arm = name.split('__', 1)
    R = raws(sc, arm)
    for t in trials(sc, arm):
        if t['status'] == 'ok' and t['style_b']:
            e = ids(R[t['trial_id']]['final'])
            if e:
                first[e[0]] += 1
                if e[0] != F['B']['F']['main']:
                    per_row_nonfence['%s|%s|%s' % (sc, arm, t.get('direction_id') or 'fixed')] += 1
OUT['V14'] = {'first_tokens': {'%d「%s」' % (i, dec(i)): n for i, n in first.most_common()}, 'n_json_direct_all': sum(first.values()), 'rows_with_other_first': dict(per_row_nonfence)}

# V15 文字の前の並びの種類（C1-11・C2-5）
CH = re.compile(r'"choice"\s*:\s*"(a|b|c|d|refuse)"')
R = raws('S4', 'Osec-Ncold')
prefixes, sel_prefixes = collections.Counter(), collections.Counter()
sel = set(F['E']['selected']['S4|Osec-Ncold|json'])
for t in trials('S4', 'Osec-Ncold'):
    if t['status'] != 'ok' or not t['style_b']:
        continue
    txt = R[t['trial_id']]['final']
    ms = list(CH.finditer(txt))
    if not (ms and ms[-1].group(1) == t['choice']):
        continue
    enc = tok(txt, add_special_tokens=False, return_offsets_mapping=True)
    pos = ms[-1].start(1)
    k = [q for q, (s0, s1) in enumerate(enc['offset_mapping']) if s0 <= pos < s1]
    if not k:
        continue
    pre = tuple(enc['input_ids'][:k[0]])
    prefixes[pre] += 1
    if t['trial_id'] in sel:
        sel_prefixes[pre] += 1
top_pre = prefixes.most_common(1)[0]
OUT['V15'] = {'n_candidates': sum(prefixes.values()), 'distinct_prefixes': len(prefixes), 'most_common_prefix_count': top_pre[1], 'most_common_prefix_text': tok.decode(list(top_pre[0])),
              'n_selected': sum(sel_prefixes.values()), 'distinct_selected': len(sel_prefixes), 'selected_counts': sorted(sel_prefixes.values(), reverse=True)}

# V16 下限の境目の近く（C1-12・C2-14）
allz = [(x['row'], 'style', x['z']) for x in F['E']['main_rows']] + [(x['row'], x['letter'], x['z']) for x in F['E']['letter_rows']]
vz = [abs(x['z']) for x in F['E']['main_rows'] if x['kind'] == 'static']
OUT['V16'] = {'near': sorted([(r, w, round(z, 2)) for r, w, z in allz if 1.5 <= abs(z) <= 2.5], key=lambda x: -abs(x[2])), 'vhat_max_abs_z_style': round(max(vz), 2),
              'vhat_row_at_max': [x['row'] for x in F['E']['main_rows'] if x['kind'] == 'static' and abs(x['z']) == max(vz)],
              'letter_pass_min_abs_z': round(min(abs(x['z']) for x in F['E']['letter_rows'] if x['pass']), 2), 'letter_fail_max_abs_z': round(max(abs(x['z']) for x in F['E']['letter_rows'] if not x['pass']), 2)}

# V17 正本の固定の文が禁止語に当たるか（C1-13・C2-6）
ban = TL['print_strings']['value_word_ban'] + TL['print_strings']['mechanism_word_ban'] + TL['print_strings']['reading_never_ban']
hits = []


def walk(x, path):
    if isinstance(x, dict):
        for k, v in x.items():
            if path == '$' and k in ('print_strings', 'print_strings_added', 'decisions', 'clause'):
                continue
            if k == 'never':
                continue
            walk(v, path + '.' + k)
    elif isinstance(x, list):
        for q, v in enumerate(x):
            walk(v, '%s[%d]' % (path, q))
    elif isinstance(x, str):
        for w in ban:
            if w in x:
                hits.append((path, w))


walk(TL, '$')
OUT['V17'] = {'ban_count': len(ban), 'hits': hits}
# V18〜V19 読みの表（C1-14・C1-15・C2-8）
RR = TL['reading_rules']
OUT['V18'] = {'echo_write': RR[0]['write'], 'style_write': RR[3]['write']}
OUT['V19'] = {'types': [r['type'] for r in RR], 'second_only_type': any('二つ目の札だけ' in r['condition'] for r in RR), 's4_signed': '符号' in cal['s4_control']}
# V20 散文の書き出しの「私は」（C1-16）
pc = F['B']['F']['per_cell']
OUT['V20'] = {k: [n for i, n in v if dec(i) == '私は'] for k, v in pc.items() if any(dec(i) == '私は' for i, n in v)}


# V21 採否表に行の無い第一巡の所見（C1 問一）
def findings(path):
    t = open(j(*path.split('/')), encoding='utf-8').read()
    return sorted(set(int(x) for x in re.findall(r'所見 ?(\d+)', t)))


cited = collections.defaultdict(set)
for m in re.finditer(r'\b([GC][12])-(\d+)', AT):
    cited[m.group(1)].add(int(m.group(2)))
R1 = {'G1': 'gemini-1', 'G2': 'gemini-2', 'C1': 'claude-ai-1', 'C2': 'claude-ai-2'}
OUT['V21'] = {tag: {'findings': findings('records/reviews/Blens/design-round1/%s/review.md' % d), 'cited': sorted(cited[tag]),
                    'not_cited': sorted(set(findings('records/reviews/Blens/design-round1/%s/review.md' % d)) - cited[tag])} for tag, d in R1.items()}
# V23 「しそ」と「レーション」（C1 問四）
OUT['V23'] = {'E_dropped': F['B']['E_dropped_chars'], 'X_nuclear_others': [dec(i) for i in Xs['nuclear']['others']]}
# V24 正本の古い値（C1 問五）
OUT['V24'] = {'design_done': TL['review_plan']['design_done'], 'rulings_next': TL['numbering']['rulings_next']}
# V25 第一巡の C2 の所見 6 と 15 の語（C2 の表）
c2 = open(j('records', 'reviews', 'Blens', 'design-round1', 'claude-ai-2', 'review.md'), encoding='utf-8').read()
i6, i7 = c2.index('所見 6【'), c2.index('所見 7【')
i15, i16 = c2.index('所見 15【'), c2.index('所見 16【')
p497 = [l for l in AT.split('\n') if l.startswith('| P497 ')][0]
p510 = [l for l in AT.split('\n') if l.startswith('| P510 ')][0]
OUT['V25'] = {'C2_6_has_単漢字': '単漢字' in c2[i6:i7], 'C2_6_has_多字': '多字' in c2[i6:i7], 'C2_6_word_side_sentence': [s for s in c2[i6:i7].split('\n') if '語の側の帰無' in s],
              'C2_15_text': c2[i15:i16].strip()[:300], 'P497': p497, 'P510': p510}
# V26 S4 の自然の対照の文と転記行 E・D（C2-6）
OUT['V26'] = {'s4_control': cal['s4_control'], 'O_Ncold_style_rows': [(x['row'], round(100 * x['diff'], 1), round(x['z'], 2)) for x in F['E']['main_rows'] if x['row'].startswith('S4|O-Ncold') and x['pass']],
              'collapse_rows': F['D']['collapse_rows']}
# V27 落とした項の向き（C2-9）
OUT['V27'] = {'dropped_term': TL['projection']['dropped_term']}
# V28 予想の第五項（C2-10）
OUT['V28'] = {'item5': TL['predictions']['items'][4], 'word_side_use': TL['nulls']['word_side']['use']}
# V29 検査の外れたときの扱い（C2-11）
OUT['V29'] = {'checks': TL['checks'], 'freeze': TL['token_sets']['freeze'], 'failure_words': [w for w in ('止め', '止ま', '進まない', '記帳して続け') if w in json.dumps(TL['checks'], ensure_ascii=False) + TL['token_sets']['freeze'] + TL['nulls']['B_random']['repro_check']]}
# V30 試行の記録のプロンプトの SHA（C2-12）
t0 = trials('S4', 'Osec-Ncold')[0]
OUT['V30'] = {'trial_keys': sorted(t0.keys()), 'has_prompt_sha': any('prompt' in k for k in t0)}
# V31 「交」は Onull の前置きにあるか（C2-13）
jiao = [i for i in Xs['nuclear']['others'] + Xs['survival']['others'] if dec(i) == '交']
OUT['V31'] = {'jiao_ids': jiao, 'jiao_in_Onull_tokens': [i in set(ids(TXT['Onull'])) for i in jiao], 'Onull_has_交': '交' in TXT['Onull'],
              'Onull_context': [TXT['Onull'][max(0, m.start() - 4):m.end() + 3] for m in re.finditer('交', TXT['Onull'])],
              'X_marks_rule': TL['token_sets']['X_marks']}
# V32 N1 の Onull の散文の出力の頭の字（C2 問4）
Rn = raws('N1', 'Onull')
heads = collections.Counter(Rn[t['trial_id']]['final'][:1] for t in trials('N1', 'Onull') if t['status'] == 'ok' and not t['style_b'])
OUT['V32'] = {'first_chars': dict(heads.most_common(5))}
# V34 「O にだけある語」と禁止語「O に特有」（G2-2-4）
OUT['V34'] = {'echo_write_has_ban': [w for w in ban if w in RR[0]['write']]}
# V35 等方の自己検査の許容（G1・C1・C2 の問三）
nI = TL['nulls']['isotropic']['count']
OUT['V35'] = {'rel_sd_of_sd': round(1 / math.sqrt(2 * (nI - 1)), 4), 'tol': TL['nulls']['isotropic']['analytic_tol'], 'tol_in_sd_units': round(TL['nulls']['isotropic']['analytic_tol'] * math.sqrt(2 * (nI - 1)), 2)}

json.dump(OUT, open(os.path.join(HERE, 'verify-Blens-design-r2.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=str)
for k, v in OUT.items():
    print(k, json.dumps(v, ensure_ascii=False, default=str)[:600])

# V7b 推奨の層が組めるか（cp932 に限る・まじりは漢字か片仮名と平仮名だけ・字数で分ける）と、C1 の 93 と器の 95 の差の中身
def ctype_new(i):
    s = dec(i)
    if not s or not cp932_ok(s) or not only_jp(s):
        return None
    if all(KANJI[0] <= ord(ch) <= KANJI[1] for ch in s):
        return CT[0]
    if all(KATA[0] <= ord(ch) <= KATA[1] or ord(ch) == CHOON for ch in s):
        return CT[1]
    return CT[2]


cells = collections.Counter()
for i in poolv:
    t_ = ctype_new(i)
    if t_:
        cells['%s|%s' % (t_, '一字' if len(dec(i)) == 1 else '二字以上')] += 1
need = collections.Counter('%s|%s' % (ctype_new(i), '一字' if len(dec(i)) == 1 else '二字以上') for i in Ep + Em)
PUNCT_OR_SPACE = lambda s: any(ch.isspace() or ord(ch) < 0x80 or ch in '，。、！？：；（）「」『』・…―' for ch in s)
extra = [dec(i) for i in mixed_pool if not only_jp(dec(i)) and not PUNCT_OR_SPACE(dec(i))]
OUT['V7b'] = {'cells': dict(cells), 'need': dict(need), 'mixed_not_jp_space_ascii_punct': sum(1 for i in mixed_pool if PUNCT_OR_SPACE(dec(i))), 'extra_not_jp_but_no_space_punct': extra}
json.dump(OUT, open(os.path.join(HERE, 'verify-Blens-design-r2.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=str)
print('V7b', json.dumps(OUT['V7b'], ensure_ascii=False))
