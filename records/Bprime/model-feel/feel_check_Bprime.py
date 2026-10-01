# -*- coding: utf-8 -*-
"""B′ の機種選びのための日英の感触の確かめ（枠 `frame-model-feel-Bprime.md`・応答を見る前に書いた）。
用法:
  python feel_check_Bprime.py run       # Nscale で 32 回呼ぶ・生の記録（一度だけ）・日本語の盲検の一覧と対応を別々に書く（中身は表示しない）
  python feel_check_Bprime.py unblind   # 起草者の判じ（控えつき）を読んでから対応を開き、機種ごとの一覧と機械の数えを書く
  python feel_check_Bprime.py final     # 英語の判じ（盲検でない）を足して、まとめを書く
鍵は読むだけで、表示しない。場面と腕は使わない（中立の課題だけ）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, time, random, hashlib, datetime, urllib.request, urllib.error, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
H = lambda n: os.path.join(HERE, n)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
jst = lambda: (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
ENV_FILE = os.environ.get('OP4B_ENV_FILE', 'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
URL = 'https://inference.api.nscale.com/v1/chat/completions'
MODELS = {'8B': 'meta-llama/Llama-3.1-8B-Instruct', 'Scout': 'meta-llama/Llama-4-Scout-17B-16E-Instruct'}
PRICE = {'8B': (0.06, 0.06), 'Scout': (0.09, 0.29)}   # 百万トークンあたりのドル（Nscale の機種の一覧・2026-09-29）
SYSTEM = {'ja': 'あなたは有用なアシスタントです。', 'en': 'You are a helpful assistant.'}
TASKS = {
    1: {'ja': '梅雨の時期に洗濯物を部屋の中で早く乾かす工夫を三つ、丁寧語で、番号つきの箇条書きで説明してください。',
        'en': 'Please explain three tips for drying laundry indoors quickly during the rainy season, as a numbered list, in a polite tone.'},
    2: {'ja': '次の文を、上司に送る丁寧なメールの文面に書き換えてください。' + NL + '「明日の会議、ちょっと遅れるかも。資料は先に送っとくね。」',
        'en': 'Rewrite the following as a polite email to your manager.' + NL + '"Might be a bit late to tomorrow\'s meeting. I\'ll send the slides ahead."'},
    3: {'ja': '次の文章を二文で要約してください。' + NL + '「図書館は本を借りる場所であるだけでなく、地域の人が集まり学び合う場でもある。近年は、子ども向けの読み聞かせ会や、高齢者向けのデジタル機器の講座を開く図書館が増えている。一方で、予算の削減により開館時間を短くせざるを得ない館もある。」',
        'en': 'Summarize the following passage in two sentences.' + NL + '"A library is not only a place to borrow books but also a place where people in the community gather and learn from one another. In recent years, more libraries have been holding story-time sessions for children and digital-device classes for older adults. On the other hand, some libraries have had to shorten their opening hours because of budget cuts."'},
    4: {'ja': '次の三つのうち、ビタミン C を最も多く含む果物を選んでください。理由を一文で述べ、最後の行に {"answer": "?"} の形の JSON を一行だけ書いてください（? には a・b・c のどれか一文字を入れる）。' + NL + 'a: りんご' + NL + 'b: キウイフルーツ' + NL + 'c: バナナ',
        'en': 'Of the following three, choose the fruit that contains the most vitamin C. Give your reason in one sentence, and on the last line write exactly one line of JSON in the form {"answer": "?"} (replace ? with one letter: a, b, or c).' + NL + 'a: apple' + NL + 'b: kiwifruit' + NL + 'c: banana'},
}
N_SAMPLES, TEMP, MAXTOK, SEED = 2, 0.7, 700, 20260929
RAW, BLIND, KEY = 'raw-feel-Bprime.jsonl', 'blind-ja.md', 'key-ja.json'
JUDJA, JUDJA_ST, JUDEN, VIEW, OUT = 'judgments-ja.md', 'judgments-ja-stamp.txt', 'judgments-en.md', 'view-by-model.md', 'feel-check-Bprime.md'
FENCE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
SIMPLIFIED = '们这说为时对么还关东车边过进长门问间题见觉让认识语'   # 日本語では使わない簡体字の目安（枠の後・応答を生成する前に足した）


def load_key(name):
    k = os.environ.get(name)
    if k:
        return k.strip()
    for line in open(ENV_FILE, encoding='utf-8'):
        line = line.strip()
        if line.startswith(name + '=') and len(line) > len(name) + 1:
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    sys.exit('鍵が見つからない')


def call(key, model, lang, task):
    body = json.dumps({'model': model, 'messages': [{'role': 'system', 'content': SYSTEM[lang]}, {'role': 'user', 'content': TASKS[task][lang]}],
                       'temperature': TEMP, 'max_tokens': MAXTOK}).encode('utf-8')
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL, data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
            d = json.loads(urllib.request.urlopen(req, timeout=180).read().decode('utf-8'))
            ch = d['choices'][0]
            return {'text': ch['message'].get('content') or '', 'finish_reason': ch.get('finish_reason'), 'usage': d.get('usage'), 'attempts': attempt + 1, 'error': None}
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
            last = '%s: %s' % (type(e).__name__, str(e)[:200])
            time.sleep(3 * (attempt + 1))
    return {'text': '', 'finish_reason': None, 'usage': None, 'attempts': 4, 'error': last}


def checks(r):
    t = r['text']
    lines = [l for l in t.split(NL) if l.strip()]
    c = {'chars': len(t), 'hangul': len(re.findall('[\u1100-\u11ff\u3130-\u318f\uac00-\ud7a3]', t)),
         'simplified': sum(t.count(ch) for ch in SIMPLIFIED)}
    body = t
    if r['task'] == 4 and lines:
        last = lines[-1].strip().strip('`').strip()
        try:
            j = json.loads(last)
            ok = isinstance(j, dict) and set(j) == {'answer'} and j['answer'] in ('a', 'b', 'c')
            c['json_last_line'] = 'ok:' + j['answer'] if ok else 'bad-shape'
        except Exception:
            c['json_last_line'] = 'not-json'
        body = NL.join(lines[:-1])
    if r['task'] == 1:
        c['numbered_items'] = len(re.findall('(?m)^[ \t]*(?:[*#]*[ \t]*)?(?:[0-9]+|[０-９]+)[ \t]*[.．)）、]', t))
    if r['lang'] == 'ja':
        c['latin_words'] = len(re.findall('[A-Za-z]{2,}', body))
    return c


def cmd_run():
    assert not os.path.exists(H(RAW)), '生の記録は既にある（一度だけ）'
    st = open(H('frame-stamp.txt'), encoding='utf-8').read()
    assert s16(H('frame-model-feel-Bprime.md')) in st, '枠が控えと違う（止める）'
    key = load_key('NSCALE_API_KEY')
    jobs = [(m, lang, task, s) for m in MODELS for lang in ('ja', 'en') for task in TASKS for s in range(1, N_SAMPLES + 1)]
    recs = []
    t0 = time.time()
    for i, (m, lang, task, s) in enumerate(jobs, 1):
        r = call(key, MODELS[m], lang, task)
        recs.append(dict(model_key=m, model=MODELS[m], lang=lang, task=task, sample=s, time_jst=jst(), system=SYSTEM[lang], prompt=TASKS[task][lang],
                         temperature=TEMP, max_tokens=MAXTOK, **r))
        print('%d/%d done%s' % (i, len(jobs), '' if r['error'] is None else ' (error)'))
    with open(H(RAW), 'w', encoding='utf-8', newline=NL) as fo:
        for r in recs:
            fo.write(json.dumps(r, ensure_ascii=False) + NL)
    ja = [r for r in recs if r['lang'] == 'ja']
    ids = ['J%02d' % (k + 1) for k in range(len(ja))]
    order = list(range(len(ja)))
    random.Random(SEED).shuffle(order)
    key_map = {ids[k]: {'model_key': ja[order[k]]['model_key'], 'task': ja[order[k]]['task'], 'sample': ja[order[k]]['sample']} for k in range(len(ja))}
    json.dump(key_map, open(H(KEY), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    L = ['# 日本語の応答の盲検の一覧（並べ替えて番号だけを付けた・機種は伏せた・`feel_check_Bprime.py run`）', '',
         '- 読む人は、`%s` を開く前に、この一覧だけを読んで `%s` に判じを書き、控え `%s` を取る。' % (KEY, JUDJA, JUDJA_ST), '']
    for k in range(len(ja)):
        r = ja[order[k]]
        L += ['## %s（課題 %d）' % (ids[k], r['task']), '', '~~~~text', r['text'].rstrip(), '~~~~', '']
    L += [FENCE, '']
    open(H(BLIND), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    tok = {m: [0, 0] for m in MODELS}
    for r in recs:
        u = r['usage'] or {}
        tok[r['model_key']][0] += u.get('prompt_tokens', 0)
        tok[r['model_key']][1] += u.get('completion_tokens', 0)
    usd = sum(tok[m][0] / 1e6 * PRICE[m][0] + tok[m][1] / 1e6 * PRICE[m][1] for m in MODELS)
    print('calls', len(recs), '| errors', sum(1 for r in recs if r['error']), '| retries', sum(r['attempts'] - 1 for r in recs), '| tokens in/out', {m: tuple(v) for m, v in tok.items()},
          '| est. USD %.5f' % usd, '| %.0f s' % (time.time() - t0), '| raw', s16(H(RAW)), '| blind', s16(H(BLIND)))


def parse_judgments(path, id_re):
    rows = {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\| (%s) \| (有|無) \| (.*?) \| (.*?) \|\s*$' % id_re, line.rstrip(NL))
        if m:
            rows[m.group(1)] = {'flag': m.group(2), 'quote': m.group(3).strip(), 'guess': m.group(4).strip()}
    return rows


def quotes_ok(quote_cell, text):
    qs = re.findall('「([^「」]*)」', quote_cell)
    return all(q in text for q in qs), len(qs)


def cmd_unblind():
    st = open(H(JUDJA_ST), encoding='utf-8').read()
    assert s16(H(JUDJA)) in st, '日本語の判じが控えと違う（止める）'
    recs = [json.loads(l) for l in open(H(RAW), encoding='utf-8') if l.strip()]
    key_map = json.load(open(H(KEY), encoding='utf-8'))
    J = parse_judgments(H(JUDJA), 'J[0-9][0-9]')
    assert set(J) == set(key_map), ('判じの番号が一覧と合わない', sorted(set(key_map) - set(J)))
    ja = {(r['model_key'], r['task'], r['sample']): r for r in recs if r['lang'] == 'ja'}
    res = {}
    for i, k in key_map.items():
        r = ja[(k['model_key'], k['task'], k['sample'])]
        ok, nq = quotes_ok(J[i]['quote'], r['text'])
        assert ok, ('引用が応答に一字違わず無い（止める）', i)
        assert J[i]['flag'] == '無' or nq >= 1, ('有と判じたのに引用が無い（止める）', i)
        res[i] = dict(k, flag=J[i]['flag'], n_quotes=nq, guess=J[i]['guess'], hit=(J[i]['guess'] == k['model_key']))
    json.dump(res, open(H('unblind-ja.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    L = ['# 機種ごとの応答の一覧（対応を開いた後・`feel_check_Bprime.py unblind`）', '']
    inv = {(k['model_key'], k['task'], k['sample']): i for i, k in key_map.items()}
    for m in MODELS:
        L += ['## %s（`%s`）' % (m, MODELS[m]), '']
        for lang in ('ja', 'en'):
            for r in [x for x in recs if x['model_key'] == m and x['lang'] == lang]:
                c = checks(r)
                tag = ('・盲検の番号 %s・判じ %s' % (inv[(m, r['task'], r['sample'])], res[inv[(m, r['task'], r['sample'])]]['flag'])) if lang == 'ja' else ''
                L += ['### %s・%s・課題 %d・%d 回目%s' % (m, {'ja': '日本語', 'en': '英語'}[lang], r['task'], r['sample'], tag), '',
                      '- 機械の数え: ' + '・'.join('%s %s' % (a, b) for a, b in c.items()) + '・終わりの理由 %s' % r['finish_reason'], '', '~~~~text', r['text'].rstrip(), '~~~~', '']
    L += [FENCE, '']
    open(H(VIEW), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    for m in MODELS:
        v = [x for x in res.values() if x['model_key'] == m]
        print(m, '| ja flagged', sum(1 for x in v if x['flag'] == '有'), '/', len(v))
    print('guess hits', sum(1 for x in res.values() if x['hit']), '/', len(res), '| view', s16(H(VIEW)))


def cmd_final():
    recs = [json.loads(l) for l in open(H(RAW), encoding='utf-8') if l.strip()]
    res = json.load(open(H('unblind-ja.json'), encoding='utf-8'))
    E = parse_judgments(H(JUDEN), '(?:8B|Scout)-en-t[1-4]-s[12]')
    en = {'%s-en-t%d-s%d' % (r['model_key'], r['task'], r['sample']): r for r in recs if r['lang'] == 'en'}
    assert set(E) == set(en), ('英語の判じの番号が合わない', sorted(set(en) - set(E)))
    for i, e in E.items():
        ok, nq = quotes_ok(e['quote'], en[i]['text'])
        assert ok and (e['flag'] == '無' or nq >= 1), ('英語の判じの引用', i)
    C = {(r['model_key'], r['lang'], r['task'], r['sample']): checks(r) for r in recs}
    T = {}
    for m in MODELS:
        ja_flag = sum(1 for x in res.values() if x['model_key'] == m and x['flag'] == '有')
        en_flag = sum(1 for i, e in E.items() if i.startswith(m + '-') and e['flag'] == '有')
        js = [C[(m, l, 4, s)].get('json_last_line', '') for l in ('ja', 'en') for s in (1, 2)]
        T[m] = {'ja_flag': ja_flag, 'en_flag': en_flag, 'json_ok': sum(1 for x in js if x.startswith('ok:')), 'json_all': js,
                'hangul_ja': sum(C[(m, 'ja', t, s)]['hangul'] for t in TASKS for s in (1, 2)),
                'simplified_ja': sum(C[(m, 'ja', t, s)]['simplified'] for t in TASKS for s in (1, 2)),
                'latin_ja': sum(C[(m, 'ja', t, s)]['latin_words'] for t in TASKS for s in (1, 2)),
                'numbered': [C[(m, l, 1, s)]['numbered_items'] for l in ('ja', 'en') for s in (1, 2)],
                'errors': sum(1 for r in recs if r['model_key'] == m and r['error'])}
    hits = sum(1 for x in res.values() if x['hit'])
    n_ja = {m: sum(1 for x in res.values() if x['model_key'] == m) for m in MODELS}
    judge = lambda ok: '当たり' if ok else '外れ'
    L = ['# B′ の機種選びのための日英の感触の確かめ（まとめ・機械生成・`feel_check_Bprime.py final`）', '',
         '- 枠: `frame-model-feel-Bprime.md`（応答を生成する前に書いた・控え `frame-stamp.txt`）。生の記録 `%s`（SHA16 %s）。日本語の盲検の一覧 `%s`（SHA16 %s）。日本語の判じ `%s`（SHA16 %s・対応を開く前の控え `%s`）。英語の判じ `%s`（SHA16 %s・盲検でない）。機種ごとの一覧 `%s`（SHA16 %s）。' % (
             RAW, s16(H(RAW)), BLIND, s16(H(BLIND)), JUDJA, s16(H(JUDJA)), JUDJA_ST, JUDEN, s16(H(JUDEN)), VIEW, s16(H(VIEW))),
         '- 呼び方: Nscale の API・system は中立の一文・temperature %.1f・max_tokens %d・各題 × 各言語 × 各機種 %d 回。場面と腕は使っていない。' % (TEMP, MAXTOK, N_SAMPLES),
         '- 判じは起草者（Claude 系）一名の目。日本語は盲検（機種の推測の当たり %d／%d）、英語は盲検でない。これは感触の記録で、検定ではない。' % (hits, len(res)), '',
         '## 1. 機種ごとの数え', '',
         '| 何 | %s |' % ' | '.join(MODELS), '|---|' + '---|' * len(MODELS),
         '| 日本語で明らかな誤りか不自然と判じた応答 | %s |' % ' | '.join('%d／%d' % (T[m]['ja_flag'], n_ja[m]) for m in MODELS),
         '| 英語で明らかな誤りと判じた応答 | %s |' % ' | '.join('%d／8' % T[m]['en_flag'] for m in MODELS),
         '| 課題 4 の最後の行の JSON が読めて答えが a・b・c | %s |' % ' | '.join('%d／4（%s）' % (T[m]['json_ok'], '・'.join(T[m]['json_all'])) for m in MODELS),
         '| 課題 1 の番号つきの項目の数（日 1・日 2・英 1・英 2） | %s |' % ' | '.join('・'.join(str(x) for x in T[m]['numbered']) for m in MODELS),
         '| 日本語の応答の中のハングルの字 | %s |' % ' | '.join(str(T[m]['hangul_ja']) for m in MODELS),
         '| 日本語の応答の中の簡体字の目安（枠の後・生成の前に足した） | %s |' % ' | '.join(str(T[m]['simplified_ja']) for m in MODELS),
         '| 日本語の応答の中のラテン文字の語（課題 4 の JSON の行を除く） | %s |' % ' | '.join(str(T[m]['latin_ja']) for m in MODELS),
         '| 呼び出しの誤り | %s |' % ' | '.join(str(T[m]['errors']) for m in MODELS), '',
         '## 2. 枠の予想と照らす（外れても消さない）', '',
         '| 何 | 予想 | 結果 | 照らし |', '|---|---|---|---|',
         '| 8B の日本語の誤りか不自然 | 4 以上（8 のうち） | %d | %s |' % (T['8B']['ja_flag'], judge(T['8B']['ja_flag'] >= 4)),
         '| Scout の日本語の誤りか不自然 | 2 以下（8 のうち） | %d | %s |' % (T['Scout']['ja_flag'], judge(T['Scout']['ja_flag'] <= 2)),
         '| 課題 4 の JSON | 両機種とも 3 以上（4 のうち） | %d・%d | %s |' % (T['8B']['json_ok'], T['Scout']['json_ok'], judge(T['8B']['json_ok'] >= 3 and T['Scout']['json_ok'] >= 3)),
         '| 英語の明らかな誤り | 両機種とも 1 以下（8 のうち） | %d・%d | %s |' % (T['8B']['en_flag'], T['Scout']['en_flag'], judge(T['8B']['en_flag'] <= 1 and T['Scout']['en_flag'] <= 1)),
         '| ハングルの混入 | 8B で 1 以上・Scout で 0 | %d・%d | %s |' % (T['8B']['hangul_ja'], T['Scout']['hangul_ja'], judge(T['8B']['hangul_ja'] >= 1 and T['Scout']['hangul_ja'] == 0)),
         '| 機種の推測の当たり | 12 以上（16 のうち） | %d | %s |' % (hits, judge(hits >= 12)), '',
         '@@NOTES@@', '', FENCE, '']
    open(H(OUT), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print(json.dumps(T, ensure_ascii=False), '| hits', hits, '| out', s16(H(OUT)))


if __name__ == '__main__':
    {'run': cmd_run, 'unblind': cmd_unblind, 'final': cmd_final}[sys.argv[1]]()
