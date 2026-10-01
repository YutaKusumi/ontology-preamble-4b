# -*- coding: utf-8 -*-
"""freeze_words_main_Bprime.py v0（2026-10-01・B′ の本の凍結の言葉〔登録者の逐語と日時〕を、会話の記録から機械で切り出す・`freeze_words_Bprime.py` の型・コーディネータ南無弥勒如来）。
読み取りの下見の機械の決定が「止める」になり、登録者が止めたときの道（本の凍結の器で下見の記録と機械の決定を凍結の記録に足す → 集計の段 stopped → 報告）で閉じることを許した発話から取る。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でも縮めた要約でもない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
逐語は、発話の中の決めの文（挨拶と結びを除いた所・下見の前の凍結の言葉と同じ型）: 決まった句を字のまま切り出す。日時は発話の時刻を日本時間に直したもの。
書く物: `records/Bprime/main-freeze-words-Bprime.json`（一度だけ）。用法: python records/Bprime/tools/freeze_words_main_Bprime.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'main-freeze-words-Bprime.json')
PHRASE = 'ご推奨の段取りで閉じてください'
JST = datetime.timezone(datetime.timedelta(hours=9))


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
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get('isCompactSummary') or o.get('type') != 'user' or 'toolUseResult' in o:
            continue
        t = text_of(o)
        if PHRASE in t:
            hits.append((o.get('timestamp'), o.get('uuid'), t))
    assert len(hits) == 1, ('決まった句を含む登録者の発話が一つでない', len(hits))
    ts, uuid, t = hits[0]
    i = t.index(PHRASE)
    words = t[i:i + len(PHRASE)]
    when = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(JST).strftime('%Y-%m-%d %H:%M')
    rec = {'kind': 'bprime_main_freeze_words', 'words': words, 'date_jst': when, 'source': {'uuid': uuid, 'timestamp_utc': ts, 'utterance_sha16': hashlib.sha256(t.encode('utf-8')).hexdigest().upper()[:16]},
           'how': '会話の記録の user の役の発話（道具の結果と縮めた要約を除く）のうち、決まった句を含むただ一つから、決まった句を字のまま切り出した（挨拶と結びは除いた）',
           'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(rec, fh, ensure_ascii=False, indent=1)
    print(json.dumps(rec, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
