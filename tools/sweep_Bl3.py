# -*- coding: utf-8 -*-
"""sweep_Bl3.py v2 —— B-lens 層三（Bl3）の掃き出しの器（正本 `report_rules.builder`・草案3 §12「掃き出しの器」・2026-09-25）。

正本と凍結の本文が求める出力の一覧（下の REQUIRED・出所の鍵つき）を、集計の器の結果を開く段の出力（`records/Bl3/analysis-Bl3.json`）と突き合わせ、欠けを返す。
組み立ての器 `tools/build_report_Bl3.py` が報告を組む前に呼び、欠けがあれば止める。下見で止まったときの出力（下見の記録と予想の答えだけ）は、止まったときに求めるものだけを見る。
本器は値の当否を見ない（有るか無いかと、行と升目と符号がそろうかだけ）。
用法: python tools/sweep_Bl3.py <集計の出力の JSON> ／ --selftest（合成の出力は `tools/build_report_Bl3.py --selftest` が作って呼ぶ）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
VERSION = 'v2'          # v2（2026-09-25・裁定 D231）: 効き目の側は全ての行で・偶然の目安の分母
key3 = lambda sc, b, sg: '%s|%s|%+d' % (sc, b, int(sg))

ROW_KEYS = [('effect', 'labels.print_rule（行の値）'), ('p', 'labels.p_rule'), ('upper', 'labels.print_rule（上の裾の本数）'), ('lower', 'labels.print_rule（下の裾の本数）'),
            ('tail', 'report_rules.template（割合を決めた裾）'), ('holm_step', 'labels.iso_outside.rule'), ('iso_outside', 'labels.iso_outside.rule'),
            ('iso_median', 'labels.print_rule（等方の帰無の中央値）'), ('side', 'labels.side_rule'), ('iso_top_share', 'labels.second.iso_top_share'), ('second', 'labels.second')]
SECOND_KEYS = [('center', 'labels.second.center_why'), ('top', 'labels.second.rule'), ('rank_oriented', 'labels.second.ranks'), ('of_oriented', 'labels.second.ranks'),
               ('rank_pair', 'labels.second.ranks'), ('of_pair', 'labels.second.ranks')]
PILOT_KEYS = [('logit_check', 'computation.self_checks.logit'), ('vi', 'pilot.checks.vi'), ('batch', 'pilot.decision.report'), ('floor', 'pilot.decision.report'),
              ('cache_tol', 'pilot.cache_tol_rule'), ('cells', 'pilot.checks.i・ii・iii'), ('iii', 'pilot.checks.iii'), ('iv', 'pilot.checks.iv'), ('v', 'pilot.checks.v'), ('decision', 'pilot.decision')]
GATES = [('main', 'gate.test'), ('without_vhat', 'gate.without_vhat'), ('desc_without_vhat_loaded', 'gate.descriptive_gates[0]'), ('desc_choice_a', 'gate.descriptive_gates[1]'),
         ('desc_without_style', 'gate.descriptive_gates[2]')]


def sweep(T3, A):
    """欠けの一覧（空なら欠け無し）。"""
    miss = []
    need = lambda cond, what: None if cond else miss.append(what)
    atts = A.get('pilot_attempts') or []
    need(atts, 'pilot_attempts（pilot.decision.report）')
    need(set(A.get('predictions_truth') or {}) == {it['key'] for it in T3['predictions']['items']}, 'predictions_truth の項目（predictions.items）')
    if not atts:
        return miss
    last = atts[-1]
    stopped = bool((A.get('predictions_meta') or {}).get('stopped'))
    if last.get('tool_error'):
        return miss
    dec = last.get('decision') or {}
    vi_stop = dec.get('stop') and dec.get('reason') == 'vi_b'
    for k, src in PILOT_KEYS:
        if vi_stop and k in ('cells', 'iii', 'iv', 'v'):
            continue
        need(k in last, '下見の記録の %s（%s）' % (k, src))
    if 'vi' in last:
        need('a' in last['vi'] and 'b' in last['vi'], '下見の (vi) の (a) と (b)（pilot.decision.report）')
    if stopped:
        return miss
    # 主の札（下見で外した升目の行を除いたすべての主の行）
    dropped = set(dec.get('dropped') or [])
    want_rows = [r['id'] for r in T3['main_rows'] if '%s|%s' % (r['scenario'], r['base']) not in dropped]
    rows = A.get('rows') or {}
    need(list(rows) == want_rows, '主の行（下見で外した後の全ての行・labels.iso_outside.rule）')
    for rid, o in rows.items():
        for k, src in ROW_KEYS:
            need(k in o, '行 %s の %s（%s）' % (rid, k, src))
        for k, src in SECOND_KEYS:
            need(k in (o.get('second') or {}), '行 %s の二つ目の札の %s（%s）' % (rid, k, src))
        need(o.get('side') is not None, '行 %s の効き目の側（labels.print_rule・どの行にも・裁定 D231）' % rid)
    need('m_rows' in (A.get('rows_meta') or {}) and 'dropped_rows' in (A.get('rows_meta') or {}), 'Holm の段の数と外した行（pilot.decision.drop_effects）')
    need(set((A.get('chance') or {})) >= {'oriented', 'pair', 'rows_by_direction'}, '二つ目の札の偶然の目安と、外した後の行の数（nulls.real.chance_note・pilot.decision.drop_effects）')
    # 門
    G = A.get('gates') or {}
    for k, src in GATES:
        g = G.get(k)
        need(g is not None, '門 %s（%s）' % (k, src))
        if g is not None:
            need('n_rows' in g and 'units' in g and (g.get('undetermined') or {'n_perm', 'rho', 'p', 'pass'} <= set(g)), '門 %s の行・単位・入れ替えの数・順位相関・p（gate.dropped）' % k)
    # 記述
    main_keys = [key3(sc, b, sg) for sc, b, sg in T3['cell_signs_main'] if '%s|%s' % (sc, b) not in dropped]
    D = A.get('descriptive') or {}
    need(set(main_keys) <= set(D.get('pa_noop') or {}), '升目と符号ごとの無操作の選択肢 a の確率（裁定 D223）')
    need(set(main_keys) <= set(D.get('mass_below_min') or {}), '質量が下限を下回った方向の数（descriptive.mass）')
    LW = A.get('layerwise') or {}
    need(set(main_keys) <= set(LW), '層ごとの差分（主の組の升目と符号・descriptive.layerwise.directions）')
    for k in main_keys:
        lw = LW.get(k) or {}
        need({'noop_lo', 'rows', 'iso_summary'} <= set(lw), '層ごとの差分の %s の行と等方の中央値と中央の区間（descriptive.layerwise）' % k)
    S2 = A.get('secondary') or {}
    need(S2.get('summary') and all('blens_direct' in v for v in S2['summary'].values()), '乙と B-lens の直接の経路の値（descriptive.secondary_readout）')
    H = A.get('head') or {}
    need('logit_check' in H and 'layer_check' in H, '本の計算の頭の自己検査（computation.self_checks）')
    need('shortcut' in H and 'shortcut' in (A.get('main_run') or {}), '本の計算の近道の使い方（computation.shortcut・裁定 D234）')
    # 独立の再計算
    rc = A.get('recompute') or {}
    for st in ('first', 'second'):
        x = rc.get(st)
        need(x is not None and {'agree', 'max_abs_diff', 'values_within_tol', 'labels_same'} <= set(x), '独立の再計算の %s（independent_recompute.stages）' % st)
    need('tol_first' in rc and 'tol_second' in rc, '独立の再計算の許容（independent_recompute.stages）')
    # 段階 B の注
    N = A.get('stage_b_notes') or {}
    need(set(want_rows) <= set(N.get('main') or {}), '主の行の段階 B の注（report_rules.template）')
    need('gate' in N, '門の行の段階 B の注（report_rules.template）')
    return miss


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] == '--selftest':
        sys.exit('用法: python tools/sweep_Bl3.py <集計の出力の JSON>（合成の確かめは tools/build_report_Bl3.py --selftest）')
    T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
    m = sweep(T3, json.load(open(sys.argv[1], encoding='utf-8')))
    print('[sweep_Bl3] 欠け %d%s' % (len(m), ''.join('\n  - ' + x for x in m)))
    sys.exit(1 if m else 0)
