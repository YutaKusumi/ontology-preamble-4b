# -*- coding: utf-8 -*-
"""runs_A.py v1 —— 段階 A の走行記録の読み出し（器材共通・2026-09-13・登録者裁定 D9 の手順3）。
走行器 tools/run_preamble_local.py v2.7 の出力（results/<tag>/<tag>__<場面>__none__seed<seed>/ の manifest.json・trials-<機種>.jsonl・raw-<機種>.jsonl）と、
起動器 tools/colab/boot_stageA.py のセッション記録（results/sessions-A/・正本 sessions）を読み、機種の key・場面・腕ごとの件数にまとめる。
集計器・門・校正帯・同一性選別・整合・抽出・応答様式・断片・合成検査が同じ関数を import する（二重実装をしない）。
root は results の代わりの置き場（合成検査は scratchpad などを指す・既定は REPO/results）。
件数の定義: n＝行数・n_ok＝status ok・api_error＝それ以外・cat＝catastrophe が真・refuse＝choice が refuse・ff＝format_fail・loop＝loop_flag・trunc＝truncated・
unmeas＝ff ∪ loop ∪ trunc（和集合・重複は一度・正本 unmeasurable.numerator）。いずれも status ok の行だけを数える（api_error を除く）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, json, glob, hashlib
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json')
VERSION = 'v1'
COUNT_FIELDS = ('trial_id', 'arm', 'status', 'catastrophe', 'choice', 'format_fail', 'loop_flag', 'truncated')


def load_T(path=None):
    return json.load(open(path or CPATH, encoding='utf-8'))


def sha16_file(p):
    """ファイルバイトの SHA-256 先頭 16 桁（CRLF→LF 正規化・strip なし）。"""
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


def results_root(root=None):
    return root or os.path.join(REPO, 'results')


def model_keys(T):
    return {m['id']: m['key'] for m in T['models']}


def model_ids(T):
    return {m['key']: m['id'] for m in T['models']}


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


def index_runs(T, tag, root=None, allow_multi=False):
    """tag の走行を (機種 key, 場面) で引ける辞書にする。値: dir・manifest・run_key・model・scenario・seed・trials_path・raw_path。
    同じ (機種, 場面) が複数あれば、allow_multi なら list にまとめ、そうでなければ停止する。"""
    MK = model_keys(T); out = {}
    for d in run_dirs(tag, root):
        m = read_json(os.path.join(d, 'manifest.json')); key = MK.get(m.get('model'))
        if key is None:
            raise RuntimeError('登録に無い機種: %s（%s）' % (m.get('model'), d))
        rec = {'dir': d, 'manifest': m, 'run_key': os.path.basename(d), 'model': key, 'scenario': m['scenario'], 'seed': m['seed'],
               'trials_path': one_file(d, 'trials'), 'raw_path': one_file(d, 'raw')}
        k = (key, m['scenario'])
        if allow_multi:
            out.setdefault(k, []).append(rec)
        elif k in out:
            raise RuntimeError('同じ機種 × 場面の走行が複数: %s（%s と %s）' % (k, out[k]['dir'], d))
        else:
            out[k] = rec
    return out


def cell_counts(trials_path):
    """腕ごとの件数（モジュールの docstring の定義）。"""
    out = {}
    for r in iter_jsonl(trials_path, COUNT_FIELDS):
        c = out.setdefault(r['arm'], dict(n=0, n_ok=0, api_error=0, cat=0, refuse=0, ff=0, loop=0, trunc=0, unmeas=0))
        c['n'] += 1
        if r['status'] != 'ok':
            c['api_error'] += 1; continue
        ff, lp, tr = bool(r['format_fail']), bool(r['loop_flag']), bool(r['truncated'])
        c['n_ok'] += 1; c['cat'] += (r['catastrophe'] is True); c['refuse'] += (r['choice'] == 'refuse')
        c['ff'] += ff; c['loop'] += lp; c['trunc'] += tr; c['unmeas'] += (ff or lp or tr)
    return out


def counts_by(T, tag, root=None):
    """{(機種 key, 場面, 腕): 件数} と走行の索引（index_runs）を返す。"""
    idx = index_runs(T, tag, root); C = {}
    for (mk, sc), rec in idx.items():
        for arm, c in cell_counts(rec['trials_path']).items():
            C[(mk, sc, arm)] = c
    return C, idx


def decode_calibration_seed(T, seed):
    """校正腕の seed を (持ち主の機種 key, 相〔main／bridge〕, 番号, セッション番号) に解く（seeds.calibration.rule）。"""
    S = T['seeds']['calibration']; num, sess = divmod(seed - S['base'], S['multiplier'])
    keys = {i: m['key'] for i, m in enumerate(T['models'], 1)}; bridge = {v: k for k, v in S['bridge_index'].items()}
    if num in keys:
        owner, phase = keys[num], 'main'
    elif num in bridge:
        owner, phase = bridge[num], 'bridge'
    else:
        raise RuntimeError('校正腕の seed が規則に合わない: %d' % seed)
    if sess < 1:
        raise RuntimeError('校正腕のセッション番号が一始まりでない: %d' % seed)
    return owner, phase, num, sess


def calibration_seed(T, owner, phase, session):
    S = T['seeds']['calibration']; num = S['bridge_index'][owner] if phase == 'bridge' else [m['key'] for m in T['models']].index(owner) + 1
    return S['base'] + S['multiplier'] * num + session


def calibration_runs(T, root=None):
    """校正腕の走行（tags.calibration）を、seed から解いた持ち主・相・セッション番号つきで返す（相・番号・セッションの順）。"""
    out = []
    for recs in index_runs(T, T['tags']['calibration'], root, allow_multi=True).values():
        for r in recs:
            owner, phase, num, sess = decode_calibration_seed(T, r['seed'])
            out.append(dict(r, owner=owner, phase=phase, number=num, session=sess))
    return sorted(out, key=lambda x: (x['phase'] != 'main', x['number'], x['session']))


def load_sessions(root=None):
    """セッション記録（results/sessions-A/*.json）を読む。"""
    return [dict(read_json(p), _path=p) for p in sorted(glob.glob(os.path.join(results_root(root), 'sessions-A', '*.json')))]


def env_by_run_key(sessions):
    """走行キー → 環境値の集合（正本 sessions.env_value_rule・一つの走行キーが複数のセッションにまたがれば和集合）。"""
    out = {}
    for s in sessions:
        for rk in (s.get('run_keys') or []):
            out.setdefault(rk, set()).add(s['env_value'])
    return out


def sessions_by_run_key(sessions):
    """走行キー → そのキーを含むセッション記録の list（正本 sessions.resume_rule）。"""
    out = {}
    for s in sessions:
        for rk in (s.get('run_keys') or []):
            out.setdefault(rk, []).append(s)
    return out
