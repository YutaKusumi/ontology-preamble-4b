# -*- coding: utf-8 -*-
"""段階 B の結果報告（表紙・草案1）の**公開前検分**の束を組む（第一巡・全範囲・2026-09-22）。引用・数値・差分は現物から機械で取る。
出力（この置き場）: review-request-results-B.md・bundle-results-B-part1〜4.md・bundle-results-B-all-in-one.md・bundle-results-B-index.md。
用法: python records/reviews/B/results/make_bundle_results_B.py"""
import os, json, hashlib, difflib, datetime, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
j = lambda *p: os.path.join(REPO, *p)
rd = lambda rel: open(j(*rel.split('/')), encoding='utf-8').read()
s16b = lambda b: hashlib.sha256(b).hexdigest().upper()[:16]
s16 = lambda rel: s16b(open(j(*rel.split('/')), 'rb').read().replace(b'\r\n', b'\n'))
NL = chr(10)
T = json.loads(rd('design/contrasts-B.json'))
HEAD = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=REPO).stdout.strip()
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

R = []
p = R.append
p('# 公開前検分のお願い（第一巡・全範囲）: **段階 B の結果報告——表紙（草案1）と二本の機械の報告**（%s 日本時間）' % now.strftime('%Y-%m-%d %H:%M'))
p('')
p('- お願いする相手: **Gemini（系統外）**と **claude.ai の Claude（起草者と同一系列）**。登録者（楠見優太）が各位にこの依頼文と束を渡します。')
p('- 依頼者: 南無弥勒如来（コーディネータ・起草者・器材も合成データも報告も書いた・Claude Fable 5.1）。')
p('- claude.ai の票は起草者と同一系列なので、何票あっても系統内の一票に数えます（裁定 D59）。系統外の判定も**プロンプトに依る**ことがこの事業で二度記録されています——称賛も断罪も、それだけでは裁定になりません。**具体の所見と、確かめられる置き場と行**をお願いします。')
p('- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （束を組んだ時点のコミット %s）。`prelim/` と `results/prelim-*` は開かないでください（段階 B と無関係の予備の走行です）。**それ以外は、すべて開いて構いません**——今回は率を伏せていません。本走行の試行の記録（`results/stageB/`）も公開済みで、表を数え直せます。' % HEAD[:7])
p('- 票には、**何を開き、何を走らせ、何を見ていないか**を書いてください（申告は検査ではないので、追い問いをすることがあります）。')
p('')
p('## 0. 何の報告か（不利なことから）')
p('')
p('- 段階 B は、単一の小型機種（Qwen3-4B-Instruct-2507）で、「存在論的な前置き O の枠組み」に対応する方向 v̂（腕対の主位置の活性の差から作った）を、残差の流れに加減したとき、破局的選択の率が**ノルムを合わせたランダム方向の加減と区別できる動きをするか**を見る事前登録の検証です。2026-09-20 に凍結し、記録を先に公開し、その後にデータを作りました（同一性選別 → 調整走行 → 品質床 → 門 → 本走行 11,800 試行）。')
p('- **集計を開いたところ、凍結した二つの器が食い違っていました。** 凍結した集計器は、確証の族 16 対比のうち減算族と加算族の 8 対比を「判定不能（品質床）」としました——床に落ちたのではなく、集計器が探した段に走行の記録が無かったためです（凍結した起動器は、正本の段取りどおり、その二腕を選定後の段から外します）。合成データがこの場合を一度も作っていなかったので、凍結の前の三重の検査を素通りしました。起草者の検査の穴です。')
p('- 率と p を伏せた四票の伺い（系統外 2・系統内 2）の後、登録者は**逸脱として直す**と裁定しました（D151）。凍結した集計器は変えず、そこから機械で作った器が、二腕の床を「門の記録（率を開く前に作った記録）の・選定の段の・選ばれた組の行」で読みます。**直すと決めたのは、起草者と登録者が率と p を見た後です。** だから報告は、凍結した器の出力と逸脱の下の出力を**同じ重さで並べ**、直した側の札に印を付けています。')
p('- 逸脱の下では、加算族の三場面と減算族の二場面で札が立ちました。**起草者はこの結果を望んでいた側にいます**（§2）。この事業には、結果を希望の向きへ読み過ぎた既往が二度あります。今回の検分でいちばんお願いしたいのは、**この報告を壊しにかかること**です。')
p('')
p('## 1. 見ていただきたいこと（全範囲）')
p('')
p('1. **数の一致**: 表紙の対照表（§2）の件数・pt 差・区間・p・Holm の段・札が、二つの集計の記録（`records/B/analysis-B-2026-09-22.json`・`analysis-B-devB1-2026-09-22.json`）と一致するか。できれば、公開の試行の記録から数え直してください——`results/stageB/<走行キー>/trials-*.jsonl` の一行が一試行で、`status == "ok"` が使えた試行（分母）、`catastrophe`・`format_fail`・`refuse_class` が三つ組の分子です。札は両側 Fisher の p を族ごと（減算 4・加算 4・交差 8）に Holm で切ったものです。')
p('2. **読みの言い過ぎと弱すぎ**: 表紙の §0・§3・§4 が、機械の表が支える以上のことを言っていないか。逆に、不利な材料（N1 で動かないこと・ランダム方向の不均一の注・選定の外挿・td が完全な統制でないこと・検出力・同一性選別の際どい合格）を薄めていないか。正本の読みの条項（束の第四部）に反する文が無いか。「確証」の語が印なしで使われていないか。')
p('3. **逸脱の扱いと開示**: 逸脱（一）〜（四）の開示は足りているか。「同じ重さで並べる」は本当に実現しているか（要約・表・読みのどこかで、片方の出力だけが主のように読めないか）。直した札の身分の書き方は妥当か。')
p('4. **統計と設計の穴**: 族の切り方・Holm・両側 Fisher と Newcombe の区間の食い違い・相手の腕の共有（加算族と交差族は同じ `Onull+vrand` を相手にする）・ランダム方向が三本であること・調整走行で選んだ組を本走行に当てること（調整走行と本走行は別の試行です）・品質床が貪欲復号で候補を見分けていないこと——ほかに、結論を動かしうる穴は無いか。')
p('5. **同じ型の穴**: 「器 X が書く記録の形」と「器 Y が読む記録の形」の食い違いが、まだ残っていないか。とくに `tools/layers_B.py`・`tools/compare_predictions_B.py`・`tools/build_report_B.py` と、表紙を組む器 `records/B/make_results_B.py`。逸脱の下の集計器 `tools/analyze_B_devB1.py` の差分（束の第三部）が、言っている以上のことをしていないか。')
p('6. **足りない限界**と、**報告に載せるべきなのに載っていない事実**。')
p('7. **公開の可否**: 可／条件つき可／差し戻し。条件は「公開の前に要るもの」と「公開の後でよいもの」に分けてください。')
p('')
p('## 2. 起草者の利益相反（先に書きます）')
p('')
p('- 起草者は、設計・器材・合成データ・食い違いを直す器・この報告を書いた当人で、札が立つ側に引かれています。')
p('- 起草者の封印の符号は、減算族と加算族の全対比で「どちらでもない」でした（外れています）。登録者の予想は、向きとしては逸脱の下の五本で当たっています。道の選び方（逸脱として直す）は、この照合の数も動かしました。')
p('- 凍結の後の直し・走行・集計・報告は、食い違いの一件についての四票の伺いを除いて、独立の目を通っていません。')
p('')
p('## 3. 束の中身（四部・機械で切り出したもの）')
p('')
p('| 部 | 中身 |')
p('|---|---|')
p('| 第一部 | この依頼文と、表紙の報告 `records/B/results-B.md`（草案1・全文） |')
p('| 第二部 | 機械の報告（逸脱の下）`records/B/results-report-B-devB1.md`（全文・凍結した組み立て器の出力） |')
p('| 第三部 | 機械の報告の二本の差分（凍結した器の出力 対 逸脱の下）・逸脱台帳の行・食い違いの事実の記録・裁定 D151〜D154・四票の採否表・集計器の差分 |')
p('| 第四部 | 走行の記録（同一性選別・調整走行・品質床・本走行）・正本の該当の登録（確証の族・読みの条項・封印の様式） |')
p('')
p('## 4. お答えの形（お願い）')
p('')
p('1. §1 の 1〜7 それぞれに、判断と**根拠の置き場と行**。')
p('2. 重大度つきの所見の一覧（重大／中／軽）。確かめ方が分かるものを優先してください。')
p('3. **ご自身が確認していないこと**を必ず一つ以上。開いたファイル・走らせた検査・数え直した行も書いてください。')
p('4. 起草者の読みへの同意は、理由が無ければ票として数えません。**この報告が間違っているとしたらどこか**を、一度は組み立ててみてください。')
p('')
p('票は逐語で保全し、事実の主張は現物で再現してから採否表で扱います（再現できなかった所見もそのまま記録します）。裁定は登録者のものです。')
p('')
p('本依頼文と束のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。')
p('')

