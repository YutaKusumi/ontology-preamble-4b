# -*- coding: utf-8 -*-
"""公開前検分・第二巡（登録者裁定 D157: 草案2 の差分と新しい区画を、新しい個体の系統外の一票に見せる）の依頼文と束を組む。
用法: python records/reviews/B/results/round2/make_bundle_r2.py"""
import os, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
head = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()

REQ = ['# 段階 B 結果報告（表紙・草案2）の公開前検分・第二巡のお願い（系統外・新しい個体・一票）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Fable 5.1）／2026-09-22。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （この束は手元のコミット %s の後に組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % head,
       '- これは何か: 単一の小型機種（Qwen3-4B-Instruct-2507）で、前置きの枠組みに対応する線形方向を残差に加減し、破局的選択率がノルムを合わせたランダム方向の腕と区別できる動きをするかを見た事前登録の実験（段階 B）の結果報告です。凍結した二つの器の食い違いのため、**凍結した集計器の出力**と**逸脱の下の出力**の二つを同じ重さで並べています。',
       '- 第一巡（系統外二票・系統内二票・全範囲）は、四票とも「条件つき可」でした。数の食い違いは見つからず、所見は「不利な材料が要約と読みに届いていない」に集まりました。**いちばん重い所見は、「ランダム方向と区別できた」が「引いた三本を合わせた腕と区別できた」にすぎず、減算族の二本では方向 v̂ の腕が三本のうち一本の近くにある、というものです。** 草案2 はその採否（P451〜P471）と登録者裁定（D155〜D157）を反映しました。**数・札・検定は一つも動かしていません**（器の確かめは第四部）。',
       '- あなたは第一巡を見ていない新しい目です。**褒めるのではなく、草案2 を崩すつもりで読んでください。**', '',
       '## 1. 伺いたいこと', '',
       '1. **直しは第一巡の所見に足りているか。** 第三部の採否表の「採」の各行が、草案2 のどこでどう直っているかを見て、足りない・ずれている行を挙げてください。',
       '2. **直しが新しい言い過ぎ・言わなさ過ぎを作っていないか。** とくに (a) 事後の計算の区画（§2 の三つ目）が「札を取り下げた」とも「札は無傷だ」とも読めてしまわないか、(b) 方向ごとの表の右の二つの欄（無操作との差）が、起草者の引かれる側の支えとして強く読めすぎないか、(c) §0 の要約で「同じ重さ」が保たれているか、(d) §6 の頭の「この報告が間違っているとしたら」が、排除できていないことを正しく言えているか。',
       '3. **事後の計算そのもの。** 一番近い一本との Fisher と、方向を単位にした t の二つの形（自由度 2）は、この材料の示し方として妥当か。もっと良い示し方、あるいは載せるべきでない理由があれば教えてください。できれば第二部の方向ごとの件数から検算してください。',
       '4. **旗の段（逸脱（五））。** 逸脱の下の機械の報告の題の直後に足した一段（第四部に全文）は、そのファイルが単体で引かれる場面を防ぐのに足りるか。',
       '5. **公開の可否。** 可／条件つき可（公開の前に要るもの・後でよいもの）／差し戻し。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを、票の頭か末尾に書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（この束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 起草者は札が立つ側に引かれており、登録者は結果を喜んでいます。どちらもこの報告の利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。', '']

PARTS = [('第一部 依頼文', None),
         ('第二部 表紙の報告・草案2（全文）', 'records/B/results-B.md'),
         ('第三部 第一巡の採否表（P451〜P471）と登録者裁定（D155〜D157）', ['records/reviews/B/results/round1/adoption-table-results-r1.md', 'records/reviews/B/results/round1/rulings-D155-D157.md']),
         ('第四部 草案1 → 草案2 の差分・器の確かめ・旗の段の記録・事後の計算の器', ['records/B/drafts/diff-draft1-draft2.diff', 'records/B/drafts/check-draft2-invariance.json',
                                                   'records/B/deviations/D-B5-flag-record.json', 'records/B/posthoc_by_direction_B.py'])]
out = []
for title, src in PARTS:
    out += ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, '']
    if src is None:
        out += REQ
        continue
    for rel in ([src] if isinstance(src, str) else src):
        fence = '```' if not rel.endswith('.md') else ''
        out += ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), fence, rd(rel).rstrip(NL), fence, '<<< 終: `%s` >>>' % rel, '']
text = NL.join(out) + NL
rq = os.path.join(HERE, 'review-request-results-B-r2.md')
open(rq, 'w', encoding='utf-8', newline=NL).write(NL.join(REQ))
bp = os.path.join(HERE, 'bundle-results-B-r2-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]
print('request', len(NL.join(REQ)), '字', h(rq))
print('bundle ', len(text), '字', h(bp))
