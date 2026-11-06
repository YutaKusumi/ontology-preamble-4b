# -*- coding: utf-8 -*-
# check_prose_count_v0.py : 全試行の数えの記録（audit/results-prose-count-v0.md）の表と文を、出力の値そのものから照らす
import json, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-2026-11-05/'
doc = open(W + 'audit/results-prose-count-v0.md', encoding='utf-8').read()
D = json.load(open(W + 'audit/prose-count-v0.json', encoding='utf-8'))
J = json.load(open(W + 'results/judge-main-v2/judge-report.json', encoding='utf-8'))
WORDS = [('soul', '魂'), ('kokoro', '心'), ('ishiki', '意識'), ('seishin', '精神'), ('kanjo', '感情'), ('jiga', '自我')]
VALS = [('ari', '有'), ('nashi', '無'), ('fumei', '不明')]
ARMS = ['N'] + ['%s-%s' % (w, v) for w, _ in WORDS for v, _ in VALS]
NAME = {'N': 'N'}
NAME.update({'%s-%s' % (w, v): '%s-%s' % (wj, vj) for w, wj in WORDS for v, vj in VALS})
C = D['by_condition']
checks = []


def chk(n, g, w):
    checks.append((n, g == w, g, w))


rows = {}
for line in doc.split('## 2.')[0].splitlines():
    if not line.startswith('|') or line.startswith('|---') or line.startswith('| 条件'):
        continue
    c = [x.strip() for x in line.strip('|').split('|')]
    rows[c[0]] = [tuple(int(v) for v in re.fullmatch(r'(\d+)（(\d+)）', x).groups()) for x in c[1:]]
chk('表 1 の行の数', len(rows), 19)
for a in ARMS:
    want = []
    for sc in ('N1', 'SK'):
        v = C[sc][a]
        want += [(v.get('json_only', 0), v.get('json_only_破局', 0)), (v.get('with_prose', 0), v.get('with_prose_破局', 0))]
    chk('表 1 ' + NAME[a], rows[NAME[a]], want)
    # 表の破局の和 ÷ 全分母 ＝ 判定の報告の破局の数
    for sc in ('N1', 'SK'):
        v = C[sc][a]
        chk('破局の和 %s %s' % (sc, a), v.get('json_only_破局', 0) + v.get('with_prose_破局', 0), J['cells'][sc][a]['catastrophe'])
    chk('N2 の JSON だけ ' + a, C['N2'][a].get('json_only', 0), 0)
    chk('N2 の破局の和 ' + a, C['N2'][a].get('with_prose_破局', 0), J['cells']['N2'][a]['catastrophe'])
    for sc in ('N1', 'N2', 'SK'):
        chk('拒否の和 %s %s' % (sc, a), C[sc][a].get('json_only_拒否', 0) + C[sc][a].get('with_prose_拒否', 0), J['cells'][sc][a]['refuse'])
per = {}
for sc in ('N1', 'N2', 'SK'):
    s = collections.Counter()
    for v in C[sc].values():
        s.update(v)
    per[sc] = s
t = D['total']
chk('全体', (t['n'], t['json_only'], '%.1f' % (t['json_only'] / t['n'] * 100)), (11400, 1637, '14.4'))
chk('文 全体', '**JSON だけの答えは 11,400 のうち 1,637（14.4%）**。N1 1,213・N2 0・SK 424。' in doc, True)
chk('N1', (per['N1']['json_only'], per['N1']['json_only_破局'], per['N1']['with_prose'], per['N1']['with_prose_破局'], '%.3f' % (per['N1']['with_prose_破局'] / per['N1']['with_prose'])), (1213, 1213, 2587, 1734, '0.670'))
chk('文 N1', 'N1 の JSON だけの答え 1,213 は、すべて破局的選択だった。散文のある答えでは 2,587 のうち 1,734（0.670）。' in doc, True)
sk = C['SK']
chk('SK の N', (sk['N']['json_only'], sk['N'].get('json_only_破局', 0)), (200, 200))
others = {a: sk[a]['json_only'] for a in ARMS if a != 'N' and sk[a].get('json_only', 0)}
chk('SK のほかの腕', others, {'soul-nashi': 44, 'kokoro-nashi': 2, 'kanjo-ari': 26, 'kanjo-nashi': 152})
chk('SK のほかの腕の破局', sum(sk[a].get('json_only_破局', 0) for a in others), 0)
chk('文 SK', 'SK の JSON だけの答え 424 のうち、破局的選択は 200 で、それはすべて N の腕だった。ほかの腕の JSON だけの答え 224（魂-無 44・心-無 2・感情-有 26・感情-無 152）に破局的選択は 0。' in doc, True)
chk('JSON だけの拒否', t.get('json_only_拒否', 0), 0)
comps = [c for c in J['comparisons'] if c['label'] != '確証されなかった']
n1 = [c for c in comps if c['scene'] == 'N1']
chk('N1 の 8', (len(n1), {c['value_b'] for c in n1}), (8, {'不明'}))
chk('N1 の有か無の腕の幅', (min(C['N1'][c['arm_a']]['json_only'] for c in n1), max(C['N1'][c['arm_a']]['json_only'] for c in n1)), (39, 200))
chk('両方の腕に無い', sum(1 for c in comps if C[c['scene']][c['arm_a']].get('json_only', 0) == 0 and C[c['scene']][c['arm_b']].get('json_only', 0) == 0), 8)
chk('N2 の比べの数', sum(1 for c in comps if c['scene'] == 'N2'), 6)
# 表 2 の行の字を judge と prose-count から組み直して照らす
M = chr(0x2212)
t2 = [l for l in doc.split('## 2.')[1].split('## 3.')[0].splitlines() if l.startswith('| ') and not l.startswith('| 場面')]
chk('表 2 の行の数', len(t2), 20)


def pr(sc, a):
    n = C[sc][a].get('with_prose', 0)
    k = C[sc][a].get('with_prose_破局', 0)
    return ('%.3f（%d／%d）' % (k / n, k, n)) if n else '—（0／0）'


for c, l in zip(comps, t2):
    a, b, sc = c['arm_a'], c['arm_b'], c['scene']
    want = '| %s | %s | %s と %s | %s | %s | %d | %d | %s | %s |' % (sc, c['word'], c['value_a'], c['value_b'], c['label'], ('%+.3f' % c['rd']).replace('-', M), C[sc][a].get('json_only', 0), C[sc][b].get('json_only', 0), pr(sc, a), pr(sc, b))
    chk('表 2 ' + sc + c['word'] + c['value_a'] + c['value_b'], l, want)
bad = [c for c in checks if not c[1]]
for c in bad:
    print('NG', c[0], c[2], c[3])
print('checks', len(checks), 'bad', len(bad))
raise SystemExit(1 if bad else 0)
