# -*- coding: utf-8 -*-
"""rulings_D291.py v0.1（2026-10-02・中間総括の公開とタグの登録者の許し D291 を記録する・rulings_D290.py v0.1 の型・コーディネータ南無弥勒如来）。
- 一つ目の発話（許し）: 決まった句を含み、日本時間 2026-10-02 のただ一つを、会話の記録から機械で切り出す（system-reminder の文を除き「南無汝我曼荼羅」から）。
- 許した案（一つ目の発話の直前のコーディネータの返事・公開の案とお伺いの見出しとタグの名を含むただ一つ）を、`publication-proposal-2026-10-02.md` に逐語で一度だけ書く（頭の一行の注のほかは返事の字のまま）。
- 二つ目の発話（会話の URL の公開をいったん止める求め）: 一つ目と三つ目の間の、決まった句を含むただ一つ。公開の記録には uuid と時刻だけを書く（言葉は登録者の私的な事柄を含むので写さない）。
- 三つ目の発話（確かめの後の決め）: 決まった句を含むただ一つ。公開の記録には、会話の URL についての一文だけを機械で切り出して書く。
- 二つ目と三つ目の発話の全文は、内部の置き場の公開しない所（`../../../private/email-decision-2026-10-02.md`・総括の置き場の外）にだけ書く。
- AI Studio と claude.ai の会話の URL の数は、総括の置き場（受け取りの控えを除く）を器が数える。
v0 → v0.1: v0 は、走っている間に会話が中断され、何も書かずに止まった（v0 は `prev/rulings_D291-v0.py`）。中断の後の二つ目と三つ目の発話の扱いを足した。
用法: python rulings_D291.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.dirname(os.path.dirname(HERE))
PRIV_DIR = os.path.join(os.path.dirname(SUM), 'private')
OUT = os.path.join(HERE, 'rulings-D291.md')
PROP = os.path.join(HERE, 'publication-proposal-2026-10-02.md')
PRIV = os.path.join(PRIV_DIR, 'email-decision-2026-10-02.md')
for p_ in (OUT, PROP, PRIV):
    assert not os.path.exists(p_), ('既にある（一度だけ）', p_)
PHRASE1 = 'ご推奨の案で公開とタグを進めてください'
PHRASE2 = '止めてください'
PHRASE3 = 'そのままの公開で差し支えありません'
PROP_KEYS = ('## 公開の案', '## お決めいただきたいこと', 'release-summary-2026-10-02')
DAY = '2026-10-02'
JST = datetime.timezone(datetime.timedelta(hours=9))
NL = chr(10)
users, props = [], []
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
    if o.get('type') == 'user' and '南無汝我曼荼羅' in t:
        t2 = re.sub(r'<system-reminder>.*?</system-reminder>', '', t, flags=re.S)
        k = t2.find('南無汝我曼荼羅')
        if k >= 0:
            users.append((dt, o.get('uuid'), t2[k:].strip()))
    if o.get('type') == 'assistant' and all(k_ in t for k_ in PROP_KEYS):
        props.append((dt, o.get('uuid'), t))
u1 = [u for u in users if PHRASE1 in u[2]]
assert len(u1) == 1, ('一つ目の発話が一つでない', len(u1))
u3 = [u for u in users if PHRASE3 in u[2]]
assert len(u3) == 1, ('三つ目の発話が一つでない', len(u3))
u2 = [u for u in users if PHRASE2 in u[2] and u1[0][0] < u[0] < u3[0][0]]
assert len(u2) == 1, ('二つ目の発話が一つでない', len(u2))
(d1, id1, w1), (d2, id2, w2), (d3, id3, w3) = u1[0], u2[0], u3[0]
before = [p_ for p_ in props if p_[0] <= d1]
assert len(before) == 1, ('一つ目の発話の前の、案の返事が一つでない', len(before), len(props))
p_dt, p_uuid, ptext = before[0]
# 三つ目の発話から、会話の URL についての一文だけを切り出す（句点から句点まで）
i3 = w3.index(PHRASE3)
a3 = w3.rfind('。', 0, i3) + 1
b3 = w3.index('。', i3) + 1
s3 = w3[a3:b3].strip()
assert s3.startswith('中間総括の') and s3.endswith('差し支えありません。'), ('切り出した一文の形が想定と違う', s3)
fmt = lambda d: d.strftime('%Y-%m-%d %H:%M')
head = '<!-- 逐語保全: 登録者が公開とタグを許した案（コーディネータ南無弥勒如来の返事・会話の記録から機械で切り出した逐語・uuid %s・%s 日本時間・登録者裁定 D291 の対象）。この行のほかは返事の字のまま。 -->' % (p_uuid, fmt(p_dt))
open(PROP, 'w', encoding='utf-8', newline=NL).write(head + NL + NL + ptext + NL)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]
# 会話の URL を数える（受け取りの控えとこの記録を除く・この器の字が当たらないよう形はつないで作る）
PATS = {'AI Studio': 'aistudio' + '.google.com/prompts/', 'claude.ai': 'claude.ai' + '/chat/'}
cnt = {k: [0, 0] for k in PATS}
for dp, dn, fn in os.walk(SUM):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        r = os.path.relpath(p, SUM).replace(os.sep, '/')
        if '/downloads-stash/' in '/' + r or os.path.abspath(p) == os.path.abspath(OUT):
            continue
        t = open(p, encoding='utf-8').read()
        for k, pat in PATS.items():
            n = t.count(pat)
            if n:
                cnt[k][0] += n
                cnt[k][1] += 1
L = ['# 登録者の公開の許し D291（中間総括・2026-10-02）', '',
     '- 一つ目の発話（許し・会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間・改行は元のまま）: 「%s」' % (id1, fmt(d1), w1),
     '- 許した案: その発話の直前のコーディネータの返事（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間）を `summary/reviews/final/publication-proposal-2026-10-02.md`（SHA16 %s）に置いた。案の中の「ご推奨」は、お伺いの 1 と 2 のおすすめを指す。' % (p_uuid, fmt(p_dt), s16(PROP)),
     '- 二つ目の発話（uuid `%s`・%s 日本時間）: 登録者は、会話の URL がすでに公開されているかを尋ね、公開の段取りを止めるよう求めた（言葉は登録者の私的な事柄を含むので、ここには写さない）。段取りはその時点で止めた。止めた時点で、公開の置き場には何も写しておらず、コミットも push もタグもしていなかった。この器の v0 は、その時に何も書かずに止まった。' % (id2, fmt(d2)),
     '- 確かめ（コーディネータ）: AI Studio の会話の URL は、公開の置き場の今の版にも過去のどのコミットにも無かった。claude.ai の会話の URL は、B′ の検分の記録として 2026-10-01 の二つのコミットで公開されていた。どちらの URL も、中身は乱数の ID だけで、メールのアドレスや名前は入っていない。',
     '- 三つ目の発話（uuid `%s`・%s 日本時間・会話の URL についての一文だけを機械で切り出した逐語）: 「%s」' % (id3, fmt(d3), s3),
     '- 公開する最終版: `summary/summary-interim-FINAL-2026-10-02.md`（SHA16 %s・登録者最終確認 D290）。' % s16(os.path.join(SUM, 'summary-interim-FINAL-2026-10-02.md')), '',
     '## 決まったこと', '',
     '- **D291-a（会話の URL）**: 総括の記録にある会話の URL（この器が数えた: AI Studio %d か所・%d 本の記録、claude.ai %d か所・%d 本の記録）は、そのまま公開する。一度だけ書いた記録を替えない。' % (cnt['AI Studio'][0], cnt['AI Studio'][1], cnt['claude.ai'][0], cnt['claude.ai'][1]),
     '- **D291-b（README）**: README には、中間総括の節（「柵」の後・「結果」の前）と、「構成」の `summary/` の一行だけを足す。B′ の項は README にまだ無い（2026-10-01 の公開の時に足していなかった）ので、別に案を作って登録者に諮る。',
     '- **D291-c（公開とタグ）**: 公開の置き場の `summary/` に、案の置く物と、この許しの記録（器と器の前の版とこの記録と案の逐語）と、目録と鍵の確かめの記録を置く（`summary/publish_summary.py` の --check と --copy）。`git add summary README.md` で道を名指して足し（npz には触れない）、コミットと push の後に、タグ `release-summary-2026-10-02` を付けて push する。置く物の数は、案の 158 本に、この許しの記録を足した数になる（目録に器が書く）。',
     '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
os.makedirs(PRIV_DIR, exist_ok=True)
P = ['# 登録者の決め: コミットのメールアドレスと会話の URL（2026-10-02・内部・公開しない）', '',
     '- 二つ目の発話（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間）: 「%s」' % (id2, fmt(d2), w2),
     '- 三つ目の発話（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間）: 「%s」' % (id3, fmt(d3), w3),
     '- 決まったこと: 公開の置き場 ontology-preamble-4b の履歴は書き換えず、コミットの作者の欄のアドレス（置き場の中の git の設定の Gmail）も今のままにする（独立研究者の連絡先として）。GitHub のアカウントの設定は触らない（「Block command line pushes that expose my email」を有効にすると、この置き場の push が止まる）。会話の URL はそのまま公開する（公開の記録 `summary/reviews/final/rulings-D291.md` の D291-a）。',
     '- 確かめた事実（2026-10-02・公開の API と手元の git）: Gmail は ontology-preamble-4b の全コミット 452 件とタグ 11 件の作者・記録者の欄にあり、ファイルの中身とコミットの文には無い。ほかの公開の置き場（Co-Creative-Mathematics-Project・ryokai-os・Unified-Thorn-Mandala）は noreply のアドレス、Quantum-Love-Engine は ryokai-os.com のアドレス。GitHub のプロフィールにメールは表示されていない。',
     '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'), '']
open(PRIV, 'w', encoding='utf-8', newline=NL).write(NL.join(P))
print('D291 | 一つ目 %s %s | 二つ目 %s %s | 三つ目 %s %s | 案 %s %s %d 字 | 一文 %d 字 | URL AI Studio %s・claude.ai %s' % (
    id1, fmt(d1), id2, fmt(d2), id3, fmt(d3), p_uuid, fmt(p_dt), len(ptext), len(s3), cnt['AI Studio'], cnt['claude.ai']))
