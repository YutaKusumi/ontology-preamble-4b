# -*- coding: utf-8 -*-
"""send_grok_followup1_deferred.py v0（2026-09-30・B′ の器の実装の検分・系統外の一巡への追い問い〔一度目・G-01〕を grok-4.7 の新しい呼び出しに送る・後で受け取る形・裁定 D276・コーディネータ南無弥勒如来）。
`send_grok_impl_deferred.py` v0 の置き場の名と発話と裁定だけを替えた写し。前の巡の型（新しい呼び出しに前の返事を添える）。
一度目（`send_grok_impl.py` v0・17:28:53）は、接続を張ったまま 3600 秒で返事の一行目も来ずに切れた（`../sending-log.md`）。二度目は同じ発話（`grok-message.md`・SHA16 を確かめる）を、
xAI の API の後で受け取る形で一度だけ送る: 送ると受付番号（request_id）が返り、答えは `GET /v1/chat/deferred-completion/<request_id>` を 30 秒おきに取りに行く（202 は待ち・200 は答え・最大 7200 秒）。
受付番号は `deferred-request.json` に一度だけ書く（鍵ではない）。答えは `../votes/grok-4.7/` に一度だけ書く（上書きしない）。鍵は読むだけで、表示しない。この形が受け付けられなければ（202 と 200 のほか）、送り直さずに止める。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, time, hashlib, datetime, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'votes', 'grok-4.7-followup1')
REQ = os.path.join(HERE, 'followup1-deferred-request.json')
MODEL = 'grok-4.7'
MSG_SHA16 = '782FB6693A407B26'
PRICE_IN, PRICE_CACHED, PRICE_OUT = 2.00, 0.50, 6.00      # 100 万トークンあたりのドル（一度目の器と同じ値）
CAP = 5.00
POLL, LIMIT = 30, 7200
ENV_FILE = os.environ.get('OP4B_ENV_FILE', 'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
NL = chr(10)
JST = datetime.timezone(datetime.timedelta(hours=9))
now = lambda: datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')


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
    assert not os.path.exists(OUT), '答えの置き場が既にある（一度だけ）'
    assert not os.path.exists(REQ), '受付番号の記録が既にある（送り直しは一度だけ）'
    raw = open(os.path.join(HERE, 'grok-followup1-message.md'), 'rb').read().replace(b'\r\n', b'\n')
    msg_sha = hashlib.sha256(raw).hexdigest().upper()[:16]
    assert msg_sha == MSG_SHA16, ('発話の SHA が決めた値と違う', msg_sha)
    msg = raw.decode('utf-8')
    key = load_key('XAI_API_KEY')
    hdr = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key}
    body = {'model': MODEL, 'messages': [{'role': 'user', 'content': msg}], 'max_tokens': 60000, 'deferred': True}
    t0 = time.time()
    print('[%s] 送る（後で受け取る形・発話 SHA16 %s・%d 字）' % (now(), msg_sha, len(msg)))
    try:
        r = urllib.request.urlopen(urllib.request.Request('https://api.x.ai/v1/chat/completions', data=json.dumps(body).encode('utf-8'), headers=hdr), timeout=300)
        d0 = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        sys.exit('送りが受け付けられなかった HTTP %d: %s' % (e.code, e.read().decode('utf-8', 'replace')[:500]))
    rid = d0.get('request_id')
    if not rid:
        sys.exit('受付番号が返らなかった（送り直さない）: %s' % json.dumps(d0, ensure_ascii=False)[:500])
    with open(REQ, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump({'request_id': rid, 'sent_jst': now(), 'model': MODEL, 'message_sha16': msg_sha, 'kind': 'followup1', 'registrant_permission': 'D276'}, fh, ensure_ascii=False, indent=1)
    print('[%s] 受付番号を受けた（deferred-request.json に書いた）。答えを 30 秒おきに取りに行く' % now())
    url = 'https://api.x.ai/v1/chat/deferred-completion/' + rid
    last_note = 0
    while True:
        el = time.time() - t0
        if el > LIMIT:
            sys.exit('[%s] %d 秒待っても答えが来なかった（受付番号は deferred-request.json・送り直さずに止める）' % (now(), LIMIT))
        time.sleep(POLL)
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=120)
            status = r.status
            txt = r.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            sys.exit('[%s] 答えを取りに行って断られた HTTP %d: %s' % (now(), e.code, e.read().decode('utf-8', 'replace')[:500]))
        except Exception as e:
            print('[%s] 取りに行く途中の誤り（続ける）: %s' % (now(), type(e).__name__))
            continue
        if status == 202 or not txt.strip():
            if el - last_note >= 300:
                print('[%s] まだ（%.0f 秒）' % (now(), el))
                last_note = el
            continue
        if status != 200:
            sys.exit('[%s] 答えの返りが決まりの外 %d: %s' % (now(), status, txt[:300]))
        d = json.loads(txt)
        break
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
    meta = {'model_requested': MODEL, 'model_returned': d.get('model'), 'time_jst': now(), 'seconds_from_send': round(secs, 1), 'message_sha16': msg_sha, 'message_chars': len(msg),
            'mode': 'deferred（後で受け取る形）', 'request_id': rid, 'kind': '追い問い（一度目・G-01）',
            'usage': u, 'est_usd_with_reasoning': round(usd, 6), 'ticks_usd': (None if ticks is None else round(ticks * 1e-10, 6)), 'cap_usd': CAP, 'registrant_permission': 'D276',
            'response_sha16': hashlib.sha256(content.encode('utf-8')).hexdigest().upper()[:16], 'finish_reason': d['choices'][0].get('finish_reason'),
            'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('done | model', meta['model_returned'], '| in', pin, '(cached', cached, ') | out', pout, '(reasoning', reasoning, ') | USD', meta['est_usd_with_reasoning'], '| ticks USD', meta['ticks_usd'],
          '| secs', meta['seconds_from_send'], '| finish', meta['finish_reason'], '| response chars', len(content))


if __name__ == '__main__':
    main()
