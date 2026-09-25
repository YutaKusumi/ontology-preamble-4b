# -*- coding: utf-8 -*-
"""make_frozen_Bl3.py v2 —— B-lens 層三（Bl3）の凍結する本文（`design/design-Bl3-FROZEN.{src.md,md}`）を、草案3 の原稿から組む（B-lens の `make_frozen_Blens.py` の型・2026-09-25）。

草案3 の登録者の確認の後に、正本の文を直す裁定（D226〜D235）があったので、凍結の本文は草案3 の本文と次の三つの差だけを持つ（ほかの差があれば止める）:
  (一) 題名の印・凍結の一行・組み立ての記録の行（段階 B の器 `make_frozen_B.other_diffs` が許す差）。
  (二) 正本の鍵と設計事実から組まれる行のうち、正本と設計事実の直しで変わった行。同じ原稿を今の正本と設計事実で組み直した本文（組み直し）と草案3 の本文の差として機械で出し、
       記録（`records/Bl3/frozen-diff-Bl3.md`）に並べる。原稿の SHA16 が草案3 の組み立ての記録と、組み立ての器の SHA16 が草案3 の本文を最後に変えたコミットの器と同じことを
       確かめるので、この差は正本と設計事実だけから来る。
  (三) 原稿の文の直し（`LITERAL_FIXES`・裁定ごと・原稿の中でちょうど一度ずつ当たる）。組み直しと凍結の本文の差が、(一) の行と、直しの前後の文を含む行だけであることを確かめる。
凍結の一行は、題名と本行と、裁定で直した行（正本の鍵から組まれる行と、原稿の直し）だけを改めたことを書く（段階 B の型の一行の「題名と本行のみ改める」を、この登録の事実に合わせた）。
**本器は凍結そのものではない**——凍結の記帳は `tools/freeze_Bl3.py` が行う。
用法: python tools/make_frozen_Bl3.py --words "<登録者の逐語>" --commit <草案の原稿のコミット> --date "<日時（日本時間）>" [--force] ／ --check（組み直しと差の記録だけ）／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, difflib, hashlib, argparse, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import make_frozen_B as MF

VERSION = 'v2'          # v2（2026-09-25）: 組み直しの数の検査の記録の置き場を決まった言い方に置き換えてから差を取る・凍結の一行の裁定の範囲を D226〜D235 に
REBUILD_LINT_LABEL = '（組み直しの一時の置き場の数の検査の記録）'      # 組み直しの本文の「束縛」の行の記録の置き場（一時の置き場の道筋を凍結物に残さない）
NL = chr(10)
SRC = os.path.join(REPO, 'design', 'design-Bl3-draft3.src.md')
DRAFT = os.path.join(REPO, 'design', 'design-Bl3-draft3.md')
FSRC = os.path.join(REPO, 'design', 'design-Bl3-FROZEN.src.md')
FOUT = os.path.join(REPO, 'design', 'design-Bl3-FROZEN.md')
LINT = os.path.join(REPO, 'records', 'Bl3', 'numbers-lint-FROZEN-Bl3.md')
DIFFREC = os.path.join(REPO, 'records', 'Bl3', 'frozen-diff-Bl3.md')
BUILDER = os.path.join(HERE, 'build_draft_Bl3.py')
FROZEN_LINE = ('- **凍結**: %s（日本時間・登録者の言葉は逐語で「%s」・草案3 の原稿〔コミット %s 時点〕を逐語複製し、題名と本行と、裁定 D226〜D235 で正本の文を直した行'
               '〔正本の鍵から組まれる行と、原稿の直し〕だけを改める・直した行は `records/Bl3/frozen-diff-Bl3.md`・以後の変更は逸脱台帳に記帳する）')
# 原稿の文の直し（裁定・直す前・直した後）。直す前の文は原稿の中でちょうど一度だけ当たること。
LITERAL_FIXES = [
    ('D226', '加減のベクトルの足し方は段階 B の走行器のフック（`tools/run_stageB_local.py`）と同じ形にし、方向ごとに違うベクトルを一つのバッチで足す道は層三の器で新しく書く（§3.3）。',
     '加減のベクトルの足し方は段階 B の走行器のフック（`tools/run_stageB_local.py`）をそのまま呼ぶ（方向ごとに違うベクトルを一つのバッチで足す形は、このフックがもともと持つ・§3.3・裁定 D226）。'),
]
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')


def diffs(a_path, b_path):
    a = open(a_path, encoding='utf-8').read().split('\n')
    b = open(b_path, encoding='utf-8').read().split('\n')
    return [l for l in difflib.unified_diff(a, b, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]


def frozen_src(text, words, commit, date):
    """原稿の本文 → 凍結版の原稿の本文（題名に印・起草の行の次に凍結の一行・原稿の文の直し）。"""
    lines = text.split('\n')
    if not lines[0].startswith('# ') or MF.MARK in lines[0]:
        raise ValueError('題名の行が見つからないか、既に凍結版の題名になっている')
    head, sep, tail = lines[0].partition('）——')
    if not sep:
        raise ValueError('題名の形が違う（「）——」で分かれない）')
    lines[0] = head + '）' + MF.MARK + tail
    idx = [i for i, l in enumerate(lines) if l.startswith('- 起草:')]
    if not idx:
        raise ValueError('起草の行が見つからない')
    lines.insert(idx[0] + 1, FROZEN_LINE % (date, words, commit))
    out = '\n'.join(lines)
    for rid, old, new in LITERAL_FIXES:
        if out.count(old) != 1:
            raise ValueError('原稿の直しの前の文がちょうど一度だけ当たらない（%s・%d 回）' % (rid, out.count(old)))
        out = out.replace(old, new)
    return out


def build(src_path, out_path, label, lint_path):
    r = subprocess.run([sys.executable, BUILDER, '--src', src_path, '--out', out_path, '--label', label, '--lint-report', lint_path],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit('組み立てが止まった（%s）' % rel(src_path))
    return r


def draft3_record():
    """草案3 の組み立ての記録の原稿の SHA16（本文の行）と、草案3 の本文を最後に変えたコミットの組み立ての器の SHA16（git から読む・草案3 の数の検査の記録は器の SHA16 を持たないため）。"""
    t = open(DRAFT, encoding='utf-8').read()
    m = re.search(r'原稿 `design/design-Bl3-draft3\.src\.md` SHA16 ([0-9A-F]{16})', t)
    c = subprocess.run(['git', '-C', REPO, 'log', '-1', '--format=%H', '--', rel(DRAFT)], capture_output=True, text=True).stdout.strip()
    b = subprocess.run(['git', '-C', REPO, 'show', '%s:%s' % (c, rel(BUILDER))], capture_output=True).stdout if c else b''
    return (m.group(1) if m else None), (hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16] if b else None)


def rebuild_and_check(fsrc=None, fout=None):
    """組み直し（同じ原稿を今の正本と設計事実で）と草案3 の差（二）・組み直しと凍結の本文の差の残り（一と三の外）を返す。"""
    src_sha, builder_sha = draft3_record()
    res = {'src_sha16_record': src_sha, 'src_sha16_now': sha16f(SRC), 'builder_sha16_record': builder_sha, 'builder_sha16_now': sha16f(BUILDER)}
    bad = []
    if src_sha != res['src_sha16_now']:
        bad.append('草案3 の原稿の SHA16 が草案3 の組み立ての記録と違う')
    if builder_sha is None:
        bad.append('草案3 の本文を最後に変えたコミットの組み立ての器を git から読めない')
    elif builder_sha != res['builder_sha16_now']:
        bad.append('組み立ての器の SHA16 が、草案3 の本文を最後に変えたコミットの器と違う')
    with tempfile.TemporaryDirectory() as td:
        rb = os.path.join(td, 'rebuilt.md')
        build(SRC, rb, '草案3', os.path.join(td, 'lint.md'))
        t_rb, tmp_lint = open(rb, encoding='utf-8').read(), rel(os.path.join(td, 'lint.md'))
        if t_rb.count(tmp_lint) != 1:
            raise SystemExit('組み直しの本文に、数の検査の記録の置き場がちょうど一度だけ現れない（止める）')
        open(rb, 'w', encoding='utf-8', newline='\n').write(t_rb.replace(tmp_lint, REBUILD_LINT_LABEL))
        canon_driven = diffs(DRAFT, rb)
        residual = None
        if fout and os.path.exists(fout):
            d = MF.other_diffs(diffs(rb, fout))
            olds = [o for _, o, _ in LITERAL_FIXES]
            news = [n for _, _, n in LITERAL_FIXES]
            residual = [l for l in d if not ((l.startswith('-') and any(o in l for o in olds)) or (l.startswith('+') and any(n in l for n in news)))]
            hit_old = sum(1 for l in d if l.startswith('-') and any(o in l for o in olds))
            hit_new = sum(1 for l in d if l.startswith('+') and any(n in l for n in news))
            if residual:
                bad.append('凍結の本文と組み直しに、許す差でない差がある（%d 行）' % len(residual))
            if hit_old != len(LITERAL_FIXES) or hit_new != len(LITERAL_FIXES):
                bad.append('原稿の直しの行が凍結の本文に現れない')
    res.update({'canon_driven': canon_driven, 'residual': residual})
    return res, bad


def write_diffrec(res):
    L = ['# B-lens 層三の凍結の本文と草案3 の差の記録（機械生成・`tools/make_frozen_Bl3.py` %s）' % VERSION, '',
         '- 草案3 の原稿 `%s` SHA16 %s（草案3 の組み立ての記録 %s）・組み立ての器 `%s` SHA16 %s（草案3 の本文を最後に変えたコミットの器 %s）。' % (
             rel(SRC), res['src_sha16_now'], res['src_sha16_record'], rel(BUILDER), res['builder_sha16_now'], res['builder_sha16_record']),
         '- (二) 正本の鍵と設計事実から組まれる行の差（同じ原稿を今の正本と設計事実で組み直した本文と、草案3 の本文の差・行の頭の - が草案3・+ が組み直し）:', '', '```diff'] + \
        res['canon_driven'] + ['```', '', '- (三) 原稿の文の直し（裁定・直す前 → 直した後）:', ''] + \
        ['  - %s: 「%s」→「%s」' % (rid, o, n) for rid, o, n in LITERAL_FIXES] + \
        ['', '- 組み直しと凍結の本文の差の残り（(一) と (三) の外）: %s' % ('無し' if res.get('residual') == [] else ('確かめていない' if res.get('residual') is None else '%d 行' % len(res['residual']))), '',
         '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(DIFFREC, 'w', encoding='utf-8', newline=NL).write(NL.join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--words')
    ap.add_argument('--commit')
    ap.add_argument('--date')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        src = open(SRC, encoding='utf-8').read()
        out = frozen_src(src, '（自己検査）', 'deadbee', '2026-09-26 10:00')
        lines = out.split('\n')
        assert MF.MARK in lines[0] and lines[3].startswith('- **凍結**:'), lines[:4]
        d = [l for l in difflib.unified_diff(src.split('\n'), lines, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]
        rest = MF.other_diffs(d)
        assert len(rest) == 2 * len(LITERAL_FIXES) and all(any(x in l for _, o, n in LITERAL_FIXES for x in (o, n)) for l in rest), rest
        try:
            frozen_src(src.replace(LITERAL_FIXES[0][1], ''), 'x', 'y', 'z')
            raise AssertionError('直しの前の文が無い原稿を通した')
        except ValueError:
            pass
        print('[make_frozen_Bl3] 自己検査 OK（題名の印・凍結の一行・原稿の直しの %d 行だけが原稿の差）' % len(LITERAL_FIXES))
        return
    if a.check:
        res, bad = rebuild_and_check(FSRC, FOUT)
        write_diffrec(res)
        print('[make_frozen_Bl3] 組み直しの差 %d 行（記録 %s）・凍結の本文の残りの差 %s・外れ %s' % (len(res['canon_driven']), rel(DIFFREC), res['residual'] if res['residual'] is None else len(res['residual']), bad or '無し'))
        if bad:
            raise SystemExit('確かめが外れた: %s' % bad)
        return
    if not (a.words and a.commit and a.date):
        raise SystemExit('--words・--commit・--date が要る')
    for p in (FSRC, FOUT):
        if os.path.exists(p) and not a.force:
            raise SystemExit('既にある（--force で上書き）: %s' % rel(p))
    open(FSRC, 'w', encoding='utf-8', newline='\n').write(frozen_src(open(SRC, encoding='utf-8').read(), a.words, a.commit, a.date))
    build(FSRC, FOUT, '凍結版', LINT)
    res, bad = rebuild_and_check(FSRC, FOUT)
    write_diffrec(res)
    if bad:
        raise SystemExit('凍結の本文の確かめが外れた: %s' % bad)
    print('[make_frozen_Bl3] %s・%s・%s（正本と設計事実から来る差 %d 行・原稿の直し %d・ほかの差 無し）' % (rel(FSRC), rel(FOUT), rel(DIFFREC), len(res['canon_driven']), len(LITERAL_FIXES)))


if __name__ == '__main__':
    main()
