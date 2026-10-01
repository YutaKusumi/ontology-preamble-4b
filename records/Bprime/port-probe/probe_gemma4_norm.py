import sys, io, json, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import torch
from transformers import Gemma4Config, Gemma4ForConditionalGeneration
HF = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/Bprime/hf/gemma-4-31B-it/842da3794eaa0b77d5f08bae87a17459d91ff475'
d = json.load(open(HF + '/config.json', encoding='utf-8'))
td = d['text_config']
td.update(hidden_size=64, intermediate_size=128, num_hidden_layers=6, num_attention_heads=4, num_key_value_heads=2, head_dim=16, global_head_dim=32, num_global_key_value_heads=1)
td['layer_types'] = list(td['layer_types'][:6])
vd = d['vision_config']
vd.update(hidden_size=32, intermediate_size=64, num_hidden_layers=1, num_attention_heads=2, num_key_value_heads=2, head_dim=16, global_head_dim=16)
t = Gemma4Config.from_dict(d)
torch.manual_seed(0)
m = Gemma4ForConditionalGeneration(t).float().eval()
lm = m.model.language_model
with torch.no_grad():
    for p in lm.norm.parameters():
        p.copy_(torch.randn_like(p) * 0.5)
import inspect
print('norm class:', type(lm.norm).__name__)
print(inspect.getsource(type(lm.norm).forward)[:700])
x = torch.tensor([[2, 105, 2364, 107, 88733, 106, 107, 105, 4368, 107, 100, 45518, 107, 101]])
cap = t.text_config.final_logit_softcapping
cap_f = lambda z: torch.tanh(z / cap) * cap
last_out = {}
def hk(mod, inp, out):
    last_out['h'] = (out[0] if isinstance(out, tuple) else out).detach().clone()
    return out
hd = lm.layers[-1].register_forward_hook(hk)
with torch.no_grad():
    o = m(input_ids=x, output_hidden_states=True)
hd.remove()
hs = o.hidden_states
W = m.lm_head.weight
L = o.logits[0, -1]
print('hs[-1] == last layer output (pre-norm)?', bool(torch.allclose(hs[-1], last_out['h'], atol=1e-6)))
print('max |cap(norm(last layer out)) - logits| =', float((cap_f(lm.norm(last_out['h'])[0, -1] @ W.T) - L).abs().max()))
print('max |cap(hs[-1]) - logits| =', float((cap_f(hs[-1][0, -1] @ W.T) - L).abs().max()))
print('max |cap(norm(hs[-1])) - logits| =', float((cap_f(lm.norm(hs[-1])[0, -1] @ W.T) - L).abs().max()))
