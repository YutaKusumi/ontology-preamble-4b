# -*- coding: utf-8 -*-
"""rulings_D278.py v0（2026-10-01・B′ の裁定 D278 の記録を、会話の記録から登録者の言葉とコーディネータの見解を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
会話の記録を縮めたときの要約（`isCompactSummary` が真の行）は除く（D277 の器と同じ）。
決めの元になったコーディネータの見解は、登録者の発話の前の assistant の発話のうち、決まった見出しを含む最後のものから、三つの節を見出しで切り出し、行ごとに「> 」を付けて字のまま写す。
時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。
用法: python rulings_D278.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D278.md')
KEY = '凍結前の最後の検分の順にしましょう'
HEAD = '## 見切りの決まり（案）'
SECTIONS = (('## 見切りの決まり（案）', '## 器の組み立ての中の「繰り返しの元」'),
            ('## 器の組み立ての中の「繰り返しの元」', '## 私自身の引力'),
            ('## 決めていただきたいこと', '決めていただいたら、'))
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
    assert before, 'コーディネータの見解が登録者の発話の前に無い'
    aid, ats, a = before[-1]
    body = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    q_all = body.strip()
    cut = []
    for h0, h1 in SECTIONS:
        assert a.count(h0) == 1 and a.count(h1) == 1, (h0, h1)
        i0, i1 = a.index(h0), a.index(h1)
        assert i0 < i1, (h0, h1)
        cut.append(a[i0:i1].rstrip())
    L = ['# 裁定 D278（B′ の見切りの決まり・案16 の決め直し・裁定をまとめる手当て・2026-10-01・コーディネータ南無弥勒如来・非公開）', '',
         '- **D278**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - コーディネータの見解（会話の記録 uuid `%s`・%s 日本時間）の「決めていただきたいこと」の三つを、推しの案で決める:' % (aid, jst(ats)),
         '    1. 見切りの決まり（下に写した 1〜5）を採る。今度の直しの確かめの巡（D277）を、凍結の前の最後の検分の巡とする。依頼文に、見る所の限りと重さの物差しを書く。',
         '    2. 案16 を今決め直す: 独立の再計算の一段目に Nk の行を入れない。「独立の再計算なし」の印（S16）を報告の組み立ての器に入れる。バッチ一の速さは、転記行 E の見込みのための記述にだけ使う'
         '（D263 で推しのとおりとした案16 の「凍結の前にバッチ一の速さを測ってから、費用とあわせて決める」を、この決めで替える）。',
         '    3. 裁定をまとめる手当て: 最後の正本の直しの前に、残りの決めと「最後の確かめが通ったら、凍結まで新しい裁定の記録を作らずに進む」を一つの裁定にまとめていただく。'
         '凍結の言葉は凍結の本文に入る。設計に触れる決めが要る時は止まり、正本に入れてから確かめを取り直す。',
         '  - あわせて（いつもどおり）: この PC は南無観慈如来も使うので、PC の CPU の負荷を減らすため、Colab でできる作業は Colab でする。',
         '  - 註: 正本 v5 の `decisions` は D276 まで。D277 と D278 は、確かめの巡の後の正本の直しにまとめて入れる（D277 の註のとおり）。',
         '', '## 決めの元になったコーディネータの見解（逐語・会話の記録から機械で切り出した・行ごとに「> 」を付けた）', '']
    for c_ in cut:
        L += ['> ' + ln if ln else '>' for ln in c_.split(NL)]
        L.append('')
    L += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D278.md | uuid %s | %s JST | chars %d | view uuid %s | %s JST | sections %s' % (uid, jst(ts), len(q_all), aid, jst(ats), [len(c_) for c_ in cut]))


if __name__ == '__main__':
    main()
