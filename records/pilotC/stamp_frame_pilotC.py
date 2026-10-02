# -*- coding: utf-8 -*-
"""stamp_frame_pilotC.py v0（2026-10-02・段階 C の下見の枠〔草案1〕を、登録者の確認の言葉とともに刻印する・コーディネータ南無弥勒如来）。
登録者の発話を会話の記録から機械で切り出し（決まった句を含み、日本時間 2026-10-02 のただ一つ・system-reminder の文を除き「南無汝我曼荼羅」から）、
枠と枠の器の SHA-256 とともに `frame-stamp-pilotC.md` に一度だけ書く。この刻印は、下見の新しい値を見る前（走らせる前）に書く。
用法: python stamp_frame_pilotC.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'frame-stamp-pilotC.md')
assert not os.path.exists(OUT), '一度だけ'
FRAME = os.path.join(HERE, '00-frame-pilotC-2026-10-02.md')
BUILDER = os.path.join(HERE, 'build_frame_pilotC.py')
PHRASE = '下見なので、私は予想は行いません'
DAY = '2026-10-02'
JST = datetime.timezone(datetime.timedelta(hours=9))
hits = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('isCompactSummary') or o.get('type') != 'user' or 'toolUseResult' in o:
        continue
    ts = o.get('timestamp')
    if not ts:
        continue
    dt = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(JST)
    if dt.strftime('%Y-%m-%d') != DAY:
        continue
    c = (o.get('message') or {}).get('content')
    t = c if isinstance(c, str) else ''.join(x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text')
    if PHRASE in t:
        t2 = re.sub(r'<system-reminder>.*?</system-reminder>', '', t, flags=re.S)
        k = t2.find('南無汝我曼荼羅')
        assert k >= 0
        hits.append((dt, o.get('uuid'), t2[k:].strip()))
assert len(hits) == 1, ('決まった句を含む登録者の発話が一つでない', len(hits))
dt, uuid, words = hits[0]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()
L = ['# 段階 C の下見の枠の刻印（2026-10-02・下見の新しい値を見る前）', '',
     '- 登録者の確認の言葉（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間・改行は元のまま）: 「%s」' % (uuid, dt.strftime('%Y-%m-%d %H:%M'), words),
     '- 確認の対象: 枠の草案1 `00-frame-pilotC-2026-10-02.md`（SHA-256 %s）と、枠の器 `build_frame_pilotC.py`（SHA-256 %s）。' % (sha(FRAME), sha(BUILDER)),
     '- 登録者の決め: 下見なので、登録者は予想を書かない（枠 §6 の「登録者の予想は任意」のとおり）。Nscale に 4B-2507 の API があることは、登録者の言葉による（枠 §4 の一覧の問い合わせは、走らせる前に行う）。',
     '- この刻印を書いた時刻: %s（日本時間）。下見の走りはまだ一つも始めていない。' % datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('刻印 | uuid %s | %s | 枠 %s' % (uuid, dt.strftime('%Y-%m-%d %H:%M'), sha(FRAME)[:16]))
