# -*- coding: utf-8 -*-
"""build_draft5A.py v1 —— 段階 A 草案5 の原稿（design/design-stageA-draft5.src.md）の §6 にある「- 〔転記行 X〕」を設計事実（records/A/design-facts-A.json）の逐語で機械置換し、design/design-stageA-draft5.md を書く（2026-09-13）。
本文中の〔転記行 X〕は「〔転記行 X・§6〕」の参照に改める。置換の記録を §6-補 に印字する。書いた後に numbers_lint.py で本文（§6 と §6-補 を除く）と正本 JSON の説明文を検査し、未登録の数があれば非零で終了する。
検査用に --facts・--facts-md・--out・--lint-report で入出力を差し替えられる（既定は上の本番の置き場）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, subprocess, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('--src', default=os.path.join(REPO, 'design', 'design-stageA-draft5.src.md')); ap.add_argument('--out', default=os.path.join(REPO, 'design', 'design-stageA-draft5.md'))
ap.add_argument('--facts', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.json')); ap.add_argument('--facts-md', default=os.path.join(REPO, 'records', 'A', 'design-facts-A.md'))
ap.add_argument('--lint-report', default=os.path.join(REPO, 'records', 'A', 'numbers-lint-draft5A.md'))
a = ap.parse_args()
CPATH = os.path.join(REPO, 'design', 'contrasts-A.json')
sha = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
rel = lambda p: os.path.relpath(p, REPO).replace('\\', '/')
FJ = json.load(open(a.facts, encoding='utf-8')); F = FJ['facts']
assert FJ['contrasts_sha16'] == sha(CPATH), ('設計事実の正本 SHA16 と現行の正本が不一致', FJ['contrasts_sha16'], sha(CPATH))
s = open(a.src, encoding='utf-8').read().replace('\r\n', '\n'); out = []; replaced = []; in6 = False
for l in s.split('\n'):
    if l.startswith('## 6.'):
        in6 = True
        out.append('## 6. 転記行（機械生成・逐語・`%s`〔SHA16 %s〕・`design/contrasts-A.json`〔SHA16 %s〕・`records/A/power-grid-A.json`〔SHA16 %s〕・生成 %s UTC）' % (rel(a.facts_md), sha(a.facts_md), FJ['contrasts_sha16'], FJ['power_grid_json_sha16'], FJ['generated_utc']))
        continue
    if in6 and l.startswith('## 7.'):
        in6 = False
        out += ['### 6-補 原稿 → 草案5 の置換の記録（機械）', '', '- 置換した転記行: %s（`tools/build_draft5A.py`・原稿 `%s` SHA16 %s）。本文中の〔転記行 X〕は §6 への参照に改めた。本文の数は `tools/numbers_lint.py` で検査した（`%s`）。' % ('・'.join(replaced), rel(a.src), sha(a.src), rel(a.lint_report)), '', l]
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
open(a.out, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print('[draft5A] written', a.out, 'sha16', sha(a.out), 'replaced', ''.join(replaced))
r = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'numbers_lint.py'), '--doc', a.out, '--json', CPATH, '--report', a.lint_report], capture_output=True, text=True, encoding='utf-8')
print(r.stdout)
if r.stderr:
    print(r.stderr, file=sys.stderr)
sys.exit(r.returncode)
