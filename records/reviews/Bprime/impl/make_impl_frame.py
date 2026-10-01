# -*- coding: utf-8 -*-
"""make_impl_frame.py —— B′ の器の実装の検分の枠（00-frame-impl-Bprime.md）を書く（2026-09-30・コーディネータ南無弥勒如来・非公開）。
SHA と数は実物から機械で写す（正本・草案・合成データの確かめの正式の記録・器の段の記録・実行の場の小さな試しの返事）。束の zip の SHA は束を作った後に別の行で足す。
用法: python reviews/impl/make_impl_frame.py <合成データの確かめの正式の記録（.md）>
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    dry_md = os.path.abspath(sys.argv[1])
    dry_js = dry_md[:-3] + '.json'
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    DJ = json.load(open(dry_js, encoding='utf-8'))
    probe = json.loads(re.search(r'```\s*(\{.*\})\s*```', open(os.path.join(HERE, 'probe', 'reply-probe-1', 'response.md'), encoding='utf-8').read(), re.S).group(1))
    log = open(os.path.join(BP, 'tools', 'tools-log-Bprime.md'), encoding='utf-8').read()
    ks = sorted({int(k) for k in re.findall(r'^- \*\*K(\d+)（', log, flags=re.M)})
    draft = os.path.join(BP, 'design', 'design-Bprime-draft10.md')
    rel = lambda p: os.path.relpath(p, HERE).replace(os.sep, '/')
    L = [
        '# B′ の器の実装の検分の枠（票を受け取る前に書く・2026-09-30・コーディネータ南無弥勒如来・非公開・草案）', '',
        '- 何か: 正本 `review_plan.impl`（裁定 D269・D270）に沿って、B′ の器の実装を claude.ai の新しいチャット二つ（Claude Opus 5.5・思考「超高」）に検分してもらう枠。**送るのは登録者の確認の後**。',
        '- 対象の版: 正本 `design/contrasts-Bprime.json`（版 %s・SHA16 %s）・草案10 `design/design-Bprime-draft10.md`（SHA16 %s）・器の段の記録 `tools/tools-log-Bprime.md`（所見 K%d〜K%d）。'
        % (C['version'], s16(os.path.join(BP, 'design', 'contrasts-Bprime.json')), s16(draft), ks[0], ks[-1]),
        '- 合成データの確かめの正式の記録: `%s`（SHA16 %s・%d のうち %d が期待どおり・Colab の CPU のランタイム・裁定 D271）。' % (rel(dry_md), s16(dry_md), DJ['n'], DJ['as_expected']),
        '- 束: `tools/make_impl_bundle_Bprime.py` で作る zip（公開の置き場の形・器・正本・草案・記録・呼ぶ凍結の器・`arms/`・設定とトークナイザ）。束の SHA-256 は束を作った後にこの枠の末尾に足す。',
        '- 依頼文: `request-impl-Bprime.md`（二つのチャットに同じ本文・役割の節だけ違える）。', '',
        '## 検分者と票', '',
        '- claude.ai の新しいチャット二つ（R1・R2）。二つで一つの系譜の票（系統内の新しい個体・D269）。前の設計の巡のチャットは使わない。',
        '- **系統外の目はこの巡に無い**。独立の再計算の二つの道の書き手（別の個体）の申し送り: 三つの道（フック・書き換え・再抽出）はどれも Claude 系が同じ指示から書いたので、指示の読み違いを共有すれば突き合わせでは捕まらない。'
        '→ 三つの道の実装を系統外（grok-4.7）に見てもらう一巡を足すかを、登録者に上げる（案・この枠の外）。', '',
        '## 役割（見る所を分ける・役割の外の所見も書いてよい）', '',
        '- **R1（計算）**: 読み取りの器 `bprime_run.py`・方向の器 `bprime_directions.py`・相の計算 `bprime_phases.py`・芯 `bprime_core.py`・集計 `analyze_Bprime.py`・行動の下見の器 `bprime_behavior.py`・'
        '独立の再計算の二つの道 `bprime_recompute_rewrite.py`・`bprime_reextract.py`。正本 `review_plan.impl.focus` のうち、softcap の見分ける力と許容の式・最後の層の自己検査の方向・両方の向きの組み方・床の余白の印・生成の設定と止める印・フックの順・採点の器・率の定義と区間・道の違いの札・書き出しの根の件数。',
        '- **R2（流れと記録）**: 起動器 `colab/boot_bprime.py`（相と段・起動の記録・出力の SHA・錠）・閉じる器 `close_behavior_Bprime.py`・系統外の模型による採点の束と依頼の文 `bprime_external.py`・`send_external_Bprime.py`・'
        '凍結の器 `freeze_Bprime.py`・封印 `seal_Bprime.py`・予想の書式 `make_predictions_form_Bprime.py`・凍結の本文 `make_frozen_Bprime.py`・移す器 `publish_Bprime.py`・`bprime_publish_map.py`・掃き出し `sweep_Bprime.py`・'
        '報告の組み立て `build_report_Bprime.py`・合成データの確かめ `dry_run_Bprime.py`。正本 `review_plan.impl.focus` のうち、本の凍結の錠・読みの規則の走査・三巡目の直し（T01〜T33）・起動の記録・器の段の所見と系統外の模型による採点の依頼の文。', '',
        '## 走らせてほしいこと（正本 `review_plan.impl.conditions`）', '',
        '- 実行の場の小さな試し（`probe/reply-probe-1/`）: Python %s・CPU %s・torch %s・transformers %s・pip で transformers 5.16.1 を落とせた（rc %s）。'
        % (probe['python'], probe['cpu_count'], probe['torch'], probe['transformers'], probe['pip_download_transformers_5_16_1']['rc']),
        '- 束の `README-impl-bundle-Bprime.md` のとおり、版を分けた置き場に numpy と transformers を入れ、torch の要らない器の自己検査と、transformers と tokenizers が要る器の自己検査を走らせてもらう。torch の要る器は走らせず、器の中と正式の記録を読んで照らしてもらう。',
        '- 走らせたコマンド・出力の末尾・束の目録の SHA と自分で計算した SHA を返事に貼ってもらい、コーディネータが手元で同じ出力になるかを照らす。', '',
        '## 返事の形（依頼文に書く）', '',
        '- 一行目に模型の名と作り手。所見ごとに: 番号・重さ（重い＝凍結の前に直す／中＝直す方がよい／軽い）・器とファイルと行・何が起きるか（入力 → 誤った出力か止まり方）・直し方の案・確信度・走らせて確かめたか読んで推したか。',
        '- 是認（見て問題が無かった所）も項目ごとに短く。読んでいない所・走らせていない所の申告。', '',
        '## 採否の決め方（先に書く）', '',
        '- 二つの票の所見を和集合で受け、採否の表（U01〜）に「採用・一部採用・不採用」と理由を書く。総評は裁定にしない。',
        '- 「重い」と書かれた所見と判断に迷う所見は、追い問いで確かめてから決める。票の主張の前提は、コーディネータが一次の資料（器の本文・走らせた出力）で確かめ、出所を書く。読了や確認の申告は、追い問いで確かめるまで検査と数えない。',
        '- 採った直しは器の版を上げ（前の版は `tools/prev/`）、自己検査と合成データの確かめを走らせ直す。直しが大きいときは、層三の D238 の型で直しの確かめの巡を足すかを登録者に上げる（顔ぶれは grok-4.7 一票と系統内の新しい個体・正本 `review_plan.impl.recheck`）。',
        '- 正本と草案の字を変える直しは、草案11 と正本 v5 にまとめて登録者の確認に上げる。', '',
        '## 予想（外れても消さない）', '',
        '| 何 | 予想 | 信頼度 |', '|---|---|---|',
        '| 少なくとも一つのチャットが「重い」を一つ以上挙げる | はい | 中 |',
        '| 器どうしの口の食い違い（K18・K19・K21 と同じ種類）がまだ見つかる | はい | 中 |',
        '| 自己検査の合成の値が通らない枝（K23 と同じ種類）の指摘が出る | はい | 中 |',
        '| 実行の場で torch の要らない器の自己検査がすべて通る | はい | 中 |',
        '| 二つのチャットの「重い」の所見が重なる | いいえ | 低 |', '',
        '## COI（事実のみ）', '',
        '- 起草者（コーディネータ）は器の書き手で、この日の合成データの確かめで器の食い違いを見つけて直した直後にいる。「もう大きな誤りは残っていない」と読む側に引かれる。逆に、指摘を理由を詰めずに採って器を重くする側（過剰譲歩）にも引かれる。',
        '- 置いた印: 予想を票の前に記す・和集合と採否の表・「重い」の追い問い・前提の一次の資料での確かめ・是認も記録。', '',
        '## 費用', '',
        '- claude.ai の新しいチャット二つ（登録者のプランの内・API の費用は無い）。束を上げる前に、claude.ai が束の zip を受け付けるかを確かめる。', '',
        '## この枠が確認していないこと', '',
        '- 検分者が束の全部を読むか（申告は検査ではない）。',
        '- claude.ai の新しいチャットが、この研究の過去の会話の記憶を持つか（アカウントの設定は登録者のもので、確かめていない）。',
        '- claude.ai の実行の場の走る時間の上限（長い自己検査が途中で切れるか）。',
        '- 系統外の目（この巡には無い）。', '', CLAUSE, '']
    out = os.path.join(HERE, '00-frame-impl-Bprime.md')
    if os.path.exists(out):
        raise SystemExit('既にある: %s' % out)
    with open(out, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(NL.join(L))
    print('書いた %s（SHA16 %s・%d 行）' % (os.path.basename(out), s16(out), len(L)))


if __name__ == '__main__':
    main()
