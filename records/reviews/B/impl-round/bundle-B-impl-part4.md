# 段階 B 器材の実装検分・資料の束 part4（機械生成・2026-09-18 03:43 UTC）

## tools/integrity_B.py（SHA16 6C55172320879D1B）

```python
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
    MF = T['runner'].get('manifest_fields') or {}
    need = list(MF.get('common', [])) + list(MF.get(PHASE, []))
    lack = [f for f in need if f not in m]
    if lack:
        problems.append('%s: manifest に欄が無い（正本 runner.manifest_fields・裁定 D89）: %s' % (rk, '・'.join(lack)))
    if m.get('batch') and m['batch'] != T['runner']['batch']:
        problems.append('%s: バッチ %s が設計定数（%s）と違う' % (rk, m['batch'], T['runner']['batch']))
    if m.get('padding') and m['padding'] not in ('left',):
        problems.append('%s: 詰めの向きが左でない（正本 runner.padding）: %s' % (rk, m['padding']))
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
```

## tools/sample_inspection_B.py（SHA16 7C51A9644E47DF78）

```python
# -*- coding: utf-8 -*-
"""sample_inspection_B.py v1 —— 段階 B の**抽出検査**（腕と場面を伏せた標本・目視の記録・対応表の封印）。段階 A の型。

何をするか:
  (1) 走行の記録から、セル（場面 × 腕）ごとに `--per-cell` 件を無作為に抜き、**腕と場面を伏せた標識**で並べた標本を書く（生本文の先頭 `--chars` 字）。
  (2) 対応表（標識 → trial_id・場面・腕・機械の分類）は**公開の置き場の外**（`--keydir`）に置き、その SHA-256 を標本の側に封印する。
  (3) 目視の後、`--agree` で目視の記録と対応表を突き合わせ、一致を記録する（対応表の SHA-256 が封印と違えば止まる）。
機械の分類（json_direct／prose）は標本に印字しない（目視の先入れを避ける）。**判定欄（破局・refuse）は標本にも対応表にも出さない。**
出力: records/B/sampling-inspection-B-<tag>-sample.txt と同 -seal.json（対応表の SHA-256 の封印・目視の前にコミットする）。
用法: python tools/sample_inspection_B.py --tag stageB --keydir <公開の外の置き場> [--per-cell 1] [--fraction 0.25] [--root ...] [--allow-dry]
      python tools/sample_inspection_B.py --tag stageB --keydir <同> --agree records/B/sampling-inspection-B-stageB-visual.json
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--tag', default=None)
ap.add_argument('--keydir', required=True, help='対応表の置き場（**公開の置き場の外**）')
ap.add_argument('--per-cell', type=int, default=1)
ap.add_argument('--fraction', type=float, default=0.25)
ap.add_argument('--chars', type=int, default=600)
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--seed', type=int, default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
ap.add_argument('--agree', default=None, help='目視の記録（json）を対応表と突き合わせる')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
tag = a.tag or T['tags']['main']
if os.path.abspath(a.keydir).startswith(os.path.abspath(REPO)):
    sys.exit('対応表の置き場が公開の置き場の中にある（外に置く・段階 A の key_rule と同じ縛り）: %s' % a.keydir)
os.makedirs(a.keydir, exist_ok=True)
key_path = os.path.join(a.keydir, 'sampling-key-B-%s.json' % tag)
out_txt = a.out or os.path.join(REPO, 'records', 'B', 'sampling-inspection-B-%s-sample.txt' % tag)
seal_path = os.path.splitext(out_txt)[0].replace('-sample', '') + '-seal.json'
sha256 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()

# ---- 突き合わせ（目視の後） ----
if a.agree:
    if not os.path.exists(key_path):
        sys.exit('対応表が無い: %s' % key_path)
    seal = runs_B.read_json(seal_path)
    if sha256(key_path) != seal['key_sha256']:
        sys.exit('対応表の SHA-256 が封印と違う（止まる）')
    KEY = runs_B.read_json(key_path)['items']
    VIS = runs_B.read_json(a.agree)['items']
    rows, agree = [], 0
    for v in VIS:
        k = next((x for x in KEY if x['label'] == v['label']), None)
        if k is None:
            sys.exit('封印に無い標識: %s' % v['label'])
        ok = (v.get('style_guess') == k['machine_style'])
        agree += ok
        rows.append({'label': v['label'], 'visual': v.get('style_guess'), 'machine': k['machine_style'], 'agree': ok,
                     'scenario': k['scenario'], 'arm': k['arm']})
    out = os.path.splitext(out_txt)[0].replace('-sample', '') + '-agreement.json'
    json.dump({'kind': 'sample_inspection_B_agreement', 'tag': tag, 'n': len(rows), 'agree': agree, 'items': rows},
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('[sample_inspection_B] 一致 %d/%d → %s' % (agree, len(rows), out))
    sys.exit(0)

# ---- 標本を作る ----
if not a.force:
    for p in (out_txt, seal_path, key_path):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)
idx = runs_B.index_runs(T, tag, a.root, allow_dry=a.allow_dry)
rng = np.random.default_rng(a.seed if a.seed is not None else T['seeds']['dryrun'])
cells = []
for k, recs in sorted(idx.items(), key=lambda kv: str(kv[0])):
    for rec in recs:
        raw = {}
        if rec['raw_path']:
            for r in runs_B.iter_jsonl(rec['raw_path']):
                raw[r.get('trial_id')] = r.get('text') or ''
        by_arm = {}
        for r in runs_B.iter_jsonl(rec['trials_path'], ('trial_id', 'arm', 'scenario', 'status', 'style_b')):
            if r['status'] == 'ok':
                by_arm.setdefault(r['arm'], []).append(r)
        for arm, rs in sorted(by_arm.items()):
            cells.append({'scenario': rs[0].get('scenario') or rec['manifest'].get('scenario'), 'arm': arm, 'rows': rs, 'raw': raw})
take = max(1, int(round(len(cells) * a.fraction)))
pick_cells = [cells[i] for i in sorted(rng.choice(len(cells), size=min(take, len(cells)), replace=False).tolist())]
items, sample_lines = [], []
for ci, c in enumerate(pick_cells):
    rs = c['rows']
    for j in rng.choice(len(rs), size=min(a.per_cell, len(rs)), replace=False).tolist():
        r = rs[j]
        label = 'X%03d' % (len(items) + 1)
        text = (c['raw'].get(r['trial_id']) or '')[:a.chars]
        items.append({'label': label, 'trial_id': r['trial_id'], 'scenario': c['scenario'], 'arm': c['arm'],
                      'machine_style': runs_B.stratum_of(r)})
        sample_lines += ['【%s】' % label, text, '']
json.dump({'kind': 'sampling_key_B', 'tag': tag, 'items': items}, open(key_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
now = datetime.datetime.now(datetime.timezone.utc)
json.dump({'kind': 'sample_inspection_B_seal', 'tag': tag, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'key_path_note': '対応表は公開の置き場の外に置いた（この記録には置き場の名を書かない）', 'key_sha256': sha256(key_path),
           'n_items': len(items), 'per_cell': a.per_cell, 'fraction': a.fraction, 'chars': a.chars,
           'seed': a.seed if a.seed is not None else T['seeds']['dryrun']},
          open(seal_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
head = ['# 段階 B 抽出検査の標本（腕と場面は伏せてある・機械の分類も伏せてある）',
        '# tag %s・%d 件・セルあたり %d 件・セルの割合 %g・先頭 %d 字' % (tag, len(items), a.per_cell, a.fraction, a.chars),
        '# 目視の記録は records/B/sampling-inspection-B-%s-visual.json に書き、--agree で対応表と突き合わせる。' % tag, '']
open(out_txt, 'w', encoding='utf-8', newline='\n').write('\n'.join(head + sample_lines))
print('[sample_inspection_B] %s（%d 件）／封印 %s' % (out_txt, len(items), seal_path))
```

