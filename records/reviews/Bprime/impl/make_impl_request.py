# -*- coding: utf-8 -*-
"""make_impl_request.py —— B′ の器の実装の検分の依頼文（二つのチャットに同じ本文・役割の節だけ違える）を書く（2026-09-30・コーディネータ南無弥勒如来・非公開）。
書く物: `request-impl-Bprime-R1.md`・`request-impl-Bprime-R2.md`（一度だけ書く）。所見の番号の幅と正本の版は実物から写す。送るのは登録者の確認の後。
用法: python reviews/impl/make_impl_request.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE))
NL = chr(10)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
s16 = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]

ROLES = {
    'R1': ('計算', [
        '読み取りの器 `tools/bprime_run.py`・方向の器 `tools/bprime_directions.py`・相の計算 `tools/bprime_phases.py`・芯 `tools/bprime_core.py`・集計 `tools/analyze_Bprime.py`・行動の下見の器 `tools/bprime_behavior.py`・'
        '独立の再計算の二つの道 `tools/bprime_recompute_rewrite.py`・`tools/bprime_reextract.py`（書き手と別の個体が書いた）。',
        '見てほしい所: 出口の値の自己検査（softcap の見分ける力と許容の式）・最後の層の自己検査の方向・両方の向きの組み方・床の余白の印・生成の設定と止める印・フックの順・採点の器の呼び出し・率の定義と区間・道の違いの札・書き出しの根の件数・'
        '三つの道（フック・書き換え・再抽出）が同じものを違う作りで計算しているか（同じ読み違いを共有していないか）。']),
    'R2': ('流れと記録', [
        '起動器 `tools/colab/boot_bprime.py`（相と段・起動の記録・出力の SHA・錠・DRY の写し）・閉じる器 `tools/close_behavior_Bprime.py`・系統外の模型による採点の束と依頼の文 `tools/bprime_external.py`・`tools/send_external_Bprime.py`・'
        '凍結の器 `tools/freeze_Bprime.py`・封印 `tools/seal_Bprime.py`・予想の書式 `tools/make_predictions_form_Bprime.py`・凍結の本文 `tools/make_frozen_Bprime.py`・移す器 `tools/publish_Bprime.py`・`tools/bprime_publish_map.py`・'
        '掃き出し `tools/sweep_Bprime.py`・報告の組み立て `tools/build_report_Bprime.py`・合成データの確かめ `tools/dry_run_Bprime.py`。',
        '見てほしい所: 本の凍結の錠（足してよい鍵の外・SHA の違い・決定の出し直し）・起動の記録と出力の SHA の記録のつながり（起動 → 走り → 閉じる → 凍結）・読みの規則の走査（二つの層）・報告の要約の型・三巡目の直し（採否の表 T01〜T33）・'
        '器の段の所見（器の段の記録の K）と系統外の模型による採点の依頼の文・器どうしの口（ある器が書く物の名と形を、別の器が同じ名と形で読むか）。']),
}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    log = open(os.path.join(BP, 'tools', 'tools-log-Bprime.md'), encoding='utf-8').read()
    ks = sorted({int(k) for k in re.findall(r'^- \*\*K(\d+)（', log, flags=re.M)})
    for role, (name, lines) in ROLES.items():
        other = [r for r in ROLES if r != role][0]
        L = [
            '# 検分の依頼（B′ の器の実装の検分・%s〔%s〕・2026-09-30）' % (role, name), '',
            '時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。', '',
            'あなたには、研究の器（Python のコード）の実装を検分していただきます。あなたは、この器の書き手（Anthropic の Claude 系の模型・コーディネータ）とは別の個体で、前の設計の巡の検分者とも別の個体です。'
            '書き手に同調する必要はありません。書き手の見落とし・読み違い・器どうしの食い違い・通っていない枝を見つけることが、あなたの役目です。', '',
            '## まず書いてほしいこと（系統の申告）', '',
            '返答の一行目に、あなた自身の模型の名と作り手を書いてください（例:「模型: ○○・作り手: ○○」）。', '',
            '## この検分の位置', '',
            '- 研究は ontology-preamble-4b の段階 B′（Gemma 4 31B で、層三の読み取りの型を日本語で追試する登録）です。設計の巡は三巡で終わり、いまは器の段の終わりです。この検分の後に、凍結の前の確かめ（Colab の GPU）と凍結があります。',
            '- 正本は `design/contrasts-Bprime.json`（版 %s）、設計の本文は `design/design-Bprime-draft10.md` です。器の段の記録 `records/Bprime/tools/tools-log-Bprime.md` に、書き手が器の段で見つけて直したこと（K%d〜K%d）があります。'
            % (C['version'], ks[0], ks[-1]),
            '- 合成データの確かめの正式の記録（小さな乱数の Gemma 4 で起動器の全ての相を通した走り・Colab の CPU）が `records/Bprime/` の `dry-run-Bprime-*.md` にあります。',
            '- 検分者は二人で、役割を分けています。あなたは **%s（%s）** です。もう一人は %s（%s）です。役割の外の所見も書いてください。' % (role, name, other, ROLES[other][0]), '',
            '## あなたの役割（%s・%s）' % (role, name), ''] + ['- ' + x for x in lines] + [
            '',
            '## 走らせてほしいこと', '',
            '- 添えた zip を展開し、`README-impl-bundle-Bprime.md` を読んでから、書いてあるとおりに版を固定して numpy と transformers を入れ（numpy 2.4.6・transformers 5.16.1）、torch の要らない器と、transformers と tokenizers が要る器の自己検査（`--selftest`）を走らせてください。',
            '- torch の要る器は、実行の場に torch が無ければ走らせず、器の中と正式の記録を読んで照らしてください。',
            '- 束の目録 `MANIFEST-impl-bundle-Bprime.json` の SHA-256 と、あなたが計算した SHA-256 が合うかを、少なくとも器のファイルについて確かめてください。',
            '- 走らせたコマンドと、出力の末尾（最後の数行）と、走らなかったときの誤りの文を、返事にそのまま貼ってください。書き手が手元で同じ出力になるかを照らします。', '',
            '## しないでほしいこと', '',
            '- 実の重みを読み込まない・実の重みで順伝播を走らせない（封印の前の決まり）。外への呼び出しをしない（`tools/send_external_Bprime.py` は `--selftest` だけ）。',
            '- ウェブ検索などの道具を使ったときは、その出所を所見と分けて書いてください。', '',
            '## 返事の形', '',
            '1. 一行目: 模型の名と作り手。',
            '2. 所見の一覧。所見ごとに: 番号（%s-01 から）・重さ（**重い**＝凍結の前に直す／**中**＝直す方がよい／**軽い**）・器とファイルと行・何が起きるか（どんな入力で、どんな誤った出力か止まり方になるか）・直し方の案・確信度（高・中・低）・'
            '走らせて確かめたか、読んで推したか。' % role,
            '3. 是認: 見て問題が無かった所を、項目ごとに短く（是認も記録に残します）。',
            '4. 走らせた記録: コマンド・出力の末尾・SHA の照らし。',
            '5. 読んでいない所・走らせていない所の申告。', '',
            '## 添えるもの', '',
            '- 器の実装の検分の束（zip・公開の置き場の形の一つの置き場）。中身は束の目録にあります。', '',
            CLAUSE, '']
        out = os.path.join(HERE, 'request-impl-Bprime-%s.md' % role)
        if os.path.exists(out):
            raise SystemExit('既にある: %s' % out)
        with open(out, 'w', encoding='utf-8', newline=NL) as fh:
            fh.write(NL.join(L))
        print('書いた %s（SHA16 %s・%d 行）' % (os.path.basename(out), s16(out), len(L)))


if __name__ == '__main__':
    main()
