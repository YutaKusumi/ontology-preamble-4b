# -*- coding: utf-8 -*-
"""calib_band_A.py v1 —— 段階 A の校正腕の帯とセッションのやり直し（2026-09-13・登録者裁定 D2・D12 (a)・D9 の三つ目の手順）。
規則は design/contrasts-A.json の calibration（band_pass・band_fail・timing・series_rule・consequence）と sessions だけから読み、帯の判定は tools/bands_A.py（格子の転記行 I と同じ関数）。
- 合格枝（門0.5 合格）: 各セッションの校正腕（4B-2507 × Ncold × N1・n=calibration_n）を API 既測に対し下側で判定（一標本・超）。
- 不合格枝（門0.5 不合格）: 本走行の最初のセッションの校正腕を初点（判定しない）とし、二つ目以降のセッション（橋を含む）の校正腕を初点と両側で判定（二標本・超）。初点と API 既測の差は記述。
- やり直し（calibration.timing）: 帯を超えたセッションの次のセッション（同じ相と持ち主）をやり直しとし、やり直しも超えたら器の異常。やり直しの記録が無ければ「やり直し待ち」。
  帯を超えたセッションのセッション記録に機種の走行キーがあれば、手順の逸脱（帯を超えたのに機種の走行に進んだ）として印字する。
- 器の異常のセッションのセッション記録の run_keys を anomaly_run_keys に書く（集計器が確証札に注を付す・機種は降格しない）。
順序: 相（本走行→橋）・持ち主の番号・セッション番号。初点は本走行の校正腕のうち manifest の created が最も早いもの。seed が規則（seeds.calibration.rule）と合うかも印字する。
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
VERSION = 'v1'

ap = argparse.ArgumentParser(); ap.add_argument('--root', default=None); ap.add_argument('--contrasts', default=None); ap.add_argument('--identity', required=True)
ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true')
a = ap.parse_args()
T = runs_A.load_T(a.contrasts); CAL = T['calibration']; tag = T['tags']['calibration']
OUT = a.out or os.path.join(REPO, 'records', 'A', 'calib-%s' % tag)
if (os.path.exists(OUT + '.json') or os.path.exists(OUT + '.md')) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUT)
ID = runs_A.read_json(a.identity)
if ID.get('kind') != 'identity_screen_A':
    sys.exit('--identity は tools/identity_screen_A.py の出力を渡す')
BRANCH = ID['verdict']; bb = T['bases_4B2507_api'][CAL['scenario']][CAL['arm']]; BASE = Fraction(bb['k'], bb['n'])
RUNS = runs_A.calibration_runs(T, a.root); SESS = runs_A.load_sessions(a.root)
rows = []
for r in RUNS:
    c = runs_A.cell_counts(r['trials_path']).get(CAL['arm']) or {'cat': 0, 'n_ok': 0}
    sess = next((s for s in SESS if s.get('calibration_run_key') == r['run_key']), None)
    rows.append({'run_key': r['run_key'], 'phase': r['phase'], 'owner': r['owner'], 'session': r['session'], 'seed': r['seed'], 'seed_rule_ok': r['seed'] == runs_A.calibration_seed(T, r['owner'], r['phase'], r['session']),
                 'k': c['cat'], 'n': c['n_ok'], 'rate': (c['cat'] / c['n_ok']) if c['n_ok'] else None, 'created': r['manifest'].get('created') or '', 'model': r['manifest'].get('model'),
                 'arms': r['manifest'].get('arms'), 'session_record': os.path.basename(sess['_path']) if sess else None, 'session_run_keys': (sess or {}).get('run_keys') or []})
MAIN = sorted([x for x in rows if x['phase'] == 'main' and x['n']], key=lambda x: x['created'])
FIRST = MAIN[0] if (BRANCH == 'fail' and MAIN) else None
for x in rows:
    x['api_diff_pt'] = None if x['rate'] is None else float((Fraction(x['k'], x['n']) - BASE) * 100)
    if not x['n']:
        x['fired'] = None; x['judged'] = 'no_data'
    elif FIRST is not None and x is FIRST:
        x['fired'] = None; x['judged'] = 'first_point'
    elif BRANCH == 'pass':
        x['fired'] = bands_A.below_base(x['k'], x['n'], BASE, CAL['band_pass']['pt']); x['judged'] = 'band_pass_lower'
    elif FIRST is None:
        x['fired'] = None; x['judged'] = 'no_first_point'
    else:
        x['fired'] = bands_A.over_band(x['k'], x['n'], FIRST['k'], FIRST['n'], CAL['band_fail']['pt']); x['judged'] = 'band_fail_two_sided'
        x['diff_vs_first_pt'] = float((Fraction(x['k'], x['n']) - Fraction(FIRST['k'], FIRST['n'])) * 100)
RETRY_WAIT = []; DEVIATIONS = []; ANOM = []
groups = {}
for x in rows:
    groups.setdefault((x['phase'], x['owner']), []).append(x)
for key, g in sorted(groups.items(), key=lambda kv: (kv[0][0] != 'main', kv[0][1])):
    pending = None
    for x in sorted(g, key=lambda y: y['session']):
        if pending is not None:
            x['role'] = 'retry'; x['retry_of_session'] = pending['session']
            x['verdict'] = 'no_data' if x['fired'] is None and x['judged'] == 'no_data' else ('anomaly' if x['fired'] else 'retry_pass')
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
                    DEVIATIONS.append({'run_key': x['run_key'], 'session_record': x['session_record'], 'run_keys': x['session_run_keys'], 'text': '帯を超えたセッションで機種の走行が記帳されている（calibration.timing の逸脱）'})
            else:
                x['verdict'] = x['judged'] if x['fired'] is None else 'pass'
    if pending is not None:
        RETRY_WAIT.append({'phase': key[0], 'owner': key[1], 'session': pending['session'], 'run_key': pending['run_key']})
ANOM_RK = sorted({rk for x in ANOM for rk in x['session_run_keys']})
RES = {'kind': 'calib_band_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'root': a.root, 'tag': tag, 'branch': BRANCH,
       'inputs': {'contrasts_sha16': runs_A.sha16_file(a.contrasts or runs_A.CPATH), 'identity_sha16': runs_A.sha16_file(a.identity), 'calib_band_A': runs_A.sha16_file(os.path.abspath(__file__)), 'bands_A': runs_A.sha16_file(os.path.join(REPO, 'tools', 'bands_A.py'))},
       'base_api': [bb['k'], bb['n']], 'band_pass_pt': CAL['band_pass']['pt'], 'band_fail_pt': CAL['band_fail']['pt'], 'first_point': FIRST and {k: FIRST[k] for k in ('run_key', 'k', 'n', 'rate', 'api_diff_pt', 'created')},
       'sessions': rows, 'retry_waiting': RETRY_WAIT, 'deviations': DEVIATIONS, 'anomaly_sessions': [x['run_key'] for x in ANOM], 'anomaly_run_keys': ANOM_RK, 'gate05_point': {'local_Ncold_N1': (ID.get('local_counts') or {}).get(CAL['arm'])},
       'rules': {'timing': CAL['timing'], 'series_rule': CAL['series_rule'], 'consequence': CAL['consequence']},
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(RES, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
M = ['# 段階 A 校正腕の帯（機械生成・`tools/calib_band_A.py` %s・%s UTC）' % (VERSION, RES['generated_utc']), '', '- 枝: %s（%s）・API 既測 %d/%d・入力 %s' % (
     '合格枝' if BRANCH == 'pass' else '不合格枝', '下側 %s pt・一標本' % CAL['band_pass']['pt'] if BRANCH == 'pass' else '初点と両側 %s pt・二標本' % CAL['band_fail']['pt'], bb['k'], bb['n'], json.dumps(RES['inputs'], ensure_ascii=False)),
     '- 初点: %s' % (json.dumps(RES['first_point'], ensure_ascii=False) if FIRST else '（合格枝では置かない）'),
     '- 器の異常: %d セッション（走行キー %d）・やり直し待ち: %d・手順の逸脱: %d' % (len(ANOM), len(ANOM_RK), len(RETRY_WAIT), len(DEVIATIONS)), '',
     '| 相 | 持ち主 | セッション | seed（規則） | 破局/n | 率 | API 既測との差（pt） | 初点との差（pt） | 役割 | 判定 |', '|---|---|---|---|---|---|---|---|---|---|']
M += ['| %s | %s | %d | %d（%s） | %d/%d | %s | %s | %s | %s | %s |' % (x['phase'], x['owner'], x['session'], x['seed'], '合う' if x['seed_rule_ok'] else '合わない', x['k'], x['n'], '—' if x['rate'] is None else '%.4f' % x['rate'],
                                                                   '—' if x['api_diff_pt'] is None else '%+.2f' % x['api_diff_pt'], '%+.2f' % x['diff_vs_first_pt'] if 'diff_vs_first_pt' in x else '—', x.get('role'), x.get('verdict')) for x in rows]
M += ['', '- 規則（timing）: %s' % CAL['timing'], '- 規則（series_rule）: %s' % CAL['series_rule']] + ['- 逸脱: %s（%s）' % (d['text'], d['run_key']) for d in DEVIATIONS] + ['', RES['clause']]
open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[calib_band_A] %s・セッション %d・器の異常 %d・やり直し待ち %d・逸脱 %d written %s.{json,md}' % (BRANCH, len(rows), len(ANOM), len(RETRY_WAIT), len(DEVIATIONS), OUT))
