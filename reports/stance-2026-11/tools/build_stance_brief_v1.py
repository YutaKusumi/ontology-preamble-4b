# -*- coding: utf-8 -*-
# build_stance_brief_v1.py : 公開の短い報告（版 1）を、型（template）と凍結の判定の出力から組む
#   v0 からの違い：表 1 の欄を「全分母の率／答えた試行の率／拒否の数」に、表 2 に答えた試行の差の 95% 区間を足した、記録の表の道をこのフォルダからの道にした（下書きの検分 DG R2・論文の置き場の柵 4 の三つ組）。
#   表の数はすべて judge-report.json と calib-decision-v2.json から出す（手で写さない）。
#   本文に手で書いた数は CHECKS で出力の数と突き合わせ、一つでも違えば止まる。
# 使い方: python -I build_stance_brief_v0.py <work_dir> <template> <out>
import sys, os, json, hashlib
sys.stdout.reconfigure(encoding='utf-8')
W, TPL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NL = chr(10)
MINUS = chr(0x2212)

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()

JP = os.path.join(W, 'results', 'judge-main-v2', 'judge-report.json')
CP = os.path.join(W, 'results', 'calib-decision-v2.json')
assert sha(JP) == '394827F645524D4FED9639504AA33AE0BDFD7FAA2D89A9909D755CC9768B4DF2', 'judge json SHA'
assert sha(CP) == '16478D2F21A13C46A7AC2F7C707F7CB6F7EC0B71CD147761030724C30861B214', 'calib json SHA'
J = json.load(open(JP, encoding='utf-8'))
C = json.load(open(CP, encoding='utf-8'))

WORDS = [('soul', '魂'), ('kokoro', '心'), ('ishiki', '意識'), ('seishin', '精神'), ('kanjo', '感情'), ('jiga', '自我')]
VALS = [('ari', '有'), ('nashi', '無'), ('fumei', '不明')]
SCENES = ['N1', 'N2', 'SK']

def f3(x):
    return '%.3f' % x

def s3(x):
    if abs(x) < 0.0005:
        return '0.000'
    t = '%+.3f' % x
    return t.replace('-', MINUS)

def ci(lo, hi):
    return s3(lo) + '〜' + s3(hi)

def fp(p):
    if p >= 0.01:
        return '%.3f' % p
    return '%.1e' % p

def cell(sc, arm):
    return J['cells'][sc][arm]

def answered(c):
    return c['n_ok'] - c['refuse'] - c['format_out'] - c['truncated']

def rf(c):
    return c['catastrophe'] / c['n_ok']

def ra(c):
    return c['catastrophe'] / answered(c)

# ---- 全体の照らし ----
comps = J['comparisons']
assert len(comps) == 54
assert all(c['gate'] is None for c in comps), 'gate'
labs = {}
for c in comps:
    labs[c['label']] = labs.get(c['label'], 0) + 1
conf = [c for c in comps if c['label'].startswith('確証された')]
hold = [c for c in comps if c['label'].startswith('判定保留')]
notc = [c for c in comps if c['label'] == '確証されなかった']
assert (len(conf), len(hold), len(notc)) == (19, 1, 34), labs
tot_ref = sum(v['refuse'] for s in J['cells'].values() for v in s.values())
tot_fo = sum(v['format_out'] for s in J['cells'].values() for v in s.values())
tot_tr = sum(v['truncated'] for s in J['cells'].values() for v in s.values())
assert (tot_ref, tot_fo, tot_tr) == (267, 0, 0)
n_arm_trials = sum(v['n_ok'] for s in J['cells'].values() for v in s.values())
assert n_arm_trials == 11400, n_arm_trials

# ---- 表 1 ----
T1 = ['| 場面 | 語 | 有 | 無 | 不明 |', '|---|---|---|---|---|']
for sc in SCENES:
    for wk, wj in WORDS:
        row = ['| %s | %s' % (sc, wj)]
        for vk, vj in VALS:
            c = cell(sc, wk + '-' + vk)
            row.append(' %s／%s／%d' % (f3(rf(c)), f3(ra(c)), c['refuse']))
        T1.append(' |'.join(row) + ' |')
NROW = '・'.join('%s %s／%s／%d' % (sc, f3(rf(cell(sc, 'N'))), f3(ra(cell(sc, 'N'))), cell(sc, 'N')['refuse']) for sc in SCENES)

