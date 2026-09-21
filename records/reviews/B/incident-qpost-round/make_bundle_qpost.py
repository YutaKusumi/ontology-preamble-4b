# -*- coding: utf-8 -*-
"""意見の伺いの束（選定後の品質床の「走行が無い」・2026-09-22）を組む。引用・コード・数値は現物から機械で取る（手で打たない）。
**確証の族の率と p は束に入れない**（伺う相手には、札がどちらに動くかを伏せる）。
出力: request-qpost.md・materials-qpost.md・all-in-one.md・bundle-index.md（この置き場）。用法: python make_bundle_qpost.py"""
import os, json, hashlib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16 = lambda rel: hashlib.sha256(open(j(*rel.split('/')), 'rb').read()).hexdigest().upper()[:16]
T = json.loads(rd('design/contrasts-B.json'))
A = json.loads(rd('records/B/analysis-B-2026-09-22.json'))
G = json.loads(rd('records/B/gate-B-2026-09-21.json'))
QF = T['quality_floor']
HEAD = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True, cwd=REPO).stdout.strip()
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))


def excerpt(rel, start_has, end_has, include_end=True, max_lines=90):
    """start_has を含む最初の行から、その後で end_has を含む最初の行まで（行番号つき）。"""
    lines = rd(rel).split('\n')
    i0 = next(i for i, l in enumerate(lines) if start_has in l)
    i1 = next(i for i in range(i0 + 1, len(lines)) if end_has in lines[i])
    if not include_end:
        i1 -= 1
    i1 = min(i1, i0 + max_lines)
    return '\n'.join('%4d  %s' % (k + 1, lines[k]) for k in range(i0, i1 + 1))


def rows_with(rel, needles):
    return [l for l in rd(rel).split('\n') if any(n in l for n in needles)]


miss = [r for r in A['quality_post'] if r.get('missing')]
okp = [r for r in A['quality_post'] if not r.get('missing')]
sel = [r for r in G['quality_floor_rows'] if float(r.get('layer')) == 0.5 and float(r.get('coef')) == 2.0]
conf = A['confirm'] if isinstance(A['confirm'], list) else list(A['confirm'].values())
tags = {}
for r in conf:
    k = r.get('tag') or r.get('label')
    tags[k] = tags.get(k, 0) + 1

