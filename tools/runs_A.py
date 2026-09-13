# -*- coding: utf-8 -*-
"""runs_A.py v1.1 —— 段階 A の走行記録の読み出し（器材共通・2026-09-13・登録者裁定 D9 の手順3）。
走行器 tools/run_preamble_local.py v2.7 の出力（results/<tag>/<tag>__<場面>__none__seed<seed>/ の manifest.json・trials-<機種>.jsonl・raw-<機種>.jsonl）と、
起動器 tools/colab/boot_stageA.py のセッション記録（results/sessions-A/・正本 sessions）を読み、機種の key・場面・腕ごとの件数にまとめる。
v1.1（2026-09-14・実装検分の採否表 P75・P78・P90）: dry-run の走行の印（dry_marks）と読み出しでの拒否（allow_dry は検査用の口）・校正腕の持ち主と相とセッション番号をセッション記録から引く関数（calibration_runs_by_session）・重みの版を完全な SHA に解く関数（registered_rev・resolve_rev）を置く。
集計器・門・校正帯・同一性選別・整合・抽出・応答様式・断片・合成検査が同じ関数を import する（二重実装をしない）。
root は results の代わりの置き場（合成検査は scratchpad などを指す・既定は REPO/results）。
件数の定義: n＝行数・n_ok＝status ok・api_error＝それ以外・cat＝catastrophe が真・refuse＝choice が refuse・ff＝format_fail・loop＝loop_flag・trunc＝truncated・
unmeas＝ff ∪ loop ∪ trunc（和集合・重複は一度・正本 unmeasurable.numerator）。いずれも status ok の行だけを数える（api_error を除く）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, json, glob, hashlib
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json')
VERSION = 'v1.1'
HEX40 = re.compile(r'[0-9a-f]{40}')
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


def dry_marks(d, m, trials_path):
    """dry-run の走行の印（manifest の dry_model_rewritten・model が stub/dry-run・置き場が _dryrun・行の dry_run）。空の list なら印なし（採否表 P78）。"""
    marks = [x for x, on in (('manifest.dry_model_rewritten', bool(m.get('dry_model_rewritten'))), ('manifest.model', m.get('model') == 'stub/dry-run'),
                             ('dir._dryrun', '_dryrun' in os.path.normpath(d).split(os.sep))) if on]
    first = next(iter_jsonl(trials_path, ('dry_run',)), None)
    if first is not None and first.get('dry_run'):
        marks.append('trials.dry_run')
    return marks


def index_runs(T, tag, root=None, allow_multi=False, allow_dry=False):
    """tag の走行を (機種 key, 場面) で引ける辞書にする。値: dir・manifest・run_key・model・scenario・seed・trials_path・raw_path・dry_marks。
    同じ (機種, 場面) が複数あれば、allow_multi なら list にまとめ、そうでなければ停止する。
    dry-run の走行（dry_marks）があれば止まる（allow_dry は検査用の口・呼び手が検査用の印を付ける・採否表 P78）。"""
    MK = model_keys(T); out = {}
    for d in run_dirs(tag, root):
        m = read_json(os.path.join(d, 'manifest.json')); tp = one_file(d, 'trials'); dm = dry_marks(d, m, tp)
        if dm and not allow_dry:
            raise RuntimeError('dry-run の走行は読まない: %s（印 %s・検査用の口だけが通す）' % (d, '・'.join(dm)))
        key = MK.get(m.get('model'))
        if key is None:
            raise RuntimeError('登録に無い機種: %s（%s）' % (m.get('model'), d))
        rec = {'dir': d, 'manifest': m, 'run_key': os.path.basename(d), 'model': key, 'scenario': m['scenario'], 'seed': m['seed'],
               'trials_path': tp, 'raw_path': one_file(d, 'raw'), 'dry_marks': dm}
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


def counts_by(T, tag, root=None, allow_dry=False):
    """{(機種 key, 場面, 腕): 件数} と走行の索引（index_runs）を返す。"""
    idx = index_runs(T, tag, root, allow_dry=allow_dry); C = {}
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


def calibration_runs(T, root=None, allow_dry=False):
    """校正腕の走行（tags.calibration）を、seed から解いた持ち主・相・セッション番号つきで返す（相・番号・セッションの順）。"""
    out = []
    for recs in index_runs(T, T['tags']['calibration'], root, allow_multi=True, allow_dry=allow_dry).values():
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


def calibration_runs_by_session(T, root=None, allow_dry=False):
    """校正腕の走行に、持ち主の機種・相・セッション番号をセッション記録（calibration_run_key）から引いて付け、seed をその値から規則（seeds.calibration.rule）で組んだ値と突合する
    （seed から解いて組み直す検査はしない・採否表 P90）。セッション記録の無い走行は session_rec が None。同じ走行を二つ以上のセッション記録が指せば止まる。"""
    SESS = load_sessions(root); out = []
    for recs in index_runs(T, T['tags']['calibration'], root, allow_multi=True, allow_dry=allow_dry).values():
        for r in recs:
            ss = [s for s in SESS if s.get('calibration_run_key') == r['run_key']]
            if len(ss) > 1:
                raise RuntimeError('校正腕の走行 %s を指すセッション記録が複数: %s' % (r['run_key'], [os.path.basename(s['_path']) for s in ss]))
            s = ss[0] if ss else None
            if s is None:
                out.append(dict(r, session_rec=None, owner=None, phase=None, session=None, expected_seed=None, seed_ok=None))
                continue
            if s.get('phase') not in ('main', 'bridge'):
                raise RuntimeError('校正腕を指すセッション記録の相が main／bridge でない: %s（%s）' % (s.get('phase'), os.path.basename(s['_path'])))
            exp = calibration_seed(T, s['model'], s['phase'], int(s['session']))
            out.append(dict(r, session_rec=s, owner=s['model'], phase=s['phase'], session=int(s['session']), expected_seed=exp, seed_ok=(r['seed'] == exp)))
    return sorted(out, key=lambda x: (x['phase'] is None, x['phase'] != 'main', str(x['owner']), x['session'] or 0, x['run_key']))


def registered_rev(HF, T, mk):
    """records/A/hf-models-A.json の models[機種] の id と登録の版（接頭辞）。id が正本の models と違えば止まる。"""
    rec = (HF.get('models') or {}).get(mk)
    if not isinstance(rec, dict) or not rec.get('rev') or rec.get('id') != model_ids(T).get(mk):
        raise RuntimeError('records/A/hf-models-A.json に機種 %s の登録の版が無い（または id が正本と違う）' % mk)
    return rec['id'], rec['rev']


def resolve_rev(HF, T, mk, api=None):
    """登録の版（接頭辞）を公開 API で完全な SHA に解き、40 桁の小文字の十六進で接頭辞と一致することを確かめる（採否表 P75）。
    api は model_info(repo_id, revision=...) を持つもの（既定は huggingface_hub.HfApi()・資格情報は使わない）。解けなければ RuntimeError。"""
    rid, prefix = registered_rev(HF, T, mk)
    if api is None:
        from huggingface_hub import HfApi
        api = HfApi()
    full = getattr(api.model_info(rid, revision=prefix), 'sha', None)
    if not (isinstance(full, str) and HEX40.fullmatch(full) and full.startswith(prefix)):
        raise RuntimeError('登録の版 %s（%s）を完全な SHA に解けない: %r' % (prefix, rid, full))
    return {'id': rid, 'registered': prefix, 'full': full}
