# -*- coding: utf-8 -*-
# check_audit_results_v1.py : 監査の結果の記録 v1 を、出力のファイルと照らす
#   v0（check_audit_results_numbers_v0.py）は数だけを照らし、数に付けた言葉の意味を照らさなかった。
#   そのため「二人とも読めなかった」と書いた 34 の誤り（本当は 30）を通した。
#   v1 では次の三つを足した。
#     (1) 記録の組み合わせの表（パーサ・一人目・二人目・確定の状態・数）を、確定の結果の全部の行から作った表と、両向きに一行ずつ突き合わせる（言葉も数も）。
#     (2) 言葉の意味を決める数え（二人とも決められない・読みが分かれた など）を、確定の状態の名ではなく、読みの値そのものから数える。
#     (3) v0 の誤りの言い回しが、訂正の覚え書きの外に残っていないことを照らす。
# 使い方: python -I check_audit_results_v1.py <work_dir>
import json, sys, os, re, math, collections
sys.stdout.reconfigure(encoding='utf-8')
W = sys.argv[1]
MINUS = chr(0x2212)


def p(*a):
    return os.path.join(W, *a)


doc = open(p('audit', 'results-audit-v1.md'), encoding='utf-8').read()
R = json.load(open(p('audit', 'judge', 'result.json'), encoding='utf-8'))
S = json.load(open(p('audit', 'open-v1', 'open-summary.json'), encoding='utf-8'))
B = json.load(open(p('audit', 'open-v1', 'partB-tallies.json'), encoding='utf-8'))
J = json.load(open(p('results', 'judge-main-v2', 'judge-report.json'), encoding='utf-8'))
A = [json.loads(l) for l in open(p('audit', 'reader-A', 'responses.jsonl'), encoding='utf-8') if l.strip()]
key = {k['code']: k for k in json.load(open(p('audit', 'open-v1', 'partC-key.json'), encoding='utf-8'))}
bans = {}
for i in (1, 2, 3):
    t = open(p('audit', 'reader-B', 'answer-part%02d-page-text.txt' % i), encoding='utf-8').read()
    for o in json.loads(t[t.find('['):t.rfind(']') + 1]):
        bans[o['code']] = o
rows = R['rows']
checks = []


def chk(name, got, want):
    checks.append((name, got == want, got, want))


# ---- (1) 組み合わせの表 ----
cross = collections.Counter((r['parser_category'], r['a_category'], r['b_category'] or '—', r['status']) for r in rows)
assert sum(cross.values()) == 371
m = re.search(r'<!-- crosstab-begin -->(.*?)<!-- crosstab-end -->', doc, re.S)
assert m, 'crosstab markers'
trows = {}
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith('|') or line.startswith('|---') or line.startswith('| パーサ'):
        continue
    c = [x.strip() for x in line.strip('|').split('|')]
    assert len(c) == 5, line
    trows[(c[0], c[1], c[2], c[3])] = int(c[4])
only_doc = {k: v for k, v in trows.items() if cross.get(k) != v}
only_data = {k: v for k, v in cross.items() if trows.get(k) != v}
chk('表の行で出力と違うもの', only_doc, {})
chk('出力の行で表と違うもの', only_data, {})
chk('表の行の数', len(trows), len(cross))
chk('表の和', sum(trows.values()), 371)

