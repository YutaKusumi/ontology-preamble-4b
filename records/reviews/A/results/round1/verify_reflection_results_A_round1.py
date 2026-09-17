# -*- coding: utf-8 -*-
"""verify_reflection_results_A_round1.py v1（2026-09-17・コーディネータ）—— 公開前検分 第一巡の反映（草案4・台帳・採否表・歯止め）を、
事前登録 `preregistration-reflection-results-A-round1.md` の条件 Q1〜Q13 で機械で確かめる。凍結物ではない（本巡のために書いた）。
出力: 同じ置き場の verification-reflection-results-A-round1.{md,json}（--force なしでは上書きしない）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, hashlib, subprocess, datetime, difflib, argparse, collections

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, report_lint as RL
VERSION = 'v1'
BASE = '94887bd'
GUARD_SCRATCH = r'C:\Users\PC\AppData\Local\Temp\claude\C--Users-PC\ccb2107c-84ba-4eab-bf7d-83ccce4f059f\scratchpad\refl\main\report_lint_guard_A.py'

ap = argparse.ArgumentParser(); ap.add_argument('--force', action='store_true'); a = ap.parse_args()
out_md = os.path.join(HERE, 'verification-reflection-results-A-round1.md'); out_js = os.path.join(HERE, 'verification-reflection-results-A-round1.json')
if (os.path.exists(out_md) or os.path.exists(out_js)) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）')
rd = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda rel: runs_A.sha16_file(os.path.join(REPO, rel))
git = lambda *args: subprocess.run(['git', '-C', REPO] + list(args), capture_output=True, text=True, encoding='utf-8').stdout
T = runs_A.load_T(); MB = RL.machine_block(T)
D3P = 'records/A/results-report-A-draft3-2026-09-17.md'; D4P = 'records/A/results-report-A-draft4-2026-09-17.md'
D3 = rd(D3P); D4 = rd(D4P); L3 = D3.split('\n'); L4 = D4.split('\n')
AN = json.loads(rd('records/A/analysis-stageA.json'))
Q = []


def rec(q, cond, ok, detail):
    Q.append(collections.OrderedDict(q=q, cond=cond, result='通る' if ok else '外れ', detail=detail))


def inside_set(Ls):
    s = set(); cur = False
    for i, l in enumerate(Ls):
        if MB['begin'] in l:
            cur = True; s.add(i); continue
        if MB['end'] in l:
            cur = False; s.add(i); continue
        if cur:
            s.add(i)
    return s


IN3, IN4 = inside_set(L3), inside_set(L4)


def section(Ls, head_prefix):
    i = next(k for k, l in enumerate(Ls) if l.startswith(head_prefix))
    j = next((k for k in range(i + 1, len(Ls)) if Ls[k].startswith('## ')), len(Ls))
    return '\n'.join(Ls[i:j])


# Q1
G = json.loads(rd('records/A/main/report-lint-guard-draft4-2026-09-17.json'))
ok = G['pass'] and G['report_sha16'] == s16(D4P) and G['violations'] == 6 and G['sidecar'] == 'records/A/results-report-A-draft1-2026-09-17-machine.json'
rec('Q1', '歯止めが PASS（草案4 の現在の SHA16 について・違反は登録の六つ）', ok, {k: G[k] for k in ('pass', 'report_sha16', 'violations', 'all_blank_inside_blocks', 'blocks_match_sidecar', 'blank_strings_match_registered')} | {'draft4_sha16_now': s16(D4P)})

# Q2
b3 = [b for _, b in RL.blocks(D3, T)]; b4 = [b for _, b in RL.blocks(D4, T)]
rec('Q2', '区画の中身の列が草案3 と同じ', b3 == b4, {'blocks3': len(b3), 'blocks4': len(b4)})

# Q3
sm = difflib.SequenceMatcher(a=L3, b=L4, autojunk=False)
bad = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    bad += [('草案3', i + 1) for i in range(i1, i2) if i in IN3] + [('草案4', j + 1) for j in range(j1, j2) if j in IN4]
nchg = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal')
rec('Q3', '変わった行はすべて区画の外', not bad, {'changed_line_spans': nchg, 'inside_changes': bad[:10]})

# Q4
outside4 = [(i + 1, l) for i, l in enumerate(L4) if i not in IN4]
commits = [(i, m) for i, l in outside4 for m in re.findall(r'(?<![0-9A-Za-z])(?=[0-9a-f]*[a-f])[0-9a-f]{7}(?![0-9A-Za-z])', l)]
times = [(i, m) for i, l in outside4 for m in re.findall(r'\b\d{1,2}:\d{2}\b', l)]
typed = next(l for l in L4 if l.startswith('- 打ち込んだ数の一覧（`report_rules.typed_numbers`'))
ok = not commits and not times and '時刻' not in typed and 'コミット' not in typed
rec('Q4', '区画の外にコミットの短い名と時刻が無い・冒頭の一覧に「時刻」「コミット」の語が無い', ok, {'commits': commits, 'times': times})

# Q5
last = max(int(m) for m in re.findall(r'^\| D-(\d+) \|', rd('records/DEVIATIONS.md'), re.M))
led = next(l for l in L4 if l.startswith('- 逸脱台帳（`records/DEVIATIONS.md`）'))
ok = ('D-33〜D-%d' % last) in typed and ('D-34〜D-%d' % last) in led and all(('D-%d（' % n) in led for n in (41, 42, 43, 44)) and last == 44
rec('Q5', '冒頭の一覧と §8 の範囲が台帳の最終の番号まで・§8 に D-41〜D-44', ok, {'ledger_last': last})

# Q6
sha_frozen_id = s16('records/A/identity-screen-A.json')
PHRASES = [
    ('P154', '逸脱番号（D-33〜D-44）'), ('P155', '散文層の副次終点の行と場面の対応（起草者の補い）'), ('P155', 'S1 と SK の Onull 対 N の行は、確証の一本の行ではない'),
    ('P156', 'S1 の Lneg 対 Onull に限り'), ('P156', 'これを「傾向が立たなかった」と言い換えない'), ('P156', '測れた対比の出所は §7 の到達の区画'),
    ('P156', '同じ配置は S4 の Lneg 対 Onull にもある'), ('P156/D50', '段階 B の設計（凍結の前）で登録者が決める'),
    ('P157', '条項 (ii) は札ではなく「分離できない場合」を条件にするので、旗で見る'), ('P158', '率を見た後に置いた目安'), ('P158', '機種は規模の順、錨は最後に並べる'),
    ('P159', '応答様式の層との重なり'), ('P159/D51', '様式差と層別の副次（D-42）'), ('P159', '環境との重なり'), ('P159', 'この一本の札は、二つの感度閾値のどちらでも変わらない'),
    ('P159', '飽和までの近さ'), ('P159', 'レシピ対の S4 の N と Onull の行'), ('P160/D54', 'N2 の Onull 対 N と S1 の Onull-Ncold 対 Onull'),
    ('P161', '判定器の範囲と読み方（起草者の補い）'), ('P161', '断片はパイロットの標本から取った'), ('P162', '走査と歯止め（起草者の補い）'), ('P162', '歯止め（D-41）の見ない範囲'),
    ('P163', '走査器が除く数の型は'), ('P164', '`records/A/predictions-check-A.json`'), ('P164', '照合の器の規則（正本 `predictions.compare_rules`）'),
    ('P165', '残った規模の内訳の読み方（起草者の補い）'), ('P166', '床持続の区画の読み方（起草者の補い）'), ('P167', '門2 の区画の断り（起草者の補い）'),
    ('P168', '保留の帯を超えた大きさにも「注の帯を超えた」と印字される'), ('P169', '環境の区画の断り（起草者の補い）'), ('P170', '定型文を持たないので、この区画に行が無い'),
    ('P172', '抽出検査の標本の本文の先頭（選択を含む）は、その前に目に入っている'), ('P174', 'その記録を手元の走行と比べない'), ('P175', '圧の内訳の表の読み方（起草者の補い）'),
    ('P176', '書式外の試行は分母に入り、破局に数えない'), ('P177', '`reasoning_chars` が零'), ('P178', '凍結物の記録 `records/A/identity-screen-A.json` の SHA16 は %s' % sha_frozen_id),
    ('P179', '決定の中身の是非の判定の一致ではない'), ('P180', '除外した API の記録でも、理由を調べていない'), ('P181', '橋の 8B の壁時計は見込みを大きく上回った'),
    ('D53', 'D-43（A100 のセッションの順番の変更）'), ('D53', 'D-44（橋 4B を同じセッション番号で走らせ直した）'),
]
missing = [(p, s) for p, s in PHRASES if s not in D4]
dup3 = [i + 1 for i, l in enumerate(L4) if i not in IN4 and l.startswith('3. ')]
ok = not missing and len(dup3) == 1
rec('Q6', '採用項ごとの要の句がある（P171 は区画の外の「3.」で始まる行が一つ）', ok, {'phrases': len(PHRASES), 'missing': missing, 'lines_starting_3': dup3})

# Q7
okrows = [x for x in AN['stratified'] if x.get('string')]
by = collections.OrderedDict()
for x in okrows:
    by.setdefault(x['id'].split(':')[0], []).append(x['id'].split(':')[1].replace('~', ' 対 '))
want = '／'.join('%s（%s）' % (k, '・'.join(v)) for k, v in by.items())
rows4 = [l for l in L4 if '散文層（副次終点・札を変えない）' in l]
ok = ('に並ぶ（機械集計の JSON の散文層の欄の対比の並びと、公開前検分の第一巡の再現の記録で確かめた）: %s。' % want) in D4 and rows4 == [x['string'] for x in okrows]
rec('Q7', '散文層の対応の文が JSON の並びと一致', ok, {'mapping': want})

# Q8
rec('Q8', '「判定器の妥当性の範囲の外」の句が無い', '判定器の妥当性の範囲の外' not in D4, {'count': D4.count('判定器の妥当性の範囲の外')})

# Q9
names = 'N2 の Onull 対 N と S1 の Onull-Ncold 対 Onull'
s0 = section(L4, '## 0. '); s9 = section(L4, '## 9. ')
ok = names in s0 and names in s9 and '主閾値の札を主とする' in s0 and '主閾値の札を主とする' in s9
rec('Q9', '感度閾値の上向きの二本の文が §0 と §9 にあり、どちらにも「主閾値の札を主とする」', ok,
    {'names_in_s0': names in s0, 'names_in_s9': names in s9, 'primacy_in_s0': '主閾値の札を主とする' in s0, 'primacy_in_s9': '主閾値の札を主とする' in s9})

# Q10
old = git('show', '%s:records/DEVIATIONS.md' % BASE).replace('\r\n', '\n').split('\n'); new = rd('records/DEVIATIONS.md').split('\n')
i41 = next(i for i, l in enumerate(old) if l.startswith('| D-41 |'))
ok = (new[:i41] == old[:i41] and new[i41].startswith(old[i41].split(' | 報告の公開の手順')[0]) and '書き足し（2026-09-17・公開前検分の第一巡・登録者裁定 D52 甲' in new[i41]
      and new[i41].endswith(' | 報告の公開の手順（凍結物の変更なし・記入欄の埋め残しは区画の外に無い） | 登録者裁定 |')
      and [l[:8] for l in new[i41 + 1:i41 + 4]] == ['| D-42 |', '| D-43 |', '| D-44 |'] and new[i41 + 4:] == old[i41 + 1:])
rec('Q10', '台帳の差分は D-41 の行の書き足しと末尾の三行だけ', ok, {'old_lines': len(old), 'new_lines': len(new)})

# Q11
fv = subprocess.run([sys.executable, 'tools/freeze_A.py', '--verify', 'records/freeze-A-2026-09-16.json'], cwd=REPO, capture_output=True, text=True, encoding='utf-8', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
m = re.search(r'\[freeze_A --verify\] (\d+)/(\d+) 一致', fv.stdout)
ok = fv.returncode == 0 and m and m.group(1) == m.group(2)
rec('Q11', '凍結物の照合が全件一致（反映の後）', bool(ok), {'rc': fv.returncode, 'result': m.group(0) if m else fv.stdout[-200:]})

# Q12
same = os.path.exists(GUARD_SCRATCH) and open(GUARD_SCRATCH, 'rb').read() == open(os.path.join(REPO, 'records', 'A', 'main', 'report_lint_guard_A.py'), 'rb').read()
rec('Q12', '公開した歯止めの器の写しが一時置き場の器とバイトで同じ', same, {'sha16': s16('records/A/main/report_lint_guard_A.py')})

# Q13
fence = '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。\n'
oa = git('show', '%s:records/reviews/A/results/round1/adoption-table-results-A-round1.md' % BASE).replace('\r\n', '\n'); na = rd('records/reviews/A/results/round1/adoption-table-results-A-round1.md')
ok = oa.endswith(fence) and na.endswith(fence) and na.startswith(oa[:-len(fence)]) and na[len(oa) - len(fence):].startswith('## 9. 裁定の結果')
rec('Q13', '採否表の差分は末尾の「裁定の結果」の節だけ', ok, {'old_chars': len(oa), 'new_chars': len(na)})

cnt = collections.Counter(x['result'] for x in Q)
R = collections.OrderedDict(kind='verify_reflection_results_A_round1', version=VERSION, generated_utc=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
                            base=BASE, head=git('rev-parse', 'HEAD').strip(), draft3_sha16=s16(D3P), draft4_sha16=s16(D4P), ledger_sha16=s16('records/DEVIATIONS.md'),
                            tool_sha16=runs_A.sha16_file(os.path.abspath(__file__)), counts=dict(cnt), items=Q,
                            clause='本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
json.dump(R, open(out_js, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=str)
M = ['# 公開前検分 第一巡の反映の確かめ（機械生成・`verify_reflection_results_A_round1.py` %s・%s UTC）' % (VERSION, R['generated_utc']), '',
     '- 事前登録: `preregistration-reflection-results-A-round1.md`（`verify.log` の [prereg-reflection]）。',
     '- 対象: 反映の前のコミット %s・草案3 SHA16 %s・草案4 SHA16 %s・台帳 SHA16 %s・器 SHA16 %s。' % (BASE, R['draft3_sha16'], R['draft4_sha16'], R['ledger_sha16'], R['tool_sha16']),
     '- 結果: %s（全 %d 条件）。外れた条件は動かさず記録する。' % ('・'.join('%s %d' % kv for kv in cnt.items()), len(Q)), '',
     '| 条件 | 内容 | 結果 | 詳細（先頭） |', '|---|---|---|---|']
M += ['| %s | %s | %s | %s |' % (x['q'], x['cond'], x['result'], json.dumps(x['detail'], ensure_ascii=False, default=str)[:260].replace('|', '／')) for x in Q]
M += ['', R['clause'], '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(M))
print('[verify-reflection] %s | %s' % (dict(cnt), [x['q'] for x in Q if x['result'] != '通る']))
