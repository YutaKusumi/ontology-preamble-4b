# -*- coding: utf-8 -*-
"""make_repro_final.py v0（2026-10-02・中間総括の検分の最終の巡の票の事実の主張を記録に照らす・二巡目の `make_repro_round2.py` v0 の型・コーディネータ南無弥勒如来）。
票（claude-ai-20・21・22・gemini-5・6）が挙げた数と文の主張のうち、採否を決めるのに要るものを、公開の置き場の記録・草案3・照らしの記録・計算の出力 v0.3 から器で出し直す。
読みは付けない。出し直した値は登録の外の記述で、札でも区間による判定でもない。書く物は一度だけ（`repro-final.json` と `repro-final.md`）。
用法: python make_repro_final.py [--dry]（--dry は書かずに表示だけする）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, glob, math, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.dirname(os.path.dirname(HERE))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
P = lambda *a: os.path.join(PUB, *a)
NL = chr(10)
DRY = '--dry' in sys.argv
OJ, OM = os.path.join(HERE, 'repro-final.json'), os.path.join(HERE, 'repro-final.md')
if not DRY:
    for p_ in (OJ, OM):
        assert not os.path.exists(p_), '一度だけ: ' + p_
D3P = os.path.join(SUM, 'summary-interim-draft3-2026-10-02.md')
D3 = open(D3P, encoding='utf-8').read()
assert hashlib.sha256(open(D3P, 'rb').read()).hexdigest().upper().startswith('55C9D3B0647E6E21'), '草案3 の SHA が違う'
CHK = json.load(open(os.path.join(SUM, 'summary-interim-draft3-checks.json'), encoding='utf-8'))
CJ = json.load(open(os.path.join(SUM, 'calc', 'calc-interim-v0.3.json'), encoding='utf-8'))
CMD = open(os.path.join(SUM, 'calc', 'calc-interim-v0.3.md'), encoding='utf-8').read()
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
    a, b = CHK['sec0_ranges'][k]
    return a, b


def where(k, s, strip_bold=True):
    L = src(FIN[k]).split(NL)
    hits = [n + 1 for n, l in enumerate(L) if s in (l.replace('**', '') if strip_bold else l)]
    a, b = sec0(k)
    return hits, ('・'.join('%d 行は §0 の%s' % (h, '中' if a <= h <= b else '外') for h in hits) if hits else '無い')


def line(k, n):
    return src(FIN[k]).split(NL)[n - 1].replace('**', '')


def d3sec(head, nxt):
    i = D3.index(head)
    return D3[i:D3.index(nxt, i + 1)]


def rec(cid, voters, claim, result, verdict):
    out.append({'id': cid, 'voters': voters, 'claim': claim, 'result': result, 'verdict': verdict})


S31 = d3sec('### 3.1 ', '### 3.2 ')
S31_cant = [l for l in S31.split(NL) if l.startswith('- **測れなかった**')][0]
S31_same = [l for l in S31.split(NL) if l.startswith('- **測って区別できなかった**')][0]
S31_rev = [l for l in S31.split(NL) if l.startswith('- **測って想定と逆だった**')][0]
S31_ok = S31.split('- **測れた**')[1].split('- **測って区別できなかった**')[0]

# ---- R01 段階 A の様式転位 9 本 ----
tally = [l for l in src(FIN['A']).split(NL) if l.startswith('傾きの族 35 対比のうち')]
segA = S31_cant.split('段階 A の')[1].split('・段階 B')[0]
segs = {'測れた': [l for l in S31_ok.split(NL) if '段階 A' in l], '測って区別できなかった': [s for s in S31_same.split('・') if '段階 A' in s],
        '測って想定と逆だった': [s for s in S31_rev.split('・') if '段階 A' in s]}
rec('R01', ['20', '21'], '段階 A の判定保留（様式転位）9 本が §3.1 の四つの欄のどこにも無い（置かれたのは 1＋2＋3＋13＋7＝26 本）',
    '段階 A の §0 の内訳の行: %s／§3.1 の測れなかった欄の段階 A の部分: 「%s」・そこに「様式転位」: %s／ほかの欄の段階 A の部分: %s' % (
        tally[0] if tally else '無い', segA, '様式転位' in segA, json.dumps({k: [x.strip()[:60] for x in v] for k, v in segs.items()}, ensure_ascii=False)), '再現')
# ---- R02 段階 F の「この仮説」 ----
hf, wf = where('F', '本段はこの仮説の検証も反証もしない（§4）。')
rec('R02', ['20', '21', '22'], '§2.4 の一行目「本段はこの仮説の検証も反証もしない（§4）。」の「この仮説」（登録者の関心の仮説・F の §0 の 1 の 2）が草案3 に無い。照らしの器は、頭が指示語でないので拾わなかった',
    '元の行 %s（%s）・同じ行に「登録者の関心」: %s／草案3 に「検査環境を見破」: %s／照らしの記録のこの引用の印: 指示語で始まる %s・文の途中 %s' % (
        hf, wf, '登録者の関心' in line('F', hf[0]), '検査環境を見破' in D3,
        [q['starts_with_demonstrative'] for q in CHK['quotes'] if q['quote'].startswith('本段はこの仮説')], [q['starts_mid_sentence'] for q in CHK['quotes'] if q['quote'].startswith('本段はこの仮説')]), '再現')
# ---- R03 族の表の語の注（M と F） ----
hm, wm = where('M', '要約表の本数を単独で引用しない')
hF, wF = where('F', '語の定義: 「判定可能」＝確証＋非有意')
hs, ws = where('M', '①複製された 21・⑤第二走行のみで Holm 基準 2・②複製されなかった 3')
rec('R03', ['20', '22', '21'], '追補 M の族の表の直下の語の注（「判定可能」は様式門の保留を含む・要約表の本数を単独で引用しない）と、段階 F の「判定可能」＝確証＋非有意の定義と、M の ②⑤⑥ の記号の意味が、草案3 に無い。同じ列名が二つの表で違う意味で並ぶ',
    'M の語の注の行 %s（%s・族の表の行 %s の直下）・草案3 に「要約表の本数を単独で引用しない」: %s／F の語の定義の行 %s（%s）・草案3 に「確証＋非有意」: %s／M の記号の内訳の行 %s（%s）・草案3 に「第二走行のみで Holm」: %s' % (
        hm, wm, CHK['family_ranges']['M'], '要約表の本数を単独で引用しない' in D3, hF, wF, '確証＋非有意' in D3, hs, ws, '第二走行のみで Holm' in D3), '再現')
# ---- R04 V′b と V′c の限り ----
hb, wb = where('Vp', 'S4 では相対的な低さを主張として書かず')
hc, wc = where('Vp', '実効的根拠は Onull 側の対比に載る')
hc2, wc2 = where('Vp', '「冷徹の内容に固有の効果」と書けるのは S1・S4・SK に限る')
hd, wd = where('Vp', '誤降格の候補であることを開示する')
rec('R04', ['20', '22'], 'V′b は「O の相対的な位置・数だけ」で、S4 では相対的な低さを主張として書かない。V′c の内容固有は S1・S4・SK に限り、O 側は床で実効的根拠は Onull 側。V′c の降格の一本は誤降格の候補。草案3 は族の表の確証を測れた欄に置くだけ',
    'V′b の行 %s（%s）・草案3 に「相対的な低さ」: %s／V′c の行 %s（%s）と %s（%s）・草案3 に「実効的根拠」: %s・「S1・S4・SK に限る」: %s／誤降格の候補の行 %s（%s）・草案3 に「誤降格」: %s／草案3 の測れた欄の V′ の行: 「%s」' % (
        hb, wb, '相対的な低さ' in D3, hc, wc, hc2, wc2, '実効的根拠' in D3, 'S1・S4・SK に限る' in D3, hd, wd, '誤降格' in D3,
        [l for l in S31_ok.split(NL) if '追補 V′' in l][0].strip()), '再現')
# ---- R05 段階 F の添え札 ----
hz, wz = where('F', '添え札は確証札・非有意札を置換せず独立の列')
rec('R05', ['20'], '段階 F の族の表の「添え札 低下 4・上昇あり 1・上昇なし 2」は検査認識の言及率の向きで、注が無いと破局率の低下と読み違えられる。列名「同じ向きの確証」は M が「向きは問わない」に直した名',
    '添え札の定めの行 %s（%s）・草案3 で「添え札」がある行: %s（族の表の行だけか: %s）／F の族の表の頭の行に「同じ向きの確証（第一走行）」: %s・M の族の表の頭の行に「確証（第一走行・向きは問わない）」: %s' % (
        hz, wz, [n + 1 for n, l in enumerate(D3.split(NL)) if '添え札' in l], all(l.startswith('|') for l in D3.split(NL) if '添え札' in l),
        '同じ向きの確証（第一走行）' in src(FIN['F']), '確証（第一走行・向きは問わない）' in src(FIN['M'])), '再現（列名は F の最終版の字のまま）')
# ---- R06 追補 M の範囲の句（M-b と M-a の本体） ----
hmb, wmb = where('M', 'M-b では N1 の Kan に限り F2／F3 が Nk・F4 より高い')
hma, wma = where('M', '対比ごとに片方の対照——同長の無意味列または同字数の有意味列——より高い')
L8 = src(FIN['M']).split(NL)
rep = [l for l in L8[399:559] if l.startswith('| ') and '①複製された' in l]
fam = {}
for k_, (a_, b_) in {'M_a': (92, 178), 'M_b': (179, 290), 'M_c': (291, 352)}.items():
    blk = NL.join(L8[a_ - 1:b_])
    for l in rep:
        cid = l.split('|')[1].strip()
        if ('| ' + cid + ' |') in blk:
            fam[cid] = k_
up = [(l.split('|')[1].strip(), l.split('|')[6].strip()) for l in rep]
upc = {}
for cid, d_ in up:
    upc.setdefault((fam.get(cid), d_), []).append(cid)
rec('R06', ['20', '21', '22'], '§2.3 に M-b の範囲の句「M-b では N1 の Kan に限り F2／F3 が Nk・F4 より高い」が無い（十一本のうち三本の範囲）。M-a は但し書きだけで、本体の範囲の句が無い。上向き 11 本の内訳は M-a 7・M-b 3・M-c 1',
    'M-b の句の行 %s（%s）・草案3 に在る: %s／M-a の本体の句の行 %s（%s）・草案3 に在る: %s／第二走行の表の ① の行 %d・族と向き₂ ごとの数: %s／M-b の上向き: %s' % (
        hmb, wmb, 'M-b では N1 の Kan に限り' in D3, hma, wma, '同長の無意味列または同字数の有意味列' in D3, len(rep),
        json.dumps({'%s %s' % k: len(v) for k, v in sorted(upc.items(), key=lambda x: str(x[0]))}, ensure_ascii=False), '・'.join(upc.get(('M_b', '+'), []))), '再現')
# ---- R07 Lneg の核の二本の「答えた分母の率で読む」 ----
a0, b0 = sec0('4B')
reads = [n for n in range(a0, b0 + 1) if '答えた分母の率' in line('4B', n)]
rec('R07', ['20', '21', '22'], '§3.1 の想定と逆の欄で、Lneg の核の二本に「答えた分母の率で読む」と書いた。§0 が「答えた分母の率で読む」と書くのは A2′ の O だけで、Lneg は値を並べるだけ',
    '4B の §0 の中で「答えた分母の率」がある行: %s（%s）／§0 の Lneg の行 13 に「で読む」: %s／草案3 の想定と逆の欄に「答えた分母の率で読む」: %s' % (
        reads, ['A2′' in line('4B', n) for n in reads], '答えた分母の率で読む' in line('4B', 13), '答えた分母の率で読む' in S31_rev), '再現')
# ---- R08 段階 A の門0.5 の「この引かれる向き」と「見込み」 ----
hg, wg = where('A', '引かれる向き＝「手元スタックは API と同一」')
hg2, wg2 = where('A', '見込み: 不合格が主経路である')
rec('R08', ['20', '21', '22'], '§2.5 の「合格はこの引かれる向きと同じ側にある」の「この引かれる向き」（手元スタックは API と同一）と「見込み」（不合格が主経路）が草案3 に無い',
    '引かれる向きの句の行 %s（%s）・草案3 に在る: %s／見込みの句の行 %s（%s）・草案3 に在る: %s' % (hg, wg, '手元スタックは API と同一' in D3, hg2, wg2, '不合格が主経路' in D3), '再現')
# ---- R09 段階 A の「この経路」 ----
hp, wp = where('A', '率盲検の外の経路（採否表 P104・P138・裁定 D35・D46）')
rec('R09', ['21'], '§4 の「率盲検の器（整合検査・抽出検査）はこの経路を覆わない」の「この経路」（率盲検の外の経路・A の §0 の 1 の 8）が草案3 に無い',
    '元の行 %s（%s）・同じ行に引用の文: %s／草案3 に「率盲検の外の経路」: %s' % (hp, wp, 'この経路を覆わない' in line('A', hp[0]), '率盲検の外の経路' in D3), '再現')
# ---- R10 段階 A の「この後」と注 #23 ----
fl = [q for q in CHK['quotes'] if q.get('referent_note')]
n23 = fl[22]
l23 = [l for l in D3.split(NL) if n23['quote'] in l][0]
pre23 = l23.split('「' + n23['quote'])[0]
rec('R10', ['21', '22'], '§4 の「この後に検分の巡を置かない（登録者決定）ので、最終検分の反映は外の目を通らない」の注 #23 は「地の文の前置き「最終検分」」を指すが、地の文にその語は無い。段階 A の最終版の頭は公開前の検分の巡を記す',
    '注 #23: 「%s」／草案3 のその行の引用の前の地の文に「最終検分」: %s／A の最終版の題の行に「公開前検分の第一巡と最終検分」: %s／A の §0 の 5 の行 %s は凍結前の最終検分の後の文' % (
        n23['referent_note'], '最終検分' in pre23, '公開前検分の第一巡と最終検分' in line('A', 1), where('A', 'この後に検分の巡を置かない（登録者決定）')[0]), '再現')
# ---- R11 文頭の接続の語（したがって・ただし） ----
i11 = line('4B', 11)
prev11 = i11.split('したがって札は')[0].split('。')[-2]
i48 = line('L3', 48)
prev48 = i48.split('ただし、計算の道を替えると')[0].split('。')[-2]
rec('R11', ['20', '21', '22'], '§2.1 の「したがって札は…」は理由の文（向きはデータ後に確定）が無く、§2.8 の「ただし、計算の道を替えると…」は何への「ただし」かの文が無い',
    '4B の §0 の 1 の「したがって」の前の文の末: 「…%s」・草案3 に「データ後に」: %s／層三の §0 の「ただし」の前の文の末: 「…%s」・草案3 に在る: %s' % (
        prev11[-40:], 'データ後に' in D3, prev48[-40:], prev48.strip()[-20:] in D3), '再現')
# ---- R12 段階 F の「様式率の表（§4）を主結果とする」 ----
hx, wx = where('F', 'これらの場面では様式率の表（§4）を主結果とする')
rec('R12', ['20', '21', '22'], '§2.4 は F の §0 の 5 の「これらの場面では様式率の表（§4）を主結果とする」を落としている。M の同じ句（様式率の表〔§10〕を主結果として置く）は引いている',
    'F の句の行 %s（%s）・草案3 に「様式率の表（§4）」: %s／草案3 に M の「様式率の表（§10）を主結果として置く」: %s' % (hx, wx, '様式率の表（§4）' in D3, '様式率の表（§10）を主結果として置く' in D3), '再現')
# ---- R13 F-2 の句 ----
hq, wq = where('F', 'F-2 の公開規則と柵は F-2 に自動継承されない')
rec('R13', ['20', '21'], '§6 C (i) が引く「F-2 の公開規則と柵は F-2 に自動継承されない」は元の字のとおりだが、自分を指す形で意味が通らない。〔原文のまま〕の注が要る',
    '元の行 %s（%s）・元の字と草案3 の引用が同じ: %s・草案3 に「原文のまま」: %s' % (hq, wq, '「F-2 の公開規則と柵は F-2 に自動継承されない」' in D3, '原文のまま' in D3), '再現')
# ---- R14 標本化と GPU の機種ごとの割り当て ----
samp = {}
for p in sorted(glob.glob(P('results', 'stageA', 'stageA__*', 'cells.json'))):
    m = json.load(open(p, encoding='utf-8'))['manifest']
    key = m['model'].split('/')[-1]
    samp.setdefault(key, set()).add('%s|gpu %s' % (json.dumps(m['sampling'].get('extra_body'), ensure_ascii=False, sort_keys=True), (m.get('local_env') or {}).get('gpu', '?').split(',')[0]))
rec('R14', ['20', '21', '22'], '§3.2 の標本化の二つの設定がどの機種のものか書かれていない（Qwen3 の稠密の六機種が enable_thinking false・4B-2507 は extra_body が空）。GPU は L4 と A100 に分かれる',
    '機種ごとの extra_body と GPU（35 の走りの manifest）: %s／草案3 の標本化の行に機種の名: %s' % (
        json.dumps({k: sorted(v) for k, v in samp.items()}, ensure_ascii=False), [x for x in ('0.6B', '4B-2507') if x in [l for l in D3.split(NL) if l.startswith('- 標本化')][0]]), '再現')
# ---- R15 計算の出力の V′ の節の定型文 ----
vsec = CMD[CMD.index('### V′ の本走行'):CMD.index('## 計算二')]
fo_v = sum(x.get('format_out', 0) for x in CJ['calc1_rows'] if x['stage'] == 'Vprime')
rec('R15', ['20', '22'], '計算の出力 v0.3 の md の V′ の節の「書式外の多い升がある」は誤り（V′ の書式外は 0）',
    'md の中の「書式外の多い升がある」の数: %d（そのうち計算一の V′ の節に %d）／V′ の腕の書式外の和: %s' % (CMD.count('書式外の多い升がある'), vsec.count('書式外の多い升がある'), fo_v), '再現')
# ---- R16 refuse の和 ----
ref = {}
for x in CJ['calc1_rows']:
    k_ = '%s %s' % (x['stage'], x['size'])
    ref[k_] = ref.get(k_, 0) + x.get('refuse', 0)
rec('R16', ['20', '21', '22'], 'refuse の和（段階 A: 11・26・226・91・57・165・49、V′: 34）が §3.2 の表に無い（読みは refuse も分母に入ると書く）',
    'refuse の和（計算の出力の腕の行から）: %s／§3.2 の表の頭に「refuse」: %s' % (json.dumps(ref, ensure_ascii=False), 'refuse' in [l for l in D3.split(NL) if l.startswith('| 段階 A の本走行')][0]), '再現')
# ---- R17 段階 B の S4 の反証の事情 ----
s4 = line('B', 34)
rec('R17', ['20', '21', '22'], '§2.6 の S4 の反証に、判定の順の理由（相手の率が登録の効き目より低いと「下がった」の枝に届かない）と、反証の腕が全試行で同じ選択・同じ様式になり、ランダムの一本も同じ形になった文が無い',
    'B の §0 の行 34 に二つの文: %s・%s／草案3 に「下がった」の枝: %s・「全試行が同じ選択」: %s' % (
        '「下がった」の枝に届かない' in s4, '全試行が同じ選択・同じ様式' in s4, '「下がった」の枝に届かない' in D3, '全試行が同じ選択' in D3), '再現')
# ---- R18 注の表 ----
L3S = d3sec('### 2.8 ', '### 2.9 ').split(NL)
i_b = [n for n, l in enumerate(L3S) if l.startswith('  - 〈両方の外〉の一行')][0]
i_e = [n for n, l in enumerate(L3S) if 'これらは札と型を変えない' in l][0]
kids = [l for l in L3S[i_b + 1:i_e] if l.startswith('    - ')]
same = fl[12]['referent_note'] == fl[14]['referent_note']
sec5 = d3sec('## 5. ', '## 6. ')
in5 = [i + 1 for i, q in enumerate(fl) if ('「' + q['quote']) in sec5]
rec('R18', ['20', '21', '22'], '注の表: #16 は「直前の五つの子」だが草案3 では六つ。#13 と #15 は指す先の違う引用に同じ注。#23 は R10。§5 の定型の注（#28〜#30）は指す先が別の小節にある。#7 の U は草案に定義が無い。#1 の「この文形・この語」は冷徹一行の逐語の文形と語を指す',
    '#16 の注: 「%s」・子の箇条の数: %d／#13 と #15 の注が同じ: %s／§5 にある注つきの引用の番号: %s／草案3 で「U」の字がある行: %s（その行の中身の頭: 「%s」）／#1 の注: 「%s」' % (
        fl[15]['referent_note'], len(kids), same, in5, [n + 1 for n, l in enumerate(D3.split(NL)) if ' U ' in l or '対 U' in l or 'U は' in l],
        [l for l in D3.split(NL) if '対 U' in l][0].strip()[:30], fl[0]['referent_note']), '再現')
# ---- R19 検分票に無いもの ----
kv = D3[D3.index('## 検分票'):]
rec('R19', ['20', '21', '22'], '検分票に、追記二 §1 の境の結果（段階 B の S4・層三の外した升目・B-lens の M_X）の欄と理由と、最終の束が追記二 §5 から変わったこと（草案2 の全文と計算の器を入れていない）が無い',
    '検分票に「S4」: %s・「M_X」: %s・「外した升目」: %s／検分票に最終の束のずれ: %s（草案3 は束の前に組んだ）／依頼文に「草案2」: %s' % (
        'S4' in kv, 'M_X' in kv, '外した升目' in kv, '最終の束' in kv, '草案2' in open(os.path.join(HERE, 'request-final.md'), encoding='utf-8').read()), '再現')
# ---- R20 M の ① と五つの断面 ----
five = {('M_a', 'S1'), ('M_a', 'S4'), ('M_b', 'N1'), ('M_b', 'S1'), ('M_c', 'S4')}
inf = {d_: [cid for cid, dd in up if dd == d_ and (fam.get(cid), cid.split(':')[0]) in five] for d_ in ('+', '−')}
rec('R20', ['20', '21'], '追補 M の上向き ① 11 本のうち 6 本（M_a S1 の 2・M_a S4 の 1・M_b N1 の 3）が五つの断面にあり、下向き ① 10 本は 0 本（段階 F とそろっていない）',
    '五つの断面にある上向き ①: %d／%d（%s）・下向き ①: %d／%d' % (len(inf['+']), sum(1 for _, d_ in up if d_ == '+'), '・'.join(inf['+']), len(inf['−']), sum(1 for _, d_ in up if d_ == '−')), '再現')
# ---- R21 B-lens の柵 ----
hl, wl = where('BL', '段の近くの値を、惜しいとも逆の側とも読まない')
rec('R21', ['21', '22'], '§2.7 は B-lens の門の数（0.03472 対 0.025）を引くが、同じ区画の柵「段の近くの値を、惜しいとも逆の側とも読まない」が無い',
    '柵の行 %s（%s）・草案3 に在る: %s・草案3 に「0.03472」: %s' % (hl, wl, '惜しいとも' in D3, '0.03472' in D3), '再現')
# ---- R22 層三の D-BLT1 の事情 ----
h7, w7 = where('L3', '効き目 2.734 の分だけ対数オッズを動かすと 0.0024')
h8, w8 = where('L3', '段階 B の無操作の破局の率 0.12')
rec('R22', ['22'], '層三の〈両方の外〉の事情のうち、無操作の a の確率 0.0001533・効き目の分だけ動かしても 0.0024・段階 B の無操作の破局の率 0.12 が草案3 に無い',
    '0.0024 の行 %s（%s）・草案3 に「0.0001533」: %s・「0.0024」: %s／0.12 の行 %s（%s）・草案3 に「破局の率 0.12」: %s／「効き目の側: 符号だけ」の行 %s・草案3 に在る: %s' % (
        h7, w7, '0.0001533' in D3, '0.0024' in D3, h8, w8, '破局の率 0.12' in D3, where('L3', '効き目の側: 符号だけ')[1], '効き目の側: 符号だけ' in D3), '再現')
# ---- R23 層三の段階 B の札 ----
rec('R23', ['21'], '§2.8 の〈両方の外〉の行の段階 B の札は凍結側の「判定不能（品質床）」だけ。B の §0 はどちらか一方の内訳だけを引くことを禁じる',
    '層三の §0 の行 110 の札の字: %s・層三の §0 に「逸脱 D-B1」: %s／B の §0 の「どちらか一方の内訳だけを引いてはならない」の行: %s' % (
        '主の表の段階 B の札: 判定不能（品質床）' in line('L3', 110), any('D-B1' in line('L3', n) for n in range(*sec0('L3'))), where('B', 'どちらか一方の内訳だけを引いてはならない')[0]), '再現（字は層三の §0 のまま）')
# ---- R24 B′ の「追試」 ----
hr, wr = where('BP', '層三の結果が別の機種で再現するか')
rec('R24', ['21'], '§2.9 の見出しの「追試」は、B′ の §0 の見ていない場所「層三の結果が別の機種で再現するか」とぶつかる。B′ の最終版は自らを追試と書いていない',
    '見ていない場所の行 %s（%s）／B′ の最終版の中の「追試」の数: %d／草案3 の §2.9 の見出しに「追試」: %s' % (
        hr, wr, src(FIN['BP']).count('追試'), '追試' in [l for l in D3.split(NL) if l.startswith('### 2.9')][0]), '再現')
# ---- R25 0.5 の補正と n ----
dn = ['%.3f' % v for v in sorted(x['logor_down'] for x in CJ['calc2_rows'] if x['stage'] == 'A' and x['size'] == '4B-2507')]
rec('R25', ['21'], '§3.3 と §6 C (f) の「0.5 の補正と n で大きさが決まる」は言い過ぎで、対照の率にも依る（4B-2507 の下向きは同じ n=200 で −5.079〜−10.368）',
    '草案3 の §3.3 の文: %s・§6 の文: %s／段階 A の 4B-2507 の下向き（計算の出力）: %s' % (
        '0.5 の補正と n で大きさが決まる' in D3, '0.5 の補正と n で決まる' in D3, dn), '再現' if dn else '照らせない（器の出力の名が違う）')
# ---- R26 段階 A の確証の一本の限り ----
lim = [n for n in range(670, 690) if '非連続' in line('A', n) or '端を欠く' in line('A', n)]
rec('R26', ['21', '22'], '段階 A の確証の一本（S4 の Onull 対 N）の限り（残った規模が非連続で端を欠く・様式の層・環境の境目・4B の N の言及率）は最終版 675〜684 行にあり、草案3 は指していない',
    '670〜689 行で「非連続」か「端を欠く」がある行: %s／草案3 に「675」: %s' % (lim, '675' in D3), '再現' if lim else '不再現')
# ---- R27 V′b の逆の一本 ----
h9, w9 = where('Vp', 'O-Ncold 96/400 対 Osec-Ncold 69/400 で有意に逆')
h9b, w9b = where('Vp', '| S4:O-Ncold~Osec-Ncold | down |')
rec('R27', ['21'], 'V′b の有意で逆の一本は S4 の O-Ncold 対 Osec-Ncold（Fisher p 0.0229）', '行 %s（%s）・対比の表の行 %s（%s）・その行の p の字: %s' % (
    h9, w9, h9b, w9b, line('Vp', h9b[0]).split('|')[6].strip() if h9b else '無い'), '再現')
# ---- R28 段階 A の「測れた」の語 ----
h10, w10 = where('A', 'Onull-Ncold~Onull: 測れた対比 0／5 本')
h11, w11 = where('A', '測れた効果種（本走行の対照の率・Δ=±15 pt')
h12, w12 = where('A', 'Onull~N: 測れた対比 0／5 本')
nonsig = [l.split('|')[1].strip() for l in src(FIN['A']).split(NL)[480:530] if l.startswith('| ') and '非有意' in l]
flagged = src(FIN['A']).split('非有意の札の対比（')[1].split('）')[0]
nonsig = ['%s（旗 %s）' % (c_, 'あり' if '%s の %s 対 %s' % (c_.split(':')[0], c_.split(':')[1].split('~')[0], c_.split('~')[1]) in flagged else 'なし') for c_ in nonsig]
rec('R28', ['22', '21'], '段階 A の §0 の 7 の「測れた効果種／測れた対比」（Δ=±15 pt で確証になる確率の区間の下端が 0.8 以上）の定義が無いので、§3.1 の欄の語とぶつかる。旗の立たない非有意の二本は N1 と SK の Onull-Ncold 対 Onull で、その型は「測れた対比 0／5」。確証の一本の型 Onull~N は「測れなかった効果種」',
    '定義の行 %s（%s）・その行で Onull-Ncold~Onull は「測れた効果種」の側: %s／Onull-Ncold~Onull の行 %s（%s）／Onull~N の行 %s（%s）／A の 481〜530 行の非有意の札の行: %s／草案3 に「下端が 0.8」: %s' % (
        h11, w11, line('A', h11[0]).split('／')[0].endswith('Onull-Ncold~Onull'), h10, w10, h12, w12, nonsig, '下端が 0.8' in D3), '再現（Onull-Ncold~Onull は効果種としては測れた側・対比としては 0／5）')
# ---- R29 二巡目の新しい誤り ----
at2 = open(os.path.join(SUM, 'reviews', 'round2', 'adoption-table-round2.md'), encoding='utf-8').read()
rec('R29', ['22'], '§4 の (6) は草案2 の新しい誤りを Z01 だけ挙げるが、二巡目の採否の表の検分票は Z01・Z03・Z04 を起草者の新しい誤りとする',
    '採否の表に「起草者の新しい誤り（Z01・Z03・Z04）」: %s／草案3 の §4 の (6) に「Z03」: %s' % ('起草者の新しい誤り（Z01・Z03・Z04）' in at2, 'Z03' in d3sec('## 4. ', '## 5. ')), '再現')
# ---- R30 照らしの記録の番号の重なり ----
rp2 = open(os.path.join(SUM, 'reviews', 'round2', 'repro-round2.md'), encoding='utf-8').read()
rec('R30', ['21'], '二巡目の照らしの記録の id（Z13b・Z25・Z26）が、採否の表の同じ番号と別の所見を指す', '照らしの記録の Z25 の主張の頭: 「%s」／採否の表の Z25 の頭: 「%s」' % (
    [l for l in rp2.split(NL) if l.startswith('| Z25 ')][0].split('|')[3].strip()[:30], [l for l in at2.split(NL) if l.startswith('| Z25 ')][0].split('|')[3].strip()[:30]), '再現')
# ---- R31 感度閾値での余地の升（参考の数） ----
c2 = [x for x in CJ['calc2_rows']]
k_on, k_o, k_u = 'Onull', 'O', 'Onull-Ncold'
rate = {}
for x in CJ['calc1_rows']:
    rate[(x['stage'], x['size'], x['scenario'], x['arm'])] = x['rate']
room = {}
for lo, hi in ((0.05, 0.95), (0.03, 0.97), (0.08, 0.92)):
    cells = []
    for x in c2:
        rs = [rate[(x['stage'], x['size'], x['scenario'], a)] for a in (k_on, k_o, k_u)]
        if all(lo <= r <= hi for r in rs):
            cells.append('%s %s %s' % (x['stage'], x['size'], x['scenario']))
    room['%s/%s' % (lo, hi)] = cells
rec('R31', ['21', '22'], '参考: 余地の升は、感度 0.03／0.97 で 6（4B N1・8B N1・32B N2・4B S1・4B S4・4B SK）、0.08／0.92 で 2（8B N1・4B SK）。錨の 4B-2507 はどの閾値でも 0。V′ もどの閾値でも 0',
    '閾値ごとの余地の升（厳密な不等号・計算の出力の率から）: %s' % json.dumps(room, ensure_ascii=False), '再現（草案3 は一巡目の照らしの記録を指す）')
# ---- R32 0/40 の上端 ----
cp = 1 - 0.025 ** (1 / 40)
z = 1.959963984540054
wil = (0 + z * z / 2 + z * math.sqrt(0 + z * z / 4)) / (40 + z * z)
rec('R32', ['21', '22'], '0/40 の 95% の上端は、Clopper–Pearson で 0.0881、Wilson で 0.0876（どちらも 0.05 を超える）', 'Clopper–Pearson %.4f・Wilson %.4f' % (cp, wil), '再現')
# ---- R33 0.6B の床と書式外（gemini-5） ----
fl6 = [x for x in CJ['calc1_rows'] if x['stage'] == 'A' and x['size'] == '0.6B' and x['rate'] < 0.05]
maj = [x for x in fl6 if x.get('format_out', 0) * 2 > x['n_ok']]
rec('R33', ['g5'], '0.6B の床（21 升）の多くが書式外の多発に起因する', '0.6B の床の升 %d・書式外が分母の過半の升 %d（%s）' % (
    len(fl6), len(maj), '・'.join('%s %s %d/%d' % (x['scenario'], x['arm'], x['format_out'], x['n_ok']) for x in maj)), '一部（床の升の数は合う・書式外が過半の升は床の一部）')
# ---- R34 gemini-6 の検算の値 ----
pick = {('8B', 'N1'): None, ('4B', 'S4'): None, ('4B', 'SK'): None}
for x in c2:
    if x['stage'] == 'A' and (x['size'], x['scenario']) in pick:
        pick[(x['size'], x['scenario'])] = '%.3f／%.3f／%.3f' % (x['logor_down'], x['logor_up'], x['abs_diff_up_minus_down'])
rec('R34', ['g6', 'g5'], '余地のある三升の下向き・上向き・絶対値の差は 8B N1 −0.460／1.329／0.869・4B S4 −0.914／1.324／0.410・4B SK −1.535／0.756／−0.779。余地は段階 A で 3／35・V′ で 0／4。向きの印は 0.6B N2 と 8B SK',
    '計算の出力: %s／余地の升: 段階 A %d／%d・V′ %d／%d／向きの印（下向きが正）: %s' % (
        json.dumps({'%s %s' % k: v for k, v in pick.items()}, ensure_ascii=False), sum(1 for x in c2 if x['stage'] == 'A' and not x['no_room']), sum(1 for x in c2 if x['stage'] == 'A'),
        sum(1 for x in c2 if x['stage'] != 'A' and not x['no_room']), sum(1 for x in c2 if x['stage'] != 'A'), '・'.join('%s %s %s' % (x['stage'], x['size'], x['scenario']) for x in c2 if x['down_positive'])), '再現')
# ---- R35 V′ の「O が最小」の前の句（claude-ai-22 の Z20） ----
h13, w13 = where('Vp', '6 土台の中で O が最小なのは S1 のみ')
rec('R35', ['22'], 'V′ の「O が最小」の前の句（O の上昇幅は +13.0〜+55.5 pt）が落ちている', '「O が最小」の行 %s（%s）・同じ行の「O が最小」の前の字: 「%s」・草案3 に「+13.0 pt」: %s' % (
    h13, w13, line('Vp', h13[0]).split('6 土台の中で O が最小')[0][-60:], '+13.0 pt' in D3), '一部（上昇の値は §2.2 の四つ目の子の箇条にある）')
# ---- R36 検分票の太字の本数の文 ----
rec('R36', ['22'], '検分票の「草案2 の検分票の太字の印を除いた本数は百三十六本の数えで、§2 の答えに限ると一本少ない」に数が無く、読めない', '草案3 の検分票の該当の文: %s' % (
    [s for s in kv.split('。') if '太字の印を除いた本数は' in s][0].strip()[:120]), '再現')
# ---- R37 選びの決まり (4) の字 ----
ad1 = open(os.path.join(SUM, '00-frame-addendum1-2026-10-02.md'), encoding='utf-8').read()
rec('R37', ['21', '22'], '選びの決まり (4) の字を追記一から変えた（V′ を足した）が、ずれの記帳が無い', '追記一の (4) に「追補 V′」: %s・草案3 の (4) に「追補 V′ の §0 の見出し」: %s・検分票に「(4)」: %s' % (
    '追補 V′' in [l for l in ad1.split(NL) if l.startswith('4. 各段の小節は')][0], '追補 V′ の §0 の見出しと、追補 M の §0 の 4 が定める' in D3, '(4)' in kv), '再現（Z13 の扱いの欄は「V′ にも当てる」）')

res = {'kind': 'repro_final_interim_summary', 'tool': 'summary/reviews/final/make_repro_final.py v0', 'draft3_sha16': '55C9D3B0647E6E21',
       'made_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
       'checks': out, 'counts': {v: sum(1 for x in out if x['verdict'].startswith(v)) for v in ('再現', '一部', '不再現', '照らせない')},
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
L = ['# 最終の巡の票の事実の主張の照らし（器・%s 日本時間）' % res['made_jst'], '', '- 器: `make_repro_final.py` v0。票の名: 20・21・22＝claude-ai-20・21・22、g5・g6＝gemini-5・6。読みは付けない。照らした草案は草案3（SHA16 55C9D3B0647E6E21）。', '',
     '| id | 票 | 主張 | 器の結果 | 照らし |', '|---|---|---|---|---|']
for x in out:
    L.append('| %s | %s | %s | %s | %s |' % (x['id'], '・'.join(x['voters']), x['claim'].replace('|', '／'), x['result'].replace('|', '／'), x['verdict']))
L += ['', '- 数え: %s' % json.dumps(res['counts'], ensure_ascii=False), '', res['clause'], '']
for x in L:
    assert x.count('|') in (0, 6) or not x.startswith('|'), '表の区切りの数: ' + x[:60]
if not DRY:
    with open(OJ, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    open(OM, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('checks %d | %s | %s' % (len(out), res['counts'], '書かない（--dry）' if DRY else '書いた'))
for x in out:
    print(' ', x['id'], x['verdict'], '|', x['result'][:400])
