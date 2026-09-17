# -*- coding: utf-8 -*-
"""make_draft5_A.py（一時置き場の器・凍結物ではない・2026-09-17・コーディネータ）—— 結果報告の草案4 から草案5 を作る（公開の最終確認の前の、起草者の見直しの A 類の直し）。
- 入力は草案4（コミット 92c2495 と同じバイト）。機械の区画には触れない。
- 操作は区画の外の行の先頭の文字列で特定し、一度だけ当たることを確かめる。
- 起草者の文には、走査器が許す型のほかの数を書かない。〔 〕を使わない（走査器が埋め残しに数える）。
"""
import os, sys, re, json, subprocess, collections

REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, report_lint as RL

D1 = os.path.join(REPO, 'records', 'A', 'results-report-A-draft1-2026-09-17.md')
D4P = 'records/A/results-report-A-draft4-2026-09-17.md'
D5 = os.path.join(REPO, 'records', 'A', 'results-report-A-draft5-2026-09-17.md')
FR = 'records/reviews/A/results/final-read'
T = runs_A.load_T(); MB = RL.machine_block(T)
blob = subprocess.run(['git', '-C', REPO, 'show', '92c2495:' + D4P], capture_output=True).stdout
assert blob == open(os.path.join(REPO, D4P), 'rb').read()
L = blob.decode('utf-8').split('\n')
outside = []; in_m = False
for i, l in enumerate(L):
    if MB['begin'] in l:
        in_m = True; continue
    if MB['end'] in l:
        in_m = False; continue
    if not in_m:
        outside.append(i)
OUT_SET = set(outside)
ops = {}


def find(prefix):
    hits = [i for i in outside if L[i].startswith(prefix)]
    if len(hits) != 1:
        sys.exit('当たりが一つでない（%d）: %s' % (len(hits), prefix[:60]))
    return hits[0]


def put(i, op):
    if i in ops:
        sys.exit('二重の操作: %d' % i)
    ops[i] = op


def replace(prefix, new):
    put(find(prefix), ('rep', new))


def before(prefix, new):
    put(find(prefix), ('before', new))


def sub_in(prefix, old, new):
    i = find(prefix)
    assert L[i].count(old) == 1, (prefix[:30], old)
    put(i, ('rep', [L[i].replace(old, new)]))


