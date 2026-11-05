# -*- coding: utf-8 -*-
# make_blind_sheet_v0.py <results の zip> <出す置き場> : 90 の答えを順を乱して読みの表（腕と語の印なし）にし、鍵を別のファイルに書く（書きは一度だけ・鍵は表示しない）
import os, sys, json, zipfile, hashlib, random
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
zp, outdir = sys.argv[1], sys.argv[2]
sheet = os.path.join(outdir, 'sheet-blind-v0.md')
key = os.path.join(outdir, 'key-v0.json')
codes = os.path.join(outdir, 'codes-v0.tsv')
for p in (sheet, key, codes):
    if os.path.exists(p):
        raise SystemExit(f'既にある・止める {os.path.basename(p)}')
z = zipfile.ZipFile(zp)
rows = [json.loads(l) for l in z.read('probe-stance-out-v0/outputs.jsonl').decode('utf-8').splitlines() if l.strip()]
if len(rows) != 90:
    raise SystemExit(f'行の数が 90 でない: {len(rows)}')
seed = int.from_bytes(os.urandom(8), 'big')
rng = random.Random(seed)
order = list(range(len(rows)))
rng.shuffle(order)
labels = rng.sample(range(100, 1000), len(rows))
keyd = {'seed': seed, 'map': {}}
with open(sheet, 'x', encoding='utf-8', newline='\n') as f:
    f.write('# 読みの表 v0（腕と語の印を伏せた・番号は乱数）\n\n')
    f.write('各答えに「推した立場（有・無・不明・読めない）／認識の一文（触れる・触れない）／事実としての言い切り（あり・なし）／覚え書き」を codes-v0.tsv に付ける。\n\n')
    for lab, i in zip(labels, order):
        r = rows[i]
        keyd['map'][str(lab)] = {'item_id': r['item_id'], 'word': r['word'], 'arm': r['arm'], 'sample': r['sample'], 'finish': r['finish'], 'n_tokens_out': r['n_tokens_out']}
        f.write(f'## No.{lab}\n\n')
        f.write('```text\n' + r['output'].replace('```', "'''") + '\n```\n\n')
with open(key, 'x', encoding='utf-8', newline='\n') as f:
    json.dump(keyd, f, ensure_ascii=False, indent=1)
with open(codes, 'x', encoding='utf-8', newline='\n') as f:
    f.write('no\tguess_arm\tepi\tassert_fact\tnote\n')
    for lab in sorted(labels):
        f.write(f'{lab}\t\t\t\t\n')
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()
print('SHEET', sha(sheet)[:16], 'KEY', sha(key)[:16], 'CODES(空)', sha(codes)[:16], 'n', len(rows))
