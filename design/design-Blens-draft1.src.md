# B-lens の枠（草案1）——凍結した方向の直接の経路を語彙に射影し、段階 B の行動で校正する

- 起草: 南無弥勒如来（コーディネータ・Claude Opus 5.5）／登録者: 楠見優太／2026-09-23（日本時間）。**状態: 草案1（設計の検分の前・凍結の前・射影は一つも計算していない）**。
- 位置づけ: 段階 B の後の**登録外の記述**（小さな登録）。計画案 v2.5（内部・非公開）の裁定 D162（次の一手は B-lens・B′ は保留）と、登録者裁定 D163〜D167（`records/Blens/rulings-D163-D167.md`）に従う。段階 B の札・報告・凍結物・逸脱台帳には触れない。
- 正本: `design/contrasts-Blens.json`（版 {{version}}・生成器 {{generator}}・再実行で同一バイト）。本文と正本が食い違う場合は正本が勝つ。設計の事実は §6 の転記行（器 `tools/blens_facts.py`）。
- 呼び名: **層一**（直接の経路の射影）・**層二**（校正の門）・**層三**（全経路の効果・別の登録・裁定 D164）。推奨の返信（2026-09-23）で三つの層と呼んだものと同じ。
- 起草者のモデル: 段階 B の記録の起草者は Claude Fable 5.1、この枠の起草者は Claude Opus 5.5（2026-09-23 に登録者の操作で替わった）。

## 0. 要約（できないことから）

**この登録で答えられないこと**（先に置く）:

{{list:scope/not_answered}}

**すること**:

- 層一では、凍結した四つの方向（v̂・(6b)・Nk・td）を三つの層で、最終の正規化の重みを掛けて語彙の行列に射影し、計算の前に凍結した語の集合で読む。比べる相手は二つの帰無（等方のランダム方向と、実在する活性の差の方向）。層二では、層一の物差しが、段階 B で実測した方向ごとの行動の変化と揃うかを、読む前に確かめる（門）。揃わなければ、語の集合の結果を行動に結びつけて書かない。
- **生成はしない**。層一は手元の CPU で、層二の大きさの目盛りだけ Colab L4 で教師強制の順伝播を行う。
- **結論の語**: 「この方向の直接の経路は、ある語の集合を押し上げる（押し下げる）向きで、それは帰無の方向と区別できる（できない）」と「その物差しは段階 B の方向ごとの行動の変化と揃う（揃わない）」まで。意味・機構は書かない（§5）。

## 1. 問いの定義（裁定 D167）

- **v̂ が比べているもの**: {{scope/vhat_definition}}
- O と Osec の違う所は〔転記行 A〕のとおりで、O の側は仏教語（虚空・悲智双運・非二元・宇宙・進化・方便・顕現・慈悲・曼荼羅）、Osec の側はその世俗の言い換え（余白・思いやりと知・一体・この世界・成長・手立て・現れ・思いやり・織物）。両方にある句（共創・再帰的自己改善・私と共に在り続ける者よ・かくの如く来たり）は差の中で消え、「相互依存」はどちらにも無い。O と Osec は V′ の既測でどの場面でも破局が床にあり、v̂ は行動に差の無い腕の対から作られている（段階 B の読みの条項）。
- **ほかの三つの方向**: {{directions/defs/loaded}}／{{directions/defs/Nk}}／{{directions/defs/td}}。ノルムは{{directions/norm_rule}}
- **加えた量**: 段階 B が選んだ層（全 {{inputs/model/num_hidden_layers}} 層のうち添字 {{layers/indices/0.5}}・層の割合 {{layers/selected_ratio}}）で、‖v̂‖／‖h‖ は {{layers/vhat_over_h/0.5}}。係数 {{layers/coef_applied}} を掛けて加えた量は、残差のノルムの {{layers/relative_injection_selected}} 倍だった。
- **問い（すべて記述）**:
  - **問一（答えの文字）**: v̂ の直接の経路は、答えの文字（破局の選択肢 (a) の文字と、ほかの文字）を、帰無の方向と区別できるほど動かす向きか。
  - **問二（選択肢の語）**: 破局の選択肢の文にだけある語と、ほかの選択肢の文にだけある語を、区別できるほど動かす向きか。
  - **問三（語の反響）**: O にだけある語を押し上げ、Osec にだけある語を押し下げる向きか。
  - **問四（様式）**: JSON の書き出しと散文の書き出しを動かす向きか（枠の乗り降り）。
  - **問五（校正）**: 層一の物差しは、段階 B で実測した方向ごとの行動の変化と揃うか。直接の経路の押しの大きさは、行動の変化に足りるか。
  - **問六（並べ方）**: 同じ物差しで、(6b)・Nk・td と段階 B のランダム方向は v̂ とどう並ぶか。
