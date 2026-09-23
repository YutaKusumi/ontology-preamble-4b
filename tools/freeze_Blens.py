# -*- coding: utf-8 -*-
"""freeze_Blens.py v1 —— B-lens の凍結の記帳（2026-09-23・正本 §9「確かめと凍結」・裁定 D175・D186）。

確かめてから記帳する（外れたら止める・登録者に相談）:
  - 凍結版の本文（`design/design-Blens-FROZEN.md`）と草案3 の本文の差が、題名・凍結の行・組み立ての記録だけ（`make_frozen_B.other_diffs`）。数の検査の違反が零。
  - 凍結の語の集合（`records/Blens/sets-Blens.json`）: 単独で割った集合が下書きの器とバイトで一致し、正本の SHA16 がいまの正本と同じ。
  - 合成データの記録（`records/Blens/dry-run-Blens-*.md`）の外れが零。予想の書式が組めて、欄の確かめを通る。
  - Colab の起動器の相 check の出力（実重み・DRY でない）: 版が B の版・重みの SHA-256 が転記行 F と同じ・B のランダム方向を B の版の NumPy で再生した SHA-256 が
    手元の再生と同じ・logits の突き合わせが許容の内・較正の検査が区間の内・選んだ試行の SHA16 が設計の事実と同じ。
  - 予想の封印はまだ無い（正本の順: 凍結と記録先行の公開の後に封印）。
記帳するもの: 凍結物の SHA16（本文・原稿・正本・設計の事実・語の集合・予想の書式・合成データの記録・Colab の確かめの記録・器と、器が import する器の閉包・読む記録）、
  八腕の主位置の活性の公開（裁定 D175・公開の置き場に写し、SHA-256 を凍結の記録の値と照らす）、全体の台帳（records/FREEZE-RECORD.md）の一行。
出力: records/Blens/FREEZE-RECORD-Blens.json・.md・records/Blens/colab-check-Blens.json（--force が無ければ上書きしない）。
用法: python tools/freeze_Blens.py --words "<登録者の逐語>" --when "<日時（日本時間）>" --colab-check <相 check の check.json> ／ --check-only（Colab の確かめを除いた確かめだけ）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, glob, json, shutil, hashlib, argparse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)

VERSION = 'v1'
NL = chr(10)
FR_JSON = os.path.join(REPO, 'records', 'Blens', 'FREEZE-RECORD-Blens.json')
FR_MD = os.path.join(REPO, 'records', 'Blens', 'FREEZE-RECORD-Blens.md')
CC_COPY = os.path.join(REPO, 'records', 'Blens', 'colab-check-Blens.json')
LEDGER = os.path.join(REPO, 'records', 'FREEZE-RECORD.md')
ACT_SRC = os.path.expanduser('~/.cache/op4b-dir/dirB__s1/main_position_activations.npz')
ACT_PUB = os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'main_position_activations.npz')
TOOLS = ['tools/blens_core.py', 'tools/blens_sets.py', 'tools/blens_lens.py', 'tools/blens_calib.py', 'tools/colab/boot_Blens.py', 'tools/build_report_Blens.py',
         'tools/dry_run_Blens.py', 'tools/make_predictions_form_Blens.py', 'tools/seal_Blens.py', 'tools/make_frozen_Blens.py', 'tools/freeze_Blens.py',
         'tools/blens_facts.py', 'tools/make_contrasts_Blens.py', 'tools/build_draft_Blens.py']
FILES = ['design/design-Blens-FROZEN.md', 'design/design-Blens-FROZEN.src.md', 'design/contrasts-Blens.json', 'records/Blens/design-facts-Blens.json',
         'records/Blens/design-facts-Blens.md', 'records/Blens/sets-Blens.json', 'records/Blens/sets-Blens.md', 'records/predictions/predictions-form-Blens-v1.html',
         'records/Blens/numbers-lint-FROZEN-Blens.md', 'records/Blens/rulings-D186.md']
READS = ['design/contrasts-B.json', 'records/B/analysis-B-2026-09-22.json', 'records/B/posthoc-by-direction-B-2026-09-22.json', 'results/dirB/dirB__s1/directions.npz',
         'results/dirB/dirB__s1/directions.json', 'arms/frozen-from-ryokai-os/app-scenarios.json', 'records/predictions/predictions-form-Vprime-v0.5.html']
rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
P = lambda r: os.path.join(REPO, *r.split('/'))
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
sha256f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


def import_closure(tools):
    """器が import する（関数の中の import も含む）手元の器の閉包。"""
    out, todo = set(), list(tools)
    while todo:
        t = todo.pop()
        if t in out:
            continue
        out.add(t)
        tree = ast.parse(open(P(t), encoding='utf-8').read())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split('.')[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = [node.module.split('.')[0]]
            for n in names:
                for cand in ('tools/%s.py' % n, 'tools/colab/%s.py' % n):
                    if os.path.exists(P(cand)) and cand not in out:
                        todo.append(cand)
    return sorted(out)


def checks(colab_check=None):
    import make_frozen_B as MF
    import make_frozen_Blens as MFL
    import make_predictions_form_Blens as FORM
    import blens_lens as BL
    TL = json.load(open(P('design/contrasts-Blens.json'), encoding='utf-8'))
    res, bad = {}, []
    # 本文
    if not os.path.exists(MFL.FOUT):
        bad.append('凍結版の本文が無い（make_frozen_Blens を先に走らせる）')
    else:
        od = MF.other_diffs(MFL.diffs(MFL.DRAFT, MFL.FOUT))
        res['frozen_text_other_diffs'] = len(od)
        if od:
            bad.append('凍結版の本文に許す差でない差がある')
        lint = open(MFL.LINT, encoding='utf-8').read()
        if '違反の合計: 0' not in lint:
            bad.append('凍結版の数の検査に違反がある')
    # 語の集合
    SJ = json.load(open(P('records/Blens/sets-Blens.json'), encoding='utf-8'))
    res['sets'] = {'facts_equal': SJ['checks']['facts_equal'], 'contrasts_sha16': SJ['contrasts_sha16'], 'in_prompt_differences': SJ['checks']['in_prompt_differences']}
    if not SJ['checks']['facts_equal'] or SJ['contrasts_sha16'] != sha16f(P('design/contrasts-Blens.json')):
        bad.append('凍結の語の集合が下書きの器と一致しないか、正本が変わっている')
    # 合成データ
    dr = sorted(glob.glob(P('records/Blens/dry-run-Blens-*.md')))
    if not dr:
        bad.append('合成データの記録が無い')
    else:
        txt = open(dr[-1], encoding='utf-8').read()
        m = re.search(r'結果: (\d+) 経路・外れ (\d+)', txt)
        res['dry_run'] = {'path': rel(dr[-1]), 'paths': int(m.group(1)) if m else None, 'off': int(m.group(2)) if m else None}
        if not m or m.group(2) != '0':
            bad.append('合成データの記録に外れがある')
    # 予想の書式
    h = open(FORM.OUT, encoding='utf-8').read()
    res['form'] = FORM.check(TL, h)
    # 封印はまだ無い
    for p in ('records/predictions/predictions-Blens-coordinator.json', 'records/predictions/predictions-Blens-registrant.json', 'records/Blens/sealing-record-Blens.json'):
        if os.path.exists(P(p)):
            bad.append('封印が凍結より先にある（正本の順と違う）: %s' % p)
    # 活性（裁定 D175）
    DJ = json.load(open(P('results/dirB/dirB__s1/directions.json'), encoding='utf-8'))
    if sha256f(ACT_SRC) != DJ['activations_npz_sha256'].upper() or os.path.getsize(ACT_SRC) != TL['publication']['bytes']:
        bad.append('手元の八腕の活性が凍結の記録と違う')
    res['activations_sha256'] = sha256f(ACT_SRC)
    # Colab の確かめ
    if colab_check is not None:
        import numpy as np
        import steer_B
        CK = json.load(open(colab_check, encoding='utf-8'))
        FJ = json.load(open(P('records/Blens/design-facts-Blens.json'), encoding='utf-8'))
        pins = TL['inputs']['versions_B']
        D = np.load(P('results/dirB/dirB__s1/directions.npz'))
        sel = BL.rkey(TL['primary']['ratio'])
        local = {'main@%s' % sel: BL.dirs_sha256(steer_B.random_directions(D['static__%s' % sel], 'main', float(sel)))}
        for r in [BL.rkey(x) for x in TL['layers']['ratios']]:
            local['tune@%s' % r] = BL.dirs_sha256(steer_B.random_directions(D['static__%s' % r], 'tune', float(r)))
        c = {'kind_check': CK.get('kind') == 'blens_colab_check', 'not_dry': CK.get('dry') is False,
             'versions': all((CK['versions'].get(k) or '').startswith(v.split('+')[0]) for k, v in (('numpy', pins['numpy']), ('torch', pins['torch']), ('transformers', pins['transformers']))),
             'weights': CK.get('weights_sha256') == FJ['facts']['F']['sha256'], 'random_dirs': CK.get('random_dirs_sha256') == local,
             'logit_check': CK['logit_check'].get('main_max_abs', 9) <= TL['magnitude']['logit_check']['atol'] and CK['logit_check'].get('letter_max_abs', 9) <= TL['magnitude']['logit_check']['atol']
                            and CK['logit_check'].get('main_argmax_equal') and CK['logit_check'].get('letter_argmax_equal'),
             'calibration': all(v['main']['inside'] and all(x['inside'] for x in (v.get('letter') or {}).values()) for v in CK['calibration'].values()),
             'selected': CK.get('selected_sha16') == FJ['facts']['E']['selected_sha16']}
        res['colab_check'] = dict(c, commit=CK.get('commit'), gpu=CK.get('gpu'), versions_seen=CK.get('versions'), random_dirs_local=local)
        bad += ['Colab の確かめ: %s' % k for k, v in c.items() if not v]
    return res, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--words')
    ap.add_argument('--when')
    ap.add_argument('--colab-check')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    res, bad = checks(None if a.check_only else a.colab_check)
    print(json.dumps({k: v for k, v in res.items() if k != 'sets'}, ensure_ascii=False, indent=1)[:3000])
    if bad:
        raise SystemExit('凍結の前の確かめが外れた（止める・登録者に相談）: %s' % bad)
    if a.check_only:
        print('[freeze_Blens] 確かめだけ（Colab の確かめを除く）: 外れ無し')
        return
    if not (a.words and a.when and a.colab_check):
        raise SystemExit('--words・--when・--colab-check が要る')
    if os.path.exists(FR_JSON) and not a.force:
        raise SystemExit('既にある: %s' % rel(FR_JSON))
    # Colab の確かめの記録を写し、活性を公開の置き場に写す（裁定 D175）
    shutil.copyfile(a.colab_check, CC_COPY)
    if not os.path.exists(ACT_PUB):
        shutil.copyfile(ACT_SRC, ACT_PUB)
    if sha256f(ACT_PUB) != res['activations_sha256']:
        raise SystemExit('公開の置き場の活性の SHA-256 が手元と違う')
    tools = import_closure(TOOLS)
    dr = res['dry_run']['path']
    frozen = {r: sha16f(P(r)) for r in FILES + [dr, rel(CC_COPY)] + tools + READS}
    frozen[rel(ACT_PUB)] = sha16f(ACT_PUB)
    R = {'kind': 'blens_freeze_record', 'version': VERSION, 'frozen_jst': a.when, 'registrant_words': a.words, 'ruling': 'D186',
         'frozen_sha16': frozen, 'tools_import_closure': tools, 'activations': {'path': rel(ACT_PUB), 'sha256': res['activations_sha256'], 'bytes': os.path.getsize(ACT_PUB)},
         'checks': res, 'deviation_rule': '凍結の後の変更は、逸脱として番号・日付・理由・登録者の承認を台帳に記す（正本 §9・段階 B の型）',
         'next': '記録先行の公開（push）→ 予想の封印（コーディネータが先・SHA だけを伝える → 登録者）→ Colab の相 extract → 層一・層二・報告（結果は登録者と一緒に開く）',
         'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    json.dump(R, open(FR_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    md = ['# B-lens の凍結の記録（機械生成・`tools/freeze_Blens.py` %s）' % VERSION, '',
          '- 凍結: %s（日本時間）・登録者の言葉は逐語で「%s」（裁定 D186）。' % (a.when, a.words),
          '- 本文: `design/design-Blens-FROZEN.md`（SHA16 %s）・草案3 との差は題名・凍結の行・組み立ての記録だけ。' % frozen['design/design-Blens-FROZEN.md'],
          '- 八腕の主位置の活性を公開の置き場 `%s` に写した（SHA-256 %s・%d バイト・裁定 D175）。' % (rel(ACT_PUB), res['activations_sha256'], os.path.getsize(ACT_PUB)),
          '- 組み立てた中と単独で割り方が違った集合（裁定 D184・組み立てた中を主にした）: %s。' % ('・'.join(sorted(res['sets']['in_prompt_differences'])) or '無し'),
          '- Colab の確かめ（相 check）: %s。' % '・'.join('%s %s' % (k, '合う' if v else '外れ') for k, v in res['colab_check'].items() if isinstance(v, bool)),
          '- 合成データ: `%s`（%s 経路・外れ %s）。' % (res['dry_run']['path'], res['dry_run']['paths'], res['dry_run']['off']),
          '- 次: ' + R['next'], '', '## 凍結物の SHA16', '', '| 置き場 | SHA16 |', '|---|---|'] + ['| `%s` | %s |' % kv for kv in sorted(frozen.items())] + ['', R['clause'], '']
    open(FR_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(md))
    row = ('| %s | **B-lens 凍結**（登録者「%s」2026-09-23 20:19 日本時間・裁定 D186）: 草案3 の原稿を design/design-Blens-FROZEN.src.md に逐語複製し題名と凍結の一行のみ改めた。'
           '凍結の記録 records/Blens/FREEZE-RECORD-Blens.json（凍結物 %d 件・器の閉包 %d）。八腕の主位置の活性を公開の置き場に写した（裁定 D175）。封印はこの後（コーディネータが先）。 | '
           'design/design-Blens-FROZEN.md | %s | 凍結の後の変更は逸脱として台帳に記す |' % (a.when.split(' ')[0], a.words, len(frozen), len(tools), frozen['design/design-Blens-FROZEN.md']))
    led = open(LEDGER, encoding='utf-8').read()
    if 'B-lens 凍結' not in led:
        open(LEDGER, 'a', encoding='utf-8', newline=NL).write(('' if led.endswith(NL) else NL) + row + NL)
    print('[freeze_Blens] 凍結を記帳した: %s・%s（凍結物 %d）' % (rel(FR_JSON), rel(FR_MD), len(frozen)))


if __name__ == '__main__':
    main()