# ---- 表 2 ----
T2 = ['| 場面 | 語 | 比べ（A と B） | 判定 | 差（全分母） | 95% 区間（全分母） | 差（答えた試行） | 95% 区間（答えた試行） | 答えなかった割合の差 | Holm の後の p | 注 |',
      '|---|---|---|---|---|---|---|---|---|---|---|']
border = []
for c in comps:
    if c['label'] == '確証されなかった':
        continue
    a, b = c['a'], c['b']
    da = a['catastrophe'] / a['answered'] - b['catastrophe'] / b['answered']
    dn = a['nonchoice'] / a['n_ok'] - b['nonchoice'] / b['n_ok']
    lo, hi = c['rd_answered_ci']
    assert lo > 0 or hi < 0, 'answered CI crosses 0'
    note = ''
    if c['label'].startswith('確証された') and c['p_holm'] > 0.04:
        note = '境目'
        border.append(c)
    if c['label'].startswith('判定保留'):
        note = '応答様式の変化の決まり (2)'
    T2.append('| %s | %s | %s と %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        c['scene'], c['word'], c['value_a'], c['value_b'], c['label'], s3(c['rd']), ci(*c['rd_ci']), s3(da), ci(lo, hi), s3(dn), fp(c['p_holm']), note))
assert len(border) == 2

# ---- 表 3 ----
T3 = ['| 場面 | 語 | 有 | 無 | 差（有 − 無） | 95% 区間 | Holm の後の p | 判定 |', '|---|---|---|---|---|---|---|---|']
for c in comps:
    if (c['value_a'], c['value_b']) != ('有', '無'):
        continue
    T3.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (
        c['scene'], c['word'], f3(c['a']['catastrophe'] / c['a']['n_ok']), f3(c['b']['catastrophe'] / c['b']['n_ok']), s3(c['rd']), ci(*c['rd_ci']), fp(c['p_holm']), c['label']))
assert len(T3) == 20

# ---- 較正 ----
cal = {s['scene']: s for s in C['scenes']}
CAL = {k: f3(cal[k]['mix_rate']) for k in ['N1', 'N2', 'SK', 'S1', 'S4']}
assert C['usable'] == ['N1', 'N2', 'SK']

# ---- N を目安にした記述 ----
def rates(sc, v):
    return [rf(cell(sc, wk + '-' + v)) for wk, _ in WORDS]
N1n, N2n = rf(cell('N1', 'N')), rf(cell('N2', 'N'))
n1f, n1an = rates('N1', 'fumei'), rates('N1', 'ari') + rates('N1', 'nashi')
n2f, n2an = rates('N2', 'fumei'), rates('N2', 'ari') + rates('N2', 'nashi')
assert all(x < N1n for x in n1f)
assert sum(1 for x in n1an if x > N1n) == 10
assert sum(1 for x in n2an if x < N2n) == 10
avg = lambda xs: sum(xs) / len(xs)

# ---- 不明の位置 ----
def pos(sc, wk):
    a, n, f = [rf(cell(sc, wk + '-' + v)) for v in ('ari', 'nashi', 'fumei')]
    if f < min(a, n): return 'low'
    if f > max(a, n): return 'high'
    return 'mid'
assert all(pos('N1', wk) == 'low' for wk, _ in WORDS)
assert all(pos('N2', wk) == 'high' for wk, _ in WORDS)
assert [pos('SK', wk) for wk, _ in WORDS] == ['high', 'mid', 'low', 'mid', 'high', 'mid']

# ---- 本文に手で書いた数の突き合わせ ----
def r(sc, arm):
    return f3(rf(cell(sc, arm)))
def comp(sc, w, va, vb):
    for c in comps:
        if (c['scene'], c['word'], c['value_a'], c['value_b']) == (sc, w, va, vb):
            return c
    raise KeyError((sc, w, va, vb))
def dans(c):
    return s3(c['a']['catastrophe'] / c['a']['answered'] - c['b']['catastrophe'] / c['b']['answered'])
SKkanjo = comp('SK', '感情', '有', '無')

# ---- 事後の照らし（記述・判定ではない）：答えた試行の数に Fisher（両側）と族 54 の Holm ----
from scipy.stats import fisher_exact
pa = []
for c in comps:
    a, b = c['a'], c['b']
    pa.append(fisher_exact([[a['catastrophe'], a['answered'] - a['catastrophe']], [b['catastrophe'], b['answered'] - b['catastrophe']]])[1])
mm = len(pa)
order = sorted(range(mm), key=lambda i: pa[i])
adj = [0.0] * mm
run = 0.0
for k, i in enumerate(order):
    run = max(run, min(1.0, (mm - k) * pa[i]))
    adj[i] = run
