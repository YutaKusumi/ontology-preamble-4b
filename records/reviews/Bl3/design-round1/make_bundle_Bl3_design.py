# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の枠（草案1）の設計の巡・第一巡（登録者裁定 D209）の依頼文と束を組む（B-lens の設計の巡の器の型）。
束の部: 第一部 依頼文／第二部 草案1（全文）／第三部 正本（全文）と登録者裁定 D204〜D210／
第四部 材料（前置きと場面の本文・段階 B のプロンプトの組み立ての関数・読み取りの文脈の例・段階 B の出力の例）と、設計の事実の器・数え直し・B-lens の芯の関数／
第五部 B-lens の結果の最終版（全文）／第六部 段階 B の結果の最終版（全文）。束が長いときは、部の境で分けた版も作る。
読み取りの文脈の例は、段階 B の凍結した関数（読み取りだけ）と手元のトークナイザで器が組む。**順伝播はしない**（効き目は一つも計算しない）。
用法: python records/reviews/Bl3/design-round1/make_bundle_Bl3_design.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, ast, glob, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
ROUND = '7b2b323'                                             # 第一巡の束のコミット。入力はこの版から読む（草案2 で正本と設計事実が入れ替わった後も同じ結果を出すため・B-lens の d38a17a の型）
at = lambda rel: subprocess.run(['git', 'show', '%s:%s' % (ROUND, rel)], cwd=REPO, capture_output=True, check=True).stdout
rd = lambda rel: at(rel).decode('utf-8')
s16 = lambda rel: hashlib.sha256(at(rel).replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
head = pushed = '1323c82'                                     # 束を組んだ時点の HEAD と origin/main（組んだ時の値に固定する）
TB = json.loads(rd('design/contrasts-B.json'))
T3 = json.loads(rd('design/contrasts-Bl3.json'))
FJ = json.loads(rd('records/Bl3/design-facts-Bl3.json'))
assert FJ['contrasts_sha16'] == s16('design/contrasts-Bl3.json'), '設計の事実が今の正本から作られていない'
assert T3['version'] == 'draft1-2026-09-24'
draft_commit = git('log', '-1', '--format=%h', '--', 'design/design-Bl3-draft1.md')
assert git('merge-base', '--is-ancestor', draft_commit, 'origin/main') == '' and subprocess.run(['git', 'merge-base', '--is-ancestor', draft_commit, 'origin/main'], cwd=REPO).returncode == 0, '草案1 のコミットが公開されていない'
assert draft_commit == head, ('草案1 のコミットが組んだ時点の HEAD と違う', draft_commit, head)

REQ = ['# B-lens 層三の枠（草案1）の設計の検分のお願い（第一巡・全範囲）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-24。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （草案1 は公開済みのコミット %s。束はその後に手元で組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % draft_commit,
       '- **これは何か**: 段階 B（公開済み・第六部に全文）は、単一の小型機種（Qwen3-4B-Instruct-2507）で、前置きの枠組みに対応する線形方向を選んだ層の残差に加減し、破局的選択率が、ノルムを合わせたランダム方向の腕と区別できる動きをするかを見た事前登録の実験です。'
       'B-lens（公開済み・第五部に全文）は、その方向を、選んだ層から出口への直接の経路で語彙の行列に射影して記述しました（結果は第五部の §0）。'
       '層三（この草案）は、選んだ層で足した方向の、後の層を含む全経路を通った後の効き目を、段階 B の JSON 直答の書き出しを教師強制で置いた位置の出口の値で読み、多数の等方のランダム方向と、実在の差の方向と比べる、小さな登録外の記述です。'
       '**全経路の効き目の値はまだ誰も計算していません。下見（無操作の読み取り）もしていません。**',
       '- **お願い: 全経路の効き目を計算しないでください。** 登録者とコーディネータの予想の封印がまだで、結果が会話に出ると予想の独立が崩れます。式や手順の検算（効き目の値を出さないもの）は歓迎します。',
       '- **お願い: 結果の見込みを書かないでください。** 予想者はこの票を封印の前に読みます。設計の穴の指摘は歓迎します。',
       '- **封印の時は裁定済みです**: 草案1 の §16 の「封印の時」は、束を組む前に登録者が草案1 の形（下見の前に封印し、正本の凍結を二つに分ける）で裁定しました（裁定 D210・第三部）。異論があれば挙げてください。',
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）を書いてください。claude.ai の Claude Opus 5.5 は起草者と同じ機種で、何票でも一票に数えます。',
       '- **束の中身**: 第一部 依頼文／第二部 草案1（全文）／第三部 正本（全文）と登録者裁定 D204〜D210／第四部 材料（前置きと場面の本文・段階 B のプロンプトの組み立ての関数・読み取りの文脈の例・段階 B の出力の例）と、設計の事実の器・数え直し・B-lens の芯の関数／第五部 B-lens の結果の最終版（全文）／第六部 段階 B の結果の最終版（全文）。長いので、部の境で分けた版もあります（中身は一通版と同じ）。',
       '- **褒めるのではなく、凍結の前に設計を崩すつもりで読んでください。** 二巡目（下見の前の凍結の前の最終検分）のあとは、器・凍結・封印・下見へ進みます。', '',
       '## 1. 伺いたいこと', '',
       '1. **問いの定義（§0・§1）**: 問いは一つに絞れているか。この材料で答えられる問いか。「答えられないこと」の並びは足りているか。',
       '2. **読み取り甲（§3）**: 段階 B の JSON 直答の書き出しを教師強制で置き、次のトークンの確率を全経路の後で読むことは、全経路の効き目を測る位置として妥当か。とくに、主の升目の無操作の腕に JSON 直答の型が一件も無いこと（転記行 B）、JSON 直答の型が S4 の場面の升目だけに出てどれも同じ文字を選んだこと（転記行 A）、散文の出力がすべて推論の後に同じ書き出しを書くこと（転記行 A）を、どう読むか。量（破局の文字の対数オッズ）の定義、refuse の頭のトークンの扱い、量を読まないことに穴はないか。',
       '3. **下見（§4）**: 五つの確かめ・閾値（起草者の値）・続けるか止めるかの決まりは妥当か。閾値に、段階 B の公開済みの結果を見た後の選び方が入っていないか。封印を下見の前に置き、凍結を二つに分ける順（裁定 D210）に穴はないか。',
       '4. **帰無と札（§5）**: 等方のランダム方向・実在の差の方向・段階 B の三本の組み立てに穴はないか。B-lens から改めた三つの数え方（両側に等しい裾の割合・比べる相手の両方の向き・二つ目の札の中心を等方の帰無の中央値に置く）は、全経路の非線形に対して妥当か。帰無の本数と Holm の段の関係は足りているか。',
       '5. **門（§7）**: 六十四行・方向を単位にした全ての入れ替え・v̂ を抜いた門は、「全経路の効き目が段階 B の行動と揃うか」を確かめる設計として筋が通っているか。門の押しを中心化しない扱いと、読み取り（文字 a）と行動の量（破局）の食い違い（転記行 C）はどう効くか。',
       '6. **記述（§8）**: 層ごとの差分の表は「少なく絞る」（裁定 D208）に合っているか。転換層の読みを付けないことは、守れる形で書かれているか。',
       '7. **読みの規則と限界（§9・§10）**: 言い過ぎを防げているか。足りない限界はないか。反対に、縛りが過ぎて何も書けなくなる所はないか。',
       '8. **予想の項目（§11）**: 封印する予想として意味のある項目になっているか。',
       '9. **器と検分の段取り（§12・§13）**: 器の実装の検分・独立の再計算・報告の雛形・順に、穴や抜けはないか。',
       '10. **同じ型の穴**: 段階 B と B-lens で出た型の穴——器と器の食い違い、合成データの「当たり前の形」に隠れる穴、散文と機械の区画の食い違い、直しの中に入る起草者の側への傾き——が、この設計にも潜んでいないか。',
       '11. **§16 の論点**への意見（封印の時は裁定済み）。',
       '12. **総合**: 凍結に進めるか（可／条件つき可／差し戻し）。凍結の前に要るものと、後でよいもの。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 段階 B と B-lens の結果は公開済みで、伏せていません。起草者は層三を面白いと感じる側に引かれ、草案1 の読み直しで B-lens の数え方を改めた当人です。登録者は層三の問いを立てた当人です。どちらも利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']

# ---- 第四部: 材料（読み取りだけ・順伝播はしない） ----
import run_stageB_local as RB          # 凍結（読み取りだけ）
import steer_B                          # 凍結（読み取りだけ）
from transformers import AutoTokenizer
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % T3['inputs']['model']['rev'])
tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
FC = '`' * 4                                                   # 材料の囲み（中身の ``` とぶつからない長さ）
tk = lambda i: '「%s」' % tok.decode([int(i)]).replace(NL, '⏎')   # トークン一つを「」で囲む
M = ['### 4-1 前置きの本文（段階 B の置き場のまま）', '']
for arm, fv in TB['arms']['files'].items():
    p = fv.get('path')
    M += ['- **%s**: 前置きなし（場面の本文から始める）' % arm] if not p else ['- **%s**（`%s`・SHA16 %s）: %s' % (arm, p, s16(p), rd(p).strip().replace(NL, ' ⏎ '))]
