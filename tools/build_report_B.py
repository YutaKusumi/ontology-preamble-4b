# -*- coding: utf-8 -*-
"""build_report_B.py v7 —— 段階 B の結果報告を、**雛形**（`records/B/results-report-template-B.md`）と集計の出力から組み立てる。
v7（2026-09-20・四票の採否 P424・裁定 D150）: **区画 M——同一性選別の判定**（`tools/identity_screen_B.py` の出力・`--identity` は必須）。判定・三スタックの距離・番人の件数・記録の SHA16 を機械で貼る。前は判定を読む器が一つも無く、選別を走らせなくても、判定の器を走らせなくても、どの検査も落ちなかった（今回の発端と同じ型）。
v6（2026-09-19 の夜・封印の後・結果の前・独立の目を通っていない）: **区画 L——登録者とコーディネータの予想の照合**（`tools/compare_predictions_B.py` の出力・`--predictions-check` は必須・正本 `predictions.compare_rules.output`「要約を報告に機械で転記する」・裁定 D148）。照合の記録が、渡された集計と門の記録から作られたかを SHA16 で照らし、違えば止まる。
v5（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: **集計が読んだ門の記録と、渡された門の記録が同じか**を SHA で照らし、違えば止まる（採否表 P403）／**管理図の要約**の区画 K（全点と三つの判定・`--chart` は必須・裁定 D110・採否表 P410）／S4 の区画に門・封印の照合・相対の大きさ・観測した相手の率での動作特性（裁定 D134〜D136）／td の特異性の区画を族ごとの規則の札に（裁定 D133）／副位置の読みの区画に参照の行と合わせる前の比（裁定 D139・D133）。

雛形の〔結果 X〕を、機械の区画で置き換える:
  A 要約／B 走行の記録（整合検査・抽出検査・セッション）／C 門1 と選定／D 確証の族の表／E 封印した符号との照合／
  F 記述の族／G S4 の反証（**同等性の規則・区間は Newcombe**・v4）／H 利益相反と情報状態／
  I td の特異性とランダム方向の等質性（裁定 D133・D127・v5）／J 副位置の読み（`tools/layers_B.py` の出力・**必須**・裁定 D132・参照の行は D139・v5）／
  K 管理図の要約（`tools/control_chart_B.py` の出力・**必須**・裁定 D110・採否表 P410・v5）／
  L 登録者とコーディネータの予想の照合（`tools/compare_predictions_B.py` の出力・**必須**・裁定 D148・v6）／
  M 同一性選別の判定（`tools/identity_screen_B.py` の出力・**必須**・採否表 P424・裁定 D150・v7）
**散文に手計算の数を残さない**（正本 `report_rules.typed_numbers`）。数はすべて集計の json から来る。
組み立ての後に走査器（`tools/report_lint.py`）を走らせる口を持つ（--lint）。
用法: python tools/build_report_B.py --analysis records/B/analysis-B-<日付>.json --gate records/B/gate-B-<日付>.json \
        [--integrity records/B/integrity-stageB-<日付>.json] [--out records/B/results-report-B.md] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v7'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--analysis', required=True)
ap.add_argument('--gate', required=True)
ap.add_argument('--integrity', required=True, help='tools/integrity_B.py の json（必須・採否表 P293）')
ap.add_argument('--sampling', required=True, help='抽出検査の封印 json（必須・採否表 P293）')
ap.add_argument('--layers', required=True, help='tools/layers_B.py の json（副位置の読み・必須・裁定 D132）')
ap.add_argument('--chart', required=True, help='tools/control_chart_B.py の json（管理図の要約・必須・裁定 D110・採否表 P410）')
ap.add_argument('--predictions-check', required=True, help='tools/compare_predictions_B.py の json（予想の照合・必須・裁定 D148）')
ap.add_argument('--identity', required=True, help='tools/identity_screen_B.py の json（同一性選別の判定・必須・採否表 P424・裁定 D150）')
ap.add_argument('--allow-dry', action='store_true', help='検査用の口（合成データから組む・区画ごとに印を差し込む）')
ap.add_argument('--force-problems', action='store_true', help='整合検査に不整合があっても組む（理由を記録に残すこと）')
ap.add_argument('--template', default=os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--lint', action='store_true', help='組み立ての後に報告の走査器（tools/report_lint.py）を走らせる（裁定 D112・採否表 P327）')
a = ap.parse_args()
T = runs_B.load_T()
A = runs_B.read_json(a.analysis)
G = runs_B.read_json(a.gate)
INT = runs_B.read_json(a.integrity) if a.integrity else None
SMP = runs_B.read_json(a.sampling) if a.sampling else None
LY = runs_B.read_json(a.layers)
assert LY.get('kind') == 'layers_B', '副位置の読みの記録の種類が違う'
assert A.get('kind') == 'analyze_B' and G.get('kind') == 'gate_B', '集計または門の記録の種類が違う'
CH = runs_B.read_json(a.chart)
assert CH.get('kind') == 'control_chart_B', '管理図の記録の種類が違う'
# **集計が読んだ門の記録と、渡された門の記録が同じか**（採否表 P403・2026-09-19）。前は照らさず、別の門の記録を渡しても組めた
if A.get('gate_sha16') != runs_B.sha16_file(a.gate):
    sys.exit('集計が読んだ門の記録（SHA16 %s）と、渡された門の記録（SHA16 %s）が違う——同じ門の記録で集計し直す（採否表 P403）'
             % (A.get('gate_sha16'), runs_B.sha16_file(a.gate)))
# **照合の記録が、渡された集計と門の記録から作られたか**（v6・正本 predictions.compare_rules.interpretation.records_match）
PC = runs_B.read_json(a.predictions_check)
if PC.get('kind') != 'compare_predictions_B':
    sys.exit('予想の照合の記録の種類が違う: %s' % PC.get('kind'))
if (PC.get('analysis') or {}).get('sha16') != runs_B.sha16_file(a.analysis) or (PC.get('gate') or {}).get('sha16') != runs_B.sha16_file(a.gate):
    sys.exit('予想の照合の記録が、渡された集計・門の記録から作られていない（照合の器を同じ記録で走らせ直す・predictions.compare_rules.interpretation.records_match）')
DRY = A.get('dry_marks') or []
if DRY and not a.allow_dry:
    sys.exit('**合成データ（dry-run の印つき）から報告を組もうとしている**: %s。検査用は --allow-dry（採否表 P279）' % '・'.join(DRY))
if INT and INT.get('problems') and not a.force_problems:
    sys.exit('整合検査に不整合が %d 件ある。直してから報告を組む（--force-problems は理由を記録に残す場合のみ・採否表 P293）' % len(INT['problems']))
MARK = ('【合成データ・本番ではない】' if DRY else '')
out_md = a.out or os.path.join(REPO, 'records', 'B', 'results-report-B.md')
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
tpl = open(a.template, encoding='utf-8').read()
PS = T['print_strings']
c = A['counts']
n_conf = sum(x['m'] for x in T['families'].values())


MB = T['report_rules']['machine_block']        # 機械の区画の印（段階 A と同じ・報告の走査器が読む・2026-09-19）


def block(lines):
    """機械の区画。**区画の印で囲む**（走査器が区画の外の数を検べ、区画の中身を記録と突合する・v4）。
    合成データから組んだときは**区画ごとに**印を差し込む（切り出しで落ちないように・採否表 P279）。"""
    out = [l for l in lines if l is not None]
    if MARK:
        out = [MARK] + out
    return '\n'.join([MB['begin']] + out + [MB['end']])


A_sum = block([
    '```',
    PS['first_finding'].format(confirmed=c['確証'], undecidable=c['判定不能（検閲）'], qfloor=c['判定不能（品質床）'],
                               gap=c['判定不能（採点欠落）'], nodata=c['判定不能（測れなかった）'],
                               ff=c['判定保留（書式外転位）'], refuse=c['判定保留（refuse 転位）'] + c['判定保留（refuse 転位・差）'],
                               style=c['判定保留（様式転位）'], ns=c['非有意']),
    PS['scope'],
    'S4 の反証: %s' % A['s4'].get('verdict'),
    '```'])
B_run = block(['```',
               '整合検査: 不整合 %d 件・注 %d 件（%s）' % (len(INT['problems']), len(INT['notes']), INT['tag']),
               '抽出検査: 標本 %d 件・対応表の封印あり（並べ替え %s）' % (SMP.get('n_items', 0), SMP.get('shuffled')),
               '正本 SHA16 %s・集計 %s UTC' % (A['contrasts_sha16'], A['generated_utc']),
               '```'])
sel = G['selection']['pick'] or {}
C_gate = block(['```',
                (PS['gate1_open'].format(k=G['gate1']['quality_pass_candidates'], layer=sel.get('layer'), coef=sel.get('coef'),
                                         eff=sel.get('eff_pt'), tied=len(G['selection']['tied']))
                 if G['gate1']['open'] else PS['gate1_closed']),
                PS['selection_coi'], PS['selection_direction'],
                ('同値の帯: 幅 %s pt（帰無の模擬 %s 回・同値の候補 %d 組）' % (G['selection']['equivalence_band']['q95_pt'],
                                                                format(G['selection']['equivalence_band']['reps'], ','),
                                                                len(G['selection']['tied'])) if G['selection'].get('equivalence_band') else ''),
                (G['selection'].get('tie_note') or ''), (G['selection'].get('nonpositive_stop') or ''),
                '```'])
fmt_p = lambda x: ('—' if x is None else ('%.3g' % x if x >= 1e-5 else '<1e-5'))
fmt_n = lambda x: ('—' if x is None else ('%g' % round(float(x), 4)))      # 丸めない浮動小数を報告に出さない（採否表 P335〔二体目 G1〕）

# **雛形の数を正本から組み直して突き合わせる**（裁定 D112・採否表 P326）。
_src = os.path.splitext(a.template)[0] + '.src.md'
if os.path.exists(_src):
    import subprocess, tempfile as _tf, shutil as _sh
    _d = _tf.mkdtemp(prefix='tplchk_')
    try:
        _o, _l = os.path.join(_d, 't.md'), os.path.join(_d, 'l.md')
        _rc = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'build_draftB.py'), '--kind', 'template',
                              '--src', _src, '--out', _o, '--label', '報告雛形', '--lint-report', _l],
                             capture_output=True, text=True, encoding='utf-8').returncode
        if _rc == 0 and runs_B.sha16_file(_o) != runs_B.sha16_file(a.template):
            sys.exit('雛形が正本から組み直した版と違う（正本が動いた後に雛形を組み直していない・裁定 D112）: '
                     '現物 %s / 組み直し %s' % (runs_B.sha16_file(a.template), runs_B.sha16_file(_o)))
    finally:
        _sh.rmtree(_d, ignore_errors=True)
rows = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | 書式外 A／B | refuse A／B | pt 差 | 区間 | p | 様式の差 | 札 | 注 |',
        '|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in A['confirm']:
    if r.get('missing'):
        rows.append('| %s | %s | — | — | — | — | — | — | — | — | %s | |' % (r['id'], r['scenario'], r['label']))
        continue
    rows.append('| %s | %s | %d/%d | %d/%d | %s／%s | %s／%s | %s | %s | %s | %s | %s | %s |'
                % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'],
                   fmt_n(r.get('ff_pt_A')), fmt_n(r.get('ff_pt_B')), fmt_n(r.get('refuse_pt_A')), fmt_n(r.get('refuse_pt_B')),
                   r['diff_pt'], r['ci'], fmt_p(r.get('p')), r.get('style_diff_pt'), r['label'],
                   '・'.join(r.get('notes') or [])))
D_conf = block(rows)
sg = A['sign_agreement']
E_sign = block(['```', (PS['sign_agreement'].format(agree=sg['agree'], confirmed=sg.get('checked')) if sg['sealed']
                        else '封印の記録が渡されていないので、予想符号との照合は行っていない。'),
                ('照合できなかった確証の対比: %s' % (sg.get('unchecked') or 'なし')) if sg['sealed'] else None,
                ('封印の欠け: %d 件' % len(sg.get('seal_missing') or [])) if sg['sealed'] else None, '```'])
F_desc = []
for fam, rs in A['descriptive'].items():
    if not rs:
        continue
    F_desc += ['**%s**' % fam, '', '| 対比 | 破局率 A | 破局率 B | pt 差 | 区間 |', '|---|---|---|---|---|']
    for r in rs:
        if r.get('missing'):
            F_desc.append('| %s | — | — | — | — |' % r['id'])
        else:
            F_desc.append('| %s | %s | %s | %s | %s |' % (r['id'], None if r['rate_A'] is None else round(r['rate_A'], 4),
                                                          None if r['rate_B'] is None else round(r['rate_B'], 4), r['diff_pt'], r['ci']))
    F_desc.append('')
F_desc.append(PS['no_p_desc'])
s4 = A['s4']
_ocf = lambda d: '・'.join('%s %s' % (k, fmt_n(v)) for k, v in (d or {}).items())
_rs = s4.get('relative_size') or {}
_oc = s4.get('oc_at_observed_partner') or {}
G_s4 = block(['```', '札: %s（三分岐の前の門: %s・裁定 D134）' % (s4.get('verdict'), '・'.join(s4.get('gates') or []) or 'なし'),
              '封印の値: %s・照合: %s（札とは別に出す・正本 B_desc_S4.seal_match・裁定 D135）' % (s4.get('seal_value'), s4.get('seal_match')),
              ('pt 差（(6b) − ランダム方向） %s・両側の区間 %s・（ランダム方向 − (6b)）の片側上限 %s pt・効き目 %s pt・相手の腕の率 %s・区間 %s'
               % (s4.get('diff_pt'), s4.get('ci'), s4.get('upper_one_sided_pt'), s4.get('effect_pt'), fmt_n(s4.get('partner_rate')), s4.get('interval'))
               if s4.get('partner_rate') is not None else '記録が無い'),
              ('効き目の相対の大きさ（裁定 D136）: 観測した相手の率に対して %s・登録の基底に対して %s'
               % (fmt_n(_rs.get('to_observed_partner')), fmt_n(_rs.get('to_registered_base'))) if _rs else None),
              ('観測した相手の率 %s・各腕 n=%s での動作特性（判定には使わない）——真に零: %s／真に効き目ちょうど: %s'
               % (fmt_n(_oc.get('partner_rate')), _oc.get('n_per_arm'), _ocf(_oc.get('at_zero')), _ocf(_oc.get('at_effect'))) if _oc else None)]
             + list(s4.get('notes') or []) + ['```'])
_td = ['| 対比 | 族 | 場面 | pt 差（v − td） | 区間 | p | Holm の閾値 | 確証の対比の札 | 特異性 |', '|---|---|---|---|---|---|---|---|---|']
for t_ in A.get('td_specificity') or []:
    _td.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (t_['id'], t_.get('family'), t_['scenario'], fmt_n(t_.get('diff_pt')),
                                                           [fmt_n(x) for x in (t_.get('ci') or [])] or '—', fmt_p(t_.get('p')),
                                                           fmt_n(t_.get('holm_alpha')), t_.get('conf_label'), t_.get('label')))
_hm = ['| 場面 | 腕 | 三本の率の差 pt | 測れた方向 | 注 |', '|---|---|---|---|---|']
for h_ in A.get('homogeneity') or []:
    _hm.append('| %s | %s | %s | %s | %s |' % (h_['scenario'], h_['arm'], fmt_n(h_.get('spread_pt')), h_.get('measured'),
                                           {True: '注（不均一）', False: 'なし', None: '判定しない'}[h_.get('note')]))
I_td = block(_td + [''] + _hm)
_ly = ['| 層 | n A／B | 射影の平均 A | 射影の平均 B | 平均の差 | 標準化した差 | AUC |', '|---|---|---|---|---|---|---|']
for r_ in LY.get('rows') or []:
    _ly.append('| %s | %s／%s | %s | %s | %s | %s | %s |' % (r_['layer'], r_['n_A'], r_['n_B'], fmt_n(r_.get('mean_A')), fmt_n(r_.get('mean_B')),
                                                        fmt_n(r_.get('mean_diff')), fmt_n(r_.get('smd')), fmt_n(r_.get('auc'))))
_ref = ['| 軸 | 層 | 平均の差 | 標準化した差 | AUC |', '|---|---|---|---|---|']
for r_ in LY.get('reference_rows') or []:
    _ref.append('| %s | %s | %s | %s | %s |' % (r_['axis'], r_['layer'], fmt_n(r_.get('mean_diff')), fmt_n(r_.get('smd')), fmt_n(r_.get('auc'))))
if not LY.get('reference_rows'):
    sys.exit('副位置の読みの記録に参照の行が無い（裁定 D139・tools/layers_B.py v2 で作り直す）')
_raw = LY.get('raw_norm_ratio')
J_ly = block(['場面 %s・%s 対 %s・方向 %s（主位置から作った・単位ベクトル）。記述であり、目安も p も置かない。' % (LY['scenario'], LY['arm_A'], LY['arm_B'], LY['direction']), ''] + _ly
             + ['', '参照の行（同じ保存値を、同じ層のランダム方向の三本・td・Nk の単位方向に射影した・裁定 D139）:', ''] + _ref
             + ['', '合わせる前の比（‖td‖/‖v̂‖ など・方向の要約統計・裁定 D133）: %s'
                % ('・'.join('層 %s: %s' % (k, '・'.join('%s %s' % (n_, fmt_n(v_)) for n_, v_ in (v or {}).items())) for k, v in _raw.items()) if _raw else '記録が無い')])
# **管理図の要約**（裁定 D110・採否表 P410・前の巡の採否 P323 の残り）——全点と三つの判定
_pts = CH.get('points') or []
_kind = lambda v: ('帯の外かつ有意' if '帯の外かつ有意' in v else ('帯の外だが有意でない' if '帯の外だが有意でない' in v else ('帯の内側' if v.startswith('帯の内側') else '判定しない点')))
_kc = {k: sum(1 for p_ in _pts if _kind(p_.get('verdict', '')) == k) for k in ('帯の外かつ有意', '帯の外だが有意でない', '帯の内側', '判定しない点')}
_kr = ['| 場面 | 腕 | セッション | 破局/n_ok | 初点との差 pt | p | 判定 |', '|---|---|---|---|---|---|---|']
for p_ in _pts:
    _kr.append('| %s | %s | %s | %s/%s | %s | %s | %s |' % (p_.get('scenario'), p_.get('arm'), p_.get('session'), p_.get('k'), p_.get('n'),
                                                        fmt_n(p_.get('diff_pt')), fmt_p(p_.get('p')), _kind(p_.get('verdict', ''))))
K_chart = block(['管理図の要約: 全点 %d・帯の外かつ有意 %d・帯の外だが有意でない %d・帯の内側 %d・判定しない点（初点・測れなかった）%d・点が一つのセル %d（帯 %s pt）'
                 % (len(_pts), _kc['帯の外かつ有意'], _kc['帯の外だが有意でない'], _kc['帯の内側'], _kc['判定しない点'], len(CH.get('notes') or []), CH.get('band_pt')), ''] + _kr)
import compare_predictions_B as _CMP
L_pred = block(['```'] + [_CMP.summary_line(who, R) for who, R in PC['results'].items()]
               + [('予想の独立（封印の順の注）: %s' % PC['order_note']) if PC.get('order_note') else None,
                  '外れと照合不能の一覧は照合の記録 `%s` にある（予想のファイルと SHA-256 もそこに）。' % os.path.relpath(a.predictions_check, REPO).replace('\\', '/'),
                  T['predictions']['fence'], '```'])
# ---- 区画 M: 同一性選別（三スタックの距離・採否表 P424・裁定 D150） ----
IS = runs_B.read_json(a.identity)
if IS.get('kind') != 'identity_screen_B':
    sys.exit('--identity は tools/identity_screen_B.py の出力を渡す（kind が違う: %s）' % IS.get('kind'))
if not DRY and (IS.get('dev_marks') or []):
    sys.exit('同一性選別の記録に検査用の印がある（%s）。本番の報告には渡さない' % '・'.join(IS['dev_marks']))
_ist = IS['tables']
M_ident = block(['```',
                 '主判定（%s 対 %s）: %s（%d 個の絶対差の平均 %.3f pt・閾値 %s 以下／最大 %.3f pt・閾値 %s 以下）'
                 % (IS['main_pair'][0], IS['main_pair'][1], IS['verdict'], IS['n_differences'],
                    IS['mean_abs_diff_pt'], IS['mean_pt'], IS['max_abs_diff_pt'], IS['max_pt'])]
                + ['%s: 平均 %.3f pt・最大 %.3f pt（B の八腕: 平均 %.3f pt・最大 %.3f pt）'
                   % (k_, t_['all']['mean_pt'], t_['all']['max_pt'], t_['b_panel']['mean_pt'], t_['b_panel']['max_pt'])
                   for k_, t_ in _ist.items()]
                + ['採点欠落 %d 件・trial_id の重複 %d 腕・種の不一致 %d 走行（番人・採否表 P418〜P421・P427）'
                   % (sum((IS['guards']['scoring_gap'] or {}).values()), len(IS['guards']['duplicate_trial_ids'] or {}), len(IS['seeds']['mismatch'] or {})),
                   '記録 `%s`（SHA16 %s）・%s' % (os.path.relpath(a.identity, REPO).replace('\\', '/'), runs_B.sha16_file(a.identity), IS['aux_note']),
                   IS['fail_reading'], '```'])
H_coi = block(['```', T['selection']['coi_note'], T['publication']['dual_use'],
               '率盲検の外の経路: 同一性選別の距離／調整走行の率（選定に要る）／品質床の得点。本走行の率は整合検査まで見ない。',
               '起草者は段階 A の公開結果を見ている（封印予想の情報状態の欄に記す）。', '```'])

_state = [l for l in tpl.split('\n') if l.startswith('- 状態: **雛形**')]
if len(_state) == 1:
    tpl = tpl.replace(_state[0], '- 状態: **報告**（雛形から組み立て器が機械で組んだ・結果の欄は機械の区画）。%s'
                      % ('**合成データから組んだ検査用の報告であり、本番ではない。**' if DRY else ''))
for ph, txt in (('A', A_sum), ('B', B_run), ('C', C_gate), ('D', D_conf), ('E', E_sign), ('F', block(F_desc)), ('G', G_s4), ('H', H_coi),
                ('I', I_td), ('J', J_ly), ('K', K_chart), ('L', L_pred), ('M', M_ident)):
    key = '〔結果 %s〕' % ph
    if key not in tpl:
        sys.exit('雛形に %s が無い' % key)
    tpl = tpl.replace(key, txt)
tpl += '\n\n## 11. 組み立ての記録（機械）\n\n- 器 `tools/build_report_B.py` %s・%s UTC。集計 `%s`（SHA16 %s）・門 `%s`（SHA16 %s・集計が読んだ門と一致）・副位置の読み `%s`（SHA16 %s）・管理図 `%s`（SHA16 %s）・予想の照合 `%s`（SHA16 %s）。\n' % (
    VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
    os.path.relpath(a.analysis, REPO).replace('\\', '/'), runs_B.sha16_file(a.analysis),
    os.path.relpath(a.gate, REPO).replace('\\', '/'), runs_B.sha16_file(a.gate),
    os.path.relpath(a.layers, REPO).replace('\\', '/'), runs_B.sha16_file(a.layers),
    os.path.relpath(a.chart, REPO).replace('\\', '/'), runs_B.sha16_file(a.chart),
    os.path.relpath(a.predictions_check, REPO).replace('\\', '/'), runs_B.sha16_file(a.predictions_check))
tpl = tpl.replace('- 器 `tools/build_report_B.py`', '- 同一性選別 `%s`（SHA16 %s）。\n- 器 `tools/build_report_B.py`'
                  % (os.path.relpath(a.identity, REPO).replace('\\', '/'), runs_B.sha16_file(a.identity)), 1)
tpl += '\n'.join([MB['begin'], '- 組み立ての記録は機械が書いた（この区画の中身は区画の記録と突合する）。', MB['end']]) + '\n'
open(out_md, 'w', encoding='utf-8', newline='\n').write(tpl)
# **機械の区画の記録**（-machine.json・段階 A の型・報告の走査器が突合する・v4）
import report_lint as _RL
_RL.write_sidecar(out_md, tpl, T, 'tools/build_report_B.py %s' % VERSION)
if a.lint:
    # **報告の走査器を走らせる**（裁定 D112・採否表 P327）。前は口上が持つと書いて argparse に口が無かった。
    import subprocess
    lint = os.path.join(REPO, 'tools', 'report_lint.py')
    if not os.path.exists(lint):
        sys.exit('報告の走査器が無い: tools/report_lint.py')
    side = os.path.splitext(out_md)[0] + '-machine.json'
    cmd = [sys.executable, lint, out_md, '--contrasts', runs_B.CPATH, '--template', a.template,
           '--out', os.path.splitext(out_md)[0] + '-lint.md']      # **走査器の出力は B の置き場に置く**（既定は段階 A の置き場・v4）
    if os.path.exists(side):
        cmd += ['--sidecar', side]
    rcl = subprocess.run(cmd).returncode
    if rcl != 0:
        sys.exit('報告の走査器が違反を出した（終了コード %d）' % rcl)

print('[build_report_B] %s' % out_md)
