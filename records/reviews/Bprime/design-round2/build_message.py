# -*- coding: utf-8 -*-
"""build_message.py v0（2026-09-29・B′ の設計の巡・二巡目の発話を組む・grok-4.7 と claude.ai の三つに同じものを送る・コーディネータ南無弥勒如来）。
一巡目の器の型: 依頼文を頭に置き、束のファイルを「=== ファイル名 ===」の見出しつきで並べる。束の中身の SHA を MANIFEST と確かめてから組む。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'kit')
NL = chr(10)
HEAD = ['glossary-bprime.md', 'design-Bprime-draft4.md', 'round1/adoption-design-round1.md', 'round1/mapping-draft4.md',
        'round1/round1-verdicts-extract.md', 'round1/facts-round1.md', 'round1/rulings-D263.md']


def build():
    man = [l.split('  ', 1) for l in open(os.path.join(KIT, 'MANIFEST.sha256'), encoding='utf-8').read().split(NL) if l.strip()]
    for h, name in man:
        if hashlib.sha256(open(os.path.join(KIT, name), 'rb').read()).hexdigest() != h:
            sys.exit('束の中身の SHA が違う: %s' % name)
    names = [n for _, n in man]
    assert all(h in names for h in HEAD) and 'request-design-round2.md' in names
    order = HEAD + sorted(n for n in names if n not in HEAD and n != 'request-design-round2.md')
    parts = [open(os.path.join(KIT, 'request-design-round2.md'), encoding='utf-8').read(), NL + '# 束のファイル' + NL]
    for n in order:
        parts.append(NL + '=== %s ===' % n + NL + open(os.path.join(KIT, n), encoding='utf-8').read())
    return ''.join(parts)


if __name__ == '__main__':
    out = os.path.join(HERE, 'kit-message.md')
    assert not os.path.exists(out), '既にある'
    m = build()
    open(out, 'w', encoding='utf-8', newline=NL).write(m)
    print('kit-message.md', len(m), 'chars | sha16', hashlib.sha256(m.encode('utf-8')).hexdigest().upper()[:16])
