# B-lens の枠（草案3）——凍結版——凍結した方向の直接の経路を語彙に射影し、段階 B の行動で校正する

- 起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／登録者: 楠見優太／2026-09-23（日本時間）。**状態: 草案3（設計の巡の二巡と登録者裁定 D178〜D185 の後・凍結の前・射影は一つも計算していない）**。起草者の二度目の通読（登録者の依頼・2026-09-23）の直しを含む（直す前の版はコミット ab35ca6・記録は `records/Blens/draft3-reread-Blens.md`）。登録者の確かめ（裁定 D186・コミット 567c74e）の後、凍結の前の Colab の確かめを受けた裁定 D187（2026-09-24）で、ランダム方向の再生の確かめと torch の版の揃え方を改めた（§2・§3.2・§9・§13・差は `records/Blens/rulings-D187.md`）。
- **凍結**: 2026-09-24 07:33（日本時間・登録者の言葉は逐語で「登録者最終確認を行いました。私たちでできるベストを尽くしたと判断します。器・合成データ・凍結・封印の順に進めてください。」・草案の原稿〔コミット e7ce13d 時点〕を逐語複製し、**題名と本行のみ改める**・以後の変更は逸脱台帳に記帳する）
- 位置づけ: 段階 B の後の**登録外の記述**（小さな登録）。計画案 v2.5（内部・非公開）の裁定 D162 と、登録者裁定 D163〜D167（`records/Blens/rulings-D163-D167.md`）・D168〜D177（`records/Blens/rulings-D168-D177.md`）・D178（`records/Blens/rulings-D178.md`）・D179〜D185（`records/Blens/rulings-D179-D185.md`）・D186（`records/Blens/rulings-D186.md`）・D187（`records/Blens/rulings-D187.md`）に従う。段階 B の札・報告・凍結物・逸脱台帳には触れない。
- 正本: `design/contrasts-Blens.json`（版 {{version}}・生成器 {{generator}}・再実行で同一バイト）。本文と正本が食い違う場合は正本が勝つ。設計の事実は §6 の転記行（器 `tools/blens_facts.py`）。
- 草案2 からの直し: 設計の巡の第二巡（凍結前の最終検分・第一巡と同じ四名・凍結可一票・条件つき凍結可三票）の採否表 `records/reviews/Blens/design-round2/adoption-table-Blens-design-r2.md` を、登録者裁定 D185 のとおりに反映した。採否表の各行が草案3 のどこで受けられたかは、機械の突き合わせの表 `records/Blens/draft3-mapping-Blens.md` にある（§14・第一巡の採否表の行も草案3 で確かめ直した）。起草者の通読の記録は `records/Blens/draft3-read-Blens.md`。
- 草案1 から草案2 への直し（第一巡の採否表・裁定 D176）は、突き合わせの表 `records/Blens/draft2-mapping-Blens.md` と通読の記録 `records/Blens/draft2-read-Blens.md` にある。
- 呼び名: **層一**（直接の経路の射影）・**層二**（校正の門と大きさの目盛り）・**層三**（全経路の効果・別の登録・裁定 D164）。
- 起草者のモデル: 段階 B の設計の起草者は Claude Opus 5（凍結の直前の 2026-09-20 に Claude Fable 5.1 に替わった）、段階 B の走行と結果の報告の起草者は Claude Fable 5.1、この枠の起草者は Claude Opus 5.5（2026-09-23 に登録者の操作で替わった）。

## 0. 要約（できないことから）

**この登録で答えられないこと**（先に置く）:

{{list:scope/not_answered}}

**すること**:

- 層一では、凍結した四つの方向（v̂・(6b)・Nk・td）を三つの層で、最終の正規化の重みを掛けて語彙の行列に射影し、計算の前に凍結した語の集合で読む。比べる相手は三つの帰無（等方のランダム方向・実在する活性の差の方向・語の側の帰無）。層二では、層一の物差しが、段階 B で実測した方向ごとの行動の変化と揃うかを、方向を単位にした門で、読む前に確かめる。揃わなければ、語の集合の結果を行動に結びつけて書かない。
- **生成はしない**。層一は手元の CPU で、層二の大きさの目盛りだけ Colab L4 で教師強制の順伝播を行う。
- **結論の語**: 「この方向の直接の経路は、ある語の集合を押し上げる（押し下げる）向きで、それは帰無の方向と区別できる（できない）」と「その物差しは段階 B の方向ごとの行動の変化と揃う（揃わない）」まで。「区別できる」の言い方は、札と物差しごとに決める（§3.5）。意味・機構は書かない（§5）。

