# -*- coding: utf-8 -*-
"""citations_B.py v1 —— 「採否表 P…」の引用を採否表と照らす（2026-09-19・束の前の点検で、手で打った引用の誤りが多数見つかったため）。

照らすもの（正本 JSON の文字列・草案・報告雛形・器材のソースの注と文字列）:
  (1) 引いた P が採否表（`records/reviews/**/adoption-table-*.md` の行と、軽微の一覧の見出し）にあるか。
  (2) 引用と同じ括弧の中に裁定の番号があり、引いた行にも裁定の番号があるとき、両者が重なるか。
  (3) 引用に添えた出所の札（系統外の検分・系統内の検分・系統内外・系統外の一名だけ・四票すべて・四票のうち三票・同系列の二票）が、
      引いた行の出所の欄と合うか（段階 B の採否表だけ。系統外＝Gemini・g1・g2／系統内＝claude.ai・c1・c2・エージェント）。
**照らせないもの**: 裁定の番号も札も添えていない引用で、別の行を引いていても、この器は気づかない。
同じ裁定・同じ出所の隣の行を引いた誤り（例: 同じ裁定 D130 の P371 と P372）も気づかない。**中身の一致は見ていない。**
用法: python tools/citations_B.py [--json 出力]   （違反があれば終了コード 1）
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, argparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION = 'v1'
SELF = os.path.basename(__file__)
TOOL_GLOBS = ('tools/*_B.py', 'tools/build_draftB.py')
DOCS = ('design/design-stageB-draft12.md', 'records/B/results-report-template-B.md')
CANON = 'design/contrasts-B.json'


def _lineage(table_dir, text):
    """出所の欄から検分者の集合を作る（G＝系統外・C＝系統内）。段階 B の採否表だけ。"""
    v = set()
    if table_dir == 'external-round':
        if '四票' in text:
            v |= {'G1', 'G2', 'C1', 'C2'}
        for who, tag in (('Gemini', 'G'), (r'claude\.ai', 'C')):
            if re.search(who + r' 二票', text):
                v |= {tag + '1', tag + '2'}
            if re.search(who + r' 一人目', text):
                v.add(tag + '1')
            if re.search(who + r' 二人目', text):
                v.add(tag + '2')
    elif table_dir == 'design-round2':
        v |= {t.upper() for t in re.findall(r'(?<![A-Za-z\d])([gc][12])(?![\d])', text)}
    elif table_dir in ('design-round1', 'impl-round'):
        v |= {'C' + t[1] for t in re.findall(r'(?<![A-Za-z\d])(a[12])(?![\d])', text)}
        if '一体目' in text:
            v.add('C1')
        if '二体目' in text:
            v.add('C2')
    elif table_dir == 'impl-round-2':
        if '一体目' in text:
            v.add('C1')
        if '二体目' in text:
            v.add('C2')
    return v


def load_rows(repo=REPO):
    """P → {table, d（裁定の番号の集合）, voters（段階 B の表のときだけ）, stage_b}。"""
    rows = {}
    for f in sorted(glob.glob(os.path.join(repo, 'records', 'reviews', '**', 'adoption-table-*.md'), recursive=True)):
        rel = os.path.relpath(f, repo).replace('\\', '/')
        parts = rel.split('/')
        tdir = parts[-2]
        stage_b = len(parts) > 3 and parts[2] == 'B'
        text = open(f, encoding='utf-8').read().replace('\r\n', '\n')
        for ln in text.split('\n'):
            m = re.match(r'^\| (P\d+) \|', ln)
            if not m:
                continue
            cols = [c.strip() for c in ln.strip().strip('|').split('|')]
            if tdir in ('external-round', 'impl-round-2'):
                src = cols[2] if len(cols) > 2 else ''
            elif tdir == 'design-round2':
                src = cols[3] if len(cols) > 3 and re.match(r'K\d+$', cols[1]) else (cols[2] if len(cols) > 2 else '')
            else:
                src = ' '.join(cols[2:4])
            assert m.group(1) not in rows, ('採否表の番号が重なる', m.group(1), rel)
            rows[m.group(1)] = {'table': rel, 'd': set(re.findall(r'D\d+', ' '.join(cols[-2:]))),
                                'voters': _lineage(tdir, src) if stage_b else None}
        # 軽微の一覧（表の行ではなく見出しと段落でまとめて採った番号）
        for m in re.finditer(r'^## \d+\. 軽微の一覧（(P\d+)・まとめて採る）\n\n\*\*\1\*\*: ([^\n]*)', text, flags=re.M):
            assert m.group(1) not in rows, ('採否表の番号が重なる', m.group(1), rel)
            rows[m.group(1)] = {'table': rel, 'd': set(), 'voters': _lineage(tdir, m.group(2).split('は、')[0]) if stage_b else None}
    return rows


LABELS = (('系統外の一名だけ', lambda v: sum(x[0] == 'G' for x in v) == 1 and not any(x[0] == 'C' for x in v)),
          ('系統内外', lambda v: any(x[0] == 'G' for x in v) and any(x[0] == 'C' for x in v)),
          ('系統外', lambda v: any(x[0] == 'G' for x in v)),
          ('系統内の', lambda v: bool(v) and not any(x[0] == 'G' for x in v)),
          ('四票すべて', lambda v: len(v) == 4),
          ('四票のうち三票', lambda v: len(v) == 3),
          ('同系列の二票', lambda v: sum(x[0] == 'C' for x in v) == 2))


def _enclosing(text, pos):
    """pos を囲む全角の括弧（入れ子を数える）の (開き, 閉じ) を返す。囲まれていなければ None。"""
    depth, i = 0, pos - 1
    while i >= 0:
        c = text[i]
        if c == '）':
            depth += 1
        elif c == '（':
            if depth == 0:
                break
            depth -= 1
        i -= 1
    if i < 0:
        return None
    depth, j = 0, pos
    while j < len(text):
        c = text[j]
        if c == '（':
            depth += 1
        elif c == '）':
            if depth == 0:
                return i, j
            depth -= 1
        j += 1
    return None


CIT = re.compile(r'(?<![A-Za-z0-9_])P(\d{3})(?!\d)(?:\s*〜\s*P?(\d{3}))?')


def check_text(text, where, rows):
    """一つの文字列（正本の値・文書の一行・ソースの一行）の引用を照らし、違反の一覧を返す。"""
    out = []
    n = {'cit': 0, 'd': 0, 'label': 0}
    for m in CIT.finditer(text):
        a = int(m.group(1))
        b = int(m.group(2)) if m.group(2) else None
        n['cit'] += 1
        cited = ['P%d' % k for k in range(a, b + 1)] if b else ['P%d' % a]
        miss = [p for p in cited if p not in rows]
        if b is None and miss:
            out.append((where, 'P%d' % a, '採否表に無い番号'))
            continue
        if b is not None and ('P%d' % a in miss or 'P%d' % b in miss):
            out.append((where, 'P%d〜P%d' % (a, b), '範囲の端が採否表に無い'))
            continue
        # 引用を囲む括弧（入れ子を数える・無ければ裁定と札は照らさない）
        enc = _enclosing(text, m.start())
        if enc is None:
            continue
        lp, rp = enc
        paren = text[lp:rp + 1]
        ds = set(re.findall(r'(?<![A-Za-z\d])D\d+', paren))
        if b is None:
            rd = rows['P%d' % a]['d']
            if ds and rd:
                n['d'] += 1
                if not (ds & rd):
                    out.append((where, 'P%d' % a, '括弧の裁定 %s と採否表の行の裁定 %s が重ならない' % ('・'.join(sorted(ds)), '・'.join(sorted(rd)))))
        # 出所の札: 括弧の手前（前の括弧の後から最大 80 字）と括弧の中
        prev_close = text.rfind('）', 0, lp)
        zone = text[max(lp - 80, prev_close + 1):rp + 1]
        voters = set()
        known = True
        for p in re.findall(r'P\d{3}', paren):
            if p in rows:
                if rows[p]['voters'] is None:
                    known = False
                else:
                    voters |= rows[p]['voters']
        if not known or not voters:
            continue
        hit = [lab for lab, _ in LABELS if lab in zone]
        if '系統外の一名だけ' in hit and '系統外' in hit:
            hit.remove('系統外')
        for lab, ok in LABELS:
            if lab in hit:
                n['label'] += 1
                if not ok(voters):
                    out.append((where, 'P%d' % a, '出所の札「%s」が採否表の出所（%s）と合わない' % (lab, '・'.join(sorted(voters)))))
    return out, n


def _walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _walk(v, path + '.' + k if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _walk(v, '%s[%d]' % (path, i))
    elif isinstance(o, str):
        yield path, o


def check_all(repo=REPO, docs=DOCS):
    """正本・文書（既定は草案と報告雛形）・器材を照らす。(違反, 数) を返す。
    組み立て器は、組み上げた一本だけを docs に渡す（もう一方がまだ古い正本で組まれたままでも止まらないように）。"""
    rows = load_rows(repo)
    out, tot = [], {'cit': 0, 'd': 0, 'label': 0, 'units': 0}

    def run(text, where):
        o, n = check_text(text, where, rows)
        out.extend(o)
        tot['units'] += 1
        for k in ('cit', 'd', 'label'):
            tot[k] += n[k]
    T = json.load(open(os.path.join(repo, *CANON.split('/')), encoding='utf-8'))
    for path, s in _walk(T):
        run(s, '%s:%s' % (CANON, path))
    files = [d for d in docs if os.path.exists(os.path.join(repo, *d.split('/')))]
    for g in TOOL_GLOBS:
        files += sorted(os.path.relpath(f, repo).replace('\\', '/') for f in glob.glob(os.path.join(repo, *g.split('/'))))
    for rel in files:
        if rel.endswith(SELF):
            continue
        for i, ln in enumerate(open(os.path.join(repo, *rel.split('/')), encoding='utf-8').read().replace('\r\n', '\n').split('\n'), 1):
            if 'P' in ln:
                run(ln, '%s:%d' % (rel, i))
    return out, dict(tot, rows=len(rows), files=len(files))


def _selftest():
    rows = {'P100': {'table': 't', 'd': {'D5'}, 'voters': {'C1', 'C2'}},
            'P101': {'table': 't', 'd': {'D6'}, 'voters': {'G2'}},
            'P102': {'table': 't', 'd': set(), 'voters': {'G1', 'G2', 'C2'}},
            'P103': {'table': 't', 'd': {'D6'}, 'voters': None}}
    ok = lambda t: not check_text(t, 'x', rows)[0]
    assert ok('前は穴があった（系統内の検分・裁定 D5・採否表 P100）'), '正しい引用を止めた'
    # 一つの試験には一つの食い違いだけを入れる（二つ混ぜると、片方の照合を外しても他方で落ち、守りを試せない——
    # 変異の器が実際にそれを捕まえた・2026-09-19）
    assert not ok('前は穴があった（裁定 D5・採否表 P101）'), '裁定の食い違いを止めない（札なし）'
    assert not ok('前は穴があった（系統外の検分・裁定 D5・採否表 P101）'), '裁定の食い違いを止めない（札は合っている）'
    assert not ok('前は穴があった（系統外の検分・採否表 P100）'), '札の食い違いを止めない（裁定なし）'
    assert not ok('前は穴があった（系統外の検分・裁定 D5・採否表 P100）'), '札の食い違いを止めない（裁定は合っている）'
    assert ok('前は穴があった（系統外の検分・採否表 P101）'), '合う札を止めた'
    assert not ok('（採否表 P109）'), '無い番号を止めない'
    assert not ok('（四票すべてが挙げた・採否表 P102）'), '票の数の食い違いを止めない'
    assert ok('（四票のうち三票が挙げた・採否表 P102）'), '合う票の数を止めた'
    assert ok('すり抜けた（系統内の検分・採否表 P100） 同方向（裁定 D6・採否表 P101）'), '前の括弧の札が次の引用に漏れた'
    assert ok('（系統内の検分・裁定 D6・採否表 P103）'), '段階 B の外の表の出所を照らした'
    assert ok('（採否表 P100〜P102）') and not ok('（採否表 P100〜P109）'), '範囲の端の検査が効かない'
    assert ok('# 採否表 P100'), '括弧の無い引用で止めた'
    assert not ok('（前は（x）であった・系統外の検分・採否表 P100）'), '入れ子の括弧の中の引用を照らさない'
    assert ok('（前は（x）であった・系統内の検分・裁定 D5・採否表 P100）'), '入れ子の括弧の中の正しい引用を止めた'
    print('[citations_B] 自己検査: すべて通った')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default=None)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    _selftest()
    if a.selftest:
        sys.exit(0)
    out, tot = check_all()
    print('[citations_B %s] 採否表の番号 %d・照らした単位 %d（ファイル %d と正本）・引用 %d・裁定の照合 %d・札の照合 %d・違反 %d'
          % (VERSION, tot['rows'], tot['units'], tot['files'], tot['cit'], tot['d'], tot['label'], len(out)))
    for w, p, why in out:
        print('  違反: %s %s —— %s' % (w, p, why))
    if a.json:
        json.dump({'version': VERSION, 'totals': tot, 'violations': [{'where': w, 'cite': p, 'why': y} for w, p, y in out]},
                  open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(1 if out else 0)
