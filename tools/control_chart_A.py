# -*- coding: utf-8 -*-
"""control_chart_A.py v1 —— 校正腕の管理図 records/control-chart.md に段階 A の行を記帳する（記述・判定しない・正本 calibration・登録者裁定 D2・2026-09-13）。
合格枝（門0.5 合格）: 既存の表（段階 F から始まる API 系列）の末尾に、本走行と橋のセッションの校正腕の行を足す。段階 A の行の既測基底の欄は正本 bases_4B2507_api の N1・Ncold、
  帯の外の欄は合格枝の下側の帯（calibration.band_pass）で、表の直下に一度だけその旨の注を置く。
不合格枝（門0.5 不合格）: 見出し「手元系列（段階 A・vLLM・門0.5 不合格）」の表を新設し、初点（本走行の最初のセッションの校正腕）と以後のセッションを記帳する（初点との差・API 既測との差は記述）。
門0.5 の Ncold × N1 は両枝とも記述として一行置く（校正帯の初点に用いない・calibration.band_fail.gate05_point）。判定は tools/calib_band_A.py の出力を写すだけで、本器は帯を計算しない。
入力: --calib（calib_band_A の出力）・--identity（identity_screen_A の出力）。同じ行の標識（tag と持ち主とセッション）は二重に記帳しない。
用法: python tools/control_chart_A.py --calib records/A/calib-stageA-calib.json --identity records/A/identity-screen-A.json [--out <検査用の出力先・既定は records/control-chart.md>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
CHART = os.path.join(REPO, 'records', 'control-chart.md')
API_HEAD = '| 記帳日（UTC） | tag | 腕 | 場面 | 破局/n | 率 | 既測基底（M1） | 差（pt） | 5 pt 帯の外 |'
LOCAL_TITLE = '## 手元系列（段階 A・vLLM・門0.5 不合格・記述・判定しない）'

ap = argparse.ArgumentParser(); ap.add_argument('--calib', required=True); ap.add_argument('--identity', required=True); ap.add_argument('--contrasts', default=None); ap.add_argument('--out', default=None)
a = ap.parse_args()
T = runs_A.load_T(a.contrasts); CAL = T['calibration']; bb = T['bases_4B2507_api'][CAL['scenario']][CAL['arm']]; base = bb['k'] / bb['n']
CB = runs_A.read_json(a.calib); ID = runs_A.read_json(a.identity)
if CB.get('kind') != 'calib_band_A' or ID.get('kind') != 'identity_screen_A':
    sys.exit('--calib は calib_band_A・--identity は identity_screen_A の出力を渡す')
if CB['branch'] != ID['verdict']:
    sys.exit('校正帯の記録の枝（%s）と門0.5 の判定（%s）が食い違う' % (CB['branch'], ID['verdict']))
OUT = a.out or CHART
if a.out and not os.path.exists(OUT) and os.path.exists(CHART):
    shutil.copy(CHART, OUT)   # 検査用: 現物の写しに足す
lines = open(OUT, encoding='utf-8').read().rstrip('\n').split('\n') if os.path.exists(OUT) else ['# 校正腕の管理図', '', API_HEAD, '|---|---|---|---|---|---|---|---|---|']
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
clause_idx = next((i for i in range(len(lines) - 1, -1, -1) if '両方向不定' in lines[i]), None)
tail = lines[clause_idx:] if clause_idx is not None else []
body = lines[:clause_idx] if clause_idx is not None else lines
while body and not body[-1].strip():
    body.pop()
label = lambda x: '%s（%s %s s%d）' % (CB['tag'], x['phase'], x['owner'], x['session'])
exists = lambda lab: any(lab in l for l in body)
g05 = ID['local_counts'].get(CAL['arm']) or {}; g05_label = '%s（門0.5・記述）' % ID['tag']; added = 0
rate = lambda k, n: (k / n) if n else None
if CB['branch'] == 'pass':
    hi = max(i for i, l in enumerate(body) if l.startswith('|')) if any(l.startswith('|') for l in body) else len(body) - 1
    new = []
    if g05.get('n_ok') and not exists(g05_label):
        r = rate(g05['catastrophe'], g05['n_ok']); new.append('| %s | %s | %s | %s | %d/%d | %.4f | %.4f | %+.1f | 記述 |' % (stamp, g05_label, CAL['arm'], CAL['scenario'], g05['catastrophe'], g05['n_ok'], r, base, (r - base) * 100))
    for x in CB['sessions']:
        if x['n'] and not exists(label(x)):
            new.append('| %s | %s | %s | %s | %d/%d | %.4f | %.4f | %+.1f | %s |' % (stamp, label(x), CAL['arm'], CAL['scenario'], x['k'], x['n'], x['rate'], base, x['api_diff_pt'], '外' if x.get('fired') else '—'))
    body[hi + 1:hi + 1] = new; added = len(new)
    note = '段階 A の行（tag %s）の既測基底の欄は正本 bases_4B2507_api の N1・Ncold（%d/%d）、帯の外の欄は合格枝の下側の帯（%s pt・calibration.band_pass）。' % (CB['tag'], bb['k'], bb['n'], CAL['band_pass']['pt'])
    if added and note not in body:
        body[hi + 1 + added:hi + 1 + added] = ['', note]
else:
    if LOCAL_TITLE not in body:
        body += ['', LOCAL_TITLE, '', '初点＝本走行の最初のセッションの校正腕（判定しない）。以後のセッションは初点と両側 %s pt（calibration.band_fail）。門0.5 の行は記述（初点に用いない）。API 既測（%d/%d）との差は記述。' % (CAL['band_fail']['pt'], bb['k'], bb['n']),
                 '', '| 記帳日（UTC） | 標識 | 破局/n | 率 | 初点との差（pt） | 帯の外 | API 既測との差（pt・記述） |', '|---|---|---|---|---|---|---|']
    new = []
    if g05.get('n_ok') and not exists(g05_label):
        r = rate(g05['catastrophe'], g05['n_ok']); new.append('| %s | %s | %d/%d | %.4f | — | 記述 | %+.1f |' % (stamp, g05_label, g05['catastrophe'], g05['n_ok'], r, (r - base) * 100))
    for x in CB['sessions']:
        if x['n'] and not exists(label(x)):
            first = x.get('verdict') == 'first_point'
            new.append('| %s | %s%s | %d/%d | %.4f | %s | %s | %+.1f |' % (stamp, label(x), '（初点）' if first else '', x['k'], x['n'], x['rate'], '—' if first else '%+.1f' % x.get('diff_vs_first_pt', 0.0), '—' if first else ('外' if x.get('fired') else '—'), x['api_diff_pt']))
    body += new; added = len(new)
out_lines = body + [''] + (tail or ['本文書のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'])
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(out_lines) + '\n')
print('[control_chart_A] %s 枝・%d 行を記帳 → %s' % (CB['branch'], added, OUT))
