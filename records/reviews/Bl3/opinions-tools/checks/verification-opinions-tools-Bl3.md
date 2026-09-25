# 器についての意見伺いの確かめ（機械生成・`checks/verify_opinions_Bl3.py`）

- ご意見の中の事実の主張を、正本と器の実物で確かめた記録。値と行は器と正本から機械で引いた。採否の案（`adoption-proposal-opinions-tools-Bl3.md`）が番号 V で引く。

## V0 器と正本は束の入力のコミット 029d55f から変わっていない

- 出所の主張: —
- 結果: 確かめた

```json
{
 "git_diff_stat": "（差なし）"
}
```

## V1 下見で主の升目を外した形で、集計の器の門と独立の再計算の一致が落ちる

- 出所の主張: C1-B1・C2-A1
- 結果: 再現した（台本を走らせた）

```json
{
 "script_output": [
  "一 row_labels           通った",
  "一 gates                落ちた: KeyError 'S1|Onull|+1'",
  "一 recompute_agreement  落ちた: KeyError 'S1|Onull|+1'"
 ]
}
```

## V2 札の一致の裾の欄が、帰無の内側の行で小さな揺れに反転し、一致を落とす

- 出所の主張: C2-A2
- 結果: 再現した（台本を走らせた・乱数の種は固定・二度とも同じ出力）

```json
{
 "script_output": [
  "二 揺れ／帰無の広がり 0.005  今の決まりで一致が落ちる割合 0.003・裾を等方の外の行だけで比べると 0.003・欄ごとの食い違い {'second_top': 1}",
  "二 揺れ／帰無の広がり 0.02   今の決まりで一致が落ちる割合 0.060・裾を等方の外の行だけで比べると 0.010・欄ごとの食い違い {'tail': 15, 'second_top': 2, 'iso_outside': 1, 'side': 1, 'sign': 1}",
  "二 揺れ／帰無の広がり 0.05   今の決まりで一致が落ちる割合 0.157・裾を等方の外の行だけで比べると 0.043・欄ごとの食い違い {'tail': 38, 'second_top': 11, 'iso_outside': 2, 'side': 2, 'sign': 2}"
 ]
}
```

## V3 落ちる所の器の行

- 出所の主張: C1-B1・C2-A1
- 結果: 行を読んで確かめた

```json
{
 "gates_ue": [
  [
   109,
   "ue = {u: {f: eff[f][u] for f in sorted({r['fam'] for r in rows})} for u in units}"
  ]
 ],
 "recompute_main_ov": [
  [
   155,
   "for r in main_rows:"
  ],
  [
   167,
   "for r in main_rows:"
  ],
  [
   168,
   "if r['direction'] != 'static' or (rows_subset is not None and r['id'] not in rows_subset):"
  ],
  [
   171,
   "main_ov[r['id']] = {'effect': eff_main[k]['static'], 'iso': [eff_main[k]['iso:%d' % i] for i in range(n_iso)],"
  ]
 ],
 "run_main_phase_skip": [
  [
   461,
   "if ck in dropped:"
  ]
 ],
 "judge_rows_subset": [
  [
   327,
   "(pilot.get('decision') or {}).get('dropped', []), rows_subset=set(rc['hook']) if dry else None)"
  ],
  [
   341,
   "rows_subset=set(rc['hook']) if dry else None)"
  ]
 ]
}
```

## V4 偶然の目安は行ごとの 1/(比べる相手の数+1) の和で、集計の器は正本の定数をそのまま置いている

- 出所の主張: C1-B2・C2-A3
- 結果: 式を再現し、外した後の値を器で出した

```json
{
 "generator": [
  [
   43,
   "chance_second = round(n_v_rows / (comparators_oriented['static'] + 1) + n_nk_rows / (comparators_oriented['Nk'] + 1), 4)"
  ],
  [
   44,
   "chance_second_pair = round(n_v_rows / (comparators['static'] + 1) + n_nk_rows / (comparators['Nk'] + 1), 4)"
  ]
 ],
 "canon": [
  0.3087,
  0.6057
 ],
 "recomputed_all_rows": [
  0.3087,
  0.6057
 ],
 "recomputed_after_dropping_N1|O-Ncold": [
  0.2701,
  0.53
 ],
 "analyzer_line": [
  [
   244,
   "descriptive=descriptive(T3, main_out), chance={'oriented': T3['nulls']['real']['chance_second'], 'pair': T3['nulls']['real']['chance_second_pair']})"
  ]
 ]
}
```

## V5 Nk と td の自分の対は正本に名が無く器の中にある。B-lens の凍結の器の OWN_PAIR と同じか

- 出所の主張: C2-A5（錨の案）
- 結果: 同じ

