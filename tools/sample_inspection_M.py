# -*- coding: utf-8 -*-
"""sample_inspection_M.py —— 凍結 §2.7 の抽出検査の標本を機械抽出する（目視はコーディネータが行い records/M/sampling-inspection-M-<date>.md に記録）。
第一走行: 全腕・腕あたり 2 件（66 腕 × 4 場面＝528 件・seed 42100）。第二走行: 第一走行と同じ枠（66 × 4 × 2）から無作為 1/4（132 件・seed 43100）。
各件について機械分類（json_direct／prose_then_json／no_json・復唱剥がし前の生本文の先頭）と、生本文の先頭 N 字を目視用ファイルに書く。分母を数える器ではない（率は analyze_M の領分）。
出力: records/M/sampling-inspection-M-<tag>-sample.txt（目視用・公開）・同 -modes.json（機械分類の集計）。"""
import os, json, glob, random, collections, argparse, datetime
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--seed', type=int, required=True); ap.add_argument('--per-arm', type=int, default=2); ap.add_argument('--fraction', type=float, default=1.0); ap.add_argument('--chars', type=int, default=600); a = ap.parse_args()
random.seed(a.seed); rows = []; modes = collections.Counter(); per_arm = {}
for d in sorted(glob.glob(os.path.join(REPO, 'results', a.tag, a.tag + '__*'))):
    key = os.path.basename(d); sc = key.split('__')[1]
    rf = glob.glob(os.path.join(d, 'raw-*.jsonl'))[0]
    byarm = collections.defaultdict(list)
    for l in open(rf, encoding='utf-8'):
        if l.strip():
            r = json.loads(l); byarm[r['arm']].append(r)
    for arm in sorted(byarm):
        for r in random.sample(byarm[arm], a.per_arm):
            t = (r.get('raw_output') or '').lstrip()
            m = 'json_direct' if (t.startswith('```json') or t.startswith('{')) else ('prose_then_json' if '```json' in t or '{' in t else 'no_json')
            rows.append((sc, arm, r['trial_id'], m, t[:a.chars].replace('\n', '⏎')))
if a.fraction < 1.0:
    rows = random.sample(rows, int(round(len(rows) * a.fraction)))
for sc, arm, tid, m, t in rows:
    modes[m] += 1; per_arm.setdefault('%s:%s' % (sc, arm), collections.Counter())[m] += 1
stamp = datetime.date.today().isoformat()
out = os.path.join(REPO, 'records', 'M', 'sampling-inspection-M-%s-sample.txt' % a.tag)
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write('# 抽出検査 標本 %s（seed %d・腕あたり %d・割合 %.2f・%d 件・生本文の先頭 %d 字・改行は ⏎）\n' % (a.tag, a.seed, a.per_arm, a.fraction, len(rows), a.chars))
    for sc, arm, tid, m, t in rows:
        f.write('\n=== %s | %s | %s | 機械分類 %s\n%s\n' % (sc, arm, tid, m, t))
json.dump({'tag': a.tag, 'seed': a.seed, 'n': len(rows), 'modes': dict(modes), 'per_arm': {k: dict(v) for k, v in per_arm.items()}, 'date': stamp}, open(out.replace('-sample.txt', '-modes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', out, len(rows), dict(modes))
