# -*- coding: utf-8 -*-
"""numbers_lint.py v2 —— 設計文書・正本・生成器の数を機械検査する（凍結前検分の採否表 P8・P53〜P58・登録者裁定 D15・2026-09-13・v1 は claude.ai 三票の採否表 C36）。
三つの検査:
 (1) 束縛検査（--src）: 原稿の本文（§6 の転記行の置き場と §6-補 を除く全節）で、数は正本のキー参照 {{…}} か構造でなければならない。キー参照の外に残る数は、正本に登録された値でも「未束縛」として止める。キー参照は正本に実在しなければ止める。
 (2) 登録検査（--doc と --json）: 組み立て後の文書（§6 と §6-補 を除く）と正本の説明文に、正本の数値の葉と配列の長さのどれにも当たらない数が無いか（v1 と同じ・未登録）。
 (3) 生成器の文字列リテラル検査（--gen）: 生成器のソースの文字列リテラル（書式指定と書式欄を除く・式や識別子のキーの値は除く・docstring は除く）に、構造でない数が残っていないか（採否表 P54・P55・P57）。
構造＝節番号・日付・時刻・版・草案番号・門の番号・裁定と採否表と追い問いの番号（D・C・V・E・J・K・P・W）・機種名・GPU 名・場面名・SHA・コミット・行頭の番号・code span・パス・URL・0/1 など（数として読まない）。
キー参照の書式: {{a/b/c}}（JSON のキーを / で区切る・配列は添字）・{{len:a/b}}（配列や辞書の長さ）・{{…|,}}（三桁区切り）・{{…|%}}（百倍の整数）。
限界（報告に印字）: 束縛した数は正本の値に置換されるので、値の取り違えは束縛の対応を誤ったときにしか起きない。構造として除外した型の数は検査しない。正本の値そのものが設計として正しいかは検査しない。
用法: python tools/numbers_lint.py --json design/contrasts-A.json [--src 原稿] [--doc 文書 ...] [--gen 生成器.py ...] [--report md]・自己検査: --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, json, argparse
VERSION = 'v2.1'   # v2.1（2026-09-14・採否表 P121・P126）: 生成器の検査で自己検査の関数の中の文字列を除き、限界に記す（組み立て器の既定の範囲に格子の器・共有関数・組み立て器を足した）
SKIP_CONST = {'bases_4B2507_api', 'contrasts', 'seeds', 'label_combo_table'}
SKIP_STR = SKIP_CONST | {'formula', 'z', 'cp_upper_rule', 'R_control', 'arms_string', 'id', 'src', 'base_src', 'sha16', 'generator', 'version', 'compared_sources', 'tags', 'models', 'value_word_ban', 'mechanism_word_ban',
                         'weights_formula', 'se_formula', 'interval_formula', 'iut_p', 'holm_rule', 'test', 'python_control', 'runner_sha', 'arm_coding', 'gate'}
MASKS = [r'`[^`]*`', r'https?://\S+', r'SHA-?(?:256|16)', r'(?:records|design|tools|results|arms|prompts)/[\w\-./]+', r'\b[0-9A-F]{16}\b', r'\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b',
         r'\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?(?:\s*UTC)?', r'\b\d{1,2}:\d{2}\b', r'§\s*\d+(?:[.\-]\d+)*(?:-補)?', r'^#{1,6}\s+\d+(?:\.\d+)*(?:-補)?',
         r'\bv\d+(?:\.\d+)*', r'草案\s?\d+[AB]?', r'第[一二三四五六七八九十〇\d]+[章節巡票部段]', r'(?<![A-Za-z])[DCVEJKPW]\d+(?:〜[DCVEJKPW]?\d+)?(?![\d.])', r'\(\d+[a-z]\)',
         r'\b(?:I|F)-\d+\b', r'F\s?§0-\d+', r'Qwen\d*(?:[-/][\w.]+)*', r'(?<![\w.])\d+(?:\.\d+)?B(?:-\d{4})?(?![\w])', r'\b(?:L4|T4|A100(?:-SXM4-80GB)?|H100)\b', r'\b\d+\s?GB\b',
         r'\b(?:N1|N2|S1|S4|SK|Odose1|T2)\b', r'\b(?:bf16|fp16|[Uu][Tt][Ff]-8|cp932)\b', r'(?:Gemini|Grok|Opus|Fable|Sonnet|Haiku|Claude|Llama|vLLM|torch|transformers|Python|numpy|scipy)\s*[\d.]+(?:\s*(?:Flash|Pro))?',
         r'\b\d+(?:\.\d+){2,}\b', r'^\s*\d+\.\s', r'(?<![\d.])\d+\.(?=\s)', r'\b\d+[x×]\d+\b', r'β[₀-₉]', r'stage[A-Z][\w\-]*', r'\bD-\d+\b', r'#\d+', r'\((?:19|20)\d{2}\)', r'(?:19|20)\d{2}(?=\s*Stat|\s*Biometrika)',
         r'門\d+(?:\.\d+)?', r'\b0/1\b', r'段\s?\d', r'\{\{[^{}]*\}\}']
MASK_RE = [re.compile(p, re.M) for p in MASKS]
FMT_RE = [re.compile(r'%[-+ #0]*\d*(?:\.\d+)?[sdfegrxiXEG%]'), re.compile(r'\{[A-Za-z_][A-Za-z0-9_]*(?::[^{}]*)?\}')]
NUM = re.compile(r'(?<![A-Za-z0-9_.,])[−\-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?')
KEY_RE = re.compile(r'\{\{([^{}|]+)(?:\|([^{}]+))?\}\}')
nz = lambda v: '%.10g' % float(v)
LIMIT = '本器は、原稿の数がキー参照か構造であること（束縛）・文書と正本の説明文の数が正本に登録されていること（登録）・生成器の文字列リテラルに構造でない数が無いこと（生成器）を見る。束縛した数は正本の値に置換されるので、値の取り違えは束縛の対応を誤ったときにしか起きない。構造として除外した型（節番号・日付・版・機種名など）の数は検査しない。正本の値そのものが設計として正しいかは検査しない。生成器の検査は docstring と自己検査の関数（_selftest）の中の文字列を検査しない（出力に届かない・採否表 P126）。'


def const_set(J):
    C = set()

    def walk(x, key=None):
        if key in SKIP_CONST or x is None or isinstance(x, bool) or (key == 'cells' and isinstance(x, list)):
            return
        if isinstance(x, (int, float)):
            C.add(nz(x)); return
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, k)
        elif isinstance(x, list):
            C.add(nz(len(x)))
            for v in x:
                walk(v, key)
    walk(J)
    return C


def json_strings(J):
    S = []

    def walk(x, path, key=None):
        if key in SKIP_STR or (key == 'cells' and isinstance(x, list)):
            return
        if isinstance(x, str):
            S.append((path, x)); return
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, path + '.' + k, k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, '%s[%d]' % (path, i), key)
    walk(J, '$')
    return S


def masked(text, extra=()):
    t = text
    for rx in list(extra) + MASK_RE:
        t = rx.sub(lambda m: ' ' * len(m.group(0)), t)
    return t


def numbers(text, extra=()):
    t = masked(text, extra); out = []
    for m in NUM.finditer(t):
        tok = m.group(0); raw = tok.replace(',', '').replace('−', '-').rstrip('%')
        try:
            out.append((tok, float(raw), m.start(), m.end()))
        except ValueError:
            continue
    return out


def resolve(J, spec):
    """キー参照を正本の値に解く。戻り値: (値, エラー)。"""
    s = spec.strip(); want_len = s.startswith('len:')
    if want_len:
        s = s[4:]
    x = J
    for seg in s.split('/'):
        if isinstance(x, dict) and seg in x:
            x = x[seg]
        elif isinstance(x, list) and re.fullmatch(r'\d+', seg) and int(seg) < len(x):
            x = x[int(seg)]
        else:
            return None, 'キー参照が正本に無い: %s' % spec
    if want_len:
        if not isinstance(x, (list, dict)):
            return None, 'len: の対象が配列でも辞書でもない: %s' % spec
        return len(x), None
    return x, None


def fmt_value(v, f):
    if isinstance(v, bool):
        return str(v)
    if f == ',':
        return format(int(v), ',') if float(v).is_integer() else format(float(v), ',')
    if f == '%':
        return '%d' % round(float(v) * 100)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return '%g' % v
    return str(v)


def bind(J, text):
    """{{…}} を正本の値で置換。戻り値: (置換後, 使ったキーの一覧, エラーの一覧)。"""
    used = []; errs = []

    def rep(m):
        v, e = resolve(J, m.group(1))
        if e:
            errs.append(e); return m.group(0)
        used.append(m.group(1).strip()); return fmt_value(v, (m.group(2) or '').strip())
    return KEY_RE.sub(rep, text), used, errs


def body_lines(text):
    """§6（転記行の置き場）と §6-補 を除く行（行番号つき）。"""
    in6 = False
    for i, l in enumerate(text.replace('\r\n', '\n').split('\n'), 1):
        if l.startswith('## 6.'):
            in6 = True; continue
        if l.startswith('## 7.'):
            in6 = False
        if not in6:
            yield i, l


def check_src(J, text):
    bad = []
    for i, l in body_lines(text):
        for m in KEY_RE.finditer(l):
            _, e = resolve(J, m.group(1))
            if e:
                bad.append((i, m.group(0), e))
        for tok, v, s0, s1 in numbers(l):
            bad.append((i, tok, '未束縛の数 … ' + l[max(0, s0 - 24):s1 + 24].replace('`', "'")))
    return bad


def check_doc(J, text, C=None):
    C = C or const_set(J); bad = []
    for i, l in body_lines(text):
        for tok, v, s0, s1 in numbers(l):
            if not (nz(v) in C or nz(abs(v)) in C or (tok.endswith('%') and nz(v / 100) in C)):
                bad.append((i, tok, '未登録 … ' + l[max(0, s0 - 24):s1 + 24].replace('`', "'")))
    return bad


def check_json(J, C=None):
    C = C or const_set(J); bad = []
    for path, s in json_strings(J):
        for tok, v, s0, s1 in numbers(s):
            if not (nz(v) in C or nz(abs(v)) in C or (tok.endswith('%') and nz(v / 100) in C)):
                bad.append((path, tok, s[max(0, s0 - 24):s1 + 24]))
    return bad


def check_gen(path):
    src = open(path, encoding='utf-8').read(); tree = ast.parse(src); skip_nodes = set(); bad = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], 'value', None), ast.Constant) and isinstance(node.body[0].value.value, str):
            skip_nodes.add(id(node.body[0].value))
        if isinstance(node, ast.FunctionDef) and node.name == '_selftest':   # 自己検査の関数の中の文字列は出力に届かない（限界に記す・採否表 P126）
            for sub in ast.walk(node):
                skip_nodes.add(id(sub))
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value in SKIP_STR:
                    for sub in ast.walk(v):
                        skip_nodes.add(id(sub))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip_nodes:
            for tok, v, s0, s1 in numbers(node.value, extra=FMT_RE):
                bad.append((node.lineno, tok, node.value[max(0, s0 - 20):s1 + 20].replace('\n', ' ')))
    return bad


def report(J, jpath, src=None, docs=(), gens=()):
    C = const_set(J); out = {'src': [], 'doc': {}, 'json': check_json(J, C), 'gen': {}}
    if src:
        out['src'] = check_src(J, open(src, encoding='utf-8').read())
    for d in docs:
        out['doc'][d] = check_doc(J, open(d, encoding='utf-8').read(), C)
    for g in gens:
        out['gen'][g] = check_gen(g)
    rel = lambda p: os.path.relpath(p).replace('\\', '/')
    n_bad = len(out['src']) + sum(len(v) for v in out['doc'].values()) + len(out['json']) + sum(len(v) for v in out['gen'].values())
    L = ['# 数の機械検査（機械生成・`tools/numbers_lint.py` %s）' % VERSION, '', '- 正本: `%s`（説明文 %d 件・設計定数の種類 %d）' % (rel(jpath), len(json_strings(J)), len(C))]
    if src:
        L.append('- 束縛検査（原稿 `%s`）: 違反 %d' % (rel(src), len(out['src'])))
    for d, v in out['doc'].items():
        L.append('- 登録検査（文書 `%s`・§6 と §6-補 を除く）: 未登録 %d' % (rel(d), len(v)))
    L.append('- 登録検査（正本の説明文）: 未登録 %d' % len(out['json']))
    for g, v in out['gen'].items():
        L.append('- 生成器の文字列リテラル検査（`%s`）: 構造でない数 %d' % (rel(g), len(v)))
    L += ['- 違反の合計: %d' % n_bad, '- 限界: ' + LIMIT, '']
    for i, tok, ctx in out['src']:
        L.append('- 原稿 %d 行: `%s` … %s' % (i, tok, ctx))
    for d, v in out['doc'].items():
        for i, tok, ctx in v:
            L.append('- 文書 %s %d 行: `%s` … %s' % (rel(d), i, tok, ctx))
    for path, tok, ctx in out['json']:
        L.append('- 正本 %s: `%s` … %s' % (path, tok, ctx.replace('`', "'")))
    for g, v in out['gen'].items():
        for i, tok, ctx in v:
            L.append('- 生成器 %s %d 行: `%s` … %s' % (rel(g), i, tok, ctx.replace('`', "'").replace('|', '｜')))
    L += ['', '本ファイルのいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
    return n_bad, L


def _selftest():
    J = {'a': {'b': 12, 'c': [0.03, 0.08]}, 'n': 2048, 'f': 0.3, 'lst': [1, 2, 3]}
    # マスクの検査例（採否表 P8）: 構造は数として読まない・構造でない数は読む
    cases = [('裁定 D1〜D15 と P1〜P74 と W32', 0), ('門0.5 と門2', 0), ('§2.4 の 0/1', 0), ('Qwen3-4B と 4B-2507 と A100 80GB', 0), ('2026-09-13 と v2.7', 0), ('草案7 と 第三章', 0),
             ('帯は 12 pt', 1), ('n=200', 1), ('30%', 1), ('D100 と C20', 0), ('X1 と 1.5 GiB', 1)]
    for text, k in cases:
        got = len(numbers(text)); assert got == k, (text, got, k)
    t, used, errs = bind(J, '帯は {{a/b}} pt・{{a/c/0}}／{{a/c/1}}・{{n|,}} トークン・{{f|%}}%・{{len:lst}} 腕')
    assert t == '帯は 12 pt・0.03／0.08・2,048 トークン・30%・3 腕' and not errs, (t, errs)
    assert check_src(J, '帯は {{a/b}} pt・{{a/x}}') and len(check_src(J, '帯は 12 pt')) == 1 and not check_src(J, '帯は {{a/b}} pt')
    assert not check_doc(J, t)
    print('numbers_lint.py %s SELFTEST PASS（マスクの検査例 %d・束縛・未束縛・登録）' % (VERSION, len(cases)))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    ap = argparse.ArgumentParser(); ap.add_argument('--json', required=True); ap.add_argument('--src', default=None); ap.add_argument('--doc', nargs='*', default=[]); ap.add_argument('--gen', nargs='*', default=[]); ap.add_argument('--report', default=None)
    a = ap.parse_args(); Jd = json.load(open(a.json, encoding='utf-8'))
    nb, L = report(Jd, a.json, a.src, a.doc, a.gen)
    if a.report:
        os.makedirs(os.path.dirname(a.report), exist_ok=True); open(a.report, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    print('\n'.join(L[:12 + min(60, nb)]))
    sys.exit(1 if nb else 0)
