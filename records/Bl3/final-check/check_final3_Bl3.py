# -*- coding: utf-8 -*-
"""報告の最終版の案（`records/Bl3/results-Bl3-FINAL-2026-09-27.md`・逸脱 D-BLT1 の器 v3 の `--final`・登録者裁定 D251・D253 の後）を、逸脱の器とは別に書いた式で確かめる（登録者最終確認の前）。
v2 の案の確かめ（`check_final_Bl3.py` → `check-final-Bl3.md`）は、v2 の案の記録として残す。確かめること:
 (一) 足した区画（中身の一行目が「- 【逸脱 D-BLT1】」で始まる機械の区画。台帳の一覧の行「- 【逸脱 D-BLT…】**」は凍結した器の出力）を除き、見出しと状態の行を戻すと、凍結した器の出力 `records/Bl3/results-Bl3.md` とバイトで同じ。
 (二) 並べ直しの表の行は、逆斜線を戻すと凍結の表の行と同じ並びで一度ずつ出る。表の行の、逃がしていない縦棒の数が見出しと同じ。
 (三) 機械の区画の中身の SHA16 が、区画の記録（-machine.json）と同じ。
 (四) 凍結した組み立ての器の走査（`build_report_Bl3.lint_report`）の違反 0。
 (五) 逸脱の器を `--final` でもう一度走らせると、置き場の最終版と同じ文になる（書かない）。
 (六) 足した区画の文に、正本の禁止語が無い。
 (七) 最終の検分を受けた草案の二つ目と最終版の違いは、決めた行（見出し・状態の行・凍結の記録の SHA16 の行・逸脱の一覧の D-BLT2 の行・頭の添えの区画・検分票の区画・起草者の欄の一行目・
      〈両方の外〉の注の二行・§5 の注の一行）だけ（器とは別の数え方）。
 (八) 草案の二つ目のファイルは、最終の検分に出したコミット（3f467e7）のときと同じ（書き換えていない）。
 (九) v2 の案（コミット 2d6dca6）から変わった行は、二度目の見直しの R-a〜R-d の直す行の六つだけで、直した行に、二度目の見直しの記録（コミット 352cfa9）の案の文があり、元の文が無い
      （案の文と元の文は、その記録の表の行から器で切り出す・手で打たない）。
 (十) 直した行のうち数を持つ行（〈両方の外〉の注の末の一行と §5 の注の一行）の数の並びが、v2 の案と同じ。
書くのは本記録（md と json）だけ。
用法: python records/Bl3/final-check/check_final3_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, subprocess, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
NL = chr(10)
BS = chr(92)
sys.path.insert(0, os.path.join(REPO, 'tools'))
import build_report_Bl3 as BR
import report_lint as RL

P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
git_show = lambda c, r: subprocess.run(['git', 'show', '%s:%s' % (c, r)], cwd=REPO, capture_output=True).stdout.decode('utf-8').replace('\r\n', NL)
OUT_MD, OUT_JS = os.path.join(HERE, 'check-final3-Bl3.md'), os.path.join(HERE, 'check-final3-Bl3.json')
FINAL = 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'
REV2, C_REV2, C_V2 = 'records/reviews/Bl3/results-final/final-read2/review2-final-Bl3.md', '352cfa9', '2d6dca6'
TAG = '【逸脱 D-BLT1】'
T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
MB = RL.machine_block(T3)
FN = open(P(FINAL), encoding='utf-8').read().replace('\r\n', NL)
FZ = open(P('records/Bl3/results-Bl3.md'), encoding='utf-8').read().replace('\r\n', NL)
D2 = open(P('records/Bl3/results-Bl3-draft2.md'), encoding='utf-8').read().replace('\r\n', NL)
V2 = git_show(C_V2, FINAL)
assert V2, 'v2 の案がコミットに無い'
R = []
add = lambda what, ok, got: R.append({'what': what, 'ok': bool(ok), 'got': got})
L = FN.split(NL)


def strip_added(Ls):
    keep, i, added = [], 0, []
    while i < len(Ls):
        if Ls[i] == MB['begin'] and i + 1 < len(Ls) and Ls[i + 1].startswith('- ' + TAG) and not Ls[i + 1].startswith('- ' + TAG + '**'):
            j = Ls.index(MB['end'], i)
            added.append((i, j))
            if keep and keep[-1] == '':
                keep.pop()
            i = j + 1
            continue
        keep.append(Ls[i])
        i += 1
    return keep, added


# (一)
keep, added = strip_added(L)
t_fn = keep[0]
keep[0] = '# B-lens 層三の結果（報告の草案・機械の組み立て）'
st = [k for k, l in enumerate(keep) if l.startswith('- 状態: **報告の最終版**')]
if len(st) == 1:
    keep[st[0]] = '- 状態: **報告の草案（結果の巡の前）**。'
add('(一) 足した区画を除き見出しと状態の行を戻すと凍結した器の出力とバイトで同じ', NL.join(keep) == FZ, '足した区画 %d・見出し「%s」・状態の行 %d' % (len(added), t_fn, len(st)))


# (二)
def tables(text):
    t = text.split(NL)
    out, k = [], 0
    while k < len(t) - 1:
        if t[k].startswith('| ') and re.match(r'^\|(---\|)+$', t[k + 1]):
            j = k + 2
            while j < len(t) and t[j].startswith('| '):
                j += 1
            out.append((k, t[k], t[k + 2:j]))
            k = j
        else:
            k += 1
    return out


esc = [(k, h, rows) for k, h, rows in tables(FN) if any(BS + '|' in r for r in rows)]
fz_rows = {h: rows for _, h, rows in tables(FZ) if any('|' in c for r in rows for c in r[2:-2].split(' | '))}
ok2 = [len([1 for h_ in fz_rows if h_ == h]) == 1 and [r.replace(BS + '|', '|') for r in rows] == fz_rows[h] and all(r.count('|') - r.count(BS + '|') == h.count('|') for r in rows) for k, h, rows in esc]
add('(二) 並べ直しの表は、逆斜線を戻すと凍結の表の行と同じ並びで一度ずつ出て、区切りの数が見出しと同じ', len(esc) == 3 and all(ok2) and len(fz_rows) == 3, '・'.join('%s…: 行 %d' % (h[:14], len(rows)) for _, h, rows in esc))
# (三)
side = json.load(open(P(FINAL.replace('.md', '-machine.json')), encoding='utf-8'))
hs = RL.block_hashes(FN, T3)
add('(三) 機械の区画の中身の SHA16 が区画の記録と同じ', hs == side['blocks'], '区画 %d・記録 %d・記録の器 %s' % (len(hs), len(side['blocks']), side.get('builder')))
# (四)
V, _ = BR.lint_report(FN, T3)
add('(四) 凍結した組み立ての器の走査の違反 0', not V, '違反 %d' % len(V))
# (五)
r = subprocess.run([sys.executable, P('tools/build_report_Bl3_devBLT1.py'), '--final'], cwd=REPO, capture_output=True, text=True, encoding='utf-8')
add('(五) 逸脱の器を --final でもう一度走らせると、置き場の最終版と同じ文になる（書かない）', r.returncode == 0 and '既にある出力と同じ' in r.stdout, (r.stdout.strip() or r.stderr.strip())[-80:].replace(REPO, '〈置き場〉'))
# (六)
PS = T3['print_strings']
bans = sorted(set(PS['value_word_ban']) | set(PS['mechanism_word_ban']) | set(PS['added_ban']) | set(PS['reading_never_ban']))
added_txt = NL.join(NL.join(L[a_:b_ + 1]) for a_, b_ in added)
hit = [w for w in bans if w in added_txt]
add('(六) 足した区画の文に正本の禁止語が無い', not hit, '禁止語 %d を見た・当たり %s' % (len(bans), hit))
# (七)
d2L = D2.split(NL)


def kind(line, Ls):
    """草案の二つ目か最終版の一行が、どの決めた行に当たるか（当たらなければ None）。"""
    if line.startswith('# B-lens 層三の結果（報告の'):
        return '見出し'
    if line.startswith('- 状態: **'):
        return '状態の行'
    if line.startswith('- 正本 `design/contrasts-Bl3.json` SHA16'):
        return '凍結の記録の SHA16 の行'
    if line.startswith('- 【逸脱 D-BLT2】'):
        return '逸脱の一覧の D-BLT2 の行'
    if line.startswith('- 「この大きさの加減では'):
        return '起草者の欄の一行目'
    if line.startswith('  - 等方の最上位の割合 '):
        return '〈両方の外〉の注の最上位の割合の一行（裁定 D251）'
    if line.startswith('  - これらは札と型を変えない。'):
        return '〈両方の外〉の注の末の一行（裁定 D253）'
    if line.startswith('- ' + TAG + '独立の再計算の範囲は'):
        return '§5 の注の一行（裁定 D253）'
    for pre, name in (('- ' + TAG + 'この草案は', '頭の添えの区画'), ('- ' + TAG + 'この最終版は', '頭の添えの区画'), ('- ' + TAG + '上の検分票は', '検分票の区画')):
        hs_ = [k for k, l in enumerate(Ls) if l == MB['begin'] and k + 1 < len(Ls) and Ls[k + 1].startswith(pre)]
        for k in hs_:
            if line in Ls[k + 1:Ls.index(MB['end'], k)]:
                return name
    return None


gone, came = [], []
for tg, i1, i2, j1, j2 in difflib.SequenceMatcher(None, d2L, L, autojunk=False).get_opcodes():
    if tg in ('replace', 'delete'):
        gone += d2L[i1:i2]
    if tg in ('replace', 'insert'):
        came += L[j1:j2]
kg, kc = [kind(l, d2L) for l in gone], [kind(l, L) for l in came]
kinds = sorted(set(k for k in kg + kc if k))
add('(七) 草案の二つ目と最終版の違いは決めた行だけ（器とは別の数え方）', None not in kg and None not in kc, '消えた行 %d・足された行 %d・当たった決めた行 %s' % (len(gone), len(came), kinds))
# (八)
c_d2 = git_show('3f467e7', 'records/Bl3/results-Bl3-draft2.md')
add('(八) 草案の二つ目のファイルは、最終の検分に出したコミット 3f467e7 のときと同じ', c_d2 == D2, 'SHA16 %s' % s16(P('records/Bl3/results-Bl3-draft2.md')))
# (九) v2 の案からの違いと、二度目の見直しの案の文
RV = git_show(C_REV2, REV2).split(NL)
row = {m.group(1): l for l in RV for m in [re.match(r'^\| (R-[a-d]) \|', l)] if m}
assert sorted(row) == ['R-a', 'R-b', 'R-c', 'R-d'], sorted(row)
cells = {k: v[2:-2].split(' | ') for k, v in row.items()}
an = {k: c[-1] for k, c in cells.items()}
fi = {k: c[3] for k, c in cells.items()}
new_a, old_a = re.search(r'（「(.*)」）$', an['R-a']).group(1), re.match(r'^「(.*?)」を', an['R-a']).group(1)
new_b, old_b = re.search(r'「(.*)」。あわせて', an['R-b']).group(1), re.search(r'一行目の「(.*?)」は', fi['R-b']).group(1)
new_c, old_c = re.match(r'^「(.*)」に直す（', an['R-c']).group(1), re.search(r'§5 の注の「(.*)」の「」の中は', fi['R-c']).group(1)
new_d, old_d = re.search(r'COI の行を「(.*?)」に直す', an['R-d']).group(1), re.search(r'COI の行は「(.*?)」と書く', fi['R-d']).group(1)
pre = {'R-a': '  - これらは札と型を変えない。', 'R-b': '- ' + TAG + 'この最終版は、', 'R-c': '- ' + TAG + '独立の再計算の範囲は',
       'R-d 四行目': '- ' + TAG + '最終の系統外の検分を受けた草案の二つ目', 'R-d 段階': '  - 段階: 結果の後。', 'R-d COI': '  - COI記録: 起草者は器と報告と起草者の欄を書いた当人で'}
at = {}
for k, p_ in pre.items():
    ix = [i for i, l in enumerate(L) if l.startswith(p_)]
    assert len(ix) == 1, (k, ix)
    at[k] = ix[0]
v2L = V2.split(NL)
changed = sorted({j for tg, i1, i2, j1, j2 in difflib.SequenceMatcher(None, v2L, L, autojunk=False).get_opcodes() if tg != 'equal' for j in range(j1, j2)})
same_len = len(v2L) == len(L)
want_ix = sorted(set(at.values()))
chk9 = {'R-a 案の文がある・元の文が無い': new_a in L[at['R-a']] and old_a not in L[at['R-a']],
        'R-b 案の文がある・元の文が無い': new_b in L[at['R-b']] and old_b not in L[at['R-b']],
        'R-c 案の文がある・元の文が無い': new_c in L[at['R-c']] and old_c not in L[at['R-c']],
        'R-d COI の案の文がある・元の文が無い': new_d in L[at['R-d COI']] and old_d not in L[at['R-d COI']],
        'R-d 頭の添えの一行目と四行目と段階の行に D251 と D253': all(('D251' in L[at[k]] and 'D253' in L[at[k]]) for k in ('R-b', 'R-d 四行目', 'R-d 段階')) and '起草者の最終の見直し' in L[at['R-d 段階']],
        '器の版 v3': ('`tools/build_report_Bl3_devBLT1.py` v3' in L[at['R-b']])}
s0 = [l for l in L if l.startswith('- 独立の再計算: 一段目')]
n_icchi, n_verdict = (s0[0].count('一致'), len(re.findall(r'） 一致', s0[0]))) if len(s0) == 1 else (None, None)
add('(九) v2 の案（%s）から変わった行は R-a〜R-d の直す行の六つだけで、直した行に二度目の見直しの記録（%s）の案の文があり、元の文が無い' % (C_V2, C_REV2),
    same_len and changed == want_ix and all(chk9.values()) and n_verdict == 2,
    '行の数が同じ %s・変わった行 %s（決めた行 %s）・%s・§0 の独立の再計算の行の「一致」は %s で、段の判定（括弧の後の「一致」）は %s' % (
        same_len, [i + 1 for i in changed], [i + 1 for i in want_ix], '・'.join('%s %s' % (k, '合う' if v else '外れ') for k, v in chk9.items()), n_icchi, n_verdict))
# (十) 数を持つ直した行の数の並び
nums = lambda l: [t for t, _, _, _ in RL.report_numbers(l)]
pairs = [(k, v2L[at[k]], L[at[k]]) for k in ('R-a', 'R-c')]
add('(十) 数を持つ直した行（R-a・R-c）の数の並びが v2 の案と同じ', all(nums(o) == nums(n) for _, o, n in pairs), '・'.join('%s 数 %d' % (k, len(nums(n))) for k, _, n in pairs))
res = {'what': '報告の最終版の案の確かめ（逸脱の器 v3・逸脱の器とは別の式）', 'inputs': {FINAL: s16(P(FINAL)), 'records/Bl3/results-Bl3.md': s16(P('records/Bl3/results-Bl3.md')),
                                                             'records/Bl3/results-Bl3-draft2.md': s16(P('records/Bl3/results-Bl3-draft2.md')), 'tools/build_report_Bl3_devBLT1.py': s16(P('tools/build_report_Bl3_devBLT1.py')),
                                                             FINAL.replace('.md', '-machine.json'): s16(P(FINAL.replace('.md', '-machine.json')))},
       'compared_with': {'v2_proposal': '%s:%s' % (C_V2, FINAL), 'review2': '%s:%s' % (C_REV2, REV2)},
       'checks': R, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(res, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
M = ['# 報告の最終版の案の確かめ（逸脱の器 v3・機械生成・`records/Bl3/final-check/check_final3_Bl3.py`）', '',
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % kv for kv in res['inputs'].items()),
     '- 比べた版: v2 の案 `%s`（コミット %s）・二度目の見直しの記録 `%s`（コミット %s）。v2 の案の確かめ（`check-final-Bl3.md`）は、v2 の案の記録として残す。' % (FINAL, C_V2, REV2, C_REV2), '',
     '| 確かめ | 結果 | 中身 |', '|---|---|---|'] + ['| %s | %s | %s |' % (cell(x['what']), '合う' if x['ok'] else '外れ', cell(x['got'])) for x in R] + ['',
     '## 検分票', '',
     '- 対象: 報告の最終版の案（逸脱 D-BLT1 の器 v3 の `--final` の出力・登録者裁定 D251・D253 の後）。',
     '- 段階: 事後（組んだ後・登録者最終確認の前）。',
     '- 凍結物の同定: 入力の SHA16（上）。凍結した器の出力は `records/Bl3/results-Bl3.md`。',
     '- 盲検の状態: 該当しない。',
     '- 敵対的検分: 逸脱の器の確かめ（作り直し・除いた戻し・草案の二つ目との違い）を、別に書いた式でもう一度行った。v2 の案からの違いの行を、二度目の見直しの記録の案の文と元の文に照らした（文は記録の表から器で切り出した）。',
     '- 系統の内訳: コーディネータ（Claude 系）一名（逸脱の器を書いた当人）。',
     '- COI記録: 器を書いた当人が確かめたので、同じ思い込みを二度通しうる。案の文を器が記録から切り出すので、案の文の打ち間違いは確かめで捕まるが、案の文そのものの当否は確かめない。',
     '- 判定: %s。' % ('確かめとして確定' if all(x['ok'] for x in R) else '外れがある（止める）'),
     '- 本検分が確認していないこと: 直した行の読みの当否（もう一度の検分を経ない・正本 `review_plan.no_more`）。公開の置き場の表示（push の後に確かめる）。', '',
     res['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('checks', len(R), '| ok', sum(x['ok'] for x in R), '|', [(x['what'][:4], x['ok']) for x in R])
for x in R:
    if not x['ok'] or x['what'].startswith(('(七)', '(九)', '(十)')):
        print(x['what'][:6], x['got'][:400])
