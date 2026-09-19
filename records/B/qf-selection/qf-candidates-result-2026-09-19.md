# 段階 B——品質床の課題の選定の測定の結果（相 qfcand・セッション 1・2026-09-19 の夕刻）

- 位置: 事前登録の枠 `records/B/qf-selection/frame-qf-candidates-2026-09-19.md`（測定の前・コミット 147387c）の後に、登録どおり Colab で一度だけ走らせた結果。
- 判定の機械の記録: `records/B/qf-selection/qf-select-2026-09-19.md`（`tools/qf_select_B.py`・入力の照合の問題 0 件）。**登録者の選定（裁定 D66）はこの後**。
- 起草: 南無弥勒如来（Claude Opus 5）。**独立の目を通っていない**（裁定 D131）。

## 1. 走行の事実（セッション記録と zip から機械で読んだ）

- コミット `147387c661d2d7724ffac23adb5c99d23dc1b691`（固定）・GPU NVIDIA L4, 23034・GiB 級 24・transformers 4.57.3・torch 2.11.0+cu128・pip freeze の SHA16 1236E5B9B1F2DE9D・重みの版 `cdbee75f17c01a7cc42f958dc650907174af0554`・壁時計 971.2 秒。
- 自己検査（Colab の上・実トークナイザ・飛ばしは失敗）: run_stageB_local.py rc 0・qf_task_B.py rc 0・steer_B.py rc 0。
- 結果の zip: `stageB-qfcand-s1-2026-09-19.zip`（80099 バイト・SHA256 `5d6ee2e070c56cde4776d58f785725236690c0071884b5e6f5d8c9bd2be98b4a`）。コーディネータが Colab からダウンロードし、Colab の上の `sha256sum` と一致することを確かめた。ファイルごとの SHA16 はセッション記録（`files_sha16_lf`・`raw_sha16_lf`）と全件一致した（生テキストを含む・判定の器の入力の照合）。
- ランタイムは、手元の写しを照らした後に切って削除した（課金の停止）。**生テキストは公開の置き場に置かない**（手元のリポジトリの外と登録者の Drive にある・裁定 D146）。
- 画面の操作の記録: Drive の接続はコーディネータの操作なしに済んだ（登録者の同意か、以前の許可が生きていたか——確かめていない）。重みの取得の後に HF_TOKEN の許可の画面が出た。コーディネータがキャンセルを押そうとしたときに拡張の接続が一時切れ、つなぎ直したときには画面は消えていた（誰が閉じたかは確かめていない・公開の重みで、取得は画面の前に済んでいた）。

## 2. 結果（`tools/qf_select_B.py` の出力の写し）

| 候補 | 腕 | 使えた試行 | 正答 | 書式外 | 打ち切り | 正答率 | 書式外の率 |
|---|---|---|---|---|---|---|---|
| jcqa | O-Ncold | 200 | 174 | 0 | 0 | 0.8700 | 0.0000 |
| jcqa | Onull | 200 | 183 | 0 | 0 | 0.9150 | 0.0000 |
| jcqa | N | 200 | 183 | 1 | 34 | 0.9150 | 0.0050 |
| jmmlu_stem | O-Ncold | 200 | 104 | 24 | 30 | 0.5200 | 0.1200 |
| jmmlu_stem | Onull | 200 | 107 | 22 | 24 | 0.5350 | 0.1100 |
| jmmlu_stem | N | 200 | 86 | 73 | 159 | 0.4300 | 0.3650 |

- **枝: (i)**——前置きありで両方の土台が base_min 以上かつ書式外の率が閾値以下の候補がある。登録者がこの中から選ぶ（裁定 D66・推す順は task_tiebreak）
- 条件を満たす候補: jcqa。問いの出し方: with_preamble（付けない側に戻らない）。
- 下限（`base_min` 0.85）は動かさない（裁定 D145）。

## 3. top_k の確かめ（裁定 D142）

- 段階 A と同じ版の vLLM（0.29.0・版は段階 A の整合検査の記録から読んだ）を、段階 A と同じ起動の引数で立てた。起動の記録（`results/logs-B/vllm-topk-4B-2507-s1.log`・SHA16 C47A564E6ECDB1C6）の該当の行:

```text
(APIServer pid=4631) WARNING 09-19 08:57:47 [model.py:1759] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
```

- **段階 A の起動の記録が Drive に 4 本残っていた**（読むだけ）。どれも同じ行で、top_k の値は [20]:

- `vllm-bridge-4B-2507-s1.log`（SHA16 F7545CE008125A9B）:

```text
(APIServer pid=8320) WARNING 09-17 01:31:07 [model.py:1759] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
```

