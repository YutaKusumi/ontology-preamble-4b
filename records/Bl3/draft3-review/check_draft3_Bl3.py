# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の草案3 の起草者の見直しの器の検査（M1〜M10・見直しの枠 `frame-draft3-review-Bl3.md` の手順 A）。
入力はコミット 3a0da45（草案3）の木から読む（git show）。直しの案を置き場に作った後に走らせ直しても、同じ出力になる。
効き目は一つも計算しない（順伝播をしない）。読みは付けない（読みは通読で付ける）。
出力: records/Bl3/draft3-review/check-draft3-Bl3.md・check-draft3-Bl3.json
用法: python records/Bl3/draft3-review/check_draft3_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, math, hashlib, subprocess, tempfile, shutil, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import numbers_lint as NLT                                   # 凍結の数の検査の器（読み取りだけで呼ぶ）
NL = chr(10)
REF = '3a0da45'


def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, check=True).stdout


TREE = set(git('ls-tree', '-r', '--name-only', REF).decode('utf-8').split(NL)) - {''}
blob_b = lambda p: git('show', '%s:%s' % (REF, p)).replace(b'\r\n', b'\n')
blob = lambda p: blob_b(p).decode('utf-8')
h16 = lambda b: hashlib.sha256(b).hexdigest().upper()[:16]


def s16_any(p):
    """木にあれば木の値、無ければ手元の値（追跡の外）。"""
    if p in TREE:
        return h16(blob_b(p)), '木'
    fp = os.path.join(REPO, *p.split('/'))
    if os.path.isfile(fp):
        return h16(open(fp, 'rb').read().replace(b'\r\n', b'\n')), '手元（追跡の外）'
    return None, '無い'


D3P, SRCP, CP, FP, FMP = 'design/design-Bl3-draft3.md', 'design/design-Bl3-draft3.src.md', 'design/contrasts-Bl3.json', 'records/Bl3/design-facts-Bl3.json', 'records/Bl3/design-facts-Bl3.md'
D3 = blob(D3P)
L3 = D3.splitlines()                                          # 最後の改行の後を行に数えない
T3 = json.loads(blob(CP))
TB = json.loads(blob('design/contrasts-B.json'))
TL = json.loads(blob('design/contrasts-Blens.json'))
FJ = json.loads(blob(FP))
F = FJ['facts']
OUT = collections.OrderedDict()
OUT['meta'] = {'ref': REF, 'draft_lines': len(L3), 'draft_sha16': h16(blob_b(D3P)), 'canon_sha16': h16(blob_b(CP)), 'facts_sha16': h16(blob_b(FP))}


def strings(o, path='$', skip=()):
    if isinstance(o, dict):
        for k, v in o.items():
            if path == '$' and k in skip:
                continue
            yield from strings(v, path + '.' + k, skip)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, '%s[%d]' % (path, i), skip)
    elif isinstance(o, str):
        yield path, o


CANON_TEXT = list(strings(T3))

# ---------------- M1: SHA16 ----------------
m1 = []
for k, v in T3['inputs']['files'].items():
    now, where = s16_any(v['path'])
    m1.append(('正本 `inputs.files.%s`' % k, v['path'], v['sha16'], now, where, now == v['sha16']))
for m in re.finditer(r'`((?:records|design|tools)/[\w\-./]+)`\s*[〔（]SHA16 ([0-9A-F]{16})', D3):
    now, where = s16_any(m.group(1))
    m1.append(('草案3 の印字', m.group(1), m.group(2), now, where, now == m.group(2)))
for m in re.finditer(r'原稿 `([\w\-./]+)` SHA16 ([0-9A-F]{16})', D3):
    now, where = s16_any(m.group(1))
    m1.append(('草案3 の §6-補', m.group(1), m.group(2), now, where, now == m.group(2)))
