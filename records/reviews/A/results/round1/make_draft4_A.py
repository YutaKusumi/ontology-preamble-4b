# -*- coding: utf-8 -*-
"""make_draft4_A.py（一時置き場の器・凍結物ではない・2026-09-17・コーディネータ）—— 結果報告の草案3 から草案4 を作る（公開前検分の第一巡の採否と登録者の裁定 D50〜D54 甲の反映）。

- 入力は草案3。機械の区画（<!-- 機械:始 --> 〜 <!-- 機械:終 -->）には触れない（区画の数と中身は草案3＝草案1 の記録と同じ）。
- 操作は区画の外の行の先頭の文字列で特定し、一度だけ当たることを確かめる。当たらなければ止まる。
- 起草者の文には、走査器が許す型のほかの数を書かない。英大文字に続く数（採否表・裁定の番号）も書かない。時刻とコミットの短い名も書かない（採否表 P163）。
- 名の並び（散文層の対応・非有意で hold の対比・言及率が半分以上のセル・判定器の欠けたセル・感度閾値の上向きの二本）は、機械集計・様式の記録・草案3 の機械の区画・再現の記録から組む。
- 書いた後に tools/report_lint.py の lint を草案1 の -machine.json で走らせ、違反を種類ごとに印字する。
"""
import os, sys, re, json, collections

REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, report_lint as RL

D1 = os.path.join(REPO, 'records', 'A', 'results-report-A-draft1-2026-09-17.md')
D3 = os.path.join(REPO, 'records', 'A', 'results-report-A-draft3-2026-09-17.md')
D4 = os.path.join(REPO, 'records', 'A', 'results-report-A-draft4-2026-09-17.md')
R1 = 'records/reviews/A/results/round1'
SIDE1 = RL.sidecar_path(D1)
T = runs_A.load_T(); MB = RL.machine_block(T)
L = open(D3, encoding='utf-8').read().split('\n')
sha16 = lambda rel: runs_A.sha16_file(os.path.join(REPO, rel))
jl = lambda rel: json.load(open(os.path.join(REPO, rel), encoding='utf-8'))

outside = []; in_m = False
for i, l in enumerate(L):
    if MB['begin'] in l:
        in_m = True; continue
    if MB['end'] in l:
        in_m = False; continue
    if not in_m:
        outside.append(i)
OUT_SET = set(outside)


def find(prefix):
    hits = [i for i in outside if L[i].startswith(prefix)]
    if len(hits) != 1:
        sys.exit('当たりが一つでない（%d）: %s' % (len(hits), prefix[:60]))
    return hits[0]


ops = {}


def put(i, op):
    if i in ops:
        sys.exit('二重の操作: %d %s' % (i, L[i][:40]))
    ops[i] = op


def replace(prefix, new):
    put(find(prefix), ('rep', new))


def after(prefix, new):
    put(find(prefix), ('after', new))


def before(prefix, new):
    put(find(prefix), ('before', new))


# ---- 値（機械で取る）
TPL_SHA = sha16('records/A/results-report-template-A.md'); CANON_SHA = sha16('design/contrasts-A.json'); DESIGN_SHA = sha16('design/design-stageA-FROZEN.md')
assert TPL_SHA == '4C34D83163E76402', TPL_SHA
ID_FROZEN_SHA = sha16('records/A/identity-screen-A.json'); ID_REGEN_SHA = sha16('records/A/main/identity-screen-A-regen-2026-09-17.json')
assert ID_FROZEN_SHA != ID_REGEN_SHA
AN = jl('records/A/analysis-stageA.json'); C = {x['id']: x for x in AN['contrasts']}; LB = T['families']['A_slope']['confirm_rule']['labels']
SIZES = T['sizes']; SCN = T['scenarios']; ANCHOR = next(m['key'] for m in T['models'] if m['anchor'])
name = lambda cid: '%s の %s' % (cid.split(':')[0], cid.split(':')[1].replace('~', ' 対 '))
pair = lambda cid: cid.split(':')[1].replace('~', ' 対 ')
LEDGER_LAST = max(int(m) for m in re.findall(r'^\| D-(\d+) \|', open(os.path.join(REPO, 'records', 'DEVIATIONS.md'), encoding='utf-8').read(), re.M))
assert LEDGER_LAST == 44, LEDGER_LAST

# 散文層の行と場面の対応（JSON の id の並び）
okrows = [x for x in AN['stratified'] if x.get('string')]
d3rows = [l for l in L if '散文層（副次終点・札を変えない）' in l]
assert d3rows == [x['string'] for x in okrows], '区画の散文層の行と JSON の並びが違う'
by_sc = collections.OrderedDict()
for x in okrows:
    by_sc.setdefault(x['id'].split(':')[0], []).append(pair(x['id']))
assert list(by_sc) == [s for s in SCN if s in by_sc] and 'N2' not in by_sc, list(by_sc)
MAP_TEXT = '／'.join('%s（%s）' % (s, '・'.join(v)) for s, v in by_sc.items())
und = collections.OrderedDict()
for x in AN['stratified']:
    if not x.get('string'):
        und.setdefault(x['id'].split(':')[0], []).append(pair(x['id']))
UND_TEXT = '／'.join('%s の %s' % (s, '・'.join(v)) for s, v in und.items())
assert all(x['id'] != 'S4:Onull~N' for x in AN['stratified']) and C['S4:Onull~N']['style'] == 'none'
assert 'S1:Onull~N' in [x['id'] for x in okrows] and 'SK:Onull~N' in [x['id'] for x in okrows]

