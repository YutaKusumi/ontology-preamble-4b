# -*- coding: utf-8 -*-
"""make_repro_results_Bprime.py v0（2026-10-01・B′ の結果の巡の二票の事実の主張を、一次の記録で再現した値を一つの記録にまとめる・コーディネータ南無弥勒如来）。
採否の表は、この記録の値を指して書く（数を打ち直さない）。書く物: `repro-results-Bprime.json`（一度だけ）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, sys, json, math, hashlib, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
BP = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime'
OUT = os.path.join(HERE, 'repro-results-Bprime.json')
P = lambda *a: os.path.join(PUB, *a)
ld = lambda p: json.load(open(p, encoding='utf-8'))
PJ, T, FR, CR = ld(P('records', 'Bprime', 'pilot', 'pilot-Bprime.json')), ld(P('design', 'contrasts-Bprime.json')), ld(P('records', 'Bprime', 'FREEZE-RECORD-Bprime.json')), ld(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'))
rep = open(P('records', 'Bprime', 'results-Bprime.md'), encoding='utf-8').read()
cmd = open(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.md'), encoding='utf-8').read()
tl = open(os.path.join(BP, 'tools', 'tools-log-Bprime.md'), encoding='utf-8').read()
B = math.log(T['pilot']['p_bounds'][1] / T['pilot']['p_bounds'][0])
z = 1.959963984540054


def wilson(k, n):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [(c - h) / d, (c + h) / d]


cells = PJ['cells']
sess = {}
for zp in (os.path.join(BP, 'records', 'Bprime', 'extract-run', 'extract-run-20261001T040457Z.zip'), os.path.join(BP, 'records', 'Bprime', 'behavior-run', 'behavior-run-20261001T042902Z.zip'),
           os.path.join(BP, 'records', 'Bprime', 'pilot-run', 'pilot-run-20261001T050942Z.zip')):
    zz = zipfile.ZipFile(zp)
    n = [x for x in zz.namelist() if x.endswith('/session.json')][0]
    S = json.loads(zz.read(n))
    sess[S['kind']] = {'keys': sorted(S.keys()), 'has_driver_or_cuda_runtime': any(k for k in S if 'driver' in k.lower() or 'cuda' in k.lower())}
R = {
    'kind': 'bprime_results_round_reproduction',
    'p_bounds_logodds': B,
    'pa': {k: v['pa'] for k, v in cells.items()},
    'mass_min_observed': min(v['mass'] for v in cells.values()),
    'distance_outside_logodds': {k: abs(v['lo']) - B for k, v in cells.items() if not v['pass_i_ii']},
    'margin_inside_logodds': {k: B - abs(v['lo']) for k, v in cells.items() if v['pass_i_ii']},
    'vi_a_below_margin_all': all(PJ['vi']['a'][k] < abs(abs(v['lo']) - B) for k, v in cells.items()),
    'vi_a_over_noise_max_all': all(x > T['pilot']['noise_max'] for x in PJ['vi']['a'].values()),
    'vi_decision': PJ['vi']['decision'],
    'decision': PJ['decision'],
    'n_forward': PJ['n_forward'],
    'variant_flags': {x: sum(1 for f in PJ['iv'][x]['flags'].values() if f) for x in ('V1', 'V2', 'V3')},
    'V2_SK_Onull_diff': PJ['iv']['V2']['lo']['SK|Onull'] - cells['SK|Onull']['lo'],
    'V1_within_bounds_cells': sum(1 for x in PJ['iv']['V1']['lo'].values() if abs(x) <= B),
    'wilson_0_of_40': wilson(0, 40), 'wilson_40_of_40': wilson(40, 40),
    'report_section1_rows': [l for l in rep.split('\n') if l.startswith('| ') and '満た' in l and '\\|' in l],
    'report_section6_external_line': [l for l in rep.split('\n') if '）による採点の一致' in l],
    'closed_md_validity_line': [l for l in cmd.split('\n') if '妥当性の測定ではない' in l],
    'report_has_validity_phrase_in_section6': '一致の記述で、妥当性の測定ではない' in rep.split('## 6.')[1].split('## 9.')[0],
    'report_stale_limit_line_present': 'Gemma の場面の出力と読み取りの値はまだ誰も見ていない' in rep,
    'report_mentions_colab_cpu_prefreeze': ('Colab の CPU' in rep) or ('案 A' in rep),
    'tools_log_promises_report_note': '報告に注として残す' in tl,
    'lock_excluded': sorted(T['computation']['main_freeze']['lock_excluded']),
    'build_report_in_lock_excluded': 'tools/build_report_Bprime.py' in T['computation']['main_freeze']['lock_excluded'],
    'freeze_record_stage': FR.get('stage'),
    'row_C_cell_keys': list(list(CR['row_C']['cells'].values())[0].keys()),
    'versions_rule': T['inputs']['versions'].get('rule'),
    'session_records': sess,
    'negation_templates_in_report': [t for t in T['negation_templates'] if t in rep],
    'negation_templates': T['negation_templates'],
    'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。',
}
assert not os.path.exists(OUT)
open(OUT, 'w', encoding='utf-8', newline='\n').write(json.dumps(R, ensure_ascii=False, indent=1))
print(json.dumps({k: R[k] for k in ('report_has_validity_phrase_in_section6', 'report_stale_limit_line_present', 'report_mentions_colab_cpu_prefreeze', 'tools_log_promises_report_note',
                                     'build_report_in_lock_excluded', 'freeze_record_stage', 'session_records', 'negation_templates_in_report', 'V1_within_bounds_cells', 'variant_flags')}, ensure_ascii=False, indent=1))
print('SHA16', hashlib.sha256(open(OUT, 'rb').read()).hexdigest().upper()[:16])
