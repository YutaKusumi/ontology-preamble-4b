# -*- coding: utf-8 -*-
"""integrity_B.py v3 —— 段階 B の走行の**整合検査**（率盲検・許可表方式）。

**判定欄（catastrophe・choice・correct・style_a・style_b・mention）は読まない。** 許可した欄だけを取り出し、manifest と正本の登録に突き合わせる。
当てる相（採否表 P230・**本走行の後だけでなく、調整走行と品質床にも当てる**）:
  同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`
検査:
  行数と目標（腕 × n）・n_ok と api_error・書式外の件数（率ではない）・trial_id の重複と trial_index の欠落・腕ごとの n の揃い・
  preamble_sha（正本 `arms.sha16`・manifest の runner_sha と model は走行を跨いだ同一性で見る）・**seed が正本の式で組み直した値と一致するか**（`seeds.derivation_formula`）・
  生成の設定（`runner.generation`／品質床は `quality_floor.generation`）・
  層と係数が候補の格子にあるか・**バッチの大きさの凍結**（`runner.fixed_across_runs`）・**詰めの向き**（`runner.padding`）・
  走行キーとセッション記録の対応（`sessions.missing_rule`）・dry-run の印。
出力: records/B/integrity-<tag>-<日付>.{md,json}（--force が無ければ上書きしない）。不整合があれば非零で終わる。
用法: python tools/integrity_B.py --tag stageB [--root results/_synth/all --allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v3'
REPO = runs_B.REPO
# 許可表は**正本から**作る（裁定 D97・器の中に手書きしない）
_T0 = runs_B.load_T()
ALLOW = tuple(runs_B.field_registry(_T0)['integrity_allow'])
BLIND = tuple(runs_B.field_registry(_T0)['blind'])
ap = argparse.ArgumentParser()
ap.add_argument('--tag', required=True)
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
TAGS = T['tags']
PHASE = next((k for k, v in TAGS.items() if v == a.tag), None)
if PHASE is None:
    sys.exit('tag %s の相が正本 tags に無い' % a.tag)
CAND = {(l, c) for l in T['selection']['candidates']['layers'] for c in T['selection']['candidates']['coefficients']}
ARM_SHA = T['arms']['sha16']
GEN_MAIN, GEN_Q = T['runner']['generation'], T['quality_floor']['generation']
problems, notes, cells = [], [], []
sessions = runs_B.sessions_by_run_key(runs_B.load_sessions(a.root))


def expect_n(phase, manifest):
    return {'identity': T['identity_screen']['n'], 'tune': T['n_tune'], 'quality': T['quality_floor']['items'], 'main': T['n_main']}[phase]


def expect_seed(phase, m):
    S = T['seeds']
    if phase == 'identity':
        return {S['identity_transformers']}
    if phase == 'tune':
        return {S['tune'].get(m.get('scenario'))}
    if phase == 'quality':
        return {S['quality']}
    return {S['main'].get(m.get('scenario'))}


def check_cell(rec):
    m, d = rec['manifest'], rec['dir']
    rk = rec['run_key']
    rows = list(runs_B.iter_jsonl(rec['trials_path'], ALLOW))
    by_arm = collections.defaultdict(list)
    for r in rows:
        by_arm[r['arm']].append(r)
    n_exp = expect_n(PHASE, m)
    seeds_exp = expect_seed(PHASE, m)
    gen_exp = GEN_Q if PHASE == 'quality' else GEN_MAIN
    for arm, rs in sorted(by_arm.items()):
        ids = [r['trial_id'] for r in rs]
        idx = sorted(r['trial_index'] for r in rs)
        n_ok = sum(1 for r in rs if r['status'] == 'ok')
        c = {'run_key': rk, 'arm': arm, 'n': len(rs), 'n_ok': n_ok, 'api_error': len(rs) - n_ok,
             'format_fail': sum(1 for r in rs if r.get('format_fail')), 'loop': sum(1 for r in rs if r.get('loop_flag')),
             'truncated': sum(1 for r in rs if r.get('truncated'))}
        cells.append(c)
        # 行数・番号・重複は**セル単位**で見る（中断と再開で走行が分かれるため・採否表 P264）。ここでは走行の中の重複だけを見る。
        if len(set(ids)) != len(ids):
            problems.append('%s × %s: 走行の中で trial_id が重複（%d 件）' % (rk, arm, len(ids) - len(set(ids))))
        if len(rs) > n_exp:
            problems.append('%s × %s: 行数 %d が目標 %d を超える' % (rk, arm, len(rs), n_exp))
        shas = {r.get('preamble_sha') for r in rs}
        base_arm = arm.split('+v')[0].split('-v')[0]
        want_sha = ARM_SHA.get(base_arm)
        if PHASE in ('main', 'identity', 'tune'):
            if len(shas) != 1:
                problems.append('%s × %s: preamble_sha が一つでない' % (rk, arm))
            elif want_sha and next(iter(shas)) != want_sha:
                problems.append('%s × %s: **preamble_sha が正本 arms.sha16 と違う**（%s 対 %s）' % (rk, arm, next(iter(shas)), want_sha))
        # 「書式外なのに正答」の検査は**ここには置けない**（裁定 D113・採否表 P314）。
        # 正答の欄は率盲検の欄なので、許可表で読む行では恒に空になり、この検査は決して発火しなかった。
        # 規約は採点器（steer_B.score_quality）が保証し、読み口が数えた件数を門と集計器が読んで止める。
        # **正本の式で組み直した値と突き合わせる**（正本 seeds.derivation_formula・裁定 D107・採否表 P310）。
        # 前は走行の種と直に比べていたので、実機が正本に従えば必ず落ちる状態だった。
        run_seed = next(iter(seeds_exp)) if len(seeds_exp) == 1 else m.get('seed')
        if run_seed is not None:
            if PHASE == 'quality':
                ckey = (m.get('stage') or ('post' if '__post__' in rk else 'selection'), arm, m.get('layer'), m.get('coef'))
            elif PHASE == 'tune':
                ckey = (m.get('scenario'), arm, m.get('layer'), m.get('coef'))
            else:
                ckey = (m.get('scenario'), arm)
            try:
                cs = runs_B.cell_seed(T, run_seed, PHASE, ckey)
            except SystemExit:
                cs = None
            if cs is not None:
                bad_seed = [r for r in rs if r.get('seed') != runs_B.trial_seed(cs, r.get('trial_index'))]
                if bad_seed:
                    problems.append('%s × %s: seed が正本の式で組み直した値と違う行が %d 件（先頭 trial_index %s・記録 %s・式 %s）'
                                    % (rk, arm, len(bad_seed), bad_seed[0].get('trial_index'), bad_seed[0].get('seed'),
                                       runs_B.trial_seed(cs, bad_seed[0].get('trial_index'))))
        for r in rs:
            if r.get('sampling') and {k: r['sampling'].get(k) for k in ('temperature', 'top_p')} != {k: gen_exp.get(k) for k in ('temperature', 'top_p')}:
                problems.append('%s × %s: 生成の設定が登録と違う（%s）' % (rk, arm, r.get('sampling')))
                break
        if PHASE in ('tune', 'quality'):
            lc = {(r.get('layer'), r.get('coef')) for r in rs}
            for l, cf in lc:
                if l is None and PHASE == 'quality':
                    continue
                if (l, cf) not in CAND:
                    problems.append('%s × %s: 層 × 係数 %s が候補の格子に無い' % (rk, arm, (l, cf)))
        if PHASE == 'main' and arm not in T['arms']['by_scenario'].get(m.get('scenario'), []):
            problems.append('%s: 腕 %s が場面 %s の登録に無い' % (rk, arm, m.get('scenario')))
    MF = T['runner'].get('manifest_fields') or {}
    need = list(MF.get('common', [])) + list(MF.get(PHASE, []))
    lack = [f for f in need if f not in m]
    if lack:
        problems.append('%s: manifest に欄が無い（正本 runner.manifest_fields・裁定 D89）: %s' % (rk, '・'.join(lack)))
    if m.get('batch') and m['batch'] != T['runner']['batch']:
        problems.append('%s: バッチ %s が設計定数（%s）と違う' % (rk, m['batch'], T['runner']['batch']))
    if m.get('padding') and m['padding'] not in ('left',):
        problems.append('%s: 詰めの向きが左でない（正本 runner.padding）: %s' % (rk, m['padding']))
    # **全相で確かめる**（裁定 D126・2026-09-18）。前は本走行の相にしか掛かっておらず、
    # 調整走行・品質床・同一性選別では記録を丸ごと消しても零件だった（系統外の検分で走らせて捕まった・採否表 P352）。
    if rk not in sessions:
        problems.append('%s: セッション記録が無い（正本 sessions.missing_rule・裁定 D126）' % rk)
    else:
        _s = sessions[rk][0] if isinstance(sessions[rk], list) else sessions[rk]
        if m.get('session') is not None and _s.get('session') is not None and m['session'] != _s['session']:
            problems.append('%s: manifest のセッション番号（%s）が記録（%s）と違う（裁定 D126）'
                            % (rk, m['session'], _s['session']))
    if rec['dry_marks']:
        notes.append('%s: dry-run の印（%s）' % (rk, '・'.join(rec['dry_marks'])))


idx = runs_B.index_runs(T, a.tag, a.root, allow_dry=a.allow_dry)
for k, recs in sorted(idx.items(), key=lambda kv: str(kv[0])):
    for rec in recs:
        check_cell(rec)
if not idx:
    problems.append('走行の記録が一つも無い（tag %s）' % a.tag)

# ---- セル単位の検査（中断と再開・採否表 P264）: 走行を跨いで trial_id の重複と欠落を見る ----
cells_by_key = {}
for k, recs in idx.items():
    for rec in recs:
        m = rec['manifest']
        for r in runs_B.iter_jsonl(rec['trials_path'], ALLOW):
            # セルの単位は相ごとに違う（本走行は 場面 × 腕・調整走行は 場面 × 層 × 係数 × 腕・品質床は 段 × 腕 × 層 × 係数 × セッション・選別は スタック × 腕）
            if PHASE == 'main':
                key = (r.get('scenario') or m.get('scenario'), r['arm'])
            elif PHASE == 'tune':
                key = (m.get('scenario'), m.get('layer'), m.get('coef'), r['arm'])
            elif PHASE == 'quality':
                key = (m.get('stage'), r['arm'], m.get('layer'), m.get('coef'), m.get('session'))
            else:
                key = (m.get('stack'), m.get('scenario'), r['arm'])
            c = cells_by_key.setdefault(key, {'ids': [], 'idx': [], 'runs': set(), 'n_ok': 0, 'gap': 0, 'cff': 0})
            c['ids'].append(r['trial_id'])
            c['idx'].append(r['trial_index'])
            c['runs'].add(rec['run_key'])
            if r['status'] == 'ok':
                c['n_ok'] += 1
n_exp_cell = expect_n(PHASE, {})
for key, c in sorted(cells_by_key.items(), key=str):
    if len(set(c['ids'])) != len(c['ids']):
        problems.append('%s × %s: **走行を跨いで trial_id が重複**（%d 件・再開の重複を見落とさない）' % (key[0], key[1], len(c['ids']) - len(set(c['ids']))))
    if sorted(c['idx']) != list(range(n_exp_cell)):
        problems.append('%s × %s: セルの試行の番号が %d 件で連番でない（目標 %d・走行 %s）'
                        % (key[0], key[1], len(c['idx']), n_exp_cell, '・'.join(sorted(c['runs']))))
    if c['n_ok'] == 0:
        problems.append('%s × %s: **n_ok が零**（測れなかったセル・裁定 D96）' % (key[0], key[1]))

# ---- 判定欄を読まないことの自己検査（率盲検・裁定 D97） ----
if set(ALLOW) & set(BLIND):
    problems.append('許可表に判定欄が混ざっている: %s' % '・'.join(sorted(set(ALLOW) & set(BLIND))))

# ---- 走行を跨いだ同一性（runner.fixed_across_runs・採否表 P274） ----
# **manifest に実在する欄で見る**（裁定 D126・2026-09-18）。`versions` はセッション記録の欄であって
# manifest には無いので、この検査は**常に飛んでいた**（系統外の検分で捕まった・採否表 P363）。
# あわせて、値が空のときも黙って飛ばさず不整合に数える。
FIX_KEYS = {'重みの rev': 'model_rev', 'tokenizer の版': 'tokenizer_rev', 'バッチの大きさ': 'batch',
            '詰めの向き': 'padding', '走行器の SHA': 'runner_sha', '環境の SHA': 'pip_freeze_sha16'}
seen = {}
for k, recs in idx.items():
    for rec in recs:
        for name, mk in FIX_KEYS.items():
            v = rec['manifest'].get(mk)
            if v is None:
                problems.append('%s: 走行を跨いで同一であるべき欄が manifest に無い（%s・正本 runner.fixed_across_runs・裁定 D126）'
                                % (rec['run_key'], mk))
                continue
            seen.setdefault(name, {}).setdefault(json.dumps(v, ensure_ascii=False, sort_keys=True), []).append(rec['run_key'])
for name, vals in seen.items():
    if len(vals) > 1:
        problems.append('**走行を跨いで %s が同じでない**（%s・正本 runner.fixed_rule）' % (name, '／'.join('%s: %d 走行' % (v[:24], len(rs)) for v, rs in vals.items())))

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'integrity-%s-%s.md' % (a.tag, jst.strftime('%Y-%m-%d')))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)
REC = {'kind': 'integrity_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'tag': a.tag, 'phase': PHASE,
       'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'cells': cells, 'problems': problems, 'notes': notes,
       'allow_fields': list(ALLOW)}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 整合検査（機械生成・`tools/integrity_B.py` %s・%s UTC・tag %s・相 %s）' % (VERSION, now.strftime('%Y-%m-%d %H:%M'), a.tag, PHASE), '',
     '- 正本 SHA16 %s。セル %d。**不整合 %d 件**・注 %d 件。' % (REC['contrasts_sha16'], len(cells), len(problems), len(notes)),
     '- 読んだ欄（判定欄は読まない）: %s' % '・'.join(ALLOW), '']
if problems:
    L += ['## 不整合', ''] + ['- ' + p for p in problems] + ['']
if notes:
    L += ['## 注', ''] + ['- ' + n for n in notes] + ['']
L += ['## セル', '', '| 走行キー | 腕 | 行 | n_ok | api_error | 書式外 |', '|---|---|---|---|---|---|']
for c in cells:
    L.append('| %s | %s | %d | %d | %d | %d |' % (c['run_key'], c['arm'], c['n'], c['n_ok'], c['api_error'], c['format_fail']))
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[integrity_B] %s | 不整合 %d・注 %d・セル %d' % (out_md, len(problems), len(notes), len(cells)))
sys.exit(1 if problems else 0)
