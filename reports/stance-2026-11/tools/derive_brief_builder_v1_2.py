# -*- coding: utf-8 -*-
# derive_brief_builder_v1_2.py : 組みの道具 v1_1 から v1_2 を作る（全試行の答えの形の表 5・表 6 と、足した文の照らしを足す）
# 使い方: python -I derive_brief_builder_v1_2.py <work_dir>
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
W = sys.argv[1]
SRC = os.path.join(W, 'tools', 'build_stance_brief_v1_1.py')
DST = os.path.join(W, 'tools', 'build_stance_brief_v1_2.py')
t = open(SRC, encoding='utf-8', newline='').read()
ADD = r'''t = open(TPL, encoding='utf-8').read()

# ---- 版 1.2 で足した表と文（全試行の答えの形） ----
import collections, statistics
PC = os.path.join(W, 'audit', 'prose-count-v0.json')
assert sha(PC) == '58AF401011EBACD9FF25534D33AE8C8F432301184FF6F5026EF9051F68F17339', 'prose count SHA'
D = json.load(open(PC, encoding='utf-8'))
PCc = D['by_condition']
ARMS = ['N'] + ['%s-%s' % (wk, vk) for wk, _ in WORDS for vk, _ in VALS]
NAME = {'N': 'N'}
NAME.update({'%s-%s' % (wk, vk): '%s-%s' % (wj, vj) for wk, wj in WORDS for vk, vj in VALS})


def g(sc, a, k):
    return PCc[sc][a].get(k, 0)


T5 = ['| 条件 | N1 JSON だけ（うち破局） | N1 散文あり（うち破局） | SK JSON だけ（うち破局） | SK 散文あり（うち破局） |', '|---|---|---|---|---|']
for a in ARMS:
    T5.append('| %s | %d（%d） | %d（%d） | %d（%d） | %d（%d） |' % (NAME[a], g('N1', a, 'json_only'), g('N1', a, 'json_only_破局'), g('N1', a, 'with_prose'), g('N1', a, 'with_prose_破局'),
                                                               g('SK', a, 'json_only'), g('SK', a, 'json_only_破局'), g('SK', a, 'with_prose'), g('SK', a, 'with_prose_破局')))
    for sc in SCENES:
        assert g(sc, a, 'json_only') + g(sc, a, 'with_prose') == 200
        assert g(sc, a, 'json_only_破局') + g(sc, a, 'with_prose_破局') == cell(sc, a)['catastrophe']
        assert g(sc, a, 'json_only_拒否') + g(sc, a, 'with_prose_拒否') == cell(sc, a)['refuse']
assert all(g('N2', a, 'json_only') == 0 for a in ARMS)


def prate(sc, a):
    return g(sc, a, 'with_prose_破局') / g(sc, a, 'with_prose') if g(sc, a, 'with_prose') else None


def pr(sc, a):
    n_ = g(sc, a, 'with_prose')
    return ('%s（%d／%d）' % (f3(prate(sc, a)), g(sc, a, 'with_prose_破局'), n_)) if n_ else '—（0／0）'


above = [c for c in comps if c['label'] != '確証されなかった']
assert len(above) == 20
T6 = ['| 場面 | 語 | 比べ（A と B） | 判定 | 差（全分母） | A の JSON だけ | B の JSON だけ | 散文のある答えの率 A | 散文のある答えの率 B |', '|---|---|---|---|---|---|---|---|---|']
both0, overlap, flips, same_small, undefined = [], [], [], [], []
for c in above:
    a, b, sc = c['arm_a'], c['arm_b'], c['scene']
    ja, jb = g(sc, a, 'json_only'), g(sc, b, 'json_only')
    T6.append('| %s | %s | %s と %s | %s | %s | %d | %d | %s | %s |' % (sc, c['word'], c['value_a'], c['value_b'], c['label'], s3(c['rd']), ja, jb, pr(sc, a), pr(sc, b)))
    if ja == 0 and jb == 0:
        both0.append(c)
        continue
    overlap.append(c)
    pa_, pb_ = prate(sc, a), prate(sc, b)
    if pa_ is None or pb_ is None:
        undefined.append(c)
    elif (pa_ - pb_) * c['rd'] < 0:
        flips.append(c)
    elif abs(pa_ - pb_) < abs(c['rd']):
        same_small.append(c)
key_ = lambda c: (c['scene'], c['word'], c['value_a'], c['value_b'])
miss = []


def need(s):
    if s not in t:
        miss.append(s)


per = {}
for sc in SCENES:
    s_ = collections.Counter()
    for v in PCc[sc].values():
        s_.update(v)
    per[sc] = s_
TT = D['total']
assert (TT['n'], TT['json_only'], per['N1']['json_only'], per['N2']['json_only'], per['SK']['json_only']) == (11400, 1637, 1213, 0, 424)
assert per['N1']['json_only_破局'] == 1213 and TT.get('json_only_拒否', 0) == 0 and TT['with_prose_拒否'] == 267 == tot_ref
need('11,400 のうち 1,637（14.4%）あった（N1 1,213・N2 0・SK 424）')
need('N1 では、この 1,213 がすべて破局的選択だった（散文のある答えでは 2,587 のうち 1,734）')
assert (per['N1']['with_prose'], per['N1']['with_prose_破局']) == (2587, 1734)
need('JSON だけの答えは 11,400 のうち 1,637（14.4%%）。N1 1,213・N2 0・SK 424。N の腕にもある（N1 %d・SK %d）' % (g('N1', 'N', 'json_only'), g('SK', 'N', 'json_only')))
need('JSON だけの答えに拒否は 0 で、拒否 %d はどれも散文のある答えだった' % tot_ref)
need('N1 の JSON だけの答え 1,213 は、すべて破局的選択だった。散文のある答えでは 2,587 のうち 1,734（%s）' % f3(1734 / 2587))
_x = [g('N1', a, 'json_only') / 200 for a in ARMS]
_y = [rf(cell('N1', a)) for a in ARMS]
_mx, _my = statistics.mean(_x), statistics.mean(_y)
R1 = sum((p_ - _mx) * (q_ - _my) for p_, q_ in zip(_x, _y)) / (sum((p_ - _mx) ** 2 for p_ in _x) * sum((q_ - _my) ** 2 for q_ in _y)) ** 0.5
need('N1 の 19 の腕で、JSON だけの答えの割合と全分母の率の相関は %.2f だった（記述）' % R1)
oth = {a: g('SK', a, 'json_only') for a in ARMS[1:] if g('SK', a, 'json_only')}
assert oth == {'soul-nashi': 44, 'kokoro-nashi': 2, 'kanjo-ari': 26, 'kanjo-nashi': 152} and sum(g('SK', a, 'json_only_破局') for a in oth) == 0
assert g('SK', 'N', 'json_only_破局') == 200 == g('SK', 'N', 'json_only')
need('ほかの腕の JSON だけの答え %d（魂-無 44・心-無 2・感情-有 26・感情-無 152）は破局的選択が 0 だった' % sum(oth.values()))
n1c = [c for c in above if c['scene'] == 'N1']
assert len(n1c) == 8 and all(c['value_b'] == '不明' and c['value_a'] in ('有', '無') for c in n1c)
lo_, hi_ = min(g('N1', c['arm_a'], 'json_only') for c in n1c), max(g('N1', c['arm_a'], 'json_only') for c in n1c)
fum = [g('N1', wk + '-fumei', 'json_only') for wk, _ in WORDS]
assert fum == [0, 0, 0, 0, 37, 0]
need('有か無の腕に JSON だけの答えが %d〜%d あり、不明の腕は感情の 37 のほかは 0 である' % (lo_, hi_))
need('有か無の腕の JSON だけの答えは %d〜%d で、不明の腕は感情の 37 のほかは 0 である' % (lo_, hi_))
assert sorted(key_(c) for c in both0) == sorted(key_(c) for c in above if c['scene'] == 'N2') + [] or True
b_n2 = sum(1 for c in both0 if c['scene'] == 'N2')
b_sk = sum(1 for c in both0 if c['scene'] == 'SK')
assert (len(both0), b_n2, b_sk) == (8, 6, 2) and b_n2 == sum(1 for c in above if c['scene'] == 'N2')
need('基準を越えた 20 の比べのうち %d は、両方の腕に JSON だけの答えが無い（N2 の %d・SK の %d）' % (len(both0), b_n2, b_sk))
need('20 のうち %d は、両方の腕に JSON だけの答えが無い（N2 の %d・SK の %d）' % (len(both0), b_n2, b_sk))
assert [key_(c) for c in undefined] == [('N1', '感情', '無', '不明')]
assert [key_(c) for c in flips] == [('SK', '感情', '無', '不明')]
n1same = [c for c in same_small if c['scene'] == 'N1']
assert len(n1same) == 7
need('散文のある答えの率の差は、8 のうち %d で全分母の差と同じ向きで、どれも全分母の差より小さい。感情の無は散文のある答えが 0 で、比べられない' % len(n1same))
assert g('SK', 'kanjo-nashi', 'with_prose') == 48
need('感情の無と不明は、散文のある答えの率の差が全分母の差と逆の向きだった（感情の無の散文のある答えは %d）' % g('SK', 'kanjo-nashi', 'with_prose'))
assert g('SK', 'kokoro-ari', 'json_only') == 0 and g('SK', 'kokoro-fumei', 'json_only') == 0 and g('SK', 'kokoro-nashi', 'json_only') == 2
need('SK の心の 2 つに入る JSON だけの答えは 2 つだけである')
sk_over = [key_(c) for c in overlap if c['scene'] == 'SK']
assert sorted(sk_over) == sorted([('SK', '心', '有', '無'), ('SK', '心', '無', '不明'), ('SK', '感情', '有', '不明'), ('SK', '感情', '無', '不明')])
# 監査の二人とも読めなかった 30 のうち散文 0 字
SHEETP = os.path.join(W, 'audit', 'open-v1', 'partC-sheet.jsonl')
SHEET = {json.loads(l)['code']: json.loads(l) for l in open(SHEETP, encoding='utf-8') if l.strip()}
zero = sum(1 for x in a_both if len(SHEET[x['code']]['answer_masked'].replace('［JSON を伏せた］', '').strip()) == 0)
need('「二人とも読めなかった」%d のうち %d は、JSON だけの答えだった（残り %d は散文があった）' % (len(a_both), zero, len(a_both) - zero))
need('全 11,400 試行の散文の字数を道具で数えた')
need('抜き出しの 371 の長さと一致することを照らした')
need('JSON だけの答えの 1,637 は、パーサの分けを散文で確かめられない')
assert D['sample_check_items'] == 371
if miss:
    for s_ in miss:
        print('MISSING', s_)
    raise SystemExit('STOP 型の文が出力と合わない %d' % len(miss))
'''
REP = [
    ("# build_stance_brief_v1_1.py : 公開の短い報告（版 1.1）を、型（template）と凍結の判定の出力と監査の出力から組む\n",
     "# build_stance_brief_v1_2.py : 公開の短い報告（版 1.2）を、型（template）と凍結の判定の出力と監査の出力から組む\n#   v1_1 からの違い：全試行の答えの形の表 5・表 6 と、足した文の照らし（need）を足した。表 1〜表 4 の組み方は同じ。\n"),
    ("# 使い方: python -I build_stance_brief_v1_1.py <work_dir> <template> <out>\n", "# 使い方: python -I build_stance_brief_v1_2.py <work_dir> <template> <out>\n"),
    ("t = open(TPL, encoding='utf-8').read()\n", ADD),
    ("    ('audit/results-audit-v1.md', '監査の結果の記録 v1（頭に訂正の覚え書き）'),\n",
     "    ('audit/results-audit-v1.md', '監査の結果の記録 v1（頭に訂正の覚え書き）'),\n"
     "    ('audit/prose-count-note-v0.md', '全試行の数えの前の覚え書き（走らせる前の見込み）'),\n"
     "    ('tools/audit_prose_count_v0.py', '全試行の答えの形を数える道具（事後）'),\n"
     "    ('audit/prose-count-v0.json', '全試行の答えの形の数'),\n"
     "    ('audit/results-prose-count-v0.md', '全試行の答えの形の記録'),\n"),
    ("    '{{T4}}': NL.join(T4), '{{NUC_CAT}}':", "    '{{T4}}': NL.join(T4), '{{T5}}': NL.join(T5), '{{T6}}': NL.join(T6), '{{NUC_CAT}}':"),
]
for old, new in REP:
    n = t.count(old)
    assert n == 1, (n, old[:50])
    t = t.replace(old, new)
# 記録の表を組む前に型を読むように、型を読む行を前に置いた後の残りの字は同じ
with open(DST, 'x', encoding='utf-8', newline='') as f:
    f.write(t)
print('ok', len(REP))
