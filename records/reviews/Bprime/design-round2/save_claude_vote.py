# -*- coding: utf-8 -*-
"""save_claude_vote.py v0（2026-09-29・B′ の設計の巡・一巡目・claude.ai の票を一度だけ残す・コーディネータ南無弥勒如来）。
枠の追記（2026-09-29 18:48:36）の「返事は、チャットの「写す」ボタンで写した直後に一度だけ読み、一字違わず `votes/claude-ai-1/`〜`votes/claude-ai-3/` に一度だけ書く」による。
使い方: python save_claude_vote.py <番号> <写しを受けたファイル> <チャットの URL> <画面の機種の欄の名> [<名前>]
写しは Windows のクリップボードを通るので改行が CRLF になる。CRLF を LF に戻す（戻した数を meta に記す）。ほかの字は変えない。
<名前> を付けると `votes/<名前>/` に書く（追い問いの返事など）。付けないときは `votes/claude-ai-<番号>/`。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NL, CRLF = chr(10), chr(13) + chr(10)


def sha16(b):
    return hashlib.sha256(b).hexdigest().upper()[:16]


def main():
    n, clip, url, label = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    name = sys.argv[5] if len(sys.argv) > 5 else 'claude-ai-%s' % n
    out = os.path.join(HERE, 'votes', name)
    assert not os.path.exists(out), '既にある（一度だけ）'
    raw = open(clip, 'rb').read()
    s = raw.decode('utf-8')
    n_crlf = s.count(CRLF)
    t = s.replace(CRLF, NL)
    assert chr(13) not in t, '孤立した CR が残る'
    os.makedirs(out)
    body = t.encode('utf-8')
    open(os.path.join(out, 'response.md'), 'wb').write(body)
    meta = {'chat': 'claude-ai-%s' % n, 'chat_url': url, 'model_label_on_screen': label,
            'model_label_note': '機種の欄の画面の要素の名（aria-label）を、コーディネータがページの中で読んで写した（模型が返した名ではない）',
            'copied_via': 'チャットの「写す」ボタン（data-testid action-bar-copy）→ Windows のクリップボード → 写した直後に一度だけ読んだ',
            'crlf_to_lf': n_crlf, 'clip_sha16': sha16(raw), 'response_sha16': sha16(body), 'response_chars': len(t),
            'first_line': t.split(NL, 1)[0], 'saved_jst': (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}
    json.dump(meta, open(os.path.join(out, 'meta.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == '__main__':
    main()
