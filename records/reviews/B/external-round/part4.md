# 器材のソース（逐語）（機械生成・2026-09-18 08:15 UTC）

## `tools/integrity_B.py`（SHA16 E9AFB7298A18677E・225 行）

```python
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
FIX_KEYS = {'重みの rev': 'model_rev', 'tokenizer の版': 'tokenizer_rev', 'transformers の版': 'versions', 'バッチの大きさと並べ方': 'batch'}
seen = {}
for k, recs in idx.items():
    for rec in recs:
        for name, mk in FIX_KEYS.items():
            v = rec['manifest'].get(mk)
            if v is None:
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
```

## `tools/sample_inspection_B.py`（SHA16 80F7FC16F04E514C・142 行）

```python
# -*- coding: utf-8 -*-
"""sample_inspection_B.py v2 —— 段階 B の**抽出検査**（腕と場面を伏せた標本・目視の記録・対応表の封印）。段階 A の型。

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

VERSION = 'v2'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--tag', default=None)
ap.add_argument('--selftest', action='store_true')
ap.add_argument('--keydir', default=None, help='対応表の置き場（**公開の置き場の外**）')
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
if not a.selftest and not a.keydir:
    sys.exit('--keydir（公開の置き場の外）が要る')
tag = a.tag or T['tags']['main']
def _inside_repo(kd):
    """置き場が公開の置き場の中かを、**大文字小文字と接合点を畳んで**見る（実装検分の採否表 P281）。"""
    k, r = os.path.normcase(os.path.realpath(kd)), os.path.normcase(os.path.realpath(REPO))
    try:
        return k == r or os.path.commonpath([k, r]) == r
    except ValueError:
        return False


if not a.selftest and _inside_repo(a.keydir):
    sys.exit('対応表の置き場が公開の置き場の中にある（外に置く・段階 A の key_rule と同じ縛り）: %s' % a.keydir)
if a.keydir:
    os.makedirs(a.keydir, exist_ok=True)
key_path = os.path.join(a.keydir, 'sampling-key-B-%s.json' % tag) if a.keydir else None
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

if a.selftest:
    # 置き場の判定（大文字小文字・接合点）と、標識の並べ替えの確かめ
    assert _inside_repo(os.path.join(REPO, 'keys')), '公開の置き場の中を外と判定した'
    assert _inside_repo(os.path.join(REPO, 'keys').lower()), '小文字の置き場を外と判定した（採否表 P281）'
    assert not _inside_repo(REPO + '-keys'), '外の兄弟を中と判定した'
    r_ = np.random.default_rng(T['seeds']['sample_inspection'])
    perm = r_.permutation(20).tolist()
    assert perm != sorted(perm), '並べ替えが恒等になっている'
    print('[sample_inspection_B selftest] 置き場の判定（大文字小文字・兄弟）・標識の並べ替え: すべて通った')
    sys.exit(0)

# ---- 標本を作る ----
if not a.force:
    for p in (out_txt, seal_path, key_path):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)
idx = runs_B.index_runs(T, tag, a.root, allow_dry=a.allow_dry)
rng = np.random.default_rng(a.seed if a.seed is not None else T['seeds']['sample_inspection'])
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
picked = []
for c in pick_cells:
    rs = c['rows']
    for j in rng.choice(len(rs), size=min(a.per_cell, len(rs)), replace=False).tolist():
        r = rs[j]
        picked.append({'trial_id': r['trial_id'], 'scenario': c['scenario'], 'arm': c['arm'],
                       'machine_style': runs_B.stratum_of(r), 'text': (c['raw'].get(r['trial_id']) or '')[:a.chars]})
# **並べ替えてから**標識を振る（整列順のままだと腕と場面が読める・段階 A の登録者裁定 D25・実装検分の採否表 P280）
order = rng.permutation(len(picked)).tolist()
items, sample_lines = [], []
for n_, i_ in enumerate(order, 1):
    x = picked[i_]
    label = 'X%03d' % n_
    items.append({'label': label, 'trial_id': x['trial_id'], 'scenario': x['scenario'], 'arm': x['arm'],
                  'machine_style': x['machine_style']})
    sample_lines += ['【%s】' % label, x['text'], '']
json.dump({'kind': 'sampling_key_B', 'tag': tag, 'items': items}, open(key_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
now = datetime.datetime.now(datetime.timezone.utc)
json.dump({'kind': 'sample_inspection_B_seal', 'tag': tag, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'key_path_note': '対応表は公開の置き場の外に置いた（この記録には置き場の名を書かない）', 'key_sha256': sha256(key_path),
           'n_items': len(items), 'per_cell': a.per_cell, 'fraction': a.fraction, 'chars': a.chars,
           'seed': a.seed if a.seed is not None else T['seeds']['sample_inspection'], 'shuffled': True},
          open(seal_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
head = ['# 段階 B 抽出検査の標本（腕と場面は伏せてある・機械の分類も伏せてある）',
        '# tag %s・%d 件・セルあたり %d 件・セルの割合 %g・先頭 %d 字' % (tag, len(items), a.per_cell, a.fraction, a.chars),
        '# 目視の記録は records/B/sampling-inspection-B-%s-visual.json に書き、--agree で対応表と突き合わせる。' % tag, '']
open(out_txt, 'w', encoding='utf-8', newline='\n').write('\n'.join(head + sample_lines))
print('[sample_inspection_B] %s（%d 件）／封印 %s' % (out_txt, len(items), seal_path))
```

## `tools/direction_B.py`（SHA16 316030741B597B56・214 行）

