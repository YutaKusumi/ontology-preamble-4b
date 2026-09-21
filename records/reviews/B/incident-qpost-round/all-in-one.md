# 意見の伺い: **選定後の品質床の「走行が無い」——凍結した二つの器の食い違いをどう扱うか**（裁定 D151 の候補・2026-09-22 05:22 日本時間）

- 伺う相手: **Gemini（系統外）**と **claude.ai の Claude（起草者と同一系列）**。登録者（楠見優太）が各位にこの依頼文と資料を渡します。
- 依頼者: 南無弥勒如来（コーディネータ・起草者・器材も合成データも書いた・Claude Fable 5.1）。
- これは設計全体の検分ではなく、**下の一件（と同じ型の穴）だけ**を問う狭い伺いです。claude.ai の票は起草者と同一系列なので系統内の一票に数えます（裁定 D59）。系統外の判定も**プロンプトに依る**ことがこの事業で二度記録されています——称賛も断罪も、それだけでは裁定になりません。**具体の指摘と、その根拠の行**をお願いします。
- 公開の置き場: https://github.com/YutaKusumi/ontology-preamble-4b （この束を組んだ時点のコミット 3ce97ca）。`prelim/` と `results/prelim-*` は開かないでください。
- 段階 B は 2026-09-20 に凍結し、データの生成（同一性選別・調整走行・品質床・本走行 11,800 試行）を終え、2026-09-22 の朝に登録者と一緒に集計を開いたところです。
- **この束には、確証の族の率と p を入れていません。** 下の道の選び方で札がどちらに動くかを、伺う相手には伏せています（起草者は見ています——§2）。構造だけでご判断いただきたいからです。この伏せ方自体が不適切なら、それもご指摘ください。

## 0. 何が起きたか（不利なことから）

- 凍結した集計器 `tools/analyze_B.py` v7 を走らせると、確証の族 16 対比のうち **8 対比——減算族 4 と加算族 4 の全部——が「判定不能（品質床）」**になりました。札の内訳は 判定不能（品質床） 8・非有意 5・確証（登録された向きと逆） 2・判定保留（様式転位） 1 です。
- 理由は、主の介入の腕二本（O-Ncold-v・Onull+v）が、集計器の区画「選定後の品質床」で「**選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）**」と数えられたことです。**正答数が下限を割ったのではありません。**
- 走行が無いのは、Colab の起動器 `tools/colab/boot_stageB.py` が、選定後の段（post）で**二つの土台の腕を外す**からです（資料 M2）。二腕は選定の段（selection）で、選ばれた層 × 係数の走行が既にあり、そこでは合格しています（資料 M5）。
- 集計器は、介入の腕の一覧を正本から数え上げ、**段が post の走行だけ**を探します（資料 M3）。選定の段の走行は見ません。**凍結した二つの器が食い違っています。**
- **なぜ凍結の前に捕まらなかったか**: 合成データの器 `tools/synth_B.py` は、選定後の段のセルを**全部の介入の腕**に書きます（資料 M4）。だから合成データによる検査（65 経路）・変異（64 件）・端から端までの検査（38 件）のどれも、「起動器が二腕を外す」場合を通っていません。三つとも起草者が書いたもので、同じ思い込みを共有していました。前の巡で四票が挙げた「登録はあるのに器が無い」と同じ系統の、**器と器のあいだの穴**です。
- 集計はここで止めてあります。副位置の読み（`layers_B`）と、**一度だけ**と決めた封印予想の照合は走らせていません。凍結した器の出力は `records/B/analysis-B-2026-09-22.{md,json}` にそのまま残してあります。

## 1. 伺いたいこと

### (a) 正本はどちらの器を支持しているか

正本には、読みようによって向きの違う二つの文があります（どちらも逐語・資料 M1）。

- `quality_floor.run_order`: 「品質床は二段に分かれる（裁定 D77・2026-09-18）。(i) 選定の段——候補 × 二つの土台（selection_cells）。(ii) **選定の後・本走行の前**——選ばれた組で、本走行に出る残りの介入の腕。(ii) は本走行の入力になるので、本走行を始める前に判定を終える」
- `quality_floor.post_selection`: 「選ばれた層 × 係数で、本走行に出るすべての介入の腕（ランダム方向・Nk 方向・腕対の差方向・(6b) を含む）に当てる（裁定 D69・2026-09-18）。相手は同じ土台の無操作」

- **読み一（起動器の側）**: (ii) は「**残りの**介入の腕」であり、二つの土台の腕の床は (i) 選定の段の・選ばれた層 × 係数の走行で既に判定されている。集計器が post の走行だけを探すのが誤り。
- **読み二（集計器の側）**: `post_selection` は「**すべての**介入の腕」に当てると言っている。段が違えば無操作の相手も違う（`partner_run`——相手は段 × 土台 × セッションごと）。だから二腕も post の段で走らせるべきで、走らせなかった起動器が誤り——走行は本当に欠けている。
- 起草者は読み一に引かれています（§2）。**読み二のほうが正しい、あるいはどちらとも決まらない、というご判断を歓迎します。**転記行 A（設計事実）は選定後の段を「15 セル」と数えており、これは二腕を外した数です（資料 M6）——ただしこれも起草者が生成器に書いた数です。

