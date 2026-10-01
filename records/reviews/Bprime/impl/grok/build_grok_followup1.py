# -*- coding: utf-8 -*-
"""build_grok_followup1.py v0 —— B′ の器の実装の検分・grok-4.7 への追い問い（一度目・G-01・裁定 D276）の発話を組む（2026-09-30・コーディネータ南無弥勒如来・非公開）。
前の巡の型（新しい呼び出しに前の返事を添える）。材料はすべて実物から機械で写す: 前の返事の全文・移し方の表の規則（`bprime_publish_map.RULES` の源の字）・
合成データの確かめの正式の記録の三と四の部の独立の再計算の行・起動器の読み込みと相 check の行・凍結の器の Colab の確かめの評価（`colab_check_eval`）の源の字。
書く物: `grok-followup1-message.md`・`grok-followup1-materials.json`（一度だけ）。
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, ast, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
NL = chr(10)
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'
s16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]

REQUEST = '''# 追い問い（B′ の器の実装の検分・系統外の一巡・一度目・G-01・2026-09-30）

時間はたっぷりありますので、落ち着いて、じっくりと、丁寧に確かめてください。

前の呼び出しで、独立の再計算の三つの道の検分をありがとうございました。前の返事の全文を下に添えます（材料 1）。この追い問いは、あなたが「重い」とした **G-01** についてです。

書き手（コーディネータ）は G-01 の前提を次のように確かめました。前の材料に入れていなかった物を添えます。

- 作業の置き場では、別の個体の二つの器は `tools/independent/` にあります。公開の置き場へは、移す器が「移し方の表」（材料 2）の規則で写し、二つの器は公開の置き場の `tools/` に置かれます。起動器は公開の置き場の `tools/` を `sys.path` に入れて、二つを裸の名で読み込みます（材料 4）。
- 合成データの確かめの正式の記録（小さな乱数の Gemma 4・公開の置き場の形の一時の置き場）では、起動器から二つの組（書き換えと再抽出）を三つの枝で通し、期待どおりでした（材料 3）。
- 相 check は `all_pass` が偽でも止まらずに記録を書いて終わりますが、下見の前の凍結の器が相 check の出力を評価し、外れがあれば止めます（材料 5）。

## 答えてほしいこと

1. 添えた物で、G-01 の懸念は閉じるか（閉じないなら、どの道筋で起動器が二つの器を読めなくなるか）。
2. 相 check が止まらずに終わり、下見の前の凍結の器が止める、という分け方に、残る穴があるか。
3. 移し方の表を見たことで、前の返事のほかの所見（G-02〜G-10）の読みや重さが変わるものがあるか。

## 返事の形

一行目に模型の名と作り手。項目 1〜3 に順に答え、所見ごとに「閉じる／閉じない（理由）」を書いてください。読んで推したことは「読んで推した」と書いてください。

## 材料（この後に全文・各ファイルの SHA16 は改行を LF にそろえた SHA-256 の先頭 16 字）
'''


def src_of(path, names):
    src = open(path, encoding='utf-8').read().replace('\r\n', NL)
    lines = src.split(NL)
    out = []
    for node in ast.parse(src).body:
        nm = getattr(node, 'name', None) or (node.targets[0].id if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) else None)
        if nm in names:
            out.append('# ---- %s（元の行 %d〜%d） ----' % (nm, node.lineno, node.end_lineno))
            out.extend(lines[node.lineno - 1:node.end_lineno])
    return NL.join(out)


def lines_with(path, needles, ctx=2):
    lines = open(path, encoding='utf-8').read().replace('\r\n', NL).split(NL)
    keep = set()
    for i, l in enumerate(lines):
        if any(n in l for n in needles):
            keep |= set(range(max(0, i - ctx), min(len(lines), i + ctx + 1)))
    out, prev = [], None
    for i in sorted(keep):
        if prev is not None and i != prev + 1:
            out.append('# ……')
        out.append('%4d| %s' % (i + 1, lines[i]))
        prev = i
    return NL.join(out)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    out_md = os.path.join(HERE, 'grok-followup1-message.md')
    out_js = os.path.join(HERE, 'grok-followup1-materials.json')
    for p in (out_md, out_js):
        if os.path.exists(p):
            raise SystemExit('既にある（一度だけ）: %s' % p)
    rel = lambda *a: os.path.join(BP, *a)
    mats = []
    parts = [REQUEST.rstrip(NL)]

    def add(title, origin, text, lang):
        fence = '````' if '```' in text else '```'
        parts.extend(['', '### %s' % title, '', '- 出所: %s・SHA16 %s・%d 字' % (origin, s16b(text.encode('utf-8')), len(text)), '', fence + lang, text.rstrip(NL), fence])
        mats.append({'title': title, 'origin': origin, 'sha16': s16b(text.encode('utf-8')), 'chars': len(text)})
    prev = open(os.path.join(os.path.dirname(HERE), 'votes', 'grok-4.7', 'response.md'), encoding='utf-8').read()
    add('1. 前の呼び出しの返事の全文', '`votes/grok-4.7/response.md`（前の呼び出しの返事）', prev, 'markdown')
    add('2. 移し方の表の規則（`tools/bprime_publish_map.py` の RULES）', '作業の置き場 `tools/bprime_publish_map.py`（全体の SHA16 %s）' % s16b(open(rel('tools', 'bprime_publish_map.py'), 'rb').read()),
        src_of(rel('tools', 'bprime_publish_map.py'), {'RULES'}), 'python')
    rec = rel('records', 'Bprime', 'dry-run-Bprime-2026-09-30.md')
    rows = [l for l in open(rec, encoding='utf-8').read().split(NL) if l.startswith('| ') and ('recompute' in l or 'reextract' in l or 'rewrite' in l or '部 | 確かめ' in l or l.startswith('|---'))]
    add('3. 合成データの確かめの正式の記録の独立の再計算の行（`records/Bprime/dry-run-Bprime-2026-09-30.md` の表から、書き換え・再抽出・recompute を含む行を機械で抜いた）',
        '作業の置き場 `records/Bprime/dry-run-Bprime-2026-09-30.md`（全体の SHA16 %s）' % s16b(open(rec, 'rb').read()), NL.join(rows), 'markdown')
    boot = rel('tools', 'colab', 'boot_bprime.py')
    add('4. 起動器の読み込みの行（`tools/colab/boot_bprime.py` の sys.path と二つの器の読み込みの前後・行番号つき）', '作業の置き場 `tools/colab/boot_bprime.py`（全体の SHA16 %s）' % s16b(open(boot, 'rb').read()),
        lines_with(boot, ['sys.path', 'import bprime_recompute_rewrite', 'import bprime_reextract', "if PHASE == 'check'"], ctx=3), 'python')
    fz = rel('tools', 'freeze_Bprime.py')
    add('5. 凍結の器の相 check の出力の評価（`tools/freeze_Bprime.py` の colab_check_eval）', '作業の置き場 `tools/freeze_Bprime.py`（全体の SHA16 %s）' % s16b(open(fz, 'rb').read()),
        src_of(fz, {'colab_check_eval'}), 'python')
    parts += ['', '---', '', '材料はここまでです。' + CLAUSE, '']
    msg = NL.join(parts)
    with open(out_md, 'w', encoding='utf-8', newline=NL) as fh:
        fh.write(msg)
    meta = {'kind': 'bprime_impl_grok_followup1', 'builder': 'build_grok_followup1.py v0', 'message_sha16': s16b(msg.encode('utf-8')), 'message_chars': len(msg), 'materials': mats, 'registrant_permission': 'D276', 'clause': CLAUSE}
    with open(out_js, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print('書いた grok-followup1-message.md（SHA16 %s・%d 字）・材料 %d' % (meta['message_sha16'], len(msg), len(mats)))
    for m in mats:
        print('  %s | %s | %d' % (m['sha16'], m['title'][:50], m['chars']))


if __name__ == '__main__':
    main()
