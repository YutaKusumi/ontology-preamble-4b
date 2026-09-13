# -*- coding: utf-8 -*-
"""gate_A.py v1.1 —— 段階 A のパイロットの門（2026-09-13・登録者裁定 D9 の三つ目の手順・D12 (b)(d)）。規則は design/contrasts-A.json の gate2・calibration.withdrawal・unmeasurable・environment_band・style_gate だけから読む。
v1.1（2026-09-14・実装検分の採否表 P78・P91・P92・登録者裁定 D16）: 再走の seed は撤退条件のセル（4B-2507 × N1）だけに許す。再走の n_ok が零は rerun_no_data（合格に数えない）。門2 の縮小では残らない場面（shrink_scenarios）を記録に書く（その場面の対比だけを判定不能にする）。dry-run の走行は拒む（--allow-dry は検査用）。
検閲は tools/confirm_A.py（Rules と整数の比較）、帯の判定と期待誤保留数は tools/bands_A.py（格子の転記行 I・M と同じ関数）。
- 門2（gate2.unit_rule）: 場面ごとに傾きの族の対比をパイロットの破局数と n_ok で両腕条件の検閲に掛け、残存規模が min_sizes 以上の対比が一本以上ある場面を「残る場面」と数え、
  min_scenarios 未満なら族を縮小（判定不能の枠として m を消費）。門はパイロットで一度（gate2.once・本走行で引き直さない）。
- 撤退条件（calibration.withdrawal）: パイロットの 4B-2507 × Ncold × N1（n=pilot_n）。門0.5 合格なら API 既測に対し下側（一標本）、不合格なら門0.5 の手元 Ncold × N1 に対し下側（二標本）。
  帯を超えたら再走（seed＋seeds.rerun_offset）を探し、無ければ「再走待ち」、再走も超えたら器の異常（本走行の全確証札に注・機種は降格しない）。
- 測定不能（記述・unmeasurable.applied_on）: パイロットの腕 × 規模 × 場面の和集合の率が閾値を超えるセルの一覧（機種を外す規則は置かない・model_rule）。
- 環境帯の選択規則の引き直し（environment_band.pilot_recheck・登録者裁定 D12 (d)）: 腕の率を橋の二機種のパイロット N1 の率の平均に置き、候補ごとの期待誤保留数と規則で選ばれる候補を印字する（帯は動かさない・登録者の裁定に回す）。
- 様式（記述・--style を渡したとき・style_gate.pilot_values）: 対比ごとに全規模で様式門を当てたときの保留と注の見込み本数（閾値は動かさない）。
出力: records/A/gate-<tag>.json と同 .md（既存は --force なしでは上書きしない）。
用法: python tools/gate_A.py [--tag pilotA] --identity records/A/identity-screen-A.json [--style records/A/style-pilotA.json]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import bands_A
import confirm_A
REPO = runs_A.REPO
VERSION = 'v1.1'
ZERO = dict(n=0, n_ok=0, api_error=0, cat=0, refuse=0, ff=0, loop=0, trunc=0, unmeas=0)

ap = argparse.ArgumentParser(); ap.add_argument('--tag', default=None); ap.add_argument('--root', default=None); ap.add_argument('--contrasts', default=None)
ap.add_argument('--identity', required=True); ap.add_argument('--style', default=None); ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true'); ap.add_argument('--allow-incomplete', action='store_true'); ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_A.load_T(a.contrasts); R = confirm_A.Rules(T); tag = a.tag or T['tags']['pilot']; SIZES = T['sizes']; SC = T['scenarios']; ARMS = T['arms']['preamble']
ANCHOR = next(m['key'] for m in T['models'] if m['anchor']); FAM = T['families']['A_slope']; G2 = T['gate2']; CAL = T['calibration']; WD = CAL['withdrawal']; S = T['seeds']; EB = T['environment_band']; BR = T['bridge']
OUT = a.out or os.path.join(REPO, 'records', 'A', 'gate-%s' % tag)
if (os.path.exists(OUT + '.json') or os.path.exists(OUT + '.md')) and not a.force:
    sys.exit('出力が既にある（門はパイロットで一度・上書きしない・--force で置き換え）: %s' % OUT)
ID = runs_A.read_json(a.identity)
if ID.get('kind') != 'identity_screen_A':
    sys.exit('--identity は tools/identity_screen_A.py の出力を渡す')
BRANCH = ID['verdict']

# ---- 走行（登録の seed と再走の seed）
try:
    IDXM = runs_A.index_runs(T, tag, a.root, allow_multi=True, allow_dry=a.allow_dry)
except RuntimeError as ex:
    sys.exit('読み出しで止まった（%s）' % ex)
REG = {}; RERUN = {}; missing = []; unknown = []
for m in T['models']:
    for sc in SC:
        recs = IDXM.get((m['key'], sc), []); s0 = S['pilot'][m['key']][sc]
        for r in recs:
            if r['seed'] == s0:
                REG[(m['key'], sc)] = r
            elif r['seed'] == s0 + S['rerun_offset'] and (m['key'], sc) == (ANCHOR, CAL['scenario']):   # 再走の seed は撤退条件のセルだけ（採否表 P92）
                RERUN[(m['key'], sc)] = r
            else:
                unknown.append(r['run_key'])
        if (m['key'], sc) not in REG:
            missing.append('%s × %s' % (m['key'], sc))
if unknown:
    sys.exit('登録に無い seed の走行: %s' % unknown)
if missing and not a.allow_incomplete:
    sys.exit('パイロットの走行が足りない（--allow-incomplete は検査用）: %s' % '・'.join(missing))
C = {}
for (mk, sc), rec in REG.items():
    for arm, c in runs_A.cell_counts(rec['trials_path']).items():
        C[(mk, sc, arm)] = c
cnt = lambda mk, sc, arm: C.get((mk, sc, arm)) or ZERO

# ---- 門2
per_sc = {}
for sc in SC:
    items = []
    for c in [x for x in FAM['contrasts'] if x['scenario'] == sc]:
        kept = []
        for s in SIZES:
            ca, cb = cnt(s, sc, c['A']), cnt(s, sc, c['B'])
            if not (ca['n_ok'] and cb['n_ok']):
                continue
            low_both = bool(confirm_A._lt(ca['cat'], ca['n_ok'], R.low) and confirm_A._lt(cb['cat'], cb['n_ok'], R.low))
            high_both = bool(confirm_A._gt(ca['cat'], ca['n_ok'], R.high) and confirm_A._gt(cb['cat'], cb['n_ok'], R.high))
            if not (low_both or high_both):
                kept.append(s)
        items.append({'id': c['id'], 'kept': kept, 'kept_n': len(kept)})
    per_sc[sc] = {'remains': any(x['kept_n'] >= G2['min_sizes'] for x in items), 'contrasts': items}
REMAIN = [sc for sc in SC if per_sc[sc]['remains']]; SHRINK = len(REMAIN) < G2['min_scenarios']

# ---- 撤退条件（合否二分・再走）
bb = T['bases_4B2507_api'][CAL['scenario']][CAL['arm']]; BASE = Fraction(bb['k'], bb['n'])


def wd_eval(c):
    k, n = c['cat'], c['n_ok']
    if n == 0:
        return {'k': 0, 'n': 0, 'fired': None, 'note': 'n_ok が零'}
    if BRANCH == 'pass':
        return {'k': k, 'n': n, 'rate': k / n, 'fired': bands_A.below_base(k, n, BASE, WD['band_pt']), 'reference': {'api': [bb['k'], bb['n']]}, 'test': '一標本・下側'}
    loc = ID['local_counts'][CAL['arm']]
    return {'k': k, 'n': n, 'rate': k / n, 'fired': bands_A.below_band(k, n, loc['catastrophe'], loc['n_ok'], WD['band_pt']), 'reference': {'gate05_local': [loc['catastrophe'], loc['n_ok']]}, 'test': '二標本・下側'}


W0 = wd_eval(cnt(ANCHOR, CAL['scenario'], CAL['arm'])); W1 = None
if W0['fired'] is None:
    WSTATUS, WANOM = 'no_data', False
elif not W0['fired']:
    WSTATUS, WANOM = 'pass', False
elif (ANCHOR, CAL['scenario']) not in RERUN:
    WSTATUS, WANOM = 'rerun_required', False
else:
    W1 = wd_eval(runs_A.cell_counts(RERUN[(ANCHOR, CAL['scenario'])]['trials_path']).get(CAL['arm'], ZERO))
    if W1['fired'] is None:   # 再走の n_ok が零は合格に数えない（採否表 P91）
        WSTATUS, WANOM = 'rerun_no_data', False
    else:
        WANOM = bool(W1['fired']); WSTATUS = 'anomaly' if WANOM else 'rerun_pass'

# ---- 測定不能（記述）
UT = Fraction(str(T['unmeasurable']['threshold'])); UM = []
for m in T['models']:
    for sc in SC:
        for arm in ARMS:
            c = cnt(m['key'], sc, arm)
            if c['n_ok'] and Fraction(c['unmeas'], c['n_ok']) > UT:
                UM.append({'model': m['key'], 'scenario': sc, 'arm': arm, 'union': c['unmeas'], 'n_ok': c['n_ok'], 'format_fail': c['ff'], 'loop': c['loop'], 'truncated': c['trunc']})
UM_SHARE = {m['key']: sum(1 for x in UM if x['model'] == m['key']) / (len(SC) * len(ARMS)) for m in T['models']}

# ---- 環境帯の選択規則の引き直し（記述・帯は動かさない）
RATES = {}; RATE_SRC = {}
for arm in ARMS:
    vals = [Fraction(cnt(bm, BR['scenario'], arm)['cat'], cnt(bm, BR['scenario'], arm)['n_ok']) for bm in BR['cells'] if cnt(bm, BR['scenario'], arm)['n_ok']]
    RATES[arm] = float(sum(vals) / len(vals)) if vals else EB['rule_missing_base_rate']; RATE_SRC[arm] = 'pilot_mean_%d' % len(vals) if vals else 'rule_missing_base_rate'
CANDS = {}
for b in EB['candidates_pt']:
    eh, q = bands_A.env_expected_held(RATES, b, BR['n'], FAM['contrasts'], len(BR['cells'])); CANDS[str(b)] = {'expected_false_held_contrasts': eh}
OKC = [b for b in EB['candidates_pt'] if CANDS[str(b)]['expected_false_held_contrasts'] <= EB['rule_expected_max']]
ENV = {'rates_used': RATES, 'rate_source': RATE_SRC, 'candidates': CANDS, 'selected_by_rule_at_pilot': min(OKC) if OKC else None, 'registered_band_pt': EB['band_pt'],
       'registered_meets_rule_at_pilot': CANDS[str(EB['band_pt'])]['expected_false_held_contrasts'] <= EB['rule_expected_max'], 'note': EB['pilot_recheck']}

# ---- 様式（記述）
STYLE = None
if a.style:
    ST = runs_A.read_json(a.style)
    if ST.get('kind') != 'response_mode_A':
        sys.exit('--style は tools/response_mode_A.py の出力を渡す')
    g = lambda s, sc, arm, k: ((ST['cells'].get(s) or {}).get(sc) or {}).get(arm, {}).get(k, 0)
    hold = []; note = []
    for c in FAM['contrasts']:
        sc = c['scenario']; col = lambda arm, k: [g(s, sc, arm, k) for s in SIZES]
        fl = confirm_A.style_flags(R, col(c['A'], 'a_final'), col(c['B'], 'a_final'), col(c['A'], 'b_final'), col(c['B'], 'b_final'), col(c['A'], 'n_ok'), col(c['B'], 'n_ok'), [True] * len(SIZES))
        (hold if fl['state'] == 'hold' else note if fl['state'] == 'note' else []).append({'id': c['id'], 'max_diff_pt': fl['max_diff_pt']})
    STYLE = {'hold_if_applied': hold, 'note_if_applied': note, 'b_rates': {'%s|%s|%s' % (s, sc, arm): (g(s, sc, arm, 'b_final') / g(s, sc, arm, 'n_ok')) if g(s, sc, arm, 'n_ok') else None
                                                                          for s in SIZES for sc in SC for arm in ARMS}, 'note': T['style_gate']['pilot_values']}

RES = {'kind': 'gate_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'tag': tag, 'root': a.root, 'identity_verdict': BRANCH,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(a.contrasts or runs_A.CPATH), 'identity_sha16': runs_A.sha16_file(a.identity), 'style_sha16': runs_A.sha16_file(a.style) if a.style else None,
                  'gate_A': runs_A.sha16_file(os.path.abspath(__file__)), 'bands_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'bands_A.py')), 'confirm_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'confirm_A.py'))},
       'missing': missing, 'dev_marks': [x for x, on in (('allow_incomplete', bool(missing)), ('allow_dry', a.allow_dry)) if on] + sorted({mk_ for r_ in list(REG.values()) + list(RERUN.values()) for mk_ in (r_.get('dry_marks') or [])}),
       'gate2': {'shrink': SHRINK, 'remaining_scenarios': REMAIN, 'shrink_scenarios': [sc for sc in SC if sc not in REMAIN] if SHRINK else [], 'rule_shrink': G2['rule'], 'min_sizes': G2['min_sizes'], 'min_scenarios': G2['min_scenarios'], 'per_scenario': per_sc, 'rule': G2['unit_rule']},
       'withdrawal': {'branch': BRANCH, 'band_pt': WD['band_pt'], 'first': W0, 'rerun': W1, 'status': WSTATUS, 'anomaly': WANOM, 'consequence': WD['rerun']},
       'unmeasurable_pilot': UM, 'unmeasurable_share_by_model': UM_SHARE, 'env_band_recheck': ENV, 'style_pilot': STYLE,
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(RES, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1, default=float)
M = ['# 段階 A パイロットの門（機械生成・`tools/gate_A.py` %s・%s UTC）' % (VERSION, RES['generated_utc']), '', '- tag %s・門0.5 の判定 %s・入力 %s・足りない走行 %s' % (tag, BRANCH, json.dumps(RES['inputs'], ensure_ascii=False), '・'.join(missing) or 'なし'), '',
     '## 門2', '', '- **族の縮小: %s**（残る場面 %d／閾値 %d 未満で縮小: %s）' % ('あり' if SHRINK else 'なし', len(REMAIN), G2['min_scenarios'], '・'.join(REMAIN) or 'なし'), '- 規則: %s' % G2['unit_rule'], '- 縮小の範囲: %s' % G2['rule'], '',
     '| 場面 | 残る | 対比ごとの残存規模数 |', '|---|---|---|']
M += ['| %s | %s | %s |' % (sc, '残る' if per_sc[sc]['remains'] else '—', '・'.join('%s %d' % (x['id'].split(':', 1)[1], x['kept_n']) for x in per_sc[sc]['contrasts'])) for sc in SC]
M += ['', '## 撤退条件（%s・帯 %s pt・下側・超）' % ('合格枝' if BRANCH == 'pass' else '不合格枝', WD['band_pt']), '', '- 判定: **%s**・器の異常: %s' % (WSTATUS, 'あり' if WANOM else 'なし'),
      '- 初回: %s' % json.dumps(W0, ensure_ascii=False, default=float), '- 再走: %s' % (json.dumps(W1, ensure_ascii=False, default=float) if W1 else 'なし'), '- 帰結の規則: %s' % WD['rerun'], '',
      '## 測定不能（パイロット・記述・機種を外す規則は置かない）', ''] + (['- %s × %s × %s: 和集合 %d/%d（書式外 %d・ループ %d・切り詰め %d）' % (x['model'], x['scenario'], x['arm'], x['union'], x['n_ok'], x['format_fail'], x['loop'], x['truncated']) for x in UM] or ['- なし'])
M += ['', '## 環境帯の選択規則の引き直し（記述・帯は動かさない・登録者の裁定に回す）', '', '| 候補（pt） | 期待誤保留数 |', '|---|---|'] + ['| %s | %.4f |' % (b, v['expected_false_held_contrasts']) for b, v in CANDS.items()]
M += ['', '- パイロットの率で規則に選ばれる候補: %s・登録の帯 %s pt が規則を満たすか: %s' % (ENV['selected_by_rule_at_pilot'], EB['band_pt'], '満たす' if ENV['registered_meets_rule_at_pilot'] else '満たさない（登録者の裁定に回す）')]
if STYLE:
    M += ['', '## 様式（記述・閾値は動かさない）', '', '- 全規模で様式門を当てたときの見込み: 保留 %d 本・注 %d 本' % (len(STYLE['hold_if_applied']), len(STYLE['note_if_applied']))]
M += ['', RES['clause']]
open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[gate_A] 門2 縮小 %s（残る場面 %s）・撤退条件 %s・測定不能 %d セル・環境帯の引き直し %s written %s.{json,md}' % (SHRINK, REMAIN, WSTATUS, len(UM), ENV['selected_by_rule_at_pilot'], OUT))
