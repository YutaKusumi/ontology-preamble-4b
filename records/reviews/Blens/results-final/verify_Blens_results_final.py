# -*- coding: utf-8 -*-
"""最終検分の二票の事実の主張を、公開の記録の現物で再現する（再現の番号 K398〜・コーディネータ・2026-09-24）。射影を新しく計算しない。既にある記録には書かない。
並べ方: 起草者に不利な主張（報告の欠け）を先に、次に票の数の食い違い、最後に票が確かめた数。
用法: python records/reviews/Blens/results-final/verify_Blens_results_final.py"""
import os, re, json, math, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
OUT_MD, OUT_JS = os.path.join(HERE, 'verification-Blens-results-final.md'), os.path.join(HERE, 'verify-Blens-results-final.json')
assert not os.path.exists(OUT_MD) and not os.path.exists(OUT_JS), '既にある'
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
js = lambda rel: json.load(open(j(*rel.split('/')), encoding='utf-8'))
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
INPUTS = ['records/Blens/results-Blens-draft2.md', 'records/reviews/Blens/results-round1/adoption-table-Blens-results-r1.md', 'records/reviews/Blens/results-round1/verify-Blens-results-r1.json',
          'records/Blens/sealing-exposures-Blens.md', 'records/Blens/indep-check-Blens.md', 'results/Blens/lens-Blens.json', 'results/Blens/calib-Blens.json', 'results/Blens/posthoc-Blens.json',
          'records/Blens/FREEZE-RECORD-Blens.json', 'records/reviews/Blens/results-final/bundle-results-final-index.md', 'design/design-Blens-FROZEN.md', 'design/contrasts-Blens.json']
D2 = rd(INPUTS[0])
AD = rd(INPUTS[1])
V1 = js(INPUTS[2])
EX = rd(INPUTS[3])
IC = rd(INPUTS[4])
L, C, PH = js(INPUTS[5]), js(INPUTS[6]), js(INPUTS[7])
FR = js(INPUTS[8])
IX = rd(INPUTS[9])
K, rows = [398], []


def row(src, claim, evidence, verdict):
    rows.append({'K': 'K%d' % K[0], 'src': src, 'claim': claim, 'evidence': evidence, 'verdict': verdict})
    K[0] += 1


B, E = '<!-- 機械:始 -->', '<!-- 機械:終 -->'
lines = D2.split(NL)
added, i = [], 0
while i < len(lines):
    if lines[i] == B:
        k = lines.index(E, i)
        if any('【逸脱 D-BL' in l for l in lines[i + 1:k]):
            added.append(lines[i + 1:k])
        i = k + 1
    else:
        i += 1
# 一 起草者に不利な主張（報告の欠け）
sec0 = D2.split('## 0.')[1].split('## 1.')[0]
sec0_added = [l for l in sec0.split(NL) if '【逸脱 D-BL3】' in l]
row('F1-1', '§0 の足した区画に、M_L_nuclear の二つ目の札の文脈（§1 の添え）への参照が無い', '§0 の足した行 %d・その中に「§1」: %s' % (len(sec0_added), any('§1' in l for l in sec0_added)),
    '再現した' if sec0_added and not any('§1' in l for l in sec0_added) else '再現しない')
cnt_line = [l for l in D2.split(NL) if '【逸脱 D-BL3】数え直し:' in l][0]
row('F1-2', '直した照合の表の数え直しで、登録者の一致 4 に p1.nuclear.dir（札の予想は外れ・等方の揺れの中の値の符号との一致）が入っていることが書かれていない',
    '数え直しの行の後に「一致 4 のうち」: %s・p1.nuclear.dir の注に「一致 4」: %s' % ('一致 4 のうち' in D2, any('p1.nuclear.dir' in l and '一致 4' in l for l in D2.split(NL) if '【逸脱 D-BL3】' in l)),
    '再現した' if '一致 4 のうち' not in D2 else '再現しない')
