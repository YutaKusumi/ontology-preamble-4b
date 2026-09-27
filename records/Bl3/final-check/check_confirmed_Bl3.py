# -*- coding: utf-8 -*-
"""登録者最終確認の後に組み直した最終版を、逸脱の器とは別に書いた式で確かめる（登録者裁定 D252 の甲・二度目の見直しの R-h で補った文）。
確かめること:
 (一) 確認の記録（`records/Bl3/final-confirmation-Bl3.json`）の言葉・時刻・uuid が、会話の記録の登録者の発言と同じ（機械で切り出し直す）。
 (二) 確認していただいた案の写し（`records/Bl3/results-Bl3-proposal-confirmed-2026-09-27.md`）が、push したコミット 1ac0e4b の最終版の案とバイトで同じで、SHA16 が確認の記録の値と同じ。
 (三) 組み直した置き場の報告（`records/Bl3/results-Bl3.md`）と、1ac0e4b のときの置き場の報告の違いは、状態の行だけで、状態の行に確認の記録の時刻・uuid・言葉がある。
 (四) 組み直した最終版と確認していただいた案の違いは、状態の行と、頭の添えの一行目だけ。状態の行は置き場の報告の状態の行と同じ。頭の添えの一行目は、置き場の報告の SHA16 を
      1ac0e4b のときの値から今の値に替えると、確認していただいた案の行と同じ。
 (五) 最終版と置き場の報告の、凍結した組み立ての器の走査（`build_report_Bl3.lint_report`）の違反 0。
 (六) 最終版の足した区画を除き、見出しを戻すと、置き場の報告とバイトで同じ。
 (七) 最終版と置き場の報告の、機械の区画の中身の SHA16 が、区画の記録（-machine.json）と同じ。
 (八) 草案の二つ目のファイルは、最終の検分に出したコミット 3f467e7 のときと同じ。
 (九) 凍結した器で組み直した文が置き場の報告と同じ（メモリの中）。逸脱の器を `--final` でもう一度走らせると、置き場の最終版と同じ文になる（書かない）。
書くのは本記録（md と json）だけ。
用法: python records/Bl3/final-check/check_confirmed_Bl3.py <会話の記録 jsonl>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, hashlib, subprocess, difflib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
NL = chr(10)
sys.path.insert(0, os.path.join(REPO, 'tools'))
os.chdir(REPO)
import build_report_Bl3 as BR
import report_lint as RL

P = lambda r: os.path.join(REPO, *r.split('/'))
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
s16 = lambda r: s16b(open(P(r), 'rb').read())
git_b = lambda c, r: subprocess.run(['git', 'show', '%s:%s' % (c, r)], cwd=REPO, capture_output=True).stdout
rd = lambda r: open(P(r), encoding='utf-8').read().replace('\r\n', NL)
jst = lambda ts: (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
OUT_MD, OUT_JS = os.path.join(HERE, 'check-confirmed-Bl3.md'), os.path.join(HERE, 'check-confirmed-Bl3.json')
FINAL, FROZ, COPY, CONF = 'records/Bl3/results-Bl3-FINAL-2026-09-27.md', 'records/Bl3/results-Bl3.md', 'records/Bl3/results-Bl3-proposal-confirmed-2026-09-27.md', 'records/Bl3/final-confirmation-Bl3.json'
C_PROP = '1ac0e4b'
TAG = '【逸脱 D-BLT1】'
T3 = json.load(open(P('design/contrasts-Bl3.json'), encoding='utf-8'))
MB = RL.machine_block(T3)
CJ = json.load(open(P(CONF), encoding='utf-8'))
R = []
add = lambda what, ok, got: R.append({'what': what, 'ok': bool(ok), 'got': got})
# (一)
U = []
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        o = json.loads(line)
    except Exception:
        continue
    c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and 'toolUseResult' not in o and isinstance(c, str):
        U.append((o.get('uuid'), o.get('timestamp'), c))
hits = [m for m in U if 'それでは、D252 のとおりに進めてください' in m[2]]
ok1 = len(hits) == 1 and (hits[0][0], jst(hits[0][1]), hits[0][2].strip()) == (CJ['uuid'], CJ['when_jst'], CJ['words'])
add('(一) 確認の記録の言葉・時刻・uuid が会話の記録の登録者の発言と同じ', ok1, '当たり %d・時刻 %s・uuid %s・言葉の字数 %d' % (len(hits), CJ['when_jst'], CJ['uuid'], len(CJ['words'])))
# (二)
prop_b = git_b(C_PROP, FINAL)
copy_b = open(P(COPY), 'rb').read()
add('(二) 確認していただいた案の写しが %s の最終版の案とバイトで同じで、SHA16 が確認の記録の値と同じ' % C_PROP, prop_b and copy_b == prop_b and s16b(copy_b) == CJ['proposal_sha16'],
    '写しの SHA16 %s・確認の記録の値 %s' % (s16b(copy_b), CJ['proposal_sha16']))
# (三)
fz_old = git_b(C_PROP, FROZ).decode('utf-8').replace('\r\n', NL).split(NL)
fz_new = rd(FROZ).split(NL)
d3 = [i for i in range(max(len(fz_old), len(fz_new))) if i >= len(fz_old) or i >= len(fz_new) or fz_old[i] != fz_new[i]]
st_new = fz_new[d3[0]] if len(d3) == 1 else ''
ok3 = len(fz_old) == len(fz_new) and len(d3) == 1 and fz_old[d3[0]].startswith('- 状態: **') and st_new.startswith('- 状態: **最終版**（登録者最終確認 ') \
      and CJ['when_jst'] in st_new and CJ['uuid'] in st_new and ('逐語「%s」' % CJ['words']) in st_new
add('(三) 置き場の報告の %s からの違いは状態の行だけで、状態の行に確認の記録の時刻・uuid・言葉がある' % C_PROP, ok3, '違う行 %s' % [i + 1 for i in d3])
# (四)
cp = copy_b.decode('utf-8').replace('\r\n', NL).split(NL)
fn = rd(FINAL).split(NL)
d4 = sorted({j for tg, i1, i2, j1, j2 in difflib.SequenceMatcher(None, cp, fn, autojunk=False).get_opcodes() if tg != 'equal' for j in range(j1, j2)})
h1 = [i for i, l in enumerate(fn) if l.startswith('- ' + TAG + 'この最終版は、')]
st_i = [i for i, l in enumerate(fn) if l.startswith('- 状態: **')]
old_s, new_s = s16b(git_b(C_PROP, FROZ)), s16(FROZ)
ok4 = len(cp) == len(fn) and len(h1) == 1 and len(st_i) == 1 and d4 == sorted([st_i[0], h1[0]]) and fn[st_i[0]] == st_new \
      and cp[h1[0]].count('（SHA16 %s）' % old_s) == 1 and cp[h1[0]].replace('（SHA16 %s）' % old_s, '（SHA16 %s）' % new_s) == fn[h1[0]] and old_s != new_s
add('(四) 最終版と確認していただいた案の違いは状態の行と頭の添えの一行目だけで、頭の添えの一行目は置き場の報告の SHA16 を替えると同じ', ok4,
    '違う行 %s・置き場の報告の SHA16 %s → %s' % ([i + 1 for i in d4], old_s, new_s))
# (五)
V1, _ = BR.lint_report(rd(FINAL), T3)
V2, _ = BR.lint_report(rd(FROZ), T3)
add('(五) 最終版と置き場の報告の走査の違反 0', not V1 and not V2, '最終版 %d・置き場の報告 %d' % (len(V1), len(V2)))
# (六)
keep, i, n_add = [], 0, 0
while i < len(fn):
    if fn[i] == MB['begin'] and i + 1 < len(fn) and fn[i + 1].startswith('- ' + TAG) and not fn[i + 1].startswith('- ' + TAG + '**'):
        j = fn.index(MB['end'], i)
        if keep and keep[-1] == '':
            keep.pop()
        i, n_add = j + 1, n_add + 1
        continue
    keep.append(fn[i])
    i += 1
t_fn = keep[0]
keep[0] = '# B-lens 層三の結果（報告の草案・機械の組み立て）'
add('(六) 最終版の足した区画を除き見出しを戻すと、置き場の報告とバイトで同じ', NL.join(keep) == rd(FROZ), '足した区画 %d・見出し「%s」' % (n_add, t_fn))
# (七)
sides = [(r_, json.load(open(P(r_.replace('.md', '-machine.json')), encoding='utf-8'))) for r_ in (FINAL, FROZ)]
ok7 = all(RL.block_hashes(rd(r_), T3) == sd['blocks'] for r_, sd in sides)
add('(七) 最終版と置き場の報告の機械の区画の中身の SHA16 が区画の記録と同じ', ok7, '・'.join('%s 区画 %d（記録の器 %s）' % (os.path.basename(r_), len(sd['blocks']), sd.get('builder')) for r_, sd in sides))
# (八)
add('(八) 草案の二つ目のファイルは、最終の検分に出したコミット 3f467e7 のときと同じ', git_b('3f467e7', 'records/Bl3/results-Bl3-draft2.md') == open(P('records/Bl3/results-Bl3-draft2.md'), 'rb').read(),
    'SHA16 %s' % s16('records/Bl3/results-Bl3-draft2.md'))
# (九)
T3_, FR, A, preds, meta, confirmation = BR.load_inputs()
marks = json.load(open(P('records/Bl3/report-marks-Bl3.json'), encoding='utf-8'))
rejected = rd('records/Bl3/results-rejected-lines-Bl3.md')
same_fz = BR.build(T3_, A, preds, meta, FR.get('deviations') or [], marks, rejected, confirmation, False) == rd(FROZ)
r = subprocess.run([sys.executable, P('tools/build_report_Bl3_devBLT1.py'), '--final'], cwd=REPO, capture_output=True, text=True, encoding='utf-8')
add('(九) 凍結した器で組み直した文が置き場の報告と同じ（メモリの中）・逸脱の器を --final でもう一度走らせると置き場の最終版と同じ文になる（書かない）',
    same_fz and confirmation == CJ and r.returncode == 0 and '既にある出力と同じ' in r.stdout, '凍結した器 %s・逸脱の器 %s' % ('同じ' if same_fz else '違う', (r.stdout.strip() or r.stderr.strip())[-60:].replace(REPO, '〈置き場〉')))
res = {'what': '登録者最終確認の後に組み直した最終版の確かめ（逸脱の器とは別の式・登録者裁定 D252）',
       'inputs': {x: s16(x) for x in (FINAL, FROZ, COPY, CONF, 'tools/build_report_Bl3_devBLT1.py', 'tools/build_report_Bl3.py')},
       'compared_with': {'confirmed_proposal': '%s:%s' % (C_PROP, FINAL), 'frozen_report_before': '%s:%s' % (C_PROP, FROZ)},
       'checks': R, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
json.dump(res, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
M = ['# 登録者最終確認の後の最終版の確かめ（機械生成・`records/Bl3/final-check/check_confirmed_Bl3.py`）', '',
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % kv for kv in res['inputs'].items()),
     '- 比べた版: 確認していただいた案 `%s`（コミット %s）・そのときの置き場の報告 `%s`。' % (FINAL, C_PROP, FROZ), '',
     '| 確かめ | 結果 | 中身 |', '|---|---|---|'] + ['| %s | %s | %s |' % (cell(x['what']), '合う' if x['ok'] else '外れ', cell(x['got'])) for x in R] + ['',
     '## 検分票', '',
     '- 対象: 登録者最終確認の後に組み直した最終版（逸脱 D-BLT1 の器 v3 の `--final`）と置き場の報告（凍結した組み立ての器の出力）。',
     '- 段階: 事後（組み直した後・公開の push の前）。',
     '- 凍結物の同定: 入力の SHA16（上）。確認していただいた案はコミット %s の版で、写しを一字違わず残した。' % C_PROP,
     '- 盲検の状態: 該当しない。',
     '- 敵対的検分: 確認していただいた案と最終版の違いを、決めた二行（状態の行・頭の添えの一行目の置き場の報告の SHA16）に一つずつ当てた。登録者の言葉は会話の記録から切り出し直して照らした。',
     '- 系統の内訳: コーディネータ（Claude 系）一名（器を書いた当人）。',
     '- COI記録: 器を書いた当人が確かめたので、同じ思い込みを二度通しうる。',
     '- 判定: %s。' % ('確かめとして確定' if all(x['ok'] for x in R) else '外れがある（止める）'),
     '- 本検分が確認していないこと: 公開の置き場での表示（push の後に確かめる）。確認していただいた案の読みの当否（登録者最終確認で終わった）。', '',
     res['clause'], '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('checks', len(R), '| ok', sum(x['ok'] for x in R), '|', [(x['what'][:4], x['ok']) for x in R])
for x in R:
    print(x['what'][:6], x['got'][:200])
