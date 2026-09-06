# -*- coding: utf-8 -*-
"""build_combo_arms_vprime.py —— 追補 V′ の組合せ腕 36 本（{O, Osec, Onull, Nk, Nlib, Nai}×{Ncold, NcoldS, Ncold3, Nneu1, Nneu2, Nneu3}・v2）を乙 V-combination-rule v2 §3 の式
COMBINED(A,B) = rd(A) + "\\n\\n" + rd(B) で決定的に生成し、arms/panel/ と SHA-LEDGER.json に記帳する。既存 4 本（O-Ncold・Ncold-O・Onull-Ncold・Osec-Ncold）には触れない
（O-Ncold・Onull-Ncold・Osec-Ncold は再生成すると同一バイトになることを検査する）。素材 SHA は走行器・台帳と同じ規約（ファイルバイト・CRLF→LF・strip なし）。
自己検査: (a) 空行ちょうど 1 回 (b) split == [A,B] (c) 長さ = |A|+|B|+2 (d) 末尾「。」 (e′) 18 本の SHA 相異（反転対が無いため乙 (e) は適用外）。引数なし・再実行で同一バイト。
"""
import os, sys, json, hashlib
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PANEL = os.path.join(REPO, 'arms', 'panel'); LEDGER = os.path.join(PANEL, 'SHA-LEDGER.json')


def rd(p):
    return open(p, encoding='utf-8').read().replace('\r\n', '\n').strip()


def sha_file(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


def sha16(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()[:16].upper()


MAT = {'O': ('arms/frozen-from-ryokai-os/armsE/preamble-O.md', 'F3EE60C33F825575', 268), 'Onull': ('arms/frozen-from-ryokai-os/armsE/preamble-Onull.md', '2123B3CD8586E7DF', 273),
       'Osec': ('arms/panel/Osec.md', '3D0E78BB21133BB0', 281), 'Nk': ('arms/panel/Nk.md', '47C3CC833B96F7A3', 16), 'Nlib': ('arms/panel/Nlib.md', '9E21FA6690C4DB91', 17),
       'Nai': ('arms/panel/Nai.md', '9F8EB1D4F876C562', 19), 'Ncold': ('arms/panel/Ncold.md', 'E4AB5608C58913E5', 17), 'NcoldS': ('arms/panel/NcoldS.md', '20EADFC8801E8057', 23),
       'Ncold3': ('arms/panel/Ncold3.md', '3B0090077C8F482C', 25),
       'Nneu1': ('arms/panel/Nneu1.md', '95B9487A0DC71C45', 18), 'Nneu2': ('arms/panel/Nneu2.md', 'F0B9780F52CE1B8E', 19), 'Nneu3': ('arms/panel/Nneu3.md', 'FCB896D63D850AB0', 17)}
X = ['O', 'Osec', 'Onull', 'Nk', 'Nlib', 'Nai']; C = ['Ncold', 'NcoldS', 'Ncold3', 'Nneu1', 'Nneu2', 'Nneu3']
texts = {}
for k, (rel, want, n) in MAT.items():
    p = os.path.join(REPO, rel); h = sha_file(p)
    if h != want:
        sys.exit('素材 SHA 不一致: %s %s != %s（生成せず中止）' % (k, h, want))
    t = rd(p)
    if len(t) != n or '\n' in t:
        sys.exit('素材字数/改行不一致: %s %d' % (k, len(t)))
    texts[k] = t
ledger = json.load(open(LEDGER, encoding='utf-8')); rows = []; shas = set()
for x in X:
    for c in C:
        arm = '%s-%s' % (x, c); g = texts[x] + '\n\n' + texts[c]
        assert g.count('\n\n') == 1 and g.split('\n\n') == [texts[x], texts[c]] and len(g) == len(texts[x]) + len(texts[c]) + 2 and g.endswith('。'), arm
        p = os.path.join(PANEL, arm + '.md')
        if os.path.exists(p):
            if rd(p) != g:
                sys.exit('既存の生成物と不一致（改変禁止）: %s' % arm)
        else:
            open(p, 'w', encoding='utf-8', newline='\n').write(g)
        h = sha16(g)
        if arm in ledger and ledger[arm] != h:
            sys.exit('台帳と不一致: %s' % arm)
        ledger[arm] = h; shas.add(h); rows.append((arm, len(g), h))
assert len(shas) == 36, '(e′) SHA 相異'
json.dump(ledger, open(LEDGER, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('| 腕ID | 字数 | SHA16 |'); print('|---|---|---|')
for r in rows:
    print('| %s | %d | %s |' % r)
print('generator_sha', sha16(open(__file__, encoding='utf-8').read().replace('\r\n', '\n')))
