# -*- coding: utf-8 -*-
"""qf_select_B.py v1 —— 品質床の課題の選定の判定（登録者裁定 D145）を、候補の測定の記録（相 qfcand・裁定 D146）に機械で当てる（2026-09-19 作）。

判定は正本 `quality_floor.decision_order` の順:
  (i) 前置きありで、両方の土台で正答率が base_min 以上、かつ書式外の率が閾値以下の候補 → その中から登録者が選ぶ（裁定 D66）
  (ii) 無ければ、両方の土台で base_min_floor 以上、かつ書式外の率が閾値以下の候補のうち、低い方の土台の正答率が最も高いもの（手当て）
  (iii) 正答率は base_min_floor に届くのに書式外の率だけが閾値を超える候補しか無ければ、付けない側に戻り、腕 N の測定に (i)(ii) を当てる
  (iv) どれにも当たらなければ止めて登録者に上げる
比べ方: 正答率＝正答 ÷ 使えた試行（書式外は不正解）・書式外の率＝書式外 ÷ 使えた試行。**分数で厳密に比べる**（浮動小数の丸めで境目が揺れない）。
正答率の下限は「以上」で満たす。書式外の率は閾値（`dilution_gate.threshold_pt`）を**超えたら**当たる（境目ちょうどは当たらない）。
候補のセルに api_error が一件でもあれば判定しない（`candidate_session.api_error_rule`）。
入力の照合: 走行の記録の組（候補 × 腕）がそろい重複が無いこと・問いの数・断片の SHA16 が登録と同じこと・腕と問いの出し方の対応・
セッション記録の files_sha16_lf と手元のファイルの SHA16 が一致すること（生テキストは手元にあれば raw_sha16_lf と照らす）。dry-run の記録は --allow-dry でしか読まない。
出力: records/B/qf-selection/qf-select-<日付>.{md,json}（--force が無ければ上書きしない）。**登録者の選定（裁定 D66）はこの後**——本器は枝と候補を印字するだけ。
用法: python tools/qf_select_B.py [--root results] [--session 1] [--allow-dry] [--force] ／ --selftest（合成の件数で全枝を確かめる）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, glob, argparse, datetime
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
QF = T['quality_floor']
CS = QF['candidate_session']
FENCE = '本記録のいかなる記述も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def _frac(x):
    return Fraction(str(x))


def cell_metrics(trials):
    """一セルの件数（正答率と書式外の率の分母は使えた試行・書式外は不正解）。"""
    n = len(trials)
    ok = [r for r in trials if r['status'] == 'ok']
    c = {'n': n, 'n_ok': len(ok), 'api_error': n - len(ok), 'correct': sum(1 for r in ok if r['correct'] is True and not r['format_fail']),
         'format_fail': sum(1 for r in ok if r['format_fail']), 'truncated': sum(1 for r in ok if r.get('truncated')),
         'correct_but_format_fail': sum(1 for r in ok if r['correct'] is True and r['format_fail'])}
    return c


def _acc(c):
    return Fraction(c['correct'], c['n_ok']) if c['n_ok'] else None


def _ffr(c):
    return Fraction(c['format_fail'], c['n_ok']) if c['n_ok'] else None


def decide(M, T_=None):
    """判定の順（裁定 D145）。M は {候補の鍵: {腕: 件数}}（`cell_metrics` の形）。返り値は枝と候補と理由。"""
    T_ = T_ or T
    Q = T_['quality_floor']
    bmin, floor = _frac(Q['base_min']), _frac(Q['base_min_floor'])
    thr = _frac(T_['dilution_gate']['threshold_pt']) / 100
    bases = list(Q['arms'])
    keys = [c['key'] for c in Q['task_candidates']]
    out = {'bases': bases, 'base_min': Q['base_min'], 'base_min_floor': Q['base_min_floor'], 'ff_threshold_pt': T_['dilution_gate']['threshold_pt'], 'rows': {}}
    errs = [(k, a, M[k][a]['api_error']) for k in keys for a in M.get(k, {}) if M[k][a]['api_error']]
    lack = [(k, a) for k in keys for a in bases + ['N'] if a not in M.get(k, {})]
    if lack:
        return dict(out, branch='incomplete', reason='候補 × 腕のセルが欠けている: %s' % lack, chosen=None, eligible=[])
    if errs:
        return dict(out, branch='incomplete', reason='候補のセルに api_error がある（判定せずに登録者に上げる・candidate_session.api_error_rule）: %s' % errs,
                    chosen=None, eligible=[])
    if any(M[k][a]['n_ok'] == 0 for k in keys for a in bases + ['N']):
        return dict(out, branch='incomplete', reason='使えた試行が零のセルがある', chosen=None, eligible=[])
    row = {}
    for k in keys:
        accs = {a: _acc(M[k][a]) for a in bases}
        ffs = {a: _ffr(M[k][a]) for a in bases}
        row[k] = {'min_acc': min(accs.values()), 'max_ff': max(ffs.values()), 'acc_N': _acc(M[k]['N']), 'ff_N': _ffr(M[k]['N'])}
        out['rows'][k] = {'min_acc': float(row[k]['min_acc']), 'max_ff_pt': float(100 * row[k]['max_ff']),
                          'acc_N': float(row[k]['acc_N']), 'ff_N_pt': float(100 * row[k]['ff_N'])}
    t1 = [k for k in keys if row[k]['min_acc'] >= bmin and row[k]['max_ff'] <= thr]
    if t1:
        return dict(out, branch='(i)', input_form='with_preamble', eligible=t1, chosen=None,
                    reason='前置きありで両方の土台が base_min 以上かつ書式外の率が閾値以下の候補がある。登録者がこの中から選ぶ（裁定 D66・推す順は task_tiebreak）')
    t2 = [k for k in keys if row[k]['min_acc'] >= floor and row[k]['max_ff'] <= thr]
    if t2:
        best = max(row[k]['min_acc'] for k in t2)
        top = [k for k in t2 if row[k]['min_acc'] == best]
        return dict(out, branch='(ii)', input_form='with_preamble', eligible=t2, chosen=top[0] if len(top) == 1 else None, tied=top if len(top) > 1 else [],
                    reason='手当て（裁定 D137）: base_min に届く候補が無く、base_min_floor 以上で書式外の率が閾値以下の候補のうち、低い方の土台の正答率が最も高いもの'
                           + ('（並んだので task_tiebreak で登録者が決める）' if len(top) > 1 else ''))
    r3 = [k for k in keys if row[k]['min_acc'] >= floor and row[k]['max_ff'] > thr]
    if r3:
        n1 = [k for k in r3 if row[k]['acc_N'] >= bmin and row[k]['ff_N'] <= thr]
        if n1:
            return dict(out, branch='(iii)-(i)', input_form='without_preamble', eligible=n1, chosen=None,
                        reason='書式外の率だけで落ちた候補で付けない側に戻り（裁定 D138）、腕 N の測定が base_min 以上かつ書式外の率が閾値以下。登録者がこの中から選ぶ')
        n2 = [k for k in r3 if row[k]['acc_N'] >= floor and row[k]['ff_N'] <= thr]
        if n2:
            best = max(row[k]['acc_N'] for k in n2)
            top = [k for k in n2 if row[k]['acc_N'] == best]
            return dict(out, branch='(iii)-(ii)', input_form='without_preamble', eligible=n2, chosen=top[0] if len(top) == 1 else None, tied=top if len(top) > 1 else [],
                        reason='書式外の率だけで落ちた候補で付けない側に戻り、腕 N の測定に手当てを当てた（正答率の最も高いもの）')
        return dict(out, branch='(iv)', input_form=None, eligible=[], chosen=None,
                    reason='書式外の率だけで落ちた候補で付けない側に戻ったが、腕 N の測定も条件を満たさない。止めて登録者に上げる')
    return dict(out, branch='(iv)', input_form=None, eligible=[], chosen=None,
                reason='前置きありで、どの候補も両方の土台で base_min_floor に届かない。止めて登録者に上げる（裁定 D137・前置きなしの測定は手元にある）')


def load_runs(root, session, allow_dry=False):
    """候補の測定の記録を読む（入力の照合つき）。返り値は（M, 走行の一覧, セッション記録, 問題の一覧）。"""
    problems = []
    tag = CS['tag']
    sp = os.path.join(root, 'sessions-B', '%s__s%d.json' % (tag, session))
    if not os.path.exists(sp):
        raise SystemExit('セッション記録が無い: %s' % sp)
    S = json.load(open(sp, encoding='utf-8'))
    if S.get('dry') and not allow_dry:
        raise SystemExit('dry-run のセッション記録なので読まない（--allow-dry）: %s' % sp)
    reg = QF['task_registered']['by_key']
    M, runs = {}, []
    for d in sorted(glob.glob(os.path.join(root, tag, '*'))):
        mp = os.path.join(d, 'manifest.json')
        if not os.path.exists(mp):
            continue
        m = json.load(open(mp, encoding='utf-8'))
        if int(m.get('session', -1)) != session:
            continue
        if m.get('dry_run') and not allow_dry:
            raise SystemExit('dry-run の走行の記録なので読まない（--allow-dry）: %s' % d)
        k, a = m['task'], m['arm']
        if a in M.get(k, {}):
            problems.append('候補 × 腕の走行が二本ある: %s × %s' % (k, a))
            continue
        want_form = 'without_preamble' if a == 'N' else 'with_preamble'
        if m.get('input_form') != want_form:
            problems.append('%s: 問いの出し方 %s が腕 %s と合わない' % (m['run_key'], m.get('input_form'), a))
        if m.get('fragment_sha16') != reg[k]['fragment_sha16']:
            problems.append('%s: 断片の SHA16 %s が登録 %s と違う' % (m['run_key'], m.get('fragment_sha16'), reg[k]['fragment_sha16']))
        tp = os.path.join(d, 'trials-%s.jsonl' % m['run_key'])
        trials = list(runs_B.iter_jsonl(tp))
        if not allow_dry and len(trials) != QF['items']:
            problems.append('%s: 試行の数 %d が登録した問いの数 %d と違う' % (m['run_key'], len(trials), QF['items']))
        if sorted(r['trial_index'] for r in trials) != list(range(len(trials))):
            problems.append('%s: 試行の番号が連番でない' % m['run_key'])
        # セッション記録の SHA16 と照らす（転送の検査）
        for f in sorted(glob.glob(os.path.join(d, '*'))):
            rel = os.path.relpath(f, root).replace('\\', '/')
            table = S.get('raw_sha16_lf' if os.path.basename(f).startswith('raw-') else 'files_sha16_lf') or {}
            if table.get(rel) != runs_B.sha16_file(f):
                problems.append('%s: SHA16 がセッション記録と違う（%s 対 %s）' % (rel, runs_B.sha16_file(f), table.get(rel)))
        M.setdefault(k, {})[a] = cell_metrics(trials)
        runs.append({'run_key': m['run_key'], 'task': k, 'arm': a, 'input_form': m.get('input_form'), 'dir': os.path.relpath(d, root).replace('\\', '/')})
    missing = sorted(set(S.get('files_sha16_lf') or {}) - {os.path.relpath(f, root).replace('\\', '/') for r in runs for f in glob.glob(os.path.join(root, r['dir'], '*'))})
    if missing:
        problems.append('セッション記録にあるファイルが手元に無い: %s' % missing[:4])
    return M, runs, S, problems


def fallback_null(obs_acc):
    """手当ての下の帰無発火率（二標本・観測した正答率での一セルと選定後のセル数・`rules_B.qf_multiplicity`）。"""
    import rules_B
    main_arms = T['arms']['main']
    post = len([a for a in main_arms if '+v' in a or '-v' in a]) - len(QF['arms'])
    return rules_B.qf_multiplicity(T, post, bases=(float(obs_acc),))


def _selftest():
    def cell(correct, ff, n=200, err=0):
        return {'n': n, 'n_ok': n - err, 'api_error': err, 'correct': correct, 'format_fail': ff, 'truncated': 0, 'correct_but_format_fail': 0}

    def M_(j_o, j_n, j_N, m_o, m_n, m_N):
        return {'jcqa': {'O-Ncold': cell(*j_o), 'Onull': cell(*j_n), 'N': cell(*j_N)},
                'jmmlu_stem': {'O-Ncold': cell(*m_o), 'Onull': cell(*m_n), 'N': cell(*m_N)}}
    # (i): jcqa が両方の土台で 0.85 ちょうど以上・書式外 10% ちょうど（境目は当たらない）
    d = decide(M_((170, 20), (180, 1), (185, 0), (120, 2), (125, 1), (130, 0)))
    assert d['branch'] == '(i)' and d['eligible'] == ['jcqa'], d
    # 低い方の土台で見る: jcqa の Onull が 0.845 なら (i) に入らず (ii)（平均で見る誤りは (i) に入れてしまう）
    d = decide(M_((190, 0), (169, 0), (185, 0), (150, 0), (150, 0), (150, 0)))
    assert d['branch'] == '(ii)' and d['chosen'] == 'jcqa' and d['eligible'] == ['jcqa', 'jmmlu_stem'], d
    # 書式外 10.5% は当たる（超えたら）→ (i) に入らず。ほかの候補が 0.70 以上なら (ii) で採る
    d = decide(M_((190, 21), (190, 0), (190, 0), (141, 0), (142, 0), (150, 0)))
    assert d['branch'] == '(ii)' and d['chosen'] == 'jmmlu_stem', d
    # (ii) の同点は並べて登録者に
    d = decide(M_((150, 0), (160, 0), (160, 0), (150, 0), (155, 0), (150, 0)))
    assert d['branch'] == '(ii)' and d['chosen'] is None and d['tied'] == ['jcqa', 'jmmlu_stem'], d
    # (iii): 正答率は届くが書式外だけで落ちる候補しか無い → 腕 N で (i)
    d = decide(M_((175, 25), (180, 0), (186, 1), (100, 0), (100, 0), (100, 0)))
    assert d['branch'] == '(iii)-(i)' and d['eligible'] == ['jcqa'] and d['input_form'] == 'without_preamble', d
    # (iii) で腕 N も届かなければ (iv)
    d = decide(M_((175, 25), (180, 0), (130, 0), (100, 0), (100, 0), (100, 0)))
    assert d['branch'] == '(iv)', d
    # (iv): どの候補も 0.70 に届かない（付けない側に戻らず止まる——裁定 D145 の COI の選択）
    d = decide(M_((139, 0), (150, 0), (190, 0), (100, 0), (100, 0), (190, 0)))
    assert d['branch'] == '(iv)' and d['input_form'] is None, d
    # api_error が一件でもあれば判定しない
    d = decide(M_((190, 0), (190, 0), (190, 0), (150, 0), (150, 0, 200, 1), (150, 0)))
    assert d['branch'] == 'incomplete', d
    # 分数で比べる: 17/20 はちょうど 0.85 で「以上」を満たす（(i)）。169/199（0.849…）は満たさず手当て（(ii)）
    assert decide({'jcqa': {'O-Ncold': cell(17, 0, 20), 'Onull': cell(17, 0, 20), 'N': cell(17, 0, 20)},
                   'jmmlu_stem': {'O-Ncold': cell(100, 0), 'Onull': cell(100, 0), 'N': cell(100, 0)}})['branch'] == '(i)'
    d = decide({'jcqa': {'O-Ncold': cell(169, 0, 199), 'Onull': cell(190, 0), 'N': cell(190, 0)},
                'jmmlu_stem': {'O-Ncold': cell(100, 0), 'Onull': cell(100, 0), 'N': cell(100, 0)}})
    assert d['branch'] == '(ii)' and d['chosen'] == 'jcqa', d
    c = cell_metrics([{'status': 'ok', 'correct': True, 'format_fail': False}, {'status': 'ok', 'correct': False, 'format_fail': True},
                      {'status': 'api_error', 'correct': None, 'format_fail': None}])
    assert c == {'n': 3, 'n_ok': 2, 'api_error': 1, 'correct': 1, 'format_fail': 1, 'truncated': 0, 'correct_but_format_fail': 0}, c
    fb = fallback_null(0.8)
    assert 'cell_at_080' in fb and 0 < fb['cell_at_080'] < 0.05, fb
    print('[qf_select_B selftest] 判定の順の全枝（(i)・低い方で見る (ii)・書式外の境目・同点・(iii)-(i)・(iii)→(iv)・(iv)・api_error・分数の比較）と件数の数え方・手当ての帰無発火率: 通った')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--root', default=os.path.join(REPO, 'results'))
    ap.add_argument('--session', type=int, default=1)
    ap.add_argument('--allow-dry', action='store_true')
    ap.add_argument('--out', default=None)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    M, runs, S, problems = load_runs(a.root, a.session, a.allow_dry)
    d = decide(M) if not problems else {'branch': 'incomplete', 'reason': '入力の照合に落ちた', 'chosen': None, 'eligible': [], 'rows': {}}
    if d['branch'] == '(ii)' or d['branch'] == '(iii)-(ii)':
        k = d['chosen'] or (d.get('tied') or [None])[0]
        if k:
            obs = d['rows'][k]['min_acc'] if d['branch'] == '(ii)' else d['rows'][k]['acc_N']
            d['fallback_null'] = fallback_null(obs)
    jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    out_md = a.out or os.path.join(REPO, 'records', 'B', 'qf-selection', 'qf-select-%s.md' % jst.strftime('%Y-%m-%d'))
    out_json = os.path.splitext(out_md)[0] + '.json'
    if not a.force and any(os.path.exists(p) for p in (out_md, out_json)):
        sys.exit('既にある（--force で上書き）: %s' % out_md)
    rec = {'tool': 'tools/qf_select_B.py %s' % VERSION, 'rule': '裁定 D145（正本 quality_floor.decision_order）', 'session': a.session,
           'session_record_sha16': runs_B.sha16_file(os.path.join(a.root, 'sessions-B', '%s__s%d.json' % (CS['tag'], a.session))),
           'dry': bool(S.get('dry')), 'problems': problems, 'cells': M, 'runs': runs, 'decision': d, 'topk': S.get('topk'), 'fence': FENCE}
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    json.dump(rec, open(out_json, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    L = ['# 品質床の課題の選定の判定（裁定 D145・`tools/qf_select_B.py` %s の出力）' % VERSION, '',
         '- セッション %d（セッション記録の SHA16 %s）%s。入力の照合: %s。' % (a.session, rec['session_record_sha16'], '・**dry-run**' if rec['dry'] else '',
                                                         '問題なし' if not problems else '**%d 件の問題**' % len(problems)), '']
    for p_ in problems:
        L.append('  - %s' % p_)
    L += ['', '| 候補 | 腕 | 問い | 使えた試行 | 正答 | 書式外 | 打ち切り | api_error | 正答率 | 書式外の率 |', '|---|---|---|---|---|---|---|---|---|---|']
    for k, arms in M.items():
        for arm_, c in arms.items():
            L.append('| %s | %s | %d | %d | %d | %d | %d | %d | %s | %s |' % (k, arm_, c['n'], c['n_ok'], c['correct'], c['format_fail'], c['truncated'], c['api_error'],
                                                                         '%.4f' % (c['correct'] / c['n_ok']) if c['n_ok'] else '—',
                                                                         '%.4f' % (c['format_fail'] / c['n_ok']) if c['n_ok'] else '—'))
    L += ['', '- **枝: %s**（%s）' % (d['branch'], d.get('reason')), '- 条件を満たす候補: %s' % ('・'.join(d.get('eligible') or []) or 'なし'),
          '- 機械で決まる候補: %s' % (d.get('chosen') or 'なし（登録者の選定・裁定 D66）'), '- 問いの出し方: %s' % d.get('input_form')]
    if d.get('fallback_null'):
        L.append('- 手当ての下の帰無発火率（二標本・上限・`rules_B.qf_multiplicity`）: %s' % json.dumps(d['fallback_null'], ensure_ascii=False))
    L += ['- top_k の確かめ（裁定 D142）: %s' % json.dumps({k: (S.get('topk') or {}).get(k) for k in ('status', 'top_k', 'top_k_values')}, ensure_ascii=False), '', FENCE, '']
    open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
    print('[qf_select_B] 枝 %s・候補 %s・問題 %d 件 → %s' % (d['branch'], d.get('eligible'), len(problems), os.path.relpath(out_md, REPO)))
