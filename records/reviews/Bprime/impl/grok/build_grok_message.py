# -*- coding: utf-8 -*-
"""build_grok_message.py v0 —— B′ の器の実装の検分・系統外の一巡（独立の再計算の三つの道・grok-4.7・裁定 D272）に送る発話を組む（2026-09-30・コーディネータ南無弥勒如来・非公開）。
発話 = 依頼文 ＋ 材料の全文（grok は実行の場を持たないので、器と正本の関わる節と Gemma 4 の層の実装の抜き書きを文字で渡す）。
材料: 別の個体への指示・三つの道の器（フック `bprime_run.py`・書き換え `bprime_recompute_rewrite.py`・再抽出 `bprime_reextract.py`）・本の抽出 `bprime_directions.py`・
模型の助け `bprime_gemma.py`・相の計算 `bprime_phases.py`・起動器 `colab/boot_bprime.py`・集計 `analyze_Bprime.py`・凍結の芯 `bl3_core.py` の関わる関数（公開の置き場の決めた版から）・
正本の関わる節・transformers 5.16.1 の Gemma 4 の層の実装の抜き書き（Apache-2.0）。別の個体の開発の記録は入れない（本人の読みの申告に引かれないように・器の本文と指示から独立に読んでもらう）。
書く物: `grok-message.md`（発話）・`grok-materials.json`（材料の出所と SHA16）。一度だけ書く。
用法: python reviews/impl/grok/build_grok_message.py
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, ast, json, hashlib, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PUB = 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
NL = chr(10)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
CONTRACT_KEYS = ['independent_recompute', 'layers', 'readout', 'directions', 'coefficient', 'nulls', 'computation', 'main_rows', 'cells_main', 'cell_signs_main', 'labels', 'pilot']
BL3_FUNCS = ['p_and_tail', 'holm', 'comparators_for', 'cache_tol', 'agreement', 'recompute_set']
GEMMA_CLASSES = ['Gemma4RMSNorm', 'Gemma4TextDecoderLayer', 'Gemma4TextScaledWordEmbedding', 'Gemma4TextModel']
GEMMA_METHODS = [('Gemma4ForConditionalGeneration', 'forward')]

REQUEST = '''# 検分の依頼（B′ の器の実装の検分・系統外の一巡〔独立の再計算の三つの道〕・2026-09-30）

時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に検分をしてください。

あなたには、研究の器（Python のコード）のうち、同じ量を違う作りで計算し直す「三つの道」の実装を検分していただきます。器の書き手は Anthropic の Claude 系の模型です（本の器はコーディネータ、書き換えの道と再抽出の道はコーディネータと別の新しい個体）。三つの道はどれも Claude 系が同じ指示と同じ資料から書いたので、指示の読み違いを共有していれば、道どうしの突き合わせでは捕まりません。あなたには、別の系統の目として、その共有された読み違いと、どの道にもある誤りを探していただきたいのです。書き手に同調する必要はありません。

## まず書いてほしいこと（系統の申告）

返答の一行目に、あなた自身の模型の名と作り手を書いてください（例:「模型: ○○・作り手: ○○」）。

## 研究と三つの道（正本の定め・材料の「正本の関わる節」の `independent_recompute`）

- 研究は ontology-preamble-4b の段階 B′ です。Gemma 4 31B（`google/gemma-4-31B-it`・transformers 5.16.1・bf16）の選んだ層の出力に、抽出した方向（v̂ など）を足したときの、読み取りの集合の選択肢 a の対数オッズの変わり方（効き目）を、等方の帰無と比べます。
- **本の器のフックの道**（コーディネータ・`bprime_run.py`）: 選んだ層の出力に forward hook で方向を足し、最終の正規化の入力を前のフックで取って、float32 で最終の正規化・語彙の行列・softcap を当てて対数オッズを出す。
- **書き換えの道**（別の個体・`bprime_recompute_rewrite.py`）: 加減をフックでなく、選んだ層の出力を書き換えて後の層を流す（近道なし・バッチ一）。一段目の突き合わせで、フックの道と厳しい許容（`independent_recompute.tol_stage1`）で比べる。
- **再抽出の道**（別の個体・`bprime_reextract.py`）: 本の抽出（`bprime_directions.py`）と同じ設定で、活性を取り出す書き方だけを変えて抽出の文脈を流し、‖h‖・‖v̂‖ の相対の差と名前のある方向の余弦で突き合わせる。
- 一致の判定は集計の器（`analyze_Bprime.py` の `recompute_agreement`・`reextract_agreement`）と凍結の芯（`bl3_core.py` の `agreement`・`recompute_set`）です。

## 見てほしいこと

1. 三つの道が、正本の定めと Gemma 4 の実装（材料の抜き書き）に照らして、本当に同じ量を計算しているか。とくに: 足す層と位置（層の出力のどの時点か・`layer_scalar` の掛け算の前か後か・層ごとの入力〔per-layer input〕の足し込みの前か後か）・足すトークンの位置・符号と倍率（係数）・最終の正規化の入力の取り方・softcap・float32 に上げる時点・注意の実装とキャッシュの設定。
2. 三つの道が同じ読み違いを共有していないか。別の個体への指示（材料の最初）の書き方が、読み違いを誘っていないか。正本の定めと違うのに、三つの道がそろって同じように違う所。
3. 一致の判定が、違いを見逃す形になっていないか（許容・札の比べ方・比べる行の選び方・外した升目の扱い・値が有限でないときの扱い）。
4. 合成データの確かめ（小さな乱数の Gemma 4・`layer_scalar` を 1 から離した変種・わざと誤らせた変種）が、三つの道の違いを見分けられる形になっているか。見分けられない誤りの種類があれば挙げてください。
5. ほかに、三つの道の実装の誤り・止まるべき所で止まらない所・止まるべきでない所で止まる所。

## 前提と、しないでほしいこと

- あなたは実行の場を持たない前提です。読んで推したことは「読んで推した」と書き、器の行（関数の名と、分かれば行の中身）を示してください。
- 材料に無いもの（transformers の他の部分・凍結の器の他の関数など）について推すときは、推しであることを書いてください。
- ウェブ検索などの道具を使ったときは、その出所を所見と分けて書いてください。

## 返事の形

1. 一行目: 模型の名と作り手。
2. 所見の一覧。所見ごとに: 番号（G-01 から）・重さ（**重い**＝凍結の前に直す／**中**＝直す方がよい／**軽い**）・器と関数（と行の中身）・何が起きるか（どんな入力で、どんな誤った値か止まり方になるか）・直し方の案・確信度（高・中・低）・読んで推したか、正本や Gemma 4 の抜き書きの字で確かめたか。
3. 是認: 見て問題が無かった所を、項目ごとに短く（是認も記録に残します）。
4. 読んでいない所の申告。

## 材料（この後に全文・各ファイルの SHA16 は改行を LF にそろえた SHA-256 の先頭 16 字）
'''


def git_show(rel, commit):
    r = subprocess.run(['git', '-C', PUB, 'show', '%s:%s' % (commit, rel)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit('公開の置き場の決めた版に無い: %s' % rel)
    return r.stdout


def ast_extract(src, names=(), methods=()):
    """ソースから、名の関数か組（class）と、組の中の関数を、行のまま抜く（並びはソースの順）。"""
    lines = src.split(NL)
    tree = ast.parse(src)
    spans = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names:
            start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])])
            spans.append((start, node.end_lineno, node.name))
        if isinstance(node, ast.ClassDef):
            for cls, meth in methods:
                if node.name == cls:
                    for sub in node.body:
                        if isinstance(sub, ast.FunctionDef) and sub.name == meth:
                            start = min([sub.lineno] + [d.lineno for d in sub.decorator_list])
                            spans.append((start, sub.end_lineno, '%s.%s' % (cls, meth)))
    got = {s[2] for s in spans}
    want = set(names) | {'%s.%s' % m for m in methods}
    if got != want:
        raise SystemExit('抜き書きの名がそろわない: 無い %s' % sorted(want - got))
    out = []
    for a, b, name in sorted(spans):
        out.append('# ---- %s（元の行 %d〜%d） ----' % (name, a, b))
        out.extend(lines[a - 1:b])
    return NL.join(out)


def block(title, origin, text, lang):
    b = text.encode('utf-8')
    fence = '````' if '```' in text else '```'
    return ['', '### %s' % title, '', '- 出所: %s・SHA16 %s・%d 字' % (origin, s16b(b), len(text)), '', fence + lang, text.rstrip(NL), fence], {'title': title, 'origin': origin, 'sha16': s16b(b), 'chars': len(text)}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    out_md = os.path.join(HERE, 'grok-message.md')
    out_js = os.path.join(HERE, 'grok-materials.json')
    for p in (out_md, out_js):
        if os.path.exists(p):
            raise SystemExit('既にある（一度だけ）: %s' % p)
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    commit = C['inputs']['public_version']
    rd = lambda rel: open(os.path.join(BP, *rel.split('/')), encoding='utf-8').read().replace('\r\n', NL)
    parts, mats = [REQUEST.rstrip(NL)], []

    def add(title, origin, text, lang):
        L, m = block(title, origin, text, lang)
        parts.extend(L)
        mats.append(m)
    add('1. 別の個体への指示（書き換えの道と再抽出の道の書き手が受けた指示の全文）', '作業の置き場 `tools/independent/instructions-rewrite-reextract-Bprime.txt`',
        rd('tools/independent/instructions-rewrite-reextract-Bprime.txt'), 'text')
    sub = collections.OrderedDict((k, C[k]) for k in CONTRACT_KEYS)
    sub['inputs.model_facts'] = C['inputs']['model_facts']
    sub['inputs.versions'] = C['inputs']['versions']
    add('2. 正本の関わる節（`design/contrasts-Bprime.json`・版 %s の中の鍵 %s と inputs.model_facts・inputs.versions）' % (C['version'], '・'.join(CONTRACT_KEYS)),
        '作業の置き場 `design/contrasts-Bprime.json`（全体の SHA16 %s）' % s16b(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), 'rb').read()),
        json.dumps(sub, ensure_ascii=False, indent=1), 'json')
    for i, (rel, what) in enumerate([
            ('tools/bprime_run.py', 'フックの道・読み取り・本の計算の行'),
            ('tools/independent/bprime_recompute_rewrite.py', '書き換えの道（別の個体）'),
            ('tools/independent/bprime_reextract.py', '再抽出の道（別の個体）'),
            ('tools/bprime_directions.py', '本の抽出'),
            ('tools/bprime_gemma.py', '模型の助け（層の添字・設定の読み）'),
            ('tools/bprime_phases.py', '相の計算（本の計算の組・抽出）'),
            ('tools/colab/boot_bprime.py', '起動器（相 recompute の三つの組の呼び方）'),
            ('tools/analyze_Bprime.py', '集計（一致の判定）')], start=3):
        add('%d. `%s`（%s）' % (i, rel, what), '作業の置き場 `%s`' % rel, rd(rel), 'python')
    bl3 = git_show('tools/bl3_core.py', commit).decode('utf-8').replace('\r\n', NL)
    add('11. 凍結の芯 `bl3_core.py` の関わる関数（%s）' % '・'.join(BL3_FUNCS), '公開の置き場の決めた版 `%s` の `tools/bl3_core.py`（全体の SHA16 %s）' % (commit, s16b(bl3.encode('utf-8'))),
        ast_extract(bl3, BL3_FUNCS), 'python')
    gm = rd('pylib/transformers/models/gemma4/modeling_gemma4.py')
    add('12. transformers 5.16.1 の Gemma 4 の実装の抜き書き（%s・Apache-2.0）' % '・'.join(GEMMA_CLASSES + ['%s.%s' % m for m in GEMMA_METHODS]),
        '手元の固定の版の transformers `transformers/models/gemma4/modeling_gemma4.py`（全体の SHA16 %s）' % s16b(gm.encode('utf-8')),
        ast_extract(gm, GEMMA_CLASSES, GEMMA_METHODS), 'python')
    parts += ['', '---', '', '材料はここまでです。' + CLAUSE, '']
    msg = NL.join(parts)
    with open(out_md, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(msg)
    meta = {'kind': 'bprime_impl_grok_message', 'builder': 'build_grok_message.py v0', 'contract_version': C['version'], 'public_version': commit,
            'message_sha16': s16b(msg.encode('utf-8')), 'message_chars': len(msg), 'materials': mats, 'excluded': ['別の個体の開発の記録（本人の読みの申告に引かれないように）'], 'clause': CLAUSE}
    with open(out_js, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('書いた grok-message.md（SHA16 %s・%d 字）・材料 %d' % (meta['message_sha16'], len(msg), len(mats)))
    for m in mats:
        print('  %s | %s | %d' % (m['sha16'], m['title'][:60], m['chars']))


if __name__ == '__main__':
    main()
