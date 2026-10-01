# -*- coding: utf-8 -*-
"""rulings_D273.py v0（2026-09-30・B′ の裁定 D273 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、本文の全体が決まった文と一字違わず同じものを一つだけ取る（二つ以上か零なら止める）。
（決まった句を含むだけの判定では、会話の続きの要約の中の同じ句にも当たるため、全体の一致で取る。）言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。
用法: python rulings_D273.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D273.md')
FULL = '南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏ご推奨の案で進めてください🍵'
AFTER = '2026-09-30T09:00:00Z'
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
    L = ['# 裁定 D273（B′ の器の実装の検分の続き・claude.ai の二つのチャットの「続ける」・grok-4.7 の待ち・2026-09-30・コーディネータ南無弥勒如来・非公開）', '',
         '- **D273**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), FULL),
         '  - 「決めていただきたいこと」（コーディネータの状況の報告の二項目）は、推しの案で進める:',
         '    - claude.ai の二つのチャット（claude-ai-10〔R1〕・claude-ai-11〔R2〕）は、一つ目の返事が「このターンのツール使用制限」で途中までだったので、返事の下の「続ける」の釦を押して、読めなかった所の検分を続けてもらう。'
         '続きの返事は別の記録として残す（一つ目の記録は変えない）。返事の下の入力の欄に出ていた赤い囲みの注意の表示（同じ添付と、括弧が半角の同じ一文）には触れない。',
         '    - grok-4.7 の呼び出しは、器の待ちの上限（3600 秒・18:28:53）まで待つ。切れたら、送り直す前に登録者に相談する（二重の費用を避ける）。',
         '  - あわせて、返事を待つ間に、R2 の「重い」の所見を器の本文で確かめる（読むだけ）。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D273.md | uuid %s | %s JST' % (uid, jst(ts)))


if __name__ == '__main__':
    main()
