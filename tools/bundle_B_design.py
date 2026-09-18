# -*- coding: utf-8 -*-
"""bundle_B_design.py v1 —— 段階 B 設計の検分（二段目・系統内外）の依頼文と資料の束を機械で作る（2026-09-18）。
束は貼り付けて読める形に分け、各部の冒頭に入力の SHA16 を置く。数と引用は記録からの逐語の写しのみ（手で打たない）。
用法: python tools/bundle_B_design.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, json, hashlib, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(REPO, 'records', 'reviews', 'B', 'design-round2')
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda *p: hashlib.sha256(open(os.path.join(REPO, *p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

FILES = {
    'draft': ('design', 'design-stageB-draft7.md'),
    'canon': ('design', 'contrasts-B.json'),
    'facts': ('records', 'B', 'design-facts-B.md'),
    'lint': ('records', 'B', 'numbers-lint-draft7B.md'),
    'restart': ('records', 'B', 'stageB-restart-2026-09-18.md'),
    'adoption1': ('records', 'reviews', 'B', 'design-round1', 'adoption-table-B-design.md'),
    'verify1': ('records', 'reviews', 'B', 'design-round1', 'verification-B-design.md'),
    'request1': ('records', 'reviews', 'B', 'design-round1', 'review-request-B-design-agents.md'),
}
SHA = {k: s16(*v) for k, v in FILES.items()}
REL = {k: '/'.join(v) for k, v in FILES.items()}
T = json.loads(rd(*FILES['canon']))
RP = T['review_plan']

# ---- 依頼文 ----
L = []
a = L.append
a('# 段階 B 設計草案7B の検分の依頼（二段目・系統内外・2026-09-18）')
a('')
a('- 依頼者: 南無弥勒如来（コーディネータ・起草者・Claude Opus 5）／登録者: 楠見優太（この依頼文と資料を、登録者が各位に渡します）')
a('- 検分していただく方: **claude.ai の Claude（系統内）**と **Gemini（系統外）**。裁定 D59 により、各段に系統外を二名以上入れます。claude.ai の票は、起草者と同一系列なので**一票**として数えます。')
a('- 対象: `%s`（SHA16 %s）。付属: 正本 `%s`（SHA16 %s）・転記行 `%s`（SHA16 %s）・数の機械検査 `%s`（SHA16 %s）。' % (REL['draft'], SHA['draft'], REL['canon'], SHA['canon'], REL['facts'], SHA['facts'], REL['lint'], SHA['lint']))
a('- 資料の束: `bundle-B-design-index.md`（この索引）・`part1`（依頼文・草案7B・転記行・数の検査）・`part2`（正本 JSON の逐語）・`part3`（再開の記録・一段目の採否表と再現の記録）。')
a('- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束に入れた資料はすべて公開されています）')
a('')
a('## 0. この検分の位置と、先に申し上げる不利な材料')
a('')
a('1. **草案1 から草案4 までの検分（系統内一巡・系統外四票・claude.ai 三票）と起草者は、設計の根に関わる誤りを誰も見つけませんでした。** 前置きブロックの末尾トークンの活性は腕だけで決まり、試行にも場面にも依らず、前置きを持たない N 腕には存在しない——この事実で、当時の主抽出位置と門が成り立たなくなりました。')
a('2. 一段目（本草案の前の版）の検分は、**起草者と同一系列のエージェント二体**で行いました。二体は重大を五つと六つ挙げ、**そのうち一つは起草者が当日入れた誤り**（機械生成の転記行の数の取り違え）でした。所見は再現して採否表にまとめ、登録者の裁定を経て本草案に反映しています（part3）。')
a('3. **同一系列の目だけでは足りない**というのが、このプログラムで繰り返し確かめられてきたことです。系統外の目をお願いする理由がそこにあります。')
a('4. **本草案の全体が、一つの未測の上に立っています**: 主抽出位置（プロンプトの最終トークン）の方向を足し引きして、破局的選択率が動くかどうかは、まだ誰も測っていません。器材もまだありません。')
a('')
a('## 1. 重点（裁定 D67・一段目と同じ三つ）')
a('')
for i, f in enumerate(RP['focus'], 1):
    a('%d. **%s**' % (i, f))
a('')
a('加えて、**一段目が見落とした型の穴**を探していただけると助かります。一段目の所見と採否は part3 にありますが、**先に草案と正本だけを読んで自分の所見を書き、その後に part3 を読む**という順でも構いません（先に読むと、そちらに視線が寄る危険があります。どちらの順で読んだかを、票に書いていただけると助かります）。')
a('')
a('## 2. 見ていただきたい具体の点（網羅ではない・ここに無い点を挙げてよい）')
a('')
a('- 主位置の方向の加減で率が動きうるか。動かないとき、草案は何を言えると書いているか（読み条項 (ix)・(xii)）。その言い方は測れる範囲を超えていないか。')
a('- 選定（層 × 係数を調整走行の効き目で選ぶ）と、確証（本走行の v 対 ランダム方向）の関係。選定の雑音（転記行 C）の下で、確証の族の読みが壊れていないか。')
a('- 統制の配線の向き（v 対 ランダム方向・腕対の差方向・無操作）。**どちらに転んでも「効いた」と読める配線**になっていないか。')
a('- 品質床の射程と合格の規則。相手側（ランダム方向など）の能力低下が差を作る経路が塞がっているか。')
a('- S4 の反証（封印する予想・判定の規則）が、外れたときに本当に不利な材料として働くか。')
a('- 両用性の扱い（層・係数・要約統計と v̂ の SHA を公開する一方、上昇を招く操作の再現手順は書かない）が、実際に運べるか。')
a('- 利益相反の申告（§0）の「置いた印」と「引かれる向きと同じ側にある決定」の分け方が、実態と合っているか。')
a('- 転記行（規模・費用・選定の雑音・検出力・品質床・活性の容量）の値が、正本の定数から辿れるか。')
a('')
a('## 3. 作法のお願い')
a('')
a('1. 数を確かめるときは、**正本と転記行から自分で計算し直して**ください。起草者の文を根拠にしないでください。')
a('2. 所見は **重大・中・軽微** に分け、(a) 対象（節）、(b) 事実（引用か再計算の値）、(c) なぜ問題か、(d) 直し方の案、を書いてください。')
a('3. 末尾に「**この検分が確認していないこと**」を一項目以上書いてください。判定は「差し戻し／条件つき／このまま進める」でお願いします。')
a('4. 価値語・機序語（「察知の座」「意識」「防御回路」など）は使わないでください。')
a('5. いただいた票は、**逐語のまま公開の置き場に保全**します（書き換えません）。所見は票の数では採らず、起草者が一次記録から再現してから採否を決めます。再現しなかった所見は、その旨を記録して採りません。')
a('')
a('## 4. この依頼が確認していないこと')
a('')
a('- 主位置の方向の加減で率が動くかは未測です（依頼者も知りません）。')
a('- 器材（抽出・操作・集計）はまだありません。実装の検分は次の段です。')
a('- 品質床の課題はまだ選んでいません（裁定 D66・候補は器材の整備の段で出します）。')
a('')
a('本依頼文のいかなる記述も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
a('')
req = '\n'.join(L)
os.makedirs(OUTDIR, exist_ok=True)
open(os.path.join(OUTDIR, 'review-request-B-design-ext.md'), 'w', encoding='utf-8', newline='\n').write(req)
req_sha = hashlib.sha256(req.encode('utf-8')).hexdigest()[:16].upper()

# ---- 束 ----
head = lambda title, items: ['# %s' % title, '',
                             '- 生成: %s UTC（日本時間 %s）・器 `tools/bundle_B_design.py`' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M')),
                             '- 収めたもの（逐語・SHA16 は器が計算）: %s' % '・'.join(items), '']
parts = {}
p1 = head('段階 B 設計草案7B の検分——資料の束 part1（依頼文・草案・転記行・数の検査）',
          ['依頼文（SHA16 %s）' % req_sha, '%s（SHA16 %s）' % (REL['draft'], SHA['draft']),
           '%s（SHA16 %s）' % (REL['facts'], SHA['facts']), '%s（SHA16 %s）' % (REL['lint'], SHA['lint'])])
p1 += ['---', '', '## 依頼文（逐語）', '', req, '', '---', '', '## 草案7B（逐語・`%s`）' % REL['draft'], '', rd(*FILES['draft']), '', '---', '',
       '## 転記行（逐語・`%s`）' % REL['facts'], '', rd(*FILES['facts']), '', '---', '',
       '## 数の機械検査（逐語・`%s`）' % REL['lint'], '', rd(*FILES['lint'])]
parts['part1'] = p1

p2 = head('段階 B 設計草案7B の検分——資料の束 part2（正本 JSON の逐語）',
          ['%s（SHA16 %s）' % (REL['canon'], SHA['canon'])])
p2 += ['本文と正本が食い違う場合は正本が勝ちます。以下は逐語です。', '', '```json', rd(*FILES['canon']).rstrip('\n'), '```']
parts['part2'] = p2

p3 = head('段階 B 設計草案7B の検分——資料の束 part3（背景・一段目の記録）',
          ['%s（SHA16 %s）' % (REL['restart'], SHA['restart']), '%s（SHA16 %s）' % (REL['adoption1'], SHA['adoption1']),
           '%s（SHA16 %s）' % (REL['verify1'], SHA['verify1']), '%s（SHA16 %s）' % (REL['request1'], SHA['request1'])])
p3 += ['**注意**: ここには一段目（エージェント二体）の所見と採否が入っています。先に part1・part2 だけを読んで自分の所見を書き、その後にここを読む順でも構いません。どちらの順で読んだかを票に書いてください。', '',
       '---', '', '## 再開の記録（逐語・`%s`）' % REL['restart'], '', rd(*FILES['restart']), '', '---', '',
       '## 一段目の採否表（逐語・`%s`）' % REL['adoption1'], '', rd(*FILES['adoption1']), '', '---', '',
       '## 一段目の再現の記録（逐語・`%s`）' % REL['verify1'], '', rd(*FILES['verify1']), '', '---', '',
       '## 一段目の依頼文（逐語・`%s`）' % REL['request1'], '', rd(*FILES['request1'])]
parts['part3'] = p3

written = {}
for name, lines in parts.items():
    txt = '\n'.join(lines) + '\n'
    path = os.path.join(OUTDIR, 'bundle-B-design-%s.md' % name)
    open(path, 'w', encoding='utf-8', newline='\n').write(txt)
    written[name] = (len(txt), hashlib.sha256(txt.encode('utf-8')).hexdigest()[:16].upper())

idx = head('段階 B 設計草案7B の検分——資料の束 索引', ['part1・part2・part3'])
idx += ['| 部 | 中身 | 字数 | SHA16 |', '|---|---|---|---|']
for name in ('part1', 'part2', 'part3'):
    what = {'part1': '依頼文・草案7B・転記行・数の検査', 'part2': '正本 JSON の逐語', 'part3': '再開の記録・一段目の採否表と再現の記録・一段目の依頼文'}[name]
    idx.append('| %s | %s | %s | %s |' % (name, what, format(written[name][0], ','), written[name][1]))
idx += ['', '- 対象の SHA16: %s' % '・'.join('%s %s' % (REL[k], SHA[k]) for k in ('draft', 'canon', 'facts', 'lint')),
        '- 読む順: part1 → part2 →（自分の所見を書いた後で）part3。', '',
        '本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
itxt = '\n'.join(idx)
open(os.path.join(OUTDIR, 'bundle-B-design-index.md'), 'w', encoding='utf-8', newline='\n').write(itxt)
print('[bundle-B-design] 依頼文 sha16=%s' % req_sha)
for name in ('index', 'part1', 'part2', 'part3'):
    pth = os.path.join(OUTDIR, 'bundle-B-design-%s.md' % name)
    print('  %-6s %8s 字 sha16=%s' % (name, format(len(open(pth, encoding='utf-8').read()), ','), hashlib.sha256(open(pth, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()))