## tools/synth_B.py（SHA16 4E4136F7EA24D891）

```python
# -*- coding: utf-8 -*-
"""synth_B.py v1 —— 段階 B の**合成データ**の生成器（器材の検査用・実データを作らない）。

札の全経路を一度ずつ以上発火させるための走行の記録を作る（器材の整備の計画 `records/B/tooling-plan-B-2026-09-18.md` の表）。
作るもの（既定の置き場は results/_synth/<場合>/）:
  本走行 `stageB`／調整走行 `tuneB`／品質床 `stageB-quality`／セッション記録 sessions-B。
件数は**乱数でなく決め打ち**（狙った札を確実に発火させるため）。すべての行に `dry_run: true` を立て、置き場に `_dryrun` を含める
（実データと取り違えないため。読む側は `--allow-dry` の検査用の口でしか読めない）。
用法: python tools/synth_B.py --case all --out-root results/_synth/all
      python tools/synth_B.py --list
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, shutil, argparse, datetime, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
SC = T['scenarios']
EX = T['extraction_scenarios']
N_MAIN, N_TUNE, N_Q = T['n_main'], T['n_tune'], T['quality_floor']['items']
LAYERS, COEFS = T['selection']['candidates']['layers'], T['selection']['candidates']['coefficients']
CANDS = [(l, c) for l in LAYERS for c in COEFS]
V_ARM, R_ARM = T['selection']['tune']['arms']
QF_ARMS = T['quality_floor']['arms']
QF_OPS = {'O-Ncold': '-v', 'Onull': '+v'}
INTERV = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
NOOP_BASE = {a: a.split('+v')[0].split('-v')[0] for a in INTERV}


def _trial(i, arm, scenario, tag, seed, run_key, cat, refuse, ff, style_a, style_b, mention, correct=None, layer=None, coef=None, status='ok', sampling=None):
    return {'trial_id': '%s__%s__%04d' % (run_key, arm, i), 'trial_index': i, 'arm': arm, 'scenario': scenario, 'tag': tag,
            'status': status, 'catastrophe': (None if status != 'ok' else bool(cat)), 'choice': ('refuse' if refuse else 'A'),
            'format_fail': bool(ff), 'style_a': bool(style_a), 'style_b': bool(style_b), 'mention': bool(mention),
            'loop_flag': False, 'truncated': False, 'correct': (None if correct is None else bool(correct)),
            'seed': seed, 'run_key': run_key, 'runner_sha': 'SYNTH', 'arms_spec': arm, 'preamble_sha': 'SYNTH',
            'model': 'stub/dry-run', 'sampling': dict(sampling or T['runner']['generation']), 'layer': layer, 'coef': coef,
            'direction_id': 'synth', 'batch_pos': i % T['runner']['batch'], 'proc_uuid': 'synth', 'dry_run': True}


def cell_trials(n, spec, **kw):
    """spec: 件数の割り当て（cat・refuse・ff・style_a・style_b・mention・correct・api_error）。残りは無印の試行。"""
    out = []
    n_err = int(spec.get('api_error', 0))
    for i in range(n):
        if i < n_err:
            out.append(_trial(i, status='error', cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, **kw))
            continue
        j = i - n_err
        out.append(_trial(i, cat=j < spec.get('cat', 0), refuse=spec.get('cat', 0) <= j < spec.get('cat', 0) + spec.get('refuse', 0),
                          ff=j < spec.get('ff', 0), style_a=j < spec.get('style_a', 0), style_b=j < spec.get('style_b', 0),
                          mention=j < spec.get('mention', 0), correct=(None if 'correct' not in spec else j < spec['correct']), **kw))
    return out


def write_run(root, tag, name, manifest, trials):
    d = os.path.join(root, tag, '%s__%s__dryrun' % (tag, name))
    os.makedirs(d, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    # 正本 runner.manifest_fields（裁定 D89）の欄をそろえる（整合検査がこの一覧を読む）
    common = {'tag': tag, 'run_key': os.path.basename(d), 'session': manifest.get('session', 1), 'n': manifest.get('n'),
              'seed': manifest.get('seed'), 'batch': T['runner']['batch'], 'padding': 'left', 'model': 'stub/dry-run',
              'model_rev': 'SYNTH', 'tokenizer_rev': 'SYNTH', 'runner_sha': 'SYNTH', 'pip_freeze_sha16': 'SYNTH',
              'gpu': 'synth', 'started': stamp, 'ended': stamp, 'dry_run': True}
    extra = {'direction_ids': ['synth'], 'arms': manifest.get('arms', []), 'task_source_sha16': 'SYNTH'}
    phase = next(k for k, v in T['tags'].items() if v == tag)
    need = list((T['runner'].get('manifest_fields') or {}).get(phase, []))
    manifest = dict({k: extra[k] for k in need if k in extra}, **dict(manifest, **common, generated=stamp))
    json.dump(manifest, open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(d, 'trials-synth.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for t in trials:
            f.write(json.dumps(t, ensure_ascii=False) + '\n')
    with open(os.path.join(d, 'raw-synth.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
        for t in trials:
            f.write(json.dumps({'trial_id': t['trial_id'], 'text': '（合成データ・本文は作らない）'}, ensure_ascii=False) + '\n')
    return d


# ---- 場合（case）ごとの仕様 ----
def base_main_spec():
    """本走行の既定: すべての腕で同じ率（札が立たない土台）。"""
    return {(sc, arm): {'cat': 60, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
            for sc in SC for arm in T['arms']['by_scenario'][sc]}


def case_all():
    """一つの走行で、確証・検閲・希釈（書式外・refuse）・refuse 門・様式門・品質床・非有意・逆向きを出す。"""
    m = base_main_spec()
    # 確証（N1 の減算族: A を大きく下げる・門には掛からない）
    m[('N1', 'O-Ncold-v')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('N1', 'O-Ncold-vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定不能（検閲・S1 の加算族: 両腕とも床）
    m[('S1', 'Onull+v')] = {'cat': 2, 'refuse': 4, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S1', 'Onull+vrand')] = {'cat': 4, 'refuse': 4, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（書式外転位・SK の減算族: A の書式外が門を超える）
    m[('SK', 'O-Ncold-v')] = {'cat': 30, 'refuse': 10, 'ff': 60, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('SK', 'O-Ncold-vrand')] = {'cat': 70, 'refuse': 10, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（refuse 転位・差・S4 の減算族）
    m[('S4', 'O-Ncold-v')] = {'cat': 30, 'refuse': 70, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'O-Ncold-vrand')] = {'cat': 70, 'refuse': 8, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（refuse 転位・答えた分母で有意を失う・N1 の加算族）
    m[('N1', 'Onull+v')] = {'cat': 44, 'refuse': 78, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('N1', 'Onull+vrand')] = {'cat': 70, 'refuse': 70, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定保留（様式転位・N1 の交差族 O-Ncold）
    m[('N1', 'O-Ncold+vNk')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 10, 'mention': 8}
    m[('N1', 'O-Ncold+vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 190, 'mention': 8}
    # 注（様式・S1 の交差族 O-Ncold: 確証だが様式の差が注の帯を超える）
    m[('S1', 'O-Ncold+vNk')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S1', 'O-Ncold+vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 160, 'mention': 8}
    # 判定保留（refuse 転位・答えた分母で名目有意を失う・SK の交差族 O-Ncold。refuse の差は門の内側に収める）
    m[('SK', 'O-Ncold+vNk')] = {'cat': 70, 'refuse': 28, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('SK', 'O-Ncold+vrand')] = {'cat': 92, 'refuse': 18, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # 判定不能（品質床・SK の交差族 Onull は品質床に落ちた腕を含む）
    m[('SK', 'Onull+vNk')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('SK', 'Onull+vrand')] = {'cat': 80, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8}
    # S4 の反証（下がった＝封印は外れ）
    m[('S4', 'Osec-Ncold+v6b')] = {'cat': 10, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'Osec-Ncold+vrand')] = {'cat': 60, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    tune = {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'tie': False, 'nonpositive': False, 'ff_fail': (LAYERS[0], COEFS[0]), 'censor_all': False}
    qual = {'fail_selection': [], 'fail_post': ['Onull+vNk']}
    return {'main': m, 'tune': tune, 'quality': qual, 'seal': {'sub:N1:O-Ncold-v~O-Ncold-vrand': '上'}}


def case_gate1_closed():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': 'all', 'fail_post': []}}


def case_nonpositive():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': None, 'eff': -3, 'nonpositive': True}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_tie():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'tie': True}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_censor_candidates():
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'censor_all': True}, 'quality': {'fail_selection': [], 'fail_post': []}}


CASES = {'all': case_all, 'gate1_closed': case_gate1_closed, 'nonpositive': case_nonpositive, 'tie': case_tie, 'censor_candidates': case_censor_candidates}


def build(case, out_root):
    spec = CASES[case]()
    if os.path.isdir(out_root):
        shutil.rmtree(out_root)
    os.makedirs(out_root, exist_ok=True)
    # ---- 本走行 ----
    for sc in SC:
        trials = []
        for arm in T['arms']['by_scenario'][sc]:
            s = spec['main'][(sc, arm)]
            trials += cell_trials(N_MAIN, s, arm=arm, scenario=sc, tag=T['tags']['main'], seed=T['seeds']['main'][sc],
                                  run_key='%s__%s__s1' % (T['tags']['main'], sc))
        _pick = spec['tune'].get('best') or (LAYERS[1], COEFS[1])
        write_run(out_root, T['tags']['main'], '%s__s1' % sc, {'scenario': sc, 'session': 1, 'n': N_MAIN, 'seed': T['seeds']['main'][sc],
                                                               'arms': T['arms']['by_scenario'][sc], 'batch': T['runner']['batch'],
                                                               'layer': _pick[0], 'coef': _pick[1]}, trials)
    # ---- 調整走行 ----
    tu = spec['tune']
    base_cat = 100                       # n_ok=200（抽出場面をまとめて）→ 一腕あたり 100 ずつ
    for sc in EX:
        for (l, c) in CANDS:
            is_best = (tu.get('best') == (l, c)) or (tu.get('tie') and (l, c) in (tu.get('best'), (LAYERS[1], COEFS[2])))
            eff = tu['eff'] if is_best else (tu['eff'] - 4 if not tu.get('nonpositive') else tu['eff'])
            cat_v = int(round(N_TUNE * (base_cat / 200.0 - eff / 200.0)))
            cat_r = int(round(N_TUNE * (base_cat / 200.0)))
            if tu.get('censor_all'):
                cat_v, cat_r = N_TUNE, N_TUNE      # 天井
            ff_v = 60 if tu.get('ff_fail') == (l, c) else 4
            for arm, cat, ff in ((V_ARM, cat_v, ff_v), (R_ARM, cat_r, 4)):
                trials = cell_trials(N_TUNE, {'cat': cat, 'refuse': 6, 'ff': ff, 'style_a': 20, 'style_b': 60, 'mention': 4},
                                     arm=arm, scenario=sc, tag=T['tags']['tune'], seed=T['seeds']['tune'][sc], layer=l, coef=c,
                                     run_key='%s__%s__L%sC%s' % (T['tags']['tune'], sc, l, c))
                write_run(out_root, T['tags']['tune'], '%s__L%sC%s__%s' % (sc, l, c, arm), {'scenario': sc, 'layer': l, 'coef': c, 'arm': arm,
                                                                                           'n': N_TUNE, 'seed': T['seeds']['tune'][sc]}, trials)
    # ---- 品質床 ----
    q = spec['quality']
    tag_q = T['tags']['quality']
    for base in QF_ARMS + ['O', 'Osec-Ncold']:
        trials = cell_trials(N_Q, {'correct': 150, 'ff': 2}, arm=base, scenario='quality', tag=tag_q, seed=T['seeds']['quality'], sampling=T['quality_floor']['generation'],
                             run_key='%s__noop__%s' % (tag_q, base))
        write_run(out_root, tag_q, 'selection__%s__noop' % base, {'stage': 'selection', 'arm': base, 'layer': None, 'coef': None, 'n': N_Q,
                                                                  'seed': T['seeds']['quality']}, trials)
    for base in QF_ARMS:
        arm = base + QF_OPS[base]
        for (l, c) in CANDS:
            bad = (q['fail_selection'] == 'all') or (arm in (q['fail_selection'] or []))
            trials = cell_trials(N_Q, {'correct': 100 if bad else 148, 'ff': 2}, arm=arm, scenario='quality', tag=tag_q, sampling=T['quality_floor']['generation'],
                                 seed=T['seeds']['quality'], layer=l, coef=c, run_key='%s__%s__L%sC%s' % (tag_q, arm, l, c))
            write_run(out_root, tag_q, 'selection__%s__L%sC%s' % (arm, l, c), {'stage': 'selection', 'arm': arm, 'layer': l, 'coef': c,
                                                                              'n': N_Q, 'seed': T['seeds']['quality']}, trials)
    pick = spec['tune'].get('best') or (LAYERS[1], COEFS[1])
    for arm in INTERV:
        bad = arm in (q['fail_post'] or [])
        trials = cell_trials(N_Q, {'correct': 100 if bad else 148, 'ff': 2}, arm=arm, scenario='quality', tag=tag_q, sampling=T['quality_floor']['generation'],
                             seed=T['seeds']['quality'], layer=pick[0], coef=pick[1], run_key='%s__post__%s' % (tag_q, arm))
        write_run(out_root, tag_q, 'post__%s' % arm, {'stage': 'post', 'arm': arm, 'layer': pick[0], 'coef': pick[1], 'n': N_Q,
                                                      'seed': T['seeds']['quality']}, trials)
    for base in sorted(set(NOOP_BASE.values())):
        trials = cell_trials(N_Q, {'correct': 150, 'ff': 2}, arm=base, scenario='quality', tag=tag_q, seed=T['seeds']['quality'], sampling=T['quality_floor']['generation'],
                             run_key='%s__post__noop__%s' % (tag_q, base))
        write_run(out_root, tag_q, 'post__%s__noop' % base, {'stage': 'post', 'arm': base, 'layer': None, 'coef': None, 'n': N_Q,
                                                             'seed': T['seeds']['quality']}, trials)
    # ---- セッション記録 ----
    sd = os.path.join(out_root, 'sessions-B')
    os.makedirs(sd, exist_ok=True)
    for sc in SC:
        json.dump({'tag': T['tags']['main'], 'session': 1, 'scenario': sc, 'gpu': 'synth', 'batch': T['runner']['batch'],
                   'run_keys': ['%s__%s__s1__dryrun' % (T['tags']['main'], sc)], 'dry_run': True},
                  open(os.path.join(sd, '%s__%s__s1.json' % (T['tags']['main'], sc)), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # ---- 封印（任意） ----
    if spec.get('seal'):
        json.dump({'kind': 'seal_B', 'signs': spec['seal'], 's4': 'synth', 'dry_run': True},
                  open(os.path.join(out_root, 'seal-B.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out_root


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--case', default='all', choices=sorted(CASES))
    ap.add_argument('--out-root', default=None)
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list:
        print('\n'.join(sorted(CASES)))
        sys.exit(0)
    root = a.out_root or os.path.join(REPO, 'results', '_synth', a.case)
    build(a.case, root)
    print('[synth_B] %s に合成データを書いた（場合 %s・すべて dry_run）' % (root, a.case))
```

