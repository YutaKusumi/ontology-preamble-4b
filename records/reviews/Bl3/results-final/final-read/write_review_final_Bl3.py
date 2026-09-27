# -*- coding: utf-8 -*-
"""起草者の最終の見直しの記録を書く（正本 `review_plan.order` の「起草者の最終の見直し」・B-lens の `records/reviews/Blens/results-final/final-read/` の型）。
見直した版は、最終版の案 `records/Bl3/results-Bl3-FINAL-2026-09-27.md`（逸脱の器 v2 の `--final`・登録者最終確認の前）。所見の引く行の番号と文は、器が最終版の案から抜き出す（手で打たない）。
確かめの記録（逸脱の器の確かめと、器とは別の確かめ）の結果も、記録から機械で読む。既にある記録には書かない。
用法: python records/reviews/Bl3/results-final/final-read/write_review_final_Bl3.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
NL = chr(10)
OUT = os.path.join(HERE, 'review-final-Bl3.md')
assert not os.path.exists(OUT), '既にある（一度だけ）: ' + OUT
P = lambda r: os.path.join(REPO, *r.split('/'))
s16 = lambda r: hashlib.sha256(open(P(r), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
FINAL = 'records/Bl3/results-Bl3-FINAL-2026-09-27.md'
FL = open(P(FINAL), encoding='utf-8').read().replace('\r\n', NL).split(NL)
D2 = open(P('records/Bl3/results-Bl3-draft2.md'), encoding='utf-8').read().replace('\r\n', NL).split(NL)
line_of = lambda Ls, s: [i + 1 for i, l in enumerate(Ls) if s in l]
fa_f, fa_d = line_of(FL, '向きまで数えた順位の分母の逆数は'), line_of(D2, '向きまで数えた比べる相手の数の逆数は')
fb = line_of(FL, '- 【逸脱 D-BLT1】**報告の表し方（結果の巡の後）**')
fc = line_of(FL, '次の区画の表は凍結した器の出力で')
fd = line_of(FL, '- 【逸脱 D-BLT1】上の検分票は、凍結した組み立ての器が結果の巡の前に出したもので')
assert len(fa_f) == 1 and len(fa_d) == 1 and len(fb) == 1 and len(fc) == 3 and len(fd) == 1, (fa_f, fa_d, fb, fc, fd)
A = json.load(open(P('records/Bl3/analysis-Bl3.json'), encoding='utf-8'))
sec = A['rows']['sub:N1:O-Ncold-v~O-Ncold-vrand']['second']
CKF = json.load(open(P('records/Bl3/results-Bl3-FINAL-2026-09-27-checks.json'), encoding='utf-8'))
CF = json.load(open(P('records/Bl3/final-check/check-final-Bl3.json'), encoding='utf-8'))
cmp = CKF['draft2_compare']
L = ['# 起草者の最終の見直し（B-lens 層三・報告の最終版の案・2026-09-27）', '',
     '- 見直した版: `%s`（SHA16 %s・逸脱の器 `tools/build_report_Bl3_devBLT1.py` v2 の `--final`・登録者最終確認の前）。行の数 %d。' % (FINAL, s16(FINAL), len(FL) - (1 if FL[-1] == '' else 0)),
     '- 見直した人: 南無弥勒如来（コーディネータ・Claude Opus 5.5）。器と報告の組み立ての器と逸脱の器と起草者の欄を書いた当人で、外の目ではない。',
     '- 段階: 事後。見直しの枠（手順・重さの決まり・予想）を、読む前に書いていない（B-lens の最終の見直しは枠を先に書いた・この見直しの弱さとして記す）。起草者は、草案の二つ目を組むときに全文を読み、最終版の案を組んだ後に、頭から末尾まで節ごとにもう一度読んだ。', '',
     '## 1. 器で確かめたこと（記録から機械で読んだ）', '',
     '- 逸脱の器の確かめ（`records/Bl3/results-Bl3-FINAL-2026-09-27-checks.json`）: 凍結した器の出力の作り直しがバイトで同じ・足した区画 %d を除いて見出しと状態の行を戻すと凍結した器の出力とバイトで同じ・並べ直しの表 %d・走査の違反 %d・結果の巡の再現の記録と照らした項 %d（外れ 0）。' % (
         CKF['added_blocks'], len(CKF['tables']), CKF['lint_violations'], len(CKF['cross_checks'])),
     '- 草案の二つ目（最終の検分を受けた版・SHA16 %s）との違い: 消えた行 %d・足された行 %d で、どれも決めた行（%s）（逸脱の器と、器とは別の確かめの両方）。' % (cmp['draft2_sha16'], cmp['removed_lines'], cmp['added_lines'], cmp['allowed']),
     '- 器とは別の確かめ（`records/Bl3/final-check/check-final-Bl3.md`）: %d／%d が合う。' % (sum(1 for x in CF['checks'] if x['ok']), len(CF['checks'])), '',
     '## 2. 所見', '',
     '| 番号 | 重さ | 置き場（最終版の案の行） | 所見 | 案 |', '|---|---|---|---|---|',
     '| F-a | 軽（直す） | %d 行（草案の二つ目では %d 行） | 〈両方の外〉の注の「向きまで数えた比べる相手の数の逆数」は不正確だった。順位の分母（%d）は、行と、向きまで数えた比べる相手を合わせた数で、比べる相手の数そのものではない（兄弟を除いた比べる相手は一つ少ない）。値（その逆数）は正しい | 「向きまで数えた順位の分母の逆数」に直す（案の版は直した形で組んである・裁定 D251 の甲）。草案の二つ目は検分を受けたまま残す |' % (fa_f[0], fa_d[0], sec['of_oriented']),
     '| F-b | 軽（記録） | %d 行 | 凍結の後の逸脱の一覧の D-BLT1 の行は、出力を草案の二つ目と書く（台帳に記したときの文）。最終版も同じ逸脱の器（v2）の出力である | 台帳は後ろに足すだけで前の行を書き換えないので、そのままにする。最終版の頭の添えが器の版と裁定を書いている |' % fb[0],
     '| F-c | 軽（記録） | %s 行 | 表示で崩れる凍結の表と、並べ直しの表が、三つの表ごとに両方ある（裁定 D243 の甲の一・B-lens の型）。読む人は断りの行で並べ直しの表へ導かれる | そのまま（裁定のとおり） |' % '・'.join(str(x) for x in fc),
     '| F-d | 軽（記録） | %d 行の上 | 凍結した組み立ての器が結果の巡の前に出した検分票が、凍結の出力のまま残る（足した区画がそう断る） | そのまま |' % fd[0], '',
     '- 札・門・読みの型・予想の照合の判定と、数と、読みの向きを変える所見は無い。',
     '- 最終版で改めた行（決めた行と F-a）のほかに、直した方がよい所は見つけなかった（起草者一名の読みで、同じ系列の目は一つ）。', '',
     '## 3. 裁定の候補', '',
     '- **D251（起草者の最終の見直しの直し）**: 甲（推奨）F-a を最終版に入れる（逸脱の器 v2 の組み方の中・草案の二つ目との違いの決めた行に足す）／乙 F-a を入れず、記録だけにする。',
     '- **D252（公開の仕上げ）**: 甲（推奨）登録者最終確認の後に、確認のお言葉と時刻を最終版の状態の行に入れて組み直し（凍結した器の最終版の型の行・確認していただいた案と状態の行のほかは同じことを器で確かめる）、確認していただいた案を一字違わず残す。README の B-lens の節の後に層三の案内の一行（最終版・凍結の本文・正本・凍結の記録と逸脱台帳・封印の前の露出の記録・開く段の記録・検分の置き場）を載せ、公開の後に、最終版の入ったコミットに注釈つきのタグ `release-Bl3-2026-09-27` を付ける（B-lens の D200 の型）／乙 README の一行とタグは置かない。', '',
     '## 検分票', '',
     '- 対象: 報告の最終版の案（登録者最終確認の前）。',
     '- 段階: 事後（見直しの枠を読む前に書いていない）。',
     '- 凍結物の同定: 正本と凍結の本文は凍結の記録の値のまま（逸脱の器の確かめ）。',
     '- 盲検の状態: 該当しない（結果は開いた後）。',
     '- 敵対的検分: 足した区画の数は器が記録から読み、再現の記録と照らした。最終版の案の文を頭から末尾まで読み、足した区画の一行ずつの言い方を、記録の意味と照らした（F-a はそれで見つけた）。',
     '- 系統の内訳: 起草者（Claude 系）一名。外の目ではない。',
     '- COI記録: 起草者は「直した」と書く側と、進める側に引かれる。所見の無いことを是認の証しにしない。F-a は、最終の検分の二票も、結果の巡の四票も挙げなかった言い方の誤りで、起草者自身の誤りでもある。',
     '- 判定: 登録者裁定要（D251・D252）と登録者最終確認。',
     '- 本検分が確認していないこと: 最終版の公開の置き場での表示（公開の後に確かめる）。足した区画の文の言い過ぎを、起草者一名の読みより先では確かめていない。見直しの枠を先に書かなかったので、読む前の予想が無い。', '',
     '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(OUT, 'w', encoding='utf-8', newline=NL).write(NL.join(L))
print('wrote', os.path.relpath(OUT, REPO), '| F-a lines', fa_f, fa_d, '| F-b', fb, '| F-c', fc, '| F-d', fd)
