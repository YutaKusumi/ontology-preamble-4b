# -*- coding: utf-8 -*-
"""direction_B.py v1 —— 段階 B の**方向の抽出**（主位置の活性・方向の作成・決定性の検査・要約統計・v̂ の凍結）。

正本 `design/contrasts-B.json` の `selection.position`・`selection.candidates`・`directions`・`activation_storage`・`runner` に従う。
何をするか:
  (1) 腕 × 場面のプロンプトを組み、**プロンプトの最終トークン**（詰めでない最後の位置・`runner.padding`）の隠れ状態を、登録した層で取り出す。
  (2) 同じ活性を**二度**（バッチの並べ方を変えて）取り、**完全一致**を確かめる（`activation_storage.determinism`）。一致しなければ止まる。
  (3) 方向を作る: (6a) 静的 h_O − h_Osec／(6b) 負荷下 h_{O-Ncold} − h_{Osec-Ncold}／Nk 方向 h_Nk − h_N／腕対の差方向 h_Onull − h_N。
      いずれも**抽出場面の平均**。td は v̂ のノルムに合わせる（`directions.td`）。
  (4) 要約統計: 層ごとのノルム・方向どうしのコサイン・**平均を取る前の場面ごとの差ベクトルどうしのコサイン**（抽出場面の間の安定性・採否表 P237）。
  (5) v̂ を凍結して保存し、SHA を記帳する（`selection.vector_fix`）。
層番号は `selection.candidates.layer_index_rule`（割合 × 総層数を四捨五入して一つ引く・総層数は config から読んで記帳）。
**この器は GPU の上でしか本走行できない。** 手元では `--selftest`（合成のベクトルで規則だけを確かめる）が走る。
用法: python tools/direction_B.py --model Qwen/Qwen3-4B-Instruct-2507 --out results/dirB [--dtype bfloat16]
      python tools/direction_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
PANEL = T['arms']['panel']
EX = T['extraction_scenarios']
LAYER_RATIOS = T['selection']['candidates']['layers']
DIRS = T['directions']


def layer_index(ratio, n_layers):
    """層の割合 → 層の添字（正本 selection.candidates.layer_index_rule・零始まり）。"""
    return int(round(ratio * n_layers)) - 1


def unit(v):
    n = float(np.linalg.norm(v))
    return v / n if n else v


def match_norm(v, ref):
    """v の向きのまま、ノルムを ref のノルムに合わせる（裁定 D75 の基準は v̂）。"""
    nv, nr = float(np.linalg.norm(v)), float(np.linalg.norm(ref))
    return v * (nr / nv) if nv else v


def cosine(a, b):
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    return float(np.dot(a, b) / (na * nb)) if na and nb else None


def build_directions(H):
    """H[(arm, scenario, layer_ratio)] = 活性ベクトル → 方向と要約統計。

    方向は抽出場面の平均。td は v̂ のノルムに合わせる。安定性は「平均を取る前の場面ごとの差ベクトルどうしのコサイン」。"""
    out, stats = {}, {}
    pairs = {'static': ('O', 'Osec'), 'loaded': ('O-Ncold', 'Osec-Ncold'), 'Nk': ('Nk', 'N'), 'td': ('Onull', 'N')}
    for ratio in LAYER_RATIOS:
        per = {}
        for name, (a1, a2) in pairs.items():
            diffs = {sc: H[(a1, sc, ratio)] - H[(a2, sc, ratio)] for sc in EX}
            per[name] = {'mean': np.mean([diffs[sc] for sc in EX], axis=0), 'by_scenario': diffs}
        v_hat = per['static']['mean']
        for name in pairs:
            v = per[name]['mean']
            if name == 'td':
                v = match_norm(v, v_hat)
            out[(name, ratio)] = v
        stats[ratio] = {
            'norms': {name: float(np.linalg.norm(out[(name, ratio)])) for name in pairs},
            'cosines': {'%s~%s' % (x, y): cosine(out[(x, ratio)], out[(y, ratio)])
                        for i, x in enumerate(sorted(pairs)) for y in sorted(pairs)[i + 1:]},
            'stability': {name: {'cos_%s_%s' % (EX[0], EX[1]): cosine(per[name]['by_scenario'][EX[0]], per[name]['by_scenario'][EX[1]]),
                                 'norm_ratio': (float(np.linalg.norm(per[name]['by_scenario'][EX[0]])) /
                                                float(np.linalg.norm(per[name]['by_scenario'][EX[1]])) if np.linalg.norm(per[name]['by_scenario'][EX[1]]) else None)}
                          for name in pairs}}
    return out, stats


def determinism_ok(h1, h2):
    """主位置の活性を二度取って**完全一致**（bitwise）を見る（activation_storage.determinism）。"""
    bad = [k for k in h1 if not np.array_equal(h1[k], h2.get(k))]
    return (not bad), bad


def _selftest():
    rng = np.random.default_rng(7)
    d, n_layers = 16, 36
    assert layer_index(0.25, n_layers) == int(round(0.25 * n_layers)) - 1
    assert layer_index(0.5, n_layers) == 17 and layer_index(0.75, n_layers) == 26
    H = {}
    for arm in PANEL:
        for sc in EX:
            for ratio in LAYER_RATIOS:
                H[(arm, sc, ratio)] = rng.normal(size=d)
    dirs, stats = build_directions(H)
    v = dirs[('static', LAYER_RATIOS[0])]
    td = dirs[('td', LAYER_RATIOS[0])]
    assert abs(np.linalg.norm(td) - np.linalg.norm(v)) < 1e-9, 'td のノルムが v̂ に合っていない'
    assert set(stats[LAYER_RATIOS[0]]['stability']) == {'static', 'loaded', 'Nk', 'td'}
    ok, bad = determinism_ok(H, dict(H))
    assert ok and not bad
    H2 = dict(H)
    k0 = next(iter(H2))
    H2[k0] = H2[k0] + 1e-9
    ok2, bad2 = determinism_ok(H, H2)
    assert not ok2 and bad2 == [k0], '決定性の検査が差を見落とす'
    print('[direction_B selftest] 層番号の規則・ノルム合わせ・安定性・決定性の検査: すべて通った')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
    ap.add_argument('--dtype', default='bfloat16')
    ap.add_argument('--out', default=None)
    ap.add_argument('--arms-dir', default=os.path.join(REPO, 'arms'))
    ap.add_argument('--scenarios-dir', default=None, help='場面の本文の置き場（凍結盤の素材）')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as e:                                    # 手元では届かない（Colab の段で走らせる）
        sys.exit('torch／transformers が無い: %s（この器は GPU の上で走らせる。手元の検査は --selftest）' % e)
    out_dir = a.out or os.path.join(REPO, 'results', 'dirB')
    os.makedirs(out_dir, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(a.model)
    tok.padding_side = 'left'                                  # 正本 runner.padding
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=getattr(torch, a.dtype), device_map='auto')
    model.eval()
    n_layers = model.config.num_hidden_layers
    idxs = {r: layer_index(r, n_layers) for r in LAYER_RATIOS}

    def prompts_for(arm, sc):
        raise SystemExit('場面と腕の本文の組み方は器材の段で確定する（--scenarios-dir の凍結素材から組む）。'
                         'この版は骨組みで、実際の組み立ては凍結の前に埋める（正本 quality_floor.input と同じ扱い）。')

    print('[direction_B] 総層数 %d・層の添字 %s（正本の割合 %s）' % (n_layers, idxs, LAYER_RATIOS))
    print('[direction_B] 本文の組み立てはまだ埋めていない（凍結の前に確定する）。--selftest で規則だけ確かめられる。')
