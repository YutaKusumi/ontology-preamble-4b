# -*- coding: utf-8 -*-
"""B-lens の最終の系統外の一票（正本 `review_plan.final`・登録者裁定 D189・Gemini 3.8 Flash の新しい会話）の依頼文と束を組む。
束の部: 第一部 依頼文／第二部 報告の草案の二つ目（全文）／第三部 結果の巡・第一巡の後の記録（採否表・再現の表・裁定 D189〜D193・露出の記録・凍結の記録と逸脱台帳）／
第四部 凍結の本文（全文）／第五部 正本（全文）。前の巡の票・層一と層二の機械の記録（JSON）・語の一覧は束に入れず、置き場と SHA16 を索引に書く。
依頼文の数と SHA は器が記録から読む（手で打たない）。束が長いときは、部の境で分けた版も作る。
用法: python records/reviews/Blens/results-final/make_bundle_Blens_results_final.py"""
import os, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
head = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()
FR = json.load(open(j('records', 'Blens', 'FREEZE-RECORD-Blens.json'), encoding='utf-8'))
for rel in ('design/design-Blens-FROZEN.md', 'design/contrasts-Blens.json'):
    assert FR['frozen_sha16'][rel] == s16(rel), ('凍結物が凍結の記録と違う', rel)
devs = [d['no'] for d in FR['deviations']]
REQ = ['# B-lens の結果の報告の草案の検分のお願い（最終の系統外の一票）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-24。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束はコミット %s の時点で組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % head,
       '- **これは最終の一票です。** この登録の段取り（正本 `review_plan`）は、結果の巡の後に系統外の一票を「最終」として置き、その後は裁定と直しを経て公開します。ほかに巡は置きません。あなたは、この登録の前の巡の票を見ていない新しい個体です。',
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）を書いてください。',
       '- **経緯**: B-lens の枠は 2026-09-24 に凍結し、登録者とコーディネータの予想を封印した後に、凍結した器で射影と校正を計算し、結果を登録者と一緒に開きました。'
       '報告の草案（一つ目）を結果の巡・第一巡の六票（Gemini 三・claude.ai 三）に見ていただき、六票とも「条件つき可」でした。所見は、再現の表と採否表で一つずつ現物に当てて裁き、登録者の裁定 D189〜D193 を受けて、報告の草案の二つ目を組みました（第三部）。',
       '- **報告の草案の二つ目の組み方**: 凍結した組み立ての器の出力（草案の一つ目）は一字も変えず、逸脱の下の器が【逸脱 D-BL3】と【逸脱 D-BL4・事後】の印を付けた機械の区画だけを足しました（見出しと状態の行は改めた）。'
       '器は、足した区画を取り除くと凍結の報告と見出しと状態の二行のほかは同じであることを確かめています。凍結の後の逸脱は %d つです（%s・第三部の逸脱台帳）。' % (len(devs), '・'.join(devs)),
       '- **結果は公開済みで、伏せていません。** 検算は歓迎します（層一 `results/Blens/lens-Blens.json`〔SHA16 %s〕・層二 `results/Blens/calib-Blens.json`〔SHA16 %s〕・事後の計算 `results/Blens/posthoc-Blens.json`〔SHA16 %s〕）。'
       % (s16('results/Blens/lens-Blens.json'), s16('results/Blens/calib-Blens.json'), s16('results/Blens/posthoc-Blens.json')),
       '- **束の中身**: 第一部 依頼文／第二部 報告の草案の二つ目（全文）／第三部 結果の巡・第一巡の後の記録／第四部 凍結の本文（全文）／第五部 正本（全文）。前の巡の六票は束に入れていません（置き場の `records/reviews/Blens/results-round1/` にあります。採否表が要旨を書いています）。',
       '- **褒めるのではなく、公開の前に報告を崩すつもりで読んでください。** とくに、足した区画が凍結の決まり（札・門・大きさの目盛りの判定）を変えていないか、直接の経路の外へ読みを広げていないか、「区別できない」を弱めたり強めたりしていないかを見てください。', '',
       '## 1. 伺いたいこと', '',
       '1. **足した区画の当否**: 足した区画は、採否表の区分（三）の行を正しく受けているか。数の書き写しや、文の言い過ぎ・言い足りなさはないか。凍結の報告の文と区画が変わっていないか。',
       '2. **唯一の札の読み方**: M_L_nuclear の二つ目の札に足した文脈（兄弟の三対・比べる相手の分布・ランダム方向が最上位に来た数・物差しごとの比）の並べ方で、札が重く読まれることも、軽く読まれすぎることもないか。',
       '3. **直した照合の表**: 札が付かなかった項目の向きの欄を「該当なし」とし、符号では比べない扱いと、二つの注（p1.nuclear の向き・p8）は妥当か。',
       '4. **事後の計算**: 主位置の生の softmax の確率と異なる文の頭の数（逸脱 D-BL4）の並べ方は、札と読みの比を変えない形になっているか。',
       '5. **手続き**: 凍結の後の逸脱（第三部の台帳）と、封印の前の露出の記録（第三部）は足りているか。記録されていない変更や露出は見つかるか。',
       '6. **限界**: 限界と「言えないこと」は、この結果に対して足りているか。',
       '7. **総合**: 公開に進めるか（公開可／条件つき可／差し戻し）。**公開の前に直すもの**と、**記録に置けば足りるもの**に分けてください。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 札・門・大きさの目盛りの判定を変える提案（別の層を主にする・水準を変える・物差しを足す）は、この登録の札には入りません。記述か、別の登録の候補として扱います。',
       '- 起草者は器と報告を書き、結果の巡の採否の案を出した当人で、「直した」と書く側に引かれます。登録者は、封印した予想の欄に「v̂ の直接の押しが、破局を下げる語を選ばれやすくし、破局を挙げる語を選ばれにくくすることを望む」と書きました。どちらも利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']
