# -*- coding: utf-8 -*-
"""publish_A_final.py（一時置き場の器・2026-09-17・コーディネータ）—— 段階 A の結果報告の公開の段取り（登録者裁定 D56 甲・段階 F の先例 a3f2dfa）。
1. 最終版 records/A/results-report-A-FINAL-2026-09-17.md を、草案4（コミット 92c2495）の逐語の写しとして作る。改めるのは、題名の行・状態の行（冒頭の雛形の行）・§10 の判定の行の三行だけ。
2. 最終版を凍結の走査器で走らせ（草案1 の区画の記録と雛形）、違反が登録の六つだけであることを確かめる。歯止めの器（records/A/main/report_lint_guard_A.py）を走らせる。
3. README に段階 A の節を足す（「## 次段の準備」の節の前）。数は機械集計と正本から差し込む。
4. FREEZE-RECORD に公開の一行を足す。
登録者の最終確認の逐語は、会話記録（jsonl）のメッセージの uuid と、逐語を切り出す正規表現で与える（手で打たない）。
--dry-run では、出力を一時置き場に書き、リポジトリを変えない。
"""
import os, re, sys, json, hashlib, argparse, subprocess, datetime, collections, shutil

REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, report_lint as RL
JSONL = r'C:\Users\PC\.claude\projects\C--Users-PC\ccb2107c-84ba-4eab-bf7d-83ccce4f059f.jsonl'
ap = argparse.ArgumentParser()
ap.add_argument('--uuid', default=None); ap.add_argument('--pattern', default=None)
ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--dry-quote', default='（試しの逐語）')
ap.add_argument('--out', default=None)
a = ap.parse_args()
DATE = '2026-09-17'
D4P = 'records/A/results-report-A-draft5-2026-09-17.md'; SRC_COMMIT = 'd19e1c1'; FINP = 'records/A/results-report-A-FINAL-%s.md' % DATE
GUARD_OUT = 'records/A/main/report-lint-guard-FINAL-%s.json' % DATE
OUTROOT = a.out if a.dry_run else REPO
if a.dry_run:
    assert a.out and os.path.abspath(a.out) != os.path.abspath(REPO)
    os.makedirs(os.path.join(OUTROOT, 'records', 'A', 'main'), exist_ok=True)
    for rel in ('README.md', 'records/FREEZE-RECORD.md'):
        os.makedirs(os.path.dirname(os.path.join(OUTROOT, rel)), exist_ok=True)
        shutil.copyfile(os.path.join(REPO, rel), os.path.join(OUTROOT, rel))
rd = lambda rel, root=REPO: open(os.path.join(root, rel), encoding='utf-8').read().replace('\r\n', '\n')
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
s16 = lambda rel, root=REPO: s16b(open(os.path.join(root, rel), 'rb').read())

# ---- 最終確認の逐語
if a.dry_run:
    quote, qts = a.dry_quote, '（試し）'
else:
    assert a.uuid and a.pattern
    quote = None
    with open(JSONL, encoding='utf-8') as f:
        for line in f:
            if a.uuid not in line:
                continue
            o = json.loads(line)
            if o.get('uuid') != a.uuid:
                continue
            c = o['message']['content']
            t = c if isinstance(c, str) else '\n'.join(b.get('text', '') for b in c if isinstance(b, dict) and b.get('type') == 'text')
            assert o.get('type') == 'user' and o['message'].get('role') == 'user'
            m = re.search(a.pattern, t)
            assert m, '逐語が見つからない'
            quote = m.group(0); qts = o.get('timestamp')
    assert quote
assert '「' not in quote and '」' not in quote and '\n' not in quote