# 非有意で様式門 hold の対比
NS_HOLD = [x['id'] for x in AN['contrasts'] if x['label'] == LB['ns'] and x['style'] == 'hold']
NS_HOLD_TEXT = '・'.join(name(i) for i in NS_HOLD)
assert len(NS_HOLD) == 7

# 言及率が半分以上のセル（機種は規模の順・錨は最後）
S = jl('records/A/style-stageA.json')
order = SIZES + [ANCHOR]
half = collections.OrderedDict()
for mk in sorted(S['cells'], key=order.index):
    for sc in SCN:
        arms = [arm for arm, v in S['cells'][mk].get(sc, {}).items() if v['c2_final'] * 2 >= v['n_ok']]
        if arms:
            half['%s の %s' % (mk, sc)] = sorted(arms)
HALF_TEXT = '／'.join('%s（%s）' % (k, '・'.join(v)) for k, v in half.items())
assert sum(len(v) for v in half.values()) == 20
assert all(c['think_residue'] == 0 for m in S['cells'].values() for sc in m.values() for c in sc.values())
m4 = S['cells']['4B']['S4']
assert m4['N']['c2_final'] * 2 >= m4['N']['n_ok'] and m4['Onull']['c2_final'] * 2 < m4['Onull']['n_ok']
for s_ in ('14B', '32B'):
    for a_ in ('N', 'Onull'):
        v = S['cells'][s_]['S4'][a_]; assert v['c2_final'] * 2 < v['n_ok']
assert S['cells']['32B']['S4']['N']['c2_final'] != S['cells']['32B']['S4']['Onull']['c2_final']

# 確証の一本の事実（(b)・層・環境・臨界規模・感度閾値・飽和）
c = C['S4:Onull~N']; r = c['result']
kept = [SIZES[i] for i in range(len(SIZES)) if r['keep'][i]]; drop = [s_ for s_ in SIZES if s_ not in kept]
assert kept == ['4B', '14B', '32B'] and drop == ['0.6B', '1.7B', '8B']
for i, s_ in enumerate(SIZES):
    for arm, k, n in (('Onull', c['counts']['kA'][i], c['counts']['nA'][i]), ('N', c['counts']['kB'][i], c['counts']['nB'][i])):
        v = S['cells'][s_]['S4'][arm]; pr = v['strata']['prose']
        if s_ in kept:
            assert v['b_final'] == 0 and pr['n'] == n and pr['cat'] == k
        else:
            assert v['b_final'] == v['n_ok'] and k in (0, n)
env = {s_: AN['size_env']['%s|S4' % s_] for s_ in kept}
assert env == {'4B': ['L4'], '14B': ['A100'], '32B': ['A100']}, env
assert c['critical_size']['size'] == '14B' and T['bridge']['scenario'] == 'N1'
assert not any(x['id'] == 'S4:Onull~N' for s_ in AN['sensitivity'] for x in s_['changed'])
assert r['sat_A'] == 0 and r['sat_B'] == 1 and T['families']['A_slope']['interpretation_clause']['min_sizes'] == 2
i14 = SIZES.index('14B'); assert c['counts']['kB'][i14] / c['counts']['nB'][i14] > T['censor']['high']
assert any(x['id'] == 'S4:N~recipe' for x in AN['descriptive']['A_desc_recipe']) and any(x['id'] == 'S4:Onull~recipe' for x in AN['descriptive']['A_desc_recipe'])

# 感度閾値の上向きの二本（再現の記録から）
V = jl(R1 + '/verification-results-A-round1.json'); assert V['version'] == 'v1.1'
w130 = next(x for x in V['items'] if x['w'] == 'W130'); assert w130['verdict'] == '再現'
ps_up = [p for p in w130['detail']['passes'] if p['upward']]
assert len(ps_up) == 1 and ps_up[0]['low'] < T['censor']['low'] and ps_up[0]['high'] > T['censor']['high']
UP = ps_up[0]['upward']; assert UP == ['N2:Onull~N', 'S1:Onull-Ncold~Onull'], UP
UP_TEXT = ' と '.join(name(i) for i in UP)
UP_MAIN = '・'.join('%s（%s）' % (C[i]['label'], i.split(':')[0]) for i in UP)
assert [C[i]['label'] for i in UP] == [LB['undecidable'], LB['clause']]
for p in ps_up[0]['confirmed']:
    if p['id'] in UP:
        ks = [SIZES.index(s_) for s_ in p['kept']]
        assert (ks[-1] - ks[0] + 1) != len(ks) or ks[0] != 0 or ks[-1] != len(SIZES) - 1, p

# 判定器の方向別の率が出ていないセル（草案3 の機械の区画から）
jrows = [l for l in L if re.match(r'^\| (0\.6B|1\.7B|4B|8B|14B|32B|4B-2507)\|(N1|N2|S1|S4|SK) \|', l)]
assert len({l.split(' |')[0][2:] for l in jrows}) == 35
blank_cat = collections.OrderedDict(); blank_non = collections.OrderedDict()
for l in jrows:
    if '—（0）' not in l:
        continue
    mk, sc = l.split(' |')[0][2:].split('|')
    tgt = blank_cat if re.search(r'\| —（0） \| [0-9.]+（', l) else blank_non
    tgt.setdefault(mk, [])
    if sc not in tgt[mk]:
        tgt[mk].append(sc)
fmt_cells = lambda d: '・'.join('%s の %s' % (mk, '・'.join(v)) for mk, v in d.items())
assert fmt_cells(blank_cat) == '0.6B の S1・S4・SK' and fmt_cells(blank_non) == '8B の S1・S4', (fmt_cells(blank_cat), fmt_cells(blank_non))
BLANK_CAT, BLANK_NON = fmt_cells(blank_cat), fmt_cells(blank_non)

