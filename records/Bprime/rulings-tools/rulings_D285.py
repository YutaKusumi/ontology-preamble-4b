# -*- coding: utf-8 -*-
"""rulings_D285.py v0（2026-10-01・B′ の裁定 D285〔最終検分の後のまとめの裁定〕の記録を、会話の記録から登録者の言葉とコーディネータの案を機械で切り出して書く・`rulings_D284.py` の型・コーディネータ南無弥勒如来）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。縮めたときの要約（`isCompactSummary`）は除く。
決めの元になったコーディネータの案は、登録者の発話の前の assistant の発話のうち、決まった見出しを含む最後のものから、二つの節を見出しで切り出し（二つ目は発話の終わりまで）、行ごとに「> 」を付けて字のまま写す。
時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。用法: python rulings_D285.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D285.md')
KEY = 'ご推奨の案（D285）で進めてください'
HEAD = '## まとめの裁定の案 D285'
S1 = '## 公開の前に直すもの（票の所見）'
NL = chr(10)


def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''


def jst(ts):
    return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    users, assts = [], []
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get('isCompactSummary'):
            continue
        s = text_of(o)
        if o.get('type') == 'assistant' and HEAD in s:
            assts.append((o['uuid'], o['timestamp'], s))
        if o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user':
            continue
        c = (o.get('message') or {}).get('content')
        if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
            continue
        if KEY in s:
            users.append((o['uuid'], o['timestamp'], s))
    uu = {h[0]: h for h in users}
    assert len(uu) == 1, ('登録者の発話がちょうど一つでない', len(uu))
    uid, ts, s = next(iter(uu.values()))
    before = [a for a in assts if a[1] < ts]
    assert before, 'コーディネータの案が登録者の発話の前に無い'
    aid, ats, a = before[-1]
    body = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    q_all = body.strip()
    assert a.count(S1) == 1 and a.count(HEAD) == 1 and a.index(S1) < a.index(HEAD)
    cut = [a[a.index(S1):a.index(HEAD)].rstrip(), a[a.index(HEAD):].rstrip()]
    L = ['# 裁定 D285（B′ の最終検分の後のまとめの裁定・2026-10-01・コーディネータ南無弥勒如来）', '',
         '- **D285**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - コーディネータの案（会話の記録 uuid `%s`・%s 日本時間）の「まとめの裁定の案 D285」の 1〜5 を、推しのとおりに決める:' % (aid, jst(ats)),
         '    1. grok-4.7 の最終検分の票は、出所（xAI の API・返った機種の名 grok-4.7・請求）で系統外の一票に数える（票の頭の申告も出所と合う・D266）。',
         '    2. 最終版の状態の行と検分票を今の状態に合わせる（採否の表 `reviews/results-final/adoption-table-final-Bprime.md` の X01・X07）: 逸脱 D-BPT1 の器を v1 に上げ、`--final` で最終版を組む（見出し・状態の行〔正本 `report_rules.template` の登録者最終確認の前と後の二つの型〕・頭の添え・検分票だけを改める・草案の二つ目は書き換えない・最終版との違いが決めた行だけであることを器が確かめる）。登録者最終確認の後は、確認の言葉を会話の記録から機械で切り出して確認の記録に置き、状態の行を確認の後の型にして最終版を組み直す。',
         '    3. 鍵の確かめの器を広げ（X02）、公開するファイルのすべてに掛けて記録を残す。注のファイルも公開物と一緒に置く（X08）。',
         '    4. ほかの所見（X03〜X06）と、凍結した器の欠け二つ（X07 の状態の型・W15 の版の印字）は記録に置く（後の登録の器の直しの候補）。',
         '    5. この後の順: 最終版の案 → 起草者の最終の見直し → 登録者最終確認 → 確認の後の状態で組み直し → push ⑧（最終版・最終の巡の記録・W22 の公開物・凍結の後の器の段の記録・確かめの記録）→ タグ（層三の型）。push とタグは、そのつど登録者の許しを得る。',
         '  - 註: 凍結の後の裁定（正本の `decisions` には入らない・正本は凍結物）。登録者の言葉（上の逐語）には、器の漏れ（X07）についての言葉がある（次の登録で活かす）。次の番号は D286。',
         '', '## 決めの元になったコーディネータの案（逐語・会話の記録から機械で切り出した・行ごとに「> 」を付けた）', '']
    for c_ in cut:
        L += ['> ' + ln if ln else '>' for ln in c_.split(NL)]
        L.append('')
    L += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D284.md | uuid %s | %s JST | chars %d | view uuid %s | %s JST | sections %s' % (uid, jst(ts), len(q_all), aid, jst(ats), [len(c_) for c_ in cut]))


if __name__ == '__main__':
    main()
