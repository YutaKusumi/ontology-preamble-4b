# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の器についての意見伺い（登録者裁定 D230・下見の前の凍結の前・正本 `review_plan` の巡に数えない）の依頼文と束を組む（設計の巡の束の器の型）。
束の部: 第一部 依頼文／第二部 正本 v6（全文）／第三部 枠（草案3）と凍結の本文との差の記録と設計の事実／第四部 走らせる器／第五部 残差の書き換えの道とその開発の記録／
第六部 集計の器と合成データの器と試しの記録／第七部 器が呼ぶ段階 B と B-lens の凍結した関数／第八部 器の段の記録と裁定。
入力は、束の入力がそろったコミット（`SRC`）から読む。器と正本は、公開済みのコミット（`TOOLS`）と同じ中身であることを確かめる。器（.py）と正本（.json）の行の頭に、そのファイルの行番号を付ける。
束が長いときは、ファイルの境で分けた版も作る（中身は一通版と同じ）。
用法: python records/reviews/Bl3/opinions-tools/make_bundle_Bl3_opinions_tools.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
NL = chr(10)
SRC = '029d55f'                         # 束の入力がそろったコミット（裁定 D228〜D230 の記録を足したコミット）
TOOLS = '0bfc0c2'                       # 器と正本を公開したコミット
at = lambda c, rel: subprocess.run(['git', 'show', '%s:%s' % (c, rel)], cwd=REPO, capture_output=True, check=True).stdout
rd = lambda rel: at(SRC, rel).decode('utf-8')
s16 = lambda rel: hashlib.sha256(at(SRC, rel).replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
assert subprocess.run(['git', 'merge-base', '--is-ancestor', TOOLS, 'origin/main'], cwd=REPO).returncode == 0, '器のコミットが公開されていない'
T3 = json.loads(rd('design/contrasts-Bl3.json'))
FJ = json.loads(rd('records/Bl3/design-facts-Bl3.json'))
assert T3['version'] == 'draft3-r2-2026-09-25'
assert FJ['contrasts_sha16'] == s16('design/contrasts-Bl3.json'), '設計の事実が正本から作られていない'

PARTS = [
    ('第二部 正本 v6（全文）', ['design/contrasts-Bl3.json']),
    ('第三部 枠（草案3・登録者の確認済み）と、凍結の本文と草案3 の差の記録と、設計の事実', ['design/design-Bl3-draft3.md', 'records/Bl3/frozen-diff-Bl3.md', 'records/Bl3/design-facts-Bl3.md']),
    ('第四部 走らせる器（本の器のフックの道・読み取り・近道・下見・本の計算・乙・Colab の起動器）', ['tools/bl3_run.py', 'tools/bl3_core.py', 'tools/colab/boot_Bl3.py']),
    ('第五部 残差の書き換えの道（別の個体が本の器の中を見ずに書いた）とその開発の記録', ['tools/bl3_recompute_rewrite.py', 'records/Bl3/tools/recompute-rewrite-dev-Bl3.md']),
    ('第六部 集計の器と合成データの器と試しの記録', ['tools/analyze_Bl3.py', 'tools/dry_run_Bl3.py', 'records/Bl3/tools/trials/dry-trial-6-Bl3.md']),
    ('第七部 器が呼ぶ段階 B と B-lens の凍結した関数（読むだけ・変えない）', ['tools/run_stageB_local.py', 'tools/steer_B.py', 'tools/direction_B.py', 'tools/blens_core.py', 'tools/colab/boot_Blens.py']),
    ('第八部 器の段の記録と裁定', ['records/Bl3/tools/tools-log-Bl3.md', 'records/Bl3/rulings-D226-D227.md', 'records/Bl3/rulings-D228-D230.md']),
]
for _, files in PARTS:
    for rel in files:
        if rel.startswith(('tools/', 'design/contrasts')):
            assert at(SRC, rel) == at(TOOLS, rel), '器か正本が公開のコミットと違う: %s' % rel

REQ = ['# B-lens 層三の器についてのご意見のお願い（下見の前の凍結の前・意見伺い）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-25。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （器と正本は公開済みのコミット %s。束はコミット %s の中身から組みました。`prelim/` と `results/prelim-*` は開かないでください）。' % (TOOLS, SRC),
       '- **これは検分の巡ではなく、ご意見のお願いです。** 層三の設計の巡は二巡で終わり（登録者裁定 D218）、器の実装の検分は、この後に系統内の新しい個体二体が行います（裁定 D209）。その前に、登録者は、器について系統外の二名と claude.ai の二名にご意見を伺うと決めました（裁定 D230）。'
       '可否の判定は要りません。気づいたことを、確かめられる形で教えてください。',
       '- **なぜ伺うか**: 独立の再計算は、全経路の効き目の一部を二つの道で計算し直して突き合わせます。一つは本の器のフックの道（コーディネータが書いた `tools/bl3_run.py`）、もう一つは残差の書き換えの道（別の個体が、本の器の中を見ずに書いた `tools/bl3_recompute_rewrite.py`）です。'
       'どちらも Claude 系の個体が同じ正本から書いたので、片方だけの誤りは突き合わせで捕まりえますが、**正本の同じ読み違いを二つの道が共有していれば捕まりません**。また、近道・バッチの組み方・下見・札・門・乙には独立の道が無く、コーディネータが一人で書きました。'
       '凍結の後に器や正本を直すと逸脱になるので、凍結の前に外の目で見ていただきたいのです。',
       '- **お願い: 本物の模型で全経路の効き目を計算しないでください。** 予想の封印がまだです（封印は下見の前の凍結の後です）。式や手順の検算と、乱数の模型の上の確かめ（本物の重みを使わないもの）は歓迎します。',
       '- **お願い: 結果の見込み（どの行に札が付くか・門を通るかなど）を書かないでください。** 書かれていたら、封印の前の露出として記録します。',
       '- **系統**: ご意見の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）と機種を書いてください。claude.ai の Claude Opus 5.5 は起草者と同じ機種です。',
       '- **束の中身**: 第一部 依頼文／第二部 正本 v6（全文）／第三部 枠（草案3・登録者の確認済み・全文）と、凍結の本文と草案3 の差の記録と、設計の事実／第四部 走らせる器（本の器のフックの道・読み取り・近道・下見・本の計算・乙・Colab の起動器）／'
       '第五部 残差の書き換えの道とその開発の記録／第六部 集計の器と合成データの器と試しの記録／第七部 器が呼ぶ段階 B と B-lens の凍結した関数（読むだけ・変えない）／第八部 器の段の記録と裁定。'
       '器（.py）と正本（.json）の行の頭の番号は、そのファイルの行番号です。長いので、ファイルの境で分けた版もあります（中身は一通版と同じ）。',
       '- **既に分かっている点**: 器の段で見つけた点は、第八部の器の段の記録（§2・§3・§5・§7・§8）と、第五部の開発の記録にあります。同じ点に気づいたら、「記録にある点」と一言添えてください（新しい点と分けて数えます）。', '',
       '## 1. 伺いたいこと', '',
       '1. **二つの道が共有しうる読み違い**: まず第二部の正本の `readout.primary`（rule・quantity・precision・place・band・batching）・`layers`・`computation`・`independent_recompute` を、器を見る前にご自分で読んでください。'
       'そのうえで、二つの道（第四部の `Runner.forward`・`Runner.readout`・`recompute_hook_path` と、第五部の `forward_rewrite`・`readout`・`recompute_rewrite`）が同じ向きに正本から外れている所、または正本の文が二通りに読めて二つの道が同じ読みを取っている所はないか。'
       '見ていただきたい所の例（これに限りません）:',
       '   - 入力の並び（プロンプトと書き出し）・主位置・読み取りの位置',
       '   - 加える帯（どの位置に足すか）',
       '   - 足し方の算術（型の直し方の順・係数を一度だけ掛けること・符号）',
       '   - どの層の出力に足すか（層の添字と `hidden_states` の添字の対応）',
       '   - 読み取り（最終の正規化の入力・`float32`・読み取りの集合のトークン・対数オッズの定義）',
       '   - 無操作（零のベクトル）と、効き目＝加えた値 − 無操作の値',
       '   - 減算の行の符号と、比べる相手の両方の向き',
       '2. **独立の道の無い所**: 近道（主位置より前の計算の使い回し）とバッチの組み方、下見の確かめと機械の決定、札（両側に等しい裾の割合・Holm・効き目の側・二つ目の札の中心と順位・等方の最上位の割合）、門（符号を +1 にした呼び方・押しの作り方・外した升目の扱い）、乙の行——器が正本から外れている所はないか。',
       '3. **合成データの確かめの盲点**: 合成データの器（第六部）は、乱数の小さな模型で確かめます。小さな模型では足す量が大きすぎて効き目が飽和することが分かり、正本の相対の加減に合わせた記述の確かめを足しました（第六部の試しの記録の三の最後の二行）。'
       '合成の確かめをすべて通っても、本物の模型の上で結果を変えうる誤りとして、どんな形のものが残りうるか。',
       '4. **凍結の前に直すべきもの**: 凍結の後に器や正本を直すと逸脱になります。凍結の前に直すべきものと、記録（限界・報告の注）に置けば足りるものを分けてください。', '',
       '## 2. お願い', '',
       '- 一つのご意見ごとに、重さ（重い・中くらい・軽い）と、根拠の置き場（束の部とファイルと行番号、または正本の鍵）と、確かめ方を付けてください。',
       '- 問題が無いと見た所も、どこを見てそう判断したかを書いてください（問題なしの判断も記録して、次の確かめに使います）。',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。「全部読んだ」ではなく、どのファイルのどの関数を読んだかで書いてください。',
       '- 起草者（コーディネータ）は器の書き手で、「器は正本どおり」と読む側に引かれます。登録者は層三の問いを立てた当人です。どちらも利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']


def numbered(text):
    lines = text.rstrip(NL).split(NL)
    w = len(str(len(lines)))
    return NL.join('%*d | %s' % (w, i, l) for i, l in enumerate(lines, 1))


items, idx = [], ['# 束の索引（B-lens 層三の器についての意見伺い・下見の前の凍結の前・登録者裁定 D230）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|', '| 第一部 依頼文 | 依頼文 | — |']
items.append(('第一部 依頼文', 'REQ', NL.join(['', '=' * 20 + ' 第一部 依頼文 ' + '=' * 20, ''] + REQ)))
for title, files in PARTS:
    for k, rel in enumerate(files):
        head = ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, ''] if k == 0 else ['']
        body = rd(rel)
        if rel.endswith(('.py', '.json')):
            block = ['<<< 始: `%s`（SHA16 %s・行の頭の番号はこのファイルの行番号） >>>' % (rel, s16(rel)), '```', numbered(body), '```', '<<< 終: `%s` >>>' % rel]
        else:
            block = ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), body.rstrip(NL), '<<< 終: `%s` >>>' % rel]
        items.append((title, rel, NL.join(head + block)))
        idx.append('| %s | `%s` | %s |' % (title, rel, s16(rel)))