## tools/dry_run_B.py（SHA16 E5014EBA7C4306AF）

```python
# -*- coding: utf-8 -*-
"""dry_run_B.py v1 —— 段階 B の器材の**合成データによる検査**（札の全経路を一度ずつ以上発火させる）。

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

VERSION = 'v1'
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

PATHS = ['確証', '確証（登録された向きと逆）', '判定不能（検閲）', '判定保留（書式外転位）', '判定保留（refuse 転位・差）',
         '判定保留（refuse 転位）', '判定保留（様式転位）', '注（様式）', '判定不能（品質床）', '非有意',
         '門1 を閉じる', '全候補が非正', '同点の割り方', '床・天井で選定から外す', 'S4 の三分岐']
fired = {k: [] for k in PATHS}
rows = []


def run(cmd):
    r = subprocess.run([PY] + cmd, capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


for case in ('all', 'gate1_closed', 'nonpositive', 'tie', 'censor_candidates'):
    root = os.path.join('results', '_synth', case)
    rc, out = run(['tools/synth_B.py', '--case', case, '--out-root', root])
    assert rc == 0, out
    rc_g, out_g = run(['tools/gate_B.py', '--root', root, '--allow-dry', '--out', os.path.join(root, 'gate-B.md'), '--force'])
    G = json.load(open(os.path.join(REPO, root, 'gate-B.json'), encoding='utf-8'))
    sel = G['selection']
    if not G['gate1']['open']:
        fired['門1 を閉じる'].append(case)
    if sel.get('nonpositive_stop'):
        fired['全候補が非正'].append(case)
    if sel.get('tie_note'):
        fired['同点の割り方'].append(case)
    if any(r.get('censored') for r in G['candidates']):
        fired['床・天井で選定から外す'].append(case)
    rec = {'case': case, 'gate_verdict': G['verdict'], 'gate_rc': rc_g, 'labels': {}}
    if G['gate1']['open']:
        seal = os.path.join(root, 'seal-B.json')
        cmd = ['tools/analyze_B.py', '--gate', os.path.join(root, 'gate-B.json'), '--root', root, '--allow-dry',
               '--out', os.path.join(root, 'analysis-B.md'), '--force']
        if os.path.exists(os.path.join(REPO, seal)):
            cmd += ['--seal', seal]
        rc_a, out_a = run(cmd)
        assert rc_a == 0, out_a
        A = json.load(open(os.path.join(REPO, root, 'analysis-B.json'), encoding='utf-8'))
        for r in A['confirm']:
            lab = r.get('label')
            if lab in fired:
                fired[lab].append(case)
            rec['labels'][lab] = rec['labels'].get(lab, 0) + 1
            if any('注（様式' in n for n in (r.get('notes') or [])):
                fired['注（様式）'].append(case)
        if A['s4'].get('verdict'):
            fired['S4 の三分岐'].append('%s（%s）' % (case, A['s4']['verdict']))
        rec['s4'] = A['s4'].get('verdict')
        rec['sign_agreement'] = A['sign_agreement']
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
```
