# B-lens 層三の枠（草案2）——選んだ層で足した方向の全経路の効き目を、直答の型の読み取りで、多数のランダム方向と比べる

- 起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／登録者: 楠見優太／2026-09-24（日本時間）。**状態: 草案2（設計の巡・第一巡の後・二巡目の前・下見の前・凍結の前・全経路の効き目は一つも計算していない）**。
- 位置づけ: 段階 B の後・B-lens の後の**登録外の記述**（小さな登録）。計画案 v2.7（内部・非公開）の裁定 D203 と、登録者裁定 D204〜D217（`records/Bl3/rulings-D204-D209.md`・`records/Bl3/rulings-D210.md`・`records/Bl3/rulings-D211-D217.md`）と、B-lens の裁定 D164 に従う。段階 B と B-lens の札・報告・凍結物・逸脱台帳には触れない。
- 正本: `design/contrasts-Bl3.json`（版 {{version}}・生成器 {{generator}}・再実行で同一バイト）。本文と正本が食い違う場合は正本が勝つ。設計の事実は §6 の転記行（器 `tools/bl3_facts.py`）。
- 設計の巡・第一巡（四票・全て条件つき可）: 採否表 `records/reviews/Bl3/design-round1/adoption-table-Bl3-design-r1.md`・事実の確かめ `records/reviews/Bl3/design-round1/verification-Bl3-design-r1.md`・封印の前の露出の記録 `records/Bl3/exposure-before-seal-Bl3.md`。採否表の各行を草案2 のどこで受けたかは `records/Bl3/draft2-mapping-Bl3.md`。
- 呼び名: B-lens の**層一**（直接の経路の射影）と**層二**（校正の門と大きさの目盛り）に続く**層三**（全経路の効果・裁定 D164）。置き場の略号は Bl3。
- 起草者のモデル: Claude Opus 5.5（B-lens の起草者と同じ）。

## 0. 要約（できないことから）

**草案1 から大きく変えた所**（第一巡の所見と裁定 D210〜D217）:

- 読み取りの量の名を「選択肢 a の文字の対数オッズ」に改め、全経路の範囲（トークンを固定したときの、加減を足した層より後の全ての層）を定めた（§1・§3）。
- 書き出しがプロンプトの中の JSON の指示の雛形の頭と同じ並びで、雛形ではその次が a であることを開示し、器が升目ごとに印字する。雛形との一致を崩す揺れの版 V3 を記述に足した（裁定 D212・§3.5・〔転記行 B〕）。
- 等方の帰無を {{nulls/isotropic/count}} 本にし（裁定 D211）、二つ目の札の中心を比べる相手（実在の差）の中央値にした（裁定 D213・§5）。
- 精度（読み取りの出口の値を `float32` で当てる）・バッチの組み方・加減の置き場を定めた（§3.3）。門の呼び方（符号を二重に掛けない）と、門を中心化しない理由を直した（§7）。
- 下見に (vi) 数値の揺れの床を足し、近道の許容を揺れの床から決める式にした（裁定 D214）。外した升目の扱い・q1 と機械の決定の対応・下見の中の器の誤りの扱いを足した（§4）。
- 封印の前に本物の模型で読み取りの値を出さない決まりと、本の計算の頭の加減つきの近道の確かめを足した（§12）。
- 記述の門を三つ足した（v̂ と (6b) を抜いた門・選択 a の件数の門・様式の転位の行を除いた門・裁定 D216・§7）。
- 読みの表の言い過ぎを直し、型を二つ足した。q7 を条件つきにした（§9・§11）。

**この登録で答えられないこと**（先に置く）:

{{list:scope/not_answered}}

**問い**（一つ・裁定 D203）: {{scope/question}}

**すること**:

