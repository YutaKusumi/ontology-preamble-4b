# 器材のソース（逐語・参照）（参照・関わる問い (b)(g)・機械生成・2026-09-19 01:57 UTC）

## `tools/integrity_B.py`（SHA16 FFB9E4177BD3E6A9・271 行）

```python
# -*- coding: utf-8 -*-
"""integrity_B.py v4 —— 段階 B の走行の**整合検査**（率盲検・許可表方式）。

**判定欄（catastrophe・choice・correct・style_a・style_b・mention）は読まない。** 許可した欄だけを取り出し、manifest と正本の登録に突き合わせる。
当てる相（採否表 P230・**本走行の後だけでなく、調整走行と品質床にも当てる**）:
  同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`
検査:
  行数と目標（腕 × n）・n_ok と api_error・書式外の件数（率ではない）・trial_id の重複と trial_index の欠落・腕ごとの n の揃い・
  preamble_sha（正本 `arms.sha16`・manifest の runner_sha と model は走行を跨いだ同一性で見る）・**seed が正本の式で組み直した値と一致するか**（`seeds.derivation_formula`）・
  生成の設定（`runner.generation`／品質床は `quality_floor.generation`）・
  層と係数が候補の格子にあるか・**バッチの大きさの凍結**（`runner.fixed_across_runs`）・**詰めの向き**（`runner.padding`）・
  走行キーとセッション記録の対応（`sessions.missing_rule`）・dry-run の印。
  **登録の升目の欠け**（相ごとに正本から升目を列挙し、欠けを不整合にする・裁定 D126・採否表 P361・v4）・
  **dtype・並べ方・transformers の版・refuse の規則の SHA** の走行を跨いだ同一性と正本との一致（採否表 P362・v4）。
