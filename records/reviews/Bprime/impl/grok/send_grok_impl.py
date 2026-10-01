# -*- coding: utf-8 -*-
"""send_grok_impl.py v0（2026-09-30・B′ の器の実装の検分・系統外の一巡〔独立の再計算の三つの道〕を grok-4.7 の新しい呼び出しに頼む・裁定 D272・コーディネータ南無弥勒如来）。
前の巡の `send_grok.py` v1 の型（考える分を出力の値段で数え、API の `cost_in_usd_ticks`〔1 tick＝10 の −10 乗ドル〕も並べる）。
発話は `grok-message.md`（送る前に SHA16 を確かめる）。前の巡の会話は持ち込まない（新しい呼び出し）。返事は `../votes/grok-4.7/` に一度だけ書く（上書きしない）。鍵は読むだけで、表示しない。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, time, hashlib, datetime, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'votes', 'grok-4.7')
MODEL = 'grok-4.7'
MSG_SHA16 = '8648D069006B6230'
PRICE_IN, PRICE_CACHED, PRICE_OUT = 2.00, 0.50, 6.00      # 100 万トークンあたりのドル（前の巡の器と同じ値・xAI の API の機種の一覧・2026-09-29）
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
    raw = open(os.path.join(HERE, 'grok-message.md'), 'rb').read().replace(b'\r\n', b'\n')
    msg_sha = hashlib.sha256(raw).hexdigest().upper()[:16]
    assert msg_sha == MSG_SHA16, ('発話の SHA が決めた値と違う', msg_sha)
    msg = raw.decode('utf-8')
    est_in = len(msg) / 1.2 / 1e6 * PRICE_IN
    print('送る前の見積もり（読み込みだけ・字数から）: %.2f ドル・上限 %.2f ドル' % (est_in, CAP))
    assert est_in < CAP / 2, '読み込みだけで上限の半分を超える見積もり（送らない）'
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
    with open(os.path.join(OUT, 'response.md'), 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(content)
    with open(os.path.join(OUT, 'response-raw.json'), 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)
    u = d.get('usage') or {}
    pin = u.get('prompt_tokens', 0)
    cached = (u.get('prompt_tokens_details') or {}).get('cached_tokens', 0)
    pout = u.get('completion_tokens', 0)
    reasoning = (u.get('completion_tokens_details') or {}).get('reasoning_tokens', 0)
    usd = (pin - cached) / 1e6 * PRICE_IN + cached / 1e6 * PRICE_CACHED + (pout + reasoning) / 1e6 * PRICE_OUT
    ticks = u.get('cost_in_usd_ticks')
    meta = {'model_requested': MODEL, 'model_returned': d.get('model'), 'time_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            'seconds': round(secs, 1), 'message_sha16': msg_sha, 'message_chars': len(msg), 'usage': u, 'est_usd_with_reasoning': round(usd, 6),
            'ticks_usd': (None if ticks is None else round(ticks * 1e-10, 6)), 'cap_usd': CAP, 'registrant_permission': 'D272',
            'response_sha16': hashlib.sha256(content.encode('utf-8')).hexdigest().upper()[:16], 'finish_reason': d['choices'][0].get('finish_reason'),
            'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('done | model', meta['model_returned'], '| in', pin, '(cached', cached, ') | out', pout, '(reasoning', reasoning, ') | USD', meta['est_usd_with_reasoning'], '| ticks USD', meta['ticks_usd'],
          '| secs', meta['seconds'], '| finish', meta['finish_reason'], '| response chars', len(content))


if __name__ == '__main__':
    main()
