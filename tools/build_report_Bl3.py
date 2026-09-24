# -*- coding: utf-8 -*-
"""build_report_Bl3.py v1 —— B-lens 層三（Bl3）の結果の報告の草案を組む（2026-09-25・正本 `reading_rules`・`negation_templates`・`report_rules`・`labels`・`limits`）。

組み立て（B-lens の組み立ての器 `tools/build_report_Blens.py` の型）:
  - 数はすべて機械の区画（凍結の走査器 `tools/report_lint.py` の区画の印）の中に置く。区画ごとの中身の SHA16 を別の記録（報告と同じ名の -machine.json）に書く。
  - 頭に、凍結の後の逸脱の一覧（凍結の記録の `deviations`・台帳から器が読む）と、下見をやり直したときの一度目の下見の記録と機械の決定（裁定 D222）を置く。
  - 状態は機械の区画で、登録者最終確認の前と後の二つの型（確認の後は逐語と時刻・`records/Bl3/final-confirmation-Bl3.json`・裁定 D199 の型）。
  - §0 に「見ていない場所」（正本 `scope.not_answered`）と「この結果が退けた説明」を置く。後者は正本に文が無いので起草者の欄（〔〕）にし、`--rejected` で起草者の行を受ける
    （欄が埋まらなければ走査が埋め残しとして止める）。答えの言い方には読み取りの位置の範囲を添える（正本 `scope.reach` と打ち消しの定型）。
  - 読みの型は、正本の読みの表の条件を器が当て、当たった型の「書くこと」を並べる（型は重なりうる）。「下見で止めた」の二つの文は、止まった理由で器が選ぶ。
    等方の外の行には、等方の帰無の中央値と効き目の側（正本 `labels.side_rule` の〔〕の三つの言い方を器が切り出す）を添える。
  - 主の表に、行ごとの p と裾の本数・等方の中央値・効き目の側・二つ目の札の中心と順位・等方の最上位の割合と、段階 B のその行の札と注を並べる。
    升目と符号ごとの無操作の選択肢 a の文字の確率（裁定 D223）と、質量が `pilot.mass_min` を下回った方向の数を、主の表の隣に並べる。
  - 下見の記録（`pilot.decision.report` に並べるもの）・門（本の門・v̂ を抜いた門・記述の門・段階 B の注のある門の行）・記述（頭の確かめ・層ごとの差分の置き場・乙と
    B-lens の直接の経路）・独立の再計算の二段・予想の照合（記録であり評価ではない）・限界・情報状態。
  - 逸脱の印を受け取る口（`--marks`: 節の鍵 → 逸脱の番号の並び）。印は節の頭の機械の区画に置く。
  - 掃き出し（`tools/sweep_Bl3.py`）: 正本と凍結の本文が求める出力の一覧を、集計の出力と突き合わせ、欠けがあれば止める。
走査: 凍結した走査器 `tools/report_lint.py` の関数 `lint` を、正本の禁止語（価値語・機序語）に `print_strings.added_ban` と `print_strings.reading_never_ban` を足して呼ぶ。
  違反があれば、報告を書いた後に非零で終わる。
入力: 集計の器の結果を開く段の出力（`records/Bl3/analysis-Bl3.json`）・一致だけを見る段の記録・凍結の記録・封印の記録と二つの予想・正本。
  下見で止まったとき（または下見の器の誤りでやり直さなかったとき）は、集計の出力なしに凍結の記録の下見の記録だけで組む。
出力: records/Bl3/results-Bl3.md・results-Bl3-machine.json・results-Bl3-lint.md（--force が無ければ上書きしない）。
用法: python tools/build_report_Bl3.py [--force] [--rejected <起草者の行の md>] [--marks <印の JSON>] [--main-tool-error] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import report_lint as RL

VERSION = 'v1'
NL = chr(10)
OUT = os.path.join(REPO, 'records', 'Bl3', 'results-Bl3.md')
FENCE = '本報告のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
SECTIONS = ('summary', 'pilot', 'main', 'gate', 'descriptive', 'recompute', 'predictions', 'limits')
REJECTED_BLANK = '〔この結果が退けた説明: 結果を登録者と一緒に開いた後に起草者が書く（読みの表の型と書かないことの一覧に従う・数は打たない）〕'
f4 = lambda x: 'なし' if x is None else ('%.4g' % x)
br = lambda s: str(s).replace('〔', '［').replace('〕', '］')     # 段階 B の行の名の〔〕は、走査が記入欄と読むので印字では［］に写す
yn = lambda b: 'はい' if b else 'いいえ'
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
P = lambda r: os.path.join(REPO, *r.split('/'))


def machine(lines, MB):
    return [MB['begin']] + list(lines) + [MB['end']]


def side_words(T3):
    """効き目の側の言い方（正本 `labels.side_rule` の〔〕の三つを器が切り出す）。"""
    q = re.findall(r'〔([^〕]*)〕', T3['labels']['side_rule'])
    assert len(q) == 3, q
    return {'stronger': q[0], 'weaker': q[1], 'opposite': q[2]}


def side_text(T3, s):
    if not s:
        return 'なし（等方の外でない）'
    if s['side'] == 'sign_only':
        return '符号だけ（零が等方の帰無の四分位の間）: %s' % ('正' if s['sign'] > 0 else ('負' if s['sign'] < 0 else '零'))
    return side_words(T3)[s['side']]


def stop_sentence(T3, reason):
    """「下見で止めた」の二つの文（正本の読みの表の「」の二つ・一つ目は (i)(ii)・二つ目は (vi) の (b)）を、止まった理由で選ぶ。"""
    w = [r for r in T3['reading_rules'] if r['type'] == '下見で止めた'][0]['write']
    q = re.findall(r'「([^」]*)」', w)
    assert len(q) == 2, q
    return q[1] if reason == 'vi_b' else q[0]


def reading_types(T3, A):
    """読みの表の条件を当てる（型は重なりうる）。戻り値: [(型, 当たった所, 書くこと)]。"""
    RR = {r['type']: r for r in T3['reading_rules']}
    last = A['pilot_attempts'][-1]
    dec = last.get('decision') or {}
    hits = []
    if A['predictions_meta']['stopped']:
        if last.get('tool_error'):
            return [('器の誤り', '下見', '器の誤りで下見を終えられなかった（正本 pilot.decision.tool_error）')]
        return [('下見で止めた', '下見の決め', RR['下見で止めた']['write'] + '（この下見で当たる文:「%s」）' % stop_sentence(T3, dec.get('reason')))]
    if dec.get('dropped'):
        hits.append(('下見で一部を外した', '・'.join(dec['dropped']), RR['下見で一部を外した']['write']))
    if last.get('iv'):
        hits.append(('揺れの版の値', '下見の (iv)', RR['揺れの版の値']['write']))
    rows = A['rows']
    if not any(o['iso_outside'] for o in rows.values()):
        hits.append(('区別できない', '主の行', RR['区別できない']['write']))
    for rid, o in rows.items():
        if o['iso_outside']:
            t = '両方の外' if o['second']['top'] else '埋もれる'
            hits.append((t, rid, RR[t]['write'] + '（等方の帰無の中央値と効き目の側は主の表）'))
        else:
            hits.append(('外でない行', rid, RR['外でない行']['write']))
            if o['second']['top']:
                hits.append(('二つ目の札だけ', rid, RR['二つ目の札だけ']['write']))
    G = A['gates']['main']
    if not G.get('undetermined'):
        t = '門を通った' if G['pass'] else '門を通らない'
        hits.append((t, '本の門', RR[t]['write']))
    return hits


def pilot_lines(T3, rec, MB, title):
    """下見の記録（正本 `pilot.decision.report` に並べるもの）。"""
    P_ = T3['pilot']
    L = ['', '**%s**' % title, '']
    if rec.get('tool_error'):
        return L + machine(['- 器の誤り: %s' % rec['tool_error']], MB)
    rows = ['- 出口の値の自己検査（下見の頭）: 差の最大 %s（許容 %s）・%s' % (f4(rec['logit_check']['max_abs']), f4(rec['logit_check']['tol']), '通った' if rec['logit_check']['pass'] else '落ちた')]
    vi = rec['vi']
    rows.append('- (vi) (a) バッチの違いの揺れ（升目の間の最大）%s・(b) バッチ一の繰り返しの揺れ（升目の間の最大）%s・上限 %s' % (
        f4(vi['decision']['spread_a']), f4(vi['decision']['spread_b']), f4(P_['noise_max'])))
    rows += ['  - %s: (a) %s・(b) %s' % (k, f4(vi['a'][k]), f4(vi['b'][k])) for k in vi['a']]
    dec = rec.get('decision') or {}
    if dec.get('stop') and dec.get('reason') == 'vi_b':
        rows.append('- (vi) の (b) で止めたので、(i)〜(v) は計算していない（正本 pilot.order）')
        return L + machine(rows, MB)
    rows.append('- バッチの大きさ %s・揺れの床 %s・近道の許容 %s' % (rec.get('batch'), f4(rec.get('floor')), f4(rec.get('cache_tol'))))
    rows += ['', '| 升目 | 主の升目 | 無操作の対数オッズ | 選択肢 a の確率（集合の中） | 変換の後の確率 | 質量 | 段階 B の無操作の破局の率 | (i)(ii) |', '|---|---|---|---|---|---|---|---|']
    for k, c in rec['cells'].items():
        why = [] if c['pass_i_ii'] else [w for w, bad in (('質量が下限の下', c['mass'] < P_['mass_min']), ('確率が床か天井の外', not (P_['p_bounds'][0] <= c['pa'] <= P_['p_bounds'][1]))) if bad]
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (k, yn(c['main']), f4(c['lo']), f4(c['pa']), f4(c.get('pa_transformed')), f4(c['mass']), f4(c.get('stage_b_rate')),
                                                              '満たす' if c['pass_i_ii'] else '満たさない（%s）' % '・'.join(why)))
    rows += ['', '- (iii) 較正（記述）: 順位相関 %s・升目 %s・文: %s' % (f4(rec['iii']['rho']), rec['iii']['n'], T3['pilot']['iii_sentences'][rec['iii']['sentence']])]
    for name, v in (rec.get('iv') or {}).items():
        rows.append('- (iv) 揺れの版 %s: %s' % (name, '・'.join('%s %s（主との差 %s%s）' % (c, f4(x), f4(x - rec['cells'][c]['lo']), '・印' if v['flags'][c] else '') for c, x in v['lo'].items())))
    rows.append('- (v) 近道の確かめ（無操作の対数オッズの差）: %s・許容 %s・近道を使う: %s' % ('・'.join('%s %s' % (c, f4(d)) for c, d in rec['v']['diffs'].items()), f4(rec['v']['tol']), yn(rec['v']['shortcut'])))
    rows.append('- 機械の決定: %s・(i)(ii) を満たす主の升目 %s／%s・外した升目: %s' % (dec.get('q1'), dec.get('n_pass'), dec.get('n_main'), '・'.join(dec.get('dropped') or []) or 'なし'))
    fam = [k for k in (dec.get('dropped') or []) if k.startswith('N1|')]
    if len(fam) >= 2:
        rows.append('- nuclear の族は測れなかった（正本 pilot.decision.family）')
    return L + machine(rows, MB)


def outcomes(A):
    return dict(A['predictions_truth'])


def build(T3, A, preds, meta, deviations=(), marks=None, rejected=None, confirmation=None, main_tool_error=False):
    MB = RL.machine_block(T3)
    marks = marks or {}
    mk = lambda s: machine(['- 逸脱の印: %s' % '・'.join(marks[s])], MB) if marks.get(s) else []
    L = ['# B-lens 層三の結果（報告の草案・機械の組み立て）', '']
    if confirmation:
        st = '- 状態: **最終版**（登録者最終確認 %s 日本時間・会話の記録 uuid `%s`・逐語「%s」）。' % (confirmation['when_jst'], confirmation['uuid'], confirmation['words'])
    else:
        st = '- 状態: **報告の草案（結果の巡の前）**。'
    L += machine([st, '- 起草: 南無弥勒如来（コーディネータ）／登録者: 楠見優太。組み立ての器: `tools/build_report_Bl3.py` %s。' % VERSION,
                  '- 正本 `design/contrasts-Bl3.json` SHA16 %s・凍結の記録 SHA16 %s・封印の記録 SHA16 %s・集計の出力 SHA16 %s。' % (meta['canon'], meta['freeze'], meta['seal'], meta['analysis'])], MB)
    L += ['', '- 位置づけ: 段階 B と B-lens の後の登録（B-lens 層三）。段階 B と B-lens の札・報告・逸脱台帳には触れない。', '- 封印の前の露出の記録: `records/Bl3/exposure-before-seal-Bl3.md`。', '']
    L += ['## 凍結の後の逸脱', ''] + machine(['- 【逸脱 %s】%s（%s）' % (d.get('no'), d.get('what'), d.get('date')) for d in deviations] or ['- 無し'], MB)
    atts = A['pilot_attempts']
    if len(atts) > 1:
        L += ['', '## 一度目の下見の記録（やり直した下見の前・裁定 D222）']
        for i, rec in enumerate(atts[:-1], start=1):
            L += pilot_lines(T3, rec, MB, '試み %d の下見の記録と機械の決定' % i)
    stopped = A['predictions_meta']['stopped']
    # 0. 要約
    L += ['', '## 0. 要約（できないことから）', ''] + mk('summary')
    L += ['**見ていない場所**（正本の「この登録で答えられないこと」）:', ''] + machine(['- ' + x for x in T3['scope']['not_answered']], MB)
    L += ['', '**この結果が退けた説明**:', '', '- ' + (rejected.strip() if rejected else REJECTED_BLANK)]
    L += ['', '**答えの範囲**:', ''] + machine(['- ' + T3['scope']['reach'], '- ' + T3['negation_templates'][2]], MB)
    last = atts[-1]
    dec = last.get('decision') or {}
    L += ['', '**下見の機械の決定**:', ''] + machine(['- %s' % ('器の誤りで下見を終えられなかった' if last.get('tool_error') else '%s（外した升目: %s）' % (dec.get('q1'), '・'.join(dec.get('dropped') or []) or 'なし'))]
                                                    + ([] if last.get('tool_error') or (dec.get('stop') and dec.get('reason') == 'vi_b') else
                                                       ['- (iii) の文: ' + T3['pilot']['iii_sentences'][last['iii']['sentence']]]), MB)
    if main_tool_error:
        L += ['', '**本の計算**:', ''] + machine(['- 器の誤りで計算を終えられなかった（正本 computation.tool_error・予想は q1 だけを採点する）'], MB)
    if not stopped and not main_tool_error:
        rows = A['rows']
        cnt = lambda d: sum(1 for o in rows.values() if o['direction'] == d and o['iso_outside'])
        G = A['gates']
        gtxt = lambda g: '判定不能' if g.get('undetermined') else ('通った' if g['pass'] else '通らない')
        rc = A.get('recompute') or {}
        L += ['', '**主の記述の札と門**（機械の出力）:', ''] + machine([
            '- 主の行 %d（下見で外した後）・等方の外の行: v̂ %d・Nk %d・二つ目の札が付く行 %d' % (A['rows_meta']['m_rows'], cnt('static'), cnt('Nk'), sum(1 for o in rows.values() if o['second']['top'])),
            '- 本の門: %s・v̂ を抜いた門: %s' % (gtxt(G['main']), gtxt(G['without_vhat'])),
            '- 独立の再計算: 一段目 %s・二段目 %s' % (('一致' if (rc.get('first') or {}).get('agree') else '不一致') if rc.get('first') else '無い', '一致' if (rc.get('second') or {}).get('agree') else '不一致')], MB)
    L += ['', '**読みの型**（正本の読みの表の条件を器が当てた・型は重なりうる）:', ''] + machine(['- 〈%s〉（%s）: %s' % h for h in reading_types(T3, A)] if not main_tool_error else ['- 〈器の誤り〉（本の計算）: 器の誤りで計算を終えられなかった'], MB)
    L += ['', '**打ち消しの定型**:', ''] + machine(['- ' + x for x in T3['negation_templates']], MB)
    # 1. 下見の記録
    L += ['', '## 1. 下見の記録（本の凍結で凍結した・無操作だけ）'] + mk('pilot')
    L += pilot_lines(T3, last, MB, '下見の記録と機械の決定（主の札の隣に並べる）')
    if not stopped and not main_tool_error:
        L += main_sections(T3, A, MB, mk)
    # 6. 予想の照合
    L += ['', '## 6. 予想の照合（記録であり評価ではない）', ''] + mk('predictions')
    L += ['- 的中は誰の判断の重みも変えない。照合は記録であり評価ではない。', '']
    oc = outcomes(A)
    items = [it['key'] for it in T3['predictions']['items']]
    rows = ['| 項目 | 結果 | 登録者 | コーディネータ |', '|---|---|---|---|']
    for k in items:
        res = oc.get(k)
        cell = lambda who: '%s（%s）' % (preds[who].get(k, '—'), '予想しない' if preds[who].get(k) == '予想しない' else ('採点しない' if res is None else ('一致' if preds[who].get(k) == res else '不一致')))
        rows.append('| %s | %s | %s | %s |' % (k, '採点しない' if res is None else res, cell('registrant'), cell('coordinator')))
    notes = []
    if stopped:
        notes.append('- ' + T3['predictions']['if_stopped'])
    if main_tool_error:
        notes.append('- 器の誤りで計算を終えられなかったので、q1 だけを採点する（正本 computation.tool_error）')
    L += machine(rows + notes, MB)
    # 7. 限界
    L += ['', '## 7. 限界（正本の限界の文）', ''] + mk('limits') + machine(['- ' + x for x in T3['limits']], MB)
    L += ['', '## 検分票', '', '- 対象: 本報告の草案（機械の組み立ての出力と、起草者の欄）。', '- 段階: 結果の後（封印の後・凍結した器で計算した）。',
          '- 本検分が確認していないこと: 読みの型の当否と起草者の欄の文は、結果の巡で見る。', '', FENCE, '']
    return NL.join(L)


def main_sections(T3, A, MB, mk):
    L = []
    rows = A['rows']
    notes = A.get('stage_b_notes') or {'main': {}, 'gate': {}}
    # 2. 主の札
    L += ['', '## 2. 主の札（等方の帰無・実在の差の方向）', ''] + mk('main')
    t = ['| 行 | 方向 | 升目と符号 | 効き目 | p | 上の裾 | 下の裾 | 割合を決めた裾 | Holm の段 | 等方の外 | 等方の中央値 | 効き目の側 | 二つ目の札（中心・最上位・順位 向き／対） | 等方の最上位の割合 | 段階 B の札と注 |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for rid, o in rows.items():
        s = o['second']
        nb = notes['main'].get(rid) or {}
        nb_txt = '・'.join([x for x in [nb.get('label')] if x] + list(nb.get('notes') or []) + (['様式の保留'] if nb.get('style_hold') else [])) or 'なし'
        t.append('| %s | %s | %s | %s | %s | %d | %d | %s | %s | %s | %s | %s | %s・%s・%d／%d・%d／%d | %s | %s |' % (
            rid, o['direction'], o['cell_sign'], f4(o['effect']), f4(o['p']), o['upper'], o['lower'], {'upper': '上', 'lower': '下'}.get(o['tail'], o['tail']), f4(o['holm_step']),
            yn(o['iso_outside']), f4(o['iso_median']), side_text(T3, o['side']), f4(s['center']), yn(s['top']), s['rank_oriented'], s['of_oriented'], s['rank_pair'], s['of_pair'],
            f4(o['iso_top_share']), nb_txt.replace('|', '｜')))
    meta = A['rows_meta']
    t += ['', '- Holm の段の数（下見で外した後の主の行の数）%d・外した行: %s' % (meta['m_rows'], '・'.join(meta['dropped_rows']) or 'なし'),
          '- 二つ目の札の偶然の目安（Holm を掛けない）: 向きまで数えて %s・対の単位で %s。%s' % (f4(A['chance']['oriented']), f4(A['chance']['pair']), T3['nulls']['real']['chance_note']),
          '- 両方の札が付いたときの言い方（正本）: %s' % T3['labels']['print_rule']]
    L += machine(t, MB)
    D = A['descriptive']
    L += ['', '**升目と符号ごとの無操作の選択肢 a の文字の確率と質量**（主の札の隣に並べる）:', '']
    L += machine(['- 報告の雛形の決まり（裁定 D223）: 升目ごとの無操作の選択肢 a の文字の確率を、主の札の隣に並べる', '| 升目と符号 | 無操作の選択肢 a の確率（選択の文字と refuse の頭の中） | 質量が下限を下回った方向の数 |', '|---|---|---|'] +
                 ['| %s | %s | %d |' % (k, f4(D['pa_noop'][k]), D['mass_below_min'][k]) for k in D['pa_noop']] + ['- ' + T3['descriptive']['mass']], MB)
    # 3. 門
    G = A['gates']
    L += ['', '## 3. 門（段階 B の方向ごとの行動と、方向の単位で）', ''] + mk('gate')
    g = ['| 門 | 行 | 入れ替える単位 | 入れ替えの数 | 順位相関 | p | 通る |', '|---|---|---|---|---|---|---|']
    for name, lab in (('main', '本の門'), ('without_vhat', 'v̂ を抜いた門'), ('desc_without_vhat_loaded', '記述: v̂ と (6b) を抜いた門'), ('desc_choice_a', '記述: 選択 a の件数を行動の量にした門'),
                      ('desc_without_style', '記述: 様式の転位の行を除いた門')):
        x = G[name]
        if x.get('undetermined'):
            g.append('| %s | %d | %s | なし | なし | なし | 判定不能 |' % (lab, x['n_rows'], '・'.join(x['units'])))
        else:
            g.append('| %s | %d | %s | %d | %s | %s | %s |' % (lab, x['n_rows'], '・'.join(x['units']), x['n_perm'], f4(x['rho']), f4(x['p']), ('はい' if x['pass'] else 'いいえ') if not name.startswith('desc_') else '記述（型を当てない）'))
    g += ['- 門が通る条件: p が水準（%s）を下回るとき。%s' % (f4(T3['gate']['alpha']), T3['gate']['power_note']), '- ' + T3['gate']['descriptive_rule'],
          '- 様式の転位の行（除いた行）: %s' % ('・'.join(br(x) for x in (A.get('style_rows') or [])) or 'なし')]
    gn = [(n, v) for n, v in (notes.get('gate') or {}).items() if v]
    g += ['- 段階 B の注のある門の行: %s' % ('・'.join('%s［%s］' % (br(n), '・'.join('%s%s' % (x['kind'], ('（三本の率の差 %s pt・門 %s pt 超）' % (f4(x['spread_pt']), f4(x['threshold_pt']))) if 'spread_pt' in x else '') for x in v)) for n, v in gn) or 'なし')]
    L += machine(g, MB)
    # 4. 記述
    H = A['head']
    L += ['', '## 4. 記述（札を付けない）', ''] + mk('descriptive')
    d = ['- 本の計算の頭の自己検査: 出口の値 差の最大 %s（許容 %s）・最後の層 差 %s（許容 %s）' % (f4(H['logit_check']['max_abs']), f4(H['logit_check']['tol']), f4(H['layer_check']['diff']), f4(H['layer_check']['tol']))]
    sc = H.get('steered_cache_check')
    d.append('- 本の計算の頭の近道の確かめ: %s・本の計算の近道: %s・バッチの大きさ %s' % (
        ('二つの道の効き目の差の最大 %s（許容 %s）' % (f4(sc['max_abs']), f4(sc['tol']))) if sc else '走らせていない（下見で近道を使わないと決めた）', yn(A['main_run']['shortcut']), A['main_run']['batch']))
    d += ['- 層ごとの差分: 値は集計の出力の `layerwise` に置いた（名前のある方向と段階 B の三本の行・等方は層ごとの中央値と中央の区間）。' + T3['descriptive']['layerwise']['note_no_reading'],
          '- ' + T3['descriptive']['others']]
    L += machine(d, MB)
    S2 = A.get('secondary')
    if S2:
        s = ['', '**乙**（B-lens の層二の文脈・門の行の符号・裁定 D227）: 順伝播 %s・文脈 %s（流した文脈 %s）' % (S2['counts']['row_passes'], S2['counts']['contexts'], S2['contexts_run']), '',
             '| 行 | 文脈の数 | 対数オッズの変化 中央値［四分位］ | a の出口の値の変化 中央値 | c の出口の値の変化 中央値 | B-lens の直接の経路 a（中央値） | B-lens の直接の経路 c（中央値） |', '|---|---|---|---|---|---|---|']
        for name, v in S2['summary'].items():
            bl = v.get('blens_direct') or {}
            s.append('| %s | %d | %s［%s, %s］ | %s | %s | %s | %s |' % (br(name).replace('|', '｜'), v['dlo']['n'], f4(v['dlo']['median']), f4(v['dlo']['q1']), f4(v['dlo']['q3']), f4(v['dz_a']['median']),
                                                              f4(v['dz_c']['median']), f4((bl.get('dlogit_exact_a') or {}).get('median')), f4((bl.get('dlogit_exact_c') or {}).get('median'))))
        s += ['- ' + T3['readout']['secondary']['note'], '- ' + T3['descriptive']['secondary_readout']]
        L += machine(s[1:], MB)
    # 5. 独立の再計算
    rc = A.get('recompute') or {}
    L += ['', '## 5. 独立の再計算（二段）', ''] + mk('recompute')
    r = []
    for st, lab in (('first', '一段目（本の器のフック と 残差の書き換え）'), ('second', '二段目（本の道 と 本の器のフック）')):
        x = rc.get(st)
        tol = rc.get('tol_first') if st == 'first' else rc.get('tol_second')
        r.append('- %s: %s' % (lab, ('%s・効き目の差の最大 %s（許容 %s）・値の許容 %s・札 %s' % ('一致' if x['agree'] else '不一致', f4(x['max_abs_diff']), f4(tol), yn(x['values_within_tol']), '同じ' if x['labels_same'] else '違う')) if x else '無い'))
    r.append('- 組の間の環境: %s' % ('同じ' if (A.get('env') or {}).get('same') else '違う（%s）' % json.dumps((A.get('env') or {}).get('diff'), ensure_ascii=False)))
    L += machine(r, MB)
    return L


def lint_report(text, T3):
    T_scan = json.loads(json.dumps(T3))
    ban = list(T_scan['print_strings']['mechanism_word_ban'])
    for w in list(T3['print_strings']['added_ban']) + list(T3['print_strings']['reading_never_ban']):
        if w not in ban:
            ban.append(w)
    T_scan['print_strings']['mechanism_word_ban'] = ban
    side = {'blocks': RL.block_hashes(text, T3)}
    return RL.lint(text, T_scan, frozenset(), sidecar=side), side


def load_inputs(main_tool_error=False):
    import sweep_Bl3 as SW
    T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
    FR = json.load(open(P('records/Bl3/FREEZE-RECORD-Bl3.json'), encoding='utf-8'))
    seal = json.load(open(P('records/Bl3/sealing-record-Bl3.json'), encoding='utf-8'))
    preds = {r: json.load(open(P(v['path']), encoding='utf-8')) for r, v in seal['predictions'].items()}
    ap_ = P('records/Bl3/analysis-Bl3.json')
    atts = FR['main_freeze']['pilot_attempts']
    if os.path.exists(ap_):
        A = json.load(open(ap_, encoding='utf-8'))
        miss = SW.sweep(T3, A)
        if miss:
            raise SystemExit('掃き出し: 集計の出力に、正本と凍結の本文が求める出力の欠けがある（止める）: %s' % miss)
    else:
        last = atts[-1]
        if not (last.get('tool_error') or (last.get('decision') or {}).get('stop') or main_tool_error):
            raise SystemExit('集計の出力が無い（下見で止まったときと器の誤りのときだけ、集計の出力なしに組む）')
        import analyze_Bl3 as AZ
        truth, tmeta = AZ.prediction_truth(T3, atts, {}, {'main': {'undetermined': True}, 'without_vhat': {'undetermined': True}}, [], 0.0)
        if main_tool_error:
            truth = collections.OrderedDict((k, v if k == 'q1.pilot' else None) for k, v in truth.items())
        A = {'pilot_attempts': atts, 'predictions_truth': truth, 'predictions_meta': dict(tmeta, stopped=tmeta['stopped'] and not main_tool_error)}
    meta = {'canon': sha16f(P('design/contrasts-Bl3.json')), 'freeze': sha16f(P('records/Bl3/FREEZE-RECORD-Bl3.json')), 'seal': sha16f(P('records/Bl3/sealing-record-Bl3.json')),
            'analysis': sha16f(ap_) if os.path.exists(ap_) else 'なし'}
    fc = P('records/Bl3/final-confirmation-Bl3.json')
    confirmation = json.load(open(fc, encoding='utf-8')) if os.path.exists(fc) else None
    return T3, FR, A, preds, meta, confirmation


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--rejected', help='「この結果が退けた説明」の起草者の行（md・数を打たない）')
    ap.add_argument('--marks', help='逸脱の印の JSON（節の鍵 → 逸脱の番号の並び・節の鍵は %s）' % '・'.join(SECTIONS))
    ap.add_argument('--main-tool-error', action='store_true', help='本の計算が器の誤りで終えられず、やり直さないと登録者が裁定したとき')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if os.path.exists(OUT) and not a.force:
        raise SystemExit('既にある: %s' % OUT)
    T3, FR, A, preds, meta, confirmation = load_inputs(a.main_tool_error)
    marks = json.load(open(a.marks, encoding='utf-8')) if a.marks else None
    if marks and any(k not in SECTIONS for k in marks):
        raise SystemExit('印の節の鍵が違う: %s' % [k for k in marks if k not in SECTIONS])
    rejected = open(a.rejected, encoding='utf-8').read() if a.rejected else None
    text = build(T3, A, preds, meta, FR.get('deviations') or [], marks, rejected, confirmation, a.main_tool_error)
    V, side = lint_report(text, T3)
    open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
    RL.write_sidecar(OUT, text, T3, 'tools/build_report_Bl3.py %s' % VERSION)
    lint_path = OUT.replace('.md', '-lint.md')
    open(lint_path, 'w', encoding='utf-8', newline=NL).write(NL.join(['# 報告の走査（凍結した `tools/report_lint.py` の lint・禁止語は正本の四つの一覧の和）', '', '- 違反 %d' % len(V)] +
                                                                  ['- %s（%s 行目）: %s' % (v['kind'], v['line'], v['token']) for v in V] + ['', FENCE, '']))
    print('wrote %s（走査の違反 %d）' % (os.path.relpath(OUT, REPO), len(V)))
    if V:
        raise SystemExit('報告の走査に違反がある（非零で終わる）')


def synth_analysis(T3, FJ, DJ, seed=3, n_iso=199, stop=None, drop=()):
    """合成の集計の出力（模型を読まない・乱数の効き目・自己検査だけに使う）。"""
    import numpy as np
    import bl3_core as K
    import bl3_run as BR
    import analyze_Bl3 as AZ
    rng = np.random.default_rng(seed)
    T3x = AZ.with_iso(T3, n_iso)
    names = {'named': list(T3['directions']['named']), 'B_random': ['rand:%d' % i for i in range(T3['nulls']['B_random']['count'])], 'iso': ['iso:%d' % i for i in range(n_iso)],
             'real': ['real:' + p for p in DJ['groups']['real']['names']]}
    gate_only = [tuple(x) for x in FJ['facts']['C']['cell_signs_gate'] if x not in T3['cell_signs_main']]
    sets = BR.cell_sign_sets(T3, None, names['named'], names['B_random'], names['iso'], names['real'], gate_only)
    cells_out = collections.OrderedDict()
    for key, ck, sg, ds in sets:
        eff = {d: float(rng.normal(loc=0.3 * sg, scale=0.5)) for d in ds}
        eff['static'] = eff.get('static', 0.0) + 2.5 * sg if 'static' in eff else eff.get('static')
        eff = {k: v for k, v in eff.items() if v is not None}
        cells_out[key] = {'effects': eff, 'mass': {d: 0.95 for d in ds}, 'pa_noop': float(rng.uniform(0.01, 0.2)), 'lo': dict(eff, **{K.NOOP: -2.0})}
    cell_keys = ['%s|%s' % tuple(c) for c in T3['cells_main']]
    pilot = {'logit_check': {'max_abs': 0.05, 'tol': 0.5, 'pass': True},
             'vi': {'a': {k: 1e-3 for k in cell_keys}, 'b': {k: 0.0 for k in cell_keys}, 'decision': {'stop': stop == 'vi_b', 'batch': 16, 'floor': 1e-3, 'spread_a': 1e-3, 'spread_b': 0.02 if stop == 'vi_b' else 0.0}},
             'batch': 16, 'floor': 1e-3, 'cache_tol': 0.005,
             'cells': {k: {'lo': -2.0, 'pa': 0.1, 'mass': 0.95, 'pa_transformed': 0.05, 'stage_b_rate': 0.2, 'pass_i_ii': k not in drop, 'main': True} for k in cell_keys},
             'iii': {'rho': 0.3, 'n': len(cell_keys), 'sentence': 'positive'}, 'iv': {'V1': {'lo': {k: -1.9 for k in cell_keys}, 'flags': {k: False for k in cell_keys}}},
             'v': {'diffs': {k: 1e-4 for k in cell_keys}, 'tol': 0.005, 'shortcut': True},
             'decision': K.cells_decision({k: k not in drop for k in cell_keys}, {}, T3['pilot']['decision']['cells_min_pass'])}
    if stop == 'vi_b':
        pilot['decision'] = {'q1': '止める', 'reason': 'vi_b', 'stop': True}
        for k in ('iii', 'iv', 'v', 'cells'):
            pilot.pop(k)
    AN = json.load(open(P('records/B/analysis-B-2026-09-22.json'), encoding='utf-8'))
    rows_gate = AZ.stage_b_gate_rows(T3, AN, AZ.trials_reader())
    style_rows = [r['name'] for r in rows_gate if abs(r['style_pt']) >= T3['gate']['style_hold_pt']]
    if pilot['decision'].get('stop'):
        truth, tmeta = AZ.prediction_truth(T3, [pilot], {}, {'main': {'undetermined': True}, 'without_vhat': {'undetermined': True}}, [], 0.0)
        return {'pilot_attempts': [pilot], 'predictions_truth': truth, 'predictions_meta': tmeta}
    rows_rc, dbr = K.recompute_set(T3['main_rows'], DJ['groups']['real']['names'], T3['nulls']['real']['swap_siblings'], n_iso, pilot['decision']['dropped'])
    ek = lambda did, sg: did if did.startswith(('static', 'iso:', 'real:')) else did
    hook = {}
    for nm, ck, s in rows_rc:
        E = {}
        for did, sg in dbr[nm]:
            E['%s|%+d' % (did, sg)] = cells_out['%s|%+d' % (ck, sg)]['effects'][did]
        hook[nm] = {'noop_lo': -2.0, 'effects': E}
    A = AZ.analyze(T3x, FJ, cells_out, [pilot], DJ['groups']['real']['names'], rows_gate, hook=hook, rewrite=hook, style_rows=style_rows)
    A = json.loads(json.dumps(A, default=lambda o: o.item() if hasattr(o, 'item') else float(o)))
    main_keys = {'%s|%s|%+d' % (sc, b, int(sg)) for sc, b, sg in T3['cell_signs_main']}
    A.update({'dry': True, 'pilot_attempts': [pilot], 'head': {'logit_check': {'max_abs': 0.05, 'tol': 0.5, 'pass': True}, 'steered_cache_check': {'max_abs': 1e-4, 'tol': 0.005, 'shortcut': True},
                                                               'shortcut': True, 'layer_check': {'diff': 0.0, 'tol': 1e-4, 'pass': True}},
              'main_run': {'batch': 16, 'shortcut': True, 'dropped': pilot['decision']['dropped']},
              'layerwise': {k: {'noop_lo': {}, 'rows': {}, 'iso_summary': None} for k in cells_out if k in main_keys},
              'gate_rows': [], 'style_rows': style_rows, 'stage_b_notes': AZ.stage_b_notes(T3, AN, rows_gate),
              'secondary': {'counts': {'row_passes': 1, 'sign_batches': 1, 'contexts': 1}, 'contexts_run': 1,
                            'summary': {'S1|O-Ncold-v|static': dict({k: {'mean': 0.1, 'median': 0.1, 'q1': 0.0, 'q3': 0.2, 'n': 20} for k in ('dlo', 'dz_a', 'dz_c')},
                                                                     blens_direct={k: {'mean': x, 'median': x, 'q1': x, 'q3': x} for k, x in (('dlogit_exact_a', 0.1), ('dlogit_exact_c', -0.1))})}},     # B-lens の層二の値と同じ形（文脈の間の要約）
              'sessions': {}, 'env': {'same': True, 'diff': {}}})
    return A


def _selftest():
    """合成の集計の出力で報告を組み、走査が通ること（起草者の欄を埋めたとき）・欄が空なら埋め残しで止まること・禁止語と未登録の数を入れた報告が止まること・
    掃き出しが欠けを捕まえること・下見で止まったときと升目を外したときの組み立てを確かめる。"""
    import sweep_Bl3 as SW
    T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
    FJ = json.load(open(P('records/Bl3/design-facts-Bl3.json'), encoding='utf-8'))
    DJ = json.load(open(P('results/Bl3/directions-Bl3.json'), encoding='utf-8'))
    preds = {'registrant': {'q1.pilot': '続ける', 'q4.gate': '通らない'}, 'coordinator': {'q1.pilot': '止める', 'q2.vhat_iso': '零'}}
    meta = {k: '0123456789ABCDEF' for k in ('canon', 'freeze', 'seal', 'analysis')}
    A = synth_analysis(T3, FJ, DJ)
    miss = SW.sweep(T3, A)
    assert miss == [], miss
    A2 = json.loads(json.dumps(A))
    A2['rows'][next(iter(A2['rows']))].pop('iso_top_share')
    assert SW.sweep(T3, A2), '掃き出しが欠けを捕まえない'
    text = build(T3, A, preds, meta, [{'no': 'D-BL3-X', 'what': '合成の逸脱', 'date': '2026-09-26'}], {'main': ['D-BL3-X']}, '起草者の行（合成）')
    V, side = lint_report(text, T3)
    assert V == [], V[:5]
    t0 = build(T3, A, preds, meta)
    V0, _ = lint_report(t0, T3)
    assert any(v['kind'] == '埋め残し' for v in V0), V0[:3]
    for bad_line, kind in (('（効いた）', '価値語'), ('（v̂ に特有）', None), (' 12 件', '未登録の数')):
        bad = text.replace('## 7. 限界', '## 7. 限界' + bad_line, 1)
        Vb, _ = lint_report(bad, T3)
        assert Vb and (kind is None or any(v['kind'] == kind for v in Vb)), (bad_line, Vb[:3])
    As = synth_analysis(T3, FJ, DJ, stop='vi_b')
    ts = build(T3, As, preds, meta, rejected='起草者の行（合成）')
    Vs, _ = lint_report(ts, T3)
    assert Vs == [] and '数値が定まらず測れなかった' in ts and '## 2. 主の札' not in ts, Vs[:3]
    Ad = synth_analysis(T3, FJ, DJ, drop=('N1|O-Ncold',))
    td = build(T3, Ad, preds, meta, rejected='起草者の行（合成）')
    Vd, _ = lint_report(td, T3)
    assert Vd == [] and '〈下見で一部を外した〉' in td and Ad['rows_meta']['m_rows'] < len(T3['main_rows']), Vd[:3]
    print('[build_report_Bl3] 自己検査 OK（合成の報告の走査の違反 0・起草者の欄が空なら埋め残し・禁止語と未登録の数は止まる・掃き出しは欠けを捕まえる・止まった下見と外した升目の組み立て）')


if __name__ == '__main__':
    main()