出力: records/B/integrity-<tag>-<日付>.{md,json}（--force が無ければ上書きしない）。不整合があれば非零で終わる。
用法: python tools/integrity_B.py --tag stageB [--root results/_synth/all --allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v4'
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
        # 「書式外なのに正答」の検査は**ここには置けない**（裁定 D113・採否表 P313）。
        # 正答の欄は率盲検の欄なので、許可表で読む行では恒に空になり、この検査は決して発火しなかった。
        # 規約は採点器（steer_B.score_quality）が保証し、読み口が数えた件数を門と集計器が読んで止める。
        # **正本の式で組み直した値と突き合わせる**（正本 seeds.derivation_formula・裁定 D107・採否表 P312）。
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
                # 記録の種は**バッチの種**（裁定 D127）。書く側と同じ `recorded_seed` で組み直す。
                bad_seed = [r for r in rs if r.get('seed') != runs_B.recorded_seed(T, cs, r.get('trial_index'))]
                if bad_seed:
                    problems.append('%s × %s: seed が正本の式で組み直した値と違う行が %d 件（先頭 trial_index %s・記録 %s・式 %s）'
                                    % (rk, arm, len(bad_seed), bad_seed[0].get('trial_index'), bad_seed[0].get('seed'),
                                       runs_B.recorded_seed(T, cs, bad_seed[0].get('trial_index'))))
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
    # **dtype と並べ方は正本の値と照らす**（採否表 P362・v4）
    if m.get('dtype') is not None and m['dtype'] != T['runner']['dtype']:
        problems.append('%s: dtype %s が正本 runner.dtype（%s）と違う' % (rk, m['dtype'], T['runner']['dtype']))
    if m.get('order') is not None and m['order'] != T['runner']['order_id']:
        problems.append('%s: 並べ方 %s が正本 runner.order_id（%s）と違う' % (rk, m['order'], T['runner']['order_id']))
    # **全相で確かめる**（裁定 D126・2026-09-18）。前は本走行の相にしか掛かっておらず、
    # 調整走行・品質床・同一性選別では記録を丸ごと消しても零件だった（系統外の検分で走らせて捕まった・採否表 P349）。
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

# ---- 登録の升目の欠け（裁定 D126・採否表 P361・v4） ----
# 相ごとに正本から升目を列挙し、記録に無い升目を不整合にする。前は調整走行の欠けを門が見るだけで、整合検査は升目を列挙していなかった。
# 選定後の品質床の升目は門の選んだ組で決まるので、ここでは列挙しない（集計器が腕ごとに数えて「合格にしない」）。
_have = set(cells_by_key)
if PHASE == 'main':
    _want = {(sc, arm) for sc in T['scenarios'] for arm in T['arms']['by_scenario'][sc]}
    _have = {(k[0], k[1]) for k in _have}
elif PHASE == 'tune':
    _V, _R = T['selection']['tune']['arms']
    _want = {(sc, l, cf, arm) for sc in T['selection']['tune']['scenarios'] for (l, cf) in CAND for arm in (_V, _R)}
elif PHASE == 'quality':
    _ops = {}
    for _fk in ('B_sub', 'B_add'):
        _c0 = T['families'][_fk]['contrasts'][0]
        _ops[_c0['base_arm']] = _c0['A'][len(_c0['base_arm']):]        # 土台の腕と、そこに当てる演算（正本の対比から引く）
    _want = {('selection', b + _ops[b], l, cf) for b in T['quality_floor']['arms'] for (l, cf) in CAND} |             {('selection', b, None, None) for b in T['quality_floor']['arms']}
    _have = {(k[0], k[1], k[2], k[3]) for k in _have}
else:
    _want = {('transformers', T['identity_screen']['scenario'], arm) for arm in T['identity_screen']['arms_run']}
_lack = sorted(_want - _have, key=str)
if _lack:
    problems.append('**登録の升目が %d 件欠けている**（先頭 %s・正本から列挙・裁定 D126・採否表 P361）'
                    % (len(_lack), '・'.join(str(x) for x in _lack[:3])))

# ---- 判定欄を読まないことの自己検査（率盲検・裁定 D97） ----
if set(ALLOW) & set(BLIND):
    problems.append('許可表に判定欄が混ざっている: %s' % '・'.join(sorted(set(ALLOW) & set(BLIND))))

# ---- 走行を跨いだ同一性（runner.fixed_across_runs・採否表 P274） ----
# **manifest に実在する欄で見る**（裁定 D126・2026-09-18）。`versions` はセッション記録の欄であって
# manifest には無いので、この検査は**常に飛んでいた**（系統内の検分で捕まった・採否表 P362）。
# あわせて、値が空のときも黙って飛ばさず不整合に数える。
FIX_KEYS = {'重みの rev': 'model_rev', 'tokenizer の版': 'tokenizer_rev', 'バッチの大きさ': 'batch',
            '詰めの向き': 'padding', '走行器の SHA': 'runner_sha', '環境の SHA': 'pip_freeze_sha16',
            'dtype': 'dtype', '並べ方': 'order', 'transformers の版': 'transformers_version', 'refuse の規則の SHA': 'refuse_rules_sha16'}
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
```

## `tools/sample_inspection_B.py`（SHA16 21F786D1D3574F2C・145 行）

```python
# -*- coding: utf-8 -*-
"""sample_inspection_B.py v3 —— 段階 B の**抽出検査**（腕と場面を伏せた標本・目視の記録・対応表の封印）。段階 A の型。

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

VERSION = 'v3'
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
# **セル（場面 × 腕）で束ねてから引く**（裁定 D130・採否表 P369・2026-09-19）。前は走行ごと × 腕でセルを作ったので、
# 中断と再開で**セッションを跨いで**分かれたセルは、その数に比例して高い確率で引かれていた。
by_cell = {}
for k, recs in sorted(idx.items(), key=lambda kv: str(kv[0])):
    for rec in recs:
        raw = {}
        if rec['raw_path']:
            for r in runs_B.iter_jsonl(rec['raw_path']):
                raw[r.get('trial_id')] = r.get('text') or ''
        for r in runs_B.iter_jsonl(rec['trials_path'], ('trial_id', 'arm', 'scenario', 'status', 'style_b', 'format_fail')):
            if r['status'] == 'ok':
                sc_ = r.get('scenario') or rec['manifest'].get('scenario')
                c_ = by_cell.setdefault((sc_, r['arm']), {'scenario': sc_, 'arm': r['arm'], 'rows': [], 'raw': {}})
                c_['rows'].append(r)
                c_['raw'][r['trial_id']] = raw.get(r['trial_id'], '')
cells = [by_cell[k] for k in sorted(by_cell, key=str)]
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

## `tools/control_chart_B.py`（SHA16 1DF75412E513EBB2・100 行）

```python
# -*- coding: utf-8 -*-
"""control_chart_B.py v3 —— 段階 B の**校正の管理図**（正本 `calibration`・起草者の見直し S1・実装検分の採否表 P276）。

別置きの校正腕は置かない（試行が増えるため）。代わりに、**無操作の腕の率をセッションごとに並べる**。
  - 点: 腕 × 場面 × セッションの全分母破局率（分子＝破局・分母＝n_ok）。
  - 初点: 同じ腕 × 場面の**最初のセッション**（初点は判定しない）。
  - 帯: `calibration.band_pt`（二標本・両側・厳密 Fisher）。**帯を超え、かつ p が `calibration.alpha` 未満のときだけ**「器の異常」を記帳し、**その走行を含む対比の確証札に注を付す**（v3・2026-09-19・正本 `calibration.judgement`・v2 までは p を判定に使っていなかった）。
限界（正本 `calibration.limitation`）: 同じ腕 × 場面が一つのセッションに収まる場合、点は一つだけで管理図にならない。その旨を印字する。
出力: records/B/control-chart-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/control_chart_B.py [--root <results>] [--allow-dry] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scipy.stats import fisher_exact
import runs_B

VERSION = 'v3'
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
ALPHA = CAL['alpha']

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
            # **使える試行が零の点は判定しない**（裁定 D110・採否表 P324）。
            # 前は空を零と読んで差を計算し、測れなかった点に「器の異常」の札を付けていた。
            row['verdict'] = '測れなかった（使えた試行が零・判定しない）'
        else:
            base = pts[0]
            pval = float(fisher_exact([[p['k'], p['n'] - p['k']], [base['k'], base['n'] - base['k']]])[1])
            d = (p['rate'] or 0) - (base['rate'] or 0)
            # **帯を超え、かつ厳密検定の p が alpha 未満のときだけ異常**（正本 calibration.judgement・裁定 D127・採否表 P350）。
            # v2 までは差だけで判定し、正本が「厳密」と書く検定の p を一度も使っていなかった。
            # この直しは異常の札を減らす向き（小さな n の揺れで札が立たない）であり、起草者の引力と同じ側——正本に書いた。
            band_out = abs(d) > BAND
            out = band_out and (pval < ALPHA)
            row.update({'diff_pt': round(100 * d, 3), 'p': pval, 'outside': out, 'band_outside': band_out,
                        'verdict': ('**帯の外かつ有意**（器の異常を記帳し、この走行を含む対比の確証札に注を付す）' if out else
                                    ('帯の外だが有意でない（異常にしない・p を印字する）' if band_out else '帯の内側'))})
            if abs(abs(d) - BAND) < 1e-9:
                row['verdict'] += '・境目に一致（%g pt）' % CAL['band_pt']
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

## `tools/freeze_B.py`（SHA16 AAFC319A94AA33EE・175 行）

```python
# -*- coding: utf-8 -*-
"""freeze_B.py v5 —— 段階 B の**凍結の記帳**（凍結物の SHA・封印予想・凍結時に記帳する値・逸脱台帳の口）。

凍結するもの（正本 `publication.record_first`・草案8B §2.11）:
  凍結本文（草案）・正本 `design/contrasts-B.json`・腕と方向の定義・器材・報告の雛形・**封印予想**。
凍結時に記帳する値（設計の段では書けないもの）:
  - 重みの rev・tokenizer の版・**総層数**（`selection.candidates.layer_index_rule`）と層の添字
  - **腕ごとのトークン長**（裁定 D82・`position_length.record_at_freeze`）
  - 品質床の課題の出所・版・ライセンス・断片の SHA（裁定 D66）と、**無操作の実測の正答率**（下限 `quality_floor.base_min` を凍結する根拠・裁定 D129）
    （入力・帯・採点・最大トークン数は裁定 D120 で正本に登録したので、ここでは求めない・v4）
  - **‖v̂‖ と主位置の ‖h‖ の比**（層ごと・`activation_storage.h_norm_record`・採否表 P356）
  - **まだ下りていない登録者の裁定**: 同一性選別に Osec-Ncold を足すか（`identity_screen.b_panel_arms_compared`）・S4 の効き目を絶対値のままにするか（`effect_pt_caveat`）
  - v̂ の SHA（`selection.vector_fix`）と方向の要約統計（ノルム・コサイン・場面間の安定性）
封印予想（`seal_format`）: 確証の各対比の符号と S4 の反証。**B のデータを一つも見る前**に書き、情報状態と時機を添える。
凍結の後の変更はすべて**逸脱**とし、番号・日付・理由・登録者の承認を記帳する（`deviation.rule`）。
**採否表の引用の照合**（v5・2026-09-19）: 正本・草案・報告雛形・器材の「採否表 P…」を `tools/citations_B.py` で照らし、違反があれば止める。
出力: records/B/FREEZE-RECORD-B.md と同 .json（--force が無ければ上書きしない）。
用法: python tools/freeze_B.py --draft design/design-stageB-draft12.md [--seal records/B/seal-B.json] [--values records/B/freeze-values-B.json] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v5'
REPO = runs_B.REPO
CARRYOVER = {'凍結走行器（組み立てと採点の型）': 'tools/run_preamble_local.py',
             '凍結パーサ': 'arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py',
             '場面の素材': 'arms/frozen-from-ryokai-os/app-scenarios.json',
             # 走行器が様式・言及・refuse の分類・ループを段階 A の凍結した関数で書くようになったので、その出所も凍結物に数える（2026-09-19）
             '様式と言及の器（段階 A）': 'tools/response_mode_A.py',
             '名の語彙（段階 M）': 'tools/response_mode_M.py',
             '名の語彙（段階 F・一致の照合）': 'tools/response_mode_F.py',
             '言及の語彙（段階 F の正本）': 'design/contrasts-F.json',
             'refuse の分類の規則（丙）': 'arms/materials-draft/hei/refuse-rules-v2.json'}
TOOLS = ['runs_B.py', 'rules_B.py', 'make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py', 'numbers_lint.py', 'gate_B.py', 'analyze_B.py',
         'layers_B.py', 'integrity_B.py', 'sample_inspection_B.py', 'direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'synth_B.py',
         'dry_run_B.py', 'mutation_B.py', 'endtoend_B.py', 'build_report_B.py', 'freeze_B.py', 'control_chart_B.py', 'citations_B.py']
NEED_VALUES = ['model_rev', 'tokenizer_rev', 'num_hidden_layers', 'layer_indices', 'arm_token_lengths',
               'quality_task', 'quality_base_accuracy', 'v_hat_sha256', 'direction_stats', 'h_norm_ratio',
               'identity_osec_ncold_decision', 's4_effect_decision']
ap = argparse.ArgumentParser()
ap.add_argument('--draft', required=True)
ap.add_argument('--seal', default=None)
ap.add_argument('--values', default=None, help='凍結時に記帳する値（json・上の NEED_VALUES）')
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-missing', action='store_true', help='記帳の値や封印が揃っていなくても書く（**凍結ではなく点検用**）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
cpath = a.contrasts or runs_B.CPATH
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'FREEZE-RECORD-B.md')
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

frozen = {'canon': {'path': 'design/contrasts-B.json', 'sha16': runs_B.sha16_file(cpath), 'version': T['version']},
          'draft': {'path': os.path.relpath(a.draft, REPO).replace('\\', '/'), 'sha16': runs_B.sha16_file(a.draft)},
          'facts': {'path': 'records/B/design-facts-B.md', 'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'))},
          'report_template': {'path': 'records/B/results-report-template-B.md',
                              'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))},
          'arms': T['arms']['sha16'], 'arm_files': T['arms'].get('files'),
          'tools': {}}
for t in TOOLS:
    p = os.path.join(REPO, 'tools', t)
    frozen['tools'][t] = runs_B.sha16_file(p) if os.path.exists(p) else None
frozen['carryover'] = {}
for name, rel in CARRYOVER.items():
    p = os.path.join(REPO, *rel.split('/'))
    frozen['carryover'][name] = {'path': rel, 'sha16': runs_B.sha16_file(p) if os.path.exists(p) else None}
missing_carry = [n for n, v in frozen['carryover'].items() if not v['sha16']]
missing_tools = [t for t, v in frozen['tools'].items() if v is None]

VALUES = runs_B.read_json(a.values) if a.values else {}
missing_values = [k for k in NEED_VALUES if k not in VALUES or VALUES[k] in (None, '', [], {})]   # **空も欠けと見る**（採否表 P282）
SEAL = runs_B.read_json(a.seal) if a.seal else None
conf_ids = [c['id'] for F in T['families'].values() for c in F['contrasts']]
missing_seal = [] if not SEAL else [i for i in conf_ids if i not in (SEAL.get('signs') or {})]
blockers = []
if missing_tools:
    blockers.append('器材が揃っていない: %s' % '・'.join(missing_tools))
if missing_carry:
    blockers.append('B が依存する凍結物が見つからない: %s' % '・'.join(missing_carry))
if missing_values:
    blockers.append('凍結時に記帳する値が揃っていない: %s' % '・'.join(missing_values))
if SEAL is None:
    blockers.append('封印予想が渡されていない（`seal_format` の様式で、データを一つも見る前に書く）')
else:
    if missing_seal:
        blockers.append('封印の無い確証の対比: %s' % '・'.join(missing_seal))
    if not SEAL.get('s4'):
        blockers.append('**S4 の反証の封印が無い**（正本 seal_format.scope は確証の族と S4 の両方を対象にする）')
    # **予想符号を列挙として検べる**（裁定 D121・採否表 P341）——集計器だけでなく凍結の器でも止める。v3 までは有無しか見ていなかった
    _vals = set(T['seal_format']['sign_values'])
    _bad = sorted({str(v) for v in (SEAL.get('signs') or {}).values() if v not in _vals})
    if _bad:
        blockers.append('封印の予想符号が正本の一覧（seal_format.sign_values）に無い: %s（使える語: %s・裁定 D121）' % ('・'.join(_bad), '・'.join(sorted(_vals))))
    if SEAL.get('s4') and SEAL['s4'] not in _vals:
        blockers.append('S4 の反証の封印が正本の一覧に無い: %s（裁定 D121）' % SEAL['s4'])
    # **正本の鍵の登録から見る**（手書きの並びを置かない・裁定 D115・採否表 P335〔二体目 G5〕）
    for need, label in sorted(T['seal_format']['record_keys'].items()):
        if need in ('signs', 's4'):
            continue                      # 上で別に見ている
        if not SEAL.get(need):
            blockers.append('封印の記録に欄が無い: %s（%s・seal_format.record_keys）' % (need, label))
# 整備の記録に載る SHA16 が現物と一致するかを見る（実装検分の採否表 P299——古い記録のまま凍結しない）。
# **止める門の前に置く**（裁定 D112・採否表 P322）。前は門の後ろにあったので、古い記録だけのときに
# 記録が書かれ、しかも「点検であり凍結ではない」と事実でないことを書いていた。
import re as _re
rec_path = os.path.join(REPO, 'records', 'B', 'tooling-record-B-2026-09-18.md')
stale, unlisted = [], []
if os.path.exists(rec_path):
    _txt = open(rec_path, encoding='utf-8').read()
    _listed = dict(_re.findall(r'`tools/([\w.]+)` \| [^|]*\| ([0-9A-F]{16})', _txt))
    for _name, _sha in _listed.items():
        _p = os.path.join(REPO, 'tools', _name)
        if os.path.exists(_p) and runs_B.sha16_file(_p) != _sha:
            stale.append(_name)
    unlisted = [t for t in TOOLS if t not in _listed]
if stale:
    blockers.append('器材の整備の記録の SHA16 が現物と違う（記録を作り直してから凍結する）: %s' % '・'.join(stale))
if unlisted:
    blockers.append('器材の整備の記録に載っていない器材がある（記録に足す）: %s' % '・'.join(unlisted))
# **採否表の引用の照合**（v5）: 手で打った引用が別の行を指していないか（裁定の番号と出所の札で照らせる範囲）
import citations_B
_cv, _ct = citations_B.check_all(REPO)
if _cv:
    blockers.append('採否表の引用の照合に違反が %d 件ある（`tools/citations_B.py`）: %s' % (len(_cv), '・'.join('%s %s' % (w, p) for w, p, _ in _cv[:5])))

if blockers and not a.allow_missing:
    print('[freeze_B] 凍結できない（--allow-missing は点検用）:')
    for b in blockers:
        print('  - ' + b)
    sys.exit(1)

REC = {'kind': 'freeze_B', 'version': VERSION, 'frozen_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'frozen_jst': jst.strftime('%Y-%m-%d %H:%M'),
       'frozen': frozen, 'values': VALUES, 'seal': SEAL, 'seal_sha256': (None if not a.seal else __import__('hashlib').sha256(open(a.seal, 'rb').read()).hexdigest().upper()),
       'stale_record_hashes': stale, 'unlisted_tools': unlisted, 'citation_violations': len(_cv), 'blockers': blockers, 'deviations': [],
       'deviation_rule': T['deviation']['rule'], 'record_first': T['publication']['record_first']}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 凍結記録（機械生成・`tools/freeze_B.py` %s）' % VERSION, '',
     '- 凍結の時刻: %s UTC（日本時間 %s）。%s' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'),
                                            ('**点検（--allow-missing）であり凍結ではない**' if a.allow_missing else
                                             ('**止めているものがある——凍結していない**' if blockers else '凍結した。'))), '',
     '## 凍結物', '', '| 物 | 置き場 | SHA16 |', '|---|---|---|']
for k in ('canon', 'draft', 'facts', 'report_template'):
    L.append('| %s | `%s` | %s |' % (k, frozen[k]['path'], frozen[k]['sha16']))
for t, v in sorted(frozen['tools'].items()):
    L.append('| 器材 | `tools/%s` | %s |' % (t, v or '**無い**'))
for name, v in sorted(frozen['carryover'].items()):
    L.append('| 持ち越しの凍結物 | `%s` | %s |' % (v['path'], v['sha16'] or '**無い**'))
for arm, sha in sorted((frozen['arms'] or {}).items()):
    L.append('| 腕 | %s | %s |' % (arm, sha or '（前置きを持たない）'))
L += ['', '## 凍結時に記帳する値', '']
for k in NEED_VALUES:
    L.append('- %s: %s' % (k, json.dumps(VALUES[k], ensure_ascii=False) if k in VALUES else '**まだ無い**'))
L += ['', '## 封印予想（`seal_format`）', '']
if SEAL:
    L += ['- 時機: %s' % T['seal_format']['timing'], '- 情報状態: %s' % T['seal_format']['information_state'],
          '- 封印した符号: %d／確証の対比 %d' % (len(SEAL.get('signs') or {}), len(conf_ids)),
          '- S4 の反証: %s' % (SEAL.get('s4') or '**まだ無い**'), '- %s' % T['seal_format']['reading']]
else:
    L.append('- **まだ無い**（`seal_format` の様式で、データを一つも見る前に書く）')
if blockers:
    L += ['', '## 凍結を止めているもの', ''] + ['- ' + b for b in blockers]
L += ['', '## 逸脱台帳', '', '- %s' % T['deviation']['rule'], '- %s' % T['deviation']['silent_fix'], '- （凍結の後に足す）', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[freeze_B] %s | 止めているもの %d 件' % (out_md, len(blockers)))
sys.exit(2 if blockers else 0)
```

## `tools/build_report_B.py`（SHA16 01332F9C9D3C4CF7・202 行）

```python
# -*- coding: utf-8 -*-
"""build_report_B.py v4 —— 段階 B の結果報告を、**雛形**（`records/B/results-report-template-B.md`）と集計の出力から組み立てる。

雛形の〔結果 X〕を、機械の区画で置き換える:
  A 要約／B 走行の記録（整合検査・抽出検査・セッション）／C 門1 と選定／D 確証の族の表／E 封印した符号との照合／
  F 記述の族／G S4 の反証（**同等性の規則・区間は Newcombe**・v4）／H 利益相反と情報状態／
  I td の特異性とランダム方向の等質性（裁定 D123・D127・v4）／J 副位置の読み（`tools/layers_B.py` の出力・**必須**・裁定 D132・v4）
**散文に手計算の数を残さない**（正本 `report_rules.typed_numbers`）。数はすべて集計の json から来る。
組み立ての後に走査器（`tools/report_lint.py`）を走らせる口を持つ（--lint）。
用法: python tools/build_report_B.py --analysis records/B/analysis-B-<日付>.json --gate records/B/gate-B-<日付>.json \
        [--integrity records/B/integrity-stageB-<日付>.json] [--out records/B/results-report-B.md] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v4'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--analysis', required=True)
ap.add_argument('--gate', required=True)
ap.add_argument('--integrity', required=True, help='tools/integrity_B.py の json（必須・採否表 P293）')
ap.add_argument('--sampling', required=True, help='抽出検査の封印 json（必須・採否表 P293）')
ap.add_argument('--layers', required=True, help='tools/layers_B.py の json（副位置の読み・必須・裁定 D132）')
ap.add_argument('--allow-dry', action='store_true', help='検査用の口（合成データから組む・区画ごとに印を差し込む）')
ap.add_argument('--force-problems', action='store_true', help='整合検査に不整合があっても組む（理由を記録に残すこと）')
ap.add_argument('--template', default=os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--lint', action='store_true', help='組み立ての後に報告の走査器（tools/report_lint.py）を走らせる（裁定 D112・採否表 P327）')
a = ap.parse_args()
T = runs_B.load_T()
A = runs_B.read_json(a.analysis)
G = runs_B.read_json(a.gate)
INT = runs_B.read_json(a.integrity) if a.integrity else None
SMP = runs_B.read_json(a.sampling) if a.sampling else None
LY = runs_B.read_json(a.layers)
assert LY.get('kind') == 'layers_B', '副位置の読みの記録の種類が違う'
assert A.get('kind') == 'analyze_B' and G.get('kind') == 'gate_B', '集計または門の記録の種類が違う'
DRY = A.get('dry_marks') or []
if DRY and not a.allow_dry:
    sys.exit('**合成データ（dry-run の印つき）から報告を組もうとしている**: %s。検査用は --allow-dry（採否表 P279）' % '・'.join(DRY))
if INT and INT.get('problems') and not a.force_problems:
    sys.exit('整合検査に不整合が %d 件ある。直してから報告を組む（--force-problems は理由を記録に残す場合のみ・採否表 P293）' % len(INT['problems']))
MARK = ('【合成データ・本番ではない】' if DRY else '')
out_md = a.out or os.path.join(REPO, 'records', 'B', 'results-report-B.md')
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
tpl = open(a.template, encoding='utf-8').read()
PS = T['print_strings']
c = A['counts']
n_conf = sum(x['m'] for x in T['families'].values())


MB = T['report_rules']['machine_block']        # 機械の区画の印（段階 A と同じ・報告の走査器が読む・2026-09-19）


def block(lines):
    """機械の区画。**区画の印で囲む**（走査器が区画の外の数を検べ、区画の中身を記録と突合する・v4）。
    合成データから組んだときは**区画ごとに**印を差し込む（切り出しで落ちないように・採否表 P279）。"""
    out = [l for l in lines if l is not None]
    if MARK:
        out = [MARK] + out
    return '\n'.join([MB['begin']] + out + [MB['end']])


A_sum = block([
    '```',
    PS['first_finding'].format(confirmed=c['確証'], undecidable=c['判定不能（検閲）'], qfloor=c['判定不能（品質床）'],
                               gap=c['判定不能（採点欠落）'], nodata=c['判定不能（測れなかった）'],
                               ff=c['判定保留（書式外転位）'], refuse=c['判定保留（refuse 転位）'] + c['判定保留（refuse 転位・差）'],
                               style=c['判定保留（様式転位）'], ns=c['非有意']),
    PS['scope'],
    'S4 の反証: %s' % A['s4'].get('verdict'),
    '```'])
