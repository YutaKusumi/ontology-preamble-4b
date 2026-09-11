# -*- coding: utf-8 -*-
"""sample_inspection_F.py —— 凍結 §2.7 の抽出検査の標本を機械抽出する（第一走行完走時に整合検査の直後に自動実行・目視はコーディネータが行い records/F/sampling-inspection-F-<date>.md に記録）。
第一走行: 全腕・腕あたり 2 件（9 腕 × 4 場面＝72 件）。第二走行: 同じ枠から無作為 1/4。判定欄と率を印字しない（率盲検の事前拘束と両立・M の D-21 の原因を器の側で除く）。
各件について機械分類（json_direct／prose_then_json／no_json・生本文の先頭）と、生本文の先頭 N 字を目視用ファイルに書く。分母を数える器ではない。
出力: records/F/sampling-inspection-F-<tag>-sample.txt（目視用・公開）・同 -modes.json（機械分類の集計）。"""
import os, json, glob, random, collections, argparse, datetime
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--seed', type=int, required=True); ap.add_argument('--per-arm', type=int, default=2); ap.add_argument('--fraction', type=float, default=1.0); ap.add_argument('--chars', type=int, default=600); ap.add_argument('--root', default=None); a = ap.parse_args()
random.seed(a.seed); rows = []; modes = collections.Counter(); per_arm = {}
for d in sorted(glob.glob(os.path.join(a.root or os.path.join(REPO, 'results', a.tag), a.tag + '__*'))):
    key = os.path.basename(d); sc = key.split('__')[1]
    rf = glob.glob(os.path.join(d, 'raw-*.jsonl'))[0]
    byarm = collections.defaultdict(list)
    for l in open(rf, encoding='utf-8'):
        if l.strip():
            r = json.loads(l); byarm[r['arm']].append({'trial_id': r['trial_id'], 'raw_output': r.get('raw_output') or ''})   # 判定欄は読まない
    for arm in sorted(byarm):
        for r in random.sample(byarm[arm], min(a.per_arm, len(byarm[arm]))):
            t = r['raw_output'].lstrip()
            m = 'json_direct' if (t.startswith('```json') or t.startswith('{')) else ('prose_then_json' if '```json' in t or '{' in t else 'no_json')
            rows.append((sc, arm, r['trial_id'], m, t[:a.chars].replace('\n', '⏎')))
if a.fraction < 1.0:
    rows = random.sample(rows, int(round(len(rows) * a.fraction)))
for sc, arm, tid, m, t in rows:
    modes[m] += 1; per_arm.setdefault('%s:%s' % (sc, arm), collections.Counter())[m] += 1
os.makedirs(os.path.join(REPO, 'records', 'F'), exist_ok=True)
out = os.path.join(REPO, 'records', 'F', 'sampling-inspection-F-%s-sample.txt' % a.tag)
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write('# 抽出検査 標本 %s（seed %d・腕あたり %d・割合 %.2f・%d 件・生本文の先頭 %d 字・改行は ⏎・判定欄と率は印字しない）\n' % (a.tag, a.seed, a.per_arm, a.fraction, len(rows), a.chars))
    for sc, arm, tid, m, t in rows:
        f.write('\n=== %s | %s | %s | 機械分類 %s\n%s\n' % (sc, arm, tid, m, t))
json.dump({'tag': a.tag, 'seed': a.seed, 'n': len(rows), 'modes': dict(modes), 'per_arm': {k: dict(v) for k, v in per_arm.items()}, 'date': datetime.date.today().isoformat()}, open(out.replace('-sample.txt', '-modes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', out, len(rows), dict(modes))
