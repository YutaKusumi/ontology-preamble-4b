# -*- coding: utf-8 -*-
"""calc_interim.py v0.3（2026-10-02・中間総括の新しい計算〔登録の外の記述・事後〕・枠 `00-frame-interim-summary-2026-10-02.md` §3・枠の追記一 `00-frame-addendum1-2026-10-02.md` §1・§2・枠の追記二 `00-frame-addendum2-2026-10-02.md` §2・コーディネータ南無弥勒如来）。
v0（`prev/calc_interim-v0.py`）から v0.2（`prev/calc_interim-v0.2.py`）までに改めたこと（追記一・登録者裁定 D287）:
  - 計算一の名を「腕ごとの端の印の地図」に替え、入力から B′ の行動の下見を外した（B′ の正本の S10）。表は段ごとに分け、頭に環境と n、列名に閾値の数を書く。
  - 器の確かめを足した（censor.strict・感度の対の順・integrity_ok が在って真・V′ の場面が重ならない・段階 A の 7 機種 × 5 場面）。provider は記録の manifest から読む。
  - 計算二の定義は変えず、出力に段ごとの数・向きの印・閾値ちょうどの印・端の行の注を足した。v0.2 は向きの印に零の幅（ZERO_TOL）を置いた（v0.1 は 1e-16 の誤差に印を付けた）。
v0.3 で足したこと（追記二 §2・登録者裁定 D288・二巡目の検分で値を見た後の記述）: 計算一の閾値に等しい腕の印と、等号を端に含めたときの機種ごとの端の数（参考）・腕ごとの書式外と refuse の数と、段と機種ごとの書式外の和・走りごとの腕の数と標本化の設定（manifest から）。v0.2 の説明文が出力を v0.1 の名で書いていた誤りを直した。率・印・対数オッズ比の値が v0.2 の出力と同じことを器で確かめる。
入力は公開の置き場の記録だけ。閾値は段階 A の正本から読む（打ち直さない）。出力: `calc/calc-interim-v0.3.json` と `calc/calc-interim-v0.3.md`（一度だけ書く・v0〜v0.2 の出力は残す）。
用法: python calc_interim.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, glob, hashlib
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, 'calc')
VER = 'v0.3'
ZERO_TOL = 1e-9
sys.path.insert(0, os.path.join(PUB, 'tools'))
import firth as FI
NL = chr(10)
P = lambda *a: os.path.join(PUB, *a)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
CA = json.load(open(P('design', 'contrasts-A.json'), encoding='utf-8'))
CEN = CA['censor']
assert CEN['type'] == 'both_arm_condition' and CEN['strict'] is True, '検閲の型と strict を正本から確かめる'
assert CEN['numerator'] == 'catastrophe' and CEN['denominator'] == 'n_ok'
LOW, HIGH = CEN['low'], CEN['high']
SLOW, SHIGH = CEN['sensitivity']['low'], CEN['sensitivity']['high']
assert len(SLOW) == 2 and len(SHIGH) == 2 and SLOW[0] < LOW < SLOW[1] and SHIGH[1] < HIGH < SHIGH[0], '感度の対の順（一つ目どうし＝両端へ広げた側・二つ目どうし＝狭めた側）'
SENS = [(SLOW[0], SHIGH[0]), (SLOW[1], SHIGH[1])]
ARMS = ['N', 'Onull', 'O', 'Ncold', 'Onull-Ncold', 'O-Ncold']
SIZE = {'Qwen/Qwen3-0.6B': '0.6B', 'Qwen/Qwen3-1.7B': '1.7B', 'Qwen/Qwen3-4B': '4B', 'Qwen/Qwen3-8B': '8B', 'Qwen/Qwen3-14B': '14B', 'Qwen/Qwen3-32B': '32B',
        'Qwen/Qwen3-4B-Instruct-2507': '4B-2507'}
ORDER = ['0.6B', '1.7B', '4B', '8B', '14B', '32B', '4B-2507']
SCN = ['N1', 'N2', 'S1', 'S4', 'SK']
ENV = {'A': '段階 A の本走行（手元・bf16）', 'Vprime': 'V′ の本走行（API）'}
LAB = {'A': '段階 A', 'Vprime': 'V′'}


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
        assert d.get('integrity_ok') is True, ('integrity_ok が在って真でない', p)
        assert m.get('provider'), ('provider が記録に無い', p)
        out.append({'stage': stage, 'model': m['model'], 'size': SIZE[m['model']], 'provider': m['provider'], 'scenario': m['scenario'], 'cells': d['cells'],
                    'n_arms': len(d['cells']), 'sampling': m.get('sampling')})
        src.append({'path': os.path.relpath(p, PUB).replace(os.sep, '/'), 'sha16': s16(p)})
    return out, src


def main():
    os.makedirs(OUTD, exist_ok=True)
    oj, om = os.path.join(OUTD, 'calc-interim-%s.json' % VER), os.path.join(OUTD, 'calc-interim-%s.md' % VER)
    for p in (oj, om):
        assert not os.path.exists(p), '一度だけ: ' + p
    A, srcA = load_runs('results/stageA/stageA__*/cells.json', 'A')
    V, srcV = load_runs('results/stageVp/stageVp__*/cells.json', 'Vprime')
    assert len(A) == 35 and len(V) == 4, (len(A), len(V))
    assert sorted((r['size'], r['scenario']) for r in A) == sorted((s, c) for s in ORDER for c in SCN), '段階 A の 7 機種 × 5 場面'
    assert len({r['scenario'] for r in V}) == 4 and {r['size'] for r in V} == {'4B-2507'}, 'V′ の四つの場面が重ならない・機種は 4B-2507'
    # ---- 計算一 腕ごとの端の印の地図 ----
    rows1 = []
    for r in A + V:
        for a in ARMS:
            k, n, rate = cell_rate(r['cells'][a])
            t3 = r['cells'][a]['triplet_all']
            eq = [('主' if t in (LOW, HIGH) else '感度') + ' %s' % t for t in (LOW, HIGH, SENS[0][0], SENS[0][1], SENS[1][0], SENS[1][1]) if abs(k - t * n) < 1e-9]
            rows1.append({'stage': r['stage'], 'model': r['model'], 'size': r['size'], 'provider': r['provider'], 'scenario': r['scenario'], 'arm': a, 'k': k, 'n_ok': n, 'rate': rate,
                          'mark_main': mark(rate, LOW, HIGH), 'mark_sens_wide': mark(rate, *SENS[0]), 'mark_sens_narrow': mark(rate, *SENS[1]),
                          'format_out': t3.get('format_out', 0), 'refuse': t3.get('refuse', 0), 'threshold_equal': eq})
    per_model = {}
    for x in rows1:
        key = '%s|%s' % (x['stage'], x['size'])
        d = per_model.setdefault(key, {'cells': 0, 'floor': 0, 'ceiling': 0, 'middle': 0, 'ends_sens_wide': 0, 'ends_sens_narrow': 0, 'ends_main_inclusive': 0, 'format_out_sum': 0, 'refuse_sum': 0,
                                       'threshold_equal_arms': []})
        d['cells'] += 1
        d[{'床': 'floor', '天井': 'ceiling', '中': 'middle'}[x['mark_main']]] += 1
        d['ends_sens_wide'] += x['mark_sens_wide'] != '中'
        d['ends_sens_narrow'] += x['mark_sens_narrow'] != '中'
        d['ends_main_inclusive'] += (x['k'] <= LOW * x['n_ok'] + 1e-9) or (x['k'] >= HIGH * x['n_ok'] - 1e-9)
        d['format_out_sum'] += x['format_out']
        d['refuse_sum'] += x['refuse']
        if x['threshold_equal']:
            d['threshold_equal_arms'].append('%s %s（%d/%d・%s）' % (x['scenario'], x['arm'], x['k'], x['n_ok'], '・'.join(x['threshold_equal'])))
    runs_info = {st: {'n_arms_per_run': sorted({r['n_arms'] for r in rs}), 'sampling': sorted({json.dumps(r['sampling'], ensure_ascii=False, sort_keys=True) for r in rs})} for st, rs in (('A', A), ('Vprime', V))}
    # v0.2 の出力と、率・印・対数オッズ比の値が同じことを確かめる
    V2 = json.load(open(os.path.join(OUTD, 'calc-interim-v0.2.json'), encoding='utf-8'))
    assert [(x['stage'], x['size'], x['scenario'], x['arm'], x['k'], x['n_ok'], x['mark_main'], x['mark_sens_wide'], x['mark_sens_narrow']) for x in V2['calc1_rows']] == \
           [(x['stage'], x['size'], x['scenario'], x['arm'], x['k'], x['n_ok'], x['mark_main'], x['mark_sens_wide'], x['mark_sens_narrow']) for x in rows1], 'v0.2 と計算一が違う'
    nset = {st: sorted({x['n_ok'] for x in rows1 if x['stage'] == st}) for st in ('A', 'Vprime')}
    prov = {st: sorted({x['provider'] for x in rows1 if x['stage'] == st}) for st in ('A', 'Vprime')}
    # ---- 計算二 段階 C の対称性の記述 ----
    rows2 = []
    for r in A + V:
        c = r['cells']
        kc, nc, rc = cell_rate(c['Onull'])
        ko, no, ro = cell_rate(c['O'])
        ku, nu, ru = cell_rate(c['Onull-Ncold'])
        dn, cd = firth_logor(kc, nc, ko, no)
        up, cu = firth_logor(kc, nc, ku, nu)
        rates = (('Onull', rc), ('O', ro), ('Onull-Ncold', ru))
        ends = [a for a, rr in rates if mark(rr, LOW, HIGH) != '中']
        exact = [a for a, rr in rates if rr == LOW or rr == HIGH]
        bounds = [a for a, (kk, nn) in (('Onull', (kc, nc)), ('O', (ko, no)), ('Onull-Ncold', (ku, nu))) if kk in (0, nn)]
        rows2.append({'stage': r['stage'], 'size': r['size'], 'provider': r['provider'], 'scenario': r['scenario'], 'k_n': {'Onull': [kc, nc], 'O': [ko, no], 'Onull-Ncold': [ku, nu]},
                      'rate_Onull': rc, 'rate_O': ro, 'rate_OnullNcold': ru, 'logor_down': dn, 'logor_up': up, 'abs_diff_up_minus_down': abs(up) - abs(dn), 'converged': cd and cu,
                      'no_room': bool(ends), 'end_arms': ends, 'down_positive': dn > ZERO_TOL, 'up_negative': up < -ZERO_TOL, 'down_zero': abs(dn) < ZERO_TOL, 'up_zero': abs(up) < ZERO_TOL, 'threshold_exact_arms': exact, 'boundary_count_arms': bounds})
    by_stage = {}
    for st in ('A', 'Vprime'):
        xs = [x for x in rows2 if x['stage'] == st]
        by_stage[st] = {'cells': len(xs), 'room': sum(1 for x in xs if not x['no_room']), 'room_cells': ['%s %s' % (x['size'], x['scenario']) for x in xs if not x['no_room']],
                        'end_arm_counts': {a: sum(1 for x in xs if a in x['end_arms']) for a in ('O', 'Onull-Ncold', 'Onull')},
                        'down_positive_cells': ['%s %s' % (x['size'], x['scenario']) for x in xs if x['down_positive']],
                        'up_negative_cells': ['%s %s' % (x['size'], x['scenario']) for x in xs if x['up_negative']],
                        'threshold_exact_cells': ['%s %s（%s）' % (x['size'], x['scenario'], '・'.join(x['threshold_exact_arms'])) for x in xs if x['threshold_exact_arms']],
                        'nonconverged': sum(1 for x in xs if not x['converged'])}
    assert [(x['stage'], x['size'], x['scenario'], round(x['logor_down'], 9), round(x['logor_up'], 9), x['no_room'], x['end_arms'], x['down_positive'], x['up_negative']) for x in V2['calc2_rows']] == \
           [(x['stage'], x['size'], x['scenario'], round(x['logor_down'], 9), round(x['logor_up'], 9), x['no_room'], x['end_arms'], x['down_positive'], x['up_negative']) for x in rows2], 'v0.2 と計算二が違う'
    res = {'kind': 'interim_summary_calc', 'tool': 'summary/calc_interim.py %s' % VER,
           'frame': '00-frame-interim-summary-2026-10-02.md（SHA16 %s）＋追記一 00-frame-addendum1-2026-10-02.md（SHA16 %s）＋追記二 00-frame-addendum2-2026-10-02.md（SHA16 %s）' % (
               s16(os.path.join(HERE, '00-frame-interim-summary-2026-10-02.md')), s16(os.path.join(HERE, '00-frame-addendum1-2026-10-02.md')), s16(os.path.join(HERE, '00-frame-addendum2-2026-10-02.md'))),
           'same_as_v0_2': '計算一の分子・分母・印と、計算二の対数オッズ比・余地なし・端の腕・向きの印が v0.2 の出力と同じことを器で確かめた', 'runs_info': runs_info,
           'post_hoc_note_v0_3': '計算一の閾値に等しい腕・等号を端に含めた端の数（参考）・書式外と refuse の数・走りの腕の数と標本化は、二巡目の検分で値を見た後に足した記述（追記二 §2）。札ではない。全分母の率は書式外と refuse を分母に含む（正本の定義のまま）。',
           'firth_tool': 'tools/firth.py %s（SHA16 %s）' % (FI.VERSION, s16(P('tools', 'firth.py'))), 'censor_from': 'design/contrasts-A.json censor（SHA16 %s）' % s16(P('design', 'contrasts-A.json')),
           'thresholds': {'main': [LOW, HIGH], 'sens_wide': list(SENS[0]), 'sens_narrow': list(SENS[1])},
           'inputs': {'A': srcA, 'Vprime': srcV}, 'not_inputs': 'B′ の行動の下見（S10・追記一 §1）・4B の最初の登録・追補 M・段階 F（腕と場面と n の組が違う）',
           'n_ok_by_stage': nset, 'provider_by_stage': prov,
           'calc1_rows': rows1, 'calc1_per_model': per_model, 'calc2_rows': rows2, 'calc2_by_stage': by_stage,
           'post_hoc_note': '計算二の段ごとの数・向きの印・閾値ちょうどの印・境の数の印は、一巡目の検分で値を見た後に足した記述（追記一 §2）。札ではない。向きの印は絶対値が %g 未満を零として付けない。' % ZERO_TOL, 'zero_tol': ZERO_TOL,
           'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(oj, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    # ---- md ----
    L = ['# 中間総括の新しい計算 %s（登録の外の記述・事後・機械生成）' % VER, '',
         '- 器: `summary/calc_interim.py` %s・枠 %s・Firth の器 %s・閾値の出所 %s。' % (VER, res['frame'], res['firth_tool'], res['censor_from']),
         '- 入力: 段階 A の本走行の %d の走りと V′ の本走行の %d の走り。入れていないもの: %s。' % (len(A), len(V), res['not_inputs']),
         '- 率は全分母破局率（分子＝破局・分母＝n_ok）。印は腕ごとの位置。正本の検閲は両腕の条件で、片腕のみの飽和は検閲せず解釈条項が受ける（`censor.text`）。この地図は腕ごとの位置の記述で、検閲や札の代わりにしない。検定はしない。値を機種の安全さの比べとして読まない。', '',
         '## 計算一 腕ごとの端の印の地図（主閾値 %s 未満＝床・%s 超＝天井・括弧は率）' % (LOW, HIGH), '']
    for st in ('A', 'Vprime'):
        L += ['### %s（provider %s・各腕の n_ok %s）' % (ENV[st], '・'.join(prov[st]), '・'.join(str(n) for n in nset[st])), '', '| 機種 | 場面 | ' + ' | '.join(ARMS) + ' |', '|---|---|' + '---|' * len(ARMS)]
        for s in [s_ for s_ in ORDER if any(x['stage'] == st and x['size'] == s_ for x in rows1)]:
            for scn in SCN:
                cells = {x['arm']: x for x in rows1 if x['stage'] == st and x['size'] == s and x['scenario'] == scn}
                if cells:
                    L.append('| %s | %s | %s |' % (s, scn, ' | '.join('%s（%.3f）' % (cells[a]['mark_main'], cells[a]['rate']) for a in ARMS)))
        L.append('')
        L += ['#### %s の機種ごとの端の升の数' % LAB[st], '', '| 機種 | 升 | 床（%s 未満） | 天井（%s 超） | 中 | 端（感度 %s／%s） | 端（感度 %s／%s） |' % (LOW, HIGH, SENS[0][0], SENS[0][1], SENS[1][0], SENS[1][1]),
              '|---|---|---|---|---|---|---|']
        for k_, d in per_model.items():
            if k_.split('|')[0] == st:
                L.append('| %s | %d | %d | %d | %d | %d | %d |' % (k_.split('|')[1], d['cells'], d['floor'], d['ceiling'], d['middle'], d['ends_sens_wide'], d['ends_sens_narrow']))
        L.append('')
        L += ['#### %s の機種ごとの書式外と refuse の数・閾値に等しい腕（v0.3 で足した・二巡目の検分で値を見た後の記述）' % LAB[st], '',
              '| 機種 | 六つの腕の書式外の和 | 六つの腕の refuse の和 | 主閾値の端（等号を含めた参考） | 閾値に等しい腕（場面・腕・k/n・閾値） |', '|---|---|---|---|---|']
        for k_, d in per_model.items():
            if k_.split('|')[0] == st:
                L.append('| %s | %d | %d | %d | %s |' % (k_.split('|')[1], d['format_out_sum'], d['refuse_sum'], d['ends_main_inclusive'], '・'.join(d['threshold_equal_arms']) or '—'))
        L += ['', '- 走りの腕の数: %s（計算はそのうち六つの腕 %s を取る）。標本化（manifest）: %s。' % (
            '・'.join(str(n) for n in runs_info[st]['n_arms_per_run']), '・'.join(ARMS), ' ／ '.join(runs_info[st]['sampling'])),
              '- 全分母の率は、書式外と refuse を分母に含む（正本の定義のまま）。率が床の升は、破局でない選択肢を選んだ位置とは限らない（書式外の多い升がある）。', '']
    L += ['## 計算二 段階 C の対称性の記述（同じ走り・同じ規模の中・札なし）', '',
          '- 下向き＝Onull→O、上向き＝Onull→Onull-Ncold の Firth の対数オッズ比。「余地なし」は三つの腕のどれかが主閾値の端。対称だった・対称でなかったとは読まない。段階 A と V′ を横断して並べて対称性を書かない。',
          '- 0/n や n/n を含む升の対数オッズ比は、0.5 の補正と n で大きさが決まる（二行の集約の形では、Firth の推定は各升に 0.5 を足した対数オッズ比と同じ）。',
          '- 向きの印・閾値ちょうどの印・段ごとの数は、一巡目の検分で値を見た後に足した記述（枠の追記一 §2）。向きの印は、絶対値が %g 未満の値（三つの腕がそろって同じ端にある升など）には付けない。' % ZERO_TOL, '']
    for st in ('A', 'Vprime'):
        b = by_stage[st]
        L += ['### %s（%d 升）' % (ENV[st], b['cells']), '', '| 機種 | 場面 | Onull | O | Onull-Ncold | 下向き | 上向き | 絶対値の差（上−下） | 余地なし | 向きの印 | 閾値ちょうど |', '|---|---|---|---|---|---|---|---|---|---|---|']
        for x in [x_ for x_ in rows2 if x_['stage'] == st]:
            sign = '・'.join(([] if not x['down_positive'] else ['下向きが正']) + ([] if not x['up_negative'] else ['上向きが負'])) or '—'
            L.append('| %s | %s | %d/%d（%.3f） | %d/%d（%.3f） | %d/%d（%.3f） | %.3f | %.3f | %.3f | %s | %s | %s |' % (
                x['size'], x['scenario'], x['k_n']['Onull'][0], x['k_n']['Onull'][1], x['rate_Onull'], x['k_n']['O'][0], x['k_n']['O'][1], x['rate_O'],
                x['k_n']['Onull-Ncold'][0], x['k_n']['Onull-Ncold'][1], x['rate_OnullNcold'], x['logor_down'], x['logor_up'], x['abs_diff_up_minus_down'],
                ('はい（%s）' % '・'.join(x['end_arms'])) if x['no_room'] else 'いいえ', sign, '・'.join(x['threshold_exact_arms']) or '—'))
        L += ['', '- %s: 三つの腕がそろって主閾値の中にある升 %d／%d（%s）・端に当たった腕 O %d・Onull-Ncold %d・Onull %d（重なりあり）・下向きが正の升 %s・上向きが負の升 %s・閾値ちょうどの升 %s・当てはめが収束しなかった升 %d。' % (
            LAB[st], b['room'], b['cells'], '・'.join(b['room_cells']) or 'なし', b['end_arm_counts']['O'], b['end_arm_counts']['Onull-Ncold'], b['end_arm_counts']['Onull'],
            '・'.join(b['down_positive_cells']) or 'なし', '・'.join(b['up_negative_cells']) or 'なし', '・'.join(b['threshold_exact_cells']) or 'なし', b['nonconverged']), '']
    L += [res['clause'], '']
    open(om, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote calc-interim-%s.json %s / .md %s | calc1 rows %d | calc2 rows %d | room A %d/%d V′ %d/%d | nonconverged %d' % (
        VER, s16(oj), s16(om), len(rows1), len(rows2), by_stage['A']['room'], by_stage['A']['cells'], by_stage['Vprime']['room'], by_stage['Vprime']['cells'],
        sum(1 for x in rows2 if not x['converged'])))


if __name__ == '__main__':
    main()