B_run = block(['```',
               '整合検査: 不整合 %d 件・注 %d 件（%s）' % (len(INT['problems']), len(INT['notes']), INT['tag']),
               '抽出検査: 標本 %d 件・対応表の封印あり（並べ替え %s）' % (SMP.get('n_items', 0), SMP.get('shuffled')),
               '正本 SHA16 %s・集計 %s UTC' % (A['contrasts_sha16'], A['generated_utc']),
               '```'])
sel = G['selection']['pick'] or {}
C_gate = block(['```',
                (PS['gate1_open'].format(k=G['gate1']['quality_pass_candidates'], layer=sel.get('layer'), coef=sel.get('coef'),
                                         eff=sel.get('eff_pt'), tied=len(G['selection']['tied']))
                 if G['gate1']['open'] else PS['gate1_closed']),
                PS['selection_coi'], PS['selection_direction'],
                ('同値の帯: 幅 %s pt（帰無の模擬 %s 回・同値の候補 %d 組）' % (G['selection']['equivalence_band']['q95_pt'],
                                                                format(G['selection']['equivalence_band']['reps'], ','),
                                                                len(G['selection']['tied'])) if G['selection'].get('equivalence_band') else ''),
                (G['selection'].get('tie_note') or ''), (G['selection'].get('nonpositive_stop') or ''),
                '```'])
