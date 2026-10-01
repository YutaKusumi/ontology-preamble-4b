# -*- coding: utf-8 -*-
"""rulings_D270.py v0（2026-09-30・B′ の裁定 D270 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。
用法: python rulings_D270.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D270.md')
KEY = '「決めていただきたいこと」については、ご推奨の案で進めてください'
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
    L = ['# 裁定 D270（B′ の器の段の所見の決めと、別の個体に書いてもらう器の起動・2026-09-30・コーディネータ南無弥勒如来・非公開）', '',
         '- **D270**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - 「決めていただきたいこと」（コーディネータの報告の四項目）は、推しの案で進める:',
         '    - K5（書式外の引き直し）: 行動の下見では引き直さない（一度の生成を一つの試行とする）。',
         '    - K1（書き出しの根 (b) の囲い）: 鍵を含むブロックの開く囲い（鍵の手前の \'```\' の数が奇数のとき、その最後の \'```\'）とする。',
         '    - K2（暦の期限の数え方）: 封印の日（日本時間）を 0 日目とし、60 日目の日本時間の暦日の終わりまでに終えなければ閉じる。',
         '    - K7（「採点できなかった」の理由）: 上限で切れた・採点の器の例外の二つ。書式外は採点の結果の一つ。上限で切れた応答は破局の形でも主の率の分子に数えない。',
         '    - 器の段で置いた値（転記行 D の数〔上位の次元 8・実効の押しの比を見る方向 名前のある 4・実在の差 28・等方の先頭 32〕と、系統外の模型による採点の依頼の文）は、置いたとおり。依頼の文は器の実装の検分にも掛ける。',
         '    - 字の体裁: 正本の決まった文のうち、〔〕の前後に空白を置いていない型を、ほかの決まった文とそろえる（意味は変えない）。',
         '    - 独立の再計算の二つの道（残差の書き換えの道・独立の再抽出の道）は、書き手と別の新しい個体（エージェント一体・Claude Opus 5.5・系統内）が書く。',
         '  - 助言: 検分を claude.ai の Claude や Grok に依頼するときは、「時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。」の型の一文を依頼文に入れる（密度の濃い回答が得られる傾向・登録者の経験）。',
         '  - 次の段取りを進める。',
         '- 草案と正本への入れ方: 正本は次の版（v4）で、K1・K2・K7 の「登録者の確認待ち」の印を外し、K5 の決め（引き直さない）を `behavior_pilot` に書き、`decisions` に D270 を足し、字の体裁をそろえる。草案は次の草案（10）で、D269 の §12 の替え方とあわせて入れる。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D270.md | uuid %s | %s JST | chars %d' % (uid, jst(ts), len(q_all)))


if __name__ == '__main__':
    main()