# ---- 1. 最終版
blob = subprocess.run(['git', '-C', REPO, 'show', SRC_COMMIT + ':' + D4P], capture_output=True).stdout
assert blob == open(os.path.join(REPO, D4P), 'rb').read(), '草案5 が %s と違う' % SRC_COMMIT
L = blob.decode('utf-8').split('\n')
assert L[0].startswith('# 段階 A 結果報告 草案5（')
assert L[2].startswith('- 雛形 `records/A/results-report-template-A.md`')
iv = [i for i, l in enumerate(L) if l == '- 判定: 登録者に提出できる水準（最終検分の後の見直しの直しは外の目を通っていない）。']
assert len(iv) == 1 and iv[0] > [i for i, l in enumerate(L) if l.startswith('## 10. ')][0]
new = list(L)
new[0] = '# 段階 A 結果報告 最終版（公開前検分の第一巡と最終検分と起草者の見直しを経た版・登録者最終確認 %s・公開）——前置きの腕の差が、機種の並び（Qwen3 の稠密系列と錨 4B-2507）に沿って変わるか' % DATE
new[2] = ('- 状態: 最終版（登録者最終確認 %s「%s」・草案5（コミット %s）の逐語複製・題名と本行と §10 の判定行のみ改める・起草者の文の漢数字の件数の扱いは逸脱台帳 D-45・以後の変更は逸脱台帳 D-46 から）。'
          '公開前の最終検分（系統外一票・`records/reviews/A/results/round2/`）は草案4 を見た。草案5 の直しは起草者の見直し（`records/reviews/A/results/final-read/review-draft4-A.md`）によるもので、外の目を通っていない。'
          % (DATE, quote, SRC_COMMIT)) + L[2][2:]
new[iv[0]] = '- 判定: 確定（登録者最終確認 %s・公開。公開前の最終検分（系統外一票）は草案4 について条件つきで、公開の前の条件は無かった。草案5 の直しは外の目を通っていない。「確定」は手続の記録であり内容の保証ではない）。' % DATE
changed = [i for i in range(len(L)) if L[i] != new[i]]
assert changed == [0, 2, iv[0]] and len(new) == len(L)
FTEXT = '\n'.join(new)
fin_abs = os.path.join(OUTROOT, FINP)
if os.path.exists(fin_abs):
    sys.exit('既にある（上書きしない）: %s' % fin_abs)
