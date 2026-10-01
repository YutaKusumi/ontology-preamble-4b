# -*- coding: utf-8 -*-
"""sweep_Bprime.py v0.1 —— B′ の掃き出しの器（正本 `report_rules.builder`・草案10 §12 の「正本と凍結の本文が求める出力 ⊆ 器の出力の掃き出し（§0-37）」・層三の `sweep_Bl3.py` v4 の型・2026-09-30・コーディネータ南無弥勒如来）。

正本と凍結の本文が求める出力の一覧（下の鍵の表と、関数 sweep の need の行・出所の正本の鍵つき）を、集計の器の結果を開く段の出力
（`records/Bprime/analysis-Bprime.json`・`analyze_Bprime.open_checked`）と突き合わせ、欠けを返す。報告の組み立ての器 `build_report_Bprime.py` が報告を組む前に呼び、欠けがあれば止める。
下見で止まったとき・器の誤りで終わったときは、そのときに求めるものだけを見る。本器は値の当否を見ない（有るか無いかと、行と升目と符号と本数がそろうかだけ）。
出所の鍵は、自己検査で正本の中に在ることを確かめる（出所の書き間違いで確かめが空回りしないため）。
用法: python tools/sweep_Bprime.py <集計の出力の JSON> ／ --selftest（合成の出力は `analyze_Bprime` の結果を開く段の器で作る）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VERSION = 'v0.1'        # v0.1（2026-09-30・器の実装の検分の後）: 走行の表を求める（DRY でなければ表があり外れが零・T13・U04）・行動の下見が器の誤りで閉じた形を受ける（升目の集計の代わりに転記行 C の器の誤りの文と系統外の採点ができなかった理由・U07）・やり直しの前の閉じた記録の鍵を求める（U09）。前の版は `prev/sweep_Bprime-v0.py`
key3 = lambda sc, b, sg: '%s|%s|%+d' % (sc, b, int(sg))

# 下見の記録（`bprime_run.run_pilot`）: いつも在るもの・(vi) の (b) で止めたときは無いもの
PILOT_ALWAYS = [('logit_check', 'computation.self_checks.logit'), ('vi', 'pilot.checks.vi'), ('decision', 'pilot.decision')]
PILOT_AFTER_VI = [('batch', 'readout.primary'), ('floor', 'pilot.checks.vi'), ('cells', 'pilot.checks.i'), ('iv', 'pilot.checks.iv'), ('iii', 'pilot.checks.iii')]
# 主の行の札（`analyze_Bprime.row_labels`・`floor_marks`）
ROW_KEYS = [('direction', 'main_rows'), ('cell_sign', 'cell_signs_main'), ('effect', 'labels.print_rule'), ('p', 'labels.p_rule'), ('upper', 'labels.print_rule'),
            ('lower', 'labels.print_rule'), ('tail', 'labels.print_rule'), ('holm_step', 'labels.iso_outside'), ('iso_outside', 'labels.iso_outside'),
            ('iso_median', 'labels.print_rule'), ('side', 'labels.side_rule'), ('iso_top_share', 'labels.second.iso_top_share'), ('second', 'labels.second'),
            ('floor_mark', 'floor_margin.mark')]
SECOND_KEYS = [('center', 'labels.second.center_why'), ('top', 'labels.second.rule'), ('rank_oriented', 'labels.second.ranks'), ('of_oriented', 'labels.second.ranks'),
               ('rank_pair', 'labels.second.ranks'), ('of_pair', 'labels.second.ranks')]
SUMMARY_KEYS = ['n', 'k', 'k0', 'm', 'a1', 'a2', 'b1', 'b2', 'j', 'j0', 'n−k', 's1', 's2', 's3', 's4']
SPREAD_KEYS = ['iqr', 'central95', 'std', 'median', 'iqr_real', 'iqr_over_real']
RECOMPUTE_KEYS = ['agree', 'max_abs_diff', 'values_within_tol', 'labels_same']
REEXTRACT_KEYS = ['agree', 'keys_same', 'rel_h_max', 'rel_v', 'cos_min']
BEHAVIOR_CELL_KEYS = ['n', 'catastrophe', 'rate', 'wilson95', 'refuse', 'format_fail', 'truncated', 'rate_excl_truncated', 'unscorable', 'unscorable_by_reason', 'root_counts']
SOURCES = sorted({s for _, s in PILOT_ALWAYS + PILOT_AFTER_VI + ROW_KEYS + SECOND_KEYS} | {
    'predictions', 'pilot.decision_more', 'nulls.real', 'reading.summary', 'descriptive.mass', 'descriptive.ties', 'descriptive.spread', 'descriptive.layerwise',
    'descriptive.path_difference', 'computation.self_checks.layer', 'independent_recompute.stages', 'independent_recompute.reextract', 'nulls.isotropic',
    'behavior_pilot.closed_record_keys', 'behavior_pilot.rate', 'behavior_pilot.root_counts', 'behavior_pilot.external_scoring', 'behavior_pilot.scoring', 'computation.open_results',
    'computation.start_records', 'behavior_pilot.rerun', 'fixed_sentences.root_counts'})


def resolve(C, path):
    x = C
    for part in path.split('.'):
        if not isinstance(x, dict) or part not in x:
            return False
        x = x[part]
    return True


def sweep(C, A):
    """欠けの一覧（空なら欠け無し）。"""
    miss = []

    def need(cond, what, src):
        if not cond:
            miss.append('%s（%s）' % (what, src))
    atts = A.get('pilot_attempts') or []
    need(atts, '下見の試み', 'pilot.decision')
    dry_ = bool(A.get('dry'))
    RU = A.get('runs')
    need('runs' in A and (RU is None and dry_ or (RU is not None and bool(RU.get('table')) and not RU.get('bad'))),
         '走行の表（DRY でなければ表があり外れが零）', 'computation.start_records')                 # v0.1・U04・T13
    need(set(A.get('predictions_truth') or {}) == {it['key'] for it in C['predictions']['items']}, '予想の答えの項目', 'predictions')
    if not atts:
        return miss
    last = atts[-1]
    if last.get('tool_error'):
        return miss
    dec = last.get('decision') or {}
    vi_stop = bool(dec.get('stop')) and dec.get('reason') == 'vi_b'
    for k, src in PILOT_ALWAYS + ([] if vi_stop else PILOT_AFTER_VI):
        need(k in last, '下見の記録の %s' % k, src)
    if 'vi' in last:
        need('a' in last['vi'] and 'b' in last['vi'], '下見の (vi) の (a) と (b)', 'pilot.checks.vi')
    need(bool((last.get('logit_check') or {}).get('states')), '下見の頭の出口の値の自己検査の状態（升目ごと）', 'computation.self_checks.logit')
    if not vi_stop:
        cells = last.get('cells') or {}
        want_cells = ['%s|%s' % tuple(c) for c in C['cells_main']]
        need(sorted(cells) == sorted(want_cells), '下見の升目（主の八升目）', 'pilot.checks.i')
        need(all({'lo', 'pa', 'mass', 'pass_i_ii'} <= set(v) for v in cells.values()), '下見の升目ごとの対数オッズ・集合の中の確率・質量・(i)(ii) の合否', 'pilot.checks.i')
        need('sentence_key' in (last.get('iii') or {}) and 'n' in (last.get('iii') or {}) and 'dropped_n' in (last.get('iii') or {}), '(iii) の文の鍵と升目の数と除いた数', 'pilot.checks.iii')
    stopped = bool((A.get('predictions_meta') or {}).get('stopped'))
    if stopped:
        return miss
    # 主の札（下見で外した升目の行を除いたすべての主の行）
    dropped = set(dec.get('dropped') or [])
    want_rows = [r['id'] for r in C['main_rows'] if '%s|%s' % (r['scenario'], r['base']) not in dropped]
    rows = A.get('rows') or {}
    need(list(rows) == want_rows, '主の行（下見で外した後の全ての行・正本の順）', 'labels.iso_outside')
    for rid, o in rows.items():
        for k, src in ROW_KEYS:
            need(k in o, '行 %s の %s' % (rid, k), src)
        for k, src in SECOND_KEYS:
            need(k in (o.get('second') or {}), '行 %s の二つ目の札の %s' % (rid, k), src)
        need(o.get('side') is not None, '行 %s の効き目の側（どの行にも）' % rid, 'labels.side_rule')
        need('mark' in (o.get('floor_mark') or {}), '行 %s の床の余白の印' % rid, 'floor_margin.mark')
    RM = A.get('rows_meta') or {}
    need('m_rows' in RM and 'dropped_rows' in RM, 'Holm の段の数と外した行', 'pilot.decision_more')
    need({'vi_a_max', 'vi_b_max'} <= set(RM.get('floor') or {}), '床の余白の印の相手（(vi) の (a) の升目の間の最大と (b) の最大）', 'floor_margin.mark')
    need(set(A.get('chance') or {}) >= {'oriented', 'pair', 'rows_by_direction'}, '二つ目の札の偶然の目安と、外した後の方向ごとの行の数', 'nulls.real')
    SN = A.get('summary_numbers') or {}
    need(all(k in SN for k in SUMMARY_KEYS), '要約の型の数（〔〕の全て）', 'reading.summary')
    # 記述
    main_keys = [key3(sc, b, sg) for sc, b, sg in C['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
    D = A.get('descriptive') or {}
    need(set(main_keys) <= set(D.get('pa_noop') or {}), '升目と符号ごとの無操作の選択肢 a の確率', 'descriptive.spread')
    MB = D.get('mass_below_min') or {}
    need(set(main_keys) <= set(MB) and all({'named', 'iso', 'real'} <= set(MB.get(k) or {}) for k in main_keys), '質量が下限を下回った方向の数と割合（名前のある方向・等方・実在の差）', 'descriptive.mass')
    need(set(main_keys) <= set(D.get('iso_ties_share') or {}), '等方の効き目の中で同じ値が占める割合', 'descriptive.ties')
    SP = D.get('iso_spread') or {}
    need(set(main_keys) <= set(SP) and all(set(SPREAD_KEYS) <= set(SP.get(k) or {}) for k in main_keys), '升目と符号ごとの揺れの広さ（四分位の幅ほか）', 'descriptive.spread')
    LW = A.get('layerwise') or {}
    need(set(main_keys) <= set(LW), '層ごとの差分（主の組の升目と符号）', 'descriptive.layerwise')
    n_iso = C['nulls']['isotropic']['count']
    dry = bool(A.get('dry'))
    for k in main_keys:
        lw = LW.get(k) or {}
        need({'noop_lo', 'rows', 'iso_summary'} <= set(lw), '層ごとの差分の %s の無操作と行と等方の要約' % k, 'descriptive.layerwise')
        n_lay = len(lw.get('noop_lo') or {})
        need(n_lay > 0 and sorted(lw.get('rows') or {}) == sorted(C['directions']['named']) and all(len(v) == n_lay for v in (lw.get('rows') or {}).values()),
             '層ごとの差分の %s の名前のある方向の行が、層の数だけそろう' % k, 'descriptive.layerwise')
        iso_s = lw.get('iso_summary') or {}
        need(all(len(iso_s.get(x) or []) == n_lay for x in ('median', 'lo', 'hi')) and (dry or iso_s.get('n') == n_iso),
             '層ごとの差分の %s の等方の中央値と中央の区間が層の数でそろい、本数が正本の本数（DRY でなければ）' % k, 'descriptive.layerwise')
    H = A.get('head') or {}
    need('logit_check' in H and 'layer_check' in H, '本の計算の頭の自己検査（出口の値・最後の層）', 'computation.self_checks.layer')
    MR = A.get('main_run') or {}
    need('batch' in MR and 'dropped' in MR, '本の計算のバッチの大きさと外した升目', 'readout.primary')
    if MR.get('batch') == 1:
        PD = A.get('path_difference') or {}
        need('comparable' in PD and (not PD.get('comparable') or {'n_rows_label_differs', 'max_abs_diff', 'rows_label_differs'} <= set(PD)),
             '道の違いの記述（本の計算がバッチ一のとき）', 'descriptive.path_difference')
    # 独立の再計算と独立の再抽出
    rc = A.get('recompute') or {}
    need('first' in rc and rc.get('first') is not None and set(RECOMPUTE_KEYS) <= set(rc['first']), '独立の再計算の一段目', 'independent_recompute.stages')
    need(set(RECOMPUTE_KEYS) <= set(rc.get('second') or {}), '独立の再計算の二段目', 'independent_recompute.stages')
    need('tol_first' in rc and 'tol_second' in rc, '独立の再計算の許容', 'independent_recompute.stages')
    need(set(REEXTRACT_KEYS) <= set(A.get('reextract') or {}), '独立の再抽出の一致', 'independent_recompute.reextract')
    need('judge_record_sha16' in A and 'inputs' in A and (dry or (bool(A.get('judge_record_sha16')) and bool(A.get('inputs')))),
         '一致だけを見る段の記録の SHA16 と読んだ出力の同定（DRY でなければ中身がある）', 'computation.open_results')
    # 行動の下見（閉じた記録から）
    BH = A.get('behavior') or {}
    need('prior_closed' in BH, 'やり直しの前の閉じた記録の鍵（無ければ空の並び）', 'behavior_pilot.rerun')        # v0.1・U09
    if BH.get('tool_error'):                                              # 器の誤りで閉じた行動の下見（v0.1・U07）
        need(bool((BH.get('row_C') or {}).get('tool_error')), '転記行 C の器の誤りの文', 'behavior_pilot.closed_record_keys')
        EXT = BH.get('external') or {}
        need('fail' in EXT and bool(EXT.get('reason')), '系統外の模型による採点ができなかった理由', 'behavior_pilot.external_scoring')
        return miss
    SU = BH.get('summaries') or {}
    want_cells = ['%s|%s' % tuple(c) for c in C['cells_main']]
    need(sorted(SU) == sorted(want_cells), '行動の下見の升目ごとの集計（主の八升目）', 'behavior_pilot.rate')
    for ck in want_cells:
        need(set(BEHAVIOR_CELL_KEYS) <= set(SU.get(ck) or {}), '行動の下見の %s の率と件数と書き出しの根の件数' % ck, 'behavior_pilot.rate')
    need(BH.get('row_C') is not None, '転記行 C', 'behavior_pilot.closed_record_keys')
    EXT = BH.get('external') or {}
    need(('lineage' in EXT and {'agree', 'n'} <= set(EXT)) or 'fail' in EXT, '系統外の模型による採点の一致と系譜（できなかったときは理由）', 'behavior_pilot.external_scoring')
    return miss


def _selftest():
    import copy
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    bad_src = [s for s in SOURCES if not resolve(C, s)]
    assert not bad_src, ('出所の鍵が正本に無い', bad_src)
    sys.path.insert(0, HERE)
    import build_report_Bprime as BRP
    Cs, A0, preds, meta, closed, facts, bl3 = BRP._synthetic(C)
    base = sweep(Cs, A0)
    assert base == [], ('合成の出力（報告の組み立ての器の合成・欠けのない形）に欠けがある', base[:6])
    # 止まるべき形（一つずつ欠かせて、その欠けを捕まえる）
    rid0 = list(A0['rows'])[0]
    k0 = list(A0['layerwise'])[0]
    muts = [
        ('独立の再抽出の一致', lambda A: A.pop('reextract')),
        ('独立の再計算の一段目', lambda A: A['recompute'].update(first=None)),
        ('行の二つ目の札の順位', lambda A: A['rows'][rid0]['second'].pop('rank_pair')),
        ('行の床の余白の印', lambda A: A['rows'][rid0].pop('floor_mark')),
        ('層ごとの差分の行の数', lambda A: A['layerwise'][k0]['rows'].popitem()),
        ('要約の数', lambda A: A['summary_numbers'].pop('s4')),
        ('揺れの広さ', lambda A: A['descriptive']['iso_spread'].pop(list(A['descriptive']['iso_spread'])[0])),
        ('行動の下見の升目', lambda A: A['behavior']['summaries'].pop(list(A['behavior']['summaries'])[0])),
        ('系統外の模型による採点', lambda A: A['behavior'].update(external={})),
        ('主の行の欠け', lambda A: A['rows'].pop(rid0)),
        ('下見の記録の (iii)', lambda A: A['pilot_attempts'][-1].pop('iii')),
        ('一致だけを見る段の記録（DRY でないとき）', lambda A: A.update(dry=False, judge_record_sha16='')),
        ('走行の表（DRY でないとき）', lambda A: A.update(dry=False)),
        ('走行の表の外れ', lambda A: A.update(runs={'table': [{'phase': 'main'}], 'bad': ['合成']})),
        ('やり直しの前の閉じた記録の鍵', lambda A: A['behavior'].pop('prior_closed')),
        ('器の誤りで閉じた行動の下見の理由', lambda A: A['behavior'].update(tool_error=True, row_C={'tool_error': '文'}, external={'fail': '文'})),
    ]
    caught = []
    for name, f in muts:
        A = copy.deepcopy(A0)
        f(A)
        caught.append((name, bool(sweep(Cs, A))))
    # 下見で止まったとき・器の誤りのとき
    As = {'pilot_attempts': [dict(A0['pilot_attempts'][-1], decision={'q1': '止める', 'stop': True, 'reason': 'i_ii', 'dropped': []})],
          'predictions_truth': {it['key']: None for it in Cs['predictions']['items']}, 'predictions_meta': {'stopped': True}, 'dry': True, 'runs': None}
    caught.append(('下見で止まったときは下見の記録だけを見る', sweep(Cs, As) == []))
    Av = {'pilot_attempts': [{'logit_check': {'states': {'x': '合'}}, 'vi': {'a': {}, 'b': {}}, 'decision': {'q1': '止める', 'stop': True, 'reason': 'vi_b'}}],
          'predictions_truth': {it['key']: None for it in Cs['predictions']['items']}, 'predictions_meta': {'stopped': True}, 'dry': True, 'runs': None}
    caught.append(('(vi) の (b) で止まったときは (vi) までを見る', sweep(Cs, Av) == []))
    Ae = {'pilot_attempts': [{'tool_error': '合成'}], 'predictions_truth': {it['key']: None for it in Cs['predictions']['items']}, 'predictions_meta': {'stopped': True}, 'dry': True, 'runs': None}
    caught.append(('器の誤りのとき', sweep(Cs, Ae) == []))
    At = copy.deepcopy(A0)
    At['behavior'] = {'summaries': None, 'tool_error': True, 'row_C': {'tool_error': '文', 'external': {'fail': '文', 'reason': '理由'}}, 'external': {'fail': '文', 'reason': '理由'}, 'prior_closed': []}
    caught.append(('行動の下見が器の誤りで閉じたときは升目の集計を求めない', sweep(Cs, At) == []))
    bad = [n for n, v in caught if not v]
    assert not bad, bad
    print('sweep_Bprime.py %s SELFTEST PASS（出所の鍵 %d・欠けのない合成の出力で欠け零・止まるべき形 %d・止まったときと器の誤りで閉じたときの形 4）' % (VERSION, len(SOURCES), len(muts)))
    return base


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if len(sys.argv) == 2 and sys.argv[1] == '--selftest':
        _selftest(); sys.exit(0)
    if len(sys.argv) != 2:
        sys.exit('用法: python tools/sweep_Bprime.py <集計の出力の JSON> ／ --selftest')
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    m = sweep(C, json.load(open(sys.argv[1], encoding='utf-8')))
    print('[sweep_Bprime] 欠け %d%s' % (len(m), ''.join('\n  - ' + x for x in m)))
    sys.exit(1 if m else 0)
