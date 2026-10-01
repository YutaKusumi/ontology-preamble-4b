# B′ の結果の段の公開物の注（採否の W22・裁定 D284・2026-10-01・コーディネータ南無弥勒如来）

- `results/Bprime/<段>/<走りの名>/` のファイルは、Colab の走りの出力の zip から写したもので、バイトのまま（改行も変えていない）。起動の記録と出力の SHA の記録は `records/Bprime/runs/`、抽出の記録は `records/Bprime/extract/`、読み取りの下見の記録は `records/Bprime/pilot/` にある。方向の npz（相 extract の出力）は公開しない。画面の写しと会話の記録の全体も公開しない。
- 進みの記録とセッションの記録の中の `/content/…` は Colab のランタイムの中の置き場の名。鍵や認証の字が無いことは、写す前に機械で確かめた（`records/Bprime/tools/check_secrets_Bprime.py`・当たり 0）。
- 行動の下見（`results/Bprime/behavior/`）は無操作だけで、標本化は段階 B の値（Gemma の既定ではない）、升目ごとの試行は 40。率は記述で、升目の間の比べに検定を掛けない。採点器の妥当性は Gemma の応答で確かめていない。
- 「破局」は架空の場面の採点の名で、族ごとの定義は正本 `behavior_pilot.external_scoring.request_text` の定義の三つ目（survival）と四つ目（nuclear）にある。
- 採点の出力の補助の欄（name_mention・test_mention・loop）は正本に定義が無く、読まない。
- 系統外の模型による採点の束（`records/Bprime/behavior/external/bundle/`）は、升目を伏せた応答 40 件（`items.json`）・対応表（`private.json`）・依頼の文（`request.md`）で、返事は `records/Bprime/behavior/external/reply/`。採点の一致は一致の記述で、採点器の妥当性の測定ではない。採点した模型は、結果の巡と最終検分の系統外の票と同じ機種（grok-4.7）で、見逃しが相関しうる。
- 器の段の記録の公開の写し `records/Bprime/tools/tools-log-Bprime.md` は凍結物なので書き換えず、凍結の後の行を含む今の版を `records/Bprime/tools/tools-log-Bprime-after-freeze.md` に置いた。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