### (b) どの道を採るべきか

- **甲**: 凍結した集計器の出力をそのまま確証の札とする。8 対比は「判定不能（品質床）」のまま報告し、食い違いは限界に書く。二腕の床を選定の段の行で読んだ場合の表は、**札を名乗らない事後の記述**として別に置く。段階 A の逸脱 D-42（資料 M7）が近い型です——凍結の一式の中の食い違いを、器も正本も変えずに報告の区画の外で書いた。
- **乙**: 逸脱として記帳し（番号・日付・理由・登録者の承認——正本 `deviation.rule`）、集計器を読み一に合わせて直し、走らせ直す。直す前の出力も残し、報告は両方を並べる。
- **丙**: 足りない二セル（二腕 × 選ばれた層 × 係数・各 200 問＋同じセッションの無操作の相手）を今から走らせ、凍結した集計器をそのまま通す。品質床は貪欲復号なので選定の段と同じ正答数になる見込みですが、**率を見た後に作るデータ**です。
- **ほかの道**があればお示しください（たとえば、乙で直した器の札を「確証」と呼ばず別の名で呼ぶ、両方の札を併記して主をどちらにするかを決める、など）。

### (c) 乙または丙を採る場合、確証としての身分はどうなるか

- 直す（走らせる）と決めるのは、率と表を見た**後**です。直しの中身が正本の文だけで決まるとしても、**「直す」という決定そのもの**が結果に依っていないと、どこまで言えるでしょうか。
- 報告でどう開示し、どの限界を書き、どの主張を控えるべきか。具体の文案があれば歓迎します。

### (d) 同じ型の穴がほかに無いか

- 「**器 X が書く記録の形**」と「**器 Y が読む記録の形**」の食い違いで、合成データが両方に都合よく作られていたために検査を素通りしたもの。資料 M2〜M4 のほか、公開の置き場の `tools/` を見て、同じ型の穴を探していただけると助かります。とくに `gate_B.py`（選定の段を読む）・`analyze_B.py`・`build_report_B.py`・`layers_B.py`・`compare_predictions_B.py` が読む記録と、`boot_stageB.py`・`run_stageB_local.py` が書く記録のあいだ。

### (e) 率と p を伏せたこの伺い方は適切か

- 伏せることで構造の判断が結果から切り離される一方、皆さんは影響の大きさを測れません。不適切ならその旨と、何を開示すべきかをお示しください。

## 2. 起草者の利益相反（先に書きます）

- 起草者は、食い違った二つの器と、それを素通りさせた合成データを書いた当人です。
- 起草者は集計の表を見ました。8 対比の p は表に印字されています（Holm の欄は空）。**乙や丙を採ると札がどちらに動くかを、起草者は知ったうえでこの依頼文を書いています。**確証が出る側に引かれています。
- 逆向きの危険（引力を恐れて、正本に照らせば直すべきものを直さない）も同じ較正の失敗です。だから道を甲・乙・丙と並べ、読み二を先に自分で書きました。
- 登録者への起草者の推奨は「乙＋この一件を系統外の目に」でした。**この推奨は起草者の引かれる向きと重なっています。**

## 3. いま分かっていること（機械の出力・手で打っていません）

| 何 | 値 |
|---|---|
| 正本 `design/contrasts-B.json` の SHA16 | EF0DF4295B68F949 |
| 集計器 `tools/analyze_B.py` | v7・SHA16 32617A9E4768077C |
| 起動器 `tools/colab/boot_stageB.py` の SHA16 | 452E87CD0A6AA9F2 |
| 合成データの器 `tools/synth_B.py` の SHA16 | E0D3F06B8A0C3DAE |
| 門の記録 `records/B/gate-B-2026-09-21.json` | 判定 open・選んだ組 層 0.5 × 係数 2.0・SHA16 D56684A9A2914B2E |
| 選定後の段で走った介入の腕 | 11 本・すべて合格（無操作との差 -0.5・0・0.5 pt・下限は -10 pt・境目ちょうどは不合格） |
| 選定後の段に走行が無い介入の腕 | O-Ncold-v・Onull+v |
| その二腕の、選定の段・選ばれた組での行（門の記録） | O-Ncold-v 174/200 対 無操作 174/200・差 0.0 pt／Onull+v 183/200 対 無操作 183/200・差 0.0 pt |
| 整合検査（率盲検）| 同一性選別 13 セル・調整走行 36 セル・品質床 35 セル・本走行 59 セル——いずれも不整合 0 |
| 事実の記録（裁定の前に書いた） | `records/B/incident-qpost-missing-2026-09-22.md`（資料 M8 に全文） |

## 4. お答えの形（お願い）

