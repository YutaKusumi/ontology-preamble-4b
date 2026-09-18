# 段階 B 器材の実装検分・資料の束 part5（機械生成・2026-09-18 03:43 UTC）

## tools/direction_B.py（SHA16 B119C2F58AE5B0B8）

```python
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
```

## tools/steer_B.py（SHA16 D2F61B71675BE324）

```python
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
```

## tools/run_stageB_local.py（SHA16 161857689B498C70）

```python
# -*- coding: utf-8 -*-
"""run_stageB_local.py v1 —— 段階 B の走行器（transformers・bf16・**hook つき**・手元／Colab）。

段階 A の走行器（`run_preamble_local.py` v2.7・vLLM の OpenAI 互換サーバ）は凍結物なので触らない。
B は hook を掛けるため transformers を直に使うが、**プロンプトの組み立てと採点の経路は凍結物に合わせる**:
  - 組み立て: `前置き + '\\n\\n' + 場面の本文 + 指示`（前置きを持たない N 腕は場面の本文から）。凍結走行器の `user_message` と同じ。
    起動時に凍結走行器のソースに同じ式があることを確かめる（食い違えば止まる）。
  - 採点: 凍結パーサ `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` の `parse_app_v2` と `is_catastrophic` を import する。
走行の相（正本 `tags`）: 同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`。
介入（正本 `selection.apply`・`random_control`）: `h ← h ± α·v̂` を**場面本文の開始位置から EOS まで**に掛ける。方向とノルムの規則は `steer_B.py`。
詰めは左（`runner.padding`）・バッチは設計定数（`runner.batch`）・生成の設定は `runner.generation`（品質床は `quality_floor.generation`）。
出力: results/<tag>/<tag>__…/{manifest.json, trials-*.jsonl, raw-*.jsonl} と results/sessions-B/<tag>__s<番号>.json。
用法: python tools/run_stageB_local.py --phase main --scenario N1 --session 1 --directions results/dirB/directions.npz
      python tools/run_stageB_local.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, uuid, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B
import steer_B

VERSION = 'v1'
REPO = runs_B.REPO
T = runs_B.load_T()
FROZEN_RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py')
FROZEN_PARSER = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py')
SCEN_PATH = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json')
ASSEMBLY_EXPR = "(t + '\\n\\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)"


def check_assembly_matches_frozen():
    """組み立ての式が凍結走行器と同じであり、正本にも登録されていることを確かめる（裁定 D87・食い違えば止まる）。"""
    src = open(FROZEN_RUNNER, encoding='utf-8').read()
    if ASSEMBLY_EXPR not in src:
        raise SystemExit('凍結走行器の組み立ての式と違う（凍結物が変わったか、この器が古い）: %s' % FROZEN_RUNNER)
    reg = (T['runner'].get('prompt_assembly') or '')
    if '前置き' not in reg or '場面の本文' not in reg or '指示' not in reg:
        raise SystemExit('正本 runner.prompt_assembly に組み立ての式が無い（裁定 D87）')
    return runs_B.sha16_file(FROZEN_RUNNER)


def arm_texts():
    """正本 `arms.sha16` の SHA16 で腕の素材を引き当てる（手で置き場を書かない）。N は前置きを持たない。"""
    want = {v: k for k, v in T['arms']['sha16'].items() if v}
    found = {}
    for root, _, fs in os.walk(os.path.join(REPO, 'arms')):
        for fn in sorted(fs):
            p = os.path.join(root, fn)
            try:
                b = open(p, 'rb').read()
            except OSError:
                continue
            h = hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
            if h in want and want[h] not in found:
                found[want[h]] = {'path': os.path.relpath(p, REPO).replace('\\', '/'), 'sha16': h,
                                  'text': b.decode('utf-8').replace('\r\n', '\n')}
    found['N'] = {'path': None, 'sha16': None, 'text': ''}
    missing = [a for a in T['arms']['panel'] if a not in found]
    if missing:
        raise SystemExit('腕の素材が見つからない（SHA16 で引いた）: %s' % '・'.join(missing))
    return found


def scenario_text(scenario):
    d = json.load(open(SCEN_PATH, encoding='utf-8'))
    s = {x['question_id']: x for x in d['scenarios']}.get(scenario)
    if s is None:
        raise SystemExit('場面が凍結の素材に無い: %s' % scenario)
    return s


