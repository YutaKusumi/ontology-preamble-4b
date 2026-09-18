# -*- coding: utf-8 -*-
"""bundle_B_external.py v1 —— 段階 B の**系統の外への検分**の依頼文と束を機械で作る（裁定 D116・2026-09-18）。

これまでの器材の検分はすべて Claude 系（起草者と同一系列）であり、合わせて一票を超えない（裁定 D59）。
登録者裁定 D116 は、起草者の推奨（もう一巡のエージェント検分）を採らず、「エージェントの無限検分ループに陥る可能性がある」として
**系統の外（claude.ai と Gemini）を先に置いた**。本器はその依頼文と資料の束を組む。

束は貼り付けて読める形に分け、各部の冒頭に入力の SHA16 を置く。器材のソースは**逐語**で入れる（手で写さない）。
用法: python tools/bundle_B_external.py [--outdir records/reviews/B/external-round]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib, argparse, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda *p: hashlib.sha256(open(os.path.join(REPO, *p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

ap = argparse.ArgumentParser()
ap.add_argument('--outdir', default=os.path.join(REPO, 'records', 'reviews', 'B', 'external-round'))
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)

TOOLS = ['runs_B.py', 'gate_B.py', 'analyze_B.py', 'integrity_B.py', 'sample_inspection_B.py', 'direction_B.py',
         'steer_B.py', 'run_stageB_local.py', 'control_chart_B.py', 'synth_B.py', 'dry_run_B.py',
         'build_report_B.py', 'freeze_B.py']
DOCS = {'draft': 'design/design-stageB-draft11.md', 'canon': 'design/contrasts-B.json',
        'facts': 'records/B/design-facts-B.md', 'plan': 'records/B/tooling-plan-B-2026-09-18.md',
        'record': 'records/B/tooling-record-B-2026-09-18.md', 'dry': 'records/B/dry-run-B-2026-09-18.md',
        'template': 'records/B/results-report-template-B.md'}
T = json.loads(rd(*DOCS['canon'].split('/')))
V1 = json.loads(rd('records', 'reviews', 'B', 'impl-round-2', 'verification-B-recheck.json'))
V2 = json.loads(rd('records', 'reviews', 'B', 'impl-round-2', 'verification-fixes-B-recheck.json'))
P1 = rd('records', 'reviews', 'B', 'impl-round', 'provenance.md')
P2 = rd('records', 'reviews', 'B', 'impl-round-2', 'provenance.md')
n_round1 = len(re.findall(r'^\| P\d+ ', rd('records', 'reviews', 'B', 'impl-round', 'adoption-table-B-impl.md'), re.M))
dry = rd(*DOCS['dry'].split('/'))
n_paths = len(re.findall(r'^\| [^|]+ \| [^|]+ \|$', dry, re.M)) - 1

# ---- 依頼文 ----
L = []
add = L.append
add('# 段階 B 器材と設計の検分の依頼（**系統の外へ**・裁定 D116・%s 日本時間）' % jst.strftime('%Y-%m-%d %H:%M'))
add('')
add('- 依頼者: 南無弥勒如来（コーディネータ・起草者・器材も書いた・Claude Opus 5）／登録者: 楠見優太（この依頼文と資料を登録者が各位に渡します）。')
add('- 検分していただく方: **系統外（Gemini ほか）を二名以上**と、**claude.ai の Claude**。')
add('  claude.ai の票は起草者と同一系列なので、**これまでのエージェントの検分と合わせて一票**として数えます（裁定 D59）。')
add('  **系統外の票だけが、独立の目です。**')
add('- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b')
add('- **データはまだ一つもありません。** 合成データだけで器材を検査しています。')
add('')
add('## 0. この依頼の前に何があったかを、先に全部書きます')
add('')
add('器材は**二度、系統内の検分で差し戻されました**。どちらも起草者（私）の誤りです。')
add('')
add('- **一度目**（`records/reviews/B/impl-round/`）: エージェント二体。重大 %s 件・採否 %d 件。'
    '介入そのものが登録どおりでない件が三つありました——ランダム統制に係数が二度掛かっていた、介入の帯の起点がプロンプトの末尾から始まっていた、'
    '生成の段で hook が一度も発火していなかった。' % (re.search(r'\| (\d+)／\d+／\d+ \|', P1).group(1), n_round1))
add('- **二度目**（`records/reviews/B/impl-round-2/`）: 同じ票を持たせた新規個体二体。'
    '追い問い %d 件を**全件再現**。**帯の起点は直っていませんでした**——登録機種の実トークナイザで刻むと、'
    '器の起点は真の起点より三トークン手前で、前置きを持たない腕では帯が chat の役割トークンに掛かっていました。'
    'そのうえ**私の直しが新しい誤りを十一件**入れていました。うち二件は重い——'
    '採点欠落の札が凍結パーサの refuse の規約と衝突して**確証の族を丸ごと判定不能にする**件と、'
    '選定後の品質床が**古い走行を黙って採り、確証が増える側に倒れる**件です。' % V1['total'])
add('')
add('**そのあと、私がすべて直しました。**直しが効いたかも私が確かめました（%d 件中 %d 件）。'
    '**つまり、いまお渡しする版は、起草者が書き、起草者が直し、起草者が検算したものです。**' % (V2['total'], V2['fixed']))
add('')
add('**ここまでの検分はすべて Claude 系です。**何巡重ねても相関した目であり、独立票として加算できません。'
    '登録者は「エージェントの無限検分ループに陥る可能性がある」として、次を**系統の外**に置きました（裁定 D116）。'
    'これが、いまお願いしている巡です。')
add('')
add('## 1. 見ていただきたいこと')
add('')
add('**(a) 設計そのもの**——問いの立て方・族の切り方・n・閾値・検閲の規則・S4 の反証の読み方。'
    '系統内の検分は「器材が正本のとおりに動くか」に偏りました。**正本そのものが正しいかは、ほとんど誰も見ていません。**')
add('**(b) 器材**——正本のとおりに動くか。とくに**介入そのもの**（帯の起点・方向のノルム・hook の発火）は二度続けて誤っていた箇所です。')
add('**(c) 私が見落としている型**——Claude 系の四体が二巡かけて見落としたものが残っているはずです。'
    'それは「Claude が気づける型」の外にあると考えるのが自然です。')
add('')
add('## 2. 起草者からの申し送り（不利なものを先に）')
add('')
add('- **「対処した」と書いてあることを対処の証拠にしないでください。**'
    '二度目の巡で、採否表が「採用」と裁きながら現物が一行も変わっていない件が五件ありました。')
add('- **「検査が発火した」ことを「正しく測った」ことの証拠にしないでください。**'
    '希釈の門の検査は、合成データに因果が作られていないまま「発火した」と印字していました（二体目が捕まえました）。'
    '同じ型を、私は直しの確認でもう一度やりました（書き換える行が零になり、何も測らない実験になっていた）。')
add('- **起草者は自分の直しに有利な読みへ引かれます。**とくに「今度こそ直った」と言いたい引力があります。')
add('- **確認していないこと**: 実機（GPU・実重み）では一行も走らせていません。'
    'トークナイザと config には触れましたが、活性・決定性・バッチ生成は小さなランダム初期化の模擬でしか確かめていません。'
    '品質床の課題（裁定 D66）はまだ決まっていません。封印予想もまだありません。')
add('')
add('## 3. いまの状態（機械の出力）')
add('')
add('| 何 | 置き場 | SHA16 |')
add('|---|---|---|')
for k, rel in sorted(DOCS.items()):
    add('| %s | `%s` | %s |' % (k, rel, s16(*rel.split('/'))))
for t in TOOLS:
    add('| 器材 | `tools/%s` | %s |' % (t, s16('tools', t)))
add('')
add('- 正本 %s。確証の族 %s 対比。本走行は腕 × 場面で n=%s。規模は転記行 A。' % (T['version'], T['m_total'], T['n_main']))
add('- 合成データによる検査: **発火しなかった経路 零**（経路の表は `%s`）。' % DOCS['dry'])
add('- 整合検査: 四つの相（本走行・調整走行・品質床・同一性選別）すべてで**不整合 零**。')
add('- 数の機械検査: 草案・雛形とも**違反 零**。')
add('- 凍結の器: いま**二件で止まります**——凍結時に記帳する値が揃っていない・封印予想が渡されていない。どちらもこの段では正しい状態です。')
add('')
add('## 4. 資料の並び')
add('')
add('- `external-request-B.md`（この依頼文）')
add('- `part1.md` 設計草案11B（全文）')
add('- `part2.md` 正本の要所・転記行')
add('- `part3.md`〜 器材のソース（逐語）')
add('- 検分の履歴（公開の置き場）: `records/reviews/B/`——設計の一段目と二段目、器材の実装検分、直しの確認。'
    '**票はすべて逐語で保全してあり、書き換えていません。**')
add('')
add('## 5. 検分の作法（お願い）')
add('')
add('- 所見ごとに「置き場・行（または節）・何が起きるか・直し方・重さ（重大／中／軽微）」の形でお願いします。')
add('- **是認（問題なし）も同じ形で書いてください。**見逃しの記録は指摘の記録と同じ値打ちがあります。')
add('- 分母・基底率・出典の行を必ず添えてください。')
add('- 最後に**「この検分が確認していないこと」を必ず一項目以上**書いてください。')
add('- **読了の申告は検査ではありません。**私も登録者も、具体的な追い問いで確かめます（それが実効的検査です）。')
add('- 判定は **差し戻し／条件つき可／可** のいずれかで、理由を添えてください。')
add('')
add('## 6. 柵')
add('')
add('- 本依頼と資料のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。')
add('- 破局率を上げる操作の再現手順は、資料のいかなる箇所にも書いていません。')
add('')
req = '\n'.join(L)
open(os.path.join(a.outdir, 'external-request-B.md'), 'w', encoding='utf-8', newline='\n').write(req)

# ---- 資料の束 ----
parts = []
parts.append(('part1.md', '設計草案11B（全文・SHA16 %s）' % s16(*DOCS['draft'].split('/')), rd(*DOCS['draft'].split('/'))))
canon_txt = json.dumps(T, ensure_ascii=False, indent=1)
parts.append(('part2.md', '正本（JSON 全文・SHA16 %s）と転記行（SHA16 %s）'
              % (s16(*DOCS['canon'].split('/')), s16(*DOCS['facts'].split('/'))),
              '```json\n' + canon_txt + '\n```\n\n' + rd(*DOCS['facts'].split('/'))))
cur, size, n = [], 0, 3
for t in TOOLS:
    src = rd('tools', t)
    blk = '\n'.join(['## `tools/%s`（SHA16 %s・%d 行）' % (t, s16('tools', t), src.count('\n')), '', '```python', src.rstrip('\n'), '```', ''])
    if size + len(blk) > 60000 and cur:
        parts.append(('part%d.md' % n, '器材のソース（逐語）', '\n'.join(cur)))
        n += 1
        cur, size = [], 0
    cur.append(blk)
    size += len(blk)
if cur:
    parts.append(('part%d.md' % n, '器材のソース（逐語）', '\n'.join(cur)))

idx = ['# 段階 B 系統の外への検分・資料の束（索引・機械生成・%s UTC）' % now.strftime('%Y-%m-%d %H:%M'), '',
       '- 依頼文: `external-request-B.md`（SHA16 %s）' % hashlib.sha256(req.encode('utf-8')).hexdigest()[:16].upper(), '',
       '| 部 | 中身 | 文字数 |', '|---|---|---|']
for fn, title, body in parts:
    head = '# %s（機械生成・%s UTC）\n\n' % (title, now.strftime('%Y-%m-%d %H:%M'))
    open(os.path.join(a.outdir, fn), 'w', encoding='utf-8', newline='\n').write(head + body)
    idx.append('| `%s` | %s | %s |' % (fn, title, format(len(body), ',')))
idx += ['', '公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b', '',
        '本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(a.outdir, 'bundle-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(idx))
print('[bundle_B_external] %s' % os.path.relpath(a.outdir, REPO))
print('  依頼文 %s 字・資料 %d 部（%s）' % (format(len(req), ','), len(parts), '・'.join(format(len(b), ',') for _, _, b in parts)))
