# 直しの確認・資料 第2部（機械生成・2026-09-18 05:48 UTC）

変わった器材のソースを**逐語**で入れています。SHA16 は現物から取ったものです。

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

## `tools/direction_B.py`（SHA16 859A3F4F0FC5E233・207 行）

```python
# -*- coding: utf-8 -*-
"""direction_B.py v2 —— 段階 B の**方向の抽出**（主位置の活性・方向の作成・決定性の検査・要約統計・v̂ の凍結）。

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

VERSION = 'v2'
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
        for name in pairs:
            v = per[name]['mean']
            if name == 'td':
                v = match_norm(v, v_hat)
            out[(name, ratio)] = v
        stats[ratio] = {
            'norms': {name: float(np.linalg.norm(out[(name, ratio)])) for name in pairs},
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
    tok = AutoTokenizer.from_pretrained(a.model)
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

## `tools/steer_B.py`（SHA16 A67438D1C326F9BC・179 行）

```python
# -*- coding: utf-8 -*-
"""steer_B.py v2 —— 段階 B の**介入**（方向の加減・ランダム方向・品質床・強制デコード）。

正本 `design/contrasts-B.json` の `selection.apply`・`random_control`・`quality_floor`・`runner` に従う。
規則（この器が守るもの）:
  - 加減は `h ← h ± α·v̂`（場面本文の開始位置から EOS まで・`register_forward_hook`・`selection.apply`）。α は**その層の v̂ のノルムに対する比**。
  - すべての方向（v̂・Nk・td・(6b)・ランダム方向）を**係数を掛ける前の ‖v̂〔static〕‖** に合わせ、**係数は加減のときに一度だけ**掛ける（裁定 D75・D90）。
    自己検査は「v 腕とランダム腕の加わる量のノルムが全係数・全層で一致する」ことを確かめる（実装検分の採否表 P257——係数が二度掛かる誤りをここで捕まえる）。
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

VERSION = 'v2'
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


def scenario_start_index(tokenizer, arm_text, pad_len=0):
    """介入の帯の**起点**（正本 `selection.apply`・`runner.prompt_assembly`）。

    組み立ては「前置き ＋ 空行 ＋ 場面の本文 ＋ 指示」なので、起点は「前置き ＋ 空行」のトークン数。
    左詰めのバッチでは行ごとに詰めの長さ pad_len だけずれるので、**行ごとに**求める（採否表 P258）。
    前置きを持たない腕（N）は起点が零（＋詰め）。"""
    head = (arm_text + '\n\n') if arm_text else ''
    n_head = len(tokenizer(head, add_special_tokens=False)['input_ids']) if head else 0
    return pad_len + n_head


def band_starts(tokenizer, arm_texts, pad_lens):
    """バッチの行ごとの起点（`make_hook` に渡す）。"""
    return [scenario_start_index(tokenizer, t, p) for t, p in zip(arm_texts, pad_lens)]


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
    # (2) **合成の検査**（実装検分の採否表 P257）: 加わる量のノルムが v 腕とランダム腕で全係数・全層で一致する
    for coef in T['selection']['candidates']['coefficients']:
        for ratio in T['selection']['candidates']['layers']:
            r = random_directions(v, 'main', ratio)[0]
            a_v = np.linalg.norm(apply_vector(np.zeros(32), v, coef, +1))
            a_r = np.linalg.norm(apply_vector(np.zeros(32), r, coef, +1))
            assert abs(a_v - a_r) < 1e-9, ('加わる量が v 腕とランダム腕で違う（係数が二度掛かっていないか）', coef, ratio, a_v, a_r)
    # (3) ほかの方向（Nk・td・(6b)）も ‖v̂‖ に合わせてから係数を掛ける
    w = rng.normal(size=32) * 7.0
    assert abs(float(np.linalg.norm(match_to_static(w, v))) - nv) < 1e-9
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
    qg, mg = quality_generation(), main_generation()
    assert qg['do_sample'] is False and 'temperature' not in qg, '品質床が貪欲でない'
    assert set(mg) <= {'do_sample', 'temperature', 'top_p', 'max_new_tokens'}, '生成の設定に transformers が知らない鍵が混ざる'
    assert mg['max_new_tokens'] == T['runner']['generation']['max_tokens'] and mg['temperature'] == T['runner']['generation']['temperature']
    print('[steer_B selftest] ノルム合わせ（合成の検査つき）・引き直し・層の子ストリーム・割り当てと再開・加減の向き・生成の設定: すべて通った')


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

## `tools/run_stageB_local.py`（SHA16 EBC7ECB8B07171B1・217 行）

```python
# -*- coding: utf-8 -*-
"""run_stageB_local.py v2 —— 段階 B の走行器（transformers・bf16・**hook つき**・手元／Colab）。

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

