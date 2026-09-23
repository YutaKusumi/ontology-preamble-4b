# -*- coding: utf-8 -*-
"""公開前検分・第三巡（最終・登録者裁定 D160）の依頼文と束を組む。用法: python records/reviews/B/results/round3/make_bundle_r3.py"""
import os, hashlib, subprocess, difflib, json

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p); NL = chr(10)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
head = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.strip()
d2, d3 = rd('records/B/drafts/results-B-draft2.md').split(NL), rd('records/B/results-B.md').split(NL)
diff = NL.join(difflib.unified_diff(d2, d3, 'results-B-draft2.md', 'results-B.md（草案3）', lineterm='', n=1)) + NL
open(j('records', 'B', 'drafts', 'diff-draft2-draft3.diff'), 'w', encoding='utf-8', newline=NL).write(diff)
FR = json.load(open(j('records', 'B', 'deviations', 'flag-record-B-2026-09-23.json'), encoding='utf-8'))
flags = NL.join('### %s（`%s`）%s%s%s%s' % (k, v['file'], NL, NL, v['flag_line'], NL) for k, v in FR['reports'].items())

REQ = ['# 段階 B 結果報告（表紙・草案3）の公開前検分・**最終**の巡のお願い（系統外・新しい個体・一票）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Fable 5.1）／2026-09-23。',
       '- **これは最終の検分です。** 登録者の裁定（D160）により、この巡の採否を反映した後は、登録者の確認を経て公開します。直しが文の範囲を超える指摘（数・札・区画の作りが動く）が出た場合だけ、公開を止めて登録者が判断します。この巡の後に別の巡は置きません（検分の繰り返しを避けるため）。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （この束は手元のコミット %s の後に組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % head,
       '- これは何か: 単一の小型機種（Qwen3-4B-Instruct-2507）で、前置きの枠組みに対応する線形方向を残差に加減し、破局的選択率がノルムを合わせたランダム方向の腕と区別できる動きをするかを見た事前登録の実験（段階 B）の結果報告です。凍結した二つの器の食い違いのため、**凍結した集計器の出力**と**逸脱の下の出力**を同じ重さで並べています。',
       '- 経緯: 第一巡（全範囲・四票）は「不利な材料が要約と読みに届いていない」を見つけ、草案2 で直しました。第二巡（四票）は、**その直しの中に起草者の側へ傾いた言い分けが入っていた**ことを見つけました——「減算族は一本の近く／加算族は三本の外」という書き分けは不正確（札が立った七本はすべて三本の範囲の外・違いは距離だけ）、事前登録の二本を方向ごとの検分から免れさせていた、無操作との差の欄の並置、検出力の弁明。草案3 はその採否（P472〜P487）と裁定（D158〜D160）を反映しました。**数・札・検定は草案1 から一つも動いていません**（器の確かめは第四部）。',
       '- あなたは前の巡を見ていない新しい目です。褒めるのではなく、草案3 を崩すつもりで読んでください。二巡とも直しの中に新しい傾きが入りました。三度目が無いかを、とくに見てください。', '',
       '## 1. 伺いたいこと', '',
       '1. **直しは第二巡の所見に足りているか。** 第三部の採否表の「採」の各行が、草案3 のどこでどう直っているかを見て、足りない・ずれている行を挙げてください。',
       '2. **直しがまた起草者の側に傾いていないか。** とくに (a) §0 と §4 の「同じ物差し」の文が、「範囲の外」を強調して札を守っていないか、(b) §2 の方向ごとの表の新しい欄（一本ずつ − 無操作）と散文が、表の見え方と噛み合っているか、(c) §2 の事後の区画の作り替え（順位の下限を頭に・下限つきの形の一列）が、「札は無傷」とも「札は取り下げ」とも読めないか、(d) §6 の頭の五つと結びの二本立てが、排除できていないことを正しく言えているか。',
       '3. **旗の段（第四部・二本）。** 内訳は走査器の決まりで漢数字です。単体で引かれる場面を防ぐのに足りるか。凍結側の旗が、逆に凍結側の出力を軽く見せていないか。',
       '4. **公開の可否。** 可／条件つき可（公開の前に要るもの・後でよいもの）／差し戻し。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。所見には重さ（重大・中・軽）と根拠の置き場を付けてください。',
       '- 起草者は札が立つ側に引かれており、登録者は結果を喜んでいます。どちらもこの報告の利害の当事者です。', '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。', '']
PARTS = [('第一部 依頼文', None),
         ('第二部 表紙の報告・草案3（全文）', 'records/B/results-B.md'),
         ('第三部 第二巡の採否表（P472〜P487）と登録者裁定（D158〜D160）', ['records/reviews/B/results/round2/adoption-table-results-r2.md', 'records/reviews/B/results/round2/rulings-D158-D160.md']),
         ('第四部 草案2 → 草案3 の差分・器の確かめ（草案1 との不変）・旗の段（二本の全文）・事後の計算の器 v2', ['records/B/drafts/diff-draft2-draft3.diff', 'records/B/drafts/check-draft3-invariance.json', 'FLAGS', 'records/B/posthoc_by_direction_B.py'])]
out = []
for title, src in PARTS:
    out += ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, '']
    if src is None:
        out += REQ
        continue
    for rel in ([src] if isinstance(src, str) else src):
        if rel == 'FLAGS':
            out += ['<<< 始: 旗の段（`records/B/deviations/flag-record-B-2026-09-23.json` から） >>>', '', flags, '<<< 終: 旗の段 >>>', '']
            continue
        fence = '```' if not rel.endswith('.md') else ''
        out += ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), fence, rd(rel).rstrip(NL), fence, '<<< 終: `%s` >>>' % rel, '']
text = NL.join(out) + NL
open(os.path.join(HERE, 'review-request-results-B-r3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(REQ))
bp = os.path.join(HERE, 'bundle-results-B-r3-all-in-one.md')
open(bp, 'w', encoding='utf-8', newline=NL).write(text)
print('bundle', len(text), '字', hashlib.sha256(open(bp, 'rb').read()).hexdigest().upper()[:16])
