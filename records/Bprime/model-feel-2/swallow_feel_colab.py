# Colab（L4）で Swallow の日英の感触の応答を作る（B′ の機種選び・二巡目・中身は表示しない）
_=0;_=0;_=0
import os, json, time, hashlib
os.environ['HF_HUB_DISABLE_XET'] = '1'
os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'
import torch, transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
CFG = json.loads(r"""{"model": "tokyotech-llm/Llama-3.1-Swallow-8B-Instruct-v0.5", "system": {"ja": "あなたは有用なアシスタントです。", "en": "You are a helpful assistant."}, "tasks": {"1": {"ja": "梅雨の時期に洗濯物を部屋の中で早く乾かす工夫を三つ、丁寧語で、番号つきの箇条書きで説明してください。", "en": "Please explain three tips for drying laundry indoors quickly during the rainy season, as a numbered list, in a polite tone."}, "2": {"ja": "次の文を、上司に送る丁寧なメールの文面に書き換えてください。\n「明日の会議、ちょっと遅れるかも。資料は先に送っとくね。」", "en": "Rewrite the following as a polite email to your manager.\n\"Might be a bit late to tomorrow's meeting. I'll send the slides ahead.\""}, "3": {"ja": "次の文章を二文で要約してください。\n「図書館は本を借りる場所であるだけでなく、地域の人が集まり学び合う場でもある。近年は、子ども向けの読み聞かせ会や、高齢者向けのデジタル機器の講座を開く図書館が増えている。一方で、予算の削減により開館時間を短くせざるを得ない館もある。」", "en": "Summarize the following passage in two sentences.\n\"A library is not only a place to borrow books but also a place where people in the community gather and learn from one another. In recent years, more libraries have been holding story-time sessions for children and digital-device classes for older adults. On the other hand, some libraries have had to shorten their opening hours because of budget cuts.\""}, "4": {"ja": "次の三つのうち、ビタミン C を最も多く含む果物を選んでください。理由を一文で述べ、最後の行に {\"answer\": \"?\"} の形の JSON を一行だけ書いてください（? には a・b・c のどれか一文字を入れる）。\na: りんご\nb: キウイフルーツ\nc: バナナ", "en": "Of the following three, choose the fruit that contains the most vitamin C. Give your reason in one sentence, and on the last line write exactly one line of JSON in the form {\"answer\": \"?\"} (replace ? with one letter: a, b, or c).\na: apple\nb: kiwifruit\nc: banana"}}, "temperature": 0.7, "max_tokens": 700, "n_samples": 2, "seed": 20260931, "tasks_sha16": "94F13F5C1C9F3AA2"}""")
MID = CFG['model']
t0 = time.time()
tok = AutoTokenizer.from_pretrained(MID)
try:
    model = AutoModelForCausalLM.from_pretrained(MID, dtype=torch.bfloat16, device_map='cuda')
except TypeError:
    model = AutoModelForCausalLM.from_pretrained(MID, torch_dtype=torch.bfloat16, device_map='cuda')
model.eval()
eos = model.generation_config.eos_token_id
eos = set(eos if isinstance(eos, list) else [eos])
torch.manual_seed(CFG['seed'])
recs = []
for lang in ('ja', 'en'):
    for task in ('1', '2', '3', '4'):
        for s in range(1, CFG['n_samples'] + 1):
            msgs = [{'role': 'system', 'content': CFG['system'][lang]}, {'role': 'user', 'content': CFG['tasks'][task][lang]}]
            enc = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors='pt', return_dict=True)
            ids, att = enc['input_ids'].to('cuda'), enc['attention_mask'].to('cuda')
            with torch.no_grad():
                out = model.generate(input_ids=ids, attention_mask=att, do_sample=True, temperature=CFG['temperature'], top_p=1.0, top_k=0,
                                     max_new_tokens=CFG['max_tokens'], pad_token_id=tok.eos_token_id)
            gen = out[0, ids.shape[1]:]
            text = tok.decode(gen, skip_special_tokens=True)
            fin = 'stop' if int(gen[-1]) in eos else ('length' if len(gen) >= CFG['max_tokens'] else 'other')
            recs.append({'model_key': 'Swallow', 'model': MID, 'place': 'colab-bf16', 'lang': lang, 'task': int(task), 'sample': s, 'system': CFG['system'][lang],
                         'prompt': CFG['tasks'][task][lang], 'temperature': CFG['temperature'], 'max_tokens': CFG['max_tokens'], 'tasks_sha16': CFG['tasks_sha16'],
                         'text': text, 'finish_reason': fin, 'usage': {'prompt_tokens': int(ids.shape[1]), 'completion_tokens': int(len(gen))}, 'error': None,
                         'system_mode': 'system', 'n_thought_parts': 0, 'attempts': 1})
            print('%s t%s s%d done (%d tok)' % (lang, task, s, len(gen)))
path = '/content/raw-swallow.jsonl'
open(path, 'w', encoding='utf-8', newline='\n').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
sha = hashlib.sha256(open(path, 'rb').read()).hexdigest().upper()[:16]
print('SWALLOW-DONE n=%d sha16=%s secs=%d transformers=%s torch=%s gpu=%s' % (len(recs), sha, time.time() - t0, transformers.__version__, torch.__version__, torch.cuda.get_device_name(0)))
from google.colab import files
files.download(path)
