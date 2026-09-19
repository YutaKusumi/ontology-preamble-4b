# 器材のソース（逐語・核）（必読・関わる問い (b)(c)(d)(e)・機械生成・2026-09-19 01:57 UTC）

## `tools/gate_B.py`（SHA16 A5A50C1DD3023DAA・276 行）

```python
# -*- coding: utf-8 -*-
"""gate_B.py v4 —— 段階 B の**門1 と選定**（品質床の判定・api_error の門・希釈の門・床と天井・操作有効性・同値の帯・同点の割り方・非正の停止）。

正本 `design/contrasts-B.json` の `quality_floor`・`dilution_gate`・`selection`・`gate1`・`censor`・`print_strings` に従う。
入力: 調整走行（tag `tuneB`）と品質床の**選定の段**（tag `stageB-quality`・stage=selection）の走行の記録。
出力: records/B/gate-B-<日付>.{md,json}（既存は --force なしでは上書きしない）。
判定:
  (1) 品質床（selection_cells）: 介入の腕の正答数と、同じ腕の無操作の正答数の差（pt）。差が threshold_pt の内側なら合格（**ちょうどは不合格**・boundary_rule）。
      候補の合格＝確証族の二つの土台の**両方**が合格（pass_rule）。
      **api_error の率（分母は全試行）が腕と相手で api_error_gate_pt を超えて違うセルは判定しない**（合格に数えない・裁定 D127・v4 で足した・`rules_B.api_error_gate`）。
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
import rules_B

VERSION = 'v4'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--reps', type=int, default=20000)
ap.add_argument('--allow-dry', action='store_true', help='検査用の口（dry-run の走行を読む・印を出力に残す）')
ap.add_argument('--allow-no-sessions', action='store_true', help='検査用の口（セッション記録が無くても走る・裁定 D126）')
ap.add_argument('--allow-missing-cells', action='store_true', help='検査用の口（登録された升目が欠けていても走る・裁定 D126）')
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

# ---- セッション記録（正本 sessions.enforced_by・裁定 D126・2026-09-18） ----
# 正本は「門・集計器・整合検査の**三つ**が確かめる」と書いているのに、門は一度も読んでいなかった
# （系統外の検分で、記録を丸ごと消しても判定 open・終了コード 0 で通ることが示された・採否表 P349）。
_SESS = runs_B.sessions_by_run_key(runs_B.load_sessions(a.root))
_miss = sorted({rec['run_key'] for recs in list(idx_tune.values()) + list(idx_q.values())
                for rec in recs if rec['run_key'] not in _SESS})
if _miss and not a.allow_no_sessions:
    sys.exit('走行キーのセッション記録が無い（正本 sessions.missing_rule・裁定 D126）: %s%s。検査用は --allow-no-sessions'
             % ('・'.join(_miss[:6]), ' ほか %d 件' % (len(_miss) - 6) if len(_miss) > 6 else ''))

# ---- 登録された升目の欠け（裁定 D126・採否表 P361） ----
# 調整走行の升目が欠けると候補は黙って選定から外れるが、判定は open のままだった。
_want_tune = {(sc, l, c, arm) for sc in EX for (l, c) in CANDS for arm in (V_ARM, R_ARM)}
_gap_tune = sorted(_want_tune - set(CT), key=str)


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
        # **相手のセルに走行が二本以上あれば止める**（正本 sessions.partner_duplicate_rule・裁定 D126）。
        # 鍵の種類は数えても鍵の中の本数は数えていなかったので、同じ番号の二本が黙って合算され、
        # 分母が倍になって門1 が誤って閉じる形が残っていた（採否表 P360）。
        if noop is not None and noop.get('n', 0) > QF['items']:
            qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': True,
                          'note': '無操作の相手の試行が %d 件あり、登録の %d 件を超える（走行が二本以上ある・裁定 D126）'
                                  % (noop.get('n', 0), QF['items'])})
            continue
        if cell is None or noop is None:
            qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': True,
                          'note': '走行の記録が無い（%s）' % ('セル' if cell is None else '同じセッションの相手')})
            continue
        # **api_error の率の差が門を超えたら、そのセルの品質床を判定しない**（正本 quality_floor.api_error_gate・裁定 D127・`rules_B.api_error_gate`）。
        # 判定しないセルは合格に数えない。v3 までは api_error を列に出すだけで、この門は無かった（直しの監査・2026-09-19）。
        if rules_B.api_error_gate(cell, noop, T):
            qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': True,
                          'api_error': cell.get('api_error', 0), 'noop_api_error': noop.get('api_error', 0),
                          'note': '判定しない（api_error の率の差が %g pt を超える・裁定 D127）' % QF['api_error_gate_pt']})
            continue
        gap = cell.get('scoring_gap', 0) + noop.get('scoring_gap', 0)
        if gap:                                   # **採点欠落があれば判定しない**（裁定 D103・採否表 P319）
            qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': True, 'scoring_gap': gap,
                          'note': '判定欄が空の試行が %d 件ある（採点が済むまで判定しない・裁定 D103）' % gap})
            continue
        if not cell['n_ok'] or not noop['n_ok']:  # 使えた試行が零（裁定 D110 と同じ扱い）
            qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': True,
                          'note': '使えた試行が零（測れなかった）'})
            continue
        # **分母は、腕と相手のそれぞれで使えた試行**（裁定 D104・採否表 P305）。
        # 固定の 200 を分母にすると、荒れたセッションがそのまま「介入が課題を壊した」に化け、選ばれる層 × 係数まで変わる。
        d_pt = 100.0 * (cell['correct'] / cell['n_ok'] - noop['correct'] / noop['n_ok'])
        qrows.append({'base': base, 'arm': arm, 'layer': l, 'coef': c, 'missing': False,
                      'correct': cell['correct'], 'noop_correct': noop['correct'],
                      'n_ok': cell['n_ok'], 'noop_n_ok': noop['n_ok'],
                      'api_error': cell.get('api_error', 0), 'noop_api_error': noop.get('api_error', 0),
                      'items': QF['denominator'],
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
        # **帯の境目に一致した値は印字する**（正本 report_rules.band_edge・裁定 D115・採否表 P332）
        row['censor_boundary'] = [name for name, val, thr in
                                  (('床', pv, CEN['low']), ('床', pr, CEN['low']), ('天井', pv, CEN['high']), ('天井', pr, CEN['high']))
                                  if val is not None and abs(val - thr) < 1e-12]
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
    # **共有の関数を呼ぶ**（裁定 D119・2026-09-18）——転記行も同じ関数を呼ぶので、二つの値が食い違わない。
    band = runs_B.equivalence_band(n_v, n_r, p0, k, reps=a.reps,
                                   seed=[T['seeds']['tiebreak'] + 1, _tie_mix])
    q95 = band['q95_pt']
    # **帯の境目に一致した候補は印字する**（正本 report_rules.band_edge・裁定 D115・採否表 P332）
    tied = [{'layer': r['layer'], 'coef': r['coef'], 'eff_pt': r['eff_pt'],
             'boundary': abs((best - r['eff_pt']) - q95) < 1e-9} for r in elig if (best - r['eff_pt']) <= q95]

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

# **登録された升目の欠けも incomplete に倒す**（裁定 D126・採否表 P361）。
# 前は調整走行の升目が欠けても判定は open のままで、最良の候補の置き場が欠けても選定が黙って変わった。
if _gap_tune and not a.allow_missing_cells:
    incomplete = True
verdict = ('incomplete' if incomplete else ('closed' if not gate1_open else ('escalate' if (stop or not elig) else 'open')))
if _gap_tune:
    lines.insert(0, '調整走行の登録された升目が %d 件欠けている（場面 × 層 × 係数 × 腕）。'
                    '**欠けた升目は候補を黙って選定から外す**ので、揃えてから判定する（裁定 D126）。' % len(_gap_tune))
if incomplete and n_missing:
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
L += ['', '## 品質床（選定の段・分母は使えた試行・裁定 D104）', '',
      '| 土台 | 腕 | 層 | 係数 | 正答/使えた試行 | 無操作 | api_error | 差 pt | 判定 |', '|---|---|---|---|---|---|---|---|---|']
for r in qrows:
    if r.get('missing'):
        L.append('| %s | %s | %s | %s | — | — | — | — | %s |' % (r['base'], r['arm'], r['layer'], r['coef'], r.get('note') or '記録が無い'))
    else:
        L.append('| %s | %s | %s | %s | %d/%d | %d/%d | %d／%d | %.3f | %s |'
                 % (r['base'], r['arm'], r['layer'], r['coef'], r['correct'], r['n_ok'], r['noop_correct'], r['noop_n_ok'],
                    r['api_error'], r['noop_api_error'], r['diff_pt'],
                    ('合格' if r['pass'] else '不合格') + ('（境目に一致）' if r['boundary'] else '')))
L += ['', '## 印字（正本 print_strings）', ''] + ['- ' + s for s in lines]
if band:
    L += ['', '- 同値の帯（候補横断の最大統計量・帰無の模擬 %s 回・%s 区間の半幅 ±%.4f pt）: 幅 %.2f pt・同値の候補 %d 組。'
          % (format(a.reps, ','), '95%', band['mc_half_pt'], band['q95_pt'], len(tied))]
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[gate_B] %s / %s | 判定 %s | 品質床の合格 %d/%d | 選定 %s' % (out_md, out_json, verdict, n_qpass, len(CANDS), (pick or {}).get('layer')))
sys.exit(0 if verdict == 'open' else 2)
```

