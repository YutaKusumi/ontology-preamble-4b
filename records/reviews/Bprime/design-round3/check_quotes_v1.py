# -*- coding: utf-8 -*-
"""check_quotes.py v1（2026-09-29・v0 は「引用」の語だけで正式の引用を見分け、「該当の行」と書いた票を 0 と数えた。v1 は「引用」か「該当の行」で見分け、出力は quote-check-v1/ に書く・B′ の設計の巡・一巡目・票の中の「」の引用の機械の確かめ・コーディネータ南無弥勒如来）。
枠（`00-frame-design-round1.md`）の「返事の中の「」の引用は、草案6 の文に一字違わずあるかを機械で確かめ、合わない引用はその印を付ける（指摘を捨てる理由にはしない）」による。
使い方: python check_quotes.py <票の名>（例: grok-4.7）。`votes/<票の名>/response.md` を読み、`quote-check/<票の名>.md` に一度だけ書く。
分け方（上から順に当てる）:
  A＝草案6 に一字違わずある／B＝草案6 に、太字の印（**）と逆引用符（`）を両側から除けばある／
  C＝草案6 には無いが、束のほかのファイルに一字違わずある（どのファイルか）／D＝どこにも一字違わずは無い（草案6 の中の最も長い一致を添える）。
「」の入れ子は外側の一組を一つの引用として数える。引用の行に「引用」の語が先にあるものを「正式の引用」と印す。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, hashlib, datetime, difflib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'kit')
DRAFT = os.path.join(KIT, 'design-Bprime-draft6.md')
DRAFT_SHA16 = '4C16FBCAC272383C'
OUTDIR = os.path.join(HERE, 'quote-check-v1')
NL = chr(10)
LQ, RQ = chr(0x300C), chr(0x300D)   # 「 」


def sha16(b):
    return hashlib.sha256(b).hexdigest().upper()[:16]


def extract(text):
    out, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == LQ:
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == RQ and depth > 0:
            depth -= 1
            if depth == 0:
                out.append((start, text[start:i]))
    return out, depth


def strip_marks(s):
    return s.replace('**', '').replace('`', '')


def near(q, draft):
    sm = difflib.SequenceMatcher(None, draft, q, autojunk=False)
    m = sm.find_longest_match(0, len(draft), 0, len(q))
    line = draft.count(NL, 0, m.a) + 1
    return m.size, line


def main():
    name = sys.argv[1]
    src = os.path.join(HERE, 'votes', name, 'response.md')
    out = os.path.join(OUTDIR, name + '.md')
    assert not os.path.exists(out), '既にある（一度だけ）'
    draft_b = open(DRAFT, 'rb').read()
    assert sha16(draft_b) == DRAFT_SHA16, '草案6 の SHA が合わない'
    draft = draft_b.decode('utf-8')
    draft_s = strip_marks(draft)
    others = {}
    for root, _, files in os.walk(KIT):
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, KIT).replace(os.sep, '/')
            if rel in ('MANIFEST.sha256', 'design-Bprime-draft6.md'):
                continue
            others[rel] = open(p, 'rb').read().decode('utf-8')
    resp_b = open(src, 'rb').read()
    resp = resp_b.decode('utf-8')
    quotes, open_depth = extract(resp)
    rows, counts = [], {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    fcounts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for k, (pos, q) in enumerate(quotes, 1):
        line = resp.count(NL, 0, pos) + 1
        line_start = resp.rfind(NL, 0, pos) + 1
        formal = ('引用' in resp[line_start:pos]) or ('該当の行' in resp[line_start:pos])
        if q in draft:
            cls, where = 'A', '草案6 の %d 行目' % (draft.count(NL, 0, draft.find(q)) + 1)
        elif strip_marks(q) in draft_s:
            cls, where = 'B', '印を除いた草案6'
        else:
            hit = [rel for rel, t in sorted(others.items()) if q in t]
            if hit:
                cls, where = 'C', '・'.join(hit)
            else:
                size, nline = near(q, draft)
                cls, where = 'D', '草案6 の中の最も長い一致 %d 字／%d 字（草案6 の %d 行目から）' % (size, len(q), nline)
        counts[cls] += 1
        if formal:
            fcounts[cls] += 1
        show = q.replace(NL, '⏎')
        if len(show) > 80:
            show = show[:40] + ' … ' + show[-30:]
        rows.append('| %d | %d | %s | %d | %s | %s | %s |' % (k, line, '正式' if formal else '', len(q), cls, where, show.replace('|', '｜')))
    lines = [
        '# 引用の機械の確かめ（%s・B′ の設計の巡・一巡目・非公開）' % name,
        '',
        '- 器: `check_quotes.py` v1。票: `votes/%s/response.md`（SHA16 %s・%d 字）。草案6: `kit/design-Bprime-draft2.md`（SHA16 %s）。' % (name, sha16(resp_b), len(resp), DRAFT_SHA16),
        '- 「」の組の数: %d（閉じていない「 の残り: %d）。うち「引用」か「該当の行」の語が同じ行の前にある正式の引用: %d。' % (len(quotes), open_depth, sum(fcounts.values())),
        '- 分け方の数（全部）: A %d・B %d・C %d・D %d。正式の引用だけ: A %d・B %d・C %d・D %d。' % (counts['A'], counts['B'], counts['C'], counts['D'], fcounts['A'], fcounts['B'], fcounts['C'], fcounts['D']),
        '- A＝草案6 に一字違わずある／B＝太字の印と逆引用符を除けばある／C＝束のほかのファイルに一字違わずある／D＝どこにも一字違わずは無い。合わない引用は印を付けるだけで、指摘を捨てる理由にはしない（枠）。',
        '- 引用の本文は長いものを頭 40 字と尻 30 字に切って見せる（改行は ⏎）。',
        '',
        '| # | 票の行 | 正式 | 字数 | 分け | どこに | 引用 |',
        '|---|---|---|---|---|---|---|',
    ] + rows + [
        '',
        '- 書いた時刻: %s（日本時間）。' % (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'),
        '',
        '## この確かめが確認していないこと',
        '',
        '- 引用が指摘の中身を正しく支えているか（字が合うことと、読みが正しいことは別）。',
        '- D の引用が、言い換え・要約・読み違いのどれか（人が読んで決める）。',
        '- 「」が引用ではなく語の名として使われたもの（A になっても引用の検査ではない）。',
        '',
        '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。',
        '',
    ]
    os.makedirs(OUTDIR, exist_ok=True)
    open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(lines))
    print(NL.join(lines[:6]))
    for r in rows:
        if '| D |' in r or '| C |' in r or '| B |' in r:
            print(r)


if __name__ == '__main__':
    main()
