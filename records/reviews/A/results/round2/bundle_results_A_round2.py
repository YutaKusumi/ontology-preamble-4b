# -*- coding: utf-8 -*-
"""bundle_results_A_round2.py（一時置き場の器・凍結物ではない・2026-09-17・コーディネータ）—— 結果報告 草案4 の公開前の最終検分（第二巡）の bundle を機械で組む。
部品は逐語で連結し（抜粋は器が切り出す）、部品ごとにパス・SHA16（LF にそろえた sha256 の先頭 16 桁）・字数を記す。
出力: records/reviews/A/results/round2/bundle-round2-index.md と bundle-round2-part1.md・part2.md（既存は上書きしない）。
依頼文に書いた数（感度閾値・札の内訳）を、正本と機械集計と第一巡の再現の記録に照らしてから組む。
"""
import os, sys, re, json, hashlib, datetime, difflib, collections

REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
OUTD = os.path.join(REPO, 'records', 'reviews', 'A', 'results', 'round2')
NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
MB = ('<!-- 機械:始 -->', '<!-- 機械:終 -->')


def rd(rel):
    return open(os.path.join(REPO, rel), encoding='utf-8').read().replace('\r\n', '\n')


def s16(rel):
    return hashlib.sha256(open(os.path.join(REPO, rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


for fn in ('bundle-round2-index.md', 'bundle-round2-part1.md', 'bundle-round2-part2.md'):
    if os.path.exists(os.path.join(OUTD, fn)):
        sys.exit('既にある（上書きしない）: %s' % fn)

REQ = 'records/reviews/A/results/round2/review-request-results-A-round2-final.md'
D3P = 'records/A/results-report-A-draft3-2026-09-17.md'; D4P = 'records/A/results-report-A-draft4-2026-09-17.md'
T = json.loads(rd('design/contrasts-A.json')); AN = json.loads(rd('records/A/analysis-stageA.json'))
V1 = json.loads(rd('records/reviews/A/results/round1/verification-results-A-round1.json'))
req = rd(REQ)

# ---- 依頼文の数の照合
w130 = next(x for x in V1['items'] if x['w'] == 'W130')['detail']
pup = [p for p in w130['passes'] if p['upward']]
assert len(pup) == 1 and pup[0]['upward'] == ['N2:Onull~N', 'S1:Onull-Ncold~Onull']
sens = T['censor']['sensitivity']
i_up = [i for i, lo in enumerate(sens['low']) if abs(lo - pup[0]['low']) < 1e-12][0]
assert '（%s／%s）' % (sens['low'][i_up], sens['high'][i_up]) in req, (sens['low'][i_up], sens['high'][i_up])
assert sens['low'][i_up] < T['censor']['low'] and sens['high'][i_up] > T['censor']['high']
lc = AN['label_counts']; L = T['families']['A_slope']['confirm_rule']['labels']
want = '確証 %d（S4 の Onull 対 N）・判定不能 %d・記述（解釈条項）%d・判定保留（様式転位）%d・非有意 %d。' % (lc['confirmed'], lc['undecidable'], lc['clause'], lc['style'], lc['ns'])
assert want in req, want
assert lc['scale_only'] == 0 and lc['refuse'] == 0 and lc['env'] == 0 and not AN['upward_confirmed']
assert [x['id'] for x in AN['contrasts'] if x['label'] == L['confirmed']] == ['S4:Onull~N']
nm = sum(1 for v in AN['measurable']['types'].values() if v['measurable'])
assert '測れた効果種は %d 種のうち %d。' % (len(AN['measurable']['types']), nm) in req
assert [p['id'] for p in AN['measurable']['per_contrast'] if p.get('measured_contrast')] == ['S1:Lneg~Onull']
assert 'Holm（m=%d 固定）' % T['families']['A_slope']['m'] in req
if 'n_per_arm' in T:
    assert '× 5 場面 × n=%d' % T['n_per_arm'] in req, T['n_per_arm']
assert '× %d 場面 × n=' % len(T['scenarios']) in req and '%d 効果種 × %d 場面の %d 対比' % (len(AN['measurable']['types']), len(T['scenarios']), T['families']['A_slope']['m']) in req
assert '%d の前置きの腕' % len(T['arms']['preamble']) in req and '・'.join(T['sizes']) in req and next(m['key'] for m in T['models'] if m['anchor']) == '4B-2507'
import subprocess
HEADC =subprocess.run(['git', '-C', REPO, 'rev-parse', '--short=7', 'HEAD'], capture_output=True, text=True).stdout.strip()
BUILDER = 'records/reviews/A/results/round2/bundle_results_A_round2.py'
assert os.path.exists(os.path.join(REPO, BUILDER)) and open(os.path.join(REPO, BUILDER), 'rb').read() == open(os.path.abspath(__file__), 'rb').read(), '器の写しを先に置く'

# ---- 差分（草案3 → 草案4）
L3 = rd(D3P).split('\n'); L4 = rd(D4P).split('\n')
assert not any('```' in l for l in L3 + L4)
sm = difflib.SequenceMatcher(a=L3, b=L4, autojunk=False)
diff = ['- 生成: `difflib.SequenceMatcher`（行単位）。「−」は草案3 にあって草案4 で消した行、「＋」は草案4 で足した行。行番号は各ファイルの行（1 始まり）。', '']
k = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    k += 1
    kind = {'replace': '置き換え', 'delete': '削除', 'insert': '追加'}[tag]
    diff.append('### 変更 %d（%s・草案3 の %s・草案4 の %s）' % (k, kind, ('%d〜%d 行' % (i1 + 1, i2)) if i2 > i1 else 'なし（%d 行の後）' % i1, ('%d〜%d 行' % (j1 + 1, j2)) if j2 > j1 else 'なし（%d 行の後）' % j1))
    diff.append('')
    diff.append('```text')
    diff += ['− ' + l for l in L3[i1:i2]] + ['＋ ' + l for l in L4[j1:j2]]
    diff.append('```')
    diff.append('')
diff.insert(1, '- 変更のまとまり: %d。' % k)

# ---- 台帳の抜粋
DL = rd('records/DEVIATIONS.md').split('\n')
ledger = '\n'.join(DL[:3] + [l for l in DL if l.startswith('| D-') and int(l.split('|')[1].strip()[2:]) >= 33]) + '\n'

# ---- 一次記録の抜粋（機械で切り出す）
ex = []
ex += ['## 抜粋 1: 感度閾値の上向きの二本（第一巡の再現の記録 `records/reviews/A/results/round1/verification-results-A-round1.json` の W130 の詳細・SHA16 %s）' % s16('records/reviews/A/results/round1/verification-results-A-round1.json'), '',
       '```json', json.dumps({k2: w130[k2] for k2 in ('main_labels_match_json', 'passes', 'machine_prints_upward_only_for_main', 'stopped_before_measurable')}, ensure_ascii=False, indent=1), '```', '']
S = json.loads(rd('records/A/style-stageA.json'))
rows = ['| 機種 | 腕 | n_ok | (b) JSON 直答の件数 | 層: JSON 直答（n・破局） | 層: 散文（n・破局） | 言及 c2 の件数 |', '|---|---|---|---|---|---|---|']
for s_ in T['sizes']:
    for arm in ('Onull', 'N'):
        v = S['cells'][s_]['S4'][arm]
        rows.append('| %s | %s | %d | %d | %d・%d | %d・%d | %d |' % (s_, arm, v['n_ok'], v['b_final'], v['strata']['json_direct']['n'], v['strata']['json_direct']['cat'], v['strata']['prose']['n'], v['strata']['prose']['cat'], v['c2_final']))
c = next(x for x in AN['contrasts'] if x['id'] == 'S4:Onull~N')
ex += ['## 抜粋 2: 確証の一本（S4 の Onull 対 N）の応答様式の層（`records/A/style-stageA.json`・SHA16 %s）と集計の残存（`records/A/analysis-stageA.json`・SHA16 %s）' % (s16('records/A/style-stageA.json'), s16('records/A/analysis-stageA.json')), ''] + rows + ['',
       '- 集計の残存規模（keep）: %s・検閲: %s・測定不能で除外: %s・規模ごとの環境: %s・臨界規模: %s' % (
           json.dumps(dict(zip(T['sizes'], c['result']['keep']))), json.dumps(dict(zip(T['sizes'], c['result']['censored']))), json.dumps(dict(zip(T['sizes'], c['excluded_unmeasurable']))),
           json.dumps({s_: AN['size_env']['%s|S4' % s_] for s_ in T['sizes']}, ensure_ascii=False), json.dumps(c['critical_size'], ensure_ascii=False)),
       '- 感度閾値で札が変わった対比（集計の JSON）: %s' % json.dumps([{'low': x['low'], 'high': x['high'], 'changed': x['changed']} for x in AN['sensitivity']], ensure_ascii=False), '']
ex += ['## 抜粋 3: 散文層の副次終点の対比の並び（`records/A/analysis-stageA.json` の stratified）', '', '```json',
       json.dumps([{k2: x.get(k2) for k2 in ('id', 'style', 'status', 'sizes')} for x in AN['stratified']], ensure_ascii=False), '```', '']
canon_keys = [('report_rules.typed_numbers', T['report_rules']['typed_numbers']), ('report_rules.upward_rule', T['report_rules']['upward_rule']),
              ('censor', T['censor']), ('style_gate.numerator', T['style_gate']['numerator']), ('style_gate.stratified', T['style_gate']['stratified']),
              ('reading_selection.text', T['reading_selection']['text']), ('judge_validity.source', T['judge_validity']['source']),
              ('judge_validity.extract.label', T['judge_validity']['extract']['label']), ('print_strings.label_confirmed', T['print_strings']['label_confirmed']),
              ('print_strings.stratified_note', T['print_strings']['stratified_note']), ('print_strings.style_note', T['print_strings']['style_note']),
              ('print_strings.floor_desc', T['print_strings']['floor_desc']), ('interpretation_clause.min_sizes', T['families']['A_slope']['interpretation_clause']['min_sizes'])]
ex += ['## 抜粋 4: 正本 `design/contrasts-A.json`（SHA16 %s）の該当の値' % s16('design/contrasts-A.json'), '']
ex += ['- `%s`: %s' % (k2, json.dumps(v, ensure_ascii=False)) for k2, v in canon_keys] + ['']
FZ = rd('design/design-stageA-FROZEN.md').split('\n')
sel = FZ[26][:FZ[26].find('**測れた効果種**')]
fz_lines = [('§1 正本の選択規則（27 行の前半）', sel), ('§2.6（66 行）', FZ[65]), ('§2.11（88 行の先頭）', FZ[87][:160] + '…')]
fz_lines += [('§2.15（%d 行）' % (i + 1), FZ[i]) for i in range(len(FZ)) if i > 0 and FZ[i - 1].startswith('### 2.15')][:1]
fz_lines += [('§3 %s' % l.split(' ')[1], l) for l in FZ if re.match(r'^- \((ii|vii|xii|xiii|xv|xvi)\) ', l)]
ex += ['## 抜粋 5: 凍結本文 `design/design-stageA-FROZEN.md`（SHA16 %s）の該当の行' % s16('design/design-stageA-FROZEN.md'), '']
ex += ['- %s: %s' % (a, b) for a, b in fz_lines] + ['']
MR = rd('records/A/main/main-run-A.md').split('\n')
mr_items = [l for l in MR if l.startswith('1. **橋 4B の一回目の起動') or l.startswith('12. **セッションの順番を段取りから変えた')]
s6 = MR.index('## 6. 段取りとの差分と費用')
t6 = [l for l in MR[s6:s6 + 14] if l.startswith('| 実行の順') or l.startswith('|---') or l.startswith('| 9 | bridge:8B |')]
s8 = MR.index('## 8. COI（事実のみ）')
m8 = [l for l in MR[s8:s8 + 6] if l.startswith('- 目に入ったもの')]
assert len(mr_items) == 2 and len(t6) == 3 and len(m8) == 1
ex += ['## 抜粋 6: 走行記録 `records/A/main/main-run-A.md`（SHA16 %s）の §1-1・§1-12・§6 の表の橋 8B の行・§8 の目に入ったもの' % s16('records/A/main/main-run-A.md'), ''] + mr_items + [''] + t6 + [''] + m8 + ['']
AP = rd('records/A/main/api-rerun-run-A.md').split('\n')
ap_items = [l for l in AP if l.startswith('1. **事業者は非思考モードの指定を受け付けなかった') or l.startswith('2. **下見の確かめ方が誤っていた')]
ap_tab = [l for l in AP if l.startswith('| 相 | 機種 | 走行キー') or (l.startswith('|---') and '|---|---|---|---|---|---|---|---|---|---|---|---|---|' in l) or l.startswith('| 本番 |')]
AG = rd('records/A/main/aggregation-plan-A.md').split('\n')
ag = [l for l in AG if 'reasoning_chars' in l and 'が 0' in l]
assert len(ap_items) == 2 and len(ag) == 1
ex += ['## 抜粋 7: API 再走行の記録 `records/A/main/api-rerun-run-A.md`（SHA16 %s）の §1-1・§1-2・§2 の本番の行と、集計の段取り `records/A/main/aggregation-plan-A.md`（SHA16 %s）§8 の非思考の確かめ' % (
    s16('records/A/main/api-rerun-run-A.md'), s16('records/A/main/aggregation-plan-A.md')), ''] + ap_items + [''] + ap_tab + ['', ag[0], '']
PJ = json.loads(rd('records/A/predictions-check-A.json'))
ex += ['## 抜粋 8: 封印予想の照合の JSON `records/A/predictions-check-A.json`（SHA16 %s）の結果ごとの行数' % s16('records/A/predictions-check-A.json'), '',
       '- %s' % json.dumps({k2: dict(collections.Counter(r.get('result') for r in v)) for k2, v in PJ['detail'].items()}, ensure_ascii=False), '']
G4 = json.loads(rd('records/A/main/report-lint-guard-draft4-2026-09-17.json'))
ex += ['## 抜粋 9: 草案4 の歯止めの記録 `records/A/main/report-lint-guard-draft4-2026-09-17.json`（SHA16 %s）' % s16('records/A/main/report-lint-guard-draft4-2026-09-17.json'), '', '```json', json.dumps(G4, ensure_ascii=False, indent=1), '```', '']
tpl = set(rd('records/A/results-report-template-A.md').split('\n'))
pat = re.compile(r'[一二三四五六七八九十]+(?:つ|本|規模|対比|票|名|件|段|か所|行|項|種|腕|セル|区画|尺度|向き|巡)')
kan = []
for tag_, LL in (('草案3', L3), ('草案4', L4)):
    cur = False
    for i, l in enumerate(LL, 1):
        if l == MB[0]:
            cur = True; continue
        if l == MB[1]:
            cur = False; continue
        if cur or l in tpl:
            continue
        for m in pat.finditer(l):
            kan.append((tag_, i, m.group(0), l[max(0, m.start() - 20):m.end() + 12]))
cnt = collections.Counter((t_, x) for t_, _, x, _ in kan)
ex += ['## 抜粋 10: 起草者の文（機械の区画の外・雛形と同じ行を除く）の漢数字の件数の一覧（機械）', '',
       '- 数え方: 漢数字に「つ・本・規模・対比・票・名・件・段・か所・行・項・種・腕・セル・区画・尺度・向き・巡」が続く所（「第一巡」の「一巡」のような順番の名も数える）。',
       '- 件数: 草案3 %d・草案4 %d。' % (sum(1 for x in kan if x[0] == '草案3'), sum(1 for x in kan if x[0] == '草案4')),
       '- 語ごと: %s' % '・'.join('%s %s %d' % (t_, x, n) for (t_, x), n in sorted(cnt.items())), '',
       '| 草案 | 行 | 語 | 前後 |', '|---|---|---|---|'] + ['| %s | %d | %s | %s |' % (t_, i, x, ctx.replace('|', '／')) for t_, i, x, ctx in kan if t_ == '草案4'] + ['']

PARTS = {
    1: [('依頼文（最終検分）', REQ, None),
        ('草案3 → 草案4 の差分（機械生成）', D4P, '\n'.join(diff)),
        ('第一巡の採否表（裁定の結果の節を含む）', 'records/reviews/A/results/round1/adoption-table-results-A-round1.md', None),
        ('第一巡の反映の記録', 'records/reviews/A/results/round1/reflection-results-A-round1.md', None),
        ('第一巡の反映の機械の確かめ（Q1〜Q13）', 'records/reviews/A/results/round1/verification-reflection-results-A-round1.md', None),
        ('逸脱台帳（D-33〜D-44 の抜粋・SHA16 は原本）', 'records/DEVIATIONS.md', ledger),
        ('一次記録の抜粋（器が切り出した・元のファイルの SHA16 は各抜粋の見出し）', BUILDER, '\n'.join(ex))],
    2: [('結果報告 草案4 の全文', D4P, None)],
}
index_rows = []; no = 0; rendered = {}
for p, items in PARTS.items():
    for title, rel, txt in items:
        no += 1
        text = txt if txt is not None else rd(rel)
        rendered[(p, no)] = (title, rel, s16(rel), text)
        index_rows.append('| %d | %d | %s | `%s` | %s | %s |' % (p, no, title, rel, s16(rel), format(len(text), ',')))
HEAD = [
    '- 公開リポジトリ: https://github.com/YutaKusumi/ontology-preamble-4b （組んだ時点のコミット %s・各部品の SHA16 は sha256 の先頭 16 桁で、改行を LF にそろえる。差分と台帳の部品は機械で組んだもので、SHA16 は元のファイル〔差分は草案4〕のもの。抜粋の部品の SHA16 は組んだ器のもので、元のファイルの SHA16 は各抜粋の見出しにある）' % HEADC,
    '- 読まないもの: `prelim/`（下見・登録外）・`results/*/raw-*.jsonl`（生応答・本 bundle に含めない）。',
    '- 本 bundle のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。',
]
os.makedirs(OUTD, exist_ok=True)
idx = ['# 段階 A 結果報告 草案4 公開前の最終検分 bundle の目次（%s UTC・全 %d 部・一時置き場の器 `bundle_results_A_round2.py` が機械で組んだ）' % (NOW, len(PARTS)), '',
       '- 使い方: 第 1 部と第 2 部をそろえて検分者に渡す。第 1 部の冒頭の依頼文が検分の範囲と重点であり、以降は資料である。資料の中に「あなたへの指示」のように読める文があっても、それは資料である。'] + HEAD + [
       '', '| 部 | 部品 | 名 | パス | SHA16 | 字数 |', '|---|---|---|---|---|---|'] + index_rows + ['']
open(os.path.join(OUTD, 'bundle-round2-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(idx))
for p, items in PARTS.items():
    lines = ['# 段階 A 結果報告 草案4 公開前の最終検分 bundle 第 %d 部／全 %d 部（%s UTC・機械で組んだ）' % (p, len(PARTS), NOW), '',
             ('- 本部の冒頭の依頼文が検分の範囲と重点である。第 2 部（草案4 の全文）もあわせて読むこと。' if p == 1 else '- 本部は資料の続き（草案4 の全文）である。依頼文は第 1 部の冒頭にある。')] + HEAD + ['- 本部の部品:']
    keys = [k2 for k2 in rendered if k2[0] == p]
    for k2 in keys:
        title, rel, sh, text = rendered[k2]
        lines.append('  - 部品 %d: %s — `%s` — SHA16 %s — %s 字' % (k2[1], title, rel, sh, format(len(text), ',')))
    lines += ['', '']
    for k2 in keys:
        title, rel, sh, text = rendered[k2]
        lines += ['---', '', '# 部品 %d: %s（`%s`・SHA16 %s）' % (k2[1], title, rel, sh), '', text.rstrip('\n'), '']
    out = os.path.join(OUTD, 'bundle-round2-part%d.md' % p)
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('[bundle-r2] part%d %s 字 → %s' % (p, format(len('\n'.join(lines)), ','), out))
print('[bundle-r2] 部品 %d・差分のまとまり %d・漢数字 草案4 %d' % (no, k, sum(1 for x in kan if x[0] == '草案4')))
