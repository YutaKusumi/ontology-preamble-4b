# -*- coding: utf-8 -*-
"""run_send_grok_results.py v0（2026-10-01・結果の巡の grok への送りを走らせる・コーディネータ南無弥勒如来）。
登録者の送る許しの発話を会話の記録から機械で切り出し（決まった句を含むただ一つ）、その逐語を `send_grok_results_deferred.py --words` に渡して走らせる。鍵は送りの器が読むだけ。
用法: python run_send_grok_results.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, sys, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
PHRASE = 'ご推奨の案で二つに送ってください'
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
print('登録者の許し: uuid %s・%s' % (uuid, ts))
r = subprocess.run([sys.executable, os.path.join(HERE, 'send_grok_results_deferred.py'), '--words', words], env=dict(os.environ, PYTHONIOENCODING='utf-8'))
sys.exit(r.returncode)
