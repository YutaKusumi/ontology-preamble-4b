# -*- coding: utf-8 -*-
"""integrity_B.py v1 —— 段階 B の走行の**整合検査**（率盲検・許可表方式）。

**判定欄（catastrophe・choice・correct・style_a・style_b・mention）は読まない。** 許可した欄だけを取り出し、manifest と正本の登録に突き合わせる。
当てる相（採否表 P230・**本走行の後だけでなく、調整走行と品質床にも当てる**）:
  同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`
検査:
  行数と目標（腕 × n）・n_ok と api_error・書式外の件数（率ではない）・trial_id の重複と trial_index の欠落・腕ごとの n の揃い・
  runner_sha と arms_spec と preamble_sha（正本 `arms.sha16`）・model と seed の登録との一致・生成の設定（`runner.generation`／品質床は `quality_floor.generation`）・
  層と係数が候補の格子にあるか・方向の id の登録・**バッチの大きさの凍結**（`runner.fixed_across_runs`）・**詰めの向き**（`runner.padding`）・
  走行キーとセッション記録の対応（`sessions.missing_rule`）・dry-run の印。
出力: records/B/integrity-<tag>-<日付>.{md,json}（--force が無ければ上書きしない）。不整合があれば非零で終わる。
用法: python tools/integrity_B.py --tag stageB [--root results/_synth/all --allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
ALLOW = ('status', 'trial_id', 'trial_index', 'arm', 'scenario', 'tag', 'run_key', 'runner_sha', 'arms_spec', 'preamble_sha',
         'format_fail', 'seed', 'model', 'sampling', 'layer', 'coef', 'direction_id', 'batch_pos', 'dry_run', 'loop_flag', 'truncated')
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
        if len(rs) != n_exp:
            problems.append('%s × %s: 行数 %d（目標 %d）' % (rk, arm, len(rs), n_exp))
        if len(set(ids)) != len(ids):
            problems.append('%s × %s: trial_id が重複（%d 件）' % (rk, arm, len(ids) - len(set(ids))))
        if idx != list(range(len(rs))):
            problems.append('%s × %s: trial_index の欠落または重複' % (rk, arm))
        bad_sha = {r.get('preamble_sha') for r in rs}
        if PHASE in ('main', 'identity') and ARM_SHA.get(arm.split('+v')[0].split('-v')[0]) and len(bad_sha) != 1:
            problems.append('%s × %s: preamble_sha が一つでない' % (rk, arm))
        for r in rs:
            if r.get('seed') not in seeds_exp:
                problems.append('%s × %s: seed %s が登録（%s）と違う' % (rk, arm, r.get('seed'), sorted(seeds_exp)))
                break
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
    if m.get('batch') and m['batch'] != T['runner']['batch']:
        problems.append('%s: バッチ %s が設計定数（%s）と違う' % (rk, m['batch'], T['runner']['batch']))
    if PHASE in ('main', 'tune') and not m.get('padding') and 'padding' in T['runner']:
        notes.append('%s: manifest に詰めの向き（padding）が無い（正本 runner.padding の記帳を器材で入れる）' % rk)
    if PHASE == 'main' and rk not in sessions:
        problems.append('%s: セッション記録が無い（sessions.missing_rule）' % rk)
    if rec['dry_marks']:
        notes.append('%s: dry-run の印（%s）' % (rk, '・'.join(rec['dry_marks'])))


idx = runs_B.index_runs(T, a.tag, a.root, allow_dry=a.allow_dry)
for k, recs in sorted(idx.items(), key=lambda kv: str(kv[0])):
    for rec in recs:
        check_cell(rec)
if not idx:
    problems.append('走行の記録が一つも無い（tag %s）' % a.tag)

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
