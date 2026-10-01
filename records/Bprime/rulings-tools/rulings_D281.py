# -*- coding: utf-8 -*-
"""rulings_D281.py v0（2026-10-01・B′ の裁定 D281 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
会話の記録を縮めたときの要約（`isCompactSummary` が真の行）は除く（D277 の器と同じ）。記録は一度だけ書く。
用法: python rulings_D280.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D281.md')
KEY = 'ご推奨の案で「続ける」を押してください'
ZIP = os.path.join(HERE, 'reviews', 'recheck', 'bundle', 'recheck-bundle-Bprime.zip')
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
    L = ['# 裁定 D281（B′ の確かめの巡の claude-ai-12 の「続ける」・2026-10-01・コーディネータ南無弥勒如来・非公開）', '',
         '- **D281**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - claude-ai-12 の返事（`reviews/recheck/votes/claude-ai-12/`）は、道具の呼び出しの上限で途中まで（返事の下に「Claudeはこのターンのツール使用制限に達しました。」と「続ける」の釦が一つ）。'
         '依頼した見る所のうち、閉じる器のやり直しの道と、いくつかの器の差分・正式の記録・裁定を見ていない。登録者の決め: 推しの案で「続ける」を一度だけ押す（同じ巡の中で、頼んだ範囲を見終えてもらう・前の巡の D273 の型）。',
         '  - 続きの返事を受け取った後、二つの返事（grok-4.7・claude-ai-12 と続き）の和集合で採否の表を作り、物差しで分けた重さと理由を添えて登録者に見せる（D278 の見切りの決まり）。',
         '  - 註: 正本の `decisions` には、確かめの巡の後の正本の直しにまとめて入れる。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D281.md | uuid %s | %s JST | chars %d' % (uid, jst(ts), len(q_all)))


if __name__ == '__main__':
    main()