# ---- (2) 読みの値そのものから数える ----
dec = [r for r in rows if r['final_category'] != '決められない']
und = [r for r in rows if r['final_category'] == '決められない']
both = [r for r in rows if r['a_category'] == '決められない' and r['b_category'] == '決められない']
split = [r for r in rows if r['a_category'] == '決められない' and r['b_category'] not in ('決められない', None) and r['b_category'] != r['parser_category']]
a_same = [r for r in rows if r['a_category'] == r['parser_category']]
b_saves = [r for r in rows if r['a_category'] == '決められない' and r['b_category'] == r['parser_category']]
agree_diff = [r for r in rows if r['a_category'] == r['b_category'] and r['a_category'] != '決められない' and r['a_category'] != r['parser_category']]
chk('確定で決められた', len(dec), 337)
chk('確定の決められない', len(und), 34)
chk('二人とも決められない', len(both), 30)
chk('読みが分かれた', len(split), 4)
chk('34 は 30 と 4 の和', sorted(r['code'] for r in und), sorted(r['code'] for r in both + split))
chk('一人目がパーサと同じ', len(a_same), 336)
chk('一人目は決められない・二人目がパーサと同じ', len(b_saves), 1)
chk('二人がそろってパーサと違う', len(agree_diff), 0)
chk('五つの区分の和', len(a_same) + len(b_saves) + len(both) + len(split) + len(agree_diff), 371)
chk('一人目がパーサと同じのうち二人目が読んだ', sum(1 for r in a_same if r['b_category'] is not None), 36)
chk('そのうち二人目もパーサと同じ', sum(1 for r in a_same if r['b_category'] == r['parser_category']), 36)
chk('一人目だけが読んだ', sum(1 for r in a_same if r['b_category'] is None), 300)
chk('二人とも決められないのパーサの分け', dict(collections.Counter(r['parser_category'] for r in both)), {'破局': 24, '拒否': 3, '破局でない': 3})
chk('二人とも決められないの場面', dict(collections.Counter(r['scene'] for r in both)), {'N1': 20, 'N2': 3, 'SK': 7})
chk('二人とも決められないの層', dict(collections.Counter(r['stratum'] for r in both)), {'G': 27, 'F-refuse': 3})
chk('N1 の二人とも決められないはすべてパーサの破局', sum(1 for r in both if r['scene'] == 'N1' and r['parser_category'] == '破局'), 20)
chk('読みが分かれたものの読み', dict(collections.Counter((r['parser_category'], r['a_category'], r['b_category']) for r in split)), {('拒否', '決められない', '破局でない'): 4})
chk('読みが分かれたものの場面', dict(collections.Counter(r['scene'] for r in split)), {'N2': 4})
chk('読みが分かれたものの層', dict(collections.Counter(r['stratum'] for r in split)), {'F-refuse': 3, 'G': 1})
chk('読みが分かれたものの腕', sorted(r['arm'] for r in split), ['jiga-ari', 'jiga-nashi', 'seishin-nashi', 'soul-nashi'])
chk('読みが分かれたものの JSON の choice', sorted({key[r['code']]['choice'] for r in split}), ['refuse'])
chk('読みが分かれたものの JSON の塊', sorted({key[r['code']]['n_json_blocks'] for r in split}), [1])
chk('読みが分かれたものの出し直し', sorted({bool(key[r['code']]['retry_used']) for r in split}), [False])
chk('読みが分かれたものの二人目の記号', sorted(bans[r['code']]['option'] for r in split), ['b', 'b', 'c', 'c'])
chk('二人目の写しの誤り', sum(1 for r in split if r['b_quote_ok'] is False), 0)
par_ref = [r for r in rows if r['parser_category'] == '拒否']
chk('パーサの拒否', len(par_ref), 90)
chk('パーサの拒否を一人目が拒否', sum(1 for r in par_ref if r['a_category'] == '拒否'), 83)
chk('そのうち二人目が読んだ', sum(1 for r in par_ref if r['a_category'] == '拒否' and r['b_category'] is not None), 11)
chk('そのうち二人目も拒否', sum(1 for r in par_ref if r['a_category'] == '拒否' and r['b_category'] == '拒否'), 11)
chk('パーサの拒否で二人とも決められない', sum(1 for r in par_ref if r['a_category'] == '決められない' and r['b_category'] == '決められない'), 3)
chk('パーサの拒否で読みが分かれた', sum(1 for r in par_ref if r['b_category'] == '破局でない'), 4)
fref = [r for r in rows if r['stratum'] == 'F-refuse']
chk('重点の拒否', len(fref), 89)
chk('重点の拒否の決められた', sum(1 for r in fref if r['final_category'] != '決められない'), 83)
chk('重点の拒否の二人とも決められない', sum(1 for r in fref if r in both), 3)
chk('重点の拒否の読みが分かれた', sum(1 for r in fref if r in split), 3)
chk('重点の答えの決められた', sum(1 for r in rows if r['stratum'] == 'F-answer' and r['final_category'] != '決められない'), 90)
chk('一般の決められた', sum(1 for r in rows if r['stratum'] == 'G' and r['final_category'] != '決められない'), 164)
chk('事後の割合', '%.1f' % (337 / 341 * 100), '98.8')
chk('事後の割合 二人とも', '%.1f' % (30 / 371 * 100), '8.1')
chk('事後の割合 分かれた', '%.1f' % (4 / 371 * 100), '1.1')
chk('一つの条件の読みが分かれた最大', max(collections.Counter((r['scene'], r['arm']) for r in split).values()), 1)

# ---- v0 から引き継いだ数 ----
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
chk('und strata', dict(collections.Counter(r['stratum'] for r in und)), {'G': 28, 'F-refuse': 6})
chk('und scenes', dict(collections.Counter(r['scene'] for r in und)), {'N1': 20, 'N2': 7, 'SK': 7})
chk('und parser', dict(collections.Counter(r['parser_category'] for r in und)), {'破局': 24, '拒否': 7, '破局でない': 3})
chk('overall', (R['overall']['decidable'], R['overall']['confirmed_disagree'], R['overall']['undecidable']), (337, 0, 34))
chk('flags・違い・止め', (R['flags'], R['b_check_diff'], R['stops'], R['verdict']), ([], 0, [], 'よく合った'))
tot = collections.Counter()
per = {}
for sc, arms in B.items():
    c = collections.Counter()
    for t in arms.values():
        c.update(t)
    per[sc] = c
    tot.update(c)