# ---------------- 依頼文 ----------------
R = []
p = R.append
p('# 意見の伺い: **選定後の品質床の「走行が無い」——凍結した二つの器の食い違いをどう扱うか**（裁定 D151 の候補・%s 日本時間）' % now.strftime('%Y-%m-%d %H:%M'))
p('')
p('- 伺う相手: **Gemini（系統外）**と **claude.ai の Claude（起草者と同一系列）**。登録者（楠見優太）が各位にこの依頼文と資料を渡します。')
p('- 依頼者: 南無弥勒如来（コーディネータ・起草者・器材も合成データも書いた・Claude Fable 5.1）。')
p('- これは設計全体の検分ではなく、**下の一件（と同じ型の穴）だけ**を問う狭い伺いです。claude.ai の票は起草者と同一系列なので系統内の一票に数えます（裁定 D59）。系統外の判定も**プロンプトに依る**ことがこの事業で二度記録されています——称賛も断罪も、それだけでは裁定になりません。**具体の指摘と、その根拠の行**をお願いします。')
p('- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （この束を組んだ時点のコミット %s）。`prelim/` と `results/prelim-*` は開かないでください。' % HEAD)
p('- 段階 B は 2026-09-20 に凍結し、データの生成（同一性選別・調整走行・品質床・本走行 11,800 試行）を終え、2026-09-22 の朝に登録者と一緒に集計を開いたところです。')
p('- **この束には、確証の族の率と p を入れていません。** 下の道の選び方で札がどちらに動くかを、伺う相手には伏せています（起草者は見ています——§2）。構造だけでご判断いただきたいからです。この伏せ方自体が不適切なら、それもご指摘ください。')
p('')
p('## 0. 何が起きたか（不利なことから）')
p('')
p('- 凍結した集計器 `tools/analyze_B.py` %s を走らせると、確証の族 16 対比のうち **8 対比——減算族 4 と加算族 4 の全部——が「%s」**になりました。札の内訳は ' % (A['version'], QF['fail_label']) + '・'.join('%s %d' % (k, v) for k, v in tags.items()) + ' です。')
p('- 理由は、主の介入の腕二本（%s）が、集計器の区画「選定後の品質床」で「**%s**」と数えられたことです。**正答数が下限を割ったのではありません。**' % ('・'.join(r['arm'] for r in miss), miss[0]['note']))
p('- 走行が無いのは、Colab の起動器 `tools/colab/boot_stageB.py` が、選定後の段（post）で**二つの土台の腕を外す**からです（資料 M2）。二腕は選定の段（selection）で、選ばれた層 × 係数の走行が既にあり、そこでは合格しています（資料 M5）。')
p('- 集計器は、介入の腕の一覧を正本から数え上げ、**段が post の走行だけ**を探します（資料 M3）。選定の段の走行は見ません。**凍結した二つの器が食い違っています。**')
p('- **なぜ凍結の前に捕まらなかったか**: 合成データの器 `tools/synth_B.py` は、選定後の段のセルを**全部の介入の腕**に書きます（資料 M4）。だから合成データによる検査（65 経路）・変異（64 件）・端から端までの検査（38 件）のどれも、「起動器が二腕を外す」場合を通っていません。三つとも起草者が書いたもので、同じ思い込みを共有していました。前の巡で四票が挙げた「登録はあるのに器が無い」と同じ系統の、**器と器のあいだの穴**です。')
p('- 集計はここで止めてあります。副位置の読み（`layers_B`）と、**一度だけ**と決めた封印予想の照合は走らせていません。凍結した器の出力は `records/B/analysis-B-2026-09-22.{md,json}` にそのまま残してあります。')
p('')
p('## 1. 伺いたいこと')
p('')
p('### (a) 正本はどちらの器を支持しているか')
p('')
p('正本には、読みようによって向きの違う二つの文があります（どちらも逐語・資料 M1）。')
p('')
p('- `quality_floor.run_order`: 「%s」' % QF['run_order'])
p('- `quality_floor.post_selection`: 「%s」' % QF['post_selection'])
p('')
p('- **読み一（起動器の側）**: (ii) は「**残りの**介入の腕」であり、二つの土台の腕の床は (i) 選定の段の・選ばれた層 × 係数の走行で既に判定されている。集計器が post の走行だけを探すのが誤り。')
p('- **読み二（集計器の側）**: `post_selection` は「**すべての**介入の腕」に当てると言っている。段が違えば無操作の相手も違う（`partner_run`——相手は段 × 土台 × セッションごと）。だから二腕も post の段で走らせるべきで、走らせなかった起動器が誤り——走行は本当に欠けている。')
p('- 起草者は読み一に引かれています（§2）。**読み二のほうが正しい、あるいはどちらとも決まらない、というご判断を歓迎します。**転記行 A（設計事実）は選定後の段を「15 セル」と数えており、これは二腕を外した数です（資料 M6）——ただしこれも起草者が生成器に書いた数です。')
p('')
p('### (b) どの道を採るべきか')
p('')
p('- **甲**: 凍結した集計器の出力をそのまま確証の札とする。8 対比は「%s」のまま報告し、食い違いは限界に書く。二腕の床を選定の段の行で読んだ場合の表は、**札を名乗らない事後の記述**として別に置く。段階 A の逸脱 D-42（資料 M7）が近い型です——凍結の一式の中の食い違いを、器も正本も変えずに報告の区画の外で書いた。' % QF['fail_label'])
p('- **乙**: 逸脱として記帳し（番号・日付・理由・登録者の承認——正本 `deviation.rule`）、集計器を読み一に合わせて直し、走らせ直す。直す前の出力も残し、報告は両方を並べる。')
p('- **丙**: 足りない二セル（二腕 × 選ばれた層 × 係数・各 200 問＋同じセッションの無操作の相手）を今から走らせ、凍結した集計器をそのまま通す。品質床は貪欲復号なので選定の段と同じ正答数になる見込みですが、**率を見た後に作るデータ**です。')
p('- **ほかの道**があればお示しください（たとえば、乙で直した器の札を「確証」と呼ばず別の名で呼ぶ、両方の札を併記して主をどちらにするかを決める、など）。')
p('')
p('### (c) 乙または丙を採る場合、確証としての身分はどうなるか')
p('')
p('- 直す（走らせる）と決めるのは、率と表を見た**後**です。直しの中身が正本の文だけで決まるとしても、**「直す」という決定そのもの**が結果に依っていないと、どこまで言えるでしょうか。')
p('- 報告でどう開示し、どの限界を書き、どの主張を控えるべきか。具体の文案があれば歓迎します。')
p('')
p('### (d) 同じ型の穴がほかに無いか')
p('')
p('- 「**器 X が書く記録の形**」と「**器 Y が読む記録の形**」の食い違いで、合成データが両方に都合よく作られていたために検査を素通りしたもの。資料 M2〜M4 のほか、公開の置き場の `tools/` を見て、同じ型の穴を探していただけると助かります。とくに `gate_B.py`（選定の段を読む）・`analyze_B.py`・`build_report_B.py`・`layers_B.py`・`compare_predictions_B.py` が読む記録と、`boot_stageB.py`・`run_stageB_local.py` が書く記録のあいだ。')
p('')
p('### (e) 率と p を伏せたこの伺い方は適切か')
p('')
p('- 伏せることで構造の判断が結果から切り離される一方、皆さんは影響の大きさを測れません。不適切ならその旨と、何を開示すべきかをお示しください。')
p('')
p('## 2. 起草者の利益相反（先に書きます）')
p('')
p('- 起草者は、食い違った二つの器と、それを素通りさせた合成データを書いた当人です。')
p('- 起草者は集計の表を見ました。8 対比の p は表に印字されています（Holm の欄は空）。**乙や丙を採ると札がどちらに動くかを、起草者は知ったうえでこの依頼文を書いています。**確証が出る側に引かれています。')
p('- 逆向きの危険（引力を恐れて、正本に照らせば直すべきものを直さない）も同じ較正の失敗です。だから道を甲・乙・丙と並べ、読み二を先に自分で書きました。')
p('- 登録者への起草者の推奨は「乙＋この一件を系統外の目に」でした。**この推奨は起草者の引かれる向きと重なっています。**')
p('')
p('## 3. いま分かっていること（機械の出力・手で打っていません）')
p('')
p('| 何 | 値 |')
p('|---|---|')
p('| 正本 `design/contrasts-B.json` の SHA16 | %s |' % s16('design/contrasts-B.json'))
p('| 集計器 `tools/analyze_B.py` | %s・SHA16 %s |' % (A['version'], s16('tools/analyze_B.py')))
p('| 起動器 `tools/colab/boot_stageB.py` の SHA16 | %s |' % s16('tools/colab/boot_stageB.py'))
p('| 合成データの器 `tools/synth_B.py` の SHA16 | %s |' % s16('tools/synth_B.py'))
p('| 門の記録 `records/B/gate-B-2026-09-21.json` | 判定 %s・選んだ組 層 0.5 × 係数 2.0・SHA16 %s |' % (G.get('verdict'), s16('records/B/gate-B-2026-09-21.json')))
p('| 選定後の段で走った介入の腕 | %d 本・すべて合格（無操作との差 %s pt・下限は %s pt・境目ちょうどは不合格） |' % (len(okp), '・'.join(sorted({'%g' % r['diff_pt'] for r in okp})), QF['threshold_pt']))
p('| 選定後の段に走行が無い介入の腕 | %s |' % '・'.join(r['arm'] for r in miss))
p('| その二腕の、選定の段・選ばれた組での行（門の記録） | ' + '／'.join('%s %s/%s 対 無操作 %s/%s・差 %s pt' % (r.get('arm'), r.get('correct'), r.get('n_ok'), r.get('noop_correct'), r.get('noop_n_ok'), r.get('diff_pt')) for r in sel) + ' |')
p('| 整合検査（率盲検）| 同一性選別 13 セル・調整走行 36 セル・品質床 35 セル・本走行 59 セル——いずれも不整合 0 |')
p('| 事実の記録（裁定の前に書いた） | `records/B/incident-qpost-missing-2026-09-22.md`（資料 M8 に全文） |')
p('')
p('## 4. お答えの形（お願い）')
p('')
p('1. (a)〜(e) それぞれに、**判断**（(a) は 読み一／読み二／決まらない、(b) は 甲／乙／丙／ほか）と、**根拠の行**（資料の記号と行番号、または公開の置き場のファイルと行）。')
p('2. 重大度をつけた所見の一覧（重大／中／軽）。再現のしかたが分かるもの（どのファイルのどの行を見れば確かめられるか）を優先してください。')
p('3. **ご自身が確認していないこと**（読んでいないファイル・走らせていない検査）を必ず一つ以上。')
p('4. 起草者の読みや推奨への同意は、理由が無ければ票として数えません。反対の読みを一度は組み立ててみてください。')
p('')
p('票は逐語で保全し、事実の主張は現物で再現してから採否表で扱います（再現できなかった所見もそのまま記録します）。裁定は登録者のものです。')
p('')
p('本依頼文と資料のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。')
p('')