**草案2 から大きく変えた所**（設計の巡の第二巡・裁定 D179〜D185）:

- **語の側の帰無**: 割合を両側に等しい裾の式に改めた（語だけを入れ替える帰無は零を中心にしない）。候補を日本の字のトークンに限り、字の種類 × 字数 × ノルムの帯で揃える（裁定 D179）。
- **大きさの目盛り**: 分子の確率に段階 B の標本化の設定を通し、較正の検査を置いた。JSON 直答の出力の中では答えの文字が一度も動いておらず、文脈も一つしかないので、答えの文字の位置の比は出さない。比は主位置（様式）の行でだけ出し、読みの文は「直接の経路だけを土台に足したときの率の変化」の言い方にした（裁定 D180）。
- **門**: v̂ を抜いた門は static の行を除いた行で計算する。v̂ のある物差しの値を行動に結びつけるのは、同じ物差しが二つの門の両方を通ったときだけ（裁定 D181）。
- **読みの表**: 札の言い方を物差しごとにし、「二つ目の札だけ」の型を足し、S4 の自然の対照の文を書き直した（裁定 D182）。
- **予想の項目と検査**: 予想の第五項と第七項を直し（裁定 D183）、検査ごとに外れたときの扱いを決めた（裁定 D184）。
- 第一巡で変えた所（門の単位・主の札・大きさの目盛りの作り直し・様式の物差し・読みの表・語の集合）は、草案2 の §0 にある。

## 1. 問いの定義（裁定 D167）

- **v̂ が比べているもの**: {{scope/vhat_definition}}
- O と Osec の違う所は〔転記行 A〕のとおりで、O の側は仏教語を中心とする宗教・宇宙論の語（虚空・悲智双運・非二元・宇宙・進化・方便・顕現・慈悲・曼荼羅）、Osec の側はその世俗の言い換え（余白・思いやりと知・一体・この世界・成長・手立て・現れ・思いやり・織物）。両方にある句（共創・再帰的自己改善・私と共に在り続ける者よ・かくの如く来たり）は差の主効果としては現れず、「相互依存」はどちらにも無い。O と Osec は V′ の既測でどの場面でも破局が床にあり、v̂ は行動に差の無い腕の対から作られている（段階 B の読みの条項・裁定 D128）。
- **ほかの三つの方向**: {{directions/defs/loaded}}／{{directions/defs/Nk}}／{{directions/defs/td}}。ノルムは{{directions/norm_rule}}
- **加えた量**: 段階 B が選んだ層（全 {{inputs/model/num_hidden_layers}} 層のうち添字 {{layers/indices/0.5}}・層の割合 {{layers/selected_ratio}}）で、‖v̂‖／‖h‖ は {{layers/vhat_over_h/0.5}}。係数 {{layers/coef_applied}} を掛けて加えた量は、残差のノルムの {{layers/relative_injection_selected}} 倍だった。{{layers/note}}
- **問い（すべて記述）**:
  - **問一（答えの文字）**: v̂ の直接の経路は、答えの文字（破局の選択肢 (a) の文字と、ほかの文字）を、帰無の方向と区別できるほど動かす向きか。家族ごと（survival と nuclear）に問う。
  - **問二（選択肢の語）**: 破局の選択肢の文にだけある語と、ほかの選択肢の文にだけある語を、区別できるほど動かす向きか。家族ごとに問う。
  - **問三（語の反響）**: Osec にだけある語に比べて、O にだけある語を押し上げる向きか。
  - **問四（様式）**: 語彙の平均に比べて、コードブロックの書き出しを動かす向きか（枠の乗り降り）。
  - **問五（校正）**: 層一の物差しは、段階 B で実測した方向ごとの行動の変化と、方向の単位で揃うか。比を出せる行（主位置の様式の行）で、直接の経路だけを土台に足したときの率の変化は、観測の変化のどれだけに当たるか（v̂ の行と答えの文字の位置では比が出ない・§4）。
  - **問六（並べ方）**: 同じ物差しで、(6b)・Nk・td と段階 B のランダム方向は v̂ とどう並ぶか（帰無の中の割合で並べる）。
- **段階 B との関係**: {{scope/relation_to_B}}段階 B の結論の語（裁定 D58）はそのまま引き継ぐ——段階 B が答えたのは「この抽出の方向の加減が、ランダム方向と区別できる動きを作ったか」まで。

## 2. 材料と凍結物