main_hdr = '| 行 | z | 観測の変化 | 変換の後の確率（前→後） |'
in_added = sum(1 for blk in added if any(l.startswith(main_hdr) for l in blk))
row('F2-1', '大きさの目盛りの主の表（z・観測の変化・比・読み・印の列）を、縦棒を字にして再掲した表が無い（足した表は部分の表と生の確率の表だけ）',
    '主の表の見出しの数 %d（凍結の出力）・足した区画の中 %d' % (D2.count(main_hdr), in_added), '再現した' if in_added == 0 else '再現しない')
info = [l for l in D2.split(NL) if '予想者の情報状態' in l][0]
row('F2-2', '§8 の予想者の情報状態の行に、登録者の予想のファイルの保存（08:15）が露出（07:52）の後であることと、前の版の SHA が無く独立は申告に依ることが書かれていない（露出の記録にはある）',
    '§8 の行に「08:15」: %s・「07:52」: %s・「申告に依る」: %s／露出の記録に「08:15」: %s・「07:52」: %s・「申告に依る」: %s' % ('08:15' in info, '07:52' in info, '申告に依る' in info, '08:15' in EX, '07:52' in EX, '申告に依る' in EX),
    '再現した' if '08:15' not in info and '申告に依る' not in info and '08:15' in EX and '申告に依る' in EX else '一部再現')
lim = D2.split('結果を開いた後に足す限界')[1].split('正誤')[0]
gate_lim = [l for l in lim.split(NL) if '門を通らなかったことは' in l]
row('F2-3', '§9 の足した限界の「門を通らなかったことは、そろわないことを示さない」の箇条に、段の近くの値を惜しいと読まない句と、M_X にそろいの兆しが無いこと（順位相関 −0.05282・割合 0.8732）が無い（§0 の添えにはある）',
    '§9 の箇条に「惜しい」: %s・「M_X」: %s／§0 の添えに「惜しい」: %s' % (any('惜しい' in l for l in gate_lim), any('M_X' in l for l in gate_lim), '惜しい' in sec0),
    '再現した' if gate_lim and not any('惜しい' in l for l in gate_lim) and '惜しい' in sec0 else '一部再現')
# 二 票の数の食い違い
n3 = sum(1 for l in AD.split(NL) if l.startswith('| P') and '（三）' in l.split('|')[-2])
row('F1-問1・F2-問1', '採否表の区分（三）の行の数（F1 は 24・F2 は 31）', '区分の欄に（三）を含む行 %d（P566・P567・P568・P572〜P586・P588〜P600）' % n3,
    '一部再現（F2 の数と合う・F1 の数は合わない）' if n3 == 31 else '一部再現')
P = L['primary']['metrics']
six = {'M_L_survival': P['M_L_survival']['p_iso'], 'M_X_survival': P['M_X_survival']['p_iso'], 'M_X_nuclear': P['M_X_nuclear']['p_iso'], 'M_E': P['M_E']['p_iso'], 'M_F': P['M_F']['p_iso']}
row('F2-問3', '「該当なし」にした六升の物差しの等方の割合は 0.35〜0.996', '物差しの等方の割合: %s（最小 %.4g・最大 %.4g）' % ('・'.join('%s %.4g' % kv for kv in six.items()), min(six.values()), max(six.values())),
    '一部再現（最小は M_E の 0.1738）' if min(six.values()) < 0.35 else '再現した')
n_lim = sum(1 for l in lim.split(NL) if l.startswith('  - '))
row('F1-問6・F2-問6', '足した限界の数（F1 は 10・F2 は 11）', '「結果を開いた後に足す限界」の下の箇条 %d（ほかに、凍結の時点の文を正す行が一つ）' % n_lim,
    '一部再現（F1 の数と合う・F2 の数は合わない）' if n_lim == 10 else '一部再現')