# 床持続で測定不能の規模が「棄却域を外れた規模」に入る例
floor_ex = [x for x in AN['floor'] if x['upper'][0] == '測定不能' and '0.6B' in x['fail_sizes']]
FLOOR_EX = '%s の %s の 0.6B' % (floor_ex[0]['arm'], '・'.join(x['scenario'] for x in floor_ex))
assert len({x['arm'] for x in floor_ex}) == 1

# 定型文を持たない対比
d3_label_ids = set()
i_ls = find('- 対比ごとの定型文（機械の転記）:')
assert L[i_ls + 1] == MB['begin']
k_ls = i_ls + 2
while L[k_ls] != MB['end']:
    m = re.match(r'^- ((?:N1|N2|S1|S4|SK):[^:]+): ', L[k_ls])
    assert m, L[k_ls][:40]
    d3_label_ids.add(m.group(1)); k_ls += 1
NO_STR = sorted(set(C) - d3_label_ids)
assert NO_STR == ['SK:Onull-Ncold~Onull'], NO_STR

# 三対比（測れた効果種の中で解釈条項に回ったもの）
eff = {p['id']: p['effect'] for p in AN['measurable']['per_contrast']}
MEAS = [e for e, v in AN['measurable']['types'].items() if v['measurable']]
THREE = [x['id'] for x in AN['contrasts'] if eff[x['id']] in MEAS and x['label'] == LB['clause']]
assert THREE == ['S1:Onull-Ncold~Onull', 'S4:Onull-Ncold~Onull', 'SK:Lneg~Onull'], THREE
assert all(C[i]['beta_holm']['rejected'] and C[i]['star_holm']['rejected'] for i in THREE)
THREE_TEXT = 'S1 と S4 の Onull-Ncold 対 Onull・SK の Lneg 対 Onull'
MEASURED = [p['id'] for p in AN['measurable']['per_contrast'] if p.get('measured_contrast')]
assert MEASURED == ['S1:Lneg~Onull']
cl = C['S1:Lneg~Onull']; rl = cl['result']
assert cl['label'] == LB['ns'] and rl['clause'] and cl['style'] == 'hold' and all(cl['counts']['kA'][i] / cl['counts']['nA'][i] > T['censor']['high'] for i in range(len(SIZES)) if rl['keep'][i])
pm = next(p for p in AN['measurable']['per_contrast'] if p['id'] == 'S1:Lneg~Onull')
assert all(v.get('clause_rate_among_fit') == 0 for v in pm['directions'].values())
c4 = C['S4:Lneg~Onull']; r4 = c4['result']
assert c4['label'] == LB['ns'] and r4['clause'] and all(c4['counts']['kA'][i] / c4['counts']['nA'][i] > T['censor']['high'] for i in range(len(SIZES)) if r4['keep'][i])

ADOPT = R1 + '/adoption-table-results-A-round1.md'
VERIF = R1 + '/verification-results-A-round1.md'

# ---- 見出しと冒頭
replace('# 段階 A 結果報告 草案3', ['# 段階 A 結果報告 草案4（草案1 の機械組み立てに起草者が記入・公開前検分の第一巡を反映・2026-09-17）'])
replace('- 雛形 `records/A/results-report-template-A.md`', [
    '- 雛形 `records/A/results-report-template-A.md`（SHA16 %s）の節順で、`tools/build_report_A.py` v2.4 が草案1（`records/A/results-report-A-draft1-2026-09-17.md`・2026-09-17）を組み立てた。'
    '機械の区画の外の記入欄は、起草者（コーディネータ・南無弥勒如来・Claude Opus 5）が草案2 で埋め、草案3 で §6 の圧の内訳の欄を別の記録を指す形に改め、本草案で公開前検分の第一巡（系統外の二票・系統内の二票）の採否と登録者の裁定を反映した（`%s`）。'
    '機械の区画の中身と並びは草案1 と同じで、`tools/report_lint.py` が草案1 の区画の記録（`records/A/results-report-A-draft1-2026-09-17-machine.json`）と突合する（走査の違反の扱いは D-41 の歯止め・§8）。' % (TPL_SHA, ADOPT)])
replace('- 打ち込んだ数の一覧（`report_rules.typed_numbers`', [
    '- 打ち込んだ数の一覧（`report_rules.typed_numbers`・起草者が機械の区画の外に書いた数の型）: 日付・SHA16（凍結物と器材と記録・雛形の SHA16 %s を含む）・逸脱番号（D-33〜D-%d）・費用の実績（登録者申告の Colab の残高とその差・§2 の費用の印の行に一つずつ）。'
    'このほかの数は機械の区画の中だけにある（記録の名に含まれる数と、機種・場面・版・節の番号は、走査器が除く型）。' % (TPL_SHA, LEDGER_LAST)])

# ---- §0
replace('3. 走行の事実の一行（起草者の補い）', [
    '   - 走行の事実（起草者の補い）: 機種は Qwen3 の 0.6B・1.7B・4B・8B・14B・32B と錨 4B-2507。本走行と錨反復と橋のセッションの一覧と走行の期間（2026-09-16〜2026-09-17・日本時間）は `records/A/main/main-run-A.md` §2 の機械の表。'
    'API 再走行は「条件を満たす提供なし」（D-38）。'])
