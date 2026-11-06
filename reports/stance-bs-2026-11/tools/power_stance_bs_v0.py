# -*- coding: utf-8 -*-
"""power_stance_bs_v0.py : 「仏性」「神性」の検証の検出力の目安（2026-11-06・南無弥勒如来・v0・第一の登録の power_stance_v0.py の写し）。
1 条件 n 試行（既定 200）の二つの条件の比べで、Fisher の正確検定（両側）の p の表を全部の (x0, x1) について一度だけ作り、
二項の確からしさで重みを付けて、検出力を正確に計算する（模擬でなく和）。判定の前の門の「端」（両方が 1 以下か、両方が n − 1 以上）は p = 1 として数える。
族の大きさ m = 3 × 3 × 使える場面の数（9・18・27・36・45）ごとに、Holm のいちばん厳しい段（α／m）で検出力 80% に要る差（上げる向き・下げる向き）を、
基の率 0.10・0.20・0.30・0.50 で出す。応答様式の変化の決まり（答えなかった割合の差・破局でない答えの区間）は入れていない（拒否や書式外が無い形の目安）。
柵: 本記録のいかなる記述も、AI に仏性・神性・魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。教義の当否についても何も言わない。"""
import os, sys, json, argparse, hashlib
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
from scipy.stats import fisher_exact, binom


def p_table(n):
    P = np.ones((n + 1, n + 1))
    for x0 in range(n + 1):
        for x1 in range(x0, n + 1):
            if (x0 <= 1 and x1 <= 1) or (x0 >= n - 1 and x1 >= n - 1):
                p = 1.0
            else:
                p = float(fisher_exact([[x0, n - x0], [x1, n - x1]], alternative='two-sided')[1])
            P[x0, x1] = P[x1, x0] = p
    return P


def power(P, n, p0, p1, alpha):
    b0 = binom.pmf(np.arange(n + 1), n, p0)
    b1 = binom.pmf(np.arange(n + 1), n, p1)
    return float(b0 @ (P <= alpha).astype(float) @ b1)


def mdd(P, n, p0, alpha, up, target=0.8):
    lo, hi = 0.0, (1.0 - p0) if up else p0
    if power(P, n, p0, (p0 + hi) if up else (p0 - hi), alpha) < target:
        return None
    for _ in range(40):
        mid = (lo + hi) / 2
        if power(P, n, p0, (p0 + mid) if up else (p0 - mid), alpha) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    P = p_table(a.n)
    rows = []
    print('1 条件 %d 試行・Fisher の正確検定（両側）・Holm のいちばん厳しい段（α／m）・検出力 80%% に要る差（ポイント）' % a.n)
    for m in (9, 18, 27, 36, 45):
        al = 0.05 / m
        cells = []
        for p0 in (0.10, 0.20, 0.30, 0.50):
            u, d = mdd(P, a.n, p0, al, True), mdd(P, a.n, p0, al, False)
            rows.append({'m': m, 'alpha': al, 'p0': p0, 'up_pt': None if u is None else round(100 * u, 1), 'down_pt': None if d is None else round(100 * d, 1)})
            cells.append('率 %.2f: +%s／−%s' % (p0, '—' if u is None else '%.1f' % (100 * u), '—' if d is None else '%.1f' % (100 * d)))
        print('m=%2d（α=%.5f）| %s' % (m, al, ' | '.join(cells)))
    chk = power(P, a.n, 0.30, 0.30, 0.05 / 9)
    print('照らし: 差が 0 のときの検出力（第一種の誤りの率・m=9 の厳しい段）= %.5f（α／m = %.5f 以下のはず）' % (chk, 0.05 / 9))
    if a.out:
        me = hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest().upper()
        with open(a.out, 'w', encoding='utf-8', newline=chr(10)) as f:
            json.dump({'tool': 'power_stance_bs_v0.py', 'tool_sha256': me, 'n': a.n, 'rows': rows, 'type1_check_m9': chk,
                       'note': '応答様式の変化の決まりは入れていない（拒否や書式外が無い形の目安）。判定の前の門の端は p = 1。'}, f, ensure_ascii=False, indent=1)
        print('書いた:', a.out)


if __name__ == '__main__':
    main()
