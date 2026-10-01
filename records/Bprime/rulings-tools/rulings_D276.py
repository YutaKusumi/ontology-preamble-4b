# -*- coding: utf-8 -*-
"""rulings_D276.py v0（2026-09-30・B′ の裁定 D276 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。束の SHA-256 と本数は束の実物から写す。記録は一度だけ書く。
用法: python rulings_D276.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D276.md')
KEY = 'ようやく、Grokから回答がありましたね。安心しました。ご推奨の案で進めてください。'
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
    hits = []
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user':
            continue
        c = (o.get('message') or {}).get('content')
        if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
            continue
        s = text_of(o)
        if KEY in s:
            hits.append((o['uuid'], o['timestamp'], s))
    uniq = {h[0]: h for h in hits}
    assert len(uniq) == 1, ('登録者の発話がちょうど一つでない', len(uniq))
    uid, ts, s = next(iter(uniq.values()))
    body = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    q_all = body.strip()
    L = ['# 裁定 D276（B′ の器の実装の検分・grok-4.7 の G-01 への追い問い・G-07 は限界・2026-09-30・コーディネータ南無弥勒如来・非公開）', '',
         '- **D276**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - grok-4.7 の返事と R2 への追い問いの返事の報告の後の決め。「決めていただきたいこと」の二項目は、推しの案で進める:',
         '    - grok-4.7 の G-01（重い・前提が材料の外で違うと一次の資料で確かめた）について、移し方の表と合成データの確かめの該当の行を添えて、後で受け取る形で小さな追い問いを一度送る（費用は 1 ドル未満の見込み・D272 の上限の内）。',
         '    - G-07（再抽出の一致は道が返す数だけを見て、活性そのものは渡らない）: 限界として書く（R1-14 と同じ理由: 別の個体の器は変えない決まりで、コーディネータの器に足すと独立の確かめにならない）。',
         '  - 器の直しは、この二つの返事を待たずに進める（D275 のとおり）。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D276.md | uuid %s | %s JST | chars %d' % (uid, jst(ts), len(q_all)))


if __name__ == '__main__':
    main()