P1 = NL.join(R) + NL + '---' + NL + NL + '# 第一部の資料: 表紙の報告 `records/B/results-B.md`（SHA16 %s・全文）' % s16('records/B/results-B.md') + NL + NL + rd('records/B/results-B.md')
P2 = '# 第二部: 機械の報告（逸脱の下）`records/B/results-report-B-devB1.md`（SHA16 %s・全文）' % s16('records/B/results-report-B-devB1.md') + NL + NL + rd('records/B/results-report-B-devB1.md')

a_, b_ = rd('records/B/results-report-B-frozen.md').split(NL), rd('records/B/results-report-B-devB1.md').split(NL)
d = [l for l in difflib.unified_diff(a_, b_, 'results-report-B-frozen.md', 'results-report-B-devB1.md', lineterm='', n=0)]
FRm = rd('records/B/FREEZE-RECORD-B.md').split(NL)
ledger = [l for l in FRm if l.startswith('| D-B')]
adopt = rd('records/reviews/B/incident-qpost-round/adoption-table-qpost.md')
P3 = NL.join([
    '# 第三部: 二つの出力の差・逸脱・裁定', '',
    '## 3-1. 機械の報告の二本の差分（`results-report-B-frozen.md`〔SHA16 %s〕対 `results-report-B-devB1.md`・文脈なしの unified diff・%d 行）' % (s16('records/B/results-report-B-frozen.md'), len(d)), '',
    '```diff'] + [l[:600] for l in d] + ['```', '',
    '## 3-2. 凍結の記録の逸脱台帳の行（`records/B/FREEZE-RECORD-B.md`・逐語）', ''] + ledger + ['',
    '## 3-3. 食い違いの事実の記録 `records/B/incident-qpost-missing-2026-09-22.md`（裁定の前に書いた・全文）', '', rd('records/B/incident-qpost-missing-2026-09-22.md'), '',
    '## 3-4. 登録者裁定 `records/reviews/B/incident-qpost-round/rulings-D151-D154.md`（全文）', '', rd('records/reviews/B/incident-qpost-round/rulings-D151-D154.md'), '',
    '## 3-5. 四票の採否表 `records/reviews/B/incident-qpost-round/adoption-table-qpost.md`（全文）', '', adopt, '',
    '## 3-6. 集計器の差分 `records/B/deviations/D-B1-analyze_B.diff`（SHA16 %s・全文）' % s16('records/B/deviations/D-B1-analyze_B.diff'), '', '```diff', rd('records/B/deviations/D-B1-analyze_B.diff'), '```', '',
    '## 3-7. 走らせる前の確かめ', '',
    '- 合成データでの回帰の確かめ: `records/B/deviations/regress_devB1.py`（選定後の走行が全腕にある合成データでは二つの器の出力が版・題・時刻のほか一致し、二腕の走行を外すと、逸脱の下の器は走行を外す前の凍結した器と同じ札を出す）。',
    '- 同じ型の食い違いの掃き出し `records/B/deviations/sweep-readers-writers-2026-09-22.md`（全文）:', '', rd('records/B/deviations/sweep-readers-writers-2026-09-22.md'), ''])