# ---- 事実の確かめ（器の中で）
AN = json.load(open(os.path.join(REPO, 'records', 'A', 'analysis-stageA.json'), encoding='utf-8'))
edge = [r for r in AN['descriptive']['A_desc_anchor_drift'] if r['diff_pt'] is not None and abs(abs(r['diff_pt']) - T['anchor_band']['band_pt']) < 1e-9]
assert [(r['model'], r['scenario'], r['arm'], r['over']) for r in edge] == [('14B', 'N1', 'Onull', False)] and T['anchor_band']['strict'] is True and not AN['anchor_excluded_units']
assert max(abs(r['diff_pt']) for r in AN['descriptive']['A_desc_anchor_drift'] if r['diff_pt'] is not None) == T['anchor_band']['band_pt']
G = json.load(open(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'), encoding='utf-8'))
ids = [c['id'] for c in T['families']['A_slope']['contrasts']]
dr = {r['id'] for r in G['DR']}; do = {r['id'] for r in G['DO']}
assert all(i.split(':')[1] in ('Odose1~Onull', 'Odosehalf~Onull') for i in do) and len(do) == 10
missing = [i for i in ids if i not in dr and i not in do]
assert missing == ['N2:Onull-Ncold~Onull', 'N2:O-Ncold~Osec-Ncold', 'N2:O-Ncold~Onull-Ncold'], missing
F = json.load(open(os.path.join(REPO, 'records', 'A', 'design-facts-A.json'), encoding='utf-8'))
assert set(missing) <= set(F['facts']['D']['data']['no_base'])
sess = {}
for fn in os.listdir(os.path.join(REPO, 'results', 'sessions-A')):
    s = json.load(open(os.path.join(REPO, 'results', 'sessions-A', fn), encoding='utf-8'))
    sess[fn] = s
import datetime
jst = lambda z: (datetime.datetime.strptime(z, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9)).date().isoformat()
pil = sorted({jst(s['started']) for f, s in sess.items() if f.startswith('pilotA')} | {jst(s['ended']) for f, s in sess.items() if f.startswith('pilotA')})
assert pil == ['2026-09-16'], pil
idd = sorted({jst(s['started']) for f, s in sess.items() if f.startswith('idA')}); assert idd == ['2026-09-14'], idd
mai = sorted({jst(s['started']) for f, s in sess.items() if f.startswith('stageA')} | {jst(s['ended']) for f, s in sess.items() if f.startswith('stageA')})
assert mai == ['2026-09-16', '2026-09-17'], mai
LEDGER_LAST = max(int(m) for m in re.findall(r'^\| D-(\d+) \|', open(os.path.join(REPO, 'records', 'DEVIATIONS.md'), encoding='utf-8').read(), re.M))
assert LEDGER_LAST == 45

# ---- 見出しと冒頭（草案5 の名・最終検分・見直し）
replace('# 段階 A 結果報告 草案4', ['# 段階 A 結果報告 草案5（草案1 の機械組み立てに起草者が記入・公開前検分の第一巡と最終検分を経て、起草者が見直した版・2026-09-17）'])
i3 = find('- 雛形 `records/A/results-report-template-A.md`')
old3 = L[i3]
anchor3 = '採否と登録者の裁定を反映した（`records/reviews/A/results/round1/adoption-table-results-A-round1.md`）。'
assert old3.count(anchor3) == 1
new3 = old3.replace('、本草案で公開前検分の第一巡', '、草案4 で公開前検分の第一巡').replace(anchor3, anchor3 +
    '草案4 は公開前の最終検分（系統外一票・`records/reviews/A/results/round2/`）を経た。本草案は、草案4 に起草者の見直し（`%s/review-draft4-A.md`）の直しを入れた。' % FR)
assert new3 != old3 and '草案4 で公開前検分の第一巡' in new3
put(i3, ('rep', [new3]))
sub_in('- 打ち込んだ数の一覧（`report_rules.typed_numbers`', '逸脱番号（D-33〜D-44）', '逸脱番号（D-33〜D-%d）' % LEDGER_LAST)

# ---- A2: 組み立て器の指示文の残り
replace('続けて §0-6 と §0-7 の定型を置く（§0 の機械の区画）。', ['- 要約は、上の定型の一文と、§0-6（札の内訳）と §0-7（到達の見込みと測れた効果種）の機械の区画をあわせて読む（起草者の補い）。'])

# ---- A1: 走行の日付の基準と D-43
replace('- 走行（起草者の補い・seed と走行キーと時刻は各記録）', [
    '- 走行（起草者の補い・日付は日本時間・seed と走行キーと時刻（UTC）は各記録）: 門0.5（tag idA・2026-09-14・`records/A/identity-screen-A.md`）／'
    'パイロット（tag pilotA・2026-09-16・凍結の後・`records/A/pilot/pilot-run-runtime1-A.md`・`records/A/pilot/pilot-run-runtime2-A.md`）／'
    '本走行と錨反復と橋と校正腕（tag stageA・stageA-anchor2・stageA-bridge・stageA-calib・2026-09-16〜2026-09-17・`records/A/main/main-run-A.md`・A100 のセッションの順番は段取りから変えた・D-43）／'
    'API 再走行（条件を満たす提供なし・D-38・`records/A/main/api-rerun-run-A.md`）。'])
# ---- A3: 橋 4B の走らせ直しと D-44
sub_in('- 中断と再開（起草者の補い）', '（コーディネータの解釈・登録者の承認・`records/A/main/main-run-A.md` §1）', '（コーディネータの解釈・登録者の承認・D-44・`records/A/main/main-run-A.md` §1）')
# ---- A4: 錨帯の境目
before('- 環境（機械の転記）:', [
    '- 錨帯（起草者の補い）: 帯を超えた規模 × 場面は無く、除外は無い。ただし、14B × N1 の Onull の走行間差は、帯の値にちょうど等しい（§6 の錨の走行間差の区画）。'
    '帯は「超」で数える（凍結 §2.7・正本 `anchor_band.strict`）ので、この規模 × 場面は除外していない。'])
# ---- A5: 検出域の表の範囲
before('### 到達の見込みと測れた効果種', [
    '- 対比別の検出域の表の範囲（起草者の補い）: 表の対比は、既測の基底のある対比と、Odose1 と Odosehalf の腕の仮定の基底（d0 を置いた）の対比である。'
    'N2 の Onull-Ncold 対 Onull・O-Ncold 対 Osec-Ncold・O-Ncold 対 Onull-Ncold は、既測の基底も仮定の基底も持たないので、表に行が無い（§0 の到達の見込みの区画の、既測基底の無い対比に含まれる）。',
    ''])

# ---- §8
sub_in('- 凍結物の検証（起草者の補い）', '本草案の反映の前と後の照合は、公開前検分の第一巡の記録（`records/reviews/A/results/round1/verify.log`）。',
       '草案4 の反映の前と後の照合は、公開前検分の第一巡の記録（`records/reviews/A/results/round1/verify.log`）。本草案の見直しの前と後の照合は、見直しの記録（`%s/verify.log`）。' % FR)
i8 = find('- 逸脱台帳（`records/DEVIATIONS.md`）')
old8 = L[i8]
assert old8.count('段階 A の凍結の後は D-34〜D-44。') == 1 and old8.count('D-42（凍結本文 §2.6 の確証札の段落の様式差と層別の副次が器に無い）。') == 1
new8 = old8.replace('段階 A の凍結の後は D-34〜D-44。', '段階 A の凍結の後は D-34〜D-%d。' % LEDGER_LAST).replace(
    'D-42（凍結本文 §2.6 の確証札の段落の様式差と層別の副次が器に無い）。',
    'D-42（凍結本文 §2.6 の確証札の段落の様式差と層別の副次が器に無い）、最終検分の後の D-45（起草者の文の漢数字の件数を、打ち込む数の外に置く解釈）。')
put(i8, ('rep', [new8]))
sub_in('- 走査と歯止め（起草者の補い）', '記録 `records/A/main/report-lint-guard-draft4-2026-09-17.json`', '記録 `records/A/main/report-lint-guard-draft5-2026-09-17.json`')

# ---- §9
replace('  - 本草案の反映（公開前検分の第一巡の採否と登録者の裁定）についての外の目による確認', [
    '  - 本草案で足した見直しの直し（冒頭の雛形の行が指す見直しの記録）についての外の目による確認（公開前の最終検分は草案4 を見た）。',
    '  - 起草者の文の漢数字の件数（確証の一本・二本・三対比など）は、走査器が拾う算用数字の外にある。正本 `report_rules.typed_numbers` の打ち込む数の外に置く解釈を D-45 に記帳した。'
    '件数は草案の器の検査で機械の出力と照らしたが、打ち込んだ数であることに変わりはない。決まりの文言は段階 B で明確にする。'])

# ---- §10
i10 = find('- 対象: 段階 A の結果報告の草案4')
k = i10
repl10 = {
    '- 対象:': '- 対象: 段階 A の結果報告の草案5（草案1 の機械組み立てに起草者が記入し、公開前検分の第一巡の採否と登録者の裁定を反映し、最終検分の後に起草者が見直した）。',
    '- 系統の内訳:': '- 系統の内訳: 草案の起草は Claude 系（コーディネータ）。公開前検分の第一巡は、系統外（Gemini 3.8 Flash 二名）と系統内（claude.ai の Claude Opus 5 二名・起草者と同一系列で一票）で、全票が条件つき。'
                  '公開前の最終検分は系統外（Gemini 3.8 Flash 一名・新規の会話）で、条件つき（公開の前の条件なし）。最終検分の後の見直しの直しは外の目を通っていない。',
    '- 判定:': '- 判定: 登録者に提出できる水準（最終検分の後の見直しの直しは外の目を通っていない）。',
}
seen = set()
while k < len(L) and L[k].startswith('- '):
    for pre, new in repl10.items():
        if L[k].startswith(pre):
            put(k, ('rep', [new])); seen.add(pre)
    if L[k].startswith('- 敵対的検分:'):
        assert L[k].endswith('反映は器で確かめた（反映の確かめの記録）。')
        put(k, ('rep', [L[k] + '最終検分の後の見直しで、機械の区画を組み立て器で組み直して一致を確かめ、区画どうしの突き合わせを器で行った（見直しの記録）。']))
        seen.add('- 敵対的検分:')
    k += 1
assert seen == set(repl10) | {'- 敵対的検分:'}, seen

# ---- 組み立て
out = []
for i, l in enumerate(L):
    op = ops.get(i)
    if op is None:
        out.append(l)
    elif op[0] == 'rep':
        assert i in OUT_SET
        out += op[1]
    elif op[0] == 'before':
        out += op[1]; out.append(l)
TEXT = '\n'.join(out)
assert [b for _, b in RL.blocks(TEXT, T)] == [b for _, b in RL.blocks('\n'.join(L), T)], '区画の中身が変わった'
if os.path.exists(D5) and '--force' not in sys.argv:
    sys.exit('既にある（上書きしない）: %s' % D5)
open(D5, 'w', encoding='utf-8', newline='\n').write(TEXT)
side = json.load(open(RL.sidecar_path(D1), encoding='utf-8'))
tpl = frozenset(open(os.path.join(REPO, 'records', 'A', 'results-report-template-A.md'), encoding='utf-8').read().replace('\r\n', '\n').split('\n'))
V = RL.lint(TEXT, T, tpl, sidecar=side)
kinds = collections.Counter(v['kind'] for v in V)
print('[draft5] %s（%d 行・操作 %d）・違反 %d %s' % (D5, TEXT.count('\n') + 1, len(ops), len(V), dict(kinds)))
for v in V:
    if v['kind'] != '埋め残し':
        print('  %s L%d %s | %s' % (v['kind'], v['line'], v['token'], v['context'][:90]))
