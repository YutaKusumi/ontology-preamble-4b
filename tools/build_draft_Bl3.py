# -*- coding: utf-8 -*-
"""build_draft_Bl3.py v2 —— B-lens 層三（Bl3）の草案を原稿から組み立てる（B-lens の `build_draft_Blens.py` の型・凍結した B-lens の器は触らない）。
- 原稿の行 `{{list:正本のキー}}` を、正本の一覧の各項目の箇条に展開する（行頭の字下げは各項目に引き継ぐ・v2）。`{{reading_table}}` は読みの表、`{{predictions_list}}` は予想の項目に展開する。
- 原稿が引く裁定番号がすべて正本 `decisions` にあることを確かめ、無ければ止める。
- 組み立ての前に、凍結した `tools/numbers_lint.py` の束縛検査（原稿の数は正本のキー参照か構造）を走らせ、違反があれば止める。
- 原稿の {{正本のキー}} を正本の値で置換し、§6 の「- **転記行 X** — 〔転記行 X〕」を設計事実の JSON の逐語で置換する。
- 組み立ての後に、登録検査（文書と正本の説明文）と生成器の文字列リテラル検査を走らせ、報告を書く。違反があれば終了コードを立てる。
用法: python tools/build_draft_Bl3.py --src design/design-Bl3-draft1.src.md --out design/design-Bl3-draft1.md --label 草案1 --lint-report records/Bl3/numbers-lint-draft1-Bl3.md
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, argparse, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numbers_lint as NL

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--label', required=True)
ap.add_argument('--json', default=os.path.join(REPO, 'design', 'contrasts-Bl3.json'))
ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'))
ap.add_argument('--facts-md', default=os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.md'))
ap.add_argument('--lint-report', required=True)
ap.add_argument('--gen', nargs='*', default=[os.path.join(REPO, 'tools', n) for n in ('make_contrasts_Bl3.py', 'bl3_facts.py', 'build_draft_Bl3.py')])
a = ap.parse_args()
sha = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
rel = lambda p: os.path.relpath(p, REPO).replace('\\', '/')
J = json.load(open(a.json, encoding='utf-8'))
s = open(a.src, encoding='utf-8').read().replace('\r\n', '\n')


def _expand(m):
    v, e = NL.resolve(J, m.group(2))
    if e or not isinstance(v, list) or not v:
        sys.exit('一覧の展開に失敗した（正本に一覧が無いか空）: %s' % m.group(0))
    return '\n'.join('%s- %s' % (m.group(1), x) for x in v)


cell = lambda x: str(x).replace('|', '｜')
READ = ['| 型 | 条件 | 書くこと | 外でないとき書くこと | 書かないこと |', '|---|---|---|---|---|'] + [
    '| %s | %s | %s | %s | %s |' % (cell(r['type']), cell(r['condition']), cell(r['write']), cell(r['write_if_not']), '・'.join(r['never'])) for r in J['reading_rules']]
PRED = ['- `%s`: %s（選べるもの: %s）' % (x['key'], x['ask'], '／'.join(x['options'])) for x in J['predictions']['items']]
s = re.sub(r'^( *)\{\{list:([^{}]+)\}\}$', _expand, s, flags=re.M)
s = re.sub(r'^\{\{reading_table\}\}$', lambda m: '\n'.join(READ), s, flags=re.M)
s = re.sub(r'^( *)\{\{predictions_list\}\}$', lambda m: '\n'.join(m.group(1) + x for x in PRED), s, flags=re.M)
LED = set((J.get('decisions') or {}).keys())
bad_led = sorted({'D%s' % m.group(1) for m in re.finditer(r'(?<![A-Za-z\d])D(\d+)', s)} - LED)
if bad_led:
    sys.exit('原稿が引く裁定番号が正本の台帳（decisions）に無い: %s' % '・'.join(bad_led))
pre = NL.check_src(J, s)
if pre:
    print('[build_draft_Bl3] 束縛検査で止めた（原稿の数がキー参照か構造でない・%d 件）' % len(pre))
    for i, tk, ctx in pre[:80]:
        print('  原稿 %d 行: %s … %s' % (i, tk, ctx))
    sys.exit(1)
bound, used, errs = NL.bind(J, s)
assert not errs, errs
FJ = json.load(open(a.facts, encoding='utf-8'))
F = FJ['facts']
assert FJ['contrasts_sha16'] == sha(a.json), ('設計事実の正本 SHA16 と現行の正本が不一致', FJ['contrasts_sha16'], sha(a.json))
out, replaced, in6 = [], [], False
for l in bound.split('\n'):
    if l.startswith('## 6.'):
        in6 = True
        out.append('## 6. 転記行（機械生成・逐語・`%s`〔SHA16 %s〕・正本 `%s`〔SHA16 %s〕・生成 %s UTC・器 `tools/bl3_facts.py`）'
                   % (rel(a.facts_md), sha(a.facts_md), rel(a.json), FJ['contrasts_sha16'], FJ['generated_utc']))
        continue
    if in6 and l.startswith('## 7.'):
        in6 = False
        out += ['### 6-補 原稿 → %s の組み立ての記録（機械）' % a.label, '',
                '- 置換した転記行: %s（器 `tools/build_draft_Bl3.py`・原稿 `%s` SHA16 %s）。本文中の転記行の置き字は §6 への参照に改めた。' % ('・'.join(replaced), rel(a.src), sha(a.src)),
                '- 束縛: 原稿のキー参照を正本 `%s`（SHA16 %s）の値で置換した。組み立ての前に束縛検査、後に登録検査と生成器の文字列リテラル検査を走らせた（記録 `%s`）。' % (rel(a.json), sha(a.json), rel(a.lint_report)),
                '- 数の出所はすべて正本と設計事実の JSON であり、散文に手で打った数を残さない。', '', l]
        continue
    if in6:
        m = re.match(r'^- \*\*転記行 ([A-Z])\*\* — 〔転記行 ([A-Z])〕$', l)
        if m:
            assert m.group(1) == m.group(2), l
            k = m.group(1)
            assert k in F, ('設計事実に無い転記行', k)
            out.append('- **転記行 %s** — %s' % (k, F[k]['text']))
            replaced.append(k)
            continue
        out.append(l)
        continue
    out.append(re.sub(r'〔転記行 ([A-Z])〕', lambda mm: '〔転記行 %s・§6〕' % mm.group(1), l))
missing = [k for k in F if k not in replaced]
assert not missing, ('§6 に置かれていない転記行', missing)
t = '\n'.join(out)
assert not re.search(r'〔転記行 [A-Z]〕', t), '置き残しがある'
assert not re.search(r'\{\{[^{}]*\}\}', t), '束縛の置き残しがある'
open(a.out, 'w', encoding='utf-8', newline='\n').write(t)
print('[build_draft_Bl3] written %s sha16 %s | 転記行 %s | 束縛したキーの種類 %d' % (rel(a.out), sha(a.out), ''.join(replaced), len(set(used))))
d = tempfile.mkdtemp(prefix='draftBl3_')
exp = os.path.join(d, os.path.basename(a.src))
open(exp, 'w', encoding='utf-8', newline='\n').write(s)
nb, L = NL.report(J, a.json, exp, [a.out], a.gen)
L = [l.replace(os.path.relpath(exp).replace('\\', '/'), rel(a.src) + '（一覧を展開した後）') for l in L]
shutil.rmtree(d, ignore_errors=True)
os.makedirs(os.path.dirname(a.lint_report), exist_ok=True)
open(a.lint_report, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('\n'.join(L[:12 + min(60, nb)]))
sys.exit(1 if nb else 0)