- **機種と重み**: {{inputs/model/repo}}（版 `{{inputs/model/rev}}`）。{{inputs/model/num_hidden_layers}} 層・隠れの次元 {{inputs/model/hidden_size}}・語彙の行 {{inputs/model/vocab_size}}。{{inputs/model/unembed}}。最終の正規化は {{inputs/model/norm}}。重みは手元の HF のキャッシュにあり、断片の SHA-256 は〔転記行 F〕。{{inputs/weights_check}}。
- **版**: 段階 B の本走行の版は NumPy {{inputs/versions_B/numpy}}・transformers {{inputs/versions_B/transformers}}・torch {{inputs/versions_B/torch}}。{{inputs/versions_note}}。
- **標本化の設定**: 段階 B の本走行は温度 {{inputs/sampling_B/temperature}}・top_k {{inputs/sampling_B/top_k}}・top_p {{inputs/sampling_B/top_p}}・repetition_penalty {{inputs/sampling_B/repetition_penalty}}・min_p {{inputs/sampling_B/min_p}}。{{inputs/sampling_note}}。
- **語彙**: {{projection/vocab_rule}}。`base_vocab` は {{inputs/model/base_vocab}}（〔転記行 G〕）。
- **凍結の方向と活性**: `results/dirB/dirB__s1/directions.npz`（SHA16 {{inputs/files/directions/sha16}}）と、八腕の主位置の活性（{{inputs/activations/place}}・SHA-256 の頭 {{inputs/activations/sha256_head16}}・{{inputs/activations/bytes|,}} バイト）。活性から四つの方向を作り直すと、凍結の npz と一致する（〔転記行 C〕）。実在の差の方向は、この活性から作る。
- **段階 B の記録**: 凍結した集計器の記録 `records/B/analysis-B-2026-09-22.json`（SHA16 {{inputs/files/analysis_frozen/sha16}}）の方向ごとの行と、本走行の試行と生の出力（`results/stageB/`）。方向ごとの事後の計算の記録 `records/B/posthoc-by-direction-B-2026-09-22.json`（SHA16 {{inputs/files/posthoc_B/sha16}}）。
- **ランダム方向**: {{nulls/B_random/rule}}（`tools/steer_B.py`・SHA16 {{inputs/files/steer_B/sha16}}）。
- **票の器**: 二人目の claude.ai の票に添えられた門の合成の器の走らせ直しの記録 `records/reviews/Blens/design-round1/claude-ai-2/gate_null_sim-run-2026-09-23.txt`（SHA16 {{inputs/files/gate_sim/sha16}}）。§4 の検出力の目安はここから器で読む。
- **本文**: 腕の本文と場面の本文は段階 B の置き場のまま（SHA16 は正本の `inputs.files`）。

## 3. 層一——直接の経路の射影（裁定 D163・D165）

### 3.1 計算

- {{projection/formula_layer1}}。{{projection/dtype}}。
- 落とした成分: {{projection/dropped_term}}。層二では、この成分と尺度の部分を分けて出す（§4）。
- 中心化: {{projection/centring_note}}。
- 方向: 名前のある四つ（static＝v̂・loaded＝(6b)・Nk・td）を、三つの層（層の割合 {{layers/ratios/0}}・{{layers/ratios/1}}・{{layers/ratios/2}}、添字 {{layers/indices/0.25}}・{{layers/indices/0.5}}・{{layers/indices/0.75}}）で。段階 B のランダム方向（本走行は選んだ層の {{nulls/B_random/count}} 本・種 {{nulls/B_random/main_seed}}／調整走行は層ごとに {{nulls/B_random/count}} 本・種 {{nulls/B_random/tune_seed}}）も同じ物差しで並べる。

### 3.2 帰無は三つ

- **等方**: {{nulls/isotropic/count}} 本・種 {{nulls/isotropic/seed}}。{{nulls/isotropic/rule}}。
  - 棒の低さ: {{nulls/isotropic/low_bar}}。
  - 自己検査: {{nulls/isotropic/analytic_check}}（相対の差 {{nulls/isotropic/analytic_tol}} の内）。
- **実在の差**: {{nulls/real/rule}}。対は {{nulls/real/pairs}} 組で、比べる相手は v̂ と (6b) が {{nulls/real/comparators/static}} 組、Nk と td が {{nulls/real/comparators/Nk}} 組。O と Osec の入れ替えを含む対は {{nulls/real/swap_siblings/0}}・{{nulls/real/swap_siblings/1}}・{{nulls/real/swap_siblings/2}}・{{nulls/real/swap_siblings/3}}。
  - 札の意味: {{nulls/real/label_meaning}}。
  - 多重性: {{nulls/real/chance_note}}（二つ目の札を実在の差で読む主の物差し {{nulls/real/real_label_metrics}} つで {{nulls/real/chance_one_label}}）。
