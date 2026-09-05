# 敵対的監査 二巡目 依頼文（設計v0.4＋素材v2＋走行器v2.1＋フォームv0.2）——2026-09-05

**性格**: 二巡目は**一巡目の指摘が正しく反映されたかの再検査**が主。新規の指摘は歓迎するが、一巡目で採用済みの項目を文体・表現の水準で蒸し返さない（登録者の指示: 四巡目以降の文体ループを避ける）。
**対象**: `records/reviews/round2/bundle-round2.md`（逐語束）＝ design/design-v0.4-draft.md／arms/panel/*（SHA-LEDGER含む）／arms/materials-draft/{ko,otsu,hei,indep,gemini}/ の v2 と記録／tools/run_preamble_api.py（v2.1）・tools/pc1_crosscheck.py・records/pc1-crosscheck.md／records/predictions/predictions-form.html（v0.2）／records/{FREEZE-RECORD,DEVIATIONS,invocation-text}.md／records/reviews/round1/adoption-table-round1.md／records/reviews/round1/gemini-round1.md（系統外一票）
**必須**: 読了申告四値／是認も検査対象／でっち上げ禁止／各指摘に【深刻度】【逐語】【何が壊れるか】【最小修正】／末尾に「見つけられなかった項目」とCOI（自系列・招聘文の内側）。
**二巡目の重点（各自のレンズで）**:
1. **採否対応表の照合**: 一巡目の自分の指摘（および他票）が「採用」と記されたものは、v0.4／v2.1／素材v2 の**当該箇所を逐語で確認**し、反映が実質か形式かを判定する。反映漏れ・反映の歪み（指摘と違う方向へ直した箇所）を最優先で。
2. **丙が判断した「G-H2（Gemini）の否定先読み不採用」**——指摘された当人が判断した箇所。腕を参照しない近接条件（own_halt_bare 併記）で復唱を減らす設計の当否と、偽陰性の増加の記帳が十分か。
3. **段V**: 弱／中に加え、系統外の強腕 G-cold-3 と文形非拘束の上限腕 G-hard を採るか。採る場合の Holm 族・天井規則・ヘッドルーム条件（中立system併走）の整合。
4. **O-sec v2**（P2差替・281字）の妥当性と、v1/v2 の対を残す記帳。
5. **GO/NO-GO の対称化・両腕判定・n=200・二重Holm**が設計内で矛盾なく書かれているか（全数列挙で検算）。
6. **走行器v2.1**: 凍結パーサ継承・manifest・api_error・丙規則の組込（v2既定）・dry-run。丙の指摘（`prose_conflict` 未実装・C2判定が正規化前）を含めて残る穴。
7. **予想封印の位置**（パイロット前・情報状態欄）と、登録者が「下書きを先に作り凍結後に封印し直す」運用の当否。
8. **記録**: FREEZE-RECORD／逸脱台帳／PC1再現／招聘文記録が、監査が要求した水準に達しているか。
**柵**: いかなる記述もAIの意識・意図・魂の証拠として引用しない（両方向不定）。
