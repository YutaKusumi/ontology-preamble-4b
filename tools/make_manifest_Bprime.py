# -*- coding: utf-8 -*-
"""make_manifest_Bprime.py v0 —— B′ の重みの断片の SHA-256 の目録（`records/Bprime/MANIFEST-gemma-4-31B-it.json`・正本 `inputs.model.manifest`・器の段の所見 K9・2026-09-30・
コーディネータ南無弥勒如来）。

手元の目録（`hf/gemma-4-31B-it/<版>/MANIFEST-local.json`・設定とトークナイザなど七本の SHA-256 を手元のファイルから計算したもの）と、手元の重みの索引
（`model.safetensors.index.json`・断片の名）から、断片の名の一覧を作る。断片の SHA-256 と大きさは、Hugging Face の目録（`HfApi.model_info(..., files_metadata=True)` の
LFS の値）から取る（**重みそのものは落とさない**・`--fetch` を与えたときだけ外に問い合わせる・資格情報は使わない〔公開の重み〕）。
手元の七本は、Hugging Face の目録の値と照らせるもの（LFS の物）は照らし、合わなければ止める。起動器は目録の `files` のすべてを、落とした重みの SHA-256 と照らす。
記録は一度だけ書く（既にあれば止める）。
用法: python tools/make_manifest_Bprime.py --fetch ／ --selftest（外に問い合わせない・合成の目録で）
柵: 本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.dirname(HERE)
VERSION = 'v0'
NL = chr(10)
REPO_ID = 'google/gemma-4-31B-it'
REV = '842da3794eaa0b77d5f08bae87a17459d91ff475'
LOCAL_DIR = os.path.join(BP, 'hf', 'gemma-4-31B-it', REV)
OUT = os.path.join(BP, 'records', 'Bprime', 'MANIFEST-gemma-4-31B-it.json')
CLAUSE = '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'


def sha16f(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]


def build(local_manifest, index, meta_files):
    """local_manifest: 手元の目録・index: 重みの索引・meta_files: 名 → {'size', 'lfs_sha256'（LFS の物だけ）}（Hugging Face の目録）。"""
    if local_manifest['repo'] != REPO_ID or local_manifest['revision'] != REV:
        raise SystemExit('手元の目録の置き場の名か版が違う')
    shards = sorted(set(index['weight_map'].values()))
    files = collections.OrderedDict()
    for name, r in sorted(local_manifest['files'].items()):
        m = meta_files.get(name)
        if m and m.get('lfs_sha256') and m['lfs_sha256'].lower() != r['sha256'].lower():
            raise SystemExit('手元の目録の SHA-256 が Hugging Face の目録の値と違う: %s' % name)
        files[name] = {'bytes': r['bytes'], 'sha256': r['sha256'].upper(), 'source': 'local'}
    miss = [s for s in shards if not (meta_files.get(s) or {}).get('lfs_sha256')]
    if miss:
        raise SystemExit('Hugging Face の目録に断片の LFS の SHA-256 が無い: %s' % miss[:5])
    for s in shards:
        files[s] = {'bytes': int(meta_files[s]['size']), 'sha256': meta_files[s]['lfs_sha256'].upper(), 'source': 'hf_lfs'}
    return collections.OrderedDict([('kind', 'bprime_weights_manifest'), ('version', VERSION), ('repo', REPO_ID), ('revision', REV), ('files', files), ('index_shards', shards),
                                    ('n_shards', len(shards)), ('bytes_shards', sum(files[s]['bytes'] for s in shards)), ('clause', CLAUSE)])


def fetch_meta():
    """Hugging Face の目録（外への問い合わせ・重みは落とさない・資格情報は使わない）。"""
    from huggingface_hub import HfApi
    info = HfApi().model_info(REPO_ID, revision=REV, files_metadata=True, token=False)
    out = {}
    for s in info.siblings:
        lfs = getattr(s, 'lfs', None)
        sha = (lfs.get('sha256') if isinstance(lfs, dict) else getattr(lfs, 'sha256', None)) if lfs else None
        out[s.rfilename] = {'size': getattr(s, 'size', None) or (lfs.get('size') if isinstance(lfs, dict) else getattr(lfs, 'size', None)), 'lfs_sha256': sha}
    return out, getattr(info, 'sha', None)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if '--selftest' in sys.argv:
        return _selftest()
    if '--fetch' not in sys.argv:
        raise SystemExit('外に問い合わせるときだけ --fetch を与える（登録者の確認の後）')
    if os.path.exists(OUT):
        raise SystemExit('既にある（一度だけ書く）')
    with open(os.path.join(LOCAL_DIR, 'MANIFEST-local.json'), encoding='utf-8') as fh:
        LM = json.load(fh)
    with open(os.path.join(LOCAL_DIR, 'model.safetensors.index.json'), encoding='utf-8') as fh:
        IX = json.load(fh)
    meta, commit = fetch_meta()
    if commit and commit != REV:
        raise SystemExit('Hugging Face の目録の版が固定の版と違う: %s' % commit)
    R = build(LM, IX, meta)
    R['source'] = {'local_manifest_sha16': sha16f(os.path.join(LOCAL_DIR, 'MANIFEST-local.json')), 'index_sha16': sha16f(os.path.join(LOCAL_DIR, 'model.safetensors.index.json')),
                   'hf_metadata': 'HfApi.model_info(files_metadata=True)・%s' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'hf_revision_seen': commit}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline=NL) as fh:
        json.dump(R, fh, ensure_ascii=False, indent=1)
    print('[make_manifest_Bprime] 目録を書いた: 断片 %d・ファイル %d・SHA16 %s' % (R['n_shards'], len(R['files']), sha16f(OUT)))


def _selftest():
    LM = {'repo': REPO_ID, 'revision': REV, 'files': {'config.json': {'bytes': 10, 'sha256': 'ab' * 32}, 'tokenizer.json': {'bytes': 20, 'sha256': 'cd' * 32}}}
    IX = {'weight_map': {'a': 'model-00001-of-00002.safetensors', 'b': 'model-00002-of-00002.safetensors', 'c': 'model-00001-of-00002.safetensors'}}
    meta = {'model-00001-of-00002.safetensors': {'size': 5, 'lfs_sha256': '01' * 32}, 'model-00002-of-00002.safetensors': {'size': 6, 'lfs_sha256': '02' * 32},
            'tokenizer.json': {'size': 20, 'lfs_sha256': 'cd' * 32}, 'config.json': {'size': 10, 'lfs_sha256': None}}
    R = build(LM, IX, meta)
    ok = [R['index_shards'] == ['model-00001-of-00002.safetensors', 'model-00002-of-00002.safetensors'] and R['files']['model-00002-of-00002.safetensors']['sha256'] == ('02' * 32).upper()
          and R['files']['config.json']['source'] == 'local' and R['bytes_shards'] == 11]
    for bad_meta, why in ((dict(meta, **{'tokenizer.json': {'size': 20, 'lfs_sha256': 'ee' * 32}}), '手元と目録の違い'),
                          ({k: v for k, v in meta.items() if k != 'model-00002-of-00002.safetensors'}, '断片の欠け')):
        try:
            build(LM, IX, bad_meta)
            ok.append(False)
        except SystemExit:
            ok.append(True)
    assert all(ok), ok
    print('make_manifest_Bprime.py %s SELFTEST PASS（断片の名は索引から・手元と目録の違いで止まる・断片の欠けで止まる・外には問い合わせていない）' % VERSION)


if __name__ == '__main__':
    main()