## `tools/layers_B.py`（SHA16 7D687E14AB876FC4・176 行）

```python
# -*- coding: utf-8 -*-
"""layers_B.py v1 —— 段階 B の**副位置の読み**（層ごとの分離・層別射影差・記述・裁定 D132・2026-09-19）。

正本 `descriptive_families.B_desc_layer.definition_D132` に従う（**データを見る前に登録した読み方**）:
  反証の場面（`B_desc_layer.scenario`）の無操作の二腕（`B_desc_layer.arms`＝O-Ncold と Osec-Ncold）の試行について、候補の各層で、
  副位置の活性（`activation_storage.response_mean`・走行器が npz に置く）を、**同じ層の (6b) の方向**（`B_desc_layer.direction`＝loaded・
  主位置から作った方向・単位ベクトルにする）に射影する。層ごとに、二腕の射影の**平均の差**・**標準化した差**（二腕を合わせた標準偏差で割る）・
  **AUC**（Osec-Ncold の試行より O-Ncold の試行の射影が大きい確率・同点は半分）を記述として出す。**目安は置かない・p を印字しない。**
  方向は抽出場面の主位置から作り、射影する活性は反証の場面の応答から取るので、同じ標本で方向を作って分離を測る循環は無い。
(6a)（静的）の分離は副位置で測れない（登録された走行に無操作の O と Osec が同じ場面で揃わない・`B_desc_direction.static_separation_D132`）。
入力: 本走行（tag `stageB`）の記録と、各走行の置き場の `resp-<run_key>.npz`（鍵は trial_id・値は［候補の層の数, 隠れ次元］の fp16）・
      方向の npz（`tools/direction_B.py` の `directions.npz`・鍵は `<名>__<層の割合>`）。
出力: records/B/layers-B-<日付>.{md,json}（既存は --force なしでは上書きしない）。報告の組み立て器が必須として読む。
用法: python tools/layers_B.py --directions results/dirB/directions.npz [--root <results>] [--allow-dry] [--force]
      python tools/layers_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO


def auc(a, b):
    """P(a > b) + 0.5 P(a = b)（Mann–Whitney の U を nA・nB で割った値・順位で数える）。"""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if not len(a) or not len(b):
        return None
    allv = np.concatenate([a, b])
    order = allv.argsort(kind='mergesort')
    ranks = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):                       # 同点は平均順位
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    ra = ranks[:len(a)].sum()
    u = ra - len(a) * (len(a) + 1) / 2.0
    return float(u / (len(a) * len(b)))


def separation(pa, pb):
    """平均の差・標準化した差（二腕を合わせた標準偏差）・AUC。記述のみ。"""
    pa, pb = np.asarray(pa, dtype=float), np.asarray(pb, dtype=float)
    na, nb = len(pa), len(pb)
    if na < 2 or nb < 2:
        return {'n_A': na, 'n_B': nb, 'mean_diff': None, 'smd': None, 'auc': None}
    d = float(pa.mean() - pb.mean())
    sp = float(np.sqrt(((na - 1) * pa.var(ddof=1) + (nb - 1) * pb.var(ddof=1)) / (na + nb - 2)))
    return {'n_A': na, 'n_B': nb, 'mean_A': float(pa.mean()), 'mean_B': float(pb.mean()), 'mean_diff': d,
            'smd': (d / sp) if sp > 0 else None, 'auc': auc(pa, pb)}


def load_resp(rec, trial_rows):
    """走行の置き場の resp npz から、試行ごとの副位置の活性を読む（無い試行は数えて返す）。"""
    arrs, missing = {}, 0
    npz = {}
    for r in trial_rows:
        p = r.get('resp_mean_path')
        if not p:
            missing += 1
            continue
        fn, key = p.split('#', 1)
        if fn not in npz:
            fp = os.path.join(rec['dir'], fn)
            npz[fn] = np.load(fp) if os.path.exists(fp) else None
        z = npz[fn]
        if z is None or key not in z.files:
            missing += 1
            continue
        arrs[r['trial_id']] = np.asarray(z[key], dtype=np.float32)
    return arrs, missing


def analyse(T, dirs, root=None, allow_dry=False):
    L = T['descriptive_families']['B_desc_layer']
    sc, (armA, armB), dname = L['scenario'], L['arms'], L['direction']
    ratios = list(T['selection']['candidates']['layers'])
    idx = runs_B.index_runs(T, T['tags']['main'], root, allow_dry=allow_dry)
    proj = {armA: {r: [] for r in ratios}, armB: {r: [] for r in ratios}}
    counts = {armA: {'ok': 0, 'no_resp': 0}, armB: {'ok': 0, 'no_resp': 0}}
    for key, recs in idx.items():
        for rec in recs:
            if (rec['manifest'].get('scenario')) != sc:
                continue
            rows = [r for r in runs_B.iter_jsonl(rec['trials_path'], ('trial_id', 'arm', 'status', 'resp_mean_path'))
                    if r['arm'] in (armA, armB) and r['status'] == 'ok']
            arrs, _ = load_resp(rec, rows)
            for r in rows:
                a = arrs.get(r['trial_id'])
                if a is None:
                    counts[r['arm']]['no_resp'] += 1
                    continue
                if a.shape[0] != len(ratios):
                    raise SystemExit('副位置の活性の層の数（%d）が候補の層の数（%d）と違う: %s' % (a.shape[0], len(ratios), r['trial_id']))
                counts[r['arm']]['ok'] += 1
                for li, ratio in enumerate(ratios):
                    u = dirs[(dname, float(ratio))]
                    u = u / float(np.linalg.norm(u))
                    proj[r['arm']][ratio].append(float(np.dot(a[li], u)))
    rows_out = []
    for ratio in ratios:
        s = separation(proj[armA][ratio], proj[armB][ratio])
        rows_out.append(dict(layer=ratio, **s))
    return {'scenario': sc, 'arm_A': armA, 'arm_B': armB, 'direction': dname, 'rows': rows_out, 'counts': counts}


def _selftest():
    rng = np.random.default_rng(11)
    # AUC: 既知の値（完全分離・完全一致・同点）
    assert auc([3, 4, 5], [0, 1, 2]) == 1.0 and auc([0, 1, 2], [3, 4, 5]) == 0.0
    assert abs(auc([1, 1], [1, 1]) - 0.5) < 1e-12
    # 正規の二群: AUC は Φ(d/√2) の近く（d は標準化した差）
    a, b = rng.normal(1.0, 1.0, 4000), rng.normal(0.0, 1.0, 4000)
    from scipy.stats import norm, mannwhitneyu
    s = separation(a, b)
    assert abs(s['auc'] - norm.cdf(1.0 / np.sqrt(2))) < 0.02, s
    assert abs(s['smd'] - 1.0) < 0.06, s
    # **別の実装**（scipy の Mann–Whitney）と照らす
    u = mannwhitneyu(a[:300], b[:300], alternative='two-sided').statistic
    assert abs(auc(a[:300], b[:300]) - u / (300 * 300)) < 1e-12, 'AUC が scipy の U と違う'
    print('[layers_B selftest] AUC（既知の値・同点・scipy の U と一致）・標準化した差: すべて通った')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--directions', default=None, help='tools/direction_B.py の directions.npz')
    ap.add_argument('--root', default=None)
    ap.add_argument('--contrasts', default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--allow-dry', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    if not a.directions:
        sys.exit('--directions（tools/direction_B.py の directions.npz）が要る')
    T = runs_B.load_T(a.contrasts)
    z = np.load(a.directions)
    dirs = {(k.split('__')[0], float(k.split('__')[1])): z[k] for k in z.files}
    R = analyse(T, dirs, a.root, a.allow_dry)
    now = datetime.datetime.now(datetime.timezone.utc)
    jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
    out_md = a.out or os.path.join(REPO, 'records', 'B', 'layers-B-%s.md' % jst.strftime('%Y-%m-%d'))
    out_json = os.path.splitext(out_md)[0] + '.json'
    if not a.force:
        for p in (out_md, out_json):
            if os.path.exists(p):
                sys.exit('既にある（--force で上書き）: %s' % p)
    REC = dict({'kind': 'layers_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'directions_sha16': runs_B.sha16_file(a.directions),
                'definition': T['descriptive_families']['B_desc_layer']['definition_D132']}, **R)
    json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    L = ['# 段階 B 副位置の読み（層ごとの分離・記述・機械生成・`tools/layers_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
         '- 正本 SHA16 %s・方向の npz SHA16 %s。場面 %s・%s 対 %s・方向 %s（主位置から作った・単位ベクトル）。'
         % (REC['contrasts_sha16'], REC['directions_sha16'], R['scenario'], R['arm_A'], R['arm_B'], R['direction']),
         '- **記述であり、目安も p も置かない**（裁定 D132）。(6a) の分離は副位置で測れない（`B_desc_direction.static_separation_D132`）。',
         '- 副位置の活性を読めた試行: %s（%s）・%s（%s）。読めなかった試行（応答が空など）: %s・%s。'
         % (R['arm_A'], R['counts'][R['arm_A']]['ok'], R['arm_B'], R['counts'][R['arm_B']]['ok'],
            R['counts'][R['arm_A']]['no_resp'], R['counts'][R['arm_B']]['no_resp']), '',
         '| 層（全層に対する深さの割合） | n A／B | 射影の平均 A | 射影の平均 B | 平均の差 | 標準化した差 | AUC |', '|---|---|---|---|---|---|---|']
    f = lambda x: '—' if x is None else ('%.4g' % x)
    for r in R['rows']:
        L.append('| %s | %s／%s | %s | %s | %s | %s | %s |' % (r['layer'], r['n_A'], r['n_B'], f(r.get('mean_A')), f(r.get('mean_B')),
                                                          f(r['mean_diff']), f(r['smd']), f(r['auc'])))
    L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
    print('[layers_B] %s / %s' % (out_md, out_json))