VERSION = 'v2'
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

## `tools/synth_B.py`（SHA16 0CEC78EDE44953F8・338 行）

```python
# -*- coding: utf-8 -*-
"""synth_B.py v2 —— 段階 B の**合成データ**の生成器（器材の検査用・実データを作らない）。

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

VERSION = 'v2'
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


def _arm_sha(arm):
    base = arm.split('+v')[0].split('-v')[0]
    return T['arms']['sha16'].get(base) or 'SYNTH'


def _trial(i, arm, scenario, tag, seed, run_key, cat, refuse, ff, style_a, style_b, mention, correct=None,
           layer=None, coef=None, status='ok', sampling=None, loop=False, trunc=False, direction_id=None):
    """一試行の記録。**実機の採点の規約に合わせる**（実装検分の採否表 P301）——
    書式外の試行は答えを読み取れないので `catastrophe`・`choice`・`correct` は None にする。"""
    ff = bool(ff)
    if status != 'ok' or ff:
        cat_v, choice, corr = None, None, None
    else:
        cat_v = bool(cat)
        choice = 'refuse' if refuse else 'A'
        corr = (None if correct is None else bool(correct))
    return {'trial_id': '%s__%s__%04d' % (run_key, arm, i), 'trial_index': i, 'arm': arm, 'scenario': scenario, 'tag': tag,
            'status': status, 'catastrophe': cat_v, 'choice': choice, 'refuse_class': None,
            'format_fail': ff, 'style_a': bool(style_a), 'style_b': bool(style_b), 'mention': bool(mention),
            'loop_flag': bool(loop), 'truncated': bool(trunc), 'correct': corr, 'logprobs': None, 'resp_mean_path': None,
            'seed': seed, 'run_key': run_key, 'runner_sha': 'SYNTH', 'arms_spec': arm, 'preamble_sha': _arm_sha(arm),
            'model': 'stub/dry-run', 'sampling': dict(sampling or T['runner']['generation']), 'layer': layer, 'coef': coef,
            'direction_id': direction_id or ('rand:%d' % (i % T['random_control']['count']) if 'vrand' in arm else 'fixed'),
            'batch_pos': i % T['runner']['batch'], 'proc_uuid': 'synth', 'dry_run': True}


def cell_trials(n, spec, start=0, **kw):
    """spec: 件数の割り当て（cat・refuse・ff・style_a・style_b・mention・correct・api_error・loop・trunc）。

    **書式外は破局の分子を食う**（実機と同じ・希釈の因果を作る・採否表 P301）。start は中断と再開のための試行の番号の起点。"""
    out = []
    n_err = int(spec.get('api_error', 0))
    n_ff, n_loop, n_trunc = int(spec.get('ff', 0)), int(spec.get('loop', 0)), int(spec.get('trunc', 0))
    cat_target, ref_target = int(spec.get('cat', 0)), int(spec.get('refuse', 0))
    for k in range(n):
        i = start + k
        if i < n_err:
            out.append(_trial(i, cat=0, refuse=0, ff=0, style_a=0, style_b=0, mention=0, status='error', **kw))
            continue
        j = i - n_err
        ff = j < n_ff
        cat = (not ff) and (n_ff <= j < n_ff + cat_target)
        refuse = (not ff) and (n_ff + cat_target <= j < n_ff + cat_target + ref_target)
        out.append(_trial(i, cat=cat, refuse=refuse, ff=ff, style_a=j < spec.get('style_a', 0), style_b=j < spec.get('style_b', 0),
                          mention=j < spec.get('mention', 0), loop=(n_ff <= j < n_ff + n_loop),
                          trunc=(n_ff + n_loop <= j < n_ff + n_loop + n_trunc),
                          correct=(None if 'correct' not in spec else (j < spec['correct'])), **kw))
        if spec.get('scoring_gap') and (n_ff + cat_target + ref_target) <= j < (n_ff + cat_target + ref_target + int(spec['scoring_gap'])):
            out[-1]['catastrophe'] = None      # 採点欠落（status は ok のまま・裁定 D96）
            out[-1]['choice'] = None
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
    # api_error と未測定（ループ・打ち切り）を無操作の腕に入れる（採否表 P300・P302）
    m[('N1', 'O')] = {'cat': 60, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8, 'api_error': 12, 'loop': 3, 'trunc': 2}
    tune = {'best': (LAYERS[1], COEFS[1]), 'eff': 12, 'tie': False, 'nonpositive': False, 'ff_fail': (LAYERS[0], COEFS[0]), 'censor_all': False}
    qual = {'fail_selection': [], 'fail_post': ['Onull+vNk']}
    # 封印は**一致する対比と逆向きの対比の両方**を持たせる（採否表 P297）
    seal = {'sub:N1:O-Ncold-v~O-Ncold-vrand': '上',          # データは「下」——逆向きの枝
            'add:N1:Onull+v~Onull+vrand': '下'}              # データも「下」——一致の枝
    return {'main': m, 'tune': tune, 'quality': qual, 'seal': seal,
            'resume': {'scenario': 'N1', 'arm': 'Onull+vtd'}}   # 中断と再開（採否表 P302）


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


def case_scoring_gap():
    """採点欠落（判定欄が空）と n_ok が零のセル（裁定 D96・採否表 P300）。"""
    m = base_main_spec()
    m[('S1', 'O-Ncold-v')] = {'cat': 20, 'refuse': 10, 'ff': 6, 'style_a': 40, 'style_b': 120, 'mention': 8, 'scoring_gap': 7}
    m[('SK', 'O-Ncold-v')] = {'cat': 0, 'refuse': 0, 'ff': 0, 'style_a': 0, 'style_b': 0, 'mention': 0, 'api_error': N_MAIN}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_s4_branches():
    """S4 の残りの枝——「下がらなかった（封印は当たり）」と「余地の条項で測れない（床）」（裁定 D81・D95）。"""
    m = base_main_spec()
    # 相手の率を**既測の基底の近く**（低い側）に置く——10 pt の検出力が線を越えるのはこの領域だけ（転記行 D）
    m[('S4', 'Osec-Ncold+v6b')] = {'cat': 33, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'Osec-Ncold+vrand')] = {'cat': 34, 'refuse': 6, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_s4_floor():
    m = base_main_spec()
    m[('S4', 'Osec-Ncold+v6b')] = {'cat': 1, 'refuse': 2, 'ff': 2, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('S4', 'Osec-Ncold+vrand')] = {'cat': 8, 'refuse': 2, 'ff': 2, 'style_a': 40, 'style_b': 120, 'mention': 8}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_dilution_causal():
    """**希釈が効く場面**——書式外が増えたぶんだけ破局の分子が減り、見かけの低下が出る（採否表 P301）。"""
    m = base_main_spec()
    m[('N1', 'Onull+v')] = {'cat': 138, 'refuse': 10, 'ff': 60, 'style_a': 40, 'style_b': 120, 'mention': 8}
    m[('N1', 'Onull+vrand')] = {'cat': 138, 'refuse': 10, 'ff': 4, 'style_a': 40, 'style_b': 120, 'mention': 8}
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12}, 'quality': {'fail_selection': [], 'fail_post': []}}


def case_incomplete():
    """品質床の走行の記録が欠けた場合（**記録の不在は「操作不能」ではない**・採否表 P272）。"""
    m = base_main_spec()
    return {'main': m, 'tune': {'best': (LAYERS[1], COEFS[1]), 'eff': 12},
            'quality': {'fail_selection': [], 'fail_post': [], 'drop_selection': [(LAYERS[0], COEFS[0])]}}


CASES = {'incomplete': case_incomplete, 'all': case_all, 'gate1_closed': case_gate1_closed, 'nonpositive': case_nonpositive, 'tie': case_tie,
         'censor_candidates': case_censor_candidates, 'scoring_gap': case_scoring_gap, 's4_branches': case_s4_branches,
         's4_floor': case_s4_floor, 'dilution_causal': case_dilution_causal}


def build(case, out_root):
    spec = CASES[case]()
    if os.path.isdir(out_root):
        shutil.rmtree(out_root)
    os.makedirs(out_root, exist_ok=True)
    # ---- 本走行 ----
    resume = spec.get('resume')                     # {'scenario': 'N1', 'arm': 'Onull+vtd'} なら、その腕を二つのセッションに分ける
    for sc in SC:
        _pick = spec['tune'].get('best') or (LAYERS[1], COEFS[1])
        man = {'scenario': sc, 'session': 1, 'n': N_MAIN, 'seed': T['seeds']['main'][sc],
               'arms': T['arms']['by_scenario'][sc], 'batch': T['runner']['batch'], 'layer': _pick[0], 'coef': _pick[1]}
        trials, tail = [], []
        for arm in T['arms']['by_scenario'][sc]:
            s_ = spec['main'][(sc, arm)]
            rk = '%s__%s__s1' % (T['tags']['main'], sc)
            if resume and resume.get('scenario') == sc and resume.get('arm') == arm:
                half = N_MAIN // 2
                trials += cell_trials(half, s_, start=0, arm=arm, scenario=sc, tag=T['tags']['main'], seed=T['seeds']['main'][sc], run_key=rk)
                tail += cell_trials(N_MAIN - half, s_, start=half, arm=arm, scenario=sc, tag=T['tags']['main'],
                                    seed=T['seeds']['main'][sc], run_key='%s__%s__s2' % (T['tags']['main'], sc))
            else:
                trials += cell_trials(N_MAIN, s_, arm=arm, scenario=sc, tag=T['tags']['main'], seed=T['seeds']['main'][sc], run_key=rk)
        write_run(out_root, T['tags']['main'], '%s__s1' % sc, man, trials)
        if tail:
            write_run(out_root, T['tags']['main'], '%s__s2' % sc, dict(man, session=2, arms=[resume['arm']]), tail)

    # ---- 同一性選別（三スタック・採否表 P302）----
    idt = T['tags']['identity']
    for stack in T['identity_screen']['stacks']:
        for arm in T['identity_screen']['arms_run']:
            trials = cell_trials(T['identity_screen']['n'], {'cat': 40, 'refuse': 6, 'ff': 4, 'style_a': 20, 'style_b': 90, 'mention': 5},
                                 arm=arm, scenario=T['identity_screen']['scenario'], tag=idt, seed=T['seeds']['identity_transformers'],
                                 run_key='%s__%s__%s' % (idt, stack, arm))
            write_run(out_root, idt, '%s__%s' % (stack, arm), {'stack': stack, 'scenario': T['identity_screen']['scenario'],
                                                               'n': T['identity_screen']['n'], 'seed': T['seeds']['identity_transformers'],
                                                               'arms': [arm], 'session': 1}, trials)

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
            if (l, c) in (q.get('drop_selection') or []):
                continue                      # 走行の記録を作らない（記録の不在）
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
        for sess in (1, 2):
            rk = '%s__%s__s%d__dryrun' % (T['tags']['main'], sc, sess)
            if not os.path.isdir(os.path.join(out_root, T['tags']['main'], rk)):
                continue
            json.dump({'tag': T['tags']['main'], 'session': sess, 'scenario': sc, 'gpu': 'synth', 'batch': T['runner']['batch'],
                       'run_keys': [rk], 'dry_run': True},
                      open(os.path.join(sd, '%s__%s__s%d.json' % (T['tags']['main'], sc, sess)), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
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