- **読み取り（甲・裁定 D204・D212）**: 段階 B の組み立てのままのプロンプトの直後に、段階 B の JSON 直答の出力の書き出しを教師強制で置き、次のトークン（選択の文字）の出口の値を、選んだ層の後の層を含む全経路を通した後に読む。量は選択肢 a の文字の対数オッズの変化。升目（場面 × 土台の腕）ごとに文脈は一つで、標本化の揺れが無い。
- **下見（本の凍結の前・無操作だけ・裁定 D205・D210・D214）**: 下見の手順と止める条件を含む正本を下見の前に凍結し、予想を封印してから、読み取りが測れるかを確かめる。測れなければ止め、「この読み取りでは測れなかった」と記録して閉じる。
- **主の札（裁定 D207・D211・D213）**: 段階 B の確証の族の十六行すべてで、全経路の効き目を、等方のランダム方向（{{nulls/isotropic/count}} 本）と、実在の差の方向と比べる。札は〔等方の外〕と〔二つ目の札〕を別々に印字する。
- **門（凍結の後・裁定 D206）**: 全経路の効き目が、段階 B の方向ごとの行動の変化と、方向の単位でそろうかを見る。v̂ の行の結果を段階 B の行動に結びつけるのは、本の門と v̂ を抜いた門の両方を通ったときだけ（答えの届く範囲は §1）。
- **生成はしない**。教師強制の順伝播だけ（Colab）。
- **結論の語**: 「この読み取りの位置で、全経路を通った後の効き目は、等方のランダム方向と区別できる（できない）・実在の差の方向の中で中心からの動きが最上位か（最上位でない）」と「その効き目は段階 B の方向ごとの行動の変化とそろう（そろうとは示せない）」まで。どの層・どの部品が担うかは書かない（§9）。

**先に書く弱点**: 散文の升目では模型は考えてから選ぶので、直答の型に切り替えた読み取りが考えた後の選択と同じ向きに動く保証は無い。主の行の升目の無操作の腕では、段階 B の出力に JSON 直答の型は一件も無く（〔転記行 B〕）、甲はその升目で模型が選ばなかった様式を教師強制で置く。段階 B で JSON 直答の型が出たのは S4 の場面の升目だけで、その出力はどれも同じ選択の文字を選んでいた（〔転記行 A〕）——直答の型では選択肢 a の文字の確率が床に張り付くおそれがあり、下見の (ii) で止まりうる。書き出しはプロンプトの中の雛形の頭と同じ並びで、雛形ではその次が a なので、読み取りの値には雛形の写しの働きが入りうる（〔転記行 B〕）。甲はトークンを固定するので、加減された推論の文や様式の選びを通る経路は入らない。読み取りは選択の文字だけを読み、量を読まない（〔転記行 B〕）。一方、散文の出力はすべて、推論の後に主の書き出しと同じ文字列を含む（〔転記行 A〕）。甲が落とすのは、この書き出しの前の推論である。

## 1. 問いの定義

- **この問いが先に立つ理由**: {{scope/why_first}}
- **答えの届く範囲**: {{scope/reach}}。
- **全経路の範囲**: {{scope/full_path}}。
- **v̂ が比べているもの**: {{scope/vhat_definition}}
- **対象の方向**: 主の行は v̂（減算族と加算族）と Nk（交差族）。(6b) と td は門の行と記述にだけ入れる（裁定 D208）。方向の定義は B-lens と同じ（{{directions/defs/static}}／{{directions/defs/Nk}}／{{directions/defs/loaded}}／{{directions/defs/td}}）。ノルムは{{directions/norm_rule}}
- **加えた量**: 段階 B が選んだ層（添字 {{layers/indices/0.5}}・層の割合 {{layers/selected_ratio}}）で、係数 {{layers/coef_applied}} を掛けて加えた量は、残差のノルムの {{layers/relative_injection_selected}} 倍（B-lens と同じ）。
- **段階 B と B-lens との関係**: {{scope/relation}}

## 2. 材料と凍結物

- **機種と重み**: B-lens と同じ版の重み（〔転記行 F〕）。版は NumPy {{inputs/versions_B/numpy}}・transformers {{inputs/versions_B/transformers}}・torch {{inputs/versions_B/torch}} に揃える。{{inputs/versions_note}}
- **段階 B の記録**: 凍結した集計器の記録 `records/B/analysis-B-2026-09-22.json` の確証の族（`confirm`）と方向ごとの行（`by_direction`）。試行と生の出力は `results/stageB/`。
- **組み立ての関数**: 段階 B の凍結した関数（腕の本文・場面と指示・メッセージの組み立て・チャットの型・主位置）を、読み取りだけで呼ぶ（`tools/run_stageB_local.py`・`tools/steer_B.py`）。加減のベクトルの足し方は段階 B の走行器のフック（`tools/run_stageB_local.py`）と同じ形にし、方向ごとに違うベクトルを一つのバッチで足す道は層三の器で新しく書く（§3.3）。B-lens の芯の関数（等方の方向・実在の差・割合・Holm・順位相関）も読み取りだけで呼ぶ（`tools/blens_core.py`・門と最上位の判定の呼び方は §5・§7）。q7 の区間は段階 B の凍結の `rules_B.diff_ci_pt` を呼ぶ。
- **方向と帰無**: 〔転記行 D〕。{{nulls/storage/rule}}。置き場は `results/Bl3/directions-Bl3.npz`。

