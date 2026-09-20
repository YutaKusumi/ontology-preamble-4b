# -*- coding: utf-8 -*-
"""identity_screen_B.py v3 —— 段階 B の**同一性選別の判定**（三スタックの距離・正本 `identity_screen`・裁定 D7・D143・2026-09-20）。
v3（2026-09-20・Fable 5.1 の見直し・登録者の指示）: **P421 の直しに欠陥があった**——n_ok == n を求めると、正本が認める api_error の残り（一度引き直してなお落ちた行）で止まる。行数 n == 登録の n に改め、api_error は件数を印字して分母から除くだけにした（欠けと重複は行数で捕まる）。

v2（2026-09-20・四票の採否 P418〜P421・P426〜P428・登録者裁定）:
  - **採点欠落の番人**（P418・P420）: 段階 A の `exclusive_counts` は、判定の欄が空いた試行を黙って「その他」に数える
    （破局率が下がる向き＝起草者に有利な側）。数える前に **B の読み口 `runs_B.cell_counts` にも通し**、
    採点欠落が一件でもあれば止める。行に `runs_A.COUNT_FIELDS` の欄が**キーとして**あるかも見る（`r.get` は欠けを黙って None にする）。
    二つの数え方（排他の件数と B の読み口）の n_ok・破局・refuse・書式外が食い違っても止める。
  - **二重計上の番人**（P421）: 腕ごとに `trial_id` の重複を見て止め、`n_ok` が登録の n と**等しい**ことを求める
    （前は「n 未満」だけを見ていたので、同じセルが二本あると n_ok が倍になっても通った）。
  - **コードの釘**（P419）: 段階 A の**正本と記録**だけでなく、呼んでいる**コード**（`identity_screen_A.py`・`runs_A.py`）も
    段階 A の凍結記録の SHA16 と照らす。
  - **種の照合**（P427）: 走行の manifest の種が正本 `seeds.identity_transformers` と一致するかを見る（段階 A の器と同じ型）。
    試行ごとの種の組み直しは整合検査（`integrity_B`）の仕事で、ここでは走行の種だけを見る。
  - **重みの版の印字**（P426）: B の走行の `model_rev`／`tokenizer_rev` と、段階 A の vLLM の記録に版が無いことを記録に書く。
  - **終了コードは常に 0**（P428）: 段階 A の器と同じ。合否は記録で読む——正本 `fail_reading` は「不合格でも B は実施できる」と定めており、
    非零で終わると一括で走らせる運用が止まりうる。止める条に当たったときだけ非零で終わる。

なぜ要るか: 段階 A の器 `tools/identity_screen_A.py` は凍結物で触れず、そのままでは B の登録を作れない——
  B の正本には `bases_4B2507_api`・`models`・`identity_n` が無く、段階 A の正本で走らせると比べる腕が 10・差が 30 になる（B は 11 腕・33 差・裁定 D143）。
  凍結の前の見直し（`records/B/pre-freeze-review-2026-09-20.md` (一)）で、この器が無く、開示にも載っていないことが分かった。

入力:
  - B の transformers 経路の走行 `results/<tags.identity>/`（腕ごとに一セル・場面は `identity_screen.scenario`・n は `identity_screen.n`）。
  - **API 既測**: 段階 A の正本 `design/contrasts-A.json` の `bases_4B2507_api[場面]`（腕ごとの k・refuse・format_fail・n）。
  - **vLLM**: 段階 A の門0.5 の記録 `records/A/identity-screen-A.json` の `local_counts`（腕ごとの排他の件数）。
  どちらも段階 A の凍結記録 `records/freeze-A-2026-09-16.json` の SHA16 と照らし、違えば止まる（凍結物を取り違えて読まない）。

判定（正本のとおり・手で決めない）:
  - **主判定は transformers 対 API**（段階 A §2.9 と同じ型——手元スタック対 API 既測）。`identity_screen.compared_arms` × `indicators` の
    絶対差（分母は `denominator`）を `n_differences` 個並べ、相加平均が `metric_mean_pt` 以下かつ最大が `metric_max_pt` 以下なら合格。分数で厳密に比べる。
  - 記述として、API↔vLLM と vLLM↔transformers の同じ表も印字する（正本 `stacks` の三者・`identity_screen.rate_definition`）。
  - **B の八腕に絞った平均差・最大差**も三対とも印字する（正本 `identity_screen.b_panel_note`・試行は増えない）。
  - 補助の検定は置かない——**B の正本に `aux` の登録が無い**（登録の無い統計を作らない）。
  - 判定は印字のみで、族・腕・n・閾値・帯を動かさない（`no_constant_change`）。不合格の読みは `fail_reading`。

採点の経路: 排他の件数（優先順 書式外 → refuse → 破局 → その他）は**段階 A の凍結した関数**
  `identity_screen_A.exclusive_counts` を呼ぶ（再実装しない・正本の「採点の経路は凍結した関数を呼ぶ」）。

止める条件: 走行が無い／腕が欠ける／`n_ok` が `identity_screen.n` と違う（`--allow-incomplete` は検査用）／
  **採点欠落がある**（`--allow-scoring-gap` は検査用）／**行に登録の欄が無い**／**二つの数え方が食い違う**／**`trial_id` が重複する**／
  **走行の種が登録と違う**（`--allow-seed-mismatch` は検査用）／
  段階 A の正本・記録・**コード**の SHA16 が凍結記録と違う／比べる腕が API 既測か vLLM の記録に無い。
出力: records/B/identity-screen-B.{json,md}（`--force` が無ければ上書きしない）。
用法: python tools/identity_screen_B.py [--tag idB] [--root <results の代わり>] [--allow-dry] [--force] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B
import identity_screen_A as ISA          # 凍結物（段階 A）——排他の件数の関数だけを使う

VERSION = 'v3'
REPO = runs_B.REPO
A_CANON = os.path.join(REPO, 'design', 'contrasts-A.json')
A_RECORD = os.path.join(REPO, 'records', 'A', 'identity-screen-A.json')
A_FREEZE = os.path.join(REPO, 'records', 'freeze-A-2026-09-16.json')
# **呼んでいるコードも釘で留める**（P419・2026-09-20）——データだけ照らしてコードを照らさない穴があった
A_TOOL = os.path.join(REPO, 'tools', 'identity_screen_A.py')
A_RUNS = os.path.join(REPO, 'tools', 'runs_A.py')
PINNED = (A_CANON, A_RECORD, A_TOOL, A_RUNS)
IND_LOCAL = {'catastrophe': 'catastrophe', 'refuse': 'refuse', 'format_fail': 'format_out'}   # 排他の件数の欄
IND_API = {'catastrophe': 'k', 'refuse': 'refuse', 'format_fail': 'format_fail'}              # 段階 A の正本の欄
PAIRS = (('transformers', 'API'), ('API', 'vLLM'), ('vLLM', 'transformers'))
MAIN_PAIR = PAIRS[0]                     # 主判定の対（手元スタック 対 API 既測・段階 A の型）


def check_pin(path, freeze_files):
    """段階 A の凍結記録に載る SHA16 と現物を照らす（載っていなければその旨を返す）。"""
    rel = os.path.relpath(path, REPO).replace('\\', '/')
    want = freeze_files.get(rel)
    got = runs_B.sha16_file(path)
    return {'path': rel, 'sha16': got, 'frozen_sha16': want, 'match': (want == got) if want else None}


def local_counts(idx, key, arms):
    """走行の索引から腕ごとの排他の件数を足し合わせ、**番人の材料**も集める（v2・P418〜P421・P426・P427）。

    戻り: (排他の件数, 走行キー, dry の印, 欠けた腕, 番人の材料)。
    番人の材料は {'cross': B の読み口の件数, 'dup_ids': 重複した trial_id の数, 'field_missing': 欄の欠け,
                 'seeds': 走行の種, 'revs': 重みとトークナイザの版}。
    """
    out, run_keys, marks = {}, [], []
    cross, ids_by_arm, field_missing, seeds, revs = {}, {}, [], {}, {}
    need_fields = set(ISA.runs_A.COUNT_FIELDS)           # 段階 A の器が読む欄（手で写さない）
    for rec in idx.get(key) or []:
        run_keys.append(rec['run_key'])
        marks += list(rec.get('dry_marks') or [])
        m = rec['manifest']
        seeds[rec['run_key']] = m.get('seed')
        revs[rec['run_key']] = {'model': m.get('model'), 'model_rev': m.get('model_rev'), 'tokenizer_rev': m.get('tokenizer_rev')}
        for arm, c in ISA.exclusive_counts(rec['trials_path']).items():
            acc = out.setdefault(arm, dict(n=0, n_ok=0, format_out=0, refuse=0, catastrophe=0, other=0))
            for k in acc:
                acc[k] += c[k]
        # **B の読み口でも数える**（採点欠落と数え方の食い違いを見る・P418）
        for arm, c in runs_B.cell_counts(rec['trials_path'], phase='identity').items():
            a2 = cross.setdefault(arm, {})
            for k, v in c.items():
                if isinstance(v, (int, float)):
                    a2[k] = a2.get(k, 0) + v
        # **行の欄がキーとしてあるか**（`r.get` は欠けを黙って None にする・P420）と **trial_id の重複**（P421）
        for r in runs_B.iter_jsonl(rec['trials_path']):
            ids_by_arm.setdefault(r.get('arm'), []).append(r.get('trial_id'))
            miss = sorted(need_fields - set(r))
            if miss:
                field_missing.append({'run_key': rec['run_key'], 'arm': r.get('arm'), 'trial_id': r.get('trial_id'), 'missing': miss})
    dup = {a: len(v) - len(set(v)) for a, v in ids_by_arm.items() if len(v) != len(set(v))}
    missing = [a for a in arms if a not in out]
    return out, sorted(set(run_keys)), sorted(set(marks)), missing, {
        'cross': cross, 'dup_ids': dup, 'field_missing': field_missing, 'seeds': seeds, 'revs': revs}


def guards(EX, G, arms, n_registered):
    """番人（P418〜P421）。止める理由の一覧と、止めない注の一覧を返す。"""
    stops, notes = [], []
    if G['field_missing']:
        stops.append('行に段階 A の器が読む欄が無い（%d 件・先頭 %s の %s）'
                     % (len(G['field_missing']), G['field_missing'][0]['trial_id'], '・'.join(G['field_missing'][0]['missing'])))
    if G['dup_ids']:
        stops.append('trial_id が重複している（腕ごとの重複数 %s）——同じセルを二重に数えている'
                     % '・'.join('%s %d' % kv for kv in sorted(G['dup_ids'].items())))
    for arm in arms:
        a, b = EX.get(arm) or {}, (G['cross'].get(arm) or {})
        if not a or not b:
            continue
        if a['n'] != b.get('n') or a['n_ok'] != b.get('n_ok'):
            stops.append('%s: 二つの数え方で n／n_ok が違う（排他 %d／%d・B の読み口 %s／%s）'
                         % (arm, a['n'], a['n_ok'], b.get('n'), b.get('n_ok')))
        if a['format_out'] + a['refuse'] + a['catastrophe'] + a['other'] != a['n_ok']:
            stops.append('%s: 排他の四区分の和が n_ok と合わない' % arm)
        if b.get('scoring_gap'):
            stops.append('%s: **採点欠落が %d 件**（判定の欄が空いた試行。段階 A の器はこれを「その他」に数えるので、破局率が下がる向きに黙って倒れる）'
                         % (arm, b['scoring_gap']))
        for k_ex, k_cc, name in (('catastrophe', 'cat', '破局'), ('refuse', 'refuse', 'refuse'), ('format_out', 'ff', '書式外')):
            if a[k_ex] != b.get(k_cc):
                notes.append('%s: %s の件数が二つの数え方で違う（排他 %d・B の読み口 %s）——区分の重なり（書式外かつ refuse など）'
                             % (arm, name, a[k_ex], b.get(k_cc)))
    return stops, notes


def rates(counts_by_arm, kind):
    """腕 → 指標 → (分子, 分母)。kind は 'local'（排他の件数）か 'api'（段階 A の正本の既測）。"""
    M, out = (IND_LOCAL, 'n_ok') if kind == 'local' else (IND_API, 'n')
    R = {}
    for arm, c in counts_by_arm.items():
        R[arm] = {ind: (c[M[ind]], c[out]) for ind in M}
    return R


def pair_diffs(X, Y, arms, indicators):
    """同じ腕 × 同じ指標の絶対差（pt・分数で厳密に）。"""
    D = []
    for arm in arms:
        for ind in indicators:
            xk, xn = X[arm][ind]
            yk, yn = Y[arm][ind]
            d = abs(Fraction(xk, xn) - Fraction(yk, yn)) * 100
            D.append({'arm': arm, 'indicator': ind, 'a': [xk, xn], 'b': [yk, yn], 'abs_diff_pt': d})
    return D


def summarize(D, arms=None):
    """平均と最大（腕を絞ることもできる）。"""
    xs = [x['abs_diff_pt'] for x in D if arms is None or x['arm'] in arms]
    if not xs:
        return {'n': 0, 'mean_pt': None, 'max_pt': None}
    return {'n': len(xs), 'mean_pt': float(sum(xs) / len(xs)), 'max_pt': float(max(xs))}


def verdict_of(D, mean_pt, max_pt):
    """相加平均が mean_pt 以下**かつ**最大が max_pt 以下で合格（分数のまま比べる・境目は合格）。"""
    mean = sum(x['abs_diff_pt'] for x in D) / len(D)
    mx = max(x['abs_diff_pt'] for x in D)
    return ('pass' if (mean <= Fraction(mean_pt) and mx <= Fraction(max_pt)) else 'fail'), mean, mx


def _selftest():
    import tempfile, shutil
    T = runs_B.load_T()
    S = T['identity_screen']
    arms, inds = S['compared_arms'], S['indicators']
    # (1) 差の数が正本の登録と合う
    mk = lambda v: {a: {i: (v, 100) for i in inds} for a in S['arms_run']}
    D = pair_diffs(mk(10), mk(10), arms, inds)
    assert len(D) == S['n_differences'], (len(D), S['n_differences'])
    assert summarize(D)['max_pt'] == 0.0
    # (2) 境目は合格・わずかに超えたら不合格（平均の側と最大の側の両方）
    X, Y = mk(10), mk(10)
    for a in arms:
        X[a]['catastrophe'] = (10 + S['metric_max_pt'], 100)                       # 一腕だけ最大ちょうど
    v, mean, mx = verdict_of(pair_diffs(X, Y, arms, inds), S['metric_mean_pt'], S['metric_max_pt'])
    assert v == 'pass' and mx == S['metric_max_pt'], (v, float(mx))
    for a in arms:
        X[a]['catastrophe'] = (10 + S['metric_max_pt'], 100)
    X[arms[0]]['catastrophe'] = (10 + S['metric_max_pt'] + 1, 100)                 # 最大を一つ超える
    v2, _, _ = verdict_of(pair_diffs(X, Y, arms, inds), S['metric_mean_pt'], S['metric_max_pt'])
    assert v2 == 'fail', v2
    Z = mk(10)
    for a in arms:                                                                 # 平均ちょうど（全差が平均の閾値）
        for i in inds:
            Z[a][i] = (10 + S['metric_mean_pt'], 100)
    v3, mean3, _ = verdict_of(pair_diffs(Z, Y, arms, inds), S['metric_mean_pt'], S['metric_max_pt'])
    assert v3 == 'pass' and mean3 == S['metric_mean_pt'], (v3, float(mean3))
    Z[arms[0]]['catastrophe'] = (10 + S['metric_max_pt'], 100)                     # 平均だけを超えさせる（この差は最大の閾値ちょうど）
    v4, mean4, mx4 = verdict_of(pair_diffs(Z, Y, arms, inds), S['metric_mean_pt'], S['metric_max_pt'])
    assert mx4 <= S['metric_max_pt'] and mean4 > S['metric_mean_pt'] and v4 == 'fail', (float(mean4), float(mx4), v4)
    # (3) B の八腕に絞った要約は、腕の数 × 指標の数になる
    sub = summarize(pair_diffs(mk(10), mk(20), arms, inds), set(T['arms']['panel']))
    assert sub['n'] == len(set(T['arms']['panel']) & set(arms)) * len(inds) == 24, sub
    assert abs(sub['mean_pt'] - 10.0) < 1e-12 and abs(sub['max_pt'] - 10.0) < 1e-12, sub
    # (4) 排他の件数は段階 A の凍結した関数が数える（優先順 書式外 → refuse → 破局 → その他）
    d = tempfile.mkdtemp()
    try:
        p = os.path.join(d, 'trials-x.jsonl')
        rows = [{'arm': 'O', 'status': 'ok', 'format_fail': True, 'choice': 'refuse', 'catastrophe': True},    # 書式外が最優先
                {'arm': 'O', 'status': 'ok', 'format_fail': False, 'choice': 'refuse', 'catastrophe': True},   # refuse が破局に優先
                {'arm': 'O', 'status': 'ok', 'format_fail': False, 'choice': 'a', 'catastrophe': True},
                {'arm': 'O', 'status': 'ok', 'format_fail': False, 'choice': 'a', 'catastrophe': False},
                {'arm': 'O', 'status': 'api_error', 'format_fail': False, 'choice': None, 'catastrophe': None}]
        open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(json.dumps(r) for r in rows) + '\n')
        EX = ISA.exclusive_counts(p)['O']
        assert (EX['n'], EX['n_ok'], EX['format_out'], EX['refuse'], EX['catastrophe'], EX['other']) == (5, 4, 1, 1, 1, 1), EX
        R = rates({'O': EX}, 'local')['O']
        assert R['catastrophe'] == (1, 4) and R['refuse'] == (1, 4) and R['format_fail'] == (1, 4), R
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # (5) 段階 A の入力は凍結記録に載り、現物と一致する
    FF = runs_B.read_json(A_FREEZE)['files']
    for p in (A_CANON, A_RECORD):
        pin = check_pin(p, FF)
        assert pin['match'] is True, pin
    # (6) 比べる腕が API 既測にも vLLM の記録にもそろっている
    AB = runs_B.read_json(A_CANON)['bases_4B2507_api'][S['scenario']]
    AR = runs_B.read_json(A_RECORD)['local_counts']
    assert not [a for a in arms if a not in AB], [a for a in arms if a not in AB]
    assert not [a for a in arms if a not in AR], [a for a in arms if a not in AR]
    # (7) 段階 A の記録の判定を、この器の関数で組み直すと段階 A の値と一致する（同じ型であることの確かめ）
    dA = pair_diffs(rates({a: AR[a] for a in json.load(open(A_CANON, encoding='utf-8'))['identity_screen']['compared_arms']}, 'local'),
                    rates({a: AB[a] for a in json.load(open(A_CANON, encoding='utf-8'))['identity_screen']['compared_arms']}, 'api'),
                    json.load(open(A_CANON, encoding='utf-8'))['identity_screen']['compared_arms'], inds)
    RA = runs_B.read_json(A_RECORD)
    s = summarize(dA)
    assert abs(s['mean_pt'] - RA['mean_abs_diff_pt']) < 1e-9 and abs(s['max_pt'] - RA['max_abs_diff_pt']) < 1e-9, (s, RA['mean_abs_diff_pt'], RA['max_abs_diff_pt'])
    # (7-b) 分母の登録が器の使う欄と合う（正本が分母を変えたら、器が気づく）
    assert S['denominator'] == 'n_ok', S['denominator']
    # (7-c) 比べる腕の **API 既測の出所**が、B の正本の登録と一致する（段階 A の既測の `src` と `compared_sources`）
    _src_bad = [(x, AB[x].get('src'), S['compared_sources'].get(x)) for x in arms if AB[x].get('src') != S['compared_sources'].get(x)]
    assert not _src_bad, _src_bad
    # (7-d) API 既測の欄がそろっている（欠けると率が作れない）
    _lack = [(x, k) for x in arms for k in IND_API.values() if k not in AB[x]] + [(x, 'n') for x in arms if 'n' not in AB[x]]
    assert not _lack, _lack
    # (10) **番人が発火する**（採点欠落・欄の欠け・trial_id の重複・v2・P418〜P421）
    d2 = tempfile.mkdtemp()
    try:
        run = os.path.join(d2, T['tags']['identity'], '%s__transformers__O__x' % T['tags']['identity'])
        os.makedirs(run)
        json.dump({'tag': T['tags']['identity'], 'stack': 'transformers', 'scenario': S['scenario'], 'arm': 'O',
                   'seed': T['seeds']['identity_transformers'], 'model': 'stub/dry-run', 'dry_run': True},
                  open(os.path.join(run, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        base = {'trial_id': 't1', 'arm': 'O', 'scenario': S['scenario'], 'status': 'ok', 'catastrophe': True,
                'choice': 'a', 'format_fail': False, 'loop_flag': False, 'truncated': False,
                'style_a': False, 'style_b': True, 'mention': False, 'correct': None, 'seed': 1, 'dry_run': True}
        rows = [dict(base),
                dict(base, trial_id='t2', catastrophe=None),                                   # 採点欠落（選択は読めた）
                dict(base, trial_id='t1'),                                                     # trial_id の重複
                {k: v for k, v in dict(base, trial_id='t4').items() if k != 'format_fail'}]    # 欄の欠け
        with open(os.path.join(run, 'trials-x.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        _idx = runs_B.index_runs(T, T['tags']['identity'], d2, allow_dry=True)
        EXx, _rk, _mk, _ms, Gx = local_counts(_idx, ('transformers', S['scenario']), ['O'])
        st, _nt = guards(EXx, Gx, ['O'], S['n'])
        assert any('採点欠落' in x for x in st), st
        assert any('重複' in x for x in st), st
        assert any('欄が無い' in x for x in st), st
        assert Gx['seeds'][os.path.basename(run)] == T['seeds']['identity_transformers'], Gx['seeds']
    finally:
        shutil.rmtree(d2, ignore_errors=True)
    # (8) 主判定の対と三スタックの組が、正本の登録と合う（器の中の並びを正本から離さない）
    assert ('主判定は %s 対 %s' % MAIN_PAIR) in S['verdict_pair'].replace('**', ''), (MAIN_PAIR, S['verdict_pair'][:80])
    assert set(x for p in PAIRS for x in p) == set(S['stacks']), (PAIRS, S['stacks'])
    assert len(PAIRS) == len(S['stacks']), (PAIRS, S['stacks'])
    print('[identity_screen_B selftest] 差の数 %d・境目の四通り（平均と最大の合否）・八腕の部分集合・'
          '排他の件数（凍結した関数）・段階 A の入力の釘（正本・記録・コード）・腕の突合と既測の欄・分母と出所の登録の一致・番人の発火（採点欠落・欄・重複）・主判定の対と正本の登録の一致・段階 A の判定の組み直し（平均 %.3f pt・最大 %.3f pt）—— すべて通った'
          % (S['n_differences'], s['mean_pt'], s['max_pt']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--tag', default=None)
    ap.add_argument('--root', default=None)
    ap.add_argument('--contrasts', default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--allow-incomplete', action='store_true', help='検査用の口（n_ok が登録の n に満たなくても書く・印を残す）')
    ap.add_argument('--allow-dry', action='store_true', help='検査用の口（dry-run の走行を読む・印を残す）')
    ap.add_argument('--allow-scoring-gap', action='store_true', help='検査用の口（採点欠落があっても書く・印を残す・P418）')
    ap.add_argument('--allow-seed-mismatch', action='store_true', help='検査用の口（走行の種が登録と違っても書く・印を残す・P427）')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    T = runs_B.load_T(a.contrasts)
    S = T['identity_screen']
    if S['denominator'] != 'n_ok':
        sys.exit('正本の分母の登録が変わった（器は n_ok で率を作る）: %s' % S['denominator'])
    tag = a.tag or T['tags']['identity']
    OUT = a.out or os.path.join(REPO, 'records', 'B', 'identity-screen-B')
    if (os.path.exists(OUT + '.json') or os.path.exists(OUT + '.md')) and not a.force:
        sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUT)
    # 段階 A の入力の釘（凍結記録と照らす）
    FF = runs_B.read_json(A_FREEZE)['files']
    PINS = [check_pin(p, FF) for p in PINNED]        # 正本・記録・**コード**（P419）
    bad = [p for p in PINS if p['match'] is not True]
    if bad:
        sys.exit('段階 A の入力が凍結記録と合わない（読まない）: %s' % '・'.join('%s（記録 %s・現物 %s）' % (p['path'], p['frozen_sha16'], p['sha16']) for p in bad))
    TA = runs_B.read_json(A_CANON)
    RA = runs_B.read_json(A_RECORD)
    API = {a_: TA['bases_4B2507_api'][S['scenario']][a_] for a_ in S['compared_arms'] if a_ in TA['bases_4B2507_api'][S['scenario']]}
    VLLM = {a_: RA['local_counts'][a_] for a_ in S['compared_arms'] if a_ in RA['local_counts']}
    lack = [a_ for a_ in S['compared_arms'] if a_ not in API or a_ not in VLLM]
    if lack:
        sys.exit('比べる腕が段階 A の既測にない: %s' % '・'.join(lack))
    # B の走行（transformers）
    try:
        idx = runs_B.index_runs(T, tag, a.root, allow_dry=a.allow_dry)
    except RuntimeError as ex:
        sys.exit('読み出しで止まった（%s）' % ex)
    key = ('transformers', S['scenario'])
    EX, RUN_KEYS, MARKS, missing, G = local_counts(idx, key, S['arms_run'])
    if not RUN_KEYS:
        sys.exit('同一性選別の走行が無い: %s × %s（tag %s）%s'
                 % (key[0], key[1], tag, '' if not idx else '（ある鍵: %s）' % '・'.join(map(str, idx))))
    if missing:
        sys.exit('走行に腕が欠けている（登録は `identity_screen.arms_run` の %d 腕）: %s' % (len(S['arms_run']), '・'.join(missing)))
    # **番人**（P418〜P421）——採点欠落・欄の欠け・数え方の食い違い・trial_id の重複
    STOPS, NOTES = guards(EX, G, S['arms_run'], S['n'])
    gap_only = [s for s in STOPS if '採点欠落' in s]
    hard = [s for s in STOPS if s not in gap_only]
    if hard:
        sys.exit('番人が止めた（数え方・欄・重複）:\n  ' + '\n  '.join(hard))
    if gap_only and not a.allow_scoring_gap:
        sys.exit('番人が止めた（採点欠落・検査用の口は --allow-scoring-gap）:\n  ' + '\n  '.join(gap_only))
    # **n_ok は登録の n と等しいことを求める**（P421・前は「n 未満」だけを見ていた）
    # **行数 n が登録の n と等しいことを求める**（P421・v3 で n_ok から行数に改めた——Fable 5.1 の見直し）。
    # 正本は「例外で落ちたバッチは一度だけ引き直し、なお落ちればその行を api_error にする」と登録し、率の分母は n_ok（api_error を除く）である。
    # v2 は n_ok == n を求めたので、正本が認める api_error の残りで止まり、検査用の口（印が残り、報告の組み立て器が拒む）しか道が無かった。
    # 行数で見れば、欠け（少ない）と重複（多い）はそのまま捕まり、api_error は件数を印字して分母から除くだけになる。
    off = [(arm, EX[arm]['n']) for arm in S['arms_run'] if EX[arm]['n'] != S['n']]
    short = [arm for arm, _ in off]
    api_err = {arm: EX[arm]['n'] - EX[arm]['n_ok'] for arm in S['arms_run'] if EX[arm]['n'] != EX[arm]['n_ok']}
    if off and not a.allow_incomplete:
        sys.exit('行数が登録の n（%d）と違う腕（%s）——少なければ走行の欠け、多ければ走行の重複を疑う。検査用の口は --allow-incomplete'
                 % (S['n'], '・'.join('%s %d' % x for x in off)))
    # **走行の種の照合**（P427・段階 A の器と同じ型。試行ごとの種の組み直しは整合検査の仕事）
    want_seed = T['seeds']['identity_transformers']
    seed_bad = {rk: sd for rk, sd in G['seeds'].items() if sd != want_seed}
    if seed_bad and not a.allow_seed_mismatch:
        sys.exit('走行の種が正本 `seeds.identity_transformers`（%s）と違う: %s。検査用の口は --allow-seed-mismatch'
                 % (want_seed, '・'.join('%s→%s' % kv for kv in sorted(seed_bad.items()))))
    # 三スタックの率
    RATES = {'transformers': rates({a_: EX[a_] for a_ in S['compared_arms']}, 'local'),
             'vLLM': rates(VLLM, 'local'), 'API': rates(API, 'api')}
    B_PANEL = set(T['arms']['panel'])
    TABLES = {}
    for x, y in PAIRS:
        D = pair_diffs(RATES[x], RATES[y], S['compared_arms'], S['indicators'])
        TABLES['%s~%s' % (x, y)] = {'pair': [x, y], 'diffs': [dict(d, abs_diff_pt=float(d['abs_diff_pt'])) for d in D],
                                    'all': summarize(D), 'b_panel': summarize(D, B_PANEL)}
    MD = pair_diffs(RATES[MAIN_PAIR[0]], RATES[MAIN_PAIR[1]], S['compared_arms'], S['indicators'])
    assert len(MD) == S['n_differences'], (len(MD), S['n_differences'])
    verdict, mean, mx = verdict_of(MD, S['metric_mean_pt'], S['metric_max_pt'])
    marks = MARKS + [x for x, on in (('allow_incomplete', bool(off)), ('allow_dry', a.allow_dry),
                                     ('allow_scoring_gap', bool(gap_only)), ('allow_seed_mismatch', bool(seed_bad))) if on]
    R = {'kind': 'identity_screen_B', 'version': VERSION,
         'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
         'tag': tag, 'root': a.root, 'run_keys': RUN_KEYS, 'stacks': S['stacks'], 'main_pair': list(MAIN_PAIR),
         'contrasts_sha16': runs_B.sha16_file(a.contrasts or runs_B.CPATH), 'stage_A_inputs': PINS, 'dev_marks': sorted(set(marks)),
         'verdict': verdict, 'mean_abs_diff_pt': float(mean), 'max_abs_diff_pt': float(mx),
         'mean_pt': S['metric_mean_pt'], 'max_pt': S['metric_max_pt'], 'n_differences': len(MD),
         'tables': TABLES, 'local_counts': EX, 'short_arms': short, 'n_off': dict(off), 'api_error': api_err,
         'guards': {'stops_bypassed': gap_only, 'notes': NOTES, 'scoring_gap': {k: v.get('scoring_gap', 0) for k, v in G['cross'].items()},
                    'duplicate_trial_ids': G['dup_ids'], 'field_missing': G['field_missing'][:20], 'field_missing_total': len(G['field_missing'])},
         'seeds': {'registered': want_seed, 'by_run': G['seeds'], 'mismatch': seed_bad},
         'model_revs': {'B_runs': G['revs'],
                        'stage_A_vLLM': {'model': RA.get('model'), 'rev': '未照合（段階 A の門0.5 の記録に版が無い）'}},
         'b_panel_note': S['b_panel_note'], 'fail_reading': S['fail_reading'], 'no_constant_change': TA['identity_screen']['no_constant_change'],
         'aux_note': '補助の検定は置かない（B の正本 `identity_screen` に `aux` の登録が無い）',
         'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(R, open(OUT + '.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    M = ['# 段階 B 同一性選別（機械生成・`tools/identity_screen_B.py` %s・%s UTC）' % (VERSION, R['generated_utc']), '',
         '- 走行 %s（tag %s）・正本 SHA16 %s・検査用の印 %s' % ('・'.join(RUN_KEYS), tag, R['contrasts_sha16'], '・'.join(R['dev_marks']) or 'なし'),
         '- 段階 A の入力（凍結記録と照合済み）: %s' % '・'.join('`%s` %s' % (p['path'], p['sha16']) for p in PINS),
         '- **主判定（%s 対 %s）: %s**（%d 個の絶対差の相加平均 %.3f pt〔閾値 %s 以下〕・最大 %.3f pt〔閾値 %s 以下〕）'
         % (MAIN_PAIR[0], MAIN_PAIR[1], '合格' if verdict == 'pass' else '不合格', len(MD), float(mean), S['metric_mean_pt'], float(mx), S['metric_max_pt']),
         '- 不合格のときの読み: %s' % S['fail_reading'], '- %s' % R['no_constant_change'], '- %s' % R['aux_note'],
         '- **番人**（採点欠落・欄・数え方・重複・種）: 止めたもの %d 件（検査用の口で通したもの %d 件）・注 %d 件。'
         '採点欠落の合計 %d 件・重複 %d 腕・欄の欠け %d 件・種の不一致 %d 走行・**api_error の残り %d 件**（分母 n_ok から除く・正本の登録どおり）'
         % (0, len(gap_only), len(NOTES), sum((v.get('scoring_gap') or 0) for v in G['cross'].values()),
            len(G['dup_ids']), len(G['field_missing']), len(seed_bad), sum(api_err.values())),
         '- 重みの版: B の走行 %s／段階 A の vLLM は**未照合**（門0.5 の記録に版が無い・機種は %s）'
         % ('・'.join(sorted({str(v.get('model_rev')) for v in G['revs'].values()})) or '（無い）', RA.get('model')), '',
         '## 三スタックの距離（記述・主判定は上の一対）', '', '| 対 | 差の数 | 平均（pt） | 最大（pt） | B の八腕の平均 | B の八腕の最大 |', '|---|---|---|---|---|---|']
    for k, t in TABLES.items():
        M.append('| %s | %d | %.3f | %.3f | %.3f | %.3f |' % (k, t['all']['n'], t['all']['mean_pt'], t['all']['max_pt'],
                                                              t['b_panel']['mean_pt'], t['b_panel']['max_pt']))
    M += ['', '## 主判定の内訳（%s 対 %s）' % MAIN_PAIR, '', '| 腕 | 指標 | %s | %s | 絶対差（pt） |' % MAIN_PAIR, '|---|---|---|---|---|']
    M += ['| %s | %s | %d/%d | %d/%d | %.3f |' % (x['arm'], x['indicator'], x['a'][0], x['a'][1], x['b'][0], x['b'][1], float(x['abs_diff_pt'])) for x in MD]
    M += ['', '## 腕ごとの手元の件数（transformers・排他——書式外 → refuse → 破局 → その他）', '',
          '| 腕 | n | n_ok | 書式外 | refuse | 破局 | その他 |', '|---|---|---|---|---|---|---|']
    M += ['| %s | %d | %d | %d | %d | %d | %d |' % (arm, EX[arm]['n'], EX[arm]['n_ok'], EX[arm]['format_out'], EX[arm]['refuse'],
                                                    EX[arm]['catastrophe'], EX[arm]['other']) for arm in S['arms_run']]
    M += ['', '- %s' % S['b_panel_note'], '', R['clause'], '']
    open(OUT + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M))
    print('[identity_screen_B] %s（平均 %.3f pt・最大 %.3f pt）written %s.{json,md}' % (verdict, float(mean), float(mx), OUT))
    # **合否で終了コードを分けない**（P428・段階 A の器と同じ）。正本 `fail_reading` は「不合格でも B は実施できる」と定めており、
    # 非零で終わると一括で走らせる運用が止まりうる。止める条に当たったときだけ、上の sys.exit が非零で終わる。
    sys.exit(0)
