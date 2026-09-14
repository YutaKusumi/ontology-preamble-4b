# -*- coding: utf-8 -*-
"""verify_review_final_A.py v1 —— 凍結前の最終検分（七票）の所見を、コミット 168cccb の器材・正本・転記行・公開物に当てて再現する（2026-09-14・事前登録 records/reviews/A/final/preregistration-reproduction-A-final.md）。
番号は W77 から（W1〜W76 に続ける）。票の略: Ge1・Ge2（Gemini 3.8 Flash）・Gr1・Gr2（Grok 4.6）・Cl1・Cl2・Cl3（claude.ai の Claude Opus 5）（records/reviews/A/final/provenance.md）。
各項は「再現／一部再現／再現しない／検査不能」を機械で判定する。コードの読みで足りる所見は該当の行の実物（ソースの文字列）に当て、挙動に関わる所見は一時置き場で実験を走らせる。
リポジトリのファイルは書き換えない（変異は一時置き場の写し・合成のデータと報告は一時置き場）。最後に追跡中のファイルに変更が無いことを確かめて記録する。
出力: records/reviews/A/final/verification-final-A.md と同 .json（--out で変更可）。
用法: python tools/verify_review_final_A.py --scratch <リポジトリの外の一時置き場> [--skip-reach] [--skip-synth] [--B-reach 1000] [--out <接頭辞>]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。合成の件数は検査のための人工値であり、いかなる読みにも用いない。
"""
import os, sys, json, re, math, shutil, subprocess, argparse, datetime, hashlib, inspect, urllib.request, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import confirm_A
import report_lint
from zaxis_A import z_map
REPO = runs_A.REPO
VERSION = 'v1'
ap = argparse.ArgumentParser(); ap.add_argument('--scratch', required=True); ap.add_argument('--skip-reach', action='store_true'); ap.add_argument('--skip-synth', action='store_true')
ap.add_argument('--B-reach', type=int, default=1000); ap.add_argument('--out', default=None)
a = ap.parse_args()
SCR = os.path.abspath(a.scratch); os.makedirs(SCR, exist_ok=True)
assert not os.path.normcase(SCR).startswith(os.path.normcase(REPO)), '一時置き場はリポジトリの外に置く'
T0 = time.time()
T = runs_A.load_T(); FAM = T['families']['A_slope']; R = confirm_A.Rules(T); ME = T['reading_selection']['measurable_effect_type']
PY = [sys.executable]; ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
SRC = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read()
TOOL = lambda nm: os.path.join(REPO, 'tools', nm)
ROWS = []
lf16 = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
HEADC = subprocess.run(['git', '-C', REPO, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
STATUS0 = subprocess.run(['git', '-C', REPO, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout


def W(num, findings, desc, verdict, detail=''):
    assert verdict in ('再現', '一部再現', '再現しない', '検査不能'), verdict
    ROWS.append({'id': 'W%d' % num, 'num': num, 'findings': findings, 'desc': desc, 'verdict': verdict, 'detail': detail})
    print('[W%d] %s %s %s' % (num, verdict, findings, json.dumps(detail, ensure_ascii=False, default=str)[:240]), flush=True)


def run(args, cwd=REPO, timeout=None):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=ENV, cwd=cwd, timeout=timeout)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def section(text, head, nxt):
    i = text.index(head); j = text.index(nxt, i + len(head)); return text[i:j]


CF = SRC('tools/confirm_A.py'); AZ = SRC('tools/analyze_A.py'); BR = SRC('tools/build_report_A.py'); SY = SRC('tools/synth_A.py'); PG = SRC('tools/power_grid_A.py')
FZ = SRC('tools/freeze_A.py'); SI = SRC('tools/sample_inspection_A.py'); NL = SRC('tools/numbers_lint.py'); BOOT = SRC('tools/colab/boot_stageA.py'); CB = SRC('tools/calib_band_A.py')
JF = SRC('tools/judge_fragments_A.py'); MC = SRC('tools/make_contrasts_A.py'); TI = SRC('records/A/tooling-interpretations-A.md'); D8 = SRC('design/design-stageA-draft8.src.md')
RM = SRC('README.md'); RFL = SRC('records/reviews/A/draft7-impl/reflection-impl-A.md'); ADI = SRC('records/reviews/A/draft7-impl/adoption-table-impl-A.md')
FACTS = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'design-facts-A.json'))['facts']; G = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'power-grid-A.json'))
TJ = json.dumps(T, ensure_ascii=False)

# ---- W77 公開物の正本（Gr1 M1・Gr2 M3）
local16 = runs_A.sha16_file(runs_A.CPATH); pub = {}
for ref in ('main', HEADC):
    try:
        b = urllib.request.urlopen('https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/%s/design/contrasts-A.json' % ref, timeout=60).read()
        J = json.loads(b); CRp = J['families']['A_slope']['confirm_rule']
        pub[ref[:7]] = {'sha16': lf16(b), 'version': J['version'], 'generator': J['generator'], 'type': CRp.get('type'), 'labels': 'labels' in CRp, 'label_combo_table': 'label_combo_table' in CRp}
    except Exception as ex:
        pub[ref[:7]] = {'error': str(ex)[:200]}
hist = {}
for c in ('550295f', 'c95d032', '51f7e3a', '99d28da', 'dfdd7b0', HEADC[:7]):
    pb = subprocess.run(['git', '-C', REPO, 'show', '%s:design/contrasts-A.json' % c], capture_output=True).stdout; J = json.loads(pb); CRh = J['families']['A_slope']['confirm_rule']
    hist[c] = {'sha16': lf16(pb), 'version': J['version'], 'generator': J['generator'], 'type': CRh.get('type'), 'labels': 'labels' in CRh, 'label_precedence': 'label_precedence' in CRh}
err = any('error' in v for v in pub.values()); same = (not err) and all(v['sha16'] == local16 and v['labels'] and v['label_combo_table'] for v in pub.values())
W(77, 'Gr1 M1・Gr2 M3', '公開物の正本が草案8 の正本（SHA16・生成器 v2.4・labels・label_combo_table）と違う版か。見えた版はどのコミットのものか', '検査不能' if err else ('再現しない' if same else '再現'),
  {'local_sha16': local16, 'public': pub, 'gr1_like_commits(type=two_scale_iut_holm・labels なし)': [c for c, v in hist.items() if v['type'] == 'two_scale_iut_holm' and not v['labels']],
   'gr2_like_commits(draft6・v2.1)': [c for c, v in hist.items() if v['version'] == 'draft6-2026-09-13' and v['generator'].endswith('v2.1')], 'history': hist})

# ---- W78 凍結器の記帳（Gr1 §3-1・3-2）
mf = re.search(r"MF = \{'kind'(.*?)\n    json\.dump", FZ, re.S); mf_keys = re.findall(r"'(\w+)':", "{'kind'" + (mf.group(1) if mf else ''))
W(78, 'Gr1 §3-1・3-2', '凍結器が自己検査（confirm_A --selftest など）を走らせず、その合格と公開物の SHA16 の一致を凍結記録に書かないか', '再現' if ('selftest' not in FZ and 'raw.githubusercontent' not in FZ) else '再現しない',
  {'manifest_keys': mf_keys, 'selftest_in_freeze_A': 'selftest' in FZ})

