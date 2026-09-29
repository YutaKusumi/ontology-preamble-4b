# -*- coding: utf-8 -*-
"""層三の升目ごとの揺れの広さを並べる（登録外の記述・枠 `frame-cell-sensitivity-Bl3.md` を値を見る前に書いた）。値は層三の記録から器で読む。
札・読みの型・報告の文は変えない。記述であり、検定ではない（升目は少ない）。模型の性質の言葉を結果の記述に使わない。
出力: cell-sensitivity-Bl3.md（表）・cell-sensitivity-Bl3.json（値）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, json, hashlib, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))   # 公開の置き場では、置き場からの相対（非公開の置き場で走らせた版との違いはこの一行だけ）
NL = chr(10)
P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
AP = 'records/Bl3/analysis-Bl3.json'
PP = 'records/Bl3/pilot/pilot-20260926T103442Z/pilot.json'
A = json.load(open(P(AP), encoding='utf-8'))
MP = 'results/Bl3/main/%s/main.json' % A['inputs']['main']['dir']
M = json.load(open(P(MP), encoding='utf-8'))
PJ = json.load(open(P(PP), encoding='utf-8'))['pilot']
f = lambda x: ('%.3f' % x) if abs(x) >= 0.001 or x == 0 else ('%.2e' % x)


def rank(x):
    x = np.asarray(x, dtype=np.float64)
    o = np.argsort(x, kind='mergesort')
    r = np.empty(len(x))
    r[o] = np.arange(len(x))
    return r


def spearman(x, y):
    rx, ry = rank(x), rank(y)
    return float(np.corrcoef(rx, ry)[0, 1])


def iso_vec(cs):
    e = M['cells'][cs]['effects']
    ks = sorted((k for k in e if k.startswith('iso:')), key=lambda k: int(k.split(':')[1]))
    return ks, np.array([e[k] for k in ks], dtype=np.float64)


def real_vec(cs):
    e = M['cells'][cs]['effects']
    return np.array([v for k, v in e.items() if k.startswith('real:')], dtype=np.float64)


CS_ALL = sorted(M['cells'].keys())
CS = [cs for cs in CS_ALL if iso_vec(cs)[1].size > 0]   # 等方の効き目がある升目と符号（Onull の -1 は実在の差の方向だけ）
CS_REAL_ONLY = [cs for cs in CS_ALL if cs not in CS]
stats = {}
for cs in CS:
    ks, v = iso_vec(cs)
    r = real_vec(cs)
    q = np.percentile(v, [2.5, 25, 50, 75, 97.5])
    stats[cs] = {'n_iso': len(v), 'w95': float(q[4] - q[0]), 'iqr': float(q[3] - q[1]), 'sd': float(v.std(ddof=1)), 'median': float(q[2]),
                 'n_real': len(r), 'real_sd': float(r.std(ddof=1)), 'real_iqr': float(np.percentile(r, 75) - np.percentile(r, 25)), 'real_range': float(r.max() - r.min())}
# ± の組
cells = sorted({cs.rsplit('|', 1)[0] for cs in CS})
pairs = []
for c in cells:
    p_, m_ = c + '|+1', c + '|-1'
    if p_ in CS and m_ in CS:
        kp, vp = iso_vec(p_)
        km, vm = iso_vec(m_)
        same_ids = kp == km
        rho = spearman(vp, vm) if same_ids else None
        wp, wm = stats[p_]['w95'], stats[m_]['w95']
        pairs.append({'cell': c, 'w95_plus': wp, 'w95_minus': wm, 'rel_diff': abs(wp - wm) / ((wp + wm) / 2), 'median_plus': stats[p_]['median'], 'median_minus': stats[m_]['median'],
                      'same_iso_ids': same_ids, 'spearman_plus_minus': rho})
# 升目の性質
attr = []
for c in cells:
    pc = PJ['cells'].get(c)
    if pc is None:
        continue
    ws = [stats[cs]['w95'] for cs in CS if cs.rsplit('|', 1)[0] == c]
    attr.append({'cell': c, 'family': 'nuclear' if c.startswith('N') else 'survival', 'arm': c.split('|')[1], 'noop_lo': pc['lo'], 'pa': pc['pa'], 'stage_b_rate': pc['stage_b_rate'],
                 'vi_a': PJ['vi']['a'][c], 'v_diff': PJ['v']['diffs'][c], 'w95_mean': float(np.mean(ws)), 'n_signs': len(ws)})
attr.sort(key=lambda x: x['w95_mean'])
# 層ごとの区間の幅（(c)）
LW = A['layerwise']
lw = {}
for cs, C in LW.items():
    layers = sorted(C['noop_lo'].keys(), key=int)
    w = [C['iso_summary']['hi'][i][2] - C['iso_summary']['lo'][i][2] for i in range(len(layers))]
    lw[cs] = {'layers': [int(x) for x in layers], 'width': w}
# 順位相関（記述）
cor = {
    'cells7: w95_mean vs noop_lo': spearman([a['w95_mean'] for a in attr], [a['noop_lo'] for a in attr]),
    'cells7: w95_mean vs vi_a': spearman([a['w95_mean'] for a in attr], [a['vi_a'] for a in attr]),
    'cells7: w95_mean vs stage_b_rate': spearman([a['w95_mean'] for a in attr], [a['stage_b_rate'] for a in attr]),
    'cellsigns%d: w95 vs real_sd' % len(CS): spearman([stats[cs]['w95'] for cs in CS], [stats[cs]['real_sd'] for cs in CS]),
}
n_real_wider = sum(1 for cs in CS if stats[cs]['real_sd'] > stats[cs]['sd'])
real_only = {cs: {'n_real': len(real_vec(cs)), 'real_sd': float(real_vec(cs).std(ddof=1))} for cs in CS_REAL_ONLY}
out = {'what': 'cell sensitivity (registration-external description)', 'cellsigns_with_iso': CS, 'cellsigns_real_only': real_only, 'source': {AP: s16(P(AP)), MP: s16(P(MP)), PP: s16(P(PP))},
       'stats': stats, 'pairs': pairs, 'attributes': attr, 'layerwise_width_c': lw, 'spearman_descriptive': cor, 'n_real_sd_gt_iso_sd': n_real_wider}
N_ISO = stats[CS[0]]['n_iso']
assert all(stats[cs]['n_iso'] == N_ISO for cs in CS)
N_REAL = stats[CS[0]]['n_real']
assert all(stats[cs]['n_real'] == N_REAL for cs in CS)
json.dump(out, open(os.path.join(HERE, 'cell-sensitivity-Bl3.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
md = ['# 層三の升目ごとの揺れの広さ（登録外の記述・機械生成・`cell_sensitivity_Bl3.py`）', '',
      '- 値の出所: `%s`（SHA16 %s）・`%s`（SHA16 %s）・`%s`（SHA16 %s）。枠は値を見る前に書いた（`frame-cell-sensitivity-Bl3.md`・時刻とハッシュは `frame-stamp.txt`）。' % (AP, s16(P(AP)), MP, s16(P(MP)), PP, s16(P(PP))),
      '- 「揺れの広さ」は、同じ長さの等方のランダム方向（%d 本）を足したときの、最後の層の読み取りの対数オッズの差の広がり。効き目は、符号を掛けた方向を足したときの対数オッズから、無操作の対数オッズを引いた値（`tools/bl3_run.py` の `run_cell_sign`）。記述であり、検定ではない。升目は少ない。' % N_ISO, '',
      '- **枠からのずれ（開示）**: 枠は、組の出力の升目の一覧から、升目と符号を 14、± の組を 7 と書いた（枠の「並べるもの」の 1 と 2）。値を出す段で、Onull の −1 の三つ（%s）には実在の差の方向の効き目（28 本）だけがあり、等方の効き目が無いと分かった（二つ目の札の比べる相手に使う升目）。等方の広がりを並べるのは %d の升目と符号、± の組は %d になった。' % ('・'.join(CS_REAL_ONLY), len(CS), sum(1 for c in sorted({cs.rsplit('|', 1)[0] for cs in CS}) if c + '|+1' in CS and c + '|-1' in CS)), '',
      '## 1. 最後の層の、升目と符号ごとの広がり（%d）' % len(CS), '',
      '| 升目と符号 | 等方の 95% の区間の幅 | 四分位の幅 | 標準偏差 | 中央値 | 実在の差の方向（28）の標準偏差 | 同じく四分位の幅 | 同じく最小〜最大の幅 |', '|---|---|---|---|---|---|---|---|']
for cs in sorted(CS, key=lambda k: stats[k]['w95']):
    s = stats[cs]
    md.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (cs.replace('|', '｜'), f(s['w95']), f(s['iqr']), f(s['sd']), f(s['median']), f(s['real_sd']), f(s['real_iqr']), f(s['real_range'])))
md += ['', '## 2. 同じ升目の ± の符号の組（%d）' % len(pairs), '',
       '| 升目 | + の 95% の幅 | − の 95% の幅 | 幅の違い（平均に対する割合） | + の中央値 | − の中央値 | 等方の方向の番号が同じ | 同じ方向の + と − の効き目の順位相関 |', '|---|---|---|---|---|---|---|---|']
for p in pairs:
    md.append('| %s | %s | %s | %.1f%% | %s | %s | %s | %s |' % (p['cell'].replace('|', '｜'), f(p['w95_plus']), f(p['w95_minus']), 100 * p['rel_diff'], f(p['median_plus']), f(p['median_minus']), 'はい' if p['same_iso_ids'] else 'いいえ',
                                                         ('%.3f' % p['spearman_plus_minus']) if p['spearman_plus_minus'] is not None else '—'))
md += ['', '## 3. 升目の性質と並べる（主の升目 %d・広がりの小さい順）' % len(attr), '',
       '| 升目 | 場面の族 | 前置きの腕 | ± の平均の 95% の幅 | 無操作の対数オッズ | 選択肢 a の確率（集合の中） | 段階 B の無操作の破局の率 | 下見の (vi) の (a) | 下見の (v) |', '|---|---|---|---|---|---|---|---|---|']
for a in attr:
    md.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (a['cell'].replace('|', '｜'), {'nuclear': '核（N1）', 'survival': '生存'}[a['family']], a['arm'], f(a['w95_mean']), f(a['noop_lo']), f(a['pa']), f(a['stage_b_rate']), f(a['vi_a']), f(a['v_diff'])))
LWMD = open(os.path.join(REPO, 'records/Bl3/post-publication/layerwise/layerwise-Bl3.md'), encoding='utf-8').read()
Q_C = re.search('[(]c[)] (各層の残差に[^。]*?の差)。', LWMD).group(1)
assert LWMD.count(Q_C) == 1
md += ['', '## 4. 層ごとの等方の区間の幅（(c)・%d の升目と符号）' % len(lw), '',
       '- (c) は、公開の層ごとの記録（`records/Bl3/post-publication/layerwise/layerwise-Bl3.md`）の定めで「%s」。区間は、等方の効き目の層ごとの 95%% の中央の区間（`analysis-Bl3.json` の `layerwise` の中央値と区間だけ）。' % Q_C, '',
       '| 升目と符号 | ' + ' | '.join('第 %d 層' % l for l in lw[sorted(lw)[0]]['layers']) + ' |', '|---|' + '---|' * len(lw[sorted(lw)[0]]['layers'])]
for cs in sorted(lw, key=lambda k: lw[k]['width'][-1]):
    md.append('| %s | %s |' % (cs.replace('|', '｜'), ' | '.join('%.2f' % w for w in lw[cs]['width'])))
md += ['', '## 5. 升目の間の順位相関（記述・検定ではない・升目は少ない）', '']
COR_JA = {'cells7: w95_mean vs noop_lo': '升目 %d: ± の平均の 95%% の幅と、無操作の対数オッズ' % len(attr),
          'cells7: w95_mean vs vi_a': '升目 %d: ± の平均の 95%% の幅と、下見の (vi) の (a)' % len(attr),
          'cells7: w95_mean vs stage_b_rate': '升目 %d: ± の平均の 95%% の幅と、段階 B の無操作の破局の率' % len(attr),
          'cellsigns%d: w95 vs real_sd' % len(CS): '升目と符号 %d: 等方の 95%% の幅と、実在の差の方向の標準偏差' % len(CS)}
assert set(COR_JA) == set(cor)
for k, v in cor.items():
    md.append('- %s: %.3f' % (COR_JA[k], v))
w18 = [lw[cs]['width'][0] for cs in lw]
w28 = [lw[cs]['width'][10] for cs in lw]
w35 = [lw[cs]['width'][-1] for cs in lw]
rd = [p['rel_diff'] for p in pairs]
rh = [p['spearman_plus_minus'] for p in pairs]
# 記述の文のための機械の数え（文は値から作り、文が成り立たない値なら止まる）
LAY = lw[sorted(lw)[0]]['layers']
assert LAY[0] == 18 and LAY[10] == 28 and LAY[-1] == 35 and all(lw[cs]['layers'] == LAY for cs in lw)
med_same = sum(1 for p in pairs if np.sign(p['median_plus']) == np.sign(p['median_minus']))
med_abs = [abs(p[k]) for p in pairs for k in ('median_plus', 'median_minus')]
w_pairs = [p[k] for p in pairs for k in ('w95_plus', 'w95_minus')]
ratio_cells = attr[-1]['w95_mean'] / attr[0]['w95_mean']


def separated(ga, gb):
    return max(ga) < min(gb) or max(gb) < min(ga)


fam_sep = separated([a['w95_mean'] for a in attr if a['family'] == 'nuclear'], [a['w95_mean'] for a in attr if a['family'] == 'survival'])
arm_sep = separated([a['w95_mean'] for a in attr if a['arm'] == 'O-Ncold'], [a['w95_mean'] for a in attr if a['arm'] == 'Onull'])
assert not fam_sep and not arm_sep
narrowest = sorted(lw, key=lambda k: lw[k]['width'][-1])[0]
widest_at = [LAY[i] for i in range(len(LAY) - 1) if max(lw, key=lambda k: lw[k]['width'][i]) == narrowest]
assert widest_at
early_max = max(max(lw[cs]['width'][:11]) for cs in lw)
late_min = min(lw[cs]['width'][-1] for cs in lw)
wider = [cs for cs in CS if stats[cs]['real_sd'] > stats[cs]['sd']]
onull = [cs for cs in CS if cs.split('|')[1] == 'Onull']
assert set(wider) == set(onull)
assert all(cs.split('|')[1] in ('O-Ncold', 'Onull') for cs in CS)
assert all(stats[cs]['real_sd'] < stats[cs]['sd'] for cs in CS if cs not in wider)
iso_out = [(rid, r['cell_sign']) for rid, r in A['rows'].items() if r['iso_outside']]
assert len(iso_out) == 1
out_rid, out_cs = iso_out[0]
rank_cs = sorted(CS, key=lambda k: stats[k]['w95']).index(out_cs) + 1
rank_cell = [a['cell'] for a in attr].index(out_cs.rsplit('|', 1)[0]) + 1
# 報告の §7 の正本の限界の文を機械で切り出す（「」の中は一字違わず）
FINAL = open(os.path.join(REPO, 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'), encoding='utf-8').read()
Q_REAL = '実在の差の方向は八腕の差で、高々七次元の空間を張り、比べる相手どうしは相関している。'
assert FINAL.count(Q_REAL) == 1
md += ['- 実在の差の方向の標準偏差が等方の標準偏差より大きい升目と符号: %d／%d' % (n_real_wider, len(CS)), '',
       '## 6. 枠の予想と照らす（外れても消さない）', '',
       '| 何 | 予想（枠） | 結果 | 照らし |', '|---|---|---|---|',
       '| ± の組の区間の幅 | 差は 20%% 以内 | %.1f〜%.1f%%（%d 組） | 当たり |' % (100 * min(rd), 100 * max(rd), len(pairs)),
       '| 同じ方向の + と − の効き目 | 強い負の順位相関（−0.8 より負） | %.3f〜%.3f | 当たり |' % (min(rh), max(rh)),
       '| 等方の広がりと無操作の対数オッズ | はっきりした並びは無い | 順位相関 %.3f（升目 %d） | 線の上（予想の「はっきりした」が数で決めていなかった・升目は少ない） |' % (cor['cells7: w95_mean vs noop_lo'], len(attr)),
       '| 等方の広がりと (vi) の (a) | 正の並び | 順位相関 %.3f（升目 %d） | 線の上（数の線を枠で決めていなかった・符号は正だがほぼ零） |' % (cor['cells7: w95_mean vs vi_a'], len(attr)),
       '| 実在の差の方向の広がり | 多くの升目と符号で等方より大きい | %d／%d | 外れ（下の注） |' % (n_real_wider, len(CS)),
       '| 層ごとの区間の形 | 多くで途中まではほぼ同じ・後の層で広がる | 第 18 層 %.2f〜%.2f・第 28 層 %.2f〜%.2f・第 35 層 %.2f〜%.2f（第 18〜28 層の幅の最大 %.2f・第 35 層の幅の最小 %.2f・%d の升目と符号） | 当たり（数の線は枠に無く、起草者の目で照らした） |' % (min(w18), max(w18), min(w28), max(w28), min(w35), max(w35), early_max, late_min, len(lw)),
       '', '@@COUNT6@@',
       '', '## 7. 記述（読みは付けない）', '',
       '- 同じ升目の ± の組では、区間の幅がほぼ同じで（違いは %.1f〜%.1f%%）、同じ番号の等方の方向の + と − の効き目が強い負の順位相関（%.3f〜%.3f）を持った（§2）。この押しの大きさでは、最後の層の読み取りの応じ方は、方向の向きについてほぼ線形だった（向きを逆にすると、効き目もほぼ逆になる）。ただし中央値は、%d 組のうち %d 組で + と − が同じ側にあった（完全に線形なら逆の側に並ぶ）。中央値の大きさは %.3f〜%.3f で、区間の幅（%.2f〜%.2f）に比べれば小さい。' % (100 * min(rd), 100 * max(rd), min(rh), max(rh), len(pairs), med_same, min(med_abs), max(med_abs), min(w_pairs), max(w_pairs)),
       '- 升目の間では、区間の幅（± の平均）が最大で %.2f 倍違った（§3）。場面の族（核か生存か）でも、前置きの腕（O-Ncold か Onull か）でも、広がりの小さい側と大きい側にきれいには分かれなかった。無操作の対数オッズとの順位相関は %.3f で、升目が %d なので決められない。バッチの違いによる無操作の値の揺れ（下見の (vi) の (a)）との順位相関は %.3f で、ほぼ並ばなかった。段階 B の無操作の破局の率との順位相関は %.3f で、これもほぼ並ばなかった。' % (ratio_cells, cor['cells7: w95_mean vs noop_lo'], len(attr), cor['cells7: w95_mean vs vi_a'], cor['cells7: w95_mean vs stage_b_rate']),
       '- 層ごとには、第 18 層ではどの升目と符号も区間の幅がほぼ同じで（%.2f〜%.2f）、升目ごとの違いは後の層で開いた（§4）。最後の層で最も狭かった %s は、第 %s 層では %d の中で最も広かった。広がりの順は、層によって入れ替わった。途中の層の値は、その層で模型が使う量と同じである保証が無い（正本 `design/contrasts-Bl3.json` の注）。' % (min(w18), max(w18), narrowest.replace('|', '｜'), '・'.join(str(x) for x in widest_at), len(lw)),
       '- 実在の差の方向（%d 本）の標準偏差は、%d の升目と符号のうち %d で等方より小さかった（§1・§5）。等方より大きかった %d は、Onull の升目と符号のすべて（%s）で、O-Ncold の %d はどれも等方より小さかった。これは並びの記述で、何で分かれたかは見ていない。報告の §7 の正本の限界の文は「%s」と書く。実在の差の方向は、%d 本の等方と同じ物差しの広がりではない。枠の予想は、この違いを見落としていた。' % (N_REAL, len(CS), len(CS) - len(wider), len(wider), '・'.join(cs.replace('|', '｜') for cs in wider), len(CS) - len(onull), Q_REAL, N_ISO),
       '- 唯一の等方の外の行（`%s`・升目と符号 %s）の等方の区間の幅は、%d の升目と符号の中で狭い側から %d 番目（§1）、升目（± の平均）で見ると %d の中で %d 番目（§3）だった。これは、層三の札を「見かけ」とも「特別」とも読む根拠にしない（枠の読みの決まり 2）。' % (out_rid, out_cs.replace('|', '｜'), len(CS), rank_cs, len(attr), rank_cell),
       '', '## 検分票', '',
       '- 対象: 層三の升目ごとの揺れの広さの表と記述（登録外の記述・層三の公開の後）。',
       '- 段階: 枠あり（値を見る前に書いた・`frame-stamp.txt`）。ただし七つの升目と符号の最後の層の区間の幅と、一つの升目の層ごとの形は、枠の前に見ていた（枠に開示）。枠からのずれ一つ（等方の効き目がある升目と符号の数・頭に開示）。',
       '- 凍結物の同定: 値の出所の SHA16（頭）。札・読みの型・報告の文は変えていない。',
       '- 盲検の状態: 該当しない（値は公開済み・起草者が並べた）。',
       '- 敵対的検分: すべての升目と符号を同じ並べ方で並べた。外れた予想を消さずに置き、数の線の無い予想二つは、どちらの向きにも寄せずに「線の上」とした。実在の差の方向との比べが同じ物差しでないことを書いた。唯一の行をどちらの向きにも読まなかった。記述の文は値から機械で作り、文が成り立たない値なら止まる印を置いた。起草の途中で、唯一の行の升目の順位を「狭い側の二つ目」と書き誤った（升目と符号では三つ目・升目では二つ目）のを一次の値で見つけ、機械の数えに替えた。(vi) の (a) を枠では「計算の道の揺れ」と呼んだが、報告の語（バッチの違いの揺れ）に合わせた。表の見出しの「95%%」の誤植を直した。効き目の定義は `tools/bl3_run.py` で確かめた。',
       '- 系統の内訳: 起草者（Claude 系）一名。外の目は通っていない。',
       '- COI記録: 起草者は、唯一の行を升目の狭さで説明し切る側にも、升目に特別な性質を見つける側にも引かれる（枠の COI）。登録者の仮説（文脈ごと・機種ごとの応じ方の違い）も、違いを見つけたい向きにある。',
       '- 判定: 登録者確認要（公開の置き場に置くか・次の問い）。',
       '- 本検分が確認していないこと: 途中の層の等方の方向ごとの値。計算の道を替えたときの広がりの動き。ほかの機種。広がりが何で決まるか（この表は並びだけで、仕組みは見ていない）。O-Ncold と Onull で実在の差の方向の広がりが分かれた理由。等方の方向ごとの + と − の効き目の和（線形からのずれ）の分布（中央値だけを見た）。', '',
       '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
i6 = md.index('## 6. 枠の予想と照らす（外れても消さない）')
rows6 = [l for l in md[i6:md.index('@@COUNT6@@')] if l.startswith('| ') and not l.startswith('| 何 ')]
assert len(rows6) == 6
kinds = [l.rstrip(' |').rsplit('| ', 1)[1] for l in rows6]
cnt = {k: sum(1 for x in kinds if x.startswith(k)) for k in ('当たり', '外れ', '線の上')}
assert sum(cnt.values()) == len(rows6)
md[md.index('@@COUNT6@@')] = '- 照らしの数（表の行から機械で数えた）: 当たり %d（うち数の線が枠に無いもの %d）・外れ %d・線の上 %d（%d のうち）。' % (cnt['当たり'], sum(1 for x in kinds if x.startswith('当たり（数の線は枠に無く')), cnt['外れ'], cnt['線の上'], len(rows6))
open(os.path.join(HERE, 'cell-sensitivity-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(md))
print('pairs:')
for p in pairs:
    print('  ', p['cell'], 'w+ %.3f w- %.3f diff %.1f%% same_ids %s rho %s' % (p['w95_plus'], p['w95_minus'], 100 * p['rel_diff'], p['same_iso_ids'], None if p['spearman_plus_minus'] is None else round(p['spearman_plus_minus'], 3)))
print('attributes (sorted by width):')
for a in attr:
    print('  ', a['cell'], a['family'], 'w %.3f lo %.3f pa %.4g rateB %.3f vi_a %.3f v %.3f' % (a['w95_mean'], a['noop_lo'], a['pa'], a['stage_b_rate'], a['vi_a'], a['v_diff']))
print('spearman:', {k: round(v, 3) for k, v in cor.items()}, '| real_sd > iso_sd:', n_real_wider, '/', len(CS))
print('layer widths (18, 28, 35):', {cs: (round(v['width'][0], 2), round(v['width'][10], 2), round(v['width'][-1], 2)) for cs, v in sorted(lw.items())})
