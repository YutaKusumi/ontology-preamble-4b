# -*- coding: utf-8 -*-
"""sample_inspection_A.py v1.1 —— 段階 A の抽出検査の標本を機械抽出する（率盲検・正本 sample_inspection・2026-09-13・登録者裁定 D9 の三つ目の手順・D25）。
枠: 機種 × 場面 × 腕ごとに status ok の試行から per_cell 件を無作為に抜き、fraction が一未満なら抜いた枠全体から割合で抜く（相ごとの設定は sample_inspection.pilot／main、
乱数は seeds.sample_inspection の相の値）。パイロットに撤退条件の再走があれば、再走の走行も同じ枠に入れる。
v1.1（2026-09-14・実装検分の採否表 P93・登録者裁定 D25）: 枠は走行キーの昇順（走行の中は腕の昇順）で乱数を消費する。標本の並びは乱数で決め、機種と場面と腕を伏せた標識（S0001…）で印字する。
  標識から機種・場面・腕・走行キー・trial_id への対応表は別ファイル（-key.json）に置き、目視の記録を書いた後に開く。機種ごとの機械分類の集計も対応表の側に置く。dry-run の走行は拒む（--allow-dry は検査用）。
各件: 生本文の先頭 chars 字（改行は ⏎）・機械分類（json_direct／prose_then_json／no_json・再試行を含む生本文の先頭で決める）・<think> の有無。判定欄（catastrophe・choice・refuse_class）と率は印字しない。
分母を数える器ではない（率は analyze_A の領分）。
出力: records/A/sampling-inspection-A-<tag>-sample.txt（標本・伏せた標識）と同 -key.json（対応表）と同 -modes.json（機械分類の全体の集計）。目視の記録はコーディネータが records/A/sampling-inspection-A-<tag>.md に書く。
  既存は --force なしでは上書きしない。
用法: python tools/sample_inspection_A.py --tag pilotA [--phase pilot] [--root <results の代わり>]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, random, argparse, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1.1'
THINK = ('<think>', '</think>')

ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--phase', default=None, choices=[None, 'pilot', 'main']); ap.add_argument('--root', default=None)
ap.add_argument('--contrasts', default=None); ap.add_argument('--out-prefix', default=None); ap.add_argument('--force', action='store_true'); ap.add_argument('--allow-dry', action='store_true')
a = ap.parse_args()
T = runs_A.load_T(a.contrasts); SI = T['sample_inspection']
PHASE = a.phase or ('pilot' if a.tag == T['tags']['pilot'] else 'main' if a.tag == T['tags']['main'] else None)
if PHASE is None:
    sys.exit('相を決められない（--phase pilot|main）')
CFG = SI[PHASE]; SEED = T['seeds']['sample_inspection'][PHASE]; CH = SI['chars']
OUTP = a.out_prefix or os.path.join(REPO, 'records', 'A', 'sampling-inspection-A-%s' % a.tag)
if any(os.path.exists(OUTP + x) for x in ('-sample.txt', '-key.json', '-modes.json')) and not a.force:
    sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % OUTP)
try:
    IDX = runs_A.index_runs(T, a.tag, a.root, allow_multi=True, allow_dry=a.allow_dry)
except RuntimeError as ex:
    sys.exit('読み出しで止まった（%s）' % ex)
rng = random.Random(SEED); rows = []
for rec in sorted((r for recs in IDX.values() for r in recs), key=lambda r: r['run_key']):   # 枠は走行キーの昇順（登録者裁定 D25）
    ok_ids = collections.defaultdict(list)
    for r in runs_A.iter_jsonl(rec['trials_path'], ('trial_id', 'arm', 'status')):
        if r['status'] == 'ok':
            ok_ids[r['arm']].append(r['trial_id'])
    raws = {r['trial_id']: r for r in runs_A.iter_jsonl(rec['raw_path'], ('trial_id', 'raw_output'))}
    for arm in sorted(ok_ids):
        ids = sorted(ok_ids[arm])
        for tid in rng.sample(ids, min(CFG['per_cell'], len(ids))):
            t = ((raws.get(tid) or {}).get('raw_output') or '').lstrip()
            mode = 'json_direct' if (t.startswith('```json') or t.startswith('{')) else ('prose_then_json' if ('```json' in t or '{' in t) else 'no_json')
            rows.append({'model': rec['model'], 'scenario': rec['scenario'], 'arm': arm, 'run_key': rec['run_key'], 'trial_id': tid, 'mode': mode, 'think': any(x in t for x in THINK), 'head': t[:CH].replace('\n', '⏎')})
if CFG['fraction'] < 1.0:
    rows = rng.sample(rows, int(round(len(rows) * CFG['fraction'])))
rng.shuffle(rows)   # 並びから機種・場面・腕が読めないよう、印字の順を乱数で決める（登録者裁定 D25）
for j, x in enumerate(rows, 1):
    x['label'] = 'S%04d' % j
modes = collections.Counter(x['mode'] for x in rows); think = sum(1 for x in rows if x['think'])
os.makedirs(os.path.dirname(OUTP), exist_ok=True)
with open(OUTP + '-sample.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write('# 抽出検査 標本 %s（相 %s・seed %d・枠あたり %d・割合 %s・%d 件・生本文の先頭 %d 字・改行は ⏎・機種と場面と腕は伏せた標識・対応表は -key.json に分けて置き、目視の記録の後に開く・判定欄と率は印字しない・`tools/sample_inspection_A.py` %s）\n'
            % (a.tag, PHASE, SEED, CFG['per_cell'], CFG['fraction'], len(rows), CH, VERSION))
    for x in rows:
        f.write('\n=== %s | 機械分類 %s | <think> %s\n%s\n' % (x['label'], x['mode'], 'あり' if x['think'] else 'なし', x['head']))
    f.write('\n本標本の応答本文は器物の出力であり、AI による自己報告ではない。いかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。\n')
json.dump({'kind': 'sample_inspection_key_A', 'version': VERSION, 'tag': a.tag, 'phase': PHASE, 'rule': '目視の記録を書いた後に開く（登録者裁定 D25）',
           'key': [{k: x[k] for k in ('label', 'model', 'scenario', 'arm', 'run_key', 'trial_id')} for x in rows],
           'per_model': {mk: dict(collections.Counter(x['mode'] for x in rows if x['model'] == mk)) for mk in sorted({x['model'] for x in rows})}},
          open(OUTP + '-key.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
json.dump({'kind': 'sample_inspection_A', 'version': VERSION, 'tag': a.tag, 'phase': PHASE, 'seed': SEED, 'n': len(rows), 'modes': dict(modes), 'think_residue': think,
           'dev_marks': [x for x, on in (('allow_dry', a.allow_dry),) if on], 'date': datetime.date.today().isoformat(),
           'sample_sha16': runs_A.sha16_file(OUTP + '-sample.txt'), 'key_sha16': runs_A.sha16_file(OUTP + '-key.json')}, open(OUTP + '-modes.json', 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('[sample_inspection_A] %s %s: %d 件 %s・<think> %d → %s-sample.txt（対応表 -key.json は目視の記録の後に開く）' % (a.tag, PHASE, len(rows), dict(modes), think, OUTP))