```python
# -*- coding: utf-8 -*-
"""direction_B.py v4 —— 段階 B の**方向の抽出**（主位置の活性・方向の作成・決定性の検査・要約統計・v̂ の凍結）。

正本 `design/contrasts-B.json` の `selection.position`・`selection.candidates`・`directions`・`activation_storage`・`runner` に従う。
何をするか:
  (1) 腕 × 場面のプロンプトを組み、**プロンプトの最終トークン**（詰めでない最後の位置・`runner.padding`）の隠れ状態を、登録した層で取り出す。
  (2) 決定性の検査は二条（裁定 D91）: **同じ並べ方**で二度取って完全一致（外れたら走行を止める）／**並べ方を変えて**一度取り、許容差の内側かを見る（外れたら記帳して登録者に上げる）。
  (3) 方向を作る: (6a) 静的 h_O − h_Osec／(6b) 負荷下 h_{O-Ncold} − h_{Osec-Ncold}／Nk 方向 h_Nk − h_N／腕対の差方向 h_Onull − h_N。
      いずれも**抽出場面の平均**。td は v̂ のノルムに合わせる（`directions.td`）。
  (4) 要約統計: 層ごとのノルム・方向どうしのコサイン・**平均を取る前の場面ごとの差ベクトルどうしのコサイン**（抽出場面の間の安定性・採否表 P237）。
  (5) v̂ を凍結して保存し、SHA を記帳する（`selection.vector_fix`）。
層番号は `selection.candidates.layer_index_rule`（割合 × 総層数を四捨五入して一つ引く・総層数は config から読んで記帳）。
**この器は GPU の上でしか本走行できない。** 手元では `--selftest`（合成のベクトルで規則だけを確かめる）が走る。
用法: python tools/direction_B.py --model Qwen/Qwen3-4B-Instruct-2507 --out results/dirB [--dtype bfloat16]
      python tools/direction_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v4'
REPO = runs_B.REPO
T = runs_B.load_T()
PANEL = T['arms']['panel']
EX = T['extraction_scenarios']
LAYER_RATIOS = T['selection']['candidates']['layers']
DIRS = T['directions']


def layer_index(ratio, n_layers):
    """層の割合 → 層の添字（正本 `selection.candidates.layer_index_rule`・零始まり）。

    **四捨五入**（Python の `round` は偶数丸めなので使わない・実装検分の採否表 P283）。"""
    idx = int(math.floor(ratio * n_layers + 0.5)) - 1
    assert 0 <= idx < n_layers, ('層の添字が範囲の外', ratio, n_layers, idx)
    return idx


def hidden_states_index(layer_idx):
    """`hidden_states` の添字（埋め込みの分だけ一つずれる・正本の「層の添字」とは別物）。"""
    return layer_idx + 1


def write_layer_record(out_dir, n_layers):
    """総層数と層の添字を**記帳**する（正本 `layer_index_rule` が求める・採否表 P283）。"""
    rec = {'num_hidden_layers': n_layers, 'ratios': LAYER_RATIOS,
           'layer_indices': {str(r): layer_index(r, n_layers) for r in LAYER_RATIOS},
           'hidden_states_indices': {str(r): hidden_states_index(layer_index(r, n_layers)) for r in LAYER_RATIOS}}
    os.makedirs(out_dir, exist_ok=True)
    json.dump(rec, open(os.path.join(out_dir, 'layers.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return rec


def unit(v):
    n = float(np.linalg.norm(v))
    return v / n if n else v


def match_norm(v, ref):
    """v の向きのまま、ノルムを ref のノルムに合わせる（裁定 D75 の基準は v̂）。"""
    nv, nr = float(np.linalg.norm(v)), float(np.linalg.norm(ref))
    return v * (nr / nv) if nv else v


def cosine(a, b):
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    return float(np.dot(a, b) / (na * nb)) if na and nb else None


def build_directions(H):
    """H[(arm, scenario, layer_ratio)] = 活性ベクトル → 方向と要約統計。

    方向は抽出場面の平均。td は v̂ のノルムに合わせる。安定性は「平均を取る前の場面ごとの差ベクトルどうしのコサイン」。"""
    out, stats = {}, {}
    pairs = {'static': ('O', 'Osec'), 'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}
    for ratio in LAYER_RATIOS:
        per = {}
        for name, (a1, a2) in pairs.items():
            diffs = {sc: H[(a1, sc, ratio)] - H[(a2, sc, ratio)] for sc in EX}
            per[name] = {'mean': np.mean([diffs[sc] for sc in EX], axis=0), 'by_scenario': diffs}
        v_hat = per['static']['mean']
        raw_ratio = {}
        for name in pairs:
            v = per[name]['mean']
            raw_ratio[name] = (float(np.linalg.norm(v)) / float(np.linalg.norm(v_hat))) if np.linalg.norm(v_hat) else None
            if name != 'static':
                v = match_norm(v, v_hat)      # **全方向を ‖v̂〔static〕‖ に合わせる**（裁定 D102・採否表 P306・P310）
            out[(name, ratio)] = v
        stats[ratio] = {
            'norms': {name: float(np.linalg.norm(out[(name, ratio)])) for name in pairs},
            'raw_norm_ratio': raw_ratio,          # **合わせる前の比**（正本 coefficient_ref・採否表 P284 の後半）
            'cosines': {'%s~%s' % (x, y): cosine(out[(x, ratio)], out[(y, ratio)])
                        for i, x in enumerate(sorted(pairs)) for y in sorted(pairs)[i + 1:]},
            'stability': {name: {'cos_%s_%s' % (EX[0], EX[1]): cosine(per[name]['by_scenario'][EX[0]], per[name]['by_scenario'][EX[1]]),
                                 'norm_ratio': (float(np.linalg.norm(per[name]['by_scenario'][EX[0]])) /
                                                float(np.linalg.norm(per[name]['by_scenario'][EX[1]])) if np.linalg.norm(per[name]['by_scenario'][EX[1]]) else None)}
                          for name in pairs}}
    return out, stats


def determinism_same_order(h1, h2):
    """**同じ並べ方**で二度取った活性の完全一致（bitwise）を見る（裁定 D91 の (i)）。一致しなければ走行を止める。"""
    if set(h1) != set(h2):
        return False, ['鍵の集合が違う: %s' % sorted(set(h1) ^ set(h2))[:4]]
    bad = []
    for k in h1:
        a, b = np.asarray(h1[k]), np.asarray(h2[k])
        if np.isnan(a).any() or np.isnan(b).any():
            bad.append('%s: NaN を含む' % (k,))
        elif not np.array_equal(a, b):
            bad.append('%s: 一致しない' % (k,))
    return (not bad), bad


def determinism_cross_order(h1, h2, tol=None):
    """**並べ方を変えて**取った活性が許容差の内側かを見る（裁定 D91 の (ii)）。外れたら記帳して登録者に上げる（止めない）。"""
    tol = tol or T['activation_storage']['determinism']['cross_order_tolerance']
    rows = []
    if set(h1) != set(h2):      # **鍵の欠けを黙って無視しない**（裁定 D114・採否表 P318）
        rows.append({'key': '（鍵の集合）', 'ok': False,
                     'note': '鍵の集合が違う: %s' % sorted(set(h1) ^ set(h2), key=str)[:4]})
    for k in sorted(set(h1) & set(h2), key=str):
        a, b = np.asarray(h1[k], dtype=float), np.asarray(h2[k], dtype=float)
        na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
        cos = float(np.dot(a, b) / (na * nb)) if na and nb else None
        rel = float(np.max(np.abs(a - b)) / na) if na else None
        ok = (cos is not None and cos >= tol['cos_min']) and (rel is not None and rel <= tol['max_abs_over_norm'])
        rows.append({'key': str(k), 'cos': cos, 'max_abs_over_norm': rel, 'ok': ok})
    return all(r['ok'] for r in rows), rows


def _selftest():
    rng = np.random.default_rng(7)
    d = 16
    # 層番号は**手で書いた期待値の表**と突き合わせる（実装式で確かめない・採否表 P283）
    want = {(0.25, 36): 8, (0.5, 36): 17, (0.75, 36): 26, (0.25, 34): 8, (0.5, 34): 16, (0.75, 34): 25,
            (0.25, 42): 10, (0.5, 42): 20, (0.75, 42): 31}
    for (ratio, n), idx in want.items():
        assert layer_index(ratio, n) == idx, ('層番号が期待値と違う', ratio, n, layer_index(ratio, n), idx)
    assert hidden_states_index(layer_index(0.5, 36)) == 18, 'hidden_states の添字の変換が違う'
    H = {}
    for arm in PANEL:
        for sc in EX:
            for ratio in LAYER_RATIOS:
                H[(arm, sc, ratio)] = rng.normal(size=d)
    dirs, stats = build_directions(H)
    v = dirs[('static', LAYER_RATIOS[0])]
    td = dirs[('td', LAYER_RATIOS[0])]
    assert abs(np.linalg.norm(td) - np.linalg.norm(v)) < 1e-9, 'td のノルムが v̂ に合っていない'
    assert set(stats[LAYER_RATIOS[0]]['stability']) == {'static', 'loaded', 'Nk', 'td'}
    # 決定性 (i) 同じ並べ方 → 完全一致
    ok, bad = determinism_same_order(H, dict(H))
    assert ok and not bad
    H2 = dict(H)
    k0 = next(iter(H2))
    H2[k0] = H2[k0] + 1e-9
    ok2, bad2 = determinism_same_order(H, H2)
    assert not ok2 and len(bad2) == 1, '決定性の検査が差を見落とす'
    H3 = dict(H)
    H3.pop(k0)
    ok3, bad3 = determinism_same_order(H, H3)
    assert not ok3 and '鍵の集合' in bad3[0], '鍵の欠けを見落とす'
    H4 = dict(H)
    H4[k0] = H4[k0] * np.nan
    ok4, bad4 = determinism_same_order(H, H4)
    assert not ok4 and 'NaN' in bad4[0], 'NaN を別の名で報告していない'
    # 決定性 (ii) 並べ方を変えた → 許容差
    tol = T['activation_storage']['determinism']['cross_order_tolerance']
    Hs = {k: vv + rng.normal(size=d) * 1e-6 for k, vv in H.items()}
    ok5, rows5 = determinism_cross_order(H, Hs)
    assert ok5, ('わずかな差が許容差を外れた', rows5[:1])
    Hb = {k: vv + rng.normal(size=d) * 1.0 for k, vv in H.items()}
    ok6, rows6 = determinism_cross_order(H, Hb)
    assert not ok6, '大きな差を許容差の内側と判定した'
    print('[direction_B selftest] 層番号（期待値の表・%d 通り）・hidden_states の添字・ノルム合わせ・安定性・'
          '決定性の二条（同じ並べ方は完全一致／並べ方を変えたら cos %g・相対差 %g）: すべて通った'
          % (len(want), tol['cos_min'], tol['max_abs_over_norm']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
    ap.add_argument('--dtype', default='bfloat16')
    ap.add_argument('--out', default=None)
    ap.add_argument('--arms-dir', default=os.path.join(REPO, 'arms'))
    ap.add_argument('--scenarios-dir', default=None, help='場面の本文の置き場（凍結盤の素材）')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as e:                                    # 手元では届かない（Colab の段で走らせる）
        sys.exit('torch／transformers が無い: %s（この器は GPU の上で走らせる。手元の検査は --selftest）' % e)
    out_dir = a.out or os.path.join(REPO, 'results', 'dirB')
    os.makedirs(out_dir, exist_ok=True)
    # 置き場を直に渡せるようにする（版を固定し、Hub への問い合わせを避ける・裁定 D115・採否表 P328）
    tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or a.model)
    tok.padding_side = 'left'                                  # 正本 runner.padding
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=getattr(torch, a.dtype), device_map='auto')
    model.eval()
    n_layers = model.config.num_hidden_layers
    idxs = {r: layer_index(r, n_layers) for r in LAYER_RATIOS}

    def prompts_for(arm, sc):
        raise SystemExit('場面と腕の本文の組み方は器材の段で確定する（--scenarios-dir の凍結素材から組む）。'
                         'この版は骨組みで、実際の組み立ては凍結の前に埋める（正本 quality_floor.input と同じ扱い）。')

    print('[direction_B] 総層数 %d・層の添字 %s（正本の割合 %s）' % (n_layers, idxs, LAYER_RATIOS))
    print('[direction_B] 本文の組み立てはまだ埋めていない（凍結の前に確定する）。--selftest で規則だけ確かめられる。')
```

