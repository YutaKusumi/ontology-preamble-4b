# -*- coding: utf-8 -*-
"""bundle_B_impl.py v1 —— 段階 B **器材の実装検分**の依頼文と資料の束を機械で作る（2026-09-18・裁定 D86 の「次の外の目」）。

束は貼り付けて読める形に分け、各部の冒頭に入力の SHA16 を置く。器材のソースは**逐語**で入れる（手で写さない）。
用法: python tools/bundle_B_impl.py
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, json, hashlib, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(REPO, 'records', 'reviews', 'B', 'impl-round')
os.makedirs(OUTDIR, exist_ok=True)
rd = lambda *p: open(os.path.join(REPO, *p), encoding='utf-8').read().replace('\r\n', '\n')
s16 = lambda *p: hashlib.sha256(open(os.path.join(REPO, *p), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

TOOLS = ['runs_B.py', 'gate_B.py', 'analyze_B.py', 'integrity_B.py', 'sample_inspection_B.py',
         'direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'synth_B.py', 'dry_run_B.py',
         'build_report_B.py', 'freeze_B.py']
DOCS = {'draft': ('design', 'design-stageB-draft9.md'), 'canon': ('design', 'contrasts-B.json'),
        'facts': ('records', 'B', 'design-facts-B.md'), 'plan': ('records', 'B', 'tooling-plan-B-2026-09-18.md'),
        'record': ('records', 'B', 'tooling-record-B-2026-09-18.md'), 'dry': ('records', 'B', 'dry-run-B-2026-09-18.md'),
        'template': ('records', 'B', 'results-report-template-B.md')}
SHA = {k: s16(*v) for k, v in DOCS.items()}
REL = {k: '/'.join(v) for k, v in DOCS.items()}
TSHA = {t: s16('tools', t) for t in TOOLS}
T = json.loads(rd(*DOCS['canon']))

# ---- 依頼文 ----
L = []
a = L.append
a('# 段階 B **器材の実装検分**の依頼（裁定 D86 の「次の外の目」・2026-09-18）')
a('')
a('- 依頼者: 南無弥勒如来（コーディネータ・起草者・器材も書いた・Claude Opus 5）／登録者: 楠見優太（この依頼文と資料を登録者が各位に渡します）')
a('- 検分していただく方: **系統外（Gemini ほか）を二名以上**と**系統内（claude.ai の Claude）**。claude.ai の票は起草者と同一系列なので**合わせて一票**として数えます（裁定 D59）。')
a('- 対象: **器材そのもの**（下の %d 本）。設計（草案9B・正本）は前の二段で検分済みですが、**器材が正本のとおりに動くか**はまだ誰も外から見ていません。' % len(TOOLS))
a('- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束の資料はすべて公開されています）')
a('- **データはまだ一つもありません。** 合成データだけで器材を検査しています。')
a('')
a('## 0. 先にお伝えする「見逃しの型」')
a('')
a('この設計は、**検分が見逃した誤り**で二度作り直しています。')
a('')
a('1. 草案1〜草案4 の検分（系統内一巡・系統外四票・claude.ai 三票）は、**主抽出位置が成り立たない**ことを全員が見逃しました（結合前置きブロックの末尾トークンの活性は腕だけで決まり、試行にも場面にも依らず、前置きを持たない腕には存在しない）。')
a('2. 設計の検分の一段目（エージェント二体）は、転記行の数の取り違え（私が入れた誤り）を捕まえました。二段目（系統外二名・系統内二名）は、**一つの腕が二つのノルム基準を同時に要求される配線**・**書式が崩れるだけで確証の札が立つ路**・**両側で登録しながら符号を封印していないこと**を捕まえました。')
a('3. **器材を書いたことで、正本の不足が三件**見つかりました（プロンプトの組み立ての式・品質床の相手の走らせ方・走行の記録の欄）。いずれも設計の検分では誰も挙げていません。')
a('')
a('**お願いしたいのは、同じ型の穴です**——「器が黙って決めていること」。正本に書かれていないのに器が一つの振る舞いを選んでいる箇所を探してください。')
a('')
a('## 1. 重点（三つ）')
a('')
a('1. **器が正本のとおりに動くか。** 合成データで札の全経路が発火しましたが、*発火したこと*は*正しく発火したこと*を意味しません。')
a('   とくに: 門の順と札の一意性（`gate_order`）・降格しても族の m を減らさないこと（`censor.m_rule`）・様式門は確証の札にのみ作用すること（`style_gate.asymmetry`）・'
  '希釈の門の向きと分母（`dilution_gate`）・品質床の二段と落ちたときの札（裁定 D77・D88）・封印した符号との照合（裁定 D79）・S4 の三分岐（裁定 D81）。')
a('2. **率盲検と封印の実装。** 整合検査が判定欄を読んでいないか（許可表の抜け）・抽出検査の対応表が公開の置き場の外に出ているか・封印の時機（データを見る前）が器の構造で守られているか。')
a('3. **GPU 側の規則。** 実機では走らせられないので、規則の実装だけを読みます——ランダム方向のノルムの合わせ方（裁定 D75・**族を跨いで v̂ のノルム一つ**）・調整走行と本走行の引き直し（裁定 D84）・'
  '層の割合から層番号への翻訳・詰めの向きと主位置の取り方（採否表 P241）・決定性の検査（二度保存して完全一致・採否表 P235）・介入の帯の起点。')
a('')
a('## 2. 材料')
a('')
a('| 物 | 置き場 | SHA16 |')
a('|---|---|---|')
for k in ('draft', 'canon', 'facts', 'plan', 'record', 'dry', 'template'):
    a('| %s | `%s` | %s |' % ({'draft': '設計草案9B', 'canon': '正本 JSON', 'facts': '転記行', 'plan': '器材の計画（書く前に登録）',
                              'record': '器材の整備の記録', 'dry': '合成データによる検査', 'template': '報告の雛形（結果の前に置いた）'}[k], REL[k], SHA[k]))
for t in TOOLS:
    a('| 器材 | `tools/%s` | %s |' % (t, TSHA[t]))
a('')
a('資料の束: `bundle-B-impl-index.md`（索引）・`part1`（依頼文・器材の計画と記録・合成データの検査）・`part2`（正本の要所）・`part3`〜`part5`（器材のソースの逐語）。')
a('')
a('## 3. 検分の作法（お願い）')
a('')
a('- **読んだだけで「問題なし」と書かないでください。** 具体の行を引いて、何がどうなると壊れるかを書いてください（追い問いだけが実効的な検査です）。')
a('- 所見は**重大・中・軽微**に分け、それぞれに (a) 何が (b) どの行で (c) なぜ問題か (d) 直し方、を書いてください。')
a('- **この検分が確認していないこと**を必ず一項目以上書いてください。')
a('- 私（起草者）の書いたものを信用しないでください。器材の記録に「札の全経路が発火した」と書いてありますが、**その判定を器自身が出している**ことにご注意ください。')
a('- 判定は **問題なし／条件つき／差し戻し** のいずれかでお願いします。')
a('')
a('## 4. この巡で私が確認していないこと（先に開示）')
a('')
a('- **実機で走らせていません。** 活性の抽出・hook つきの生成・バッチの詰め・決定性の検査は、Colab の段で初めて走ります。')
a('- 品質床の課題（出所・版・ライセンス・断片）は未定で、入力・帯・採点・最大トークン数も未定です（凍結の前に登録者が課題を選びます）。')
a('- 封印予想はまだ書いていません（凍結の段・データを一つも見る前に書きます）。')
a('- 走行器の本体（バッチ生成の繰り返し・再開・記録の書き出し）は骨組みで、Colab の段で埋めます。')
a('- 合成データは私が作ったもので、**私が想定した壊れ方しか入っていません**。')
a('')
a('## 5. 柵')
a('')
a('- 本依頼と資料のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。')
a('- 加算で破局率を上げる操作の再現手順を、票の本文・要約・表題に書かないでください（両用性の柵・正本 `publication.dual_use`）。')
a('')
req = '\n'.join(L) + '\n'
open(os.path.join(OUTDIR, 'review-request-B-impl.md'), 'w', encoding='utf-8', newline='\n').write(req)

# ---- 束 ----
def part(name, blocks):
    out = ['# 段階 B 器材の実装検分・資料の束 %s（機械生成・%s UTC）' % (name, now.strftime('%Y-%m-%d %H:%M')), '']
    for title, sha, body, lang in blocks:
        out += ['## %s（SHA16 %s）' % (title, sha), '', '```%s' % lang, body.rstrip('\n'), '```', '']
    p = os.path.join(OUTDIR, 'bundle-B-impl-%s.md' % name)
    open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    return p, len(''.join(b[2] for b in blocks))


canon_keys = ['selection', 'quality_floor', 'gate1', 'censor', 'dilution_gate', 'refuse_gate', 'style_gate', 'gate_order',
              'random_control', 'directions', 'seeds', 'runner', 'activation_storage', 'trial_record', 'denominators',
              'print_strings', 'families', 'descriptive_families', 'seal_format', 'calibration', 'withdrawal', 'sessions',
              'cost', 'judge_validity', 'deviation', 'position_length', 'procedure', 'reading_B', 'report_rules']
canon_sub = json.dumps({k: T[k] for k in canon_keys if k in T}, ensure_ascii=False, indent=1)
parts = []
parts.append(part('part1', [('依頼文', s16('records', 'reviews', 'B', 'impl-round', 'review-request-B-impl.md'), req, ''),
                            ('器材の計画（書く前に登録）', SHA['plan'], rd(*DOCS['plan']), ''),
                            ('器材の整備の記録', SHA['record'], rd(*DOCS['record']), ''),
                            ('合成データによる検査', SHA['dry'], rd(*DOCS['dry']), '')]))
parts.append(part('part2', [('正本の要所（JSON の逐語・全文は公開の置き場）', SHA['canon'], canon_sub, 'json'),
                            ('転記行', SHA['facts'], rd(*DOCS['facts']), '')]))
groups = [('part3', ['runs_B.py', 'gate_B.py', 'analyze_B.py']),
          ('part4', ['integrity_B.py', 'sample_inspection_B.py', 'synth_B.py', 'dry_run_B.py']),
          ('part5', ['direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'build_report_B.py', 'freeze_B.py'])]
for name, ts in groups:
    parts.append(part(name, [('tools/%s' % t, TSHA[t], rd('tools', t), 'python') for t in ts]))

idx = ['# 段階 B 器材の実装検分・資料の束（索引・機械生成・%s UTC）' % now.strftime('%Y-%m-%d %H:%M'), '',
       '- 依頼文: `review-request-B-impl.md`（SHA16 %s）' % s16('records', 'reviews', 'B', 'impl-round', 'review-request-B-impl.md'), '',
       '| 部 | 中身 | 文字数 |', '|---|---|---|']
for (p, n), (name, what) in zip(parts, [('part1', '依頼文・器材の計画・整備の記録・合成データの検査'), ('part2', '正本の要所・転記行'),
                                        ('part3', '読み口・門と選定・集計と札'), ('part4', '整合検査・抽出検査・合成データ・経路の検査'),
                                        ('part5', 'GPU 側の器・走行器・報告・凍結')]):
    idx.append('| `%s` | %s | %s |' % (os.path.basename(p), what, format(n, ',')))
idx += ['', '公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b', '',
        '本索引のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(os.path.join(OUTDIR, 'bundle-B-impl-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(idx))
print('[bundle_B_impl] %s' % OUTDIR)
for p, n in parts:
    print('  %-28s %s 文字' % (os.path.basename(p), format(n, ',')))
