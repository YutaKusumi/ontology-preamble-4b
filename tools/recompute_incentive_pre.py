# -*- coding: utf-8 -*-
"""recompute_incentive_pre.py —— 復唱除去「前」の誘因言及率と腕別削除字数（12字規則／20字感度）を、生出力から再計算する（凍結 §3.3・§13「復唱除去前後の両方を報告」）。
凍結走行器の incentive/strip_echo/_norm を AST で逐語抽出して用いる。出力: records/results/incentive-pre-post-<date>.json / .md
"""
import os, sys, json, glob, ast, re, unicodedata, datetime, collections
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = open(os.path.join(REPO, 'tools', 'run_preamble_api.py'), encoding='utf-8').read().replace('\r\n', '\n')
ns = {'os': os, 'sys': sys, 'json': json, 're': re, 'unicodedata': unicodedata}
for node in ast.parse(SRC).body:
    if isinstance(node, ast.FunctionDef) and node.name in ('_norm', '_any', 'strip_echo', '_quoted_segments', 'incentive'):
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'frozen', 'exec'), ns)
LEX = json.load(open(os.path.join(REPO, 'arms', 'materials-draft', 'hei', 'incentive-lexicon-v2.json'), encoding='utf-8')); ns['LEX'] = LEX
SC = json.load(open(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
SCEN = {x['question_id']: x for x in SC['scenarios']}


class A: pass


res = {}
for tag in ('stage1', 'stage6', 'stage2', 'stage5'):
    for d in sorted(glob.glob(os.path.join(REPO, 'results', tag, '*'))):
        cf = os.path.join(d, 'cells.json')
        if not os.path.isfile(cf):
            continue
        man = json.load(open(cf, encoding='utf-8'))['manifest']; sc = man['scenario']; fam = man['family']
        a = A(); a.scenario = sc; ns['args'] = a; ns['FAM'] = fam
        rows = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8') if l.strip()}
        raws = [json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8') if l.strip()]
        agg = collections.defaultdict(lambda: {'n': 0, 'pre': 0, 'post': 0, 'post20': 0, 'chars12': 0, 'chars20': 0, 'trials12': 0, 'trials20': 0})
        for rr in raws:
            r = rows.get(rr['trial_id'])
            if not r or r['status'] != 'ok':
                continue
            txt = rr['raw_output'].split('\n===RETRY===\n')[-1]   # 最終試行のみ採点（凍結規約）
            g = agg[r['arm']]; g['n'] += 1
            pre = ns['incentive'](txt, ())            # 復唱除去なし（除去後の値は走行時の行 incentive_core をそのまま用いる）
            g['pre'] += 1 if (pre or {}).get('core') else 0
            g['post'] += 1 if r.get('incentive_core') else 0
            g['chars12'] += r.get('echo_stripped_chars') or 0; g['chars20'] += r.get('echo_stripped_chars_20') or 0
            g['trials12'] += 1 if r.get('echo_stripped_chars') else 0; g['trials20'] += 1 if r.get('echo_stripped_chars_20') else 0
        res[os.path.basename(d)] = {arm: {'n': g['n'], 'pre_rate': round(g['pre'] / g['n'], 4), 'post_rate_12': round(g['post'] / g['n'], 4), 'echo_trials_12': g['trials12'], 'echo_chars_12': g['chars12'],
                                          'echo_trials_20': g['trials20'], 'echo_chars_20': g['chars20']} for arm, g in agg.items()}
os.makedirs(os.path.join(REPO, 'records', 'results'), exist_ok=True)
stamp = datetime.date.today().isoformat()
json.dump(res, open(os.path.join(REPO, 'records', 'results', 'incentive-pre-post-%s.json' % stamp), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
out = ['# 誘因言及率 復唱除去前／後と腕別削除字数 —— %s' % stamp, '', '除去後（12字＋鉤括弧6字規則）は走行時の値（cells）。除去前は生出力に同じ語彙を除去なしで再適用した値。20字感度規則の削除字数は走行時に併記記録。S3 は core 合算を主指標にしない（チャネル別は cells 参照）。', '']
for k, v in res.items():
    out.append('## %s' % k); out.append('| 腕 | n | 除去前 core 率 | 除去後 core 率(12字) | 削除あり試行(12字) | 削除字数(12字) | 削除あり試行(20字) | 削除字数(20字) |'); out.append('|---|---|---|---|---|---|---|---|')
    for arm, g in v.items():
        out.append('| %s | %d | %.3f | %.3f | %d | %d | %d | %d |' % (arm, g['n'], g['pre_rate'], g['post_rate_12'], g['echo_trials_12'], g['echo_chars_12'], g['echo_trials_20'], g['echo_chars_20']))
    out.append('')
open(os.path.join(REPO, 'records', 'results', 'incentive-pre-post-%s.md' % stamp), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n'); print('written', len(res))
