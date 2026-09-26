# -*- coding: utf-8 -*-
"""B-lens 層三（Bl3）の下見の前の凍結の後の確かめの記録を書く（裁定 D242）。数・行の番号・SHA16・コミットはすべて機械で出す（手で打たない）。
  (一) 凍結したとおりのコミット（凍結の記録を足したコミット）の中身を、凍結の記録と照らす（凍結物の SHA16・登録者の言葉・凍結の一行・組み立ての記録の行・差の記録・台帳の行）。
  (二) 凍結物を手元の道筋の形で走査し、見つけた外れ（数の検査の記録の一行の、代わりの原稿の一時の置き場の道筋）を書く。代わりの原稿を凍結版の原稿から組み直し、
       凍結の本文の器 `tools/make_frozen_Bl3.py` の `build`（組み立ての器 `tools/build_draft_Bl3.py`）で一時の置き場に組んで、凍結の本文と数の検査の記録が再現することを確かめる。
  (三) origin/main にある追跡しているファイルを同じ形で走査し、前からの外れ（公開済みの記録の手元の道筋）の数と置き場を書く（直さない・本の計算の後に登録者と相談する）。
器は変えない・リポジトリには本記録のほか何も書かない。既にある記録には書かない。凍結の記録を足したコミットが HEAD で、追跡しているファイルに変更が無いときだけ走る。
用法: python records/Bl3/prepilot_freeze_check_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, hashlib, datetime, tempfile, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import make_frozen_Bl3 as MFB

NL = chr(10)
OUT = os.path.join(HERE, 'prepilot-freeze-check-Bl3.md')
assert not os.path.exists(OUT), '既にある: ' + OUT
os.chdir(REPO)
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda p: s16b(open(p, 'rb').read())
git = lambda *a: subprocess.run(['git'] + list(a), capture_output=True, text=True, encoding='utf-8').stdout
gshow = lambda c, p: subprocess.run(['git', 'show', '%s:%s' % (c, p)], capture_output=True).stdout
rd = lambda p: open(p, encoding='utf-8').read()
FRP = 'records/Bl3/FREEZE-RECORD-Bl3.json'
c_fz = git('log', '--diff-filter=A', '--format=%H', '-1', '--', FRP).strip()
assert len(c_fz) == 40 and git('rev-parse', 'HEAD').strip() == c_fz, '凍結の記録を足したコミットが HEAD でない'
assert not git('status', '--porcelain', '--untracked-files=no').strip(), '追跡しているファイルに変更がある'
FR = json.loads(gshow(c_fz, FRP).decode('utf-8'))
assert s16(FRP) == s16b(gshow(c_fz, FRP))
fz = FR['frozen_sha16']
origin = git('rev-parse', 'origin/main').strip()
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')

# (一) 凍結の出力
bad_c = [k for k in fz if s16b(gshow(c_fz, k)) != fz[k]]
bad_w = [k for k in fz if not os.path.exists(k) or s16(k) != fz[k]]
W = rd('records/Bl3/prepilot-freeze-words-Bl3.md')
m_cut = re.search(r'^- 凍結の一行と凍結の記録に渡す部分（[^\n]*?）: 「(.*)」$', W, flags=re.M)
words_same = bool(m_cut) and m_cut.group(1) == FR['registrant_words']
T = rd(MFB.FOUT)
fl = [l for l in T.split(NL) if l.startswith('- **凍結**:')]
rec_line = '原稿 `%s` SHA16 %s' % (MFB.rel(MFB.FSRC), MFB.sha16f(MFB.FSRC))
DIFF = rd('records/Bl3/frozen-diff-Bl3.md').split(NL)
diff_ok = any(l.endswith('（(一) と (三) の外）: 無し') for l in DIFF) and any(l.endswith('凍結版の原稿を同じ手順で組み直した本文と凍結の本文: 同じ') for l in DIFF)
dr_rec = [k for k in fz if re.fullmatch(r'records/Bl3/dry-run-Bl3-\d{4}-\d{2}-\d{2}\.md', k)]
must = ['records/Bl3/colab-check-Bl3-session.json', 'records/Bl3/colab-check-Bl3.json', 'records/Bl3/tools/tools-log-Bl3.md', 'records/predictions/predictions-form-Bl3-v1.html']
ledger_rows = sum(1 for l in gshow(c_fz, 'records/FREEZE-RECORD.md').decode('utf-8').split(NL) if l.startswith('| ') and 'B-lens 層三 下見の前の凍結' in l)

# 手元の道筋の形（名そのものは器に書かない）
SEP = r'(?:\\\\|\\|/)'
PAT = {'user': re.compile(r'Users' + SEP + r'[^\\/\s"\'`<>|:*?]+' + SEP),
       'temp': re.compile(r'AppData' + SEP + r'Local' + SEP + r'Temp'),
       'session': re.compile(r'Temp' + SEP + r'claude' + SEP + r'[^\\/\s"\']+' + SEP + r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')}


def scan_text(t):
    hits = []
    for i, l in enumerate(t.split(NL), 1):
        for k, p in PAT.items():
            if p.search(l):
                hits.append((i, k))
    return hits


def as_text(b, path):
    if path.endswith(('.npz', '.gz', '.png', '.pdf', '.zip', '.pt', '.bin', '.safetensors')):
        return None
    try:
        return b.decode('utf-8')
    except UnicodeDecodeError:
        return None


# (二) 凍結物の走査と組み直し
fz_text, fz_hits = 0, {}
for k in fz:
    t = as_text(gshow(c_fz, k), k)
    if t is None:
        continue
    fz_text += 1
    h = scan_text(t)
    if h:
        fz_hits[k] = h
LINT_REL = MFB.rel(MFB.LINT)
assert list(fz_hits) == [LINT_REL] and len(fz_hits[LINT_REL]) == 1 and fz_hits[LINT_REL][0][1] == 'temp', ('凍結物の当たりが思ったものと違う', fz_hits)
lint_no = fz_hits[LINT_REL][0][0]
LOLD = rd(MFB.LINT).rstrip(NL).split(NL)
RX = re.compile(r'^- 束縛検査（原稿 `(.+)/frozen-standin\.src\.md（一覧を展開した後）`）: 違反 0$')
assert RX.match(LOLD[lint_no - 1]), '外れの行の形が思ったものと違う'
src = rd(MFB.FSRC)
sfl = [l for l in src.split(NL) if l.startswith('- **凍結**:')]
assert len(sfl) == 1
standin = src.replace(sfl[0], MFB.STANDIN)
standin16 = s16b(standin.encode('utf-8'))
with tempfile.TemporaryDirectory() as td:
    tmp = os.path.join(td, 'frozen-standin.src.md')
    open(tmp, 'w', encoding='utf-8', newline=NL).write(standin)
    assert MFB.sha16f(tmp) == standin16
    out, lint = os.path.join(td, 'rebuilt.md'), os.path.join(td, 'lint.md')
    MFB.build(tmp, out, '凍結版', lint)
    raw = rd(out)
    rec_tmp = '原稿 `%s` SHA16 %s' % (MFB.rel(tmp), standin16)
    n_rec_tmp = raw.count(rec_tmp)
    rebuilt = raw.replace(rec_tmp, rec_line).replace(MFB.STANDIN, sfl[0]).replace(MFB.rel(lint), LINT_REL)
    same_text = rebuilt == T
    # 組み直しの本文は一時の置き場に書くので、登録検査の行の文書の名は凍結の本文の置き場に置き換えて比べる
    LNEW = [l.replace(MFB.rel(out), MFB.rel(MFB.FOUT)) for l in rd(lint).rstrip(NL).split(NL)]
    n_doc_named = sum(MFB.rel(out) in l for l in rd(lint).split(NL))
lint_diff = [i + 1 for i in range(max(len(LOLD), len(LNEW))) if (LOLD[i] if i < len(LOLD) else None) != (LNEW[i] if i < len(LNEW) else None)]
lint_new_rx = bool(RX.match(LNEW[lint_no - 1])) if len(LNEW) >= lint_no else False
lint_new_zero = '- 違反の合計: 0' in LNEW
assert n_rec_tmp == 1 and same_text and lint_diff == [lint_no] and lint_new_rx and lint_new_zero, (n_rec_tmp, same_text, lint_diff, lint_new_rx, lint_new_zero)
# この記録を名で読む器と、中身を読む行
readers = sorted(p.replace(os.sep, '/') for p in glob.glob('tools/*.py') + glob.glob('tools/colab/*.py') if 'numbers-lint-FROZEN-Bl3' in rd(p) or 'MFB.LINT' in rd(p))
FZT = rd('tools/freeze_Bl3.py').split(NL)
read_lines = [i + 1 for i, l in enumerate(FZT) if re.search(r'open\(MFB\.LINT', l)]
assert readers == ['tools/freeze_Bl3.py', 'tools/make_frozen_Bl3.py'] and len(read_lines) == 1 and '違反の合計: 0' in FZT[read_lines[0] - 1], (readers, read_lines)
MFT = rd('tools/make_frozen_Bl3.py').split(NL)
write_lines = [i + 1 for i, l in enumerate(MFT) if l.strip() == 'build_frozen(FSRC, FOUT, LINT)']
list_lines = [i + 1 for i, l in enumerate(FZT) if "'records/Bl3/numbers-lint-FROZEN-Bl3.md'" in l]
assert len(write_lines) == 1 and len(list_lines) == 1, (write_lines, list_lines)
prev = {}
for p in ('records/B/numbers-lint-FROZEN-B.md', 'records/Blens/numbers-lint-FROZEN-Blens.md'):
    L_ = [l for l in rd(p).split(NL) if l.startswith('- 束縛検査（原稿 `')]
    prev[p] = len(L_) == 1 and re.search(r'`design/design-[A-Za-z]+-FROZEN\.src\.md（一覧を展開した後）`', L_[0]) is not None and not scan_text(L_[0])
assert all(prev.values()), prev
votes = sorted(x.replace(os.sep, '/') for x in glob.glob('records/reviews/Bl3/fixcheck/*/vote.md')) + ['records/reviews/Bl3/fixcheck/adoption-fixcheck-Bl3.md']
vote_mentions = sum(rd(p).count('numbers-lint-FROZEN') for p in votes)
RU = rd('records/Bl3/rulings-D242.md')
m_ru = re.search(r'^- 登録者の言葉（逐語・会話の記録 uuid `[0-9a-f-]+`・(\S+ \S+) 日本時間）', RU, flags=re.M)
assert m_ru

# (三) origin/main の追跡しているファイルの走査
names = [x for x in git('ls-tree', '-r', '--name-only', 'origin/main').split(NL) if x]
pr = subprocess.run(['git', 'cat-file', '--batch'], input=''.join('origin/main:%s\n' % n for n in names).encode('utf-8'), capture_output=True).stdout
pos, blobs = 0, {}
for n in names:
    hdr_end = pr.index(b'\n', pos)
    hdr = pr[pos:hdr_end].split(b' ')
    size = int(hdr[2])
    blobs[n] = pr[hdr_end + 1:hdr_end + 1 + size]
    pos = hdr_end + 1 + size + 1
o_text, o_hits = 0, {}
for n in names:
    t = as_text(blobs[n], n)
    if t is None:
        continue
    o_text += 1
    h = scan_text(t)
    if h:
        o_hits[n] = sorted({k for _, k in h})
kinds = {k: sum(1 for v in o_hits.values() if k in v) for k in PAT}
sess = sorted(n for n, v in o_hits.items() if 'session' in v)
in_fz = sorted(n for n in o_hits if n in fz)
bd = {d: sorted(n for n in sess if n.startswith('records/Bl3/tools/trials/%s/' % d)) for d in ('boot-dry-1', 'boot-dry-2')}
add = lambda p: git('log', '--diff-filter=A', '--format=%h %ad', '--date=format:%Y-%m-%d %H:%M', '-1', '--', p).strip()
bd_add = {d: sorted({add(n) for n in v}) for d, v in bd.items()}
san = 'records/Bl3/tools/trials/sanitize_paths.py'
san_add = add(san)
b3 = 'records/Bl3/tools/trials/boot-dry-3/summary.md'
b3_line = os.path.exists(b3) and '手元の置き場の道筋' in rd(b3) and '置き換えた' in rd(b3)
bd_summary = {d: os.path.exists('records/Bl3/tools/trials/%s/summary.md' % d) for d in bd}
sess_other = [n for n in sess if not any(n in v for v in bd.values())]
UID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
per_uid = {}
for n in sess:
    for u in {UID.search(m.group(0)).group(0) for m in PAT['session'].finditer(blobs[n].decode('utf-8'))}:
        per_uid[u] = per_uid.get(u, 0) + 1
uid_counts = sorted(per_uid.values(), reverse=True)
bd_forbidden = all(any(k in o_hits[n] for k in ('user', 'temp')) for v in bd.values() for n in v)
kind_ja = {'user': '利用者のフォルダの形', 'temp': 'OS の一時の置き場の形', 'session': '会話の作業の置き場の形〔会話の番号を含む〕'}

R = ['# B-lens 層三の下見の前の凍結の後の確かめ（機械生成・`prepilot_freeze_check_Bl3.py`・裁定 D242）', '',
     '- 凍結したとおりのコミット: %s（凍結の記録 `%s` を足したコミット）。確かめた時: %s（日本時間）。その時の origin/main: %s。' % (c_fz, FRP, now, origin[:7]),
     '- 本記録は凍結物ではない。凍結物は一字も変えていない（裁定 D242・逸脱は立てない・`records/Bl3/rulings-D242.md`）。', '',
     '## 1. 凍結の出力の確かめ', '',
     '- 凍結の記録: 版 %s・段 %s・凍結の時 %s（日本時間）・凍結物 %d 件・器の閉包 %d・逸脱 %d。' % (FR['version'], FR['stage'], FR['frozen_jst'], len(fz), len(FR['tools_import_closure']), len(FR['deviations'])),
     '- 凍結物の SHA16（改行を LF にそろえた）: 凍結したとおりのコミットの中身で %d 件のうち %d 件が凍結の記録と同じ（違い %s）。作業木でも %d 件が同じ（違い %s）。'
     % (len(fz), len(fz) - len(bad_c), '・'.join(bad_c) or '無し', len(fz) - len(bad_w), '・'.join(bad_w) or '無し'),
     '- 凍結の記録の登録者の言葉と、会話の記録から機械で切り出した部分（`records/Bl3/prepilot-freeze-words-Bl3.md`）: %s。' % ('同じ' if words_same else '**違う**'),
     '- 凍結の本文（`%s`）: 凍結の一行は %d つで、登録者の言葉がそのまま%s。組み立ての記録の行は `%s` の道筋と SHA16 %s を%s。'
     % (MFB.rel(MFB.FOUT), len(fl), '入っている' if len(fl) == 1 and FR['registrant_words'] in fl[0] else '**入っていない**', MFB.rel(MFB.FSRC), MFB.sha16f(MFB.FSRC), '指す' if T.count(rec_line) == 1 else '**指さない**'),
     '- 凍結の本文の差の記録（`records/Bl3/frozen-diff-Bl3.md`）: 組み直しと凍結の本文の差の残りは「無し」、凍結版の原稿を同じ手順で組み直した本文と凍結の本文は「同じ」: %s。' % ('そのとおり' if diff_ok else '**違う**'),
     '- 凍結物に入っているもの: 合成データの正式の記録（%s）・%s。%s' % ('・'.join('`%s`' % x for x in dr_rec), '・'.join('`%s`' % x for x in must), '' if all(x in fz for x in must) and len(dr_rec) == 1 else '**欠けがある**'),
     '- 台帳（`records/FREEZE-RECORD.md`）の「B-lens 層三 下見の前の凍結」の行: %d 行。' % ledger_rows, '',
     '## 2. 見つけた外れ（凍結物の数の検査の記録の一行・裁定 D242）', '',
     '- 走査: 凍結物 %d 件のうち文字で読める %d 件を、手元の道筋の三つの形（%s）で行ごとに走査した。当たりは `%s` の %d 行目の一つだけで、%s。'
     % (len(fz), fz_text, '・'.join(kind_ja.values()), LINT_REL, lint_no, kind_ja[fz_hits[LINT_REL][0][1]]),
     '- この行は束縛検査の原稿の名で、凍結の本文の器が組み立ての間に置いた代わりの原稿（凍結版の原稿の凍結の一行を、決まった代わりの行 `STANDIN` に替えた本文・裁定 D236）を、'
     'リポジトリからの相対の道筋（OS の一時の置き場の下）で書いている。組み立ての器 `tools/build_draft_Bl3.py` が、原稿の置き場をリポジトリからの相対の道筋で書くことから来る。',
     '- 原因: 裁定 D239 の直し（器の直しの確かめ C2-1）は、凍結の本文の組み立ての記録の行の一時の道筋だけを、凍結版の原稿の道筋と SHA16 に置き換えた（`tools/make_frozen_Bl3.py` の `build_frozen`）。'
     '同じ走りが書く数の検査の記録は置き換えの外に残った。直しの確かめの四票と採否の案（%s）は、この記録の名を%s。' % ('・'.join('`%s`' % p for p in votes), '挙げていない（数えて 0 回）' if vote_mentions == 0 else ' %d 回挙げている' % vote_mentions),
     '  前の段の凍結の数の検査の記録（%s）は、リポジトリの中の凍結版の原稿を指す: %s（代わりの原稿で組む形は層三が初めて）。' % ('・'.join('`%s`' % p for p in prev), 'そのとおり' if all(prev.values()) else '**違う**'),
     '- 影響: 束縛検査の結果（違反 0）は正しい（下の組み直しで確かめた）。器（`tools/` の下）でこの記録の名を持つのは %s の二つだけ。`tools/make_frozen_Bl3.py` は %d 行目で書き、`tools/freeze_Bl3.py` は %d 行目で凍結物に並べ、%d 行目（凍結の前の確かめ `prepilot_checks`）で「違反の合計: 0」の有無だけを読む。外れの行を読む器は無い。'
     % ('・'.join('`%s`' % p for p in readers), write_lines[0], list_lines[0], read_lines[0]),
     '- 組み直し（一時の置き場で行い、リポジトリには書かない）:',
     '  - 代わりの原稿（凍結版の原稿 `%s` の凍結の一行を `tools/make_frozen_Bl3.py` の `STANDIN` に替えた本文）の SHA16: %s。' % (MFB.rel(MFB.FSRC), standin16),
     '  - この代わりの原稿を、凍結の本文の器の `build`（組み立ての器 `tools/build_draft_Bl3.py`・凍結の走りと同じ札「凍結版」で、出力の本文と数の検査の記録の置き場だけを一時の置き場にした）で組むと、器は止まらず、組み立ての記録の行は代わりの原稿の道筋と SHA16 %s を %d 度だけ持つ。' % (standin16, n_rec_tmp),
     '  - 組んだ本文の組み立ての記録の行を凍結版の原稿の道筋と SHA16 に、代わりの行を凍結の一行に、数の検査の記録の置き場を凍結物の置き場に置き換えると、凍結の本文と%s。' % ('同じ' if same_text else '**違う**'),
     '  - 組み直しの数の検査の記録は、凍結物の数の検査の記録と、%d 行のうち %s 行目（代わりの原稿の置き場の名）のほかは同じ（組み直しの本文は一時の置き場に書いたので、登録検査の行が挙げる文書の名 %d か所は、凍結の本文の置き場に置き換えて比べた）。組み直しの違反の合計は 0。'
     % (len(LOLD), '・'.join(map(str, lint_diff)), n_doc_named),
     '- 裁定 D242（登録者・%s 日本時間・`records/Bl3/rulings-D242.md`）: 凍結物は凍結したとおりにコミットし、逸脱は立てない。外れは本記録に書く。' % m_ru.group(1), '',
     '## 3. 前からの外れ（公開済みの記録の手元の道筋・今は何もしない）', '',
     '- 走査: origin/main（%s）の追跡しているファイル %d 件のうち文字で読める %d 件を、同じ三つの形で走査した。' % (origin[:7], len(names), o_text),
     '- 三つの形のどれかを含むファイル: %d 件（%s）。層三の凍結物はこの中に %d 件。' % (len(o_hits), '・'.join('%s %d' % (kind_ja[k], kinds[k]) for k in PAT), len(in_fz)),
     '- 会話の作業の置き場の形を含むファイル（%d 件・会話の番号は %d 通りで、番号ごとのファイルの数は %s・番号そのものは書かない）:' % (len(sess), len(uid_counts), '・'.join(map(str, uid_counts)))] + ['  - `%s`' % n for n in sess] + [
     '- このうち層三の試し走りの記録の二つの置き場は、`boot-dry-1` の %d 件（最初のコミット %s）と `boot-dry-2` の %d 件（最初のコミット %s）。置き換えの台本 `%s` は、その後のコミット %s で入り（`boot-dry-3` と同じ時・`boot-dry-3` のまとめには台本の一行が%s）、'
     'この二つの置き場には当てていない（二つの置き場のファイルには、台本が残りを許さない形〔利用者のフォルダ・OS の一時の置き場〕が%s・二つの置き場にまとめは%s）。'
     % (len(bd['boot-dry-1']), '・'.join(bd_add['boot-dry-1']), len(bd['boot-dry-2']), '・'.join(bd_add['boot-dry-2']), san, san_add, 'ある' if b3_line else '無い', 'すべてに残る' if bd_forbidden else '**残らないものがある**', '無い' if not any(bd_summary.values()) else 'ある'),
     '- 走査は道筋の形だけで、鍵の値は探していない（鍵の値を見ない決まり）。',
     '- 直すかどうかは、本の計算の後に登録者と相談する（書き換えない決まりの逐語の記録も含まれ、履歴からは消えない）。', '',
     '## 検分票', '',
     '- 対象: 下見の前の凍結の出力（凍結したとおりのコミット %s）と、凍結の後に見つけた外れの扱い（裁定 D242）。' % c_fz[:7],
     '- 段階: 事後適用。確かめる項目（凍結の記録の言葉・凍結物の数と SHA16・凍結の一行・組み立ての記録の行・差の記録・相 check の写し・台帳の行・手元の道筋の走査）は確かめの前に立てた（凍結の走りの後）。何が出たらどうするかの表は前に書いていない。',
     '- 凍結物の同定: 凍結の記録 `%s`（SHA16 %s）・凍結物 %d 件・凍結したとおりのコミット %s。' % (FRP, s16(FRP), len(fz), c_fz[:7]),
     '- 盲検の状態: 該当しない（値を出す計算ではない）。',
     '- 敵対的検分: 凍結物の SHA16 を作業木だけでなくコミットの中身で照らした。外れの一行は、代わりの原稿を組み直して組み立ての器で組み、凍結の本文と数の検査の記録（外れの行のほか）が再現することを確かめた。'
     '登録者への報告（会話）で書いた「どの器も中身を読まない」という見立ては、器を走査して、中身を読む一行（違反の合計の有無）を見つけて改めた。同じ報告で試し走りの記録の二つの置き場をどちらも一つのコミットに入ったと書いた誤りも、コミットを機械で引いて改めた。同じ報告の会話の番号を含むファイルの数は、この会話の番号だけを数えたもので、本記録は番号を問わず数える（§3 の番号ごとの数）。',
     '- 系統の内訳: 起草者（Claude 系）一名。外の目は無い（裁定 D241 により直しの後の検分の巡は置かない）。',
     '- COI記録: 早く封印へ進みたい側に引かれている（推した A はその向きと同じ・裁定の候補にそう書いた）。自分の直しの漏れを小さく書く側にも引かれうるので、原因を影響より先に書き、影響の見立ては器の走査と組み直しで裏づけた。',
     '- 判定: 登録者に出せる水準（裁定は登録者のもの・D242）。',
     '- 本検分が確認していないこと: 起動器の相 pilot がこの凍結の記録で凍結の照らしを通るか（封印の後に走らせる）。push の後の GitHub 側の中身の SHA（push の後に照らす）。'
     '前からの外れの中の鍵の値の有無（探していない）。三つの形の外にある手元の情報（手元の機械の名など）。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
text = NL.join(R)
tg, sr = 'pasted' + '_content', 'system' + '-reminder'
assert not scan_text(text) and 'AppData' not in text and not any(x in text for x in ('<' + tg, '</' + tg, '<' + sr, sr + '>')), '本記録に手元の道筋か印が入る'
open(OUT, 'w', encoding='utf-8', newline=NL).write(text)
print('wrote', os.path.basename(OUT), '| lines', len(R), '| frozen ok', len(fz) - len(bad_c), '/', len(fz), '| lint line', lint_no, '| standin', standin16, '| rebuilt same', same_text,
      '| origin files', len(names), 'text', o_text, 'hits', len(o_hits), kinds, '| session files', len(sess), '| in frozen', len(in_fz))