m1.append(('設計事実の `contrasts_sha16`', CP, FJ['contrasts_sha16'], h16(blob_b(CP)), '木', FJ['contrasts_sha16'] == h16(blob_b(CP))))
OUT['M1'] = [dict(zip(('where', 'path', 'printed', 'now', 'source', 'ok'), x)) for x in m1]

# ---------------- M2: パス ----------------
PATH_RE = re.compile(r'(?:records|design|tools|results|arms|prompts)/[\w\-./]*')
m2 = collections.OrderedDict()
for src, text in [('草案3', D3)] + [('正本 ' + p, t) for p, t in CANON_TEXT]:
    for m in PATH_RE.finditer(text):
        p = m.group(0).rstrip('.')
        if p in m2:
            continue
        if p.endswith('/'):
            st = '在る（置き場）' if any(x.startswith(p) for x in TREE) else '無い'
        elif p in TREE:
            st = '在る（木）'
        elif os.path.exists(os.path.join(REPO, *p.split('/'))):
            st = '在る（手元・追跡の外）'
        else:
            st = '無い'
        m2[p] = (src.split(' ')[0], st)
OUT['M2'] = [{'path': p, 'first_seen': a, 'status': b} for p, (a, b) in m2.items()]

# ---------------- M3: 番号 ----------------
AT1 = blob('records/reviews/Bl3/design-round1/adoption-table-Bl3-design-r1.md')
AT2 = blob('records/reviews/Bl3/design-round2/adoption-table-Bl3-design-r2.md')
V1 = blob('records/reviews/Bl3/design-round1/verification-Bl3-design-r1.md')
V2 = blob('records/reviews/Bl3/design-round2/verification-Bl3-design-r2.md')
P_ROWS = set(re.findall(r'^\| (P\d{3}) \|', AT1 + NL + AT2, flags=re.M))
K_ROWS = set(re.findall(r'^\| (K\d{3}) \|', V1 + NL + V2, flags=re.M))
m3 = collections.OrderedDict()
for src, text in [('草案3', D3)] + [('正本', t) for _, t in CANON_TEXT]:
    for kind, rx, ok in (('D', r'(?<![A-Za-z\d\-])D(\d{2,3})(?!\d)', lambda c: c in T3['decisions']),
                         ('P', r'(?<![A-Za-z\d])P(\d{3})(?!\d)', lambda c: c in P_ROWS), ('K', r'(?<![A-Za-z\d])K(\d{3})(?!\d)', lambda c: c in K_ROWS)):
        for m in re.finditer(rx, text):
            c = kind + m.group(1)
            if c not in m3:
                m3[c] = (src, ok(c))
OUT['M3'] = [{'id': c, 'first_seen': a, 'ok': b} for c, (a, b) in sorted(m3.items(), key=lambda kv: (kv[0][0], int(kv[0][1:])))]

# ---------------- M4: 鍵の名 ----------------


def resolve(root, dotted):
    x = root
    for k in dotted.split('.'):
        if isinstance(x, dict) and k in x:
            x = x[k]
        else:
            return False
    return True


