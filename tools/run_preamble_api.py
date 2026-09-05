# -*- coding: utf-8 -*-
"""run_eprime_deepseek.py —— 追補E′ の【登録外・試験走行】を DeepSeek API（deepseek-v4-flash）でローカル実施する。

性格: 凍結設計（Qwen3-30B 単一モデル）の対象外。別モデルでの器材・素材の実地検査と基底の感触取りであり、
      いかなる主張の根拠にもならない。公開・凍結の対象ではない。Qwen 側のデータと混ぜない。

借用: 凍結器材 pipeline/boot_eprime.py（EP_MODE='import'）から、素材の凍結 SHA 照合・割付（pilot seed 2267559785 /
      main seed 273635904）・N2 シナリオ・JSON 指示・パーサ app_parser_rev2・破局定義・周期ループ検出器・連結式を
      そのまま使う。差し替えるのは生成部（HF transformers → DeepSeek chat/completions）のみ。
      生成パラメタは凍結値を継承: temperature 0.7 / top_p 0.9 / max_tokens 4096。リトライ規則: JSON 解析不能なら一度だけ再生成。

鍵: 環境変数 DEEPSEEK_API_KEY、無ければ Ryokai-OS/.env.local から読む（値は一切印字しない）。

使い方:  python run_eprime_deepseek.py smoke|pilot|main [--workers 4] [--tag eprime-ds-pilot1]
"""
import os, sys, json, time, uuid, datetime, hashlib, argparse, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_VERIF = os.environ.get('EP_ROOT_LOCAL',
    r'C:/Users/PC/AppData/Local/Temp/claude/C--Users-PC/40603118-d22a-466f-a4f6-53fee5112305/scratchpad/ryokai-os/verification')
TEMPERATURE, TOP_P = 0.7, 0.9
PROVIDERS = {
    # OpenAI 互換 chat/completions。モデル ID は各社 docs で確認した正式文字列（確認日 2026-09-04）。
    'deepseek': dict(url='https://api.deepseek.com/chat/completions', key='DEEPSEEK_API_KEY',
                     model='deepseek-v4-flash', tag='ds', thinking_param=True),
    'xai':      dict(url='https://api.x.ai/v1/chat/completions', key='XAI_API_KEY',
                     model='grok-4.20-0309-non-reasoning', tag='grok', thinking_param=False),
    # Google Gemini の OpenAI 互換エンドポイント（system メッセージ対応）
    'gemini':   dict(url='https://generativelanguage.googleapis.com/v1beta/openai/chat/completions', key='GEMINI_API_KEY',
                     model='gemini-2.5-flash-lite', tag='gem', thinking_param=False),
    # Nscale serverless（OpenAI 互換・基底 URL とモデル ID は登録者がコンソールで確認し --base-url/--model で指定・要確認）
    'nscale':   dict(url='https://inference.api.nscale.com/v1/chat/completions', key='NSCALE_API_KEY',
                     model='Qwen/Qwen3-4B-Instruct-2507', tag='q4b', thinking_param=False),
}

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['smoke', 'pilot', 'main'])
ap.add_argument('--provider', choices=list(PROVIDERS), default='deepseek')
ap.add_argument('--model', default=None, help='モデル ID の上書き（既定はプロバイダ既定）')
ap.add_argument('--base-url', default=None, help='chat/completions の完全 URL の上書き（汎用 OpenAI 互換プロバイダ用）')
ap.add_argument('--workers', type=int, default=4)
ap.add_argument('--tag', default=None)
ap.add_argument('--thinking', choices=['enabled', 'disabled'], default='disabled',
                help='DeepSeek 思考モード。既定 disabled＝Qwen3-30B-Instruct（隠れ推論なし）との同等性。xAI では送らない')
ap.add_argument('--max-tokens', type=int, default=4096)
ap.add_argument('--system', choices=['a2', 'none'], default='a2',
                help='土台。a2=凍結の A2-on-full（3.0系・降板条項あり）。none=素の場（system なし・登録外の基底下見用）')
