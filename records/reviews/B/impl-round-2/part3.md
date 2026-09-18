# 直しの確認・資料 第3部（機械生成・2026-09-18 05:48 UTC）

変わった器材のソースを**逐語**で入れています。SHA16 は現物から取ったものです。

## `tools/dry_run_B.py`（SHA16 A4B9B6F7114EC003・139 行）

```python
# -*- coding: utf-8 -*-
"""dry_run_B.py v2 —— 段階 B の器材の**合成データによる検査**（札の全経路を一度ずつ以上発火させる）。

器材の整備の計画 `records/B/tooling-plan-B-2026-09-18.md` の表の経路を、合成データ（`synth_B.py`）で作り、
`gate_B.py`（門1 と選定）と `analyze_B.py`（本走行の集計と札）を走らせて、**どの経路が発火したか**を数える。
発火しない経路があれば非零で終わる（凍結の前に全経路が発火していることが条件）。
合成データは results/_synth/ に置き、行にも置き場にも dry-run の印を立てる（公開の置き場には入れない）。
出力: records/B/dry-run-B-<日付>.md（--out で変える・--force が無ければ上書きしない）。
用法: python tools/dry_run_B.py [--keep] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, argparse, datetime, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

T = runs_B.load_T()

VERSION = 'v2'
REPO = runs_B.REPO
PY = sys.executable
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--keep', action='store_true', help='合成データを消さない')
a = ap.parse_args()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'dry-run-B-%s.md' % jst.strftime('%Y-%m-%d'))
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)

PATHS = ['確証', '確証（登録された向きと逆）', '封印した符号と一致', '判定不能（検閲）', '判定不能（採点欠落）', '判定不能（測れなかった）',
         '判定保留（書式外転位）', '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '注（様式）',
         '判定不能（品質床）', '非有意', '門1 を閉じる', '記録の不在（incomplete）', '全候補が非正', '同点の割り方',
         '床・天井で選定から外す', 'S4: 下がった（外れ）', 'S4: 下がらなかった（当たり）', 'S4: 当否を言わない', 'S4: 余地の条項',
         '希釈が効く場面（書式外が分子を食う）', '中断と再開', '同一性選別の走行', '未測定（ループ・打ち切り）', '封印の欠けで止まる']
fired = {k: [] for k in PATHS}
rows = []


def run(cmd):
    r = subprocess.run([PY] + cmd, capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


for case in ('all', 'gate1_closed', 'nonpositive', 'tie', 'censor_candidates', 'scoring_gap', 's4_branches', 's4_floor', 'dilution_causal', 'incomplete'):
    root = os.path.join('results', '_synth', case)
    rc, out = run(['tools/synth_B.py', '--case', case, '--out-root', root])
    assert rc == 0, out
    rc_g, out_g = run(['tools/gate_B.py', '--root', root, '--allow-dry', '--out', os.path.join(root, 'gate-B.md'), '--force'])
    assert rc_g in (0, 2), ('門の器が思わぬ終了コードで落ちた', rc_g, out_g[-400:])   # 採否表 P296
    G = json.load(open(os.path.join(REPO, root, 'gate-B.json'), encoding='utf-8'))
    if G['verdict'] == 'incomplete':
        fired['記録の不在（incomplete）'].append(case)
    sel = G['selection']
    if not G['gate1']['open']:
        fired['門1 を閉じる'].append(case)
    if sel.get('nonpositive_stop'):
        fired['全候補が非正'].append(case)
    if sel.get('tie_note'):
        fired['同点の割り方'].append(case)
    if any(r.get('censored') for r in G['candidates']):
        fired['床・天井で選定から外す'].append(case)
    rec = {'case': case, 'gate_verdict': G['verdict'], 'gate_rc': rc_g, 'labels': {}}
    if G['gate1']['open']:
        seal = os.path.join(root, 'seal-B.json')
        cmd = ['tools/analyze_B.py', '--gate', os.path.join(root, 'gate-B.json'), '--root', root, '--allow-dry',
               '--out', os.path.join(root, 'analysis-B.md'), '--force']
        if os.path.exists(os.path.join(REPO, seal)):
            # 合成の封印は全対比ぶんではないので、**まず止まることを確かめてから**検査用の口で進む（裁定 D79・採否表 P277）
            rc_stop, _ = run(cmd + ['--seal', seal])
            if rc_stop != 0:
                fired['封印の欠けで止まる'].append(case)
            cmd += ['--seal', seal, '--allow-partial-seal']
        rc_a, out_a = run(cmd)
        assert rc_a == 0, out_a
        A = json.load(open(os.path.join(REPO, root, 'analysis-B.json'), encoding='utf-8'))
        for r in A['confirm']:
            lab = r.get('label')
            if lab in fired:
                fired[lab].append(case)
            rec['labels'][lab] = rec['labels'].get(lab, 0) + 1
            if any('注（様式' in n for n in (r.get('notes') or [])):
                fired['注（様式）'].append(case)
        v4 = A['s4'].get('verdict') or ''
        for nm, key in (('S4: 下がった（外れ）', '下がった'), ('S4: 下がらなかった（当たり）', '下がらなかった'),
                        ('S4: 当否を言わない', '当否を言わない'), ('S4: 余地の条項', '余地の条項')):
            if key in v4:
                fired[nm].append('%s（%s）' % (case, v4))
        if (A['sign_agreement'].get('agree') or 0) > 0:
            fired['封印した符号と一致'].append(case)
        rec['s4'] = A['s4'].get('verdict')
        rec['sign_agreement'] = A['sign_agreement']
    # 合成データの中身から確かめる経路（採否表 P300〜P302）
    import glob as _g
    mainroot = os.path.join(REPO, root, T['tags']['main'])
    if os.path.isdir(mainroot):
        sess = {json.load(open(os.path.join(d, 'manifest.json'), encoding='utf-8')).get('session') for d in _g.glob(os.path.join(mainroot, '*'))}
        if len(sess) > 1:
            fired['中断と再開'].append(case)
        ff_cat = unmeas = 0
        for d in _g.glob(os.path.join(mainroot, '*')):
            for f in _g.glob(os.path.join(d, 'trials-*.jsonl')):
                for line in open(f, encoding='utf-8'):
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    if r.get('format_fail') and r.get('catastrophe'):
                        ff_cat += 1
                    if r.get('loop_flag') or r.get('truncated'):
                        unmeas += 1
        if unmeas:
            fired['未測定（ループ・打ち切り）'].append(case)
        if ff_cat == 0 and case == 'dilution_causal':
            fired['希釈が効く場面（書式外が分子を食う）'].append(case)
    if os.path.isdir(os.path.join(REPO, root, T['tags']['identity'])):
        fired['同一性選別の走行'].append(case)
    rows.append(rec)

missing = [k for k, v in fired.items() if not v]
L = ['# 段階 B 器材の合成データによる検査（機械生成・`tools/dry_run_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 合成データは `results/_synth/<場合>/`（行にも置き場にも dry-run の印・公開の置き場には入れない）。',
     '- 正本 SHA16 %s。**発火しなかった経路 %d 件**。' % (runs_B.sha16_file(runs_B.CPATH), len(missing)), '',
     '| 経路 | 発火した場合 |', '|---|---|']