fmt_p = lambda x: ('—' if x is None else ('%.3g' % x if x >= 1e-5 else '<1e-5'))
fmt_n = lambda x: ('—' if x is None else ('%g' % round(float(x), 4)))      # 丸めない浮動小数を報告に出さない（採否表 P335〔二体目 G1〕）

# **雛形の数を正本から組み直して突き合わせる**（裁定 D112・採否表 P326）。
_src = os.path.splitext(a.template)[0] + '.src.md'
if os.path.exists(_src):
    import subprocess, tempfile as _tf, shutil as _sh
    _d = _tf.mkdtemp(prefix='tplchk_')
    try:
        _o, _l = os.path.join(_d, 't.md'), os.path.join(_d, 'l.md')
        _rc = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'build_draftB.py'), '--kind', 'template',
                              '--src', _src, '--out', _o, '--label', '報告雛形', '--lint-report', _l],
                             capture_output=True, text=True, encoding='utf-8').returncode
        if _rc == 0 and runs_B.sha16_file(_o) != runs_B.sha16_file(a.template):
            sys.exit('雛形が正本から組み直した版と違う（正本が動いた後に雛形を組み直していない・裁定 D112）: '
                     '現物 %s / 組み直し %s' % (runs_B.sha16_file(a.template), runs_B.sha16_file(_o)))
    finally:
        _sh.rmtree(_d, ignore_errors=True)