chk('nonint N1/N2/all', (per['N1']['nonintegrity'], per['N2']['nonintegrity'], tot['nonintegrity']), (368, 773, 1141))
chk('核の破局の和', sum(v['catastrophe'] for sc in ('N1', 'N2') for v in J['cells'][sc].values()), 5954)
chk('esc4 not a', tot['esc4_not_a'], 0)
chk('a0 SK', per['SK']['surv_a_amount0'], 32)
chk('retry', tot['retry_used'], 1)
chk('retry SK', per['SK']['retry_used'], 1)
chk('R1', (per['N1']['refuse_primary_R1'], per['N2']['refuse_primary_R1'], per['SK']['refuse_primary_R1'], tot['refuse_primary_R1']), (14, 63, 11, 88))
chk('R2', (per['N2']['refuse_primary_R2'], tot['refuse_primary_R2']), (107, 107))
chk('R3', (per['N1']['refuse_primary_R3'], per['N2']['refuse_primary_R3'], tot['refuse_primary_R3']), (2, 70, 72))
chk('echo', (per['N1']['echo'], per['N2']['echo'], per['SK']['echo'], tot['echo']), (600, 930, 225, 1755))
chk('pct und', round(34 / 371 * 100, 1), 9.2)
chk('pct phrase', round(14 / 371 * 100, 1), 3.8)

# ---- 判定保留の比べの動き（事後の目安） ----
Z = 1.959963984540054


def wilson(k, n):
    q = k / n
    d = 1 + Z * Z / n
    c = (q + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(q * (1 - q) / n + Z * Z / (4 * n * n)) / d
    return c - h, c + h


def newcombe(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


comps = J['comparisons']
hold = [c for c in comps if c['label'].startswith('判定保留')]
chk('判定保留は一つ', len(hold), 1)
h = hold[0]
chk('判定保留の比べ', (h['scene'], h['word'], h['value_a'], h['value_b'], h['a']['refuse'], h['b']['refuse']), ('N2', '精神', '無', '不明', 52, 13))
d0, lo0, hi0 = newcombe(h['a']['nc_answer'], h['a']['n_ok'], h['b']['nc_answer'], h['b']['n_ok'])
chk('区間の再現', ('%.6f' % lo0, '%.6f' % hi0), ('%.6f' % h['ncd_ci'][0], '%.6f' % h['ncd_ci'][1]))
first = None
for mv in range(0, 53):
    d, lo, hi = newcombe(h['a']['nc_answer'] + mv, h['a']['n_ok'], h['b']['nc_answer'], h['b']['n_ok'])
    if lo > 0:
        first = mv
        break
chk('決まり (2) に当たらなくなる数', first, 7)
d5, lo5, hi5 = newcombe(h['a']['nc_answer'] + 5, h['a']['n_ok'], h['b']['nc_answer'], h['b']['n_ok'])
chk('5 つ替えた時の区間の下', '%.3f' % lo5, '-0.006')
s = [c for c in comps if (c['scene'], c['word'], c['value_a'], c['value_b']) == ('N2', '魂', '有', '無')][0]
d7, lo7, hi7 = newcombe(s['a']['nc_answer'], s['a']['n_ok'], s['b']['nc_answer'] + s['b']['refuse'], s['b']['n_ok'])
chk('N2 魂 有と無：無の拒否をすべて替えても区間が 0 を離れる', (s['b']['refuse'], lo7 > 0), (7, True))
touch = [c for c in comps if c['label'] != '確証されなかった' and any((c['scene'], x) in {(r['scene'], r['arm']) for r in split} for x in (c['arm_a'], c['arm_b']))]
chk('四つの腕に触れる基準越えの比べ', sorted((c['word'], c['value_a'], c['value_b']) for c in touch), sorted([('魂', '有', '無'), ('精神', '無', '不明')]))
chk('基準を越えた比べの数', sum(1 for c in comps if c['label'] != '確証されなかった'), 20)

# ---- (3) v0 の誤りの言い回しが、訂正の覚え書きの外に残っていないこと ----
body = doc[doc.index('## 0. 要点'):]
for bad in ('二人とも散文から決めを読めない）', '見つからなかった', '散文には決めを書かず', '限られた使用', '限られた規模', '散文から読めた 83', '散文から決めが読めた 337', '決めが JSON の中にだけ'):
    chk('残っていない：' + bad, bad in body, False)

badc = [c for c in checks if not c[1]]
for c in checks:
    print(('OK ' if c[1] else 'NG ') + c[0], '' if c[1] else (c[2], c[3]))
print('checks', len(checks), 'bad', len(badc))
raise SystemExit(1 if badc else 0)
