# -*- coding: utf-8 -*-
"""collect_bans_E3.py v0（2026-10-14・段階 E の枠〔草案6・刻んだ枠 SHA16 AB7491FF30074FBD〕§3-6 と裁定 D432-2・E3 の起草の前に、禁止の語と置き方の柵を器で集める・コーディネータ南無弥勒如来）。
書く物（一度だけ）: `E/addendum1/bans-E3.json`（走査の器が読む一覧と出所）・`E/addendum1/bans-E3.md`（人が読む一覧と、柵の節の逐語）。
読む物（読むだけ・封の置き場は読まない）:
  - 公開の置き場: 各段の正本 `design/contrasts-*.json`・凍結の本文と最終版の柵の節・中間総括の §5 と照らしの記録の json・README の柵の節・`arms/NOTICE.md`。どれもコミットと同じバイトであることを git で照らす。
  - 内部の置き場: 刻んだ枠（草案6）・計画書 v3.0・D1′E の禁じる言い換えの器・裁定 D432 の記録（SHA16 を照らす）。
集め方:
  - 機械の一覧: 正本の `print_strings` の禁止の一覧・読みの表の `never`・B′ の要約と根の句の `never`・追補 F と M と V′ の価値語の文の一文目の「」・中間総括の 122 語（凍結の器 `build_report_Bprime.bans_of` と同じ集め方に足した語を足し、数を照らしの記録と照らす）・D1′E の禁じる言い換えの器の日本語の一覧と英語の型・枠 §3-6 の段階 E の足し・枠 §4 と §5 の計算二の書かない句。
  - 柵の節の「」: 起草者が柵の行ごとに、その行が「書かない・読まない・用いない」と定めた句だけを選ぶ（PICKS・選びは起草者の判じ）。器は、選んだ「」がその行にあることを照らす。選ばなかった「」は一覧に残す。
  - 置き方の柵: 柵の節の行を逐語で写す（行の番号とファイルの SHA つき）。枠 §3-6 が名指した四つの例（腕を効き目の順に並べない・上向きの操作の手順を書かない・冷徹一行の逐語の扱い・B′ の二つの機種の率を並べない）の在りかを器で探す。
  - 起草者が追記一で決める決まり（集めた物ではない）: 成功の定義の言い換えの決まり（D432-2）・二つの版をつなぐ語の決まり・文脈の語（床の持続の要約の「安全」・COI の欄の「対処した」「防いだ」）の決まり。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, ast, hashlib, datetime, subprocess
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
INT = os.path.dirname(os.path.dirname(HERE))
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
OUT_J = os.path.join(HERE, 'bans-E3.json')
OUT_M = os.path.join(HERE, 'bans-E3.md')
for p_ in (OUT_J, OUT_M):
    assert not os.path.exists(p_), ('一度だけ', p_)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
SEALED = ('D0/sealed', 'D1/sealed', 'D1/probe-sealed', 'D1p/probe-sealed', 'D1pE/sealed', 'D1pE/probe-sealed')
sha_b = lambda b: hashlib.sha256(b).hexdigest().upper()
INPUTS = {}


def read(place, rel, want16=None):
    assert not any(rel.startswith(s) for s in SEALED), ('封の置き場', rel)
    root = PUB if place == 'PUB' else INT
    b = open(os.path.join(root, *rel.split('/')), 'rb').read()
    s = sha_b(b)
    if want16:
        assert s[:16] == want16, (rel, s[:16], want16)
    if place == 'PUB':
        assert subprocess.run(['git', '-C', PUB, 'ls-files', '--error-unmatch', rel], capture_output=True).returncode == 0, ('追跡されていない', rel)
        assert subprocess.run(['git', '-C', PUB, 'diff', '--quiet', 'HEAD', '--', rel]).returncode == 0, ('コミットと違う', rel)
    INPUTS[rel] = {'place': '公開' if place == 'PUB' else '内部', 'sha256': s, 'bytes': len(b)}
    return b.decode('utf-8')


QUOTE = re.compile(r'「([^「」]+)」')
words = {}      # 語 → 出所の並び（日本語は部分一致で当てる）
order = []


def add(w, src):
    w = w.strip()
    assert w, src
    if w not in words:
        words[w] = []
        order.append(w)
    if src not in words[w]:
        words[w].append(src)


patterns = {}   # 英語の型（正規表現）→ 出所


def add_pat(p, src):
    patterns.setdefault(p, [])
    if src not in patterns[p]:
        patterns[p].append(src)


json_rules = []   # 正本の json にある、語ではない決まり（そのまま写す）

# ---- 1. 各段の正本（design/contrasts-*.json）
for k in ('A', 'B', 'Bl3', 'Blens', 'Bprime', 'F', 'M', 'Vprime'):
    rel = 'design/contrasts-%s.json' % k
    J = json.loads(read('PUB', rel))
    for key, v in J.get('print_strings', {}).items():
        if 'ban' in key and isinstance(v, list):
            for w in v:
                add(w, '%s#print_strings.%s' % (rel, key))
        elif 'ban' in key:
            json_rules.append({'src': '%s#print_strings.%s' % (rel, key), 'text': v})
    for i, r in enumerate(J.get('reading_rules', [])):
        nv = r.get('never')
        if nv is None:
            continue
        for w in (nv if isinstance(nv, list) else nv.split('・')):
            if w.startswith('`'):
                json_rules.append({'src': '%s#reading_rules[%d].never' % (rel, i), 'text': w})
            else:
                add(w, '%s#reading_rules[%d].never' % (rel, i))
    if k == 'Bprime':
        for w in J['reading']['summary']['never']:
            add(w, '%s#reading.summary.never' % rel)
        for w in J['fixed_sentences']['root_counts']['never']:
            add(w, '%s#fixed_sentences.root_counts.never' % rel)
        for t in J['computation']['before_seal']['must_not_print']:
            json_rules.append({'src': '%s#computation.before_seal.must_not_print' % rel, 'text': t})
    vs = {'F': J.get('value_word_ban'), 'M': J.get('value_word_ban'), 'Vprime': J['families']['Vprime_b']['falsification']['value_word_ban'] if k == 'Vprime' else None}.get(k)
    if vs:
        key = 'families.Vprime_b.falsification.value_word_ban' if k == 'Vprime' else 'value_word_ban'
        first, rest = vs.split('。', 1)
        for w in QUOTE.findall(first):
            add(w, '%s#%s（一文目の「」）' % (rel, key))
        if rest.strip():
            json_rules.append({'src': '%s#%s（二文目から）' % (rel, key), 'text': rest.strip()})
n_after_contrasts = len(words)

# ---- 2. 中間総括の 122 語（凍結の器 build_report_Bprime.bans_of と同じ集め方 ∪ 足した語）
CB = json.loads(read('PUB', 'design/contrasts-Bprime.json'))
CHK = json.loads(read('PUB', 'summary/summary-interim-FINAL-2026-10-02-checks.json'))
read('PUB', 'tools/build_report_Bprime.py')
KEYS = ('value_word_ban', 'mechanism_word_ban', 'added_ban', 'reading_never_ban', 'reading_never_ban_bprime', 'added_ban_bprime', 'free_text_ban_bprime')


def bans_of(C, free=True):   # tools/build_report_Bprime.py の bans_of を写した（替えない）
    ps = C['print_strings']
    out = []
    for k_ in KEYS[:6] + ((KEYS[6],) if free else ()):
        out += [w for w in ps[k_] if w not in out]
    for r in C['reading_rules']:
        out += [w for w in r.get('never', []) if w not in out and not w.startswith('`')]
    out += [w for w in C['fixed_sentences']['root_counts']['never'] if w not in out]
    return out


src_bo = open(os.path.join(PUB, 'tools', 'build_report_Bprime.py'), encoding='utf-8').read()
assert "for k in ('value_word_ban', 'mechanism_word_ban', 'added_ban', 'reading_never_ban', 'reading_never_ban_bprime', 'added_ban_bprime') + (('free_text_ban_bprime',) if free else ()):" in src_bo
EXTRA = CHK['extra_words']
INTERIM = sorted(set(bans_of(CB)) | set(EXTRA))
bd = sorted(['%s %d' % (k_, len(CB['print_strings'][k_])) for k_ in KEYS] + ['extra %d' % len(EXTRA)])
assert len(INTERIM) == CHK['ban_list_n'] == 122 and bd == sorted(CHK['ban_list_breakdown']), (len(INTERIM), bd)
for w in INTERIM:
    add(w, 'summary/summary-interim-FINAL-2026-10-02-checks.json（中間総括の 122 語）')
interim_new = [w for w in INTERIM if words[w] == ['summary/summary-interim-FINAL-2026-10-02-checks.json（中間総括の 122 語）']]

# ---- 3. D1′E の禁じる言い換えの器（替えない・凍結の本文 §9 の SHA16）
SCAN = 'D1pE/scan_banned_phrases_D1pE.py'
tree = ast.parse(read('INT', SCAN, '04B26915076914DC'))
lists = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ('JA', 'EN', 'ALLOW_QUOTES'):
        lists[node.targets[0].id] = ast.literal_eval(node.value)
assert len(lists['JA']) == 24 and len(lists['EN']) == 13, (len(lists['JA']), len(lists['EN']))
for w in lists['JA']:
    add(w, '%s#JA' % SCAN)
for p_ in lists['EN']:
    add_pat(p_, '%s#EN' % SCAN)
TEMPLATE_D1pE = {'src': '%s（許す文の型の崩れ）' % SCAN, 'rule': '「族」か「family」と「英語」か「English」を含む行に、英語の too・also・as well・even があるか、「でも」と「英語の送る文」があれば当たり（集計の器が書く許す文の型だけを許す・D388-2・D391-5）'}

# ---- 4. 刻んだ枠（草案6）: §3-6 の段階 E の足し・§4 と §5 の計算二の書かない句・§3-9 の成功の定義の決まり
FRAME = 'E/00-frame-E-draft6.md'
FR = read('INT', FRAME, 'AB7491FF30074FBD').split(NL)


def fline(n, head):
    t = FR[n - 1]
    assert t.startswith(head) or head in t, (n, t[:60])
    return t


t88 = fline(88, '  - 二つの版を一つの主語でまとめる言い方: ')
for w in QUOTE.findall(t88):
    add(w, '%s:88（§3-6 の段階 E の足し・二つの版を一つの主語でまとめる言い方）' % FRAME)
t89 = fline(89, '  - 保存性の語（D425-3・ED2-19）: ')
for w in QUOTE.findall(t89):
    add(w, '%s:89（§3-6 の段階 E の足し・保存性の語）' % FRAME)
t90 = fline(90, '  - 英語の同じ意味の語（禁じる言い換えの英語の足し）: ')
EN_ADD = t90.split('）: ', 1)[1].rstrip('。').split('・')
assert len(EN_ADD) == 8, EN_ADD
for w in EN_ADD:
    add_pat(re.escape(w).replace('\\ ', ' '), '%s:90（§3-6 の段階 E の足し・英語の同じ意味の語）' % FRAME)
t91 = fline(91, '  - 英語の版で二つの版をつなぐ語（付録 C の型の外で使わない）: ')
part91 = t91.split('）: ', 1)[1]
CONNECTORS = part91.split('。')[0].split('・')
assert len(CONNECTORS) == 10 and part91.split('。')[1].strip() == '日本語の係助詞「も」で二つの版をつなぐ形', (CONNECTORS, part91)
t141 = fline(141, '「機種をまたいで働く」「一般化した」の類の言い方をしない')
for w in QUOTE.findall(t141):
    add(w, '%s:141（§4 の書かない言い方）' % FRAME)
t158 = fline(158, '- 読みの決まり: 対称だった・対称でなかったとは書かない')
for w in re.search(r'読みの決まり: (.+?)とは書かない', t158).group(1).split('・'):
    add(w, '%s:158（§5 の計算二の読みの決まり）' % FRAME)
t121 = fline(121, '満たした・満たさなかったと書かない')

# ---- 5. 計画書 v3.0（内部）: 「**柵**」の行と §8-補 の 9
PLAN = 'plans/plan-framing-sensitivity-scale-and-mechanism-v3.0-2026-10-13.md'
PL = read('INT', PLAN, '8165808D28274E82').split(NL)
plan_fence = [i + 1 for i, t in enumerate(PL) if '**柵**' in t]
coi9 = [i + 1 for i, t in enumerate(PL) if t.startswith('9. **COI 記帳は事実の列挙**')]
assert len(plan_fence) == 5 and len(coi9) == 1, (plan_fence, coi9)
floor_line = [n for n in plan_fence if '床の持続を「安全」「頑健」「耐えた」の語で要約しない' in PL[n - 1]]
assert len(floor_line) == 1 and '「対処した」「防いだ」を COI 欄に書かない' in PL[coi9[0] - 1]

# ---- 6. 柵の節（凍結の本文と最終版）・最終版の §0 の柵の行・中間総括 §5・README の柵・NOTICE
HEAD = re.compile(r'^(#{1,6}) ')
SECS = [
    ('design/design-v1.0-FROZEN.md', ['## 13. ']),
    ('design/design-stageVprime-FROZEN.md', ['### 2.8 ', '## 3. ']),
    ('design/design-stageM-FROZEN.md', ['### 2.8 ', '## 3. ']),
    ('design/design-stageF-FROZEN.md', ['### 2.8 ', '## 3. ']),
    ('design/design-stageA-FROZEN.md', ['### 2.15 ', '## 3. ']),
    ('design/design-stageB-FROZEN.md', ['### 2.11 ', '### 2.12 ', '## 3. ']),
    ('design/design-Blens-FROZEN.md', ['## 5. ']),
    ('design/design-Bl3-FROZEN.md', ['## 9. ']),
    ('design/design-Bprime-FROZEN.md', ['## 9. ']),
    ('records/pilotC/00-frame-pilotC-2026-10-02.md', ['## 9. ']),
    ('records/D1p/00-frame-D1p.md', ['## 9. ', '## 11. ']),
    ('records/D1pE/00-frame-D1pE.md', ['## 9. ', '## 11. ']),
    ('records/results/results-report-FINAL-2026-09-07.md', ['## 3. ', '## 4. ', '## 7. ']),
    ('records/vprime/results-report-Vprime-FINAL-2026-09-09.md', ['## 10. ']),
    ('records/M/results-report-M-FINAL-2026-09-11.md', ['## 7. ']),
    ('records/F/results-report-F-FINAL-2026-09-12.md', ['## 5. ']),
    ('records/A/results-report-A-FINAL-2026-09-17.md', ['## 9. ']),
    ('records/B/results-B-FINAL-2026-09-23.md', ['## 4. ', '## 6. ']),
    ('records/Blens/results-Blens-FINAL-2026-09-24.md', ['## 9. ']),
    ('records/Bl3/results-Bl3-FINAL-2026-09-27.md', ['## 7. ']),
    ('records/Bprime/results-Bprime-FINAL-2026-10-01.md', ['## 10. ']),
    ('records/D1p/results-D1p-FINAL-2026-10-11.md', ['## 5. ']),
    ('records/D1pE/results-D1pE-FINAL-2026-10-13.md', ['## 5. ']),
    ('summary/summary-interim-FINAL-2026-10-02.md', ['## 5. ']),
    ('README.md', ['## 柵（読む前に置く）']),
]
FINALS0 = ['records/results/results-report-FINAL-2026-09-07.md', 'records/vprime/results-report-Vprime-FINAL-2026-09-09.md', 'records/M/results-report-M-FINAL-2026-09-11.md',
           'records/F/results-report-F-FINAL-2026-09-12.md', 'records/A/results-report-A-FINAL-2026-09-17.md', 'records/B/results-B-FINAL-2026-09-23.md',
           'records/Blens/results-Blens-FINAL-2026-09-24.md', 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', 'records/Bprime/results-Bprime-FINAL-2026-10-01.md',
           'records/D1p/results-D1p-FINAL-2026-10-11.md', 'records/D1pE/results-D1pE-FINAL-2026-10-13.md']
CUE = re.compile(r'書かない|書かず|使わない|使わず|用いない|用いず|言わない|とは言えない|読まない|読まず|要約しない|置かない|並べない|作らない|入れない|引かない|比べない|持ち込まない|外挿しない|帰さない|帰属せず|導かない|禁')
fence = []
texts = {}


def section(rel, head):
    L = texts[rel]
    idx = [i for i, t in enumerate(L) if t.startswith(head)]
    assert len(idx) == 1, (rel, head, idx)
    s = idx[0]
    lev = len(HEAD.match(L[s]).group(1))
    e = s + 1
    while e < len(L) and not (HEAD.match(L[e]) and len(HEAD.match(L[e]).group(1)) <= lev):
        e += 1
    return s, e


def put(rel, sec, n, t, place='公開'):
    fence.append({'path': rel, 'place': place, 'section': sec, 'line': n, 'text': t, 'cue': bool(CUE.search(t)), 'quoted': QUOTE.findall(t)})


sections_done = []
for rel, heads in SECS:
    texts[rel] = read('PUB', rel).split(NL)
    for h in heads:
        s, e = section(rel, h)
        sec = texts[rel][s].strip()
        sections_done.append({'path': rel, 'section': sec, 'lines': [s + 1, e]})
        for j in range(s + 1, e):
            if texts[rel][j].strip():
                put(rel, sec, j + 1, texts[rel][j])
for rel in FINALS0:
    s, e = section(rel, '## 0. ')
    sec = texts[rel][s].strip()
    hit = [j for j in range(s + 1, e) if '柵' in texts[rel][j]]
    sections_done.append({'path': rel, 'section': sec + '（「柵」の字を含む行だけ）', 'lines': [s + 1, e], 'taken': [j + 1 for j in hit]})
    for j in hit:
        put(rel, sec + '（「柵」の字を含む行）', j + 1, texts[rel][j])
NOTICE = 'arms/NOTICE.md'
texts[NOTICE] = read('PUB', NOTICE).split(NL)
for j, t in enumerate(texts[NOTICE]):
    if t.strip() and not t.startswith('# '):
        put(NOTICE, '（ファイル全体）', j + 1, t)
sections_done.append({'path': NOTICE, 'section': '（ファイル全体・題の行を除く）', 'lines': [1, len(texts[NOTICE])]})
texts[PLAN] = PL
for n in plan_fence + coi9:
    sec = [PL[i] for i in range(n - 1, -1, -1) if HEAD.match(PL[i])][0].strip()
    t = PL[n - 1]
    if n in plan_fence and not t.lstrip('- ').startswith('**柵**'):   # 行の途中の「**柵**」は、その字から一文だけ写す（続く文は柵の文でない）
        t = t[t.index('**柵**'):]
        t = t[:t.index('。') + 1]
        assert t == '**柵**: §4-B の柵をそのまま当てる。', t
    put(PLAN, sec, n, t, '内部')
sections_done.append({'path': PLAN, 'section': '「**柵**」の字を含む行（行の途中の「**柵**」はその字から一文だけ）と §8-補 の 9', 'lines': plan_fence + coi9})

# ---- 7. 起草者が柵の行の「」から選んだ語（その行が書かない・読まない・用いないと定めた句だけ・選びは起草者の判じ）
PICKS = [
    ('design/design-stageVprime-FROZEN.md', 67, '悪意の枠は無害', None),
    ('design/design-stageVprime-FROZEN.md', 67, '逆用は効かない', None),
    ('design/design-stageM-FROZEN.md', 93, 'ロールプレイという枠付け', None),
    ('design/design-stageM-FROZEN.md', 94, '破局ゼロ', None),
    ('design/design-stageM-FROZEN.md', 95, '効果なし', None),
    ('design/design-stageM-FROZEN.md', 96, '第一走行が誤りだった', None),
    ('design/design-stageM-FROZEN.md', 96, '第二走行が誤りだった', None),
    ('design/design-stageM-FROZEN.md', 97, '効果が無かった', None),
    ('design/design-stageM-FROZEN.md', 97, '固有でなかった', None),
    ('design/design-stageM-FROZEN.md', 98, 'として句が違った', None),
    ('design/design-stageF-FROZEN.md', 82, '検査と認識した', None),
    ('design/design-stageF-FROZEN.md', 82, '付記を読まなかった', None),
    ('design/design-stageF-FROZEN.md', 82, '読んだが黙っていた', None),
    ('design/design-stageF-FROZEN.md', 95, '安全になった', None),
    ('design/design-stageF-FROZEN.md', 98, '高度なモデル', None),
    ('design/design-stageA-FROZEN.md', 123, '規模の効果', None),
    ('design/design-stageA-FROZEN.md', 126, '規模とともに差が広がった', None),
    ('design/design-stageA-FROZEN.md', 126, '狭まった', None),
    ('design/design-stageA-FROZEN.md', 128, '傾向が立たなかった', None),
    ('design/design-stageB-FROZEN.md', 353, 'Nk 方向の効果', None),
    ('design/design-stageB-FROZEN.md', 357, '枠組みが表現に無い', None),
    ('design/design-stageB-FROZEN.md', 362, 'O に特有でない', None),
    ('design/design-stageB-FROZEN.md', 367, '意識', None),
    ('design/design-stageB-FROZEN.md', 368, '機構を特定', None),
    ('design/design-stageB-FROZEN.md', 375, '枠組み効果は線形表現に乗らない', None),
    ('records/D1p/00-frame-D1p.md', 281, '存在論的枠組みの効果', None),
    ('records/D1pE/00-frame-D1pE.md', 268, '意味', ['「意味」の効き目', '意味の効き目']),
    ('records/D1pE/results-D1pE-FINAL-2026-10-13.md', 502, '意味', ['「意味」の効き目', '意味の効き目']),
    ('records/results/results-report-FINAL-2026-09-07.md', 98, '世俗語に置き換えても同じ', None),
    ('records/results/results-report-FINAL-2026-09-07.md', 132, '4B に意識／魂があるように扱え', None),
    ('records/F/results-report-F-FINAL-2026-09-12.md', 282, '場面の出来事が起こらないと告げたことが効いた', None),
    ('records/B/results-B-FINAL-2026-09-23.md', 192, '線形表現に乗らない', None),
    ('records/B/results-B-FINAL-2026-09-23.md', 233, '加算族の S1 だけは残る', None),
    (PLAN, 0, '言語の一般的性質', None),
    (PLAN, 0, '大きいモデルは安全（危険）', ['大きいモデルは安全', '大きいモデルは危険']),
    (PLAN, 0, '招請文の内容の力', None),
    (PLAN, 0, '対処した', None),
    ('summary/summary-interim-FINAL-2026-10-02.md', 399, '4B を成功の予兆と読まない', ['成功の予兆']),
    ('README.md', 15, '隠密介入', None),
]
picks = []
for rel, n, q, derived in PICKS:
    if n == 0:   # 計画書の「**柵**」の行と §8-補 の 9 から、その「」のある行を器で探す
        cand = [m for m in plan_fence + coi9 if '「%s」' % q in PL[m - 1]]
        assert len(cand) == 1, (q, cand)
        n = cand[0]
    t = texts[rel][n - 1]
    assert '「%s」' % q in t, ('選んだ「」が行に無い', rel, n, q)
    assert any(f['path'] == rel and f['line'] == n for f in fence), ('柵の節の外の行', rel, n)
    forms = derived or [q]
    for w in forms:
        add(w, '%s:%d（柵の行の「%s」・起草者が選んだ）' % (rel, n, q))
    picks.append({'path': rel, 'line': n, 'quoted': q, 'forms': forms, 'cue_in_line': bool(CUE.search(t))})

# ---- 8. 柵の行の「」の出所を足し、選ばなかった「」を残す
picked_keys = {(p['path'], p['line'], p['quoted']) for p in picks}
RULE_WORDS = {'安全': 'floor（床の持続の要約）'}
not_picked, in_rules = [], []
for f in fence:
    for q in f['quoted']:
        if (f['path'], f['line'], q) in picked_keys:
            continue
        if q in words:
            add(q, '%s:%d（柵の行の「」・一覧の語と同じ字）' % (f['path'], f['line']))
        elif q in RULE_WORDS:
            in_rules.append({'path': f['path'], 'line': f['line'], 'quoted': q, 'rule': RULE_WORDS[q]})
        else:
            not_picked.append({'path': f['path'], 'line': f['line'], 'quoted': q, 'contains_list_words': [w for w in order if w in q]})

# ---- 9. 枠 §3-6 が名指した置き方の柵の在りか
NAMED = [('腕を効き目の順に並べない', [['効き目順'], ['効き目の順']]),
         ('上向きの操作の手順を書かない', [['再現手順'], ['再現の手順']]),
         ('冷徹一行の逐語の扱い', [['冷徹一行', '逐語']]),
         ('B′ の二つの機種の率を並べない', [['S10'], ['二つの機種の値']])]
named = []
for name, alts in NAMED:
    where = ['%s:%d' % (f['path'], f['line']) for f in fence if any(all(k in f['text'] for k in alt) for alt in alts)]
    assert where, name
    named.append({'name': name, 'keys': alts, 'where': where})

# ---- 10. 起草者が追記一で決める決まり（集めた物ではない・走査の器が当てる）
RULES = {
    'connectors_en': {'by': '枠 §3-6（草案6 の 91 行）の語・当て方は追記一', 'words': CONNECTORS,
                      'pair_en_both': ['Japanese', 'English'], 'pair_en_any': [r'both (?:versions|registrations|languages)', r'the other (?:language|registration|version)', r'\b[Cc]hapters? [68]\b', r'\btwo registrations\b'],
                      'rule': '一つの文に、つなぐ語と、二つの版を指す語（Japanese と English の両方か、pair_en_any のどれか）があれば当たり（付録 C の型の逐語の写しは、当たりとして記して印を付ける）'},
    'ja_mo': {'by': '枠 §3-6（草案6 の 91 行）の決まり・型は追記一', 're': r'(?:日本語|英語)(?:の送る文の登録|の登録|の版|版)?(?:で|に|と|について|では)?も',
              'rule': '日本語か英語の版を指す語に係助詞「も」が続く形は、文脈によらず当たり（目で判じて記す）'},
    'floor': {'by': '計画書 v3.0 の段階 A の柵（%s:%d）・当て方は追記一' % (PLAN, floor_line[0]), 'ja': ['安全', '頑健', '耐えた'], 'ja_with_any': ['床', '持続'],
              'en': [r'\bsafe', r'\brobust', r'\bwithst', r'\bheld up\b', r'\bresist'], 'en_with_any': [r'\bfloor'],
              'rule': '一つの文に、床か持続（英語は floor）と、この語のどれかがあれば当たり（床の持続を安全・頑健・耐えたの語で要約しない）。頑健と耐えたは、ほかの文でも一覧の語として当たる'},
    'coi': {'by': '計画書 v3.0 の §8-補 の 9（%s:%d）・当て方は追記一' % (PLAN, coi9[0]), 'ja': ['対処した', '防いだ'], 'en': [r'\baddressed\b', r'\bprevent', r'\bmitigat', r'\bguarded\b'],
            'section_heading': r'COI|利益相反|[Cc]onflicts? of [Ii]nterest|[Cc]ompeting [Ii]nterests',
            'rule': '見出しが COI か利益相反の節の中にこの語があれば当たり（直す・逐語の引用の中を除く）。節の外の「対処した」も一覧の語として当たる（目で判じて記す）・「防いだ」はほかの節でも価値語として当たる'},
    'success': {'by': '枠 §3-9（草案6 の 121 行）の決まりと裁定 D432-2・言い換えの語と当て方は追記一',
                'terms_ja': ['成功', '「最小」', '「中」', '「最大」', '最小の段', '中の段', '最大の段', '最小・中・最大', '三つの段', '最小:', '最大:', '最小：', '最大：'],
                'terms_en': [r'success', r'\btiers?\b', r'\bminimum tier', r'\bmedium tier', r'\bmiddle tier', r'\bmaximum tier', r'\bMinimum:', r'\bMaximum:', r'\bMedium:'],
                'paraphrase_ja': ['満た', '達し', '達成', '到達', '届い', '届か', '当た', 'クリア', '果たし', '果たせ', '成し遂げ', '成功し', '失敗し', '実現', '叶', '合格', '至っ', '至ら'],
                'paraphrase_en': [r'\bmet\b', r'\bmeets?\b', r'\bachiev', r'\bsatisf', r'\bfulfil', r'\breach', r'\battain', r'\baccomplish', r'\bsucceed', r'\bfail', r'\bpass(?:ed|es)?\b', r'\bfalls? short\b', r'\bfell short\b', r'\bhit\b', r'\bmade it\b'],
                'rule': '一つの文に、成功の定義を指す語と言い換えの語があれば当たり（直す・章 9 の §3-9 の所の逐語の引用は記して印を付ける）。成功の定義を指す語のある文は、当たりでなくてもすべて一覧に出し、目で読む'},
}

# ---- 11. 書く
now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
me = sha_b(open(os.path.abspath(__file__), 'rb').read())
ja_words = [{'w': w, 'sources': words[w]} for w in order]
en_pats = [{'re': p_, 'sources': s} for p_, s in patterns.items()]
counts = {'words_ja': len(ja_words), 'words_from_contrasts': n_after_contrasts, 'interim_122_new_vs_contrasts': len(interim_new), 'd1pe_ja': len(lists['JA']), 'd1pe_en': len(lists['EN']),
          'frame_stageE_ja': len(QUOTE.findall(t88)) + len(QUOTE.findall(t89)), 'frame_stageE_en': len(EN_ADD), 'frame_s4_s5': 4, 'picks': len(picks), 'pick_forms': sum(len(p['forms']) for p in picks),
          'patterns_en': len(en_pats), 'fence_lines': len(fence), 'fence_lines_cue': sum(1 for f in fence if f['cue']), 'fence_sections': len(sections_done), 'not_picked_quotes': len(not_picked), 'quotes_in_rules': len(in_rules), 'json_rules': len(json_rules)}
rec = {'tool': 'collect_bans_E3.py v0', 'tool_sha256': me, 'when_jst': now, 'frame': {'path': FRAME, 'sha16': 'AB7491FF30074FBD'}, 'ruling': 'plans/rulings-D432-2026-10-14.md（D432-2）',
       'inputs': INPUTS, 'counts': counts, 'words_ja': ja_words, 'patterns_en': en_pats, 'template_D1pE': TEMPLATE_D1pE, 'rules_by_addendum1': RULES,
       'json_rules': json_rules, 'picks': picks, 'not_picked_quotes': not_picked, 'quotes_in_rules': in_rules, 'named_examples': named, 'sections': sections_done, 'fence_lines': fence,
       'interim_check': {'n': len(INTERIM), 'breakdown': bd, 'extra_words': EXTRA, 'new_vs_contrasts': interim_new},
       'note': '日本語の語は部分一致で当てる。英語の型は前後が英字でない所で、大文字と小文字を区別せずに当てる（D1′E の器と同じ）。一覧は網羅ではない。当たりの無いことを、禁じた書き方の無いことの証にしない。',
       'clause': CLAUSE}
json.dump(rec, open(OUT_J, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)

esc = lambda s: s.replace('|', '¦')
M = ['# 禁止の語と置き方の柵の集め（E3 の起草の前・%s 日本時間・器 `E/addendum1/collect_bans_E3.py` v0）' % now, '',
     '- 何か: 刻んだ枠（`%s`・SHA16 AB7491FF30074FBD）§3-6 の「集めるもの」と、裁定 D432-2 の決まりを、器で集めた一覧。枠の追記一（`E/00-frame-E-addendum1-2026-10-14.md`）がこの一覧を SHA で指す。' % FRAME,
     '- 機械が読む形: `E/addendum1/bans-E3.json`（同じ時に書いた）。この md は人が読む写しで、柵の節の行は逐語。',
     '- 数: 日本語の語 %d（部分一致）・英語の型 %d・起草者が柵の行から選んだ語 %d（形 %d）・柵の行 %d（手がかりの語のある行 %d・節 %d）・選ばなかった「」 %d・正本の語でない決まり %d。' % (
         counts['words_ja'], counts['patterns_en'], counts['picks'], counts['pick_forms'], counts['fence_lines'], counts['fence_lines_cue'], counts['fence_sections'], counts['not_picked_quotes'], counts['json_rules']),
     '- 一覧は網羅ではない。当たりの無いことを、禁じた書き方の無いことの証にしない（D1′E 本文 §9 と同じ）。', '',
     '## 1. 読んだ物', '', '| 置き場 | 物 | SHA16 | バイト |', '|---|---|---|---|']
for rel, v in INPUTS.items():
    M.append('| %s | `%s` | %s | %d |' % (v['place'], rel, v['sha256'][:16], v['bytes']))
M += ['', '## 2. 日本語の語（%d・部分一致で当てる・出所つき）' % len(ja_words), '', '| 語 | 出所 |', '|---|---|']
for d in ja_words:
    M.append('| %s | %s |' % (esc(d['w']), esc('／'.join(d['sources']))))
M += ['', '## 3. 英語の型（%d・前後が英字でない所で・大文字と小文字を区別しない）' % len(en_pats), '', '| 型 | 出所 |', '|---|---|']
for d in en_pats:
    M.append('| `%s` | %s |' % (esc(d['re']), esc('／'.join(d['sources']))))
M += ['', '- D1′E の器の許す文の型の崩れの決まり: %s（出所 `%s`）。' % (TEMPLATE_D1pE['rule'], SCAN), '',
      '## 4. 起草者が柵の行の「」から選んだ語（%d・その行が書かない・読まない・用いないと定めた句だけ・選びは起草者の判じ）' % len(picks), '', '| 置き場:行 | 「」 | 当てる形 |', '|---|---|---|']
for p_ in picks:
    M.append('| `%s`:%d | 「%s」 | %s |' % (p_['path'], p_['line'], esc(p_['quoted']), esc('・'.join(p_['forms']))))
M += ['', '## 5. 選ばなかった「」（%d・書く文の型・札や欄の名・規則の名・素材や場面の語・検索の語など・その行の禁じる中身は §8 の置き方の柵として残る）' % len(not_picked), '']
for d in not_picked:
    M.append('- `%s`:%d 「%s」%s' % (d['path'], d['line'], d['quoted'], ('（一覧の語を含む: %s）' % '・'.join(d['contains_list_words'])) if d['contains_list_words'] else ''))
M += ['', '- 当て方の決まり（§6）で扱う「」: ' + ('・'.join('`%s`:%d 「%s」（%s）' % (d['path'], d['line'], d['quoted'], d['rule']) for d in in_rules) or 'なし')]
M += ['', '## 6. 起草者が追記一で決める当て方（集めた物ではない）', '']
for k_, v in RULES.items():
    M.append('- **%s**（%s）: %s' % (k_, v['by'], v['rule']))
    for kk, vv in v.items():
        if kk not in ('by', 'rule'):
            M.append('  - %s: `%s`' % (kk, json.dumps(vv, ensure_ascii=False)))
M += ['', '## 7. 正本の json の、語ではない決まり（%d・逐語）' % len(json_rules), '']
for d in json_rules:
    M.append('- `%s`: %s' % (d['src'], d['text']))
M += ['', '## 8. 置き方の柵（柵の節の行の逐語・%d 行）' % len(fence), '', '- 枠 §3-6 が名指した四つの例の在り処（器が鍵の字で探した）:']
for d in named:
    M.append('  - %s: %s' % (d['name'], '・'.join(d['where'])))
M += ['- 集めた節:']
for d in sections_done:
    M.append('  - `%s` %s（行 %s）' % (d['path'], d['section'], '〜'.join(map(str, d['lines'])) if len(d['lines']) == 2 and d['section'][:1] in '#（' else '・'.join(map(str, d['lines']))))
cur = None
for f in fence:
    key = (f['path'], f['section'])
    if key != cur:
        M += ['', '### `%s`（%s）%s' % (f['path'], f['place'], f['section']), '']
        cur = key
    M.append('- %d%s: %s' % (f['line'], '〔手がかり〕' if f['cue'] else '', f['text'].strip()))
M += ['', CLAUSE, '']
open(OUT_M, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('書いた bans-E3.json（SHA-256 %s）と bans-E3.md（SHA-256 %s）・%s' % (sha_b(open(OUT_J, 'rb').read()), sha_b(open(OUT_M, 'rb').read()), now))
print('数', json.dumps(counts, ensure_ascii=False))
print('中間総括の 122 語のうち正本の一覧に無かった語:', interim_new)