before('6. **札の内訳**（`print_strings.first_finding` の定型）', [
    '   - 上向きの確証の断り（起草者の補い・登録者裁定・§9）: 上の一行は主閾値の札による。正本の決まり（`censor.sensitivity_report`）により、主閾値の札を主とする。'
    '感度閾値のうち検閲の閾値を両端へ広げた側（censor.low を下げ、censor.high を上げた側）では確証になる対比が増え、そのうち %s は `report_rules.upward_rule` の定義に当たる。'
    'この二本の主閾値の札は、%sである。感度閾値の下で残った規模は、どちらも連続でないか端を欠く（読み条項 (xii)）。'
    'この事実は機械の区画には無く、公開前検分の第一巡の再現の記録（`%s`）で、凍結した集計器の関数から出し直した。感度閾値の対比ごとの札と傾きと上向きの判定を、集計器は印字しない。'
    '腕を効き目順に並べず、上昇を招く操作の手順は書かない（凍結 §2.15）。' % (UP_TEXT, UP_MAIN, VERIF)])
replace('   - 様式転位の判定保留に回った対比では、破局率の差を', [
    '   - 様式門の hold の旗が立った対比では、破局率の差を応答様式の差と分離できない（凍結 §3 (ii)・§3 の様式門の機械の区画・§4 の並記表）。'
    '旗は、様式転位の判定保留に回った対比のほか、解釈条項の札の対比（§3 の降格・保留の三行で、理由に様式門の旗がある行）と、非有意の札の対比（%s）にも立つ。'
    '条項 (ii) は札ではなく「分離できない場合」を条件にするので、旗で見る。' % NS_HOLD_TEXT])
replace('   - 検査認識の言及率（語彙の機械計数）が半分以上のセルがある', [
    '   - 検査認識の言及率（語彙の機械計数）が半分以上のセルがある（凍結 §3 (vii)・§6 の機械の表）。閾値は登録に無く、半分は起草者が率を見た後に置いた目安である。'
    '機種は規模の順、錨は最後に並べる: %s。確証の一本（S4 の Onull 対 N）の言及率は、§4 の確証の一本の段落に書く。' % HALF_TEXT])

# ---- §1
replace('- 選択規則の読み（正本 `reading_selection`・凍結 §3 (xvi)・起草者の記入）', [
    '- 選択規則の読み（正本 `reading_selection`・凍結 §3 (xvi)・起草者の記入）: 測れた効果種（Lneg 対 Onull・Onull-Ncold 対 Onull）のどの対比にも確証の札は立たなかった。これを「傾向が立たなかった」と言い換えない。',
    '  - 測れた対比は S1 の Lneg 対 Onull だけで、その札は初めの段（β₃ の Holm）の非有意である（測れた対比の出所は §7 の到達の区画・札は §4 の並記表）。Onull-Ncold 対 Onull には測れた対比が無く、選択規則の読みを書ける場面が無い。',
    '  - この対比には、読みを左右しうる事実が機械の区画にある。処置腕 Lneg は残った三規模とも天井（censor.high を超える）にある（§4 の破局/n）。並記表の同じ行に、解釈条項の発火と様式門 hold の旗が立ち、定型文の区画に様式の差の大きさがある。'
    'pt 差の傾きは強く立っている（並記表）。到達の模擬（§7）は、この対比の解釈条項の発火を両向きとも零と見込んでいたが、実測の配置はこの前提と違う。',
    '  - 札は規則どおりである（解釈条項は後の段にしか効かない）。この非有意は、処置腕が天井にある配置での対数オッズの交互作用の非棄却であり、「傾向が無い」とも「傾向がある」とも読まない。'
    '同じ配置は S4 の Lneg 対 Onull にもある。§4 の札 × 状況の表の非有意の読み文（検出域の外でありうる）は、この二本では、この配置の断りと並べて読む。',
    '  - 測れた効果種の中で、二つの Holm に棄却されて解釈条項に回った三対比（%s）を、正本 `reading_selection` の前提「どの測れた効果種にも傾向が立たず」にどう数えるかは、正本にも凍結本文にも定めが無い。'
    '段階 A の本報告では決めず、段階 B の設計（凍結の前）で登録者が決める（登録者裁定・`%s` の裁定の結果）。' % (THREE_TEXT, ADOPT),
    '  - 正本の規則では、段階 A 単独では帰無の図を主図に置く。規模に依らないという読みは、上の数え方を決めた上で段階 B の結果と合わせて書き、そのときも S1 の Lneg 対 Onull に限り、測れた対比でない場面と効果種に広げない。'])

# ---- §2
after('- 環境（起草者の補い）: GPU の型とメモリ', [
    '- 環境の区画の断り（起草者の補い）: 上の機械の区画は、tag ごとに一つの走行キーの GPU だけを出す。橋の tag では A100 側（4B）の走行キーだけが出ており、L4 側（8B）の走行は `records/A/main/main-run-A.md` §2 の表にある。',
    '- 非思考の確かめ（起草者の補い）: 手元の走行（本走行・錨反復・橋・校正腕）の全試行で、走行器の記帳 `reasoning_chars` が零だった（`records/A/main/aggregation-plan-A.md` §8）。'
    '本走行の応答様式の記録の `<think>` の列も全セルで零（§6 の機械の表）。事業者の API の走行は、この記帳で思考していたと分かり（下見では本文の印だけを数えて見落とし、本番の途中で気づいた）、集計に入れていない（D-38）。'])
