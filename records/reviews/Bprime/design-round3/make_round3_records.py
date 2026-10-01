# -*- coding: utf-8 -*-
"""make_round3_records.py v0（2026-09-29・B′ の設計の巡・三巡目〔最終の検分〕の束のため・三つの記録を機械で作る・コーディネータ南無弥勒如来）。
1. `facts-round2.md`: 二巡目の採否で確かめた事実を、出所のファイルから抜き出す（SHA16 と鍵か行を添え、値は出所から読む）。
2. `mapping-draft6.md`: 草案6 の中の〔R..〕〔S..〕の印と、一巡目・二巡目の採否の表の行の対応を並べる（欄は「 | 」で割る）。
3. `round2-verdicts-extract.md`: 二巡目の四票の「Q7 最も重い弱点」と「総評」の節を、票のファイルから一字違わず切り出す。
どの出力も一度だけ書く。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, math, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.normpath(os.path.join(HERE, '..', '..'))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b/'
NL = chr(10)
FENCE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()[:16]


def once(path, lines):
    assert not os.path.exists(path), ('既にある（一度だけ）', path)
    open(path, 'w', encoding='utf-8', newline=NL).write(NL.join(lines))


def facts():
    out = ['# 二巡目の採否で確かめた事実（機械で抜き出した・B′ の設計の巡・三巡目の束・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
           '- 何か: 二巡目の採否の表（`adoption-design-round2.md`）の「確かめ」の欄の事実のうち、束のほかのファイルに無いものを、出所のファイルから器 `make_round3_records.py` が抜き出したもの。値は出所から読み、手で打っていない。', '']
    p = PUB + 'records/Bl3/pilot/pilot-20260926T103442Z/pilot.json'
    d = json.load(open(p, encoding='utf-8'))
    pv = d['pilot']
    out += ['## 1. 層三の下見の記録（公開の置き場 `records/Bl3/pilot/pilot-20260926T103442Z/pilot.json`・SHA16 %s）' % sha16(p), '',
            '- `pilot.vi.a` の N1|O-Ncold: %r・S4|Onull: %r・`pilot.vi.decision.spread_a`: %r' % (pv['vi']['a']['N1|O-Ncold'], pv['vi']['a']['S4|Onull'], pv['vi']['decision']['spread_a']),
            '- `pilot.v.diffs` の N1|Onull: %r' % pv['v']['diffs']['N1|Onull'],
            '- 層三の最終版の 470 行目（`facts-round1.md` の 1）で二つとも 1.621 と書かれた値は、(vi) の (a) の S4|Onull と (v) の N1|Onull の、別の値が四桁で丸めて重なったもの。', '']
    pB = PUB + 'design/contrasts-B.json'
    T = json.load(open(pB, encoding='utf-8'))
    out += ['## 2. 段階 B の正本（公開の置き場 `design/contrasts-B.json`・SHA16 %s）の鍵（逐語）' % sha16(pB), '',
            '- `censor.text`: 「%s」' % T['censor']['text'],
            '- `report_rules.format_fail_denominator`: 「%s」' % T['report_rules']['format_fail_denominator'],
            '- `interval.method`: 「%s」・`interval.conf`: %r' % (T['interval']['method'], T['interval']['conf']), '']
    pL = BP + '/reviews/design-round3/kit/reference/contrasts-Bl3.json' if False else PUB + 'design/contrasts-Bl3.json'
    L3 = json.load(open(pL, encoding='utf-8'))
    ro = L3['review_plan'].get('order')
    out += ['## 3. 層三の正本（公開の置き場 `design/contrasts-Bl3.json`・SHA16 %s）の鍵（逐語・束の `reference/contrasts-Bl3.json` と同じファイル）' % sha16(pL), '',
            '- `computation.before_seal`: 「%s」' % L3['computation']['before_seal'],
            '- `computation.main_freeze_check`: 「%s」' % L3['computation']['main_freeze_check'],
            '- `pilot.order`: 「%s」' % L3['pilot']['order'],
            '- `independent_recompute.agreement`: 「%s」' % L3['independent_recompute']['agreement'],
            '- `review_plan.order` のうち「凍結」の語を含む段: %s' % '／'.join('「%s」' % x for x in ro if '凍結' in x), '']
    pc = BP + '/tools/boot_bprime_cost.py'
    out += ['## 4. 費用の見込みの数え直し（コーディネータの計算）', '',
            '- 層三の組み方（組ごとに 名前のある 4・等方 1999・実在の差 28・零 1 の 2032・Onull の 4 組に逆の向きの 28 と零 1 の 29）でのバッチ 16 の回数: 12 × ⌈2032/16⌉ ＋ 4 × ⌈29/16⌉ ＝ %d' % (12 * math.ceil(2032 / 16) + 4 * math.ceil(29 / 16)),
            '- 費用の下見の器 `Bprime/tools/boot_bprime_cost.py`（SHA16 %s）の式の値: 12 × ⌈2060/16⌉ ＋ 3 × ⌈57/16⌉ ＝ %d（二重の数えと、逆の向きの組を 3 と数えたこと）' % (sha16(pc), 12 * math.ceil(2060 / 16) + 3 * math.ceil(57 / 16)), '',
            '## この記録が確認していないこと', '',
            '- 公開の置き場の写しが GitHub の上の版と同じか（手元の写しの版 0a45688 の後に push は無い）。', '', FENCE, '']
    once(os.path.join(HERE, 'facts-round2.md'), out)


def table_rows(path, prefix):
    rows = {}
    for l in open(path, encoding='utf-8').read().split(NL):
        if re.match(r'^\| %s\d\d \| ' % prefix, l):
            cells = [c.strip() for c in l.strip().strip('|').split(' | ')]
            assert len(cells) == 6, ('欄の数が 6 でない', cells[0], len(cells))
            rows[cells[0]] = (cells[1], cells[4])
    return rows


def mapping():
    d6 = BP + '/design/design-Bprime-draft6.md'
    a1 = BP + '/reviews/design-round1/adoption-design-round1.md'
    a2 = BP + '/reviews/design-round2/adoption-design-round2.md'
    L = open(d6, encoding='utf-8').read().split(NL)
    head, where = '', {}
    for i, l in enumerate(L, 1):
        if l.startswith('#'):
            head = l.lstrip('#').strip()
        for m in re.finditer(r'〔([^〕]*)〕', l):
            for r in m.group(1).split('・'):
                if re.match(r'^[RS]\d\d$', r):
                    where.setdefault(r, []).append((i, head))
    out = ['# 採否の表の行と草案6 の対応（機械で並べた・B′ の設計の巡・三巡目の束・2026-09-29・コーディネータ南無弥勒如来・非公開）', '',
           '- 器: `make_round3_records.py`。草案6 `design-Bprime-draft6.md`（SHA16 %s）の中の〔R..〕〔S..〕の印と、一巡目の採否の表（SHA16 %s・行 R01〜R41）・二巡目の採否の表（SHA16 %s・行 S01〜S29）の行を突き合わせた。' % (sha16(d6), sha16(a1), sha16(a2)),
           '- 印は「その行の直しがここに入った」という起草者の印で、直しが正しいかの確かめではない（それは三巡目の検分の問い）。', '']
    for label, rows in (('一巡目（R）', table_rows(a1, 'R')), ('二巡目（S）', table_rows(a2, 'S'))):
        out += ['## %s' % label, '', '| 行 | 主題 | 採否 | 草案6 の印の所（行の番号・節） |', '|---|---|---|---|']
        none = []
        for r in sorted(rows):
            subj, dec = rows[r]
            w = where.get(r, [])
            if not w:
                none.append(r)
            cell = '・'.join('%d（%s）' % (i, h[:24]) for i, h in w) if w else '印なし'
            out.append('| %s | %s | %s | %s |' % (r, subj, dec.replace('|', '｜'), cell))
        out += ['', '- 印の無い行: %s。' % ('・'.join(none) if none else 'なし'), '']
    extra = sorted(r for r in where if not (r.startswith('R') and 1 <= int(r[1:]) <= 41) and not (r.startswith('S') and 1 <= int(r[1:]) <= 29))
    out += ['- 採否の表に無い印: %s。' % ('・'.join(extra) if extra else 'なし'), '', FENCE, '']
    once(os.path.join(HERE, 'mapping-draft6.md'), out)
    return extra


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


def verdicts():
    V = BP + '/reviews/design-round2/votes'
    out = ['# 二巡目の四票の「最も重い弱点」と総評の抜き書き（逐語・器 `make_round3_records.py`・B′ の設計の巡・三巡目の束・2026-09-29）', '',
           '- 票の全文はこの束に入れていない（層三の設計の巡の二巡目の束と同じ型）。各々の指摘は二巡目の採否の表の行に入っている。追い問いの答えの要点も採否の表の「追い問いで分かったこと」にある。',
           '- 抜き書きは票のファイルから一字違わず切り出した。見出しの深さは票のまま。', '']
    for name, lin in (('grok-4.7', '系統外・xAI'), ('claude-ai-4', '系統内・Anthropic（三つで一票）'), ('claude-ai-5', '系統内・Anthropic（三つで一票）'), ('claude-ai-6', '系統内・Anthropic（三つで一票）')):
        p = os.path.join(V, name, 'response.md')
        t = open(p, encoding='utf-8').read()
        out.append('## %s（%s・二巡目の `votes/%s/response.md`・SHA16 %s）' % (name, lin, name, sha16(p)))
        out.append('')
        got = sections(t, 'Q7') + sections(t, '総評')
        assert got, ('節が見つからない', name)
        for s in got:
            out += ['```text', s, '```', '']
    out += ['## この抜き書きが確認していないこと', '', '- 最も重い弱点と総評の外にある指摘の中身（採否の表で見ること）。', '', FENCE, '']
    once(os.path.join(HERE, 'round2-verdicts-extract.md'), out)


if __name__ == '__main__':
    facts()
    extra = mapping()
    verdicts()
    print('written: facts-round2.md, mapping-draft6.md, round2-verdicts-extract.md | extra marks:', extra)
