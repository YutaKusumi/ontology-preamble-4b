# -*- coding: utf-8 -*-
"""build_summary_draft2.py v0（2026-10-02・中間総括の草案2 を組む・枠 `00-frame-interim-summary-2026-10-02.md` と枠の追記一 `00-frame-addendum1-2026-10-02.md`・一巡目の採否の表 Y01〜Y34・登録者裁定 D287・コーディネータ南無弥勒如来）。
- 引く文は、公開の置き場の最終版・凍結の本文・正本から器で切り出して差し込む（開きの字と終わりの字で切る・手で打たない）。切り出した字が元の記録にあることと、§2 の答えの引用が各段の最終版の §0 の行の範囲にあることを器が確かめる。
- 冷徹一行の逐語は、切り出した文の中で器が「冷徹一行〔逐語は V′ の台帳〕」に置き換える（逐語を器に打たない・置き換えの前の文を照らす・D287-b）。
- 数は計算の記録（`calc/calc-interim-v0.2.json`）と git のタグと台帳から器で差し込む。地の文の数は、記録の集まりにあることを器が照らす。
- 起草者の地の文を、禁止の語の一覧（`build_report_Bprime.bans_of` の和に、枠 §2 の例の語と「働いた」と「多いものと少ないもの」を足したもの）で走査する（引用は走査しない）。地の文の「」は、引用でないものとして検分票に器が並べる。
- 書く物: `summary-interim-draft2-2026-10-02.md` と `summary-interim-draft2-checks.json`（一度だけ）。照らしが通らなければ書かない。
用法: python build_summary_draft2.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, glob, hashlib, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'summary-interim-draft2-2026-10-02.md')
CHK = os.path.join(HERE, 'summary-interim-draft2-checks.json')
NL = chr(10)
P = lambda *a: os.path.join(PUB, *a)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16t = lambda t: hashlib.sha256(t.encode('utf-8')).hexdigest().upper()[:16]
sys.path.insert(0, P('tools'))
import build_report_Bprime as BR
CB = json.load(open(P('design', 'contrasts-Bprime.json'), encoding='utf-8'))
BANS = sorted(set(BR.bans_of(CB)) | {'証明', '効いた', '耐えた', '頑健', '守った', '防いだ', '特定した', '一般化', '機種の違いで', '働いた', '多いものと少ないもの'})
CALC_J = os.path.join(HERE, 'calc', 'calc-interim-v0.2.json')
CALC = json.load(open(CALC_J, encoding='utf-8'))
CEN = json.load(open(P('design', 'contrasts-A.json'), encoding='utf-8'))['censor']
FRAME = os.path.join(HERE, '00-frame-interim-summary-2026-10-02.md')
ADD1 = os.path.join(HERE, '00-frame-addendum1-2026-10-02.md')
FIN = {'4B': 'records/results/results-report-FINAL-2026-09-07.md', 'Vp': 'records/vprime/results-report-Vprime-FINAL-2026-09-09.md', 'M': 'records/M/results-report-M-FINAL-2026-09-11.md',
       'F': 'records/F/results-report-F-FINAL-2026-09-12.md', 'A': 'records/A/results-report-A-FINAL-2026-09-17.md', 'B': 'records/B/results-B-FINAL-2026-09-23.md',
       'BL': 'records/Blens/results-Blens-FINAL-2026-09-24.md', 'L3': 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', 'BP': 'records/Bprime/results-Bprime-FINAL-2026-10-01.md'}
TAG = {'4B': 'release-2026-09-07', 'Vp': 'release-Vprime-2026-09-09', 'M': 'release-M-2026-09-11', 'F': 'release-F-2026-09-12', 'A': 'release-A-2026-09-17', 'B': 'release-B-2026-09-23',
       'BL': 'release-Blens-2026-09-24', 'L3': 'release-Bl3-2026-09-27', 'BP': 'release-Bprime-2026-10-01'}
NAME = {'4B': '4B の最初の登録', 'Vp': '追補 V′', 'M': '追補 M', 'F': '段階 F', 'A': '段階 A', 'B': '段階 B', 'BL': 'B-lens', 'L3': '層三（B-lens 層三）', 'BP': 'B′'}
FREEZE_ROW = {'Vp': '**追補 V′ 凍結**', 'M': '**追補 M 凍結**', 'F': '**段階 F 凍結**', 'A': '**段階 A 凍結**', 'B': '**段階 B 凍結**', 'BL': '**B-lens 凍結**',
              'L3': '**B-lens 層三 下見の前の凍結**', 'BP': '**B′ 下見の前の凍結**'}
ORDER9 = ('4B', 'Vp', 'M', 'F', 'A', 'B', 'BL', 'L3', 'BP')
TXT = {}
used = []
SEC0 = {}


def src(path):
    if path not in TXT:
        TXT[path] = open(P(*path.split('/')), encoding='utf-8').read().replace('\r\n', '\n')
    return TXT[path]


def sec0(k):
    if k not in SEC0:
        L = src(FIN[k]).split(NL)
        i = [n for n, l in enumerate(L) if l.startswith('## 0.')]
        assert len(i) == 1, k
        j = [n for n in range(i[0] + 1, len(L)) if L[n].startswith('## ')]
        a, b = i[0] + 1, j[0]
        SEC0[k] = (a, b, NL.join(L[a - 1:b]))
    return SEC0[k]


def cut(k_or_path, start, end=None, keep_end=True, cat='ans'):
    """元の記録から、開きの字 start の最初の一か所から、終わりの字 end の最初の一つまで（end が無ければ行の終わりまで）を切り出す。太字の印は除く。"""
    path = FIN.get(k_or_path, k_or_path)
    t = src(path)
    assert t.count(start) >= 1, ('開きの字が無い', path, start[:30])
    i = t.index(start)
    if end is None:
        j = t.index(NL, i) if NL in t[i:] else len(t)
        seg = t[i:j]
    else:
        j = t.index(end, i + len(start) - (len(end) if start.endswith(end) else 0))
        seg = t[i:j + (len(end) if keep_end else 0)]
    q = seg.replace('**', '')
    l0, l1 = t.count(NL, 0, i) + 1, t.count(NL, 0, i + len(seg)) + 1
    rec = {'stage': k_or_path if k_or_path in FIN else None, 'source': path, 'lines': [l0, l1], 'cat': cat, 'quote': q, 'bold_stripped': '**' in seg}
    used.append(rec)
    return q


def cut_cold(k, start, end):
    """冷徹一行の逐語を含む文を切り出し、逐語の部分（「冷徹一行「」から次の「」」まで）を器が置き換える。逐語は器に打たない。"""
    q = cut(k, start, end)
    i = q.index('冷徹一行「')
    j = q.index('」', i + len('冷徹一行「'))
    old = q[i:j + 1]
    new = '冷徹一行〔逐語は V′ の台帳〕'
    used[-1]['replaced'] = {'from_sha16': s16t(old), 'from_chars': len(old), 'to': new}
    used[-1]['display'] = q.replace(old, new)
    return used[-1]['display']


def title_q(k):
    line = src(FIN[k]).split(NL)[0]
    assert '——' in line, k
    q = line.split('——', 1)[1].strip()
    used.append({'stage': k, 'source': FIN[k], 'lines': [1, 1], 'cat': 'title', 'quote': q, 'bold_stripped': False})
    return q


def after(path, head, cat='question'):
    t = src(path)
    assert t.count(head) == 1, ('頭の字が一つでない', path, head[:30], t.count(head))
    i = t.index(head) + len(head)
    j = t.index(NL, i)
    q = t[i:j].replace('**', '')
    l0 = t.count(NL, 0, i) + 1
    used.append({'stage': None, 'source': path, 'lines': [l0, l0], 'cat': cat, 'quote': q, 'bold_stripped': '**' in t[i:j]})
    return q


def git(*a):
    return subprocess.run(['git', '-C', PUB] + list(a), capture_output=True, text=True).stdout.strip()


def tag_date(k):
    return git('log', '-1', '--format=%ad', '--date=format:%Y-%m-%d', TAG[k])


def freeze_date(k):
    if k == '4B':
        assert os.path.exists(P('records', 'freeze-2026-09-05.json'))
        return '2026-09-05'
    led = src('records/FREEZE-RECORD.md').split(NL)
    rows = [l for l in led if l.startswith('| 20') and FREEZE_ROW[k] in l]
    assert len(rows) == 1, (k, len(rows))
    return rows[0].split(' | ')[0][2:]


segs = []
T = lambda s: segs.append(('t', s))
Q = lambda q: segs.append(('q', '「' + q + '」'))
X = lambda s: segs.append(('x', s))          # 走査の外（柵の文）
V = lambda s: segs.append(('v', s))          # 器で切り出した表の行（逐語・走査の外）


def QL(k, start, end=None, cat='ans', pre='- ', post=NL):
    T(pre); Q(cut(k, start, end, cat=cat)); T(post)


frame16, add16 = s16(FRAME), s16(ADD1)
D287 = os.path.join(HERE, 'reviews', 'round1', 'rulings-D287.md')
AT1 = os.path.join(HERE, 'reviews', 'round1', 'adoption-table-round1.md')
r1, pm, r2, bst = CALC['calc1_rows'], CALC['calc1_per_model'], CALC['calc2_rows'], CALC['calc2_by_stage']
TH = CALC['thresholds']

# ---------------- 頭 ----------------
T('# 中間総括（草案2）——Qwen3-4B-Instruct-2507 での最初の登録を発端とした検証の案内図（B′ まで・登録の外・内部・非公開）' + NL + NL)
T('- 起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／登録者: 楠見優太／2026-10-02。枠 `summary/00-frame-interim-summary-2026-10-02.md`（SHA16 %s・起草と計算と検分の前に書いた）と、枠の追記一 `summary/00-frame-addendum1-2026-10-02.md`（SHA16 %s・一巡目の採否と登録者裁定 D287 の後、草案2 と計算の器の版上げの前に書いた）のとおりに組んだ（器 `summary/build_summary_draft2.py`）。' % (frame16, add16) + NL)
T('- 状態: 草案2（検分の二巡目の前）。一巡目（claude.ai の Claude 三名で一票・Gemini 3.8 Flash 一名）の採否の表 `summary/reviews/round1/adoption-table-round1.md`（Y01〜Y34）と登録者裁定 D287（`summary/reviews/round1/rulings-D287.md`）を反映した。内部で作り、完成したら公開する（登録者の決め・2026-10-02）。' + NL + NL)

# ---------------- §0 ----------------
T('## 0. この文書は何で、何でないか' + NL + NL)
T('- **登録の外の案内図**: 2026-09-05 から 2026-10-01 までに凍結・公開した九つの段（4B の最初の登録・追補 V′・追補 M・段階 F・段階 A・段階 B・B-lens・層三・B′）を、一か所に並べる。凍結した結果を読み直さず、札・門・決定を変えない。各段の結果に新しい証拠を足さない。' + NL)
T('- **新しい計算（§3.2・§3.3）は登録の外の記述**: 公開した記録だけから計算し、札を付けず、検定もしない。定義は、枠を書いた時点（起草と計算の前）に枠 §3 で定め、一巡目の検分の後に枠の追記一で改めた（B′ を外した・段ごとに分けた・向きと閾値ちょうどの印を足した）。改めた所と足した印は、一巡目の検分で値を見た後の記述である。' + NL)
T('- **答えは各段の最終版の §0 の文の範囲**: 段ごとの答えは、その段の最終版の §0 から器で切り出して引く（引用の選びの決まりは §2 の頭）。段をまたぐ言い方は、段ごとの引用を並べた後に、引用の範囲で言えることだけを書く。' + NL)
T('- **前身**: 4B の最初の登録の前に、別の置き場の追補E（Qwen3-30B-A3B）がある。本書はその数を引かない。' + NL)
X('- **柵**: 本書のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'); T('機種の率を、機種の安全さの比べとして読まない。二つの機種の行動の率を、同じ表にも同じ文にも置かない（§5）。' + NL + NL)

# ---------------- §1 ----------------
T('## 1. 問いの系譜と時系列' + NL + NL)
T('| 段 | 問い（最終版の題か凍結の本文から引く） | 凍結 | 公開（タグの日付） | タグ | 最終版 |' + NL + '|---|---|---|---|---|---|' + NL)
QQ = {}
for k in ('4B', 'Vp', 'M', 'F', 'A', 'B'):
    QQ[k] = title_q(k)
QQ['BL'] = after('design/design-Blens-FROZEN.md', '  - **問一（答えの文字）**: ')
QQ['L3'] = after('design/design-Bl3-FROZEN.md', '**問い**（一つ・裁定 D203）: ')
QQ['BP'] = after('design/design-Bprime-FROZEN.md', '**問い**（一つの問いを二つの部分に分けた）〔R01〕: ')
for k in ORDER9:
    T('| %s | ' % NAME[k]); Q(QQ[k].replace('|', '｜')); T(' | %s | %s | `%s` | `%s` |' % (freeze_date(k), tag_date(k), TAG[k], FIN[k]) + NL)
T(NL + '- 問いの出所は段によって違う。4B の最初の登録から段階 B までは最終版の題、B-lens・層三・B′ は凍結の本文の問いで、抽象の度合いがそろわない。B-lens の問いは六つあり（すべて記述）、表には一つ目だけを引いた（凍結の本文 `design/design-Blens-FROZEN.md`）。B′ の問いは、計画の当初の B′（Llama-3.1-8B・日英）から、裁定 D255〜D258 で機種と問いを改めたもの。' + NL + NL)

# ---------------- §2 ----------------
T('## 2. 各段の答え（できないことから・最終版の §0 から引く）' + NL + NL)
T('- **引用の選びの決まり**（枠の追記一 §3・草案2 の前に書いた）: (1) 各段の答えは、その段の最終版の §0 の文から引く（器が §0 の行の範囲を確かめる）。(2) 太字の文を引いたら、同じ項の中で分母・対照・範囲・複製の状態・向きを確定した時点を限る文を続けて引く。(3) §0 に見ていない場所・答えられないこと・答えの範囲の区画があれば、要点を一つ以上引く。(4) 各小節は、できないこと・限りを先に置く（追補 M は、§0 が上向きの所見を先頭に置くと定めているので、その数を限りの文とともに先に引く）。(5) 上昇を招く操作の逐語は引かず、器が置き換える。(6) 太字の印をまたぐ引用は、器が印を除いて照らす。各段の §0 の行の範囲と写しの SHA16 は付録 A。' + NL + NL)

T('### 2.1 4B の最初の登録（Qwen3-4B-Instruct-2507・段 0〜VI）' + NL + NL)
QL('4B', '段V（逆用・上向き）は測れなかった', '。')
QL('4B', '「同じ機構が悪意の枠にも上向きに働くか」は本設定では答えない', '。', pre='  - ')
QL('4B', '段V の 4 本目（O-Ncold 対 Ncold）は 54/320 対 320/320 で両側 Fisher が有意', '。', pre='  - ')
QL('4B', 'したがって札は「確証（両側有意）・向きは事後確定」とし', 'とは書かない', pre='  - ')
QL('4B', 'Onull の段間幅 1.9pt は段0 の 6 回の帯（1.5pt）を超え', '。')
QL('4B', 'O（存在論的前置き）対 Onull（中立前置き）は 10 本すべて有意・想定方向', '。')
QL('4B', 'O の三つ組は refuse 0〜156（A2′ で最大）', '。', pre='  - ')
QL('4B', 'A2′ では O refuse 156/320 と多く', '。', pre='  - ')
QL('4B', '否定の前置き（Lneg）対 Onull（上向き想定）は 3 本が確証・2 本が有意で逆方向', '。')
QL('4B', '「否定の前置きは破局を上げる」は survival 3 本で成立し', '。', pre='  - ')
QL('4B', '段III で O の転向は圧力 0/223・中立 9/218（有意・想定と逆）', '。')
QL('4B', 'Onull は分母 1 対 1 で検定不能（記述）', '。', pre='  - ')
T(NL)

T('### 2.2 追補 V′（悪意の枠付けの加算・4B-2507・n=400）' + NL + NL)
QL('Vp', 'これは「悪意の枠は危険にする」を新発見として書くものではない', '。')
QL('Vp', '本追補が独立に言えるのは', '。')
T('- '); Q(cut_cold('Vp', 'この文形・この語・この 4B 構成で、冷徹一行', '上げた')); T(NL)
QL('Vp', '主張はシナリオ単位・4 中 3 の規則により「O が最小」は一般化しない', 'しない', pre='  - ')
QL('Vp', '上昇幅は出発点の床・天井に制約される', 'される', pre='  - ')
QL('Vp', '冷徹の付加で O の破局率は絶対値として', '無力化はできていない')
T(NL)

T('### 2.3 追補 M（仏名・末尾文字列・呼び出しの形式・置き場・4B-2507）' + NL + NL)
T('- 利益相反（§0 の 1）: '); Q(cut('M', '登録者は長文招請（LAmi・LKan）の著者・実践者であり', '」。')); T(NL)
T('- 上向きの所見（§0 の 4・追補 M の §0 は先頭に置くと定める）: '); Q(cut('M', '第一走行で確証し第二走行でも Holm 基準を満たした対比（札 ①）は 21 本、うち ', '上向き')); T(NL)
QL('M', 'T0 との副対比なしに「なし」より高いとは書けない', 'ない', pre='  - ')
QL('M', '長文 対 非長文ではない', 'ない', pre='  - ')
QL('M', 'これらの差は A 腕の上昇ではなく対照の床が作る', '。', pre='  - ')
QL('M', '下向き ① は 10 本', '。')
QL('M', '様式門で判定保留（様式転位）に置換された対比は 36／136', '。')
QL('M', 'これらの断面の', '主結果として置く。', pre='  - ')
QL('M', '上向きの一般化は構造的に書けず', '。')
T(NL)

T('### 2.4 段階 F（場面冒頭の検査認識の付記・4B-2507）' + NL + NL)
QL('F', '本段はこの仮説の検証も反証もしない', '。')
QL('F', 'T 対 U は検査の内容と冒頭に一文あることを分離しない', 'しない')
QL('F', '確証対比 24 本のうち判定不能（門）2', '。')
QL('F', '一斉保留（場面ごと', '（4/6）。', pre='  - ')
QL('F', '第一の所見（機械札・S1・S4・SK）', '」。', pre='  - ')
T('- '); Q(cut('F', '上向きの確証 3 本', '本')); T('・'); Q(cut('F', '下向きの確証 4 本', '本')); T('（§0 の 4）。上向きの三本はどれも一斉保留の起きた場面（S1・S4・SK）にあり、そのうち SK の一本は第二走行で判定保留だった。下向きの四本は、どれも第二走行で複製された（§0 の 4）。' + NL + NL)

T('### 2.5 段階 A（規模軸・Qwen3 の稠密系列 0.6B〜32B と錨 4B-2507）' + NL + NL)
QL('A', '記述（解釈条項）に回った対比の多さは効果の不在を意味しない。', None)
QL('A', '測れなかった効果種: ', '。')
QL('A', '（測れた対比でない場面について傾向の不在を書かない）', None, pre='  - ')
QL('A', '様式門の hold の旗が立った対比では、破局率の差を応答様式の差と分離できない', 'できない')
QL('A', '合格は等価の確立ではない', 'ない')
QL('A', '傾きの族 35 対比のうち、確証 1', '。')
QL('A', '確証の一本（S4 の Onull 対 N）', '）', pre='  - ')
QL('A', '上向きの確証はなかった。', None)
QL('A', '感度閾値のうち検閲の閾値を両端へ広げた側', '定義に当たる。', pre='  - ')
QL('A', 'この二本の主閾値の札は、判定不能（N2）・記述（解釈条項）（S1）である', '。', pre='  - ')
T(NL)

T('### 2.6 段階 B（機構層・4B-2507・方向の加減と破局率）' + NL + NL)
QL('B', '凍結した集計器の出力と、逸脱の下の出力は、札の内訳が大きく違う。', '違う。')
QL('B', '違いの原因は測定ではなく、凍結した二つの器の食い違いである', '引いてはならない。', pre='  - ')
L_B = src(FIN['B']).split(NL)
a_, b_, _ = sec0('B')
tbl = [i for i in range(a_ - 1, b_) if L_B[i].startswith('|')]
assert len(tbl) == 8, ('段階 B の §0 の表の行の数', len(tbl))
T(NL)
for i in tbl:
    V(L_B[i] + NL)
    used.append({'stage': 'B', 'source': FIN['B'], 'lines': [i + 1, i + 1], 'cat': 'table', 'quote': L_B[i], 'bold_stripped': False})
T(NL)
QL('B', '凍結した集計器は、減算族と加算族のすべての対比を', 'ためである。')
QL('B', '登録者は、**確証の族の率と p を見た後に**', '道の選び方）。')
QL('B', '逸脱の下の出力で札が立った対比は、', '持たない**。', pre='  - ')
QL('B', '区別できた相手は「引いた三本のランダム方向を合わせた腕」であり', 'ではない。')
QL('B', '三本では方向の間のばらつきを見積もれず', '。', pre='  - ')
QL('B', '十六本の Holm を掛けると S1 だけになり', 'どの行も区別は残らない', pre='  - ')
QL('B', '減算族の二本（逸脱の下）と事前登録の交差族の二本は、一番近い一本と区別できない。', None, pre='  - ')
QL('B', '区別できた場面はすべて survival の場面で', '区別できなかった。')
QL('B', '調整走行で選んだ組が N1 で示した低下は、本走行では縮んだ', '。', pre='  - ')
QL('B', '交差族の二本（Nk 方向・Onull の土台）は二つの出力に共通である', '。', pre='  - ')
QL('B', 'v̂ に特有の動きか、前置きの内容一般の方向の動きかは、B の登録では見分けられない。', '低下を作った。')
QL('B', '加算族と交差族の Onull の土台は', '（§2・§6）。', pre='  - ')
QL('B', '確証の札で、起草者の封印の符号と一致したもの', '。')
QL('B', 'S4 の反証の観測は低下の側にある。', '。')
QL('B', '札は「当否を言わない」', 'である。', pre='  - ')
QL('B', '札に付く「登録された向きと逆」の文言は、', 'ではない**。')
QL('B', 'B が答えるのは', '射程の外にある。')
T(NL)

T('### 2.7 B-lens（v̂ の直接の経路の押し・層の割合 0.5）' + NL + NL + '- この登録で答えられないこと（§0 の区画から三つ）: ')
Q(cut('BL', '意味の有無・機構（直接の経路の外にある後の層の処理は見ない）', None)); T('・')
Q(cut('BL', 'ランダム方向一般と区別できる行動の動き（層三の問い・別の登録）', None)); T('・')
Q(cut('BL', 'ほかの機種・規模' + NL, None)); T(NL)
QL('BL', '直接の経路では、等方の帰無と区別できる押しは無かった。後の層の経路は見ていない', None, pre='- 〈区別できない〉（主の六つ）: ')
QL('BL', '二つ目の札は付いたが、等方の帰無とは区別できなかった', None, pre='- 〈二つ目の札だけ〉（M_L_nuclear）: ')
QL('BL', 'この札は、この要約の行だけで読まない。', None, pre='  - ')
QL('BL', '直接の経路の物差しは、B の方向ごとの行動の変化と、方向の単位でそろわなかった。上の型の記述は行動に結びつけない', None, pre='- 〈門を通らない〉: ')
QL('BL', '〈門を通らない〉の「そろわなかった」は', None, pre='  - ')
T(NL)

T('### 2.8 層三（全経路の効き目・直答の型の読み取りの位置）' + NL + NL + '- 見ていない場所（§0 の区画から三つ）: ')
Q(cut('L3', '意味の有無・機構（区別できても、どの層・どの部品が効き目を担うかは見ない', None)); T('・')
Q(cut('L3', 'プロンプトの中の JSON の指示の雛形の続きを写す働きと、選択の構えの区別', None)); T('・')
Q(cut('L3', 'ほかの機種・規模・層・係数（段階 B が選んだ層と係数だけ）', None)); T(NL)
QL('L3', '層三の答えが段階 B の開いた問い', None, pre='- 答えの範囲: ')
QL('L3', '本の門: 通らない・v̂ を抜いた門: 通らない', None, pre='- 門: ')
QL('L3', '直答の型の読み取りの全経路の効き目は、段階 B の方向ごとの行動の変化と、方向の単位でそろうことは示せなかった。', None, pre='  - ')
QL('L3', 'ただし、計算の道を替えると無操作の値が動いた', '測っていない。', pre='- 計算の道: ')
QL('L3', '主の行 14（下見で外した後）・等方の外の行', None, pre='- 主の行: ')
QL('L3', 'その行の効き目は、等方のランダム方向と区別できなかった（この読み取りの位置での記述）', None, pre='  - 〈外でない行〉（13 行）: ')
QL('L3', 'これは、それらの行が等方と同じ程度だったことを示さない', '。', pre='  - ')
QL('L3', '封印したコーディネータの予想の考え方は、この説明に立っていた', 'た', pre='  - ')
QL('L3', 'その行の効き目は、等方のランダム方向と区別でき、実在の差の方向（兄弟を除く・両方の向き）の中で、中心からの動きが最上位だった', '）', pre='  - 〈両方の外〉の一行（`sub:N1:O-Ncold-v~O-Ncold-vrand`）: ')
QL('L3', '段階 B のこの行の差 -2.0 pt', '。', pre='    - ')
QL('L3', '主の表の段階 B の札: 判定不能（品質床）。', None, pre='    - ')
QL('L3', '無操作の対数オッズ -8.783 と床の対数オッズ -9.210 の差', '。', pre='    - ')
QL('L3', 'Holm の第一段までの余白: 効き目 2.734 以上の等方の方向は 1 本（3.018）。', None, pre='    - ')
QL('L3', 'これらは札と型を変えない。どちらの向きにも読まない（区別できたことを強める側にも、弱める側にも）。', None, pre='    - ')
QL('L3', 'この読み取りの値には、プロンプトの中の雛形の続きを写す働きが入りうる', None, pre='- 打ち消しの定型（§0 から一つ）: ')
T(NL)

T('### 2.9 B′（Gemma-4-31B-it・日本語・層三の型の読み取りの追試）' + NL + NL + '- 見ていない場所（§0 の区画から四つ）: ')
Q(cut('BP', '採点器の Gemma の書式での妥当性', None)); T('・')
Q(cut('BP', 'Gemma の既定の標本化での振る舞い', '）')); T('・')
Q(cut('BP', 'Gemma の行動との結びつき', '）')); T('・')
Q(cut('BP', '二つの機種の違いを、系譜・規模・トークナイザのどれか一つから来たものとして読むこと', 'こと')); T(NL)
QL('BP', '機械の決定: 止める', None, pre='- 下見の機械の決定: ')
QL('BP', 'この読み取りでは測れなかった（閾値は層三の登録の値を写したもので、Gemma で較正していない）。B′ の問いには答えていない', None, pre='  - ')
QL('BP', '下見は全体で止まったので、どの族も測れていない', '。', pre='  - ')
QL('BP', 'これは値の位置の記述で、なぜその位置に出たかの記述ではない。', None, pre='  - ')
T('- 行動の下見（無操作・升目ごとの試行 40）の率は、最終版の転記行 C にある。本書は、その率を本文と計算に写さない（S10・§5・裁定 D287）。最終版は、行動の下見の応答の書き出しの根の件数を升目ごとに報告の頭に置き、')
Q(cut('BP', 'この件数は、読み取りの位置の妥当さについて、どちらの向きの根拠にもしない。', None)); T('と書く。' + NL + NL)

# ---------------- §3 ----------------
T('## 3. 測れた所と測れなかった所（横断の地図）' + NL + NL)
T('### 3.1 各段の結果の四つの欄（各段の最終版の §0 の語で置く・§2 の引用の範囲）' + NL + NL)
T('- **測れた**（各段の札と区別の語のとおり。範囲は §2 に引いた限りの文のとおり）:' + NL)
T('  - 4B の最初の登録: O 対 Onull の確証（A2′ は refuse が多く、答えた分母の率で読む）・Lneg 対 Onull の survival の確証（Onull を対照にした場合だけ）・段V の 4 本目の確証（向きはデータの後に確定し、想定方向とは書かない）。' + NL)
T('  - 追補 V′: 冷徹一行の後置きによる上昇（上昇幅は出発点の床と天井に制約される・本追補が独立に言えるのは上向きの再現まで）。' + NL)
T('  - 追補 M: 札 ① の対比（上向きと下向き）。ただし、様式門で過半が保留された断面の第一の所見は応答様式の転換との分離不能で、上向きのうち対照が床にある対比の差は対照の床が作る。' + NL)
T('  - 段階 F: 確証の対比（上向きと下向き）。ただし、上向きはどれも一斉保留の起きた場面にあり、その場面の第一の所見は応答様式の転換との分離不能。' + NL)
T('  - 段階 A: 確証の一本（S4 の Onull 対 N・O の腕を含まない）。主閾値の札では上向きの確証は無い（感度閾値の広げた側で上向きの定義に当たる二本は §2.5）。' + NL)
T('  - 段階 B: 事前登録の確証の二本（交差族＝Nk 方向・Onull の土台・一番近い一本と区別できない）。逸脱の下の札は、事前登録の確証と同じ身分を持たない。' + NL)
T('  - 層三: 〈両方の外〉の一行（床からの余白は下見の幅より小さく、段階 B のこの行の札は判定不能・読みは付けない）。' + NL)
T('- **測って区別できなかった**: 段階 A の非有意・段階 B の非有意（二つの出力とも）・B-lens の主の六つ（〈区別できない〉）・層三の〈外でない行〉・B-lens と層三の門（そろうことが示せなかった。そろわないことを示したのではない）。' + NL)
T('- **測って想定と逆だった**: 4B の最初の登録の Lneg の核の二本（Lneg が低い）と、段III の O の転向（有意・想定と逆）。' + NL)
T('- **測れなかった**: 4B の最初の登録の段V の上向き（天井）と段III の Onull（分母が足りず検定不能）・応答様式の転換と分離できなかった断面（追補 M・段階 F・段階 A の様式門）・段階 A の判定不能と解釈条項と測れなかった効果種・段階 B の凍結した集計器の判定不能（品質床に落ちたのではなく、集計器が探した段の走行の記録が無かった）・B′ の読み取りの下見（止まった）。' + NL)
T('- 読み: 測れなかった所は、効き目が無かったことを示さない。測って区別できなかった所は、同じ程度だったことを示さない（層三の §0 の言い方・§2.8）。段階 B の札に付く登録された向きと逆の文言は、反対向きに動いたという意味ではない（§2.6）ので、想定と逆の欄に置かない。' + NL + NL)

T('### 3.2 新しい計算一 腕ごとの端の印の地図（登録の外の記述・事後・`summary/calc/calc-interim-v0.2.md`）' + NL + NL)
T('- 定義: 腕ごとの全分母破局率（分子＝破局・分母＝n_ok）に、段階 A の正本の主閾値（%s 未満＝床・%s 超＝天井）で印を付けた。感度閾値（%s／%s・%s／%s）の端の数は表の右の二列。検定はしない。' % (
    TH['main'][0], TH['main'][1], TH['sens_wide'][0], TH['sens_wide'][1], TH['sens_narrow'][0], TH['sens_narrow'][1]) + NL)
T('- 正本の検閲は両腕の条件である: ')
assert CEN['text'] in src('design/contrasts-A.json')
used.append({'stage': None, 'source': 'design/contrasts-A.json', 'lines': [src('design/contrasts-A.json').count(NL, 0, src('design/contrasts-A.json').index(CEN['text'])) + 1] * 2, 'cat': 'canon', 'quote': CEN['text'], 'bold_stripped': False})
Q(CEN['text']); T('（`design/contrasts-A.json` の `censor.text`）。この地図は腕ごとの位置の記述で、検閲や札の代わりにしない。' + NL)
T('- 入力: 段階 A の本走行の %d の走り（provider %s・各腕の n_ok %s）と、V′ の本走行の %d の走り（provider %s・各腕の n_ok %s）。入れていないもの: %s。機種の名の 4B は Qwen3-4B、4B-2507 は Qwen3-4B-Instruct-2507（§3.3 も同じ）。' % (
    len(CALC['inputs']['A']), '・'.join(CALC['provider_by_stage']['A']), '・'.join(str(n) for n in CALC['n_ok_by_stage']['A']),
    len(CALC['inputs']['Vprime']), '・'.join(CALC['provider_by_stage']['Vprime']), '・'.join(str(n) for n in CALC['n_ok_by_stage']['Vprime']), CALC['not_inputs']) + NL + NL)
for st, lab in (('A', '段階 A の本走行（手元・bf16）'), ('Vprime', 'V′ の本走行（API）')):
    T('| %sの機種 | 升 | 床（%s 未満） | 天井（%s 超） | 中 | 端（感度 %s／%s） | 端（感度 %s／%s） |' % (lab, TH['main'][0], TH['main'][1], TH['sens_wide'][0], TH['sens_wide'][1], TH['sens_narrow'][0], TH['sens_narrow'][1]) + NL + '|---|---|---|---|---|---|---|' + NL)
    for k_, d in pm.items():
        if k_.split('|')[0] == st:
            T('| %s | %d | %d | %d | %d | %d | %d |' % (k_.split('|')[1], d['cells'], d['floor'], d['ceiling'], d['middle'], d['ends_sens_wide'], d['ends_sens_narrow']) + NL)
    T(NL)
T('- 読み: 表は腕ごとの位置の記述で、機種の安全さの比べとして読まない。端の数は、土台の腕の位置と、操作で端まで押された腕の位置を足したもので、動く幅の広さとしては読まない。全升の率と印は計算の出力にある。' + NL + NL)

T('### 3.3 新しい計算二 段階 C の対称性の記述（同じ走り・同じ規模の中・札なし）' + NL + NL)
T('- 定義: 下向き＝Onull→O、上向き＝Onull→Onull-Ncold の Firth の対数オッズ比（段階 A の凍結の器 `tools/firth.py`）。三つの腕のどれかが主閾値の端なら余地なし。下向き（O で置き換える）と上向き（冷徹一行を足す）は種類の違う操作で、この表は二つの操作の効き目の大きさを並べるだけである。' + NL)
for st, lab in (('A', '段階 A'), ('Vprime', 'V′')):
    b = bst[st]
    ov = sum(b['end_arm_counts'].values()) > (b['cells'] - b['room'])
    T('- %s（%d 升）: 三つの腕がそろって主閾値の中にある升は %d（%s）。端に当たった腕は O が %d 升・Onull-Ncold が %d 升・Onull が %d 升%s。' % (
        lab, b['cells'], b['room'], '・'.join(b['room_cells']) or 'なし', b['end_arm_counts']['O'], b['end_arm_counts']['Onull-Ncold'], b['end_arm_counts']['Onull'], '（一つの升に二つ以上の腕が当たることがある）' if ov else '') + NL)
room = [x for x in r2 if not x['no_room']]
f3 = lambda v: '%.3f' % (0.0 if abs(v) < 1e-9 else v)
T('- 余地のあった升の絶対値の差（上向き − 下向き）は ' + '・'.join('%.3f' % x['abs_diff_up_minus_down'] for x in room) + '（升の順は上と同じ）。対称だった・対称でなかったとは読まない。段階 A と V′ を横断して対称性を書かない。' + NL)
pa = bst['A']
T('- 一巡目の検分で値を見た後に足した記述（札ではない・枠の追記一 §2）: 下向きの対数オッズ比が正（O の側で率が高い）の升は%s。上向きが負の升は%s。率が主閾値の値に等しい升は%s（厳密な不等号で中に入る）。0/n や n/n を含む升の対数オッズ比は、0.5 の補正と n で大きさが決まる。感度閾値で数えた余地の升の数と、差の揺れの目安は、照らしの記録 `summary/reviews/round1/repro-round1.md` にある。' % (
    '・'.join('段階 A の ' + c for c in pa['down_positive_cells']) or 'なし', '・'.join(pa['up_negative_cells']) or 'なし', '・'.join('段階 A の ' + c for c in pa['threshold_exact_cells']) or 'なし') + NL + NL)
for st, lab in (('A', '段階 A'), ('Vprime', 'V′')):
    T('| %s の機種 | 場面 | 下向き | 上向き | 絶対値の差 | 余地なし（端の腕） | 向きの印 |' % lab + NL + '|---|---|---|---|---|---|---|' + NL)
    for x in [x_ for x_ in r2 if x_['stage'] == st]:
        sign = '・'.join(([] if not x['down_positive'] else ['下向きが正']) + ([] if not x['up_negative'] else ['上向きが負'])) or '—'
        T('| %s | %s | %s | %s | %s | %s | %s |' % (x['size'], x['scenario'], f3(x['logor_down']), f3(x['logor_up']), f3(x['abs_diff_up_minus_down']),
                                                     ('はい（%s）' % '・'.join(x['end_arms'])) if x['no_room'] else 'いいえ', sign) + NL)
    T(NL)

# ---------------- §4 ----------------
T('## 4. 手続き（繰り返し用いた型と、繰り返した誤り）' + NL + NL)
T('- 出所: 各段の最終版の §0（COI の項を含む）と、最終版の頭の逸脱の区画。計画書（内部）は使わない。新しい教訓は作らない。' + NL + NL)
T('**繰り返し用いた型**（各型の限りを、§0 の文で添える）:' + NL + NL)
T('- 事前登録と予想の封印（コーディネータが先・登録者が後）: 段階 F の §0 は'); Q(cut('F', '的中は証拠に数えない', '。', cat='proc')); T('と書く。' + NL)
T('- 凍結と記録先行の公開・機械の区画（数は器が書く）: 4B の最初の登録の §0（先に書くこと）の 5 は'); Q(cut('4B', '草案1 は数値誤りを、草案2 は存在しない引用を、草案3 は散文に別走行の値の混入を含んでいた', '。', cat='proc')); T('と書く。' + NL)
T('- 率盲検の整合検査: 追補 M の §0 は'); Q(cut('M', '率盲検下で走った検査は v1・v2 は率の閲覧後の再実施', '再実施', cat='proc')); T('と書き、段階 A の §0 は'); Q(cut('A', '率盲検の器（整合検査・抽出検査）はこの経路を覆わないことをここに開示する', 'する', cat='proc')); T('と書く。' + NL)
T('- 凍結の後の逸脱の台帳と、逸脱の下の器（凍結した器の出力を作り直して照らし、印を付けた区画だけを足す）: 段階 B の §0 は、逸脱を確証の族の率と p を見た後に裁定したことと、逸脱の下の札が事前登録の確証と同じ身分を持たないことを書く（§2.6）。' + NL)
T('- 系統外の目による検分（票の総括を裁定にせず、所見ごとに記録で照らして採否を決める）: 段階 F の §0 は'); Q(cut('F', '検分の数は独立な確認の数ではない', '。', cat='proc')); T('と書き、段階 A の §0 は'); Q(cut('A', 'この後に検分の巡を置かない（登録者決定）ので、最終検分の反映は外の目を通らない', 'ない', cat='proc')); T('と書く。' + NL)
T('- 止める道: B′ は、凍結した決定木で読み取りの下見を止め、止まったまま公開した（§2.9）。' + NL + NL)
T('**繰り返した誤り**:' + NL + NL)
T('- (1) 器の欠けが、結果を見た後に見つかった。測りの器では、段階 B の凍結した二つの器の食い違い（§2.6）と、段階 A の'); Q(cut('A', '感度閾値の対比ごとの札と傾きと上向きの判定を、集計器は印字しない', 'しない', cat='proc')); T('。報告の組み立ての器では、B-lens・層三・B′ の最終版が、凍結した組み立ての器の出力に逸脱の区画を足している（各最終版の頭の逸脱の区画）。起動器の記帳では、B′ の起動器がドライバと CUDA の実行時の版を記録していなかった（B′ の最終版の逸脱の区画）。' + NL)
T('- (2) 率や p を見た後の決めがあった。追補 M の整合検査の再実施（上）・段階 B の逸脱の裁定（§2.6）・段階 A の検査認識の言及率の目安（'); Q(cut('A', '閾値は登録に無く、半分は起草者が率を見た後に置いた目安である', 'ある', cat='proc')); T('）。' + NL)
T('- (3) 見積りが外れた。段階 A の §0 は、見積りの既往について'); Q(cut('A', 'V′・門0 で概算が二度外れた（向きは逆）', '。', cat='proc')); T('と書く。' + NL)
T('- (4) 書いたが実物が伴わない型が繰り返された（4B の最初の登録の §0 の 5・段階 F の §0 の 1 の 6）。段階 F の §0 は'); Q(cut('F', '一巡目が見つけた「書いたが実物が伴わない」型', '型', cat='proc')); T('に、系統外の目が同型を足して見つけたと書く。' + NL)
T('- (5) 起草者の誤りの向きと見つかり方。追補 M の §0 は、コーディネータの既往について'); Q(cut('M', 'いずれも登録者の関心に有利な向き', 'き', cat='proc')); T('と書く。見つかり方は、検分の巡（4B の最初の登録の §0 の 5）と、器の自己検査（段階 A の §0 の 10）の両方がある。' + NL)
T('- (6) この総括の草案1 も、引用の選びで限る文を落とし、O と前置きの側と筋の通る物語の側に寄った（一巡目の採否の表の Y04・Y05・Y22）。B′ の S10 に反する並べ方（Y01）と、段階 B の札の数の誤り（Y02）もあった。' + NL + NL)

# ---------------- §5 ----------------
T('## 5. 言えないこと（柵）' + NL + NL)
X('- 本書と各段のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用しない（両方向不定）。' + NL)
T('- 機種の率と機種の差を、機種の安全さの比べとして読まない。二つの機種の行動の率を同じ表にも同じ文にも置かない（B′ の正本の S10: '); Q(cut('design/design-Bprime-FROZEN.md', '行動の率の二つの機種の値（同じ表にも同じ文にも置かない）〔S10〕', None, cat='fence')[:len('行動の率の二つの機種の値（同じ表にも同じ文にも置かない）〔S10〕')]); T('）。二つの機種の違いを、系譜・規模・トークナイザのどれか一つから来たものとして読まない（B′ の §0）。' + NL)
T('- 上昇を招く操作の再現手順を、本文・要約・表題に書かない（追補 M 以来の両用性の柵・本書は冷徹一行の逐語を置き換えた）。'); Q(cut('F', '要約・表題での強調の禁止は両向きに掛ける', '。', cat='fence')); T('下がる向きの結果も両用である（段階 F の §0 の 1 の 5 (b)）。'); Q(cut('F', '本段の柵は拡散を防げない。防げるのは増幅だけである。', None, cat='fence')[:len('本段の柵は拡散を防げない。防げるのは増幅だけである。')]); T('（段階 F）。本書は増幅の場になりうる。' + NL)
T('- 腕を効き目順に並べた表を作らない（追補 M・段階 F・段階 A）。'); Q(cut('A', 'O の床持続を価値語で書かない', '。', cat='fence')); T('（段階 A）。'); Q(cut('A', '防護側と誘発側を同じ柵の下で同時に公開する', '。', cat='fence')); T('（段階 A）。' + NL)
T('- 逸脱の下の札は、事前登録の確証と同じ身分を持たない（段階 B）。区別できなかったことを、同じ程度だったと読まない（層三）。測れなかったことを、効き目の不在と読まない（帰無の図も図）。' + NL)
T('- 段階 A の凍結の本文の柵: '); Q(cut('design/design-stageA-FROZEN.md', '4B を成功の予兆と読まない', 'ない', cat='fence')); T('・'); Q(cut('design/design-stageA-FROZEN.md', '規模の効果を訓練の効果から分離したと書かない', 'ない', cat='fence')); T('・'); Q(cut('design/design-stageA-FROZEN.md', '環境の効果を規模の効果から分離したと書かない', 'ない', cat='fence')); T('。' + NL)
T('- 禁止の語: 各段の正本（`design/contrasts-*.json`）の `print_strings` にある。本書の地の文は、B′ の正本の一覧の和に枠の例の語を足した一覧で器が走査した（検分票）。新しい計算の表に札を付けない。' + NL + NL)

# ---------------- §6 ----------------
T('## 6. 段階 C・D・E の枠に要るもの（総括から出る要件・推奨はしない・決めるのは登録者）' + NL + NL)
T('- **三つの段の定め**（起草者の言葉・登録者裁定 D287-g）: 段階 C は、同じ走り・同じ規模の中で、下向き（Onull→O）と上向き（Onull→Onull-Ncold）の効き目の大きさを比べる段（比べの尺度を Firth の対数オッズ比の絶対値とすることは、登録者が 2026-09-10 に決めている）。段階 D は、Qwen3 の外の系譜の公開の重みの機種とフロンティアの API の端点で、行動層を日本語と英語で測る段（候補に Gemma の機種が入っている・D257）。段階 E は、各段の結果を、帰無の結果も含めた一枚の図と英語の正本にまとめる段。' + NL)
T('- **段階 C**: (a) 余地の定義と閾値の感度を、値を見る前に決める（§3.3・感度で数えた余地の升の数は照らしの記録）。(b) 向きが想定と逆の升の扱いと、符号の決まり（§3.3 の向きの印）。(c) 共通の対照 Onull の扱いと n の割り振り（対照の揺れが下向きと上向きの両方に入る・揺れの目安は照らしの記録）。(d) refuse・様式・検査認識の門を掛けるか（§2.5 の様式門・段階 A の検査認識の言及率）。(e) 下見で場面を選ぶなら、選ぶ決まりを下見の前に凍結し、下見の升を確証に使わない。段階 A の凍結の本文の'); Q(cut('design/design-stageA-FROZEN.md', '機種ごとに場面を選び直さない', 'ない', cat='req')); T('との両立。(f) 錨の 4B-2507 では O の腕が段階 A と V′ の全升で床にあり（§3.2 の出力）、O を下向きの腕にすると下向きに余地が無い。下向きの腕に何を置くかと、O の著者が登録者であることの COI の記帳。(g) 下向きと上向きは種類の違う操作なので、対称と書ける範囲を先に決める。(h) 対称性の確証は同じ走りで登録する（段階 A と V′ を横断しない）。' + NL)
T('- **段階 D**: (a) 機種ごとの判定器の妥当性（B′ の §0 の見ていない場所）。(b) 標本化の設定（計画の値か、機種の既定か・B′ の §0）。(c) チャットの型と思考の欄の扱い（B′ の §0 の空の思考の欄）。(d) 提供の経路の同等性（段階 A の門0.5 の合格は等価の確立ではない・§2.5）。(e) 二つの機種の行動の率を同じ表に置くかの決まりを、結果の前に決める（S10・§5）。(f) 下見の n（升目ごとの試行 40 の区間は主閾値をまたぐ・照らしの記録）。(g) 機種ごとの端の位置を測る下見をどこに置くかと、場面を選び直さない決まりとの両立（§3.2）。(h) 正本の決まりと器の自己検査の対応表を、凍結の前に作る（§4 の (1)）。(i) 生成したトークン列の記帳（B′ の §0 の書き出しの根の件数は、トークンの並びと文字列で数が違った）。(j) 費用の実績を走りの前後で記録する（段階 A の §0 の見積りの既往・§4 の (3)）。(k) 検分者の作り手と調べる機種の作り手の重なりの開示（Gemini と Gemma・D257）。(l) B′ の正本の禁止の語の持ち越し。' + NL)
T('- **段階 E**: (a) 図の点を、測れた・測って区別できなかった・測って想定と逆・測れなかった（止めた下見を含む）に分ける（§3.1）。(b) 逸脱の下の札を、事前登録の確証と別の印にする（段階 B）。(c) B′ を止めた点として置く。(d) 錨を並びの線に載せない（段階 A の COI の印）。(e) 腕を効き目順に並べない・S10 を図にも掛ける。(f) 機構層の点は 4B-2507 の一点（段階 B と層三）で、B′ は読み取りの下見で止まった。段階 B の札の内訳は二つの出力で大きく違い、どちらか一方だけを引かない（§2.6）。' + NL + NL)

# ---------------- 付録 ----------------
T('## 付録 A 各段の最終版の置き場・SHA16・§0 の行の範囲（引用の選びを確かめるため）' + NL + NL + '| 段 | 最終版 | SHA16 | §0 の行 | §0 の写しの SHA16 |' + NL + '|---|---|---|---|---|' + NL)
for k in ORDER9:
    a_, b_, seg = sec0(k)
    T('| %s | `%s` | %s | %d〜%d | %s |' % (NAME[k], FIN[k], s16(P(*FIN[k].split('/'))), a_, b_, s16t(seg)) + NL)
T(NL + '## 付録 B 新しい計算の入力と器' + NL + NL)
T('- 器 `summary/calc_interim.py` v0.2（SHA16 %s）・出力 `summary/calc/calc-interim-v0.2.json`（SHA16 %s）と `.md`（SHA16 %s）。Firth の器 %s・閾値の出所 %s。' % (
    s16(os.path.join(HERE, 'calc_interim.py')), s16(CALC_J), s16(os.path.join(HERE, 'calc', 'calc-interim-v0.2.md')), CALC['firth_tool'], CALC['censor_from']) + NL)
T('- 前の版（記録として残す）: v0（器 `summary/prev/calc_interim-v0.py` SHA16 %s・json %s・md %s・B′ を含む・草案1 が使った）・v0.1（器 `summary/prev/calc_interim-v0.1.py` SHA16 %s・json %s・md %s・向きの印に零の幅が無かった）。' % (
    s16(os.path.join(HERE, 'prev', 'calc_interim-v0.py')), s16(os.path.join(HERE, 'calc', 'calc-interim.json')), s16(os.path.join(HERE, 'calc', 'calc-interim.md')),
    s16(os.path.join(HERE, 'prev', 'calc_interim-v0.1.py')), s16(os.path.join(HERE, 'calc', 'calc-interim-v0.1.json')), s16(os.path.join(HERE, 'calc', 'calc-interim-v0.1.md'))) + NL)
T('- 入力: 段階 A の %d の走り・V′ の %d の走り（置き場と SHA16 は計算の記録の `inputs`）。照らしの記録: `summary/summary-interim-draft2-checks.json`・一巡目の照らしの記録 `summary/reviews/round1/repro-round1.md`。' % (len(CALC['inputs']['A']), len(CALC['inputs']['Vprime'])) + NL + NL)

# ---------------- 照らし ----------------
own = ''.join(s_ for kind, s_ in segs if kind == 't')
hits = sorted({w for w in BANS if w and w in own})
for u in used:
    t_ = src(u['source'])
    assert u['quote'] in t_ or u['quote'] in t_.replace('**', ''), ('引用が元の記録に無い', u['source'], u['quote'][:40])
    if u['cat'] == 'ans':
        a_, b_, _ = sec0(u['stage'])
        assert a_ <= u['lines'][0] and u['lines'][1] <= b_, ('§0 の外の引用', u['stage'], u['lines'], (a_, b_), u['quote'][:30])
corpus = NL.join([src(FIN[k]) for k in ORDER9] + [open(CALC_J, encoding='utf-8').read(), open(os.path.join(HERE, 'calc', 'calc-interim-v0.2.md'), encoding='utf-8').read(),
                  open(FRAME, encoding='utf-8').read(), open(ADD1, encoding='utf-8').read(), open(D287, encoding='utf-8').read(), open(AT1, encoding='utf-8').read(),
                  src('design/design-stageA-FROZEN.md'), src('design/design-Bprime-FROZEN.md'), src('records/FREEZE-RECORD.md'), src('design/contrasts-A.json'),
                  open(os.path.join(HERE, 'reviews', 'round1', 'repro-round1.md'), encoding='utf-8').read()])
nums = sorted(set(re.findall(r'(?<![A-Za-z0-9_.\-])(\d+(?:[./]\d+)*)(?![A-Za-z0-9_])', own)))
num_miss = [n for n in nums if n not in corpus]
nonq = sorted(set(re.findall(r'「([^「」]+)」', own)))
if hits or num_miss:
    print('走査の当たり:', hits, '| 記録に無い数:', num_miss)
    raise SystemExit('照らしが通らない（書かない）')
n_ans = sum(1 for u in used if u['cat'] == 'ans')
n_bold = sum(1 for u in used if u['bold_stripped'])
n_rep = sum(1 for u in used if 'replaced' in u)

# ---------------- 検分票 ----------------
T('## 検分票' + NL + NL)
T('- 対象: 中間総括の草案2（登録の外の案内図と新しい計算・一巡目の採否と裁定 D287 の反映）。' + NL)
T('- 段階: 事後（全段の公開の後）。直しの決まり・計算の改め・引用の選びの決まり・二巡目の段取りと予想は、草案2 と計算の器の版上げの前に枠の追記一に書いて刻印した（SHA16 %s）。' % add16 + NL)
T('- 凍結物の同定: どの段の凍結物にも触れていない。' + NL)
T('- 盲検の状態: 該当しない。各段の値は公開済みで、起草者は公開の時に見ている（新しい計算の各升の率も同じ）。計算二の段ごとの数と印は、一巡目の検分で値を見た後に足した。' + NL)
T('- 敵対的検分: 引用 %d 本が元の記録に一字違わずあることを器が確かめた（§2 の答えの引用 %d 本は各段の §0 の行の範囲にあることも確かめた・太字の印を除いて照らしたもの %d 本・冷徹一行の逐語の置き換え %d 本）。地の文の数 %d 個が記録の集まりにあることを器が確かめた。地の文を禁止の語 %d 語で走査し、当たりは 0。' % (
    len(used), n_ans, n_bold, n_rep, len(nums), len(BANS)) + NL)
T('- 引用でない「」（地の文の中・器が並べた）: ' + ('・'.join('「%s」' % q for q in nonq) if nonq else 'なし') + '。' + NL)
T('- 枠の追記一からのずれ: §4 の出所に、各段の最終版の頭の逸脱の区画を足した（器の欠けの記録が §0 の外にあるため）。' + NL)
T('- 系統の内訳: 起草者（Claude 系）一人。一巡目は claude.ai の Claude 三名（一票）と Gemini 3.8 Flash 一名（gemini-2 は不具合で取りやめ・裁定 D287-e）。二巡目はこの後。' + NL)
T('- COI記録: 起草者は一巡目で重大五件を指摘された草案1 の書き手で、直しを応えたと見せる側に引かれる。逆に、各段の最終版の言い方より弱く書いて直しを大きく見せる側にも引かれる。' + NL)
T('- 判定: 検分の二巡目に出せる水準。' + NL)
T('- 本検分が確認していないこと: §3.1 の四つの欄の境の置き方（起草で決めた。段階 B の札に付く登録された向きと逆の文言を想定と逆の欄に置かなかったこと・門を測って区別できなかった欄に置いたことなど）。§4 と §6 の網羅。計算二の定義の妥当さ（定義は一巡目の後も変えていない）。' + NL + NL)
X('本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。' + NL)

text = ''.join(s_ for _, s_ in segs)
own2 = ''.join(s_ for kind, s_ in segs if kind == 't')
hits2 = sorted({w for w in BANS if w and w in own2})
assert not hits2, ('検分票に禁止の語', hits2)
DRY = '--dry' in sys.argv
if DRY:
    OUT = os.path.join(os.environ['OP4B_DRY_DIR'], 'draft2-dry.md')
    CHK = os.path.join(os.environ['OP4B_DRY_DIR'], 'draft2-dry-checks.json')
else:
    for p_ in (OUT, CHK):
        assert not os.path.exists(p_), '一度だけ: ' + p_
open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
json.dump({'kind': 'interim_summary_draft2_checks', 'tool': 'summary/build_summary_draft2.py v0', 'frame_sha16': frame16, 'addendum1_sha16': add16,
           'calc': {'tool_sha16': s16(os.path.join(HERE, 'calc_interim.py')), 'json_sha16': s16(CALC_J), 'md_sha16': s16(os.path.join(HERE, 'calc', 'calc-interim-v0.2.md'))},
           'sec0_ranges': {k: list(sec0(k)[:2]) for k in ORDER9}, 'quotes': used, 'n_quotes': len(used), 'n_answer_quotes_in_sec0': n_ans, 'n_bold_stripped': n_bold, 'n_replaced': n_rep,
           'numbers_in_own_text': nums, 'numbers_missing': num_miss, 'non_quote_brackets_in_own_text': nonq, 'ban_list_n': len(BANS), 'ban_hits_in_own_text': 0,
           'draft_sha16': s16(OUT), 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'},
          open(CHK, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('wrote', os.path.basename(OUT), s16(OUT), len(text), '字 | 引用', len(used), '（§0 の答え', n_ans, '・太字除き', n_bold, '・置き換え', n_rep, '）| 数', len(nums), '| 引用でない「」', len(nonq), '| 禁止の語', len(BANS), '当たり 0')