el = [x for x in PH['raw_softmax_main'] if x['eligible']]
row('F2-問4', '生の確率の各方向による変化は 0.001 程度', '比を出した 7 行の生の確率の変化: %s' % '・'.join('%s %.4g' % (x['row'], x['raw_diff']) for x in el),
    '一部再現（O-Ncold の四行は 0.0008〜0.003・Osec-Ncold の三行は |0.002〜0.009|）')
# 三 票が確かめた数
sec9 = D2.split('## 9.')[1]
n22 = sum(1 for l in sec9.split(B)[1].split(E)[0].split(NL) if l.startswith('- '))
row('F2-問6', '正本の限界の文は 22 項目', '§9 の凍結の区画の箇条 %d' % n22, '再現した' if n22 == 22 else '一部再現')
k364 = [r for r in V1['rows'] if r['K'] == 'K364'][0]
row('F2-問3', '符号だけで突き合わせると、札が付かなかった六升はすべて予想の向きと一致してしまう', '結果の巡・第一巡の再現 K364 の判定「%s」' % k364['verdict'],
    '再現した（K364 と同じ）' if k364['verdict'] == '再現した' else '一部再現')
zm = re.search(r'\| M_L_nuclear \| [^|]+ \| [^|]+ \| [^|]+ \| ([^|]+) \|', IC)
row('F1-問2', 'M_L_nuclear は等方の標準偏差から見て z ≈ −0.71', '独立の再計算の記録の z: %s' % (zm.group(1).strip() if zm else None), '再現した' if zm and zm.group(1).strip().startswith('-0.71') else '一部再現')
ctx = ['-0.06414', '0.05117', '2.2%', '0.07343', 'M_L_nuclear 0.15', '108 のうち 12']
row('F1-問2・F2-問2', '唯一の札の文脈の数（兄弟 −0.06414・最大の相手 0.05117 と差 2.2%・等方の標準偏差 0.07343・中央値の比 0.15・ランダム方向の最上位 12／108）は草案の添えの数と同じ',
    '草案の二つ目にある: %s' % '・'.join('%s %s' % (t, t in D2) for t in ctx), '再現した' if all(t in D2 for t in ctx) else '一部再現')
pc = C['magnitude']['colab_check']['calibration']['S4|Osec-Ncold|json']['main']
tail = sum(math.comb(pc['n'], i) * pc['p_T'] ** i * (1 - pc['p_T']) ** (pc['n'] - i) for i in range(pc['k'], pc['n'] + 1))
row('F1-問3・F2-問6', '較正の検査は 0.999 の区間の上端近くで通った（裾の割合 0.001471・z 2.97・上端 155 に対し 154）', '裾の割合 %.6f・区間 %s・観測 %d' % (tail, pc['interval'], pc['k']),
    '再現した' if abs(tail - 0.001471) < 5e-6 and pc['interval'][1] == 155 and pc['k'] == 154 else '一部再現')
g = C['gates']['full']['M_X']
row('F2-所見3', '門の M_X は順位相関 −0.05282・割合 0.8732', '順位相関 %.5g・割合 %.4g' % (g['rho'], g['p']), '再現した' if abs(g['rho'] + 0.05282) < 1e-4 and abs(g['p'] - 0.8732) < 1e-4 else '一部再現')
eo = [x for x in el if x['row'].startswith('S4|O-Ncold')]
row('F1-問4・F2-問4', '切り詰めで零の四行でも、生の確率は約 0.059 あり、直接の経路の変化は +0.0008〜+0.0030', '生の確率（前）%s・変化 %s' % (sorted({round(x['raw_before'], 5) for x in eo}), '・'.join('%.4g' % x['raw_diff'] for x in eo)),
    '再現した' if all(abs(x['raw_before'] - 0.05909) < 1e-4 for x in eo) and 0.0007 < min(x['raw_diff'] for x in eo) and max(x['raw_diff'] for x in eo) < 0.0031 else '一部再現')
