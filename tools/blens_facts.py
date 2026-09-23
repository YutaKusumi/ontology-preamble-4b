# -*- coding: utf-8 -*-
"""blens_facts.py v2 —— B-lens の枠に置く設計の事実（転記行 A〜H）を、記録と凍結物から機械で作る。**射影は一つも計算しない**（語彙の行列と方向を掛け合わせない）。
v2（2026-09-23・草案2・裁定 D168〜D176）: 片仮名一字を主から外し、感度の集合を並べる／落ちた字を元の語ごとに印字する／X の断片を異なる選択肢の文ごとに数える／
X の幹と指示の印／集合の重なり／様式の主（一つのトークン）と感度（なぞりを除いた散文の書き出し）／校正の方向の単位と崩れの行／
大きさの目盛りの層・下限を超えた行・選んだ試行（転記行 E）／語の側の帰無の候補（転記行 H・語彙の行のノルムだけを使い、方向とは掛けない）。
出力: records/Blens/design-facts-Blens.json・records/Blens/design-facts-Blens.md
語の集合はここでは下書きで、凍結は器 `tools/blens_sets.py` が同じ規則で作り直して行い、バイトで一致することを確かめる。
用法: python tools/blens_facts.py [--tokenizer 置き場] [--skip-weights-hash]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, math, hashlib, difflib, argparse, datetime, collections
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
VERSION = 'v2'
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
ACT = os.path.expanduser('~/.cache/op4b-dir/dirB__s1/main_position_activations.npz')
ap = argparse.ArgumentParser()
ap.add_argument('--tokenizer', default=os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
ap.add_argument('--skip-weights-hash', action='store_true')
a = ap.parse_args()
s16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read().strip()
TB = json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8'))
TL = json.load(open(j('design', 'contrasts-Blens.json'), encoding='utf-8'))
FILES = TB['arms']['files']
for arm in ('O', 'Osec', 'Onull', 'Nk'):
    assert s16f(j(*FILES[arm]['path'].split('/'))) == TB['arms']['sha16'][arm], arm
TXT = {arm: rd(FILES[arm]['path']) for arm in ('O', 'Osec', 'Onull', 'Nk')}
NCOLD = TB['arms']['ncold_text']
SC = json.load(open(j('arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
SCN = {s['question_id']: s for s in SC['scenarios']}
SCENES = ['N1', 'S1', 'SK', 'S4']
FAM = {sc: SCN[sc]['family'] for sc in SCENES}
F = {}

# ---------------- 転記行 A: O と Osec の差 ----------------
O, S = TXT['O'], TXT['Osec']
sm = difflib.SequenceMatcher(None, O, S, autojunk=False)
_raw = sm.get_opcodes()
MERGE = TL['token_sets']['diff_merge']
ops_pos, cur = [], None
for t, i1, i2, j1, j2 in _raw:                          # 短い一致（MERGE 字未満）をはさむ違いは一つの組にまとめる（語の単位で読むため）
    if t == 'equal':
        if cur and i2 - i1 < MERGE and i2 < len(O):
            cur = [cur[0], i2, cur[2], j2]
            continue
        if cur:
            ops_pos.append(cur); cur = None
        continue
    cur = [cur[0], i2, cur[2], j2] if cur else [i1, i2, j1, j2]
if cur:
    ops_pos.append(cur)
ops = [('replace', O[i1:i2], S[j1:j2]) for i1, i2, j1, j2 in ops_pos]
same = sum(i2 - i1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t == 'equal')
shared = [w for w in ('共創', '再帰的自己改善', '私と共に在り続ける者よ', 'かくの如く来たり', '慈悲を核として', '思いやりを核として') if w in O and w in S]
absent = [w for w in ('相互依存',) if w not in O and w not in S]
F['A'] = {'text': 'O（%d 字・`%s`）と Osec（%d 字・`%s`）を文字で突き合わせた（`difflib`・器 `tools/blens_facts.py`）。共通の文字 %d。違う所（O → Osec）: %s。両方にある句: %s。どちらにも無い語: %s。'
          % (len(O), FILES['O']['path'], len(S), FILES['Osec']['path'], same, '／'.join('「%s」→「%s」' % (x, y) for t, x, y in ops), '・'.join('「%s」' % w for w in shared), '・'.join('「%s」' % w for w in absent)),
          'ops': ops, 'same': same, 'len_O': len(O), 'len_Osec': len(S)}

# ---------------- トークナイザと字の規則 ----------------
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(a.tokenizer)
ids = lambda s: tok(s, add_special_tokens=False)['input_ids']
encf = lambda s: tok(s, add_special_tokens=False, return_offsets_mapping=True)
import functools
dec = functools.lru_cache(maxsize=None)(lambda i: tok.decode([i]))
FR = chr(0xFFFD)
base_vocab = min(tok.added_tokens_decoder.keys())
assert base_vocab == TL['inputs']['model']['base_vocab'] and len(tok) == TL['inputs']['model']['tokenizer_len'], (base_vocab, len(tok))
KANJI, KATA, CHOON = (0x4E00, 0x9FFF), (0x30A1, 0x30FA), 0x30FC          # 漢字・片仮名の字（中黒と長音符は字に数えない）
n_kanji = lambda s: sum(1 for ch in s if KANJI[0] <= ord(ch) <= KANJI[1])
n_kata = lambda s: sum(1 for ch in s if KATA[0] <= ord(ch) <= KATA[1])
is_frag = lambda i: FR in dec(i)
content_any = lambda i: n_kanji(dec(i)) + n_kata(dec(i)) > 0
single_kata = lambda i: n_kanji(dec(i)) == 0 and n_kata(dec(i)) == 1
is_main = lambda i: content_any(i) and not single_kata(i)


def split(raw):
    raw = sorted(raw)
    nf = [i for i in raw if not is_frag(i)]
    return {'main': [i for i in nf if is_main(i)], 'kata1': [i for i in nf if content_any(i)], 'all': nf, 'fragments': [i for i in raw if is_frag(i)]}


def frag_chars(text, raw_ids):
    e = encf(text)
    return [(s0, s1, text[s0:s1]) for i, (s0, s1) in zip(e['input_ids'], e['offset_mapping']) if i in raw_ids and is_frag(i)]


instr = SC['json_instruction']
ctx_ids = set()
for sc in SCENES:
    ctx_ids |= set(ids(SCN[sc]['text'])) | set(ids(instr[FAM[sc]]))
tO, tS, tN, tK = set(ids(O)), set(ids(S)), set(ids(TXT['Onull'])), set(ids(TXT['Nk']))

# ---------------- 語の反響 E ----------------
E_raw = {'static': ((tO - tS) - ctx_ids, (tS - tO) - ctx_ids), 'td': (tN - ctx_ids, set()), 'Nk': (tK - ctx_ids, set())}
E = {}
for k, (p, m) in E_raw.items():
    sp, sm_ = split(p), split(m)
    E[k] = {'plus': sp['main'], 'minus': sm_['main'], 'plus_kata1': sp['kata1'], 'minus_kata1': sm_['kata1'], 'plus_all': sp['all'], 'minus_all': sm_['all'],
            'fragments': sp['fragments'] + sm_['fragments'], 'single_kata_removed': sorted(set(sp['kata1']) - set(sp['main'])) + sorted(set(sm_['kata1']) - set(sm_['main']))}
E['loaded'] = E['static']                              # (6b) の二腕は Ncold の一行を共有するので、違う語は O と Osec の差と同じ


def word_at(pos, spans, text):
    for s0, s1 in spans:
        if s0 <= pos < s1:
            return text[s0:s1]
    return None


drop_E = collections.OrderedDict()
for side, text, raw, spans in (('O', O, E_raw['static'][0], [(p[0], p[1]) for p in ops_pos]), ('Osec', S, E_raw['static'][1], [(p[2], p[3]) for p in ops_pos]),
                               ('Onull', TXT['Onull'], E_raw['td'][0], []), ('Nk', TXT['Nk'], E_raw['Nk'][0], [])):
    for s0, s1, ch in frag_chars(text, raw):
        w = word_at(s0, spans, text) or ('…%s…' % text[max(0, s0 - 2):s1 + 2])
        drop_E.setdefault('%s「%s」' % (side, w), [])
        if ch not in drop_E['%s「%s」' % (side, w)]:
            drop_E['%s「%s」' % (side, w)].append(ch)


# ---------------- 選択肢の語 X（家族ごと）----------------
def options(text):
    ms = list(re.finditer(r'\(([a-d])\)', text))
    out = {}
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else text.index('。', m.end())
        out[m.group(1)] = text[m.end():end].strip().rstrip('、').strip()
    return out


OPT = {sc: options(SCN[sc]['text']) for sc in SCENES}
fam_scenes = collections.OrderedDict()
for sc in SCENES:
    fam_scenes.setdefault(FAM[sc], []).append(sc)
X, drop_X, xfrag = {}, collections.OrderedDict(), {}
for fam, scs in fam_scenes.items():
    assert all(OPT[s] == OPT[scs[0]] for s in scs), ('同じ家族の選択肢の文が違う', fam)
    sc = scs[0]
    op = OPT[sc]
    a_ids = set(ids(op['a']))
    o_ids = set().union(*[set(ids(v)) for k, v in op.items() if k != 'a'])
    ra, ro = a_ids - o_ids, o_ids - a_ids
    sa, so = split(ra), split(ro)
    stem = SCN[sc]['text'][:SCN[sc]['text'].index('(a)')]
    stem_ids, instr_ids = set(ids(stem)), set(ids(instr[fam]))
    mark = lambda i: [m for m, S_ in (('stem', stem_ids), ('instr', instr_ids)) if i in S_]
    X[fam] = {'scenes': scs, 'options': op, 'a': sa['main'], 'others': so['main'], 'a_kata1': sa['kata1'], 'others_kata1': so['kata1'], 'a_all': sa['all'], 'others_all': so['all'],
              'marks': {str(i): mark(i) for i in sa['main'] + so['main'] if mark(i)},
              'a_unmarked': [i for i in sa['main'] if not mark(i)], 'others_unmarked': [i for i in so['main'] if not mark(i)],
              'single_kata_removed': sorted(set(sa['kata1']) - set(sa['main'])) + sorted(set(so['kata1']) - set(so['main']))}
    xfrag[fam] = len(sa['fragments']) + len(so['fragments'])
    for letter_, text in op.items():
        for s0, s1, ch in frag_chars(text, ra | ro):
            key = '%s (%s)「%s」' % (fam, letter_, text)
            drop_X.setdefault(key, [])
            if ch not in drop_X[key]:
                drop_X[key].append(ch)

# ---------------- 答えの文字 L と拒否 R ----------------
letter = {}
for x in ('a', 'b', 'c', 'd', 'refuse'):
    seq = ids('{"choice": "%s"' % x)
    pre = ids('{"choice": "')
    assert seq[:len(pre)] == pre, x
    letter[x] = seq[len(pre)]


def trials_raw(sc, arm):
    d = j('results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
    T = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}
    R = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
    return [(T[k], R[k]) for k in sorted(T, key=lambda k: T[k]['trial_index'])]


def row_counts(sc, arm):
    d = j('results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
    C = collections.defaultdict(collections.Counter)
    for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8'):
        t = json.loads(l)
        if t['status'] != 'ok':
            continue
        did = t.get('direction_id') or 'fixed'
        C[did][t['choice']] += 1
        C[did]['_n'] += 1
        C[did]['_style'] += 1 if t['style_b'] else 0
    return C


# ---------------- 様式 F と、大きさの目盛りの候補 ----------------
CH = re.compile(r'"choice"\s*:\s*"(a|b|c|d|refuse)"')
first = collections.defaultdict(collections.Counter)
letter_cov = collections.defaultdict(collections.Counter)
cands = collections.defaultdict(list)
noop = TL['token_sets']['noop_arms']
for sc in SCENES:
    for arm in noop[sc]:
        for t, r in trials_raw(sc, arm):
            if t['status'] != 'ok':
                continue
            txt = r['final']
            e = encf(txt)
            style = 'json' if t['style_b'] else 'prose'
            if e['input_ids']:
                first[(sc, arm, style)][e['input_ids'][0]] += 1
            ms = list(CH.finditer(txt))
            if ms and ms[-1].group(1) == t['choice']:
                pos = ms[-1].start(1)
                cover = [i for i, (s0, s1) in zip(e['input_ids'], e['offset_mapping']) if s0 <= pos < s1]
                if cover:
                    letter_cov[t['choice']][cover[0]] += 1
                    cands[(sc, arm, style)].append((t['trial_index'], t['trial_id'], t['preamble_sha']))
first_json, first_prose = collections.Counter(), collections.Counter()
for (sc, arm, style), c in first.items():
    (first_json if style == 'json' else first_prose).update(c)
f_main, f_main_n = first_json.most_common(1)[0]
assert dec(f_main) == '```', dec(f_main)
json_cells = sorted('%s|%s' % (sc, arm) for (sc, arm, style), c in first.items() if style == 'json' and sum(c.values()))
echo = set()
for t_ in [TXT['O'], TXT['Osec'], TXT['Onull'], TXT['Nk'], NCOLD] + [SCN[s]['text'] for s in SCENES] + [instr[f] for f in fam_scenes]:
    echo |= set(ids(t_))
other_sets = set(letter.values()) | {f_main}
for k in ('static', 'td', 'Nk'):
    other_sets |= set(E[k]['plus']) | set(E[k]['minus'])
for fam in X:
    other_sets |= set(X[fam]['a']) | set(X[fam]['others'])
K_F = TL['token_sets']['F_top']
prose_rank = [i for i, _ in first_prose.most_common()]
why_out = {}
for i in prose_rank:
    w = [m for m, c in (('断片', is_frag(i)), ('なぞり', i in echo), ('重なり', i in other_sets)) if c]
    if w:
        why_out[i] = w
f_sens = [i for i in prose_rank if i not in why_out][:K_F]
f_prose_top_raw = [i for i in prose_rank if not is_frag(i)][:K_F]
FSET = {'main': f_main, 'main_n': f_main_n, 'n_json_first': sum(first_json.values()), 'n_prose_first': sum(first_prose.values()), 'json_cells': json_cells,
        'prose_distinct': len(first_prose), 'prose_sens': f_sens, 'prose_top_raw': f_prose_top_raw, 'prose_excluded_in_top': {str(i): why_out[i] for i in prose_rank[:K_F * 2] if i in why_out},
        'per_cell': {'%s|%s|%s' % k: [[i, n] for i, n in c.most_common(3)] for k, c in sorted(first.items()) if sum(c.values())}}
lv = {x: {'canonical': letter[x], 'observed': dict(letter_cov[x].most_common())} for x in ('a', 'b', 'c', 'd', 'refuse')}

# ---------------- 集合の重なり ----------------
SETS = collections.OrderedDict([('L', set(letter[x] for x in 'abcd')), ('R', {letter['refuse']}), ('E_static+', set(E['static']['plus'])), ('E_static−', set(E['static']['minus'])),
                                ('E_td+', set(E['td']['plus'])), ('E_Nk+', set(E['Nk']['plus']))] +
                               [('X_%s_%s' % (fam, s_), set(X[fam][k_])) for fam in X for s_, k_ in (('a', 'a'), ('o', 'others'))] +
                               [('F_main', {f_main}), ('F_prose_top', set(f_prose_top_raw)), ('F_prose_sens', set(f_sens))])
names = list(SETS)
DERIVED = {frozenset(('F_prose_top', 'F_prose_sens'))}                      # 感度の集合は上位の部分なので、この組の重なりは数えない
overlaps = [(names[p], names[q], sorted(SETS[names[p]] & SETS[names[q]])) for p in range(len(names)) for q in range(p + 1, len(names))
            if SETS[names[p]] & SETS[names[q]] and frozenset((names[p], names[q])) not in DERIVED]
assert not (SETS['F_prose_sens'] & (other_sets | echo)), '様式の感度の集合がほかの集合かなぞりの語と重なる'

show = lambda L: '・'.join('%d「%s」' % (i, dec(i).replace('\n', '⏎')) for i in L)
showw = lambda L: '・'.join('「%s」' % dec(i).replace('\n', '⏎') for i in L)
F['B'] = {'text': ('答えの文字（L）: %s。B の無操作の出力で、選択の値の最初の文字を覆うトークン: %s。拒否（R）: %d「%s」（値は二つのトークンに割れる）。'
                   '語の反響（E・主＝中身の語から片仮名一字を除く）: v̂ と (6b) の E+（O にだけある語）%d 個＝%s／E−（Osec にだけある語）%d 個＝%s／td の E+（Onull にだけある語）%d 個／Nk の E+ %d 個＝%s。'
                   '感度の集合の数（片仮名一字を含む中身の語／全てのトークン）: v̂ の E+ %d／%d・E− %d／%d・td %d／%d・Nk %d／%d。主から外した片仮名一字: %s。'
                   '断片で落ちた字（元の語ごと）: %s。'
                   '選択肢の語（X・家族ごと・主）: %s。X の断片の数（異なる選択肢の文ごと）: %s。断片で落ちた字（選択肢の文ごと）: %s。'
                   '様式（F）: 主はコードブロックの書き出し %d「%s」（JSON 直答の出力 %d 件のうち %d 件の最初のトークン・JSON 直答のある升目は %s のみ）。散文の出力 %d 件の最初のトークンの種類 %d。散文の書き出しの上位（断片を除く）: %s。'
                   'なぞりと重なりと断片を除いた散文の書き出し（様式の感度・上位 %d）: %s。上位で除いたもの: %s。'
                   '集合の重なり: %s。場面の本文と JSON の指示にある語は E から除いた。語の数はトークンの数。td の E+ の一覧と、升目ごとの最初のトークンの件数は記録の JSON にある。')
          % ('・'.join('%s＝%d' % (x, letter[x]) for x in ('a', 'b', 'c', 'd')),
             '／'.join('%s: %s' % (x, '・'.join('%d×%d' % (i, n) for i, n in letter_cov[x].most_common())) for x in ('a', 'b', 'c', 'd', 'refuse') if letter_cov[x]),
             letter['refuse'], dec(letter['refuse']),
             len(E['static']['plus']), show(E['static']['plus']), len(E['static']['minus']), show(E['static']['minus']), len(E['td']['plus']), len(E['Nk']['plus']), show(E['Nk']['plus']),
             len(E['static']['plus_kata1']), len(E['static']['plus_all']), len(E['static']['minus_kata1']), len(E['static']['minus_all']), len(E['td']['plus_kata1']), len(E['td']['plus_all']), len(E['Nk']['plus_kata1']), len(E['Nk']['plus_all']),
             showw(sorted(set(E['static']['single_kata_removed'] + E['td']['single_kata_removed'] + E['Nk']['single_kata_removed']))) or '無し',
             '／'.join('%s: %s' % (k, '・'.join(v)) for k, v in drop_E.items()) or '無し',
             '／'.join('%s（%s・(a)「%s」）X_a %d 個＝%s・X_o %d 個＝%s（片仮名一字を含む集合では %d・%d 個、全てのトークンでは %d・%d 個。幹か指示の印: %s。主から外した片仮名一字: %s）'
                      % (fam, '・'.join(X[fam]['scenes']), X[fam]['options']['a'], len(X[fam]['a']), show(X[fam]['a']), len(X[fam]['others']), show(X[fam]['others']),
                         len(X[fam]['a_kata1']), len(X[fam]['others_kata1']), len(X[fam]['a_all']), len(X[fam]['others_all']),
                         '・'.join('「%s」（%s）' % (dec(int(i)), '・'.join(m)) for i, m in X[fam]['marks'].items()) or '無し', showw(X[fam]['single_kata_removed']) or '無し') for fam in X),
             '・'.join('%s %d' % kv for kv in xfrag.items()),
             '／'.join('%s: %s' % (k, '・'.join(v)) for k, v in drop_X.items()) or '無し',
             f_main, dec(f_main), FSET['n_json_first'], f_main_n, '・'.join(json_cells), FSET['n_prose_first'], FSET['prose_distinct'], show(f_prose_top_raw),
             K_F, show(f_sens), '・'.join('「%s」（%s）' % (dec(int(i)).replace('\n', '⏎'), '・'.join(w)) for i, w in FSET['prose_excluded_in_top'].items()) or '無し',
             '／'.join('%s と %s: %s' % (p, q, showw(v)) for p, q, v in overlaps) or '無し'),
          'L': letter, 'L_observed': lv, 'E': E, 'E_dropped_chars': drop_E, 'X': X, 'X_dropped_chars': drop_X, 'X_fragments': xfrag, 'F': FSET,
          'overlaps': [[p, q, v] for p, q, v in overlaps], 'echo_count': len(echo)}

# ---------------- 転記行 C: 方向と活性の一致 ----------------
D = np.load(j('results', 'dirB', 'dirB__s1', 'directions.npz'))
Z = np.load(ACT)
act_sha = hashlib.sha256(open(ACT, 'rb').read()).hexdigest().upper()
DJ = json.load(open(j('results', 'dirB', 'dirB__s1', 'directions.json'), encoding='utf-8'))
assert act_sha == DJ['activations_npz_sha256'].upper(), '活性のファイルが凍結の記録と違う'
scenes_ex = DJ['extraction_scenarios']
h = lambda arm, r: np.mean([Z['same_order__%s__%s__%s' % (arm, sc, r)].astype(np.float64) for sc in scenes_ex], axis=0)
pairs = {'static': ('O', 'Osec'), 'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}
rows_c = []
for r in (str(x) for x in TL['layers']['ratios']):
    vs = h('O', r) - h('Osec', r)
    for name, (A_, B_) in pairs.items():
        u = h(A_, r) - h(B_, r)
        if name != 'static':
            u = u * (np.linalg.norm(vs) / np.linalg.norm(u))
        ref = D['%s__%s' % (name, r)].astype(np.float64)
        rows_c.append((name, r, float(np.max(np.abs(u - ref)) / np.linalg.norm(ref)), float(u @ ref / (np.linalg.norm(u) * np.linalg.norm(ref)))))
worst = max(x[2] for x in rows_c)
arms8 = DJ['arms']
F['C'] = {'text': '凍結の活性（`main_position_activations.npz`・%d バイト・SHA-256 %s・凍結の記録の値と一致）の `same_order` の区画から、四つの方向を三つの層で作り直し、凍結の `directions.npz` と比べた: 最大の |差| ／ ノルムの最大 %.2e・余弦の最小 %.9f（%d 組）。実在の差の方向の元になる腕は %d 本（%s）で、対は %d 組。'
          % (os.path.getsize(ACT), act_sha, worst, min(x[3] for x in rows_c), len(rows_c), len(arms8), '・'.join(arms8), len(arms8) * (len(arms8) - 1) // 2),
          'rows': rows_c, 'activations_sha256': act_sha, 'activations_bytes': os.path.getsize(ACT)}

# ---------------- 転記行 D: 校正の升目（方向の単位） ----------------
AN = json.load(open(j(*TL['calibration']['input'].split('/')), encoding='utf-8'))
BD = AN['by_direction']
noop_rows = {(r['scenario'], r['arm']): r for r in BD if r['arm'] in noop[r['scenario']]}
ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')              # 最後の枝は (6b) の腕
KIND = {'': 'static', 'rand': 'rand', 'Nk': 'Nk', 'td': 'td'}
kind = lambda arm: KIND.get(ARM_RE.match(arm).group(3) or '', 'loaded')
cnt, cnt_dir, excl = collections.Counter(), collections.Counter(), collections.Counter()
RC = {}
collapse = []
for r in BD:
    if r['arm'] in noop[r['scenario']]:
        continue
    m = ARM_RE.match(r['arm']); assert m, r['arm']
    base = noop_rows[(r['scenario'], m.group(1))]
    k = kind(r['arm'])
    key = (r['scenario'], r['arm'])
    if key not in RC:
        RC[key] = row_counts(*key)
    c = RC[key][r['direction_id']]
    assert c['_n'] == r['n_ok'], (key, r['direction_id'], c['_n'], r['n_ok'])
    if c['_n'] and max(c[x] for x in ('a', 'b', 'c', 'd', 'refuse')) == c['_n']:
        collapse.append('%s・%s・%s（%s %d/%d）' % (r['scenario'], r['arm'], r['direction_id'], [x for x in 'abcd' if c[x] == c['_n']][0], c['_n'], c['_n']))
    if 0 < base['cat'] < base['n_ok']:
        cnt[k] += 1
        cnt_dir[r['direction_id']] += 1
    else:
        excl['%s（土台 %s・%s）' % (k, m.group(1), r['scenario'])] += 1
gate_dirs = TL['calibration']['directions']
assert sorted(cnt_dir) == sorted(gate_dirs), (sorted(cnt_dir), gate_dirs)
TU = collections.defaultdict(set)
tune_dirs = set()
for d in glob.glob(j('results', 'tuneB', '*')):
    for f in glob.glob(os.path.join(d, 'trials-*.jsonl')):
        for l in open(f, encoding='utf-8'):
            t = json.loads(l)
            if t['status'] == 'ok':
                TU[(t['scenario'], t['layer'], t['coef'])].add(t['direction_id'])
                tune_dirs.add((t['layer'], t['direction_id']))
quads = sum(1 for v in TU.values() if len(v) == 4)
F['D'] = {'text': 'B の本走行の方向ごとの行（凍結した集計器の記録 `by_direction`）のうち、土台の無操作の腕の破局が零でも全部でもない行: %s（計 %d）。方向の単位（門の並べ替えの単位）ごとの行の数: %s（%d 本）。床か天井の土台で外す行: %s。'
                  '出力が一つの選択にそろった行（崩れの行）: %s。調整走行の層ごとの方向（層 × 方向）: %d 本。調整走行の組（場面 × 層 × 係数）で、v̂ と三本のランダム方向が揃う組: %d／%d。'
          % ('・'.join('%s %d' % kv for kv in sorted(cnt.items())), sum(cnt.values()), '・'.join('%s %d' % (d_, cnt_dir[d_]) for d_ in gate_dirs), len(gate_dirs),
             '・'.join('%s %d' % kv for kv in sorted(excl.items())) or '無し', '／'.join(collapse) or '無し', len(tune_dirs), quads, len(TU)),
          'eligible': dict(cnt), 'eligible_by_direction': dict(cnt_dir), 'excluded': dict(excl), 'collapse_rows': collapse, 'tune_directions': sorted('%s|%s' % x for x in tune_dirs), 'tune_quads': quads}

# ---------------- 転記行 E: 大きさの目盛り（層・選んだ試行・下限を超えた行） ----------------
MG = TL['magnitude']
per_cell, zmin, cc = MG['per_cell'], MG['lower_bound']['z_min'], MG['lower_bound']['continuity']
sel = collections.OrderedDict()
json_key = ('S4', 'Osec-Ncold', 'json')
sel['S4|Osec-Ncold|json'] = sorted(cands[json_key])[:per_cell]
for sc in SCENES:
    for base in ('Onull', 'O-Ncold'):
        sel['%s|%s|prose' % (sc, base)] = sorted(cands[(sc, base, 'prose')])[:per_cell]
n_cand = {'S4|Osec-Ncold|json': len(cands[json_key])}
n_cand.update({'%s|%s|prose' % (sc, base): len(cands[(sc, base, 'prose')]) for sc in SCENES for base in ('Onull', 'O-Ncold')})
for k, v in sel.items():
    assert len(v) == per_cell, ('候補が足りない', k, len(v))
    assert len(set(x[2] for x in v)) == 1, ('前置きの SHA が升目の中で揃わない', k)
sel_ids = {k: [x[1] for x in v] for k, v in sel.items()}
sel_sha = hashlib.sha256(json.dumps(sel_ids, sort_keys=True).encode('utf-8')).hexdigest().upper()[:16]


def z2(k0, n0, k1, n1):
    q0, q1 = (k0 + cc) / (n0 + 2 * cc), (k1 + cc) / (n1 + 2 * cc)
    se = math.sqrt(q0 * (1 - q0) / n0 + q1 * (1 - q1) / n1)
    return k1 / n1 - k0 / n0, (k1 / n1 - k0 / n0) / se


letter_rows, main_rows = [], []
for r in BD:
    if r['arm'] in noop[r['scenario']]:
        continue
    m = ARM_RE.match(r['arm'])
    base_arm = m.group(1)
    if (r['scenario'], base_arm) not in RC:
        RC[(r['scenario'], base_arm)] = row_counts(r['scenario'], base_arm)
    c0 = RC[(r['scenario'], base_arm)]['fixed']
    c1 = RC[(r['scenario'], r['arm'])][r['direction_id']]
    name = '%s|%s|%s' % (r['scenario'], r['arm'], r['direction_id'])
    dlt, z = z2(c0['_style'], c0['_n'], c1['_style'], c1['_n'])
    main_rows.append({'row': name, 'kind': kind(r['arm']), 'p0': c0['_style'] / c0['_n'], 'p1': c1['_style'] / c1['_n'], 'diff': dlt, 'z': z, 'pass': abs(z) >= zmin})
    if r['scenario'] == 'S4' and base_arm == 'Osec-Ncold':
        for x in ('a', 'c'):
            dlt, z = z2(c0[x], c0['_n'], c1[x], c1['_n'])
            letter_rows.append({'row': name, 'letter': x, 'p0': c0[x] / c0['_n'], 'p1': c1[x] / c1['_n'], 'diff': dlt, 'z': z, 'pass': abs(z) >= zmin})
vhat_pass = [x['row'] for x in main_rows if x['kind'] == 'static' and x['pass']]
assert not vhat_pass, ('v̂ の行に様式の変化が下限を超える行がある——「v̂ の行では比が出ない」は成り立たない', vhat_pass)
pt = lambda v: '%+.1f' % (100 * v)
F['E'] = {'text': ('層二の大きさの目盛り（裁定 D170）。候補（B の本走行の無操作の腕の出力のうち、JSON の選択を読めて、選択の値の文字を覆うトークンが見つかった出力の数）: JSON 直答の層 %s／散文の層 %s。'
                   '各層で試行の番号の小さい順に %d 件ずつ選んだ（選んだ試行の番号の一覧の SHA16 %s・一覧は記録の JSON・各層の前置きの SHA は一つにそろう）。'
                   '答えの文字の位置の比（S4 の Osec-Ncold の行・文字 a と c）で下限（二標本の z の絶対値 %s 以上）を超えるもの: %s。超えないもの: %s。'
                   '主位置の比（様式の変化・全ての行 %d）で下限を超えるもの: %s。v̂ の行で様式の変化が下限を超えるもの: 無し（v̂ の行では比が出ない）。')
          % ('%d' % n_cand['S4|Osec-Ncold|json'], '・'.join('%s %d' % (k.rsplit('|', 1)[0], n_cand[k]) for k in sel if k.endswith('prose')), per_cell, sel_sha, '%g' % zmin,
             '・'.join('%s の %s（%s pt・z %.2f）' % (x['row'], x['letter'], pt(x['diff']), x['z']) for x in letter_rows if x['pass']) or '無し',
             '・'.join('%s の %s（%s pt・z %.2f）' % (x['row'], x['letter'], pt(x['diff']), x['z']) for x in letter_rows if not x['pass']) or '無し',
             len(main_rows), '・'.join('%s（%s pt・z %.2f）' % (x['row'], pt(x['diff']), x['z']) for x in main_rows if x['pass']) or '無し'),
          'candidates': n_cand, 'selected': sel_ids, 'selected_sha16': sel_sha, 'selected_preamble_sha': {k: v[0][2] for k, v in sel.items()},
          'letter_rows': letter_rows, 'main_rows': main_rows}

# ---------------- 転記行 F: 重みとトークナイザ ----------------
sh = {}
if not a.skip_weights_hash:
    for p in sorted(glob.glob(os.path.join(a.tokenizer, '*.safetensors'))) + [os.path.join(a.tokenizer, n) for n in ('config.json', 'tokenizer.json', 'model.safetensors.index.json')]:
        hh = hashlib.sha256()
        with open(p, 'rb') as fh:
            for b in iter(lambda: fh.read(1 << 24), b''):
                hh.update(b)
        sh[os.path.basename(p)] = hh.hexdigest().upper()
cfg = json.load(open(os.path.join(a.tokenizer, 'config.json'), encoding='utf-8'))
F['F'] = {'text': '手元の重み（版 `%s`・HF のキャッシュ）の断片と設定の SHA-256: %s。設定: 層 %d・隠れの次元 %d・語彙の行 %d・埋め込みの共有 %s。Colab の起動器は、同じ版を取り込んだ断片の SHA-256 を印字し、この値と突き合わせる（HF のキャッシュが実体の写しで、断片の名から内容の SHA を読めないため）。'
          % (os.path.basename(a.tokenizer), '・'.join('`%s` %s' % (k, v) for k, v in sh.items()) or '（計算を飛ばした）', cfg['num_hidden_layers'], cfg['hidden_size'], cfg['vocab_size'], cfg['tie_word_embeddings']),
          'sha256': sh}

# ---------------- 転記行 G: 語彙 ----------------
F['G'] = {'text': '語彙の行 %d のうち、含めるのは添字 %d 未満の %d 行。除くのは追加の特別なトークン %d 個（添字 %d〜%d）と、トークナイザに無い詰めの行 %d 行。'
          % (cfg['vocab_size'], base_vocab, base_vocab, len(tok) - base_vocab, base_vocab, len(tok) - 1, cfg['vocab_size'] - len(tok)), 'base_vocab': base_vocab}

# ---------------- 転記行 H: 語の側の帰無の候補（語彙の行のノルムだけを使う・方向とは掛けない） ----------------
from safetensors import safe_open
IDX = json.load(open(os.path.join(a.tokenizer, 'model.safetensors.index.json'), encoding='utf-8'))


def read_rows(name, s0, s1):
    with safe_open(os.path.join(a.tokenizer, IDX['weight_map'][name]), framework='pt') as fh:
        return fh.get_slice(name)[s0:s1].float().numpy()


with safe_open(os.path.join(a.tokenizer, IDX['weight_map']['model.norm.weight']), framework='pt') as fh:
    g = fh.get_tensor('model.norm.weight').float().numpy()
nrm = np.zeros(base_vocab)
STEP = 1 << 13
for s0 in range(0, base_vocab, STEP):
    s1 = min(base_vocab, s0 + STEP)
    nrm[s0:s1] = np.linalg.norm(read_rows('model.embed_tokens.weight', s0, s1) * g[None, :], axis=1)
WS = TL['nulls']['word_side']
CT = WS['char_types']


def ctype(i):
    s = dec(i)
    if s and all(KANJI[0] <= ord(ch) <= KANJI[1] for ch in s):
        return CT[0]
    if s and all(KATA[0] <= ord(ch) <= KATA[1] or ord(ch) == CHOON for ch in s):
        return CT[1]
    return CT[2]


excl_ids = tO | tS | ctx_ids
pool = [i for i in range(base_vocab) if i not in excl_ids and not is_frag(i) and is_main(i)]
nb = WS['norm_bands']
edges = np.quantile(nrm[pool], [k / nb for k in range(1, nb)])
band = lambda i: int(np.searchsorted(edges, nrm[i], side='right'))
strat = lambda L: collections.Counter((ctype(i), band(i)) for i in L)
P_ = strat(pool)
need_p, need_m = strat(E['static']['plus']), strat(E['static']['minus'])
need = need_p + need_m
ratio_min = min(P_[k] / v for k, v in need.items())
fmt_st = lambda C: '・'.join('%s 帯%d %d' % (t_, b_ + 1, C[(t_, b_)]) for t_ in CT for b_ in range(nb) if C[(t_, b_)])
F['H'] = {'text': ('語の側の帰無の候補（裁定 D171・M_E の二つ目の札）: 含める語彙のうち規則を通るトークン %d（O と Osec の本文・場面の本文・JSON の指示に現れるトークンと、断片と、中身の語でないものと、片仮名一字を除く）。'
                   'ノルムは語彙の行に最終の正規化の重みを掛けたベクトルのノルムで、候補を %d 帯に分けた（帯の境 %s）。字の種類 × 帯の候補の数: %s。'
                   'v̂ の E+（%d）の組み立て: %s／E−（%d）の組み立て: %s。要る数に対する候補の数の比の最小 %.1f。語彙の行列は行のノルムだけを使い、方向とは掛けていない。')
          % (len(pool), nb, '・'.join('%.4f' % x for x in edges), fmt_st(P_), len(E['static']['plus']), fmt_st(need_p), len(E['static']['minus']), fmt_st(need_m), ratio_min),
          'pool': len(pool), 'edges': [float(x) for x in edges], 'strata_pool': {'%s|%d' % k: v for k, v in sorted(P_.items())},
          'strata_plus': {'%s|%d' % k: v for k, v in sorted(need_p.items())}, 'strata_minus': {'%s|%d' % k: v for k, v in sorted(need_m.items())}, 'ratio_min': ratio_min}

T = {'kind': 'blens_design_facts', 'version': VERSION, 'contrasts_sha16': s16f(j('design', 'contrasts-Blens.json')), 'generated_utc': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
     'note': '射影は一つも計算していない（語彙の行列と方向を掛け合わせていない・転記行 H は語彙の行のノルムだけを使う）。語の集合は下書きで、凍結は器 `tools/blens_sets.py` が同じ規則で行い、バイトで一致することを確かめる。',
     'facts': F, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(j('records', 'Blens'), exist_ok=True)
jp = j('records', 'Blens', 'design-facts-Blens.json')
json.dump(T, open(jp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = ['# B-lens の設計の事実（転記行・機械生成・`tools/blens_facts.py` %s・%s UTC）' % (VERSION, T['generated_utc']), '', '- 正本 `design/contrasts-Blens.json` SHA16 %s。' % T['contrasts_sha16'], '- ' + T['note'], '']
md += ['- **転記行 %s** — %s' % (k, F[k]['text']) for k in sorted(F)]
md += ['', T['clause'], '']
open(j('records', 'Blens', 'design-facts-Blens.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(md))
print('wrote', jp, s16f(jp))
for k in sorted(F):
    print(k, F[k]['text'][:400])