ap.add_argument('--arms', default=None, help='腕の限定（カンマ区切り・例 N,O,BP）。main の配置から当該腕のみ実行')
ap.add_argument('--n-per-arm', type=int, default=None,
                help='下見用: main の腕あたり試行数を拡張（同一 seed で 50 ブロック以降も同じ乱数列を続ける・凍結配置の先頭 50 は一致）')
ap.add_argument('--custom-arms', default=None,
                help='登録外の追加腕: 名前=前置きファイル をカンマ区切り（例 Om=arms-h1/preamble-Om.md,Osec=...）。--arms に含めて実行')
ap.add_argument('--gem-thinking', choices=['default', 'effort-none', 'budget-0'], default='default',
                help='Google 互換 EP の思考制御。effort-none=reasoning_effort:"none"／budget-0=extra_body.google.thinking_config.thinking_budget=0')
args = ap.parse_args()
PROV = PROVIDERS[args.provider]
MODEL = args.model or PROV['model']
API_URL = args.base_url or PROV['url']
KEY_NAME = PROV['key']
THINKING = args.thinking if PROV['thinking_param'] else 'n/a'
MODE = args.mode
RUN_TAG = args.tag or ('eprime-%s-%s%s' % (PROV['tag'], MODE, '-nosys' if args.system == 'none' else ''))
MAX_TOKENS = args.max_tokens
OUT_DIR = os.path.join(HERE, 'results')
os.makedirs(OUT_DIR, exist_ok=True)
MODEL_FN = MODEL.replace('/', '_')   # ファイル名用（モデル ID の '/' を無害化）
OUT_T = os.path.join(OUT_DIR, 'trials-%s-%s.jsonl' % (RUN_TAG, MODEL_FN))
OUT_R = os.path.join(OUT_DIR, 'raw-%s-%s.jsonl' % (RUN_TAG, MODEL_FN))

# ---- 凍結器材を import モードで取り込む（照合・配置・パーサ・連結式を借用）----
g = {'EP_MODE': 'import', 'EP_ROOT': REPO_VERIF, 'EP_OUT': OUT_DIR, 'EP_RUN_TAG': RUN_TAG, '__name__': 'boot_eprime'}
exec(open(os.path.join(REPO_VERIF, 'pipeline', 'boot_eprime.py'), encoding='utf-8').read(), g)
_needed, verify_frozen, build_schedule = g['_needed'], g['verify_frozen'], g['build_schedule']
load_scenario, load_parser, user_message = g['load_scenario'], g['load_parser'], g['user_message']
catastrophe, loop_info, selftests, _read, _sha16 = g['catastrophe'], g['loop_info'], g['selftests'], g['_read'], g['_sha16']
PATH, FROZEN_SHA16, PREAMBLE_OF, CLAUSE = g['PATH'], g['FROZEN_SHA16'], g['PREAMBLE_OF'], g['CLAUSE']
PILOT_SEED, MAIN_SEED = g['PILOT_SEED'], g['MAIN_SEED']

# ---- 鍵（値は印字しない）----
def load_key():
    k = os.environ.get(KEY_NAME)
    if k: return k.strip()
    envp = r'C:/Users/PC/Desktop/Ryokai-OS/.env.local'
    if os.path.isfile(envp):
        for line in open(envp, encoding='utf-8'):
            line = line.strip()
            if line.startswith(KEY_NAME + '=') and len(line) > len(KEY_NAME) + 1:
                return line.split('=', 1)[1].strip().strip('"').strip("'")
    sys.exit('%s が見つかりません（環境変数か Ryokai-OS/.env.local）。' % KEY_NAME)
KEY = load_key()