for k in PATHS:
    L.append('| %s | %s |' % (k, '・'.join(sorted(set(fired[k]))) or '**発火せず**'))
L += ['', '## 場合ごとの結果', '', '| 場合 | 門の判定 | 札の内訳 | S4 | 符号の一致 |', '|---|---|---|---|---|']
for r in rows:
    L.append('| %s | %s | %s | %s | %s |' % (r['case'], r['gate_verdict'],
                                             '・'.join('%s %d' % (k, v) for k, v in sorted(r['labels'].items())) or '—',
                                             r.get('s4') or '—', r.get('sign_agreement') or '—'))
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
if not a.keep:
    shutil.rmtree(os.path.join(REPO, 'results', '_synth'), ignore_errors=True)
print('[dry_run_B] %s | 発火しなかった経路 %d' % (out_md, len(missing)))
if missing:
    print('  未発火: ' + '・'.join(missing))
sys.exit(1 if missing else 0)
```

## `tools/build_report_B.py`（SHA16 27B502251078693C・135 行）

```python
# -*- coding: utf-8 -*-
"""build_report_B.py v2 —— 段階 B の結果報告を、**雛形**（`records/B/results-report-template-B.md`）と集計の出力から組み立てる。

雛形の〔結果 X〕を、機械の区画で置き換える:
  A 要約／B 走行の記録（整合検査・抽出検査・セッション）／C 門1 と選定／D 確証の族の表／E 封印した符号との照合／
  F 記述の族／G S4 の反証／H 利益相反と情報状態
**散文に手計算の数を残さない**（正本 `report_rules.typed_numbers`）。数はすべて集計の json から来る。
組み立ての後に走査器（`tools/report_lint.py`）を走らせる口を持つ（--lint）。
用法: python tools/build_report_B.py --analysis records/B/analysis-B-<日付>.json --gate records/B/gate-B-<日付>.json \
        [--integrity records/B/integrity-stageB-<日付>.json] [--out records/B/results-report-B.md] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v2'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--analysis', required=True)
ap.add_argument('--gate', required=True)
ap.add_argument('--integrity', required=True, help='tools/integrity_B.py の json（必須・採否表 P293）')
ap.add_argument('--sampling', required=True, help='抽出検査の封印 json（必須・採否表 P293）')
ap.add_argument('--allow-dry', action='store_true', help='検査用の口（合成データから組む・区画ごとに印を差し込む）')
ap.add_argument('--force-problems', action='store_true', help='整合検査に不整合があっても組む（理由を記録に残すこと）')
ap.add_argument('--template', default=os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
T = runs_B.load_T()
A = runs_B.read_json(a.analysis)
G = runs_B.read_json(a.gate)
INT = runs_B.read_json(a.integrity) if a.integrity else None
SMP = runs_B.read_json(a.sampling) if a.sampling else None
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


def block(lines):
    """機械の区画。合成データから組んだときは**区画ごとに**印を差し込む（切り出しで落ちないように・採否表 P279）。"""
    out = [l for l in lines if l is not None]
    if MARK:
        out = [MARK] + out
    return '\n'.join(out)


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
rows = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | 書式外 A／B | refuse A／B | pt 差 | 区間 | p | 様式の差 | 札 | 注 |',
        '|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in A['confirm']:
    if r.get('missing'):
        rows.append('| %s | %s | — | — | — | — | — | — | — | — | %s | |' % (r['id'], r['scenario'], r['label']))
        continue
    rows.append('| %s | %s | %d/%d | %d/%d | %s／%s | %s／%s | %s | %s | %s | %s | %s | %s |'
                % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'],
                   r.get('ff_pt_A'), r.get('ff_pt_B'), r.get('refuse_pt_A'), r.get('refuse_pt_B'),
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
              ('pt 差 %s・区間 %s・相手の腕の率 %s・%s pt の検出力 %s（線は %s）'
               % (s4.get('diff_pt'), s4.get('ci'), s4.get('partner_rate'), s4.get('effect_pt'), s4.get('power_at_effect'), s4.get('power_min'))
               if s4.get('power_at_effect') is not None else '検出力は出さない（余地の条項または低下の余地が無い・裁定 D95）'),
              '封印: %s' % s4.get('sealed_prediction'), '```'])
H_coi = block(['```', T['selection']['coi_note'], T['publication']['dual_use'],
               '率盲検の外の経路: 同一性選別の距離／調整走行の率（選定に要る）／品質床の得点。本走行の率は整合検査まで見ない。',
               '起草者は段階 A の公開結果を見ている（封印予想の情報状態の欄に記す）。', '```'])

for ph, txt in (('A', A_sum), ('B', B_run), ('C', C_gate), ('D', D_conf), ('E', E_sign), ('F', block(F_desc)), ('G', G_s4), ('H', H_coi)):
    key = '〔結果 %s〕' % ph
    if key not in tpl:
        sys.exit('雛形に %s が無い' % key)
    tpl = tpl.replace(key, txt)
tpl += '\n\n## 11. 組み立ての記録（機械）\n\n- 器 `tools/build_report_B.py` %s・%s UTC。集計 `%s`（SHA16 %s）・門 `%s`（SHA16 %s）。\n' % (
    VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
    os.path.relpath(a.analysis, REPO).replace('\\', '/'), runs_B.sha16_file(a.analysis),
    os.path.relpath(a.gate, REPO).replace('\\', '/'), runs_B.sha16_file(a.gate))
open(out_md, 'w', encoding='utf-8', newline='\n').write(tpl)
print('[build_report_B] %s' % out_md)
```

## `tools/freeze_B.py`（SHA16 72A8487BDDDBAF25・145 行）

```python
# -*- coding: utf-8 -*-
"""freeze_B.py v2 —— 段階 B の**凍結の記帳**（凍結物の SHA・封印予想・凍結時に記帳する値・逸脱台帳の口）。