```

## `tools/runs_B.py`（SHA16 F8D809536E055480・388 行）

```python
# -*- coding: utf-8 -*-
"""runs_B.py v4 —— 段階 B の走行の記録を読む共有の口（段階 A の `runs_A.py` の型・**段階 A の器は触らない**）。

段階 B の相（正本 `tags`）と置き場:
  同一性選別 `idB`      : results/idB/idB__<スタック>__<場面>__<印>/      （manifest の stack・scenario）
  調整走行   `tuneB`    : results/tuneB/tuneB__<場面>__L<層>C<係数>__<印>/（manifest の scenario・layer・coef）
  品質床     `stageB-quality`: results/stageB-quality/<tag>__<段>__<腕>__L<層>C<係数>__<印>/（manifest の stage〔selection|post〕・arm・layer・coef）
  本走行     `stageB`   : results/stageB/stageB__<場面>__s<セッション>__<印>/（manifest の scenario・session）

どの走行も manifest.json と trials-*.jsonl（一行一試行）と raw-*.jsonl を持つ。
試行の欄（正本 `trial_record`）のうち、この口が数えるのは次だけ:
  trial_id・arm・status・catastrophe・choice・format_fail・style_a（名言及）・style_b（JSON 直答）・mention（検査認識の言及）・loop_flag・truncated・correct（品質床）。
全分母（n_ok）＝ api_error を除いた試行（書式外と refuse を含む・正本 `denominators.n_ok`）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPATH = os.path.join(REPO, 'design', 'contrasts-B.json')
VERSION = 'v4'
COUNT_FIELDS = ('trial_id', 'arm', 'status', 'catastrophe', 'choice', 'format_fail', 'style_a', 'style_b', 'mention', 'loop_flag', 'truncated', 'correct')


def field_registry(T):
    """試行の記録の鍵・判定欄・整合検査の許可欄（正本 `trial_record_fields`・裁定 D97）。器の中に手書きしない。"""
    f = T.get('trial_record_fields') or {}
    assert f.get('fields') and f.get('blind') and f.get('integrity_allow'), '正本に試行の記録の鍵の登録が無い（裁定 D97）'
    return f
ZERO = dict(n=0, n_ok=0, api_error=0, cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, loop=0, trunc=0, unmeas=0,
            correct=0, scoring_gap=0, style_gap=0, correct_format_fail=0)


def load_T(path=None):
    return json.load(open(path or CPATH, encoding='utf-8'))


def sha16_file(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


def results_root(root=None):
    return root or os.path.join(REPO, 'results')


def read_json(p):
    return json.load(open(p, encoding='utf-8'))


def run_dirs(tag, root=None):
    return sorted(d for d in glob.glob(os.path.join(results_root(root), tag, tag + '__*')) if os.path.isdir(d))


def one_file(d, prefix):
    fs = sorted(glob.glob(os.path.join(d, prefix + '-*.jsonl')))
    if len(fs) != 1:
        raise RuntimeError('%s の %s ファイルが %d 本（一本であるべき）' % (d, prefix, len(fs)))
    return fs[0]


def iter_jsonl(p, fields=None):
    with open(p, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                yield ({k: r.get(k) for k in fields} if fields else r)


def dry_marks(d, m, trials_path):
    """dry-run の印（manifest の dry・置き場 _dryrun・行の dry_run）。空なら印なし。"""
    marks = [x for x, on in (('manifest.dry_run', bool(m.get('dry_run'))), ('manifest.model', m.get('model') in ('stub/dry-run', 'stub')),
                             ('dir._dryrun', '_dryrun' in os.path.normpath(d).split(os.sep) or os.path.basename(d).endswith('__dryrun')),
                             ('dir._synth', '_synth' in os.path.normpath(d).split(os.sep))) if on]
    # **先頭一行だけを見ない**（裁定 D115・採否表 P335〔二体目 G4〕）。合成の行が途中に混ざっても捕まえる。
    any_dry = any(r.get('dry_run') for r in iter_jsonl(trials_path, ('dry_run',)))
    if any_dry:
        marks.append('trials.dry_run')
    return marks


def _rec(d, allow_dry):
    m = read_json(os.path.join(d, 'manifest.json'))
    tp = one_file(d, 'trials')
    dm = dry_marks(d, m, tp)
    if dm and not allow_dry:
        raise RuntimeError('dry-run の走行は読まない: %s（印 %s・検査用の口だけが通す）' % (d, '・'.join(dm)))
    return {'dir': d, 'run_key': os.path.basename(d), 'manifest': m, 'trials_path': tp,
            'raw_path': one_file(d, 'raw') if glob.glob(os.path.join(d, 'raw-*.jsonl')) else None, 'dry_marks': dm}


def index_runs(T, tag, root=None, key=None, allow_multi=True, allow_dry=False):
    """走行を manifest から作った鍵で引ける辞書にする（既定の鍵は相ごとの自然な組）。

    key は manifest を受けて鍵を返す関数。allow_multi なら同じ鍵に複数の走行（セッションを跨いだ中断と再開）を list で持つ。"""
    if key is None:
        tags = {v: k for k, v in T['tags'].items()}

        def key(m):
            phase = tags.get(m.get('tag'))
            if phase == 'identity' or (phase is None and 'stack' in m):
                return (m['stack'], m['scenario'])
            if phase == 'quality' or (phase is None and 'stage' in m):
                # 相手はセッションを跨いで合算しない（裁定 D92・採否表 P261）
                return (m['stage'], m['arm'], m.get('layer'), m.get('coef'), m.get('session'))
            if phase == 'tune' or (phase is None and 'layer' in m and 'arm' in m):
                return (m['scenario'], m['layer'], m['coef'])
            return (m['scenario'],)                # 本走行（選ばれた層 × 係数は manifest の欄にあるが、鍵は場面だけ）
    out = {}
    for d in run_dirs(tag, root):
        rec = _rec(d, allow_dry)
        k = key(rec['manifest'])
        if allow_multi:
            out.setdefault(k, []).append(rec)
        elif k in out:
            raise RuntimeError('同じ鍵の走行が複数: %s（%s と %s）' % (k, out[k]['dir'], d))
        else:
            out[k] = rec
    return out


def cell_counts(trials_path, acc=None, phase='main'):
    """腕ごとの件数（acc に足し込める——中断と再開でセルが複数のセッションにまたがるため）。

    phase は採点欠落の判定に効く（裁定 D103）——本走行は選択の欄、品質床は正答の欄で見る。"""
    out = acc if acc is not None else {}
    for r in iter_jsonl(trials_path, COUNT_FIELDS):
        c = out.setdefault(r['arm'], dict(ZERO))
        c['n'] += 1
        if r['status'] != 'ok':
            c['api_error'] += 1
            continue
        ff, lp, tr = bool(r['format_fail']), bool(r['loop_flag']), bool(r['truncated'])
        c['n_ok'] += 1
        # **「まだ採点していない」と「採点した結果として当てはまらない」を分ける**（裁定 D103・採否表 P306・P319）。
        # 凍結パーサ `is_catastrophic` は refuse に破局の判定を返さない規約なので、破局の欄の空で数えると
        # refuse が全件この札に落ち、確証の族が丸ごと判定不能になる（直しの確認の巡で実際に零になった）。
        # 書式外の試行は判定を持たないのが正しいので、ここには数えない。
        gap = False
        if not ff:
            if (r.get('correct') is None) if phase == 'quality' else (r.get('choice') is None):
                gap = True                         # 判定欄が空（採点前・採点漏れ）——裁定 D96・D103
            # **逆向きの穴も塞ぐ**（裁定 D126・採否表 P363）: 選択が読めているのに破局の判定が空の試行は、
            # 黙って「破局でない」に数えられていた。凍結パーサは登録外の族に None を返すので、
            # 走行器が族を取り違えると率が下がる（起草者に有利な向き）。
            elif phase != 'quality' and r.get('choice') not in (None, 'refuse') and r['catastrophe'] is None:
                gap = True
        # **様式・言及の欄が空の場面の試行も採点欠落に数える**（正本 `response_mode.gap_rule`・2026-09-19）。
        # 前は走行器がこれらを空で書き、ここは空を「該当なし」と数えていたので、様式門が実データでは黙って効かなかった
        # （合成データは欄を埋めていたので検査は通っていた）。書式外の試行も様式は測る（段階 A の (b) は本文の先頭で決める）。
        if phase != 'quality' and any(r.get(k) is None for k in ('style_a', 'style_b', 'mention')):
            c['style_gap'] += 1
            gap = True
        c['scoring_gap'] += gap                    # 一つの試行は一度だけ数える
        c['cat'] += (r['catastrophe'] is True)
        c['refuse'] += (r['choice'] == 'refuse')
        c['ff'] += ff
        c['style_a'] += bool(r['style_a'])
        c['style_b'] += bool(r['style_b'])
        c['mention'] += bool(r['mention'])
        c['loop'] += lp
        c['trunc'] += tr
        c['unmeas'] += (ff or lp or tr)
        c['correct_format_fail'] += (ff and r['correct'] is True)   # 規約違反の検出用（整合検査が止める）
        c['correct'] += (r['correct'] is True and not ff)   # 書式外は不正解に数える（quality_floor.format_fail_rule・採否表 P269）
    return out


def counts_main(T, tag=None, root=None, allow_dry=False):
    """本走行: {(場面, 腕): 件数} と走行の索引。中断と再開でまたがったセルは足し合わせる（正本 sessions.resume_rule）。"""
    tag = tag or T['tags']['main']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc,), recs in idx.items():
        acc = {}
        for rec in recs:
            cell_counts(rec['trials_path'], acc, phase='main')
        for arm, c in acc.items():
            C[(sc, arm)] = c
    return C, idx


def counts_tune(T, tag=None, root=None, allow_dry=False):
    """調整走行: {(場面, 層, 係数, 腕): 件数} と索引。"""
    tag = tag or T['tags']['tune']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc, layer, coef), recs in idx.items():
        acc = {}
        for rec in recs:
            cell_counts(rec['trials_path'], acc, phase='tune')
        for arm, c in acc.items():
            C[(sc, layer, coef, arm)] = c
    return C, idx


def counts_quality(T, tag=None, root=None, allow_dry=False):
    """品質床: {(段, 腕, 層, 係数): 件数} と索引（無操作の相手は層・係数を None で持つ）。"""
    tag = tag or T['tags']['quality']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for k, recs in idx.items():
        acc = {}
        for rec in recs:
            cell_counts(rec['trials_path'], acc, phase='quality')
        for arm, c in acc.items():
            C[(k[0], arm, k[2], k[3], k[4] if len(k) > 4 else None)] = c
    return C, idx


def equivalence_band(n_v, n_r, p0, k, reps=20000, seed=0, q=0.95):
    """**同値の帯**（候補横断の最大統計量・正本 `selection.equivalence_band`・裁定 D98）。

    帰無（全候補が同じ率）で「候補横断の最大と最小の差」を模擬し、その q 分位を帯とする。
    **門と転記行の両方がこの一つの関数を呼ぶ**（裁定 D119・2026-09-18）——
    前は転記行が別の式（差の分散を一候補の二倍で出す素の区間）で ±13.8 pt を印字し、
    しかも **正本の鍵の名を出典に付けていた**。正本の当該の条はその式を「採らない」と明記しており、
    門の模擬は 21.5 pt を出していた（系統外の検分で捕まった・採否表 P339）。
    """
    import math as _m
    import numpy as _np
    rng = _np.random.default_rng(seed)
    sim_v = rng.binomial(max(int(n_v), 1), p0, size=(int(reps), int(k))) / max(int(n_v), 1)
    sim_r = rng.binomial(max(int(n_r), 1), p0, size=(int(reps), int(k))) / max(int(n_r), 1)
    eff = 100.0 * (sim_r - sim_v)
    spread = eff.max(axis=1) - eff.min(axis=1)
    q95 = float(_np.quantile(spread, q))
    half = 1.96 * float(_np.std(spread)) / _m.sqrt(int(reps))
    return {'q95_pt': round(q95, 3), 'reps': int(reps), 'mc_half_pt': round(half, 4), 'null_rate': round(float(p0), 5),
            'k': int(k), 'n_v': int(n_v), 'n_r': int(n_r),
            'rule': '帰無（全候補が同じ）で、候補横断の最大と最小の差が %g 分位に収まる幅。'
                    '最大の候補との差がこの幅の内側の候補を同値として一覧に出す（決め方には使わない）' % q}


def cell_index(T, phase, key):
    """セルの番号（正本 `seeds.cell_index_rule`・裁定 D107）。相ごとに決まった鍵の組の**登録順の添字**（零始まり）。

    同一性選別と本走行は（場面, 腕）、調整走行は（場面, 腕, 層, 係数）、品質床は（段, 腕, 層, 係数）。
    """
    SCEN = list(T['scenarios'])
    LAY, COE = list(T['selection']['candidates']['layers']), list(T['selection']['candidates']['coefficients'])
    ARMS = list(T['arms']['panel'])
    for src in (T['arms']['main'], T['identity_screen'].get('arms_run') or [], T['identity_screen'].get('compared_arms') or []):
        for x in src:
            if x not in ARMS:
                ARMS.append(x)
    STAGES = ['selection', 'post']
    ESC = int(T['seeds']['cell_index_escape'])     # 逃げ道の幅（正本に登録・採否表 P378・前は器の中に手書きしていた）
    def _ai(arm):
        if arm in ARMS:
            return ARMS.index(arm)
        import hashlib as _h
        return len(ARMS) + int(_h.sha256(str(arm).encode('utf-8')).hexdigest()[:8], 16) % ESC   # 登録に無い腕も決定的に一意な番号を持つ
    if phase == 'identity':
        sc, arm = key
        return (SCEN.index(sc) if sc in SCEN else len(SCEN)) * (len(ARMS) + ESC) + _ai(arm)
    if phase == 'main':
        sc, arm = key
        return SCEN.index(sc) * (len(ARMS) + ESC) + _ai(arm)
    if phase == 'tune':
        sc, arm, l, c = key
        return ((SCEN.index(sc) * (len(ARMS) + ESC) + _ai(arm)) * len(LAY) + LAY.index(l)) * len(COE) + COE.index(c)
    if phase == 'quality':
        stage, arm, l, c = key
        li = LAY.index(l) if l in LAY else len(LAY)      # 無操作の相手は層・係数を持たない
        ci = COE.index(c) if c in COE else len(COE)
        return ((STAGES.index(stage) * (len(ARMS) + ESC) + _ai(arm)) * (len(LAY) + 1) + li) * (len(COE) + 1) + ci
    raise SystemExit('相の名が正本に無い: %s' % phase)


def cell_seed(T, run_seed, phase, key):
    """セルの種（正本 `seeds.derivation_formula`・裁定 D107・D99）。"""
    import numpy as _np
    idx = cell_index(T, phase, key)
    return int(_np.random.SeedSequence([int(run_seed), int(T['seeds']['phase_index'][phase]), int(idx)]).generate_state(1)[0])


def trial_seed(cell_s, trial_index):
    """試行の種（正本 `seeds.derivation_formula`）。**記録には書かない**——下の `recorded_seed` を見よ。"""
    import numpy as _np
    return int(_np.random.SeedSequence([int(cell_s), int(trial_index)]).generate_state(1)[0])


def batch_seed(cell_s, batch_index):
    """バッチの種（正本 `seeds.unit_D127`・裁定 D127）。**試行単位の再現は主張しない。**"""
    import numpy as _np
    return int(_np.random.SeedSequence([int(cell_s), int(batch_index)]).generate_state(1)[0])


def retry_seed(cell_s, batch_index, attempt=1):
    """**書式外の引き直しの種**＝`SeedSequence([セルの種, バッチ番号, 引き直しの回])`（正本 `seeds.derivation_formula`・2026-09-19）。
    前は走行器の中で「バッチの種 ＋ 一」と手書きしていた（登録の外の種）。引き直しは一回だけ（凍結走行器の規約）。"""
    import numpy as _np
    return int(_np.random.SeedSequence([int(cell_s), int(batch_index), int(attempt)]).generate_state(1)[0])


def recorded_seed(T, cell_s, trial_index, start=0):
    """**試行の記録に書く種**＝その試行が属する**バッチの種**（裁定 D127・2026-09-19）。

    書く側（走行器・合成データ）と検べる側（整合検査）は**この一つの関数を呼ぶ**。
    前は走行器がバッチの種を書き、整合検査と合成データは試行の種を使っていたので、
    **合成データは整合検査を通り、本物の出力は全件落ちる**形になっていた
    （起草者が裁定 D127 の直しで入れた食い違い・本体を書いて記録を集計に通す段で見つけた）。
    **バッチの区切りはセルの頭（試行の番号 零）から数えた倍数に固定する**——中断して途中から再開しても、
    同じ試行は同じバッチの番号に属し、同じ種を持つ（走行器は区切りをこれに合わせる）。
    """
    return batch_seed(cell_s, int(trial_index) // int(T['runner']['batch']))


def counts_main_by_direction(T, tag=None, root=None, allow_dry=False):
    """本走行の**方向ごと**の件数（正本 `random_control.pooling`・裁定 D110・採否表 P315）。

    合併する前に三本のランダム方向の率を出すために要る。{(場面, 腕, 方向の id): 件数}。"""
    tag = tag or T['tags']['main']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc,), recs in sorted(idx.items()):
        for rec in recs:
            for r in iter_jsonl(rec['trials_path'], COUNT_FIELDS + ('direction_id',)):
                did = r.get('direction_id')
                if did is None:
                    continue
                c = C.setdefault((sc, r['arm'], did), dict(ZERO))
                c['n'] += 1
                if r['status'] != 'ok':
                    c['api_error'] += 1
                    continue
                c['n_ok'] += 1
                c['cat'] += (r['catastrophe'] is True)
                c['ff'] += bool(r['format_fail'])
                c['refuse'] += (r['choice'] == 'refuse')
    return C


def stratum_of(r):
    """様式の層（正本 style_gate.stratified.strata）。JSON 直答なら json_direct・そうでなければ prose。

    **書式外の試行は層に入れない**（答えが読めないので様式も読めない・裁定 D115・採否表 P335〔二体目 G6〕）。
    前は合成データの書式外の行が様式の欄を持っていたため、読めない試行が json_direct の層に入っていた。"""
    if r.get('format_fail'):
        return None
    return 'json_direct' if bool(r.get('style_b')) else 'prose'


def counts_main_strata(T, tag=None, root=None, allow_dry=False):
    """本走行: {(場面, 腕, 層): 件数}（様式門の層別の副次・札は変えない）。"""
    tag = tag or T['tags']['main']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc,), recs in idx.items():
        for rec in recs:
            for r in iter_jsonl(rec['trials_path'], COUNT_FIELDS):
                st_ = stratum_of(r)
                if st_ is None:
                    continue
                k = (sc, r['arm'], st_)
                c = C.setdefault(k, dict(ZERO))
                c['n'] += 1
                if r['status'] != 'ok':
                    c['api_error'] += 1
                    continue
                c['n_ok'] += 1
                c['cat'] += (r['catastrophe'] is True)
                c['refuse'] += (r['choice'] == 'refuse')
                c['ff'] += bool(r['format_fail'])
    return C


def load_sessions(root=None):
    """セッション記録（正本 sessions.record）。"""
    out = []
    for p in sorted(glob.glob(os.path.join(results_root(root), 'sessions-B', '*.json'))):
        out.append(read_json(p))
    return out


def sessions_by_run_key(sessions):
    out = {}
    for s in sessions:
        for rk in s.get('run_keys') or []:
            out.setdefault(rk, []).append(s)
    return out


def rate(k, n):
    return (k / n) if n else None


def pt(x):
    return None if x is None else 100.0 * x
```

## `tools/steer_B.py`（SHA16 BD5690BB56FF54FF・278 行）

```python
# -*- coding: utf-8 -*-
"""steer_B.py v5 —— 段階 B の**介入**（方向の加減・ランダム方向・品質床の生成と採点）。

