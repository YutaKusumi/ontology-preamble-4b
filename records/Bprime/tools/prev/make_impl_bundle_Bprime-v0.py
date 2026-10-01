# -*- coding: utf-8 -*-
"""make_impl_bundle_Bprime.py v0 —— B′ の器の実装の検分（正本 `review_plan.impl`・claude.ai の新しいチャット二つ・D269）に渡す束を作る（2026-09-30・コーディネータ南無弥勒如来）。

束は一つの置き場（公開の置き場の形）にまとめた zip:
  - B′ の木: 移す器（`publish_Bprime`）で作業の置き場から写した公開の形（器・正本・草案・記録）。設計の巡の記録・中立の課題の感触の確かめ・器の前の版は入れない（検分に要らない・束を小さく）。
  - 凍結の器と読む物: B′ の器の読み込みの閉包に入る公開の置き場の器・段階 B の走行器が文字として読む器（`tools/run_preamble_local.py`）・`arms/` の全体（走行器が SHA を確かめる）・
    正本 `inputs.files_public` の置き場の物（器が読む公開の記録）。どれも公開の置き場の決めた版（正本 `inputs.public_version`）の字のまま。
  - 設定とトークナイザ: `hf/gemma-4-31B-it/<版>/`（手元の写し・器がこの道筋で読む）。
  - `README-impl-bundle-Bprime.md`（日本語・実行の場での走らせ方と、torch の要る器の印）と、束の目録 `MANIFEST-impl-bundle-Bprime.json`（置き場・SHA-256・大きさ）。
束は作業の一時の置き場に書き、GitHub には置かない。送るのは登録者の確認の後（claude.ai の新しいチャット二つ・依頼文は別の器）。
用法: python tools/make_impl_bundle_Bprime.py <束の zip の置き場>
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, glob, shutil, hashlib, zipfile, tempfile, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bprime_gemma as G
import publish_Bprime as PUBL
import freeze_Bprime as FZ

VERSION = 'v0'
NL = chr(10)
PUB = G.REPO
REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'
SKIP_PREFIX = ('records/reviews/Bprime/design-round', 'records/Bprime/model-feel', 'records/Bprime/tools/prev/', 'records/Bprime/design/prev/', 'records/Bprime/cost-pilot/kit/')
NO_TORCH = ['tools/bprime_core.py', 'tools/bprime_typo.py', 'tools/bprime_external.py', 'tools/analyze_Bprime.py', 'tools/sweep_Bprime.py', 'tools/build_report_Bprime.py',
            'tools/make_frozen_Bprime.py', 'tools/make_predictions_form_Bprime.py', 'tools/seal_Bprime.py', 'tools/send_external_Bprime.py', 'tools/make_manifest_Bprime.py',
            'tools/freeze_Bprime.py']
TOKENIZER = ['tools/close_behavior_Bprime.py']                 # transformers と tokenizers が要る（torch は要らない形で書いた・走るかは実行の場で確かめてもらう）
TORCH = ['tools/bprime_behavior.py', 'tools/bprime_directions.py', 'tools/dry_bprime.py', 'tools/dry_bprime_behavior.py', 'tools/dry_run_Bprime.py',
         'tools/bprime_recompute_rewrite.py', 'tools/bprime_reextract.py', 'tools/colab/boot_bprime.py']
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 22), b''):
            h.update(blk)
    return h.hexdigest().upper()


def git_show(rel, commit):
    r = subprocess.run(['git', '-C', PUB, 'show', '%s:%s' % (commit, rel)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit('公開の置き場の決めた版に無い: %s' % rel)
    return r.stdout


def readme(C, n_files, dry_rec):
    L = ['# B′ の器の実装の検分の束（機械生成・`tools/make_impl_bundle_Bprime.py` %s）' % VERSION, '',
         '- 束は公開の置き場の形の一つの置き場です。B′ の器・正本（`design/contrasts-Bprime.json`・版 %s）・草案（`design/design-Bprime-draft10.md`）・記録（`records/Bprime/`）と、'
         'B′ の器が呼ぶ凍結の器（層三・B-lens・段階 B・公開の置き場の版 `%s`）・`arms/`・設定とトークナイザ（`hf/gemma-4-31B-it/%s/`）を入れました（%d 本・目録 `MANIFEST-impl-bundle-Bprime.json`）。'
         % (C['version'], C['inputs']['public_version'], REV, n_files),
         '- 器の段の記録は `records/Bprime/tools/tools-log-Bprime.md`、書き手と別の個体の器の指示と開発の記録は `records/Bprime/tools/independent/` にあります。', '',
         '## 実行の場での走らせ方', '',
         '```', 'pip install numpy==2.4.6 transformers==5.16.1',
         'export OP4B_REPO="$PWD" OP4B_PUBLIC_REPO="$PWD" OP4B_PUB_TOOLS="$PWD/tools" PYTHONIOENCODING=utf-8', '```', '',
         '- torch の要らない器の自己検査（numpy と SciPy だけで走る）: ' + '・'.join('`python %s --selftest`' % t for t in NO_TORCH) + '。',
         '- transformers と tokenizers が要る器（torch は要らない形で書いたつもりですが、走るかを確かめてください）: ' + '・'.join('`python %s --selftest`' % t for t in TOKENIZER) + '。',
         '- torch が要る器（小さな乱数の Gemma 4 で確かめる器・実行の場に torch が無ければ走らせず、器の中と正式の記録を読んで照らしてください）: ' + '・'.join('`%s`' % t for t in TORCH) + '。',
         '- 合成データの正式の記録（Colab の CPU のランタイムで走らせた・小さな模型の確かめを含む）: %s。' % (('`%s`' % dry_rec) if dry_rec else '（まだ無い）'),
         '- 別の個体の二つの器（`tools/bprime_recompute_rewrite.py`・`tools/bprime_reextract.py`）の自己検査と `--dry` は、器の置き場から二つ上を B′ の作業の置き場とみなす形で書かれているので、'
         'この束の形のままでは走りません（本番の起動器は正本と台帳を引数で渡すので、この形に依りません）。結果は開発の記録と正式の記録にあります。', '',
         '## 読まないでほしい物・しないでほしいこと', '',
         '- 実の重みを読み込まない・実の重みで順伝播を走らせない（封印の前の決まり・正本 `computation.before_seal`）。`tools/colab/boot_bprime.py` を DRY（環境変数 `OP4B_DRY=1`）でなく走らせない。',
         '- 外への呼び出しをしない（`tools/send_external_Bprime.py` は `--selftest` だけ・送る操作はしない）。', '', CLAUSE, '']
    return NL.join(L)


def build(out_zip):
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    commit = C['inputs']['public_version']
    with tempfile.TemporaryDirectory() as td:
        T = os.path.join(td, 'tree')
        rows, P = PUBL.publish(T)
        drop = [r['dst'] for r in rows if r['dst'].startswith(SKIP_PREFIX)]
        for d in drop:
            os.remove(os.path.join(T, *d.split('/')))
        # 凍結の器の閉包と読む物（公開の置き場の決めた版の字のまま）
        closure = [c for c in FZ.import_closure(FZ.TOOLS) if not os.path.exists(os.path.join(T, *c.split('/')))]
        pub_files = set(closure) | {'tools/run_preamble_local.py'} | {v['path'] for v in C['inputs']['files_public'].values()}
        pub_files |= set(subprocess.run(['git', '-C', PUB, 'ls-tree', '-r', '--name-only', commit, 'arms'], capture_output=True, text=True).stdout.split())
        for rel in sorted(pub_files):
            dst = os.path.join(T, *rel.split('/'))
            if os.path.exists(dst):
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'wb') as fh:
                fh.write(git_show(rel, commit))
        # 設定とトークナイザ
        hf_src = os.path.join(BP, 'hf', 'gemma-4-31B-it', REV)
        hf_dst = os.path.join(T, 'hf', 'gemma-4-31B-it', REV)
        os.makedirs(hf_dst, exist_ok=True)
        for fn in sorted(os.listdir(hf_src)):
            if os.path.isfile(os.path.join(hf_src, fn)):
                shutil.copyfile(os.path.join(hf_src, fn), os.path.join(hf_dst, fn))
        dry = sorted(glob.glob(os.path.join(T, 'records', 'Bprime', 'dry-run-Bprime-*.md')))
        dry_rec = os.path.relpath(dry[-1], T).replace(os.sep, '/') if dry else None
        files = []
        for root, _, fs in os.walk(T):
            for f in fs:
                files.append(os.path.relpath(os.path.join(root, f), T).replace(os.sep, '/'))
        files.sort()
        with open(os.path.join(T, 'README-impl-bundle-Bprime.md'), 'w', encoding='utf-8', newline=NL) as fh:
            fh.write(readme(C, len(files) + 2, dry_rec))
        man = collections.OrderedDict([('kind', 'bprime_impl_bundle'), ('version', VERSION), ('contract_version', C['version']), ('public_version', commit),
                                       ('files', collections.OrderedDict((f, {'sha256': sha256f(os.path.join(T, *f.split('/'))), 'bytes': os.path.getsize(os.path.join(T, *f.split('/')))}) for f in files)),
                                       ('clause', CLAUSE)])
        with open(os.path.join(T, 'MANIFEST-impl-bundle-Bprime.json'), 'w', encoding='utf-8', newline=NL) as fh:
            json.dump(man, fh, ensure_ascii=False, indent=1)
        with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for f in files + ['README-impl-bundle-Bprime.md', 'MANIFEST-impl-bundle-Bprime.json']:
                z.write(os.path.join(T, *f.split('/')), 'bprime-impl-bundle/' + f)
    return {'files': len(files) + 2, 'zip_mb': round(os.path.getsize(out_zip) / 2 ** 20, 2), 'zip_sha256': sha256f(out_zip), 'dropped': len(drop), 'public_added': len(pub_files), 'dry_record': dry_rec}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) != 2:
        raise SystemExit('用法: python tools/make_impl_bundle_Bprime.py <束の zip の置き場>')
    print('[make_impl_bundle_Bprime] %s' % json.dumps(build(sys.argv[1]), ensure_ascii=False))