凍結するもの（正本 `publication.record_first`・草案8B §2.11）:
  凍結本文（草案）・正本 `design/contrasts-B.json`・腕と方向の定義・器材・報告の雛形・**封印予想**。
凍結時に記帳する値（設計の段では書けないもの）:
  - 重みの rev・tokenizer の版・**総層数**（`selection.candidates.layer_index_rule`）と層の添字
  - **腕ごとのトークン長**（裁定 D82・`position_length.record_at_freeze`）
  - 品質床の課題の出所・版・ライセンス・断片の SHA（裁定 D66）と、入力・帯・採点・最大トークン数（採否表 P216）
  - v̂ の SHA（`selection.vector_fix`）と方向の要約統計（ノルム・コサイン・場面間の安定性）
封印予想（`seal_format`）: 確証の各対比の符号と S4 の反証。**B のデータを一つも見る前**に書き、情報状態と時機を添える。
凍結の後の変更はすべて**逸脱**とし、番号・日付・理由・登録者の承認を記帳する（`deviation.rule`）。
出力: records/B/FREEZE-RECORD-B.md と同 .json（--force が無ければ上書きしない）。
用法: python tools/freeze_B.py --draft design/design-stageB-draft10.md [--seal records/B/seal-B.json] [--values records/B/freeze-values-B.json] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v2'
REPO = runs_B.REPO
CARRYOVER = {'凍結走行器（組み立てと採点の型）': 'tools/run_preamble_local.py',
             '凍結パーサ': 'arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py',
             '場面の素材': 'arms/frozen-from-ryokai-os/app-scenarios.json'}
