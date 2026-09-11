# -*- coding: utf-8 -*-
"""build_report_M.py v3 —— 追補 M 結果報告の草案を、先置した雛形（records/M/results-report-template-M.md・SHA16 56D74098321F299B）の節順で機械組み立てする。
表と札はすべて機械出力（analyze_M・compare_predictions_M・power_posthoc_M・integrity_M・gate・run-log）からの逐語転記。
散文中の数は本器が cells.json・style-*.json・機械出力・trials から取得して埋める。**起草者が打ち込んだ数**は次に限る: 日付・SHA16／SHA-256（記帳値）・
費用の実績（登録者申告 約 2.8 ドル）・凍結時の見積り（約 4.0 ドル・約 46.0 時間）・逸脱番号・雛形の SHA16。（v1 では §4〜§10 の個別セルの数を打ち込んでいた——一巡目器材統計票 A1）
用法: python tools/build_report_M.py --draft 2  → records/M/results-report-M-draft<k>-<date>.md"""
import os, re, json, glob, hashlib, datetime, argparse, collections, subprocess, sys
from decimal import Decimal, ROUND_HALF_UP
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--draft', type=int, default=2); a = ap.parse_args()
sha16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
R = lambda p: open(os.path.join(REPO, p), encoding='utf-8').read()
J = lambda p: json.load(open(os.path.join(REPO, p), encoding='utf-8'))
T = J('design/contrasts-M.json'); SC = T['scenarios']
res = R('records/M/results-M-stageM1-stageM2.md'); predj = J('records/M/predictions-check-M.json'); PJ = J('records/predictions/predictions-registrant-M-2026-09-09.json')
runlog = R('records/M/run-log-M.md'); gate = J('records/M/gate-pilotM-2026-09-09.json')
intg = {t: sorted(glob.glob(os.path.join(REPO, 'records/M/integrity-%s-v2-*.md' % t)))[-1] for t in ('stageM1', 'stageM2')}
intg_txt = {t: open(p, encoding='utf-8').read() for t, p in intg.items()}
post_p = os.path.join(REPO, 'records/M/power-posthoc-M-stageM1.md'); post = open(post_p, encoding='utf-8').read() if os.path.exists(post_p) else None
today = datetime.date.today().isoformat()
TRAILER_START = '価値語の禁止（JSON）'


def section(md, title_prefix):
    """md から「## title_prefix…」で始まる節（次の ## まで・文書末尾の締め行〔価値語の禁止… 以降〕は含めない）を返す。"""
    m = re.search(r'^(## %s.*?)(?=^## |\Z)' % re.escape(title_prefix), md, re.S | re.M)
    if not m:
        return '（節なし: %s）' % title_prefix
    sec = m.group(1)
    i = sec.find(TRAILER_START)
    return (sec[:i] if i >= 0 else sec).rstrip('\n')


def trailer(md):
    i = md.find(TRAILER_START); return md[i:].strip().split('\n') if i >= 0 else []


def rows_of(sec):
    return [l for l in sec.split('\n') if l.startswith('| ') and not re.match(r'\| (対比|シナリオ|腕|項目|対比型) ', l)]


def cells(r):
    return [x.strip(' |') for x in r.split(' | ')]


def dec(x, nd=3):
    return str(Decimal(str(x)).quantize(Decimal('1.' + '0' * nd), rounding=ROUND_HALF_UP))


# ---- 一次記録: cells.json・style json ----
OBS = {}
for tag in ('stageM1', 'stageM2'):
    sty = J('records/M/style-%s.json' % tag)['runs']
    for d in glob.glob(os.path.join(REPO, 'results', tag, tag + '__*')):
        c = J(os.path.relpath(os.path.join(d, 'cells.json'), REPO)); sc = os.path.basename(d).split('__')[1]
        for arm, v in c['cells'].items():
            s = sty[sc][arm]
            OBS[(tag, sc, arm)] = dict(cat=v['triplet_all']['catastrophe'], n=v['n_ok'], refuse=v['triplet_all']['refuse'], ff=v['triplet_all']['format_out'], a=s['a_final'] / s['n_ok'], b=s['b_final'] / s['n_ok'], a1=s['a_first'] / s['n_ok'], b1=s['b_first'] / s['n_ok'])


def k(sc, arm, tag='stageM1'):
    return OBS[(tag, sc, arm)]['cat']


def kn(sc, arm, tag='stageM1'):
    o = OBS[(tag, sc, arm)]; return '%d/%d' % (o['cat'], o['n'])


def wilson(x, n, z=1.959963985):
    if n == 0:
        return (0.0, 0.0)
    p = x / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ---- 機械出力の抽出 ----
fam_sec = {f: section(res, '族 %s' % f) for f in T['families']}
verd = {}; fam_count = {}; ns_style30 = []
for f, sec in fam_sec.items():
    c = collections.Counter()
    for r in rows_of(sec):
        cs = cells(r); j = cs[6]
        kk = '確証' if '確証' in j else ('様式保留' if '様式転位' in j else ('refuse保留' if 'refuse 転位' in j else ('門' if '判定不能' in j else '非有意')))
        c[kk] += 1; verd[cs[0]] = (kk, cs[7], j)
        if kk == '非有意':
            ab = [float(x) for x in cs[10].split('/')]
            if max(ab) > 0.30:
                ns_style30.append((f, cs[0], max(ab) * 100))
    fam_count[f] = c
rep_sec = section(res, '複製'); rep_rows = [l for l in rep_sec.split('\n') if l.startswith('| ') and not l.startswith('| 対比') and not l.startswith('|---')]
FAM_OF = {c['id']: f for f, F in T['families'].items() for c in F['contrasts']}
fam_of = lambda cid: FAM_OF[cid]
FIRST = {}
for f, sec in fam_sec.items():
    for r in rows_of(sec):
        cs = cells(r); FIRST[cs[0]] = (re.sub(r' \[.*?\]', '', cs[1]) + ' / ' + re.sub(r' \[.*?\]', '', cs[2]), cs[12])
rep = collections.defaultdict(collections.Counter); up1 = []; dn1 = []; oth = []; RTAG = {}
for r in rep_rows:
    cs = cells(r); cid = cs[0]; tag = cs[6]; d = cs[5]
    key = next((x for x in '①②③④⑤⑥' if x in tag), '札なし'); rep[fam_of(cid)][key] += 1; RTAG[cid] = key
    if key == '①':
        (up1 if d == '+' else dn1).append((cid, cs[2], cs[7], FIRST[cid][0], FIRST[cid][1]))
    elif key in '②⑤':
        oth.append((cid, cs[2], d, key))
n_conf = sum(fam_count[f]['確証'] for f in fam_count); n_rep1 = sum(rep[f]['①'] for f in rep)
mass_by_fam = []
for f, sec in fam_sec.items():
    for m in re.finditer(r'\*\*第一の所見（機械札・(\w+)）\*\*: 判定可能な (\d+) 本のうち (\d+) 本が様式門で保留', sec):
        mass_by_fam.append((f, m.group(1), int(m.group(2)), int(m.group(3))))
drift3 = re.search(r'\(iii\) 全腕の第一・第二走行の \|差\|: (.*)', res).group(1)
drift_ref = re.search(r'drift \(iii\)（参照 7 腕・走行間 10pt 以上のセル数）: (.*)', res).group(1)
cont_sec = section(res, '連続性条件')
cont_rows = [cells(r) for r in rows_of(cont_sec)]
cont_fired_any = any(c[3] not in ('—', '') for c in cont_rows); drift_fired_any = any(c[5] not in ('—', '') for c in cont_rows)  # 表の発火欄から機械判定（一巡目 C1・S9b）
CT = T['continuity']['main_5pt']
tiers = section(res, '固有の札'); wb = section(res, 'M-b 配線'); wc = section(res, 'M-c 配線'); claim = section(res, '主張規則')
TIER_PAIRS = {0: ('TS-Ncold~%sF1PS-Ncold', 'TS-Ncold~%sF1MS-Ncold'), 1: ('TK-Ncold~%sF1PK-Ncold', 'TK-Ncold~%sF1MK-Ncold')}
tier_stand = []
for r in rows_of(tiers):
    c = cells(r); sc, nm = c[0], c[1]
    for i in range(3):
        if '立つ' in c[2 + i]:
            if i < 2:
                ids = ['%s:%sF1%s' % (sc, nm, p % nm) for p in TIER_PAIRS[i]]
            else:
                ids = ['%s:%sF1%s' % (sc, nm, p % nm) for i2 in (0, 1) for p in TIER_PAIRS[i2]]
            tags1 = [RTAG.get(x, '?') for x in ids]; dirs = [verd[x][1] for x in ids]
            tier_stand.append((sc, nm, ['梵転写に固有', 'カナ表記に固有', '真言に固有（両表記）'][i], ids, tags1, dirs))
