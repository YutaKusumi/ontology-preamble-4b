# -*- coding: utf-8 -*-
"""blens_lens.py v2 —— B-lens の層一（凍結した方向の直接の経路を語彙に射影し、凍結した語の集合で読む・2026-09-23・正本 §3・裁定 D163・D165・D171・D173・D179）。

計算（正本の規則のとおり・芯は `tools/blens_core.py`）:
  - Δℓ(u)＝W_E·(g⊙u) を含める語彙の平均で中心化（物差しは係数のベクトル a で M(u) = a·u）。重みは bf16 を float32 に上げ、語彙の行の平均は float64 で足して float32 に戻す。
  - 方向: 名前のある四つ（static＝v̂・loaded＝(6b)・Nk・td）× 三つの層・段階 B のランダム方向（本走行は選んだ層の三本・調整走行は層ごとの三本・凍結の関数 `steer_B.random_directions` で再生）。
  - 帰無は三つ: 等方（層ごとに千本・種 81001・写した器）・実在の差（凍結の八腕の活性の全ての対・ノルムを揃える）・語の側（v̂ の M_E だけ・層を揃えた語の集合の抽選）。
  - 主の記述の札: v̂・選んだ層・六つの物差しに、等方の外（Holm・段の数 6・p < 段）と二つ目の札（M_L・M_X・M_F は兄弟を除いた実在の差の中で最上位・M_E は語の側の帰無の外）。
  - 記述: 全ての方向 × 層 × 物差し（感度の変種を含む）の値・等方の割合・実在の差の中の順位、八腕の値と対の距離、語の一覧（上位と下位の 50 語・集合の印・数える記述）、
    封印の後の記述（‖g⊙u‖／‖u‖・上位の次元の割合・狙いの度合い・上位の次元を零にした感度・一覧の語のノルムの偏り）。
自己検査（外れたら止める・登録者に相談・裁定 D184）:
  - 等方の帰無の標準偏差を解析の値と突き合わせる（相対の差 `nulls.isotropic.analytic_tol` の内）。
  - 写した等方の器が、段階 B の種で凍結の関数とビットで一致する。段階 B のランダム方向を手元で再生した方向が、Colab の起動器が B の版の NumPy で再生して置いた方向と、
    方向ごとの相対の差 `nulls.B_random.repro_tol` の内で一致する（`compare_random_dirs`・両方の SHA-256 を記録に並べる・合わなければ層一の計算に進まない・裁定 D187）。
  - 活性から作り直した方向が凍結の npz と一致する・凍結の語の集合と正本の SHA が凍結の記録と一致する。
封印の前には走らない: 凍結の記録と封印の記録（両方の予想の JSON の SHA-256）が無ければ止まる（正本 `predictions.order`「封印は射影を一つも計算する前」）。
出力: results/Blens/lens-Blens.json（--force が無ければ上書きしない）。
用法: python tools/blens_lens.py --colab-check <Colab の確かめの JSON> --colab-dirs <同じ確かめの方向の npz> [--force] ／ --selftest（合成の小さな入力で計算の経路を回す）
v2（2026-09-24・裁定 D187）: Colab の再生との突き合わせを、SHA-256 のビットの一致から、方向ごとの相対の差の許容に改めた（一度目の凍結の前の Colab の確かめで、
  方向の大きさを揃えるノルムの計算の最後の桁が機械の違いで変わり、SHA-256 が合わなかった）。層一は手元で再生した方向で計算する（前と同じ）。
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, math, hashlib, argparse, datetime, unicodedata, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C

VERSION = 'v2'
NL = chr(10)
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
ACT = os.path.expanduser('~/.cache/op4b-dir/dirB__s1/main_position_activations.npz')
SETS = os.path.join(REPO, 'records', 'Blens', 'sets-Blens.json')
FREEZE = os.path.join(REPO, 'records', 'Blens', 'FREEZE-RECORD-Blens.json')
SEAL = os.path.join(REPO, 'records', 'Blens', 'sealing-record-Blens.json')
OUT = os.path.join(REPO, 'results', 'Blens', 'lens-Blens.json')
NAMED = ('static', 'loaded', 'Nk', 'td')
OWN_E = {'static': 'static', 'loaded': 'static', 'Nk': 'Nk', 'td': 'td'}
OWN_PAIR = {'static': 'O~Osec', 'loaded': 'O-Ncold~Osec-Ncold', 'Nk': 'Nk~N', 'td': 'Onull~N'}
sha256f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()
sha16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
rkey = lambda r: ('%g' % float(r))


def dirs_sha256(vecs):
    """方向の並びの SHA-256（float64 に上げたバイト列を順に連ねる）。Colab の起動器と同じ式。"""
    h = hashlib.sha256()
    for v in vecs:
        h.update(np.asarray(v, dtype=np.float64).tobytes())
    return h.hexdigest().upper()


def compare_random_dirs(local, colab, tol):
    """段階 B のランダム方向の、手元の再生と Colab の再生の突き合わせ（裁定 D187・正本 `nulls.B_random.repro_check`）。
    local・colab は {'main@0.5': 方向の並び, ...}。方向ごとの相対の差＝要素ごとの差の絶対値の最大 ÷ 手元の方向の要素の絶対値の最大。
    鍵・方向の数・次元が違うか、相対の差が tol を超える（または有限でない）方向が一つでもあれば ok は False。両方の SHA-256・相対の差・ビットの一致を返す。"""
    out = {'tol': tol, 'ok': True, 'problems': [], 'keys': {}}
    if sorted(local) != sorted(colab):
        out['ok'] = False
        out['problems'].append('鍵が違う（手元 %s・Colab %s）' % (sorted(local), sorted(colab)))
    for k in sorted(set(local) & set(colab)):
        lv, cv = np.asarray(local[k], dtype=np.float64), np.asarray(colab[k], dtype=np.float64)
        row = {'sha256_local': dirs_sha256(lv), 'sha256_colab': dirs_sha256(cv), 'shape_local': list(lv.shape), 'shape_colab': list(cv.shape), 'rel_max': None}
        if lv.ndim != 2 or lv.shape != cv.shape:
            out['ok'] = False
            out['problems'].append('%s: 方向の数か次元が違う' % k)
        else:
            with np.errstate(divide='ignore', invalid='ignore'):
                rel = [float(np.max(np.abs(c - l)) / np.max(np.abs(l))) for l, c in zip(lv, cv)]
            row.update({'rel_per_direction': rel, 'rel_max': max(rel), 'bitwise_equal': bool(np.array_equal(lv, cv))})
            if not all(math.isfinite(x) for x in rel) or max(rel) > tol:
                out['ok'] = False
                out['problems'].append('%s: 相対の差の最大 %.3g が許容 %g の外' % (k, max(rel), tol))
        out['keys'][k] = row
    fin = [r['rel_max'] for r in out['keys'].values() if r['rel_max'] is not None]
    out['rel_max'] = max(fin) if fin else None
    return out


def load_colab_dirs(npz_path, CC):
    """Colab の起動器が置いた方向の npz を読む（ファイルの SHA-256 が確かめの JSON の記録と同じことと、JSON の SHA-256 の欄と方向が同じことを先に確かめる）。"""
    want = (CC.get('random_dirs_npz') or {}).get('sha256')
    if not want or sha256f(npz_path) != want:
        raise SystemExit('方向の npz の SHA-256 が Colab の確かめの JSON の記録と違う（組み合わせが違う・止める）: %s' % npz_path)
    Z = np.load(npz_path)
    out = {k: Z[k] for k in Z.files}
    if any((CC.get('random_dirs_sha256') or {}).get(k) != dirs_sha256(v) for k, v in out.items()) or sorted(out) != sorted(CC.get('random_dirs_sha256') or {}):
        raise SystemExit('方向の npz と、確かめの JSON の SHA-256 の欄が食い違う（止める）')
    return out


def primary_metric_names(TL):
    """主の六つの物差しの、正本の名 → 係数の表の名。"""
    out = collections.OrderedDict()
    for m in TL['primary']['metrics']:
        out[m] = {'M_E': 'M_E_static', 'M_F': 'M_F'}.get(m, m)
    return out


def comparators(kind, pairs, TL):
    if kind in ('static', 'loaded'):
        return [p for p in pairs if p not in TL['nulls']['real']['swap_siblings']]
    if kind in OWN_PAIR:
        return [p for p in pairs if p != OWN_PAIR[kind]]
    return list(pairs)


def metric_of(kind, name):
    """物差しの表の名のうち、方向の種類に効くもの（M_E はその方向の E）。"""
    if name.startswith('M_E_'):
        base = name.split(':')[0]
        return base == 'M_E_' + OWN_E.get(kind, 'static')
    return True


def token_kind(s):
    if '�' in s:
        return 'fragment'
    if s and all(ord(ch) < 128 for ch in s):
        return 'ascii'
    if s and not any(unicodedata.category(ch)[0] in 'LN' for ch in s):
        return 'symbol'
    return 'word'


def layer1(TL, SJ, rows_of, mu_W, g, dirs, arm_means, b_rand, delta_full, decode, vocab_norms, base_vocab):
    """層一の計算（読み込みをしない・合成データでも回る）。

    dirs: 種類 → 層の割合の文字 → 方向・arm_means: 層 → 腕 → 平均の活性・b_rand: {'main': {層: [方向]}, 'tune': {層: [方向]}}・
    delta_full(U) → 含める語彙の Δℓ（行×本数・中心化の前）・decode(i) → 字・vocab_norms: 含める語彙の ‖g⊙W_E[t]‖。"""
    sets, WS = SJ['sets'], SJ['word_side']
    fams = list(TL['metrics']['families'])
    table = C.metric_table(sets, fams, TL['metrics']['letters'])
    A = C.coef_vectors(table, rows_of, mu_W, g)
    ratios = [rkey(r) for r in TL['layers']['ratios']]
    sel = rkey(TL['primary']['ratio'])
    d = int(len(mu_W))
    ISO = TL['nulls']['isotropic']
    out = {'layers': collections.OrderedDict(), 'metric_names': list(A), 'checks': {}}
    iso_vals = {}
    for r in ratios:
        vs = np.asarray(dirs['static'][r], dtype=np.float32)
        target = float(np.linalg.norm(vs))
        U_iso = C.iso_directions(vs, ISO['seed'], float(r), ISO['count'], ISO['layer_key_scale'])
        iv = C.values(A, U_iso)
        iso_vals[r] = iv
        sd = collections.OrderedDict()
        for m, a in A.items():
            s_, an = float(np.std(iv[m])), C.analytic_sd(a, target, d)
            sd[m] = {'sampled': s_, 'analytic': an, 'rel': abs(s_ - an) / an if an else 0.0}
        bad = {m: x['rel'] for m, x in sd.items() if x['rel'] > ISO['analytic_tol']}
        if bad:
            raise SystemExit('等方の帰無の標準偏差が解析の値から外れた（止める・登録者に相談）: 層 %s %s' % (r, bad))
        # 実在の差
        rd = C.real_differences(arm_means[r], target)
        pairs = list(rd)
        rv = C.values(A, np.array([rd[p] for p in pairs]))
        real = {p: {m: float(rv[m][k]) for m in A} for k, p in enumerate(pairs)}
        names_arm = list(arm_means[r])
        av = C.values(A, np.array([arm_means[r][arm] for arm in names_arm]))
        arm_vals = {arm: {m: float(av[m][k]) for m in A} for k, arm in enumerate(names_arm)}
        names = list(arm_means[r])
        pdist = {'%s~%s' % (names[i], names[j]): float(np.linalg.norm(np.asarray(arm_means[r][names[i]], dtype=np.float64) - np.asarray(arm_means[r][names[j]], dtype=np.float64)))
                 for i in range(len(names)) for j in range(i + 1, len(names))}
        # 方向
        D = collections.OrderedDict((k, np.asarray(dirs[k][r], dtype=np.float32)) for k in NAMED)
        for i, v in enumerate(b_rand['tune'].get(r, [])):
            D['tune_rand:%d' % i] = np.asarray(v, dtype=np.float32)
        if r == sel:
            for i, v in enumerate(b_rand['main'][r]):
                D['rand:%d' % i] = np.asarray(v, dtype=np.float32)
        dv = C.values(A, np.array(list(D.values())))
        dres = collections.OrderedDict()
        for k, name in enumerate(D):
            kind = name if name in NAMED else 'rand'
            comp = comparators(kind, pairs, TL)
            row = collections.OrderedDict()
            for m in A:
                val = float(dv[m][k])
                row[m] = {'value': val, 'p_iso': C.p_two_sided(val, iv[m]), 'real_rank': C.top_rank(val, [real[p][m] for p in comp]), 'own': metric_of(kind, m)}
            dres[name] = row
        siblings = {k: {p: real[p] for p in TL['nulls']['real']['swap_siblings'] if p != OWN_PAIR[k]} for k in ('static', 'loaded')}
        out['layers'][r] = {'directions': dres, 'iso_sd': sd, 'iso_summary': {m: {'mean': float(np.mean(iv[m])), 'sd': float(np.std(iv[m]))} for m in A},
                            'real': real, 'arm_values': arm_vals, 'pair_distance': pdist, 'siblings': siblings, 'target_norm': target}
    # 主の記述の札
    PM = primary_metric_names(TL)
    pv = out['layers'][sel]['directions']['static']
    iso_p = {m: pv[t]['p_iso'] for m, t in PM.items()}
    H = C.holm(iso_p, TL['primary']['alpha'], TL['primary']['holm_m'])
    # 語の側の帰無（v̂・選んだ層）
    u_sel = np.asarray(dirs['static'][sel], dtype=np.float32)
    delta_v = delta_full(u_sel[None, :])[:, 0].astype(np.float64)
    cells = {int(k): tuple(v) for k, v in WS['cells'].items()}
    cell_of = lambda t: cells[int(t)]
    Es = sets['E']['static']

    def groups(strata):
        return collections.OrderedDict((tuple(k.split('|')), [(tuple(g_[0]), g_[1], g_[2]) for g_ in gl]) for k, gl in strata.items())

    ws_null = C.word_side_draws(delta_v, Es['plus'], Es['minus'], cell_of, WS['pool'], groups(WS['strata']), TL['nulls']['word_side']['draws'], TL['nulls']['word_side']['seed'])
    m_E = float(delta_v[Es['plus']].mean() - delta_v[Es['minus']].mean())
    ws_p = C.p_equal_tailed(m_E, ws_null)
    sens_null = C.word_side_draws(delta_v, Es['plus'], Es['minus'], cell_of, WS['sens_pool'], groups(WS['sens_strata']), TL['nulls']['word_side']['draws'], TL['nulls']['word_side']['seed']) if WS.get('sens_ok') else None
    out['word_side'] = {'m': m_E, 'p': ws_p, 'outside': ws_p < TL['nulls']['word_side']['alpha'], 'null_mean': float(ws_null.mean()), 'null_median': float(np.median(ws_null)),
                        'null_sd': float(ws_null.std()), 'draws': int(len(ws_null)),
                        'sens': None if sens_null is None else {'p': C.p_equal_tailed(m_E, sens_null), 'null_mean': float(sens_null.mean()), 'null_median': float(np.median(sens_null)), 'null_sd': float(sens_null.std())}}
    if abs(m_E - pv['M_E_static']['value']) > 1e-3 * max(1.0, abs(m_E)):
        raise SystemExit('語の側の帰無の M_E が係数のベクトルの値と合わない（止める）: %s %s' % (m_E, pv['M_E_static']['value']))
    prim = collections.OrderedDict()
    for m, t in PM.items():
        iso_lab = bool(H[m]['pass'])
        if m == 'M_E':
            second, detail = bool(out['word_side']['outside']), {'word_side_p': ws_p}
        else:
            rr = pv[t]['real_rank']
            second, detail = bool(rr['top']), rr
        prim[m] = {'table_name': t, 'value': pv[t]['value'], 'p_iso': pv[t]['p_iso'], 'holm_step': H[m]['step'], 'iso_outside': iso_lab, 'second': second, 'second_detail': detail}
    out['primary'] = {'direction': 'static', 'ratio': sel, 'metrics': prim, 'chance_one_label': TL['nulls']['real']['chance_one_label']}
    # 語の一覧と封印の後の記述（名前のある方向 × 層）
    K = TL['projection']['top_k']
    marks = collections.OrderedDict()
    for x, t in sets['L'].items():
        marks.setdefault(int(t), []).append('L_' + x)
    for k in ('static', 'td', 'Nk'):
        for side in ('plus', 'minus'):
            for t in sets['E'][k][side]:
                marks.setdefault(int(t), []).append('E_%s_%s' % (k, side))
    for f_, x in sets['X'].items():
        for side in ('a', 'others'):
            for t in x[side]:
                marks.setdefault(int(t), []).append('X_%s_%s' % (f_, side))
    marks.setdefault(int(sets['F']['main']), []).append('F_main')
    for t in sets['F']['sens']:
        marks.setdefault(int(t), []).append('F_sens')
    pool = set(WS['pool'])
    TD = TL['descriptive_after_seal']['top_dims']
    vn_rank = np.argsort(np.argsort(vocab_norms, kind='mergesort'), kind='mergesort') / max(1, len(vocab_norms) - 1)
    lists, desc = collections.OrderedDict(), collections.OrderedDict()
    for r in ratios:
        U = np.array([np.asarray(dirs[k][r], dtype=np.float32) for k in NAMED])
        DL = delta_full(U).astype(np.float64)
        for j, k in enumerate(NAMED):
            dl = DL[:, j] - DL[:, j].mean()
            order = np.argsort(-dl, kind='mergesort')
            top, bot = order[:K], order[::-1][:K]
            show = lambda idx: [{'id': int(i), 's': decode(int(i)), 'v': float(dl[i]), 'marks': marks.get(int(i), []) + (['pool'] if int(i) in pool else [])} for i in idx]
            cnt = lambda idx: dict(collections.Counter(m for i in idx for m in marks.get(int(i), [])))
            kinds = lambda idx: dict(collections.Counter(token_kind(decode(int(i))) for i in idx))
            lists['%s@%s' % (k, r)] = {'top': show(top), 'bottom': show(bot), 'top_counts': cnt(top), 'bottom_counts': cnt(bot), 'top_kinds': kinds(top), 'bottom_kinds': kinds(bot)}
            u = U[j].astype(np.float64)
            gu = np.asarray(g, dtype=np.float64) * u
            c2 = gu * gu
            topd = np.argsort(-c2, kind='mergesort')[:TD]
            uz = u.copy()
            uz[topd] = 0.0
            zv = C.values(A, uz[None, :])
            sdv = float(dl.std())
            own = {m: out['layers'][r]['directions'][k][m]['value'] for m in A}
            desc['%s@%s' % (k, r)] = {'gu_over_u': float(np.linalg.norm(gu) / np.linalg.norm(u)), 'top_dims_share': float(c2[topd].sum() / c2.sum()), 'top_dims': [int(x) for x in topd],
                                      'targeting': {m: (own[m] / sdv if sdv else None) for m in A}, 'zeroed': {m: float(np.asarray(zv[m]).ravel()[0]) for m in A},
                                      'list_norm_pct': {'top': float(vn_rank[top].mean()), 'bottom': float(vn_rank[bot].mean())}}
        # 帰無の ‖g⊙u‖／‖u‖（等方は解析で決まらないので、層の等方の方向の平均）
        vs = np.asarray(dirs['static'][r], dtype=np.float32)
        U_iso = C.iso_directions(vs, ISO['seed'], float(r), ISO['count'], ISO['layer_key_scale'])
        gi = np.linalg.norm(U_iso * np.asarray(g, dtype=np.float64)[None, :], axis=1) / np.linalg.norm(U_iso, axis=1)
        desc['iso@%s' % r] = {'gu_over_u_mean': float(gi.mean()), 'gu_over_u_sd': float(gi.std())}
    out['lists'], out['descriptive_after_seal'] = lists, desc
    return out


# ---------------- 実データの読み込み ----------------
class Weights:
    """手元の重み（safetensors）を行ごとに読む。語彙の行列は大きいので、塊ごとに流す。"""
    def __init__(self, snap, base_vocab):
        from safetensors import safe_open
        self.snap, self.base = snap, base_vocab
        self.idx = json.load(open(os.path.join(snap, 'model.safetensors.index.json'), encoding='utf-8'))
        with safe_open(os.path.join(snap, self.idx['weight_map']['model.norm.weight']), framework='pt') as fh:
            self.g = fh.get_tensor('model.norm.weight').float().numpy()
        self.path = os.path.join(snap, self.idx['weight_map']['model.embed_tokens.weight'])
        self.step = 1 << 13
        s = np.zeros(self.g.shape[0], dtype=np.float64)
        for blk in self.blocks():
            s += blk[1].astype(np.float64).sum(axis=0)
        self.mu = (s / base_vocab).astype(np.float32)

    def blocks(self):
        from safetensors import safe_open
        with safe_open(self.path, framework='pt') as fh:
            sl = fh.get_slice('model.embed_tokens.weight')
            for s0 in range(0, self.base, self.step):
                s1 = min(self.base, s0 + self.step)
                yield s0, sl[s0:s1].float().numpy()

    def rows_of(self, ids):
        from safetensors import safe_open
        with safe_open(self.path, framework='pt') as fh:
            sl = fh.get_slice('model.embed_tokens.weight')
            return [sl[int(i):int(i) + 1].float().numpy()[0] for i in ids]

    def delta_full(self, U):
        GU = (np.asarray(U, dtype=np.float32) * self.g[None, :]).T
        out = np.zeros((self.base, GU.shape[1]), dtype=np.float32)
        for s0, blk in self.blocks():
            out[s0:s0 + blk.shape[0]] = blk @ GU
        return out

    def norms(self):
        out = np.zeros(self.base, dtype=np.float32)
        for s0, blk in self.blocks():
            out[s0:s0 + blk.shape[0]] = np.linalg.norm(blk * self.g[None, :], axis=1)
        return out


def require_sealed(TL):
    """封印の前には走らない（凍結の記録と封印の記録と、両方の予想の JSON の SHA-256 がそろうこと）。"""
    if not os.path.exists(FREEZE):
        raise SystemExit('凍結の記録が無い（凍結の前には射影を計算しない）: %s' % FREEZE)
    if not os.path.exists(SEAL):
        raise SystemExit('封印の記録が無い（封印の前には射影を計算しない・正本 predictions.order）: %s' % SEAL)
    FR, SR = json.load(open(FREEZE, encoding='utf-8')), json.load(open(SEAL, encoding='utf-8'))
    for role in ('coordinator', 'registrant'):
        p = os.path.join(REPO, *SR['predictions'][role]['path'].split('/'))
        if not os.path.exists(p) or sha256f(p) != SR['predictions'][role]['sha256']:
            raise SystemExit('封印した予想の JSON が無いか、SHA-256 が封印の記録と違う: %s' % role)
    for rel_, want in FR['frozen_sha16'].items():
        p = os.path.join(REPO, *rel_.split('/'))
        if rel_ in ('design/contrasts-Blens.json', 'records/Blens/sets-Blens.json', 'tools/blens_core.py', 'tools/blens_lens.py') and sha16f(p) != want:
            raise SystemExit('凍結物が凍結の記録と違う（凍結の後の変更は逸脱）: %s' % rel_)
    return FR, SR


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--colab-check', help='Colab の起動器の確かめの JSON（B の版の NumPy で再生したランダム方向の SHA-256 と、方向の npz の SHA-256 を含む）')
    ap.add_argument('--colab-dirs', help='同じ確かめで起動器が置いた方向の npz（裁定 D187）')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    FR, SR = require_sealed(TL)
    if os.path.exists(OUT) and not a.force:
        raise SystemExit('既にある: %s' % OUT)
    import steer_B
    SJ = json.load(open(SETS, encoding='utf-8'))
    D = np.load(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz'))
    if sha16f(os.path.join(REPO, 'results', 'dirB', 'dirB__s1', 'directions.npz')) != TL['inputs']['files']['directions']['sha16']:
        raise SystemExit('凍結の方向の npz の SHA16 が正本と違う')
    if sha256f(ACT)[:16] != TL['inputs']['activations']['sha256_head16']:
        raise SystemExit('八腕の活性の SHA-256 が正本と違う')
    Z = np.load(ACT)
    ratios = [rkey(r) for r in TL['layers']['ratios']]
    dirs = {k: {r: D['%s__%s' % (k, r)] for r in ratios} for k in NAMED}
    arms, scenes = TL['inputs']['activations']['arms'], TL['inputs']['activations']['scenes']
    arm_means = {r: collections.OrderedDict((arm, np.mean([Z['same_order__%s__%s__%s' % (arm, sc, r)].astype(np.float64) for sc in scenes], axis=0)) for arm in arms) for r in ratios}
    # 活性から作り直した方向が凍結の npz と一致する
    for r in ratios:
        vs = arm_means[r]['O'] - arm_means[r]['Osec']
        for k, (p_, q_) in {'static': ('O', 'Osec'), 'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}.items():
            u = arm_means[r][p_] - arm_means[r][q_]
            if k != 'static':
                u = u * (np.linalg.norm(vs) / np.linalg.norm(u))
            ref = dirs[k][r].astype(np.float64)
            if np.max(np.abs(u - ref)) / np.linalg.norm(ref) > 1e-6:
                raise SystemExit('活性から作り直した方向が凍結の npz と違う（止める）: %s %s' % (k, r))
    # 段階 B のランダム方向（凍結の関数で再生）と、写した器のビットの一致・Colab の B の版の NumPy の再生との許容の内の一致（裁定 D187）
    sel = rkey(TL['primary']['ratio'])
    b_rand = {'main': {sel: steer_B.random_directions(dirs['static'][sel], 'main', float(sel))}, 'tune': {r: steer_B.random_directions(dirs['static'][r], 'tune', float(r)) for r in ratios}}
    BRn = TL['nulls']['B_random']
    for phase, seed in (('main', BRn['main_seed']), ('tune', BRn['tune_seed'])):
        for r, vs_ in b_rand[phase].items():
            mine = C.iso_directions(dirs['static'][r], seed, float(r), BRn['count'], TL['nulls']['isotropic']['layer_key_scale'])
            if not np.array_equal(mine, np.array(vs_)):
                raise SystemExit('写した器が凍結の関数の再生とビットで一致しない（止める）: %s %s' % (phase, r))
    local_sha = {'%s@%s' % (ph, r): dirs_sha256(v) for ph in b_rand for r, v in b_rand[ph].items()}
    if not (a.colab_check and a.colab_dirs):
        raise SystemExit('Colab の起動器の確かめの JSON と方向の npz が要る（B の版の NumPy で再生したランダム方向と突き合わせる・--colab-check・--colab-dirs・裁定 D187）')
    CC = json.load(open(a.colab_check, encoding='utf-8'))
    cmp_ = compare_random_dirs({'%s@%s' % (ph, r): v for ph in b_rand for r, v in b_rand[ph].items()}, load_colab_dirs(a.colab_dirs, CC), TL['nulls']['B_random']['repro_tol'])
    if not cmp_['ok']:
        raise SystemExit('Colab の B の版の NumPy で再生したランダム方向が、手元の再生と許容の内で一致しない（層一の計算に進まない・止める）: %s' % cmp_['problems'])
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(SNAP)
    base_vocab = TL['inputs']['model']['base_vocab']
    W = Weights(SNAP, base_vocab)
    dec_cache = {}

    def decode(i):
        if i not in dec_cache:
            dec_cache[i] = tok.decode([int(i)])
        return dec_cache[i]
    res = layer1(TL, SJ, W.rows_of, W.mu, W.g, dirs, arm_means, b_rand, W.delta_full, decode, W.norms(), base_vocab)
    res.update({'kind': 'blens_lens', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
                'inputs': {'contrasts_sha16': sha16f(os.path.join(REPO, 'design', 'contrasts-Blens.json')), 'sets_sha16': sha16f(SETS),
                           'freeze_record_sha16': sha16f(FREEZE), 'sealing_record_sha16': sha16f(SEAL), 'colab_check_sha16': sha16f(a.colab_check),
                           'colab_dirs_sha256': sha256f(a.colab_dirs)},
                'checks': {'iso_analytic': 'ok', 'directions_rebuilt': 'ok', 'random_copy_bits': 'ok', 'random_dirs_sha256': local_sha,
                           'random_colab_numpy': {'ok': True, 'tol': cmp_['tol'], 'rel_max': cmp_['rel_max'],
                                                  'keys': {k: {x: r[x] for x in ('sha256_local', 'sha256_colab', 'rel_max', 'bitwise_equal')} for k, r in cmp_['keys'].items()}}},
                'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    print('wrote', os.path.relpath(OUT, REPO))


def synth_bundle(seed=3, d=48, V=400):
    """合成の小さな入力（自己検査と合成データの器が使う）。"""
    rng = np.random.default_rng(seed)
    Wm = rng.normal(size=(V, d)).astype(np.float32)
    g = rng.uniform(0.5, 1.5, size=d).astype(np.float32)
    mu = Wm.mean(axis=0).astype(np.float32)
    ratios = ['0.25', '0.5', '0.75']
    arms = ['O', 'Osec', 'Onull', 'Nk', 'N', 'O-Ncold', 'Osec-Ncold', 'Onull-Ncold']
    arm_means = {r: collections.OrderedDict((a, rng.normal(size=d) * 3) for a in arms) for r in ratios}
    dirs = {}
    for r in ratios:
        vs = arm_means[r]['O'] - arm_means[r]['Osec']
        dirs.setdefault('static', {})[r] = vs.astype(np.float32)
        for k, (p_, q_) in {'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}.items():
            u = arm_means[r][p_] - arm_means[r][q_]
            dirs.setdefault(k, {})[r] = (u * np.linalg.norm(vs) / np.linalg.norm(u)).astype(np.float32)
    b_rand = {'main': {'0.5': list(C.iso_directions(dirs['static']['0.5'], 71002, 0.5, 3, 1000))}, 'tune': {r: list(C.iso_directions(dirs['static'][r], 71001, float(r), 3, 1000)) for r in ratios}}
    return Wm, g, mu, dirs, arm_means, b_rand, rng


def synth_sets(rng, V, n_bands=5):
    """合成の語の集合と語の側の帰無の候補・層（凍結の集合の形）。"""
    ids = list(rng.permutation(V))
    take = lambda n: sorted(int(ids.pop()) for _ in range(n))
    L = {'a': take(1)[0], 'b': take(1)[0], 'c': take(1)[0], 'd': take(1)[0], 'refuse': take(1)[0]}
    E = {'static': {'plus': take(6), 'minus': take(5)}, 'td': {'plus': take(8), 'minus': []}, 'Nk': {'plus': take(3), 'minus': []}}
    for k, e in E.items():
        for side in ('plus', 'minus'):
            e[side + '_kata1'] = list(e[side])
            e[side + '_all'] = list(e[side])
            e[side + '_multi'] = list(e[side][:2])
    X = {}
    for f_ in ('survival', 'nuclear'):
        a_, o_ = take(4), take(5)
        X[f_] = {'a': a_, 'others': o_, 'a_unmarked': a_[1:], 'others_unmarked': o_[1:], 'a_kata1': a_, 'others_kata1': o_, 'a_all': a_, 'others_all': o_, 'a_multi': a_[:1], 'others_multi': o_[:1]}
    F = {'main': take(1)[0], 'sens': take(2)}
    pool = take(200)
    cells = {}
    for i in pool + E['static']['plus'] + E['static']['minus']:
        cells[str(i)] = ['K', '1' if i % 3 else '2', int(i % n_bands)]
    ce = collections.Counter(tuple(cells[str(i)]) for i in pool)
    ne = collections.Counter(tuple(cells[str(i)]) for i in E['static']['plus'] + E['static']['minus'])
    g_, ok = C.strata_groups(ce, ne, n_bands, 5)
    strata = {'%s|%s' % tl: [[list(x[0]), x[1], x[2], 0, 0] for x in gl] for tl, gl in g_.items()}
    ws = {'pool': pool, 'cells': cells, 'strata': strata, 'sens_pool': pool[:120], 'sens_ok': True}
    ce2 = collections.Counter(tuple(cells[str(i)]) for i in pool[:120])
    g2, ok2 = C.strata_groups(ce2, ne, n_bands, 5)
    ws['sens_strata'] = {'%s|%s' % tl: [[list(x[0]), x[1], x[2], 0, 0] for x in gl] for tl, gl in g2.items()}
    ws['sens_ok'] = ok2
    return {'sets': {'L': L, 'R': L['refuse'], 'E': E, 'X': X, 'F': F}, 'word_side': ws}


def _selftest():
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    TL = json.loads(json.dumps(TL))
    TL['nulls']['isotropic']['count'] = 1000
    TL['nulls']['word_side']['draws'] = 300
    V, d = 400, 48
    Wm, g, mu, dirs, arm_means, b_rand, rng = synth_bundle(d=d, V=V)
    SJ = synth_sets(rng, V)
    rows_of = lambda ids: [Wm[int(i)] for i in ids]
    delta_full = lambda U: (Wm @ (np.asarray(U, dtype=np.float32) * g[None, :]).T)
    res = layer1(TL, SJ, rows_of, mu, g, dirs, arm_means, b_rand, delta_full, lambda i: 'w%d' % i, np.linalg.norm(Wm * g[None, :], axis=1), V)
    # 係数のベクトルの値と、Δℓ を直に組んだ値が一致する
    u = dirs['static']['0.5']
    dl = (Wm @ (u * g)).astype(np.float64)
    L = SJ['sets']['L']
    ml = dl[L['a']] - np.mean([dl[L['b']], dl[L['c']]])
    assert abs(res['layers']['0.5']['directions']['static']['M_L_survival']['value'] - ml) < 1e-3 * max(1, abs(ml))
    mf = dl[SJ['sets']['F']['main']] - dl.mean()
    assert abs(res['layers']['0.5']['directions']['static']['M_F']['value'] - mf) < 1e-3 * max(1, abs(mf))
    assert set(res['primary']['metrics']) == set(TL['primary']['metrics']) and len(res['lists']) == 12
    assert res['layers']['0.5']['directions']['rand:0'] and 'tune_rand:2' in res['layers']['0.25']['directions']
    # ランダム方向の突き合わせ（裁定 D187）: 同じ・最後の桁の違い・許容の十倍の大きさの違い・乱数の列の違い・形の違い・鍵の欠け・有限でない値
    loc = {'main@0.5': np.array(b_rand['main']['0.5'])}
    loc.update({'tune@%s' % r: np.array(v) for r, v in b_rand['tune'].items()})
    tol = TL['nulls']['B_random']['repro_tol']
    c0 = compare_random_dirs(loc, {k: v.copy() for k, v in loc.items()}, tol)
    assert c0['ok'] and c0['rel_max'] == 0 and all(r['bitwise_equal'] for r in c0['keys'].values())
    ulp = {k: v * (1.0 + float(np.finfo(np.float32).eps)) for k, v in loc.items()}
    c1 = compare_random_dirs(loc, ulp, tol)
    assert c1['ok'] and 0 < c1['rel_max'] < tol and not any(r['bitwise_equal'] for r in c1['keys'].values())
    assert c1['keys']['main@0.5']['sha256_local'] != c1['keys']['main@0.5']['sha256_colab']
    big = dict(loc, **{'tune@0.75': loc['tune@0.75'] * (1 + 10 * tol)})
    assert not compare_random_dirs(loc, big, tol)['ok']
    other = dict(loc, **{'main@0.5': np.array(C.iso_directions(dirs['static']['0.5'], 71003, 0.5, 3, 1000))})
    c3 = compare_random_dirs(loc, other, tol)
    assert not c3['ok'] and c3['keys']['main@0.5']['rel_max'] > 0.1
    assert not compare_random_dirs(loc, dict(loc, **{'main@0.5': loc['main@0.5'][:2]}), tol)['ok']
    assert not compare_random_dirs(loc, {k: v for k, v in loc.items() if k != 'tune@0.25'}, tol)['ok']
    bad = loc['tune@0.5'].copy()
    bad[1, 5] = np.nan
    assert not compare_random_dirs(loc, dict(loc, **{'tune@0.5': bad}), tol)['ok']
    # 方向の npz の読み（JSON の SHA-256 の欄との食い違いで止まる）
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        npz = os.path.join(td, 'random_dirs.npz')
        np.savez(npz, **loc)
        CCx = {'random_dirs_npz': {'sha256': sha256f(npz)}, 'random_dirs_sha256': {k: dirs_sha256(v) for k, v in loc.items()}}
        back = load_colab_dirs(npz, CCx)
        assert sorted(back) == sorted(loc) and all(np.array_equal(back[k], loc[k]) for k in loc)
        for broken in ({'random_dirs_npz': {'sha256': '0' * 64}, 'random_dirs_sha256': CCx['random_dirs_sha256']},
                       {'random_dirs_npz': CCx['random_dirs_npz'], 'random_dirs_sha256': dict(CCx['random_dirs_sha256'], **{'main@0.5': 'X'})}):
            try:
                load_colab_dirs(npz, broken)
                raise AssertionError('止まるべき読みが通った')
            except SystemExit:
                pass
    print('[blens_lens] 自己検査 OK（%s・ランダム方向の突き合わせの七つの形と方向の npz の読みを含む）' % VERSION)


if __name__ == '__main__':
    main()