正本 `design/contrasts-B.json` の `selection.apply`・`random_control`・`quality_floor`・`runner` に従う。
規則（この器が守るもの）:
  - 加減は `h ← h ± α·v̂`（**主位置〔組み立て済みの列の最後のトークン〕から EOS まで**・`register_forward_hook`・`selection.apply`・裁定 D124）。α は**その層の v̂ のノルムに対する比**。
  - すべての方向（v̂・Nk・td・(6b)・ランダム方向）を**係数を掛ける前の ‖v̂〔static〕‖** に合わせ、**係数は加減のときに一度だけ**掛ける（裁定 D75・D90）。
    自己検査は「**全方向 × 全係数 × 全層**で加わる量のノルムが一致する」ことを確かめる（裁定 D102——前は v 腕とランダム腕の対しか回さず、交差族に同じ穴が残った）。
  - 介入の帯の起点は、**chat template を当てた組み立て済みの列の最後のトークン（主位置）**（裁定 D101 で template を当て、裁定 D124 で起点を主位置にした）。
    自己検査は起点を**独立の正解**（器を通さずに作った列の最後の位置）と照らし、復号して最終トークンと一致することを見る
    （`OP4B_TOKENIZER_DIR` に実トークナイザの置き場を渡したときに走る。**`OP4B_REQUIRE_FULL_SELFTEST=1` なら、飛ばすと失敗に倒す**・裁定 D122）。
    関数の名 `scenario_start_index` は裁定 D124 の前の名残で、返すのは主位置である。
  - ランダム方向は**調整走行と本走行で引き直す**（裁定 D84・種は `seeds.random_dirs` の tune と main）。
  - 一腕の試行は方向の登録順に等分し、端数は登録順に一つずつ配る（`random_control.allocation`・調整走行にも当てる）。
  - 品質床は**貪欲**（`quality_floor.generation`）で、**生成した文字列から記号を読み取る**（強制デコードは採らない・裁定 D120）。書式外は不正解に数え、api_error は一度だけ引き直す（`quality_floor.format_fail_rule`）。
  - 場面の試行は `runner.generation` の設定。詰めは左（`runner.padding`）。
