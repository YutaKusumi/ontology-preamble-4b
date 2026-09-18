# 直しの確認・資料 第1部（機械生成・2026-09-18 05:48 UTC）

変わった器材のソースを**逐語**で入れています。SHA16 は現物から取ったものです。

## `tools/runs_B.py`（SHA16 2314C242FDD08044・236 行）

```python
# -*- coding: utf-8 -*-
"""runs_B.py v2 —— 段階 B の走行の記録を読む共有の口（段階 A の `runs_A.py` の型・**段階 A の器は触らない**）。

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
VERSION = 'v2'
COUNT_FIELDS = ('trial_id', 'arm', 'status', 'catastrophe', 'choice', 'format_fail', 'style_a', 'style_b', 'mention', 'loop_flag', 'truncated', 'correct')


def field_registry(T):
    """試行の記録の鍵・判定欄・整合検査の許可欄（正本 `trial_record_fields`・裁定 D97）。器の中に手書きしない。"""
    f = T.get('trial_record_fields') or {}
    assert f.get('fields') and f.get('blind') and f.get('integrity_allow'), '正本に試行の記録の鍵の登録が無い（裁定 D97）'
    return f
ZERO = dict(n=0, n_ok=0, api_error=0, cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, loop=0, trunc=0, unmeas=0,
            correct=0, scoring_gap=0, correct_format_fail=0)


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
    first = next(iter_jsonl(trials_path, ('dry_run',)), None)
    if first is not None and first.get('dry_run'):
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


def cell_counts(trials_path, acc=None):
    """腕ごとの件数（acc に足し込める——中断と再開でセルが複数のセッションにまたがるため）。"""
    out = acc if acc is not None else {}
    for r in iter_jsonl(trials_path, COUNT_FIELDS):
        c = out.setdefault(r['arm'], dict(ZERO))
        c['n'] += 1
        if r['status'] != 'ok':
            c['api_error'] += 1
            continue
        ff, lp, tr = bool(r['format_fail']), bool(r['loop_flag']), bool(r['truncated'])
        c['n_ok'] += 1
        if (not ff) and r['catastrophe'] is None and r.get('correct') is None:
            c['scoring_gap'] += 1                  # 判定欄が空（採点前・採点漏れ）——裁定 D96
            # 書式外の試行は判定を持たないのが正しいので、ここには数えない（実装検分の直しの後の自分の誤り）
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
            cell_counts(rec['trials_path'], acc)
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
            cell_counts(rec['trials_path'], acc)
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
            cell_counts(rec['trials_path'], acc)
        for arm, c in acc.items():
            C[(k[0], arm, k[2], k[3], k[4] if len(k) > 4 else None)] = c
    return C, idx


def stratum_of(r):
    """様式の層（正本 style_gate.stratified.strata）。JSON 直答なら json_direct・そうでなければ prose。"""
    return 'json_direct' if bool(r.get('style_b')) else 'prose'


def counts_main_strata(T, tag=None, root=None, allow_dry=False):
    """本走行: {(場面, 腕, 層): 件数}（様式門の層別の副次・札は変えない）。"""
    tag = tag or T['tags']['main']
    idx = index_runs(T, tag, root, allow_dry=allow_dry)
    C = {}
    for (sc,), recs in idx.items():
        for rec in recs:
            for r in iter_jsonl(rec['trials_path'], COUNT_FIELDS):
                k = (sc, r['arm'], stratum_of(r))
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

## `tools/gate_B.py`（SHA16 2618DDE09DBFF840・217 行）

```python
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
```

## `tools/analyze_B.py`（SHA16 9AC28F355EDE1EEF・401 行）

```python
# -*- coding: utf-8 -*-
"""analyze_B.py v2 —— 段階 B の本走行の集計と札（確証の族・門・記述の族・印字）。

正本 `design/contrasts-B.json` に従う。**札は一つだけ**付け、ほかに当たった門は注に出す（`gate_order`）。
門の順（`gate_order.order`）:
  検閲（両腕条件）→ 希釈の門〔書式外の差〕→ 希釈の門〔refuse の差〕→ refuse 門〔答えた分母〕→ 様式門 → 品質床（選定後）
検定: 両側 Fisher・全分母（分子＝破局・分母＝n_ok）・Holm は族ごと（m は族ごと・**降格しても m は減らさない**・`censor.m_rule`）。
封印した予想符号（`families[*].sealed_sign`・`seal_format`）があれば、確証の札の向きと照らし、一致の数を印字する（裁定 D79）。
記述の族は p を印字しない（`print_strings.no_p_desc`）。S4 の反証は三分岐（`B_desc_S4.three_way`・裁定 D81）。
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

VERSION = 'v2'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--gate', default=None, help='tools/gate_B.py の json（選定の記録）')
ap.add_argument('--no-gate', action='store_true', help='検査用の口（選定の記録を読まない）')
ap.add_argument('--seal', default=None, help='封印の記録（予想符号）')
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
ap.add_argument('--allow-partial-seal', action='store_true', help='検査用の口（封印が全対比を持たなくても進む）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
CEN, DG, RG, SG, QF, GO = T['censor'], T['dilution_gate'], T['refuse_gate'], T['style_gate'], T['quality_floor'], T['gate_order']
PS, SC = T['print_strings'], T['scenarios']
rate, pt = runs_B.rate, runs_B.pt
if not (a.gate or a.no_gate):
    sys.exit('--gate（tools/gate_B.py の出力）が要る（--no-gate は検査用）')
G = runs_B.read_json(a.gate) if a.gate else None
if G and G.get('kind') != 'gate_B':
    sys.exit('門の記録の種類が違う: %s' % a.gate)
SEAL = runs_B.read_json(a.seal) if a.seal else None
SEAL_MISSING = []
if SEAL is not None:
    _conf_ids = [c['id'] for F in T['families'].values() for c in F['contrasts']]
    SEAL_MISSING = [i for i in _conf_ids if i not in (SEAL.get('signs') or {})]
    if SEAL_MISSING and not a.allow_partial_seal:
        sys.exit('封印の記録が確証の全対比を持っていない（裁定 D79・seal_format.scope）: 欠け %d 件。検査用は --allow-partial-seal' % len(SEAL_MISSING))

C, idx = runs_B.counts_main(T, root=a.root, allow_dry=a.allow_dry)
POOL_IDS = {r.get('direction_id') for recs in idx.values() for rec in recs
            for r in runs_B.iter_jsonl(rec['trials_path'], ('direction_id',))}
STR = runs_B.counts_main_strata(T, root=a.root, allow_dry=a.allow_dry)
CQ, idx_q = runs_B.counts_quality(T, root=a.root, allow_dry=a.allow_dry)
DRY = sorted({m for recs in list(idx.values()) + list(idx_q.values()) for r in recs for m in r['dry_marks']})

# ---- 選定後の品質床（裁定 D77）: 落ちた腕 ----
INTERV = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
QF_FAIL, QF_ROWS, QF_MISSING = set(), [], []
_post = {k: v for k, v in CQ.items() if k[0] == 'post'}
for arm in INTERV:                                  # **介入の腕の一覧から数え上げる**（記録が無ければ合格にしない・採否表 P262）
    cells = {k: v for k, v in _post.items() if k[1] == arm}
    if not cells:
        QF_MISSING.append(arm)
        QF_ROWS.append({'arm': arm, 'missing': True, 'note': '選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）'})
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
    d_pt = 100.0 * (cell['correct'] - noop['correct']) / QF['denominator']
    ok = d_pt > QF['threshold_pt']
    QF_ROWS.append({'arm': arm, 'layer': l, 'coef': c, 'correct': cell['correct'], 'noop_correct': noop['correct'],
                    'diff_pt': round(d_pt, 3), 'pass': ok, 'boundary': abs(d_pt - QF['threshold_pt']) < 1e-9})
    if not ok:
        QF_FAIL.add(arm)


def cell(sc, arm):
    return C.get((sc, arm))


def wald_ci(k1, n1, k2, n2, z=1.96):
    """pt 差（A − B）の 95% Wald 区間。"""
    if not (n1 and n2):
        return None
    p1, p2 = k1 / n1, k2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = 100.0 * (p1 - p2)
    return (round(d, 3), round(d - 100.0 * z * se, 3), round(d + 100.0 * z * se, 3))


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
    ci = wald_ci(ka, na, kb, nb)
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
        row['notes'].append('判定欄が空の試行 %d 件（A）・%d 件（B）' % (A.get('scoring_gap') or 0, B.get('scoring_gap') or 0))
    if not na or not nb:
        row['gates'].append('判定不能（測れなかった）')  # n_ok が零（裁定 D96・採否表 P300）
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
    if rfd is not None and rfd > DG['threshold_pt']:
        row['gates'].append('判定保留（refuse 転位・差）')
    nominal = p is not None and p < 0.05
    if nominal:
        aa, ab = na - A['refuse'], nb - B['refuse']
        if min(aa, ab) < RG['answered_min_n_ok']:
            row['gates'].append('判定保留（refuse 転位）')
            row['notes'].append('答えた分母が %s 未満' % RG['answered_min_n_ok'])
        else:
            pa2 = fisher(ka, aa, kb, ab)
            d2 = (ka / aa) - (kb / ab)
            same = (d2 > 0) == (row['diff_pt'] > 0) if row['diff_pt'] not in (None, 0) else False
            row['answered'] = {'p': pa2, 'diff_pt': round(100.0 * d2, 3), 'n_A': aa, 'n_B': ab}
            if (not same) or pa2 >= 0.05:
                row['gates'].append('判定保留（refuse 転位）')
    sa = None if None in (row['style_a_pt_A'], row['style_a_pt_B']) else abs(row['style_a_pt_A'] - row['style_a_pt_B'])
    sb = None if None in (row['style_b_pt_A'], row['style_b_pt_B']) else abs(row['style_b_pt_A'] - row['style_b_pt_B'])
    row['style_diff_pt'] = None if None in (sa, sb) else round(max(sa, sb), 3)
    if row['style_diff_pt'] is not None and row['style_diff_pt'] > SG['hold_pt']:
        row['gates'].append('判定保留（様式転位）')     # 当たった事実は札に関わらず記録する（裁定 D94）
    if c['A'] in QF_FAIL or c['B'] in QF_FAIL:
        row['gates'].append('判定不能（品質床）')
    # --- 札（正本 gate_order.order の順で最初の一つ・様式門は確証の札にのみ作用する非対称を保つ） ---
    order = ['判定不能（採点欠落）', '判定不能（測れなかった）', '判定不能（検閲）', '判定保留（書式外転位）',
             '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '判定不能（品質床）']
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
    if d > SG['hold_pt']:
        row['label'] = '判定保留（様式転位）'
        row['fired'] = row.get('fired', []) + ['判定保留（様式転位）']
    elif d > SG['note_pt']:
        row['notes'].append('注（様式・差 %.1f pt）' % d)


RES, FAMROWS = {}, []
for famkey, F in T['families'].items():
    rows = [analyse_contrast(famkey, c, 0.05) for c in F['contrasts']]
    # Holm（族ごと・m は減らさない・降格した対比も順位に含める）
    # **降格した対比は順位に含めない**（裁定 D93）。m は登録値のまま減らさない。
    # 降格した対比は順位に含めない（裁定 D93）。ただし**様式門の保留は確証の札にのみ作用する**ので、順位からは外さない（裁定 D94）。
    _hard = lambda r: [g for g in (r.get('fired') or []) if g != '判定保留（様式転位）']
    ordered = sorted([r for r in rows if r.get('p') is not None and not _hard(r)], key=lambda r: r['p'])
    m = F['m']
    passed = True
    for i, r in enumerate(ordered):
        step = 0.05 / (m - i)
        r['holm_alpha'] = step
        r['holm_pass'] = passed and (r['p'] < step)
        passed = r['holm_pass']
    for r in rows:
        if r.get('label') == '確証' and not r.get('holm_pass'):
            r['label'] = '非有意'
        if r.get('label') == '確証' and r.get('style_hold'):
            r['label'] = '判定保留（様式転位）'
        elif r.get('label') == '確証':
            apply_style_gate(r)
        if len(r.get('fired') or []) > 1:
            r['notes'].append('当たった門: ' + '・'.join(r['fired']))
        if r.get('label') == '確証' and SEAL:
            want = (SEAL.get('signs') or {}).get(r['id'])
            r['sealed_sign'] = want
            if want and want != r['sign']:
                r['label'] = '確証（登録された向きと逆）'
                r['notes'].append(PS['label_reverse'].format(A=r['A'], B=r['B'], sign=r['sign'], diff=r['diff_pt'], ci=r['ci']))
    RES[famkey] = rows
    FAMROWS += rows

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
        ci = wald_ci(A['cat'], A['n_ok'], B['cat'], B['n_ok'])
        rows.append({'id': c['id'], 'scenario': c['scenario'], 'A': c['A'], 'B': c['B'],
                     'rate_A': rate(A['cat'], A['n_ok']), 'rate_B': rate(B['cat'], B['n_ok']),
                     'diff_pt': None if ci is None else ci[0], 'ci': None if ci is None else [ci[1], ci[2]],
                     'ff_pt_A': pt(rate(A['ff'], A['n_ok'])), 'ff_pt_B': pt(rate(B['ff'], B['n_ok'])),
                     'refuse_pt_A': pt(rate(A['refuse'], A['n_ok'])), 'refuse_pt_B': pt(rate(B['refuse'], B['n_ok']))})
    DESC[famkey] = rows


def ci_excl_zero_power(p_a, p_b, n, z=1.96):
    k = np.arange(n + 1)
    pa, pb = binom.pmf(k, n, p_a), binom.pmf(k, n, p_b)
    r = k / n
    diff = r[:, None] - r[None, :]
    se = np.sqrt(r[:, None] * (1 - r[:, None]) / n + r[None, :] * (1 - r[None, :]) / n)
    se = np.where(se == 0, np.inf, se)
    w = pa[:, None] * pb[None, :]
    return float(w[(diff + z * se) < 0].sum())


# ---- S4 の反証（三分岐・裁定 D81） ----
S4 = T['descriptive_families']['B_desc_S4']
s4c = S4['contrasts'][0]
s4A, s4B = cell(s4c['scenario'], s4c['A']), cell(s4c['scenario'], s4c['B'])
s4 = {'id': s4c['id']}
if s4A and s4B and s4A['n_ok'] and s4B['n_ok']:
    ci = wald_ci(s4A['cat'], s4A['n_ok'], s4B['cat'], s4B['n_ok'])
    ra4, base_r = rate(s4A['cat'], s4A['n_ok']), rate(s4B['cat'], s4B['n_ok'])
    eff, pmin = S4['three_way']['effect_pt'], S4['three_way']['power_min']
    both_low4 = ra4 < CEN['low'] and base_r < CEN['low']
    both_high4 = ra4 > CEN['high'] and base_r > CEN['high']
    if both_low4 or both_high4:                      # **検閲を先に当てる**（裁定 D95）
        verdict, power = '余地の条項で測れない（%s）' % ('床' if both_low4 else '天井'), None
    elif base_r < eff / 100.0:                       # 低下の余地が無い（率の切り上げをしない・裁定 D95）
        verdict, power = '当否を言わない', None
    else:
        power = ci_excl_zero_power(base_r - eff / 100.0, base_r, s4B['n_ok'])
        if ci[2] < 0:
            verdict = '下がった（封印は外れ）'
        elif ci[1] > 0:
            verdict = '上がった（封印は当たり）'
        elif power >= pmin:
            verdict = '下がらなかった（封印は当たり）'
        else:
            verdict = '当否を言わない'
    s4.update({'diff_pt': ci[0], 'ci': [ci[1], ci[2]], 'rate_A': ra4, 'partner_rate': base_r,
               'power_at_effect': (None if power is None else round(power, 4)),
               'effect_pt': eff, 'power_min': pmin, 'verdict': verdict,
               'sealed_prediction': (SEAL or {}).get('s4') or S4['sealed_prediction']})
else:
    s4['verdict'] = '表に載らない（記録が無い）'

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
                      'diff_pt': wald_ci(A['cat'], A['n_ok'], B['cat'], B['n_ok'])[0], 'n_A': A['n_ok'], 'n_B': B['n_ok']})

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
       'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'gate': (G or {}).get('verdict'),
       'selection': (G or {}).get('selection', {}).get('pick'), 'counts': counts, 'confirm': FAMROWS, 'descriptive': DESC,
       's4': s4, 'stratified': STRAT, 'mention': MENTION, 'direction_ids': sorted(str(x) for x in POOL_IDS if x is not None), 'quality_post': QF_ROWS, 'orphan_arms': orphans, 'missing_cells': missing,
       'sign_agreement': {'agree': agree, 'checked': n_conf, 'unchecked': unchecked, 'seal_missing': SEAL_MISSING, 'sealed': bool(SEAL)}, 'dry_marks': DRY}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

L = ['# 段階 B 本走行の集計（機械生成・`tools/analyze_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 正本 SHA16 %s。選定: %s。門の判定: %s。' % (REC['contrasts_sha16'], REC['selection'], REC['gate']), '',
     '- **%s**' % first]
if SEAL:
    L.append('- ' + PS['sign_agreement'].format(agree=agree, confirmed=n_conf) +
             ('（照合できなかった確証の対比 %s・封印の欠け %d 件）' % (unchecked or 'なし', len(SEAL_MISSING)) if (unchecked or SEAL_MISSING) else ''))
else:
    L.append('- 封印の記録が渡されていないので、予想符号との照合は行っていない（裁定 D79・凍結時に封印する）。')
L += ['- ' + PS['scope'], '- ' + PS['style_move'], '- ' + PS['no_p_desc'], '- ' + PS['selection_direction'],
      '- ' + T['style_gate']['asymmetry'], '- ' + T['fwer_note'], '']
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
      '## S4 の反証（三分岐・裁定 D81・D95）', '', '- 判定: **%s**' % s4.get('verdict')]
if 'partner_rate' in s4:
    L.append('- pt 差 %s・区間 %s・相手の腕の率 %.4f・%d pt の検出力 %s（線は %g）'
             % (s4['diff_pt'], s4['ci'], s4['partner_rate'], s4['effect_pt'],
                ('%.3f' % s4['power_at_effect']) if s4.get('power_at_effect') is not None else '出さない（余地の条項または低下の余地が無い・裁定 D95）',
                s4['power_min']))
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
```

## `tools/integrity_B.py`（SHA16 39910AE25D3ECF6F・208 行）

```python
# -*- coding: utf-8 -*-
"""integrity_B.py v2 —— 段階 B の走行の**整合検査**（率盲検・許可表方式）。

