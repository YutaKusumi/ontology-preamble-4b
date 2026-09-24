# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の草案3 の直しの案（登録者が見た版・写しを `records/Bl3/draft3-review/proposal/` に保存）と、裁定 D224・D225 の記帳の後の版を比べる。
- 写しの SHA16 が、見直しの記録に書いた直しの案の SHA16 と同じことを確かめる（違えば止める）。
- 正本の葉の差と、草案3 の行の差を器が並べ、差が裁定の記帳に伴う所だけであることを確かめる（決めた型の外の差があれば止める）。
出力: records/Bl3/draft3-review/final-diff-draft3-Bl3.md
用法: python records/Bl3/draft3-review/verify_final_draft3_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
NL = chr(10)
rd = lambda p: open(os.path.join(REPO, *p.split('/')), 'rb').read().replace(b'\r\n', b'\n')
h16 = lambda p: hashlib.sha256(rd(p)).hexdigest().upper()[:16]
RV = 'records/Bl3/draft3-review/review-draft3-Bl3.md'
line = [l for l in rd(RV).decode('utf-8').split(NL) if l.startswith('- 置き場のファイル: ')]
assert len(line) == 1
cited = dict(re.findall(r'`([^`]+)`（SHA16 ([0-9A-F]{16})）', line[0]))
PD, PC = 'records/Bl3/draft3-review/proposal/design-Bl3-draft3-proposal.md', 'records/Bl3/draft3-review/proposal/contrasts-Bl3-proposal.json'
FD, FC = 'design/design-Bl3-draft3.md', 'design/contrasts-Bl3.json'
assert h16(PD) == cited[FD] and h16(PC) == cited[FC], ('写しが見直しの記録の直しの案と違う', h16(PD), h16(PC))