**この器は GPU の上でしか本走行できない。** 手元では `--selftest`（ノルム合わせ・割り当て・引き直し・種の再現を合成のベクトルで確かめる）が走る。
用法: python tools/steer_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v5'
STRICT = os.environ.get('OP4B_REQUIRE_FULL_SELFTEST') == '1'     # 実機の段では飛ばしを失敗に倒す（裁定 D122・採否表 P344）
REPO = runs_B.REPO
T = runs_B.load_T()
RC = T['random_control']
N_RAND = RC['count']


def random_directions(v_hat_static, phase, layer_ratio, count=N_RAND):
    """層ごとに count 本のランダム方向を引き、**係数を掛ける前の ‖v̂〔static〕‖** に合わせる（裁定 D90・2026-09-18）。

    係数は加減のときに一度だけ掛ける（`apply_vector`・`selection.apply`）。基準は**静的 v̂ ひとつ**で、族を跨いで変えない（裁定 D75）。
    phase は 'tune' か 'main'（裁定 D84・種を分けて引き直す）。子ストリームは**層ごと**（正本 `random_control.per_layer`・係数は入れない・採否表 P285）。"""
    assert phase in ('tune', 'main'), '相は tune か main（裁定 D84）'
    seed = RC['seed'][phase]
    d = int(np.asarray(v_hat_static).shape[-1])
    ss = np.random.SeedSequence([seed, int(round(layer_ratio * 1000))])
    rng = np.random.default_rng(ss)
    target = float(np.linalg.norm(v_hat_static))
    out = []
    for i in range(count):
        g = rng.normal(size=d)
        n = float(np.linalg.norm(g))
        out.append(g * (target / n) if n else g)
    return out


