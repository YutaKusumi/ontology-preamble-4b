# -*- coding: utf-8 -*-
"""integrity_M.py v2 —— 追補 M 走行の整合検査（率盲検・許可表方式）。run-log-M.md の事前拘束（2026-09-10）の器。
v1（2026-09-10・scratchpad・SHA16 は run-log に記帳）は status・trial_id・trial_index・arm・run_key・runner_sha・arms_spec・system・system_sha・時刻のみを読み、
行数・n_ok・api_error・重複・欠落・腕ごと n・runner_sha 単一・arms_spec 一致・system_sha 腕ごと単一を検査した。
v2（2026-09-11・一巡目器材統計票 A2 の条件）は事前拘束が挙げた残り二項を加える: (a) format_fail の件数（書式外＝三つ組の第三項・破局率ではない）・
(b) 盤の SHA 突合（各試行の preamble_sha／system_sha を台帳 arms/panelM/SHA-LEDGER-M.json と突合）。判定欄（catastrophe・choice・refuse_class 等）は読まない。
用法: python tools/integrity_M.py --tag stageM1 [--n 400]  → 標準出力に表・records/M/integrity-<tag>-v2-<date>.md に保全。"""
import os, sys, json, glob, argparse, collections, datetime
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--n', type=int, default=400); a = ap.parse_args()
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8'))
PRE = [x if isinstance(x, str) else x['name'] for x in T['arms']['preamble']]
SYS = [x if isinstance(x, str) else x['name'] for x in T['arms']['system']]
SYSMAP = {x['name']: x for x in T['arms']['system'] if isinstance(x, dict)}
ALLOW = ('status', 'trial_id', 'trial_index', 'arm', 'run_key', 'runner_sha', 'arms_spec', 'system', 'system_sha', 'preamble_sha', 'preamble_src', 'format_fail', 'timestamp', 'timestamp_end')
LED = json.load(open(os.path.join(REPO, 'arms', 'panelM', 'SHA-LEDGER-M.json'), encoding='utf-8'))
LEDV = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8'))  # V′ の盤（参照腕 O-Ncold・Onull-Ncold・Ncold・Nk-Ncold は V′ 凍結素材）


def led_sha(section, key):
    v = LED.get(section, {}).get(key)
    if v is None and section == 'preamble':
        v = LEDV.get(key)
    if isinstance(v, dict):
        return v.get('sha16') or v.get('sha') or next((x for x in v.values() if isinstance(x, str) and len(x) == 16), None)
    return v


out = []; bad = 0


def P(x):
    out.append(x); print(x)


P('# 整合検査 v2 %s（率盲検・許可表方式・%s UTC）' % (a.tag, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')))
P('| run_key | 行数 | 目標 | n_ok | api_error | format_fail | 重複 id | 欠落 index | 腕数 | 腕ごと n 揃い | runner_sha | arms_spec 一致 | system_sha 腕ごと単一 | 盤 SHA 台帳突合 |')
P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for d in sorted(glob.glob(os.path.join(REPO, 'results', a.tag, a.tag + '__*'))):
    key = os.path.basename(d); tf = glob.glob(os.path.join(d, 'trials-*.jsonl'))
    if len(tf) != 1:
        P('| %s | — | | | | | | | | | | | | trials ファイル %d 本 |' % (key, len(tf))); bad += 1; continue
    recs = [{k: v for k, v in json.loads(l).items() if k in ALLOW} for l in open(tf[0], encoding='utf-8') if l.strip()]
    sysrun = bool(recs) and recs[0].get('system') not in (None, 'none')
    arms = SYS if sysrun else PRE; target = len(arms) * a.n
    ids = [r['trial_id'] for r in recs]; dup = len(ids) - len(set(ids))
    idx = sorted(r['trial_index'] for r in recs); missing = (idx[-1] - idx[0] + 1 - len(set(idx))) if idx else 0
    n_ok = sum(1 for r in recs if r.get('status') == 'ok'); err = len(recs) - n_ok; ff = sum(1 for r in recs if r.get('format_fail'))
    per = collections.Counter(r['arm'] for r in recs); even = (set(per) == set(arms)) and all(v == a.n for v in per.values())
    rs = set(r.get('runner_sha') for r in recs); rsha = ','.join(sorted(x or '—' for x in rs))
    aspec = all(r.get('arms_spec') == recs[0].get('arms_spec') for r in recs)
    ss = collections.defaultdict(set); ps = collections.defaultdict(set)
    for r in recs:
        ss[r['arm']].add(r.get('system_sha')); ps[r['arm']].add(r.get('preamble_sha'))
    sys_ok = all(len(v) == 1 for v in ss.values()) and (sysrun or all(v == {None} for v in ss.values()))
    # 盤の SHA 台帳突合
    mism = []
    for arm in per:
        if sysrun:
            spec = SYSMAP.get(arm, {}); exp_sys = led_sha('system', spec.get('system', '').replace('.md', '')) or led_sha('system', spec.get('system', ''))
            got = next(iter(ss[arm]))
            if exp_sys is not None and got is not None and got != exp_sys:
                mism.append('%s system %s≠%s' % (arm, got, exp_sys))
            pre_name = spec.get('prefix'); exp_pre = led_sha('preamble', pre_name) if pre_name else None
            gotp = next(iter(ps[arm]))
            if exp_pre is not None and gotp is not None and gotp != exp_pre:
                mism.append('%s preamble %s≠%s' % (arm, gotp, exp_pre))
        else:
            exp_pre = led_sha('preamble', arm); gotp = next(iter(ps[arm]))
            if arm == 'N':
                if gotp is not None:
                    mism.append('N preamble_sha が None でない')
            elif exp_pre is None:
                mism.append('%s 台帳なし' % arm)
            elif gotp != exp_pre:
                mism.append('%s preamble %s≠%s' % (arm, gotp, exp_pre))
    ledger_ok = not mism
    ok = (len(recs) == target and dup == 0 and missing == 0 and err == 0 and ff == 0 and even and len(rs) == 1 and aspec and sys_ok and ledger_ok)
    if not ok:
        bad += 1
    P('| %s | %d | %d | %d | %d | %d | %d | %d | %d | %s | %s | %s | %s | %s |' % (key, len(recs), target, n_ok, err, ff, dup, missing, len(per), '○' if even else '×', rsha, '○' if aspec else '×', '○' if sys_ok else '×', '○' if ledger_ok else '×: ' + '・'.join(mism[:5])))
P('')
P('判定: %s' % ('全走行 整合' if bad == 0 else '不整合または未完 %d 走行' % bad))
P('本検査は判定欄（catastrophe・choice・refuse_class 等）を読まない（許可表 %s の欄のみ保持）。format_fail は書式外の件数（三つ組の第三項）であり破局率ではない。盤の SHA 突合は各試行の preamble_sha／system_sha を arms/panelM/SHA-LEDGER-M.json（参照腕は V′ の arms/panel/SHA-LEDGER.json・N は前置きなしゆえ None）と比較（台帳に無い腕は不一致として印字）。' % (ALLOW,))
p = os.path.join(REPO, 'records', 'M', 'integrity-%s-v2-%s.md' % (a.tag, datetime.date.today().isoformat()))
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
sys.exit(0 if bad == 0 else 1)
