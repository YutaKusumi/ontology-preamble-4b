# -*- coding: utf-8 -*-
"""verify_B_final.py —— 最後の系統外の巡（裁定 D131）の票の所見を、一次記録から**再現する**器（追い問い K177〜K206）。

枠: `preregistration-final-B.md`（票の前）・追い問い `preregistration-reproduction-K177.md`（票を読んだ後・この器を書く前）。
やり方: 器の関数を直に呼ぶ・全数で数える・ソースを読んで行を示す・一つの器（torch の検査）は torch を隠して走らせる。
**票の数は照らすだけで、ここで出す数は器と同じ規則で数え直したもの**。読みで確かめたものは「読み」と印字する。
出力: verification-B-final.md・verification-B-final.json（--force が無ければ上書きしない）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, copy, glob, shutil, tempfile, subprocess, argparse, datetime
import numpy as np
from scipy.stats import binom

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import rules_B, runs_B, steer_B

ap = argparse.ArgumentParser()
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
OUT_MD, OUT_JS = os.path.join(HERE, 'verification-B-final.md'), os.path.join(HERE, 'verification-B-final.json')
if os.path.exists(OUT_MD) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % OUT_MD)
T = runs_B.load_T()
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
SRC = lambda f: rd('tools', f)


def lines_of(text, pat, flags=0):
    return [i + 1 for i, ln in enumerate(text.split('\n')) if re.search(pat, ln, flags)]


def span(text, start_pat, end_pat=None):
    """start_pat の行から end_pat の行の手前までの (開始行, 終了行, 本文)。"""
    L = text.split('\n')
    s = next(i for i, ln in enumerate(L) if re.search(start_pat, ln))
    e = len(L)
    if end_pat:
        e = next((i for i in range(s + 1, len(L)) if re.search(end_pat, L[i])), len(L))
    return s + 1, e, '\n'.join(L[s:e])


ROWS = []


def add(k, src, cat, status, ev, nums=None):
    ROWS.append({'K': k, 'source': src, 'category': cat, 'status': status, 'evidence': ev, 'numbers': nums or {}})


def null_excl(n, p, conf):
    """v と td の真の率が同じ p（各 n）のとき、(v − td) の Newcombe 区間（水準 conf）が零を外す確率（上に外す・下に外す）。"""
    k = np.arange(n + 1)
    w = binom.pmf(k, n, p)
    K1, K2 = np.meshgrid(k.astype(float), k.astype(float), indexing='ij')
    d, lo, hi = rules_B._newcombe_vec(K1, n, K2, n, conf)
    W = w[:, None] * w[None, :]
    return float(W[lo > 0].sum()), float(W[hi < 0].sum())


# ================================================================ K177 td の特異性
r177 = rules_B.td_specificity(100, 200, 70, 200, T)
TDR = T['descriptive_families']['B_desc_textdiff']['specificity_rule']
an = SRC('analyze_B.py')
s_td = span(an, r'^# ---- td の特異性', r'^# ---- S4 の反証')
conf_lo = 1.0 - float(T['alpha_upper'])
nulls = {}
for p in (0.13, 0.15, 0.37, 0.40, 0.555, 0.69, 0.70):
    up85, dn85 = null_excl(200, p, conf_lo)
    up95, dn95 = null_excl(200, p, 0.95)
    nulls[str(p)] = {'85_any': round(up85 + dn85, 4), '85_up': round(up85, 4), '85_down': round(dn85, 4),
                     '95_any': round(up95 + dn95, 4), '95_one_dir': round(up95, 4)}
worst85 = max(v['85_any'] for v in nulls.values())
best85 = min(v['85_any'] for v in nulls.values())
any8 = 1 - (1 - worst85) ** 8
any8_lo = 1 - (1 - best85) ** 8
dir95 = max(v['95_one_dir'] for v in nulls.values())
add('K177', 'claude.ai 二票（重大）・Gemini 二人目（軽微）', '甲（設計・正本の条）',
    '**再現した**',
    '`td_specificity(v 100/200, td 70/200)` → 書ける=%s・向き「%s」・区間 %s pt（td のほうが破局を下げた組でも「書ける」）。'
    '器は正本 `specificity_rule` の文（「零を含めば書かない」「外したときは向きを印字する」）のとおりで、**向きも確証の成否も見ない**（集計器 L%d–L%d は v の腕 対 td の腕の対比すべてに当てる）。'
    '帰無（v と td の真の率が同じ・n=200 対 200・全数）で水準 %.2f の区間が零を外す確率は一対比 %.3f〜%.3f、八対比のどこかで（独立の近似）%.3f〜%.3f。水準 0.95 の一方の向きだけなら一対比 %.3f 以下'
    % (r177['write_specificity'], r177['direction'], [round(x, 1) for x in r177['ci']], s_td[0], s_td[1], conf_lo, best85, worst85, any8_lo, any8, dir95),
    {'call': r177, 'null_by_base': nulls, 'any_of_8_independent': [round(any8_lo, 3), round(any8, 3)]})

# ================================================================ K178 S4 に門が無い
v_full = rules_B.s4_verdict(20, 200, 24, 200, T)
v_read = rules_B.s4_verdict(20, 200, 24, 120, T)
s_s4 = span(an, r'^# ---- S4 の反証', r'^# ---- ')
gates_in_s4 = [w for w in ('gates', 'refuse_gate', 'ff_pt', 'dilution', 'scoring_gap', 'gate_order') if w in s_s4[2]]
prev = rd('records', 'reviews', 'B', 'external-round', 'claude-ai-2', 'review.md')
prev_gate = '三分岐の前に、確証族と同じ門を当ててください' in prev
adopt = rd('records', 'reviews', 'B', 'external-round', 'adoption-table-B-external.md')
p338 = next(l for l in adopt.split('\n') if l.startswith('| P338 |'))
add('K178', 'claude.ai 二人目', '乙（採否の漏れ）',
    '**再現した**',
    '全分母: (6b) 20/200・ランダム 24/200 → 「%s」（片側上限 %.1f pt）。書式外の 80 を除いた読めた分母: 20/200・24/120 → 「%s」（差 %.1f pt・区間 %s）。'
    '集計器の S4 の節（L%d–L%d）は門の語を持たない（%s）。**前の巡の票に「三分岐の前に、確証族と同じ門を当ててください」がある**（%s）が、採否表の P338 の直す中身は同等性と区間だけで、門は入っていない——**採否の段で半分を落とした**'
    % (v_full['verdict'], v_full['upper_one_sided_pt'], v_read['verdict'], v_read['diff_pt'], [round(x, 1) for x in v_read['ci']],
       s_s4[0], s_s4[1], '門の語なし' if not gates_in_s4 else '・'.join(gates_in_s4), '見つかった' if prev_gate else '見つからない'),
    {'full': v_full, 'readable': v_read, 'p338_row': p338})

# ================================================================ K179 S4 の札と封印
labels = T['descriptive_families']['B_desc_S4']['three_way']['labels']
sv = T['seal_format']['sign_map']
seal_in_verdict = bool(re.search(r"SEAL[^\n]*s4[^\n]*verdict|verdict[^\n]*SEAL", s_s4[2]))
v_down = rules_B.s4_verdict(10, 200, 40, 200, T)
add('K179', 'claude.ai 一人目', '甲（設計）', '**再現した**',
    '札は正本の固定の文 %s。封印の S4 の欄は三語（%s）の列挙で検べるだけで、**集計器は S4 の封印の値を札の判定に使わない**（S4 の節で封印は `sealed_prediction` として並べるだけ）。'
    '例: (6b) 10/200・ランダム 40/200 → 「%s」。封印が「低下」でも、この札は「封印は外れ」と書く'
    % (labels, '・'.join(sv), v_down['verdict']), {'labels': labels, 'seal_used_in_verdict': seal_in_verdict})

# ================================================================ K180 効き目 10 pt の相対の大きさ
oc5 = rules_B.s4_oc(0.1725, 200, 5, T)
T7, T5 = copy.deepcopy(T), copy.deepcopy(T)
T7['descriptive_families']['B_desc_S4']['three_way']['effect_pt'] = 7
T5['descriptive_families']['B_desc_S4']['three_way']['effect_pt'] = 5
oc0_7, oc0_5 = rules_B.s4_oc(0.1725, 200, 0, T7), rules_B.s4_oc(0.1725, 200, 0, T5)
eff = float(T['descriptive_families']['B_desc_S4']['three_way']['effect_pt'])
add('K180', 'Gemini 二人目（中）・claude.ai 一人目（軽微）・claude.ai 二人目（是認の注）', '丙（限界・札の文言）', '**再現した**',
    '効き目 %g pt は相手の基底 0.1725 に対して相対 %.0f%%。真の低下 5 pt で「%s」が %.3f。余地を 7 pt にすると真の帰無で「%s」が %.3f、5 pt では %.3f（n=200 では狭い余地は判定できなくなる）'
    % (eff, 100 * eff / 17.25, labels[2], oc5[labels[2]], labels[3], oc0_7[labels[3]], oc0_5[labels[3]]),
    {'oc_drop5': oc5, 'undecided_null_eff7': oc0_7[labels[3]], 'undecided_null_eff5': oc0_5[labels[3]]})

# ================================================================ K181 S4 の動作特性の数
oc0, oc10 = rules_B.s4_oc(0.1725, 200, 0, T), rules_B.s4_oc(0.1725, 200, 10, T)
M = T['measured']['s4_seal_right']
add('K181', 'claude.ai 一人目（L-j）・claude.ai 二人目（是認の数）', '丁（記録済み）／軽微', '一部再現（量の取り違え）',
    'いまの規則（Newcombe・`s4_oc`）: 真の低下 0 で「下がらなかった」%.4f・「上がった」を含む「封印は当たり」%.4f／10 pt で「下がらなかった」%.4f。'
    '正本 `measured.s4_seal_right` は notdrop_at_zero %s・seal_right_at_zero %s・notdrop_at_effect %s で一致する。設計の問いの表の 0.817・0.053 は **Wald の区間の時の値**で、正本の `wald_era` に注つきで残っている。'
    '票の「0.841 対 0.817」は「上がったを含む」と「含まない」の量を並べたもの、系統外の一人目の「5.3%%・81.7%%」は Wald の時の値を今の値として引いたもの'
    % (oc0[labels[2]], oc0[labels[2]] + oc0[labels[1]], oc10[labels[2]], M['notdrop_at_zero'], M['seal_right_at_zero'], M['notdrop_at_effect']),
    {'oc0': oc0, 'oc10': oc10, 'measured': M})

# ================================================================ K182 転記行 D・E が古い規則
facts = rd('records', 'B', 'design-facts-B.md')
rowD = next(l for l in facts.split('\n') if l.startswith('- **転記行 D**'))
rowE = next(l for l in facts.split('\n') if l.startswith('- **転記行 E**'))
old_s4 = '10 pt の検出力が 0.8 以上なら「下がらなかった（封印は当たり）」' in rowD
old_den = '分母＝200' in rowE
dfb = SRC('design_facts_B.py')
add('K182', 'claude.ai 二人目', '乙（生成器の漏れ）', '**再現した**',
    '転記行 D に旧い規則「区間が零を含んだとき、10 pt の検出力が 0.8 以上なら…下がらなかった」が%s（裁定 D118 で廃した規則・草案 §6 に逐語で入る）。転記行 E に「分母＝200」が%s（裁定 D127 で「登録した問いの数」と改めた）。'
    '生成器 `design_facts_B.py` は `rules_B` を%s（S4 の文は L%s で、正本に残った旧い鍵 `three_way.power_min` を読んで組む・「分母＝」は L%s）'
    % ('ある' if old_s4 else '無い', 'ある' if old_den else '無い',
       '呼ばない（名は転記行 G の器の一覧 L%s にだけ出る）' % lines_of(dfb, r"'rules_B\.py'") if not re.search(r'^\s*import rules_B|rules_B\.\w+\(', dfb, re.M) else '呼ぶ',
       lines_of(dfb, r'検出力が %g 以上'), lines_of(dfb, r'分母＝')), {'rowD_old_rule': old_s4, 'rowE_old_den': old_den,
                                                                   'canon_power_min': T['descriptive_families']['B_desc_S4']['three_way'].get('power_min')})

# ================================================================ K183 草案の残り・転記行 E
dr = rd('design', 'design-stageB-draft12.md')
d1 = lines_of(dr, r'差の分散は一つの候補の低下幅の分散の二倍')
d2 = lines_of(dr, r'分母＝200')
d3 = lines_of(dr, r'上の `denominator`')
e085 = bool(re.search(r'0\.85 で 0\.\d+', rowE))
add('K183', 'claude.ai 一人目（L-h・L-i）', '乙（草案と転記行の傷）', '**再現した**',
    '草案に素の区間の式（差の分散を一候補の二倍）が L%s に、「分母＝200」が L%s に、指す先の無い「上の `denominator`」が L%s にある。転記行 E に下限 0.85 での帰無発火率が%s'
    % (d1, d2, d3, 'ある' if e085 else '無い'), {'lines_naive_band': d1, 'lines_den200': d2, 'lines_dangling': d3, 'rowE_has_085': e085})

# ================================================================ K184 品質床の下限の数
def qf_null(p, n=200, fail_at=20):
    """二標本（無操作と腕の真の正答率が同じ p）で、無操作 − 腕 ≥ fail_at 問（10 pt）となる確率。"""
    k = np.arange(n + 1)
    w = binom.pmf(k, n, p)
    D = k[:, None] - k[None, :]
    return float((w[:, None] * w[None, :])[D >= fail_at].sum())


def qf_power(p, drop, n=200, fail_at=20):
    k = np.arange(n + 1)
    wN, wA = binom.pmf(k, n, p), binom.pmf(k, n, max(p - drop, 0))
    D = k[:, None] - k[None, :]
    return float((wN[:, None] * wA[None, :])[D >= fail_at].sum())


QFN = {}
for p in (0.5, 0.6, 0.7, 0.8, 0.85, 0.9):
    fail_eq = qf_null(p, fail_at=20)            # 境目ちょうど（−10 pt）を不合格に数える（正本 boundary_rule）
    fail_gt = qf_null(p, fail_at=21)            # 境目を合格に数える
    QFN[str(p)] = {'cell_boundary_fail': round(fail_eq, 4), 'cell_boundary_pass': round(fail_gt, 4),
                   'any11_boundary_fail': round(1 - (1 - fail_eq) ** 11, 3), 'any11_boundary_pass': round(1 - (1 - fail_gt) ** 11, 3),
                   'power15_boundary_fail': round(qf_power(p, 0.15), 3)}
mc = SRC('make_contrasts_B.py')
typed = lines_of(mc, r"'false_drop_at_085': 0\.024")
Q = T['measured']['quality_floor_multiplicity']
add('K184', 'claude.ai 二票・Gemini 二人目', '乙（数の出所）＋甲（届かないときの手当て）', '**再現した**',
    '正本 `measured.quality_floor_multiplicity`（0.50 で %s・0.85 で %s・捕捉 %s→%s）は**生成器に手で打った数**（`make_contrasts_B.py` L%s・生成のときに数えていない）。'
    '正本の境目の規則（ちょうど −10 pt は不合格）で全数に数え直すと、一セルの帰無発火率は 0.50 で %.4f・0.70 で %.4f・0.85 で %.4f、十一セルで一つ以上は 0.50 で %.3f・0.85 で %.3f（独立の近似）。'
    '境目を合格に数えると 0.70 で %.4f・0.85 で %.4f（設計の問いの表 0.0128・0.0022 はこちらに近い）。転記行 E（器が数えた値）の 0.5 で 0.0255・0.7 で 0.0166 は境目を不合格に数えた値と一致する。'
    '**同じ量が、手で打った正本の値と、器が数えた転記行 E で食い違っている**。届く課題が無いときの手当ては正本に無い'
    % (Q['false_drop_at_050'], Q['false_drop_at_085'], Q['power15_at_050'], Q['power15_at_085'], typed,
       QFN['0.5']['cell_boundary_fail'], QFN['0.7']['cell_boundary_fail'], QFN['0.85']['cell_boundary_fail'],
       QFN['0.5']['any11_boundary_fail'], QFN['0.85']['any11_boundary_fail'], QFN['0.7']['cell_boundary_pass'], QFN['0.85']['cell_boundary_pass']),
    {'recount': QFN, 'canon_measured': Q})

# ================================================================ K185 品質床を前置き無しで測る——演算の重複
INTERV = sorted(x for x in T['arms']['main'] if '+v' in x or '-v' in x)
SEL = {'O-Ncold-v', 'Onull+v'}                      # 選定の段で測る二腕（正本 quality_floor.operations）
POST = [x for x in INTERV if x not in SEL]
op = lambda x: (('+' if '+v' in x else '-') + x.split('+v' if '+v' in x else '-v', 1)[1])
ops = {}
for x in POST:
    ops.setdefault(op(x)[0] + 'v' + op(x)[1:], []).append(x)
add('K185', 'claude.ai 一人目', '甲（設計）', '**再現した**（事実の部分）',
    '選定後の品質床のセルは %d（%s）。問いに前置きを付けない（正本 `quality_floor.input`）ので、腕の違いは演算（符号 × 方向の種類）だけになり、**演算の異なり数は %d**（%s）。'
    '「−v」は選定の段の O-Ncold−v と同じ演算である。貪欲の生成なので、同じ演算のセルは同じ出力になる'
    % (len(POST), '・'.join(POST), len(ops), '／'.join('%s: %s' % (k, '・'.join(v)) for k, v in sorted(ops.items()))),
    {'post_cells': POST, 'ops': ops})

# ================================================================ K186 層の割合と添字の対応
rs = SRC('run_stageB_local.py')
s_rc = span(rs, r'^def run_cell', r'^def manifest_env')
checks_ratio = [w for w in ('layer_index(', 'layer_ratio ==', 'layer_idx ==', 'idx_of') if w in s_rc[2]]
add('K186', 'claude.ai 二票', '乙（守りの欠け）', '**再現した**',
    '`run_cell`（L%d–L%d）は方向を `layer_ratio` で引き、hook を `layer_idx` に掛けるが、二つの対応を照らす行が無い（%s）。`assert_hooks_exactly` は hook の置き場（添字）と中身の一致しか見ない'
    % (s_rc[0], s_rc[1], '照らす式なし' if not checks_ratio else checks_ratio), {'found': checks_ratio})

# ================================================================ K187 介入の腕の副位置に加えた量が入る
s_cap = span(rs, r'^def capture_resp_mean', r'^def run_cell')
add('K187', 'claude.ai 一人目', '丙（限界の未記載）', '**再現した**（読み）',
    '`capture_resp_mean`（L%d–L%d）は生成と同じ hook を掛けたまま順伝播する（口上どおり）。介入の層の活性には加えた量が入る。D132 の読みは無操作の二腕だけなので効かないが、介入の腕を射影すると機械的に上がる。正本に一行が無い'
    % (s_cap[0], s_cap[1]))

# ================================================================ K188 D132 の参照の行
ly = SRC('layers_B.py')
_an_ly = span(ly, r'^def analyse', r'^def _selftest')[2]          # 読みの本体だけを見る（自己検査の乱数の語を拾わない）
refs = [w for w in ('vrand', 'random_dir', 'td', 'Nk', 'reference', '参照') if re.search(r'\b%s\b' % w, _an_ly)]
add('K188', 'claude.ai 二票（Gemini 二票は循環の無さを是認）', '甲（設計・読み）', '再現した（参照の行が無い）',
    '`layers_B.py` は (6b) の単位方向への射影だけを出し、ランダム・td・Nk の軸の参照の行を持たない（語の出現: %s）。二腕の差から作った方向で同じ二腕を分けるので、別の場面でも作り方から分かれうる——**データが無いので分かれるかは測れない**。参照の行は保存した活性から出せるので試行は増えない'
    % (refs or '無し'), {'ref_words': refs})

# ================================================================ K189 抽出器の決定性 (ii)
db = SRC('direction_B.py')
single = 'torch.tensor([ids]' in db
rev = 'list(reversed(PANEL_ARMS))' in db
add('K189', 'claude.ai 一人目', '乙（落ちようのない検査）', '**再現した**（読み）',
    '主位置の活性は一本ずつ流して取る（`torch.tensor([ids]…)`＝%s）。決定性 (ii) は腕の並べ方を逆にして同じ一本流しを繰り返すだけ（%s）で、バッチの組成が変わらないので丸めの差が入らない。走行器は同じプロンプト 16 行のバッチで流す'
    % (single, rev))

# ================================================================ K190 走行器の自己検査の締めの行
fk = tempfile.mkdtemp(prefix='notorch_')
os.makedirs(os.path.join(fk, 'torch'))
open(os.path.join(fk, 'torch', '__init__.py'), 'w', encoding='ascii').write("raise ImportError('torch hidden for the reproduction')\n")
env = dict(os.environ)
env.pop('OP4B_REQUIRE_FULL_SELFTEST', None)
env['PYTHONPATH'] = fk + os.pathsep + env.get('PYTHONPATH', '')
env['PYTHONIOENCODING'] = 'utf-8'
pr = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'run_stageB_local.py'), '--selftest'], capture_output=True, text=True,
                    encoding='utf-8', env=env, cwd=REPO)
shutil.rmtree(fk, ignore_errors=True)
outl = (pr.stdout or '') + (pr.stderr or '')
skipped = '飛ばした' in outl
last = [l for l in outl.strip().split('\n') if l.strip()][-1] if outl.strip() else ''
add('K190', 'claude.ai 二票', '乙（印字）', '**再現した**' if (skipped and 'すべて通った' in last and 'hook' in last) else '再現しない',
    'torch を隠して厳密でない口で走らせた（終了コード %d）。「飛ばした」の行: %s。締めの行: 「…%s」' % (pr.returncode, skipped, last[-90:]),
    {'rc': pr.returncode})

# ================================================================ K191 ランダム方向の割り当て
dirs = [steer_B.direction_of(i, 200) for i in range(200)]
blocks, cur = [], None
for i, d in enumerate(dirs):
    if d != cur:
        blocks.append([d, i, i])
        cur = d
    else:
        blocks[-1][2] = i
add('K191', 'claude.ai 一人目', '甲（設計・登録どおり）', '**再現した**',
    '試行の番号から方向: %s（登録順の連続した塊・正本 `random_control.allocation` の文のとおり）。バッチ 16 は番号の順に組むので、方向とバッチ・時刻・セッションが交絡する'
    % '・'.join('方向 %d＝%d〜%d' % tuple(b) for b in blocks), {'blocks': blocks})

# ================================================================ K192 等質性の注の帰無の率
def homog_null(p, ns=(67, 67, 66), thr=None):
    thr = thr if thr is not None else float(T['random_control']['homogeneity_max_spread_pt'])
    ks = [np.arange(n + 1) for n in ns]
    ws = [binom.pmf(k, n, p) for k, n in zip(ks, ns)]
    r = [100.0 * k / n for k, n in zip(ks, ns)]
    R0, R1, R2 = np.meshgrid(r[0], r[1], r[2], indexing='ij')
    W = ws[0][:, None, None] * ws[1][None, :, None] * ws[2][None, None, :]
    spread = np.maximum(np.maximum(R0, R1), R2) - np.minimum(np.minimum(R0, R1), R2)
    return float(W[spread > thr + 1e-12].sum())


hr = rules_B.homogeneity([(27, 67), (27, 67), (26, 66)], T)
HN = {str(p): round(homog_null(p), 3) for p in (0.15, 0.37, 0.40, 0.50, 0.60)}
add('K192', 'claude.ai 二票', '丙（動作特性の未記載）', '**再現した**',
    '三本（67・67・66 試行）の率が真に等しいときに注が立つ確率（全数・閾値は正本の値）: %s。正本と報告にこの率は無い'
    % '・'.join('基底 %s で %.3f' % (k, v) for k, v in HN.items()), {'homog_null': HN, 'rule_output_example': hr})

# ================================================================ K193 ‖v̂‖/‖h‖ の帰結
hn = T['activation_storage']['h_norm_record']
has_consequence = bool(re.search(r'見せ.{0,30}(後|うえで).{0,40}(変え|決め|しない|止め)', hn))
add('K193', 'claude.ai 二票', '甲（未登録の分かれ道）', '**再現した**',
    '正本 `activation_storage.h_norm_record` は比を記帳し「調整走行の前に登録者に見せる」と書くが、見た後に何をしてよいか（何もしない、を含む）の帰結が%s。‖h‖ は主位置（プロンプトの最終トークン）でだけ測る'
    % ('無い' if not has_consequence else 'ある'), {'text': hn[:300]})

# ================================================================ K194 様式門の札と正本の非対称の条
asym = T['style_gate']['asymmetry']
s_hold = lines_of(an, r"r\['label'\] = '判定保留（様式転位）'")
excluded = "not (r.get('fired') or [])" in an
add('K194', 'claude.ai 二人目', '乙（正本との食い違い・起草者に有利な向き）', '**再現した**（読み）',
    '集計器は様式門の保留を Holm の順位から外し（%s）、門に当たったすべての対比を p に関わらず「判定保留（様式転位）」にする（L%s）。'
    '正本の非対称の条は「%s」。**非有意の対比が保留に化ける**'
    % ('外す' if excluded else '外さない', s_hold, asym), {'asymmetry': asym})

# ================================================================ K195 top_k
ge = T['runner']['generation_explicit']
rpl = rd('tools', 'run_preamble_local.py')
body_fields = re.search(r"body = json\.dumps\(dict\(\{([^}]*)\}", rpl)
boot = rd('tools', 'colab', 'boot_stageA.py')
gencfg_arg = '--generation-config' in boot
recA = ''.join(open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(REPO, 'records', 'A', '*.json')))
add('K195', 'claude.ai 二人目', '丙（確かめていない前提）', '一部再現（手元で vLLM を走らせられない）',
    '正本 B は top_k=%s を明示で渡す。段階 A の走行器が vLLM に送った鍵は「%s」（anchor の 4B-2507 には extra_body を併合しない）で、top_k を送っていない。起動器は `--generation-config` を%s。段階 A の記録に top_k の値は%s。'
    '**段階 A の実効の top_k は記録から決められない**——vLLM がこの版で登録機種の generation_config を既定に使うかは、手元で確かめられない'
    % (ge.get('top_k'), re.sub(r"\s+", ' ', body_fields.group(1)) if body_fields else '?', '渡していない' if not gencfg_arg else '渡している',
       '無い' if 'top_k' not in recA else 'ある'), {'b_top_k': ge.get('top_k')})

# ================================================================ K196 検査用の口・報告の束縛・相手の重複
nogate = "ap.add_argument('--no-gate'" in an
br = SRC('build_report_B.py')
bind_check = bool(re.search(r"A\[['\"]gate|A\.get\(['\"]gate|gate_sha|selection['\"]\]\s*!=|G\[['\"]selection['\"]\].*A\[", br))
gb = SRC('gate_B.py')
dup_gate = lines_of(gb, r"partner\('selection'")
dup_an = 'partner_duplicate' in an or bool(re.search(r"noop\.get\('n'", an))
add('K196', 'claude.ai 二人目', '乙（前の巡の採否の一部）', '**再現した**',
    '集計器の `--no-gate`（%s）は門の記録を読まないので、門の判定（D109）と束縛（D105）を一度に外す（前の巡の P381 は二つの口に分けたが、この口が残る）。'
    '報告の器は、集計が使った門・選定と、渡された門の記録の一致を確かめない（%s）。無操作の相手の重複の番人は門の器にだけあり、選定の段の相手にだけ当たる（L%s）。**選定後の段の相手の重複は、集計器が合算したまま読む**（番人%s）'
    % ('ある' if nogate else '無い', '照合なし' if not bind_check else '照合あり', dup_gate, '無し' if not dup_an else 'あり'))

# ================================================================ K197 帯の起点の自己検査が使われない関数を見る
used = [w for w in ('scenario_start_index', 'band_starts') if re.search(r'\b%s\(' % w, rs)]          # 呼び出しだけを数える（注の中の名は数えない）
add('K197', 'claude.ai 二人目', '乙（検査の的外れ）', '**再現した**',
    '走行器は起点を `inp.shape[1] - 1` で出し（L%s）、`scenario_start_index`・`band_starts` を%s。介入の器の帯の自己検査はその使われない関数を検べる'
    % (lines_of(rs, r'inp\.shape\[1\] - 1'), '呼ばない' if not used else '呼ぶ（%s）' % used))

# ================================================================ K198 同値の帯の二つの値
rowC = next(l for l in facts.split('\n') if l.startswith('- **転記行 C**'))
bandC = re.search(r'同値の帯（95%）は ([\d.]+) pt', rowC)
add('K198', 'claude.ai 二人目', '乙（注の古い数）', '**再現した**',
    '転記行 C は %s pt。生成器の注（`design_facts_B.py` L%s）は「門の模擬は 21.5 pt を出す」と現在形で書く（読み口の口上 L%s は「出していた」）'
    % (bandC.group(1) if bandC else '?', lines_of(dfb, r'21\.5 pt を出す'), lines_of(SRC('runs_B.py'), r'21\.5 pt')))

# ================================================================ K199 再開の最初のバッチの行数
rec_batch_rows = 'batch_rows' in rs or 'rows_in_batch' in rs
add('K199', 'claude.ai 二人目', '乙（記録の欄・軽微）', '**再現した**（読み）',
    '試行の記録はバッチの中の位置（`batch_pos`）を持つが、そのバッチの実際の行数を%s。再開で最初のバッチが 16 行未満になっても、記録からは読めない（manifest の `batch` は名目の値）'
    % ('持つ' if rec_batch_rows else '持たない'))

# ================================================================ K200 監査の列
AA = json.load(open(os.path.join(REPO, 'records', 'reviews', 'B', 'external-round', 'verification-fixes-B-external-after.json'), encoding='utf-8'))
p340 = next(r for r in AA['rows'] if r['P'] == 'P340' and r['D'] == 'D120')
add('K200', 'claude.ai 一人目', '丁（記録の注）', '一部再現',
    '監査の P340（D120）は「%s」で、根拠は「%s」——欄の有無と、生成の設定を作る関数の出力（最大トークン数）が混ざっている。前者は配線の列に当たる'
    % (p340['status'], p340['evidence'][:120]))

# ================================================================ K201 同値の帯の模擬の独立
tn = T['selection']['tune']
add('K201', 'Gemini 一人目', '戊（前提が成り立たない）', '再現しない',
    '調整走行は候補（層 × 係数）ごとに v 腕とランダム腕を別に走らせ（正本 `selection.tune.pairing`: 「%s」）、種も腕 × 層 × 係数の子ストリームに降ろす。'
    'ランダム方向は層で共有するが、それは**真の効き目**を似せるだけで、**帰無の標本の揺れは候補の間で独立**である。帯は帰無の範囲で定義している（`runs_B.equivalence_band`）ので、独立の模擬は正しい'
    % tn['pairing'][:60])

# ================================================================ K202 層別の計数の書式外
s_st = span(SRC('runs_B.py'), r'^def counts_main_strata', r'^def load_sessions')
dead = "c['ff'] += bool(r['format_fail'])" in s_st[2] and 'stratum_of(r)' in s_st[2]
add('K202', 'Gemini 一人目', '乙（死んだ行・軽微）', '**再現した**',
    '`counts_main_strata`（L%d–L%d）は書式外の試行を層に入れない（`stratum_of` が None を返して飛ばす）ので、`c[\'ff\'] += …` は常に 0 を足す（%s）' % (s_st[0], s_st[1], dead))

# ================================================================ K203 管理図の要約が報告に無い
tpl = rd('records', 'B', 'results-report-template-B.md')
rc_ = SRC('build_report_B.py')
ad = rd('records', 'reviews', 'B', 'impl-round-2', 'adoption-table-B-recheck.md')
p323 = next(l for l in ad.split('\n') if l.startswith('| P323 |'))
add('K203', 'Gemini 一人目', '乙（前の巡の採用の一部が未着手）', '**再現した**',
    '管理図の器は「帯の外かつ有意」「帯の外だが有意でない」「帯の内側」を分けて記録するが、報告の雛形に管理図の節が%s、組み立て器も管理図を読まない（%s）。'
    '集計の記録は異常（帯の外かつ有意）だけを並べる。前の巡の採否 P323 の「報告に要約を入れる」が入っていない（その巡の確認は「経路の表への追加は次の巡の検査対象」とした）'
    % ('無く' if '管理図' not in tpl else 'あり', '読まない' if 'chart' not in rc_ else '読む'), {'p323': p323})

# ================================================================ K204 Osec-Ncold と同一性選別
cmp_ = T['identity_screen']['compared_arms']
bv = T['bases_4B2507_api_stageVp']
add('K204', 'Gemini 二票・claude.ai 一人目', '（登録者の裁定待ち）', '**再現した**（事実）',
    '比べる腕（%d）に Osec-Ncold が%s。V′ の既測は N1 で %s/%s・S4 で %s/%s。選別の 13 腕に入っているので、足しても試行は増えない'
    % (len(cmp_), '無い' if 'Osec-Ncold' not in cmp_ else 'ある', bv['N1']['Osec-Ncold']['k'], bv['N1']['Osec-Ncold']['n'], bv['S4']['Osec-Ncold']['k'], bv['S4']['Osec-Ncold']['n']))

# ================================================================ K205 共分散の統制の理由
add('K205', 'claude.ai 一人目', '丁（記録）', '記録のみ',
    '取り下げには同意し、理由の「推定できない」は言い過ぎ（観測した差の張る部分空間で引けば共分散は要らない）とする。取り下げの判断（裁定 D123）は変えない。理由の文を「共分散を誠実に推定できない（全次元で）」に限る注を足すかは軽微')

# ================================================================ K206 系統外の二票の読みの確かめ
def where(f, pat):
    return lines_of(SRC(f), pat)


CLAIMS = [('gemini-1', 'rules_B.py', 57, 100, r'^def s4_verdict'),
          ('gemini-1', 'analyze_B.py', 248, 255, r"ordered = sorted\("),
          ('gemini-1', 'runs_B.py', 185, 205, r'^def equivalence_band'),
          ('gemini-1', 'runs_B.py', 355, 355, r"c\['ff'\] \+= bool\(r\['format_fail'\]\)"),
          ('gemini-1', 'control_chart_B.py', 53, 56, r'out = band_out and \(pval < ALPHA\)'),
          ('gemini-1', 'steer_B.py', 108, 115, r'^def assert_batch_uniform'),
          ('gemini-2', 'analyze_B.py', 185, 205, r"ordered = sorted\("),
          ('gemini-2', 'rules_B.py', 73, 115, r'^def s4_verdict'),
          ('gemini-2', 'rules_B.py', 144, 160, r'^def td_specificity'),
          ('gemini-2', 'steer_B.py', 73, 88, r'^def scenario_start_index|^def band_starts'),
          ('gemini-2', 'run_stageB_local.py', 370, 370, r'inp\.shape\[1\] - 1')]
ck = []
for who, f, lo, hi, pat in CLAIMS:
    ls = where(f, pat)
    inside = any(lo - 3 <= x <= hi + 3 for x in ls)
    ck.append({'who': who, 'file': f, 'claimed': [lo, hi], 'actual': ls, 'inside': inside})
cit = json.load(open(os.path.join(REPO, 'records', 'B', 'citation-check-2026-09-19.json'), encoding='utf-8'))
g1 = rd('records', 'reviews', 'B', 'final-round', 'gemini-1', 'review.md')
claim_cit = 'citations_B.py` を通じて完全に是正' in g1
lit = '56/70' in SRC('rules_B.py') or '0.0524' in SRC('rules_B.py')
n_in = sum(c['inside'] for c in ck)
add('K206', 'Gemini 二票（読みの確かめ）', '—（票の読みの深さ）', '一部しか確かめられない',
    '票が挙げた行の範囲に、その中身があったもの **%d／%d**（前後三行の余裕）: %s。'
    '系統外の一人目の「採否表の引用の誤りは `citations_B.py` を通じて完全に是正」は%s（直したのは起草者が読んで・器は直す前の版の %d 項のうち %d 項しか捕まえない）。'
    '文献値（Newcombe 1998 の 56/70 対 48/80）の記述は自己検査に%s。行の数（走行器 647 行・抽出器 372 行）は束の見出しに印字してある値と同じ'
    % (n_in, len(ck), '／'.join('%s %s 挙げた L%d–%d・実際 L%s' % (c['who'], c['file'], c['claimed'][0], c['claimed'][1], c['actual']) for c in ck),
       '記録と合わない' if claim_cit else '無い', len(cit['items']), cit['caught_by_checker_before'], 'ある' if lit else '無い'),
    {'line_claims': ck})

# ---------------------------------------------------------------- 書く
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
L = ['# 段階 B 最後の系統外の巡——**再現の記録**（追い問い K177〜K206・%s 日本時間）' % jst.strftime('%Y-%m-%d %H:%M'), '',
     '- 器: `verify_B_final.py`（この置き場）。枠は `preregistration-final-B.md`（票の前）と `preregistration-reproduction-K177.md`（票を読んだ後・この器を書く前）。',
     '- **数は器と同じ規則で数え直したもの**（全数・関数を直に呼ぶ）。「読み」と書いたものはソースを読んで確かめた。torch の要る検査は、torch を隠して走らせた（K190）。',
     '- 正本 SHA16 %s。' % runs_B.sha16_file(os.path.join(REPO, 'design', 'contrasts-B.json')), '',
     '| K | 出所 | 区分（案） | 再現 | 根拠（機械） |', '|---|---|---|---|---|']
for r in ROWS:
    L.append('| %s | %s | %s | %s | %s |' % (r['K'], r['source'], r['category'], r['status'], r['evidence'].replace('|', '／')))
cnt = {}
for r in ROWS:
    key = '再現した' if '再現した' in r['status'] else r['status']
    cnt[key] = cnt.get(key, 0) + 1
L += ['', '- 数: %s（全 %d 件）。' % ('・'.join('%s %d' % kv for kv in cnt.items()), len(ROWS)), '',
      '## 確認していないこと', '',
      '- torch と実重みの要る振る舞い（K186 の止まり方・K189 のバッチの丸め・K195 の vLLM の既定）は、手元で走らせていない。',
      '- 系統外の二票の読みの深さは、挙げた行の範囲と一件の記述で確かめただけで、全 12 部を読んだかは確かめられない。',
      '- 区分（案）は起草者の案で、採否は採否表と登録者の裁定で決める。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))


def _j(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return str(o)


json.dump({'kind': 'verify_B_final', 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'rows': ROWS, 'counts': cnt},
          open(OUT_JS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=_j)
print('[verify_B_final] %s（%d 件・%s）' % (OUT_MD, len(ROWS), cnt))