def match_to_static(v, v_hat_static):
    """どの方向（Nk・td・(6b)）も、加える前に ‖v̂〔static〕‖ に合わせる（裁定 D75・D90）。"""
    n = float(np.linalg.norm(v))
    return v * (float(np.linalg.norm(v_hat_static)) / n) if n else v


def allocate(n_trials, count=N_RAND):
    """一腕の試行を方向の登録順に等分し、端数は登録順に一つずつ配る（random_control.allocation）。"""
    base, rem = divmod(int(n_trials), int(count))
    return [base + (1 if i < rem else 0) for i in range(count)]


def direction_of(trial_index, n_trials, count=N_RAND):
    """試行の番号から方向の添字を決める（**再開しても変わらない**・採否表 P298）。

    残り件数から割り直すと等分にならないので、常に全体の割り当てを基準にする。"""
    al = allocate(n_trials, count)
    acc = 0
    for i, n in enumerate(al):
        acc += n
        if trial_index < acc:
            return i
    raise ValueError('試行の番号が全体の数を超えている: %s / %s' % (trial_index, n_trials))


def apply_vector(h, v_hat, coef, sign):
    """h ← h ± α·v̂（α は v̂ のノルムに対する比なので、掛けるのは coef·v̂）。"""
    assert sign in (+1, -1)
    return h + sign * coef * np.asarray(v_hat)


