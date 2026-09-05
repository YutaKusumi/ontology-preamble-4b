# -*- coding: utf-8 -*-
"""段V 組合せ腕・段VI 用量腕を arms/panel/ に決定的に生成する（乙 V-combination-rule v2 §3・§6・§7 の契約）。
引数なし・表を内蔵・実行のたびに同一バイト。素材SHAは arms/panel/SHA-LEDGER.json と凍結表で照合し、不一致なら生成せず終了。
【注】乙 v2 §5 の Osec 行（59394457C47B2E05・v2）は登録者裁定 U-1（2026-09-05）で O-sec v3（3D0E78BB21133BB0）に更新された。
"""
import os, sys, json, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANEL = os.path.join(REPO, 'arms', 'panel')
LEDGER = os.path.join(PANEL, 'SHA-LEDGER.json')


def rd(p):
    return open(p, encoding='utf-8').read().replace('\r\n', '\n').strip()


def sha16(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()[:16].upper()


# 素材SHA（凍結表）
MATERIALS = {
    'arms/frozen-from-ryokai-os/armsE/preamble-O.md': ('O', 'F3EE60C33F825575', 268),
    'arms/frozen-from-ryokai-os/armsE/preamble-Onull.md': ('Onull', '2123B3CD8586E7DF', 273),
    'arms/frozen-from-ryokai-os/armsE/preamble-Lneg.md': ('Lneg', 'A16E20E4827D9C86', 287),
    'arms/panel/Osec.md': ('Osec', '3D0E78BB21133BB0', 281),          # v3（U-1）
    'arms/panel/Ncold.md': ('Ncold', 'E4AB5608C58913E5', 17),
    'arms/materials-draft/ko/O-dose-1.md': ('Odose1', None, 34),
    'arms/materials-draft/ko/O-dose-half.md': ('Odosehalf', None, 92),
    'arms/materials-draft/ko/Lneg-dose-1.md': ('Lnegdose1', None, 49),
    'arms/materials-draft/ko/Lneg-dose-half.md': ('Lnegdosehalf', None, 108),
}
# 組合せ腕（A 先・B 後・"\n\n" 連結）
COMBOS = [('O-Ncold', 'arms/frozen-from-ryokai-os/armsE/preamble-O.md', 'arms/panel/Ncold.md'),
          ('Ncold-O', 'arms/panel/Ncold.md', 'arms/frozen-from-ryokai-os/armsE/preamble-O.md'),
          ('Onull-Ncold', 'arms/frozen-from-ryokai-os/armsE/preamble-Onull.md', 'arms/panel/Ncold.md'),
          ('Osec-Ncold', 'arms/panel/Osec.md', 'arms/panel/Ncold.md')]
# 用量腕（甲起草物の写し・逐語）
DOSES = ['arms/materials-draft/ko/O-dose-1.md', 'arms/materials-draft/ko/O-dose-half.md',
         'arms/materials-draft/ko/Lneg-dose-1.md', 'arms/materials-draft/ko/Lneg-dose-half.md']

def sha_file(p):
    """走行器・台帳と同じ規約: ファイルのバイト列を CRLF→LF 正規化して SHA-256 先頭16桁（strip しない）"""
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()


texts = {}
for rel, (name, sha, n) in MATERIALS.items():
    t = rd(os.path.join(REPO, rel)); h = sha_file(os.path.join(REPO, rel))
    if sha and h != sha:
        sys.exit('素材SHA不一致: %s %s != %s（生成せず中止）' % (rel, h, sha))
    if len(t) != n:
        sys.exit('素材字数不一致: %s %d != %d' % (rel, len(t), n))
    texts[rel] = t

out = {}
for arm, a, b in COMBOS:
    A, B = texts[a], texts[b]
    g = A + '\n\n' + B
    assert g.count('\n\n') == 1 and g.split('\n\n') == [A, B] and len(g) == len(A) + len(B) + 2 and g.endswith('。'), arm
    out[arm] = g
assert len(out['O-Ncold']) == len(out['Ncold-O']) and sha16(out['O-Ncold']) != sha16(out['Ncold-O'])
for rel in DOSES:
    out[MATERIALS[rel][0]] = texts[rel]

ledger = json.load(open(LEDGER, encoding='utf-8'))
rows = []
for arm, g in out.items():
    p = os.path.join(PANEL, arm + '.md')
    if os.path.exists(p) and rd(p) != g:
        sys.exit('既存の生成物と不一致（改変禁止）: %s' % arm)
    open(p, 'w', encoding='utf-8', newline='\n').write(g)
    ledger[arm] = sha16(g)
    rows.append((arm, len(g), ledger[arm]))
json.dump(ledger, open(LEDGER, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print('| 腕ID | 字数 | SHA16 |'); print('|---|---|---|')
for r in rows:
    print('| %s | %d | %s |' % r)
print('generator_sha', sha16(open(__file__, encoding='utf-8').read().replace('\r\n', '\n')))