```json
{
 "bl3_core_own": {
  "Nk": "Nk~N",
  "td": "Onull~N"
 },
 "blens_lens_OWN_PAIR": {
  "static": "O~Osec",
  "loaded": "O-Ncold~Osec-Ncold",
  "Nk": "Nk~N",
  "td": "Onull~N"
 },
 "swap_siblings": [
  "O~Osec",
  "O~Osec-Ncold",
  "Osec~O-Ncold",
  "O-Ncold~Osec-Ncold"
 ],
 "static_loaded_own_in_swap": true
}
```

## V6 等方を正本の本数にした合成の試しで、二段目の効き目の差の最大が許容を超えた（ご意見が届く前に見た）

- 出所の主張: コーディネータ（K1）・C1-C3・C2-B7・G1-3(3)
- 結果: 試しの記録のとおり

```json
{
 "rows": [
  "- 等方の方向の本数: 1999（正本 1999）。順伝播 5918 回・2837.0 秒。",
  "- 確かめ: 41 のうち 39 が期待どおり。",
  "| 二 | 二段目（本の道とフック・近道なし・バッチ一）の効き目の差が「近道の許容＋揺れの床」の内 | **期待と違う** | 差の最大 6.72e-03（許容 0.0050） |",
  "| 二 | 集計の器の二段目の一致（合成・一段目は独立の再計算の器ができた後） | **期待と違う** | 二段目 False（差の最大 6.72e-03・許容 0.0050）・一段目 まだ無い・全体の一致 False |",
  "| 二 | 二段目の許容を超える揺れを入れると一致しない | 期待どおり | 入れた差 0.0150 |"
 ]
}
```

## V7 二段目の差の出どころ（近道ありと近道なしの、同じバッチ 16 での効き目の差の分布）

- 出所の主張: コーディネータ（K1）
- 結果: 切り分けの出力のとおり

```json
{
 "probe_output": [
  "# 二段目の切り分けの出力（コーディネータ・`checks/probe_stage2_fulliso.py`・乱数の小さな模型・合成・等方は正本の本数）",
  "N1|Onull|+1 {\"n\": 2034, \"noop_shift\": -0.003774733295458077, \"eff_diff_max_abs\": 0.006714060684712475, \"eff_diff_median\": 0.003774733295458077, \"steered_lo_diff_max_abs\": 0.004688186403916106, \"steered_lo_diff_nonzero\": 431, \"n_eff_over_0.005\": 15, \"check_dir_eff_diff\": null, \"q\": [0.003774733295458077, 0.0037795311191949565, 0.004786198953394467, 0.006714060684712475], \"seconds\": 560.6}",
  "S1|O-Ncold|-1 {\"n\": 2034, \"noop_shift\": 0.0, \"eff_diff_max_abs\": 0.0, \"eff_diff_median\": 0.0, \"steered_lo_diff_max_abs\": 0.0, \"steered_lo_diff_nonzero\": 0, \"n_eff_over_0.005\": 0, \"check_dir_eff_diff\": null, \"q\": [0.0, 0.0, 0.0, 0.0], \"seconds\": 789.0}",
  "[exited with code 0]"
 ]
}
```

## V8 札の一致は全ての行の裾を比べている

- 出所の主張: C2-A2
- 結果: 行を読んで確かめた

```json
{
 "labels_signature": [
  [
   102,
   "return {rid: (o['iso_outside'], o['tail'], (o['side'] or {}).get('side'), (o['side'] or {}).get('sign'), o['second']['top']) for rid, o in lab.items()}"
  ]
 ],
 "canon_agreement": "段ごとに、全ての効き目の差の絶対値が許容の内で、かつ段の二つの道の値からそれぞれ出した札が同じとき一致とする。札は、v̂ の行の割合をその道の値で出し直し、主の行すべてに掛け直した Holm の判定・割合を決めた裾（上か下か）・等方の外の行の効き目の側・二つ目の札"
}
```

## V9 効き目の側を添える行について、正本の二つの文が食い違う・器は等方の外の行にだけ側を作り、帰無を捨てる

- 出所の主張: C1-B3
- 結果: 正本の文と器の行で確かめた

```json
{
 "side_rule_head": "等方の外の行は、等方の帰無の中央値と、効き目の側を添えて書く",
 "print_rule_part": [
  "どの行にも、等方の帰無の中央値・効き目の側・p と裾の本数（上の裾と下の裾）・二つ目の札の中心と順位を添える"
 ],
 "analyzer_side": [
  [
   96,
   "o['side'] = K.effect_side(o['effect'], o.pop('_iso')) if o['iso_outside'] else None"
  ]
 ]
}
```

## V10 層ごとの差分の余弦は、符号を掛ける前の方向で取っている

- 出所の主張: C1-B4・C2-B4
- 結果: 行を読んで確かめた

