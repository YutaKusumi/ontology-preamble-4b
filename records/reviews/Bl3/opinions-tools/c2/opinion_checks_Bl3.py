# -*- coding: utf-8 -*-
"""opinion_checks_Bl3.py —— 層三の器への意見に付けた確かめ（claude.ai・Claude Opus 5.5・2026-09-25）。

numpy だけで走る（重み・模型・トークナイザ・本物の方向・段階 B の記録を読まない）。値はすべて乱数の合成で、意味は無い。
置き場: リポジトリの直下に置き、`python opinion_checks_Bl3.py` で走らせる（tools/ の analyze_Bl3・bl3_core・blens_core を import する）。
  一. 下見で主の升目を一つ外した形で、集計の器（analyze_Bl3）の row_labels・gates・recompute_agreement が通るか。
  二. 独立の再計算の札の一致（labels_signature）が、許容の内の小さな揺れで、どの欄で食い違うか（v̂ の行 8 行だけ・等方 1999 本）。
合成の対の名は、正本の八腕の組み合わせで作った（本物の方向の記録の名の並びは見ていない）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, itertools, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import analyze_Bl3 as AZ

T3 = json.load(open(os.path.join(HERE, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
ARMS = T3['nulls']['real']['arms']
PAIRS = ['%s~%s' % (a, b) for a, b in itertools.combinations(ARMS, 2)]
B3 = ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])]
KEYS = ['%s|%s|%+d' % (sc, b, s) for sc, b, s in T3['cell_signs_main']] + ['%s|Onull|-1' % sc for sc in ('N1', 'S1', 'S4', 'SK')]


def part_one():
    n_iso = 49
    T3d = json.loads(json.dumps(T3)); T3d['nulls']['isotropic']['count'] = n_iso
    rng = np.random.default_rng(0)
    names = list(T3['directions']['named']) + B3 + ['iso:%d' % i for i in range(n_iso)] + ['real:' + p for p in PAIRS]
    eff_all = {k: {d: float(rng.normal()) for d in names} for k in KEYS}
    rows_gate = []
    for k in KEYS:
        if k.endswith('|-1') and '|Onull|' in k:
            continue
        sc, base, _ = k.split('|')
        for u in list(T3['directions']['named']) + B3:
            rows_gate.append({'unit': u, 'cell': '%s|%s' % (sc, base), 'fam': k, 'y': float(rng.normal()), 'y_a': float(rng.normal()), 'name': '%s|%s|%d' % (k, u, len(rows_gate))})
    dropped = ['S1|Onull']                                              # 下見で外した主の升目（合成）
    eff = {k: v for k, v in eff_all.items() if not k.startswith('S1|Onull|')}   # run_main_phase は外した升目を流さない
    hook = {r['id']: {'noop_lo': 0.0, 'effects': {}} for r in T3['main_rows'] if r['direction'] == 'static' and not r['id'].startswith('add:S1')}
    for label, fn in [('row_labels', lambda: AZ.row_labels(T3d, T3['main_rows'], eff, PAIRS, dropped)),
                      ('gates', lambda: AZ.gates(T3d, rows_gate, eff, dropped, ())),
                      ('recompute_agreement', lambda: AZ.recompute_agreement(T3d, T3['main_rows'], eff, PAIRS, hook, None, {'floor': 1e-5}, dropped))]:
        try:
            fn(); print('一 %-20s 通った' % label)
        except Exception as e:
            print('一 %-20s 落ちた: %s %s' % (label, type(e).__name__, e))


def part_two(rels=(5e-3, 2e-2, 5e-2), reps=300, seed=7):
    K = T3['nulls']['isotropic']['count']
    names = list(T3['directions']['named']) + ['iso:%d' % i for i in range(K)] + ['real:' + p for p in PAIRS]
    st = [r['id'] for r in T3['main_rows'] if r['direction'] == 'static']
    fields = ('iso_outside', 'tail', 'side', 'sign', 'second_top')
    rng = np.random.default_rng(seed)
    for rel in rels:
        cnt, bad_now, bad_alt = collections.Counter(), 0, 0
        for _ in range(reps):
            A = {k: {d: float(v) for d, v in zip(names, rng.normal(size=len(names)))} for k in KEYS}   # 行も帰無も同じ分布（区別できない形）
            B = {k: {d: v + float(rng.normal(scale=rel)) for d, v in A[k].items()} for k in KEYS}
            la, lb = AZ.row_labels(T3, T3['main_rows'], A, PAIRS)[0], AZ.row_labels(T3, T3['main_rows'], B, PAIRS)[0]
            sa, sb = AZ.labels_signature(la), AZ.labels_signature(lb)
            b1 = b2 = False
            for rid in st:
                for i, f in enumerate(fields):
                    if sa[rid][i] != sb[rid][i]:
                        cnt[f] += 1; b1 = True
                        if f != 'tail' or la[rid]['iso_outside'] or lb[rid]['iso_outside']:
                            b2 = True
            bad_now += b1; bad_alt += b2
        print('二 揺れ／帰無の広がり %-6g 今の決まりで一致が落ちる割合 %.3f・裾を等方の外の行だけで比べると %.3f・欄ごとの食い違い %s'
              % (rel, bad_now / reps, bad_alt / reps, dict(cnt)))


if __name__ == '__main__':
    part_one()
    part_two()