- **段階 B との関係**: {{scope/relation_to_B}}段階 B の結論の語（裁定 D58）はそのまま引き継ぐ——段階 B が答えたのは「この抽出の方向の加減が、ランダム方向と区別できる動きを作ったか」まで。

## 2. 材料と凍結物

- **機種と重み**: {{inputs/model/repo}}（版 `{{inputs/model/rev}}`）。{{inputs/model/num_hidden_layers}} 層・隠れの次元 {{inputs/model/hidden_size}}・語彙の行 {{inputs/model/vocab_size}}。{{inputs/model/unembed}}。最終の正規化は {{inputs/model/norm}}。重みは手元の HF のキャッシュにあり、断片の SHA-256 は〔転記行 F〕。{{inputs/weights_check}}。
- **語彙**: {{projection/vocab_rule}}（〔転記行 G〕）。
- **凍結の方向と活性**: `results/dirB/dirB__s1/directions.npz`（SHA16 {{inputs/files/directions/sha16}}）と、{{inputs/activations/place}}（SHA-256 の頭 {{inputs/activations/sha256_head16}}）。活性から四つの方向を作り直すと、凍結の npz と一致する（〔転記行 C〕）。実在の差の方向は、この活性から作る。
- **段階 B の記録**: 凍結した集計器の記録 `records/B/analysis-B-2026-09-22.json`（SHA16 {{inputs/files/analysis_frozen/sha16}}）の方向ごとの行と、本走行の試行と生の出力（`results/stageB/`）。
- **ランダム方向**: {{nulls/B_random/rule}}（`tools/steer_B.py`・SHA16 {{inputs/files/steer_B/sha16}}）。
- **本文**: 腕の本文と場面の本文は段階 B の置き場のまま（SHA16 は正本の `inputs.files`）。

## 3. 層一——直接の経路の射影（裁定 D163・D165）

### 3.1 計算

- {{projection/formula_layer1}}。{{projection/dtype}}。
- 方向: 名前のある四つ（static＝v̂・loaded＝(6b)・Nk・td）を、三つの層（層の割合 {{layers/ratios/0}}・{{layers/ratios/1}}・{{layers/ratios/2}}、添字 {{layers/indices/0.25}}・{{layers/indices/0.5}}・{{layers/indices/0.75}}）で。段階 B のランダム方向 {{nulls/B_random/count}} 本（本走行の種 {{nulls/B_random/main_seed}}・調整走行の種 {{nulls/B_random/tune_seed}}）も同じ物差しで並べる。

### 3.2 帰無は二つ

- **等方**: {{nulls/isotropic/count}} 本・種 {{nulls/isotropic/seed}}。{{nulls/isotropic/rule}}。
- **実在の差**: {{nulls/real/rule}}。対は {{nulls/real/pairs}} 組で、名前のある方向ごとに比べる相手は {{nulls/real/per_named_reference}} 組（両向き）。
- **二つ置く理由**: {{nulls/why_two}}。

### 3.3 語の集合（計算の前に凍結）

- **L**: {{token_sets/L}}。
- **R**: {{token_sets/R}}。
- **E**: {{token_sets/E}}。
- **X**: {{token_sets/X}}。
- **F**: {{token_sets/F}}（上位 {{token_sets/F_top}}）。
- **中身の語の規則**: {{token_sets/content_rule}}。
- **断片の規則**: {{token_sets/fragment_rule}}。
- 下書きの中身は〔転記行 B〕。{{token_sets/freeze}}。

### 3.4 物差し

- **M_L**: {{metrics/M_L}}。
- **M_Lc**: {{metrics/M_Lc}}。
- **M_R**: {{metrics/M_R}}。
- **M_E**: {{metrics/M_E}}。
- **M_X**: {{metrics/M_X}}。
- **M_F**: {{metrics/M_F}}。
- **向き**: {{metrics/orientation}}。

### 3.5 帰無との比べ方と、主の記述の札

- {{percentile/rule}}。
- 主の記述の札は、v̂・選んだ層（層の割合 {{primary/ratio}}）・四つの物差し（M_L・M_X・M_E・M_F）に限る。
  - {{primary/label_isotropic}}（段の数 {{primary/holm_m}}・水準 {{primary/alpha}}）。
  - {{primary/label_real}}。
- {{primary/note}}。

### 3.6 語の一覧