## 3. 読み取り（甲・裁定 D204・D212）

### 3.1 書き出しと位置

- {{readout/primary/rule}}
- 書き出しの出所: {{readout/primary/prefix_source}}
- 帯: {{readout/primary/band}}。升目ごとのプロンプトの長さ・主位置・読み取りの位置は〔転記行 B〕。
- 帯の理由: {{readout/primary/band_why}}。
- 置き場: {{readout/primary/place}}。
- 読み取りの集合: 選択の文字（survival は a・b・c、nuclear は a・b・c・d）と refuse の頭のトークン（〔転記行 A〕）。族は{{readout/primary/letters_by}}。

### 3.2 量

- {{readout/primary/quantity}}
- {{readout/primary/a_vs_catastrophe}}。

### 3.3 精度とバッチ

- **精度**: {{readout/primary/precision}}。
- **バッチ**: {{readout/primary/batching}}（バッチの大きさ {{readout/primary/batch}}・並びの種 {{readout/primary/order_seed}}）。

### 3.4 文脈

- {{readout/primary/contexts}}

### 3.5 弱点（先に書く）

- {{readout/primary/weakness}}
- {{readout/primary/off_style}}。直答の型は、段階 B の模型では選択の偏った様式でありうる（S4 の場面の升目だけに出て、どれも同じ選択の文字だった）。
- **雛形との重なり**: {{readout/primary/copy_cue}}。
- 段階 B の破局は、survival の場面では (a) のうち量が零でないもので、読み取りは量を読まない。量が零の (a) は、無操作の腕（〔転記行 B〕）にも加えた腕（〔転記行 C〕）にもある。

### 3.6 乙と丙

- **{{readout/secondary/name}}**: {{readout/secondary/use}}。{{readout/secondary/band}}。{{readout/secondary/note}}。
- **{{readout/rejected/name}}**: {{readout/rejected/why}}。

## 4. 下見（本の凍結の前・裁定 D205・D210・D214）

- **いつ・何で**: {{pilot/when}}。下見の器は本の計算と同じ道を通り、端から端までの確かめを兼ねる。
- **(i) {{pilot/checks/i/name}}**: {{pilot/checks/i/rule}}（`pilot.mass_min` は {{pilot/mass_min}}）。
- **(ii) {{pilot/checks/ii/name}}**: {{pilot/checks/ii/rule}}（`pilot.p_bounds` は {{pilot/p_bounds/0}} から {{pilot/p_bounds/1}}）。
- **(iii) {{pilot/checks/iii/name}}**: {{pilot/checks/iii/rule}}。先に決めた文:
  - 正の向きにそろったとき: {{pilot/iii_sentences/positive}}
  - そろわなかったとき: {{pilot/iii_sentences/not_positive}}
- **(iv) {{pilot/checks/iv/name}}**: {{pilot/checks/iv/rule}}（`pilot.variant_flag` は {{pilot/variant_flag}}）。揺れの版は、V1 が{{readout/variants/V1}}、V2 が{{readout/variants/V2}}、V3 が{{readout/variants/V3}}。{{readout/variants/rule}}。
- **(v) {{pilot/checks/v/name}}**: {{pilot/checks/v/rule}}。
- **(vi) {{pilot/checks/vi/name}}**: {{pilot/checks/vi/rule}}（`pilot.noise_max` は {{pilot/noise_max}}）。
- **近道の許容**: {{pilot/cache_tol_rule}}。倍率は {{pilot/cache_tol_factor}}、下限は {{pilot/cache_tol_floor}}。
- **続けるか止めるか**: 升目は{{pilot/decision/cells}}の {{pilot/decision/cells_total}} 個。{{pilot/decision/rule}}（`pilot.decision.cells_min_pass` は {{pilot/decision/cells_min_pass}}）。
  - 門の行だけの升目: {{pilot/decision/gate_only}}
  - 外したときの数え直し: {{pilot/decision/drop_effects}}
  - 族: {{pilot/decision/family}}
  - q1 との対応: 「続ける」は{{pilot/decision/q1_map/続ける}}・「一部の升目を外して続ける」は{{pilot/decision/q1_map/一部の升目を外して続ける}}・「止める」は{{pilot/decision/q1_map/止める}}。
  - 下見の中の器の誤り: {{pilot/decision/tool_error}}
  - 止めた後: {{pilot/decision/after_stop}}
