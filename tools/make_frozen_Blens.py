# -*- coding: utf-8 -*-
"""make_frozen_Blens.py v1 —— B-lens の凍結する本文（`design/design-Blens-FROZEN.{src.md,md}`）を、草案3 の原稿から**題名と一行だけ**変えて組む（段階 A・B と同じ型・2026-09-23）。

やること:
  1. 草案の原稿（既定 `design/design-Blens-draft3.src.md`）を読み、題名に `——凍結版——` を差し込み、起草の行の次に凍結の一行を足す（段階 B の器 `make_frozen_B.frozen_src` をそのまま使う）。
     凍結の一行には、凍結の日時・登録者の逐語・草案の原稿のコミットを置き、以後の変更は逸脱台帳に記帳すると書く。
  2. `tools/build_draft_Blens.py` で組み立てる（数はキー参照のまま置換され、数の検査器が走る）。
  3. 組み上がった本文と草案3 の本文の差が、題名の行・凍結の行・組み立ての記録の行だけであることを機械で確かめる（`make_frozen_B.other_diffs`）。ほかに差があれば非零で終わる。
**本器は凍結そのものではない**——凍結の記帳は `tools/freeze_Blens.py` が行う。
用法: python tools/make_frozen_Blens.py --words "<登録者の逐語>" --commit <草案の原稿のコミット> --date "<日時（日本時間）>" [--force] ／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, difflib, argparse, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import make_frozen_B as MF

VERSION = 'v1'
SRC = os.path.join(REPO, 'design', 'design-Blens-draft3.src.md')
DRAFT = os.path.join(REPO, 'design', 'design-Blens-draft3.md')
FSRC = os.path.join(REPO, 'design', 'design-Blens-FROZEN.src.md')
FOUT = os.path.join(REPO, 'design', 'design-Blens-FROZEN.md')
LINT = os.path.join(REPO, 'records', 'Blens', 'numbers-lint-FROZEN-Blens.md')


def diffs(a_path, b_path):
    a = open(a_path, encoding='utf-8').read().split('\n')
    b = open(b_path, encoding='utf-8').read().split('\n')
    return [l for l in difflib.unified_diff(a, b, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--words')
    ap.add_argument('--commit')
    ap.add_argument('--date')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        src = open(SRC, encoding='utf-8').read()
        out = MF.frozen_src(src, '（自己検査）', 'deadbee', '2026-09-24 10:00')
        lines = out.split('\n')
        assert MF.MARK in lines[0] and lines[3].startswith('- **凍結**:'), lines[:4]
        d = [l for l in difflib.unified_diff(src.split('\n'), lines, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]
        assert len(d) == 3 and MF.other_diffs(d) == [], d
        print('[make_frozen_Blens] 自己検査 OK（題名の印と凍結の一行だけが差）')
        return
    if not (a.words and a.commit and a.date):
        raise SystemExit('--words・--commit・--date が要る')
    for p in (FSRC, FOUT):
        if os.path.exists(p) and not a.force:
            raise SystemExit('既にある（--force で上書き）: %s' % os.path.relpath(p, REPO))
    src = open(SRC, encoding='utf-8').read()
    open(FSRC, 'w', encoding='utf-8', newline='\n').write(MF.frozen_src(src, a.words, a.commit, a.date))
    r = subprocess.run([sys.executable, os.path.join(HERE, 'build_draft_Blens.py'), '--src', FSRC, '--out', FOUT, '--label', '凍結版', '--lint-report', LINT],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit('組み立てが止まった')
    od = MF.other_diffs(diffs(DRAFT, FOUT))
    if od:
        raise SystemExit('凍結版の本文と草案3 の本文に、許す差でない差がある: %s' % od[:5])
    print('[make_frozen_Blens] %s・%s（草案3 との差は題名・凍結の行・組み立ての記録だけ）' % (os.path.relpath(FSRC, REPO), os.path.relpath(FOUT, REPO)))


if __name__ == '__main__':
    main()
