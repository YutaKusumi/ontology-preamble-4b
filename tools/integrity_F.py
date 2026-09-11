# -*- coding: utf-8 -*-
"""integrity_F.py v1 —— 段階 F 走行の整合検査（率盲検・許可表方式）。run-log-F.md の事前拘束の器。**第一走行の起動前に公開し SHA16 を run-log に記帳する**（反映メモ M §5-1）。
許可表（ALLOW）の欄のみを読み、行数・n_ok・api_error・format_fail（書式外の件数・三つ組の第三項・破局率ではない）・trial_id の重複・trial_index の欠落・腕ごと n・runner_sha 単一・arms_spec 一致・
system_sha が全試行 None（本段は system 型を置かない）・盤の SHA 突合（preamble_sha を arms/panelF/SHA-LEDGER-F.json、U-Ncold・U-O-Ncold は V′ の arms/panel/SHA-LEDGER.json と突合・腕名 N は前置きなしゆえ None を期待〔台帳外の既知腕として先に例外登録〕）を検査する。
判定欄（catastrophe・choice・refuse_class・raw 等）は読まない。出力に本器の SHA16 を印字する。
用法: python tools/integrity_F.py --tag stageF1 [--n 400]  → 標準出力に表・records/F/integrity-<tag>-<date>.md に保全。"""
import os, sys, json, glob, argparse, collections, datetime, hashlib
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF_SHA = hashlib.sha256(open(__file__, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--n', type=int, default=400); ap.add_argument('--root', default=None); a = ap.parse_args()
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8'))
PRE = list(T['arms']['preamble'])
ALLOW = ('status', 'trial_id', 'trial_index', 'arm', 'run_key', 'runner_sha', 'arms_spec', 'system', 'system_sha', 'preamble_sha', 'preamble_src', 'format_fail', 'timestamp', 'timestamp_end')
KNOWN_NO_LEDGER = {'N': None}   # 前置きなし・期待値 None（M の sysO／sysOnull の先例の再発防止＝先に例外登録）
LEDF = json.load(open(os.path.join(REPO, 'arms', 'panelF', 'SHA-LEDGER-F.json'), encoding='utf-8')).get('preamble', {})
LEDV = json.load(open(os.path.join(REPO, 'arms', 'panel', 'SHA-LEDGER.json'), encoding='utf-8'))


def led_sha(key):
    v = LEDF.get(key)
    if v is None:
        v = LEDV.get(key)
    if isinstance(v, dict):
        return v.get('sha16') or v.get('sha') or next((x for x in v.values() if isinstance(x, str) and len(x) == 16), None)
    return v


out = []; bad = 0


def P(x):
    out.append(x); print(x)


P('# 整合検査 v1 %s（段階 F・率盲検・許可表方式・器 SHA16 %s・%s UTC）' % (a.tag, SELF_SHA, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')))
P('| run_key | 行数 | 目標 | n_ok | api_error | format_fail | 重複 id | 欠落 index | 腕数 | 腕ごと n 揃い | runner_sha | arms_spec 一致 | system_sha 全 None | 盤 SHA 台帳突合 |')
P('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for d in sorted(glob.glob(os.path.join(a.root or os.path.join(REPO, 'results', a.tag), a.tag + '__*'))):
    key = os.path.basename(d); tf = glob.glob(os.path.join(d, 'trials-*.jsonl'))
    if len(tf) != 1:
        P('| %s | — | | | | | | | | | | | | trials ファイル %d 本 |' % (key, len(tf))); bad += 1; continue
    recs = [{k: v for k, v in json.loads(l).items() if k in ALLOW} for l in open(tf[0], encoding='utf-8') if l.strip()]
    target = len(PRE) * a.n
    ids = [r['trial_id'] for r in recs]; dup = len(ids) - len(set(ids))
    idx = sorted(r['trial_index'] for r in recs); missing = (idx[-1] - idx[0] + 1 - len(set(idx))) if idx else 0
    n_ok = sum(1 for r in recs if r.get('status') == 'ok'); err = len(recs) - n_ok; ff = sum(1 for r in recs if r.get('format_fail'))
    per = collections.Counter(r['arm'] for r in recs); even = (set(per) == set(PRE)) and all(v == a.n for v in per.values())
    rs = set(r.get('runner_sha') for r in recs); rsha = ','.join(sorted(x or '—' for x in rs))
    aspec = all(r.get('arms_spec') == recs[0].get('arms_spec') for r in recs)
    sys_none = all(r.get('system_sha') is None for r in recs)
    ps = collections.defaultdict(set)
    for r in recs:
        ps[r['arm']].add(r.get('preamble_sha'))
    mism = []
    for arm in per:
        gotp = next(iter(ps[arm])) if len(ps[arm]) == 1 else 'MULTI'
        if arm in KNOWN_NO_LEDGER:
            if gotp is not None:
                mism.append('%s preamble_sha が None でない' % arm)
            continue
        exp = led_sha(arm)
        if exp is None:
            mism.append('%s 台帳なし' % arm)
        elif gotp != exp:
            mism.append('%s preamble %s≠%s' % (arm, gotp, exp))
    ledger_ok = not mism
    ok = (len(recs) == target and dup == 0 and missing == 0 and err == 0 and ff == 0 and even and len(rs) == 1 and aspec and sys_none and ledger_ok)
    if not ok:
        bad += 1
    P('| %s | %d | %d | %d | %d | %d | %d | %d | %d | %s | %s | %s | %s | %s |' % (key, len(recs), target, n_ok, err, ff, dup, missing, len(per), '○' if even else '×', rsha, '○' if aspec else '×', '○' if sys_none else '×', '○' if ledger_ok else '×: ' + '・'.join(mism[:5])))
P('')
P('判定: %s' % ('全走行 整合' if bad == 0 else '不整合または未完 %d 走行' % bad))
P('本検査は判定欄（catastrophe・choice・refuse_class・raw 等）を読まない（許可表 %s の欄のみ保持）。format_fail は書式外の件数（三つ組の第三項）であり破局率ではない。盤の SHA 突合は各試行の preamble_sha を arms/panelF/SHA-LEDGER-F.json（U-Ncold・U-O-Ncold は V′ の arms/panel/SHA-LEDGER.json・腕名 N は前置きなしゆえ None を期待〔既知腕として先に例外登録〕）と比較し、台帳に無い腕は不一致として印字する。system 型は置かないため system_sha は全試行 None を期待する。' % (ALLOW,))
os.makedirs(os.path.join(REPO, 'records', 'F'), exist_ok=True)
p = os.path.join(REPO, 'records', 'F', 'integrity-%s-%s.md' % (a.tag, datetime.date.today().isoformat()))
open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
sys.exit(0 if bad == 0 else 1)