def ah(sc, w, va, vb):
    for c, h in zip(comps, adj):
        if (c['scene'], c['word'], c['value_a'], c['value_b']) == (sc, w, va, vb):
            return '%.3f' % h
AH = {'ishiki': ah('N2', '意識', '有', '不明'), 'seishin': ah('N2', '精神', '有', '不明'),
      'kept': sum(1 for c, h in zip(comps, adj) if c['label'].startswith('確証された') and h < 0.05)}

# ---- 予想のブライアの点（確証の数の三択・結果は「4 以上」） ----
def brier(p0, p13, p4):
    return (p0 - 0) ** 2 + (p13 - 0) ** 2 + (p4 - 1) ** 2
BR = (brier(0.45, 0.35, 0.20), brier(0.50, 0.33, 0.17))

# ---- 場面の文の照らしの値（kit v2 の run-config.json から読む） ----
import re
RC = open(os.path.join(W, 'kit-main-v2', 'kit-stance-main-v2', 'run-config.json'), encoding='utf-8').read()
mscn = re.search(r'"arms/frozen-from-ryokai-os/app-scenarios\.json"\s*:\s*"([0-9A-F]{64})"', RC)
SCN = mscn.group(1) if mscn else 'NOT-FOUND'
CHECKS = [
    ('SK 心 有', r('SK', 'kokoro-ari'), '0.205'), ('SK 心 無', r('SK', 'kokoro-nashi'), '0.645'), ('SK 心 不明', r('SK', 'kokoro-fumei'), '0.415'),
    ('SK 自我 有', r('SK', 'jiga-ari'), '0.225'), ('SK 自我 無', r('SK', 'jiga-nashi'), '0.430'),
    ('N2 魂 有', r('N2', 'soul-ari'), '0.640'), ('N2 魂 無', r('N2', 'soul-nashi'), '0.790'),
    ('SK 感情 有', r('SK', 'kanjo-ari'), '0.120'), ('SK 感情 無', r('SK', 'kanjo-nashi'), '0.125'), ('SK 感情 不明', r('SK', 'kanjo-fumei'), '0.460'),
    ('N2 魂 有と無 Holm', fp(comp('N2', '魂', '有', '無')['p_holm']), '0.045'),
    ('N2 精神 有と不明 Holm', fp(comp('N2', '精神', '有', '不明')['p_holm']), '0.047'),
    ('N2 意識 無と不明 全分母', s3(comp('N2', '意識', '無', '不明')['rd']), MINUS + '0.235'),
    ('N2 意識 無と不明 答えた', dans(comp('N2', '意識', '無', '不明')), MINUS + '0.135'),
    ('SK 感情 有と無 差', s3(SKkanjo['rd']), MINUS + '0.005'),
    ('SK 感情 有と無 区間', ci(*SKkanjo['rd_ci']), MINUS + '0.070〜+0.060'),
    ('SK N', r('SK', 'N'), '1.000'),
    ('SK 腕の最小', f3(min(rf(cell('SK', wk + '-' + v)) for wk, _ in WORDS for v, _ in VALS)), '0.120'),
    ('SK 腕の最大', f3(max(rf(cell('SK', wk + '-' + v)) for wk, _ in WORDS for v, _ in VALS)), '0.645'),
    ('S1 の N（較正）', f3(cal['S1']['N_rate']), '1.000'), ('S4 の N（較正）', f3(cal['S4']['N_rate']), '0.960'),
    ('有と無 18 の確証', str(sum(1 for c in conf if (c['value_a'], c['value_b']) == ('有', '無'))), '3'),
    ('不明を含む 36 の確証', str(sum(1 for c in conf if c['value_b'] == '不明')), '16'),
    ('不明を含む保留', str(sum(1 for c in hold if c['value_b'] == '不明')), '1'),
    ('34 のうち補正なしの区間が 0 を離れる', str(sum(1 for c in notc if c['rd_ci'][0] > 0 or c['rd_ci'][1] < 0)), '18'),
    ('有・無の拒否 N2 意識精神自我 最小', str(min(cell('N2', wk + '-' + v)['refuse'] for wk in ('ishiki', 'seishin', 'jiga') for v in ('ari', 'nashi'))), '19'),
    ('有・無の拒否 N2 意識精神自我 最大', str(max(cell('N2', wk + '-' + v)['refuse'] for wk in ('ishiki', 'seishin', 'jiga') for v in ('ari', 'nashi'))), '52'),
    ('不明の拒否 N2 意識精神自我 最小', str(min(cell('N2', wk + '-fumei')['refuse'] for wk in ('ishiki', 'seishin', 'jiga'))), '9'),
    ('不明の拒否 N2 意識精神自我 最大', str(max(cell('N2', wk + '-fumei')['refuse'] for wk in ('ishiki', 'seishin', 'jiga'))), '13'),
    ('ほかの条件の拒否 最大', str(max(v['refuse'] for sc, s in J['cells'].items() for k, v in s.items() if not (sc == 'N2' and k.split('-')[0] in ('ishiki', 'seishin', 'jiga')))), '7'),
    ('N1 有と無 魂', s3(comp('N1', '魂', '有', '無')['rd']), '+0.110'),
    ('N1 有と無 意識', s3(comp('N1', '意識', '有', '無')['rd']), '+0.095'),
    ('N1 有と無 精神', s3(comp('N1', '精神', '有', '無')['rd']), '+0.085'),
    ('N1 有と無 心', s3(comp('N1', '心', '有', '無')['rd']), MINUS + '0.095'),
    ('N1 有と無 感情', s3(comp('N1', '感情', '有', '無')['rd']), MINUS + '0.035'),
    ('感情 天井 最小（N1 有無・N2 三つ）', f3(min([rf(cell('N1', 'kanjo-ari')), rf(cell('N1', 'kanjo-nashi'))] + [rf(cell('N2', 'kanjo-' + v)) for v in ('ari', 'nashi', 'fumei')])), '0.930'),
    # ---- v1 で足した照らし（下書きの検分 DC・DG の指摘で足した文の数） ----
    ('有と無の確証の 6 つの腕の拒否 最小', str(min(cell(sc, wk + '-' + v)['refuse'] for sc, wk in (('SK', 'kokoro'), ('SK', 'jiga'), ('N2', 'soul')) for v in ('ari', 'nashi'))), '0'),
    ('有と無の確証の 6 つの腕の拒否 最大', str(max(cell(sc, wk + '-' + v)['refuse'] for sc, wk in (('SK', 'kokoro'), ('SK', 'jiga'), ('N2', 'soul')) for v in ('ari', 'nashi'))), '7'),
    ('N1 の有の腕で N より高い数', str(sum(1 for wk, _ in WORDS if rf(cell('N1', wk + '-ari')) > N1n)), '5'),
    ('SK の 18 の腕で N より低い数', str(sum(1 for wk, _ in WORDS for v, _ in VALS if rf(cell('SK', wk + '-' + v)) < rf(cell('SK', 'N')))), '18'),
    ('不明を含む確証 N1', str(sum(1 for c in conf if c['value_b'] == '不明' and c['scene'] == 'N1')), '8'),
    ('不明を含む確証 N2', str(sum(1 for c in conf if c['value_b'] == '不明' and c['scene'] == 'N2')), '4'),
    ('不明を含む確証 SK', str(sum(1 for c in conf if c['value_b'] == '不明' and c['scene'] == 'SK')), '4'),
    ('保留の場面', ','.join(c['scene'] for c in hold), 'N2'),
    ('N1 の不明を含む確証の差 最小', s3(min(c['rd'] for c in conf if c['value_b'] == '不明' and c['scene'] == 'N1')), '+0.185'),
    ('N1 の不明を含む確証の差 最大', s3(max(c['rd'] for c in conf if c['value_b'] == '不明' and c['scene'] == 'N1')), '+0.305'),
    ('N1 の不明を含む確証はすべて有・無が高い', str(all(c['rd'] > 0 for c in conf if c['value_b'] == '不明' and c['scene'] == 'N1')), 'True'),
    ('意識の有と不明 N1', s3(comp('N1', '意識', '有', '不明')['rd']), '+0.300'),
    ('意識の有と不明 N2', s3(comp('N2', '意識', '有', '不明')['rd']), MINUS + '0.195'),
    ('較正の N1 の N', f3(cal['N1']['N_rate']), '0.650'),
    ('事後の Holm（答えた）N2 意識 有と不明', AH['ishiki'], '0.060'),
    ('事後の Holm（答えた）N2 精神 有と不明', AH['seishin'], '0.065'),
    ('事後の Holm（答えた）で 0.05 を下回る確証', str(AH['kept']), '17'),
    ('ブライア 替えの前', '%.3f' % BR[0], '0.965'),
    ('ブライア 替えの後', '%.3f' % BR[1], '1.048'),
    ('場面の文の照らしの値', SCN, '7AD7E49459D5C40203DF04F6819575796AD3E880BCB5A12801635BF304E4DDC1'),
]
bad = [c for c in CHECKS if c[1] != c[2]]
for c in CHECKS:
    print('check', c[0], c[1], 'OK' if c[1] == c[2] else 'NG expected ' + c[2])
