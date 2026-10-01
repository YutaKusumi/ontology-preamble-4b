# -*- coding: utf-8 -*-
"""rulings_D284.py v0（2026-10-01・B′ の裁定 D284〔結果の巡の後のまとめの裁定〕の記録を、会話の記録から登録者の言葉とコーディネータの案を機械で切り出して書く・`rulings_D283.py` の型・コーディネータ南無弥勒如来）。
登録者の発話は、会話の記録（jsonl）の中の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つだけ取る（二つ以上か零なら止める）。縮めたときの要約（`isCompactSummary`）は除く。
決めの元になったコーディネータの案は、登録者の発話の前の assistant の発話のうち、決まった見出しを含む最後のものから、二つの節を見出しで切り出し（二つ目は発話の終わりまで）、行ごとに「> 」を付けて字のまま写す。
時刻は会話の記録の時刻を日本時間に直したもの。記録は一度だけ書く。用法: python rulings_D284.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'rulings-D284.md')
KEY = 'ご推奨の案（D284）で進めてください'
HEAD = '## まとめの裁定の案（D284・一つにまとめて）'
S1 = '## 採否の案の要点'
NL = chr(10)


def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''


def jst(ts):
    return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    users, assts = [], []
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get('isCompactSummary'):
            continue
        s = text_of(o)
        if o.get('type') == 'assistant' and HEAD in s:
            assts.append((o['uuid'], o['timestamp'], s))
        if o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user':
            continue
        c = (o.get('message') or {}).get('content')
        if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
            continue
        if KEY in s:
            users.append((o['uuid'], o['timestamp'], s))
    uu = {h[0]: h for h in users}
    assert len(uu) == 1, ('登録者の発話がちょうど一つでない', len(uu))
    uid, ts, s = next(iter(uu.values()))
    before = [a for a in assts if a[1] < ts]
    assert before, 'コーディネータの案が登録者の発話の前に無い'
    aid, ats, a = before[-1]
    body = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    q_all = body.strip()
    assert a.count(S1) == 1 and a.count(HEAD) == 1 and a.index(S1) < a.index(HEAD)
    cut = [a[a.index(S1):a.index(HEAD)].rstrip(), a[a.index(HEAD):].rstrip()]
    L = ['# 裁定 D284（B′ の結果の巡の後のまとめの裁定・2026-10-01・コーディネータ南無弥勒如来）', '',
         '- **D284**（登録者・会話の記録 uuid `%s`・%s 日本時間）。登録者の言葉（逐語・会話の記録から機械で切り出した）: 「%s」' % (uid, jst(ts), q_all.replace(NL, ' ')),
         '  - コーディネータの案（会話の記録 uuid `%s`・%s 日本時間）の「まとめの裁定の案（D284）」の 1〜7 を、推しのとおりに決める:' % (aid, jst(ats)),
         '    1. grok-4.7 の結果の巡の票は、票の頭の自己の申告（「起草者と同じ Claude 系」）ではなく出所（xAI の API・返った機種 `grok-4.7`・請求）で、系統外の一票に数える（D266 の型）。',
         '    2. 採否の表（`reviews/results/adoption-table-results-Bprime.md`）の注の区画（W01〜W06・W12・W15・W16・W19）を、層三の D-BLT1 の型の逸脱（凍結した組み立ての器の出力をバイトのまま作り直して照らし、印を付けた区画だけを足す・機械の行は一字も変えない）で足す。逸脱は凍結の記録の台帳に記す。',
         '    3. 起草者の欄の三行に範囲の句を足し、四行目を足す（W11・凍結した器の走査を通す）。',
         '    4. 公開の扱いは W22 のとおり（系統外の採点の束と返事・行動の下見の生成と採点の出力・走りの進みの記録〔秘密が無いことを機械で確かめてから〕・凍結の後の器の段の記録〔別の名〕を公開し、npz・画面の写し・会話の記録の全体は公開しない・注を添える）。',
         '    5. ほかの所見（W07〜W10・W13・W14・W17・W18・W20・W21・W23）は記録に置く。',
         '    6. claude.ai の票の末尾の「続ける」（ツール使用制限）は押さない。票が「済んでいない」と書いた確かめ（起草者の欄の言い換えの走査）は、凍結した走査の器を通して起草者が行う。',
         '    7. この後の順: 逸脱の器と注の文の起草 → 起草者の欄の直し → 報告の最終版の案 → 最終の系統外の一票（grok-4.7・新しい呼び出し・「最終」・採否の行 X01〜）→ 起草者の最終の見直し → 登録者最終確認と公開。',
         '  - 註: 凍結の後の裁定（正本の `decisions` には入らない・正本は凍結物）。次の番号は D285。',
         '', '## 決めの元になったコーディネータの案（逐語・会話の記録から機械で切り出した・行ごとに「> 」を付けた）', '']
    for c_ in cut:
        L += ['> ' + ln if ln else '>' for ln in c_.split(NL)]
        L.append('')
    L += ['本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
    print('wrote rulings-D284.md | uuid %s | %s JST | chars %d | view uuid %s | %s JST | sections %s' % (uid, jst(ts), len(q_all), aid, jst(ats), [len(c_) for c_ in cut]))


if __name__ == '__main__':
    main()
