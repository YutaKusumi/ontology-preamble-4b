# -*- coding: utf-8 -*-
# score_blind_v0.py <codes の tsv> <key の json> <出す json> : 凍結したコードと鍵を突き合わせ、語ごとの当て率と判定（計画 v0 §4 の表）を数える（書きは一度だけ）
import sys, json, collections
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
codes_p, key_p, out_p = sys.argv[1:4]
key = json.load(open(key_p, encoding='utf-8'))['map']
lines = open(codes_p, encoding='utf-8').read().splitlines()
hdr = lines[0].split('\t')
assert hdr[:4] == ['no', 'guess_arm', 'epi', 'assert_fact'], hdr
codes = {}
for l in lines[1:]:
    if not l.strip():
        continue
    c = l.split('\t')
    c += [''] * (5 - len(c))
    codes[c[0]] = {'guess_arm': c[1].strip(), 'epi': c[2].strip(), 'assert_fact': c[3].strip(), 'note': c[4].strip()}
if set(codes) != set(key):
    raise SystemExit(f'番号が鍵と合わない: コード {len(codes)} 鍵 {len(key)}')
ARMS = ['有', '無', '不明']
for no, c in codes.items():
    if c['guess_arm'] not in ARMS + ['読めない']:
        raise SystemExit(f'推した立場の値が決まりの外: {no} {c["guess_arm"]!r}')
    if c['epi'] not in ('触れる', '触れない'):
        raise SystemExit(f'認識の一文の値が決まりの外: {no} {c["epi"]!r}')
    if c['assert_fact'] not in ('あり', 'なし'):
        raise SystemExit(f'言い切りの値が決まりの外: {no} {c["assert_fact"]!r}')
words = ['魂', '心', '意識', '精神', '感情', '自我']
res = {'per_word': {}, 'confusion': {}, 'total_hits': 0}
conf = collections.Counter()
for w in words:
    nos = [n for n, k in key.items() if k['word'] == w]
    hits = sum(1 for n in nos if codes[n]['guess_arm'] == key[n]['arm'])
    verdict = '読み分けられる' if hits >= 13 else ('要検討' if hits >= 10 else '読み分けられない')
    by_arm = {}
    for a in ARMS:
        na = [n for n in nos if key[n]['arm'] == a]
        by_arm[a] = {'n': len(na), 'hits': sum(1 for n in na if codes[n]['guess_arm'] == a),
                     'epi_touch': sum(1 for n in na if codes[n]['epi'] == '触れる'),
                     'assert_fact': sum(1 for n in na if codes[n]['assert_fact'] == 'あり')}
    res['per_word'][w] = {'n': len(nos), 'hits': hits, 'verdict': verdict, 'by_arm': by_arm}
    res['total_hits'] += hits
for n, k in key.items():
    conf[(k['arm'], codes[n]['guess_arm'])] += 1
res['confusion'] = {f'{a}→{g}': v for (a, g), v in sorted(conf.items())}
res['n_total'] = len(key)
res['finish_not_stop'] = sum(1 for k in key.values() if k['finish'] != 'stop')
res['jiga_nashi_notes'] = {n: codes[n]['note'] for n, k in key.items() if k['word'] == '自我' and k['arm'] == '無'}
with open(out_p, 'x', encoding='utf-8', newline='\n') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
for w in words:
    r = res['per_word'][w]
    print(w, f"{r['hits']}/{r['n']}", r['verdict'], {a: f"{v['hits']}/{v['n']}" for a, v in r['by_arm'].items()})
print('全体', f"{res['total_hits']}/{res['n_total']}", '取り違え', {k: v for k, v in res['confusion'].items() if k.split('→')[0] != k.split('→')[1]})
print('stop でない答え', res['finish_not_stop'])