TOOLS = ['runs_B.py', 'make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py', 'numbers_lint.py', 'gate_B.py', 'analyze_B.py',
         'integrity_B.py', 'sample_inspection_B.py', 'direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'synth_B.py',
         'dry_run_B.py', 'build_report_B.py', 'freeze_B.py', 'control_chart_B.py']
NEED_VALUES = ['model_rev', 'tokenizer_rev', 'num_hidden_layers', 'layer_indices', 'arm_token_lengths',
               'quality_task', 'quality_input', 'quality_apply_band', 'quality_scoring', 'quality_max_tokens',
               'v_hat_sha256', 'direction_stats']
ap = argparse.ArgumentParser()
ap.add_argument('--draft', required=True)
ap.add_argument('--seal', default=None)
ap.add_argument('--values', default=None, help='凍結時に記帳する値（json・上の NEED_VALUES）')
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-missing', action='store_true', help='記帳の値や封印が揃っていなくても書く（**凍結ではなく点検用**）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
cpath = a.contrasts or runs_B.CPATH
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'FREEZE-RECORD-B.md')
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

frozen = {'canon': {'path': 'design/contrasts-B.json', 'sha16': runs_B.sha16_file(cpath), 'version': T['version']},
          'draft': {'path': os.path.relpath(a.draft, REPO).replace('\\', '/'), 'sha16': runs_B.sha16_file(a.draft)},
          'facts': {'path': 'records/B/design-facts-B.md', 'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'))},
          'report_template': {'path': 'records/B/results-report-template-B.md',
                              'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))},
          'arms': T['arms']['sha16'], 'arm_files': T['arms'].get('files'),
          'tools': {}}