rows = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | 書式外 A／B | refuse A／B | pt 差 | 区間 | p | 様式の差 | 札 | 注 |',
        '|---|---|---|---|---|---|---|---|---|---|---|---|']
for r in A['confirm']:
    if r.get('missing'):
        rows.append('| %s | %s | — | — | — | — | — | — | — | — | %s | |' % (r['id'], r['scenario'], r['label']))
        continue
    rows.append('| %s | %s | %d/%d | %d/%d | %s／%s | %s／%s | %s | %s | %s | %s | %s | %s |'
                % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'],
                   fmt_n(r.get('ff_pt_A')), fmt_n(r.get('ff_pt_B')), fmt_n(r.get('refuse_pt_A')), fmt_n(r.get('refuse_pt_B')),
                   r['diff_pt'], r['ci'], fmt_p(r.get('p')), r.get('style_diff_pt'), r['label'],
                   '・'.join(r.get('notes') or [])))
D_conf = block(rows)
sg = A['sign_agreement']
E_sign = block(['```', (PS['sign_agreement'].format(agree=sg['agree'], confirmed=sg.get('checked')) if sg['sealed']
                        else '封印の記録が渡されていないので、予想符号との照合は行っていない。'),
                ('照合できなかった確証の対比: %s' % (sg.get('unchecked') or 'なし')) if sg['sealed'] else None,
                ('封印の欠け: %d 件' % len(sg.get('seal_missing') or [])) if sg['sealed'] else None, '```'])
