# -*- coding: utf-8 -*-
"""器についての意見伺い（登録者裁定 D230）のご意見の中の、事実についての主張を、正本と器の実物で確かめる（コーディネータの追い問い・機械で引く）。
確かめの番号 V は採否の案（`adoption-proposal-opinions-tools-Bl3.md`）から引く。値と行は器と正本から機械で取り、手で打たない。
器と正本は束の入力のコミット（029d55f）から変わっていないことを先に確かめる。長い走り（C2 の方の台本・全等方の試し・二段目の切り分け）は、保存した出力のファイルを読む。
出力: checks/verification-opinions-tools-Bl3.json・.md
用法: python records/reviews/Bl3/opinions-tools/checks/verify_opinions_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, ast, json, math, hashlib, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OP = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(OP, '..', '..', '..', '..'))
NL = chr(10)
P = lambda r: os.path.join(REPO, *r.split('/'))
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
V = collections.OrderedDict()


def lines_of(rel, pattern, flags=0):
    """ファイルの中で pattern に当たる行（行番号と中身）。"""
    out = []
    for i, l in enumerate(open(P(rel), encoding='utf-8').read().split(NL), 1):
        if re.search(pattern, l, flags):
            out.append([i, l.strip()[:220]])
    return out


def put(vid, what, claim_by, result, evidence):
    V[vid] = {'what': what, 'claim_by': claim_by, 'result': result, 'evidence': evidence}


# 器と正本が束の入力のコミットから変わっていない
diff = subprocess.run(['git', 'diff', '--stat', '029d55f', '--', 'tools/', 'design/'], cwd=REPO, capture_output=True, text=True).stdout.strip()
put('V0', '器と正本は束の入力のコミット 029d55f から変わっていない', '—', '確かめた' if not diff else '変わっている', {'git_diff_stat': diff or '（差なし）'})
T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
FJ = json.load(open(P('records/Bl3/design-facts-Bl3.json'), encoding='utf-8'))

# V1・V2: C2 の方の台本の出力
run = open(os.path.join(OP, 'checks', 'c2-script-run.txt'), encoding='utf-8').read()
p1 = [l for l in run.split(NL) if l.startswith('一 ')]
p2 = [l for l in run.split(NL) if l.startswith('二 ')]
put('V1', '下見で主の升目を外した形で、集計の器の門と独立の再計算の一致が落ちる', 'C1-B1・C2-A1', '再現した（台本を走らせた）', {'script_output': p1})
put('V2', '札の一致の裾の欄が、帰無の内側の行で小さな揺れに反転し、一致を落とす', 'C2-A2', '再現した（台本を走らせた・乱数の種は固定・二度とも同じ出力）', {'script_output': p2})
# V3: 落ちる行（門は外した升目の行を落とす前に効き目を引く・独立の再計算の本の値の側は外した升目の行を飛ばさない）
put('V3', '落ちる所の器の行', 'C1-B1・C2-A1', '行を読んで確かめた', {
    'gates_ue': lines_of('tools/analyze_Bl3.py', r"ue = \{u: \{f: eff\[f\]\[u\]"),
    'recompute_main_ov': lines_of('tools/analyze_Bl3.py', r"main_ov\[r\['id'\]\] = |for r in main_rows:|if r\['direction'\] != 'static' or \(rows_subset"),
    'run_main_phase_skip': lines_of('tools/bl3_run.py', r"if ck in dropped:"),
    'judge_rows_subset': lines_of('tools/analyze_Bl3.py', r"rows_subset=set\(rc\['hook'\]\) if dry else None")})
# V4: 偶然の目安の式（生成器）と、升目を外したときの数え直し
rows = T3['main_rows']
co, cp = T3['nulls']['real']['comparators_oriented'], T3['nulls']['real']['comparators']
ch = lambda rs: (round(sum(1 / (co[r['direction']] + 1) for r in rs), 4), round(sum(1 / (cp[r['direction']] + 1) for r in rs), 4))
drop = 'N1|O-Ncold'
put('V4', '偶然の目安は行ごとの 1/(比べる相手の数+1) の和で、集計の器は正本の定数をそのまま置いている', 'C1-B2・C2-A3', '式を再現し、外した後の値を器で出した', {
    'generator': lines_of('tools/make_contrasts_Bl3.py', r"^chance_second"), 'canon': [T3['nulls']['real']['chance_second'], T3['nulls']['real']['chance_second_pair']],
    'recomputed_all_rows': ch(rows), 'recomputed_after_dropping_%s' % drop: ch([r for r in rows if '%s|%s' % (r['scenario'], r['base']) != drop]),
    'analyzer_line': lines_of('tools/analyze_Bl3.py', r"chance=\{'oriented'")})
# V5: 比べる相手の自分の対（器）と、B-lens の凍結の器の OWN_PAIR
tree = ast.parse(open(P('tools/blens_lens.py'), encoding='utf-8').read())
own_blens = [ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == 'OWN_PAIR' for t in n.targets)][0]
own_bl3 = ast.literal_eval(re.search(r"own = (\{[^}]*\})", open(P('tools/bl3_core.py'), encoding='utf-8').read()).group(1))
put('V5', 'Nk と td の自分の対は正本に名が無く器の中にある。B-lens の凍結の器の OWN_PAIR と同じか', 'C2-A5（錨の案）', '同じ' if all(own_blens[k] == v for k, v in own_bl3.items()) else '違う', {
    'bl3_core_own': own_bl3, 'blens_lens_OWN_PAIR': own_blens, 'swap_siblings': T3['nulls']['real']['swap_siblings'],
    'static_loaded_own_in_swap': all(own_blens[k] in T3['nulls']['real']['swap_siblings'] for k in ('static', 'loaded'))})
# V6: 全等方の試し（コーディネータがご意見を読む前に見つけた点）
tr = open(P('records/Bl3/tools/trials/dry-trial-7-fulliso-Bl3.md'), encoding='utf-8').read()
put('V6', '等方を正本の本数にした合成の試しで、二段目の効き目の差の最大が許容を超えた（ご意見が届く前に見た）', 'コーディネータ（K1）・C1-C3・C2-B7・G1-3(3)', '試しの記録のとおり', {
    'rows': [l[:260] for l in tr.split(NL) if '二段目' in l or '等方の方向の本数' in l or '確かめ:' in l]})
# V7: 二段目の切り分け（近道ありと近道なしの効き目の差を全ての方向で）
pr = os.path.join(OP, 'checks', 'probe-stage2-fulliso.txt')
put('V7', '二段目の差の出どころ（近道ありと近道なしの、同じバッチ 16 での効き目の差の分布）', 'コーディネータ（K1）', '切り分けの出力のとおり' if os.path.exists(pr) else 'まだ',
    {'probe_output': [l[:700] for l in open(pr, encoding='utf-8').read().split(NL) if l.strip()] if os.path.exists(pr) else None})
# V8・V9: 札の一致の中身と、効き目の側の二つの文
put('V8', '札の一致は全ての行の裾を比べている', 'C2-A2', '行を読んで確かめた', {'labels_signature': lines_of('tools/analyze_Bl3.py', r"return \{rid: \(o\['iso_outside'\], o\['tail'\]"),
                                                                    'canon_agreement': T3['independent_recompute']['agreement']})
put('V9', '効き目の側を添える行について、正本の二つの文が食い違う・器は等方の外の行にだけ側を作り、帰無を捨てる', 'C1-B3', '正本の文と器の行で確かめた', {
    'side_rule_head': T3['labels']['side_rule'].split('。')[0], 'print_rule_part': [s for s in T3['labels']['print_rule'].split('。') if 'どの行にも' in s],
    'analyzer_side': lines_of('tools/analyze_Bl3.py', r"o\['side'\] = K\.effect_side")})
# V10・V11
put('V10', '層ごとの差分の余弦は、符号を掛ける前の方向で取っている', 'C1-B4・C2-B4', '行を読んで確かめた', {'bl3_run': lines_of('tools/bl3_run.py', r"u = R\.torch\.tensor\(R\.vec\(d\)|cos = float\(\(dh @ u\)"),
                                                                                  'canon': [v for v in T3['descriptive']['layerwise']['values'] if '余弦' in v]})
put('V11', '門は入れ替える単位が二つ未満のときも判定不能にしている（正本は行が残らないときだけ）', 'C1-B5・C2-B3', '行を読んで確かめた', {
    'bl3_core': lines_of('tools/bl3_core.py', r"if not rs or len\(us\) < 2"), 'canon': T3['pilot']['decision']['drop_effects'].split('。')[-1]})
# V12・V13・V14
put('V12', '書き換えの道の use_cache の既定は None（模型の設定＝既定の呼び方）で、起動器は False を明示して呼ぶ', 'G1-A1', '行を読んで確かめた', {
    'rewrite_def': lines_of('tools/bl3_recompute_rewrite.py', r"^def recompute_rewrite\("), 'boot_call': lines_of('tools/colab/boot_Bl3.py', r"RW\.recompute_rewrite\(")})
put('V13', '対数オッズの算術の精度: 本の器は出口の値を float64 にしてから、書き換えの道は float32 のまま logsumexp を取る', 'G2-1-1', '行を読んで確かめた', {
    'bl3_run': lines_of('tools/bl3_run.py', r"Zs = \(hn @ self\.W32\[cell\.set_ids\]\.T\)\.double\(\)"), 'rewrite': lines_of('tools/bl3_recompute_rewrite.py', r"lo = z\[0\] - torch\.logsumexp")})
put('V14', '独立の再計算の一致は効き目だけを比べ、無操作の値（noop_lo）を比べていない', 'G2-2-1', '行を読んで確かめた', {
    'as_eff': lines_of('tools/analyze_Bl3.py', r"return \{rid: \[o\['effect'\]\]"), 'canon_what': T3['independent_recompute']['what']})
# V15〜V18
M = T3['inputs']['model']
put('V15', '全語彙の softmax は模型の出口の全ての行で、トークナイザの外の行を含む', 'C2-B6', '正本の数から出した', {'vocab_size': M['vocab_size'], 'tokenizer_len': M['tokenizer_len'], 'rows_outside_tokenizer': M['vocab_size'] - M['tokenizer_len']})
put('V16', 'glob(...)[0] はファイルがちょうど一つかを確かめていない', 'C2-B8', '行を読んで確かめた', {'analyze': lines_of('tools/analyze_Bl3.py', r"glob\.glob\(.*\)\[0\]"), 'bl3_run': lines_of('tools/bl3_run.py', r"glob\.glob\(.*\)\[0\]")})
put('V17', '起動器は本の凍結の pilot を、集計の器は pilot_attempts の最後を読む', 'C2-B9', '行を読んで確かめた', {'boot': lines_of('tools/colab/boot_Bl3.py', r"pilot = FR\['main_freeze'\]\['pilot'\]"),
                                                                                     'analyze': lines_of('tools/analyze_Bl3.py', r"return FR\['main_freeze'\]\['pilot_attempts'\]")})
put('V18', '近道の assert は記録した切れ目（pc の end）を見て、使い回す cache の実の長さを見ていない', 'C2-B2', '行を読んで確かめた', {'bl3_run': lines_of('tools/bl3_run.py', r"if pc\['end'\] != cell\.mp:")})
# V19: 本物の模型の領域での bf16 の丸め（転記行 D から）
vn = FJ['facts']['D']['vhat_norm']
coef = T3['layers']['coef_applied']
rel_ = T3['layers']['vhat_over_h'][str(T3['layers']['selected_ratio'])]
d = M['hidden_size']
add_c = coef * vn / math.sqrt(d)
res_c = vn / rel_ / math.sqrt(d)
spacing = lambda x: 2.0 ** (math.floor(math.log2(x)) - 7)           # bf16 の刻み（仮数 7 桁＋隠れた一桁）
put('V19', '本物の模型の領域で、足す量の一成分と残差の一成分の大きさ・bf16 の刻み（C1 の見積もりの再計算）', 'C1-C2', '転記行 D と正本の数から出した（推論の見積もり）', {
    'add_component_rms': round(add_c, 4), 'residual_component_rms': round(res_c, 4), 'bf16_spacing_at': {str(x): spacing(x) for x in (0.5, 0.85, 1.0, 4.0, 16.0)}})
# V20: 書き換えの道の --dry の相手の版
dev = open(P('records/Bl3/tools/recompute-rewrite-dev-Bl3.md'), encoding='utf-8').read()
put('V20', '書き換えの道の開発の記録の --dry の相手の bl3_run の SHA16 と、束の版の SHA16', 'C1-C4・C2', '記録と器から出した', {
    'in_dev_record': sorted(set(re.findall(r'7ECB9CF764F4F8AE', dev))), 'bl3_run_now': sha16f(P('tools/bl3_run.py')),
    'coordinator_rerun_logs': [os.path.basename(x) for x in ('records/Bl3/tools/trials/recompute-rewrite-selftest-coordinator-rerun.log', 'records/Bl3/tools/trials/recompute-rewrite-dry-coordinator-rerun.log')],
    'rerun_logs_record_sha': any('SHA16' in open(P(x), encoding='utf-8').read() for x in ('records/Bl3/tools/trials/recompute-rewrite-dry-coordinator-rerun.log',))})
# V21: 門の升目の外しを「問題なし」とした是認（V1 の見逃し）
put('V21', '門の升目の外しの扱いを「問題なし」とした是認（V1 で落ちることが分かった所）', 'G1-2(5)・G2-2-3', 'ご意見の行を引いた', {
    'G1': lines_of('records/reviews/Bl3/opinions-tools/g1/opinion.md', r"外された升目|drop_cells"), 'G2': lines_of('records/reviews/Bl3/opinions-tools/g2/opinion.md', r"門（`gate`）においても|実装の逸脱はありません")})
# V22: 機種の申告
put('V22', 'Gemini の二名の本文の中の機種の申告と、登録者が確かめた機種', 'G1・G2', 'ご意見の頭の行と登録者の言葉から引いた', {
    'G1': lines_of('records/reviews/Bl3/opinions-tools/g1/opinion.md', r"\*\*機種\*\*"), 'G2': lines_of('records/reviews/Bl3/opinions-tools/g2/opinion.md', r"\*\*機種\*\*"),
    'registrant': lines_of('records/reviews/Bl3/opinions-tools/registrant-message-head.md', r"Gemini 3\.8 Flash")})
# V23: 露出の候補（結果の見込みに当たりうる語の行・コーディネータが読んで判断する）
cand = {}
for lab in ('g1', 'g2', 'c1', 'c2'):
    cand[lab.upper()] = lines_of('records/reviews/Bl3/opinions-tools/%s/opinion.md' % lab, r"見込み|予想|札が付く|門を通る|通らない|区別でき")
put('V23', '露出の候補の行（結果の見込みに当たりうる語を含む行・コーディネータが読んで判断する）', '四名', '候補を引いた（判断は採否の案）', cand)

json.dump({'kind': 'bl3_opinions_verification', 'items': V, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'},
          open(os.path.join(HERE, 'verification-opinions-tools-Bl3.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = ['# 器についての意見伺いの確かめ（機械生成・`checks/verify_opinions_Bl3.py`）', '',
      '- ご意見の中の事実の主張を、正本と器の実物で確かめた記録。値と行は器と正本から機械で引いた。採否の案（`adoption-proposal-opinions-tools-Bl3.md`）が番号 V で引く。', '']
for vid, v in V.items():
    md += ['## %s %s' % (vid, v['what']), '', '- 出所の主張: %s' % v['claim_by'], '- 結果: %s' % v['result'], '', '```json', json.dumps(v['evidence'], ensure_ascii=False, indent=1)[:6000], '```', '']
md += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'verification-opinions-tools-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(md))
print('items', len(V), '|', {k: v['result'] for k, v in V.items()})
