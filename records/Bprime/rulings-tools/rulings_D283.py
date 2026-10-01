# -*- coding: utf-8 -*-
"""rulings_D283.py v0（2026-10-01・B′ の裁定 D283〔まとめの裁定〕の記録を、会話の記録から登録者の言葉とコーディネータの案を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
会話の記録を縮めたときの要約（`isCompactSummary` が真の行）は除く（D277 の器と同じ）。
決めの元になったコーディネータの案は、登録者の発話の前の assistant の発話のうち、決まった見出しを含む最後のものから、二つの節を見出しで切り出し、行ごとに「> 」を付けて字のまま写す。
時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。
用法: python rulings_D283.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D283.md')
KEY = 'ご推奨の案（1〜6 のとおり）で進めてください'
HEAD = '## まとめの裁定（D283）の案'
SECTIONS = (('## 訂正（U32 の `.gitattributes`）', '## まとめの裁定（D283）の案'),
            ('## まとめの裁定（D283）の案', '## 決めていただきたいこと'))
NL = chr(10)


def text_of(o):
    m = o.get('message') or {}
    c = m.get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = [x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text']
        return ''.join(parts)
    return ''


def jst(ts):
    t = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    return t.astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    users, assts = [], []
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        s = text_of(o)
        if o.get('type') == 'assistant' and HEAD in s:
            assts.append((o['uuid'], o['timestamp'], s))
        if o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user' or o.get('isCompactSummary'):
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
    cut = []
    for h0, h1 in SECTIONS:
        assert a.count(h0) == 1 and a.count(h1) == 1, (h0, h1)
        i0, i1 = a.index(h0), a.index(h1)
        assert i0 < i1, (h0, h1)
        cut.append(a[i0:i1].rstrip())
    L = ['# 裁定 D283（B′ のまとめの裁定〔凍結の前の最後の裁定〕・2026-10-01・コーディネータ南無弥勒如来・非公開）', '',
         '- **D283**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - コーディネータの案（会話の記録 uuid `%s`・%s 日本時間）の「まとめの裁定（D283）の案」の 1〜6 を、推しのとおりに決める（D278 の 3 の「最後の正本の直しの前の、一つの裁定」）:' % (aid, jst(ats)),
         '    1. 採否の表（`reviews/recheck/adoption-table-recheck-Bprime.md`・V01〜V17）を確認。',
         '    2. 最後の正本と草案の直し（草案12・正本 v6）に、下に写した一覧のものを入れる（裁定 D277〜D283・次の番号は D284）。',
         '    3. Colab で、最後の合成データの確かめを一度走らせる。',
         '    4. すべて期待どおりなら、新しい裁定の記録を作らずに、結果の報告 → 凍結の言葉（逐語で凍結の本文に入れる）→ 凍結の本文を組み公開の置き場に写して push（G4 の確かめの前）→ G4 の確かめ（封印の前の実物の走り・意味のない列だけ）→ 露出の記録 → 下見の前の凍結 → 凍結の記録の push、の順に進む。',
         '    5. 確かめの器そのものの誤りで行が外れたときは、その器だけを直して取り直してよい（器の本体と正本に触れない直しに限る・直したことは記録に書く）。',
         '    6. それ以外の予期しないことが起きたら止めて相談する（新しい裁定になり、正本を直して確かめを取り直す）。',
         '  - あわせて: 登録者の予想の欄は、凍結の後の予想の封印の段で、後で書く（登録者が承知した）。',
         '  - 註: この記録は、D278 の決まりどおり最後の正本の直しの前の裁定で、正本 v6 の `decisions` の最後の番号になる（次の番号 D284）。この後、凍結までの間は、予期しないことが無ければ裁定の記録を作らない。',
         '', '## 決めの元になったコーディネータの案（逐語・会話の記録から機械で切り出した・行ごとに「> 」を付けた）', '']
    for c_ in cut:
        L += ['> ' + ln if ln else '>' for ln in c_.split(NL)]
        L.append('')
    L += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D283.md | uuid %s | %s JST | chars %d | view uuid %s | %s JST | sections %s' % (uid, jst(ts), len(q_all), aid, jst(ats), [len(c_) for c_ in cut]))


if __name__ == '__main__':
    main()
