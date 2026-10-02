# -*- coding: utf-8 -*-
"""make_repro_round2.py v0（2026-10-02・中間総括の検分の二巡目の票の事実の主張を記録に照らす・一巡目の器の型・コーディネータ南無弥勒如来）。
票（claude-ai-17・18・19・gemini-3・4）が挙げた数と文の主張のうち、採否を決めるのに要るものを、公開の置き場の記録・草案2・計算の出力 v0.2 から器で出し直す。
読みは付けない。出し直した値は登録の外の記述で、札でも区間による判定でもない。書く物は一度だけ（`repro-round2.json` と `repro-round2.md`）。
用法: python make_repro_round2.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, glob, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.dirname(os.path.dirname(HERE))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
P = lambda *a: os.path.join(PUB, *a)
NL = chr(10)
OJ, OM = os.path.join(HERE, 'repro-round2.json'), os.path.join(HERE, 'repro-round2.md')
for p_ in (OJ, OM):
    assert not os.path.exists(p_), '一度だけ: ' + p_
D2 = open(os.path.join(SUM, 'summary-interim-draft2-2026-10-02.md'), encoding='utf-8').read()
CJ = json.load(open(os.path.join(SUM, 'calc', 'calc-interim-v0.2.json'), encoding='utf-8'))
CALC_PY = open(os.path.join(SUM, 'calc_interim.py'), encoding='utf-8').read()
FIN = {'4B': 'records/results/results-report-FINAL-2026-09-07.md', 'Vp': 'records/vprime/results-report-Vprime-FINAL-2026-09-09.md', 'M': 'records/M/results-report-M-FINAL-2026-09-11.md',
       'F': 'records/F/results-report-F-FINAL-2026-09-12.md', 'A': 'records/A/results-report-A-FINAL-2026-09-17.md', 'B': 'records/B/results-B-FINAL-2026-09-23.md',
       'BL': 'records/Blens/results-Blens-FINAL-2026-09-24.md', 'L3': 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', 'BP': 'records/Bprime/results-Bprime-FINAL-2026-10-01.md'}
TXT = {}
out = []


def src(rel):
    if rel not in TXT:
        TXT[rel] = open(P(*rel.split('/')), encoding='utf-8').read().replace('\r\n', '\n')
    return TXT[rel]


def sec0(k):
    L = src(FIN[k]).split(NL)
    i = [n for n, l in enumerate(L) if l.startswith('## 0.')][0]
    j = [n for n in range(i + 1, len(L)) if L[n].startswith('## ')][0]
    return i + 1, j


def where(k, s, strip_bold=True):
    L = src(FIN[k]).split(NL)
    hits = [n + 1 for n, l in enumerate(L) if s in (l.replace('**', '') if strip_bold else l)]
    a, b = sec0(k)
    return hits, ('§0 の中' if hits and all(a <= h <= b for h in hits) else ('§0 の外' if hits else '無い'))


def rec(cid, voters, claim, result, verdict):
    out.append({'id': cid, 'voters': voters, 'claim': claim, 'result': result, 'verdict': verdict})


# ---- Z01 追補 M の「これら」 ----
h1, w1 = where('M', '上向き ① のうち対照（B 腕）が第一走行で破局 0/400 の対比')
h2, w2 = where('M', 'これらの差は A 腕の上昇ではなく対照の床が作る')
i_up = D2.index('うち 11 本が上向き')
i_these = D2.index('これらの差は A 腕の上昇ではなく対照の床が作る')
i_next = D2.index('下向き ① は 10 本')
rec('Z01-a', ['17', '18', '19'], '§0 の「これらの差」は「上向き ① のうち対照（B 腕）が第一走行で破局 0/400 の対比」の三本を指す。草案2 は前置きの句を引かず、「11 本が上向き」の直下の子の箇条に置いた',
    '前置きの句の行 %s（%s）・「これらの差」の行 %s（%s）・草案2 で前置きの句を引いているか: %s・「これらの差」の箇条は「11 本が上向き」と「下向き ① は 10 本」の間にあるか: %s' % (
        h1, w1, h2, w2, '上向き ① のうち対照（B 腕）が第一走行で破局 0/400 の対比' in D2, i_up < i_these < i_next), '再現')
h3, w3 = where('M', '判定可能な対比の過半を保留した族 × 場面は 5')
rec('Z01-b', ['17', '18', '19'], '「これらの断面」の指す先（族 × 場面の五つ）の文が草案2 に無い', '元の文の行 %s（%s）・草案2 に在る: %s' % (h3, w3, '族 × 場面は 5' in D2), '再現')
h4, w4 = where('M', '重みは同じであるため同じ書式でここにも並べる')
rec('Z01-c', ['17'], '下向き ① の「重みは同じであるため同じ書式でここにも並べる」が草案2 に無い', '行 %s（%s）・草案2 に在る: %s' % (h4, w4, '重みは同じであるため' in D2), '再現')
# ---- Z02 V′ の族の表・4B の段VI ----
vt = [l for l in src(FIN['Vp']).split(NL) if l.startswith('| Vprime_')]
st6 = [l for l in src(FIN['4B']).split(NL) if l.startswith('| VI（m=1）')]
rec('Z02', ['19'], 'V′ の §0 は V′a だけで、V′b（確証 7・有意で逆 1）と V′c（確証 31・門で記述に降格 1）は §0 の外。4B の最初の登録の段VI（門で降格）も §0 の外で、四つの欄に無い',
    'V′ の族の表の行: %s／4B の段VI の行: %s／V′ の §0 の行の範囲 %s・4B の §0 の行の範囲 %s／草案2 に「V′b」「段VI」: %s・%s' % (
        ' / '.join(vt), ' / '.join(st6), sec0('Vp'), sec0('4B'), 'V′b' in D2 or 'Vprime_b' in D2, '段VI' in D2), '再現')
# ---- Z03 段階 B の Holm の文 ----
hb, wb = where('B', '一番近い一本との比較で名目の水準を下回るのは')
hb2, wb2 = where('B', '（事後の計算・札を作らず取り下げもしない）')
rec('Z03', ['17', '18', '19'], '段階 B の太字の文を「十六本の Holm を掛けると」から切り、主語（一番近い一本との比較）と「（事後の計算・札を作らず取り下げもしない）」が落ちた',
    '主語の句の行 %s（%s）・断りの行 %s（%s）・草案2 に主語の句: %s・断り: %s' % (hb, wb, hb2, wb2, '一番近い一本との比較で名目の水準を下回るのは' in D2, '（事後の計算・札を作らず取り下げもしない）' in D2), '再現')
# ---- Z04 層三の「この説明」 ----
hl, wl = where('L3', '主の行の多くで等方のランダム方向の広がりの外に大きく出る')
hv, wv = where('L3', '揺れの版の印: V1・V2・V3')
hg, wg = where('L3', '二つ目の札の偶然の目安 0.2701〜0.53')
rec('Z04', ['17', '18', '19'], '層三の「封印したコーディネータの予想の考え方は、この説明に立っていた」の指す説明（外に大きく出る）と「退けられた」が草案2 に無い。揺れの版の印と二つ目の札の偶然の目安も落ちた',
    '説明の行 %s（%s）・草案2 に説明: %s／揺れの版の印 %s（%s）・草案2: %s／偶然の目安 %s（%s）・草案2: %s' % (
        hl, wl, '外に大きく出る' in D2, hv, wv, 'V1・V2・V3' in D2, hg, wg, '0.2701' in D2), '再現')
# ---- Z05 §3.1 の層三の行 ----
l3 = [l for l in D2.split(NL) if l.startswith('  - 層三: 〈両方の外〉の一行')]
rec('Z05', ['g3', 'g4', '18', '19'], '§3.1 の層三の行に、読み取りの位置の記述・門を通らない・段階 B の行動に結びつけない、の限りが無い。事情は弱める側の二つだけで、段階 B の札は凍結した集計器の側だけ',
    '草案2 の行: %s' % (l3[0] if l3 else '無い'), '再現' if l3 and '読み取りの位置' not in l3[0] else '一部')
# ---- Z06 4B の限りの不揃い ----
h6, w6 = where('4B', '素の場では refuse ≤35 で破局減 ≥115 を吸収できないため転位だけでは説明できない')
h7, w7 = where('4B', 'いずれも refuse が 140／201')
h8, w8 = where('4B', '上向きに読めば天井で記述となるが、数値はどちらの札でも同じ')
rec('Z06', ['17', '18', '19'], '4B の §0 の限る文のうち、O 対 Onull の転位の文・Lneg の核の二本の refuse と答えた分母・段V の「上向きに読めば天井で記述」が草案2 に無い',
    '転位の文 %s（%s）草案2: %s／Lneg の refuse %s（%s）草案2: %s／段V の文 %s（%s）草案2: %s' % (
        h6, w6, '転位だけでは説明できない' in D2, h7, w7, '140／201' in D2, h8, w8, '上向きに読めば天井で記述' in D2), '再現')
# ---- Z07 段階 A の限り ----
ha, wa = where('A', '感度閾値の下で残った規模は、どちらも連続でないか端を欠く')
ha2, wa2 = where('A', '合格はこの引かれる向きと同じ側にある')
rec('Z07', ['17', '18', '19'], '段階 A の感度閾値の二本の限り（連続でないか端を欠く）と、門0.5 の合格の文脈（引かれる向きと同じ側）が草案2 に無い',
    '感度の限り %s（%s）草案2: %s／合格の文 %s（%s）草案2: %s' % (ha, wa, '連続でないか端を欠く' in D2, ha2, wa2, '引かれる向きと同じ側にある' in D2), '再現')
# ---- Z08 段階 F の両向き ----
hf, wf = where('F', '判定保留・判定不能の 14 本の向き（札なし・数のみ）: 上向き 0・下向き 13・差なし 1')
down = [x for x in ('S1:T2-O-Ncold~O-Ncold', 'S4:T2-O-Ncold~O-Ncold') if x in src(FIN['F'])]
rec('Z08', ['17', '18', '19'], '段階 F の下向きの確証 4 本のうち S1・S4 の 2 本も一斉保留の起きた場面にある。草案2 は限りを上向きにだけ付けた。14 本の向きの文も無い',
    '下向きの確証のうち S1・S4 の対比: %s・一斉保留の場面: S1・S4・SK（§0 の 5）／14 本の向きの行 %s（%s）草案2: %s' % (down, hf, wf, '下向き 13' in D2), '再現')
# ---- Z09 段階 A の非有意と旗 ----
hflag, wflag = where('A', '非有意の札の対比（N1 の Lneg 対 Onull')
rec('Z09', ['17', '18', '19'], '段階 A の非有意 9 本のうち 7 本に様式門の旗が立つ（§0 が名指す）。草案2 §3.1 は非有意を丸ごと「測って区別できなかった」に置いた',
    '旗の文の行 %s（%s）・旗の立つ非有意の対比の数（§0 の括弧の中の「・」で区切った数）: %d' % (
        hflag, wflag, src(FIN['A']).split('非有意の札の対比（')[1].split('）')[0].count('・') + 1), '再現')
# ---- Z11 S10 の範囲 ----
s10 = [l for l in D2.split(NL) if '二つの機種の行動の率を' in l]
rec('Z11', ['17', '19'], '§0 と §5 が S10 を「二つの機種」一般に広げて書き、七機種を並べた §3.2・§3.3 と字の上で食い違う', '草案2 の該当の行の数 %d・B′ の凍結の本文の S10 の行 %s' % (
    len(s10), [n + 1 for n, l in enumerate(src('design/design-Bprime-FROZEN.md').split(NL)) if '〔S10〕' in l]), '再現')
# ---- Z15 書式外 ----
fo = {}
for p in sorted(glob.glob(P('results', 'stageA', 'stageA__*', 'cells.json'))):
    d = json.load(open(p, encoding='utf-8'))
    sz = d['manifest']['model'].split('/')[-1]
    for a in ('N', 'Onull', 'O', 'Ncold', 'Onull-Ncold', 'O-Ncold'):
        f_ = d['cells'][a]['triplet_all'].get('format_out', 0)
        fo[sz] = fo.get(sz, 0) + f_
big = []
for p in sorted(glob.glob(P('results', 'stageA', 'stageA__*', 'cells.json'))):
    d = json.load(open(p, encoding='utf-8'))
    if d['manifest']['model'].endswith('0.6B'):
        for a in ('N', 'Onull', 'O', 'Ncold', 'Onull-Ncold', 'O-Ncold'):
            t_ = d['cells'][a]['triplet_all']
            if t_.get('format_out', 0) >= 30:
                big.append('%s %s 書式外 %d／%d（破局 %d）' % (d['manifest']['scenario'], a, t_['format_out'], d['cells'][a]['n_ok'], t_['catastrophe']))
rec('Z15', ['18', '19'], '全分母の率は書式外と refuse を分母に含む。0.6B の床の升の中に書式外が過半の升がある（S1 の N・Ncold、S4 の N・Ncold）。六つの腕の書式外の和は 0.6B で 881、Qwen3-4B で 1、ほかは 0',
    '六つの腕の書式外の和: %s／0.6B で 30 以上の升: %s' % (json.dumps(fo, ensure_ascii=False), '・'.join(big)), '再現')
# ---- Z25 閾値ちょうど ----
th = [0.05, 0.95, 0.03, 0.97, 0.08, 0.92]
ex = ['%s %s %s %s %d/%d=%s' % (x['stage'], x['size'], x['scenario'], x['arm'], x['k'], x['n_ok'], t) for x in CJ['calc1_rows'] for t in th if abs(x['rate'] - t) < 1e-12]
inc = []
for st in ('A', 'Vprime'):
    for sz in ('0.6B', '1.7B', '4B', '8B', '14B', '32B', '4B-2507'):
        xs = [x for x in CJ['calc1_rows'] if x['stage'] == st and x['size'] == sz]
        if xs:
            a_ = sum(1 for x in xs if x['rate'] < 0.05 or x['rate'] > 0.95)
            b_ = sum(1 for x in xs if x['rate'] <= 0.05 or x['rate'] >= 0.95)
            if a_ != b_:
                inc.append('%s %s 端 %d→%d' % (st, sz, a_, b_))
rec('Z25', ['17', '18', '19'], '計算一の腕にも閾値に等しい腕がある（主: 1.7B N1 Onull・4B S1 Ncold・4B S4 Onull-Ncold／感度: 1.7B SK Ncold 0.97・4B S1 N 0.92・32B N1 Onull 0.08）。等号を端に含めると 1.7B は 20→21、4B は 9→11',
    '閾値に等しい腕: %s／等号を端に含めたときに変わる数: %s' % ('・'.join(ex), '・'.join(inc)), '再現')
# ---- Z19 器の説明文 ----
rec('Z19', ['17', '18', '19', 'g3', 'g4'], '計算の器 v0.2 の説明文は出力を v0.1 の名で書いている（コードは v0.2 を書く）', '説明文に「calc-interim-v0.1.json」: %s・VER: %s' % (
    'calc-interim-v0.1.json' in CALC_PY.split('import os')[0], [l for l in CALC_PY.split(NL) if l.startswith('VER = ')]), '再現')
# ---- Z26 標本化と腕の数 ----
dv = json.load(open(sorted(glob.glob(P('results', 'stageVp', 'stageVp__*', 'cells.json')))[0], encoding='utf-8'))['manifest']
da = json.load(open(sorted(glob.glob(P('results', 'stageA', 'stageA__*', 'cells.json')))[0], encoding='utf-8'))['manifest']
h52, w52 = where('Vp', '4 シナリオ × 52 腕 × 400')
rec('Z26', ['19'], 'V′ の走りは 52 腕で、計算はそのうち 6 腕を取る。標本化は温度 0.7・top_p 0.9（段階 A は思考を切る）', 'V′ の 52 腕の行 %s（%s）／V′ の標本化 %s／段階 A の標本化 %s' % (
    h52, w52, json.dumps(dv.get('sampling'), ensure_ascii=False), json.dumps(da.get('sampling'), ensure_ascii=False)), '再現')
# ---- Z14 Firth の帰属（計画書は内部・照らしは起草者が読みで行った） ----
rec('Z14', ['17', '18', '19'], '§6 の段階 C の定めで、「Firth の」を 2026-09-10 の登録者の決めに帰した。枠 §3 には Firth が無い',
    '枠 §3 の計算二の行: Firth の当てはめを器の選びとして書き、決めは「対数オッズ比の絶対値の比べ」と書く（%s）。内部の計画書の段階 C の節は、登録者決定 2026-09-10（裁定 3）として「対数オッズ比の絶対値（Firth）の比較」と書く（起草者が読みで確かめた・計画書は束に入れていない）' % (
        '対数オッズ比の絶対値の比べ・登録者決定 2026-09-10' in open(os.path.join(SUM, '00-frame-interim-summary-2026-10-02.md'), encoding='utf-8').read()), '一部（計画書には Firth がある・出所を内部の計画書と書けば足りる）')
# ---- B-lens の M_X の未試験 ----
hx, wx = where('BL', 'M_X 割合 0.8732（第一段で止まったので試されていない）')
rec('Z13b', ['18'], 'B-lens の門の M_X は第一段で止まったので試されていない（測れなかった側）', '行 %s（%s）・草案2 に「試されていない」: %s' % (hx, wx, '試されていない' in D2), '再現')

res = {'kind': 'repro_round2_interim_summary', 'tool': 'summary/reviews/round2/make_repro_round2.py v0',
       'made_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
       'checks': out, 'counts': {v: sum(1 for x in out if x['verdict'].startswith(v)) for v in ('再現', '一部', '不再現')},
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
with open(OJ, 'w', encoding='utf-8', newline=NL) as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
L = ['# 二巡目の票の事実の主張の照らし（器・%s 日本時間）' % res['made_jst'], '', '- 器: `make_repro_round2.py` v0。票の名: 17・18・19＝claude-ai-17・18・19、g3・g4＝gemini-3・4。読みは付けない。', '',
     '| id | 票 | 主張 | 器の結果 | 照らし |', '|---|---|---|---|---|']
for x in out:
    L.append('| %s | %s | %s | %s | %s |' % (x['id'], '・'.join(x['voters']), x['claim'].replace('|', '／'), x['result'].replace('|', '／'), x['verdict']))
L += ['', '- 数え: %s' % json.dumps(res['counts'], ensure_ascii=False), '', res['clause'], '']
open(OM, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('checks %d | %s' % (len(out), res['counts']))
for x in out:
    print(' ', x['id'], x['verdict'], '|', x['result'][:230])
