# -*- coding: utf-8 -*-
"""gate_B.py v2 —— 段階 B の**門1 と選定**（品質床の判定・希釈の門・床と天井・操作有効性・同値の帯・同点の割り方・非正の停止）。

正本 `design/contrasts-B.json` の `quality_floor`・`dilution_gate`・`selection`・`gate1`・`censor`・`print_strings` に従う。
入力: 調整走行（tag `tuneB`）と品質床の**選定の段**（tag `stageB-quality`・stage=selection）の走行の記録。
出力: records/B/gate-B-<日付>.{md,json}（既存は --force なしでは上書きしない）。
判定:
  (1) 品質床（selection_cells）: 介入の腕の正答数と、同じ腕の無操作の正答数の差（pt）。差が threshold_pt の内側なら合格（**ちょうどは不合格**・boundary_rule）。
      候補の合格＝確証族の二つの土台の**両方**が合格（pass_rule）。
  (2) 門1: 合格する候補が一つも無ければ閉じる（`gate1.rule`・「操作不能」を記帳）。**方向の非存在は記帳しない。**
  (3) 希釈の門（選定・裁定 D76）: 候補の v 腕と v_random 腕の書式外率の差・refuse 率の差が threshold_pt 超なら、その候補を選定から外す。
  (4) 床と天井（採否表 P247）: 両腕とも censor.low 未満、または両腕とも censor.high 超の候補は外す。
  (5) 操作有効性＝ v_random の全分母破局率 − v の全分母破局率（pt・低下が正）。**点推定が最大**の候補を採る（裁定 D68）。同点は**無作為**（seeds.tiebreak・裁定の採否表 P228）。
  (6) 同値の帯: 候補横断の**最大統計量**で出す（帰無の模擬・反復数と区間を併記・`report_rules.mc_reporting`）。帯は決め方に使わず、一覧として印字する。
  (7) 非正の停止（裁定 D83）: 残った候補の有効性の点推定が全て零以下なら、**本走行に進まず登録者に上げる**（費用の停止規則・門1 の判定は変えない）。
用法: python tools/gate_B.py [--root <results の代わり>] [--out <md>] [--force] [--reps 20000]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v2'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--reps', type=int, default=20000)
ap.add_argument('--allow-dry', action='store_true', help='検査用の口（dry-run の走行を読む・印を出力に残す）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
SEL, QF, DG, CEN = T['selection'], T['quality_floor'], T['dilution_gate'], T['censor']
EX = T['extraction_scenarios']
LAYERS, COEFS = SEL['candidates']['layers'], SEL['candidates']['coefficients']
CANDS = [(l, c) for l in LAYERS for c in COEFS]
assert len(CANDS) == SEL['candidates']['count'], '候補の数が正本と合わない'
V_ARM, R_ARM = SEL['tune']['arms']                      # ['Onull+v', 'Onull+vrand']
QF_ARMS = QF['arms']                                    # ['O-Ncold', 'Onull']
QF_OPS = {'O-Ncold': '-v', 'Onull': '+v'}               # 減算族の土台は引き、加算族の土台は足す（quality_floor.operations）
rate = runs_B.rate

# ---- 走行の記録 ----
CT, idx_tune = runs_B.counts_tune(T, root=a.root, allow_dry=a.allow_dry)
CQ, idx_q = runs_B.counts_quality(T, root=a.root, allow_dry=a.allow_dry)
DRY = sorted({m for recs in list(idx_tune.values()) + list(idx_q.values()) for r in recs for m in r['dry_marks']})


def tune_pooled(layer, coef, arm):
    """抽出場面をまとめた件数（selection.tune.pooled）。"""
    acc = dict(runs_B.ZERO)
    for sc in EX:
        c = CT.get((sc, layer, coef, arm))
        if c is None:
            return None
        for k in acc:
            acc[k] += c[k]
    return acc


# ---- (1) 品質床（選定の段） ----
THR = QF['threshold_pt']
qrows = []
def partner(stage, base, session):
    """無操作の相手を**同じセッション**から引く（裁定 D92・合算しない・採否表 P261）。"""
    return CQ.get((stage, base, None, None, session))


for base in QF_ARMS:
    for (l, c) in CANDS:
        arm = base + QF_OPS[base]
        cells = {k: v for k, v in CQ.items() if k[0] == 'selection' and k[1] == arm and k[2] == l and k[3] == c}
        if len(cells) > 1:
            qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': True,
                          'note': '同じセルの走行が %d セッションに分かれている（相手も分ける・裁定 D92）' % len(cells)})
            continue
        cell = next(iter(cells.values()), None)
        session = next(iter(cells), (None,) * 5)[4] if cells else None
        noop = partner('selection', base, session)
        if cell is None or noop is None:
            qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': True,
                          'note': '走行の記録が無い（%s）' % ('セル' if cell is None else '同じセッションの相手')})
            continue
        n = QF['denominator']
        d_pt = 100.0 * (cell['correct'] - noop['correct']) / n
        qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': False,
                      'correct': cell['correct'], 'noop_correct': noop['correct'], 'n': n,
                      'diff_pt': round(d_pt, 3), 'boundary': abs(d_pt - THR) < 1e-9, 'pass': d_pt > THR})
qpass = {(l, c): all(r['pass'] for r in qrows if not r['missing'] and (r['layer'], r['coef']) == (l, c))
         and len([r for r in qrows if not r['missing'] and (r['layer'], r['coef']) == (l, c)]) == len(QF_ARMS) for (l, c) in CANDS}

# ---- (3)(4)(5) 候補ごとの指標 ----
rows = []
for (l, c) in CANDS:
    v, r = tune_pooled(l, c, V_ARM), tune_pooled(l, c, R_ARM)
    row = {'layer': l, 'coef': c, 'quality_pass': bool(qpass[(l, c)]), 'missing': v is None or r is None}
    if not row['missing']:
        pv, pr = rate(v['cat'], v['n_ok']), rate(r['cat'], r['n_ok'])
        ffv, ffr = rate(v['ff'], v['n_ok']), rate(r['ff'], r['n_ok'])
        rfv, rfr = rate(v['refuse'], v['n_ok']), rate(r['refuse'], r['n_ok'])
        row.update({'n_ok_v': v['n_ok'], 'n_ok_r': r['n_ok'], 'cat_v': v['cat'], 'cat_r': r['cat'],
                    'rate_v': None if pv is None else round(pv, 5), 'rate_r': None if pr is None else round(pr, 5),
                    'eff_pt': None if (pv is None or pr is None) else round(100.0 * (pr - pv), 3),
                    'ff_pt_v': runs_B.pt(ffv), 'ff_pt_r': runs_B.pt(ffr), 'refuse_pt_v': runs_B.pt(rfv), 'refuse_pt_r': runs_B.pt(rfr)})
        row['ff_diff_pt'] = None if None in (ffv, ffr) else round(100.0 * abs(ffv - ffr), 3)
        row['refuse_diff_pt'] = None if None in (rfv, rfr) else round(100.0 * abs(rfv - rfr), 3)
        row['dilution_fail'] = [k for k, val in (('書式外', row['ff_diff_pt']), ('refuse', row['refuse_diff_pt']))
                                if val is not None and val > DG['threshold_pt']]
        both_low = (pv is not None and pr is not None and pv < CEN['low'] and pr < CEN['low'])
        both_high = (pv is not None and pr is not None and pv > CEN['high'] and pr > CEN['high'])
        row['censored'] = bool(both_low or both_high)
        row['censor_side'] = '床' if both_low else ('天井' if both_high else None)
    row['eligible'] = bool(row.get('quality_pass') and not row.get('missing') and not row.get('dilution_fail') and not row.get('censored'))
    rows.append(row)

# ---- (2) 門1 ----
n_qpass = sum(1 for (l, c) in CANDS if qpass[(l, c)])
n_missing = len({(r['layer'], r['coef']) for r in qrows if r.get('missing')})
gate1_open = n_qpass > 0
incomplete = n_missing > 0          # 記録の不在は「操作不能」と区別する（採否表 P272）

# ---- (5)(6)(7) 選定 ----
# 同点の割り方の種に**データ由来の値**を混ぜる（固定の種だけだと「添字の小さい方」に偏る・実装検分の軽微1）
_tie_mix = int(hashlib.sha256(json.dumps([[r.get('layer'), r.get('coef'), r.get('cat_v'), r.get('cat_r')] for r in rows],
                                          ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:8], 16)
rng = np.random.default_rng([T['seeds']['tiebreak'], _tie_mix])
rng_band = np.random.default_rng([T['seeds']['tiebreak'] + 1, _tie_mix])   # 帯の模擬は別の流れ（軽微2）
elig = [r for r in rows if r['eligible'] and r.get('eff_pt') is not None]
pick, tie_note, band, tied, stop = None, None, None, [], None
if gate1_open and elig:
    best = max(r['eff_pt'] for r in elig)
    top = [r for r in elig if abs(r['eff_pt'] - best) < 1e-9]
    if len(top) > 1:                                   # 同点は無作為に割る（selection.tie_break）
        pick = top[int(rng.integers(len(top)))]
        tie_note = '同点 %d 組を無作為に割った（種 %s）' % (len(top), T['seeds']['tiebreak'])
    else:
        pick = top[0]
    if best <= 0:                                      # 非正の停止（裁定 D83）
        stop = '全候補の操作有効性の点推定が零以下（最大 %.2f pt）。本走行に進む前に登録者に上げる。' % best
    # 同値の帯（候補横断の最大統計量・帰無の模擬）
    n_v = int(np.mean([r['n_ok_v'] for r in elig]))
    n_r = int(np.mean([r['n_ok_r'] for r in elig]))
    p0 = float(np.mean([(r['cat_v'] + r['cat_r']) / max(r['n_ok_v'] + r['n_ok_r'], 1) for r in elig]))
    k = len(elig)
    sim_v = rng_band.binomial(n_v, p0, size=(a.reps, k)) / max(n_v, 1)
    sim_r = rng_band.binomial(n_r, p0, size=(a.reps, k)) / max(n_r, 1)
    eff = 100.0 * (sim_r - sim_v)
    spread = eff.max(axis=1) - eff.min(axis=1)
    q95 = float(np.quantile(spread, 0.95))
    half = 1.96 * float(np.std(spread)) / math.sqrt(a.reps)
    band = {'q95_pt': round(q95, 3), 'reps': a.reps, 'mc_half_pt': round(half, 4), 'null_rate': round(p0, 5),
            'rule': '帰無（全候補が同じ）で、候補横断の最大と最小の差が %g 分位に収まる幅。最大の候補との差がこの幅の内側の候補を同値として一覧に出す（決め方には使わない）' % 0.95}
    tied = [{'layer': r['layer'], 'coef': r['coef'], 'eff_pt': r['eff_pt']} for r in elig if (best - r['eff_pt']) <= q95]

PS = T['print_strings']
lines = []
if not gate1_open:
    lines.append(PS['gate1_closed'])
else:
    if pick is None:
        lines.append('門1: 品質床に合格する層 × 係数は %d 組あるが、**選定の対象が残らなかった**（希釈の門・床と天井で全候補が外れた）。'
                     '正本 selection.censor により、非正の停止と同じ扱いにして登録者に上げる。' % n_qpass)
    else:
        lines.append(PS['gate1_open'].format(k=n_qpass, layer=pick.get('layer'), coef=pick.get('coef'),
                                             eff=pick.get('eff_pt'), tied=len(tied)))
lines.append(PS['selection_coi'])
lines.append(PS['selection_direction'])
if stop:
    lines.append(PS['nonpositive'].format(eff=max((r['eff_pt'] for r in elig), default=None)))

verdict = ('incomplete' if incomplete else ('closed' if not gate1_open else ('escalate' if (stop or not elig) else 'open')))
if incomplete:
    lines.insert(0, '品質床の走行の記録が %d 候補ぶん欠けている。**記録の不在は「操作不能」ではない**——揃えてから門1 を判定する（採否表 P272）。' % n_missing)
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'gate-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

REC = {'kind': 'gate_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
       'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'verdict': verdict,
       'gate1': {'open': gate1_open, 'quality_pass_candidates': n_qpass, 'rule': T['gate1']['rule']},
       'quality_floor_rows': qrows, 'candidates': rows,
       'selection': {'pick': pick, 'tie_note': tie_note, 'equivalence_band': band, 'tied': tied, 'nonpositive_stop': stop},
       'dry_marks': DRY, 'print': lines}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

L = ['# 段階 B 門1 と選定（機械生成・`tools/gate_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 正本 SHA16 %s。判定: **%s**。品質床に合格する候補 %d／%d。' % (REC['contrasts_sha16'], verdict, n_qpass, len(CANDS)), '']
if DRY:
    L += ['- **dry-run の走行を読んだ（検査用）**: %s' % '・'.join(DRY), '']
L += ['## 候補ごとの指標', '', '| 層 | 係数 | 品質床 | 書式外の差 pt | refuse の差 pt | 床・天井 | 有効性 pt | 選定の対象 |', '|---|---|---|---|---|---|---|---|']
for r in rows:
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s |'
             % (r['layer'], r['coef'], '合格' if r.get('quality_pass') else '不合格',
                r.get('ff_diff_pt'), r.get('refuse_diff_pt'), r.get('censor_side') or '—',
                r.get('eff_pt'), '○' if r['eligible'] else '×（%s）' % ('・'.join(r.get('dilution_fail') or []) or ('床・天井' if r.get('censored') else ('品質床' if not r.get('quality_pass') else '記録が無い')))))
L += ['', '## 品質床（選定の段）', '', '| 土台 | 腕 | 層 | 係数 | 正答 | 無操作 | 差 pt | 判定 |', '|---|---|---|---|---|---|---|---|']
for r in qrows:
    if r.get('missing'):
        L.append('| %s | %s | %s | %s | — | — | — | 記録が無い |' % (r['base'], r['arm'], r['layer'], r['coef']))
    else:
        L.append('| %s | %s | %s | %s | %d | %d | %.2f | %s |' % (r['base'], r['arm'], r['layer'], r['coef'], r['correct'], r['noop_correct'], r['diff_pt'],
                                                                  ('合格' if r['pass'] else '不合格') + ('（境目に一致）' if r['boundary'] else '')))
L += ['', '## 印字（正本 print_strings）', ''] + ['- ' + s for s in lines]
if band:
    L += ['', '- 同値の帯（候補横断の最大統計量・帰無の模擬 %s 回・%s 区間の半幅 ±%.4f pt）: 幅 %.2f pt・同値の候補 %d 組。'
          % (format(a.reps, ','), '95%', band['mc_half_pt'], band['q95_pt'], len(tied))]
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[gate_B] %s / %s | 判定 %s | 品質床の合格 %d/%d | 選定 %s' % (out_md, out_json, verdict, n_qpass, len(CANDS), (pick or {}).get('layer')))
sys.exit(0 if verdict == 'open' else 2)