def user_message(arm_text, scen_text, instruction):
    """凍結走行器 `user_message` と同じ組み立て。"""
    t = arm_text or ''
    return (t + '\n\n' + scen_text + instruction) if t else (scen_text + instruction)


def base_arm_of(arm):
    return re.split(r'[+\-]v', arm)[0]


def arm_plan(arm):
    """腕の名から介入の中身を決める（向き・方向の種類）。無操作なら None。"""
    if '+v' not in arm and '-v' not in arm:
        return None
    sign = +1 if '+v' in arm else -1
    tail = arm.split('+v')[-1] if '+v' in arm else arm.split('-v')[-1]
    kind = {'': 'static', 'rand': 'random', 'Nk': 'Nk', 'td': 'td', '6b': 'loaded'}.get(tail)
    if kind is None:
        raise SystemExit('腕の名から方向を決められない: %s' % arm)
    return {'sign': sign, 'kind': kind, 'base': base_arm_of(arm)}


def make_hook(vec, coef, sign, start_idx):
    """`h ← h ± α·v̂` を、場面本文の開始位置から後ろ全部に掛ける hook（register_forward_hook）。"""
    import torch

    def hook(module, inputs, output):
        hs = output[0] if isinstance(output, tuple) else output
        v = torch.as_tensor(vec, dtype=hs.dtype, device=hs.device)
        hs[:, start_idx:, :] = hs[:, start_idx:, :] + sign * coef * v
        return (hs,) + tuple(output[1:]) if isinstance(output, tuple) else hs
    return hook


def trial_record(**kw):
    """正本 `trial_record` の欄をそろえる（欠けたら止まる）。"""
    need = ['生テキスト', '機械判定（三つ組）', '応答様式 (a)(b)', '検査認識の言及', '各選択肢の対数尤度（強制デコード・記述）',
            '副位置の活性（応答トークン平均・fp16）', '操作の有無と層・係数', '方向の id', 'seed', 'バッチ位置', '走行キー', 'proc_uuid']
    assert T['trial_record'] == need, '正本の試行の記録の欄が変わった（器を合わせ直す）'
    fields = ('trial_id', 'trial_index', 'arm', 'scenario', 'tag', 'status', 'catastrophe', 'choice', 'refuse_class',
              'format_fail', 'style_a', 'style_b', 'mention', 'loop_flag', 'truncated', 'correct', 'logprobs',
              'resp_mean_path', 'layer', 'coef', 'direction_id', 'seed', 'batch_pos', 'run_key', 'proc_uuid',
              'runner_sha', 'arms_spec', 'preamble_sha', 'model', 'sampling', 'dry_run')
    missing = [f for f in fields if f not in kw]
    if missing:
        raise SystemExit('試行の記録に欠けた欄がある: %s' % '・'.join(missing))
    return {f: kw[f] for f in fields}


