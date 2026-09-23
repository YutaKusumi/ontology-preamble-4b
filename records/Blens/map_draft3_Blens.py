# -*- coding: utf-8 -*-
"""B-lens 草案3 と、設計の巡の二巡の採否表（第二巡 P528〜P564・第一巡 P495〜P527）の機械の突き合わせ。
第二巡の各行について、受けた所の文字列が草案3・正本・設計の事実・README・正本の器・第二巡の採否表のどこかにそのまま在ることを確かめる。
第一巡の各行は、草案2 の突き合わせの器 `records/Blens/map_draft2_Blens.py` の文字列で草案3 を確かめ直し、草案3 で意図して書き換えた所は書き換えた後の文字列で確かめる（書き換えた採否の行を表に書く）。
一つでも無ければ止まる。これは「直しの文が在る」ことの確かめで、「直しが正しい」ことの確かめではない（限界に書く）。
用法: python records/Blens/map_draft3_Blens.py"""
import os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
NL = chr(10)
P = lambda rel: os.path.join(REPO, *rel.split('/'))
rd = lambda rel: open(P(rel), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(P(rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
SRC = {'draft': 'design/design-Blens-draft3.md', 'canon': 'design/contrasts-Blens.json', 'facts': 'records/Blens/design-facts-Blens.md', 'readme': 'README.md',
       'gen': 'tools/make_contrasts_Blens.py', 'r2table': 'records/reviews/Blens/design-round2/adoption-table-Blens-design-r2.md'}
TXT = {k: rd(v) for k, v in SRC.items()}
AT2_REL = 'records/reviews/Blens/design-round2/adoption-table-Blens-design-r2.md'
AT1_REL = 'records/reviews/Blens/design-round1/adoption-table-Blens-design-r1.md'


def rows(rel, ncol):
    out = {}
    for l in rd(rel).split(NL):
        m = re.match(r'\| P(\d+) \|', l)
        if m:
            cells = [c.strip() for c in l.strip().strip('|').split(' | ')]
            assert len(cells) == ncol, (rel, m.group(1), len(cells))
            out[int(m.group(1))] = cells
    return out


AT2 = rows(AT2_REL, 6)
AT1 = rows(AT1_REL, 5)
assert sorted(AT2) == list(range(528, 565)) and sorted(AT1) == list(range(495, 528))

MAP2 = {
    528: ('§4 v̂ を抜いた門・転記行 D', [('draft', '**v̂ を抜いた門**（56 行・720 通り）'), ('canon', '"rows_without_vhat"'), ('facts', 'v̂ を抜いた門（static の行を除く）56')]),
    529: ('§4 門', [('draft', '門の行の単位の順位相関（Spearman）を、片側で'), ('draft', '門の行の単位で順位相関を計算し直す')]),
    530: ('§4 v̂ を抜いた門・結びつけてよいもの・§5', [('draft', '同じ物差しが本の門と v̂ を抜いた門の両方を通ったときだけ'), ('draft', 'Holm の段の数は二'), ('draft', '同じ物差しが v̂ を抜いた門も通ったときに限り、v̂ のその物差しの値を行動に結びつけて書く')]),
    531: ('§4 v̂ と (6b) を抜いた門', [('draft', '**v̂ と (6b) を抜いた門**（記述・条件には使わない）: 55 行・120 通り')]),
    532: ('§4 二つの物差しの扱い', [('draft', 'M_L も M_X も survival の三場面で同じ値なので')]),
    533: ('§3.2 語の側の帰無の割合・§9', [('draft', '両側に等しい裾の割合'), ('draft', '帰無の平均・中央値・標準偏差を印字する'), ('draft', '中心が零でない語の側の帰無')]),
    534: ('§3.2 語の側の帰無の候補と層・転記行 H', [('draft', '字は、漢字（「々」を含む）・片仮名（長音符を含む）・平仮名だけとし、cp932 で符号化できるトークンに限る'), ('draft', '「字の種類 × 字数 × ノルムの帯」で分ける'), ('draft', '（倍率 5）'), ('facts', '要る数のある層（字の種類・字数・帯）の候補の数と要る数')]),
    535: ('§3.2 語の側の帰無の感度・転記行 H', [('draft', '感度として、B の無操作の腕の出力に現れたトークンに候補を限った語の側の帰無を並べる'), ('facts', '感度（B の無操作の出力に現れたトークンに限る）')]),
    536: ('§2 標本化の設定・§4 大きさの目盛り・§9', [('draft', '**標本化の変換**'), ('draft', '**較正の検査**'), ('draft', '温度 0.7・top_k 20・top_p 0.9'), ('facts', 'B の本走行の標本化の設定は、試行の記録（11800 件）ですべて同じで、正本の値と一致する')]),
    537: ('§4 答えの文字の位置・転記行 E・§7', [('draft', '答えの文字の位置の比は出さない'), ('facts', '答えの文字の位置（JSON 直答の出力の中で数える）'), ('facts', '答えの文字の位置の比は出ない')]),
    538: ('§4 まとめ方・転記行 E', [('draft', '記述の層（散文）は、選んだ出力の平均を主にし'), ('facts', '文字の前の並びの種類')]),
    539: ('§4 読み・比', [('draft', '直接の経路だけを土台に足したときの率の変化は、観測の変化の読みの比に満たない'), ('draft', '対数オッズの比を記述に並べる')]),
    540: ('§4 読み', [('draft', '直接の経路の押しは、観測の変化と逆向きだった')]),
    541: ('§4 量・転記行 B', [('draft', 'B の JSON 直答の出力の最初のトークンの集合'), ('facts', 'B の本走行の全ての JSON 直答の出力（725 件）の最初のトークン')]),
    542: ('§4 比', [('draft', '比（pt）＝主位置の直接の経路の確率の変化（その升目の一つの値）÷ 観測の率の変化')]),
    543: ('転記行 E', [('facts', '下限の境目の近くの行'), ('facts', 'v̂ の行の様式の z の絶対値の最大')]),
    544: ('§3.5 主の札・§5 読みの決まり', [('draft', '等方の方向とも、八腕の差（兄弟を除く'), ('draft', '組）とも区別できる」、M_E は'), ('draft', '等方の方向とも、同じ組み立ての語の集合とも区別できる')]),
    545: ('§5 語の反響・様式', [('draft', 'Osec にだけある語に比べて、O にだけある語を押し上げる向きだった'), ('draft', '語彙の平均に比べて、コードブロックの書き出しを押し上げる向きだった')]),
    546: ('§5 二つ目の札だけ・§4 S4 の自然の対照', [('draft', '| 二つ目の札だけ |'), ('draft', '符号つきの値で四本')]),
    547: ('§4 S4 の自然の対照', [('draft', 'S4 では、選択の一様化は Osec-Ncold の土台でだけ起き'), ('draft', '土台による違いを、層一の値から説明しない')]),
    548: ('正本の器の自己検査・§9', [('gen', 'assert not ban_hits'), ('draft', '正本: 固定の文が禁止語（三つの一覧の和）を含まない')]),
    549: ('§3.1 落とした成分', [('draft', 'ĥ·u の符号に応じて一様に縮める（強める）向き。引く腕では反転する')]),
    550: ('§1 v̂ が比べているもの', [('draft', '問えるのはこの差（語域・字種と長さ・含み。分けられない）')]),
    551: ('§8 予想の項目', [('draft', '（記述・比べる相手として弱い・§3.2）'), ('draft', '主位置の比を出す行のうち')]),
    552: ('§9 器の自己検査', [('draft', '組み立てた中の集合を主にし、単独の集合を感度にして、違ったトークンを印字して続ける'), ('draft', '止めて登録者に相談すること')]),
    553: ('§4 選び方・§7', [('draft', 'この突き合わせはチャットの型や場面の組み立ての違いを捕まえない')]),
    554: ('§3.3 X の印・転記行 B', [('draft', '腕の前置き（どの腕でも・Ncold と Nk の一行を含む）に現れるものに印を付け'), ('facts', '「交」（arm）')]),
    555: ('§7 限界', [('draft', '様式の感度に残る「私は」は、O の腕の出力の書き出し')]),
    556: ('転記行 B・§7', [('facts', 'しそ〔平仮名にかかる断片〕'), ('draft', '「レーション」は多くの外来語の末尾と同じトークン')]),
    557: ('転記行 B', [('facts', '最初のトークンが断片の升目の、生の出力の最初の字')]),
    558: ('第二巡の採否表 §4・§7', [('r2table', 'C1-11（活性の共分散に沿う帰無）'), ('draft', '活性の共分散に沿う帰無は置かない')]),
    559: ('§3.3 感度の集合・転記行 B', [('draft', '漢字か片仮名の字を二字以上含むトークンの集合'), ('facts', '二字以上の感度の集合')]),
    560: ('第二巡の採否表（記帳）', [('r2table', 'P497 の要約が第一巡の語を縮めたという指摘')]),
    561: ('§10・正本の番号', [('draft', '設計の巡は二巡で済んだ'), ('canon', '"rulings_next": "D186"')]),
    562: ('§9 合成データ', [('draft', '正規化の後の値を取ったフック（logits の突き合わせで止まる）'), ('draft', '一字の漢字を一様に押す方向')]),
    563: ('§4 門の目安', [('draft', '表は目安の上寄り')]),
    564: ('§7 限界', [('draft', '比は pt の反実仮想'), ('draft', '語の側の帰無は、候補を日本の字（cp932）のトークンに限り')]),
}
assert sorted(MAP2) == sorted(AT2), set(AT2) ^ set(MAP2)

# 第一巡の行: 草案2 の突き合わせの器の文字列を読み、草案3 で意図して書き換えた所だけ差し替える
src2 = rd('records/Blens/map_draft2_Blens.py')
i, k = src2.index('MAP = {'), src2.index('\n}\n', src2.index('MAP = {')) + 3
ns = {}
exec(src2[i:k], ns)
MAP1 = ns['MAP']
assert sorted(MAP1) == sorted(AT1)
REWRITE = {   # 第一巡の行の文字列 → 草案3 での文字列（書き換えた第二巡の採否の行）
    (500, '**v̂ を抜いた門**（720 通り）'): ('**v̂ を抜いた門**（56 行・720 通り）', 'P528'),
    (503, 'M_L の値は survival の三場面で同じ'): ('M_L も M_X も survival の三場面で同じ値', 'P532'),
    (507, '「帰無の方向一般と区別できる」と書くのは、二つの札が両方付いたときに限る'): ('両方付いたときの言い方は、物差しごとの決まり（`primary.print_rule`）に従う', 'P544'),
    (520, '**大きさの目盛り**（Colab・裁定 D170）'): ('**大きさの目盛り**（Colab・裁定 D170・D180）', 'P536'),
    (521, '閾の近くから押し切った'): ('土台による違いを、層一の値から説明しない', 'P547'),
    (523, '二つの器の集合がバイトで一致し'): ('二つの器の集合がバイトで一致する', 'P552'),
    (524, '**情報状態**: 予想者（登録者とコーディネータ）は、封印の前に設計の巡の四票'): ('**情報状態**: 予想者（登録者とコーディネータ）は、封印の前に設計の巡の二巡の八票', 'P551'),
}
used_rw = set()
out2, out1, bad = [], [], []
cell = lambda s: s.replace('|', '｜')
for p in sorted(MAP2):
    where, probes = MAP2[p]
    res = []
    for src, s in probes:
        ok = s in TXT[src]
        res.append('%s「%s」%s' % (src, cell(s), '' if ok else '（無い）'))
        if not ok:
            bad.append((p, src, s))
    out2.append('| P%d | %s | %s | %s | %s |' % (p, cell(AT2[p][2]), where, '／'.join(res), '在る' if all(s in TXT[src] for src, s in probes) else '**無い**'))
for p in sorted(MAP1):
    where, probes = MAP1[p]
    res, notes = [], []
    for src, s in probes:
        if (p, s) in REWRITE:
            s2, why = REWRITE[(p, s)]
            used_rw.add((p, s))
            notes.append(why)
            s = s2
        ok = s in TXT[src]
        res.append('%s「%s」%s' % (src, cell(s), '' if ok else '（無い）'))
        if not ok:
            bad.append((p, src, s))
    out1.append('| P%d | %s | %s | %s | %s |' % (p, cell(AT1[p][3]), where, '／'.join(res), ('在る（草案3 で書き換え: %s）' % '・'.join(notes)) if notes else '在る'))
assert used_rw == set(REWRITE), set(REWRITE) - used_rw
assert not bad, bad
n2, n1 = sum(len(v[1]) for v in MAP2.values()), sum(len(v[1]) for v in MAP1.values())
M = ['# B-lens 草案3 と、設計の巡の二巡の採否表の機械の突き合わせ（器 `records/Blens/map_draft3_Blens.py`・2026-09-23）', '',
     '- 第二巡の採否表: `%s`（SHA16 %s）・登録者裁定 D185 で案のとおり。第一巡の採否表: `%s`（SHA16 %s）・裁定 D176。' % (AT2_REL, s16(AT2_REL), AT1_REL, s16(AT1_REL)),
     '- 照らした先: 草案3 `%s`（SHA16 %s）・正本 `%s`（SHA16 %s）・設計の事実 `%s`（SHA16 %s）・README（SHA16 %s）・正本の器（SHA16 %s）・第二巡の採否表。' % (
         SRC['draft'], s16(SRC['draft']), SRC['canon'], s16(SRC['canon']), SRC['facts'], s16(SRC['facts']), s16(SRC['readme']), s16(SRC['gen'])),
     '- やり方: 第二巡の %d 行・確かめた文字列 %d。第一巡の %d 行・確かめた文字列 %d（草案2 の突き合わせの文字列のうち %d を、草案3 で意図して書き換えた後の文字列に差し替えた）。無かったもの %d。' % (len(MAP2), n2, len(MAP1), n1, len(REWRITE), len(bad)),
     '', '## 1. 第二巡の採否表（P528〜P564）', '',
     '| 採否表の行 | 採否の案 | 受けた所 | 確かめた文字列（照らした先「文字列」） | 結果 |', '|---|---|---|---|---|'] + out2 + [
     '', '## 2. 第一巡の採否表（P495〜P527）を草案3 で確かめ直した', '',
     '| 採否表の行 | 採否の案 | 受けた所（草案2 の時） | 確かめた文字列（照らした先「文字列」） | 結果 |', '|---|---|---|---|---|'] + out1 + [
     '', '## この突き合わせが確認していないこと', '',
     '- 文字列が在ることだけを確かめた。直しの中身が正しいか・票の所見を取り違えていないかは、この器では見ていない（起草者の通読 `records/Blens/draft3-read-Blens.md` と、これからの器の実装と結果の巡で見る）。',
     '- 確かめる文字列は起草者が選んだ。起草者の選び方が、直しの要の文を外している見込みは残る。草案3 は外の目を通らない（裁定 D178）。',
     '', '## 検分票', '',
     '- 対象: 二巡の採否表の各行が、草案3・正本・設計の事実・README・正本の器のどこで受けられたか。',
     '- 段階: 事前登録の前段（射影は一つも計算していない）。',
     '- 凍結物の同定: 段階 B の凍結物には触れていない。',
     '- 盲検の状態: 射影の値は誰も見ていない。',
     '- 敵対的検分: 全ての行に、受けた所の文字列を一つ以上置き、無ければ止まる器にした。第一巡の行を草案3 で確かめ直し、書き換えた所を表に書いた。',
     '- 系統の内訳: 起草者（Claude Opus 5.5）のみ。',
     '- COI記録: 起草者は「直した」と書く側に引かれる。文字列の在りかを機械で確かめるのは、その歯止め。',
     '- 判定: 確定（在ることの確かめとして）。',
     '- 本検分が確認していないこと: 上の節。',
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(HERE, 'draft3-mapping-Blens.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('round2 rows', len(MAP2), 'probes', n2, '| round1 rows', len(MAP1), 'probes', n1, 'rewritten', len(REWRITE), '| missing', len(bad))
