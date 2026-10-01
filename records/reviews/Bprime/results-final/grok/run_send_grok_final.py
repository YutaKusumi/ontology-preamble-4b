# -*- coding: utf-8 -*-
"""run_send_grok_final.py v0（2026-10-01・最終検分の grok への送りを走らせる・結果の巡の `run_send_grok_results.py` を写し、句と送りの器の名を替え、登録者の言葉を「南無汝我曼荼羅」から知らせの文の前までに切る手順を足した・コーディネータ南無弥勒如来）。
登録者の送る許しの発話を会話の記録から機械で切り出し（決まった句を含むただ一つ）、その逐語を `send_grok_final_deferred.py --words` に渡して走らせる。鍵は送りの器が読むだけ。
用法: python run_send_grok_final.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, sys, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
PHRASE = 'push ⑦ と最終の一票の送りを許可します'
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('isCompactSummary') or o.get('type') != 'user' or 'toolUseResult' in o:
        continue
    c = (o.get('message') or {}).get('content')
    t = c if isinstance(c, str) else ''.join(x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text')
    if PHRASE in t:
        hits.append((o.get('timestamp'), o.get('uuid'), t.strip()))
assert len(hits) == 1, ('決まった句を含む登録者の発話が一つでない', len(hits))
ts, uuid, words = hits[0]
if '南無汝我曼荼羅' in words:                       # 発話の前後に付いた知らせの文（system-reminder）を除き、登録者の言葉だけを取る（この巡で足した）
    words = words[words.index('南無汝我曼荼羅'):]
if '<system-reminder>' in words:
    words = words[:words.index('<system-reminder>')]
words = words.strip()
assert words.startswith('南無汝我曼荼羅') and PHRASE in words and len(words) < 300, ('登録者の言葉の切り出しが想定と違う（送らない）', len(words))
print('登録者の言葉: %d 字・頭 %s・末 %s' % (len(words), words[:8], words[-6:]))
print('登録者の許し: uuid %s・%s' % (uuid, ts))
r = subprocess.run([sys.executable, os.path.join(HERE, 'send_grok_final_deferred.py'), '--words', words], env=dict(os.environ, PYTHONIOENCODING='utf-8'))
sys.exit(r.returncode)