# ---------------- 資料 ----------------
M = []
m = M.append
m('# 資料（選定後の品質床の「走行が無い」の伺い・機械で切り出したもの）')
m('')
m('## M1. 正本 `design/contrasts-B.json` の該当の登録（逐語）')
m('')
for k in ('run_order', 'post_selection', 'selection_cells', 'partner_run', 'pass_rule', 'fail_rule', 'fail_label', 'unit', 'arms', 'operations', 'threshold_pt', 'boundary_rule'):
    m('- `quality_floor.%s`: %s' % (k, json.dumps(QF[k], ensure_ascii=False)))
for k in ('D69', 'D77', 'D88', 'D92', 'D106', 'D126'):
    m('- `decisions.%s`: %s' % (k, json.dumps(T['decisions'].get(k), ensure_ascii=False)))
for k in ('rule', 'silent_fix', 'scope'):
    m('- `deviation.%s`: %s' % (k, json.dumps(T['deviation'][k], ensure_ascii=False)))
m('- `selection.binding`: %s' % json.dumps(T['selection'].get('binding'), ensure_ascii=False))
m('- `arms.main`（本走行の腕）: %s' % json.dumps(T['arms']['main'], ensure_ascii=False))
m('')
m('## M2. 起動器 `tools/colab/boot_stageB.py`（SHA16 %s）——品質床の相の計画' % s16('tools/colab/boot_stageB.py'))
m('')
m('```python')
m(excerpt('tools/colab/boot_stageB.py', "_QF = T['quality_floor']", "'extra': {'stage': STAGE, 'arm': a, 'layer': _l, 'coef': _c}})"))
m('```')
m('')
m('## M3. 集計器 `tools/analyze_B.py`（SHA16 %s）——選定後の品質床の読み' % s16('tools/analyze_B.py'))
m('')
m('```python')
m(excerpt('tools/analyze_B.py', '# ---- 選定後の品質床（裁定 D77）: 落ちた腕 ----', "'diff_pt': round(d_pt, 3), 'pass': ok", max_lines=80))
m('```')
m('')
m('## M4. 合成データの器 `tools/synth_B.py`（SHA16 %s）——選定後の段のセルの書き方' % s16('tools/synth_B.py'))
m('')
m('```python')
m(excerpt('tools/synth_B.py', "INTERV = sorted(a for a in T['arms']['main']", 'NOOP_BASE = {a:'))
m('...')
_sl = rd('tools/synth_B.py').split('\n')
_i = next(i for i, l in enumerate(_sl) if "run_key='%s__post__%s' % (tag_q, arm))" in l)
m('\n'.join('%4d  %s' % (k + 1, _sl[k]) for k in range(_i - 6, _i + 8)))
m('```')
m('')
m('## M5. 記録の行（品質床の正答数——**本走行の率ではない**）')
m('')
m('門の記録 `records/B/gate-B-2026-09-21.json` の、選ばれた組（層 0.5 × 係数 2.0）の選定の段の行:')
m('')
m('```json')
m(json.dumps(sel, ensure_ascii=False, indent=1))
m('```')
m('')
m('集計の記録 `records/B/analysis-B-2026-09-22.json` の `quality_post`（選定後の段・全行）:')
m('')
m('```json')
m(json.dumps(A['quality_post'], ensure_ascii=False, indent=1))
m('```')
m('')
m('## M6. 段取りと設計事実の該当の行')
m('')
for l in rows_with('records/B/run-plan-B.md', ['| quality |', '| 4 | 品質床', '| 5 | 門1', '| 6 | 品質床']):
    m('- `records/B/run-plan-B.md`: %s' % l)