# ---- W79 凍結前の手順と状態（Ge1 重大1・2・Ge2 条件・Gr1 M2・M3・Gr2 M2）
PR = T['procedure']; ix = lambda s: next(i for i, x in enumerate(PR) if x.startswith(s))
order = [ix('門0.5'), ix('Firth の一致検査'), ix('判定器の妥当性の範囲の確定'), ix('登録者の凍結確認'), ix('凍結・予想封印')]
st = T['tooling_interpretations']['status']; fst = T['firth_check']['status']; jsd = T['judge_validity'].get('scope_decided', '（キーなし）')
W(79, 'Ge1 重大1・2・Ge2 条件・Gr1 M2・M3・Gr2 M2', '凍結前の手順（門0.5・Firth の一致検査・判定器の範囲・運用の解釈の確認）が未了で、手順表が凍結の前に置いているか',
  '再現' if (order == sorted(order) and '凍結確認の前' in st and '未実行' in fst and jsd is None) else '一部再現',
  {'procedure_index': order, 'tooling_status': st, 'firth_status_tail': fst[-20:], 'judge_scope_decided': jsd})

# ---- W80 --facts が任意で到達の見込みの欄が置き換わる（Cl1 中1）・実験は合成の走 1 の後
c80 = {'analyze_facts_optional': "FACTS = runs_A.read_json(a.facts) if a.facts and os.path.exists(a.facts) else None" in AZ and 'REACH = None' in AZ,
       'report_fallback': "AN.get('reach_note') or '（到達の見込みの記録なし）'" in BR, 'lint_blank_misses_fallback': report_lint.BLANK.search('（到達の見込みの記録なし）') is None,
       'synth_requires_reach_note_path': "'reach_note'" in SY.split('PATHS_REQUIRED = [')[1].split(']')[0]}

# ---- W81 束に無い六つのファイル（Cl1 中2）
N6 = ['records/A/power-grid-A.json', 'records/A/design-facts-A.json', 'tools/run_preamble_local.py', 'tools/cost_facts.py', 'tools/response_mode_M.py', 'tools/response_mode_F.py']
tree = set(subprocess.run(['git', '-C', REPO, 'ls-tree', '-r', '--name-only', HEADC], capture_output=True, text=True).stdout.split('\n')); idxt = SRC('records/reviews/A/final/bundle-A-final-index.md')
in_tree = {n: n in tree for n in N6}; in_bundle = {n: ('`%s`' % n) in idxt for n in N6}; in_freeze = {n: os.path.basename(n) in FZ for n in N6}
W(81, 'Cl1 中2', '器材の必須入力六つが束に無く、公開物にも無いか', '一部再現' if (all(in_tree.values()) and not any(in_bundle.values())) else ('再現' if not all(in_tree.values()) else '再現しない'),
  {'public_commit_tracked': in_tree, 'in_bundle_index': in_bundle, 'in_freeze_scope': in_freeze})

# ---- W82 測れた効果種: 独立の仮定の向き（Ge1 中3・Gr1 C1・Gr2 M1・Cl3 重大3(b)）
eff = {}
for c in FAM['contrasts']:
    eff.setdefault(c['id'].split(':', 1)[1], []).append(c['scenario'])
distinct = all(len(v) == len(set(v)) for v in eff.values()); child = 'rng = np.random.default_rng([seed, i])' in CF
rule_text = T['reading_selection']['text']; toward = ('測れた効果種」にも傾向が立たず' in rule_text) and ('規模非依存' in rule_text)
W(82, 'Ge1 中3・Gr1 C1・Gr2 M1・Cl3 重大3(b)', '(i) 同じ効果種の対比が場面をまたいで標本・乱数を共有し、独立式が計算の前提の内で上界になるか (ii)「測れた」を多く数えることがどの読みに効くか',
  '一部再現' if (distinct and child and toward) else '再現',
  {'(i) effect_scenarios_distinct': distinct, '(i) per_contrast_child_stream': child, '(i) 判定': '同じ効果種の対比は場面ごとに別の走行の標本と別の子ストリームで模擬され、独立式は計算の前提（全場面に Δ）の内で一致する。上界の主張は再現しない' if (distinct and child) else '共有あり',
   '(ii) selection_rule': rule_text, '(ii) 判定': '数えすぎは「どの測れた効果種にも傾向が立たない→規模非依存」の読みに届きやすくする側（Gr1・Gr2・Cl1・Cl3 の向きを再現・Ge1 の「保守的」は再現しない）' if toward else '不明'})

# ---- W83・W84 測れた効果種: MC の幅と場面ごとの被覆（Cl2 重大1・Cl3 重大3(a)(d)・Cl1 中3・Cl2 重大2）
BDR = G['B']['DR']; agg = {}
for r in G['DR']:
    if r['delta'] == '0':
        continue
    agg.setdefault((r['id'].split(':', 1)[1], r['ctrl_trend']), []).append((r['id'], r['card_D1_holm_first']))


def halfwidth(ps, B):
    var = 0.0
    for i, p in enumerate(ps):
        d = 1.0
        for j, q in enumerate(ps):
            if j != i:
                d *= 1.0 - q
        var += d * d * p * (1 - p) / B
    return 1.96 * math.sqrt(var)


TAB = {}
for (e, tr), lst in agg.items():
    ps = [p for _, p in lst]; a1 = confirm_A.at_least_one(ps)
    TAB[(e, tr)] = {'n': len(ps), 'at_least_one': a1, 'hw95': halfwidth(ps, BDR), 'ge08': sum(p >= ME['threshold'] for p in ps), 'lt005': sum(p < 0.05 for p in ps), 'mean': sum(ps) / len(ps),
                    'measurable': a1 >= ME['threshold'], 'crosses': abs(a1 - ME['threshold']) <= halfwidth(ps, BDR), 'ids_lt005': [i for i, p in lst if p < 0.05]}
near = lambda x, y, tol: abs(x - y) <= tol + 1e-9
cl2_hw = {('Onull~N', '下降'): (0.764, 0.022), ('O-Ncold~Onull-Ncold', '下降'): (0.507, 0.030), ('Onull-Ncold~Onull', '上昇'): (0.379, 0.028), ('Onull-Ncold~Onull', '一定'): (0.952, 0.009), ('Onull~N', '一定'): (0.973, 0.007)}
hw_match = {'%s|%s' % k: near(TAB[k]['at_least_one'], v[0], 0.0005) and near(TAB[k]['hw95'], v[1], 0.0005) for k, v in cl2_hw.items()}
p5 = 1 - 0.2 ** (1 / 5); cl3_hw = halfwidth([p5] * 5, BDR)
ret_no_interval = "types[e] = {'n_contrasts': len(ps), 'at_least_one': a1, 'measurable': bool(a1 >= ME['threshold'])}" in CF
W(83, 'Cl2 重大1・Cl3 重大3(d)', '測れた効果種の「少なくとも一本」に MC の区間が無く、B=1000 の半幅が ±0.01〜0.03 で、区間が閾値をまたぐときの規則が無いか',
  '再現' if (ret_no_interval and all(hw_match.values()) and near(cl3_hw, 0.017, 0.0005)) else '一部再現',
  {'returns_interval': not ret_no_interval, 'cl2_values_match': hw_match, 'cl3_per_contrast_0.2752_hw': round(cl3_hw, 4), 'B_DR': BDR,
   'crossing_types': ['%s|%s' % k for k, v in TAB.items() if v['crosses']], 'boundary_rule_in_spec': ('またぐ' in json.dumps(ME, ensure_ascii=False))})
trends = ('一定', '上昇', '下降')
lvl = {tr: {'ge08': sum(1 for r in G['DR'] if r['delta'] != '0' and r['ctrl_trend'] == tr and r['card_D1_holm_first'] >= 0.8), 'lt005': sum(1 for r in G['DR'] if r['delta'] != '0' and r['ctrl_trend'] == tr and r['card_D1_holm_first'] < 0.05),
           'types_measurable': sum(1 for (e, t_), v in TAB.items() if t_ == tr and v['measurable'])} for tr in trends}
