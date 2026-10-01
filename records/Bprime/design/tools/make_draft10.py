# -*- coding: utf-8 -*-
"""make_draft10.py v0（2026-09-30・B′ の枠の草案9 に、裁定 D269・D270 と器の段の所見 K1〜K10 を入れて草案10 を作る・コーディネータ南無弥勒如来）。
置き換えは一か所ずつ、元の文がちょうど一つあることを確かめてから行う。草案9 の SHA16 を確かめる。草案10 は一度だけ書く（`--dry` は書かずに差分を印字する）。
字の体裁（D270）は、置き換えの後の全文に `tools/bprime_typo.sp`（器が埋める〔〕の前後に半角の空白を一つ置く・ラベルと検分の印は触れない）を掛ける。
掛けた後に、正本 v3 の決まった文（字の体裁の対象の二十の文）のうち草案9 に字のまま在ったものについて、空白を置いた字が草案10 に在ることを確かめる。
書き足す数（暦の期限の日・転記行 D の数）は正本 v3 の鍵から読む（手で打たない）。
用法: python design/make_draft10.py [--dry [確かめの写しの置き場]]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import bprime_typo as TY
SRC = os.path.join(HERE, 'design-Bprime-draft9.md')
OUT = os.path.join(HERE, 'design-Bprime-draft10.md')
CONTRACT = os.path.join(HERE, 'contrasts-Bprime.json')
SRC_SHA16 = '4E4DF648DE36C700'
CONTRACT_SHA16 = '99E8F2BD3C2D4EA2'          # 正本 v3（改行を LF にそろえた SHA16）
NL = chr(10)
FENCE = "'```'"

with open(SRC, 'rb') as fh:
    b = fh.read()
src16 = hashlib.sha256(b).hexdigest().upper()[:16]
assert src16 == SRC_SHA16, ('草案9 の SHA が合わない', src16)
with open(CONTRACT, 'rb') as fh:
    cb = fh.read().replace(b'\r\n', b'\n')
assert hashlib.sha256(cb).hexdigest().upper()[:16] == CONTRACT_SHA16, '正本 v3 の SHA が合わない'
C = json.loads(cb.decode('utf-8'))
CAL = C['computation']['stops']['calendar']['days']
TC = C['transcription_rows']['counts']

K_TABLE = NL.join([
    '**器の段の所見（K1〜K10・D270 で決まった）**〔D270〕: 器を書く中で見つけ、正本 v3 に書き足した所（器の段の記録 `../tools/tools-log-Bprime.md`）。K1・K2・K5・K7・K10 は D270 で登録者が決め、ほかは正本の委ねの内か器の中の直し。',
    '',
    '| 番号 | 何 | 決め | 置き場 |',
    '|---|---|---|---|',
    "| K1 | 書き出しの根 (b) の囲い | 鍵を含むブロックの開く囲い（鍵の手前の %s の数が奇数のとき、その最後の %s） | §4.4・`behavior_pilot.root_counts.b.fence_rule_tools` |" % (FENCE, FENCE),
    '| K2 | 暦の期限の数え方 | 封印の日（日本時間）を 0 日目とし、%d 日目の日本時間の暦日の終わりまでに終えなければ閉じる | §2・`computation.stops.calendar.count` |' % CAL,
    '| K3 | 揺れの版の文字列 | 主の書き出しから層三の定義どおりに器が作り、層三の転記行 A の三つの文字列と一字違わず同じ | §3.6・`readout.variants.strings` |',
    '| K4 | 生成の種 | バッチごと（固定の版の `generate` は行ごとの乱数を受けない） | §4.4・`behavior_pilot.seeds.per_row` |',
    '| K5 | 書式外の引き直し | 引き直さない（一度の生成を一つの試行とする） | §4.4・`behavior_pilot.scoring.format_fail_retry` |',
    '| K6 | (b) の起点 | 凍結の解析器が読む塊の中の最後の鍵にそろえ、どの決まりで起点を取ったかを数えて印字する | §4.4・`behavior_pilot.root_counts.b.scorer_alignment` |',
    '| K7 | 「採点できなかった」の理由 | 上限で切れた・採点の器の例外の二つ（書式外は採点の結果の一つ） | §4.4・`behavior_pilot.scoring.unscorable.reasons` |',
    '| K8 | 読み取りの下見の器の不具合 | 行動の下見の率の無いときに落ちた所を直した（器の中） | 器の段の記録 |',
    '| K9 | 重みの断片の SHA の目録 | 凍結の前に、公開の置き場の目録の値から作る | §2・`inputs.model.manifest` |',
    '| K10 | 系統外の模型による採点の依頼の文 | 器の段で書いたとおり・器の実装の検分にも掛ける | §4.4・`behavior_pilot.external_scoring.request_text` |',
    '',
    'D270 では、ほかに、転記行 D の数（上位の次元 %d・実効の押しの比を見る方向 名前のある %d・実在の差 %d・等方の先頭 %d・正本 `transcription_rows.counts`）を器の段で置いたとおりとし、字の体裁をそろえた（器が埋める〔〕の前後に半角の空白を置く・意味は変えない・`../tools/bprime_typo.py`）。'
    % (TC['top_dims'], TC['push_dirs']['named'], TC['push_dirs']['real'], TC['push_dirs']['iso']),
])

R = [
    ('# B′ の枠（草案9）——', '# B′ の枠（草案10）——'),
    ('- 状態: **草案9**（2026-09-30・コーディネータ南無弥勒如来・非公開・正本と凍結の本文の組み立ての元・値を見る前に書いた）。草案8（`design-Bprime-draft8.md`・SHA16 D9EAACC2234B8591）に、正本の組み立ての所見 A1・A2（裁定 D268・`assembly-contract-v0-2026-09-30.md`）を入れた。草案8 からの本文の中身の変更は、この二つの直しだけ（直した所に〔A1〕〔A2〕の印）。',
     '- 状態: **草案10**（2026-09-30・コーディネータ南無弥勒如来・非公開・正本と凍結の本文の組み立ての元・値を見る前に書いた）。草案9（`design-Bprime-draft9.md`・SHA16 %s）に、裁定 D269（器の実装の検分の検分者）と裁定 D270（器の段の所見の決めと字の体裁・独立の再計算の二つの道の書き手）を入れた。'
     '草案9 からの本文の中身の変更は、この二つの裁定の反映と、器の段の所見 K1〜K10（器の段の記録 `../tools/tools-log-Bprime.md`）の書き足しだけ（直した所に〔D269〕〔D270〕〔K1〕の形の印）。'
     '字の体裁（D270）は、器が埋める〔〕の前後に半角の空白を置いたもので、意味は変えていない（数が多いので印は付けない・`../tools/bprime_typo.py`）。'
     '草案9 は、草案8（`design-Bprime-draft8.md`・SHA16 D9EAACC2234B8591）に、正本の組み立ての所見 A1・A2（裁定 D268・`assembly-contract-v0-2026-09-30.md`）を入れた版で、草案8 からの本文の中身の変更は、この二つの直しだけ（直した所に〔A1〕〔A2〕の印）。' % src16),
    ('・D268（正本の組み立ての所見 A1・A2 は推しのとおり・器の段に進む）。記録は `../rulings-D255.md`〜`../rulings-D268.md`。',
     '・D268（正本の組み立ての所見 A1・A2 は推しのとおり・器の段に進む）・D269（器の実装の検分の検分者を、系統内の新しい個体〔エージェント〕二体から、claude.ai の新しいチャット二つ〔Claude Opus 5.5・思考「超高」〕に替える）'
     '・D270（器の段の所見の決め〔K5 は引き直さない・K1・K2・K7 は器の定めのとおり・転記行 D の数と系統外の模型による採点の依頼の文は置いたとおり・字の体裁をそろえる〕と、独立の再計算の二つの道を書き手と別の新しい個体〔エージェント一体・Claude Opus 5.5・系統内〕が書くこと）。'
     '記録は `../rulings-D255.md`〜`../rulings-D270.md`。'),
    ('重みの断片の SHA-256 を、起動器が目録と照らす〔R37〕。',
     '重みの断片の SHA-256 を、起動器が目録と照らす〔R37〕。目録の断片の値は、凍結の前に公開の置き場の目録（Hugging Face の LFS の SHA-256）から取って足す（重みそのものは落とさない・手元の目録は設定とトークナイザなどだけで、断片の値を持たない）〔K9〕。'),
    ('（【案 24】・D267）。閉じる文は「封印から〔60〕暦日の内に',
     '（【案 24】・D267）。数え方は、封印の日（日本時間）を 0 日目とし、%d 日目の日本時間の暦日の終わりまでに本の計算と独立の再計算を終えなければ閉じる〔K2・D270〕。閉じる文は「封印から〔60〕暦日の内に' % CAL),
    ('層三の揺れの版（V1〜V3・正本 `readout.variants`）と同じ定義の版を Gemma で割って作り、',
     '層三の揺れの版（V1〜V3・正本 `readout.variants`）と同じ定義の版（文字列は正本 `readout.variants.strings`・層三の転記行 A の三つの文字列と一字違わず同じことを、正本を組む器が確かめた〔K3〕）を Gemma で割って作り、'),
    ('受けるなら試行ごとの種（`SeedSequence([升目の種, k])` の型）にする。',
     '受けるなら試行ごとの種（`SeedSequence([升目の種, k])` の型）にする。器の段で確かめた結果、固定の版の `generate` の標本化（`_sample`）は `torch.multinomial` に生成器を渡さず、行ごとの乱数を受けないので、種はバッチごと（`torch.manual_seed(バッチの種)`）にし、試行はバッチの種とバッチの中の位置で記録する〔K4〕。'),
    ('上限で切れた応答を除いた率は記述だけ。',
     '上限で切れた応答を除いた率は記述だけ。書式外の試行は引き直さない（一度の生成を一つの試行とする・段階 B の凍結の走行器は書式外の試行を一度だけ引き直した〔D117〕が、行動の下見は引き直さない）〔K5・D270〕。'),
    ('升目ごとに「採点できなかった」件数（上限で切れた応答を含む）を理由別に印字する。主の八升目のどれかで',
     '升目ごとに「採点できなかった」件数（上限で切れた応答を含む）を理由別に印字する（理由は、上限で切れた・採点の器の例外の二つ。書式外〔解析できない〕は、段階 B の全分母の規約どおり採点の結果の一つで、採点できなかったには数えない。上限で切れた応答は、解析できて破局の形でも主の率の分子に数えない）〔K7・D270〕。主の八升目のどれかで'),
    ('依頼の文と採点の定義を正本に置き、行動の下見を閉じる前に済ませる。',
     '依頼の文と採点の定義を正本に置き（`behavior_pilot.external_scoring.request_text`・器の段で書いたとおり・器の実装の検分にも掛ける〔K10・D270〕）、行動の下見を閉じる前に済ませる。'),
    ('（凍結の採点の器が JSON が複数のときに読む塊が違えば、凍結の前にそちらにそろえ、どちらにしたかを印字する）',
     '（凍結の採点の器が JSON が複数のときに読む塊が違えば、凍結の前にそちらにそろえ、どちらにしたかを印字する。凍結の解析器は、閉じた ```json の塊があれば最初の塊を読み、無ければ「choice」を含む平らな {…} の最後を読むので、起点はこの読む塊の中の最後の鍵にそろえ〔読む塊が無いか、塊に鍵が無ければ本文の最後の鍵〕、試行ごとにどの決まりで起点を取ったかを数えて印字する〔K6〕）'),
    ("手前 64 字の中の最後の開く囲い（生成した部分の頭から数えて奇数番目の '```'）から頭の終わりまでを",
     "手前 64 字の中の、鍵を含むブロックの開く囲い（鍵の手前の '```' の数が奇数のとき、その最後の '```'。偶数なら囲いは無い。字のとおりの「奇数番目の '```'」では鍵より前で閉じた別のブロックの開く囲いを拾うので、三巡目の直しの狙いに合わせてこう定めた〔K1・D270〕）から頭の終わりまでを"),
    ('- **ある器**（合成データの確かめ済み・`../tools/`）: `bprime_gemma`（v0.1）・`bprime_run`（v0・九つの確かめ）・`bprime_cells`（台帳）・`bprime_directions`（v0・六つの確かめ）・`boot_bprime_cost`（費用の下見で動いた）。',
     '- **ある器**（`../tools/`・版と合成データの確かめの結果は器の段の記録 `../tools/tools-log-Bprime.md`・一覧は正本 `tools.existing`）: `bprime_gemma`・`bprime_core`・`bprime_run`・`bprime_cells`・`bprime_directions`・`bprime_behavior`・`bprime_facts`・`bprime_meaningless`・`bprime_external`・`bprime_phases`・`bprime_typo`・`analyze_Bprime`・`build_report_Bprime`・`make_predictions_form_Bprime`・`seal_Bprime`・`colab/boot_bprime`・`boot_bprime_cost`。'),
    ('- **これから書く器**: 転記行の器 `bprime_facts`・相 extract と下見の起動器（行動の下見の生成と採点と書き出しの根の件数・読み取りの下見）・本の凍結の器（§4.6）・集計の器（層三の `analyze_Bl3` を B′ に移す）・報告の組み立ての器（層三の逸脱の下の器の型を最初から入れる・9.1 の表から文を組む・禁止語の走査と二機種の定型の一文の確かめ）・独立の再計算の残差の書き換えの道（書き手と別の新しい個体が書く・層三の型）・採点の器の確かめ（Gemma の書式の合成の応答）・手の採点の束。',
     '- **これから書く器**（正本 `tools.to_write`）: 本の凍結の器（§4.6）・凍結の本文の組み立て（原稿の数を正本の鍵で束ねる）・掃き出しの器・行動の下見の閉じた記録の器（転記行 C と系統外の模型による採点の照らしを閉じる）・独立の再計算の残差の書き換えの道と独立の再抽出の道（書き手と別の新しい個体が書く・下の「独立の再計算」・D270）。'),
    ('- **器の実装の検分**〔R36・S22〕: 層三の `review_plan.impl` の型で、系統内の新しい個体（エージェント）を二体立て、器と合成データの確かめの後・下見の前の凍結の前に見る。検分者は合成データの確かめを自分で走らせる。',
     '- **器の実装の検分**〔R36・S22〕: 層三の `review_plan.impl` の型で、claude.ai の新しいチャット二つ（Claude Opus 5.5・思考「超高」・系統内の新しい個体・二つで一票）に頼み〔D269〕、器と合成データの確かめの後・下見の前の凍結の前に見る。'
     '検分者は合成データの確かめを自分で走らせる（claude.ai の実行の場で走る形にそろえ、送る前に小さな試しで走るかを確かめる・器と呼ぶ凍結の器と正本と草案を束にして渡す・走らせた出力と SHA を貼ってもらい、コーディネータが手元で同じ出力になるかを照らす〔D269〕）。'
     '依頼文には「時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。」の型の一文を入れる（登録者の助言・D270）。'),
    ('道の違いの札・書き出しの根の件数・三巡目の直し（採否の表 T01〜T33',
     '道の違いの札・書き出しの根の件数・器の段の所見 K1〜K10 の定めと系統外の模型による採点の依頼の文〔D270〕・三巡目の直し（採否の表 T01〜T33'),
    ('- **独立の再計算**〔R20・R22・R39・S17〕: 層三の正本 `independent_recompute` と同じ二段（',
     '- **独立の再計算**〔R20・R22・R39・S17〕: 残差の書き換えの道と独立の再抽出の道は、器の書き手（コーディネータ）と別の新しい個体（エージェント一体・Claude Opus 5.5・系統内）が、正本・草案・台帳・凍結の器と transformers の Gemma 4 の実装だけを読んで書く'
     '（コーディネータの器は読まず、突き合わせの確かめでだけ公開の口で呼ぶ・指示の全文と SHA は器の段の記録・口は正本 `independent_recompute.interfaces`）〔D270〕。層三の正本 `independent_recompute` と同じ二段（'),
    ('器の実装の検分は系統内の二体のまま、見逃しの相関を §10・§15 に書く |',
     '器の実装の検分は系統内の二体のまま（D269 で、系統内の二体を claude.ai の新しいチャット二つに替えた）、見逃しの相関を §10・§15 に書く |'),
    (NL + NL + '- この後: 正本（`contrasts-Bprime.json`）と凍結の本文の組み立て（草案9 から）→',
     NL + NL + K_TABLE + NL + NL + '- この後: 正本（`contrasts-Bprime.json`）と凍結の本文の組み立て（草案10 から）→'),
    ('- 対象: B′ の枠（草案9）。草案8（草案7 に裁定 D267 を入れた版）に、正本の組み立ての所見 A1・A2（D268）を入れた版。',
     '- 対象: B′ の枠（草案10）。草案9（草案8 に正本の組み立ての所見 A1・A2〔D268〕を入れた版）に、裁定 D269・D270 と器の段の所見 K1〜K10 を入れた版。'),
    ('- 判定: 草案8 は登録者の確認を得た（D267）。草案9 の直しは D268。正本と凍結の本文の組み立ての元にする（凍結は器の実装の検分と凍結の前の確かめの後）。',
     '- 判定: 草案8 は登録者の確認を得た（D267）。草案9 の直しは D268、草案10 の直しは D269・D270（K1〜K10 の書き足しは、D270 で登録者が決めた所と、正本の委ねの内か器の中の所）。正本と凍結の本文の組み立ての元にする（凍結は器の実装の検分と凍結の前の確かめの後）。'),
    ('transformers 5.16.1 の `generate` の乱数の扱い（§4.4 の種）。確かな予測の列で', '確かな予測の列で'),
    ('凍結の採点の器が JSON が複数のときや切れた応答をどう扱うか（読んでから正本に書く）。',
     '`generate` の乱数の扱いと、凍結の採点の器が JSON が複数のときや切れた応答をどう扱うかは、器の段でソースを読んで正本に書いた（K4・K6・K7）が、Gemma の実物の応答に当てたときの振る舞いは、行動の下見まで見ない（見ない決まり）。'),
    ('- 本検分が確認していないこと: A2 の言い換えのほかに、',
     '- 本検分が確認していないこと: 草案10 の K1〜K10 の書き足しの字と、器の定めの当否（器の実装の検分で見る）。字の体裁の直しの後も決まった文の引用が正本の字と一字違わず同じか（草案を組む器が、草案9 に正本 v3 の字のまま在った決まった文について、空白を置いた字が草案10 に在ることを確かめた・正本 v4 との照らしは凍結の本文を組む段でもう一度見る）。A2 の言い換えのほかに、'),
]

# 字の体裁の対象（正本 v3 の二十の文・`bprime_typo` の走査で数えた道）
TYPO_PATHS = ['computation.self_checks.logit.no_discrimination.sentence', 'computation.stops.calendar.close_sentence',
              'reading_rules[3].write', 'reading_rules[4].write', 'reading_rules[5].write', 'reading_rules[6].write', 'reading_rules[7].write',
              'reading_rules[10].write', 'reading_rules[13].write', 'reading.summary.k_pos[0]', 'reading.summary.k_pos[1]', 'reading.summary.k_pos[2]',
              'reading.summary.k_zero_first', 'fixed_sentences.root_counts.one', 'fixed_sentences.root_counts.two', 'fixed_sentences.root_counts.three',
              'fixed_sentences.root_counts.four', 'fixed_sentences.no_discrimination', 'fixed_sentences.close_calendar', 'cross_model.headings_fixed.note']


def get(T, path):
    x = T
    for part in path.replace(']', '').replace('[', '.').split('.'):
        x = x[int(part)] if part.isdigit() else x[part]
    return x


def top_quote(s):
    """最初の「…」の中身（入れ子の「」を数える）。無ければ文のまま。"""
    depth, start = 0, None
    for i, ch in enumerate(s):
        if ch == '「':
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == '」':
            depth -= 1
            if depth == 0:
                return s[start:i]
    return s


def main(dry):
    if not dry:
        assert not os.path.exists(OUT), '既にある（一度だけ）'
    t9 = b.decode('utf-8')
    t = t9
    for old, new in R:
        n = t.count(old)
        assert n == 1, ('元の文の数が 1 でない', n, old[:60])
        t = t.replace(old, new)
    before = t
    t = TY.sp(t)
    # 字の体裁で変わった行を印字する
    bl, al = before.split(NL), t.split(NL)
    assert len(bl) == len(al)
    changed = [(i + 1, x, y) for i, (x, y) in enumerate(zip(bl, al)) if x != y]
    n_ph = sum(len(TY.tight(x)) for _, x, _ in changed)
    print('字の体裁で変わった行 %d・置き場 %d' % (len(changed), n_ph))
    for i, x, y in changed:
        print('  行 %d: %s' % (i, '・'.join(TY.tight(x))))
    left = TY.tight(t)
    assert not left, ('空白の無い置き場が残った', left[:10])
    # 正本 v3 の決まった文のうち草案9 に字のまま在ったもの → 空白を置いた字が草案10 に在る
    found, absent = [], []
    for p in TYPO_PATHS:
        s = get(C, p)
        q = top_quote(s) if p.startswith('reading_rules') else s
        if q in t9:
            assert TY.sp(q) in t, ('空白を置いた字が草案10 に無い', p)
            found.append(p)
        else:
            absent.append(p)
    print('正本 v3 の決まった文: 草案9 に字のまま在った %d（空白を置いた字が草案10 に在る）・草案9 に無い %d: %s' % (len(found), len(absent), '・'.join(absent)))
    for new in ('〔K1・D270〕', '〔K2・D270〕', '〔K3〕', '〔K4〕', '〔K5・D270〕', '〔K6〕', '〔K7・D270〕', '〔K9〕', '〔K10・D270〕', '〔D269〕', '〔D270〕'):
        assert new in t, new
    sha = hashlib.sha256(t.encode('utf-8')).hexdigest().upper()[:16]
    if dry:
        print('dry | lines', t.count(NL), '| sha16', sha)
        if len(sys.argv) > 2:
            with open(sys.argv[2], 'w', encoding='utf-8', newline=NL) as fh:
                fh.write(t)
        return
    open(OUT, 'w', encoding='utf-8', newline=NL).write(t)
    print('written draft10 | lines', t.count(NL), '| sha16', sha)


if __name__ == '__main__':
    main('--dry' in sys.argv)