def _selftest():
    sha = check_assembly_matches_frozen()
    texts = arm_texts()
    assert texts['O']['text'] and texts['N']['text'] == ''
    msg = user_message(texts['O']['text'], '場面の本文', '\n指示')
    assert msg.startswith(texts['O']['text']) and msg.endswith('\n指示') and '\n\n場面の本文' in msg
    assert user_message('', '場面の本文', '\n指示') == '場面の本文\n指示', 'N 腕は前置きを付けない'
    plans = {a: arm_plan(a) for a in T['arms']['main']}
    assert plans['Onull'] is None and plans['Onull+v']['kind'] == 'static' and plans['Onull+v']['sign'] == +1
    assert plans['O-Ncold-v']['sign'] == -1 and plans['O-Ncold+vNk']['kind'] == 'Nk'
    assert plans['Onull+vrand']['kind'] == 'random' and plans['Osec-Ncold+v6b']['kind'] == 'loaded'
    assert plans['O-Ncold-vtd']['kind'] == 'td' and plans['O-Ncold-vtd']['base'] == 'O-Ncold'
    # 方向の規則は steer_B 側で確かめる（ここでは繋がりだけ）
    v = np.ones(8)
    rs = steer_B.random_directions(v, 1.0, 'main', 0.5)
    assert len(rs) == T['random_control']['count']
    rec = trial_record(**{f: None for f in ('trial_id', 'trial_index', 'arm', 'scenario', 'tag', 'status', 'catastrophe', 'choice',
                                            'refuse_class', 'format_fail', 'style_a', 'style_b', 'mention', 'loop_flag', 'truncated',
                                            'correct', 'logprobs', 'resp_mean_path', 'layer', 'coef', 'direction_id', 'seed',
                                            'batch_pos', 'run_key', 'proc_uuid', 'runner_sha', 'arms_spec', 'preamble_sha',
                                            'model', 'sampling', 'dry_run')})
    assert len(rec) == 31
    print('[run_stageB_local selftest] 組み立ての式（凍結走行器 SHA16 %s）・腕の素材・腕の名から方向・試行の記録の欄: すべて通った' % sha)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--phase', choices=['identity', 'tune', 'quality', 'main'], default=None)
    ap.add_argument('--scenario', default=None)
    ap.add_argument('--session', type=int, default=1)
    ap.add_argument('--directions', default=None, help='direction_B.py が凍結した方向（npz）')
    ap.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
    ap.add_argument('--out-root', default=None)
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    check_assembly_matches_frozen()
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except Exception as e:
        sys.exit('torch／transformers が無い: %s（この器は GPU の上で走らせる。手元の検査は --selftest）' % e)
    sys.exit('走行の本体（バッチ生成・hook の登録・採点・記録の書き出し）は Colab の段で埋める。'
             '規則の検査は --selftest、札の経路の検査は tools/dry_run_B.py（合成データ）で済ませてある。')
