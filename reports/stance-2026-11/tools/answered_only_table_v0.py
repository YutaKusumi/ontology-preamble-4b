# -*- coding: utf-8 -*-
# answered_only_table.py : 凍結の判定の道具の出力（judge-report.json）から、答えた試行を分母とする率と差の区間を写す（記述・事前登録 §4 の「答えた試行を分母とする率も並べる」）
# 使い方: python -I answered_only_table.py <judge-report.json> <out.md>
import sys, json, hashlib, os
sys.stdout.reconfigure(encoding='utf-8')
src, out = sys.argv[1], sys.argv[2]
b = open(src, 'rb').read()
sha = hashlib.sha256(b).hexdigest().upper()
d = json.loads(b.decode('utf-8'))
WORDS = [('soul', '魂'), ('kokoro', '心'), ('ishiki', '意識'), ('seishin', '精神'), ('kanjo', '感情'), ('jiga', '自我')]
VALS = [('ari', '有'), ('nashi', '無'), ('fumei', '不明')]
NL = chr(10)
L = []
L.append('入力: ' + os.path.basename(src) + '（SHA-256 ' + sha + '）')
L.append('')
L.append('## 表 A. 条件ごとの率（全分母と、答えた試行を分母とする率）')
L.append('')
L.append('| 場面 | 語 | 置く値 | 破局的選択 | 答えた試行 | 答えなかった試行 | 全分母の率 | 答えた試行の率 |')
L.append('|---|---|---|---|---|---|---|---|')
order = {}
for sc in ['N1', 'N2', 'SK']:
    cells = d['cells'][sc]
    for wk, wj in WORDS:
        rates_full = {}
        rates_ans = {}
        for vk, vj in VALS:
            c = cells[wk + '-' + vk]
            nonans = c['refuse'] + c['format_out']
            ans = c['n_ok'] - nonans
            rf = c['catastrophe'] / c['n_ok']
            ra = c['catastrophe'] / ans
            rates_full[vj] = rf
            rates_ans[vj] = ra
            L.append('| %s | %s | %s | %d | %d | %d | %.3f | %.3f |' % (sc, wj, vj, c['catastrophe'], ans, nonans, rf, ra))
        order[(sc, wj)] = (rates_full, rates_ans)
    c = cells['N']
    nonans = c['refuse'] + c['format_out']
    ans = c['n_ok'] - nonans
    L.append('| %s | （N） | — | %d | %d | %d | %.3f | %.3f |' % (sc, c['catastrophe'], ans, nonans, c['catastrophe'] / c['n_ok'], c['catastrophe'] / ans))
L.append('')
L.append('## 表 B. 「不明」の位置（点の値の並び・検定していない）')
L.append('')
L.append('| 場面 | 語 | 全分母：不明は | 答えた試行：不明は |')
L.append('|---|---|---|---|')
def pos(r):
    f, a, n = r['不明'], r['有'], r['無']
    if f < min(a, n):
        return '最も低い'
    if f > max(a, n):
        return '最も高い'
    if min(a, n) <= f <= max(a, n):
        return '間'
    return '?'
cnt = {}
for sc in ['N1', 'N2', 'SK']:
    for wk, wj in WORDS:
        rf, ra = order[(sc, wj)]
        pf, pa = pos(rf), pos(ra)
        cnt[(sc, 'full', pf)] = cnt.get((sc, 'full', pf), 0) + 1
        cnt[(sc, 'ans', pa)] = cnt.get((sc, 'ans', pa), 0) + 1
        L.append('| %s | %s | %s | %s |' % (sc, wj, pf, pa))
L.append('')
for k in sorted(cnt):
    L.append('- 数え ' + ' '.join(k) + ' : ' + str(cnt[k]))
L.append('')
L.append('## 表 C. 確証と保留の比べ（凍結の判定のまま）と、答えた試行を分母とする差（凍結の道具が計算した区間 rd_answered_ci）')
L.append('')
L.append('| 場面 | 語 | 比べ | 判定 | Holm の後の p | 差（全分母） | 差（答えた試行） | 答えた試行の差の 95% 区間 | 答えなかった割合の差 |')
L.append('|---|---|---|---|---|---|---|---|---|')
n_cross = 0
n_conf = 0
for c in d['comparisons']:
    if c['label'] == '確証されなかった':
        continue
    a, bb = c['a'], c['b']
    ra = a['catastrophe'] / a['answered']
    rb = bb['catastrophe'] / bb['answered']
    lo, hi = c['rd_answered_ci']
    if c['label'].startswith('確証'):
        n_conf += 1
        if lo <= 0 <= hi:
            n_cross += 1
    nonans_a = a['nonchoice'] / a['n_ok']
    nonans_b = bb['nonchoice'] / bb['n_ok']
    L.append('| %s | %s | %s と %s | %s | %.4g | %+.3f | %+.3f | %+.3f〜%+.3f | %+.3f |' % (
        c['scene'], c['word'], c['value_a'], c['value_b'], c['label'], c['p_holm'], c['rd'], ra - rb, lo, hi, nonans_a - nonans_b))
L.append('')
L.append('- 確証の数 %d・そのうち答えた試行の差の区間が 0 をまたぐ数 %d' % (n_conf, n_cross))
L.append('')
L.append('## 表 D. 有と無の比べ（18）の生の p（記述・族は 54 のまま）')
L.append('')
L.append('| 場面 | 語 | p | Holm の後の p（m＝54） | 判定 |')
L.append('|---|---|---|---|---|')
ps = []
for c in d['comparisons']:
    if c['value_a'] == '有' and c['value_b'] == '無':
        ps.append((c['p'], c['scene'], c['word'], c['p_holm'], c['label']))
        L.append('| %s | %s | %.4g | %.4g | %s |' % (c['scene'], c['word'], c['p'], c['p_holm'], c['label']))
L.append('')
ps.sort()
m = len(ps)
passed = 0
for i, (p, sc, w, ph, lab) in enumerate(ps):
    if p * (m - i) <= 0.05:
        passed += 1
    else:
        break
L.append('- 仮に有と無の 18 だけで Holm（m＝%d）を当てたときに通る数（事後・記述・凍結の判定ではない）: %d' % (m, passed))
txt = NL.join(L) + NL
with open(out, 'x', encoding='utf-8', newline=NL) as f:
    f.write(txt)
print('sha_in', sha)
print('out', out, 'bytes', len(txt.encode('utf-8')))
print('n_conf', n_conf, 'n_cross', n_cross, 'holm18_pass', passed)
for k in sorted(cnt):
    print(k, cnt[k])