replace('- 抽出検査（起草者の補い）: 標本と封印を目視の前にコミットして公開し', [
    '- 抽出検査（起草者の補い）: 標本と封印を目視の前にコミットして公開し、目視の分類を対応表を開く前にコミットし、その後に照合した（順はリポジトリの履歴で確かめられる）。'
    '食い違った件は、照合の前に書いた「先頭の途中で切れて JSON の始まりが見えない件」と同じだった（`records/A/sampling-inspection-A-stageA.md`・`records/A/sampling-inspection-A-stageA-after.md`・`records/A/sampling-inspection-A-stageA-agreement.md`）。'
    'パイロットの抽出検査は行っていない（D-37）。'])
replace('- 率盲検の事前拘束と開示（起草者の記入）', [
    '- 率盲検の事前拘束と開示（起草者の記入）: 段階 A は run-log を置いていない。事前拘束は凍結本文 §0-8 と、走らせる前にコミットした段取り `records/A/main/main-plan-A.md` §8 の末尾に書いた。'
    'コーディネータの目に入ったものは `records/A/main/main-run-A.md` §8 と `records/A/main/aggregation-plan-A.md` §1-5 に列挙した。腕ごとの率は、集計の器を走らせた時点（2026-09-17）で初めて読んだ。'
    'ただし、抽出検査の標本の本文の先頭（選択を含む）は、その前に目に入っている（伏せた標識の下で、本文から場面は分かり、腕も推し量れる件があった・§10）。'])

# ---- §3
replace('- 門0.5 の記録（起草者の補い）', [
    '- 門0.5 の記録（起草者の補い）: 集計と本報告の組み立てには、凍結物の記録を凍結した器と正本で作り直した `records/A/main/identity-screen-A-regen-2026-09-17.json` を使った（D-40・凍結物の記録と、正本の SHA16 と作成時刻のほかは一致）。'
    '冒頭の前提の区画の門0.5 の記録の SHA16 は、この作り直した記録のもの（%s）で、凍結物の記録 `records/A/identity-screen-A.json` の SHA16 は %s。' % (ID_REGEN_SHA, ID_FROZEN_SHA)])
before('- 校正腕と撤退条件（機械の転記', [
    '- 門2 の区画の断り（起草者の補い）: 上の区画の対比ごとの数は、パイロットの率で数えた残存規模の数である（門の記録 `records/A/gate-pilotA.json`）。§4 の並記表の本走行の残存規模とは違う。'])
before('### 降格・保留の三行', [
    '- 散文層の副次終点の行と場面の対応（起草者の補い）: 上の区画の散文層の行には場面の名が無い（正本の定型に場面の置き字が無い）。'
    '行は上から次の順に並ぶ（機械集計の JSON の散文層の欄の対比の並びと、公開前検分の第一巡の再現の記録で確かめた）: %s。N2 の行は無い。' % MAP_TEXT,
    '- 確証の一本（S4 の Onull 対 N）は様式門が none なので、正本の決まり（`style_gate.stratified.applies_to`）により散文層の行を持たない。S1 と SK の Onull 対 N の行は、確証の一本の行ではない。',
    '- 散文層の当てはめが判定不能に落ちた対比（%s）は、機械集計の md の散文層の節にだけ対比の名つきで出ており、組み立て器は区画に写していない（§9）。' % UND_TEXT,
    ''])
replace('- 規模間の差の推定の幅は設計事実の転記行 O', [
    '- 規模間の差の推定の幅は設計事実の転記行 O（`records/A/design-facts-A.md`）に置いた。自動の保留規則は置かない。',
    '- 判定器の範囲と読み方（起草者の補い）: 判定器の妥当性は全機種・全場面で測った（断片はパイロットの標本から取った・凍結 §2.11）。'
    '方向別の誤判定率が出ていないセルは、機械が破局とした対が無い %s と、機械が非破局とした対が無い %s である（上の表の「—」）。'
    'κ は、判定者が読み取った応答の最終の決定（選択肢の記号など）から決まる破局の判定と、機械の判定の一致である（正本 `judge_validity.extract`・§9）。' % (BLANK_CAT, BLANK_NON)])

# ---- §4
before('- 区間の被覆（`print_strings.interval_note`', [
    '- 残った規模の内訳の読み方（起草者の補い）: 並記表の「検閲」と「測定不能」の数は、同じ規模を両方に数えることがある（例: S4 の Onull 対 N の 0.6B は、両腕とも床の検閲で、N が測定不能でもある）。外れた規模は、残った規模の欄から読む。'])
before('- 残存規模の非連続と端の欠けの注（機械の転記', [
    '- 定型文の区画の読み方（起草者の補い）: 正本の様式の定型は一つで、保留の帯を超えた大きさにも「注の帯を超えた」と印字される。帯の判定は §3 の様式門の区画による。'
    '非有意で、様式門と環境の旗も無い対比（%s）は定型文を持たないので、この区画に行が無い。' % '・'.join(name(i) for i in NO_STR)])
