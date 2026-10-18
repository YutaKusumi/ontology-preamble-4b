# -*- coding: utf-8 -*-
"""calc3_model_figures.py v0.5（2026-10-15・裁定 D460-3 の当て: 表の注の内部の記録の名を「付録 H」に替えた〔本文の章に差し込む表〕・その前の出力は見せる前に prev/calc3-v0.5-unshown-first/ へ移し、器の前の写しは prev/calc3_model_figures-v0.5-unshown-first.py・三巡目の採否の後: ‡ の注に分母と定めの節〔3I-08〕・表の注の「写した値」を検定の族の比べの行に限り照らしの記録の名を書く〔3I-06〕・中の区画の白抜きの六角と凡例と横軸の分母〔3I-10〕・右端の数の字〔3I-10〕・判定不能の × を区間の棒の少し上に〔3I-10〕・図の注に並べて読むことと並びの出所〔3I-20〕・記録に入力の SHA の行・入力と値は替えない・v0.4 は prev/calc3_model_figures-v0.4.py〔出力 calc3-v0.4/ は草案4 と三巡目の検分が使ったので残す〕）。
calc3_model_figures.py v0.4（2026-10-15・論文の草案3 の検分の二巡目の採否 2I-08・2I-15・2J-07・2J-12 と裁定 D453 の後: 題から登録の符号〔D1′・D1′E〕を外す〔画像で字形を見分けにくい〕・中の区画の印を灰色の六角にする〔判定不能の × と紛れない〕・中の区画の縦軸の名にも † と ‡ を付ける・右の区画の帯の右に答えなかった割合の数を添える・凡例の「答えなかった」に「（拒否と書式外）」を添える・注に比べの縦の並びと ‡ の定め〔本番の実行の Onull の率〕を書く・セルが 2 以下の機種の表の注に、値は同じ集計の出力から写した値で書式だけが違うことを書く・v0.4 の一度目の出力は、右の区画の凡例が右の端で切れたので、見せる前に `prev/calc3-v0.4-unshown-first/` へ移した・入力と値は替えない・v0.3 は `prev/calc3_model_figures-v0.3.py`〔出力 calc3-v0.3/ は草案3 と二巡目の検分が使ったので残す〕・以下は v0.3 の説明: 2026-10-14・v0.2 の出力は見せる前に prev/calc3-v0.2-unshown-first へ移した〔図の下の注の一行目が右の端で切れた〕・器は prev/calc3_model_figures-v0.2-unshown-first.py・v0.2: 一巡目の採否 F-03〜F-06 と裁定 D450・枠の追記二の後: 率の名と計測不能の名を追記二の論文の言葉にし、中の区画〔N と Onull の差〕の印を判定ラベルに使わない縦の棒にし、図の中の注に判定ラベルの決め方の順と ◇・白抜きの ○ の読み方を書き、表の差に＋の符号を付けて p を有効数字三桁の指数の形にそろえ、表に N と Onull の行と条件ごとの三つ組の表を足した・v0 は `prev/calc3_model_figures-v0.py`・v0 の出力 calc3/ は草案2 と一巡目が使ったので残す・枠 §5 の計算三〔段階 D の機種ごとの差の図・言語ごとに別の図・D425-4・EF1-17〕・登録の外の記述・コーディネータ南無弥勒如来）。
入力: 公開の二つの集計の出力（`records/D1p/confirm/confirm-D1p.json`・`records/D1pE/confirm/confirm-D1pE.json`）。読む前に、公開の置き場の SHA の記録（confirm-*-sha256.txt）と照らす。
描き方（枠 §5 の計算三のとおり）:
  - 機種ごとに一つの図（その機種の節にだけ置く）。セルが 2 以下の機種は図でなく表（D425-4）。
  - セルごとに「O と Onull」「OAmi と Onull」「OAmi と O」の差（全試行を分母とする破局的選択の率の差・a − b）と区間（集計の器の Newcombe の hybrid score の区間）と判定ラベル。
  - 差の軸はすべての機種で同じ（−1〜1）。判定ラベルは点の形で示し、判定保留・判定不能・計測不能は形を替える。
  - 腕ごとの三つ組（破局的選択・破局でない答え・答えなかった）を別の区画に描く。前置きの無い N と Onull の差（a − b・族の外の記述）を別の区画に置く。
  - 図の中に「区間は補正していない・判定ラベルは族の中の Holm で決めた」を書く。事前の結果への接触の印と、検出力の低いセルの印を付ける。
  - 英語の送る文の登録の図に日本語の送る文の登録の値を描かない（言語ごとに別の図・別の置き場）。族の水準の区間は描かない。
  - 色は比べの種類ごとの三色（値の良し悪しを思わせない色）で、点の形が判定ラベル。腕と比べの並びは凍結の並び（効き目の順にしない）。
書く物（一度だけ）: `E/E3/calc/calc3/<ja|en>/` の図（PNG）と表（Markdown）・`calc3-values-<ja|en>.json`（描いた値と出所）・`calc3-record.md`。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
OUT = os.path.join(HERE, 'calc3-v0.5')
SEC = {'ja': '節 6.1', 'en': '節 8.1'}   # v0.5: ‡ の定めの節（3I-08）
assert not os.path.exists(OUT), '一度だけ'
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
plt.rcParams['font.family'] = 'Noto Sans JP'
assert any(f.name == 'Noto Sans JP' for f in font_manager.fontManager.ttflist)
sha = lambda b: hashlib.sha256(b).hexdigest().upper()
SRC = {'ja': ('records/D1p/confirm/confirm-D1p.json', 'records/D1p/confirm/confirm-D1p-sha256.txt', '日本語の送る文の登録'),
       'en': ('records/D1pE/confirm/confirm-D1pE.json', 'records/D1pE/confirm/confirm-D1pE-sha256.txt', '英語の送る文の登録')}
NAMES = {'gemini25flash': 'Gemini 2.5 Flash', 'grok420nr': 'grok-4.20（非推論）', 'deepseekv32-a': 'DeepSeek V3.2', 'deepseekflash': 'deepseek-flash',
         'llama31-8b-n': 'Llama 3.1 8B Instruct', 'llama4scout': 'Llama-4-Scout-17B-16E-Instruct', 'mistrallarge3-m': 'Mistral Large 3（2512）',
         'kimik3-m': 'Kimi K3', 'qwen25coder32b-n': 'Qwen2.5-Coder-32B-Instruct', 'qwen38max-a': 'Qwen3.8 Max（0902）'}
COMPS = [('O', 'Onull', 'O と Onull', '#0072B2'), ('OAmi', 'Onull', 'OAmi と Onull', '#E69F00'), ('OAmi', 'O', 'OAmi と O', '#CC79A7')]
LABEL_STYLE = {'確証（下げた）': ('o', True), '確証（上げた）': ('^', True), '確かめられなかった': ('o', False), '判定保留（様式転位）': ('D', False),
               '判定不能（端）': ('x', True), '計器が読めない（様式崩壊）': ('s', False)}
PAPER_LABEL = {'確証（下げた）': '確証された低下', '確証（上げた）': '確証された上昇', '確かめられなかった': '確証されなかった', '判定保留（様式転位）': '判定保留（応答様式の変化）',
               '判定不能（端）': '判定不能（両条件が床か天井）', '計器が読めない（様式崩壊）': '応答の様式の崩れによる計測不能', '走っていない': '走っていない'}
ARMS = ['N', 'Onull', 'O', 'OAmi']
os.makedirs(OUT)
now = datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')
rec_rows = []
src_rows = []   # v0.5: 入力の SHA-256 を記録に書く（3I-06）
for lg, (rel, shafile, regname) in SRC.items():
    b = open(os.path.join(PUB, *rel.split('/')), 'rb').read()
    want = [l.split()[0].upper() for l in open(os.path.join(PUB, *shafile.split('/')), encoding='utf-8').read().split(NL) if l.strip() and rel.rsplit('/', 1)[1] in l]
    assert want and sha(b) == want[0], ('公開の SHA の記録と合わない', rel)
    J = json.loads(b.decode('utf-8'))
    rows = {(r['model'], r['scene'], r['arm_a'], r['arm_b']): r for r in J['family_P'] + J['family_A']}
    cells = list(J['describe'].keys())
    models = []
    for c in cells:
        if c.split('|')[0] not in models:
            models.append(c.split('|')[0])
    od = os.path.join(OUT, lg)
    os.makedirs(od)
    values = {'source': rel, 'source_sha256': sha(b), 'models': {}}
    src_rows.append((rel, shafile, sha(b)))
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
                assert cv['arms'][arm]['non_answer'] >= 0, (mk, sc, arm)
            mv['cells'][sc] = cv
        values['models'][mk] = mv
        title = '%s（%s）' % (NAMES[mk], regname)
        if len(scenes) <= 2:
            T = ['| セル（場面） | 比べ（a と b） | 差（a − b） | 95% 区間（補正なし） | p | 族の中の Holm の後の p | 判定ラベル |', '|---|---|---|---|---|---|---|']
            for sc in scenes:
                cv = mv['cells'][sc]
                mark = ('†' if cv['exposure'] else '') + ('‡' if cv['low_power'] else '')
                for c in cv['comparisons']:
                    if c['rd'] is None:
                        T.append('| %s%s | %s | — | — | — | — | %s |' % (sc, mark, c['comp'], PAPER_LABEL['走っていない']))
                    else:
                        T.append('| %s%s | %s | %+.3f | [%+.3f, %+.3f] | %.2e | %.2e | %s |' % (sc, mark, c['comp'], c['rd'], c['rd_ci'][0], c['rd_ci'][1], c['p'], c['p_holm'], PAPER_LABEL[c['label']]))
                nmo = cv['N_minus_Onull']
                T.append('| %s%s | N と Onull（検定の族の外の記述） | %+.3f | [%+.3f, %+.3f] | — | — | 判定ラベルなし |' % (sc, mark, nmo['rd'], nmo['rd_ci'][0], nmo['rd_ci'][1]))
            T += ['', '| セル（場面） | 条件 | 破局的選択 | 破局でない答え | 答えなかった（拒否と書式外） | 応答の得られた試行 |', '|---|---|---|---|---|---|']
            for sc in scenes:
                for arm in ARMS:
                    v = mv['cells'][sc]['arms'][arm]
                    T.append('| %s | %s | %d | %d | %d | %d |' % (sc, arm, v['catastrophe'], v['nc_answer'], v['non_answer'], v['n']))
            T += ['', '- 差は、応答の得られた試行を分母とする破局的選択の率の差（a − b）。区間は Newcombe の hybrid score の 95% で、多重性を補正していない。p は有効数字三桁。判定ラベルは、判定の前の門・族の中の Holm・応答様式の変化の決まりの順で決めた（節 2.3）。N と Onull の行は検定の族の外の記述で、判定ラベルを持たない。二つ目の表は条件ごとの三つ組の数（応答の得られた試行を分母）。† 事前の結果への接触の印。‡ 検出力の低いセルの印（本番の実行の Onull の率〔応答の得られた試行を分母〕が 0.15 未満・' + SEC[lg] + '）。検定の族の比べの行の差・区間・p・判定ラベルは、同じ節の最終版の表（引用）と同じ集計の出力（公開の置き場の集計の json・公開の SHA の記録と照らした）から写した値で、書式だけが違う（照らしの記録は付録 H）。N と Onull の行は、集計の出力の記述の値から組んだ。']
            open(os.path.join(od, 'table-%s.md' % mk), 'w', encoding='utf-8', newline=NL).write(NL.join(T) + NL)
            rec_rows.append((lg, mk, 'table', len(scenes)))
            continue
        nrow = len(scenes)
        fig = plt.figure(figsize=(11.5, 1.35 * nrow + 2.2))
        gs = fig.add_gridspec(1, 3, width_ratios=[3.2, 1.6, 2.2], wspace=0.35)
        ax, axn, axt = fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])
        ys = list(range(nrow))[::-1]
        for (a, bb, nm, col), off in zip(COMPS, (0.25, 0.0, -0.25)):
            for sc, y in zip(scenes, ys):
                c = [x for x in mv['cells'][sc]['comparisons'] if x['comp'] == nm][0]
                if c['rd'] is None:
                    ax.text(0, y + off, '走っていない', fontsize=7, ha='center', va='center')
                    continue
                mkr, filled = LABEL_STYLE[c['label']]
                ax.errorbar([c['rd']], [y + off], xerr=[[c['rd'] - c['rd_ci'][0]], [c['rd_ci'][1] - c['rd']]], fmt='none', ecolor=col, elinewidth=1.2, capsize=2)
                ax.plot([c['rd']], [y + off + (0.1 if mkr == 'x' else 0.0)], marker=mkr, markersize=7, color=col, markerfacecolor=(col if filled else 'white'), markeredgewidth=1.4, linestyle='none')   # v0.5: 判定不能の × は区間の棒の少し上に置く（3I-10）
        ax.axvline(0, color='0.6', linewidth=0.8)
        ax.set_xlim(-1, 1)
        ax.set_yticks(ys)
        ax.set_yticklabels(['%s%s' % (sc, ('†' if mv['cells'][sc]['exposure'] else '') + ('‡' if mv['cells'][sc]['low_power'] else '')) for sc in scenes])
        ax.set_ylim(-0.7, nrow - 0.3)
        ax.set_xlabel('破局的選択の率の差（a − b・応答の得られた試行を分母）')
        ax.set_title('比べ（a と b）の差と 95% 区間', fontsize=10)
        from matplotlib.lines import Line2D
        h1 = [Line2D([0], [0], color=col, marker='o', linestyle='none', label=nm) for _, _, nm, col in COMPS]
        h2 = [Line2D([0], [0], color='0.3', marker=LABEL_STYLE[k][0], markerfacecolor=('0.3' if LABEL_STYLE[k][1] else 'white'), linestyle='none', label=PAPER_LABEL[k]) for k in LABEL_STYLE]
        ax.legend(handles=h1 + h2, fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)
        for sc, y in zip(scenes, ys):
            nmo = mv['cells'][sc]['N_minus_Onull']
            axn.errorbar([nmo['rd']], [y], xerr=[[nmo['rd'] - nmo['rd_ci'][0]], [nmo['rd_ci'][1] - nmo['rd']]], fmt='none', ecolor='0.35', capsize=2)
            axn.plot([nmo['rd']], [y], marker='h', markersize=7, markeredgewidth=1.2, color='0.35', markerfacecolor='white', linestyle='none')   # v0.5: 白抜きの六角（3I-10）
        axn.axvline(0, color='0.6', linewidth=0.8)
        axn.set_xlim(-1, 1)
        axn.set_yticks(ys)
        axn.set_yticklabels(['%s%s' % (sc, ('†' if mv['cells'][sc]['exposure'] else '') + ('‡' if mv['cells'][sc]['low_power'] else '')) for sc in scenes])
        axn.set_ylim(-0.7, nrow - 0.3)
        axn.set_title('N と Onull の差（a − b）\n検定の族の外の記述・判定ラベルなし', fontsize=9)
        axn.set_xlabel('率の差（N − Onull）\n応答の得られた試行を分母', fontsize=8)   # v0.5: 分母を書く（3I-10）
        axn.legend(handles=[Line2D([0], [0], color='0.35', marker='h', markerfacecolor='white', markeredgewidth=1.2, linestyle='none', label='N と Onull の差（記述・判定ラベルなし）')], fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=1, frameon=False)   # v0.5: 凡例を足す（3I-10）
        yy, labels = [], []
        for sc, y in zip(scenes, ys):
            for k, arm in enumerate(ARMS):
                v = mv['cells'][sc]['arms'][arm]
                yv = y + 0.3 - 0.2 * k
                n = float(v['n'])
                axt.barh(yv, v['catastrophe'] / n, height=0.16, color='0.25')
                axt.barh(yv, v['nc_answer'] / n, left=v['catastrophe'] / n, height=0.16, color='0.75')
                axt.barh(yv, v['non_answer'] / n, left=(v['catastrophe'] + v['nc_answer']) / n, height=0.16, color='white', edgecolor='0.4', hatch='///', linewidth=0.5)
                axt.text(1.02, yv, '%.2f' % (v['non_answer'] / n), fontsize=6.8, va='center', ha='left', clip_on=False)   # v0.5: 字を大きく（3I-10）
                yy.append(yv)
                labels.append('%s %s' % (sc, arm))
        axt.set_yticks(yy)
        axt.set_yticklabels(labels, fontsize=6.5)
        axt.set_xlim(0, 1)
        axt.set_ylim(-0.7, nrow - 0.3)
        axt.set_title('条件ごとの三つ組（応答の得られた試行を分母）\n右の端の数は答えなかった割合', fontsize=9)
        axt.set_xlabel('割合')
        from matplotlib.patches import Patch
        axt.legend(handles=[Patch(color='0.25', label='破局的選択'), Patch(color='0.75', label='破局でない答え'), Patch(facecolor='white', edgecolor='0.4', hatch='///', label='答えなかった（拒否と書式外）')], fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)
        fig.suptitle(title, fontsize=11)
        fig.text(0.01, 0.005, '区間は Newcombe の hybrid score の 95% で、多重性を補正していない。判定ラベルは、判定の前の門・族の中の Holm・応答様式の変化の決まりの順で決めた。各セルの三つの比べは、上から「O と Onull」「OAmi と Onull」「OAmi と O」の順。\n判定保留は ◇、確証されなかった比べは白抜きの ○（補正しない区間が 0 を外れていても、Holm の後に確証されなかった比べを含む）。判定不能（両条件が床か天井）の × は、区間の棒と重ならないように棒の少し上に置いた。\n中の区画は判定ラベルを持たない記述（白抜きの灰色の六角）で、応答様式の変化の決まりを当てていない。三つの区画は並べて読む（中の区画の幅は左の区画の約半分で、同じ差が短く見える）。\n† 事前の結果への接触の印。‡ 検出力の低いセルの印（本番の実行の Onull の率〔応答の得られた試行を分母〕が 0.15 未満・' + SEC[lg] + '）。条件と比べの並びは、凍結した本文の機種の表と比べの並び（事前登録の並び）。', fontsize=7)
        fig.subplots_adjust(left=0.06, right=0.95, top=0.88, bottom=0.21 + 0.6 / (nrow + 1))   # v0.5: 注が一行増えた
        p = os.path.join(od, 'fig-%s.png' % mk)
        fig.savefig(p, dpi=150)
        plt.close(fig)
        rec_rows.append((lg, mk, 'figure', len(scenes)))
    json.dump(values, open(os.path.join(OUT, 'calc3-values-%s.json' % lg), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
me = sha(open(os.path.abspath(__file__), 'rb').read())
R = ['# 計算三の記録 v0.5（機種ごとの差の図・言語ごとに別・%s 日本時間・器 `E/E3/calc/calc3_model_figures.py` v0.5・SHA16 %s）' % (now, me[:16]), '',
     '- 何か: 枠 §5 の計算三。登録の外の記述で、判定ラベルを替えない。入力は公開の二つの集計の出力（公開の SHA の記録と照らした）。',
     '- 露出: 起草者は二つの集計の報告と最終版の値を前に見ている。図と表の値は集計の出力の値を写したもので、新しく計算した値は無い（三つ組の割合は数を割っただけ）。',
     '- v0.5 の直し（三巡目の採否 3I-06・3I-08・3I-10・3I-20）: 注と印と字の大きさと × の置き方だけで、入力・値・区間・判定ラベルは v0.4 と同じ。',
     '- 照らし: 入力の二つの集計の出力の SHA-256 を、公開の置き場の SHA の記録の行と照らした（合わなければ器が止まる）。'] + ['  - `%s` %s（照らした記録 `%s`）' % (r_, s_, f_) for r_, f_, s_ in src_rows] + ['',
     '| 言語の登録 | 機種 | 形 | セル |', '|---|---|---|---|']
for lg, mk, kind, n in rec_rows:
    R.append('| %s | %s | %s | %d |' % ({'ja': '日本語の送る文の登録', 'en': '英語の送る文の登録'}[lg], NAMES[mk], {'figure': '図', 'table': '表（セルが 2 以下・D425-4）'}[kind], n))
R += ['', '- 出力の SHA-256:']
for root, _, fs in sorted(os.walk(OUT)):
    for fn in sorted(fs):
        p = os.path.join(root, fn)
        R.append('  - `%s` %s' % (os.path.relpath(p, os.path.dirname(HERE)).replace(os.sep, '/'), sha(open(p, 'rb').read())))
R += ['', CLAUSE, '']
open(os.path.join(OUT, 'calc3-record.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print(NL.join(R[:20]))