def keynames(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            acc.add(k)
            keynames(v, acc)
    elif isinstance(o, list):
        for v in o:
            keynames(v, acc)
    return acc


K3 = keynames(T3, set())
CODE = {n: blob('tools/%s.py' % n) for n in ('steer_B', 'rules_B', 'blens_core', 'run_stageB_local')}
m4 = collections.OrderedDict()
for src, text in [('草案3', D3)] + [('正本', t) for _, t in CANON_TEXT]:
    for m in re.finditer(r'`([^`]+)`', text):
        tkn = m.group(1)
        if tkn in m4 or '/' in tkn:
            continue
        if re.fullmatch(r'[A-Za-z_]\w*(?:\.\w+)+', tkn):
            head = tkn.split('.')[0]
            if resolve(T3, tkn):
                st = '層三の正本'
            elif head in CODE and re.search(r'def %s\b' % re.escape(tkn.split('.', 1)[1]), CODE[head]):
                st = '器 tools/%s.py の関数' % head
            elif resolve(TB, tkn):
                st = '段階 B の正本'
            elif resolve(TL, tkn):
                st = 'B-lens の正本'
            elif tkn.startswith('model.'):
                st = '模型の重みの名'
            else:
                st = '**解けない**'
        elif re.fullmatch(r'[A-Za-z_]\w*', tkn):
            if tkn in K3:
                st = '層三の正本の鍵の名'
            elif any(re.search(r'\b%s\b' % re.escape(tkn), c) for c in CODE.values()):
                st = '器の中の名'
            elif tkn in keynames(TB, set()) or tkn in keynames(TL, set()):
                st = '段階 B か B-lens の正本の鍵の名'
            else:
                st = 'その他（型・語）'
        else:
            st = '式・字句'
        m4[tkn] = (src, st)
OUT['M4'] = [{'token': t, 'first_seen': a, 'status': b} for t, (a, b) in m4.items()]

# ---------------- M5: 節の参照 ----------------
heads = {}
for i, l in enumerate(L3, 1):
    m = re.match(r'^(#{2,3}) (\d+(?:\.\d+)?)\.?\s*(.*)$', l)
    if m:
        heads[m.group(2)] = (i, m.group(3)[:40])
m5 = []
for i, l in enumerate(L3, 1):
    for m in re.finditer(r'§(\d+(?:\.\d+)?)', l):
        before = l[max(0, m.start() - 14):m.start()]
        other = any(w in before for w in ('最終版の', '草案2 の', '草案1 の', 'B-lens の', '段階 B の'))
        m5.append({'line': i, 'ref': m.group(1), 'other_doc': other, 'exists': m.group(1) in heads, 'heading': heads.get(m.group(1), (None, ''))[1], 'context': l[max(0, m.start() - 30):m.end() + 10]})
OUT['M5'] = m5

# ---------------- M6: 数の検査と禁止語の走査（凍結の数の検査の器を呼ぶ） ----------------
d = tempfile.mkdtemp(prefix='chkBl3_')
try:
    paths = {}
    for p in (CP, D3P, 'tools/make_contrasts_Bl3.py', 'tools/bl3_facts.py', 'tools/build_draft_Bl3.py'):
        q = os.path.join(d, os.path.basename(p))
        open(q, 'wb').write(blob_b(p))
        paths[p] = q
    C_ = NLT.const_set(T3)
    doc_bad = NLT.check_doc(T3, D3, C_)
    json_bad = NLT.check_json(T3, C_)
    gen_bad = {p: NLT.check_gen(paths[p]) for p in ('tools/make_contrasts_Bl3.py', 'tools/bl3_facts.py', 'tools/build_draft_Bl3.py')}
finally:
    shutil.rmtree(d, ignore_errors=True)
BAN = sorted({w for v in T3['print_strings'].values() for w in v})
ban_hits, in9 = [], False
for i, l in enumerate(L3, 1):
    if l.startswith('## '):
        in9 = l.startswith('## 9.')
    if in9 and l.startswith('| '):
        continue
    ban_hits += [(i, w) for w in BAN if w in l]
lint_rec = blob('records/Bl3/numbers-lint-draft3-Bl3.md')
OUT['M6'] = {'doc_unregistered': len(doc_bad), 'canon_unregistered': len(json_bad), 'generator_literals': {k: len(v) for k, v in gen_bad.items()}, 'ban_hits': ban_hits,
             'lint_record_total_zero': '- 違反の合計: 0' in lint_rec}

# ---------------- M7: 派生の数 ----------------
rows = T3['main_rows']
n_v = sum(1 for r in rows if r['direction'] == 'static')
n_nk = sum(1 for r in rows if r['direction'] == 'Nk')
K = T3['nulls']['isotropic']['count']
cv, cnk = T3['nulls']['real']['comparators']['static'], T3['nulls']['real']['comparators']['Nk']
arms8 = T3['nulls']['real']['arms']
pairs = len(arms8) * (len(arms8) - 1) // 2
alpha = T3['labels']['iso_outside']['holm_alpha']
m_rows = len(rows)
limits = []
for step in range(1, m_rows + 1):
    thr = alpha / (m_rows - step + 1)
    limits.append(max(e for e in range(0, K) if 2 * (1 + e) / (1 + K) < thr))
units_gate = sorted({r['unit'] for r in F['C']['gate_rows']})
units_wo = [u for u in units_gate if u != 'static']
units_wo_vl = [u for u in units_wo if u != 'loaded']
cells_B = F['B']['cells']
n_dirs = len(T3['directions']['named']) + T3['nulls']['B_random']['count'] + K + pairs
per_row = 2 + K + 2 * cv
tok_rc = sum(len(T3['independent_recompute']['new_paths']) * per_row * (cells_B['%s|%s' % (r['scenario'], r['base'])]['prompt_len'] + len(F['A']['prefix_ids'])) for r in rows if r['direction'] == 'static')
bt = T3['readout']['primary']['batch']
style_n = sum(1 for v in F['C']['style_share_pt'].values() if abs(v) >= T3['gate']['style_hold_pt'])
m7 = [
    ('比べる相手の対の数（v̂・Nk）', [pairs - len(T3['nulls']['real']['swap_siblings']), pairs - 1], [cv, cnk]),
    ('向きまで数えた比べる相手の数（v̂・Nk）', [2 * cv, 2 * cnk], [T3['nulls']['real']['comparators_oriented']['static'], T3['nulls']['real']['comparators_oriented']['Nk']]),
    ('偶然の目安（向きまで・対の単位）', [round(n_v / (2 * cv + 1) + n_nk / (2 * cnk + 1), 4), round(n_v / (cv + 1) + n_nk / (cnk + 1), 4)], [T3['nulls']['real']['chance_second'], T3['nulls']['real']['chance_second_pair']]),
    ('最小の p・Holm の第一段・第一段の外側の本数', [round(2 / (1 + K), 6), round(alpha / m_rows, 6), limits[0]], [T3['labels']['p_min'], T3['labels']['holm_first_step'], T3['labels']['first_step_margin']]),
    ('Holm の各段の外側の本数の上限（二巡目の確かめ K456 と比べる）', limits, json.loads(blob('records/reviews/Bl3/design-round2/verify-Bl3-design-r2.json')).get('holm_limits')),
    ('入れ替えの数（本の門・v̂ を抜く・v̂ と (6b) を抜く）', [math.factorial(len(units_gate)), math.factorial(len(units_wo)), math.factorial(len(units_wo_vl))],
     [T3['gate']['permutations'], T3['gate']['permutations_without_vhat'], T3['gate']['permutations_without_vhat_loaded']]),
    ('門の行の数（本・v̂ を抜く・v̂ と (6b) を抜く）', [len(F['C']['gate_rows']), sum(1 for r in F['C']['gate_rows'] if r['unit'] != 'static'), sum(1 for r in F['C']['gate_rows'] if r['unit'] not in ('static', 'loaded'))],
     [T3['gate']['rows_gate'], T3['gate']['rows_without_vhat'], T3['gate']['rows_without_vhat_loaded']]),
    ('様式の転位で除く行の数', style_n, len(F['C']['style_rows'])),
    ('主の升目の数・続ける最小の数', [len(T3['cells_main']), T3['pilot']['decision']['cells_min_pass'] <= len(T3['cells_main'])], [T3['pilot']['decision']['cells_total'], True]),
    ('主の順伝播（組 × 方向）', len(T3['cell_signs_main']) * n_dirs, F['E']['passes_main']),
    ('頭の近道の確かめ（組 × 二つの道 × 二つのベクトル）', len(T3['cell_signs_main']) * 4, F['E']['passes_cache']),
    ('独立の再計算の順伝播', len(T3['independent_recompute']['new_paths']) * n_v * per_row, F['E']['passes_recompute']),
    ('独立の再計算のトークン', tok_rc, F['E']['tokens_recompute']),
    ('下見の (vi) の順伝播（(a)・(b)）', [len(T3['cells_main']) * (bt + 1), len(T3['cells_main']) * T3['pilot']['repeat_n']], [F['E']['passes_noise_a'], F['E']['passes_noise_b']]),
    ('主の組のバッチの数と埋める数', [math.ceil((n_dirs + 1) / bt), math.ceil((n_dirs + 1) / bt) * bt - (n_dirs + 1)], F['E']['batch_fill_main']),
    ('方向の npz の本数（方向 ＋ 近道の確かめの一本）', n_dirs + 1, F['D']['npz_directions']),
    ('近道の許容の範囲（下限・上限）と一段目の許容', [T3['pilot']['cache_tol_floor'] < T3['pilot']['noise_max'], T3['independent_recompute']['tol_stage1'] <= T3['pilot']['cache_tol_floor']], [True, True]),
]
OUT['M7'] = [{'what': a, 'recomputed': b, 'printed': c, 'ok': b == c} for a, b, c in m7]

# ---------------- M8: §15 が B-lens の最終版から引く二つの事実 ----------------
BF = blob('records/Blens/results-Blens-FINAL-2026-09-24.md').split(NL)


def section_of(i):
    for j in range(i, -1, -1):
        if BF[j].startswith('## '):
            return BF[j][:60]
    return None


m8 = []
for w in ('答えの文字が一度も動いていない', '較正の検査（S4|Osec-Ncold|json）'):                 # 最終版の表の外の行は半角の縦棒で書かれている
    hits = [i for i, l in enumerate(BF) if w in l]
    m8.append({'phrase': w, 'lines': [i + 1 for i in hits], 'sections': [section_of(i) for i in hits], 'excerpt': [BF[i][:160] for i in hits]})
OUT['M8'] = m8

# ---------------- M9: 草案3 に一度も出ない正本の文 ----------------
SKIP = ('decisions', 'main_rows', 'cells_main', 'cell_signs_main', 'inputs', 'print_strings', 'clause', 'id', 'version', 'generator')
m9 = [{'path': p, 'text': t[:90]} for p, t in strings(T3, skip=SKIP) if t not in D3]
OUT['M9'] = m9

# ---------------- M10: 時点の古い語と改めた名の古い形 ----------------
STALE = ['草案2 の', '二巡目で諮る', '設計の巡で諮る', '経験の割合', 'iso_rate', '揺れの床（記述と決め）', '数値の揺れの床', 'まだ', 'これから', '諮る', 'independent_recompute.tol`', '雛形との一致を崩す版', '(vi) の升目の間の最大']
m10 = [{'line': i, 'word': w, 'text': l[:120]} for i, l in enumerate(L3, 1) for w in STALE if w in l]
OUT['M10'] = m10

json.dump(OUT, open(os.path.join(HERE, 'check-draft3-Bl3.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
esc = lambda x: str(x).replace('|', '｜').replace(NL, ' ')
M = ['# B-lens 層三の草案3 の見直しの器の検査（機械生成・`records/Bl3/draft3-review/check_draft3_Bl3.py`）', '',
     '- 入力: コミット %s の木（草案3 %s〔SHA16 %s・%d 行〕・正本〔SHA16 %s〕・設計事実〔SHA16 %s〕）。効き目は一つも計算していない。読みは付けていない（通読で付ける）。' % (
         REF, D3P, OUT['meta']['draft_sha16'], len(L3), OUT['meta']['canon_sha16'], OUT['meta']['facts_sha16']), '',
     '## M1 SHA16', '', '| 所 | パス | 印字 | 今 | 出所 | 合う |', '|---|---|---|---|---|---|'] + [
     '| %s | `%s` | %s | %s | %s | %s |' % (x['where'], x['path'], x['printed'], x['now'], x['source'], '合う' if x['ok'] else '**合わない**') for x in OUT['M1']] + [
     '', '## M2 パス', '', '| パス | 最初に見た所 | 在るか |', '|---|---|---|'] + ['| `%s` | %s | %s |' % (x['path'], x['first_seen'], x['status']) for x in OUT['M2']] + [
     '', '## M3 番号', '', '| 番号 | 最初に見た所 | 台帳・表・記録に在るか |', '|---|---|---|'] + ['| %s | %s | %s |' % (x['id'], x['first_seen'], '在る' if x['ok'] else '**無い**') for x in OUT['M3']] + [
     '', '## M4 鍵の名（code span）', '', '| 字句 | 最初に見た所 | 解けた先 |', '|---|---|---|'] + ['| `%s` | %s | %s |' % (esc(x['token']), x['first_seen'], x['status']) for x in OUT['M4']] + [
     '', '## M5 節の参照', '', '| 行 | 参照 | 他の文書の節 | 節が在る | 見出し | 前後 |', '|---|---|---|---|---|---|'] + [
     '| %d | §%s | %s | %s | %s | %s |' % (x['line'], x['ref'], 'はい' if x['other_doc'] else '', '在る' if x['exists'] else '**無い**', esc(x['heading']), esc(x['context'])) for x in OUT['M5']] + [
     '', '## M6 数の検査と禁止語の走査', '',
     '- 文書の登録検査の未登録 %d・正本の説明文の未登録 %d・生成器の文字列リテラルの構造でない数 %s・禁止語の当たり %d・組み立ての記録の「違反の合計: 0」: %s。' % (
         OUT['M6']['doc_unregistered'], OUT['M6']['canon_unregistered'], '・'.join('%s %d' % kv for kv in OUT['M6']['generator_literals'].items()), len(OUT['M6']['ban_hits']), OUT['M6']['lint_record_total_zero']),
     '', '## M7 派生の数', '', '| 何 | 計算し直した値 | 印字された値 | 合う |', '|---|---|---|---|'] + [
     '| %s | %s | %s | %s |' % (x['what'], esc(x['recomputed']), esc(x['printed']), '合う' if x['ok'] else '**合わない**') for x in OUT['M7']] + [
     '', '## M8 §15 が B-lens の最終版から引く事実', '', '| 字句 | 行 | 節 | 抜き書き |', '|---|---|---|---|'] + [
     '| %s | %s | %s | %s |' % (x['phrase'], x['lines'], esc(x['sections']), esc(x['excerpt'])) for x in OUT['M8']] + [
     '', '## M9 草案3 に一度も出ない正本の文（%d）' % len(OUT['M9']), '', '| 正本の置き場 | 文の頭 |', '|---|---|'] + ['| `%s` | %s |' % (x['path'], esc(x['text'])) for x in OUT['M9']] + [
     '', '## M10 時点の古い語と改めた名の古い形（%d）' % len(OUT['M10']), '', '| 行 | 語 | 行の頭 |', '|---|---|---|'] + ['| %d | %s | %s |' % (x['line'], x['word'], esc(x['text'])) for x in OUT['M10']] + [
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'check-draft3-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(M))
bad = sum(not x['ok'] for x in OUT['M1']) + sum(x['status'] == '無い' for x in OUT['M2']) + sum(not x['ok'] for x in OUT['M3']) + sum(x['status'] == '**解けない**' for x in OUT['M4']) + \
      sum(not x['exists'] and not x['other_doc'] for x in OUT['M5']) + OUT['M6']['doc_unregistered'] + OUT['M6']['canon_unregistered'] + sum(OUT['M6']['generator_literals'].values()) + len(OUT['M6']['ban_hits']) + sum(not x['ok'] for x in OUT['M7'])
print('wrote check-draft3-Bl3.{md,json} | M1 %d | M2 %d | M3 %d | M4 %d | M5 %d | M7 %d | M9 %d | M10 %d | flagged %d' % (
    len(OUT['M1']), len(OUT['M2']), len(OUT['M3']), len(OUT['M4']), len(OUT['M5']), len(OUT['M7']), len(OUT['M9']), len(OUT['M10']), bad))
