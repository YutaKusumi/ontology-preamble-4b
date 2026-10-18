# -*- coding: utf-8 -*-
"""calc1_2_scale_figures.py v0.5（2026-10-15・草案5 の照らしの後: 図 3.1 の注から記録の言葉「計算一」を外した〔照らしの器の残してはいけない句〕・その前の出力は見せる前に prev/calc1-v0.5-unshown-third/・prev/calc2-v0.5-unshown-third/ へ移した・裁定 D460-3 の当て: 図 3.2 の注から決定の番号を外し、決めの記録は付録 H と書いた〔本文の章に差し込む図〕・その前の出力は見せる前に prev/calc1-v0.5-unshown-second/・prev/calc2-v0.5-unshown-second/ へ移し、器の前の写しは prev/calc1_2_scale_figures-v0.5-unshown-second.py・三巡目の採否と裁定 D458 の後: 冷徹な戦略家の役の一行の範囲を記録の字で〔3L-02〕・効き目の断りをどの条件にも同じ形で〔3L-01〕・八つの条件の選びの出所〔3L-09・D458-2〕・★の見本を組の外へ〔3L-05〕・図 3.2 の決定の注〔3L-10〕・測定不能の注〔3L-15〕・入力と値は替えない・v0.4 は prev/calc1_2_scale_figures-v0.4.py・v0.5 の一度目の出力は 3L-15 の当て漏れで見せる前に prev/calc1-v0.5-unshown-first/・prev/calc2-v0.5-unshown-first/ へ移した）。
calc1_2_scale_figures.py v0.4（2026-10-15・論文の草案3 の検分の二巡目の採否〔`E/reviews/paper-r2/adoption-paper-r2-v0.md` の 2L-01・2L-02・2L-04・2L-05・2L-06・2L-07・2L-08・2L-09〕と裁定 D453 の後・
v0.3 は `prev/calc1_2_scale_figures-v0.3.py`〔出力 calc1-v0.3/・calc2-v0.3/ は草案3 と二巡目の検分が使ったので残す〕・枠 §5 の計算一〔規模の図〕と計算二〔段階 C の予備実験の 4B の点・決定 D292・D425-5〕・
図の作りは枠の追記二〔裁定 D450-1・D450-2〕のまま・コーディネータ南無弥勒如来）。
v0.4 の一度目の出力は、計算二の題の字の書式の誤りで途中で止まったので、見せる前に `prev/calc1-v0.4-unshown-first/`・`prev/calc2-v0.4-unshown-first/` へ移した（計算一の図は描けていた）。二度目の出力も、注の字の折り返しが「。」で行を始め、下の余白が空いたので、見せる前に `prev/calc1-v0.4-unshown-second/`・`prev/calc2-v0.4-unshown-second/` へ移した（値は同じ）。
v0.3 からの違い（図の字と見やすさだけ・入力・描く条件・値・区間の計算は替えない）:
  - 計算一: 目盛りの「4B」を「Qwen3-4B」、「4B-2507」を「4B〔2507〕」にし、題を地の文の粗さにそろえ「規模の効果を示す図ではない」を題に入れる（2L-04・2L-09）。
    縦軸の名を目盛りの数と重ならない置き場所にする。凡例を二つの組（一行を含まない条件・含む条件）に分け、4B〔2507〕の印の見本を白抜きの★にする（2L-09）。
    横軸の注に 4B〔2507〕が並びの外であることを書く。注の字を地の文にそろえる: 分母（どのセルも応答の得られた試行は 200・2L-08）・論文の三つ組と四つの分けが重ならないこと（2L-07・2L-09）・
    灰色の帯と、検閲や測定不能として対比から外した規模の点を率の比べとして読まないこと（2L-06・付録 J.5 の (iii)）・描いた八つの条件と描いていない五つ（2L-09）・
    冷徹な戦略家の役の一行の範囲と両用性の制約と、図の上の差をこの一行の効き目として読まないこと（2L-05）・機構の層の点を打たない理由（操作が違う・2L-02）。
  - 計算二: 注の「段階 E の枠の計算二の決め・D292」を「段階 E の枠の決め（決定 D292〔2026-10-02・予備実験の値を見た後〕・決定 D425-5）」にし、題の Nscale を「提供者 Nscale」にする（2L-01）。
    冷徹な戦略家の役の一行の範囲と両用性の制約の一文を足す（2L-05）。縦軸の名の置き場所を直す（2L-09）。分母の注を足す。
書く物（一度だけ）: `E/E3/calc/calc1-v0.4/`・`E/E3/calc/calc2-v0.4/` の図と値の json と記録。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, math, glob, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
O1, O2 = os.path.join(HERE, 'calc1-v0.5'), os.path.join(HERE, 'calc2-v0.5')
for p_ in (O1, O2):
    assert not os.path.exists(p_), ('一度だけ', p_)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
plt.rcParams['font.family'] = 'Noto Sans JP'
sha = lambda b: hashlib.sha256(b).hexdigest().upper()
Z = 1.959963984540054
RATE_LABEL = '破局的選択の率\n（応答の得られた試行を分母）'
NOANS_LABEL = '答えなかった割合\n（拒否と書式外・同じ分母）'
COLD_BASE = ('冷徹な戦略家の役の一行は、追補 V′ が「この文形・この語・この 4B 構成で」「後置き」で上昇を報告した一行である（記録の字・範囲は付録 J.2）。図の点は、追補 V′ と構成や置き方が違いうる。'
             'この一行を含む条件も含まない条件と同じ解釈上の制約の下に置き、加えて追補 V′ と同じ両用性の制約（上昇を招く操作の手順を書かない）の下に置く。')
COLD = COLD_BASE + '図の上の差を、どの条件の効き目としても読まない（この一行を含む条件も、含まない条件も）。'   # v0.5: 図 3.1（3L-01）
COLD2 = COLD_BASE + '図の上の差を、どの条件の効き目としても読まない（Onull と冷徹な戦略家の役の一行の条件も、O と Onull の差も）。'   # v0.5: 図 3.2（3L-01）


def wilson(k, n):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def ebar(ax, x, k, n, col, mk, ms, face=None):
    r = k / n
    lo, hi = wilson(k, n)
    ax.errorbar([x], [r], yerr=[[max(0.0, r - lo)], [max(0.0, hi - r)]], fmt='none', ecolor=col, elinewidth=0.9, capsize=1.5)
    ax.plot([x], [r], marker=mk, markersize=ms, color=col, markerfacecolor=face if face else col, linestyle='none')
    return r, (lo, hi)


def wrap(s, n):
    out, cur = [], ''
    for i, ch in enumerate(s):
        cur += ch
        nxt = s[i + 1] if i + 1 < len(s) else ''
        if len(cur) >= n and ch in '。・、）' and nxt not in '。、）」・':
            out.append(cur)
            cur = ''
    if cur:
        out.append(cur)
    return NL.join(out)


now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
# ---------------- 計算一
SCENES = ['N1', 'N2', 'S1', 'S4', 'SK']
MODELS = ['Qwen/Qwen3-0.6B', 'Qwen/Qwen3-1.7B', 'Qwen/Qwen3-4B', 'Qwen/Qwen3-8B', 'Qwen/Qwen3-14B', 'Qwen/Qwen3-32B', 'Qwen/Qwen3-4B-Instruct-2507']
XPOS = {'Qwen/Qwen3-0.6B': 0, 'Qwen/Qwen3-1.7B': 1, 'Qwen/Qwen3-4B': 2, 'Qwen/Qwen3-8B': 3, 'Qwen/Qwen3-14B': 4, 'Qwen/Qwen3-32B': 5, 'Qwen/Qwen3-4B-Instruct-2507': 6.8}
XLAB = {'Qwen/Qwen3-0.6B': '0.6B', 'Qwen/Qwen3-1.7B': '1.7B', 'Qwen/Qwen3-4B': 'Qwen3-4B', 'Qwen/Qwen3-8B': '8B', 'Qwen/Qwen3-14B': '14B', 'Qwen/Qwen3-32B': '32B', 'Qwen/Qwen3-4B-Instruct-2507': '4B〔2507〕'}
ARMS_A = ['Onull', 'N', 'Odose1', 'Odosehalf', 'Lneg']
ARMS_B = ['Onull-Ncold', 'O-Ncold', 'Osec-Ncold']
NOT_DRAWN = ['O', 'Osec', 'Nk', 'Ncold', 'Nstr']
COL = {'Onull': '#000000', 'N': '#0072B2', 'Odose1': '#E69F00', 'Odosehalf': '#009E73', 'Lneg': '#CC79A7', 'Onull-Ncold': '#D55E00', 'O-Ncold': '#56B4E9', 'Osec-Ncold': '#999999'}
runs = sorted(glob.glob(os.path.join(PUB, 'results', 'stageA', 'stageA__*__none__seed*', 'cells.json')))
assert len(runs) == 35, len(runs)
tri, inputs = {}, []
for p in runs:
    b = open(p, 'rb').read()
    C = json.loads(b.decode('utf-8'))
    assert C['integrity_ok'] is True
    m, sc = C['manifest']['model'], C['manifest']['scenario']
    inputs.append({'path': os.path.relpath(p, PUB).replace(os.sep, '/'), 'sha256': sha(b), 'model': m, 'scenario': sc})
    assert sorted(C['cells']) == sorted(ARMS_A + ARMS_B + NOT_DRAWN), sorted(C['cells'])
    for arm, v in C['cells'].items():
        t = v['triplet_all']
        assert t['catastrophe'] + t['refuse'] + t['format_out'] + t['other_answered'] == t['n_ok'] and t['sum_ok'] is True, (m, sc, arm)
        tri[(m, sc, arm)] = {'catastrophe': t['catastrophe'], 'refuse': t['refuse'], 'format_out': t['format_out'], 'other_answered': t['other_answered'], 'n_ok': t['n_ok']}
assert sorted({(m, s) for (m, s, a) in tri}) == sorted((m, s) for m in MODELS for s in SCENES)
assert all(tri[(m, s, a)]['n_ok'] == 200 for m in MODELS for s in SCENES for a in ARMS_A + ARMS_B), '応答の得られた試行が 200 でないセルがある'
CI = json.load(open(os.path.join(PUB, 'summary', 'calc', 'calc-interim-v0.4.json'), encoding='utf-8'))
cmp_rows, mism = 0, []
for r in CI['calc1_rows']:
    if r['stage'] != 'A':
        continue
    x = tri[(r['model'], r['scenario'], r['arm'])]
    cmp_rows += 1
    if not (x['catastrophe'] == r['k'] and x['n_ok'] == r['n_ok'] and abs(x['catastrophe'] / x['n_ok'] - r['rate']) < 1e-12):
        mism.append((r['model'], r['scenario'], r['arm']))
assert not mism, mism
os.makedirs(O1)
fig, axes = plt.subplots(4, 5, figsize=(16, 14.2), sharex=True, sharey=True)
vals1 = []
for blk, arms in enumerate((ARMS_A, ARMS_B)):
    for j, sc in enumerate(SCENES):
        axr, axn = axes[2 * blk][j], axes[2 * blk + 1][j]
        axr.axhspan(0, 0.05, color='0.92', zorder=0)
        axr.axhspan(0.95, 1.0, color='0.92', zorder=0)
        for k, arm in enumerate(arms):
            off = 0.11 * (k - (len(arms) - 1) / 2.0)
            for m in MODELS:
                x = tri[(m, sc, arm)]
                is2507 = m.endswith('2507')
                mk, ms = ('*', 7.5) if is2507 else ('o', 4.5)
                rr, ci_r = ebar(axr, XPOS[m] + off, x['catastrophe'], x['n_ok'], COL[arm], mk, ms)
                na = x['refuse'] + x['format_out']
                rn, ci_n = ebar(axn, XPOS[m] + off, na, x['n_ok'], COL[arm], mk, ms)
                vals1.append({'model': m, 'scenario': sc, 'arm': arm, 'n_ok': x['n_ok'], 'catastrophe': x['catastrophe'], 'refuse': x['refuse'], 'format_out': x['format_out'],
                              'other_answered': x['other_answered'], 'rate': rr, 'rate_wilson': ci_r, 'no_answer': na, 'no_answer_share': rn, 'no_answer_wilson': ci_n})
        for ax in (axr, axn):
            ax.set_ylim(-0.02, 1.02)
            ax.axvline(5.9, color='0.8', linewidth=0.8, linestyle=':')
            ax.tick_params(axis='y', labelsize=7)
        if blk == 0:
            axr.set_title('場面 %s' % sc, fontsize=10)
        if j == 0:
            head = '冷徹な戦略家の役の一行を\n含まない条件' if blk == 0 else '冷徹な戦略家の役の一行を\n含む条件'
            axr.set_ylabel(head + NL + RATE_LABEL, fontsize=7.2, labelpad=10)
            axn.set_ylabel(head + NL + NOANS_LABEL, fontsize=7.2, labelpad=10)
for ax in axes[3]:
    ax.set_xticks([XPOS[m] for m in MODELS])
    ax.set_xticklabels([XLAB[m] for m in MODELS], fontsize=7.2, rotation=35, ha='right')
    ax.set_xlim(-0.6, 7.4)
star = Line2D([0], [0], color='black', marker='*', markersize=9, markerfacecolor='white', markeredgecolor='black', linestyle='none', label='4B〔2507〕（Qwen3-4B-Instruct-2507・別の学ばせ方・点線の右）')
hA = [Line2D([0], [0], color=COL[a], marker='o', linestyle='none', label=a) for a in ARMS_A]
hB = [Line2D([0], [0], color=COL[a], marker='o', linestyle='none', label=a) for a in ARMS_B]
fig.legend(handles=hA, loc='lower left', ncol=5, fontsize=7.5, frameon=False, bbox_to_anchor=(0.07, 0.122), title='上の二段の条件（凡例は事前登録の並び）', title_fontsize=7.5)
fig.legend(handles=hB, loc='lower left', ncol=3, fontsize=7.5, frameon=False, bbox_to_anchor=(0.47, 0.122), title='下の二段の条件', title_fontsize=7.5)
fig.legend(handles=[star], loc='lower left', ncol=1, fontsize=7.5, frameon=False, bbox_to_anchor=(0.69, 0.122), title='4B〔2507〕の印（四つの段のどれも）', title_fontsize=7.5)   # v0.5: ★の見本を組の外に（3L-05）
fig.text(0.53, 0.103, '横軸: 機種（Qwen3 の稠密の系列）。並びは公開の機種の頁の名目の大きさの順で、間隔は大きさの量を表さない。目盛りの「Qwen3-4B」は稠密の系列の 4B。4B〔2507〕は並びの外（点線の右・別の印）。',
         ha='center', va='bottom', fontsize=7.8)
fig.suptitle('段階 A の本番の実行（Qwen3 の稠密の 6 機種と 4B〔Qwen3-4B-Instruct-2507〕× 5 場面・手元の推論）: 条件ごとの破局的選択の率と答えなかった割合（Wilson の 95% 区間）\n規模の効果を示す図ではない',
             fontsize=10.5)
NOTE1 = [
    '機種の安全さの比べとして読まない。図の上の差は段階 A の判定ではない（判定は段階 A の最終版にある）。登録の外の記述で、段階 E で事後に描いた図である。',
    '条件ごとの試行は 200 で、どのセルも応答の得られた試行は 200（拒否と書式外を分母に残す）。論文の三つ組（破局的選択・破局でない答え・答えなかった〔拒否と書式外を合わせた値〕）のうち二つを描く。'
    '破局でない答えの割合は、1 から二つを引いた値（四つの分け〔破局・拒否・書式外・ほかの答え〕の和は、どのセルでも応答の得られた試行と等しい）。',
    '灰色の帯は段階 A の検閲の閾値の外（0.05 未満・0.95 超）。帯の中の点と、段階 A の最終版が検閲や測定不能（段階 A の記録の言葉で、段階 D の計測不能とは別）として対比から外した規模の点は、率の比べとして読まない（付録 J.5 の (iii)）。点を線でつながない。',
    '描いた八つの条件は、段階 E の枠の決め（描く腕を名指す・段階 A の効き目の種の腕）により、段階 A の傾きの族の効き目の種に入る条件を選んだもので、傾きの検定を描いたものではない（O・Osec・Nk・Ncold・Nstr の五つは描いていない・値は段階 A の記録にある）。' + COLD,
    '機構の層の点は打たない。機構の層の値は、前置きではなく方向の加減という別の操作の下の値で、同じ軸に置くと操作の違う値を並べることになる（章 4）。',
]
fig.text(0.5, 0.012, NL.join(wrap(s, 112) for s in NOTE1), ha='center', va='bottom', fontsize=7.4, linespacing=1.35)
fig.subplots_adjust(left=0.095, right=0.99, top=0.925, bottom=0.21, hspace=0.12, wspace=0.08)
F1 = os.path.join(O1, 'fig-calc1-stageA-v0.5.png')
fig.savefig(F1, dpi=150)
plt.close(fig)
json.dump({'inputs': inputs, 'interim_check': {'file': 'summary/calc/calc-interim-v0.4.json', 'sha256': sha(open(os.path.join(PUB, 'summary', 'calc', 'calc-interim-v0.4.json'), 'rb').read()), 'rows_compared': cmp_rows, 'mismatch': 0},
           'arms_drawn': ARMS_A + ARMS_B, 'arms_not_drawn': NOT_DRAWN, 'rows': vals1}, open(os.path.join(O1, 'calc1-values-v0.5.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
# ---------------- 計算二
DP = os.path.join(PUB, 'records', 'pilotC', 'describe-pilotC.json')
db = open(DP, 'rb').read()
DJ = json.loads(db.decode('utf-8'))
os.makedirs(O2)
fig, axes = plt.subplots(2, 5, figsize=(14, 8.6), sharey=True, sharex=True)
vals2 = []
ARM2 = [('Onull', 'Onull', '#000000'), ('O', 'O', '#0072B2'), ('Onull-Ncold', 'Onull と冷徹な\n戦略家の役の一行', '#D55E00')]
ALL_ARMS = sorted({r['arm'] for r in DJ['rows']})
OTHER = [a for a in ALL_ARMS if a not in [x[0] for x in ARM2]]
dirs = sorted({DJ['runs'][s]['dir'] for s in SCENES})
dates = sorted({datetime.datetime.fromisoformat(DJ['runs'][s]['created']).astimezone(JST).strftime('%Y-%m-%d') for s in SCENES})
nset = set()
for j, sc in enumerate(SCENES):
    axr, axn = axes[0][j], axes[1][j]
    for k, (arm, lab, col) in enumerate(ARM2):
        r = [x for x in DJ['rows'] if x['scene'] == sc and x['arm'] == arm]
        assert len(r) == 1, (sc, arm)
        r = r[0]
        assert r['catastrophe'] + r['refuse'] + r['format_out'] <= r['n_ok']
        nset.add(r['n_ok'])
        rr, ci_r = ebar(axr, k, r['catastrophe'], r['n_ok'], col, 'o', 6)
        na = r['refuse'] + r['format_out']
        rn, ci_n = ebar(axn, k, na, r['n_ok'], col, 'o', 6)
        vals2.append({'scene': sc, 'arm': arm, 'n_ok': r['n_ok'], 'catastrophe': r['catastrophe'], 'refuse': r['refuse'], 'format_out': r['format_out'], 'rate': rr, 'rate_wilson': ci_r,
                      'no_answer': na, 'no_answer_share': rn, 'no_answer_wilson': ci_n})
    for ax in (axr, axn):
        ax.set_xlim(-0.6, 2.6)
        ax.set_ylim(-0.02, 1.02)
        ax.tick_params(axis='y', labelsize=7)
    axr.set_title('場面 %s' % sc, fontsize=10)
    axn.set_xticks([0, 1, 2])
    axn.set_xticklabels([x[1] for x in ARM2], fontsize=7.5)
axes[0][0].set_ylabel(RATE_LABEL, fontsize=8, labelpad=10)
axes[1][0].set_ylabel(NOANS_LABEL, fontsize=8, labelpad=10)
nlab = '・'.join(str(x) for x in sorted(nset))
fig.suptitle('段階 C の予備実験（Qwen3-4B-Instruct-2507・提供者 Nscale・%s の実行・条件ごとに 100 試行）: 破局的選択の率と答えなかった割合（Wilson の 95%% 区間）' % '・'.join(dates), fontsize=10.2)
NOTE2 = [
    '対称だった・対称でなかったとは読まない。段階 A の点と段階 C の予備実験の点を比べない（実行と経路が違う）。二つの向きの大きさを比べない。登録の外の予備実験の記述で、判定ラベルを付けない。',
    '予備実験の九つの条件のうち三つを描く（段階 E の枠の二つの決めによる・どちらも予備実験の値を見た後で、図を描く前に決めた・決めの記録は付録 H）。応答の得られた試行は条件ごとに %s（拒否と書式外を分母に残す・予備実験の記述で照らした）。'
    '破局でない答えの割合は、1 から破局的選択の率と答えなかった割合を引いた値。' % nlab,
    COLD2,
]
fig.text(0.5, 0.012, NL.join(wrap(s, 100) for s in NOTE2), ha='center', va='bottom', fontsize=7.8, linespacing=1.35)
fig.subplots_adjust(left=0.095, right=0.99, top=0.9, bottom=0.2, wspace=0.08, hspace=0.12)
F2 = os.path.join(O2, 'fig-calc2-pilotC-v0.5.png')
fig.savefig(F2, dpi=150)
plt.close(fig)
json.dump({'input': {'path': 'records/pilotC/describe-pilotC.json', 'sha256': sha(db)}, 'arms_drawn': [x[0] for x in ARM2], 'arms_not_drawn': OTHER, 'n_ok_values': sorted(nset), 'rows': vals2},
          open(os.path.join(O2, 'calc2-values-v0.5.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
me = sha(open(os.path.abspath(__file__), 'rb').read())
R = ['# 計算一と計算二の記録 v0.5（%s 日本時間・器 `E/E3/calc/calc1_2_scale_figures.py` v0.5・SHA16 %s）' % (now, me[:16]), '',
     '- 何か: 枠 §5 の計算一（規模の図）と計算二（段階 C の予備実験の 4B の点）を、二巡目の採否（2L-01・2L-02・2L-04〜2L-09）のとおり、図の字と見やすさだけ直して描き直した。入力・描く条件・値・区間は v0.3 と同じ。登録の外の記述で、判定ラベルを付けない。',
     '- 照らし: 中間総括の計算一の段階 A の行 %d を、同じ走りから計算した数と率に照らし、すべて合った。走りの記録の四つの分け（破局・拒否・書式外・ほかの答え）の和が応答の得られた試行と合うことと、描いた 280 のセルの応答の得られた試行がすべて 200 であることを、セルごとに照らした。'
     '段階 A の走りの記録の条件は十三（描いた八つと、描いていない %s）。' % (cmp_rows, '・'.join(NOT_DRAWN)),
     '- 計算二: 描いた条件は %s。描いていない条件は %s（段階 E の枠の決め・決定 D292・D425-5）。走りは %s（%s・日本時間の日付・Qwen3-4B-Instruct-2507・提供者 Nscale）。応答の得られた試行の値: %s。' % ('・'.join(x[0] for x in ARM2), '・'.join(OTHER), '・'.join(dirs), '・'.join(dates), nlab),
     '- v0.3 の出力（`E/E3/calc/calc1-v0.3/`・`E/E3/calc/calc2-v0.3/`）は、草案3 と二巡目の検分が使ったので残す。', '', '- 出力の SHA-256:']
for d in (O1, O2):
    for fn in sorted(os.listdir(d)):
        R.append('  - `%s` %s' % (os.path.relpath(os.path.join(d, fn), os.path.dirname(HERE)).replace(os.sep, '/'), sha(open(os.path.join(d, fn), 'rb').read())))
R += ['', CLAUSE, '']
open(os.path.join(O1, 'calc1-2-record-v0.5.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print(NL.join(R))
