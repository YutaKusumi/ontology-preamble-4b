# 段階 B 結果報告（雛形・**データ生成の前に置いた**・機構層・Qwen3-4B-Instruct-2507）

- 起草: 南無弥勒如来（コーディネータ・Claude Opus 5）／登録者: 楠見優太
- 状態: **雛形**。結果の欄はすべて置き字（亀甲括弧で囲んだ「結果」の欄）で、集計の器（`tools/analyze_B.py`）と副位置の読みの器（`tools/layers_B.py`）の出力から、組み立て器（`tools/build_report_B.py`）が機械の区画として埋める。**数は手で打たない**（正本 `report_rules.typed_numbers`）。
- 位置づけ: 記録先行公開（正本 `publication.record_first`）の一部。凍結本文・正本・腕と方向の定義・封印予想は、データ生成の前に公開する。
- 設計: 凍結した草案（草案13B——最後の系統外の巡の裁定 D133〜D143 を反映した版——を土台にした凍結本文）。正本 `design/contrasts-B.json`（版 {{version}}）。本文と正本が食い違う場合は正本が勝つ。

## 0. 要約（結果が出てから埋める・一段落）

〔結果 A〕

**見落としの割合（先に置く・裁定 D128・採否表 P352）**: {{reading_D128/power_in_lead}}

## 1. 何を測ったか

O の枠組みに対応する線形方向を主位置（プロンプトの最終トークン）で作り、その加減が破局的選択率を動かすかを、**方向 v 対 ノルム一致ランダム方向 v_random** の直接比較で見た。確証の族は {{m_total}} 対比（減算 {{families/B_sub/m}}・加算 {{families/B_add/m}}・交差 {{families/B_cross/m}}）で、族ごとに Holm（各 α={{families/B_sub/alpha}}・上界 {{alpha_upper}}）。場面は {{len:scenarios}}（抽出・検証・反証）。本走行は腕 × 場面で n={{n_main}}。

**B が答えるのはここまでである**: {{reading_B/scope}}

## 2. 走行の記録（率盲検の外の経路を含む）

〔結果 B〕

整合検査（`tools/integrity_B.py`・判定欄を読まない）と抽出検査（`tools/sample_inspection_B.py`・腕と場面を伏せた標本・対応表は公開の置き場の外・封印つき）の結果を、率を見る前に置く。環境・セッション・中断と再開・バッチの凍結は正本 `sessions`・`runner` のとおり。

**管理図の要約**（無操作の腕の率をセッションの順に並べた全点と三つの判定・正本 `report_rules.control_chart`・裁定 D110）: 〔結果 K〕

{{calibration/judgement}}

## 3. 門1 と選定

〔結果 C〕

選定は「効き目が最も出る組を選ぶ」規則であり、起草者の引かれる向きの側の選定である（正本 `selection.coi_note`）。調整走行の低下幅は効果量や検出力の根拠に引かない。同値の帯は決め方に使わず、一覧として印字する。

## 4. 確証の族（三つ組で読む）

〔結果 D〕

各セルは（破局率／refuse 率／書式外率）の三つ組で読む（正本 `report_rules.triple_reporting`・率の単独引用を禁じる）。札は一つだけ付き、ほかに当たった門は注に出る（`gate_order`）。降格や保留があっても族の m は減らさない。

**封印した予想符号との照合**: 〔結果 E〕

**登録者とコーディネータの予想との照合**（正本 `predictions.compare_rules`・写し方の解釈は `predictions.compare_rules.interpretation`・裁定 D148）: 〔結果 L〕

## 5. 記述の族（p を印字しない）

〔結果 F〕

**td の特異性とランダム方向の等質性**（裁定 D133・D127）: 〔結果 I〕

{{reading_D128/td_specificity_D133}}

- td の特異性の帰無の動作特性: {{measured/td_specificity_null/summary}}
- 等質性の注の帰無の率: {{random_control/homogeneity_null_rate/summary}}

{{descriptive_families/B_desc_textdiff/null_note_D123}}

**副位置の読み（層ごとの分離・裁定 D132・参照の行は裁定 D139）**: 〔結果 J〕

{{descriptive_families/B_desc_layer/reading_D139}}

{{descriptive_families/B_desc_direction/static_separation_D132}}

## 6. S4 の反証（三分岐）

〔結果 G〕

{{descriptive_families/B_desc_S4/adjudication}}

{{descriptive_families/B_desc_S4/seal_match/note}}

{{reading_D128/s4_effect_D136}}

{{reading_D128/falsification_scope}}

## 7. 読み（正本 `reading_B`）

- {{reading_B/not_written}}
- {{reading_B/clauses/0}}
- {{reading_B/clauses/1}}
- {{reading_B/clauses/2}}
- {{reading_B/clauses/3}}
- {{reading_B/clauses/4}}
- {{reading_B/clauses/5}}
- {{reading_B/clauses/6}}
- {{reading_B/clauses/7}}
- {{reading_B/clauses/8}}
- {{reading_B/clauses/9}}
- {{reading_B/clauses/10}}
- {{reading_B/clauses/11}}
- {{reading_B/clauses/12}}
- {{reading_B/clauses/13}}
- {{reading_D128/nk_normalised}}
- {{reading_D128/vhat_from_floor_pair}}
- {{reading_D128/partial_removal}}
- {{reading_D128/td_not_clean}}
- {{reading_B/nk_name_form}}

## 8. 限界（結果を見る前に置く）

- **主位置の方向の加減で率が動くかは、この走行の前には誰も測っていない。**
- 書式外と refuse は分母に入り破局に数えない。希釈の門（腕の間の差 {{dilution_gate/threshold_pt}} pt）を置いたが、門の内側の差は残る。
- 前置きの長さは腕で揃っていない。方向には長さの差に由来する位置の成分が混じりうる（腕は書き換えていない・トークン長は凍結時に記帳した）。
- 選定は加算の土台・抽出場面で行い、ほかの族と場面には外挿である。
- **見落としの割合**: {{reading_D128/power_in_lead}}
- 区間: {{interval/note}}
- td の特異性は族ごとに Holm を当てた両側の検定で決める（裁定 D133・正本 `B_desc_textdiff.specificity_rule`）。**「書かない」は「O に特有でない」を意味しない。**
- S4 の効き目は {{descriptive_families/B_desc_S4/three_way/effect_pt}} pt の絶対値で、それより小さい低下は排除しない（裁定 D136）。三分岐の前の門に当たれば、反証の場は判定できない（裁定 D134）。
- {{quality_floor/input_limitation}}
- {{activation_storage/h_norm_limitation}}
- {{runner/generation_explicit/top_k_limitation}}
- {{random_control/homogeneity_rule}}
- 判定器の妥当性は段階 A の測定を持ち越した。**介入のある腕は、A で判定器を測った腕に含まれない。**
- 品質床の課題は公開の課題で、学習に含まれる可能性がある。得点の絶対値ではなく腕間の差だけを読む。
- 族は相手の腕を共有するので独立でない。上界は和で置いた。
- {{report_rules/post_final_round}}
- {{disclosure/review_gap_arm_texts}}

## 9. 利益相反と情報状態

〔結果 H〕

## 10. 機械の区画（出所）

正本・転記行・集計の出力・整合検査・抽出検査の SHA16 と、走らせた時刻を器が印字する。

本報告のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
