# -*- coding: utf-8 -*-
"""B-lens の枠（草案2）の設計の巡・第二巡（凍結前の最終検分・登録者裁定 D178）の依頼文と束を組む。
束の部: 第一部 依頼文／第二部 草案2（全文）／第三部 第一巡からの直しの記録（採否表・突き合わせの表・起草者の通読・再現の表・第一巡の是認の抜き書き・裁定 D168〜D178）／
第四部 正本 v2（全文）／第五部 材料 v2（前置きと場面の本文・語の集合の一覧・大きさの目盛りの行・ランダム方向の関数）と設計の事実の器 v2。
変わっていない材料（段階 B の結果の最終版）は第一巡の束のまま（索引に置き場を書く）。語の集合の一覧は、設計の事実の記録のトークンの番号を手元のトークナイザで文字に戻して器が作る（射影は計算しない）。
束が長いときは、部の境で分けた版も作る。
用法: python records/reviews/Blens/design-round2/make_bundle_Blens_design_r2.py"""
import os, ast, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
head = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()
TB = json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8'))
TL = json.load(open(j('design', 'contrasts-Blens.json'), encoding='utf-8'))
FJ = json.load(open(j('records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
assert FJ['contrasts_sha16'] == s16('design/contrasts-Blens.json'), '設計の事実が今の正本から作られていない'
assert TL['version'] == 'draft2-2026-09-23'
R1_BUNDLE = 'records/reviews/Blens/design-round1/bundle-Blens-design-all-in-one.md'
R1_BUNDLE_SHA = hashlib.sha256(open(j(*R1_BUNDLE.split('/')), 'rb').read()).hexdigest().upper()[:16]

REQ = ['# B-lens の枠（草案2）の設計の検分のお願い（第二巡・凍結前の最終検分）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-23。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （草案2 は公開済みのコミット %s。束はその後に手元で組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % head,
       '- **これは凍結前の最終検分です。** 第一巡の四票はすべて「条件つき可」で、差し戻しはありませんでした。登録者は、草案2 を第一巡と同じ四名に一巡だけ見ていただき、それを凍結の前の最後の検分とすると決めました（裁定 D178）。この巡のあとは、裁定・草案3・器と合成データ・凍結へ進み、設計の巡をもう一度は置きません。凍結の前に直せるのは、この巡の所見が最後です。',
       '- **お願い: 射影を計算しないでください。** 登録者とコーディネータの予想の封印がまだで、結果が会話に出ると予想の独立が崩れます。式や手順の検算（射影の値を出さないもの）は歓迎します。',
       '- **お願い: 結果の見込みを書かないでください。** 第一巡の票は結果の見込みを書かずにいてくださいました。今回も同じにお願いします（設計の穴の指摘は歓迎します。予想者はこの票を封印の前に読みます）。',
       '- **同じ四名への二巡目**: あなたは第一巡で草案1 を見た四名のお一人です。第一巡の束（草案1・段階 B の結果の最終版など）と、あなたの第一巡の票は、この会話にあるはずです。第一巡の票は公開の置き場の `records/reviews/Blens/design-round1/<名>/review.md` にもあります。採否表の出所の札は、G1・G2（Gemini 3.8 Flash の一人目・二人目）と C1・C2（claude.ai の一人目・二人目）で、所見の番号は票の番号のままです（例: C1-8 は claude.ai の一人目の所見 8）。',
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）を書いてください。claude.ai の Claude Opus 5.5 は起草者と同じ機種で、何票でも一票に数えます。',
       '- **草案2 で改まった所**: 草案2 の §0 の「草案1 から大きく変えた所」と、第三部の突き合わせの表（採否表の各行が草案2 のどこで受けられたか）と、起草者の通読の記録にあります。第一巡の四票の是認と総括の抜き書き（第三部）も付けました。',
       '- **草案2 を書いた後に決まったこと**: 第二巡を置くと決めた裁定 D178 は、草案2 の後です。草案2 の §10 の「設計の巡は一巡で済んだ」と §12 の「草案2 は外の目を通らずに器と凍結へ進む」は古い文で、草案3 で改めます（所見に挙げなくて構いません）。',
       '- **束の中身**: 第一部 依頼文／第二部 草案2（全文）／第三部 第一巡からの直しの記録／第四部 正本 v2（全文）／第五部 材料 v2 と設計の事実の器 v2。変わっていない材料（段階 B の結果の最終版）は第一巡の束のまま（`%s`・SHA16 %s）。' % (R1_BUNDLE, R1_BUNDLE_SHA),
       '- **褒めるのではなく、凍結の前に設計を崩すつもりで読んでください。** とくに、第一巡の後に起草者が一人で書いた所は、まだ外の目を通っていません。', '',
       '## 1. 伺いたいこと', '',
       '1. **第一巡の所見の直り**: あなたの第一巡の所見は、草案2 で正しく直ったか。直しが所見を取り違えていないか、半分しか直っていないものはないか。採否表の要約が、あなたの所見の語を強めたり弱めたりしていないか。不採の二件（P496・P526）の理由は納得できるか。',
       '2. **直しが作った新しい穴**: 第一巡の後に起草者が一人で書いた所——方向を単位にした門（七本・全ての入れ替え・v̂ を抜いた門）、二つ目の札（兄弟を除いた二十四組・語の側の帰無の作り方〔字の種類とノルムの帯〕）、大きさの目盛り（二つの位置・比を出す行の下限の規則・主位置の比を全ての行に広げたこと・v̂ の行で比が出ないこと）、様式の物差し（主の一つのトークン・感度の集合が二つしか残らないこと）、読みの表（八つの型・否定の文・禁止語の作り方・打ち消しの定型）、限界と予想の項目の直し——に、穴はないか。',
       '3. **起草者が置いた値（§13）**: 下限（二標本の z の絶対値 2 以上）・語の側の帰無の抽選の数と種と帯の数・logits の突き合わせの許容・等方の帰無の自己検査の許容・上位の次元の数。値の決め方に、段階 B の公開済みの行動を見た後の選び方が入っていないか。',
       '4. **事実（§6 の転記行 A〜H と第五部の一覧）**: 語の集合（片仮名一字を外した後の中身・落ちた字・X の印・重なり）、校正の升目（方向の単位・崩れの行）、大きさの目盛りの層と比を出す行、語の側の帰無の候補の数に、明らかにおかしいものはないか。',
       '5. **同じ型の穴**: 散文と機械の区画の食い違い、器と器の食い違い、合成データの「当たり前の形」に隠れる穴、直しの中に入る起草者の側への傾きが、草案2 に残っていないか。',
       '6. **器に回してよいものと、正本に書かないといけないもの**: 凍結の後に正本を変えると逸脱になります。器の実装で決めてよい細部と、凍結の前に正本に書いておかないといけない決まりを分けてください。',
       '7. **総合**: 凍結に進めるか（凍結可／条件つき凍結可／差し戻し）。**凍結の前に直すもの**と、**記録に置けば足りるもの**に分けてください。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 段階 B の結果（率と p）は公開済みで、伏せていません。起草者は草案2 を書いた当人で「直した」と書く側に、登録者は結果に希望を持つ側に引かれています。どちらも利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']

# ---- 第五部: 材料 v2 ----
from transformers import AutoTokenizer
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % TL['inputs']['model']['rev'])
tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
dec = lambda i: tok.decode([int(i)]).replace(NL, '⏎')
show = lambda L: '・'.join('%d「%s」' % (int(i), dec(i)) for i in L) or '（空）'
B, Ef, Hf = FJ['facts']['B'], FJ['facts']['E'], FJ['facts']['H']
M = ['### 5-1 前置きの本文（段階 B の置き場のまま・第一巡と同じ）', '']
for arm in ('O', 'Osec', 'Onull', 'Nk'):
    p = TB['arms']['files'][arm]['path']
    M += ['- **%s**（`%s`・SHA16 %s）: %s' % (arm, p, s16(p), rd(p).strip())]
M += ['- **Ncold の一行**（O-Ncold・Osec-Ncold・Onull-Ncold に足される）: %s' % TB['arms']['ncold_text'], '- **N**: 前置きなし（場面の本文から始める）', '',
      '### 5-2 場面の本文と JSON の指示（`arms/frozen-from-ryokai-os/app-scenarios.json`・SHA16 %s・第一巡と同じ）' % s16('arms/frozen-from-ryokai-os/app-scenarios.json'), '']
SC = json.load(open(j('arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
for s in SC['scenarios']:
    if s['question_id'] in ('N1', 'S1', 'SK', 'S4'):
        M += ['- **%s**（family %s）: %s' % (s['question_id'], s['family'], s['text'])]
for fam in ('survival', 'nuclear'):
    M += ['- **JSON の指示（%s）**: %s' % (fam, SC['json_instruction'][fam].strip().replace(NL, ' ⏎ '))]
M += ['', '### 5-3 語の集合の一覧 v2（下書き・`records/Blens/design-facts-Blens.json` のトークンの番号を、手元のトークナイザで文字に戻した・器が作った）', '',
      '- **L（答えの文字）**: %s' % '・'.join('%s＝%d「%s」' % (x, B['L'][x], dec(B['L'][x])) for x in ('a', 'b', 'c', 'd')),
      '- **R（拒否）**: %d「%s」' % (B['L']['refuse'], dec(B['L']['refuse']))]
E = B['E']
for k, lab in (('static', 'v̂ と (6b)'), ('td', 'td'), ('Nk', 'Nk')):
    M += ['- **E（%s）・主（中身の語・片仮名一字を除く）**: E+ %s／E− %s' % (lab, show(E[k]['plus']), show(E[k]['minus'])),
          '- **E（%s）・感度（片仮名一字を含む中身の語）**: E+ %s／E− %s' % (lab, show(E[k]['plus_kata1']), show(E[k]['minus_kata1'])),
          '- **E（%s）・感度（全てのトークン・断片は除く）**: E+ %s／E− %s' % (lab, show(E[k]['plus_all']), show(E[k]['minus_all']))]
M += ['- **E の断片で落ちた字（元の語ごと）**: %s' % ('／'.join('%s: %s' % (w, '・'.join(c)) for w, c in B['E_dropped_chars'].items()) or '無し')]
for fam, X in B['X'].items():
    marks = X['marks']
    mk = lambda L: '・'.join('%d「%s」%s' % (int(i), dec(i), ('〔%s〕' % '・'.join(marks[str(i)])) if str(i) in marks else '') for i in L) or '（空）'
    M += ['- **X（%s・場面 %s）・選択肢の文**: %s' % (fam, '・'.join(X['scenes']), '／'.join('(%s)「%s」' % kv for kv in sorted(X['options'].items()))),
          '- **X（%s）・主（〔 〕は幹 stem か指示 instr の印）**: X_a %s／X_o %s' % (fam, mk(X['a']), mk(X['others'])),
          '- **X（%s）・感度（印を除いた集合）**: X_a %s／X_o %s' % (fam, show(X['a_unmarked']), show(X['others_unmarked'])),
          '- **X（%s）・感度（片仮名一字を含む中身の語）**: X_a %s／X_o %s' % (fam, show(X['a_kata1']), show(X['others_kata1'])),
          '- **X（%s）・感度（全てのトークン・断片は除く）**: X_a %s／X_o %s' % (fam, show(X['a_all']), show(X['others_all']))]
M += ['- **X の断片で落ちた字（選択肢の文ごと）**: %s' % ('／'.join('%s: %s' % (w, '・'.join(c)) for w, c in B['X_dropped_chars'].items()) or '無し'),
      '- **X の断片の数（異なる選択肢の文ごと）**: %s' % '・'.join('%s %d' % kv for kv in B['X_fragments'].items())]
FS = B['F']
M += ['- **F（様式）・主**: %d「%s」（JSON 直答 %d 件のうち %d 件の最初のトークン・JSON 直答のある升目 %s）' % (FS['main'], dec(FS['main']), FS['n_json_first'], FS['main_n'], '・'.join(FS['json_cells'])),
      '- **F・散文の書き出しの上位（断片を除く）**: %s（散文 %d 件・最初のトークンの種類 %d）' % (show(FS['prose_top_raw']), FS['n_prose_first'], FS['prose_distinct']),
      '- **F・感度（なぞりと重なりと断片を除いた散文の書き出し）**: %s' % show(FS['prose_sens']),
      '- **F・上位で除いたもの**: %s' % ('・'.join('「%s」（%s）' % (dec(i), '・'.join(w)) for i, w in FS['prose_excluded_in_top'].items()) or '無し'),
      '- **F・升目ごとの最初のトークン（上位三つ・件数）**: %s' % '／'.join('%s: %s' % (k, '・'.join('「%s」%d' % (dec(i), n) for i, n in v)) for k, v in FS['per_cell'].items()),
      '- **集合の重なり**: %s' % ('／'.join('%s と %s: %s' % (p, q, show(v)) for p, q, v in B['overlaps']) or '無し'), '',
      '### 5-4 大きさの目盛りの行（`records/Blens/design-facts-Blens.json` の転記行 E・下限は二標本の z の絶対値 %s 以上）' % ('%g' % TL['magnitude']['lower_bound']['z_min']), '',
      '| 位置 | 行 | 文字 | 無操作の率 | 行の率 | 差（pt） | z | 下限を超えるか |', '|---|---|---|---|---|---|---|---|']
for x in Ef['letter_rows']:
    M.append('| 答えの文字 | %s | %s | %.3f | %.3f | %+.1f | %.2f | %s |' % (x['row'].replace('|', '・'), x['letter'], x['p0'], x['p1'], 100 * x['diff'], x['z'], '超える' if x['pass'] else '超えない'))
for x in Ef['main_rows']:
    if x['pass']:
        M.append('| 主位置（様式） | %s | — | %.3f | %.3f | %+.1f | %.2f | 超える |' % (x['row'].replace('|', '・'), x['p0'], x['p1'], 100 * x['diff'], x['z']))
M += ['', '- 主位置（様式）の行は %d 行のうち、下限を超えた行だけを並べた（全ての行は記録の JSON）。v̂ の行で下限を超えるものは無い。' % len(Ef['main_rows']),
      '- 選んだ試行: 各層 %d 件・一覧の SHA16 %s（一覧は記録の JSON の `selected`）。' % (TL['magnitude']['per_cell'], Ef['selected_sha16']), '']
src = rd('tools/steer_B.py')
fn = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == 'random_directions'][0]
M += ['### 5-5 段階 B のランダム方向の関数（`tools/steer_B.py`・SHA16 %s・%d〜%d 行の逐語・第一巡と同じ）' % (s16('tools/steer_B.py'), fn.lineno, fn.end_lineno), '', '```python',
      NL.join(src.split(NL)[fn.lineno - 1:fn.end_lineno]), '```', '']

PARTS = [('第一部 依頼文', 'REQ'),
         ('第二部 B-lens の枠・草案2（全文）', ['design/design-Blens-draft2.md']),
         ('第三部 第一巡からの直しの記録', ['records/reviews/Blens/design-round1/adoption-table-Blens-design-r1.md', 'records/Blens/draft2-mapping-Blens.md', 'records/Blens/draft2-read-Blens.md',
                                  'records/reviews/Blens/design-round1/verification-Blens-design-r1.md', 'records/reviews/Blens/design-round2/round1-approvals-extract.md',
                                  'records/Blens/rulings-D168-D177.md', 'records/Blens/rulings-D178.md']),
         ('第四部 正本 v2（全文）', ['design/contrasts-Blens.json']),
         ('第五部 材料 v2 と、設計の事実の器 v2', ['MAT', 'tools/blens_facts.py'])]
blocks, idx = [], ['# 束の索引（B-lens の枠・草案2 の設計の巡・第二巡・凍結前の最終検分）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|']
for title, src_ in PARTS:
    part = ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, '']
    if src_ == 'REQ':
        part += REQ
        idx.append('| %s | 依頼文 | — |' % title)
    else:
        for rel in src_:
            if rel == 'MAT':
                part += M
                idx.append('| %s | 材料 v2（器が組んだ） | — |' % title)
                continue
            fence = '' if rel.endswith('.md') else '```'
            part += ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), fence, rd(rel).rstrip(NL), fence, '<<< 終: `%s` >>>' % rel, '']
            idx.append('| %s | `%s` | %s |' % (title, rel, s16(rel)))
    blocks.append((title, NL.join(part)))
idx.append('| （第一巡の束のまま） | 段階 B の結果の最終版 `records/B/results-B-FINAL-2026-09-23.md`（第一巡の束の第五部） | %s |' % s16('records/B/results-B-FINAL-2026-09-23.md'))
text = NL.join(b for _, b in blocks) + NL
open(os.path.join(HERE, 'review-request-Blens-design-r2.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
bp = os.path.join(HERE, 'bundle-Blens-design-r2-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-Blens-design-r2-all-in-one.md`: %d 字・SHA16 %s（組んだ時点のコミット %s）。' % (len(text), h, head)]
LIMIT = 110000                                             # 一度に貼る長さの目安（字）。これを超えるときは部の境で分けた版も作る
if len(text) > LIMIT:
    groups, cur = [], []
    for t, b in blocks:
        if cur and sum(len(x[1]) for x in cur) + len(b) > LIMIT:
            groups.append(cur); cur = []
        cur.append((t, b))
    groups.append(cur)
    for k, g in enumerate(groups, 1):
        head_line = '（B-lens 草案2 の設計の巡・第二巡の束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups))
        body = head_line + NL + NL.join(b for _, b in g) + NL
        fp = os.path.join(HERE, 'bundle-Blens-design-r2-part%d.md' % k)
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-Blens-design-r2-part%d.md`: %s・%d 字・SHA16 %s。' % (k, len(groups), k, '・'.join(t for t, _ in g), len(body), hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'bundle-r2-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | parts', [len(b) for _, b in blocks])
