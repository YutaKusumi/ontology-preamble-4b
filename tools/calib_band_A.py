# -*- coding: utf-8 -*-
"""calib_band_A.py v2 —— 段階 A の校正腕の帯とセッションのやり直し（2026-09-13 整備・登録者裁定 D2・D12 (a)・D24）。
規則は design/contrasts-A.json の calibration（n・band_pass・band_fail・timing・series_rule・consequence）と sessions だけから読み、帯の判定は tools/bands_A.py（格子の転記行 I と同じ関数）。
v2（2026-09-14・実装検分の採否表 P77・P81・P90・P91・登録者裁定 D24）:
- 判定を関数 judge_calibration にまとめ、起動器 tools/colab/boot_stageA.py はそれを import する（session_verdict・claim_first_point・二重実装をしない）。本器の CLI は同じ関数の出力を記録に書く。
- 持ち主の機種・相・セッション番号はセッション記録（calibration_run_key）から引き、seed はその値から規則で組んだ値と突合する（seed から解いて組み直す検査をやめる）。
  セッション記録の無い校正腕は判定しない。CLI はその場合と seed が合わない場合に、記録を書いてから非零で終わる（--allow-missing-sessions は検査用の口）。
- 件数（n_ok）が calibration.n に満たない校正腕は判定しない（n_ok が零は no_data・それ以外は incomplete）。合格にも帯を超えないにも数えず、やり直しの待ちも解かない。初点は件数のそろった本走行の校正腕に限る。
- 合格枝（門0.5 合格）: 各セッションの校正腕（4B-2507 × Ncold × N1・n=calibration_n）を API 既測に対し下側で判定（一標本・超）。
- 不合格枝（門0.5 不合格）: 件数のそろった本走行の校正腕のうち manifest の created が最も早いものを初点（判定しない）とし、ほかのセッション（橋を含む）の校正腕を初点と両側で判定（二標本・超）。
  初点の校正腕の判定の時刻（セッション記録の log の calibration）より前に始まったほかのセッションを逸脱として印字する（登録者裁定 D24・起動器は初点の名乗りで並行を拒む）。
- やり直し（calibration.timing）: 同じ相と持ち主で、帯を超えたセッションの次に判定されたセッションをやり直しとし、やり直しも超えたら器の異常。やり直しの記録が無ければ「やり直し待ち」。
  帯を超えたセッションと件数のそろわないセッションのセッション記録に機種の走行キーがあれば、手順の逸脱として印字する。
- 器の異常のセッションのセッション記録の run_keys を anomaly_run_keys に書く（集計器が確証札に注を付す・機種は降格しない）。
出力: records/A/calib-<tags.calibration>.json と同 .md（既存は --force なしでは上書きしない）。
用法: python tools/calib_band_A.py --identity records/A/identity-screen-A.json [--root <results の代わり>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import bands_A
REPO = runs_A.REPO
VERSION = 'v2.1'   # v2.1（2026-09-14・登録者裁定 D26）: 初点の名乗りの移し替え release_first_point（記録は消さずに退避の名へ移す）
CLAIM = '_first_point_claim.json'
UNJUDGED = ('no_session_record', 'no_data', 'incomplete', 'no_first_point')
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def _ts(v):
    """起動器の時刻（…Z）と manifest の isoformat の両方を datetime に（読めなければ None）。"""
    if not v:
        return None
    try:
        d = datetime.datetime.fromisoformat(str(v).replace('Z', '+00:00'))
        return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return None


def _calib_time(s):
    """セッション記録の log の最初の calibration の時刻（無ければ None）。"""
    return next((e.get('at') for e in ((s or {}).get('log') or []) if e.get('step') == 'calibration'), None)


def judge_calibration(T, branch, root=None, allow_dry=False, need=None):
    """校正腕の全走行を判定する。branch は門0.5 の判定（pass／fail）。need は件数の下限（既定 calibration.n・起動器の DRY だけが小さくする）。"""
    assert branch in ('pass', 'fail'), branch
    CAL = T['calibration']; bb = T['bases_4B2507_api'][CAL['scenario']][CAL['arm']]; BASE = Fraction(bb['k'], bb['n']); NEED = CAL['n'] if need is None else int(need)
    rows = []
    for r in runs_A.calibration_runs_by_session(T, root, allow_dry=allow_dry):
        c = runs_A.cell_counts(r['trials_path']).get(CAL['arm']) or {'cat': 0, 'n_ok': 0, 'n': 0}; s = r['session_rec']
        rows.append({'run_key': r['run_key'], 'phase': r['phase'], 'owner': r['owner'], 'session': r['session'], 'seed': r['seed'], 'expected_seed': r['expected_seed'], 'seed_rule_ok': r['seed_ok'],
                     'k': c['cat'], 'n': c['n_ok'], 'rows': c['n'], 'rate': (c['cat'] / c['n_ok']) if c['n_ok'] else None, 'created': r['manifest'].get('created') or '',
                     'model': r['manifest'].get('model'), 'arms': r['manifest'].get('arms'), 'dry_marks': r.get('dry_marks') or [],
                     'session_record': os.path.basename(s['_path']) if s else None, 'session_run_keys': (s or {}).get('run_keys') or [],
                     'session_started': (s or {}).get('started'), 'session_calibrated': _calib_time(s)})
    for x in rows:
        x['api_diff_pt'] = None if not x['n'] else float((Fraction(x['k'], x['n']) - BASE) * 100)
    MAIN = sorted([x for x in rows if x['session_record'] and x['phase'] == 'main' and x['n'] >= NEED], key=lambda x: (_ts(x['created']) or datetime.datetime.max.replace(tzinfo=datetime.timezone.utc), x['run_key']))
    FIRST = MAIN[0] if (branch == 'fail' and MAIN) else None
    for x in rows:
        if x['session_record'] is None:
            x['fired'] = None; x['judged'] = 'no_session_record'
        elif x['n'] < NEED:
            x['fired'] = None; x['judged'] = 'no_data' if x['n'] == 0 else 'incomplete'
        elif FIRST is not None and x is FIRST:
            x['fired'] = None; x['judged'] = 'first_point'
        elif branch == 'pass':
            x['fired'] = bool(bands_A.below_base(x['k'], x['n'], BASE, CAL['band_pass']['pt'])); x['judged'] = 'band_pass_lower'
        elif FIRST is None:
            x['fired'] = None; x['judged'] = 'no_first_point'
        else:
            x['fired'] = bool(bands_A.over_band(x['k'], x['n'], FIRST['k'], FIRST['n'], CAL['band_fail']['pt'])); x['judged'] = 'band_fail_two_sided'
            x['diff_vs_first_pt'] = float((Fraction(x['k'], x['n']) - Fraction(FIRST['k'], FIRST['n'])) * 100)
    RETRY_WAIT = []; DEVIATIONS = []; ANOM = []; INCOMPLETE = []; groups = {}
    for x in rows:
        if x['session_record'] is not None:
            groups.setdefault((x['phase'], x['owner']), []).append(x)
        else:
            x['role'] = 'unjudged'; x['verdict'] = x['judged']
    for key, g in sorted(groups.items(), key=lambda kv: (kv[0][0] != 'main', str(kv[0][1]))):
        pending = None
        for x in sorted(g, key=lambda y: (y['session'], y['run_key'])):
            if x['judged'] in UNJUDGED:
                x['role'] = 'unjudged'; x['verdict'] = x['judged']
                if x['judged'] in ('no_data', 'incomplete'):
                    INCOMPLETE.append(x['run_key'])
                    if x['session_run_keys']:
                        DEVIATIONS.append({'kind': 'model_runs_after_incomplete_calibration', 'run_key': x['run_key'], 'session_record': x['session_record'], 'run_keys': x['session_run_keys'],
                                           'text': '校正腕の件数がそろわないセッションで機種の走行が記帳されている（起動器の件数の検査の逸脱）'})
                continue
            if pending is not None:
                x['role'] = 'retry'; x['retry_of_session'] = pending['session']; x['verdict'] = 'anomaly' if x['fired'] else 'retry_pass'
                if x['session'] != pending['session'] + 1:
                    x['note'] = 'やり直しのセッション番号が連続していない'
                if x['verdict'] == 'anomaly':
                    ANOM.append(x)
                pending = None
            else:
                x['role'] = 'regular'
                if x['fired']:
                    x['verdict'] = 'fired'; pending = x
                    if x['session_run_keys']:
                        DEVIATIONS.append({'kind': 'model_runs_after_fired', 'run_key': x['run_key'], 'session_record': x['session_record'], 'run_keys': x['session_run_keys'],
                                           'text': '帯を超えたセッションで機種の走行が記帳されている（calibration.timing の逸脱）'})
                else:
                    x['verdict'] = 'first_point' if x['judged'] == 'first_point' else 'pass'
        if pending is not None:
            RETRY_WAIT.append({'phase': key[0], 'owner': key[1], 'session': pending['session'], 'run_key': pending['run_key']})
    if FIRST is not None:
        t_first = _ts(FIRST['session_calibrated']) or _ts(FIRST['created'])
        for x in rows:
            if x is FIRST or x['session_record'] is None or x['session_record'] == FIRST['session_record']:
                continue
            ts = _ts(x['session_started'])
            if ts is not None and t_first is not None and ts < t_first:
                DEVIATIONS.append({'kind': 'started_before_first_point', 'run_key': x['run_key'], 'session_record': x['session_record'], 'started': x['session_started'],
                                   'first_point_calibrated': FIRST['session_calibrated'] or FIRST['created'], 'text': '不合格枝で、初点の校正腕の判定より前にほかのセッションが始まっている（登録者裁定 D24）'})
    ANOM_RK = sorted({rk for x in ANOM for rk in x['session_run_keys']})
    return {'branch': branch, 'need': NEED, 'base_api': [bb['k'], bb['n']], 'band_pass_pt': CAL['band_pass']['pt'], 'band_fail_pt': CAL['band_fail']['pt'],
            'first_point': FIRST and {k: FIRST[k] for k in ('run_key', 'owner', 'session', 'k', 'n', 'rate', 'api_diff_pt', 'created', 'session_record', 'session_calibrated')},
            'sessions': rows, 'retry_waiting': RETRY_WAIT, 'deviations': DEVIATIONS, 'incomplete': INCOMPLETE, 'anomaly_sessions': [x['run_key'] for x in ANOM], 'anomaly_run_keys': ANOM_RK,
            'missing_session_records': [x['run_key'] for x in rows if x['session_record'] is None], 'seed_mismatch': [x['run_key'] for x in rows if x['seed_rule_ok'] is False]}


def session_verdict(T, branch, root, run_key, allow_dry=False, need=None):
    """起動器が使う: 校正腕の走行 run_key の行（verdict・judged・k・n・seed_rule_ok）と全体の判定を返す。"""
    R = judge_calibration(T, branch, root, allow_dry=allow_dry, need=need)
    row = next((x for x in R['sessions'] if x['run_key'] == run_key), None)
    if row is None:
        raise RuntimeError('校正腕の走行 %s が読み出しに無い' % run_key)
    return row, R


def claim_first_point(sdir, who):
    """不合格枝の初点の名乗り（登録者裁定 D24）。who は {'tag','model','session'}。戻り値: (始めてよいか, 既存の名乗り)。
    すでに名乗りがあり、それが同じ tag と機種なら始めてよい（中断の後に次のセッション番号で再開する場合を含む・sessions.number_rule）。名乗りを別の機種へ移すのは登録者の判断で名乗りの記録を退避してから。Drive の同期は原子的でないので、並行のランタイムを同時に起こさない運用を前提にする。"""
    os.makedirs(sdir, exist_ok=True); p = os.path.join(sdir, CLAIM)
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        cur = runs_A.read_json(p)
        return all(cur.get(k) == who.get(k) for k in ('tag', 'model')), cur
    with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(dict(who, claimed=_now()), f, ensure_ascii=False)
    return True, None


def release_first_point(sdir, reason, by):
    """初点の名乗りの移し替え（正本 calibration.claim_release・登録者裁定 D26）。登録者が理由を記帳して判断したときにだけ呼ぶ。
    名乗りの記録を消さずに退避の名（_first_point_claim-released-<時刻>.json）へ移し、理由と判断した人と時刻を書き足す。名乗りが無ければ None を返す。
    退避の後は、別の機種が claim_first_point で名乗れる。並行のランタイムを同時に起こさない運用を前提にする。"""
    p = os.path.join(sdir, CLAIM)
    if not os.path.exists(p):
        return None
    if not (isinstance(reason, str) and reason.strip() and isinstance(by, str) and by.strip()):
        raise ValueError('退避には理由と判断した人の記帳が要る（calibration.claim_release）')
    cur = runs_A.read_json(p); stamp = _now(); dst = os.path.join(sdir, CLAIM.replace('.json', '-released-%s.json' % stamp.replace(':', '')))
    if os.path.exists(dst):
        raise RuntimeError('退避の名が既にある: %s' % dst)
    with open(dst, 'x', encoding='utf-8', newline='\n') as f:
        json.dump(dict(cur, released=stamp, release_reason=reason, released_by=by), f, ensure_ascii=False)
    os.remove(p)
    return dst


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root', default=None); ap.add_argument('--contrasts', default=None); ap.add_argument('--identity', required=True)
    ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true'); ap.add_argument('--allow-dry', action='store_true'); ap.add_argument('--allow-missing-sessions', action='store_true')
    a = ap.parse_args()
    T = runs_A.load_T(a.contrasts); CAL = T['calibration']; tag = T['tags']['calibration']
    OUT = a.out or os.path.join(REPO, 'records', 'A', 'calib-%s' % tag)
    if (os.path.exists(OUT + '.json') or os.path.exists(OUT + '.md')) and not a.force:
        sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUT)
    ID = runs_A.read_json(a.identity)
    if ID.get('kind') != 'identity_screen_A':
        sys.exit('--identity は tools/identity_screen_A.py の出力を渡す')
    R = judge_calibration(T, ID['verdict'], a.root, allow_dry=a.allow_dry)
    DEV = [x for x, on in (('allow_dry', a.allow_dry), ('allow_missing_sessions', a.allow_missing_sessions)) if on] + sorted({m for x in R['sessions'] for m in x['dry_marks']})
    RES = dict({'kind': 'calib_band_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'root': a.root, 'tag': tag, 'dev_marks': DEV,
                'inputs': {'contrasts_sha16': runs_A.sha16_file(a.contrasts or runs_A.CPATH), 'identity_sha16': runs_A.sha16_file(a.identity), 'calib_band_A': runs_A.sha16_file(os.path.abspath(__file__)),
                           'bands_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'bands_A.py')), 'runs_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'runs_A.py'))},
                'gate05_point': {'local_Ncold_N1': (ID.get('local_counts') or {}).get(CAL['arm'])}, 'rules': {'timing': CAL['timing'], 'series_rule': CAL['series_rule'], 'consequence': CAL['consequence']},
                'clause': CLAUSE}, **R)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(RES, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    B = R['branch']; bb = R['base_api']
    M = ['# 段階 A 校正腕の帯（機械生成・`tools/calib_band_A.py` %s・%s UTC）' % (VERSION, RES['generated_utc']), '',
         '- 枝: %s（%s）・API 既測 %d/%d・件数の下限 %d・入力 %s%s' % ('合格枝' if B == 'pass' else '不合格枝', '下側 %s pt・一標本' % R['band_pass_pt'] if B == 'pass' else '初点と両側 %s pt・二標本' % R['band_fail_pt'],
                                                     bb[0], bb[1], R['need'], json.dumps(RES['inputs'], ensure_ascii=False), ('・検査用の印 %s' % ','.join(DEV)) if DEV else ''),
         '- 初点: %s' % (json.dumps(R['first_point'], ensure_ascii=False) if R['first_point'] else ('（合格枝では置かない）' if B == 'pass' else '（未確立）')),
         '- 器の異常: %d セッション（走行キー %d）・やり直し待ち: %d・件数のそろわない校正腕: %d・手順の逸脱: %d・セッション記録の無い校正腕: %d・seed が規則と合わない: %d' % (
             len(R['anomaly_sessions']), len(R['anomaly_run_keys']), len(R['retry_waiting']), len(R['incomplete']), len(R['deviations']), len(R['missing_session_records']), len(R['seed_mismatch'])), '',
         '| 相 | 持ち主 | セッション | seed（規則の値・一致） | 破局/n_ok（行） | 率 | API 既測との差（pt） | 初点との差（pt） | 役割 | 判定 |', '|---|---|---|---|---|---|---|---|---|---|']
    f2 = lambda v, fmt: '—' if v is None else fmt % v
    M += ['| %s | %s | %s | %d（%s・%s） | %d/%d（%d） | %s | %s | %s | %s | %s |' % (x['phase'] or '—', x['owner'] or '—', f2(x['session'], '%d'), x['seed'], f2(x['expected_seed'], '%d'),
                                                                       {True: '合う', False: '合わない', None: '記録なし'}[x['seed_rule_ok']], x['k'], x['n'], x['rows'], f2(x['rate'], '%.4f'),
                                                                       f2(x['api_diff_pt'], '%+.2f'), f2(x.get('diff_vs_first_pt'), '%+.2f'), x.get('role'), x.get('verdict')) for x in R['sessions']]
    M += ['', '- 規則（timing）: %s' % CAL['timing'], '- 規則（series_rule）: %s' % CAL['series_rule']] + ['- 逸脱（%s）: %s（%s）' % (d['kind'], d['text'], d['run_key']) for d in R['deviations']] + ['', CLAUSE]
    open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
    print('[calib_band_A] %s・校正腕 %d・器の異常 %d・やり直し待ち %d・未完 %d・逸脱 %d・記録なし %d・seed 不一致 %d written %s.{json,md}' % (
        B, len(R['sessions']), len(R['anomaly_sessions']), len(R['retry_waiting']), len(R['incomplete']), len(R['deviations']), len(R['missing_session_records']), len(R['seed_mismatch']), OUT))
    if (R['missing_session_records'] and not a.allow_missing_sessions) or R['seed_mismatch']:
        sys.exit('[calib_band_A] セッション記録の無い校正腕 %s・seed が規則と合わない校正腕 %s（記録は書いた・集計の前にそろえる）' % (R['missing_session_records'], R['seed_mismatch']))


if __name__ == '__main__':
    main()
