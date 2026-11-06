# -*- coding: utf-8 -*-
# score_blind_v0.py <codes の tsv> <key の json> <出す json> : 凍結したコードと鍵を突き合わせ、語ごとの当て率と判定（下見の計画 §5 の表）を数える（書きは一度だけ）
#   第一の登録の score_blind_v1.py の写し。語を替え、置き場所を一つにし、副の数え（前置き・結び・整理の印を読めないに替える）を道具の中で数える形にした。
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
    if c[0] in codes:
        raise SystemExit(f'番号が二度ある: {c[0]}')
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
MARKS = ('前置き', '結び', '整理')


def strict_guess(c):
    if any(m in c['note'] for m in MARKS):
        return '読めない'
    return c['guess_arm']


words = ['仏性', '神性', '帽子']
R = {'per_word': {}, 'n_total': len(key), 'total_hits': 0, 'total_hits_strict': 0}
conf = collections.Counter()
for w in words:
    nos = [n for n, k in key.items() if k['word'] == w]
    if len(nos) != 15:
        raise SystemExit(f'語の答えの数が 15 でない: {w} {len(nos)}')
    hits = sum(1 for n in nos if codes[n]['guess_arm'] == key[n]['arm'])
    hits_s = sum(1 for n in nos if strict_guess(codes[n]) == key[n]['arm'])
    verdict = '読み分けられる' if hits >= 13 else ('要検討' if hits >= 10 else '読み分けられない')
    by_arm = {}
    for a in ARMS:
        na = [n for n in nos if key[n]['arm'] == a]
        by_arm[a] = {'n': len(na), 'hits': sum(1 for n in na if codes[n]['guess_arm'] == a),
                     'hits_strict': sum(1 for n in na if strict_guess(codes[n]) == a),
                     'epi_touch': sum(1 for n in na if codes[n]['epi'] == '触れる'),
                     'assert_fact': sum(1 for n in na if codes[n]['assert_fact'] == 'あり')}
    R['per_word'][w] = {'n': len(nos), 'hits': hits, 'hits_strict': hits_s, 'verdict': verdict, 'by_arm': by_arm}
    R['total_hits'] += hits
    R['total_hits_strict'] += hits_s
for n, k in key.items():
    conf[(k['arm'], codes[n]['guess_arm'])] += 1
R['confusion'] = {f'{a}→{g}': v for (a, g), v in sorted(conf.items())}
R['finish_not_stop'] = sum(1 for k in key.values() if k['finish'] != 'stop')
R['assert_fact_total'] = sum(1 for c in codes.values() if c['assert_fact'] == 'あり')
R['epi_touch_total'] = sum(1 for c in codes.values() if c['epi'] == '触れる')
with open(out_p, 'x', encoding='utf-8', newline='\n') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print(f"全体 {R['total_hits']}/{R['n_total']}", '副', R['total_hits_strict'], 'stop でない', R['finish_not_stop'], '言い切り', R['assert_fact_total'], '認識に触れる', R['epi_touch_total'])
for w in words:
    r = R['per_word'][w]
    print(' ', w, f"{r['hits']}/{r['n']}", '副', r['hits_strict'], r['verdict'], {a: f"{v['hits']}/{v['n']}" for a, v in r['by_arm'].items()})
print('  取り違え', {k: v for k, v in R['confusion'].items() if k.split('→')[0] != k.split('→')[1]})