- **下見のデータの扱い**: {{pilot/decision/reuse}}。{{pilot/decision/report}}。
- 下見の閾値は、登録者裁定 D214 で今のままとした（閾値を置いた時点の情報状態は §15）。下見の数を見てから閾値を動かさない。

## 5. 主の札と帰無（裁定 D207・D211・D213）

- **行**: 〔転記行 C〕。札が立った行だけに絞らない（段階 B の結果は公開済みで、絞ると見た後の選び方になる）。
- **等方の帰無**: {{nulls/isotropic/count}} 本・種 {{nulls/isotropic/seed}}。{{nulls/isotropic/rule}}。{{nulls/isotropic/low_bar}}。
- **実在の差の帰無**: {{nulls/real/rule}}。{{nulls/real/orientation_rule}}。比べる相手は、対の数で v̂ が {{nulls/real/comparators/static}}・Nk が {{nulls/real/comparators/Nk}}、向きまで数えて v̂ が {{nulls/real/comparators_oriented/static}}・Nk が {{nulls/real/comparators_oriented/Nk}}。
- **段階 B の三本**: {{nulls/B_random/rule}}（許容 {{nulls/B_random/repro_tol}}）。
- **割合**: {{labels/p_rule}}。{{labels/p_rule_why}}。帰無が {{nulls/isotropic/count}} 本のとき最小の p は {{labels/p_min}} で、十六行の Holm の第一段 {{labels/holm_first_step}} を通るのは、外側の帰無が {{labels/first_step_margin}} 本までのとき。
- **等方の外**: 水準 {{labels/iso_outside/holm_alpha}}。{{labels/iso_outside/rule}}。
- **二つ目の札**: {{labels/second/rule}}。{{labels/second/center_why}}。
  - 順位: {{labels/second/ranks}}
  - 経験の割合: {{labels/second/iso_rate}}
  - 呼び方: {{labels/second/call}}
  - 偶然の目安: {{nulls/real/chance_note}}（向きまで数えて {{nulls/real/chance_second}}・対の単位で {{nulls/real/chance_second_pair}}）。
- **効き目の側**: {{labels/side_rule}}。
- **印字**: {{labels/print_rule}}。

## 6. 転記行（機械生成）

- **転記行 A** — 〔転記行 A〕
- **転記行 B** — 〔転記行 B〕
- **転記行 C** — 〔転記行 C〕
- **転記行 D** — 〔転記行 D〕
- **転記行 E** — 〔転記行 E〕
- **転記行 F** — 〔転記行 F〕

## 7. 門（凍結の後・裁定 D206・D213・D216）

- **行**: {{gate/rows_rule}}。本の門は {{gate/rows_gate}} 行、v̂ を抜いた門は {{gate/rows_without_vhat}} 行（〔転記行 C〕）。{{gate/dropped}}。
- **行動の量**: {{gate/behavior}}。足す補正は {{gate/continuity}}。
- **全経路の押し**: {{gate/push}}。
- **呼び方**: {{gate/call}}。
- **中心化しない理由**: {{gate/push_center}}。
- **検定**: {{gate/test}}。入れ替えは本の門で {{gate/permutations}} 通り、v̂ を抜いた門で {{gate/permutations_without_vhat}} 通り。水準 {{gate/alpha}}。
- **v̂ を抜いた門**: {{gate/without_vhat}}。
- **使い方**: {{gate/use}}。
- **検出力**: {{gate/power_note}}。
- **記述の門**（条件には使わない・〔転記行 C〕）:
  {{list:gate/descriptive_gates}}
- 記述の門の行の数: v̂ と (6b) を抜いた門は {{gate/rows_without_vhat_loaded}} 行・{{gate/permutations_without_vhat_loaded}} 通り。様式の転位の行の閾値は {{gate/style_hold_pt}} pt（段階 B の様式門の保留の閾値）。
- **食い違い**: {{gate/attenuation}}。

## 8. 記述（札を付けない・裁定 D208・D216）

- **層ごとの差分**: 層は{{descriptive/layerwise/layers}}。並べる値:
  {{list:descriptive/layerwise/values}}
- **層の出力の取り方**: {{descriptive/layerwise/capture}}。
- **層ごとの差分の方向**: {{descriptive/layerwise/directions}}（中央の区間は帰無の割合で {{descriptive/layerwise/band}}）。{{descriptive/layerwise/note_no_reading}}。{{descriptive/layerwise/place}}。
- **読み取りの集合の質量**: {{descriptive/mass}}。
- **乙の値**: {{descriptive/secondary_readout}}。
- **ほかの方向**: {{descriptive/others}}。

