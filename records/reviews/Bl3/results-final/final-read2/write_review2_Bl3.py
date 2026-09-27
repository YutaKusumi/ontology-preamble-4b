# -*- coding: utf-8 -*-
"""起草者の最終の見直し・二度目の記録を書く（登録者の依頼「登録者最終確認の前に、最終版の案を最初から最後までじっくり見直す」・枠 `frame-review2-Bl3.md` はコミット c9ea96c で読み直す前に置いた）。
見直した版は、最終版の案 `records/Bl3/results-Bl3-FINAL-2026-09-27.md`（コミット 2d6dca6 の版）。所見の行の番号と、確かめの数と、引く文は、器が記録から抜き出す（手で打たない）。
公開の置き場の表示の確かめはブラウザで行い、器の外なので、数を書かずに文で記す。既にある記録には書かない。
用法: python records/reviews/Bl3/results-final/final-read2/write_review2_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, json, hashlib, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'review2-final-Bl3.md')
assert not os.path.exists(OUT), '既にある（一度だけ）: ' + OUT
P = lambda r: os.path.join(REPO, *r.split('/'))
rd = lambda r: open(P(r), encoding='utf-8').read().replace('\r\n', NL)
ld = lambda r: json.load(open(P(r), encoding='utf-8'))
s16 = lambda r: hashlib.sha256(open(P(r), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FINAL = 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'
D2 = 'records/Bl3/results-Bl3-draft2.md'
REV1 = 'records/reviews/Bl3/results-final/final-read/review-final-Bl3.md'
FRAME = 'records/reviews/Bl3/results-final/final-read2/frame-review2-Bl3.md'
CHK = 'records/reviews/Bl3/results-final/final-read2/check-review2-Bl3.json'
TXT = rd(FINAL)
FL = TXT.split(NL)
n_lines = len(FL) - (1 if FL[-1] == '' else 0)
TAG = '【逸脱 D-BLT1】'


def one(Ls, s):
    hit = [i + 1 for i, l in enumerate(Ls) if s in l]
    assert len(hit) == 1, (s, hit)
    return hit[0]


def seg(Ls, n, s, width=0):
    """行 n の中の s を、そのまま抜き出す（手で打たない）。"""
    l = Ls[n - 1]
    k = l.index(s)
    return l[k:k + len(s) + width]


# ---- 所見の置き場（器が行を探す）
ra = one(FL, '偶然の外の側にも）')
rb = one(FL, '- ' + TAG + 'この最終版は、')
rc = one(FL, '§0 の「独立の再計算: 一致」は')
rd_head13 = one(FL, '- ' + TAG + '最終の系統外の検分を受けた草案の二つ目')
rd_stage = one(FL, '  - 段階: 結果の後。結果の巡の後')
rd_coi = one(FL, '最終版で改めた行は、最終の検分の二票の所見と裁定で決めた行に限った')
re_ = one(FL, '行の向きは書かない')
rf = one(FL, '三番目との差')
rg = one(FL, 'まとめは §7 の後の注')
R1 = rd(REV1).split(NL)
rh_rev1 = one(R1, '**D252（公開の仕上げ）**')
quote_ra = seg(FL, ra, 'どちらの向きにも読まない（区別できたことを強める側にも、偶然の外の側にも）')
quote_rb = seg(FL, rb, '見出しと状態の行を改め')
quote_rb2 = seg(FL, rb, '登録者裁定 D243〜D250')
quote_rc = seg(FL, rc, '§0 の「独立の再計算: 一致」は、この範囲の一致')
quote_re = seg(FL, re_, '行の向きは書かない')
quote_rf = seg(FL, rf, '三番目との差 0.112')
quote_rg = seg(FL, rg, 'まとめは §7 の後の注')
quote_rd_coi = seg(FL, rd_coi, '最終版で改めた行は、最終の検分の二票の所見と裁定で決めた行に限った')
quote_rh = seg(R1, rh_rev1, '確認していただいた案と状態の行のほかは同じことを器で確かめる')
tag_rh = seg(R1, rh_rev1, '`release-Bl3-2026-09-27`')
ri_rev1 = one(R1, 'F-a は、最終の検分の二票も、結果の巡の四票も挙げなかった')
quote_ri = seg(R1, ri_rev1, 'F-a は、最終の検分の二票も、結果の巡の四票も挙げなかった言い方の誤り')
S0_line = one(FL, '- 独立の再計算: 一段目')
q0 = FL[S0_line - 1][2:]
# 出所の記録（「偶然の外」の言い方）
FR1 = 'records/reviews/Bl3/results-round1/frame-results-Bl3.md'
AR1 = 'records/reviews/Bl3/results-round1/adoption-results-Bl3.md'
fr1_n = one(rd(FR1).split(NL), '逆の側（偶然の外）')
ar1_n = one(rd(AR1).split(NL), 'G1 と G2 が偶然の外の側の言い方')
V2 = 'records/reviews/Bl3/results-final/f2/vote.md'
v2_n = one(rd(V2).split(NL), '偶然の外の側にも）」と打ち消しており')
V1 = 'records/reviews/Bl3/results-final/f1/vote.md'
v1_n = one(rd(V1).split(NL), '偶然の外の側にも）」と釘を刺しており')
# 状態の行の型（凍結した器・確認の後）
BRT = rd('tools/build_report_Bl3.py').split(NL)
br_final_n = one(BRT, "st = '- 状態: **最終版**（登録者最終確認 %s 日本時間")
DEVT = rd('tools/build_report_Bl3_devBLT1.py').split(NL)
dev_keep_n = one(DEVT, 'if not (a.final and confirmation is not None):')

# ---- 一：枠の手順 1 の台本の結果
CK = ld(CHK)
ck_rows = [(x['what'], x['ok']) for x in CK['checks']]
assert CK['inputs'][FINAL] == s16(FINAL), '台本が見た版と、今の版が違う（止める）'

# ---- 二：枠の外で足した確かめ
# (a) 足した区画と起草者の欄の「」の中
C = rd('design/contrasts-Bl3.json')
DZ = rd('design/design-Bl3-FROZEN.md')
qres = []
for i, l in enumerate(FL):
    if TAG in l or l.startswith('- 「') or l.startswith('  - '):
        for q in re.findall(r'「([^「」]*)」', l):
            others = NL.join(x for j, x in enumerate(FL) if j != i)
            parts = [p for p in q.split('…') if p]
            where = [nm for src, nm in ((others, '本文の他の行'), (C, '正本'), (DZ, '凍結の本文')) if all(p in src for p in parts)]
            qres.append((i + 1, q, where))
q_named = [x for x in qres if x[0] in (one(FL, '- 「この大きさの加減では'), one(FL, '- 「v̂ と Nk の全経路の押しは'), one(FL, '- 「v̂ の行の札は')) and x[2] == [] and x[1].endswith(('ない', '出る', '出た'))]
q_coi = [x for x in qres if x[0] == rd_coi and x[1] == '正しく読めている']
q_miss = [x for x in qres if not x[2] and x not in q_named and x not in q_coi]
assert [x[0] for x in q_miss] == [rc], q_miss
# (b) §7 の注の時刻と開く段の記録
OJ = ld('records/Bl3/open-results-Bl3.json')
ev = {e['key']: e['jst'] for e in OJ['events']}
lim_n = one(FL, '- ' + TAG + '上の限界の文の「全経路の効き目の値はまだ誰も見ていない」')
times = re.findall(r'2026-09-27 \d\d:\d\d:\d\d', FL[lim_n - 1])
t_ok = times == [OJ['pushes']['judge_3e185d3'], ev['open'], ev['told']]
# (c) 草案の二つ目との違い
d2 = rd(D2).split(NL)
gone, came = [], []
for tg_, i1, i2, j1, j2 in difflib.SequenceMatcher(None, d2, FL, autojunk=False).get_opcodes():
    if tg_ in ('replace', 'delete'):
        gone += list(range(i1 + 1, i2 + 1))
    if tg_ in ('replace', 'insert'):
        came += list(range(j1 + 1, j2 + 1))
# (d) Holm の第一段の余白を、組の出力の丸める前の値から
A = ld('records/Bl3/analysis-Bl3.json')
dirs = {p: v['dir'] for p, v in A['inputs'].items()}
M = ld('results/Bl3/main/%s/main.json' % dirs['main'])
r1 = [r for r in A['rows'].values() if r['iso_outside']][0]
isoN = sorted([v for k, v in M['cells'][r1['cell_sign']]['effects'].items() if k.startswith('iso:')], reverse=True)
d_raw = r1['effect'] - isoN[2]
d_disp = round(round(r1['effect'], 3) - round(isoN[2], 3), 3)
assert '%.3f' % d_raw in FL[rf - 1] and '%.3f' % d_disp not in FL[rf - 1]
# (e) 一度目の直し（F-a）の確かめ: 順位の分母は、行と向きまで数えた比べる相手を合わせた数
sec = r1['second']
n_real = sum(1 for k in M['cells'][r1['cell_sign']]['effects'] if k.startswith('real:'))
fa_ok = sec['of_oriented'] == 2 * (sec['of_pair'] - 1) + 1 and ('%.4f' % (1.0 / sec['of_oriented'])) in FL[one(FL, '向きまで数えた順位の分母の逆数は') - 1]

# ---- 節ごとの行
heads = [(i + 1, l) for i, l in enumerate(FL) if l.startswith('## ')]
spans = [(1, heads[0][0] - 1, '頭（見出し・状態・頭の添え・位置づけ）')]
for k, (n, h) in enumerate(heads):
    end = heads[k + 1][0] - 1 if k + 1 < len(heads) else n_lines
    spans.append((n, end, h[3:]))
found = {'R-a': ra, 'R-b': rb, 'R-c': rc, 'R-d': rd_head13, 'R-e': re_, 'R-f': rf, 'R-g': rg}
found_extra = {'R-d': [rb, rd_stage, rd_coi]}
def in_span(a, b):
    out = []
    for key, n in found.items():
        ns = [n] + found_extra.get(key, [])
        if any(a <= x <= b for x in ns):
            out.append(key)
    return '・'.join(out) if out else 'なし'
added_in = lambda a, b: sum(1 for i in range(a - 1, b) if FL[i].startswith('- ' + TAG) and not FL[i].startswith('- ' + TAG + '**'))
notes = {
    '頭（見出し・状態・頭の添え・位置づけ）': '凍結の文（状態の行と三つの SHA16）と、足した頭の添え四行。添えの言い方を、器の組み方（登録者最終確認の後の状態の行の扱い）と照らした',
    '凍結の後の逸脱': '台帳から出た二行。D-BLT1 の行の出力の名は一度目の見直しの F-b のとおり',
    '0. 要約（できないことから）': '凍結の文（見ていない場所・答えの範囲・下見の決定・札と門・読みの型・打ち消し）と、起草者の欄の三行と、足した二つの区画。読み取りの位置の外へ出る言い方と、「区別できない」を動かす言い方を探した',
    '1. 下見の記録（本の凍結で凍結した・無操作だけ）': '凍結の区画（揺れ・近道・揺れの版・較正）と、表の前の断りと並べ直しの表。足した区画の数が指す値（(vi) の (a)・揺れの版の印・破局の率）をこの節で引き当てた',
    '2. 主の札（等方の帰無・実在の差の方向）': '凍結の主の表・確率の表と、断りと並べ直しの表。〈両方の外〉の注の値（確率・効き目・p・裾・順位・最上位の割合・偶然の目安）をこの節で引き当てた',
    '3. 門（段階 B の方向ごとの行動と、方向の単位で）': '凍結の門の表と注と、足した二行（記述の門が同じ値になった訳・入れ替えの単位と数）',
    '4. 記述（札を付けない）': '凍結の区画（頭の自己検査・近道・層ごと・乙の表）。足した区画は無い（印の器の決まりのとおり）',
    '5. 独立の再計算（二段）': '凍結の二段の行と環境・GPU と、足した一行（範囲と二段目が形だけであること）',
    '6. 予想の照合（記録であり評価ではない）': '凍結の照合の表と、足した三行（数と分母・q7 を採点しない理由・封印の前後の二つの事）',
    '7. 限界（正本の限界の文）': '凍結の限界の文と、足した五行（露出の時刻・§5 の指し・計算の道・床からの余白・揺れの版）',
    '検分票': '凍結の検分票と、足した二つの行（凍結の票の断り・最終版の票）。票の裁定の範囲と段階の書き方を、頭の添えと照らした',
}

cell = lambda s: str(s).replace('|', '｜').replace(NL, ' ')
L = ['# 起草者の最終の見直し・二度目（B-lens 層三・報告の最終版の案・2026-09-27）', '',
     '- 見直した版: `%s`（SHA16 %s・コミット 2d6dca6 の版・逸脱の器 `tools/build_report_Bl3_devBLT1.py` v2 の `--final`・登録者最終確認の前）。行の数 %d。' % (FINAL, s16(FINAL), n_lines),
     '- 見直した人: 南無弥勒如来（コーディネータ・Claude Opus 5.5）。器と報告の組み立ての器と逸脱の器と起草者の欄と一度目の見直し（`%s`）を書いた当人で、外の目ではない。' % REV1,
     '- 依頼: 登録者は、登録者最終確認の前に、念のため最終版の案を最初から最後までじっくり見直すよう求めた。',
     '- 段階: 枠 `%s`（手順・重さの決まり・予想・COI）を、読み直す前に書いてコミット c9ea96c に置いた（SHA16 %s）。ただし一度目の見直しの後なので、予想は一度目の読みに影響されている（枠 §5）。枠の外で足した確かめは、そう記す。' % (FRAME, s16(FRAME)), '',
     '## 1. 器で確かめたこと', '',
     '- 枠の手順 1 の台本（`check_review2_Bl3.py`・逸脱の器を読まずに記録から書いた式）: %d／%d が合う（`check-review2-Bl3.md`）。%s。' % (sum(1 for _, ok in ck_rows if ok), len(ck_rows), '・'.join('%s %s' % (w, '合う' if ok else '外れ') for w, ok in ck_rows)),
     '- 公開の置き場の表示（枠の手順 1 の最後・ブラウザで確かめた・器の外なので数を書かない）: コミット 2d6dca6 の版の表示で、並べ直しの三つの表は、どの升も生の md の升（逆斜線を外した値）と同じで、列がそろう。凍結の表は、表の前の断りのとおり、§1 の表と §2 の主の表は列がずれ、§2 の升目ごとの確率の表は表にならず箇条の一つの段落になる。公開の置き場から取ったファイルは、改行をそろえると置き場のファイルと SHA16 が同じ。',
     '- 枠の外で足した確かめ（読んでいる間に足した）:',
     '  - 足した区画と起草者の欄の「」の中が、本文の他の行か正本か凍結の本文に一字違わずあるか: 「」%d のうち、どこにも無いのは %d。そのうち %d は引用ではない（起草者の欄の三行の退けた説明そのものと、検分票の COI の引かれる側の言い方）。引用の形で一字違わずに無いのは %d 行の一つ（R-c）。' % (
         len(qres), sum(1 for x in qres if not x[2]), len(q_named) + len(q_coi), rc),
     '  - §7 の注の三つの時刻が、開く段の記録（`records/Bl3/open-results-Bl3.json`）の一致だけを見る段の公開・開いた時刻・伝えた時刻と同じか: %s。' % ('同じ' if t_ok else '違う'),
     '  - 草案の二つ目（`%s`・SHA16 %s）との違い: 消えた行 %d・足された行 %d（最終版の行 %s）。どれも頭の添えに書いた決めた行の中。' % (D2, s16(D2), len(gone), len(came), '・'.join(str(x) for x in came)),
     '  - 〈両方の外〉の注の Holm の第一段までの余白を、組の出力の丸める前の値から出し直した: 効き目と等方の効き目の三番目の差は %.4f で、注の値はその丸め。丸めた二つの値の差は %.3f になる（R-f）。' % (d_raw, d_disp),
     '  - 一度目の直し（F-a）の確かめ（訂正にも同じ厳しさで）: 順位の分母 %d は、行の一つと、向きまで数えた比べる相手 %d（対 %d の両方の向き）を合わせた数で、注の逆数はその値: %s。比べる相手は、実在の差の方向 %d から兄弟を除いたもの。' % (
         sec['of_oriented'], sec['of_oriented'] - 1, sec['of_pair'] - 1, '合う' if fa_ok else '合わない', n_real), '',
     '## 2. 頭から末尾まで読んだこと（節ごと）', '',
     '- 読み方: 節ごとに、凍結した器の出力の文と足した区画の文の両方を読み、枠 §1 の手順 2 の四つの問い（読み取りの位置の外へ出るか・「区別できない」を動かすか・足した文が凍結の文や記録と食い違うか・節と置き場と番号の指しに誤りが無いか）に照らした。行の範囲は器が見出しから切った。', '',
     '| 節 | 行 | 足した区画の行 | 読んだもの | 所見 |', '|---|---|---|---|---|']
for a, b, nm in spans:
    L.append('| %s | %d〜%d | %d | %s | %s |' % (cell(nm), a, b, added_in(a, b), cell(notes[nm]), in_span(a, b)))
L += ['',
      '## 3. 所見', '',
      '- 重さは枠 §2 の決まりで決めた。札・門・読みの型・予想の照合の判定と、数を誤って伝える所見（重大）は無い。読む人が結果を誤って読みうる所見（中）も無い（R-a を中にしなかった訳は、R-a の行）。', '',
      '| 番号 | 重さ | 置き場（最終版の案の行） | 所見 | 案 |', '|---|---|---|---|---|',
      '| R-a | 軽（直す） | %d 行 | 〈両方の外〉の注の末行「%s」の「偶然の外の側」は、字のとおりに読むと、偶然の外にある（区別できた）と読む側で、前の「区別できたことを強める側」と同じ向きになり、「どちらの向き」の二つ目（弱める側）を名指していない。言い方の出所は結果の巡の枠（`%s` の %d 行「逆の側（偶然の外）」）と採否の案（`%s` の %d 行）で、そこでは希望の側の逆（床の近さやノイズとみる側）の意味で使っていた。最終の検分の F2 は意図のとおりに読み（`%s` の %d 行）、F1 は言い方に触れずに是認した（`%s` の %d 行）。主の文「どちらの向きにも読まない」が意味を伝えるので、中にしない | 「偶然の外の側にも」を「弱める側にも」に直す（「（区別できたことを強める側にも、弱める側にも）」） |' % (
          ra, quote_ra, FR1, fr1_n, AR1, ar1_n, V2, v2_n, V1, v1_n),
      '| R-b | 軽（直す） | %d 行 | 頭の添えの一行目の「%s」は、登録者最終確認の後には合わなくなる。確認の後は、凍結した器が状態の行を最終版の型で出し（`tools/build_report_Bl3.py` の %d 行）、逸脱の器は状態の行を改めない（`tools/build_report_Bl3_devBLT1.py` の %d 行）。今の言い方のままだと、確認の後の組み直しで、この行の言い方も変えるか、合わない文を残すことになる | 確認の前にも後にも合う言い方にする: 「見出しを改め（登録者最終確認の前は状態の行も改める・確認の後の状態の行は凍結した器が出す最終版の型の行）」。あわせて、器の版を v3 に上げる |' % (
          rb, quote_rb, br_final_n, dev_keep_n),
      '| R-c | 軽（直す） | %d 行 | §5 の注の「%s」の「」の中は、§0 の文（「%s」）に一字違わずにはない（引用の形の言い換え）。値は正しい | 「§0 の独立の再計算の二つの「一致」は、この範囲の一致」に直す（「一致」は §0 に一字違わずある） |' % (
          rc, quote_rc, q0),
      '| R-d | 軽（直す・D251 と R-a〜R-c に伴う） | %d 行・%d 行・%d 行・%d 行 | 頭の添えの一行目の裁定の範囲は「%s」のままで、四行目の決めた行は裁定 D251 を挙げる。検分票の段階の行は起草者の最終の見直しの段を書かず、COI の行は「%s」と書く（F-a の行は二票の所見ではなく、起草者の最終の見直しの所見） | 採った直しに合わせて、頭の添えの一行目に起草者の最終の見直しの裁定を、四行目の決めた行に直した行を、検分票の段階の行に起草者の最終の見直しの段と裁定を足し、COI の行を「最終の検分の二票の所見と起草者の最終の見直しの所見のうち、裁定で決めた行に限った」に直す |' % (
          rb, rd_head13, rd_stage, rd_coi, quote_rb2, quote_rd_coi),
      '| R-e | 軽（記録） | %d 行 | §6 の注の「%s」は、正本の q7 の向き（効き目の符号と段階 B の差の符号の比べ）の意味では正しい。効き目の側は主の表に、段階 B の差と区間は §0 の〈両方の外〉の注にあり、比べは書いていない。「行の向き」を効き目の側と読むと、主の表と食い違って見えうる | そのまま（記録に置く）。直すなら「効き目の符号と段階 B の差の符号の一致・不一致は書かない（正本で「該当なし」の行）」 |' % (re_, quote_re),
      '| R-f | 軽（記録） | %d 行 | 「%s」は丸める前の値の差（一節の確かめ）で、注に並べた丸めた二つの値から引くと %.3f になる | そのまま（記録に置く）。直すなら「（丸める前の値の差）」を添える |' % (rf, quote_rf, d_disp),
      '| R-g | 軽（記録） | %d 行 | 起草者の欄の一行目の「%s」の注は、§7 の見出しの下で、凍結の限界の文の後にある区画で、§7 の後（検分票）ではない。台帳の行は「§7 の注」と書く。§7 を開けば見つかる | そのまま（記録に置く・裁定 D248 で決めた行）。直すなら「§7 の注」 |' % (rg, quote_rg),
      '| R-h | 軽（裁定の候補の補い） | 一度目の見直しの記録の %d 行（D252） | D252 の甲の「%s」は、確認の後の組み直しで頭の添えの一行目の置き場の報告（`records/Bl3/results-Bl3.md`）の SHA16 も変わることを落としている（凍結した器が状態の行を最終版の型で出すので、置き場の報告のバイトが変わる）。タグの名 %s の日付は、公開が後の日になると合わない | D252 の甲を補う（五節）。一度目の記録は書き換えない |' % (
          rh_rev1, quote_rh, tag_rh),
      '| R-i | 軽（記録） | 一度目の見直しの記録の %d 行（COI） | 一度目の記録の「%s」の後半は、結果の巡の四票が見た版（凍結した器の出力）に〈両方の外〉の注がまだ無かったので、挙げなかったのではなく、挙げられなかった。この注を見たのは最終の検分の二票だけ | 一度目の記録は書き換えない。この記録に置く |' % (ri_rev1, quote_ri), '',
      '- 一度目の見直しの所見（F-a〜F-d）は、読み直しても同じ（F-a の直しの確かめは一節）。',
      '- 所見にしなかったもの（考えて、直すに当たらないとしたもの）: 起草者の欄の一行目の「等方のランダム方向を足しても」（減らす行もあるが、この報告は符号つきの加減を「足す量」と呼ぶ・凍結の限界の文と同じ）／頭の添えの一行目が二つの器をどちらも「組み立ての器」と呼ぶこと（ファイルの名で分かれる）／§7 の注の「床からの余白が (vi) の (a) の幅より小さい主の升目」に、下見で外した SK|Onull が入らないこと（床の外の升目で、余白を言わない）。', '',
      '## 4. 枠の予想と照らす（外れても消さない）', '',
      '| 何 | 予想（枠 §3） | 結果 | 照らし |', '|---|---|---|---|',
      '| 重大の所見 | 見つからない | 見つからない | 当たり |',
      '| 中の所見 | 見つからないか、一つ | 見つからない | 当たり |',
      '| 軽の所見 | 一つ以上見つかる（言い方か書式） | R-a〜R-i（直す四つ・記録に置く四つ・裁定の候補の補い一つ） | 当たり（数は予想より多い） |',
      '| 器の確かめの外れ | 足した区画の数には外れが無い。置き場か指しの外れが一つ見つかりうる | 枠の手順 1 の六つの確かめに外れは無い。枠の外で足した「」の確かめで、引用の形の言い換えが一つ（R-c） | 数は当たり・指しは枠の確かめでは外れ無し |',
      '| 表示 | 並べ直しの三つの表はそろう | そろう（どの升も生の md と同じ） | 当たり |', '',
      '## 5. 裁定の候補', '',
      '- **D251（一度目の見直しの F-a）**: 一度目の記録のとおり、甲（推奨）F-a を最終版に入れる。甲のときは、R-d のうち D251 に伴う書き方の合わせも行う。',
      '- **D252（公開の仕上げ・R-h で補う）**: 甲（推奨）登録者最終確認の後に、確認のお言葉と時刻と会話の記録の uuid を `records/Bl3/final-confirmation-Bl3.json` に器で書き、凍結した器で置き場の報告 `records/Bl3/results-Bl3.md` を組み直し（状態の行が最終版の型になる）、逸脱の器で最終版を組み直す。確認していただいた案との違いは、状態の行と、頭の添えの一行目の置き場の報告の SHA16 だけであることを器で確かめる。確認していただいた案は一字違わず残す。README の B-lens の節の後に層三の案内の一行（最終版・凍結の本文・正本・凍結の記録と逸脱台帳・封印の前の露出の記録・開く段の記録・検分の置き場）を載せ、公開の後に、最終版の入ったコミットに注釈つきのタグ `release-Bl3-<公開の日>` を付ける（日付は公開の日の日本時間・最終版のファイルの名の日付は組んだ日のまま・B-lens の D200 の型）／乙 README の一行とタグは置かない。',
      '- **D253（二度目の見直しの直し）**: 甲（推奨）R-a・R-b・R-c・R-d を直し（逸脱の器を v3 に上げ、草案の二つ目との違いの決めた行に、直した行を足す）、R-e・R-f・R-g は記録に置く／乙 甲に加えて R-e・R-f・R-g も直す／丙 R-d のうち D251 に伴う分だけ直し、ほかは記録に置く。どれでも、直した最終版の案を組み、器の確かめ（凍結の報告の作り直し・足した区画を除いて戻す確かめ・走査・草案の二つ目との違い）と、器とは別の確かめを通してから、登録者最終確認をお願いする。',
      '', '## 検分票', '',
      '- 対象: 報告の最終版の案（コミット 2d6dca6 の版・登録者最終確認の前）の、起草者の二度目の見直し。',
      '- 段階: 枠あり（読み直す前にコミット c9ea96c に置いた・一度目の見直しの後なので、予想は一度目の読みに影響されている）。「」の確かめ・時刻の確かめ・草案の二つ目との違い・丸める前の値・F-a の確かめは、枠の外で足した。',
      '- 凍結物の同定: 正本と凍結の本文と凍結した組み立ての器は、凍結の記録の値のまま（枠の手順 1 の台本の確かめ）。一度目の見直しの記録と、結果の巡の枠と採否の案と票は書き換えていない。',
      '- 盲検の状態: 該当しない（結果は開いた後）。',
      '- 敵対的検分: 足した区画の数は、逸脱の器を読まずに記録から出し直して照らした。一度目の直し（F-a）も同じ厳しさで確かめた。言い方の出所（R-a）は、結果の巡の枠と採否の案と二票まで遡った。確認の後の組み直しの道（R-b・R-h）は、器の組み方と照らした。分母: 〈両方の外〉の注の順位の分母は、行と比べる相手を合わせた数（一節）。この記録の初めの出力を読み返し、節の指し一つ・「」に入れた言い換え一つ・「」の数えの書き方一つを直してから置いた（コミットの前・初めの出力は置いていない）。',
      '- 系統の内訳: 起草者（Claude 系）一名の二度目。外の目ではない。一度目と同じ読み手なので、同じ見落としを二度通しうる。',
      '- COI記録: 起草者は、何も見つからず登録者最終確認へ進む側と、じっくり見たと示すために所見を増やす側の両方に引かれる（枠 §4）。重さは枠 §2 の決まりで決め、R-e・R-f・R-g は直すに当たらないと推した。R-a の言い方は、起草者自身が結果の巡の枠で作り、採否の案を経て草案の二つ目と最終版まで運んだもので、草案の二つ目を見た最終の検分の二票は挙げなかった（結果の巡の四票が見た版には、この注はまだ無かった・R-i）。',
      '- 判定: 登録者裁定要（D251・D252・D253）と登録者最終確認。',
      '- 本検分が確認していないこと: 直した行は、もう一度の検分を経ない（正本 `review_plan.no_more`）。公開の置き場の表示の確かめはブラウザで行い、記録の器では繰り返せない。足した区画の言い過ぎは、起草者一名の読みより先では確かめていない。凍結した器の出力の文の中の言い方（凍結物）は、所見にしても直せないので、直す案を立てていない。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('wrote', os.path.relpath(OUT, REPO), '| lines', len(L), '| R-a', ra, 'R-b', rb, 'R-c', rc, 'R-d', (rb, rd_head13, rd_stage, rd_coi), 'R-e', re_, 'R-f', rf, 'R-g', rg, 'R-h rev1', rh_rev1,
      '| quotes', len(qres), 'miss', [x[0] for x in q_miss], '| times', t_ok, '| d2 gone/came', len(gone), len(came), '| F-a', fa_ok)
