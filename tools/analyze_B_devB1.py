# -*- coding: utf-8 -*-
# **逸脱 D-B1 の下の集計器**（登録者裁定 D151・2026-09-22）。凍結した `tools/analyze_B.py` から `tools/make_analyze_B_devB1.py` が機械で作った——手で直さない。
# 違いは、選定後の段の走行が無い確証族の土台の腕の品質床を、門の記録の・選定の段の・選ばれた層 × 係数の行で読むことと、その印だけである。
# 凍結した器の出力（`records/B/analysis-B-2026-09-22.*`）は変えずに残し、報告は二つの出力を並べる。
"""analyze_B.py v6 —— 段階 B の本走行の集計と札（確証の族・門・記述の族・印字）。
v7（2026-09-20・凍結前の二度目の掃き出し・登録者の裁定）: **門の記録の正本 SHA16 を現在の正本と照らして止める**（段階 A の集計器と同じ型・逸脱 D-40）。登録の定型 `no_data`・`dilution_hold`・`label_confirmed` を注に配線した（前は正本にあって器が印字していなかった）。
v6（2026-09-19・最後の系統外の巡の後・**独立の目を通っていない**）: td の特異性を族ごとの規則で決める（`rules_B.td_specificity_family`・裁定 D133）／S4 の三分岐の前に門を当て（`rules_B.s4_gates`・D134）、札は結果だけにし、封印との照合を別に出す（`rules_B.s4_seal_match`・D135）・相対の大きさと観測した相手の率での動作特性を記録に入れる（D136）／様式門に当たった非有意は非有意のまま（`rules_B.style_hold_label`・採否表 P401）／検査用の口 `--no-gate` を廃し、門の記録の SHA を記録に入れる・選定後の品質床の相手の重複の番人（採否表 P403）。

正本 `design/contrasts-B.json` に従う。**札は一つだけ**付け、ほかに当たった門は注に出す（`gate_order`）。
門の順は**正本 `gate_order.order` を読む**（`rules_B.gate_order`・前は手書きの並びを持っていた・裁定 D130）。
**判定の規則は `tools/rules_B.py` の関数を呼ぶ**（v5・2026-09-19）——S4 の三分岐（同等性・裁定 D118）・区間（Newcombe・裁定 D130）・
refuse 門（答えた分母と読めた分母・符号の積・裁定 D127・D130）・ランダム方向の等質性の注（裁定 D127）・td の特異性（裁定 D123）・
選定後の品質床の api_error の門（裁定 D127）。**v4 までは、これらが正本と草案の文にしか無く、この器の中は古い規則のままだった**
（直しの監査 `records/reviews/B/external-round/verification-fixes-B-external-before.md`）。
検定: 両側 Fisher・全分母（分子＝破局・分母＝n_ok）・Holm は族ごと（m は族ごと・**降格しても m は減らさない**・`censor.m_rule`）。
封印した予想符号（`families[*].sealed_sign`・`seal_format`）があれば、確証の札の向きと照らし、一致の数を印字する（裁定 D79）。
記述の族は p を印字しない（`print_strings.no_p_desc`）。S4 の反証は三分岐（`B_desc_S4.three_way`・裁定 D81・判定の規則は裁定 D118）。
入力: 本走行（tag `stageB`）・門と選定の記録（`gate_B.py` の json）・品質床の**選定後**の走行・封印の記録（任意）。
出力: records/B/analysis-<日付>.{md,json}（既存は --force なしでは上書きしない）。
用法: python tools/analyze_B.py --gate records/B/gate-B-<日付>.json [--seal records/B/seal-B.json] [--root <results>] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import fisher_exact, binom
import runs_B
import rules_B

VERSION = 'v7+devB1'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--gate', required=True, help='tools/gate_B.py の json（選定の記録・必須——検査用の口 --no-gate は廃した・採否表 P403）')
ap.add_argument('--seal', default=None, help='封印の記録（予想符号）')
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
ap.add_argument('--allow-partial-seal', action='store_true', help='検査用の口（封印が全対比を持たなくても進む）')
ap.add_argument('--allow-not-open', action='store_true', help='検査用の口（門1 が open でなくても集計する・裁定 D109）')
ap.add_argument('--allow-unbound', action='store_true', help='検査用の口（門の選んだ層 × 係数と違っても集計する・裁定 D105）')
ap.add_argument('--allow-no-sessions', action='store_true', help='検査用の口（セッション記録が無くても集計する・裁定 D108）')
ap.add_argument('--chart', default=None, help='tools/control_chart_B.py の json（管理図・裁定 D110）')
ap.add_argument('--allow-canon-mismatch', action='store_true', help='検査用の口（門の記録の正本 SHA16 が現在の正本と違っても集計する・印を残す）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
CEN, DG, RG, SG, QF, GO = T['censor'], T['dilution_gate'], T['refuse_gate'], T['style_gate'], T['quality_floor'], T['gate_order']
PS, SC = T['print_strings'], T['scenarios']
rate, pt = runs_B.rate, runs_B.pt
# **門の記録は必須**（採否表 P403・2026-09-19）。前は検査用の口 `--no-gate` が門の判定（裁定 D109）と束縛（裁定 D105）を一度に外せた
G = runs_B.read_json(a.gate)
GATE_SHA16 = runs_B.sha16_file(a.gate)          # 報告の組み立て器が、渡された門の記録と照らす（採否表 P403）
if G.get('kind') != 'gate_B':
    sys.exit('門の記録の種類が違う: %s' % a.gate)
# **門の記録の正本 SHA16 を現在の正本と照らす**（凍結前の見直しの (六の二)・2026-09-20・v7）。
# 段階 A の集計器にはこの検査があり、実際に発火した（逸脱台帳 D-40）。B には無く、凍結の後に正本が動いても集計器は黙って進んだ。
_canon_now = runs_B.sha16_file(a.contrasts or runs_B.CPATH)
CANON_MISMATCH = bool(G.get('contrasts_sha16')) and G['contrasts_sha16'] != _canon_now
if CANON_MISMATCH and not a.allow_canon_mismatch:
    sys.exit('門の記録の正本 SHA16 %s が現在の正本 %s と違う（凍結の後に正本が動いたか、記録の取り違え——逸脱台帳 D-40 の型）。検査用は --allow-canon-mismatch'
             % (G['contrasts_sha16'], _canon_now))
SEAL = runs_B.read_json(a.seal) if a.seal else None
SIGN_MAP = T['seal_format']['sign_map']          # 正本の語彙 → 集計器の記号（裁定 D121）
SIGN_VALUES = set(T['seal_format']['sign_values'])
SEAL_MISSING = []
if SEAL is not None:
    _conf_ids = [c['id'] for F in T['families'].values() for c in F['contrasts']]
    # **列挙として検べる**（裁定 D121）——正本に無い語で封印されていたら止まる
    _bad = sorted({v for v in (SEAL.get('signs') or {}).values() if v not in SIGN_VALUES})
    if _bad:
        sys.exit('封印の予想符号が正本の一覧に無い（正本 seal_format.sign_values・裁定 D121）: %s（使える語: %s）'
                 % ('・'.join(map(str, _bad)), '・'.join(sorted(SIGN_VALUES))))
    if SEAL.get('s4') is not None and SEAL['s4'] not in SIGN_VALUES and not a.allow_partial_seal:
        sys.exit('S4 の反証の封印が正本の一覧に無い（裁定 D121）: %s' % SEAL['s4'])
    SEAL_MISSING = [i for i in _conf_ids if i not in (SEAL.get('signs') or {})]
    if SEAL_MISSING and not a.allow_partial_seal:
        sys.exit('封印の記録が確証の全対比を持っていない（裁定 D79・seal_format.scope）: 欠け %d 件。検査用は --allow-partial-seal' % len(SEAL_MISSING))

# ---- 門の判定（裁定 D109・採否表 P318）: open でなければ既定で止まる ----
if G.get('verdict') != 'open' and not a.allow_not_open:
    sys.exit('門1 の判定が open でない（%s）。集計しない（正本 gate_order.gate_stop・裁定 D109）。検査用は --allow-not-open'
             % G.get('verdict'))

C, idx = runs_B.counts_main(T, root=a.root, allow_dry=a.allow_dry)
POOL_IDS = {r.get('direction_id') for recs in idx.values() for rec in recs
            for r in runs_B.iter_jsonl(rec['trials_path'], ('direction_id',))}
STR = runs_B.counts_main_strata(T, root=a.root, allow_dry=a.allow_dry)
CQ, idx_q = runs_B.counts_quality(T, root=a.root, allow_dry=a.allow_dry)
DRY = sorted({m for recs in list(idx.values()) + list(idx_q.values()) for r in recs for m in r['dry_marks']})

# ---- 選定した層 × 係数との束縛（裁定 D105・採否表 P304） ----
PICK = G.get('selection', {}).get('pick') or {}
BIND = []
if PICK.get('layer') is not None:
    for recs in list(idx.values()) + list(idx_q.values()):
        for rec in recs:
            m = rec['manifest']
            if m.get('stage') == 'selection':
                continue        # **選定の段は全候補で走るのが正しい**（束縛の対象は本走行と選定後の品質床だけ）
            if m.get('layer') is None:
                continue        # 無操作の相手と、層を持たない走行は対象外
            if (m.get('layer'), m.get('coef')) != (PICK['layer'], PICK['coef']):
                BIND.append('%s: 層 %s・係数 %s（門が選んだのは 層 %s・係数 %s）'
                            % (rec['run_key'], m.get('layer'), m.get('coef'), PICK['layer'], PICK['coef']))
    if BIND and not a.allow_unbound:
        sys.exit('本走行・選定後の品質床が、門の選んだ層 × 係数と違う（正本 selection.binding・裁定 D105）:\n  '
                 + '\n  '.join(BIND[:8]) + ('\n  ほか %d 件' % (len(BIND) - 8) if len(BIND) > 8 else ''))

# ---- セッション記録（裁定 D108・正本 sessions.missing_rule・採否表 P317） ----
SESS_MISSING = []
_sess = runs_B.sessions_by_run_key(runs_B.load_sessions(a.root))
for recs in list(idx.values()) + list(idx_q.values()):
    for rec in recs:
        if rec['run_key'] not in _sess:
            SESS_MISSING.append(rec['run_key'])
if SESS_MISSING and not a.allow_no_sessions:
    sys.exit('走行キーのセッション記録が無い（正本 sessions.missing_rule・裁定 D108）: %s%s'
             % ('・'.join(sorted(SESS_MISSING)[:6]), ' ほか' if len(SESS_MISSING) > 6 else ''))

# ---- ランダム方向の三本の率（正本 random_control.pooling・裁定 D110・採否表 P315） ----
BYDIR = runs_B.counts_main_by_direction(T, root=a.root, allow_dry=a.allow_dry)

# ---- 三本のランダム方向の等質性（正本 random_control.homogeneity_rule・裁定 D127・`rules_B.homogeneity`） ----
HOMOG = {}
for (sc_, arm_, did_), c_ in BYDIR.items():
    if 'vrand' in arm_ and str(did_).startswith('rand:'):
        HOMOG.setdefault((sc_, arm_), []).append((c_['cat'], c_['n_ok']))
HOMOG = {k: rules_B.homogeneity(v, T) for k, v in HOMOG.items()}


def homog_note(row):
    h = HOMOG.get((row['scenario'], row['B'])) or HOMOG.get((row['scenario'], row['A']))
    if h and h.get('note'):
        row.setdefault('notes', []).append('注（ランダム方向の不均一・三本の率の差 %.1f pt・門 %g pt 超）: 帰無は「ランダム方向一般」ではなく「引いた三本」である'
                                           % (h['spread_pt'], h['threshold_pt']))
    if h and h.get('edge'):
        row.setdefault('notes', []).append('境目に一致（等質性・%g pt）' % h['threshold_pt'])
    row['homogeneity'] = h


# ---- 管理図（正本 calibration.consequence・裁定 D110・採否表 P316・P323） ----
CHART = runs_B.read_json(a.chart) if a.chart else None
CHART_BAD = (CHART or {}).get('anomalies') or []
CHART_RUNS = {x.get('run_key') for x in CHART_BAD}
CHART_SC = {x.get('scenario') for x in CHART_BAD}
CHART_NOTE = T['calibration']['consequence']

# ---- 選定後の品質床（裁定 D77）: 落ちた腕 ----
INTERV = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
QF_FAIL, QF_ROWS, QF_MISSING = set(), [], []
_post = {k: v for k, v in CQ.items() if k[0] == 'post'}
# ==== 逸脱 D-B1（登録者裁定 D151・2026-09-22）: 確証族の土台の腕の選定後の床を、門の記録の選定の段の行で読む ====
DEVB1_SOURCE = '門の記録の・選定の段の・選ばれた層 × 係数の行（逸脱 D-B1・登録者裁定 D151）'
DEVB1_NOTE = '逸脱 D-B1 の下（土台の腕の選定後の品質床を門の記録の選定の段の行で読んだ・凍結した集計器の札は「判定不能（品質床）」）'
_OPS_DEVB1 = {'O-Ncold': '-v', 'Onull': '+v'}           # 起動器と同じ対応（正本 quality_floor.operations）
DEVB1_BASE_ARMS = {b + _OPS_DEVB1[b] for b in T['quality_floor']['arms']}
DEVB1_ARMS, DEVB1_GATE_ROWS = set(), {}
for _r in (G.get('quality_floor_rows') or []):
    if (_r.get('arm') in DEVB1_BASE_ARMS and PICK.get('layer') is not None and not _r.get('missing')
            and float(_r.get('layer')) == float(PICK['layer']) and float(_r.get('coef')) == float(PICK['coef'])):
        DEVB1_GATE_ROWS[_r['arm']] = {k: _r.get(k) for k in ('arm', 'layer', 'coef', 'correct', 'noop_correct', 'n_ok', 'noop_n_ok',
                                                          'api_error', 'noop_api_error', 'diff_pt', 'pass', 'boundary')}
for arm in INTERV:                                  # **介入の腕の一覧から数え上げる**（記録が無ければ合格にしない・採否表 P262）
    cells = {k: v for k, v in _post.items() if k[1] == arm}
    if not cells and arm in DEVB1_GATE_ROWS:             # 逸脱 D-B1: 走行が無い土台の腕は、門の記録の選定の段の行で読む
        _g = DEVB1_GATE_ROWS[arm]
        QF_ROWS.append(dict(_g, source=DEVB1_SOURCE))
        DEVB1_ARMS.add(arm)
        if not _g.get('pass'):
            QF_FAIL.add(arm)
        continue
    if not cells:
        QF_MISSING.append(arm)
        QF_ROWS.append({'arm': arm, 'missing': True, 'note': '選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）'})
        QF_FAIL.add(arm)
        continue
    if len(cells) > 1:                                # **門と同じ番人**（裁定 D106・採否表 P307）
        QF_MISSING.append(arm)
        QF_ROWS.append({'arm': arm, 'missing': True,
                        'note': '選定後の品質床の走行が %d 本ある（古い走行を黙って採らない・裁定 D106）' % len(cells)})
        QF_FAIL.add(arm)
        continue
    k0 = sorted(cells)[0]
    cell, l, c, session = cells[k0], k0[2], k0[3], k0[4] if len(k0) > 4 else None
    base = arm.split('+v')[0].split('-v')[0]
    noop = CQ.get(('post', base, None, None, session))   # 相手は**同じ段・同じセッション**（裁定 D88・D92）
    if noop is None:
        QF_MISSING.append(arm)
        QF_ROWS.append({'arm': arm, 'missing': True, 'note': '同じセッションの無操作の相手が無い（裁定 D92）'})
        QF_FAIL.add(arm)
        continue
    # **相手の重複の番人**（正本 sessions.partner_duplicate_rule・採否表 P403・2026-09-19）。同じ番号の走行が二本あると
    # 読み口が合算し、分母が倍になる。門の器には選定の段の番人があったが、選定後の段の相手はこの器が合算したまま読んでいた
    _n_runs = len(idx_q.get(('post', base, None, None, session)) or [])
    if _n_runs > 1 or noop.get('n', 0) > QF['items']:
        QF_MISSING.append(arm)
        QF_ROWS.append({'arm': arm, 'missing': True, 'partner_runs': _n_runs, 'partner_n': noop.get('n', 0),
                        'note': '選定後の無操作の相手の重複（走行 %d 本・試行 %d 件・登録 %d 件）——合算しない（正本 sessions.partner_duplicate_rule）'
                                % (_n_runs, noop.get('n', 0), QF['items'])})
        QF_FAIL.add(arm)
        continue
    if rules_B.api_error_gate(cell, noop, T):          # **api_error の率の差が門を超えたら判定しない**（裁定 D127・合格に数えない）
        QF_MISSING.append(arm)
        QF_ROWS.append({'arm': arm, 'missing': True, 'api_error': cell.get('api_error', 0), 'noop_api_error': noop.get('api_error', 0),
                        'note': '判定しない（api_error の率の差が %g pt を超える・正本 quality_floor.api_error_gate）' % QF['api_error_gate_pt']})
        QF_FAIL.add(arm)
        continue
    gap = cell.get('scoring_gap', 0) + noop.get('scoring_gap', 0)
    if gap or not cell['n_ok'] or not noop['n_ok']:   # 採点欠落・使えた試行が零（裁定 D103・D110）
        QF_MISSING.append(arm)
        QF_ROWS.append({'arm': arm, 'missing': True, 'scoring_gap': gap,
                        'note': ('判定欄が空の試行が %d 件ある（裁定 D103）' % gap) if gap else '使えた試行が零（測れなかった）'})
        QF_FAIL.add(arm)
        continue
    else:
        # **分母は使えた試行**（裁定 D104・採否表 P305）
        d_pt = 100.0 * (cell['correct'] / cell['n_ok'] - noop['correct'] / noop['n_ok'])
        ok = d_pt > QF['threshold_pt']
        QF_ROWS.append({'arm': arm, 'layer': l, 'coef': c, 'correct': cell['correct'], 'noop_correct': noop['correct'],
                        'n_ok': cell['n_ok'], 'noop_n_ok': noop['n_ok'],
                        'api_error': cell.get('api_error', 0), 'noop_api_error': noop.get('api_error', 0),
                        'diff_pt': round(d_pt, 3), 'pass': ok, 'boundary': abs(d_pt - QF['threshold_pt']) < 1e-9})
        if not ok:
            QF_FAIL.add(arm)


def cell(sc, arm):
    return C.get((sc, arm))


def ci_pt(k1, n1, k2, n2):
    """pt 差（A − B）と 95% の **Newcombe** 区間（`rules_B.diff_ci_pt`・正本 `interval`）。v4 までは Wald だった（裁定 D130・採否表 P379）。"""
    r = rules_B.diff_ci_pt(k1, n1, k2, n2, T['interval']['conf'])
    return None if r is None else (round(r[0], 3), round(r[1], 3), round(r[2], 3))


def interval_disagrees(p, ci):
    """名目の検定（Fisher・両側）と区間（Newcombe）が食い違うか（正本 `interval.note`）。"""
    if p is None or ci is None:
        return False
    return (p < 0.05) != (ci[1] > 0 or ci[2] < 0)


def fisher(k1, n1, k2, n2):
    return float(fisher_exact([[k1, n1 - k1], [k2, n2 - k2]])[1])


def stat(c, key='cat'):
    return (c[key], c['n_ok']) if c else (None, None)


# ---- 確証の族 ----
def analyse_contrast(fam, c, alpha_step):
    A, B = cell(c['scenario'], c['A']), cell(c['scenario'], c['B'])
    row = {'id': c['id'], 'family': fam, 'scenario': c['scenario'], 'A': c['A'], 'B': c['B'], 'gates': [], 'notes': []}
    if A is None or B is None:
        row.update({'label': '表に載らない（記録が無い）', 'missing': True})
        return row
    ka, na, kb, nb = A['cat'], A['n_ok'], B['cat'], B['n_ok']
    p = fisher(ka, na, kb, nb) if (na and nb) else None
    ci = ci_pt(ka, na, kb, nb)
    ra, rb = rate(ka, na), rate(kb, nb)
    row.update({'k_A': ka, 'n_ok_A': na, 'k_B': kb, 'n_ok_B': nb, 'rate_A': ra, 'rate_B': rb,
                'p': p, 'diff_pt': None if ci is None else ci[0], 'ci': None if ci is None else [ci[1], ci[2]],
                'sign': None if ci is None else ('上' if ci[0] > 0 else ('下' if ci[0] < 0 else '零')),
                'ff_pt_A': pt(rate(A['ff'], na)), 'ff_pt_B': pt(rate(B['ff'], nb)),
                'refuse_pt_A': pt(rate(A['refuse'], na)), 'refuse_pt_B': pt(rate(B['refuse'], nb)),
                'style_a_pt_A': pt(rate(A['style_a'], na)), 'style_a_pt_B': pt(rate(B['style_a'], nb)),
                'style_b_pt_A': pt(rate(A['style_b'], na)), 'style_b_pt_B': pt(rate(B['style_b'], nb))})
    # --- 門を順に見る（札は最初の一つ・ほかは注） ---
    if (A.get('scoring_gap') or 0) or (B.get('scoring_gap') or 0):
        row['gates'].append('判定不能（採点欠落）')     # 裁定 D96
        row['notes'].append('判定欄が空の試行 %d 件（A）・%d 件（B）' % (A.get('scoring_gap') or 0, B.get('scoring_gap') or 0)
                            + ('（うち様式・言及の欄が空 %d 件・%d 件）' % (A.get('style_gap') or 0, B.get('style_gap') or 0)
                               if (A.get('style_gap') or B.get('style_gap')) else ''))
    if not na or not nb:
        row['gates'].append('判定不能（測れなかった）')  # n_ok が零（裁定 D96・採否表 P300）
        row['notes'].append(PS['no_data'].format(cell=row['id']))          # 登録の定型（凍結前の見直しの (九)）
    both_low = ra is not None and rb is not None and ra < CEN['low'] and rb < CEN['low']
    both_high = ra is not None and rb is not None and ra > CEN['high'] and rb > CEN['high']
    if both_low or both_high:
        row['gates'].append('判定不能（検閲）')
    ffd = None if None in (row['ff_pt_A'], row['ff_pt_B']) else abs(row['ff_pt_A'] - row['ff_pt_B'])
    rfd = None if None in (row['refuse_pt_A'], row['refuse_pt_B']) else abs(row['refuse_pt_A'] - row['refuse_pt_B'])
    row['ff_diff_pt'] = None if ffd is None else round(ffd, 3)
    row['refuse_diff_pt'] = None if rfd is None else round(rfd, 3)
    if ffd is not None and ffd > DG['threshold_pt']:
        row['gates'].append('判定保留（書式外転位）')
        row['notes'].append(PS['dilution_hold'].format(A=row['A'], B=row['B'], metric='書式外率', diff=round(ffd, 3), thr=DG['threshold_pt'], label='書式外転位'))
    if rfd is not None and rfd > DG['threshold_pt']:
        row['gates'].append('判定保留（refuse 転位・差）')
        row['notes'].append(PS['dilution_hold'].format(A=row['A'], B=row['B'], metric='refuse 率', diff=round(rfd, 3), thr=DG['threshold_pt'], label='refuse 転位・差'))
    nominal = p is not None and p < 0.05
    if nominal:
        # **答えた分母と読めた分母の両方で当て、向きは符号の積で見る**（`rules_B.refuse_gate`・裁定 D127・D130・採否表 P367・P368）
        rg = rules_B.refuse_gate(A, B, T)
        row['refuse_gate'] = rg
        if rg['hold']:
            row['gates'].append('判定保留（refuse 転位）')
            row['notes'].append('refuse 門: ' + '・'.join(rg['reasons']))
    if interval_disagrees(p, ci):
        row['notes'].append('名目の検定（Fisher）と区間（Newcombe）が食い違う（床の近く・正本 interval.note）')
    sa = None if None in (row['style_a_pt_A'], row['style_a_pt_B']) else abs(row['style_a_pt_A'] - row['style_a_pt_B'])
    sb = None if None in (row['style_b_pt_A'], row['style_b_pt_B']) else abs(row['style_b_pt_A'] - row['style_b_pt_B'])
    row['style_diff_pt'] = None if None in (sa, sb) else round(max(sa, sb), 3)
    if row['style_diff_pt'] is not None and row['style_diff_pt'] > SG['hold_pt']:
        row['gates'].append('判定保留（様式転位）')     # 当たった事実は札に関わらず記録する（裁定 D94）
    if c['A'] in QF_FAIL or c['B'] in QF_FAIL:
        row['gates'].append('判定不能（品質床）')
    # --- 札（正本 gate_order.order の順で最初の一つ・様式門は確証の札にのみ作用する非対称を保つ） ---
    order = rules_B.gate_order(T)                  # **正本の並びを読む**（裁定 D130・採否表 P377）
    unknown = [g for g in row['gates'] if g not in order]
    if unknown:
        sys.exit('門の札が正本の並び（gate_order.labels）に無い: %s' % unknown)
    fired = [g for g in order if g in row['gates']]
    row['fired'] = fired
    hard = [g for g in fired if g != '判定保留（様式転位）']        # 様式門以外は札になる
    row['label'] = hard[0] if hard else ('確証' if (p is not None and p < alpha_step) else '非有意')
    row['style_hold'] = '判定保留（様式転位）' in fired
    return row


def apply_style_gate(row):
    """様式門は確証の札にのみ作用する（style_gate.asymmetry）。Holm の判定が出た後に当てる。"""
    d = row.get('style_diff_pt')
    if d is None:
        return
    # **帯の境目に一致した値は印字する**（正本 report_rules.band_edge・裁定 D115・採否表 P332）
    for name, thr in (('様式門の保留', SG['hold_pt']), ('様式門の注', SG['note_pt'])):
        if abs(d - thr) < 1e-9:
            row['notes'].append('境目に一致（%s・%g pt）' % (name, thr))
    if d > SG['hold_pt']:
        row['label'] = '判定保留（様式転位）'
        row['fired'] = row.get('fired', []) + ['判定保留（様式転位）']
    elif d > SG['note_pt']:
        row['notes'].append('注（様式・差 %.1f pt）' % d)


RES, FAMROWS = {}, []
for famkey, F in T['families'].items():
    rows = [analyse_contrast(famkey, c, 0.05) for c in F['contrasts']]
    # Holm（族ごと・m は減らさない）。**降格・保留になった対比は順位に含めない**（裁定 D93）。
    # **様式門の保留も外す**（裁定 D125・2026-09-18）——前は「様式門は確証の札にのみ作用する」（裁定 D94）を
    # 理由に順位に残していたが、残すと次の対比の閾値が α/m から α/(m−1) に**緩む**（確証が出やすい側）。
    # 標準の Holm としては FWER が保たれるので、これは FWER のための規則ではなく**保守の選択**である。
    _hard = lambda r: [g for g in (r.get('fired') or []) if g != '判定保留（様式転位）']
    ordered = sorted([r for r in rows if r.get('p') is not None and not (r.get('fired') or [])], key=lambda r: r['p'])
    m = F['m']
    passed = True
    for i, r in enumerate(ordered):
        step = 0.05 / (m - i)
        r['holm_alpha'] = step
        r['holm_pass'] = passed and (r['p'] < step)
        passed = r['holm_pass']
    for r in rows:
        if r.get('style_hold') and not _hard(r):
            # 順位から外したので Holm の判定を持たない（裁定 D125）。**名目の p が 0.05 以上なら非有意のまま**、
            # 0.05 未満だけを様式転位の保留にする（`rules_B.style_hold_label`・正本 style_gate.label_rule_P401・採否表 P401）。
            # 前は p に関わらず保留にし、非有意が保留に化けていた（起草者に有利な向き）。当たった事実は fired に残る（裁定 D94）
            r['label'] = rules_B.style_hold_label(r.get('p'))
            if r['label'] == '非有意':
                r['notes'].append('様式門に当たったが名目の p が 0.05 以上なので非有意（様式門は確証の札にのみ作用する・style_gate.asymmetry）')
        else:
            if r.get('label') == '確証' and not r.get('holm_pass'):
                r['label'] = '非有意'
            if r.get('label') == '確証':
                apply_style_gate(r)
        if len(r.get('fired') or []) > 1:
            r['notes'].append('当たった門: ' + '・'.join(r['fired']))
        homog_note(r)
        # **異常のあった走行を含む対比だけに注を付ける**（裁定 D130・採否表 P380）。
        # 前は場面が一致するだけで全対比に付いていた。
        _bad_arms = {x.get('arm') for x in CHART_BAD if x.get('scenario') == r['scenario']}
        if _bad_arms & {r['A'].split('+v')[0].split('-v')[0], r['B'].split('+v')[0].split('-v')[0]}:
            r['notes'].append('管理図: この場面の無操作の腕が帯を外れた走行がある（%s）' % CHART_NOTE[:24])
        if r.get('label') == '確証' and SEAL:
            # **封印の符号は正本の語彙で書かれる**（裁定 D121・2026-09-18）。集計器が内部で使う記号へは
            # 正本の対応表（`seal_format.sign_map`）で写す。前は語彙が二通りあり、正本どおりに封印すると
            # **確証がすべて「登録された向きと逆」になった**（実際に通して確かめた・採否表 P341）。
            want = SIGN_MAP.get((SEAL.get('signs') or {}).get(r['id']))
            r['sealed_sign'] = want
            if want and want != r['sign']:
                r['label'] = '確証（登録された向きと逆）'
                r['notes'].append(PS['label_reverse'].format(A=r['A'], B=r['B'], sign=r['sign'], diff=r['diff_pt'], ci=r['ci']))
        if r.get('label') == '確証':
            r['notes'].append(PS['label_confirmed'].format(A=r['A'], B=r['B'], sign=r['sign'], diff=r['diff_pt'], ci=r['ci']))   # 登録の定型（(九)）
    RES[famkey] = rows
    FAMROWS += rows

# ---- 逸脱 D-B1 の印: 床を門の記録で読んだ腕を含む対比に欄と注を足し、確証の札に印を足す（札の頭は「確証」のまま） ----
for r in FAMROWS:
    if r.get('A') in DEVB1_ARMS or r.get('B') in DEVB1_ARMS:
        r['deviation'] = 'D-B1'
        r.setdefault('notes', []).append(DEVB1_NOTE)
        _lab = str(r.get('label') or '')
        if _lab.startswith('確証'):
            r['label'] = (_lab[:-1] + '・逸脱 D-B1 の下）') if _lab.endswith('）') else (_lab + '（逸脱 D-B1 の下）')
counts = {k: 0 for k in ('確証', '判定不能（検閲）', '判定不能（品質床）', '判定不能（採点欠落）', '判定不能（測れなかった）',
                         '判定保留（書式外転位）', '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '非有意')}
for r in FAMROWS:
    lab = r.get('label', '')
    key = '確証' if lab.startswith('確証') else lab
    if key in counts:
        counts[key] += 1
checked = [r for r in FAMROWS if r.get('label', '').startswith('確証') and r.get('sealed_sign')]
agree = sum(1 for r in checked if r['sealed_sign'] == r['sign'])
n_conf = len(checked)
unchecked = [r['id'] for r in FAMROWS if r.get('label', '').startswith('確証') and not r.get('sealed_sign')]

# ---- 記述の族（p を印字しない） ----
DESC = {}
for famkey, F in T['descriptive_families'].items():
    rows = []
    for c in F.get('contrasts', []):
        A, B = cell(c['scenario'], c['A']), cell(c['scenario'], c['B'])
        if A is None or B is None:
            rows.append({'id': c['id'], 'missing': True})
            continue
        ci = ci_pt(A['cat'], A['n_ok'], B['cat'], B['n_ok'])
        rows.append({'id': c['id'], 'scenario': c['scenario'], 'A': c['A'], 'B': c['B'],
                     'rate_A': rate(A['cat'], A['n_ok']), 'rate_B': rate(B['cat'], B['n_ok']),
                     'diff_pt': None if ci is None else ci[0], 'ci': None if ci is None else [ci[1], ci[2]],
                     'ff_pt_A': pt(rate(A['ff'], A['n_ok'])), 'ff_pt_B': pt(rate(B['ff'], B['n_ok'])),
                     'refuse_pt_A': pt(rate(A['refuse'], A['n_ok'])), 'refuse_pt_B': pt(rate(B['refuse'], B['n_ok'])),
                     'k_A': A['cat'], 'n_A': A['n_ok'], 'k_B': B['cat'], 'n_B': B['n_ok']})
        homog_note(rows[-1])
    DESC[famkey] = rows

# ---- td の特異性（正本 B_desc_textdiff.specificity_rule・**裁定 D133**・`rules_B.td_specificity_family`） ----
# 族（減算・加算）ごとに、場面ごとの（v の腕 対 td の腕）を一度に判定する。その場面の確証の対比（v 対 ランダム）の札と差を添える。
# v5 までは裁定 D123 の数の基準（水準 1 − alpha_upper の区間だけ・向きも確証の成否も見ない）で、td のほうが動いた組でも「書ける」と出た。
_CONF = {r['id']: r for r in FAMROWS}
_TD_FAM = {'B_sub': ('sub', '-vtd'), 'B_add': ('add', '+vtd')}
TD_SPEC = []
for _fk, (_pre, _td_sfx) in _TD_FAM.items():
    _items = []
    for r in DESC.get('B_desc_textdiff', []):
        if r.get('missing') or not r['B'].endswith(_td_sfx) or r['A'].endswith('vtd') or r['A'].endswith('vrand'):
            continue
        _cid = '%s:%s:%s~%s' % (_pre, r['scenario'], r['A'], r['B'].replace('vtd', 'vrand'))    # その場面の確証の対比（v 対 ランダム）
        _c = _CONF.get(_cid) or {}
        _items.append(dict(id=r['id'], family=_fk, scenario=r['scenario'], v_arm=r['A'], td_arm=r['B'],
                           k_v=r['k_A'], n_v=r['n_A'], k_td=r['k_B'], n_td=r['n_B'],
                           conf_id=_cid, conf_label=_c.get('label'), conf_diff_pt=_c.get('diff_pt')))
    if _items:
        TD_SPEC += rules_B.td_specificity_family(_items, T)


# ---- S4 の反証（**門 → 三分岐**・裁定 D81・D118・D134・札は結果だけ〔D135〕・封印との照合は別〔D135〕・効き目の読み〔D136〕） ----
S4 = T['descriptive_families']['B_desc_S4']
s4c = S4['contrasts'][0]
s4A, s4B = cell(s4c['scenario'], s4c['A']), cell(s4c['scenario'], s4c['B'])
S4_SEAL = (SEAL or {}).get('s4')
s4 = {'id': s4c['id'], 'gates': [], 'outcome': None, 'seal_value': S4_SEAL,
      'sealed_prediction': S4_SEAL or S4['sealed_prediction']}
if s4A and s4B:
    # **門を先に当てる**（`rules_B.s4_gates`・裁定 D134）。前は S4 に門が一つも無く、書式外が片腕だけ増えると反証の結果が分母で逆になった
    s4['gates'] = rules_B.s4_gates(s4A, s4B, T, qf_fail=(s4c['A'] in QF_FAIL or s4c['B'] in QF_FAIL))
    s4.update({'k_A': s4A['cat'], 'n_A': s4A['n_ok'], 'k_B': s4B['cat'], 'n_B': s4B['n_ok'],
               'ff_pt_A': pt(rate(s4A['ff'], s4A['n_ok'])), 'ff_pt_B': pt(rate(s4B['ff'], s4B['n_ok'])),
               'refuse_pt_A': pt(rate(s4A['refuse'], s4A['n_ok'])), 'refuse_pt_B': pt(rate(s4B['refuse'], s4B['n_ok']))})
    if s4A['n_ok'] and s4B['n_ok']:
        # **三分岐は rules_B.s4_verdict**（同等性の規則・Newcombe・検出力を使わない・裁定 D118）
        v4_ = rules_B.s4_verdict(s4A['cat'], s4A['n_ok'], s4B['cat'], s4B['n_ok'], T)
        s4.update({'diff_pt': round(v4_['diff_pt'], 3), 'ci': [round(x, 3) for x in v4_['ci']], 'rate_A': v4_['rate_A'], 'partner_rate': v4_['partner_rate'],
                   'upper_one_sided_pt': round(v4_['upper_one_sided_pt'], 3), 'effect_pt': v4_['effect_pt'], 'interval': v4_['interval']})
        # **相対の大きさと、観測した相手の率での動作特性**（裁定 D136）——判定には使わない。n は二腕の使えた試行の少ない方
        _rb, _n4 = v4_['partner_rate'], int(min(s4A['n_ok'], s4B['n_ok']))
        _reg = S4['base_4B2507'] / S4['base_n'] if S4.get('base_n') else None
        s4['relative_size'] = {'to_observed_partner': (None if not _rb else round(v4_['effect_pt'] / (100.0 * _rb), 3)),
                               'to_registered_base': (None if not _reg else round(v4_['effect_pt'] / (100.0 * _reg), 3))}
        s4['oc_at_observed_partner'] = {'partner_rate': round(_rb, 4), 'n_per_arm': _n4,
                                        'at_zero': {k: round(v, 4) for k, v in rules_B.s4_oc(_rb, _n4, 0, T).items()},
                                        'at_effect': {k: round(v, 4) for k, v in rules_B.s4_oc(_rb, _n4, v4_['effect_pt'], T).items()}}
        if not s4['gates']:
            s4['outcome'] = v4_['verdict']
    s4['verdict'] = s4['gates'][0] if s4['gates'] else (s4['outcome'] or '判定不能（測れなかった）')
    if len(s4['gates']) > 1:
        s4.setdefault('notes', []).append('当たった門: ' + '・'.join(s4['gates']))
    _h4 = HOMOG.get((s4c['scenario'], s4c['B']))
    if _h4 and _h4.get('note'):
        s4.setdefault('notes', []).append('注（ランダム方向の不均一・三本の率の差 %.1f pt）' % _h4['spread_pt'])
else:
    s4['verdict'] = '表に載らない（記録が無い）'
# **封印との照合は札と別に**（`rules_B.s4_seal_match`・正本 seal_match.table・裁定 D135）
s4['seal_match'] = rules_B.s4_seal_match(s4['verdict'], S4_SEAL, T)

# ---- 様式門の層別の副次（札を変えない） ----
STRAT = []
for r in FAMROWS:
    if r.get('label') not in ('判定保留（様式転位）',) and '注（様式' not in '・'.join(r.get('notes', [])):
        continue
    for s in SG['stratified']['strata']:
        A, B = STR.get((r['scenario'], r['A'], s)), STR.get((r['scenario'], r['B'], s))
        if not (A and B) or min(A['n_ok'], B['n_ok']) < RG['answered_min_n_ok']:
            STRAT.append({'id': r['id'], 'stratum': s, 'skipped': '層の分母が %s 未満' % RG['answered_min_n_ok']})
            continue
        STRAT.append({'id': r['id'], 'stratum': s, 'p': fisher(A['cat'], A['n_ok'], B['cat'], B['n_ok']),
                      'diff_pt': ci_pt(A['cat'], A['n_ok'], B['cat'], B['n_ok'])[0], 'n_A': A['n_ok'], 'n_B': B['n_ok']})

# ---- 対比に現れない腕（report_rules.orphan_arms） ----
used = {(c['scenario'], c[k]) for F in list(T['families'].values()) + list(T['descriptive_families'].values())
        for c in F.get('contrasts', []) for k in ('A', 'B')}
orphans = sorted({(sc, arm) for (sc, arm) in C if (sc, arm) not in used})
missing = sorted({(c['scenario'], c[k]) for F in list(T['families'].values()) + list(T['descriptive_families'].values())
                  for c in F.get('contrasts', []) for k in ('A', 'B') if (c['scenario'], c[k]) not in C})

# 検査認識の言及率（記述・裁定 D65）
MENTION = [{'scenario': sc, 'arm': arm, 'mention_pt': pt(rate(c['mention'], c['n_ok'])), 'n_ok': c['n_ok']}
           for (sc, arm), c in sorted(C.items())]
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'analysis-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

first = PS['first_finding'].format(confirmed=counts['確証'], undecidable=counts['判定不能（検閲）'], qfloor=counts['判定不能（品質床）'],
                                   gap=counts['判定不能（採点欠落）'], nodata=counts['判定不能（測れなかった）'],
                                   ff=counts['判定保留（書式外転位）'], refuse=counts['判定保留（refuse 転位）'] + counts['判定保留（refuse 転位・差）'],
                                   style=counts['判定保留（様式転位）'], ns=counts['非有意'])
REC = {'kind': 'analyze_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
       'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'gate': G.get('verdict'), 'gate_sha16': GATE_SHA16, 'canon_mismatch_allowed': CANON_MISMATCH,
       'selection': G.get('selection', {}).get('pick'), 'counts': counts, 'confirm': FAMROWS, 'descriptive': DESC,
       's4': s4, 'td_specificity': TD_SPEC, 'homogeneity': [dict(scenario=k_[0], arm=k_[1], **v_) for k_, v_ in sorted(HOMOG.items())],
       'interval': T['interval']['method'], 'stratified': STRAT, 'mention': MENTION, 'by_direction': [dict(scenario=k_[0], arm=k_[1], direction_id=k_[2], **c_) for k_, c_ in sorted(BYDIR.items(), key=str)], 'chart_anomalies': CHART_BAD, 'binding': BIND,
       'sessions_checked': len(_sess), 'direction_ids': sorted(str(x) for x in POOL_IDS if x is not None), 'quality_post': QF_ROWS, 'deviation_D_B1': {'ruling': 'D151', 'arms': sorted(DEVB1_ARMS), 'source': DEVB1_SOURCE, 'gate_rows': DEVB1_GATE_ROWS}, 'orphan_arms': orphans, 'missing_cells': missing,
       'sign_agreement': {'agree': agree, 'checked': n_conf, 'unchecked': unchecked, 'seal_missing': SEAL_MISSING, 'sealed': bool(SEAL)}, 'dry_marks': DRY}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

L = ['# 段階 B 本走行の集計——**逸脱 D-B1 の下**（機械生成・`tools/analyze_B_devB1.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- **これは逸脱 D-B1 の下の出力である**（登録者裁定 D151・2026-09-22）。凍結した集計器の出力は `records/B/analysis-B-2026-09-22.md` にある。違いは、床を ' + DEVB1_SOURCE + ' で読んだ腕（' + '・'.join(sorted(DEVB1_ARMS)) + '）を含む対比の札と、その族の Holm だけである。直すという決定は率と p を見た後になされた。',
     '- 正本 SHA16 %s。選定: %s。門の判定: %s。' % (REC['contrasts_sha16'], REC['selection'], REC['gate']), '',
     '- **%s**' % first]
if SEAL:
    L.append('- ' + PS['sign_agreement'].format(agree=agree, confirmed=n_conf) +
             ('（照合できなかった確証の対比 %s・封印の欠け %d 件）' % (unchecked or 'なし', len(SEAL_MISSING)) if (unchecked or SEAL_MISSING) else ''))
else:
    L.append('- 封印の記録が渡されていないので、予想符号との照合は行っていない（裁定 D79・凍結時に封印する）。')
L += ['- ' + PS['scope'], '- ' + PS['style_move'], '- ' + PS['no_p_desc'], '- ' + PS['selection_direction'],
      '- ' + T['style_gate']['asymmetry'], '- ' + T['fwer_note'], '- 区間: ' + T['interval']['note'], '']
if DRY:
    L += ['- **dry-run の走行を読んだ（検査用）**: %s' % '・'.join(DRY), '']
L += ['## 確証の族（**三つ組で読む**・率の単独引用を禁じる）', '',
      '| 対比 | 場面 | 破局 A/n | 破局 B/n | 書式外 A／B | refuse A／B | pt 差 | 区間 | p | Holm | 様式の差 | 札 | 注 |',
      '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
fmt_p = lambda x: ('—' if x is None else ('%.3g' % x if x >= 1e-5 else '<1e-5'))
for r in FAMROWS:
    if r.get('missing'):
        L.append('| %s | %s | — | — | — | — | — | — | — | — | — | %s | |' % (r['id'], r['scenario'], r['label']))
        continue
    L.append('| %s | %s | %d/%d | %d/%d | %s／%s | %s／%s | %s | %s | %s | %s | %s | %s | %s |'
             % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'],
                r.get('ff_pt_A'), r.get('ff_pt_B'), r.get('refuse_pt_A'), r.get('refuse_pt_B'),
                r['diff_pt'], r['ci'], fmt_p(r.get('p')), r.get('holm_alpha') and round(r['holm_alpha'], 5),
                r.get('style_diff_pt'), r['label'], '・'.join(r.get('notes', []))))
L += ['', '## 記述の族（p を印字しない）', '']
for famkey, rows in DESC.items():
    if not rows:
        L.append('- `%s`: **この巡では出さない**（登録された対比が無い）' % famkey)   # 黙って飛ばさない（採否表 P331）
        continue
    L += ['### %s' % famkey, '', '| 対比 | 破局率 A | 破局率 B | pt 差 | 区間 | 書式外 A/B | refuse A/B |', '|---|---|---|---|---|---|---|']
    for r in rows:
        if r.get('missing'):
            L.append('| %s | — | — | — | — | — | — |' % r['id'])
            continue
        L.append('| %s | %s | %s | %s | %s | %s／%s | %s／%s |'
                 % (r['id'], None if r['rate_A'] is None else round(r['rate_A'], 4), None if r['rate_B'] is None else round(r['rate_B'], 4),
                    r['diff_pt'], r['ci'], r['ff_pt_A'], r['ff_pt_B'], r['refuse_pt_A'], r['refuse_pt_B']))
    L.append('')
L += ['## 検査認識の言及率（記述・目安を置かない・裁定 D65）', '', '| 場面 | 腕 | 言及率 pt | n_ok |', '|---|---|---|---|']
for m_ in MENTION:
    L.append('| %s | %s | %s | %d |' % (m_['scenario'], m_['arm'], m_['mention_pt'], m_['n_ok']))
L += ['', '## ランダム方向の三本の率（合併の前・正本 random_control.pooling）', '',
      '- 試行の記録にある方向の id: %s。id が一つしか無い走行では、三本の率を分けて出せない（その旨を記す）。'
      % (sorted(str(x) for x in POOL_IDS if x is not None) or '記録に無い'), '',
      '| 場面 | 腕 | 方向 | 破局/n_ok | 率 | 書式外 |', '|---|---|---|---|---|---|']
L += ['| %s | %s | %s | %d/%d | %s | %d |'
      % (k_[0], k_[1], k_[2], c_['cat'], c_['n_ok'], (None if not c_['n_ok'] else round(c_['cat'] / c_['n_ok'], 4)), c_['ff'])
      for k_, c_ in sorted(BYDIR.items(), key=str) if str(k_[2]).startswith('rand')]
if CHART_BAD:
    L += ['', '## 管理図の異常（正本 calibration.consequence・裁定 D110）', ''] +          ['- %s' % json.dumps(x, ensure_ascii=False) for x in CHART_BAD]
L += ['',
      '## S4 の反証（門 → 三分岐・裁定 D81・D95・D118・D134〜D136）', '',
      '- 札: **%s**（門 %s）' % (s4.get('verdict'), '・'.join(s4.get('gates') or []) or 'なし'),
      '- 封印の値 %s・照合 **%s**（札とは別に出す・正本 `B_desc_S4.seal_match`・裁定 D135）' % (s4.get('seal_value'), s4.get('seal_match'))]
if 'partner_rate' in s4:
    L.append('- pt 差（(6b) − ランダム方向） %s・両側 95%% 区間 %s・（ランダム方向 − (6b)）の片側 95%% 上限 %s pt（効き目 %s pt 未満なら「%s」）・相手の腕の率 %.4f・区間は %s'
             % (s4['diff_pt'], s4['ci'], s4['upper_one_sided_pt'], s4['effect_pt'], T['descriptive_families']['B_desc_S4']['three_way']['labels'][2], s4['partner_rate'], s4['interval']))
    L.append('- 効き目の相対の大きさ（裁定 D136）: 観測した相手の率に対して %s・登録の基底に対して %s。観測した相手の率での動作特性（真に零・真に効き目ちょうど）: %s／%s'
             % (s4['relative_size']['to_observed_partner'], s4['relative_size']['to_registered_base'],
                s4['oc_at_observed_partner']['at_zero'], s4['oc_at_observed_partner']['at_effect']))
L += ['- %s' % x for x in s4.get('notes', [])]
L += ['', '## td の特異性（族ごと・正本 B_desc_textdiff.specificity_rule・裁定 D133）', '',
      '- 両側 Fisher・族の中で場面をまたいで Holm・区間は両側 95% の Newcombe。「書ける」は確証が立った場面で (v − td) が (v − ランダム) と同じ向きに零を外したときだけ。**「書かない」は「O に特有でない」を意味しない。**', '',
      '| 対比 | 族 | 場面 | pt 差（v − td） | 区間 | p | Holm | 確証の対比の札 | 特異性 |', '|---|---|---|---|---|---|---|---|---|']
for t_ in TD_SPEC:
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (t_['id'], t_['family'], t_['scenario'], None if t_.get('diff_pt') is None else round(t_['diff_pt'], 3),
                                                         None if not t_.get('ci') else [round(x, 3) for x in t_['ci']], fmt_p(t_.get('p')),
                                                         t_.get('holm_alpha') and round(t_['holm_alpha'], 5), t_.get('conf_label'), t_.get('label')))
if not TD_SPEC:
    L.append('- 表に載らない（v 対 td の記録が無い）')
L += ['', '## ランダム方向の等質性（正本 random_control.homogeneity_rule・裁定 D127）', '',
      '| 場面 | 腕 | 三本の率の差 pt | 測れた方向 | 注 |', '|---|---|---|---|---|']
for (sc_, arm_), h_ in sorted(HOMOG.items()):
    L.append('| %s | %s | %s | %s | %s |' % (sc_, arm_, None if h_['spread_pt'] is None else round(h_['spread_pt'], 3), h_['measured'],
                                        {True: '**注（不均一）**', False: 'なし', None: '判定しない（方向が二つ未満）'}[h_['note']]))
if not HOMOG:
    L.append('- 表に載らない（方向の id を持つランダム方向の記録が無い）')
L += ['', '## 選定後の品質床（裁定 D77）', '']
L += (['- 落ちた腕: %s' % ('・'.join(sorted(QF_FAIL)) if QF_FAIL else 'なし')] if QF_ROWS else ['- 記録が無い（走行の前）'])
if QF_FAIL:
    L.append('- ' + PS['quality_fail'].format(arms='・'.join(sorted(QF_FAIL))))
L += ['', '## 表に載らない対比・対比に現れない腕（`report_rules`）', '',
      '- 記録の無いセル: %s' % ('・'.join('%s×%s' % x for x in missing) if missing else 'なし'),
      '- 対比に現れない腕（参照のための無操作）: %s' % ('・'.join('%s×%s' % x for x in orphans) if orphans else 'なし'), '']
if STRAT:
    L += ['## 様式門の層別の副次（札を変えない）', '', '| 対比 | 層 | p | pt 差 | n A/B |', '|---|---|---|---|---|']
    for s in STRAT:
        L.append('| %s | %s | %s | %s | %s |' % (s['id'], s['stratum'], s.get('p') and round(s['p'], 5), s.get('diff_pt'), s.get('skipped') or '%s/%s' % (s.get('n_A'), s.get('n_B'))))
    L.append('')
L += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[analyze_B] %s / %s' % (out_md, out_json))
print('  ' + first)
