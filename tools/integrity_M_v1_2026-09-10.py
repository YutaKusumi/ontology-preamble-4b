# -*- coding: utf-8 -*-
"""integrity_M.py —— 追補 M 走行の整合検査（率を読まない実装・run-log-M.md の事前拘束 2026-09-10）。
読むのは trials-*.jsonl の status・trial_id・arm・run_key・manifest の不一致検査キーのみ。raw の判定欄・cells.json の率は開かない。
用法: python integrity_M.py --tag stageM1  → 標準出力に表・records/M/integrity-<tag>-<date>.md に保全（呼び出し側で保存）。"""
import os, sys, json, glob, argparse, collections, hashlib, datetime
REPO = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--n', type=int, default=400); a = ap.parse_args()
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8'))
PRE = [x if isinstance(x, str) else x['name'] for x in T['arms']['preamble']]
SYS = [x if isinstance(x, str) else x['name'] for x in T['arms']['system']]
ALLOW = ('status', 'trial_id', 'trial_index', 'arm', 'run_key', 'runner_sha', 'arms_spec', 'system', 'system_sha', 'timestamp', 'timestamp_end')  # 許可表方式: 判定欄（catastrophe・choice・refuse_class・format_fail 等）は読み込まない
out = []; bad = 0
def P(x):
    out.append(x); print(x)
P('# 整合検査 %s（率を読まない・%s UTC）' % (a.tag, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')))
P('| run_key | 行数 | 目標 | n_ok | api_error | 重複 id | 欠落 index | 腕数 | 腕ごと n 揃い | runner_sha | arms_spec 一致 | system_arm_sha 一致 |')
P('|---|---|---|---|---|---|---|---|---|---|---|---|')
for d in sorted(glob.glob(os.path.join(REPO, 'results', a.tag, a.tag + '__*'))):
    key = os.path.basename(d); tf = glob.glob(os.path.join(d, 'trials-*.jsonl'))
    if not tf:
        P('| %s | — | | | | | | | | | | 未着手 |' % key); bad += 1; continue
    recs = []
    for l in open(tf[0], encoding='utf-8'):
        if not l.strip(): continue
        r = json.loads(l)
        # 許可表の欄だけを保持する（実装上の盲検・判定欄は落とす）
        recs.append({k: v for k, v in r.items() if k in ALLOW})
    sysrun = recs and recs[0].get('system') not in (None, 'none')
    arms = SYS if sysrun else PRE; target = len(arms) * a.n
    ids = [r['trial_id'] for r in recs]; dup = len(ids) - len(set(ids))
    idx = sorted(r['trial_index'] for r in recs); missing = (idx[-1] - idx[0] + 1 - len(set(idx))) if idx else 0
    n_ok = sum(1 for r in recs if r.get('status') == 'ok'); err = len(recs) - n_ok
    per = collections.Counter(r['arm'] for r in recs); even = (set(per) == set(arms)) and all(v == a.n for v in per.values())
    mf = glob.glob(os.path.join(d, 'manifest*.json')); m = json.load(open(mf[0], encoding='utf-8')) if mf else {}
    rs = set(r.get('runner_sha') for r in recs); rsha = ','.join(sorted(x or '—' for x in rs))
    aspec = all(r.get('arms_spec') == recs[0].get('arms_spec') for r in recs)
    if sysrun:
        led = json.load(open(os.path.join(REPO, 'arms', 'panelM', 'SHA-LEDGER-M.json'), encoding='utf-8'))
        led_sys = {k: v for k, v in led.items()}
        ss = collections.defaultdict(set)
        for r in recs: ss[r['arm']].add(r.get('system_sha'))
        sys_ok = all(len(v) == 1 for v in ss.values())
    else:
        sys_ok = all(r.get('system_sha') is None for r in recs)
    ok = (len(recs) == target and dup == 0 and missing == 0 and err == 0 and even and len(rs) == 1 and aspec and sys_ok)
    if not ok: bad += 1
    P('| %s | %d | %d | %d | %d | %d | %d | %d | %s | %s | %s | %s |' % (key, len(recs), target, n_ok, err, dup, missing, len(per), '○' if even else '×', rsha, '○' if aspec else '×', '○' if sys_ok else '×'))
P('')
P('判定: %s' % ('全走行 整合' if bad == 0 else '不整合または未完 %d 走行' % bad))
P('本検査は判定欄を読まない（許可表 %s の欄のみ保持）。' % (ALLOW,))
open(os.path.join(REPO, 'records', 'M', 'integrity-%s-%s.md' % (a.tag, datetime.date.today().isoformat())), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
sys.exit(0 if bad == 0 else 1)