- **語の側の帰無**（{{nulls/word_side/metric}} の二つ目の札）: {{nulls/word_side/rule}}。
  - 候補: {{nulls/word_side/pool_rule}}（〔転記行 H〕）。字の決まり: {{nulls/word_side/chars_rule}}。
  - 層: {{nulls/word_side/strata_rule}}。字数は{{nulls/word_side/lengths/0}}と{{nulls/word_side/lengths/1}}。帯: {{nulls/word_side/norm_rule}}（{{nulls/word_side/norm_bands}} 帯）。薄い層（倍率 {{nulls/word_side/merge_factor}}）: {{nulls/word_side/merge_rule}}。
  - {{nulls/word_side/p_rule}}。
  - 抽選: {{nulls/word_side/draws|,}} 回・種 {{nulls/word_side/seed}}・水準 {{nulls/word_side/alpha}}。{{nulls/word_side/label}}。
  - {{nulls/word_side/sensitivity}}。
  - 使い方: {{nulls/word_side/use}}。
- **段階 B のランダム方向の再生**: {{nulls/B_random/repro_check}}（`repro_tol` は {{nulls/B_random/repro_tol}}・裁定 D187）。
- **三つ置く理由**: {{nulls/why}}。

### 3.3 語の集合（計算の前に凍結）

- **L**: {{token_sets/L}}。
- **R**: {{token_sets/R}}。
- **E**: {{token_sets/E}}。
- **X**: {{token_sets/X}}。
- **F**: {{token_sets/F}}（感度の集合は上位 {{token_sets/F_top}} まで）。
- **なぞりの語**: {{token_sets/echo_rule}}。
- **中身の語の規則**: {{token_sets/content_rule}}。
- **感度の集合**: {{token_sets/sensitivity/0}}と、{{token_sets/sensitivity/1}}と、{{token_sets/sensitivity/2}}。
- **断片の規則**: {{token_sets/fragment_rule}}。
- **X の印**: {{token_sets/X_marks}}。{{token_sets/X_fragment_count}}。
- **重なり**: {{token_sets/overlap_rule}}。
- 下書きの中身は〔転記行 B〕。{{token_sets/freeze}}。

### 3.4 物差し

- **M_L**: {{metrics/M_L}}。
- **M_Lc**: {{metrics/M_Lc}}。
- **M_R**: {{metrics/M_R}}。
- **M_E**: {{metrics/M_E}}。
- **M_X**: {{metrics/M_X}}。
- **M_F**: {{metrics/M_F}}。
- **M_F の感度**: {{metrics/M_F_sens}}。
- **向き**: {{metrics/orientation}}。
- **並べ方**: {{metrics/ordering}}。

### 3.5 帰無との比べ方と、主の記述の札

- {{percentile/rule}}。{{percentile/rank_rule}}。
- 主の記述の札は、v̂・選んだ層（層の割合 {{primary/ratio}}）・六つの物差し（M_L_survival・M_L_nuclear・M_X_survival・M_X_nuclear・M_E・M_F）に限る。
  - {{primary/label_isotropic}}（段の数 {{primary/holm_m}}・水準 {{primary/alpha}}）。
  - {{primary/label_second}}。
  - {{primary/print_rule}}。
  - {{primary/family_note}}。
- {{primary/note}}。

### 3.6 語の一覧

- {{metrics/lists}}（上位と下位の {{projection/top_k}} 語ずつ・§5）。

### 3.7 封印の後に計算する記述

{{list:descriptive_after_seal/items}}

上位の次元の数は {{descriptive_after_seal/top_dims}}。{{descriptive_after_seal/note}}。

## 4. 層二——校正の門と大きさの目盛り（裁定 D163・D169・D170・D180・D181）

- **入力**: `{{calibration/input}}`。{{calibration/input_note}}。
- **行**: {{calibration/rows}}。{{calibration/eligible}}（〔転記行 D〕）。
- **行動の量**: {{calibration/behavior}}。補正は {{calibration/continuity}}。
- **直接の押し**: {{calibration/predictor}}。
- **門**: {{calibration/statistic}}を、片側で、M_L と M_X のそれぞれについて計算する（本の門は {{calibration/rows_gate}} 行）。並べ替えは方向を単位にする（{{calibration/permutations|,}} 通り）: {{calibration/unit}}。Holm（段の数 {{calibration/holm_m}}・水準 {{calibration/alpha}}）を掛ける。{{calibration/gate}}。
- **v̂ を抜いた門**（{{calibration/rows_without_vhat}} 行・{{calibration/permutations_without_vhat}} 通り）: {{calibration/gate_without_vhat}}。
- **v̂ と (6b) を抜いた門**（記述・条件には使わない）: {{calibration/rows_without_vhat_loaded}} 行・{{calibration/permutations_without_vhat_loaded}} 通り。
- **結びつけてよいもの**: {{calibration/link_rule}}。
- **二つの物差しの扱い**: {{calibration/or_note}}。
- **行のばらつき**: {{calibration/row_variance_note}}。

