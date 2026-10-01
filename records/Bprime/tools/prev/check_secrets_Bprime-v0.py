# -*- coding: utf-8 -*-
"""check_secrets_Bprime.py v0（2026-10-01・公開の前に、ファイルに鍵や認証の字が無いことを機械で確かめる・W22・コーディネータ南無弥勒如来）。
二つの照らし: (一) 鍵の置き場（`OP4B_ENV_FILE`・既定は登録者の .env.local）の「名=値」の値（16 字以上）が、ファイルの中にそのまま無いこと（値は読むだけで、表示しない・どの名の値かも表示しない）。
(二) 鍵の形の字（xai- / sk- / hf_ / AIza / ghp_ / github_pat_ / Bearer の後の長い字 / Authorization の行の長い字）が無いこと（当たった形の名だけを表示し、当たった字は表示しない）。
用法: python check_secrets_Bprime.py <ファイルか置き場> [...]（置き場は中のファイルをすべて見る）。当たりが一つでもあれば非零で終わる。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ENV_FILE = os.environ.get('OP4B_ENV_FILE', 'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
PAT = {'xai': re.compile(r'xai-[A-Za-z0-9]{20,}'), 'sk': re.compile(r'\bsk-[A-Za-z0-9_\-]{20,}'), 'hf': re.compile(r'\bhf_[A-Za-z0-9]{20,}'),
       'google': re.compile(r'AIza[0-9A-Za-z_\-]{30,}'), 'ghp': re.compile(r'\bghp_[A-Za-z0-9]{20,}'), 'github_pat': re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
       'bearer': re.compile(r'Bearer\s+[A-Za-z0-9_\-\.]{20,}'), 'authorization': re.compile(r'Authorization["\']?\s*[:=]\s*["\']?[A-Za-z]*\s*[A-Za-z0-9_\-\.]{20,}')}


def values():
    out = []
    for line in open(ENV_FILE, encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        v = line.split('=', 1)[1].strip().strip('"').strip("'")
        if len(v) >= 16:
            out.append(v)
    return out


def files(args):
    for a in args:
        if os.path.isdir(a):
            for dp, _, fns in os.walk(a):
                for fn in sorted(fns):
                    yield os.path.join(dp, fn)
        else:
            yield a


def main():
    vals = values()
    n_files, bad = 0, []
    for p in files(sys.argv[1:]):
        n_files += 1
        b = open(p, 'rb').read()
        t = b.decode('utf-8', errors='replace')
        hit_v = sum(1 for v in vals if v in t or v.encode('utf-8') in b)
        hit_p = [k for k, rx in PAT.items() if rx.search(t)]
        if hit_v or hit_p:
            bad.append((p, hit_v, hit_p))
    print('ファイル %d・鍵の置き場の値 %d 個と照らした' % (n_files, len(vals)))
    for p, hv, hp in bad:
        print('当たり: %s（鍵の値 %d・形 %s）' % (p, hv, hp))
    print('当たり %d' % len(bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
