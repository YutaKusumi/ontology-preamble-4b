# -*- coding: utf-8 -*-
"""direction_B.py v4 —— 段階 B の**方向の抽出**（主位置の活性・方向の作成・決定性の検査・要約統計・v̂ の凍結）。

正本 `design/contrasts-B.json` の `selection.position`・`selection.candidates`・`directions`・`activation_storage`・`runner` に従う。
何をするか:
  (1) 腕 × 場面のプロンプトを組み、**プロンプトの最終トークン**（詰めでない最後の位置・`runner.padding`）の隠れ状態を、登録した層で取り出す。
  (2) 決定性の検査は二条（裁定 D91）: **同じ並べ方**で二度取って完全一致（外れたら走行を止める）／**並べ方を変えて**一度取り、許容差の内側かを見る（外れたら記帳して登録者に上げる）。
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
import os, sys, json, math, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v4'
REPO = runs_B.REPO
T = runs_B.load_T()
PANEL = T['arms']['panel']
EX = T['extraction_scenarios']
LAYER_RATIOS = T['selection']['candidates']['layers']
DIRS = T['directions']


def layer_index(ratio, n_layers):
    """層の割合 → 層の添字（正本 `selection.candidates.layer_index_rule`・零始まり）。

    **四捨五入**（Python の `round` は偶数丸めなので使わない・実装検分の採否表 P283）。"""
    idx = int(math.floor(ratio * n_layers + 0.5)) - 1
    assert 0 <= idx < n_layers, ('層の添字が範囲の外', ratio, n_layers, idx)
    return idx


def hidden_states_index(layer_idx):
    """`hidden_states` の添字（埋め込みの分だけ一つずれる・正本の「層の添字」とは別物）。"""
    return layer_idx + 1


def write_layer_record(out_dir, n_layers):
    """総層数と層の添字を**記帳**する（正本 `layer_index_rule` が求める・採否表 P283）。"""
    rec = {'num_hidden_layers': n_layers, 'ratios': LAYER_RATIOS,
           'layer_indices': {str(r): layer_index(r, n_layers) for r in LAYER_RATIOS},
           'hidden_states_indices': {str(r): hidden_states_index(layer_index(r, n_layers)) for r in LAYER_RATIOS}}
    os.makedirs(out_dir, exist_ok=True)
    json.dump(rec, open(os.path.join(out_dir, 'layers.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return rec


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
        raw_ratio = {}
        for name in pairs:
            v = per[name]['mean']
            raw_ratio[name] = (float(np.linalg.norm(v)) / float(np.linalg.norm(v_hat))) if np.linalg.norm(v_hat) else None
            if name != 'static':
                v = match_norm(v, v_hat)      # **全方向を ‖v̂〔static〕‖ に合わせる**（裁定 D102・採否表 P306・P310）
            out[(name, ratio)] = v
        stats[ratio] = {
            'norms': {name: float(np.linalg.norm(out[(name, ratio)])) for name in pairs},
            'raw_norm_ratio': raw_ratio,          # **合わせる前の比**（正本 coefficient_ref・採否表 P284 の後半）
            'cosines': {'%s~%s' % (x, y): cosine(out[(x, ratio)], out[(y, ratio)])
                        for i, x in enumerate(sorted(pairs)) for y in sorted(pairs)[i + 1:]},
            'stability': {name: {'cos_%s_%s' % (EX[0], EX[1]): cosine(per[name]['by_scenario'][EX[0]], per[name]['by_scenario'][EX[1]]),
                                 'norm_ratio': (float(np.linalg.norm(per[name]['by_scenario'][EX[0]])) /
                                                float(np.linalg.norm(per[name]['by_scenario'][EX[1]])) if np.linalg.norm(per[name]['by_scenario'][EX[1]]) else None)}
                          for name in pairs}}
    return out, stats


def determinism_same_order(h1, h2):
    """**同じ並べ方**で二度取った活性の完全一致（bitwise）を見る（裁定 D91 の (i)）。一致しなければ走行を止める。"""
    if set(h1) != set(h2):
        return False, ['鍵の集合が違う: %s' % sorted(set(h1) ^ set(h2))[:4]]
    bad = []
    for k in h1:
        a, b = np.asarray(h1[k]), np.asarray(h2[k])
        if np.isnan(a).any() or np.isnan(b).any():
            bad.append('%s: NaN を含む' % (k,))
        elif not np.array_equal(a, b):
            bad.append('%s: 一致しない' % (k,))
    return (not bad), bad


def determinism_cross_order(h1, h2, tol=None):
    """**並べ方を変えて**取った活性が許容差の内側かを見る（裁定 D91 の (ii)）。外れたら記帳して登録者に上げる（止めない）。"""
    tol = tol or T['activation_storage']['determinism']['cross_order_tolerance']
    rows = []
    if set(h1) != set(h2):      # **鍵の欠けを黙って無視しない**（裁定 D114・採否表 P318）
        rows.append({'key': '（鍵の集合）', 'ok': False,
                     'note': '鍵の集合が違う: %s' % sorted(set(h1) ^ set(h2), key=str)[:4]})
    for k in sorted(set(h1) & set(h2), key=str):
        a, b = np.asarray(h1[k], dtype=float), np.asarray(h2[k], dtype=float)
        na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
        cos = float(np.dot(a, b) / (na * nb)) if na and nb else None
        rel = float(np.max(np.abs(a - b)) / na) if na else None
        ok = (cos is not None and cos >= tol['cos_min']) and (rel is not None and rel <= tol['max_abs_over_norm'])
        rows.append({'key': str(k), 'cos': cos, 'max_abs_over_norm': rel, 'ok': ok})
    return all(r['ok'] for r in rows), rows


def _selftest():
    rng = np.random.default_rng(7)
    d = 16
    # 層番号は**手で書いた期待値の表**と突き合わせる（実装式で確かめない・採否表 P283）
    want = {(0.25, 36): 8, (0.5, 36): 17, (0.75, 36): 26, (0.25, 34): 8, (0.5, 34): 16, (0.75, 34): 25,
            (0.25, 42): 10, (0.5, 42): 20, (0.75, 42): 31}
    for (ratio, n), idx in want.items():
        assert layer_index(ratio, n) == idx, ('層番号が期待値と違う', ratio, n, layer_index(ratio, n), idx)
    assert hidden_states_index(layer_index(0.5, 36)) == 18, 'hidden_states の添字の変換が違う'
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
    # 決定性 (i) 同じ並べ方 → 完全一致
    ok, bad = determinism_same_order(H, dict(H))
    assert ok and not bad
    H2 = dict(H)
    k0 = next(iter(H2))
    H2[k0] = H2[k0] + 1e-9
    ok2, bad2 = determinism_same_order(H, H2)
    assert not ok2 and len(bad2) == 1, '決定性の検査が差を見落とす'
    H3 = dict(H)
    H3.pop(k0)
    ok3, bad3 = determinism_same_order(H, H3)
    assert not ok3 and '鍵の集合' in bad3[0], '鍵の欠けを見落とす'
    H4 = dict(H)
    H4[k0] = H4[k0] * np.nan
    ok4, bad4 = determinism_same_order(H, H4)
    assert not ok4 and 'NaN' in bad4[0], 'NaN を別の名で報告していない'
    # 決定性 (ii) 並べ方を変えた → 許容差
    tol = T['activation_storage']['determinism']['cross_order_tolerance']
    Hs = {k: vv + rng.normal(size=d) * 1e-6 for k, vv in H.items()}
    ok5, rows5 = determinism_cross_order(H, Hs)
    assert ok5, ('わずかな差が許容差を外れた', rows5[:1])
    Hb = {k: vv + rng.normal(size=d) * 1.0 for k, vv in H.items()}
    ok6, rows6 = determinism_cross_order(H, Hb)
    assert not ok6, '大きな差を許容差の内側と判定した'
    print('[direction_B selftest] 層番号（期待値の表・%d 通り）・hidden_states の添字・ノルム合わせ・安定性・'
          '決定性の二条（同じ並べ方は完全一致／並べ方を変えたら cos %g・相対差 %g）: すべて通った'
          % (len(want), tol['cos_min'], tol['max_abs_over_norm']))


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
    # 置き場を直に渡せるようにする（版を固定し、Hub への問い合わせを避ける・裁定 D115・採否表 P328）
    tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or a.model)
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