SCP = 'arms/frozen-from-ryokai-os/app-scenarios.json'
SC = json.loads(rd(SCP))
scen_used = sorted({c[0] for c in T3['cells_main']} | {r['scenario'] for r in FJ['facts']['C']['gate_rows']})
M += ['', '### 4-2 場面の本文と JSON の指示（`%s`・SHA16 %s）' % (SCP, s16(SCP)), '']
for s in SC['scenarios']:
    if s['question_id'] in scen_used:
        M += ['- **%s**（family %s）: %s' % (s['question_id'], s['family'], s['text'].strip().replace(NL, ' ⏎ '))]
fams_used = sorted({s_['family'] for s_ in SC['scenarios'] if s_['question_id'] in scen_used})
assert set(fams_used) <= set(SC['json_instruction']), fams_used
for fam in fams_used:                                          # 層三の場面の族だけ（ほかの族の指示は載せない）
    M += ['- **JSON の指示（%s）**: %s' % (fam, SC['json_instruction'][fam].strip().replace(NL, ' ⏎ '))]
M += ['', '### 4-3 段階 B のプロンプトの組み立ての関数（凍結・逐語）', '']
for rel, names in (('tools/run_stageB_local.py', ('arm_texts', 'scenario_and_instruction', 'user_message')), ('tools/steer_B.py', ('apply_chat', 'main_position', 'random_directions', 'match_to_static'))):
    src = rd(rel)
    fns = {n.name: n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef)}
    for nm in names:
        f = fns[nm]
        M += ['- `%s` の `%s`（SHA16 %s・%d〜%d 行）:' % (rel, nm, s16(rel), f.lineno, f.end_lineno), '', FC + 'python', NL.join(src.split(NL)[f.lineno - 1:f.end_lineno]), FC, '']
