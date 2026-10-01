# -*- coding: utf-8 -*-
"""send_grok_followup.py v0（2026-09-29・B′ の設計の巡・二巡目・grok-4.7 への追い問い・一巡目の器の定数を替えたもの・コーディネータ南無弥勒如来）。
枠（`00-frame-design-round1.md`）の「重大と書かれた指摘と、判断に迷う指摘は、追い問いで確かめてから採否を決める」による。
会話の形: 一つ目の発話（`build_message.build()`・送ったものと SHA が同じことを確かめる）→ grok-4.7 の一つ目の返事（`votes/grok-4.7/response.md`・SHA を確かめる）→ 追い問い（`followup2-grok.md`）。
返事は `votes/grok-4.7-followup1/` に一度だけ書く（上書きしない）。鍵は読むだけで、表示しない。費用は考える分を出力の値段で数え、API の `cost_in_usd_ticks` を並べて記す。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, time, hashlib, datetime, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'votes', 'grok-4.7-followup1')
FIRST = os.path.join(HERE, 'votes', 'grok-4.7', 'response.md')
QUESTION = os.path.join(HERE, 'followup2-grok.md')
MODEL = 'grok-4.7'
MSG_SHA16, FIRST_SHA16 = 'A2A9F7EB47F5270A', '0B848AD9864D8FC7'
PRICE_IN, PRICE_CACHED, PRICE_OUT = 2.00, 0.50, 6.00      # 100 万トークンあたりのドル（send_grok.py と同じ）
SPENT_BEFORE = 0.57436                                      # 二巡目の一つ目の票の費用（votes/grok-4.7/meta.json の tick の値）
CAP = 5.00
ENV_FILE = os.environ.get('OP4B_ENV_FILE', 'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
NL = chr(10)


def sha16s(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest().upper()[:16]


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
    assert sha16s(msg) == MSG_SHA16, '一つ目の発話の SHA が合わない'
    first = open(FIRST, 'rb').read().decode('utf-8')
    assert sha16s(first) == FIRST_SHA16, '一つ目の返事の SHA が合わない'
    q = open(QUESTION, 'rb').read().decode('utf-8')
    messages = [{'role': 'user', 'content': msg}, {'role': 'assistant', 'content': first}, {'role': 'user', 'content': q}]
    key = load_key('XAI_API_KEY')
    body = {'model': MODEL, 'messages': messages, 'max_tokens': 60000}
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
            'seconds': round(secs, 1), 'first_message_sha16': MSG_SHA16, 'first_response_sha16': FIRST_SHA16, 'question_sha16': sha16s(q),
            'usage': u, 'est_usd_with_reasoning': round(usd, 6), 'ticks_usd': (None if ticks is None else round(ticks * 1e-10, 6)),
            'spent_round_after': round(SPENT_BEFORE + (usd if ticks is None else ticks * 1e-10), 6), 'cap_usd': CAP,
            'response_sha16': sha16s(content), 'finish_reason': d['choices'][0].get('finish_reason')}
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('done | model', meta['model_returned'], '| in', pin, '(cached', cached, ') | out', pout, '(reasoning', reasoning, ') | USD', meta['est_usd_with_reasoning'], '| ticks USD', meta['ticks_usd'],
          '| round total', meta['spent_round_after'], '| secs', meta['seconds'], '| finish', meta['finish_reason'], '| chars', len(content))


if __name__ == '__main__':
    main()
