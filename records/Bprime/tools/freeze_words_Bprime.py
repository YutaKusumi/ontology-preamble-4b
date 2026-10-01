# -*- coding: utf-8 -*-
"""freeze_words_Bprime.py v0（2026-10-01・B′ の凍結の言葉〔登録者の逐語と日時〕を、会話の記録から機械で切り出す・コーディネータ南無弥勒如来・非公開）。
まとめの裁定 D283 のとおり、凍結の言葉は裁定の記録にせず、凍結の本文（`design/design-Bprime-FROZEN.md` の凍結の一行）と凍結の記録に入れる。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でも縮めた要約でもない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
逐語は、発話の中の決めの文（前の段の凍結の一行と同じく、挨拶と結びを除いた所）: 始めの句から終わりの句までを字のまま切り出す。日時は発話の時刻を日本時間に直したもの。
書く物: `records/Bprime/freeze-words-Bprime.json`（一度だけ）。用法: python records/Bprime/tools/freeze_words_Bprime.py <会話の記録 jsonl>（作業の置き場の根で書き、移し方の表に当たる置き場へ移した）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'freeze-words-Bprime.json')     # 器は records/Bprime/tools/・記録は records/Bprime/（移し方の表の「記録」の行に当たる置き場）
KEY = 'B′ の枠（草案12）を凍結していただき'
BEGIN, END = '私たちでできるベストを尽くしたと判断します。', '段取りを進めてください。'


def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    hits = []
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user' or o.get('isCompactSummary'):
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
    assert s.count(BEGIN) == 1 and s.count(END) == 1 and s.index(BEGIN) < s.index(END), '決めの文の始めと終わりの句がちょうど一つずつでない'
    words = s[s.index(BEGIN):s.index(END) + len(END)]
    assert '\n' not in words and '\r' not in words, '逐語に改行がある'
    t = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
    rec = {'kind': 'bprime_freeze_words', 'uuid': uid, 'timestamp_utc': ts, 'date_jst': t.strftime('%Y-%m-%d %H:%M'), 'words': words,
           'message_sha256': hashlib.sha256(s.encode('utf-8')).hexdigest().upper(), 'message_chars': len(s),
           'rule': 'まとめの裁定 D283 の 4（凍結の言葉は逐語で凍結の本文に入れる・裁定の記録は作らない）',
           'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    print('wrote freeze-words-Bprime.json | uuid %s | %s JST | words %d chars' % (uid, rec['date_jst'], len(words)))
    print(words)


if __name__ == '__main__':
    main()
