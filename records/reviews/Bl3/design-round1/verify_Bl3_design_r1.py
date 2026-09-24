# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の設計の巡・第一巡の四票の事実の主張を、一次記録・凍結の器・手元のトークナイザ・合成データで確かめる（再現の番号 K418〜）。
- 全経路の効き目は一つも計算しない（模型の順伝播をしない・重みを読まない）。トークナイザと、段階 B と B-lens の記録と、凍結した芯の関数と、合成の数だけを使う。
- 票の文は打ち直さない。票の所見は「票の名・所見の番号」で指し、確かめた内容は一次記録から器が切り出した文と、器が計算した数で書く。
出力: records/reviews/Bl3/design-round1/verify-Bl3-design-r1.json・verification-Bl3-design-r1.md
用法: python records/reviews/Bl3/design-round1/verify_Bl3_design_r1.py <会話の記録 jsonl>
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, math, hashlib, datetime, collections, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
import blens_core as C                  # 凍結（読み取りだけ）
import run_stageB_local as RB           # 凍結（読み取りだけ）
import steer_B                          # 凍結（読み取りだけ）
T3 = json.load(open(j('design', 'contrasts-Bl3.json'), encoding='utf-8'))
TB = json.load(open(j('design', 'contrasts-B.json'), encoding='utf-8'))
TL = json.load(open(j('design', 'contrasts-Blens.json'), encoding='utf-8'))
FJ = json.load(open(j('records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
AN = json.load(open(j('records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
P2 = rd('records/reviews/Bl3/design-round1/bundle-Bl3-design-part2.md').split(NL)
DRAFT = rd('design/design-Bl3-draft1.md')
DL = DRAFT.split(NL)
line2 = lambda n: P2[n - 1]                         # 束の分けた版 2／2 の n 行目（票が引いた行の番号）
K, k0 = [], 418


def add(votes, claim, method, result, evidence):
    K.append({'id': 'K%d' % (k0 + len(K)), 'votes': votes, 'claim': claim, 'method': method, 'result': result, 'evidence': evidence})


def must(cond, msg):
    assert cond, msg


# ---------------- 1. 割合の刻みと Holm の段（合成の数・凍結の芯の関数） ----------------
Kiso = T3['nulls']['isotropic']['count']
alpha = T3['labels']['iso_outside']['holm_alpha']
p_of = lambda e: C.p_equal_tailed(1.0, [2.0] * e + [0.0] * (Kiso - e))           # 帰無のうち e 本が観測と同じか外側
pv = {e: p_of(e) for e in range(0, 40)}
def max_pass(m):
    out = []
    for step in range(1, m + 1):
        thr = alpha / (m - step + 1)
        ok = [pv[e] for e in pv if pv[e] < thr]
        out.append(max(ok) if ok else None)
    return out
mp16, mp12 = max_pass(16), max_pass(12)
must(abs(pv[0] - T3['labels']['p_min']) < 1e-12 and abs(pv[1] - 0.004) < 1e-12, '割合の刻みが正本と合わない')
add(['G1-4-1', 'G2-2', 'C1-L1', 'C2-R6'], '等方の帰無 999 本・両側に等しい裾の割合で、最小の p は 0.002、一本が同じか外側なら 0.004 で、十六行の Holm の第一段を通らない。十六行で 0.004 が通るのは第五段から（票の段の表）',
    '凍結の `blens_core.p_equal_tailed` に、帰無のうち e 本だけが観測と同じか外側の合成の値を入れ、Holm の各段の閾値（水準 ÷ 残りの行の数・下回ると通る）と比べた',
    '再現', '外側の本数 e と p: %s。十六行で各段を通る p の最大: %s。十二行（二升目を外したとき）: %s' % (
        '・'.join('e=%d→%.3f' % (e, pv[e]) for e in range(0, 6)),
        '・'.join('%d段 %s' % (i + 1, ('%.3f' % x) if x is not None else '無し') for i, x in enumerate(mp16)),
        '・'.join('%d段 %s' % (i + 1, ('%.3f' % x) if x is not None else '無し') for i, x in enumerate(mp12))))
Kb = TL['nulls']['isotropic']['count']
add(['G1-4-1'], 'B-lens の等方の帰無（零を中心に対称な割合）では最小の p が 0.001 で、一本が外側でも第一段を通った',
    'B-lens の正本の本数で `blens_core.p_two_sided` の最小と、一本が外側のときの値を計算した',
    '再現（票は本数を 1000 として 1/1000 と書いたが、B-lens の本数では 1/(1+%d)）' % Kb,
    'B-lens の本数 %d・最小 %.6f・一本が外側 %.6f（十六行の第一段 %.6f の内）' % (Kb, C.p_two_sided(1.0, [0.0] * Kb), C.p_two_sided(1.0, [2.0] + [0.0] * (Kb - 1)), alpha / 16))
R0 = rd('records/Bl3/rulings-D204-D209.md')
i0 = R0.index('999 本なら割合の最小は')
sent = R0[i0:R0.index('。', i0) + 1]
add(['C2-R6'], '本数を承認した根拠の文（裁定の前の案）は、対称の割合で最小 0.001 と書いていた。数え方を改めた後の値で、登録者が本数を確かめ直すべき',
    '裁定の記録 `records/Bl3/rulings-D204-D209.md`（逐語の案）から、根拠の文を器が切り出した', '再現（承認の前提が、草案1 の読み直しで変わった）', '案の文（逐語）: 「%s」。草案1 の最小は %.3f' % (sent, pv[0]))

# ---------------- 2. 芯の関数の線形の口 ----------------
src_core = rd('tools/blens_core.py')
gl = [l.strip() for l in src_core.split(NL) if 'x = sg * V[' in l]
tl = [l.strip() for l in src_core.split(NL) if 'np.all(abs(m) > c)' in l]
must(len(gl) == 1 and len(tl) == 1, '芯の関数の行が見つからない')
units = ['static', 'loaded', 'Nk', 'td', 'rand:0', 'rand:1', 'rand:2']
GR = FJ['facts']['C']['gate_rows']
cs_of = lambda r: '%s|%s|%+d' % (r['scenario'], r['base'], r['sign'])
css = sorted({cs_of(r) for r in GR})
rng = np.random.default_rng(20260924)
Vs = {u: {cs: float(rng.normal()) for cs in css} for u in units}                  # 符号つきの方向を加えた効き目（合成）
yy = {id(r): Vs[r['unit']][cs_of(r)] + 0.05 * float(rng.normal()) for r in GR}     # 行動が押しとそろう合成
ok_rows = [{'unit': r['unit'], 'sign': 1, 'fam': cs_of(r), 'y': yy[id(r)]} for r in GR]
bad_rows = [{'unit': r['unit'], 'sign': r['sign'], 'fam': cs_of(r), 'y': yy[id(r)]} for r in GR]
g_ok, g_bad = C.gate_perm(ok_rows, Vs, units), C.gate_perm(bad_rows, Vs, units)
add(['C1-S2', 'C2-R2'], '門の関数は押しを「行の符号 × 単位と家族の値」で作り、最上位の判定は零を中心に |値| で比べる（線形の口）。層三の押し（符号つきの方向を加えた効き目）で行の符号を渡すと、減算の行で符号が二重にかかる',
    '凍結の `tools/blens_core.py` の該当の行を器が切り出し、門の行の形（転記行 C の 64 行）で、押しと行動がそろう合成の数を二通りの呼び方で門に通した',
    '再現', '門の関数の行: `%s`・最上位の判定の行: `%s`。合成: 行の符号を +1 にした呼び方 ρ=%.3f・p=%.4f／行の符号を渡した呼び方 ρ=%.3f・p=%.4f（減算の行 %d 行で符号が反転する）' % (
        gl[0], tl[0], g_ok['rho'], g_ok['p'], g_bad['rho'], g_bad['p'], sum(1 for r in GR if r['sign'] < 0)))

# ---------------- 3. transformers 4.57.3 の出口の値と hidden_states ----------------
import transformers
TD = os.path.dirname(transformers.__file__)
mq = open(os.path.join(TD, 'models', 'qwen3', 'modeling_qwen3.py'), encoding='utf-8').read()
ge = open(os.path.join(TD, 'utils', 'generic.py'), encoding='utf-8').read()
c1 = [l.strip() for l in mq.split(NL) if 'do not upcast them to float' in l]
c2 = [l.strip() for l in mq.split(NL) if 'logits = self.lm_head(' in l]
c3 = [l.strip() for l in ge.split(NL) if 'Whether to overwrite `out.hidden_states[-1]`' in l]
c4 = [l.strip() for l in ge.split(NL) if 'collected_outputs[key] += (outputs.last_hidden_state,)' in l]
c5 = [l.strip() for l in mq.split(NL) if l.strip() == '@check_model_inputs()']
must(transformers.__version__ == TB['runner'].get('transformers', transformers.__version__) or True, '')
add(['C1-S1', 'C2-R3'], 'transformers 4.57.3 の Qwen3 は、損失を計算しないとき出口の値を浮動小数に上げない（bf16 の刻みが効き目に乗る）',
    '手元に入っている transformers（版 %s・段階 B と B-lens の版と同じ）の `models/qwen3/modeling_qwen3.py` から該当の行を器が切り出した' % transformers.__version__,
    '再現' if (c1 and c2 and transformers.__version__ == T3['inputs']['versions_B']['transformers']) else '要確認',
    '行: `%s`／`%s`。版の一致: 手元 %s・正本 %s' % (c1[0] if c1 else '無し', c2[0] if c2 else '無し', transformers.__version__, T3['inputs']['versions_B']['transformers']))
add(['C1-M7'], '`check_model_inputs(tie_last_hidden_states=True)` は hidden_states の最後の要素を、最終の正規化の後の値で上書きする。そこに最終の正規化を当てると二重にかかる',
    '同じ版の `utils/generic.py` と `modeling_qwen3.py` から該当の行を器が切り出した', '再現' if (c3 and c4 and c5) else '要確認',
    '行: `%s`／`%s`／`Qwen3Model.forward` の飾り `%s`' % (c3[0] if c3 else '無し', c4[0] if c4 else '無し', c5[0] if c5 else '無し'))
hsi = T3['layers']['hidden_states_indices'][str(T3['layers']['selected_ratio'])]
li = T3['layers']['indices'][str(T3['layers']['selected_ratio'])]
rsrc = rd('tools/run_stageB_local.py')
hk = [l.strip() for l in rsrc.split(NL) if 'torch.as_tensor(V, dtype=hs.dtype' in l]
sec2 = [l for l in DL if l.startswith('- **組み立ての関数**')][0]
add(['C2-R3', 'C1-M6'], '加減の置き場（層 17 の出力＝hidden_states の 18）と、加減の関数が §2 の呼ぶ関数に無い。段階 B の加減はバッチ全体に一本のベクトルを足す形で、方向ごとに違うベクトルを一つのバッチで足すのは新しい道になる',
    '正本の層の添字、段階 B の走行器の加減の行、草案1 §2 の行を器が切り出した', '再現',
    '層の添字 %d・hidden_states の添字 %d。段階 B の加減の行: `%s`（一本のベクトルを層の出力の型に直して足す）。§2 の行に加減の関数の名が無い: %s' % (li, hsi, hk[0] if hk else '無し', 'apply_vector' not in sec2 and 'hook' not in sec2))

# ---------------- 4. B-lens の最終版の行（票が引いた束の行） ----------------
chk = [(209, ['0.0942']), (224, ['S1|Onull 8', 'bf16']), (108, ['108 のうち 12', '3.72']), (457, ['共分散']), (432, ['p8', '(6b)']), (433, ['封印の前']), (515, ['bf16']),
       (578, ['cross:S4:O-Ncold+vNk', '判定保留（様式転位）']), (684, ['80.0／19.0', '61.0 pt']), (591, ['sub:N1:O-Ncold-v', '-2.0'])]
for n, ws in chk:
    must(all(w in line2(n) for w in ws), ('束の行が票の読みと合わない', n, ws))
row176 = [l for l in P2[170:200] if l.startswith('| S4|O-Ncold+vNk|Nk')]
must(len(row176) >= 1, '176〜196 行の S4|O-Ncold+vNk の行が無い')
add(['C1-S1'], 'B-lens の最終版の逸脱 D-BL3 の記録に、手元で組み直した出口の値と Colab の模型の出口の値の差（最大 0.0942）と、入力の長さの違いで主位置の残差が要素で最大 8 動いた記録がある',
    '束の分けた版 2／2 の 209 行と 224 行を器が読んだ', '再現', '209 行: %s／224 行（頭）: %s' % (line2(209)[:160], line2(224)[:200]))
add(['C1-M1', 'C2-R4'], '段階 B は主の行 cross:S4:O-Ncold+vNk を様式の転位で判定保留とし（JSON 直答 80.0／19.0）、B-lens の直接の経路はこの切り替えを説明できなかった。S4|O-Ncold の JSON 直答は無操作 0・+vNk 160・+vrand 38・−vrand 17',
    '束の分けた版 2／2 の 578・684 行と 176〜196 行の表の行、設計の事実の JSON 直答の升目の内訳を器が読んだ', '再現',
    '578 行: %s／684 行: %s／表の行: %s／設計の事実: %s' % (line2(578)[:130], line2(684)[:110], row176[0][:120],
        '・'.join('%s %d' % (k, v) for k, v in sorted(FJ['facts']['A']['json_direct_by_cell'].items()) if k.startswith('S4|O-Ncold'))))
cc = collections.Counter()
for arm in ('Osec-Ncold+vrand', 'Osec-Ncold+v6b'):
    for l in open(glob.glob(j('results', 'stageB', 'stageB__S4__%s__s1' % arm, 'trials-*.jsonl'))[0], encoding='utf-8'):
        t = json.loads(l)
        if t['status'] == 'ok':
            cc[(arm, t['direction_id'], t['style_b'], t['choice'])] += 1
add(['C2-R4'], '門の行の S4|Osec-Ncold+v6b と rand:0 は、全試行が JSON 直答の c だった',
    '段階 B の試行の記録を方向の番号ごとに数えた', '再現',
    '・'.join('%s〔%s〕JSON直答=%s 選択 %s: %d' % (a, d, sb, ch, n) for (a, d, sb, ch), n in sorted(cc.items()) if d in ('rand:0', 'loaded')))

# ---------------- 5. 二つ目の札の偶然の目安（合成の数） ----------------
v_rows = sum(1 for r in T3['main_rows'] if r['direction'] == 'static')
nk_rows = sum(1 for r in T3['main_rows'] if r['direction'] == 'Nk')
co, cp = T3['nulls']['real']['comparators_oriented'], T3['nulls']['real']['comparators']
mirror = round(v_rows / (cp['static'] + 1) + nk_rows / (cp['Nk'] + 1), 4)
rs = np.random.default_rng(20260925)
Nsim, npair = 200000, cp['static']
sim = {}
for eps in (0.0, 0.25, 0.5, 1.0, 2.0, 5.0, 20.0):
    o = rs.normal(size=(Nsim, npair + 1))
    ep, em = rs.normal(size=(Nsim, npair + 1)), rs.normal(size=(Nsim, npair + 1))
    row = np.abs(o[:, 0] + eps * ep[:, 0])
    comp = np.maximum(np.abs(o[:, 1:] + eps * ep[:, 1:]), np.abs(-o[:, 1:] + eps * em[:, 1:])).max(axis=1)
    sim[eps] = float(np.mean(row > comp))
add(['C1-M2', 'C2-R5'], '偶然の目安 0.3087 は向きまで数えた相手を別々の相手として数えた値で、効き目がほぼ奇（±d がほぼ鏡）なら実質の相手は対の数になり、目安は 0.6057 になる。B-lens の直接の経路では、ランダム方向が実在の差の最上位に来た升目が 108 のうち 12（交換可能なら 3.72）',
    '正本の比べる相手の数から二つの目安を計算し、票の合成の形（対の値＝奇の部分＋奇でない部分×ε・奇でない部分は向きごとに独立）で、一行が最上位になる割合を %d 回の合成で数えた（v̂ の相手 %d 対）。B-lens の記録は束の分けた版 2／2 の 108 行' % (Nsim, npair),
    '再現', '正本の目安 %.4f（向きまで数えた %d・%d）／対の単位の目安 %.4f（%d・%d）。一行が最上位になる割合: %s（1/%d=%.4f・1/%d=%.4f）。108 行: %s' % (
        T3['nulls']['real']['chance_second'], co['static'], co['Nk'], mirror, cp['static'], cp['Nk'],
        '・'.join('ε=%g→%.4f' % (e, p) for e, p in sim.items()), npair + 1, 1 / (npair + 1), 2 * npair + 1, 1 / (2 * npair + 1), line2(108).strip()))
l15 = [l for l in DL if '向きを数えることは二つ目の札を付きにくくする' in l]
must(len(l15) == 1, '§15 の文が見つからない')
add(['C2-R5'], '草案1 §15 の「向きを数えることは二つ目の札を付きにくくする」は、効き目がほぼ線形のときにはほとんど当たらず、一方で印字する目安は半分になる（札を珍しく見せる向きの傾き）',
    '上の合成の数で、ε が零に近いときの最上位の割合を、向きを数えない相手（対 %d）での割合 1/%d と比べた' % (npair, npair + 1),
    '再現（起草者の文の誤り）', 'ε=0 の最上位の割合 %.4f（向きを数えない 1/%d=%.4f とほぼ同じ）。正本の目安は %.4f で、対の単位の %.4f の約半分' % (sim[0.0], npair + 1, 1 / (npair + 1), T3['nulls']['real']['chance_second'], mirror))

# ---------------- 6. 正本と草案の抜け・古い所 ----------------
canon_txt = json.dumps(T3, ensure_ascii=False)
add(['C1-M8'], 'B-lens は限界に「活性の共分散に沿う帰無は置かない（層三かその後）」と書いたが、草案1 は置くとも置かないとも書いていない',
    '束の分けた版 2／2 の 457 行と、草案1 と正本の文を器が走査した', '再現', '457 行: %s／草案1 の「共分散」: %d 件・正本: %d 件' % (line2(457).strip(), DRAFT.count('共分散'), canon_txt.count('共分散')))
add(['C1-L3'], '段階 B の v̂ の腕と無操作の差には零に近い行があり（sub:N1 は −2.0 pt）、B-lens の p8 は零に近い値の符号で答えが決まった',
    '束の分けた版 2／2 の 591 行と 432 行を器が読んだ', '再現', '591 行（末尾）: %s／432 行: %s' % (line2(591)[-60:], line2(432)[:150]))
add(['C1-L7', 'C2-R15'], '正本の `numbering.rulings_next` が D210 のまま・`inputs.files` に D210 の記録が無い・§16 と `drafter_values` に裁定済みの封印の時が残る',
    '正本と草案1 を器が読んだ（草案1 は D210 の前に組んだもので、正本への D210 の記帳は草案2 で行うと裁定の記録に書いた）', '再現（草案2 で直す予定の所）',
    'rulings_next %s・inputs.files の裁定の記録 %s・drafter_values に predictions.when: %s・§16 の封印の時の行: %s' % (
        T3['numbering']['rulings_next'], [v['path'] for v in T3['inputs']['files'].values() if 'rulings' in v['path']], 'predictions.when' in T3['drafter_values'],
        any('**封印の時**（登録者の裁定を要する）' in l for l in DL)))
ga = FJ['facts']['C']['gate_a_not_catastrophe']
sk = sum(v for k, v in ga.items() if k.startswith('SK|Onull'))
nb = sum(v['a_not_catastrophe'] for v in FJ['facts']['B']['cells'].values() if v['in_main'])
add(['C2-R14', 'G2-3'], '量が零の (a) は門の行の 13 行に計 29 件で、うち 20 件が SK|Onull の行に寄る。無操作の主の升目にも 4 件ある',
    '設計の事実の転記行 B・C の数を器が数えた', '再現', '門の行で量が零の (a) がある行 %d・合計 %d・SK|Onull の行 %d。無操作の主の升目 %d' % (sum(1 for v in ga.values() if v), sum(ga.values()), sk, nb))
seeds_B = sorted({v for p_, v in [(k, v) for k, v in TB['seeds'].items() if isinstance(v, int)]} | set(TB['seeds'].get('random_dirs', {}).values()) | set(TB['seeds'].get('tune', {}).values()) | set(TB['seeds'].get('main', {}).values()))
msrc = rd('tools/make_contrasts_Bl3.py')
sa = [l.strip() for l in msrc.split(NL) if '種が B-lens と重なる' in l]
add(['C2-R16'], '種 91001 が新しい種であることを、器は段階 B の種とは突き合わせていない',
    '段階 B の正本 `seeds` の整数の値を器が集め、正本の生成器の assert の行を切り出した', '再現（種は段階 B のどの種とも違うが、器の assert は B-lens の種だけを見る）',
    '段階 B の種: %s・層三の種 %d は含まれない: %s。assert の行: `%s`' % ('・'.join(str(x) for x in seeds_B), T3['nulls']['isotropic']['seed'], T3['nulls']['isotropic']['seed'] not in seeds_B, sa[0] if sa else '無し'))
lens = [v['prompt_len'] for v in FJ['facts']['B']['cells'].values()]
npre = len(FJ['facts']['A']['prefix_ids'])
add(['C2-R17'], '近道が使えないとき一回の長さは 475〜564 位置になり、費用の見込みに層ごとの差分・乙・独立の再計算の分が入っていない',
    '転記行 B のプロンプトの長さと書き出しの長さ、正本の `cost.note` を器が読んだ', '再現', '長さ %d〜%d（プロンプト %d〜%d ＋ 書き出し %d）・費用の注: %s' % (min(lens) + npre, max(lens) + npre, min(lens), max(lens), npre, T3['cost']['note']))
rk = list(json.loads(open(glob.glob(j('results', 'stageB', 'stageB__S1__Onull__s1', 'raw-*.jsonl'))[0], encoding='utf-8').readline()).keys())
add(['C2-R18'], '書き出しの割り方の確かめは出力の文字列を割り直して比べている。生成したトークンの並びが記録にあれば、それと比べる',
    '段階 B の生の出力の記録の欄を器が読んだ', '再現せず（段階 B の生の出力の記録にトークンの並びの欄が無いので、割り直しのほかに比べる相手が無い）', '欄: %s' % '・'.join(rk))

# ---------------- 7. 書き出しとプロンプトの雛形の重なり・refuse の頭（トークナイザだけ） ----------------
from transformers import AutoTokenizer
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % T3['inputs']['model']['rev'])
tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
dec = lambda i: tok.decode([int(i)]).replace(NL, '⏎')
PI = FJ['facts']['A']['prefix_ids']
AT = RB.arm_texts()
ov = collections.OrderedDict()
for key in FJ['facts']['B']['cells']:
    sc, arm = key.split('|')
    scen, inst = RB.scenario_and_instruction(sc)
    ids = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
    o7 = [i for i in range(len(ids) - len(PI) + 1) if ids[i:i + len(PI)] == PI]
    o1 = [i for i in range(len(ids) - 1) if ids[i] == PI[-1]]
    ov[key] = {'full_prefix_count': len(o7), 'next_after_full': [dec(ids[i + len(PI)]) for i in o7], 'last_token_count': len(o1),
               'next_after_last': dict(collections.Counter(dec(ids[i + 1]) for i in o1))}
all_a = all(v['full_prefix_count'] == 1 and v['next_after_full'] == ['a'] for v in ov.values())
ref_cue = all(v['next_after_last'].get('ref', 0) >= 1 for v in ov.values())
add(['C2-R1'], '読み取りの書き出しは、プロンプトの中の JSON の指示の雛形の頭と同じ並びで、雛形ではその次が a（破局の文字）。refuse の頭の ref にも、書き出しの最後と同じ字面のトークンの直後という手がかりがある',
    '手元のトークナイザで、九つの升目のプロンプト（段階 B の凍結の組み立てのまま）の中に、書き出しの %d トークンの並びと、書き出しの最後のトークンが現れる所を数え、次のトークンを戻した（順伝播はしない）' % len(PI),
    '再現' if (all_a and ref_cue) else '一部再現',
    '書き出しの並びの全体: どの升目でも %s。書き出しの最後のトークン「%s」: %s' % (
        '一回・次は a' if all_a else json.dumps({k: (v['full_prefix_count'], v['next_after_full']) for k, v in ov.items()}, ensure_ascii=False),
        dec(PI[-1]), '・'.join('%s %d 回（次の中の ref %d）' % (k, v['last_token_count'], v['next_after_last'].get('ref', 0)) for k, v in ov.items())))
V0 = FJ['facts']['A']['prefix']
nx = collections.Counter()
for d in sorted(glob.glob(j('results', 'stageB', 'stageB__*__s1'))):
    TT = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}
    for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8'):
        o = json.loads(l)
        t = TT[o['trial_id']]
        if t['status'] == 'ok' and t['choice'] == 'refuse':
            tx = o['text']
            i = tx.rfind(V0)
            if i < 0:
                nx['書き出し無し'] += 1
                continue
            e = tok.encode(tx[i:], add_special_tokens=False)
            nx[dec(e[len(PI)]) if e[:len(PI)] == PI else '割り方が違う'] += 1
add(['G2-Q2'], 'refuse の頭のトークン ref は、JSON 直答の型の出力に refuse が無いので、実物で確かめられていない',
    '段階 B で refuse を選んだ使えた試行の出力（散文の JSON）で、書き出しの次のトークンを手元のトークナイザで数えた', '確かめた（票の心配には当たらない）',
    'refuse を選んだ出力 %d 件の書き出しの次のトークン: %s' % (sum(nx.values()), '・'.join('%s %d' % kv for kv in sorted(nx.items()))))

# ---------------- 8. 段階 B のランダム方向の腕の率・逸脱 D-BL3 の中身 ----------------
BD = AN['by_direction']
noop = {(r['scenario'], r['arm']): r for r in BD if r['direction_id'] == 'fixed' and '+v' not in r['arm'] and '-v' not in r['arm']}
ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')
agg = collections.defaultdict(lambda: [0, 0])
for r in BD:
    m = ARM_RE.match(r['arm'])
    if m and m.group(3) == 'rand':
        agg[(r['scenario'], r['arm'])][0] += r['cat']
        agg[(r['scenario'], r['arm'])][1] += r['n_ok']
dd = []
for (sc, arm), (c_, n_) in agg.items():
    b = noop[(sc, ARM_RE.match(arm).group(1))]
    dd.append(100 * (c_ / n_ - b['cat'] / b['n_ok']))
ad = sorted(abs(x) for x in dd)
bf = rd('records/B/results-B-FINAL-2026-09-23.md').split(NL)
het = [l for l in bf if l.startswith('- ランダム方向の不均一の注が付く確証の札')]
add(['G2-5'], '段階 B の本走行では、ランダム方向三本の平均は無操作のすぐ近くにあった',
    '凍結した集計器の記録の方向ごとの行から、ランダム方向の腕（三本を合わせた率）と無操作の腕の破局の率の差を数え、段階 B の最終版の不均一の注の行を切り出した',
    '一部再現（三本を合わせた腕の率は無操作に近いが、三本の間の開きには段階 B の最終版が注を付けている）',
    '腕 %d 本・差の絶対値の中央値 %.1f pt・最大 %.1f pt・5 pt 以上 %d 本。最終版の行: %s' % (len(dd), ad[len(ad) // 2], ad[-1], sum(1 for x in ad if x >= 5), het[0][:160] if het else '無し'))
fr = [l for l in rd('records/Blens/FREEZE-RECORD-Blens.md').split(NL) if l.startswith('| D-BL3 | ')]
add(['G2-Q6', 'G2-Q9'], 'B-lens の逸脱 D-BL3 は、器が出力を含め忘れた型の誤り',
    'B-lens の凍結の記録の台帳の行を器が切り出した', '再現', fr[0][:260] if fr else '無し')

# ---------------- 9. 正本の抜け（下見・門・読み・予想・乙・帯・独立の再計算・露出） ----------------
pk = set(T3['pilot']['decision'].keys()) | set(T3['pilot'].keys())
add(['G1-3-2', 'G2-1', 'C1-M4', 'C2-R8'], '下見で外した升目の門の行の扱い・門だけの升目 S4|Osec-Ncold の下見・外した後の Holm の段と偶然の目安と予想の分母・族（nuclear）の脱落・(v) が許容の外のときの範囲・q1 と機械の決定の対応が、正本に無い',
    '正本の `pilot`・`gate`・`predictions` の鍵と文を器が走査した', '再現',
    '下見の升目: %s（門だけの升目は入らない）・門の行の数は固定 %d／%d・`pilot` の鍵: %s・q1 の選択肢: %s' % (
        '・'.join('|'.join(c) for c in T3['cells_main']), T3['gate']['rows_gate'], T3['gate']['rows_without_vhat'], '・'.join(sorted(pk)), '／'.join(T3['predictions']['items'][0]['options'])))
types = [r['type'] for r in T3['reading_rules']]
add(['G2-4', 'C2-R10'], '読みの表に、下見で一部の升目を外したときの型と、行ごとの「外でない」の型が無い。裾の側の決まりは、効き目が零を越えて反対側にあるとき「押しが弱い側」と誤る。q7 の向きの基準が無い',
    '正本の読みの表の型の名と `labels.side_rule` と q7 を器が読み、零を越える場合を合成の数で当てた', '再現',
    '型: %s。裾の側の決まり: %s。合成: 帰無の中央値 −0.30・効き目 +0.20（上の裾・零を越えた反対側）は、決まりでは「零に近い側の裾」に当たり「押しが弱い」と書く形になる。q7: %s' % (
        '・'.join(types), T3['labels']['side_rule'], T3['predictions']['items'][6]['ask']))
add(['G1-8-1', 'C1-L3', 'C2-R10'], 'q7 は「外の行が無い」を選択肢に持ち、q2 が零なら決まる（従属）',
    '正本の予想の項目を器が読んだ', '再現', 'q2 の選択肢: %s／q7 の選択肢: %s' % ('／'.join(T3['predictions']['items'][1]['options']), '／'.join(T3['predictions']['items'][6]['options'])))
add(['C2-R12'], '乙の帯（教師強制の推論の文を帯に含むか）が書かれていない', '正本の `readout.secondary` を器が読んだ', '再現', json.dumps(T3['readout']['secondary'], ensure_ascii=False))
units_c = collections.Counter(r['unit'] for r in GR)
add(['C2-R13'], 'v̂ を抜いた門にも、兄弟の (6b) の行が残る', '転記行 C の門の行の単位と、正本の `gate.without_vhat` を器が読んだ', '再現',
    'v̂ を抜いた門の決まり: %s／(6b)〔loaded〕の行 %d' % (T3['gate']['without_vhat'], units_c['loaded']))
add(['G1-2-1'], '教師強制の書き出しの位置にも加減を掛ける理由が、本文にも正本にも無い', '正本の `readout.primary.band` を器が読んだ', '再現（理由の欠落）', T3['readout']['primary']['band'])
add(['G1-2-2', 'C1-L2'], '加えた腕で、選択の文字と refuse の頭の確率の和が保たれるかの決まりが無い', '正本の `pilot` と `labels` を器が走査した', '再現',
    '質量の決まりは下見の (i) だけ: %s' % T3['pilot']['checks']['i']['rule'])
add(['G1-9-1'], '加減の掛かった近道の確かめは、合成の小さな模型で行うとしている', '正本の `pilot.checks.v.rule` を器が読んだ', '再現（書かれているとおり）', T3['pilot']['checks']['v']['rule'])
add(['C1-M6'], '独立の再計算の書き手・許容・食い違ったときの扱いが無い', '正本の `independent_recompute` を器が読んだ', '再現', T3['independent_recompute'])
add(['C1-M5', 'C2-R8'], 'B-lens では予想者が封印の前に凍結の前の確かめの出力を見た。層三の正本には、封印の前に本物の模型で読み取りの値を印字しない決まりが無い',
    '束の分けた版 2／2 の 433 行と、正本の文の走査', '再現', '433 行: %s／正本の「露出」: %d 件' % (line2(433)[:170], canon_txt.count('露出')))

# ---------------- 10. 禁止語の衝突（起草者の器の抜け） ----------------
PS = T3['print_strings']
ban = sorted(set(PS['value_word_ban'] + PS['mechanism_word_ban'] + PS['added_ban']))
printed = []


def walk(x, path):
    if isinstance(x, dict):
        for k_, v_ in x.items():
            if k_ in ('never', 'decisions', 'clause', 'print_strings'):
                continue
            walk(v_, path + '.' + k_)
    elif isinstance(x, list):
        for q_, v_ in enumerate(x):
            walk(v_, '%s[%d]' % (path, q_))
    elif isinstance(x, str):
        printed.append((path, x))


for key in ('limits', 'negation_templates', 'reading_rules', 'descriptive', 'labels', 'scope', 'readout', 'gate', 'nulls', 'pilot'):
    walk(T3[key], '$.' + key)
walk({'never_note': T3['descriptive']['layerwise']['never']}, '$.descriptive.layerwise')
hits = sorted({(p_, w) for p_, s_ in printed for w in ban if w in s_})
sk_line = [l.strip() for l in msrc.split(NL) if "k_ == 'never'" in l]
add(['C1-M7'], '正本の注「転換層の読みは付けない」は、正本が足した禁止語「転換層」に当たる（印字されうる文の禁止語の走査で一件）',
    '正本の印字されうる文（限界・定型・読みの表・記述・札・範囲・読み取り・門・帰無・下見の文と、`descriptive.layerwise.never` の注）を、正本の禁止語の一覧で器が走査し、正本の生成器の禁止語の走査の行を切り出した',
    '再現（起草者の器は `never` の鍵を飛ばして走査していた）', '当たり %d 件: %s。生成器の走査の行: `%s`' % (len(hits), '・'.join('%s〔%s〕' % h for h in hits), sk_line[0] if sk_line else '無し'))

# ---------------- 11. 門の妥当性（升目ごとの共通の動き・合成の数） ----------------
rg = np.random.default_rng(20260926)
nsim, pp, pn = 400, [], []
for _ in range(nsim):
    off = {cs: float(rg.normal()) for cs in css}
    Vn = {u: {cs: off[cs] + float(rg.normal()) for cs in css} for u in units}           # 方向に固有の揃いは無い（帰無）
    rows = [{'unit': r['unit'], 'sign': 1, 'fam': cs_of(r), 'y': 1.0 * off[cs_of(r)] + float(rg.normal())} for r in GR]
    g = C.gate_perm(rows, Vn, units)
    pp.append(g['p'])
    x = np.array([Vn[r['unit']][r['fam']] for r in rows]); y = np.array([r['y'] for r in rows])
    rho = C.spearman(x, y)
    tstat = rho * math.sqrt((len(rows) - 2) / max(1e-12, 1 - rho * rho))
    pn.append(0.5 * math.erfc(tstat / math.sqrt(2)))                                       # 行を独立とみなす素朴な片側の近似
fp_perm, fp_naive = float(np.mean(np.array(pp) < alpha)), float(np.mean(np.array(pn) < alpha))
add(['G1-5-1', 'G2-5', 'C1-L6', 'C2-Q5'], '門の押しを中心化しないと、升目ごとの共通の動きが順位を決めて見かけの相関が生じる（G1-5-1・G2-5）。方向を単位にした入れ替えは行の升目と符号を保つので、共通の動きは観測にも入れ替えにも同じく入り、検定の正しさは変わらず、変わるのは検出力（C1-L6・C2-Q5）',
    '門の行の形（転記行 C の 64 行・七つの単位）で、方向に固有の揃いが無い合成（押し＝升目と符号ごとの共通の動き＋方向ごとの揺れ・行動＝同じ共通の動き＋揺れ）を %d 回作り、凍結の `gate_perm`（正しい呼び方）と、行を独立とみなす素朴な順位相関の検定で、水準 %.2f を下回る割合を数えた' % (nsim, alpha),
    '一部再現（素朴な検定なら見かけの相関で偽って通るが、方向を単位にした入れ替えでは名目の水準に近い。検出力への効きは確かめていない）',
    '水準を下回った割合: 入れ替えの門 %.3f・素朴な検定 %.3f' % (fp_perm, fp_naive))

# ---------------- 12. 閾値を置いた時点の情報状態（会話の記録の時刻） ----------------
pats = {'閾値（p の範囲・質量の下限・升目の数）を正本の生成器に書いた': "'cells_min_pass': 6", 'JSON 直答がすべて c という器の出力を見た': 'c 725'}
first = {}
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    ts = o.get('timestamp')
    cn = (o.get('message') or {}).get('content')
    if not ts or not isinstance(cn, list):
        continue
    for x in cn:
        if not isinstance(x, dict):
            continue
        s_ = json.dumps(x.get('input', ''), ensure_ascii=False) if x.get('type') == 'tool_use' else (json.dumps(x.get('content', ''), ensure_ascii=False) if x.get('type') == 'tool_result' else '')
        for k_, p_ in pats.items():
            if k_ not in first and p_ in s_:
                first[k_] = jst(ts)
must(len(first) == 2, ('時刻が取れない', first))
add(['C1-M4', 'C2-R9'], '下見の閾値は、段階 B の出力（転記行 A の「JSON 直答はすべて c」）を見た後に置かれ、続ける側に緩い。升目の数 6 は S4 の主の二升目が外れても続けられる値と一致する',
    '会話の記録から、閾値を正本の生成器に最初に書いた時刻と、器の出力で「JSON 直答がすべて c」を最初に見た時刻を器が取った。裁定の前の案の閾値の文を読んだ',
    '一部再現（閾値は段階 B と B-lens の公開済みの結果を見た後に置いたが、転記行 A の事実を器で見る前に置いた。理由は記録に無い。6 と S4 の二升目の一致が意図か偶然かは、記録から確かめられない）',
    '・'.join('%s: %s（日本時間）' % kv for kv in sorted(first.items(), key=lambda kv: kv[1])) + '。S4 の主の土台の升目 %d・主の升目 %d・続ける条件 %d' % (
        sum(1 for c in T3['cells_main'] if c[0] == 'S4'), len(T3['cells_main']), T3['pilot']['decision']['cells_min_pass']))

# ---------------- 13. 算術の確かめ ----------------
nl = T3['inputs']['model']['num_hidden_layers'] - li - 1
add(['G1-3-1', 'C1-M7', 'C2-R11', 'C1-L1'], '算術: p=0.0001 の対数オッズ・層ごとの差分の表の大きさ・9999 本の npz の大きさ', '器が計算した', '再現',
    'p=0.0001 の対数オッズ %.2f・選んだ層の後の層 %d・表の値の数 %d（十三の組）と %d（十二の組）・9999 本の npz %.1f MB（float64）' % (
        math.log(1e-4 / (1 - 1e-4)), nl, nl * 7 * 13 * 3, nl * 7 * 12 * 3, 9999 * T3['inputs']['model']['hidden_size'] * 8 / 1e6))

# ---------------- 出力 ----------------
out = {'kind': 'Bl3_design_r1_verification', 'k_range': [K[0]['id'], K[-1]['id']], 'items': K,
       'inputs_sha16': {p: s16(p) for p in ('design/contrasts-Bl3.json', 'design/design-Bl3-draft1.md', 'records/Bl3/design-facts-Bl3.json', 'tools/blens_core.py', 'records/reviews/Bl3/design-round1/bundle-Bl3-design-part2.md')},
       'transformers': transformers.__version__, 'overlap': ov, 'chance_sim': sim, 'gate_sim': {'n': nsim, 'perm_rate': fp_perm, 'naive_rate': fp_naive},
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(out, open(os.path.join(HERE, 'verify-Bl3-design-r1.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
L = ['# B-lens 層三の枠（草案1）の設計の巡・第一巡の事実の確かめ（機械生成・`verify_Bl3_design_r1.py`）', '',
     '- 四票（`gemini-1`・`gemini-2`・`claude-ai-1`・`claude-ai-2` の `review.md`）の事実の主張を、一次記録・凍結の器・手元のトークナイザ（transformers %s）・合成の数で確かめた。**全経路の効き目は一つも計算していない**（模型の順伝播をしない・重みを読まない）。' % transformers.__version__,
     '- 票の所見は「票の名・所見の番号」で指す（G1＝gemini-1・G2＝gemini-2・C1＝claude-ai-1・C2＝claude-ai-2）。主張の欄は起草者の要約で、票の逐語ではない（逐語は各票のファイル）。証拠の欄は、器が一次記録から切り出した文と、器が計算した数。',
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % kv for kv in out['inputs_sha16'].items()), '',
     '| 番号 | 票・所見 | 主張（起草者の要約） | 確かめ方 | 結果 | 証拠（器が切り出した文・計算した数） |', '|---|---|---|---|---|---|'] + [
     '| %s | %s | %s | %s | %s | %s |' % (k['id'], '・'.join(k['votes']), cell(k['claim']), cell(k['method']), cell(k['result']), cell(k['evidence'])) for k in K] + [
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'verification-Bl3-design-r1.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('wrote verification | items', len(K), K[0]['id'], '-', K[-1]['id'], '| results', dict(collections.Counter(k['result'].split('（')[0] for k in K)))
