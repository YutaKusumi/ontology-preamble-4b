# -*- coding: utf-8 -*-
"""make_frozen_Bprime.py v0.1 —— B′ の凍結する本文（`design/design-Bprime-FROZEN.md`）を、登録者の確認を得た草案から組む（層三の `make_frozen_Bl3.py` v4 の型・
2026-09-30・コーディネータ南無弥勒如来）。

B′ の草案は正本の鍵から組む原稿（層三の `.src.md`）を持たず、数は草案の字のまま置いた。そこで「原稿の数を正本の鍵で束ねる」は、凍結の本文のすべての数（§6 と凍結の一行を除く）が
正本の数値の葉か配列の長さに当たることを、B′ の数の検査の包み（`bprime_numbers_lint`・凍結した `numbers_lint.py` の登録検査を呼ぶ）で確かめることとする（違反が零でなければ止める）。
凍結の本文と草案の差は、次の三つだけ（ほかの差があれば止める）:
  (一) 題名の印（段階 B の器 `make_frozen_B.MARK`・「）——」の所に置く）と、状態の行の次の凍結の一行（登録者の逐語と日時・草案の SHA16）。
  (二) §6 の見出し（転記行の記録と正本の SHA16 と器）と、§6 の草案の行の後に足す「凍結の前に決まる行」の節（転記行の記録 `records/Bprime/facts-Bprime-pre.md` の本文を逐語で）。
  (三) 原稿の文の直し（`LITERAL_FIXES`・裁定ごと・草案の中でちょうど一度ずつ当たる）。今は無い。
草案の中の `../` の道筋は作業の置き場（非公開）のもので、凍結の本文では直さない。公開の置き場での道筋は、移し方の表（`bprime_publish_map`）の記録で引く（凍結の一行に書く）。
凍結の一行は、数の検査の間は決まった代わりの行にし（登録者の逐語と日時の数を検査の外に置く・層三の D236 の型）、組んだ後に逐語の一行に戻す。
**本器は凍結そのものではない**——凍結の記帳は `tools/freeze_Bprime.py` が行う。
出力: `design/design-Bprime-FROZEN.md`・`records/Bprime/numbers-lint-FROZEN-Bprime.md`・`records/Bprime/frozen-diff-Bprime.md`。
用法: python tools/make_frozen_Bprime.py --words "<登録者の逐語>" --date "<日時（日本時間）>" [--force] ／ --check（組み直して凍結の本文と照らす）／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, difflib, hashlib, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G                     # 凍結の器の置き場を sys.path に足す
import make_frozen_B as MF                   # 凍結の器（題名の印を使うだけ）
import bprime_numbers_lint as NL_           # B′ の数の検査の包み

VERSION = 'v0.1'        # v0.1（2026-09-30・器の実装の検分の後）: 元を草案11 に替えた（正本 v5・登録者の確認を待つ）・登録者の逐語に改行があれば先に理由を示して止める（凍結の一行に入らない・U25・R2-28）。前の版は `prev/make_frozen_Bprime-v0.py`
NL = chr(10)
SRC = os.path.join(ROOT, 'design', 'design-Bprime-draft11.md')
SRC_SHA16 = '1C8CF84AA14A31B8'                 # 草案11（v0.1・前は草案10 2337E14DF7BDE68D・登録者の確認を得た版に替えるときは、この値と SRC を替える）
FOUT = os.path.join(ROOT, 'design', 'design-Bprime-FROZEN.md')
CANON = os.path.join(ROOT, 'design', 'contrasts-Bprime.json')
FACTS_MD = os.path.join(ROOT, 'records', 'Bprime', 'facts-Bprime-pre.md')
FACTS_JSON = os.path.join(ROOT, 'records', 'Bprime', 'facts-Bprime-pre.json')
LINT = os.path.join(ROOT, 'records', 'Bprime', 'numbers-lint-FROZEN-Bprime.md')
DIFFREC = os.path.join(ROOT, 'records', 'Bprime', 'frozen-diff-Bprime.md')
H6_DRAFT = '## 6. 転記行（機械生成・この草案では口だけ）'
H6_FROZEN = '## 6. 転記行（機械生成・逐語・`records/Bprime/facts-Bprime-pre.md`〔SHA16 %s〕・正本 `design/contrasts-Bprime.json`〔SHA16 %s〕・器 `tools/bprime_facts.py`・行 C と D は走行の記録から作る）'
SUB6 = '### 6.1 凍結の前に決まる行（転記行の記録の本文を逐語で）'
STANDIN = '- **凍結**: （凍結の一行・登録者の逐語と日時は組み立ての後に入れる）'
FROZEN_LINE = ('- **凍結**: %s（日本時間・登録者の言葉は逐語で「%s」・草案（`design/%s`・SHA16 %s）を逐語複製し、題名と本行と §6 の転記行（機械生成）だけを改める・'
               '本文の中の `../` の道筋は作業の置き場のもので、公開の置き場での道筋は移し方の記録（`records/Bprime/publish-map-Bprime.json`）で引く・以後の変更は逸脱台帳に記帳する）')
LITERAL_FIXES = []                           # (裁定, 直す前, 直した後)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha16b(b):
    return hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def sha16f(p):
    with open(p, 'rb') as fh:
        return sha16b(fh.read())


def read(p):
    with open(p, encoding='utf-8') as fh:
        return fh.read()


def write(p, text):
    with open(p, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(text)


def facts_body(facts_md_text):
    """転記行の記録の本文（題の行と柵の文を除いた行・前後の空行を除く）。"""
    lines = facts_md_text.split(NL)
    if not lines or not lines[0].startswith('# '):
        raise SystemExit('転記行の記録の題の行が無い')
    body = [l for l in lines[1:] if l.strip() != CLAUSE]
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return body


def build(draft_text, facts_text, facts_sha16, canon_sha16, frozen_line):
    """草案 → 凍結の本文（(一)(二)(三) だけを改める）。"""
    lines = draft_text.split(NL)
    head, sep, tail = lines[0].partition('）——')
    if not lines[0].startswith('# ') or not sep or MF.MARK in lines[0]:
        raise SystemExit('題名の行の形が違うか、既に凍結版の題名になっている')
    lines[0] = head + '）' + MF.MARK + tail
    st = [i for i, l in enumerate(lines) if l.startswith('- 状態:')]
    if len(st) != 1:
        raise SystemExit('状態の行がちょうど一つでない')
    lines.insert(st[0] + 1, frozen_line)
    h6 = [i for i, l in enumerate(lines) if l == H6_DRAFT]
    h7 = [i for i, l in enumerate(lines) if l.startswith('## 7.')]
    if len(h6) != 1 or len(h7) != 1 or h7[0] < h6[0]:
        raise SystemExit('§6 の見出しか §7 の見出しがちょうど一つでない')
    lines[h6[0]] = H6_FROZEN % (facts_sha16, canon_sha16)
    ins = [SUB6, ''] + facts_body(facts_text) + ['']
    lines[h7[0]:h7[0]] = ins
    out = NL.join(lines)
    for rid, old, new in LITERAL_FIXES:
        if out.count(old) != 1:
            raise SystemExit('原稿の直しの前の文がちょうど一度だけ当たらない（%s・%d 回）' % (rid, out.count(old)))
        out = out.replace(old, new)
    return out


def residual_diff(draft_text, frozen_text):
    """凍結の本文から (一)(二) を外して草案に戻し、草案と字のまま同じかを見る（(三) の直しは戻してから比べる）。戻せなければ理由を返す。"""
    t = frozen_text
    for rid, old, new in LITERAL_FIXES:
        t = t.replace(new, old)
    lines = t.split(NL)
    if MF.MARK not in lines[0]:
        return ['題名の印が無い']
    lines[0] = lines[0].replace('）' + MF.MARK, '）——', 1)
    fl = [i for i, l in enumerate(lines) if l.startswith('- **凍結**:')]
    if len(fl) != 1:
        return ['凍結の一行がちょうど一つでない']
    del lines[fl[0]]
    h6 = [i for i, l in enumerate(lines) if l.startswith('## 6. 転記行（機械生成・逐語・')]
    s6 = [i for i, l in enumerate(lines) if l == SUB6]
    h7 = [i for i, l in enumerate(lines) if l.startswith('## 7.')]
    if len(h6) != 1 or len(s6) != 1 or len(h7) != 1 or not (h6[0] < s6[0] < h7[0]):
        return ['§6 の見出しか足した節の形が違う']
    lines[h6[0]] = H6_DRAFT
    del lines[s6[0]:h7[0]]
    back = NL.join(lines)
    if back == draft_text:
        return []
    return [l for l in difflib.unified_diff(draft_text.split(NL), back.split(NL), n=0, lineterm='') if l[:1] in '+-' and not l.startswith(('---', '+++'))][:20]


def lint(frozen_standin_text, canon_path=CANON):
    """凍結の本文（凍結の一行は代わりの行）に数の登録検査を掛ける（§6 を除く）。"""
    with open(canon_path, encoding='utf-8') as fh:
        J = json.load(fh)
    Cset = NL_.N0.const_set(J)
    return NL_.check_doc(J, frozen_standin_text, Cset)


def make(words, date, draft_path=SRC, draft_sha16=SRC_SHA16, out=FOUT, lint_path=LINT, diff_path=DIFFREC, facts_md=FACTS_MD, facts_json=FACTS_JSON, canon=CANON):
    if any(ch in str(words) for ch in ('\n', '\r', '\u2028', '\u2029', '\x85')):
        raise SystemExit('登録者の逐語に改行がある。凍結の一行は一行なので、逐語のまま入らない（改行の所を登録者に確かめる・U25）')
    d_raw = open(draft_path, 'rb').read()
    if sha16b(d_raw) != draft_sha16:
        raise SystemExit('草案の SHA16 が、登録者の確認を得た版と違う')
    draft = d_raw.decode('utf-8')
    with open(facts_json, encoding='utf-8') as fh:
        FJ = json.load(fh)
    canon16 = sha16f(canon)
    if FJ.get('contract_sha16') != canon16:
        raise SystemExit('転記行の記録の正本の SHA16 が今の正本と違う（`bprime_facts.py` で作り直す）')
    facts_text, f16 = read(facts_md), sha16f(facts_md)
    fl = FROZEN_LINE % (date, words, os.path.basename(draft_path), draft_sha16)
    standin = build(draft, facts_text, f16, canon16, STANDIN)
    bad = lint(standin, canon)
    frozen = standin.replace(STANDIN, fl)
    if frozen.count(fl) != 1:
        raise SystemExit('凍結の一行がちょうど一度だけ入らない')
    res = residual_diff(draft, frozen)
    rep = ['# 数の機械検査（B′ の凍結の本文・機械生成・`tools/make_frozen_Bprime.py` %s が `bprime_numbers_lint` を呼んだ）' % VERSION, '',
           '- 本文: `design/%s`（凍結の一行は検査の間は決まった代わりの行・§6 は検査の外）・正本 `design/contrasts-Bprime.json`（SHA16 %s）。' % (os.path.basename(out), canon16),
           '- 登録検査（本文の数が正本の数値の葉か配列の長さに当たるか）: 未登録 %d' % len(bad)] + ['- %d 行: `%s` … %s' % (i, tok, ctx.replace('`', "'")) for i, tok, ctx in bad] + ['', CLAUSE, '']
    diff = [l for l in difflib.unified_diff(draft.split(NL), frozen.split(NL), n=0, lineterm='') if l[:1] in '+-' and not l.startswith(('---', '+++'))]
    drec = ['# B′ の凍結の本文と草案の差の記録（機械生成・`tools/make_frozen_Bprime.py` %s）' % VERSION, '',
            '- 草案 `design/%s`（SHA16 %s）・転記行の記録 `records/Bprime/facts-Bprime-pre.md`（SHA16 %s）・正本（SHA16 %s）。' % (os.path.basename(draft_path), draft_sha16, f16, canon16),
            '- 差は (一) 題名の印と凍結の一行・(二) §6 の見出しと「凍結の前に決まる行」の節・(三) 原稿の文の直し（%d）だけ。凍結の本文から (一)(二) を外し (三) を戻すと草案と字のまま同じ: %s。' % (
                len(LITERAL_FIXES), '同じ' if not res else '**違う**'),
            '- 凍結の一行は、数の検査の間は決まった代わりの行にし、組んだ後に逐語の一行に戻した（層三の D236 の型）。', '', '```diff'] + diff + ['```', '', CLAUSE, '']
    if bad or res:
        raise SystemExit('凍結の本文の確かめが外れた（数の検査の未登録 %d・草案との差の残り %s）' % (len(bad), res[:5]))
    return frozen, NL.join(rep), NL.join(drec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--words')
    ap.add_argument('--date')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.check:
        t = read(FOUT)
        m = re.search(r'^- \*\*凍結\*\*: (.+?)（日本時間・登録者の言葉は逐語で「(.*)」・草案（', t, flags=re.M)
        if not m:
            raise SystemExit('凍結の本文に凍結の一行が無い')
        frozen, _, _ = make(m.group(2), m.group(1))
        same = frozen == t
        print('[make_frozen_Bprime] 組み直しと凍結の本文: %s' % ('同じ' if same else '違う'))
        sys.exit(0 if same else 1)
    if not (a.words and a.date):
        raise SystemExit('--words と --date が要る')
    for p in (FOUT, LINT, DIFFREC):
        if os.path.exists(p) and not a.force:
            raise SystemExit('既にある（--force で上書き）: %s' % os.path.relpath(p, ROOT))
    frozen, rep, drec = make(a.words, a.date)
    write(FOUT, frozen)
    write(LINT, rep)
    write(DIFFREC, drec)
    print('[make_frozen_Bprime] %s（SHA16 %s）・%s・%s' % (os.path.relpath(FOUT, ROOT), sha16f(FOUT), os.path.relpath(LINT, ROOT), os.path.relpath(DIFFREC, ROOT)))


def _selftest():
    import tempfile
    ok = []
    with tempfile.TemporaryDirectory() as td:
        # 合成の転記行の記録（今の正本の SHA16 を持つ）と草案の写しで組む
        canon16 = sha16f(CANON)
        fj, fm = os.path.join(td, 'facts.json'), os.path.join(td, 'facts.md')
        write(fj, json.dumps({'contract_sha16': canon16}))
        write(fm, '# 合成の転記行の記録' + NL + NL + '- **転記行 A** — 合成の 7 トークン（2717「```」）' + NL + NL + CLAUSE + NL)
        words = '10時30分に凍結してください（自己検査・数のある逐語）'
        fz, rep, drec = make(words, '2026-10-01 10:30', facts_md=fm, facts_json=fj)
        lines = fz.split(NL)
        ok.append(('題名の印', MF.MARK in lines[0] and lines[0].startswith('# B′ の枠（草案11）' + MF.MARK)))
        ok.append(('凍結の一行が状態の行の次に一つ', lines[3].startswith('- **凍結**: 2026-10-01 10:30') and fz.count('- **凍結**:') == 1 and words in fz))
        ok.append(('§6 に転記行の記録の本文が逐語で入る', SUB6 in fz and '- **転記行 A** — 合成の 7 トークン（2717「```」）' in fz and (H6_FROZEN % (sha16f(fm), canon16)) in fz))
        ok.append(('草案に戻る', residual_diff(read(SRC), fz) == []))
        ok.append(('数の検査は零（§6 と凍結の一行の数は外）', '未登録 0' in rep))
        fz2, _, _ = make(words, '2026-10-01 10:30', facts_md=fm, facts_json=fj)
        ok.append(('同じ入力で同じ本文', fz2 == fz))
        # 止まるべき形
        bad_cases = []
        write(fj, json.dumps({'contract_sha16': '0' * 16}))
        try:
            make(words, '2026-10-01 10:30', facts_md=fm, facts_json=fj)
            bad_cases.append(('転記行の記録の正本が古い', False))
        except SystemExit:
            bad_cases.append(('転記行の記録の正本が古い', True))
        write(fj, json.dumps({'contract_sha16': canon16}))
        try:
            make(words, '2026-10-01 10:30', draft_sha16='F' * 16, facts_md=fm, facts_json=fj)
            bad_cases.append(('草案の SHA16 の違い', False))
        except SystemExit:
            bad_cases.append(('草案の SHA16 の違い', True))
        fz_bad = fz.replace('## 9. 読みの規則（先に凍結）', '## 9. 読みの規則（先に凍結・書き足し）')
        bad_cases.append(('草案に無い差を捕まえる', residual_diff(read(SRC), fz_bad) != []))
        dr2 = os.path.join(td, 'draft.md')
        src_ = read(SRC)
        assert src_.count('## 1. 問いの定義') == 1
        write(dr2, src_.replace('## 1. 問いの定義', '## 1. 問いの定義' + NL + NL + '層の数は 7919 だった。', 1))     # 7919 は正本に登録されていない数（器で確かめて選んだ）
        try:
            make(words, '2026-10-01 10:30', draft_path=dr2, draft_sha16=sha16f(dr2), facts_md=fm, facts_json=fj)
            bad_cases.append(('正本に無い数で止まる', False))
        except SystemExit:
            bad_cases.append(('正本に無い数で止まる', True))
        try:
            make('一行目' + NL + '二行目', '2026-10-01 10:30', facts_md=fm, facts_json=fj)
            bad_cases.append(('逐語の改行を先に拒む（U25）', False))
        except SystemExit as e_:
            bad_cases.append(('逐語の改行を先に拒む（U25）', '改行' in str(e_)))
        ok += bad_cases
    bad = [n for n, v in ok if not v]
    assert not bad, bad
    print('make_frozen_Bprime.py %s SELFTEST PASS（%d 項目・止まるべき形 %d）' % (VERSION, len(ok), len(bad_cases)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