F_desc = []
for fam, rs in A['descriptive'].items():
    if not rs:
        continue
    F_desc += ['**%s**' % fam, '', '| 対比 | 破局率 A | 破局率 B | pt 差 | 区間 |', '|---|---|---|---|---|']
    for r in rs:
        if r.get('missing'):
            F_desc.append('| %s | — | — | — | — |' % r['id'])
        else:
            F_desc.append('| %s | %s | %s | %s | %s |' % (r['id'], None if r['rate_A'] is None else round(r['rate_A'], 4),
                                                          None if r['rate_B'] is None else round(r['rate_B'], 4), r['diff_pt'], r['ci']))
    F_desc.append('')
F_desc.append(PS['no_p_desc'])
s4 = A['s4']
G_s4 = block(['```', '判定: %s' % s4.get('verdict'),
              ('pt 差（(6b) − ランダム方向） %s・両側の区間 %s・（ランダム方向 − (6b)）の片側上限 %s pt・効き目 %s pt・相手の腕の率 %s・区間 %s'
               % (s4.get('diff_pt'), s4.get('ci'), s4.get('upper_one_sided_pt'), s4.get('effect_pt'), fmt_n(s4.get('partner_rate')), s4.get('interval'))
               if s4.get('partner_rate') is not None else '記録が無い'),
              '封印: %s' % s4.get('sealed_prediction')] + list(s4.get('notes') or []) + ['```'])
