# -*- coding: utf-8 -*-
"""dry_run_B.py v6 —— 段階 B の器材の**合成データによる検査**（札の全経路を一度ずつ以上発火させる）。
v6（2026-09-19 の夜・封印の後・結果の前・独立の目を通っていない）: **予想の照合**（`tools/compare_predictions_B.py`）を通す経路——門が開いた回は集計と門の記録で、門1 が閉じた回は門の記録だけで照らす——と、報告の区画 L の経路を足した。照らすのは**封印した実物の予想**（`records/predictions`）で、合成データの結果と照らした出力は合成データの置き場に置き、印を付ける。
v5（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: S4 の札を結果だけの名にし（経路の名は正本の札から作る）、門で保留・封印の照合の三つを足した（裁定 D134・D135）。td の特異性の三つの札（裁定 D133）・様式門に当たった非有意（採否表 P401）・選定後の品質床の相手の重複（採否表 P403）・副位置の読みの参照の行（裁定 D139）・報告の管理図の要約と、門の記録の食い違いで報告の器が止まること（採否表 P410・P403）を足した。

器材の整備の計画 `records/B/tooling-plan-B-2026-09-18.md` の表の経路を、合成データ（`synth_B.py`）で作り、
`gate_B.py`（門1 と選定）と `analyze_B.py`（本走行の集計と札）を走らせて、**どの経路が発火したか**を数える。
発火しない経路があれば非零で終わる（凍結の前に全経路が発火していることが条件）。
合成データは results/_synth/ に置き、行にも置き場にも dry-run の印を立てる（公開の置き場には入れない）。
出力: records/B/dry-run-B-<日付>.md（--out で変える・--force が無ければ上書きしない）。
用法: python tools/dry_run_B.py [--keep] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, argparse, datetime, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

T = runs_B.load_T()

VERSION = 'v6'
REPO = runs_B.REPO
PY = sys.executable
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--keep', action='store_true', help='合成データを消さない')
a = ap.parse_args()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'dry-run-B-%s.md' % jst.strftime('%Y-%m-%d'))
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)

PATHS = ['確証', '確証（登録された向きと逆）', '封印した符号と一致', '判定不能（検閲）', '判定不能（採点欠落）', '判定不能（測れなかった）',
         '判定保留（書式外転位）', '判定保留（refuse 転位・差）', '判定保留（refuse 転位）', '判定保留（様式転位）', '注（様式）',
         '判定不能（品質床）', '非有意', '門1 を閉じる', '記録の不在（incomplete）', '全候補が非正', '同点の割り方',
         '床・天井で選定から外す'] + ['S4: %s' % l_ for l_ in T['descriptive_families']['B_desc_S4']['three_way']['labels']] + ['S4: 余地の条項', 'S4: 門で保留',
         'S4 の照合: 当たり', 'S4 の照合: 外れ', 'S4 の照合: 言えない',
         '希釈が効く場面（書式外が分子を食う）', '採点の規約（書式外と refuse に判定を付けない）', '門が開いていないと集計器が止まる', '束縛の食い違いで集計器が止まる',
         '中断と再開', '同一性選別の走行', '未測定（ループ・打ち切り）', '封印の欠けで止まる',
         # v4（2026-09-19・直しの監査で、判定の規則が器に入っていなかった件と、経路の表に無かった件を足した）
         '等質性の注（ランダム方向の不均一）', '等質性の内側', 'td の特異性: 書かない', 'td の特異性: 書ける', 'td の特異性: td のほうが動いた',
         'refuse 門: 読めた分母だけで保留', '品質床の api_error の門（選定の段）', '品質床の api_error の門（選定後）',
         '様式・言及の欄が空（採点欠落）', '管理図: 帯の外かつ有意', '管理図: 帯の外だが有意でない', '管理図: 帯の内側', '管理図の注が対比に付く',
         '副位置の読み（層ごとの分離）', 'S4 の区間は Newcombe', '報告の組み立て（全区画・走査器）',
         # v5（2026-09-19・最後の系統外の巡の後）
         '様式門に当たった非有意（札は非有意のまま）', '集計: 選定後の相手の重複', '副位置の読み: 参照の行',
         '報告: 管理図の要約', '報告: 門の記録の食い違いで止まる',
         # v6（2026-09-19 の夜・封印の後）
         '予想の照合（両者・向き・S4・全体）', '予想の照合: 門1 が閉じた回', '報告: 予想の照合の区画']
_s4_labels = T['descriptive_families']['B_desc_S4']['three_way']['labels']
_s4_paths = [p for p in PATHS if p.startswith('S4: ')]
assert _s4_paths == ['S4: %s' % l_ for l_ in _s4_labels] + ['S4: 余地の条項', 'S4: 門で保留'], (
    '経路の表の S4 の枝が正本の札と合わない（札の四つ・余地の条項・門で保留の六つになるはず）', _s4_paths, _s4_labels)
fired = {k: [] for k in PATHS}
rows = []


def run(cmd):
    r = subprocess.run([PY] + cmd, capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


for case in ('all', 'gate1_closed', 'nonpositive', 'tie', 'censor_candidates', 'scoring_gap', 's4_branches', 's4_up', 's4_floor', 'dilution_causal', 'incomplete',
             'refuse_readable', 'api_error_gate', 'style_gap', 'chart', 's4_undecided', 's4_floor_rule', 's4_gate', 'post_partner_dup'):
    root = os.path.join('results', '_synth', case)
    rc, out = run(['tools/synth_B.py', '--case', case, '--out-root', root])
    assert rc == 0, out
    rc_g, out_g = run(['tools/gate_B.py', '--root', root, '--allow-dry', '--out', os.path.join(root, 'gate-B.md'), '--force'])
    assert rc_g in (0, 2), ('門の器が思わぬ終了コードで落ちた', rc_g, out_g[-400:])   # 採否表 P296
    G = json.load(open(os.path.join(REPO, root, 'gate-B.json'), encoding='utf-8'))
    if G['verdict'] == 'incomplete':
        fired['記録の不在（incomplete）'].append(case)
    sel = G['selection']
    if not G['gate1']['open']:
        fired['門1 を閉じる'].append(case)
    if sel.get('nonpositive_stop'):
        fired['全候補が非正'].append(case)
    if sel.get('tie_note'):
        fired['同点の割り方'].append(case)
    if any(r.get('censored') for r in G['candidates']):
        fired['床・天井で選定から外す'].append(case)
    if any('api_error' in str(r.get('note', '')) for r in (G.get('quality_floor_rows') or [])):
        fired['品質床の api_error の門（選定の段）'].append(case)
    rec = {'case': case, 'gate_verdict': G['verdict'], 'gate_rc': rc_g, 'labels': {}}
    if G['gate1']['open']:
        seal = os.path.join(root, 'seal-B.json')
        cmd = ['tools/analyze_B.py', '--gate', os.path.join(root, 'gate-B.json'), '--root', root, '--allow-dry',
               '--out', os.path.join(root, 'analysis-B.md'), '--force']
        if os.path.exists(os.path.join(REPO, seal)):
            # 合成の封印は全対比ぶんではないので、**まず止まることを確かめてから**検査用の口で進む（裁定 D79・採否表 P277）
            rc_stop, _ = run(cmd + ['--seal', seal])
            if rc_stop != 0:
                fired['封印の欠けで止まる'].append(case)
            cmd += ['--seal', seal, '--allow-partial-seal']
        # **門が開いていなければ止まることを先に確かめる**（裁定 D109・採否表 P318）
        if G.get('verdict') != 'open':
            rc_stop2, _ = run(cmd)
            if rc_stop2 != 0:
                fired['門が開いていないと集計器が止まる'].append(case)
            cmd += ['--allow-not-open']
        # **束縛の食い違いで止まることを確かめる**（裁定 D105・採否表 P304）。
        # 合成データの走行は場合ごとの「best」で作るが、門が実際に選ぶ組はそれと違うことがある
        # （候補が希釈や床・天井で外れる場合）。そのとき集計器は止まるのが正しい。
        rc_b, out_b = run(cmd)
        if rc_b != 0 and '門の選んだ層 × 係数と違う' in out_b:
            fired['束縛の食い違いで集計器が止まる'].append(case)
            cmd += ['--allow-unbound']
        # **管理図**（裁定 D110・D127）: 管理図の器を走らせ、集計器に渡す
        rc_c, out_c = run(['tools/control_chart_B.py', '--root', root, '--allow-dry', '--out', os.path.join(root, 'chart-B.md'), '--force'])
        assert rc_c in (0, 1) and os.path.exists(os.path.join(REPO, root, 'chart-B.json')), ('管理図の器が落ちた', rc_c, out_c[-400:])   # 異常があれば 1 で終わる器
        CH = json.load(open(os.path.join(REPO, root, 'chart-B.json'), encoding='utf-8'))
        for pnt in CH['points']:
            vd = pnt.get('verdict', '')
            if '帯の外かつ有意' in vd:
                fired['管理図: 帯の外かつ有意'].append(case)
            elif '帯の外だが有意でない' in vd:
                fired['管理図: 帯の外だが有意でない'].append(case)
            elif vd.startswith('帯の内側'):
                fired['管理図: 帯の内側'].append(case)
        cmd += ['--chart', os.path.join(root, 'chart-B.json')]
        rc_a, out_a = run(cmd)
        assert rc_a == 0, out_a
        A = json.load(open(os.path.join(REPO, root, 'analysis-B.json'), encoding='utf-8'))
        if any('管理図' in n for r in A['confirm'] for n in (r.get('notes') or [])):
            fired['管理図の注が対比に付く'].append(case)
        for h in A.get('homogeneity') or []:
            fired['等質性の注（ランダム方向の不均一）' if h.get('note') else '等質性の内側'].append(case) if h.get('note') is not None else None
        for t_ in A.get('td_specificity') or []:
            _tl = 'td の特異性: %s' % t_.get('label')           # 札は `rules_B.td_specificity_family` の三つ（裁定 D133）
            if _tl in fired:
                fired[_tl].append(case)
        if any(q.get('missing') and '相手の重複' in str(q.get('note', '')) for q in (A.get('quality_post') or [])):
            fired['集計: 選定後の相手の重複'].append(case)
        for r in A['confirm']:
            if r.get('label') == '非有意' and '判定保留（様式転位）' in (r.get('fired') or []):
                fired['様式門に当たった非有意（札は非有意のまま）'].append(case)
        for r in A['confirm']:
            rg = r.get('refuse_gate') or {}
            if rg.get('hold') and not any('答えた' in x for x in rg.get('reasons', [])) and any('読めた' in x for x in rg.get('reasons', [])):
                fired['refuse 門: 読めた分母だけで保留'].append(case)
            if r.get('label') == '判定不能（採点欠落）' and any('様式・言及の欄が空' in n for n in (r.get('notes') or [])):
                fired['様式・言及の欄が空（採点欠落）'].append(case)
        if any('api_error' in str(q.get('note', '')) for q in (A.get('quality_post') or [])):
            fired['品質床の api_error の門（選定後）'].append(case)
        if (A.get('s4') or {}).get('interval') == 'Newcombe':
            fired['S4 の区間は Newcombe'].append(case)
        # **副位置の読み**（裁定 D132）: 合成の方向と配列で layers_B を走らせる（層が深いほど分離が大きくなるように作ってある）
        if case == 'all':
            rc_l, out_l = run(['tools/layers_B.py', '--directions', os.path.join(root, 'dirB', 'directions.npz'), '--root', root,
                               '--allow-dry', '--out', os.path.join(root, 'layers-B.md'), '--force'])
            assert rc_l == 0, ('副位置の読みの器が落ちた', out_l[-400:])
            LY = json.load(open(os.path.join(REPO, root, 'layers-B.json'), encoding='utf-8'))
            aucs = [r_.get('auc') for r_ in LY['rows']]
            if all(x is not None for x in aucs) and aucs == sorted(aucs) and aucs[-1] > aucs[0]:
                fired['副位置の読み（層ごとの分離）'].append(case)
            # **参照の行**（裁定 D139）: 軸がそろい、層ごとに行があること
            _ax = {r_['axis'] for r_ in (LY.get('reference_rows') or [])}
            if _ax >= {'rand0', 'rand1', 'rand2', 'td', 'Nk'} and len(LY.get('reference_rows') or []) == len(_ax) * len(LY['rows']):
                fired['副位置の読み: 参照の行'].append(case)
            # **報告の組み立ての通し**（2026-09-19）: 整合検査 → 抽出検査（対応表は公開の置き場の外）→ 報告の組み立て（走査器つき）
            import tempfile as _tf
            rc_i, out_i = run(['tools/integrity_B.py', '--tag', T['tags']['main'], '--root', root, '--allow-dry',
                               '--out', os.path.join(root, 'integrity-B.md'), '--force'])
            _keys = _tf.mkdtemp(prefix='op4b_keys_')
            rc_s, out_s = run(['tools/sample_inspection_B.py', '--tag', T['tags']['main'], '--root', root, '--allow-dry', '--keydir', _keys,
                               '--out', os.path.join(root, 'sampling-B-sample.txt'), '--force'])
            assert rc_s == 0, ('抽出検査が落ちた', out_s[-400:])
            # **予想の照合**（v6・裁定 D148）: 封印した実物の予想を、合成データの結果と照らす（出力は合成データの置き場・印つき）
            rc_p, out_p = run(['tools/compare_predictions_B.py', '--gate', os.path.join(root, 'gate-B.json'), '--analysis', os.path.join(root, 'analysis-B.json'),
                               '--allow-dry', '--out', os.path.join(root, 'predictions-check-B.md'), '--force'])
            _PCJ = os.path.join(REPO, root, 'predictions-check-B.json')
            if rc_p == 0 and os.path.exists(_PCJ):
                _pc = json.load(open(_PCJ, encoding='utf-8'))
                _m = sum(F_['m'] for F_ in T['families'].values())
                if len(_pc['results']) == 2 and _pc.get('dry_marks') and all(
                        sum(R_['counts']['向き'].values()) == _m and sum(R_['counts']['S4'].values()) == 1 and sum(R_['counts']['全体'].values()) == 2
                        for R_ in _pc['results'].values()):
                    fired['予想の照合（両者・向き・S4・全体）'].append(case)
            else:
                rec['compare_error'] = (out_p or '')[-600:]
            _rep_cmd = ['tools/build_report_B.py', '--analysis', os.path.join(root, 'analysis-B.json'), '--gate', os.path.join(root, 'gate-B.json'),
                        '--integrity', os.path.join(root, 'integrity-B.json'), '--sampling', os.path.join(root, 'sampling-B-seal.json'),
                        '--layers', os.path.join(root, 'layers-B.json'), '--chart', os.path.join(root, 'chart-B.json'),
                        '--predictions-check', os.path.join(root, 'predictions-check-B.json'), '--allow-dry', '--force-problems',
                        '--out', os.path.join(root, 'report-B.md'), '--force', '--lint']
            rc_r, out_r = run(_rep_cmd)
            _rep = os.path.join(REPO, root, 'report-B.md')
            _txt = open(_rep, encoding='utf-8').read() if os.path.exists(_rep) else ''
            if rc_r == 0 and _txt and '〔結果' not in _txt and '{{' not in _txt:
                fired['報告の組み立て（全区画・走査器）'].append(case)
            else:
                rec['report_error'] = (out_r or '')[-600:]
            # **管理図の要約**（採否表 P410）: 報告の本文に要約の行と、全点の表が出ること
            _CHJ = json.load(open(os.path.join(REPO, root, 'chart-B.json'), encoding='utf-8'))
            if rc_r == 0 and ('管理図の要約: 全点 %d・' % len(_CHJ.get('points') or [])) in _txt:
                fired['報告: 管理図の要約'].append(case)
            # **予想の照合の区画**（v6）: 二人の要約の行と、封印の順の注が本文に出ること
            if rc_r == 0 and all(('%s: 向き（' % w_) in _txt for w_ in ('登録者', 'コーディネータ')) and '予想の独立（封印の順の注）' in _txt:
                fired['報告: 予想の照合の区画'].append(case)
            # **門の記録の食い違いで止まる**（採否表 P403）: 集計が読んだ門とは別の門の記録を渡す
            _g2 = os.path.join(REPO, root, 'gate-B-other.json')
            _GJ = json.load(open(os.path.join(REPO, root, 'gate-B.json'), encoding='utf-8'))
            json.dump(dict(_GJ, note_dryrun='別の門の記録（検査用）'), open(_g2, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            _cmd2 = [x if x != os.path.join(root, 'gate-B.json') else os.path.join(root, 'gate-B-other.json') for x in _rep_cmd]
            _cmd2[_cmd2.index('--out') + 1] = os.path.join(root, 'report-B-other.md')
            rc_g2, out_g2 = run(_cmd2)
            if rc_g2 != 0 and '門の記録' in out_g2 and not os.path.exists(os.path.join(REPO, root, 'report-B-other.md')):
                fired['報告: 門の記録の食い違いで止まる'].append(case)
            shutil.rmtree(_keys, ignore_errors=True)
        for r in A['confirm']:
            lab = r.get('label')
            if lab in fired:
                fired[lab].append(case)
            rec['labels'][lab] = rec['labels'].get(lab, 0) + 1
            if any('注（様式' in n for n in (r.get('notes') or [])):
                fired['注（様式）'].append(case)
        v4 = A['s4'].get('verdict') or ''
        # **札は結果だけ**（裁定 D135）: 経路の名は正本の札から作る。門に当たった回は門で保留（裁定 D134）
        if A['s4'].get('gates'):
            fired['S4: 門で保留'].append('%s（%s）' % (case, v4))
        elif ('S4: %s' % v4) in fired:
            fired['S4: %s' % v4].append(case)
        elif '余地の条項' in v4:
            fired['S4: 余地の条項'].append('%s（%s）' % (case, v4))
        _sm = A['s4'].get('seal_match')
        if ('S4 の照合: %s' % _sm) in fired:
            fired['S4 の照合: %s' % _sm].append('%s（封印 %s・札 %s）' % (case, A['s4'].get('seal_value'), v4))
        if (A['sign_agreement'].get('agree') or 0) > 0:
            fired['封印した符号と一致'].append(case)
        rec['s4'] = A['s4'].get('verdict')
        rec['sign_agreement'] = A['sign_agreement']
    # **門1 が閉じた回の予想の照合**（v6）: 門の記録だけで照らし、向き・S4・本数は照合不能、門1 だけを照らす
    if (not G['gate1']['open']) and G['verdict'] != 'incomplete':
        rc_pc, out_pc = run(['tools/compare_predictions_B.py', '--gate', os.path.join(root, 'gate-B.json'), '--allow-dry',
                             '--out', os.path.join(root, 'predictions-check-B.md'), '--force'])
        _PCJ = os.path.join(REPO, root, 'predictions-check-B.json')
        _g1k = T['predictions']['fields']['gate1']['key']
        if rc_pc == 0 and os.path.exists(_PCJ):
            _pc = json.load(open(_PCJ, encoding='utf-8'))
            if all(all(r_['verdict'] in ('照合不能', '予想しない') for r_ in R_['rows'] if r_['key'] != _g1k)
                   and [r_['verdict'] for r_ in R_['rows'] if r_['key'] == _g1k] in (['的中'], ['外れ']) for R_ in _pc['results'].values()):
                fired['予想の照合: 門1 が閉じた回'].append(case)
        else:
            rec['compare_error'] = (out_pc or '')[-600:]
    # 合成データの中身から確かめる経路（採否表 P300〜P302）
    import glob as _g
    mainroot = os.path.join(REPO, root, T['tags']['main'])
    if os.path.isdir(mainroot):
        sess = {json.load(open(os.path.join(d, 'manifest.json'), encoding='utf-8')).get('session') for d in _g.glob(os.path.join(mainroot, '*'))}
        if len(sess) > 1:
            fired['中断と再開'].append(case)
        ff_cat = unmeas = 0
        for d in _g.glob(os.path.join(mainroot, '*')):
            for f in _g.glob(os.path.join(d, 'trials-*.jsonl')):
                for line in open(f, encoding='utf-8'):
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    if r.get('format_fail') and r.get('catastrophe'):
                        ff_cat += 1
                    if r.get('loop_flag') or r.get('truncated'):
                        unmeas += 1
        if unmeas:
            fired['未測定（ループ・打ち切り）'].append(case)
        if case == 'dilution_causal':
            # **恒真にしない**（裁定 D111・採否表 P310）。書式外の差・見かけの破局率の差・札の三つがそろって初めて発火。
            cc = runs_B.counts_main(T, root=root, allow_dry=True)[0]
            v, r = cc.get(('N1', 'Onull+v')), cc.get(('N1', 'Onull+vrand'))
            if v and r:
                ff_d = abs(100.0 * v['ff'] / v['n_ok'] - 100.0 * r['ff'] / r['n_ok'])
                cat_d = 100.0 * r['cat'] / r['n_ok'] - 100.0 * v['cat'] / v['n_ok']
                lab = [x.get('label') for x in (A.get('confirm') or []) if 'Onull+v~Onull+vrand' in str(x.get('id'))]
                if ff_d >= T['dilution_gate']['threshold_pt'] and cat_d > 0 and any('書式外転位' in str(x) for x in lab):
                    fired['希釈が効く場面（書式外が分子を食う）'].append(case)
        if ff_cat == 0:
            fired['採点の規約（書式外と refuse に判定を付けない）'].append(case)
    if os.path.isdir(os.path.join(REPO, root, T['tags']['identity'])):
        fired['同一性選別の走行'].append(case)
    rows.append(rec)

missing = [k for k, v in fired.items() if not v]
L = ['# 段階 B 器材の合成データによる検査（機械生成・`tools/dry_run_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 合成データは `results/_synth/<場合>/`（行にも置き場にも dry-run の印・公開の置き場には入れない）。',
     '- 正本 SHA16 %s。**発火しなかった経路 %d 件**。' % (runs_B.sha16_file(runs_B.CPATH), len(missing)), '',
     '| 経路 | 発火した場合 |', '|---|---|']
for k in PATHS:
    L.append('| %s | %s |' % (k, '・'.join(sorted(set(fired[k]))) or '**発火せず**'))
L += ['', '## 場合ごとの結果', '', '| 場合 | 門の判定 | 札の内訳 | S4 | 符号の一致 |', '|---|---|---|---|---|']
for r in rows:
    if r.get('report_error'):
        L.append('- **報告の組み立てが通らなかった**（%s）: %s' % (r['case'], r['report_error'].replace('\n', ' ')[:400]))
    if r.get('compare_error'):
        L.append('- **予想の照合が通らなかった**（%s）: %s' % (r['case'], r['compare_error'].replace('\n', ' ')[:400]))
for r in rows:
    L.append('| %s | %s | %s | %s | %s |' % (r['case'], r['gate_verdict'],
                                             '・'.join('%s %d' % (k, v) for k, v in sorted(r['labels'].items())) or '—',
                                             r.get('s4') or '—', r.get('sign_agreement') or '—'))
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
if not a.keep:
    shutil.rmtree(os.path.join(REPO, 'results', '_synth'), ignore_errors=True)
print('[dry_run_B] %s | 発火しなかった経路 %d' % (out_md, len(missing)))
if missing:
    print('  未発火: ' + '・'.join(missing))
sys.exit(1 if missing else 0)
