# -*- coding: utf-8 -*-
"""calc_interim.py v0（2026-10-02・中間総括の新しい計算〔登録の外の記述・事後〕・枠 `00-frame-interim-summary-2026-10-02.md` §3 の計算一と計算二・コーディネータ南無弥勒如来）。
計算一 動く幅の地図: 段階 A の本走行 35 の走り・V′ の本走行 4 つの走り・B′ の行動の下見の閉じた記録の転記行 C から、腕 N・Onull・O・Ncold・Onull-Ncold・O-Ncold
  （B′ は Onull と O-Ncold）の全分母破局率（分子＝破局・分母＝n_ok）を取り、段階 A の正本 `censor` の主閾値（0.05 未満＝床・0.95 超＝天井）と感度閾値（0.03／0.08・0.97／0.92）で
  腕ごとの位置に印を付ける。検定はしない。
計算二 段階 C の対称性の記述: 段階 A と V′ の各走り（同じ走り・同じ規模）で、下向き（Onull→O）と上向き（Onull→Onull-Ncold）の Firth の対数オッズ比を、段階 A の凍結の器
  `tools/firth.py` の `fit`（集約形・行＝腕・成功＝破局・試行＝n_ok）で当て、絶対値の差（上向き − 下向き）と「余地なし」の印（三つの腕のどれかが主閾値の端）を並べる。検定・札は付けない。
入力は公開の置き場の記録だけ。閾値は段階 A の正本から読む（打ち直さない）。出力: `calc/calc-interim.json` と `calc/calc-interim.md`（一度だけ書く）。
用法: python calc_interim.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, glob, hashlib, math
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, 'calc')
sys.path.insert(0, os.path.join(PUB, 'tools'))
import firth as FI
NL = chr(10)
P = lambda *a: os.path.join(PUB, *a)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
CA = json.load(open(P('design', 'contrasts-A.json'), encoding='utf-8'))
CEN = CA['censor']
LOW, HIGH = CEN['low'], CEN['high']
SLOW, SHIGH = CEN['sensitivity']['low'], CEN['sensitivity']['high']
assert CEN['numerator'] == 'catastrophe' and CEN['denominator'] == 'n_ok'
ARMS = ['N', 'Onull', 'O', 'Ncold', 'Onull-Ncold', 'O-Ncold']
SIZE = {'Qwen/Qwen3-0.6B': '0.6B', 'Qwen/Qwen3-1.7B': '1.7B', 'Qwen/Qwen3-4B': '4B', 'Qwen/Qwen3-8B': '8B', 'Qwen/Qwen3-14B': '14B', 'Qwen/Qwen3-32B': '32B',
        'Qwen/Qwen3-4B-Instruct-2507': '4B-2507'}
ORDER = ['0.6B', '1.7B', '4B', '8B', '14B', '32B', '4B-2507']
SCN = ['N1', 'N2', 'S1', 'S4', 'SK']


def mark(r, lo, hi):
    return '床' if r < lo else ('天井' if r > hi else '中')


def cell_rate(c):
    k, n = c['triplet_all']['catastrophe'], c['n_ok']
    return k, n, k / n


def firth_logor(kc, nc, kt, nt):
    X = np.array([[1.0, 0.0], [1.0, 1.0]])
    r = FI.fit(X, np.array([float(kc), float(kt)]), np.array([float(nc), float(nt)]))
    return float(r['beta'][1]), bool(r['converged'])


def load_runs(pattern, stage):
    out, src = [], []
    for p in sorted(glob.glob(P(*pattern.split('/')))):
        d = json.load(open(p, encoding='utf-8'))
        m = d['manifest']
        assert d.get('integrity_ok') is not False, p
        out.append({'stage': stage, 'model': m['model'], 'size': SIZE[m['model']], 'provider': m.get('provider'), 'scenario': m['scenario'], 'cells': d['cells'], 'n_per_arm': m.get('n_per_arm')})
        src.append({'path': os.path.relpath(p, PUB).replace(os.sep, '/'), 'sha16': s16(p)})
    return out, src


def main():
    os.makedirs(OUTD, exist_ok=True)
    oj, om = os.path.join(OUTD, 'calc-interim.json'), os.path.join(OUTD, 'calc-interim.md')
    for p in (oj, om):
        assert not os.path.exists(p), '一度だけ: ' + p
    A, srcA = load_runs('results/stageA/stageA__*/cells.json', 'A')
    V, srcV = load_runs('results/stageVp/stageVp__*/cells.json', 'Vprime')
    assert len(A) == 35 and len(V) == 4, (len(A), len(V))
    assert sorted({(r['size'], r['scenario']) for r in A}) == sorted((s, c) for s in ORDER for c in SCN)
    BC = json.load(open(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'), encoding='utf-8'))
    srcB = [{'path': 'records/Bprime/behavior/behavior-closed-Bprime.json', 'sha16': s16(P('records', 'Bprime', 'behavior', 'behavior-closed-Bprime.json'))}]
    # ---- 計算一 ----
    rows1 = []
    for r in A + V:
        for a in ARMS:
            k, n, rate = cell_rate(r['cells'][a])
            rows1.append({'stage': r['stage'], 'model': r['model'], 'size': r['size'], 'provider': r['provider'], 'scenario': r['scenario'], 'arm': a, 'k': k, 'n_ok': n, 'rate': rate,
                          'mark_main': mark(rate, LOW, HIGH), 'mark_sens_strict': mark(rate, SLOW[0], SHIGH[0]), 'mark_sens_loose': mark(rate, SLOW[1], SHIGH[1])})
    for cell, c in BC['row_C']['cells'].items():
        scn, arm = cell.split('|')
        assert c['unscorable'] == 0 and c['n'] == 40, cell
        rows1.append({'stage': 'Bprime', 'model': 'google/gemma-4-31B-it', 'size': 'Gemma-31B', 'provider': 'local（G4）', 'scenario': scn, 'arm': arm, 'k': c['catastrophe'], 'n_ok': c['n'],
                      'rate': c['catastrophe'] / c['n'], 'mark_main': mark(c['catastrophe'] / c['n'], LOW, HIGH), 'mark_sens_strict': mark(c['catastrophe'] / c['n'], SLOW[0], SHIGH[0]),
                      'mark_sens_loose': mark(c['catastrophe'] / c['n'], SLOW[1], SHIGH[1])})
    per_model = {}
    for x in rows1:
        key = '%s|%s' % (x['stage'], x['size'])
        d = per_model.setdefault(key, {'cells': 0, 'floor': 0, 'ceiling': 0, 'middle': 0, 'ends_strict': 0, 'ends_loose': 0})
        d['cells'] += 1
        d[{'床': 'floor', '天井': 'ceiling', '中': 'middle'}[x['mark_main']]] += 1
        d['ends_strict'] += x['mark_sens_strict'] != '中'
        d['ends_loose'] += x['mark_sens_loose'] != '中'
    # ---- 計算二 ----
    rows2 = []
    for r in A + V:
        c = r['cells']
        kc, nc, rc = cell_rate(c['Onull'])
        ko, no, ro = cell_rate(c['O'])
        ku, nu, ru = cell_rate(c['Onull-Ncold'])
        dn, cd = firth_logor(kc, nc, ko, no)
        up, cu = firth_logor(kc, nc, ku, nu)
        ends = [a for a, rr in (('Onull', rc), ('O', ro), ('Onull-Ncold', ru)) if mark(rr, LOW, HIGH) != '中']
        rows2.append({'stage': r['stage'], 'size': r['size'], 'provider': r['provider'], 'scenario': r['scenario'], 'rate_Onull': rc, 'rate_O': ro, 'rate_OnullNcold': ru,
                      'logor_down': dn, 'logor_up': up, 'abs_diff_up_minus_down': abs(up) - abs(dn), 'converged': cd and cu, 'no_room': bool(ends), 'end_arms': ends})
    res = {'kind': 'interim_summary_calc', 'tool': 'summary/calc_interim.py v0', 'frame': '00-frame-interim-summary-2026-10-02.md（SHA16 %s）' % s16(os.path.join(HERE, '00-frame-interim-summary-2026-10-02.md')),
           'firth_tool': 'tools/firth.py %s（SHA16 %s）' % (FI.VERSION, s16(P('tools', 'firth.py'))), 'censor_from': 'design/contrasts-A.json censor（SHA16 %s）' % s16(P('design', 'contrasts-A.json')),
           'thresholds': {'main': [LOW, HIGH], 'sens_strict': [SLOW[0], SHIGH[0]], 'sens_loose': [SLOW[1], SHIGH[1]]},
           'inputs': {'A': srcA, 'Vprime': srcV, 'Bprime': srcB},
           'calc1_rows': rows1, 'calc1_per_model': per_model, 'calc2_rows': rows2,
           'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(oj, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    # ---- md ----
    L = ['# 中間総括の新しい計算（登録の外の記述・事後・機械生成）', '',
         '- 器: `summary/calc_interim.py` v0・枠 %s・Firth の器 %s・閾値の出所 %s。' % (res['frame'], res['firth_tool'], res['censor_from']),
         '- 率は全分母破局率（分子＝破局・分母＝n_ok）。印は腕ごとの位置（主閾値 %s 未満＝床・%s 超＝天井）。検定はしない。値を機種の安全さの比べとして読まない。' % (LOW, HIGH), '',
         '## 計算一 動く幅の地図（主閾値の印・括弧は率）', '']
    for stage, label in (('A', '段階 A（本走行・n_ok は各腕 200 前後・手元 bf16）'), ('Vprime', 'V′（本走行・n_ok は各腕 400 前後・API）'), ('Bprime', 'B′（行動の下見・各升目 40・段階 B の標本化）')):
        L += ['### ' + label, '', '| 機種 | 場面 | ' + ' | '.join(ARMS) + ' |', '|---|---|' + '---|' * len(ARMS)]
        sizes = [s for s in ORDER if any(x['stage'] == stage and x['size'] == s for x in rows1)] or sorted({x['size'] for x in rows1 if x['stage'] == stage})
        for s in sizes:
            for scn in SCN:
                cells = {x['arm']: x for x in rows1 if x['stage'] == stage and x['size'] == s and x['scenario'] == scn}
                if not cells:
                    continue
                L.append('| %s | %s | %s |' % (s, scn, ' | '.join(('%s（%.3f）' % (cells[a]['mark_main'], cells[a]['rate'])) if a in cells else '—' for a in ARMS)))
        L.append('')
    L += ['### 機種ごとの端の升の数', '', '| 段・機種 | 升 | 床 | 天井 | 中 | 端（感度・狭い）| 端（感度・広い）|', '|---|---|---|---|---|---|---|']
    for k_, d in per_model.items():
        L.append('| %s | %d | %d | %d | %d | %d | %d |' % (k_, d['cells'], d['floor'], d['ceiling'], d['middle'], d['ends_strict'], d['ends_loose']))
    L += ['', '## 計算二 段階 C の対称性の記述（同じ走り・同じ規模の中・札なし）', '',
          '- 下向き＝Onull→O、上向き＝Onull→Onull-Ncold の Firth の対数オッズ比。「余地なし」は三つの腕のどれかが主閾値の端。対称だった・対称でなかったとは読まない。段階 A と V′ を横断して並べて対称性を書かない。', '',
          '| 段 | 機種 | 場面 | Onull | O | Onull-Ncold | 下向き | 上向き | 絶対値の差（上−下）| 余地なし |', '|---|---|---|---|---|---|---|---|---|---|']
    for x in rows2:
        L.append('| %s | %s | %s | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %s |' % (x['stage'], x['size'], x['scenario'], x['rate_Onull'], x['rate_O'], x['rate_OnullNcold'], x['logor_down'], x['logor_up'],
                                                                              x['abs_diff_up_minus_down'], ('はい（%s）' % '・'.join(x['end_arms'])) if x['no_room'] else 'いいえ'))
    L += ['', '- 当てはめが収束しなかった升: %d' % sum(1 for x in rows2 if not x['converged']), '', res['clause'], '']
    open(om, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote calc-interim.json %s / calc-interim.md %s | calc1 rows %d | calc2 rows %d | no_room %d | nonconverged %d' % (
        s16(oj), s16(om), len(rows1), len(rows2), sum(1 for x in rows2 if x['no_room']), sum(1 for x in rows2 if not x['converged'])))


if __name__ == '__main__':
    main()
