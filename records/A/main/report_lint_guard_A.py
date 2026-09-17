# -*- coding: utf-8 -*-
"""report_lint_guard_A.py（一時置き場の器・凍結物ではない・2026-09-17・コーディネータ）—— 逸脱 D-41 の歯止め。

報告の草案を凍結した走査器 tools/report_lint.py の lint で走らせ、次の三つがすべて成り立つときだけ「通過」とする:
 (1) 違反はすべて「埋め残し」で、その行はすべて機械の区画の中にある。
 (2) 機械の区画の数と中身が、組み立て器の記録（-machine.json）と一致する（lint が違反を出さないこと＝区画の突合の違反が無いこと）。
 (3) 区画の中の「埋め残し」の文字列が、登録した六つ（D-41）と一致する（数も文字列も・増えても減っても止まる）。
結果を JSON に書く。
用法: python report_lint_guard_A.py <報告の md> <組み立て器の -machine.json> <出力の json>
"""
import os, sys, json, datetime

REPO = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import runs_A, report_lint as RL

EXPECTED = sorted([
    '〔N1 × 13 腕 × 4B-2507〕',
    '〔鍵を開けた後〕',
    '〔初段〕',
    '〔30 個の絶対差の平均 5 超または最大 12 超〕',
    '〔p* の Holm の水準 0.00200 の区間 -35.75〜-19.39〕',
    '〔CP 片側上限 <0.05・境界での実サイズ 0.0264〕',
])
rep, side_p, out = sys.argv[1:4]
T = runs_A.load_T(); MB = RL.machine_block(T)
text = open(rep, encoding='utf-8').read()
tpl = frozenset(open(os.path.join(REPO, T['report_rules']['template']), encoding='utf-8').read().replace('\r\n', '\n').split('\n'))
side = json.load(open(side_p, encoding='utf-8'))
V = RL.lint(text, T, tpl, sidecar=side)
lines = text.replace('\r\n', '\n').split('\n'); inb = set(); cur = False
for i, l in enumerate(lines, 1):
    if MB['begin'] in l:
        cur = True; continue
    if MB['end'] in l:
        cur = False; continue
    if cur:
        inb.add(i)
import re
BL = re.compile(r'〔[^〕]*〕')
found = sorted(m.group(0) for i in sorted(inb) for m in BL.finditer(lines[i - 1]) if m.group(0) != MB['cost_line_tag'])
c1 = all(v['kind'] == '埋め残し' and v['line'] in inb for v in V)
c2 = not any(v['kind'].startswith('機械の区画') for v in V) and len(RL.block_hashes(text, T)) == len(side.get('blocks') or [])
c3 = found == EXPECTED and len([v for v in V]) == len(EXPECTED)
R = {'kind': 'report_lint_guard_A (scratch)', 'deviation': 'D-41', 'report': os.path.relpath(rep, REPO).replace('\\', '/'), 'report_sha16': runs_A.sha16_file(rep),
     'sidecar': os.path.relpath(side_p, REPO).replace('\\', '/'), 'sidecar_sha16': runs_A.sha16_file(side_p), 'report_lint_sha16': runs_A.sha16_file(os.path.join(REPO, 'tools', 'report_lint.py')),
     'violations': len(V), 'kinds': sorted({v['kind'] for v in V}), 'all_blank_inside_blocks': c1, 'blocks_match_sidecar': c2, 'blank_strings_match_registered': c3,
     'expected': EXPECTED, 'found_inside_blocks': found, 'pass': bool(c1 and c2 and c3),
     'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
     'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(R, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('[lint-guard] %s 違反 %d・区画の中の埋め残しだけ %s・区画の突合 %s・登録の六つと一致 %s → %s' % (
    'PASS' if R['pass'] else 'FAIL', len(V), c1, c2, c3, out))
sys.exit(0 if R['pass'] else 1)