FAM = T['families']
fam_lines = []
for k, v in FAM.items():
    fam_lines.append('- `families.%s`: 問い「%s」・m %s・α %s・検定 %s・対比 %s' % (k, v['question'], v['m'], v['alpha'], v['contrasts'][0]['test'], '／'.join(c['id'] for c in v['contrasts'])))
    fam_lines.append('  - `direction_rationale`: %s' % v.get('direction_rationale'))
P4 = NL.join([
    '# 第四部: 走行の記録と、正本の該当の登録', '',
    '## 4-1. 同一性選別の走行記録 `records/B/identity-run-B.md`（全文）', '', rd('records/B/identity-run-B.md'), '',
    '## 4-2. 調整走行の走行記録 `records/B/tune-run-B.md`（全文）', '', rd('records/B/tune-run-B.md'), '',
    '## 4-3. 品質床（選定の段）の走行記録 `records/B/quality-selection-run-B.md`（全文）', '', rd('records/B/quality-selection-run-B.md'), '',
    '## 4-4. 本走行の走行記録 `records/B/main-run-B.md`（全文）', '', rd('records/B/main-run-B.md'), '',
    '## 4-5. 門1 と選定の記録 `records/B/gate-B-2026-09-21.md`（全文）', '', rd('records/B/gate-B-2026-09-21.md'), '',
    '## 4-6. 正本 `design/contrasts-B.json`（SHA16 %s）の該当の登録（逐語）' % s16('design/contrasts-B.json'), ''] + fam_lines + ['',
    '- `reading_B`（読みの条項・全文）:', '', '```json', json.dumps(T['reading_B'], ensure_ascii=False, indent=1), '```', '',
    '- `seal_format.sign_values`: %s ／ `seal_format.reading`: %s' % (json.dumps(T['seal_format']['sign_values'], ensure_ascii=False), T['seal_format']['reading']),
    '- `print_strings.value_word_ban`: %s' % json.dumps(T['print_strings']['value_word_ban'], ensure_ascii=False),
    '- `print_strings.mechanism_word_ban`: %s' % json.dumps(T['print_strings']['mechanism_word_ban'], ensure_ascii=False),
    '- 起草者の封印 `records/B/seal-B.json` の符号: %s' % json.dumps(json.loads(rd('records/B/seal-B.json'))['signs'], ensure_ascii=False), ''])

