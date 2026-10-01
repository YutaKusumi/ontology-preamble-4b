# -*- coding: utf-8 -*-
"""make_adoption_table_final.py v0（2026-09-30・B′ の器の実装の検分の採否の表の最終版・コーディネータ南無弥勒如来・非公開）。
採否の表の草案四（`make_adoption_impl.py` v0.3 の行と追い問いの節）に、行ごとの結果（直した器と版・記録の注・限界・決め）の欄を足して、凍結の器が求める名
（`adoption-table-impl-Bprime.md`・移し方の表で `records/reviews/Bprime/impl/`）に書く。草案四の器と草案四の本文は変えない。
確かめ（器の自己検査と合成データの正式の確かめの取り直し〔五の凍結と錠の道を含む〕）の結果は、その記録を指す（この表は結果の値を持たない）。
用法: python make_adoption_table_final.py [--force]
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_adoption_impl as MA

VERSION = 'v0'
NL = chr(10)
OUTCOMES = {
    'U01': 'dry_run v0.6〜v0.9: 閉包と SHA の表を公開の形の置き場で取る・別の個体の二つの器のバイトを始めと終わりで照らす・五で凍結の器が記録を読む。freeze v0.2: 閉包の始めの器が無ければ止める・作業の置き場の読み替え',
    'U02': 'boot v0.4: form_items_check（六項目・時差つきの時刻・相 extract の起動の記録の器の SHA を台帳の差分でつなぐ・二つ以上は器の誤りの記録と台帳のやり直しの行・項目ごとの合否と照らした相）・起動の記録に台帳の行の数。dry_run v0.6〜v0.9: 通る形と六つの落ちる形',
    'U03': 'core v0.2: LOCK_EXCLUDED と lock_bad。freeze v0.2: 七つ目・除く器を正本と照らす。analyze v0.4: 一致だけを見る段と開く段。build_report v0.3: 本番の入口の頭。正本 v5 `computation.main_freeze.lock_excluded`',
    'U04': 'core v0.2: runs_table・runs_bad・reruns_of。freeze v0.2: 八つ目。analyze v0.4: 開く段が runs を読んで置く（外れは止める）。build_report v0.3: 報告の頭の走行の表を読み直して照らす。sweep v0.1。正本 v5 `computation.start_records`',
    'U05': 'boot v0.4: 錠を関数 gate_bad に（暦の期限の型の誤りも直した・K25）。dry_run v0.6〜v0.9 の五: 凍結・封印・錠の通る形と止まる形・起動の記録のコミット・本の凍結・集計の DRY でない枝・報告の本番の入口',
    'U06': 'freeze v0.2: 自己検査の一覧（移す器は例だけの閉じた検査・別の個体の二つの器は合成データの記録の三の部の行）。publish_map v0.2: --selftest-examples',
    'U07': 'close_behavior v0.2: 器の誤りで閉じた記録に系統外の採点ができなかった文・理由の閉じた一覧・やり直しの道。build_report v0.3・sweep v0.1・analyze v0.4 が受ける。正本 v5。dry_run v0.6〜v0.9: 器の誤りで閉じた枝',
    'U08': 'analyze v0.4: 組の間の照らしを中身に・層三の照らしを戻した。boot v0.4: 器の SHA16 を閉包で・session に本の凍結の節の SHA16 と npz の SHA-256。正本 v5 `computation.start_records.procedure`。dry_run v0.6〜v0.9 の五: 組ごとに違うコミット',
    'U09': 'core v0.2: run_record_name。boot v0.4: 名にセッション。close_behavior v0.2: 名の読み方とやり直しの道。正本 v5 `computation.start_records.names`・`reruns`',
    'U10': 'freeze v0.2: 本の凍結の節の SHA16 を記す。boot v0.4: 起動の記録の凍結と封印の SHA16 を run で照らす・錠で節の SHA16。analyze v0.4: 組ごとに照らす。正本 v5 `computation.main_freeze.section_sha16`',
    'U11': 'freeze v0.2: 本の凍結の節の実際の鍵を閉じた一覧と照らす・自己検査',
    'U12': 'boot v0.4: 相 pilot の起動の記録に閉じた記録の SHA16・run で種類と正本の SHA と runs を照らす。dry_run v0.6〜v0.9: 差し替えで止まる形',
    'U13': 'close_behavior v0.2・send_external v0.1: 改行を訳さずに読み、SHA はバイトで・自己検査に \\r',
    'U14': 'build_report v0.3: 要約の型を §0 と読みの節に同じ字で・自己検査で照らす',
    'U15': 'build_report v0.3: 報告の頭に見分ける力の無い位置の定型の文（下見と本の計算の頭の数）',
    'U16': 'g4_attempts_Bprime v0（新しい器）: 試みの記録（つながり・画面の写しの SHA）・日の数え・閉じた記録と定型の文・錠が見る。core v0.2: 封印の時刻より後・ISO の時刻も読む（K27）',
    'U17': 'analyze v0.4: 升目の二つの組のどちらかで印（二つの値を置く）。正本 v5 `floor_margin.mark`（草案11 §4.3・登録者の確認を待つ）',
    'U18': 'bprime_run v1.3: 語彙の行列の float32 の写しを模型ごとに一つ',
    'U19': 'boot v0.4: k とバッチの既定の値は DRY だけ',
    'U20': 'boot v0.4: start の段で組を照らす',
    'U21': 'bprime_run v1.3: k の測りでバッチのすべての行',
    'U22': 'core v0.2・bprime_behavior v1.1・bprime_phases v0.2: 続きの振り分けに升目の選択の字',
    'U23': 'bprime_external v1.1: catastrophe を型で',
    'U24': 'boot v0.4: 本番でも OP4B_PUB_TOOLS',
    'U25': 'make_frozen v0.1: 逐語の改行を先に拒む（元を草案11 に）',
    'U26': 'close_behavior v0.2: 試行ごとの採点の当て直し',
    'U27': 'bprime_phases v0.2: ノルムと次元を値から・三つ目は注',
    'U28': 'publish v0.2: 移し方の記録を一度だけ（写す前に照らす・後は別の名）。freeze v0.2: 凍結物に入れる。正本 v5 `computation.frozen_text.publish_record`',
    'U29': '正本 v5: 文の型を（〔理由〕）に・理由の一覧。close_behavior v0.2・build_report v0.3: 埋める',
    'U30': 'make_impl_bundle v0.3: 分け方を直し・説明を目録に',
    'U31': '器の説明の版を器の版にそろえ、凍結の器の説明は八つ。秒の違いの由来は器の段の記録に書いた',
    'U32': '公開の置き場に `.gitattributes`（records と tools を LF）を置く（push の時に登録者の確認・D275）。まだ置いていない',
    'U33': 'freeze v0.2: 下見の前の凍結の記録の注。core v0.2: 自己検査の説明の字',
    'U34': 'freeze v0.2: 測った k での出口の値の下限を記録に一行（z_floor・票の数と小数一桁で一致）',
    'U35': 'freeze v0.2: 記録の注', 'U36': 'freeze v0.2: 記録の注', 'U37': '変えない（freeze v0.2: 記録の注）', 'U38': 'freeze v0.2: 記録の注', 'U39': 'freeze v0.2: 記録の注',
    'U40': '限界（正本 v5 `limits.bprime`・草案11 §10・D275）',
    'U41': '決めの材料（正本 v5 `independent_recompute.nk_material`・決めは `independent_recompute.nk_decision`）',
    'U42': 'boot v0.4: 別の個体の器の読み込みを始めに確かめる', 'U43': 'boot v0.4: 別の個体の器の SystemExit を器の誤りとして受ける',
    'U44': 'analyze v0.4: 比べる行と二つの道の鍵の集合（DRY でも外さない）', 'U45': 'dry_run v0.6〜v0.9: 小さな模型の層の倍率の行',
    'U46': 'dry_run v0.6〜v0.9: 出口の値の大きさの行と、出口の値を大きくした枝（語彙の行列を大きくした小さな模型で一段目）。boot v0.4: DRY だけの OP4B_DRY_WSCALE',
    'U47': 'freeze v0.2: 記録の注', 'U48': '限界（正本 v5 `limits.bprime`・草案11 §10・D276）', 'U49': 'freeze v0.2: 記録の注', 'U50': 'boot v0.4: 列の長さと窓の照らし', 'U51': '変えない',
    'U52': 'freeze v0.2: 決定性の四つの値と k の項目の合否と形',
}
MORE = [('K26', '下見が止めたときの報告を組む入口が器に無かった（直しの中で読んで見つけた）', 'analyze v0.4: 段 stopped（止めたときの集計の出力）・build_report v0.3 の本番の入口が読む'),
        ('K27', '芯の G4 の日の数えが封印の記録の ISO の時刻を読めなかった（G4 の器を書く中で見つけた）', 'core v0.2: ISO の「T」つきも読む・自己検査'),
        ('K25', '起動器の錠の暦の期限の照らしが時刻の形を取り違え、封印の後のどの相でも例外になる形だった（読んで見つけた）', 'boot v0.4: 錠を関数に切り出して時刻の文字列を渡す（U05）')]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    out = os.path.join(HERE, 'adoption-table-impl-Bprime.md')
    if os.path.exists(out) and '--force' not in sys.argv:
        raise SystemExit('既にある（--force で書き直す）: %s' % out)
    rows = MA.ROWS
    miss = [r[0] for r in rows if r[0] not in OUTCOMES]
    extra = [u for u in OUTCOMES if u not in {r[0] for r in rows}]
    if miss or extra:
        raise SystemExit('結果の欄と表の行がそろわない: %s %s' % (miss, extra))
    esc = lambda s: s.replace('|', '\\|')
    L = ['# B′ の器の実装の検分の採否の表（最終・結果の欄つき・2026-09-30・コーディネータ南無弥勒如来）', '',
         '- 元: 採否の表の草案四（`adoption-impl-Bprime.md`・`make_adoption_impl.py` %s・行 %d）。票・追い問い・決め方は草案四のとおり。この表は、行ごとの結果（直した器と版・記録の注・限界・決め）を足した。' % ('v0.3', len(rows)),
         '- 確かめ: 器の自己検査と、合成データの正式の確かめの取り直し（Colab・`dry_run_Bprime.py` v0.9・一〜四の記録 `records/Bprime/dry-run-Bprime-2026-09-30.md` と、五〔凍結と錠の道〕の記録 `records/Bprime/freeze-path-dry-Bprime-2026-09-30.md`・走りの順と確かめの器の直しは器の段の記録）で見る。この表は確かめの値を持たない。',
         '- 正本と草案: 設計に触れる直しは正本 v5（`design/contrasts-Bprime.json`）と草案11（`design/design-Bprime-draft11.md`）に写した（登録者の確認を待つ）。器の版と所見は器の段の記録（`tools/tools-log-Bprime.md`）。', '',
         '| 番号 | 出所 | 票の重さ | 採否 | 扱い | 直し方の案・理由 | 結果 |', '|---|---|---|---|---|---|---|']
    for u, src, sev, dec, how, chk, fix in rows:
        L.append('| %s | %s | %s | %s | %s | %s | %s |' % (u, esc(src), sev, dec, how, esc(fix), esc(OUTCOMES[u])))
    L += ['', '## 直しの中で見つけた所（器の段の所見）', '', '| 番号 | 何 | 直し |', '|---|---|---|'] + ['| %s | %s | %s |' % (a, esc(b), esc(c)) for a, b, c in sorted(MORE)]
    L += ['', '## この表が確認していないこと', '',
          '- 直した器の当否（器の自己検査と合成データの正式の確かめの取り直しで見る・直しの確かめの巡を足すかは登録者の決め）。',
          '- 票と追い問いの返事が読んでいない所（草案四の「この表が確認していないこと」のとおり）。', '', MA.CLAUSE, '']
    with open(out, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(L))
    print('書いた %s（%d 行・直しの中の所見 %d）' % (os.path.basename(out), len(rows), len(MORE)))


if __name__ == '__main__':
    main()