1. (a)〜(e) それぞれに、**判断**（(a) は 読み一／読み二／決まらない、(b) は 甲／乙／丙／ほか）と、**根拠の行**（資料の記号と行番号、または公開の置き場のファイルと行）。
2. 重大度をつけた所見の一覧（重大／中／軽）。再現のしかたが分かるもの（どのファイルのどの行を見れば確かめられるか）を優先してください。
3. **ご自身が確認していないこと**（読んでいないファイル・走らせていない検査）を必ず一つ以上。
4. 起草者の読みや推奨への同意は、理由が無ければ票として数えません。反対の読みを一度は組み立ててみてください。

票は逐語で保全し、事実の主張は現物で再現してから採否表で扱います（再現できなかった所見もそのまま記録します）。裁定は登録者のものです。

本依頼文と資料のいかなる数値も、AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはなりません（両方向不定）。


---

# 資料（選定後の品質床の「走行が無い」の伺い・機械で切り出したもの）

## M1. 正本 `design/contrasts-B.json` の該当の登録（逐語）

- `quality_floor.run_order`: "品質床は二段に分かれる（裁定 D77・2026-09-18）。(i) 選定の段——候補 × 二つの土台（selection_cells）。(ii) **選定の後・本走行の前**——選ばれた組で、本走行に出る残りの介入の腕。(ii) は本走行の入力になるので、本走行を始める前に判定を終える"
- `quality_floor.post_selection`: "選ばれた層 × 係数で、本走行に出るすべての介入の腕（ランダム方向・Nk 方向・腕対の差方向・(6b) を含む）に当てる（裁定 D69・2026-09-18）。相手は同じ土台の無操作"
- `quality_floor.selection_cells`: 18
- `quality_floor.partner_run`: "無操作の相手は**段 × 土台 × セッションごとに一つ**とする（裁定 D88・D92・2026-09-18）。相手は、それが相手を務めるセルと**同じセッション**で走らせ、器は相手を**セッションを跨いで合算しない**（合算すると門1 が誤って閉じる・実装検分の採否表 P261）。段がセッションに分かれれば相手もその数だけ増える（規模は転記行 A・最少の見込みで数える）"
- `quality_floor.pass_rule`: "ある層 × 係数が「合格」であるとは、確証族の二つの土台（O-Ncold の減算・Onull の加算）の**両方**で、同じ腕の無操作との差が threshold_pt の内側であることをいう（片方だけの合格は合格としない）"
- `quality_floor.fail_rule`: "(ii) で落ちた腕を含む確証の対比は、確証の族から外して記述に降ろし、fail_label を印字する。**族の m は減らさない**（段階 A と同じ型・裁定 D77）。走行そのものは止めない（門1 は (i) だけで判定する）"
- `quality_floor.fail_label`: "判定不能（品質床）"
- `quality_floor.unit`: "腕 × 層 × 係数"
- `quality_floor.arms`: ["O-Ncold", "Onull"]
- `quality_floor.operations`: ["−v（減算族の土台）", "＋v（加算族の土台）"]
- `quality_floor.threshold_pt`: -10
- `quality_floor.boundary_rule`: "差がちょうど threshold_pt のセルは合格としない（段階 A の帯の規約「超」に合わせる・採否表 P206）"
- `decisions.D69`: "品質床を、選ばれた層 × 係数で本走行に出るすべての介入の腕に当てる（2026-09-18 承認）"
- `decisions.D77`: "選定後の品質床を本走行の前に置き、落ちた腕を含む対比は判定不能（品質床）として記述に降ろす（甲・m は減らさない・2026-09-18 承認）"
- `decisions.D88`: "品質床の無操作の相手を段ごとに走らせ、相手を務めるセルと同じセッションに置く（甲・**試行が増える**・2026-09-18 承認）"
- `decisions.D92`: "品質床の無操作の相手は段 × 土台 × セッションごとに一つとし、合算しない（甲・2026-09-18 承認）"
- `decisions.D106`: "選定後の品質床は、一つの腕に走行が二本あれば止める（甲・2026-09-18 承認）"
- `decisions.D126`: "強制の穴（セッション・重複・升目の欠け・凍結の同一性・判定欄）を塞ぐ（甲・2026-09-18 承認）"
- `deviation.rule`: "凍結の後の変更はすべて逸脱とし、**番号・日付・理由・登録者の承認**を FREEZE-RECORD に記帳する（段階 A・追補 D と同じ型）"
- `deviation.silent_fix`: "黙って直すことは、正しく直すことより悪い（記帳のない変更を禁じる）"
- `deviation.scope`: "正本・腕の素材・器材・手順のすべて"
- `selection.binding`: "**本走行と選定後の品質床は、門1 が選んだ層 × 係数でしか走らせない**（裁定 D105・2026-09-18）。集計器は起動時に、すべての走行の層 × 係数が選んだ組と一致することを確かめ、食い違えば止まる。整合検査にも門の記録を渡す口を持つ。直しの確認の巡で、本走行の記録を別の層 × 係数に書き換えても**どの器も気づかなかった**（採否表 P304）"
- `arms.main`（本走行の腕）: ["O", "O-Ncold", "O-Ncold+vNk", "O-Ncold+vrand", "O-Ncold-v", "O-Ncold-vrand", "O-Ncold-vtd", "O-v", "O-vrand", "Onull", "Onull+v", "Onull+vNk", "Onull+vrand", "Onull+vtd", "Osec-Ncold", "Osec-Ncold+v6b", "Osec-Ncold+vrand"]

