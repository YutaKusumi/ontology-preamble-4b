# -*- coding: utf-8 -*-
"""報告の草案の二つ目（`records/Bl3/results-Bl3-draft2.md`・逸脱 D-BLT1）を、逸脱の器とは別に書いた式で確かめる（起草者の確かめ・最終の系統外の一票の前）。
確かめること:
 (一) 足した区画（中身の一行目が「- 【逸脱 D-BLT1】」で始まる機械の区画。台帳の一覧の行「- 【逸脱 D-BLT1】**」は凍結した器の出力）を除き、見出しと状態の行を戻すと、凍結した器の出力 `records/Bl3/results-Bl3.md` とバイトで同じ。
 (二) 並べ直しの表の行は、逆斜線を戻すと凍結の表の行と同じで、同じ並びで一度ずつ出る。表の行の、逃がしていない縦棒の数が見出しと同じ。
 (三) 草案の二つ目の機械の区画の中身の SHA16 が、区画の記録（-machine.json）と同じ。
 (四) 凍結した組み立ての器の走査（`build_report_Bl3.lint_report`）の違反 0。
 (五) 逸脱の器をもう一度走らせると、置き場の草案の二つ目と同じ文になる（書かない）。
 (六) 足した区画の文に、正本の禁止語が無い（(四) と別に数える）。
書くのは本記録（md と json）だけ。
用法: python records/Bl3/draft2-check/check_draft2_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
NL = chr(10)
BS = chr(92)
sys.path.insert(0, os.path.join(REPO, 'tools'))
import build_report_Bl3 as BR
import report_lint as RL

P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
OUT_MD, OUT_JS = os.path.join(HERE, 'check-draft2-Bl3.md'), os.path.join(HERE, 'check-draft2-Bl3.json')
TAG = '【逸脱 D-BLT1】'
T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
MB = RL.machine_block(T3)
D2 = open(P('records/Bl3/results-Bl3-draft2.md'), encoding='utf-8').read().replace('\r\n', NL)
FZ = open(P('records/Bl3/results-Bl3.md'), encoding='utf-8').read().replace('\r\n', NL)
R = []
add = lambda what, ok, got: R.append({'what': what, 'ok': bool(ok), 'got': got})

# (一)
L = D2.split(NL)
keep, i, added, added_lines = [], 0, [], 0
while i < len(L):
    if L[i] == MB['begin'] and i + 1 < len(L) and L[i + 1].startswith('- ' + TAG) and not L[i + 1].startswith('- ' + TAG + '**'):
        j = L.index(MB['end'], i)
        added.append((i, j))
        added_lines += j - i + 1
        if keep and keep[-1] == '':
            keep.pop()                                    # 足した区画の前の空の行も足したもの
        i = j + 1
        continue
    keep.append(L[i])
    i += 1
t_d2 = keep[0]
keep[0] = '# B-lens 層三の結果（報告の草案・機械の組み立て）'
st = [k for k, l in enumerate(keep) if l.startswith('- 状態: **報告の草案の二つ目**')]
if len(st) == 1:
    keep[st[0]] = '- 状態: **報告の草案（結果の巡の前）**。'
back = NL.join(keep)
add('(一) 足した区画を除き見出しと状態の行を戻すと凍結した器の出力とバイトで同じ', back == FZ, '足した区画 %d・足した行（区画の印を含む）%d・見出し「%s」・状態の行 %d' % (len(added), added_lines, t_d2, len(st)))

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


td2, tfz = tables(D2), tables(FZ)
esc = [(k, h, rows) for k, h, rows in td2 if any(BS + '|' in r for r in rows)]
fz_rows = {h: rows for _, h, rows in tfz if any('|' in c for r in rows for c in r[2:-2].split(' | '))}
ok2, info2 = [], []
for k, h, rows in esc:
    back_rows = [r.replace(BS + '|', '|') for r in rows]
    n_h = h.count('|')
    src = [rows_ for h_, rows_ in fz_rows.items() if h_ == h]
    ok2.append(len(src) == 1 and back_rows == src[0] and all(r.count('|') - r.count(BS + '|') == n_h for r in rows))
    info2.append('%s…: 行 %d' % (h[:14], len(rows)))
add('(二) 並べ直しの表は、逆斜線を戻すと凍結の表の行と同じ並びで一度ずつ出て、区切りの数が見出しと同じ', len(esc) == 3 and all(ok2) and len(fz_rows) == 3, '・'.join(info2))

# (三)
side = json.load(open(P('records/Bl3/results-Bl3-draft2-machine.json'), encoding='utf-8'))
hs = RL.block_hashes(D2, T3)
add('(三) 機械の区画の中身の SHA16 が区画の記録と同じ', hs == side['blocks'], '区画 %d・記録 %d・記録の器 %s' % (len(hs), len(side['blocks']), side.get('builder')))

# (四)
V, _ = BR.lint_report(D2, T3)
add('(四) 凍結した組み立ての器の走査の違反 0', not V, '違反 %d' % len(V))

# (五)
r = subprocess.run([sys.executable, P('tools/build_report_Bl3_devBLT1.py')], cwd=REPO, capture_output=True, text=True, encoding='utf-8')
add('(五) 逸脱の器をもう一度走らせると、置き場の草案の二つ目と同じ文になる（書かない）', r.returncode == 0 and '既にある出力と同じ' in r.stdout, (r.stdout.strip() or r.stderr.strip())[-80:].replace(REPO, '〈置き場〉'))

# (六)
PS = T3['print_strings']
bans = sorted(set(PS['value_word_ban']) | set(PS['mechanism_word_ban']) | set(PS['added_ban']) | set(PS['reading_never_ban']))
added_txt = NL.join(NL.join(L[a_:b_ + 1]) for a_, b_ in added)
hit = [w for w in bans if w in added_txt]
add('(六) 足した区画の文に正本の禁止語が無い', not hit, '禁止語 %d を見た・当たり %s' % (len(bans), hit))

res = {'what': '報告の草案の二つ目の確かめ（逸脱の器とは別の式）', 'inputs': {'records/Bl3/results-Bl3-draft2.md': s16(P('records/Bl3/results-Bl3-draft2.md')), 'records/Bl3/results-Bl3.md': s16(P('records/Bl3/results-Bl3.md')),
                                                         'tools/build_report_Bl3_devBLT1.py': s16(P('tools/build_report_Bl3_devBLT1.py')), 'records/Bl3/results-Bl3-draft2-machine.json': s16(P('records/Bl3/results-Bl3-draft2-machine.json'))},
       'checks': R, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(res, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
M = ['# 報告の草案の二つ目の確かめ（機械生成・`records/Bl3/draft2-check/check_draft2_Bl3.py`）', '',
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % kv for kv in res['inputs'].items()), '',
     '| 確かめ | 結果 | 中身 |', '|---|---|---|'] + ['| %s | %s | %s |' % (cell(x['what']), '合う' if x['ok'] else '外れ', cell(x['got'])) for x in R] + ['',
     '## 検分票', '',
     '- 対象: 報告の草案の二つ目（逸脱 D-BLT1 の器の出力）。',
     '- 段階: 事後（組んだ後・最終の系統外の一票の前）。',
     '- 凍結物の同定: 入力の SHA16（上）。凍結した器の出力は `records/Bl3/results-Bl3.md`。',
     '- 盲検の状態: 該当しない。',
     '- 敵対的検分: 逸脱の器の確かめ（作り直しと除いた戻し）を、別に書いた式でもう一度行った。器の走査とは別に、足した区画の禁止語を数えた。',
     '- 系統の内訳: コーディネータ（Claude 系）一名（逸脱の器を書いた当人）。',
     '- COI記録: 器を書いた当人が確かめたので、同じ思い込みを二度通しうる。数の正しさは逸脱の器が結果の巡の再現の記録と照らした（草案の二つ目の確かめの記録 `records/Bl3/results-Bl3-draft2-checks.json`）。',
     '- 判定: %s。' % ('確かめとして確定' if all(x['ok'] for x in R) else '外れがある（止める）'),
     '- 本検分が確認していないこと: 足した区画の文の読みの当否（最終の系統外の一票と起草者の最終の見直しで見る）。公開の置き場の表示（公開の後に確かめる）。', '',
     res['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('checks', len(R), '| ok', sum(x['ok'] for x in R), '|', [(x['what'][:6], x['ok']) for x in R])