**判定欄（catastrophe・choice・correct・style_a・style_b・mention）は読まない。** 許可した欄だけを取り出し、manifest と正本の登録に突き合わせる。
当てる相（採否表 P230・**本走行の後だけでなく、調整走行と品質床にも当てる**）:
  同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`
検査:
  行数と目標（腕 × n）・n_ok と api_error・書式外の件数（率ではない）・trial_id の重複と trial_index の欠落・腕ごとの n の揃い・
  runner_sha と arms_spec と preamble_sha（正本 `arms.sha16`）・model と seed の登録との一致・生成の設定（`runner.generation`／品質床は `quality_floor.generation`）・
  層と係数が候補の格子にあるか・方向の id の登録・**バッチの大きさの凍結**（`runner.fixed_across_runs`）・**詰めの向き**（`runner.padding`）・
  走行キーとセッション記録の対応（`sessions.missing_rule`）・dry-run の印。
出力: records/B/integrity-<tag>-<日付>.{md,json}（--force が無ければ上書きしない）。不整合があれば非零で終わる。
用法: python tools/integrity_B.py --tag stageB [--root results/_synth/all --allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v2'
REPO = runs_B.REPO
# 許可表は**正本から**作る（裁定 D97・器の中に手書きしない）
_T0 = runs_B.load_T()
ALLOW = tuple(runs_B.field_registry(_T0)['integrity_allow'])
BLIND = tuple(runs_B.field_registry(_T0)['blind'])
ap = argparse.ArgumentParser()
ap.add_argument('--tag', required=True)
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
TAGS = T['tags']
PHASE = next((k for k, v in TAGS.items() if v == a.tag), None)
if PHASE is None:
    sys.exit('tag %s の相が正本 tags に無い' % a.tag)
CAND = {(l, c) for l in T['selection']['candidates']['layers'] for c in T['selection']['candidates']['coefficients']}
ARM_SHA = T['arms']['sha16']
GEN_MAIN, GEN_Q = T['runner']['generation'], T['quality_floor']['generation']
problems, notes, cells = [], [], []
sessions = runs_B.sessions_by_run_key(runs_B.load_sessions(a.root))


def expect_n(phase, manifest):
    return {'identity': T['identity_screen']['n'], 'tune': T['n_tune'], 'quality': T['quality_floor']['items'], 'main': T['n_main']}[phase]


def expect_seed(phase, m):
    S = T['seeds']
    if phase == 'identity':
        return {S['identity_transformers']}
    if phase == 'tune':
        return {S['tune'].get(m.get('scenario'))}
    if phase == 'quality':
        return {S['quality']}
    return {S['main'].get(m.get('scenario'))}


def check_cell(rec):
    m, d = rec['manifest'], rec['dir']
    rk = rec['run_key']
    rows = list(runs_B.iter_jsonl(rec['trials_path'], ALLOW))
    by_arm = collections.defaultdict(list)
    for r in rows:
        by_arm[r['arm']].append(r)
    n_exp = expect_n(PHASE, m)
    seeds_exp = expect_seed(PHASE, m)
    gen_exp = GEN_Q if PHASE == 'quality' else GEN_MAIN
    for arm, rs in sorted(by_arm.items()):
        ids = [r['trial_id'] for r in rs]
        idx = sorted(r['trial_index'] for r in rs)
        n_ok = sum(1 for r in rs if r['status'] == 'ok')
        c = {'run_key': rk, 'arm': arm, 'n': len(rs), 'n_ok': n_ok, 'api_error': len(rs) - n_ok,
             'format_fail': sum(1 for r in rs if r.get('format_fail')), 'loop': sum(1 for r in rs if r.get('loop_flag')),
             'truncated': sum(1 for r in rs if r.get('truncated'))}
        cells.append(c)
        # 行数・番号・重複は**セル単位**で見る（中断と再開で走行が分かれるため・採否表 P264）。ここでは走行の中の重複だけを見る。
        if len(set(ids)) != len(ids):
            problems.append('%s × %s: 走行の中で trial_id が重複（%d 件）' % (rk, arm, len(ids) - len(set(ids))))
        if len(rs) > n_exp:
            problems.append('%s × %s: 行数 %d が目標 %d を超える' % (rk, arm, len(rs), n_exp))
        shas = {r.get('preamble_sha') for r in rs}
        base_arm = arm.split('+v')[0].split('-v')[0]
        want_sha = ARM_SHA.get(base_arm)
        if PHASE in ('main', 'identity', 'tune'):
            if len(shas) != 1:
                problems.append('%s × %s: preamble_sha が一つでない' % (rk, arm))
            elif want_sha and next(iter(shas)) != want_sha:
                problems.append('%s × %s: **preamble_sha が正本 arms.sha16 と違う**（%s 対 %s）' % (rk, arm, next(iter(shas)), want_sha))
        if PHASE == 'quality':
            bad_ff = sum(1 for r in rs if r.get('format_fail') and r.get('correct') is True)
            if bad_ff:
                problems.append('%s × %s: 書式外なのに正答と記録された行が %d 件（正本 quality_floor.format_fail_rule）' % (rk, arm, bad_ff))
        for r in rs:
            if r.get('seed') not in seeds_exp:
                problems.append('%s × %s: seed %s が登録（%s）と違う' % (rk, arm, r.get('seed'), sorted(seeds_exp)))
                break
            if r.get('sampling') and {k: r['sampling'].get(k) for k in ('temperature', 'top_p')} != {k: gen_exp.get(k) for k in ('temperature', 'top_p')}:
                problems.append('%s × %s: 生成の設定が登録と違う（%s）' % (rk, arm, r.get('sampling')))
                break
        if PHASE in ('tune', 'quality'):
            lc = {(r.get('layer'), r.get('coef')) for r in rs}
            for l, cf in lc:
                if l is None and PHASE == 'quality':
                    continue
                if (l, cf) not in CAND:
                    problems.append('%s × %s: 層 × 係数 %s が候補の格子に無い' % (rk, arm, (l, cf)))
        if PHASE == 'main' and arm not in T['arms']['by_scenario'].get(m.get('scenario'), []):
            problems.append('%s: 腕 %s が場面 %s の登録に無い' % (rk, arm, m.get('scenario')))
    MF = T['runner'].get('manifest_fields') or {}
    need = list(MF.get('common', [])) + list(MF.get(PHASE, []))
    lack = [f for f in need if f not in m]
    if lack:
        problems.append('%s: manifest に欄が無い（正本 runner.manifest_fields・裁定 D89）: %s' % (rk, '・'.join(lack)))
    if m.get('batch') and m['batch'] != T['runner']['batch']:
        problems.append('%s: バッチ %s が設計定数（%s）と違う' % (rk, m['batch'], T['runner']['batch']))
    if m.get('padding') and m['padding'] not in ('left',):
        problems.append('%s: 詰めの向きが左でない（正本 runner.padding）: %s' % (rk, m['padding']))
    if PHASE == 'main' and rk not in sessions:
        problems.append('%s: セッション記録が無い（sessions.missing_rule）' % rk)
    if rec['dry_marks']:
        notes.append('%s: dry-run の印（%s）' % (rk, '・'.join(rec['dry_marks'])))


idx = runs_B.index_runs(T, a.tag, a.root, allow_dry=a.allow_dry)
for k, recs in sorted(idx.items(), key=lambda kv: str(kv[0])):
    for rec in recs:
        check_cell(rec)
if not idx:
    problems.append('走行の記録が一つも無い（tag %s）' % a.tag)

# ---- セル単位の検査（中断と再開・採否表 P264）: 走行を跨いで trial_id の重複と欠落を見る ----
cells_by_key = {}
for k, recs in idx.items():
    for rec in recs:
        m = rec['manifest']
        for r in runs_B.iter_jsonl(rec['trials_path'], ALLOW):
            # セルの単位は相ごとに違う（本走行は 場面 × 腕・調整走行は 場面 × 層 × 係数 × 腕・品質床は 段 × 腕 × 層 × 係数 × セッション・選別は スタック × 腕）
            if PHASE == 'main':
                key = (r.get('scenario') or m.get('scenario'), r['arm'])
            elif PHASE == 'tune':
                key = (m.get('scenario'), m.get('layer'), m.get('coef'), r['arm'])
            elif PHASE == 'quality':
                key = (m.get('stage'), r['arm'], m.get('layer'), m.get('coef'), m.get('session'))
            else:
                key = (m.get('stack'), m.get('scenario'), r['arm'])
            c = cells_by_key.setdefault(key, {'ids': [], 'idx': [], 'runs': set(), 'n_ok': 0, 'gap': 0, 'cff': 0})
            c['ids'].append(r['trial_id'])
            c['idx'].append(r['trial_index'])
            c['runs'].add(rec['run_key'])
            if r['status'] == 'ok':
                c['n_ok'] += 1
n_exp_cell = expect_n(PHASE, {})
for key, c in sorted(cells_by_key.items(), key=str):
    if len(set(c['ids'])) != len(c['ids']):
        problems.append('%s × %s: **走行を跨いで trial_id が重複**（%d 件・再開の重複を見落とさない）' % (key[0], key[1], len(c['ids']) - len(set(c['ids']))))
    if sorted(c['idx']) != list(range(n_exp_cell)):
        problems.append('%s × %s: セルの試行の番号が %d 件で連番でない（目標 %d・走行 %s）'
                        % (key[0], key[1], len(c['idx']), n_exp_cell, '・'.join(sorted(c['runs']))))
    if c['n_ok'] == 0:
        problems.append('%s × %s: **n_ok が零**（測れなかったセル・裁定 D96）' % (key[0], key[1]))

# ---- 判定欄を読まないことの自己検査（率盲検・裁定 D97） ----
if set(ALLOW) & set(BLIND):
    problems.append('許可表に判定欄が混ざっている: %s' % '・'.join(sorted(set(ALLOW) & set(BLIND))))

# ---- 走行を跨いだ同一性（runner.fixed_across_runs・採否表 P274） ----
FIX_KEYS = {'重みの rev': 'model_rev', 'tokenizer の版': 'tokenizer_rev', 'transformers の版': 'versions', 'バッチの大きさと並べ方': 'batch'}
seen = {}
for k, recs in idx.items():
    for rec in recs:
        for name, mk in FIX_KEYS.items():
            v = rec['manifest'].get(mk)
            if v is None:
                continue
            seen.setdefault(name, {}).setdefault(json.dumps(v, ensure_ascii=False, sort_keys=True), []).append(rec['run_key'])
for name, vals in seen.items():
    if len(vals) > 1:
        problems.append('**走行を跨いで %s が同じでない**（%s・正本 runner.fixed_rule）' % (name, '／'.join('%s: %d 走行' % (v[:24], len(rs)) for v, rs in vals.items())))

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'integrity-%s-%s.md' % (a.tag, jst.strftime('%Y-%m-%d')))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)
REC = {'kind': 'integrity_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'tag': a.tag, 'phase': PHASE,
       'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'cells': cells, 'problems': problems, 'notes': notes,
       'allow_fields': list(ALLOW)}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 整合検査（機械生成・`tools/integrity_B.py` %s・%s UTC・tag %s・相 %s）' % (VERSION, now.strftime('%Y-%m-%d %H:%M'), a.tag, PHASE), '',
     '- 正本 SHA16 %s。セル %d。**不整合 %d 件**・注 %d 件。' % (REC['contrasts_sha16'], len(cells), len(problems), len(notes)),
     '- 読んだ欄（判定欄は読まない）: %s' % '・'.join(ALLOW), '']
if problems:
    L += ['## 不整合', ''] + ['- ' + p for p in problems] + ['']
if notes:
    L += ['## 注', ''] + ['- ' + n for n in notes] + ['']
L += ['## セル', '', '| 走行キー | 腕 | 行 | n_ok | api_error | 書式外 |', '|---|---|---|---|---|---|']
for c in cells:
    L.append('| %s | %s | %d | %d | %d | %d |' % (c['run_key'], c['arm'], c['n'], c['n_ok'], c['api_error'], c['format_fail']))
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[integrity_B] %s | 不整合 %d・注 %d・セル %d' % (out_md, len(problems), len(notes), len(cells)))
sys.exit(1 if problems else 0)
```
