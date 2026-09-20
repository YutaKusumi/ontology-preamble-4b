# -*- coding: utf-8 -*-
"""make_frozen_B.py v1 —— 凍結する本文（`design/design-stageB-FROZEN.{src.md,md}`）を、草案の原稿から**題名と一行だけ**変えて組む（段階 A と同じ型・2026-09-20）。

なぜ: 段階 A は凍結の日に `design-stageA-FROZEN.src.md` を作り、草案の原稿との差は**題名に「——凍結版——」を足し、凍結の一行を加えただけ**（六行）だった。
      段階 B も同じ型にする。凍結の一行には、日付・**登録者の逐語**・コミットの短い名を置き、以後の変更は逸脱台帳に記帳すると書く。
      この段取りは、凍結の前の見直しの (四)（`records/B/pre-freeze-review-2026-09-20.md`）で決まった。

やること:
  1. 草案の原稿（既定 `design/design-stageB-draft13.src.md`）を読み、題名に `——凍結版——` を差し込み、起草の行の次に凍結の一行を足す（`frozen_src`）。
  2. `tools/build_draftB.py` で組み立てる（数はキー参照のまま置換され、採否表の引用も照らされる）。
  3. 組み上がった本文と草案の本文の差が**題名の行・凍結の行・組み立ての記録の行だけ**であることを機械で確かめ、ほかに差があれば非零で終わる。
**本器は凍結そのものではない**——凍結の記帳は `tools/freeze_B.py` が行う。本器は凍結する本文を作るだけである。
用法: python tools/make_frozen_B.py --words "<登録者の逐語>" --commit <短いコミット名> [--date 2026-09-20] [--force] ／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, difflib, argparse, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
PY = sys.executable
MARK = '——凍結版——'
FROZEN_LINE = ('- **凍結**: %s（日本時間・登録者の言葉は逐語で「%s」・草案の原稿〔コミット %s 時点〕を逐語複製し、'
               '**題名と本行のみ改める**・以後の変更は逸脱台帳に記帳する）')


def frozen_src(text, words, commit, date):
    """原稿の本文 → 凍結版の原稿の本文（題名に印・起草の行の次に凍結の一行）。ほかは一字も変えない。"""
    lines = text.split('\n')
    if not lines[0].startswith('# '):
        raise ValueError('題名の行が見つからない')
    if MARK in lines[0]:
        raise ValueError('既に凍結版の題名になっている')
    head, sep, tail = lines[0].partition('）——')
    if not sep:
        raise ValueError('題名の形が段階 A と違う（「）——」で分かれない）')
    lines[0] = head + '）' + MARK + tail          # 段階 A と同じ形（「）——凍結版——<説明>」）
    idx = [i for i, l in enumerate(lines) if l.startswith('- 起草:')]
    if not idx:
        raise ValueError('起草の行が見つからない')
    lines.insert(idx[0] + 1, FROZEN_LINE % (date, words, commit))
    return '\n'.join(lines)


def _selftest():
    src = ('# 段階 X 設計草案1（…・凍結前）——問い\n'
           '\n'
           '- 起草: だれか／登録者: だれか\n'
           '- 状態: 草案\n'
           '\n'
           '本文。\n')
    out = frozen_src(src, '凍結をしてください。', 'abc1234', '2026-09-20')
    lines = out.split('\n')
    assert lines[0] == '# 段階 X 設計草案1（…・凍結前）——凍結版——問い', lines[0]
    assert lines[2].startswith('- 起草:') and lines[3].startswith('- **凍結**: 2026-09-20'), lines[2:4]
    assert '凍結をしてください。' in lines[3] and 'abc1234' in lines[3], lines[3]
    # ほかの行は一字も変えない（差は題名の一行と、足した一行だけ）
    a, b = src.split('\n'), out.split('\n')
    d = [l for l in difflib.unified_diff(a, b, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]
    assert len(d) == 3 and sum(1 for l in d if l.startswith('+')) == 2, d
    # 二度掛けは拒む・題名の形が違えば拒む
    for bad, why in ((out, '二度掛け'), ('# 題名だけ\n- 起草: x\n', '題名の形')):
        try:
            frozen_src(bad, 'x', 'y', 'z')
        except ValueError:
            pass
        else:
            raise AssertionError('拒まなかった: %s' % why)
    # 実物の草案の原稿でも、題名の形と起草の行がある
    real = open(os.path.join(REPO, 'design', 'design-stageB-draft13.src.md'), encoding='utf-8').read()
    r = frozen_src(real, '（自己検査）', 'deadbee', '2026-09-20')
    assert MARK in r.split('\n')[0] and r.split('\n')[3].startswith('- **凍結**:'), r.split('\n')[:4]
    print('[make_frozen_B selftest] 題名の印・凍結の行の位置と中身・ほかの行を変えないこと・二度掛けと題名の形の拒み・'
          '実物の草案の原稿での組み立て —— すべて通った')


def build(src_src, out_src, out_md, words, commit, date, label, lint_report, draft_md, force=False):
    """原稿 → 凍結版の原稿 → 凍結版の本文。戻りは (差の行, 題名と凍結の行以外の差, 組み立ての出力)。"""
    if os.path.exists(out_src) and not force:
        sys.exit('既にある（--force で置き換え）: %s' % out_src)
    open(out_src, 'w', encoding='utf-8', newline='\n').write(frozen_src(open(src_src, encoding='utf-8').read(), words, commit, date))
    r = subprocess.run([PY, os.path.join(REPO, 'tools', 'build_draftB.py'), '--kind', 'draft', '--src', out_src,
                        '--out', out_md, '--label', label, '--lint-report', lint_report],
                       capture_output=True, text=True, encoding='utf-8', cwd=REPO)
    out = (r.stdout or '') + (r.stderr or '')
    if r.returncode != 0:
        sys.exit('組み立てが落ちた（終了コード %d）:\n%s' % (r.returncode, out[-1500:]))
    a = open(draft_md, encoding='utf-8').read().split('\n')
    b = open(out_md, encoding='utf-8').read().split('\n')
    diff = [l for l in difflib.unified_diff(a, b, n=0) if l[:1] in '+-' and not l.startswith(('---', '+++'))]
    # 題名の行・凍結の行・組み立ての記録の行（原稿の名と SHA16・検査の記録の置き場）だけが変わってよい
    bad = [l for l in diff if not (MARK in l or '**凍結**:' in l or 'FROZEN' in l or '組み立ての記録' in l
                                   or ('原稿' in l and 'SHA16' in l))]
    return diff, bad, out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--words', help='登録者の凍結の言葉（逐語）')
    ap.add_argument('--commit', help='草案の原稿のコミットの短い名')
    ap.add_argument('--date', default=None)
    ap.add_argument('--src', default=os.path.join(REPO, 'design', 'design-stageB-draft13.src.md'))
    ap.add_argument('--draft', default=os.path.join(REPO, 'design', 'design-stageB-draft13.md'))
    ap.add_argument('--label', default='凍結版B')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    if not (a.words and a.commit and a.date):
        sys.exit('--words（登録者の逐語）・--commit・--date が要る（凍結の一行に置く）')
    out_src = os.path.join(REPO, 'design', 'design-stageB-FROZEN.src.md')
    out_md = os.path.join(REPO, 'design', 'design-stageB-FROZEN.md')
    lint = os.path.join(REPO, 'records', 'B', 'numbers-lint-FROZEN-B.md')
    diff, bad, out = build(a.src, out_src, out_md, a.words, a.commit, a.date, a.label, lint, a.draft, a.force)
    print((out.strip().split('\n')[-1] if out.strip() else ''))
    print('[make_frozen_B] %s / %s を書いた。草案との差 %d 行。' % (os.path.relpath(out_src, REPO), os.path.relpath(out_md, REPO), len(diff)))
    for l in diff[:12]:
        print('   ', l[:120])
    if bad:
        print('**題名と凍結の行のほかに差がある（確かめること）**: %d 行' % len(bad))
        for l in bad[:8]:
            print('   ', l[:160])
        sys.exit(2)
    sys.exit(0)
