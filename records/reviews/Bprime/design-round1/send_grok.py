# -*- coding: utf-8 -*-
"""send_grok.py v0（2026-09-29・B′ の設計の巡・一巡目・系統外の一票を grok-4.7 に頼む・コーディネータ南無弥勒如来）。
依頼文を頭に置き、束のファイルを「=== ファイル名 ===」の見出しつきで並べた一つの発話にして送る（枠 `00-frame-design-round1.md`）。
返事は `votes/grok-4.7/` に一度だけ書く（上書きしない）。鍵は読むだけで、表示しない。束の中身の SHA を送る前に確かめる。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, time, hashlib, datetime, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'kit')
OUT = os.path.join(HERE, 'votes', 'grok-4.7')
MODEL = 'grok-4.7'
PRICE_IN, PRICE_CACHED, PRICE_OUT = 2.00, 0.50, 6.00      # 100 万トークンあたりのドル（xAI の API の機種の一覧・2026-09-29）
ENV_FILE = os.environ.get('OP4B_ENV_FILE', 'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
NL = chr(10)


def load_key(name):
    k = os.environ.get(name)
    if k:
        return k.strip()
    for line in open(ENV_FILE, encoding='utf-8'):
        line = line.strip()
        if line.startswith(name + '=') and len(line) > len(name) + 1:
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    sys.exit('鍵が見つからない')


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    import build_message
    msg = build_message.build()
    msg_sha = hashlib.sha256(msg.encode('utf-8')).hexdigest().upper()[:16]
    key = load_key('XAI_API_KEY')
    body = {'model': MODEL, 'messages': [{'role': 'user', 'content': msg}], 'max_tokens': 60000}
    t0 = time.time()
    req = urllib.request.Request('https://api.x.ai/v1/chat/completions', data=json.dumps(body).encode('utf-8'),
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=3600).read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        sys.exit('HTTP %d: %s' % (e.code, e.read().decode('utf-8', 'replace')[:500]))
    secs = time.time() - t0
    os.makedirs(OUT)
    content = d['choices'][0]['message'].get('content') or ''
    open(os.path.join(OUT, 'response.md'), 'w', encoding='utf-8', newline=NL).write(content)
    json.dump(d, open(os.path.join(OUT, 'response-raw.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    u = d.get('usage') or {}
    pin = u.get('prompt_tokens', 0)
    cached = (u.get('prompt_tokens_details') or {}).get('cached_tokens', 0)
    pout = u.get('completion_tokens', 0)
    reasoning = (u.get('completion_tokens_details') or {}).get('reasoning_tokens', 0)
    usd = (pin - cached) / 1e6 * PRICE_IN + cached / 1e6 * PRICE_CACHED + pout / 1e6 * PRICE_OUT
    meta = {'model_requested': MODEL, 'model_returned': d.get('model'), 'time_jst': (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
            'seconds': round(secs, 1), 'message_sha16': msg_sha, 'message_chars': len(msg), 'kit_manifest_sha16': hashlib.sha256(open(os.path.join(KIT, 'MANIFEST.sha256'), 'rb').read()).hexdigest().upper()[:16],
            'usage': u, 'est_usd': round(usd, 4), 'response_sha16': hashlib.sha256(content.encode('utf-8')).hexdigest().upper()[:16], 'finish_reason': d['choices'][0].get('finish_reason')}
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('done | model', meta['model_returned'], '| in', pin, '(cached', cached, ') | out', pout, '(reasoning', reasoning, ') | est USD', meta['est_usd'], '| secs', meta['seconds'], '| finish', meta['finish_reason'], '| response chars', len(content))


if __name__ == '__main__':
    main()
