# -*- coding: utf-8 -*-
"""make_analyze_B_devB1.py —— 逸脱 D-B1（登録者裁定 D151・2026-09-22）の集計器 `tools/analyze_B_devB1.py` を、凍結した `tools/analyze_B.py` から**機械で**作る。

なぜ: 凍結した集計器は、選定後の品質床で、確証族の二つの土台の腕（O-Ncold-v・Onull+v）にも選定後の段の走行を求める。凍結した起動器は正本
      `quality_floor.run_order`（「(ii)…残りの介入の腕」）に従ってこの二腕を選定後の段から外すので、二腕は「走行が無い」と数えられ、減算族と加算族の
      8 対比が「判定不能（品質床）」になった（事実の記録 `records/B/incident-qpost-missing-2026-09-22.md`・四票の採否 `records/reviews/B/incident-qpost-round/`）。
直し（最小・採否表 P437）: 選定後の段の走行が**無い**腕が確証族の土台の腕であるとき、その床を**門の記録の・選定の段の・選ばれた層 × 係数の行**で読む。
      それ以外は一字も変えない（検定・族・Holm・閾値・門・様式・S4・td——すべて凍結した器のまま）。床をこの読みで通った腕を含む対比には
      `deviation: 'D-B1'` の欄と注を足し、確証の札には「逸脱 D-B1 の下」の印を足す（札の頭は「確証」のまま——照合の器と特異性の規則は頭で読む・採否表 P444）。
**凍結した `tools/analyze_B.py` は変えない。** 本器は凍結物の SHA16 を凍結の記録と照らしてから読み、差分を `records/B/deviations/D-B1-analyze_B.diff` に書く。
用法: python tools/make_analyze_B_devB1.py [--force]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, difflib, hashlib, argparse

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = os.path.join(REPO, 'tools', 'analyze_B.py')
OUT = os.path.join(REPO, 'tools', 'analyze_B_devB1.py')
DIFF = os.path.join(REPO, 'records', 'B', 'deviations', 'D-B1-analyze_B.diff')
NL = chr(10)
s16 = lambda b: hashlib.sha256(b).hexdigest().upper()[:16]

HEADER = NL.join([
    '# -*- coding: utf-8 -*-',
    '# **逸脱 D-B1 の下の集計器**（登録者裁定 D151・2026-09-22）。凍結した `tools/analyze_B.py` から `tools/make_analyze_B_devB1.py` が機械で作った——手で直さない。',
    '# 違いは、選定後の段の走行が無い確証族の土台の腕の品質床を、門の記録の・選定の段の・選ばれた層 × 係数の行で読むことと、その印だけである。',
    '# 凍結した器の出力（`records/B/analysis-B-2026-09-22.*`）は変えずに残し、報告は二つの出力を並べる。',
]) + NL

DEFS = NL.join([
    "# ==== 逸脱 D-B1（登録者裁定 D151・2026-09-22）: 確証族の土台の腕の選定後の床を、門の記録の選定の段の行で読む ====",
    "DEVB1_SOURCE = '門の記録の・選定の段の・選ばれた層 × 係数の行（逸脱 D-B1・登録者裁定 D151）'",
    "DEVB1_NOTE = '逸脱 D-B1 の下（土台の腕の選定後の品質床を門の記録の選定の段の行で読んだ・凍結した集計器の札は「判定不能（品質床）」）'",
    "_OPS_DEVB1 = {'O-Ncold': '-v', 'Onull': '+v'}           # 起動器と同じ対応（正本 quality_floor.operations）",
    "DEVB1_BASE_ARMS = {b + _OPS_DEVB1[b] for b in T['quality_floor']['arms']}",
    "DEVB1_ARMS, DEVB1_GATE_ROWS = set(), {}",
    "for _r in (G.get('quality_floor_rows') or []):",
    "    if (_r.get('arm') in DEVB1_BASE_ARMS and PICK.get('layer') is not None and not _r.get('missing')",
    "            and float(_r.get('layer')) == float(PICK['layer']) and float(_r.get('coef')) == float(PICK['coef'])):",
    "        DEVB1_GATE_ROWS[_r['arm']] = {k: _r.get(k) for k in ('arm', 'layer', 'coef', 'correct', 'noop_correct', 'n_ok', 'noop_n_ok',",
    "                                                          'api_error', 'noop_api_error', 'diff_pt', 'pass', 'boundary')}",
]) + NL

BRANCH = NL.join([
    "    if not cells and arm in DEVB1_GATE_ROWS:             # 逸脱 D-B1: 走行が無い土台の腕は、門の記録の選定の段の行で読む",
    "        _g = DEVB1_GATE_ROWS[arm]",
    "        QF_ROWS.append(dict(_g, source=DEVB1_SOURCE))",
    "        DEVB1_ARMS.add(arm)",
    "        if not _g.get('pass'):",
    "            QF_FAIL.add(arm)",
    "        continue",
]) + NL

MARK = NL.join([
    "# ---- 逸脱 D-B1 の印: 床を門の記録で読んだ腕を含む対比に欄と注を足し、確証の札に印を足す（札の頭は「確証」のまま） ----",
    "for r in FAMROWS:",
    "    if r.get('A') in DEVB1_ARMS or r.get('B') in DEVB1_ARMS:",
    "        r['deviation'] = 'D-B1'",
    "        r.setdefault('notes', []).append(DEVB1_NOTE)",
    "        _lab = str(r.get('label') or '')",
    "        if _lab.startswith('確証'):",
    "            r['label'] = (_lab[:-1] + '・逸脱 D-B1 の下）') if _lab.endswith('）') else (_lab + '（逸脱 D-B1 の下）')",
]) + NL

# (目印, 置き換え方, 中身)
A_VERSION = "VERSION = 'v7'"
A_POST = "_post = {k: v for k, v in CQ.items() if k[0] == 'post'}" + NL
A_BRANCH = "    if not cells:" + NL + "        QF_MISSING.append(arm)" + NL
A_COUNTS = "counts = {k: 0 for k in ('確証', '判定不能（検閲）'"
A_TITLE = "L = ['# 段階 B 本走行の集計（機械生成・`tools/analyze_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',"
A_REC = "'quality_post': QF_ROWS,"


def build(src_text):
    t = src_text
    for anchor in (A_VERSION, A_POST, A_BRANCH, A_COUNTS, A_TITLE, A_REC):
        assert t.count(anchor) == 1, '目印が一つでない: %r（%d）' % (anchor[:50], t.count(anchor))
    assert t.startswith('# -*- coding: utf-8 -*-' + NL)
    t = HEADER + t[len('# -*- coding: utf-8 -*-' + NL):]
    t = t.replace(A_VERSION, "VERSION = 'v7+devB1'")
    t = t.replace(A_POST, A_POST + DEFS)
    t = t.replace(A_BRANCH, BRANCH + A_BRANCH)
    t = t.replace(A_COUNTS, MARK + A_COUNTS)
    t = t.replace(A_TITLE, "L = ['# 段階 B 本走行の集計——**逸脱 D-B1 の下**（機械生成・`tools/analyze_B_devB1.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',"
                  + NL + "     '- **これは逸脱 D-B1 の下の出力である**（登録者裁定 D151・2026-09-22）。凍結した集計器の出力は `records/B/analysis-B-2026-09-22.md` にある。違いは、床を ' + DEVB1_SOURCE + ' で読んだ腕（' + '・'.join(sorted(DEVB1_ARMS)) + '）を含む対比の札と、その族の Holm だけである。直すという決定は率と p を見た後になされた。',")
    t = t.replace(A_REC, A_REC + " 'deviation_D_B1': {'ruling': 'D151', 'arms': sorted(DEVB1_ARMS), 'source': DEVB1_SOURCE, 'gate_rows': DEVB1_GATE_ROWS},")
    return t


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    raw = open(SRC, 'rb').read()
    FR = json.load(open(os.path.join(REPO, 'records', 'B', 'FREEZE-RECORD-B.json'), encoding='utf-8'))
    want = FR['frozen']['tools']['analyze_B.py']
    got = s16(raw.replace(b'\r\n', b'\n'))
    if got != want:
        sys.exit('凍結した集計器の SHA16 が凍結の記録と違う（%s ≠ %s）——止まる' % (got, want))
    src = raw.decode('utf-8').replace('\r\n', NL)
    new = build(src)
    compile(new, OUT, 'exec')
    if os.path.exists(OUT) and not a.force:
        sys.exit('既にある（--force で置き換え）: %s' % OUT)
    open(OUT, 'w', encoding='utf-8', newline=NL).write(new)
    d = list(difflib.unified_diff(src.split(NL), new.split(NL), 'tools/analyze_B.py', 'tools/analyze_B_devB1.py', lineterm='', n=2))
    os.makedirs(os.path.dirname(DIFF), exist_ok=True)
    open(DIFF, 'w', encoding='utf-8', newline=NL).write(NL.join(d) + NL)
    plus = sum(1 for l in d if l.startswith('+') and not l.startswith('+++'))
    minus = sum(1 for l in d if l.startswith('-') and not l.startswith('---'))
    print('[make_analyze_B_devB1] 凍結した集計器 SHA16 %s（凍結の記録と一致）→ %s SHA16 %s' % (got, os.path.relpath(OUT, REPO), s16(new.encode('utf-8'))))
    print('  差分 %s（足した行 %d・外した行 %d）SHA16 %s／本器 SHA16 %s' % (os.path.relpath(DIFF, REPO), plus, minus,
                                                                  s16(open(DIFF, 'rb').read()), s16(open(os.path.abspath(__file__), 'rb').read().replace(b'\r\n', b'\n'))))