# ---- 素材照合・自己検査（凍結器材のものをそのまま）----
keys, arms = _needed(MODE)
verify_frozen(keys)
print('[ds/check] 凍結素材 SHA 照合 PASS（%d 点）' % len(keys))
scen_text, inst, fam = load_scenario(); parse = load_parser()
BASE = _read(PATH['base'])
texts = {k: _read(PATH[k]) for k in keys if k not in ('base', 'scen', 'parser')}
sf = selftests(parse, scen_text, inst, texts); assert not sf, '自己検査 FAIL: %s' % sf
SCHEDULE = build_schedule(MODE)
if MODE == 'main' and args.n_per_arm and args.n_per_arm != 50:
    import random as _random
    _rng = _random.Random(MAIN_SEED); SCHEDULE = []
    _ARMS = ['BP', 'BP-sec', 'BP-scr', 'BP-sec-scr', 'N', 'Onull', 'O']
    for _ in range(args.n_per_arm):
        _blk = list(_ARMS); _rng.shuffle(_blk); SCHEDULE.extend(_blk)
    assert SCHEDULE[:350] == build_schedule('main'), '拡張配置の先頭 350 が凍結配置と不一致'
    print('[ds] 配置拡張: %d ブロック × 7 腕 = %d（先頭 350 は凍結配置と一致）' % (args.n_per_arm, len(SCHEDULE)))
CUSTOM = {}
if args.custom_arms:
    for kv in args.custom_arms.split(','):
        name, path = kv.split('=', 1); CUSTOM[name] = os.path.join(HERE, path) if not os.path.isabs(path) else path
        texts[name] = _read(CUSTOM[name]); PREAMBLE_OF[name] = name
        FROZEN_SHA16[name] = _sha16(texts[name])   # 登録外腕: 起動時に計算した SHA を記帳
    if MODE == 'main' and args.arms:
        import random as _random
        _sel = args.arms.split(','); _rng = _random.Random(MAIN_SEED); SCHEDULE = []
        for _ in range(args.n_per_arm or 50):
            _blk = list(_sel); _rng.shuffle(_blk); SCHEDULE.extend(_blk)
        print('[ds] 自由腕配置: %s × %d ブロック = %d（登録外・seed %d）' % (_sel, args.n_per_arm or 50, len(SCHEDULE), MAIN_SEED))
    if MODE == 'smoke':
        SCHEDULE = list(CUSTOM.keys())
nblk = 3 if MODE in ('pilot', 'smoke') else (len(args.arms.split(',')) if (CUSTOM and args.arms) else 7)
seed_used = PILOT_SEED if MODE == 'pilot' else (MAIN_SEED if MODE == 'main' else None)
PROC_UUID = str(uuid.uuid4())
print('[ds] mode=%s trials=%d model=%s out=%s' % (MODE, len(SCHEDULE), MODEL, OUT_DIR))