def leaves(o, p='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, p + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, '%s[%d]' % (p, i))
    else:
        yield p, o


Lo, Ln = dict(leaves(json.loads(rd(PC)))), dict(leaves(json.loads(rd(FC))))
leaf_diff = sorted(k for k in set(Lo) | set(Ln) if Lo.get(k) != Ln.get(k))
ALLOWED_LEAF = re.compile(r'^\$\.(decisions\.D22[45]|numbering\.rulings_next|inputs\.files\.(rulings_D224_D225|draft3_review)\.(path|sha16)|inputs\.files\.\w+\.sha16)$')
bad_leaf = [k for k in leaf_diff if not ALLOWED_LEAF.match(k)]
sha_moved = [k for k in leaf_diff if k.endswith('.sha16') and not re.search(r'(rulings_D224_D225|draft3_review)', k)]
Do, Dn = rd(PD).decode('utf-8').splitlines(), rd(FD).decode('utf-8').splitlines()
ops = [op for op in difflib.SequenceMatcher(a=Do, b=Dn, autojunk=False).get_opcodes() if op[0] != 'equal']
changes = []
for tag, i1, i2, j1, j2 in ops:
    assert tag == 'replace' and i2 - i1 == j2 - j1, ('行の足し引きがある', tag, i1, i2, j1, j2)
    for a, b in zip(range(i1, i2), range(j1, j2)):
        changes.append((a + 1, Do[a], Dn[b]))
KINDS = [('状態の行', lambda o, n: o.startswith('- 起草: ') and '起草者の見直しの後の案・' in o and '起草者の見直しの後・' in n and o.replace('起草者の見直しの後の案・', '起草者の見直しの後・') == n),
         ('位置づけの行（裁定の記録の一覧）', lambda o, n: o.startswith('- 位置づけ: ') and o.replace('D204〜D223', 'D204〜D225').replace('`records/Bl3/rulings-D219-D223.md`）', '`records/Bl3/rulings-D219-D223.md`・`records/Bl3/rulings-D224-D225.md`）') == n),
         ('§0 の見直しの直しの行', lambda o, n: o.startswith('- 起草者の見直しで見つけた所を直した') and o.replace('（見直しの記録）。', '（見直しの記録・裁定 D224・D225）。') == n),
         ('§16 の書き足した決まりの見出し', lambda o, n: o.startswith('- **起草者の見直しで書き足した決まり**') and o.replace('（見直しの記録・外の目を通っていない・登録者の確認で見ていただく所）', '（見直しの記録・裁定 D224・D225 で採った・外の目を通っていない）') == n),
         ('§6 の見出し（設計事実と正本の SHA16・生成の時刻）', lambda o, n: o.startswith('## 6. 転記行') and re.sub(r'[0-9A-F]{16}|\d{2}:\d{2} UTC', '', o) == re.sub(r'[0-9A-F]{16}|\d{2}:\d{2} UTC', '', n)),
         ('§6-補（原稿と正本の SHA16）', lambda o, n: (o.startswith('- 置換した転記行') or o.startswith('- 束縛: ')) and re.sub(r'[0-9A-F]{16}', '', o) == re.sub(r'[0-9A-F]{16}', '', n))]
kinded = []
for ln, o, n in changes:
    k = [name for name, f in KINDS if f(o, n)]
    kinded.append((ln, k[0] if len(k) == 1 else None, o, n))
bad_line = [x for x in kinded if x[1] is None]
esc = lambda s: str(s).replace('|', '｜')
R = ['# B-lens 層三の草案3 の直しの案と、裁定 D224・D225 の記帳の後の版の比べ（機械生成・`records/Bl3/draft3-review/verify_final_draft3_Bl3.py`）', '',
     '- 直しの案（登録者が見た版）の写し: `%s`（SHA16 %s）・`%s`（SHA16 %s）。見直しの記録 `%s` に書いた直しの案の SHA16 と同じ。' % (PD, h16(PD), PC, h16(PC), RV),
     '- 記帳の後の版: `%s`（SHA16 %s・%d 行）・`%s`（SHA16 %s）。' % (FD, h16(FD), len(Dn), FC, h16(FC)),
     '- 正本の葉の差: %d（決めた型の外 %d）。草案3 の行の差: %d 行（行の足し引き無し・決めた型の外 %d）。' % (len(leaf_diff), len(bad_leaf), len(changes), len(bad_line)), '',
     '## 正本の葉の差', '', '| 葉 | 案 | 記帳の後 |', '|---|---|---|'] + [
     '| `%s` | %s | %s |' % (k[2:], esc(str(Lo.get(k, '（無い）'))[:80]), esc(str(Ln.get(k, '（無い）'))[:80])) for k in leaf_diff] + [
     '', '- `inputs.files` の中で、足した二つのほかに SHA16 が動いた入力: %s。' % ('・'.join('`%s`' % k[2:] for k in sha_moved) or '無し'), '',
     '## 草案3 の行の差', '', '| 行 | 型 | 案 | 記帳の後 |', '|---|---|---|---|'] + [
     '| %d | %s | %s | %s |' % (ln, k or '**決めた型の外**', esc(o[:110]), esc(n[:110])) for ln, k, o, n in kinded] + [
     '', '## 注（事実のみ）', '',
     '- 見直しの記録は、裁定の後に変える所を「台帳・§0 の直しの行・状態の行」の三つと見込んだ。実際には、ほかに位置づけの行（裁定の記録の一覧）と §16 の書き足した決まりの見出しの二つも変えた。どちらも裁定の記帳に伴う言い方の直しで、決まりの中身は変えていない。§6 と §6-補 の行は、正本と設計事実の SHA16 が変わったので機械で変わった。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'final-diff-draft3-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
print('wrote final-diff-draft3-Bl3.md | leaf diff', len(leaf_diff), 'bad', len(bad_leaf), '| line diff', len(changes), 'bad', len(bad_line), '| sha moved', sha_moved)
sys.exit(1 if (bad_leaf or bad_line) else 0)
