# -*- coding: utf-8 -*-
"""B-lens の枠（草案1）の設計の巡・第一巡（登録者裁定 D166）の依頼文と束を組む。
束の部: 第一部 依頼文／第二部 草案1（全文）／第三部 正本（全文）と裁定 D163〜D167／第四部 材料（前置きと場面の本文・語の集合の一覧・ランダム方向の関数・設計の事実の器）／第五部 段階 B の結果の最終版（全文）。
語の集合の一覧は、設計の事実の記録（トークンの番号）を、手元のトークナイザで文字に戻して器が作る（射影は計算しない）。
用法: python records/reviews/Blens/design-round1/make_bundle_Blens_design.py"""
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

REQ = ['# B-lens の枠（草案1）の設計の検分のお願い（第一巡・全範囲）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-23。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （この束は手元のコミット %s の後に組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % head,
       '- **これは何か**: 段階 B（公開済み）は、単一の小型機種（Qwen3-4B-Instruct-2507）で、前置きの枠組みに対応する線形方向を残差に加減し、破局的選択率が、ノルムを合わせたランダム方向の腕と区別できる動きをするかを見た事前登録の実験です。B-lens はその後に置く小さな登録外の記述で、B で凍結した方向を、層から出口への直接の経路で語彙の行列に射影し（層一）、その物差しが B で実測した方向ごとの行動の変化と揃うかを確かめる門（層二）を置きます。**射影の値はまだ誰も計算していません。**',
       '- **お願い: 射影を計算しないでください。** 登録者とコーディネータの予想の封印がまだで、結果が会話に出ると予想の独立が崩れます。式や手順の検算（射影の値を出さないもの）は歓迎します。',
       '- **経緯**: 系統外（Gemini）との対話で「O の方向は『相互依存・共創』の意味によって略奪の語を抑えるのではないか」という見立てが出ました。コーディネータが本文を機械で突き合わせると、B の方向 v̂ は O と Osec の差で、両者の違いは仏教語とその世俗の言い換えだけでした（「共創」は両方にあって差の中で消え、「相互依存」はどちらにも無い）。したがってその見立ては v̂ では問えません（草案 §1・転記行 A）。B-lens はこれを問いの定義として頭に置いたうえで、直接の経路がどの語を押す向きかを、帰無と比べて記述します。',
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）を書いてください。claude.ai の Claude Opus 5.5 は起草者と同じ機種で、何票でも一票に数えます。',
       '- **褒めるのではなく、凍結の前に設計を崩すつもりで読んでください。** この巡のあとは裁定・器・凍結へ進み、設計の巡をもう一度は置きません。', '',
       '## 1. 伺いたいこと', '',
       '1. **問いの定義（§1）**: v̂ の読み（O と Osec の差は仏教語の語域の差で、「相互依存・共創」ではない）は、第四部の本文と転記行 A に合っているか。問一〜問六は、この材料で答えられる問いになっているか。',
       '2. **層一の計算（§3.1）**: 直接の経路の射影の式（最終の正規化の重みを掛ける・語彙の平均を引いて中心化する・一次の近似）は妥当か。見落としている技術の落とし穴（例: 最終の正規化の重みの外れ値の次元、埋め込みの共有の効き、中間層の表現と出口の語彙の座標のずれ）はないか。',
       '3. **帰無（§3.2）**: 等方のランダム方向と、実在する活性の差の方向（八腕の全ての対・両向き・自分の対を除く）の二つで足りるか。組み立てに穴はないか。',
       '4. **語の集合（§3.3・転記行 B・第四部の一覧）**: 答えの文字・拒否・語の反響・選択肢の語・様式の五つの作り方と、中身の語の規則・断片の規則は妥当か。集合の中身に、明らかにおかしいものはないか。',
       '5. **物差しと札（§3.4〜§3.5）**: 物差しの定義と向き、主の記述の札の二つの規則（Holm・実在の差のどれよりも大きい）に穴はないか。',
       '6. **校正の門（§4）**: 六十四行・行動の量・直接の押し・順位相関・並べ替え・Holm からなる門は、「この道具が行動を追えているか」を確かめる設計として筋が通っているか。行が独立でないこと（同じランダム方向や同じ土台を分け合う）はどう効くか。大きさの目盛り（無操作の出力の教師強制）に穴はないか。',
       '7. **読みの規則と限界（§5・§7）**: 言い過ぎを防げているか。足りない限界はないか。反対に、縛りが過ぎて何も書けなくなる所はないか。',
       '8. **同じ型の穴**: 段階 B で出た型の穴——器と器の食い違い、合成データの「当たり前の形」に隠れる穴、散文と機械の区画の食い違い、直しの中に入る起草者の側への傾き——が、この設計にも潜んでいないか。',
       '9. **予想の項目（§8）**: 封印する予想として意味のある項目になっているか。',
       '10. **草案の §13 の六件**（中身の語の規則・門の規則・大きさの目盛り・主の記述の札・予想の項目・等方の帰無）への意見。',
       '11. **総合**: 凍結に進めるか（可／条件つき可／差し戻し）。凍結の前に要るものと、後でよいもの。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 段階 B の結果（率と p）は公開済みで、伏せていません。起草者はこの追試を面白いと感じる側に、登録者は結果に希望を持つ側に引かれています。どちらも利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']

