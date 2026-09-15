# -*- coding: utf-8 -*-
"""review_checks_A.py v1 —— 凍結確認の前の草案9 の見直しの機械の突き合わせ（2026-09-15・事前登録 records/A/freeze-prep/preregistration-review-draft9-A.md の §2 A の M1〜M8）。
対象: 組み立てた草案9（既定 design/design-stageA-draft9.md）と報告雛形（既定 records/A/results-report-template-A.md）。本文は変えない。
M1 code span のパスの実在・M2 code span の正本のキーの実在・M3 節と読み条項の参照・M4 裁定の番号（§5 の一覧との突き合わせ・重なりと欠け）・M5 採否表の番号・M6 器の名に添えた版と器のファイルの版・M7 価値語と機序語・M8 末尾の柵の一行。
見つけたものは全件印字する。直すかどうかは見直しの記録で決める（本器は判定をしない）。外の文書の節（F §0-5 など）を引く参照は M3 で「解けない」に数えるので、見直しの記録で内と外を分ける。
用法: python tools/review_checks_A.py [--draft …] [--template …] [--out records/A/freeze-prep/review-checks-A] [--force]
柵: 本器の出力のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
CODE = re.compile(r'`([^`\n]+)`')
PATH_TOK = re.compile(r'(?:records|design|tools|arms|results|prompts)/[^\s`、。・（）()〔〕\[\]|「」]*')
BARE_FILE = re.compile(r'^[\w\-.]+\.(?:py|R|json|md|html|sh|jsonl|txt)$')
FILE_EXT = re.compile(r'\.(?:py|R|json|md|html|sh|jsonl|txt)$')
KEY_SPAN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_\-]+)+$')
WORD_SPAN = re.compile(r'^[a-z][a-z0-9_]+$')
TABLES = ['records/reviews/A/prefreeze/adoption-table-A-prefreeze.md', 'records/reviews/A/draft7-impl/adoption-table-impl-A.md', 'records/reviews/A/final/adoption-table-A-final.md']
SEARCH_ROOTS = ['tools', 'design', 'records', 'arms']
FENCE = '両方向不定'


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def ctx(text, pos, end=None, w=24):
    end = pos if end is None else end
    return text[max(0, pos - w):min(len(text), end + w)].replace('\n', '⏎')


def find_bare(name):
    for root in SEARCH_ROOTS:
        hits = glob.glob(os.path.join(REPO, root, '**', name), recursive=True)
        if hits:
            return os.path.relpath(hits[0], REPO).replace('\\', '/')
    return None


def m1_paths(text):
    out = []
    for m in CODE.finditer(text):
        span = m.group(1); ln = line_of(text, m.start()); toks = PATH_TOK.findall(span)
        if not toks and BARE_FILE.match(span):
            hit = find_bare(span); out.append({'line': ln, 'span': span, 'token': span, 'status': 'bare_found' if hit else 'bare_missing', 'found': hit}); continue
        for t in toks:
            t = t.rstrip('.,:;')
            if re.search(r'[<>{}*]|YYYY', t):
                base = re.split(r'[<>{}*]|YYYY', t)[0]; d = base if base.endswith('/') else os.path.dirname(base)
                if '*' in t and not re.search(r'[<>{}]', t):
                    st = 'glob_ok' if glob.glob(os.path.join(REPO, t)) else 'glob_none'
                else:
                    st = 'template_dir_ok' if os.path.isdir(os.path.join(REPO, d)) else 'template_dir_missing'
                out.append({'line': ln, 'span': span, 'token': t, 'status': st}); continue
            p = os.path.join(REPO, t)
            st = ('dir_ok' if os.path.isdir(p) else 'dir_missing') if t.endswith('/') else ('ok' if os.path.exists(p) else 'missing')
            out.append({'line': ln, 'span': span, 'token': t, 'status': st})
    return out


def resolve(S, dotted):
    cur = S
    for seg in dotted.split('.'):
        if isinstance(cur, dict) and seg in cur:
            cur = cur[seg]
        elif isinstance(cur, list) and seg.isdigit() and int(seg) < len(cur):
            cur = cur[int(seg)]
        else:
            return False
    return True


def all_keys(o, acc=None):
    acc = set() if acc is None else acc
    if isinstance(o, dict):
        for k, v in o.items():
            acc.add(k); all_keys(v, acc)
    elif isinstance(o, list):
        for v in o:
            all_keys(v, acc)
    return acc


def m2_keys(text, S):
    keys = all_keys(S); out = []
    for m in CODE.finditer(text):
        span = m.group(1).strip(); ln = line_of(text, m.start())
        if KEY_SPAN.match(span) and not FILE_EXT.search(span):
            out.append({'line': ln, 'span': span, 'status': 'ok' if resolve(S, span) else 'missing'})
        elif WORD_SPAN.match(span):
            out.append({'line': ln, 'span': span, 'status': 'top' if span in S else ('nested' if span in keys else 'absent_word')})
    return out


def sections(text):
    heads = set()
    for m in re.finditer(r'^## (\d+)\.', text, flags=re.M):
        heads.add(m.group(1))
    for m in re.finditer(r'^### (\d+\.\d+)', text, flags=re.M):
        heads.add(m.group(1))
    for m in re.finditer(r'^### (\d+)-補', text, flags=re.M):
        heads.add(m.group(1) + '-補')
    s0 = re.search(r'^## 0\..*?(?=^## 1\.)', text, flags=re.M | re.S)
    if s0:
        for m in re.finditer(r'^(\d+)\. ', s0.group(0), flags=re.M):
            heads.add('0-' + m.group(1))
    s3 = re.search(r'^## 3\..*?(?=^## 4\.)', text, flags=re.M | re.S)
    clauses = set(re.findall(r'^- \(([ivx]+)\)', s3.group(0), flags=re.M)) if s3 else set()
    return heads, clauses


def m3_refs(text):
    heads, clauses = sections(text); out = []
    for m in re.finditer(r'§\s?(\d+(?:\.\d+)?(?:-(?:\d+|補))?)', text):
        ref = m.group(1); ok = ref in heads
        out.append({'line': line_of(text, m.start()), 'ref': '§' + ref, 'status': 'ok' if ok else 'unresolved', 'context': ctx(text, m.start(), m.end())})
    for m in re.finditer(r'(?:§3|読み条項)\s?((?:\([ivx]+\)・?)+)', text):
        for r in re.findall(r'\(([ivx]+)\)', m.group(1)):
            out.append({'line': line_of(text, m.start()), 'ref': '(%s)' % r, 'status': 'ok' if r in clauses else 'unresolved_clause', 'context': ctx(text, m.start(), m.end())})
    return out, sorted(heads), sorted(clauses)


def listed_decisions(draft_text):
    s5 = re.search(r'^## 5\..*?(?=^## 6\.)', draft_text, flags=re.M | re.S)
    listed = [int(x) for x in re.findall(r'^- D(\d+) ', s5.group(0), flags=re.M)] if s5 else []
    return listed


def m4_decisions(text, listed):
    known = set(listed) | {4, 5}; out = []
    for m in re.finditer(r'(?<![A-Za-z0-9\-])D(\d+)(?:〜D?(\d+))?(?![\d\-])', text):
        a, b = int(m.group(1)), (int(m.group(2)) if m.group(2) else None)
        bad = [x for x in ([a] if b is None else [a, b]) if x not in known]
        out.append({'line': line_of(text, m.start()), 'ref': m.group(0), 'status': 'ok' if not bad else 'unlisted', 'context': ctx(text, m.start(), m.end())})
    return out


def m5_adoption(text):
    pset = set()
    for t in TABLES:
        pset |= {int(x) for x in re.findall(r'^\|\s*P(\d+)', open(os.path.join(REPO, t), encoding='utf-8').read(), flags=re.M)}
    out = []
    for m in re.finditer(r'(?<![A-Za-z0-9])P(\d+)(?:〜P?(\d+))?(?!\d)', text):
        a, b = int(m.group(1)), (int(m.group(2)) if m.group(2) else None)
        bad = [x for x in ([a] if b is None else [a, b]) if x not in pset]
        out.append({'line': line_of(text, m.start()), 'ref': m.group(0), 'status': 'ok' if not bad else 'not_in_tables', 'context': ctx(text, m.start(), m.end())})
    return out, len(pset)


def tool_version(name):
    p = find_bare(name)
    if not p:
        return None, None, None
    src = open(os.path.join(REPO, p), encoding='utf-8', errors='replace').read()
    m = re.search(r"^VERSION\s*=\s*'(v[\d.]+)'", src, flags=re.M)
    if m:
        return m.group(1), 'VERSION', p
    m = re.search(re.escape(name) + r'\s+(v\d+(?:\.\d+)*)', src[:3000])
    return (m.group(1), 'docstring', p) if m else (None, None, p)


def m6_versions(text):
    out = []
    for m in re.finditer(r'`(?:tools/)?(?:colab/)?([\w\-]+\.(?:py|R))`\s?(v\d+(?:\.\d+)*)', text):
        name, ref = m.group(1), m.group(2); fv, how, p = tool_version(name)
        out.append({'line': line_of(text, m.start()), 'tool': name, 'text_version': ref, 'file_version': fv, 'how': how, 'path': p, 'status': 'ok' if fv == ref else ('no_file_version' if fv is None else 'mismatch'), 'context': ctx(text, m.start(), m.end())})
    return out


def m7_words(text, S):
    PS = S['print_strings']; out = []
    for kind, words in (('value', PS['value_word_ban']), ('mechanism', PS['mechanism_word_ban'])):
        for w in words:
            for m in re.finditer(re.escape(w), text):
                out.append({'line': line_of(text, m.start()), 'kind': kind, 'word': w, 'context': ctx(text, m.start(), m.end())})
    return out


def m8_fence(text):
    last = [l for l in text.split('\n') if l.strip()][-1]
    return {'last_line': last[:200], 'ok': FENCE in last and '引用してはならない' in last}


def check(path, S, listed):
    text = open(os.path.join(REPO, path), encoding='utf-8').read()
    m3, heads, clauses = m3_refs(text); m5, n_p = m5_adoption(text)
    R = {'file': path, 'sha16': runs_A.sha16_file(os.path.join(REPO, path)), 'M1': m1_paths(text), 'M2': m2_keys(text, S), 'M3': m3, 'M3_heads': heads, 'M3_clauses': clauses,
         'M4': m4_decisions(text, listed), 'M5': m5, 'M5_table_rows': n_p, 'M6': m6_versions(text), 'M7': m7_words(text, S), 'M8': m8_fence(text)}
    return R


BAD = {'M1': ('missing', 'dir_missing', 'template_dir_missing', 'glob_none', 'bare_missing'), 'M2': ('missing', 'absent_word'), 'M3': ('unresolved', 'unresolved_clause'), 'M4': ('unlisted',), 'M5': ('not_in_tables',), 'M6': ('mismatch', 'no_file_version')}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--draft', default='design/design-stageA-draft9.md'); ap.add_argument('--template', default='records/A/results-report-template-A.md')
    ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'freeze-prep', 'review-checks-A')); ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    if not a.force and (os.path.exists(a.out + '.json') or os.path.exists(a.out + '.md')):
        sys.exit('既存の記録があるので上書きしない（--force）: %s' % a.out)
    S = runs_A.load_T(); dtext = open(os.path.join(REPO, a.draft), encoding='utf-8').read(); listed = listed_decisions(dtext)
    dups = sorted({x for x in listed if listed.count(x) > 1}); gaps = sorted((set(range(1, max(listed) + 1)) - {4, 5}) - set(listed)) if listed else []
    RES = [check(a.draft, S, listed), check(a.template, S, listed)]
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
    OUT = {'kind': 'review_checks_A', 'version': VERSION, 'generated_utc': now, 'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'decisions_listed': listed, 'decisions_duplicates': dups, 'decisions_gaps': gaps,
           'results': RES, 'preregistration': 'records/A/freeze-prep/preregistration-review-draft9-A.md', 'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out + '.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(OUT, ensure_ascii=False, indent=1) + '\n')
    esc = lambda s: str(s).replace('|', '／')
    M = ['# 草案9 の見直しの機械の突き合わせ（機械生成・`tools/review_checks_A.py` %s・%s UTC）' % (VERSION, now), '',
         '- 事前登録: `%s` の §2 A（M1〜M8）。本器は判定をしない。直すかどうかは見直しの記録で決める。' % OUT['preregistration'],
         '- 正本 SHA16 %s・§5 の裁定の番号 %d 件（重なり %s・欠け %s・段階 B の D4・D5 を除く）' % (OUT['contrasts_sha16'], len(listed), dups or 'なし', gaps or 'なし'), '']
    for R in RES:
        M += ['## %s（SHA16 %s）' % (R['file'], R['sha16']), '']
        for k in ('M1', 'M2', 'M3', 'M4', 'M5', 'M6'):
            bad = [x for x in R[k] if x['status'] in BAD[k]]
            M.append('- %s: %d 件のうち要確認 %d 件' % (k, len(R[k]), len(bad)))
            for x in bad:
                M.append('  - 行 %d: %s' % (x['line'], esc({kk: vv for kk, vv in x.items() if kk != 'line'})))
        M.append('- M7: 価値語と機序語の出現 %d 件' % len(R['M7']))
        for x in R['M7']:
            M.append('  - 行 %d: %s「%s」…%s…' % (x['line'], x['kind'], x['word'], esc(x['context'])))
        M += ['- M8: 末尾の柵の一行 %s（%s）' % ('あり' if R['M8']['ok'] else '**なし**', esc(R['M8']['last_line'][:80])), '']
    M.append(OUT['clause'])
    open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
    print('[review_checks_A %s] written %s.{json,md} | %s' % (VERSION, a.out, ' / '.join('%s: %s' % (R['file'], {k: sum(1 for x in R[k] if x['status'] in BAD[k]) for k in BAD} | {'M7': len(R['M7']), 'M8': R['M8']['ok']}) for R in RES)))