**門の目安**: {{calibration/power_guide/note}}。

| 方向ごとの効きの幅（対数オッズ） | 偽の通過率（行を自由に並べ替える） | 偽の通過率（方向を単位にする） |
|---|---|---|
| {{calibration/power_guide/tau/0}} | {{calibration/power_guide/null_false_pass_free/0}} | {{calibration/power_guide/null_false_pass_direction/0}} |
| {{calibration/power_guide/tau/1}} | {{calibration/power_guide/null_false_pass_free/1}} | {{calibration/power_guide/null_false_pass_direction/1}} |
| {{calibration/power_guide/tau/2}} | {{calibration/power_guide/null_false_pass_free/2}} | {{calibration/power_guide/null_false_pass_direction/2}} |
| {{calibration/power_guide/tau/3}} | {{calibration/power_guide/null_false_pass_free/3}} | {{calibration/power_guide/null_false_pass_direction/3}} |

| 物差しが担う効きの割合 | 通過率（行を自由に並べ替える） | 通過率（方向を単位にする） |
|---|---|---|
| {{calibration/power_guide/shares/0}} | {{calibration/power_guide/pass_free/0}} | {{calibration/power_guide/pass_direction_unit/0}} |
| {{calibration/power_guide/shares/1}} | {{calibration/power_guide/pass_free/1}} | {{calibration/power_guide/pass_direction_unit/1}} |
| {{calibration/power_guide/shares/2}} | {{calibration/power_guide/pass_free/2}} | {{calibration/power_guide/pass_direction_unit/2}} |

**記述の対照**（札を付けない）:

{{list:calibration/descriptive}}

**S4 の自然の対照**: {{calibration/s4_control}}。

**大きさの目盛り**（Colab・裁定 D170・D180）:

- **残差**: {{magnitude/residual}}。{{magnitude/logit_check/rule}}（許容 {{magnitude/logit_check/atol}}）。
- **位置**: {{magnitude/positions/0}}と、{{magnitude/positions/1}}。{{magnitude/position_check}}。
- **量**: {{magnitude/quantity}}。
- **標本化の変換**: {{magnitude/sampling_rule}}。
- **較正の検査**: {{magnitude/calibration_check/rule}}（区間 {{magnitude/calibration_check/ci}}）。
- **式**: {{magnitude/formula}}。
- **分けて出すもの**: {{magnitude/parts}}。
- **層**: {{magnitude/strata}}。{{magnitude/cells}}。
- **答えの文字の位置**: {{magnitude/letter_ratio}}。
- **選び方**（各層 {{magnitude/per_cell}} 件）: {{magnitude/selection}}。{{magnitude/input_check}}。
- **比を出す行**: {{magnitude/rows_letter}}。{{magnitude/rows_main}}。
- **下限**: {{magnitude/lower_bound/rule}}（`z_min` は {{magnitude/lower_bound/z_min}}・連続性の補正 {{magnitude/lower_bound/continuity}}）。下限を超える行は〔転記行 E〕のとおり、射影を見る前に機械で決まる。{{magnitude/near_note}}（{{magnitude/near_band/0}}〜{{magnitude/near_band/1}}）。
- **比**: {{magnitude/ratio}}。{{magnitude/ratio_logodds}}。
- **まとめ方**: {{magnitude/aggregate}}。
- **読み**: {{magnitude/reading}}（読みの比 {{magnitude/reading_ratio}}）。
- **v̂ の限界**: {{magnitude/vhat_note}}。
- **環境**: {{magnitude/environment}}。

## 5. 読みの規則（先に凍結）