for l in rows_with('records/B/design-facts-B.md', ['**転記行 A**']):
    m('- `records/B/design-facts-B.md`: %s' % l[:700])
m('')
m('## M7. 先例——段階 A の逸脱台帳 `records/DEVIATIONS.md` の行（逐語）')
m('')
for l in rows_with('records/DEVIATIONS.md', ['| D-40 |', '| D-41 |', '| D-42 |']):
    m(l)
    m('')
m('## M8. 事実の記録 `records/B/incident-qpost-missing-2026-09-22.md`（全文・裁定の前に書いた）')
m('')
m(rd('records/B/incident-qpost-missing-2026-09-22.md'))
m('')

open(os.path.join(HERE, 'request-qpost.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(R))
open(os.path.join(HERE, 'materials-qpost.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(M))
allin = '\n'.join(R) + '\n\n---\n\n' + '\n'.join(M)
open(os.path.join(HERE, 'all-in-one.md'), 'w', encoding='utf-8', newline='\n').write(allin)
idx = ['# 束の索引（機械生成・%s 日本時間・コミット %s）' % (now.strftime('%Y-%m-%d %H:%M'), HEAD), '',
       '| ファイル | 字数 | SHA16 |', '|---|---|---|']
for f in ('request-qpost.md', 'materials-qpost.md', 'all-in-one.md'):
    t = open(os.path.join(HERE, f), encoding='utf-8').read()
    idx.append('| `%s` | %d | %s |' % (f, len(t), hashlib.sha256(t.encode('utf-8')).hexdigest().upper()[:16]))
idx += ['', '- 渡し方: `all-in-one.md` を一通で貼る（依頼文＋資料）。入らなければ `request-qpost.md` → `materials-qpost.md` の順に二通。',
        '- **確証の族の率と p は入れていない**（伺う相手には札の動く向きを伏せる）。', '']
open(os.path.join(HERE, 'bundle-index.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(idx))
print('\n'.join(idx))
# 伏せの確かめ: 束に、確証の族の p や pt 差の値が入っていないこと
leak = []
for r in conf:
    for key in ('p', 'diff_pt', 'pt'):
        v = r.get(key)
        if isinstance(v, float) and abs(v) > 0 and ('%g' % v) in allin and len('%g' % v) >= 5:
            leak.append((r.get('id') or r.get('contrast'), key, v))
print('leak check (values of the confirmatory table found in the bundle):', leak)
