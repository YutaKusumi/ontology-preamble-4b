# -*- coding: utf-8 -*-
"""verify_fixes_B_final.py —— 最後の系統外の巡の**直しの監査**（枠 `preregistration-fix-audit-B-final.md`・器を書く前に登録した）。

採否表 `adoption-table-B-final.md` で「採用」「裁定へ」とした行と、登録者裁定 D133〜D143 を、**現物の器で一件ずつ当て直す**。
器の振る舞いの件は器を走らせて確かめる（関数を直に呼ぶ・合成データを門と集計器に通す・torch を隠して自己検査を走らせる）。
**二度走らせる**——直す前（--label before）と直した後（--label after）。直す前に「直っている」と出た検査には「働いていない」の印を付ける。
出力: verification-fixes-B-final-<label>.{md,json}（--force が無ければ上書きしない）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, shutil, tempfile, subprocess, argparse, datetime, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
PY = sys.executable
ap = argparse.ArgumentParser()
ap.add_argument('--label', required=True, choices=['before', 'after'])
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
OUT = os.path.join(HERE, 'verification-fixes-B-final-%s.md' % a.label)
if os.path.exists(OUT) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % OUT)
import runs_B, rules_B, steer_B
T = runs_B.load_T()
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n') if os.path.exists(os.path.join(REPO, *p)) else ''
S = lambda f: rd('tools', f)
OK_B, OK_W, OK_T, NG = '直っている（振る舞い）', '直っている（配線）', '直っている（文）', '直っていない'
ROWS = []


def check(P, D, what, fn):
    try:
        st, ev = fn()
    except Exception as e:                    # 器が無い・関数が無い・形が違う——直っていない
        st, ev = NG, '検査が例外で止まった: %s: %s' % (type(e).__name__, str(e)[:160])
    ROWS.append({'P': P, 'D': D, 'what': what, 'status': st, 'evidence': ev})


DRAFT13 = 'design/design-stageB-draft13.md'
DR = rd(*DRAFT13.split('/'))
TPL = rd('records', 'B', 'results-report-template-B.md')
FACTS = rd('records', 'B', 'design-facts-B.md')
MC = S('make_contrasts_B.py')
AN = S('analyze_B.py')
RS = S('run_stageB_local.py')
BR = S('build_report_B.py')
MU = S('mutation_B.py')


def latest_dry():
    fs = sorted(f for f in os.listdir(os.path.join(REPO, 'records', 'B')) if re.match(r'^dry-run-B-\d{4}-\d{2}-\d{2}\.md$', f))
    return rd('records', 'B', fs[-1]) if fs else ''


DRY = latest_dry()


def dry_fired(path_name):
    """合成データによる検査の記録で、その経路が一度以上発火したか（発火した場合の数・経路が表に無ければ None）。
    直す前の走行の後に改めた（2026-09-19）: 前は「| 名 | 数 |」の形を読んでいたが、経路の表の第二列は**発火した場合の名の並び**
    （無ければ「**発火せず**」）で、この読み方は常に None を返していた（直す前の P385・P410 の判定は、ほかの条件でも「直っていない」だった）。"""
    m = re.search(r'^\| %s \| (.*) \|$' % re.escape(path_name), DRY, flags=re.M)
    if not m:
        return None
    cell = m.group(1).strip()
    return 0 if (not cell or '発火せず' in cell) else len([x for x in cell.split('・') if x.strip()])


# ---- 合成データを門と集計器に通す（集計器の振る舞いを見る・一度だけ） ----
_td = tempfile.mkdtemp(prefix='fixaudit_')
AJ = None
try:
    root = os.path.join(_td, 'all')
    r1 = subprocess.run([PY, os.path.join(REPO, 'tools', 'synth_B.py'), '--case', 'all', '--out-root', root], capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    r2 = subprocess.run([PY, os.path.join(REPO, 'tools', 'gate_B.py'), '--root', root, '--allow-dry', '--out', os.path.join(root, 'g.md'), '--force'],
                        capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    seal = os.path.join(root, 'seal-B.json')
    cmd = [PY, os.path.join(REPO, 'tools', 'analyze_B.py'), '--root', root, '--gate', os.path.join(root, 'g.json'), '--allow-dry', '--allow-partial-seal',
           '--out', os.path.join(root, 'a.md'), '--force'] + (['--seal', seal] if os.path.exists(seal) else [])
    r3 = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    if os.path.exists(os.path.join(root, 'a.json')):
        AJ = json.load(open(os.path.join(root, 'a.json'), encoding='utf-8'))
    PIPE_ERR = '' if AJ else ('集計器が記録を書かなかった: %s' % ((r3.stdout or '') + (r3.stderr or ''))[-300:])
finally:
    shutil.rmtree(_td, ignore_errors=True)


# ================================================================ 裁定 D133〜D143
def c384():
    f = rules_B.td_specificity_family
    items = [dict(scenario='N1', k_v=70, n_v=200, k_td=100, n_td=200, conf_label='確証', conf_diff_pt=-20.0),
             dict(scenario='S1', k_v=100, n_v=200, k_td=70, n_td=200, conf_label='確証', conf_diff_pt=-20.0),
             dict(scenario='SK', k_v=70, n_v=200, k_td=100, n_td=200, conf_label='非有意', conf_diff_pt=-5.0),
             dict(scenario='S4', k_v=90, n_v=200, k_td=95, n_td=200, conf_label='確証', conf_diff_pt=-20.0)]
    got = [o['label'] for o in f(items, T)]
    want = ['書ける', 'td のほうが動いた', '書かない', '書かない']
    null = (T.get('measured') or {}).get('td_specificity_null')
    mut = '向きを見ない' in MU
    ok = got == want and null and mut
    return (OK_B if ok else NG), '札 %s（期待 %s）・帰無の動作特性 %s・変異 %s' % (got, want, 'あり' if null else '無し', mut)


def c385():
    g = rules_B.s4_gates
    A = dict(cat=20, n_ok=200, ff=0, refuse=0, gap=0)
    B = dict(cat=24, n_ok=200, ff=80, refuse=0, gap=0)
    f1 = g(A, B, T)
    f2 = g(dict(A, gap=3), B, T)
    wire = 'rules_B.s4_gates(' in AN
    dry = dry_fired('S4: 門で保留')
    ok = ('判定保留（書式外転位）' in f1) and ('判定不能（採点欠落）' in f2) and wire and (dry or 0) > 0
    return (OK_B if ok else NG), '薄まった例 %s・採点欠落の例 %s・集計器が呼ぶ %s・合成データの経路 %s' % (f1, f2, wire, dry)


def c386():
    m = rules_B.s4_seal_match
    lab = rules_B.s4_labels(T)
    cases = [((lab[0], '低下'), '当たり'), ((lab[0], 'どちらでもない'), '外れ'), ((lab[2], 'どちらでもない'), '当たり'),
             ((lab[1], '上昇'), '当たり'), ((lab[3], '低下'), '言えない'), (('判定保留（書式外転位）', '低下'), '言えない')]
    got = [m(o, s, T) for (o, s), _ in cases]
    want = [w for _, w in cases]
    no_seal_word = not any('封印' in x for x in lab)
    ok = got == want and no_seal_word
    return (OK_B if ok else NG), '照合 %s（期待 %s）・札に「封印」の語が無い %s' % (got, want, no_seal_word)


def c387():
    lab = rules_B.s4_labels(T)
    eff = T['descriptive_families']['B_desc_S4']['three_way']['effect_pt']
    has_eff = ('%s pt' % eff) in lab[2]
    s4 = (AJ or {}).get('s4') or {}
    fields = all(k in s4 for k in ('relative_size', 'oc_at_observed_partner'))
    clause = 's4_effect_D136' in (T.get('reading_D128') or {})
    pend = 'S4 の効き目' not in (DR.split('### 5-補')[-1][:1500] if DR else 'S4 の効き目')
    ok = has_eff and fields and clause and pend and bool(DR)
    return (OK_B if ok else NG), '札に効き目 %s・集計の記録に相対と動作特性 %s・読み条項 %s・§5-補 から消えた %s' % (has_eff, fields, clause, pend)


def c391():
    Q = T['measured']['quality_floor_multiplicity']
    f = rules_B.qf_null_rate
    v = round(f(0.85, 200, T), 4)
    typed = bool(re.search(r"'false_drop_at_085': 0\.0\d+", MC))
    rowE = next((l for l in FACTS.split('\n') if l.startswith('- **転記行 E**')), '')
    e085 = bool(re.search(r'0\.85 で 0\.\d+', rowE))
    qf = T['quality_floor']
    rules = 'base_min_fallback' in qf and 'task_tiebreak' in qf
    ok = (abs(Q.get('cell_at_085', -1) - v) < 1e-4) and not typed and e085 and rules
    return (OK_B if ok else NG), '正本の一セル（0.85）%s 対 器 %s・手で打った数 %s・転記行 E の 0.85 %s・手当てと割り方の条 %s' % (Q.get('cell_at_085'), v, typed, e085, rules)


def c392():
    # 直す前の走行の後に改めた（2026-09-19）: 「前置きを付ける」の語は旧い条の「前置きを付けると…」にも含まれ、直す前でも満たされた。
    # 裁定 D138 の条に固有の語（土台の前置きを付けて測る・付けない側に戻る）で見る。基準（条があり草案が束縛する）は変えていない。
    inp = T['quality_floor']['input']
    new_rule = ('土台の前置きを付けて測る' in inp) and ('付けない側に戻る' in inp)
    bound = '{{quality_floor/input}}' in rd('design', 'design-stageB-draft13.src.md')
    ok = new_rule and bound
    return (OK_T if ok else NG), '正本の入力の条（裁定 D138 の語）%s・草案13B が束縛 %s' % (new_rule, bound)


def c395():
    import layers_B
    importlib.reload(layers_B)
    rows = layers_B.reference_rows_selftest()
    kinds = sorted({r['axis'] for r in rows})
    clause = '機序の証拠ではない' in json.dumps(T['descriptive_families']['B_desc_layer'], ensure_ascii=False)
    ok = set(kinds) >= {'rand0', 'rand1', 'rand2', 'td', 'Nk'} and clause
    return (OK_B if ok else NG), '参照の行の軸 %s・読み条項 %s' % (kinds, clause)


def c398():
    importlib.reload(steer_B)
    seq = [steer_B.direction_of(i, 200) for i in range(6)]
    cnt = [sum(1 for i in range(200) if steer_B.direction_of(i, 200) == d) for d in range(3)]
    ok = seq == [0, 1, 2, 0, 1, 2] and cnt == steer_B.allocate(200, 3)
    return (OK_B if ok else NG), '番号 0〜5 の方向 %s・各方向の数 %s（等分 %s）' % (seq, cnt, steer_B.allocate(200, 3))


def c400():
    h = T['activation_storage']['h_norm_record']
    ok = ('格子は変えない' in h) and ('主位置' in h and '生成トークン' in h)
    return (OK_T if ok else NG), '帰結の文 %s・主位置だけの限界 %s' % ('格子は変えない' in h, '生成トークン' in h)


def c402():
    ge = T['runner']['generation_explicit']
    need = re.search(r'NEED_VALUES\s*=\s*\[[\s\S]*?\]', S('freeze_B.py'))
    in_need = bool(need) and "'top_k_stageA_effective'" in need.group(0)
    in_pend = 'top_k' in (DR.split('### 5-補')[-1][:2000] if DR else '')
    ok = ('top_k_rule' in ge) and in_need and in_pend
    return (OK_T if ok else NG), '決め方の条 %s・凍結時に記帳する値 %s・§5-補 %s' % ('top_k_rule' in ge, in_need, in_pend)


def c411():
    cmp_ = T['identity_screen']['compared_arms']
    n = T['identity_screen'].get('n_differences')
    ok = 'Osec-Ncold' in cmp_ and n == 3 * len(cmp_)
    return (OK_T if ok else NG), '比べる腕に Osec-Ncold %s・差の数 %s（腕 %d × 三つの率）' % ('Osec-Ncold' in cmp_, n, len(cmp_))


# ================================================================ 採用の行
def c389():
    rowD = next((l for l in FACTS.split('\n') if l.startswith('- **転記行 D**')), '')
    rowE = next((l for l in FACTS.split('\n') if l.startswith('- **転記行 E**')), '')
    old = '検出力が' in rowD and '「下がらなかった' in rowD
    oc = rules_B.s4_oc(0.1725, 200, 10, T)
    lab = rules_B.s4_labels(T)
    num = ('%.3f' % oc[lab[2]]) in rowD
    pm = 'power_min' in T['descriptive_families']['B_desc_S4']['three_way']
    den = '分母＝200' in rowE
    ok = not old and num and not pm and not den
    return (OK_B if ok else NG), '転記行 D の旧い規則 %s・器の値 %.3f が行にある %s・正本の power_min %s・転記行 E の「分母＝200」%s' % (old, oc[lab[2]], num, pm, den)


def c390():
    bad = [w for w in ('差の分散は一つの候補の低下幅の分散の二倍', '分母＝200', '上の `denominator`') if w in DR]
    ok = bool(DR) and not bad
    return (OK_T if ok else NG), '草案13B に残る古い文 %s（草案13B %s）' % (bad, 'あり' if DR else '無し')


def c393():
    import run_stageB_local as R
    importlib.reload(R)
    f = R.layer_binding_ok
    n_layers = 36
    good = f(0.5, steer_B_layer(0.5, n_layers), n_layers)
    bad = f(0.5, steer_B_layer(0.5, n_layers) + 1, n_layers)
    wire = 'layer_binding_ok(' in re.search(r'def run_cell[\s\S]*?\n(?=def )', RS).group(0)
    mut = '層の添字' in MU
    ok = good and not bad and wire and mut
    return (OK_B if ok else NG), '正しい添字 %s・一つずれた添字 %s・run_cell が呼ぶ %s・変異 %s' % (good, bad, wire, mut)


def steer_B_layer(r, n):
    import direction_B
    return direction_B.layer_index(r, n)


def c394():
    rm = T['activation_storage']['response_mean']
    note = '加えた量' in json.dumps(rm, ensure_ascii=False)
    field = "'added_norm'" in RS or '"added_norm"' in RS
    ok = note and field
    return (OK_W if ok else NG), '正本の一行 %s・走行の記録の欄 %s' % (note, field)


def c396():
    db = S('direction_B.py')
    ok = bool(re.search(r'def main_position_activation_batch|batch_rows\s*=|\[ids\]\s*\*\s*\w+', db)) and 'determinism_cross_order(' in db
    return (OK_W if ok else NG), '決定性 (ii) がバッチの組成を変えた値を比べる %s' % ok


def c397():
    fk = tempfile.mkdtemp(prefix='notorch_')
    os.makedirs(os.path.join(fk, 'torch'))
    open(os.path.join(fk, 'torch', '__init__.py'), 'w', encoding='ascii').write("raise ImportError('torch hidden for the audit')\n")
    env = dict(os.environ)
    env.pop('OP4B_REQUIRE_FULL_SELFTEST', None)
    env['PYTHONPATH'] = fk + os.pathsep + env.get('PYTHONPATH', '')
    env['PYTHONIOENCODING'] = 'utf-8'
    p = subprocess.run([PY, os.path.join(REPO, 'tools', 'run_stageB_local.py'), '--selftest'], capture_output=True, text=True, encoding='utf-8', env=env, cwd=REPO)
    shutil.rmtree(fk, ignore_errors=True)
    out = ((p.stdout or '') + (p.stderr or '')).strip().split('\n')
    last = out[-1] if out else ''
    claims = 'hook の帯と復号の段と行ごとの方向: すべて通った' in last
    ok = p.returncode == 0 and not claims
    return (OK_B if ok else NG), 'torch を隠した口の終了コード %d・締めの行が hook を通ったと言う %s（…%s）' % (p.returncode, claims, last[-70:])


def c399():
    hn = T['random_control'].get('homogeneity_null_rate')
    tpl = 'random_control/homogeneity_null_rate' in rd('records', 'B', 'results-report-template-B.src.md')
    ok = bool(hn) and tpl
    return (OK_B if ok else NG), '正本の帰無の率 %s・雛形が束縛 %s' % ('あり' if hn else '無し', tpl)


def c401():
    f = rules_B.style_hold_label
    got = [f(0.2), f(0.01)]
    wire = 'rules_B.style_hold_label(' in AN
    ok = got == ['非有意', '判定保留（様式転位）'] and wire
    return (OK_B if ok else NG), '札（p 0.2・0.01）%s・集計器が呼ぶ %s' % (got, wire)


def c403():
    nogate = "'--no-gate'" in AN
    bind = 'gate_sha16' in BR and 'gate_sha16' in AN
    dup = bool(re.search(r'partner_duplicate|相手の重複', AN))
    ok = not nogate and bind and dup
    return (OK_W if ok else NG), '集計器の --no-gate %s・報告の器が門の記録の SHA を照らす %s・集計器の相手の重複の番人 %s' % (nogate, bind, dup)


def c404():
    wire = 'steer_B.main_position(' in RS
    st = 'main_position(' in re.search(r'def _selftest[\s\S]*', S('steer_B.py')).group(0)
    ok = wire and st
    return (OK_W if ok else NG), '走行器が呼ぶ %s・介入の器の自己検査が検べる %s' % (wire, st)


def c405():
    ok = '21.5 pt を出す' not in S('design_facts_B.py')
    return (OK_T if ok else NG), '生成器の古い数 %s' % ('無い' if ok else 'ある')


def c406():
    fields = json.dumps(T.get('trial_record_fields', {}), ensure_ascii=False)
    ok = 'batch_rows=' in RS and 'batch_rows' in fields
    return (OK_W if ok else NG), '走行器の書き込み %s・正本の試行の記録の欄 %s' % ('batch_rows=' in RS, 'batch_rows' in fields)


def c409():
    s = re.search(r'def counts_main_strata[\s\S]*?\n(?=def )', S('runs_B.py')).group(0)
    ok = "c['ff'] += bool(r['format_fail'])" not in s
    return (OK_T if ok else NG), '層別の計数の常に零の行 %s' % ('無い' if ok else 'ある')


def c410():
    tpl = '管理図' in TPL
    dry = dry_fired('報告: 管理図の要約')
    ok = tpl and (dry or 0) > 0
    return (OK_B if ok else NG), '雛形の節 %s・合成データから組んだ報告に要約が出た回 %s' % (tpl, dry)


def c412():
    ok = '全次元' in T['descriptive_families']['B_desc_textdiff'].get('null_note_D123', '')
    return (OK_T if ok else NG), '正本の注 %s' % ok


def cX1():
    import citations_B
    importlib.reload(citations_B)
    rows = citations_B.load_rows(REPO)
    v = (rows.get('P384') or {}).get('voters')
    ok = bool(v) and v >= {'C1', 'C2'}
    return (OK_B if ok else NG), '最後の巡の採否表の P384 の出所 %s' % (sorted(v) if v else v)


def cX2():
    t = json.dumps(T.get('disclosure', {}), ensure_ascii=False) + json.dumps(T.get('report_rules', {}), ensure_ascii=False)
    ok = '独立の目を通っていない' in t and '独立の目を通っていない' in DR and '独立の目を通っていない' in TPL
    return (OK_T if ok else NG), '正本 %s・草案13B %s・雛形 %s' % ('独立の目を通っていない' in t, '独立の目を通っていない' in DR, '独立の目を通っていない' in TPL)


def cX3():
    sec = '### 5-9' in DR and 'a959f6d1-3dbc-4eb5-b553-006c6a1dd2f8' in DR
    tail = DR.split('### 5-補')[-1][:1500] if DR else ''
    pend_ok = ('Osec-Ncold を足すか' not in tail) and ('絶対値のままにするか' not in tail)
    ok = bool(DR) and sec and pend_ok
    return (OK_T if ok else NG), '草案13B %s・§5-9 と逐語の uuid %s・§5-補 から決まった二件が消えた %s' % ('あり' if DR else '無し', sec, pend_ok)


for P, D, what, fn in [('P384', 'D133', 'td の特異性の規則', c384), ('P385', 'D134', 'S4 の三分岐の前の門', c385),
                       ('P386', 'D135', 'S4 の札と封印の照合', c386), ('P387', 'D136', 'S4 の効き目・札の文言・相対の大きさ', c387),
                       ('P391', 'D137', '品質床の下限の手当てと多重性の数', c391), ('P392', 'D138', '品質床の前置き', c392),
                       ('P395', 'D139', 'D132 の読みの参照の行', c395), ('P398', 'D140', 'ランダム方向の割り当てを交互に', c398),
                       ('P400', 'D141', '‖v̂‖/‖h‖ の帰結', c400), ('P402', 'D142', 'top_k の決め方', c402),
                       ('P411', 'D143', '同一性選別に Osec-Ncold', c411),
                       ('P389', 'D118・D127', '転記行 D・E と正本の旧い鍵', c389), ('P390', 'D98・D119・D127', '草案の古い文', c390),
                       ('P393', '—', '層の割合と添字の対応', c393), ('P394', '—', '副位置の加えた量', c394),
                       ('P396', '—', '決定性 (ii) のバッチの組成', c396), ('P397', '—', '自己検査の締めの行', c397),
                       ('P399', '—', '等質性の注の帰無の率', c399), ('P401', 'D94・D125', '様式門の札', c401),
                       ('P403', 'D126・D130', '検査用の口と報告の照合と相手の重複', c403), ('P404', '—', '起点の一つの関数', c404),
                       ('P405', '—', '生成器の古い数', c405), ('P406', '—', 'バッチの行数', c406), ('P409', '—', '層別の計数の死んだ行', c409),
                       ('P410', 'D110', '報告の管理図の要約', c410), ('P412', '—', 'D123 の理由の注', c412),
                       ('X1', '—', '照合の器が最後の巡の採否表を読む', cX1), ('X2', 'D131', '最後の巡の後の直しの限界', cX2),
                       ('X3', 'D133〜D143', '草案13B と裁定の逐語', cX3)]:
    check(P, D, what, fn)

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
cnt = {}
for r in ROWS:
    cnt[r['status']] = cnt.get(r['status'], 0) + 1
flag = [r['P'] for r in ROWS if a.label == 'before' and r['status'] != NG]
L = ['# 段階 B 最後の系統外の巡の直しの監査（**%s**・%s 日本時間）' % ('直す前' if a.label == 'before' else '直した後', jst.strftime('%Y-%m-%d %H:%M')), '',
     '- 器: `verify_fixes_B_final.py`（枠は `preregistration-fix-audit-B-final.md`・**器を書く前に登録した**）。',
     '- 正本 SHA16 %s。合成データを門と集計器に通した回: %s。' % (runs_B.sha16_file(os.path.join(REPO, 'design', 'contrasts-B.json')), '通った' if AJ else ('通らなかった（%s）' % PIPE_ERR)),
     '- 数: %s（全 %d 行）。' % ('・'.join('%s %d' % kv for kv in cnt.items()), len(ROWS))]
if a.label == 'before':
    L.append('- **直す前に「直っていない」と出なかった検査（働いていない印）**: %s。' % ('無し' if not flag else '・'.join(flag)))
L.append('- 直す前の走行の後に改めた検査（基準は変えていない）: P392（「前置きを付ける」の語が旧い条にも含まれていたので、裁定 D138 の条に固有の語で見る形にした）。'
         '合成データの経路の読み方 `dry_fired`（P385・P410 が使う）——経路の表の第二列を数と読んでおり、表の形（発火した場合の名の並び）と合わず常に None を返していた。表の形どおりに読む形にした（直した後の走行の前・2026-09-19）。')
L += ['', '| P | 裁定 | 何を | 判定 | 証拠 |', '|---|---|---|---|---|']
for r in ROWS:
    L.append('| %s | %s | %s | %s | %s |' % (r['P'], r['D'], r['what'], r['status'], r['evidence'].replace('|', '／')))
L += ['', '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
json.dump({'label': a.label, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'rows': ROWS, 'counts': cnt, 'not_working_before': flag},
          open(OUT.replace('.md', '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('[verify_fixes_B_final] %s: %s（働いていない印 %s）' % (a.label, cnt, flag))
