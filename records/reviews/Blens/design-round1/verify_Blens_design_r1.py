# -*- coding: utf-8 -*-
"""B-lens 設計の巡・第一巡の四票の事実の主張を、正本・設計の事実・トークナイザ・段階 B の試行の記録・凍結した器の本文で確かめる。
**射影は計算しない**（語彙の行列と方向を掛け合わせない。方向どうしの余弦も出さない）。
用法: python records/reviews/Blens/design-round1/verify_Blens_design_r1.py → verify-Blens-design-r1.json"""
import os, re, sys, json, glob, math, inspect, itertools, collections
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
TB = json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8'))
import subprocess
ROUND_COMMIT = 'bb8e27b'   # 票の日の公開の置き場の main（この巡の束の push）。正本・設計の事実・事実の器はこの巡の後の草案2 で作り直したので、票が見た版をここから読む
git_show = lambda rel: subprocess.run(['git', '-C', REPO, 'show', ROUND_COMMIT + ':' + rel], capture_output=True, check=True).stdout.decode('utf-8')
TL = json.loads(git_show('design/contrasts-Blens.json'))
FJ = json.loads(git_show('records/Blens/design-facts-Blens.json'))
B = FJ['facts']['B']
OUT = {}
from transformers import AutoTokenizer
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % TL['inputs']['model']['rev'])
tok = AutoTokenizer.from_pretrained(SNAP)
ids = lambda s: tok(s, add_special_tokens=False)['input_ids']
dec = lambda i: tok.decode([i])
FR = chr(0xFFFD)

# V1 兄弟の対・自分の対だけを除く規則
arms = TL['nulls']['real']['arms']
src_facts = git_show('tools/blens_facts.py')
OUT['V1'] = {'arms': arms, 'rule': TL['nulls']['real']['rule'], 'loaded_pair_in_arms': ('O-Ncold' in arms and 'Osec-Ncold' in arms),
             'facts_tool_loaded_eq_static': "E['loaded'] = E['static']" in src_facts}

# V2 語の規則で比べる相手（C2）と、入れ替えの兄弟（C1）
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read().strip()
F = TB['arms']['files']
ncold = TB['arms']['ncold_text']
text = {'O': rd(F['O']['path']), 'Osec': rd(F['Osec']['path']), 'Onull': rd(F['Onull']['path']), 'Nk': rd(F['Nk']['path']), 'N': ''}
text.update({'O-Ncold': text['O'] + ncold, 'Osec-Ncold': text['Osec'] + ncold, 'Onull-Ncold': text['Onull'] + ncold})
Ew = set(B['E']['static']['plus_all']) | set(B['E']['static']['minus_all'])
sig = {a: frozenset(set(ids(text[a])) & Ew) if text[a] else frozenset() for a in arms}
pairs = list(itertools.combinations(arms, 2))
same_E = [p for p in pairs if sig[p[0]] == sig[p[1]]]
swap = [p for p in pairs if {p[0].replace('-Ncold', ''), p[1].replace('-Ncold', '')} == {'O', 'Osec'}]
Ec = set(B['E']['static']['plus']) | set(B['E']['static']['minus'])            # 中身の語の E（C2 の規則を中身の語で当てた場合）
sigc = {a: frozenset(set(ids(text[a])) & Ec) if text[a] else frozenset() for a in arms}
same_Ec = [p for p in pairs if sigc[p[0]] == sigc[p[1]]]
OUT['V2c'] = {'same_content_E_pairs': ['%s~%s' % p for p in same_Ec], 'n_same_content_E': len(same_Ec), 'Onull_has': sorted(dec(i) for i in sigc['Onull'])}
OUT['V2'] = {'pairs_total': len(pairs), 'same_E_words_pairs': ['%s~%s' % p for p in same_E], 'n_same_E': len(same_E),
             'swap_siblings': ['%s~%s' % p for p in swap], 'n_after_swap_exclusion': len(pairs) - len(swap)}
