# 器の記録（中間総括の検分の一巡目・2026-10-02・コーディネータ南無弥勒如来）

- `save_round1_vote.py` v0: B′ の結果の巡の保存の器を写し、置き場と許しの記し方だけを替えた。五つの票の保存に同じ版を使った（gemini-1 の meta の `model_label_note` の定型の文は AI Studio の機種の欄に合わない・受け取りの記録に書いた）。
- `cut_permission_round1.py` v0: 登録者の許しを会話の記録から切り出した（`permission-round1.json`）。
- `write_sending_log_round1.py` v0・`write_receiving_log_round1.py` v0: 送りと受け取りの記録を書いた。
- `make_repro_round1.py` v0: 票の事実の主張を記録に照らした（`repro-round1.json`・`repro-round1.md`）。「一部」の二件（B-one・BL-gate）は、器の問いを「草案に無いこと」と立てたためで、文は草案の別の節に在る（採否の表の Y17 と検分票）。
- `make_adoption_round1.py` **v0 → v0.1**: v0 は書く前の照らしを持たず、`adoption-table-round1.md` を一度書いた（2026-10-02 10:35:14 日本時間のファイルの時刻・SHA-256 F5C119FDF8641954CBC5B9F8F106FEDF97BC285B88060A25010F2964D232DD4F）。直後に照らしの器 `check_adoption_quotes_round1.py` v0 を当てると、「」の中身のうち四つが元の文と一字違わずではなく（「想定方向」の内側の鉤括弧を落とした形・二つの列名を一つに縮めた形・gemini-1 の申告の言い換え）、一つは起草者の付けた名、二つは照らしの集まりに計算の出力を入れていなかったための見落としだった。数は 47 すべて在った。
  - 経緯: 照らしを器に足す直しを当てる一つの呼び出しの中で、直しが当たらずに止まった後、続けて書いてあった試しの走り（`--dry` のつもり）が v0 のまま走り、照らしなしで書いた。
  - 扱い: v0 の出力は消さず `adoption-table-round1-build1.md` に名を替えて残した。v0 の器は `prev/make_adoption_round1-v0.py`。v0.1 は「」の言い回しを直し、照らしの器を書く前に走らせ、通らなければ書かない。v0.1 の出力 `adoption-table-round1.md`（SHA-256 83BA55E12B206A585B64CC5BA9DDA39135B750B6346F2784A2A55E60B192A4A9）は照らしを通った（「」の欠け 0・数の欠け 0）。
- `check_adoption_quotes_round1.py` v0: 照らしの集まりに計算の出力の md を足した（v0 の内で、v0.1 の採否の表を書く前）。
- この記録を書いた時刻: 2026-10-02 10:37:41（日本時間）。
- `make_adoption_round1.py` **v0.1 → v0.2**（2026-10-02 10:38:30 日本時間に追記）: 書いた表を読み直して、Y08 の行の式（上向きと下向きの絶対値の差を縦棒で書いた形）が Markdown の表の区切りとして読まれ、行が崩れることに気づいた。v0.1 の出力（SHA-256 83BA55E12B206A585B64CC5BA9DDA39135B750B6346F2784A2A55E60B192A4A9）は `adoption-table-round1-build2.md` に名を替えて残し、v0.1 の器は `prev/make_adoption_round1-v0.1.py`。v0.2 は式を言葉に替え、表の行の縦棒の数を書く前に確かめる。v0.2 の出力 `adoption-table-round1.md`（SHA-256 CBF5710115CB8BF8AA007ECDBA0BFDF207FB4F6E3A61A0ED27DCDBFBE3A79727）は、「」と数の照らしと縦棒の数の確かめを通った。内容は v0.1 と式の一か所と頭の一行だけが違う。

本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
