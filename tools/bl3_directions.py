# -*- coding: utf-8 -*-
"""bl3_directions.py v1 —— B-lens 層三（Bl3）の方向の npz を手元で作る（正本 `nulls.storage`・裁定 D211・2026-09-25）。

作るもの（選んだ層・`float64`・‖v̂〔static〕‖ にノルムを揃える）:
  - named: 名前のある方向（正本 `directions.named` の順・凍結の npz `results/dirB/dirB__s1/directions.npz` から `steer_B.match_to_static`）
  - B_random: 段階 B の本走行の三本（凍結の `steer_B.random_directions`・相 main）
  - iso: 等方のランダム方向（正本 `nulls.isotropic`・`blens_core.iso_directions`）
  - real: 実在の差の方向（凍結の活性の抽出の場面の平均の八腕の全ての対・`blens_core.real_differences`・名の並びは正本 `nulls.real.arms` の順の i<j）
  - check: 本の計算の頭の近道の確かめの一本（正本 `computation.steered_cache_check.seed`・帰無に入らない）
組ごとの SHA-256（`float64` の連続したバイト）を、設計事実の転記行 D の値と突き合わせ、違えば止める（転記行 D の器 `tools/bl3_facts.py` と同じ作り方）。
npz は時刻を持たない形（zip の日付を固定・圧縮なし）で書くので、再実行で同一バイトになる。`--check` は作り直して置き場の npz とバイトで突き合わせる。
**効き目は一つも計算しない**（模型を読まない）。
出力: results/Bl3/directions-Bl3.npz・results/Bl3/directions-Bl3.json（--force が無ければ上書きしない）
用法: python tools/bl3_directions.py [--force] ／ --check ／ --selftest
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, io, sys, json, hashlib, zipfile, argparse, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
VERSION = 'v1'
NL = chr(10)
OUT_NPZ = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.npz')
OUT_JSON = os.path.join(REPO, 'results', 'Bl3', 'directions-Bl3.json')
ACT = os.path.expanduser('~/.cache/op4b-dir/dirB__s1/main_position_activations.npz')
GROUPS = ('named', 'B_random', 'iso', 'real', 'check')
ZDATE = (1980, 1, 1, 0, 0, 0)
sha_arr = lambda x: hashlib.sha256(np.ascontiguousarray(np.asarray(x, dtype=np.float64)).tobytes()).hexdigest().upper()


def write_npz_fixed(path, arrays):
    """時刻を持たない npz（名の順・圧縮なし・zip の日付を固定）。np.load で読める。"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_STORED) as zf:
        for name in arrays:
            zi = zipfile.ZipInfo(name + '.npy', date_time=ZDATE)
            zi.compress_type = zipfile.ZIP_STORED
            zi.external_attr = 0o644 << 16
            with zf.open(zi, 'w', force_zip64=True) as f:
                np.lib.format.write_array(f, np.ascontiguousarray(arrays[name]), allow_pickle=False)
    b = buf.getvalue()
    if path is not None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'wb').write(b)
    return b


