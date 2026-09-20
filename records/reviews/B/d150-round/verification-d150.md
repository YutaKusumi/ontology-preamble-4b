# 四票の所見の追い問い（機械生成・`tools/verify_d150.py` v1・2026-09-20T06:03:25Z UTC）

- 正本 SHA16 5D45DFF3802F4D58・判定の器 SHA16 8D9F4FB83139C426。
- **事後の再現**（再現の枠を先に登録していない・票を読んだ直後に現物を当たった）。
- 票の出所: G1・G2（系統外・Gemini 3.8 Flash 二名）／C1・C2（系統内・claude.ai の Claude Opus 5 二名・**どちらも Gemini の票を読んでから書いたと申告**）。

| 番号 | 所見 | 出所 | 現物で当てた結果 | 判定 |
|---|---|---|---|---|
| K207 | 走行器と整合検査が選別の十三腕を引けない（Gemini 二人目・重大） | G2 | 走行器 arm_texts() は 13 腕すべてを引いた（欠け 0）。整合検査の ARM_SHA も合わせた一覧から作る | 再現しない |
| K208 | 凍結の一覧に判定の器・持ち越しに段階 A の器が無い（Gemini 二人目・重大） | G2 | TOOLS に identity_screen_B.py: ある／CARRYOVER に tools/identity_screen_A.py: ある | 再現しない |
| K209 | 不合格のとき終了コード 2 で終わる（段階 A の器は 0・Gemini 一人目） | G1 | B: sys.exit(0 if verdict == 'pass' else 2)／A: 終了コードの指定 なし（常に 0） | **再現する** |
| K210 | 採点欠落（選択は読めたが破局が空）を黙って「その他」に数え、止まらない（claude.ai 二人目） | C2 | 判定の器は終了コード 2 で判定 fail を書いた。排他の件数は破局 140・その他 20、B の読み口は採点欠落 20 件 | **再現する** |
| K211 | 同じ腕の走行が二本あると n_ok を足し合わせ、登録の n を超えても止まらない（claude.ai 二人目） | C2 | Onull の n_ok=320（登録の n は 160）・終了コード 2・判定 fail | **再現する** |
| K212 | 整合検査が標本化の top_k を照らさない（claude.ai 二人目） | C2 | 照らしている欄: temperature・top_p | **再現する** |
| K213 | 正本 `identity_screen.generation` に top_k が無い（claude.ai 二人目） | C2 | 鍵: temperature・top_p・max_tokens・thinking | **再現する** |
| K214 | 判定の器が走行の種を登録と照らさない（段階 A の器は照らしていた） | C1・C2 | B の器に seed の文字列: 無い／A の器に seed_registered: ある | **再現する** |
| K215 | 判定の記録を読む器が無い（報告の組み立て器も入力に取らない） | C1・C2 | 名指す器 8 本（bundle_B_d150.py・design_facts_B.py・dry_run_B.py・freeze_B.py・identity_screen_B.py・make_contrasts_B.py・mutation_B.py・verify_d150.py）・報告の組み立て器が読む: いいえ | **再現する** |
| K216 | 判定の器が呼ぶ段階 A の**コード**が凍結の網に無い（`runs_A.py`）・器も照らさない | C1 | freeze_B の持ち越しに runs_A.py: 無い／check_pin の対象は正本と記録の二つ | **再現する** |
| K217 | 帰無での不合格率（登録の対 対 別案の対）を数え直す | C1・C2 | 登録の対 0.0315／別案の対 0.0910／API 固定 0.0050／段階 A の十腕 0.0246（反復 200,000・種 20260920） | 概ね一致 |
| K218 | 段階 A の門0.5 の記録に重みの版（rev）が無い（claude.ai 一人目） | C1 | 記録の鍵に model はある（Qwen/Qwen3-4B-Instruct-2507）が rev は 無い | **再現する** |
| K219 | vLLM の件数は段階 A の別のセッションの走行である（claude.ai 二人目） | C2 | 走行キー idA__N1__none__seed60001・記録の作成 2026-09-14 10:28 UTC | **そのとおり** |

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