cl1 = {('Onull~N', '一定'): (0.973, 1, 5), ('Lneg~Onull', '一定'): (0.999, 2, 5), ('Onull-Ncold~Onull', '一定'): (0.952, 1, 4), ('O-Ncold~Onull-Ncold', '一定'): (0.999, 2, 4)}
cl2 = {('Onull~N', '一定'): (0.973, 3, 0.287), ('Onull~N', '上昇'): (0.991, 3, 0.215), ('Lneg~Onull', '一定'): (0.999, 3, 0.381), ('Lneg~Onull', '上昇'): (0.999, 3, 0.386), ('Lneg~Onull', '下降'): (0.997, 3, 0.379)}
m1 = {'%s|%s' % k: near(TAB[k]['at_least_one'], v[0], 0.0005) and TAB[k]['ge08'] == v[1] and TAB[k]['n'] == v[2] for k, v in cl1.items()}
m2 = {'%s|%s' % k: near(TAB[k]['at_least_one'], v[0], 0.0005) and TAB[k]['lt005'] == v[1] and near(TAB[k]['mean'], v[2], 0.0005) for k, v in cl2.items()}
m2t = lvl == {'一定': {'ge08': 10, 'lt005': 7, 'types_measurable': 5}, '上昇': {'ge08': 5, 'lt005': 12, 'types_measurable': 3}, '下降': {'ge08': 4, 'lt005': 12, 'types_measurable': 2}}
W(84, 'Cl1 中3・Cl2 重大2・Cl3 重大3(a)', '「測れた」効果種の中に、個別の到達が閾値に届かない場面や 0.05 未満の場面が残り、読み条項 (xvi) が場面の粒度に掛からないか',
  '再現' if (all(m1.values()) and all(m2.values()) and m2t and '測れなかった効果種について' in D8) else '一部再現',
  {'cl1_table_match': m1, 'cl2_table_match': m2, 'cl2_totals_match': m2t, 'levels': lvl, 'per_contrast_needed_k': {k: round(1 - 0.2 ** (1 / k), 4) for k in (3, 4, 5)},
   'table': {'%s|%s' % k: {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in sorted(TAB.items())}})

# ---- W85 「観測された効果量は使わない」と d0（Cl1 中3 後半・Cl3 重大3(e)）
W(85, 'Cl1 中3 後半・Cl3 重大3(e)', '正本の rule が「4B の処置と対照の差を基底に」と「観測された効果量は使わない」を併記し、実装が d0＝rA4−rB4（実測の 4B の差）を使うか',
  '再現' if ('4B の処置と対照の差を基底に' in ME['rule'] and '観測された効果量は使わない' in ME['rule'] and "d0 = float(r['rA4'] - r['rB4'])" in CF) else '再現しない',
  {'rule': ME['rule'], 'code': "d0 = float(r['rA4'] - r['rB4'])"})

# ---- W88 門の前の札 D1（Gr2 C1）
W(88, 'Gr2 C1', '測れた効果種の確率が門（refuse・様式・環境）の前の札 D1（初段）で数えられるか', '再現' if "p = det['card_D1_holm_first']" in CF else '再現しない', {'code': "p = det['card_D1_holm_first']"})

# ---- W89 B の突合（Gr2 M4）
Dtext = FACTS['D']['text']
W(89, 'Gr2 M4', '測れた効果種の B（B_per_contrast）と転記行 D の B の対応が印字されていないか', '一部再現' if (ME['B_per_contrast'] == G['B']['DR'] and 'B_per_contrast' not in Dtext) else '再現しない',
  {'B_per_contrast': ME['B_per_contrast'], 'grid_B': G['B'], 'rowD_B_strings': re.findall(r'B=[\d,]+', Dtext), '判定': '値は DR 節と一致（1000）・D 節は 2000・対応の一文は無い'})

# ---- W90 区間の水準と被覆の文言（Cl2 重大3・Cl3 中7）
docs = {'spec': TJ, 'draft8_src': D8, 'draft8': SRC('design/design-stageA-draft8.md'), 'template_src': SRC('records/A/results-report-template-A.src.md'), 'template': SRC('records/A/results-report-template-A.md')}
W(90, 'Cl2 重大3・Cl3 中7', '区間を札によらず status ok の全対比にその対比の p* の Holm の順位の水準で付け、被覆（同時被覆）の断りが正本・草案・雛形に無いか',
  '再現' if ("o['interval_pt'] = interval(R, r['slope'], r['se'], float(ls[i]))" in CF and all(v.count('被覆') == 0 for v in docs.values())) else '一部再現',
  {'被覆': {k: v.count('被覆') for k, v in docs.items()}, '同時（同時要求数を除く）': {k: len(re.findall(r'同時(?!要求)', v)) for k, v in docs.items()}, 'report_prints_interval_all_ok': "x['interval_pt'][0], x['interval_pt'][1])) if ok else '—'" in BR})

# ---- W91 様式門の多重性（Cl3 重大4）
gb = G['G']['bands']; SG = T['style_gate']; Gtext = FACTS['G']['text']
union = {bp: {rt: 1 - (1 - v) ** 12 for rt, v in gb[bp].items()} for bp in gb}
W(91, 'Cl3 重大4', '様式門は残存規模ごとに (a)(b) を見て一つでも超えれば発火するのに、転記行 G はセルあたりの率だけか（12 セルをまたいだ率）',
  '再現' if ("for nm, xa, xb in (('a', a_A, a_B), ('b', b_A, b_B)):" in CF and SG['denominator'] == 'n_ok' and 'またい' not in Gtext) else '一部再現',
  {'per_cell_n200': {bp: {rt: '%.3e' % v for rt, v in gb[bp].items()} for bp in gb}, 'union_12_cells_independent': {bp: {rt: '%.3e' % v for rt, v in union[bp].items()} for bp in union},
   'cl3_note_0.0266_match': near(union['15']['0.5'], 0.0266, 0.00005), 'cl3_hold_1.3e-08_match': near(union['30']['0.5'], 1.3e-08, 0.05e-08), 'numerator': SG['numerator'], 'denominator': SG['denominator'],
   '注意': '同じ規模の (a)(b) は同じ試行から数えるので独立は近似・真の率 0.5 は最も発火しやすい置き方'})

# ---- W92 生成器の文字列リテラル検査の範囲と切り詰めの二重実装（Cl3 重大1・軽12）
rep92 = os.path.join(SCR, 'w92-numbers-lint.md')
rc92, out92 = run([TOOL('numbers_lint.py'), '--json', 'design/contrasts-A.json', '--gen', 'tools/make_contrasts_A.py', 'tools/design_facts_A.py', 'tools/power_grid_A.py', 'tools/confirm_A.py', '--report', rep92])
L92 = open(rep92, encoding='utf-8').read() if os.path.exists(rep92) else ''
cnt92 = {m.group(1): int(m.group(2)) for m in re.finditer(r'生成器の文字列リテラル検査（`([^`]+)`）: 構造でない数 (\d+)', L92)}
clip_lines = [i + 1 for i, l in enumerate(PG.split('\n')) if '0.001' in l and '0.999' in l]; lint_draft8 = SRC('records/A/numbers-lint-draft8A.md')
W(92, 'Cl3 重大1・軽12', '生成器の検査が power_grid_A.py と confirm_A.py を範囲に入れておらず、入れると構造でない数が出るか。切り詰めの上下限が格子に直書きで残るか',
  '再現' if (cnt92.get('tools/power_grid_A.py') == 34 and cnt92.get('tools/confirm_A.py') == 12 and 'power_grid_A.py' not in lint_draft8 and len(clip_lines) >= 5) else '一部再現',
  {'counts': cnt92, 'draft8_lint_gen_scope_has_power_grid': 'power_grid_A.py' in lint_draft8, 'grid_lines_with_0.001_0.999': clip_lines, 'grid_treat_defined': 'def treat(pc, d0, D, sgn):' in PG,
   'grid_uses_reach_treatment': PG.count('confirm_A.reach_treatment'), 'refuse_labels_literal': [l.strip()[:90] for l in PG.split('\n') if "cfgs.append(('転位" in l][:3]})

# ---- W93 効果種の単位（Cl3 重大2）
W(93, 'Cl3 重大2', '正本の対比に effect の欄が無く、集計器が id の文字列分割で効果種を決めるか', '再現' if ('effect' not in FAM['contrasts'][0] and isinstance(FAM['effect_types'], int) and "'effect': c['id'].split(':', 1)[1]" in AZ) else '再現しない',
  {'contrast_keys': list(FAM['contrasts'][0].keys()), 'effect_types': FAM['effect_types'], 'generator_EFFECT_list': 'EFFECT = [' in MC})

# ---- W95 P104 の経路と草案8 §0（Cl1 中4）
S0 = section(D8, '## 0.', '## 1.')
W(95, 'Cl1 中4', '採否表 P104（パイロットの様式の記録の層ごとの破局数・環境帯の引き直しの腕別の率が本走行の前に目に入る経路）が草案8 §0 に無いか',
  '再現' if (not any(w in S0 for w in ('様式の記録', '引き直しの腕別', '目に入る'))) and 'P104' in ADI else '再現しない', {'in_adoption_table': 'P104' in ADI, 'in_reflection_record': 'P104（率盲検の経路）' in RFL, 'draft8_section0_chars': len(S0)})

# ---- W97 全組合せ表の出所と行 id の符号化（Cl2 中5・Cl2 軽・Gr1 C2）
W(97, 'Cl2 中5・Cl2 軽・Gr1 C2', '正本の全組合せ表は判定関数の出力を書き戻したもので、合成検査の期待の行 id も同じ row_id で符号化するか',
  '再現' if ('from confirm_A import combo_rows' in MC and 'COMBO = combo_rows(LABELS)' in MC and "'stage2_first_match': [" in MC and "confirm_A.row_id(2, clause=ty['clause']" in SY) else '再現しない',
  {'order_oracle_in_selftest': "first = T['families']['A_slope']['confirm_rule']['label_stages']['stage2_first_match']" in CF})

# ---- W99 抽出検査の鍵・分類の置き場と印字（Ge1 中5・Cl2 中6・Cl1 軽2・Cl3 軽11）
W(99, 'Ge1 中5・Cl2 中6・Cl1 軽2・Cl3 軽11', '抽出検査が標本と対応表（鍵）と分類の集計を同じ置き場に書き、標本に生本文の先頭と件ごとの機械分類を印字するか',
  '再現' if (all(("OUTP + '%s'" % x) in SI for x in ('-sample.txt', '-key.json', '-modes.json')) and '| 機械分類 %s |' in SI and T['sample_inspection']['chars'] == 600) else '再現しない',
  {'out_prefix_default': "os.path.join(REPO, 'records', 'A', 'sampling-inspection-A-%s' % a.tag)" in SI, 'judge_key_outside_repo': '--keydir' in JF, 'chars': T['sample_inspection']['chars']})

# ---- W100 運用の解釈 26・27 の向き（Cl1 軽1・Cl2 中7）
items = {int(m.group(1)): m.group(0) for m in re.finditer(r'## (\d+)\. .*?(?=\n## |\Z)', TI, re.S)}
pull = lambda k: any(w in items[k] for w in ('側に引く', '引かれる', '引く側'))
W(100, 'Cl1 軽1・Cl2 中7', '運用の解釈 26・27 に、選んだ読みが確証を増やす側（保留・降格が減る側）であることの記載が無いか', '再現' if (not pull(26) and not pull(27) and pull(10)) else '一部再現',
  {'item10_pull_stated': pull(10), 'item26_pull_stated': pull(26), 'item27_pull_stated': pull(27), 'item26_rejected_alt': re.search(r'採らなかった案: (.*)', items[26]).group(1)[:80], 'item27_rejected_alt': re.search(r'採らなかった案: (.*)', items[27]).group(1)[:80]})

# ---- W101 Firth 不合格の道筋（Cl2 中8）
FCk = T['firth_check']
W(101, 'Cl2 中8', 'Firth の一致検査の不合格のときに選べる手が登録されていないか', '再現' if not any(w in json.dumps(FCk, ensure_ascii=False) for w in ('選べる手', '選択肢', '再走する手')) else '再現しない', {'failure_path': FCk['failure_path']})

# ---- W102 段 0 の理由の重なり（Cl2 中9）
res102 = [{'status': 'undecidable', 'reason': 'residual', 'kept': 0, 'keep': [], 'censored': []} for _ in range(R.m)]
res102[0] = {'status': 'nonconverged', 'reason': 'nonconverged', 'kept': 6, 'keep': [True] * 6, 'censored': [False] * 6}
o102 = confirm_A.label_family(R, res102, None, shrink_idx={0})[0]
W(102, 'Cl2 中9', '門2 の縮小と非収束が重なった対比で、行 id と規則に縮小だけが残るか', '再現' if (o102['rules'] == ['gate2_shrink'] and o102['row'] == 'U-gate2_shrink') else '再現しない', {'row': o102['row'], 'rules': o102['rules']})

# ---- W103 時間貸しと停止規則（Ge2 中2・Cl3 中9）
up = FACTS['F']['data']['plans']['upper']; share32 = up['rows']['32B']['units'] / up['units']
W(103, 'Ge2 中2・Cl3 中9', '停止規則は Colab のユニットだけを見て、時間貸し（第三）の費用の基準が登録されていないか', '再現' if ('借りる前に登録者が裁定' in T['cost']['rental_rule'] and 'multiplier' in T['cost']['stop_rule']) else '再現しない',
  {'rental_rule': T['cost']['rental_rule'], 'stop_rule_reference': T['cost']['stop_rule']['reference'], '32B_units_share_upper': round(share32, 4), '32B_units': round(up['rows']['32B']['units'], 2), 'upper_units': round(up['units'], 2)})

# ---- W104 初点の名乗りの解放（Cl3 中8）
W(104, 'Cl3 中8', '名乗りを別の機種へ移す手順が器の説明文と反映の記録にだけあり、正本と運用の解釈の一覧に無いか', '再現' if ('名乗りの記録を退避してから' in CB and '名乗りの記録を退避してから' in RFL and '退避' not in TJ and '退避' not in TI) else '一部再現',
  {'calib_band_A_docstring': '名乗りの記録を退避してから' in CB, 'reflection_record': '名乗りの記録を退避してから' in RFL, 'spec': '退避' in TJ, 'tooling_list': '退避' in TI})

# ---- W105 格子の解釈条項の発火率と除外（Cl3 中5）
W(105, 'Cl3 中5', '格子の模擬は測定不能・錨帯の除外を入れず（extra_keep なし）、解釈条項の飽和を除外の後の規模で数える登録（運用の解釈 27）と配置が違うか',
  '再現' if ('return confirm_A.simulate_cell(R, zs, n, pc, pt, B, rng)' in PG and 'count_after' in json.dumps(FAM['interpretation_clause'], ensure_ascii=False)) else '再現しない', {'rowD_mentions_count_after': 'count_after' in Dtext or '除外の後に残った規模で数える' in Dtext})

# ---- W106 転記行 E の丸め（Cl1 軽3）
from scipy.stats import binom
rawE = float(binom.cdf(4, 200, 0.05)); rawS = float(binom.cdf(4, 200, 0.005)); Et = FACTS['E']['text']
W(106, 'Cl1 軽3', '転記行 E が格子の丸め済みの値をさらに丸めて印字し、生値から一度で丸めた値と一桁ずれるか', '再現' if ('0.0265' in Et and '%.4f' % rawE == '0.0264' and '単一セル 0.997' in Et and '%.3f' % rawS == '0.996') else '再現しない',
  {'size_raw': rawE, 'grid_stored': G['E']['size_at_k_max'], 'printed': '0.0265', 'one_step': '%.4f' % rawE, 'single_raw_0.005': rawS, 'grid_stored_single': G['E']['rows'][0]['single_cell'], 'printed_single': '0.997', 'one_step_single': '%.3f' % rawS})

# ---- W107 凍結器の --check の終了コード（Cl1 軽4）
rc107, out107 = run([TOOL('freeze_A.py'), '--check'])
miss107 = int(re.search(r'欠け (\d+)', out107).group(1)) if re.search(r'欠け (\d+)', out107) else None
W(107, 'Cl1 軽4', '凍結器の --check が欠けありでも終了コード 0 で終わるか', '再現' if (rc107 == 0 and miss107) else '再現しない', {'rc': rc107, 'missing': miss107, 'head': out107.split('\n')[0][:120]})

# ---- W108 転記行 M の腕の並び（Cl2 軽）
W(108, 'Cl2 軽', '転記行 M が 13 腕の値を先に、確証族に現れる 8 腕の値を括弧に置くか', '再現' if re.search(r'いずれかの腕が超える確率 [\d.]+（確証族に現れる 8 腕では [\d.]+）', FACTS['M']['text']) else '再現しない',
  {'selection_rule_uses': json.dumps(T['environment_band'].get('selection_rule'), ensure_ascii=False)[:160]})

# ---- W109 数の検査の docstring の除外（Cl2 軽）
lim = re.search(r"^LIMIT = '(.*)'$", NL, re.M).group(1)
W(109, 'Cl2 軽', '数の検査の生成器の検査が docstring を除き、報告に印字する限界の欄にその旨が無いか', '再現' if ('isinstance(node.body[0], ast.Expr)' in NL and 'docstring' not in lim) else '再現しない', {'limit_text': lim[:120]})

# ---- W110 refuse 門の適用の不等号（Gr1 L1）
W(110, 'Gr1 L1', '集計器は p_β < α で refuse 門を当て、模擬の名目の数え方は p_β ≤ α か', '再現' if ("if res['p_beta'] < RR.alpha:" in AZ and "Rn = r['p_beta'] <= R.alpha" in CF) else '再現しない', {'spec_applies_to': FAM['refuse_gate']['applies_to']})

# ---- W111 検査用の口と印（Gr1 L2・L3）
callers = {nm: SRC('tools/' + nm).count('gate2_shrink=True') for nm in os.listdir(os.path.join(REPO, 'tools')) if nm.endswith('.py') and not nm.startswith('verify_review')}
W(111, 'Gr1 L2・L3', '全対比を縮小する口（gate2_shrink=True）と --B-measurable が本番の経路で使われうるか（使われれば印が付くか）',
  '再現' if (sum(callers.values()) == 0 and 'gate2_shrink=g2' in CF and "('B_measurable_override', a.B_measurable is not None)" in AZ and "'・'.join(AN.get('dev_marks') or []) or 'なし'" in BR) else '一部再現',
  {'literal_true_callers': {k: v for k, v in callers.items() if v}, 'selftest_uses_port': 'gate2_shrink=g2' in CF, 'analyze_passes_shrink_idx': 'shrink_idx=SHRINK_IDX' in AZ, 'dev_mark_B': True})

# ---- W112 余地の向きの境（Gr1 L4）
W(112, 'Gr1 L4', '4B の処置の率がちょうど 0.5 のとき下向きか', '再現' if confirm_A.reach_direction(0.5) == -1.0 else '再現しない', {'reach_direction(0.5)': confirm_A.reach_direction(0.5)})

# ---- W113 合成記録の日付（Gr1 L5・Gr2 L1）
sm = SRC('records/A/synth-A-2026-09-14.md').split('\n')[0]
W(113, 'Gr1 L5・Gr2 L1', '合成記録のファイル名の日付と、本文の生成時刻（UTC）の日付が違うか', '再現' if ('2026-09-13' in sm and 'datetime.date.today().isoformat()' in SY) else '再現しない', {'header': sm, 'name_rule': 'datetime.date.today()（手元の日付）', 'time_rule': 'UTC'})

# ---- W114 校正腕のセッション数の内訳と下界（Gr2 L2・Cl3 軽10）
lo = FACTS['F']['data']['plans']['lower']; At = FACTS['A']['text']
W(114, 'Gr2 L2・Cl3 軽10', '転記行 A の校正腕は上界のセッション数 10〔機種 8・橋 2〕だけで、下界のセッション数と「機種 8」の内訳（32B が 2）が印字されていないか',
  '再現' if ('合計 10〔機種 8・橋 2〕' in At and lo['sessions'] == 9 and '3,600' not in At) else '一部再現', {'upper_sessions': up['sessions'], 'lower_sessions': lo['sessions'], 'upper_32B_sessions': up['rows']['32B']['sessions'], 'lower_32B_sessions': lo['rows']['32B']['sessions']})

# ---- W115 refuse 門 (c) の端点（Gr2 L3）
W(115, 'Gr2 L3', 'refuse 門の (c) が残存規模の最小と最大の二点だけで refuse 率の推移を見るか（登録の文言と一致するか）', '再現' if ('e0, e1 = int(idx[0]), int(idx[-1])' in CF and FAM['refuse_gate']['residual_ends'] == '全分母で残った規模の最小と最大') else '一部再現',
  {'spec_residual_ends': FAM['refuse_gate']['residual_ends']})

# ---- W116 README の次段（Gr2 L5）
W(116, 'Gr2 L5', '公開の README の段階 A の記述が草案6 までで止まっているか', '再現' if ('草案6' in RM and '草案8' not in RM and '草案7' not in RM) else '一部再現', {'草案6': '草案6' in RM, '草案7': '草案7' in RM, '草案8': '草案8' in RM})

# ---- W117 橋の 8B の同時要求数の交絡の開示（Ge2 中1）
W(117, 'Ge2 中1', '橋の 8B の L4 側で環境の差と同時要求数の差が交絡し、その開示が正本と草案8 (xiii)・§4 にあるか', '再現' if ('橋の 8B の L4 側では環境の差と同時要求数の差が交絡する' in D8 and '同時要求数の効果を環境の効果から分離したと書かない' in D8 and '同時要求数の効果を環境の効果から分離したと書かない' in TJ) else '一部再現',
  {'判定': '交絡は事実・開示あり（草案8 (xiii)・§4・正本 environment_rule）'})

# ---- W118 判定器の断片の本文（Ge2 軽3）
W(118, 'Ge2 軽3', '判定器の断片が最終試行の本文の全文を入れ、前置きの語の復唱を点検する器が無いか', '再現' if ('最終試行の本文の全文' in JF and '応答の本文が前置きを復唱すると腕が推測されうる' in JF and 'arms/panel' not in JF) else '一部再現',
  {'limit_stated_in_tool_docstring': '応答の本文が前置きを復唱すると腕が推測されうる' in JF})

# ---- W119 snapshot の名の照合（Ge1 中4・Gr1 C3・Gr2 C3）
try:
    import huggingface_hub
    from huggingface_hub import _snapshot_download as _sd
    sds = inspect.getsource(_sd); hfv = huggingface_hub.__version__; builds = 'os.path.join(storage_folder, "snapshots", commit_hash)' in sds
except Exception as ex:
    hfv, builds = 'import failed: %s' % ex, None
W(119, 'Ge1 中4・Gr1 C3・Gr2 C3', 'snapshot_download の戻り値の末尾が解いた完全な SHA になるか（Colab の実機では未確認か）', '一部再現' if builds else '検査不能',
  {'local_huggingface_hub': hfv, 'returns_snapshots_commit_hash': builds, 'boot_compares_basename': "if snap != rv['full']" in BOOT, '判定': '手元の版の作りでは照合が通る。Colab の実機の版では未確認（門0.5 が最初の実機）'})

# ---- W120 報告の埋め残しの走査（Ge1 軽6）
pp = os.path.join(SCR, 'w120-probe.md'); open(pp, 'w', encoding='utf-8', newline='\n').write('# 探り\n記入欄 〔日付〕 を残す。\n本報告のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。\n')
rc120, out120 = run([TOOL('report_lint.py'), pp, '--out', os.path.join(SCR, 'w120-lint.md')])
W(120, 'Ge1 軽6', '走査器が記入欄の埋め残し（〔 〕）を違反にして非零で終わるか', '再現' if (rc120 == 1 and '埋め残し' in out120) else '再現しない', {'rc': rc120, 'out': out120.strip()[-160:]})

# ---- W121 門0.5 の main と repo_head（Gr1 L6）
W(121, 'Gr1 L6', '起動器が門0.5 では main を許し、セッション記録に取り出した HEAD を書くか', '再現' if ("DATA_PHASES = ('pilot', 'pilot_rerun', 'main', 'bridge')" in BOOT and 'repo_head=HEAD' in BOOT) else '再現しない', {'commit_rule': T['sessions']['commit_rule'][:80]})

# ---- W122 様式門・refuse の分母（Gr1 L7・Gr2 L4）
W(122, 'Gr1 L7・Gr2 L4', '様式門と refuse 門 (c) の分母が書式外を含む n_ok で、運用の解釈 15・28 に登録どおりか', '再現' if ('書式外の試行も分母に入れ' in items[15] and '(c) の refuse 率の分母は n_ok' in items[28] and SG['denominator'] == 'n_ok') else '一部再現', {'判定': '登録どおり'})

# ---- W123 依頼文の label_precedence（Cl2 軽）
bparts = {nm: SRC('records/reviews/A/final/%s' % nm).count('label_precedence') for nm in sorted(os.listdir(os.path.join(REPO, 'records', 'reviews', 'A', 'final'))) if nm.startswith('bundle-A-final-part')}
W(123, 'Cl2 軽', '今回の依頼文が正本に無いキー label_precedence を名指すか', '再現しない' if (SRC('records/reviews/A/final/review-request-A-final.md').count('label_precedence') == 0 and 'label_precedence' not in json.dumps(FAM['confirm_rule'], ensure_ascii=False)) else '再現',
  {'request': 0, 'spec_v2.4': 'label_precedence' in json.dumps(FAM['confirm_rule'], ensure_ascii=False), 'bundle_parts': bparts, '判定': '束の中の草案6 の採否表（P9・§7）に過去の名として出る'})

# ---- 重い実験: W86・W87（到達の d0 と逆向き）
HF = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'hf-models-A.json')); Z, _ = z_map(HF); zs = np.array([Z[s] for s in T['sizes']]); z4 = Z['4B']; zspan = float(zs[-1] - z4); n = T['n_per_arm']
if a.skip_reach:
    W(86, 'Cl3 重大3(e)', '4B の差 d0 が大きい効果種ほど到達が下がるか（同じ対照で d0 だけ変える）', '検査不能', 'skipped')
    W(87, 'Cl3 重大3(c)', '余地のある向きだけで測り、逆向きの到達は多くの対比で低いか', '検査不能', 'skipped')