_td = ['| 対比 | 場面 | pt 差（v − td） | 区間 | 特異性 | 向き |', '|---|---|---|---|---|---|']
for t_ in A.get('td_specificity') or []:
    _td.append('| %s | %s | %s | %s | %s | %s |' % (t_['id'], t_['scenario'], fmt_n(t_.get('diff_pt')),
                                                [fmt_n(x) for x in (t_.get('ci') or [])] or '—',
                                                {True: '書ける', False: '書かない（区間が零を含む）', None: '測れない'}[t_.get('write_specificity')],
                                                t_.get('direction') or '—'))
_hm = ['| 場面 | 腕 | 三本の率の差 pt | 測れた方向 | 注 |', '|---|---|---|---|---|']
for h_ in A.get('homogeneity') or []:
    _hm.append('| %s | %s | %s | %s | %s |' % (h_['scenario'], h_['arm'], fmt_n(h_.get('spread_pt')), h_.get('measured'),
                                           {True: '注（不均一）', False: 'なし', None: '判定しない'}[h_.get('note')]))
I_td = block(_td + [''] + _hm)
_ly = ['| 層 | n A／B | 射影の平均 A | 射影の平均 B | 平均の差 | 標準化した差 | AUC |', '|---|---|---|---|---|---|---|']
for r_ in LY.get('rows') or []:
    _ly.append('| %s | %s／%s | %s | %s | %s | %s | %s |' % (r_['layer'], r_['n_A'], r_['n_B'], fmt_n(r_.get('mean_A')), fmt_n(r_.get('mean_B')),
                                                        fmt_n(r_.get('mean_diff')), fmt_n(r_.get('smd')), fmt_n(r_.get('auc'))))
