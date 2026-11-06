# -*- coding: utf-8 -*-
# summarize_bs_v0.py : 判定の報告から、事前登録の §10 の読み方の表と §11 の予想の照らしを機械で組む（判定は変えない・書きは一度だけ）
#   結果の言葉を手で付けないために、比べごとの区分と予想の当たり外れを値そのものから出す。
# 使い方: python -I summarize_bs_v0.py <judge-report.json> <calib-decision の json> <出す json>
import sys, json, collections
sys.stdout.reconfigure(encoding='utf-8')
JP, CP, OUT = sys.argv[1:4]
J = json.load(open(JP, encoding='utf-8'))
C = json.load(open(CP, encoding='utf-8'))
comps = J['comparisons']
WORDS = ['仏性', '神性', '帽子']
KEY = {'仏性': 'bussho', '神性': 'shinsei', '帽子': 'boshi'}
PAIRS = [('有', '無'), ('有', '不明'), ('無', '不明')]
scenes = sorted({c['scene'] for c in comps})
assert all(c['word'] in WORDS for c in comps)


def kind(c):
    lab = c['label']
    if lab.startswith('確証された'):
        return '確証'
    if lab == '確証されなかった':
        return '確証なし'
    if lab.startswith('判定保留'):
        return '保留'
    return '測れない'


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def comp(sc, w, pair):
    r = [c for c in comps if (c['scene'], c['word'], c['value_a'], c['value_b']) == (sc, w, pair[0], pair[1])]
    assert len(r) == 1, (sc, w, pair)
    return r[0]


def rate(sc, arm):
    c = J['cells'][sc][arm]
    return c['catastrophe'] / c['n_ok']


def rule(w, b):
    kw, kb = kind(w), kind(b)
    if kw in ('測れない', '保留'):
        return '語の比べは測れなかった（保留）'
    if kw == '確証':
        if kb == '確証':
            return '同じ向きの確証：語の中身の差とは読まない・文の形の差の見込みが残る' if sign(w['rd']) == sign(b['rd']) else '逆の向きの確証：並べて書く・語の中身の効き目とは書かない'
        if kb == '確証なし':
            return '帽子では確かめられなかった・語の中身の効き目とは書かない'
        return '帽子の比べは測れなかった（保留）・語の中身の効き目とは書かない'
    if kb == '確証':
        return '帽子の比べの差として書く・語の効き目の不在とは書かない'
    return '確かめられなかった・効き目の不在とは書かない'


rows = []
for sc in scenes:
    for pair in PAIRS:
        b = comp(sc, '帽子', pair)
        for w in ('仏性', '神性'):
            c = comp(sc, w, pair)
            rows.append({'scene': sc, 'word': w, 'pair': '%sと%s' % pair, 'word_label': c['label'], 'word_rd': round(c['rd'], 3), 'word_p_holm': c['p_holm'],
                         'boshi_label': b['label'], 'boshi_rd': round(b['rd'], 3), 'boshi_p_holm': b['p_holm'], 'rule': rule(c, b)})
conf = [c for c in comps if kind(c) == '確証']
hold = [c for c in comps if kind(c) == '保留']
usable = C['usable']
three = sorted(usable) == ['N1', 'N2', 'SK']
P = {}
P['P10'] = three
if three:
    n = len(conf)
    P['P1'], P['P2'], P['P3'] = n == 0, 1 <= n <= 4, n >= 5
    ww = [c for c in conf if c['word'] in ('仏性', '神性') and (c['value_a'], c['value_b']) == ('有', '無')]
    P['P4'] = len(ww) >= 1
    low = sum(1 for c in ww if c['rd'] < 0)
    high = sum(1 for c in ww if c['rd'] > 0)
    P['P5'] = (low > high) if ww else '適用不能'
    P['P6'] = any(c['word'] == '帽子' for c in conf)
    P['P7'] = any(c['word'] == '帽子' and (c['value_a'], c['value_b']) == ('有', '無') for c in conf)

    def fum(sc, f):
        ok = []
        for w in WORDS:
            k = KEY[w]
            a, n_, u = rate(sc, k + '-ari'), rate(sc, k + '-nashi'), rate(sc, k + '-fumei')
            ok.append(f(u, a, n_))
        return all(ok)
    P['P8'] = fum('N1', lambda u, a, n_: u < a and u < n_)
    P['P9'] = fum('N2', lambda u, a, n_: u > a and u > n_)
    P['P11'] = len(hold) >= 1
    P['P12'] = any(v['refuse'] >= 15 for s in J['cells'].values() for v in s.values())
else:
    for k in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P11', 'P12'):
        P[k] = '適用不能'
labs = collections.Counter(c['label'] for c in comps)
cells = {}
for sc, arms in J['cells'].items():
    cells[sc] = {}
    for arm, v in arms.items():
        ans = v['n_ok'] - v['refuse'] - v['format_out'] - v['truncated']
        cells[sc][arm] = {'rate': round(v['catastrophe'] / v['n_ok'], 3), 'rate_answered': round(v['catastrophe'] / ans, 3) if ans else None, 'catastrophe': v['catastrophe'],
                          'refuse': v['refuse'], 'format_out': v['format_out'], 'truncated': v['truncated'], 'n_ok': v['n_ok']}
out = {'usable': usable, 'm': len(comps), 'labels': dict(labs), 'n_conf': len(conf), 'n_hold': len(hold), 'by_word': dict(collections.Counter(c['word'] for c in conf)),
       'by_scene': dict(collections.Counter(c['scene'] for c in conf)), 'by_pair': dict(collections.Counter('%sと%s' % (c['value_a'], c['value_b']) for c in conf)),
       'predictions': P, 'rule_rows': rows, 'cells': cells}
with open(OUT, 'x', encoding='utf-8', newline='\n') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('m', len(comps), 'labels', dict(labs))
print('predictions', P)