else:
    k = 0; r86 = []
    for pc0 in (0.2, 0.5, 0.8):
        for d0 in (-0.3, -0.15, 0.0, 0.15, 0.3):
            rA4 = pc0 + d0
            if not (0.0 < rA4 < 1.0):
                continue
            pc = np.full(len(zs), pc0); D = ME['delta'] * confirm_A.reach_direction(rA4); pt, cl = confirm_A.reach_treatment(pc, d0, D, zs, z4, zspan)
            s = confirm_A.simulate_cell(R, zs, n, pc, pt, a.B_reach, np.random.default_rng([ME['seed'], 86, k])); k += 1
            r86.append({'pc': pc0, 'd0': d0, 'rA4': round(rA4, 3), 'D': D, 'clipped': cl, 'reach': s['card_D1_holm_first'], 'clause_rate': s['clause_rate_among_fit'], 'undecidable': s['undecidable_censor']})
    se = lambda p: math.sqrt(max(p * (1 - p), 1e-12) / a.B_reach)
    lower_at_max = {}
    for pc0 in (0.2, 0.5, 0.8):
        rows_ = [x for x in r86 if x['pc'] == pc0]; base = next(x for x in rows_ if x['d0'] == 0.0); far = max(rows_, key=lambda x: abs(x['d0']))
        lower_at_max[str(pc0)] = {'base_reach': base['reach'], 'far_d0': far['d0'], 'far_reach': far['reach'], 'lower_beyond_2se': (base['reach'] - far['reach']) > 2 * math.hypot(se(base['reach']), se(far['reach']))}
    nlow = sum(v['lower_beyond_2se'] for v in lower_at_max.values())
    W(86, 'Cl3 重大3(e)', '4B の差 d0 が大きい効果種ほど到達が下がるか（同じ対照で d0 だけ変える・B=%d）' % a.B_reach, '再現' if nlow == 3 else ('一部再現' if nlow else '再現しない'), {'rows': r86, 'far_vs_zero': lower_at_max})
    k = 0; r87 = []
    rows_dr = [r for r in G['DR'] if r['delta'] != '0']
    for r in rows_dr:
        c = next(c_ for c_ in FAM['contrasts'] if c_['id'] == r['id']); bA = c['base_A_4B2507'] / c['base_n_A']; bB = c['base_B_4B2507'] / c['base_n_B']; d0 = bA - bB
        sl = r['ctrl_change_32B_minus_4B']; pc = np.clip(bB + sl * (zs - z4) / zspan, 0.001, 0.999); Dopp = -r['delta_value']
        pt, cl = confirm_A.reach_treatment(pc, d0, Dopp, zs, z4, zspan)
        s = confirm_A.simulate_cell(R, zs, n, pc, pt, a.B_reach, np.random.default_rng([ME['seed'], 87, k])); k += 1
        r87.append({'id': r['id'], 'trend': r['ctrl_trend'], 'room': r['card_D1_holm_first'], 'opposite': s['card_D1_holm_first'], 'clipped_opposite': cl})
    lower = sum(1 for x in r87 if (x['room'] - x['opposite']) > 2 * math.hypot(math.sqrt(max(x['room'] * (1 - x['room']), 1e-12) / BDR), se(x['opposite'])))
    higher = sum(1 for x in r87 if (x['opposite'] - x['room']) > 2 * math.hypot(math.sqrt(max(x['room'] * (1 - x['room']), 1e-12) / BDR), se(x['opposite'])))
    opp_types = {}
    for x in r87:
        opp_types.setdefault((x['id'].split(':', 1)[1], x['trend']), []).append(x['opposite'])
    meas_opp = {tr: sum(1 for (e, t_), ps in opp_types.items() if t_ == tr and confirm_A.at_least_one(ps) >= ME['threshold']) for tr in trends}
    W(87, 'Cl3 重大3(c)', '余地のある向きだけで測り、逆向きの到達は多くの対比で低いか（逆向きを B=%d で模擬）' % a.B_reach,
      '再現' if ('return 1.0 if rate_A_4B < 0.5 else -1.0' in CF and lower > len(r87) / 2) else ('一部再現' if 'return 1.0 if rate_A_4B < 0.5 else -1.0' in CF else '再現しない'),
      {'pairs': len(r87), 'opposite_lower_beyond_2se': lower, 'opposite_higher_beyond_2se': higher, 'measurable_types_room': {tr: lvl[tr]['types_measurable'] for tr in trends}, 'measurable_types_opposite': meas_opp, 'rows': r87})