def apply_chat(tokenizer, user_message):
    """**段階 B は chat template を当てる**（正本 `runner.chat_template`・裁定 D101）。組み立て済みのトークン列を返す。"""
    return list(tokenizer.apply_chat_template([{'role': 'user', 'content': user_message}],
                                              add_generation_prompt=True, tokenize=True))


def scenario_start_index(tokenizer, arm_text, scen_text, instruction, pad_len=0):
    """介入の帯の**起点**＝**主位置（プロンプトの最終トークン）**（正本 `selection.apply`・裁定 D124・2026-09-18）。

    裁定 D124 で帯を「場面本文の開始から」ではなく「主位置から EOS まで」に狭めた。
    抽出した場所と加える場所を一致させるためであり、**狭めて落ちるのは prefill の場面本文の位置だけ**
    （選択が作られる復号の段はすべて掛かる）。
    左詰めのバッチでは、詰めの長さに関わらず**最終トークンは列の最後の位置**にある。
    pad_len は左詰めの詰めの長さ（この式では結果に効かないが、呼び手の意図を明示するために受ける）。
    """
    ids = apply_chat(tokenizer, _user_message(arm_text, scen_text, instruction))
    return pad_len + len(ids) - 1


def _user_message(arm_text, scen_text, instruction):
    """凍結走行器 `user_message` と同じ式（正本 `runner.prompt_assembly`）。"""
    t = arm_text or ''
    return (t + '\n\n' + scen_text + instruction) if t else (scen_text + instruction)


def band_starts(tokenizer, arm_texts, scen_text, instruction, pad_lens):
    """バッチの行ごとの起点（`make_hook` に渡す）。

    正本 `selection.batch_composition` により**一つのバッチは一つの場面 × 一つの腕**なので、
    詰めは起きず、全行が同じ起点になる。式は一般のまま置き、器が取り決めを守っているかを
    `assert_batch_uniform` で確かめる。
    """
    return [scenario_start_index(tokenizer, t, scen_text, instruction, p) for t, p in zip(arm_texts, pad_lens)]


def assert_batch_uniform(arm_texts, scenarios=None):
    """**一つのバッチは一つの場面 × 一つの腕**（正本 `selection.batch_composition`・裁定 D124）。"""
    if len(set(arm_texts)) > 1:
        raise SystemExit('バッチに複数の腕が混ざっている（正本 selection.batch_composition・裁定 D124）: %d 種'
                         % len(set(arm_texts)))
    if scenarios is not None and len(set(scenarios)) > 1:
        raise SystemExit('バッチに複数の場面が混ざっている（正本 selection.batch_composition・裁定 D124）: %d 種'
                         % len(set(scenarios)))


def _to_hf(g, greedy):
    """正本の生成の設定を transformers の引数名に写す（説明の欄は落とす・採否表 P286）。"""
    out = {'max_new_tokens': g.get('max_tokens')}
    if greedy:
        out['do_sample'] = False
    else:
        out.update({'do_sample': True, 'temperature': g.get('temperature'), 'top_p': g.get('top_p')})
    return {k: v for k, v in out.items() if v is not None}


def quality_generation():
    """品質床の生成の設定（**貪欲**・正本 quality_floor.generation・裁定 D78）。"""
    g = T['quality_floor']['generation']
    assert g['temperature'] == 0, '品質床は貪欲（temperature 零）でなければならない（裁定 D78）'
    if g.get('max_tokens') is None:      # **黙って落とさない**（裁定 D103・採否表 P328）
        raise SystemExit('品質床の最大トークン数が未定（裁定 D66 と採否表 P216 で決める）。'
                         'このまま実機に渡すと transformers の既定で走り、例外も警告も出ない')
    return _to_hf(g, greedy=True)


def main_generation():
    """場面の試行の生成の設定（正本 runner.generation）。"""
    return _to_hf(T['runner']['generation'], greedy=False)


def score_quality(answer_letter, correct_letter, format_fail):
    """品質床の採点（書式外は不正解に数えて分母を保つ・quality_floor.format_fail_rule）。"""
    if format_fail or not answer_letter:
        return False
    return answer_letter.strip().upper() == correct_letter.strip().upper()


