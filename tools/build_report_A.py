# -*- coding: utf-8 -*-
"""build_report_A.py v2 —— 段階 A 結果報告の草案を、先置した雛形（records/A/results-report-template-A.md）の節順で機械組み立てする（2026-09-13・登録者裁定 D9 の三つ目の手順・採否表 P61〜P68）。
v2（2026-09-14・実装検分の採否表 P95〜P97・登録者裁定 D16・D19・D20・D22）: 雛形の行を消さず、機械の区画の後に雛形の行をそのまま残す。機械の区画の中身の SHA16 を別の記録（-machine.json）に書き、走査器がそれと突合する。打ち込んだ数の一覧の欄を冒頭に置く。記入欄の埋め残しのほかの違反があれば非零で終わる。対照腕の表に Wilson の区間、並記表に PPLRT の統計量。上向きの確証は report_rules.upward_rule（集計器の upward_confirmed）。判定器の妥当性は機械の判定で条件付けた誤判定率・除いた件数・全対の κ・鍵の照合。対照どうしの差と残存規模の非連続の注の枠。門2 の縮小の範囲。
方式: 雛形の見出し「## 0.」以降を一行ずつ写し、機械で埋められる行と表（RULES）を機械の区画（report_rules.machine_block）に置き換える。機械で埋められない記入欄（〔 〕）はそのまま残し、
  起草者が埋める（tools/report_lint.py が埋め残し・区画の外の未登録の数・価値語と機序語を止める）。節の順序・見出し・定型文は雛形のまま（出力の見出しの列を雛形と突合し、一致しなければ停止）。
  表と散文の数は機械の出力（analyze_A・identity_screen_A・gate_A・calib_band_A・integrity_A・judge_fragments_A・design_facts_A・power_grid_A・freeze_A）からの転記だけで、本器は判定をしない。
入力: --analysis（必須）・--identity・--gate・--calib・--integrity（複数）・--judge・--facts・--grid・--style・--design（凍結本文・§0 の逐語転記）・--freeze-verify（freeze_A --verify の出力の写し）・--predictions（予想の照合）。
出力: records/A/results-report-A-draft<k>-<日付>.md（既存は上書きしない）。組み立ての後に report_lint を走らせ、違反の件数を印字する（起草者が埋めるまで埋め残しが残るのは想定どおり）。
用法: python tools/build_report_A.py --draft 1 --analysis records/A/analysis-stageA.json --identity records/A/identity-screen-A.json --gate records/A/gate-pilotA.json --calib records/A/calib-stageA-calib.json
        --integrity records/A/integrity-*.json --facts records/A/design-facts-A.json --grid records/A/power-grid-A.json --style records/A/style-stageA.json --design design/design-stageA-FROZEN.md
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
import report_lint
REPO = runs_A.REPO
VERSION = 'v2.2'   # v2.2（2026-09-15・登録者裁定 D37・D39）: 判定器の欄に判定者の系統・κ の群・判定者の構成・取りまとめの記録・位置の記述の行
# v2.1（2026-09-14・採否表 P128・P133・登録者裁定 D27〜D31・D32・P141）: 到達の見込みの欠けで止まる・両向きの測れた効果種と測れた対比の本数・区間の被覆の断り・抽出検査の一致・断片の復唱の記述・検査用の口

ap = argparse.ArgumentParser()
ap.add_argument('--draft', type=int, required=True); ap.add_argument('--analysis', required=True); ap.add_argument('--identity'); ap.add_argument('--gate'); ap.add_argument('--calib'); ap.add_argument('--integrity', nargs='*', default=[])
ap.add_argument('--judge'); ap.add_argument('--facts'); ap.add_argument('--grid'); ap.add_argument('--style'); ap.add_argument('--design'); ap.add_argument('--freeze-verify'); ap.add_argument('--predictions')
ap.add_argument('--template', default=None); ap.add_argument('--contrasts', default=None); ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true')
ap.add_argument('--sampling', nargs='*', default=[]); ap.add_argument('--allow-dev-marks', action='store_true')
a = ap.parse_args()
T = runs_A.load_T(a.contrasts); MB = report_lint.machine_block(T); L = T['families']['A_slope']['confirm_rule']['labels']; PS = T['print_strings']; SIZES = T['sizes']
TP = a.template or os.path.join(REPO, T['report_rules']['template'])
RD = lambda p: runs_A.read_json(p) if p else None
AN = RD(a.analysis); ID = RD(a.identity); GT = RD(a.gate); CB = RD(a.calib); INTEG = [runs_A.read_json(p) for p in a.integrity]; JUD = RD(a.judge); FACTS = RD(a.facts); GRID = RD(a.grid)
STY = RD(a.style); FV = RD(a.freeze_verify); PRED = RD(a.predictions); SAMP = [runs_A.read_json(p) for p in a.sampling]
C = AN['label_counts']; OUTC = AN['contrasts']
f3 = lambda v: '—' if v is None else '%.3f' % v
sha = lambda p: runs_A.sha16_file(p) if (p and os.path.exists(p)) else '記録なし'


def mb(lines):
    return [MB['begin']] + list(lines) + [MB['end']]


def facts_text(k):
    return (FACTS or {}).get('facts', {}).get(k, {}).get('text')


# ---- 行の規則（雛形の行に含まれる文字列 → 置き換え）
def r_premise(line):
    return ['- 前提（機械の転記）:'] + mb(['凍結設計 %s（SHA16 %s）・正本（SHA16 %s）・門0.5 の記録（SHA16 %s）・門2 の記録（SHA16 %s）・校正帯の記録（SHA16 %s）・集計（SHA16 %s）・雛形（SHA16 %s）' % (
        a.design or '記録なし', sha(a.design), AN['inputs']['contrasts_sha16'], sha(a.identity), sha(a.gate), sha(a.calib), sha(a.analysis), sha(TP))])


def r_coi(line):
    if not a.design:
        return None
    lines = open(a.design, encoding='utf-8').read().split('\n'); i0 = next(i for i, l in enumerate(lines) if l.startswith('## 0.')); i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].startswith('## '))
    return ['1. 利益相反（第一条項・凍結 §0 の逐語転記）:'] + mb(lines[i0 + 1:i1])


def r_runfacts(line):
    if not INTEG:
        return None
    tot = sum(r['rows'] for I in INTEG for r in I['runs']); api = sum(r['api_error'] for I in INTEG for r in I['runs']); ff = sum(r['format_fail'] for I in INTEG for r in I['runs'])
    return ['3. 走行の事実の一行:'] + mb(['総試行 %d・api_error %d・書式外 %d・整合: %s' % (tot, api, ff, '／'.join('%s（%s）%s' % (I['tag'], I['phase'], I['verdict']) for I in INTEG))])


def r_identity0(line):
    if not ID:
        return None
    out = ['4. **門0.5 の分岐（先に置く）**:'] + mb(['%s（%d 個の絶対差の平均 %.3f pt・最大 %.3f pt）・補助検定の統合 p %.4f（合否を動かさない）' % ('合格' if ID['verdict'] == 'pass' else '不合格', len(ID['diffs']), ID['mean_abs_diff_pt'], ID['max_abs_diff_pt'], ID['aux']['p_combined']), '帰結: ' + ID['consequence']])
    return out + (['- 手元重みを別個体として扱い、既測点との並置と向きの比較を書かない（凍結 §2.9・§3 (iv)）。'] if ID['verdict'] == 'fail' else [])


def r_upward(line):
    ids = {u['id']: u for u in (AN.get('upward_confirmed') or [])}   # report_rules.upward_rule（登録者裁定 D20・analyze_A v2 の upward_confirmed）
    up = [x for x in OUTC if x['id'] in ids]
    return ['5. **上向きの確証（`report_rules.upward_rule`）**:'] + mb(['- %s: %s（最大の残存規模 %s）' % (x['id'], x['strings'].get('label', ''), ids[x['id']]['largest_residual_size']) for x in up] or ['上向きの確証はなかった。'])


def r_labels6(line):
    hold = C['refuse'] + C['style'] + C['env']
    return ['6. **札の内訳**（`print_strings.first_finding` の定型）:'] + mb([AN['first_finding'], '確証に残った対比は %d 本で、%d 本は判定不能、%d 本は解釈条項、%d 本は対数オッズ尺度でのみ、%d 本は判定保留に回った（§4 の並記表）。' % (C['confirmed'], C['undecidable'], C['clause'], C['scale_only'], hold)])


def r_reach7(line):
    if AN.get('reach_note') is None and 'no_facts' not in (AN.get('dev_marks') or []):
        sys.exit('[build_report_A] 集計に到達の見込みの記録が無い（設計事実の記録を渡して集計し直す・採否表 P128）')
    return ['7. **到達の見込みと測れた効果種**:'] + mb([AN.get('reach_note') or '（到達の見込みの記録なし）', AN['measurable']['string']] + list(AN['measurable'].get('coverage') or []))


def r_coverage(line):
    return ['- 測れた対比の本数（効果種ごと・両向き・機械の転記）:'] + mb(list(AN['measurable'].get('coverage') or ['記録なし']))


def t_summary(tbl):
    hold = '%d／%d／%d' % (C['refuse'], C['style'], C['env'])
    return mb(tbl[:2] + ['| 傾きの族 | %d | %d | %d | %d | %d | %d | %s | %d | analyze_A |' % (sum(C.values()), C['confirmed'] + C['ns'], C['confirmed'], C['clause'], C['scale_only'], C['undecidable'], hold, C['ns'])])


def r_summary_sentence(line):
    return ['要約文（`print_strings.first_finding` の定型のみ）:'] + mb([AN['first_finding']]) + ['続けて §0-6 と §0-7 の定型を置く（§0 の機械の区画）。']


def r_tools(line):
    I = AN['inputs']; rs = sorted({x for J in INTEG for r in J['runs'] for x in r['runner_sha']})
    return ['- 器材（機械の転記）:'] + mb(['走行器の SHA16 %s・confirm_A %s・firth %s・runs_A %s・analyze_A %s・凍結マニフェストの突合 %s' % ('・'.join(rs) or '記録なし', '／'.join(I['confirm_A']), '／'.join(I['firth']), I['runs_A'], I['analyze_A'],
                                                                                              ('%d/%d 一致' % (FV['matched'], FV['total'])) if FV else '記録なし')])


def r_env(line):
    se = AN['size_env']; rows = collections.OrderedDict()
    for k, v in se.items():
        s, sc = k.split('|'); rows.setdefault(s, set()).update(v)
    return ['- 環境（機械の転記・残りは起草者）:'] + mb(['規模ごとの環境値: %s・セッション記録が無く登録値で補った走行キー %d' % ('／'.join('%s %s' % (s, '・'.join(sorted(v))) for s, v in rows.items()), len(AN.get('env_fallback_run_keys') or []))] +
                                                        ['%s: GPU %s・vLLM %s' % (r['run_key'], r.get('local_env_gpu'), r.get('vllm')) for J in INTEG for r in J['runs'][:1]])


def r_integ(line):
    if not INTEG:
        return None
    return ['- 整合（機械の転記）:'] + mb(['%s（相 %s）: %s・走行 %d' % (J['tag'], J['phase'], J['verdict'], len(J['runs'])) for J in INTEG] +
                                      ['抽出検査の目視と機械分類の一致（%s・%s）: 照合 %d 件・一致 %d・一致率 %s' % (S_['tag'], S_['phase'], S_['n_compared'], S_['agree'], f3(S_['agree_rate'])) for S_ in SAMP] +
                                      ['ループ・切り詰めは §3 の測定不能の一覧（和集合）を参照。抽出検査の目視の記録は起草者が転記する。'])


def r_g05(line):
    if not ID:
        return None
    return ['- 門0.5（機械の転記）:'] + mb(['%s・平均 %.3f pt・最大 %.3f pt・補助の統合 p %.4f' % (ID['verdict'], ID['mean_abs_diff_pt'], ID['max_abs_diff_pt'], ID['aux']['p_combined'])] + ([facts_text('N')] if facts_text('N') else []))


def r_gate2(line):
    if not GT:
        return None
    g = GT['gate2']
    return ['- 門2（機械の転記）:'] + mb(['族の縮小 %s・残る場面 %s・縮小で判定不能にした対比 %d（残らない場面の対比だけ・登録者裁定 D16）' % ('あり' if g['shrink'] else 'なし', '・'.join(g['remaining_scenarios']) or 'なし', len(AN.get('gate2_shrink_ids') or []))] + ['%s: %s' % (sc, '・'.join('%s %d' % (x['id'].split(':', 1)[1], x['kept_n']) for x in v['contrasts'])) for sc, v in g['per_scenario'].items()])


def r_calib(line):
    out = []
    if CB:
        out += ['校正帯（%s）: セッション %d・器の異常 %d・やり直し待ち %d・逸脱 %d' % ('合格枝' if CB['branch'] == 'pass' else '不合格枝', len(CB['sessions']), len(CB['anomaly_sessions']), len(CB['retry_waiting']), len(CB['deviations']))]
        out += ['%s %s s%s: %d/%d・API 既測との差 %s pt・判定 %s' % (x['phase'] or '—', x['owner'] or '—', '—' if x['session'] is None else x['session'], x['k'], x['n'], '—' if x['api_diff_pt'] is None else '%+.2f' % x['api_diff_pt'], x.get('verdict')) for x in CB['sessions']]
        out += ['件数のそろわない校正腕 %d・セッション記録の無い校正腕 %d・seed が規則と合わない校正腕 %d' % (len(CB.get('incomplete') or []), len(CB.get('missing_session_records') or []), len(CB.get('seed_mismatch') or []))]
        out += ['逸脱（%s）: %s' % (d.get('kind', ''), d['run_key']) for d in (CB.get('deviations') or [])]
    if GT:
        w = GT['withdrawal']; out += ['撤退条件（%s）: %s・器の異常 %s' % ('合格枝' if w['branch'] == 'pass' else '不合格枝', w['status'], 'あり' if w['anomaly'] else 'なし')]
    return (['- 校正腕と撤退条件（機械の転記・管理図は records/control-chart.md）:'] + mb(out)) if out else None


def r_unmeas(line):
    return ['- 測定不能（機械の転記）:'] + mb(['%s × %s × %s: 和集合 %d/%d（書式外 %d・ループ %d・切り詰め %d・延べ %d）' % (x['model'], x['scenario'], x['arm'], x['union'], x['n_ok'], x['format_fail'], x['loop'], x['truncated'], x['total_count']) for x in AN['unmeasurable']] or ['なし'])


def r_anchor(line):
    return ['- 錨帯（機械の転記）:'] + mb(['除外単位 %s × %s（帯を超えた腕: %s）' % (x['model'], x['scenario'], '・'.join(x['arms'])) for x in AN['anchor_excluded_units']] or ['除外なし'])


def r_env3(line):
    out = ['環境保留の対比: %s' % ('・'.join('%s（%s）' % (x['id'], '・'.join(e['rule'] for e in x['env_reasons'])) for x in OUTC if x['env_hold']) or 'なし')]
    out += ['橋の帯を超えた腕: %s' % ('・'.join('%s（%s %+.1f pt）' % (arm, r['model'], r['diff_pt']) for arm, rs in AN['env_flag_arms'].items() for r in rs) or 'なし')]
    if GT:
        e = GT['env_band_recheck']; out += ['パイロットの率での選択規則の引き直し: 選ばれる候補 %s・登録の帯が規則を満たすか %s' % (e['selected_by_rule_at_pilot'], '満たす' if e['registered_meets_rule_at_pilot'] else '満たさない（登録者の裁定）')]
    out += ['環境ダミーの副次解析（記述）: %s' % ('／'.join('%s %s' % (x['id'], x['status']) for x in AN['descriptive']['A_desc_env']['secondary']) or 'なし')]
    return ['- 環境（機械の転記）:'] + mb(out)


def r_refuse(line):
    return ['- refuse 門（機械の転記）:'] + mb(['%s: 保留（%s）' % (x['id'], ''.join(x['refuse_gate']['reasons'])) for x in OUTC if x['refuse_gate'] and x['refuse_gate']['hold']] or ['保留なし'])


def r_style(line):
    out = ['%s: 様式門 %s' % (x['id'], x['style']) for x in OUTC if x['style'] in ('hold', 'note')] or ['保留・注なし']
    out += [s['string'] for s in AN['stratified'] if s.get('string')]
    if GT and GT.get('style_pilot'):
        out += ['パイロットで全規模に当てたときの見込み: 保留 %d 本・注 %d 本（記述）' % (len(GT['style_pilot']['hold_if_applied']), len(GT['style_pilot']['note_if_applied']))]
    return ['- 様式門（機械の転記）:'] + mb(out)


def r_demote(line):
    return mb(['- %s: %s' % (d['id'], d['string']) for d in AN['demotions']] or ['- 降格・保留なし'])


def judge_label(name):
    m = (JUD.get('judges_meta') or {}).get(name) or {}
    return '%s（%s）' % (name, m.get('lineage') or '系統の記録なし')


def t_judge(tbl):
    if not JUD:
        return mb(['（判定器の妥当性の採点の記録なし）'])
    rows = tbl[:2]   # 方向別の誤判定率は機械の判定で条件付ける（登録者裁定 D19）・判定者の欄に系統（登録者裁定 D37）
    for name, out in JUD['per_judge'].items():
        rows += ['| %s | %d | %d | %s | %s（%d） | %s（%d） | 機械 %d・%d／判定者 %d・%d・%d・%d | %s |' % (
            cell, v['n_fragments'], v['n_pairs'], f3(v['kappa']), f3(v['judge_non_given_machine_cat']), v['n_machine_cat'], f3(v['judge_cat_given_machine_non']), v['n_machine_non'],
            v['excluded_machine']['format_fail'], v['excluded_machine']['refuse'], v['excluded_judge']['undecidable'], v['excluded_judge']['refuse'], v['excluded_judge']['malformed'], v['excluded_judge']['unlabeled'], judge_label(name))
                 for cell, v in out.items()]
    return mb(rows)


def r_judge_inter(line):
    if not JUD:
        return None
    E_ = JUD.get('echo') or {}; G_ = JUD.get('groups') or {}; C_ = JUD.get('composition') or {}
    L_ = ['判定者の構成（登録と実際）: %s' % ('・'.join('%s（%s）登録 %d 名%s・実際 %d 名・%s' % (s, c['lineage'], c['registered_min'], '以上' if c['registered_max'] is None else '', c['actual'], '満たす' if c['meets'] else '満たさない')
                                              for s, c in C_.items()) or '記録なし')]
    if G_:   # κ の四つの群（登録者裁定 D37）
        L_.append('系統外×機械: %s の機種 × 場面の表（上）' % ('・'.join(G_.get('系統外×機械', {}).get('judges') or []) or 'なし'))
        for g in ('系統外どうし', '系統内どうし', '系統外×系統内'):
            L_.append('%s: %s' % (g, '・'.join('%s 対 %s（対 %d・κ %s）' % (d['judges'][0], d['judges'][1], d['n_pairs'], f3(d['kappa'])) for d in (G_.get(g) or {}).get('pairs') or []) or 'なし'))
    else:
        L_ += ['%s 対 %s: 対 %d・κ %s' % (d['judges'][0], d['judges'][1], d['n_pairs'], f3(d['kappa'])) for d in JUD['inter_judge']]
    L_.append('鍵の SHA-256 %s（封印の記録との一致を採点の器が確かめた）・取りまとめの記録 %s' % (JUD['key_sha256'], ('%s（SHA16 %s）' % (JUD['merge_record']['file'], JUD['merge_record']['sha16'])) if JUD.get('merge_record') else 'なし'))
    if E_:
        L_.append('断片の本文と自分の腕の前置きの最長共通部分（字数・記述・閾値なし）: %s・自分の腕の値がほかの腕の最大を超える断片 %d/%d' % (
            json.dumps(E_.get('own_arm_quantiles'), ensure_ascii=False), E_.get('own_exceeds_max_other', 0), E_.get('n_with_preamble', 0)))
    return ['- 判定者どうしの κ と判定者の構成と鍵の照合（機械の転記）:'] + mb(L_)


def r_judge_position(line):
    if not JUD or not JUD.get('position'):
        return None
    out = []   # ファイルの中の位置の記述（登録者裁定 D39・ファイルごとの値は採点の記録）
    for name, P in JUD['position'].items():
        if not P:
            out.append('%s: 位置の記述なし（区切りの記録なし）' % judge_label(name))
            continue
        out.append('%s・区切り %s: %s' % (judge_label(name), P['split'], '／'.join('%s 破局の一致 %s（対 %d）・選択の一致 %s（%d）・判定不能 %d・形の不備 %d・ラベルなし %d' % (
            b, f3(v['agree_catastrophe']), v['n_pairs'], f3(v['agree_choice']), v['n_choice_pairs'], v['undecidable'], v['malformed'], v['unlabeled']) for b, v in P['pooled'].items())))
    return ['- 位置の記述（ファイルを合わせた前・中・後・機械の転記）:'] + mb(out)


def t_ctrl(tbl):
    head = '| 場面 | 対照腕 | %s |' % ' | '.join(SIZES + ['4B-2507（別記号）'])
    wil = lambda w: '—' if (not w or w[0] is None) else '%.3f〜%.3f' % tuple(w)   # Wilson の区間（採否表 P97）
    return mb([head, '|---|---|%s' % ('---|' * (len(SIZES) + 1))] + ['| %s | %s | %s |' % (x['scenario'], x['arm'], ' | '.join('%d/%d（%s・Wilson %s）' % (x['sizes'][s]['k'], x['sizes'][s]['n'], f3(x['sizes'][s]['rate']), wil(x['sizes'][s].get('wilson'))) for s in SIZES + ['4B-2507'])) for x in AN['control_bases']])


def r_bigtable(line):
    rows = ['| 対比 | 残った規模 | β₃（推定・PPLRT 統計量・p_β・Holm 順位/水準） | pt 差の傾き（pt／z・p_pt） | p*（Holm 順位/水準・区間） | 解釈条項 | refuse 門 | 様式門 | 環境 | 札 | 段 | 当てはまった規則 | 行 id | 注 |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for x in OUTC:
        r = x['result']; ok = r['status'] == 'ok' and x['stage'] != 0   # 門2 の縮小で判定不能にした対比は統計量を印字しない（登録者裁定 D16）
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d | %s | %s | %s |' % (
            x['id'], x['strings']['residual_sizes'], ('%+.3f・%.2f・%.3g・%d/%.5f' % (r['beta'], r['stat'], r['p_beta'], x['beta_holm']['rank'], x['beta_holm']['level'])) if ok else r['status'],
            ('%+.2f・%.3g' % (x['slope_pt'], r['p_pt'])) if ok else '—', ('%.3g・%d/%.5f・%+.2f〜%+.2f' % (r['p_star'], x['star_holm']['rank'], x['star_holm']['level'], x['interval_pt'][0], x['interval_pt'][1])) if ok else '—',
            ('発火（A %d・B %d）' % (r['sat_A'], r['sat_B']) if r['clause'] else '—') if ok else '—', ('保留（%s）' % ''.join(x['refuse_gate']['reasons']) if x['refuse_gate']['hold'] else '保留なし') if x['refuse_gate'] else '—',
            x['style'], '保留' if x['env_hold'] else '—', x['label'], x['stage'], '・'.join(x['rules']), x['row'], '・'.join(x['notes']) or '—'))
    rows += ['', PS['interval_note']]   # 区間の被覆の断り（登録者裁定 D31）
    rows += ['', '破局/n（規模順 %s）:' % '・'.join(SIZES)] + ['- %s: A %s／B %s' % (x['id'], ' '.join('%d/%d' % (k, n) for k, n in zip(x['counts']['kA'], x['counts']['nA'])), ' '.join('%d/%d' % (k, n) for k, n in zip(x['counts']['kB'], x['counts']['nB']))) for x in OUTC]
    return mb(rows)


def r_label_strings(line):
    out = []
    for x in OUTC:
        s = x['strings']; parts = [s.get('label', '')] + s.get('env', []) + s.get('style', [])
        if any(parts):
            out.append('- %s: %s' % (x['id'], ' '.join(p for p in parts if p)))
    return ['- 対比ごとの定型文（機械の転記）:'] + mb(out or ['- なし'])


def t_reading(tbl):
    name_to_key = {v: k for k, v in L.items()}; rows = tbl[:2]
    for l in tbl[2:]:
        cells = l.strip('|').split('|'); lab = cells[0].strip(); k = name_to_key.get(lab)
        if k is not None and len(cells) >= 3:
            cells[1] = ' %d ' % C[k]
        rows.append('|' + '|'.join(cells) + '|')
    return mb(rows)


def t_sens(tbl):
    order = ['confirmed', 'undecidable', 'clause', 'scale_only', 'refuse', 'ns']
    fmt = lambda cn: [str(cn[k]) for k in order[:4]] + ['%d' % (cn['refuse'] + cn['style'] + cn['env']), str(cn['ns'])]
    rows = tbl[:2] + ['| %s／%s（主） | %s | — |' % (T['censor']['low'], T['censor']['high'], ' | '.join(fmt(C)))]
    rows += ['| %s／%s | %s | %s |' % (s['low'], s['high'], ' | '.join(fmt(s['counts'])), '・'.join(x['id'] for x in s['changed']) or 'なし') for s in AN['sensitivity']]
    return mb(rows)


def t_detect(tbl):
    if not GRID:
        return None
    rows = tbl[:2]
    for r in GRID.get('DR', []):
        rows.append('| %s | %.3f | %.3f | 既測 | %s | %s | %d | %.3f | %s |' % (r['id'], r['base_A'], r['base_B'], r['ctrl_trend'], r['delta'], r['clipped_sizes'], r['card_D1_holm_first'], f3(r['clause_rate_among_fit'])))
    for r in GRID.get('DO', []):
        rows.append('| %s | %.3f | %.3f | 仮定（d0 %+.2f） | %s | %s | %d | %.3f | %s |' % (r['id'], r['base_A'], r['base_B'], r['assumed_d0'], r['ctrl_trend'], r['delta'], r['clipped_sizes'], r['card_D1_holm_first'], f3(r['clause_rate_among_fit'])))
    return mb(rows)


def t_reach(tbl):
    frozen = collections.defaultdict(lambda: collections.defaultdict(lambda: 1.0)); frozen_o = collections.defaultdict(lambda: collections.defaultdict(lambda: 1.0))
    for r in (GRID or {}).get('DR', []):
        if r['delta_value'] != 0.0:
            frozen[r['effect']][r['ctrl_trend']] *= (1 - r['card_D1_holm_first'])
    for r in (GRID or {}).get('DR_opp', []):
        frozen_o[r['effect']][r['ctrl_trend']] *= (1 - r['card_D1_holm_first'])
    dtx = lambda d: '—' if d is None else '%.3f（%.3f〜%.3f）' % (d['at_least_one'], d['ci'][0], d['ci'][1])
    rows = tbl[:2]
    for e, v in AN['measurable']['types'].items():
        fz = '／'.join('%s %.3f・%.3f' % (tr, 1 - q, 1 - frozen_o[e][tr]) for tr, q in frozen[e].items()) if e in frozen else '既測基底なし'
        rows.append('| %s | %s | %s／%s | %d/%d | %s | %s |' % (e, fz, dtx(v['directions'].get('room')), dtx(v['directions'].get('opposite')), v['measured_contrasts'], v['n_contrasts'],
                                                              '・'.join(v['blind_ids']) or 'なし', '測れた' if v['measurable'] else '測れなかった（%s）' % '・'.join(v['reasons'])))
    return mb(rows)


def r_floor(line):
    return mb([x['string'] for x in AN['floor']] + (['到達可能性の三段（転記行 E）: ' + facts_text('E')] if facts_text('E') else []))


def t_critical(tbl):
    return mb(tbl[:2] + ['| %s | %s | %s |' % (x['id'], x['critical_size']['size'], '・'.join(x['critical_size']['sizes']) or 'なし') for x in OUTC])


def r_desc_pairs(line):
    out = ['| 対比 | %s |' % ' | '.join(SIZES), '|---|%s' % ('---|' * len(SIZES))]
    for fk in ('A_desc_nstr', 'A_desc_ncold'):
        out += ['| %s | %s |' % (x['id'], ' | '.join('測定不能' if y['unmeasurable'] else ('—' if y['diff_pt'] is None else '%+.1f' % y['diff_pt']) for y in x['sizes'])) for x in AN['descriptive'][fk]]
    return ['- Nstr−Onull・Ncold−N（規模ごとの差・pt・機械の転記）:'] + mb(out)


def r_style_desc(line):
    if not STY:
        return None
    out = ['| 機種 | 場面 | 腕 | (a) | (b) | 言及 c2 | <think> |', '|---|---|---|---|---|---|---|']
    for mk, scs in STY['cells'].items():
        for sc, arms in scs.items():
            for arm, v in arms.items():
                n = v['n_ok'] or 1
                out.append('| %s | %s | %s | %.3f | %.3f | %.3f | %d |' % (mk, sc, arm, v['a_final'] / n, v['b_final'] / n, v['c2_final'] / n, v['think_residue']))
    return ['- 応答様式 (a)(b)・検査認識の言及率（機械の転記・場面を跨いで比べない）:'] + mb(out)


def r_anchor_desc(line):
    return ['- 錨の走行間差（機械の転記）:'] + mb(['%s × %s × %s: %s pt%s' % (x['model'], x['scenario'], x['arm'], '—' if x['diff_pt'] is None else '%+.1f' % x['diff_pt'], '（帯を超える）' if x['over'] else '') for x in AN['descriptive']['A_desc_anchor_drift']] or ['記録なし'])


def r_recipe(line):
    return ['- レシピ対（機械の転記）:'] + mb(['%s: %s pt' % (x['id'], '—' if x['diff_pt'] is None else '%+.1f' % x['diff_pt']) for x in AN['descriptive']['A_desc_recipe']])


def r_stack(line):
    s = AN['descriptive']['A_desc_stack']
    return ['- スタック差（機械の転記）:'] + mb([s['status']] + ['%s × %s × %s: %s pt' % (x['model'], x['scenario'], x['arm'], '—' if x['diff_pt'] is None else '%+.1f' % x['diff_pt']) for x in s['rows']])


def r_envdesc(line):
    e = AN['descriptive']['A_desc_env']
    return ['- 環境差と環境ダミーの副次解析（機械の転記）:'] + mb(['%s × %s: %s pt（主 %s・橋 %s）' % (x['model'], x['arm'], '—' if x['diff_pt'] is None else '%+.1f' % x['diff_pt'], '・'.join(x['main_env']), '・'.join(x['bridge_env'])) for x in e['bridge']] +
                                                         ['%s: %s %s' % (x['id'], x['status'], json.dumps(x.get('estimates', {}), ensure_ascii=False)) for x in e['secondary']])


def r_residual(line):
    return ['- 残った規模の一覧（機械の転記）:'] + mb(['%s: %s' % (x['id'], x['strings']['residual_sizes']) for x in OUTC])


def r_residual_gap(line):
    out = ['%s: %s' % (x['id'], n) for x in OUTC for n in x['notes'] if '残存規模は連続でない' in n]
    return ['- 残存規模の非連続と端の欠けの注（機械の転記・読み条項 (xii)）:'] + mb(out or ['なし'])


def r_control_pairs(line):
    cps = AN['descriptive'].get('A_desc_control_pairs') or []
    rows = ['| 処置腕 | B₁ | B₂ | 場面 | %s | 二つの対比がともに確証で同じ向き |' % ' | '.join(SIZES), '|---|---|---|---|%s---|' % ('---|' * len(SIZES))]
    rows += ['| %s | %s | %s | %s | %s | %s |' % (x['treatment'], x['B1'], x['B2'], x['scenario'], ' | '.join('測定不能' if y['unmeasurable'] else ('—' if y['diff_pt'] is None else '%+.1f' % y['diff_pt']) for y in x['sizes']),
                                                   'はい' if x['both_confirmed_same_direction'] else '—') for x in cps]
    return ['- 対照どうしの差（機械の転記・B₁−B₂ の pt・読み条項 (v)）:'] + mb(rows + [x['string'] for x in cps if x.get('string')])


def r_recalc(line):
    out = []
    for p in AN['measurable']['per_contrast']:
        ds = '・'.join('%s %.3f（解釈条項の発火 %s）' % ({'room': '余地のある向き', 'opposite': '逆向き'}[dn], v['p_card_D1_first'], f3(v.get('clause_rate_among_fit'))) for dn, v in p['directions'].items())
        rs = '・'.join(sorted({v['reason'] for v in p['directions'].values() if v.get('reason')}))
        out.append('%s: d0 %s・%s%s' % (p['id'], '—' if p['d0'] is None else '%+.3f' % p['d0'], ds, '（%s）' % rs if rs else ''))
    return ['- 実測の対照の率での初段の札の確率（機械の転記・両向き・Δ は凍結時の値・観測された効果量は使わない・基底と 4B の水準差 d0 は実測）:'] + mb(out)


def r_measrec(line):
    ME = T['reading_selection']['measurable_effect_type']; M_ = AN['measurable']
    return ['- 測れた効果種の計算の記録（機械の転記）:'] + mb(['B=%d・seed %d・閾値 %s・Δ ±%s・向き %s・区間の水準 %s・下限 %s' % (M_['B'], ME['seed'], ME['threshold'], ME['delta'], M_.get('directions'), M_.get('ci_level'), ME['blind_below'])])


def r_pred(line):
    if not PRED:
        return None
    return ['- 封印予想との照合（機械の転記）:'] + mb([json.dumps(PRED.get('summary', PRED), ensure_ascii=False)[:2000]]) + ['- **帯の的中は誰の判断の重みも変えない**。']


def r_freeze(line):
    if not FV:
        return None
    return ['- 凍結物の検証（機械の転記）:'] + mb(['freeze_A --verify: %d/%d 一致' % (FV['matched'], FV['total'])])


LINE_RULES = [('- 前提: 凍結設計', r_premise), ('1. 利益相反（第一条項', r_coi), ('3. 走行の事実の一行', r_runfacts), ('4. **門0.5 の分岐', r_identity0), ('5. **上向きの確証', r_upward),
              ('6. **札の内訳**', r_labels6), ('7. **到達の見込みと測れた効果種**', r_reach7), ('- 測れた対比の本数（効果種ごと', r_coverage),('要約文は次の定型のみ', r_summary_sentence), ('- 器材: 走行器', r_tools), ('- 環境: 機種ごとの GPU 型', r_env),
              ('- 整合: 〔integrity_A', r_integ), ('- 門0.5（凍結前', r_g05), ('- 門2（パイロット・一度）', r_gate2), ('- 校正腕と撤退条件', r_calib), ('- 測定不能（腕 × 規模 × 場面', r_unmeas), ('- 錨帯（', r_anchor),
              ('- 環境（橋・環境帯', r_env3), ('- refuse 門（全分母で名目有意', r_refuse), ('- 様式門（', r_style), ('- 〔対比 id〕: 上限', r_demote), ('〔analyze_A の表', r_bigtable), ('- 確証札の定型', r_label_strings),
              ('- 残存規模の非連続と端の欠けの注', r_residual_gap), ('- 〔二つの対照を持つ処置腕', r_control_pairs), ('- 判定者どうしの κ（すべての対', r_judge_inter), ('- 位置の記述（`judge_validity.position`', r_judge_position),('〔`print_strings.floor_desc`', r_floor),
              ('- Nstr−Onull・Ncold−N', r_desc_pairs), ('- 応答様式 (a)(b)・検査認識の言及率', r_style_desc), ('- 錨の走行間差', r_anchor_desc), ('- レシピ対', r_recipe), ('- スタック差', r_stack),
              ('- 環境差（橋', r_envdesc), ('- 残った規模の一覧', r_residual), ('- 〔`tools/confirm_A.py` と格子と同じ関数', r_recalc), ('- 測れた効果種の計算の記録', r_measrec), ('- 封印予想（', r_pred), ('- `tools/freeze_A.py --verify`', r_freeze)]
TABLE_RULES = [('| 族 | m | 判定可能 |', t_summary), ('| 範囲（機種 × 場面） |', t_judge), ('| 場面 | 対照腕 |', t_ctrl), ('| 札 | 件数 | 先置する読み', t_reading), ('| 閾値 | 確証 |', t_sens),
               ('| 対比 id | A の基底 |', t_detect), ('| 効果種 | 凍結時の見込み', t_reach), ('| 効果種 × 場面 |', t_critical)]

tl = open(TP, encoding='utf-8').read().replace('\r\n', '\n').split('\n')
start = next(i for i, l in enumerate(tl) if l.startswith('## 0.'))
OUT_LINES = ['# 段階 A 結果報告 草案%d（機械組み立て・`tools/build_report_A.py` %s・%s UTC）' % (a.draft, VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')), '',
             '- 雛形 `%s`（SHA16 %s）の節順で組み立てた。機械の区画の外の記入欄（〔 〕）は起草者が埋める（`tools/report_lint.py` が埋め残しと未登録の数を止める）。' % (os.path.relpath(TP, REPO).replace('\\', '/'), sha(TP)),
             '- 集計の検査用の印: %s・足りない記録: %s' % ('・'.join(AN.get('dev_marks') or []) or 'なし', '・'.join(AN.get('missing') or []) or 'なし'),
             '- 打ち込んだ数の一覧（`report_rules.typed_numbers`・起草者が記入し、ここに無い数を機械の区画の外に書かない）: 〔日付・SHA16・SHA-256・費用の実績・逸脱番号・雛形の SHA16 の一覧〕']
if a.allow_dev_marks:
    OUT_LINES.append('- 検査用の口 --allow-dev-marks で組み立てた（検査用の印が残っても走査の違反にしない・公開する報告には使わない）')   # 機械の区画の外に数を書かない（走査器の未登録の数・反映の確かめで見つけた）
for i in range(0, start):
    if tl[i].startswith('- 前提:'):
        OUT_LINES += r_premise(tl[i])
OUT_LINES.append('')
i = start; used = collections.Counter()
while i < len(tl):
    line = tl[i]; done = False
    for key, fn in TABLE_RULES:
        if line.startswith(key):
            j = i
            while j < len(tl) and tl[j].startswith('|'):
                j += 1
            rep = fn(tl[i:j])
            if rep is not None:
                OUT_LINES += rep + tl[i:j]; used[key] += 1; i = j; done = True   # 雛形の行は消さず、機械の区画の後にそのまま残す（採否表 P95）
            break
    if done:
        continue
    for key, fn in LINE_RULES:
        if key in line:
            rep = fn(line)
            if rep is not None:
                OUT_LINES += rep; used[key] += 1
            break
    OUT_LINES.append(line)   # 雛形の行は消さない（採否表 P95）
    i += 1
heads_t = [l for l in tl[start:] if l.startswith('#')]; heads_o = [l for l in OUT_LINES if l.startswith('#')][1:]
if heads_t != heads_o:
    sys.exit('見出しの列が雛形と一致しない（停止）')
out = a.out or os.path.join(REPO, 'records', 'A', 'results-report-A-draft%d-%s.md' % (a.draft, datetime.date.today().isoformat()))
if os.path.exists(out) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % out)
TEXT = '\n'.join(OUT_LINES) + '\n'
open(out, 'w', encoding='utf-8', newline='\n').write(TEXT)
SIDE = report_lint.write_sidecar(out, TEXT, T, builder='tools/build_report_A.py %s' % VERSION)   # 機械の区画の中身の SHA16（採否表 P96）
unused = [k for k, _ in LINE_RULES + TABLE_RULES if not used[k]]
TL = frozenset(tl); V = report_lint.lint(TEXT, T, TL, sidecar=SIDE, allow_dev_marks=a.allow_dev_marks); kinds = collections.Counter(v['kind'] for v in V)
print('[build_report_A] written %s（機械の区画 %d・記録 %s）| 置き換え %d 規則・当たらなかった規則 %d（%s）| 走査の違反 %d %s' % (
    out, len(SIDE['blocks']), report_lint.sidecar_path(out), len(used), len(unused), '・'.join(unused) or 'なし', len(V), dict(kinds)))
BAD = [v for v in V if v['kind'] != '埋め残し']
if BAD:
    sys.exit('[build_report_A] 記入欄の埋め残しのほかの違反 %d 件（%s）。組み立てを止める（採否表 P96）' % (len(BAD), dict(collections.Counter(v['kind'] for v in BAD))))