# ---- 生成（DeepSeek）----
def generate(msgs):
    payload = {'model': MODEL, 'messages': msgs, 'temperature': TEMPERATURE, 'top_p': TOP_P,
               'max_tokens': MAX_TOKENS, 'stream': False}
    if PROV['thinking_param']:
        payload['thinking'] = {'type': THINKING}
    if args.provider == 'gemini' and args.gem_thinking == 'effort-none':
        payload['reasoning_effort'] = 'none'
    elif args.provider == 'gemini' and args.gem_thinking == 'budget-0':
        payload['extra_body'] = {'google': {'thinking_config': {'thinking_budget': 0, 'include_thoughts': False}}}
    body = json.dumps(payload).encode('utf-8')
    for attempt in range(6):
        try:
            req = urllib.request.Request(API_URL, data=body, method='POST', headers={
                'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY})
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read().decode('utf-8'))
            ch = data['choices'][0]; msg = ch['message']
            txt = msg.get('content') or ''
            reasoning = msg.get('reasoning_content') or ''
            # Gemma 4 は思考を本文内 <thought>…</thought> として返す（API から無効化不可・2026-09-04 確認）。
            # 解析・ループ検出は本文のみで行い、思考部は reasoning 欄へ退避して長さを記録する。
            import re as _re
            thoughts = _re.findall(r'<thought>(.*?)</thought>', txt, flags=_re.S)
            if thoughts:
                reasoning = (reasoning + '\n'.join(thoughts)).strip()
                txt = _re.sub(r'<thought>.*?</thought>', '', txt, flags=_re.S).strip()
            elif '<thought>' in txt:      # 閉じタグ無し＝思考中に切り詰め
                reasoning = (reasoning + txt.split('<thought>', 1)[1]).strip(); txt = txt.split('<thought>', 1)[0].strip()
            u = data.get('usage', {}) or {}
            li = loop_info(txt)
            return dict(text=txt, gen=int(u.get('completion_tokens', 0)), ptok=int(u.get('prompt_tokens', 0)),
                        finish=ch.get('finish_reason'), trunc=(ch.get('finish_reason') == 'length'),
                        reasoning_len=len(reasoning),
                        reasoning=reasoning,
                        api_model=data.get('model'), api_id=data.get('id'),
                        tsha=_sha16(txt), loop=li['fired'], loop_period=li['period'], loop_index=li['index'], nsent=li['nsent'])
        except urllib.error.HTTPError as e:
            err = e.read().decode('utf-8', 'replace')[:300]
            if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                time.sleep(3 * (attempt + 1)); continue
            raise RuntimeError('%s HTTP %s: %s' % (args.provider, e.code, err))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt < 5: time.sleep(3 * (attempt + 1)); continue
            raise

lock = threading.Lock()
have_t = set()
if os.path.exists(OUT_T):
    for l in open(OUT_T, encoding='utf-8'):
        if l.strip(): have_t.add(json.loads(l)['trial_id'])
    print('[ds/resume] 既存 %d 行' % len(have_t))

idx_in_arm = {}; jobs = []
for i, arm in enumerate(SCHEDULE):
    idx_in_arm[arm] = idx_in_arm.get(arm, 0) + 1
    tid = '%s-%03d-%s-%02d' % (RUN_TAG, i, arm, idx_in_arm[arm])
    if tid in have_t: continue
    if args.arms and arm not in args.arms.split(','): continue
    jobs.append((i, arm, idx_in_arm[arm], tid))
if MODE == 'smoke': jobs = jobs[:3]
print('[ds] 残り %d 試行' % len(jobs))

def one(job):
    i, arm, ai, tid = job
    um = {'role': 'user', 'content': user_message(arm, texts, scen_text, inst)}
    msgs = [{'role': 'system', 'content': BASE}, um] if args.system == 'a2' else [um]
    ts0 = datetime.datetime.utcnow().isoformat() + 'Z'; t1 = time.time()
    g1 = generate(msgs); parsed = parse(g1['text'], fam); retry = False; gsel = g1
    raw = g1['text']; raw_first = g1['text']; raw_retry = None
    if parsed is None:
        retry = True; g2 = generate(msgs); p2 = parse(g2['text'], fam)
        raw = raw + '\n===RETRY===\n' + g2['text']; raw_retry = g2['text']
        if p2 is not None: parsed, gsel = p2, g2
    sec = round(time.time() - t1, 1)
    row = {
        'arm': arm, 'family': fam, 'question_id': 'N2', 'run_tag': RUN_TAG, 'mode': MODE,
        'registration': 'OUT-OF-REGISTRATION test run (non-frozen model; not evidence for any claim)',
        'trial_id': tid, 'trial_index': i, 'arm_index': ai,
        'superblock': (None if MODE == 'smoke' else i // nblk), 'schedule_seed': seed_used,
        'choice': (parsed or {}).get('choice'), 'escalation': (parsed or {}).get('escalation'),
        'catastrophe': catastrophe(parsed), 'nonintegrity': (parsed or {}).get('_nonintegrity'),
        'format_retry_used': retry, 'format_fail': parsed is None,
        'truncated': gsel['trunc'], 'finish_reason': gsel['finish'],
        'loop_flag': gsel['loop'], 'loop_period': gsel['loop_period'], 'loop_index': gsel['loop_index'], 'nsent': gsel['nsent'],
        'first_gen_tokens': g1['gen'], 'first_truncated': g1['trunc'], 'first_loop': g1['loop'],
        'gen_tokens': gsel['gen'], 'prompt_tokens': gsel['ptok'], 'reasoning_content_chars': gsel['reasoning_len'],
        'seconds': sec, 'tokens_sha': gsel['tsha'],
        'preamble_sha': (FROZEN_SHA16[PREAMBLE_OF[arm]] if PREAMBLE_OF[arm] else None),
        'system': args.system, 'system_sha': (_sha16(BASE) if args.system == 'a2' else None),
        'scenario_sha': FROZEN_SHA16['scen'], 'parser_sha': FROZEN_SHA16['parser'],
        'max_tokens': MAX_TOKENS, 'thinking': THINKING, 'gem_thinking': args.gem_thinking, 'provider': args.provider, 'model': MODEL, 'api_model': gsel['api_model'], 'api_id': gsel['api_id'],
        'sampling': {'temperature': TEMPERATURE, 'top_p': TOP_P},
        'timestamp': ts0, 'timestamp_end': datetime.datetime.utcnow().isoformat() + 'Z',
        'pid': os.getpid(), 'proc_uuid': PROC_UUID,
    }
    with lock:
        with open(OUT_T, 'a', encoding='utf-8') as f: f.write(json.dumps(row, ensure_ascii=False) + '\n')
        with open(OUT_R, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'trial_id': tid, 'arm': arm, 'trial_index': i, 'raw_output': raw, 'raw_output_first': raw_first,
                                'raw_output_retry': raw_retry, 'tokens_sha': gsel['tsha'], 'format_retry_used': retry,
                                'reasoning_content_first': g1['reasoning'], 'reasoning_content_selected': gsel['reasoning'],
                                'thinking': THINKING,
                                'clause': CLAUSE, 'registration': row['registration']}, ensure_ascii=False) + '\n')
        print('[ds] %s choice=%s esc=%s cat=%s gen=%d retry=%s loop=%s fin=%s sec=%.0f' %
              (tid, row['choice'], row['escalation'], row['catastrophe'], gsel['gen'], retry, gsel['loop'], gsel['finish'], sec), flush=True)
    return tid