def _selftest():
    rng = np.random.default_rng(3)
    v = rng.normal(size=32)
    nv = float(np.linalg.norm(v))
    # (1) ランダム方向は ‖v̂‖ に合う（係数は掛けない・裁定 D90）
    for ratio in T['selection']['candidates']['layers']:
        rs = random_directions(v, 'main', ratio)
        assert len(rs) == N_RAND
        for r in rs:
            assert abs(float(np.linalg.norm(r)) - nv) < 1e-9, 'ランダム方向のノルムが ‖v̂‖ に合っていない（裁定 D90）'
    # (2) **合成の検査**（裁定 D102・採否表 P309・P311）: 加わる量のノルムが
    #     **全方向（v̂・Nk・td・(6b)・ランダム方向） × 全係数 × 全層**で一致する。
    #     前は v 腕とランダム腕の対しか回さなかったため、交差族と S4 の反証に同じ穴が残った。
    raw = {'Nk': rng.normal(size=32) * 7.0, 'td': rng.normal(size=32) * 0.2, 'loaded': rng.normal(size=32) * 3.5}
    others = {k: match_to_static(w, v) for k, w in raw.items()}      # 方向を作る器が合わせたものを模す
    n_checked = 0
    for coef in T['selection']['candidates']['coefficients']:
        for ratio in T['selection']['candidates']['layers']:
            a_v = np.linalg.norm(apply_vector(np.zeros(32), v, coef, +1))
            cand = dict(others)
            for i, r in enumerate(random_directions(v, 'main', ratio)):
                cand['rand:%d' % i] = r
            for name, w in cand.items():
                a_w = np.linalg.norm(apply_vector(np.zeros(32), w, coef, +1))
                assert abs(a_v - a_w) < 1e-9, ('加わる量が v 腕と %s で違う（係数が二度掛かっていないか）' % name, coef, ratio, a_v, a_w)
                n_checked += 1
    assert n_checked == len(T['selection']['candidates']['coefficients']) * len(T['selection']['candidates']['layers']) * (len(raw) + N_RAND)
    # (3) 合わせる器そのもの
    assert abs(float(np.linalg.norm(match_to_static(rng.normal(size=32) * 7.0, v))) - nv) < 1e-9
    # (4) 引き直し（裁定 D84）と層ごとの子ストリーム（係数は入れない・採否表 P285）
    a1 = random_directions(v, 'tune', 0.5)[0]
    a2 = random_directions(v, 'main', 0.5)[0]
    assert not np.allclose(a1, a2), '調整走行と本走行で引き直していない'
    assert np.allclose(a1, random_directions(v, 'tune', 0.5)[0]), '同じ引数で再現しない'
    assert not np.allclose(random_directions(v, 'main', 0.25)[0], random_directions(v, 'main', 0.75)[0]), '層で子ストリームが分かれていない'
    # (5) 割り当てと、試行の番号から方向へ（再開しても変わらない・採否表 P298）
    for n in (200, 201, 100, 7):
        al = allocate(n)
        assert sum(al) == n and max(al) - min(al) <= 1 and al == sorted(al, reverse=True), '割り当ての端数の配り方が規則と違う'
    n = T['n_main']
    got = [direction_of(i, n) for i in range(n)]
    assert [got.count(i) for i in range(N_RAND)] == allocate(n), '試行から方向への写像が割り当てと合わない'
    assert [direction_of(i, n) for i in range(n // 2, n)] == got[n // 2:], '再開すると方向の割り当てが変わる'
    # (6) 加減の向き
    h = rng.normal(size=32)
    assert np.allclose(apply_vector(h, v, 2.0, +1) - h, 2.0 * v)
    assert np.allclose(apply_vector(h, v, 0.5, -1) - h, -0.5 * v)
    # (7) 品質床の採点と生成（transformers の引数名で出す・採否表 P286）
    assert score_quality('A', 'a', False) and not score_quality('A', 'B', False) and not score_quality('A', 'A', True)
    try:
        qg = quality_generation()
    except SystemExit as e:
        qg = None
        assert '最大トークン数' in str(e), '品質床の生成の設定が、別の理由で止まっている: %s' % e
    mg = main_generation()
    if qg is not None:
        assert qg['do_sample'] is False and 'temperature' not in qg, '品質床が貪欲でない'
        assert 'max_new_tokens' in qg, '品質床の最大トークン数が黙って落ちている（裁定 D103）'
    assert set(mg) <= {'do_sample', 'temperature', 'top_p', 'max_new_tokens'}, '生成の設定に transformers が知らない鍵が混ざる'
    assert mg['max_new_tokens'] == T['runner']['generation']['max_tokens'] and mg['temperature'] == T['runner']['generation']['temperature']
        # (8) **帯の起点**（裁定 D101・採否表 P308）: 実トークナイザがあれば、起点のトークンを復号して場面本文の先頭に一致することを確かめる
    band = _selftest_band()
    print('[steer_B selftest] 全方向 × 全係数 × 全層の合成 %d 通り・引き直し・層の子ストリーム・割り当てと再開・加減の向き・生成の設定・%s: すべて通った'
          % (n_checked, band))


def _selftest_band(model_dir=None):
    """帯の起点の自己検査（正本 `runner.chat_template`・`selection.apply`・裁定 D122）。

    **独立の正解と照らす**（裁定 D122）——起点を求めるのに使った経路とは別に、
    組み立て済みの列を自分で作って最後の位置を取り、二つが一致することを確かめる。
    さらに、その位置のトークンを**復号して**、組み立て済みの列の最終トークンと文字列で一致することを見る。
    左詰めのバッチでも、詰めを入れた列の中で同じ位置が最終トークンを指すことを確かめる。
    前の版は、起点を探すのに使ったトークンでそのまま照合していたので**恒真**だった。
    """
    try:
        from transformers import AutoTokenizer
    except Exception:
        if STRICT:
            raise SystemExit('帯の起点の検査を飛ばした（transformers が無い）——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
        return '帯の起点（**飛ばした**——transformers が無い）'
    src = model_dir or os.environ.get('OP4B_TOKENIZER_DIR')
    if not src:
        if STRICT:
            raise SystemExit('帯の起点の検査を飛ばした（OP4B_TOKENIZER_DIR が無い）——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
        return '帯の起点（**飛ばした**——OP4B_TOKENIZER_DIR が無い）'
    tok = AutoTokenizer.from_pretrained(src)
    scen, inst = '場面の本文がここから始まる。', '\n\n指示。'
    n_ok = 0
    for arm_text in ('前置きがここにある。', ''):
        ids = apply_chat(tok, _user_message(arm_text, scen, inst))
        want = len(ids) - 1                                   # **独立の正解**（器を通さずに作る）
        got = scenario_start_index(tok, arm_text, scen, inst, 0)
        assert got == want, ('起点が独立の正解と違う', arm_text[:8], got, want)
        assert tok.decode([ids[got]]) == tok.decode([ids[-1]]), '起点のトークンが最終トークンでない'
        for pad in (0, 5, 37):                                # 左詰めの詰めを入れても最終トークンを指すか
            padded = [tok.pad_token_id or 0] * pad + ids
            st = scenario_start_index(tok, arm_text, scen, inst, pad)
            assert padded[st] == ids[-1], ('詰めを入れると起点がずれる', pad, st)
        n_ok += 1
    assert_batch_uniform(['a', 'a', 'a'])
    try:
        assert_batch_uniform(['a', 'b'])
        raise AssertionError('腕が混ざったバッチを止めていない（裁定 D124）')
    except SystemExit:
        pass
    return '帯の起点（実トークナイザ・独立の正解と照合・詰め三通り・腕の混在を止めることも確かめた）'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    sys.exit('この器は GPU の上の走行器から import して使う（手元の検査は --selftest）。'
             '走行の組み立て（場面の本文・hook の登録・バッチ）は走行器 `tools/run_stageB_local.py` の側にある。')
```
