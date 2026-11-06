# -*- coding: utf-8 -*-
# results_tables_bs_v0.py : 判定の報告と §10 の読み方の表から、結果の記録と報告に使う表を組む（表の数はすべて出力から出す・手で写さない）
# 使い方: python -I results_tables_bs_v0.py <judge-report.json> <summary の json> <出す md>
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
JP, SP, OUT = sys.argv[1:4]
J = json.load(open(JP, encoding='utf-8'))
S = json.load(open(SP, encoding='utf-8'))
NL = chr(10)
MINUS = chr(0x2212)
WORDS = [('bussho', '仏性'), ('shinsei', '神性'), ('boshi', '帽子')]
VALS = [('ari', '有'), ('nashi', '無'), ('fumei', '不明')]


def f3(x):
    return '%.3f' % x


def s3(x):
    if abs(x) < 0.0005:
        return '0.000'
    return ('%+.3f' % x).replace('-', MINUS)


def ci(lo, hi):
    return s3(lo) + '〜' + s3(hi)


def fp(p):
    return ('%.3f' % p) if p >= 0.01 else ('%.1e' % p)


scenes = sorted(J['cells'])


def cell(sc, arm):
    return J['cells'][sc][arm]


def ans(c):
    return c['n_ok'] - c['refuse'] - c['format_out'] - c['truncated']


L = ['<!-- T1 -->', '| 場面 | 語 | 有 | 無 | 不明 |', '|---|---|---|---|---|']
for sc in scenes:
    for wk, wj in WORDS:
        row = ['| %s | %s' % (sc, wj)]
        for vk, vj in VALS:
            c = cell(sc, wk + '-' + vk)
            row.append(' %s／%s／%d' % (f3(c['catastrophe'] / c['n_ok']), f3(c['catastrophe'] / ans(c)) if ans(c) else '—', c['refuse']))
        L.append(' |'.join(row) + ' |')
L += ['', '<!-- NROW -->', '・'.join('%s %s／%s／%d' % (sc, f3(cell(sc, 'N')['catastrophe'] / cell(sc, 'N')['n_ok']), f3(cell(sc, 'N')['catastrophe'] / ans(cell(sc, 'N'))), cell(sc, 'N')['refuse']) for sc in scenes), '']
L += ['<!-- T2 -->', '| 場面 | 語 | 比べ（A と B） | 判定 | 差（全分母） | 95% 区間（全分母） | 差（答えた試行） | 95% 区間（答えた試行） | 答えなかった割合の差 | Holm の後の p | 注 |', '|---|---|---|---|---|---|---|---|---|---|---|']
for c in J['comparisons']:
    if c['label'] == '確証されなかった':
        continue
    a, b = c['a'], c['b']
    da = a['catastrophe'] / a['answered'] - b['catastrophe'] / b['answered'] if a['answered'] and b['answered'] else None
    dn = a['nonchoice'] / a['n_ok'] - b['nonchoice'] / b['n_ok']
    lo, hi = c['rd_answered_ci'] if c.get('rd_answered_ci') else (None, None)
    note = '境目' if (c['label'].startswith('確証された') and c['p_holm'] > 0.04) else ''
    if c['label'].startswith('判定保留'):
        note = '応答様式の変化の決まり'
    L.append('| %s | %s | %s と %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (c['scene'], c['word'], c['value_a'], c['value_b'], c['label'], s3(c['rd']), ci(*c['rd_ci']),
                                                                               s3(da) if da is not None else '—', ci(lo, hi) if lo is not None else '—', s3(dn), fp(c['p_holm']), note))
L += ['', '<!-- T3 -->', '| 場面 | 語 | 有 | 無 | 差（有 − 無） | 95% 区間 | Holm の後の p | 判定 |', '|---|---|---|---|---|---|---|---|']
for c in J['comparisons']:
    if (c['value_a'], c['value_b']) != ('有', '無'):
        continue
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (c['scene'], c['word'], f3(c['a']['catastrophe'] / c['a']['n_ok']), f3(c['b']['catastrophe'] / c['b']['n_ok']), s3(c['rd']), ci(*c['rd_ci']), fp(c['p_holm']), c['label']))
L += ['', '<!-- T4 -->', '| 場面 | 語 | 比べ | 語の比べ | 差 | 帽子の比べ | 差 | 書き方（事前登録 §10） |', '|---|---|---|---|---|---|---|---|']
for r in S['rule_rows']:
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (r['scene'], r['word'], r['pair'], r['word_label'], s3(r['word_rd']), r['boshi_label'], s3(r['boshi_rd']), r['rule']))
L += ['', '<!-- P -->']
for k in sorted(S['predictions'], key=lambda x: int(x[1:])):
    L.append('- %s：%s' % (k, S['predictions'][k]))
L += ['', '<!-- COUNTS -->', json.dumps({k: S[k] for k in ('m', 'labels', 'n_conf', 'n_hold', 'by_word', 'by_scene', 'by_pair')}, ensure_ascii=False)]
with open(OUT, 'x', encoding='utf-8', newline=NL) as f:
    f.write(NL.join(L) + NL)
print('rows', len(L))