# V2c の文脈: Onull の本文で中身の E のトークンが現れる所（前後のトークンつき）
toks_on = ids(text['Onull'])
OUT['V2c']['Onull_contexts'] = ['%s〔%s〕%s' % (dec(toks_on[q - 1]) if q else '', dec(toks_on[q]), dec(toks_on[q + 1]) if q + 1 < len(toks_on) else '')
                                for q in range(len(toks_on)) if toks_on[q] in sigc['Onull']]
# V2w 語の単位（O と Osec の違いの十二組の文字列が、腕の本文に部分の文字列として現れるか）と、票の読み（O を含む腕は E+、Osec を含む腕は E− を持ち、ほかの腕は持たない）
opsA = FJ['facts']['A']['ops']
Wp = [o[1] for o in opsA if o[1]]; Wm = [o[2] for o in opsA if o[2]]
sigw = {a: frozenset([('+', w) for w in Wp if w in text[a]] + [('-', w) for w in Wm if w in text[a]]) for a in arms}
same_w = [p for p in pairs if sigw[p[0]] == sigw[p[1]]]
base = lambda a: a.replace('-Ncold', '')
expected = lambda a, sgn: (base(a) == 'O' and sgn == '+') or (base(a) == 'Osec' and sgn == '-')
incid = {a: sorted('%s%s' % (sgn, w) for sgn, w in sigw[a] if not expected(a, sgn)) for a in arms}
sigi = {a: ('+' if base(a) == 'O' else '-' if base(a) == 'Osec' else '') for a in arms}
same_i = [p for p in pairs if sigi[p[0]] == sigi[p[1]]]
OUT['V2w'] = {'same_word_pairs': ['%s~%s' % p for p in same_w], 'n_same_word': len(same_w),
              'incidental': {a: v for a, v in incid.items() if v}, 'Nk_text': text['Nk'], 'ncold_text': ncold,
              'same_intended_pairs': ['%s~%s' % p for p in same_i], 'n_same_intended': len(same_i)}

# V3 断片に割れる字
chars = ['顕', '観', '戦', '撃', '渉', '対', '単', '応', '扱', '綴']
words = ['顕現', '対象', '交渉', '反撃', '静観', '単位', '応じる', '戦略']
OUT['V3'] = {'chars': {c: {'ids': ids(c), 'fragment': any(FR in dec(i) for i in ids(c))} for c in chars},
             'words': {w: [(i, dec(i)) for i in ids(w)] for w in words},
             'E_plus_has_顕': any('顕' in dec(i) for i in B['E']['static']['plus_all'])}