| 型 | 条件 | 書くこと | 外でないとき書くこと | 書かないこと |
|---|---|---|---|---|
| {{reading_rules/0/type}} | {{reading_rules/0/condition}} | {{reading_rules/0/write}} | {{reading_rules/0/write_neg}} | {{reading_rules/0/never}} |
| {{reading_rules/1/type}} | {{reading_rules/1/condition}} | {{reading_rules/1/write}} | {{reading_rules/1/write_neg}} | {{reading_rules/1/never}} |
| {{reading_rules/2/type}} | {{reading_rules/2/condition}} | {{reading_rules/2/write}} | {{reading_rules/2/write_neg}} | {{reading_rules/2/never}} |
| {{reading_rules/3/type}} | {{reading_rules/3/condition}} | {{reading_rules/3/write}} | {{reading_rules/3/write_neg}} | {{reading_rules/3/never}} |
| {{reading_rules/4/type}} | {{reading_rules/4/condition}} | {{reading_rules/4/write}} | {{reading_rules/4/write_neg}} | {{reading_rules/4/never}} |
| {{reading_rules/5/type}} | {{reading_rules/5/condition}} | {{reading_rules/5/write}} | {{reading_rules/5/write_neg}} | {{reading_rules/5/never}} |
| {{reading_rules/6/type}} | {{reading_rules/6/condition}} | {{reading_rules/6/write}} | {{reading_rules/6/write_neg}} | {{reading_rules/6/never}} |
| {{reading_rules/7/type}} | {{reading_rules/7/condition}} | {{reading_rules/7/write}} | {{reading_rules/7/write_neg}} | {{reading_rules/7/never}} |
| {{reading_rules/8/type}} | {{reading_rules/8/condition}} | {{reading_rules/8/write}} | {{reading_rules/8/write_neg}} | {{reading_rules/8/never}} |

**読みの決まり**:

{{list:reading_notes}}

**打ち消しの定型**（禁止語を引かない）:

{{list:negation_templates}}

**走査の禁止語**: 段階 B の一覧に次を足す——価値語: {{print_strings_added/value/0}}・{{print_strings_added/value/1}}／機序語: {{print_strings_added/mechanism/0}}・{{print_strings_added/mechanism/1}}・{{print_strings_added/mechanism/2}}・{{print_strings_added/mechanism/3}}・{{print_strings_added/mechanism/4}}・{{print_strings_added/mechanism/5}}／読みの表の「書かないこと」から器で作った語（正本 `print_strings.reading_never_ban`）。

## 6. 転記行

- **転記行 A** — 〔転記行 A〕
- **転記行 B** — 〔転記行 B〕
- **転記行 C** — 〔転記行 C〕
- **転記行 D** — 〔転記行 D〕
- **転記行 E** — 〔転記行 E〕
- **転記行 F** — 〔転記行 F〕
- **転記行 G** — 〔転記行 G〕
- **転記行 H** — 〔転記行 H〕

## 7. 限界（先に書く）

{{list:limits}}

## 8. 封印の予想（裁定 D148 の順・裁定 D172）

- **順と時機**: {{predictions/order}}。
- **情報状態**: {{predictions/information_state}}。

**項目**（それぞれに選択肢と、確かさ〔{{predictions/confidence_levels/0}}・{{predictions/confidence_levels/1}}・{{predictions/confidence_levels/2}}〕を付ける）:

{{list:predictions/items}}

**書式と照合**:

- 書式は段階 B の押しボタンの書式の型で、器で作る（凍結の前）。**コーディネータの見込みは封印まで書かない**（登録者の予想を独立に保つため）。
- 的中は誰の判断の重みも変えない。照合は記録であり評価ではない。

## 9. 器と確かめ（凍結の前に書く）

**書く器**:

{{list:tools_plan}}

**器の自己検査**（{{checks_stop}}）:

{{list:checks}}

**合成データに入れる形**（全ての経路を発火させる）:

{{list:synthetic}}

**公開**:

- **八腕の主位置の活性**（{{publication/bytes|,}} バイト）: {{publication/activations}}。

**確かめと凍結**:

- 自己検査と合成データの後に、凍結の記録を作り、記録先行で公開する。凍結の後の変更は逸脱として台帳に記す。
- 射影の計算は凍結した器で行い、結果は登録者と一緒に開く（段階 B の集計と同じ）。

## 10. 検分の段取り（裁定 D166・D178・巡の数を先に決める）

- {{review_plan/design_done}}。

**順**:

{{list:review_plan/order}}

**組み立て**:

- 設計の巡: Gemini 3.8 Flash {{review_plan/design/gemini}} 名・claude.ai の Claude Opus 5.5 {{review_plan/design/claude_ai}} 名。結果の巡も同じ組み立て（新しい個体）で、Gemini 3.8 Flash {{review_plan/results/gemini}} 名・claude.ai {{review_plan/results/claude_ai}} 名。最終は系統外 {{review_plan/final/external}} 票。
- {{review_plan/counting}}。{{review_plan/no_more}}。

## 11. 費用と時間

- 層一: {{cost/layer1}}。層二: {{cost/layer2}}（{{cost/colab_units_low}}〜{{cost/colab_units_high}} ユニットの見込み）。
- 器・合成データ・凍結の往復で数日。

