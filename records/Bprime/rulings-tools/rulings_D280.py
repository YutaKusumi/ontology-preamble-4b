# -*- coding: utf-8 -*-
"""rulings_D280.py v0（2026-10-01・B′ の裁定 D280 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
会話の記録を縮めたときの要約（`isCompactSummary` が真の行）は除く（D277 の器と同じ）。束の大きさと SHA-256 はファイルの実物から写す。記録は一度だけ書く。
用法: python rulings_D280.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D280.md')
KEY = 'ご推奨の案（1、だめなら2）で進めてください'
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
    zb = open(ZIP, 'rb').read()
    zsha = hashlib.sha256(zb).hexdigest().upper()
    L = ['# 裁定 D280（B′ の確かめの巡の束の添え方・2026-10-01・コーディネータ南無弥勒如来・非公開）', '',
         '- **D280**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - D279 で送ると決めた束（`reviews/recheck/bundle/recheck-bundle-Bprime.zip`・%d バイト・SHA-256 `%s`）が、claude.ai のページへ添える道（Chrome の拡張の橋）の一度の上限 10 MB を越え、添えられなかった'
         '（依頼文は添えた・まだ送っていない・grok-4.7 は受付済み）。コーディネータは予期しないこととして中断して相談し、次の案を推した。登録者の決め: 推しの案で進める。' % (len(zb), zsha),
         '    1. 同じ zip を、中身を変えずにバイトのまま二つに割って添える。検分者に、`cat` でつなぎ、SHA-256 が上の値と同じことを確かめてから展開してもらう（束も依頼文も変わらない・欄の一文に、つなぎ方と SHA の確かめを足す）。',
         '    2. 1 を claude.ai が受け付けなければ、改めて相談せずに、中身は同じまま二つの zip（トークナイザだけの zip と、残りの zip）に組み直して添える（ファイルごとの SHA は束の目録で照らせる・zip の SHA は新しくなる）。',
         '  - 註: 欄の一文は、枠（`reviews/recheck/00-frame-recheck-Bprime.md`）に「予定」として書いた一文から変わる（送りの記録に、送った一文と違いを書く）。正本の `decisions` には、確かめの巡の後の正本の直しにまとめて入れる。',
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D280.md | uuid %s | %s JST | chars %d | zip %d bytes %s' % (uid, jst(ts), len(q_all), len(zb), zsha[:16]))


if __name__ == '__main__':
    main()
