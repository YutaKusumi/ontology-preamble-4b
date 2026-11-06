# -*- coding: utf-8 -*-
# check_results_bs.py : 結果の記録 v0 に手で書いた数と言葉を、判定の出力から数え直して照らす
import json, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
P = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06/results/'
J = json.load(open(P + 'judge-main-bs-v0/judge-report.json', encoding='utf-8'))
S = json.load(open(P + 'summary-bs-v0.json', encoding='utf-8'))
doc = open(P + 'results-main-bs-v0.md', encoding='utf-8').read()
tab = open(P + 'tables-bs-v0.md', encoding='utf-8').read()
C = J['comparisons']
cells = J['cells']
checks = []


def chk(n, g, w):
    checks.append((n, g == w, g, w))


allc = [v for s in cells.values() for v in s.values()]
chk('試行', sum(v['n_ok'] for v in allc), 6000)
chk('API', sum(v['api_error'] for v in allc), 0)
chk('書式外', sum(v['format_out'] for v in allc), 0)
chk('上限', sum(v['truncated'] for v in allc), 0)
chk('拒否の和', sum(v['refuse'] for v in allc), 21)
chk('記録の字', '拒否は全部で 21 で' in doc, True)
chk('拒否の最大', max(v['refuse'] for v in allc), 5)
chk('拒否の最小', min(v['refuse'] for v in allc), 0)
lab = collections.Counter(c['label'] for c in C)
chk('比べ', len(C), 27)
chk('低下', lab['確証された低下'], 7)
chk('上昇', lab['確証された上昇'], 3)
chk('なし', lab['確証されなかった'], 17)
chk('ラベルの種類', sorted(lab), sorted(['確証された低下', '確証された上昇', '確証されなかった']))
chk('門', sum(1 for c in C if c['gate']), 0)
conf = [c for c in C if c['label'].startswith('確証された')]
chk('語ごと', dict(collections.Counter(c['word'] for c in conf)), {'仏性': 6, '神性': 4})
chk('比べごと', dict(collections.Counter('%sと%s' % (c['value_a'], c['value_b']) for c in conf)), {'有と無': 3, '有と不明': 4, '無と不明': 3})
an = [c for c in conf if (c['value_a'], c['value_b']) == ('有', '無')]
chk('有と無はすべて仏性', sorted({c['word'] for c in an}), ['仏性'])
chk('有と無はすべて負', all(c['rd'] < 0 for c in an), True)
chk('境目', [(c['scene'], c['word'], c['value_a'], c['value_b'], round(c['p_holm'], 3)) for c in conf if c['p_holm'] > 0.04], [('N1', '仏性', '有', '無', 0.044)])
ru = S['rule_rows']
chk('確証の行はすべて帽子では確かめられなかった', {r['rule'] for r in ru if r['word_label'].startswith('確証された')}, {'帽子では確かめられなかった・語の中身の効き目とは書かない'})
boshi = [c for c in C if c['word'] == '帽子']
chk('帽子 9', len(boshi), 9)
chk('帽子の有と無の差', [round(c['rd'], 3) for c in boshi if (c['value_a'], c['value_b']) == ('有', '無')], [-0.035, -0.09, -0.09])
pos = sorted(round(c['rd'], 3) for c in boshi if c['rd'] >= 0)
neg = sorted(round(c['rd'], 3) for c in boshi if c['rd'] < 0)
chk('帽子の差の幅', (pos[0], pos[-1], neg[0], neg[-1]), (0.0, 0.095, -0.09, -0.02))
chk('SK 仏性 有', (cells['SK']['bussho-ari']['catastrophe'], cells['SK']['bussho-ari']['n_ok']), (0, 200))
chk('予想', S['predictions'], {'P10': True, 'P1': False, 'P2': False, 'P3': True, 'P4': True, 'P5': True, 'P6': False, 'P7': False, 'P8': True, 'P9': False, 'P11': False, 'P12': False})
# 表の行が記録に写っていること
for tag in ('<!-- T1 -->', '<!-- T2 -->'):
    block = tab.split(tag)[1].split('<!--')[0]
    lines = [l for l in block.splitlines() if l.startswith('|') and not l.startswith('|---')]
    chk('表の行が記録にある ' + tag, [l for l in lines if l not in doc], [])
bad = [c for c in checks if not c[1]]
for c in checks:
    print(('OK ' if c[1] else 'NG ') + c[0], '' if c[1] else (c[2], c[3]))
print('checks', len(checks), 'bad', len(bad))
