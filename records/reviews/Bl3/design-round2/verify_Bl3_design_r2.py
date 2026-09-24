# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の設計の巡・二巡目（最終検分）の四票の事実の主張を、一次記録・凍結の器・手元のトークナイザで確かめる（再現の番号 K455〜）。
- 全経路の効き目は一つも計算しない（模型の順伝播をしない・重みを読まない）。
- 票の文は打ち直さない。票の所見は「票の名・所見の番号」で指し、確かめた内容は一次記録から器が切り出した文と、器が計算した数で書く。
- 草案2 の正本・設計事実・草案は、二巡目の束の入力のコミット（`SRC`）から読む（草案3 の後も同じ結果を出すため）。
出力: records/reviews/Bl3/design-round2/verify-Bl3-design-r2.json・verification-Bl3-design-r2.md
用法: python records/reviews/Bl3/design-round2/verify_Bl3_design_r2.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, math, hashlib, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
SRC = '0882084'                                                # 二巡目の束の入力のコミット
at = lambda rel: subprocess.run(['git', 'show', '%s:%s' % (SRC, rel)], cwd=REPO, capture_output=True, check=True).stdout
rd = lambda rel: at(rel).decode('utf-8')
s16 = lambda rel: hashlib.sha256(at(rel).replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
import blens_core as C                  # 凍結（読み取りだけ）
import rules_B                          # 凍結（読み取りだけ）
T3 = json.loads(rd('design/contrasts-Bl3.json'))
FJ = json.loads(rd('records/Bl3/design-facts-Bl3.json'))
AN = json.loads(rd('records/B/analysis-B-2026-09-22.json'))
TB = json.loads(rd('design/contrasts-B.json'))
D2 = rd('design/design-Bl3-draft2.md')
GEN = rd('tools/make_contrasts_Bl3.py')
FACTS_TOOL = rd('tools/bl3_facts.py')
assert T3['version'] == 'draft2-2026-09-24'
K, k0 = [], 455


def add(votes, claim, method, result, evidence):
    K.append({'id': 'K%d' % (k0 + len(K)), 'votes': votes, 'claim': claim, 'method': method, 'result': result, 'evidence': evidence})


P = T3['pilot']
IR = T3['independent_recompute']
Kiso = T3['nulls']['isotropic']['count']
step = 2.0 / (1 + Kiso)
add(['G1-2-1', 'G2-Ⅱ-1', 'C1-N2', 'C2-N1'], '独立の再計算の許容は、下見の (vi) で本の道に認めた揺れや近道の許容より厳しく、器が正しくても差が許容を超えうる。割合の刻みは帰無一本で許容と同じ幅になる',
    '正本の許容の値と決まりの文を器が読み、等方の帰無の本数から割合の刻みを計算した',
    '再現', '独立の再計算の許容 %g・再計算の道: %s／揺れの床の上限 `pilot.noise_max` %g・近道の許容の倍率 %g・下限 %g（上限は無い）／割合の刻み（帰無一本）%g' % (
        IR['tol'], IR['how'], P['noise_max'], P['cache_tol_factor'], P['cache_tol_floor'], step))
alpha = T3['labels']['iso_outside']['holm_alpha']
m = len(T3['main_rows'])
lim = []
for s_ in range(1, m + 1):
    thr = alpha / (m - s_ + 1)
    lim.append(max(e for e in range(0, Kiso) if min(1.0, 2.0 * (1 + e) / (1 + Kiso)) < thr))
add(['C1-検算'], '十六行の Holm の各段を通れる外側の帰無の本数の上限は、段の順に 2・2・2・2・3・3・3・4・5・6・7・8・11・15・23・48',
    '両側に等しい裾の割合の式（`blens_core.p_equal_tailed` の形）で、段ごとに閾値を下回る外側の本数の最大を数えた', '再現' if lim == [2, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8, 11, 15, 23, 48] else '一部再現',
    '段ごとの上限: %s' % '・'.join(str(x) for x in lim))
add(['G1-2-2'], '(vi) でバッチ一に移ったとき下見の (i)〜(v) をバッチ一でやり直すか、バッチ一でも揺れが上限を超えたときにどうするかが無い',
    '正本の `pilot.checks.vi` の決まりを器が読んだ', '再現', P['checks']['vi']['rule'])
add(['G1-2-3'], '近道の許容の式に上限が無く、揺れの床が上限の近くなら許容は上限の二倍まで広がる',
    '正本の `pilot.cache_tol_rule` と値を器が読み、揺れの床が `pilot.noise_max` のときの許容を計算した', '再現',
    '%s／揺れの床が上限のときの許容 %g' % (P['cache_tol_rule'], max(P['cache_tol_factor'] * P['noise_max'], P['cache_tol_floor'])))
from transformers import AutoTokenizer
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/%s' % T3['inputs']['model']['rev'])
tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
A = FJ['facts']['A']
v0, v3 = A['prefix_ids'], A['variants']['V3']['ids']
nsp = wsp = 0
for d in glob.glob(j('results', 'stageB', 'stageB__*__s1')):
    for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8'):
        tx = json.loads(l)['text']
        nsp += '"choice":"' in tx
        wsp += '"choice": "' in tx
same5 = v0[:len(v3) - 1] == v3[:len(v3) - 1]
add(['G1-2-4', 'C1-N11', 'C2-N3'], 'V3 は雛形との一致の最後のトークンだけを崩し、頭のトークンは主の書き出しと同じ。V3 の形（鍵の後に空白が無い）は段階 B の出力に無い。(iv) に V3 の読みの基準が無い',
    '設計事実の V0 と V3 のトークンの並びを手元のトークナイザで戻して比べ、段階 B の生の出力で鍵の二つの書き方を数えた。正本の (iv) の文を読んだ',
    '再現', 'V0: %s／V3: %s（頭の %d トークンが同じ: %s）。段階 B の出力のうち鍵の後に空白が無い形を含むもの %d 件・空白のある形を含むもの %d 件。(iv): %s' % (
        '・'.join('「%s」' % tok.decode([i]).replace(NL, '⏎') for i in v0), '・'.join('「%s」' % tok.decode([i]).replace(NL, '⏎') for i in v3), len(v3) - 1, same5, nsp, wsp, P['checks']['iv']['rule']))
lo2 = lambda p_: math.log(p_ / (1 - p_))
add(['G1-5-1'], '確率が床の近く（0.0002）では、0.0002 動くだけで対数オッズが約 0.69 動く', '対数オッズを計算した', '再現', '0.0002→0.0004 の対数オッズの差 %.3f' % (lo2(0.0004) - lo2(0.0002)))
BD = AN['by_direction']
noop = {(r['scenario'], r['arm']): r for r in BD if r['direction_id'] == 'fixed' and '+v' not in r['arm'] and '-v' not in r['arm']}
arm_row = {(r['scenario'], r['arm']): r for r in BD if r['direction_id'] == 'static'}
q7 = []
for mr in T3['main_rows']:
    if mr['direction'] != 'static':
        continue
    r = arm_row[(mr['scenario'], mr['arm'])]
    b = noop[(mr['scenario'], mr['base'])]
    d_, lo, hi = rules_B.diff_ci_pt(r['cat'], r['n_ok'], b['cat'], b['n_ok'])
    q7.append((mr['id'], d_, lo, hi, lo <= 0 <= hi))
bf = rd('records/B/results-B-FINAL-2026-09-23.md').split(NL)
g2rows = [l for l in bf if (l.startswith('| sub:N1:') or l.startswith('| add:N1:')) and 'Newcombe' not in l and '[' in l]
add(['G2-Ⅱ-2', 'C1-N8', 'C2-N7'], 'q7 の決まりに、等方の外の v̂ の行がすべて「該当なし」になったときの扱いが無い。G2 は、N1 の二行（sub・add）は段階 B の区間がすでに零を含むとした',
    '正本の `predictions.q7_rule` を読み、v̂ の主の八行について、q7 の決まりの区間（その行の破局の率と土台の無操作の腕の率の差・凍結の `rules_B.diff_ci_pt`）を計算した。G2 が引いた区間は、段階 B の最終版の §2 の表の行から器が切り出した',
    '一部再現（決まりの抜けは確か。零を含むのは sub:N1 だけで、G2 の引いた区間は v̂ の腕とランダムの腕の差の区間で、q7 の決まりの区間ではない）',
    'q7 の区間: %s。G2 の引いた行: %s' % ('・'.join('%s %+.1f [%.2f, %.2f]%s' % (i_, d_, lo, hi, '〔零を含む〕' if z else '') for i_, d_, lo, hi, z in q7), '／'.join(l[:120] for l in g2rows)))
add(['G2-Ⅱ-3'], '二つ目の札の「対の単位の順位」の「対ごとに両方の向きの大きい方」が、中心からの距離の大きい方か、生の効き目の大きい方か、決まっていない',
    '正本の `labels.second.ranks` を読んだ', '再現', T3['labels']['second']['ranks'])
D = P['decision']
add(['C1-N1', 'C2-N2'], '下見の中の「器の誤り」の定めが無く、値を見た後にやり直せる。器を直すと、本の凍結の確かめ（器の SHA が変わらない）を通れない',
    '正本の `pilot.decision.tool_error` と `computation.main_freeze_check` を読んだ', '再現', '%s／%s' % (D['tool_error'], T3['computation']['main_freeze_check']))
n_dirs = FJ['facts']['E']['n_dirs']
bt = T3['readout']['primary']['batch']
add(['C1-N3'], '升目と符号ごとの方向の数（零のベクトルを含む）はバッチの大きさで割り切れず、端数のバッチで同じ形が崩れる',
    '設計事実の方向の数と正本のバッチの大きさで割り算をし、正本の `readout.primary.batching` を読んだ', '再現',
    '方向 %d ＋ 零のベクトル 1 ＝ %d ＝ %d × %d ＋ %d。決まり: %s' % (n_dirs, n_dirs + 1, bt, (n_dirs + 1) // bt, (n_dirs + 1) % bt, T3['readout']['primary']['batching']))
add(['C1-N4'], '(vi) が主に測るのはバッチの大きさの違いで、測る道（近道の有無）も書かれていない', '正本の `pilot.checks.vi` を読んだ', '再現', P['checks']['vi']['rule'])
add(['C1-N5'], '本の計算の頭の近道の確かめは、読み取りの値のまま比べている（効き目で比べる案）', '正本の `computation.steered_cache_check` を読んだ', '再現', T3['computation']['steered_cache_check']['rule'])
add(['C1-N6'], '効き目の側の「中央値が零なら」は、連続の値ではまず当たらない', '正本の `labels.side_rule` を読んだ', '再現', T3['labels']['side_rule'])
add(['C1-N7'], '記述の門に「読まない」の決まりが無い', '正本の `gate.descriptive_gates` を読んだ', '再現', '・'.join(T3['gate']['descriptive_gates']))
st = T3['nulls']['storage']['rule']
add(['C1-N9'], '頭の近道の確かめの一本は npz に入る決まりが無く、最後の層の一致の自己検査は封印の前には本物の模型で走らせられない',
    '正本の `nulls.storage.rule`・`computation`・`descriptive.layerwise.capture` を読んだ', '再現',
    'npz の決まり: %s／封印の前: %s／自己検査: %s' % (st, T3['computation']['before_seal'], T3['descriptive']['layerwise']['capture']))
add(['C1-N10', 'C2-N6'], '(iii) の文の選び方（生の値か変換の後か・零や定まらないとき）が無く、正の側の文だけに「行動の率の代わりに読まない」が無い。正の側の文は升目の数に比べて強い',
    '正本の `pilot.checks.iii` と `pilot.iii_sentences` を読んだ', '再現', '%s／正: %s／正でない: %s' % (P['checks']['iii']['rule'], P['iii_sentences']['positive'], P['iii_sentences']['not_positive']))
add(['C1-N12'], '下見で外した後に行の無くなった単位を、入れ替えに残すか外すかが無い', '正本の `pilot.decision.drop_effects` と `gate` を読んだ', '再現', D['drop_effects'])
ss = FJ['facts']['C']['style_share_pt']
near = sorted(((k_, v_) for k_, v_ in ss.items() if 15 <= abs(v_) < T3['gate']['style_hold_pt']), key=lambda kv: -abs(kv[1]))
gl = [l.strip() for l in GEN.split(NL) if 'STYLE_HOLD_PT = TB[' in l]
fl = [l.strip() for l in FACTS_TOOL.split(NL) if "hold = T3['gate']['style_hold_pt']" in l]
add(['C1-R1', 'C2-N5'], '様式の転位の閾値は段階 B の値だと書くが、器は段階 B の正本と突き合わせていない。閾値のすぐ下に四行ある',
    '設計事実の門の行ごとの差（pt）から閾値の下の行を並べ、正本の生成器と設計事実の器の該当の行を切り出した',
    '一部再現（正本の生成器は段階 B の正本の鍵から読んでいる。設計事実の器は層三の正本から読み、段階 B の正本と突き合わせていない。閾値の下の四行は票のとおり）',
    '閾値 %d pt・閾値の下（15 pt 以上）: %s。生成器: `%s`／設計事実の器: `%s`・段階 B の正本の値 %d' % (T3['gate']['style_hold_pt'], '・'.join('%s %+.1f' % kv for kv in near), gl[0] if gl else '無し', fl[0] if fl else '無し', TB['style_gate']['hold_pt']))
sa = [l.strip() for l in GEN.split(NL) if '種が段階 B か B-lens の種と重なる' in l]
ba = [l.strip() for l in GEN.split(NL) if "'batch': TB['runner']['batch']" in l]
add(['C1-R4', 'C2-N9'], '種が段階 B の種と重ならないことの assert と、バッチの大きさが段階 B の走行器と同じことは、束からは確かめられない',
    '二巡目の束の入力のコミットの正本の生成器から、該当の行を器が切り出した', '確かめた（生成器にあるが、束に入っていなかった）',
    'assert: `%s`／バッチ: `%s`（段階 B の正本の `runner.batch` は %d）' % (sa[0] if sa else '無し', ba[0] if ba else '無し', TB['runner']['batch']))
add(['C2-N4'], '二つ目の札の「経験の割合」を偶然の目安の経験の値と書いているが、等方の方向が比べる相手の中で最上位になる割合は、二つの帰無の広がりの比べで、行の偶然の目安ではない',
    '正本の `labels.second.iso_rate` を読んだ', '再現（名と説明の直し）', T3['labels']['second']['iso_rate'])
add(['C2-N8'], '最後の層の一致の自己検査は、層ごとの最後の行と読み取りが同じ誤りを持てば通る', '正本の `descriptive.layerwise.capture` を読んだ', '再現', T3['descriptive']['layerwise']['capture'])
BL = rd('records/Blens/results-Blens-FINAL-2026-09-24.md').split(NL)
l33 = [(i + 1, l) for i, l in enumerate(BL) if '答えの文字が一度も動いていない' in l]
l160 = [(i + 1, l) for i, l in enumerate(BL) if l.startswith('- 較正の検査（S4|Osec-Ncold|json）')]
bl_time = subprocess.run(['git', 'log', '-1', '--format=%ad', '--date=format:%Y-%m-%d %H:%M', '807f29c', '--', 'records/Blens/results-Blens-FINAL-2026-09-24.md'], cwd=REPO, capture_output=True, text=True).stdout.strip()
s15 = [l for l in D2.split(NL) if 'を器で見る前に置いた' in l]
V1J = json.load(open(os.path.join(HERE, '..', 'design-round1', 'verify-Bl3-design-r1.json'), encoding='utf-8'))
t_thr = re.search(r'正本の生成器に書いた: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})（日本時間）', [k_['evidence'] for k_ in V1J['items'] if '正本の生成器に書いた' in k_['evidence']][0]).group(1)
add(['C2-N10'], '§15 の「転記行 A の事実を器で見る前に置いた」は「知る前」ではない。起草者はそれ以前に、B-lens の最終版で、JSON 直答の出力の答えの文字が一度も動いていないことと、S4|Osec-Ncold の直答 154 件が c であることを見ていた',
    'B-lens の最終版から該当の行を器が切り出し、最終版の確定のコミットの時刻を読み、草案2 の §15 の行を切り出した',
    '再現（起草者の情報状態の書き方の誤り）',
    'B-lens の最終版 %d 行: %s／%d 行: %s／最終版のコミット 807f29c の時刻 %s（閾値を正本の生成器に書いた時刻は %s・第一巡の確かめの記録）。草案2 §15: %s' % (
        l33[0][0], l33[0][1][:150], l160[0][0], l160[0][1][:170], bl_time, t_thr, s15[0][:150] if s15 else '無し'))
EX = open(j('records', 'Bl3', 'exposure-before-seal-Bl3.md'), encoding='utf-8').read()
AT1 = open(j('records', 'reviews', 'Bl3', 'design-round1', 'adoption-table-Bl3-design-r1.md'), encoding='utf-8').read()
xr = [l for l in AT1.split(NL) if 'C2-R18' in l and '再現しなかった' in l]
add(['C2-N11'], '露出の記録の「扱い（登録者の裁定を待つ）」が D217 の後も残る。第一巡の採否表の検分票が C2-R18 を「再現しなかった主張」と書くが、所見は記録にあればの条件つきで、条件が立たなかったもの',
    '露出の記録と第一巡の採否表を器が読んだ', '再現（記録の直し）', '露出の記録の見出し「扱い（登録者の裁定を待つ）」の有無: %s／採否表の行: %s' % ('## 扱い（登録者の裁定を待つ）' in EX, xr[0][:200] if xr else '無し'))
lens = [v_['prompt_len'] for v_ in FJ['facts']['B']['cells'].values()]
npre = len(v0)
E = FJ['facts']['E']
add(['C2-Q4', 'C1-4'], '独立の再計算がトークンの数で最も大きい（約 760 万〜900 万）。乙の無操作の順伝播の見込みが転記行 E に無い',
    '設計事実の順伝播の見込みとプロンプトの長さから計算し、転記行 E の文を読んだ', '再現',
    '独立の再計算 %d 回 × 長さ %d〜%d ＝ %d〜%d トークン。乙の見込み %d 回（名前のある方向と段階 B の三本だけ・無操作の分を含まない）' % (
        E['passes_recompute'], min(lens) + npre, max(lens) + npre, E['passes_recompute'] * (min(lens) + npre), E['passes_recompute'] * (max(lens) + npre), E['passes_secondary_max']))
add(['G2-Ⅱ-1'], 'B-lens の逸脱 D-BL3 で、入力の長さの違いだけで残差の要素が最大 8（float 値換算で約 0.064）動いた', 'B-lens の最終版の該当の行を器が切り出した',
    '一部再現（最大 8 は記録どおり。0.064 は一件目の残差の要素の絶対値の最大に対する割合で、float 値への換算ではない）', [l for l in BL if l.startswith('- 【逸脱 D-BL3】升目の中の主位置の残差の揺れ')][0][:260])

out = {'kind': 'Bl3_design_r2_verification', 'k_range': [K[0]['id'], K[-1]['id']], 'items': K, 'src_commit': SRC,
       'inputs_sha16': {p_: s16(p_) for p_ in ('design/contrasts-Bl3.json', 'design/design-Bl3-draft2.md', 'records/Bl3/design-facts-Bl3.json')},
       'q7_intervals': [{'id': i_, 'diff_pt': d_, 'lo': lo, 'hi': hi, 'contains_zero': z} for i_, d_, lo, hi, z in q7], 'holm_limits': lim,
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(out, open(os.path.join(HERE, 'verify-Bl3-design-r2.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
L = ['# B-lens 層三の枠（草案2）の設計の巡・二巡目（最終検分）の事実の確かめ（機械生成・`verify_Bl3_design_r2.py`）', '',
     '- 四票（`gemini-1`・`gemini-2`・`claude-ai-1`・`claude-ai-2` の `review.md`）の事実の主張を、一次記録・凍結の器・手元のトークナイザで確かめた。**全経路の効き目は一つも計算していない**。草案2 の正本・設計事実・草案はコミット %s から読んだ。' % SRC,
     '- 票の所見は「票の名・所見の番号」で指す（G1＝gemini-1・G2＝gemini-2・C1＝claude-ai-1・C2＝claude-ai-2）。主張の欄は起草者の要約で、票の逐語ではない。証拠の欄は、器が一次記録から切り出した文と、器が計算した数。',
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % kv for kv in out['inputs_sha16'].items()), '',
     '| 番号 | 票・所見 | 主張（起草者の要約） | 確かめ方 | 結果 | 証拠（器が切り出した文・計算した数） |', '|---|---|---|---|---|---|'] + [
     '| %s | %s | %s | %s | %s | %s |' % (k['id'], '・'.join(k['votes']), cell(k['claim']), cell(k['method']), cell(k['result']), cell(k['evidence'])) for k in K] + [
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'verification-Bl3-design-r2.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('wrote verification r2 | items', len(K), K[0]['id'], '-', K[-1]['id'], '| results', dict(collections.Counter(k['result'].split('（')[0] for k in K)))