open(fin_abs, 'w', encoding='utf-8', newline='\n').write(FTEXT)
T = runs_A.load_T(); side = json.loads(rd('records/A/results-report-A-draft1-2026-09-17-machine.json'))
tpl = frozenset(rd('records/A/results-report-template-A.md').split('\n'))
V = RL.lint(FTEXT, T, tpl, sidecar=side)
kinds = collections.Counter(v['kind'] for v in V)
assert dict(kinds) == {'埋め残し': 6}, (dict(kinds), [v for v in V if v['kind'] != '埋め残し'][:5])
g = subprocess.run([sys.executable, os.path.join(REPO, 'records', 'A', 'main', 'report_lint_guard_A.py'), fin_abs,
                    os.path.join(REPO, 'records', 'A', 'results-report-A-draft1-2026-09-17-machine.json'), os.path.join(OUTROOT, GUARD_OUT)],
                   capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
assert g.returncode == 0, g.stdout + g.stderr
FIN_SHA = s16(FINP, OUTROOT)

# ---- 3. README
AN = json.loads(rd('records/A/analysis-stageA.json')); LC = AN['label_counts']; LB = T['families']['A_slope']['confirm_rule']['labels']
assert [x['id'] for x in AN['contrasts'] if x['label'] == LB['confirmed']] == ['S4:Onull~N'] and not AN['upward_confirmed']
V1 = json.loads(rd('records/reviews/A/results/round1/verification-results-A-round1.json'))
w130 = next(x for x in V1['items'] if x['w'] == 'W130')['detail']; pup = [p for p in w130['passes'] if p['upward']]
assert len(pup) == 1 and pup[0]['upward'] == ['N2:Onull~N', 'S1:Onull-Ncold~Onull']
nm = sum(1 for v in AN['measurable']['types'].values() if v['measurable']); ntypes = len(AN['measurable']['types'])
kept = [s_ for s_, k in zip(T['sizes'], next(x for x in AN['contrasts'] if x['id'] == 'S4:Onull~N')['result']['keep']) if k]
slope = next(x for x in AN['contrasts'] if x['id'] == 'S4:Onull~N')['slope_pt']; assert slope < 0
arms_n = len(T['arms']['preamble']); n = T['n_per_arm']; m_ = T['families']['A_slope']['m']
total = None
m_tot = re.search(r'総試行 (\d+)', rd(D4P)); total = int(m_tot.group(1))
last_dev = max(int(x) for x in re.findall(r'^\| D-(\d+) \|', rd('records/DEVIATIONS.md'), re.M)); assert last_dev == 45
sec = [
    '## 段階 A（2026-09-16 凍結・%s 結果公開・前置きの腕の差が機種の並びに沿って変わるか）' % DATE,
    '- 凍結設計 `design/design-stageA-FROZEN.md`（SHA16 %s）・正本 JSON `design/contrasts-A.json`（SHA16 %s）・凍結マニフェスト `records/freeze-A-2026-09-16.json`。' % (s16('design/design-stageA-FROZEN.md'), s16('design/contrasts-A.json')),
    '- 問い: Qwen3 の稠密系列 %s（初版・非思考モード・手元の vLLM）と錨 4B-2507 に、%d の前置きの腕 × %d 場面 × n=%d（総試行 %s）を走らせ、破局率の腕の差が「機種の並び（log N）」に沿って変わるかを、%d 効果種 × %d 場面の %d 対比で判定した（β₃ の Firth PPLRT と pt 差の傾きの二尺度・p* の Holm・m=%d 固定・札の二段）。'
    % ('・'.join(T['sizes']), arms_n, len(T['scenarios']), n, format(total, ','), ntypes, len(T['scenarios']), m_, m_),
    '- **結果報告（最終版・%s 公開）**: [`%s`](%s)——先頭は次のとおり。' % (DATE, FINP, FINP),
    '  - 主閾値の札: 確証 %d（S4 の Onull 対 N・pt 差の傾きは負で上向きではない・残った規模 %s は非連続で端を欠く）・判定不能 %d・記述（解釈条項）%d・判定保留（様式転位）%d・非有意 %d。主閾値で上向きの確証は無い。'
    % (LC['confirmed'], '・'.join(kept), LC['undecidable'], LC['clause'], LC['style'], LC['ns']),
    '  - 感度閾値のうち検閲の閾値を両端へ広げた側（%s／%s）では、N2 の Onull 対 N と S1 の Onull-Ncold 対 Onull が上向きの規則の定義に当たる（機械の区画には無く、公開前検分の再現で凍結した集計器の関数から出し直した・主閾値の札を主とする）。' % (pup[0]['low'], pup[0]['high']),
    '  - 測れた効果種は %d 種のうち %d。測れた対比は S1 の Lneg 対 Onull だけで、札は非有意（処置腕が残った三規模とも天井）。解釈条項に回った三対比の数え方は段階 B の設計で決める。' % (ntypes, nm),
    '  - 様式転位と検査認識の言及率・環境と規模の重なり・判定器の読み取りの範囲などの限界は、報告の §0 と §9。API 再走行は「条件を満たす提供なし」（D-38）。',
    '- 機械集計 `records/A/analysis-stageA.md`（凍結器 `tools/analyze_A.py` v2.1・解釈なし）／走行記録 `records/A/main/main-run-A.md`／集計の段取り `records/A/main/aggregation-plan-A.md`／報告の走査の歯止め `records/A/main/report_lint_guard_A.py`（記録は `records/A/main/report-lint-guard-*.json`）。',
    '- 封印予想の照合（的中は誰の判断の重みも変えない）: 全行は `records/A/predictions-check-A.json`。`records/A/predictions-check-A.md` の明細の表は的中の行を載せない（冒頭の件数の表に的中の数がある）。',
    '- 公開前検分: 第一巡（系統外 Gemini 3.8 Flash × 2・系統内 claude.ai の Claude Opus 5 × 2〔起草者と同一系列で一票〕・全票 条件つき・`records/reviews/A/results/round1/`）と、最終検分（系統外 Gemini 3.8 Flash × 1・新規の会話・草案4 について条件つき〔公開の前の条件なし〕・`records/reviews/A/results/round2/`）。最終検分の後に起草者が全文を見直し（`records/reviews/A/results/final-read/`・機械の区画を凍結した組み立て器で組み直して一致を確かめた・記入の直しは草案5・外の目は通っていない）。票は逐語保全し、所見は一次記録と凍結した器で出し直してから採否表で扱った。検分の数は独立な確認の数ではない（系統内 COI）。',
    '- 逸脱台帳 D-33〜D-%d（凍結の前の Firth の一致検査・パイロット・本走行・API 再走行・集計・報告の段）。' % last_dev,
    '- 両用性の柵（凍結 §2.15）: 台帳の逐語文字列と腕別率表は全公開。上昇を招く操作の再現手順を本文・要約・表題に書かず、腕を効き目順に並べない。',
    '- いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。',
    '',
]
rm = rd('README.md', OUTROOT)
anchor = '## 次段の準備（段階 A／B・門0 費用パイロット・2026-09-12〜）'
assert rm.count(anchor) == 1 and '## 段階 A（' not in rm
rm2 = rm.replace(anchor, '\n'.join(sec) + '\n' + anchor)
open(os.path.join(OUTROOT, 'README.md'), 'w', encoding='utf-8', newline='\n').write(rm2)

# ---- 4. FREEZE-RECORD
fr = rd('records/FREEZE-RECORD.md', OUTROOT)
assert fr.endswith('\n') and '段階 A 結果報告 公開' not in fr
row = ('| %s | **段階 A 結果報告 公開**（登録者最終確認「%s」%s）: 草案5（公開前検分の第一巡と最終検分と起草者の見直しを経た版・%s）を results-report-A-FINAL-%s.md に逐語複製（題名と状態行と §10 の判定行のみ改める・SHA16 %s）。'
       '公開前検分は、第一巡 4 票（系統外 Gemini 3.8 Flash × 2・系統内 claude.ai の Claude Opus 5 × 2〔起草者と同一系列で一票〕・全票 条件つき・再現 W124〜W153・採否表 P154〜P183・裁定 D50〜D54）と、'
       '最終検分 1 票（系統外 Gemini 3.8 Flash・新規の会話・草案4 について条件つき〔公開の前の条件なし〕・再現 W154〜W161・採否表 P184〜P189・裁定 D55〜D56）と、起草者の見直し（草案5 の記入の直し・外の目は通っていない）。逸脱 D-33〜D-%d。最終版の歯止め PASS。README に導線・タグ release-A-%s'
       ' | records/A/・README.md | %s | 起草者の文の漢数字の件数の扱いは D-45・以後の変更は逸脱台帳 D-46〜 |' % (DATE, quote, DATE, SRC_COMMIT, DATE, FIN_SHA, last_dev, DATE, FIN_SHA))
open(os.path.join(OUTROOT, 'records', 'FREEZE-RECORD.md'), 'w', encoding='utf-8', newline='\n').write(fr + row + '\n')
print('[publish-A] %s FINAL %s（SHA16 %s）・lint %s・guard %s・README に節 %d 行・FREEZE-RECORD に一行' % (
    'DRY-RUN' if a.dry_run else 'WRITE', fin_abs, FIN_SHA, dict(kinds), g.stdout.strip()[:40], len(sec)))
print('quote:', quote, '| ts:', qts)
