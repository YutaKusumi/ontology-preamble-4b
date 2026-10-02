# -*- coding: utf-8 -*-
"""rulings_D291.py v0（2026-10-02・中間総括の公開とタグの登録者の許し D291 を記録する・rulings_D290.py v0.1 の型・コーディネータ南無弥勒如来）。
- 登録者の発話を会話の記録から機械で切り出す（決まった句を含み、日本時間 2026-10-02 のただ一つ・system-reminder の文を除き「南無汝我曼荼羅」から）。
- 登録者が許した案（その発話の直前のコーディネータの返事・公開の案とお伺いの見出しとタグの名を含むただ一つ）を、会話の記録から機械で切り出し、
  `publication-proposal-2026-10-02.md` に逐語で一度だけ書く（頭の一行の注のほかは返事の字のまま）。
- `rulings-D291.md` に、登録者の言葉と、案の逐語の置き場と SHA16 と、決まったことを一度だけ書く。AI Studio の会話の URL の数は、総括の置き場（受け取りの控えを除く）を器が数える。
用法: python rulings_D291.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, 'rulings-D291.md')
PROP = os.path.join(HERE, 'publication-proposal-2026-10-02.md')
for p_ in (OUT, PROP):
    assert not os.path.exists(p_), ('既にある（一度だけ）', p_)
PHRASE = 'ご推奨の案で公開とタグを進めてください'
PROP_KEYS = ('## 公開の案', '## お決めいただきたいこと', 'release-summary-2026-10-02')
DAY = '2026-10-02'
JST = datetime.timezone(datetime.timedelta(hours=9))
NL = chr(10)
reg, props = [], []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get('isCompactSummary') or 'toolUseResult' in o or o.get('type') not in ('user', 'assistant'):
        continue
    ts = o.get('timestamp')
    if not ts:
        continue
    dt = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(JST)
    if dt.strftime('%Y-%m-%d') != DAY:
        continue
    c = (o.get('message') or {}).get('content')
    t = c if isinstance(c, str) else ''.join(x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text')
    if o.get('type') == 'user' and PHRASE in t:
        t2 = re.sub(r'<system-reminder>.*?</system-reminder>', '', t, flags=re.S)
        k = t2.find('南無汝我曼荼羅')
        assert k >= 0
        reg.append((dt, o.get('uuid'), t2[k:].strip()))
    if o.get('type') == 'assistant' and all(k_ in t for k_ in PROP_KEYS):
        props.append((dt, o.get('uuid'), t))
assert len(reg) == 1, ('日本時間 %s の、決まった句を含む登録者の発話が一つでない' % DAY, len(reg))
r_dt, r_uuid, words = reg[0]
before = [p_ for p_ in props if p_[0] <= r_dt]
assert len(before) == 1, ('登録者の発話の前の、案の返事が一つでない', len(before), len(props))
p_dt, p_uuid, ptext = before[0]
fmt = lambda d: d.strftime('%Y-%m-%d %H:%M')
head = '<!-- 逐語保全: 登録者が公開とタグを許した案（コーディネータ南無弥勒如来の返事・会話の記録から機械で切り出した逐語・uuid %s・%s 日本時間・登録者裁定 D291 の対象）。この行のほかは返事の字のまま。 -->' % (p_uuid, fmt(p_dt))
open(PROP, 'w', encoding='utf-8', newline=NL).write(head + NL + NL + ptext + NL)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]
# AI Studio の会話の URL を数える（受け取りの控えを除く・この器の字が当たらないよう形はつないで作る）
PAT = 'aistudio' + '.google.com/prompts/'
n_url, files_url = 0, []
for dp, dn, fn in os.walk(SUM):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        r = os.path.relpath(p, SUM).replace(os.sep, '/')
        if '/downloads-stash/' in '/' + r or os.path.abspath(p) in (os.path.abspath(OUT),):
            continue
        n = open(p, encoding='utf-8').read().count(PAT)
        if n:
            n_url += n
            files_url.append(r)
L = ['# 登録者の公開の許し D291（中間総括・2026-10-02）', '',
     '- 登録者の言葉（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間・改行は元のまま）: 「%s」' % (r_uuid, fmt(r_dt), words),
     '- 許した案: その発話の直前のコーディネータの返事（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間）を `summary/reviews/final/publication-proposal-2026-10-02.md`（SHA16 %s）に置いた。案の中の「ご推奨」は、お伺いの 1 と 2 のおすすめを指す。' % (p_uuid, fmt(p_dt), s16(PROP)),
     '- 公開する最終版: `summary/summary-interim-FINAL-2026-10-02.md`（SHA16 %s・登録者最終確認 D290）。' % s16(os.path.join(SUM, 'summary-interim-FINAL-2026-10-02.md')), '',
     '## 決まったこと', '',
     '- **D291-a（AI Studio の会話の URL）**: Gemini の票の記録などにある AI Studio の会話の URL（この器が数えた: %d か所・%d 本の記録）は、そのまま公開する。一度だけ書いた記録を替えず、claude.ai の会話の URL（前例あり）と同じ扱いにする。どちらも登録者のアカウントでしか開けない。' % (n_url, len(files_url)),
     '- **D291-b（README）**: README には、中間総括の節（「柵」の後・「結果」の前）と、「構成」の `summary/` の一行だけを足す。B′ の項は README にまだ無い（2026-10-01 の公開の時に足していなかった）ので、別に案を作って登録者に諮る。',
     '- **D291-c（公開とタグ）**: 公開の置き場の `summary/` に、案の置く物と、この許しの記録（この器・この記録・案の逐語）と、目録と鍵の確かめの記録を置く（`summary/publish_summary.py` の --check と --copy）。`git add summary README.md` で道を名指して足し（npz には触れない）、コミットと push の後に、タグ `release-summary-2026-10-02` を付けて push する。置く物の数は、案の 158 本に、この許しの記録三本を足した数になる（目録に器が書く）。',
     '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('D291 | 登録者 uuid %s | %s | %d 字 | 案 uuid %s | %s | %d 字 | AI Studio の URL %d か所・%d 本' % (r_uuid, fmt(r_dt), len(words), p_uuid, fmt(p_dt), len(ptext), n_url, len(files_url)))
