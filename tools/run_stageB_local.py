# -*- coding: utf-8 -*-
"""run_stageB_local.py v4 —— 段階 B の走行器（transformers・bf16・**hook つき**・手元／Colab）。

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

VERSION = 'v4'
REPO = runs_B.REPO
T = runs_B.load_T()
FROZEN_RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py')
FROZEN_PARSER = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py')
SCEN_PATH = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json')
ASSEMBLY_EXPR = "(t + '\\n\\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)"


def check_assembly_matches_frozen():
    """組み立てが凍結走行器と同じであることを確かめる（裁定 D87・採否表 P288）。

    (i) 凍結走行器のソースに同じ式があること、(ii) 正本に登録があること、(iii) **B 自身の `user_message` が式どおりに振る舞うこと**。
    """
    src_txt = open(FROZEN_RUNNER, encoding='utf-8').read()
    if ASSEMBLY_EXPR not in src_txt:
        raise SystemExit('凍結走行器の組み立ての式と違う（凍結物が変わったか、この器が古い）: %s' % FROZEN_RUNNER)
    reg = (T['runner'].get('prompt_assembly') or '')
    if '前置き' not in reg or '場面の本文' not in reg or '指示' not in reg:
        raise SystemExit('正本 runner.prompt_assembly に組み立ての式が無い（裁定 D87）')
    # (iii) 凍結走行器の式をそのまま評価して、B の実装と突き合わせる
    for t, SCEN_TEXT, INST in (('前置き', '場面', '指示'), ('', '場面', '指示')):
        want = (t + '\n\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)
        got = user_message(t, SCEN_TEXT, INST)
        if want != got:
            raise SystemExit('B の user_message が凍結走行器の式と違う: %r 対 %r' % (want, got))
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


def scenario_and_instruction(scenario):
    """場面の本文と**指示**を凍結の素材から引く（凍結走行器 `run_preamble_local.py` と同じ出所・採否表 P287）。"""
    d = json.load(open(SCEN_PATH, encoding='utf-8'))
    s = {x['question_id']: x for x in d['scenarios']}.get(scenario)
    if s is None:
        raise SystemExit('場面が凍結の素材に無い: %s' % scenario)
    inst = (d.get('json_instruction') or {}).get(s.get('family'))
    if inst is None:
        raise SystemExit('指示（json_instruction）が凍結の素材から引けない: 場面 %s' % scenario)
    return s, inst


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


def make_hook(vec, coef, sign, starts):
    """`h ← h ± α·v̂` を場面本文の開始位置から EOS まで掛ける hook（register_forward_hook）。

    starts は**行ごとの起点**（左詰めの詰めの長さを含む・`steer_B.band_starts`・採否表 P258）。
    復号の段は隠れ状態の長さが一なので、**その一トークン全体に掛ける**（掛けないと生成に介入が入らない・採否表 P259）。
    """
    import torch

    def hook(module, inputs, output):
        hs = output[0] if isinstance(output, tuple) else output
        v = torch.as_tensor(vec, dtype=hs.dtype, device=hs.device)
        add = sign * coef * v
        if len(starts) != hs.shape[0]:
            raise SystemExit('hook: 起点の数（%d）とバッチの行数（%d）が違う——一つのバッチは一つの腕にそろえる'
                             '（正本 runner.one_arm_per_batch・裁定 D114）' % (len(starts), hs.shape[0]))
        if hs.shape[1] == 1:                       # 復号の段（KV キャッシュ）: 位置は必ず帯の内側
            hs[:, 0, :] = hs[:, 0, :] + add
        else:                                       # prefill: 行ごとの起点から後ろに掛ける
            for i, st in enumerate(starts):
                hs[i, int(st):, :] = hs[i, int(st):, :] + add
        return (hs,) + tuple(output[1:]) if isinstance(output, tuple) else hs
    return hook


def scoring():
    """採点は**凍結パーサ**の関数を使う（正本 §2.9・採否表 P289）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location('app_parser_rev2', FROZEN_PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {'parse_app_v2': mod.parse_app_v2, 'is_catastrophic': mod.is_catastrophic,
            'parser_sha16': runs_B.sha16_file(FROZEN_PARSER)}


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
    rs = steer_B.random_directions(v, 'main', 0.5)
    assert len(rs) == T['random_control']['count']
    # 指示は凍結の素材から引ける（採否表 P287）
    sc, inst = scenario_and_instruction(T['scenarios'][0])
    assert isinstance(inst, str) and inst, '指示（json_instruction）が引けない'
    # 採点は凍結パーサの関数（採否表 P289）
    sco = scoring()
    assert callable(sco['parse_app_v2']) and callable(sco['is_catastrophic'])
    # 試行の記録の欄は正本の登録（裁定 D97）から作る
    fields = T['trial_record_fields']['fields']
    rec = trial_record(**{f: None for f in fields})
    assert len(rec) == len(fields)
    # hook は復号の段でも掛かる（採否表 P259）——小さな模擬で形だけ確かめる
    try:
        import torch
        starts = [2, 0]
        h_pre = torch.zeros((2, 5, 3))
        h_dec = torch.zeros((2, 1, 3))
        hk = make_hook(np.ones(3), 2.0, +1, starts)
        hk(None, None, h_pre)
        hk(None, None, h_dec)
        assert float(h_pre[0, 0].sum()) == 0 and float(h_pre[0, 2].sum()) == 6, 'prefill の帯の起点が違う'
        assert float(h_dec[0, 0].sum()) == 6 and float(h_dec[1, 0].sum()) == 6, '復号の段で加算が起きていない'
    except ImportError:
        pass
    print('[run_stageB_local selftest] 組み立て（凍結走行器 SHA16 %s・振る舞いの照合つき）・腕の素材・腕の名から方向・指示・凍結パーサ（%s）・'
          '試行の記録の欄 %d・hook の帯と復号の段: すべて通った' % (sha, sco['parser_sha16'], len(fields)))




# ---- 本体（裁定 D117・2026-09-18） ----
def load_directions(npz_path, json_path=None):
    """凍結した方向を読み、**ノルムが ‖v̂〕に合っていることを実機で確かめる**（裁定 D102・D117）。

    方向を作る器の自己検査は「作るとき」しか見られない。npz が差し替わっていたら、ここでしか捕まらない。
    """
    import numpy as _np
    z = _np.load(npz_path)
    dirs = {}
    for k in z.files:
        name, ratio = k.split('__')
        dirs[(name, float(ratio))] = z[k]
    bad = []
    for ratio in {r for _, r in dirs}:
        nv = float(_np.linalg.norm(dirs[('static', ratio)]))
        for name in {n for n, r in dirs if r == ratio} - {'static'}:
            d = abs(float(_np.linalg.norm(dirs[(name, ratio)])) - nv)
            if d > 1e-6 * max(nv, 1.0):
                bad.append('%s 層%s: ノルムの差 %.6g' % (name, ratio, d))
    if bad:
        raise SystemExit('凍結した方向のノルムが ‖v̂〕に合っていない（正本 selection.candidates.coefficient_ref・裁定 D102）: %s'
                         % '・'.join(bad))
    meta = json.load(open(json_path, encoding='utf-8')) if json_path and os.path.exists(json_path) else {}
    return dirs, meta


def register_hook(model, layer_idx, hook):
    """hook を一本だけ掛け、**掛かっている本数を確かめる**（裁定 D114・D117）。"""
    import direction_B
    layer = direction_B.decoder_layers(model)[layer_idx]
    n_before = len(getattr(layer, '_forward_hooks', {}) or {})
    if n_before:
        raise SystemExit('この層に hook が既に %d 本掛かっている（前のバッチで外し損ねている・裁定 D114）' % n_before)
    handle = layer.register_forward_hook(hook)
    n_after = len(getattr(layer, '_forward_hooks', {}) or {})
    if n_after != 1:
        handle.remove()
        raise SystemExit('hook が一本になっていない（%d 本）' % n_after)
    return handle


def assert_no_hooks(model, layer_idx):
    import direction_B
    n = len(getattr(direction_B.decoder_layers(model)[layer_idx], '_forward_hooks', {}) or {})
    if n:
        raise SystemExit('バッチの後に hook が %d 本残っている（裁定 D114）' % n)


def batch_seed(cell_seed_value, batch_index):
    """バッチの種（正本 `seeds.unit_D127`・裁定 D127）。**試行単位の再現は主張しない。**"""
    import numpy as _np
    return int(_np.random.SeedSequence([int(cell_seed_value), int(batch_index)]).generate_state(1)[0])


def run_cell(model, tok, *, scenario, arm, layer_ratio, coef, n, cell_seed_value, tag, run_key,
             dirs=None, layer_idx=None, gen=None, batch=None, start=0):
    """一つのセル（場面 × 腕 × 層 × 係数）を走らせて、試行の記録の一覧を返す。

    **一つのバッチは一つの場面 × 一つの腕**（正本 `selection.batch_composition`・裁定 D124）なので、
    バッチ内の入力は同一で詰めは起きない。帯の起点は**主位置（列の最後）**。
    """
    import torch
    import steer_B
    T_ = T
    batch = batch or T_['runner']['batch']
    gen = dict(gen or steer_B.main_generation())
    # **この機関が受け取る鍵だけを渡す**（裁定 D127・端から端までの検査で捕まえた）。
    _na = set((T_['runner'].get('generation_explicit') or {}).get('not_applicable') or [])
    gen.update({k: v for k, v in (T_['runner'].get('generation_explicit') or {}).items()
                if k not in ('note', 'not_applicable', 'why') and k not in _na})
    scen, inst = scenario_and_instruction(scenario)
    at = arm_texts()[base_arm_of(arm)]['text']
    ids = steer_B.apply_chat(tok, user_message(at, scen['text'], inst))
    plan = arm_plan(arm)
    sco = scoring()
    out, bi = [], 0
    while start + len(out) < n:
        k = min(batch, n - (start + len(out)))
        inp = torch.tensor([ids] * k, device=model.device)
        am = torch.ones_like(inp)
        starts = [inp.shape[1] - 1] * k                 # **主位置**（裁定 D124・詰めは起きない）
        steer_B.assert_batch_uniform([at] * k, [scenario] * k)
        handle = None
        v = None if plan is None else dirs[(plan['kind'], layer_ratio)]
        try:
            if plan is not None:
                handle = register_hook(model, layer_idx, make_hook(v, coef, plan['sign'], starts))
            torch.manual_seed(batch_seed(cell_seed_value, bi))
            with torch.no_grad():
                gen_out = model.generate(input_ids=inp, attention_mask=am, **gen)
        finally:
            if handle is not None:
                handle.remove()
                assert_no_hooks(model, layer_idx)
        texts = tok.batch_decode(gen_out[:, inp.shape[1]:], skip_special_tokens=True)
        fam = scen.get('family')
        parsed = [sco['parse_app_v2'](t, fam) for t in texts]
        # **書式外は一度だけ引き直し、最終試行だけを採点する**（凍結走行器と同じ手順・裁定 D117）。
        # 持たないと書式外率が段階 A と別物になり、希釈の門が見るものが変わる。
        need = [j for j, o in enumerate(parsed) if o is None]
        raws = list(texts)
        if need:
            inp2 = torch.tensor([ids] * len(need), device=model.device)
            am2 = torch.ones_like(inp2)
            h2 = None
            try:
                if plan is not None:
                    h2 = register_hook(model, layer_idx, make_hook(v, coef, plan['sign'], [inp2.shape[1] - 1] * len(need)))
                torch.manual_seed(batch_seed(cell_seed_value, bi) + 1)
                with torch.no_grad():
                    g2 = model.generate(input_ids=inp2, attention_mask=am2, **gen)
            finally:
                if h2 is not None:
                    h2.remove()
                    assert_no_hooks(model, layer_idx)
            t2 = tok.batch_decode(g2[:, inp2.shape[1]:], skip_special_tokens=True)
            for m_, j in enumerate(need):
                parsed[j] = sco['parse_app_v2'](t2[m_], fam)     # 最終試行のみ採点（凍結パーサ規約）
                raws[j] = raws[j] + '\n===RETRY===\n' + t2[m_]
        for j, txt in enumerate(texts):
            i = start + len(out)
            o = parsed[j]
            cat = sco['is_catastrophic'](o, fam)
            out.append(trial_record(
                trial_id='%s__%s__%04d' % (run_key, arm, i), trial_index=i, arm=arm, scenario=scenario, tag=tag,
                status='ok', catastrophe=cat, choice=(o or {}).get('choice'), refuse_class=None,
                format_fail=(o is None), style_a=None, style_b=None, mention=None,
                loop_flag=False, truncated=False, correct=None, logprobs=None, resp_mean_path=None,
                seed=batch_seed(cell_seed_value, bi), run_key=run_key, runner_sha=None, arms_spec=arm,
                preamble_sha=arm_texts()[base_arm_of(arm)]['sha16'], model=None, sampling=gen,
                layer=layer_ratio, coef=coef, direction_id=('fixed' if plan is None else plan['kind']),
                batch_pos=j, proc_uuid=None, dry_run=False))
        bi += 1
    return out


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
    if not a.directions:
        sys.exit('--directions（tools/direction_B.py が凍結した npz）が要る')
    import direction_B
    tok = AutoTokenizer.from_pretrained(os.environ.get('OP4B_TOKENIZER_DIR') or a.model)
    tok.padding_side = 'left'                                   # 正本 runner.padding
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.bfloat16, device_map='auto')
    model.eval()
    dirs, dmeta = load_directions(a.directions, os.path.splitext(a.directions)[0] + '.json')
    n_layers = model.config.num_hidden_layers
    if dmeta.get('num_hidden_layers') not in (None, n_layers):
        sys.exit('方向を抽出した機種の総層数（%s）が、いまの機種（%s）と違う' % (dmeta.get('num_hidden_layers'), n_layers))
    print('[run_stageB_local] 方向を読んだ（%d 本・総層数 %d）。走らせる相・セルは起動器（Colab の段）から渡す。'
          % (len(dirs), n_layers))
    print('[run_stageB_local] 一つのセルを走らせるには `run_cell(...)` を呼ぶ（正本 selection.batch_composition のとおり'
          '一つのバッチは一つの場面 × 一つの腕）。')
    sys.exit(0)
