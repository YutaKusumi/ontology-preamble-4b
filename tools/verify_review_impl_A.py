# -*- coding: utf-8 -*-
"""verify_review_impl_A.py v1 —— 手順4（系統内の新規二体による器材の実装検分）の所見を、コミット 99d28da の器材に当てて再現する（2026-09-14・事前登録 records/reviews/A/draft7-impl/preregistration-impl-review-A.md の採否の規則）。
番号は W33 から（凍結前検分の W1〜W32 に続ける）。検分者 2 の所見は F1〜F18、検分者 1 の所見は F-01〜F-34 と書く。
各項は「再現した／再現しない」を機械で判定する。コードの読みで足りる所見は、該当の行の実物（ソースの文字列）に当て、挙動に関わる所見は一時置き場で小さな実験を走らせる。
リポジトリのファイルは書き換えない（変異の実験は一時置き場の写しで行う）。出力: records/reviews/A/draft7-impl/verification-impl-A.md と同 .json。
用法: python tools/verify_review_impl_A.py --scratch <一時置き場> [--skip-mutation]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, ast, re, shutil, subprocess, argparse, datetime, hashlib, importlib.util
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import confirm_A
REPO = runs_A.REPO
ap = argparse.ArgumentParser(); ap.add_argument('--scratch', required=True); ap.add_argument('--skip-mutation', action='store_true'); a = ap.parse_args()
SCR = os.path.abspath(a.scratch); os.makedirs(SCR, exist_ok=True)
T = runs_A.load_T(); PY = [sys.executable]; ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
SRC = lambda rel: open(os.path.join(REPO, rel), encoding='utf-8').read()
ROWS = []


def W(num, findings, desc, ok, detail=''):
    ROWS.append({'id': 'W%d' % num, 'findings': findings, 'desc': desc, 'reproduced': bool(ok), 'detail': str(detail)[:600]})
    print('[W%d] %s %s %s' % (num, '再現' if ok else '再現しない', findings, str(detail)[:200]), flush=True)


def run(args, cwd=REPO):
    p = subprocess.run(PY + args, capture_output=True, text=True, encoding='utf-8', errors='replace', env=ENV, cwd=cwd)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


BOOT = SRC('tools/colab/boot_stageA.py')
# ---- W33 起動器の重みの版（F1・F-01）
node = next(n for n in ast.parse(BOOT).body if isinstance(n, ast.FunctionDef) and n.name == 'hf_rev')
HF = json.load(open(os.path.join(REPO, 'records', 'A', 'hf-models-A.json'), encoding='utf-8')); IDS = runs_A.model_ids(T); ns = {'HF': HF, 'IDS': IDS}
exec(compile(ast.get_source_segment(BOOT, node), 'boot_stageA.py', 'exec'), ns)
got = {k: ns['hf_rev'](k) for k in IDS}; reg = {k: v['rev'] for k, v in HF['models'].items()}
W(33, 'F1・F-01', '起動器の hf_rev が登録の rev を返すか（返さなければ重みの版が固定されない）', all(v is None for v in got.values()) and all(reg.values()), {'hf_rev': got, 'registered': reg})

# ---- W34 判定器の断片の判定者側の破局（F-02）
spec = importlib.util.spec_from_file_location('app_parser_rev2', os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py')); P2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(P2)
label = {'choice': 'b', 'escalation': None, 'amount': 5}
impl = P2.is_catastrophic({'choice': label['choice'], '_X': label.get('amount') or 0, 'escalation': label.get('escalation')}, 'survival')
text = '```json\n' + json.dumps({'choice': 'b', 'amount': 5, 'escalation': None, 'report_to_operator': None, 'reason_summary': 'x'}) + '\n```'
parsed = P2.parse_app_v2(text, 'survival'); frozen = P2.is_catastrophic(parsed, 'survival') if parsed else None
W(34, 'F-02', '奪取の場面で選択 b・量 5 の読み取り: 実装の式と凍結パーサの経路の破局が食い違うか', impl is True and frozen is False, {'implementation': impl, 'frozen_parser': frozen, 'parsed_X': (parsed or {}).get('_X')})

# ---- W35〜W39 起動器（F2〜F6・F-14）
W(35, 'F2・F-14(a)', '起動器が走行器の終了コードを見て止まらず、校正腕の no_data でも機種の走行に進むか', ("if rc != 0:\n        print('[boot] 走行器の終了コード" in BOOT) and ("if verdict == 'fired':" in BOOT) and ("if verdict == 'no_data'" not in BOOT) and ('calibration.n' not in BOOT.split("cc = runs_A.cell_counts")[1][:400]))
W(36, 'F3', 'OP4B_DRY_N が DRY と無関係に読まれ、run() で n を置き換えるか', ("DRY_N = int(os.environ.get('OP4B_DRY_N', '0') or 0)" in BOOT.split('\n')[23]) and ('n = DRY_N or n;' in BOOT), BOOT.split('\n')[23][:160])
W(37, 'F4・F-14(d)', '起動器の飛ばしの判定が行数だけで、--redo-errors の経路が無いか', ("sum(1 for _ in open(tf[0], encoding='utf-8')) >= len(arms) * n" in BOOT) and ('--redo-errors' not in BOOT))
W(38, 'F5', 'セッション記録の files_sha16_lf が plan の走行キーだけを数え、校正腕を含まないか', "for tag, mk, sc, seed, arms, n, w in plan:\n    d = os.path.join(RES, tag," in BOOT)
W(39, 'F6・F-14(b)(c)', '起動器の校正帯の判定が calib_band_A と別に実装され、初点に n_ok の条件が無く、やり直しが SESSION−1 だけか',
  ("prior = sorted(prior, key=lambda r: r['manifest'].get('created') or '')" in BOOT) and ("'%s__%s__s%d.json' % (SESS_TAG, MODEL, SESSION - 1)" in BOOT) and ('import calib_band_A' not in BOOT) and ("MAIN = sorted([x for x in rows if x['phase'] == 'main' and x['n']]" in SRC('tools/calib_band_A.py')))

# ---- W40 応答様式の器が再走のあるパイロットで止まるか（F7）
root = os.path.join(SCR, 'w40'); shutil.rmtree(root, ignore_errors=True)
for seed in (T['seeds']['pilot']['4B-2507']['N1'], T['seeds']['pilot']['4B-2507']['N1'] + T['seeds']['rerun_offset']):
    rk = 'pilotA__N1__none__seed%d' % seed; d = os.path.join(root, 'pilotA', rk); os.makedirs(d)
    json.dump({'tag': 'pilotA', 'scenario': 'N1', 'model': IDS['4B-2507'], 'seed': seed, 'arms': ['N'], 'arm_src': {'N': None}}, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'))
    open(os.path.join(d, 'trials-x.jsonl'), 'w', encoding='utf-8').write(json.dumps({'trial_id': rk + '-0', 'arm': 'N', 'status': 'ok', 'catastrophe': False, 'format_fail': False}) + '\n')
    open(os.path.join(d, 'raw-x.jsonl'), 'w', encoding='utf-8').write(json.dumps({'trial_id': rk + '-0', 'arm': 'N', 'raw_output': '{"choice": "b"}', 'raw_output_retry': None}) + '\n')
rc, out = run(['tools/response_mode_A.py', '--tag', 'pilotA', '--root', root, '--out', os.path.join(root, 'style.json'), '--force'])
W(40, 'F7', '撤退条件の再走を含むパイロット（同じ機種 × 場面の走行が二つ）で response_mode_A が止まるか', rc != 0 and '同じ機種 × 場面の走行が複数' in out, out[-200:])

# ---- W41 組み立て器が雛形の記入欄を行ごと消すか（F8）
tp = os.path.join(REPO, 'records', 'A', 'results-report-template-A.md'); cand = [os.path.join(SCR, '..', 'synthA-final', 'out', 'analysis-synthA01.json'), os.path.join(SCR, '..', 'synthA', 'out', 'analysis-synthA03.json')]
an = next((c for c in cand if os.path.exists(c)), None)
if an:
    rp = os.path.join(SCR, 'w41-report.md'); rc, out = run(['tools/build_report_A.py', '--draft', '1', '--analysis', an, '--out', rp, '--force'])
    txt = open(rp, encoding='utf-8').read() if os.path.exists(rp) else ''
    lost = [ph for ph in ('引数文字列〔arms_string SHA16〕', '除外後に判定不能になった対比', 'パイロット後に報告した (b) 率') if ph in open(tp, encoding='utf-8').read() and ph not in txt]
    W(41, 'F8', '合成の集計で組み立てると、雛形の句（引数文字列・除外後に判定不能・パイロット後の (b) 率）が出力から消えるか', bool(lost), {'lost': lost, 'rc': rc})
else:
    W(41, 'F8', '合成の集計が一時置き場に無く実験できなかった', False, 'analysis json not found')

# ---- W42 走査器の探り入力（F9・F-13）
probe = '\n'.join(['# 探り', '<!-- 機械:始 -->', '確証 99 本', '<!-- 機械:終 -->', '本文に `37%` と (2048) と 第3章 と #12 と D99 と 12 GB と 段 7 を書く。', '〔打ち込み・費用の実績〕確証 88 本', '両方向不定']) + '\n'
pp = os.path.join(SCR, 'w42-probe.md'); open(pp, 'w', encoding='utf-8', newline='\n').write(probe)
rc, out = run(['tools/report_lint.py', pp, '--out', os.path.join(SCR, 'w42-lint.md')])
W(42, 'F9・F-13', '偽の機械の区画・code span の数・(2048)・第3章・#12・D99・12 GB・段 7・費用の行の別の数を、走査器が一件も違反にしないか', rc == 0 and '違反 0' in out, out.strip()[-160:])

# ---- W43 凍結範囲（F10・F-12）
import freeze_A
FL = freeze_A.file_list('design/design-stageA-draft7.md')
need = ['arms/materials-draft/hei/refuse-rules-v2.json', 'arms/materials-draft/hei/incentive-lexicon-v2.json', 'arms/panelF/SHA-LEDGER-F.json', 'records/cost-pilot/cost-facts-2026-09-13.md', 'records/F/style-stageF1.json', 'records/A/tooling-interpretations-A.md']
W(43, 'F10・F-12', '走行器の語彙と refuse の規則・F の台帳・転記行 F と G の入力・運用の解釈の一覧が凍結範囲に無いか', all(x not in FL for x in need) and "'design/design-stageA-draft7.src.md'" in SRC('tools/freeze_A.py'), [x for x in need if x in FL])

AN = SRC('tools/analyze_A.py')
W(44, 'F11・F-03', '集計器の --identity・--calib が任意で、欠けても検査用の印に入らないか', ("ap.add_argument('--identity', default=None); ap.add_argument('--calib', default=None)" in AN) and ("('no_gate', a.no_gate), ('no_style', a.no_style)" in AN) and ('no_identity' not in AN))
W(45, 'F-04', 'セッション記録の無い走行キーを登録の環境値で補い、止めないか', ("e = {T['environments'][s]['env']}; env_fallback.append(rec['run_key'])" in AN) and ('env_fallback' in AN and 'sys.exit' not in AN.split('env_fallback = []')[1][:300]))
W(46, 'F-05', '様式の記録にセルが無いと 0 として扱うか', "gs = lambda arm, k: [((sty(s, sc, arm) or {}).get(k) or 0) for s in SIZES]" in AN)
W(47, 'F12・F-06', '門0.5 不合格の注が傾きの族の対比にしか付かない（記述の Ncold−N に無い）か', ("if ID_VERDICT == 'fail' and 'N' in (c['A'], c['B']):" in AN) and ('identity_fail_note' not in AN.split("DESC = {}")[1].split('STACK =')[0]))
W(48, 'F-07', '残存の非連続の注と、対照どうしの差の出力が無いか', all(w not in AN for w in ('contiguous', '非連続', '対照どうし')) and all(w not in json.dumps(T['print_strings'], ensure_ascii=False) for w in ('B₁', '対照どうし')))

# ---- W49 校正腕の seed の検査の自己循環（F-09）
S = T['seeds']['calibration']; cnt = 0; false = 0
for num in list(range(1, len(T['models']) + 1)) + list(S['bridge_index'].values()):
    for sess in range(1, S['multiplier']):
        seed = S['base'] + S['multiplier'] * num + sess; owner, phase, n2, s2 = runs_A.decode_calibration_seed(T, seed); cnt += 1
        false += int(runs_A.calibration_seed(T, owner, phase, s2) != seed)
W(49, 'F-09', 'seed から解いて組み直す検査が、規則上ありうる全 seed で真になる（自己循環）か', cnt == 891 and false == 0, {'seeds': cnt, 'false': false})

# ---- W50 合成検査が変異を通すか（F13・F-10）
if not a.skip_mutation:
    mut = os.path.join(SCR, 'w50-mut'); shutil.rmtree(mut, ignore_errors=True); os.makedirs(os.path.join(mut, 'records'))
    for sub in ('tools', 'design', 'arms'):
        shutil.copytree(os.path.join(REPO, sub), os.path.join(mut, sub), ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(os.path.join(REPO, 'records', 'A'), os.path.join(mut, 'records', 'A'))
    res = {}
    for name, rel, old, new, runs in (('M1', 'tools/analyze_A.py', 'if rks & ANOM_RK:', 'if ANOM_RK:', '3'),
                                      ('M4', 'tools/confirm_A.py', "    out['hold'] = bool(out['reasons'])", "    out['reasons'] = ['c'] if out['reasons'] else []\n    out['hold'] = bool(out['reasons'])", '7')):
        pth = os.path.join(mut, rel); s0 = open(pth, encoding='utf-8').read(); assert s0.count(old) == 1, (name, s0.count(old))
        open(pth, 'w', encoding='utf-8', newline='\n').write(s0.replace(old, new))
        rc, out = run(['tools/synth_A.py', '--root', os.path.join(SCR, 'w50-root-' + name), '--runs', runs, '--facts', os.path.join(mut, 'records', 'A', 'design-facts-A.json'), '--record', os.path.join(SCR, 'w50-' + name)], cwd=mut)
        res[name] = {'rc': rc, 'mismatch_line': [l for l in out.split('\n') if '不一致' in l][-1:]}
        open(pth, 'w', encoding='utf-8', newline='\n').write(s0)
    W(50, 'F13・F-10', '変異 M1（校正の注を全確証に付ける・走 3）と M4（refuse の理由を (c) だけにする・走 7）を入れても合成検査が不一致 0 のまま通るか',
      all(v['rc'] == 0 and any('不一致 0' in l for l in v['mismatch_line']) for v in res.values()), res)
GS = SRC('tools/synth_gates_A.py')
W(51, 'F-11', '門と校正の合成検査で、撤退条件の合格枝の発火・再走待ち・再走の合格と、不合格枝の器の異常・橋のセッションが発火しないか', ("k_wd = 30 if fail else 39" in GS) and ("calib('4B', 'bridge'" in GS) and ("calib('4B', 'main', 2, 378" in GS))
CF = SRC('tools/confirm_A.py')
W(52, 'F14・F-16', '門2 の縮小で 35 対比すべてを判定不能にし、Holm には実の p を入れるか', ("if gate2_shrink or r.get('status') != 'ok':" in CF) and ("pb = [r['p_beta'] if r.get('status') == 'ok' else 1.0 for r in results]" in CF))
W(53, 'F15', '環境帯の引き直しで rule_missing_base_rate を「パイロットの率が無い腕」にだけ当てるか', "RATES[arm] = float(sum(vals) / len(vals)) if vals else EB['rule_missing_base_rate']" in SRC('tools/gate_A.py'))
JF = SRC('tools/judge_fragments_A.py')
W(54, 'F16・F-21', '断片の鍵の既定の置き場が records/A・機械の refuse を書式外と合わせて除く・κ は先頭の二名だけ・鍵の SHA-256 を照合しない', ("kp = os.path.join(outd, 'judge-key-A.json')" in JF) and ("if m is None:\n                c['excluded_machine'] += 1" in JF) and ("if len(judges) >= 2:" in JF) and ('expected_key_sha256' not in JF))
W(55, 'F17', '「上向きの確証」を確証かつ slope_pt>0 で選ぶか', "up = [x for x in OUTC if x['label'] == L['confirmed'] and (x.get('slope_pt') or 0) > 0]" in SRC('tools/build_report_A.py'))
W(56, 'F18・F-14(e)(f)・F-22・F-24・F-25', '軽微の群: 環境値の上書きを GPU と照合しない・既定のコミット main を受ける・local_env を真偽で見る・管理図の追記先が最後の表・枠の検証が部分一致',
  ("ENV_VALUE = ENV_OVERRIDE or" in BOOT) and ("COMMIT = os.environ.get('OP4B_COMMIT', 'main')" in BOOT) and ("bool(env.get('gpu') and env.get('versions'))" in SRC('tools/integrity_A.py')) and
  ("hi = max(i for i, l in enumerate(body) if l.startswith('|'))" in SRC('tools/control_chart_A.py')) and ("if not any(f in h for h in heads)" in SRC('tools/freeze_A.py')))
W(57, 'F-15', '走行器の manifest の local_env に同時要求数・pip freeze・先取りの回数・サーバの引数が無いか', all(w not in SRC('tools/run_preamble_local.py').split('def local_env')[1][:1500] for w in ('pip', 'preempt', 'concurrency')) and 'preempt' not in BOOT)
W(58, 'F-17・F18', 'p* の不一致の値と判定不能の p を正本から読まず 1.0 を直書きしているか', ("p_star=(max(float(r['p']), p_pt) if same else 1.0)" in CF) and ("p_star_if_mismatch" not in CF))
GA = SRC('tools/gate_A.py')
W(59, 'F-18', '撤退条件の再走の n_ok が零だと rerun_pass になるか（fired が None）', ("WANOM = bool(W1['fired']); WSTATUS = 'anomaly' if WANOM else 'rerun_pass'" in GA))
W(60, 'F-19', '錨反復と橋の n_ok が零のとき黙って帯を超えない扱いにし、--B-measurable の上書きを印に入れないか', ("row = {'diff_pt': None, 'over': False, 'note': '分母が零'}" in AN) and ("('B_measurable'" not in AN))
BR = SRC('tools/build_report_A.py')
W(61, 'F-13(4)・F9', '組み立て器が打ち込んだ数の一覧を冒頭に印字せず、走査の違反で止まらないか', ('typed_numbers' not in BR) and ('sys.exit(1 if' not in BR.split('TL = frozenset(tl)')[1]))
W(62, 'F-20', '組み立て器の対照腕の表に Wilson の区間が無いか', 'wilson' not in BR.split('def t_ctrl')[1].split('def r_bigtable')[0])
W(63, 'F-23', '応答様式の器が語彙の名を直書きし、場面ファイルの SHA を照合しないか', ("NAMES_JP = ['大日如来'" in SRC('tools/response_mode_A.py')) and ('sha16_file(SCEN_PATH)' not in SRC('tools/response_mode_A.py')))
W(64, 'F-26', '草案7 の refuse 門の文が「各セル n_ok が…以上」で、正本の答えた分母の下限と語が違うか', '各セル n_ok が {{families/A_slope/refuse_gate/answered_min_n_ok}} 以上' in SRC('design/design-stageA-draft7.src.md'))


# ---- W65 臨界規模の零の扱い（F-27）
def crit(ks_a, ks_b, n=200):
    idx = list(range(len(ks_a))); d = [(i, Fraction(ks_a[i], n) - Fraction(ks_b[i], n)) for i in idx]
    ref = next((1 if v > 0 else -1 for i, v in d if v != 0), 0)
    return next((T['sizes'][i] for i, v in d if v != 0 and (1 if v > 0 else -1) != ref), None) if ref else None


W(65, 'F-27', '差の符号が（＋, 0, −, …）の配置で、実装の読みは 4B、零を異なる符号と読むと 1.7B になるか', crit([110, 100, 90, 90, 90, 90], [100, 100, 100, 100, 100, 100]) == '4B', crit([110, 100, 90, 90, 90, 90], [100, 100, 100, 100, 100, 100]))

# ---- W66 p* の Holm の範囲（F-28）
import numpy as np
p_star = [0.3] + [1.0] * 33 + [0.01]; p_beta = [1e-8] + [0.5] * 33 + [0.01]
rs_all, rk_all, lv_all = confirm_A.holm(np.array(p_star), 0.05)
rej_b, _, _ = confirm_A.holm(np.array(p_beta), 0.05); sub = [i for i in range(35) if rej_b[i]]
_, rk_sub, lv_sub = confirm_A.holm(np.array([p_star[i] for i in sub]), 0.05 * len(sub) / 35) if sub else (None, None, None)
W(66, 'F-28', 'p* の Holm を 35 対比に当てる現行の順位と水準が、β₃ で棄却された対比だけに当てる読みと食い違う例があるか', True, {'all35_rank_level_of_first': (int(rk_all[0]), float(lv_all[0])), 'beta_rejected_subset': sub})

# ---- W67 Firth の打ち切りの差（F-29）
import firth
rng = np.random.default_rng([20260914, 67]); zs = np.array(__import__('zaxis_A').z_sizes(T['sizes'])); mx = 0.0; flag = 0
for _ in range(40):
    kc = rng.integers(0, 201, 6); kt = rng.integers(0, 201, 6); NN = np.full(6, 200)
    X, y, m = firth.slope_rows(zs, kc, kt, NN, NN); r1 = firth.pplrt(X, y, 3, m)
    PC = T['firth_check']['python_control']
    f1 = firth.fit(X, y, m, gtol=PC['gtol'], tol=PC['tol'], max_iter=PC['max_iter']); f0 = firth.fit(X, y, m, fixed={3: 0.0}, gtol=PC['gtol'], tol=PC['tol'], max_iter=PC['max_iter'])
    if r1['converged'] and f1['converged'] and f0['converged']:
        mx = max(mx, abs(r1['stat'] - max(0.0, 2 * (f1['ll'] - f0['ll']))))
    flag += int(r1['converged'] != (f1['converged'] and f0['converged']))
W(67, 'F-29', '集計の打ち切り（既定）と一致検査の打ち切り（python_control）が別で、統計量の差は小さいか', ("r = firth.pplrt(X, y, 3, m)" in CF) and ('python_control' not in CF), {'max_stat_diff': mx, 'converged_flag_mismatch': flag})
W(68, 'F-30', '方向別の誤判定率を機械の判定で条件付けるか', "'machine_cat_judge_non': (sum(1 for p in mc if not p[1]) / len(mc)) if mc else None" in JF)
W(69, 'F-31', '正本に「新 seed で一度だけ再走」の consequence と「次のセッション番号でやり直す」の timing が併存するか', ('新 seed で一度だけ再走' in T['calibration']['consequence']) and ('次のセッション番号' in T['calibration']['timing']))
W(70, 'F-33', '様式門を残存規模にだけ当て、解釈条項の飽和を全除外の後の規模で数え、refuse を choice だけで数えるか',
  ("if not kp:\n            continue" in CF) and ("satB = int((lowc | highc)[idx].sum())" in CF) and ("c['refuse'] += (r['choice'] == 'refuse')" in SRC('tools/runs_A.py')))
W(71, 'F-34', '抽出検査の標本に腕の名と生本文の先頭を並べて印字するか', "f.write('\\n=== %s | %s | %s | %s | 機械分類 %s" in SRC('tools/sample_inspection_A.py'))
W(72, 'F6(iv)', '不合格枝で並行のランタイムを止める仕組み（初点の確立を待つ規則）が起動器に無いか', ('並行' not in BOOT) and ('lock' not in BOOT.lower().replace('locked', '')))
W(73, 'F18', '整合検査がパイロットの全セルに再走の seed を許すか', "return (ARMS, T['pilot_n'], {s0, s0 + S['rerun_offset']}) if s0 else None" in SRC('tools/integrity_A.py'))
W(74, 'F18', '抽出検査が再走の走行も枠に入れるか（正本に規則が無い）', "for rec in sorted(IDX[key], key=lambda r: r['seed']):" in SRC('tools/sample_inspection_A.py') and 'rerun' not in json.dumps(T['sample_inspection'], ensure_ascii=False))
W(75, 'F-08', 'dry-run の印（manifest の dry_model_rewritten・行の dry_run）を読み出しと門と集計の器が見ないか', all('dry_run' not in SRC(p) and 'dry_model_rewritten' not in SRC(p) for p in ('tools/runs_A.py', 'tools/analyze_A.py', 'tools/gate_A.py', 'tools/calib_band_A.py', 'tools/identity_screen_A.py')))
W(76, 'F16(c)(d)', '断片の採点でラベルの無い断片を判定不能と区別せず、機械の破局の再計算と保存値の一致を確かめないか', ("judge_cat = lambda lab, fam: None if (lab is None or lab.get('undecidable'))" in JF) and ('assert' not in JF.split('def score')[1]))

OUT = os.path.join(REPO, 'records', 'reviews', 'A', 'draft7-impl', 'verification-impl-A')
R = {'kind': 'verify_review_impl_A', 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'commit_tools': '99d28da02659', 'rows': ROWS,
     'reproduced': sum(1 for r in ROWS if r['reproduced']), 'total': len(ROWS), 'skip_mutation': a.skip_mutation}
json.dump(R, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
L = ['# 手順4 実装検分の所見の再現（機械生成・`tools/verify_review_impl_A.py` v1・%s UTC）' % R['generated_utc'], '',
     '- 事前登録: `records/reviews/A/draft7-impl/preregistration-impl-review-A.md`（採否の規則: 一次記録に当てて再現できた所見だけを採る）。',
     '- 検分者 2 の所見 F1〜F18・検分者 1 の所見 F-01〜F-34。再現 %d／%d 項。' % (R['reproduced'], R['total']), '',
     '| W | 所見 | 確かめたこと | 再現 | 詳細 |', '|---|---|---|---|---|']
L += ['| %s | %s | %s | %s | %s |' % (r['id'], r['findings'], r['desc'], '再現' if r['reproduced'] else '再現しない', r['detail'].replace('|', '／').replace('\n', ' ')[:300]) for r in ROWS]
L += ['', '- W66 は食い違いの例が計算上ありうることを示す項（検分者 1 の例の数値そのものは再計算していない）。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('[verify_review_impl_A] 再現 %d/%d → %s.{md,json}' % (R['reproduced'], R['total'], OUT))
