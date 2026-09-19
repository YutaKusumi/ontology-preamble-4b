# -*- coding: utf-8 -*-
"""build_draftB.py v3 —— 段階 B の草案（と報告雛形）を原稿から組み立てる（段階 A の `build_draftA.py` の型・凍結した A の器は触らない）。
- **一覧の展開**（v2・2026-09-19）: 原稿の行 `{{list:正本のキー}}` を、正本の一覧の各項目の箇条に展開する（開示の五項目を依頼文と草案が同じ出所から組むため・裁定 D117）。
- **裁定の台帳の検査**（v2・採否表 P376）: 原稿が引く裁定番号がすべて正本 `decisions` にあることを確かめ、無ければ止める。
  数の走査器 `numbers_lint.py` は段階 A の凍結した器なので、この検査はそちらに足さず、B の組み立て器に置く。
- **採否表の引用の照合**（v3・2026-09-19）: 組み上げた文書・正本・器材の「採否表 P…」を `tools/citations_B.py` で採否表と照らし、
  違反があれば終了コードを立てる（束の前の点検で、手で打った引用の誤りが多数見つかったため）。
- 組み立ての前に `numbers_lint` の束縛検査（原稿の数はキー参照か構造）を走らせ、違反があれば止める。
- 原稿の {{正本のキー}} を正本 JSON の値で置換する。
- 草案（--kind draft）: §6 の「- **転記行 X** — 〔転記行 X〕」を設計事実 JSON の逐語で置換し、本文中の〔転記行 X〕を「〔転記行 X・§6〕」に改め、§6-補 に置換の記録を印字する。
- 組み立ての後に登録検査（文書と正本の説明文）と生成器の文字列リテラル検査を走らせ、報告を書く。違反があれば終了コードを立てる。
用法: python tools/build_draftB.py --kind draft --src design/design-stageB-draft5.src.md --out design/design-stageB-draft5.md --label 草案5B --lint-report records/B/numbers-lint-draft5B.md
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numbers_lint as NL
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--kind', choices=['draft', 'template'], required=True)
ap.add_argument('--src', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--label', required=True)
ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'B', 'design-facts-B.json'))
ap.add_argument('--facts-md', default=os.path.join(REPO, 'records', 'B', 'design-facts-B.md'))
ap.add_argument('--json', default=os.path.join(REPO, 'design', 'contrasts-B.json'))
ap.add_argument('--lint-report', required=True)
ap.add_argument('--gen', nargs='*', default=[os.path.join(REPO, 'tools', nm) for nm in ('make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py')])
a = ap.parse_args()
sha = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
rel = lambda p: os.path.relpath(p, REPO).replace('\\', '/')
J = json.load(open(a.json, encoding='utf-8'))
s = open(a.src, encoding='utf-8').read().replace('\r\n', '\n')

# ---- 一覧の展開（v2） ----
def _expand(m):
    v, e = NL.resolve(J, m.group(1))
    if e or not isinstance(v, list) or not v:
        sys.exit('一覧の展開に失敗した（正本に一覧が無いか空）: %s' % m.group(0))
    return '\n'.join('- %s' % x for x in v)


s = re.sub(r'^\{\{list:([^{}]+)\}\}$', _expand, s, flags=re.M)

# ---- 裁定の台帳の検査（v2・採否表 P376） ----
LED = set((J.get('decisions') or {}).keys())
_refs = {('D%s%s' % (m.group(1), m.group(2) or ''), 'D%s' % m.group(1))
         for m in re.finditer(r'(?<![A-Za-z\d])D(\d+)(?:\s*\(([a-z])\))?', s)}
_bad_led = sorted({full for full, bare in _refs if full not in LED and bare not in LED})
if _bad_led:
    sys.exit('原稿が引く裁定番号が正本の台帳（decisions）に無い: %s' % '・'.join(_bad_led))

pre = NL.check_src(J, s)
if pre:
    print('[build_draftB] 束縛検査で止めた（原稿の数がキー参照か構造でない・%d 件）' % len(pre))
    for i, tok, ctx in pre[:80]:
        print('  原稿 %d 行: %s … %s' % (i, tok, ctx))
    sys.exit(1)
bound, used, errs = NL.bind(J, s)
assert not errs, errs

out, replaced = [], []
if a.kind == 'draft':
    FJ = json.load(open(a.facts, encoding='utf-8'))
    F = FJ['facts']
    assert FJ['contrasts_sha16'] == sha(a.json), ('設計事実の正本 SHA16 と現行の正本が不一致', FJ['contrasts_sha16'], sha(a.json))
    in6 = False
    for l in bound.split('\n'):
        if l.startswith('## 6.'):
            in6 = True
            out.append('## 6. 転記行（機械生成・逐語・`%s`〔SHA16 %s〕・`%s`〔SHA16 %s〕・生成 %s UTC・器 `tools/design_facts_B.py`）'
                       % (rel(a.facts_md), sha(a.facts_md), rel(a.json), FJ['contrasts_sha16'], FJ['generated_utc']))
            continue
        if in6 and l.startswith('## 7.'):
            in6 = False
            out += ['### 6-補 原稿 → %s の組み立ての記録（機械）' % a.label, '',
                    '- 置換した転記行: %s（器 `tools/build_draftB.py`・原稿 `%s` SHA16 %s）。本文中の転記行の置き字は §6 への参照に改めた。' % ('・'.join(replaced), rel(a.src), sha(a.src)),
                    '- 束縛: 原稿のキー参照を正本 `%s`（SHA16 %s）の値で置換した（異なるキーの種類は下の検査の記録に印字する）。組み立ての前に束縛検査、後に登録検査と生成器の文字列の検査を走らせた（`%s`）。' % (rel(a.json), sha(a.json), rel(a.lint_report)),
                    '- 数値の出所はすべて正本と設計事実の JSON であり、散文に手計算の数を残さない。', '', l]
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
else:
    out = bound.split('\n')

t = '\n'.join(out)
assert not re.search(r'〔転記行 [A-Z]〕', t), '置き残しがある'
assert not re.search(r'\{\{[^{}]*\}\}', t), '束縛の置き残しがある'
open(a.out, 'w', encoding='utf-8', newline='\n').write(t)
print('[build_draftB] written %s sha16 %s | 転記行 %s | 束縛したキーの種類 %d' % (rel(a.out), sha(a.out), ''.join(replaced) or '—', len(used)))
# 束縛検査は**一覧を展開した後の原稿**に当てる（展開の印そのものは正本のキー参照ではない・v2）。
# 展開した原稿は一時の置き場に書き、検査の記録の中の置き場の名は元の原稿の名に戻す。
import tempfile as _tf
_d = _tf.mkdtemp(prefix='draftB_')
_exp = os.path.join(_d, os.path.basename(a.src))
open(_exp, 'w', encoding='utf-8', newline='\n').write(s)
nb, L = NL.report(J, a.json, _exp, [a.out], a.gen)
L = [l.replace(os.path.relpath(_exp).replace('\\', '/'), rel(a.src) + '（一覧を展開した後）') for l in L]
import shutil as _sh
_sh.rmtree(_d, ignore_errors=True)
os.makedirs(os.path.dirname(a.lint_report), exist_ok=True)
open(a.lint_report, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('\n'.join(L[:12 + min(60, nb)]))
# ---- 採否表の引用の照合（v3） ----
import citations_B as _CB
_cv, _ct = _CB.check_all(REPO, docs=[rel(a.out)])
print('[build_draftB] 採否表の引用の照合（`tools/citations_B.py` %s）: 引用 %d・裁定の照合 %d・札の照合 %d・違反 %d'
      % (_CB.VERSION, _ct['cit'], _ct['d'], _ct['label'], len(_cv)))
for _w, _p, _y in _cv[:40]:
    print('  違反: %s %s —— %s' % (_w, _p, _y))
sys.exit(1 if (nb or _cv) else 0)