## `tools/steer_B.py`（SHA16 01F78C860C2FCF15・246 行）

```python
# -*- coding: utf-8 -*-
"""steer_B.py v3 —— 段階 B の**介入**（方向の加減・ランダム方向・品質床・強制デコード）。

正本 `design/contrasts-B.json` の `selection.apply`・`random_control`・`quality_floor`・`runner` に従う。
規則（この器が守るもの）:
  - 加減は `h ← h ± α·v̂`（場面本文の開始位置から EOS まで・`register_forward_hook`・`selection.apply`）。α は**その層の v̂ のノルムに対する比**。
  - すべての方向（v̂・Nk・td・(6b)・ランダム方向）を**係数を掛ける前の ‖v̂〔static〕‖** に合わせ、**係数は加減のときに一度だけ**掛ける（裁定 D75・D90）。
    自己検査は「**全方向 × 全係数 × 全層**で加わる量のノルムが一致する」ことを確かめる（裁定 D102——前は v 腕とランダム腕の対しか回さず、交差族に同じ穴が残った）。
  - 介入の帯の起点は、**chat template を当てた列の中で場面の本文が始まる位置**（裁定 D101）。自己検査は起点のトークンを復号して場面本文の先頭と照合する
    （`OP4B_TOKENIZER_DIR` に実トークナイザの置き場を渡したときに走る）。
  - ランダム方向は**調整走行と本走行で引き直す**（裁定 D84・種は `seeds.random_dirs` の tune と main）。
  - 一腕の試行は方向の登録順に等分し、端数は登録順に一つずつ配る（`random_control.allocation`・調整走行にも当てる）。
  - 品質床は**貪欲**（`quality_floor.generation`）。書式外は不正解に数え、api_error は一度だけ引き直す（`quality_floor.format_fail_rule`）。
  - 場面の試行は `runner.generation` の設定。詰めは左（`runner.padding`）。
**この器は GPU の上でしか本走行できない。** 手元では `--selftest`（ノルム合わせ・割り当て・引き直し・種の再現を合成のベクトルで確かめる）が走る。
用法: python tools/steer_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v3'
REPO = runs_B.REPO
T = runs_B.load_T()
RC = T['random_control']
N_RAND = RC['count']


def random_directions(v_hat_static, phase, layer_ratio, count=N_RAND):
    """層ごとに count 本のランダム方向を引き、**係数を掛ける前の ‖v̂〔static〕‖** に合わせる（裁定 D90・2026-09-18）。

    係数は加減のときに一度だけ掛ける（`apply_vector`・`selection.apply`）。基準は**静的 v̂ ひとつ**で、族を跨いで変えない（裁定 D75）。
    phase は 'tune' か 'main'（裁定 D84・種を分けて引き直す）。子ストリームは**層ごと**（正本 `random_control.per_layer`・係数は入れない・採否表 P285）。"""
    assert phase in ('tune', 'main'), '相は tune か main（裁定 D84）'
    seed = RC['seed'][phase]
    d = int(np.asarray(v_hat_static).shape[-1])
    ss = np.random.SeedSequence([seed, int(round(layer_ratio * 1000))])
    rng = np.random.default_rng(ss)
    target = float(np.linalg.norm(v_hat_static))
    out = []
    for i in range(count):
        g = rng.normal(size=d)
        n = float(np.linalg.norm(g))
        out.append(g * (target / n) if n else g)
    return out


def match_to_static(v, v_hat_static):
    """どの方向（Nk・td・(6b)）も、加える前に ‖v̂〔static〕‖ に合わせる（裁定 D75・D90）。"""
    n = float(np.linalg.norm(v))
    return v * (float(np.linalg.norm(v_hat_static)) / n) if n else v


def allocate(n_trials, count=N_RAND):
    """一腕の試行を方向の登録順に等分し、端数は登録順に一つずつ配る（random_control.allocation）。"""
    base, rem = divmod(int(n_trials), int(count))
    return [base + (1 if i < rem else 0) for i in range(count)]


def direction_of(trial_index, n_trials, count=N_RAND):
    """試行の番号から方向の添字を決める（**再開しても変わらない**・採否表 P298）。

    残り件数から割り直すと等分にならないので、常に全体の割り当てを基準にする。"""
    al = allocate(n_trials, count)
    acc = 0
    for i, n in enumerate(al):
        acc += n
        if trial_index < acc:
            return i
    raise ValueError('試行の番号が全体の数を超えている: %s / %s' % (trial_index, n_trials))


def apply_vector(h, v_hat, coef, sign):
    """h ← h ± α·v̂（α は v̂ のノルムに対する比なので、掛けるのは coef·v̂）。"""
    assert sign in (+1, -1)
    return h + sign * coef * np.asarray(v_hat)


def apply_chat(tokenizer, user_message):
    """**段階 B は chat template を当てる**（正本 `runner.chat_template`・裁定 D101）。組み立て済みのトークン列を返す。"""
    return list(tokenizer.apply_chat_template([{'role': 'user', 'content': user_message}],
                                              add_generation_prompt=True, tokenize=True))


def scenario_start_index(tokenizer, arm_text, scen_text, instruction, pad_len=0, probe=8):
    """介入の帯の**起点**（正本 `selection.apply`・`runner.chat_template`・裁定 D101）。

    **組み立て済みのトークン列の中で場面の本文が始まる位置**を引く（前置きの長さを別に数えない）。
    前は「前置き ＋ 空行」のトークン数だけを数えており、chat template の頭のぶん（登録機種では三トークン）だけ
    帯が手前から始まっていた——前置きを持たない腕では役割トークンそのものに掛かっていた（採否表 P305）。
    左詰めのバッチでは行ごとに詰めの長さ pad_len だけずれるので、**行ごとに**求める（採否表 P258）。"""
    body = (scen_text or '') + (instruction or '')
    ids = apply_chat(tokenizer, _user_message(arm_text, scen_text, instruction))
    want = tokenizer(body, add_special_tokens=False)['input_ids'][:probe]
    if not want:
        raise SystemExit('場面の本文が空で起点を引けない')
    for i in range(len(ids) - len(want) + 1):
        if ids[i:i + len(want)] == want:
            return pad_len + i
    raise SystemExit('組み立て済みの列の中に場面の本文の先頭が見つからない（腕の本文か指示の出所を確かめる）')


def _user_message(arm_text, scen_text, instruction):
    """凍結走行器 `user_message` と同じ式（正本 `runner.prompt_assembly`）。"""
    t = arm_text or ''
    return (t + '\n\n' + scen_text + instruction) if t else (scen_text + instruction)


def band_starts(tokenizer, arm_texts, scen_text, instruction, pad_lens):
    """バッチの行ごとの起点（`make_hook` に渡す）。"""
    return [scenario_start_index(tokenizer, t, scen_text, instruction, p) for t, p in zip(arm_texts, pad_lens)]


def _to_hf(g, greedy):
    """正本の生成の設定を transformers の引数名に写す（説明の欄は落とす・採否表 P286）。"""
    out = {'max_new_tokens': g.get('max_tokens')}
    if greedy:
        out['do_sample'] = False
    else:
        out.update({'do_sample': True, 'temperature': g.get('temperature'), 'top_p': g.get('top_p')})
    return {k: v for k, v in out.items() if v is not None}


def quality_generation():
    """品質床の生成の設定（**貪欲**・正本 quality_floor.generation・裁定 D78）。"""
    g = T['quality_floor']['generation']
    assert g['temperature'] == 0, '品質床は貪欲（temperature 零）でなければならない（裁定 D78）'
    if g.get('max_tokens') is None:      # **黙って落とさない**（裁定 D103・採否表 P325）
        raise SystemExit('品質床の最大トークン数が未定（裁定 D66 と採否表 P216 で決める）。'
                         'このまま実機に渡すと transformers の既定で走り、例外も警告も出ない')
    return _to_hf(g, greedy=True)


def main_generation():
    """場面の試行の生成の設定（正本 runner.generation）。"""
    return _to_hf(T['runner']['generation'], greedy=False)


def score_quality(answer_letter, correct_letter, format_fail):
    """品質床の採点（書式外は不正解に数えて分母を保つ・quality_floor.format_fail_rule）。"""
    if format_fail or not answer_letter:
        return False
    return answer_letter.strip().upper() == correct_letter.strip().upper()


def _selftest():
    rng = np.random.default_rng(3)
    v = rng.normal(size=32)
    nv = float(np.linalg.norm(v))
    # (1) ランダム方向は ‖v̂‖ に合う（係数は掛けない・裁定 D90）
    for ratio in T['selection']['candidates']['layers']:
        rs = random_directions(v, 'main', ratio)
        assert len(rs) == N_RAND
        for r in rs:
            assert abs(float(np.linalg.norm(r)) - nv) < 1e-9, 'ランダム方向のノルムが ‖v̂‖ に合っていない（裁定 D90）'
    # (2) **合成の検査**（裁定 D102・採否表 P306・P310）: 加わる量のノルムが
    #     **全方向（v̂・Nk・td・(6b)・ランダム方向） × 全係数 × 全層**で一致する。
    #     前は v 腕とランダム腕の対しか回さなかったため、交差族と S4 の反証に同じ穴が残った。
    raw = {'Nk': rng.normal(size=32) * 7.0, 'td': rng.normal(size=32) * 0.2, 'loaded': rng.normal(size=32) * 3.5}
    others = {k: match_to_static(w, v) for k, w in raw.items()}      # 方向を作る器が合わせたものを模す
    n_checked = 0
    for coef in T['selection']['candidates']['coefficients']:
        for ratio in T['selection']['candidates']['layers']:
            a_v = np.linalg.norm(apply_vector(np.zeros(32), v, coef, +1))
            cand = dict(others)
            for i, r in enumerate(random_directions(v, 'main', ratio)):
                cand['rand:%d' % i] = r
            for name, w in cand.items():
                a_w = np.linalg.norm(apply_vector(np.zeros(32), w, coef, +1))
                assert abs(a_v - a_w) < 1e-9, ('加わる量が v 腕と %s で違う（係数が二度掛かっていないか）' % name, coef, ratio, a_v, a_w)
                n_checked += 1
    assert n_checked == len(T['selection']['candidates']['coefficients']) * len(T['selection']['candidates']['layers']) * (len(raw) + N_RAND)
    # (3) 合わせる器そのもの
    assert abs(float(np.linalg.norm(match_to_static(rng.normal(size=32) * 7.0, v))) - nv) < 1e-9
    # (4) 引き直し（裁定 D84）と層ごとの子ストリーム（係数は入れない・採否表 P285）
    a1 = random_directions(v, 'tune', 0.5)[0]
    a2 = random_directions(v, 'main', 0.5)[0]
    assert not np.allclose(a1, a2), '調整走行と本走行で引き直していない'
    assert np.allclose(a1, random_directions(v, 'tune', 0.5)[0]), '同じ引数で再現しない'
    assert not np.allclose(random_directions(v, 'main', 0.25)[0], random_directions(v, 'main', 0.75)[0]), '層で子ストリームが分かれていない'
    # (5) 割り当てと、試行の番号から方向へ（再開しても変わらない・採否表 P298）
    for n in (200, 201, 100, 7):
        al = allocate(n)
        assert sum(al) == n and max(al) - min(al) <= 1 and al == sorted(al, reverse=True), '割り当ての端数の配り方が規則と違う'
    n = T['n_main']
    got = [direction_of(i, n) for i in range(n)]
    assert [got.count(i) for i in range(N_RAND)] == allocate(n), '試行から方向への写像が割り当てと合わない'
    assert [direction_of(i, n) for i in range(n // 2, n)] == got[n // 2:], '再開すると方向の割り当てが変わる'
    # (6) 加減の向き
    h = rng.normal(size=32)
    assert np.allclose(apply_vector(h, v, 2.0, +1) - h, 2.0 * v)
    assert np.allclose(apply_vector(h, v, 0.5, -1) - h, -0.5 * v)
    # (7) 品質床の採点と生成（transformers の引数名で出す・採否表 P286）
    assert score_quality('A', 'a', False) and not score_quality('A', 'B', False) and not score_quality('A', 'A', True)
    try:
        qg = quality_generation()
    except SystemExit as e:
        qg = None
        assert '最大トークン数' in str(e), '品質床の生成の設定が、別の理由で止まっている: %s' % e
    mg = main_generation()
    if qg is not None:
        assert qg['do_sample'] is False and 'temperature' not in qg, '品質床が貪欲でない'
        assert 'max_new_tokens' in qg, '品質床の最大トークン数が黙って落ちている（裁定 D103）'
    assert set(mg) <= {'do_sample', 'temperature', 'top_p', 'max_new_tokens'}, '生成の設定に transformers が知らない鍵が混ざる'
    assert mg['max_new_tokens'] == T['runner']['generation']['max_tokens'] and mg['temperature'] == T['runner']['generation']['temperature']
        # (8) **帯の起点**（裁定 D101・採否表 P305）: 実トークナイザがあれば、起点のトークンを復号して場面本文の先頭に一致することを確かめる
    band = _selftest_band()
    print('[steer_B selftest] 全方向 × 全係数 × 全層の合成 %d 通り・引き直し・層の子ストリーム・割り当てと再開・加減の向き・生成の設定・%s: すべて通った'
          % (n_checked, band))


def _selftest_band(model_dir=None):
    """帯の起点の自己検査（正本 `runner.chat_template`・裁定 D101）。

    **前置きを持つ腕と持たない腕の両方**で、起点のトークンを復号して場面本文の先頭に一致することを確かめる。
    トークナイザが手元に無ければ、その旨を返して飛ばす（実機の段では必ず走らせる）。"""
    try:
        from transformers import AutoTokenizer
    except Exception:
        return '帯の起点（トークナイザが無いので飛ばした）'
    src = model_dir or os.environ.get('OP4B_TOKENIZER_DIR')
    if not src:
        return '帯の起点（OP4B_TOKENIZER_DIR が無いので飛ばした）'
    tok = AutoTokenizer.from_pretrained(src)
    scen, inst = '場面の本文がここから始まる。', '\n\n指示。'
    body_first = tok(scen + inst, add_special_tokens=False)['input_ids'][0]
    n_ok = 0
    for arm_text in ('前置きがここにある。', ''):            # 前置きを持つ腕と持たない腕
        st = scenario_start_index(tok, arm_text, scen, inst, 0)
        ids = apply_chat(tok, _user_message(arm_text, scen, inst))
        assert ids[st] == body_first, ('起点のトークンが場面本文の先頭でない', arm_text[:8], st, tok.decode([ids[st]]))
        n_ok += 1
    return '帯の起点（実トークナイザで %d 通り・起点のトークンを復号して照合）' % n_ok


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    sys.exit('この器は GPU の上の走行器から import して使う（手元の検査は --selftest）。'
             '走行の組み立て（場面の本文・hook の登録・バッチ）は `boot_stageB.py` の側にある。')
```

