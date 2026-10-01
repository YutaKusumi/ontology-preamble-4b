# -*- coding: utf-8 -*-
"""rulings_D279.py v0（2026-10-01・B′ の裁定 D279 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
会話の記録を縮めたときの要約（`isCompactSummary` が真の行）は除く（D277 の器と同じ）。
束の SHA-256 と、依頼文・発話・枠の SHA16 は、ファイルの実物から写し、送る前の刻印（`reviews/recheck/frame-stamp.txt`）の値と照らす。記録は一度だけ書く。
用法: python rulings_D279.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D279.md')
KEY = 'ご推奨の案で送ってください'
RC = os.path.join(HERE, 'reviews', 'recheck')
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
    body = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    q_all = body.strip()
    stamp = open(os.path.join(RC, 'frame-stamp.txt'), encoding='utf-8').read()
    zsha = hashlib.sha256(open(os.path.join(RC, 'bundle', 'recheck-bundle-Bprime.zip'), 'rb').read()).hexdigest().upper()
    s16 = lambda p: hashlib.sha256(open(os.path.join(RC, p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
    req16, grok16, frame16 = s16('request-recheck-Bprime.md'), s16('grok/grok-recheck-message.md'), s16('00-frame-recheck-Bprime.md')
    for v in (zsha, req16, grok16, frame16):
        assert v in stamp, ('送る前の刻印と違う', v)
    L = ['# 裁定 D279（B′ の器の実装の直しの確かめの巡を送る・2026-10-01・コーディネータ南無弥勒如来・非公開）', '',
         '- **D279**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - 確かめの巡の用意（束・依頼文・発話・枠）の報告の後の決め: 推しの案で送る。',
         '    - claude.ai の新しいチャット一つ（系統内・Claude Opus 5.5・思考「超高」）: 登録者の Chrome をコーディネータが操作して開き、依頼文 `reviews/recheck/request-recheck-Bprime.md`（SHA16 `%s`）と束 `reviews/recheck/bundle/recheck-bundle-Bprime.zip`（SHA-256 `%s`）を添えて送る。' % (req16, zsha),
         '    - grok-4.7（系統外）: 発話 `reviews/recheck/grok/grok-recheck-message.md`（SHA16 `%s`）を、後で受け取る形で一度だけ送る（器 `reviews/recheck/grok/send_grok_recheck_deferred.py`・費用の上限 3 ドル）。' % grok16,
         '    - 送らない枠 `reviews/recheck/00-frame-recheck-Bprime.md`（SHA16 `%s`）の予想と採否の決め方（D278 の見切りの決まり）は、票を受け取る前に書いた（送る前の刻印 `reviews/recheck/frame-stamp.txt`）。' % frame16,
         '  - 註: 正本 v5 の `decisions` は D276 まで。D277〜D279 は、確かめの巡の後の正本の直しにまとめて入れる（D277・D278 の註のとおり）。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D279.md | uuid %s | %s JST | chars %d | bundle %s | request %s | grok %s | frame %s' % (uid, jst(ts), len(q_all), zsha[:16], req16, grok16, frame16))


if __name__ == '__main__':
    main()
