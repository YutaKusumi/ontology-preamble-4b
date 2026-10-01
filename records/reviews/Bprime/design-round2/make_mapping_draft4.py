# -*- coding: utf-8 -*-
"""make_mapping_draft4.py v1（2026-09-29・v0 は採否の表の行を「|」で割ったので、欄の中の「N1|O-Ncold」「`<turn|>`」で R15・R17 を読み落とした。v1 は欄の区切りを「 | 」（前後に空白）で割る。v0 の出力は使う前に消して作り直した・B′ の設計の巡・二巡目の束のため・採否の表の行 R01〜R41 と草案4 の〔R〕の印の対応を機械で並べる・コーディネータ南無弥勒如来）。
草案4 の中の〔R..〕（「・」で並んだものを含む）を拾い、行ごとに、その印がある草案4 の行の番号と節の見出しを並べる。印の無い行は、その旨と採否の表の採否を並べる。出力 `mapping-draft4.md` は一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
D4 = os.path.normpath(os.path.join(HERE, '..', '..', 'design', 'design-Bprime-draft4.md'))
AD = os.path.normpath(os.path.join(HERE, '..', 'design-round1', 'adoption-design-round1.md'))
OUT = os.path.join(HERE, 'mapping-draft4.md')
NL = chr(10)


def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    L = open(D4, encoding='utf-8').read().split(NL)
    head = ''
    where = {}
    for i, l in enumerate(L, 1):
        if l.startswith('#'):
            head = l.lstrip('#').strip()
        for m in re.finditer(r'〔(R\d\d(?:・R\d\d)*)〕', l):
            for r in m.group(1).split('・'):
                where.setdefault(r, []).append((i, head))
    A = open(AD, encoding='utf-8').read().split(NL)
    rows = {}
    for l in A:
        if re.match(r'^\| R\d\d \| ', l):
            cells = [c.strip() for c in l.strip().strip('|').split(' | ')]
            assert len(cells) == 6, ('欄の数が 6 でない', cells[0], len(cells))
            rows[cells[0]] = (cells[1], cells[4])
    out = ['# 採否の表の行と草案4 の対応（機械で並べた・B′ の設計の巡・二巡目の束・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
           '- 器: `make_mapping_draft4.py`。草案4 `design-Bprime-draft4.md`（SHA16 %s）の中の〔R..〕の印と、採否の表 `adoption-design-round1.md`（SHA16 %s）の行を突き合わせた。' % (sha16(D4), sha16(AD)),
           '- 印は「その行の直しがここに入った」という起草者の印で、直しが正しいかの確かめではない（それは二巡目の検分の問い）。', '',
           '| 行 | 主題 | 採否 | 草案4 の印の所（行の番号・節） |', '|---|---|---|---|']
    none = []
    for r in sorted(rows):
        subj, dec = rows[r]
        w = where.get(r, [])
        cell = '・'.join('%d（%s）' % (i, h[:24]) for i, h in w) if w else '印なし'
        if not w:
            none.append(r)
        out.append('| %s | %s | %s | %s |' % (r, subj, dec.replace('|', '｜'), cell))
    extra = sorted(set(where) - set(rows))
    out += ['', '- 印の無い行: %s（採否の表の採否を見ること・登録者の裁定に上げた行は草案4 では【案】と D263 で入れた）。' % ('・'.join(none) if none else 'なし'),
            '- 採否の表に無い印: %s。' % ('・'.join(extra) if extra else 'なし'),
            '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(out))
    print('rows', len(rows), '| marked', len(rows) - len(none), '| unmarked', none, '| extra', extra)


if __name__ == '__main__':
    main()
