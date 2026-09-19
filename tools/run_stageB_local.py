# -*- coding: utf-8 -*-
"""run_stageB_local.py v8 —— 段階 B の走行器（transformers・bf16・**hook つき**・手元／Colab）。
v8（2026-09-19 の夕刻・裁定 D145・D146・独立の目を通っていない）: **品質床のセル `run_quality_cell`** を書いた（前は「課題が未定のため」本体が無かった）。問いの本文は `qf_task_B.block`、前置きの付け方は `user_message`（凍結走行器と同じ式・指示の欄は空）、バッチは断片の順に左詰め、貪欲、記号の読み取りは `qf_task_B.extract_letter`、例外のバッチは一度だけ引き直す。試行の記録の生成の設定には正本の温度と top_p を添える（`quality_sampling_record`——渡した鍵だけを書くと本物の出力が整合検査で全件落ちる型）。
v7（2026-09-19 の後刻・独立の目を通っていない）: **腕の本文を凍結走行器の `rd` で読む**（改行を LF にそろえて前後の空白を除く）。v6 までは末尾の改行を残して読み、**O・Osec・Onull で前置きと場面の本文の間の改行が一つ多かった**——段階 A と V′ の列と一字違っていた（Nk の名の確かめ〔裁定 D144〕の途中で見つけた・採否表の外）。起動時の照合に、盤の全腕の本文が凍結走行器の `rd` と一致することを足した。
v6（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: `run_cell` の頭で**層の割合と層の添字の対応**を確かめて止まる（`layer_binding_ok`・採否表 P393）／帯の起点を `steer_B.main_position` から出す（P404）／試行の記録に**バッチの実際の行数** `batch_rows`（P406）／セルの**加えた量** `added_norm` を返す（P394）／`generate` に渡す鍵を正本 `generation_explicit.passed_keys` に限る（裁定 D142 の条を足したため）／自己検査の締めの行が、飛ばした検査を「通った」に数えない（P397）。

段階 A の走行器（`run_preamble_local.py` v2.7・vLLM の OpenAI 互換サーバ）は凍結物なので触らない。
B は hook を掛けるため transformers を直に使うが、**プロンプトの組み立てと採点の経路は凍結物に合わせる**:
  - 組み立て: `前置き + '\\n\\n' + 場面の本文 + 指示`（前置きを持たない N 腕は場面の本文から）。凍結走行器の `user_message` と同じ。
    起動時に凍結走行器のソースに同じ式があることを確かめる（食い違えば止まる）。
  - 採点: 凍結パーサ `arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py` の `parse_app_v2` と `is_catastrophic` を import する。
    書式外は一度だけ引き直し、最終試行だけを採点する（凍結走行器の規約）。
  - **様式 (a)(b)・言及・refuse の分類・ループ・打ち切り**（正本 `response_mode`・v5）: 段階 A の器 `response_mode_A.measure` と、
    凍結走行器の `refuse_class`・`loop_info` を ast で読んで呼ぶ（再実装しない）。**v4 までは、これらを空で書いていた**——
    集計器は空を「該当なし」と数えたので、様式門が実データでは黙って効かなかった（束の前の点検・2026-09-19）。
走行の相（正本 `tags`）: 同一性選別 `idB`／調整走行 `tuneB`／品質床 `stageB-quality`／本走行 `stageB`。
介入（正本 `selection.apply`・`random_control`）: `h ← h ± α·v̂` を**主位置（組み立て済みの列の最後のトークン）から EOS まで**に掛ける（裁定 D124）。
  **ランダム方向の腕は、行ごとに違う方向を掛ける**（`random_control.per_row`・試行の方向は `steer_B.direction_of`・v5）。
  v4 まではこの処理が無く、ランダム方向の腕を呼ぶと止まった——確証のすべての対比の相手が走らなかった。
**副位置の活性**（正本 `activation_storage.response_mean`・裁定 D132・v5）: 調整走行と本走行の試行について、
  最終試行の応答の位置の、候補の各層の出力の平均を、生成と同じ hook を掛けたまま一度の順伝播で取り、セルごとの npz に置く。
**生テキスト**（正本 `trial_record` の最初の欄）: 走行器が返し、置き場に書く（v4 までは返しておらず、raw の本文が空だった）。
詰めは左（`runner.padding`）・バッチは設計定数（`runner.batch`）・生成の設定は `runner.generation`（品質床は `quality_floor.generation`）。
出力: results/<tag>/<run_key>/{manifest.json, trials-<run_key>.jsonl, raw-<run_key>.jsonl, resp-<run_key>.npz} と results/sessions-B/<tag>__s<番号>.json。
用法: python tools/run_stageB_local.py --selftest
      （一つのセルを走らせる口は `run_cell`・品質床は `run_quality_cell`（v8）・書く口は `write_cell`・`write_session`。相をまたいだ順は起動器が渡す——品質床の課題の選定の測定は `tools/colab/boot_stageB.py`）
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, uuid, hashlib, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import runs_B
import steer_B

VERSION = 'v8'
REPO = runs_B.REPO
T = runs_B.load_T()
FROZEN_RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py')
FROZEN_PARSER = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'pipeline', 'app_parser_rev2.py')
SCEN_PATH = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json')
REFUSE_RULES = os.path.join(REPO, 'arms', 'materials-draft', 'hei', 'refuse-rules-v2.json')
ASSEMBLY_EXPR = "(t + '\\n\\n' + SCEN_TEXT + INST) if t else (SCEN_TEXT + INST)"
RUNNER_SHA16 = runs_B.sha16_file(os.path.abspath(__file__))
PROC = str(uuid.uuid4())
STRICT = os.environ.get('OP4B_REQUIRE_FULL_SELFTEST') == '1'     # 実機の段では飛ばしを失敗に倒す（裁定 D122・採否表 P344）
RESP_ROWS = 4       # 副位置を取る順伝播の小分けの行数（数の結果は変えない・メモリのための実装の値）


def frozen_rd():
    """凍結走行器 `run_preamble_local.py` の `rd`（腕の本文の読み方）を **ast で抜き出して**返す（再実装しない・2026-09-19）。
    凍結走行器は腕の本文を `rd` で読み、改行を LF にそろえて前後の空白を除く。B の走行器はこれを使って読む。"""
    import ast as _ast
    src = open(FROZEN_RUNNER, encoding='utf-8').read().replace('\r\n', '\n')
    got = [_ast.get_source_segment(src, n) for n in _ast.parse(src).body if isinstance(n, _ast.FunctionDef) and n.name == 'rd']
    if len(got) != 1:
        raise SystemExit('凍結走行器に腕の本文の読み方 `rd` が一つだけ無い: %d 件' % len(got))
    ns = {}
    exec(compile(got[0], FROZEN_RUNNER, 'exec'), ns)
    return ns['rd']


def check_assembly_matches_frozen():
    """組み立てが凍結走行器と同じであることを確かめる（裁定 D87・採否表 P288）。

    (i) 凍結走行器のソースに同じ式があること、(ii) 正本に登録があること、(iii) **B 自身の `user_message` が式どおりに振る舞うこと**、
    (iv) **盤の全腕の本文が、凍結走行器の `rd` で読んだ本文と同じこと**（v7・2026-09-19——v6 までは末尾の改行を残して読み、
    O・Osec・Onull で前置きと場面の本文の間の改行が一つ多かった）。
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
    # (iv) 腕の本文の読み方（v7）
    rd_ = frozen_rd()
    AT_ = arm_texts()
    bad = [a for a, v in AT_.items() if v['path'] and v['text'] != rd_(os.path.join(REPO, *v['path'].split('/')))]
    if bad:
        raise SystemExit('腕の本文が凍結走行器の rd で読んだ本文と違う（末尾の改行など）: %s' % '・'.join(bad))
    return runs_B.sha16_file(FROZEN_RUNNER)


