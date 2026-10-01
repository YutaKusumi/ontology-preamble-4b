# -*- coding: utf-8 -*-
"""extract_round1_verdicts.py v0（2026-09-29・B′ の設計の巡・二巡目の束のため・一巡目の四票の総評と「最も重い弱点」を逐語で抜き出す・コーディネータ南無弥勒如来）。
層三の設計の巡の二巡目の束（総括の抜き書き）の型。見出し「総評」「Q9」の節を、次の同じ深さか浅い見出しの前まで、票のファイルから一字違わず切り出す。出力 `round1-verdicts-extract.md` は一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.normpath(os.path.join(HERE, '..', 'design-round1', 'votes'))
OUT = os.path.join(HERE, 'round1-verdicts-extract.md')
NL = chr(10)
NAMES = [('grok-4.7', '系統外・xAI'), ('claude-ai-1', '系統内・Anthropic（三つで一票）'), ('claude-ai-2', '系統内・Anthropic（三つで一票）'), ('claude-ai-3', '系統内・Anthropic（三つで一票）')]


def sections(text, key):
    L = text.split(NL)
    out = []
    for i, l in enumerate(L):
        m = re.match(r'^(#+)\s*(.*)$', l)
        if m and key in m.group(2):
            depth = len(m.group(1))
            j = i + 1
            while j < len(L):
                m2 = re.match(r'^(#+)\s', L[j])
                if m2 and len(m2.group(1)) <= depth:
                    break
                j += 1
            out.append(NL.join(L[i:j]).rstrip())
    return out


def main():
    assert not os.path.exists(OUT), '既にある（一度だけ）'
    out = ['# 一巡目の四票の総評と「最も重い弱点」の抜き書き（逐語・器 `extract_round1_verdicts.py`・B′ の設計の巡・二巡目の束・2026-09-29）', '',
           '- 票の全文はこの束に入れていない（層三の設計の巡の二巡目の束と同じ型）。各々の指摘は採否の表 `adoption-design-round1.md` の行に入っている。追い問いの答えの要点も採否の表の「追い問いで分かったこと」にある。',
           '- 抜き書きは票のファイルから一字違わず切り出した。見出しの深さは票のまま。', '']
    for name, lin in NAMES:
        p = os.path.join(V, name, 'response.md')
        b = open(p, 'rb').read()
        t = b.decode('utf-8')
        out.append('## %s（%s・`votes/%s/response.md`・SHA16 %s）' % (name, lin, name, hashlib.sha256(b).hexdigest().upper()[:16]))
        out.append('')
        got = sections(t, 'Q9') + sections(t, '総評')
        assert got, ('節が見つからない', name)
        for s in got:
            out.append('```text')
            out.append(s)
            out.append('```')
            out.append('')
    out += ['## この抜き書きが確認していないこと', '', '- 総評と「最も重い弱点」の外にある指摘の中身（採否の表で見ること）。', '',
            '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
    open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(out))
    print('written', OUT, sum(len(x) for x in out), 'chars')


if __name__ == '__main__':
    main()
