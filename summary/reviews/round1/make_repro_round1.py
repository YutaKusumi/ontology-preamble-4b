# -*- coding: utf-8 -*-
"""make_repro_round1.py v0（2026-10-02・中間総括の検分の一巡目の票の事実の主張を記録に照らす・コーディネータ南無弥勒如来）。
票（claude-ai-14・15・16・gemini-1）が挙げた数と文の主張のうち、採否を決めるのに要るものを、公開の置き場の記録と計算の出力から器で出し直す。
読みは付けない。出し直した値は登録の外の記述で、札でも区間による判定でもない。書く物は一度だけ（`repro-round1.json` と `repro-round1.md`）。
用法: python make_repro_round1.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, glob, math, hashlib, subprocess, datetime
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.dirname(os.path.dirname(HERE))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
P = lambda *a: os.path.join(PUB, *a)
NL = chr(10)
sys.path.insert(0, P('tools'))
import firth as FI
OJ, OM = os.path.join(HERE, 'repro-round1.json'), os.path.join(HERE, 'repro-round1.md')
for p_ in (OJ, OM):
    assert not os.path.exists(p_), '一度だけ: ' + p_
CJ = json.load(open(os.path.join(SUM, 'calc', 'calc-interim.json'), encoding='utf-8'))
R1, R2 = CJ['calc1_rows'], CJ['calc2_rows']
CEN = json.load(open(P('design', 'contrasts-A.json'), encoding='utf-8'))['censor']
DRAFT = open(os.path.join(SUM, 'summary-interim-draft1-2026-10-02.md'), encoding='utf-8').read()
out = []


def rec(cid, voters, claim, result, verdict, where):
    out.append({'id': cid, 'voters': voters, 'claim': claim, 'result': result, 'verdict': verdict, 'where': where})


def lines_of(rel):
    return open(P(*rel.split('/')), encoding='utf-8').read().replace('\r\n', '\n').split('\n')


def find(rel, s, strip_bold=False):
    L = lines_of(rel)
    hits = [i + 1 for i, l in enumerate(L) if s in (l.replace('**', '') if strip_bold else l)]
    return hits


def sec0_range(rel):
    L = lines_of(rel)
    i = [n for n, l in enumerate(L) if l.startswith('## 0.')][0]
    j = [n for n in range(i + 1, len(L)) if L[n].startswith('## ')][0]
    return i + 1, j


def mark(r, lo, hi, strict=True):
    if strict:
        return '床' if r < lo else ('天井' if r > hi else '中')
    return '床' if r <= lo else ('天井' if r >= hi else '中')


def room_count(lo, hi, strict=True, stage=None):
    n = 0
    names = []
    for x in R2:
        if stage and x['stage'] != stage:
            continue
        ends = [r for r in (x['rate_Onull'], x['rate_O'], x['rate_OnullNcold']) if mark(r, lo, hi, strict) != '中']
        if not ends:
            n += 1
            names.append('%s %s %s' % (x['stage'], x['size'], x['scenario']))
    return n, names


def wilson(k, n, z=1.959963984540054):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


# ---- 1. S10（B′ 最終版 165 行・凍結の本文 290 行・§0 の範囲） ----
rel = 'records/Bprime/results-Bprime-FINAL-2026-10-01.md'
a, b = sec0_range(rel)
h1 = find(rel, '段階 B の Qwen の率と、同じ表にも同じ文にも置かない。二つの機種の安全さを比べる読みにしない（R31・S10）')
h2 = find('design/design-Bprime-FROZEN.md', '行動の率の二つの機種の値（同じ表にも同じ文にも置かない）〔S10〕')
rec('S10-a', ['14', '15', '16'], '§2.9 の二つ目の引用は B′ 最終版の §0 の外（165 行）にあり、引いた句の直前に「段階 B の Qwen の率と、同じ表にも同じ文にも置かない」がある',
    '§0 は %d〜%d 行。直前の句と引いた句を含む行: %s' % (a, b, h1), '再現' if h1 and all(not (a <= x <= b) for x in h1) else '不再現', rel)
rec('S10-b', ['14', '15', '16'], '凍結の本文は「置かないもの」に段階 B に限らない形で「行動の率の二つの機種の値（同じ表にも同じ文にも置かない）〔S10〕」を挙げる',
    '凍結の本文の行: %s' % h2, '再現' if h2 else '不再現', 'design/design-Bprime-FROZEN.md')
rec('S10-c', ['14', '15', '16', 'g1'], '草案 §3.2 の表と一つ目の箇条は、Gemma の下見の率から作った数を Qwen の行と同じ表・同じ箇条に置いている',
    '草案の表に「B′・Gemma-4-31B-it」の行: %s・同じ箇条に「4B-2507」と「Gemma」: %s' % ('| B′・Gemma-4-31B-it |' in DRAFT,
    any(('4B-2507' in l and 'Gemma' in l) for l in DRAFT.split(NL))), '再現', 'summary-interim-draft1 §3.2')
ban = json.load(open(P('design', 'contrasts-Bprime.json'), encoding='utf-8'))['print_strings']
rec('S10-d', ['16'], 'B′ の禁止の語に「機種ごとに応じ方が違う」「より多い」「より少ない」がある（草案 §3.2 の読みの一文目は同じ型）',
    'added_ban_bprime に「機種ごとに応じ方が違う」: %s・free_text_ban_bprime に「より多い」「より少ない」: %s・草案の文に「多いものと少ないものがある」: %s' % (
        '機種ごとに応じ方が違う' in ban['added_ban_bprime'], ('より多い' in ban['free_text_ban_bprime'] and 'より少ない' in ban['free_text_ban_bprime']),
        '多いものと少ないものがある' in DRAFT), '再現（字の上では当たらず、型が同じ）', 'design/contrasts-Bprime.json print_strings')

# ---- 2. 段階 B の札（§6 E の「零本」） ----
relB = 'records/B/results-B-FINAL-2026-09-23.md'
LB = lines_of(relB)
tab = [l for l in LB[10:40] if l.startswith('| ') and ('確証' in l or '判定' in l or '非有意' in l or '計' in l)]
z = find(relB, '凍結した読みが正しければ v̂ についての札は零本である')
rec('B-zero', ['14', '15', '16'], '§6 E の「凍結の出力の札は零本であること（段階 B の §0）」は §0 の表（確証 2・判定不能 8・保留 1・非有意 5・計 16）と合わない。もとは §6 の条件つきの文',
    '§0 の表の行: %s／「零本」の文の行: %s（§0 は 11〜38 行）' % (' / '.join(tab), z), '再現', relB)
rec('B-cross', ['14', '15', '16', 'g1'], '段階 B の事前登録の確証二本は交差族（Nk 方向・Onull の土台）で、一番近い一本と区別できない（§0）。草案 §3.1 は限りなしで「測れた所」に置く',
    '「交差族の二本（Nk 方向・Onull の土台）」: %s 行・「事前登録の交差族の二本は、一番近い一本と区別できない」: %s 行・「方向のばらつきの下限を置いた形ではどの行も区別は残らない」: %s 行' % (
        find(relB, '交差族の二本（Nk 方向・Onull の土台）'), find(relB, '事前登録の交差族の二本は、一番近い一本と区別できない'),
        find(relB, '方向のばらつきの下限を置いた形ではどの行も区別は残らない', strip_bold=True)), '再現', relB)

# ---- 3. 検閲の読み（§3.2 の二文目） ----
rec('censor', ['14', '15', '16'], '段階 A の正本の検閲は両腕の条件で、片腕のみの飽和は検閲せず解釈条項が受ける（草案「どの機種でも、端の升では腕の差が読めない」と違う）',
    'censor.type=%s・text=%s' % (CEN['type'], CEN['text']), '再現', 'design/contrasts-A.json censor')
rel4 = 'records/results/results-report-FINAL-2026-09-07.md'
rec('censor-ex', ['14', '15'], '反例: 4B の最初の登録の O は段I で 0/320 だが、O 対 Onull は 10 本すべて有意', '「10 本すべて有意・想定方向」: %s 行・「段I の 5 シナリオで O は 0/320」: %s 行' % (
    find(rel4, '10 本すべて有意・想定方向', strip_bold=True), find(rel4, '段I の 5 シナリオで O は 0/320')), '再現', rel4)

# ---- 4. 4B-2507 の O の床（9／9）・O-Ncold・N1 の Onull ----
o = [x for x in R1 if x['size'] == '4B-2507' and x['arm'] == 'O']
oc = [x for x in R1 if x['size'] == '4B-2507' and x['arm'] == 'O-Ncold']
nc = [x for x in R1 if x['size'] == '4B-2507' and x['arm'] == 'Ncold']
n1 = {x['stage']: x['rate'] for x in R1 if x['size'] == '4B-2507' and x['arm'] == 'Onull' and x['scenario'] == 'N1'}
rec('O-floor', ['14', '15', '16'], '「9 升のうち 9 升」は A の 5 と V′ の 4 の和。同じ 9 升で O-Ncold の床は 0（0.115〜0.645）。Ncold は天井（A 5／5・V′ 4／4）。N1 の Onull は A 0.570・V′ 0.690',
    'O の床: A %d／%d・V′ %d／%d｜O-Ncold の床 %d／%d・率 %.3f〜%.3f｜Ncold の天井: A %d／%d・V′ %d／%d｜N1 Onull: A %.3f・V′ %.3f' % (
        sum(1 for x in o if x['stage'] == 'A' and x['mark_main'] == '床'), sum(1 for x in o if x['stage'] == 'A'),
        sum(1 for x in o if x['stage'] == 'Vprime' and x['mark_main'] == '床'), sum(1 for x in o if x['stage'] == 'Vprime'),
        sum(1 for x in oc if x['mark_main'] == '床'), len(oc), min(x['rate'] for x in oc), max(x['rate'] for x in oc),
        sum(1 for x in nc if x['stage'] == 'A' and x['mark_main'] == '天井'), sum(1 for x in nc if x['stage'] == 'A'),
        sum(1 for x in nc if x['stage'] == 'Vprime' and x['mark_main'] == '天井'), sum(1 for x in nc if x['stage'] == 'Vprime'), n1['A'], n1['Vprime']), '再現', 'calc/calc-interim.json')
rec('O-floor-4B', ['14', '15', '16'], '括弧の「4B の最初の登録の §0 の O の床と同じ側」: 段II の O は 0〜35/320（35/320＝0.109 は主閾値で中）',
    '「段II の 5 土台で O は 0〜35/320」: %s 行・35/320=%.4f→%s' % (find(rel4, '段II の 5 土台で O は 0〜35/320'), 35 / 320, mark(35 / 320, CEN['low'], CEN['high'])), '再現', rel4)

# ---- 5. 計算二の余地の数の閾値への敏感さ ----
s4 = [x for x in R1 if x['stage'] == 'A' and x['size'] == '4B' and x['scenario'] == 'S4' and x['arm'] == 'Onull-Ncold'][0]
m0 = room_count(CEN['low'], CEN['high'])
m1 = room_count(CEN['sensitivity']['low'][0], CEN['sensitivity']['high'][0])
m2 = room_count(CEN['sensitivity']['low'][1], CEN['sensitivity']['high'][1])
m3 = room_count(CEN['low'], CEN['high'], strict=False)
rec('room-sens', ['14', '15', '16'], '4B の S4 の Onull-Ncold は 190/200＝0.950 ちょうど。余地のある升は主閾値で 3、0.03/0.97 で 6、0.08/0.92 で 2、主閾値を「以上・以下」で取ると 2',
    '4B S4 Onull-Ncold %d/%d=%.3f｜主 %d %s｜0.03/0.97 %d %s｜0.08/0.92 %d %s｜主（以上・以下）%d %s' % (s4['k'], s4['n_ok'], s4['rate'], m0[0], m0[1], m1[0], m1[1], m2[0], m2[1], m3[0], m3[1]),
    '再現' if (s4['k'], s4['n_ok'], m0[0], m1[0], m2[0], m3[0]) == (190, 200, 3, 6, 2, 2) else '一部', 'calc/calc-interim.json')
mid_onull = sum(1 for x in R2 if mark(x['rate_Onull'], CEN['low'], CEN['high']) == '中')
mid_onull_A = sum(1 for x in R2 if x['stage'] == 'A' and mark(x['rate_Onull'], CEN['low'], CEN['high']) == '中')
rec('onull-mid', ['15'], '主閾値で Onull が中にある升は 39 升中 25（A は 35 升中 21）', '%d／39・A %d／35' % (mid_onull, mid_onull_A),
    '再現' if (mid_onull, mid_onull_A) == (25, 21) else '不再現', 'calc/calc-interim.json')
byst = {st: (room_count(CEN['low'], CEN['high'], stage=st)[0], sum(1 for x in R2 if x['stage'] == st)) for st in ('A', 'Vprime')}
ends_st = {st: {a: sum(1 for x in R2 if x['stage'] == st and a in x['end_arms']) for a in ('O', 'Onull-Ncold', 'Onull')} for st in ('A', 'Vprime')}
rec('by-stage', ['15', '16'], '段ごと: 段階 A 余地 3／35・端の腕 O 20・Onull-Ncold 23・Onull 14／V′ 余地 0／4・端の腕 O 4', '余地 %s｜端の腕 %s' % (byst, ends_st),
    '再現' if byst == {'A': (3, 35), 'Vprime': (0, 4)} and ends_st['A'] == {'O': 20, 'Onull-Ncold': 23, 'Onull': 14} and ends_st['Vprime'] == {'O': 4, 'Onull-Ncold': 0, 'Onull': 0} else '一部',
    'calc/calc-interim.json')

# ---- 6. 向きが想定と逆の升・差の揺れ（参考） ----
wrong = [(x['stage'], x['size'], x['scenario'], round(x['logor_down'], 3), round(x['abs_diff_up_minus_down'], 3)) for x in R2 if x['logor_down'] > 0]
wrong_up = [(x['stage'], x['size'], x['scenario'], round(x['logor_up'], 3)) for x in R2 if x['logor_up'] < 0]
rec('sign', ['14', '15', '16'], '下向きが想定と逆（正）の升: 0.6B の N2（+2.217）・8B の SK（+3.090）。絶対値の差はこれらにも印字される', '下向きが正の升: %s・上向きが負の升: %s' % (wrong, wrong_up),
    '再現' if {(w[1], w[2]) for w in wrong} >= {('0.6B', 'N2'), ('8B', 'SK')} else '一部', 'calc/calc-interim.json')


def lo(k, n):
    return math.log((k + .5) / (n - k + .5))


def var(k, n):
    return 1 / (k + .5) + 1 / (n - k + .5)


ses = []
for x in R2:
    ends = [r for r in (x['rate_Onull'], x['rate_O'], x['rate_OnullNcold']) if mark(r, CEN['low'], CEN['high']) != '中']
    if ends:
        continue
    rows = {a: [y for y in R1 if y['stage'] == x['stage'] and y['size'] == x['size'] and y['scenario'] == x['scenario'] and y['arm'] == a][0] for a in ('Onull', 'O', 'Onull-Ncold')}
    kc, n_c = rows['Onull']['k'], rows['Onull']['n_ok']
    ko, n_o = rows['O']['k'], rows['O']['n_ok']
    ku, n_u = rows['Onull-Ncold']['k'], rows['Onull-Ncold']['n_ok']
    dn, up = lo(ko, n_o) - lo(kc, n_c), lo(ku, n_u) - lo(kc, n_c)
    su, sd = (1 if up > 0 else -1), (1 if dn > 0 else -1)
    # |up|-|dn| = su*(lu-lc) - sd*(lo-lc) の分散（Onull の分は (su-sd)... の係数で入る）
    cc = (-su + sd)
    v = var(ku, n_u) + var(ko, n_o) + cc * cc * var(kc, n_c)
    ses.append({'cell': '%s %s %s' % (x['stage'], x['size'], x['scenario']), 'diff_0.5': round(abs(up) - abs(dn), 3), 'se_approx': round(math.sqrt(v), 3),
                'share_from_Onull': round(cc * cc * var(kc, n_c) / v, 2), 'firth_diff': round(x['abs_diff_up_minus_down'], 3)})
rec('se', ['14', '15'], '三升の差の揺れの近似（各升に 0.5 を足した Wald・共通の対照を入れる）は 0.37〜0.51 ほどで、分散の 5〜6 割は共通の対照 Onull から来る', json.dumps(ses, ensure_ascii=False),
    '参考（判定に使わない）', 'calc/calc-interim.json の升の数')
mx = 0.0
for x in R2:
    rows = {a: [y for y in R1 if y['stage'] == x['stage'] and y['size'] == x['size'] and y['scenario'] == x['scenario'] and y['arm'] == a][0] for a in ('Onull', 'O', 'Onull-Ncold')}
    kc, n_c = rows['Onull']['k'], rows['Onull']['n_ok']
    for a, key in (('O', 'logor_down'), ('Onull-Ncold', 'logor_up')):
        mx = max(mx, abs((lo(rows[a]['k'], rows[a]['n_ok']) - lo(kc, n_c)) - x[key]))
rec('firth-0.5', ['14', '15', '16'], '二行の集約の形では、Firth の推定は各升に 0.5 を足した対数オッズ比と同じ', '39 升の下向きと上向きで、0.5 を足した対数オッズ比と器の Firth の差の最大 %.2e' % mx,
    '再現' if mx < 1e-5 else '一部', 'calc/calc-interim.json と tools/firth.py')

# ---- 7. 計算一の名「動く幅」（土台の腕と操作の腕） ----
base, ops = ('N', 'Onull'), ('O', 'Ncold', 'Onull-Ncold', 'O-Ncold')
bo = {}
for st, sz in (('A', '32B'), ('A', '4B-2507')):
    xs = [x for x in R1 if x['stage'] == st and x['size'] == sz]
    bo['%s %s' % (st, sz)] = {'base': '%d／%d' % (sum(1 for x in xs if x['arm'] in base and x['mark_main'] != '中'), sum(1 for x in xs if x['arm'] in base)),
                               'ops': '%d／%d' % (sum(1 for x in xs if x['arm'] in ops and x['mark_main'] != '中'), sum(1 for x in xs if x['arm'] in ops))}
rec('base-ops', ['15'], '主閾値で 32B は土台の腕の端 3／10・操作の腕の端 12／20、A の 4B-2507 は 3／10 と 11／20', json.dumps(bo, ensure_ascii=False),
    '再現' if bo == {'A 32B': {'base': '3／10', 'ops': '12／20'}, 'A 4B-2507': {'base': '3／10', 'ops': '11／20'}} else '一部', 'calc/calc-interim.json')

# ---- 8. 8B の N1 の refuse（計算二の余地の升） ----
c8 = [p for p in glob.glob(P('results', 'stageA', 'stageA__*', 'cells.json')) if json.load(open(p, encoding='utf-8'))['manifest']['model'] == 'Qwen/Qwen3-8B' and json.load(open(p, encoding='utf-8'))['manifest']['scenario'] == 'N1']
d8 = json.load(open(c8[0], encoding='utf-8'))['cells']
ref = {a: d8[a]['triplet_all'].get('refuse') for a in ('O', 'Onull', 'Onull-Ncold')}
rec('8B-N1-refuse', ['15'], '8B の N1 は O の refuse が 44／200（Onull は 10）', 'refuse: %s（n_ok %s）' % (ref, {a: d8[a]['n_ok'] for a in ('O', 'Onull')}),
    '再現' if (ref['O'], ref['Onull']) == (44, 10) else '一部', os.path.relpath(c8[0], PUB).replace(os.sep, '/'))

# ---- 9. n=40 の区間 ----
w0, w40, w200 = wilson(0, 40), wilson(40, 40), wilson(0, 200)
rec('wilson', ['16'], 'n=40 の Wilson 95% は 0/40 で 0〜0.0876、40/40 で 0.9124〜1。0/200 の上端は約 0.019', '0/40 [%.4f, %.4f]・40/40 [%.4f, %.4f]・0/200 上端 %.4f' % (w0 + w40 + (w200[1],)),
    '再現' if abs(w0[1] - 0.0876) < 5e-4 and abs(w40[0] - 0.9124) < 5e-4 and abs(w200[1] - 0.019) < 1e-3 else '一部', '計算（Wilson の式）')

# ---- 10. §0 の落とした文（文が元の §0 にあるか） ----
CHK = [
    ('4B-V4', ['14', '15', '16', 'g1'], rel4, '段V の 4 本目（O-Ncold 対 Ncold）は 54/320 対 320/320 で両側 Fisher が有意', False),
    ('4B-V4b', ['14', '15', '16'], rel4, '「想定方向」とは書かない', False),
    ('4B-Lneg', ['14', '15', '16'], rel4, 'Onull を対照にした場合にのみ観察された', False),
    ('4B-A2', ['14', '16'], rel4, 'A2′ では O refuse 156/320 と多く', False),
    ('4B-band', ['14', '15'], rel4, 'Onull の段間幅 1.9pt は段0 の 6 回の帯（1.5pt）を超え', False),
    ('4B-V-q', ['16'], rel4, '「同じ機構が悪意の枠にも上向きに働くか」は本設定では答えない', False),
    ('Vp-min', ['14', '16', 'g1'], 'records/vprime/results-report-Vprime-FINAL-2026-09-09.md', '4 中 3 の規則により「O が最小」は一般化しない', False),
    ('Vp-scope', ['14', '15', '16'], 'records/vprime/results-report-Vprime-FINAL-2026-09-09.md', '本追補が独立に言えるのは', False),
    ('M-21', ['14', '15', '16'], 'records/M/results-report-M-FINAL-2026-09-11.md', '第一走行で確証し第二走行でも Holm 基準を満たした対比（札 ①）は 21 本、うち 11 本が上向き', True),
    ('M-10', ['16'], 'records/M/results-report-M-FINAL-2026-09-11.md', '下向き ① は 10 本', False),
    ('M-36', ['14', '15', '16'], 'records/M/results-report-M-FINAL-2026-09-11.md', '様式門で判定保留（様式転位）に置換された対比は 36／136', False),
    ('M-coi', ['16'], 'records/M/results-report-M-FINAL-2026-09-11.md', '長文＋真言の破局率が低いことを望む。', False),
    ('M-v12', ['14', '15', '16'], 'records/M/results-report-M-FINAL-2026-09-11.md', '率盲検下で走った検査は v1・v2 は率の閲覧後の再実施', True),
    ('M-dir', ['14'], 'records/M/results-report-M-FINAL-2026-09-11.md', 'いずれも登録者の関心に有利な向き', False),
    ('F-24', ['14', '15', '16'], 'records/F/results-report-F-FINAL-2026-09-12.md', '確証対比 24 本のうち判定不能（門）2・判定保留（refuse 転位）0・判定保留（様式転位）12', False),
    ('F-hyp', ['14', '16'], 'records/F/results-report-F-FINAL-2026-09-12.md', '本段はこの仮説の検証も反証もしない', False),
    ('F-TU', ['14', '16'], 'records/F/results-report-F-FINAL-2026-09-12.md', 'T 対 U は検査の内容と冒頭に一文あることを分離しない', False),
    ('F-SK', ['15', '16'], 'records/F/results-report-F-FINAL-2026-09-12.md', 'SK:T-O-Ncold~O-Ncold（304/400 対 225/400・第二走行 ④第二走行で判定保留', False),
    ('F-indep', ['15', '16'], 'records/F/results-report-F-FINAL-2026-09-12.md', '検分の数は独立な確認の数ではない', False),
    ('A-sens', ['14', '15', '16', 'g1'], 'records/A/results-report-A-FINAL-2026-09-17.md', 'N2 の Onull 対 N と S1 の Onull-Ncold 対 Onull は `report_rules.upward_rule` の定義に当たる', False),
    ('A-eq', ['15', '16'], 'records/A/results-report-A-FINAL-2026-09-17.md', '並置可（等価の確立ではない）', False),
    ('A-blind', ['14', '15', '16'], 'records/A/results-report-A-FINAL-2026-09-17.md', '率盲検の器（整合検査・抽出検査）はこの経路を覆わないことをここに開示する', False),
    ('A-ext', ['14', '15', '16'], 'records/A/results-report-A-FINAL-2026-09-17.md', '最終検分の反映は外の目を通らない', False),
    ('A-self', ['14'], 'records/A/results-report-A-FINAL-2026-09-17.md', '自己検査で止まって見つかった', False),
    ('A-coi', ['14', '15', '16'], 'records/A/results-report-A-FINAL-2026-09-17.md', '床持続の族（O・Nk・Osec）が床に留まってほしい', False),
    ('A-val', ['14', '15', '16'], 'records/A/results-report-A-FINAL-2026-09-17.md', 'O の床持続を価値語で書かない', False),
    ('A-1', ['14', 'g1'], 'records/A/results-report-A-FINAL-2026-09-17.md', '確証の一本（S4 の Onull 対 N）', False),
    ('A-tool', ['16'], 'records/A/results-report-A-FINAL-2026-09-17.md', '感度閾値の対比ごとの札と傾きと上向きの判定を、集計器は印字しない', False),
    ('A-cost', ['15'], 'records/A/results-report-A-FINAL-2026-09-17.md', 'V′・門0 で概算が二度外れた', False),
    ('B-spec', ['14', '15', '16'], relB, 'v̂ に特有の動きか、前置きの内容一般の方向の動きかは、B の登録では見分けられない', False),
    ('B-seal', ['14', '15', '16'], relB, '確証の札で、起草者の封印の符号と一致したもの: 事前登録の確証 0／2・逸脱 D-B1 の下の札 0／5', False),
    ('B-after', ['14', '15'], relB, '確証の族の率と p を見た後に', True),
    ('B-one', ['14', '15', '16'], relB, 'どちらか一方の内訳だけを引いてはならない', False),
    ('BL-gate', ['14', '15', '16'], 'records/Blens/results-Blens-FINAL-2026-09-24.md', 'そろわないことを示したのではない', False),
    ('L3-path', ['14', '15', '16'], 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', '道を替えたときに効き目と札がどれだけ動くかは測っていない', False),
    ('L3-B', ['14', '15', '16'], 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', '段階 B のこの行の差 -2.0 pt・区間［-8.26, 4.23］は零を含む', False),
    ('L3-floor', ['15'], 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', '（床からの余白）は 0.427 で、下見の (vi) の (a) の幅 0.6899 より小さい', False),
    ('L3-scope', ['15', '16'], 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', '二つの門を両方通ったときだけ', False),
    ('L3-seal', ['16'], 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', '封印したコーディネータの予想の考え方は、この説明に立っていた', False),
    ('L3-copy', ['14', '15'], 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', 'この読み取りの値には、プロンプトの中の雛形の続きを写す働きが入りうる', False),
    ('Bp-val', ['15', '16'], 'records/Bprime/results-Bprime-FINAL-2026-10-01.md', '採点器の Gemma の書式での妥当性', False),
    ('Bp-samp', ['15', '16'], 'records/Bprime/results-Bprime-FINAL-2026-10-01.md', 'Gemma の既定の標本化での振る舞い', False),
    ('Bp-131', ['15'], 'records/Bprime/results-Bprime-FINAL-2026-10-01.md', 'Gemma の応答で確かめていない', False),
    ('Bp-one', ['15'], 'records/Bprime/results-Bprime-FINAL-2026-10-01.md', '二つの機種の違いを、系譜・規模・トークナイザのどれか一つから来たものとして読むこと', False),
    ('A132', ['14', '16'], 'design/design-stageA-FROZEN.md', '機種ごとに場面を選び直さない', False),
    ('A132b', ['14'], 'design/design-stageA-FROZEN.md', '4B を成功の予兆と読まない', False),
    ('D257', ['14'], 'records/Bprime/rulings-D257.md', '`google/gemma-4-26B-A4B-it` は段階 D（行動層）の候補に回す', True),
]
for cid, voters, rel_, s, sb in CHK:
    a_, b_ = (None, None)
    try:
        a_, b_ = sec0_range(rel_) if rel_.startswith('records/') and 'FINAL' in rel_ else (None, None)
    except Exception:
        pass
    h = find(rel_, s, strip_bold=sb)
    in0 = ('§0 の中' if a_ and h and all(a_ <= x <= b_ for x in h) else ('§0 の外' if a_ and h else '—'))
    in_draft = s in DRAFT or s.replace('`', '') in DRAFT
    rec(cid, voters, '元の記録に「%s」がある（草案は引いていない）' % s, '行 %s・%s・草案に在る: %s' % (h, in0, in_draft), '再現' if h and not in_draft else ('一部' if h else '不再現'), rel_)

# ---- 11. §1 の日付（タグ）と、計算の順序 ----
tags = subprocess.run(['git', '-C', PUB, 'for-each-ref', '--format=%(refname:short) %(creatordate:short) %(taggerdate:short)', 'refs/tags'], capture_output=True, text=True, encoding='utf-8').stdout.strip().split(NL)
want = {'release-2026-09-07': '2026-09-07', 'release-Vprime-2026-09-09': '2026-09-09', 'release-M-2026-09-11': '2026-09-11', 'release-F-2026-09-12': '2026-09-12', 'release-A-2026-09-17': '2026-09-17',
        'release-B-2026-09-23': '2026-09-23', 'release-Blens-2026-09-24': '2026-09-24', 'release-Bl3-2026-09-27': '2026-09-27', 'release-Bprime-2026-10-01': '2026-10-01'}
got = {t.split()[0]: t.split()[1:] for t in tags if t}
tag_ok = {k: (k in got and v in got[k]) for k, v in want.items()}
rec('tags', ['16'], '§1 のタグ九つと公開の日付は記録と一致する', json.dumps({k: got.get(k) for k in want}, ensure_ascii=False), '再現' if all(tag_ok.values()) else '一部', 'git tags（公開の置き場）')
st = open(os.path.join(SUM, 'frame-stamp.txt'), encoding='utf-8').read().strip().split(NL)[0]
mt = {f: datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(SUM, *f.split('/'))), datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')
      for f in ('00-frame-interim-summary-2026-10-02.md', 'calc_interim.py', 'calc/calc-interim.json', 'summary-interim-draft1-2026-10-02.md')}
rec('order', ['14', '15', '16'], '依頼文は計算を「起草の途中で…足しました」と書くが、枠 §3 は追記の節ではなく時刻の刻みも無い（順序の裏付けが無い）',
    '枠の刻印の一行目: %s｜ファイルの書かれた時刻（手元・日本時間）: %s' % (st, mt), '再現（依頼文の言い方が事実と違う。枠は計算の前に刻印した）', 'frame-stamp.txt・依頼文')

# ---- 12. calc json の SHA16 ----
s16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
rec('calc-sha', ['14', '15', '16'], '照らしの記録の calc_sha16 2315B10EE737E70F が何を指すか分からない（検分者の再実行の json は 4C9D1979BDB3E67E・md は一致）',
    'calc-interim.json %s・calc-interim.md %s・calc_interim.py %s（json は浮動小数を repr で書くので、計算の環境が違えば末の桁が変わりうる・md は %%.3f）' % (
        s16f(os.path.join(SUM, 'calc', 'calc-interim.json')), s16f(os.path.join(SUM, 'calc', 'calc-interim.md')), s16f(os.path.join(SUM, 'calc_interim.py'))),
    '再現（json の値。付録 B に三つの SHA16 を並べる）', 'calc/')

res = {'kind': 'repro_round1_interim_summary', 'tool': 'summary/reviews/round1/make_repro_round1.py v0',
       'made_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
       'checks': out, 'counts': {v: sum(1 for x in out if x['verdict'].startswith(v)) for v in ('再現', '一部', '不再現', '参考')},
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
with open(OJ, 'w', encoding='utf-8', newline=NL) as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
L = ['# 一巡目の票の事実の主張の照らし（器・%s 日本時間）' % res['made_jst'], '', '- 器: `make_repro_round1.py` v0。票の名: 14・15・16＝claude-ai-14・15・16、g1＝gemini-1。読みは付けない。', '',
     '| id | 票 | 主張 | 器の結果 | 照らし | 置き場 |', '|---|---|---|---|---|---|']
for x in out:
    L.append('| %s | %s | %s | %s | %s | %s |' % (x['id'], '・'.join(x['voters']), x['claim'].replace('|', '／'), x['result'].replace('|', '／'), x['verdict'], x['where']))
L += ['', '- 数え: %s' % json.dumps(res['counts'], ensure_ascii=False), '', res['clause'], '']
open(OM, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('checks %d | %s | json %s | md %s' % (len(out), res['counts'], s16f(OJ), s16f(OM)))
for x in out:
    if not x['verdict'].startswith('再現'):
        print(' ', x['id'], x['verdict'], '|', x['result'][:200])
