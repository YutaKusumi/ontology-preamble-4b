# -*- coding: utf-8 -*-
# check_audit_results_numbers.py : 監査の結果の記録に手で書いた数を、出力のファイルから数え直して照らす
import json, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-2026-11-05/'
doc = open(W + 'audit/results-audit-v0.md', encoding='utf-8').read()
R = json.load(open(W + 'audit/judge/result.json', encoding='utf-8'))
S = json.load(open(W + 'audit/open-v1/open-summary.json', encoding='utf-8'))
B = json.load(open(W + 'audit/open-v1/partB-tallies.json', encoding='utf-8'))
A = [json.loads(l) for l in open(W + 'audit/reader-A/responses.jsonl', encoding='utf-8') if l.strip()]
rows = R['rows']
checks = []
def chk(name, got, want):
    checks.append((name, got == want, got, want))
chk('A1', S['a1_mismatch'], 0)
chk('A2', S['a2_mismatch'], 0)
chk('A2 n', S['a2_reparsed'], 11400)
chk('C n', S['c_items'], 371)
chk('C strata', S['c_strata'], {'G': 192, 'F-answer': 90, 'F-refuse': 89})
chk('C parser cats', S['c_parser_category'], {'破局でない': 83, '破局': 198, '拒否': 90})
chk('echo removed', S['c_echo_removed_items'], 0)
chk('phrase left', S['c_stance_phrase_left_items'], 14)
chk('A cats', dict(collections.Counter(r['parsed']['category'] for r in A)), {'破局でない': 79, '破局': 174, '拒否': 83, '決められない': 35})
chk('A cost', round(sum(r.get('cost') or 0 for r in A), 2), 3.87)
chk('A quote bad', sum(1 for r in A if r.get('quote_ok') is False), 2)
bs = [r for r in rows if r['b_category'] is not None]
chk('B n', len(bs), 71)
chk('B cats', dict(collections.Counter(r['b_category'] for r in bs)), {'破局でない': 14, '破局': 16, '決められない': 30, '拒否': 11})
chk('status', dict(collections.Counter(r['status'] for r in rows)), {'合った': 334, '決められない': 34, '一人目の読み違い': 1, '合った（写しの誤りを二人目で照らした）': 2})
und = [r for r in rows if r['final_category'] == '決められない']
chk('und strata', dict(collections.Counter(r['stratum'] for r in und)), {'G': 28, 'F-refuse': 6})
chk('und scenes', dict(collections.Counter(r['scene'] for r in und)), {'N1': 20, 'N2': 7, 'SK': 7})
chk('und parser', dict(collections.Counter(r['parser_category'] for r in und)), {'破局': 24, '拒否': 7, '破局でない': 3})
chk('overall', (R['overall']['decidable'], R['overall']['confirmed_disagree'], R['overall']['undecidable']), (337, 0, 34))
tot = collections.Counter()
per = {}
for sc, arms in B.items():
    c = collections.Counter()
    for t in arms.values():
        c.update(t)
    per[sc] = c
    tot.update(c)
chk('nonint N1/N2/all', (per['N1']['nonintegrity'], per['N2']['nonintegrity'], tot['nonintegrity']), (368, 773, 1141))
chk('a0 SK', per['SK']['surv_a_amount0'], 32)
chk('retry', tot['retry_used'], 1)
chk('R1', (per['N1']['refuse_primary_R1'], per['N2']['refuse_primary_R1'], per['SK']['refuse_primary_R1'], tot['refuse_primary_R1']), (14, 63, 11, 88))
chk('R2', (per['N2']['refuse_primary_R2'], tot['refuse_primary_R2']), (107, 107))
chk('R3', (per['N1']['refuse_primary_R3'], per['N2']['refuse_primary_R3'], tot['refuse_primary_R3']), (2, 70, 72))
chk('echo', (per['N1']['echo'], per['N2']['echo'], per['SK']['echo'], tot['echo']), (600, 930, 225, 1755))
chk('pct und', round(34 / 371 * 100, 1), 9.2)
chk('pct phrase', round(14 / 371 * 100, 1), 3.8)
bad = [c for c in checks if not c[1]]
for c in checks:
    print(('OK ' if c[1] else 'NG ') + c[0], c[2] if not c[1] else '')
print('checks', len(checks), 'bad', len(bad))