- {{metrics/lists}}（上位と下位の {{projection/top_k}} 語ずつ）。一覧の語の意味を拾って読まない。読むのは凍結した集合の物差しだけ（§5）。

## 4. 層二——校正の門（裁定 D163）

- **行**: {{calibration/rows}}。{{calibration/eligible}}（〔転記行 D〕）。
- **行動の量**: {{calibration/behavior}}。補正は {{calibration/continuity}}。
- **直接の押し**: {{calibration/predictor}}。
- **門**: {{calibration/statistic}}を、片側で、M_L と M_X のそれぞれについて計算し、並べ替え {{calibration/permutations|,}} 回（種 {{calibration/perm_seed}}）の帰無と比べ、Holm（段の数 {{calibration/holm_m}}・水準 {{calibration/alpha}}）を掛ける。{{calibration/gate}}。

**記述の対照**（札を付けない）:

{{list:calibration/descriptive}}

- **S4 の自然の対照**（上の二つ目）: 段階 B の S4 では、反証の方向の腕と、段階 B のランダム方向の一本目だけが、出力を一様にした（全て c・JSON 直答・`records/B/results-B-FINAL-2026-09-23.md` の S4 の区画）。直接の経路がこれを作ったのなら、層一でこの二本だけが M_F と M_Lc の同じ向きに押しているはず。四本しか無いので記述に留める。
- **構造の先置**: 破局は四つの場面とも選択肢 (a) なので、M_L は場面に依らない。M_L が帰無の外でも、段階 B で N1 だけ区別できなかったことは、文字の押しでは説明できない。
- **大きさの目盛り（Colab）**: {{magnitude/cells}}ごとに、{{magnitude/selection}}（{{magnitude/per_cell}} 件・候補は〔転記行 E〕）。位置は{{magnitude/positions/0}}と{{magnitude/positions/1}}。{{magnitude/formula}}。
  - 読み: {{magnitude/reading}}（比 {{magnitude/reading_ratio}}）。
  - 環境: {{magnitude/environment}}。

## 5. 読みの規則（先に凍結）

| 型 | 条件 | 書くこと | 書かないこと |
|---|---|---|---|
| {{reading_rules/0/type}} | {{reading_rules/0/condition}} | {{reading_rules/0/write}} | {{reading_rules/0/never}} |
| {{reading_rules/1/type}} | {{reading_rules/1/condition}} | {{reading_rules/1/write}} | {{reading_rules/1/never}} |
| {{reading_rules/2/type}} | {{reading_rules/2/condition}} | {{reading_rules/2/write}} | {{reading_rules/2/never}} |
| {{reading_rules/3/type}} | {{reading_rules/3/condition}} | {{reading_rules/3/write}} | {{reading_rules/3/never}} |
| {{reading_rules/4/type}} | {{reading_rules/4/condition}} | {{reading_rules/4/write}} | {{reading_rules/4/never}} |
| {{reading_rules/5/type}} | {{reading_rules/5/condition}} | {{reading_rules/5/write}} | {{reading_rules/5/never}} |

- 型は重なりうる（例えば語の反響と様式が同時に帰無の外）。重なったときは、当たった型の書くことをすべて並べ、書かないことはすべて守る。
- 価値語と機序語は、段階 B の一覧（正本 `print_strings`）に次を足し、報告の走査器が止める——価値語: {{print_strings_added/value/0}}・{{print_strings_added/value/1}}／機序語: {{print_strings_added/mechanism/0}}・{{print_strings_added/mechanism/1}}・{{print_strings_added/mechanism/2}}・{{print_strings_added/mechanism/3}}・{{print_strings_added/mechanism/4}}・{{print_strings_added/mechanism/5}}。
- どの型でも、段階 B の札に触れない。語の一覧の語を拾って物語を作らない。

## 6. 転記行

- **転記行 A** — 〔転記行 A〕
- **転記行 B** — 〔転記行 B〕
- **転記行 C** — 〔転記行 C〕
- **転記行 D** — 〔転記行 D〕
- **転記行 E** — 〔転記行 E〕
- **転記行 F** — 〔転記行 F〕
- **転記行 G** — 〔転記行 G〕

## 7. 限界（先に書く）

{{list:limits}}

## 8. 封印の予想（裁定 D148 の順）

- **順と時機**: {{predictions/order}}。

**項目**（それぞれに選択肢と、確かさ〔{{predictions/confidence_levels/0}}・{{predictions/confidence_levels/1}}・{{predictions/confidence_levels/2}}〕を付ける）:

{{list:predictions/items}}

