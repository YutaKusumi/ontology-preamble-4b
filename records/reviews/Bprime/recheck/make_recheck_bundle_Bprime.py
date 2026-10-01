# -*- coding: utf-8 -*-
"""make_recheck_bundle_Bprime.py v0 —— B′ の器の実装の直しの確かめの巡（凍結の前の最後の検分の巡・裁定 D277・D278）に渡す束を作る（2026-10-01・コーディネータ南無弥勒如来・非公開）。

束 = 今の形の木 ＋ 確かめの材料（`recheck/`）:
  - 今の形の木: 器の実装の検分の束の器（`tools/make_impl_bundle_Bprime.py` の `build`）で、今の作業の置き場から組む（前の巡の束と同じ組み方なので、差分には中身の違いだけが出る）。
    その器の説明（README）と目録は、前の巡の字（草案10 など）のままなので外し、この器の説明と目録に替える。
  - `recheck/diff/`: 前の巡の検分者が見た束（`impl-bundle-Bprime.zip`・SHA-256 は下の BASE_SHA256 で照らす）と今の木の、ファイルごとの差分（unified diff・前後三行）と、
    変わった・足した・外したファイルの一覧（`INDEX.md`・SHA16 と行の増減）。
  - `recheck/adoption-table-impl-Bprime.md`: 採否の表（U01〜U52・K25〜K27・所見と直しの対応）の写し。
束は作業の一時の置き場に書き、GitHub には置かない。送るのは登録者の確認の後。依頼文と枠は別の器（`make_recheck_request.py`）。
用法: python reviews/recheck/make_recheck_bundle_Bprime.py <前の巡の束の zip> <書く束の zip>
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, io, json, hashlib, zipfile, difflib, tempfile, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(BP, 'tools'))
VERSION = 'v0'
NL = chr(10)
BASE_SHA256 = 'C89AE3FF939C41FFE626B8CBD143281A32E6547691F1871BA46F4CC9A4B2F3F0'
BASE_PREFIX, CUR_PREFIX, OUT_PREFIX = 'bprime-impl-bundle/', 'bprime-impl-bundle/', 'bprime-recheck-bundle/'
OLD_META = ('README-impl-bundle-Bprime.md', 'MANIFEST-impl-bundle-Bprime.json')
SKIP_CUR = ('records/reviews/Bprime/recheck/',)        # この巡の置き場（枠の予想と依頼文を組む器）は束に入れない（検分者に書き手の予想を見せない・前の巡の束の器の v0.1 と同じ）
DRAFT_PAIR = ('design/design-Bprime-draft10.md', 'design/design-Bprime-draft11.md')     # 草案は版ごとに別のファイルなので、前の版から今の版への差分を別に足す
TEXT_EXT = ('.py', '.md', '.json', '.txt', '.jsonl', '.csv', '.yaml', '.yml', '.toml', '.cfg', '.ini', '.sh', '.tsv')
ADOPTION = os.path.join(BP, 'reviews', 'impl', 'adoption-table-impl-Bprime.md')
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha256b(b):
    return hashlib.sha256(b).hexdigest().upper()


def members(zp, prefix):
    z = zipfile.ZipFile(zp)
    out = collections.OrderedDict()
    for n in z.namelist():
        if n.endswith('/'):
            continue
        assert n.startswith(prefix), (zp, n)
        rel = n[len(prefix):]
        if rel in OLD_META or rel.startswith(SKIP_CUR):
            continue
        out[rel] = z.read(n)
    return out


def is_text(rel, b):
    if not rel.endswith(TEXT_EXT):
        return False
    try:
        b.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def diff_of(rel, a, b):
    la = a.decode('utf-8').split(NL) if a is not None else []
    lb = b.decode('utf-8').split(NL) if b is not None else []
    d = list(difflib.unified_diff(la, lb, fromfile='a/%s（前の巡の束）' % rel if a is not None else '/dev/null', tofile='b/%s（今）' % rel if b is not None else '/dev/null', n=3, lineterm=''))
    plus = sum(1 for x in d if x.startswith('+') and not x.startswith('+++'))
    minus = sum(1 for x in d if x.startswith('-') and not x.startswith('---'))
    return NL.join(d) + NL, plus, minus


def readme(C, n_files, idx):
    L = ['# B′ の器の実装の直しの確かめの束（機械生成・`reviews/recheck/make_recheck_bundle_Bprime.py` %s）' % VERSION, '',
         '- 束は公開の置き場の形の一つの置き場です。前の巡（器の実装の検分）の束と同じ組み方で、今の作業の置き場から組みました（%d 本・目録 `MANIFEST-recheck-bundle-Bprime.json`）。' % n_files,
         '  正本は `design/contrasts-Bprime.json`（版 %s）、草案は `design/design-Bprime-draft11.md` です。' % C['version'],
         '- 前の巡の束（SHA-256 `%s`）との違いは `recheck/diff/` にあります。一覧は `recheck/diff/INDEX.md`（変わった %d・足した %d・外した %d）です。'
         % (BASE_SHA256, len(idx['changed']), len(idx['added']), len(idx['removed'])),
         '- 所見と直しの対応は `recheck/adoption-table-impl-Bprime.md`（採否の表）、器の段の記録は `records/Bprime/tools/tools-log-Bprime.md` です。',
         '- 合成データの正式の記録は `records/Bprime/dry-run-Bprime-2026-09-30.md` と `records/Bprime/freeze-path-dry-Bprime-2026-09-30.md` です。'
         'ただし、この記録の後に直した器が二つあります（報告の組み立ての器 v0.4 と合成データの確かめの器 v1.0・器の段の記録の K28・裁定 D278）。この二つは、記録の SHA の表と合いません（凍結の前に取り直します）。', '',
         '## 実行の場での走らせ方', '',
         '```', 'pip install numpy==2.4.6 transformers==5.16.1',
         'export OP4B_REPO="$PWD" OP4B_PUBLIC_REPO="$PWD" OP4B_PUB_TOOLS="$PWD/tools" PYTHONIOENCODING=utf-8', '```', '',
         '- 器の自己検査は、前の巡の束と同じく `python tools/<器>.py --selftest` で走ります。torch の要らない器と、transformers と tokenizers が要る器の一覧は、前の巡の束の説明と同じです'
         '（`tools/make_impl_bundle_Bprime.py` の `NO_TORCH`・`TOKENIZER`・`TORCH`）。torch が要る器は走らせず、器の中と正式の記録を読んで照らしてください。',
         '- 別の個体の二つの器（`tools/bprime_recompute_rewrite.py`・`tools/bprime_reextract.py`）は、この束の形のままでは自己検査が走りません（前の巡と同じ）。この巡では変えていません。', '',
         '## 読まないでほしい物・しないでほしいこと', '',
         '- 実の重みを読み込まない・実の重みで順伝播を走らせない（封印の前の決まり・正本 `computation.before_seal`）。`tools/colab/boot_bprime.py` を DRY（環境変数 `OP4B_DRY=1`）でなく走らせない。',
         '- 外への呼び出しをしない（`tools/send_external_Bprime.py` は `--selftest` だけ・送る操作はしない）。', '', CLAUSE, '']
    return NL.join(L)


def build(base_zip, out_zip):
    got = sha256b(open(base_zip, 'rb').read())
    assert got == BASE_SHA256, ('前の巡の束の SHA-256 が違う', got)
    import make_impl_bundle_Bprime as MIB
    C = json.load(open(os.path.join(BP, 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    with tempfile.TemporaryDirectory() as td:
        cur_zip = os.path.join(td, 'cur.zip')
        info = MIB.build(cur_zip)
        base, cur = members(base_zip, BASE_PREFIX), members(cur_zip, CUR_PREFIX)
    assert DRAFT_PAIR[0] in base and DRAFT_PAIR[1] in cur and DRAFT_PAIR[1] not in base, '草案の組がそろわない'
    idx = {'changed': [], 'added': [], 'removed': [], 'binary_changed': []}
    diffs = collections.OrderedDict()
    for rel in sorted(set(base) | set(cur)):
        a, b = base.get(rel), cur.get(rel)
        if a is not None and b is not None and a == b:
            continue
        kind = 'changed' if (a is not None and b is not None) else ('added' if a is None else 'removed')
        text = is_text(rel, b if b is not None else a) and (a is None or is_text(rel, a))
        row = {'path': rel, 'before16': sha256b(a)[:16] if a is not None else None, 'after16': sha256b(b)[:16] if b is not None else None}
        if text:
            d, plus, minus = diff_of(rel, a, b)
            diffs['recheck/diff/' + rel + '.diff'] = d.encode('utf-8')
            row.update({'plus': plus, 'minus': minus})
        elif kind == 'changed':
            idx['binary_changed'].append(rel)
        idx[kind].append(row)
    dd, dp, dm = diff_of('%s → %s' % DRAFT_PAIR, base[DRAFT_PAIR[0]], cur[DRAFT_PAIR[1]])
    diffs['recheck/diff/design/design-Bprime-draft10-to-draft11.md.diff'] = dd.encode('utf-8')
    L = ['# 前の巡の束と今の木の違い（機械生成・`make_recheck_bundle_Bprime.py` %s）' % VERSION, '',
         '- 前の巡の束: SHA-256 `%s`（器の実装の検分で claude.ai の二つのチャットに添えた束）。今の木: 同じ組み方（`tools/make_impl_bundle_Bprime.py` の `build`）で今の作業の置き場から組んだ。' % BASE_SHA256,
         '- 束の説明と目録（前の巡の字のまま）は比べない。行の増減は unified diff の + と − の行の数。',
         '- 草案は版ごとに別のファイル（草案10 は前の巡の束にもあり、今の木にも残る）なので、草案10 から草案11 への差分を `recheck/diff/design/design-Bprime-draft10-to-draft11.md.diff` に別に置いた（+ %d・− %d）。' % (dp, dm), '']
    for kind, title in (('changed', '変わったファイル'), ('added', '足したファイル'), ('removed', '外したファイル')):
        L += ['## %s（%d）' % (title, len(idx[kind])), '', '| ファイル | 前 SHA16 | 今 SHA16 | + | − |', '|---|---|---|---|---|']
        L += ['| `%s` | %s | %s | %s | %s |' % (r['path'], r['before16'] or '—', r['after16'] or '—', r.get('plus', '—'), r.get('minus', '—')) for r in idx[kind]]
        L.append('')
    if idx['binary_changed']:
        L += ['- 字でないファイルで変わったもの（差分は無い）: ' + '・'.join('`%s`' % x for x in idx['binary_changed']), '']
    L += [CLAUSE, '']
    extra = collections.OrderedDict()
    extra['recheck/diff/INDEX.md'] = NL.join(L).encode('utf-8')
    extra.update(diffs)
    extra['recheck/adoption-table-impl-Bprime.md'] = open(ADOPTION, 'rb').read()
    files = collections.OrderedDict((rel, cur[rel]) for rel in sorted(cur))
    files.update(extra)
    rd = readme(C, len(files) + 2, idx).encode('utf-8')
    files['README-recheck-bundle-Bprime.md'] = rd
    man = collections.OrderedDict([('kind', 'bprime_recheck_bundle'), ('version', VERSION), ('contract_version', C['version']), ('base_bundle_sha256', BASE_SHA256),
                                   ('files', collections.OrderedDict((f, {'sha256': sha256b(b), 'bytes': len(b)}) for f, b in files.items())), ('clause', CLAUSE)])
    files['MANIFEST-recheck-bundle-Bprime.json'] = json.dumps(man, ensure_ascii=False, indent=1).encode('utf-8')
    assert not os.path.exists(out_zip), out_zip
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f, b in files.items():
            z.writestr(OUT_PREFIX + f, b)
    return {'files': len(files), 'zip_mb': round(os.path.getsize(out_zip) / 2 ** 20, 2), 'zip_sha256': sha256b(open(out_zip, 'rb').read()),
            'changed': len(idx['changed']), 'added': len(idx['added']), 'removed': len(idx['removed']), 'binary_changed': idx['binary_changed'],
            'diff_lines': sum(d.count(b'\n') for d in diffs.values()), 'impl_builder': info}


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if len(sys.argv) != 3:
        raise SystemExit('用法: python reviews/recheck/make_recheck_bundle_Bprime.py <前の巡の束の zip> <書く束の zip>')
    print('[make_recheck_bundle_Bprime] %s' % json.dumps(build(sys.argv[1], sys.argv[2]), ensure_ascii=False))
