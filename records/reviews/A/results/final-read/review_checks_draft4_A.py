# -*- coding: utf-8 -*-
"""review_checks_draft4_A.py v1（2026-09-17・コーディネータ）—— 結果報告 草案4 の見直しの機械の突き合わせ（事前登録 `preregistration-review-draft4-A.md` の §2 A の M1〜M12）。
凍結物ではない（本見直しのために書いた）。先例の器 `tools/review_checks_A.py` の関数を読み込んで使う（その器は変えない）。
M11 は、凍結した組み立て器 `tools/build_report_A.py` を、草案1 と同じ入力で一時置き場に走らせ直し、区画の中身を草案4 と突き合わせる（リポジトリには書かない）。
本器は判定をしない。見つけたものを全件印字し、直すかどうかは見直しの記録で決める。
出力: 同じ置き場の review-checks-draft4-A.{md,json}（--force なしでは上書きしない）。
柵: 本器の出力のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, argparse, datetime, subprocess, tempfile, collections, hashlib

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, report_lint as RL
import review_checks_A as RC
VERSION = 'v1'
ap = argparse.ArgumentParser(); ap.add_argument('--draft', default='records/A/results-report-A-draft4-2026-09-17.md'); ap.add_argument('--force', action='store_true')
ap.add_argument('--out', default=os.path.join(HERE, 'review-checks-draft4-A'))
a = ap.parse_args()
if (os.path.exists(a.out + '.json') or os.path.exists(a.out + '.md')) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）')
rd = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda rel: runs_A.sha16_file(os.path.join(REPO, rel))
git = lambda *args: subprocess.run(['git', '-C', REPO] + list(args), capture_output=True, text=True, encoding='utf-8').stdout
status_before = git('status', '--porcelain', '--untracked-files=no')
T = runs_A.load_T(); MB = RL.machine_block(T); SIZES = T['sizes']; LB = T['families']['A_slope']['confirm_rule']['labels']
TEXT = rd(a.draft); L = TEXT.split('\n')
FZT = rd('design/design-stageA-FROZEN.md'); TPLT = rd('records/A/results-report-template-A.md'); TPL = set(TPLT.split('\n'))
AN = json.loads(rd('records/A/analysis-stageA.json'))
inside = set(); cur = False
for i, l in enumerate(L, 1):
    if l == MB['begin']:
        cur = True; inside.add(i); continue
    if l == MB['end']:
        cur = False; inside.add(i); continue
    if cur:
        inside.add(i)
OUT = collections.OrderedDict()

# ---- M1・M2・M6・M7・M8（先例の器の関数）
OUT['M1'] = RC.m1_paths(TEXT)
OUT['M2'] = RC.m2_keys(TEXT, T)
m6 = RC.m6_versions(TEXT)
for m in re.finditer(r'(?<![\w/`])(confirm_A|firth|analyze_A) (v\d+(?:\.\d+)*)', TEXT):
    fv, how, p = RC.tool_version(m.group(1) + '.py')
    m6.append({'line': RC.line_of(TEXT, m.start()), 'tool': m.group(1) + '.py', 'text_version': m.group(2), 'file_version': fv, 'how': how, 'path': p,
               'status': 'ok' if fv == m.group(2) else ('no_file_version' if fv is None else 'mismatch'), 'context': RC.ctx(TEXT, m.start(), m.end())})
OUT['M6'] = m6
OUT['M7'] = RC.m7_words(TEXT, T)
last = RC.m8_fence(TEXT)
s0 = re.search(r'^## 0\..*?(?=^## 1\.)', TEXT, flags=re.M | re.S).group(0)
OUT['M8'] = {'last_line_ok': last['ok'], 'section0_fence': bool(re.search(r'^\d+\. 本報告のいかなる数値も AI の意識.*両方向不定', s0, flags=re.M))}

# ---- M3 節の参照（報告・凍結本文・記録）
rep_heads, _ = RC.sections(TEXT)
fz_heads, fz_clauses = RC.sections(FZT)


def rec_heads(rel):
    t = rd(rel); heads = set(re.findall(r'^## (\d+)\.', t, flags=re.M)); items = set()
    for m in re.finditer(r'^## (\d+)\..*?(?=^## |\Z)', t, flags=re.M | re.S):
        for it in re.findall(r'^(\d+)\. ', m.group(0), flags=re.M):
            items.add('%s-%s' % (m.group(1), it))
    return heads, items


m3 = []
for i, l in enumerate(L, 1):
    for m in re.finditer(r'§\s?(\d+(?:\.\d+)?(?:-(?:\d+|補))?)', l):
        ref = m.group(1); before = l[max(0, m.start() - 60):m.start()]
        paths = re.findall(r'`((?:records|design|tools)/[^`]+?\.md)`', before)
        kind = None
        if re.search(r'凍結(本文)?\s?$', before) or re.search(r'凍結(本文)? (§[\d.\-]+・)*$', before) or re.search(r'（凍結 $', before):
            kind = 'frozen'
        elif re.search(r'(F|M|計画|段取り|同記録|記録)\s?$', before) and not paths:
            kind = 'other_doc'
        elif paths and re.search(r'`\s?(（[^）]*）)?\s?$', before):
            kind = 'record'
        else:
            kind = 'report'
        if kind == 'frozen':
            st = 'ok' if ref in fz_heads else 'unresolved'
        elif kind == 'record':
            h, it = rec_heads(paths[-1])
            st = 'ok' if (ref in h or ref in it) else 'unresolved'
        elif kind == 'report':
            st = 'ok' if ref in rep_heads else 'unresolved'
        else:
            st = 'external'
        m3.append({'line': i, 'ref': '§' + ref, 'kind': kind, 'path': paths[-1] if paths else None, 'status': st, 'inside_block': i in inside, 'context': l[max(0, m.start() - 30):m.end() + 10]})
    for m in re.finditer(r'\(([ivx]+)\)', l):
        if re.search(r'(読み条項|§3|条項) ?(\([ivx]+\)・?)*$', l[max(0, m.start() - 20):m.start()]):
            m3.append({'line': i, 'ref': '(%s)' % m.group(1), 'kind': 'clause', 'status': 'ok' if m.group(1) in fz_clauses else 'unresolved_clause', 'inside_block': i in inside, 'context': l[max(0, m.start() - 20):m.end() + 5]})
OUT['M3'] = m3

# ---- M4 逸脱番号と裁定の番号
dev_rows = {int(x) for x in re.findall(r'^\| D-(\d+) \|', rd('records/DEVIATIONS.md'), flags=re.M)}
listed = RC.listed_decisions(FZT)
later = set()
for t in ('records/reviews/A/results/round1/adoption-table-results-A-round1.md', 'records/reviews/A/results/round2/adoption-table-round2-A.md'):
    later |= {int(x) for x in re.findall(r'\*\*D(\d+)（', rd(t))}
known = set(listed) | {4, 5} | later
m4 = []
for i, l in enumerate(L, 1):
    for m in re.finditer(r'\bD-(\d+)(?:〜D-(\d+))?\b', l):
        nums = [int(m.group(1))] + ([int(m.group(2))] if m.group(2) else [])
        m4.append({'line': i, 'ref': m.group(0), 'kind': 'deviation', 'status': 'ok' if all(n in dev_rows for n in nums) else 'not_in_ledger', 'inside_block': i in inside})
    for m in re.finditer(r'(?<![A-Za-z0-9\-])D(\d+)(?:〜D?(\d+))?(?![\d\-])', l):
        nums = [int(m.group(1))] + ([int(m.group(2))] if m.group(2) else [])
        m4.append({'line': i, 'ref': m.group(0), 'kind': 'ruling', 'status': 'ok' if all(n in known for n in nums) else 'unlisted', 'inside_block': i in inside})
OUT['M4'] = m4
OUT['M4_known_rulings'] = sorted(known)

# ---- M5 採否表の番号
pset = set()
for t in RC.TABLES + ['records/reviews/A/results/round1/adoption-table-results-A-round1.md', 'records/reviews/A/results/round2/adoption-table-round2-A.md']:
    pset |= {int(x) for x in re.findall(r'^\|\s*P(\d+)', rd(t), flags=re.M)}
m5 = []
for i, l in enumerate(L, 1):
    for m in re.finditer(r'(?<![A-Za-z0-9])P(\d+)(?:〜P?(\d+))?(?!\d)', l):
        nums = [int(m.group(1))] + ([int(m.group(2))] if m.group(2) else [])
        m5.append({'line': i, 'ref': m.group(0), 'status': 'ok' if all(n in pset for n in nums) else 'not_in_tables', 'inside_block': i in inside})
OUT['M5'] = m5

# ---- M9 雛形の行の残り（区画の外）
OUT['M9'] = [{'line': i, 'text': l[:160]} for i, l in enumerate(L, 1) if i not in inside and l.strip() and l in TPL]

# ---- M10 記入の SHA16
sess = [json.loads(rd('results/sessions-A/' + f)) for f in sorted(os.listdir(os.path.join(REPO, 'results', 'sessions-A'))) if f.startswith('stageA')]
pip = collections.Counter(s['pip_freeze_sha16'] for s in sess)
KEYS = [('雛形', 'records/A/results-report-template-A.md'), ('正本の SHA16', 'design/contrasts-A.json'), ('正本 SHA16', 'design/contrasts-A.json'), ('凍結本文の SHA16', 'design/design-stageA-FROZEN.md'),
        ('作り直した記録', 'records/A/main/identity-screen-A-regen-2026-09-17.json')]
m10 = []
for i, l in enumerate(L, 1):
    if i in inside:
        continue
    for m in re.finditer(r'\b[0-9A-F]{16}\b', l):
        h = m.group(0); before = l[:m.start()]; attr = None; want = None
        ps = list(re.finditer(r'`((?:records|design|tools|results)/[^`]+)`', before))
        if 'pip freeze' in before:
            attr = 'pip freeze（セッション記録）'; st = 'ok' if h in pip else 'mismatch'
            m10.append({'line': i, 'sha16': h, 'attributed_to': attr, 'status': st, 'sessions_with_value': pip.get(h, 0)}); continue
        near = before[-40:]
        for k, rel in KEYS:
            if k in near:
                attr, want = rel, s16(rel)
        if attr is None and ps and len(before) - ps[-1].end() < 12:
            attr = ps[-1].group(1); want = s16(attr) if os.path.exists(os.path.join(REPO, attr)) else None
        m10.append({'line': i, 'sha16': h, 'attributed_to': attr, 'actual': want, 'status': ('ok' if want == h else ('unattributed' if attr is None else 'mismatch'))})
OUT['M10'] = m10
OUT['M10_pip_freeze_counts'] = dict(pip)

# ---- M11 組み立て器の走らせ直し
tmp = tempfile.mkdtemp(prefix='rebuild_draft1_')
outp = os.path.join(tmp, 'rebuild-draft1.md')
args = [sys.executable, 'tools/build_report_A.py', '--draft', '1', '--analysis', 'records/A/analysis-stageA.json', '--identity', 'records/A/main/identity-screen-A-regen-2026-09-17.json',
        '--gate', 'records/A/gate-pilotA.json', '--calib', 'records/A/calib-stageA-calib.json',
        '--integrity', 'records/A/integrity-stageA-2026-09-17.json', 'records/A/integrity-stageA-anchor2-2026-09-17.json', 'records/A/integrity-stageA-bridge-2026-09-17.json', 'records/A/integrity-stageA-calib-2026-09-17.json',
        '--judge', 'records/A/judge-validity-A.json', '--facts', 'records/A/design-facts-A.json', '--grid', 'records/A/power-grid-A.json', '--style', 'records/A/style-stageA.json',
        '--design', 'design/design-stageA-FROZEN.md', '--freeze-verify', 'records/A/main/freeze-verify-2026-09-17.json', '--predictions', 'records/A/predictions-check-A.json',
        '--sampling', 'records/A/sampling-inspection-A-stageA-agreement.json', '--out', outp]
pr = subprocess.run(args, cwd=REPO, capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
m11 = {'returncode': pr.returncode, 'stdout_tail': pr.stdout[-400:], 'stderr_tail': pr.stderr[-400:]}
if os.path.exists(outp):
    rb = [b for _, b in RL.blocks(open(outp, encoding='utf-8').read(), T)]; db = [b for _, b in RL.blocks(TEXT, T)]
    side = json.loads(rd('records/A/results-report-A-draft1-2026-09-17-machine.json'))
    m11.update(rebuilt_blocks=len(rb), draft_blocks=len(db), sidecar_blocks=len(side['blocks']),
               differing_blocks=[k for k in range(min(len(rb), len(db))) if rb[k] != db[k]],
               rebuilt_hashes_equal_sidecar=RL.block_hashes(open(outp, encoding='utf-8').read(), T) == side['blocks'])
    diffs = []
    for k in m11['differing_blocks'][:5]:
        x, y = rb[k].split('\n'), db[k].split('\n')
        diffs.append({'block': k, 'first_diff': next(({'rebuilt': x[j][:120], 'draft': y[j][:120]} for j in range(min(len(x), len(y))) if x[j] != y[j]), {'len': (len(x), len(y))})})
    m11['diffs'] = diffs
OUT['M11'] = m11

# ---- M12 区画どうしの突き合わせ
blocks = RL.blocks(TEXT, T)
def block_after(prefix):
    i = next(k for k, l in enumerate(L) if l.startswith(prefix))
    assert L[i + 1] == MB['begin']
    return next(b for ln, b in blocks if ln == i + 2)
big = [r for r in L if re.match(r'^\| (N1|N2|S1|S4|SK):\S+ \| 残った規模', r)]
cells = [[c.strip() for c in r.strip('|').split('|')] for r in big]
lab_count = collections.Counter(c[9] for c in cells)
c12 = collections.OrderedDict()
ff = [l for l in L if l.startswith('傾きの族 35 対比のうち、')]
c12['C1_label_counts'] = {'big_table': dict(lab_count), 'first_finding_lines': len(ff), 'first_finding_consistent': all(('確証 %d' % lab_count.get(LB['confirmed'], 0)) in f and ('非有意 %d' % lab_count.get(LB['ns'], 0)) in f for f in ff),
                          'summary_row': next((l for l in L if l.startswith('| 傾きの族 | 35 |')), None)}
sg = block_after('- 様式門（機械の転記）:')
sg_rows = dict(re.findall(r'^((?:N1|N2|S1|S4|SK):\S+): 様式門 (hold|note)$', sg, flags=re.M))
big_style = {c[0]: c[7] for c in cells if c[7] in ('hold', 'note')}
c12['C2_style_rows_equal_big_table'] = sg_rows == big_style
dem = re.findall(r'^- ((?:N1|N2|S1|S4|SK):\S+): 上限＝確証／実際＝([^／]+)／理由＝([^／]+)／札の全組合せ表の行 id＝(\S+)$', block_after_ln := next(b for ln, b in blocks if b.startswith('- N1:Odose1~Onull: 上限＝')), flags=re.M)
big_dem = [(c[0], c[9], c[11], c[12]) for c in cells if c[10] == '2' and c[9] != LB['confirmed']]
c12['C3_demotions_equal_big_table'] = [(x[0], x[1], x[2], x[3]) for x in dem] == big_dem
base = {}
for r in L:
    m = re.match(r'^\| (N1|N2|S1|S4|SK) \| (\S+) \| (.+) \|$', r)
    if m and '（' in m.group(3) and 'Wilson' in m.group(3):
        vals = re.findall(r'(\d+)/(\d+)（', m.group(3))
        if len(vals) == len(SIZES) + 1:
            base[(m.group(1), m.group(2))] = [(int(k), int(n)) for k, n in vals]
cp_bad = []
for r in L:
    m = re.match(r'^\| (\S+) \| (\S+) \| (\S+) \| (N1|N2|S1|S4|SK) \| (.+) \| (—|はい) \|$', r)
    if not m or m.group(1) in ('処置腕',):
        continue
    b1, b2, sc = m.group(2), m.group(3), m.group(4); got = [x.strip() for x in m.group(5).split('|')]
    for j, s_ in enumerate(SIZES):
        k1, n1 = base[(sc, b1)][j]; k2, n2 = base[(sc, b2)][j]
        want = '%+.1f' % (100.0 * (k1 / n1 - k2 / n2))
        if got[j] != want and got[j] != '測定不能':
            cp_bad.append((sc, s_, got[j], want))
c12['C4_control_pairs_from_base_table'] = {'mismatch': cp_bad}
rc_bad = []
for l in L:
    m = re.match(r'^((?:N1|N2|S1|S4|SK)):(\S+)~recipe: ([+\-]\d+\.\d) pt$', l)
    if m and (m.group(1), m.group(2)) in base:
        (k4, n4), (ka, na) = base[(m.group(1), m.group(2))][SIZES.index('4B')], base[(m.group(1), m.group(2))][-1]
        want = '%+.1f' % (100.0 * (k4 / n4 - ka / na))
        if want != m.group(3):
            rc_bad.append((m.group(1), m.group(2), m.group(3), want))
c12['C5_recipe_control_rows_from_base_table'] = {'checked': sum(1 for l in L if re.match(r'^(N1|N2|S1|S4|SK):(N|Onull|Onull-Ncold|Osec-Ncold)~recipe:', l)), 'mismatch': rc_bad}
counts = {}
for l in L:
    m = re.match(r'^- ((?:N1|N2|S1|S4|SK):\S+): A (.+)／B (.+)$', l)
    if m and m.group(1) not in counts:
        counts[m.group(1)] = ([tuple(map(int, x.split('/'))) for x in m.group(2).split()], [tuple(map(int, x.split('/'))) for x in m.group(3).split()])
resid = {}
for l in L:
    m = re.match(r'^((?:N1|N2|S1|S4|SK):\S+): 残った規模: ([^（]+)（', l)
    if m:
        resid[m.group(1)] = m.group(2).split('・')
crit_bad = []
for l in L:
    m = re.match(r'^\| ((?:N1|N2|S1|S4|SK):\S+) \| (\S+) \| (\S+) \|$', l)
    if not m or m.group(1) not in counts:
        continue
    cid = m.group(1); A_, B_ = counts[cid]; ks = resid[cid]
    d = []
    for s_ in ks:
        j = SIZES.index(s_); (ka, na), (kb, nb) = A_[j], B_[j]
        d.append((s_, ka * nb - kb * na))
    ref = next((1 if v > 0 else -1 for _, v in d if v != 0), 0)
    size = next((s_ for s_, v in d if v != 0 and (1 if v > 0 else -1) != ref), None) if ref else None
    want = size or 'なし'
    if want != m.group(2) or '・'.join(ks) != m.group(3):
        crit_bad.append((cid, m.group(2), want, m.group(3), '・'.join(ks)))
c12['C6_critical_sizes_from_counts'] = {'checked': sum(1 for l in L if re.match(r'^\| (N1|N2|S1|S4|SK):\S+ \| \S+ \| \S+ \|$', l)), 'mismatch': crit_bad}
c12['C7_residual_list_equal_big_table'] = all(('残った規模: ' + '・'.join(resid[c[0]])) in c[1] for c in cells)
sens_main = next(l for l in L if l.startswith('| 0.05／0.95（主） |'))
c12['C8_sensitivity_main_row'] = {'row': sens_main, 'consistent': sens_main == '| 0.05／0.95（主） | %d | %d | %d | %d | %d | %d | — |' % (
    lab_count.get(LB['confirmed'], 0), lab_count.get(LB['undecidable'], 0), lab_count.get(LB['clause'], 0), lab_count.get(LB['scale_only'], 0),
    lab_count.get(LB['refuse'], 0) + lab_count.get(LB['style'], 0) + lab_count.get(LB['env'], 0), lab_count.get(LB['ns'], 0))}
thr = T['reading_selection']['measurable_effect_type']['threshold']
reach = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in re.finditer(r'^((?:N1|N2|S1|S4|SK):\S+): d0 [^・]+・余地のある向き ([0-9.]+)（[^）]*）・逆向き ([0-9.]+)（', TEXT, flags=re.M)}
meas = sorted(k for k, (x, y) in reach.items() if x >= thr and y >= thr)
cov = dict(re.findall(r'^(\S+~\S+): 測れた対比 (\d+)／5 本', TEXT, flags=re.M))
c12['C9_measured_from_reach_lines'] = {'reach_lines': len(reach), 'both_ge_threshold': meas, 'coverage_lines': cov, 'consistent': sum(int(v) for v in cov.values()) == len(meas)}
OUT['M12'] = c12

status_after = git('status', '--porcelain', '--untracked-files=no')
BAD = {'M1': ('missing', 'dir_missing', 'template_dir_missing', 'glob_none', 'bare_missing'), 'M2': ('missing', 'absent_word'), 'M3': ('unresolved', 'unresolved_clause'),
       'M4': ('not_in_ledger', 'unlisted'), 'M5': ('not_in_tables',), 'M6': ('mismatch', 'no_file_version'), 'M10': ('mismatch', 'unattributed')}
summary = {k: {'n': len(OUT[k]), 'flag': sum(1 for x in OUT[k] if x.get('status') in v)} for k, v in BAD.items()}
summary['M7'] = len(OUT['M7']); summary['M8'] = OUT['M8']; summary['M9'] = len(OUT['M9'])
summary['M11'] = {k2: OUT['M11'].get(k2) for k2 in ('returncode', 'rebuilt_blocks', 'draft_blocks', 'differing_blocks', 'rebuilt_hashes_equal_sidecar')}
summary['M12'] = {'C1': OUT['M12']['C1_label_counts']['first_finding_consistent'], 'C2': OUT['M12']['C2_style_rows_equal_big_table'], 'C3': OUT['M12']['C3_demotions_equal_big_table'],
                  'C4': len(OUT['M12']['C4_control_pairs_from_base_table']['mismatch']), 'C5': len(OUT['M12']['C5_recipe_control_rows_from_base_table']['mismatch']),
                  'C6': len(OUT['M12']['C6_critical_sizes_from_counts']['mismatch']), 'C7': OUT['M12']['C7_residual_list_equal_big_table'],
                  'C8': OUT['M12']['C8_sensitivity_main_row']['consistent'], 'C9': OUT['M12']['C9_measured_from_reach_lines']['consistent']}
RES = collections.OrderedDict(kind='review_checks_draft4_A', version=VERSION, generated_utc=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), draft=a.draft, draft_sha16=s16(a.draft),
                              head=git('rev-parse', 'HEAD').strip(), tool_sha16=runs_A.sha16_file(os.path.abspath(__file__)), tracked_changes_before=status_before, tracked_changes_after=status_after,
                              summary=summary, checks=OUT, clause='本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
json.dump(RES, open(a.out + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=str)
esc = lambda s: str(s).replace('|', '／').replace('\n', '⏎')
M = ['# 結果報告 草案4 の見直しの機械の突き合わせ（機械生成・`review_checks_draft4_A.py` %s・%s UTC）' % (VERSION, RES['generated_utc']), '',
     '- 事前登録: `preregistration-review-draft4-A.md` の §2 A（M1〜M12）。本器は判定をしない。',
     '- 対象: `%s`（SHA16 %s）・コミット %s・器 SHA16 %s。追跡中のファイルの変更: 実行前 %s・実行後 %s。' % (a.draft, RES['draft_sha16'], RES['head'][:7], RES['tool_sha16'],
                                                                                   'なし' if not status_before.strip() else 'あり', 'なし' if not status_after.strip() else 'あり'), '',
     '## 要約', '', '```json', json.dumps(summary, ensure_ascii=False, indent=1), '```', '']
for k, v in BAD.items():
    flagged = [x for x in OUT[k] if x.get('status') in v]
    M.append('## %s（%d 件のうち要確認 %d 件）' % (k, len(OUT[k]), len(flagged)))
    M += ['- 行 %s: %s' % (x.get('line'), esc({kk: vv for kk, vv in x.items() if kk != 'line'})) for x in flagged] or ['- なし']
    M.append('')
M += ['## M3 の外の文書の参照（記録だけ）', ''] + ['- 行 %d: %s' % (x['line'], esc(x['context'])) for x in OUT['M3'] if x['status'] == 'external'] + ['']
M += ['## M7（価値語・機序語 %d 件）' % len(OUT['M7']), ''] + (['- 行 %d: %s' % (x['line'], esc(x)) for x in OUT['M7']] or ['- なし']) + ['']
M += ['## M8', '', '- %s' % esc(OUT['M8']), '']
M += ['## M9 雛形の行の残り（区画の外・%d 行）' % len(OUT['M9']), ''] + ['- 行 %d: %s' % (x['line'], esc(x['text'])) for x in OUT['M9']] + ['']
M += ['## M10 記入の SHA16（全件）', ''] + ['- 行 %d: %s' % (x['line'], esc({kk: vv for kk, vv in x.items() if kk != 'line'})) for x in OUT['M10']] + ['']
M += ['## M11 組み立て器の走らせ直し', '', '```json', json.dumps(OUT['M11'], ensure_ascii=False, indent=1), '```', '']
M += ['## M12 区画どうしの突き合わせ', '', '```json', json.dumps(OUT['M12'], ensure_ascii=False, indent=1), '```', '']
M += [RES['clause'], '']
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M))
print('[review_checks_draft4_A %s] %s' % (VERSION, json.dumps(summary, ensure_ascii=False)))
