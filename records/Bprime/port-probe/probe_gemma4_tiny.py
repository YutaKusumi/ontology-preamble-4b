# Gemma 4（transformers 5.16.1）のつくりを、小さな乱数の模型で確かめる（下調べ・記録ではない・場面の文は使わない）
import os, sys, io, json, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import torch
import transformers
from transformers import AutoTokenizer, Gemma4Config, Gemma4ForConditionalGeneration
HF = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475'
print('transformers', transformers.__version__, 'torch', torch.__version__)
tok = AutoTokenizer.from_pretrained(HF)
msgs = [{'role': 'user', 'content': 'テスト'}]
s = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
print('rendered (no system):', repr(s))
ids = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True)
ids = ids['input_ids'] if isinstance(ids, dict) or hasattr(ids, 'keys') else ids
print('ids:', ids, '| decoded pieces:', [tok.decode([i]) for i in ids])
s2 = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False, enable_thinking=True)
print('rendered (enable_thinking=True):', repr(s2))
d = json.load(open(HF + '/config.json', encoding='utf-8'))
print('real text_config head/kv/global:', {k: d['text_config'].get(k) for k in ('head_dim', 'global_head_dim', 'num_key_value_heads', 'num_global_key_value_heads', 'final_logit_softcapping', 'attention_k_eq_v', 'num_hidden_layers', 'hidden_size')})
td = d['text_config']
td.update(hidden_size=64, intermediate_size=128, num_hidden_layers=6, num_attention_heads=4, num_key_value_heads=2, head_dim=16, global_head_dim=32, num_global_key_value_heads=1)
td['layer_types'] = list(td['layer_types'][:6])
vd = d['vision_config']
vd.update(hidden_size=32, intermediate_size=64, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2, head_dim=16, global_head_dim=16)
t = Gemma4Config.from_dict(d)
tt = t.text_config
torch.manual_seed(0)
m = Gemma4ForConditionalGeneration(t).float().eval()
print('top modules:', [n for n, _ in m.named_children()])
print('model children:', [n for n, _ in m.model.named_children()])
lm = m.model.language_model
print('language_model children:', [n for n, _ in lm.named_children()])
print('n layers:', len(lm.layers), '| layer0 type:', type(lm.layers[0]).__name__)
print('lm_head:', type(m.lm_head).__name__ if hasattr(m, 'lm_head') else None, '| tied:', m.lm_head.weight.data_ptr() == lm.embed_tokens.weight.data_ptr() if hasattr(m, 'lm_head') else None)
x = torch.tensor([ids])
captured = {}
def hk(mod, inp, out):
    captured['type'] = type(out).__name__
    captured['h'] = (out[0] if isinstance(out, tuple) else out).detach().clone()
    return out
k = 2
hd = lm.layers[k].register_forward_hook(hk)
with torch.no_grad():
    o = m(input_ids=x, output_hidden_states=True)
hd.remove()
hs = o.hidden_states if getattr(o, 'hidden_states', None) is not None else None
print('output type:', type(o).__name__, '| logits', tuple(o.logits.shape), '| hidden_states len', len(hs) if hs is not None else None, '| hook out type', captured['type'])
print('hidden_states[k+1] == layers[k] output:', bool(torch.allclose(hs[k + 1], captured['h'])) if hs is not None else None)
h_last = hs[-1][0, -1] if hs is not None else None
fn = lm.norm
man = fn(hs[-1])[0, -1] @ m.lm_head.weight.T if hs is not None else None
cap = tt.final_logit_softcapping
man_c = torch.tanh(man / cap) * cap if cap else man
print('final hidden_states is post-norm?:', 'check below')
print('max |manual(norm(hs[-1]))->softcap - logits| =', float((man_c - o.logits[0, -1]).abs().max()))
man2 = hs[-1][0, -1] @ m.lm_head.weight.T
man2_c = torch.tanh(man2 / cap) * cap if cap else man2
print('max |manual(hs[-1] no norm)->softcap - logits| =', float((man2_c - o.logits[0, -1]).abs().max()))
add = torch.zeros(tt.hidden_size); add[0] = 5.0
def hk_add(mod, inp, out):
    hs0 = out[0] if isinstance(out, tuple) else out
    hs0[:, -1:, :] = hs0[:, -1:, :] + add
    return (hs0,) + tuple(out[1:]) if isinstance(out, tuple) else hs0
hd = lm.layers[k].register_forward_hook(hk_add)
with torch.no_grad():
    o2 = m(input_ids=x)
hd.remove()
print('steering changes last logits:', float((o2.logits[0, -1] - o.logits[0, -1]).abs().max()) > 0)
print('params (tiny):', sum(p.numel() for p in m.parameters()))