for t in TOOLS:
    p = os.path.join(REPO, 'tools', t)
    frozen['tools'][t] = runs_B.sha16_file(p) if os.path.exists(p) else None
frozen['carryover'] = {}
for name, rel in CARRYOVER.items():
    p = os.path.join(REPO, *rel.split('/'))
    frozen['carryover'][name] = {'path': rel, 'sha16': runs_B.sha16_file(p) if os.path.exists(p) else None}
missing_carry = [n for n, v in frozen['carryover'].items() if not v['sha16']]
missing_tools = [t for t, v in frozen['tools'].items() if v is None]

VALUES = runs_B.read_json(a.values) if a.values else {}
missing_values = [k for k in NEED_VALUES if k not in VALUES or VALUES[k] in (None, '', [], {})]   # **空も欠けと見る**（採否表 P282）
SEAL = runs_B.read_json(a.seal) if a.seal else None
conf_ids = [c['id'] for F in T['families'].values() for c in F['contrasts']]
missing_seal = [] if not SEAL else [i for i in conf_ids if i not in (SEAL.get('signs') or {})]
blockers = []
if missing_tools:
    blockers.append('器材が揃っていない: %s' % '・'.join(missing_tools))
if missing_carry:
    blockers.append('B が依存する凍結物が見つからない: %s' % '・'.join(missing_carry))
if missing_values:
    blockers.append('凍結時に記帳する値が揃っていない: %s' % '・'.join(missing_values))
if SEAL is None:
    blockers.append('封印予想が渡されていない（`seal_format` の様式で、データを一つも見る前に書く）')
else:
    if missing_seal:
        blockers.append('封印の無い確証の対比: %s' % '・'.join(missing_seal))
    if not SEAL.get('s4'):
        blockers.append('**S4 の反証の封印が無い**（正本 seal_format.scope は確証の族と S4 の両方を対象にする）')
    for f in T['seal_format']['fields']:
        pass
    for need in ('information_state', 'timing', 'who'):
        if not SEAL.get(need):
            blockers.append('封印の記録に欄が無い: %s（seal_format.fields）' % need)
if blockers and not a.allow_missing:
    print('[freeze_B] 凍結できない（--allow-missing は点検用）:')
    for b in blockers:
        print('  - ' + b)
    sys.exit(1)

# 整備の記録に載る SHA16 が現物と一致するかを見る（実装検分の採否表 P299——古い記録のまま凍結しない）
import re as _re
rec_path = os.path.join(REPO, 'records', 'B', 'tooling-record-B-2026-09-18.md')
stale = []
if os.path.exists(rec_path):
    _txt = open(rec_path, encoding='utf-8').read()
    for _name, _sha in _re.findall(r'`tools/([\w.]+)` \| [^|]*\| ([0-9A-F]{16})', _txt):
        _p = os.path.join(REPO, 'tools', _name)
        if os.path.exists(_p) and runs_B.sha16_file(_p) != _sha:
            stale.append(_name)