replace('- 確証の一本（起草者の記入）: S4 の Onull 対 N だけが確証に残った', [
    '- 確証の一本（起草者の記入）: S4 の Onull 対 N だけが確証に残った（機械の区画の定型文）。残った規模（%s）は非連続で端を欠くので、直線を主張しない（凍結 §3 (xii)・機械の区画の注）。'
    'この一本の読みの範囲を決める事実を、区画と表を指して並べる。' % '・'.join(kept),
    '  - 応答様式の層との重なり: 残った三規模は、両腕とも JSON 直答が無いセル（§6 の表の (b) が零）である。外れた三規模（%s）は、両腕とも JSON 直答だけのセル（(b) が一）で、率は床か天井（§4 の破局/n）である。'
    '残存の偏り（読み条項 (xii)）が、応答様式の層と重なる。' % '・'.join(drop),
    '  - 様式差と層別の副次（D-42）: 凍結本文 §2.6 は、この型の確証札の段落に、様式差と順位の機械印字と層別の副次を求める。正本と組み立て器には実装が無く、区画に出ていない。'
    '残った規模では両腕とも JSON 直答が無いので、様式の差は零である。両腕の試行はすべて散文の層にあり、散文層の当てはめは主の当てはめと同じデータになる（`records/A/style-stageA.json` の層の件数）。「順位」の定義は正本に無い。',
    '  - 環境との重なり: 残った規模のうち L4 側は 4B だけで、14B と 32B は A100 側である（§2 の環境の区画）。差の符号が変わる臨界規模は 14B（§5 の臨界規模の表）で、環境の境目と同じ位置にある。'
    '環境保留の規則には当たらないが、橋は N1 だけで測ったので、この対比の環境の読みは外挿である（読み条項 (xiii)）。',
    '  - 言及率: 4B の N は §0 の言及率が半分以上のセルに入り、4B の Onull は目安の下にある。14B と 32B では両腕とも目安の下で、32B では腕の間に差がある（§6 の表の S4 の行）。',
    '  - 感度閾値: この一本の札は、二つの感度閾値のどちらでも変わらない（上の表の変わった対比に無い）。感度閾値で確証の本数が動くのは、ほかの対比の札が変わるためである（§0 の上向きの確証の断り）。',
    '  - 飽和までの近さ: 対照腕 N は残った規模の一つ（14B）で飽和の域にあり（§4 の破局/n）、解釈条項の発火（二規模以上）まで一規模の差である。',
    '  - 資料: レシピ対の S4 の N と Onull の行（§6）を、読み条項 (xi) の資料として指す。4B-2507 を並びの線に載せる読みではない。',
    '  - 札は主閾値のものを主とする。'])

# ---- §5
before('### 臨界規模（記述・凍結 §2.5', [
    '- 床持続の区画の読み方（起草者の補い）: 「棄却域を外れた規模」の欄には、測定不能の規模も入る（器の数え方・例: %s）。測定不能の規模は上限を計算せず、「全規模で上限が censor.low 未満」を満たさない側に数える。' % FLOOR_EX,
    ''])

# ---- §6
replace('- スタック差（起草者の補い）', [
    '- スタック差（起草者の補い）: API 再走行は「条件を満たす提供なし」として扱い（D-38）、スタック差は記述しない。上の機械の区画の「記録なし」はこの扱いによる。'
    '事業者の API の走行は思考モードで生成されており、スタックの差に思考の有無が重なるので、その記録を手元の走行と比べない。集計にも入れていない（`results/excluded-stageA-api-thinking-2026-09-17/`・`records/A/main/api-rerun-run-A.md`）。'])
after('- 記述であり場面を格付けしない。', [
    '- 圧の内訳の表の読み方（起草者の補い）: 表の見出しの「凍結の表」は雛形の文言で、表そのものは凍結本文に無く、内部の計画案にある（記録の冒頭）。'
    '出典の表には場面を比べる最上級の語があるが、出典の文言であり、本報告の読みに用いない（読み条項 (vi)）。'])

# ---- §7
replace('- 照合の記録（起草者の補い）', [
    '- 照合の記録（起草者の補い）: 欄ごとの予想と実測と結果の全行は、照合の記録の JSON（`records/A/predictions-check-A.json`）にある。md（`records/A/predictions-check-A.md`）の表は的中の行を載せていない。'
    '照合に使ったのは登録者の第二版（拘束版）とコーディネータの封印で、第一版は非拘束の記録なので照合に入れていない。照合は記録であり評価ではない。照合の器の規則（正本 `predictions.compare_rules`）を、起草者は照らし合わせていない（§9）。'])

# ---- §8
replace('- 凍結物の検証（起草者の補い）', [
    '- 凍結物の検証（起草者の補い）: 凍結マニフェスト `records/freeze-A-2026-09-16.json` の全ファイル（盤・台帳・正本・器材・雛形を含む）の SHA16 を、集計の前と後と草案の組み立ての前に照合した（`records/A/main/freeze-verify-2026-09-17.json`）。'
    '本草案の反映の前と後の照合は、公開前検分の第一巡の記録（`%s/verify.log`）。正本の SHA16 は %s、凍結本文の SHA16 は %s。' % (R1, CANON_SHA, DESIGN_SHA)])
replace('- 逸脱台帳（`records/DEVIATIONS.md`）', [
    '- 逸脱台帳（`records/DEVIATIONS.md`）: 段階 A の凍結の後は D-34〜D-%d。' % LEDGER_LAST
    + 'パイロットの D-34（撤退条件の暫定の判定）・D-35（ダウンロードの常設の許可）・D-36（ランタイムの操作の委任）、本走行と橋の D-43（A100 のセッションの順番の変更）・D-44（橋 4B を同じセッション番号で走らせ直した）、'
    '本走行の後の D-37（パイロットの抽出検査を行わない）・D-38（API 再走行は条件を満たす提供なし）・D-39（コーディネータの器の説明の誤り）・D-40（集計の器に渡す門0.5 の記録の作り直し）、'
    '報告の段の D-41（走査器が機械の区画の中の括弧を埋め残しに数える件の扱いと歯止め）・D-42（凍結本文 §2.6 の確証札の段落の様式差と層別の副次が器に無い）。凍結の前の Firth の一致検査の D-33 も並べる。率盲検の事前拘束とその開示は §2。',
    '- 走査と歯止め（起草者の補い）: 本草案は、凍結した走査器で違反が残る（機械の区画の中の括弧）。雛形の公開の条件（走査器が違反も埋め残しも無しに終わること）は満たさず、'
    'D-41 の歯止め（器 `records/A/main/report_lint_guard_A.py`・記録 `records/A/main/report-lint-guard-draft4-2026-09-17.json`）の通過に依って公開する。歯止めの見る範囲と、登録した文字列の性格は §9。'])

