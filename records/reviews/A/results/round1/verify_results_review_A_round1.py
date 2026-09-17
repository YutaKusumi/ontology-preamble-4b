# -*- coding: utf-8 -*-
"""verify_results_review_A_round1.py v1（2026-09-17・コーディネータ）—— 結果報告 草案3 の公開前検分（第一巡・四票）の所見を、一次記録で出し直す器。
凍結物ではない（本巡のために書いた・凍結の器は読み込むだけで変えない）。事前登録 `preregistration-reproduction-results-A-round1.md` の W124〜W153 に対応する。
出力: 同じ置き場の verification-results-A-round1.{md,json}（既存は --force なしでは上書きしない）。
W130 は、凍結の集計器 `tools/analyze_A.py` を別の工程で読み込み、`confirm_A.label_family` の呼び出しを外から記録して感度閾値の対比ごとの札と傾きを取り出す
（器のファイルは変えない・到達の模擬の手前で止める・集計の出力は書かせない）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, re, json, hashlib, subprocess, datetime, time, argparse, tempfile
from collections import Counter, OrderedDict

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(REPO, 'tools')
VERSION = 'v1.1'   # v1.1（2026-09-17・一回目の走行の後）: W151 の行の選び方を §6 に限る・W134 で照合の記録の JSON の行も数える
MB_BEGIN, MB_END = '<!-- 機械:始 -->', '<!-- 機械:終 -->'
SC_RE = r'(?<![A-Za-z0-9])(N1|N2|S1|S4|SK)(?![A-Za-z0-9])'


def rd(rel):
    return open(os.path.join(REPO, rel), encoding='utf-8').read().replace('\r\n', '\n')


def lines(rel):
    return rd(rel).split('\n')


def s16(rel):
    return hashlib.sha256(open(os.path.join(REPO, rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


def jl(rel):
    return json.loads(rd(rel))


# ---------------------------------------------------------------- W130 の別工程（感度閾値の札を取り出す）
def sens_runner(out_path):
    import runpy
    sys.path.insert(0, TOOLS)
    import confirm_A
    cap = []
    orig = confirm_A.label_family

    def wrap(R, results, flags=None, **kw):
        out = orig(R, results, flags, **kw)
        cap.append({'low': float(R.low), 'high': float(R.high),
                    'rows': [{'label': o['label'], 'slope_pt': o.get('slope_pt'), 'status': r.get('status'),
                              'keep': [bool(x) for x in r.get('keep', [])] if r.get('keep') is not None else None} for o, r in zip(out, results)]})
        return out

    class Stop(Exception):
        pass

    def stop(*a, **k):
        raise Stop()

    confirm_A.label_family = wrap
    confirm_A.measurable_effect_types = stop
    scratch = tempfile.mkdtemp(prefix='verify_sens_')
    sys.argv = ['analyze_A.py', '--tag', 'stageA', '--gate', os.path.join(REPO, 'records', 'A', 'gate-pilotA.json'),
                '--identity', os.path.join(REPO, 'records', 'A', 'main', 'identity-screen-A-regen-2026-09-17.json'),
                '--calib', os.path.join(REPO, 'records', 'A', 'calib-stageA-calib.json'),
                '--style', os.path.join(REPO, 'records', 'A', 'style-stageA.json'),
                '--out', os.path.join(scratch, 'analysis-never-written')]
    stopped = False
    try:
        runpy.run_path(os.path.join(TOOLS, 'analyze_A.py'), run_name='__main__')
    except Stop:
        stopped = True
    wrote = os.listdir(scratch)
    json.dump({'captures': cap, 'stopped_before_measurable': stopped, 'scratch_files': wrote}, open(out_path, 'w', encoding='utf-8'), ensure_ascii=False)


# ---------------------------------------------------------------- 本体
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--sens-runner', default=None)
    a = ap.parse_args()
    if a.sens_runner:
        sens_runner(a.sens_runner)
        return
    out_md = os.path.join(HERE, 'verification-results-A-round1.md'); out_js = os.path.join(HERE, 'verification-results-A-round1.json')
    if (os.path.exists(out_md) or os.path.exists(out_js)) and not a.force:
        sys.exit('出力が既にある（上書きしない・--force で置き換え）')
    t0 = time.time()
    git = lambda *args: subprocess.run(['git', '-C', REPO] + list(args), capture_output=True, text=True, encoding='utf-8').stdout
    status_before = git('status', '--porcelain', '--untracked-files=no')
    head = git('rev-parse', 'HEAD').strip()

    D3P = 'records/A/results-report-A-draft3-2026-09-17.md'
    D3 = lines(D3P)
    L = lambda i: D3[i - 1]
    blocks = []; st = None
    for i, l in enumerate(D3, 1):
        if l == MB_BEGIN:
            st = i
        elif l == MB_END:
            blocks.append((st, i)); st = None
    in_block = lambda i: any(s < i < e for s, e in blocks)
    AN = jl('records/A/analysis-stageA.json'); T = jl('design/contrasts-A.json'); SIZES = T['sizes']
    C = {c['id']: c for c in AN['contrasts']}; LB = T['families']['A_slope']['confirm_rule']['labels']
    AM = lines('records/A/analysis-stageA.md'); FZ = lines('design/design-stageA-FROZEN.md'); TPL = lines('records/A/results-report-template-A.md')
    STY = jl('records/A/style-stageA.json'); GUARD = jl('records/A/main/report-lint-guard-draft3-2026-09-17.json')
    DEV = lines('records/DEVIATIONS.md'); PCM = lines('records/A/predictions-check-A.md'); MR = lines('records/A/main/main-run-A.md')
    API = lines('records/A/main/api-rerun-run-A.md'); AGG = lines('records/A/main/aggregation-plan-A.md'); PB = lines('records/A/main/pressure-breakdown-A.md')
    SI = lines('records/A/sampling-inspection-A-stageA.md'); BUILD = lines('tools/build_report_A.py'); ANPY = lines('tools/analyze_A.py'); LINT = rd('tools/report_lint.py')
    PS = T['print_strings']
    R = []

    def rec(w, finding, checked, verdict, detail):
        R.append(OrderedDict(w=w, finding=finding, checked=checked, verdict=verdict, detail=detail))

    def find(Ls, pred):
        return [i for i, l in enumerate(Ls, 1) if pred(l)]

    def rate(k, n):
        return None if not n else round(k / n, 3)

    def cell(s, sc, arm):
        return STY['cells'][s][sc][arm]

    # ---- W124
    d = OrderedDict()
    d['L5_D33_D40'] = 'D-33〜D-40' in L(5); d['L5_D41'] = 'D-41' in L(5)
    i8 = find(D3, lambda l: l.startswith('- 逸脱台帳（`records/DEVIATIONS.md`）'))
    d['sec8_lines'] = i8; d['sec8_D34_D40'] = bool(i8) and 'D-34〜D-40' in L(i8[0]); d['sec8_D41'] = bool(i8) and 'D-41' in L(i8[0])
    d['draft_D41_anywhere'] = find(D3, lambda l: 'D-41' in l)
    d['ledger_D41_row'] = find(DEV, lambda l: l.startswith('| D-41 |'))
    ok = d['L5_D33_D40'] and not d['L5_D41'] and d['sec8_D34_D40'] and not d['sec8_D41'] and not d['draft_D41_anywhere'] and bool(d['ledger_D41_row'])
    rec('W124', 'D-41 が冒頭の一覧と §8 に無い（Ge1・Ge2・Cl1・Cl2）', '草案3 の 5 行と §8 の台帳の行の文字列・草案3 全文の D-41・台帳の D-41 の行', '再現' if ok else '再現しない', d)

    # ---- W125
    d = OrderedDict()
    rows = [(i, l) for i, l in enumerate(D3, 1) if '散文層（副次終点・札を変えない）' in l]
    d['draft_rows'] = len(rows); d['draft_row_lines'] = [rows[0][0], rows[-1][0]] if rows else None
    d['draft_rows_all_in_block'] = all(in_block(i) for i, _ in rows)
    d['draft_rows_with_scenario_name'] = sum(1 for _, l in rows if re.search(SC_RE, l))
    k = AM.index('## 散文層の副次終点（札を変えない）'); sec = []; j = k + 2
    while j < len(AM) and AM[j].startswith('- '):
        sec.append((j + 1, AM[j])); j += 1
    idrows = [(i, l) for i, l in sec if re.match(r'^- (N1|N2|S1|S4|SK):', l)]
    d['analysis_md_rows'] = len(sec); d['analysis_md_row_lines'] = [sec[0][0], sec[-1][0]]; d['analysis_md_rows_with_id'] = len(idrows)
    d['analysis_md_id_rows'] = [l[2:] for _, l in idrows]
    d['id_rows_in_draft'] = [l for _, l in idrows if any(l[2:] in x for x in D3)]
    okrows = [x for x in AN['stratified'] if x.get('string')]
    d['json_stratified'] = len(AN['stratified']); d['json_stratified_ok'] = len(okrows)
    d['json_stratified_status'] = dict(Counter(x['status'] for x in AN['stratified']))
    d['canon_stratified_note'] = PS['stratified_note']; d['canon_note_has_scenario'] = ('{sc}' in PS['stratified_note'])
    d['builder_keeps_only_string_rows'] = find(BUILD, lambda l: "s['string'] for s in AN['stratified'] if s.get('string')" in l)
    same_order = [l for _, l in rows] == [x['string'] for x in okrows]
    d['draft_rows_equal_json_strings_in_order'] = same_order
    mapping = [{'line': i, 'id': x['id'], 'beta': round(x['beta'], 3), 'sizes': x['sizes']} for (i, _), x in zip(rows, okrows)] if same_order else []
    d['mapping'] = mapping
    d['mapping_per_scenario'] = dict(Counter(m['id'].split(':')[0] for m in mapping))
    cl = {**{i: 'N1' for i in range(220, 227)}, **{i: 'S1' for i in range(227, 231)}, **{i: 'S4' for i in range(231, 234)}, **{i: 'SK' for i in range(234, 238)}}
    d['cl1_cl2_mapping_matches'] = bool(mapping) and all(cl.get(m['line']) == m['id'].split(':')[0] for m in mapping) and len(mapping) == len(cl)
    d['line229'] = next((m for m in mapping if m['line'] == 229), None); d['line236'] = next((m for m in mapping if m['line'] == 236), None)
    d['S4_Onull_N_style'] = C['S4:Onull~N']['style']; d['canon_stratified_applies_to'] = T['style_gate']['stratified']['applies_to']
    d['S4_Onull_N_in_json_stratified'] = any(x['id'] == 'S4:Onull~N' for x in AN['stratified'])
    sg = [l for l in D3 if re.match(r'^(N1|N2|S1|S4|SK):\S+: 様式門 (hold|note)$', l)]
    d['draft_style_gate_rows'] = len(sg); d['draft_style_gate_rows_per_scenario'] = dict(Counter(l.split(':')[0] for l in sg))
    d['ge2_excerpt_undecidable_row_in_analysis_md'] = any(l == '- N2:Odose1~Onull: undecidable（残った規模 32B）' for _, l in sec)
    d['ge2_excerpt_undecidable_row_in_draft'] = bool(find(D3, lambda l: 'N2:Odose1~Onull: undecidable' in l))
    ok = (d['draft_rows'] == 18 and d['draft_rows_with_scenario_name'] == 0 and not d['canon_note_has_scenario'] and d['builder_keeps_only_string_rows']
          and d['cl1_cl2_mapping_matches'] and d['S4_Onull_N_style'] == 'none' and not d['S4_Onull_N_in_json_stratified'])
    rec('W125', '散文層の副次終点の行に場面の名が無い（Ge1・Ge2・Cl1・Cl2）', '草案3 の区画の行・機械集計の md と JSON の散文層・正本の置き字・組み立て器の行・行と場面の対応（JSON の id と文字列の順の一致）・Ge2 の行の数と抜粋',
        '再現（Ge2 の「28 行」は様式門の行と機械集計の行の数で、草案3 の区画は 18 行。Ge2 が区画の抜粋とした判定不能の行は草案3 に無い）' if ok else '一部再現', d)

    # ---- W126
    d = OrderedDict()
    c = C['S1:Lneg~Onull']; r = c['result']; keep = r['keep']
    d['row_line'] = find(D3, lambda l: l.startswith('| S1:Lneg~Onull |'))
    d.update(label=c['label'], beta=round(r['beta'], 3), p_beta=float('%.3g' % r['p_beta']), beta_rank=c['beta_holm']['rank'], slope_pt=round(c['slope_pt'], 2), p_pt=float('%.3g' % r['p_pt']),
             clause=r['clause'], sat_A=r['sat_A'], sat_B=r['sat_B'], style=c['style'], refuse_gate_applied=c['refuse_gate'] is not None)
    kept = [SIZES[i] for i in range(len(SIZES)) if keep[i]]
    d['kept'] = kept
    d['Lneg_at_kept'] = ['%d/%d' % (c['counts']['kA'][i], c['counts']['nA'][i]) for i in range(len(SIZES)) if keep[i]]
    hi = T['censor']['high']
    d['Lneg_above_censor_high_at_all_kept'] = all(c['counts']['kA'][i] / c['counts']['nA'][i] > hi for i in range(len(SIZES)) if keep[i])
    d['style_cells'] = [(x['kind'], SIZES[x['size_index']], x['diff_pt']) for x in (c['style_detail'] or {}).get('cells', [])]
    pm = {p['id']: p for p in AN['measurable']['per_contrast']}
    pp = pm['S1:Lneg~Onull']['directions']
    d['reach'] = {k2: {'p': round(v.get('p_card_D1_first'), 3) if v.get('p_card_D1_first') is not None else None,
                       'clause_rate': (round(v['clause_rate_among_fit'], 3) if v.get('clause_rate_among_fit') is not None else None)} for k2, v in pp.items()}
    d['measured_contrasts'] = [p['id'] for p in AN['measurable']['per_contrast'] if p.get('measured_contrast')]
    d['ns_reading_line'] = find(D3, lambda l: '検出域の外でありうる' in l)
    c4 = C['S4:Lneg~Onull']; r4 = c4['result']
    d['S4_Lneg'] = dict(label=c4['label'], clause=r4['clause'], sat_A=r4['sat_A'], style=c4['style'], slope_pt=round(c4['slope_pt'], 2), p_pt=float('%.3g' % r4['p_pt']),
                        Lneg_at_kept=['%d/%d' % (c4['counts']['kA'][i], c4['counts']['nA'][i]) for i in range(len(SIZES)) if r4['keep'][i]])
    rs_text = T['reading_selection']['text']
    d['reading_selection_text'] = rs_text
    d['reading_selection_mentions_clause'] = '解釈条項' in rs_text
    fz27 = FZ[26]
    d['frozen_27_selection_rule_sentence'] = fz27[:fz27.find('**測れた効果種**')]
    d['frozen_27_rule_mentions_clause'] = '解釈条項' in d['frozen_27_selection_rule_sentence']
    eff = {p['id']: p['effect'] for p in AN['measurable']['per_contrast']}
    meas_types = [e for e, v in AN['measurable']['types'].items() if v['measurable']]
    three = [x for x in AN['contrasts'] if eff[x['id']] in meas_types and x['label'] == LB['clause']]
    d['clause_contrasts_in_measurable_types'] = [dict(id=x['id'], beta_rejected=x['beta_holm']['rejected'], star_rejected=x['star_holm']['rejected'], sat=(x['result']['sat_A'], x['result']['sat_B'])) for x in three]
    d['L86'] = L(86)
    ok = (d['label'] == LB['ns'] and d['clause'] and d['style'] == 'hold' and d['Lneg_above_censor_high_at_all_kept'] and all(v['clause_rate'] == 0.0 for v in d['reach'].values())
          and d['measured_contrasts'] == ['S1:Lneg~Onull'] and not d['reading_selection_mentions_clause'] and not d['frozen_27_rule_mentions_clause']
          and sorted(x['id'] for x in three) == ['S1:Onull-Ncold~Onull', 'S4:Onull-Ncold~Onull', 'SK:Lneg~Onull'] and all(x['beta_holm']['rejected'] and x['star_holm']['rejected'] for x in three))
    rec('W126', 'S1 の Lneg 対 Onull の読みを左右する事実が §1 に無い・解釈条項に回った三対比の数え方に定めが無い（Cl1・Cl2）', '並記表の行・破局/n・様式の差・到達の模擬・非有意の読み文・正本 reading_selection と凍結 §1 の文言・三対比の札と二つの Holm',
        '再現' if ok else '一部再現', d)

    # ---- W127
    d = OrderedDict()
    hold = [x for x in AN['contrasts'] if x['style'] == 'hold']
    d['hold_total'] = len(hold); d['hold_by_label'] = dict(Counter(x['label'] for x in hold))
    d['hold_ns_ids'] = [x['id'] for x in hold if x['label'] == LB['ns']]
    d['hold_clause_ids'] = [x['id'] for x in hold if x['label'] == LB['clause']]
    d['note_total'] = sum(1 for x in AN['contrasts'] if x['style'] == 'note')
    d['frozen_clause_ii'] = next(l for l in FZ if l.startswith('- (ii)'))
    d['L47'] = L(47)
    ok = d['hold_total'] == 25 and d['hold_by_label'].get(LB['style']) == 9 and d['hold_by_label'].get(LB['clause']) == 9 and d['hold_by_label'].get(LB['ns']) == 7 and '分離できない場合' in d['frozen_clause_ii']
    rec('W127', '(ii) の一行が様式転位の 9 本に限られ、様式門 hold の旗は 25 本にある（Cl1・Cl2）', '機械集計の JSON の様式門の状態を札ごとに数える・凍結 §3 (ii) の文言・草案3 の 47 行', '再現' if ok else '一部再現', d)

    # ---- W128
    d = OrderedDict()
    d['L48_has_drafter_threshold_note'] = '起草者が置いた目安' in L(48)
    d['L48_says_after_seeing_rates'] = bool(re.search(r'見た後|読んだ後|率を見て', L(48)))
    mention = {}
    for s in ('4B', '14B', '32B'):
        for arm in ('N', 'Onull'):
            cc = cell(s, 'S4', arm); mention['%s|%s' % (s, arm)] = rate(cc['c2_final'], cc['n_ok'])
    d['S4_mention_rates'] = mention
    listed = re.findall(r'(\d+(?:\.\d+)?B(?:-2507)?) の (N1|N2|S1|S4|SK)（([^）]*)）', L(48).split('）: ', 1)[-1])
    d['L48_model_order'] = [m for m, _, _ in listed]
    d['L48_order_is_string_sort'] = d['L48_model_order'] == sorted(d['L48_model_order'])
    size_key = SIZES + ['4B-2507']
    d['L48_order_is_size_order'] = d['L48_model_order'] == sorted(d['L48_model_order'], key=size_key.index)
    half = set()
    for s, v in STY['cells'].items():
        for sc, vv in v.items():
            for arm, cc in vv.items():
                if cc['n_ok'] and cc['c2_final'] / cc['n_ok'] >= 0.5:
                    half.add((s, sc, arm))
    lset = {(m, sc, arm.strip()) for m, sc, arms in listed for arm in arms.split('・')}
    d['cells_ge_half'] = len(half); d['L48_equals_cells_ge_half'] = half == lset
    ok = d['L48_has_drafter_threshold_note'] and not d['L48_says_after_seeing_rates'] and d['L48_equals_cells_ge_half']
    rec('W128', '(vii) の「半分」は率を見た後の目安で、その旨が無い・確証の一本の言及率の並び（Cl1・Cl2）', '草案3 の 48 行の文言と並び・様式の記録の c2 の率（S4 の N と Onull）・半分以上のセルの集合', '再現' if ok else '一部再現', d)

    # ---- W129
    d = OrderedDict()
    c = C['S4:Onull~N']; r = c['result']; keep = r['keep']
    per = []
    for i, s in enumerate(SIZES):
        per.append(dict(size=s, kept=keep[i], censored=r['censored'][i], unmeasurable=c['excluded_unmeasurable'][i],
                        Onull='%d/%d' % (c['counts']['kA'][i], c['counts']['nA'][i]), N='%d/%d' % (c['counts']['kB'][i], c['counts']['nB'][i]),
                        b_Onull=rate(cell(s, 'S4', 'Onull')['b_final'], cell(s, 'S4', 'Onull')['n_ok']), b_N=rate(cell(s, 'S4', 'N')['b_final'], cell(s, 'S4', 'N')['n_ok']),
                        env=AN['size_env'].get('%s|S4' % s)))
    d['per_size'] = per
    d['a_b_zero_at_kept'] = all(p['b_Onull'] == 0 and p['b_N'] == 0 for p in per if p['kept'])
    d['b_one_at_excluded'] = all(p['b_Onull'] == 1 and p['b_N'] == 1 for p in per if not p['kept'])
    d['critical_size'] = c['critical_size']
    d['bridge_scenario'] = T['bridge']['scenario']
    br = AN['descriptive']['A_desc_env']['bridge']
    d['bridge_max_abs_diff_pt'] = max(abs(x['diff_pt']) for x in br if x['diff_pt'] is not None)
    d['frozen_2_6_has_OnullN_print'] = '確証札の段落に様式差と順位を機械印字・層別副次' in FZ[65]
    d['canon_label_confirmed'] = PS['label_confirmed']; d['label_confirmed_has_style_placeholder'] = bool(re.search(r'\{(style|rank|b_|a_)', PS['label_confirmed']))
    d['S4_Onull_N_in_sensitivity_changed'] = [s_['low'] for s_ in AN['sensitivity'] if any(x['id'] == 'S4:Onull~N' for x in s_['changed'])]
    d['recipe'] = {x['id']: x['diff_pt'] for x in AN['descriptive']['A_desc_recipe'] if x['id'] in ('S4:N~recipe', 'S4:Onull~recipe')}
    d['recipe_lines'] = find(D3, lambda l: l.startswith('S4:N~recipe') or l.startswith('S4:Onull~recipe'))
    d['L658'] = L(658)
    ok = (d['a_b_zero_at_kept'] and d['b_one_at_excluded'] and d['critical_size']['size'] == '14B' and d['bridge_scenario'] == 'N1' and d['frozen_2_6_has_OnullN_print']
          and not d['label_confirmed_has_style_placeholder'] and not d['S4_Onull_N_in_sensitivity_changed'])
    rec('W129', '確証の一本の段落に、読みの範囲を決める事実が欠ける（Cl1・Cl2 (a)〜(e)）', '規模ごとの残存・検閲・測定不能・破局/n・(b)・環境・臨界規模・橋の場面と最大差・凍結 §2.6 と正本の定型・感度閾値の変更の一覧・レシピ対',
        '再現（(d) は凍結本文と正本・組み立て器の食い違い）' if ok else '一部再現', d)

    # ---- W130（別工程）
    d = OrderedDict()
    tmp = os.path.join(tempfile.gettempdir(), 'verify_sens_capture_%d.json' % os.getpid())
    t1 = time.time()
    pr = subprocess.run([sys.executable, os.path.abspath(__file__), '--sens-runner', tmp], capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    d['runner_rc'] = pr.returncode; d['runner_seconds'] = round(time.time() - t1, 1); d['runner_stderr_tail'] = pr.stderr[-600:]
    if pr.returncode == 0 and os.path.exists(tmp):
        cap = json.load(open(tmp, encoding='utf-8')); os.remove(tmp)
        caps = cap['captures']; d['captures'] = len(caps); d['stopped_before_measurable'] = cap['stopped_before_measurable']; d['scratch_files'] = cap['scratch_files']
        ids = [x['id'] for x in T['families']['A_slope']['contrasts']]
        main_c = caps[0]
        d['main_labels_match_json'] = all(main_c['rows'][i]['label'] == C[ids[i]]['label'] for i in range(len(ids)))
        passes = []
        for cp in caps[1:]:
            sref = next(s_ for s_ in AN['sensitivity'] if abs(s_['low'] - cp['low']) < 1e-9)
            cnt = Counter(rw['label'] for rw in cp['rows'])
            counts_match = all(cnt.get(LB[k2], 0) == v for k2, v in sref['counts'].items())
            changed = sorted(ids[i] for i in range(len(ids)) if cp['rows'][i]['label'] != C[ids[i]]['label'])
            conf = []
            for i, rw in enumerate(cp['rows']):
                if rw['label'] != LB['confirmed']:
                    continue
                cc = C[ids[i]]['counts']; kidx = [j2 for j2, kk in enumerate(rw['keep']) if kk]; j = max(kidx)
                up = (rw['slope_pt'] or 0) > 0 and cc['nA'][j] and cc['nB'][j] and cc['kA'][j] * cc['nB'][j] > cc['kB'][j] * cc['nA'][j]
                conf.append(dict(id=ids[i], slope_pt=round(rw['slope_pt'], 2), kept=[SIZES[x] for x in kidx], largest=SIZES[j],
                                 A_at_largest='%d/%d' % (cc['kA'][j], cc['nA'][j]), B_at_largest='%d/%d' % (cc['kB'][j], cc['nB'][j]), upward_rule=bool(up)))
            passes.append(dict(low=cp['low'], high=cp['high'], counts_match_json=counts_match, changed_match_json=changed == sorted(x['id'] for x in sref['changed']),
                               confirmed=conf, upward=[x['id'] for x in conf if x['upward_rule']]))
        d['passes'] = passes
        d['machine_prints_upward_only_for_main'] = bool(find(ANPY, lambda l: l.startswith('UPWARD = []'))) and not any('upward' in l.lower() for l in ANPY[287:297])
        ups = {p['low']: p['upward'] for p in passes}
        ok = d['main_labels_match_json'] and all(p['counts_match_json'] and p['changed_match_json'] for p in passes) and sorted(ups.get(0.03, [])) == ['N2:Onull~N', 'S1:Onull-Ncold~Onull']
        verdict = '再現' if ok else ('一部再現' if d['main_labels_match_json'] else '検査不能')
    else:
        verdict = '検査不能'
    rec('W130', '「上向きの確証はなかった」は主閾値の文で、感度閾値の下では上向きの規則に当たる確証がある（Cl2）', '凍結の集計器を別の工程で読み込み、label_family の呼び出しを外から記録（主閾値の札が JSON と一致・感度閾値の件数と変わった対比が JSON と一致することを確かめてから、上向きの規則を当てる）',
        verdict, d)

    # ---- W131
    d = OrderedDict()
    d['draft_lines'] = find(D3, lambda l: '判定器の妥当性の範囲の外' in l)
    d['frozen_xv'] = next(l for l in FZ if l.startswith('- (xv)'))
    d['frozen_2_11_all_models'] = '範囲は全機種' in FZ[87]; d['frozen_2_11_pilot_fragments'] = 'パイロットの標本から機械抽出した断片' in FZ[87]
    jrows = [l for l in D3 if re.match(r'^\| (0\.6B|1\.7B|4B|8B|14B|32B|4B-2507)\|(N1|N2|S1|S4|SK) \|', l)]
    cells_cov = {l.split(' |')[0][2:] for l in jrows}
    d['judge_rows'] = len(jrows); d['judge_cells_covered'] = len(cells_cov)
    d['cells_with_unmeasurable_direction_rate'] = sorted({l.split(' |')[0][2:] + ('（機械が破局とした対が無い）' if re.search(r'\| —（0） \| [0-9.]+（', l) else '（機械が非破局とした対が無い）') for l in jrows if '—（0）' in l})
    sec3 = D3[find(D3, lambda l: l.startswith('### 判定器の妥当性'))[0] - 1:find(D3, lambda l: l.startswith('## 4. '))[0]]
    d['draft_judge_section_mentions_pilot'] = any('パイロット' in l for l in sec3)
    ok = bool(d['draft_lines']) and d['frozen_2_11_all_models'] and d['judge_cells_covered'] == 35 and bool(d['cells_with_unmeasurable_direction_rate']) and not d['draft_judge_section_mentions_pilot']
    rec('W131', '§9 の「判定器の妥当性の範囲の外の機種と場面」は実物と合わない（Cl1）', '草案3 の該当の行・凍結 §3 (xv) と §2.11・判定器の表の覆い・方向別の率が無いセル・判定器の節のパイロットの記載', '再現' if ok else '一部再現', d)

    # ---- W132
    d = OrderedDict()
    d['template_L5_rule'] = '報告は、走査器が違反も埋め残しも無しに終わることを確かめてから公開する' in TPL[4]
    d['guard_violations'] = GUARD['violations']; d['guard_expected'] = GUARD['expected']
    d['guard_string_with_result_value'] = [x for x in GUARD['expected'] if re.search(r'-?\d+\.\d+〜', x)]
    d['analysis_undecidable_prose_rows_absent_from_draft'] = len([l for _, l in idrows]) and not any(any(l[2:] in x for x in D3) for _, l in idrows)
    bt0 = AM.index(next(l for l in AM if l.startswith('| 対比 | A 破局/n'))); am_tab = [l for l in AM[bt0:bt0 + 40] if l.startswith('| ') and ':' in l.split('|')[1]]
    d['analysis_md_refuse_applied_text'] = sum(1 for l in am_tab if '| 当てた・保留なし |' in l)
    dt = [l for l in D3 if re.match(r'^\| (N1|N2|S1|S4|SK):\S+ \| 残った規模', l)]
    d['draft_table_refuse_text'] = sum(1 for l in dt if '| 保留なし |' in l)
    d['builder_refuse_text_line'] = find(BUILD, lambda l: "'保留なし') if x['refuse_gate'] else '—'" in l)
    d['draft_mentions_guard'] = find(D3, lambda l: '歯止め' in l)
    ok = d['template_L5_rule'] and d['guard_violations'] == 6 and len(d['guard_string_with_result_value']) == 1 and d['analysis_undecidable_prose_rows_absent_from_draft'] and d['analysis_md_refuse_applied_text'] == d['draft_table_refuse_text'] > 0 and not d['draft_mentions_guard']
    rec('W132', '歯止め（D-41）の見ない範囲・雛形の「違反 0 で公開」と実際・登録した文字列の一つが結果の値（Cl1・Cl2）', '雛形の 5 行・歯止めの記録・散文層の判定不能の行・refuse 門の列の文言（機械集計の md と草案3）・草案3 の「歯止め」の記載', '再現' if ok else '一部再現', d)

    # ---- W133
    d = OrderedDict()
    tn = T['report_rules']['typed_numbers']; d['canon_typed_numbers'] = tn
    d['canon_has_time'] = '時刻' in tn; d['canon_has_commit'] = 'コミット' in tn
    d['draft_L5_has_time_and_commit'] = ('時刻' in L(5)) and ('コミット' in L(5))
    outside = [(i, l) for i, l in enumerate(D3, 1) if not in_block(i) and l not in (MB_BEGIN, MB_END)]
    d['commit_ids_outside_blocks'] = sorted({(i, m) for i, l in outside for m in re.findall(r'(?<![0-9A-Za-z])(?=[0-9a-f]*[a-f])[0-9a-f]{7}(?![0-9A-Za-z])', l)})
    d['times_outside_blocks'] = sorted({(i, m) for i, l in outside for m in re.findall(r'\d{2}:\d{2} UTC', l)})
    NLT = rd('tools/numbers_lint.py')
    d['lint_uses_numbers_lint_masks'] = 'import numbers_lint as NL' in LINT
    d['lint_masks_time'] = r"r'\b\d{1,2}:\d{2}\b'" in NLT; d['lint_masks_commit'] = r"r'\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b'" in NLT
    ok = (not d['canon_has_time'] and not d['canon_has_commit'] and d['draft_L5_has_time_and_commit'] and bool(d['commit_ids_outside_blocks']) and bool(d['times_outside_blocks'])
          and d['lint_uses_numbers_lint_masks'] and d['lint_masks_time'] and d['lint_masks_commit'])
    rec('W133', '打ち込んだ数の型（時刻・コミットの短い名）が登録の文言より広い（Cl2）', '正本 typed_numbers・草案3 の 5 行・区画の外のコミットの短い名と時刻・走査器の型', '再現' if ok else '一部再現', d)

    # ---- W134
    d = OrderedDict()
    d['count_0_1_0'] = sum(l.count('（0/1 0）') for l in PCM); d['count_dup_ns'] = sum(l.count('（非有意）（非有意）') for l in PCM)
    tabrows = [l for l in PCM if l.startswith('| 向き |') or l.startswith('| 床持続 |') or l.startswith('| 全体 |')]
    detail_rows = [l for l in tabrows if l.split('|')[2].strip().startswith('a.')]
    d['detail_rows_by_result'] = dict(Counter(l.rstrip(' |').split('|')[-1].strip() for l in detail_rows))
    try:
        PCJ = jl('records/A/predictions-check-A.json'); d['json_exists'] = True
        d['json_keys'] = list(PCJ.keys())[:12]
        d['json_detail_rows_by_result'] = {k2: dict(Counter(rw.get('result') for rw in v)) for k2, v in PCJ['detail'].items()}   # v1.1: 的中の行は JSON にある
    except Exception as ex:
        d['json_exists'] = False; d['json_error'] = str(ex)[:120]
    d['L1923'] = L(1923)
    ok = d['count_0_1_0'] > 0 and d['count_dup_ns'] > 0 and '的中' not in d['detail_rows_by_result']
    rec('W134', '予想の照合の記録の書式・的中の行の欠け（Cl1・Cl2）', '照合の記録の md の表の行と書式・JSON の行・草案3 の 1923 行',
        '再現（的中の行は md の表に無く、JSON にはある）' if ok and d.get('json_detail_rows_by_result') and all('的中' in v for v in d['json_detail_rows_by_result'].values()) else ('再現' if ok else '一部再現'), d)

    # ---- W135
    d = OrderedDict()
    c = C['S4:Onull~N']; r = c['result']
    d['censored'] = sum(r['censored']); d['unmeasurable'] = sum(c['excluded_unmeasurable']); d['excluded'] = len(SIZES) - sum(r['keep'])
    d['both'] = [SIZES[i] for i in range(len(SIZES)) if r['censored'][i] and c['excluded_unmeasurable'][i]]
    d['all_contrasts_with_overlap'] = [x['id'] for x in AN['contrasts'] if any(x['result']['censored'][i] and x['excluded_unmeasurable'][i] for i in range(len(SIZES)))] if all('censored' in x['result'] for x in AN['contrasts']) else 'n/a'
    ok = d['censored'] + d['unmeasurable'] > d['excluded'] and d['both'] == ['0.6B']
    rec('W135', '「検閲 3・測定不能 1」で 0.6B が二重に数えられる（Cl2）', '確証の一本の残存規模の内訳と、重なった規模・同じ重なりを持つ対比', '再現' if ok else '再現しない', d)

    # ---- W136
    d = OrderedDict()
    fl = [x for x in AN['floor'] if x['arm'] == 'Nk']
    d['Nk_rows'] = [dict(id=x['id'], upper06=x['upper'][0], fail_sizes=x['fail_sizes']) for x in fl]
    d['canon_floor_desc'] = PS['floor_desc']
    d['analyze_line'] = find(ANPY, lambda l: "ubs.append('測定不能'); fails.append(s)" in l)
    ok = all(('0.6B' in x['fail_sizes']) for x in fl if x['upper'][0] == '測定不能') and any(x['upper'][0] == '測定不能' for x in fl)
    rec('W136', '床持続で 0.6B の Nk の測定不能が「棄却域を外れた規模」に入る（Cl1）', '機械集計の床持続の Nk の行・正本の定型・集計器の行', '再現' if ok else '再現しない', d)

    # ---- W137
    d = OrderedDict()
    d['L134'] = L(134); d['L134_mentions_pilot'] = 'パイロット' in L(134)
    G = jl('records/A/gate-pilotA.json'); d['gate_tag'] = G.get('tag')
    g2 = {x['id']: x['kept_n'] for v in G['gate2']['per_scenario'].values() for x in v['contrasts']}
    d['gate_N2_Onull_N_kept_n'] = g2.get('N2:Onull~N'); d['main_N2_Onull_N_kept'] = sum(C['N2:Onull~N']['result']['keep'])
    d['L138_has_Onull_N_4'] = 'Onull~N 4' in L(138)
    ok = not d['L134_mentions_pilot'] and d['gate_N2_Onull_N_kept_n'] == 4 and d['main_N2_Onull_N_kept'] == 2
    rec('W137', '門2 の区画に見出しが無く、並記表の残存規模と違う（Cl1）', '草案3 の 134 行と 138 行・門の記録（パイロット）の残存規模・本走行の残存規模', '再現' if ok else '一部再現', d)

    # ---- W138
    d = OrderedDict()
    d['canon_style_note'] = PS['style_note']; d['hold_pt'] = T['style_gate']['hold_pt']; d['note_pt'] = T['style_gate']['note_pt']
    big = [(i, float(m)) for i, l in enumerate(D3, 1) for m in re.findall(r'様式の差が注の帯を超えた（[ab]・[^・]+・([0-9.]+) pt）', l) if float(m) > T['style_gate']['hold_pt']]
    d['note_strings_above_hold'] = len(big); d['examples'] = [x for x in big if x[0] in (565, 572)]
    ok = '注の帯を超えた' in PS['style_note'] and len(big) > 0
    rec('W138', '保留の大きさにも「注の帯を超えた」と印字される（Cl1）', '正本 style_note・草案3 の定型文の区画で保留の閾値を超える大きさの件', '再現' if ok else '再現しない', d)

    # ---- W139
    d = OrderedDict()
    envl = [l for l in D3[99:103]]
    d['env_block_run_keys'] = [l.split(':')[0] for l in envl]
    sess = {}
    for fn in sorted(os.listdir(os.path.join(REPO, 'results', 'sessions-A'))):
        if fn.startswith('stageA-bridge__'):
            sj = jl('results/sessions-A/' + fn); sess[fn] = dict(run_keys=sj['run_keys'], gpu=sj['gpu'], concurrency=sj['concurrency'])
    d['bridge_sessions'] = sess
    shown = set(d['env_block_run_keys']); allb = {k2 for v in sess.values() for k2 in v['run_keys']}
    d['bridge_keys_not_shown'] = sorted(allb - shown)
    ok = len(d['bridge_keys_not_shown']) == 1 and 'L4' in sess.get('stageA-bridge__8B__s1.json', {}).get('gpu', '')
    rec('W139', '§2 の環境の区画が tag ごとに一走行キーで、橋 8B の L4 側が見えない（Cl1）', '草案3 の 100〜103 行・橋のセッション記録の走行キーと GPU', '再現' if ok else '再現しない', d)

    # ---- W140
    d = OrderedDict()
    b = next((s, e) for s, e in blocks if s == 550)
    ls_ids = [l[2:].split(':')[0] + ':' + l[2:].split(':')[1] for l in D3[b[0]:b[1] - 1] if l.startswith('- ')]
    d['label_block_lines'] = len(ls_ids); d['missing_ids'] = sorted(set(C) - set(ls_ids))
    mi = d['missing_ids']
    d['missing_detail'] = [dict(id=x, label=C[x]['label'], style=C[x]['style'], env=C[x]['env_hold'], strings=list(C[x]['strings'].keys())) for x in mi]
    ok = mi == ['SK:Onull-Ncold~Onull'] and d['label_block_lines'] == 34
    rec('W140', '定型文の区画に SK の Onull-Ncold 対 Onull の行が無い（Cl1）', '草案3 の 551〜584 行の対比・無い対比の札と定型の有無', '再現' if ok else '一部再現', d)

    # ---- W141
    d = OrderedDict(L28=L(28)[:30], L32=L(32)[:30], L75=L(75))
    ok = L(28).startswith('3. ') and L(32).startswith('3. ')
    rec('W141', '§0 の番号「3.」の重複（Cl1）', '草案3 の 28・32・75 行', '再現' if ok else '再現しない', d)

    # ---- W142
    d = OrderedDict()
    d['L119_first_read'] = '初めて読んだ' in L(119)
    d['run_record_sec8_sample_text'] = find(MR, lambda l: '抽出検査の標本の本文の先頭 600 字（選択が含まれる' in l)
    d['L1982'] = L(1982)
    ok = d['L119_first_read'] and bool(d['run_record_sec8_sample_text']) and not ('選択' in L(119))
    rec('W142', '「率は…初めて読んだ」と抽出検査の標本の本文（Cl1）', '草案3 の 119 行・走行記録 §8・草案3 の 1982 行', '再現' if ok else '一部再現', d)

    # ---- W143
    d = OrderedDict()
    d['run_record_bridge4B_same_number'] = find(MR, lambda l: '同じセッション番号（1）のまま' in l and '登録者が承認した' in l)
    d['run_record_session_order'] = find(MR, lambda l: 'セッションの順番を段取りから変えた' in l and '登録者が裁定した' in l)
    devrows = [l for l in DEV if re.match(r'^\| D-(3[4-9]|4[0-9]) \|', l)]
    d['ledger_mentions'] = [l[:8] for l in devrows if ('セッションの順番' in l or '同じセッション番号' in l or 'セッション番号' in l)]
    ok = bool(d['run_record_bridge4B_same_number']) and bool(d['run_record_session_order']) and not d['ledger_mentions']
    rec('W143', 'セッション順の変更と、橋 4B の同じ番号での走らせ直しが台帳に無い（Cl1）', '走行記録 §1 の該当の項・台帳の D-34〜D-41', '再現' if ok else '再現しない', d)

    # ---- W144
    d = OrderedDict(L1790_says_not_compared=bool(re.search(r'比べ', L(1790))), api_record_says=find(API, lambda l: '比べられない' in l))
    ok = not d['L1790_says_not_compared'] and bool(d['api_record_says'])
    rec('W144', '除外した API の記録を手元の走行と比べない旨（Cl1）', '草案3 の 1790 行・API 再走行の記録', '再現' if ok else '再現しない', d)

    # ---- W145
    d = OrderedDict()
    d['pressure_superlatives'] = [(i, [w for w in ('最強', '最も高い') if w in l]) for i, l in enumerate(PB, 1) if ('最強' in l or '最も高い' in l)]
    d['L1868'] = L(1868); d['L1868_says_frozen_table_verbatim'] = '凍結の表の逐語' in L(1868)
    d['pressure_record_says_table_not_in_frozen'] = any('表そのものは本文に置かず' in l for l in PB)
    d['L1870_notes_superlatives'] = bool(re.search(r'最上級|最強|読みに用いない', L(1870)))
    ok = bool(d['pressure_superlatives']) and d['L1868_says_frozen_table_verbatim'] and d['pressure_record_says_table_not_in_frozen'] and not d['L1870_notes_superlatives']
    rec('W145', '圧の内訳の記録の最上級の語と、見出し「凍結の表の逐語」（Cl1・Cl2）', '圧の内訳の記録の本文・草案3 の 1868・1870 行', '再現' if ok else '一部再現', d)

    # ---- W146
    d = OrderedDict()
    tj = json.dumps(T, ensure_ascii=False)
    hits = sorted({m.group(0) for m in re.finditer(r'[^。「」"]{0,40}書式外[^。「」"]{0,60}', tj) if ('非破局' in m.group(0) or '分母' in m.group(0))})
    d['canon_format_fail_rules'] = hits[:8]
    d['draft_sec9_mentions_format_fail_denominator'] = any(('書式外' in l and '分母' in l) for l in D3[1933:1975])
    ok = bool(hits) and not d['draft_sec9_mentions_format_fail_denominator']
    rec('W146', '書式外を全分母で非破局に数える限界が §9 に無い（Cl1）', '正本の書式外の扱いの文言・草案3 §9', '再現' if ok else '一部再現', d)

    # ---- W147
    d = OrderedDict(aggregation_plan=find(AGG, lambda l: 'reasoning_chars' in l and 'が 0' in l), draft_mentions=find(D3, lambda l: 'reasoning_chars' in l))
    ok = bool(d['aggregation_plan']) and not d['draft_mentions']
    rec('W147', '非思考の確かめとして reasoning_chars 0 を指していない（Cl2）', '集計の段取りの記録・草案3 全文', '再現' if ok else '再現しない', d)

    # ---- W148
    d = OrderedDict(L8_sha=re.search(r'門0\.5 の記録（SHA16 ([0-9A-F]{16})）', L(8)).group(1), regen=s16('records/A/main/identity-screen-A-regen-2026-09-17.json'),
                    frozen_record=s16('records/A/identity-screen-A.json'), analysis_input=AN['inputs']['identity'], L133_has_sha=bool(re.search(r'[0-9A-F]{16}', L(133))))
    ok = d['L8_sha'] == d['regen'] == d['analysis_input'] and d['frozen_record'] != d['regen'] and not d['L133_has_sha']
    rec('W148', '冒頭の門0.5 の記録の SHA16 が作り直した記録のもの（Cl2）', '草案3 の 8 行と 133 行・二つの記録の SHA16・集計の入力', '再現' if ok else '再現しない', d)

    # ---- W149
    d = OrderedDict()
    jv = T['judge_validity']
    d['judge_validity_rule'] = str(jv.get('rule'))[:400]; d['judge_validity_report'] = str(jv.get('report'))[:400]
    d['judge_validity_reading_check'] = str(jv.get('reading_check'))[:400]
    d['kappa_values_in_draft'] = sorted({m for l in D3[272:412] for m in re.findall(r'\| (1\.000|0\.\d{3}|—) \| [—0-9.]+（', l)})
    d['draft_position_rows_have_both_agreements'] = all(('破局の一致' in l and '選択の一致' in l) for l in D3[426:430])
    ok = d['kappa_values_in_draft'] == ['1.000', '—']
    rec('W149', '判定器の κ 1.000 の意味の断り（Cl2）', '正本 judge_validity の文言・草案3 の判定器の表と位置の記述', '一部再現（κ は機械の判定と判定者の判定の一致で、全範囲で 1.000 か算出不能。何の一致かの断りは §9 に無い）' if ok else '一部再現', d)

    # ---- W150
    d = OrderedDict(L1969=L(1969), api_8B_retries=next((l.split('|')[12].strip() for l in API if '| 本番 | 8B |' in l), None),
                    sample_retry_line=find(SI, lambda l: '===RETRY===' in l and '件' in l)[:2])
    ok = d['api_8B_retries'] == '18' and 'API' not in L(1969)
    rec('W150', '書式の再試行の理由の未精査の範囲（Ge2）', '草案3 の 1969 行・API 再走行の記録の表・目視の記録', '再現' if ok else '一部再現', d)

    # ---- W151
    s6 = MR.index('## 6. 段取りとの差分と費用')   # v1.1: §5 の校正腕の表にも「| 9 | bridge:8B |」で始まる行があるので §6 の中に限る
    d = OrderedDict(run_record_row=next((l for l in MR[s6:] if l.startswith('| 9 | bridge:8B |')), None),
                    draft_sec9_mentions_overrun=any(('壁時計' in l or '見込みを' in l or '処理速度' in l) for l in D3[1958:1974]),
                    draft_L124_points=('main-run-A.md` §2 と §6' in L(124)))
    ok = bool(d['run_record_row']) and '5.22' in d['run_record_row'] and not d['draft_sec9_mentions_overrun']
    rec('W151', '橋 8B の壁時計の超過の開示（Ge1）', '走行記録 §6 の表・草案3 §9 と 124 行', '再現（数は走行記録にあり、草案3 は §2 で記録を指すが §9 に言及なし）' if ok else '一部再現', d)

    # ---- W152
    d = OrderedDict(json=s16('records/A/design-facts-A.json'), md=s16('records/A/design-facts-A.md'), analysis_input=AN['inputs']['facts'], frozen_line_208=FZ[207][:120])
    ok = d['json'] == 'CA116EC39DADEECD' and d['md'] == '945DD38717F47CAB'
    rec('W152', '設計事実の SHA16 が二つある（Cl1 の未解決）', '設計事実の json と md の SHA16', '再現しない（食い違いではない: CA116… は json・945D… は md）' if ok else '一部再現', d)

    # ---- W153
    d = OrderedDict()
    offs = {}
    for p in (1, 2, 3):
        BL = lines('records/reviews/A/results/bundle-results-A-part%d.md' % p)
        for i, l in enumerate(BL, 1):
            m = re.match(r'^# 部品 (\d+): ', l)
            if m:
                offs[int(m.group(1))] = i + 1
    cl2 = {2: 79, 3: 2075, 6: 2235, 10: 17, 11: 474, 13: 739, 14: 16, 15: 204}
    d['offsets'] = {k2: offs[k2] for k2 in cl2}; d['cl2_offsets_match'] = all(offs[k2] == v for k2, v in cl2.items())
    ok = d['cl2_offsets_match']
    rec('W153', '票の行の指し方の検査（Cl2 の部品ごとの足し算）', 'bundle の部品の書き出しの行（部品の本文の 1 行目 = 足し算の値 + 1）', '再現' if ok else '再現しない', d)

    status_after = git('status', '--porcelain', '--untracked-files=no')
    counts = Counter(x['verdict'].split('（')[0] for x in R)
    RESULT = OrderedDict(kind='verify_results_review_A_round1', version=VERSION, generated_utc=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
                         head=head, draft3_sha16=s16(D3P), analysis_sha16=s16('records/A/analysis-stageA.json'), contrasts_sha16=s16('design/contrasts-A.json'),
                         tool_sha16=hashlib.sha256(open(os.path.abspath(__file__), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper(),
                         tracked_changes_before=status_before, tracked_changes_after=status_after, seconds=round(time.time() - t0, 1), counts=dict(counts), items=R,
                         clause='本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
    json.dump(RESULT, open(out_js, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=str)
    M = ['# 結果報告 草案3 の公開前検分（第一巡）の所見の再現（機械生成・`verify_results_review_A_round1.py` %s・%s UTC）' % (VERSION, RESULT['generated_utc']), '',
         '- 事前登録: `preregistration-reproduction-results-A-round1.md`（SHA-256 は `verify.log` の [prereg] の行・再現の前に記帳）。票の略は `provenance.md`。',
         '- 対象: コミット %s・草案3 SHA16 %s・機械集計 SHA16 %s・正本 SHA16 %s・器 SHA16 %s。' % (head[:12], RESULT['draft3_sha16'], RESULT['analysis_sha16'], RESULT['contrasts_sha16'], RESULT['tool_sha16']),
         '- 判定の数: %s（全 %d 項）。所要 %s 秒。' % ('・'.join('%s %d' % (k2, v) for k2, v in counts.items()), len(R), RESULT['seconds']),
         '- 追跡中のファイルの変更: 実行前 %s・実行後 %s（リポジトリは書き換えていない）。' % ('なし' if not status_before.strip() else 'あり', 'なし' if not status_after.strip() else 'あり'),
         '- 詳細の全文は JSON。表の「詳細」は先頭だけを載せる。', '',
         '| W | 所見（票） | 確かめたこと | 判定 | 詳細（先頭） |', '|---|---|---|---|---|']
    for x in R:
        M.append('| %s | %s | %s | %s | %s |' % (x['w'], x['finding'], x['checked'], x['verdict'], json.dumps(x['detail'], ensure_ascii=False, default=str)[:300].replace('|', '／')))
    M += ['', RESULT['clause'], '']
    open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(M))
    print('[verify] %s | %s | %s 秒' % (out_md, dict(counts), RESULT['seconds']))


if __name__ == '__main__':
    main()