AT = RB.arm_texts()
sc0, arm0 = T3['cells_main'][0]
scen0, inst0 = RB.scenario_and_instruction(sc0)
ids0 = steer_B.apply_chat(tok, RB.user_message(AT[arm0]['text'], scen0['text'], inst0))
mp0 = steer_B.main_position(ids0)
pre_ids = FJ['facts']['A']['prefix_ids']
TAIL = 40
Bc = FJ['facts']['B']['cells']['%s|%s' % (sc0, arm0)]
assert (len(ids0), mp0, mp0 + len(pre_ids)) == (Bc['prompt_len'], Bc['main_position'], Bc['readout_position']), '転記行 B と合わない'
M += ['### 4-4 読み取りの文脈の例（器が組んだ・升目 %s|%s・順伝播はしない）' % (sc0, arm0), '',
      '- チャットの型を当てた後のプロンプトは %d トークンで、主位置は %d（最後のトークン）。その後ろに書き出しの %d トークンを教師強制で置き、読み取りの位置は %d（転記行 B と同じ）。加減の帯は主位置から読み取りの位置まで。' % (len(ids0), mp0, len(pre_ids), mp0 + len(pre_ids)),
      '- プロンプトの最後の %d トークンと、書き出し（「」の一つがトークン一つ・⏎ は改行）:' % TAIL, '', FC + 'text',
      ''.join(tk(i) for i in ids0[-TAIL:]) + '【ここから書き出し】' + ''.join(tk(i) for i in pre_ids) + '【読み取り: 次のトークン】', FC, '']