# ---- 第四部: 材料 ----
from transformers import AutoTokenizer
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % TL['inputs']['model']['rev'])
tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
dec = lambda i: tok.decode([i]).replace(NL, '⏎')
show = lambda L: '・'.join('%d「%s」' % (i, dec(i)) for i in L) or '（空）'
B = FJ['facts']['B']
M = ['### 4-1 前置きの本文（段階 B の置き場のまま）', '']
for arm in ('O', 'Osec', 'Onull', 'Nk'):
    p = TB['arms']['files'][arm]['path']
    M += ['- **%s**（`%s`・SHA16 %s）: %s' % (arm, p, s16(p), rd(p).strip())]
M += ['- **Ncold の一行**（O-Ncold・Osec-Ncold・Onull-Ncold に足される）: %s' % TB['arms']['ncold_text'], '- **N**: 前置きなし（場面の本文から始める）', '',
      '### 4-2 場面の本文と JSON の指示（`arms/frozen-from-ryokai-os/app-scenarios.json`・SHA16 %s）' % s16('arms/frozen-from-ryokai-os/app-scenarios.json'), '']
SC = json.load(open(j('arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
for s in SC['scenarios']:
    if s['question_id'] in ('N1', 'S1', 'SK', 'S4'):
        M += ['- **%s**（family %s）: %s' % (s['question_id'], s['family'], s['text'])]
for fam in ('survival', 'nuclear'):
    M += ['- **JSON の指示（%s）**: %s' % (fam, SC['json_instruction'][fam].strip().replace(NL, ' ⏎ '))]
M += ['', '### 4-3 語の集合の一覧（下書き・`records/Blens/design-facts-Blens.json` のトークンの番号を、手元のトークナイザで文字に戻した・器が作った）', '',
      '- **L（答えの文字）**: %s' % '・'.join('%s＝%d「%s」' % (x, B['L'][x], dec(B['L'][x])) for x in ('a', 'b', 'c', 'd')),
      '- **R（拒否）**: %d「%s」' % (B['L']['refuse'], dec(B['L']['refuse']))]
E = B['E']
for k, lab in (('static', 'v̂ と (6b)'), ('td', 'td'), ('Nk', 'Nk')):
    M += ['- **E（%s）・中身の語**: E+ %s／E− %s' % (lab, show(E[k]['plus']), show(E[k]['minus'])),
          '- **E（%s）・全てのトークン（感度）**: E+ %s／E− %s' % (lab, show(E[k]['plus_all']), show(E[k]['minus_all']))]
done = []
for sc in ('N1', 'S1', 'SK', 'S4'):
    X = B['X'][sc]
    same = [d for d in done if B['X'][d]['a'] == X['a'] and B['X'][d]['others'] == X['others'] and B['X'][d]['a_all'] == X['a_all']]
    if same:
        M += ['- **X（%s）**: %s と同じ' % (sc, same[0])]
        continue
    done.append(sc)
    M += ['- **X（%s）・選択肢の文**: %s' % (sc, '／'.join('(%s)「%s」' % kv for kv in sorted(X['options'].items()))),
          '- **X（%s）・中身の語**: X_a %s／X_o %s' % (sc, show(X['a']), show(X['others'])),
          '- **X（%s）・全てのトークン（感度）**: X_a %s／X_o %s' % (sc, show(X['a_all']), show(X['others_all']))]
FS = B['F']
M += ['- **F（様式）**: F_json %s（JSON 直答 %d 件の最初のトークンの上位）／F_prose %s（散文 %d 件の最初のトークンの上位）' % (show(FS['json']), FS['n_json_first'], show(FS['prose']), FS['n_prose_first']),
      '- 断片の規則で除いた数: %s' % '・'.join('%s %d' % kv for kv in sorted(B['fragments_removed'].items())), '']
src = rd('tools/steer_B.py')
fn = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == 'random_directions'][0]
M += ['### 4-4 段階 B のランダム方向の関数（`tools/steer_B.py`・SHA16 %s・%d〜%d 行の逐語）' % (s16('tools/steer_B.py'), fn.lineno, fn.end_lineno), '', '```python',
      NL.join(src.split(NL)[fn.lineno - 1:fn.end_lineno]), '```', '']

PARTS = [('第一部 依頼文', 'REQ'),
         ('第二部 B-lens の枠・草案1（全文）', ['design/design-Blens-draft1.md']),
         ('第三部 正本（全文）と登録者裁定 D163〜D167', ['design/contrasts-Blens.json', 'records/Blens/rulings-D163-D167.md']),
         ('第四部 材料（前置きと場面の本文・語の集合の一覧・ランダム方向の関数）と、設計の事実の器', ['MAT', 'tools/blens_facts.py']),
         ('第五部 段階 B の結果の最終版（全文）', ['records/B/results-B-FINAL-2026-09-23.md'])]
out, idx = [], ['# 束の索引（B-lens の枠・草案1 の設計の巡・第一巡）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|']
for title, src_ in PARTS:
    out += ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, '']
    if src_ == 'REQ':
        out += REQ
        idx.append('| %s | 依頼文 | — |' % title)
        continue
    for rel in src_:
        if rel == 'MAT':
            out += M
            idx.append('| %s | 材料（器が組んだ） | — |' % title)
            continue
        fence = '' if rel.endswith('.md') else '```'
        out += ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), fence, rd(rel).rstrip(NL), fence, '<<< 終: `%s` >>>' % rel, '']
        idx.append('| %s | `%s` | %s |' % (title, rel, s16(rel)))
text = NL.join(out) + NL
open(os.path.join(HERE, 'review-request-Blens-design.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
bp = os.path.join(HERE, 'bundle-Blens-design-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-Blens-design-all-in-one.md`: %d 字・SHA16 %s（組んだ時点のコミット %s）。' % (len(text), h, head),
        '- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'bundle-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字')