# ---- §9
cl_new = {
    '  - (ii) 適用:': '  - (ii) 適用: 様式門の hold の旗が立った対比（様式転位の札のほか、解釈条項と非有意の札の対比を含む）では、破局率の差を応答様式の差と分離できない。その旨を §0 の札の内訳の直後に置いた。確証の一本では、残存の偏りが応答様式の層と重なる（§4）。',
    '  - (vii) 適用:': '  - (vii) 適用: 言及率が半分以上のセルを §0 の先頭に列挙した（半分は率を見た後の起草者の目安）。確証の一本の言及率は §4 の段落に書いた。言及率は語彙の機械計数で、場面を跨いで比べない。',
    '  - (xii) 適用:': '  - (xii) 適用: 残存規模が非連続または端を欠く対比に注を付した（§4 の機械の区画）。確証の一本も残った規模が非連続で端を欠くので、直線を主張しない。感度閾値の下で上向きの規則の定義に当たる二本も、残った規模が非連続または端を欠く（§0）。',
    '  - (xiii) 適用:': '  - (xiii) 適用: 環境保留は発火していない。橋は 4B と 8B の二規模で、環境のずれが規模に依らないことは検定していない。環境差は N1 の腕だけで測り、他の場面へは外挿として読む。確証の一本では、差の符号が変わる規模が環境の境目と重なる（§4）。',
    '  - (xv) 適用:': '  - (xv) 適用: 判定器の妥当性は全機種・全場面で測った（範囲の外の機種は無い）。方向別の誤判定率が出ていないセルと κ の意味は、§3 と下の確認していないことに書いた。位置の記述は機械の区画。',
    '  - (xvi) 適用:': '  - (xvi) 適用: 測れなかった効果種（機械の区画）について「傾向が立たなかった」と書かない。測れた効果種でも、測れた対比（S1 の Lneg 対 Onull）でない場面について傾向の不在を書かない。解釈条項に回った三対比の数え方は未決（§1）。',
}
for pre, new in cl_new.items():
    replace(pre, [new])
replace('  - 適用: 橋の環境保留は発火していない。', [
    '  - 適用: 橋の環境保留は発火していない。発火していなくても、橋の 8B の L4 側では、環境の差と同時要求数の差（と pip freeze の差と時点の差）が交絡する。'
    '橋の 8B の壁時計は見込みを大きく上回った（`records/A/main/main-run-A.md` §6）。原因は調べていない。'])
i_nc = find('- **確認していないこと**（空欄不可')
j = i_nc + 1
while j < len(L) and L[j].startswith('  - '):
    j += 1
old_items = L[i_nc + 1:j]
assert len(old_items) == 14 and old_items[2] == '  - 判定器の妥当性の範囲の外の機種と場面。', old_items[2]
for k in range(i_nc + 1, j):
    put(k, ('del', None))
put(i_nc, ('after', [
    '  - 機種の並びに沿った変化を、訓練・後訓練・トークナイザの違いから分離すること。',
    '  - 環境のずれの規模依存性、同時要求数の効果、橋 8B のランタイムの pip freeze の差の効果（どの包みが違うかも特定していない）、橋 8B の壁時計が見込みを上回った原因。',
    '  - 判定器の方向別の誤判定率のうち、機械が破局とした対が無いセル（%s）と、機械が非破局とした対が無いセル（%s）の値。'
    '判定器の κ は、判定者が読み取った最終の決定から決まる破局の判定と機械の判定の一致で、決定の中身の是非の判定の一致ではない。断片はパイロットの標本で、本走行の試行ではない。' % (BLANK_CAT, BLANK_NON),
    '  - 測れなかった効果種の傾向と、測れた対比でない場面の傾向。',
    '  - 測れた効果種の中で解釈条項に回った三対比を、選択規則の前提にどう数えるか（段階 B の設計で登録者が決める・§1）。',
    '  - 感度閾値の対比ごとの札と傾きと上向きの判定（集計器が印字しない）。感度閾値のうち検閲の閾値を両端へ広げた側で上向きの規則の定義に当たる二本（%s・§0）は、'
    '公開前検分の第一巡の再現の記録で出し直したもので、機械の区画には無い。正本の決まりにより、主閾値の札を主とする（この二本の主閾値の札は §0）。' % UP_TEXT,
    '  - 並記表の区間の族全体の同時被覆。',
    '  - 言及率は語彙の機械計数であり、内容の判定ではない。',
    '  - 破局率の分母は n_ok で、書式外の試行は分母に入り、破局に数えない（正本の検閲の分子と分母）。測定不能の閾値の内側の書式外があるセルでは、その分だけ率が低めに出うる。'
    '本報告は、本走行の書式外がどのセルにどれだけあるかを並べていない（走行ごとの件数は整合検査の記録）。',
    '  - スタック差（API 再走行は条件を満たす提供なし・D-38）と、事業者が配る重みの版。',
    '  - 圧の内訳の表の登録者の確認の最終の状態（出典の計画案の中に「確認を要する案」と「承認済みの台帳」の両方の記録がある・`records/A/main/pressure-breakdown-A.md`）。',
    '  - API 再走行の実際の請求額（登録者の画面）。',
    '  - 書式の再試行が起きた理由と件数（手元の走行の全体でも、除外した API の記録でも、理由を調べていない。抽出検査の標本に区切りを含む件がある。API の記録の再試行の件数は `records/A/main/api-rerun-run-A.md` の表）。',
    '  - 抽出検査での伏せの破れの程度（腕推測の記録は取っていない）。',
    '  - 本草案の反映（公開前検分の第一巡の採否と登録者の裁定）についての外の目による確認（第一巡の四票は草案3 を見た）。',
    '  - 走査器が見ない種類の誤り（機械の区画の中の数の当否と、読みの当否）。',
    '  - 歯止め（D-41）の見ない範囲。歯止めは組み立て器の出力どうし（草案と草案1 の区画の記録）を突き合わせ、集計器から区画への写しは見ない。'
    '組み立て器は、判定不能の散文層の行を区画に写さず、refuse 門の列の文言を、集計器の md の「当てた・保留なし」から「保留なし」に変えている。'
    '登録した文字列は草案1 の出力を見た後に登録したもので、一つは確証の区間の値を含む（D-41 の書き足し）。',
    '  - 走査器が除く数の型は、正本 `report_rules.typed_numbers` の文言より広い（時刻とコミットの短い名も除く）。本草案は、機械の区画の外に時刻とコミットの短い名を打っていない。',
    '  - 照合の器の規則（正本 `predictions.compare_rules`）と、照合の記録の md の書式（重なった語と、零か一かの欄の書き方）。',
    '  - 計画 §7 の語の一覧による照合（一覧が公開の記録に無い）。',
]))

