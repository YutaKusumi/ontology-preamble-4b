# -*- coding: utf-8 -*-
"""bundle_final_A.py v1 —— 段階 A 設計草案7（凍結候補の二つ目）の凍結前の最終検分用 bundle を機械連結する（2026-09-14・bundle_prefreeze_A.py の型・登録者決定: 手順5 を凍結前の最終検分とする）。
部品は逐語（LF 正規化）で、各部品の SHA16 と字数を見出しに印字する。内部の計画案は含めない。系統外（Gemini・Grok）と claude.ai の Claude に同じものを渡す。
貼付の上限に合わせて、部品の境目で複数の部に分ける（--max-chars・部品は割らない・一つの部品が上限を超えるときはその部品だけで一部にする）。各部の冒頭に全部の目次と SHA16 を置く。
部品が欠けていれば止まる（--allow-missing は検査用で、欠けを目次に印字する）。
出力: records/reviews/A/final/bundle-A-final-part<k>.md（k は一始まり）と同 -index.md。
用法: python tools/bundle_final_A.py [--max-chars 300000] [--allow-missing]
柵: 本 bundle のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, hashlib, datetime, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTD = os.path.join(REPO, 'records', 'reviews', 'A', 'final')
PARTS = [('依頼文（凍結前の最終検分）', 'records/reviews/A/final/review-request-A-final.md'),
         ('段階 A 設計草案7（凍結候補の二つ目）', 'design/design-stageA-draft7.md'),
         ('草案7 の原稿（正本のキー参照）', 'design/design-stageA-draft7.src.md'),
         ('報告雛形 A（組み立て）', 'records/A/results-report-template-A.md'),
         ('報告雛形 A の原稿', 'records/A/results-report-template-A.src.md'),
         ('運用の解釈の一覧（登録者の確認待ち）', 'records/A/tooling-interpretations-A.md'),
         ('本文の数の機械検査（草案7）', 'records/A/numbers-lint-draft7A.md'),
         ('本文の数の機械検査（雛形）', 'records/A/numbers-lint-template-A.md'),
         ('設計事実 A（転記行 A〜O の出所）', 'records/A/design-facts-A.md'),
         ('正本 contrasts-A.json', 'design/contrasts-A.json'),
         ('検出力格子 A', 'records/A/power-grid-A.md'),
         ('機種の設定と GPU 容量 hf-models-A.json', 'records/A/hf-models-A.json'),
         ('門0 の実測 cost-facts', 'records/cost-pilot/cost-facts-2026-09-13.md'),
         ('合成検査（集計器）の記録', 'records/A/synth-A-2026-09-14.md'),
         ('合成検査（門と校正の器）の記録', 'records/A/synth-gates-A-2026-09-14.md'),
         ('草案6 の凍結前検分の採否表（P1〜P74・裁定 D9〜D15）', 'records/reviews/A/prefreeze/adoption-table-A-prefreeze.md'),
         ('手順4 実装検分の依頼文', 'records/reviews/A/draft7-impl/review-request-impl-A.md'),
         ('手順4 実装検分の事前登録', 'records/reviews/A/draft7-impl/preregistration-impl-review-A.md'),
         ('手順4 検分者 1 の票（逐語）', 'records/reviews/A/draft7-impl/reviewer-1/review.md'),
         ('手順4 検分者 2 の票（逐語）', 'records/reviews/A/draft7-impl/reviewer-2/review.md'),
         ('手順4 の採否表（反映の記録）', 'records/reviews/A/draft7-impl/adoption-table-impl-A.md')] + \
        [(t, 'tools/' + t) for t in ('confirm_A.py', 'bands_A.py', 'runs_A.py', 'zaxis_A.py', 'firth.py', 'analyze_A.py', 'gate_A.py', 'calib_band_A.py', 'identity_screen_A.py', 'control_chart_A.py',
                                    'response_mode_A.py', 'integrity_A.py', 'sample_inspection_A.py', 'judge_fragments_A.py', 'build_report_A.py', 'report_lint.py', 'freeze_A.py', 'build_draftA.py',
                                    'numbers_lint.py', 'make_contrasts_A.py', 'power_grid_A.py', 'design_facts_A.py', 'colab/boot_stageA.py', 'synth_A.py', 'synth_gates_A.py', 'firth_check_A.py', 'firth_check_A.R')]
LANG = {'.py': 'python', '.json': 'json', '.R': 'r'}
CLAUSE = '本 bundle のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'

ap = argparse.ArgumentParser(); ap.add_argument('--max-chars', type=int, default=300000); ap.add_argument('--allow-missing', action='store_true'); ap.add_argument('--outdir', default=None); a = ap.parse_args()
OUTD = a.outdir or OUTD
items = []; missing = []
for title, rel in PARTS:
    p = os.path.join(REPO, rel.replace('/', os.sep))
    if not os.path.exists(p):
        missing.append(rel); continue
    b = open(p, 'rb').read().replace(b'\r\n', b'\n'); text = b.decode('utf-8')
    items.append({'title': title, 'rel': rel, 'sha16': hashlib.sha256(b).hexdigest()[:16].upper(), 'chars': len(text), 'text': text, 'lang': LANG.get(os.path.splitext(rel)[1], '')})
if missing and not a.allow_missing:
    sys.exit('部品が欠けている（反映の前は --allow-missing で目次だけ確かめる）: %s' % '・'.join(missing))
parts = [[]]; size = 0
for it in items:
    if parts[-1] and size + it['chars'] > a.max_chars:
        parts.append([]); size = 0
    parts[-1].append(it); size += it['chars']
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
toc = ['| 部 | 部品 | パス | SHA16 | 字数 |', '|---|---|---|---|---|'] + ['| %d | %s | `%s` | %s | %s |' % (k, it['title'], it['rel'], it['sha16'], format(it['chars'], ',')) for k, P in enumerate(parts, 1) for it in P]
if missing:
    toc += ['', '- 欠けている部品（検査用の組み立て）: %s' % '・'.join(missing)]
os.makedirs(OUTD, exist_ok=True)
for k, P in enumerate(parts, 1):
    L = ['# 段階 A 凍結前の最終検分 bundle 第 %d 部／全 %d 部（機械連結・`tools/bundle_final_A.py` v1・%s UTC）' % (k, len(parts), stamp), '',
         '- 部品は逐語（LF 正規化）。見出しの SHA16 はファイルバイトの SHA-256 先頭 16 桁（CRLF→LF 正規化）。全部の目次は下の表。', '', '## 目次（全部）', ''] + toc + ['']
    for it in P:
        fence = '````' if '```' in it['text'] else '```'
        L += ['## 部品: %s（`%s`・SHA16 %s・%s 字）' % (it['title'], it['rel'], it['sha16'], format(it['chars'], ',')), '', fence + it['lang'], it['text'].rstrip('\n'), fence, '']
    L += [CLAUSE]
    open(os.path.join(OUTD, 'bundle-A-final-part%d.md' % k), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
open(os.path.join(OUTD, 'bundle-A-final-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(['# 段階 A 凍結前の最終検分 bundle の目次（%s UTC・全 %d 部）' % (stamp, len(parts)), ''] + toc + ['', CLAUSE]) + '\n')
print('[bundle_final_A] %d 部・部品 %d・欠け %d・合計 %s 字 → %s' % (len(parts), len(items), len(missing), format(sum(it['chars'] for it in items), ','), OUTD))