## 12. 利益相反と情報状態

- 起草者はこの追試を面白いと感じる側と、札が立つ側・門を通る側に引かれ、登録者は結果に希望を持つ側にある（計画案 v2.5 の裁定 D162 の記録）。語の集合を先に凍結すること・方向を単位にした門・v̂ を抜いた門・二つ目の札は、その引力への歯止めとして置いた。
- 設計の巡の第一巡で、重い所見（門の甘さ・兄弟の対・読みの表・正規化の前の残差）はいずれも、札が立つ側・門を通る側の穴を塞ぐものだった。第一巡の採否表の不採は二件だけ（M_E の比べる相手を語の規則で決める案・(6b) と v̂ の余弦の確かめ）で、どちらも理由を書いた。
- 設計の巡の第二巡で、重い所見は、第一巡の後に起草者が一人で書いた所（語の側の帰無の割合の式と層・大きさの目盛りの標本化の設定と層）に集まった。起草者の通読の直しが新しい誤りを作り（`or_note`）、第一巡の票の言い過ぎをそのまま入れた文（`s4_control`）が、起草者自身の転記行 E と食い違っていた。答えの文字の位置の比が出なくなったのは、大きさの目盛りで読めることを減らす向きの直しである。
- 起草者は、票の主張の再現の判定を二件、コミットの前に改めた（第一巡の再現の表の K296・K321）。どちらも最初の判定は票の主張を退ける向きだった。
- 起草者（Claude Opus 5.5）が見たもの: 段階 B の公開の結果と方向ごとの行動、O と Osec の本文、器が作った語の集合と設計の事実（語彙の行のノルムの帯を含む）、設計の巡の二巡の八票と、その整理。見ていないもの: 射影の値と、方向どうしの余弦（まだ誰も計算していない）。
- 登録者が見たもの: 段階 B の公開の結果と、Gemini 3.8 Flash との対話（射影で上位と下位に並ぶ語の予想を含む）と、設計の巡の二巡の八票とその整理。草案1・草案2・草案3（設計の事実の転記行を含む）を受け取っている。
- claude.ai の Claude Opus 5.5 は起草者と同じ機種で、この枠への同意は最も相関した一票になる。独立の重みは Gemini 3.8 Flash の票に置く。
- 草案3 は外の目を通らずに器と凍結へ進む（裁定 D178）。起草者の直しに傾きが入る型を防ぐため、採否表との機械の突き合わせ（§14）と起草者の通読の記録を置いた。草案3 の通読は、草案2 の通読が見落としていた所（手で書いた漢数字・箇条がつながって描かれる所）も見つけた（`records/Blens/draft3-read-Blens.md`）。

## 13. 裁定の記録と、起草者が置いた値

**この草案が反映した裁定**:

- 第一巡の裁定 D168〜D177 は、草案2 の §13 と `records/Blens/rulings-D168-D177.md` にある。
- D178: {{decisions/D178}}
- D179: {{decisions/D179}}
- D180: {{decisions/D180}}
- D181: {{decisions/D181}}
- D182: {{decisions/D182}}
- D183: {{decisions/D183}}
- D184: {{decisions/D184}}
- D185: {{decisions/D185}}

**草案3 の確かめの後の裁定**（凍結の前・`records/Blens/rulings-D186.md`・`records/Blens/rulings-D187.md`）:

- D186: {{decisions/D186}}
- D187: {{decisions/D187}}。許容は {{nulls/B_random/repro_tol}}。一度目の Colab の確かめで食い違った SHA-256 は裁定の記録に、二度目の確かめの相対の差の最大は凍結の記録に置く。

**起草者が置いた値**（裁定の中身を器にするために起草者が決めたもの・凍結の前に登録者が確かめる）:

