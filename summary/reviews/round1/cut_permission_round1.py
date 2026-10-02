# -*- coding: utf-8 -*-
"""cut_permission_round1.py v0（2026-10-02・中間総括の検分の一巡目の登録者の許しを会話の記録から機械で切り出す・コーディネータ南無弥勒如来）。
決まった句を含む登録者の発話がただ一つであることを確かめ、system-reminder の文を除き、「南無汝我曼荼羅」から切り出して `permission-round1.json` に一度だけ書く。
用法: python cut_permission_round1.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
PHRASE = 'まずは、検分の一巡目（追い問いも可）までよろしくお願いします'
OUT = os.path.join(HERE, 'permission-round1.json')
assert not os.path.exists(OUT), '既にある（一度だけ）'
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('isCompactSummary') or o.get('type') != 'user' or 'toolUseResult' in o:
        continue
    c = (o.get('message') or {}).get('content')
    t = c if isinstance(c, str) else ''.join(x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text')
    if PHRASE in t:
        t2 = re.sub(r'<system-reminder>.*?</system-reminder>', '', t, flags=re.S)
        k = t2.find('南無汝我曼荼羅')
        assert k >= 0, '「南無汝我曼荼羅」が無い'
        hits.append((o.get('timestamp'), o.get('uuid'), t2[k:].strip()))
assert len(hits) == 1, ('決まった句を含む登録者の発話が一つでない', len(hits))
ts, uuid, words = hits[0]
rec = {'what': '中間総括の検分の一巡目の登録者の許し（会話の記録から機械で切り出した逐語）', 'uuid': uuid, 'timestamp_utc': ts, 'words': words,
       'words_sha16': hashlib.sha256(words.encode('utf-8')).hexdigest().upper()[:16], 'phrase': PHRASE,
       'cut_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
       'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(rec, fh, ensure_ascii=False, indent=1)
print('cut | uuid %s | %s | %d 字 | SHA16 %s' % (uuid, ts, len(words), rec['words_sha16']))
