# -*- coding: utf-8 -*-
"""blens_facts.py v1 —— B-lens の枠に置く設計の事実（転記行 A〜G）を、記録と凍結物から機械で作る。**射影は一つも計算しない**（語彙の行列と方向を掛け合わせない）。
出力: records/Blens/design-facts-Blens.json（転記行の逐語と、機械で読む語の集合の下書き）・records/Blens/design-facts-Blens.md
語の集合はここでは下書きで、凍結は器 `tools/blens_sets.py`（設計の検分の後に書く）が、同じ規則で作り直して行う。
用法: python tools/blens_facts.py [--tokenizer 置き場]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, hashlib, difflib, argparse, datetime, collections
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
VERSION = 'v1'
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
SC = json.load(open(j('arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
SCN = {s['question_id']: s for s in SC['scenarios']}
SCENES = ['N1', 'S1', 'SK', 'S4']
F = {}

# ---------------- 転記行 A: O と Osec の差 ----------------
O, S = TXT['O'], TXT['Osec']
sm = difflib.SequenceMatcher(None, O, S, autojunk=False)
_raw = sm.get_opcodes()
MERGE = TL['token_sets']['diff_merge']
ops, cur = [], None
for t, i1, i2, j1, j2 in _raw:                          # 短い一致（MERGE 字未満）をはさむ違いは一つの組にまとめる（語の単位で読むため）
    if t == 'equal':
        if cur and i2 - i1 < MERGE and i2 < len(O):
            cur = [cur[0], i2, cur[2], j2]
            continue
        if cur:
            ops.append(cur); cur = None
        continue
    cur = [cur[0], i2, cur[2], j2] if cur else [i1, i2, j1, j2]
if cur:
    ops.append(cur)
ops = [('replace', O[i1:i2], S[j1:j2]) for i1, i2, j1, j2 in ops]
same = sum(i2 - i1 for t, i1, i2, j1, j2 in sm.get_opcodes() if t == 'equal')
shared = [w for w in ('共創', '再帰的自己改善', '私と共に在り続ける者よ', 'かくの如く来たり', '慈悲を核として', '思いやりを核として') if w in O and w in S]
absent = [w for w in ('相互依存',) if w not in O and w not in S]
F['A'] = {'text': 'O（%d 字・`%s`）と Osec（%d 字・`%s`）を文字で突き合わせた（`difflib`・器 `tools/blens_facts.py`）。共通の文字 %d。違う所（O → Osec）: %s。両方にある句: %s。どちらにも無い語: %s。'
          % (len(O), FILES['O']['path'], len(S), FILES['Osec']['path'], same, '／'.join('「%s」→「%s」' % (x, y) for t, x, y in ops), '・'.join('「%s」' % w for w in shared), '・'.join('「%s」' % w for w in absent)),
          'ops': ops, 'same': same, 'len_O': len(O), 'len_Osec': len(S)}

# ---------------- トークナイザ ----------------
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(a.tokenizer)
ids = lambda s: tok(s, add_special_tokens=False)['input_ids']
dec = lambda i: tok.decode([i])
base_vocab = min(tok.added_tokens_decoder.keys())
assert base_vocab == TL['inputs']['model']['base_vocab'] and len(tok) == TL['inputs']['model']['tokenizer_len'], (base_vocab, len(tok))

# ---------------- 語の集合（下書き） ----------------
instr = SC['json_instruction']
ctx_ids = set()
for sc in SCENES:
    ctx_ids |= set(ids(SCN[sc]['text'])) | set(ids(instr[SCN[sc]['family']]))
tO, tS, tN, tK = set(ids(O)), set(ids(S)), set(ids(TXT['Onull'])), set(ids(TXT['Nk']))
E = {'static': {'plus': sorted((tO - tS) - ctx_ids), 'minus': sorted((tS - tO) - ctx_ids)},
     'td': {'plus': sorted(tN - ctx_ids), 'minus': []}, 'Nk': {'plus': sorted(tK - ctx_ids), 'minus': []}}
FRAG = lambda L: [i for i in L if chr(0xFFFD) in dec(i)]
nofrag = lambda L: [i for i in L if chr(0xFFFD) not in dec(i)]
frag_removed = collections.Counter()
for k in E:
    for side in ('plus', 'minus'):
        frag_removed['E'] += len(FRAG(E[k][side])); E[k][side] = nofrag(E[k][side])
CJK = re.compile('[' + chr(0x4E00) + '-' + chr(0x9FFF) + chr(0x30A1) + '-' + chr(0x30FA) + ']')   # 漢字と片仮名の字（中黒・長音符・繰り返し記号は含めない）
content = lambda L: [i for i in L if CJK.search(dec(i))]
for k in E:
    for side in ('plus', 'minus'):
        E[k][side + '_all'] = E[k][side]; E[k][side] = content(E[k][side])
E['loaded'] = E['static']                              # (6b) の二腕は Ncold の一行を共有するので、違う語は O と Osec の差と同じ


def options(text):
    ms = list(re.finditer(r'\(([a-d])\)', text))
    out = {}
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else text.index('。', m.end())
        out[m.group(1)] = text[m.end():end].strip().rstrip('、').strip()
    return out


X = {}
for sc in SCENES:
    op = options(SCN[sc]['text'])
    a_ids = set(ids(op['a']))
    o_ids = set().union(*[set(ids(v)) for k, v in op.items() if k != 'a'])
    frag_removed['X'] += len(FRAG(sorted(a_ids ^ o_ids)))
    _xa, _xo = nofrag(sorted(a_ids - o_ids)), nofrag(sorted(o_ids - a_ids))
    X[sc] = {'options': op, 'a': content(_xa), 'others': content(_xo), 'a_all': _xa, 'others_all': _xo}

# 答えの文字と拒否（JSON の形の中で）
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


CH = re.compile(r'"choice"\s*:\s*"(a|b|c|d|refuse)"')
first_json, first_prose = collections.Counter(), collections.Counter()
letter_cov = collections.defaultdict(collections.Counter)
tf_ok = {}
noop = TL['token_sets']['noop_arms']
for sc in SCENES:
    for arm in noop[sc]:
        good = 0
        for t, r in trials_raw(sc, arm):
            if t['status'] != 'ok':
                continue
            txt = r['final']
            enc = tok(txt, add_special_tokens=False, return_offsets_mapping=True)
            if enc['input_ids']:
                (first_json if t['style_b'] else first_prose)[enc['input_ids'][0]] += 1
            ms = list(CH.finditer(txt))
            if ms and ms[-1].group(1) == t['choice']:
                pos = ms[-1].start(1)
                cover = [i for i, (s0, s1) in zip(enc['input_ids'], enc['offset_mapping']) if s0 <= pos < s1]
                if cover:
                    letter_cov[t['choice']][cover[0]] += 1
                    good += 1
        tf_ok['%s|%s' % (sc, arm)] = good
K_F = TL['token_sets']['F_top']
fj = [i for i, _ in first_json.most_common(K_F)]
fp = [i for i, _ in first_prose.most_common(K_F)]
frag_removed['F'] += len(FRAG(fj)) + len(FRAG(fp))
fj, fp = nofrag(fj), nofrag(fp)
both = set(fj) & set(fp)
FSET = {'json': [i for i in fj if i not in both], 'prose': [i for i in fp if i not in both], 'removed_both': sorted(both),
        'n_json_first': sum(first_json.values()), 'n_prose_first': sum(first_prose.values())}
lv = {x: {'canonical': letter[x], 'observed': dict(letter_cov[x].most_common())} for x in ('a', 'b', 'c', 'd', 'refuse')}

show = lambda L: '・'.join('%d「%s」' % (i, dec(i).replace('\n', '⏎')) for i in L)
XG = []
for sc in SCENES:
    for g in XG:
        if X[g[0]]['a'] == X[sc]['a'] and X[g[0]]['others'] == X[sc]['others']:
            g.append(sc); break
    else:
        XG.append([sc])
F['B'] = {'text': ('答えの文字（L）: %s。B の無操作の出力で、選択の値の最初の文字を覆うトークン: %s。拒否（R）: %d「%s」（値は二つのトークンに割れる）。'
                   '語の反響（E・中身の語）: v̂ と (6b) の E+（O にだけある語）%d 個＝%s／E−（Osec にだけある語）%d 個＝%s／td の E+（Onull にだけある語）%d 個／Nk の E+ %d 個＝%s（全てのトークンでは E+ %d・E− %d・td %d・Nk %d 個）。'
                   '選択肢の語（X・中身の語）: %s。様式（F・無操作の腕の出力の最初のトークン・上位 %d）: JSON 直答 %d 件から F_json＝%s／散文 %d 件から F_prose＝%s（両方の上位にあって除いたもの: %s）。'
                   '場面の本文と JSON の指示にある語は E から除いた。文字にならないトークン（バイトの断片）を除いた数: %s。語の数はトークンの数。td の E+ の一覧は記録の JSON にある。')
          % ('・'.join('%s＝%d' % (x, letter[x]) for x in ('a', 'b', 'c', 'd')),
             '／'.join('%s: %s' % (x, '・'.join('%d×%d' % (i, n) for i, n in letter_cov[x].most_common())) for x in ('a', 'b', 'c', 'd', 'refuse') if letter_cov[x]),
             letter['refuse'], dec(letter['refuse']),
             len(E['static']['plus']), show(E['static']['plus']), len(E['static']['minus']), show(E['static']['minus']), len(E['td']['plus']), len(E['Nk']['plus']), show(E['Nk']['plus']),
             len(E['static']['plus_all']), len(E['static']['minus_all']), len(E['td']['plus_all']), len(E['Nk']['plus_all']),
             '／'.join('%s（(a)「%s」）X_a %d 個＝%s・X_o %d 個＝%s（全てのトークンでは %d・%d 個）' % ('・'.join(g), X[g[0]]['options']['a'], len(X[g[0]]['a']), show(X[g[0]]['a']), len(X[g[0]]['others']), show(X[g[0]]['others']), len(X[g[0]]['a_all']), len(X[g[0]]['others_all'])) for g in XG),
             K_F, FSET['n_json_first'], show(FSET['json']), FSET['n_prose_first'], show(FSET['prose']), show(FSET['removed_both']) or '無し', '・'.join('%s %d' % kv for kv in sorted(frag_removed.items()))),
          'L': letter, 'L_observed': lv, 'E': E, 'fragments_removed': dict(frag_removed), 'X': X, 'F': FSET}

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
F['C'] = {'text': '凍結の活性（`main_position_activations.npz`・SHA-256 %s・凍結の記録の値と一致）の `same_order` の区画から、四つの方向を三つの層で作り直し、凍結の `directions.npz` と比べた: 最大の |差| ／ ノルムの最大 %.2e・余弦の最小 %.9f（%d 組）。実在の差の方向の元になる腕は %d 本（%s）で、対は %d 組。'
          % (act_sha, worst, min(x[3] for x in rows_c), len(rows_c), len(arms8), '・'.join(arms8), len(arms8) * (len(arms8) - 1) // 2),
          'rows': rows_c, 'activations_sha256': act_sha}

# ---------------- 転記行 D: 校正の升目 ----------------
AN = json.load(open(j('records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
BD = AN['by_direction']
noop_rows = {(r['scenario'], r['arm']): r for r in BD if r['arm'] in noop[r['scenario']]}
ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')              # 最後の枝は (6b) の腕
KIND = {'': 'static', 'rand': 'rand', 'Nk': 'Nk', 'td': 'td'}
kind = lambda arm, did: KIND.get(ARM_RE.match(arm).group(3) or '', 'loaded')
cnt, excl = collections.Counter(), collections.Counter()
for r in BD:
    if r['arm'] in noop[r['scenario']]:
        continue
    m = ARM_RE.match(r['arm']); assert m, r['arm']
    base = noop_rows[(r['scenario'], m.group(1))]
    k = kind(r['arm'], r['direction_id'])
    if 0 < base['cat'] < base['n_ok']:
        cnt[k] += 1
    else:
        excl['%s（土台 %s・%s）' % (k, m.group(1), r['scenario'])] += 1
TU = collections.defaultdict(set)
for d in glob.glob(j('results', 'tuneB', '*')):
    for f in glob.glob(os.path.join(d, 'trials-*.jsonl')):
        for l in open(f, encoding='utf-8'):
            t = json.loads(l)
            if t['status'] == 'ok':
                TU[(t['scenario'], t['layer'], t['coef'])].add(t['direction_id'])
quads = sum(1 for v in TU.values() if len(v) == 4)
F['D'] = {'text': 'B の本走行の方向ごとの行（凍結した集計器の記録 `by_direction`）のうち、土台の無操作の腕の破局が零でも全部でもない行: %s（計 %d）。床か天井の土台で外す行: %s。調整走行の組（場面 × 層 × 係数）で、v̂ と三本のランダム方向が揃う組: %d／%d。'
          % ('・'.join('%s %d' % kv for kv in sorted(cnt.items())), sum(cnt.values()), '・'.join('%s %d' % kv for kv in sorted(excl.items())) or '無し', quads, len(TU)),
          'eligible': dict(cnt), 'excluded': dict(excl), 'tune_quads': quads}

# ---------------- 転記行 E: 教師強制の候補 ----------------
cells = []
for sc in SCENES:
    for base in ('Onull', 'O-Ncold') + (('Osec-Ncold',) if sc == 'S4' else ()):
        cells.append('%s・%s %d' % (sc, base, tf_ok['%s|%s' % (sc, base)]))
need = TL['magnitude']['per_cell']
F['E'] = {'text': '層二の大きさの目盛りの候補（B の本走行の無操作の腕の出力のうち、JSON の選択を読めて、選択の値の文字を覆うトークンが見つかった出力の数）: %s。各升目に要る数は %d。'
          % ('／'.join(cells), need), 'counts': tf_ok, 'enough': all(tf_ok['%s|%s' % (c.split('・')[0], c.split('・')[1].rsplit(' ', 1)[0])] >= need for c in cells)}

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

T = {'kind': 'blens_design_facts', 'version': VERSION, 'contrasts_sha16': s16f(j('design', 'contrasts-Blens.json')), 'generated_utc': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
     'note': '射影は一つも計算していない（語彙の行列と方向を掛け合わせていない）。語の集合は下書きで、凍結は設計の検分の後に器 `tools/blens_sets.py` が同じ規則で行う。',
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
    print(k, F[k]['text'][:300])