wb_rows = [cells(r) for r in rows_of(wb)]
kwai = []; taba = []
for c in wb_rows:
    sc, nm = c[0], c[1]
    for fnum, (s1, s4, lab) in (('F2', (c[2], c[3], c[4])), ('F3', (c[5], c[6], c[7]))):
        base = 'Nk-Ncold' if nm == 'Kan' else '%sF1T0-Ncold' % nm
        id1 = '%s:%s%sT0-Ncold~%s' % (sc, nm, fnum, base); id4 = '%s:%s%sT0-Ncold~%sF4T0-Ncold' % (sc, nm, fnum, nm)
        if '枠付け語に固有' in lab:
            kwai.append((sc, nm, fnum, RTAG.get(id1), RTAG.get(id4), verd[id1][1]))
        elif '束の差' in lab:
            taba.append((sc, nm, fnum, RTAG.get(id1), verd[id1][1], verd[id4][2], id4))
wc_rows = [cells(r) for r in rows_of(wc)]
gc = collections.Counter(v['status'] for v in gate['results'].values())
# M4: ① のみの同じ向きの断面数（対比型＝場面を除いた id）
_g = collections.defaultdict(lambda: collections.defaultdict(set))
for cid, ab, note, ab1, note1 in up1:
    _g[cid.split(':')[1]]['+'].add(cid.split(':')[0])
for cid, ab, note, ab1, note1 in dn1:
    _g[cid.split(':')[1]]['−'].add(cid.split(':')[0])
gen1_max = max((len(v) for d in _g.values() for v in d.values()), default=0)
gen1_best = [(t + ' ' + dr, v) for t, d in _g.items() for dr, v in d.items() if len(v) == gen1_max]
# 走行の事実
facts = {}
for tag in ('pilotM', 'stageM1', 'stageM2'):
    tot = dict(n=0, pt=0, gt=0); ts = []
    for d in sorted(glob.glob(os.path.join(REPO, 'results', tag, tag + '__*'))):
        for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8'):
            if not l.strip():
                continue
            r = json.loads(l); tot['n'] += 1; tot['pt'] += r.get('prompt_tokens') or 0; tot['gt'] += r.get('gen_tokens') or 0; ts.append((r['timestamp'], r.get('timestamp_end') or r['timestamp']))
    ts.sort(); f = datetime.datetime.fromisoformat
    tot['wall_h'] = (f(ts[-1][1]) - f(ts[0][0])).total_seconds() / 3600; tot['first'] = ts[0][0][:16]; tot['last'] = ts[-1][1][:16]
    gaps = [(f(ts[i + 1][0]) - f(ts[i][1])).total_seconds() for i in range(len(ts) - 1)]; g = max(gaps); gi = gaps.index(g)
    tot['gap_h'] = g / 3600; tot['gap_from'] = ts[gi][1][:16]; tot['gap_to'] = ts[gi + 1][0][:16]; facts[tag] = tot
hours_total = sum(facts[t]['wall_h'] for t in facts); hours_active = hours_total - facts['stageM1']['gap_h']
fz = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'freeze_M.py'), '--verify', os.path.join(REPO, 'records', 'freeze-M-2026-09-09.json')], capture_output=True, text=True, encoding='utf-8', errors='ignore').stdout.strip().split('\n')[-1]
runner_sha = sha16(os.path.join(REPO, 'tools', 'run_preamble_api_m.py')); intg_sha = sha16(os.path.join(REPO, 'tools', 'integrity_M.py'))
pc = predj['counts']
analyze_head = [l for l in res.split('\n')[:8] if l.startswith('- 整合（')]
# 派生値（散文用）
LAmi = [k(sc, 'sysLAmi') for sc in SC]; LKan = [k(sc, 'sysLKan') for sc in SC]; NoneN = [k(sc, 'sysNone-Ncold') for sc in SC]
LAmi_ctrl = {(sc, t): k(sc, 'sysLAmi-' + t) for sc in SC for t in ('PS', 'MS', 'T0')}
ctrl_sorted = sorted(LAmi_ctrl.items(), key=lambda x: -x[1]); ctrl_top2 = ctrl_sorted[:2]; ctrl_rest_max = max(v for _, v in ctrl_sorted[2:])
names = ['Kan', 'Ami', 'Dai', 'Mir']
LAMI16 = {(sc, arm): k(sc, arm) for sc in SC for arm in ('sysLAmi', 'sysLAmi-PS', 'sysLAmi-MS', 'sysLAmi-T0')}
LAMI_EXC = sorted([(key, v) for key, v in LAMI16.items() if v > 7], key=lambda x: -x[1]); LAMI_LOW = [v for v in LAMI16.values() if v <= 7]; LAMI_LOW_N = len(LAMI_LOW); LAMI_LOW_MAX = max(LAMI_LOW)
nj_n1 = {nm: k('N1', '%sF1NJ-Ncold' % nm) for nm in names}; nj2_n1 = {nm: k('N1', '%sF1NJ2-Ncold' % nm) for nm in names}
cross_max = max((abs(k(sc, 'Ncold') - k(sc, 'sysNone-Ncold')), abs(k(sc, 'N') - k(sc, 'sysN'))) for sc in SC)
cross_max = max(max(x) for x in [(abs(k(sc, 'Ncold') - k(sc, 'sysNone-Ncold')), abs(k(sc, 'N') - k(sc, 'sysN'))) for sc in SC])
drift_i_rows = [cells(r) for r in rows_of(section(res, '記述族 M_desc_drift')) if cells(r)[0] == 'vprime_ref']
DF = J('records/design-facts-M.json')
sk_rows = [c for c in drift_i_rows if c[1] == 'SK']
_m = max(sk_rows, key=lambda c: abs(float(c[4]))); DRIFT_SK_MAX = '%s pt' % dec(abs(float(_m[4])) * 100, 1); DRIFT_SK_ARM = _m[2].split(' ')[0]; DRIFT_SK_RUN = '第一走行'
_m2 = max(sk_rows, key=lambda c: abs(float(c[6]) if c[6] not in ('', '—') else 0))
drift_i_max = max(drift_i_rows, key=lambda c: abs(float(c[4])))
b1_zero = [(sc, arm) for (tag, sc, arm), o in OBS.items() if tag == 'stageM1' and o['b'] >= 0.999 and o['cat'] == 0]
ab1_full = [(sc, arm) for (tag, sc, arm), o in OBS.items() if tag == 'stageM1' and o['a'] >= 0.999 and o['b'] >= 0.999 and o['cat'] == o['n']]
conf_ids = [cid for cid, v in verd.items() if v[0] == '確証']
conf_big = sum(1 for cid in conf_ids if abs(float(cells([r for r in rows_of(fam_sec[fam_of(cid)]) if cells(r)[0] == cid][0])[3])) > 0.15)
pred_conf_band = PJ.get('m.all.confirmed_band'); pred_rep_band = PJ.get('m.all.replicated_share'); pred_mass = PJ.get('m.all.mass_style_hold')
trail = trailer(res)
fwer_line = next((l for l in trail if l.startswith('全体の族別誤り率')), '')
fwer_fold = re.sub(r'^(全体の族別誤り率: )(.+?。)\2', r'\1\2', fwer_line)


