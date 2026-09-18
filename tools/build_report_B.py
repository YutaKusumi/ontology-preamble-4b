# -*- coding: utf-8 -*-
"""build_report_B.py v1 —— 段階 B の結果報告を、**雛形**（`records/B/results-report-template-B.md`）と集計の出力から組み立てる。

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

VERSION = 'v1'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--analysis', required=True)
ap.add_argument('--gate', required=True)
ap.add_argument('--integrity', default=None)
ap.add_argument('--sampling', default=None)
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
out_md = a.out or os.path.join(REPO, 'records', 'B', 'results-report-B.md')
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
tpl = open(a.template, encoding='utf-8').read()
PS = T['print_strings']
c = A['counts']
n_conf = sum(x['m'] for x in T['families'].values())


def block(lines):
    return '\n'.join(lines)


A_sum = block([
    '```',
    PS['first_finding'].format(confirmed=c['確証'], undecidable=c['判定不能（検閲）'], qfloor=c['判定不能（品質床）'],
                               ff=c['判定保留（書式外転位）'], refuse=c['判定保留（refuse 転位）'] + c['判定保留（refuse 転位・差）'],
                               style=c['判定保留（様式転位）'], ns=c['非有意']),
    PS['scope'],
    'S4 の反証: %s' % A['s4'].get('verdict'),
    '```'])
B_run = block(['```',
               '整合検査: %s' % ('不整合 %d 件・注 %d 件（%s）' % (len(INT['problems']), len(INT['notes']), INT['tag']) if INT else '（記録が渡されていない）'),
               '抽出検査: %s' % ('標本 %d 件・対応表の封印あり' % SMP.get('n_items', 0) if SMP else '（記録が渡されていない）'),
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
rows = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | pt 差 | 区間 | p | 書式外の差 | refuse の差 | 様式の差 | 札 |', '|---|---|---|---|---|---|---|---|---|---|---|']
for r in A['confirm']:
    if r.get('missing'):
        rows.append('| %s | %s | — | — | — | — | — | — | — | — | %s |' % (r['id'], r['scenario'], r['label']))
        continue
    rows.append('| %s | %s | %d/%d | %d/%d | %s | %s | %s | %s | %s | %s | %s |'
                % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'], r['diff_pt'], r['ci'],
                   None if r['p'] is None else round(r['p'], 5), r.get('ff_diff_pt'), r.get('refuse_diff_pt'), r.get('style_diff_pt'), r['label']))
D_conf = block(rows)
sg = A['sign_agreement']
E_sign = block(['```', (PS['sign_agreement'].format(agree=sg['agree'], confirmed=sg['confirmed']) if sg['sealed']
                        else '封印の記録が渡されていないので、予想符号との照合は行っていない。'), '```'])
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
               if 'power_at_effect' in s4 else ''),
              '封印: %s' % s4.get('sealed_prediction'), '```'])
H_coi = block(['```', T['selection']['coi_note'], T['publication']['dual_use'][:0] or '',
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
