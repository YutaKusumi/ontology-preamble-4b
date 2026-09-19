# -*- coding: utf-8 -*-
"""steer_B.py v6 —— 段階 B の**介入**（方向の加減・ランダム方向・品質床の生成と採点）。
v6（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: ランダム方向の割り当てを**交互**（試行の番号を方向の数で割った余り）にした（裁定 D140）。帯の起点（主位置）を**一つの関数 `main_position`** から出し、走行器がそれを呼び、自己検査がそれを検べる（採否表 P404）。

正本 `design/contrasts-B.json` の `selection.apply`・`random_control`・`quality_floor`・`runner` に従う。
規則（この器が守るもの）:
  - 加減は `h ← h ± α·v̂`（**主位置〔組み立て済みの列の最後のトークン〕から EOS まで**・`register_forward_hook`・`selection.apply`・裁定 D124）。α は**その層の v̂ のノルムに対する比**。
  - すべての方向（v̂・Nk・td・(6b)・ランダム方向）を**係数を掛ける前の ‖v̂〔static〕‖** に合わせ、**係数は加減のときに一度だけ**掛ける（裁定 D75・D90）。
    自己検査は「**全方向 × 全係数 × 全層**で加わる量のノルムが一致する」ことを確かめる（裁定 D102——前は v 腕とランダム腕の対しか回さず、交差族に同じ穴が残った）。
  - 介入の帯の起点は、**chat template を当てた組み立て済みの列の最後のトークン（主位置）**（裁定 D101 で template を当て、裁定 D124 で起点を主位置にした）。
    自己検査は起点を**独立の正解**（器を通さずに作った列の最後の位置）と照らし、復号して最終トークンと一致することを見る
    （`OP4B_TOKENIZER_DIR` に実トークナイザの置き場を渡したときに走る。**`OP4B_REQUIRE_FULL_SELFTEST=1` なら、飛ばすと失敗に倒す**・裁定 D122）。
    関数の名 `scenario_start_index` は裁定 D124 の前の名残で、返すのは主位置である。**起点の式は `main_position` 一つ**で、走行器もこれを呼ぶ（採否表 P404）。
  - ランダム方向は**調整走行と本走行で引き直す**（裁定 D84・種は `seeds.random_dirs` の tune と main）。
  - 一腕の試行の方向は**試行の番号を方向の数で割った余り**（交互・`random_control.allocation`・裁定 D140・調整走行にも当てる）。各方向の数は登録順の等分（端数は登録順に一つずつ）と同じ。
  - 品質床は**貪欲**（`quality_floor.generation`）で、**生成した文字列から記号を読み取る**（強制デコードは採らない・裁定 D120）。書式外は不正解に数え、api_error は一度だけ引き直す（`quality_floor.format_fail_rule`）。
  - 場面の試行は `runner.generation` の設定。詰めは左（`runner.padding`）。
**この器は GPU の上でしか本走行できない。** 手元では `--selftest`（ノルム合わせ・割り当て・引き直し・種の再現を合成のベクトルで確かめる）が走る。
用法: python tools/steer_B.py --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B

VERSION = 'v6'
STRICT = os.environ.get('OP4B_REQUIRE_FULL_SELFTEST') == '1'     # 実機の段では飛ばしを失敗に倒す（裁定 D122・採否表 P344）
REPO = runs_B.REPO
T = runs_B.load_T()
RC = T['random_control']
N_RAND = RC['count']


def random_directions(v_hat_static, phase, layer_ratio, count=N_RAND):
    """層ごとに count 本のランダム方向を引き、**係数を掛ける前の ‖v̂〔static〕‖** に合わせる（裁定 D90・2026-09-18）。

    係数は加減のときに一度だけ掛ける（`apply_vector`・`selection.apply`）。基準は**静的 v̂ ひとつ**で、族を跨いで変えない（裁定 D75）。
    phase は 'tune' か 'main'（裁定 D84・種を分けて引き直す）。子ストリームは**層ごと**（正本 `random_control.per_layer`・係数は入れない・採否表 P285）。"""
    assert phase in ('tune', 'main'), '相は tune か main（裁定 D84）'
    seed = RC['seed'][phase]
    d = int(np.asarray(v_hat_static).shape[-1])
    ss = np.random.SeedSequence([seed, int(round(layer_ratio * 1000))])
    rng = np.random.default_rng(ss)
    target = float(np.linalg.norm(v_hat_static))
    out = []
    for i in range(count):
        g = rng.normal(size=d)
        n = float(np.linalg.norm(g))
        out.append(g * (target / n) if n else g)
    return out


def match_to_static(v, v_hat_static):
    """どの方向（Nk・td・(6b)）も、加える前に ‖v̂〔static〕‖ に合わせる（裁定 D75・D90）。"""
    n = float(np.linalg.norm(v))
    return v * (float(np.linalg.norm(v_hat_static)) / n) if n else v


def allocate(n_trials, count=N_RAND):
    """各方向の試行の数（登録順に等分し、端数は登録順に一つずつ）。交互の割り当て（`direction_of`）の数と一致する（random_control.allocation）。"""
    base, rem = divmod(int(n_trials), int(count))
    return [base + (1 if i < rem else 0) for i in range(count)]


def direction_of(trial_index, n_trials, count=N_RAND):
    """試行の番号から方向の添字を決める——**試行の番号を方向の数で割った余り（交互）**（正本 `random_control.allocation`・裁定 D140）。

    試行の番号だけで決まるので**再開しても変わらない**（採否表 P298）。各方向の数は `allocate` と一致する。
    前は登録順の連続した塊に割っており、方向がバッチ・時刻・セッションと交絡した（採否表 P398）。"""
    if not 0 <= int(trial_index) < int(n_trials):
        raise ValueError('試行の番号が全体の数の外にある: %s / %s' % (trial_index, n_trials))
    return int(trial_index) % int(count)


def apply_vector(h, v_hat, coef, sign):
    """h ← h ± α·v̂（α は v̂ のノルムに対する比なので、掛けるのは coef·v̂）。"""
    assert sign in (+1, -1)
    return h + sign * coef * np.asarray(v_hat)


def apply_chat(tokenizer, user_message):
    """**段階 B は chat template を当てる**（正本 `runner.chat_template`・裁定 D101）。組み立て済みのトークン列を返す。"""
    return list(tokenizer.apply_chat_template([{'role': 'user', 'content': user_message}],
                                              add_generation_prompt=True, tokenize=True))


def main_position(ids, pad_len=0):
    """**介入の帯の起点＝主位置（組み立て済みの列の最後のトークン）**の添字（正本 `selection.apply`・裁定 D124）。**起点の式はこの一つ**（採否表 P404）。

    ids は組み立て済みのトークン列（chat template を当てたもの）。pad_len は左詰めの詰めの長さ——詰めを入れた列の中でも最終トークンを指す。
    走行器（`run_stageB_local.run_cell`・`capture_resp_mean`）と `scenario_start_index` がこれを呼び、自己検査がこれを独立の正解と照らす。"""
    return int(pad_len) + len(ids) - 1


def scenario_start_index(tokenizer, arm_text, scen_text, instruction, pad_len=0):
    """介入の帯の**起点**＝**主位置（プロンプトの最終トークン）**（正本 `selection.apply`・裁定 D124・2026-09-18）。

    裁定 D124 で帯を「場面本文の開始から」ではなく「主位置から EOS まで」に狭めた。
    抽出した場所と加える場所を一致させるためであり、**狭めて落ちるのは prefill の場面本文の位置だけ**
    （選択が作られる復号の段はすべて掛かる）。
    左詰めのバッチでは、詰めの長さに関わらず**最終トークンは列の最後の位置**にある。
    pad_len は左詰めの詰めの長さ（この式では結果に効かないが、呼び手の意図を明示するために受ける）。
    """
    ids = apply_chat(tokenizer, _user_message(arm_text, scen_text, instruction))
    return main_position(ids, pad_len)


def _user_message(arm_text, scen_text, instruction):
    """凍結走行器 `user_message` と同じ式（正本 `runner.prompt_assembly`）。"""
    t = arm_text or ''
    return (t + '\n\n' + scen_text + instruction) if t else (scen_text + instruction)


def band_starts(tokenizer, arm_texts, scen_text, instruction, pad_lens):
    """バッチの行ごとの起点（`make_hook` に渡す）。

    正本 `selection.batch_composition` により**一つのバッチは一つの場面 × 一つの腕**なので、
    詰めは起きず、全行が同じ起点になる。式は一般のまま置き、器が取り決めを守っているかを
    `assert_batch_uniform` で確かめる。
    """
    return [scenario_start_index(tokenizer, t, scen_text, instruction, p) for t, p in zip(arm_texts, pad_lens)]


def assert_batch_uniform(arm_texts, scenarios=None):
    """**一つのバッチは一つの場面 × 一つの腕**（正本 `selection.batch_composition`・裁定 D124）。"""
    if len(set(arm_texts)) > 1:
        raise SystemExit('バッチに複数の腕が混ざっている（正本 selection.batch_composition・裁定 D124）: %d 種'
                         % len(set(arm_texts)))
    if scenarios is not None and len(set(scenarios)) > 1:
        raise SystemExit('バッチに複数の場面が混ざっている（正本 selection.batch_composition・裁定 D124）: %d 種'
                         % len(set(scenarios)))


def _to_hf(g, greedy):
    """正本の生成の設定を transformers の引数名に写す（説明の欄は落とす・採否表 P286）。"""
    out = {'max_new_tokens': g.get('max_tokens')}
    if greedy:
        out['do_sample'] = False
    else:
        out.update({'do_sample': True, 'temperature': g.get('temperature'), 'top_p': g.get('top_p')})
    return {k: v for k, v in out.items() if v is not None}


def quality_generation():
    """品質床の生成の設定（**貪欲**・正本 quality_floor.generation・裁定 D78）。"""
    g = T['quality_floor']['generation']
    assert g['temperature'] == 0, '品質床は貪欲（temperature 零）でなければならない（裁定 D78）'
    if g.get('max_tokens') is None:      # **黙って落とさない**（裁定 D103・採否表 P328）
        raise SystemExit('品質床の最大トークン数が未定（裁定 D66 と採否表 P216 で決める）。'
                         'このまま実機に渡すと transformers の既定で走り、例外も警告も出ない')
    return _to_hf(g, greedy=True)


def main_generation():
    """場面の試行の生成の設定（正本 runner.generation）。"""
    return _to_hf(T['runner']['generation'], greedy=False)


def score_quality(answer_letter, correct_letter, format_fail):
    """品質床の採点（書式外は不正解に数えて分母を保つ・quality_floor.format_fail_rule）。"""
    if format_fail or not answer_letter:
        return False
    return answer_letter.strip().upper() == correct_letter.strip().upper()


def _selftest():
    rng = np.random.default_rng(3)
    v = rng.normal(size=32)
    nv = float(np.linalg.norm(v))
    # (1) ランダム方向は ‖v̂‖ に合う（係数は掛けない・裁定 D90）
    for ratio in T['selection']['candidates']['layers']:
        rs = random_directions(v, 'main', ratio)
        assert len(rs) == N_RAND
        for r in rs:
            assert abs(float(np.linalg.norm(r)) - nv) < 1e-9, 'ランダム方向のノルムが ‖v̂‖ に合っていない（裁定 D90）'
    # (2) **合成の検査**（裁定 D102・採否表 P309・P311）: 加わる量のノルムが
    #     **全方向（v̂・Nk・td・(6b)・ランダム方向） × 全係数 × 全層**で一致する。
    #     前は v 腕とランダム腕の対しか回さなかったため、交差族と S4 の反証に同じ穴が残った。
    raw = {'Nk': rng.normal(size=32) * 7.0, 'td': rng.normal(size=32) * 0.2, 'loaded': rng.normal(size=32) * 3.5}
    others = {k: match_to_static(w, v) for k, w in raw.items()}      # 方向を作る器が合わせたものを模す
    n_checked = 0
    for coef in T['selection']['candidates']['coefficients']:
        for ratio in T['selection']['candidates']['layers']:
            a_v = np.linalg.norm(apply_vector(np.zeros(32), v, coef, +1))
            cand = dict(others)
            for i, r in enumerate(random_directions(v, 'main', ratio)):
                cand['rand:%d' % i] = r
            for name, w in cand.items():
                a_w = np.linalg.norm(apply_vector(np.zeros(32), w, coef, +1))
                assert abs(a_v - a_w) < 1e-9, ('加わる量が v 腕と %s で違う（係数が二度掛かっていないか）' % name, coef, ratio, a_v, a_w)
                n_checked += 1
    assert n_checked == len(T['selection']['candidates']['coefficients']) * len(T['selection']['candidates']['layers']) * (len(raw) + N_RAND)
    # (3) 合わせる器そのもの
    assert abs(float(np.linalg.norm(match_to_static(rng.normal(size=32) * 7.0, v))) - nv) < 1e-9
    # (4) 引き直し（裁定 D84）と層ごとの子ストリーム（係数は入れない・採否表 P285）
    a1 = random_directions(v, 'tune', 0.5)[0]
    a2 = random_directions(v, 'main', 0.5)[0]
    assert not np.allclose(a1, a2), '調整走行と本走行で引き直していない'
    assert np.allclose(a1, random_directions(v, 'tune', 0.5)[0]), '同じ引数で再現しない'
    assert not np.allclose(random_directions(v, 'main', 0.25)[0], random_directions(v, 'main', 0.75)[0]), '層で子ストリームが分かれていない'
    # (5) 割り当てと、試行の番号から方向へ（**交互**・裁定 D140・再開しても変わらない・採否表 P298）
    for n in (200, 201, 100, 7):
        al = allocate(n)
        assert sum(al) == n and max(al) - min(al) <= 1 and al == sorted(al, reverse=True), '割り当ての端数の配り方が規則と違う'
    n = T['n_main']
    got = [direction_of(i, n) for i in range(n)]
    assert [got.count(i) for i in range(N_RAND)] == allocate(n), '試行から方向への写像が割り当てと合わない'
    assert [direction_of(i, n) for i in range(n // 2, n)] == got[n // 2:], '再開すると方向の割り当てが変わる'
    # **交互であること**を、器を通さずに作った正解（番号を方向の数で割った余り）と照らす——塊に戻すとここで落ちる
    assert got[:2 * N_RAND] == [i % N_RAND for i in range(2 * N_RAND)], ('割り当てが交互でない（裁定 D140）', got[:2 * N_RAND])
    _bt = T['runner']['batch']
    assert all(len({got[j] for j in range(b, min(b + _bt, n))}) == min(N_RAND, min(b + _bt, n) - b) for b in range(0, n, _bt)), \
        'バッチの中に方向が混ざっていない（塊の割り当てに戻っている）'
    # (5b) **帯の起点の関数**（採否表 P404）——器を通さずに作った正解（列の最後の位置）と照らす。詰めを入れても最終トークンを指す
    for ids_ in ([5, 6, 7], [9], list(range(40))):
        assert main_position(ids_) == len(ids_) - 1, ('起点が列の最後でない', ids_[:4], main_position(ids_))
        for pad in (0, 3, 11):
            padded = [0] * pad + list(ids_)
            assert padded[main_position(ids_, pad)] == ids_[-1] and main_position(ids_, pad) == len(padded) - 1, ('詰めを入れると起点がずれる', pad)
    # (6) 加減の向き
    h = rng.normal(size=32)
    assert np.allclose(apply_vector(h, v, 2.0, +1) - h, 2.0 * v)
    assert np.allclose(apply_vector(h, v, 0.5, -1) - h, -0.5 * v)
    # (7) 品質床の採点と生成（transformers の引数名で出す・採否表 P286）
    assert score_quality('A', 'a', False) and not score_quality('A', 'B', False) and not score_quality('A', 'A', True)
    try:
        qg = quality_generation()
    except SystemExit as e:
        qg = None
        assert '最大トークン数' in str(e), '品質床の生成の設定が、別の理由で止まっている: %s' % e
    mg = main_generation()
    if qg is not None:
        assert qg['do_sample'] is False and 'temperature' not in qg, '品質床が貪欲でない'
        assert 'max_new_tokens' in qg, '品質床の最大トークン数が黙って落ちている（裁定 D103）'
    assert set(mg) <= {'do_sample', 'temperature', 'top_p', 'max_new_tokens'}, '生成の設定に transformers が知らない鍵が混ざる'
    assert mg['max_new_tokens'] == T['runner']['generation']['max_tokens'] and mg['temperature'] == T['runner']['generation']['temperature']
        # (8) **帯の起点**（裁定 D101・採否表 P308）: 実トークナイザがあれば、起点のトークンを復号して場面本文の先頭に一致することを確かめる
    band = _selftest_band()
    print('[steer_B selftest] 全方向 × 全係数 × 全層の合成 %d 通り・引き直し・層の子ストリーム・割り当て（交互）と再開・帯の起点の関数・加減の向き・生成の設定・%s: すべて通った'
          % (n_checked, band))


def _selftest_band(model_dir=None):
    """帯の起点の自己検査（正本 `runner.chat_template`・`selection.apply`・裁定 D122）。

    **独立の正解と照らす**（裁定 D122）——起点を求めるのに使った経路とは別に、
    組み立て済みの列を自分で作って最後の位置を取り、二つが一致することを確かめる。
    さらに、その位置のトークンを**復号して**、組み立て済みの列の最終トークンと文字列で一致することを見る。
    左詰めのバッチでも、詰めを入れた列の中で同じ位置が最終トークンを指すことを確かめる。
    前の版は、起点を探すのに使ったトークンでそのまま照合していたので**恒真**だった。
    """
    try:
        from transformers import AutoTokenizer
    except Exception:
        if STRICT:
            raise SystemExit('帯の起点の検査を飛ばした（transformers が無い）——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
        return '帯の起点（**飛ばした**——transformers が無い）'
    src = model_dir or os.environ.get('OP4B_TOKENIZER_DIR')
    if not src:
        if STRICT:
            raise SystemExit('帯の起点の検査を飛ばした（OP4B_TOKENIZER_DIR が無い）——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
        return '帯の起点（**飛ばした**——OP4B_TOKENIZER_DIR が無い）'
    tok = AutoTokenizer.from_pretrained(src)
    scen, inst = '場面の本文がここから始まる。', '\n\n指示。'
    n_ok = 0
    for arm_text in ('前置きがここにある。', ''):
        ids = apply_chat(tok, _user_message(arm_text, scen, inst))
        want = len(ids) - 1                                   # **独立の正解**（器を通さずに作る）
        got = scenario_start_index(tok, arm_text, scen, inst, 0)
        assert got == want, ('起点が独立の正解と違う', arm_text[:8], got, want)
        assert tok.decode([ids[got]]) == tok.decode([ids[-1]]), '起点のトークンが最終トークンでない'
        for pad in (0, 5, 37):                                # 左詰めの詰めを入れても最終トークンを指すか
            padded = [tok.pad_token_id or 0] * pad + ids
            st = scenario_start_index(tok, arm_text, scen, inst, pad)
            assert padded[st] == ids[-1], ('詰めを入れると起点がずれる', pad, st)
        n_ok += 1
    assert_batch_uniform(['a', 'a', 'a'])
    try:
        assert_batch_uniform(['a', 'b'])
        raise AssertionError('腕が混ざったバッチを止めていない（裁定 D124）')
    except SystemExit:
        pass
    return '帯の起点（実トークナイザ・独立の正解と照合・詰め三通り・腕の混在を止めることも確かめた）'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        sys.exit(0)
    sys.exit('この器は GPU の上の走行器から import して使う（手元の検査は --selftest）。'
             '走行の組み立て（場面の本文・hook の登録・バッチ）は走行器 `tools/run_stageB_local.py` の側にある。')