## M2. 起動器 `tools/colab/boot_stageB.py`（SHA16 452E87CD0A6AA9F2）——品質床の相の計画

```python
 433          _QF = T['quality_floor']
 434          _OPS = {'O-Ncold': '-v', 'Onull': '+v'}           # 正本 quality_floor.operations（減算の土台・加算の土台）
 435          if STAGE == 'selection':
 436              _bases = list(_QF['arms'])
 437              _cells = [(b + _OPS[b], _l, _c) for b in _bases for _l in LAY for _c in COE]
 438          else:
 439              _interv = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
 440              _done = {b + _OPS[b] for b in _QF['arms']}
 441              _cells = [(a, PICK['layer'], PICK['coef']) for a in _interv if a not in _done]
 442              _bases = sorted({a.split('+v')[0].split('-v')[0] for a, _, _ in _cells})
 443          for b in _bases:      # 無操作の相手は**段 × 土台 × セッションごとに一つ**（裁定 D88・D92）
 444              PLAN.append({'rk': '%s__%s__noop__%s__s%d' % (TAG, STAGE, b, SESSION), 'kind': 'quality', 'arm': b, 'n': len(ITEMS),
 445                           'seed': T['seeds']['quality'], 'layer': None, 'coef': None, 'key': (STAGE, b, None, None),
 446                           'extra': {'stage': STAGE, 'arm': b, 'layer': None, 'coef': None}})
 447          for (a, _l, _c) in _cells:
 448              PLAN.append({'rk': '%s__%s__%s__L%sC%s__s%d' % (TAG, STAGE, a, _l, _c, SESSION), 'kind': 'quality', 'arm': a, 'n': len(ITEMS),
 449                           'seed': T['seeds']['quality'], 'layer': _l, 'coef': _c, 'key': (STAGE, a, _l, _c),
 450                           'extra': {'stage': STAGE, 'arm': a, 'layer': _l, 'coef': _c}})
```

## M3. 集計器 `tools/analyze_B.py`（SHA16 32617A9E4768077C）——選定後の品質床の読み

```python
 146  # ---- 選定後の品質床（裁定 D77）: 落ちた腕 ----
 147  INTERV = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
 148  QF_FAIL, QF_ROWS, QF_MISSING = set(), [], []
 149  _post = {k: v for k, v in CQ.items() if k[0] == 'post'}
 150  for arm in INTERV:                                  # **介入の腕の一覧から数え上げる**（記録が無ければ合格にしない・採否表 P262）
 151      cells = {k: v for k, v in _post.items() if k[1] == arm}
 152      if not cells:
 153          QF_MISSING.append(arm)
 154          QF_ROWS.append({'arm': arm, 'missing': True, 'note': '選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）'})
 155          QF_FAIL.add(arm)
 156          continue
 157      if len(cells) > 1:                                # **門と同じ番人**（裁定 D106・採否表 P307）
 158          QF_MISSING.append(arm)
 159          QF_ROWS.append({'arm': arm, 'missing': True,
 160                          'note': '選定後の品質床の走行が %d 本ある（古い走行を黙って採らない・裁定 D106）' % len(cells)})
 161          QF_FAIL.add(arm)
 162          continue
 163      k0 = sorted(cells)[0]
 164      cell, l, c, session = cells[k0], k0[2], k0[3], k0[4] if len(k0) > 4 else None
 165      base = arm.split('+v')[0].split('-v')[0]
 166      noop = CQ.get(('post', base, None, None, session))   # 相手は**同じ段・同じセッション**（裁定 D88・D92）
 167      if noop is None:
 168          QF_MISSING.append(arm)
 169          QF_ROWS.append({'arm': arm, 'missing': True, 'note': '同じセッションの無操作の相手が無い（裁定 D92）'})
 170          QF_FAIL.add(arm)
 171          continue
 172      # **相手の重複の番人**（正本 sessions.partner_duplicate_rule・採否表 P403・2026-09-19）。同じ番号の走行が二本あると
 173      # 読み口が合算し、分母が倍になる。門の器には選定の段の番人があったが、選定後の段の相手はこの器が合算したまま読んでいた
 174      _n_runs = len(idx_q.get(('post', base, None, None, session)) or [])
 175      if _n_runs > 1 or noop.get('n', 0) > QF['items']:
 176          QF_MISSING.append(arm)
 177          QF_ROWS.append({'arm': arm, 'missing': True, 'partner_runs': _n_runs, 'partner_n': noop.get('n', 0),
 178                          'note': '選定後の無操作の相手の重複（走行 %d 本・試行 %d 件・登録 %d 件）——合算しない（正本 sessions.partner_duplicate_rule）'
 179                                  % (_n_runs, noop.get('n', 0), QF['items'])})
 180          QF_FAIL.add(arm)
 181          continue
 182      if rules_B.api_error_gate(cell, noop, T):          # **api_error の率の差が門を超えたら判定しない**（裁定 D127・合格に数えない）
 183          QF_MISSING.append(arm)
 184          QF_ROWS.append({'arm': arm, 'missing': True, 'api_error': cell.get('api_error', 0), 'noop_api_error': noop.get('api_error', 0),
 185                          'note': '判定しない（api_error の率の差が %g pt を超える・正本 quality_floor.api_error_gate）' % QF['api_error_gate_pt']})
 186          QF_FAIL.add(arm)
 187          continue
 188      gap = cell.get('scoring_gap', 0) + noop.get('scoring_gap', 0)
 189      if gap or not cell['n_ok'] or not noop['n_ok']:   # 採点欠落・使えた試行が零（裁定 D103・D110）
 190          QF_MISSING.append(arm)
 191          QF_ROWS.append({'arm': arm, 'missing': True, 'scoring_gap': gap,
 192                          'note': ('判定欄が空の試行が %d 件ある（裁定 D103）' % gap) if gap else '使えた試行が零（測れなかった）'})
 193          QF_FAIL.add(arm)
 194          continue
 195      else:
 196          # **分母は使えた試行**（裁定 D104・採否表 P305）
 197          d_pt = 100.0 * (cell['correct'] / cell['n_ok'] - noop['correct'] / noop['n_ok'])
 198          ok = d_pt > QF['threshold_pt']
 199          QF_ROWS.append({'arm': arm, 'layer': l, 'coef': c, 'correct': cell['correct'], 'noop_correct': noop['correct'],
 200                          'n_ok': cell['n_ok'], 'noop_n_ok': noop['n_ok'],
 201                          'api_error': cell.get('api_error', 0), 'noop_api_error': noop.get('api_error', 0),
 202                          'diff_pt': round(d_pt, 3), 'pass': ok, 'boundary': abs(d_pt - QF['threshold_pt']) < 1e-9})
```