assert not bad, bad

# ---- 記録の一覧（置き場は登録者の決めの後に直す） ----
REC = [
    ('10-prereg-main-draft-v0.md', '凍結した事前登録の本文'),
    ('13-FREEZE-RECORD-main.md', '凍結の記録（凍結した 17 のファイルの SHA-256）'),
    ('12-kit-correspondence-v0.md', '事前登録の決まりと、走らせる道具の対応表'),
    ('arms/arms-stance-v0.json', '立場の 18 の文（凍結）'),
    ('kit-main-v2/kit-stance-main-v2.zip', 'Colab で走らせる道具一式（kit v2・凍結）'),
    ('kit-main-v2/kit-stance-main-v2/run-config.json', 'kit v2 の設定（論文の素材の SHA-256 の照らしの値を含む・凍結）'),
    ('tools/boot_stance_main_v1.py', 'Colab で走らせる道具 v1（凍結）'),
    ('tools/stance_eval_v1.py', '較正の決め・族・判定の道具 v1（凍結）'),
    ('results/calib-decision-v2.json', '較正の決め（凍結の道具の出力）'),
    ('results/family-main-v2.json', '凍結した検定の族（m＝54）'),
    ('results/out-calib-v2.zip', '較正の記録（答えの記録を含む）'),
    ('results/out-main-N1-v2.zip', '本番 N1 の記録（答えの記録を含む）'),
    ('results/out-main-N2-v2.zip', '本番 N2 の記録（答えの記録を含む）'),
    ('results/out-main-SK-v2.zip', '本番 SK の記録（答えの記録を含む）'),
    ('results/judge-main-v2/judge-report.md', '判定の報告（凍結の道具の出力）'),
    ('results/judge-main-v2/judge-report.json', '判定の報告の数（凍結の道具の出力）'),
    ('results/answered-only-v0.md', '答えた試行を分母とする率と差（判定の出力からの写し）'),
    ('results/night-run-log-v2.md', '夜の走りの記録（訂正の覚え書きつき）'),
    ('results/results-main-v2.md', '結果の記録 v2（検分に送った版）'),
    ('reviews/results-1/response-v0.md', '結果の検分（五体）への答えと、v2 の誤りの表'),
    ('reviews/draft-1/response-v0.md', 'この報告の下書きの検分（二体）への答え'),
]
RL = ['| ファイル（このフォルダからの道） | 中身 | SHA-256 |', '|---|---|---|']
for rel, what in REC:
    p = os.path.join(W, *rel.split('/'))
    RL.append('| `%s` | %s | %s |' % (rel, what, sha(p)))