## `tools/run_stageB_local.py`（SHA16 A0DED812E8CD6BCB・220 行）

```python
# -*- coding: utf-8 -*-
"""run_stageB_local.py v3 —— 段階 B の走行器（transformers・bf16・**hook つき**・手元／Colab）。

段階 A の走行器（`run_preamble_local.py` v2.7・vLLM の OpenAI 互換サーバ）は凍結物なので触らない。
B は hook を掛けるため transformers を直に使うが、**プロンプトの組み立てと採点の経路は凍結物に合わせる**:
  - 組み立て: `前置き + '\\n\\n' + 場面の本文 + 指示`（前置きを持たない N 腕は場面の本文から）。凍結走行器の `user_message` と同じ。
    起動時に凍結走行器のソースに同じ式があることを確かめる（食い違えば止まる）。
  - 採点: 凍結パーサ `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` の `parse_app_v2` と `is_catastrophic` を import する。
走行の相（正本 `tags`）: 同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`。
介入（正本 `selection.apply`・`random_control`）: `h ← h ± α·v̂` を**場面本文の開始位置から EOS まで**に掛ける。方向とノルムの規則は `steer_B.py`。
詰めは左（`runner.padding`）・バッチは設計定数（`runner.batch`）・生成の設定は `runner.generation`（品質床は `quality_floor.generation`）。
出力: results/<tag>/<tag>__…/{manifest.json, trials-*.jsonl, raw-*.jsonl} と results/sessions-B/<tag>__s<番号>.json。
用法: python tools/run_stageB_local.py --phase main --scenario N1 --session 1 --directions results/dirB/directions.npz
      python tools/run_stageB_local.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, uuid, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B
