# -*- coding: utf-8 -*-
"""bprime_directions.py v1（2026-09-30・B′ の方向の抽出と帰無の方向の作り方・Gemma-4-31B-it・コーディネータ南無弥勒如来）。前の版は `prev/bprime_directions-v0.py`。

正本 `design/contrasts-Bprime.json` の `directions`・`nulls`・`coefficient` のとおり:
  - 抽出（相 extract）: 八腕 × 抽出の二場面の文脈の主位置（`<channel|>`）の、選んだ層の出力（`layers[k]` の出力をフックで取る）。選んだ層より後を流さない（層の出力を取った所で
    順伝播を打ち切り、最後の正規化の前のフックが一度も呼ばれないことを assert する・`directions.extraction.no_readout`・S26）。効き目を一つも計算しない。
  - 名前のある方向は段階 B と同じ定義（static＝h_O − h_Osec・loaded＝h_{O-Ncold} − h_{Osec-Ncold}・Nk＝h_Nk − h_N・td＝h_Onull − h_N・h は二場面の平均）で、‖static‖ に合わせる
    （凍結の `steer_B.match_to_static`）。揃える前のノルムが有限で零でないことを assert する（S19）。
  - 等方の方向は凍結の `blens_core.iso_directions`（種・層の割合・本数・`layer_key_scale`）の出力をそのまま npz に入れる。凍結の前に同じ引き方で正規化の前の乱数 g を引き
    （`iso_g`）、g と種と層の割合と次元の SHA を凍結の記録に入れる。相 extract では、凍結の関数の出力が g × ‖v̂‖ ÷ ‖g‖ と相対の差 `nulls.isotropic.g_rel_tol` の内で一致することを確かめる。
  - 実在の差の方向は凍結の `blens_core.real_differences`（八腕の全ての対・名の並びは八腕の順の i<j）。自己検査の一本は等方と同じ作り方で `nulls.self_check_direction.seed` の種。
  - 係数（`coefficient.rule`）: 層三の比 ÷（‖v̂‖ ÷ ‖h‖）。層三の比は層三の凍結の活性から出し直す（`bl3_ratio`）。確かめ二つ（`coefficient.check_bl3`・`coefficient.check_B_record`）。
  - npz は凍結の `bl3_directions.write_npz_fixed`（時刻を持たない形・再実行で同一バイト）。
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, hashlib, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bprime_gemma as G
import bprime_core as P

VERSION = 'v1'          # v1（2026-09-30）: 正本 v2 に合わせた（選んだ層より後を流さない assert・g の保存と一致・自己検査の一本・揃える前のノルムの assert・係数と二つの確かめ・帯の位置の ‖h‖）
REAL_ARMS = ['O', 'Osec', 'Onull', 'Nk', 'N', 'O-Ncold', 'Osec-Ncold', 'Onull-Ncold']
EXTRACT_SCENES = ['N1', 'S1']
NAMED = collections.OrderedDict([('static', ('O', 'Osec')), ('loaded', ('O-Ncold', 'Osec-Ncold')), ('Nk', ('Nk', 'N')), ('td', ('Onull', 'N'))])
sha_arr = lambda x: hashlib.sha256(np.ascontiguousarray(np.asarray(x, dtype=np.float64)).tobytes()).hexdigest().upper()
ToolError = P.ToolError


class _Stop(Exception):
    """選んだ層の出力を取った所で順伝播を打ち切る印（読み取りの値を作らない）。"""


def activations(model, contexts, layer_idx, positions=None):
    """文脈（名 → トークンの並び）ごとに、選んだ層の出力の主位置の値（float64）を返す（加減はしない）。positions を与えると、その位置（名 → 添字の並び）の値も返す。
    選んだ層の出力を取った所で打ち切り、最後の正規化の前のフックが呼ばれないこと（読み取りの値を作らないこと）を assert する。"""
    import torch
    dev = next(model.parameters()).device
    layer = G.decoder_layers(model)[layer_idx]
    out, norms, extra = collections.OrderedDict(), collections.OrderedDict(), collections.OrderedDict()
    for key, ids in contexts.items():
        mp = G.main_position(ids)
        cap, flag = {}, {'norm': False}

        def hook(m, a, o):
            hh = (o[0] if isinstance(o, tuple) else o)[0]
            cap['h'] = hh[mp, :].detach().double().cpu().numpy()
            if positions is not None and key in positions:
                cap['pos'] = hh[list(positions[key]), :].detach().double().cpu().numpy()
            raise _Stop()
        h = layer.register_forward_hook(hook)
        hn = G.final_norm(model).register_forward_pre_hook(lambda m, a: flag.__setitem__('norm', True))
        try:
            with torch.no_grad():
                try:
                    model(input_ids=torch.tensor([ids], device=dev), use_cache=False, logits_to_keep=1)
                except _Stop:
                    pass
        finally:
            h.remove()
            hn.remove()
        if flag['norm'] or 'h' not in cap:
            raise ToolError('抽出が選んだ層より後を流した（最後の正規化が呼ばれた）か、層の出力を取れなかった: %s' % key)
        out[key] = cap['h']
        norms[key] = float(np.linalg.norm(cap['h']))
        if 'pos' in cap:
            extra[key] = cap['pos']
    return out, norms, extra


def arm_means(acts):
    """文脈の名（`場面|腕`）から、腕ごとの抽出の二場面の平均（八腕の順）。"""
    return collections.OrderedDict((arm, np.mean([acts['%s|%s' % (sc, arm)] for sc in EXTRACT_SCENES], axis=0)) for arm in REAL_ARMS)


def _finite_nonzero(vecs, where):
    bad = [k for k, v in vecs.items() if not np.all(np.isfinite(v)) or float(np.linalg.norm(v)) == 0.0]
    if bad:
        raise ToolError('揃える前のノルムが有限でないか零（%s）: %s' % (where, bad))


def iso_g(seed, layer_ratio, count, key_scale, d):
    """正規化の前の乱数 g（凍結の `blens_core.iso_directions` と同じ引き方: SeedSequence([種, 層の割合 × key_scale])・方向ごとに正規分布を d 個）。"""
    ss = np.random.SeedSequence([int(seed), int(round(float(layer_ratio) * int(key_scale)))])
    rng = np.random.default_rng(ss)
    return np.array([rng.normal(size=int(d)) for _ in range(int(count))], dtype=np.float64)


def g_record(g, seed, layer_ratio, count, key_scale):
    return {'g_sha256': sha_arr(g), 'seed': int(seed), 'layer_ratio': float(layer_ratio), 'count': int(count), 'layer_key_scale': int(key_scale), 'dim': int(g.shape[1]),
            'numpy': np.__version__}


def check_iso_against_g(iso, g, vhat_norm, rel_tol):
    """凍結の関数の出力（iso）が、保存した g から同じ式で作った値と相対の差の内で一致するか（ビットの一致は求めない）。"""
    want = g * (float(vhat_norm) / np.linalg.norm(g, axis=1, keepdims=True))
    rel = float(np.max(np.abs(iso - want)) / max(float(np.max(np.abs(want))), 1e-300))
    return {'rel_max': rel, 'pass': bool(rel <= rel_tol)}


def build(acts, C, g=None):
    """方向の組（名前のある方向・等方・実在の差・自己検査の一本）を作る。g を与えると等方の一致を確かめる（落ちたら ToolError）。"""
    import steer_B
    import blens_core as CB
    M = arm_means(acts)
    raw_named = collections.OrderedDict((k, M[a] - M[b]) for k, (a, b) in NAMED.items())
    _finite_nonzero(raw_named, '名前のある方向')
    static = raw_named['static']
    nv = float(np.linalg.norm(static))
    named = collections.OrderedDict((k, steer_B.match_to_static(v, static)) for k, v in raw_named.items())
    ratio = float(C['layers']['ratio'])
    ks = int(C['nulls']['isotropic']['layer_key_scale'])
    iso = np.asarray(CB.iso_directions(static, int(C['nulls']['isotropic']['seed']), ratio, int(C['nulls']['isotropic']['count']), ks), dtype=np.float64)
    if iso.shape[1] != static.shape[0]:
        raise ToolError('等方の方向の次元が抽出した活性の次元と違う（R23）')
    iso_check = None
    if g is not None:
        iso_check = check_iso_against_g(iso, g, nv, C['nulls']['isotropic']['g_rel_tol'])
        if not iso_check['pass']:
            raise ToolError('等方の方向が保存した g と一致しない（相対の差 %.3g）' % iso_check['rel_max'])
    raw_real = collections.OrderedDict()
    names = list(M)
    import itertools
    for i, j in itertools.combinations(range(len(names)), 2):
        raw_real['%s~%s' % (names[i], names[j])] = M[names[i]] - M[names[j]]
    _finite_nonzero(raw_real, '実在の差の方向')
    real = CB.real_differences(M, nv)
    if list(real) != list(raw_real):
        raise ToolError('実在の差の名の並びが凍結の関数と違う')
    check = np.asarray(CB.iso_directions(static, int(C['nulls']['self_check_direction']['seed']), ratio, 1, ks), dtype=np.float64)
    arrays = collections.OrderedDict([('named', np.array(list(named.values()), dtype=np.float64)), ('iso', iso), ('real', np.array(list(real.values()), dtype=np.float64)), ('check', check)])
    names_ = collections.OrderedDict([('named', list(named)), ('iso', ['iso:%d' % i for i in range(len(iso))]), ('real', list(real)), ('check', ['check'])])
    un = lambda v: v / np.linalg.norm(v)
    cos_check = float(max(abs(float(un(check[0]) @ un(x))) for x in list(iso) + list(real.values())))
    meta = {'version': VERSION, 'layer_ratio': ratio, 'dim': int(static.shape[0]), 'vhat_norm': nv, 'iso_seed': int(C['nulls']['isotropic']['seed']), 'iso_count': int(len(iso)),
            'layer_key_scale': ks, 'check_seed': int(C['nulls']['self_check_direction']['seed']), 'check_cos_max': cos_check, 'iso_check': iso_check,
            'natural_norms_real': {k: float(np.linalg.norm(v)) for k, v in raw_real.items()}, 'natural_norms_named': {k: float(np.linalg.norm(v)) for k, v in raw_named.items()},
            'sha256': {k: sha_arr(v) for k, v in arrays.items()}}
    return arrays, names_, meta


def h_norm_mean(norms):
    """‖h‖ の平均（抽出の文脈の主位置・段階 B の `direction_B.h_norm_record` と同じ定義・R13）。"""
    return float(np.mean(list(norms.values())))


def bl3_ratio(npz_path, ratio_key='0.5'):
    """層三の比（正本 `coefficient.bl3_ratio`）: 層三の凍結の活性（`same_order`・八腕 × 二場面）から ‖h‖ の平均と ‖v̂‖ を出し直し、`coef_applied` × ‖v̂‖ ÷ ‖h‖。"""
    Z = np.load(npz_path)
    acts = collections.OrderedDict(('%s|%s' % (sc, arm), np.asarray(Z['same_order__%s__%s__%s' % (arm, sc, ratio_key)], dtype=np.float64)) for arm in REAL_ARMS for sc in EXTRACT_SCENES)
    norms = collections.OrderedDict((k, float(np.linalg.norm(v))) for k, v in acts.items())
    M = arm_means(acts)
    vhat = float(np.linalg.norm(M['O'] - M['Osec']))
    hm = h_norm_mean(norms)
    return {'h_norm_mean': hm, 'vhat_norm': vhat, 'vhat_over_h': vhat / hm, 'acts': acts, 'norms': norms}


def coefficient(bl3_ratio_value, vhat_norm, h_mean):
    """係数＝層三の比 ÷（‖v̂‖ ÷ ‖h‖）（上下の限りを置かない・R13）。"""
    if not (np.isfinite(vhat_norm) and np.isfinite(h_mean) and vhat_norm > 0 and h_mean > 0):
        raise ToolError('係数の分母が有限の正の値でない')
    return float(bl3_ratio_value / (vhat_norm / h_mean))


def coefficient_checks(npz_path, C):
    """係数の二つの確かめ（`coefficient.check_bl3`・`coefficient.check_B_record`）。戻り値: 値と合否（落ちたら ToolError）。"""
    r = bl3_ratio(npz_path)
    coef_applied = float(C['coefficient']['bl3_coef_applied'])
    ratio = coef_applied * r['vhat_over_h']
    coef = coefficient(ratio, r['vhat_norm'], r['h_norm_mean'])
    tol = float(C['coefficient']['check_bl3']['rel_tol'])
    ok1 = abs(coef - coef_applied) / coef_applied <= tol
    rec = C['coefficient']['check_B_record']
    d_h = abs(r['h_norm_mean'] - rec['h_norm_main']) / rec['h_norm_main']
    d_v = abs(r['vhat_norm'] - rec['vhat_norm']) / rec['vhat_norm']
    ok2 = d_h <= tol and d_v <= tol
    out = {'bl3_ratio': ratio, 'coef_on_bl3': coef, 'check_bl3_pass': bool(ok1), 'h_norm_mean': r['h_norm_mean'], 'vhat_norm': r['vhat_norm'], 'rel_h': d_h, 'rel_v': d_v, 'check_B_record_pass': bool(ok2)}
    if not (ok1 and ok2):
        raise ToolError('係数の確かめが落ちた: %s' % out)
    return out


def npz_bytes(arrays):
    import bl3_directions as BD
    return BD.write_npz_fixed(None, arrays)


def _selftest():
    """模型を読まない確かめ（numpy だけ・合成の活性）: g の引き方が凍結の関数と同じ・一致の確かめ・揃える前のノルムの assert・係数の式と二つの確かめ（層三の実の活性で）。"""
    import json
    import blens_core as CB
    C = json.load(open(os.path.join(os.path.dirname(HERE), 'design', 'contrasts-Bprime.json'), encoding='utf-8'))
    rng = np.random.default_rng(7)
    d = 48
    acts = collections.OrderedDict(('%s|%s' % (sc, arm), rng.standard_normal(d) * 3.0) for arm in REAL_ARMS for sc in EXTRACT_SCENES)
    Cs = json.loads(json.dumps(C))
    Cs['nulls']['isotropic']['count'] = 25
    g = iso_g(Cs['nulls']['isotropic']['seed'], Cs['layers']['ratio'], 25, Cs['nulls']['isotropic']['layer_key_scale'], d)
    arrays, names, meta = build(acts, Cs, g=g)
    assert meta['iso_check']['pass'] and meta['iso_check']['rel_max'] < 1e-14, meta['iso_check']
    assert arrays['iso'].shape == (25, d) and arrays['real'].shape == (28, d) and arrays['named'].shape == (4, d) and arrays['check'].shape == (1, d)
    assert np.allclose(np.linalg.norm(arrays['iso'], axis=1), meta['vhat_norm']) and np.allclose(np.linalg.norm(arrays['check']), meta['vhat_norm'])
    g_bad = g.copy(); g_bad[0, 0] += 1.0
    try:
        build(acts, Cs, g=g_bad); raise AssertionError('g の違いで止まらない')
    except ToolError:
        pass
    acts0 = dict(acts); acts0['N1|Osec'] = acts['N1|O']; acts0['S1|Osec'] = acts['S1|O']
    try:
        build(collections.OrderedDict(acts0), Cs); raise AssertionError('零のノルムで止まらない')
    except ToolError:
        pass
    PUB = os.environ.get('OP4B_PUBLIC_REPO', 'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b')
    cc = coefficient_checks(os.path.join(PUB, 'results', 'dirB', 'dirB__s1', 'main_position_activations.npz'), C)
    assert cc['check_bl3_pass'] and cc['check_B_record_pass']
    b1, b2 = npz_bytes(arrays), npz_bytes(arrays)
    assert b1 == b2
    print('bprime_directions.py %s SELFTEST PASS（g の一致 %.2g・係数の確かめ 層三の活性で %.9f・‖h‖ の相対の差 %.2g・‖v̂‖ の相対の差 %.2g）' % (VERSION, meta['iso_check']['rel_max'], cc['coef_on_bl3'], cc['rel_h'], cc['rel_v']))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _selftest(); sys.exit(0)
    print(__doc__)
