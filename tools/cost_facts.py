# -*- coding: utf-8 -*-
"""cost_facts.py v1.2 —— 費用パイロット（門0・計画案 v2.2 §5 1″）の実測から §6 の転記行を機械生成する（2026-09-12）。
入力: results/costpilot-*/session.json（boot_cost_pilot.py が書く）と当該 run_dir の trials-*.jsonl・cells.json。ユニットは登録者申告（`--units TAG=before,after[,rate]` で上書き・session.json の units 欄が空なら「申告待ち」と印字）。
出力: records/cost-pilot/cost-facts-<date>.md（転記行 U〔セッション〕・T〔トークン〕・R〔処理量〕・P〔段階 A/B への外挿・仮定つき ◐〕・G〔門0 の判定〕・S〔同一性の下見・記述〕）。
規則: 打ち込んだ数は登録者申告のユニットのみ。外挿の係数は本ファイルに逐語で置き ◐ を付す。率は記述であり確証ではない。
"""
import os, sys, json, glob, argparse, datetime, math, statistics
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--root', default=REPO); ap.add_argument('--out', default=None)
ap.add_argument('--units', action='append', default=[], help='TAG=before,after[,rate_display]（登録者申告・複数可）')
ap.add_argument('--glob', default='results/costpilot-*/session.json')
ap.add_argument('--api-ref', action='append', default=['results/stageVp/stageVp__N1__none__seed41001/cells.json', 'results/stage1/stage1__N1__none__seed31001/cells.json'],
                help='同一性の下見に使う API 既測の cells.json（先に挙げた方を優先）')
a = ap.parse_args()
ROOT = a.root
# ---- 外挿の係数（◐・仮定・本ファイルの逐語）----
SIZE_FACTOR = {'0.6B': 0.25, '1.7B': 0.5, '4B': 1.0, '8B': 2.0, '14B': 3.5, '32B': None}   # 4B 比の試行時間の仮定（パラメータ比より緩い・小型機種は出力長で下限がある・32B は A100 40GB bf16 に載らない）
A_TRIALS_PER_SIZE = 98000 / 6        # 計画案 v2.2 §4-A 規模 ≈98,000 を 6 機種で等分（◐）
B_TRIALS = 6000                       # B-4B（選別 n=80 × 腕・調整走行・本走行）の試行数の仮定（◐・§4-B に数の記載なし）
SESSION_HOURS = 8.0                   # 一セッションの上限の仮定（◐・Pro の背景実行なし）
BOUND_A, BOUND_B, BAND_UPPER = 250, 100, 400   # §6 の表の値（A ≈250・B-4B ≈100）と較正メモの帯の上限（A＋B ≈150〜400）
Z = 1.959963985


def wilson(k, n):
    if not n:
        return None
    p = k / n; dd = 1 + Z * Z / n; c = (p + Z * Z / (2 * n)) / dd; h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / dd
    return (round(c - h, 3), round(c + h, 3))


def pct(x, d=1):
    return '—' if x is None else ('%.*f' % (d, x))


units_cli = {}
for u in a.units:
    t, v = u.split('=', 1); parts = [x.strip() for x in v.split(',')]
    units_cli[t] = dict(before=float(parts[0]), after=float(parts[1]), rate_display=(float(parts[2]) if len(parts) > 2 else None))