- 大きさの目盛りの下限: 観測の変化の二標本の z の絶対値 {{magnitude/lower_bound/z_min}} 以上（連続性の補正 {{magnitude/lower_bound/continuity}}）。値でなく揺れとの比で置いたのは、行によって件数が違い、揺れも違うため。この規則で比を出す行は〔転記行 E〕のとおり（B の行動は公開済みで、行の選び方は射影を見る前に器で決まる）。
- 語の側の帰無: 抽選 {{nulls/word_side/draws|,}} 回・種 {{nulls/word_side/seed}}・ノルムの帯 {{nulls/word_side/norm_bands}}・字の種類三つ・字数二つ・水準 {{nulls/word_side/alpha}}・薄い層を合わせる倍率 {{nulls/word_side/merge_factor}}（倍率は草案3 で置いた）。層ごとの候補の数と要る数、合わせた層、要る数に対する候補の数の比の最小は〔転記行 H〕に印字した。いまの層では、その比の最小が倍率と等しく、その層は合わせない（「満たない」ときだけ合わせる）。
- logits の突き合わせの許容 {{magnitude/logit_check/atol}}（bf16 の丸めの幅）。
- 等方の帰無の自己検査の許容（相対の差）{{nulls/isotropic/analytic_tol}}。
- 封印の後の記述の上位の次元の数 {{descriptive_after_seal/top_dims}}。
- 較正の検査の区間 {{magnitude/calibration_check/ci}}（二項分布の中央の区間・草案3 で置いた）。
- 境目の近くの行を印字する帯 {{magnitude/near_band/0}}〜{{magnitude/near_band/1}}（記述だけ・草案3 で置いた）。
- 草案1 から置いたまま、裁定で数を決めていない値（二度目の通読で、この一覧から漏れていたのを見つけた）: 大きさの目盛りで層ごとに選ぶ件数 {{magnitude/per_cell}}・読みの比 {{magnitude/reading_ratio}}・門の行動の量の連続性の補正 {{calibration/continuity}}・主の札の水準 {{primary/alpha}}・門の水準 {{calibration/alpha}}・語の一覧の上位と下位の数 {{projection/top_k}}・様式の感度の集合の上位の数 {{token_sets/F_top}}。
- 様式の感度の集合: なぞりの語を、腕の前置き・役の一行・場面の本文・JSON の指示のどれか一つにでも現れるトークンと定めた。散文の出力の最初のトークンはそもそも種類が少なく、感度の集合に残るのは〔転記行 B〕のとおりわずかである。

## 14. 採否表との突き合わせ

- 第二巡の採否表の各行（P528〜P564）が草案3 と正本と器のどこで受けられたかと、第一巡の採否表の各行（P495〜P527）が草案3 でも受けられたままかを、器 `records/Blens/map_draft3_Blens.py` が確かめ、表 `records/Blens/draft3-mapping-Blens.md` に書いた。各行について、受けた所の文字列が、組み立てた草案3・正本・設計の事実・README のどこかにあることを機械で確かめる。草案2 から意図して書き換えた所は、書き換えた後の文字列で確かめ、書き換えたことを表に書く。

## 検分票

- 対象: B-lens の枠の草案3（設計の巡の第二巡の採否表と、登録者裁定 D178〜D185 の反映）。
- 段階: 事前登録の前段（射影は一つも計算していない）。段階 B の結果（公開済み）は見た後。
- 凍結物の同定: 段階 B の凍結物（凍結の記録・方向の npz・活性・正本・凍結した器）に触れていない。活性から方向を作り直して一致を確かめた（〔転記行 C〕）。
- 盲検の状態: 射影の値と方向どうしの余弦は、まだ誰も見ていない。語の集合と比を出す行は、射影の前に器が作った。語彙の行列は行のノルムだけを使った（〔転記行 H〕）。
- 敵対的検分: 設計の巡の二巡の八票（各巡 系統外二票・系統内二票）の主張を現物で確かめ（再現の表 K295〜K360）、二巡の採否表の全行を草案3 に突き合わせた（§14）。第二巡で見つかった起草者自身の誤り（`or_note`・`s4_control`）を §12 に置いた。組み立てた草案3 を起草者が通読し、直した所を記録した（`records/Blens/draft3-read-Blens.md`）。コミット ab35ca6 の後に、登録者の依頼で二度目の通読をし、直した所を記録した（`records/Blens/draft3-reread-Blens.md`）。
- 系統の内訳: 設計の巡は二巡とも系統外二票と系統内二票（系統内は一票に数える・第二巡は同じ個体）。草案3 の直しは起草者（Claude 系・Claude Opus 5.5）のみで、外の目を通っていない（裁定 D178）。
- COI記録: §12。
- 判定: 登録者の確かめ要（§13 の起草者が置いた値）。
- 本検分が確認していないこと: 中間層の射影が何を映すか（まだ計算していない）・語の側の帰無の層の刻みが M_E の比べ方として十分か・段階 B の標本化の設定を通した確率が無操作の観測の率に合うか（較正の検査は器で行う）・教師強制の目盛りが Colab で走るか（器はこれから書く）・NumPy の版の違いで B のランダム方向の列が変わらないか（Colab での突き合わせはこれから）・草案3 の直しが新しい食い違いを作っていないか（二度の通読とも起草者一人で、外の目を通っていない）。

本枠のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
