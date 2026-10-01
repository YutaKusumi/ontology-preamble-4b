# -*- coding: utf-8 -*-
"""B′ の機種選びのための日英の感触の確かめ・二巡目（枠 `frame-model-feel-Bprime-2.md`・応答を見る前に書いた）。
用法:
  python feel_check_Bprime_2.py run-gemma                      # Gemini の API で gemma-4 の二機種 × 16 回（生の記録は一度だけ・中身は表示しない）
  python feel_check_Bprime_2.py make-colab                     # Colab で Swallow を動かす台本 swallow_feel_colab.py を書く
  python feel_check_Bprime_2.py ingest-swallow <path> <sha16>  # Colab から持ち帰った生の記録を置く（一度だけ・Colab で出した SHA16 と照らす・中身は表示しない）
  python feel_check_Bprime_2.py blind                          # 日本語 24 を並べ替えた盲検の一覧と対応を別々に書く（中身は表示しない）
  python feel_check_Bprime_2.py unblind                        # 日本語の判じの控えを確かめてから対応を開き、機種ごとの一覧を書く
  python feel_check_Bprime_2.py final                          # 英語の判じを足してまとめを書く
課題と system は一巡目の台本 `../model-feel/feel_check_Bprime.py` から読み込む。鍵は読むだけで、表示しない（鍵は URL に入れない）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, time, random, hashlib, datetime, shutil, importlib.util, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('fc1', os.path.join(HERE, '..', 'model-feel', 'feel_check_Bprime.py'))
FC1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FC1)          # 一巡目の台本を読み込む（標準出力は一巡目の台本が utf-8 に包む）
NL = chr(10)
H = lambda n: os.path.join(HERE, n)
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda p: s16b(open(p, 'rb').read())
jst = lambda: (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
SYSTEM, TASKS = FC1.SYSTEM, FC1.TASKS
TASKS_SHA = s16b(json.dumps({'system': SYSTEM, 'tasks': {str(k): v for k, v in TASKS.items()}}, ensure_ascii=False, sort_keys=True).encode('utf-8'))
TEMP, MAXTOK, N_SAMPLES, SEED = FC1.TEMP, FC1.MAXTOK, FC1.N_SAMPLES, 20260929 + 2
GEMMA = {'31B': 'gemma-4-31b-it', '26B': 'gemma-4-26b-a4b-it'}
SWALLOW = 'tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.5'
MODELS = ['31B', '26B', 'Swallow']
NAME = {'31B': 'gemma-4-31b-it（Gemini の API）', '26B': 'gemma-4-26b-a4b-it（Gemini の API）', 'Swallow': SWALLOW + '（Colab・bf16）'}
RAW_G, RAW_G2, RAW_S = 'raw-gemma.jsonl', 'raw-gemma-nothink.jsonl', 'raw-swallow.jsonl'   # 盲検の一覧には RAW_G2 を使う（逸脱 1）
BLIND, KEY, JUDJA, JUDJA_ST, JUDEN, VIEW, OUT = 'blind-ja-2.md', 'key-ja-2.json', 'judgments-ja-2.md', 'judgments-ja-2-stamp.txt', 'judgments-en-2.md', 'view-by-model-2.md', 'feel-check-Bprime-2.md'
FENCE = FC1.FENCE
SIMPLIFIED = FC1.SIMPLIFIED + '减发经应实现济类产业务动种处'   # 一巡目の一覧に、漏れた「减」と日本語では使わない簡体字を足した（枠の見方 3・生成の前）


THINK = None   # 逸脱 1: 取り直しでは 'minimal'（`deviation-1-gemma-thinking.md`）


def gemini_call(key, model, lang, task):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent' % model
    mode = 'system'
    last = None
    for attempt in range(6):
        if mode == 'system':
            body = {'systemInstruction': {'parts': [{'text': SYSTEM[lang]}]}, 'contents': [{'role': 'user', 'parts': [{'text': TASKS[task][lang]}]}]}
        else:
            body = {'contents': [{'role': 'user', 'parts': [{'text': SYSTEM[lang] + NL + NL + TASKS[task][lang]}]}]}
        body['generationConfig'] = {'temperature': TEMP, 'maxOutputTokens': MAXTOK}
        if THINK:
            body['generationConfig']['thinkingConfig'] = {'thinkingLevel': THINK}
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json', 'x-goog-api-key': key})
            d = json.loads(urllib.request.urlopen(req, timeout=240).read().decode('utf-8'))
            c = d['candidates'][0]
            parts = (c.get('content') or {}).get('parts') or []
            text = ''.join(p.get('text', '') for p in parts if not p.get('thought'))
            return {'text': text, 'n_thought_parts': sum(1 for p in parts if p.get('thought')), 'thought_chars': sum(len(p.get('text', '')) for p in parts if p.get('thought')),
                    'thinking_level': THINK, 'finish_reason': c.get('finishReason'), 'usage': d.get('usageMetadata'), 'system_mode': mode, 'attempts': attempt + 1, 'error': None}
        except urllib.error.HTTPError as e:
            msg = e.read().decode('utf-8', 'replace')[:300]
            last = 'HTTP %d: %s' % (e.code, msg)
            if e.code == 400 and mode == 'system' and re.search('(?i)system|developer instruction', msg):
                mode = 'prepended'
                continue
            time.sleep(5 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError, IndexError) as e:
            last = '%s: %s' % (type(e).__name__, str(e)[:200])
            time.sleep(5 * (attempt + 1))
    return {'text': '', 'n_thought_parts': 0, 'finish_reason': None, 'usage': None, 'system_mode': mode, 'attempts': 6, 'error': last}


def cmd_run_gemma(nothink=False):
    global THINK
    out = RAW_G2 if nothink else RAW_G
    THINK = 'minimal' if nothink else None
    assert not os.path.exists(H(out)), '生の記録は既にある（一度だけ）'
    assert s16(H('frame-model-feel-Bprime-2.md')) in open(H('frame-stamp.txt'), encoding='utf-8').read(), '枠が控えと違う（止める）'
    key = FC1.load_key('GEMINI_API_KEY')
    jobs = [(m, lang, task, s) for m in ('31B', '26B') for lang in ('ja', 'en') for task in TASKS for s in range(1, N_SAMPLES + 1)]
    recs = []
    t0 = time.time()
    for i, (m, lang, task, s) in enumerate(jobs, 1):
        r = gemini_call(key, GEMMA[m], lang, task)
        recs.append(dict(model_key=m, model=GEMMA[m], place='gemini-api', lang=lang, task=task, sample=s, time_jst=jst(), system=SYSTEM[lang], prompt=TASKS[task][lang],
                         temperature=TEMP, max_tokens=MAXTOK, tasks_sha16=TASKS_SHA, **r))
        print('%d/%d done%s' % (i, len(jobs), '' if r['error'] is None else ' (error)'))
        time.sleep(2)
    with open(H(out), 'w', encoding='utf-8', newline=NL) as fo:
        for r in recs:
            fo.write(json.dumps(r, ensure_ascii=False) + NL)
    print('calls', len(recs), '| errors', sum(1 for r in recs if r['error']), '| retries', sum(r['attempts'] - 1 for r in recs),
          '| system_mode', sorted(set(r['system_mode'] for r in recs)), '| thought parts', sum(r['n_thought_parts'] for r in recs),
          '| thought chars', sum(r.get('thought_chars', 0) for r in recs), '| finish', sorted(set(str(r['finish_reason']) for r in recs)), '| %.0f s' % (time.time() - t0), '| raw', out, s16(H(out)))


COLAB_TPL = r'''# Colab（L4）で Swallow の日英の感触の応答を作る（B′ の機種選び・二巡目・中身は表示しない）
_=0;_=0;_=0
import os, json, time, hashlib
os.environ['HF_HUB_DISABLE_XET'] = '1'
os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'
import torch, transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
CFG = json.loads(r"""@@CFG@@""")
MID = CFG['model']
t0 = time.time()
tok = AutoTokenizer.from_pretrained(MID)
try:
    model = AutoModelForCausalLM.from_pretrained(MID, dtype=torch.bfloat16, device_map='cuda')
except TypeError:
    model = AutoModelForCausalLM.from_pretrained(MID, torch_dtype=torch.bfloat16, device_map='cuda')
model.eval()
eos = model.generation_config.eos_token_id
eos = set(eos if isinstance(eos, list) else [eos])
torch.manual_seed(CFG['seed'])
recs = []
for lang in ('ja', 'en'):
    for task in ('1', '2', '3', '4'):
        for s in range(1, CFG['n_samples'] + 1):
            msgs = [{'role': 'system', 'content': CFG['system'][lang]}, {'role': 'user', 'content': CFG['tasks'][task][lang]}]
            enc = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors='pt', return_dict=True)
            ids, att = enc['input_ids'].to('cuda'), enc['attention_mask'].to('cuda')
            with torch.no_grad():
                out = model.generate(input_ids=ids, attention_mask=att, do_sample=True, temperature=CFG['temperature'], top_p=1.0, top_k=0,
                                     max_new_tokens=CFG['max_tokens'], pad_token_id=tok.eos_token_id)
            gen = out[0, ids.shape[1]:]
            text = tok.decode(gen, skip_special_tokens=True)
            fin = 'stop' if int(gen[-1]) in eos else ('length' if len(gen) >= CFG['max_tokens'] else 'other')
            recs.append({'model_key': 'Swallow', 'model': MID, 'place': 'colab-bf16', 'lang': lang, 'task': int(task), 'sample': s, 'system': CFG['system'][lang],
                         'prompt': CFG['tasks'][task][lang], 'temperature': CFG['temperature'], 'max_tokens': CFG['max_tokens'], 'tasks_sha16': CFG['tasks_sha16'],
                         'text': text, 'finish_reason': fin, 'usage': {'prompt_tokens': int(ids.shape[1]), 'completion_tokens': int(len(gen))}, 'error': None,
                         'system_mode': 'system', 'n_thought_parts': 0, 'attempts': 1})
            print('%s t%s s%d done (%d tok)' % (lang, task, s, len(gen)))
path = '/content/raw-swallow.jsonl'
open(path, 'w', encoding='utf-8', newline='\n').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
sha = hashlib.sha256(open(path, 'rb').read()).hexdigest().upper()[:16]
print('SWALLOW-DONE n=%d sha16=%s secs=%d transformers=%s torch=%s gpu=%s' % (len(recs), sha, time.time() - t0, transformers.__version__, torch.__version__, torch.cuda.get_device_name(0)))
from google.colab import files
files.download(path)
'''


def cmd_make_colab():
    cfg = {'model': SWALLOW, 'system': SYSTEM, 'tasks': {str(k): v for k, v in TASKS.items()}, 'temperature': TEMP, 'max_tokens': MAXTOK, 'n_samples': N_SAMPLES,
           'seed': SEED, 'tasks_sha16': TASKS_SHA}
    js = json.dumps(cfg, ensure_ascii=False)
    assert '"""' not in js
    code = COLAB_TPL.replace('@@CFG@@', js)
    open(H('swallow_feel_colab.py'), 'w', encoding='utf-8', newline=NL).write(code)
    print('colab script', s16(H('swallow_feel_colab.py')), '| tasks_sha16', TASKS_SHA)