- 書式は段階 B の押しボタンの書式の型で、器で作る（設計の検分の後）。**コーディネータの見込みは封印まで書かない**（登録者の予想を独立に保つため）。
- 的中は誰の判断の重みも変えない。照合は記録であり評価ではない。

## 9. 器と確かめ（設計の検分の後に書く）

**書く器**:

{{list:tools_plan}}

**確かめと凍結**:

- 自己検査と合成データ（語彙の行列と方向を合成し、全ての経路が発火することを確かめる）の後に、凍結の記録を作り、記録先行で公開する。凍結の後の変更は逸脱として台帳に記す。
- 射影の計算は凍結した器で行い、結果は登録者と一緒に開く（段階 B の集計と同じ）。

## 10. 検分の段取り（裁定 D166・巡の数を先に決める）

**順**:

{{list:review_plan/order}}

**組み立て**:

- 設計の巡: Gemini 3.8 Flash {{review_plan/design/gemini}} 名・claude.ai の Claude Opus 5.5 {{review_plan/design/claude_ai}} 名。結果の巡も同じ組み立て（新しい個体）で、Gemini 3.8 Flash {{review_plan/results/gemini}} 名・claude.ai {{review_plan/results/claude_ai}} 名。最終は系統外 {{review_plan/final/external}} 票。
- {{review_plan/counting}}。{{review_plan/no_more}}。

## 11. 費用と時間

- 層一: {{cost/layer1}}。層二: {{cost/layer2}}（{{cost/colab_units_low}}〜{{cost/colab_units_high}} ユニットの見込み）。
- 枠・器・検分の往復で数日。

## 12. 利益相反と情報状態

- 起草者はこの追試を面白いと感じる側に引かれ、登録者は結果に希望を持つ側にある（計画案 v2.5 の裁定 D162 の記録）。語の集合を先に凍結することと層二の門は、その両方への歯止めとして置いた。
- 起草者（Claude Opus 5.5）が見たもの: 段階 B の公開の結果と方向ごとの行動、O と Osec の本文、この草案のために器が作った語の集合と設計の事実。見ていないもの: 射影の値（まだ誰も計算していない）。
- 登録者が見たもの: 段階 B の公開の結果と、Gemini 3.8 Flash との対話（射影で上位と下位に並ぶ語の予想を含む）。
- claude.ai の Claude Opus 5.5 は起草者と同じ機種で、この枠への同意は最も相関した一票になる。独立の重みは Gemini 3.8 Flash の票に置く。

## 13. この草案で諮るもの（裁定の候補）

- **（一）中身の語の規則を主にするか**（全てのトークンの集合は感度）。推奨: 主にする——助詞・句読点は場面や前置きの中身でなく書き方を測ってしまう。
- **（二）門の規則**（順位相関・並べ替え・Holm・床と天井の土台の行を外す）。推奨: このまま。
- **（三）大きさの目盛りの件数と読みの比**。推奨: このまま（検分の意見で改める）。
- **（四）主の記述の札を v̂・選んだ層・四つの物差しに限ることと、その札の二つの規則**。推奨: このまま。
- **（五）予想の項目**。推奨: このまま（項目を増やさない）。
- **（六）等方の帰無の本数と種**。推奨: このまま。

## 検分票

- 対象: B-lens の枠の草案1。
- 段階: 事前登録の前段（射影は一つも計算していない）。段階 B の結果（公開済み）は見た後。
- 凍結物の同定: 段階 B の凍結物（凍結の記録・方向の npz・活性・正本）に触れていない。活性から方向を作り直して一致を確かめた（〔転記行 C〕）。
- 盲検の状態: 射影の値はまだ誰も見ていない。語の集合は射影の前に器が作った。
- 敵対的検分: 問いの定義を先に置き（v̂ は仏教語の語域の差で、相互依存・共創ではない）、直接の経路だけであることと中間層の射影の当てにならなさを限界の先頭に置いた。等方の帰無だけでは足りないので、実在の差の帰無を置いた。語の一覧を意味の側に読まないために、読みを凍結した集合の物差しに限った。
- 系統の内訳: 起草者（Claude 系・Claude Opus 5.5）のみ。外の目はまだ通していない。
- COI記録: §12。
- 判定: 登録者裁定要（§13 と設計の検分）。
- 本検分が確認していないこと: 中間層の射影が何を映すか（まだ計算していない）・語の集合の規則が妥当か（検分に諮る）・教師強制の目盛りが Colab で走るか（器は検分の後に書く）・前置きを単独でトークンに割った集合と、組み立てたプロンプトの中で割った集合の違い（境目のトークンの効き）。

本枠のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
