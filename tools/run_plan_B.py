# -*- coding: utf-8 -*-
"""run_plan_B.py v1 —— 段階 B の**走行の段取り**（`records/B/run-plan-B.md`）を、正本と設計事実から機械で組む（2026-09-20・凍結前の見直しの (あ)）。

なぜ: 段階 A は走らせる前に段取り（`records/A/main/main-plan-A.md`）を書いた——相の順・tag・試行数・seed・セッションの割り方・
      相の間に何を確かめるか・中断と再開・止める規則。B にはこれが無く、開示に「相の間は人手で進める」とだけあった。
      登録者の方針（本試行で困ったり慌てたりしないように、いま手当てできることは手当てする）に沿って置く。
数は正本 `design/contrasts-B.json` と設計事実 `records/B/design-facts-B.json` から読む（手で打たない）。
凍結のコミットは凍結の後に分かるので、その行だけ置き字にし、凍結の記帳の後に `--commit` で埋め直す。
用法: python tools/run_plan_B.py [--commit <凍結のコミット>] [--force]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
FACTS = runs_B.read_json(os.path.join(REPO, 'records', 'B', 'design-facts-B.json'))
FA = FACTS['facts']['A']['data']
FF = FACTS['facts']['F']['data']
fmt = lambda x: format(x, ',')
S = T['identity_screen']
TU = T['selection']['tune']
QF = T['quality_floor']
TAGS = T['tags']

ap = argparse.ArgumentParser()
ap.add_argument('--commit', default=None, help='凍結のコミットの短い名（凍結の後に埋める）')
ap.add_argument('--out', default=os.path.join(REPO, 'records', 'B', 'run-plan-B.md'))
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
if os.path.exists(a.out) and not a.force:
    sys.exit('既にある（--force で置き換え）: %s' % a.out)
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

q_sel = QF['selection_cells'] + len(QF['arms'])
q_post = FA['quality_cells'] - q_sel
n_id, n_tune, n_main, n_q = FA['identity'], FA['tune'], FA['main'], FA['quality']
rows = [(TAGS['identity'], 'identity', '同一性選別（transformers・%d 腕 × N1 × n=%d）' % (S['arms'], S['n']), n_id),
        (TAGS['tune'], 'tune', '調整走行（%d 候補 × %d 腕 × n=%d × 抽出場面 %d）' % (T['selection']['candidates']['count'], len(TU['arms']), T['n_tune'], len(TU['scenarios'])), n_tune),
        (TAGS['quality'] + '（OP4B_STAGE=selection）', 'quality', '品質床・選定の段（%d セル × %d 問）' % (q_sel, QF['items']), q_sel * QF['items']),
        (TAGS['quality'] + '（OP4B_STAGE=post）', 'quality', '品質床・選定後の段（%d セル × %d 問・門の記録が選んだ層 × 係数）' % (q_post, QF['items']), q_post * QF['items']),
        (TAGS['main'], 'main', '本走行（%d セル × n=%d・門の記録が選んだ層 × 係数）' % (len(T['main_cells']), T['n_main']), n_main)]
assert sum(r[3] for r in rows) == FA['total'], (sum(r[3] for r in rows), FA['total'])
commit = a.commit or '**（凍結の後に、凍結のコミットの短い名をここに埋める——`tools/run_plan_B.py --commit … --force`）**'

L = []
p = L.append
p('# 段階 B 走行の段取り（走らせる前・%s 日本時間・コーディネータ）' % jst.strftime('%Y-%m-%d %H:%M'))
p('')
p('- 性格: 正本 `procedure` の相を、Colab の起動器 `tools/colab/boot_stageB.py` で**一相ずつ**走らせ、相の間に手元の器で確かめて登録者の確認を挟む段取り。'
  '数は正本（SHA16 %s）と設計事実（`records/B/design-facts-B.json`）から機械で組んだ。' % runs_B.sha16_file(runs_B.CPATH))
p('- 書いた人: コーディネータ（南無弥勒如来・**Claude Fable 5.1**〔この段取りを書いた時点の機種〕）。Colab は登録者の Chrome 越しにコーディネータが操作し、'
  'ランタイムの選択と結果の zip の取り出しもコーディネータが行う。**Drive の同意・プラン・支払いだけ登録者**。')
p('- **起動の固定のコミット**: %s。凍結の記録（`records/B/FREEZE-RECORD-B.json`）があれば、起動器は正本・器材・持ち越しの SHA16 を現物と照らして違えば止まる（起動器 v5）。' % commit)
p('- **凍結物を変えない。** 走らせる途中で直したくなったものは、逸脱として番号・日付・理由・登録者の承認を凍結の記録に記帳してから直す（正本 `deviation.rule`）。')
p('')
p('## 1. 走らせる量（正本の登録から機械で組む）')
p('')
p('| 相 | tag | 中身 | 試行 |')
p('|---|---|---|---|')
for tag, ph, what, n in rows:
    p('| %s | `%s` | %s | %s |' % (ph, tag, what, fmt(n)))
p('')
p('- 合計 **%s 試行**（転記行 A）。バッチ %d で ≈%s ユニットの見込み（転記行 F・比例の見込み・実測は調整走行の最初のセッションで取る）。'
  % (fmt(FA['total']), FF['batch'], fmt(round(FF['units_batch']))))
p('- seed は正本 `seeds`（同一性選別 %d・調整走行 %s・本走行 %s・品質床 %d・ランダム方向 %s）。試行の記録の seed は**バッチの種**（裁定 D127）。'
  % (T['seeds']['identity_transformers'], json.dumps(T['seeds']['tune']), json.dumps(T['seeds']['main']), T['seeds']['quality'], json.dumps(T['seeds']['random_dirs'])))
p('- 方向は**凍らせた v̂**（`results/dirB/dirB__s1/directions.npz`・SHA-256 は凍結の値）。介入のある相は読んで照らし、違えば止まる。')
p('')
p('## 2. 相の順と、相の間に確かめること（正本 `procedure`・同一性選別の判定は裁定 D150）')
p('')
p('| 段 | すること | 器 | 確かめること・進む条件 |')
p('|---|---|---|---|')
p('| 1 | 同一性選別を走らせる | 起動器 `OP4B_PHASE=identity` | zip を回収し、整合検査 `python tools/integrity_B.py --tag %s` が**不整合 0** |' % TAGS['identity'])
p('| 2 | 同一性選別を判定する | `python tools/identity_screen_B.py` | 番人（採点欠落・欄・重複・種）を通り、`records/B/identity-screen-B.{json,md}` が書ける。**合否は進む条件ではない**（`fail_reading`）。判定は登録者に見せる |')
p('| 3 | 調整走行を走らせる | 起動器 `OP4B_PHASE=tune` | 起動器は判定の記録が無ければ始めない。zip を回収し、整合検査 `--tag %s` が不整合 0。**率盲検の抽出検査** `python tools/sample_inspection_B.py --tag %s --keydir <公開の外>` を先に通す（対応表は公開の置き場の外） |' % (TAGS['tune'], TAGS['tune']))
p('| 4 | 品質床（選定の段） | 起動器 `OP4B_PHASE=quality OP4B_STAGE=selection` | zip を回収し、整合検査 `--tag %s` が不整合 0 |' % TAGS['quality'])
p('| 5 | 門1 と選定 | `python tools/gate_B.py` | 判定 open なら選んだ層 × 係数と同値の帯を**登録者に見せる**。closed／escalate（全候補が非正など）なら止めて登録者に上げる（正本 `withdrawal`） |')
p('| 6 | 品質床（選定後の段） | 起動器 `OP4B_PHASE=quality OP4B_STAGE=post` | 選んだ層 × 係数でしか走らない（正本 `selection.binding`）。整合検査が不整合 0・`gate_B` を再度通して post の行を得る |')
p('| 7 | 本走行 | 起動器 `OP4B_PHASE=main` | 選んだ層 × 係数でしか走らない。**本走行の率は整合検査まで見ない**（率盲検） |')
p('| 8 | 率盲検の整合検査・抽出検査 | `integrity_B --tag %s`・`sample_inspection_B --tag %s` | 不整合 0・標本の目視と対応表の照合 |' % (TAGS['main'], TAGS['main']))
p('| 9 | 集計 | `control_chart_B` → `analyze_B --gate … --seal records/B/seal-B.json --chart …` → `layers_B` → `compare_predictions_B` | 集計器は門の記録の正本 SHA16 を照らして止まる。予想の照合は**一度だけ** |')
p('| 10 | 報告 | `build_report_B --identity records/B/identity-screen-B.json … --lint` | 走査器が違反 0・漢数字の一覧を読み手が照らす・`block_rebuild`（走らせ直して一字一句で突き合わせる） |')
p('| 11 | 検分 → 公開 → 反映メモ B | — | 登録者の判断 |')
p('')
p('- 相の間は**必ず手元に回収して確かめてから**次へ進む。起動器は書き終えたセルを飛ばすので、中断からの再開は同じ相をもう一度起動すればよい（セッション番号は正本 `sessions.number_rule`）。')
p('')
p('## 3. 起動の一行（Colab のセルに打つのは一行だけ・先頭の下線は入力の先頭が落ちる事故の緩衝）')
p('')
p('```')
p('______________________________=0;import os,urllib.request as u;os.environ.update(OP4B_PHASE="identity",OP4B_COMMIT="<凍結のコミット 40 桁>");exec(u.urlopen("https://raw.githubusercontent.com/YutaKusumi/ontology-preamble-4b/<同じコミット>/tools/colab/boot_stageB.py").read().decode())')
p('```')
p('')
p('- 相ごとに `OP4B_PHASE` を変える（`identity`・`tune`・`quality`・`main`）。品質床は `OP4B_STAGE`（`selection`／`post`）も付ける。')
p('- HF の秘密のポップアップは**キャンセル**（公開の重み）。Drive の同意は登録者。')
p('- 一相ごとに zip を取り出し（名と大きさを申告）、手元の `results/<tag>/` に置いて SHA を照らす。品質床の生テキストは公開の置き場に入れない（`.gitignore`・裁定 D146）。')
p('')
p('## 4. 見込みと止める規則')
p('')
p('- 費用: ≈%s ユニット（バッチ %d・比例の見込み）。**見込みの %s 倍を超えたら登録者の再裁定**（正本 `cost.stop_rule`）。' % (fmt(round(FF['units_batch'])), FF['batch'], FF['stop_ratio']))
p('- 撤退（正本 `withdrawal`・時機は「%s」）: %s。帰結: %s' % (T['withdrawal']['when'], '／'.join(T['withdrawal']['conditions']), T['withdrawal']['consequence']))
p('- %s' % T['withdrawal']['not_a_direction_test'])
p('- 決定性 (i) の不一致・重みの版が解けない・GPU が登録の環境に無い・自己検査が落ちる——起動器が止める（正本 `activation_storage.pre_freeze_run.stops` と同じ条）。')
p('')
p('## 5. 率盲検の外の経路（本走行の前に起草者の目に入る率・開示）')
p('')
p('- 同一性選別の三スタックの距離／調整走行の率（選定に要る）／品質床の得点／整合検査が印字する書式外の件数（裁定 D97）。**本走行の率は整合検査まで見ない。**')
p('')
p('## 6. 予想（走らせる前・信頼度つき・外れても消さない）')
p('')
p('| 何 | 予想 | 信頼度 |')
p('|---|---|---|')
p('| 同一性選別の主判定 | 合格（transformers 対 API の平均 %s pt 以内・最大 %s pt 以内） | 中 |' % (S['metric_mean_pt'], S['metric_max_pt']))
p('| 門1 | 開く（品質床に合格する候補が一つ以上） | 中 |')
p('| 全候補が非正（撤退） | 起きない | 中〜低（‖v̂‖／‖h‖ が小さい層があり、効かない域に入りうる） |')
p('| 費用 | 見込みの %s 倍の内側 | 中 |' % FF['stop_ratio'])
p('| 逸脱 | 一件も要らない | 低（段階 A は凍結の後に十二件あった） |')
p('')
p('## 7. COI（事実のみ）')
p('')
p('- 起草者は設計と器材を書き、四条を決め、直した当人である。門1 が開き、確証が出る側に引かれている。率盲検と、判定を機械の区画に貼る型がその引力に逆らう。')
p('')
p('## 8. 本記録が確認していないこと')
p('')
p('- **実重みでの各相の挙動**（時間・メモリ・書式外の率）。見込みは比例で、実測は調整走行の最初のセッションで取る。')
p('- Colab の側の事故（切断・割当・版の更新）。')
p('- この段取り自体は独立の目を通っていない。')
p('')
p('## 検分票')
p('')
p('- 対象: 段階 B の走行の段取り（相の順・量・確かめること・止める規則）。')
p('- 段階: 事前登録あり（走らせる前に書いた）。')
p('- 凍結物の同定: 正本 SHA16 %s・凍らせた v̂・凍結の記録（凍結の後に記帳）。' % runs_B.sha16_file(runs_B.CPATH))
p('- 盲検の状態: 本走行の率は整合検査まで見ない（率盲検）。調整走行と品質床の率は選定に要るので見る（開示済み）。')
p('- 敵対的検分: 数はすべて正本と設計事実から機械で組み、合計が転記行 A と一致することを器が確かめる。')
p('- 系統の内訳: Claude 系 1 巡（起草者）。')
p('- COI記録: §7。')
p('- 判定: 登録者裁定要（走らせる前に一読していただく）。')
p('- 本検分が確認していないこと: §8。')
p('')
p('本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。')
p('')
open(a.out, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[run_plan_B] %s（%d 行・合計 %s 試行・≈%s ユニット）' % (os.path.relpath(a.out, REPO), len(L), fmt(FA['total']), fmt(round(FF['units_batch']))))