J_ly = block(['場面 %s・%s 対 %s・方向 %s（主位置から作った・単位ベクトル）。記述であり、目安も p も置かない。' % (LY['scenario'], LY['arm_A'], LY['arm_B'], LY['direction']), ''] + _ly)
H_coi = block(['```', T['selection']['coi_note'], T['publication']['dual_use'],
               '率盲検の外の経路: 同一性選別の距離／調整走行の率（選定に要る）／品質床の得点。本走行の率は整合検査まで見ない。',
               '起草者は段階 A の公開結果を見ている（封印予想の情報状態の欄に記す）。', '```'])

_state = [l for l in tpl.split('\n') if l.startswith('- 状態: **雛形**')]
if len(_state) == 1:
    tpl = tpl.replace(_state[0], '- 状態: **報告**（雛形から組み立て器が機械で組んだ・結果の欄は機械の区画）。%s'
                      % ('**合成データから組んだ検査用の報告であり、本番ではない。**' if DRY else ''))
for ph, txt in (('A', A_sum), ('B', B_run), ('C', C_gate), ('D', D_conf), ('E', E_sign), ('F', block(F_desc)), ('G', G_s4), ('H', H_coi),
                ('I', I_td), ('J', J_ly)):
    key = '〔結果 %s〕' % ph
    if key not in tpl:
        sys.exit('雛形に %s が無い' % key)
    tpl = tpl.replace(key, txt)
tpl += '\n\n## 11. 組み立ての記録（機械）\n\n- 器 `tools/build_report_B.py` %s・%s UTC。集計 `%s`（SHA16 %s）・門 `%s`（SHA16 %s）・副位置の読み `%s`（SHA16 %s）。\n' % (
    VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
    os.path.relpath(a.analysis, REPO).replace('\\', '/'), runs_B.sha16_file(a.analysis),
    os.path.relpath(a.gate, REPO).replace('\\', '/'), runs_B.sha16_file(a.gate),
    os.path.relpath(a.layers, REPO).replace('\\', '/'), runs_B.sha16_file(a.layers))
tpl += '\n'.join([MB['begin'], '- 組み立ての記録は機械が書いた（この区画の中身は区画の記録と突合する）。', MB['end']]) + '\n'
open(out_md, 'w', encoding='utf-8', newline='\n').write(tpl)
# **機械の区画の記録**（-machine.json・段階 A の型・報告の走査器が突合する・v4）
import report_lint as _RL
_RL.write_sidecar(out_md, tpl, T, 'tools/build_report_B.py %s' % VERSION)
if a.lint:
    # **報告の走査器を走らせる**（裁定 D112・採否表 P327）。前は口上が持つと書いて argparse に口が無かった。
    import subprocess
    lint = os.path.join(REPO, 'tools', 'report_lint.py')
    if not os.path.exists(lint):
        sys.exit('報告の走査器が無い: tools/report_lint.py')
    side = os.path.splitext(out_md)[0] + '-machine.json'
    cmd = [sys.executable, lint, out_md, '--contrasts', runs_B.CPATH, '--template', a.template,
           '--out', os.path.splitext(out_md)[0] + '-lint.md']      # **走査器の出力は B の置き場に置く**（既定は段階 A の置き場・v4）
    if os.path.exists(side):
        cmd += ['--sidecar', side]
    rcl = subprocess.run(cmd).returncode
    if rcl != 0:
        sys.exit('報告の走査器が違反を出した（終了コード %d）' % rcl)

print('[build_report_B] %s' % out_md)
```
