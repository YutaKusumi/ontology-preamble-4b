# -*- coding: utf-8 -*-
"""B-lens の報告の最終版の器の検査（起草者の最終の見直しの A・枠 `frame-final-read-Blens.md` の M1〜M8・2026-09-24・コーディネータ）。
最終版の数は組み立ての器を通さずに、層一・層二・事後の計算の記録と、最終版の中の別の所から読み直して突き合わせる。既にある出力には書かない。
用法: python records/reviews/Blens/results-final/final-read/check_final_Blens.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, math, hashlib, statistics, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import build_report_Blens as BR                                         # 凍結した組み立ての器（走査の関数だけを使う）
NL = chr(10)
P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda r: hashlib.sha256(open(P(r), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FINAL = 'records/Blens/results-Blens-FINAL-2026-09-24.md'
OUT_MD, OUT_JS = os.path.join(HERE, 'check-final-Blens.md'), os.path.join(HERE, 'check-final-Blens.json')
if len(sys.argv) == 3:                                  # 器の試し: 別の報告（草案の二つ目）に当て、一時の置き場に書く（本番は引数なし）
    FINAL, OUT_MD, OUT_JS = sys.argv[1], os.path.join(sys.argv[2], 'check-test.md'), os.path.join(sys.argv[2], 'check-test.json')
assert not os.path.exists(OUT_MD) and not os.path.exists(OUT_JS), '既にある'
T = open(P(FINAL), encoding='utf-8').read().replace('\r\n', NL)
LN = T.split(NL)
L = json.load(open(P('results/Blens/lens-Blens.json'), encoding='utf-8'))
C = json.load(open(P('results/Blens/calib-Blens.json'), encoding='utf-8'))
PH = json.load(open(P('results/Blens/posthoc-Blens.json'), encoding='utf-8'))
FR = json.load(open(P('records/Blens/FREEZE-RECORD-Blens.json'), encoding='utf-8'))
TL = json.load(open(P('design/contrasts-Blens.json'), encoding='utf-8'))
g4 = lambda x: '%.4g' % x
res = collections.OrderedDict()
MB, ME = '<!-- 機械:始 -->', '<!-- 機械:終 -->'
inblk, tagged = [False] * len(LN), [False] * len(LN)
st = None
for i, l in enumerate(LN):
    if l == MB:
        st = i
    elif l == ME and st is not None:
        blk = LN[st + 1:i]
        for k in range(st, i + 1):
            inblk[k] = True
            tagged[k] = any('【逸脱 D-BL' in x for x in blk)
        st = None
sec_of = []
cur = 'head'
for l in LN:
    m = re.match(r'## (\d+)\.', l)
    if m:
        cur = '§' + m.group(1)
    elif l.startswith('## 検分票'):
        cur = '検分票'
    sec_of.append(cur)
where = lambda i: '%d 行目（%s・%s）' % (i + 1, sec_of[i], '足した区画' if tagged[i] else ('凍結の区画' if inblk[i] else '区画の外'))

# ---- M1: SHA16
LABEL = {'封印の記録': 'records/Blens/sealing-record-Blens.json', '層一の記録': 'results/Blens/lens-Blens.json', '層二の記録': 'results/Blens/calib-Blens.json',
         '凍結の本文': 'design/design-Blens-FROZEN.md', '正本': 'design/contrasts-Blens.json'}
m1, seen = [], set()
for i, l in enumerate(LN):
    for m in re.finditer(r'`([^`]+)`(?:（SHA16 |・SHA16 | SHA16 | )([0-9A-F]{16})', l):
        m1.append((i, m.group(1), m.group(2), s16(m.group(1)) if os.path.exists(P(m.group(1))) else None))
        seen.add((i, m.group(2)))
    for lab, path in LABEL.items():
        for m in re.finditer(re.escape(lab) + r' SHA16 ([0-9A-F]{16})', l):
            if (i, m.group(1)) not in seen:
                m1.append((i, path, m.group(1), s16(path)))
                seen.add((i, m.group(1)))
    for m in re.finditer(r'(?<![0-9A-Za-z])([0-9A-F]{16})(?![0-9A-Za-z])', l):
        if (i, m.group(1)) not in seen:
            m1.append((i, None, m.group(1), None))
res['M1'] = [{'line': i + 1, 'path': p, 'printed': h, 'now': n, 'ok': (n == h) if p else None} for i, p, h, n in m1]

# ---- M2: パス
m2 = []
for i, l in enumerate(LN):
    for m in re.finditer(r'`([^`\s]+)`', l):
        s = m.group(1)
        if '/' in s or re.search(r'\.(py|md|json|npz)$', s):
            m2.append({'line': i + 1, 'path': s, 'exists': os.path.exists(P(s.rstrip('/')))})
res['M2'] = m2

# ---- M3: 裁定・逸脱・採否の番号
defined = set()
for fn in os.listdir(P('records/Blens')):
    if fn.startswith('rulings-') and fn.endswith('.md'):
        tx = open(P('records/Blens/' + fn), encoding='utf-8').read()
        defined |= set(re.findall(r'^\| (D\d+) \|', tx, re.M)) | set(re.findall(r'\*\*(D\d+)\*\*', tx))
devs = {d['no'] for d in FR['deviations']}
padopt = set()
for rel in ('records/reviews/Blens/results-round1/adoption-table-Blens-results-r1.md', 'records/reviews/Blens/results-final/adoption-table-Blens-results-final.md'):
    padopt |= set(re.findall(r'^\| (P\d+) \|', open(P(rel), encoding='utf-8').read(), re.M))
m3 = []
for i, l in enumerate(LN):
    for m in re.finditer(r'(?<![0-9A-Fa-f-])(D\d{3})(?![0-9A-Fa-f])', l):
        m3.append({'line': i + 1, 'id': m.group(1), 'defined': m.group(1) in defined})
    for m in re.finditer(r'D-BL\d', l):
        m3.append({'line': i + 1, 'id': m.group(0), 'defined': m.group(0) in devs})
    for m in re.finditer(r'(?<![0-9A-Za-z])(P\d{3})(?![0-9])', l):
        m3.append({'line': i + 1, 'id': m.group(1), 'defined': m.group(1) in padopt})
res['M3'] = m3
res['M3_devs_not_named'] = sorted(devs - {x['id'] for x in m3})

# ---- M4: 節の参照
secs = {sec_of[i] for i in range(len(LN))}
m4 = []
for i, l in enumerate(LN):
    for m in re.finditer(r'§(\d+)(?: の([^・。（）、]{1,12}))?', l):
        tgt = '§' + m.group(1)
        idx = [k for k in range(len(LN)) if sec_of[k] == tgt]
        m4.append({'line': i + 1, 'ref': m.group(0), 'exists': tgt in secs, 'target_has_added_block': any(tagged[k] for k in idx)})
res['M4'] = m4

# ---- M5: 表の列の数
m5, i = [], 0
while i < len(LN):
    if LN[i].startswith('|'):
        j = i
        while j < len(LN) and LN[j].startswith('|'):
            j += 1
        cnt = [LN[k].replace('\\|', '').count('|') for k in range(i, j)]
        bad = [k + 1 for k in range(i, j) if LN[k].replace('\\|', '').count('|') != cnt[0]]
        m5.append({'first_line': i + 1, 'rows': j - i, 'cols_head': cnt[0] - 1, 'misaligned_lines': bad})
        i = j
    else:
        i += 1
res['M5'] = m5

# ---- M6: 区画の印と走査
res['M6'] = {'begin': T.count(MB), 'end': T.count(ME), 'balanced': T.count(MB) == T.count(ME) and st is None, 'lint_violations': len(BR.lint_report(T, TL)[0]), 'lines': len(LN) - (1 if T.endswith(NL) else 0), 'sha16': s16(FINAL)}

# ---- M7: 数の突き合わせ（器を通さずに読み直す）
m7 = []
def chk(name, want, where_line):
    ok = [k for k, l in enumerate(LN) if where_line(l)]
    hit = [k for k in ok if want in LN[k]]
    m7.append({'item': name, 'want': want, 'lines': [k + 1 for k in hit], 'ok': bool(hit)})
g = C['gates']
gl = lambda l: '【逸脱 D-BL3】門の数' in l
for k_, v in (('本の門 M_L 順位相関', g4(g['full']['M_L']['rho'])), ('本の門 M_L 割合', g4(g['full']['M_L']['p'])), ('本の門 M_X 割合', g4(g['full']['M_X']['p'])),
              ('v̂ を抜いた門 M_L 割合', g4(g['without_vhat']['M_L']['p'])), ('v̂ を抜いた門 M_X 割合', g4(g['without_vhat']['M_X']['p'])),
              ('v̂ と (6b) を抜いた門 M_L', g4(g['without_vhat_loaded']['M_L']['p'])), ('v̂ と (6b) を抜いた門 M_X', g4(g['without_vhat_loaded']['M_X']['p']))):
    chk('§0 ' + k_, v, gl)
PM = L['primary']['metrics']
for m, x in PM.items():
    d = x['second_detail']
    chk('§0 順位 ' + m, ('%s 語の側の帰無の割合 %s' % (m, g4(d['word_side_p']))) if 'word_side_p' in d else ('%s %d／%d' % (m, d['rank'], d['of'])), lambda l: '実在の差の中の順位（M_E は' in l)
lay = L['layers'][L['primary']['ratio']]
SW = {'O~Osec', 'O~Osec-Ncold', 'Osec~O-Ncold', 'O-Ncold~Osec-Ncold'}
comp = sorted(abs(v['M_L_nuclear']) for p, v in lay['real'].items() if p not in SW)
chk('§1 比べる相手の数', '比べる相手 %d 組' % len(comp), lambda l: True)
chk('§1 中央値', '中央値 %s' % g4(statistics.median(comp)), lambda l: '比べる相手' in l)
chk('§1 最大', g4(comp[-1]), lambda l: '比べる相手' in l)
chk('§1 等方の標準偏差（抽選）', '抽選 %s' % g4(lay['iso_sd']['M_L_nuclear']['sampled']), lambda l: '等方の標準偏差' in l)
chk('§1 等方の標準偏差（解析）', '解析 %s' % g4(lay['iso_sd']['M_L_nuclear']['analytic']), lambda l: '等方の標準偏差' in l)
for p, v in lay['siblings']['static'].items():
    chk('§1 兄弟 ' + p, '%s %s' % (p, g4(v['M_L_nuclear'])), lambda l: '兄弟の三対（比べる相手から除いた対・正本' in l)
pc = C['magnitude']['colab_check']['calibration']['S4|Osec-Ncold|json']['main']
tail = sum(math.comb(pc['n'], i) * pc['p_T'] ** i * (1 - pc['p_T']) ** (pc['n'] - i) for i in range(pc['k'], pc['n'] + 1))
chk('§3 較正の裾の割合', g4(tail), lambda l: '較正の検査の位置' in l)
chk('§3 較正の z', 'z %.2f' % ((pc['k'] - pc['n'] * pc['p_T']) / math.sqrt(pc['n'] * pc['p_T'] * (1 - pc['p_T']))), lambda l: '較正の検査の位置' in l)
for x in PH['raw_softmax_main']:
    if x['eligible']:
        chk('§3 事後の生の確率 ' + x['row'], '| %s | %s→%s | %s |' % (x['row'].replace('|', '\\|'), g4(x['raw_before']), g4(x['raw_after']), g4(x['raw_diff'])), lambda l: True)
for x in C['magnitude']['main_rows']:
    if x['eligible']:
        chk('§3 部分の表 ' + x['row'], '| %s | %s | %s |' % (x['row'].replace('|', '\\|'), g4(x['parts_fmain']['exact']), g4(x['parts_fmain']['layer1'])), lambda l: True)
# §3 の並べ直しの表が、凍結の表の行と縦棒のほか同じか
fro = [l for l in LN if re.match(r'\| S4\|O', l)]
esc = [l for l in LN if re.match(r'\| S4\\\|O', l) and l.count('|') - l.count('\\|') == 10]
m7.append({'item': '§3 並べ直しの表と凍結の表（縦棒のほか同じ）', 'want': '%d 行' % len(fro), 'lines': [], 'ok': sorted(l.replace('\\|', '|') for l in esc) == sorted(fro)})
# §8 の数え直しを、最終版の直した照合の表そのものから数える
h8 = [k for k, l in enumerate(LN) if l.startswith('| 欄 | 結果 | 登録者 | コーディネータ |')]
cnt = {'登録者': collections.Counter(), 'コーディネータ': collections.Counter()}
k = h8[-1] + 2
while LN[k].startswith('| p'):
    cells = [c.strip() for c in LN[k].strip('|').split('|')]
    for who, c in (('登録者', cells[2]), ('コーディネータ', cells[3])):
        cnt[who][re.search(r'（([^（）]+)）$', c).group(1)] += 1
    k += 1
lab = ('一致', '不一致', '該当なし', '予想しない')
want8 = '数え直し: 登録者 %s／コーディネータ %s。' % ('・'.join('%s %d' % (x, cnt['登録者'][x]) for x in lab), '・'.join('%s %d' % (x, cnt['コーディネータ'][x]) for x in lab))
chk('§8 数え直し（表から数えた）', want8, lambda l: True)
chk('§8 一致の注の数', '登録者の一致 %d のうち' % cnt['登録者']['一致'], lambda l: True)
reg_p1 = [LN[q] for q in range(h8[-1] + 2, k) if LN[q].startswith('| p1.nuclear.dir |')][0]
m7.append({'item': '§8 直した表の p1.nuclear.dir は登録者「一致」・p1.nuclear.label は登録者「不一致」', 'want': '', 'lines': [],
           'ok': '（一致）' in reg_p1.split('|')[3] and '（不一致）' in [LN[q] for q in range(h8[-1] + 2, k) if LN[q].startswith('| p1.nuclear.label |')][0].split('|')[3]})
chk('§9 加えた量', '残差のノルムの %s 倍' % g4(TL['layers']['relative_injection_selected']), lambda l: True)
nl = TL['inputs']['model']['num_hidden_layers'] - 1 - TL['layers']['indices'][L['primary']['ratio']]
chk('§9 後の層の数', '後の %d 層' % nl, lambda l: True)
chk('§9 門の限界の M_X', '順位相関 %s・割合 %s' % (g4(g['full']['M_X']['rho']), g4(g['full']['M_X']['p'])), lambda l: '門の検出力は低い' in l)
res['M7'] = m7

# ---- M8: 時点の古い語
m8 = []
for i, l in enumerate(LN):
    for w in ('草案', 'まだ', 'この後', '前の', '予定', 'これから', '次の', '見る。'):
        if w in l:
            m8.append({'line': i + 1, 'word': w, 'where': where(i)})
res['M8'] = m8

json.dump(res, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
bad1 = [x for x in res['M1'] if x['ok'] is False]
unk1 = [x for x in res['M1'] if x['path'] is None]
bad2 = [x for x in m2 if not x['exists']]
bad3 = [x for x in m3 if not x['defined']]
bad4 = [x for x in m4 if not x['exists']]
bad5 = [x for x in m5 if x['misaligned_lines']]
bad7 = [x for x in m7 if not x['ok']]
M = ['# 最終版の器の検査（機械生成・`check_final_Blens.py`・起草者の最終の見直しの A・2026-09-24）', '',
     '- 対象: `%s`（%d 行・SHA16 %s）。枠: `frame-final-read-Blens.md`（通読の前に書いた・e82536d）。' % (FINAL, res['M6']['lines'], res['M6']['sha16']),
     '- M1 SHA16: 当てた %d・合わない %d・名指しの無い 16 桁 %d。' % (sum(1 for x in res['M1'] if x['path']), len(bad1), len(unk1)),
     '- M2 パス: %d・無い %d%s。' % (len(m2), len(bad2), ('（%s）' % '・'.join('%d 行目 `%s`' % (x['line'], x['path']) for x in bad2)) if bad2 else ''),
     '- M3 番号: %d・記録に無い %d%s。台帳にあって最終版が一度も名指さない逸脱: %s。' % (len(m3), len(bad3), ('（%s）' % '・'.join('%d 行目 %s' % (x['line'], x['id']) for x in bad3)) if bad3 else '', '・'.join(res['M3_devs_not_named']) or 'なし'),
     '- M4 節の参照: %d・節が無い %d。' % (len(m4), len(bad4)),
     '- M5 表: %d・列の数が見出しと合わない表 %d%s。' % (len(m5), len(bad5), ('（%s）' % '・'.join('%d 行目から %d 行・合わない行 %s' % (x['first_line'], x['rows'], x['misaligned_lines']) for x in bad5)) if bad5 else ''),
     '- M6 区画の印: 始 %d・終 %d・対 %s・走査の違反 %d。' % (res['M6']['begin'], res['M6']['end'], res['M6']['balanced'], res['M6']['lint_violations']),
     '- M7 数の突き合わせ: %d・合わない %d%s。' % (len(m7), len(bad7), ('（%s）' % '・'.join(x['item'] for x in bad7)) if bad7 else ''), '',
     '## M1 の名指しの無い 16 桁', ''] + (['- %d 行目 %s' % (x['line'], x['printed']) for x in unk1] or ['- なし']) + [
     '', '## M4 節の参照（通読で中身を見る）', '', '| 行 | 参照 | 節がある | その節に足した区画がある |', '|---|---|---|---|'] + [
     '| %d | %s | %s | %s |' % (x['line'], x['ref'], x['exists'], x['target_has_added_block']) for x in m4] + [
     '', '## M8 時点の古い語の出る行（読みは通読で付ける）', '', '| 行 | 語 | 所 |', '|---|---|---|'] + ['| %d | %s | %s |' % (x['line'], x['word'], x['where']) for x in m8] + [
     '', '## 検分票', '', '- 対象: 最終版の器で調べられる型（SHA16・パス・番号・節の参照・表の列・区画の印・数の突き合わせ・時点の古い語）。', '- 段階: 枠の後・通読とは別に走らせた。',
     '- 凍結物の同定: 凍結の本文・正本・凍結した器の SHA16 は M1 で当てた。', '- 盲検の状態: 該当しない。',
     '- 敵対的検分: 数は組み立ての器を通さずに記録から読み直し、§8 の数え直しは最終版の表そのものから数えた。',
     '- 系統の内訳: コーディネータ（Claude 系）一名。', '- COI記録: 起草者は「合う」と出る側に引かれる。当て方は器で固定した。',
     '- 本検分が確認していないこと: 文の意味と読みの当否（通読で見る）。M7 は選んだ数だけで、最終版のすべての数ではない。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print(NL.join(M[:12]))
for x in bad1 + bad2 + bad3 + bad5 + bad7:
    print('BAD', x)
