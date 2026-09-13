# -*- coding: utf-8 -*-
"""build_draftA.py v1 —— 段階 A の草案と報告雛形を原稿から組み立てる（build_draft5A.py の後継・版に依らない名・凍結前検分の採否表 P7・P57・P58・登録者裁定 D15・2026-09-13）。
- 組み立ての前に numbers_lint の束縛検査（原稿の数はキー参照か構造）を走らせる。
- 原稿の {{正本のキー}} を正本 JSON の値で置換する（書式は | で指定・`tools/numbers_lint.py` の bind）。
- 草案（--kind draft）: §6 の「- 〔転記行 X〕」を設計事実 JSON の逐語で置換し、本文中の〔転記行 X〕を「〔転記行 X・§6〕」に改め、§6-補 に置換の記録（転記行・束縛したキーの数と種類）を印字する。雛形（--kind template）は §6 を持たない。
- 組み立ての後に登録検査（文書と正本の説明文）と生成器の文字列リテラル検査（make_contrasts_A.py・design_facts_A.py）を走らせ、記録を書く。どれかに違反があれば非零で終了する。
用法: python tools/build_draftA.py --kind draft --src design/design-stageA-draft7.src.md --out design/design-stageA-draft7.md --label 草案7 --lint-report records/A/numbers-lint-draft7A.md
      python tools/build_draftA.py --kind template --src records/A/results-report-template-A.src.md --out records/A/results-report-template-A.md --label 報告雛形 --lint-report records/A/numbers-lint-template-A.md
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numbers_lint as NL
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--kind', choices=['draft', 'template'], required=True); ap.add_argument('--src', required=True); ap.add_argument('--out', required=True); ap.add_argument('--label', required=True)
ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); ap.add_argument('--facts-md', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.md'))
ap.add_argument('--json', default=os.path.join(REPO, 'design', 'contrasts-A.json')); ap.add_argument('--lint-report', required=True)
ap.add_argument('--gen', nargs='*', default=[os.path.join(REPO, 'tools', 'make_contrasts_A.py'), os.path.join(REPO, 'tools', 'design_facts_A.py')])
a = ap.parse_args()
sha = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
rel = lambda p: os.path.relpath(p, REPO).replace('\\', '/')
J = json.load(open(a.json, encoding='utf-8')); s = open(a.src, encoding='utf-8').read().replace('\r\n', '\n')
pre = NL.check_src(J, s)
if pre:
    print('[build_draftA] 束縛検査で止めた（原稿の数がキー参照か構造でない・%d 件）' % len(pre))
    for i, tok, ctx in pre[:60]:
        print('  原稿 %d 行: %s … %s' % (i, tok, ctx))
    sys.exit(1)
bound, used, errs = NL.bind(J, s); assert not errs, errs
out = []; replaced = []
if a.kind == 'draft':
    FJ = json.load(open(a.facts, encoding='utf-8')); F = FJ['facts']
    assert FJ['contrasts_sha16'] == sha(a.json), ('設計事実の正本 SHA16 と現行の正本が不一致', FJ['contrasts_sha16'], sha(a.json))
    assert not FJ.get('dev_marks'), ('検査用の印つきの設計事実は組み立てに使わない', FJ.get('dev_marks'))
    in6 = False
    for l in bound.split('\n'):
        if l.startswith('## 6.'):
            in6 = True
            out.append('## 6. 転記行（機械生成・逐語・`%s`〔SHA16 %s〕・`%s`〔SHA16 %s〕・`records/A/power-grid-A.json`〔SHA16 %s〕・生成 %s UTC）' % (rel(a.facts_md), sha(a.facts_md), rel(a.json), FJ['contrasts_sha16'], FJ['power_grid_json_sha16'], FJ['generated_utc']))
            continue
        if in6 and l.startswith('## 7.'):
            in6 = False
            out += ['### 6-補 原稿 → %s の組み立ての記録（機械）' % a.label, '',
                    '- 置換した転記行: %s（`tools/build_draftA.py`・原稿 `%s` SHA16 %s）。本文中の〔転記行 X〕は §6 への参照に改めた。' % ('・'.join(replaced), rel(a.src), sha(a.src)),
                    '- 束縛: 原稿のキー参照 %d 箇所（異なるキー %d 種）を正本 `%s`（SHA16 %s）の値で置換した。組み立ての前に束縛検査、後に登録検査と生成器の文字列リテラル検査を走らせた（`%s`）。' % (len(used), len(set(used)), rel(a.json), sha(a.json), rel(a.lint_report)), '', l]
            continue
        if in6:
            m = re.match(r'^- 〔転記行 ([A-Z])〕\s*$', l)
            if m:
                k = m.group(1); assert k in F, ('設計事実に無い転記行', k); out.append('- **転記行 %s** — %s' % (k, F[k]['text'])); replaced.append(k)
            else:
                out.append(l)
            continue
        out.append(re.sub(r'〔転記行 ([A-Z])〕', lambda mm: '〔転記行 %s・§6〕' % mm.group(1), l))
    missing = [k for k in F if k not in replaced]; assert not missing, ('§6 に置かれていない転記行', missing)
else:
    out = bound.split('\n')
    out = [l.replace('〔束縛の記録〕', '束縛: 原稿 `%s`（SHA16 %s）のキー参照を正本 `%s`（SHA16 %s）の値で置換した（`tools/build_draftA.py`・件数は組み立ての標準出力・数の検査の記録 `%s`）。' % (rel(a.src), sha(a.src), rel(a.json), sha(a.json), rel(a.lint_report))) for l in out]
open(a.out, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print('[build_draftA] written', rel(a.out), 'sha16', sha(a.out), '| transcription', ''.join(replaced) or '—', '| bound keys', len(used))
nb, L = NL.report(J, a.json, a.src, [a.out], a.gen)
os.makedirs(os.path.dirname(a.lint_report), exist_ok=True); open(a.lint_report, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('\n'.join(L[:12 + min(60, nb)]))
sys.exit(1 if nb else 0)
