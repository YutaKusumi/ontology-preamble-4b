# -*- coding: utf-8 -*-
"""save_probe_reply.py v0（2026-09-30・B′ の器の実装の検分の前の小さな試しの返事を一度だけ残す・コーディネータ南無弥勒如来）。
返事の本文は、チャットのページの中で「写す」ボタンが渡す文を差し替えて受け取った（クリップボードは使わない・登録者の操作と共有のため）。
ページの中で計算した SHA-256（区切りを入れて受け取った値）と、ここに書いたファイルの SHA-256 が一致することを確かめる（一致しなければ書かない）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'reply-probe-1')
PAGE_SHA256 = '6EFA52B7 77A8F7B4 9AAEC6AA CA3D5B37 B48AFDCC 2DD252A5 874825DA EDBDD57A'.replace(' ', '')
TEXT = json.loads(r'''"```\n{\n \"python\": \"3.12.3\",\n \"platform\": \"Linux-6.18.44-fc-v50-x86_64-with-glibc2.39\",\n \"cpu_count\": 1,\n \"disk_free_gb\": 10.0,\n \"mem_total\": \"MemTotal:        4095316 kB\",\n \"numpy\": \"2.4.4\",\n \"scipy\": \"1.17.1\",\n \"torch\": \"無い（ModuleNotFoundError）\",\n \"transformers\": \"無い（ModuleNotFoundError）\",\n \"tokenizers\": \"無い（ModuleNotFoundError）\",\n \"jinja2\": \"3.1.6\",\n \"safetensors\": \"無い（ModuleNotFoundError）\",\n \"zip_roundtrip\": true,\n \"pip_download_transformers_5_16_1\": {\n  \"rc\": 0,\n  \"seconds\": 1.1,\n  \"tail\": \"\"\n },\n \"pip_download_numpy_2_4_6\": {\n  \"rc\": 0,\n  \"tail\": \"\"\n }\n}\n```"''')


def main():
    b = TEXT.encode('utf-8')
    got = hashlib.sha256(b).hexdigest().upper()
    if got != PAGE_SHA256:
        raise SystemExit('ページの中の SHA-256 と違う（書かない）: %s' % got)
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    os.makedirs(OUT)
    with open(os.path.join(OUT, 'response.md'), 'wb') as fh:
        fh.write(b)
    probe = os.path.join(HERE, 'probe_env_Bprime.py')
    meta = {'chat': 'probe-1', 'chat_url': 'https://claude.ai/chat/e82cb92b-b7fb-4a07-8069-38aa2efe187d', 'model_label_on_screen': 'モデル: Opus 5.5 超高',
            'model_label_note': '機種の欄の画面の要素の名（aria-label）を、コーディネータがページの中で読んで写した（模型が返した名ではない）',
            'copied_via': 'チャットの「写す」ボタン（data-testid action-bar-copy）が navigator.clipboard.write に渡す文を、ページの中で差し替えて受け取った（クリップボードは使わない）',
            'page_sha256': PAGE_SHA256, 'response_sha256': got, 'response_bytes': len(b), 'response_chars': len(TEXT),
            'probe_script_sha16': hashlib.sha256(open(probe, 'rb').read()).hexdigest().upper()[:16],
            'request_chars': 235, 'registrant_permission': 'D271（器の実装の検分の前の小さな試し・推しのとおり）',
            'saved_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
            'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    with open(os.path.join(OUT, 'meta.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('saved reply-probe-1 | sha256 matches page | bytes %d | chars %d' % (len(b), len(TEXT)))


if __name__ == '__main__':
    main()
