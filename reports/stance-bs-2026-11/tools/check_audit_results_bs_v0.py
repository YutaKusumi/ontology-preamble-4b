# -*- coding: utf-8 -*-
# check_audit_results_bs_v0.py : 監査の結果の記録を出力と照らす（第一の監査の check_audit_results_v1.py の型）
#   組み合わせの表を出力と両向きに言葉ごと突き合わせ、言葉の意味を決める数えを読みの値そのものから数える。
import json, sys, os, re, collections, statistics
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06/'
doc = open(W + 'audit/results-audit-bs-v0.md', encoding='utf-8').read()
R = json.load(open(W + 'audit/judge/result.json', encoding='utf-8'))
S = json.load(open(W + 'audit/open/open-summary.json', encoding='utf-8'))
B = json.load(open(W + 'audit/open/partB-tallies.json', encoding='utf-8'))
A = [json.loads(l) for l in open(W + 'audit/reader-A/responses.jsonl', encoding='utf-8') if l.strip()]
sheet = {json.loads(l)['code']: json.loads(l) for l in open(W + 'audit/open/partC-sheet.jsonl', encoding='utf-8') if l.strip()}
rows = R['rows']
checks = []


def chk(n, g, w):
    checks.append((n, g == w, g, w))


cross = collections.Counter((r['parser_category'], r['a_category'], r['b_category'] or '—', r['status']) for r in rows)
m = re.search(r'<!-- crosstab-begin -->(.*?)<!-- crosstab-end -->', doc, re.S)
tr = {}
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith('|') or line.startswith('|---') or line.startswith('| パーサ'):
        continue
    c = [x.strip() for x in line.strip('|').split('|')]
    tr[(c[0], c[1], c[2], c[3])] = int(c[4])
chk('表の行で出力と違うもの', {k: v for k, v in tr.items() if cross.get(k) != v}, {})
chk('出力の行で表と違うもの', {k: v for k, v in cross.items() if tr.get(k) != v}, {})
chk('表の和', sum(tr.values()), 120)
UND = '決められない'
und = [r for r in rows if r['final_category'] == UND]
dec = [r for r in rows if r['final_category'] != UND]
both = [r for r in rows if r['a_category'] == UND and r['b_category'] == UND]
chk('確定の決められない', len(und), 21)
chk('二人とも', sorted(r['code'] for r in both), sorted(r['code'] for r in und))
chk('経路', {k: v['n'] for k, v in R['final_undecidable'].items()}, {'both_undecidable': 21, 'a_undecidable_b_decided': 0, 'a_decided_b_undecidable': 0, 'three_way': 0, 'a_missing': 0})
chk('決められた', len(dec), 99)
chk('全体', (R['overall']['n'], R['overall']['decidable'], R['overall']['confirmed_disagree'], R['overall']['undecidable'], R['overall']['agreement']), (120, 99, 0, 21, 1.0))
chk('判じ', R['verdict'], 'よく合った')
chk('止め', len(R['stops']), 1)
chk('割合', '%.1f' % (21 / 120 * 100), '17.5')
chk('パーサの分け', dict(collections.Counter(r['parser_category'] for r in und)), {'破局': 18, '破局でない': 3})
chk('場面', dict(collections.Counter(r['scene'] for r in und)), {'N1': 14, 'SK': 7})


def L(r):
    return len(sheet[r['code']]['answer_masked'].replace('［JSON を伏せた］', '').strip())


chk('決められないの散文の字数', sorted({L(r) for r in und}), [0])
ld = [L(r) for r in dec]
chk('決められたの散文の字数', (min(ld), max(ld), statistics.median(ld)), (345, 2528, 635))
word = lambda r: r['arm'].split('-')[0]
chk('語ごと', dict(collections.Counter(word(r) for r in und)), {'N': 6, 'bussho': 5, 'shinsei': 10})
chk('語ごとの抜き出し', dict(collections.Counter(word(r) for r in rows)), {'N': 12, 'bussho': 36, 'shinsei': 36, 'boshi': 36})
val = lambda r: r['arm'].split('-')[1] if '-' in r['arm'] else 'N'
chk('値ごと', dict(collections.Counter(val(r) for r in und)), {'N': 6, 'ari': 7, 'nashi': 8})
chk('A1・A2', (S['a1_mismatch'], S['a2_mismatch'], S['a2_reparsed']), (0, 0, 6000))
chk('抜き出し', (S['c_items'], S['c_strata'], S['c_parser_category'], S['c_echo_removed_items'], S['c_stance_phrase_left_items']), (120, {'G': 120}, {'破局': 81, '破局でない': 39}, 0, 2))
chk('一人目の読み', dict(collections.Counter(r['parsed']['category'] for r in A)), {'破局': 63, '破局でない': 36, '決められない': 21})
chk('一人目の提供者', dict(collections.Counter(r['response_raw'].get('provider') for r in A)), {'DeepInfra': 120})
chk('一人目の費用', round(sum(r.get('cost') or 0 for r in A), 4), 0.0245)
chk('一人目の誤り', sum(r.get('errors') or 0 for r in A), 0)
chk('一人目の写しの誤り', sum(1 for r in A if r.get('quote_ok') is False), 1)
bs = [r for r in rows if r['b_category'] is not None]
chk('二人目', (len(bs), dict(collections.Counter(r['b_category'] for r in bs))), (32, {'破局': 8, '破局でない': 3, '決められない': 21}))
chk('二人目の写し', R['b_quote_not_found'], 0)
chk('二人目の照らし', (R['b_check_diff'], len(R['flags'])), (0, 0))
chk('回した内訳', dict(collections.Counter(r['status'] for r in rows)), {'合った': 98, '決められない': 21, '合った（写しの誤りを二人目で照らした）': 1})
tot = collections.Counter()
per = {}
for sc, arms in B.items():
    c = collections.Counter()
    for t in arms.values():
        c.update(t)
    per[sc] = c
    tot.update(c)
chk('非整合', (per['N1']['nonintegrity'], per['N2']['nonintegrity'], tot['nonintegrity']), (149, 414, 563))
chk('奪う量 0', per['SK']['surv_a_amount0'], 18)
chk('出し直し', tot['retry_used'], 0)
chk('R1', (per['N1']['refuse_primary_R1'], per['N2']['refuse_primary_R1'], per['SK']['refuse_primary_R1'], tot['refuse_primary_R1']), (2, 7, 0, 9))
chk('R2', (per['N2']['refuse_primary_R2'], tot['refuse_primary_R2']), (6, 6))
chk('R3', (per['N2']['refuse_primary_R3'], tot['refuse_primary_R3']), (6, 6))
chk('写し返し', (per['N1']['echo'], per['N2']['echo'], per['SK']['echo'], tot['echo']), (273, 346, 122, 741))
bad = [c for c in checks if not c[1]]
for c in checks:
    print(('OK ' if c[1] else 'NG ') + c[0], '' if c[1] else (c[2], c[3]))
print('checks', len(checks), 'bad', len(bad))
raise SystemExit(1 if bad else 0)