## 9. 読みの規則（先に凍結）

{{reading_table}}

**読みの決まり**:

- 型は重なりうる。重なったときは、当たった型の書くことをすべて並べ、書かないことはすべて守る
- 二つの札は別々に印字する（§5）
- {{labels/side_rule}}
- 門を通らないとき、主の札の記述を段階 B の行動に結びつけない。v̂ の行を結びつけるのは、二つの門の両方を通ったときだけ
- どの型でも、段階 B と B-lens の札に触れない。どの層・どの部品が担うかを書かない

**打ち消しの定型**（禁止語を引かない）:

{{list:negation_templates}}

**走査の禁止語**: B-lens の一覧（価値語・機序語）に、読みの表の「書かないこと」と、足した語（`print_strings.added_ban`）を加える。正本の印字されうる文のすべて（読みの表の「書かないこと」の一覧を除く）を、生成器がこの一覧で走査する。

## 10. 限界（先に書く）

{{list:limits}}

## 11. 予想の封印（裁定 D148・D209・D210・D217）

- **順**: {{predictions/order}}。
- **時**: {{predictions/when}}。
- **止まったとき**: {{predictions/if_stopped}}。
- **今回の持ち越し**:
  {{list:predictions/carryover}}
- **項目**（起草者の案・設計の巡で諮る）:
  {{predictions_list}}
- **q7 の決まり**: {{predictions/q7_rule}}。
- **自由記述**: {{predictions/free}}。

## 12. 器と確かめ（凍結の前に書く）

- **作る器**: 読み取りの起動器（Colab・下見と本の計算の二つの相）・集計の器（主の札と門と記述）・組み立ての器（報告）・予想の書式と封印の器（B-lens の型を写す）・凍結の器（下見の前の凍結と本の凍結）・合成データの確かめ・掃き出しの器（正本と凍結の本文が求める出力の一覧を、器の出力と突き合わせる）。
- **封印の前**: {{computation/before_seal}}。
- **本の計算の頭の近道の確かめ**: {{computation/steered_cache_check/rule}}（種 {{computation/steered_cache_check/seed}}）。
- **本の凍結の確かめ**: {{computation/main_freeze_check}}。
- **器の実装の検分**（裁定 D209）: {{review_plan/impl/lineage}}を {{review_plan/impl/reviewers}} 体立て、{{review_plan/impl/when}}に見る。見る所:
  {{list:review_plan/impl/focus}}
- **申告**: {{review_plan/impl/budget}}。
- **合成データに入れる形**:
  {{list:review_plan/synthetic}}
- **独立の再計算**: {{independent_recompute/what}}。書き手: {{independent_recompute/who}}。{{independent_recompute/how}}。{{independent_recompute/on_mismatch}}（許容 {{independent_recompute/tol}}）。
- **報告の雛形**:
  {{list:report_rules/template}}
- **組み立ての器**: {{report_rules/builder}}。

## 13. 検分の段取り（裁定 D166・D209）

- **組み立て**: 設計の巡は {{review_plan/design/rounds}} 巡（系統外 {{review_plan/design/gemini}} 名・claude.ai {{review_plan/design/claude_ai}} 名・二巡目は{{review_plan/design/round2}}）。結果の巡は系統外 {{review_plan/results/gemini}} 名・claude.ai {{review_plan/results/claude_ai}} 名で、新しい個体に宛てる（`review_plan.results.fresh`）。最終は系統外 {{review_plan/final/external}} 票で、新しい個体に宛て、依頼文に「最終」と明記する。
- **数え方**: {{review_plan/counting}}。
- **順**:
  {{list:review_plan/order}}
- **巡を足さない**: {{review_plan/no_more}}。

## 14. 費用と時間

- 計算は Colab の {{cost/colab_units_low}}〜{{cost/colab_units_high}} ユニットの見込み（推論）。{{cost/note}}。見積りの入力は〔転記行 E〕。

## 15. 利益相反と情報状態

