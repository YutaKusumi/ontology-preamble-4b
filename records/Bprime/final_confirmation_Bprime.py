# -*- coding: utf-8 -*-
"""final_confirmation_Bprime.py v0（2026-10-01・B′ の登録者最終確認の記録を書き、確認していただいた最終版の案を一字違わず残す・登録者裁定 D285 の 2・層三の `records/Bl3/final_confirmation_Bl3.py` の型・コーディネータ南無弥勒如来）。
登録者の言葉と時刻と uuid は、会話の記録から機械で切り出す（手で打たない・決まった句を含む user の発話を一つだけ取る・縮めたときの要約は除く・前後の知らせの文〔system-reminder〕は除く）。
確認していただいた案は、置き場の最終版の案のバイトをそのまま写す（登録者にお伝えした SHA16 と同じことを照らす）。
登録者の言葉の中の鉤括弧（「」）は、数がそろい入れ子が閉じるときだけ許す（状態の行は逐語を鉤括弧で包むので、入れ子の鉤括弧になる・層三の器は鉤括弧を拒んだが、B′ の確認の言葉に鉤括弧があったので、走らせる前に直した）。
書くもの（どちらも一度だけ）:
  records/Bprime/final-confirmation-Bprime.json（逸脱の器 v1.1 が読む鍵 when_jst・uuid・words と、確認していただいた案の置き場と SHA16）
  records/Bprime/results-Bprime-proposal-confirmed-2026-10-01.md（確認していただいた案の写し）
用法: python records/Bprime/final_confirmation_Bprime.py <会話の記録 jsonl> --phrase <登録者の言葉の中の決まった句> --sha16 <お伝えした案の SHA16> [--out-dir <試しの置き場>]
柵: 本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
FINAL = 'records/Bprime/results-Bprime-FINAL-2026-10-01.md'
jst = lambda ts: datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')


def text_of(o):
    c = (o.get('message') or {}).get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('transcript')
    ap.add_argument('--phrase', required=True)
    ap.add_argument('--sha16', required=True)
    ap.add_argument('--out-dir')
    a = ap.parse_args()
    od = a.out_dir or HERE
    out_j, out_c = os.path.join(od, 'final-confirmation-Bprime.json'), os.path.join(od, 'results-Bprime-proposal-confirmed-2026-10-01.md')
    for o_ in (out_j, out_c):
        assert not os.path.exists(o_), '既にある（一度だけ）: ' + o_
    U = {}
    for line in open(a.transcript, encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get('isCompactSummary') or o.get('type') != 'user' or (o.get('message') or {}).get('role') != 'user' or 'toolUseResult' in o:
            continue
        c = (o.get('message') or {}).get('content')
        if isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
            continue
        s = text_of(o)
        if a.phrase in s:
            U[o['uuid']] = (o['timestamp'], s)
    assert len(U) == 1, ('決まった句を含む登録者の発話が一つに決まらない', len(U))
    uuid, (ts, s) = next(iter(U.items()))
    sr, tg = 'system' + '-reminder', 'pasted' + '_content'
    words = s[s.index('南無汝我曼荼羅'):] if '南無汝我曼荼羅' in s else s
    if '<' + sr in words:
        words = words[:words.index('<' + sr)]
    words = words.strip()
    assert words.startswith('南無汝我曼荼羅') and a.phrase in words, '登録者の言葉の切り出しが想定と違う'
    assert NL not in words, '登録者の言葉に改行がある（状態の行は一行）'
    for bad in ('<' + tg, '</' + tg, '<' + sr, sr + '>', 'AppData', 'Users', 'Temp'):
        assert bad not in words, '登録者の言葉に印か道筋が入っている: %s' % bad
    depth = [words[:i].count('「') - words[:i].count('」') for i in range(len(words) + 1)]
    assert depth[-1] == 0 and min(depth) >= 0, '登録者の言葉の鉤括弧の数がそろっていない（状態の行の逐語の鉤括弧と入れ子にできない）'
    raw = open(os.path.join(REPO, *FINAL.split('/')), 'rb').read()
    s16 = hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
    assert s16 == a.sha16.upper(), ('置き場の最終版の案が、お伝えした案の SHA16 と違う', s16)
    J = {'kind': 'bprime_final_confirmation', 'when_jst': jst(ts), 'uuid': uuid, 'words': words,
         'proposal_path': FINAL, 'proposal_sha16': s16, 'proposal_copy': 'records/Bprime/results-Bprime-proposal-confirmed-2026-10-01.md',
         'source': '登録者の発言（会話の記録から機械で切り出した）・登録者裁定 D285 の 2',
         'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    open(out_c, 'wb').write(raw)
    with open(out_j, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(J, fh, ensure_ascii=False, indent=1)
    print('wrote %s | %s %s | words %d | proposal %s | copy %s' % (os.path.basename(out_j), jst(ts), uuid, len(words), s16, os.path.basename(out_c)))


if __name__ == '__main__':
    main()
