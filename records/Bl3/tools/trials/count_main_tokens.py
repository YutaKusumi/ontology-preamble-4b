# -*- coding: utf-8 -*-
"""本の計算の順伝播のトークンの数を、近道なし（裁定 D234）と近道あり（前の形）で数える（転記行 B のプロンプトの長さと、正本のバッチの組み方から・重みは読まない）。
出力: records/Bl3/tools/trials/count-main-tokens.txt（数は印字のまま・この記録から打ち直さない）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import bl3_run as BR
T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
DJ = json.load(open(os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json'), encoding='utf-8'))
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
B = FJ['facts']['B']['cells']
nA = len(FJ['facts']['A']['prefix_ids'])
names = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])],
         'iso': ['iso:%d' % i for i in range(T3['nulls']['isotropic']['count'])], 'real': ['real:' + p for p in DJ['groups']['real']['names']]}
gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
sets = BR.cell_sign_sets(T3, None, names['named'], names['B_random'], names['iso'], names['real'], gate_only)
bs = T3['readout']['primary']['batch']
n_batches = tok_no = tok_short = 0
for key, ck, sg, ds in sets:
    b = -(-(len(ds) + 1) // bs)
    n_batches += b
    tok_no += b * bs * (B[ck]['prompt_len'] + nA)                       # 近道なし: 列の全体（プロンプト ＋ 書き出し）
    tok_short += b * bs * (nA + 1) + (B[ck]['prompt_len'] - 1)          # 近道あり: 主位置から後ろ（主位置 ＋ 書き出し）と、主位置より前の一回
E = FJ['facts']['E']
L = ['# 本の計算の順伝播のトークンの数（機械生成・`records/Bl3/tools/trials/count_main_tokens.py`・正本 SHA16 %s・設計事実 SHA16 %s）' % (
        sha16f(os.path.join(REPO, 'design', 'contrasts-Bl3.json')), sha16f(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'))), '',
     '- 升目と符号の組 %d・バッチ %d（大きさ %d）' % (len(sets), n_batches, bs),
     '- 近道なし（裁定 D234・本の計算の今の形）: %d トークン' % tok_no,
     '- 近道あり（前の形・参考）: %d トークン' % tok_short,
     '- 転記行 E の独立の再計算の見込み（参考）: 順伝播 %d 回・%d トークン' % (E['passes_recompute'], E['tokens_recompute']), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
out = os.path.join(HERE, 'count-main-tokens.txt')
open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('\n'.join(L[:6]))
