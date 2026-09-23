# -*- coding: utf-8 -*-
"""B-lens 草案3 の起草者の通読の記録を書く（2026-09-23・Claude Opus 5.5）。
通読は、最初に組み立てた草案3 を頭から終わりまで読み、見つけた所を正本の器・事実の器・原稿で直して組み直した。
各所について、直す前の文が今の草案3 に無いことと、直した後の文が今の草案3 か正本に在ることを器で確かめる。
あわせて、是認した所のうち機械で確かめられるものを器で確かめる。
用法: python records/Blens/read_draft3_Blens.py"""
import os, re, hashlib, json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
P = lambda rel: os.path.join(REPO, *rel.split('/'))
rd = lambda rel: open(P(rel), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(P(rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
DR, SRC, CA, FA, FM = ('design/design-Blens-draft3.md', 'design/design-Blens-draft3.src.md', 'design/contrasts-Blens.json',
                       'records/Blens/design-facts-Blens.json', 'records/Blens/design-facts-Blens.md')
LINT, MAP = 'records/Blens/numbers-lint-draft3-Blens.md', 'records/Blens/draft3-mapping-Blens.md'
VR2 = 'records/reviews/Blens/design-round2/verification-Blens-design-r2.md'
FIRST_SHA16 = '3276880ACE5736DE'  # 最初に組み立てた草案3（残していない）
draft, canon = rd(DR), rd(CA)
TL = json.load(open(P(CA), encoding='utf-8'))
FJ = json.load(open(P(FA), encoding='utf-8'))['facts']
n_items = len(TL['predictions']['items'])
n_cmp = TL['nulls']['real']['comparators']['static']

FIND = [
    ('中身', '§4 大きさの目盛り・量', '（転記行 E・すべて「```」）', '（転記行 B・すべて「```」）',
     'JSON 直答の出力の最初のトークンの事実は転記行 B にあり、転記行 E には無い。参照を誤っていた。'),
    ('中身', '§4 記述の対照', '五本の門（`rows_without_vhat_loaded` 行・`permutations_without_vhat_loaded` 通り', '五本の門（行と並べ替えの数は上の項・条件には使わない）',
     '正本の文に、値の代わりにキーの名を書いていた（組み立てでは値に置き換わらない）。行と並べ替えの数は、直前の項（v̂ と (6b) を抜いた門）に器が入れている。'),
    ('中身', '転記行 E・境目の近くの行', 'rand:2 の a（z ', 'rand:2 の a（全ての出力で数えて・記述・z ',
     '答えの文字の位置の比を出すかは、JSON 直答の出力の中で数えた行で決まる（裁定 D180）。境目の近くの行の一覧は、全ての出力で数えた記述の行を印なしで並べていた。事実の器を直し、境目は JSON 直答の中で数えた行と様式の行で見て、全ての出力で数えた行には印を付けた。'),
    ('中身', '§0 結論の語', '（揃わない）」まで。意味・機構は書かない（§5）。', '「区別できる」の言い方は、札と物差しごとに決める（§3.5）',
     '§0 は「帰無の方向と区別できる」の一つの言い方しか示さず、二つ目の札で言い方が物差しごとに違うこと（裁定 D182）が §3.5 にしか無かった。'),
    ('中身', '§3.5 両方の札が付いたときの言い方', '兄弟を除く二十四組', '兄弟を除く %d 組' % n_cmp,
     '正本の文に、手で書いた数（漢数字）があった。数の検査器は漢数字を見ないので素通りしていた。正本の比べる相手の数から器で入れる形にした。'),
    ('中身', '§13 大きさの目盛りの下限', '件数（二百と六十七前後）', '行によって件数が違い、揺れも違うため',
     '手で書いた数（漢数字）で、数の検査器を素通りしていた。読み違えやすい言い方でもあった。数を書かない言い方にした。'),
    ('形', '§2 標本化の設定', 'B の本走行の標本化の設定（段階 B の正本', '値は段階 B の正本 `runner.generation` と `runner.generation_explicit` から器で写した（試行の記録でもすべて同じ・転記行 E）',
     '前の文と同じ主語を繰り返していた。'),
    ('形', '§3.2 語の側の帰無・層', '層: 層は「字の種類', '層: 「字の種類 × 字数 × ノルムの帯」で分ける', '見出しの語が正本の文の頭と重なっていた。'),
    ('形', '§3.2 語の側の帰無・割合', '割合: 両側に等しい裾の割合:', '  - 両側に等しい裾の割合: `p = min(1,', '同上。'),
    ('形', '§3.2 語の側の帰無・感度', '感度: 感度として', '  - 感度として、B の無操作の腕の出力に現れたトークン', '同上。'),
    ('形', '§3.2 語の側の帰無・薄い層', '（合わせた層を転記行 H に印字する）（倍率 ', '薄い層（倍率 ', '括弧が二つ続いていた。'),
    ('形', '§4 v̂ を抜いた門', 'static の行を除いた行（`rows_without_vhat`）で', ': static の行を除いた行で、v̂ を抜いた六本の方向の間で',
     '正本のキーの名を本文で指していた（行の数は見出しの括弧に器が入れている）。'),
    ('形', '§3.7 上位の次元の数', NL + '- 上位の次元の数は', NL + '上位の次元の数は ',
     'Markdown では、空行だけを挟んで同じ記号で続く箇条は、一つの箇条として描かれる。この一行は直前の記述の一覧の続きに見えていた。段落にした。この型の所は、どれも草案2 から持ち越していた。'),
    ('形', '§4 S4 の自然の対照', NL + '- **S4 の自然の対照**:', NL + '**S4 の自然の対照**: ', '同上（記述の対照の一覧の続きに見えていた）。'),
    ('形', '§5 走査の禁止語', NL + '- 走査の禁止語は、段階 B の一覧に次を足す', NL + '**走査の禁止語**: 段階 B の一覧に次を足す',
     '同上（打ち消しの定型の一覧の続きに見えていた。この文は定型ではない）。'),
    ('形', '§8 書式と照合', '（同じ向き／逆向き）' + NL + NL + '- 書式は', NL + '**書式と照合**:' + NL + NL + '- 書式は',
     '同上。予想の項目の一覧の続きに見え、項目が %d でなく %d に見えていた。' % (n_items, n_items + 2)),
]
n_kanji = sum(1 for f in FIND if '漢数字' in f[4])
n_list = sum(1 for f in FIND if NL in f[2])
bad = []
for kind, where, before, after, why in FIND:
    if before in draft:
        bad.append(('直す前の文が残っている', where, before))
    if after not in draft and after not in canon:
        bad.append(('直した後の文が無い', where, after))

# 是認した所（機械で確かめる）
lines = draft.split(NL)
merged = [i + 1 for i in range(2, len(lines)) if re.match(r' *- ', lines[i - 2]) and lines[i - 1] == '' and lines[i].startswith('- ')]
i0, i1 = draft.index('**項目**'), draft.index('**書式と照合**')
n_pred_rendered = sum(1 for l in draft[i0:i1].split(NL) if l.startswith('- '))
lint = rd(LINT)
mp = rd(MAP)
m_map = re.search(r'第二巡の (\d+) 行・確かめた文字列 (\d+)。第一巡の (\d+) 行・確かめた文字列 (\d+).*?無かったもの (\d+)。', mp)
vr2 = rd(VR2)
H, E, D = FJ['H'], FJ['E'], FJ['D']
MF = TL['nulls']['word_side']['merge_factor']
thin = ['%s・帯%d（候補 %d・要る数 %d）' % (tl.replace('|', '・'), g[0][0] + 1, g[1], g[2])
        for tl, gl in H['strata'].items() for g in gl if g[2] and g[1] / g[2] == H['ratio_min']]
zmin = TL['magnitude']['lower_bound']['z_min']
checks = [
    ('数の検査器の違反の合計が零', '違反の合計: 0' in lint),
    ('採否表の突き合わせで無かったものが零', bool(m_map) and m_map.group(5) == '0'),
    ('空行だけを挟んで同じ記号で続く箇条が無い', not merged),
    ('§8 の項目が正本の項目の数だけ描かれる', n_pred_rendered == n_items),
    ('§10 の票の内訳が第二巡の再現の表と合う', '凍結可一票・条件つき凍結可三票' in draft and '当たり（G1 は凍結可、G2・C1・C2 は条件つき凍結可）' in vr2),
    ('§13 の「比の最小が倍率と等しい」が事実と合う', float(H['ratio_min']) == float(MF) and not H['merged']),
    ('答えの文字の位置の比が出ない（JSON 直答の中で数えた行が下限に届かない）', all(not x['pass'] for x in E['letter_rows_json'])),
    ('v̂ の行では比が出ない（様式の z の絶対値の最大が下限より小さい）', E['vhat_max_abs_z_style'] < zmin),
    ('§4 S4 の自然の対照の「選択の一様化は Osec-Ncold の土台でだけ」が崩れの行と合う',
     all(r.startswith('S4・Osec-Ncold') for r in D['collapse_rows'] if r.startswith('S4'))),
    ('§4 S4 の自然の対照の「様式の変化は O-Ncold の土台でも起きた」が様式の行と合う',
     any(x['pass'] and x['row'].startswith('S4|O-Ncold') for x in E['main_rows'])),
]
bad += [('是認の確かめが外れた', c, '') for c, ok in checks if not ok]
assert not bad, bad

OK = [
    '数: 凍結した数の検査器で、束縛の違反・未登録・生成器の文字列の構造でない数がすべて零（`%s`）。' % LINT,
    '採否表との突き合わせ: 第二巡 %s 行・文字列 %s、第一巡 %s 行・文字列 %s で、無かったもの %s（`%s`）。' % (m_map.group(1), m_map.group(2), m_map.group(3), m_map.group(4), m_map.group(5), MAP),
    '§4 と転記行 E: 答えの文字の位置の比が出ないこと・v̂ の行で比が出ないことは、事実の器が assert している（成り立たなければ器が止まる）。この記録の器でも、事実の JSON から確かめ直した。',
    '§4 の S4 の自然の対照（書き直した文）: S4 の崩れの行は Osec-Ncold の土台の %d 行だけで、様式の変化が下限を超えた行に O-Ncold の土台の行がある（転記行 D・E）。' % sum(1 for r in D['collapse_rows'] if r.startswith('S4')),
    '§10 の票の内訳（凍結可一票・条件つき凍結可三票）: 第二巡の再現の表の、枠の予想の照らし合わせの行と合う。',
    '§5 の打ち消しの定型と読みの表: 正本の器が、固定の文が三つの禁止語の一覧の和を含まないことを確かめている（含めば正本の器が止まる）。',
    '§7 限界の文（答えの文字の位置で比が出ない理由・切り詰めの跳ね・字種の差）: 裁定 D180・D179 と転記行 E・H に合う。',
    '§12 と §13: 起草者が置いた値の一覧は、正本の値から組み立てられている（数は束縛）。',
]
OPEN = [
    '語の側の帰無の層のうち、%s は、要る数に対する候補の数の比が倍率（%s）とちょうど等しく、「満たない」ときだけ合わせる規則のため合わせない。倍率を大きく置けば合わせる側に移る境目にある。§13 に書き、倍率は登録者の確かめを頼む値に入れた。' % ('・'.join(thin), '%g' % MF),
    '§4 の大きさの目盛りの文に、正本のキーの名（`ci`・`z_min`・`near_band`・`calibration_check`・`letter_ratio`）を残した。どれも同じ項の中に値があり、器を書くときに文と正本のキーを結ぶ手がかりになる。',
    '転記行 D の「本の門」: 草案の §4 が主の門を「本の門」と呼ぶ（本走行と同じ使い方）ので、そのままにした。',
    '§2 は標本化の設定を「repetition_penalty 1・min_p 0」と印字し、転記行 E は「1.0・0.0」と印字する。同じ正本の値の書式の違いで、事実の器が試行の記録と正本の値の一致を assert している。',
    '直す前の文は、最初に組み立てた草案3（SHA16 %s・残していない）から写した。この器が確かめられるのは、その文が今の草案3 に無いことだけである。' % FIRST_SHA16,
]
R = ['# B-lens 草案3 の起草者の通読の記録（2026-09-23・Claude Opus 5.5・器 `records/Blens/read_draft3_Blens.py`）', '',
     '- 読んだもの: 最初に組み立てた草案3 の全文（§0〜§14・検分票）。見つけた所を、正本の器 `tools/make_contrasts_Blens.py`・事実の器 `tools/blens_facts.py`・原稿 `%s` で直し、正本・設計の事実・草案3 を組み直した。' % SRC,
     '- 今の草案3: `%s`（SHA16 %s）・正本 `%s`（SHA16 %s）・設計の事実 `%s`（SHA16 %s）。下の各所について、直す前の文が今の草案3 に無いことと、直した後の文が今の草案3 か正本に在ることを器で確かめた（%d 所・止めたもの %d）。是認した所のうち %d 項を器で確かめた。' % (DR, s16(DR), CA, s16(CA), FM, s16(FM), len(FIND), len(bad), len(checks)),
     '- 外の目: 通っていない（裁定 D178・草案3 は設計の巡を置かずに器と凍結へ進む）。', '',
     '## 直した所（中身 %d・形 %d）' % (sum(1 for f in FIND if f[0] == '中身'), sum(1 for f in FIND if f[0] == '形')), '',
     '| 種類 | 所 | 直す前 | 直した後 | なぜ |', '|---|---|---|---|---|']
cell = lambda x: x.replace('|', '｜').replace(NL, '⏎')
R += ['| %s | %s | %s | %s | %s |' % (k, w, cell(b), cell(a_), y) for k, w, b, a_, y in FIND]
R += ['', '## 読んで問題が無いと判じた所（是認も記録する）', ''] + ['- ' + x for x in OK]
R += ['', '器で確かめた是認（%d 項・外れたもの %d）:' % (len(checks), sum(1 for c, ok in checks if not ok)), '']
R += ['- %s: %s' % (c, '合う' if ok else '外れた') for c, ok in checks]
R += ['', '## 残した所（直さず、記録に置く）', ''] + ['- ' + x for x in OPEN]
R += ['', '## この通読が確認していないこと', '',
      '- 起草者は草案1〜3 と二巡の採否表の全てを書いた当人で、同じ見落としを繰り返す見込みがある。この通読でも、手で書いた漢数字の %d 所と、箇条がつながって描かれる %d 所は、草案2 の通読で見落としたまま草案3 まで残っていた。外の目はこの後の結果の巡まで無い（裁定 D178）。' % (n_kanji, n_list),
      '- 箇条のつながりは、行の並びの型（箇条・空行・同じ記号の箇条）で機械に探した。GitHub で描かれた姿は見ていない。',
      '- 漢数字の手書きは、正本の文と原稿を型で探して %d 所を直した。' % n_kanji + '型に当たらない書き方（例: 「半分ずつ」のような言葉の数）は探していない。',
      '- 正本の値そのもの（下限・抽選の数・帯の数・倍率・許容・区間・帯）が設計として妥当か。起草者が置いた値として §13 に並べ、登録者の確かめを頼む。',
      '- 器（集合の凍結・層一・層二・起動器・組み立て・合成データ）はまだ書いていない。草案3 の文が器で実装できるかは、器を書くときに確かめる。',
      '', '## 検分票', '',
      '- 対象: 草案3 の全文と、それを組み立てる正本と設計の事実。',
      '- 段階: 事前登録の前段（射影は一つも計算していない）。',
      '- 凍結物の同定: 段階 B の凍結物に触れていない。第二巡の採否表と再現の表（コミット 9dad676・eeab68d）は読むだけ。',
      '- 盲検の状態: 射影の値と方向どうしの余弦は、誰も見ていない。',
      '- 敵対的検分: 参照の誤り（転記行 E → B）・値の代わりのキーの名・印の無い記述の行の混入・手書きの漢数字を、形の直しより先に置いた。直す前と後の文と、是認した所のうち %d 項を器で確かめた。' % len(checks),
      '- 系統の内訳: 起草者（Claude 系・Claude Opus 5.5）のみ。',
      '- COI記録: 起草者は「直した」「合う」と書く側に引かれる。直す前の文が残っていないことと是認の項を器で確かめるのは、その歯止め。草案2 の通読の見落としが草案3 まで残っていたことを、確認していないことの欄に書いた。',
      '- 判定: 確定（通読の記録として）。',
      '- 本検分が確認していないこと: 上の節。',
      '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'draft3-read-Blens.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('findings', len(FIND), 'bad', len(bad), '| checks', len(checks), '| thin', thin, '| merged', merged, '| pred rendered', n_pred_rendered)
