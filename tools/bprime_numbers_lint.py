# -*- coding: utf-8 -*-
"""bprime_numbers_lint.py v0（2026-09-30・B′ の数の機械検査・凍結した `tools/numbers_lint.py` v2.1 を呼ぶ包み・コーディネータ南無弥勒如来）。
凍結した器は変えない。B′ の文書に出る構造の数（採否の表の行の印〔R〕〔S〕〔T〕・案の番号・機種名・GPU の名・問いと版の番号・模型の版など）を、構造として読まない型を外から足して、
登録検査（文書の数と正本の説明文の数が、正本の数値の葉か配列の長さに当たるか）を掛ける。束縛検査（原稿の {{…}}）は凍結の本文を組む段で同じ包みを使う。
用法: python tools/bprime_numbers_lint.py --json design/contrasts-Bprime.json [--doc 文書 ...] [--report md]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, io, json, argparse
PUB = os.environ.get('OP4B_PUBLIC_REPO', 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b')
sys.path.insert(0, os.path.join(PUB, 'tools'))
import numbers_lint as N0                                                   # 凍結の器（読むだけ・呼ぶだけ）

EXTRA = [re.compile(p, re.M) for p in [
    r'(?<![A-Za-z])[RST]\d\d(?:〜[RST]?\d\d)?(?![\d.])',              # 採否の表の行の印（R01〜R41・S01〜S29・T01〜T33）
    r'案\s?\d+(?:〜\d+)?(?:・\d+(?:〜\d+)?)*', r'【案\s?\d+】',                  # 案の番号（「案 19〜21・23」の続きを含む）
    r'(?<![\d.])9\.[1-4](?![\d.])', r'\$[\w.\[\]]+', r'^\d+\.\d+$',          # § の付かない節の番号（9.1〜9.4）・JSON の道筋・版の数だけの文
    r'[Gg]emma-\d+(?:-[\w.]+)*', r'\b\d+B-A\d+B\b', r'grok-\d+(?:\.\d+)?', r'\bG4\b', r'RTX PRO \d+', r'Apache \d\.\d',
    r'\bq\d(?:〜q\d)?', r'\bV\d(?:〜V\d)?', r'\bA\d-\d+\b', r'\bG\d-\d+\b', r'\bD\d{3}\b',
    r'cu\d+', r'\bLF\b', r'Gemma4RMSNorm', r'Ryokai-OS',
]]


def check_doc(J, text, C):
    bad = []
    for i, l in N0.body_lines(text):
        for tok, v, s0, s1 in N0.numbers(l, EXTRA):
            if not (N0.nz(v) in C or N0.nz(abs(v)) in C or (tok.endswith('%') and N0.nz(v / 100) in C)):
                bad.append((i, tok, l[max(0, s0 - 24):s1 + 24]))
    return bad


def check_json(J, C):
    bad = []
    for path, s in N0.json_strings(J):
        for tok, v, s0, s1 in N0.numbers(s, EXTRA):
            if not (N0.nz(v) in C or N0.nz(abs(v)) in C or (tok.endswith('%') and N0.nz(v / 100) in C)):
                bad.append((path, tok, s[max(0, s0 - 24):s1 + 24]))
    return bad


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ap = argparse.ArgumentParser(); ap.add_argument('--json', required=True); ap.add_argument('--doc', nargs='*', default=[]); ap.add_argument('--report', default=None)
    a = ap.parse_args()
    J = json.load(open(a.json, encoding='utf-8'))
    C = N0.const_set(J)
    L = ['# 数の機械検査（B′・機械生成・`tools/bprime_numbers_lint.py` が凍結の `numbers_lint.py` %s を呼んだ）' % N0.VERSION, '',
         '- 正本: `%s`（説明文 %d 件・設計定数の種類 %d）' % (a.json, len(N0.json_strings(J)), len(C))]
    bj = check_json(J, C)
    L.append('- 登録検査（正本の説明文）: 未登録 %d' % len(bj))
    bd = {}
    for d in a.doc:
        bd[d] = check_doc(J, open(d, encoding='utf-8').read(), C)
        L.append('- 登録検査（文書 `%s`・§6 を除く）: 未登録 %d' % (d, len(bd[d])))
    L += ['- 限界: ' + N0.LIMIT + ' B′ の包みは、構造として読まない型（採否の表の行の印・案の番号・機種名など）を足しただけで、判定の式は凍結の器のまま。', '']
    for path, tok, ctx in bj:
        L.append('- 正本 %s: `%s` … %s' % (path, tok, ctx.replace('`', "'")))
    for d, v in bd.items():
        for i, tok, ctx in v:
            L.append('- 文書 %s %d 行: `%s` … %s' % (d, i, tok, ctx.replace('`', "'")))
    L += ['', '本ファイルのいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。']
    if a.report:
        open(a.report, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    print('\n'.join(L[:8 + 80]))
    return len(bj) + sum(len(v) for v in bd.values())


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