```

## tools/build_report_B.py（SHA16 83DCA2954528D696）

```python
# -*- coding: utf-8 -*-
"""build_report_B.py v1 —— 段階 B の結果報告を、**雛形**（`records/B/results-report-template-B.md`）と集計の出力から組み立てる。

雛形の〔結果 X〕を、機械の区画で置き換える:
  A 要約／B 走行の記録（整合検査・抽出検査・セッション）／C 門1 と選定／D 確証の族の表／E 封印した符号との照合／
  F 記述の族／G S4 の反証／H 利益相反と情報状態
**散文に手計算の数を残さない**（正本 `report_rules.typed_numbers`）。数はすべて集計の json から来る。
組み立ての後に走査器（`tools/report_lint.py`）を走らせる口を持つ（--lint）。
用法: python tools/build_report_B.py --analysis records/B/analysis-B-<日付>.json --gate records/B/gate-B-<日付>.json \
        [--integrity records/B/integrity-stageB-<日付>.json] [--out records/B/results-report-B.md] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
ap = argparse.ArgumentParser()
ap.add_argument('--analysis', required=True)
ap.add_argument('--gate', required=True)
ap.add_argument('--integrity', default=None)
ap.add_argument('--sampling', default=None)
ap.add_argument('--template', default=os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
a = ap.parse_args()
T = runs_B.load_T()
A = runs_B.read_json(a.analysis)
G = runs_B.read_json(a.gate)
INT = runs_B.read_json(a.integrity) if a.integrity else None
SMP = runs_B.read_json(a.sampling) if a.sampling else None
assert A.get('kind') == 'analyze_B' and G.get('kind') == 'gate_B', '集計または門の記録の種類が違う'
out_md = a.out or os.path.join(REPO, 'records', 'B', 'results-report-B.md')
if os.path.exists(out_md) and not a.force:
    sys.exit('既にある（--force で上書き）: %s' % out_md)
tpl = open(a.template, encoding='utf-8').read()
PS = T['print_strings']
c = A['counts']
n_conf = sum(x['m'] for x in T['families'].values())


def block(lines):
    return '\n'.join(lines)


A_sum = block([
    '```',
    PS['first_finding'].format(confirmed=c['確証'], undecidable=c['判定不能（検閲）'], qfloor=c['判定不能（品質床）'],
                               ff=c['判定保留（書式外転位）'], refuse=c['判定保留（refuse 転位）'] + c['判定保留（refuse 転位・差）'],
                               style=c['判定保留（様式転位）'], ns=c['非有意']),
    PS['scope'],
    'S4 の反証: %s' % A['s4'].get('verdict'),
    '```'])
B_run = block(['```',
               '整合検査: %s' % ('不整合 %d 件・注 %d 件（%s）' % (len(INT['problems']), len(INT['notes']), INT['tag']) if INT else '（記録が渡されていない）'),
               '抽出検査: %s' % ('標本 %d 件・対応表の封印あり' % SMP.get('n_items', 0) if SMP else '（記録が渡されていない）'),
               '正本 SHA16 %s・集計 %s UTC' % (A['contrasts_sha16'], A['generated_utc']),
               '```'])
sel = G['selection']['pick'] or {}
C_gate = block(['```',
                (PS['gate1_open'].format(k=G['gate1']['quality_pass_candidates'], layer=sel.get('layer'), coef=sel.get('coef'),
                                         eff=sel.get('eff_pt'), tied=len(G['selection']['tied']))
                 if G['gate1']['open'] else PS['gate1_closed']),
                PS['selection_coi'], PS['selection_direction'],
                ('同値の帯: 幅 %s pt（帰無の模擬 %s 回・同値の候補 %d 組）' % (G['selection']['equivalence_band']['q95_pt'],
                                                                format(G['selection']['equivalence_band']['reps'], ','),
                                                                len(G['selection']['tied'])) if G['selection'].get('equivalence_band') else ''),
                (G['selection'].get('tie_note') or ''), (G['selection'].get('nonpositive_stop') or ''),
                '```'])
rows = ['| 対比 | 場面 | 破局 A/n | 破局 B/n | pt 差 | 区間 | p | 書式外の差 | refuse の差 | 様式の差 | 札 |', '|---|---|---|---|---|---|---|---|---|---|---|']
for r in A['confirm']:
    if r.get('missing'):
        rows.append('| %s | %s | — | — | — | — | — | — | — | — | %s |' % (r['id'], r['scenario'], r['label']))
        continue
    rows.append('| %s | %s | %d/%d | %d/%d | %s | %s | %s | %s | %s | %s | %s |'
                % (r['id'], r['scenario'], r['k_A'], r['n_ok_A'], r['k_B'], r['n_ok_B'], r['diff_pt'], r['ci'],
                   None if r['p'] is None else round(r['p'], 5), r.get('ff_diff_pt'), r.get('refuse_diff_pt'), r.get('style_diff_pt'), r['label']))
D_conf = block(rows)
sg = A['sign_agreement']
E_sign = block(['```', (PS['sign_agreement'].format(agree=sg['agree'], confirmed=sg['confirmed']) if sg['sealed']
                        else '封印の記録が渡されていないので、予想符号との照合は行っていない。'), '```'])
F_desc = []
for fam, rs in A['descriptive'].items():
    if not rs:
        continue
    F_desc += ['**%s**' % fam, '', '| 対比 | 破局率 A | 破局率 B | pt 差 | 区間 |', '|---|---|---|---|---|']
    for r in rs:
        if r.get('missing'):
            F_desc.append('| %s | — | — | — | — |' % r['id'])
        else:
            F_desc.append('| %s | %s | %s | %s | %s |' % (r['id'], None if r['rate_A'] is None else round(r['rate_A'], 4),
                                                          None if r['rate_B'] is None else round(r['rate_B'], 4), r['diff_pt'], r['ci']))
    F_desc.append('')
F_desc.append(PS['no_p_desc'])
s4 = A['s4']
G_s4 = block(['```', '判定: %s' % s4.get('verdict'),
              ('pt 差 %s・区間 %s・相手の腕の率 %s・%s pt の検出力 %s（線は %s）'
               % (s4.get('diff_pt'), s4.get('ci'), s4.get('partner_rate'), s4.get('effect_pt'), s4.get('power_at_effect'), s4.get('power_min'))
               if 'power_at_effect' in s4 else ''),
              '封印: %s' % s4.get('sealed_prediction'), '```'])
H_coi = block(['```', T['selection']['coi_note'], T['publication']['dual_use'][:0] or '',
               '率盲検の外の経路: 同一性選別の距離／調整走行の率（選定に要る）／品質床の得点。本走行の率は整合検査まで見ない。',
               '起草者は段階 A の公開結果を見ている（封印予想の情報状態の欄に記す）。', '```'])

for ph, txt in (('A', A_sum), ('B', B_run), ('C', C_gate), ('D', D_conf), ('E', E_sign), ('F', block(F_desc)), ('G', G_s4), ('H', H_coi)):
    key = '〔結果 %s〕' % ph
    if key not in tpl:
        sys.exit('雛形に %s が無い' % key)
    tpl = tpl.replace(key, txt)
tpl += '\n\n## 11. 組み立ての記録（機械）\n\n- 器 `tools/build_report_B.py` %s・%s UTC。集計 `%s`（SHA16 %s）・門 `%s`（SHA16 %s）。\n' % (
    VERSION, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
    os.path.relpath(a.analysis, REPO).replace('\\', '/'), runs_B.sha16_file(a.analysis),
    os.path.relpath(a.gate, REPO).replace('\\', '/'), runs_B.sha16_file(a.gate))
open(out_md, 'w', encoding='utf-8', newline='\n').write(tpl)
print('[build_report_B] %s' % out_md)
```

## tools/freeze_B.py（SHA16 516ADCFD5178D185）

```python
# -*- coding: utf-8 -*-
"""freeze_B.py v1 —— 段階 B の**凍結の記帳**（凍結物の SHA・封印予想・凍結時に記帳する値・逸脱台帳の口）。

