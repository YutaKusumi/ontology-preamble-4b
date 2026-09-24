# -*- coding: utf-8 -*-
"""build_report_Blens_devBL3.py v2 —— B-lens の報告の草案の二つ目と最終版（逸脱 D-BL3・登録者裁定 D191・D193／v2 は最終検分の後・登録者裁定 D196 の案・2026-09-24）。

凍結した組み立ての器 `tools/build_report_Blens.py` を読み込み、同じ入力で凍結の報告を作り直して、置き場の `records/Blens/results-Blens.md` とバイトで同じことを
確かめてから、見出しと状態の行を改め、【逸脱 D-BL3】（と事後の計算の【逸脱 D-BL4・事後】）の印を付けた機械の区画を足す。凍結の報告の文と区画は一字も変えない。
足す区画は、結果の巡・第一巡の採否表（`records/reviews/Blens/results-round1/adoption-table-Blens-results-r1.md`・区分（三））のとおり:
  器の同定と費用（P567・P568）・範囲と門の数（P584・P586・P588）・型の文の添え（P585）・唯一の札の文脈（P575・P576）・調整走行の読み方（P594）・
  大きさの目盛りの添え（P580・P581・P589・P590・P591・P599）・事後の計算（P582・P583・D-BL4）・§4 の数え上げと注と感度の集合と兄弟・八腕・対の距離（P577・P578・P592・P600）・
  §6 の注（P593）・§7 の狙いと零にした感度（P579・P595）・直した照合の表と注（P572〜P574）・§9 の添えと限界と正誤（P570・P587・P596・P597）・草案の検分票（P598）。
v2（最終検分の採否表 `records/reviews/Blens/results-final/adoption-table-Blens-results-final.md` の区分（三）の行・P605〜P609）: `--final` で最終版を組む。草案の二つ目に、
  §0 の §1 への参照（P605）・§8 の一致の注（P606）・§3 の表の並べ直し（P607）・§8 の登録者の予想のファイルの時刻の注（P608）・§9 の門の限界の句（P609）を足し、
  見出し・状態・冒頭の添え・検分票を最終版のものにする。最終版では、草案の二つ目を同じ走りで作り直して置き場のファイルと同じことを確かめ、
  草案の二つ目から消えた行（改めた行）が、決めた行だけであることを確かめる。`--final` が無ければ、出力は v1 と同じ（草案の二つ目）。
  出力が既にあって --force が無ければ、組んだ文を置き場のファイルと比べ、同じなら何も書かずに終わり、違えば止める。
v3（起草者の最終の見直し `records/reviews/Blens/results-final/final-read/review-final-Blens.md` の所見・登録者裁定 D198 の案）: `--final` の出力だけを改める。
  状態の行を機械の区画に移す（F-A: 登録者最終確認の記録 `records/Blens/final-confirmation-Blens.json` があれば、確認の逐語と時刻を書き、無ければ「登録者最終確認の前」と書く）・
  冒頭に凍結の後の逸脱の一覧（台帳から読む）と、検分票に D-BL2 の一句（F-B）・§3 の二つの行の言い回し（F-C・F-C2）・検分票の区画の頭の添え（F-D）・
  §3 の並べ直しの表の見出しの理由の句（F-E・任意）・§0 の〈門を通らない〉の添え（F-F・任意）。草案の二つ目の出力は v1・v2 と同じ。
数はすべて記録から器が読む。走査は凍結した組み立ての器の `lint_report`（凍結した走査器 `report_lint.lint` と、読みの表から作った禁止語）で行い、違反があれば止める。
出力: records/Blens/results-Blens-draft2.md（`--final` では results-Blens-FINAL-2026-09-24.md）と、同じ名の -machine.json・-lint.md。
用法: python tools/build_report_Blens_devBL3.py [--final] [--colab-dir <相 extract の出力の置き場>] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, math, difflib, hashlib, argparse, itertools, statistics, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import build_report_Blens as BR
import report_lint as RL
import make_predictions_form_Blens as FORM
import blens_core as C
import blens_lens as BL
import blens_calib as BC

VERSION = 'v3'
NL = chr(10)
OUT = os.path.join(REPO, 'records', 'Blens', 'results-Blens-draft2.md')
OUT_FINAL = os.path.join(REPO, 'records', 'Blens', 'results-Blens-FINAL-2026-09-24.md')
FINAL_REL = 'records/Blens/results-Blens-FINAL-2026-09-24.md'
CONFIRM = os.path.join(REPO, 'records', 'Blens', 'final-confirmation-Blens.json')     # v3: 登録者最終確認の記録（あれば状態の区画に逐語を書く）
REVIEW = 'records/reviews/Blens/results-final/final-read/review-final-Blens.md'
OPT_E, OPT_F = True, True                                                                # v3: 起草者の最終の見直しの任意の二つ（裁定 D198 で選ぶ）
POST = os.path.join(REPO, 'results', 'Blens', 'posthoc-Blens.json')
UNITS = os.path.join(REPO, 'records', 'Blens', 'colab-units-Blens.json')
FRJ = os.path.join(REPO, 'records', 'Blens', 'FREEZE-RECORD-Blens.json')
EXPO = os.path.join(REPO, 'records', 'Blens', 'sealing-exposures-Blens.md')
EXT = os.path.join(REPO, 'results', 'Blens', 'extract', 'extract-20260923T233625Z')
f4 = BR.f4
P_ = lambda *p: os.path.join(REPO, *p)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
TAG, TAG4 = '【逸脱 D-BL3】', '【逸脱 D-BL4・事後】'
PRIM = collections.OrderedDict([('M_L_survival', 'M_L_survival'), ('M_L_nuclear', 'M_L_nuclear'), ('M_X_survival', 'M_X_survival'), ('M_X_nuclear', 'M_X_nuclear'), ('M_F', 'M_F'), ('M_E', 'M_E_static')])
SW = {'O~Osec', 'O~Osec-Ncold', 'Osec~O-Ncold', 'O-Ncold~Osec-Ncold'}
E_OWN = {'static': 'M_E_static', 'loaded': 'M_E_static', 'Nk': 'M_E_Nk', 'td': 'M_E_td'}
NA = '該当なし（札が付かない）'


def binom_upper(n, p, k):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def set_size(SJ, mark):
    """一覧の印の名（E_static_plus・F_main・X_survival_a など）から、集合の語の数。"""
    parts = mark.split('_')
    node = SJ['sets'].get(parts[0])
    for q in parts[1:]:
        if isinstance(node, dict) and q in node:
            node = node[q]
        else:
            return None
    return 1 if isinstance(node, int) else (len(node) if isinstance(node, list) else None)


def blocks_of(lines, MB):
    out, i = [], 0
    while i < len(lines):
        if lines[i] == MB['begin']:
            j = lines.index(MB['end'], i)
            out.append((i, j, lines[i + 1] if i + 1 < j else ''))
            i = j + 1
        else:
            i += 1
    return out


def exposure_times():
    """露出の記録（`records/Blens/sealing-exposures-Blens.md`・機械生成）の表から、登録者に伝わった二つの露出の時刻と、登録者の予想のファイルの更新の時刻を読む（v2・P608）。"""
    rows = [l for l in open(EXPO, encoding='utf-8').read().replace('\r\n', NL).split(NL) if l.startswith('| ') and not l.startswith('| 時刻')]

    def t_of(key):
        hit = [l for l in rows if key in l]
        if len(hit) != 1:
            raise SystemExit('露出の記録に「%s」の行が %d（止める）' % (key, len(hit)))
        m = re.match(r'\| (?:\d{4}-\d{2}-\d{2} )?(\d{2}:\d{2}) \| コーディネータ → 登録者 \| ', hit[0])
        if not m:
            raise SystemExit('露出の記録の「%s」の行の時刻か向きが想定と違う（止める）' % key)
        return m.group(1)
    t_cal, t_pred = t_of('較正の検査の確率（無操作の模型'), t_of('コーディネータの予想の一部')
    sv = sorted(set(m for l in rows for m in re.findall(r'ファイルの更新 (\d{2}:\d{2})', l)))
    if len(sv) != 1:
        raise SystemExit('露出の記録の、登録者の予想のファイルの更新の時刻が一つでない（止める）: %s' % sv)
    if not t_cal < t_pred < sv[0]:
        raise SystemExit('露出の時刻の順が想定と違う（止める）: %s・%s・%s' % (t_cal, t_pred, sv[0]))
    return t_cal, t_pred, sv[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--final', action='store_true')
    ap.add_argument('--colab-dir', default=EXT)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    TL = json.load(open(P_('design', 'contrasts-Blens.json'), encoding='utf-8'))
    BL.require_sealed(TL)
    out = OUT_FINAL if a.final else OUT
    lens = json.load(open(BL.OUT, encoding='utf-8'))
    calib = json.load(open(BC.OUT, encoding='utf-8'))
    SJ = json.load(open(BL.SETS, encoding='utf-8'))
    seal = json.load(open(BL.SEAL, encoding='utf-8'))
    preds = {r: json.load(open(P_(*v['path'].split('/')), encoding='utf-8')) for r, v in seal['predictions'].items()}
    meta = {'canon': BR.sha16f(P_('design', 'contrasts-Blens.json')), 'sets': BR.sha16f(BL.SETS), 'seal': BR.sha16f(BL.SEAL), 'lens': BR.sha16f(BL.OUT), 'calib': BR.sha16f(BC.OUT)}
    frozen = BR.build(TL, lens, calib, SJ, seal, preds, meta)
    if frozen != open(BR.OUT, encoding='utf-8').read().replace('\r\n', NL):
        raise SystemExit('凍結した器で作り直した報告が、置き場の報告と違う（止める）')
    PH, UJ, FR = json.load(open(POST, encoding='utf-8')), json.load(open(UNITS, encoding='utf-8')), json.load(open(FRJ, encoding='utf-8'))
    CK = json.load(open(os.path.join(a.colab_dir, 'check.json'), encoding='utf-8'))
    H = np.load(os.path.join(a.colab_dir, 'h.npz'))
    MB = RL.machine_block(TL)
    sel = lens['primary']['ratio']
    lay = lens['layers'][sel]
    P = lens['primary']['metrics']
    g = calib['gates']
    changed = {}                                       # 最終版で改める草案の二つ目の行（v2・器の確かめに使う）

    def compose(final):
        ins = {}                                       # 足す区画: 凍結の区画の添字 → 行の並び

        # ---- 器の同定と費用
        used = ['tools/blens_core.py', 'tools/blens_lens.py', 'tools/blens_calib.py', 'tools/colab/boot_Blens.py', 'tools/steer_B.py', 'tools/run_stageB_local.py', 'tools/build_report_Blens.py', 'tools/report_lint.py']
        same = [(r, s16(P_(*r.split('/')))) for r in used]
        if any(FR['frozen_sha16'].get(r) != h for r, h in same):
            raise SystemExit('計算に使った器が凍結の記録の値と違う（止める）: %s' % [r for r, h in same if FR['frozen_sha16'].get(r) != h])
        st = {x['step']: x['used'] for x in UJ['steps']}
        head_draft = (TAG + 'この草案は、凍結した組み立ての器 `tools/build_report_Blens.py`（SHA16 %s）の出力を同じ入力で作り直し、置き場の `records/Blens/results-Blens.md`（SHA16 %s）とバイトで同じことを確かめてから、'
                      '見出しと状態の行を改め、%sと%sの印の区画だけを足したもの（組み立ての器 `tools/build_report_Blens_devBL3.py`・登録者裁定 D191・D193）。印の無い文と区画は凍結の器の出力のまま。'
                      % (s16(BR.__file__), s16(BR.OUT), TAG, TAG4))
        head_final = (TAG + 'この最終版は、凍結した組み立ての器 `tools/build_report_Blens.py`（SHA16 %s）の出力を同じ入力で作り直し、置き場の `records/Blens/results-Blens.md`（SHA16 %s）とバイトで同じことを確かめてから、'
                      '見出しと状態の行を改め、%sと%sの印の区画だけを足したもの（組み立ての器 `tools/build_report_Blens_devBL3.py` %s・登録者裁定 D191・D193・D196・D198）。印の無い文と区画は凍結の器の出力のまま。'
                      % (s16(BR.__file__), s16(BR.OUT), TAG, TAG4, VERSION))
        changed['head'] = '- ' + head_draft
        ins[0] = [head_final if final else head_draft,
                  '- 上の行の封印の記録の SHA16 は `records/Blens/sealing-record-Blens.json` のもの。',
                  '- 計算に使った器の SHA16 は凍結の記録の値と同じ: %s。凍結の後に改めた器は封印の器 `tools/seal_Blens.py`（逸脱 D-BL1・計算には使わない）。事後の計算の器は `tools/posthoc_Blens.py`（逸脱 D-BL4）。'
                  % '・'.join('`%s` %s' % (r, h) for r, h in same),
                  MB['cost_line_tag'] + ' Colab のユニット %.2f（%s・登録者の表示から）。手元の計算はユニットを使わない。' % (UJ['total_used'], '・'.join('%s %.2f' % (k, v) for k, v in st.items()))]
        ins[0][0] = '- ' + ins[0][0]
        if final:
            opt = ('・〈門を通らない〉の添え' if OPT_F else '', '（見出しに理由の句）' if OPT_E else '')
            ins[0][1:1] = ['- %s最終版で草案の二つ目（`records/Blens/results-Blens-draft2.md`・SHA16 %s）に足した行と句は、最終検分の二票の所見（採否表 `records/reviews/Blens/results-final/adoption-table-Blens-results-final.md` の P605〜P609・'
                           '登録者裁定 D195・D196）と、起草者の最終の見直しの所見（`%s`・登録者裁定 D198）によるもの: 状態の区画・凍結の後の逸脱の一覧・§0 の §1 への参照%s・§3 の表の並べ直し%s・'
                           '§8 の一致の注と登録者の予想のファイルの時刻の注・§9 の門の限界の句・検分票の区画の頭の添え。ほかに改めたのは、見出し・状態の行・この冒頭の添え・§3 の答えの文字の位置の二つの行の言い回し・検分票だけで、'
                           'ほかの行は草案の二つ目と同じ（器が確かめた）。' % (TAG, s16(OUT), REVIEW, opt[0], opt[1])]
            FRD = FR['deviations']
            ttl = lambda d: re.search(r'\*\*([^*]+)\*\*', d['what']).group(1) + ('（更新あり）' if d.get('updates') else '')
            ins[0].insert(4, '- %s凍結の後の逸脱（台帳 `records/Blens/FREEZE-RECORD-Blens.md`）: %s。' % (TAG, '・'.join('%s %s' % (d['no'], ttl(d)) for d in FRD)))

        # ---- 範囲と門の数
        ins[2] = ['- %s範囲: 上の札の分類と、下の読みの型の〈区別できない〉は、v̂・層の割合 %s・主の六つの物差しについてのもの。ほかの方向・層・物差し（§4）には札を付けない。' % (TAG, sel),
                  '- %s門の数: 本の門 M_L 順位相関 %s・割合 %s（Holm の第一段 %s）・M_X 割合 %s（第一段で止まったので試されていない）／v̂ を抜いた門 M_L 割合 %s・M_X 割合 %s／v̂ と (6b) を抜いた門（記述）M_L 割合 %s・M_X 割合 %s。'
                  % (TAG, f4(g['full']['M_L']['rho']), f4(g['full']['M_L']['p']), f4(g['full']['M_L']['holm_step']), f4(g['full']['M_X']['p']), f4(g['without_vhat']['M_L']['p']), f4(g['without_vhat']['M_X']['p']),
                     f4(g['without_vhat_loaded']['M_L']['p']), f4(g['without_vhat_loaded']['M_X']['p'])),
                  '- %s門の読みの添え: 凍結した基準では、物差しと行動の変化がそろうことは示せなかった。そろわないことを示したのではない（門の検出力は低い・§9 の限界の文）。段の近くの値を、惜しいとも逆の側とも読まない。' % TAG]

        # ---- 型の文の添え
        rk = []
        for m, x in P.items():
            d = x['second_detail']
            rk.append('%s %s' % (m, ('語の側の帰無の割合 %s' % f4(d['word_side_p'])) if 'word_side_p' in d else ('%d／%d' % (d['rank'], d['of']))))
        ins[3] = ['- %s〈二つ目の札だけ〉（M_L_nuclear）の括弧の中で当たるのは「比べる相手の中では最も大きい」の句だけ（「語の側の帰無の外」は M_E のときの句）。' % TAG,
                  '- %s各物差しの、実在の差の中の順位（M_E は語の側の帰無の割合・正本 `reading_notes`）: %s。' % (TAG, '・'.join(rk))]
        if final:                                      # P605
            ins[3].append('- %sM_L_nuclear の二つ目の札を読むための並び（兄弟の三対・比べる相手の |値| の最大と中央値・等方の標準偏差・ランダム方向が実在の差の最上位に来た升目の数・物差しごとの比）は、'
                          '§1 の添えにある。この札は、この要約の行だけで読まない。' % TAG)
            if OPT_F:                                  # v3・F-F
                ins[3].append('- %s〈門を通らない〉の「そろわなかった」は、凍結した基準でそろうことが示せなかったという意味で、そろわないことを示したのではない（上の門の読みの添え）。' % TAG)

        # ---- 唯一の札の文脈
        comp = {m: [abs(v[PRIM[m]]) for p, v in lay['real'].items() if p not in SW] for m in PRIM}
        mx = max(((p, abs(v['M_L_nuclear'])) for p, v in lay['real'].items() if p not in SW), key=lambda t: t[1])
        vabs = abs(P['M_L_nuclear']['value'])
        cells = tops = 0
        for r in lens['layers']:
            for u, dd in lens['layers'][r]['directions'].items():
                if 'rand' in u:
                    for m in ('M_L_survival', 'M_L_nuclear', 'M_X_survival', 'M_X_nuclear', 'M_Lc', 'M_R_survival', 'M_F', 'M_F_sens', 'M_E_static'):
                        if m in dd and 'real_rank' in dd[m]:
                            cells += 1
                            tops += 1 if dd[m]['real_rank']['top'] else 0
        of_r = lay['directions']['rand:0']['M_F']['real_rank']['of']
        ratio = {m: statistics.median(comp[m]) / lay['iso_sd'][PRIM[m]]['sampled'] for m in PRIM}
        ins[5] = ['- %s唯一の札（M_L_nuclear の二つ目の札）を読むための並び（札の判定は変えない）:' % TAG,
                  '  - 兄弟の三対（比べる相手から除いた対・正本 `nulls.real.rule`）の M_L_nuclear: %s。v̂ の |値| %s。' % ('・'.join('%s %s' % (p, f4(v['M_L_nuclear'])) for p, v in lay['siblings']['static'].items()), f4(vabs)),
                  '  - 比べる相手 %d 組の |値|: 最大 %s %s（v̂ との差 %.1f%%）・中央値 %s。等方の標準偏差 抽選 %s・解析 %s。' % (len(comp['M_L_nuclear']), mx[0], f4(mx[1]), 100 * (1 - mx[1] / vabs), f4(statistics.median(comp['M_L_nuclear'])),
                                                                                        f4(lay['iso_sd']['M_L_nuclear']['sampled']), f4(lay['iso_sd']['M_L_nuclear']['analytic'])),
                  '  - M_L_survival は実在の差の中の順位 %d／%d で、二つ目の札は付かない。' % (P['M_L_survival']['second_detail']['rank'], P['M_L_survival']['second_detail']['of']),
                  '  - ランダム方向が実在の差の最上位に来た升目（§4）: %d のうち %d（比べる相手と交換可能なら %.2f）。' % (cells, tops, cells / of_r),
                  '  - 選んだ層の、比べる相手の |値| の中央値 ÷ 等方の標準偏差（抽選）: %s。一より小さい物差しでは、実在の差は等方の方向の揺れより小さい側に集まる。' % '・'.join('%s %.2f' % (m, v) for m, v in ratio.items())]

        # ---- 門の表の添え（Holm の第二段・調整走行の読み方）
        base = [0, 1, 2, 3]
        hi = sum(1 for p in itertools.permutations(base) if C.spearman(base, list(p)) >= 0.8 - 1e-12)
        ntot = math.factorial(4)
        pr = collections.OrderedDict()
        for t in calib.get('tune', []):
            for m in TL['calibration']['tests']:
                pr.setdefault(m, collections.OrderedDict()).setdefault('%s@%s' % (t['scenario'], t['layer']), set()).add(t[m]['vhat_rank_push'])
        if any(len(v) != 1 for d_ in pr.values() for v in d_.values()):
            raise SystemExit('調整走行の押しの順位が係数で変わる（止める）')
        ins[7] = ['- %sHolm の段の欄: 本の門と v̂ を抜いた門の M_X の段は、第一段で止まったので試されていない。' % TAG,
                  '- %s調整走行の行の読み方: 順位は大きい順（1 が最大）。同じ場面と層では、物差しの値が係数に依らないので、係数の三つの行は押しの順位を共有する（行は独立でない）。方向 4 本では、組の中の順位相関が 0.8 以上になる並べ替えが %d／%d ある。'
                  '選んだ組（層 %s・係数 %s）は調整走行の行動から選ばれたので、その組の v̂ の行動の順位には選定が入る。' % (TAG, hi, ntot, sel, f4(TL['layers']['coef_applied'])),
                  '- %s場面と層ごとの v̂ の押しの順位（係数の行を一つに数える）: %s。' % (TAG, '／'.join('%s %s' % (m, '・'.join('%s %d' % (k, list(v)[0]) for k, v in d_.items())) for m, d_ in pr.items()))]

        # ---- 大きさの目盛りの添え
        mg = calib['magnitude']
        el = [x for x in mg['main_rows'] if x['eligible']]
        zero = [x['row'] for x in el if x['pT_before'] == 0 and x['pT_after'] == 0]
        nz = [x['row'] for x in el if x['row'] not in zero]
        pc = mg['colab_check']['calibration']['S4|Osec-Ncold|json']['main']
        loc = [x for x in el if x['row'].startswith('S4|Osec-Ncold')][0]['pT_before']
        zc = (pc['k'] - pc['n'] * pc['p_T']) / math.sqrt(pc['n'] * pc['p_T'] * (1 - pc['p_T']))
        applied = re.findall(r'「([^」]*)」', TL['magnitude']['reading'])[0]
        first = collections.OrderedDict()
        for k, c in enumerate(CK['contexts']):
            first.setdefault('%s|%s' % (c['scenario'], c['arm']), []).append(k)
        spread = []
        for key, idx in first.items():
            h0 = np.asarray(H['h_main'][idx[0]], dtype=np.float64)
            sp = max(float(np.max(np.abs(np.asarray(H['h_main'][k], dtype=np.float64) - h0))) for k in idx)
            spread.append('%s %s（%s）' % (key, f4(sp), f4(sp / float(np.max(np.abs(h0))))))
        rows5 = []
        if final:                                      # P607: 凍結の器の出力の表を写し、行の名の縦棒だけを字にする（列と値は変えない）
            fl = frozen.split(NL)
            hd = [i for i, l in enumerate(fl) if l.startswith('| 行 | z | 観測の変化 |')]
            if len(hd) != 1:
                raise SystemExit('凍結の報告の大きさの目盛りの表の見出しが一つでない（止める）')
            ncol = fl[hd[0]].count('|')
            names, tb, i_ = [x['row'] for x in el], [fl[hd[0]], fl[hd[0] + 1]], hd[0] + 2
            while i_ < len(fl) and fl[i_].startswith('| '):
                nm = [n for n in names if fl[i_].startswith('| %s | ' % n)]
                if len(nm) != 1:
                    raise SystemExit('凍結の報告の大きさの目盛りの表の行の名が想定と違う（止める）: %s' % fl[i_][:40])
                esc = '| %s | ' % nm[0].replace('|', '\\|') + fl[i_][len('| %s | ' % nm[0]):]
                if esc.replace('\\|', '').count('|') != ncol:
                    raise SystemExit('並べ直した行の列の数が見出しと違う（止める）: %s' % nm[0])
                tb.append(esc)
                names.remove(nm[0])
                i_ += 1
            if names:
                raise SystemExit('凍結の報告の大きさの目盛りの表に無い行がある（止める）: %s' % names)
            why = '行の名の縦棒が表の区切りと重なって列がずれるので、縦棒' if OPT_E else '行の名の縦棒'     # v3・F-E
            rows5 += ['- %s上の凍結の表の並べ直し（%sを字として書いた・列と値は凍結の器の出力の表のまま）:' % (TAG, why), ''] + tb
        rows5 += ['- %s土台の確率の二つの値: 上の表の変換の後の確率（前）は、Colab の相 extract の残差から手元で組み直した出口の値から出した（S4|Osec-Ncold %s）。較正の検査の確率（%s）は、Colab の模型そのものの出口の値から出した。'
                  '組み直しの差は、手元の logits の突き合わせの最大 %s（許容 %s）の内。比は、同じ組み直しの前と後の差から出している。' % (TAG, f4(loc), f4(pc['p_T']), f4(mg['logit_check_local']['main']['max_abs']), f4(TL['magnitude']['logit_check']['atol'])),
                  '- %s較正の検査の位置（S4|Osec-Ncold|json）: 確率 %s のもとで観測 %d 件以上の割合 %s（z %.2f）。区間 %d〜%d の上端から %d 件内側で「内」。' % (
                      TAG, f4(pc['p_T']), pc['k'], f4(binom_upper(pc['n'], pc['p_T'], pc['k'])), zc, pc['interval'][0], pc['interval'][1], pc['interval'][1] - pc['k']),
                  '- %s比を出した %d 行の内訳: 切り詰めの外で、変換の後の確率が前も後も零の行 %d（%s）・比が出た行 %d（%s）。' % (TAG, len(el), len(zero), '・'.join(zero), len(nz), '・'.join(nz)),
                  '- %s当てた読みの文（%d 行とも読みの比に満たない）: %s。' % (TAG, sum(1 for x in el if x['reading'] == '満たない'), applied),
                  '', '| 行 | 「```」の出口の値の正確な変化 | 層一の近似の部分 | 最終の残差に沿う部分 | 尺度の部分 | 方向と最終の残差の余弦 |', '|---|---|---|---|---|---|']
        rows5 += ['| %s | %s | %s | %s | %s | %s |' % (x['row'].replace('|', '\\|'), f4(x['parts_fmain']['exact']), f4(x['parts_fmain']['layer1']), f4(x['parts_fmain']['along']), f4(x['parts_fmain']['scale']), f4(x['cos_u_h'])) for x in el]
        rows5 += ['- %s上の凍結の表の行の名には縦棒が入っていて表の区切りと重なるので、表示では列がずれる（凍結の器の出力のまま）。この区画と事後の区画の表では、縦棒を字として書いた。' % TAG]
        heads_d = '- %s答えの文字の位置の升目の出力の数と、異なる文の頭の数（%s）: %s。上の表の「文脈」の数は出力の数（S4|Osec-Ncold は、出力が同じ並びで、文脈は一つ）。' % (
            TAG, TAG4, '・'.join('%s 出力 %d・異なる文の頭 %d' % (k, v['n_outputs'], v['distinct_heads']) for k, v in PH['distinct_heads'].items()))
        lhead_d = '- %s答えの文字の位置の、正確な直接の経路による出口の値の変化（記述・散文の層は写しの位置・v̂ の行は平均と中央値と四分位、ほかの行は平均）:' % TAG
        heads_f = heads_d.replace('上の表の「文脈」の数は出力の数', '上の凍結の区画の答えの文字の位置の行の「文脈」の数は出力の数')    # v3・F-C
        lhead_f = lhead_d.replace('散文の層は写しの位置', '散文の升目は写しの位置')                                        # v3・F-C2
        if heads_f == heads_d or lhead_f == lhead_d:
            raise SystemExit('§3 の二つの行の言い回しの直しが当たらない（止める）')
        changed['heads'], changed['lhead'] = heads_d, lhead_d
        rows5 += ['- %s升目の中の主位置の残差の揺れ（同じ升目の出力の、一件目との要素ごとの差の絶対値の最大・括弧は一件目の残差の要素の絶対値の最大に対する割合）: %s。入力の長さの違いによる bf16 の丸めと見ている。大きさの目盛りは、升目ごとに一件目の残差を使う。'
                  % (TAG, '・'.join(spread)),
                  heads_f if final else heads_d,
                  lhead_f if final else lhead_d]
        st_ = lambda d: '平均 %s（中央値 %s・四分位 %s〜%s）' % (f4(d['mean']), f4(d['median']), f4(d['q1']), f4(d['q3']))
        for key, v in mg['letter'].items():
            parts = []
            for rname, rv in v['rows'].items():
                if rname.endswith('|static'):
                    parts.append('%s: a %s・c %s' % (rname, st_(rv['dlogit_exact_a']), st_(rv['dlogit_exact_c'])))
                else:
                    parts.append('%s: a %s・c %s' % (rname, f4(rv['dlogit_exact_a']['mean']), f4(rv['dlogit_exact_c']['mean'])))
            rows5.append('  - %s: %s' % (key, '／'.join(parts)))
        ins[9] = rows5
        rows4 = ['- %s主位置の生の全語彙の softmax の「```」の確率（温度も切り詰めも掛けない・札と読みの比は変えない・登録者裁定 D192）:' % TAG4, '',
                 '| 行 | 生の確率（前→後） | 生の確率の変化 | 変換の後の確率（前→後） | 観測の変化 |', '|---|---|---|---|---|']
        rows4 += ['| %s | %s→%s | %s | %s→%s | %s |' % (x['row'].replace('|', '\\|'), f4(x['raw_before']), f4(x['raw_after']), f4(x['raw_diff']), f4(x['pT_before']), f4(x['pT_after']), f4(x['obs_diff'])) for x in PH['raw_softmax_main'] if x['eligible']]
        rows4 += ['- %s事後の器は、同じ芯の関数で変換の後の確率を出し直し、層二の記録と %d 行すべてで一致することを確かめた。答えの文字を覆うトークンの位置も、%d 件すべてで Colab の記録と一致した。' % (
            TAG4, PH['checks']['pT_reproduced_rows'], PH['checks']['cover_reproduced'])]
        ins['9b'] = rows4

        # ---- §4 の数え上げと注・感度の集合・兄弟・八腕・対の距離
        allp, low_layers = [], collections.Counter()
        for r, L_ in lens['layers'].items():
            for name, mv in L_['directions'].items():
                main_ms = [m for m in ('M_L_survival', 'M_L_nuclear', 'M_X_survival', 'M_X_nuclear', 'M_Lc', 'M_R_survival', 'M_F', 'M_F_sens') if m in mv] + [m for m in mv if m.startswith('M_E_') and ':' not in m and mv[m]['own']]
                for m in main_ms:
                    allp.append(mv[m]['p_iso'])
                    if mv[m]['p_iso'] < 0.01:
                        low_layers[r] += 1
        var = [k for k in lay['directions']['static'] if ':' in k and k.split(':')[0] in ('M_X_survival', 'M_X_nuclear', 'M_E_static')]
        dS = lay['directions']['static']
        below = [k for k in var if dS[k]['p_iso'] < 0.05]
        ofs = {u: lay['directions'][u]['M_F']['real_rank']['of'] for u in ('static', 'Nk', 'rand:0')}
        rows6 = ['- %s§4 の数え上げ: 値 %d・等方の割合が 0.05 を下回るもの %d（偶然の目安 %.1f）・0.01 を下回るもの %d（%s）・0.002 以下 %d。' % (
            TAG, len(allp), sum(p < 0.05 for p in allp), 0.05 * len(allp), sum(p < 0.01 for p in allp), '・'.join('層 %s に %d' % kv for kv in sorted(low_layers.items())), sum(p <= 0.002 for p in allp)),
                 '- %s札は選んだ層の v̂ の主の六つの物差しだけに付けた。§4 の値には札を付けない。段階 B の本走行の加減は層 %s だけで、ほかの層の値には本走行の行動の相手が無い（調整走行だけ）。' % (TAG, sel),
                 '- %s層ごとに方向のノルムをその層の ‖v̂‖ に揃えたので、生の値は層の間で比べない。M_F と M_F_sens のように、物差しには重なりがある。' % TAG,
                 '- %s実在の差の順位の分母: v̂ と (6b) は %d（兄弟の三対と自分の対を除く）・Nk と td は %d（自分の対を除く）・ランダム方向は %d（除かない）。' % (TAG, ofs['static'], ofs['Nk'], ofs['rand:0']),
                 '- %s感度の集合（v̂・層の割合 %s・札を付けない）: %s。E の片仮名一字の変種は主の集合と同じ値（E に片仮名一字が無い）。名目の 0.05 を下回るのは %s で、Holm の第一段（%s）には届かない。' % (
                     TAG, sel, '・'.join('%s %s（等方 %s・実在の差 %d／%d）' % (k, f4(dS[k]['value']), f4(dS[k]['p_iso']), dS[k]['real_rank']['rank'], dS[k]['real_rank']['of']) for k in var),
                     '・'.join(below) or 'なし', f4(min(x['holm_step'] for x in P.values()))),
                 '- %s兄弟の三対（比べる相手から除いた対・別の行・主の六つの物差し）:' % TAG]
        for r, L_ in lens['layers'].items():
            for dn in ('static', 'loaded'):
                rows6.append('  - 層 %s・%s: %s' % (r, dn, '／'.join('%s: %s' % (p, '・'.join('%s %s' % (m, f4(v[PRIM[m]])) for m in PRIM)) for p, v in L_['siblings'][dn].items())))
        rows6.append('- %s八腕の値（主の六つの物差しを、各腕の活性の平均に当てた値・正本 `nulls.real.label_meaning`）:' % TAG)
        for r, L_ in lens['layers'].items():
            rows6.append('  - 層 %s: %s' % (r, '／'.join('%s: %s' % (arm, '・'.join('%s %s' % (m, f4(av[PRIM[m]])) for m in PRIM)) for arm, av in L_['arm_values'].items())))
        rows6.append('- %s対の距離（八腕の活性の平均の差のノルム）:' % TAG)
        for r, L_ in lens['layers'].items():
            rows6.append('  - 層 %s: %s' % (r, '・'.join('%s %s' % (p, f4(d)) for p, d in L_['pair_distance'].items())))
        ins[11] = rows6

        # ---- §6 の注
        marks = sorted({mk for v in lens['lists'].values() for side in ('top_counts', 'bottom_counts') for mk in v[side]})
        bv, topk = TL['inputs']['model']['base_vocab'], TL['projection']['top_k']
        ch = []
        for mk in marks:
            n = set_size(SJ, mk)
            if n:
                ch.append('%s %d 語で %s' % (mk, n, f4(n * topk / bv)))
        ins[13] = ['- %s上の数には比べる帰無が無く、読まない。上位 %d 語に集合の語が偶然に入る数の目安（集合の語の数 × %d ÷ 含める語彙の数 %d）: %s。E の語は、埋め込みの共有の下で入力の語の写しとして上位に入りうる（§9 の限界の文）。'
                   % (TAG, topk, topk, bv, '・'.join(ch) or 'なし')]

        # ---- §7 の狙いと零にした感度
        rows7 = ['- %s狙いの度合い（物差し ÷ 語彙にわたる Δℓ の標準偏差）と、上位の次元（%d 個）を零にした物差しの値（札を付けない）:' % (TAG, TL['descriptive_after_seal']['top_dims'])]
        for k, v in lens['descriptive_after_seal'].items():
            if k.startswith('iso@'):
                continue
            dn = k.split('@')[0]
            ks = [('M_L_survival', 'M_L_survival'), ('M_L_nuclear', 'M_L_nuclear'), ('M_X_survival', 'M_X_survival'), ('M_X_nuclear', 'M_X_nuclear'), ('M_F', 'M_F'), ('M_E', E_OWN[dn])]
            rows7.append('  - %s: 狙い %s／零にした値 %s' % (k, '・'.join('%s %s' % (lab, f4(v['targeting'][m])) for lab, m in ks), '・'.join('%s %s' % (lab, f4(v['zeroed'][m])) for lab, m in ks)))
        zz = lens['descriptive_after_seal']['static@%s' % sel]['zeroed']
        rows7 += ['- %sv̂・層の割合 %s では、上位の次元を零にすると M_X_nuclear は %s から %s に、M_F は %s から %s になる。' % (TAG, sel, f4(dS['M_X_nuclear']['value']), f4(zz['M_X_nuclear']), f4(dS['M_F']['value']), f4(zz['M_F'])),
                  '- %s等方の方向の上位の次元の割合は計算していない（上の割合に等方の参照は無い）。' % TAG]
        ins[14] = rows7

        # ---- 直した照合の表と注
        oc = BR.outcomes(TL, lens, calib)
        na = {k for k in oc if k.endswith('.dir') and oc[k] == FORM.NP}
        cnt = {}
        rows8 = ['- %s直した照合の表（札が付かなかった項目の向きの欄は「札が付くなら」の条件が立たないので「該当なし」。符号では比べない。上の表は凍結した器の出力のまま残す）:' % TAG, '',
                 '| 欄 | 結果 | 登録者 | コーディネータ |', '|---|---|---|---|']

        def verdict(who, k):
            v = preds[who].get(k, FORM.NP)
            if k in na:
                return v, '該当なし'
            if v == FORM.NP:
                return v, '予想しない'
            return v, '一致' if v == oc[k] else '不一致'
        for who in ('registrant', 'coordinator'):
            cnt[who] = collections.Counter(verdict(who, k)[1] for k in oc)
        for k in [k for p_, fs in FORM.FIELDS for k, _, _ in fs]:
            rows8.append('| %s | %s | %s | %s |' % (k, NA if k in na else oc[k], '%s（%s）' % verdict('registrant', k), '%s（%s）' % verdict('coordinator', k)))
        lab = ('一致', '不一致', '該当なし', '予想しない')
        lo, r0 = [[x for x in mg['main_rows'] if x['row'] == rn][0] for rn in ('S4|Osec-Ncold+v6b|loaded', 'S4|Osec-Ncold+vrand|rand:0')]
        tail8 = ['- %s数え直し: 登録者 %s／コーディネータ %s。' % (TAG, '・'.join('%s %d' % (l_, cnt['registrant'][l_]) for l_ in lab), '・'.join('%s %d' % (l_, cnt['coordinator'][l_]) for l_ in lab)),
                 '- %sp1.nuclear.dir の結果「%s」は、二つ目の札だけが付いた物差し（等方の割合 %s）の値の符号。読みの表は、この型では向きを書かない。' % (TAG, oc['p1.nuclear.dir'], f4(P['M_L_nuclear']['p_iso'])),
                 '- %sp8 の結果「%s」は、(6b) の M_F（%s・等方の割合 %s）の符号に依る。層二の正確な直接の経路では、変換の後の確率は (6b) %+.4f・一本目 %+.4f と、どちらも上がる。' % (
                     TAG, oc['p8.answer'], f4(lay['directions']['loaded']['M_F']['value']), f4(lay['directions']['loaded']['M_F']['p_iso']), lo['dp'], r0['dp']),
                 '- %s予想者の情報状態: コーディネータは封印の前に、凍結の前の Colab の確かめの出力（較正の検査の確率・S4 の O-Ncold の主位置の確率 0 を含む）を見た。登録者は、予想が 2026-09-23 に固まっていたと申告した。封印の前の露出は `records/Blens/sealing-exposures-Blens.md` にまとめた（登録者裁定 D190）。' % TAG]
        if final:
            vd, vl = verdict('registrant', 'p1.nuclear.dir'), verdict('registrant', 'p1.nuclear.label')
            if vd[1] != '一致' or vl[1] != '不一致':
                raise SystemExit('登録者の p1.nuclear の欄の判定が想定と違う（止める）: %s・%s' % (vd, vl))
            tail8.insert(1, '- %s登録者の一致 %d のうち p1.nuclear.dir は、札の欄 p1.nuclear.label の予想（%s）が外れた項目の向きの欄で、等方の揺れの中の値の符号と形の上で一致したもの（すぐ下の注）。'
                         % (TAG, cnt['registrant']['一致'], vl[0]))                                    # P606
            t_cal, t_pred, t_save = exposure_times()
            tail8.append('- %s登録者の予想の JSON のファイルの更新（%s・書式から保存した時刻）は、コーディネータから登録者に伝わった露出（%s の較正の検査の確率・%s のコーディネータの予想の一部）の後。'
                         '前の版のファイルの SHA は取っていないので、予想の中身がそれより前に固まっていたことは器では確かめられず、登録者の申告に依る（`records/Blens/sealing-exposures-Blens.md` の注）。'
                         % (TAG, t_save, t_cal, t_pred))                                                  # P608
        rows8 += tail8
        ins[15] = rows8

        # ---- §9 の添えと限界と正誤
        need = {m: 2.638 * lay['iso_sd'][PRIM[m]]['analytic'] / abs(P[m]['value']) for m in ('M_E', 'M_L_survival', 'M_L_nuclear', 'M_F')}
        rc = FR['checks']['colab_check']['random_dirs_compare']
        nl = TL['inputs']['model']['num_hidden_layers'] - 1 - TL['layers']['indices'][sel]
        gate_lim = '  - 門の検出力は低い（上の限界の文）。門を通らなかったことは、物差しと行動の変化がそろわないことを示さない。'
        changed['gate'] = gate_lim
        if final:                                      # P609
            gate_lim += '段の近くの値を、惜しいとも逆の側とも読まない（§0 の添え）。M_X の本の門は順位相関 %s・割合 %s で、段の近くの値でもない。' % (f4(g['full']['M_X']['rho']), f4(g['full']['M_X']['p']))
        ins[16] = ['- %s上の「射影の値はまだ誰も見ていない」は凍結の時点の文。射影は封印の後に計算し、結果は登録者と一緒に開いた。' % TAG,
                   '- %s結果を開いた後に足す限界:' % TAG,
                   '  - 選んだ層で加えた量は、残差のノルムの %s 倍。' % f4(TL['layers']['relative_injection_selected']),
                   '  - 札は選んだ層の v̂ の主の六つの物差しだけに付けた。',
                   '  - Holm の第一段を越えるのに要る |値| は、観測の %s〜%s 倍（M_E・M_L・M_F・解析の標準偏差・正規の近似）。' % (f4(min(need.values())), f4(max(need.values()))),
                   gate_lim,
                   '  - p8 の答えは、零に近い値の符号に依る（§8 の添え）。',
                   '  - 較正の検査は、区間の上端の近くで通った（§3 の添え）。',
                   '  - 段階 B のランダム方向は再生したもので、B は方向そのものを記録していない。手元と Colab の再生は、方向ごとの相対の差の最大 %s（許容 %s）で一致した（登録者裁定 D187）。' % (f4(rc['rel_max']), f4(rc['tol'])),
                   '  - 二つ目の札の比べる相手どうしは相関している（八腕の差・高々七次元）。',
                   '  - 直接の経路の結果は、選んだ層の後の %d 層を通る経路については何も言わない。' % nl,
                   '  - 限界の文「非等方の残差から作った方向には越える棒が低い」は、この結果では物差しで分かれた（§1 の添えの比）。',
                   '- %s正誤: 正本 `report_rules.machine_block.rule` の組み立て器の名（`tools/build_report_B.py`）は段階 B からの写しで、この報告の組み立て器は `tools/build_report_Blens.py`。打ち消しの定型「この順位のそろいは…」は、門を通らなかったこの報告では、そろいが有ったことを前提にしない。' % TAG]

        # ---- 組み立て
        lines = frozen.split(NL)
        t0 = '# B-lens の結果（報告の草案・機械の組み立て）'
        s0 = '- 起草: 南無弥勒如来（コーディネータ）／登録者: 楠見優太。**状態: 報告の草案（結果の巡の前）**。組み立ての器: `tools/build_report_Blens.py`。'
        if lines[0] != t0 or lines[2] != s0:
            raise SystemExit('凍結の報告の見出しか状態の行が想定と違う（止める）')
        t_draft = '# B-lens の結果（報告の草案の二つ目・凍結した組み立ての器の出力に逸脱の区画を足したもの）'
        s_draft = '- 起草: 南無弥勒如来（コーディネータ）／登録者: 楠見優太。**状態: 報告の草案の二つ目（結果の巡・第一巡の後・最終の系統外の一票の前）**。組み立ての器: `tools/build_report_Blens.py`（凍結）と `tools/build_report_Blens_devBL3.py`（逸脱の下）。'
        t_fin = '# B-lens の結果（報告の最終版・凍結した組み立ての器の出力に逸脱の区画を足したもの）'
        s_fin = '- 起草: 南無弥勒如来（コーディネータ）／登録者: 楠見優太。組み立ての器: `tools/build_report_Blens.py`（凍結）と `tools/build_report_Blens_devBL3.py`（逸脱の下）。'    # v3・F-A: 状態は下の機械の区画
        changed['title'], changed['status'] = t_draft, s_draft
        lines[0], lines[2] = (t_fin, s_fin) if final else (t_draft, s_draft)
        bl = blocks_of(lines, MB)
        want_heads = {0: '- 正本 `design/contrasts-Blens.json`', 2: '- M_L_survival: 値', 3: '- 〈', 5: '| 物差し | 値 |', 7: '| 門 | 物差し |', 9: '- 手元の logits の突き合わせ', 11: '- 層の割合',
                      13: '- static@', 14: '- static@', 15: '| 欄 | 結果 |', 16: '- 直接の経路だけを見る'}
        for k, hd_ in want_heads.items():
            if not bl[k][2].startswith(hd_):
                raise SystemExit('凍結の報告の区画 %d の頭が想定と違う（止める）: %s' % (k, bl[k][2][:40]))
        after = collections.OrderedDict()
        for k in sorted(ins, key=lambda x: (int(str(x).rstrip('b')), str(x))):
            kk = int(str(k).rstrip('b'))
            after.setdefault(bl[kk][1], []).append(ins[k])
        for end in sorted(after, reverse=True):
            add = []
            for blk in after[end]:
                add += [''] + [MB['begin']] + blk + [MB['end']]
            lines[end + 1:end + 1] = add
        fence_i = max(i for i, l in enumerate(lines) if l == BR.FENCE)
        rev_draft = ['- %sこの草案の検分票:' % TAG,
                     '  - 対象: 報告の草案の二つ目（凍結した器の出力と、足した区画）。',
                     '  - 段階: 結果の後・結果の巡・第一巡の後（採否表 P565〜P603・登録者裁定 D189〜D193）。',
                     '  - 凍結物の同定: 凍結の本文 SHA16 %s・正本 SHA16 %s・計算に使った器は凍結の値のまま（冒頭の添え）。' % (FR['frozen_sha16']['design/design-Blens-FROZEN.md'], FR['frozen_sha16']['design/contrasts-Blens.json']),
                     '  - 盲検の状態: 該当しない（結果は登録者と一緒に開いた）。',
                     '  - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外三票（新しい個体一）と系統内三票（一票）。最終の系統外の一票はこの後（新しい個体・登録者裁定 D189）。',
                     '  - COI記録: 起草者は器と報告を書いた当人で、「正しく読めている」と書く側に引かれる。登録者は封印した予想の欄に希望の向きを書いた。照合の直しで符号を使わないことを、その向きへの歯止めにした。',
                     '  - 本検分が確認していないこと: 最終の系統外の一票が見つけること。足した区画の文の言い過ぎ（走査は禁止語だけを見る）。']
        rev_final = ['- %s上の三行は、凍結した組み立ての器が草案のときに出した検分票で、凍結の出力のまま残す。読みの型の当否は、結果の巡と最終検分で見た（採否表 P565〜P603・P604〜P619）。' % TAG,   # v3・F-D
                     '- %s最終版の検分票:' % TAG,
                     '  - 対象: 報告の最終版（凍結した器の出力と、足した区画）。',
                     '  - 段階: 結果の後。結果の巡・第一巡の後（採否表 P565〜P603・登録者裁定 D189〜D193）と、最終検分の後（採否表 P604〜P619・登録者裁定 D194〜D197）と、'
                     '起草者の最終の見直しの後（`%s`・登録者裁定 D198・D199）。' % REVIEW,
                     rev_draft[3],
                     rev_draft[4],
                     '  - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外三票（新しい個体一）と系統内三票（一票）で、凍結の本文 §10 は結果の巡を新しい個体で組むとしたが、'
                     '依頼文は設計の巡と同じ四名に宛てた（逸脱 D-BL2）。最終検分は系統外二票（Gemini 3.8 Flash の新しい個体二・正本の一票を二票にした逸脱 D-BL5・登録者裁定 D195）。同じ機種の二票は、会話が別でも相関しうる。'
                     '起草者の最終の見直しは起草者自身のもので、外の目ではない。',                                                                                          # v3・F-B
                     '  - COI記録: 起草者は器と報告を書いた当人で、「正しく読めている」と書く側に引かれる。登録者は封印した予想の欄に希望の向きを書いた。照合の直しで符号を使わないことを、その向きへの歯止めにした。'
                     '最終版で足した行と句は、最終検分の票と起草者の最終の見直しが挙げたものに限った（読みを足さない）。',
                     '  - 本検分が確認していないこと: 最終版で足した行と句は、もう一度の検分を経ていない（登録者裁定 D194・最終検分の後に巡を置かない。起草者の最終の見直しは起草者自身のもの）。足した区画の文の言い過ぎ（走査は禁止語だけを見る）。']
        changed['rev'] = rev_draft
        lines[fence_i:fence_i] = [MB['begin']] + (rev_final if final else rev_draft) + [MB['end'], '']
        if final:                                      # v3・F-A: 状態の区画（登録者最終確認の記録があれば逐語と時刻・無ければ確認の前）
            prev = re.search(r'`%s` の (\w+) の版（' % re.escape(FINAL_REL), open(P_(*REVIEW.split('/')), encoding='utf-8').read()).group(1)
            if os.path.exists(CONFIRM):
                cf = json.load(open(CONFIRM, encoding='utf-8'))
                stl = '- 状態: **最終版**（登録者最終確認 %s 日本時間・会話の記録 uuid `%s`・逐語「%s」）。登録者が確かめた案（SHA16 %s）と、この一行のほかは同じ。' % (
                    cf['jst'], cf['uuid'], cf['words'], cf['proposal_sha16'])
            else:
                stl = '- 状態: **報告の最終版**（最終検分と起草者の最終の見直しの後・登録者最終確認の前。確認の後に、この区画に確認の逐語と時刻を入れる）。'
            lines[3:3] = [MB['begin'], stl,
                          '- %sこの版の一つ前の最終版（%s の版）は、登録者の指示で登録者最終確認の前に push した（登録者裁定 D199）。その版の状態の行は、確認の後に公開すると書いていた（起草者の最終の見直し F-A）。' % (TAG, prev),
                          MB['end']]
        return NL.join(lines)

    text = compose(a.final)
    if a.final:                                        # 草案の二つ目を同じ走りで作り直し、置き場と同じことと、消えた行が決めた行だけであることを確かめる
        draft = compose(False)
        if draft != open(OUT, encoding='utf-8').read().replace('\r\n', NL):
            raise SystemExit('作り直した草案の二つ目が、置き場の草案の二つ目と違う（止める）')
        allowed = {changed['title'], changed['status'], changed['head'], changed['gate'], changed['heads'], changed['lhead']} | set(changed['rev'])
        dl, fl_ = draft.split(NL), text.split(NL)
        gone = [dl[i] for tg, i1, i2, j1, j2 in difflib.SequenceMatcher(None, dl, fl_, autojunk=False).get_opcodes() if tg in ('replace', 'delete') for i in range(i1, i2)]
        if any(l not in allowed for l in gone):
            raise SystemExit('草案の二つ目から、決めていない行が消えた（止める）: %s' % [l[:60] for l in gone if l not in allowed])
        added_n = len(fl_) - len(dl) + len(gone)
        print('草案の二つ目と同じ（作り直し）・最終版で改めた草案の行 %d・足した行 %d' % (len(gone), added_n))
    V, side = BR.lint_report(text, TL)
    if os.path.exists(out) and not a.force:
        if text != open(out, encoding='utf-8').read().replace('\r\n', NL):
            raise SystemExit('既にある出力と、組んだ文が違う（止める・--force で書き直す）: %s' % os.path.relpath(out, REPO))
        print('既にある出力と同じ（書かない）: %s（走査の違反 %d）' % (os.path.relpath(out, REPO), len(V)))
        if V:
            raise SystemExit('報告の走査に違反がある（非零で終わる）')
        return
    open(out, 'w', encoding='utf-8', newline=NL).write(text)
    RL.write_sidecar(out, text, TL, 'tools/build_report_Blens_devBL3.py %s' % VERSION)
    lint_path = out.replace('.md', '-lint.md')
    what = '報告の最終版' if a.final else '報告の草案の二つ目'
    open(lint_path, 'w', encoding='utf-8', newline=NL).write(NL.join(['# %sの走査（凍結した `tools/report_lint.py` の lint・凍結した組み立ての器の `lint_report`）' % what, '', '- 違反 %d' % len(V)] +
                                                                  ['- %s（%s 行目）: %s' % (v['kind'], v['line'], v['token']) for v in V] + ['', BR.FENCE, '']))
    print('wrote %s（走査の違反 %d・区画 %d）' % (os.path.relpath(out, REPO), len(V), len(side['blocks'])))
    if V:
        for v in V[:20]:
            print(v)
        raise SystemExit('報告の走査に違反がある（非零で終わる）')


if __name__ == '__main__':
    main()