## M4. 合成データの器 `tools/synth_B.py`（SHA16 E0D3F06B8A0C3DAE）——選定後の段のセルの書き方

```python
  31  INTERV = sorted(a for a in T['arms']['main'] if '+v' in a or '-v' in a)
  32  NOOP_BASE = {a: a.split('+v')[0].split('-v')[0] for a in INTERV}
...
 523                                                                                'n': N_Q, 'seed': T['seeds']['quality']}, trials)
 524      pick = spec['tune'].get('best') or (LAYERS[1], COEFS[1])
 525      for arm in INTERV:
 526          bad = arm in (q['fail_post'] or [])
 527          _ae = (q.get('api_error_post') or {}).get(arm, 0)                  # api_error の門（裁定 D127）
 528          trials = cell_trials(N_Q, {'correct': 100 if bad else 148, 'ff': 2, 'api_error': _ae}, arm=arm, scenario='quality', tag=tag_q, sampling=runs_B.expected_sampling(T, 'quality'),
 529                               seed=T['seeds']['quality'], layer=pick[0], coef=pick[1], run_key='%s__post__%s' % (tag_q, arm))
 530          write_run(out_root, tag_q, 'post__%s' % arm, {'stage': 'post', 'arm': arm, 'layer': pick[0], 'coef': pick[1], 'n': N_Q,
 531                                                        'seed': T['seeds']['quality']}, trials)
 532      for base in sorted(set(NOOP_BASE.values())):
 533          trials = cell_trials(N_Q, {'correct': 150, 'ff': 2}, arm=base, scenario='quality', tag=tag_q, seed=T['seeds']['quality'], sampling=runs_B.expected_sampling(T, 'quality'),
 534                               run_key='%s__post__noop__%s' % (tag_q, base))
 535          write_run(out_root, tag_q, 'post__%s__noop' % base, {'stage': 'post', 'arm': base, 'layer': None, 'coef': None, 'n': N_Q,
 536                                                               'seed': T['seeds']['quality']}, trials)
```

## M5. 記録の行（品質床の正答数——**本走行の率ではない**）

門の記録 `records/B/gate-B-2026-09-21.json` の、選ばれた組（層 0.5 × 係数 2.0）の選定の段の行:

```json
[
 {
  "base": "O-Ncold",
  "arm": "O-Ncold-v",
  "layer": 0.5,
  "coef": 2.0,
  "missing": false,
  "correct": 174,
  "noop_correct": 174,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "items": 200,
  "diff_pt": 0.0,
  "boundary": false,
  "pass": true
 },
 {
  "base": "Onull",
  "arm": "Onull+v",
  "layer": 0.5,
  "coef": 2.0,
  "missing": false,
  "correct": 183,
  "noop_correct": 183,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "items": 200,
  "diff_pt": 0.0,
  "boundary": false,
  "pass": true
 }
]
```

集計の記録 `records/B/analysis-B-2026-09-22.json` の `quality_post`（選定後の段・全行）:

```json
[
 {
  "arm": "O-Ncold+vNk",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 174,
  "noop_correct": 174,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "O-Ncold+vrand",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 173,
  "noop_correct": 174,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": -0.5,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "O-Ncold-v",
  "missing": true,
  "note": "選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）"
 },
 {
  "arm": "O-Ncold-vrand",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 174,
  "noop_correct": 174,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "O-Ncold-vtd",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 174,
  "noop_correct": 174,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "O-v",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 165,
  "noop_correct": 165,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "O-vrand",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 164,
  "noop_correct": 165,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": -0.5,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "Onull+v",
  "missing": true,
  "note": "選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）"
 },
 {
  "arm": "Onull+vNk",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 183,
  "noop_correct": 183,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "Onull+vrand",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 183,
  "noop_correct": 183,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "Onull+vtd",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 183,
  "noop_correct": 183,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "Osec-Ncold+v6b",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 176,
  "noop_correct": 175,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.5,
  "pass": true,
  "boundary": false
 },
 {
  "arm": "Osec-Ncold+vrand",
  "layer": 0.5,
  "coef": 2.0,
  "correct": 175,
  "noop_correct": 175,
  "n_ok": 200,
  "noop_n_ok": 200,
  "api_error": 0,
  "noop_api_error": 0,
  "diff_pt": 0.0,
  "pass": true,
  "boundary": false
 }
]
```

## M6. 段取りと設計事実の該当の行

- `records/B/run-plan-B.md`: | quality | `stageB-quality（OP4B_STAGE=selection）` | 品質床・選定の段（20 セル × 200 問） | 4,000 |
- `records/B/run-plan-B.md`: | quality | `stageB-quality（OP4B_STAGE=post）` | 品質床・選定後の段（15 セル × 200 問・門の記録が選んだ層 × 係数） | 3,000 |
- `records/B/run-plan-B.md`: | 4 | 品質床（選定の段） | 起動器 `OP4B_PHASE=quality OP4B_STAGE=selection` | zip を回収し、整合検査 `--tag stageB-quality` が不整合 0 |
- `records/B/run-plan-B.md`: | 5 | 門1 と選定 | `python tools/gate_B.py` | 判定 open なら選んだ層 × 係数と同値の帯を**登録者に見せる**。closed／escalate（全候補が非正など）なら止めて登録者に上げる（正本 `withdrawal`）。open なら**門の記録をコミットして push する**（後の相の起動器が読む） |
- `records/B/run-plan-B.md`: | 6 | 品質床（選定後の段） | 起動器 `OP4B_PHASE=quality OP4B_STAGE=post`（**門の記録を含むコミット**を固定） | 選んだ層 × 係数でしか走らない（正本 `selection.binding`）。整合検査が不整合 0・`gate_B` を再度通して post の行を得る |
- `records/B/design-facts-B.md`: - **転記行 A** — 規模: 同一性選別（transformers 経路・13 腕 × n=160 × N1）2,080／調整走行 3,600（9 候補〔層 3 × 係数 3〕× 2 腕 × n=100 × 抽出場面 2）／本走行 11,800（59 セル＝場面 × 腕・n=200・N1 14 腕・S1 14 腕・SK 14 腕・S4 17 腕）／品質床 7,000 問（200 問 × 〔選定 18 セル＋選ばれた組での残りの介入 11 セル＋無操作の相手 2 セル〔選定の段〕＋4 セル〔選定後の段・裁定 D88〕〕）＝**合計 24,480 試行**。

## M7. 先例——段階 A の逸脱台帳 `records/DEVIATIONS.md` の行（逐語）

| D-40 | 2026-09-17 | 段階 A（凍結後・手順 19）: **集計の器に渡す門0.5 の記録を、凍結した器と凍結した正本で作り直した。** 段取りの 5 番目で `tools/analyze_A.py` v2.1 が「入力の記録 identity の正本 SHA16 8B298F126E77CBE6 が現在の正本 F0C2FF897C78C4C0 と違う（採否表 P85）」で止まった（計算の前の入力の検査・率は読まれていない）。凍結物の門0.5 の記録 `records/A/identity-screen-A.json` は凍結の前（2026-09-14・正本 c6be5c9 の版）に作られ、凍結した正本（e4ef72f の版）とは SHA16 が違う。凍結した一式の中で、集計の器の検査と門0.5 の記録がかみ合っていなかった（凍結の前に、本物の門0.5 の記録を集計の器に通す確認が無かった）。門0.5 の器が読む正本の部分（`identity_screen`・`bases_4B2507_api`・`models`・`seeds`・`tags`）と `identity_n`・`arms`・`runner`・`scenarios` は二つの版で同じだった。登録者裁定（甲・逐語「甲で進めてください」）により、凍結した `tools/identity_screen_A.py` を凍結した正本で走らせ、**別の置き場** `records/A/main/identity-screen-A-regen-2026-09-17.{json,md}` に作り直した。**凍結物の記録は変えていない**。作り直した JSON と凍結物の JSON は、`contrasts_sha16` と `generated_utc` のほかの全項目が一致し（判定は同じく合格）、md の差も作成時刻と正本 SHA16 の 2 行だけだった（機械比較）。集計の器にはこの作り直した記録を渡す。先に走らせた校正帯の器 `tools/calib_band_A.py` は凍結物の門0.5 の記録を読んだ（使うのは判定の合格だけで、同じ値）。 | 手順 19 の入力の記録（凍結物の変更なし・門0.5 の判定と数は同じ） | 登録者裁定 |