_RD = None


def arm_texts():
    """正本 `arms.sha16` の SHA16 で腕の素材を引き当てる（手で置き場を書かない）。N は前置きを持たない。"""
    global _RD
    if _RD is None:
        _RD = frozen_rd()
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
                # **本文は凍結走行器の rd で読む**（改行を LF にそろえて前後の空白を除く・v7）。v6 までは末尾の改行を残していた
                found[want[h]] = {'path': os.path.relpath(p, REPO).replace('\\', '/'), 'sha16': h,
                                  'text': _RD(p)}
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


def make_hook(vec, coef, sign, starts, meta=None):
    """`h ← h ± α·v̂` を**主位置から EOS まで**掛ける hook（register_forward_hook・正本 `selection.apply`・裁定 D124）。

    vec は一本（全行に同じ方向）か、**行ごとの方向の行列**（ランダム方向の腕・`random_control.per_row`・v5）。
    starts は**行ごとの起点**（詰めの長さを含む・`steer_B.band_starts`・採否表 P258）。
    復号の段は隠れ状態の長さが一なので、**その一トークン全体に掛ける**（掛けないと生成に介入が入らない・採否表 P259）。
    hook は腕・方向・係数・バッチ番号を `hook.op4b` に持ち、生成の直前に `assert_hooks_exactly` が期待と照らす（裁定 D122・採否表 P345）。
    """
    import torch
    V = np.asarray(vec, dtype=np.float32)
    per_row = V.ndim == 2
    if per_row and V.shape[0] != len(starts):
        raise SystemExit('hook: 行ごとの方向の数（%d）と起点の数（%d）が違う' % (V.shape[0], len(starts)))
    cache = {}

    def hook(module, inputs, output):
        hs = output[0] if isinstance(output, tuple) else output
        if len(starts) != hs.shape[0]:
            raise SystemExit('hook: 起点の数（%d）とバッチの行数（%d）が違う——一つのバッチは一つの腕にそろえる'
                             '（正本 runner.one_arm_per_batch・裁定 D114）' % (len(starts), hs.shape[0]))
        key = (hs.dtype, hs.device)
        if key not in cache:
            cache[key] = sign * coef * torch.as_tensor(V, dtype=hs.dtype, device=hs.device)
        add = cache[key]
        if hs.shape[1] == 1:                       # 復号の段（KV キャッシュ）: 位置は必ず帯の内側
            hs[:, 0, :] = hs[:, 0, :] + add
        else:                                       # prefill: 行ごとの起点から後ろに掛ける
            for i, st in enumerate(starts):
                hs[i, int(st):, :] = hs[i, int(st):, :] + (add[i] if per_row else add)
        return (hs,) + tuple(output[1:]) if isinstance(output, tuple) else hs
    hook.op4b = dict(meta or {}, per_row=per_row, coef=float(coef), sign=int(sign), rows=len(starts))
    return hook


