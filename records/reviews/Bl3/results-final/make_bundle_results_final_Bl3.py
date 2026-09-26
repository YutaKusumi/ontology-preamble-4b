# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の最終の系統外の一票（正本 `review_plan.final`・新しい個体・「最終」と明記）の依頼文と束を組む（結果の巡の束の器 `records/reviews/Bl3/results-round1/make_bundle_results_Bl3.py` の型）。
束の部: 第一部 依頼文／第二部 報告の草案の二つ目（全文）／第三部 結果の巡の後の記録と逸脱の器（採否の案・再現の記録・裁定 D243〜D246・開く段の記録・凍結の記録・
草案の二つ目の二つの確かめの記録・逸脱の器の台本）／第四部 凍結の本文（全文）／第五部 正本（全文）。結果の巡の四票と組の出力と集計の記録の全体は束に入れず、置き場と SHA16 を索引に書く。
依頼文の数と SHA は器が記録から読む（手で打たない）。束が長いときは、部の境で分けた版も作る。既にあるファイルには書かない。
用法: python records/reviews/Bl3/results-final/make_bundle_results_final_Bl3.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
bs = chr(92)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
ld = lambda rel: json.load(open(j(*rel.split('/')), encoding='utf-8'))
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
git = lambda *a: subprocess.run(['git'] + list(a), cwd=REPO, capture_output=True, text=True, encoding='utf-8').stdout.strip()
head = git('rev-parse', '--short', 'HEAD')
assert not git('status', '--porcelain', '--untracked-files=no'), '作業木に、コミットしていない直しがある（束はコミットの時点で組む）'
OUT_REQ, OUT_ALL, OUT_IDX = (os.path.join(HERE, n) for n in ('request-results-final-Bl3.md', 'bundle-results-final-Bl3-all-in-one.md', 'bundle-index.md'))
for p in (OUT_REQ, OUT_ALL, OUT_IDX):
    assert not os.path.exists(p), '既にある: ' + p
T3, FR = ld('design/contrasts-Bl3.json'), ld('records/Bl3/FREEZE-RECORD-Bl3.json')
A, J = ld('records/Bl3/analysis-Bl3.json'), ld('records/Bl3/judge-Bl3.json')
RP = ld('records/predictions/predictions-Bl3-registrant.json')
V = ld('records/reviews/Bl3/results-round1/checks/verification-results-Bl3.json')
CK = ld('records/Bl3/results-Bl3-draft2-checks.json')
D2C = ld('records/Bl3/draft2-check/check-draft2-Bl3.json')
OJ = ld('records/Bl3/open-results-Bl3.json')
MF = FR['main_freeze']
for rel in ('design/design-Bl3-FROZEN.md', 'design/contrasts-Bl3.json'):
    assert FR['frozen_sha16'][rel] == s16(rel), ('凍結物が凍結の記録と違う', rel)