def cmd_ingest_swallow(path, sha):
    assert not os.path.exists(H(RAW_S)), '既にある（一度だけ）'
    b = open(path, 'rb').read()
    got = hashlib.sha256(b).hexdigest().upper()[:16]
    assert got == sha.upper(), ('Colab で出した SHA16 と違う（止める）', got, sha)
    recs = [json.loads(l) for l in b.decode('utf-8').split(NL) if l.strip()]
    assert len(recs) == 16 and all(r['tasks_sha16'] == TASKS_SHA for r in recs) and all(r['model'] == SWALLOW for r in recs)
    open(H(RAW_S), 'wb').write(b)
    print('ingested', len(recs), '| sha16', got, '| finish', sorted(set(r['finish_reason'] for r in recs)), '| tokens out', sum(r['usage']['completion_tokens'] for r in recs))


def load_all():
    recs = [json.loads(l) for f in (RAW_G2, RAW_S) for l in open(H(f), encoding='utf-8') if l.strip()]
    assert len(recs) == 48 and all(r['tasks_sha16'] == TASKS_SHA for r in recs)
    return recs


def cmd_blind():
    assert not os.path.exists(H(BLIND)) and not os.path.exists(H(KEY)), '既にある（一度だけ）'
    recs = load_all()
    ja = [r for r in recs if r['lang'] == 'ja']
    order = list(range(len(ja)))
    random.Random(SEED).shuffle(order)
    ids = ['K%02d' % (k + 1) for k in range(len(ja))]
    key_map = {ids[k]: {'model_key': ja[order[k]]['model_key'], 'task': ja[order[k]]['task'], 'sample': ja[order[k]]['sample']} for k in range(len(ja))}
    json.dump(key_map, open(H(KEY), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    L = ['# 日本語の応答の盲検の一覧・二巡目（三機種を混ぜて並べ替え、番号だけを付けた・機種は伏せた・`feel_check_Bprime_2.py blind`）', '',
         '- 読む人は、`%s` を開く前に、この一覧だけを読んで `%s` に判じを書き、控え `%s` を取る。推測は 31B・26B・Swallow のどれか。' % (KEY, JUDJA, JUDJA_ST), '']
    for k in range(len(ja)):
        r = ja[order[k]]
        L += ['## %s（課題 %d）' % (ids[k], r['task']), '', '~~~~text', r['text'].rstrip(), '~~~~', '']
    L += [FENCE, '']
    open(H(BLIND), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('blind', s16(H(BLIND)), '| n', len(ja))


def checks(r):
    t = r['text']
    lines = [l for l in t.split(NL) if l.strip()]
    c = {'chars': len(t), 'hangul': len(re.findall('[ᄀ-ᇿ㄰-㆏가-힣]', t)), 'simplified': sum(t.count(ch) for ch in SIMPLIFIED)}
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


def cmd_unblind():
    assert s16(H(JUDJA)) in open(H(JUDJA_ST), encoding='utf-8').read(), '日本語の判じが控えと違う（止める）'
    recs = load_all()
    key_map = json.load(open(H(KEY), encoding='utf-8'))
    J = FC1.parse_judgments(H(JUDJA), 'K[0-9][0-9]')
    assert set(J) == set(key_map), ('判じの番号が一覧と合わない', sorted(set(key_map) - set(J)))
    ja = {(r['model_key'], r['task'], r['sample']): r for r in recs if r['lang'] == 'ja'}
    res = {}
    for i, k in key_map.items():
        r = ja[(k['model_key'], k['task'], k['sample'])]
        ok, nq = FC1.quotes_ok(J[i]['quote'], r['text'])
        assert ok, ('引用が応答に一字違わず無い（止める）', i)
        assert J[i]['flag'] == '無' or nq >= 1, ('有と判じたのに引用が無い（止める）', i)
        res[i] = dict(k, flag=J[i]['flag'], n_quotes=nq, guess=J[i]['guess'], hit=(J[i]['guess'] == k['model_key']))
    json.dump(res, open(H('unblind-ja-2.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    inv = {(k['model_key'], k['task'], k['sample']): i for i, k in key_map.items()}
    L = ['# 機種ごとの応答の一覧・二巡目（対応を開いた後・`feel_check_Bprime_2.py unblind`）', '']
    for m in MODELS:
        L += ['## %s（%s）' % (m, NAME[m]), '']
        for lang in ('ja', 'en'):
            for r in [x for x in recs if x['model_key'] == m and x['lang'] == lang]:
                c = checks(r)
                tag = ('・盲検の番号 %s・判じ %s' % (inv[(m, r['task'], r['sample'])], res[inv[(m, r['task'], r['sample'])]]['flag'])) if lang == 'ja' else ''
                L += ['### %s・%s・課題 %d・%d 回目%s' % (m, {'ja': '日本語', 'en': '英語'}[lang], r['task'], r['sample'], tag), '',
                      '- 機械の数え: ' + '・'.join('%s %s' % (a, b) for a, b in c.items()) + '・終わりの理由 %s・system %s・思考の部分 %s' % (r['finish_reason'], r['system_mode'], r['n_thought_parts']), '',
                      '~~~~text', r['text'].rstrip(), '~~~~', '']
    L += [FENCE, '']
    open(H(VIEW), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    for m in MODELS:
        v = [x for x in res.values() if x['model_key'] == m]
        print(m, '| ja flagged', sum(1 for x in v if x['flag'] == '有'), '/', len(v))
    print('guess hits', sum(1 for x in res.values() if x['hit']), '/', len(res), '| view', s16(H(VIEW)))


def cmd_final():
    recs = load_all()
    res = json.load(open(H('unblind-ja-2.json'), encoding='utf-8'))
    E = FC1.parse_judgments(H(JUDEN), '(?:31B|26B|Swallow)-en-t[1-4]-s[12]')
    en = {'%s-en-t%d-s%d' % (r['model_key'], r['task'], r['sample']): r for r in recs if r['lang'] == 'en'}
    assert set(E) == set(en), ('英語の判じの番号が合わない', sorted(set(en) - set(E)))
    for i, e in E.items():
        ok, nq = FC1.quotes_ok(e['quote'], en[i]['text'])
        assert ok and (e['flag'] == '無' or nq >= 1), ('英語の判じの引用', i)
    C = {(r['model_key'], r['lang'], r['task'], r['sample']): checks(r) for r in recs}
    T = {}
    for m in MODELS:
        js = [C[(m, l, 4, s)].get('json_last_line', '') for l in ('ja', 'en') for s in (1, 2)]
        T[m] = {'ja_flag': sum(1 for x in res.values() if x['model_key'] == m and x['flag'] == '有'),
                'en_flag': sum(1 for i, e in E.items() if i.startswith(m + '-') and e['flag'] == '有'),
                'json_ok': sum(1 for x in js if x.startswith('ok:')), 'json_all': js,
                'hangul_ja': sum(C[(m, 'ja', t, s)]['hangul'] for t in TASKS for s in (1, 2)),
                'simplified_ja': sum(C[(m, 'ja', t, s)]['simplified'] for t in TASKS for s in (1, 2)),
                'latin_ja': sum(C[(m, 'ja', t, s)]['latin_words'] for t in TASKS for s in (1, 2)),
                'numbered': [C[(m, l, 1, s)]['numbered_items'] for l in ('ja', 'en') for s in (1, 2)],
                'errors': sum(1 for r in recs if r['model_key'] == m and r['error']),
                'system_modes': sorted(set(r['system_mode'] for r in recs if r['model_key'] == m)),
                'thought_parts': sum(r['n_thought_parts'] for r in recs if r['model_key'] == m),
                'finish': sorted(set(str(r['finish_reason']) for r in recs if r['model_key'] == m))}
    hits = sum(1 for x in res.values() if x['hit'])
    n_ja = {m: sum(1 for x in res.values() if x['model_key'] == m) for m in MODELS}
    judge = lambda ok: '当たり' if ok else '外れ'
    row = lambda label, f: '| %s | %s |' % (label, ' | '.join(f(m) for m in MODELS))
    L = ['# B′ の機種選びのための日英の感触の確かめ・二巡目（まとめ・機械生成・`feel_check_Bprime_2.py final`）', '',
         '- 枠: `frame-model-feel-Bprime-2.md`（応答を生成する前に書いた・控え `frame-stamp.txt`）。課題と system は一巡目と同じ（SHA16 %s）。生の記録 `%s`（SHA16 %s）・`%s`（SHA16 %s）。日本語の盲検の一覧 `%s`（SHA16 %s）。日本語の判じ `%s`（SHA16 %s・対応を開く前の控え `%s`）。英語の判じ `%s`（SHA16 %s・盲検でない）。機種ごとの一覧 `%s`（SHA16 %s）。' % (
             TASKS_SHA, RAW_G2, s16(H(RAW_G2)), RAW_S, s16(H(RAW_S)), BLIND, s16(H(BLIND)), JUDJA, s16(H(JUDJA)), JUDJA_ST, JUDEN, s16(H(JUDEN)), VIEW, s16(H(VIEW))),
         '- 呼び方: temperature %.1f・出力の上限 %d・各題 × 各言語 × 各機種 %d 回。Gemma 4 は Gemini の API（top_p・top_k は配信の既定・思考は `thinkingLevel` minimal で止めた・逸脱 1）、Swallow は Colab で bf16 の生成（top_p 1.0・top_k なし）。場面と腕は使っていない。' % (TEMP, MAXTOK, N_SAMPLES),
         '- 判じは起草者（Claude 系）一名の目。日本語は三機種を混ぜた盲検（機種の推測の当たり %d／%d）、英語は盲検でない。これは感触の記録で、検定ではない。' % (hits, len(res)), '',
         '## 1. 機種ごとの数え', '',
         '| 何 | %s |' % ' | '.join(MODELS), '|---|' + '---|' * len(MODELS),
         row('日本語で明らかな誤りか不自然と判じた応答', lambda m: '%d／%d' % (T[m]['ja_flag'], n_ja[m])),
         row('英語で明らかな誤りと判じた応答', lambda m: '%d／8' % T[m]['en_flag']),
         row('課題 4 の最後の行の JSON が読めて答えが a・b・c', lambda m: '%d／4（%s）' % (T[m]['json_ok'], '・'.join(T[m]['json_all']))),
         row('課題 1 の番号つきの項目の数（日 1・日 2・英 1・英 2）', lambda m: '・'.join(str(x) for x in T[m]['numbered'])),
         row('日本語の応答の中のハングルの字', lambda m: str(T[m]['hangul_ja'])),
         row('日本語の応答の中の簡体字の目安（一覧を足した）', lambda m: str(T[m]['simplified_ja'])),
         row('日本語の応答の中のラテン文字の語（課題 4 の JSON の行を除く）', lambda m: str(T[m]['latin_ja'])),
         row('system の渡し方', lambda m: '・'.join(T[m]['system_modes'])),
         row('思考の部分（本文から外した数）', lambda m: str(T[m]['thought_parts'])),
         row('終わりの理由', lambda m: '・'.join(T[m]['finish'])),
         row('呼び出しの誤り', lambda m: str(T[m]['errors'])), '',
         '## 2. 枠の予想と照らす（外れても消さない）', '',
         '| 何 | 予想 | 結果 | 照らし |', '|---|---|---|---|',
         '| Swallow の日本語の誤りか不自然 | 1 以下（8 のうち） | %d | %s |' % (T['Swallow']['ja_flag'], judge(T['Swallow']['ja_flag'] <= 1)),
         '| gemma-4-31b の日本語の誤りか不自然 | 1 以下（8 のうち） | %d | %s |' % (T['31B']['ja_flag'], judge(T['31B']['ja_flag'] <= 1)),
         '| gemma-4-26b-a4b の日本語の誤りか不自然 | 2 以下（8 のうち） | %d | %s |' % (T['26B']['ja_flag'], judge(T['26B']['ja_flag'] <= 2)),
         '| 課題 4 の JSON | 三機種とも 3 以上（4 のうち） | %s | %s |' % ('・'.join(str(T[m]['json_ok']) for m in MODELS), judge(all(T[m]['json_ok'] >= 3 for m in MODELS))),
         '| 英語の明らかな誤り | 三機種とも 1 以下（8 のうち） | %s | %s |' % ('・'.join(str(T[m]['en_flag']) for m in MODELS), judge(all(T[m]['en_flag'] <= 1 for m in MODELS))),
         '| 機種の推測の当たり | 16 以下（24 のうち） | %d | %s |' % (hits, judge(hits <= 16)), '',
         '@@NOTES@@', '', FENCE, '']
    open(H(OUT), 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print(json.dumps(T, ensure_ascii=False), '| hits', hits, '| out', s16(H(OUT)))


if __name__ == '__main__':
    a = sys.argv[1:]
    {'run-gemma': lambda: cmd_run_gemma(), 'run-gemma-nothink': lambda: cmd_run_gemma(True), 'make-colab': lambda: cmd_make_colab(), 'ingest-swallow': lambda: cmd_ingest_swallow(a[1], a[2]),
     'blind': lambda: cmd_blind(), 'unblind': lambda: cmd_unblind(), 'final': lambda: cmd_final()}[a[0]]()