sessions = []
for sp in sorted(glob.glob(os.path.join(ROOT, a.glob))):
    S = json.load(open(sp, encoding='utf-8')); rd = os.path.join(ROOT, S['run_dir'])
    tf = glob.glob(os.path.join(rd, 'trials-*.jsonl')); cf = os.path.join(rd, 'cells.json')
    rows = [json.loads(l) for l in open(tf[0], encoding='utf-8') if l.strip()] if tf else []
    cells = json.load(open(cf, encoding='utf-8')) if os.path.isfile(cf) else None
    ok = [r for r in rows if r.get('status') == 'ok']
    gen = sorted(r.get('gen_tokens') or 0 for r in ok); pt = sorted(r.get('prompt_tokens') or 0 for r in ok); sec = sorted(r.get('seconds') or 0 for r in ok)
    q = lambda xs, p: (xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None)
    tl = S.get('timeline_s', {}); main_s = next((x.get('seconds') for x in S.get('log', []) if x.get('k') == 'main'), None)
    # v1.2: boot v2 は再実行・二段で runs を持つ。経費の各区間は runs 全体の最大（導入・取得・起動は初回にしか起きない）、壁時計は最初の run の開始から最後の run の終了まで
    runs = S.get('runs') or [dict(started=S.get('date_utc'), timeline_s=tl)]
    def _iv(t, a, b):
        return max(0.0, (t.get(b) or 0) - (t.get(a) or 0)) if (t.get(b) is not None and t.get(a) is not None) else 0.0
    iv = {k: max(_iv(r.get('timeline_s', {}), a, b) for r in runs) for k, (a, b) in {'pip': ('gpu', 'pip'), 'download': ('clone', 'download'), 'server': ('download', 'server_ready')}.items()}
    setup_s = iv['pip'] + iv['download'] + iv['server'] + max(_iv(r.get('timeline_s', {}), 'pip', 'clone') for r in runs)
    import datetime as _dt
    def _p(x):
        try:
            return _dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
        except Exception:
            return None
    _st = [(_p(r.get('started')), max([0.0] + [float(v) for v in (r.get('timeline_s') or {}).values()])) for r in runs]
    _st = [(a, b) for a, b in _st if a]
    wall_session_h = ((max(a + _dt.timedelta(seconds=b) for a, b in _st) - min(a for a, _ in _st)).total_seconds() / 3600) if _st else None
    u = units_cli.get(S['tag']) or {k: (float(v) if v not in (None, '') else None) for k, v in (S.get('units') or {}).items() if k in ('before', 'after', 'rate_display')}
    used = (u['before'] - u['after']) if (u.get('before') is not None and u.get('after') is not None) else None
    wall_h = wall_session_h if wall_session_h else (S.get('wall_total_s') or 0) / 3600
    sessions.append(dict(S=S, rows=rows, ok=ok, cells=cells, gen=gen, pt=pt, sec=sec, q=q, main_s=main_s, setup_s=setup_s, iv=iv, u=u, used=used, wall_h=wall_h,
                         trials=len(rows), n_err=sum(1 for r in rows if r.get('status') == 'api_error'), n_trunc=sum(1 for r in ok if r.get('truncated')),
                         n_fail=sum(1 for r in ok if r.get('format_fail')), n_loop=sum(1 for r in ok if r.get('loop_flag')),
                         tph=(len(rows) / (main_s / 3600) if main_s else None),
                         upt=((used / wall_h) if (used is not None and wall_h) else None),   # 消費ユニット／壁時計（経費込みの実測の時間あたり）
                         u_per_1k=((used / len(rows) * 1000) if (used is not None and rows) else None)))   # 経費込み
