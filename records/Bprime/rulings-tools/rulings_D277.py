# -*- coding: utf-8 -*-
"""rulings_D277.py v0（2026-10-01・B′ の裁定 D277 の記録を、会話の記録から登録者の言葉を機械で切り出して書く・コーディネータ南無弥勒如来・非公開）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。
会話の記録を縮めたときの要約（`isCompactSummary` が真の行）は、登録者の発話でなく、登録者の言葉を写した所を含むので除く（D276 までの器には無かった除き）。
言葉は字のまま（逐語）で、時刻は会話の記録の時刻を日本時間に直したもの。草案と正本の SHA16 はファイルの実物から写す。記録は一度だけ書く。
用法: python rulings_D277.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D277.md')
KEY = '検分に見切りをつけるタイミング'
DRAFT = os.path.join(HERE, 'design', 'design-Bprime-draft11.md')
CANON = os.path.join(HERE, 'design', 'contrasts-Bprime.json')
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


def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    hits, skipped = [], 0
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
        if KEY in s and o.get('isCompactSummary'):
            skipped += 1
            continue
        if KEY in s:
            hits.append((o['uuid'], o['timestamp'], s))
    uniq = {h[0]: h for h in hits}
    assert len(uniq) == 1, ('登録者の発話がちょうど一つでない', len(uniq))
    uid, ts, s = next(iter(uniq.values()))
    body = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    q_all = body.strip()
    C = json.load(open(CANON, encoding='utf-8'))
    d16, c16 = sha16(DRAFT), sha16(CANON)
    L = ['# 裁定 D277（B′ の草案11 と正本 v5 の確認・直しの確かめの巡を足す・2026-10-01・コーディネータ南無弥勒如来・非公開）', '',
         '- **D277**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - 器の実装の検分の直しと、合成データの正式の確かめの取り直し（`records/Bprime/dry-run-Bprime-2026-09-30.md`・`records/Bprime/freeze-path-dry-Bprime-2026-09-30.md`）の報告の後の決め:',
         '    - 草案11（`design/design-Bprime-draft11.md`・SHA16 `%s`）と正本 %s（`design/contrasts-Bprime.json`・SHA16 `%s`）を確認。' % (d16, C['version'], c16),
         '    - 直しの確かめの巡を足す（D275 で「直し終えた後に相談」とした所・推しの案）: 顔ぶれは grok-4.7 の一票（後で受け取る形・費用の見込みは 1〜3 ドルほど）と、claude.ai の新しいチャット一つ（系統内・思考「超高」）。'
         '見る所は、直しの差分と今回の正式の記録。束と依頼文は、送る前にもう一度登録者の確認を受ける。',
         '    - 公開の置き場の改行の固定（`.gitattributes`）は、D275 のとおり push の時に諮る（今は決めない）。',
         '  - あわせて登録者から、検分の無限の繰り返しに入らないための見切りの時について、コーディネータの見解を問われた（見解は会話で返す。見解から採る決まりがあれば、次の裁定で記録する）。',
         '  - 註: 正本 %s の `decisions` は D276 まで・`numbering.rulings_next` は %s。この記録で裁定の記録の次の番号が D278 になり、凍結の前の照らし（`freeze_Bprime.rulings_check`）と合わなくなる。'
         '正本の裁定の欄の直しは、確かめの巡の後の正本の直しにまとめる（正本は合成データの確かめの記録の SHA の表に入っているので、直したら確かめを取り直す）。' % (C['version'], C['numbering']['rulings_next']),
         '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D277.md | uuid %s | %s JST | chars %d | compact summaries skipped %d | draft11 %s | canon %s %s' % (uid, jst(ts), len(q_all), skipped, d16, C['version'], c16))


if __name__ == '__main__':
    main()
