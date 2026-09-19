# -*- coding: utf-8 -*-
"""build_report_B.py v4 —— 段階 B の結果報告を、**雛形**（`records/B/results-report-template-B.md`）と集計の出力から組み立てる。

雛形の〔結果 X〕を、機械の区画で置き換える:
  A 要約／B 走行の記録（整合検査・抽出検査・セッション）／C 門1 と選定／D 確証の族の表／E 封印した符号との照合／
  F 記述の族／G S4 の反証（**同等性の規則・区間は Newcombe**・v4）／H 利益相反と情報状態／
  I td の特異性とランダム方向の等質性（裁定 D123・D127・v4）／J 副位置の読み（`tools/layers_B.py` の出力・**必須**・裁定 D132・v4）
**散文に手計算の数を残さない**（正本 `report_rules.typed_numbers`）。数はすべて集計の json から来る。
組み立ての後に走査器（`tools/report_lint.py`）を走らせる口を持つ（--lint）。
用法: python tools/build_report_B.py --analysis records/B/analysis-B-<日付>.json --gate records/B/gate-B-<日付>.json \
        [--integrity records/B/integrity-stageB-<日付>.json] [--out records/B/results-report-B.md] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v4'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--analysis', required=True)
ap.add_argument('--gate', required=True)
ap.add_argument('--integrity', required=True, help='tools/integrity_B.py の json（必須・採否表 P293）')
ap.add_argument('--sampling', required=True, help='抽出検査の封印 json（必須・採否表 P293）')
ap.add_argument('--layers', required=True, help='tools/layers_B.py の json（副位置の読み・必須・裁定 D132）')
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
G_s4 = block(['```', '判定: %s' % s4.get('verdict'),
              ('pt 差（(6b) − ランダム方向） %s・両側の区間 %s・（ランダム方向 − (6b)）の片側上限 %s pt・効き目 %s pt・相手の腕の率 %s・区間 %s'
               % (s4.get('diff_pt'), s4.get('ci'), s4.get('upper_one_sided_pt'), s4.get('effect_pt'), fmt_n(s4.get('partner_rate')), s4.get('interval'))
               if s4.get('partner_rate') is not None else '記録が無い'),
              '封印: %s' % s4.get('sealed_prediction')] + list(s4.get('notes') or []) + ['```'])
_td = ['| 対比 | 場面 | pt 差（v − td） | 区間 | 特異性 | 向き |', '|---|---|---|---|---|---|']
for t_ in A.get('td_specificity') or []:
    _td.append('| %s | %s | %s | %s | %s | %s |' % (t_['id'], t_['scenario'], fmt_n(t_.get('diff_pt')),
                                                [fmt_n(x) for x in (t_.get('ci') or [])] or '—',
                                                {True: '書ける', False: '書かない（区間が零を含む）', None: '測れない'}[t_.get('write_specificity')],
                                                t_.get('direction') or '—'))
_hm = ['| 場面 | 腕 | 三本の率の差 pt | 測れた方向 | 注 |', '|---|---|---|---|---|']
for h_ in A.get('homogeneity') or []:
    _hm.append('| %s | %s | %s | %s | %s |' % (h_['scenario'], h_['arm'], fmt_n(h_.get('spread_pt')), h_.get('measured'),
                                           {True: '注（不均一）', False: 'なし', None: '判定しない'}[h_.get('note')]))
I_td = block(_td + [''] + _hm)
_ly = ['| 層 | n A／B | 射影の平均 A | 射影の平均 B | 平均の差 | 標準化した差 | AUC |', '|---|---|---|---|---|---|---|']
for r_ in LY.get('rows') or []:
    _ly.append('| %s | %s／%s | %s | %s | %s | %s | %s |' % (r_['layer'], r_['n_A'], r_['n_B'], fmt_n(r_.get('mean_A')), fmt_n(r_.get('mean_B')),
                                                        fmt_n(r_.get('mean_diff')), fmt_n(r_.get('smd')), fmt_n(r_.get('auc'))))
J_ly = block(['場面 %s・%s 対 %s・方向 %s（主位置から作った・単位ベクトル）。記述であり、目安も p も置かない。' % (LY['scenario'], LY['arm_A'], LY['arm_B'], LY['direction']), ''] + _ly)
H_coi = block(['```', T['selection']['coi_note'], T['publication']['dual_use'],
               '率盲検の外の経路: 同一性選別の距離／調整走行の率（選定に要る）／品質床の得点。本走行の率は整合検査まで見ない。',
               '起草者は段階 A の公開結果を見ている（封印予想の情報状態の欄に記す）。', '```'])

_state = [l for l in tpl.split('\n') if l.startswith('- 状態: **雛形**')]
if len(_state) == 1:
    tpl = tpl.replace(_state[0], '- 状態: **報告**（雛形から組み立て器が機械で組んだ・結果の欄は機械の区画）。%s'
                      % ('**合成データから組んだ検査用の報告であり、本番ではない。**' if DRY else ''))
for ph, txt in (('A', A_sum), ('B', B_run), ('C', C_gate), ('D', D_conf), ('E', E_sign), ('F', block(F_desc)), ('G', G_s4), ('H', H_coi),
                ('I', I_td), ('J', J_ly)):
    key = '〔結果 %s〕' % ph
    if key not in tpl:
        sys.exit('雛形に %s が無い' % key)
    tpl = tpl.replace(key, txt)
tpl += '\n\n## 11. 組み立ての記録（機械）\n\n- 器 `tools/build_report_B.py` %s・%s UTC。集計 `%s`（SHA16 %s）・門 `%s`（SHA16 %s）・副位置の読み `%s`（SHA16 %s）。\n' % (
    VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
    os.path.relpath(a.analysis, REPO).replace('\\', '/'), runs_B.sha16_file(a.analysis),
    os.path.relpath(a.gate, REPO).replace('\\', '/'), runs_B.sha16_file(a.gate),
    os.path.relpath(a.layers, REPO).replace('\\', '/'), runs_B.sha16_file(a.layers))
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