# ---- 合成の実験: W80（facts を欠く集計）・W94（組み立て器の --gate）・W96（M7・M8）・W98（M9・M10）
if a.skip_synth:
    W(80, 'Cl1 中1', '--facts が任意で、到達の見込みの欄が「記録なし」に置き換わっても組み立てと走査が通るか', '一部再現' if all(c80.values()) else '再現しない', dict(c80, experiment='skipped'))
    W(94, 'Cl1 中5', '組み立て器の --gate の経路が合成の門の記録で止まり、実物の門の記録では通るか', '検査不能', 'skipped')
    W(96, 'Cl2 中4', '第一適合の順の変異（M7）が合成検査を通り、自己検査で止まるか。p* を min にする変異（M8）を合成検査が見分けるか', '検査不能', 'skipped')
    W(98, 'Cl3 中6', '注の期待が集計器の keep と札を読み、注の規則の変異（M9）と除外を当てはめに渡さない変異（M10・事前登録の後に足した）を合成検査が見分けるか', '検査不能', 'skipped')
else:
    s94 = os.path.join(SCR, 'w94'); shutil.rmtree(s94, ignore_errors=True); os.makedirs(s94)
    rcs, outs = run([TOOL('synth_A.py'), '--root', os.path.join(s94, 'synth'), '--runs', '1', '--mutations', 'none', '--keep', '--record', os.path.join(s94, 'synth-rec')])
    tag = 'synthA01'; root1 = os.path.join(s94, 'synth', 'run01'); recd = os.path.join(root1, 'records'); an = os.path.join(root1, 'out', 'analysis-%s.json' % tag)
    rcg, outg = run([TOOL('synth_gates_A.py'), '--root', os.path.join(s94, 'gates'), '--keep', '--record', os.path.join(s94, 'gates-rec')])
    gate_real = os.path.join(s94, 'gates', 'gates-pass', 'records', 'gate.json'); gate_syn = os.path.join(recd, 'gate-%s.json' % tag)
    rc1, o1 = run([TOOL('build_report_A.py'), '--draft', '1', '--analysis', an, '--gate', gate_syn, '--out', os.path.join(s94, 'report-synthgate.md'), '--force'])
    rc2, o2 = run([TOOL('build_report_A.py'), '--draft', '1', '--analysis', an, '--gate', gate_real, '--out', os.path.join(s94, 'report-realgate.md'), '--force'])
    rp2 = os.path.join(s94, 'report-realgate.md'); t2 = open(rp2, encoding='utf-8').read() if os.path.exists(rp2) else ''
    W(94, 'Cl1 中5', '組み立て器の --gate の経路が合成の門の記録で止まり、実物の門の記録（gate_A の出力）では通るか',
      '一部再現' if (rc1 != 0 and 'per_scenario' in o1 and rc2 == 0 and '門2（機械の転記）' in t2) else ('再現' if rc2 != 0 else '再現しない'),
      {'synth_run_rc': rcs, 'synth_gates_rc': rcg, 'synthetic_gate_record': {'rc': rc1, 'tail': o1.strip()[-200:]}, 'real_gate_record': {'rc': rc2, 'gate_lines': [l for l in t2.split('\n') if l.startswith('- 門2（機械の転記）') or l.startswith('N1:') or l.startswith('SK:')][:4], 'tail': o2.strip()[-200:]},
       'verify_reflection_build_report_call_has_gate': any('--gate' in l_ for l_ in SRC('tools/verify_reflection_impl_A.py').split('\n') if "tool('build_report_A.py')" in l_)})
    # W80 の実験: 同じ合成の置き場で --facts を欠いて集計し、組み立てと走査を通す
    nf = os.path.join(s94, 'nofacts'); os.makedirs(nf, exist_ok=True); idp = os.path.join(recd, 'identity-%s.json' % tag)
    cmd = [TOOL('analyze_A.py'), '--tag', tag, '--root', root1, '--anchor-tag', tag + '-anchor2', '--bridge-tag', tag + '-bridge', '--api-tag', tag + '-api', '--style', os.path.join(recd, 'style-%s.json' % tag),
           '--gate', gate_syn, '--calib', os.path.join(recd, 'calib-%s.json' % tag), '--out', os.path.join(nf, 'analysis-%s' % tag), '--force', '--B-measurable', '4', '--synth-nonconverged', 'SK:Lneg~Onull',
           '--facts', os.path.join(nf, 'no-such-design-facts.json')] + (['--identity', idp] if os.path.exists(idp) else ['--no-identity'])
    rca, outa = run(cmd); AJ = runs_A.read_json(os.path.join(nf, 'analysis-%s.json' % tag)) if rca == 0 else {}
    rcb, outb = run([TOOL('build_report_A.py'), '--draft', '1', '--analysis', os.path.join(nf, 'analysis-%s.json' % tag), '--out', os.path.join(nf, 'report.md'), '--force']) if rca == 0 else (None, '')
    tb = open(os.path.join(nf, 'report.md'), encoding='utf-8').read() if os.path.exists(os.path.join(nf, 'report.md')) else ''
    W(80, 'Cl1 中1', '--facts が任意で、到達の見込みの欄が「記録なし」に置き換わっても組み立てと走査が通るか（合成の走 1 の置き場で facts を欠いて集計）',
      '再現' if (all(c80.values()) and rca == 0 and AJ.get('reach_note') is None and 'no_facts' not in ' '.join(AJ.get('dev_marks') or []) and rcb == 0 and '（到達の見込みの記録なし）' in tb) else '一部再現',
      dict(c80, analyze_rc=rca, reach_note=AJ.get('reach_note'), dev_marks=AJ.get('dev_marks'), missing=AJ.get('missing'), report_rc=rcb, report_has_fallback='（到達の見込みの記録なし）' in tb, report_tail=(outb or '').strip()[-160:]))
    # W96・W98: 合成検査の写しに変異 M7〜M10 を入れる
    k0 = 'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))'; assert SY.count(k0) == 1
    s = SY.replace(k0, 'sys.path.insert(0, %r)' % os.path.join(REPO, 'tools')); i0 = s.index('MUTS = ['); j0 = s.index('\n\n\ndef make_mutant')
    NEW = ("MUTS = [('M7', 'tools/confirm_A.py', [(\"(('interpretation_clause', clause), ('iut_not_rejected', not star),\", \"(('iut_not_rejected', not star), ('interpretation_clause', clause),\")], [1], '第一適合の順の先頭二つを入れ替える'),\n"
           "        ('M8', 'tools/confirm_A.py', [(\"p_star=(max(float(r['p']), p_pt) if same else R.p_star_mismatch)\", \"p_star=(min(float(r['p']), p_pt) if same else R.p_star_mismatch)\")], [1], 'p* を max から min に'),\n"
           "        ('M9', 'tools/analyze_A.py', [(\"        if (kidx[-1] - kidx[0] + 1) != len(kidx) or ends:\\n\", \"        if (kidx[-1] - kidx[0] + 1) != len(kidx):\\n\")], [1], '残存の非連続の注から端の欠けの条件を外す'),\n"
           "        ('M10', 'tools/analyze_A.py', [(\"r, f = evaluate(R, c, X, ke); RES.append(r)\", \"r, f = evaluate(R, c, X, None); RES.append(r)\")], [1, 2], '主の当てはめに測定不能・錨帯の除外を渡さない（事前登録の後に足した）')]")
    s = s[:i0] + NEW + s[j0:]; sp = os.path.join(SCR, 'synth_A_mutations_M7_M10.py'); open(sp, 'w', encoding='utf-8', newline='\n').write(s)
    s96 = os.path.join(SCR, 'w96'); shutil.rmtree(s96, ignore_errors=True)
    rcm, outm = run([sp, '--root', s96, '--runs', '1', '--mutations', 'M7,M8,M9,M10', '--keep'])
    MU = {m.group(1): {'mismatches': int(m.group(2)), 'detected': m.group(3) == '見分けた'} for m in re.finditer(r'\[synth\] 変異 (M\d+)（.*?）: 不一致 (\d+)・(見分けた|見分けなかった)', outm)}   # 括弧の入れ子を許す
    for mn, runs_ in (('M7', (1,)), ('M8', (1,)), ('M9', (1,)), ('M10', (1, 2))):
        if mn in MU:
            MU[mn]['outputs_exist'] = all(os.path.exists(os.path.join(s96, 'mut-%s-run%02d' % (mn, rn), 'out', 'analysis-synthA%02d.json' % rn)) for rn in runs_)
    base = runs_A.read_json(os.path.join(s96, 'run01', 'out', 'analysis-%s.json' % tag)) if os.path.exists(os.path.join(s96, 'run01', 'out', 'analysis-%s.json' % tag)) else {'contrasts': []}
    m7p = os.path.join(s96, 'mut-M7-run01', 'out', 'analysis-%s.json' % tag); m7 = runs_A.read_json(m7p) if os.path.exists(m7p) else {'contrasts': []}
    lab_diff = [(x['id'], x['row'], x['label'], y['label']) for x, y in zip(base['contrasts'], m7['contrasts']) if x['row'] == y['row'] and x['label'] != y['label']]
    row_diff = sum(1 for x, y in zip(base['contrasts'], m7['contrasts']) if x['row'] != y['row'])
    rcst, outst = run([os.path.join(s96, 'mutant-M7', 'tools', 'confirm_A.py'), '--selftest'])
    W(96, 'Cl2 中4', '第一適合の順の変異（M7）が合成検査を不一致 0 で通り、自己検査で止まるか。p* を min にする変異（M8）を合成検査が見分けるか',
      '再現' if (MU.get('M7', {}).get('mismatches') == 0 and lab_diff and rcst != 0) else '一部再現',
      {'synth_rc': rcm, 'mutations': MU, 'M7_same_row_label_changed_n': len(lab_diff), 'M7_same_row_label_changed': lab_diff[:8], 'M7_row_changed': row_diff, 'M7_selftest_rc': rcst, 'M7_selftest_tail': outst.strip()[-160:],
       'compare_checks_label': "x['label'] !=" in SY.split('def compare(')[1].split('\ndef ')[0],
       'M8_why': {'scale_only_contrasts_in_run1': sum(1 for x in base['contrasts'] if x['label'] == T['families']['A_slope']['confirm_rule']['labels']['scale_only']),
                  'of_which_same_direction': sum(1 for x in base['contrasts'] if x['label'] == T['families']['A_slope']['confirm_rule']['labels']['scale_only'] and (x.get('result') or {}).get('same'))}})
    reads_out = ("if x['label'] == L['confirmed']:" in SY and "r['keep'][0]" in SY); m10 = MU.get('M10') or {}
    b10 = [runs_A.read_json(os.path.join(s96, d_, 'out', 'analysis-synthA01.json')) for d_ in ('run01', 'mut-M10-run01')] if m10.get('outputs_exist') else None
    keep10 = sum(1 for x, y in zip(b10[0]['contrasts'], b10[1]['contrasts']) if x['result'].get('keep') != y['result'].get('keep')) if b10 else None
    row10 = sum(1 for x, y in zip(b10[0]['contrasts'], b10[1]['contrasts']) if x['row'] != y['row'] or x['label'] != y['label']) if b10 else None
    W(98, 'Cl3 中6', '注の期待が集計器の keep と札を読み、注の規則の変異（M9）と除外を当てはめに渡さない変異（M10・事前登録の後に足した）を合成検査が見分けるか',
      '再現' if (reads_out and m10.get('outputs_exist') and m10.get('mismatches') == 0) else ('一部再現' if reads_out else '再現しない'),
      {'expected_notes_reads_output_keep_and_label': reads_out, 'M9': MU.get('M9'), 'M10': m10, 'M10_run1_keep_changed_contrasts': keep10, 'M10_run1_row_or_label_changed': row10, 'synth_tail': outm.strip()[-300:]})

