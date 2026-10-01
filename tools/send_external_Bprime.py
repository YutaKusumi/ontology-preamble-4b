# -*- coding: utf-8 -*-
"""send_external_Bprime.py v0.1 —— B′ の行動の下見の「系統外の模型による採点」の依頼を grok-4.7 に送る器（正本 `behavior_pilot.external_scoring`・草案10 §4.4・
設計の巡の `reviews/design-round3/send_grok.py` v1 の型・2026-09-30・コーディネータ南無弥勒如来）。

束の置き場（`close_behavior_Bprime.py bundle` が書いた `request.md`）の依頼の文を、一つの新しい呼び出しで送り、返事を返事の置き場に一度だけ書く（上書きしない）:
`response.md`（返事の本文・逐語）・`response-raw.json`（API の返事のまま）・`meta.json`（模型の名・system_fingerprint・時刻・依頼の文の SHA16・使った量と費用・登録者の言葉）。
**送る前に登録者の確認を得る**（外に出す操作・Gemma の応答の一部を xAI に渡す）。器は --go が無ければ送らない。登録者の言葉を --words に逐語で与え、meta に置く。
鍵は環境の変数か鍵のファイルから読むだけで、印字しない・記録に書かない・URL に入れない。標本化の値（温度など）は渡さない（正本に定めが無い・設計の巡の送信と同じ・meta に書く）。
用法: python tools/send_external_Bprime.py <束の置き場> <返事の置き場> --go --words "<登録者の逐語>" ／ --selftest（送らない）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, time, hashlib, datetime, argparse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VERSION = 'v0.1'        # v0.1（2026-09-30・器の実装の検分 U13・R2-20）: 依頼の文を改行を訳さずに読み、依頼の文の SHA16 をファイルのバイトで取る（閉じる器と同じ取り方・前は改行を訳して読み、Gemma の応答に \r があると閉じる器の照らしと合わなかった）。前の版は `prev/send_external_Bprime-v0.py`
MODEL = 'grok-4.7'
URL = 'https://api.x.ai/v1/chat/completions'
PRICE_IN, PRICE_CACHED, PRICE_OUT = 2.00, 0.50, 6.00      # 100 万トークンあたりのドル（設計の巡の送信の器と同じ値・2026-09-29 の xAI の API の機種の一覧）
ENV_FILE = os.environ.get('OP4B_ENV_FILE', 'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
NL = chr(10)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def load_key(name, env_file=None):
    """鍵を読む（印字しない）。無ければ止める。"""
    k = os.environ.get(name)
    if k:
        return k.strip()
    with open(env_file or ENV_FILE, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(name + '=') and len(line) > len(name) + 1:
                return line.split('=', 1)[1].strip().strip('"').strip("'")
    sys.exit('鍵が見つからない')


def read_request(path):
    """依頼の文を改行を訳さずに読み（\r も \r\n もそのまま）、SHA16 はファイルのバイトで取る（閉じる器の `sha16raw` と同じ・v0.1・U13）。"""
    with open(path, 'rb') as fh:
        b = fh.read()
    return b.decode('utf-8'), hashlib.sha256(b).hexdigest().upper()[:16]


def body_of(req_text):
    return {'model': MODEL, 'messages': [{'role': 'user', 'content': req_text}], 'max_tokens': 60000}


def wjson(path, obj):
    with open(path, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def send(bundle_dir, reply_dir, words, key_name='XAI_API_KEY'):
    if os.path.exists(reply_dir):
        sys.exit('返事の置き場は既にある（一度だけ書く）')
    C = json.load(open(os.path.join(ROOT, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    if MODEL not in C['behavior_pilot']['external_scoring']['scorer']:
        sys.exit('正本の採点する者の機種と、器の機種が違う')
    req, req_sha16 = read_request(os.path.join(bundle_dir, 'request.md'))
    key = load_key(key_name)
    t0 = time.time()
    rq = urllib.request.Request(URL, data=json.dumps(body_of(req)).encode('utf-8'), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    try:
        d = json.loads(urllib.request.urlopen(rq, timeout=3600).read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        sys.exit('HTTP %d（呼び出しの失敗・閉じるときは --fail に理由を書く）: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300]))
    secs = time.time() - t0
    os.makedirs(reply_dir)
    content = d['choices'][0]['message'].get('content') or ''
    with open(os.path.join(reply_dir, 'response.md'), 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(content)
    wjson(os.path.join(reply_dir, 'response-raw.json'), d)
    u = d.get('usage') or {}
    pin, pout = u.get('prompt_tokens', 0), u.get('completion_tokens', 0)
    cached = (u.get('prompt_tokens_details') or {}).get('cached_tokens', 0)
    reasoning = (u.get('completion_tokens_details') or {}).get('reasoning_tokens', 0)
    usd = (pin - cached) / 1e6 * PRICE_IN + cached / 1e6 * PRICE_CACHED + (pout + reasoning) / 1e6 * PRICE_OUT
    ticks = u.get('cost_in_usd_ticks')
    meta = {'kind': 'bprime_external_scoring_call', 'tool': 'send_external_Bprime.py %s' % VERSION, 'model_requested': MODEL, 'model_returned': d.get('model'),
            'system_fingerprint': d.get('system_fingerprint'), 'time_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            'seconds': round(secs, 1), 'request_sha16': req_sha16, 'request_chars': len(req), 'sampling': '渡していない（API の既定）', 'usage': u,
            'est_usd_with_reasoning': round(usd, 6), 'ticks_usd': (None if ticks is None else round(ticks * 1e-10, 6)), 'finish_reason': d['choices'][0].get('finish_reason'),
            'response_sha16': hashlib.sha256(content.encode('utf-8')).hexdigest().upper()[:16], 'registrant_words': words, 'clause': CLAUSE}
    wjson(os.path.join(reply_dir, 'meta.json'), meta)
    print('done | model', meta['model_returned'], '| in', pin, '| out', pout, '(reasoning', reasoning, ') | USD', meta['est_usd_with_reasoning'], '| secs', meta['seconds'],
          '| finish', meta['finish_reason'], '| response chars', len(content))
    return meta


def _selftest():
    import io, tempfile, contextlib
    fake = 'SELFTEST-NOT-A-KEY-0000'
    with tempfile.TemporaryDirectory() as td:
        ef = os.path.join(td, 'env')
        with open(ef, 'w', encoding='utf-8') as fh:
            fh.write('OTHER=1' + NL + 'OP4B_SELFTEST_KEY="%s"' % fake + NL)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            k = load_key('OP4B_SELFTEST_KEY', env_file=ef)
        assert k == fake and fake not in buf.getvalue(), '鍵の読み方'
        b = body_of('依頼')
        assert b['model'] == MODEL and 'temperature' not in b and b['messages'][0]['content'] == '依頼'
        # 依頼の文は改行を訳さずに読み、SHA16 はバイトで取る（v0.1・U13）
        rp = os.path.join(td, 'request.md')
        raw = ('依頼' + NL + '応答の中の \r だけ' + chr(13) + 'と \r\n' + chr(13) + NL + '終わり' + NL).encode('utf-8')
        with open(rp, 'wb') as fh:
            fh.write(raw)
        t_, s_ = read_request(rp)
        assert t_.encode('utf-8') == raw and s_ == hashlib.sha256(raw).hexdigest().upper()[:16], '依頼の文の読み方'
        # --go が無ければ送らない
        rc = main_args(['x', 'y'], dry=True)
        assert rc == 'no_go'
    print('send_external_Bprime.py %s SELFTEST PASS（鍵を読むが印字しない・送る本文・依頼の文を改行を訳さずに読む・--go が無ければ送らない・送る操作はしていない）' % VERSION)


def main_args(argv, dry=False):
    ap = argparse.ArgumentParser()
    ap.add_argument('bundle')
    ap.add_argument('reply')
    ap.add_argument('--go', action='store_true')
    ap.add_argument('--words')
    a = ap.parse_args(argv)
    if not a.go or not a.words:
        if dry:
            return 'no_go'
        sys.exit('送らなかった（送る前に登録者の確認を得て、--go と --words "<登録者の逐語>" を与える）')
    return send(a.bundle, a.reply, a.words)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    main_args(sys.argv[1:])
