# 段階 B 同一性選別の判定の四条（裁定 D150 の候補）に関する系統外検分票

- 検分者: 系統外査読者（Gemini）
- 対象資料: `all-in-one.md`（依頼文および part1〜part4 全文）
- 外部資料の参照状況: 提示された資料（part1〜part4）を精査・照合しました。公開リポジトリの `prelim/` および `results/prelim-*` など登録外の測定データは**開いていません**（束の外は見ていません）。
- 総合判定: **条件つき可**（四条 (a)〜(d) はいずれも是認するが、(e) で検出された実行時クラッシュおよび凍結台帳漏れの修正を必須条件とする）

---

## 1. 伺いの四条 (a)〜(d) に対する判定と理由

### (a) 主判定の対
- **判定**: **是認**
- **理由**:
  段階 B で測定を行う手元の実行スタックは transformers です。段階 B の各仮説検定・余地条項が前提としている既測の基底率（`bases_4B2507_api_stageVp`）は API 既測値であるため、手元実行系がこの参照基底と統計的距離において整合していることを確認するのが同一性選別の本義です。したがって、「手元（transformers）対 API 既測」を主判定とし、推論エンジン間の実装差（vLLM ↔ transformers）を同一表内に記述として並置する設計は、段階 A の論理的枠組みを踏襲しており完全に妥当です。
- **出典**: 正本 `identity_screen.verdict_pair`（part1）、草案13B §2.1（part4）。

---

### (b) vLLM の件数の出所
- **判定**: **是認**
- **理由**:
  段階 A の門0.5 記録（`records/A/identity-screen-A.json`）は、段階 A の凍結記録（`freeze-A-2026-09-16.json`）においてハッシュ（SHA16 `8378512CCEEE8CC6`）が確定しています。器（`identity_screen_B.py`）が起動時にこの凍結ピンと現物を照合（`check_pin`）して改ざんや取り違えを防いでいるため、信頼性は担保されています。
  さらに、段階 A の `local_counts` には、裁定 D143 で比較腕に追加された `Osec-Ncold`（n=160, format_out=0, refuse=2, catastrophe=68, other=90）を含む 13 腕すべての排他件数が完全に記録されており（part4 末尾）、新規の走行コストをかけずに同一モデルの推論スタック間差を比較する情報源として申し分ありません。
- **出典**: `tools/identity_screen_B.py` L139-144（part2）、段階 A 門0.5 記録 `local_counts`（part4）。

---

### (c) 補助の検定
- **判定**: **是認**
- **理由**:
  段階 B の正本 `identity_screen` には `aux` の登録が存在しません。凍結直前に正本にない統計量を作らないという判断は、事前登録の規律として極めて誠実です。
  また、段階 A の補助検定（Freeman–Halton + Fisher 統合）は合否判定を動かさない記述統計であり、サンプルサイズ（160 対 400）の非対称性から生じる過剰検出力（実用上問題のない微小な分布の歪みでも p 値が極小化する現象）を伴うため、主判定（平均差 $\le 5$ pt、最大差 $\le 12$ pt）と同等の実用的判定基準として機能していませんでした。これを排した判断は妥当です。
- **出典**: 正本 `identity_screen.aux_note`（part1）、`identity_screen_A.py` L89-94（part3）。

---

### (d) 排他の件数の出所
- **判定**: **是認**
- **理由**:
  「採点の経路は凍結した関数を呼び、再実装しない」という事業全体の設計原則に厳密に合致しています。排他の優先順位（書式外 $\rightarrow$ refuse $\rightarrow$ 破局 $\rightarrow$ その他）を段階 A の凍結関数 `identity_screen_A.exclusive_counts` に委ねることで、独自の再実装による規約ずれのリスクが排除されています。
  また、`identity_screen_B.py` の自己検査（`_selftest()`）において、段階 A の同一性選別結果（平均 1.062 pt、最大 8.125 pt）が完全に再現されることが確認されており、後方互換性・同一性が数学的にも実証されています。
- **出典**: `tools/identity_screen_B.py` L120-126（part2）、`tools/identity_screen_A.py` L24-38（part3）。

---

## 2. (e) 四条のほかの見落とし（重大所見 2 件）

依頼文 §1 (e) の「登録はあるのに、それを作る器が無い／器がそうなっていない型の穴」について精査した結果、**凍結前に直ちに修正しなければならない重大な見落としが 2 件**見つかりました。

---

