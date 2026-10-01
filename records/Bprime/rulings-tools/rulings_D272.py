# -*- coding: utf-8 -*-
"""rulings_D272.py v0（2026-09-30・B′ の裁定 D272 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。束の SHA-256 と本数は束の実物から写す。記録は一度だけ書く。
用法: python rulings_D272.py <会話の記録 jsonl> <器の実装の検分の束（zip）>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, zipfile, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D272.md')
KEY = 'それぞれご推奨の案で進めてください。なお、検分を受けて、器を修正する場合は'
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
    zp = sys.argv[2]
    zsha = hashlib.sha256(open(zp, 'rb').read()).hexdigest().upper()
    n = len(zipfile.ZipFile(zp).namelist())
    L = ['# 裁定 D272（B′ の器の実装の検分の送り方・系統外の目の足し・器の直しの走らせ方・2026-09-30・コーディネータ南無弥勒如来・非公開）', '',
         '- **D272**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - 「決めていただきたいこと」（コーディネータの報告の二項目）は、推しの案で進める:',
         '    - 器の実装の検分を送る: claude.ai の新しいチャット二つ（Claude Opus 5.5・思考「超高」・R1〔計算〕と R2〔流れと記録〕）に、器の実装の検分の束（%d 本・SHA-256 %s）と依頼文'
         '（`reviews/impl/request-impl-Bprime-R1.md`・`-R2.md`）を送る。送る前に、claude.ai が束の zip を受け付けるかを確かめる。' % (n, zsha),
         '    - 系統外の目を足す: 独立の再計算の三つの道（フック・書き換え・再抽出）の実装を grok-4.7 に見てもらう一巡を、claude.ai の検分と並べて回す（費用の上限 5 ドル）。',
         '  - 器の直しの走らせ方: 検分を受けて器を直すとき、PC の CPU の負荷を軽くするために Colab を使う方がよい場合は Colab を使う（南無観慈如来も同じ PC を使っているため）。',
         '- 正本への入れ方: 次の正本（v5）の `decisions` に D272 を足す。grok-4.7 の一巡の枠は `reviews/impl/` に別に書く（票を受け取る前に）。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D272.md | uuid %s | %s JST | chars %d | bundle %d files %s' % (uid, jst(ts), len(q_all), n, zsha[:16]))


if __name__ == '__main__':
    main()