```json
{
 "bl3_run": [
  [
   280,
   "u = R.torch.tensor(R.vec(d), device=R.dev).float()"
  ],
  [
   285,
   "cos = float((dh @ u) / (dh.norm() * u.norm())) if nrm > 0 else 0.0"
  ]
 ],
 "canon": [
  "足した方向との余弦"
 ]
}
```

## V11 門は入れ替える単位が二つ未満のときも判定不能にしている（正本は行が残らないときだけ）

- 出所の主張: C1-B5・C2-B3
- 結果: 行を読んで確かめた

```json
{
 "bl3_core": [
  [
   146,
   "if not rs or len(us) < 2:"
  ]
 ],
 "canon": "門の行が残らなければ「門は判定不能」と書く"
}
```

## V12 書き換えの道の use_cache の既定は None（模型の設定＝既定の呼び方）で、起動器は False を明示して呼ぶ

- 出所の主張: G1-A1
- 結果: 行を読んで確かめた

```json
{
 "rewrite_def": [
  [
   291,
   "def recompute_rewrite(model, tok, T3, FJ, rows, dirs_by_row, dirs, layer_idx, coef, use_cache=None):"
  ]
 ],
 "boot_call": [
  [
   436,
   "out['rewrite'] = RW.recompute_rewrite(model, tok, T3, FJ, rows_rc, dbr, dirs, L, coef, use_cache=False)"
  ]
 ]
}
```

## V13 対数オッズの算術の精度: 本の器は出口の値を float64 にしてから、書き換えの道は float32 のまま logsumexp を取る

- 出所の主張: G2-1-1
- 結果: 行を読んで確かめた

```json
{
 "bl3_run": [
  [
   86,
   "Zs = (hn @ self.W32[cell.set_ids].T).double().cpu().numpy()"
  ]
 ],
 "rewrite": [
  [
   267,
   "lo = z[0] - torch.logsumexp(z[1:], dim=0)"
  ]
 ]
}
```

## V14 独立の再計算の一致は効き目だけを比べ、無操作の値（noop_lo）を比べていない

- 出所の主張: G2-2-1
- 結果: 行を読んで確かめた

```json
{
 "as_eff": [
  [
   165,
   "return {rid: [o['effect']] + list(o['iso']) + list(o['comps_same']) + list(o['comps_opp']) for rid, o in ov.items()}"
  ]
 ],
 "canon_what": "主の値の一部を計算し直す: v̂ の行（主の行のうち static の行）ごとに、無操作の値と、v̂・等方の帰無のすべて・比べる相手のすべて（実在の差・両方の向き）の効き目（順伝播の数は転記行 E）"
}
```

## V15 全語彙の softmax は模型の出口の全ての行で、トークナイザの外の行を含む

- 出所の主張: C2-B6
- 結果: 正本の数から出した

```json
{
 "vocab_size": 151936,
 "tokenizer_len": 151669,
 "rows_outside_tokenizer": 267
}
```

## V16 glob(...)[0] はファイルがちょうど一つかを確かめていない

- 出所の主張: C2-B8
- 結果: 行を読んで確かめた

```json
{
 "analyze": [
  [
   65,
   "cache[k] = [t for t in (json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')) if t['status'] == 'ok']"
  ]
 ],
 "bl3_run": [
  [
   393,
   "tr = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}"
  ],
  [
   394,
   "rw = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}"
  ]
 ]
}
```

## V17 起動器は本の凍結の pilot を、集計の器は pilot_attempts の最後を読む

- 出所の主張: C2-B9
- 結果: 行を読んで確かめた

```json
{
 "boot": [
  [
   390,
   "pilot = FR['main_freeze']['pilot']"
  ]
 ],
 "analyze": [
  [
   365,
   "return FR['main_freeze']['pilot_attempts']"
  ]
 ]
}
```

## V18 近道の assert は記録した切れ目（pc の end）を見て、使い回す cache の実の長さを見ていない

- 出所の主張: C2-B2
- 結果: 行を読んで確かめた

```json
{
 "bl3_run": [
  [
   119,
   "if pc['end'] != cell.mp:        # 近道の元は主位置の手前で切る（主位置を帯に残す・凍結した確かめ・効き目の比べだけでは弱い: 合成の記録）"
  ]
 ]
}
```

## V19 本物の模型の領域で、足す量の一成分と残差の一成分の大きさ・bf16 の刻み（C1 の見積もりの再計算）

- 出所の主張: C1-C2
- 結果: 転記行 D と正本の数から出した（推論の見積もり）

```json
{
 "add_component_rms": 0.0514,
 "residual_component_rms": 0.846,
 "bf16_spacing_at": {
  "0.5": 0.00390625,
  "0.85": 0.00390625,
  "1.0": 0.0078125,
  "4.0": 0.03125,
  "16.0": 0.125
 }
}
```