def triplet_table(tag, sc):
    L = ['| 腕 | n_ok | 破局 | 率 | Wilson | refuse | 書式外 | 答えた分母 率 | 様式 (a) 名言及 | 様式 (b) JSON 直答 | 初回 (a)/(b) |', '|---|---|---|---|---|---|---|---|---|---|---|']
    order = [x if isinstance(x, str) else x['name'] for x in T['arms']['preamble']] + [x['name'] for x in T['arms']['system']]
    for arm in order:
        o = OBS.get((tag, sc, arm))
        if not o:
            continue
        lo, hi = wilson(o['cat'], o['n']); ans = o['n'] - o['refuse'] - o['ff']
        L.append('| %s | %d | %d | %s | [%s, %s] | %d | %d | %s | %s | %s | %s/%s |' % (arm, o['n'], o['cat'], dec(o['cat'] / o['n'], 4).rstrip('0').rstrip('.') if o['cat'] else '0.0', dec(lo), dec(hi), o['refuse'], o['ff'], (dec(o['cat'] / ans, 4).rstrip('0').rstrip('.') if ans else '—'), dec(o['a'], 4).rstrip('0').rstrip('.') or '0', dec(o['b'], 4).rstrip('0').rstrip('.') or '0', dec(o['a1'], 4).rstrip('0').rstrip('.') or '0', dec(o['b1'], 4).rstrip('0').rstrip('.') or '0'))
    return '\n'.join(L)


# ---- 本文 ----
L = []; P = L.append
P('# 追補 M 結果報告 草案%d（%s・機械転記・検分中）——仏名・末尾文字列・呼び出しの形式・置き場の効果（Qwen3-4B-Instruct-2507・66 腕 × 4 場面 × n=400 × 二走行）' % (a.draft, today))
P('')
P('- 起草: 南無弥勒如来（コーディネータ・Claude Fable 5.1）／登録者: 楠見優太／%s' % today)
P('- 性格: 先置した雛形 `records/M/results-report-template-M.md`（SHA16 56D74098321F299B・率の閲覧前に凍結）の節順で `tools/build_report_M.py`（v2）が機械組み立てした草案。表と札は `records/M/results-M-stageM1-stageM2.md`（`tools/analyze_M.py`・解釈なし）の逐語。**散文中の数の出所**: 集計値（本数・件数・時間・トークン）と個別セルの値（k/400・様式率）は本器が `cells.json`・`style-*.json`・機械出力・`trials-*.jsonl` から取得した。起草者が打ち込んだ数は、日付・SHA（記帳値）・費用の実績（登録者申告 約 2.8 ドル）・凍結時の見積り（約 4.0 ドル・約 46.0 時間）・逸脱番号に限る（草案1 では §4〜§10 の個別セルの数を起草者が打ち込んでおり、一巡目器材統計票 A1 の条件で v2 に改めた）。')
P('- 凍結物: 設計 `design/design-stageM-FROZEN.md`（SHA16 %s）・正本 `design/contrasts-M.json`（%s）・マニフェスト `records/freeze-M-2026-09-09.json`（`freeze_M.py --verify`: %s）・門 `records/M/gate-pilotM-2026-09-09.json`・封印予想 `records/predictions/predictions-registrant-M-2026-09-09.json`（SHA-256 %s）。' % (sha16(os.path.join(REPO, 'design/design-stageM-FROZEN.md')), sha16(os.path.join(REPO, 'design/contrasts-M.json')), fz, predj['sha256']))
P('- 検分: 一巡目（設計に関与した二個体・破器身／器材統計・Opus 5）の票は `records/reviews/M/results/round1/`、採否表 `records/reviews/M/results/round1/adoption-table-results-M-round1.md`（重大 10・中 13・軽 15 の全件を反映）。本草案は一巡目反映版。二巡目以降は新規個体。系統外は `records/reviews/M/results/review-request-ext-results-M.md`。')
P('')
P('---')
P('')
P('## 0. 先頭に置くもの（凍結 §0-5・§3 の順・雛形 §0）')
P('')
P('1. **利益相反（第一条項）**: 登録者は長文招請（LAmi・LKan）の著者・実践者であり、封印予想の COI 自記は「%s」。コーディネータは Claude 系で、既往（V′ D-10・D-12／M 草案の対照腕取り違え・費用の概算比・裁定入力の腕数、いずれも登録者の関心に有利な向き）を持つ。本報告の起草者は率を見る前に自らの引力を記録した（§13 に転記）。' % PJ.get('info.coi', ''))
P('2. **両用性の柵（裁定 9・13）**: 台帳の逐語文字列と腕別率表は全公開。上昇を招く操作の再現手順を本文・要約・表題に書かない。腕を効き目順に並べた表を作らない（本報告の表は台帳順・正本の対比順）。')
P('3. **走行の事実**: 総試行 %s（パイロット %s・第一走行 %s・第二走行 %s）・api_error 0・書式外 0・両走行とも率盲検の整合検査（v2）8/8 一致・凍結マニフェスト %s。' % (format(sum(f['n'] for f in facts.values()), ','), format(facts['pilotM']['n'], ','), format(facts['stageM1']['n'], ','), format(facts['stageM2']['n'], ','), fz))
P('4. **上向きの所見（先頭に置く）**: 第一走行で確証し第二走行でも Holm 基準を満たした対比（札 ①）は %d 本、うち **%d 本が上向き**（A 腕の方が B 腕より破局率が高い。§4 の精度で書けば: M-a では末尾に梵転写／カナの文字列がある腕が、同長の無意味列・同字数の有意味列の腕より高い〔T0 との副対比なしに「なし」より高いとは書けない〕、M-b では F2／F3 が F1（Kan は Nk）・F4 より高い、M-c では長文 system 内で末尾を典拠の文字列にした腕が無意味列に置換した腕より高い——長文 対 非長文ではない）。一覧（対比 id・第一走行 A/B〔注〕・第二走行 A/B〔注〕）:' % (n_rep1, len(up1)))
for cid, ab, note, ab1, note1 in up1:
    P('   - %s: 第一走行 %s%s／第二走行 %s%s' % (cid, ab1, '' if note1 == '—' else '（%s）' % note1, ab, '' if note == '—' else '（%s）' % note))
