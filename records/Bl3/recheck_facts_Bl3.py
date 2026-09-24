# -*- coding: utf-8 -*-
"""recheck_facts_Bl3.py v2 —— B-lens 層三（Bl3）の設計の事実（`records/Bl3/design-facts-Bl3.json`）の件数を、器 `tools/bl3_facts.py` のコードを使わずに数え直す（読み取りだけ）。
数え直すもの: JSON 直答の型の出力の総数と升目ごとの内訳・その選択・散文の出力の件数と書き出しを含む件数・主の升目の JSON 直答の件数・使えた試行の件数・量が零の (a) の件数（無操作の升目と門の行）・refuse を選んだ出力の件数と、その JSON の選択の値の字面・門の行ごとの JSON 直答の割合の差と様式の転位の行（v2）。
数え直さないもの: プロンプトの長さ・主位置・トークンの番号・方向と帰無の SHA・重みの SHA（凍結の関数と模型の割り方を要し、器と同じ関数を呼ぶことになるため）。
出力: records/Bl3/recheck-facts-Bl3.md（機械生成）。一つでも食い違えば終了コードを立てる。
用法: python records/Bl3/recheck_facts_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, glob, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FP = os.path.join(R, 'records', 'Bl3', 'design-facts-Bl3.json')
FJ = json.load(open(FP, encoding='utf-8'))
F = FJ['facts']
T3 = json.load(open(os.path.join(R, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
PREF = '`' * 3 + 'json' + NL + '{"choice": "'                                  # 器と別に組んだ書き出し
KEY = '"choice": "'
ok, sb, sb_choice = collections.Counter(), collections.Counter(), collections.Counter()
prose = prose_key = prose_pref = 0
a0_arm_dir = collections.Counter()
ref_n = ref_lit = 0
sb_arm_dir = collections.defaultdict(lambda: [0, 0])
for d in sorted(glob.glob(os.path.join(R, 'results', 'stageB', 'stageB__*__s1'))):
    sc, arm = os.path.basename(d).split('__')[1:3]
    cell = '%s|%s' % (sc, arm)
    raw = {}
    for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8'):
        o = json.loads(l)
        raw[o['trial_id']] = o['text']
    for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8'):
        t = json.loads(l)
        if t['status'] != 'ok':
            continue
        ok[cell] += 1
        if t['style_b']:
            sb[cell] += 1
            sb_choice[t['choice']] += 1
        else:
            prose += 1
            prose_key += KEY in raw[t['trial_id']]
            prose_pref += PREF in raw[t['trial_id']]
        if t['choice'] == 'a' and not t['catastrophe']:
            a0_arm_dir[(sc, arm, t['direction_id'])] += 1
        if t['choice'] == 'refuse':
            ref_n += 1
            ref_lit += ('"choice": "refuse"' in raw[t['trial_id']])
        sb_arm_dir[(sc, arm, t['direction_id'])][0] += int(bool(t['style_b']))
        sb_arm_dir[(sc, arm, t['direction_id'])][1] += 1
A, B, C = F['A'], F['B']['cells'], F['C']
main = ['%s|%s' % tuple(c) for c in T3['cells_main']]
gate_a0 = {}
for r in C['gate_rows']:
    k = '%s|%s' % (r['scenario'], r['arm']) + ('〔%s〕' % r['direction_id'] if r['direction_id'].startswith('rand') else '')
    gate_a0[k] = a0_arm_dir.get((r['scenario'], r['arm'], r['direction_id']), 0)
hold = T3['gate']['style_hold_pt']
share = {}
for r in C['gate_rows']:
    k = '%s|%s' % (r['scenario'], r['arm']) + ('〔%s〕' % r['direction_id'] if r['direction_id'].startswith('rand') else '')
    a_, n_ = sb_arm_dir[(r['scenario'], r['arm'], r['direction_id'])]
    b_ = sb_arm_dir[(r['scenario'], r['base'], 'fixed')]
    share[k] = round(100.0 * (a_ / n_ - b_[0] / b_[1]), 1)
style_rows = [k for k, v in share.items() if abs(v) >= hold]
rows = [
    ('書き出しの文字列（器と別に組んだもの）', repr(PREF), repr(A['prefix']), PREF == A['prefix']),
    ('JSON 直答の型の出力の総数', sum(sb.values()), A['json_direct_n'], sum(sb.values()) == A['json_direct_n']),
    ('JSON 直答の型の出力の升目ごとの内訳', '・'.join('%s %d' % kv for kv in sorted(sb.items())), '・'.join('%s %d' % kv for kv in sorted(A['json_direct_by_cell'].items())), dict(sb) == A['json_direct_by_cell']),
    ('JSON 直答の型の出力の選択（試行の記録）と、選択の値の最初のトークン（器）', '・'.join('%s %d' % kv for kv in sorted(sb_choice.items())), '・'.join('%s %d' % kv for kv in sorted(A['first_letters'].items())), dict(sb_choice) == A['first_letters']),
    ('散文の出力の件数', prose, A['prose_n'], prose == A['prose_n']),
    ('散文の出力のうち選択の鍵を含む件数', prose_key, A['prose_with_key'], prose_key == A['prose_with_key']),
    ('散文の出力のうち書き出しをそのまま含む件数', prose_pref, A['prose_with_prefix'], prose_pref == A['prose_with_prefix']),
    ('主の升目の無操作の腕の JSON 直答の件数', '・'.join('%s %d' % (c, sb.get(c, 0)) for c in main), '・'.join('%s %d' % (c, B[c]['json_direct']) for c in main), all(sb.get(c, 0) == B[c]['json_direct'] for c in main)),
    ('転記行 B の升目の使えた試行', '・'.join('%s %d' % (c, ok[c]) for c in B), '・'.join('%s %d' % (c, B[c]['n_ok']) for c in B), all(ok[c] == B[c]['n_ok'] for c in B)),
    ('転記行 B の升目の量が零の (a)', '・'.join('%s %d' % (c, a0_arm_dir.get((c.split('|')[0], c.split('|')[1], 'fixed'), 0)) for c in B), '・'.join('%s %d' % (c, B[c]['a_not_catastrophe']) for c in B),
     all(a0_arm_dir.get((c.split('|')[0], c.split('|')[1], 'fixed'), 0) == B[c]['a_not_catastrophe'] for c in B)),
    ('refuse を選んだ出力の件数（器の数え方と別に・JSON の選択の値の字面が refuse か）', '%d 件・字面が一致 %d 件' % (ref_n, ref_lit), '%d 件（書き出しの次のトークン %s）' % (sum(A['refuse_next'].values()), '・'.join('%s %d' % kv for kv in A['refuse_next'].items())), ref_n == sum(A['refuse_next'].values()) == ref_lit),
    ('門の行ごとの JSON 直答の割合の差（pt）と様式の転位の行', '差の一致 %d 行・転位の行 %s' % (len(share), '・'.join(style_rows)), '転位の行 %s' % '・'.join(C['style_rows']), share == C['style_share_pt'] and style_rows == C['style_rows']),
    ('門の行ごとの量が零の (a)（行の数と合計）', '%d 行・合計 %d' % (len(gate_a0), sum(gate_a0.values())), '%d 行・合計 %d' % (len(C['gate_a_not_catastrophe']), sum(C['gate_a_not_catastrophe'].values())), gate_a0 == C['gate_a_not_catastrophe']),
]
bad = [x for x in rows if not x[3]]
L = ['# B-lens 層三の設計の事実の数え直し（機械生成・`records/Bl3/recheck_facts_Bl3.py` v2）', '',
     '- 数え直した記録: `records/Bl3/design-facts-Bl3.json`（SHA16 %s・生成 %s UTC）。器 `tools/bl3_facts.py` のコードは使わず、段階 B の試行と生の出力（`results/stageB/`）を読み直した。' % (s16(FP), FJ['generated_utc']),
     '- 数え直さないもの: プロンプトの長さ・主位置・トークンの番号・方向と帰無の SHA・重みの SHA（凍結の関数と模型の割り方を要し、器と同じ関数を呼ぶことになるため）。',
     '- 食い違い: %d 件。' % len(bad), '', '| 項目 | 数え直し | 器 | 一致 |', '|---|---|---|---|'] + [
     '| %s | %s | %s | %s |' % (a, str(b).replace('|', '｜'), str(c).replace('|', '｜'), '一致' if d else '**食い違い**') for a, b, c, d in rows] + [
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'recheck-facts-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('wrote recheck-facts-Bl3.md | rows', len(rows), '| mismatches', len(bad))
sys.exit(1 if bad else 0)