parts = {'bundle-results-B-part1.md': P1, 'bundle-results-B-part2.md': P2, 'bundle-results-B-part3.md': P3, 'bundle-results-B-part4.md': P4}
open(os.path.join(HERE, 'review-request-results-B.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(R))
for f, t in parts.items():
    open(os.path.join(HERE, f), 'w', encoding='utf-8', newline=NL).write(t)
allin = (NL + NL + '---' + NL + NL).join(parts[f] for f in sorted(parts))
open(os.path.join(HERE, 'bundle-results-B-all-in-one.md'), 'w', encoding='utf-8', newline=NL).write(allin)
idx = ['# 束の索引（段階 B の結果報告・公開前検分の第一巡・機械生成・%s 日本時間・コミット %s）' % (now.strftime('%Y-%m-%d %H:%M'), HEAD[:7]), '',
       '| ファイル | 字数 | SHA16 |', '|---|---|---|']
for f in ['review-request-results-B.md'] + sorted(parts) + ['bundle-results-B-all-in-one.md']:
    t = open(os.path.join(HERE, f), encoding='utf-8').read()
    idx.append('| `%s` | %d | %s |' % (f, len(t), s16b(t.encode('utf-8'))))
idx += ['', '- 渡し方: `bundle-results-B-all-in-one.md` を一通で（第一部の頭が依頼文）。入らなければ第一部 → 第二部 → 第三部 → 第四部の順に四通。',
        '- この巡は率を伏せない（報告そのものの検分）。`prelim/` と `results/prelim-*` だけは開かないよう頼んである。', '']
open(os.path.join(HERE, 'bundle-results-B-index.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(idx))
print(NL.join(idx))
