# -*- coding: utf-8 -*-
"""check_nscale_model.py v0（2026-10-02・段階 C の下見の枠 §4: 走らせる前に、Nscale がこの機種名を提供していることを、生成を伴わない一覧の問い合わせで確かめる・コーディネータ南無弥勒如来）。
鍵は走行器と同じ所（環境変数 NSCALE_API_KEY か OP4B_ENV_FILE の .env.local）から読み、表示も記録もしない。結果を `nscale-model-check-pilotC.json` に一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'nscale-model-check-pilotC.json')
assert not os.path.exists(OUT), '一度だけ'
ENV_FILE = os.environ.get('OP4B_ENV_FILE', r'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
TARGET = 'Qwen/Qwen3-4B-Instruct-2507'
URL = 'https://inference.api.nscale.com/v1/models'


def load_key(name):
    k = os.environ.get(name)
    if k:
        return k.strip()
    for line in open(ENV_FILE, encoding='utf-8'):
        line = line.strip()
        if line.startswith(name + '='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise SystemExit('鍵が見つからない（値は表示しない）')


req = urllib.request.Request(URL, headers={'Authorization': 'Bearer ' + load_key('NSCALE_API_KEY'), 'User-Agent': 'op4b-pilotC-check'})
with urllib.request.urlopen(req, timeout=60) as r:
    status = r.status
    data = json.load(r)
ids = [m.get('id') for m in data.get('data', [])]
hit = [m for m in data.get('data', []) if m.get('id') == TARGET]
rec = {'kind': 'nscale_model_check', 'tool': 'check_nscale_model.py v0', 'time_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
       'endpoint': URL, 'http_status': status, 'n_models_listed': len(ids), 'target': TARGET, 'target_listed': bool(hit),
       'target_entry': {k: hit[0].get(k) for k in ('id', 'object', 'created', 'owned_by') if k in hit[0]} if hit else None,
       'note': '生成は伴わない。鍵の値は表示も記録もしない。機種名の一致は、重みが最初の登録の時と同じことを示さない。',
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(rec, open(OUT, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('HTTP %d | 一覧の機種 %d | %s: %s' % (status, len(ids), TARGET, '一覧にある' if hit else '一覧に無い'))