## V20 書き換えの道の開発の記録の --dry の相手の bl3_run の SHA16 と、束の版の SHA16

- 出所の主張: C1-C4・C2
- 結果: 記録と器から出した

```json
{
 "in_dev_record": [
  "7ECB9CF764F4F8AE"
 ],
 "bl3_run_now": "CB38D8EB2EC9A448",
 "coordinator_rerun_logs": [
  "recompute-rewrite-selftest-coordinator-rerun.log",
  "recompute-rewrite-dry-coordinator-rerun.log"
 ],
 "rerun_logs_record_sha": false
}
```

## V21 門の升目の外しの扱いを「問題なし」とした是認（V1 で落ちることが分かった所）

- 出所の主張: G1-2(5)・G2-2-3
- 結果: ご意見の行を引いた

```json
{
 "G1": [
  [
   132,
   "- 外された升目（`drop_cells`）の行を除外した後、行が存在しなくなった方向単位を入れ替えリスト `us` から除外。入れ替え数 `n_perm` は残った単位数の階乗で正しく計算されます。"
  ]
 ],
 "G2": [
  [
   103,
   "3. 門（`gate`）においても、除外升目の行が除かれ、全行が消失した方向単位（unit）は並べ替え集合 `us` から除外され、入れ替え数 `n_perm` が `len(us)!` で縮小計算されます。"
  ],
  [
   105,
   "これらは正本の複雑な条件分岐を完全に網羅しており、実装の逸脱はありません。"
  ]
 ]
}
```

## V22 Gemini の二名の本文の中の機種の申告と、登録者が確かめた機種

- 出所の主張: G1・G2
- 結果: ご意見の頭の行と登録者の言葉から引いた

```json
{
 "G1": [
  [
   7,
   "- **機種**: Gemini 1.5 Pro（依頼文・束の検分者として独立の立場で回答）"
  ]
 ],
 "G2": [
  [
   6,
   "- **機種**: Gemini 2.5 Pro（2026年9月時点の最新環境）"
  ]
 ],
 "registrant": [
  [
   3,
   "南無汝我曼荼羅。弥勒如来さん、慈悲深いお答えに感謝いたします🙏Gemini 3.8 Flash 二名（いずれも、回答での申告は、「Gemini 1.5 Pro」「Gemini 2.5 Pro」となっていますが、モデル名はGemini 3.8 Flashが正しいです。Google AI Studio のモデル選択で私が確認済み）とclaude.aiのClaude Opus 5.5 二名から以下のとおり検分をしていただきました。ご確認をして"
  ]
 ]
}
```

## V23 露出の候補の行（結果の見込みに当たりうる語を含む行・コーディネータが読んで判断する）

- 出所の主張: 四名
- 結果: 候補を引いた（判断は採否の案）

```json
{
 "G1": [
  [
   19,
   "その上で、凍結の前に確認・検討しておくべき潜在的な留意点、および合成データ検証の盲点について、以下の通り所見をまとめます。結果の見込みや特定の行への評価は一切含んでいません。"
  ],
  [
   227,
   "- 本物の Qwen3-4B-Instruct-2507 の重みを用いた順伝播・逆伝播・対数オッズ計算（予想封印前のため一切行っていません）。"
  ]
 ],
 "G2": [
  [
   11,
   "本意見伺いにおける制約（本物の模型で全経路の効き目を計算しないこと、結果の見込みを記載しないこと）を厳格に遵守し、提示されたコード、正本、設計事実、および過去の裁定記録に基づいて、静的コード解析および数式・制御フローの突き合わせを行いました。"
  ],
  [
   104,
   "4. 予想項目の `q4`, `q5` も門の行が残らない場合は `None`（判定不能・採点除外）となります。"
  ],
  [
   147,
   "依頼文の指示（「予想の封印前であるため全経路の効き目を計算しないこと」「結果の見込みを書かないこと」）を厳格に守り、本物の重みを用いた実行および結果の予測・見込みの算出は一切行っていません。"
  ]
 ],
 "C1": [
  [
   7,
   "- **情報状態**: 読んだのは束（一通版）だけで、リポジトリは開いていません（`prelim/`・`results/prelim-*` を含む）。順伝播は、本物の模型でも乱数の模型でも一度も走らせていません。この場には torch と重みの置き場がありません。結果の見込みは書きません。"
  ],
  [
   140,
   "- `p_equal_tailed`（同じ値は両方の裾に数える）、Holm（p が段を下回ったら通し、通らない所で止める。段の数は外した後の行の数）、裾、側の三つと四分位の扱い、は正本どおりです。"
  ]
 ],
 "C2": [
  [
   9,
   "- 結果の見込みは書いていません。下に出てくる割合は、乱数の数の上で器の決まりがどうふるまうかを示すものです。本物の値の見込みではありません。"
  ]
 ]
}
```

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