assert A['judge_record_sha16'] == s16('records/Bl3/judge-Bl3.json') and J['agree'] and not A['dry']
assert CK['sha16']['records/Bl3/results-Bl3.md'] == s16('records/Bl3/results-Bl3.md') and CK['sha16']['tools/build_report_Bl3_devBLT1.py'] == s16('tools/build_report_Bl3_devBLT1.py')
assert D2C['inputs']['records/Bl3/results-Bl3-draft2.md'] == s16('records/Bl3/results-Bl3-draft2.md') and all(x['ok'] for x in D2C['checks'])
ad = rd('records/reviews/Bl3/results-round1/adoption-results-Bl3.md')
ps = re.findall(r'^\| (P\d+) \|', ad, re.M)
idx_v = rd('records/reviews/Bl3/results-round1/votes-index.md')
votes = re.findall(r'^\| ([GC]\d) \| `', idx_v, re.M)
ev = {e['key']: e['jst'] for e in OJ['events']}
devs = FR.get('deviations') or []
dec = MF['decision'] or {}
coi_r = RP.get('info.coi') or ''
REQ = ['# B-lens 層三の結果の報告の草案の検分のお願い（最終検分・最終の系統外の一票）', '',
       '- 依頼者: 楠見優太（登録者）／起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／2026-09-27。',
       '- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束はコミット %s の時点で組んだ。`prelim/` と `results/prelim-*` は開かないでください）。' % head,
       '- **これは最終検分です。** 正本 `review_plan` の「最終の系統外の一票」にあたります。あなたの所見は、裁定で受けて報告を直し、起草者の最終の見直しと登録者最終確認を経て公開します。この後に検分の巡は置きません。あなたは、この登録（B-lens 層三）の前の巡の票を見ていない新しい個体です。',
       '- **最終検分なので**、所見は「公開の前に直すもの」と「記録に置けば足りるもの」にはっきり分けてください。公開の前に直すものは、もう一度の検分を経ずに直します。',
       '- **系統**: 票の頭に、あなたの系統（系統外か、起草者と同じ Claude 系か）と機種を書いてください。',
       '- **この登録の問い**（一つ）: %s。' % T3['scope']['question'],
       '- **経緯**: 下見の前の凍結（%s 日本時間・`design/design-Bl3-FROZEN.md`・凍結物 %d）の後に、登録者とコーディネータの予想を封印し、Colab（%s）で無操作だけの下見を走らせました（機械の決定「%s」・本の計算のバッチの大きさ %s）。'
       '本の凍結（%s 日本時間）の後に本の計算の三つの組を走らせ、一致だけを見る段（全体 %s）の記録を公開してから、%s（日本時間）に結果を開きました（開く段の記録 `records/Bl3/open-results-Bl3.md`）。'
       % (FR['frozen_jst'], len(FR['frozen_sha16']), MF['sessions'][-1]['gpu'], dec.get('q1'), MF['pilot'].get('batch'), MF['frozen_jst'], '一致' if J['agree'] else '不一致', ev['open']),
       '- **結果の巡**: 凍結した組み立ての器が組んだ報告の草案（一つ目）を、新しい個体の %d 名（系統外 %d 名・claude.ai の Claude %d 名で一票）に見ていただき、全員が「条件つき可」でした。票の事実の主張を現物で再現し（%s〜%s）、採否の案（%s〜%s）を作り、登録者が推奨の案をすべて承認しました（裁定 D243〜D246・`records/Bl3/rulings-D243-D246.md`）。'
       % (len(votes), sum(1 for v in votes if v.startswith('G')), sum(1 for v in votes if v.startswith('C')), V['checks'][0]['k'], V['checks'][-1]['k'], ps[0], ps[-1]),
       '- **報告の草案の二つ目の組み方**: 凍結した組み立ての器の出力（起草者の欄の三行を器の口で直して組み直したもの・`records/Bl3/results-Bl3.md`）は、見出しと状態の行のほか一字も変えず、逸脱の下の器 `tools/build_report_Bl3_devBLT1.py` が【逸脱 D-BLT1】の印を付けた機械の区画 %d を足しました。'
       '器は、足した区画を取り除いて見出しと状態の行を戻すと凍結した器の出力とバイトで同じになることと、印の区画の数が結果の巡の再現の記録と合うこと（照らした項 %d・外れ 0）を確かめ、別の台本でも確かめました（%d／%d・第三部）。凍結の後の逸脱は %d です（%s・第三部の凍結の記録の台帳）。'
       % (CK['added_blocks'], len(CK['cross_checks']), sum(1 for x in D2C['checks'] if x['ok']), len(D2C['checks']), len(devs), '・'.join(d['no'] for d in devs)),
       '- **結果は公開済みで、伏せていません。** 検算は歓迎します（集計の記録 `records/Bl3/analysis-Bl3.json`〔SHA16 %s〕・組の出力 `results/Bl3/main/`・一致だけを見る段の記録 `records/Bl3/judge-Bl3.json`〔SHA16 %s〕）。' % (s16('records/Bl3/analysis-Bl3.json'), s16('records/Bl3/judge-Bl3.json')),
       '- **束の中身**: 第一部 依頼文／第二部 報告の草案の二つ目（全文）／第三部 結果の巡の後の記録（採否の案・再現の記録・裁定 D243〜D246・開く段の記録・凍結の記録・草案の二つ目の二つの確かめの記録）と逸脱の器の台本（全文）／第四部 凍結の本文（全文）／第五部 正本（全文）。結果の巡の四票は束に入れていません（置き場の `records/reviews/Bl3/results-round1/` にあります。採否の案が要旨を書いています）。',
       '- **褒めるのではなく、公開の前に報告を崩すつもりで読んでください。** とくに、足した区画が凍結の決まり（札・門・読みの型）を変えていないか、直答の型の読み取りの位置の外（意味・機構・行動の原因）へ読みを広げていないか、「区別できない」を弱めたり強めたりしていないかを見てください。', '',
       '## 1. 伺いたいこと', '',
       '1. **足した区画の当否**: 足した区画は、採否の案の区分（三）の行を正しく受けているか。数の書き写しや、文の言い過ぎ・言い足りなさはないか。凍結の報告の文と区画が変わっていないか。',
       '2. **唯一の等方の外の行の注**: 〈両方の外〉の隣の注（升目の事情と札の余白）の並べ方で、札が重く読まれることも、軽く読まれすぎることもないか。',
       '3. **起草者の欄の三行**: この結果と凍結した決まりから支えられるか。一行目の「退けられた」（範囲を添えた。結果の巡では系統外の二票が緩めるか撤回するよう求め、登録者は範囲を添えて保つと裁いた・裁定 D244）は強すぎないか。',
       '4. **表の直し方**: 凍結の表を残し、表の前に断りを、表の後に升目の名の縦棒を逃がした並べ直しの表を置く形（B-lens の前例）で、表示の問題は解けているか。',
       '5. **限界と注**: §3・§5・§6・§7 の注と計算の道の注で、限界と「言えないこと」は、この結果に対して足りているか。',
       '6. **手続き**: 凍結の後の逸脱の台帳・開く段の記録・裁定の記録は足りているか。記録されていない変更や露出は見つかるか。',
       '7. **総合**: 公開に進めるか（公開可／条件つき可／差し戻し）。**公開の前に直すもの**と、**記録に置けば足りるもの**に分けてください。', '',
       '## 2. お願い', '',
       '- 何を開き、何を検算し、何を見ていないかを書いてください（**確認していないこと**の欄を必ず）。',
       '- 所見には重さ（重大・中・軽）と、根拠の置き場（束の部と行、または公開の置き場のファイル）を付けてください。',
       '- 札と門の判定を変える提案（水準・帰無・行・外し方を変える）は、この登録の札には入りません。記述か、別の登録の候補として扱います。',
       '- 起草者は器と報告の組み立ての器と逸脱の器を書き、結果の巡の採否の案を出した当人で、「直した」と書く側に引かれます。登録者は、封印した予想の欄（引かれている結論）に「%s」と書いた側にあります。どちらも利害の当事者です。二人の予想の当たり外れは照合の表にあります。' % coi_r, '',
       '本依頼と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。']