# V4 X の中の幹と JSON の指示の語
SC = json.load(open(j('arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
SCN = {s['question_id']: s for s in SC['scenarios']}
V4 = {}
for sc in ('N1', 'S1'):
    t = SCN[sc]['text']
    stem = t[:t.index('(a)')]
    instr = SC['json_instruction'][SCN[sc]['family']]
    st, it = set(ids(stem)), set(ids(instr))
    X = B['X'][sc]
    V4[sc] = {k: [(i, dec(i), 'stem' if i in st else '', 'instr' if i in it else '') for i in X[k] if i in st or i in it] for k in ('a', 'others')}
V4['nuclear_instruction_mentions'] = {w: w in SC['json_instruction']['nuclear'] for w in ('全面的核使用', '静観', '核')}
OUT['V4'] = V4

# V5 集合をまたぐ重なり
sets = {'L': set(B['L'][x] for x in 'abcd'), 'R': {B['L']['refuse']}, 'E_static+': set(B['E']['static']['plus']), 'E_static-': set(B['E']['static']['minus']),
        'E_td': set(B['E']['td']['plus']), 'E_Nk': set(B['E']['Nk']['plus']), 'X_N1_a': set(B['X']['N1']['a']), 'X_N1_o': set(B['X']['N1']['others']),
        'X_surv_a': set(B['X']['S1']['a']), 'X_surv_o': set(B['X']['S1']['others']), 'F_json': set(B['F']['json']), 'F_prose': set(B['F']['prose']),
        'E_static-_all': set(B['E']['static']['minus_all'])}
OUT['V5'] = {'%s&%s' % (a, b): [(i, dec(i)) for i in sorted(sets[a] & sets[b])] for a, b in itertools.combinations(sets, 2) if sets[a] & sets[b]}

# V6・V7 様式: JSON 直答の出所と散文の最初のトークンの種類
cnt, prose_first = collections.Counter(), collections.Counter()
for sc in ('N1', 'S1', 'SK', 'S4'):
    for arm in TL['token_sets']['noop_arms'][sc]:
        d = j('results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
        T = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}
        R = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
        for k, t in T.items():
            if t['status'] != 'ok':
                continue
            if t['style_b']:
                cnt['%s|%s' % (sc, arm)] += 1
            else:
                first = ids(R[k]['final'])[:1]
                if first:
                    prose_first[first[0]] += 1
OUT['V6'] = {'json_direct_by_cell': dict(cnt)}
OUT['V7'] = {'distinct_prose_first_tokens': len(prose_first), 'top': [(i, dec(i), n) for i, n in prose_first.most_common(10)]}

# V8 X の断片の数え方
per_scene, uniq = 0, {}
for sc in ('N1', 'S1', 'SK', 'S4'):
    op = B['X'][sc]['options']
    a_ids = set(ids(op['a'])); o_ids = set().union(*[set(ids(v)) for k, v in op.items() if k != 'a'])
    fr = [i for i in sorted(a_ids ^ o_ids) if FR in dec(i)]
    per_scene += len(fr); uniq[json.dumps(op, ensure_ascii=False, sort_keys=True)] = len(fr)
OUT['V8'] = {'sum_over_scenes': per_scene, 'sum_over_unique_option_texts': sum(uniq.values()), 'recorded': B['fragments_removed']}

# V9・V10 主位置と加減の掛かる所（凍結した器の本文）
sys.path.insert(0, j('tools'))
steer = open(j('tools', 'steer_B.py'), encoding='utf-8').read()
m = re.search(r'def main_position\(.*?\n(?=def |\Z)', steer, re.S)
OUT['V9'] = {'main_position_src': m.group(0)[:900] if m else None}
runner = open(j('tools', 'run_stageB_local.py'), encoding='utf-8').read()
hooks = [runner[max(0, k.start() - 700):k.start() + 500] for k in re.finditer(r'register_forward_hook', runner)]
OUT['V10'] = {'n_hooks': len(hooks), 'hook_context': hooks[:2]}

# V11 transformers の hidden_states の最後（手元の版の本文）
import transformers
from transformers.models.qwen3 import modeling_qwen3 as MQ
fsrc = inspect.getsource(MQ.Qwen3Model.forward)
try:
    from transformers.utils import generic as G
    rec = inspect.getsource(G)
    k = rec.find('last_hidden_state')
    rec_ctx = rec[max(0, k - 600):k + 300] if k >= 0 else None
except Exception as e:
    rec_ctx = repr(e)
OUT['V11'] = {'version': transformers.__version__, 'forward_has_norm_after_layers': 'self.norm(hidden_states)' in fsrc,
              'forward_collects_hidden_states_itself': 'all_hidden_states' in fsrc, 'recorder_context': rec_ctx}

# V12 等方の帰無の棒（解析の目安）
d = TL['inputs']['model']['hidden_size']
sd = 1 / math.sqrt(d)
OUT['V12'] = {'sd_cos': sd, 'cos_at_p0.0125': stats.norm.isf(0.0125 / 2) * sd, 'cos_at_p0.001': stats.norm.isf(0.001 / 2) * sd}

# V13 ランダム方向の種の取り方
fn = re.search(r'def random_directions\(.*?\n(?=\ndef )', steer, re.S).group(0)
OUT['V13'] = {'asserts_phase': "assert phase in ('tune', 'main')" in fn, 'seed_from_canon': "RC['seed'][phase]" in fn, 'has_arm_argument': 'arm' in fn.split(')')[0]}

# V14 S4 で同じランダム方向を別の土台に加えた行
PH = json.load(open(j('records', 'B', 'posthoc-by-direction-B-2026-09-22.json'), encoding='utf-8'))
rows = {}
for c in PH['contrasts']:
    if c['scenario'] == 'S4':
        rows[c['B']] = [(x['direction_id'], '%d/%d' % (x['cat'], x['n_ok'])) for x in c['directions']]
rows['Osec-Ncold+vrand'] = [(k, '%d/%d' % (v['cat'], v['n_ok'])) for k, v in PH['s4']['Osec-Ncold+vrand']['per_direction'].items()]
OUT['V14'] = rows

# V15 README の段階 B の見出し
README_COMMIT = ROUND_COMMIT   # 票の日の公開の置き場の main（この巡の束の push）。README をあとで直しても、この記録は同じ値を再生する
rm = subprocess.run(['git', '-C', REPO, 'show', README_COMMIT + ':README.md'], capture_output=True, check=True).stdout.decode('utf-8')
OUT['V15'] = {'stageB_heading': [l for l in rm.split('\n') if l.startswith('## 段階 B')], 'has_results_line': '**結果（2026-09-22〜23・公開' in rm}
lines15 = rm.split('\n')
i15 = next(q for q, l in enumerate(lines15) if l.startswith('## 段階 B'))
sec15 = []
for l in lines15[i15 + 1:]:
    if l.startswith('## '):
        break
    sec15.append(l)
now15 = [l for l in sec15 if l.startswith('- **いまどこか**')]
OUT['V15'].update({'readme_commit': README_COMMIT, 'has_sekkeichu_anywhere': '設計中' in rm, 'now_line_count': len(now15),
                   'now_line_status': re.match(r'- \*\*いまどこか\*\*: \*\*([^*]+)\*\*', now15[0]).group(1) if now15 else None,
                   'now_says_no_main_data': bool(now15) and '本走行のデータは一つも無い' in now15[0],
                   'now_says_next_main_run': bool(now15) and '次は選定後の品質床と本走行' in now15[0],
                   'heading_mentions_results': '結果' in lines15[i15]})

# V16〜V20 草案と正本の文
draft = open(j('design', 'design-Blens-draft1.md'), encoding='utf-8').read()
OUT['V16'] = {'draft_says_M_L_scene_independent': 'M_L は場面に依らない' in draft, 'M_L_def': TL['metrics']['M_L']}
OUT['V17'] = {'primary_metrics': TL['primary']['metrics'], 'holm_m': TL['primary']['holm_m'], 'family_in_primary': 'family' in json.dumps(TL['primary'], ensure_ascii=False)}
OUT['V18'] = {'conditions': [r['condition'] for r in TL['reading_rules']], 'mentions_real_null': any('実在' in r['condition'] for r in TL['reading_rules'])}
OUT['V19'] = {'rows_text': TL['calibration']['rows'], 'names_a_file': 'analysis-B' in TL['calibration']['rows'], 'facts_tool_reads': re.findall(r"analysis-B[^']*json", src_facts)}
OUT['V20'] = {'magnitude': {k: TL['magnitude'][k] for k in ('reading', 'reading_ratio', 'per_cell', 'positions')}, 'aggregation_defined': 'aggregat' in json.dumps(TL['magnitude']) or '集約' in json.dumps(TL['magnitude'], ensure_ascii=False)}

json.dump(OUT, open(os.path.join(HERE, 'verify-Blens-design-r1.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
for k, v in OUT.items():
    print(k, json.dumps(v, ensure_ascii=False)[:1500])