text = NL.join(b for _, _, b in items) + NL
open(os.path.join(HERE, 'request-Bl3-opinions-tools.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
bp = os.path.join(HERE, 'bundle-Bl3-opinions-tools-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-Bl3-opinions-tools-all-in-one.md`: %d 字・SHA16 %s（入力のコミット %s・器と正本のコミット %s）。' % (len(text), h, SRC, TOOLS)]
LIMIT = 110000                                             # 一度に貼る長さの目安（字）。これを超えるときはファイルの境で分けた版も作る
if len(text) > LIMIT:
    groups, cur = [], []
    for it in items:
        if cur and sum(len(x[2]) for x in cur) + len(it[2]) > LIMIT:
            groups.append(cur)
            cur = []
        cur.append(it)
    groups.append(cur)
    for k, g in enumerate(groups, 1):
        head_line = '（B-lens 層三の器についての意見伺いの束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups))
        body = head_line + NL + NL.join(b for _, _, b in g) + NL
        fp = os.path.join(HERE, 'bundle-Bl3-opinions-tools-part%d.md' % k)
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-Bl3-opinions-tools-part%d.md`: %s・%d 字・SHA16 %s。' % (
            k, len(groups), k, '・'.join(rel if rel != 'REQ' else '依頼文' for _, rel, _ in g), len(body), hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'bundle-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | items', len(items), '| parts', (len(groups) if len(text) > LIMIT else 1))
