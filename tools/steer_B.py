# -*- coding: utf-8 -*-
"""steer_B.py v1 —— 段階 B の**介入**（方向の加減・ランダム方向・品質床・強制デコード）。

正本 `design/contrasts-B.json` の `selection.apply`・`random_control`・`quality_floor`・`runner` に従う。
規則（この器が守るもの）:
  - 加減は `h ← h ± α·v̂`（場面本文の開始位置から EOS まで・`register_forward_hook`・`selection.apply`）。α は**その層の v̂ のノルムに対する比**。
  - ランダム方向は層ごとに `random_control.count` 本引き、**係数を掛けた後の v̂ のノルムに合わせる**（裁定 D75・族を跨いで基準は一つ）。
  - ランダム方向は**調整走行と本走行で引き直す**（裁定 D84・種は `seeds.random_dirs` の tune と main）。
  - 一腕の試行は方向の登録順に等分し、端数は登録順に一つずつ配る（`random_control.allocation`・調整走行にも当てる）。
  - 品質床は**貪欲**（`quality_floor.generation`）。書式外は不正解に数え、api_error は一度だけ引き直す（`quality_floor.format_fail_rule`）。
  - 場面の試行は `runner.generation` の設定。詰めは左（`runner.padding`）。
**この器は GPU の上でしか本走行できない。** 手元では `--selftest`（ノルム合わせ・割り当て・引き直し・種の再現を合成のベクトルで確かめる）が走る。
用法: python tools/steer_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
RC = T['random_control']
N_RAND = RC['count']


def random_directions(v_hat, coef, phase, layer_ratio, count=N_RAND):
    """層ごとに count 本のランダム方向を引き、**係数を掛けた後の v̂ のノルム**に合わせる（裁定 D75）。

    phase は 'tune' か 'main'（裁定 D84・種を分けて引き直す）。同じ引数なら同じ方向が出る（決定的）。"""
    assert phase in ('tune', 'main'), '相は tune か main（裁定 D84）'
    seed = RC['seed'][phase]
    d = int(np.asarray(v_hat).shape[-1])
    # 層と係数で子ストリームを分ける（seeds.derivation の型・同じ層 × 係数なら再現する）
    ss = np.random.SeedSequence([seed, int(round(layer_ratio * 1000)), int(round(coef * 1000))])
    rng = np.random.default_rng(ss)
    target = coef * float(np.linalg.norm(v_hat))
    out = []
    for i in range(count):
        g = rng.normal(size=d)
        n = float(np.linalg.norm(g))
        out.append(g * (target / n) if n else g)
    return out


def allocate(n_trials, count=N_RAND):
    """一腕の試行を方向の登録順に等分し、端数は登録順に一つずつ配る（random_control.allocation）。"""
    base, rem = divmod(int(n_trials), int(count))
    return [base + (1 if i < rem else 0) for i in range(count)]


def apply_vector(h, v_hat, coef, sign):
    """h ← h ± α·v̂（α は v̂ のノルムに対する比なので、掛けるのは coef·v̂）。"""
    assert sign in (+1, -1)
    return h + sign * coef * np.asarray(v_hat)


def band_slice(prompt_len, total_len):
    """介入の帯（場面本文の開始位置から EOS まで）。左詰めの場合、帯は生成の側にも掛かる。"""
    return slice(prompt_len, total_len)


def quality_generation():
    """品質床の生成の設定（貪欲・正本 quality_floor.generation）。"""
    g = dict(T['quality_floor']['generation'])
    g['do_sample'] = bool(g.get('temperature'))
    return g


def main_generation():
    g = dict(T['runner']['generation'])
    g['do_sample'] = True
    return g


def score_quality(answer_letter, correct_letter, format_fail):
    """品質床の採点（書式外は不正解に数えて分母を保つ・quality_floor.format_fail_rule）。"""
    if format_fail or not answer_letter:
        return False
    return answer_letter.strip().upper() == correct_letter.strip().upper()


def _selftest():
    rng = np.random.default_rng(3)
    v = rng.normal(size=32)
    for coef in T['selection']['candidates']['coefficients']:
        for ratio in T['selection']['candidates']['layers']:
            rs = random_directions(v, coef, 'main', ratio)
            assert len(rs) == N_RAND
            for r in rs:
                assert abs(float(np.linalg.norm(r)) - coef * float(np.linalg.norm(v))) < 1e-9, 'ランダム方向のノルムが v̂ × 係数に合っていない'
    # 引き直し（裁定 D84）: 同じ層 × 係数でも相が違えば別の方向
    a1 = random_directions(v, 1.0, 'tune', 0.5)[0]
    a2 = random_directions(v, 1.0, 'main', 0.5)[0]
    assert not np.allclose(a1, a2), '調整走行と本走行で引き直していない'
    assert np.allclose(a1, random_directions(v, 1.0, 'tune', 0.5)[0]), '同じ引数で再現しない'
    assert not np.allclose(random_directions(v, 1.0, 'main', 0.25)[0], random_directions(v, 1.0, 'main', 0.75)[0]), '層で子ストリームが分かれていない'
    # 割り当て（random_control.allocation）
    for n in (200, 201, 100, 7):
        al = allocate(n)
        assert sum(al) == n and max(al) - min(al) <= 1 and al == sorted(al, reverse=True), '割り当ての端数の配り方が規則と違う'
    # 加減の向き
    h = rng.normal(size=32)
    assert np.allclose(apply_vector(h, v, 2.0, +1) - h, 2.0 * v)
    assert np.allclose(apply_vector(h, v, 0.5, -1) - h, -0.5 * v)
    # 品質床の採点と生成
    assert score_quality('A', 'a', False) and not score_quality('A', 'B', False) and not score_quality('A', 'A', True)
    assert quality_generation()['do_sample'] is False, '品質床が貪欲でない'
    assert main_generation()['temperature'] == T['runner']['generation']['temperature']
    print('[steer_B selftest] ノルム合わせ・引き直し・子ストリーム・割り当て・加減の向き・品質床の採点: すべて通った')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    sys.exit('この器は GPU の上の走行器から import して使う（手元の検査は --selftest）。'
             '走行の組み立て（場面の本文・hook の登録・バッチ）は `boot_stageB.py` の側にある。')