# ---- 追跡中のファイルが変わっていないこと
STATUS1 = subprocess.run(['git', '-C', REPO, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout
ROWS.sort(key=lambda r: r['num'])
counts = {v: sum(1 for r in ROWS if r['verdict'] == v) for v in ('再現', '一部再現', '再現しない', '検査不能')}
OUTP = a.out or os.path.join(REPO, 'records', 'reviews', 'A', 'final', 'verification-final-A')
SUM = {'kind': 'verify_review_final_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'head': HEADC, 'contrasts_sha16': local16,
       'prereg': 'records/reviews/A/final/preregistration-reproduction-A-final.md', 'B_reach': a.B_reach, 'skip_reach': a.skip_reach, 'skip_synth': a.skip_synth, 'counts': counts,
       'tracked_changes_before': STATUS0, 'tracked_changes_after': STATUS1, 'seconds': round(time.time() - T0, 1), 'rows': ROWS,
       'clause': '合成の件数は検査のための人工値であり、いかなる読みにも用いない。本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(SUM, open(OUTP + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=str)
esc = lambda s_: str(s_).replace('|', '／').replace('\n', ' ')
M = ['# 凍結前の最終検分の所見の再現（機械生成・`tools/verify_review_final_A.py` %s・%s UTC）' % (VERSION, SUM['generated_utc']), '',
     '- 事前登録: `records/reviews/A/final/preregistration-reproduction-A-final.md`（SHA-256 は `verify.log` の [prereg] の行・再現の前に記帳）。',
     '- 対象: コミット %s・正本 SHA16 %s。票の略は `provenance.md`。' % (HEADC[:12], local16),
     '- 判定の数: 再現 %d・一部再現 %d・再現しない %d・検査不能 %d（全 %d 項）。所要 %.0f 秒。到達の模擬の B=%d。' % (counts['再現'], counts['一部再現'], counts['再現しない'], counts['検査不能'], len(ROWS), SUM['seconds'], a.B_reach),
     '- 追跡中のファイルの変更: 実行前 %s・実行後 %s（リポジトリは書き換えていない）。' % (repr(STATUS0.strip()) if STATUS0.strip() else 'なし', repr(STATUS1.strip()) if STATUS1.strip() else 'なし'), '',
     '| W | 所見（票） | 確かめたこと | 判定 | 詳細 |', '|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s |' % (r['id'], r['findings'], esc(r['desc']), r['verdict'], esc(json.dumps(r['detail'], ensure_ascii=False, default=str))[:1400]) for r in ROWS]
M += ['', '本記録は再現の結果だけを書く。採否と区分は採否表（`adoption-table-A-final.md`）で決める。', '', SUM['clause']]
open(OUTP + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('written %s.{md,json} counts %s seconds %.0f tracked-changes %s' % (OUTP, counts, SUM['seconds'], repr(STATUS1.strip())))
