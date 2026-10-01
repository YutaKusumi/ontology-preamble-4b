# -*- coding: utf-8 -*-
"""rulings_D274.py v0.1（2026-09-30・v0.1: 一度目と二度目の書き出しで記録の行の裁定の番号が前の裁定のままだったのを直した〔書いた直後に見つけて消し、書き直した〕・B′ の裁定 D274 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、本文の全体が決まった文と一字違わず同じものを一つだけ取る（二つ以上か零なら止める）。
（決まった句を含むだけの判定では、会話の続きの要約の中の同じ句にも当たるため、全体の一致で取る。）言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。
用法: python rulings_D274.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D274.md')
FULL = '南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏ご推奨の案で進めてください。よろしくお願いします🍵'
AFTER = '2026-09-30T09:40:00Z'
NL = chr(10)


def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
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
        if text_of(o).strip() == FULL and o['timestamp'] > AFTER:
            hits.append((o['uuid'], o['timestamp']))
    uniq = dict(hits)
    assert len(uniq) == 1, ('登録者の発話がちょうど一つでない', len(uniq))
    uid, ts = next(iter(uniq.items()))
    L = ['# 裁定 D274（B′ の器の実装の検分・grok-4.7 の送り直し〔後で受け取る形〕・採否の表の作り始め・2026-09-30・コーディネータ南無弥勒如来・非公開）', '',
         '- **D274**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), FULL),
         '  - 前の問い（grok-4.7 の窓の大きさが原因か）への答え（発話はおよそ 9 万〜12 万トークンの見込みで窓の内・窓を超えればすぐに断られる・今回は受け付けたまま返事が来なかった）の後の決め。「決めていただきたいこと」の二項目は、推しの案で進める:',
         '    - grok-4.7 に、同じ発話（`reviews/impl/grok/grok-message.md`・中身は変えない）を、xAI の後で受け取る形（deferred completion・受付番号を取り、答えを取りに行く）で一度だけ送り直す。費用は一度目の分かもしれない額を含めて D272 の上限 5 ドルの内。この形が受け付けられなければ、その時点で改めて相談する。',
         '    - 採否の表（U01〜）を、grok-4.7 の返事を待たずに claude.ai の二つのチャットの所見から作り始め、grok-4.7 の所見は届いたら足す（和集合）。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D274.md | uuid %s | %s JST' % (uid, jst(ts)))


if __name__ == '__main__':
    main()