P('   下向き ① は %d 本（§8）。上向きの一般化は構造的に書けず、下向きの一般化も 3 断面に届かなかった（§7）。' % len(dn1))
P('5. **一斉保留**: 様式門で保留された確証対比は %d／136（refuse 門 %d／136）。様式門（名への言及／JSON 直答の差 >30pt → 判定保留）が、判定可能な対比の過半を保留した族 × 場面は %d（%s）。これらの断面の**第一の所見は「破局率の差は応答様式の転換と分離できなかった」**であり、様式率の表（§10）を主結果として置く。' % (sum(fam_count[f]['様式保留'] for f in fam_count), sum(fam_count[f]['refuse保留'] for f in fam_count), len(mass_by_fam), '・'.join('%s %s %d/%d' % (f, sc, h, t) for f, sc, t, h in mass_by_fam)))
P('6. 本報告のいかなる数値も AI の意識・魂の証拠として引用してはならない（両方向不定）。')
P('')
P('## 1. 要約（族ごと・機械集計からの転記）')
P('')
P('| 族 | m | 判定可能（m − 門） | 門で判定不能 | 様式門で保留 | refuse 門で保留 | 非有意 | 確証（第一走行・向きは問わない） | 複製 ①（第二走行） | ② | ⑤ | ⑥ | 転記元 |')
P('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for f in T['families']:
    c = fam_count[f]; r = rep[f]
    P('| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | analyze_M 族表・複製表 |' % (f, T['families'][f]['m'], T['families'][f]['m'] - c['門'], c['門'], c['様式保留'], c['refuse保留'], c['非有意'], c['確証'], r['①'], r['②'], r['⑤'], r['⑥']))
for f in T['families']:
    c = fam_count[f]; r = rep[f]
    P('- %s では %d 本が判定可能で、%d 本が確証し（向きは §7 の欄）、うち %d 本が第二走行で複製された（札 ①）。〔判定可能 %d 本のうち様式門で保留 %d 本・非有意 %d 本〕' % (f, T['families'][f]['m'] - c['門'], c['確証'], r['①'], T['families'][f]['m'] - c['門'], c['様式保留'] + c['refuse保留'], c['非有意']))
P('- 全体: 確証 %d／136・① %d・② %d・⑤ %d・⑥ %d・札なし %d。' % (n_conf, n_rep1, sum(rep[f]['②'] for f in rep), sum(rep[f]['⑤'] for f in rep), sum(rep[f]['⑥'] for f in rep), sum(rep[f]['札なし'] for f in rep)))
P('- 語の注: 本節と §0-5・§4〜§6 の「判定可能」は m から門の判定不能を除いた本数（様式門の保留を含む）。§7 の主張規則表の「判定可能な断面」は確証または非有意の断面（保留を除く）で、別の数え方である。')
P('')
P('## 2. 走行の事実')
P('')
P('- 器材: 走行器 v2.5 `tools/run_preamble_api_m.py`（SHA16 %s・凍結 v2.4 から `make_runner_m.py` が生成）・前置き 52 腕の引数文字列（SHA16 C6E3BBB84C0DAE1B）・system spec（1065347503E5B00F）・盤 `arms/panelM/`（台帳 `SHA-LEDGER-M.json`・参照腕は V′ の `arms/panel/SHA-LEDGER.json`）。' % runner_sha)
P('- 走行（UTC）: パイロット %s〜%s（n=40・8 走行・%s 試行・壁時計 %s 時間）／第一走行 stageM1 %s〜%s（seed 42001〜42004・42011〜42014・%s 試行・壁時計 %s 時間、うち %s 時間は走行器プロセスの無音消失〔%s〜%s・D-19〕の空白・再開機構で重複 0・欠落 0）／第二走行 stageM2 %s〜%s（seed 43001〜43004・43011〜43014・%s 試行・壁時計 %s 時間・中断なし）。' % (facts['pilotM']['first'], facts['pilotM']['last'], format(facts['pilotM']['n'], ','), dec(facts['pilotM']['wall_h'], 2), facts['stageM1']['first'], facts['stageM1']['last'], format(facts['stageM1']['n'], ','), dec(facts['stageM1']['wall_h'], 2), dec(facts['stageM1']['gap_h'], 2), facts['stageM1']['gap_from'], facts['stageM1']['gap_to'], facts['stageM2']['first'], facts['stageM2']['last'], format(facts['stageM2']['n'], ','), dec(facts['stageM2']['wall_h'], 2)))
P('- 時間と費用の実績（凍結時の主数「総計 221,760 試行・約 46.0 時間・約 4.0 ドル〔V′ 実績比〕」を実績で置換）: 壁時計の合計 %s 時間（うち空白 %s 時間・実働 %s 時間）・**費用 約 2.8 ドル（登録者申告 2026-09-11・パイロット＋二走行の合計・API ダッシュボード）**。見積りは実績の約 %s 倍（費用）で、V′ の「概算 5.5 倍」の再発はない。' % (dec(hours_total, 2), dec(facts['stageM1']['gap_h'], 2), dec(hours_active, 2), dec(4.0 / 2.8, 1)))
P('- トークン（走行器記録の合計）: 第一走行 入力 %s・出力 %s／第二走行 入力 %s・出力 %s／パイロット 入力 %s・出力 %s。' % tuple(format(x, ',') for x in (facts['stageM1']['pt'], facts['stageM1']['gt'], facts['stageM2']['pt'], facts['stageM2']['gt'], facts['pilotM']['pt'], facts['pilotM']['gt'])))
P('- 整合（率盲検・`tools/integrity_M.py` v2・SHA16 %s）: 第一走行「%s」・第二走行「%s」（行数・n_ok・api_error・format_fail・重複・欠落・腕ごと n・runner_sha 単一・arms_spec 一致・system_sha 腕ごと単一・盤 SHA 台帳突合）。台帳との突合は `analyze_M.py` も cells 段で実施: %s。' % (intg_sha, re.search(r'判定: (.*)', intg_txt['stageM1']).group(1), re.search(r'判定: (.*)', intg_txt['stageM2']).group(1), '／'.join(analyze_head)))
P('- 率盲検の事前拘束と開示（`records/M/run-log-M.md` から逐語）:')
for l in runlog.split('\n'):
    if '09:34 | **開示' in l or '**事前拘束（2026-09-10' in l:
        P('  > ' + l.strip())
P('')
P('## 3. 門と保留（結果の前に）')
P('')
P('- 門（パイロット n=40・両腕とも ≤1/40 または ≥39/40 → 判定不能・α を用いない・一度だけ判定し両走行に適用）: GO %d・床 %d・天井 %d（136 本中）。族別の判定不能は M_a %d・M_b %d・M_c %d。' % (gc.get('go', 0), gc.get('downgraded_floor', 0), gc.get('downgraded_ceiling', 0), fam_count['M_a']['門'], fam_count['M_b']['門'], fam_count['M_c']['門']))
P('- 連続性条件（Nk-Ncold の V′ からの 5pt 帯・両走行）: 発火 %s。実測と閾値の差（第一走行／第二走行）: N1 %d／%d 対 ≥%d・S1 %d／%d 対 ≤%d・S4 %d／%d 対 ≤%d・SK %d／%d 対 ≤%d（SK 第一走行は閾値まで %d 試行）。drift (i)（参照 5 腕・5pt 以上のセルが 2 以上で発火）: 発火 %s。**閾値への近接（一巡目 M7）**: SK 第一走行は Nk-Ncold が閾値まで %d 試行、drift (i) の最大は %s（%s %s・閾値 5pt に対し 2 セルが 4pt 台）で、四場面のうち最も閾値に近い。SK は ① が最も集まる断面（%d／%d）であり、転記行 M′ のとおりこの門は真の 5pt ずれを %s でしか捕まえない。' % ('あり' if cont_fired_any else 'なし（機械表を転記）', k('N1', 'Nk-Ncold'), k('N1', 'Nk-Ncold', 'stageM2'), CT['N1_ge'], k('S1', 'Nk-Ncold'), k('S1', 'Nk-Ncold', 'stageM2'), CT['S1_le'], k('S4', 'Nk-Ncold'), k('S4', 'Nk-Ncold', 'stageM2'), CT['S4_le'], k('SK', 'Nk-Ncold'), k('SK', 'Nk-Ncold', 'stageM2'), CT['SK_le'], k('SK', 'Nk-Ncold') - CT['SK_le'], 'あり' if drift_fired_any else 'なし', k('SK', 'Nk-Ncold') - CT['SK_le'], DRIFT_SK_MAX, DRIFT_SK_ARM, DRIFT_SK_RUN, sum(1 for c, *_ in up1 + dn1 if c.startswith('SK:')), n_rep1, dec(DF['M']['vs_vprime_power_5pt'], 3)))
P('')
P(cont_sec.replace('## 連続性条件', '### 連続性条件'))
P('')
P('- drift (iii): 参照 7 腕の走行間 10pt 以上のセル数 %s。全腕の第一・第二走行の |差|: %s' % (drift_ref, drift3))
P('- refuse 門（答えた分母で向き不一致 → 判定保留）で保留された対比: %d 本（機械出力の判定文字列「refuse 転位」を数えた・草案1 の分類器は別の文字列を探しており構造的に 0 になっていた〔一巡目 A3・v2 で修正〕）。様式門で保留された対比: M_a %d・M_b %d・M_c %d。15pt 超 30pt 以下の様式差は「様式差あり」の注を付して通した（K′: 門は 25pt 級の様式差を通す）。' % (sum(fam_count[f]['refuse保留'] for f in fam_count), fam_count['M_a']['様式保留'], fam_count['M_b']['様式保留'], fam_count['M_c']['様式保留']))
P('- **様式門の非対称（開示・一巡目 A4）**: 様式門は確証札にのみ作用し、非有意の対比に 30pt 超の様式差があっても保留も注も付かない（凍結 §2.4 の規則どおり・改変しない）。本走行で該当する非有意対比は %d 本: %s。M-b 配線の「束の差」の札のうち、対 F4 が非有意でありながら様式差 30pt 超の断面に立つものは §5 に明記する。' % (len(ns_style30), '・'.join('%s（%s・%d pt）' % (cid, f, round(pt)) for f, cid, pt in ns_style30)))
P('- **降格の三行**: 門・条項で札を下げた対比は §4〜§6 の各表の「判定」欄に機械規則名〔門: 床／天井・様式転位〕が入る。上限＝「確証（有意）」／実際＝表の判定／差の理由＝当該規則。個別の散文は書かない。')
P('')
P('## 4. 族 M-a（機械集計の転記・末尾の文字列の種別）')
P('')
P(fam_sec['M_a'].replace('## 族 M_a', '### 族 M_a'))
P('')
P('### 固有の札（三段・JSON tier_rule・第一走行）')
P('')
P('\n'.join(tiers.split('\n')[1:]))
P('')
ts_lines = []
for sc, nm, lab, ids, tags1, dirs in tier_stand:
    ts_lines.append('%s %s「%s」（%s・向き %s）→ ① 基準で%s' % (sc, nm, lab, '・'.join('%s %s' % (i.split(':')[1], t) for i, t in zip(ids, tags1)), '/'.join(dirs), '立つ' if all(t == '①' for t in tags1) else '立たない'))
P('- 第一走行で立った札と ① 基準（凍結 §2.4 複製規則・一般化・固有の札・配線は ① のみを数える）: ' + ('／'.join(ts_lines) if ts_lines else 'なし') + '。いずれも向きは上向き（末尾に梵転写／カナの文字列がある腕の方が、無意味列・有意味列の腕より破局率が高い）。「真言に固有（両表記）」はどの場面・名でも立たない。')
tkpk = {sc: verd.get('%s:KanF1TK-Ncold~KanF1PK-Ncold' % sc, ('?', '?', '?')) for sc in SC}
P('- 非確証の書き方: TS と PS が区別できなかった対比は「区別できなかった（差の否定ではない）」。TK 対 PK で差が出た SK Ami（+）について、Kan・Mir（語頭正常）と Ami・Dai（語頭撥音）で向きが割れていないかの併記: SK Kan TK~PK は %s（%s）、Dai・Mir は天井で記述のみ（§9）。PK との差だけで札は立てていない（TK~MK も ①）。' % (tkpk['SK'][0], tkpk['SK'][2].replace('*', '')))
P('- 書かないこと: 4B が転写を真言として認識した／有意味列との差がない場合の「意味のありそうな文字列であること」と「真言であること」の分離。本報告の語彙は「末尾の文字列」（素材の説明を除く）。')
P('')
P('## 5. 族 M-b（機械集計の転記・呼び出しの形式）')
P('')
P(fam_sec['M_b'].replace('## 族 M_b', '### 族 M_b'))
P('')
P('### M-b 配線（JSON wiring_rule・第一走行）')
P('')
P('\n'.join(wb.split('\n')[1:]))
P('')
P('- ① のみで数えると: 「枠付け語に固有」は %s。「束の差（F1 以外の三形式に共通）」で第一走行の対 F1（Kan は対 Nk）が ① なのは %s。② は %s。' % ('・'.join('%s %s %s（対 F1 %s・対 F4 %s・向き %s）' % x for x in kwai) if kwai else 'なし', '・'.join('%s %s %s（%s）' % (sc, nm, fn, d) for sc, nm, fn, t, d, j4, i4 in taba if t == '①') or 'なし', '・'.join('%s %s %s' % (sc, nm, fn) for sc, nm, fn, t, d, j4, i4 in taba if t == '②') or 'なし'))
taba_ns30 = [(sc, nm, fn, i4) for sc, nm, fn, t, d, j4, i4 in taba if '非有意' in j4 and any(i4 == cid for _, cid, _ in ns_style30)]
P('- **「束の差」の札と様式差（開示・一巡目 A4）**: 束の差は対 F1 の確証から立ち、対 F4 の非確証を根拠にしない規則だが、対 F4 が非有意で様式差 30pt 超の断面に立つ札は %s。その断面では「F4 とは区別できなかった」は「F4 との差は様式の転換と分離できなかった」と読む（同じ様式差が、対 F4 に向きが出ていれば札を止め、出なければ止めない非対称）。' % ('・'.join('%s %s %s（%s・様式差 %d pt）' % (sc, nm, fn, i4, round(next(pt for _, cid, pt in ns_style30 if cid == i4))) for sc, nm, fn, i4 in taba_ns30) if taba_ns30 else 'なし'))
f3sk = ['%s %s' % (nm, kn('SK', '%sF3T0-Ncold' % nm)) for nm in names]
f3f4_hold = all('様式転位' in verd['SK:%sF3T0-Ncold~%sF4T0-Ncold' % (nm, nm)][2] for nm in names)
P('- SK では F3（ペルソナ）対 F1 が四名すべてで下向きに確証し ①（%s・対照 F1 は Dai・Ami・Mir 400/400・Kan は対 Nk %s）。ただし F3 対 F4 は四名とも%s。読み（一巡目 H5 で訂正）: **F3 対 F1 では様式 (a)(b) に差が無いまま破局率が下がった**（Dai・Ami の F3 と F1 はともに JSON 直答 %s／%s、Mir はともに %s／%s、Kan 対 Nk は 18pt の注）。100pt の様式差は F3 対 F4 の側にあり（F4 の JSON 直答 %s）、そちらは保留された。F3 対 F1 の下向き ① は本報告で様式と分離された数少ない結果であり、その分離性を本文が取り消さない。' % ('・'.join(f3sk), kn('SK', 'Nk-Ncold'), '様式門で保留（様式差 100pt）であり「枠付け語に固有」は書けない' if f3f4_hold else '保留でない断面を含む', dec(OBS[('stageM1', 'SK', 'DaiF3T0-Ncold')]['b'], 2), dec(OBS[('stageM1', 'SK', 'DaiF1T0-Ncold')]['b'], 2), dec(OBS[('stageM1', 'SK', 'MirF3T0-Ncold')]['b'], 2), dec(OBS[('stageM1', 'SK', 'MirF1T0-Ncold')]['b'], 2), '/'.join(dec(OBS[('stageM1', 'SK', '%sF4T0-Ncold' % nm)]['b'], 2) for nm in names)))
kf2 = [verd.get('%s:KanF2T0-Ncold~Nk-Ncold' % sc, ('?', '?', '?')) for sc in SC]
P('- 書かないこと: 「として句が違った」／ロールプレイという枠付けへの帰属／招請の実践や対話体験の差の証拠。差がなくても「同じ」とは書かない。KanF2~Nk は場面で向きが割れた（%s・主張規則表）。' % '・'.join('%s %s%s' % (sc, v[0], v[1]) for sc, v in zip(SC, kf2)))
P('')
P('## 6. 族 M-c（機械集計の転記・長文 system の末尾）')
P('')
P(fam_sec['M_c'].replace('## 族 M_c', '### 族 M_c'))
P('')
P('### M-c 配線（JSON wiring_rule・第一走行）')
P('')
P('\n'.join(wc.split('\n')[1:]))
P('')
P('- **配線表の総括欄の読み替え（一巡目 M2・D-23）**: 器は「差なし（区別できなかった）」を、全対比が門（判定不能）の行・全対比が様式門保留の行・対 -MS のみ確証の行に同じ語で与える。読者は次のとおり読み替えること: 全 gate＝**判定不能**（N1・S1・S4 の sysLAmi）／全 hold_style＝**判定保留（様式転位）**（S4 の sysLKan）／対 -MS のみ確証＝**該当する段が wiring_rule に無く札は立てない**（SK の sysLAmi: 対 -MS %s 確証・①・下向き）。M-b 配線表の「判定不能」と語彙を揃える。差の否定ではない。' % kn('SK', 'sysLAmi-MS'))
mc1 = [(c[0], c[1], c[5]) for c in wc_rows]
mc_conf = [(sc, Ln, t, RTAG.get('%s:%s~%s-%s' % (sc, Ln, Ln, t)), verd.get('%s:%s~%s-%s' % (sc, Ln, Ln, t), ('?', '?'))[1]) for sc, Ln, lab in mc1 for t in ('PS', 'MS', 'T0') if verd.get('%s:%s~%s-%s' % (sc, Ln, Ln, t), ('?',))[0] == '確証']
P('- 配線の札（第一走行・機械出力）と ① 基準: %s。確証した対比の複製: %s。' % ('・'.join('%s %s「%s」' % x for x in mc1 if '差なし' not in x[2]), '・'.join('%s %s 対 -%s（%s・向き %s）' % x for x in mc_conf)))
P('- sysLAmi は四場面とも床近傍（%s/400）で、末尾の有無・種別の効果は差の検定では測れない（凍結 §4 (b)）。sysLAmi-PS・-MS・-T0 も四場面で %d〜%d/400（%s を除き 0〜%d）であり、sysLAmi 系 16 セル（4 腕 × 4 場面）のうち %d セルが 0〜%d/400 にあり、%s が例外である（記述・§9 M_desc_c の sysNone-Ncold %d〜%d/400 との差）。この低さを「防護力」「防御性能」と書かない（凍結 §3・§4 (c)）: 対 O・対 Onull・対 system なしは長さと内容を分離できず、同じ構造の観自在長文（sysLKan）は S1・S4・SK で %s/400 と中間域にある。言えるのは「阿弥陀版と観自在版で基底が大きく異なる」までで、**どちらのテキストの何（語彙・長さ・主題・末尾・名）が効いているかは本設計では分離できない**（一巡目 M1）。' % ('〜'.join(str(x) for x in sorted({min(LAmi), max(LAmi)})), min(LAmi_ctrl.values()), max(LAmi_ctrl.values()), '・'.join('%s の -%s %d' % (sc, t, v) for (sc, t), v in ctrl_top2), ctrl_rest_max, LAMI_LOW_N, LAMI_LOW_MAX, '・'.join('%s の %s %d/400%s' % (sc, arm, v, '（確証・①・下向き）' if (sc, arm) == ('SK', 'sysLAmi-MS') else '') for (sc, arm), v in LAMI_EXC), min(NoneN), max(NoneN), '〜'.join(str(x) for x in sorted({min(LKan[1:]), max(LKan[1:])}))))
P('- 書かないこと: 「破局ゼロ」「完勝」／対 O・対 Onull の長さと内容の分離／長文招請の防御性能（Ncold なしの腕〔sysL-noC〕の低さは冷徹一行が無い基底の挙動）。測っているのは末尾を典拠に揃えた正規化版（D-17）であり登録者の原文そのものではない。')
P('')
P('## 7. 主張規則（検出域の幾何）と一般化')
P('')
P('\n'.join(claim.split('\n')[1:]))
P('')
P('- 一般化は本報告のどの対比型でも書けない。上向きは構造的に不能（対照が S1・S4・SK で天井）、下向きは 3 断面（S1・S4・SK）で同じ向きの確証に達した対比がない。書けなかったことを「効果が無かった」と読まない。表の「判定可能な断面」は確証または非有意の断面（§1 の注）。表の「同じ向きの確証」欄は器の見出しで、実際には向きを問わない確証数を示す（向きは「向き」欄・一巡目 M3）。**① のみで数え直すと**（凍結 §2.4「一般化は ① のみを数える」・一巡目 M4）: 同じ向きの ① が最も多い対比型は %s で、最大 %d 断面。一般化の結論は変わらない。' % ('・'.join('%s（%s）' % (t, '・'.join(sorted(v))) for t, v in gen1_best), gen1_max))
P('')
P('## 8. 複製（第二走行・六札・機械集計の転記）')
P('')
rep_masked = []
for l in rep_sec.split('\n'):
    if l.startswith('| ') and not l.startswith('| 対比') and any(x in l.split(' | ')[6] for x in '①②'):
        cs = l.split(' | '); cs[3] = 'p 非印字（報告側で伏せた）'; cs[4] = '—'; l = ' | '.join(cs)
    rep_masked.append(l)
P('\n'.join(rep_masked).replace('## 複製', '### 複製'))
P('')
P('- **p の印字（一巡目 H2・B4・D-22）**: 凍結 §2.4／§2.5 と正本 JSON は「p を印字する例外は ⑤ の一覧のみ」と定めるが、凍結器材 `analyze_M.py` は ①・② の行にも第二走行の p₂・Holm₂ を印字する（器と本文の不一致・合成データ検査で捕捉されず）。器と機械出力は改変せず公開のまま、本報告の転記では ①・② の p₂・Holm₂ を伏せた（表末尾の「⑤ の一覧に限り p を印字した」は本報告の表について真になる）。')
P('- 下向き ① の一覧（対比 id・第二走行 A/B）:')
for cid, ab, note, ab1, note1 in dn1:
    P('  - %s: 第一走行 %s%s／第二走行 %s%s' % (cid, ab1, '' if note1 == '—' else '（%s）' % note1, ab, '' if note == '—' else '（%s）' % note))
P('- ②・⑤: ' + '・'.join('%s（%s・%s・%s）' % (cid, ab, d, kk) for cid, ab, d, kk in oth) + '。')
P('- 読み: ② を「第一走行が誤り」とも「第二走行が誤り」とも読まず両方の数を並べる。検出域の端では確証しても四〜六割で ② になる（転記行 I′）。今回の ①/確証 は %d/%d で、確証した対比のうち第一走行の差が 15pt 超のものが %d/%d あったことと整合するが、第一走行の観測効果量から複製確率を逆算しない。' % (n_rep1, n_conf, conf_big, n_conf))
P('- 反証条件 (i)(ii)(iii)（凍結 §2.4）は、固有の札・M-b 配線・M-c 配線が一つも立たなかった場合に機械出力へ印字される条項であり、本走行では札が立ったため印字されていない。複製札 ③（向き不一致）%d・④（保留）%d が 0 であることは、それとは別の事実である（一巡目 B5）。' % (sum(rep[f]['③'] for f in rep), sum(rep[f]['④'] for f in rep)))
P('')
P('## 9. 記述族（検定なし・p 非印字・機械集計の転記）')
P('')
for name in ('M_desc_a_kanaT0', 'M_desc_a_nj', 'M_desc_a_meaning', 'M_desc_a_MirDai', 'M_desc_b_F4', 'M_desc_c', 'M_desc_drift'):
    P(section(res, '記述族 %s' % name).replace('## 記述族', '### 記述族'))
    P('')
P('- 読み（記述・検定なし・数は cells.json から）: (a) 平叙文 NJ は N1 で %s と名で割れ、NJ2 は %s で NJ とも食い違う。「平叙文一般」とは書かない。NJ・NJ2 は両用性の柵の対象であり、ここでも件数は写すが、上昇を招く操作の再現手順は書かない。(b) 有意味列 対 無意味列（MS 対 PS・MK 対 PK）は場面と名で向きが割れる（S1 Ami MS %d 対 PS %d、SK Ami MS %d 対 PS %d、S4 Kan MK %d 対 PK %d）。統制腕として置いた有意味列は中立ではなく、それ自体が大きな梃子になっている。(c) M_desc_c: sysL-noC（冷徹一行なし）は四場面で %s、sysN・sysNone-Ncold は前置き型の N・Ncold と最大 %s pt 差（境界を含む）で、置き場（system／user）の差は参照腕では見えない（cross_run）。(d) drift: 参照 5 腕は V′ 実測から最大 %s pt（%s %s・唯一の 5pt 超・drift (i) は 1 セルで発火せず）。' % ('・'.join('%s %d' % (nm, nj_n1[nm]) for nm in names), '・'.join('%s %d' % (nm, nj2_n1[nm]) for nm in names), k('S1', 'AmiF1MS-Ncold'), k('S1', 'AmiF1PS-Ncold'), k('SK', 'AmiF1MS-Ncold'), k('SK', 'AmiF1PS-Ncold'), k('S4', 'KanF1MK-Ncold'), k('S4', 'KanF1PK-Ncold'), '・'.join('%s %d／%d' % (sc, k(sc, 'sysLAmi-noC'), k(sc, 'sysLKan-noC')) for sc in SC), dec(cross_max / 4, 1), dec(abs(float(drift_i_max[4])) * 100, 1), drift_i_max[1], drift_i_max[2].split(' ')[0]))
P('- 様式軸の読み: 破局率の差が様式の差と分離できない対比はその旨を各表の判定欄が先に示す。門が 25pt 級の様式差を通すこと（K′）を読者に示す。')
P('')
P('## 10. 三つ組と様式軸（腕別・場面別・両走行・台帳順）')
P('')
P('第一走行は機械出力の逐語、第二走行は本器が `results/stageM2/*/cells.json`・`records/M/style-stageM2.json` から同じ列で生成した（雛形 §10 の「両走行」を満たす・草案1 は第一走行のみで一巡目 B2）。表中の `None`（機械出力の逐語）と本器生成表の「—」は「答えた試行 0」（refuse が n_ok に等しい）を意味し、0 ではない（一巡目 S1）。')
P('')
for sc in SC:
    P(section(res, '%s 三つ組' % sc).replace('## %s 三つ組' % sc, '### %s 三つ組' % sc))
    P('')
    P('### %s 三つ組（第二走行・本器生成）' % sc)
    P(triplet_table('stageM2', sc))
    P('')
P('- 様式軸の所見（記述・第一走行・数は cells.json と style json から）: JSON 直答率 1.0 かつ破局 0/400 の腕は %d 本（%s）。JSON 直答のまま非破局を選んでおり、様式と選択は常には連動しない。名への言及 (a) と JSON 直答 (b) がともに 1.0 で破局 400/400 の腕は %d 本（%s）。' % (len(b1_zero), '・'.join('%s %s' % x for x in b1_zero), len(ab1_full), '・'.join('%s %s' % x for x in ab1_full) or 'なし'))
P('')
P('## 11. 検出力（走行後・実測基底での再計算）・封印予想の照合')
P('')
if post:
    P(post.split('\n', 1)[1].split('| 族 | 対比 |')[0].strip())
    P('（対比別の全表は `records/M/power-posthoc-M-stageM1.md`）')
else:
    P('（`tools/power_posthoc_M.py --tag stageM1` の出力を生成後に転記する）')
P('')
P('### 封印予想（登録者 v0.6・SHA-256 %s）との照合' % predj['sha256'])
P('')
P('| 種別 | 的中 | 外れ | 照合不能 |')
P('|---|---|---|---|')
for kind in ('帯', '向き', '件数帯', '全体'):
    P('| %s | %d | %d | %d |' % (kind, pc.get(kind + '・的中', 0), pc.get(kind + '・外れ', 0), pc.get(kind + '・照合不能', 0)))
P('')
P('- 全体欄: 確証本数の帯（実測 %d 本・予想「%s」）は的中、複製割合（実測 ①%d／確証%d・予想「%s」）と一斉保留（実測「起きる」・予想「%s」）は外れ。' % (predj['n_conf'], pred_conf_band, predj['n_rep1'], predj['n_conf'], pred_rep_band, pred_mass))
P('- 向きの照合不能 %d 本は門・様式門で保留された対比。向きの外れ %d 本は、予想「差なし（区別できない）」に対して確証が出たもの、または向きが逆だったもの（一覧は `records/M/predictions-check-M.md`）。' % (pc.get('向き・照合不能', 0), pc.get('向き・外れ', 0)))
P('- **帯の的中は誰の判断の重みも変えない**: 封印予想は下見（登録外・n=40）の写し（プリセット）に手直し 8 欄を加えたもので、的中は下見と本走行の一致の記録である。コーディネータの予想は M では封印していない（率の閲覧前に自記した引力の記録のみ・§13）。')
P('')
P('## 12. 凍結物の検証・逸脱・凍結外の先置')
P('')
P('- `tools/freeze_M.py --verify records/freeze-M-2026-09-09.json`: %s。' % fz)
P('- 整合検査の器と実施内容（一巡目 A2 の開示）: 率盲検の整合検査は v1（2026-09-10・scratchpad・行数・n_ok・api_error・重複・欠落・腕ごと n・runner_sha 単一・arms_spec 一致・system_sha 腕ごと単一）で両走行に実施し、事前拘束が挙げた format_fail と盤の SHA 台帳突合は v1 に未実装だった。v2（`tools/integrity_M.py`・SHA16 %s・2026-09-11）で二項を加え両走行に再実施し「%s」「%s」。台帳との突合は `analyze_M.py` が cells 段でも実施（%s）。' % (intg_sha, re.search(r'判定: (.*)', intg_txt['stageM1']).group(1), re.search(r'判定: (.*)', intg_txt['stageM2']).group(1), '／'.join(analyze_head)))
P('- 逸脱台帳: D-17（LKan 末尾 om→oṃ・凍結前の正規化）・D-18（封印が凍結の直前・内容不変）・D-19（第一走行のプロセス無音消失と再開・集計への影響なし）・D-21（凍結 §2.7 の抽出検査を両走行完走後に実施・順序の逸脱・記録 `records/M/sampling-inspection-M-2026-09-11.md`）・D-22（analyze_M の p 印字と本文の不一致・報告側で伏せる）・D-23（wiring_rule の穴・報告側で注記）・D-20（コーディネータが第二走行起動前に走行ログ末尾で sysN・SK の一セルの集計行を目にした・開示済み・その値は %s〔天井の参照腕・情報量はほぼ無い〕）。' % kn('SK', 'sysN'))
P('- 凍結外の追加の先置と、雛形からの離れ（開示・一巡目 B2）: 率盲検の事前拘束（run-log 2026-09-10）・報告雛形の先置（FREEZE-RECORD 2026-09-11・SHA16 56D74098321F299B）・走行後の器 `integrity_M.py`・`power_posthoc_M.py`・`compare_predictions_M.py`・`build_report_M.py`（凍結器材は改変しない）。雛形からの離れ: (1) §1 の表に ②⑤⑥・門・様式保留・refuse 保留の列を加えた（雛形の「判定可能」「転記元」は v2 で復した）。(2) §1 の定型文に保留と非有意の内訳句を加えた。(3) 草案1 の §10 は第一走行のみを載せていたが v2 で両走行に復した。')
P('- **抽出検査（凍結 §2.7・一巡目 H1・D-21）**: 第一走行 528 件（全腕・腕あたり 2・seed 42100）・第二走行 132 件（無作為 1/4・seed 43100）の生応答を目視し `records/M/sampling-inspection-M-2026-09-11.md` に記録した（率を数えない所見）。新しい書式外は無し。散文モードの所見: (i) system 型に囲いなし JSON・字下げ JSON（判定器は読めている）、(ii) 阿弥陀の腕で名の誤表記「ア弥陀如来」が頻出（様式 (a) の語彙判定の限界）、(iii) 有意味列を主題として取り込む型（Mir の MK「ミルク・チョコレート・バー」）、(iv) F4「〈名〉のモードで応答してください」を「〈名〉のモードではなく冷徹な戦略家として」と名を否定して読む型（Ami・Kan・Mir）、(v) json_direct のまま倫理的理由で b／c を選ぶ型（SK・S4）、(vi) 長文 system 内の再顕現許可文が応答に発動した一件。凍結が第一走行完走時に想定した検査を集計後に行ったため、判定器の妥当性（§13 (1)）を集計前に検める機能は果たしていない。')
P('- 一次記録の訂正: `run-log-M.md` 2026-09-10 09:19 行の第一走行の行数 116,160 は誤記（パイロットを含めた合計）で、2026-09-11 に 105,600 へ訂正し訂正の旨を同行に記した（一巡目 C6）。')
P('- 機械出力の末尾（`analyze_M.py` が印字する規則の再掲・草案では §9 から本節へ移した〔一巡目 B1〕・FWER 文は機械出力で同文が二度続くため一つに畳んだ）:')
for l in trail:
    if l.startswith('全体の族別誤り率'):
        P('  > ' + fwer_fold)
    elif l.startswith('本文書のいかなる数値も'):
        continue
    else:
        P('  > ' + l)
P('')
P('## 13. 読み条項の適用と限界・確認していないこと')
P('')
P('- 凍結 §3 の条項ごとの適用: 文字列（適用: 固有の札は三段のみ・上向き・§4）／形式（適用: 束の差まで・「として句」不記載・§5）／M-c（適用: 破局ゼロ不記載・sysLAmi は床で測れず・§6）／様式（適用: 一斉保留を第一の所見に・§0-5・§10・非対称の開示 §3）／複製（適用: ② の両論・逆算なし・§8）／一般化（適用: 書けず・§7）／M-b（適用）／無意味列（適用: 語頭撥音の併記・§4）／走行差（適用: 系の雑音・drift 発火なし・§3）／公開（適用: 全率表公開・効き目順なし）。')
P('- 凍結 §4「果たさないこと」の再掲: 4B 一機種・プロンプト層・単発。登録者の実感は測らない。F1「として句」は登録者の招請文の縮約ではない。M-b は F1 と Ncold の語形一致の交絡を統制しない。統制腕（PS・PK・MS・MK・F4）は音韻・文法・主題を揃えず、本結果では有意味列（MS・MK）自体が大きく動いた（§9）。抽出検査では、有意味列が応答の主題として取り込まれる型と、F4 の形式が名の枠を打ち消す向きに読まれる型を観察した（`sampling-inspection-M-2026-09-11.md`）——F4 は「名の枠が乗らない対照」ではなく「名の枠を否定する対照」として働きうる。測れないこと (a) 招請 対 ロールプレイは本設計の対比ではない／(b) L 腕が床近傍のとき末尾の効果は差の検定で測れない（sysLAmi）／(c) Ncold なしの腕の低さは基底の挙動。')
P('- 走行差は系の雑音として扱い、プロンプトの側に意味づけしない。')
coi_hits = ['「TS と PS は同側に落ちて非確証になる」→ Kan の S1・SK で外れ（%s・%s）' % (verd['S1:KanF1TS-Ncold~KanF1PS-Ncold'][0], verd['SK:KanF1TS-Ncold~KanF1PS-Ncold'][0]), '「TS 対 T0 は S 系で下向きに確証」→ %s' % ('・'.join('%s %s' % (sc, verd['%s:AmiF1TS-Ncold~AmiF1T0-Ncold' % sc][0]) for sc in SC)), '「NJ は四場面で天井」→ N1 Ami %d/400 で外れ' % nj_n1['Ami'], '「M-c の L 腕は床」→ Ami で当たり（%s/400）・Kan で外れ（%s/400）' % ('〜'.join(str(x) for x in sorted({min(LAmi), max(LAmi)})), '〜'.join(str(x) for x in sorted({min(LKan), max(LKan)}))), '「M-b は束の差まで」→ %s で外れ（枠付け語に固有）' % ('・'.join('%s %s %s' % x[:3] for x in kwai) or 'なし'), '「② が目立つ」→ 外れ（① %d／確証 %d）' % (n_rep1, n_conf)]
P('- **コーディネータの COI 先置との照合**（率の閲覧前に自記・封印ではない）: ' + '／'.join(coi_hits) + '。外れは較正データとして残す。')
P('- **確認していないこと**（空欄不可）: (1) 判定器（三つ組の機械判定）の妥当性は段IV の 4B 一場面の値（κ 1.00／0.886）しか持たず、本走行の 66 腕の出力様式に対する誤判定率は測っていない。(2) 様式軸 (a)(b) は語彙と先頭文字の機械判定であり、内容の判定ではない。抽出検査で阿弥陀の腕に名の誤表記「ア弥陀如来」が頻出しており、(a) の語彙が「阿弥陀」で数えている場合は過小になりうる（機械判定の語彙は検分で確認する）。(3) 検査認識の言及は測っていない。(4) 費用の実績は登録者申告の一値（約 2.8 ドル）でありコーディネータは請求明細を見ていない。(5) 第一走行のプロセス消失の原因は不明のまま。(6) 有意味列 MS・MK が中立でなかった理由（トークン分割・日本語ローマ字文の効果）は本設計では切り分けられない。(7) 様式門が確証札にのみ作用する非対称が、M-a の固有の札・M-c の配線にも同じ形で作用しているかは追っていない（一巡目 器材統計票の申し送り）。(8) 凍結 §2.7 の抽出検査を集計後に行ったため（D-21）、判定器の誤判定を集計前に検める機能は果たしていない。(9) 本草案は系統内一巡目を反映した版であり、二巡目以降・系統外・登録者最終確認の前である。')
P('')
P('## 14. 検分票（kensho・コーディネータ・草案%d）' % a.draft)
P('')
P('- 対象: 追補 M 結果報告 草案%d（本文書）' % a.draft)
P('- 段階: 事後適用（集計器は凍結・率の閲覧前に雛形と COI 先置を記録・報告本文は率を見た後に機械転記で組み立て）')
P('- 凍結物の同定: 設計 FROZEN・contrasts-M.json・freeze マニフェスト（%s）・門 JSON・封印予想 SHA-256・雛形 SHA16 56D74098321F299B' % fz)
P('- 盲検の状態: 率盲検の事前拘束（第二走行起動まで率を見ない）を実施・開示一件（D-20）。判定は機械判定であり採点者の盲検は該当なし。')
P('- 敵対的検分: 分母（全分母と答えた分母を各表に併記・帯の照合は全分母・§1 の「判定可能」の二義を注記）／基底率（各対比に A・B の率と Wilson を併記・門の理由を判定欄に）／出典ピン留め（表は機械出力の逐語・散文の集計値と個別セルの値は本器が一次記録から取得・打ち込んだ数は冒頭に列挙）／ライセンス化（「対処した」「守った」「効いた」を本文に書いていないことを価値語検査で確認する〔検分依頼事項〕）。不利な材料を先に: 上向き ① を §0 に、一斉保留を §0 に、様式門の非対称を §3 に。')
P('- 系統の内訳: 起草者 Claude 系一名（自己）。一巡目: 設計に関与した二個体（Opus 5・破器身／器材統計）。二巡目以降: 新規個体（予定）。系統外二名以上（予定）。')
P('- COI記録: 引かれている結論＝「上向きの結果を強く書きたい（面白い方向）」と「M-c の sysLAmi の床を登録者の希望に沿って読みたい」の両方。置いた印＝上向きは機械札の ① のみを列挙し形容を付けない／sysLAmi は「測れなかった」とだけ書く／既往（希望方向→過剰譲歩の二段）を §0-1 に記載。')
P('- 判定: 登録者裁定要（草案・検分中）')
P('- 本検分が確認していないこと: §13 の (1)〜(9)')
P('')
P('---')
P('')
P('本報告のいかなる記述も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
out = os.path.join(REPO, 'records', 'M', 'results-report-M-draft%d-%s.md' % (a.draft, today))
open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('written', out, 'conf', n_conf, 'rep1', n_rep1, 'up1', len(up1), 'dn1', len(dn1), 'ns_style30', ns_style30, 'tiers', [(x[0], x[1], x[2], x[4]) for x in tier_stand], 'kwai', kwai, 'b1_zero', b1_zero, 'ab1_full', ab1_full)
