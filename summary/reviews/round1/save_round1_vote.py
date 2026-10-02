# -*- coding: utf-8 -*-
"""save_round1_vote.py v0（2026-10-02・中間総括の検分の一巡目の返事を一度だけ残す・B′ の結果の巡の `save_results_vote.py` v0 を写し、置き場〔この器の置き場の votes/〕と許しの記し方〔登録者の言葉 2026-10-02〕だけを替えた・claude.ai と Google AI Studio の両方に使う）。
返事の本文は、画面の「写す」ボタンが渡す文をページの中で差し替えて受け取り（クリップボードは使わない）、ページの中で SHA-256 を計算してから Blob で書き出した（ダウンロードの置き場に落ちる）。
この器は、落ちたファイルの SHA-256 がページの中の値と一致することを確かめてから、`votes/<名>/response.md` と `meta.json` に一度だけ書く（一致しなければ書かない）。
用法: python save_round1_vote.py <名（claude-ai-14・gemini-1 など）> <落ちたファイル> <ページの中の SHA-256> <チャットの URL> <画面の機種の欄の名> <依頼文のファイル名> [<一時の置き場>]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, shutil, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)


def main():
    name, got_path, page_sha, url, label, request = sys.argv[1:7]
    stash = sys.argv[7] if len(sys.argv) > 7 else None
    out = os.path.join(HERE, 'votes', name)
    assert not os.path.exists(out), '既にある（一度だけ）'
    b = open(got_path, 'rb').read()
    sha = hashlib.sha256(b).hexdigest().upper()
    want = page_sha.replace(' ', '').upper()
    if sha != want:
        raise SystemExit('ページの中の SHA-256 と違う（書かない）: %s' % sha)
    text = b.decode('utf-8')
    assert chr(13) not in text, 'CR がある（ページの中の文は LF のはず）'
    os.makedirs(out)
    with open(os.path.join(out, 'response.md'), 'wb') as fh:
        fh.write(b)
    meta = {'chat': name, 'chat_url': url, 'model_label_on_screen': label,
            'model_label_note': '機種の欄の画面の要素の名（aria-label）を、コーディネータがページの中で読んで写した（模型が返した名ではない）',
            'copied_via': os.environ.get('OP4B_VOTE_VIA') or 'チャットの「写す」ボタン（最後の返事のもの）が navigator.clipboard に渡す文を、ページの中で差し替えて受け取り、ページの中で SHA-256 を計算して Blob で書き出した（クリップボードは使わない）',
            'page_sha256': want, 'response_sha256': sha, 'response_bytes': len(b), 'response_chars': len(text), 'first_line': text.split(NL, 1)[0][:200],
            'request_file': request, 'request_sha16': hashlib.sha256(open(os.path.join(HERE, request), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16],
            'registrant_permission': '登録者の言葉（2026-10-02・中間総括の検分の一巡目まで進める・送りの記録 sending-log-round1.md）', 'saved_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(os.path.join(out, 'meta.json'), 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    if stash:
        os.makedirs(stash, exist_ok=True)
        shutil.move(got_path, os.path.join(stash, os.path.basename(got_path)))
    print('saved %s | sha256 matches page | bytes %d | chars %d | first line: %s' % (name, len(b), len(text), meta['first_line'][:80]))


if __name__ == '__main__':
    main()
