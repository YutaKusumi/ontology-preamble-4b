# -*- coding: utf-8 -*-
"""make_choices_coordinator_Bprime.py v0（2026-10-01・B′ の予想の封印の前段・コーディネータ南無弥勒如来）。
コーディネータの選んだ値（正本 `predictions.items` の四つ）と、情報状態の自由記述・引かれている結論の一行を、封印の器 `tools/seal_Bprime.py coordinator --choices` が読む JSON に書く。
自由記述の中の数は、層三の報告の最終版・正本・下見の前の凍結の記録・露出の記録・層三のコーディネータの予想から、この器が読んで入れる（打ち直さない）。
選んだ値は下の CHOICE に置く（封印が済むまで、返信に書かない・露出の記録の「扱い」）。
用法: python make_choices_coordinator_Bprime.py（作業の置き場で・出力 records/Bprime/seal/choices-coordinator-Bprime.json・既にあれば止める）
柵: 本器のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import io, os, re, sys, json, math, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
OUT = os.path.join(HERE, 'choices-coordinator-Bprime.json')
sha16 = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
fmt = lambda x: ('%.4g' % x)

CHOICE = {'q1.pilot': '止める', 'q2.vhat_iso': '零', 'q3.nk_iso': '零', 'q4.second': '零'}

T = json.load(open(os.path.join(PUB, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
T3 = json.load(open(os.path.join(PUB, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
FR = json.load(open(os.path.join(PUB, 'records', 'Bprime', 'FREEZE-RECORD-Bprime.json'), encoding='utf-8'))
P3 = json.load(open(os.path.join(PUB, 'records', 'predictions', 'predictions-Bl3-coordinator.json'), encoding='utf-8'))
REP = open(os.path.join(PUB, 'records', 'Bl3', 'results-Bl3-FINAL-2026-09-27.md'), encoding='utf-8').read()
EXPO_B = open(os.path.join(PUB, 'records', 'Bprime', 'exposure-before-seal-Bprime.md'), 'rb').read()
EXPO = EXPO_B.decode('utf-8')
assert sha16(EXPO_B) == FR['frozen_sha16']['records/Bprime/exposure-before-seal-Bprime.md']

# 選んだ値は正本の選択肢の内か
items = {it['key']: it['options'] for it in T['predictions']['items']}
assert set(CHOICE) == set(items), (set(CHOICE) ^ set(items))
for k, v in CHOICE.items():
    assert v in items[k], (k, v)

# 層三の下見の表（主の升目・縦棒をエスケープした表）
cells = []
L = REP.split('\n')
HEAD = '| 升目 | 主の升目 | 無操作の対数オッズ | 選択肢 a の確率（集合の中） | 変換の後の確率 | 質量 | 段階 B の無操作の破局の率 | (i)(ii) |'
blocks = []
for i, line in enumerate(L):
    if line == HEAD:
        rows = []
        for r in L[i + 2:]:
            if not r.startswith('|'):
                break
            rows.append(r)
        blocks.append(rows)
esc_blocks = [b for b in blocks if all('\\|' in r for r in b)]
assert len(blocks) == 2 and len(esc_blocks) == 1, (len(blocks), len(esc_blocks))
for line in esc_blocks[0]:
    c = [x.strip() for x in line.replace('\\|', '／').strip('|').split('|')]
    assert len(c) == 8, c
    if c[1] == 'はい':
        cells.append({'cell': c[0], 'lo': float(c[2]), 'mass': float(c[5]), 'ok': c[7]})
names = [c['cell'] for c in cells]
assert len(cells) == 8 and len(set(names)) == 8, names
assert all(c['mass'] == 1.0 for c in cells)
pb = T['pilot']['p_bounds']
assert pb == T3['pilot']['p_bounds'], (pb, T3['pilot']['p_bounds'])
lo_floor = math.log(pb[0] / (1 - pb[0]))
lo_ceil = math.log(pb[1] / (1 - pb[1]))
assert abs(lo_floor + lo_ceil) < 1e-9
out3 = [c for c in cells if not (lo_floor <= c['lo'] <= lo_ceil)]
assert len(out3) == 1 and all(c['ok'].startswith('満たさない') for c in out3) and sum(1 for c in cells if c['ok'].startswith('満たさない')) == 1
top3 = sorted(cells, key=lambda c: -abs(c['lo']))[:3]
assert all(c['lo'] < 0 for c in top3), top3            # 大きい三つは床の側（「床の外」と書くため）
mags = sorted((abs(c['lo']) for c in cells), reverse=True)
s2 = abs(lo_floor) / mags[1]
s3 = abs(lo_floor) / mags[2]
n_min = T['pilot']['decision']['cells_min_pass']
n_tot = T['pilot']['decision']['cells_total']
assert (n_tot, n_min) == (8, 6) and n_tot - n_min + 1 == 3   # 外れが三つで止める
lo_min, lo_max = min(c['lo'] for c in cells), max(c['lo'] for c in cells)

# 層三の主の札の要約と偶然の目安
m = re.search(r'^- 主の行 (\d+)（下見で外した後）・等方の外の行: v̂ (\d+)・Nk (\d+)・二つ目の札が付く行 (\d+)$', REP, re.M)
bl3_rows, bl3_v, bl3_nk, bl3_sec = m.groups()
m = re.search(r'二つ目の札の偶然の目安（Holm を掛けない・下見で外した後の行で数えた）: 向きまで数えて ([0-9.]+)・対の単位で ([0-9.]+)', REP)
ch_dir, ch_pair = m.groups()
m = re.search(r'\*\*下見の機械の決定\*\*:\s*\n\s*\n<!-- 機械:始 -->\n- ([^（\n]+)（', REP)
bl3_pilot = m.group(1)
assert bl3_pilot in T['pilot']['decision']['q1_map'], bl3_pilot

# B′ の Holm の最初の段（主の行がすべて残ったとき）
alpha = T['labels']['iso_outside']['holm_alpha']
m_rows = len(T['main_rows'])
K = FR['prefreeze']['g']['count']
maxk = max(k for k in range(K + 1) if 2 * (1 + k) / (1 + K) < alpha / m_rows)

# 露出の記録の E9 の数
m = re.search(r'測った行 (\d+)・\|z\| ≥ 16 の行 (\d+)', EXPO)
zrows, z16 = m.groups()
bl3_model = T3['inputs']['model']['repo']
bp_model = T['inputs']['model']['id']
assert bl3_model.startswith('Qwen/') and bp_model == 'google/gemma-4-31B-it', (bl3_model, bp_model)
cap = T['inputs']['model_facts']['final_logit_softcapping']
m = re.search(r'ほかの (\d+) 行の p は ([0-9.]+)〜([0-9.]+)', REP)
rest_n, rest_lo, rest_hi = m.groups()
assert int(rest_n) == int(bl3_rows) - int(bl3_v) - int(bl3_nk) and float(rest_hi) < 0.5

free = (
    '封印の前に見たもの: 封印の前の露出の記録 `records/Bprime/exposure-before-seal-Bprime.md`（SHA16 %s）を読んだ。記録を組んだのは私で、E1〜E9 と票の中の見込みの文は、どれも記録を組む前から見ている。'
    'ほかに、凍結した本文・正本・器・合成データの確かめの記録（乱数の小さな模型の値で、Gemma の値ではない）・下見の前の凍結の記録を見た。Gemma の場面の出力と読み取りの値は、誰もまだ計算していない。'
    '封印の直前に、層三の報告の最終版の下見の表（主の升目ごとの無操作の対数オッズと (i)(ii) の合否）と、主の札の要約（主の行 %s・等方の外 v̂ %s・Nk %s・二つ目の札 %s）を読み直した。\n'
    '採点の合成の応答と中立の課題の感触の書式: 露出の記録のとおり。合成の応答は、器が型から組んだ JSON の塊と、Gemma のチャットの型の印でできていて、感触の応答の字は使っていない。'
    'ただし形（思考の欄の印を置く形を含む）は感触の後に作ったので、形の選びに感触の知識が入りうる。\n'
    '考え方（q1）: q1 は、主の升目 %d のうち (i)(ii) を満たさない升目の数で決まる（一つも無ければ続ける・%d か %d なら一部を外して続ける・%d 以上なら止める）。'
    'バッチ一の繰り返しは意味のない列でビットで一致したので、(vi) の (b) で止まる見込みは小さいと見た。(i) の読み取りの集合の確率の和は、書き出しが JSON の choice の値の頭なので、どの升目でも高いと見た（層三ではすべて 1）。'
    '決め手は (ii) の床と天井（対数オッズで ±%s）。層三では無操作の対数オッズが %s〜%s に散り、床の外が一つだった。目安として、層三の値を一律に %s 倍を越えて強めると床の外が二つ、%s 倍を越えると三つになる。'
    'Gemma の応答の強さは見ていない。手がかりは弱く、層三の模型（%s）より大きい模型（%s）であることと、意味のない列でも測った行の約半分（%s／%s）で出口の値の絶対値が 16 以上だったこと（層三の同じ値は無い）だけ。'
    'Gemma は出口の値を softcap（上限 %s）で丸めるので、極端な値はむしろ抑えられる側にある。'
    'a が雛形の写しで天井に寄る道もある。止める見込みと一部を外して続ける見込みはほぼ同じで、同じくらいのときの決め（起草者が引かれる「続ける」の側と逆に置く）で、止める側に置いた。\n'
    '考え方（q2〜q4）: 本の計算まで進んだときの見込み（下見で止まれば採点されない）。主の行が %d すべて残れば、等方の外になるには、Holm の最初の段で、効き目と同じか外側にある等方の方向が %d 本のうち %d 本以下でなければならない。'
    '層三では、Holm の段を越えたのは v̂ の一行だけで、ほかの %s 行も p は %s〜%s と、どれも等方の効き目の真ん中の半分の外にはあったが、段には届かなかった。B′ でも同じ程度と見て、q2・q3 は零とした（q2 は「一から三」とほぼ同じで、q1 と同じ決めで零の側に置いた）。'
    '二つ目の札は、比べる相手の実在の差の方向の中で中心からの動きが最上位になることで、層三の、偶然で付く行の数の目安は %s〜%s（層三の実際は %s）。v̂ と Nk が実在の差の中で最上位になる理由は見当たらないので、零とした。\n'
    '確からしさ（主観・数を打たない）: q1 中の下（「一部の升目を外して続ける」とほぼ同じ）・q2 中の下（「一から三」とほぼ同じ）・q3 中・q4 中。\n'
    'この予想が確かめていないこと: Gemma の場面の入力の値は一つも見ていない。見込みは層三の値と作りから引いた推論で、層三の値を一律に強める目安は、Gemma の値が層三と同じ形のまま強まるとする仮定の上の数。'
) % (sha16(EXPO_B), bl3_rows, bl3_v, bl3_nk, bl3_sec,
     n_tot, 1, n_tot - n_min, n_tot - n_min + 1,
     fmt(abs(lo_floor)), fmt(lo_min), fmt(lo_max), fmt(s2), fmt(s3),
     bl3_model, bp_model, z16, zrows, fmt(cap),
     m_rows, K, maxk, rest_n, rest_lo, rest_hi, ch_dir, ch_pair, bl3_sec)
coi = ('起草者（この枠・正本・器を書いた）。下見を続ける側・札が立つ側に引かれる。層三では q1 を「%s」、v̂ と Nk の等方の外を「%s」「%s」と封印し、結果は「%s」・v̂ %s・Nk %s だった（引かれた側に外れた）。'
       '同じくらいのときは引かれる側と逆に置いた。') % (P3['q1.pilot'], P3['q2.vhat_iso'], P3['q3.nk_iso'], bl3_pilot, bl3_v, bl3_nk)
vals = dict(CHOICE)
vals['free'] = free
vals['info.coi'] = coi
assert not os.path.exists(OUT), OUT
b = (json.dumps(vals, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
open(OUT, 'wb').write(b)
print('[make_choices_coordinator_Bprime] 書いた: %s（%d バイト・SHA16 %s）' % (os.path.basename(OUT), len(b), sha16(b)))
print('free の字数 %d・coi の字数 %d' % (len(free), len(coi)))
