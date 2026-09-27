# -*- coding: utf-8 -*-
"""報告の最終版（`records/Bl3/results-Bl3-FINAL-2026-09-27.md`・逸脱 D-BLT1 の器 v2 の `--final`）を、逸脱の器とは別に書いた式で確かめる（起草者の確かめ・起草者の最終の見直しの前）。
確かめること:
 (一) 足した区画（中身の一行目が「- 【逸脱 D-BLT1】」で始まる機械の区画。台帳の一覧の行「- 【逸脱 D-BLT…】**」は凍結した器の出力）を除き、見出しと状態の行を戻すと、凍結した器の出力 `records/Bl3/results-Bl3.md` とバイトで同じ。
 (二) 並べ直しの表の行は、逆斜線を戻すと凍結の表の行と同じ並びで一度ずつ出る。表の行の、逃がしていない縦棒の数が見出しと同じ。
 (三) 機械の区画の中身の SHA16 が、区画の記録（-machine.json）と同じ。
 (四) 凍結した組み立ての器の走査（`build_report_Bl3.lint_report`）の違反 0。
 (五) 逸脱の器を `--final` でもう一度走らせると、置き場の最終版と同じ文になる（書かない）。
 (六) 足した区画の文に、正本の禁止語が無い。
 (七) 最終の検分を受けた草案の二つ目と最終版の違いは、決めた行（見出し・状態の行・凍結の記録の SHA16 の行・逸脱の一覧の D-BLT2 の行・頭の添えの区画・検分票の区画・起草者の欄の一行目・〈両方の外〉の注の一行）だけ（器とは別の数え方）。
 (八) 草案の二つ目のファイルは、最終の検分に出したコミット（3f467e7）のときと同じ（書き換えていない）。
書くのは本記録（md と json）だけ。
用法: python records/Bl3/final-check/check_final_Bl3.py
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
OUT_MD, OUT_JS = os.path.join(HERE, 'check-final-Bl3.md'), os.path.join(HERE, 'check-final-Bl3.json')
FINAL = 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'
TAG = '【逸脱 D-BLT1】'
T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
MB = RL.machine_block(T3)
FN = open(P(FINAL), encoding='utf-8').read().replace('\r\n', NL)
FZ = open(P('records/Bl3/results-Bl3.md'), encoding='utf-8').read().replace('\r\n', NL)
D2 = open(P('records/Bl3/results-Bl3-draft2.md'), encoding='utf-8').read().replace('\r\n', NL)
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
        return '〈両方の外〉の注の一行（起草者の最終の見直し）'
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
c_d2 = subprocess.run(['git', 'show', '3f467e7:records/Bl3/results-Bl3-draft2.md'], cwd=REPO, capture_output=True).stdout.decode('utf-8').replace('\r\n', NL)
add('(八) 草案の二つ目のファイルは、最終の検分に出したコミット 3f467e7 のときと同じ', c_d2 == D2, 'SHA16 %s' % s16(P('records/Bl3/results-Bl3-draft2.md')))
res = {'what': '報告の最終版の確かめ（逸脱の器とは別の式）', 'inputs': {FINAL: s16(P(FINAL)), 'records/Bl3/results-Bl3.md': s16(P('records/Bl3/results-Bl3.md')),
                                                  'records/Bl3/results-Bl3-draft2.md': s16(P('records/Bl3/results-Bl3-draft2.md')), 'tools/build_report_Bl3_devBLT1.py': s16(P('tools/build_report_Bl3_devBLT1.py')),
                                                  FINAL.replace('.md', '-machine.json'): s16(P(FINAL.replace('.md', '-machine.json')))},
       'checks': R, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(res, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
M = ['# 報告の最終版の確かめ（機械生成・`records/Bl3/final-check/check_final_Bl3.py`）', '',
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % kv for kv in res['inputs'].items()), '',
     '| 確かめ | 結果 | 中身 |', '|---|---|---|'] + ['| %s | %s | %s |' % (cell(x['what']), '合う' if x['ok'] else '外れ', cell(x['got'])) for x in R] + ['',
     '## 検分票', '',
     '- 対象: 報告の最終版（逸脱 D-BLT1 の器 v2 の `--final` の出力）。',
     '- 段階: 事後（組んだ後・起草者の最終の見直しと登録者最終確認の前）。',
     '- 凍結物の同定: 入力の SHA16（上）。凍結した器の出力は `records/Bl3/results-Bl3.md`。',
     '- 盲検の状態: 該当しない。',
     '- 敵対的検分: 逸脱の器の確かめ（作り直し・除いた戻し・草案の二つ目との違い）を、別に書いた式でもう一度行った。違いの行は、決めた行の種類に一つずつ当てた。',
     '- 系統の内訳: コーディネータ（Claude 系）一名（逸脱の器を書いた当人）。',
     '- COI記録: 器を書いた当人が確かめたので、同じ思い込みを二度通しうる。',
     '- 判定: %s。' % ('確かめとして確定' if all(x['ok'] for x in R) else '外れがある（止める）'),
     '- 本検分が確認していないこと: 最終版の文の読みの当否（起草者の最終の見直しで見る）。公開の置き場の表示（公開の後に確かめる）。', '',
     res['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('checks', len(R), '| ok', sum(x['ok'] for x in R), '|', [(x['what'][:4], x['ok']) for x in R], '|', [x['got'][:90] for x in R if x['what'].startswith('(七)')])
