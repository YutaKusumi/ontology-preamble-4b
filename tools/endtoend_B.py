# -*- coding: utf-8 -*-
"""endtoend_B.py v1 —— 走行器と抽出器の本体を、**小さな模型で端から端まで通す**（裁定 D117・2026-09-18）。

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
**実重みでは何も確かめていない。** 模型は乱数で初期化したもので、率にも活性にも意味は無い。
出力: records/B/endtoend-B-<日付>.{md,json}（--force が無ければ上書きしない）。
用法: python tools/endtoend_B.py [--force] [--layers 4] [--hidden 64]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, argparse, datetime, tempfile, shutil

VERSION = 'v1'
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
try:
    rows = RUN.run_cell(model, tok, scenario=T['scenarios'][0], arm='Onull+v', layer_ratio=ratio, coef=1.0,
                        n=3, cell_seed_value=12345, tag=T['tags']['main'], run_key='e2e__test',
                        dirs=loaded, layer_idx=li, gen=gen, batch=2)
    need = set(T['trial_record_fields']['fields'])
    got = set(rows[0]) if rows else set()
    check('(7) セルを走らせて記録の欄がそろう', len(rows) == 3 and need <= got,
          '%d 行・欠けた欄 %s' % (len(rows), sorted(need - got) or 'なし'))
except Exception as e:
    check('(7) セルを走らせて記録の欄がそろう', False, '%s: %s' % (type(e).__name__, e))

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
      '- 品質床の走行は含まない（課題が未定・裁定 D66）。',
      '- 中断と再開・記録の書き出しの置き場・セッション記録の作成は、起動器（Colab の段）の側にある。', '',
      '本記録のいかなる数値も、AI に意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(out_md, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
print('[endtoend_B] %s | %d 件中 落ちた検査 %d 件' % (os.path.relpath(out_md, REPO), len(checks), fails))
sys.exit(1 if fails else 0)
