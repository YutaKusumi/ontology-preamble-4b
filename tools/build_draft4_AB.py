# -*- coding: utf-8 -*-
"""build_draft4_AB.py v1 —— 草案3（A・B）の〔転記行 X〕を設計事実（records/A/design-facts-A.json・records/B/design-facts-B.json）の逐語で機械置換し、草案4 を書く（2026-09-13）。
置換は §6 の各行（「- X …〔転記行 X〕」）を転記行の全文に、本文中の〔転記行 X〕を「〔転記行 X〕（§6）」の参照に。差分（置換した行の一覧）を各草案の §6-補 に印字する。
"""
import os, re, json, hashlib
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sha = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
for stage, keys in (('A', 'ABCDEFGHIJKLM'), ('B', 'ABCDEFGHI')):
    src = os.path.join(REPO, 'design', 'design-stage%s-draft3.md' % stage); dst = os.path.join(REPO, 'design', 'design-stage%s-draft4.md' % stage)
    FJ = json.load(open(os.path.join(REPO, 'records', stage, 'design-facts-%s.json' % stage), encoding='utf-8')); F = FJ['facts']
    s = open(src, encoding='utf-8').read(); lines = s.split('\n'); out = []; replaced = []
    in6 = False
    for l in lines:
        if l.startswith('## 6.'):
            in6 = True; out.append('## 6. 転記行（機械生成・逐語・`records/%s/design-facts-%s.md`〔SHA16 %s〕・`design/contrasts-%s.json`〔SHA16 %s〕・生成 %s UTC）' % (stage, stage, sha(os.path.join(REPO, 'records', stage, 'design-facts-%s.md' % stage)), stage, FJ['contrasts_sha16'], FJ['generated_utc'])); continue
        if l.startswith('## 7.'):
            in6 = False; out.append('### 6-補 草案3 → 草案4 の置換の記録（機械）'); out.append(''); out += ['- 置換した転記行: %s。本文中の〔転記行 X〕は §6 への参照に改めた。数値の出所はすべて設計事実の JSON（散文に手計算の数を残さない）。' % '・'.join(replaced)]; out.append(''); out.append(l); continue
        if in6:
            if re.match(r'^- A 規模〔転記行 A〕・B ', l):   # B の草案は §6 が一行に連結
                for k in keys:
                    if k in F:
                        out.append('- **転記行 %s** — %s' % (k, F[k]['text'])); replaced.append(k)
                continue
            m = re.match(r'^- ([A-M]) ', l) or re.match(r'^- ([A-M]) 規模', l)
            if m and m.group(1) in keys and m.group(1) in F:
                k = m.group(1); out.append('- **転記行 %s** — %s' % (k, F[k]['text'])); replaced.append(k); continue
            if l.strip() == '':
                out.append(l); continue
            # B の草案は §6 が一行に連結されている場合がある
            if re.match(r'^- A 規模〔転記行 A〕', l):
                for k in keys:
                    if k in F:
                        out.append('- **転記行 %s** — %s' % (k, F[k]['text'])); replaced.append(k)
                continue
            out.append(l); continue
        l2 = re.sub(r'〔転記行 ([A-M])〕', lambda m: '〔転記行 %s・§6〕' % m.group(1), l)
        out.append(l2)
    t = '\n'.join(out)
    t = t.replace('設計草案3', '設計草案4', 1)
    t = re.sub(r'- 状態: \*\*草案3（', '- 状態: **草案4（草案3 の〔転記行〕を設計事実の逐語で機械置換・`tools/build_draft4_AB.py`・', t, count=1)
    t = t.replace('数は設計定数のみ・計算量は〔転記行〕（器材整備後に `design_facts_A.py` で機械置換）。', '本文の数は設計定数と §6 の転記行（機械生成・逐語）のみ。', 1).replace('数は設計定数のみ・計算量は〔転記行〕。', '本文の数は設計定数と §6 の転記行（機械生成・逐語）のみ。', 1)
    t = t.replace('## 7. 検分票（kensho・コーディネータ・草案3）', '## 7. 検分票（kensho・コーディネータ・草案4）')
    open(dst, 'w', encoding='utf-8', newline='\n').write(t)
    print('[draft4]', stage, dst, 'sha16', sha(dst), 'replaced', ''.join(replaced))
