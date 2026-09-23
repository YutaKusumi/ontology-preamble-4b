# -*- coding: utf-8 -*-
"""build_report_Blens.py v1 —— B-lens の結果の報告の草案を組む（2026-09-23・正本 `reading_rules`・`reading_notes`・`negation_templates`・`report_rules`・§5）。

組み立て:
  - 数はすべて機械の区画（`report_rules.machine_block` の印）の中に置く。区画ごとの中身の SHA16 を別の記録（報告と同じ名の -machine.json）に書く（段階 A の型）。
  - 読みの型は、正本の読みの表の条件を器が当て、当たった型の「書くこと」と、外でない物差しの「外でないとき書くこと」を並べる（型は重なりうる・読みの決まり）。
    各型の文に、実在の差の中の順位（M_E は語の側の帰無の割合）を一行添える。書かないことは走査の禁止語にする。
  - 語の一覧の語は報告に載せない（数える記述だけ）。語は別の記録（lists-Blens.md）に器が並べる（語を拾って物語を作らない・読みの決まり）。
  - 予想の照合: 封印した二つの予想の JSON の各欄と、器が決めた結果の値を並べる（照合は記録であり評価ではない）。
走査: 凍結した走査器 `tools/report_lint.py` の関数 `lint` を、正本の禁止語（価値語・機序語）に読みの表の「書かないこと」から器で作った語（`print_strings.reading_never_ban`）を足して呼ぶ。
  違反があれば非零で終わる。
出力: records/Blens/results-Blens.md・results-Blens-machine.json・results-Blens-lint.md・lists-Blens.md（--force が無ければ上書きしない）。
用法: python tools/build_report_Blens.py [--force] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import report_lint as RL
import make_predictions_form_Blens as FORM

VERSION = 'v1'
NL = chr(10)
OUT = os.path.join(REPO, 'records', 'Blens', 'results-Blens.md')
LISTS = os.path.join(REPO, 'records', 'Blens', 'lists-Blens.md')
FENCE = '本報告のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
f4 = lambda x: 'なし' if x is None else ('%.4g' % x)
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def label_cat(iso, second):
    return {(True, True): '両方', (True, False): '等方の外だけ', (False, True): '二つ目の札だけ', (False, False): '付かない'}[(bool(iso), bool(second))]


def outcomes(TL, lens, calib):
    """予想の欄ごとの、器が決めた結果の値（予想の書式の選択肢の字で）。"""
    P = lens['primary']['metrics']
    o = {}
    for fam in ('survival', 'nuclear'):
        for p_, m, pos in (('p1', 'M_L_%s' % fam, '破局の文字の側'), ('p2', 'M_X_%s' % fam, '破局の選択肢の語の側')):
            x = P[m]
            cat = label_cat(x['iso_outside'], x['second'])
            o['%s.%s.label' % (p_, fam)] = cat
            o['%s.%s.dir' % (p_, fam)] = FORM.NP if cat == '付かない' else (pos if x['value'] > 0 else '反対')
    for p_, m, pos, neg in (('p3', 'M_E', 'O の語の側', 'Osec の語の側'), ('p4', 'M_F', 'コードブロックの書き出しを押し上げる', '押し下げる')):
        x = P[m]
        cat = label_cat(x['iso_outside'], x['second'])
        o['%s.label' % p_] = cat
        o['%s.dir' % p_] = FORM.NP if cat == '付かない' else (pos if x['value'] > 0 else neg)
    sel = lens['primary']['ratio']
    o['p5.answer'] = '大きい' if lens['layers'][sel]['directions']['static']['M_E_static']['real_rank']['top'] else '大きくない'
    pm = calib['passed_metrics']
    o['p6.gate'] = '両方' if len(pm) == 2 else ('M_L で通る' if pm == ['M_L'] else ('M_X で通る' if pm == ['M_X'] else '通らない'))
    o['p6.without_vhat'] = '通る' if any(calib['gates']['without_vhat'][m]['pass'] for m in TL['calibration']['tests']) else '通らない'
    mg = calib.get('magnitude')
    if mg:
        s = mg['summary']
        o['p7.answer'] = '無い' if s['at_or_above'] == 0 else ('全部' if s['at_or_above'] == s['ratio_rows'] else '一部')
    else:
        o['p7.answer'] = '（大きさの目盛りの出力が無い）'
    o['p8.answer'] = '同じ向き' if calib['s4_control']['rand0_same_sign_as_loaded_MF'] else '逆向き'
    return o


def reading_types(TL, lens, calib):
    """読みの表の条件を当てる。戻り値: [(型, 当たった物差し, 書くこと)] と、外でない物差しの否定の文。"""
    P = lens['primary']['metrics']
    RR = {r['type']: r for r in TL['reading_rules']}
    hit, neg = [], []
    by_type = {'M_E': '語の反響', 'M_X_survival': '選択肢の語', 'M_X_nuclear': '選択肢の語', 'M_L_survival': '答えの文字', 'M_L_nuclear': '答えの文字', 'M_F': '様式'}
    for m, t in by_type.items():
        if P[m]['iso_outside']:
            hit.append((t, m, RR[t]['write']))
        else:
            neg.append((t, m, RR[t]['write_neg']))
    if not any(P[m]['iso_outside'] for m in P):
        hit.append(('区別できない', '主の六つ', RR['区別できない']['write']))
    for m in P:
        if P[m]['iso_outside'] and not P[m]['second']:
            hit.append(('埋もれる', m, RR['埋もれる']['write']))
        if not P[m]['iso_outside'] and P[m]['second']:
            hit.append(('二つ目の札だけ', m, RR['二つ目の札だけ']['write']))
    if calib['gate_passed']:
        hit.append(('門を通った', '・'.join(calib['passed_metrics']), RR['門を通った']['write']))
    else:
        hit.append(('門を通らない', '門', RR['門を通らない']['write']))
    return hit, neg


def both_wording(TL, m):
    """両方の札が付いたときの言い方（正本 primary.print_rule の「」の中の二つの句を器で切り出す・M_E は後の句）。"""
    import re
    qs = re.findall(r'「([^」]*)」', TL['primary']['print_rule'])
    assert len(qs) == 2, qs
    return qs[1] if m == 'M_E' else qs[0]


def machine(lines, MB):
    return [MB['begin']] + lines + [MB['end']]


def build(TL, lens, calib, SJ, seal, preds, meta):
    MB = RL.machine_block(TL)
    P = lens['primary']['metrics']
    sel = lens['primary']['ratio']
    L = ['# B-lens の結果（報告の草案・機械の組み立て）', '',
         '- 起草: 南無弥勒如来（コーディネータ）／登録者: 楠見優太。**状態: 報告の草案（結果の巡の前）**。組み立ての器: `tools/build_report_Blens.py`。',
         '- 位置づけ: 段階 B の後の登録外の記述（小さな登録）。段階 B の札・報告・逸脱台帳には触れない。', '']
    L += machine(['- 正本 `design/contrasts-Blens.json` SHA16 %s・凍結の語の集合 `records/Blens/sets-Blens.json` SHA16 %s・封印の記録 SHA16 %s・層一の記録 SHA16 %s・層二の記録 SHA16 %s。' % (
        meta['canon'], meta['sets'], meta['seal'], meta['lens'], meta['calib'])], MB)
    L += ['', '## 0. 要約（できないことから）', '', '**この登録で答えられないこと**:', ''] + machine(['- ' + x for x in TL['scope']['not_answered']], MB)
    hit, neg = reading_types(TL, lens, calib)
    L += ['', '**主の記述の札と門**（v̂・選んだ層・機械の出力）:', '']
    L += machine(['- %s: 値 %s・等方の割合 %s（段 %s）・等方の外 %s・二つ目の札 %s・札の分類「%s」' % (
        m, f4(x['value']), f4(x['p_iso']), f4(x['holm_step']), 'はい' if x['iso_outside'] else 'いいえ', 'はい' if x['second'] else 'いいえ', label_cat(x['iso_outside'], x['second'])) for m, x in P.items()]
        + ['- 門（方向を単位にした並べ替え）: %s・v̂ を抜いた門で同じ物差しも通った物差し: %s' % (
            ('通った（%s）' % '・'.join(calib['passed_metrics'])) if calib['gate_passed'] else '通らない', '・'.join(calib['link_vhat_metrics']) or 'なし')], MB)
    L += ['', '**読みの型**（正本の読みの表の条件を器が当てた・型は重なりうる）:', '']
    L += machine(['- 〈%s〉（%s）: %s' % (t, m, w) for t, m, w in hit] + ['- 外でない（%s・%s）: %s' % (t, m, w) for t, m, w in neg], MB)
    L += ['', '**打ち消しの定型**:', ''] + machine(['- ' + x for x in TL['negation_templates']], MB)
    # 1. 主の記述の札
    L += ['', '## 1. 主の記述の札（v̂・選んだ層）', '']
    rows = ['| 物差し | 値 | 等方の割合 | Holm の段 | 等方の外 | 二つ目の札 | 二つ目の札の中身 |', '|---|---|---|---|---|---|---|']
    for m, x in P.items():
        d = x['second_detail']
        det = ('語の側の帰無の割合 %s' % f4(d['word_side_p'])) if 'word_side_p' in d else ('実在の差の中の順位 %d／%d' % (d['rank'], d['of']))
        rows.append('| %s | %s | %s | %s | %s | %s | %s |' % (m, f4(x['value']), f4(x['p_iso']), f4(x['holm_step']), 'はい' if x['iso_outside'] else 'いいえ', 'はい' if x['second'] else 'いいえ', det))
    rows.append('- 偶然で一つ付く割合の目安（和の上限・実在の差の札）: %s' % f4(lens['primary']['chance_one_label']))
    L += machine(rows, MB)
    L += [''] + machine(['- 両方の札が付いた物差しの言い方: %s' % ('・'.join('%s は「%s」' % (m, both_wording(TL, m)) for m, x in P.items() if x['iso_outside'] and x['second']) or 'なし'),
                         '- ' + TL['primary']['note']], MB)
    # 2. 門
    L += ['', '## 2. 門（層二）', '']
    rows = ['| 門 | 物差し | 行の数 | 入れ替えの数 | 順位相関 | 割合 | Holm の段 | 通る |', '|---|---|---|---|---|---|---|---|']
    for g, res in calib['gates'].items():
        for m, x in res.items():
            rows.append('| %s | %s | %d | %d | %s | %s | %s | %s |' % (g, m, x['n_rows'], x['n_perm'], f4(x['rho']), f4(x['p']), f4(x.get('holm_step')), {True: 'はい', False: 'いいえ', None: '記述'}[x.get('pass')]))
    for m, x in calib['descriptive'].items():
        rows.append('- 記述（%s）: 行の単位の順位相関 %s・ランダム方向の行だけ %s・崩れの行を除いた門の順位相関 %s（割合 %s・除いた行 %s）' % (
            m, f4(x['row_rho']), f4(x['random_rows_rho']), f4(x['without_collapse']['rho']), f4(x['without_collapse']['p']), '・'.join(x['collapse_rows']) or 'なし'))
    s4 = calib['s4_control']
    rows.append('- S4 の自然の対照（記述・偶然なら六分の一）: M_F の上の二本 %s・M_Lc の上の二本 %s・(6b) と一本目がそろって上の二本: M_F %s・M_Lc %s・一本目は (6b) と M_F で同じ向き: %s' % (
        '・'.join(s4['M_F']['top2']), '・'.join(s4['M_Lc']['top2']), 'はい' if s4['M_F']['loaded_and_rand0_top2'] else 'いいえ', 'はい' if s4['M_Lc']['loaded_and_rand0_top2'] else 'いいえ',
        'はい' if s4['rand0_same_sign_as_loaded_MF'] else 'いいえ'))
    for t in calib.get('tune', []):
        rows.append('- 調整走行（記述）: %s・層 %s・係数 %s: %s' % (t['scenario'], t['layer'], t['coef'], '・'.join(
            '%s の v̂ の順位（行動 %d・押し %d・組の中の順位相関 %s）' % (m, t[m]['vhat_rank_behaviour'], t[m]['vhat_rank_push'], f4(t[m]['rho'])) for m in TL['calibration']['tests'])))
    L += machine(rows, MB)
    L += [''] + machine(['- ' + TL['calibration']['link_rule'], '- ' + TL['calibration']['or_note']], MB)
    # 3. 大きさの目盛り
    L += ['', '## 3. 大きさの目盛り（層二）', '']
    mg = calib.get('magnitude')
    if mg:
        rows = ['- 手元の logits の突き合わせ（最初の一件）: %s' % '・'.join('%s 最大の差 %s・最上位 %s' % (k, f4(v['max_abs']), '同じ' if v['argmax_equal'] else '違う') for k, v in (mg['logit_check_local'] or {}).items())]
        cc = mg.get('colab_check') or {}
        for key, v in (cc.get('calibration') or {}).items():
            rows.append('- 較正の検査（%s）: 主位置 変換の後の確率 %s・観測 %d／%d・区間 %d〜%d・%s%s' % (
                key, f4(v['main']['p_T']), v['main']['k'], v['main']['n'], v['main']['interval'][0], v['main']['interval'][1], '内' if v['main']['inside'] else '外',
                ''.join('／答えの文字 %s: %s・%d／%d・%s' % (x, f4(y['p_T']), y['k'], y['n'], '内' if y['inside'] else '外') for x, y in (v.get('letter') or {}).items())))
        rows += ['', '| 行 | z | 観測の変化 | 変換の後の確率（前→後） | 直接の経路の変化 | 比（pt） | 読み | 対数オッズの比 | 印 |', '|---|---|---|---|---|---|---|---|---|']
        for x in mg['main_rows']:
            if not x['eligible']:
                continue
            marks = [m_ for m_, f_ in (('土台か行の率が零か一', x.get('rate_edge')), ('対数オッズが定まらない', x.get('logodds_undefined'))) if f_]
            rows.append('| %s | %s | %s | %s→%s | %s | %s | %s | %s | %s |' % (x['row'], f4(x['z']), f4(x['obs_diff']), f4(x['pT_before']), f4(x['pT_after']), f4(x['dp']),
                                                                         f4(x['ratio']), x['reading'], f4(x.get('ratio_logodds')), '・'.join(marks) or 'なし'))
        s = mg['summary']
        rows.append('- 比を出した行 %d・読みの比（%s）以上 %d・満たない %d・逆向き %d。ほかの行は「比を出さない」。' % (s['ratio_rows'], f4(s['reading_ratio']), s['at_or_above'], s['below'], s['reverse']))
        for key, v in mg['letter'].items():
            rows.append('- 答えの文字の位置（記述・%s・文脈 %d）: 層一の M_L と正確な直接の経路の順位の一致 %s' % (key, v['n_contexts'], f4(v['rank_agreement_ML_exact'])))
        L += machine(rows, MB)
        L += [''] + machine(['- 読みの文（正本）: ' + TL['magnitude']['reading'], '- ' + TL['magnitude']['vhat_note']], MB)
    else:
        L += ['- 大きさの目盛りの出力が無い（Colab の相 extract の出力を読んでいない）。']
    # 4. 記述の表（層一）
    L += ['', '## 4. 記述の表（層一・札を付けない）', '']
    rows = []
    for r, lay in lens['layers'].items():
        rows.append('- 層の割合 %s:' % r)
        for name, mv in lay['directions'].items():
            main_ms = [m for m in ('M_L_survival', 'M_L_nuclear', 'M_X_survival', 'M_X_nuclear', 'M_Lc', 'M_R_survival', 'M_F', 'M_F_sens') if m in mv] + [m for m in mv if m.startswith('M_E_') and ':' not in m and mv[m]['own']]
            rows.append('  - %s: %s' % (name, '・'.join('%s %s（等方 %s・実在の差 %d／%d）' % (m, f4(mv[m]['value']), f4(mv[m]['p_iso']), mv[m]['real_rank']['rank'], mv[m]['real_rank']['of']) for m in main_ms)))
    L += machine(rows, MB)
    # 5. 語の側の帰無
    ws = lens['word_side']
    L += ['', '## 5. 語の側の帰無（v̂ の M_E・選んだ層）', '']
    L += machine(['- M_E %s・両側に等しい裾の割合 %s・帰無の平均 %s・中央値 %s・標準偏差 %s（抽選 %d）・語の側の帰無の外: %s' % (
        f4(ws['m']), f4(ws['p']), f4(ws['null_mean']), f4(ws['null_median']), f4(ws['null_sd']), ws['draws'], 'はい' if ws['outside'] else 'いいえ')]
        + (['- 感度（B の無操作の出力に現れたトークンに限る）: 割合 %s・帰無の平均 %s' % (f4(ws['sens']['p']), f4(ws['sens']['null_mean']))] if ws.get('sens') else []), MB)
    # 6. 語の一覧（数える記述だけ）
    L += ['', '## 6. 語の一覧（数える記述・語は報告に載せない）', '', '- 語は別の記録 `records/Blens/lists-Blens.md` に器が並べた。一覧は数える記述で読み、語を拾って読まない。', '']
    rows = []
    for k, v in lens['lists'].items():
        rows.append('- %s: 上位の集合の数 %s・種類 %s／下位の集合の数 %s・種類 %s' % (k, json.dumps(v['top_counts'], ensure_ascii=False, sort_keys=True), json.dumps(v['top_kinds'], ensure_ascii=False, sort_keys=True),
                                                                   json.dumps(v['bottom_counts'], ensure_ascii=False, sort_keys=True), json.dumps(v['bottom_kinds'], ensure_ascii=False, sort_keys=True)))
    L += machine(rows, MB)
    # 7. 封印の後の記述
    L += ['', '## 7. 封印の後の記述（札を付けない）', '']
    rows = []
    for k, v in lens['descriptive_after_seal'].items():
        if k.startswith('iso@'):
            rows.append('- %s: ‖g⊙u‖／‖u‖ の平均 %s（標準偏差 %s）' % (k, f4(v['gu_over_u_mean']), f4(v['gu_over_u_sd'])))
        else:
            rows.append('- %s: ‖g⊙u‖／‖u‖ %s・上位の次元の割合 %s・一覧の語のノルムの語彙の中の割合（上位 %s・下位 %s）' % (
                k, f4(v['gu_over_u']), f4(v['top_dims_share']), f4(v['list_norm_pct']['top']), f4(v['list_norm_pct']['bottom'])))
    L += machine(rows, MB)
    # 8. 予想の照合
    L += ['', '## 8. 予想の照合（記録であり評価ではない）', '', '- 的中は誰の判断の重みも変えない。照合は記録であり評価ではない。', '']
    oc = outcomes(TL, lens, calib)
    rows = ['| 欄 | 結果 | 登録者 | コーディネータ |', '|---|---|---|---|']
    for k in [k for p_, fs in FORM.FIELDS for k, _, _ in fs]:
        cell = lambda who: '%s（%s）' % (preds[who].get(k, '—'), '予想しない' if preds[who].get(k) == FORM.NP else ('一致' if preds[who].get(k) == oc.get(k) else '不一致'))
        rows.append('| %s | %s | %s | %s |' % (k, oc.get(k), cell('registrant'), cell('coordinator')))
    L += machine(rows, MB)
    # 9. 限界
    L += ['', '## 9. 限界（正本の限界の文）', ''] + machine(['- ' + x for x in TL['limits']], MB)
    L += ['', '## 検分票', '', '- 対象: 本報告の草案（機械の組み立ての出力）。', '- 段階: 結果の後（封印の後・凍結した器で計算した）。',
          '- 本検分が確認していないこと: 読みの型の当否は結果の巡で見る。', '', FENCE, '']
    return NL.join(L)


def lint_report(text, TL):
    T_scan = json.loads(json.dumps(TL))
    T_scan['print_strings']['mechanism_word_ban'] = list(T_scan['print_strings']['mechanism_word_ban']) + [w for w in TL['print_strings']['reading_never_ban'] if w not in T_scan['print_strings']['mechanism_word_ban']]
    side = {'blocks': RL.block_hashes(text, TL)}
    return RL.lint(text, T_scan, frozenset(), sidecar=side), side


def lists_md(lens):
    L = ['# B-lens の語の一覧（機械生成・`tools/build_report_Blens.py`・語を拾って読まない）', '']
    for k, v in lens['lists'].items():
        for side in ('top', 'bottom'):
            L.append('- %s・%s: %s' % (k, side, '・'.join('%d「%s」%s' % (x['id'], x['s'].replace(NL, '⏎'), ('〔%s〕' % '・'.join(x['marks'])) if x['marks'] else '') for x in v[side])))
    L += ['', FENCE, '']
    return NL.join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    import blens_lens as BL
    BL.require_sealed(TL)
    if os.path.exists(OUT) and not a.force:
        raise SystemExit('既にある: %s' % OUT)
    lens = json.load(open(BL.OUT, encoding='utf-8'))
    import blens_calib as BC
    calib = json.load(open(BC.OUT, encoding='utf-8'))
    SJ = json.load(open(BL.SETS, encoding='utf-8'))
    seal = json.load(open(BL.SEAL, encoding='utf-8'))
    preds = {r: json.load(open(os.path.join(REPO, *v['path'].split('/')), encoding='utf-8')) for r, v in seal['predictions'].items()}
    meta = {'canon': sha16f(os.path.join(REPO, 'design', 'contrasts-Blens.json')), 'sets': sha16f(BL.SETS), 'seal': sha16f(BL.SEAL), 'lens': sha16f(BL.OUT), 'calib': sha16f(BC.OUT)}
    text = build(TL, lens, calib, SJ, seal, preds, meta)
    V, side = lint_report(text, TL)
    open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
    RL.write_sidecar(OUT, text, TL, 'tools/build_report_Blens.py %s' % VERSION)
    open(LISTS, 'w', encoding='utf-8', newline=NL).write(lists_md(lens))
    lint_path = OUT.replace('.md', '-lint.md')
    open(lint_path, 'w', encoding='utf-8', newline=NL).write(NL.join(['# 報告の走査（凍結した `tools/report_lint.py` の lint・禁止語は正本の三つの一覧の和）', '', '- 違反 %d' % len(V)] +
                                                                  ['- %s（%s 行目）: %s' % (v['kind'], v['line'], v['token']) for v in V] + ['', FENCE, '']))
    print('wrote %s（走査の違反 %d）' % (os.path.relpath(OUT, REPO), len(V)))
    if V:
        raise SystemExit('報告の走査に違反がある（非零で終わる）')


def _selftest():
    """合成の層一・層二の出力で報告を組み、走査が通ることと、禁止語を入れた報告が止まることを確かめる。"""
    import blens_lens as BL, blens_calib as BC
    import numpy as np
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    TL2 = json.loads(json.dumps(TL))
    TL2['nulls']['isotropic']['count'] = 1000
    TL2['nulls']['word_side']['draws'] = 200
    V_, d_ = 400, 48
    Wm, g, mu, dirs, arm_means, b_rand, rng = BL.synth_bundle(d=d_, V=V_)
    SJ = BL.synth_sets(rng, V_)
    lens = BL.layer1(TL2, SJ, lambda ids: [Wm[int(i)] for i in ids], mu, g, dirs, arm_means, b_rand, lambda U: (Wm @ (np.asarray(U, dtype=np.float32) * g[None, :]).T),
                     lambda i: 'w%d' % i, np.linalg.norm(Wm * g[None, :], axis=1), V_)
    lens = json.loads(json.dumps(lens))
    units = list(TL['calibration']['directions'])
    per_unit = {'static': 8, 'loaded': 1, 'Nk': 8, 'td': 8, 'rand:0': 13, 'rand:1': 13, 'rand:2': 13}
    rows = []
    for u in units:
        for i in range(per_unit[u]):
            f = ('nuclear', 'survival')[i % 2]
            rows.append({'scenario': 'S1' if f == 'survival' else 'N1', 'arm': 'X', 'base_arm': 'Y', 'unit': u, 'sign': 1, 'fam': f, 'eligible': True, 'collapse': False,
                         'y': rng.normal(), 'k': 1, 'n': 2, 'k0': 1, 'n0': 2})
    values_of = lambda u, m: lens['layers']['0.5']['directions'][u][m]['value']
    calib = BC.gate_part(TL, rows, values_of)
    calib['s4_control'] = BC.s4_control(values_of)
    calib['tune'] = []
    calib = json.loads(json.dumps(calib))
    preds = {'registrant': {'p1.survival.label': '付かない', 'p8.answer': '同じ向き'}, 'coordinator': {'p1.survival.label': '両方', 'p8.answer': '逆向き'}}
    meta = {k: '0123456789ABCDEF' for k in ('canon', 'sets', 'seal', 'lens', 'calib')}
    text = build(TL, lens, calib, SJ, None, preds, meta)
    V, side = lint_report(text, TL)
    assert V == [], V[:5]
    bad = text.replace('## 9. 限界', '## 9. 限界（効いた）', 1)
    V2, _ = lint_report(bad, TL)
    assert any(v['kind'] == '価値語' for v in V2), V2[:3]
    bad2 = text.replace('## 9. 限界', '## 9. 限界（v̂ に特有）', 1)
    V3, _ = lint_report(bad2, TL)
    assert any(v['token'] == 'v̂ に特有' for v in V3), V3[:3]
    bad3 = text.replace('## 9. 限界', '## 9. 限界 12 件', 1)
    V4, _ = lint_report(bad3, TL)
    assert any(v['kind'] == '未登録の数' for v in V4), V4[:3]
    print('[build_report_Blens] 自己検査 OK（合成の報告の走査の違反 0・禁止語と未登録の数を入れた報告は止まる）')


if __name__ == '__main__':
    main()