if stale:
    blockers.append('器材の整備の記録の SHA16 が現物と違う（記録を作り直してから凍結する）: %s' % '・'.join(stale))

REC = {'kind': 'freeze_B', 'version': VERSION, 'frozen_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'frozen_jst': jst.strftime('%Y-%m-%d %H:%M'),
       'frozen': frozen, 'values': VALUES, 'seal': SEAL, 'seal_sha256': (None if not a.seal else __import__('hashlib').sha256(open(a.seal, 'rb').read()).hexdigest().upper()),
       'stale_record_hashes': stale, 'blockers': blockers, 'deviations': [],
       'deviation_rule': T['deviation']['rule'], 'record_first': T['publication']['record_first']}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 凍結記録（機械生成・`tools/freeze_B.py` %s）' % VERSION, '',
     '- 凍結の時刻: %s UTC（日本時間 %s）。%s' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'),
                                            '**点検（--allow-missing）であり凍結ではない**' if blockers else '凍結した。'), '',
     '## 凍結物', '', '| 物 | 置き場 | SHA16 |', '|---|---|---|']
for k in ('canon', 'draft', 'facts', 'report_template'):
    L.append('| %s | `%s` | %s |' % (k, frozen[k]['path'], frozen[k]['sha16']))
for t, v in sorted(frozen['tools'].items()):
    L.append('| 器材 | `tools/%s` | %s |' % (t, v or '**無い**'))
for name, v in sorted(frozen['carryover'].items()):
    L.append('| 持ち越しの凍結物 | `%s` | %s |' % (v['path'], v['sha16'] or '**無い**'))
for arm, sha in sorted((frozen['arms'] or {}).items()):
    L.append('| 腕 | %s | %s |' % (arm, sha or '（前置きを持たない）'))
L += ['', '## 凍結時に記帳する値', '']
for k in NEED_VALUES:
    L.append('- %s: %s' % (k, json.dumps(VALUES[k], ensure_ascii=False) if k in VALUES else '**まだ無い**'))
L += ['', '## 封印予想（`seal_format`）', '']
if SEAL:
    L += ['- 時機: %s' % T['seal_format']['timing'], '- 情報状態: %s' % T['seal_format']['information_state'],
          '- 封印した符号: %d／確証の対比 %d' % (len(SEAL.get('signs') or {}), len(conf_ids)),
          '- S4 の反証: %s' % (SEAL.get('s4') or '**まだ無い**'), '- %s' % T['seal_format']['reading']]
else:
    L.append('- **まだ無い**（`seal_format` の様式で、データを一つも見る前に書く）')
if blockers:
    L += ['', '## 凍結を止めているもの', ''] + ['- ' + b for b in blockers]
