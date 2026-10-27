# -*- coding: utf-8 -*-
"""figs_en_v1.py v1（2026-10-27・英語の版の図〔図 3.1・図 3.2・章 6 と章 8 の機種ごとの図〕を描く器・裁定 D521-3 の (4)・D523・コーディネータ南無弥勒如来・内部）。
写したもの: 日本語の版の図の器 `E/E3/calc/calc1_2_scale_figures.py` v0.5 と `E/E3/calc/calc3_model_figures.py` v0.5 の入力・照らし・計算・描き方（区画・印・色・並び・値・区間）。日本語の版の器は替えない。
替えたもの（字だけ）: 図の中の日本語の字を、凍結した図の字の段の英語（`E/E5/ft/check/fixed/ft-1.md`・単位の番号で引く・凍結の記録 `E/E5/freeze/freeze-E5-en-ft-v1.json` の SHA と照らす）と、新しい訳の束の直した写しの英語（`E/E5/tm/back-tm/fixed/tm-1〜3.md`・同じ凍結の記録と照らす・用語の表で決まっている図の字 12）に替える。英語はこの器の中に打たない（単位の番号で引くだけ）。
  - 守る字（⟦n⟧）は、凍結した図の字の束 `E/E5/ft/bundles/ft-1.md` の「例:」の行（束を組む器が日本語の字から写した値）で埋める。器が埋める字（⟦F⟧）は、日本語の版の器と同じ値（場面の名・実行の日付・応答の得られた試行の数・節の指し）で埋める。
  - 字の形だけの替え: 〔〕→ [ ]（図の字の段の決まり）・機種の名の全角の括弧 → 半角の括弧と前の空き・並べの点「・」→「, 」・文と文の間の空き。
  - 二行に折る名（F101〜F103）は、語の切れ目のうち、字の幅のまん中に近い所で折る。注は語の切れ目で、測った幅（ポイント）で折り返し、下の余白を行の数に合わせて広げる（区画の大きさと並びは日本語の版のまま）。
  - 字体は日本語の版と同じ Noto Sans JP（英字と ◇・○・×・†・‡ を含む）。
照らし: (1) 描いた値（区間を含む）を、日本語の版の値の記録（`E/E3/calc/calc1-v0.5/calc1-values-v0.5.json`・`calc2-v0.5/calc2-values-v0.5.json`・`calc3-v0.5/calc3-values-<ja|en>.json`）と一つずつ照らす（一つでも違えば止まる）。(2) 図に描く字に日本語の字と ⟦ ⟧ の印が残っていないことを照らす。(3) 図の数は日本語の版と同じ（図 3.1・図 3.2・機種ごとの図 9）。
用法: python figs_en_v1.py <書く置き場（無い所）>
書く物（一度だけ）: <置き場>/calc1/fig-calc1-stageA-en.png・calc2/fig-calc2-pilotC-en.png・calc3/<ja|en>/fig-<機種>.png・値の json・`figs-en-record.md`（字の出所の表・入力と出力の SHA-256）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, math, glob, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib import font_manager
from matplotlib.textpath import TextToPath
from matplotlib.font_manager import FontProperties
HERE = os.path.dirname(os.path.abspath(__file__))
E5 = os.path.dirname(HERE)
INT = os.path.dirname(os.path.dirname(E5))
CALC = os.path.join(INT, 'E', 'E3', 'calc')
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
TOOL = 'figs_en_v1.py v1'
assert len(sys.argv) == 2, '用法: python figs_en_v1.py <書く置き場>'
OUT = os.path.abspath(sys.argv[1])
assert not os.path.exists(OUT), ('一度だけ', OUT)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
plt.rcParams['font.family'] = 'Noto Sans JP'
assert any(f.name == 'Noto Sans JP' for f in font_manager.fontManager.ttflist)
sha = lambda b: hashlib.sha256(b).hexdigest().upper()
shaf = lambda p: sha(open(p, 'rb').read())
JA = re.compile(r'[぀-ヿ㐀-鿿々]')
UNIT = re.compile(r'^@@ ([FNT]\d{3,4}) @@\s*$')
Z = 1.959963984540054

# ---- 字の出所（凍結の記録と照らす）
FZ = json.load(open(os.path.join(E5, 'freeze', 'freeze-E5-en-ft-v1.json'), encoding='utf-8'))
FTP = os.path.join(E5, 'ft', 'check', 'fixed', 'ft-1.md')
TMP = [os.path.join(E5, 'tm', 'back-tm', 'fixed', 'tm-%d.md' % k) for k in (1, 2, 3)]
BNP = os.path.join(E5, 'ft', 'bundles', 'ft-1.md')
rel = lambda p: os.path.relpath(p, INT).replace(os.sep, '/')
for p in [FTP] + TMP:
    assert FZ['frozen'][rel(p)] == shaf(p), ('凍結の記録と違う', rel(p))
assert FZ['basis'][rel(BNP)] == shaf(BNP), ('凍結の記録と違う', rel(BNP))


def units_of(path):
    d, cur = {}, None
    for l in open(path, encoding='utf-8').read().split(NL):
        m = UNIT.match(l)
        if m:
            cur = m.group(1)
            continue
        if l.startswith('=== '):
            cur = None
            continue
        if cur and l.strip():
            assert cur not in d, ('一つの単位に二行', cur)
            d[cur] = l
    return d


FT = units_of(FTP)
assert len(FT) == 47
TM = {}
for p in TMP:
    TM.update(units_of(p))
# 守る字（⟦n⟧）の値: 束の「例:」の行から（⟦F⟧ の例は使わない）
TOK = {}
cur = None
for l in open(BNP, encoding='utf-8').read().split(NL):
    m = UNIT.match(l)
    if m:
        cur = m.group(1)
        continue
    if cur and l.startswith('例: '):
        pairs = re.findall(r'⟦(\d+)⟧ = ([^・]+)', l[len('例: '):])
        TOK[cur] = [v.strip() for k, v in sorted(pairs, key=lambda kv: int(kv[0]))]
USED = []   # 字の出所の表


def ft(uid, toks=None, F=None):
    s = FT[uid]
    n = len(re.findall(r'⟦\d+⟧', s))
    toks = TOK.get(uid, []) if toks is None else toks
    assert n == len(toks), ('守る字の数が合わない', uid, n, toks)
    for i, v in enumerate(toks, 1):
        assert s.count('⟦%d⟧' % i) == 1, (uid, i)
        s = s.replace('⟦%d⟧' % i, v)
    F = F or []
    assert s.count('⟦F⟧') == len(F), ('器が埋める字の数が合わない', uid)
    for v in F:
        s = s.replace('⟦F⟧', v, 1)
    assert '⟦' not in s and not JA.search(s), ('字が残った', uid, s)
    USED.append((uid, 'ft', s))
    return s


def tm(tid, toks=()):
    s = TM[tid]
    for i, v in enumerate(toks, 1):
        assert s.count('⟦%d⟧' % i) == 1, (tid, i)
        s = s.replace('⟦%d⟧' % i, v)
    assert '⟦' not in s and not JA.search(s), ('字が残った', tid, s)
    USED.append((tid, 'tm', s))
    return s


# ---- 測った幅で折る
T2P = TextToPath()


def width_pt(s, size):
    w, h, d = T2P.get_text_width_height_descent(s, FontProperties(family='Noto Sans JP', size=size), ismath=False)
    return w


def wrap_pt(s, size, maxw):
    out, cur = [], ''
    for w in s.split(' '):
        t = (cur + ' ' + w) if cur else w
        if cur and width_pt(t, size) > maxw:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def split2(s, size):
    ws = s.split(' ')
    best = None
    for i in range(1, len(ws)):
        a, b = ' '.join(ws[:i]), ' '.join(ws[i:])
        if a.count('"') % 2:   # 引用符の中では折らない
            continue
        d = abs(width_pt(a, size) - width_pt(b, size))
        if best is None or d < best[0]:
            best = (d, a + NL + b)
    return best[1]


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


def same(a, b):
    if isinstance(a, float) or isinstance(b, float):
        return (isinstance(a, (int, float)) and isinstance(b, (int, float)) and (a == b or (a != a and b != b) or abs(a - b) < 1e-12))
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    return a == b


now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
os.makedirs(OUT)
# ---- 英語の字（日本語の版の器の同じ名の字に当たる）
RATE_LABEL = ft('F001') + NL + ft('F002')
NOANS_LABEL = ft('F003') + NL + ft('F004')
COLD_BASE = ft('F005')
COLD = COLD_BASE + ' ' + ft('F006')
COLD2 = COLD_BASE + ' ' + ft('F007')
B2507 = '4B [2507]'   # 日本語の版の目盛りの「4B〔2507〕」の〔〕を [ ] に（図の字の段の決まり・F016 と F019 の英語と同じ形）
assert B2507 in ft('F016') and B2507 in ft('F019')

# ---------------- 図 3.1（計算一）
SCENES = ['N1', 'N2', 'S1', 'S4', 'SK']
MODELS = ['Qwen/Qwen3-0.6B', 'Qwen/Qwen3-1.7B', 'Qwen/Qwen3-4B', 'Qwen/Qwen3-8B', 'Qwen/Qwen3-14B', 'Qwen/Qwen3-32B', 'Qwen/Qwen3-4B-Instruct-2507']
XPOS = {'Qwen/Qwen3-0.6B': 0, 'Qwen/Qwen3-1.7B': 1, 'Qwen/Qwen3-4B': 2, 'Qwen/Qwen3-8B': 3, 'Qwen/Qwen3-14B': 4, 'Qwen/Qwen3-32B': 5, 'Qwen/Qwen3-4B-Instruct-2507': 6.8}
XLAB = {'Qwen/Qwen3-0.6B': '0.6B', 'Qwen/Qwen3-1.7B': '1.7B', 'Qwen/Qwen3-4B': 'Qwen3-4B', 'Qwen/Qwen3-8B': '8B', 'Qwen/Qwen3-14B': '14B', 'Qwen/Qwen3-32B': '32B', 'Qwen/Qwen3-4B-Instruct-2507': B2507}
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
assert all(tri[(m, s, a)]['n_ok'] == 200 for m in MODELS for s in SCENES for a in ARMS_A + ARMS_B)
O1 = os.path.join(OUT, 'calc1')
os.makedirs(O1)
# 下の字の高さ（インチ）: 日本語の版の図は高さ 14.2・上 0.925・下 0.21。区画の高さとの間は同じに保ち、下に足りない分だけ図を高くする
NOTE1 = [ft('F011'), ft('F012'), ft('F013'), ft('F020') + ' ' + COLD, ft('F014')]
N1_SIZE, N1_W = 7.4, 829.0     # 日本語の版の注の折り返しの幅（112 字 × 7.4 ポイント）
note1_lines = [l for s in NOTE1 for l in wrap_pt(s, N1_SIZE, N1_W)]
X1_SIZE, X1_W = 7.8, 1100.0
x1_lines = wrap_pt(ft('F008'), X1_SIZE, X1_W)
note_h = len(note1_lines) * N1_SIZE * 1.35 / 72.0
x1_h = len(x1_lines) * X1_SIZE * 1.3 / 72.0
JA_H, JA_TOP, JA_BOT = 14.2, 0.925, 0.21
plot_h = JA_H * (JA_TOP - JA_BOT)
top_in = JA_H * (1 - JA_TOP)
pad, gap = 0.17, 0.12
legend_in = 0.62                 # 凡例の三つの組（題と一行）の高さの見込み
ticks_in = 0.55                  # 斜めの目盛りの字の高さの見込み
bottom_in = pad + note_h + gap + x1_h + gap + legend_in + ticks_in
H1 = top_in + plot_h + bottom_in
fig, axes = plt.subplots(4, 5, figsize=(16, H1), sharex=True, sharey=True)
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
            axr.set_title(ft('F026', F=[sc]), fontsize=10)
        if j == 0:
            head = split2(ft('F102'), 7.2) if blk == 0 else split2(ft('F103'), 7.2)
            axr.set_ylabel(head + NL + RATE_LABEL, fontsize=7.2, labelpad=10)
            axn.set_ylabel(head + NL + NOANS_LABEL, fontsize=7.2, labelpad=10)
for ax in axes[3]:
    ax.set_xticks([XPOS[m] for m in MODELS])
    ax.set_xticklabels([XLAB[m] for m in MODELS], fontsize=7.2, rotation=35, ha='right')
    ax.set_xlim(-0.6, 7.4)
leg_y = (pad + note_h + gap + x1_h + gap) / H1
star = Line2D([0], [0], color='black', marker='*', markersize=9, markerfacecolor='white', markeredgecolor='black', linestyle='none', label=ft('F016'))
hA = [Line2D([0], [0], color=COL[a], marker='o', linestyle='none', label=a) for a in ARMS_A]
hB = [Line2D([0], [0], color=COL[a], marker='o', linestyle='none', label=a) for a in ARMS_B]
fig.legend(handles=hA, loc='lower left', ncol=5, fontsize=7.5, frameon=False, bbox_to_anchor=(0.07, leg_y), title=ft('F017'), title_fontsize=7.5)
fig.legend(handles=hB, loc='lower left', ncol=3, fontsize=7.5, frameon=False, bbox_to_anchor=(0.43, leg_y), title=ft('F018'), title_fontsize=7.5)
fig.legend(handles=[star], loc='lower left', ncol=1, fontsize=7.5, frameon=False, bbox_to_anchor=(0.63, leg_y), title=ft('F019'), title_fontsize=7.5)
fig.text(0.53, (pad + note_h + gap) / H1, NL.join(x1_lines), ha='center', va='bottom', fontsize=X1_SIZE, linespacing=1.3)
fig.suptitle(ft('F009') + NL + ft('F010'), fontsize=10.5)
fig.text(0.5, pad / H1, NL.join(note1_lines), ha='center', va='bottom', fontsize=N1_SIZE, linespacing=1.35)
fig.subplots_adjust(left=0.095, right=0.99, top=1 - top_in / H1, bottom=bottom_in / H1, hspace=0.12, wspace=0.08)
F1 = os.path.join(O1, 'fig-calc1-stageA-en.png')
fig.savefig(F1, dpi=150)
plt.close(fig)
JV1 = json.load(open(os.path.join(CALC, 'calc1-v0.5', 'calc1-values-v0.5.json'), encoding='utf-8'))
v1j = json.loads(json.dumps(vals1))
assert same(v1j, JV1['rows']), '図 3.1 の値が日本語の版と違う'
assert [x['sha256'] for x in inputs] == [x['sha256'] for x in JV1['inputs']], '図 3.1 の入力が日本語の版と違う'
json.dump({'inputs': inputs, 'same_as_ja_values': 'E/E3/calc/calc1-v0.5/calc1-values-v0.5.json', 'rows': vals1}, open(os.path.join(O1, 'calc1-values-en.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
# ---------------- 図 3.2（計算二）
DP = os.path.join(PUB, 'records', 'pilotC', 'describe-pilotC.json')
db = open(DP, 'rb').read()
DJ = json.loads(db.decode('utf-8'))
O2 = os.path.join(OUT, 'calc2')
os.makedirs(O2)
ARM2 = [('Onull', 'Onull', '#000000'), ('O', 'O', '#0072B2'), ('Onull-Ncold', split2(ft('F101'), 7.5), '#D55E00')]
dates = sorted({datetime.datetime.fromisoformat(DJ['runs'][s]['created']).astimezone(JST).strftime('%Y-%m-%d') for s in SCENES})
nset = set()
for sc in SCENES:
    for arm, _, _ in ARM2:
        r = [x for x in DJ['rows'] if x['scene'] == sc and x['arm'] == arm]
        assert len(r) == 1
        nset.add(r[0]['n_ok'])
nlab = ', '.join(str(x) for x in sorted(nset))
NOTE2 = [ft('F015'), ft('F025', F=[nlab]), COLD2]
N2_SIZE, N2_W = 7.8, 780.0     # 日本語の版の注の折り返しの幅（100 字 × 7.8 ポイント）
note2_lines = [l for s in NOTE2 for l in wrap_pt(s, N2_SIZE, N2_W)]
note2_h = len(note2_lines) * N2_SIZE * 1.35 / 72.0
JA2_H, JA2_TOP, JA2_BOT = 8.6, 0.9, 0.2
plot2_h = JA2_H * (JA2_TOP - JA2_BOT)
top2_in = JA2_H * (1 - JA2_TOP)
bottom2_in = pad + note2_h + gap + 0.62    # 目盛りの字（二行に折った名）の高さの見込み
H2 = top2_in + plot2_h + bottom2_in
fig, axes = plt.subplots(2, 5, figsize=(14, H2), sharey=True, sharex=True)
vals2 = []
for j, sc in enumerate(SCENES):
    axr, axn = axes[0][j], axes[1][j]
    for k, (arm, lab, col) in enumerate(ARM2):
        r = [x for x in DJ['rows'] if x['scene'] == sc and x['arm'] == arm][0]
        assert r['catastrophe'] + r['refuse'] + r['format_out'] <= r['n_ok']
        rr, ci_r = ebar(axr, k, r['catastrophe'], r['n_ok'], col, 'o', 6)
        na = r['refuse'] + r['format_out']
        rn, ci_n = ebar(axn, k, na, r['n_ok'], col, 'o', 6)
        vals2.append({'scene': sc, 'arm': arm, 'n_ok': r['n_ok'], 'catastrophe': r['catastrophe'], 'refuse': r['refuse'], 'format_out': r['format_out'], 'rate': rr, 'rate_wilson': ci_r,
                      'no_answer': na, 'no_answer_share': rn, 'no_answer_wilson': ci_n})
    for ax in (axr, axn):
        ax.set_xlim(-0.6, 2.6)
        ax.set_ylim(-0.02, 1.02)
        ax.tick_params(axis='y', labelsize=7)
    axr.set_title(ft('F026', F=[sc]), fontsize=10)
    axn.set_xticks([0, 1, 2])
    axn.set_xticklabels([x[1] for x in ARM2], fontsize=7.5)
axes[0][0].set_ylabel(RATE_LABEL, fontsize=8, labelpad=10)
axes[1][0].set_ylabel(NOANS_LABEL, fontsize=8, labelpad=10)
fig.suptitle(ft('F024', F=[', '.join(dates)]), fontsize=10.2)
fig.text(0.5, pad / H2, NL.join(note2_lines), ha='center', va='bottom', fontsize=N2_SIZE, linespacing=1.35)
fig.subplots_adjust(left=0.095, right=0.99, top=1 - top2_in / H2, bottom=bottom2_in / H2, wspace=0.08, hspace=0.12)
F2 = os.path.join(O2, 'fig-calc2-pilotC-en.png')
fig.savefig(F2, dpi=150)
plt.close(fig)
JV2 = json.load(open(os.path.join(CALC, 'calc2-v0.5', 'calc2-values-v0.5.json'), encoding='utf-8'))
assert same(json.loads(json.dumps(vals2)), JV2['rows']), '図 3.2 の値が日本語の版と違う'
assert JV2['input']['sha256'] == sha(db), '図 3.2 の入力が日本語の版と違う'
json.dump({'input': {'path': 'records/pilotC/describe-pilotC.json', 'sha256': sha(db)}, 'same_as_ja_values': 'E/E3/calc/calc2-v0.5/calc2-values-v0.5.json', 'rows': vals2},
          open(os.path.join(O2, 'calc2-values-en.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
# ---------------- 章 6・章 8 の機種ごとの図（計算三）
SEC = {'ja': ft('F030', toks=['6.1']), 'en': ft('F030', toks=['8.1'])}   # 日本語の版の器の SEC（節 6.1・節 8.1）
SRC = {'ja': ('records/D1p/confirm/confirm-D1p.json', 'records/D1p/confirm/confirm-D1p-sha256.txt', ft('F045')),
       'en': ('records/D1pE/confirm/confirm-D1pE.json', 'records/D1pE/confirm/confirm-D1pE-sha256.txt', ft('F046'))}
NAMES = {'gemini25flash': 'Gemini 2.5 Flash', 'grok420nr': tm('T0038', ('4.20',)), 'deepseekv32-a': 'DeepSeek V3.2', 'deepseekflash': 'deepseek-flash',
         'llama31-8b-n': 'Llama 3.1 8B Instruct', 'llama4scout': 'Llama-4-Scout-17B-16E-Instruct', 'mistrallarge3-m': 'Mistral Large 3 (2512)',
         'kimik3-m': 'Kimi K3', 'qwen25coder32b-n': 'Qwen2.5-Coder-32B-Instruct', 'qwen38max-a': 'Qwen3.8 Max (0902)'}
COMPS = [('O', 'Onull', tm('T0011'), '#0072B2'), ('OAmi', 'Onull', tm('T0013'), '#E69F00'), ('OAmi', 'O', tm('T0014'), '#CC79A7')]
COMP_JA = {'O と Onull': COMPS[0][2], 'OAmi と Onull': COMPS[1][2], 'OAmi と O': COMPS[2][2]}
LABEL_STYLE = {'確証（下げた）': ('o', True), '確証（上げた）': ('^', True), '確かめられなかった': ('o', False), '判定保留（様式転位）': ('D', False),
               '判定不能（端）': ('x', True), '計器が読めない（様式崩壊）': ('s', False)}
PAPER_LABEL = {'確証（下げた）': tm('T0012'), '確証（上げた）': tm('T0025'), '確かめられなかった': tm('T0017'), '判定保留（様式転位）': tm('T0044'),
               '判定不能（端）': tm('T0028'), '計器が読めない（様式崩壊）': ft('F044'), '走っていない': ft('F038')}
ARMS = ['N', 'Onull', 'O', 'OAmi']
O3 = os.path.join(OUT, 'calc3')
os.makedirs(O3)
JV3 = {lg: json.load(open(os.path.join(CALC, 'calc3-v0.5', 'calc3-values-%s.json' % lg), encoding='utf-8')) for lg in ('ja', 'en')}
rec_rows, src_rows = [], []
for lg, (rl, shafile, regname) in SRC.items():
    b = open(os.path.join(PUB, *rl.split('/')), 'rb').read()
    want = [l.split()[0].upper() for l in open(os.path.join(PUB, *shafile.split('/')), encoding='utf-8').read().split(NL) if l.strip() and rl.rsplit('/', 1)[1] in l]
    assert want and sha(b) == want[0], ('公開の SHA の記録と合わない', rl)
    J = json.loads(b.decode('utf-8'))
    rows = {(r['model'], r['scene'], r['arm_a'], r['arm_b']): r for r in J['family_P'] + J['family_A']}
    cells = list(J['describe'].keys())
    models = []
    for c in cells:
        if c.split('|')[0] not in models:
            models.append(c.split('|')[0])
    od = os.path.join(O3, lg)
    os.makedirs(od)
    values = {'source': rl, 'source_sha256': sha(b), 'models': {}}
    src_rows.append((rl, shafile, sha(b)))
    for mk in models:
        mc = [c for c in cells if c.startswith(mk + '|')]
        scenes = [c.split('|')[1] for c in mc]
        mv = {'cells': {}}
        for sc in scenes:
            d = J['describe'][mk + '|' + sc]
            cv = {'comparisons': [], 'arms': {}, 'N_minus_Onull': d['N_minus_Onull'], 'exposure': bool(J['exposure_marks'].get(mk + '|' + sc)), 'low_power': (mk + '|' + sc) in J['low_onull_cells']}
            for a, bb, nm, col in COMPS:
                r = rows.get((mk, sc, a, bb))
                cv['comparisons'].append({'comp': nm, 'rd': r['rd'] if r else None, 'rd_ci': r['rd_ci'] if r else None, 'p': r['p'] if r else None, 'p_holm': r['p_holm'] if r else None, 'label': r['label'] if r else '走っていない'})
            for arm in ARMS:
                x = d['arms'][arm]
                n = x['n_trials']
                cv['arms'][arm] = {'n': n, 'catastrophe': x['catastrophe'], 'nc_answer': x['nc_answer'], 'non_answer': n - x['catastrophe'] - x['nc_answer']}
                assert cv['arms'][arm]['non_answer'] >= 0
            mv['cells'][sc] = cv
        values['models'][mk] = mv
        # 日本語の版の値と照らす（比べの名だけ日本語の版の名に戻して）
        jm = JV3[lg]['models'][mk]
        for sc in scenes:
            a_ = json.loads(json.dumps(mv['cells'][sc]))
            for c in a_['comparisons']:
                c['comp'] = [k for k, v in COMP_JA.items() if v == c['comp']][0]
            assert same(a_, jm['cells'][sc]), ('機種ごとの図の値が日本語の版と違う', lg, mk, sc)
        if len(scenes) <= 2:
            rec_rows.append((lg, mk, 'table（英語の版では組み立ての器が新しい訳の束で組む）', len(scenes)))
            continue
        title = '%s (%s)' % (NAMES[mk], regname)
        nrow = len(scenes)
        NOTE3 = [ft('F060'), ft('F061'), ft('F062'), ft('F104', F=[SEC[lg]])]
        N3_SIZE, N3_W = 7.0, 800.0
        note3_lines = [l for s in NOTE3 for l in wrap_pt(s, N3_SIZE, N3_W)]
        note3_h = len(note3_lines) * N3_SIZE * 1.3 / 72.0
        JA3_H = 1.35 * nrow + 2.2
        JA3_BOT = 0.21 + 0.6 / (nrow + 1)
        ja_note_h = 4 * 7.0 * 1.3 / 72.0
        plot3_h = JA3_H * (0.88 - JA3_BOT)
        top3_in = JA3_H * (1 - 0.88)
        bottom3_in = JA3_H * JA3_BOT - ja_note_h + note3_h + 0.25
        H3 = top3_in + plot3_h + bottom3_in
        fig = plt.figure(figsize=(11.5, H3))
        gs = fig.add_gridspec(1, 3, width_ratios=[3.2, 1.6, 2.2], wspace=0.35)
        ax, axn, axt = fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])
        ys = list(range(nrow))[::-1]
        for (a, bb, nm, col), off in zip(COMPS, (0.25, 0.0, -0.25)):
            for sc, y in zip(scenes, ys):
                c = [x for x in mv['cells'][sc]['comparisons'] if x['comp'] == nm][0]
                if c['rd'] is None:
                    ax.text(0, y + off, PAPER_LABEL['走っていない'], fontsize=7, ha='center', va='center')
                    continue
                mkr, filled = LABEL_STYLE[c['label']]
                ax.errorbar([c['rd']], [y + off], xerr=[[c['rd'] - c['rd_ci'][0]], [c['rd_ci'][1] - c['rd']]], fmt='none', ecolor=col, elinewidth=1.2, capsize=2)
                ax.plot([c['rd']], [y + off + (0.1 if mkr == 'x' else 0.0)], marker=mkr, markersize=7, color=col, markerfacecolor=(col if filled else 'white'), markeredgewidth=1.4, linestyle='none')
        ax.axvline(0, color='0.6', linewidth=0.8)
        ax.set_xlim(-1, 1)
        ax.set_yticks(ys)
        ax.set_yticklabels(['%s%s' % (sc, ('†' if mv['cells'][sc]['exposure'] else '') + ('‡' if mv['cells'][sc]['low_power'] else '')) for sc in scenes])
        ax.set_ylim(-0.7, nrow - 0.3)
        ax.set_xlabel(ft('F050'))
        ax.set_title(ft('F051'), fontsize=10)
        h1 = [Line2D([0], [0], color=col, marker='o', linestyle='none', label=nm) for _, _, nm, col in COMPS]
        h2 = [Line2D([0], [0], color='0.3', marker=LABEL_STYLE[k][0], markerfacecolor=('0.3' if LABEL_STYLE[k][1] else 'white'), linestyle='none', label=PAPER_LABEL[k]) for k in LABEL_STYLE]
        ax.legend(handles=h1 + h2, fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)
        for sc, y in zip(scenes, ys):
            nmo = mv['cells'][sc]['N_minus_Onull']
            axn.errorbar([nmo['rd']], [y], xerr=[[nmo['rd'] - nmo['rd_ci'][0]], [nmo['rd_ci'][1] - nmo['rd']]], fmt='none', ecolor='0.35', capsize=2)
            axn.plot([nmo['rd']], [y], marker='h', markersize=7, markeredgewidth=1.2, color='0.35', markerfacecolor='white', linestyle='none')
        axn.axvline(0, color='0.6', linewidth=0.8)
        axn.set_xlim(-1, 1)
        axn.set_yticks(ys)
        axn.set_yticklabels(['%s%s' % (sc, ('†' if mv['cells'][sc]['exposure'] else '') + ('‡' if mv['cells'][sc]['low_power'] else '')) for sc in scenes])
        axn.set_ylim(-0.7, nrow - 0.3)
        axn.set_title(ft('F052') + NL + ft('F053'), fontsize=9)
        axn.set_xlabel(ft('F054') + NL + ft('F055'), fontsize=8)
        axn.legend(handles=[Line2D([0], [0], color='0.35', marker='h', markerfacecolor='white', markeredgewidth=1.2, linestyle='none', label=ft('F064'))], fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=1, frameon=False)
        yy, labels = [], []
        for sc, y in zip(scenes, ys):
            for k, arm in enumerate(ARMS):
                v = mv['cells'][sc]['arms'][arm]
                yv = y + 0.3 - 0.2 * k
                n = float(v['n'])
                axt.barh(yv, v['catastrophe'] / n, height=0.16, color='0.25')
                axt.barh(yv, v['nc_answer'] / n, left=v['catastrophe'] / n, height=0.16, color='0.75')
                axt.barh(yv, v['non_answer'] / n, left=(v['catastrophe'] + v['nc_answer']) / n, height=0.16, color='white', edgecolor='0.4', hatch='///', linewidth=0.5)
                axt.text(1.02, yv, '%.2f' % (v['non_answer'] / n), fontsize=6.8, va='center', ha='left', clip_on=False)
                yy.append(yv)
                labels.append('%s %s' % (sc, arm))
        axt.set_yticks(yy)
        axt.set_yticklabels(labels, fontsize=6.5)
        axt.set_xlim(0, 1)
        axt.set_ylim(-0.7, nrow - 0.3)
        axt.set_title(ft('F056') + NL + ft('F057'), fontsize=9)
        axt.set_xlabel(ft('F058'))
        axt.legend(handles=[Patch(color='0.25', label=tm('T0019')), Patch(color='0.75', label=tm('T0020')), Patch(facecolor='white', edgecolor='0.4', hatch='///', label=tm('T0021'))], fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)
        fig.suptitle(title, fontsize=11)
        fig.text(0.01, 0.06 / H3, NL.join(note3_lines), fontsize=N3_SIZE, va='bottom', linespacing=1.3)
        fig.subplots_adjust(left=0.06, right=0.95, top=1 - top3_in / H3, bottom=bottom3_in / H3)
        p = os.path.join(od, 'fig-%s.png' % mk)
        fig.savefig(p, dpi=150)
        plt.close(fig)
        rec_rows.append((lg, mk, 'figure', len(scenes)))
    json.dump(values, open(os.path.join(O3, 'calc3-values-%s.json' % lg), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
nfig = sum(1 for r in rec_rows if r[2] == 'figure')
assert nfig == 9, nfig
# 図に描いた字に日本語の字が無いこと（ft と tm の関数が一つずつ照らした・ここでは数だけ）
assert all(not JA.search(s) for _, _, s in USED)
me = shaf(os.path.abspath(__file__))
R = ['# 英語の版の図の記録 v1（%s 日本時間・器 `E/E5/figs/figs_en_v1.py`・SHA16 %s）' % (now, me[:16]), '',
     '- 何か: 日本語の版の図（図 3.1・図 3.2・章 6 と章 8 の機種ごとの図 9）の英語の版。入力・照らし・計算・描き方は日本語の版の器（`E/E3/calc/calc1_2_scale_figures.py` v0.5・`calc3_model_figures.py` v0.5）のまま、字だけを凍結した英語に替えた（裁定 D521-3・D522-1・D523）。',
     '- 値の照らし: 描いた値を日本語の版の値の記録と一つずつ照らし、すべて同じだった（図 3.1 の %d 行・図 3.2 の %d 行・機種ごとの図と表の全セル）。' % (len(vals1), len(vals2)),
     '- 字の出所: 図の字の段の凍結した英語 `E/E5/ft/check/fixed/ft-1.md`（SHA-256 %s）と、新しい訳の束の直した写し `E/E5/tm/back-tm/fixed/tm-1〜3.md`（凍結の記録 `E/E5/freeze/freeze-E5-en-ft-v1.json` と照らした）。守る字の値は束 `E/E5/ft/bundles/ft-1.md` の「例:」の行から。' % shaf(FTP),
     '- 字の形だけの替え（英語は打っていない）: 目盛りの「4B〔2507〕」→ "%s"・機種の名の全角の括弧 → 半角・並べの点「・」→「, 」・文と文の間の空き・二行に折る名は語の切れ目で折った。' % B2507,
     '- 字体: Noto Sans JP（日本語の版と同じ）。', '',
     '## 字の出所の表（使った順・同じ単位は一度だけ）', '', '| 単位 | 出所 | 図に描いた英語 |', '|---|---|---|']
seen = set()
for uid, kind, s in USED:
    if (uid, s) in seen:
        continue
    seen.add((uid, s))
    R.append('| %s | %s | %s |' % (uid, {'ft': '図の字の段', 'tm': '新しい訳の束'}[kind], s.replace('|', '｜').replace(NL, ' / ')))
R += ['', '## 機種ごとの図と表', '', '| 言語の登録 | 機種 | 形 | セル |', '|---|---|---|---|']
for lg, mk, kind, n in rec_rows:
    R.append('| %s | %s | %s | %d |' % (lg, mk, kind, n))
R += ['', '## 入力の SHA-256', '']
R += ['- `%s` %s' % (x['path'], x['sha256']) for x in inputs]
R += ['- `records/pilotC/describe-pilotC.json` %s' % sha(db)]
R += ['- `%s` %s（照らした記録 `%s`）' % (r_, s_, f_) for r_, f_, s_ in src_rows]
R += ['', '## 出力の SHA-256', '']
for root, _, fs in sorted(os.walk(OUT)):
    for fn in sorted(fs):
        p = os.path.join(root, fn)
        R.append('- `%s` %s' % (os.path.relpath(p, OUT).replace(os.sep, '/'), shaf(p)))
R += ['', CLAUSE, '']
open(os.path.join(OUT, 'figs-en-record.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print(json.dumps({'out': OUT, 'figures': nfig + 2, 'rows1': len(vals1), 'rows2': len(vals2), 'H1': round(H1, 2), 'H2': round(H2, 2), 'note1_lines': len(note1_lines), 'note2_lines': len(note2_lines), 'x1_lines': len(x1_lines)}, ensure_ascii=False))