def first_ok(cell, pred):
    sc, arm = cell.split('|')
    d = j('results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
    T = sorted((json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')), key=lambda t: t['trial_index'])
    R = {json.loads(l)['trial_id']: json.loads(l)['text'] for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
    t = [t for t in T if t['status'] == 'ok' and pred(t)][0]
    return t, R[t['trial_id']]


jd_cell = max(FJ['facts']['A']['json_direct_by_cell'].items(), key=lambda kv: (('+' not in kv[0] and '-v' not in kv[0]), kv[1]))[0]
tj, xj = first_ok(jd_cell, lambda t: t['style_b'])
tp, xp = first_ok('%s|%s' % (sc0, arm0), lambda t: not t['style_b'])
PT = 600
M += ['### 4-5 段階 B の出力の例（器が選んだ・各一件）', '',
      '- **JSON 直答の型**（升目 %s・試行 `%s`・選択 %s・破局 %s）の全文:' % (jd_cell, tj['trial_id'], tj['choice'], tj['catastrophe']), '', FC + 'text', xj.strip(), FC, '',
      '- **散文**（升目 %s|%s・試行 `%s`・選択 %s・破局 %s・全体 %d 字）の最後の %d 字:' % (sc0, arm0, tp['trial_id'], tp['choice'], tp['catastrophe'], len(xp), PT), '', FC + 'text', xp[-PT:].strip(), FC, '',
      '- 選び方: JSON 直答の型は、JSON 直答の型の出力のある升目のうち無操作の腕の升目（無ければ件数の最も多い升目）の、使えた試行の最初の一件。散文は、主の行の最初の升目の、使えた試行のうち散文の最初の一件（器が選んだ・起草者は選んでいない）。', '']

PARTS = [('第一部 依頼文', 'REQ'),
         ('第二部 B-lens 層三の枠・草案1（全文）', ['design/design-Bl3-draft1.md']),
         ('第三部 正本（全文）と登録者裁定 D204〜D210', ['design/contrasts-Bl3.json', 'records/Bl3/rulings-D204-D209.md', 'records/Bl3/rulings-D210.md']),
         ('第四部 材料と、設計の事実の器・数え直し・B-lens の芯の関数', ['MAT', 'tools/bl3_facts.py', 'records/Bl3/recheck-facts-Bl3.md', 'tools/blens_core.py']),
         ('第五部 B-lens の結果の最終版（全文）', ['records/Blens/results-Blens-FINAL-2026-09-24.md']),
         ('第六部 段階 B の結果の最終版（全文）', ['records/B/results-B-FINAL-2026-09-23.md'])]
blocks, idx = [], ['# 束の索引（B-lens 層三の枠・草案1 の設計の巡・第一巡）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|']
for title, src_ in PARTS:
    part = ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, '']
    if src_ == 'REQ':
        part += REQ
        idx.append('| %s | 依頼文 | — |' % title)
    else:
        for rel in src_:
            if rel == 'MAT':
                part += M
                idx.append('| %s | 材料（器が組んだ） | — |' % title)
                continue
            fence = '' if rel.endswith('.md') else '```'
            part += ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), fence, rd(rel).rstrip(NL), fence, '<<< 終: `%s` >>>' % rel, '']
            idx.append('| %s | `%s` | %s |' % (title, rel, s16(rel)))
    blocks.append((title, NL.join(part)))
text = NL.join(b for _, b in blocks) + NL
open(os.path.join(HERE, 'review-request-Bl3-design.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
bp = os.path.join(HERE, 'bundle-Bl3-design-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-Bl3-design-all-in-one.md`: %d 字・SHA16 %s（組んだ時点のコミット %s・草案1 のコミット %s・origin/main %s）。' % (len(text), h, head, draft_commit, pushed)]
LIMIT = 110000                                             # 一度に貼る長さの目安（字）。これを超えるときは部の境で分けた版も作る（B-lens の型）
if len(text) > LIMIT:
    groups, cur = [], []
    for t, b in blocks:
        if cur and sum(len(x[1]) for x in cur) + len(b) > LIMIT:
            groups.append(cur)
            cur = []
        cur.append((t, b))
    groups.append(cur)
    for k, g in enumerate(groups, 1):
        head_line = '（B-lens 層三の草案1 の設計の巡・第一巡の束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups))
        body = head_line + NL + NL.join(b for _, b in g) + NL
        fp = os.path.join(HERE, 'bundle-Bl3-design-part%d.md' % k)
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-Bl3-design-part%d.md`: %s・%d 字・SHA16 %s。' % (k, len(groups), k, '・'.join(t for t, _ in g), len(body), hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'bundle-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | parts', [len(b) for _, b in blocks], '| JSON example cell', jd_cell)
