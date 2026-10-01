# -*- coding: utf-8 -*-
"""bprime_typo.py v0（2026-09-30・B′ の字の体裁〔裁定 D270〕・コーディネータ南無弥勒如来・非公開）。
決まった文の中の、器が埋める置き場〔…〕と、隣の字の間に半角の空白を一つ置く（ほかの決まった文の「升目ごとの試行 40」「SHA16 〔SHA〕」の形にそろえる・意味は変えない）。
触れるのは、器が数・識別子・決まった言い方で埋める置き場（`FILL` の名）だけ。ラベルを囲む〔〕（〔等方の外〕〔二つ目の札〕など）・草案の検分の印（〔T08〕〔K1〕など）・鍵の道の置き場（`cross_model.bl3_keys_list`）・字どおりの〔〕（`cross_model.fixed_sentence`）は、名が `FILL` に無いので触れない。
隣の字が空白・句読点・括弧・記号のときは空白を置かない。二度掛けても同じ（冪等）。
用法: import bprime_typo as TY; TY.sp(文)。python tools/bprime_typo.py --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import re, sys, io

VERSION = 'v0'
# 器が埋める置き場の名（正本 v3 の決まった文の置き場を数えて取った・`reading.summary`・`fixed_sentences`・`reading_rules[*].write`・`cross_model.headings_fixed.note`）
FILL = frozenset(['n', 'k', 'k0', 'a1', 'a2', 'm', 'b1', 'b2', 'j', 's1', 's2', 's3', 's4', 'n−k', 'j0',
                  '升目', '件数', '含む件数', '分母', '文字列の件数', '番号の件数', '差', '数', '60', '段',
                  '行', '側', '値', '割合', '外した対の数', '除いた対の数', '記録', 'SHA'])
NO_SPACE = frozenset(' \t\n　、。，．・：；（）「」『』【】［］｛｝〈〉《》｜' + ',.:;()[]{}/|`\'"')
PH = re.compile(r'〔([^〔〕]*)〕')


def sp(s):
    """埋める置き場と隣の字（空白・句読点・括弧・記号でない字）の間に半角の空白を一つ置く。"""
    r, last = '', 0
    for m in PH.finditer(s):
        if m.group(1) not in FILL:
            continue
        r += s[last:m.start()]
        if r and r[-1] not in NO_SPACE:
            r += ' '
        r += m.group(0)
        nxt = s[m.end()] if m.end() < len(s) else ''
        if nxt and nxt not in NO_SPACE:
            r += ' '
        last = m.end()
    return r + s[last:]


def tight(s):
    """埋める置き場のうち、隣に空白を置いていないものの並び（sp で変わる所）。"""
    out = []
    for m in PH.finditer(s):
        if m.group(1) not in FILL:
            continue
        b = s[m.start() - 1] if m.start() > 0 else ''
        a = s[m.end()] if m.end() < len(s) else ''
        if (b and b not in NO_SPACE) or (a and a not in NO_SPACE):
            out.append(m.group(0))
    return out


def _selftest():
    cases = [
        ('残った主の行〔n〕のうち〔k〕行で', '残った主の行 〔n〕 のうち 〔k〕 行で'),
        ('（v̂〔a1〕・Nk〔a2〕）', '（v̂ 〔a1〕・Nk 〔a2〕）'),
        ('区別できなかった〔n−k〕行のうち', '区別できなかった 〔n−k〕 行のうち'),
        ('は、〔升目〕で〔件数〕件だった', 'は、〔升目〕 で 〔件数〕 件だった'),
        ('（効き目の側: 〔側〕・等方の帰無の中央値〔値〕）', '（効き目の側: 〔側〕・等方の帰無の中央値 〔値〕）'),
        ('（〔記録〕・SHA16 〔SHA〕）', '（〔記録〕・SHA16 〔SHA〕）'),
        ('その行が〔等方の外〕で、〔二つ目の札〕が付かない', 'その行が〔等方の外〕で、〔二つ目の札〕が付かない'),
        ('同じ字）〔T08・T10〕', '同じ字）〔T08・T10〕'),
        ('rows.〔主の行〕.iso_outside', 'rows.〔主の行〕.iso_outside'),
        ('〔行〕の効き目は', '〔行〕 の効き目は'),
        ('〔数〕〔値〕', '〔数〕 〔値〕'),
        ('', ''),
    ]
    for a, b in cases:
        got = sp(a)
        assert got == b, (a, got, b)
        assert sp(got) == got, ('冪等でない', a)
        assert tight(got) == [], ('空白が足りない', got)
    assert tight('行〔n〕の') == ['〔n〕'] and tight('行 〔n〕 の') == []
    print('bprime_typo.py %s SELFTEST PASS（%d 例・冪等・ラベルと検分の印と鍵の道は触れない）' % (VERSION, len(cases)))


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    print(__doc__)
