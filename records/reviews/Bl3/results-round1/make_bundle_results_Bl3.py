# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の結果の巡（正本 `review_plan.results`・新しい個体の系統外二名と claude.ai 二名）の依頼文と束を組む（B-lens の結果の巡の束の器の型）。
束の部: 第一部 依頼文／第二部 報告の草案（全文）と起草者の欄の元の文／第三部 集計の記録と組の出力の抜き出し（機械・検算に要る分）／第四部 凍結の本文（全文）／
第五部 正本（全文）／第六部 凍結の後の記録（凍結の記録・凍結の後の確かめと裁定 D242・封印の記録と二つの予想・下見と本の計算の走りの記録・一致だけを見る段の記録・言葉の記録・露出の記録）。
組の出力と集計の記録の全体（JSON）は長いので束に入れず、置き場と SHA16 を索引に書く。依頼文の数と SHA は器が記録から読む（手で打たない）。束が長いときは、部の境で分けた版も作る。
既にあるファイルには書かない。
用法: python records/reviews/Bl3/results-round1/make_bundle_results_Bl3.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, json, hashlib, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
bs = chr(92)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.strip()
head = git('rev-parse', '--short', 'HEAD')
OUT_REQ, OUT_ALL, OUT_IDX, OUT_EXT = (os.path.join(HERE, n) for n in ('request-results-Bl3.md', 'bundle-results-Bl3-all-in-one.md', 'bundle-index.md', 'extract-results-Bl3.json'))
for p in (OUT_REQ, OUT_ALL, OUT_IDX, OUT_EXT):
    assert not os.path.exists(p), '既にある: ' + p
T3 = json.load(open(j('design', 'contrasts-Bl3.json'), encoding='utf-8'))
FR = json.load(open(j('records', 'Bl3', 'FREEZE-RECORD-Bl3.json'), encoding='utf-8'))
A = json.load(open(j('records', 'Bl3', 'analysis-Bl3.json'), encoding='utf-8'))
J = json.load(open(j('records', 'Bl3', 'judge-Bl3.json'), encoding='utf-8'))
RP = json.load(open(j('records', 'predictions', 'predictions-Bl3-registrant.json'), encoding='utf-8'))
MF = FR['main_freeze']
for rel in ('design/design-Bl3-FROZEN.md', 'design/contrasts-Bl3.json'):
    assert FR['frozen_sha16'][rel] == s16(rel), ('凍結物が凍結の記録と違う', rel)
assert A['judge_record_sha16'] == s16('records/Bl3/judge-Bl3.json') and J['agree'] and not A['dry']
dirs = {p: v['dir'] for p, v in A['inputs'].items()}
MAIN_REL = 'results/Bl3/main/%s/main.json' % dirs['main']
M = json.load(open(j(*MAIN_REL.split('/')), encoding='utf-8'))
# ---- 第三部の抜き出し（機械）
cells = {}
for key, c in M['cells'].items():
    eff = c['effects']
    iso = np.array([v for k, v in eff.items() if k.startswith('iso:')], dtype=np.float64)
    ent = {'real': {k: v for k, v in sorted(eff.items()) if k.startswith('real')}}
    if len(iso):
        ent = {'noop_lo': c['lo']['noop'], 'pa_noop': c['pa_noop'],
               'named_and_stage_b_random': {k: eff[k] for k in ('static', 'loaded', 'Nk', 'td', 'rand:0', 'rand:1', 'rand:2') if k in eff},
               'real': ent['real'],
               'iso_summary': {'n': int(len(iso)), 'median': float(np.median(iso)), 'q1': float(np.percentile(iso, 25)), 'q3': float(np.percentile(iso, 75)),
                               'min': float(iso.min()), 'max': float(iso.max())}}
    cells[key] = ent
