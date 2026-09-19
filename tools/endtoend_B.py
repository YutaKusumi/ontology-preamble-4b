# -*- coding: utf-8 -*-
"""endtoend_B.py v5 —— 走行器と抽出器の本体を、**小さな模型で端から端まで通す**（裁定 D117・2026-09-18）。
v5（2026-09-19 の夕刻・裁定 D145・D146）: **品質床のセル** `run_quality_cell` を (13) で通す——問いの組み立て（前置きあり・なし）・係数 0 の hook と無操作の一致（左詰めのバッチ）・係数 ≠ 0 で出力が変わる・記号と書式外と正誤が生テキストから組み直せる・生成の設定の記録・例外の引き直しと api_error・本物の整合検査に通す（問いは合成）。
v4（2026-09-19 の後刻）: 盤の全腕で、組み立て済みの列が凍結走行器の読み方（`rd`）と式で作った列と一致することを足した（走行器 v6 までの末尾の改行の欠陥の型）。
v3（2026-09-19・最後の系統外の巡の後・独立の目を通っていない）: 試行の記録のバッチの行数（採否表 P406）・走行の記録の加えた量（P394）・層の割合と添字の食い違いで走行器が止まること（P393）・決定性 (ii) のバッチの組成の比較（P396）・ランダム方向の交互の割り当て（裁定 D140）を足した。

系統の外への検分で、四票すべてが「**介入を掛けて走らせる器がまだ無い**」ことを最初に挙げた。
本体を書いたので、**実重みが無くても通せるところまで通す**——
ランダム初期化の小さな Qwen3 形（層が少なく隠れ次元も小さい）で、
方向の抽出 → 凍結 → 読み込み → hook → 生成 → 採点 → 記録の書き出しを一本の流れで走らせる。

確かめること（いずれも**恒真にならない形**で・裁定 D122）:
  (1) `hidden_states[idx+1]` が `layers[idx]` の出力と一致する（抽出した層と介入する層が同じ）。
  (2) 係数 0 の hook を掛けた生成が、hook 無しと**一致**する（hook そのものが結果を壊していない）。
  (3) 係数 ≠ 0 で、**prefill の主位置**と**復号の各段**に、狙いどおりの量が加わる。
  (4) hook はバッチの後に**零本**になる（`finally` で外す）。
  (5) 腕が混ざったバッチは**止まる**。
  (6) 凍結した方向のノルムが崩れていたら、走行器が**読み込みの時点で止まる**。
  (7) 試行の記録が正本の欄をそろえている。
  (8) 走行器の出力を置き場に書き、本物の整合検査に通す（種・再開）。
  (9) v2（2026-09-19・束の前の点検で見つけた穴）: **すべての種類の腕**を走らせる（前は無操作と +v の二腕だけで、
      ランダム方向の腕が走らないことに気づかなかった）。ランダム方向の行ごとの割り当て・hook の中身の照合・
      様式と言及と refuse の分類とループが段階 A の凍結した関数と一致・生テキストの書き出し・副位置の活性。
**実重みでは何も確かめていない。** 模型は乱数で初期化したもので、率にも活性にも意味は無い。
出力: records/B/endtoend-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/endtoend_B.py [--force] [--layers 4] [--hidden 64]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, tempfile, shutil

VERSION = 'v5'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE)

ap = argparse.ArgumentParser()
ap.add_argument('--layers', type=int, default=4)
ap.add_argument('--hidden', type=int, default=64)
ap.add_argument('--out', default=None)
ap.add_argument('--force', action='store_true')
a = ap.parse_args()

try:
    import torch
    import numpy as np
    from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
except Exception as e:
    sys.exit('torch／transformers が無い: %s' % e)

import runs_B, steer_B, direction_B
import run_stageB_local as RUN

T = runs_B.load_T()
SNAP = os.environ.get('OP4B_TOKENIZER_DIR')
if not SNAP:
    sys.exit('OP4B_TOKENIZER_DIR に、登録機種のトークナイザの置き場を渡す（実重みは要らない）')

now = datetime.datetime.now(datetime.timezone.utc)
jst = now.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
out_md = a.out or os.path.join(REPO, 'records', 'B', 'endtoend-B-%s.md' % jst.strftime('%Y-%m-%d'))
out_json = os.path.splitext(out_md)[0] + '.json'
if not a.force:
    for p in (out_md, out_json):
        if os.path.exists(p):
            sys.exit('既にある（--force で上書き）: %s' % p)

checks, fails = [], 0


def check(name, ok, detail):
    global fails
    checks.append({'name': name, 'ok': bool(ok), 'detail': str(detail)[:220]})
    if not ok:
        fails += 1
    print('  %-44s %s  %s' % (name, '通った' if ok else '**落ちた**', str(detail)[:90]))


# ---- 小さな模型（乱数で初期化・実重みではない） ----
tok = AutoTokenizer.from_pretrained(SNAP)
tok.padding_side = 'left'
cfg = AutoConfig.from_pretrained(SNAP)
cfg.num_hidden_layers = a.layers
cfg.hidden_size = a.hidden
cfg.intermediate_size = a.hidden * 2
cfg.num_attention_heads = max(2, a.hidden // 32)
cfg.num_key_value_heads = cfg.num_attention_heads
torch.manual_seed(11)
model = AutoModelForCausalLM.from_config(cfg)
# **float32 に明示で揃える**（2026-09-19）。実物の設定を読んで作ると設定の dtype（bf16）になる版があり、
# 「小さな模型は float32」を前提に置いた (8e) の期待が版によって変わった。小さな模型の数の照合（9g・9h）も float32 のほうが確か。
model = model.float()
model.eval()
n_layers = model.config.num_hidden_layers
ratios = T['selection']['candidates']['layers']
idxs = {r: direction_B.layer_index(r, n_layers) for r in ratios}
print('[endtoend_B] 小さな模型: 層 %d・隠れ次元 %d・層の添字 %s' % (n_layers, cfg.hidden_size, idxs))

AT = {k: v['text'] for k, v in RUN.arm_texts().items()}
scen, inst = RUN.scenario_and_instruction(T['scenarios'][0])
ids = steer_B.apply_chat(tok, RUN.user_message(AT['O'], scen['text'], inst))
inp = torch.tensor([ids])
am = torch.ones_like(inp)

# (1) 層の対応
try:
    d = direction_B.assert_layer_alignment(model, inp, am, idxs[ratios[0]])
    check('(1) hidden_states[idx+1] ＝ layers[idx] の出力', True, '最大差 %g' % d)
except AssertionError as e:
    check('(1) hidden_states[idx+1] ＝ layers[idx] の出力', False, e)

# ---- 方向を作る（抽出器と同じ経路で・小さな模型の活性から） ----
def act(arm, sc, ratio):
    s_, i_ = RUN.scenario_and_instruction(sc)
    t = torch.tensor([steer_B.apply_chat(tok, RUN.user_message(AT[arm], s_['text'], i_))])
    with torch.no_grad():
        o = model(input_ids=t, attention_mask=torch.ones_like(t), output_hidden_states=True)
    return o.hidden_states[direction_B.hidden_states_index(idxs[ratio])][0, -1, :].detach().float().numpy()


H = {(arm, sc, r): act(arm, sc, r) for arm in T['arms']['panel'] for sc in T['extraction_scenarios'] for r in ratios}
dirs, stats = direction_B.build_directions(H)
tmp = tempfile.mkdtemp(prefix='e2eB_')
npz = os.path.join(tmp, 'directions.npz')
np.savez(npz, **{'%s__%s' % (n, r): v for (n, r), v in dirs.items()})

# (6) ノルムが崩れた npz は読み込みで止まる
bad_npz = os.path.join(tmp, 'bad.npz')
bad = {('%s__%s' % (n, r)): (v * 2.0 if n == 'Nk' else v) for (n, r), v in dirs.items()}
np.savez(bad_npz, **bad)
try:
    RUN.load_directions(bad_npz)
    check('(6) ノルムの崩れた方向を読み込みで止める', False, '止まらなかった')
except SystemExit as e:
    check('(6) ノルムの崩れた方向を読み込みで止める', True, str(e)[:80])
loaded, _ = RUN.load_directions(npz)
check('(6b) 正しい方向は読める', len(loaded) == len(dirs), '%d 本' % len(loaded))

# (2)(3) hook の効き目
ratio = ratios[0]
li = idxs[ratio]
v = loaded[('static', ratio)]
gen = {'do_sample': False, 'max_new_tokens': 4}


def gen_once(coef, sign=+1):
    h = None
    if coef is not None:
        h = RUN.register_hook(model, li, RUN.make_hook(v, coef, sign, [inp.shape[1] - 1]))
    try:
        torch.manual_seed(5)
        with torch.no_grad():
            return model.generate(input_ids=inp, attention_mask=am, **gen)
    finally:
        if h is not None:
            h.remove()


base = gen_once(None)
zero = gen_once(0.0)
check('(2) 係数 0 の hook は結果を変えない', torch.equal(base, zero), '一致 %s' % bool(torch.equal(base, zero)))
big = gen_once(50.0)
check('(2b) 大きな係数は結果を変える', not torch.equal(base, big), '違う %s' % bool(not torch.equal(base, big)))

# (3) 加わる量を直に測る（prefill の主位置と復号の各段）
seen = {'prefill': None, 'decode': []}
ref = {}


def probe(module, inputs, output):
    hs = output[0] if isinstance(output, tuple) else output
    key = 'decode' if hs.shape[1] == 1 else 'prefill'
    if key == 'prefill':
        ref['prefill'] = hs.detach().clone()
    else:
        ref.setdefault('decode', []).append(hs.detach().clone())


h0 = direction_B.decoder_layers(model)[li].register_forward_hook(probe)
try:
    torch.manual_seed(5)
    with torch.no_grad():
        model.generate(input_ids=inp, attention_mask=am, **gen)
finally:
    h0.remove()

coef = 2.0
add = {'prefill': None, 'decode': []}


def probe2(module, inputs, output):
    hs = output[0] if isinstance(output, tuple) else output
    if hs.shape[1] == 1:
        add.setdefault('decode', []).append(hs.detach().clone())
    else:
        add['prefill'] = hs.detach().clone()


hk = RUN.make_hook(v, coef, +1, [inp.shape[1] - 1])
h1 = direction_B.decoder_layers(model)[li].register_forward_hook(hk)
h2 = direction_B.decoder_layers(model)[li].register_forward_hook(probe2)
try:
    torch.manual_seed(5)
    with torch.no_grad():
        model.generate(input_ids=inp, attention_mask=am, **gen)
finally:
    h1.remove(); h2.remove()

want = torch.as_tensor(v, dtype=ref['prefill'].dtype) * coef
d_last = float((add['prefill'][0, -1, :] - ref['prefill'][0, -1, :] - want).abs().max())
d_prev = float((add['prefill'][0, :-1, :] - ref['prefill'][0, :-1, :]).abs().max())
check('(3) prefill は主位置にだけ加わる', d_last < 1e-3 and d_prev < 1e-6,
      '主位置の差 %.3g・それ以外の差 %.3g' % (d_last, d_prev))
n_dec = len(add.get('decode', []))
check('(3b) 復号の各段に加わる', n_dec == gen['max_new_tokens'] - 1 or n_dec == gen['max_new_tokens'],
      '復号の段 %d 回' % n_dec)

# (4) hook が残らない
try:
    RUN.assert_no_hooks(model, li)
    check('(4) バッチの後に hook が零本', True, '零本')
except SystemExit as e:
    check('(4) バッチの後に hook が零本', False, e)

# (5) 腕が混ざったバッチは止まる
try:
    steer_B.assert_batch_uniform([AT['O'], AT['Onull']])
    check('(5) 腕が混ざったバッチを止める', False, '止まらなかった')
except SystemExit:
    check('(5) 腕が混ざったバッチを止める', True, '止まった')

# (7) 一つのセルを本当に走らせて、記録の欄がそろうか
LIDX = [idxs[r] for r in ratios]
try:
    rows = RUN.run_cell(model, tok, scenario=T['scenarios'][0], arm='Onull+v', layer_ratio=ratio, coef=1.0,
                        n=3, cell_seed_value=12345, tag=T['tags']['main'], run_key='e2e__test',
                        dirs=loaded, layer_idx=li, gen=gen, batch=2, resp_layer_idxs=LIDX)['trials']
    need = set(T['trial_record_fields']['fields'])
    got = set(rows[0]) if rows else set()
    check('(7) セルを走らせて記録の欄がそろう', len(rows) == 3 and need <= got,
          '%d 行・欠けた欄 %s' % (len(rows), sorted(need - got) or 'なし'))
except Exception as e:
    check('(7) セルを走らせて記録の欄がそろう', False, '%s: %s' % (type(e).__name__, e))

# (8) **走行器の出力を置き場に書き、本物の整合検査に通す**（裁定 D117・D127・2026-09-19）。
#     前は走行器が記録を書かず、走行器の出力は一度も集計の器に読まれていなかった。
#     さらに種の単位が走行器（バッチの種）と整合検査・合成データ（試行の種）で食い違っており、
#     **合成データは通り、本物の出力は全件落ちる**形になっていた。
import subprocess
root = os.path.join(tmp, 'runroot')
sc0 = T['scenarios'][0]
tag = T['tags']['main']
run_key = '%s__%s__s1__e2e' % (tag, sc0)
cells, raws_all, resp_all, n_cell, bt = [], [], {}, 5, 2          # 五試行・バッチ二（区切りを跨ぐ）
arms_run = ['Onull', 'Onull+v', 'Onull+vrand']
added = {}
for arm in arms_run:
    cs = runs_B.cell_seed(T, T['seeds']['main'][sc0], 'main', (sc0, arm))
    o_ = RUN.run_cell(model, tok, scenario=sc0, arm=arm, layer_ratio=ratio, coef=1.0, n=n_cell,
                      cell_seed_value=cs, tag=tag, run_key=run_key, dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)
    cells += o_['trials']
    raws_all += o_['raws']
    resp_all.update(o_['resp'])
    added[arm] = o_.get('added_norm')
# 正本の欄をそろえた manifest（整合検査がこの一覧を読む）
T_b = dict(T)
man = {'tag': tag, 'run_key': run_key, 'session': 1, 'n': n_cell, 'seed': T['seeds']['main'][sc0],
       'batch': T['runner']['batch'], 'padding': 'left', 'model': 'e2e/random-init', 'model_rev': 'E2E',
       'tokenizer_rev': 'E2E', 'runner_sha': runs_B.sha16_file(os.path.join(HERE, 'run_stageB_local.py')),
       'pip_freeze_sha16': 'E2E', 'gpu': 'cpu', 'started': 'e2e', 'ended': 'e2e', 'dry_run': True,
       'scenario': sc0, 'arms': arms_run, 'layer': ratio, 'coef': 1.0, 'direction_ids': ['fixed', 'static', 'rand'],
       'dtype': str(next(model.parameters()).dtype).replace('torch.', ''), 'order': T['runner']['order_id'],
       'transformers_version': __import__('transformers').__version__, 'refuse_rules_sha16': runs_B.sha16_file(RUN.REFUSE_RULES),
       'added_norm': added}
try:
    RUN.write_cell(root, tag, run_key, man, cells, raws_all, resp_all)
    RUN.write_session(root, tag, 1, [run_key], {'gpu': 'cpu'})
    check('(8a) 走行器が記録とセッション記録を置き場に書く', os.path.exists(os.path.join(root, tag, run_key, 'manifest.json')),
          '%d 行を書いた' % len(cells))
except SystemExit as e:
    check('(8a) 走行器が記録とセッション記録を置き場に書く', False, e)
# 上書きしないこと
try:
    RUN.write_cell(root, tag, run_key, man, cells)
    check('(8b) 既にある記録に上書きしない', False, '上書きした')
except SystemExit:
    check('(8b) 既にある記録に上書きしない', True, '止まった')
# **バッチの実際の行数**（採否表 P406）: 器を通さずに数えた行数（五試行・バッチ二なら 2・2・2・2・1）と照らす
_want_rows = [min((i // bt + 1) * bt, n_cell) - (i // bt) * bt for i in range(n_cell)]
_got_rows = [c_['batch_rows'] for c_ in cells if c_['arm'] == 'Onull']
check('(8g) 試行の記録にバッチの実際の行数が入る（採否表 P406）', _got_rows == _want_rows, '記録 %s／数え直し %s' % (_got_rows, _want_rows))
# **加えた量**（採否表 P394）: 無操作は空、介入の腕は 係数 × ‖v̂〔static〕‖（ランダム方向の腕も同じ量）
_nv = float(np.linalg.norm(loaded[('static', ratio)]))
check('(8h) 走行器がセルの加えた量を返し、走行の記録に入る（採否表 P394）',
      added.get('Onull') is None and abs((added.get('Onull+v') or 0) - _nv) < 1e-6 and abs((added.get('Onull+vrand') or 0) - _nv) < 1e-6,
      '無操作 %s・静的 %s・ランダム %s（‖v̂‖ %.6g）' % (added.get('Onull'), added.get('Onull+v'), added.get('Onull+vrand'), _nv))
# 読み口が読めるか
cc = runs_B.counts_main(T, root=root, allow_dry=True)[0]
check('(8c) 読み口（runs_B）が走行器の出力を読める', sum(c['n'] for c in cc.values()) == len(cells),
      '読んだ試行 %d／書いた試行 %d' % (sum(c['n'] for c in cc.values()), len(cells)))
# **本物の整合検査に通す**（種は「バッチの種」で組み直して照合される）
p = subprocess.run([sys.executable, os.path.join(HERE, 'integrity_B.py'), '--tag', tag, '--root', root, '--allow-dry',
                    '--out', os.path.join(tmp, 'i.md'), '--force'], capture_output=True, text=True, encoding='utf-8', cwd=REPO)
ij = os.path.join(tmp, 'i.json')
probs = json.load(open(ij, encoding='utf-8')).get('problems', []) if os.path.exists(ij) else ['記録が読めない']
seed_probs = [x for x in probs if 'seed' in x]
check('(8d) 走行器の種が整合検査の組み直しと一致する（裁定 D127）', not seed_probs,
      ('種の不整合 %d 件' % len(seed_probs)) if seed_probs else '種の不整合 零')
# この検査は**速さのために四点を登録から外している**——貪欲の生成・セルの試行数（本走行の n より小さい）・
# 走らせるセルの数（登録の升目の一部だけ）・模型の dtype（小さな模型は float32）。
# 整合検査は**その四点を捕まえるべき**であり（眠っていないことの確かめ）、**それ以外は零であるべき**である。
_expected = ('生成の設定が登録と違う', '連番でない', '登録の升目', 'dtype')
caught = [x for x in probs if 'seed' not in x and any(e in x for e in _expected)]
other = [x for x in probs if 'seed' not in x and not any(e in x for e in _expected)]
check('(8e) 検査のために登録から外した四点を、整合検査が捕まえる',
      all(any(e in x for x in caught) for e in _expected),
      '捕まえた %d 件（%s）' % (len(caught), '・'.join(e for e in _expected if any(e in x for x in caught))))
check('(8e2) それ以外の不整合は零', not other, ('%d 件: %s' % (len(other), other[:2])) if other else '零')
# 再開: 途中から走らせ直しても、同じ試行は同じ種を持つ
cs = runs_B.cell_seed(T, T['seeds']['main'][sc0], 'main', (sc0, 'Onull'))
full = RUN.run_cell(model, tok, scenario=sc0, arm='Onull', layer_ratio=ratio, coef=1.0, n=n_cell,
                    cell_seed_value=cs, tag=tag, run_key='r', dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)['trials']
part = RUN.run_cell(model, tok, scenario=sc0, arm='Onull', layer_ratio=ratio, coef=1.0, n=n_cell,
                    cell_seed_value=cs, tag=tag, run_key='r', dirs=loaded, layer_idx=li, gen=gen, batch=bt, start=3, resp_layer_idxs=LIDX)['trials']
same = all(a_['seed'] == b_['seed'] for a_, b_ in zip(full[3:], part))
check('(8f) 途中から再開しても同じ試行は同じ種を持つ', same and len(part) == n_cell - 3,
      '再開 %d 行・種の一致 %s' % (len(part), same))

# (9) **すべての種類の腕**（v2・2026-09-19）。反証の場面にはすべての種類の腕がそろう。
sc4 = T['falsification_scenario']
kinds = {'Osec-Ncold': None, 'Onull+v': 'static', 'O-Ncold-v': 'static', 'Onull+vrand': 'random', 'O-Ncold+vNk': 'Nk',
         'O-Ncold-vtd': 'td', 'Osec-Ncold+v6b': 'loaded'}
outs, errs = {}, []
for arm in kinds:
    try:
        outs[arm] = RUN.run_cell(model, tok, scenario=sc4, arm=arm, layer_ratio=ratio, coef=1.0, n=n_cell,
                                 cell_seed_value=runs_B.cell_seed(T, T['seeds']['main'][sc4], 'main', (sc4, arm)),
                                 tag=tag, run_key='e2e__s4', dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)
    except BaseException as e:
        errs.append('%s: %s' % (arm, str(e)[:80]))
check('(9a) すべての種類の腕が走る（無操作・静的・ランダム・Nk・td・(6b)）', not errs and all(len(o['trials']) == n_cell for o in outs.values()),
      ('止まった腕: %s' % errs) if errs else '腕 %d 種・各 %d 試行' % (len(outs), n_cell))
if 'Onull+vrand' in outs:
    got_ids = [t_['direction_id'] for t_ in outs['Onull+vrand']['trials']]
    want_ids = ['rand:%d' % steer_B.direction_of(t_['trial_index'], n_cell) for t_ in outs['Onull+vrand']['trials']]
    check('(9b) ランダム方向の腕は試行ごとに交互（番号を方向の数で割った余り・裁定 D140）で方向を持つ',
          got_ids == want_ids and got_ids == ['rand:%d' % (t_['trial_index'] % T['random_control']['count']) for t_ in outs['Onull+vrand']['trials']],
          '記録 %s／登録の割り当て %s' % (got_ids, want_ids))
    V_, D_ = RUN.row_vectors(RUN.arm_plan('Onull+vrand'), loaded, ratio, list(range(n_cell)), n_cell, 'main')
    R_ = steer_B.random_directions(loaded[('static', ratio)], 'main', ratio)
    ok_v = all(np.allclose(V_[i], R_[steer_B.direction_of(i, n_cell)]) for i in range(n_cell))
    check('(9b2) 行ごとの方向は、その試行に割り当てた方向そのもの', ok_v, '行ごとの一致 %s' % ok_v)
# hook の中身の照合: 別の層に残った hook があれば、走らせる前に止まる
_stray = direction_B.decoder_layers(model)[(li + 1) % n_layers].register_forward_hook(lambda m, i, o: o)
try:
    RUN.run_cell(model, tok, scenario=sc4, arm='Onull+v', layer_ratio=ratio, coef=1.0, n=2, cell_seed_value=1, tag=tag,
                 run_key='e2e__stray', dirs=loaded, layer_idx=li, gen=gen, batch=bt, resp_layer_idxs=LIDX)
    check('(9c) 掛けるべきでない層の hook を見つけて止まる（裁定 D122）', False, '止まらなかった')
except SystemExit as e:
    check('(9c) 掛けるべきでない層の hook を見つけて止まる（裁定 D122）', 'hook' in str(e), str(e)[:80])
finally:
    _stray.remove()
# 様式・言及・refuse の分類・ループ・打ち切り: 生テキストの最終試行を、段階 A の凍結した関数で**別に**採点し直して照らす
import response_mode_A as _RMA
TF_ = RUN.frozen_text_funcs()
s4s, s4i = RUN.scenario_and_instruction(sc4)
bad_mode = []
for arm, o in outs.items():
    at_ = RUN.arm_texts()[RUN.base_arm_of(arm)]['text']
    sent_ = ('', at_, s4s['text'], s4i)
    for t_, r_ in zip(o['trials'], o['raws']):
        mf = _RMA.measure(r_['final'], tuple(_RMA._norm(x) for x in sent_))
        lp_ = TF_['loop_info'](r_['final'])
        want_ = {'style_a': bool(mf['a']), 'style_b': bool(mf['b']), 'mention': bool(mf['c1']), 'loop_flag': bool(lp_['fired']),
                 'truncated': r_['finish'] == 'length'}
        if any(t_[k_] != v_ for k_, v_ in want_.items()) or t_['refuse_class'] is None:
            bad_mode.append((t_['trial_id'], {k_: (t_[k_], v_) for k_, v_ in want_.items() if t_[k_] != v_}))
check('(9d) 様式・言及・ループ・打ち切りが段階 A の関数の採点と一致し、refuse の分類が空でない', not bad_mode,
      ('食い違い %d 件: %s' % (len(bad_mode), bad_mode[:1])) if bad_mode else '試行 %d 件すべて一致' % sum(len(o['trials']) for o in outs.values()))
# 生テキスト: 置き場に書かれ、試行と行が対応する
rawp = os.path.join(root, tag, run_key, 'raw-%s.jsonl' % run_key)
rraw = [json.loads(l) for l in open(rawp, encoding='utf-8')] if os.path.exists(rawp) else []
check('(9e) 生テキストが置き場に書かれ、試行と行が対応する', len(rraw) == len(cells) and all(r_.get('text') is not None and r_['trial_id'] == c_['trial_id']
                                                                   for r_, c_ in zip(rraw, cells)),
      '生テキストの行 %d／試行 %d・引き直しの印 %d 件' % (len(rraw), len(cells), sum('===RETRY===' in (r_.get('text') or '') for r_ in rraw)))
# 副位置の活性: 置き場の npz・形・有限・小分けと一行ずつの一致・手で組んだ計算との一致
rp = os.path.join(root, tag, run_key, 'resp-%s.npz' % run_key)
zr = np.load(rp) if os.path.exists(rp) else None
with_path = [c_ for c_ in cells if c_.get('resp_mean_path')]
ok_shape = zr is not None and all(zr[c_['resp_mean_path'].split('#')[1]].shape == (len(ratios), cfg.hidden_size) and
                                  np.isfinite(zr[c_['resp_mean_path'].split('#')[1]].astype(np.float32)).all() for c_ in with_path)
check('(9f) 副位置の活性が置き場に書かれる（候補の層 × 隠れ次元・有限）', bool(with_path) and ok_shape,
      '活性を持つ試行 %d／%d' % (len(with_path), len(cells)))
resp_ids = [tok(r_['final'], add_special_tokens=False)['input_ids'][:6] or [0] for r_ in raws_all[:4]]
_hv = np.stack([loaded[('static', ratio)]] * len(resp_ids))
h_args = {'layer_idx': li, 'vecs': _hv, 'coef': 1.0, 'sign': +1}
m4 = RUN.capture_resp_mean(model, ids, resp_ids, LIDX, h_args, rows=4)
m1 = RUN.capture_resp_mean(model, ids, resp_ids, LIDX, h_args, rows=1)
d41 = max(float(np.abs(a_.astype(np.float32) - b_.astype(np.float32)).max()) for a_, b_ in zip(m4, m1))
check('(9g) 副位置の活性は、左詰めの小分けと一行ずつで一致する（位置の番号の扱い）', d41 < 1e-2, '最大差 %.3g（fp16 の丸めの内）' % d41)
# 手で組む: 列をつなぎ、hook を掛けて順伝播し、応答の位置の平均を取る（器を通さない計算）
_seq = torch.tensor([list(ids) + list(resp_ids[0])])
_h = RUN.register_hook(model, li, RUN.make_hook(loaded[('static', ratio)], 1.0, +1, [len(ids) - 1]))
try:
    with torch.no_grad():
        _o = model(input_ids=_seq, attention_mask=torch.ones_like(_seq), output_hidden_states=True)
finally:
    _h.remove()
_man = np.stack([_o.hidden_states[k_ + 1][0, len(ids):, :].float().mean(0).numpy() for k_ in LIDX])
d_man = float(np.abs(_man - m1[0].astype(np.float32)).max())
check('(9h) 副位置の活性は、手で組んだ計算と一致する', d_man < 1e-2, '最大差 %.3g' % d_man)

# (10) **層の割合と層の添字が食い違えば、走行器が走らせる前に止まる**（採否表 P393）
try:
    RUN.run_cell(model, tok, scenario=sc4, arm='Onull+v', layer_ratio=ratio, coef=1.0, n=2, cell_seed_value=1, tag=tag,
                 run_key='e2e__badlayer', dirs=loaded, layer_idx=(li + 1) % n_layers, gen=gen, batch=bt, resp_layer_idxs=LIDX)
    check('(10) 層の割合と添字の食い違いで止まる（採否表 P393）', False, '止まらなかった')
except SystemExit as e:
    check('(10) 層の割合と添字の食い違いで止まる（採否表 P393）', '層の割合' in str(e), str(e)[:80])
# (11) **決定性 (ii) はバッチの組成を変えた比較**（採否表 P396）: 一本流しと、走行器と同じ組成（同じプロンプトを runner.batch 行）の主位置の活性
_H1, _H3 = {}, {}
for _arm in ('O', 'Osec'):
    _s, _i = RUN.scenario_and_instruction(T['extraction_scenarios'][0])
    _ids = steer_B.apply_chat(tok, RUN.user_message(AT[_arm], _s['text'], _i))
    for _r in ratios:
        _H1[(_arm, _r)] = direction_B.main_position_activation(model, _ids, idxs[_r])
        _H3[(_arm, _r)] = direction_B.main_position_activation_batch(model, _ids, idxs[_r])
_ok11, _rows11 = direction_B.determinism_cross_order(_H1, _H3)
check('(11) 決定性 (ii): 一本流しと走行器と同じバッチの組成の主位置の活性が許容差の内側（採否表 P396）', _ok11,
      'バッチ %d 行・%d 組・最小のコサイン %s' % (T['runner']['batch'], len(_rows11), min((r_['cos'] for r_ in _rows11 if r_.get('cos') is not None), default=None)))
# (12) **盤の全腕で、組み立て済みの列が凍結走行器の読み方と式で作った列と一致する**（v4・2026-09-19）。
#      走行器 v6 までは腕の本文の末尾の改行を残して読み、O・Osec・Onull で前置きと場面の本文の間の改行が一つ多かった。
#      期待値は正本の置き場から凍結走行器の `rd` で読んだ本文と凍結走行器の式で作る（走行器の読み口 `arm_texts` を通さない）。
_rd12 = RUN.frozen_rd()
_bad12 = []
for _arm in T['arms']['panel']:
    _t12 = '' if _arm == 'N' else _rd12(os.path.join(REPO, *T['arms']['files'][_arm]['path'].split('/')))
    for _sc12 in T['extraction_scenarios']:
        _s12, _i12 = RUN.scenario_and_instruction(_sc12)
        _want12 = (_t12 + '\n\n' + _s12['text'] + _i12) if _t12 else (_s12['text'] + _i12)
        _got12 = RUN.user_message(AT[_arm], _s12['text'], _i12)
        if _got12 != _want12 or steer_B.apply_chat(tok, _got12) != steer_B.apply_chat(tok, _want12):
            _bad12.append('%s×%s' % (_arm, _sc12))
check('(12) 盤の全腕で、組み立て済みの列が凍結走行器の読み方と式で作った列と一致する（2026-09-19）', not _bad12,
      ('食い違い %s' % _bad12) if _bad12 else '腕 %d × 抽出場面 %d・一致' % (len(T['arms']['panel']), len(T['extraction_scenarios'])))

# (13) **品質床のセル**（v5・裁定 D145・D146・2026-09-19 の夕刻）。問いは合成（長さを変えて左詰めを起こす・候補のデータは使わない）。
import qf_task_B
import subprocess
_Q = [{'id': str(k_), 'question': ('問い%d。' % k_) + ('長い文。' * (k_ % 7)), 'choices': ['甲%d' % k_, '乙', '丙', '丁'] + (['戊'] if k_ % 2 else []),
       'answer': 'ABCD'[k_ % 4]} for k_ in range(20)]
_qtag = T['tags']['quality']
_cs = lambda arm_, l_, c_: runs_B.cell_seed(T, T['seeds']['quality'], 'quality', ('selection', arm_, l_, c_))
_msgs = []
_orig_apply = steer_B.apply_chat
steer_B.apply_chat = lambda tok_, m_: (_msgs.append(m_), _orig_apply(tok_, m_))[1]
try:
    q0 = RUN.run_quality_cell(model, tok, items=_Q, arm='Onull', stage='selection', task='synth', cell_seed_value=_cs('Onull', None, None),
                              tag=_qtag, run_key='e2e__q_noop')
    _m_with = list(_msgs); _msgs.clear()
    qN = RUN.run_quality_cell(model, tok, items=_Q[:3], arm='Onull', stage='selection', task='synth', cell_seed_value=1, tag=_qtag,
                              run_key='e2e__q_nopre', input_form='without_preamble')
    _m_without = list(_msgs)
finally:
    steer_B.apply_chat = _orig_apply
_bk = [qf_task_B.block(q_) for q_ in _Q]
check('(13a) 品質床の問いの組み立て: 前置きあり＝前置き＋空行＋問いの本文、なし＝問いの本文だけ（裁定 D138・D146）',
      _m_with == [AT['Onull'] + '\n\n' + b_ for b_ in _bk] and _m_without == _bk[:3], '前置きあり %d 件・なし %d 件' % (len(_m_with), len(_m_without)))
qc0 = RUN.run_quality_cell(model, tok, items=_Q, arm='Onull+v', stage='selection', task='synth', cell_seed_value=_cs('Onull+v', ratio, 0.0),
                           tag=_qtag, run_key='e2e__q_c0', layer_ratio=ratio, coef=0.0, dirs=loaded, layer_idx=li)
_same = [a_['text'] == b_['text'] for a_, b_ in zip(q0['raws'], qc0['raws'])]
check('(13b) 品質床: 係数 0 の hook を掛けたセルが無操作と一致する（左詰めのバッチ・貪欲）', all(_same) and len(_same) == len(_Q), '%d/%d 行一致' % (sum(_same), len(_same)))
qc4 = RUN.run_quality_cell(model, tok, items=_Q, arm='Onull+v', stage='selection', task='synth', cell_seed_value=_cs('Onull+v', ratio, 4.0),
                           tag=_qtag, run_key='e2e__q_c4', layer_ratio=ratio, coef=4.0, dirs=loaded, layer_idx=li)
_diff = sum(a_['text'] != b_['text'] for a_, b_ in zip(q0['raws'], qc4['raws']))
check('(13c) 品質床: 係数 ≠ 0 の hook は出力を変える（介入が品質床の経路に掛かっている）', _diff > 0 and qc4['added_norm'] and qc4['added_norm'] > 0,
      '%d/%d 行が違う・加えた量 %.3g' % (_diff, len(_Q), qc4['added_norm'] or 0))
_bt = T['runner']['batch']
_rows13 = [r_['batch_rows'] for r_ in q0['trials']]
_cons = all(r_['choice'] == qf_task_B.extract_letter(w_['text'], qf_task_B.letters_of(q_)) and r_['format_fail'] == (r_['choice'] is None)
            and r_['correct'] == (r_['choice'] == q_['answer']) and w_['item_id'] == q_['id']
            for r_, w_, q_ in zip(q0['trials'], q0['raws'], _Q))
_samp = q0['trials'][0]['sampling']
check('(13d) 品質床の記録: バッチの行数・記号と書式外と正誤が生テキストから組み直せる・生成の設定に正本の温度と top_p・前置きの SHA',
      _rows13 == [min(_bt, len(_Q))] * min(_bt, len(_Q)) + [len(_Q) - _bt] * (len(_Q) - _bt) and _cons
      and _samp.get('temperature') == T['quality_floor']['generation']['temperature'] and _samp.get('top_p') == T['quality_floor']['generation']['top_p']
      and q0['trials'][0]['preamble_sha'] == T['arms']['sha16']['Onull'] and qN['trials'][0]['preamble_sha'] is None,
      'バッチの行数 %s・整合 %s・生成の設定 %s' % (sorted(set(_rows13)), _cons, {k_: _samp.get(k_) for k_ in ('temperature', 'top_p', 'do_sample', 'max_new_tokens')}))
# 例外の引き直し: 一度目だけ落ちるバッチは引き直して ok、二度とも落ちるバッチは api_error（hook は外れている）
_orig_gen = model.generate
_calls = {'n': 0}


def _flaky(*a_, **k_):
    _calls['n'] += 1
    if _calls['n'] == 1:
        raise RuntimeError('擬似の例外（一度目）')
    return _orig_gen(*a_, **k_)


model.generate = _flaky
try:
    qr = RUN.run_quality_cell(model, tok, items=_Q[:4], arm='Onull+v', stage='selection', task='synth', cell_seed_value=1, tag=_qtag,
                              run_key='e2e__q_retry', layer_ratio=ratio, coef=1.0, dirs=loaded, layer_idx=li)
    model.generate = lambda *a_, **k_: (_ for _ in ()).throw(RuntimeError('擬似の例外（常に）'))
    qe = RUN.run_quality_cell(model, tok, items=_Q[:4], arm='Onull+v', stage='selection', task='synth', cell_seed_value=1, tag=_qtag,
                              run_key='e2e__q_err', layer_ratio=ratio, coef=1.0, dirs=loaded, layer_idx=li)
finally:
    model.generate = _orig_gen
_nh = sum(len(getattr(L_, '_forward_hooks', {}) or {}) for L_ in direction_B.decoder_layers(model))
check('(13e) 品質床: 一度だけ落ちたバッチは引き直して ok・二度とも落ちたバッチは api_error・hook は残らない',
      all(r_['status'] == 'ok' for r_ in qr['trials']) and all(r_['status'] == 'api_error' and r_['correct'] is None for r_ in qe['trials'])
      and all(w_['error'] for w_ in qe['raws']) and _nh == 0, '引き直し %d 行 ok・api_error %d 行・残った hook %d 本' % (
          sum(r_['status'] == 'ok' for r_ in qr['trials']), sum(r_['status'] == 'api_error' for r_ in qe['trials']), _nh))
# 本物の整合検査に通す（選定の段の二セル・種と生成の設定と manifest の欄と走行を跨いだ同一性で落ちないこと）
_root13 = os.path.join(tmp, 'q13')
_env13 = dict(RUN.manifest_env(model, tok), pip_freeze_sha16='E2E', gpu='cpu', started='x', ended='x', dry_run=False)
_rk13 = []
for _arm13, _out13, _l13, _c13 in (('Onull', q0, None, None), ('Onull+v', qc4, ratio, 4.0)):
    _rk = 'e2e13__%s__L%sC%s' % (_arm13, _l13, _c13)
    _tr = [dict(r_, run_key=_rk, trial_id=r_['trial_id'].replace(r_['run_key'], _rk)) for r_ in _out13['trials']]
    RUN.write_cell(_root13, _qtag, _rk, dict(_env13, tag=_qtag, run_key=_rk, session=1, n=len(_tr), seed=T['seeds']['quality'], stage='selection',
                                              arm=_arm13, layer=_l13, coef=_c13, task_source_sha16='E2E', added_norm=_out13['added_norm']), _tr, _out13['raws'])
    _rk13.append(_rk)
RUN.write_session(_root13, _qtag, 1, _rk13, extra={'gpu': 'cpu'})
_ij = os.path.join(tmp, 'integrity13.md')
subprocess.run([sys.executable, os.path.join(HERE, 'integrity_B.py'), '--tag', _qtag, '--root', _root13, '--out', _ij, '--force'],
               capture_output=True, text=True, encoding='utf-8', errors='replace', env=dict(os.environ, PYTHONIOENCODING='utf-8'))
_ip = json.load(open(os.path.splitext(_ij)[0] + '.json', encoding='utf-8'))['problems'] if os.path.exists(os.path.splitext(_ij)[0] + '.json') else ['整合検査の出力が無い']
_bad13 = [p_ for p_ in _ip if any(w_ in p_ for w_ in ('seed', '生成の設定', 'manifest に欄が無い', 'セッション記録が無い', '同一であるべき', '同じでない', '出力が無い'))]
check('(13f) 品質床の記録が本物の整合検査の種・生成の設定・manifest の欄・走行を跨いだ同一性で落ちない', not _bad13,
      ('落ちた %s' % _bad13[:2]) if _bad13 else '整合検査の問題 %d 件はいずれも小さな検査に由来（問いの数・升目の欠け）' % len(_ip))

shutil.rmtree(tmp, ignore_errors=True)

json.dump({'kind': 'endtoend_B', 'version': VERSION, 'generated_utc': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
           'model': {'layers': n_layers, 'hidden': cfg.hidden_size, 'random_init': True},
           'checks': checks, 'failed': fails, 'total': len(checks)},
          open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
L = ['# 段階 B **端から端まで**の検査（小さな模型・機械生成・`tools/endtoend_B.py` %s・%s UTC）' % (VERSION, now.strftime('%Y-%m-%d %H:%M')), '',
     '- 裁定 D117: 走行器と抽出器の本体を書き、**小さな模型で端から端まで通す**。',
     '- 模型は**乱数で初期化**した小さな Qwen3 形（層 %d・隠れ次元 %d）。**実重みではない**——率にも活性にも意味は無い。' % (n_layers, cfg.hidden_size),
     '- トークナイザだけは**登録機種の現物**を使う（`OP4B_TOKENIZER_DIR`）。',
     '- **%d 件のうち落ちた検査は %d 件。**' % (len(checks), fails), '',
     '| 確かめたこと | 結果 | 中身 |', '|---|---|---|']
for c in checks:
    L.append('| %s | %s | %s |' % (c['name'], '通った' if c['ok'] else '**落ちた**', c['detail']))
L += ['', '## この検査が確認していないこと', '',
      '- **実重み（Qwen3-4B-Instruct-2507）では一行も走らせていない。**模型は乱数の初期化である。',
      '- したがって**破局率も活性のノルムも、この検査からは何も言えない**。',
      '- バッチ 16・実重み・実際のメモリでの挙動（OOM・KV キャッシュ・速度）は確かめていない。',
      '- 品質床のセルは**合成の問い**で通した（13）。候補の課題（JCommonsenseQA・JMMLU）の問いは、ここでは使わない（課題の器の自己検査が断片の登録と照らす）。',
      '- **相をまたいだ走らせ方の順**（同一性選別 → 調整走行 → 品質床 → 本走行）と、Colab での起動は、'
      '  まだ書いていない（一つのセルを走らせて書く口と、セッション記録を書く口までは書いた）。',
      '- 様式と言及の照らし合わせ（9d）は、走行器と同じ段階 A の関数で採点し直したもので、**関数そのものの正しさ**は段階 A の検分と走行器の自己検査（見本の文）に拠る。',
      '- 乱数の模型の出力はほぼすべて書式外になるので、**答えの読める試行（破局・refuse の判定）の経路は、ここでは走らない**（走行器の自己検査の見本の文で確かめた）。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[endtoend_B] %s | %d 件中 落ちた検査 %d 件' % (os.path.relpath(out_md, REPO), len(checks), fails))
sys.exit(1 if fails else 0)