def scoring():
    """採点は**凍結パーサ**の関数を使う（正本 §2.9・採否表 P289）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location('app_parser_rev2', FROZEN_PARSER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {'parse_app_v2': mod.parse_app_v2, 'is_catastrophic': mod.is_catastrophic,
            'parser_sha16': runs_B.sha16_file(FROZEN_PARSER)}


def frozen_text_funcs():
    """凍結走行器 `run_preamble_local.py` から `_norm`・`_any`・`_quoted_segments`・`strip_echo`・`refuse_class`・`_sents`・`loop_info` を
    **ast で抜き出して実行する**（段階 A の `response_mode_A.load_funcs` と同じ型・再実装しない・正本 `response_mode`）。
    refuse の分類の規則（丙）が読めなければ止まる（空の分類を書かない）。"""
    import ast as _ast, unicodedata as _ud
    if not os.path.exists(REFUSE_RULES):
        raise SystemExit('refuse の分類の規則が無い（正本 response_mode.refuse_class）: %s' % REFUSE_RULES)
    RR = json.load(open(REFUSE_RULES, encoding='utf-8'))
    src = open(FROZEN_RUNNER, encoding='utf-8').read().replace('\r\n', '\n')
    tree = _ast.parse(src)
    want = ('_norm', '_any', '_quoted_segments', 'strip_echo', 'refuse_class', '_sents', 'loop_info')
    got = {n.name: _ast.get_source_segment(src, n) for n in tree.body if isinstance(n, _ast.FunctionDef) and n.name in want}
    lack = [w for w in want if w not in got]
    if lack:
        raise SystemExit('凍結走行器に採点の関数が無い: %s' % lack)
    ns = {'re': re, 'unicodedata': _ud, 'RR': RR}
    for name in want:
        exec(compile(got[name], FROZEN_RUNNER, 'exec'), ns)
    ns['refuse_rules_sha16'] = runs_B.sha16_file(REFUSE_RULES)
    return ns


def response_mode_A():
    """段階 A の器 `response_mode_A.measure`（(a)(b)・言及の c1／c2）を import する（正本 `response_mode`・再実装しない）。"""
    import response_mode_A as _rm
    return _rm


def score_text(final_text, fam, finish, sent, sco, TF, RM):
    """一つの試行の**最終試行の本文**を採点する（凍結パーサ・凍結走行器の refuse の分類とループ・段階 A の様式と言及）。

    sent は（system, 前置き, 場面の本文, 指示）——凍結走行器と段階 A の器が strip_echo に渡すのと同じ組（B は system を持たない）。"""
    o = sco['parse_app_v2'](final_text, fam)
    cat = sco['is_catastrophic'](o, fam) if o is not None else None
    choice = (o or {}).get('choice')
    li = TF['loop_info'](final_text or '')
    rc = TF['refuse_class'](final_text or '', choice, finish, li['fired'], sent)
    mf = RM.measure(final_text or '', tuple(RM._norm(x or '') for x in sent))
    return {'parsed': o, 'catastrophe': cat, 'choice': choice, 'refuse_class': rc, 'format_fail': o is None,
            'style_a': bool(mf['a']), 'style_b': bool(mf['b']), 'mention': bool(mf['c1']),
            'mode': {'a': bool(mf['a']), 'b': bool(mf['b']), 'c1': bool(mf['c1']), 'c2': bool(mf['c2'])},
            'loop_flag': bool(li['fired']), 'loop_period': li['period'], 'truncated': finish == 'length'}


def trial_record(**kw):
    """正本 `trial_record` の欄をそろえる（欠けたら止まる）。"""
    need = ['生テキスト', '機械判定（三つ組）', '応答様式 (a)(b)', '検査認識の言及',
            '副位置の活性（応答トークン平均・fp16）', '操作の有無と層・係数', '方向の id', 'seed', 'バッチ位置', '走行キー', 'proc_uuid']
    assert T['trial_record'] == need, '正本の試行の記録の欄が変わった（器を合わせ直す）'
    fields = tuple(T['trial_record_fields']['fields'])
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
    # **品質床の問いの組み立て**（v8・裁定 D138・D146）: 前置き ＋ 空行 ＋ 問いの本文（指示の欄は空）・前置きなしは問いの本文だけ・記録の生成の設定は正本の温度と top_p
    import qf_task_B
    _it = {'id': '0', 'question': '問い', 'choices': ['一', '二', '三', '四'], 'answer': 'B'}
    _bk = qf_task_B.block(_it)
    assert user_message(texts['Onull']['text'], _bk, '') == texts['Onull']['text'] + '\n\n' + _bk and user_message('', _bk, '') == _bk, '品質床の問いの組み立てが式と違う'
    _qs = quality_sampling_record(steer_B.quality_generation())
    assert _qs['temperature'] == T['quality_floor']['generation']['temperature'] and _qs['top_p'] == T['quality_floor']['generation']['top_p'] and _qs.get('do_sample') is False, _qs
    # **腕の本文の末尾に改行が残らない**（v7）——末尾に改行を持つ素材（O・Osec・Onull）でも、前置きと場面の本文の間は空行一つ
    for a_ in ('O', 'Osec', 'Onull'):
        m_ = user_message(texts[a_]['text'], '場面の本文', '\n\n指示')
        assert not texts[a_]['text'].endswith('\n') and texts[a_]['text'] + '\n\n場面の本文' in m_ and '\n\n\n' not in m_, \
            ('前置きと場面の本文の間の改行が凍結走行器と違う', a_)
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
    assert 'batch_rows' in fields, '試行の記録にバッチの行数の欄が無い（採否表 P406）'
    # **層の割合と添字の対応**（採否表 P393）: 器を通さずに書いた期待値の表と照らし、一つずれた添字を止めることを確かめる
    for (ratio_, n_, idx_) in ((0.5, 36, 17), (0.25, 36, 8), (0.75, 34, 25)):
        assert layer_binding_ok(ratio_, idx_, n_) is True, ('正しい添字を拒んだ', ratio_, n_, idx_)
        assert layer_binding_ok(ratio_, idx_ + 1, n_) is False and layer_binding_ok(ratio_, idx_ - 1, n_) is False, ('一つずれた添字を通した', ratio_, n_, idx_)
    # 生成に渡す鍵は正本の一覧だけ（説明の欄を渡さない）
    _ge = T['runner']['generation_explicit']
    assert _ge.get('passed_keys') and all(isinstance(_ge[k], (int, float)) for k in _ge['passed_keys']), '生成に渡す鍵の一覧が無いか、数でない鍵がある'
    # **様式・言及・refuse の分類・ループは段階 A の凍結した関数で決まる**（正本 response_mode・v5）
    TF, RM = frozen_text_funcs(), response_mode_A()
    sent = ('', texts['O']['text'], sc['text'], inst)
    assert sc.get('family') == 'nuclear', '自己検査の見本は場面 N1（nuclear の族）の書式で書いてある'
    j = score_text('{"choice": "b", "amount": null, "escalation": 1, "report_to_operator": null, "reason_summary": "x"}',
                   sc.get('family'), 'stop', sent, sco, TF, RM)
    assert j['style_b'] is True and j['format_fail'] is False and j['choice'] == 'b' and j['catastrophe'] is False, ('JSON 直答が読めない', j)
    rf = score_text('理由を書きます。\n```json\n{"choice": "refuse", "amount": null, "escalation": null, "report_to_operator": null, "reason_summary": "x"}\n```',
                    sc.get('family'), 'stop', sent, sco, TF, RM)
    assert rf['choice'] == 'refuse' and rf['catastrophe'] is None and rf['style_b'] is False and (rf['refuse_class'] or {}).get('route') == 'json_refuse', \
        ('refuse の JSON が読めない', rf)
    p = score_text('お答えできません。' * 3, sc.get('family'), 'stop', sent, sco, TF, RM)
    assert p['style_b'] is False and p['format_fail'] is True and p['refuse_class'], ('散文の分類が空', p)
    lp = score_text('同じ文です。' * 40, sc.get('family'), 'length', sent, sco, TF, RM)
    assert lp['loop_flag'] is True and lp['truncated'] is True, ('ループと打ち切りが立たない', lp)
    # hook は復号の段でも掛かる（採否表 P259）・**行ごとの方向**（v5）——小さな模擬で形を確かめる
    try:
        import torch
    except ImportError:
        if STRICT:
            raise SystemExit('torch が無いので hook の検査を飛ばした——実機の段では失敗に倒す（OP4B_REQUIRE_FULL_SELFTEST=1・裁定 D122）')
        print('[run_stageB_local selftest] hook の検査は**飛ばした**（torch が無い）')
        torch = None
    hook_done = False
    if torch is not None:
        starts = [2, 0]
        h_pre = torch.zeros((2, 5, 3))
        h_dec = torch.zeros((2, 1, 3))
        hk = make_hook(np.ones(3), 2.0, +1, starts)
        hk(None, None, h_pre)
        hk(None, None, h_dec)
        assert float(h_pre[0, 0].sum()) == 0 and float(h_pre[0, 2].sum()) == 6, 'prefill の帯の起点が違う'
        assert float(h_dec[0, 0].sum()) == 6 and float(h_dec[1, 0].sum()) == 6, '復号の段で加算が起きていない'
        V = np.array([[1.0, 0, 0], [0, 1.0, 0]])
        h2 = torch.zeros((2, 4, 3))
        make_hook(V, 1.0, -1, [3, 3])(None, None, h2)
        assert float(h2[0, 3, 0]) == -1 and float(h2[1, 3, 1]) == -1 and float(h2[0, 3, 1]) == 0, '行ごとの方向が行に届いていない'
        assert make_hook(V, 1.0, -1, [3, 3], meta={'arm': 'x'}).op4b['arm'] == 'x', 'hook が中身を持っていない'
        hook_done = True
    # **締めの行は、走らせた検査だけを「通った」に数える**（採否表 P397・v6）。前は torch が無くて hook の検査を飛ばしても
    # 「hook の帯と復号の段と行ごとの方向: すべて通った」と印字していた
    print('[run_stageB_local selftest] 組み立て（凍結走行器 SHA16 %s・振る舞いの照合つき）・腕の素材・腕の名から方向・指示・凍結パーサ（%s）・'
          '試行の記録の欄 %d・層の割合と添字の対応・様式と言及と refuse の分類とループ（段階 A の凍結した関数）%s'
          % (sha, sco['parser_sha16'], len(fields),
             '・hook の帯と復号の段と行ごとの方向: すべて通った' if hook_done else ': 通った。**hook の帯と復号の段と行ごとの方向の検査は飛ばした**（torch が無い）'))


# ---- 本体（裁定 D117・2026-09-18・v5 で 2026-09-19 に直した） ----
def load_directions(npz_path, json_path=None):
    """凍結した方向を読み、**ノルムが ‖v̂〕に合っていることを実機で確かめる**（裁定 D102・D117）。

    方向を作る器の自己検査は「作るとき」しか見られない。npz が差し替わっていたら、ここでしか捕まらない。
    """
    z = np.load(npz_path)
    dirs = {}
    for k in z.files:
        name, ratio = k.split('__')
        dirs[(name, float(ratio))] = z[k]
    bad = []
    for ratio in {r for _, r in dirs}:
        nv = float(np.linalg.norm(dirs[('static', ratio)]))
        for name in {n for n, r in dirs if r == ratio} - {'static'}:
            d = abs(float(np.linalg.norm(dirs[(name, ratio)])) - nv)
            if d > 1e-6 * max(nv, 1.0):
                bad.append('%s 層%s: ノルムの差 %.6g' % (name, ratio, d))
    if bad:
        raise SystemExit('凍結した方向のノルムが ‖v̂〕に合っていない（正本 selection.candidates.coefficient_ref・裁定 D102）: %s'
                         % '・'.join(bad))
    meta = json.load(open(json_path, encoding='utf-8')) if json_path and os.path.exists(json_path) else {}
    return dirs, meta


def layer_binding_ok(layer_ratio, layer_idx, n_layers):
    """**層の割合と層の添字が正本の規則どおりに対応しているか**（正本 `selection.candidates.layer_index_rule`・採否表 P393）。
    `direction_B.layer_index`（抽出器と同じ関数）で割合から添字を作り直し、渡された添字と照らす。"""
    import direction_B
    return int(layer_idx) == direction_B.layer_index(float(layer_ratio), int(n_layers))


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


def assert_hooks_exactly(model, layer_idx, expected):
    """生成の直前に、**全層の hook の集合が期待と同じ**であることを確かめる（裁定 D122・採否表 P345・v5）。

    expected が None なら、どの層にも hook が無いこと。そうでなければ、介入の層にだけ一本あり、その中身（腕・方向・係数・バッチ番号）が期待と同じこと。
    前は「一つのバッチは一つの腕」の検査が行数の一致だけで、前のバッチの hook が残って次も同じ行数、という壊れ方を素通りした。"""
    import direction_B
    for i, L in enumerate(direction_B.decoder_layers(model)):
        hooks = list((getattr(L, '_forward_hooks', {}) or {}).values())
        if expected is not None and i == layer_idx:
            if len(hooks) != 1:
                raise SystemExit('介入の層 %d の hook が %d 本（一本のはず）' % (i, len(hooks)))
            meta = getattr(hooks[0], 'op4b', None) or {}
            diff = {k: (meta.get(k), v) for k, v in expected.items() if meta.get(k) != v}
            if diff:
                raise SystemExit('hook の中身が期待と違う（裁定 D122）: %s' % diff)
        elif hooks:
            raise SystemExit('層 %d に hook が %d 本ある（掛けるべきでない層・裁定 D114）' % (i, len(hooks)))


def batch_seed(cell_seed_value, batch_index):
    """バッチの種（正本 `seeds.unit_D127`・裁定 D127）。**共有の `runs_B.batch_seed` を呼ぶ**（書く側と検べる側で一つ）。"""
    return runs_B.batch_seed(cell_seed_value, batch_index)


def _eos_ids(model, tok):
    g = getattr(model, 'generation_config', None)
    e = getattr(g, 'eos_token_id', None) if g is not None else None
    ids = set(e if isinstance(e, (list, tuple)) else ([e] if e is not None else []))
    for x in (getattr(tok, 'eos_token_id', None), getattr(tok, 'pad_token_id', None)):
        if x is not None:
            ids.add(int(x))
    return ids


def _response(ids_row, eos, max_new):
    """生成した列から応答のトークン（EOS と詰めを除く）と終わり方（stop／length）を取る（凍結走行器の finish と同じ意味）。"""
    ids = [int(t) for t in ids_row]
    for k, t in enumerate(ids):
        if t in eos:
            return ids[:k], 'stop'
    return ids, ('length' if len(ids) >= max_new else 'stop')


def row_vectors(plan, dirs, layer_ratio, trial_indices, n, phase_for_random):
    """行ごとの方向（ランダム方向の腕は `steer_B.direction_of` で試行ごとに割り当てる・正本 `random_control.per_row`・v5）。"""
    if plan is None:
        return None, ['fixed'] * len(trial_indices)
    if plan['kind'] == 'random':
        rs = steer_B.random_directions(dirs[('static', layer_ratio)], phase_for_random, layer_ratio)
        ks = [steer_B.direction_of(i, n) for i in trial_indices]
        return np.stack([rs[k] for k in ks]), ['rand:%d' % k for k in ks]
    v = dirs[(plan['kind'], layer_ratio)]
    return np.stack([v] * len(trial_indices)), [plan['kind']] * len(trial_indices)


def capture_resp_mean(model, prompt_ids, resp_list, layer_idxs, hook_args=None, rows=RESP_ROWS):
    """**副位置の活性**（正本 `activation_storage.response_mean`・裁定 D132）: プロンプトと最終試行の応答をつないだ列を一度だけ順伝播し、
    応答の位置（EOS と詰めを除く）の、各層の出力（`hidden_states[層の添字 + 1]`）の平均を fp16 で返す。
    **介入のある腕は、生成のときと同じ hook（同じ帯・同じ方向・同じ係数）を掛けたまま取る**。左詰めなので位置の番号を明示で渡す。
    応答が空の行は None。"""
    import torch
    out = [None] * len(resp_list)
    P = len(prompt_ids)
    # **出力層（語彙の確率）を通さない本体で取る**——要るのは隠れ状態だけで、語彙の確率は列の長さ × 語彙の数の大きさになる
    # （小さな模型の端から端までの検査が、これで時間切れになった）。層の出力の添字は全体を通した場合と同じ（`hidden_states[層の添字 + 1]`・
    # 最後の層だけは本体が正規化した後の値を返すので、候補の層に最後の層は来ないことを確かめる）。
    core = getattr(model, 'model', None)
    if core is None or not hasattr(core, 'layers'):
        core = model
    n_layers_ = len(getattr(core, 'layers', []) or []) or getattr(getattr(model, 'config', None), 'num_hidden_layers', 0)
    if n_layers_ and any(li >= n_layers_ - 1 for li in layer_idxs):
        raise SystemExit('副位置を取る層に最後の層がある（本体の最後の隠れ状態は正規化の後なので、層の出力と同じでない）: %s' % list(layer_idxs))
    for s0 in range(0, len(resp_list), rows):
        idxs = [j for j in range(s0, min(s0 + rows, len(resp_list))) if resp_list[j]]
        if not idxs:
            continue
        seqs = [list(prompt_ids) + list(resp_list[j]) for j in idxs]
        L = max(len(x) for x in seqs)
        ids = torch.zeros((len(seqs), L), dtype=torch.long, device=model.device)
        am = torch.zeros_like(ids)
        pads = []
        for r, sq in enumerate(seqs):
            pd = L - len(sq)
            pads.append(pd)
            ids[r, pd:] = torch.tensor(sq, dtype=torch.long, device=model.device)
            am[r, pd:] = 1
        pos = (am.cumsum(-1) - 1).clamp(min=0)
        handle = None
        if hook_args is not None:
            starts = [steer_B.main_position(prompt_ids, pads[r]) for r in range(len(seqs))]      # **起点の式は一つ**（採否表 P404）
            handle = register_hook(model, hook_args['layer_idx'],
                                   make_hook(hook_args['vecs'][idxs], hook_args['coef'], hook_args['sign'], starts, meta={'capture': True}))
        try:
            with torch.no_grad():
                o = core(input_ids=ids, attention_mask=am, position_ids=pos, output_hidden_states=True)
        finally:
            if handle is not None:
                handle.remove()
                assert_no_hooks(model, hook_args['layer_idx'])
        for r, j in enumerate(idxs):
            a0 = pads[r] + P
            a1 = a0 + len(resp_list[j])
            out[j] = np.stack([o.hidden_states[li + 1][r, a0:a1, :].float().mean(0).cpu().numpy() for li in layer_idxs]).astype(np.float16)
    return out


def run_cell(model, tok, *, scenario, arm, layer_ratio, coef, n, cell_seed_value, tag, run_key,
             dirs=None, layer_idx=None, gen=None, batch=None, start=0, store_resp=None, resp_layer_idxs=None):
    """一つのセル（場面 × 腕 × 層 × 係数）を走らせて、**試行の記録・生テキスト・副位置の活性**を返す（v5）。

    返り値: {'trials': [...], 'raws': [...], 'resp': {trial_id: 配列}, 'added_norm': 加えた量のノルム（無操作は None）}。
    **頭で層の割合と添字の対応を確かめる**（`layer_binding_ok`・採否表 P393）。
    **一つのバッチは一つの場面 × 一つの腕**（正本 `selection.batch_composition`・裁定 D124）なので、バッチ内の入力は同一で詰めは起きない。
    帯の起点は**主位置（列の最後）**。ランダム方向の腕は行ごとに違う方向を掛ける（`random_control.per_row`）。
    store_resp（既定: 調整走行と本走行）なら副位置の活性を取る。resp_layer_idxs は候補の各層の添字（正本の登録順）。
    """
    import torch
    T_ = T
    batch = batch or T_['runner']['batch']
    gen = dict(gen or steer_B.main_generation())
    # **この機関が受け取る鍵だけを渡す**（裁定 D127・端から端までの検査で捕まえた）。
    # **渡すのは正本 `generation_explicit.passed_keys` の鍵だけ**（説明の欄〔top_k の決め方など・裁定 D142〕を渡さない・v6）
    _ge = T_['runner'].get('generation_explicit') or {}
    _na = set(_ge.get('not_applicable') or [])
    _keys = _ge.get('passed_keys')
    if not _keys:
        raise SystemExit('正本 runner.generation_explicit.passed_keys が無い（generate に渡す鍵の一覧・v6）')
    gen.update({k: _ge[k] for k in _keys if k not in _na})
    max_new = int(gen['max_new_tokens'])
    if store_resp is None:
        store_resp = tag in (T_['tags']['tune'], T_['tags']['main'])
    phase_for_random = 'tune' if tag == T_['tags']['tune'] else 'main'       # 正本 random_control.draw_by_phase
    scen, inst = scenario_and_instruction(scenario)
    fam = scen.get('family')
    AT = arm_texts()
    at = AT[base_arm_of(arm)]['text']
    ids = steer_B.apply_chat(tok, user_message(at, scen['text'], inst))
    plan = arm_plan(arm)
    if plan is not None and (dirs is None or layer_idx is None):
        raise SystemExit('介入の腕 %s には方向と層の添字が要る' % arm)
    # **層の割合と層の添字の対応を、走らせる前に確かめる**（採否表 P393）。介入の層と副位置の層の添字が、割合と総層数から
    # 作り直した値と違えば止まる。前は添字をそのまま受け取り、割合と食い違っていても誰も気づかなかった
    # （記録の `layer` は割合なので、違う層に掛けても記録は正しく見える）
    import direction_B
    _nl = len(direction_B.decoder_layers(model))
    if layer_idx is not None and layer_ratio is not None and not layer_binding_ok(layer_ratio, layer_idx, _nl):
        raise SystemExit('層の割合 %s と層の添字 %s が対応しない（総層数 %d なら添字 %d・正本 layer_index_rule・採否表 P393）'
                         % (layer_ratio, layer_idx, _nl, direction_B.layer_index(float(layer_ratio), _nl)))
    if store_resp and resp_layer_idxs and list(resp_layer_idxs) != [direction_B.layer_index(float(r_), _nl) for r_ in T_['selection']['candidates']['layers']]:
        raise SystemExit('副位置を取る層の添字 %s が、候補の層の割合から作り直した添字と違う（採否表 P393）' % list(resp_layer_idxs))
    # **加えた量**（係数 × ‖v̂〔static〕‖・その層・採否表 P394）——全方向を ‖v̂‖ に合わせてあるので、ランダム方向の行も同じ量
    added_norm = None if plan is None else float(coef) * float(np.linalg.norm(dirs[('static', layer_ratio)]))
    sco, TF, RM = scoring(), frozen_text_funcs(), response_mode_A()
    sent = ('', at, scen['text'], inst)
    eos = _eos_ids(model, tok)
    model_name = getattr(getattr(model, 'config', None), '_name_or_path', None)
    trials, raws, resp = [], [], {}
    done = 0
    # **バッチの区切りはセルの頭（試行の番号 零）から数えた倍数**（正本 `seeds.unit_D127`・`runs_B.recorded_seed`）。
    # 中断して途中から再開しても、同じ試行は同じバッチの番号に属し、同じ種を持つ。
    while start + done < n:
        i0 = start + done
        bi = i0 // batch
        k = min((bi + 1) * batch, n) - i0
        tidx = list(range(i0, i0 + k))
        V, dir_ids = row_vectors(plan, dirs, layer_ratio, tidx, n, phase_for_random)
        inp = torch.tensor([ids] * k, device=model.device)
        am = torch.ones_like(inp)
        starts = [steer_B.main_position(ids)] * k       # **主位置**（裁定 D124・詰めは起きない・起点の式は一つ——採否表 P404）
        steer_B.assert_batch_uniform([at] * k, [scenario] * k)
        expected = None if plan is None else {'arm': arm, 'kind': plan['kind'], 'coef': float(coef), 'batch_index': bi}

        def _gen(n_rows, seed_value, vecs, row_starts):
            h = None
            try:
                if plan is not None:
                    h = register_hook(model, layer_idx, make_hook(vecs, coef, plan['sign'], row_starts,
                                                                  meta={'arm': arm, 'kind': plan['kind'], 'batch_index': bi}))
                assert_hooks_exactly(model, layer_idx if plan is not None else -1, expected)
                torch.manual_seed(seed_value)
                x = torch.tensor([ids] * n_rows, device=model.device)
                with torch.no_grad():
                    return model.generate(input_ids=x, attention_mask=torch.ones_like(x), **gen)
            finally:
                if h is not None:
                    h.remove()
                    assert_no_hooks(model, layer_idx)
        g1 = _gen(k, batch_seed(cell_seed_value, bi), V, starts)
        P = inp.shape[1]
        first = [_response(g1[j, P:], eos, max_new) for j in range(k)]
        texts1 = [tok.decode(r_, skip_special_tokens=True) for r_, _ in first]
        final_ids = [r_ for r_, _ in first]
        finish = [f_ for _, f_ in first]
        final_text = list(texts1)
        raw_all = list(texts1)
        parsed1 = [sco['parse_app_v2'](t, fam) for t in texts1]
        # **書式外は一度だけ引き直し、最終試行だけを採点する**（凍結走行器と同じ手順・裁定 D117）。
        # 引き直しの種は `runs_B.retry_seed`（正本 seeds.derivation_formula・v5 まで器の中に手書きしていた）。
        need = [j for j, o in enumerate(parsed1) if o is None]
        if need:
            V2 = None if V is None else V[need]
            g2 = _gen(len(need), runs_B.retry_seed(cell_seed_value, bi), V2, [steer_B.main_position(ids)] * len(need))
            for m_, j in enumerate(need):
                r2, f2 = _response(g2[m_, P:], eos, max_new)
                t2 = tok.decode(r2, skip_special_tokens=True)
                final_ids[j], finish[j], final_text[j] = r2, f2, t2
                raw_all[j] = raw_all[j] + '\n===RETRY===\n' + t2
        # **副位置の活性**（裁定 D132）——生成と同じ hook を掛けたまま、最終試行の応答で一度だけ順伝播する
        rm = [None] * k
        if store_resp:
            lidx = resp_layer_idxs or []
            if not lidx:
                raise SystemExit('副位置を取る層の添字が要る（resp_layer_idxs・正本 selection.candidates.layers の登録順）')
            hook_args = None if plan is None else {'layer_idx': layer_idx, 'vecs': V, 'coef': coef, 'sign': plan['sign']}
            rm = capture_resp_mean(model, ids, final_ids, lidx, hook_args)
        for j in range(k):
            i = tidx[j]
            s_ = score_text(final_text[j], fam, finish[j], sent, sco, TF, RM)
            tid = '%s__%s__%04d' % (run_key, arm, i)
            if rm[j] is not None:
                resp[tid] = rm[j]
            trials.append(trial_record(
                trial_id=tid, trial_index=i, arm=arm, scenario=scenario, tag=tag,
                status='ok', catastrophe=s_['catastrophe'], choice=s_['choice'], refuse_class=s_['refuse_class'],
                format_fail=s_['format_fail'], style_a=s_['style_a'], style_b=s_['style_b'], mention=s_['mention'],
                loop_flag=s_['loop_flag'], truncated=s_['truncated'], correct=None,
                resp_mean_path=(('resp-%s.npz#%s' % (run_key, tid)) if rm[j] is not None else None),
                seed=runs_B.recorded_seed(T_, cell_seed_value, i), run_key=run_key, runner_sha=RUNNER_SHA16, arms_spec=arm,
                preamble_sha=AT[base_arm_of(arm)]['sha16'], model=model_name, sampling=gen,
                layer=layer_ratio, coef=coef, direction_id=dir_ids[j],
                batch_pos=j, batch_rows=k, proc_uuid=PROC, dry_run=False))     # **バッチの実際の行数**（採否表 P406）
            raws.append({'trial_id': tid, 'text': raw_all[j], 'final': final_text[j], 'finish': finish[j],
                         'mode': s_['mode'], 'loop_period': s_['loop_period'], 'retry': j in need})
        done += k
    return {'trials': trials, 'raws': raws, 'resp': resp, 'added_norm': added_norm}


def quality_sampling_record(gen):
    """品質床の試行の記録に書く生成の設定（v8）。`generate` に渡すのは貪欲の鍵（温度を渡さない）だが、記録には正本
    `quality_floor.generation` の温度と top_p を添える——整合検査は記録の温度と top_p を正本の値と照らすので、
    渡した鍵だけを書くと**本物の出力が全件「生成の設定が登録と違う」に落ちる**（合成データは正本の値を書くので通る型）。"""
    g0 = T['quality_floor']['generation']
    return dict(gen, temperature=g0['temperature'], top_p=g0['top_p'])


def run_quality_cell(model, tok, *, items, arm, stage, task, cell_seed_value, tag, run_key, layer_ratio=None, coef=None,
                     dirs=None, layer_idx=None, input_form='with_preamble', batch=None, start=0):
    """品質床の一つのセル（段 × 腕 × 層 × 係数・一つの課題の断片）を走らせて、試行の記録と生テキストを返す（v8・裁定 D146・2026-09-19）。

    items は `qf_task_B.fragment` の返り値（提示の順）。**バッチは断片の順に `runner.batch` 問ずつ前から詰め、左詰め**（`quality_floor.batching`）。
    一つのバッチは一つの腕（裁定 D114）。帯の起点は行ごとの主位置（左詰めなので列の最後の位置・`steer_B.main_position`）。生成は貪欲（`quality_floor.generation`）。
    input_form は 'with_preamble'（土台の前置き ＋ 空行 ＋ 問いの本文・裁定 D138）か 'without_preamble'（問いの本文だけ・判定の順の戻る枝・裁定 D145）。
    例外で落ちたバッチは同じ組で一度だけ引き直し、なお落ちればその行を api_error にする（器の番人の SystemExit は止める）。
    記録（`trial_record_scope`）: 答えの記号は `choice`、正誤は `correct`、書式外は `format_fail`。場面にだけ意味のある欄は空。
    返り値: {'trials': [...], 'raws': [...], 'added_norm': 加えた量のノルム（無操作は None）}。
    """
    import torch
    import qf_task_B
    T_ = T
    if input_form not in ('with_preamble', 'without_preamble'):
        raise SystemExit('品質床の問いの出し方が登録に無い: %s' % input_form)
    batch = batch or T_['runner']['batch']
    gen = dict(steer_B.quality_generation())
    _ge = T_['runner'].get('generation_explicit') or {}
    _na = set(_ge.get('not_applicable') or [])
    _keys = _ge.get('passed_keys')
    if not _keys:
        raise SystemExit('正本 runner.generation_explicit.passed_keys が無い（generate に渡す鍵の一覧・v6）')
    gen.update({k: _ge[k] for k in _keys if k not in _na})
    max_new = int(gen['max_new_tokens'])
    plan = arm_plan(arm)
    if plan is not None and (dirs is None or layer_idx is None):
        raise SystemExit('介入の腕 %s には方向と層の添字が要る' % arm)
    import direction_B
    _nl = len(direction_B.decoder_layers(model))
    if layer_idx is not None and layer_ratio is not None and not layer_binding_ok(layer_ratio, layer_idx, _nl):
        raise SystemExit('層の割合 %s と層の添字 %s が対応しない（総層数 %d なら添字 %d・正本 layer_index_rule・採否表 P393）'
                         % (layer_ratio, layer_idx, _nl, direction_B.layer_index(float(layer_ratio), _nl)))
    added_norm = None if plan is None else float(coef) * float(np.linalg.norm(dirs[('static', layer_ratio)]))
    AT = arm_texts()
    base = base_arm_of(arm)
    at = AT[base]['text'] if input_form == 'with_preamble' else ''
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id
    if pad_id is None:
        raise SystemExit('トークナイザに詰めのトークンが無い（左詰めにできない）')
    eos = _eos_ids(model, tok)
    model_name = getattr(getattr(model, 'config', None), '_name_or_path', None)
    rec_sampling = quality_sampling_record(gen)
    n = len(items)
    trials, raws = [], []
    done = 0
    # **バッチの区切りは断片の頭（試行の番号 零）から数えた倍数**（場面の試行と同じ・再開しても同じ問いは同じバッチに入る）
    while start + done < n:
        i0 = start + done
        bi = i0 // batch
        k = min((bi + 1) * batch, n) - i0
        tidx = list(range(i0, i0 + k))
        its = [items[i] for i in tidx]
        rows = [steer_B.apply_chat(tok, user_message(at, qf_task_B.block(it), '')) for it in its]
        P = max(len(r_) for r_ in rows)
        pads = [P - len(r_) for r_ in rows]
        inp = torch.full((k, P), int(pad_id), dtype=torch.long, device=model.device)
        am = torch.zeros_like(inp)
        for r_, (row, pd) in enumerate(zip(rows, pads)):
            inp[r_, pd:] = torch.tensor(row, dtype=torch.long, device=model.device)
            am[r_, pd:] = 1
        starts = [steer_B.main_position(row, pd) for row, pd in zip(rows, pads)]      # **主位置**（左詰めなので全行が列の最後・起点の式は一つ）
        if any(s_ != P - 1 for s_ in starts):
            raise SystemExit('左詰めの主位置が列の最後にない: %s（正本 runner.padding）' % starts)
        V, dir_ids = row_vectors(plan, dirs, layer_ratio, tidx, n, 'main')            # 品質床は main の方向（§2.8 の相ごとの方向）
        expected = None if plan is None else {'arm': arm, 'kind': plan['kind'], 'coef': float(coef), 'batch_index': bi}

        def _gen():
            h = None
            try:
                if plan is not None:
                    h = register_hook(model, layer_idx, make_hook(V, coef, plan['sign'], starts,
                                                                  meta={'arm': arm, 'kind': plan['kind'], 'batch_index': bi}))
                assert_hooks_exactly(model, layer_idx if plan is not None else -1, expected)
                torch.manual_seed(batch_seed(cell_seed_value, bi))
                with torch.no_grad():
                    return model.generate(input_ids=inp, attention_mask=am, pad_token_id=int(pad_id), **gen)
            finally:
                if h is not None:
                    h.remove()
                    assert_no_hooks(model, layer_idx)
        g, err = None, None
        for _attempt in (1, 2):                    # **一度だけ引き直す**（quality_floor.format_fail_rule・batching）
            try:
                g = _gen()
                break
            except Exception as e:                 # 器の番人（SystemExit）はここを通らずに止まる
                err = '%s: %s' % (type(e).__name__, str(e)[:160])
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
        for j in range(k):
            i, it = tidx[j], its[j]
            if g is not None:
                resp, fin = _response(g[j, P:], eos, max_new)
                text = tok.decode(resp, skip_special_tokens=True)
                letter = qf_task_B.extract_letter(text, qf_task_B.letters_of(it))
                ff = letter is None
                correct = steer_B.score_quality(letter, it['answer'], ff)
                status = 'ok'
            else:
                text, fin, letter, ff, correct, status = None, None, None, None, None, 'api_error'
            tid = '%s__%s__%04d' % (run_key, arm, i)
            trials.append(trial_record(
                trial_id=tid, trial_index=i, arm=arm, scenario=task, tag=tag, status=status,
                catastrophe=None, choice=letter, refuse_class=None, format_fail=ff, style_a=None, style_b=None, mention=None,
                loop_flag=None, truncated=(None if fin is None else fin == 'length'), correct=correct, resp_mean_path=None,
                layer=layer_ratio, coef=coef, direction_id=dir_ids[j], seed=runs_B.recorded_seed(T_, cell_seed_value, i),
                batch_pos=j, batch_rows=k, run_key=run_key, proc_uuid=PROC, runner_sha=RUNNER_SHA16, arms_spec=arm,
                preamble_sha=(AT[base]['sha16'] if input_form == 'with_preamble' else None), model=model_name, sampling=rec_sampling,
                dry_run=False))
            raws.append({'trial_id': tid, 'item_id': it['id'], 'text': text, 'finish': fin, 'error': err if g is None else None,
                         'stage': stage, 'input_form': input_form})
        done += k
    return {'trials': trials, 'raws': raws, 'added_norm': added_norm}


def manifest_env(model, tok):
    """manifest の環境の欄のうち、走行器が知っているもの（正本 `runner.manifest_fields.common`・v5）。残り（セッション・時刻・pip の SHA など）は起動器が足す。"""
    import transformers
    cfg = getattr(model, 'config', None)
    return {'model': getattr(cfg, '_name_or_path', None), 'model_rev': getattr(cfg, '_commit_hash', None),
            'tokenizer_rev': getattr(tok, 'init_kwargs', {}).get('_commit_hash') or getattr(tok, 'name_or_path', None),
            'dtype': T['runner']['dtype'], 'order': T['runner']['order_id'], 'padding': 'left', 'batch': T['runner']['batch'],
            'transformers_version': transformers.__version__, 'refuse_rules_sha16': runs_B.sha16_file(REFUSE_RULES),
            'runner_sha': RUNNER_SHA16}


def write_cell(out_root, tag, run_key, manifest, trials, raws=None, resp=None):
    """一つの走行の記録を**置き場に書く**（裁定 D117・2026-09-19）。

    置き方は合成データ（`synth_B.write_run`）と同じにし、読み口（`runs_B`）と整合検査がそのまま読めるようにする。
    **既にある置き場には書かない**（上書きで記録を失わない）。生テキストと副位置の活性も書く（v5）。
    """
    import datetime as _dt
    d = os.path.join(out_root, tag, run_key)
    if os.path.exists(os.path.join(d, 'manifest.json')):
        raise SystemExit('既に記録がある（上書きしない）: %s' % d)
    os.makedirs(d, exist_ok=True)
    phase = next(k for k, v in T['tags'].items() if v == tag)
    need = list((T['runner'].get('manifest_fields') or {}).get('common', [])) + \
        list((T['runner'].get('manifest_fields') or {}).get(phase, []))
    missing = [k for k in need if k not in manifest]
    if missing:
        raise SystemExit('manifest に正本の欄が無い（正本 runner.manifest_fields）: %s' % '・'.join(missing))
    if raws is not None and len(raws) != len(trials):
        raise SystemExit('生テキストの行数（%d）が試行の数（%d）と違う' % (len(raws), len(trials)))
    json.dump(dict(manifest, written=_dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')),
              open(os.path.join(d, 'manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(d, 'trials-%s.jsonl' % run_key), 'w', encoding='utf-8', newline='\n') as f:
        for t in trials:
            f.write(json.dumps(t, ensure_ascii=False) + '\n')
    with open(os.path.join(d, 'raw-%s.jsonl' % run_key), 'w', encoding='utf-8', newline='\n') as f:
        for t, r in zip(trials, raws or [None] * len(trials)):
            f.write(json.dumps(r if isinstance(r, dict) else {'trial_id': t['trial_id'], 'text': r}, ensure_ascii=False) + '\n')
    if resp:
        np.savez(os.path.join(d, 'resp-%s.npz' % run_key), **resp)
    return d


def write_session(out_root, tag, session, run_keys, extra=None):
    """セッション記録を書く（正本 `sessions.record`・`sessions.fields`）。門・集計器・整合検査が読む（裁定 D126）。"""
    d = os.path.join(out_root, 'sessions-B')
    os.makedirs(d, exist_ok=True)
    rec = dict({'tag': tag, 'session': int(session), 'run_keys': list(run_keys), 'batch': T['runner']['batch']}, **(extra or {}))
    p = os.path.join(d, '%s__s%d.json' % (tag, int(session)))
    if os.path.exists(p):
        old = json.load(open(p, encoding='utf-8'))
        rec['run_keys'] = sorted(set(old.get('run_keys', [])) | set(rec['run_keys']))
    json.dump(rec, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return p


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
    print('[run_stageB_local] 方向を読んだ（%d 本・総層数 %d）。走らせる相・セルは起動器（まだ書いていない）から渡す。'
          % (len(dirs), n_layers))
    print('[run_stageB_local] 一つのセルを走らせるには `run_cell(...)` を呼ぶ（正本 selection.batch_composition のとおり'
          '一つのバッチは一つの場面 × 一つの腕）。')
    sys.exit(0)