EXT = {'what': '結果の巡の束の第三部: 集計の記録（records/Bl3/analysis-Bl3.json）の区画のうち検算に要るものと、組 main の出力（%s）の升目と符号ごとの無操作の値・名前のある方向と段階 B の三本の効き目・実在の差の効き目・等方の効き目の要約（機械で抜き出した）' % MAIN_REL,
       'sources': {'analysis': {'path': 'records/Bl3/analysis-Bl3.json', 'sha16': s16('records/Bl3/analysis-Bl3.json')}, 'main': {'path': MAIN_REL, 'sha16': s16(MAIN_REL)}},
       'analysis': {k: A[k] for k in ('rows', 'rows_meta', 'gates', 'gate_rows', 'q7_rows', 'predictions_truth', 'predictions_meta', 'recompute', 'chance', 'head', 'main_run', 'descriptive', 'style_rows', 'env')},
       'cells': cells,
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
ext_text = json.dumps(EXT, ensure_ascii=False, indent=1)
open(OUT_EXT, 'w', encoding='utf-8', newline=NL).write(ext_text + NL)
EXT_REL = os.path.relpath(OUT_EXT, REPO).replace(os.sep, '/')
# ---- 依頼文の数（記録から）
dec = MF['decision'] or {}
q1 = dec.get('q1')
dropped = '・'.join(dec.get('dropped') or [])
m_rows = A['rows_meta']['m_rows']
coi_r = RP.get('info.coi') or ''
REQ = ['# B-lens 層三の結果の報告の草案の検分のお願い（結果の巡）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-27。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束はコミット %s の時点で組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % head,
       '- **初めての方へ**: あなたは、この登録（B-lens 層三）の検分に初めて加わる新しい個体です（正本 `review_plan.results.fresh`）。前の巡の票は公開の置き場の `records/reviews/Bl3/` にありますが、読まなくて構いません。束の中だけで検分できるように組みました。',
       '- **この登録の問い**（一つ）: %s。' % T3['scope']['question'],
       '- **経緯**: 下見の前の凍結（%s 日本時間・`design/design-Bl3-FROZEN.md`・凍結物 %d）の後に、登録者とコーディネータの予想を封印し（コーディネータが先・SHA だけを伝える順）、Colab（%s）で無操作だけの下見を走らせました'
       '（機械の決定「%s」・外した升目 %s・本の計算のバッチの大きさ %s）。本の凍結（%s 日本時間）の後に本の計算の三つの組を走らせ、一致だけを見る段（全体 %s）を経て、結果を登録者と一緒に開き、報告の草案を凍結した組み立ての器で組みました。凍結の後の逸脱は %d です。'
       % (FR['frozen_jst'], len(FR['frozen_sha16']), MF['sessions'][-1]['gpu'], q1, dropped, MF['pilot'].get('batch'), MF['frozen_jst'], '一致' if J['agree'] else '不一致', len(FR.get('deviations') or [])),
       '- **結果は公開済みで、伏せていません。** 検算は歓迎します（集計の記録 `records/Bl3/analysis-Bl3.json`〔SHA16 %s〕・組の出力 `results/Bl3/main/`・一致だけを見る段の記録 `records/Bl3/judge-Bl3.json`〔SHA16 %s〕）。検算に要る分は、束の第三部に機械で抜き出しました（`%s`）。'
       % (s16('records/Bl3/analysis-Bl3.json'), s16('records/Bl3/judge-Bl3.json'), EXT_REL),
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）と機種を書いてください。claude.ai の Claude は起草者と同じ系列で、何票でも一票に数えます。',
       '- **この巡の後**: 裁定・報告の直し・最終の系統外の一票（「最終」と明記）・起草者の最終の見直し・登録者最終確認と公開の順で、ほかに巡は置きません（正本 `review_plan`）。',
       '- **凍結の前後に起きたこと**（第六部に記録）:',
       '  - 下見の前の凍結の後の確かめで、凍結物の一つ（数の検査の記録）の一行に、組み立ての間の代わりの原稿の一時の置き場の道筋が残っていたことが見つかりました。登録者は、凍結物を凍結したとおりにし、逸脱を立てずに記録に置くと裁きました（裁定 D242・`records/Bl3/prepilot-freeze-check-Bl3.md`）。',
       '  - コーディネータの予想の値は、封印の台本（道具の呼び出しの中身）に出ました（登録者には封印の前に開かないよう伝えました）。登録者の予想の情報状態の欄は露出の記録の名を挙げておらず、封印の後に登録者の言葉で補いました（どちらも台帳の封印の行）。',
       '  - Colab で一行を打つときの打ち損じ（頭の字が落ちる）を、走らせる前の照らしで見つけて打ち直しました。壊れた一行は走らせていません（下見と本の計算の走りの記録）。',
       '- **起草者が結果を開いた後に見つけたこと**（所見に挙げて構いません）:',
       '  - 報告の §7（限界）の「段階 B の行動の記録は公開済みで…全経路の効き目の値はまだ誰も見ていない」は、正本の封印の前の文が機械の区画にそのまま出たもので、結果を開いた後の報告では事実と合いません。凍結した器の出力なので、直すなら逸脱になります（まだ直していません）。',
       '  - §7 の「割合は対称を仮定しない数え方で、最小の p と、十六行の Holm の第一段を通る外側の帰無の本数は…（値は §5）」の「§5」は凍結の本文の §5 を指し、報告の §5（独立の再計算）ではありません。行も、下見で外した後は %d 行です。' % m_rows,
       '  - 下見で、計算の道の小さな違い（バッチの大きさ・近道）で無操作の対数オッズが動きました（報告の §1 の (vi) の (a) と (v)）。等方の帰無の広がりも大きく、報告の読みはこの二つを分けずに扱っています（起草者の欄の一行目に添えました）。',
       '  - 等方の外の唯一の行（sub:N1）の升目は、無操作の選択肢 a の確率が床の近くで（報告の §2 の升目ごとの表）、この行の段階 B の行動の変化は区間が零を含みます（q7 で数えない行）。',
       '  - 等方の外でない行の効き目の符号には並びが見えますが、札でも門でもないので、報告は読みを付けていません。',
       '- **束の中身**: 第一部 依頼文／第二部 報告の草案（全文）と起草者の欄の元の文／第三部 集計の記録と組の出力の抜き出し（機械）／第四部 凍結の本文（全文）／第五部 正本（全文）／第六部 凍結の後の記録。組の出力と集計の記録の全体（JSON）は長いので束に入れず、索引に置き場を書きました。',
       '- **褒めるのではなく、公開の前に報告を崩すつもりで読んでください。** とくに、読みが直答の型の読み取りの位置の外（意味・機構・行動の原因）へ出ていないか、「区別できない」を弱めたり強めたりしていないかを見てください。', '',
       '## 1. 伺いたいこと', '',
       '1. **読みの型の当否**: 器が当てた読みの型（〈両方の外〉〈外でない行〉〈門を通らない〉〈下見で一部を外した〉〈揺れの版の値〉）は、凍結した読みの表（凍結の本文の §9）と数に照らして正しいか。直答の型の読み取りの位置の外へ出る言い方や、札の無い値に意味を持たせる言い方が紛れていないか（禁止語の走査は違反 0 ですが、語を替えた言い過ぎは走査で捕まりません）。',
       '2. **札と門の判定の検算**: Holm の段（下見で外した後の %d 行）・裾の本数と p・二つ目の札の順位（兄弟を除いた実在の差・両方の向き）・方向を単位にした門（全ての入れ替え・v̂ を抜いた門）の判定が、記録の数から正しく出ているか。段の近くの値を、希望の側にも逆の側にも読んでいないか。' % m_rows,
       '3. **数値の揺れと読み取りの測るもの**: 下見の (vi) の (a) と (v) の揺れ、等方の帰無の広がりの大きさ、床の近くの升目を、報告は足りる形で書いているか。足すべき限界の文はあるか。',
       '4. **起草者の欄（この結果が退けた説明）**: 三行は、この結果と凍結した決まりから支えられるか。「退けられた」は強すぎないか。ほかに、この結果が退けた説明や、退けていないのに退けたように読める所はあるか。',
       '5. **限界の二つの文**（上の「起草者が結果を開いた後に見つけたこと」の一つ目と二つ目）: 器を直す逸脱にするか・報告の機械の区画の外に注を足すか・記録に置けば足りるか。',
       '6. **予想の照合**: 照合の表に誤りや誤解を招く所はないか（q7 は採点しない）。照合は記録であり評価ではない、という書き方で足りるか。',
       '7. **手続き**: 凍結・封印・下見・本の凍結・本の計算・一致だけを見る段・結果を開く段の記録と順は足りているか。記録されていない変更や露出は見つかるか。',
       '8. **総合**: 公開に進めるか（公開可／条件つき可／差し戻し）。**公開の前に直すもの**と、**記録に置けば足りるもの**に分けてください。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 札と門の判定を変える提案（水準・帰無・行・外し方を変える）は、この登録の札には入りません。記述か、別の登録の候補として扱います。',
       '- 起草者は器と報告の組み立ての器と起草者の欄を書いた当人で「正しく読めている」と書く側に、登録者は封印した予想の欄（引かれている結論）に「%s」と書いた側にあります。どちらも利害の当事者です。二人の予想の当たり外れは照合の表にあります。' % coi_r, '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']
PARTS = [('第一部 依頼文', 'REQ'),
         ('第二部 報告の草案（全文）と起草者の欄の元の文', ['records/Bl3/results-Bl3.md', 'records/Bl3/results-rejected-lines-Bl3.md']),
         ('第三部 集計の記録と組の出力の抜き出し（機械）', [EXT_REL]),
         ('第四部 凍結の本文（全文）', ['design/design-Bl3-FROZEN.md']),
         ('第五部 正本（全文）', ['design/contrasts-Bl3.json']),
         ('第六部 凍結の後の記録', ['records/Bl3/FREEZE-RECORD-Bl3.md', 'records/Bl3/prepilot-freeze-check-Bl3.md', 'records/Bl3/rulings-D242.md', 'records/Bl3/sealing-record-Bl3.md',
                                'records/predictions/predictions-Bl3-coordinator.json', 'records/predictions/predictions-Bl3-registrant.json', 'records/Bl3/pilot/pilot-run-Bl3.md',
                                'records/Bl3/main/main-run-Bl3.md', 'records/Bl3/judge-Bl3.json', 'records/Bl3/prepilot-freeze-words-Bl3.md', 'records/Bl3/main-freeze-words-Bl3.md',
                                'records/Bl3/exposure-before-seal-Bl3.md'])]
blocks, idx = [], ['# 束の索引（B-lens 層三の結果の巡）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|']
for title, src_ in PARTS:
    part = ['', '=' * 20 + ' ' + title + ' ' + '=' * 20, '']
    if src_ == 'REQ':
        part += REQ
        idx.append('| %s | 依頼文（`%s`） | — |' % (title, os.path.relpath(OUT_REQ, REPO).replace(os.sep, '/')))
    else:
        for rel in src_:
            fence = '' if rel.endswith('.md') else '```'
            part += ['<<< 始: `%s`（SHA16 %s） >>>' % (rel, s16(rel)), fence, rd(rel).rstrip(NL), fence, '<<< 終: `%s` >>>' % rel, '']
            idx.append('| %s | `%s` | %s |' % (title, rel, s16(rel)))
    blocks.append((title, NL.join(part)))
for rel, what in (('records/Bl3/analysis-Bl3.json', '集計の記録の全体（束に入れない）'), (MAIN_REL, '組 main の出力（束に入れない）'),
                  ('results/Bl3/main/%s/recompute.json' % dirs['recompute'], '組 recompute の出力（束に入れない）'),
                  ('results/Bl3/main/%s/secondary.json' % dirs['secondary'], '組 secondary の出力（束に入れない）'),
                  ('records/Bl3/results-Bl3-machine.json', '報告の機械の区画の SHA16（束に入れない）')):
    idx.append('| （公開の置き場） | %s `%s` | %s |' % (what, rel, s16(rel)))
text = NL.join(b for _, b in blocks) + NL
home = os.path.expanduser('~')
for x in (home, home.replace(bs, '/'), home.replace(bs, bs + bs), 'AppData' + bs, 'AppData/', 'pasted' + '_content', 'system' + '-reminder'):
    assert x not in text, ('束に手元の道筋か印が入る', x)
open(OUT_REQ, 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
open(OUT_ALL, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(OUT_ALL, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-results-Bl3-all-in-one.md`: %d 字・SHA16 %s（組んだ時点のコミット %s）。' % (len(text), h, head)]
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
        fp = os.path.join(HERE, 'bundle-results-Bl3-part%d.md' % k)
        assert not os.path.exists(fp), '既にある: ' + fp
        head_line = '（B-lens 層三の結果の巡の束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups))
        body = head_line + NL + NL.join(b for _, b in g) + NL
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-results-Bl3-part%d.md`: %s・%d 字・SHA16 %s。' % (k, len(groups), k, '・'.join(t for t, _ in g), len(body), hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_IDX, 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | parts', [(t.split(' ')[0], len(b)) for t, b in blocks], '| extract', len(ext_text), '字')