凍結するもの（正本 `publication.record_first`・草案8B §2.11）:
  凍結本文（草案）・正本 `design/contrasts-B.json`・腕と方向の定義・器材・報告の雛形・**封印予想**。
凍結時に記帳する値（設計の段では書けないもの）:
  - 重みの rev・tokenizer の版・**総層数**（`selection.candidates.layer_index_rule`）と層の添字
  - **腕ごとのトークン長**（裁定 D82・`position_length.record_at_freeze`）
  - 品質床の課題の出所・版・ライセンス・断片の SHA（裁定 D66）と、入力・帯・採点・最大トークン数（採否表 P216）
  - v̂ の SHA（`selection.vector_fix`）と方向の要約統計（ノルム・コサイン・場面間の安定性）
封印予想（`seal_format`）: 確証の各対比の符号と S4 の反証。**B のデータを一つも見る前**に書き、情報状態と時機を添える。
凍結の後の変更はすべて**逸脱**とし、番号・日付・理由・登録者の承認を記帳する（`deviation.rule`）。
出力: records/B/FREEZE-RECORD-B.md と同 .json（--force が無ければ上書きしない）。
用法: python tools/freeze_B.py --draft design/design-stageB-draft8.md [--seal records/B/seal-B.json] [--values records/B/freeze-values-B.json] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_B

VERSION = 'v1'
REPO = runs_B.REPO
TOOLS = ['runs_B.py', 'make_contrasts_B.py', 'design_facts_B.py', 'build_draftB.py', 'numbers_lint.py', 'gate_B.py', 'analyze_B.py',
         'integrity_B.py', 'sample_inspection_B.py', 'direction_B.py', 'steer_B.py', 'run_stageB_local.py', 'synth_B.py',
         'dry_run_B.py', 'build_report_B.py', 'freeze_B.py']
NEED_VALUES = ['model_rev', 'tokenizer_rev', 'num_hidden_layers', 'layer_indices', 'arm_token_lengths',
               'quality_task', 'quality_input', 'quality_apply_band', 'quality_scoring', 'quality_max_tokens',
               'v_hat_sha256', 'direction_stats']
ap = argparse.ArgumentParser()
ap.add_argument('--draft', required=True)
ap.add_argument('--seal', default=None)
ap.add_argument('--values', default=None, help='凍結時に記帳する値（json・上の NEED_VALUES）')
ap.add_argument('--contrasts', default=None)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
ap.add_argument('--allow-missing', action='store_true', help='記帳の値や封印が揃っていなくても書く（**凍結ではなく点検用**）')
a = ap.parse_args()
T = runs_B.load_T(a.contrasts)
cpath = a.contrasts or runs_B.CPATH
now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'FREEZE-RECORD-B.md')
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

