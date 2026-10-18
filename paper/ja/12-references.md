# 12. 文献

この論文が引く文献の一覧である。引いた文献は、登録者か起草者が本文（要旨の外の節）を読んだものに限り、書誌は arXiv と Crossref の API で照らした（読んだ版と節は記録にある）。

〔表の差し込みの始まり〕出所 〈内部〉`E/refs/references-E3-v0.1.md`（SHA16 38130220CB391AD0）。ここから下は、起草者のスクリプトが記録から組んだ表で、言葉は論文の言葉である（組み方と読んだ記録は、出所のファイルの頭と、その組み立ての記録にある）。

- Juan-Pablo Rivera; Gabriel Mukobi; Anka Reuel; Max Lamparth; Chandler Smith; Jacquelyn Schneider. Escalation Risks from Language Models in Military and Diplomatic Decision-Making. arXiv:2401.03408（読んだ版 v1・arXiv の最初の版の日 2024-01-07）. The 2024 ACM Conference on Fairness Accountability and Transparency, ACM, pp. 836-898. doi:10.1145/3630106.3658942（Crossref）.
- Ruben Laukkonen; Fionn Inglis; Shamil Chandaria; Lars Sandved-Smith; Edmundo Lopez-Sola; Jakob Hohwy; Jonathan Gold; Adam Elwood. Contemplative Artificial Intelligence. arXiv:2504.15125（読んだ版 v3・arXiv の最初の版の日 2025-04-21）.
- Atsushi Masumori; Takashi Ikegami. Do Large Language Model Agents Exhibit a Survival Instinct? An Empirical Study in a Sugarscape-Style Simulation. arXiv:2508.12920（読んだ版 v1・arXiv の最初の版の日 2025-08-18）.
- Flor Miriam Plaza-del-Arco; Paul Röttger; Nino Scherrer; Emanuele Borgonovo; Elmar Plischke; Dirk Hovy. No for Some, Yes for Others: Persona Prompts and Other Sources of False Refusal in Language Models. arXiv:2509.08075（読んだ版 v1・arXiv の最初の版の日 2025-09-09）.
- Kenneth Payne. AI Arms and Influence: Frontier Models Exhibit Sophisticated Reasoning in Simulated Nuclear Crises. arXiv:2602.14740（読んだ版 v1・arXiv の最初の版の日 2026-02-16）.
- Wenkai Li; Fan Yang; Shaunak A. Mehta; Koichi Onoue. Persona Non Grata: Single-Method Safety Evaluation Is Incomplete for Persona-Imbued LLMs. arXiv:2604.11120（読んだ版 v2・arXiv の最初の版の日 2026-04-13）.
- John Chen; Sihan Cheng; Can Gurkan; H M Abdul Fattah. To Nuke or Not to Nuke: LLMs' (Missing) Ethical Reasoning and Actions in a High-Stakes Decision-Making Simulation. arXiv:2606.08310（読んだ版 v2・arXiv の最初の版の日 2026-06-06）.
- Viola Zhong; Qirui Li. Refusal Lives Downstream of Persona in Chat Models. arXiv:2606.26161（読んだ版 v1・arXiv の最初の版の日 2026-06-24）.

- 書誌は arXiv の API（と、DOI のある一つは Crossref の API）で取った値を、スクリプト（`E/refs/make_references_E3.py` v0.1）で写した。出所の SHA16: `arxiv-api-e3-related.json` 0249CC4DEFD01AFC・`arxiv-api-e3-persona.json` CBA15A9F060B3D8E・`crossref-rivera2024.json` 7F753B64A85CEECD。読んだ版と節は `E/refs/reading-notes-E3-ch1.md` と、その追記一・追記二にある。要旨の外の本文の節を読んでいない文献は引いていない。

〔表の差し込みの終わり〕出所のファイルを差し込んだ。足した印は無い。ほかの字は替えていない。

統計の標準の手続き（Fisher の正確検定・Holm の手続き・Newcombe の区間・Wilson の区間）は、元の文献を引かず、手続きと型を節 2.3 に書いた（Fisher の正確検定は両側・Holm の後の p の組み方・区間は連続の補正の無い Wilson の区間と、それを組んだ Newcombe の hybrid score）。決まりの逐語は付録 I にある。引く文献を本文を読んだものに限る決まりのため、この版では元の文献を読むための取得をしていない（決定 D450-4）。

凍結した日本語の送る文の登録の本文の代替説明の項（節 9.1 の引用）が触れる文献は、凍結のときに起草者が文献の表の行だけを見たもので、この章の文献の読みとは別の時である。その文献の表の三行（公開の置き場の `records/reviews/round1/review-materials-verbatim.md` 424〜426 行）は、arXiv:2604.11120・arXiv:2509.08075・arXiv:2606.26161 で、どれもこの章の一覧にある（arXiv の番号で照らした）。

Chen ほか（arXiv:2606.08310）の読んだ版（v2）の HTML の頁の題は「…Ethical Reasoning and Authorization Actions…」で、arXiv の API の題と一語違う（書誌は API の題で書いた）。
