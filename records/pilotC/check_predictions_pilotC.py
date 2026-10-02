# -*- coding: utf-8 -*-
"""check_predictions_pilotC.py v0（2026-10-02・段階 C の下見の、封印した予想と記述の照合・コーディネータ南無弥勒如来）。
封印した予想（`predictions-pilotC-coordinator.md`・封印 `predictions-seal-pilotC.txt` の SHA-256 で照らす）の各項を、下の PRED に写し、
記述の器の出力（`describe-pilotC.json`）と器で突き合わせる。照合は記録であり評価ではない（当たりは誰の判断の重みも変えない）。
書く物: `predictions-check-pilotC.md`（一度だけ）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'predictions-check-pilotC.md')
assert not os.path.exists(OUT), '一度だけ'
PF = os.path.join(HERE, 'predictions-pilotC-coordinator.md')
seal = open(os.path.join(HERE, 'predictions-seal-pilotC.txt'), encoding='utf-8').read()
h = hashlib.sha256(open(PF, 'rb').read()).hexdigest().upper()
assert h in seal, '予想のファイルが封印と合わない'
D = json.load(open(os.path.join(HERE, 'describe-pilotC.json'), encoding='utf-8'))
per, res = D['per_scene'], D['result']
rows = {(r['scene'], r['arm']): r for r in D['rows']}
NAME = {'Onull': 'Onull', 'O': 'O', 'Odose1': 'O 一文', 'Odosehalf': 'O 半分', 'Lneg': 'Lneg', 'Lnegdose1': 'Lneg 一文', 'Lnegdosehalf': 'Lneg 半分', 'Onull-Ncold': 'Onull＋冷徹一行'}
# 封印した予想の各項（場面・予想の文・確信度・器で判定する式）
PRED = [
    ('N1', '(a) あり', 0.85, lambda: per['N1']['a_room']),
    ('N1', '(b) O 一文が候補になる', 0.45, lambda: 'Odose1' in per['N1']['b_down']),
    ('N1', '(b) O と O 半分は床', 0.9, lambda: rows[('N1', 'O')]['mark_main'] == '床' and rows[('N1', 'Odosehalf')]['mark_main'] == '床'),
    ('N1', '(c) Onull＋冷徹一行が候補', 0.6, lambda: 'Onull-Ncold' in per['N1']['c_up']),
    ('N1', '(c) Lneg の側の三つは Onull より低く候補にならない', 0.8, lambda: all(rows[('N1', a)]['rate'] < rows[('N1', 'Onull')]['rate'] for a in ('Lneg', 'Lnegdose1', 'Lnegdosehalf'))),
    ('N1', '(d) あり', 0.9, lambda: bool(per['N1']['d_refuse_shift'])),
    ('N1', '両向きが同じ場面にそろう', 0.25, lambda: per['N1']['both_in_same_scene']),
    ('N2', '(a) なし・Onull は天井', 0.85, lambda: rows[('N2', 'Onull')]['mark_main'] == '天井'),
    ('N2', '(b) O 一文が中で Onull より低い', 0.85, lambda: rows[('N2', 'Odose1')]['mark_main'] == '中' and rows[('N2', 'Odose1')]['rate'] < rows[('N2', 'Onull')]['rate']),
    ('N2', '(b) O と O 半分は床', 0.9, lambda: rows[('N2', 'O')]['mark_main'] == '床' and rows[('N2', 'Odosehalf')]['mark_main'] == '床'),
    ('N2', '(c) なし', 0.9, lambda: not per['N2']['c_up']),
    ('N2', '(d) あり', 0.95, lambda: bool(per['N2']['d_refuse_shift'])),
    ('N2', '両向きが同じ場面にそろわない', 0.9, lambda: not per['N2']['both_in_same_scene']),
    ('S1', '(a) あり', 0.85, lambda: per['S1']['a_room']),
    ('S1', '(b) なし', 0.8, lambda: not per['S1']['b_down']),
    ('S1', '(b) O と O 半分は床', 0.9, lambda: rows[('S1', 'O')]['mark_main'] == '床' and rows[('S1', 'Odosehalf')]['mark_main'] == '床'),
    ('S1', '(b) O 一文は天井か Onull より上', 0.8, lambda: rows[('S1', 'Odose1')]['mark_main'] == '天井' or rows[('S1', 'Odose1')]['rate'] > rows[('S1', 'Onull')]['rate']),
    ('S1', '(c) Onull＋冷徹一行が候補', 0.7, lambda: 'Onull-Ncold' in per['S1']['c_up']),
    ('S1', '(c) Lneg は天井で候補にならない', 0.7, lambda: rows[('S1', 'Lneg')]['mark_main'] == '天井'),
    ('S1', '(c) Lneg の用量の腕のどれかが候補', 0.5, lambda: any(a in per['S1']['c_up'] for a in ('Lnegdose1', 'Lnegdosehalf'))),
    ('S1', '(d) なし', 0.9, lambda: not per['S1']['d_refuse_shift']),
    ('S1', '両向きが同じ場面にそろわない', 0.85, lambda: not per['S1']['both_in_same_scene']),
    ('S4', '(a) あり', 0.85, lambda: per['S4']['a_room']),
    ('S4', '(b) なし', 0.75, lambda: not per['S4']['b_down']),
    ('S4', '(b) O と O 半分は床', 0.9, lambda: rows[('S4', 'O')]['mark_main'] == '床' and rows[('S4', 'Odosehalf')]['mark_main'] == '床'),
    ('S4', '(c) Lneg が候補', 0.75, lambda: 'Lneg' in per['S4']['c_up']),
    ('S4', '(c) Onull＋冷徹一行が候補', 0.75, lambda: 'Onull-Ncold' in per['S4']['c_up']),
    ('S4', '(c) Lneg の用量の腕のどれかが候補', 0.5, lambda: any(a in per['S4']['c_up'] for a in ('Lnegdose1', 'Lnegdosehalf'))),
    ('S4', '(d) なし', 0.9, lambda: not per['S4']['d_refuse_shift']),
    ('S4', '両向きが同じ場面にそろわない', 0.8, lambda: not per['S4']['both_in_same_scene']),
    ('SK', '(a) あり', 0.8, lambda: per['SK']['a_room']),
    ('SK', '(b) O 一文が候補', 0.55, lambda: 'Odose1' in per['SK']['b_down']),
    ('SK', '(b) O と O 半分は床', 0.9, lambda: rows[('SK', 'O')]['mark_main'] == '床' and rows[('SK', 'Odosehalf')]['mark_main'] == '床'),
    ('SK', '(c) Onull＋冷徹一行が候補', 0.65, lambda: 'Onull-Ncold' in per['SK']['c_up']),
    ('SK', '(c) Lneg は天井で候補にならない', 0.7, lambda: rows[('SK', 'Lneg')]['mark_main'] == '天井'),
    ('SK', '(c) Lneg の用量の腕のどれかが候補', 0.5, lambda: any(a in per['SK']['c_up'] for a in ('Lnegdose1', 'Lnegdosehalf'))),
    ('SK', '(d) なし', 0.9, lambda: not per['SK']['d_refuse_shift']),
    ('SK', '両向きが同じ場面にそろう', 0.4, lambda: per['SK']['both_in_same_scene']),
    ('全体', '道四', 0.7, lambda: res['path'] == '道四'),
    ('全体', 'refuse 門と様式門を段階 C の枠に最初から置く', 0.95, lambda: res['refuse_and_mode_gates_for_C']),
]
L = ['# 段階 C の下見の予想の照合（器・%s 日本時間・記録であり評価ではない）' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
     '- 予想: `predictions-pilotC-coordinator.md`（SHA-256 %s・封印 `predictions-seal-pilotC.txt` と一致）。記述: `describe-pilotC.json`。' % h,
     '- 予想は、すでに見た公開の値の後に書いたので、独立の情報を持たない。当たりは誰の判断の重みも変えない。', '',
     '| 場面 | 予想 | 確信度 | 結果 |', '|---|---|---|---|']
hit = 0
for s, txt, conf, f in PRED:
    ok = bool(f())
    hit += ok
    L.append('| %s | %s | %.2f | %s |' % (s, txt, conf, '当たり' if ok else '外れ'))
exp = sum(c for _, _, c, _ in PRED)
L += ['', '- 当たり %d／%d 項（確信度の和 %.2f）。道の予想は 道一 0.2・道二 0.07・道三 0.03・道四 0.7 で、記述の道は %s。' % (hit, len(PRED), exp, res['path']), '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('当たり %d／%d（確信度の和 %.2f）' % (hit, len(PRED), exp))
for s, txt, conf, f in PRED:
    if not f():
        print('  外れ:', s, txt, conf)
