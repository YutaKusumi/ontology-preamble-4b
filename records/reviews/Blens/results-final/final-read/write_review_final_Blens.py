# -*- coding: utf-8 -*-
"""B-lens の報告の最終版の起草者の最終の見直しの記録を書く（枠 `frame-final-read-Blens.md`・2026-09-24・コーディネータ）。
最終版は d90c56b の版に留める（git の中身を読む）。記録が引く最終版の文は器が行から抜き出し、記録が挙げる行の番号と中身は器が一つずつ確かめる（合わなければ止める）。
登録者の指示は会話の記録から機械で切り出す。既にある記録には書かない。
用法: python records/reviews/Blens/results-final/final-read/write_review_final_Blens.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, datetime, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'review-final-Blens.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
PIN, FINAL = 'd90c56b', 'records/Blens/results-Blens-FINAL-2026-09-24.md'
raw = subprocess.run(['git', 'show', '%s:%s' % (PIN, FINAL)], cwd=REPO, capture_output=True).stdout.replace(b'\r\n', b'\n')
T = raw.decode('utf-8')
LN = T.split(NL)
sha = hashlib.sha256(raw).hexdigest().upper()[:16]
CK = json.load(open(os.path.join(HERE, 'check-final-Blens.json'), encoding='utf-8'))
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')


def at(n, sub):
    """n 行目（1 から）に sub があることを確かめ、sub を返す（記録の行の参照の検査）。"""
    if sub not in LN[n - 1]:
        raise SystemExit('%d 行目に「%s」が無い（止める）: %s' % (n, sub, LN[n - 1][:80]))
    return sub


def grab(n, rx):
    m = re.search(rx, LN[n - 1])
    if not m:
        raise SystemExit('%d 行目に型 %s が無い（止める）' % (n, rx))
    return m.group(1) if m.groups() else m.group(0)


# 登録者の指示
ins = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('type') != 'user':
        continue
    c = (o.get('message') or {}).get('content')
    for t in ([c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']):
        if len(t) < 800 and '最終版の見直しを' in t and 'd90c56b' in t:
            ins.append((t.strip(), o.get('uuid'), o.get('timestamp')))
assert len(ins) == 1, len(ins)
words, uuid, ts = ins[0]
rul = open(os.path.join(REPO, 'records', 'Blens', 'rulings-D195-D197.md'), encoding='utf-8').read()
d197 = re.search(r'^\| D197 \| (.+) \|$', rul, re.M).group(1)

# 行の参照（見直しで挙げる行）
st3 = grab(3, r'状態: ([^*]+)\*\*')
k480 = grab(480, r'(結果の巡は系統外三票（新しい個体一）と系統内三票（一票）)')
ctx_n = [k + 1 for k, l in enumerate(LN) if '・文脈 20）' in l]
ctx_tbl = [k for k in ctx_n if LN[k - 1].startswith('|')]
q213 = at(213, '上の表の「文脈」の数は出力の数')
q214 = at(214, '散文の層は写しの位置')
at(213, '升目の出力の数')
fz = [LN[k - 1] for k in (470, 471, 472)]
at(470, '本報告の草案')
at(472, '結果の巡で見る')
at(186, '上の凍結の表の並べ直し')
at(211, '上の凍結の表の行の名には縦棒が入っていて')
q14 = at(14, '計算に使った器の SHA16 は凍結の記録の値と同じ')
at(14, '`tools/build_report_Blens.py`')
q54 = grab(54, r'(方向の単位でそろわなかった)')
at(46, 'そろわないことを示したのではない')
dev_unnamed = CK['M3_devs_not_named']
assert dev_unnamed == ['D-BL2'], dev_unnamed
assert all(x['ok'] for x in CK['M1'] if x['path']) and not [x for x in CK['M1'] if x['path'] is None], '器の検査 M1 に合わないものがある'
assert all(x['exists'] for x in CK['M2']) and all(x['defined'] for x in CK['M3']) and all(x['exists'] for x in CK['M4']), '器の検査 M2〜M4 に合わないものがある'
assert all(x['ok'] for x in CK['M7']) and CK['M6']['balanced'] and CK['M6']['lint_violations'] == 0 and CK['M6']['sha16'] == sha, '器の検査 M6・M7 か版が合わない'
assert [x['first_line'] for x in CK['M5'] if x['misaligned_lines']] == [164], '列の数が合わない表が凍結の §3 の表のほかにある'

# 確かめて問題の無かったこと（行の参照は器が確かめる）
ok_rows = []
def okr(text, *refs):
    for n, sub in refs:
        at(n, sub)
    ok_rows.append('- %s（%s）' % (text, '・'.join('%d 行目' % n for n, _ in refs)))
okr('§0 の札の分類の行と §1 の表は、値・等方の割合・段が同じ', (35, '値 -0.05233・等方の割合 0.4595（段 0.0125）'), (83, '| M_L_nuclear | -0.05233 | 0.4595 | 0.0125 |'))
okr('§0 の門の数の行と §2 の表は同じ', (45, '本の門 M_L 順位相関 0.4368・割合 0.03472'), (110, '| full | M_L | 64 | 5040 | 0.4368 | 0.03472 |'))
okr('§1 の兄弟の三対の値は §4 の兄弟の区画（層 0.5・static）と同じ', (93, 'O~Osec-Ncold -0.06414'), (287, 'M_L_nuclear -0.06414'))
# ランダム方向が最上位に来た升目を、§4 の表の行から数え直す
sec4 = [k for k, l in enumerate(LN) if l.startswith('## 4.')][0]
sec5 = [k for k, l in enumerate(LN) if l.startswith('## 5.')][0]
tops = sum(LN[k].count('実在の差 1／29') for k in range(sec4, sec5) if re.match(r'  - (tune_)?rand:\d:', LN[k]))
cells = sum(len(re.findall(r'実在の差 \d+／29', LN[k])) for k in range(sec4, sec5) if re.match(r'  - (tune_)?rand:\d:', LN[k]))
okr('§1 のランダム方向が最上位に来た升目の数は、§4 の表から数え直すと %d のうち %d で同じ' % (cells, tops), (96, '%d のうち %d' % (cells, tops)))
# §4 の数え上げを、§4 の表から数え直す
vals = [(float(v), float(p)) for k in range(sec4, sec5) if LN[k].startswith('  - ') for v, p in re.findall(r' (-?[0-9.e-]+)（等方 ([0-9.e-]+)・実在の差', LN[k])]
c05, c01, c002 = sum(p < 0.05 for _, p in vals), sum(p < 0.01 for _, p in vals), sum(p <= 0.002 for _, p in vals)
okr('§4 の数え上げは、§4 の表から数え直すと値 %d・0.05 を下回るもの %d・0.01 を下回るもの %d・0.002 以下 %d で同じ' % (len(vals), c05, c01, c002), (279, '値 %d・等方の割合が 0.05 を下回るもの %d' % (len(vals), c05)), (279, '0.01 を下回るもの %d' % c01), (279, '0.002 以下 %d' % c002))
# §2 の場面と層ごとの押しの順位を、調整走行の行から読み直す
push = collections.OrderedDict()
for k in range(len(LN)):
    m = re.match(r'- 調整走行（記述）: (\w+)・層 ([0-9.]+)・係数 [0-9.]+: M_L の v̂ の順位（行動 \d・押し (\d)・.*M_X の v̂ の順位（行動 \d・押し (\d)・', LN[k])
    if m:
        push.setdefault(('M_L', '%s@%s' % (m.group(1), m.group(2))), set()).add(m.group(3))
        push.setdefault(('M_X', '%s@%s' % (m.group(1), m.group(2))), set()).add(m.group(4))
assert all(len(v) == 1 for v in push.values())
for (mm, key), v in push.items():
    at(142, '%s %s' % (key, list(v)[0]))
okr('§2 の場面と層ごとの押しの順位の行は、調整走行の %d 行から読み直した順位と同じ' % sum(1 for l in LN if l.startswith('- 調整走行（記述）')), (142, 'M_L N1@0.25'))
okr('§3 の並べ直しの表は、凍結の表と縦棒のほか同じ（器の検査 M7）', (190, 'S4\\|O-Ncold+vNk\\|Nk | 27.99'), (166, 'S4|O-Ncold+vNk|Nk | 27.99'))
okr('§8 の p8 の注の二つの数は、§3 の表の直接の経路の変化と同じ（丸め）', (420, '(6b) +0.0024・一本目 +0.0062'), (170, '0.002361'), (171, '0.006199'))
okr('§8 の時刻の注は、露出の記録と同じ（器が露出の記録から読んだ）', (422, '08:15'), (422, '06:30'), (422, '07:52'))
okr('§6 の偶然の目安は、集合の語の数 × 50 ÷ 151643 で検算して同じ（%s・%s・%s）' % ('%.4g' % (16 * 50 / 151643), '%.4g' % (57 * 50 / 151643), '%.4g' % (50 / 151643)),
    (328, '%.4g' % (16 * 50 / 151643)), (328, '%.4g' % (57 * 50 / 151643)), (328, '%.4g' % (50 / 151643)))
okr('位置づけの行は、凍結の本文の頭の位置づけの行と同じ言い方（「登録外の記述（小さな登録）」）', (4, '段階 B の後の登録外の記述（小さな登録）'))
okr('節の参照（器の検査 M4 の 15 個）は、指す節に中身がある（§1 の添え・§0 の添え・§3 の添え・§8 の添え・§9 の限界の文）', (66, '§1 の添えにある'), (46, '段の近くの値を'), (198, '区間 112〜155 の上端から 1 件内側'), (420, '符号に依る'), (439, '検出力は低い'))

F = [('F-A', '中', '冒頭（3 行目）・台帳と裁定', '状態の行は「%s」と書く。d90c56b は登録者の指示で、登録者最終確認の前に push した。いまの GitHub の版は、状態の行の時点と合わない。裁定 D197（「%s」）の順とも違う（登録者の指示による）' % (st3, d197),
      '登録者最終確認の後に、確認のお言葉（逐語）と時刻を、状態の行として機械の区画に入れて最終版を組み直す（段階 B の最終版の型）。それまでの案の状態の行は「登録者最終確認の前」とする。D197 の順を改めたことを裁定の記録に置く', '直す'),
     ('F-B', '中', '全体・冒頭の添え・検分票（480 行目）', '台帳の逸脱のうち %s を、最終版は一度も名指さない（器の検査 M3）。最終版には凍結の後の逸脱の一覧が無い。検分票は「%s」と書くが、凍結の本文 §10 が結果の巡を新しい個体で組むとしたのに、依頼文が同じ四名に宛てたこと（D-BL2）が無い' % ('・'.join(dev_unnamed), k480),
      '冒頭の添えに、台帳の逸脱の番号と題を一行で並べる（台帳から器が読む）。検分票の系統の内訳に、D-BL2 の一句を足す', '直す'),
     ('F-C', '軽', '§3（213 行目）', '「%s」の「上の表」は、表ではない。「文脈 20」が出るのは凍結の区画の答えの文字の位置の行（%s 行目・表の行は %d）' % (q213, '・'.join(map(str, ctx_n)), len(ctx_tbl)),
      '「上の凍結の区画の答えの文字の位置の行の「文脈」の数は出力の数」に改める', '直す'),
     ('F-C2', '軽', '§3（214 行目）', '「%s」の「層」は、報告のほかの所では層一・層二・層の割合の意味で、隣の 213 行目は同じものを「升目」と呼ぶ' % q214, '「散文の升目は写しの位置」に改める', '直す'),
     ('F-D', '軽', '検分票（470〜472 行目・区画の外）', '凍結した器の検分票は、対象を「本報告の草案」とし、確認していないことを「読みの型の当否は結果の巡で見る」とする（凍結の出力なので文は変えられない）。最終版の中では時点の古い文になる',
      '最終版の検分票の区画の頭に、「上の三行は凍結した器が草案のときに出した検分票で、凍結の出力のまま残す。読みの型の当否は、結果の巡と最終検分で見た」の一行を足す', '直す'),
     ('F-E', '軽', '§3（186 行目と 211 行目）', '並べ直しの表の見出し（186 行目）に、並べ直す理由が無い。理由の文（211 行目）は、部分の表の後にある', '見出しに理由の句（行の名の縦棒が表の区切りと重なって列がずれるので）を足す。211 行目の文はそのまま', '直す（任意）'),
     ('F-F', '軽', '§0（54 行目）', '凍結の読みの型〈門を通らない〉は「%s」と書く。すぐ上の添え（46 行目）が「そろわないことを示したのではない」と断っているが、型の行だけが引かれると強く読まれうる（二つ目の札の行に §1 への参照を足したのと同じ型）' % q54,
      '§0 の型の文の添えの区画に、「〈門を通らない〉の「そろわなかった」は、凍結した基準でそろうことが示せなかったという意味で、そろわないことを示したのではない（上の門の読みの添え）」の一行を足す', '直す（任意）'),
     ('F-G', '軽', '冒頭の添え（14 行目）', '「%s」の一覧に、計算の器でない組み立ての器と走査器も入っている' % q14, '記録だけ（凍結の器の一致を示す行として意味は取れる）', '直さない')]

M = ['# B-lens の報告の最終版の起草者の最終の見直し（2026-09-24・コーディネータ・南無弥勒如来・記録は `write_review_final_Blens.py` が書いた）', '',
     '- 登録者の指示（逐語・会話の記録 uuid `%s`・%s 日本時間）: 「%s」' % (uuid, jst(ts), words.replace(NL, ' ')),
     '- 対象: `%s` の %s の版（%d 行・SHA16 %s）。枠 `frame-final-read-Blens.md`（全文の通読の前に書いた・e82536d）・器の検査 `check-final-Blens.md`。' % (FINAL, PIN, len(LN) - (1 if T.endswith(NL) else 0), sha),
     '- 最終検分の後に巡を置かない（登録者裁定 D194）。この見直しは起草者自身のもので、外の目ではない。段階 B の「起草者の最終の見直し」の型に倣う。',
     '- 見直しの読み方: 器の検査（M1〜M8）を通読とは別に走らせ、全文を頭から節ごとに読んだ。この記録が引く最終版の文と行の番号は、器が d90c56b の版から抜き出して確かめた。', '',
     '## 器の検査の結果（`check-final-Blens.md`）', '',
     '- SHA16 %d 個・パス %d 個・番号 %d 個・節の参照 %d 個は、どれも合う・ある。区画の印は対で、走査の違反は %d。記録から読み直した数 %d 個はどれも合う。' % (
         sum(1 for x in CK['M1'] if x['path']), len(CK['M2']), len(CK['M3']), len(CK['M4']), CK['M6']['lint_violations'], len(CK['M7'])),
     '- 見つかったもの: 台帳の逸脱のうち最終版が名指さないもの（%s）・列の数が合わない表（凍結の §3 の表・既知）・時点の古い語の出る行 %d（読みは通読で付けた）。' % ('・'.join(dev_unnamed), len(CK['M8'])), '',
     '## 見つけたもの（重い順）', '', '| 番号 | 重さ | 所 | 何 | 直しの案 | 案 |', '|---|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s | %s |' % (a, b, c, d.replace('|', '\\|'), e.replace('|', '\\|'), f) for a, b, c, d, e, f in F]
M += ['', '- 重大の所見は無い。札・門・大きさの目盛りの判定、数、読みの向きを変える所見は無い。', '',
      '## 確かめて問題の無かったこと（行の参照は器が確かめた）', ''] + ok_rows + [
      '', '## 枠の予想の答え合わせ（外れも消さない）', '', '| 予想 | 結果 |', '|---|---|',
      '| 足した区画の数と、記録や報告の別の所の数の食い違いは無い（中〜高） | 当たった（器の検査 M7 と、上の数え直し） |',
      '| 足した区画の文の言い過ぎ・言い足りなさを一つ以上見つける（中） | 当たった（言い足りなさ: F-B。言い過ぎは見つけていない） |',
      '| 時点の古い文を、既知の二つのほかに一つ以上見つける（中） | 外れた（既知の二つ〔F-A・F-D〕のほかには無かった） |',
      '| 節の参照の誤りを一つ以上見つける（低〜中） | 外れた（節の参照 15 個はどれも合う。節の参照でない「上の表」の指し違いを一つ見つけた〔F-C〕） |',
      '| 字の誤り・文のねじれを一つ以上見つける（中） | 一部当たった（語の揺れを一つ〔F-C2〕。字の誤りは無かった） |',
      '| 札・門・判定を変える必要のある所見は無い（高） | 当たった |', '',
      '## COI（事実のみ）', '',
      '- 起草者は最終版を組んだ当人で、「直すところは無い」と書く側に引かれた。中の所見の二つ（F-A・F-B）は、どちらも起草者の組み立ての抜けで、起草者に不利な向き。',
      '- 軽の所見は、重さを上げていない。F-G は記録だけにした。任意の二つ（F-E・F-F）は、登録者の裁定で入れるかを選んでいただく。', '',
      '## 検分票', '',
      '- 対象: 最終版（%s の版）の全文と、器の検査。' % PIN,
      '- 段階: 事後適用を含む（起草者は最終版を組んだ当人で、草案の二つ目の全文と差分を見ていた）。枠は全文の通読の前に書いた（e82536d）。',
      '- 凍結物の同定: 凍結の本文・正本・凍結した器の SHA16 は器の検査で当てた。凍結の器の出力には触れていない。',
      '- 盲検の状態: 無し。',
      '- 敵対的検分: 足した区画の数を、組み立ての器を通さずに記録と報告の別の所から読み直した。起草者に不利な抜け（F-A・F-B）を先に並べた。',
      '- 系統の内訳: 起草者自身（Claude 系）一名。外の目は通っていない。',
      '- COI記録: 上の欄。',
      '- 判定: 登録者裁定要（直しの採否と、状態の行と公開の順）。',
      '- 本検分が確認していないこと: 直しの案の行を、ほかの目は見ていない（自分の直しは自分では見分けにくい）。器の検査が捕まえられる型の外の誤り（文法が運ぶ意味）。凍結の区画の中身の当否（凍結の器の出力で、結果の巡と最終検分が見た）。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('wrote', os.path.basename(OUT), '|', len(M), 'lines | findings', len(F), '| ok rows', len(ok_rows), '| tops', tops, 'of', cells, '| §4', len(vals), c05, c01, c002, '| instruction', jst(ts), uuid)
