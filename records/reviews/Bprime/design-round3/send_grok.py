# -*- coding: utf-8 -*-
"""send_grok.py v1（2026-09-29・B′ の設計の巡・三巡目〔最終の検分〕・系統外の一票を grok-4.7 の新しい呼び出しに頼む・二巡目の器の定数を替えたもの・コーディネータ南無弥勒如来）。
一巡目の v0 の型。v0 の費用の式は考える分（reasoning_tokens）を入れていなかったので、v1 は考える分を出力の値段で数え、API の `cost_in_usd_ticks`（1 tick＝10 の −10 乗ドル）も並べる。
一巡目・二巡目の会話は持ち込まない（新しい個体・枠）。返事は `votes/grok-4.7/` に一度だけ書く（上書きしない）。鍵は読むだけで、表示しない。束の中身の SHA を送る前に確かめる。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, time, hashlib, datetime, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'kit')
OUT = os.path.join(HERE, 'votes', 'grok-4.7')
MODEL = 'grok-4.7'
MSG_SHA16 = 'E5361C957BB4CB0A'
PRICE_IN, PRICE_CACHED, PRICE_OUT = 2.00, 0.50, 6.00      # 100 万トークンあたりのドル（xAI の API の機種の一覧・2026-09-29）
CAP = 5.00
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
    assert msg_sha == MSG_SHA16, ('発話の SHA が kit-message.md と違う', msg_sha)
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
    usd = (pin - cached) / 1e6 * PRICE_IN + cached / 1e6 * PRICE_CACHED + (pout + reasoning) / 1e6 * PRICE_OUT
    ticks = u.get('cost_in_usd_ticks')
    meta = {'model_requested': MODEL, 'model_returned': d.get('model'), 'time_jst': (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
            'seconds': round(secs, 1), 'message_sha16': msg_sha, 'message_chars': len(msg), 'kit_manifest_sha16': hashlib.sha256(open(os.path.join(KIT, 'MANIFEST.sha256'), 'rb').read()).hexdigest().upper()[:16],
            'usage': u, 'est_usd_with_reasoning': round(usd, 6), 'ticks_usd': (None if ticks is None else round(ticks * 1e-10, 6)), 'cap_usd': CAP,
            'response_sha16': hashlib.sha256(content.encode('utf-8')).hexdigest().upper()[:16], 'finish_reason': d['choices'][0].get('finish_reason')}
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('done | model', meta['model_returned'], '| in', pin, '(cached', cached, ') | out', pout, '(reasoning', reasoning, ') | USD', meta['est_usd_with_reasoning'], '| ticks USD', meta['ticks_usd'],
          '| secs', meta['seconds'], '| finish', meta['finish_reason'], '| response chars', len(content))


if __name__ == '__main__':
    main()