if not sessions:
    sys.exit('session.json が見つからない: %s' % a.glob)
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
O = ['# 費用パイロット（門0）の実測と転記行（機械生成・`tools/cost_facts.py` v1.2・%s UTC）' % now, '',
     '- 入力: ' + '・'.join('`%s`' % os.path.relpath(os.path.join(ROOT, s['S']['run_dir']), ROOT).replace('\\', '/') for s in sessions) + '。ユニットの数は登録者申告（器は測れない）。外挿の係数は ◐（仮定・本器の逐語）。率は記述であり確証ではない。', '',
     '## U. セッション（環境と経費）', '', '| tag | GPU | vLLM／torch | 重み rev | 取得 GiB | 導入 s | 取得 s | 起動待ち s | 経費合計 s（各区間の runs 最大の和） | 本走行 s | 壁時計 h（最初の run 開始〜最後の run 終了） | HEAD | 走行器 |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for s in sessions:
    S = s['S']; tl = S.get('timeline_s', {}); v = S.get('versions') or {}
    O.append('| %s | %s | %s／%s | %s | %s | %s | %s | %s | %s | %s | %.2f | %s | %s |' % (
        S['tag'], S.get('gpu', '').split(',')[0], v.get('vllm'), v.get('torch'), (S.get('model_rev') or '')[:12], pct((S.get('model_bytes') or 0) / 2**30, 2),
        pct(s['iv']['pip'], 0), pct(s['iv']['download'], 0), pct(s['iv']['server'], 0),
        pct(s['setup_s'], 0), pct(s['main_s'], 0), s['wall_h'], (S.get('repo_head') or '')[:12], S.get('runner_sha16')))
O += ['', '## T. トークン長と応答の状態（本走行・腕をまとめて）', '', '| tag | 試行 | api_error | 書式外 | 切り詰め | ループ | prompt tok 中央値 | 出力 tok 中央値／p90／最大 | 試行秒 中央値／p90 |', '|---|---|---|---|---|---|---|---|---|']
for s in sessions:
    q = s['q']
    O.append('| %s | %d | %d | %d | %d | %d | %s | %s／%s／%s | %s／%s |' % (s['S']['tag'], s['trials'], s['n_err'], s['n_fail'], s['n_trunc'], s['n_loop'], q(s['pt'], 0.5), q(s['gen'], 0.5), q(s['gen'], 0.9), (s['gen'][-1] if s['gen'] else None), q(s['sec'], 0.5), q(s['sec'], 0.9)))
O += ['', '## R. 処理量とユニット（登録者申告）', '', '| tag | workers | 試行／時（本走行） | ユニット before→after（申告） | 消費ユニット | 表示の時間あたりユニット（申告） | 実測の時間あたりユニット（消費／壁時計・経費込み） | ユニット／1,000 試行（経費込み） | 経費の割合（経費／〔経費＋本走行〕） |', '|---|---|---|---|---|---|---|---|---|']
for s in sessions:
    u = s['u']; ov = (s['setup_s'] / (s['setup_s'] + s['main_s'])) if (s['setup_s'] and s['main_s']) else None
    O.append('| %s | %s | %s | %s→%s | %s | %s | %s | %s | %s |' % (s['S']['tag'], s['S']['cfg'].get('workers'), pct(s['tph'], 0), pct(u.get('before'), 2), pct(u.get('after'), 2), pct(s['used'], 2) if s['used'] is not None else '申告待ち',
                                                              pct(u.get('rate_display'), 2), pct(s['upt'], 2), pct(s['u_per_1k'], 2), pct(ov, 2)))
O += ['', '## P. 段階 A／B-4B への外挿（◐・仮定つき・§6 の置換候補）', '',
      '係数（仮定・本器の逐語）: 4B 比の試行時間 %s。A の試行数 ≈98,000 を 6 機種で等分（%.0f／機種）。B-4B の試行数 %d（§4-B に数の記載なし・仮定）。一セッション %.0f 時間で経費（導入・取得・起動）が毎回かかると仮定。32B は A100 40GB bf16 に載らないため外挿から外す（別環境・時間貸し）。' % (
          json.dumps(SIZE_FACTOR, ensure_ascii=False), A_TRIALS_PER_SIZE, B_TRIALS, SESSION_HOURS), '',
      '| tag | 4B 換算の A 試行時間 h（5 機種・32B 除く） | セッション数（経費込み） | A の見込みユニット | B-4B の見込みユニット | A＋B | §6 の値（A %d・B %d・帯の上限 %d） |' % (BOUND_A, BOUND_B, BAND_UPPER), '|---|---|---|---|---|---|---|']
verdict = []
for s in sessions:
    if not s['tph']:
        O.append('| %s | —（本走行の時間なし） | — | — | — | — | — |' % s['S']['tag']); continue
    hours_A = sum(A_TRIALS_PER_SIZE * f / s['tph'] for f in SIZE_FACTOR.values() if f)
    setup_h = (s['setup_s'] or 0) / 3600; n_sess = math.ceil(hours_A / max(SESSION_HOURS - setup_h, 1)); hours_A_total = hours_A + n_sess * setup_h
    hours_B = B_TRIALS / s['tph']; n_sess_B = math.ceil(hours_B / max(SESSION_HOURS - setup_h, 1)); hours_B_total = hours_B + n_sess_B * setup_h
    rate = s['u'].get('rate_display') or s['upt']   # 表示の時間あたりユニット（申告）を優先・無ければ消費／壁時計
    uA = hours_A_total * rate if rate else None; uB = hours_B_total * rate if rate else None
    O.append('| %s | %.1f（経費込み %.1f） | %d | %s | %s | %s | A %d・B %d・上限 %d |' % (s['S']['tag'], hours_A, hours_A_total, n_sess, pct(uA, 0), pct(uB, 0), pct((uA + uB) if (uA is not None and uB is not None) else None, 0), BOUND_A, BOUND_B, BAND_UPPER))
    if uA is not None and uB is not None:
        tot = uA + uB
        verdict.append((s['S']['tag'], tot, '帯の上限 %d を超える → §5 1″ の代替（単一 API 事業者）を登録者裁定に上げる' % BAND_UPPER if tot > BAND_UPPER else
                        ('§6 の表の値（%d）を超え帯の内側 → 続行・§6 を本転記行で置換し注を付す' % (BOUND_A + BOUND_B) if tot > BOUND_A + BOUND_B else '§6 の表の値の内側 → 続行・§6 を本転記行で置換')))
    else:
        verdict.append((s['S']['tag'], None, 'ユニットの申告待ち（判定不能）'))
O += ['', '## G. 門0 の判定（事前登録の決定木・`records/cost-pilot/cost-pilot-plan-2026-09-12.md` §4）', '']
for t, tot, v in verdict:
    O.append('- %s: A＋B 見込み %s ユニット → %s' % (t, pct(tot, 0), v))
O += ['', '判定は GPU ごとに出す。二セッションの判定が食い違う場合は、安い側の GPU を A の主環境とし、高い側を橋のセルに限る（§3 の二環境の規則・登録者裁定）。', '']
# ---- S. 同一性の下見（記述）----
refs = {}
for rp in a.api_ref:
    p = os.path.join(ROOT, rp)
    if os.path.isfile(p):
        d = json.load(open(p, encoding='utf-8'))
        for arm, c in d['cells'].items():
            refs.setdefault(arm, (c, rp, d['manifest'].get('n_per_arm')))
O += ['## S. API 既測との同一性の下見（記述・n=40・B の選別〔n=80・三セルの距離〕ではない・確証に用いない）', '',
      '| tag | 腕 | 手元 破局 k/n（Wilson） | API 既測 破局 k/n（Wilson・出所） | 差 pt | 手元 refuse／書式外 | API refuse／書式外 |', '|---|---|---|---|---|---|---|']
for s in sessions:
    if not s['cells']:
        continue
    for arm in s['S']['cfg']['arms'].split(','):
        c = s['cells']['cells'].get(arm)
        if not c:
            continue
        k, n = c.get('catastrophe') or 0, c.get('catastrophe_n_all') or c.get('n', 0); r = refs.get(arm)
        loc = '%d/%d（%s）' % (k, n, wilson(k, n)) if n else '—'
        if r:
            rc, rp, rn = r; rk, rnn = rc.get('catastrophe') or 0, rc.get('catastrophe_n_all') or rc.get('n', 0)
            api = '%d/%d（%s・%s）' % (rk, rnn, wilson(rk, rnn), rp.split('/')[1]); diff = pct((k / n - rk / rnn) * 100, 1) if (n and rnn) else '—'
            api_rf = '%s／%s' % (rc.get('refuse'), rc.get('format_fail'))
        else:
            api, diff, api_rf = '既測なし（API で未走行の腕）', '—', '—'
        O.append('| %s | %s | %s | %s | %s | %s／%s | %s |' % (s['S']['tag'], arm, loc, api, diff, c.get('refuse'), c.get('format_fail'), api_rf))
O += ['', '- 読み: 差は「同一でないことは検出されなかった」の予備の目安に留まる。B の前提（同素材・同場面 × n=80・平均絶対差 ≤5pt かつ最大絶対差 ≤12pt・Freeman–Halton）は別に走らせる。Odose1・Odosehalf は API 既測がない（V′ の盤の未使用腕）。', '',
      '## 打ち込んだ数の一覧', '', '- 登録者申告のユニット（before／after／表示の時間あたりユニット）のみ。ほかは session.json・trials・cells からの機械取得。外挿の係数は ◐ の仮定。', '',
      '柵: 本ファイルのいかなる率も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。機種を安全性で順位づけしない。']
out = a.out or os.path.join(ROOT, 'records', 'cost-pilot', 'cost-facts-%s.md' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'))
os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(O) + '\n')
print('[cost_facts] →', out, '| sessions', [s['S']['tag'] for s in sessions], '| verdicts', [(t, pct(tot, 0)) for t, tot, _ in verdict])
