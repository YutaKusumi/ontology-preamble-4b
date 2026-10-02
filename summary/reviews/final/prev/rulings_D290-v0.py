# -*- coding: utf-8 -*-
"""rulings_D290.py v0（2026-10-02・中間総括の登録者最終確認 D290 を記録する・D289 の器の型・コーディネータ南無弥勒如来）。
登録者の発話を会話の記録から機械で切り出し（決まった句を含むただ一つ・system-reminder の文を除き「南無汝我曼荼羅」から）、`rulings-D290.md` に一度だけ書く。
最終確認の対象は草案5（`summary/summary-interim-draft5-2026-10-02.md`）と二つの差分の資料と起草者の見直しの記録。
用法: python rulings_D290.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import io, os, re, sys, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
HERE = os.path.dirname(os.path.abspath(__file__))
SUM = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, 'rulings-D290.md')
assert not os.path.exists(OUT), '既にある（一度だけ）'
PHRASE = '私たちでできるベストを尽くしたと判断します'
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
        assert k >= 0
        hits.append((o.get('timestamp'), o.get('uuid'), t2[k:].strip()))
assert len(hits) == 1, ('決まった句を含む登録者の発話が一つでない', len(hits))
ts, uuid, words = hits[0]
jst = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')
s16 = lambda p: hashlib.sha256(open(os.path.join(SUM, p), 'rb').read()).hexdigest().upper()[:16]
L = ['# 登録者最終確認 D290（中間総括・2026-10-02・内部）', '',
     '- 登録者の言葉（会話の記録から機械で切り出した逐語・uuid `%s`・%s 日本時間・改行は元のまま）: 「%s」' % (uuid, jst, words),
     '- 確認の対象: 草案5（`summary/summary-interim-draft5-2026-10-02.md`・SHA16 %s）・差分の資料（`summary/diff-draft3-to-draft4-2026-10-02.md`・SHA16 %s と `summary/diff-draft4-to-draft5-2026-10-02.md`・SHA16 %s）・起草者の見直しの記録（`summary/review-draft4/01-review-draft4.md`・SHA16 %s）。' % (
         s16('summary-interim-draft5-2026-10-02.md'), s16('diff-draft3-to-draft4-2026-10-02.md'), s16('diff-draft4-to-draft5-2026-10-02.md'), s16('review-draft4/01-review-draft4.md')), '',
     '## 決まったこと', '',
     '- **D290（最終確認）**: 草案5 を最終の内容とする（登録者の言葉）。最終版は、草案5 の本文に、公開の時の直し（頭の題と状態の行・公開の頭の断り・検分票の判定と状態）だけを入れて器で組む（最終の巡の採否の表の Q30・裁定 D288-j）。',
     '- 公開の段取り: 最終版と、枠・追記・計算の器と出力・草案と器・差分の資料・検分の記録（依頼文・束・票・採否の表・裁定・照らしの記録・起草者の見直しの記録）を、公開の置き場に置く案を組み、置く物の一覧とタグの名の案を登録者に示す。push とタグは、そのつど登録者の許しを得てから行う。',
     '- この記録を書いた時刻: %s（日本時間）。' % datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'), '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('D290 | uuid %s | %s | %d 字' % (uuid, jst, len(words)))
