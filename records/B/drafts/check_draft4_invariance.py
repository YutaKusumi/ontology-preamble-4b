# -*- coding: utf-8 -*-
"""草案1 と草案4 の表紙を突き合わせる: 草案1 の機械の区画の表の行（対照表・札の文言の表・td の表・予想の照合・S4 の区画・門と走行の区画）が、
草案2 にそのまま在ることを確かめ（td の表は区間の丸めだけが違う）、unified diff を書く。数・札・検定が動いていないことの器による確かめ。
用法: python records/B/drafts/check_draft2_invariance.py"""
import os, re, json, difflib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
NL = chr(10)
d1 = open(os.path.join(HERE, 'results-B-draft1.md'), encoding='utf-8').read().split(NL)
d2 = open(os.path.join(REPO, 'records', 'B', 'results-B.md'), encoding='utf-8').read().split(NL)
s16 = lambda t: hashlib.sha256(t.encode('utf-8')).hexdigest().upper()[:16]


def machine_lines(L):
    out, on = [], False
    for l in L:
        if l.startswith('<!-- 機械:始'):
            on = True
        elif l.startswith('<!-- 機械:終'):
            on = False
        elif on and l.strip():
            out.append(l)
    return out


m1, m2 = machine_lines(d1), set(machine_lines(d2))
missing = [l for l in m1 if l not in m2]
# 草案2 で意図して変えた行: 要約の表の確証の行（二つに分けた）・td の表の 8 行（区間の丸め）・出所の表（SHA16 と行の追加）・番号の対応の行
allowed = []
for l in missing:
    if l.startswith('| 確証 |'):
        allowed.append(('要約の表の確証の行を二つに分けた', l)); continue
    if l.startswith('| B_sub |') or l.startswith('| B_add |'):
        nums = lambda s: [round(float(x), 3) for x in re.findall(r'-?[0-9]+[.][0-9]+(?:e-?[0-9]+)?', s)]
        twin = [x for x in m2 if x.split('|')[1:3] == l.split('|')[1:3]]
        assert len(twin) == 1 and nums(twin[0]) == nums(l) and twin[0].split('|')[6:] == l.split('|')[6:], l
        allowed.append(('td の表の区間の丸めだけ（値は同じ）', l)); continue
    if l.startswith('- 確証の札で、起草者の封印の符号と一致したもの'):
        allowed.append(('符号の一致の行を事前登録／逸脱の下に分けた（第二巡 P483）', l)); continue
    if '| `records/B/' in l or '| `tools/' in l or '| `design/' in l or 'この表紙の散文の呼び名と番号の対応' in l or '凍結の記録の逸脱台帳' in l:
        allowed.append(('出所の表と番号の対応（凍結の記録と機械の報告の一本が逸脱（五）で変わった）', l)); continue
    raise SystemExit('草案1 の機械の区画の行が草案2 に無い: ' + l[:160])
diff = list(difflib.unified_diff(d1, d2, 'results-B-draft1.md', 'results-B.md（草案4）', lineterm='', n=1))
out = os.path.join(HERE, 'diff-draft1-draft4.diff')
open(out, 'w', encoding='utf-8', newline=NL).write(NL.join(diff) + NL)
rec = dict(kind='check_draft4_invariance', draft1_sha16=s16(NL.join(d1)), draft4_sha16=s16(NL.join(d2)), machine_lines_draft1=len(m1), machine_lines_draft4=len(m2),
           kept_verbatim=len(m1) - len(missing), changed_allowed=[dict(reason=r, line=l[:120]) for r, l in allowed],
           diff_lines=len(diff), added=sum(1 for l in diff if l.startswith('+') and not l.startswith('+++')), removed=sum(1 for l in diff if l.startswith('-') and not l.startswith('---')))
json.dump(rec, open(os.path.join(HERE, 'check-draft4-invariance.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in rec.items() if k != 'changed_allowed'}, ensure_ascii=False))
for r, l in allowed:
    print(' ', r, '::', l[:80])