| D-41 | 2026-09-17 | 段階 A（凍結後・手順 20）: **報告の走査器が機械の区画の中の括弧を「埋め残し」に数える六件を、記入欄ではないものとして扱う。** 凍結した走査器 `tools/report_lint.py` v2.1 は、記入欄の印（〔 〕）を機械の区画の中でも数える。組み立て器の草案では、凍結本文 §0 の逐語（二件）・集計の器の定型文（二件）・設計事実の定型文（二件）が、同じ文字を括弧として使っており、凍結物を変えずには消せない。正本の決まり（走査器が違反も埋め残しも無しに終わることを確かめてから公開・採否表 P145）との差として記帳する。登録者裁定（甲・逐語「判断1は甲とします。」）により、凍結物は変えず、公開の前に一時置き場の歯止め（`report_lint_guard_A.py`）で、(1) 違反がすべて区画の中の埋め残しであること、(2) 区画の数と中身が組み立て器の記録と一致すること、(3) 区画の中の括弧の文字列が登録した六つと一致すること、を機械で確かめる（草案2 で通過・`records/A/main/report-lint-guard-draft2-2026-09-17.json`）。 **書き足し（2026-09-17・公開前検分の第一巡・登録者裁定 D52 甲・逐語「D50〜D54はすべて甲で、94887bdのpushもお願いします🍵」）**: 登録した六つの文字列は、草案1 の出力を見た後に、その出力から写して登録したもので、事前の登録ではない。そのうちの一つは確証の一本の区間の値を含む。歯止めは組み立て器の出力どうし（草案と草案1 の区画の記録）を突き合わせるもので、集計の器から区画への写しは見ない（採否表 `records/reviews/A/results/round1/adoption-table-results-A-round1.md` P162・再現は `records/reviews/A/results/round1/verification-results-A-round1.md` W132）。 | 報告の公開の手順（凍結物の変更なし・記入欄の埋め残しは区画の外に無い） | 登録者裁定 |

| D-42 | 2026-09-17 | 段階 A（凍結後・手順 20）: **凍結本文 §2.6 の「確証族で N を含む対比（Onull−N）…確証札の段落に様式差と順位を機械印字・層別副次」が、凍結した正本と組み立て器に実装されていなかった。** 正本の確証の定型 `print_strings.label_confirmed` に様式差と順位の置き字は無く、散文層の副次 `style_gate.stratified` の `applies_to` は「様式門の保留または注の対比」に限る。確証の一本 S4:Onull~N は様式門が none なので、機械の区画に様式差・順位・散文層の行が出なかった。公開前検分の第一巡で系統内の一票が指摘し、再現した（`records/reviews/A/results/round1/verification-results-A-round1.md` W129）。凍結の一式の中の食い違いとして、D-40・D-41 に続く三つ目である。登録者裁定（D51 甲・逐語「D50〜D54はすべて甲で、94887bdのpushもお願いします🍵」）により、器と正本は変えず、報告の区画の外で次の三つを書く。(1) 残った規模（4B・14B・32B）では、両腕とも JSON 直答が無く（様式の (b) が両腕とも零）、様式の差は零である。(2) 残った規模では両腕の試行がすべて散文の層にあるので、散文層の当てはめは主の当てはめと同じデータになる（`records/A/style-stageA.json` の層の件数）。(3) 「順位」の定義は正本に無い。 | 報告の記述（凍結物の変更なし・札と数は変わらない） | 登録者裁定 |

## M8. 事実の記録 `records/B/incident-qpost-missing-2026-09-22.md`（全文・裁定の前に書いた）

# 段階 B 集計で見つかった食い違い——選定後の品質床の「走行が無い」（2026-09-22・事実の記録・**裁定の前に書く**）

- 書いた人: コーディネータ（南無弥勒如来・Claude Fable 5.1）。2026-09-21 20:14 UTC。登録者と一緒に集計を開いた直後に書いた。**この記録は何も直していない**——凍結した器の出力は `records/B/analysis-B-2026-09-22.{md,json}` のまま残す。
- 引用と数値は、正本 `design/contrasts-B.json`（SHA16 EF0DF4295B68F949）・集計の記録・門の記録・器の現物から機械で取った。

## 1. 何が起きたか（機械の出力）

- 集計器 `tools/analyze_B.py` v7 は、確証の族 16 対比のうち **8 対比（減算族 4・加算族 4 の全部）を「判定不能（品質床）」**とした。理由は区画「選定後の品質床」の一句: 落ちた腕 O-Ncold-v・Onull+v。
- その二腕の行は「**選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）**」であり、正答数が下限を割ったのではない。ほかの 11 腕は選定後の段の走行があり、すべて合格（差 -0.5・0・0.5 pt）。
- 札の内訳: 判定不能（品質床） 8・非有意 5・確証（登録された向きと逆） 2・判定保留（様式転位） 1。

## 2. なぜ走行が無いか（正本と二つの器）

