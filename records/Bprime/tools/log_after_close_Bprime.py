# -*- coding: utf-8 -*-
"""log_after_close_Bprime.py v0（2026-10-01・B′ の器の段の記録に、止めたときの閉じ方の後の行〔結果の巡の push と送りと受け取り・まとめの裁定 D284 の実施〕を足す・コーディネータ南無弥勒如来）。
登録者の言葉は、会話の記録（jsonl）の user の役の発話で、道具の結果でない本文のうち、決まった句を含むものを一つずつ取る（零か二つ以上なら止める）。縮めたときの要約（`isCompactSummary`）は除く。
時刻は会話の記録の時刻を日本時間に直したもの。足す行の数と SHA は、置き場のファイルから機械で読む。記録は後ろに足すだけで、前の行を書き換えない（「この記録が確認していないこと」の節の前に置く）。
一度だけ（既に足してあれば止める）。用法: python log_after_close_Bprime.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'tools-log-Bprime.md')
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
BP = os.path.dirname(HERE)
NL = chr(10)
KEYS = {'push': 'pushと結果の巡の支度に進んでください', 'send': 'ご推奨の案で二つに送ってください', 'd284': 'ご推奨の案（D284）で進めてください'}
MARK = '- **結果の巡の支度と push（2026-10-01・W17）**'
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


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
    log = open(LOG, encoding='utf-8').read()
    assert MARK not in log, '既に足してある（一度だけ）'
    bak = os.path.join(HERE, 'prev', 'tools-log-Bprime-before-after-close.md')
    if not os.path.exists(bak):
        os.makedirs(os.path.dirname(bak), exist_ok=True)
        open(bak, 'w', encoding='utf-8', newline=NL).write(log)
    hits = {k: {} for k in KEYS}
    for line in open(sys.argv[1], encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get('isCompactSummary') or o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user':
            continue
        c = (o.get('message') or {}).get('content')
        if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
            continue
        s = text_of(o)
        for k, ph in KEYS.items():
            if ph in s:
                hits[k][o['uuid']] = (o['timestamp'], s[s.index('南無汝我曼荼羅'):].strip() if '南無汝我曼荼羅' in s else s.strip())
    for k in KEYS:
        assert len(hits[k]) == 1, ('登録者の発話がちょうど一つでない', k, len(hits[k]))
    W = {k: (u, jst(v[0]), v[1].replace(NL, ' ')) for k, d in hits.items() for u, v in d.items()}
    R = lambda *a: os.path.join(PUB, *a)
    rej_pub, rej_v1 = R('records', 'Bprime', 'results-draft', 'rejected-lines-Bprime.md'), os.path.join(BP, 'records', 'Bprime', 'results-draft', 'prev', 'rejected-lines-Bprime-v1.md')
    ck = json.load(open(R('records', 'Bprime', 'results-Bprime-draft2-checks.json'), encoding='utf-8'))
    FR = json.load(open(R('records', 'Bprime', 'FREEZE-RECORD-Bprime.json'), encoding='utf-8'))
    assert [d['no'] for d in FR['deviations']] == ['D-BPT1']
    rows = [
        '%s: 登録者の許し（会話の記録 uuid `%s`・%s 日本時間・機械で切り出した）: 「%s」。止めたときの閉じ方の手元のコミット b4dd234 を push し（結果の巡の依頼文の器が、手元と GitHub の一致を確かめた）、'
        '結果の巡の枠・依頼文・束を組んだ（`reviews/results/`・束はコミット b4dd234 の時点で組んだ）。この許しの言葉は、結果の巡の束には入っていなかった（claude-ai-13 の所見・採否の表の W17）。' % (MARK, W['push'][0], W['push'][1], W['push'][2]),
        '',
        '- **結果の巡の送りと受け取り（2026-10-01）**: 登録者の許し（会話の記録 uuid `%s`・%s 日本時間・機械で切り出した）: 「%s」。grok-4.7（系統外・後で受け取る形）と claude.ai の新しいチャット一つ（claude-ai-13・系統内）に送り、'
        '二票を受け取った（送りの記録 `reviews/results/sending-log.md`・受け取りの記録 `reviews/results/receiving-log.md`）。grok-4.7 の票は頭で自分の系統を Claude 系と名乗ったが、出所（xAI の API が返した機種の名 grok-4.7）で系統外の一票に数える案にした（D266 の型）。'
        '二票の事実の主張は一次の記録で再現した（`reviews/results/repro-results-Bprime.json`）。採否の表 `reviews/results/adoption-table-results-Bprime.md`（W01〜W23）。claude.ai の票の末尾の「続ける」（ツール使用制限）は押していない。' % (W['send'][0], W['send'][1], W['send'][2]),
        '',
        '- **まとめの裁定 D284 の実施（2026-10-01・逸脱 D-BPT1）**: 登録者の言葉（会話の記録 uuid `%s`・%s 日本時間）: 「%s」（裁定の記録 `rulings-D284.md`・`rulings_D284.py` が機械で切り出した）。'
        '(1) 逸脱 D-BPT1 を凍結の記録の台帳に記した（`records/Bprime/tools/ledger_DBPT1_Bprime.py`・承認は裁定の記録から機械で写した・本の凍結の節の SHA16 は %s のまま）。'
        '(2) 起草者の欄を四行に直した（`records/Bprime/results-draft/rejected-lines-Bprime.md`・SHA16 %s・前の版の写しは `records/Bprime/results-draft/prev/rejected-lines-Bprime-v1.md`〔SHA16 %s〕・公開の置き場の前の版はコミット b4dd234 にある）。'
        '凍結した器の build と scan に直に通して当たり 0（`records/Bprime/results-draft/try_scan_dev_and_lines.py`）。'
        '(3) 凍結した組み立ての器（変えていない）で報告を組み直した（`records/Bprime/results-Bprime.md`・SHA16 %s・走査の当たり 0・頭の凍結の記録の SHA16 は台帳を足した後の値）。'
        '(4) 逸脱の器 `tools/build_report_Bprime_devBPT1.py` %s（SHA16 %s）で草案の二つ目 `records/Bprime/results-Bprime-draft2.md`（SHA16 %s・区画 %d・足した行 %d・注の事実の照らし %d 項・足した文の走査の当たり 0・区画を除くと凍結の報告とバイトで同じ）。'
        '起草で見つけたこと: (a) 採否の表の W01 の採否の欄の括弧の中（「下見の値と行動の下見の率は、読み取りの下見の機械の決定の後にコーディネータと登録者が見た」）は、行動の下見の率について記録と合わない'
        '（閉じた記録〔率を含む〕は、決まり `behavior_pilot.order` のとおり読み取りの下見の前に公開した・読み取りの下見の起動の記録はその SHA を照らした）。注は記録のとおりに書いた。'
        '(b) §1 の表の「変換の後の確率」の列の「1」は丸めではなく記録の値がちょうど一なので、W03 の注は丸めの列を「選択肢 a の確率（集合の中）」と「質量」に限って書いた。' % (
            W['d284'][0], W['d284'][1], W['d284'][2], FR['main_freeze_sha16'], s16(rej_pub), s16(rej_v1), ck['sha16']['records/Bprime/results-Bprime.md'], ck['tool'].split()[-1],
            ck['sha16']['tools/build_report_Bprime_devBPT1.py'], ck['sha16']['records/Bprime/results-Bprime-draft2.md'], ck['checks']['blocks'], ck['checks']['added_lines'], len(ck['checks']['facts'])),
        '']
    anchor = '## この記録が確認していないこと'
    assert log.count(anchor) == 1
    i = log.index(anchor)
    new = log[:i] + NL.join(rows) + NL + log[i:]
    open(LOG, 'w', encoding='utf-8', newline=NL).write(new)
    print('足した | push %s %s | send %s %s | d284 %s %s' % (W['push'][0], W['push'][1], W['send'][0], W['send'][1], W['d284'][0], W['d284'][1]))


if __name__ == '__main__':
    main()