PARTS = [('第一部 依頼文', 'REQ'),
         ('第二部 報告の草案の二つ目（全文）', ['records/Bl3/results-Bl3-draft2.md']),
         ('第三部 結果の巡の後の記録と逸脱の器', ['records/reviews/Bl3/results-round1/adoption-results-Bl3.md', 'records/reviews/Bl3/results-round1/checks/verification-results-Bl3.md',
                                        'records/Bl3/rulings-D243-D246.md', 'records/Bl3/open-results-Bl3.md', 'records/Bl3/FREEZE-RECORD-Bl3.md', 'records/Bl3/results-Bl3-draft2-checks.json',
                                        'records/Bl3/draft2-check/check-draft2-Bl3.md', 'tools/build_report_Bl3_devBLT1.py']),
         ('第四部 凍結の本文（全文）', ['design/design-Bl3-FROZEN.md']),
         ('第五部 正本（全文）', ['design/contrasts-Bl3.json'])]
blocks, idx = [], ['# 束の索引（B-lens 層三の最終の系統外の一票）', '', '| 部 | 中身 | SHA16 |', '|---|---|---|']
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
dirs = {p: v['dir'] for p, v in A['inputs'].items()}
for rel, what in (('records/Bl3/results-Bl3.md', '凍結した組み立ての器の出力（草案の一つ目を起草者の欄の口で直したもの・束に入れない）'), ('tools/build_report_Bl3.py', '凍結した組み立ての器（束に入れない）'),
                  ('records/Bl3/results-rejected-lines-Bl3.md', '起草者の欄の元の文（束に入れない）'), ('records/Bl3/report-marks-Bl3.json', '逸脱の印の JSON（束に入れない）'),
                  ('records/Bl3/analysis-Bl3.json', '集計の記録の全体（束に入れない）'), ('results/Bl3/main/%s/main.json' % dirs['main'], '組 main の出力（束に入れない）'),
                  ('records/Bl3/results-Bl3-draft2-machine.json', '草案の二つ目の機械の区画の SHA16（束に入れない）')):
    idx.append('| （公開の置き場） | %s `%s` | %s |' % (what, rel, s16(rel)))
idx.append('| （公開の置き場） | 結果の巡の四票 `records/reviews/Bl3/results-round1/<札>/vote.md`（束に入れない） | — |')
text = NL.join(b for _, b in blocks) + NL
home = os.path.expanduser('~')
for x in (home, home.replace(bs, '/'), home.replace(bs, bs + bs), 'AppData' + bs, 'AppData/', 'pasted' + '_content', 'system' + '-reminder'):
    assert x not in text, ('束に手元の道筋か印が入る', x)
open(OUT_REQ, 'w', encoding='utf-8', newline=NL).write(NL.join(REQ) + NL)
open(OUT_ALL, 'w', encoding='utf-8', newline=NL).write(text)
h = hashlib.sha256(open(OUT_ALL, 'rb').read()).hexdigest().upper()[:16]
idx += ['', '- 一通版 `bundle-results-final-Bl3-all-in-one.md`: %d 字・SHA16 %s（組んだ時点のコミット %s）。' % (len(text), h, head)]
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
        fp = os.path.join(HERE, 'bundle-results-final-Bl3-part%d.md' % k)
        assert not os.path.exists(fp), '既にある: ' + fp
        head_line = '（B-lens 層三の最終の系統外の一票の束・分けた版 %d／%d・中身は一通版と同じ）' % (k, len(groups))
        body = head_line + NL + NL.join(b for _, b in g) + NL
        open(fp, 'w', encoding='utf-8', newline=NL).write(body)
        idx.append('- 分けた版 %d／%d `bundle-results-final-Bl3-part%d.md`: %s・%d 字・SHA16 %s。' % (k, len(groups), k, '・'.join(t for t, _ in g), len(body), hashlib.sha256(open(fp, 'rb').read()).hexdigest().upper()[:16]))
idx += ['- 本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_IDX, 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print('bundle', len(text), '字', h, '| request', len(NL.join(REQ)), '字 | parts', [(t.split(' ')[0], len(b)) for t, b in blocks], '| commit', head)
