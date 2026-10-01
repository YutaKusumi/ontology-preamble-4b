# -*- coding: utf-8 -*-
"""extract_capture.py v0.2（2026-09-30・v0.2: 全角の空白〔U+3000〕も本文の読み取りで普通の空白に変わるので、印 U+2422 に置き換えて表示し、切り出すときに戻す〔v0.1 の R2 の続きの切り出しは SHA が合わず書かなかった〕／v0.1: 本文の読み取りの道具が行の頭の空白を落とすので、ページの中で空白を印 U+2423 に置き換えて表示し、切り出すときに戻す〔v0 の切り出しは SHA が合わず書かなかった〕・B′ の器の実装の検分の返事を、会話の記録（jsonl）の道具の結果から機械で切り出す・コーディネータ南無弥勒如来）。
ダウンロードが止められたときの道: ページの中で「写す」ボタンの文を受け取り、ページの表示を一時的に印つきの <pre> に置き換えて本文の読み取りの道具で取った。
その道具の結果（会話の記録の tool_result）から、印のあいだの文を切り出し、SHA-256 を計算して、ページの中の値と一致したときだけ書く（一致しなければ書かない）。
用法: python extract_capture.py <会話の記録 jsonl> <印の名（R1C など）> <ページの中の SHA-256> <書き出すファイル>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib
sys.stdout.reconfigure(encoding='utf-8')


def results(path):
    for line in open(path, encoding='utf-8'):
        if not line.strip():
            continue
        o = json.loads(line)
        c = (o.get('message') or {}).get('content')
        if not isinstance(c, list):
            continue
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'tool_result':
                cc = x.get('content')
                if isinstance(cc, str):
                    yield cc
                elif isinstance(cc, list):
                    for y in cc:
                        if isinstance(y, dict) and y.get('type') == 'text':
                            yield y.get('text', '')


def main():
    log, mark, page_sha, out = sys.argv[1:5]
    b, e = '@@CAPTURE-%s-BEGIN@@\n' % mark, '\n@@CAPTURE-%s-END@@' % mark
    hits = [r for r in results(log) if b in r and e in r]
    if not hits:
        raise SystemExit('印のついた道具の結果が無い')
    r = hits[-1]
    text = r[r.index(b) + len(b):r.index(e)].replace(chr(0x2423), ' ').replace(chr(0x2422), chr(0x3000))        # 空白の印を戻す（v0.1〜v0.2・元の文に U+2423 と U+2422 が無いことはページの中で確かめる）
    sha = hashlib.sha256(text.encode('utf-8')).hexdigest().upper()
    want = page_sha.replace(' ', '').upper()
    if sha != want:
        raise SystemExit('ページの中の SHA-256 と違う（書かない）: %s・字数 %d・結果の数 %d' % (sha, len(text), len(hits)))
    assert not os.path.exists(out), '既にある'
    with open(out, 'wb') as fh:
        fh.write(text.encode('utf-8'))
    print('extracted %s | chars %d | sha256 matches page | results %d' % (mark, len(text), len(hits)))


if __name__ == '__main__':
    main()
