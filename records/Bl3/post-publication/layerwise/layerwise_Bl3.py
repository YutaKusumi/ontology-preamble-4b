# -*- coding: utf-8 -*-
"""層三の層ごとの差分を並べる（登録外の記述・枠 `frame-layerwise-Bl3.md` を値を見る前に書いた）。値は集計の記録 `records/Bl3/analysis-Bl3.json` の `layerwise` から器で読む。
札・読みの型・報告の文は変えない。どの層も「効き目が生まれた層」「転換層」と呼ばない（裁定 D203・D208・正本の注）。
出力: layerwise-Bl3.md（表）・layerwise-Bl3.json（図のための値）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))   # 公開の置き場では、置き場からの相対（非公開の置き場で走らせた版との違いはこの一行だけ）
NL = chr(10)
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
AP = os.path.join(REPO, 'records', 'Bl3', 'analysis-Bl3.json')
A = json.load(open(AP, encoding='utf-8'))
L = A['layerwise']
rows = A['rows']
vrows = [(rid, r) for rid, r in rows.items() if r['direction'] == 'static']
assert len(vrows) == 7
f = lambda x: ('%.3f' % x) if abs(x) >= 0.001 or x == 0 else ('%.2e' % x)
out = {'what': 'layerwise (registration-external description)', 'source': {'records/Bl3/analysis-Bl3.json': s16(AP)}, 'cells': {}}
md = ['# 層三の層ごとの差分（登録外の記述・機械生成・`layerwise_Bl3.py`）', '',
      '- 値の出所: `records/Bl3/analysis-Bl3.json`（SHA16 %s）の `layerwise`。枠は値を見る前に書いた（`frame-layerwise-Bl3.md`・時刻とハッシュは `frame-stamp.txt`）。' % s16(AP),
      '- 値: (a) 無操作との残差の差のノルム・(b) 足した方向との余弦・(c) 各層の残差に最終の正規化と語彙の行列を当てた、選択肢 a の文字の対数オッズの、加えた腕と無操作の差。等方は層ごとの中央値と 95% の中央の区間（1999 本）。',
      '- 読みの決まり: どの層も「効き目が生まれた層」「転換層」と呼ばない。区間の内か外かは記述で、検定ではない（層と行をまたいだ補正も無い）。途中の層の (c) は、その層で模型が使う量と同じである保証が無い（正本の注）。', '']
summary = []
for rid, r in vrows:
    cs = r['cell_sign']
    C = L[cs]
    layers = sorted(C['noop_lo'].keys(), key=int)
    v = C['rows']['static']
    med, lo, hi = C['iso_summary']['median'], C['iso_summary']['lo'], C['iso_summary']['hi']
    last_c = v[-1][2]
    outside = [int(layers[i]) for i in range(len(layers)) if not (lo[i][2] <= v[i][2] <= hi[i][2])]
    out_ab = {'a': [int(layers[i]) for i in range(len(layers)) if not (lo[i][0] <= v[i][0] <= hi[i][0])],
              'b': [int(layers[i]) for i in range(len(layers)) if not (lo[i][1] <= v[i][1] <= hi[i][1])]}
    out['cells'][cs] = {'row': rid, 'iso_outside_row': r['iso_outside'], 'effect': r['effect'], 'layers': [int(x) for x in layers],
                        'noop_lo': [C['noop_lo'][x] for x in layers], 'static': v, 'iso_median': med, 'iso_lo': lo, 'iso_hi': hi,
                        'others': {k: C['rows'][k] for k in ('Nk', 'td', 'loaded', 'rand:0', 'rand:1', 'rand:2')}}
    summary.append((rid, cs, r['iso_outside'], r['effect'], last_c, outside, out_ab))
md += ['## 1. v̂ の行ごとのまとめ（七行）', '',
       '| 行 | 升目と符号 | 等方の外（札） | 読み取りの効き目 | 最後の層の (c) | (c) が等方の区間の外の層 | (a) が外の層 | (b) が外の層 |', '|---|---|---|---|---|---|---|---|']
for rid, cs, io, eff, lc, o, oab in summary:
    md.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (rid, cs.replace('|', '｜'), 'はい' if io else 'いいえ', f(eff), f(lc), '・'.join(map(str, o)) or 'なし',
                                                      '・'.join(map(str, oab['a'])) or 'なし', '・'.join(map(str, oab['b'])) or 'なし'))
md += ['', '- 最後の層の (c) と読み取りの効き目の差の最大: %.2e（正本の許容 %s）。' % (max(abs(x[3] - x[4]) for x in summary), json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))['computation']['layer_tol']), '']
# 唯一の行の層ごとの表
rid1, r1 = [(rid, r) for rid, r in vrows if r['iso_outside']][0]
C = out['cells'][r1['cell_sign']]
md += ['## 2. 唯一の等方の外の行（%s・%s）の層ごとの値' % (rid1, r1['cell_sign'].replace('|', '｜')), '',
       '| 層 | 無操作の対数オッズ（その層の lens） | v̂ の (c) | 等方の (c) の中央値 | 区間の下 | 区間の上 | 内か外か | v̂ の (a) | 等方の (a) の中央値［区間］ | v̂ の (b) | 等方の (b) の中央値［区間］ | Nk の (c) | td の (c) | (6b) の (c) | 三本の (c) |',
       '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for i, ly in enumerate(C['layers']):
    v, m, lo_, hi_ = C['static'][i], C['iso_median'][i], C['iso_lo'][i], C['iso_hi'][i]
    md.append('| %d | %s | %s | %s | %s | %s | %s | %s | %s［%s, %s］ | %s | %s［%s, %s］ | %s | %s | %s | %s |' % (
        ly, f(C['noop_lo'][i]), f(v[2]), f(m[2]), f(lo_[2]), f(hi_[2]), '内' if lo_[2] <= v[2] <= hi_[2] else '外', f(v[0]), f(m[0]), f(lo_[0]), f(hi_[0]), f(v[1]), f(m[1]), f(lo_[1]), f(hi_[1]),
        f(C['others']['Nk'][i][2]), f(C['others']['td'][i][2]), f(C['others']['loaded'][i][2]), '・'.join(f(C['others'][k][i][2]) for k in ('rand:0', 'rand:1', 'rand:2'))))
md += ['', '## 3. 最後の層の効き目と、升目ごとの等方の区間（七行）', '',
       '| 行 | 升目と符号 | 効き目 | 等方の (c) の中央値［区間］ | 区間の幅 | 効き目 ÷ 区間の半分の幅 | 無操作の対数オッズ |', '|---|---|---|---|---|---|---|']
for rid, cs, io, eff, lc, o, oab in summary:
    Cc = out['cells'][cs]
    lo_, hi_, m_ = Cc['iso_lo'][-1][2], Cc['iso_hi'][-1][2], Cc['iso_median'][-1][2]
    md.append('| %s | %s | %s | %s［%s, %s］ | %s | %.2f | %s |' % (rid, cs.replace('|', '｜'), f(eff), f(m_), f(lo_), f(hi_), f(hi_ - lo_), abs(eff) / ((hi_ - lo_) / 2), f(Cc['noop_lo'][-1])))
md += ['', '## 4. 枠の予想と照らす（外れても消さない）', '',
       '| 何 | 予想（枠） | 結果 | 照らし |', '|---|---|---|---|',
       '| 最後の層の (c) と読み取りの効き目 | 一致する | 七行とも一致（§1 の差の最大） | 当たり |',
       '| 唯一の行の v̂ の (c) が等方の区間の外に出る層 | 最後の数層だけ | 第 24 層から後の多くの層（間に内の層を挟む・§1） | 外れ |',
       '| 等方の区間の幅 | 層とともに広がる | 途中まではほぼ同じで、後の層で広がる（§2） | 当たり |',
       '| 余弦 (b) | v̂ も等方も層とともに下がる | 下がる（最後の二層で v̂ はわずかに上がる・§2） | 当たり |',
       '| 唯一の行の形 | ほかの v̂ の行の少なくとも一つにも見える | (c) では見えない（ほかの行は多くて一層）。(a) のノルムが多くの層で区間の上にある形は sub:S1 にも見える（§1） | (c) は外れ・(a) は当たり |',
       '', '## 5. 記述（読みは付けない）', '',
       '- 唯一の行の v̂ の (c) は、第 23 層までは等方の区間の内にあり、第 24 層から後の多くの層で区間の外にあった（§1・§2）。どの層も「効き目が生まれた層」「転換層」とは呼ばない（枠の読みの決まり 1）。ほかの v̂ の行では、(c) が区間の外に出た層は多くて一つだった。',
       '- 最後の層の効き目の大きさは、唯一の行と sub:S1 で近い。唯一の行の升目の等方の区間は、ほかの升目より狭い（§3）。区別できたことには、効き目の大きさと升目ごとの等方の広がりの両方が入る。',
       '- (a) 残差の差のノルム: v̂ のノルムは、唯一の行と sub:S1 で多くの層にわたって等方の区間の上にあり、ほかの行でも初めの層で区間の上にあった（§1）。等方のランダム方向は偏りのある残差の中では低い棒である（凍結の限界の文）ので、このノルムの差を v̂ に特有の働きの印とは読まない。',
       '- (b) 足した方向との余弦は、v̂ も等方も層とともに下がった。最後の層では、唯一の行を含む多くの行で、v̂ の余弦が等方の区間の上にあった（§1・§2）。',
       '- 唯一の行の升目では、Nk と (6b) の (c) も後の層で v̂ と同じ側に動き、最後の層で等方の区間の端のあたりにあった（§2）。名前のある方向どうしの向きの近さは、ここでは見ていない。',
       '- 途中の層の無操作の lens の値は、層ごとに大きく揺れる（§2 の二列目）。途中の層の lens の値が、その層で模型が使う量と同じである保証は無い（正本の注）。',
       '', '## 検分票', '',
       '- 対象: 層三の層ごとの差分の表と記述（登録外の記述・層三の公開の後）。',
       '- 段階: 枠あり（値を見る前に書いた・`frame-stamp.txt`）。§3 の升目ごとの区間の幅の比べは、値を見た後に足した。',
       '- 凍結物の同定: 集計の記録の SHA16（頭）。札・読みの型・報告の文は変えていない。',
       '- 盲検の状態: 該当しない（値は公開済み・起草者が並べた）。',
       '- 敵対的検分: 一行だけを見ず、七行を同じ並べ方で並べた。最後の層の値を読み取りの効き目と照らした。層を名指さなかった。ノルムの差を、等方の帰無の弱さ（凍結の限界の文）と並べた。',
       '- 系統の内訳: 起草者（Claude 系）一名。外の目は通っていない。',
       '- COI記録: 起草者は層の中に変わり目を見つけたい側に引かれる（枠の COI）。予想の「最後の数層だけ」は外れ、区間の外の層は第 24 層から始まった。これを「変わり目」と読まないことを、読みの決まり 1 で先に決めていた。',
       '- 判定: 登録者確認要（記録を公開の置き場に置くか・次の一手と合わせて）。',
       '- 本検分が確認していないこと: 等方の方向ごとの層ごとの値（中央値と区間だけ）。途中の層の値の当否（tuned lens などの補正なし）。計算の道を替えたときの値の動き。名前のある方向どうしの向きの近さ。',
       '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'layerwise-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(md))
json.dump(out, open(os.path.join(HERE, 'layerwise-Bl3.json'), 'w', encoding='utf-8', newline=NL), ensure_ascii=False)
for rid, cs, io, eff, lc, o, oab in summary:
    print(rid, cs, 'iso_out' if io else '-', 'eff %.3f last_c %.3f' % (eff, lc), '| c outside layers:', o, '| a:', oab['a'], '| b:', oab['b'])