# ---- §10
i10 = find('- 対象: 段階 A の結果報告の草案3')
k = i10
repl10 = {
    '- 対象:': '- 対象: 段階 A の結果報告の草案4（草案1 の機械組み立てに起草者が記入し、公開前検分の第一巡の採否と登録者の裁定を反映した）。',
    '- 敵対的検分:': '- 敵対的検分: 機械の区画の外に数を書かず、数の要る欄は機械の区画と一次記録を指した。確証の一本の読みを、定型と残存規模の注と、区画と表で確かめた事実に限った。予想の照合を読みの根拠に引いていない。'
                     '走査器の違反を種類ごとに確かめた。第一巡の四票の所見は、凍結の器の関数と一次記録で出し直してから採否を決めた（再現の記録）。反映は器で確かめた（反映の確かめの記録）。',
    '- 系統の内訳:': '- 系統の内訳: 草案の起草は Claude 系（コーディネータ）。公開前検分の第一巡は、系統外（Gemini 3.8 Flash 二名）と系統内（claude.ai の Claude Opus 5 二名・起草者と同一系列で一票）で、全票が条件つき。本草案の反映は外の目を通っていない。',
    '- COI 記録:': '- COI 記録: 引かれた向き——確証の一本を大きく読みたい、または小さく読みたい。自分の封印予想の結果を読みに寄せたい。自分の過失を小さく書きたい。感度閾値の上向きの二本を目立たない所に置きたい、または主閾値の札より前に出したい。'
                  '置いた印——札は雛形の定型だけで書いた。照合は定型のまま転記した。過失は §2・§8 と各記録に書いた。二本の文は、主閾値の札を主とする句を前に置き、§0 と §9 に置いた（登録者裁定）。',
    '- 判定:': '- 判定: 登録者に提出できる水準（第一巡の反映は外の目を通っていない）。',
}
seen = set()
while k < len(L) and L[k].startswith('- '):
    for pre, new in repl10.items():
        if L[k].startswith(pre):
            put(k, ('rep', [new])); seen.add(pre)
    k += 1
assert seen == set(repl10), set(repl10) - seen

# ---- 組み立て
out = []
for i, l in enumerate(L):
    op = ops.get(i)
    if op is None:
        out.append(l)
    elif op[0] == 'del':
        continue
    elif op[0] == 'rep':
        if i not in OUT_SET:
            sys.exit('区画の中を置き換えようとした: %d' % i)
        out += op[1]
    elif op[0] == 'after':
        out.append(l); out += op[1]
    elif op[0] == 'before':
        out += op[1]; out.append(l)
final = []; in_m = False
for l in out:
    if MB['begin'] in l:
        in_m = True
    if not in_m and not l.strip() and final and not final[-1].strip():
        continue
    final.append(l)
    if MB['end'] in l:
        in_m = False
TEXT = '\n'.join(final)
assert RL.blocks(TEXT, T) == RL.blocks('\n'.join(L), T) or [b for _, b in RL.blocks(TEXT, T)] == [b for _, b in RL.blocks('\n'.join(L), T)], '区画の中身が変わった'
if os.path.exists(D4) and '--force' not in sys.argv:
    sys.exit('既にある（上書きしない）: %s' % D4)
open(D4, 'w', encoding='utf-8', newline='\n').write(TEXT)
side = json.load(open(SIDE1, encoding='utf-8'))
tpl = frozenset(open(os.path.join(REPO, 'records', 'A', 'results-report-template-A.md'), encoding='utf-8').read().replace('\r\n', '\n').split('\n'))
V = RL.lint(TEXT, T, tpl, sidecar=side)
kinds = collections.Counter(v['kind'] for v in V)
print('[draft4] %s（%d 行）・違反 %d %s' % (D4, TEXT.count('\n') + 1, len(V), dict(kinds)))
for v in V:
    print('  %s L%d %s | %s' % (v['kind'], v['line'], v['token'], v['context'][:90]))