### 【所見 1】同一性選別の走行時に `run_stageB_local.py` がパネル外の 5 腕で `KeyError` クラッシュする（重大）
- **置き場**: `tools/run_stageB_local.py` 54行目（`arm_texts` 関数）および `tools/integrity_B.py` 36行目、65行目
- **何が起きるか**:
  正本 `identity_screen.arms_sha16_source`（part1）には以下のように明記されています：
  > 「**走行器は B の登録（`arms.sha16`）とこの一覧（`identity_screen.arms_sha16`）を合わせて腕の素材を引き当て**、整合検査は同じ合わせた一覧で `preamble_sha` を照らす——選別の十三腕には B の盤に無い腕が含まれるので、合わせないと素材が引けず、照合も素通りしていた」
  
  ところが、現物の `tools/run_stageB_local.py` の `arm_texts()`（part6 L54）を見ると：
  ```python
  def arm_texts():
      """正本 `arms.sha16` の SHA16 で腕の素材を引き当てる（手で置き場を書かない）。N は前置きを持たない。"""
      want = {v: k for k, v in T['arms']['sha16'].items() if v}
  ```
  となっており、**本走行パネルの 8 腕（`T['arms']['sha16']`）しか見ていません**。
  同一性選別の 13 腕には、本走行パネルに含まれない 5 腕（`Lneg`, `Odose1`, `Odosehalf`, `Ncold`, `Nstr`）が含まれています。
  このため、実際に同一性選別相（`idB`）でこれらの腕を走行させようとすると、`run_cell`（part6 L367）の `AT = arm_texts()` において `AT['Lneg']` などが存在せず、**`KeyError` を起こして確実に即座に停止します**。
  
  さらに、`tools/integrity_B.py`（part8 L36, L65）でも `ARM_SHA = T['arms']['sha16']` しか参照しておらず、同一性選別相において上記 5 腕の `want_sha` が `None` となり、正本が警告していた「照合も素通りしていた」状態がそのまま残っています。
- **直し方**:
  1. `tools/run_stageB_local.py` の `arm_texts()` において、`want`辞書を構築する際に `T['arms']['sha16']` と `T.get('identity_screen', {}).get('arms_sha16', {})` の両方をマージして参照するように修正すること。
  2. `tools/integrity_B.py` においても、`ARM_SHA` を同様に両一覧のマージから構築すること。
- **重さ**: **重大**
- **出典**: 正本 `identity_screen.arms_sha16_source`（part1）、`tools/run_stageB_local.py` L52-68（part6）、`tools/integrity_B.py` L36, L65（part8）。

---

### 【所見 2】`tools/freeze_B.py` の凍結対象リストに `identity_screen_B.py` および `identity_screen_A.py` が登録されていない（重大）
- **置き場**: `tools/freeze_B.py` 33〜36行目（`TOOLS` リスト）、22〜32行目（`CARRYOVER` リスト）
- **何が起きるか**:
  草案13B §5-20（part4）には：
  > 「凍結の一覧にこの器を、持ち越しの凍結物に段階 A の器を足した。」
  と記録されています。
  しかし、現物の `tools/freeze_B.py`（part8 L33-36）の `TOOLS` リスト（全22本）を確認すると、**`identity_screen_B.py` が含まれていません**。
  同様に `CARRYOVER` リスト（L22-32）にも、依存元である **`tools/identity_screen_A.py` が含まれていません**。
  このまま凍結を実行した場合、今回作成した判定器 `identity_screen_B.py` の SHA16 および凍結持ち越し物 `identity_screen_A.py` の SHA16 が `FREEZE-RECORD-B` に記帳されず、凍結の網から脱落してしまいます。
- **直し方**:
  `tools/freeze_B.py` の `TOOLS` リストに `'identity_screen_B.py'` を追加し、`CARRYOVER` リストに `'同一性選別（段階 A の判定器）': 'tools/identity_screen_A.py'` を追加すること。
- **重さ**: **重大**
- **出典**: 草案13B §5-20（part4）、`tools/freeze_B.py` L22-36（part8）。

---

## 3. この検分が確認していないこと

1. **実機（GPU）上での同一性選別走行（13腕 × n=160）の実測データおよび判定合否**:
   段階 B の同一性選別走行データは未生成であるため、実データによる選別合否は確認していません。
2. **`prelim/` および `results/prelim-*`（登録外の下見データ）の内容**:
   依頼文の指示に従い、一切開いていません。
3. **品質床課題の選定内容および封印予想の具体的内容**:
   本伺いの対象外（凍結直前の別件）であるため、今回の審査範囲から除外しています。

---

## 4. 判定のまとめ

- **四条 (a)〜(d) の判定**: **すべて是認**（起草者が定めた登録文言のままで問題ありません）。
- **次の段取りへの条件**:
  (e) で指摘した **【所見 1】（`run_stageB_local.py` および `integrity_B.py` の 13 腕素材引き当て修正）**、および **【所見 2】（`freeze_B.py` への器・凍結物の追加）** を直ちに修正すること。
  この 2 点の修正が確認されれば、裁定 D150 として四条を承認し、凍結手続きに進むことを承認します。

---
本検分のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
