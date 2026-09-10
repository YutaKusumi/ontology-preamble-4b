# -*- coding: utf-8 -*-
"""progress_M.py —— 追補 M の走行進捗を表で印字する（凍結対象外の便利器・集計には用いない）。
各走行（pilotM・stageM1・stageM2 × 前置き型／system 型 × N1/S1/S4/SK）について、書かれた行数／目標・最終行の時刻・直近 30 分の速度・残り時間の見込み・
api_error の件数を出し、走行器プロセス（run_preamble_api_m.py）の個数を Get-CimInstance（PID 単位）で確認する（wmic の行数計数は 1 プロセスを 4 と数えたため 2026-09-10 に置換）。
用法: python tools/progress_M.py            （PowerShell: $env:PYTHONUTF8=1; python tools/progress_M.py）
"""
import os, sys, json, glob, datetime, subprocess
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(os.path.join(REPO, 'design', 'contrasts-M.json'), encoding='utf-8'))
NPRE, NSYS = len(T['arms']['preamble']), len(T['arms']['system'])
PLAN = [('pilotM', 40), ('stageM1', 400), ('stageM2', 400)]
now = datetime.datetime.now(datetime.timezone.utc)


def alive():
    try:
        ps = "(Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Where-Object { $_.CommandLine -like '*run_preamble_api_m*' } | Measure-Object).Count"
        out = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, timeout=30).stdout.decode('utf-8', 'ignore').strip()
        return int(out.splitlines()[-1])
    except Exception:
        try:
            out = subprocess.run(['tasklist'], capture_output=True, timeout=20).stdout.decode('cp932', 'ignore')
            return out.lower().count('python.exe')
        except Exception:
            return -1


rows = []
for tag, n in PLAN:
    for kind, seeds, narm in (('前置き', T['seeds'][{'pilotM': 'pilot', 'stageM1': 'main1', 'stageM2': 'main2'}[tag]]['preamble'], NPRE), ('system', T['seeds'][{'pilotM': 'pilot', 'stageM1': 'main1', 'stageM2': 'main2'}[tag]]['system'], NSYS)):
        for sc in T['scenarios']:
            target = narm * n
            ds = glob.glob(os.path.join(REPO, 'results', tag, '%s__%s__*__seed%d' % (tag, sc, seeds[sc])))
            if not ds:
                rows.append((tag, kind, sc, 0, target, '—', '—', '—', '未着手', 0)); continue
            tf = glob.glob(os.path.join(ds[0], 'trials-*.jsonl'))
            if not tf:
                rows.append((tag, kind, sc, 0, target, '—', '—', '—', '未着手', 0)); continue
            recs = [json.loads(l) for l in open(tf[0], encoding='utf-8') if l.strip()]
            err = sum(1 for r in recs if r.get('status') != 'ok'); ts = sorted(r['timestamp_end'] for r in recs if r.get('timestamp_end'))
            last = datetime.datetime.fromisoformat(ts[-1]) if ts else None
            recent = [t for t in ts if (now - datetime.datetime.fromisoformat(t)).total_seconds() <= 1800]
            rate = len(recent) / 30.0 if recent else 0.0
            done = os.path.exists(os.path.join(ds[0], 'cells.json'))
            st = '完走' if (done and len(recs) >= target) else ('走行中' if (last and (now - last).total_seconds() < 600) else '**停止中?**（10 分以上更新なし）')
            eta = ('%.1f 時間' % ((target - len(recs)) / rate / 60)) if (rate > 0 and len(recs) < target) else ('—' if len(recs) >= target else '不明')
            rows.append((tag, kind, sc, len(recs), target, last.strftime('%m-%d %H:%M UTC') if last else '—', '%.0f 行/分' % rate if rate else '—', eta, st, err))
print('追補 M 走行進捗（%s UTC＝日本時間 %s）' % (now.strftime('%Y-%m-%d %H:%M'), (now + datetime.timedelta(hours=9)).strftime('%H:%M')))
print('| 段 | 型 | シナリオ | 行数/目標 | 最終行 | 直近 30 分の速度 | 残り見込み | 状態 | api_error |')
print('|---|---|---|---|---|---|---|---|---|')
for r in rows:
    print('| %s | %s | %s | %s/%s | %s | %s | %s | %s | %d |' % (r[0], r[1], r[2], format(r[3], ','), format(r[4], ','), r[5], r[6], r[7], r[8], r[9]))
a = alive()
print('走行器プロセス（run_preamble_api_m.py）: %s' % ('%d 個 稼働中' % a if a > 0 else ('なし' if a == 0 else '確認不能')))
tot_done = sum(r[3] for r in rows); tot = sum(r[4] for r in rows)
print('全体: %s / %s 試行（%.1f%%）' % (format(tot_done, ','), format(tot, ','), 100.0 * tot_done / tot))