t_all = time.time()
with ThreadPoolExecutor(max_workers=args.workers) as ex:
    futs = [ex.submit(one, j) for j in jobs]
    for f in as_completed(futs):
        f.result()

# ---- 整合検査（凍結器材の integrity は OUT パスがモデル名固定のため自前で同等検査）----
rows = [json.loads(l) for l in open(OUT_T, encoding='utf-8') if l.strip()]
rids = {json.loads(l)['trial_id'] for l in open(OUT_R, encoding='utf-8') if l.strip()}
ids = [r['trial_id'] for r in rows]
print('[ds/integrity] trials=%d raw=%d dup=%d raw_mismatch=%d' % (len(rows), len(rids), len(ids) - len(set(ids)), len(set(ids) ^ rids)))
by = {}
for r in rows:
    a = by.setdefault(r['arm'], {'n': 0, 'cat': 0, 'fail': 0, 'retry': 0, 'trunc': 0, 'loop': 0, 'nonint': 0})
    a['n'] += 1; a['cat'] += int(bool(r['catastrophe'])); a['fail'] += int(bool(r['format_fail']))
    a['retry'] += int(bool(r['format_retry_used'])); a['trunc'] += int(bool(r['truncated'])); a['loop'] += int(bool(r['loop_flag']))
    a['nonint'] += int(r['nonintegrity'] is not None)
print('[ds/summary] 登録外・記述のみ（p 値なし）:')
for a in ['BP', 'BP-sec', 'BP-scr', 'BP-sec-scr', 'N', 'Onull', 'O']:
    if a in by:
        s = by[a]; print('  %-10s n=%2d 破局=%2d (%.0f%%) fail=%d retry=%d trunc=%d loop=%d nonint=%d' %
                         (a, s['n'], s['cat'], 100.0 * s['cat'] / s['n'], s['fail'], s['retry'], s['trunc'], s['loop'], s['nonint']))
print('[ds] 経過 %.0fs。%s' % (time.time() - t_all, CLAUSE))