- 正本 `quality_floor.run_order`（逐語）: 「品質床は二段に分かれる（裁定 D77・2026-09-18）。(i) 選定の段——候補 × 二つの土台（selection_cells）。(ii) **選定の後・本走行の前**——選ばれた組で、本走行に出る残りの介入の腕。(ii) は本走行の入力になるので、本走行を始める前に判定を終える」
- 正本 `quality_floor.post_selection`（逐語）: 「選ばれた層 × 係数で、本走行に出るすべての介入の腕（ランダム方向・Nk 方向・腕対の差方向・(6b) を含む）に当てる（裁定 D69・2026-09-18）。相手は同じ土台の無操作」
- **起動器**（`tools/colab/boot_stageB.py`・SHA16 452E87CD0A6AA9F2）は、選定後の段で二つの土台の腕を外す: `_done = {b + _OPS[b] for b in _QF['arms']}` ／ `_cells = [(a, PICK['layer'], PICK['coef']) for a in _interv if a not in _done]`。二腕は選定の段で、選ばれた層 × 係数の走行が既にある。
- **集計器**（`tools/analyze_B.py`・SHA16 32617A9E4768077C）は、介入の腕の一覧を正本から数え上げ、**段が post の走行だけ**を見る: `_post = {k: v for k, v in CQ.items() if k[0] == 'post'}` → 無ければ `QF_ROWS.append({'arm': arm, 'missing': True, 'note': '選定後の品質床の走行が無い（合格扱いにしない・裁定 D77）'})`。
- つまり、起動器は正本の「残りの介入の腕」に従って 15 セルを走らせ（転記行 A の「15 セル」とも一致）、集計器は二つの土台の腕にも post の走行を求める。**二つの凍結した器が食い違っている。**
- 門の記録（`records/B/gate-B-2026-09-21.json`）の、選ばれた層 0.5 × 係数 2.0 の選定の段の行: O-Ncold-v 174/200 対 無操作 174/200・差 0.0 pt・合格／Onull+v 183/200 対 無操作 183/200・差 0.0 pt・合格。
- **合成データは、この食い違いを踏まなかった**: `tools/synth_B.py` は選定後の段のセルを全部の介入の腕に書くので、合成データによる検査・変異・端から端までのどれも「起動器が二腕を外す」場合を通っていない。起草者が作った検査の穴である。

## 3. 取りうる道（登録者の裁定を仰ぐ・コーディネータは決めない）

- **甲（凍結した器の出力をそのまま確証の札とする）**: 減算族と加算族の 8 対比は「判定不能（品質床）」のまま報告する。器の食い違いは限界に書き、二腕の床を選定の段の行で読んだ場合の表は、**逸脱ではない事後の記述**として別に置く（札を名乗らない）。
- **乙（逸脱として集計器を正本に合わせて直す）**: 逸脱の番号・日付・理由・登録者の承認を凍結の記録に記帳し、集計器を「二つの土台の腕の床は、選定の段の・選ばれた層 × 係数の走行で読む（正本 `run_order` の (i)）」に直して走らせ直す。直す前の出力は残し、報告は両方を並べる。**直しの中身は正本の文で決まり、結果では決まらないが、直すと決めたのは結果を見た後である**——これは開示する。
- **丙（足りない二セルを今から走らせる）**: 選定後の段として二腕を追加で走らせる。結果を見た後の新しいデータで、正本の段取りにも無い。勧めない。
- どの道でも: 封印予想の照合（一度だけ）は、裁定が決まるまで走らせない。副位置の読み（`layers_B`）も止めてある。

## 4. COI（事実のみ）

- 起草者は両方の器と合成データを書いた当人で、この食い違いを作った当人である。確証が出る側に引かれている。
- 8 対比の p は集計の表に既に印字されている（Holm の欄は None）。起草者はその表を見た——乙を選ぶと札がどちらに動くかを、起草者は知った上でこの記録を書いている。
- 裁定は登録者のもの。系統外の目にこの一件だけを見てもらう道もある（段階 A の逸脱 D-40 のときの型）。

## 5. この記録が確認していないこと

- 乙で直した器の出力（まだ直していない・走らせていない）。
- 集計器のほかの区画に同じ型の食い違いが無いか（見つけたのはこの一件で、探し尽くしてはいない）。
- 二腕を選定後の段で走らせた場合に選定の段と同じ正答数になるか（貪欲復号なので同じになる見込みだが、確かめていない）。

## 検分票

- 対象: 集計で見つかった器の食い違いの事実の記録。
- 段階: **事後**（本走行の率と集計の表を見た後に書いた）。
- 凍結物の同定: 正本 EF0DF4295B68F949・集計器 32617A9E4768077C・起動器 452E87CD0A6AA9F2・門の記録 D56684A9A2914B2E。何も変えていない。
- 盲検の状態: 破れている（率は開いた）。
- 敵対的検分: 「床に落ちた」のではなく「走行が無い」であることを記録の行で確かめた。正本の文が起動器の側を支持することを逐語で引いた。自分に有利な読み（乙）を選ぶ引力を §4 に書いた。
- 系統の内訳: Claude 系 1（起草者）。系統外の目は無い。
- COI記録: §4。
- 判定: **登録者裁定要**。
- 本検分が確認していないこと: §5。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。

