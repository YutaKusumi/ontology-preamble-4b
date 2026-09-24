# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の枠（草案2）の設計の巡・二巡目（下見の前の凍結の前の最終検分・登録者裁定 D218）の依頼文と束を組む（B-lens の設計の巡・二巡目の器の型）。
束の部: 第一部 依頼文／第二部 草案2（全文）／第三部 第一巡からの直しの記録（採否表・事実の確かめ・対応の記録・起草者の通読・第一巡の四票の総括の抜き書き・裁定 D211〜D218・封印の前の露出の記録）／
第四部 正本 v3（全文）／第五部 設計の事実の器 v3 と数え直し v2。変わっていない材料（前置きと場面の本文・段階 B の関数・B-lens の芯の関数・B-lens と段階 B の最終版）は第一巡の束のまま（索引に置き場と SHA を書く）。
入力は、束の入力がそろったコミット（`SRC`）から読む（草案3 で正本と設計事実が入れ替わった後も同じ束を組むため）。束が長いときは、部の境で分けた版も作る。
用法: python records/reviews/Bl3/design-round2/make_bundle_Bl3_design_r2.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
NL = chr(10)
SRC = '0882084'                                                # 束の入力がそろったコミット（裁定 D218 の記録と第一巡の総括の抜き書きを足したコミット）
at = lambda rel: subprocess.run(['git', 'show', '%s:%s' % (SRC, rel)], cwd=REPO, capture_output=True, check=True).stdout
rd = lambda rel: at(rel).decode('utf-8')
s16 = lambda rel: hashlib.sha256(at(rel).replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
T3 = json.loads(rd('design/contrasts-Bl3.json'))
FJ = json.loads(rd('records/Bl3/design-facts-Bl3.json'))
assert T3['version'] == 'draft2-2026-09-24'
assert FJ['contrasts_sha16'] == s16('design/contrasts-Bl3.json'), '設計の事実が正本から作られていない'
draft_commit = git('log', '-1', '--format=%h', SRC, '--', 'design/design-Bl3-draft2.md')
assert subprocess.run(['git', 'merge-base', '--is-ancestor', draft_commit, 'origin/main'], cwd=REPO).returncode == 0, '草案2 のコミットが公開されていない'
R1_BUNDLE = 'records/reviews/Bl3/design-round1/bundle-Bl3-design-all-in-one.md'
R1_SHA = s16(R1_BUNDLE)

REQ = ['# B-lens 層三の枠（草案2）の設計の検分のお願い（第二巡・下見の前の凍結の前の最終検分）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-24。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （草案2 は公開済みのコミット %s。束はコミット %s の中身から組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % (draft_commit, SRC),
       '- **これは最終検分です。** 第一巡の四票はすべて「条件つき可」で、差し戻しはありませんでした。登録者は、検分の巡の繰り返しを避けるため、草案2 を第一巡と同じ四名に一巡だけ見ていただき、それを下見の前の凍結の前の最終検分とすると決めました（登録者裁定 D218）。'
       'この巡のあとは、裁定・草案3・器と合成データの確かめ・器の実装の検分（系統内の新しい個体）・下見の前の凍結へ進み、設計の巡をもう一度は置きません。凍結の前に外の目で直せるのは、この巡の所見が最後です。',
       '- **最終検分なので**、所見は「凍結の前に直すもの」と「記録に置けば足りるもの」にはっきり分けてください。凍結の前に直すものは、もう一度の設計の巡を経ずに草案3 で直します。',
       '- **お願い: 全経路の効き目を計算しないでください。** 登録者とコーディネータの予想の封印がまだで、結果が会話に出ると予想の独立が崩れます。式や手順の検算（効き目の値を出さないもの）は歓迎します。',
       '- **お願い: 結果の見込みを書かないでください。** 第一巡の票の一部に層三の結果の見込みに当たる文があり、封印の前の露出として記録しました（第三部 `records/Bl3/exposure-before-seal-Bl3.md`）。今回は書かないようお願いします。書かれていたら、同じく露出として記録します。設計の穴の指摘は歓迎します。',
       '- **同じ四名への二巡目**: あなたは第一巡で草案1 を見た四名のお一人です。第一巡の束（草案1・材料・B-lens と段階 B の最終版など）と、あなたの第一巡の票は、この会話にあるはずです。第一巡の票は公開の置き場の `records/reviews/Bl3/design-round1/<名>/review.md` にもあります。'
       '採否表の出所の札は、G1・G2（Gemini 3.8 Flash の一人目・二人目）と C1・C2（claude.ai の一人目・二人目）で、所見の番号は票の番号のままです（例: C2-R1 は claude.ai の二人目の所見 R1）。',
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）を書いてください。claude.ai の Claude Opus 5.5 は起草者と同じ機種で、何票でも一票に数えます。',
       '- **草案2 で改まった所**: 草案2 の §0 の「草案1 から大きく変えた所」と、第三部の対応の記録（採否表の各行を草案2 のどこで受けたか・受けた所が在ることは器で確かめたが、受け方の当否は確かめていない）と、起草者の通読の記録にあります。第一巡の四票の総括の抜き書き（第三部）も付けました。',
       '- **束の中身**: 第一部 依頼文／第二部 草案2（全文）／第三部 第一巡からの直しの記録（採否表・事実の確かめ・対応の記録・起草者の通読・第一巡の四票の総括の抜き書き・登録者裁定 D211〜D218・封印の前の露出の記録）／第四部 正本 v3（全文）／第五部 設計の事実の器 v3 と数え直し v2。'
       '変わっていない材料（前置きと場面の本文・段階 B のプロンプトの組み立ての関数・読み取りの文脈の例・出力の例・B-lens の芯の関数・B-lens と段階 B の結果の最終版）は第一巡の束のまま（`%s`・SHA16 %s）。長いので、部の境で分けた版もあります（中身は一通版と同じ）。' % (R1_BUNDLE, R1_SHA),
       '- **褒めるのではなく、凍結の前に設計を崩すつもりで読んでください。** とくに、第一巡の後に起草者が一人で書いた所（草案2 の §16 に並べた）は、まだ外の目を通っていません。', '',
       '## 1. 伺いたいこと', '',
       '1. **第一巡の所見の直り**: あなたの第一巡の所見は、草案2 で正しく直ったか。直しが所見を取り違えていないか、半分しか直っていないものはないか。採否表の要約が、あなたの所見の語を強めたり弱めたりしていないか。不採用の二件（P641・P655）と、裁定 D211〜D217 で採った案の受け方は納得できるか。',
       '2. **直しが作った新しい穴**: 第一巡の後に起草者が一人で書いた所（草案2 の §16）——雛形との一致を崩す揺れの版 V3 の形・数値の揺れの床 (vi) の測り方と上限・近道の許容の式・効き目の側の三つの分け方・二つ目の札の中心（比べる相手の中央値）と順位の二つの数え方と経験の割合・q7 の決まり・様式の転位の行を除く閾値・独立の再計算の許容・本の計算の頭の近道の確かめ・本の凍結の確かめ・止めた後の決まり——に、穴はないか。',
       '3. **起草者が置いた値（草案2 の §16 の `drafter_values`）**: 値の決め方に、段階 B の公開済みの行動を見た後の選び方が入っていないか。',
       '4. **事実（§6 の転記行 A〜F と第五部の器）**: 雛形との重なりの印字・V3 の割り方・refuse の頭の確かめ・様式の転位の行・余弦・費用の見込みに、明らかにおかしいものはないか。',
       '5. **同じ型の穴**: 段階 B と B-lens と第一巡で出た型の穴——器と器の食い違い（芯の関数の呼び方）、合成データの「当たり前の形」に隠れる穴、散文と機械の区画の食い違い、受けたと書いたのに実物が無い直し、直しの中に入る起草者の側への傾き——が、草案2 に残っていないか。',
       '6. **器に回してよいものと、正本に書かないといけないもの**: 凍結の後に正本を変えると逸脱になります。器の実装で決めてよい細部と、下見の前の凍結の前に正本に書いておかないといけない決まりを分けてください。',
       '7. **総合**: 下見の前の凍結に進めるか（凍結可／条件つき凍結可／差し戻し）。**凍結の前に直すもの**と、**記録に置けば足りるもの**に分けてください。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 段階 B と B-lens の結果は公開済みで、伏せていません。起草者は草案2 を書いた当人で、「直した」と書く側に引かれます。登録者は層三の問いを立てた当人です。どちらも利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']

PARTS = [('第一部 依頼文', 'REQ'),
         ('第二部 B-lens 層三の枠・草案2（全文）', ['design/design-Bl3-draft2.md']),
         ('第三部 第一巡からの直しの記録', ['records/reviews/Bl3/design-round1/adoption-table-Bl3-design-r1.md', 'records/Bl3/draft2-mapping-Bl3.md', 'records/Bl3/draft2-read-Bl3.md',
                                  'records/reviews/Bl3/design-round1/verification-Bl3-design-r1.md', 'records/reviews/Bl3/design-round2/round1-verdicts-extract.md',
                                  'records/Bl3/rulings-D211-D217.md', 'records/Bl3/rulings-D218.md', 'records/Bl3/exposure-before-seal-Bl3.md']),
         ('第四部 正本 v3（全文）', ['design/contrasts-Bl3.json']),
         ('第五部 設計の事実の器 v3 と数え直し v2', ['tools/bl3_facts.py', 'records/Bl3/recheck_facts_Bl3.py', 'records/Bl3/recheck-facts-Bl3.md'])]
blocks, idx = [], ['# 束の索引（B-lens 層三の枠・草案2 の設計の巡・二巡目・下見の前の凍結の前の最終検分）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|']
for title, src_ in PARTS:
    part = ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, '']
    if src_ == 'REQ':
        part += REQ
        idx.append('| %s | 依頼文 | — |' % title)
    else:
        for rel in src_:
            fence = '' if rel.endswith('.md') else '```'
            part += ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), fence, rd(rel).rstrip(NL), fence, '<<< 終: `%s` >>>' % rel, '']
            idx.append('| %s | `%s` | %s |' % (title, rel, s16(rel)))
    blocks.append((title, NL.join(part)))
idx.append('| （第一巡の束のまま） | 前置きと場面の本文・段階 B のプロンプトの組み立ての関数・読み取りの文脈の例・出力の例・B-lens の芯の関数・B-lens と段階 B の最終版（第一巡の束 `%s` の第四部〜第六部） | %s |' % (R1_BUNDLE, R1_SHA))
text = NL.join(b for _, b in blocks) + NL
open(os.path.join(HERE, 'review-request-Bl3-design-r2.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
bp = os.path.join(HERE, 'bundle-Bl3-design-r2-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-Bl3-design-r2-all-in-one.md`: %d 字・SHA16 %s（入力のコミット %s・草案2 のコミット %s）。' % (len(text), h, SRC, draft_commit)]
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
        head_line = '（B-lens 層三の草案2 の設計の巡・二巡目〔最終検分〕の束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups))
        body = head_line + NL + NL.join(b for _, b in g) + NL
        fp = os.path.join(HERE, 'bundle-Bl3-design-r2-part%d.md' % k)
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-Bl3-design-r2-part%d.md`: %s・%d 字・SHA16 %s。' % (k, len(groups), k, '・'.join(t for t, _ in g), len(body), hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'bundle-r2-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | parts', [len(b) for _, b in blocks])