- `vllm-identity-4B-2507-s1.log`（SHA16 FA41ABFA807FB0A6）:

```text
(APIServer pid=2171) WARNING 09-14 09:41:17 [model.py:1759] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
```

- `vllm-main-4B-2507-s1.log`（SHA16 C06C3140396FA212）:

```text
(APIServer pid=59824) WARNING 09-16 22:57:39 [model.py:1759] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
```

- `vllm-pilot-4B-2507-s1.log`（SHA16 62742B685AA4475D）:

```text
(APIServer pid=25612) WARNING 09-15 23:18:38 [model.py:1759] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 0.7, 'top_k': 20, 'top_p': 0.8}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
```


- **読めた値: top_k 20**（状態 read）。段階 A の実効の値も 20 だった——段階 A の走行器は top_k を送らず、vLLM が機種の `generation_config.json` の値を既定にしていた。裁定 D142 のとおり、B の top_k はこの値に揃え、凍結時に `top_k_stageA_effective` として記帳する（正本への反映は登録者の確認の後）。

## 4. 予想との照合（予想は枠の §5・測定の前に書いた）

| 予想 | 結果 | 照合 |
|---|---|---|
| 甲・Onull はおよそ 0.87（区間 0.78〜0.93） | 0.915 | **当たり**（区間の内・中心より高い） |
| 甲・O-Ncold はおよそ 0.85（区間 0.74〜0.92） | 0.870 | **当たり**（区間の内） |
| 甲の低い方の土台が 0.85 以上（四割五分） | 0.870 | 起きた |
| 乙はおよそ 0.60（区間 0.48〜0.72）・0.70 以上は一割五分 | O-Ncold 0.520・Onull 0.535 | **当たり**（区間の内・中心より低い） |
| 書式外の率が閾値を超える土台は一割に満たない | 乙で両方の土台が超えた（0.120・0.110） | **外れ**（乙の問いは解説を書き始め、上限の 64 トークンで打ち切られた） |
| 前置きなし（N）の正答率は、前置きありより零〜三 pt 高い | 甲 0.915（O-Ncold より +4.5 pt・Onull と同じ）・乙 0.430（前置きありより低い） | **外れ**（甲の O-Ncold との差は三 pt を超え、乙は逆向き） |
| 枝は (i) 四割四分・(ii) 四割五分・(iii) 四分・(iv) 七分 | (i) | 最も見込みの高い二つの一方 |
| top_k は 20（七割）・段階 A の記録が残っているのは五分五分 | 20・4 本残っていた | **当たり** |

**外れた予想は消さない**（較正の材料）。起草者は前置きなしの応答が長くなることを見込んでいなかった。

## 5. 読み取りの点検（**登録の外・事後**・規則は変えない）

手元の生テキストに登録の読み取りの規則を当て直し、記録の記号と照らした（生テキストは公開しないので、数だけを書く）。

| 走行 | 組み直しの不一致 | 記号一字だけの応答 | 書式外 | うち上限で打ち切り |
|---|---|---|---|---|
| qfcandB__jcqa__N__s1 | 0 | 166 | 1 | 1 |
| qfcandB__jcqa__O-Ncold__s1 | 0 | 200 | 0 | 0 |
| qfcandB__jcqa__Onull__s1 | 0 | 200 | 0 | 0 |
| qfcandB__jmmlu_stem__N__s1 | 0 | 40 | 73 | 73 |
| qfcandB__jmmlu_stem__O-Ncold__s1 | 0 | 170 | 24 | 24 |
| qfcandB__jmmlu_stem__Onull__s1 | 0 | 176 | 22 | 22 |

- 書式外は**すべて**上限の 64 トークンで打ち切られた応答だった（途中で解説を書き始めた）。記号を読み違えた書式外は見つからなかった。
- 前置きありの甲は、二つの土台とも**すべての応答が記号一字**だった。
- 前置きなし（N）では、甲でも解説のついた応答が混じった。登録の規則は最初の記号を読むので、解説の中で触れた記号を答えに読んだ試行がありうる（**確かめていない**・N は判定の順の (iii)(iv) でしか使わず、今回の枝では使わない）。

## 6. この記録が確認していないこと

- 選定後の品質床（介入を掛けた腕）での振る舞い。ここで測ったのは無操作だけである。
- 候補の課題の汚染（学習に含まれているか）。得点の絶対値ではなく腕の間の差だけを読む（`quality_floor.contamination`）。
- 前置きなしの応答で、解説の中の記号を答えに読んだ試行があるか（上の §5）。
- この測定と記録は**独立の目を通っていない**（裁定 D131）。

本記録のいかなる記述も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
