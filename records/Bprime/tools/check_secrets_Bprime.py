# -*- coding: utf-8 -*-
"""check_secrets_Bprime.py v0.1（2026-10-01・公開の前に、ファイルに鍵や認証の字が無いことを機械で確かめる・W22・コーディネータ南無弥勒如来）。
v0.1（最終検分の X02・裁定 D285）: 形の一覧を広げた（Google の認可のトークン ya29.・GitHub のトークン gh?_・JWT の形・Cookie の頭・api_key／access_token／secret／password などの名に
長い値を置いた形・HF_TOKEN の代入・秘密鍵の頭・AWS の鍵の形・Slack のトークンの形・メールの宛先の形〔noreply@anthropic.com は除く〕）。`--record` で確かめの記録（JSON）を書く。
前の版は `prev/check_secrets_Bprime-v0.py`。
二つの照らし: (一) 鍵の置き場（`OP4B_ENV_FILE`・既定は登録者の .env.local）の「名=値」の値（16 字以上）が、ファイルの中にそのまま無いこと（値は読むだけで、表示しない・どの名の値かも表示しない・記録にも書かない）。
(二) 鍵や認証の形の字が無いこと（当たった形の名だけを表示し、当たった字は表示しない・記録にも書かない）。
用法: python check_secrets_Bprime.py [--record <記録の JSON> --base <記録に書く置き場の基の置き場>] <ファイルか置き場> [...]（置き場は中のファイルをすべて見る）。当たりが一つでもあれば非零で終わる。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, hashlib, argparse, datetime
if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
VERSION = 'v0.1'
ENV_FILE = os.environ.get('OP4B_ENV_FILE', 'C:/Users/PC/Desktop/Ryokai-OS/.env.local')
PAT = {'xai': re.compile(r'xai-[A-Za-z0-9]{20,}'), 'sk': re.compile(r'\bsk-[A-Za-z0-9_\-]{20,}'), 'hf': re.compile(r'\bhf_[A-Za-z0-9]{20,}'),
       'google': re.compile(r'AIza[0-9A-Za-z_\-]{30,}'), 'ghp': re.compile(r'\bghp_[A-Za-z0-9]{20,}'), 'github_pat': re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
       'bearer': re.compile(r'Bearer\s+[A-Za-z0-9_\-\.]{20,}'), 'authorization': re.compile(r'Authorization["\']?\s*[:=]\s*["\']?[A-Za-z]*\s*[A-Za-z0-9_\-\.]{20,}'),
       # v0.1 で足した形
       'google_oauth': re.compile(r'ya29\.[0-9A-Za-z_\-]{20,}'), 'github_tokens': re.compile(r'\bgh[opusr]_[A-Za-z0-9]{20,}'),
       'jwt': re.compile(r'eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}'),
       'cookie': re.compile(r'(?i)\b(?:set-)?cookie["\']?\s*[:=]\s*["\']?[^\s"\']{20,}'),
       'key_value': re.compile(r'(?i)\b(?:api[_\-]?key|access[_\-]?token|refresh[_\-]?token|auth[_\-]?token|id[_\-]?token|client[_\-]?secret|secret|password|passwd)["\']?\s*[:=]\s*["\']?[A-Za-z0-9_\-\./\+=]{16,}'),
       'hf_token_env': re.compile(r'HF_TOKEN["\']?\s*[:=]\s*["\']?[A-Za-z0-9_]{10,}'), 'private_key': re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
       'aws': re.compile(r'\bAKIA[0-9A-Z]{16}\b'), 'slack': re.compile(r'\bxox[baprs]-[A-Za-z0-9\-]{10,}')}
EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
EMAIL_ALLOW = {'noreply@anthropic.com'}


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


def check_bytes(b, vals):
    """一つのファイルの中身の照らし: (鍵の値の当たりの数, 当たった形の名の並び)。"""
    t = b.decode('utf-8', errors='replace')
    hv = sum(1 for v in vals if v in t or v.encode('utf-8') in b)
    hp = [k for k, rx in PAT.items() if rx.search(t)]
    if any(m.group(0) not in EMAIL_ALLOW for m in EMAIL.finditer(t)):
        hp.append('email')
    return hv, hp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--record')
    ap.add_argument('--base')
    ap.add_argument('paths', nargs='+')
    a = ap.parse_args()
    vals = values()
    rows, bad = [], []
    for p in files(a.paths):
        b = open(p, 'rb').read()
        hv, hp = check_bytes(b, vals)
        lab = os.path.relpath(p, a.base).replace(os.sep, '/') if a.base else os.path.basename(p)
        rows.append({'path': lab, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest().upper(), 'hits': hv + len(hp)})
        if hv or hp:
            bad.append((p, hv, hp))
    print('ファイル %d・鍵の置き場の値 %d 個と照らした・形 %d（とメールの宛先の形）' % (len(rows), len(vals), len(PAT)))
    for p, hv, hp in bad:
        print('当たり: %s（鍵の値 %d・形 %s）' % (p, hv, hp))
    print('当たり %d' % len(bad))
    if a.record:
        assert not os.path.exists(a.record), ('記録は一度だけ', a.record)
        rec = {'kind': 'secret_check', 'tool': 'check_secrets_Bprime.py %s' % VERSION,
               'time_jst': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S'),
               'env_values_compared': len(vals), 'patterns': sorted(PAT) + ['email（noreply@anthropic.com は除く）'], 'files': rows, 'files_with_hits': len(bad),
               'note': '鍵の値と当たった字は、表示も記録もしない。',
               'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
        with open(a.record, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(rec, fh, ensure_ascii=False, indent=1)
        print('記録を書いた: %s' % a.record)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