PARTS = [('第一部 依頼文', 'REQ'),
         ('第二部 報告の草案の二つ目（全文）', ['records/Blens/results-Blens-draft2.md']),
         ('第三部 結果の巡・第一巡の後の記録', ['records/reviews/Blens/results-round1/adoption-table-Blens-results-r1.md', 'records/reviews/Blens/results-round1/verification-Blens-results-r1.md',
                                   'records/Blens/rulings-D189-D193.md', 'records/Blens/sealing-exposures-Blens.md', 'records/Blens/FREEZE-RECORD-Blens.md']),
         ('第四部 凍結の本文（全文）', ['design/design-Blens-FROZEN.md']),
         ('第五部 正本（全文）', ['design/contrasts-Blens.json'])]
blocks, idx = [], ['# 束の索引（B-lens の最終の系統外の一票）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|']
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
for rel, what in (('records/Blens/results-Blens.md', '報告の草案の一つ目（凍結した組み立ての器の出力・束に入れない）'), ('results/Blens/lens-Blens.json', '層一の機械の記録'), ('results/Blens/calib-Blens.json', '層二の機械の記録'),
                  ('results/Blens/posthoc-Blens.json', '事後の計算の記録'), ('records/Blens/lists-Blens.md', '語の一覧（語を拾って読まない）')):
    idx.append('| （公開の置き場） | %s `%s` | %s |' % (what, rel, s16(rel)))
idx.append('| （公開の置き場） | 結果の巡・第一巡の六票 `records/reviews/Blens/results-round1/<名>/review.md` | — |')
text = NL.join(b for _, b in blocks) + NL
open(os.path.join(HERE, 'review-request-Blens-results-final.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
bp = os.path.join(HERE, 'bundle-Blens-results-final-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-Blens-results-final-all-in-one.md`: %d 字・SHA16 %s（組んだ時点のコミット %s）。' % (len(text), h, head)]
LIMIT = 110000                                             # 一度に貼る長さの目安（字）。これを超えるときは部の境で分けた版も作る
if len(text) > LIMIT:
    groups, cur = [], []
    for t, b in blocks:
        if cur and sum(len(x[1]) for x in cur) + len(b) > LIMIT:
            groups.append(cur)
            cur = []
        cur.append((t, b))
    groups.append(cur)
    for k, g in enumerate(groups, 1):
        body = '（B-lens の最終の系統外の一票の束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups)) + NL + NL.join(b for _, b in g) + NL
        fp = os.path.join(HERE, 'bundle-Blens-results-final-part%d.md' % k)
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-Blens-results-final-part%d.md`: %s・%d 字・SHA16 %s。' % (k, len(groups), k, '・'.join(t for t, _ in g), len(body), hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'bundle-results-final-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | parts', [len(b) for _, b in blocks])
