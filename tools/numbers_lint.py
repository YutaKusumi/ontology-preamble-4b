# -*- coding: utf-8 -*-
"""numbers_lint.py v1 —— 設計文書の本文と正本 JSON の説明文に「転記行でも設計定数でも構造でもない数」が残っていないかを機械で調べる逆向きの検査器（claude.ai 三票の採否表 C36・2026-09-13）。
用法: python tools/numbers_lint.py --doc design/design-stageA-draft5.md --json design/contrasts-A.json [--report records/A/numbers-lint-draft5A.md]
分類:
  構造＝節番号・日付・時刻・版・草案番号・裁定と採否表と追い問いの番号・機種名・GPU 名・場面名・腕名・SHA・コミット・行頭の番号・code span・パス・URL など（数として読まない）
  設計定数＝正本 JSON の数値の葉と配列の長さ（既測の基底・対比の個票・seed は除く）
  未登録＝それ以外（1 つでもあれば非零で終了）
本文は §6（転記行）と §6-補 を除く。正本 JSON は式・識別子・台帳の文字列を除く説明文を検査する。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, argparse
ap = argparse.ArgumentParser(); ap.add_argument('--doc', required=True); ap.add_argument('--json', required=True); ap.add_argument('--report', default=None)
a = ap.parse_args()
Jd = json.load(open(a.json, encoding='utf-8'))
nz = lambda v: '%.10g' % float(v)
SKIP_CONST = {'bases_4B2507_api', 'contrasts', 'seeds'}
SKIP_STR = SKIP_CONST | {'formula', 'z', 'cp_upper_rule', 'R_control', 'arms_string', 'id', 'src', 'base_src', 'sha16', 'generator', 'version', 'compared_sources', 'tags', 'models', 'value_word_ban', 'mechanism_word_ban', 'weights', 'se', 'interval'}
CONST = set()


def walk_const(x, key=None):
    if key in SKIP_CONST or x is None or isinstance(x, bool) or (key == 'cells' and isinstance(x, list)):
        return
    if isinstance(x, (int, float)):
        CONST.add(nz(x)); return
    if isinstance(x, dict):
        for k, v in x.items():
            walk_const(v, k)
    elif isinstance(x, list):
        CONST.add(nz(len(x)))
        for v in x:
            walk_const(v, key)


STRS = []


def walk_str(x, path, key=None):
    if key in SKIP_STR or (key == 'cells' and isinstance(x, list)):
        return
    if isinstance(x, str):
        STRS.append((path, x)); return
    if isinstance(x, dict):
        for k, v in x.items():
            walk_str(v, path + '.' + k, k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            walk_str(v, '%s[%d]' % (path, i), key)


walk_const(Jd); walk_str(Jd, '$')
MASKS = [r'`[^`]*`', r'https?://\S+', r'SHA-?(?:256|16)', r'(?:records|design|tools|results|arms|prompts)/[\w\-./]+', r'\b[0-9A-F]{16}\b', r'\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b',
         r'\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?(?:\s*UTC)?', r'\b\d{1,2}:\d{2}\b', r'§\s*\d+(?:[.\-]\d+)*(?:-補)?', r'^#{1,6}\s+\d+(?:\.\d+)*(?:-補)?',
         r'\bv\d+(?:\.\d+)*', r'草案\s?\d+[AB]?', r'第[一二三四五六七八九十〇\d]+[章節巡票部段]', r'(?<![A-Za-z])[DCVEJK]\d+(?:〜[DCVEJK]?\d+)?(?![\d.])', r'\(\d+[a-z]\)',
         r'\b(?:I|F)-\d+\b', r'F\s?§0-\d+', r'Qwen\d*(?:[-/][\w.]+)*', r'(?<![\w.])\d+(?:\.\d+)?B(?:-\d{4})?(?![\w])', r'\b(?:L4|T4|A100(?:-SXM4-80GB)?|H100)\b', r'\b\d+\s?GB\b',
         r'\b(?:N1|N2|S1|S4|SK|Odose1|T2)\b', r'\b(?:bf16|fp16|UTF-8|cp932)\b', r'(?:Gemini|Grok|Opus|Fable|Sonnet|Haiku|Claude|Llama|vLLM|torch|transformers|Python|numpy|scipy)\s*[\d.]+(?:\s*(?:Flash|Pro))?',
         r'\b\d+(?:\.\d+){2,}\b', r'^\s*\d+\.\s', r'(?<![\d.])\d+\.(?=\s)', r'\b\d+[x×]\d+\b', r'β[₀-₉]', r'stage[A-Z][\w\-]*', r'\bD-\d+\b', r'#\d+', r'\((?:19|20)\d{2}\)', r'(?:19|20)\d{2}(?=\s*Stat|\s*Biometrika)']
MASK_RE = [re.compile(p, re.M) for p in MASKS]
NUM = re.compile(r'(?<![A-Za-z0-9_.,])[−\-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?')


def unregistered(text):
    t = text
    for rx in MASK_RE:
        t = rx.sub(lambda m: ' ' * len(m.group(0)), t)
    bad = []
    for m in NUM.finditer(t):
        tok = m.group(0); raw = tok.replace(',', '').replace('−', '-').rstrip('%')
        try:
            v = float(raw)
        except ValueError:
            continue
        ok = nz(v) in CONST or nz(abs(v)) in CONST or (tok.endswith('%') and (nz(v / 100) in CONST))
        if not ok:
            bad.append((tok, max(0, m.start() - 24), m.end() + 24))
    return bad


doc = open(a.doc, encoding='utf-8').read().replace('\r\n', '\n').split('\n'); in6 = False; doc_bad = []; checked_lines = 0
for i, l in enumerate(doc, 1):
    if l.startswith('## 6.'):
        in6 = True; continue
    if l.startswith('## 7.'):
        in6 = False
    if in6:
        continue
    checked_lines += 1
    for tok, s0, s1 in unregistered(l):
        doc_bad.append((i, tok, l[s0:s1]))
json_bad = []
for path, s in STRS:
    for tok, s0, s1 in unregistered(s):
        json_bad.append((path, tok, s[s0:s1]))
R = ['# 本文の数の検査（機械生成・`tools/numbers_lint.py` v1）', '', '- 文書: `%s`（検査した行 %d・§6 と §6-補 を除く）・正本: `%s`（説明文 %d 件）・設計定数の種類 %d' % (os.path.relpath(a.doc).replace('\\', '/'), checked_lines, os.path.relpath(a.json).replace('\\', '/'), len(STRS), len(CONST)),
     '- 未登録の数: 本文 %d・正本の説明文 %d' % (len(doc_bad), len(json_bad)), '']
for i, tok, ctx in doc_bad:
    R.append('- 本文 %d 行: `%s` … %s' % (i, tok, ctx.replace('`', "'")))
for path, tok, ctx in json_bad:
    R.append('- 正本 %s: `%s` … %s' % (path, tok, ctx.replace('`', "'")))
R += ['', '本ファイルのいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
if a.report:
    os.makedirs(os.path.dirname(a.report), exist_ok=True); open(a.report, 'w', encoding='utf-8', newline='\n').write('\n'.join(R) + '\n')
print('\n'.join(R[:4 + min(40, len(doc_bad) + len(json_bad))]))
sys.exit(1 if (doc_bad or json_bad) else 0)