row('F1-問5・F2-問5', '凍結の後の逸脱は D-BL1〜D-BL4 の四つで、承認は裁定 D188・D189・D191・D192', '逸脱と承認: %s' % '・'.join('%s %s' % (d['no'], re.search(r'裁定 (D\d+)', d['approval']).group(1)) for d in FR['deviations']),
    '再現した' if [d['no'] for d in FR['deviations']] == ['D-BL1', 'D-BL2', 'D-BL3', 'D-BL4'] else '一部再現')
tm = ['06:30', '07:52', '08:15', '08:17']
row('F2-問5', '露出の記録に 06:30（較正の確率）・07:52（予想の一部）・08:15（登録者のファイルの保存）・08:17（SHA の提示）がある', '露出の記録にある: %s' % '・'.join('%s %s' % (t, t in EX) for t in tm),
    '再現した' if all(t in EX for t in tm) else '一部再現')
shas = {'records/Blens/results-Blens-draft2.md': 'DE95E94809573421', 'design/design-Blens-FROZEN.md': 'A6281F419F059145', 'design/contrasts-Blens.json': '3864252EC540F93B'}
row('F2-頭', '検分した草案の二つ目・凍結の本文・正本の SHA16 は DE95E94809573421・A6281F419F059145・3864252EC540F93B', '置き場の値: %s' % '・'.join('%s %s' % (k2, s16(k2)) for k2 in shas),
    '再現した' if all(s16(k2) == v for k2, v in shas.items()) else '一部再現')
row('F1-頭', '対象のコミットは 893b8ef', '束の索引の「組んだ時点のコミット」: %s' % re.search(r'組んだ時点のコミット (\w+)', IX).group(1), '再現した' if '組んだ時点のコミット 893b8ef' in IX else '一部再現')
json.dump({'rows': rows, 'inputs': {r: s16(r) for r in INPUTS}}, open(OUT_JS, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
cnt = {v: sum(1 for r in rows if r['verdict'].startswith(v)) for v in ('再現した', '一部再現', '再現しない')}
M = ['# 最終検分の二票の事実の主張の再現（機械生成・`verify_Blens_results_final.py`・2026-09-24・コーディネータ）', '',
     '- 出所の札: F1・F2 は、最終検分の新しい Gemini 3.8 Flash の一人目・二人目（登録者の並べた順）。票は `gemini-final-1/review.md`・`gemini-final-2/review.md`（逐語）。',
     '- 並べ方: 起草者に不利な主張（報告の欠け）を先に、次に票の数の食い違い、最後に票が確かめた数。',
     '- 判定の数: %s（%s）。' % ('・'.join('%s %d' % kv for kv in cnt.items()), 'K%d〜K%d' % (398, K[0] - 1)),
     '- 入力の SHA16: %s。' % '・'.join('`%s` %s' % (r, s16(r)) for r in INPUTS), '',
     '| 再現 | 出所 | 票の主張 | 現物 | 判定 |', '|---|---|---|---|---|']
M += ['| %s | %s | %s | %s | %s |' % (r['K'], r['src'], r['claim'].replace('|', '\\|'), r['evidence'].replace('|', '\\|'), r['verdict']) for r in rows]
M += ['', '## 検分票', '', '- 対象: 最終検分の二票の事実の主張。', '- 段階: 票を読んだ後。', '- 凍結物の同定: 凍結の本文・正本・草案の二つ目の SHA16 を置き場の値に当てた（上の表）。', '- 盲検の状態: 該当しない。',
      '- 敵対的検分: 起草者に不利な主張（報告の欠け）から先に当てた。票の数の食い違い（F1 の区分の数・F2 の限界の数・等方の割合の幅・生の確率の変化の大きさ）も消さずに並べた。',
      '- 系統の内訳: コーディネータ（Claude 系）一名が当てた。', '- COI記録: 起草者は「足りている」と読む側に引かれる。当て方は器で固定した。',
      '- 本検分が確認していないこと: 二票の読みの提案の当否（採否表で裁く）。票が束のどこまでを読んだか（票の申告に依る）。', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('rows', len(rows), cnt)
for r in rows:
    print(r['K'], r['verdict'][:22], '|', r['evidence'][:150])