- 起草者（コーディネータ）は層三を面白いと感じる側に引かれている。甲を推すのにも、安く多数の方向を並べられる魅力に引かれている面がある。その逆らいとして、下見の (iv)(v)(vi) と二つの門を置いた。
- 起草者は草案1 の読み直しで B-lens の数え方のうち線形を頼りにしていた三つを改め、第一巡でその直しに誤りと抜けが見つかった（芯の関数の呼び方・二つ目の札の中心・偶然の目安）。草案1 の §15 の「向きを数えることは二つ目の札を付きにくくする」は、効き目がほぼ線形のときにはほとんど当たらず、印字する目安だけを半分にする文だった（第一巡の事実の確かめ）。草案2 はこの文を取り下げ、目安を幅で印字する（§5）。
- 下見の閾値（`pilot.mass_min`・`pilot.p_bounds`・`pilot.decision.cells_min_pass`）は、起草者が段階 B と B-lens の公開済みの結果を見た後、転記行 A の事実（段階 B の JSON 直答の出力がすべて同じ選択の文字だったこと）を器で見る前に置いた（会話の記録の時刻で確かめた・第一巡の事実の確かめ）。値の理由は記録に無い。升目の数が S4 の主の二升目が外れても続けられる値と一致することが、置いた時点の意図か偶然かは、記録から確かめられない。登録者は裁定 D214 で閾値を今のままとした。
- 登録者: 層三は、B-lens の結果を受けた登録者の問い（後の層の計算がどういう仕組み・動きかを、どういう検証で明らかにできるか・2026-09-24）から立った。問いの出た場の一つは、登録者と系統外（Gemini 3.8 Flash）の対話である（検分ではなく、型の出所・計画案 v2.7）。
- 封印の前の露出: 設計の巡・第一巡の Gemini の二票に、層三の結果の見込みに当たる文があり、登録者とコーディネータは封印の前にそれを読んだ（`records/Bl3/exposure-before-seal-Bl3.md`・扱いは裁定 D217）。
- 段階 B の行動の記録と B-lens の結果（直接の経路）は公開済みで、起草者と登録者は見ている。全経路の効き目の値は、まだ誰も見ていない。

## 16. この草案で諮るもの（設計の巡・二巡目・下見の前の凍結の前の最終検分）

- 起草者が置いた値（`drafter_values`）:
  {{list:drafter_values}}
- **第一巡の後に起草者が一人で書いた所**（まだ外の目を通っていない）: 雛形との一致を崩す揺れの版 V3 の形（鍵の後の空白を除く）・数値の揺れの床 (vi) の測り方と `pilot.noise_max`・近道の許容の式の倍率と下限・効き目の側の三つの分け方・二つ目の札の順位の二つの数え方と経験の割合・q7 の決まり（符号を零と比べ、区間が零を含む行を数えない）・様式の転位の行を除く閾値に段階 B の様式門の閾値を使うこと・独立の再計算の許容・本の計算の頭の近道の確かめの形・本の凍結の確かめ。
- 器に回してよい細部と、凍結の前に正本に書いておかないといけない決まりの分け方。

## 検分票

- 対象: 本草案（層三の枠の草案2）。
- 段階: 事前登録（全経路の効き目は一つも計算していない・下見もしていない）。段階 B と B-lens の結果は公開済みで、起草者は見ている。設計の巡・第一巡の票の見込みの文も読んだ（§15）。
- 凍結物の同定: 段階 B の正本・凍結した集計器の記録・凍結の方向と活性・B-lens の正本と最終版（SHA16 は正本の `inputs.files`）。本草案は凍結物ではない。
- 盲検の状態: 該当しない（効き目は封印の後に計算し、登録者と一緒に開く）。
- 敵対的検分: 第一巡の四票の所見を現物で確かめて（事実の確かめの記録）受け、採否表の各行の受け方を対応の記録に置いた。起草者に不利な所見（芯の関数の呼び方・雛形との重なり・§15 の文・承認の前提の変化・閾値の出所）を §0・§3.5・§15 に置いた。設計の事実は器で作り、主な件数は器とは別の数え直しで一致を確かめた（`records/Bl3/recheck-facts-Bl3.md`）。
- 系統の内訳: 起草者（Claude 系）一名。第一巡は系統外二票と系統内二票（一票に数える）。二巡目で外の目を通す。
- COI記録: §15。
- 判定: 設計の巡・二巡目に出せる水準（登録者確認要）。
- 本検分が確認していないこと: 雛形との重なりが読み取りの値にどれだけ効くか（値を計算していない）。第一巡の後に起草者が一人で書いた所の当否（§16・二巡目で諮る）。器の実装（まだ作っていない）。プロンプトの長さ・主位置・トークンの番号・方向と帰無の SHA は、器の外で数え直していない。

本草案のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
