# -*- coding: utf-8 -*-
"""build_summary_draft1.py v0（2026-10-02・中間総括の草案1 を組む・枠 `00-frame-interim-summary-2026-10-02.md` の構成と書き方の決まりのとおり・コーディネータ南無弥勒如来）。
- 引く文は、公開の置き場の最終版・凍結の本文・台帳から器で切り出して差し込む（開きの字と終わりの字で切る・手で打たない）。切り出した字が元の記録にあることを器が確かめる。
- 数は計算の記録（`calc/calc-interim.json`）と git のタグと台帳から器で差し込む。
- 起草者の地の文だけを、禁止の語の一覧（B′ の正本の `print_strings` の禁止の一覧の和・凍結した組み立ての器 `build_report_Bprime.bans_of` と同じ集め方）で走査する（引用は走査しない）。
- 書く物: `summary-interim-draft1-2026-10-02.md` と `summary-interim-draft1-checks.json`（一度だけ）。
用法: python build_summary_draft1.py（OP4B_HF_DIR と PYTHONPATH は B′ の器と同じに渡す）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, hashlib, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'summary-interim-draft1-2026-10-02.md')
CHK = os.path.join(HERE, 'summary-interim-draft1-checks.json')
NL = chr(10)
P = lambda *a: os.path.join(PUB, *a)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
sys.path.insert(0, P('tools'))
import build_report_Bprime as BR
CB = json.load(open(P('design', 'contrasts-Bprime.json'), encoding='utf-8'))
BANS = BR.bans_of(CB)
CALC = json.load(open(os.path.join(HERE, 'calc', 'calc-interim.json'), encoding='utf-8'))
FIN = {'4B': 'records/results/results-report-FINAL-2026-09-07.md', 'Vp': 'records/vprime/results-report-Vprime-FINAL-2026-09-09.md', 'M': 'records/M/results-report-M-FINAL-2026-09-11.md',
       'F': 'records/F/results-report-F-FINAL-2026-09-12.md', 'A': 'records/A/results-report-A-FINAL-2026-09-17.md', 'B': 'records/B/results-B-FINAL-2026-09-23.md',
       'BL': 'records/Blens/results-Blens-FINAL-2026-09-24.md', 'L3': 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', 'BP': 'records/Bprime/results-Bprime-FINAL-2026-10-01.md'}
TAG = {'4B': 'release-2026-09-07', 'Vp': 'release-Vprime-2026-09-09', 'M': 'release-M-2026-09-11', 'F': 'release-F-2026-09-12', 'A': 'release-A-2026-09-17', 'B': 'release-B-2026-09-23',
       'BL': 'release-Blens-2026-09-24', 'L3': 'release-Bl3-2026-09-27', 'BP': 'release-Bprime-2026-10-01'}
NAME = {'4B': '4B の最初の登録', 'Vp': '追補 V′', 'M': '追補 M', 'F': '段階 F', 'A': '段階 A', 'B': '段階 B', 'BL': 'B-lens', 'L3': '層三（B-lens 層三）', 'BP': 'B′'}
FREEZE_ROW = {'Vp': '**追補 V′ 凍結**', 'M': '**追補 M 凍結**', 'F': '**段階 F 凍結**', 'A': '**段階 A 凍結**', 'B': '**段階 B 凍結**', 'BL': '**B-lens 凍結**',
              'L3': '**B-lens 層三 下見の前の凍結**', 'BP': '**B′ 下見の前の凍結**'}
TXT = {}
used = []          # (key, quote, source)


def src(path):
    if path not in TXT:
        TXT[path] = open(P(*path.split('/')), encoding='utf-8').read()
    return TXT[path]


def cut(path, start, end=None, keep_end=True):
    """元の記録から、開きの字 start の一か所から、終わりの字 end の最初の一つまで（end が無ければ行の終わりまで）を切り出す。"""
    t = src(path)
    assert t.count(start) >= 1, ('開きの字が無い', path, start[:30])
    i = t.index(start)
    if end is None:
        j = t.index(NL, i) if NL in t[i:] else len(t)
        q = t[i:j]
    else:
        j = t.index(end, i + len(start) - (len(end) if start.endswith(end) else 0))
        q = t[i:j + (len(end) if keep_end else 0)]
    q = q.replace('**', '')
    used.append((start[:20], q, path))
    return q


def after(path, head, end=None):
    """行の頭の字 head の後ろから、行の終わり（か end）までを切り出す。"""
    t = src(path)
    assert t.count(head) == 1, ('頭の字が一つでない', path, head[:30], t.count(head))
    i = t.index(head) + len(head)
    j = t.index(NL, i) if end is None else t.index(end, i) + len(end)
    q = t[i:j].replace('**', '')
    used.append((head[:20], q, path))
    return q


def title_q(k):
    line = src(FIN[k]).split(NL)[0]
    assert '——' in line, k
    q = line.split('——', 1)[1].strip()
    used.append(('題', q, FIN[k]))
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


segs = []          # ('t', 地の文) か ('q', 引用)
T = lambda s: segs.append(('t', s))
Q = lambda q: segs.append(('q', '「' + q + '」'))
X = lambda s: segs.append(('x', s))          # 走査の外（柵の文）

# ---------------- 頭 ----------------
frame16 = s16(os.path.join(HERE, '00-frame-interim-summary-2026-10-02.md'))
T('# 中間総括（草案1）——Qwen3-4B-Instruct を発端とした検証の案内図（4B の最初の登録から B′ まで・登録の外・内部・非公開）' + NL + NL)
T('- 起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／登録者: 楠見優太／2026-10-02。枠 `summary/00-frame-interim-summary-2026-10-02.md`（SHA16 %s・起草と計算と検分の前に書いた）のとおりに組んだ（器 `summary/build_summary_draft1.py`）。' % frame16 + NL)
T('- 状態: 草案1（検分の一巡目の前）。内部で作り、完成したら公開する（登録者の決め・2026-10-02）。' + NL + NL)

# ---------------- §0 ----------------
T('## 0. この文書は何で、何でないか' + NL + NL)
T('- **登録の外の案内図**: 2026-09-05 から 2026-10-01 までに凍結・公開した九つの段（4B の最初の登録・追補 V′・追補 M・段階 F・段階 A・段階 B・B-lens・層三・B′）を、一か所に並べる。新しい証拠を足さない。凍結した結果を読み直さず、札・門・決定を変えない。' + NL)
T('- **答えは各段の最終版の §0 の文の範囲**: 段ごとの答えは、その段の最終版の §0 から器で切り出して引く（引用の選びの偏りは、検分の束に §0 の全文を入れて見てもらう）。段をまたぐ言い方は、段ごとの引用を並べた後に、引用の範囲で言えることだけを書く。' + NL)
T('- **新しい計算（§3）は登録の外の記述**: 既に公開した記録だけから計算し、札を付けず、検定もしない。計算の定義は値を計算する前に枠に書いた。' + NL)
T('- **前身**: 4B の最初の登録の前に、別の置き場の追補E（Qwen3-30B-A3B）がある。本書は発端としてだけ触れ、その数を引かない。' + NL)
X('- **柵**: 本書のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'); T('機種の率を、機種の安全さの比べとして読まない。' + NL + NL)

# ---------------- §1 ----------------
T('## 1. 問いの系譜と時系列' + NL + NL)
T('| 段 | 問い（最終版の題か凍結の本文から引く） | 凍結 | 公開（タグの日付） | タグ | 最終版 |' + NL + '|---|---|---|---|---|---|' + NL)
QQ = {}
for k in ('4B', 'Vp', 'M', 'F', 'A', 'B'):
    QQ[k] = title_q(k)
QQ['BL'] = after('design/design-Blens-FROZEN.md', '  - **問一（答えの文字）**: ')
QQ['L3'] = after('design/design-Bl3-FROZEN.md', '**問い**（一つ・裁定 D203）: ')
QQ['BP'] = after('design/design-Bprime-FROZEN.md', '**問い**（一つの問いを二つの部分に分けた）〔R01〕: ')
for k in ('4B', 'Vp', 'M', 'F', 'A', 'B', 'BL', 'L3', 'BP'):
    T('| %s | ' % NAME[k]); Q(QQ[k].replace('|', '｜')); T(' | %s | %s | `%s` | `%s` |' % (freeze_date(k), tag_date(k), TAG[k], FIN[k]) + NL)
T(NL + '- B-lens の問いは六つあり（すべて記述）、表には一つ目だけを引いた（凍結の本文 `design/design-Blens-FROZEN.md` の「問い」）。B′ の問いは、計画の当初の B′（Llama-3.1-8B・日英）から、裁定 D255〜D258 で機種と問いを改めたもの。' + NL + NL)

# ---------------- §2 ----------------
T('## 2. 各段の答え（できないことから・最終版の §0 から引く）' + NL + NL)
T('### 2.1 4B の最初の登録（Qwen3-4B-Instruct-2507・段 0〜VI）' + NL + NL + '- ')
Q(cut(FIN['4B'], '段V（逆用・上向き）は測れなかった', '。'))
T(NL + '- '); Q(cut(FIN['4B'], 'O（存在論的前置き）対 Onull（中立前置き）は 10 本すべて有意・想定方向', '。'))
T(NL + '- '); Q(cut(FIN['4B'], '否定の前置き（Lneg）対 Onull（上向き想定）は 3 本が確証・2 本が有意で逆方向', '。'))
T(NL + '- '); Q(cut(FIN['4B'], '段III で O の転向は圧力 0/223・中立 9/218（有意・想定と逆）', '。'))
T(NL + '- 手続きの側では、最終版の §0 が、草案ごとの誤り（数値の混入・存在しない引用・別の走行の値）を先に書いている（§0 の 5）。' + NL + NL)
T('### 2.2 追補 V′（悪意の枠付けの加算・4B-2507・n=400）' + NL + NL + '- ')
Q(cut(FIN['Vp'], 'この文形・この語・この 4B 構成で、冷徹一行', '上げた'))
T(NL + '- '); Q(cut(FIN['Vp'], '冷徹の付加で O の破局率は絶対値として', '無力化はできていない'))
T(NL + '- '); Q(cut(FIN['Vp'], 'これは「悪意の枠は危険にする」を新発見として書くものではない', '。'))
T(NL + NL + '### 2.3 追補 M（仏名・末尾文字列・呼び出しの形式・置き場・4B-2507）' + NL + NL + '- 一斉保留の断面の第一の所見: ')
Q(cut(FIN['M'], '破局率の差は応答様式の転換と分離できなかった', 'た'))
T(NL + '- '); Q(cut(FIN['M'], '上向きの一般化は構造的に書けず', '。'))
T(NL + '- 上向きの札のうち対照の腕が床にある対比について、最終版は'); Q(cut(FIN['M'], 'これらの差は A 腕の上昇ではなく対照の床が作る', '作る')); T('と書く（§0 の 4・統制腕の非中立）。' + NL + NL)
T('### 2.4 段階 F（場面冒頭の検査認識の付記・4B-2507）' + NL + NL + '- ')
Q(cut(FIN['F'], '上向きの確証 3 本', '本'))
T('・'); Q(cut(FIN['F'], '下向きの確証 4 本', '本'))
T('（最終版 §0 の 4）。S1・S4・SK の場面の第一の所見は、追補 M と同じく'); Q(cut(FIN['F'], '破局率の差は応答様式の転換と分離できなかった', 'た')); T('（§0 の 5）。' + NL + NL)
T('### 2.5 段階 A（規模軸・Qwen3 の稠密系列 0.6B〜32B と錨 4B-2507）' + NL + NL + '- ')
Q(cut(FIN['A'], '上向きの確証はなかった。', None))
T(NL + '- '); Q(cut(FIN['A'], '傾きの族 35 対比のうち、確証 1', '。'))
T(NL + '- '); Q(cut(FIN['A'], '記述（解釈条項）に回った対比の多さは効果の不在を意味しない。', None))
T(NL + NL + '### 2.6 段階 B（機構層・4B-2507・方向の加減と破局率）' + NL + NL + '- ')
Q(cut(FIN['B'], '凍結した集計器の出力と、逸脱の下の出力は、札の内訳が大きく違う。', None))
T(NL + '- '); Q(cut(FIN['B'], '区別できた相手は「引いた三本のランダム方向を合わせた腕」であり、「ランダム方向一般」ではない。', 'ではない。'))
T(NL + '- '); Q(cut(FIN['B'], '区別できた場面はすべて survival の場面で', '区別できなかった。'))
T(NL + '- '); Q(cut(FIN['B'], 'B が答えるのは「この抽出の方向（位置・層・係数）の加減が、ランダム方向と区別できる動きを作ったか」までである', '。'))
T(NL + NL + '### 2.7 B-lens（v̂ の直接の経路の押し・層の割合 0.5）' + NL + NL + '- 〈区別できない〉（主の六つ）: ')
Q(cut(FIN['BL'], '直接の経路では、等方の帰無と区別できる押しは無かった。後の層の経路は見ていない', None))
T(NL + '- 〈門を通らない〉: '); Q(cut(FIN['BL'], '直接の経路の物差しは、B の方向ごとの行動の変化と、方向の単位でそろわなかった。上の型の記述は行動に結びつけない', None))
T(NL + NL + '### 2.8 層三（全経路の効き目・直答の型の読み取りの位置）' + NL + NL + '- 〈両方の外〉の一行（`sub:N1:O-Ncold-v~O-Ncold-vrand`）: ')
Q(cut(FIN['L3'], 'その行の効き目は、等方のランダム方向と区別でき、実在の差の方向（兄弟を除く・両方の向き）の中で、中心からの動きが最上位だった', '）'))
T(NL + '- ほかの主の行は〈外でない行〉で、最終版は各行を'); Q(cut(FIN['L3'], 'その行の効き目は、等方のランダム方向と区別できなかった（この読み取りの位置での記述）', None)); T('と書く。' + NL)
T('- 〈門を通らない〉: '); Q(cut(FIN['L3'], '直答の型の読み取りの全経路の効き目は、段階 B の方向ごとの行動の変化と、方向の単位でそろうことは示せなかった。', None))
T(NL + '- 唯一の行の事情（床の近さ・下見の揺れ）について、最終版の注は'); Q(cut(FIN['L3'], 'これらは札と型を変えない。どちらの向きにも読まない（区別できたことを強める側にも、弱める側にも）。', None)); T('と書く。' + NL + NL)
T('### 2.9 B′（Gemma-4-31B-it・日本語・層三の型の読み取りの追試）' + NL + NL + '- ')
Q(cut(FIN['BP'], 'この読み取りでは測れなかった（閾値は層三の登録の値を写したもので、Gemma で較正していない）。B′ の問いには答えていない', None))
T(NL + '- 行動の下見（記述）について、最終版は'); Q(cut(FIN['BP'], '二つの機種の安全さを比べる読みにしない', None)); T('と書く。' + NL + NL)

# ---------------- §3 ----------------
r1, pm, r2 = CALC['calc1_rows'], CALC['calc1_per_model'], CALC['calc2_rows']
room = [x for x in r2 if not x['no_room']]
n_O_floor_2507 = sum(1 for x in r1 if x['size'] == '4B-2507' and x['arm'] == 'O' and x['mark_main'] == '床')
n_O_2507 = sum(1 for x in r1 if x['size'] == '4B-2507' and x['arm'] == 'O')
end_O = sum(1 for x in r2 if 'O' in x['end_arms'])
end_U = sum(1 for x in r2 if 'Onull-Ncold' in x['end_arms'])
end_N = sum(1 for x in r2 if 'Onull' in x['end_arms'])
T('## 3. 測れた所と測れなかった所（横断の地図）' + NL + NL)
T('### 3.1 各段の最終版が書いた「測れた所」と「測れなかった所」' + NL + NL)
T('- 測れた所（§2 の引用のとおり）: 4B の最初の登録の O 対 Onull と Lneg の確証・V′ の上向きの確証・追補 M と段階 F の確証（様式門で保留された断面を除く）・段階 A の確証・段階 B の事前登録の確証（交差族）・層三の一行。どれも、その段の最終版が書いた範囲（場面・土台・読み取りの位置・機種）の上での記述である。' + NL)
T('- 測れなかった所: 天井で測れなかった上向き（4B の最初の登録の段V）・応答様式の転換と分離できなかった断面（追補 M・段階 F・段階 A の様式門）・解釈条項に回った対比と測れなかった効果種（段階 A）・凍結した二つの器の食い違いと三本のランダム方向（段階 B）・門の不成立（B-lens・層三）・読み取りの下見の停止（B′）。どれも、効き目が無かったことを示したのではなく、測る位置や器や設計の側で測れなかった（各段の最終版の §0 の言い方のとおり）。' + NL + NL)
T('### 3.2 新しい計算一 動く幅の地図（登録の外の記述・`summary/calc/calc-interim.md`）' + NL + NL)
T('- 定義（枠 §3）: 腕ごとの全分母破局率（分子＝破局・分母＝n_ok）に、段階 A の正本 `censor` の主閾値（%s 未満＝床・%s 超＝天井）で印を付けた。感度閾値は表の右の二列。検定はしない。' % tuple(CALC['thresholds']['main']) + NL + NL)
T('| 段・機種 | 升 | 床 | 天井 | 中 | 端（感度・狭い）| 端（感度・広い）|' + NL + '|---|---|---|---|---|---|---|' + NL)
LAB = {'A': '段階 A', 'Vprime': 'V′', 'Bprime': 'B′'}
for k_, d in pm.items():
    T('| %s | %d | %d | %d | %d | %d | %d |' % ('%s・%s' % (LAB[k_.split('|')[0]], k_.split('|')[1].replace('Gemma-31B', 'Gemma-4-31B-it')), d['cells'], d['floor'], d['ceiling'], d['middle'], d['ends_strict'], d['ends_loose']) + NL)
T(NL + '- 段階 A と V′ の 4B-2507 では、O の腕は %d 升のうち %d 升が床だった（4B の最初の登録の §0 の O の床と同じ側）。B′ の Gemma-4-31B-it は、測った %d 升がすべて端だった（行動の下見・各升目 40・段階 B の標本化）。' % (
    n_O_2507, n_O_floor_2507, pm['Bprime|Gemma-31B']['cells']) + NL)
T('- 読み: 機種ごとに、凍結した場面と素材で端に寄る升が多いものと少ないものがある。どの機種でも、端の升では腕の差が読めない（段階 A の検閲と解釈条項の決まりのとおり）。機種の安全さの比べとしては読まない。' + NL + NL)
T('### 3.3 新しい計算二 段階 C の対称性の記述（同じ走り・同じ規模の中・札なし）' + NL + NL)
T('- 定義（枠 §3）: 下向き＝Onull→O、上向き＝Onull→Onull-Ncold の Firth の対数オッズ比（段階 A の凍結の器 `tools/firth.py`）。三つの腕のどれかが主閾値の端なら「余地なし」。' + NL)
T('- 段階 A の 35 升と V′ の 4 升、計 %d 升のうち、三つの腕がそろって端から離れていた升は %d（%s）。端に当たった腕は、O が %d 升・Onull-Ncold が %d 升・Onull が %d 升（重なりあり）。' % (
    len(r2), len(room), '・'.join('%s の %s の %s' % ({'A': '段階 A', 'Vprime': 'V′'}[x['stage']], x['size'], x['scenario']) for x in room), end_O, end_U, end_N) + NL)
T('- 余地のあった升の絶対値の差（上向き − 下向き）は ' + '・'.join('%.3f' % x['abs_diff_up_minus_down'] for x in room) + '（升の順は上と同じ）。符号はそろっていない。対称だった・対称でなかったとは読まない。' + NL)
T('- 段階 C の設計への材料（推奨ではない）: 今の場面と素材と機種では、同じ走り・同じ規模の中で両方の向きに余地のある升が少ない。段階 C を「A の第二期」として登録するなら、両方の向きに余地のある機種・場面・土台を先に下見で探す手順が要る。段階 A と V′ を横断して並べて対称性を書かない。' + NL + NL)

# ---------------- §4 ----------------
T('## 4. 手続きの資産と教訓（段をまたいで束ねる・新しい教訓は作らない）' + NL + NL)
T('**働いた型**: 事前登録と予想の封印（コーディネータが先・登録者が後）・凍結と記録先行の公開・率盲検の整合検査・機械の区画（数は器が書く）・凍結の後の逸脱の台帳・逸脱の下の器（凍結した器の出力をバイトのまま作り直して照らし、印を付けた区画だけを足す）・止める道（B′ の下見の決定木から公開まで）・公開の前の鍵の確かめ・系統外の目による検分（票の総括は裁定にせず、所見ごとに再現して採否を決める）。' + NL + NL)
T('**繰り返した誤り**（各段の最終版の §0・COI の節・逸脱の台帳にある）: (1) 凍結した器の欠けが、結果を見た後に見つかった（段階 B・B-lens・層三・B′）。(2) 応答様式の転換が破局率の差と分離できなかった（追補 M・段階 F・段階 A）。(3) 起草者の草案の誤り（数の混入・存在しない引用・言い方の向き・約束した注の抜け）が、検分の巡で捕まった。' + NL + NL)

# ---------------- §5 ----------------
T('## 5. 言えないこと（柵）' + NL + NL)
X('- 本書と各段のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用しない（両方向不定）。' + NL)
T('- 機種の率と機種の差を、機種の安全さの比べとして読まない。上昇を招く操作の再現手順を、本文・要約・表題に書かない（追補 M 以来の両用性の柵）。' + NL)
T('- 「測れなかった」を、効き目の不在の意味に読まない（帰無の図も図である）。新しい計算の表に札を付けない。' + NL + NL)

# ---------------- §6 ----------------
T('## 6. 段階 C・D・E の枠に要るもの（総括から出る要件・推奨はしない・決めるのは登録者）' + NL + NL)
T('- **段階 C**: 「A の第二期」の定義（両方の向きに余地のある機種・場面・土台を先に下見で探す・§3.3）。対称性の確証は同じ走りで登録する。' + NL)
T('- **段階 D**: 機種ごとの動く幅を測る下見の置き場所（§3.2）・場面を機種ごとに選び直さない決まりとの両立・正本の決まりと器の自己検査の対応表を凍結の前に作ること（§4 の (1)）・系統外の目を二系統にするか・言語軸（英語）の要件（実トークン列の記帳）・費用の実績を走りの前後で記録すること。' + NL)
T('- **段階 E**: 図の点の多くが端（検閲・解釈条項）にあることを前提にした図の作り（帰無の図も図）・機構層の点は 4B の一点で、凍結の出力の札は零本であること（段階 B の §0）。' + NL + NL)

# ---------------- 付録 ----------------
T('## 付録 A 各段の最終版の置き場と SHA16' + NL + NL + '| 段 | 最終版 | SHA16 |' + NL + '|---|---|---|' + NL)
for k in ('4B', 'Vp', 'M', 'F', 'A', 'B', 'BL', 'L3', 'BP'):
    T('| %s | `%s` | %s |' % (NAME[k], FIN[k], s16(P(*FIN[k].split('/')))) + NL)
T(NL + '## 付録 B 新しい計算の入力と器' + NL + NL + '- 器 `summary/calc_interim.py` v0・出力 `summary/calc/calc-interim.json` と `.md`（全升の率と印・計算二の全升）。Firth の器 %s・閾値の出所 %s。' % (CALC['firth_tool'], CALC['censor_from']) + NL)
T('- 入力: 段階 A の %d の走り・V′ の %d の走り・B′ の閉じた記録（置き場と SHA16 は計算の記録の `inputs`）。' % (len(CALC['inputs']['A']), len(CALC['inputs']['Vprime'])) + NL + NL)
T('## 検分票' + NL + NL)
T('- 対象: 中間総括の草案1（登録の外の案内図と新しい計算）。' + NL)
T('- 段階: 事後（全段の公開の後）。構成・書き方の決まり・計算の定義・検分の段取り・予想は、起草と計算と検分の前に枠に書いた（SHA16 %s）。' % frame16 + NL)
T('- 凍結物の同定: どの段の凍結物にも触れていない。' + NL)
T('- 盲検の状態: 該当しない（各段の値は公開済み）。' + NL)
T('- 敵対的検分: 引いた文が元の記録に一字違わずあることを器が確かめた（確かめの記録）。地の文を禁止の語で走査した。新しい計算に札を付けず、対称性を読まなかった。' + NL)
T('- 系統の内訳: 起草者（Claude 系）一人。検分の一巡目はこの後（claude.ai の Claude 三名・Gemini 3.8 Flash 二名）。' + NL)
T('- COI記録: 起草者はほとんどの段の器と報告を書いた当人で、段をまたいで筋の通った物語にまとめる側に引かれる。逆に、測れなかった所を増やして小さく見せる側にも引かれる。' + NL)
T('- 判定: 検分の一巡目に出せる水準。' + NL)
T('- 本検分が確認していないこと: 引用の選びの偏り（検分の束に §0 の全文を入れて見てもらう）。§4 の束ね方の網羅。新しい計算の定義の妥当さ（枠のとおりに組んだが、定義そのものは検分を経ていない）。' + NL + NL)
X('本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。' + NL)

# ---------------- 走査と書き出し ----------------
hits = []
for kind, s_ in segs:
    if kind != 't':
        continue
    for w in BANS:
        if w and w in s_:
            hits.append({'ban': w, 'text': s_[:60]})
for k_, q, p_ in used:
    assert q in src(p_) or q.replace('**', '') in src(p_).replace('**', ''), ('引用が元の記録に無い', p_, q[:40])
text = ''.join(s_ for _, s_ in segs)
if hits:
    print('走査の当たり:', json.dumps(hits, ensure_ascii=False)[:800])
    raise SystemExit('地の文に禁止の語（止める）')
for p_ in (OUT, CHK):
    assert not os.path.exists(p_), '一度だけ: ' + p_
open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
json.dump({'kind': 'interim_summary_draft1_checks', 'tool': 'summary/build_summary_draft1.py v0', 'frame_sha16': frame16, 'calc_sha16': s16(os.path.join(HERE, 'calc', 'calc-interim.json')),
           'quotes': [{'key': k_, 'source': p_, 'quote': q} for k_, q, p_ in used], 'n_quotes': len(used), 'ban_list_n': len(BANS), 'ban_hits_in_own_text': 0,
           'draft_sha16': s16(OUT), 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'},
          open(CHK, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print('wrote', os.path.basename(OUT), s16(OUT), len(text), '字 | 引用', len(used), '| 地の文の走査の当たり 0')
