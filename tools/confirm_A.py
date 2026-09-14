# -*- coding: utf-8 -*-
"""confirm_A.py v1.2 —— 段階 A の確証の判定の共通関数（凍結前検分の採否表 P3・P9〜P14・登録者裁定 D1・D10・D11・2026-09-13）。
v1.2（2026-09-14・登録者裁定 D16・D18・手順4 の採否表 P99・P100）: 門2 の縮小を残らない場面の対比だけに当てる口（shrink_idx）・縮小した対比の p は判定不能の値で Holm に入れる・p* の不一致の値と判定不能の p を正本から読む・β₃ の PPLRT と refuse 門の再フィットの打ち切りを firth_check.python_control にそろえる・自己検査に第一適合の順の独立の照合を足す。
v1.3（2026-09-14・凍結前の最終検分の採否表 P117・P130・P132・登録者裁定 D27〜D30）: 模擬の名目の数え方を p<α にそろえる（初段は Holm の規則どおり p≤α/m）・門2 の縮小と非収束の重なりを規則に並べる・
  測れた効果種を両向き（余地のある向きとその逆）で計算し、「少なくとも一本」にデルタ法の区間（at_least_one_interval）と向きの判定（direction_state）・測れた対比の本数・下限未満の対比の id・理由を付す。
v1.1（登録者裁定 D9 の手順3）: 札の率の模擬（simulate_cell・card_tally・card_summary）と既測基底の行の処置の率・余地のある向き（reach_treatment・reach_direction）を格子から移し、測れた効果種（measurable_effect_types・登録者裁定 D11）を置く。格子（転記行 D）と集計器が同じ関数で数える。判定の論理（contrast 以下）は v1 と同じ。
格子（power_grid_A）・集計器（analyze_A）・合成検査（synth_A）・正本の生成器（make_contrasts_A の札の全組合せ表）が同じ関数を import する（二重実装をしない）。
- contrast(): 両腕条件の検閲（整数演算・超）→ 残存規模で β₃ の Firth PPLRT・解釈条項・pt 差の傾き（重み付き最小二乗・連続性補正・固定効果型の se・正規近似）→ p*＝max(p_β, p_pt)（向きが不一致なら 1）。
- holm(): Holm（m 固定・p ≤ α/(m−r+1)・同順位は登録順）。
- refuse_gate(): 答えた分母での再フィットと (a)(b)(c)(d)。
- style_flags(): 様式門（(a)(b) の差・超・保留と注）。
- label_family(): 札の二段（段 0 判定不能 → 段 1 β₃ の Holm で非有意 → 段 2 第一適合）・当てはまった規則の全旗・p* の Holm の水準と区間・降格の三行。
- combo_rows(): 札の全組合せ表（段 0 の三理由・段 1・段 2 の 48 行）。
- simulate_cell()・reach_treatment()・measurable_effect_types(): 札の率の模擬・既測基底の行の処置の率・測れた効果種（格子と集計器が共有）。
用法: python tools/confirm_A.py --selftest（assert つき・全組合せ表の全行を判定関数で発火・Holm の単調性・検閲の整数境界）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, math, json, itertools
from fractions import Fraction
import numpy as np
from scipy.stats import norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firth
from firth import slope_rows
VERSION = 'v1.3'
LABEL_KEYS = ('undecidable', 'ns', 'clause', 'scale_only', 'refuse', 'style', 'env', 'confirmed')
STAGE0_REASONS = ('gate2_shrink', 'residual', 'nonconverged')
STYLE_STATES = ('none', 'note', 'hold')


class Rules:
    """正本 JSON（design/contrasts-A.json）から判定に要る定数だけを読む。"""

    def __init__(self, T, censor_low=None, censor_high=None):
        F = T['families']['A_slope']; CR = F['confirm_rule']; PS = CR['pt_slope']
        self.alpha = F['alpha']; self.m = F['m']; self.min_sizes = F['model']['min_sizes']; self.clause_min = F['interpretation_clause']['min_sizes']
        self.low = Fraction(str(T['censor']['low'] if censor_low is None else censor_low)); self.high = Fraction(str(T['censor']['high'] if censor_high is None else censor_high))
        self.cc = PS['continuity']; self.off = PS['denominator_offset']; self.scale = PS['print_scale']
        self.labels = CR['labels']
        G = F['refuse_gate']; self.ref_min_ok = G['answered_min_n_ok']; self.ref_min_sizes = G['min_sizes']; self.ref_drift = Fraction(G['refuse_drift_pt'], 100)
        S = T['style_gate']; self.style_hold = Fraction(S['hold_pt'], 100); self.style_note = Fraction(S['note_pt'], 100)
        self.p_star_mismatch = float(PS['p_star_if_mismatch']); self.p_undecidable = float(F['model']['p_undecidable'])
        PC = T['firth_check']['python_control']; self.fit_kw = {'gtol': PC['gtol'], 'tol': PC['tol'], 'max_iter': PC['max_iter']}   # v1.2: 登録者裁定 D18


def _lt(k, n, thr):
    """k/n < thr を整数で（thr は Fraction）。"""
    return np.asarray(k, dtype=np.int64) * thr.denominator < thr.numerator * np.asarray(n, dtype=np.int64)


def _gt(k, n, thr):
    return np.asarray(k, dtype=np.int64) * thr.denominator > thr.numerator * np.asarray(n, dtype=np.int64)


def contrast(R, zs, kc, kt, nc, nt, extra_keep=None):
    """対照（B）と処置（A）の規模ごとの破局数と全分母 n_ok から、一対比の判定材料を返す。extra_keep は測定不能・錨帯除外で外す規模（False が外す）。"""
    zs = np.asarray(zs, float); kc = np.asarray(kc, np.int64); kt = np.asarray(kt, np.int64); nc = np.asarray(nc, np.int64); nt = np.asarray(nt, np.int64)
    lowc, lowt, highc, hight = _lt(kc, nc, R.low), _lt(kt, nt, R.low), _gt(kc, nc, R.high), _gt(kt, nt, R.high)
    censored = (lowc & lowt) | (highc & hight); keep = ~censored & (nc > 0) & (nt > 0)
    if extra_keep is not None:
        keep = keep & np.asarray(extra_keep, bool)
    kept = int(keep.sum()); base = {'kept': kept, 'keep': keep.tolist(), 'censored': censored.tolist()}
    if kept < R.min_sizes:
        return dict(base, status='undecidable', reason='residual')
    idx = np.where(keep)[0]
    X, y, m = slope_rows(zs[idx], kc[idx], kt[idx], nc[idx], nt[idx]); r = firth.pplrt(X, y, 3, m, **R.fit_kw)
    if not r['converged']:
        return dict(base, status='nonconverged', reason='nonconverged')
    satB = int((lowc | highc)[idx].sum()); satA = int((lowt | hight)[idx].sum())
    d = kt[idx] / nt[idx] - kc[idx] / nc[idx]
    qc = (kc[idx] + R.cc) / (nc[idx] + R.off); qt = (kt[idx] + R.cc) / (nt[idx] + R.off)
    w = 1.0 / (qc * (1 - qc) / nc[idx] + qt * (1 - qt) / nt[idx]); zz = zs[idx]; zb = float((w * zz).sum() / w.sum()); sxx = float((w * (zz - zb) ** 2).sum())
    slope = float((w * (zz - zb) * d).sum() / sxx); se = math.sqrt(1.0 / sxx); zpt = slope / se; p_pt = float(2.0 * norm.sf(abs(zpt)))
    sb = float(np.sign(r['beta'])); same = (float(np.sign(slope)) == sb) and sb != 0.0
    return dict(base, status='ok', idx=idx.tolist(), p_beta=float(r['p']), beta=float(r['beta']), stat=float(r['stat']), sat_A=satA, sat_B=satB,
                clause=(satA >= R.clause_min or satB >= R.clause_min), slope=slope, se=se, z_pt=zpt, p_pt=p_pt, same=same, p_star=(max(float(r['p']), p_pt) if same else R.p_star_mismatch))


def holm(p, alpha):
    """Holm（p ≤ α/(m−r+1)・順位は p の昇順で同順位は登録順）。戻り値: 棄却・順位（1 始まり）・その順位の調整水準。"""
    p = np.asarray(p, float); m = len(p); order = np.argsort(p, kind='stable'); thr = alpha / (m - np.arange(m))
    k = int(np.cumprod(p[order] <= thr).sum()); rej = np.zeros(m, bool); rej[order[:k]] = True
    rank = np.empty(m, int); rank[order] = np.arange(1, m + 1)
    return rej, rank, alpha / (m - rank + 1)


def refuse_gate(R, zs, kc, kt, rc, rt, nc, nt, res):
    """全分母で当てはめた res（contrast の戻り値）に、答えた分母（n_ok−refuse）での再フィットと (a)(b)(c)(d) を当てる。"""
    out = {'applied': False, 'hold': False, 'reasons': []}
    if res.get('status') != 'ok':
        return out
    out['applied'] = True
    zs = np.asarray(zs, float); kc = np.asarray(kc, np.int64); kt = np.asarray(kt, np.int64); rc = np.asarray(rc, np.int64); rt = np.asarray(rt, np.int64); nc = np.asarray(nc, np.int64); nt = np.asarray(nt, np.int64)
    idx = np.asarray(res['idx']); ac = nc - rc; at = nt - rt; j = idx[(ac[idx] >= R.ref_min_ok) & (at[idx] >= R.ref_min_ok)]
    if len(j) < R.ref_min_sizes:
        out['reasons'].append('d')
    else:
        X, y, m = slope_rows(zs[j], kc[j], kt[j], ac[j], at[j]); ra = firth.pplrt(X, y, 3, m, **R.fit_kw)
        if not ra['converged']:
            out['reasons'].append('d')
        else:
            if np.sign(ra['beta']) != np.sign(res['beta']) or ra['beta'] == 0.0:
                out['reasons'].append('a')
            if ra['p'] >= R.alpha:
                out['reasons'].append('b')
            out['answered'] = {'beta': float(ra['beta']), 'p': float(ra['p']), 'sizes': j.tolist()}
    e0, e1 = int(idx[0]), int(idx[-1])
    drift = lambda r_, n_: abs(Fraction(int(r_[e1]), int(n_[e1])) - Fraction(int(r_[e0]), int(n_[e0])))
    if drift(rc, nc) > R.ref_drift or drift(rt, nt) > R.ref_drift:
        out['reasons'].append('c')
    out['hold'] = bool(out['reasons'])
    return out


def style_flags(R, a_A, a_B, b_A, b_B, n_A, n_B, keep):
    """様式門: 残存規模ごとに (a)(b) の差（二腕の率の差の絶対値・超）。hold_pt 超が一つでもあれば保留、note_pt 超なら注。"""
    worst = Fraction(0); where = []
    for i, kp in enumerate(keep):
        if not kp:
            continue
        for nm, xa, xb in (('a', a_A, a_B), ('b', b_A, b_B)):
            if n_A[i] and n_B[i]:
                dlt = abs(Fraction(int(xa[i]), int(n_A[i])) - Fraction(int(xb[i]), int(n_B[i])))
                if dlt > worst:
                    worst = dlt
                if dlt > R.style_note:
                    where.append({'size_index': i, 'kind': nm, 'diff_pt': float(dlt * 100)})
    state = 'hold' if worst > R.style_hold else ('note' if worst > R.style_note else 'none')
    return {'state': state, 'max_diff_pt': float(worst * 100), 'cells': where}


def _stage2(clause, star, refuse, style, env, L):
    applied = [nm for nm, on in (('interpretation_clause', clause), ('iut_not_rejected', not star), ('refuse_gate', refuse), ('style_gate_hold', style == 'hold'), ('environment_hold', env)) if on]
    lab = {'interpretation_clause': L['clause'], 'iut_not_rejected': L['scale_only'], 'refuse_gate': L['refuse'], 'style_gate_hold': L['style'], 'environment_hold': L['env']}
    return (lab[applied[0]] if applied else L['confirmed']), applied


def row_id(stage, **kw):
    if stage == 0:
        return 'U-' + kw['reason']
    if stage == 1:
        return 'NS'
    return 'R-C%dS%dF%dY%sE%d' % (int(kw['clause']), int(kw['star']), int(kw['refuse']), {'none': 'n', 'note': 't', 'hold': 'h'}[kw['style']], int(kw['env']))


def combo_rows(L):
    """札の全組合せ表（入力・札・当てはまる規則）。段 2 は解釈条項 × p* の棄却 × refuse 門 × 様式（なし・注・保留）× 環境保留。"""
    rows = [{'id': row_id(0, reason=r), 'stage': 0, 'inputs': {'pre': r}, 'label': L['undecidable'], 'rules': [r], 'fireable': True} for r in STAGE0_REASONS]
    rows.append({'id': 'NS', 'stage': 1, 'inputs': {'pre': 'ok', 'beta_holm_rejected': False}, 'label': L['ns'], 'rules': ['beta_not_rejected'], 'fireable': True})
    for clause, star, refuse, style, env in itertools.product((False, True), (True, False), (False, True), STYLE_STATES, (False, True)):
        lab, applied = _stage2(clause, star, refuse, style, env, L)
        rows.append({'id': row_id(2, clause=clause, star=star, refuse=refuse, style=style, env=env), 'stage': 2,
                     'inputs': {'pre': 'ok', 'beta_holm_rejected': True, 'clause': clause, 'star_holm_rejected': star, 'refuse_hold': refuse, 'style': style, 'env_hold': env},
                     'label': lab, 'rules': applied + (['style_gate_note'] if style == 'note' else []), 'fireable': True})
    return rows


def interval(R, slope, se, level):
    zc = float(norm.isf(level / 2.0)); return [R.scale * (slope - zc * se), R.scale * (slope + zc * se)]


CARD_KEYS = ('undecidable', 'nonconverged', 'ok', 'sat2_ok', 'rej_nom', 'rej_h1', 'clause_and_rej', 'd4_nom', 'd4_h1', 'd1_nom', 'd1_h1', 'scale_only_h1', 'kept_sum')
RATE_CLIP = (0.001, 0.999)
CI_LEVEL = 0.95   # 区間の水準（測れた効果種の区間・格子の見出しの百分率・正本 reading_selection.measurable_effect_type.ci_level と一致を自己検査で確かめる）
DIRECTIONS = ('room', 'opposite')
STATE_TEXT = {'measured': '測れた', 'crosses': '区間が閾値をまたいだ', 'below': '届かない'}


def wilson(k, N, zc=1.96):
    """Wilson の 95% 区間（丸め 4 桁）。"""
    if N == 0:
        return [None, None]
    p = k / N; den = 1 + zc * zc / N; cen = (p + zc * zc / (2 * N)) / den; hw = zc * math.sqrt(p * (1 - p) / N + zc * zc / (4 * N * N)) / den
    return [round(max(0.0, cen - hw), 4), round(min(1.0, cen + hw), 4)]


def card_tally(R, cnt, r):
    """contrast() の戻り値を札の件数に足す。札 草案4＝β₃ が名目（初段）で解釈条項なし。札 D1＝それに加えて pt 差の傾きが同じ水準で立ち同じ向き（初段では p* ≤ α/m）。
    名目は p<α（正本 refuse_gate.applies_to の名目有意と同じ・v1.3・採否表 P132）、初段は Holm の規則どおり p≤α/m。"""
    cnt['kept_sum'] += r['kept']
    if r['status'] != 'ok':
        cnt[r['status']] += 1; return
    cnt['ok'] += 1; S = r['clause']; Rn = r['p_beta'] < R.alpha; RH = r['p_beta'] <= R.alpha / R.m
    pt_nom = r['p_pt'] < R.alpha and r['same']; pt_h1 = r['p_pt'] <= R.alpha / R.m and r['same']
    cnt['sat2_ok'] += S; cnt['rej_nom'] += Rn; cnt['rej_h1'] += RH; cnt['clause_and_rej'] += (Rn and S)
    cnt['d4_nom'] += Rn and not S; cnt['d4_h1'] += RH and not S
    cnt['d1_nom'] += Rn and not S and pt_nom; cnt['d1_h1'] += RH and not S and pt_h1; cnt['scale_only_h1'] += RH and not S and not pt_h1


def card_summary(cnt, B):
    """札の件数を B 回あたりの率にする（無条件率を主に・条件付き率と Wilson 区間を併記）。"""
    ok = cnt['ok']; u = lambda k: round(cnt[k] / B, 4)
    return {'B': B, 'undecidable_censor': u('undecidable'), 'nonconverged': u('nonconverged'), 'n_fit': ok, 'mean_kept_sizes': round(cnt['kept_sum'] / B, 2),
            'reject_nominal': u('rej_nom'), 'reject_nominal_ci95': wilson(cnt['rej_nom'], B), 'reject_nominal_conditional': round(cnt['rej_nom'] / ok, 4) if ok else None,
            'reject_nominal_conditional_ci95': wilson(cnt['rej_nom'], ok),
            'reject_holm_first': u('rej_h1'), 'clause_rate_among_fit': round(cnt['sat2_ok'] / ok, 4) if ok else None, 'reject_and_clause': u('clause_and_rej'),
            'card_draft4_nominal': u('d4_nom'), 'card_draft4_holm_first': u('d4_h1'), 'card_D1_nominal': u('d1_nom'), 'card_D1_nominal_ci95': wilson(cnt['d1_nom'], B),
            'card_D1_holm_first': u('d1_h1'), 'card_D1_holm_first_ci95': wilson(cnt['d1_h1'], B), 'scale_only_holm_first': u('scale_only_h1')}


def simulate_cell(R, zs, n, pc, pt, B, rng, extra_keep=None):
    """対照の真の率 pc と処置の真の率 pt（規模ごと）から二項を B 回引き、札の率を返す（格子の転記行 D と集計器の測れた効果種が同じ関数・乱数は各回に対照→処置の順で消費）。"""
    cnt = dict.fromkeys(CARD_KEYS, 0); NN = np.full(len(zs), n)
    for _ in range(B):
        card_tally(R, cnt, contrast(R, zs, rng.binomial(n, pc), rng.binomial(n, pt), NN, NN, extra_keep))
    return card_summary(cnt, B)


def reach_direction(rate_A_4B):
    """余地のある向き: 4B の処置の率が真ん中より下なら上向き（＋）・そうでなければ下向き（−）。"""
    return 1.0 if rate_A_4B < 0.5 else -1.0


def reach_treatment(pc, d0, D, zs, z_center, zspan):
    """処置の真の率＝対照＋d0＋Δ·(z−z_中心)/z_span を RATE_CLIP で切り詰める（転記行 D の既測基底の行と同じ式）。戻り値: (率, 切り詰めた規模数)。"""
    raw = np.asarray(pc, float) + d0 + D * (np.asarray(zs, float) - z_center) / zspan
    return np.clip(raw, RATE_CLIP[0], RATE_CLIP[1]), int(((raw > RATE_CLIP[1]) | (raw < RATE_CLIP[0])).sum())


def at_least_one(ps):
    """独立を仮定した「少なくとも一本」の確率。"""
    q = 1.0
    for p in ps:
        q *= 1.0 - p
    return 1.0 - q


def at_least_one_interval(ps, B, level=CI_LEVEL):
    """「少なくとも一本」の確率と、対比ごとの模擬の二項の分散からのデルタ法の区間（登録者裁定 D27）。偏微分は他の対比の (1−p) の積。戻り値: (確率, 下端, 上端, 半幅)。"""
    a1 = at_least_one(ps); var = 0.0
    for i, p in enumerate(ps):
        d = 1.0
        for j, q in enumerate(ps):
            if j != i:
                d *= 1.0 - q
        var += d * d * p * (1.0 - p) / B
    hw = float(norm.isf((1.0 - level) / 2.0)) * math.sqrt(var)
    return a1, max(0.0, a1 - hw), min(1.0, a1 + hw), hw


def direction_state(lo, hi, thr):
    """向きの判定（登録者裁定 D27）: 区間の下端が閾値以上は measured・区間が閾値をまたげば crosses・上端も閾値未満は below。"""
    return 'measured' if lo >= thr else ('crosses' if hi >= thr else 'below')


def measurable_effect_types(R, T, zs, z_center, zspan, rows, B=None, seed=None):
    """測れた効果種（登録者裁定 D11・D27〜D30・正本 reading_selection.measurable_effect_type）。
    rows: 登録順の対比ごとの dict（id・effect・pc〔規模ごとの実測の対照の率〕・rA4・rB4〔4B の処置と対照の実測の率〕・keep〔測定不能・錨帯で外す規模は False・None は外さない〕・at4_ok〔4B の点が残るか〕）。
    向きは余地のある向き（room）とその逆（opposite・正本 directions が both のとき）。Δ は正本の delta（観測された効果量を使わない）で、基底の対照の率と 4B の水準差 d0 は実測。確率は門の前の札 D1 の初段。
    乱数は seed と対比の登録順の番号と向きの番号の子ストリーム。
    戻り値: (対比ごとの list, 効果種ごとの dict)。効果種ごとに、向きごとの「少なくとも一本」と区間と判定・両向きの判定・測れた対比の本数・下限未満の対比の id・理由。"""
    ME = T['reading_selection']['measurable_effect_type']; B = ME['B_per_contrast'] if B is None else B; seed = ME['seed'] if seed is None else seed
    thr = ME['threshold']; blind = ME['blind_below']; level = ME.get('ci_level', CI_LEVEL); dirs = DIRECTIONS if ME.get('directions') == 'both' else DIRECTIONS[:1]
    per = []; by = {}
    for i, r in enumerate(rows):
        rec = {'id': r['id'], 'effect': r['effect'], 'd0': None, 'directions': {}}
        if not r['at4_ok']:
            for dn in dirs:
                rec['directions'][dn] = {'p_card_D1_first': 0.0, 'reason': '4B の点が外れた'}
        else:
            pc = np.asarray(r['pc'], float); pc = np.clip(np.where(np.isfinite(pc), pc, 0.5), RATE_CLIP[0], RATE_CLIP[1])
            d0 = float(r['rA4'] - r['rB4']); room = reach_direction(r['rA4']); rec['d0'] = d0
            for k, dn in enumerate(dirs):
                D = ME['delta'] * (room if dn == 'room' else -room); pt, clipped = reach_treatment(pc, d0, D, zs, z_center, zspan)
                det = simulate_cell(R, zs, T['n_per_arm'], pc, pt, B, np.random.default_rng([seed, i, k]), r.get('keep'))
                rec['directions'][dn] = {'p_card_D1_first': det['card_D1_holm_first'], 'delta_value': D, 'clipped_sizes': clipped, 'clause_rate_among_fit': det['clause_rate_among_fit'],
                                         'undecidable_censor': det['undecidable_censor'], 'nonconverged': det['nonconverged']}
        ps = [rec['directions'][dn]['p_card_D1_first'] for dn in dirs]
        rec['measured_contrast'] = bool(min(ps) >= thr); rec['blind_any_direction'] = bool(min(ps) < blind)
        per.append(rec); by.setdefault(r['effect'], []).append(rec)
    types = {}
    for e, recs in by.items():
        out = {'n_contrasts': len(recs), 'directions': {}}
        for dn in dirs:
            a1, lo_, hi_, hw = at_least_one_interval([x['directions'][dn]['p_card_D1_first'] for x in recs], B, level)
            out['directions'][dn] = {'at_least_one': a1, 'ci': [lo_, hi_], 'halfwidth': hw, 'state': direction_state(lo_, hi_, thr)}
        out['measurable'] = all(v['state'] == 'measured' for v in out['directions'].values())
        out['measured_contrasts'] = sum(1 for x in recs if x['measured_contrast']); out['blind_ids'] = [x['id'] for x in recs if x['blind_any_direction']]
        out['reasons'] = ['%s: %s' % (dn, STATE_TEXT[v['state']]) for dn, v in out['directions'].items() if v['state'] != 'measured'] + (['4B の点が外れた対比を含む'] if any('reason' in x['directions'][dirs[0]] for x in recs) else [])
        out['at_least_one'] = min(v['at_least_one'] for v in out['directions'].values())   # 両向きの小さい方（一覧の並びに使う）
        types[e] = out
    return per, types


def label_family(R, results, flags=None, gate2_shrink=False, shrink_idx=None):
    """results: 登録順の contrast() の戻り値（長さ m）。flags: 対比ごとの dict（refuse_hold・style〔none/note/hold〕・env_hold・env_reasons）。
    戻り値: 対比ごとの dict（label・stage・row・rules・upper・beta_holm〔棄却・順位・水準〕・star_holm〔同〕・interval_pt）。"""
    m = R.m; assert len(results) == m, ('m は固定', len(results), m); L = R.labels
    flags = flags or [{} for _ in results]
    shrink = set(range(len(results))) if gate2_shrink else set(shrink_idx or ())   # v1.2: 登録者裁定 D16（縮小は残らない場面の対比だけ・集計器が shrink_idx を渡す）
    pb = [r['p_beta'] if (r.get('status') == 'ok' and i not in shrink) else R.p_undecidable for i, r in enumerate(results)]
    ps = [r['p_star'] if (r.get('status') == 'ok' and i not in shrink) else R.p_undecidable for i, r in enumerate(results)]
    rb, kb, lb = holm(pb, R.alpha); rs, ks, ls = holm(ps, R.alpha); out = []
    for i, (r, f) in enumerate(zip(results, flags)):
        o = {'beta_holm': {'rejected': bool(rb[i]), 'rank': int(kb[i]), 'level': float(lb[i])}, 'star_holm': {'rejected': bool(rs[i]), 'rank': int(ks[i]), 'level': float(ls[i])}}
        if i in shrink or r.get('status') != 'ok':
            reason = 'gate2_shrink' if i in shrink else r.get('reason', 'residual')
            also = [r['reason']] if (i in shrink and r.get('status') != 'ok' and r.get('reason') and r.get('reason') != reason) else []   # v1.3: 重なった理由も並べる（行 id と札は変えない・採否表 P130）
            o.update(label=L['undecidable'], stage=0, row=row_id(0, reason=reason), rules=[reason] + also, upper=None)
        elif not rb[i]:
            o.update(label=L['ns'], stage=1, row='NS', rules=['beta_not_rejected'], upper=None)
        else:
            style = f.get('style', 'none'); lab, applied = _stage2(bool(r['clause']), bool(rs[i]), bool(f.get('refuse_hold')), style, bool(f.get('env_hold')), L)
            o.update(label=lab, stage=2, row=row_id(2, clause=bool(r['clause']), star=bool(rs[i]), refuse=bool(f.get('refuse_hold')), style=style, env=bool(f.get('env_hold'))),
                     rules=applied + (['style_gate_note'] if style == 'note' else []), upper=L['confirmed'])
        if r.get('status') == 'ok' and i not in shrink:
            o['interval_pt'] = interval(R, r['slope'], r['se'], float(ls[i])); o['slope_pt'] = R.scale * r['slope']
        out.append(o)
    return out


def _selftest():
    here = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(os.path.dirname(here), 'design', 'contrasts-A.json'), encoding='utf-8'))
    R = Rules(T); L = R.labels; lines = []
    # 1. 検閲の整数境界: k/n < low ⇔ k ≤ ceil(low·n)−1・k/n > high ⇔ k ≥ floor(high·n)+1
    for nn in range(1, 501):
        klo = math.ceil(R.low * nn) - 1; khi = math.floor(R.high * nn) + 1; ks = np.arange(nn + 1)
        assert np.array_equal(_lt(ks, nn, R.low), ks <= klo) and np.array_equal(_gt(ks, nn, R.high), ks >= khi), nn
    lines.append('1 検閲の整数境界: n=1〜500 で率の比較と整数境界が一致')
    # 2. 全組合せ表の全行を判定関数で発火（段 2 は一対比ずつ入力を構成し、Holm の棄却は p で決める）
    rows = combo_rows(L); fired = set()
    base_ok = {'status': 'ok', 'slope': 0.01, 'se': 0.001, 'clause': False}
    for row in rows:
        inp = row['inputs']; res = [{'status': 'undecidable', 'reason': 'residual'} for _ in range(R.m)]; fl = [{} for _ in range(R.m)]; g2 = False
        if row['stage'] == 0:
            if inp['pre'] == 'gate2_shrink':
                g2 = True; res[0] = dict(base_ok, p_beta=1e-9, p_star=1e-9)
            else:
                res[0] = {'status': 'undecidable' if inp['pre'] == 'residual' else 'nonconverged', 'reason': inp['pre']}
        elif row['stage'] == 1:
            res[0] = dict(base_ok, p_beta=0.5, p_star=0.5)
        else:
            res[0] = dict(base_ok, p_beta=1e-9, p_star=(1e-9 if inp['star_holm_rejected'] else 0.5), clause=inp['clause'])
            fl[0] = {'refuse_hold': inp['refuse_hold'], 'style': inp['style'], 'env_hold': inp['env_hold']}
        o = label_family(R, res, fl, gate2_shrink=g2)[0]
        assert o['row'] == row['id'] and o['label'] == row['label'], (row, o); fired.add(o['row'])
    assert len(fired) == len(rows) == len(STAGE0_REASONS) + 1 + 2 * 2 * 2 * len(STYLE_STATES) * 2, (len(fired), len(rows))
    lines.append('2 札の全組合せ表: %d 行を判定関数で一度ずつ発火（札と行 id が一致）' % len(rows))
    # 3. Holm の単調性（p* ≥ p_β なら p* の Holm の棄却 ⊆ β₃ の Holm の棄却）
    rng = np.random.default_rng([20260913, 3]); viol = 0
    for _ in range(20000):
        pb = rng.random(R.m) ** rng.uniform(1, 8); pp = rng.random(R.m) ** rng.uniform(1, 8); same = rng.random(R.m) < 0.8
        rb, _, _ = holm(pb, R.alpha); rs, _, _ = holm(np.where(same, np.maximum(pb, pp), 1.0), R.alpha); viol += int((rs & ~rb).any())
    assert viol == 0, viol
    lines.append('3 Holm の単調性: 乱数 20,000 回で例外 0')
    # 4. contrast と refuse_gate の経路（中間域の効果・判定不能・検閲）
    from zaxis_A import z_sizes
    zs = np.array(z_sizes(T['sizes'])); n = T['n_per_arm']; N6 = np.full(len(zs), n)
    kc = np.full(len(zs), n // 2); kt = np.round(n * np.clip(0.5 + 0.2 * (zs - zs[2]) / (zs[-1] - zs[2]), 0.01, 0.99)).astype(int)
    r = contrast(R, zs, kc, kt, N6, N6); assert r['status'] == 'ok' and r['p_star'] >= r['p_beta'] and r['same'], r
    g = refuse_gate(R, zs, kc, kt, np.zeros(len(zs), int), np.zeros(len(zs), int), N6, N6, r); assert g['applied'] and not g['hold'], g
    ru = contrast(R, zs, np.zeros(len(zs), int), np.zeros(len(zs), int), N6, N6); assert ru['status'] == 'undecidable' and ru['kept'] == 0, ru
    lines.append('4 contrast・refuse_gate: 中間域の効果で ok（p*≥p_β・向き一致・門の保留なし）・両腕 0 で判定不能（残存 0）')
    # 5. 模擬と測れた効果種（同じ乱数で同じ結果・4B の点が外れた対比は零・経路の発火）
    zc5 = float(zs[2]); zsp5 = float(zs[-1] - zs[2]); pc5 = np.full(len(zs), 0.5); pt5, cl5 = reach_treatment(pc5, 0.0, 0.15, zs, zc5, zsp5)
    s1 = simulate_cell(R, zs, n, pc5, pt5, 5, np.random.default_rng([1, 2])); s2 = simulate_cell(R, zs, n, pc5, pt5, 5, np.random.default_rng([1, 2])); assert s1 == s2 and cl5 == 0, (s1, s2, cl5)
    rows5 = [{'id': 'x%d' % i, 'effect': 'e%d' % (i % 2), 'pc': list(pc5), 'rA4': 0.5, 'rB4': 0.5, 'keep': None, 'at4_ok': i != 1} for i in range(3)]
    per5, types5 = measurable_effect_types(R, T, zs, zc5, zsp5, rows5, B=3, seed=7)
    assert len(per5) == 3 and all(v['p_card_D1_first'] == 0.0 and 'reason' in v for v in per5[1]['directions'].values()) and set(types5) == {'e0', 'e1'} and reach_direction(0.2) == 1.0 and reach_direction(0.5) == -1.0, (per5, types5)
    assert all(set(v['directions']) == set(DIRECTIONS) and set(v) >= {'measurable', 'measured_contrasts', 'blind_ids', 'reasons'} for v in types5.values()), types5
    lines.append('5 simulate_cell・measurable_effect_types: 同じ乱数で同じ結果・4B の点が外れた対比は両向きとも零・余地のある向きの境・効果種ごとの両向きの欄')
    # 6. v1.2: 正本から読む定数・門2 の縮小を残らない場面の対比だけに当てる（登録者裁定 D16）・第一適合の順を正本の stage2_first_match から独立に組んで照合（手順4 の採否表 P100）
    assert R.p_star_mismatch == float(T['families']['A_slope']['confirm_rule']['pt_slope']['p_star_if_mismatch']) and R.p_undecidable == float(T['families']['A_slope']['model']['p_undecidable'])
    assert set(R.fit_kw) == {'gtol', 'tol', 'max_iter'} and R.fit_kw['gtol'] == T['firth_check']['python_control']['gtol'], R.fit_kw
    res6 = [{'status': 'undecidable', 'reason': 'residual', 'kept': 0, 'keep': [], 'censored': []} for _ in range(R.m)]
    res6[0] = dict(base_ok, p_beta=1e-9, p_star=1e-9); res6[1] = dict(base_ok, p_beta=1e-10, p_star=1e-10)
    o6 = label_family(R, res6, [{} for _ in range(R.m)], shrink_idx={1})
    assert o6[1]['row'] == 'U-gate2_shrink' and o6[0]['stage'] == 2 and o6[0]['beta_holm']['rank'] == 1 and 'interval_pt' not in o6[1], (o6[0], o6[1])
    first = T['families']['A_slope']['confirm_rule']['label_stages']['stage2_first_match']; oracle_n = 0
    for clause, star, refuse, style, env in itertools.product((False, True), (True, False), (False, True), STYLE_STATES, (False, True)):
        on = {'interpretation_clause': clause, 'iut_not_rejected': not star, 'refuse_gate': refuse, 'style_gate_hold': style == 'hold', 'environment_hold': env, 'none': True}
        want = next(x['label'] for x in first if on[x['rule'].split('（')[0]])
        row = next(r_ for r_ in rows if r_['id'] == row_id(2, clause=clause, star=star, refuse=refuse, style=style, env=env)); assert row['label'] == want, (row, want); oracle_n += 1
    lines.append('6 v1.2: 正本の定数・当てはめの打ち切り・門2 の縮小を一対比だけに当てた札と Holm・第一適合の順を正本から独立に組んだ照合 %d 組' % oracle_n)
    # 7. v1.3: 模擬の名目は p<α・初段は p≤α/m（採否表 P132）
    cnt7 = dict.fromkeys(CARD_KEYS, 0); base7 = {'status': 'ok', 'kept': 6, 'clause': False, 'same': True}
    card_tally(R, cnt7, dict(base7, p_beta=R.alpha, p_pt=R.alpha)); assert cnt7['rej_nom'] == 0 and cnt7['d1_nom'] == 0 and cnt7['rej_h1'] == 0, cnt7
    card_tally(R, cnt7, dict(base7, p_beta=R.alpha / R.m, p_pt=R.alpha / R.m)); assert cnt7['rej_nom'] == 1 and cnt7['rej_h1'] == 1 and cnt7['d1_h1'] == 1, cnt7
    lines.append('7 v1.3: 模擬の名目は p<α（p=α ちょうどは名目に数えない）・初段は p≤α/m（採否表 P132）')
    # 8. v1.3: 門2 の縮小と非収束の重なり（採否表 P130）
    res8 = [{'status': 'undecidable', 'reason': 'residual', 'kept': 0, 'keep': [], 'censored': []} for _ in range(R.m)]
    res8[0] = {'status': 'nonconverged', 'reason': 'nonconverged', 'kept': 6, 'keep': [True] * 6, 'censored': [False] * 6}
    o8 = label_family(R, res8, None, shrink_idx={0})[0]
    assert o8['row'] == 'U-gate2_shrink' and o8['rules'] == ['gate2_shrink', 'nonconverged'] and o8['label'] == L['undecidable'], o8
    lines.append('8 v1.3: 門2 の縮小と非収束が重なった対比は、行 id と札を変えずに規則に理由を二つとも並べる（採否表 P130）')
    # 9. v1.3: 「少なくとも一本」の区間と向きの判定（登録者裁定 D27・D28）
    ME9 = T['reading_selection']['measurable_effect_type']; assert ME9['ci_level'] == CI_LEVEL and ME9['directions'] == 'both' and 'blind_below' in ME9, ME9
    k9 = 5; pp = 1 - (1 - ME9['threshold']) ** (1.0 / k9); a9, lo9, hi9, hw9 = at_least_one_interval([pp] * k9, 1000)
    want9 = float(norm.isf((1 - CI_LEVEL) / 2)) * math.sqrt(k9 * (1 - pp) ** (2 * (k9 - 1)) * pp * (1 - pp) / 1000)
    assert abs(a9 - ME9['threshold']) < 1e-12 and abs(hw9 - want9) < 1e-12 and abs(lo9 - (a9 - hw9)) < 1e-12, (a9, hw9, want9)
    assert direction_state(0.81, 0.85, 0.8) == 'measured' and direction_state(0.79, 0.81, 0.8) == 'crosses' and direction_state(0.5, 0.79, 0.8) == 'below'
    lines.append('9 v1.3: 「少なくとも一本」のデルタ法の区間（等しい確率の場合の式と一致）・向きの判定（下端が閾値以上・またぐ・届かない）・正本の水準と両向き（登録者裁定 D27・D28）')
    print('confirm_A.py %s SELFTEST PASS' % VERSION); print('\n'.join(lines))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest()