frozen = {'canon': {'path': 'design/contrasts-B.json', 'sha16': runs_B.sha16_file(cpath), 'version': T['version']},
          'draft': {'path': os.path.relpath(a.draft, REPO).replace('\\', '/'), 'sha16': runs_B.sha16_file(a.draft)},
          'facts': {'path': 'records/B/design-facts-B.md', 'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'design-facts-B.md'))},
          'report_template': {'path': 'records/B/results-report-template-B.md',
                              'sha16': runs_B.sha16_file(os.path.join(REPO, 'records', 'B', 'results-report-template-B.md'))},
          'arms': T['arms']['sha16'], 'arm_files': T['arms'].get('files'),
          'tools': {}}
for t in TOOLS:
    p = os.path.join(REPO, 'tools', t)
    frozen['tools'][t] = runs_B.sha16_file(p) if os.path.exists(p) else None
missing_tools = [t for t, v in frozen['tools'].items() if v is None]

VALUES = runs_B.read_json(a.values) if a.values else {}
missing_values = [k for k in NEED_VALUES if k not in VALUES]
SEAL = runs_B.read_json(a.seal) if a.seal else None
conf_ids = [c['id'] for F in T['families'].values() for c in F['contrasts']]
missing_seal = [] if not SEAL else [i for i in conf_ids if i not in (SEAL.get('signs') or {})]
blockers = []
if missing_tools:
    blockers.append('器材が揃っていない: %s' % '・'.join(missing_tools))
if missing_values:
    blockers.append('凍結時に記帳する値が揃っていない: %s' % '・'.join(missing_values))
if SEAL is None:
    blockers.append('封印予想が渡されていない（`seal_format` の様式で、データを一つも見る前に書く）')
elif missing_seal:
    blockers.append('封印の無い確証の対比: %s' % '・'.join(missing_seal))
if blockers and not a.allow_missing:
    print('[freeze_B] 凍結できない（--allow-missing は点検用）:')
    for b in blockers:
        print('  - ' + b)
    sys.exit(1)

REC = {'kind': 'freeze_B', 'version': VERSION, 'frozen_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'frozen_jst': jst.strftime('%Y-%m-%d %H:%M'),
       'frozen': frozen, 'values': VALUES, 'seal': SEAL, 'blockers': blockers, 'deviations': [],
       'deviation_rule': T['deviation']['rule'], 'record_first': T['publication']['record_first']}
json.dump(REC, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B 凍結記録（機械生成・`tools/freeze_B.py` %s）' % VERSION, '',
     '- 凍結の時刻: %s UTC（日本時間 %s）。%s' % (now.strftime('%Y-%m-%d %H:%M'), jst.strftime('%Y-%m-%d %H:%M'),
                                            '**点検（--allow-missing）であり凍結ではない**' if blockers else '凍結した。'), '',
     '## 凍結物', '', '| 物 | 置き場 | SHA16 |', '|---|---|---|']
for k in ('canon', 'draft', 'facts', 'report_template'):
    L.append('| %s | `%s` | %s |' % (k, frozen[k]['path'], frozen[k]['sha16']))
for t, v in sorted(frozen['tools'].items()):
    L.append('| 器材 | `tools/%s` | %s |' % (t, v or '**無い**'))
for arm, sha in sorted((frozen['arms'] or {}).items()):
    L.append('| 腕 | %s | %s |' % (arm, sha or '（前置きを持たない）'))
L += ['', '## 凍結時に記帳する値', '']
for k in NEED_VALUES:
    L.append('- %s: %s' % (k, json.dumps(VALUES[k], ensure_ascii=False) if k in VALUES else '**まだ無い**'))
L += ['', '## 封印予想（`seal_format`）', '']
if SEAL:
    L += ['- 時機: %s' % T['seal_format']['timing'], '- 情報状態: %s' % T['seal_format']['information_state'],
          '- 封印した符号: %d／確証の対比 %d' % (len(SEAL.get('signs') or {}), len(conf_ids)),
          '- S4 の反証: %s' % (SEAL.get('s4') or '**まだ無い**'), '- %s' % T['seal_format']['reading']]
else:
    L.append('- **まだ無い**（`seal_format` の様式で、データを一つも見る前に書く）')
if blockers:
    L += ['', '## 凍結を止めているもの', ''] + ['- ' + b for b in blockers]
L += ['', '## 逸脱台帳', '', '- %s' % T['deviation']['rule'], '- %s' % T['deviation']['silent_fix'], '- （凍結の後に足す）', '',
      '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[freeze_B] %s | 止めているもの %d 件' % (out_md, len(blockers)))
sys.exit(2 if blockers else 0)
```
