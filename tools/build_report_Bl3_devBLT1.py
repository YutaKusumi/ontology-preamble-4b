# -*- coding: utf-8 -*-
"""build_report_Bl3_devBLT1.py v3 —— B-lens 層三（Bl3）の報告の草案の二つ目と最終版（逸脱 D-BLT1・登録者裁定 D243〜D246・v2 は D249・v3 は D251・D253・2026-09-27・B-lens の `tools/build_report_Blens_devBL3.py` の型）。

凍結した組み立ての器 `tools/build_report_Bl3.py` を読み込み、同じ入力（凍結の記録の台帳・逸脱の印の JSON `records/Bl3/report-marks-Bl3.json`・起草者の欄
`records/Bl3/results-rejected-lines-Bl3.md`）で凍結の報告を作り直して、置き場の `records/Bl3/results-Bl3.md` とバイトで同じことを確かめてから、
見出しと状態の行を改め、【逸脱 D-BLT1】の印を付けた機械の区画を足す。凍結の報告の文と区画は、見出しと状態の行のほか一字も変えない。
足す区画は、結果の巡の採否の案（`records/reviews/Bl3/results-round1/adoption-results-Bl3.md`）の区分（三）の行:
  頭の添え（P711）・起草者の欄の数（P704）・唯一の等方の外の行の升目の事情と札の余白（P705）・表の前の断りと並べ直しの表（P699・B-lens の P607 の型・升目の名の縦棒を逆斜線で逃がす）・
  §3 の注（P706）・§5 の注（P707）・§6 の注（P708）・§7 の注（P709・P710）・草案の検分票。
数はすべて記録（集計の記録・組の出力・下見の記録・設計事実・開く段の記録）から器が読む。印の区画の数のうち結果の巡の再現の記録
（`records/reviews/Bl3/results-round1/checks/verification-results-Bl3.json`・票の主張を器とは別の式で再現した記録）にあるものは、その記録の値と照らし、外れたら止める。
確かめ: (一) 凍結の報告の作り直しがバイトで同じ (二) 足した区画を除いて見出しと状態の行を戻すと、凍結の報告とバイトで同じ (三) 並べ直しの表の各行は、逆斜線を戻すと凍結の表の行と同じで、
  列の区切りの数が見出しと同じ・凍結の表の行がすべて一度ずつ出る (四) 凍結した走査器の違反 0 (五) 再現の記録との照らしの外れ 0。
出力: records/Bl3/results-Bl3-draft2.md・同じ名の -machine.json・-lint.md と、確かめの記録 records/Bl3/results-Bl3-draft2-checks.json。
  出力が既にあって --force が無ければ、組んだ文を置き場のファイルと比べ、同じなら何も書かずに終わり、違えば止める。
v2（最終の系統外の検分の後・登録者裁定 D249）: `--final` で最終版を組む。見出しを「報告の最終版」に、状態の行を「最終の系統外の検分の後・登録者最終確認の前」
  （登録者最終確認の記録があれば凍結した器の最終版の型の行をそのまま）に、頭の添えと検分票を最終版のものにする。足す区画の中身は草案の二つ目と同じ組み方。
  最終の検分を受けた草案の二つ目（置き場のファイル）は書き換えず、最終版との違いが決めた行（見出し・状態の行・凍結の記録の SHA16 の行・逸脱の一覧の D-BLT2 の行・
  頭の添え・検分票・起草者の欄の一行目〔裁定 D248〕・〈両方の外〉の注の等方の最上位の割合の一行〔起草者の最終の見直し・裁定 D251〕）だけであることを確かめる。`--final` が無ければ v1 と同じ組み方（台帳が D-BLT1 だけのときに限る）。
  最終版の出力: records/Bl3/results-Bl3-FINAL-2026-09-27.md・同じ名の -machine.json・-lint.md・-checks.json。
v3（起草者の最終の見直しの一度目と二度目の後・登録者裁定 D251・D253・記録 `records/Bl3/rulings-D251-D253.md`）: `--final` だけを組む（草案の二つ目は器 v1 の出力で、検分を受けたまま残す・
  今の台帳では `--final` の無い組み方は止まる）。二度目の見直し（`records/reviews/Bl3/results-final/final-read2/review2-final-Bl3.md`）の R-a〜R-d を入れる:
  R-a 〈両方の外〉の注の末の一行の二つ目の向きを「弱める側」に／R-b 頭の添えの一行目を、登録者最終確認の前にも後にも合う言い方に（確認の後の状態の行は凍結した器が出す）／
  R-c §5 の注の「」の中を §0 の文に一字違わずある語に／R-d 頭の添えの一行目と四行目・検分票の段階と COI の行に、起草者の最終の見直しとその裁定を足す。
  草案の二つ目との違いの決めた行に、〈両方の外〉の注の末の一行と §5 の注の一行を足す（頭の添えと検分票は v2 から決めた行）。
用法: python tools/build_report_Bl3_devBLT1.py --final [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, math, hashlib, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import build_report_Bl3 as BR
import report_lint as RL

VERSION = 'v3'
NL = chr(10)
BS = chr(92)
TAG = '【逸脱 D-BLT1】'
DEV = 'D-BLT1'
P = lambda r: os.path.join(REPO, *r.split('/'))
OUT = P('records/Bl3/results-Bl3-draft2.md')
CHECKS = P('records/Bl3/results-Bl3-draft2-checks.json')
OUT_FINAL = P('records/Bl3/results-Bl3-FINAL-2026-09-27.md')
CHECKS_FINAL = P('records/Bl3/results-Bl3-FINAL-2026-09-27-checks.json')
REJ, MARKS, OPEN = P('records/Bl3/results-rejected-lines-Bl3.md'), P('records/Bl3/report-marks-Bl3.json'), P('records/Bl3/open-results-Bl3.json')
VER_REL = 'records/reviews/Bl3/results-round1/checks/verification-results-Bl3.json'
ADOPT_REL = 'records/reviews/Bl3/results-round1/adoption-results-Bl3.md'
ADOPT_FINAL_REL = 'records/reviews/Bl3/results-final/adoption-final-Bl3.md'
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
f4 = BR.f4
T_FROZEN = '# B-lens 層三の結果（報告の草案・機械の組み立て）'
S_FROZEN = '- 状態: **報告の草案（結果の巡の前）**。'
T_DRAFT = '# B-lens 層三の結果（報告の草案の二つ目・凍結した組み立ての器の出力に逸脱の区画を足したもの）'
S_DRAFT = '- 状態: **報告の草案の二つ目**（結果の巡の後・最終の系統外の一票の前）。'
T_FINAL = '# B-lens 層三の結果（報告の最終版・凍結した組み立ての器の出力に逸脱の区画を足したもの）'
S_FINAL_PRE = '- 状態: **報告の最終版**（最終の系統外の検分の後・登録者最終確認の前）。'


def blocks_of(lines, MB):
    """機械の区画の並び: (始まりの行の添字, 終わりの行の添字, 中身の一行目)。"""
    out, i = [], 0
    while i < len(lines):
        if lines[i] == MB['begin']:
            j = lines.index(MB['end'], i)
            out.append((i, j, lines[i + 1] if i + 1 < j else ''))
            i = j + 1
        else:
            i += 1
    return out


def dec_tol(s):
    """数の文字列の最後の桁の半分（丸めの幅）。"""
    m = re.match(r'^-?(\d+)(?:\.(\d+))?(?:e([+-]?\d+))?$', s)
    assert m, s
    return 0.5 * 10 ** (-(len(m.group(2) or '')) + int(m.group(3) or 0)) + 1e-12


class Cross:
    """再現の記録（票の主張を器とは別の式で再現した記録）の数と、器が読んだ値を照らす。"""

    def __init__(self, V):
        self.got = {x['k']: x['got'] for x in V['checks']}
        self.done = []

    def __call__(self, k, pattern, values):
        m = re.search(pattern, self.got[k])
        if not m:
            raise SystemExit('再現の記録 %s に照らす形が見つからない（止める）: %s' % (k, pattern))
        for g, v in zip(m.groups(), values):
            if isinstance(v, bool) or isinstance(v, str):
                ok = g == str(v)
            elif isinstance(v, int):
                ok = int(g) == v
            else:
                ok = abs(float(g) - float(v)) <= dec_tol(g)
            if not ok:
                raise SystemExit('再現の記録 %s の値 %s と、器が読んだ値 %r が合わない（止める）' % (k, g, v))
        assert len(m.groups()) == len(values), (k, m.groups(), values)
        self.done.append({'k': k, 'record': list(m.groups()), 'builder': [v if isinstance(v, (str, int)) else float(v) for v in values]})


def table_of(block_lines):
    """区画の中の表: (見出しの添字, 見出しの行, 列の数, 行の添字の並び)。列の区切りは前後に空白のある縦棒で、升目の名の中の縦棒には空白が無い。"""
    for i in range(len(block_lines) - 1):
        if block_lines[i].startswith('| ') and re.match(r'^\|(---\|)+$', block_lines[i + 1]):
            n = len(block_lines[i][2:-2].split(' | '))
            rows, k = [], i + 2
            while k < len(block_lines) and block_lines[k].startswith('| '):
                rows.append(k)
                k += 1
            return i, block_lines[i], n, rows
    raise SystemExit('区画に表が無い（止める）')


def escape_row(row, n):
    cells = row[2:-2].split(' | ')
    if len(cells) != n:
        raise SystemExit('表の行の列の数が見出しと違う（止める）: %s' % row[:60])
    out = '| ' + ' | '.join(c.replace('|', BS + '|') for c in cells) + ' |'
    if out.count('|') - out.count(BS + '|') != n + 1 or out.replace(BS + '|', '|') != row:
        raise SystemExit('並べ直した行が見出しと合わないか、逆斜線を戻しても元の行にならない（止める）: %s' % row[:60])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--final', action='store_true')
    a = ap.parse_args()
    if not a.final:
        raise SystemExit('v3 は最終版（--final）だけを組む。草案の二つ目は器 v1 の出力で、検分を受けたまま残す（止める・裁定 D249・D253）')
    T3, FR, A, preds, meta, confirmation = BR.load_inputs()
    if confirmation is not None and not a.final:
        raise SystemExit('登録者最終確認の記録があるときは、最終版（--final）だけを組む（止める）')
    devs_ = [d.get('no') for d in (FR.get('deviations') or [])]
    if devs_ != ([DEV, 'D-BLT2'] if a.final else [DEV]):
        raise SystemExit('凍結の記録の台帳が想定と違う（止める）: %s（草案の二つ目は台帳が D-BLT1 だけのときに組んだもので、検分を受けたまま残す・裁定 D249）' % devs_)
    marks = json.load(open(MARKS, encoding='utf-8'))
    rejected = open(REJ, encoding='utf-8').read()
    frozen = BR.build(T3, A, preds, meta, FR.get('deviations') or [], marks, rejected, confirmation, False)
    if frozen != open(BR.OUT, encoding='utf-8').read().replace('\r\n', NL):
        raise SystemExit('凍結した器で作り直した報告が、置き場の報告と違う（止める）')
    MB = RL.machine_block(T3)
    V = json.load(open(P(VER_REL), encoding='utf-8'))
    X = Cross(V)
    OJ = json.load(open(OPEN, encoding='utf-8'))
    FJ = json.load(open(P('records/Bl3/design-facts-Bl3.json'), encoding='utf-8'))
    dirs = {p_: v['dir'] for p_, v in A['inputs'].items()}
    M = json.load(open(P('results/Bl3/main/%s/main.json' % dirs['main']), encoding='utf-8'))
    RC = json.load(open(P('results/Bl3/main/%s/recompute.json' % dirs['recompute']), encoding='utf-8'))
    rec = A['pilot_attempts'][-1]
    rows = A['rows']
    KISO = T3['nulls']['isotropic']['count']
    m = A['rows_meta']['m_rows']
    iso = lambda k: np.array([v for kk, v in M['cells'][k]['effects'].items() if kk.startswith('iso:')], dtype=np.float64)
    ev = {e['key']: e for e in OJ['events']}

    # ---- 起草者の欄の数（P704）
    cs = sorted({r['cell_sign'] for r in rows.values()})
    iqr = {r['cell_sign']: r['side']['q3'] - r['side']['q1'] for r in rows.values()}
    for k in cs:
        q1_, q3_ = np.percentile(iso(k), 25), np.percentile(iso(k), 75)
        if abs((q3_ - q1_) - iqr[k]) > 1e-9:
            raise SystemExit('集計の記録の四分位と組の出力の等方の効き目が合わない（止める）: %s' % k)
    iq_lo, iq_hi = min(iqr.values()), max(iqr.values())
    g_lo, g_hi = min(float(iso(k).min()) for k in cs), max(float(iso(k).max()) for k in cs)
    X('K498', r'四分位の幅 ([\d.]+)〜([\d.]+)・範囲 (-?[\d.]+)〜(-?[\d.]+)（主の升目と符号 (\d+)）', [iq_lo, iq_hi, g_lo, g_hi, len(cs)])
    outs = [rid for rid, r in rows.items() if r['iso_outside']]
    non = [r for r in rows.values() if not r['iso_outside']]
    p_lo, p_hi = min(r['p'] for r in non), max(r['p'] for r in non)
    tl = [min(r['upper'], r['lower']) for r in non]
    X('K525', r'行 (\d+)・p ([\d.]+)〜([\d.]+)', [len(non), p_lo, p_hi])
    X('K502', r'(\d+)〜(\d+) 本・([\d.]+)〜([\d.]+)%', [min(tl), max(tl), 100.0 * min(tl) / KISO, 100.0 * max(tl) / KISO])
    ab = [abs(r['effect']) for r in rows.values()]
    X('K524', r'([\d.]+)〜([\d.]+)（行 (\d+)）', [min(ab), max(ab), len(ab)])
    n_st = sum(1 for r in rows.values() if r['direction'] == 'static')
    n_nk = sum(1 for r in rows.values() if r['direction'] == 'Nk')
    n_rc = len(RC['rows'])
    if {x[0].split(':')[0] for x in RC['rows']} - {'sub', 'add'} or n_rc != n_st:
        raise SystemExit('独立の再計算の行が v̂ の行と違う（止める）')
    d1 = A['recompute']['first']['max_abs_diff']
    batch = A['main_run']['batch']
    X('K506', r'再計算の行 (\d+)（[^）]*）・一段目の差の最大 ([\d.e+-]+)・本の計算のバッチ (\d+)', [n_rc, d1, batch])
    X('K480', r"通った \['([^']+)'\]", [outs[0] if len(outs) == 1 else '・'.join(outs)])
    b_rej = ['- %s起草者の欄の文が指す数（記録から器が読んだ）:' % TAG,
             '  - 升目と符号ごとの等方の効き目（%d 本）の四分位の幅 %.2f〜%.2f・範囲 %.2f〜%.2f（主の升目と符号 %d）。' % (KISO, iq_lo, iq_hi, g_lo, g_hi, len(cs)),
             '  - Holm の後に等方の外になった行 %d（主の行 %d のうち）。ほかの %d 行の p は %.3f〜%.3f で、効き目と同じか外側にある等方の方向の本数は、割合を決めた裾で %d〜%d 本（%.1f〜%.1f%%）。'
             % (len(outs), m, len(non), p_lo, p_hi, min(tl), max(tl), 100.0 * min(tl) / KISO, 100.0 * max(tl) / KISO),
             '  - 主の行の効き目の大きさ（絶対値）%.3f〜%.3f。' % (min(ab), max(ab)),
             '  - 独立の再計算の行 %d（v̂ の行）・Nk の行 %d は計算し直していない・一段目の差の最大 %.3g・本の計算のバッチの大きさ %d。' % (n_rc, n_nk, d1, batch)]

    # ---- 唯一の等方の外の行（P705）
    if len(outs) != 1:
        raise SystemExit('等方の外の行が一つでない（この器は一つの形だけを組む・止める）')
    rid1 = outs[0]
    r1 = rows[rid1]
    c1 = r1['cell_sign']
    cell1 = c1.rsplit('|', 1)[0]
    pa0 = A['descriptive']['pa_noop'][c1]
    pfl, pceil = T3['pilot']['p_bounds']
    lo_floor, lo_ceil = math.log(pfl / (1 - pfl)), math.log(pceil / (1 - pceil))
    pa1 = 1 / (1 + (1 - pa0) / pa0 * math.exp(-r1['effect']))
    lo1 = rec['cells'][cell1]['lo']
    via = rec['vi']['a']
    fl1 = [v for v in sorted(rec['iv']) if rec['iv'][v]['flags'].get(cell1)]
    rate1 = rec['cells'][cell1]['stage_b_rate']
    isoN = np.sort(iso(c1))[::-1]
    kmax = lambda mm: max(k for k in range(50) if 2 * (1 + k) / (1 + KISO) < 0.05 / mm)
    if r1['upper'] != int((iso(c1) >= r1['effect']).sum()):
        raise SystemExit('上の裾の本数が組の出力と合わない（止める）')
    q7 = {e['id']: e for e in FJ['facts']['C']['q7_intervals']}[rid1]
    lab1 = (A['stage_b_notes']['main'].get(rid1) or {}).get('label')
    X('K504', r'上位 ([\d.]+)・([\d.]+)・([\d.]+)・余白 ([\d.]+)・偶の標準偏差 [\d.]+・確率 ([\d.]+) → ([\d.]+)', [isoN[0], isoN[1], isoN[2], r1['effect'] - isoN[2], pa0, pa1])
    X('K494', r"床 (-?[\d.]+)・余白 \{'N1\|O-Ncold': ([\d.]+), ", [lo_floor, lo1 - lo_floor])
    X('K527', r'率 ([\d.]+)・確率 ([\d.e-]+)', [rate1, pa0])
    X('K495', r'N1\|O-Ncold の印 \[(.*)\]', [', '.join(str(bool(rec['iv'][v]['flags'].get(cell1))) for v in ('V1', 'V2', 'V3'))])
    X('K530', r'差 (-?[\d.]+) pt・区間［(-?[\d.]+), (-?[\d.]+)］・零を含む (\w+)', [q7['diff_pt'], q7['lo'], q7['hi'], str(bool(q7['contains_zero']))])
    X('K526', r'(\d+) 行 (\d+) 本（p ([\d.]+)・段 ([\d.]+)）・十六行 (\d+) 本', [m, kmax(m), 2 * (1 + kmax(m)) / (1 + KISO), 0.05 / m, kmax(16)])
    X('K488', r'sub:N1 ([\d.]+)・1/49 ([\d.]+)', [r1['iso_top_share'], 1 / r1['second']['of_oriented']])
    X('K489', r'式 ([\d.]+) と ([\d.]+)', [A['chance']['oriented'], A['chance']['pair']])
    if not (q7['contains_zero'] and [x['id'] for x in A['q7_rows']] == [rid1]):
        raise SystemExit('q7 の区間の記録が想定と違う（止める）')
    b_n1 = ['- %s〈両方の外〉の行（%s）の升目の事情と札の余白（読みは付けない）:' % (TAG, rid1),
            '  - 升目 %s の無操作の選択肢 a の確率 %s（床 %s の %.2f 倍・§2 の升目ごとの表）。効き目 %.3f の分だけ対数オッズを動かすと %.2g。' % (cell1, f4(pa0), f4(pfl), pa0 / pfl, r1['effect'], pa1),
            '  - 無操作の対数オッズ %s と床の対数オッズ %.3f の差（床からの余白）は %.3f で、下見の (vi) の (a) の幅 %s より小さい（§1）。揺れの版の印: %s（§1）。段階 B の無操作の破局の率 %s（§1）。'
            % (f4(lo1), lo_floor, lo1 - lo_floor, f4(via[cell1]), '・'.join(fl1) or 'なし', f4(rate1)),
            '  - Holm の第一段までの余白: 効き目 %.3f 以上の等方の方向は %d 本（%.3f）。第一段 %.6f を通る上限は %d 本で、等方の効き目の二番目と三番目は %.3f と %.3f（三番目との差 %.3f）。'
            % (r1['effect'], r1['upper'], isoN[0], 0.05 / m, kmax(m), isoN[1], isoN[2], r1['effect'] - isoN[2]),
            '  - 段階 B のこの行の差 %.1f pt・区間［%.2f, %.2f］は零を含む（q7 で数えない行・転記行 C）。主の表の段階 B の札: %s。' % (q7['diff_pt'], q7['lo'], q7['hi'], lab1),
            '  - 等方の最上位の割合 %s（向きまで数えた順位の分母の逆数は %.4f）・二つ目の札の偶然の目安 %s〜%s（§2）。等方の帰無の中央値 %s・効き目の側: %s（主の表）。'
            % (f4(r1['iso_top_share']), 1 / r1['second']['of_oriented'], f4(A['chance']['oriented']), f4(A['chance']['pair']), f4(r1['iso_median']), BR.side_text(T3, r1['side'])),
            '  - これらは札と型を変えない。どちらの向きにも読まない（区別できたことを強める側にも、弱める側にも）。']   # 二度目の見直しの R-a（裁定 D253）

    # ---- §3（P706）
    G = A['gates']
    gw, gd = G['without_vhat'], G['desc_without_vhat_loaded']
    loaded_cells = sorted({g['cell'] for g in A['gate_rows'] if g['unit'] == 'loaded'})
    _, gate_only = BR.dropped_split(T3, rec.get('decision') or {})
    if not (loaded_cells and set(loaded_cells) <= set(gate_only) and 'loaded' not in G['main']['units']
            and (gw['n_rows'], gw['n_perm'], gw['rho'], gw['p']) == (gd['n_rows'], gd['n_perm'], gd['rho'], gd['p'])):
        raise SystemExit('記述の門と v̂ を抜いた門の同じ形か、loaded の行の升目が想定と違う（止める）')
    X('K490', r'main 行 (\d+)・単位 (\d+)・入れ替え (\d+)・ρ ([\d.]+)・p ([\d.]+) ／ without_vhat 行 (\d+)・単位 (\d+)・入れ替え (\d+)・ρ ([\d.]+)・p ([\d.]+) ／ desc_without_vhat_loaded 行 (\d+)',
      [G['main']['n_rows'], len(G['main']['units']), G['main']['n_perm'], G['main']['rho'], G['main']['p'], gw['n_rows'], len(gw['units']), gw['n_perm'], gw['rho'], gw['p'], gd['n_rows']])
    b_gate = ['- %s記述の「v̂ と (6b) を抜いた門」は、v̂ を抜いた門と同じ行 %d・同じ値（順位相関 %s・p %s）になった。(6b) の行は下見で外した門の行だけの升目 %s にだけあったためで、別の手がかりとして数えない。'
              % (TAG, gd['n_rows'], f4(gd['rho']), f4(gd['p']), '・'.join(loaded_cells)),
              '- %s入れ替える単位からは loaded が消え、本の門の単位は %d（%s）・入れ替えの数は %d になった（下見の前の見込みの入れ替えの数は %d・正本 `gate.permutations`）。'
              % (TAG, len(G['main']['units']), '・'.join(G['main']['units']), G['main']['n_perm'], T3['gate']['permutations'])]

    # ---- §5（P707）
    b_rc = ['- %s独立の再計算の範囲は v̂ の行 %d だけで、Nk の行 %d は計算し直していない（正本 `independent_recompute.what`）。本の計算のバッチの大きさは %d で、正本の注「%s」のとおり、二段目は形だけの確かめだった。'
            '§0 の独立の再計算の二つの「一致」は、この範囲の一致。' % (TAG, n_rc, n_nk, batch, T3['independent_recompute']['stages']['second']['note'])]   # 二度目の見直しの R-c（裁定 D253）

    # ---- §6（P708）
    cq = {'q2': (sum(1 for r in rows.values() if r['direction'] == 'static' and r['iso_outside']), n_st), 'q3': (sum(1 for r in rows.values() if r['direction'] == 'Nk' and r['iso_outside']), n_nk),
          'q6': (sum(1 for r in rows.values() if r['second']['top']), len(rows))}
    X('K509', r"数 \{'q2': (\d+), 'q3': (\d+), 'q6': (\d+)\}・分母 \{'q2': (\d+), 'q3': (\d+), 'q6': (\d+)\}", [cq['q2'][0], cq['q3'][0], cq['q6'][0], cq['q2'][1], cq['q3'][1], cq['q6'][1]])
    b_pred = ['- %s数と分母: q2 %d／%d（v̂ の行）・q3 %d／%d（Nk の行）・q6 %d／%d（主の行）。' % (TAG, cq['q2'][0], cq['q2'][1], cq['q3'][0], cq['q3'][1], cq['q6'][0], cq['q6'][1]),
              '- %sq7 を採点しない理由: 等方の外の v̂ の行は %d（%s）あったが、段階 B のその行の差の区間が零を含み（転記行 C）、正本 `predictions.q7_rule` で数えられる行が残らなかった。行の向きは書かない。' % (TAG, len(A['q7_rows']), rid1),
              '- %s封印の前後に起きた二つの事（コーディネータの予想の値が封印の台本（道具の呼び出しの中身）に出たこと・登録者の予想の情報状態の欄が露出の記録を挙げず、封印の後に登録者の言葉で補ったこと）は、'
              '台帳の封印の行（`records/FREEZE-RECORD.md`）にある。封印の前の露出の記録（凍結物）は書き換えていない。' % TAG]

    # ---- §7（P709・P710）
    TS_ = r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)'
    X('K536', r'判定の記録（3e185d3）の push ' + TS_ + r'・開く段の呼び出し ' + TS_ + r'・登録者への報告 ' + TS_, [OJ['pushes']['judge_3e185d3'], ev['open']['jst'], ev['told']['jst']])
    vd = rec['v']['diffs']
    main_cells = [c for c in rec['cells'] if rec['cells'][c].get('main')]
    v_main = max(main_cells, key=lambda c: abs(vd[c]))
    vi_c = max(via, key=lambda c: via[c])
    noise = T3['pilot']['noise_max']
    X('K492', r'\(vi\)\(a\) (\S+) ([\d.]+)・\(v\) 主の升目 (\S+) ([\d.]+)・門だけ ([\d.]+)', [vi_c, via[vi_c], v_main, abs(vd[v_main]), max(abs(vd[c]) for c in gate_only)])
    X('K493', r'([\d.]+) 倍', [via[vi_c] / noise])
    near = []
    for c in main_cells:
        if not rec['cells'][c].get('pass_i_ii'):
            continue
        mg = min(rec['cells'][c]['lo'] - lo_floor, lo_ceil - rec['cells'][c]['lo'])
        if mg < via[c]:
            near.append((c, mg, via[c]))
    X('K494', r"・余白 \{'N1\|O-Ncold': ([\d.]+), 'S4\|Onull': ([\d.]+)\}・\(vi\)\(a\) \{'N1\|O-Ncold': ([\d.]+), 'S4\|Onull': ([\d.]+)\}",
      [dict((c, g_) for c, g_, _ in near)['N1|O-Ncold'], dict((c, g_) for c, g_, _ in near)['S4|Onull'], via['N1|O-Ncold'], via['S4|Onull']])
    if [c for c, _, _ in near] != ['N1|O-Ncold', 'S4|Onull']:
        raise SystemExit('床からの余白が (vi) の (a) の幅より小さい升目が想定と違う（止める）: %s' % near)
    dv = {v: {c: rec['iv'][v]['lo'][c] - rec['cells'][c]['lo'] for c in rec['iv'][v]['lo']} for v in sorted(rec['iv'])}
    vmx = {v: max(d_, key=lambda c: abs(d_[c])) for v, d_ in dv.items()}
    X('K495', r'V2 (\S+) ([\d.]+)・V3 (\S+) ([\d.]+)', [vmx['V2'], abs(dv['V2'][vmx['V2']]), vmx['V3'], abs(dv['V3'][vmx['V3']])])
    same_order = [via[vi_c], abs(vd[v_main]), iq_lo, iq_hi, min(ab), max(ab)]
    if max(same_order) / min(same_order) >= 10:
        raise SystemExit('「同じ桁」が成り立たない（止める）')
    step = 0.05 / m
    b_lim = ['- %s上の限界の文の「全経路の効き目の値はまだ誰も見ていない」は、封印の前の情報状態を述べた正本の文が、凍結した器からそのまま出たもの。値は、一致だけを見る段の記録の公開（%s）の後、'
             '%s にコーディネータが登録者の許しを受けて開き、%s に同じ会話で登録者に伝えた（時刻は日本時間・開く段の記録 `records/Bl3/open-results-Bl3.md`・値はコーディネータが先に読んだ）。'
             % (TAG, OJ['pushes']['judge_3e185d3'], ev['open']['jst'], ev['told']['jst']),
             '- %s上の限界の文の「十六行の Holm の第一段…（値は §5）」の §5 は凍結の本文（`design/design-Bl3-FROZEN.md`）の §5 で、本報告の §5 ではない。下見で外した後の主の行は %d 行で、Holm の第一段は %.6f、'
             '第一段を通る外側の帰無の本数の上限は %d 本（十六行のときの %d 本と同じ・正本 `labels.first_step_margin`）。' % (TAG, m, step, kmax(m), kmax(16)),
             '- %s計算の道: 札と門は、本の計算の一つの道（バッチの大きさ %d・近道なし・%s・組の session の記録にある版）の上の記述である。道を替えたときに効き目と札がどれだけ動くかは測っていない。'
             '下見で測ったのは無操作の値の動きだけで、(vi) の (a) の升目の間の最大 %s（%s・揺れの上限 %s の %.0f 倍）・(v) の主の升目の最大 %s（%s・門の行だけの升目 %s）。'
             'これは等方の効き目の四分位の幅（%.2f〜%.2f）と主の行の効き目の大きさ（%.3f〜%.3f）と同じ桁。'
             % (TAG, batch, '・'.join(A['env']['pilot_gpu']), f4(via[vi_c]), vi_c, f4(noise), via[vi_c] / noise, f4(abs(vd[v_main])), v_main, f4(max(abs(vd[c]) for c in gate_only)), iq_lo, iq_hi, min(ab), max(ab)),
             '- %s床からの余白が (vi) の (a) の幅より小さい主の升目: %s。これらの升目が下見を通ったことも、道に依る幅の中にある。' % (TAG, '・'.join('%s（余白 %.3f・幅 %s）' % (c, g_, f4(w_)) for c, g_, w_ in near)),
             '- %s揺れの版では、無操作の値が主の書き出しから動いた（最大: %s・§1）。加えた腕の効き目が書き出しの形にどれだけ依るかは測っていない。'
             % (TAG, '・'.join('%s %s（%s）' % (v, f4(abs(dv[v][vmx[v]])), vmx[v]) for v in sorted(dv)))]

    # ---- 組み立て
    lines = frozen.split(NL)
    if lines[0] != T_FROZEN:
        raise SystemExit('凍結の報告の見出しが想定と違う（止める）')
    bl = blocks_of(lines, MB)
    want = {'status': '- 状態: **', 'reading': '- 〈', 'pilot': '- 出口の値の自己検査（下見の頭）', 'main': '| 行 | 方向 | 升目と符号 |', 'pa': '- 報告の雛形の決まり（裁定 D223）',
            'gate': '| 門 | 行 | 入れ替える単位 |', 'recompute': '- 一段目（本の器のフック と 残差の書き換え', 'predictions': '| 項目 | 結果 | 登録者 | コーディネータ |',
            'limits': '- 読み取りは直答の型の書き出しを教師強制で置いた位置で'}
    B = {}
    for key, hd in want.items():
        hit = [b for b in bl if b[2].startswith(hd)]
        if len(hit) != 1:
            raise SystemExit('凍結の報告の区画 %s が一つに決まらない（止める）: %d' % (key, len(hit)))
        B[key] = hit[0]
    s_line = lines[B['status'][0] + 1]
    if not (s_line == S_FROZEN or (a.final and confirmation is not None and s_line.startswith('- 状態: **最終版**（登録者最終確認 '))):
        raise SystemExit('凍結の報告の状態の行が想定と違う（止める）')
    ans = [i for i, l in enumerate(lines) if l == '**答えの範囲**:']
    fence_i = [i for i, l in enumerate(lines) if l == BR.FENCE]
    if len(ans) != 1 or lines[ans[0] - 1] != '' or len(fence_i) != 1 or lines[fence_i[0] - 1] != '':
        raise SystemExit('凍結の報告の起草者の欄の後か、柵の前の形が想定と違う（止める）')
    ins = []                                                   # (凍結の行の添字, 区画の中身): 添字の行の前に、空の行と区画を置く
    tables = []
    why = {'pilot': '升目の名の縦棒が表の区切りと重なるので、表示では列がずれる', 'main': '升目の名の縦棒が表の区切りと重なるので、表示では列がずれる',
           'pa': '表の前に空の行が無いので、表示では表にならず一つの段落になる。升目の名の縦棒も表の区切りと重なる'}
    for key in ('pilot', 'main', 'pa'):
        b0, b1, _ = B[key]
        blk = lines[b0 + 1:b1]
        hi, hdr, n, rix = table_of(blk)
        new_rows = [escape_row(blk[k], n) for k in rix]
        if [r_.replace(BS + '|', '|') for r_ in new_rows] != [blk[k] for k in rix]:
            raise SystemExit('並べ直しの表の行が凍結の表の行と一度ずつ合わない（止める）: %s' % key)
        tables.append({'table': key, 'rows': len(new_rows), 'columns': n, 'escaped_cells': sum(r_.count(BS + '|') for r_ in new_rows)})
        ins.append((b0, ['- %s次の区画の表は凍結した器の出力で、%s（生の md の値は正しい）。値は、この区画の後の並べ直しの表で読む。' % (TAG, why[key])]))
        ins.append((b1 + 1, ['- %s上の区画の表の並べ直し（升目の名の縦棒を逆斜線で逃がした・列と値は凍結の器の出力の表のまま）:' % TAG, '', hdr, blk[hi + 1]] + new_rows))
    ver_s16 = s16(P(VER_REL))
    head = ['- %sこの草案は、凍結した組み立ての器 `tools/build_report_Bl3.py`（SHA16 %s）の出力を同じ入力で作り直し、置き場の `records/Bl3/results-Bl3.md`（SHA16 %s）とバイトで同じことを確かめてから、'
            '見出しと状態の行を改め、%sの印の区画だけを足したもの（組み立ての器 `tools/build_report_Bl3_devBLT1.py` %s・登録者裁定 D243〜D246・採否の案 `%s`）。印の無い文と区画は凍結した器の出力のまま。'
            % (TAG, s16(BR.__file__), s16(BR.OUT), TAG, VERSION, ADOPT_REL),
            '- %s起草者の欄（「この結果が退けた説明」）の三行は、結果の巡の後に、凍結した器の口（`--rejected`）で直した（登録者裁定 D244・D246）。' % TAG,
            None]
    if a.final:
        head[0] = ('- %sこの最終版は、凍結した組み立ての器 `tools/build_report_Bl3.py`（SHA16 %s）の出力を同じ入力で作り直し、置き場の `records/Bl3/results-Bl3.md`（SHA16 %s）とバイトで同じことを確かめてから、'
                   '見出しを改め（登録者最終確認の前は状態の行も改める・確認の後の状態の行は凍結した器が出す最終版の型の行）、%sの印の区画だけを足したもの'
                   '（組み立ての器 `tools/build_report_Bl3_devBLT1.py` %s・登録者裁定 D243〜D250・起草者の最終の見直しの裁定 D251・D253・採否の案 `%s` と `%s`）。印の無い文と区画は凍結した器の出力のまま。'
                   % (TAG, s16(BR.__file__), s16(BR.OUT), TAG, VERSION, ADOPT_REL, ADOPT_FINAL_REL))   # 二度目の見直しの R-b・R-d（裁定 D253）
        head[1] = '- %s起草者の欄（「この結果が退けた説明」）の三行は、結果の巡の後（登録者裁定 D244・D246）と、最終の系統外の検分の後（一行目・登録者裁定 D248）に、凍結した器の口（`--rejected`）で直した。' % TAG
        head.append('- %s最終の系統外の検分を受けた草案の二つ目（`records/Bl3/results-Bl3-draft2.md`・SHA16 %s）から最終版で改めた行は、決めた行（見出し・状態の行・凍結の記録の SHA16 の行・逸脱の一覧の D-BLT2 の行・'
                    'この頭の添え・検分票・起草者の欄の一行目・起草者の最終の見直しで直した行（〈両方の外〉の注の二行・§5 の注の一行・裁定 D251・D253））だけ（器が確かめた・草案の二つ目のファイルは書き換えていない）。' % (TAG, s16(OUT)))   # R-d
    ins.append((B['status'][1] + 1, head))
    ins.append((ans[0] - 1, b_rej))
    ins.append((B['reading'][1] + 1, b_n1))
    ins.append((B['gate'][1] + 1, b_gate))
    ins.append((B['recompute'][1] + 1, b_rc))
    ins.append((B['predictions'][1] + 1, b_pred))
    ins.append((B['limits'][1] + 1, b_lim))
    rev = ['- %s上の検分票は、凍結した組み立ての器が結果の巡の前に出したもので、凍結の出力のまま残す。読みの型の当否と起草者の欄の文は、結果の巡で見た（採否の案 `%s`・登録者裁定 D243〜D246）。' % (TAG, ADOPT_REL),
           '- %sこの草案の検分票:' % TAG,
           '  - 対象: 報告の草案の二つ目（凍結した器の出力と、足した区画）。',
           '  - 段階: 結果の後・結果の巡の後（採否の案・登録者裁定 D243〜D246）。',
           '  - 凍結物の同定: 凍結の本文 SHA16 %s・正本 SHA16 %s。計算に使った器は凍結の記録の値のまま（凍結した組み立ての器の入力の確かめ）。' % (FR['frozen_sha16']['design/design-Bl3-FROZEN.md'], FR['frozen_sha16']['design/contrasts-Bl3.json']),
           '  - 盲検の状態: 該当しない（結果は開いた後・開く段の記録）。',
           '  - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外二票と系統内二票（一票に数える）。最終の系統外の一票はこの後（新しい個体・正本 `review_plan.final`）。',
           '  - COI記録: 起草者は器と報告と起草者の欄を書いた当人で、「正しく読めている」と書く側に引かれる。足した区画は採否の案の区分（三）の行に限り、読みを足さない。',
           '  - 本検分が確認していないこと: 最終の系統外の一票が見つけること。足した区画の文の言い過ぎ（走査器は禁止語と数の形だけを見る）。並べ直しの表の公開の置き場での表示（公開の後に確かめる）。']
    if a.final:
        rev = [('- %s上の検分票は、凍結した組み立ての器が結果の巡の前に出したもので、凍結の出力のまま残す。読みの型の当否と起草者の欄の文は、結果の巡と最終の系統外の検分で見た'
                '（採否の案 `%s` と `%s`・登録者裁定 D243〜D250）。') % (TAG, ADOPT_REL, ADOPT_FINAL_REL),
               '- %s最終版の検分票:' % TAG,
               '  - 対象: 報告の最終版（凍結した器の出力と、足した区画）。',
               '  - 段階: 結果の後。結果の巡の後（登録者裁定 D243〜D246）と、最終の系統外の検分の後（登録者裁定 D247〜D250）と、起草者の最終の見直しの後（登録者裁定 D251・D253）。',   # R-d
               rev[4], rev[5],
               '  - 系統の内訳: 組み立てはコーディネータ（Claude 系）一名。結果の巡は系統外二票と系統内二票（一票に数える）。最終の系統外の検分は新しい個体の二票で、正本の一票を二票にした（逸脱 D-BLT2・同じ機種を選んだ二票は会話が別でも相関しうる）。'
               '起草者の最終の見直しは起草者自身のもので、外の目ではない。',
               '  - COI記録: 起草者は器と報告と起草者の欄を書いた当人で、「正しく読めている」と書く側に引かれる。足した区画は採否の案の区分（三）の行に限り、読みを足さない。最終版で改めた行は、最終の検分の二票の所見と起草者の最終の見直しの所見のうち、裁定で決めた行に限った。',   # R-d
               '  - 本検分が確認していないこと: 最終版で改めた行は、もう一度の検分を経ていない（正本 `review_plan.no_more`）。足した区画の文の言い過ぎ（走査器は禁止語と数の形だけを見る）。']
    ins.append((fence_i[0] - 1, rev))

    def compose(n_cross):
        head[2] = '- %s印の区画の数は記録（集計の記録・組の出力・下見の記録・設計事実・開く段の記録）から器が読み、そのうち結果の巡の再現の記録（`%s`・SHA16 %s）にある数は、その記録の値と照らした（照らした記録の項 %d・外れ 0）。' % (
            TAG, VER_REL, ver_s16, n_cross)
        L = list(lines)
        for idx, blk in sorted(ins, key=lambda x: x[0], reverse=True):
            L[idx:idx] = ['', MB['begin']] + blk + [MB['end']]
        L[0] = T_FINAL if a.final else T_DRAFT
        if not (a.final and confirmation is not None):
            st = [i for i, l in enumerate(L) if l == S_FROZEN]
            if len(st) != 1:
                raise SystemExit('状態の行が一つに決まらない（止める）')
            L[st[0]] = S_FINAL_PRE if a.final else S_DRAFT
        return NL.join(L)

    text = compose(len(X.done))

    # ---- 確かめ: 足した区画を除き、見出しと状態の行を戻すと、凍結の報告とバイトで同じ
    Lt = text.split(NL)
    back, i, n_added = [], 0, 0
    while i < len(Lt):
        if Lt[i] == '' and i + 2 < len(Lt) and Lt[i + 1] == MB['begin'] and Lt[i + 2].startswith('- ' + TAG) and not Lt[i + 2].startswith('- ' + TAG + '**'):
            j = Lt.index(MB['end'], i + 1)
            i, n_added = j + 1, n_added + 1
            continue
        back.append(Lt[i])
        i += 1
    back[0] = T_FROZEN if back[0] in (T_DRAFT, T_FINAL) else back[0]
    back = [S_FROZEN if l in (S_DRAFT, S_FINAL_PRE) else l for l in back]
    if NL.join(back) != frozen or n_added != len(ins):
        raise SystemExit('足した区画を除いても凍結の報告に戻らない（止める）: 足した区画 %d・数えた %d' % (len(ins), n_added))
    V_, side = BR.lint_report(text, T3)
    if V_:
        raise SystemExit('走査の違反（止める）: %s' % [(v['kind'], v['line'], v['token']) for v in V_][:8])
    out, chk_path = (OUT_FINAL, CHECKS_FINAL) if a.final else (OUT, CHECKS)
    cmp = None
    if a.final:                                        # v2: 検分を受けた草案の二つ目（書き換えない）と比べ、変わった行が決めた行だけであることを確かめる
        import difflib
        d2 = open(OUT, encoding='utf-8').read().replace('\r\n', NL).split(NL)
        fl = text.split(NL)
        gone, came = [], []
        for tg_, i1, i2, j1, j2 in difflib.SequenceMatcher(None, d2, fl, autojunk=False).get_opcodes():
            if tg_ in ('replace', 'delete'):
                gone += d2[i1:i2]
            if tg_ in ('replace', 'insert'):
                came += fl[j1:j2]

        def block_lines(Ls, prefix):
            hit_ = [k for k, l in enumerate(Ls) if l == MB['begin'] and k + 1 < len(Ls) and Ls[k + 1].startswith(prefix)]
            if len(hit_) != 1:
                raise SystemExit('区画が一つに決まらない（止める）: %s' % prefix[:30])
            return Ls[hit_[0] + 1:Ls.index(MB['end'], hit_[0])]
        fr_line = lambda Ls: [l for l in Ls if l.startswith('- 正本 `design/contrasts-Bl3.json` SHA16')]
        rej1 = lambda Ls: [l for l in Ls if l.startswith('- 「この大きさの加減では')]
        share1 = lambda Ls: [l for l in Ls if l.startswith('  - 等方の最上位の割合 ')]         # 起草者の最終の見直しの直し（裁定 D251）
        last1 = lambda Ls: [l for l in Ls if l.startswith('  - これらは札と型を変えない。')]     # 二度目の見直しの R-a（裁定 D253）
        rc1 = lambda Ls: [l for l in Ls if l.startswith('- ' + TAG + '独立の再計算の範囲は')]  # 二度目の見直しの R-c（裁定 D253）
        for f_ in (share1, last1, rc1):
            if len(f_(d2)) != 1 or len(f_(fl)) != 1:
                raise SystemExit('決めた行が一つに決まらない（止める）')
        ok_gone = ({T_DRAFT, S_DRAFT} | set(fr_line(d2)) | set(rej1(d2)) | set(share1(d2)) | set(last1(d2)) | set(rc1(d2)) | set(block_lines(d2, '- ' + TAG + 'この草案は'))
                   | set(block_lines(d2, '- ' + TAG + '上の検分票は')))
        ok_came = ({T_FINAL} | {l for l in fl if l.startswith('- 状態: **')} | set(fr_line(fl)) | set(rej1(fl)) | set(share1(fl)) | set(last1(fl)) | set(rc1(fl))
                   | {l for l in fl if l.startswith('- 【逸脱 D-BLT2】')}
                   | set(block_lines(fl, '- ' + TAG + 'この最終版は')) | set(block_lines(fl, '- ' + TAG + '上の検分票は')))
        bad_g, bad_c = [l for l in gone if l not in ok_gone], [l for l in came if l not in ok_came]
        if bad_g or bad_c:
            raise SystemExit('草案の二つ目から、決めていない行が変わった（止める）: 消えた %s・足された %s' % ([l[:50] for l in bad_g], [l[:50] for l in bad_c]))
        cmp = {'draft2': 'records/Bl3/results-Bl3-draft2.md', 'draft2_sha16': s16(OUT), 'removed_lines': len(gone), 'added_lines': len(came),
               'allowed': '見出し・状態の行・凍結の記録の SHA16 の行・逸脱の一覧の D-BLT2 の行・頭の添え・検分票・起草者の欄の一行目・〈両方の外〉の注の等方の最上位の割合の一行（裁定 D251）と末の一行・§5 の注の一行（裁定 D253）'}
    ck = {'what': ('報告の最終版の確かめ' if a.final else '報告の草案の二つ目の確かめ') + '（逸脱 D-BLT1 の器 %s）' % VERSION,
          'sha16': {'tools/build_report_Bl3.py': s16(BR.__file__), 'records/Bl3/results-Bl3.md': s16(BR.OUT), 'tools/build_report_Bl3_devBLT1.py': s16(os.path.abspath(__file__)), VER_REL: ver_s16,
                    'records/Bl3/open-results-Bl3.json': s16(OPEN), 'records/Bl3/report-marks-Bl3.json': s16(MARKS), 'records/Bl3/results-rejected-lines-Bl3.md': s16(REJ)},
          'frozen_rebuilt_equal': True, 'added_blocks': n_added, 'strip_back_equal': True, 'tables': tables, 'lint_violations': 0, 'cross_checks': X.done,
          'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    if cmp:
        ck['draft2_compare'] = cmp
        ck['sha16']['records/Bl3/results-Bl3-draft2.md'] = s16(OUT)
    if os.path.exists(out) and not a.force:
        if text != open(out, encoding='utf-8').read().replace('\r\n', NL):
            raise SystemExit('既にある出力と、組んだ文が違う（止める・--force で書き直す）: %s' % os.path.relpath(out, REPO))
        print('既にある出力と同じ（書かない）: %s' % os.path.relpath(out, REPO))
        return
    open(out, 'w', encoding='utf-8', newline=NL).write(text)
    RL.write_sidecar(out, text, T3, 'tools/build_report_Bl3_devBLT1.py %s' % VERSION)
    open(out.replace('.md', '-lint.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(['# 報告の走査（凍結した `tools/report_lint.py` の lint・禁止語は正本の四つの一覧の和・逸脱 D-BLT1 の器が呼んだ）', '', '- 違反 0', '', BR.FENCE, '']))
    json.dump(ck, open(chk_path, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('wrote %s（走査の違反 0・足した区画 %d・並べ直した表 %s・再現の記録と照らした項 %d%s）' % (os.path.relpath(out, REPO), n_added, [(t['table'], t['rows']) for t in tables], len(X.done),
                                                                  ('・草案の二つ目から消えた行 %d・足された行 %d' % (cmp['removed_lines'], cmp['added_lines'])) if cmp else ''))


if __name__ == '__main__':
    main()