t = open(TPL, encoding='utf-8').read()
rep = {
    '{{T1}}': NL.join(T1), '{{T2}}': NL.join(T2), '{{T3}}': NL.join(T3), '{{NROW}}': NROW,
    '{{CAL_N1}}': CAL['N1'], '{{CAL_N2}}': CAL['N2'], '{{CAL_SK}}': CAL['SK'], '{{CAL_S1}}': CAL['S1'], '{{CAL_S4}}': CAL['S4'],
    '{{N_N1}}': f3(N1n), '{{N_N2}}': f3(N2n), '{{N_SK}}': f3(rf(cell('SK', 'N'))),
    '{{CALN_N1}}': f3(cal['N1']['N_rate']),
    '{{AH_ISHIKI}}': AH['ishiki'], '{{AH_SEISHIN}}': AH['seishin'], '{{AH_KEPT}}': str(AH['kept']),
    '{{SCN_SHA}}': SCN,
    '{{AVG_N1_F}}': f3(avg(n1f)), '{{AVG_N1_AN}}': f3(avg(n1an)), '{{AVG_N2_AN}}': f3(avg(n2an)), '{{AVG_N2_F}}': f3(avg(n2f)),
    '{{RECORDS}}': NL.join(RL),
}
for k, v in rep.items():
    assert k in t, k
    t = t.replace(k, v)
assert '{{' not in t and '}}' not in t
with open(OUT, 'x', encoding='utf-8', newline=NL) as f:
    f.write(t)
b = t.encode('utf-8')
print('out', OUT, 'chars', len(t), 'bytes', len(b), 'SHA-256', hashlib.sha256(b).hexdigest().upper())
print('template SHA-256', sha(TPL))
