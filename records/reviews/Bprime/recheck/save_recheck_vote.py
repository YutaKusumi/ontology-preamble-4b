# -*- coding: utf-8 -*-
"""save_recheck_vote.py v0（2026-10-01・器の実装の検分の `../impl/save_impl_vote.py` v0.1 を写し、置き場〔この器の置き場の votes/〕と裁定の番号〔D279〕だけを替えた・直しの確かめの巡の claude.ai の返事を一度だけ残す）。以下は写した元の説明: save_impl_vote.py v0.1（2026-09-30・v0.1: 環境変数 OP4B_VOTE_VIA で写しの道の説明を替えられる〔ダウンロードが止められて、本文の読み取りと会話の記録からの機械の切り出しで取ったとき〕・B′ の器の実装の検分の claude.ai の返事を一度だけ残す・裁定 D272・コーディネータ南無弥勒如来）。
返事の本文は、チャットのページの中で「写す」ボタンが渡す文を差し替えて受け取り（クリップボードは使わない・登録者の操作と共有のため）、
ページの中で SHA-256 を計算してから Blob で書き出した（ダウンロードの置き場に落ちる）。この器は、落ちたファイルの SHA-256 がページの中の値と一致することを確かめてから、
`votes/<名>/response.md` と `meta.json` に一度だけ書き、落ちたファイルを一時の置き場へ移す（一致しなければ書かない）。
用法: python save_impl_vote.py <名（claude-ai-10 など）> <落ちたファイル> <ページの中の SHA-256> <チャットの URL> <画面の機種の欄の名> <依頼文のファイル名> [<一時の置き場>]
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
            'registrant_permission': 'D279', 'saved_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(os.path.join(out, 'meta.json'), 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    if stash:
        os.makedirs(stash, exist_ok=True)
        shutil.move(got_path, os.path.join(stash, os.path.basename(got_path)))
    print('saved %s | sha256 matches page | bytes %d | chars %d | first line: %s' % (name, len(b), len(text), meta['first_line'][:80]))


if __name__ == '__main__':
    main()
