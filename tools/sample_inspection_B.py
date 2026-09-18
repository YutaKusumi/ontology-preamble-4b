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