def build(T3, TL):
    """正本と凍結物から、組ごとの方向（float64）と名の並びを作る。"""
    import steer_B
    import blens_core as C
    sel = str(T3['layers']['selected_ratio'])
    D = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
    v = D['static__%s' % sel].astype(np.float64)
    nv = float(np.linalg.norm(v))
    named = collections.OrderedDict((k, steer_B.match_to_static(D['%s__%s' % (k, sel)].astype(np.float64), v)) for k in T3['directions']['named'])
    b3 = np.array(steer_B.random_directions(v, 'main', float(sel)), dtype=np.float64)
    assert len(b3) == T3['nulls']['B_random']['count']
    iso = C.iso_directions(v, T3['nulls']['isotropic']['seed'], float(sel), T3['nulls']['isotropic']['count'], T3['nulls']['isotropic']['layer_key_scale']).astype(np.float64)
    DJ = json.load(open(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.json'), encoding='utf-8'))
    act_sha = hashlib.sha256(open(ACT, 'rb').read()).hexdigest().upper()
    if act_sha != DJ['activations_npz_sha256'].upper():
        raise SystemExit('活性のファイルが凍結の記録と違う（止める）')
    Z = np.load(ACT)
    arm_means = collections.OrderedDict((arm, np.mean([Z['same_order__%s__%s__%s' % (arm, sc, sel)].astype(np.float64) for sc in DJ['extraction_scenarios']], axis=0))
                                        for arm in T3['nulls']['real']['arms'])
    real = C.real_differences(arm_means, nv)
    assert len(real) == T3['nulls']['real']['pairs']
    chk = C.iso_directions(v, T3['computation']['steered_cache_check']['seed'], float(sel), 1, T3['nulls']['isotropic']['layer_key_scale']).astype(np.float64)
    arrays = collections.OrderedDict([('named', np.array(list(named.values()), dtype=np.float64)), ('B_random', b3), ('iso', iso),
                                      ('real', np.array(list(real.values()), dtype=np.float64)), ('check', chk)])
    names = collections.OrderedDict([('named', list(named)), ('B_random', ['rand:%d' % i for i in range(len(b3))]), ('iso', ['iso:%d' % i for i in range(len(iso))]),
                                     ('real', list(real)), ('check', ['check'])])
    meta = {'layer_ratio': float(sel), 'dim': int(v.shape[0]), 'vhat_norm': nv, 'activations_sha256': act_sha}
    return arrays, names, meta


def verify_against_facts(arrays, FJ):
    """組ごとの SHA-256 を、設計事実の転記行 D と突き合わせる（違えば止める）。"""
    D = FJ['facts']['D']
    want = {'named': D['named_sha256'], 'B_random': D['B_random_sha256'], 'iso': D['iso_sha256'], 'real': D['real_sha256'], 'check': D['cache_check_sha256']}
    got = {k: sha_arr(arrays[k]) for k in GROUPS}
    bad = {k: (got[k][:16], want[k][:16]) for k in GROUPS if got[k] != want[k]}
    if bad:
        raise SystemExit('方向の組の SHA-256 が設計事実の転記行 D と違う（止める）: %s' % bad)
    if sum(len(arrays[k]) for k in GROUPS) != D['npz_directions']:
        raise SystemExit('方向の本数が設計事実の転記行 D と違う（止める）')
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--check', action='store_true', help='作り直して置き場の npz とバイトで突き合わせる')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    T3 = json.load(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), encoding='utf-8'))
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    FJ = json.load(open(os.path.join(REPO, 'records', 'Bl3', 'design-facts-Bl3.json'), encoding='utf-8'))
    arrays, names, meta = build(T3, TL)
    sha = verify_against_facts(arrays, FJ)
    b = write_npz_fixed(None, arrays)
    file_sha = hashlib.sha256(b).hexdigest().upper()
    if a.check:
        if not os.path.exists(OUT_NPZ):
            raise SystemExit('置き場に npz が無い: %s' % OUT_NPZ)
        now = open(OUT_NPZ, 'rb').read()
        if now != b:
            raise SystemExit('作り直した npz が置き場の npz とバイトで違う（止める）')
        print('[bl3_directions] --check: 作り直した npz は置き場の npz とバイトで同じ（SHA-256 %s）' % file_sha)
        return
    if os.path.exists(OUT_NPZ) and not a.force:
        raise SystemExit('既にある: %s（--force で上書き・--check で突き合わせ）' % OUT_NPZ)
    os.makedirs(os.path.dirname(OUT_NPZ), exist_ok=True)
    open(OUT_NPZ, 'wb').write(b)
    J = {'kind': 'bl3_directions', 'version': VERSION, 'npz': 'results/Bl3/directions-Bl3.npz', 'npz_sha256': file_sha, 'dtype': 'float64',
         'groups': {k: {'count': int(len(arrays[k])), 'sha256': sha[k], 'names': names[k] if k != 'iso' else {'first': names[k][0], 'last': names[k][-1], 'count': len(names[k])}} for k in GROUPS},
         'meta': meta, 'contrasts_sha16': hashlib.sha256(open(os.path.join(REPO, 'design', 'contrasts-Bl3.json'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16],
         'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    json.dump(J, open(OUT_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('[bl3_directions] wrote %s（SHA-256 %s・%d 本・%.1f MB）と %s' % (os.path.relpath(OUT_NPZ, REPO), file_sha, sum(len(arrays[k]) for k in GROUPS), len(b) / 1e6, os.path.relpath(OUT_JSON, REPO)))


def _selftest():
    rng = np.random.default_rng(1)
    arrs = collections.OrderedDict([('named', rng.normal(size=(4, 8))), ('iso', rng.normal(size=(5, 8)))])
    b1, b2 = write_npz_fixed(None, arrs), write_npz_fixed(None, arrs)
    assert b1 == b2, '同じ入力で npz のバイトが違う（時刻が入っている）'
    z = np.load(io.BytesIO(b1))
    assert list(z.files) == ['named', 'iso'] and all(np.array_equal(z[k], arrs[k]) for k in arrs) and z['iso'].dtype == np.float64
    arrs2 = collections.OrderedDict(arrs)
    arrs2['iso'] = arrs['iso'].copy()
    arrs2['iso'][0, 0] += 1e-12
    assert write_npz_fixed(None, arrs2) != b1, '値の違いが npz のバイトに出ない'
    print('[bl3_directions] 自己検査 OK（%s）: 同じ入力で同一バイト・np.load で読める・値の違いがバイトに出る' % VERSION)


if __name__ == '__main__':
    main()
