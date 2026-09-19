# -*- coding: utf-8 -*-
"""direction_B.py v7 —— 段階 B の**方向の抽出**（主位置の活性・方向の作成・決定性の検査・要約統計・v̂ の凍結）。
v7（2026-09-20・凍結の前の方向の抽出の準備・独立の目を通っていない）: **本体を関数 `extract` に切り出した**——起動器（相 dir）と口（`__main__`）が同じものを呼ぶ。これまで口の本体は一度も走っておらず（端から端までの検査は部品の関数だけを呼んでいた）、起動器から実重みで呼ぶ前に小さな模型で通すため。決定性の二条の当て方を `check_determinism` に、**腕ごとのトークン長**（正本 `position_length.record_at_freeze`）を `token_lengths` に置き、自己検査で確かめる。口の使われていなかった引数（--arms-dir・--scenarios-dir——渡しても何も変わらなかった）を外した。
v6（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: 決定性 (ii) を**バッチの組成を変えた比較**にした——走行器と同じ組成（同じプロンプトを `runner.batch` 行）で取った主位置の活性と、一本流しの値を比べる（採否表 P396）。前は腕の並べ方を逆にした一本流しどうしを比べており、行列の形が変わらないので落ちようがなかった。主位置の活性を取る関数を本体の外（`main_position_activation`・`main_position_activation_batch`）に出し、端から端までの検査が同じ関数を呼べるようにした。

正本 `design/contrasts-B.json` の `selection.position`・`selection.candidates`・`directions`・`activation_storage`・`runner` に従う。
何をするか:
  (1) 腕 × 場面のプロンプトを組み、**プロンプトの最終トークン**（詰めでない最後の位置・`runner.padding`）の隠れ状態を、登録した層で取り出す。
  (2) 決定性の検査は二条（裁定 D91）: **同じ並べ方**で二度取って完全一致（外れたら走行を止める）／**バッチの組成を変えて**（走行器と同じ組成）一度取り、許容差の内側かを見る（外れたら記帳して登録者に上げる・採否表 P396）。
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

VERSION = 'v7'
STRICT = os.environ.get('OP4B_REQUIRE_FULL_SELFTEST') == '1'     # 実機の段では飛ばしを失敗に倒す（裁定 D122・採否表 P344）
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


def decoder_layers(model):
    """hook を掛ける層の並びを、**一箇所で**決める（裁定 D117・2026-09-18）。

    抽出器（`hidden_states[idx+1]` を取る）と走行器（`layers[idx]` に hook を掛ける）が**同じ層を指す**ことが要る。
    `hidden_states[idx+1]` は「`layers[idx]` の出力」と等しい——この対応が崩れると、
    **抽出した層と介入した層が違う**まま誰も気づけない（系統内の検分の是認 A3 が「走行器が `layers[i]` に掛けることが条件」と断った箇所）。
    `assert_layer_alignment` で実機のたびに確かめる。
    """
    for path in (('model', 'layers'), ('transformer', 'h'), ('model', 'decoder', 'layers')):
        o = model
        for p in path:
            o = getattr(o, p, None)
            if o is None:
                break
        if o is not None:
            return o
    raise SystemExit('この機種の層の並びを見つけられない（`decoder_layers` に経路を足す）')


def assert_layer_alignment(model, input_ids, attention_mask, layer_idx, atol=0.0):
    """**`hidden_states[idx+1]` が `layers[idx]` の出力と同じ**ことを、実機で確かめる（裁定 D117・D122）。

    恒真にならないよう、hook で実際に受け取ったテンソルと、`output_hidden_states` の該当位置を突き合わせる。
    """
    import torch
    got = {}

    def _h(module, inputs, output):
        got['h'] = (output[0] if isinstance(output, tuple) else output).detach().float().cpu()

    hd = decoder_layers(model)[layer_idx].register_forward_hook(_h)
    try:
        with torch.no_grad():
            out = model(input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=True)
    finally:
        hd.remove()
    hs = out.hidden_states[hidden_states_index(layer_idx)].detach().float().cpu()
    d = float((got['h'] - hs).abs().max())
    assert d <= atol, ('hidden_states[idx+1] と layers[idx] の出力が一致しない（層の対応が崩れている）', layer_idx, d)
    return d


def main_position_activation(model, ids, layer_idx, rows=1):
    """**主位置（プロンプトの最終トークン）**の活性（正本 `selection.position.main`）。同じプロンプトを rows 行並べたバッチで流し、零行目を返す。
    rows=1 は一本流し。バッチの入力は同一なので詰めは起きず、最終トークンは列の最後にある。
    `hidden_states[idx+1]` を取る——`layers[idx]` の出力と同じであることは `assert_layer_alignment` で確かめる。"""
    import torch
    t = torch.tensor([list(ids)] * int(rows), device=model.device)
    am = torch.ones_like(t)
    with torch.no_grad():
        out = model(input_ids=t, attention_mask=am, output_hidden_states=True)
    return out.hidden_states[hidden_states_index(layer_idx)][0, -1, :].detach().float().cpu().numpy()


def main_position_activation_batch(model, ids, layer_idx, rows=None):
    """**走行器と同じバッチの組成**（同じプロンプトを `runner.batch` 行・正本 `selection.batch_composition`）で取った主位置の活性。
    決定性 (ii) は、これと一本流しの値を比べる（採否表 P396）。"""
    batch_rows = int(rows or T['runner']['batch'])
    return main_position_activation(model, ids, layer_idx, batch_rows)


def h_norm_record(H, dirs):
    """**‖v̂‖ と主位置の ‖h‖ の比を層ごとに**（正本 `activation_storage.h_norm_record`・裁定 D127・採否表 P356・2026-09-19）。

    ‖h‖ は抽出場面の前置きの腕の主位置の活性のノルムの平均。係数の格子は ‖v̂‖ に対する比なので、
    ‖v̂‖ が ‖h‖ に比べて小さいと九候補すべてが「何も起きない」域に入りうる——**調整走行の前に登録者に見せる**。"""
    out = {}
    for r in LAYER_RATIOS:
        hn = float(np.mean([np.linalg.norm(H[(arm, sc, r)]) for arm in PANEL for sc in EX if (arm, sc, r) in H]))
        vn = float(np.linalg.norm(dirs[('static', r)]))
        out[str(r)] = {'h_norm_main': hn, 'vhat_norm': vn, 'vhat_over_h': (vn / hn) if hn else None}
    return out


def write_layer_record(out_dir, n_layers, h_norm=None):
    """総層数と層の添字を**記帳**する（正本 `layer_index_rule` が求める・採否表 P283）。‖v̂‖ と ‖h‖ の比も書く（採否表 P356）。"""
    rec = {'num_hidden_layers': n_layers, 'ratios': LAYER_RATIOS,
           'layer_indices': {str(r): layer_index(r, n_layers) for r in LAYER_RATIOS},
           'hidden_states_indices': {str(r): hidden_states_index(layer_index(r, n_layers)) for r in LAYER_RATIOS},
           'h_norm': h_norm}
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
                v = match_norm(v, v_hat)      # **全方向を ‖v̂〔static〕‖ に合わせる**（裁定 D102・採否表 P309・P311）
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
    """**バッチの組成を変えて**取った活性が許容差の内側かを見る（裁定 D91 の (ii)・採否表 P396）。外れたら記帳して登録者に上げる（止めない）。
    名の `cross_order` は前の名残（前は並べ方を変えた一本流しどうしを比べていた）。"""
    tol = tol or T['activation_storage']['determinism']['cross_order_tolerance']
    rows = []
    if set(h1) != set(h2):      # **鍵の欠けを黙って無視しない**（裁定 D114・採否表 P325）
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
    # **`build_directions` の出力そのものを読んで、全方向 × 全層を照合する**（裁定 D122・D102）。
    # 前は td 一本だけを見ていたので、td だけ合わせる誤りに戻しても検査が通った（系統外の検分で捕まった）。
    n_norm = 0
    for ratio in LAYER_RATIOS:
        nv = float(np.linalg.norm(dirs[('static', ratio)]))
        for name in ('Nk', 'td', 'loaded'):
            nw = float(np.linalg.norm(dirs[(name, ratio)]))
            assert abs(nw - nv) < 1e-9, ('方向のノルムが ‖v̂〕に合っていない（裁定 D102）', name, ratio, nw, nv)
            n_norm += 1
    assert n_norm == 3 * len(LAYER_RATIOS), 'ノルムの照合の回数が足りない'
    assert 'raw_norm_ratio' in stats[LAYER_RATIOS[0]], '合わせる前の比が記帳されていない（採否表 P284）'
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
    # 決定性 (ii) バッチの組成を変えた → 許容差（採否表 P396）
    tol = T['activation_storage']['determinism']['cross_order_tolerance']
    Hs = {k: vv + rng.normal(size=d) * 1e-6 for k, vv in H.items()}
    ok5, rows5 = determinism_cross_order(H, Hs)
    assert ok5, ('わずかな差が許容差を外れた', rows5[:1])
    Hb = {k: vv + rng.normal(size=d) * 1.0 for k, vv in H.items()}
    ok6, rows6 = determinism_cross_order(H, Hb)
    assert not ok6, '大きな差を許容差の内側と判定した'
    # 決定性の二条の当て方（v7）: (i) の不一致は止まり、(ii) の外れは止まらずに記帳する
    try:
        check_determinism(H, H2, H)
        raise AssertionError('決定性 (i) の不一致で止まらなかった')
    except SystemExit:
        pass
    ok_s, ok_c, rows_c = check_determinism(H, dict(H), Hb)
    assert ok_s and not ok_c and rows_c, '決定性 (ii) の外れを記帳していない（止まった・または外れを見落とした）'
    # 腕ごとのトークン長（v7）: 前置きの本文だけの数（N は零）と、場面ごとの組み立て済みの列の長さ（手で数えた期待値と照らす）
    class _Tok:
        def __call__(self, t, add_special_tokens=False):
            return {'input_ids': t.split()}
    _AT = {'O': 'a b c', 'N': '', 'Osec': 'a b c d'}
    _SC = ['N1', 'S1', 'SK', 'S4']
    _pid = lambda arm, sc: list(range(len(_AT[arm].split()) + 10 + _SC.index(sc)))
    tl = token_lengths(_Tok(), _AT, _SC, _pid)
    assert tl['N']['preamble_tokens'] == 0 and tl['O']['preamble_tokens'] == 3 and tl['Osec']['preamble_tokens'] == 4, ('前置きのトークン数が違う', tl)
    assert set(tl) == set(_AT) and all(set(v['prompt_tokens']) == set(_SC) for v in tl.values()), ('腕か場面が欠けた', tl)
    assert tl['Osec']['prompt_tokens']['S4'] == 17 and tl['N']['prompt_tokens']['N1'] == 10, ('組み立て済みの列の長さが違う', tl)
    # ‖v̂‖ と ‖h‖ の比（採否表 P356）——器を通さずに一層だけ数え直して照らす
    hr = h_norm_record(H, dirs)
    r0 = LAYER_RATIOS[0]
    hn0 = sum(float(np.sqrt((H[(a_, s_, r0)] ** 2).sum())) for a_ in PANEL for s_ in EX) / (len(PANEL) * len(EX))
    assert abs(hr[str(r0)]['h_norm_main'] - hn0) < 1e-9, ('‖h‖ の記帳が数え直しと違う', hr[str(r0)], hn0)
    assert abs(hr[str(r0)]['vhat_over_h'] - float(np.linalg.norm(dirs[('static', r0)])) / hn0) < 1e-9
    if STRICT:
        try:
            import torch  # noqa: F401  実機の段では torch が要る（層の対応の検査・裁定 D122）
        except ImportError:
            raise SystemExit('torch が無い——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
    print('[direction_B selftest] 層番号（期待値の表・%d 通り）・hidden_states の添字・ノルム合わせ・安定性・‖v̂‖ と ‖h‖ の比・'
          '決定性の二条（同じ並べ方は完全一致／バッチの組成を変えたら cos %g・相対差 %g）・二条の当て方（(i) は止め (ii) は記帳）・腕ごとのトークン長: すべて通った'
          % (len(want), tol['cos_min'], tol['max_abs_over_norm']))


def check_determinism(H1, H2, H3):
    """**決定性の二条**（裁定 D91・正本 `activation_storage.determinism`）を当てる。

    (i) 同じ並べ方で二度取った値（H1・H2）が完全一致でなければ**止める**（SystemExit・登録者に上げる）。
    (ii) バッチの組成を変えた値（H3）は許容差を見て**記帳するだけ**（止めない）。戻り値: (ok_same, ok_cross, rows_cross)。"""
    ok_same, bad_same = determinism_same_order(H1, H2)
    if not ok_same:
        raise SystemExit('決定性 (i)（同じ並べ方で完全一致）に落ちた——走行を止め、登録者に上げる（裁定 D91）: %s' % bad_same[:4])
    ok_cross, rows_cross = determinism_cross_order(H1, H3)
    return ok_same, ok_cross, rows_cross


def token_lengths(tok, arm_text, scenarios, prompt_ids_fn):
    """**腕ごとのトークン長**（正本 `position_length.record_at_freeze`・裁定 D82）。

    前置きの本文だけのトークン数（特別なトークンを付けない・N は零）と、場面ごとの組み立て済みの列の長さ（主位置は列の最後）を返す。
    arm_text: 腕 → 前置きの本文、scenarios: 場面の並び、prompt_ids_fn(arm, sc): 組み立て済みのトークン列。"""
    out = {}
    for arm in sorted(arm_text):
        t = arm_text[arm] or ''
        pre = len(tok(t, add_special_tokens=False)['input_ids']) if t else 0
        out[arm] = {'preamble_tokens': int(pre), 'prompt_tokens': {sc: int(len(prompt_ids_fn(arm, sc))) for sc in scenarios}}
    return out


def extract(model, tok, out_dir, model_label=None, dtype_label=None, log=print):
    """**方向の抽出の本体**（凍結の前・活性だけ・生成しない）。起動器（`tools/colab/boot_stageB.py` の相 dir）と、この器の口（`__main__`）が同じものを呼ぶ。

    (1) 層の対応を実機で確かめる → (2) 活性を三度取る（同じ並べ方で二度・走行器と同じバッチの組成で一度）→ 決定性の二条 →
    (3) 方向を作る（全方向を ‖v̂‖ に合わせる）→ (4) npz と記録を書く（方向・主位置の活性・層・‖v̂‖／‖h‖・腕ごとのトークン長）。
    戻り値: 記録（`directions.json` と同じ中身）。決定性 (i) に落ちたら SystemExit。"""
    import torch
    import steer_B
    import run_stageB_local as RUN
    os.makedirs(out_dir, exist_ok=True)
    n_layers = model.config.num_hidden_layers
    idxs = {r: layer_index(r, n_layers) for r in LAYER_RATIOS}
    AT = {k: v['text'] for k, v in RUN.arm_texts().items()}          # 腕の素材は SHA16 で引き当てる
    PANEL_ARMS = list(T['arms']['panel'])
    EXTRACT = list(T['extraction_scenarios'])

    def prompt_ids(arm, sc):
        """一つの (腕, 場面) の**組み立て済みのトークン列**（正本 `runner.prompt_assembly`・`runner.chat_template`）。"""
        scen, inst = RUN.scenario_and_instruction(sc)
        msg = RUN.user_message(AT[arm], scen['text'], inst)
        return steer_B.apply_chat(tok, msg)

    def collect(order, rows=1):
        """腕 × 場面 × 層の主位置の活性を集める。order は腕の並べ方、rows はバッチの行数（1 は一本流し・決定性の検査に使う）。"""
        H = {}
        for arm in order:
            for sc in EXTRACT:
                ids = prompt_ids(arm, sc)
                for r in LAYER_RATIOS:
                    H[(arm, sc, r)] = (main_position_activation(model, ids, idxs[r]) if rows == 1
                                       else main_position_activation_batch(model, ids, idxs[r], rows))
        return H

    # (1) 層の対応を実機で確かめる（抽出した層と介入する層が同じであること）
    _ids = prompt_ids(PANEL_ARMS[0], EXTRACT[0])
    _t = torch.tensor([_ids], device=model.device)
    align = {str(r): assert_layer_alignment(model, _t, torch.ones_like(_t), idxs[r]) for r in LAYER_RATIOS}
    log('[direction_B] 層の対応を確かめた（hidden_states[idx+1] と layers[idx] の最大差 %s）' % align)

    # (2) 活性を三度取る（決定性の二条・裁定 D91）
    H1 = collect(PANEL_ARMS)
    H2 = collect(PANEL_ARMS)                       # 同じ並べ方
    H3 = collect(PANEL_ARMS, rows=T['runner']['batch'])   # **バッチの組成を変えた**（走行器と同じ組成・採否表 P396）
    ok_same, ok_cross, rows_cross = check_determinism(H1, H2, H3)
    log('[direction_B] 決定性 (i) 完全一致・(ii) バッチの組成（%d 行）を変えた値が許容差の内側 %s' % (T['runner']['batch'], ok_cross))

    # (3) 方向を作る（全方向を ‖v̂〕に合わせる・裁定 D102）
    dirs, stats = build_directions(H1)
    nv = {r: float(np.linalg.norm(dirs[('static', r)])) for r in LAYER_RATIOS}
    for (name, r), v in dirs.items():
        if name != 'static':
            d = abs(float(np.linalg.norm(v)) - nv[r])
            assert d < 1e-6 * max(nv[r], 1.0), ('方向のノルムが ‖v̂〕に合っていない（裁定 D102）', name, r, d)

    # (4) 書き出す（npz・要約統計・層の記帳・トークン長）
    npz = os.path.join(out_dir, 'directions.npz')
    np.savez(npz, **{'%s__%s' % (name, r): v for (name, r), v in dirs.items()})
    sha = hashlib.sha256(open(npz, 'rb').read()).hexdigest().upper()
    # **主位置の活性そのものを保存する**（正本 activation_storage.prompt_final・determinism.material・2026-09-19）
    act = os.path.join(out_dir, 'main_position_activations.npz')
    np.savez(act, **{'same_order__%s__%s__%s' % (arm, sc, r): v for (arm, sc, r), v in H1.items()},
             **{'batch_rows__%s__%s__%s' % (arm, sc, r): v for (arm, sc, r), v in H3.items()})
    act_sha = hashlib.sha256(open(act, 'rb').read()).hexdigest().upper()
    hrec = h_norm_record(H1, dirs)                     # 採否表 P356・調整走行の前に登録者に見せる（見せるだけ・裁定 D141）
    write_layer_record(out_dir, n_layers, hrec)
    tl = token_lengths(tok, {a_: AT[a_] for a_ in PANEL_ARMS}, list(T['scenarios']), prompt_ids)
    log('[direction_B] ‖v̂‖／‖h‖（主位置・層ごと）: %s——**調整走行の前に登録者に見せる・見せるだけで格子は変えない**（正本 activation_storage.h_norm_record・裁定 D141）'
        % {r_: (None if v_['vhat_over_h'] is None else round(v_['vhat_over_h'], 6)) for r_, v_ in hrec.items()})
    rec = {'kind': 'direction_B', 'version': VERSION, 'model': model_label, 'dtype': dtype_label, 'h_norm': hrec,
           'num_hidden_layers': n_layers, 'layer_indices': {str(r): idxs[r] for r in LAYER_RATIOS},
           'alignment_max_abs': align, 'determinism_same_order': bool(ok_same),
           'determinism_cross_order': {'ok': bool(ok_cross), 'rows': rows_cross, 'compared': '一本流し 対 走行器と同じバッチの組成（%d 行）' % T['runner']['batch']},
           'stats': {str(r): stats[r] for r in LAYER_RATIOS}, 'npz_sha256': sha, 'activations_npz_sha256': act_sha,
           'arm_token_lengths': tl, 'arms': PANEL_ARMS, 'extraction_scenarios': EXTRACT,
           'contrasts_sha16': runs_B.sha16_file(runs_B.CPATH)}
    json.dump(rec, open(os.path.join(out_dir, 'directions.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log('[direction_B] 方向を書いた: %s（SHA-256 %s…）' % (npz, sha[:16]))
    log('[direction_B] 総層数 %d・層の添字 %s・合わせる前の比 %s'
        % (n_layers, idxs, {str(r): stats[r].get('raw_norm_ratio') for r in LAYER_RATIOS}))
    return rec


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--model', default='Qwen/Qwen3-4B-Instruct-2507')
    ap.add_argument('--dtype', default='bfloat16')
    ap.add_argument('--out', default=None)
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
    # 置き場を直に渡せるようにする（版を固定し、Hub への問い合わせを避ける・裁定 D115・採否表 P335〔二体目 G8〕）
    tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or a.model)
    tok.padding_side = 'left'                                  # 正本 runner.padding
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=getattr(torch, a.dtype), device_map='auto')
    model.eval()
    rec = extract(model, tok, out_dir, model_label=a.model, dtype_label=a.dtype)
    sys.exit(0 if rec['determinism_cross_order']['ok'] else 2)      # (ii) は止めない条だが、外れたら非零で知らせる（裁定 D91）