L += ['', '## 逸脱台帳', '', '- %s' % T['deviation']['rule'], '- %s' % T['deviation']['silent_fix'], '- （凍結の後に足す）', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[freeze_B] %s | 止めているもの %d 件' % (out_md, len(blockers)))
sys.exit(2 if blockers else 0)
```

## `tools/control_chart_B.py`（SHA16 20E5661203A7E628・88 行）

```python
# -*- coding: utf-8 -*-
"""control_chart_B.py v1 —— 段階 B の**校正の管理図**（正本 `calibration`・起草者の見直し S1・実装検分の採否表 P276）。

別置きの校正腕は置かない（試行が増えるため）。代わりに、**無操作の腕の率をセッションごとに並べる**。
  - 点: 腕 × 場面 × セッションの全分母破局率（分子＝破局・分母＝n_ok）。
  - 初点: 同じ腕 × 場面の**最初のセッション**（初点は判定しない）。
  - 帯: `calibration.band_pt`（二標本・両側・厳密 Fisher）。外れたら「器の異常」を記帳し、**その走行を含む対比の確証札に注を付す**。
限界（正本 `calibration.limitation`）: 同じ腕 × 場面が一つのセッションに収まる場合、点は一つだけで管理図にならない。その旨を印字する。
出力: records/B/control-chart-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/control_chart_B.py [--root <results>] [--allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.stats import fisher_exact
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
CAL = T['calibration']
NOOP = set(T['arms']['noop'])
BAND = CAL['band_pt'] / 100.0

idx = runs_B.index_runs(T, T['tags']['main'], a.root, allow_dry=a.allow_dry)
points, anomalies, notes = [], [], []
by_cell = {}
for (sc,), recs in sorted(idx.items()):
    for rec in recs:
        sess = rec['manifest'].get('session')
        for arm, c in runs_B.cell_counts(rec['trials_path']).items():
            if arm not in NOOP:
                continue
            by_cell.setdefault((sc, arm), []).append({'session': sess, 'run_key': rec['run_key'], 'k': c['cat'], 'n': c['n_ok'],
                                                      'rate': runs_B.rate(c['cat'], c['n_ok'])})
for (sc, arm), pts in sorted(by_cell.items(), key=str):
    pts.sort(key=lambda x: (x['session'] is None, x['session']))
    for i, p in enumerate(pts):
        row = dict(p, scenario=sc, arm=arm, first_point=(i == 0))
        if i == 0:
            row['verdict'] = '初点（判定しない）'
        else:
            base = pts[0]
            pval = float(fisher_exact([[p['k'], p['n'] - p['k']], [base['k'], base['n'] - base['k']]])[1])
            d = (p['rate'] or 0) - (base['rate'] or 0)
            out = abs(d) > BAND
            row.update({'diff_pt': round(100 * d, 3), 'p': pval, 'outside': out,
                        'verdict': ('**帯の外**（器の異常を記帳し、この走行を含む対比の確証札に注を付す）' if out else '帯の内側')})
            if out:
                anomalies.append({'scenario': sc, 'arm': arm, 'run_key': p['run_key'], 'diff_pt': row['diff_pt']})
        points.append(row)
    if len(pts) == 1:
        notes.append('%s × %s は点が一つ（%s）——管理図にならない（%s）' % (sc, arm, pts[0]['run_key'], CAL['limitation'][:40] + '…'))

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'control-chart-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p_ in (out_md, out_json):
        if os.path.exists(p_):
            sys.exit('既にある（--force で上書き）: %s' % p_)
json.dump({'kind': 'control_chart_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'band_pt': CAL['band_pt'], 'points': points, 'anomalies': anomalies, 'notes': notes,
           'design': CAL['design'], 'limitation': CAL['limitation']},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 校正の管理図（機械生成・`tools/control_chart_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- %s' % CAL['design'], '- 帯 %g pt・%s・相手は初点（同じ腕 × 場面の最初のセッション）。' % (CAL['band_pt'], CAL['test']),
     '- **帯の外の点 %d 件**。点が一つしかないセル %d 件。' % (len(anomalies), len(notes)), '',
     '| 場面 | 腕 | セッション | 破局/n_ok | 率 | 初点との差 pt | p | 判定 |', '|---|---|---|---|---|---|---|---|']
for p_ in points:
    L.append('| %s | %s | %s | %d/%d | %s | %s | %s | %s |'
             % (p_['scenario'], p_['arm'], p_['session'], p_['k'], p_['n'],
                None if p_['rate'] is None else round(p_['rate'], 4), p_.get('diff_pt', '—'),
                ('%.4g' % p_['p']) if p_.get('p') is not None else '—', p_['verdict']))
if notes:
    L += ['', '## 注（限界）', ''] + ['- ' + n for n in notes]
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[control_chart_B] %s | 点 %d・帯の外 %d・点が一つのセル %d' % (out_md, len(points), len(anomalies), len(notes)))
sys.exit(1 if anomalies else 0)
```