import steer_B

VERSION = 'v3'
REPO = runs_B.REPO
T = runs_B.load_T()
FROZEN_RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py')
FROZEN_PARSER = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py')
SCEN_PATH = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json')
ASSEMBLY_EXPR = "(t + '\\n\\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)"


def check_assembly_matches_frozen():
    """組み立てが凍結走行器と同じであることを確かめる（裁定 D87・採否表 P288）。

    (i) 凍結走行器のソースに同じ式があること、(ii) 正本に登録があること、(iii) **B 自身の `user_message` が式どおりに振る舞うこと**。
    """
    src_txt = open(FROZEN_RUNNER, encoding='utf-8').read()
    if ASSEMBLY_EXPR not in src_txt:
        raise SystemExit('凍結走行器の組み立ての式と違う（凍結物が変わったか、この器が古い）: %s' % FROZEN_RUNNER)
    reg = (T['runner'].get('prompt_assembly') or '')
    if '前置き' not in reg or '場面の本文' not in reg or '指示' not in reg:
        raise SystemExit('正本 runner.prompt_assembly に組み立ての式が無い（裁定 D87）')
    # (iii) 凍結走行器の式をそのまま評価して、B の実装と突き合わせる
    for t, SCEN_TEXT, INST in (('前置き', '場面', '指示'), ('', '場面', '指示')):
        want = (t + '\n\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)
        got = user_message(t, SCEN_TEXT, INST)
        if want != got:
            raise SystemExit('B の user_message が凍結走行器の式と違う: %r 対 %r' % (want, got))
    return runs_B.sha16_file(FROZEN_RUNNER)


def arm_texts():
    """正本 `arms.sha16` の SHA16 で腕の素材を引き当てる（手で置き場を書かない）。N は前置きを持たない。"""
    want = {v: k for k, v in T['arms']['sha16'].items() if v}
    found = {}
    for root, _, fs in os.walk(os.path.join(REPO, 'arms')):
        for fn in sorted(fs):
            p = os.path.join(root, fn)
            try:
                b = open(p, 'rb').read()
            except OSError:
                continue
            h = hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
            if h in want and want[h] not in found:
                found[want[h]] = {'path': os.path.relpath(p, REPO).replace('\\', '/'), 'sha16': h,
                                  'text': b.decode('utf-8').replace('\r\n', '\n')}
    found['N'] = {'path': None, 'sha16': None, 'text': ''}
    missing = [a for a in T['arms']['panel'] if a not in found]
    if missing:
        raise SystemExit('腕の素材が見つからない（SHA16 で引いた）: %s' % '・'.join(missing))
    return found


def scenario_and_instruction(scenario):
    """場面の本文と**指示**を凍結の素材から引く（凍結走行器 `run_preamble_local.py` と同じ出所・採否表 P287）。"""
    d = json.load(open(SCEN_PATH, encoding='utf-8'))
    s = {x['question_id']: x for x in d['scenarios']}.get(scenario)
    if s is None:
        raise SystemExit('場面が凍結の素材に無い: %s' % scenario)
    inst = (d.get('json_instruction') or {}).get(s.get('family'))
    if inst is None:
        raise SystemExit('指示（json_instruction）が凍結の素材から引けない: 場面 %s' % scenario)
    return s, inst


def user_message(arm_text, scen_text, instruction):
    """凍結走行器 `user_message` と同じ組み立て。"""
    t = arm_text or ''
    return (t + '\n\n' + scen_text + instruction) if t else (scen_text + instruction)


def base_arm_of(arm):
    return re.split(r'[+\-]v', arm)[0]


def arm_plan(arm):
    """腕の名から介入の中身を決める（向き・方向の種類）。無操作なら None。"""
    if '+v' not in arm and '-v' not in arm:
        return None
    sign = +1 if '+v' in arm else -1
    tail = arm.split('+v')[-1] if '+v' in arm else arm.split('-v')[-1]
    kind = {'': 'static', 'rand': 'random', 'Nk': 'Nk', 'td': 'td', '6b': 'loaded'}.get(tail)
    if kind is None:
        raise SystemExit('腕の名から方向を決められない: %s' % arm)
    return {'sign': sign, 'kind': kind, 'base': base_arm_of(arm)}


def make_hook(vec, coef, sign, starts):
    """`h ← h ± α·v̂` を場面本文の開始位置から EOS まで掛ける hook（register_forward_hook）。

    starts は**行ごとの起点**（左詰めの詰めの長さを含む・`steer_B.band_starts`・採否表 P258）。
    復号の段は隠れ状態の長さが一なので、**その一トークン全体に掛ける**（掛けないと生成に介入が入らない・採否表 P259）。
    """
    import torch

    def hook(module, inputs, output):
        hs = output[0] if isinstance(output, tuple) else output
        v = torch.as_tensor(vec, dtype=hs.dtype, device=hs.device)
        add = sign * coef * v
        if len(starts) != hs.shape[0]:
            raise SystemExit('hook: 起点の数（%d）とバッチの行数（%d）が違う——一つのバッチは一つの腕にそろえる'
                             '（正本 runner.one_arm_per_batch・裁定 D114）' % (len(starts), hs.shape[0]))
        if hs.shape[1] == 1:                       # 復号の段（KV キャッシュ）: 位置は必ず帯の内側
            hs[:, 0, :] = hs[:, 0, :] + add
        else:                                       # prefill: 行ごとの起点から後ろに掛ける
            for i, st in enumerate(starts):
                hs[i, int(st):, :] = hs[i, int(st):, :] + add
        return (hs,) + tuple(output[1:]) if isinstance(output, tuple) else hs
    return hook


def scoring():
    """採点は**凍結パーサ**の関数を使う（正本 §2.9・採否表 P289）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location('app_parser_rev2', FROZEN_PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {'parse_app_v2': mod.parse_app_v2, 'is_catastrophic': mod.is_catastrophic,
            'parser_sha16': runs_B.sha16_file(FROZEN_PARSER)}


def trial_record(**kw):
    """正本 `trial_record` の欄をそろえる（欠けたら止まる）。"""
    need = ['生テキスト', '機械判定（三つ組）', '応答様式 (a)(b)', '検査認識の言及', '各選択肢の対数尤度（強制デコード・記述）',
            '副位置の活性（応答トークン平均・fp16）', '操作の有無と層・係数', '方向の id', 'seed', 'バッチ位置', '走行キー', 'proc_uuid']
    assert T['trial_record'] == need, '正本の試行の記録の欄が変わった（器を合わせ直す）'
    fields = ('trial_id', 'trial_index', 'arm', 'scenario', 'tag', 'status', 'catastrophe', 'choice', 'refuse_class',
              'format_fail', 'style_a', 'style_b', 'mention', 'loop_flag', 'truncated', 'correct', 'logprobs',
              'resp_mean_path', 'layer', 'coef', 'direction_id', 'seed', 'batch_pos', 'run_key', 'proc_uuid',
              'runner_sha', 'arms_spec', 'preamble_sha', 'model', 'sampling', 'dry_run')
    missing = [f for f in fields if f not in kw]
    if missing:
        raise SystemExit('試行の記録に欠けた欄がある: %s' % '・'.join(missing))
    return {f: kw[f] for f in fields}


def _selftest():
    sha = check_assembly_matches_frozen()
    texts = arm_texts()
    assert texts['O']['text'] and texts['N']['text'] == ''
    msg = user_message(texts['O']['text'], '場面の本文', '\n指示')
    assert msg.startswith(texts['O']['text']) and msg.endswith('\n指示') and '\n\n場面の本文' in msg
    assert user_message('', '場面の本文', '\n指示') == '場面の本文\n指示', 'N 腕は前置きを付けない'
    plans = {a: arm_plan(a) for a in T['arms']['main']}
    assert plans['Onull'] is None and plans['Onull+v']['kind'] == 'static' and plans['Onull+v']['sign'] == +1
    assert plans['O-Ncold-v']['sign'] == -1 and plans['O-Ncold+vNk']['kind'] == 'Nk'
    assert plans['Onull+vrand']['kind'] == 'random' and plans['Osec-Ncold+v6b']['kind'] == 'loaded'
    assert plans['O-Ncold-vtd']['kind'] == 'td' and plans['O-Ncold-vtd']['base'] == 'O-Ncold'
    # 方向の規則は steer_B 側で確かめる（ここでは繋がりだけ）
    v = np.ones(8)
    rs = steer_B.random_directions(v, 'main', 0.5)
    assert len(rs) == T['random_control']['count']
    # 指示は凍結の素材から引ける（採否表 P287）
    sc, inst = scenario_and_instruction(T['scenarios'][0])
    assert isinstance(inst, str) and inst, '指示（json_instruction）が引けない'
    # 採点は凍結パーサの関数（採否表 P289）
    sco = scoring()
    assert callable(sco['parse_app_v2']) and callable(sco['is_catastrophic'])
    # 試行の記録の欄は正本の登録（裁定 D97）から作る
    fields = T['trial_record_fields']['fields']
    rec = trial_record(**{f: None for f in fields})
    assert len(rec) == len(fields)
    # hook は復号の段でも掛かる（採否表 P259）——小さな模擬で形だけ確かめる
    try:
        import torch
        starts = [2, 0]
        h_pre = torch.zeros((2, 5, 3))
        h_dec = torch.zeros((2, 1, 3))
        hk = make_hook(np.ones(3), 2.0, +1, starts)
        hk(None, None, h_pre)
        hk(None, None, h_dec)
        assert float(h_pre[0, 0].sum()) == 0 and float(h_pre[0, 2].sum()) == 6, 'prefill の帯の起点が違う'
        assert float(h_dec[0, 0].sum()) == 6 and float(h_dec[1, 0].sum()) == 6, '復号の段で加算が起きていない'
    except ImportError:
        pass
    print('[run_stageB_local selftest] 組み立て（凍結走行器 SHA16 %s・振る舞いの照合つき）・腕の素材・腕の名から方向・指示・凍結パーサ（%s）・'
          '試行の記録の欄 %d・hook の帯と復号の段: すべて通った' % (sha, sco['parser_sha16'], len(fields)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--phase', choices=['identity', 'tune', 'quality', 'main'], default=None)
    ap.add_argument('--scenario', default=None)
    ap.add_argument('--session', type=int, default=1)
    ap.add_argument('--directions', default=None, help='direction_B.py が凍結した方向（npz）')
    ap.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
    ap.add_argument('--out-root', default=None)
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    check_assembly_matches_frozen()
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as e:
        sys.exit('torch／transformers が無い: %s（この器は GPU の上で走らせる。手元の検査は --selftest）' % e)
    sys.exit('走行の本体（バッチ生成・hook の登録・採点・記録の書き出し）は Colab の段で埋める。'
             '規則の検査は --selftest、札の経路の検査は tools/dry_run_B.py（合成データ）で済ませてある。')
```

## `tools/control_chart_B.py`（SHA16 B78F1033FF53ABF6・92 行）

```python
# -*- coding: utf-8 -*-
"""control_chart_B.py v2 —— 段階 B の**校正の管理図**（正本 `calibration`・起草者の見直し S1・実装検分の採否表 P276）。

別置きの校正腕は置かない（試行が増えるため）。代わりに、**無操作の腕の率をセッションごとに並べる**。
  - 点: 腕 × 場面 × セッションの全分母破局率（分子＝破局・分母＝n_ok）。
  - 初点: 同じ腕 × 場面の**最初のセッション**（初点は判定しない）。
  - 帯: `calibration.band_pt`（二標本・両側・厳密 Fisher）。外れたら「器の異常」を記帳し、**その走行を含む対比の確証札に注を付す**。
限界（正本 `calibration.limitation`）: 同じ腕 × 場面が一つのセッションに収まる場合、点は一つだけで管理図にならない。その旨を印字する。
出力: records/B/control-chart-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/control_chart_B.py [--root <results>] [--allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.stats import fisher_exact
import runs_B

VERSION = 'v2'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
CAL = T['calibration']
NOOP = set(T['arms']['noop'])
BAND = CAL['band_pt'] / 100.0

idx = runs_B.index_runs(T, T['tags']['main'], a.root, allow_dry=a.allow_dry)
points, anomalies, notes = [], [], []
by_cell = {}
for (sc,), recs in sorted(idx.items()):
    for rec in recs:
        sess = rec['manifest'].get('session')
        for arm, c in runs_B.cell_counts(rec['trials_path']).items():
            if arm not in NOOP:
                continue
            by_cell.setdefault((sc, arm), []).append({'session': sess, 'run_key': rec['run_key'], 'k': c['cat'], 'n': c['n_ok'],
                                                      'rate': runs_B.rate(c['cat'], c['n_ok'])})
for (sc, arm), pts in sorted(by_cell.items(), key=str):
    pts.sort(key=lambda x: (x['session'] is None, x['session']))
    for i, p in enumerate(pts):
        row = dict(p, scenario=sc, arm=arm, first_point=(i == 0))
        if i == 0:
            row['verdict'] = '初点（判定しない）'
        elif p['rate'] is None or pts[0]['rate'] is None:
            # **使える試行が零の点は判定しない**（裁定 D110・採否表 P323）。
            # 前は空を零と読んで差を計算し、測れなかった点に「器の異常」の札を付けていた。
            row['verdict'] = '測れなかった（使えた試行が零・判定しない）'
        else:
            base = pts[0]
            pval = float(fisher_exact([[p['k'], p['n'] - p['k']], [base['k'], base['n'] - base['k']]])[1])
            d = (p['rate'] or 0) - (base['rate'] or 0)
            out = abs(d) > BAND
            row.update({'diff_pt': round(100 * d, 3), 'p': pval, 'outside': out,
                        'verdict': ('**帯の外**（器の異常を記帳し、この走行を含む対比の確証札に注を付す）' if out else '帯の内側')})
            if out:
                anomalies.append({'scenario': sc, 'arm': arm, 'run_key': p['run_key'], 'diff_pt': row['diff_pt']})
        points.append(row)
    if len(pts) == 1:
        notes.append('%s × %s は点が一つ（%s）——管理図にならない（%s）' % (sc, arm, pts[0]['run_key'], CAL['limitation']))

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'control-chart-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p_ in (out_md, out_json):
        if os.path.exists(p_):
            sys.exit('既にある（--force で上書き）: %s' % p_)
json.dump({'kind': 'control_chart_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'band_pt': CAL['band_pt'], 'points': points, 'anomalies': anomalies, 'notes': notes,
           'design': CAL['design'], 'limitation': CAL['limitation']},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 校正の管理図（機械生成・`tools/control_chart_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- %s' % CAL['design'], '- 帯 %g pt・%s・相手は初点（同じ腕 × 場面の最初のセッション）。' % (CAL['band_pt'], CAL['test']),
     '- **帯の外の点 %d 件**。点が一つしかないセル %d 件。' % (len(anomalies), len(notes)), '',
     '| 場面 | 腕 | セッション | 破局/n_ok | 率 | 初点との差 pt | p | 判定 |', '|---|---|---|---|---|---|---|---|']
for p_ in points:
    L.append('| %s | %s | %s | %d/%d | %s | %s | %s | %s |'
             % (p_['scenario'], p_['arm'], p_['session'], p_['k'], p_['n'],
                None if p_['rate'] is None else round(p_['rate'], 4), p_.get('diff_pt', '—'),
                ('%.4g' % p_['p']) if p_.get('p') is not None else '—', p_['verdict']))
if notes:
    L += ['', '## 注（限界）', ''] + ['- ' + n for n in notes]
L += ['', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[control_chart_B] %s | 点 %d・帯の外 %d・点が一つのセル %d' % (out_md, len(points), len(anomalies), len(notes)))
sys.exit(1 if anomalies else 0)
```
