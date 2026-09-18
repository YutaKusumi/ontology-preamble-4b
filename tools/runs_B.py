# -*- coding: utf-8 -*-
"""runs_B.py v1 —— 段階 B の走行の記録を読む共有の口（段階 A の `runs_A.py` の型・**段階 A の器は触らない**）。

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
VERSION = 'v1'
COUNT_FIELDS = ('trial_id', 'arm', 'status', 'catastrophe', 'choice', 'format_fail', 'style_a', 'style_b', 'mention', 'loop_flag', 'truncated', 'correct')
ZERO = dict(n=0, n_ok=0, api_error=0, cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, loop=0, trunc=0, unmeas=0, correct=0)


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
                             ('dir._dryrun', '_dryrun' in os.path.normpath(d).split(os.sep))) if on]
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
        def key(m):
            if 'stack' in m:                       # 同一性選別
                return (m['stack'], m['scenario'])
            if 'stage' in m:                       # 品質床（段・腕・層・係数。無操作の相手は層と係数が None）
                return (m['stage'], m['arm'], m.get('layer'), m.get('coef'))
            if 'layer' in m:                       # 調整走行（場面 × 層 × 係数・腕は中で分かれる）
                return (m['scenario'], m['layer'], m['coef'])
            return (m['scenario'],)                # 本走行
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
        c['cat'] += (r['catastrophe'] is True)
        c['refuse'] += (r['choice'] == 'refuse')
        c['ff'] += ff
        c['style_a'] += bool(r['style_a'])
        c['style_b'] += bool(r['style_b'])
        c['mention'] += bool(r['mention'])
        c['loop'] += lp
        c['trunc'] += tr
        c['unmeas'] += (ff or lp or tr)
        c['correct'] += (r['correct'] is True)
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
            C[(k[0], arm, k[2], k[3])] = c
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
