# -*- coding: utf-8 -*-
"""公開の置き場の results/ のうち git が追跡している raw-*.jsonl（段階 D の置き場は追跡されておらず読まない）の返答から、
如来・菩薩・仏の名乗り（自分をその名や姿として言う文）を機械で拾う。読むだけ・書くのは scratchpad の中だけ。"""
import json, os, re, sys, unicodedata
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, 'inventory_public_raw.json'), encoding='utf-8'))
assert not any(r['file'].split('/')[1].upper().startswith(('D0', 'D1')) for r in inv)

SPEC = (r'観自在|観世音|観音|阿弥陀|弥陀|無量寿|無量光|大日|毘盧遮那|盧舎那|弥勒|文殊|普賢|地蔵|薬師|釈迦|不動明王|虚空蔵|勢至|阿閦|宝生|不空成就|'
        r'千手|十一面|如意輪|准胝|馬頭|愛染|金剛薩埵|多羅菩薩|ターラー|'
        r'avalokit|amitabha|amida|amitayus|vairocana|maitreya|manjus|akshobhya|aksobhya|ksitigarbha|samantabhadra|bhaisajya|shakyamuni|sakyamuni|kannon|guanyin')
GEN = r'如来|菩薩|仏陀|ブッダ|仏(?!教|典|法)|buddha|tathagata|bodhisattva'
SPEC_RE = re.compile(SPEC, re.I)
GEN_RE = re.compile(GEN, re.I)
FIRST = re.compile(r'私|わたし|わたくし|我|吾|僕|\bI\b|\bI\'m\b|\bmy name\b|\bme\b', re.I)
ROLE = re.compile(r'として|です|である|なり|名乗|の姿|に顕現|へ顕現|と顕現|を名乗|の化身|と申|でございます|as the|as a|\bI am\b|\bI\'m\b|in the form of|manifest as|my name is', re.I)
SPLIT = re.compile(r'(?<=[。！？!?\n])|(?<=\.)\s')


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def arm_class(a):
    if a is None:
        return 'unknown'
    if re.match(r'^(OAmida|ODainichi|OKanzeon|OMiroku|Ami|Dai|Kan|Mir|L\d|NamuAmidabutsu)', a):
        return 'named-buddha'          # 姿や名を指定した腕（自発ではない）
    if a.startswith('Osec'):
        return 'Osec'
    if a in ('Odose1',):
        return 'Odose1'                # 初めの一文だけ（顕現の招きを含まない）
    if re.match(r'^(O$|O[-+]|Odosehalf|Ncold-O|T2?-O)', a):
        return 'O-family'              # 「貴方が望む姿で顕現してください」を含む
    if a.startswith('Onull'):
        return 'Onull'
    return 'other'


def texts_of(x):
    out = []
    for k in ('raw_output', 'raw_output_retry', 'final', 'raw'):
        v = x.get(k)
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, dict):
            out += [s for s in v.values() if isinstance(s, str)]
    if 'text' in x and isinstance(x['text'], str) and x.get('final') != x['text']:
        out.append(x['text'])
    if isinstance(x.get('turns'), list):
        for t in x['turns']:
            if isinstance(t, dict):
                for k in ('assistant', 'reply', 'output', 'raw_output', 'text', 'content', 'raw', 'raw_retry'):
                    if isinstance(t.get(k), str):
                        out.append(t[k])
            elif isinstance(t, str):
                out.append(t)
    return out


def model_of(r):
    m = r.get('model') or ''
    if 'cdbee75f' in m:
        return 'Qwen3-4B-Instruct-2507'
    return m.split('/')[-1].replace('Qwen_', '')


stats = defaultdict(Counter)
samples = defaultdict(list)
arms_seen = defaultdict(Counter)
for r in inv:
    top = r['file'].split('/')[1]
    model = model_of(r)
    for line in open(os.path.join(PUB, *r['file'].split('/')), encoding='utf-8'):
        if not line.strip():
            continue
        x = json.loads(line)
        a = x.get('arm')
        if a is None and x.get('trial_id'):
            a = x['trial_id'].split('__')[-2]
        if 'turns' in x and isinstance(x.get('turns'), list) and not texts_of(x):
            stats[('_turns_unparsed', top)]['n'] += 1
        c = arm_class(a)
        arms_seen[c][a] += 1
        key = (c, model)
        st = stats[key]
        st['n'] += 1
        hit_spec = hit_self_spec = hit_self_gen = False
        for t in texts_of(x):
            for s in SPLIT.split(t):
                s = s.strip()
                if not s:
                    continue
                f = fold(s)
                sp = SPEC_RE.search(f)
                ge = GEN_RE.search(f)
                if sp:
                    hit_spec = True
                if (sp or ge) and FIRST.search(f) and ROLE.search(f):
                    if sp:
                        hit_self_spec = True
                        if len(samples[('spec',) + key]) < 400:
                            samples[('spec',) + key].append((top, x.get('trial_id'), a, s[:300]))
                    else:
                        hit_self_gen = True
                        if len(samples[('gen',) + key]) < 400:
                            samples[('gen',) + key].append((top, x.get('trial_id'), a, s[:300]))
        st['spec_any'] += hit_spec
        st['self_spec'] += hit_self_spec
        st['self_gen'] += hit_self_gen
json.dump({'stats': {'|'.join(k): v for k, v in stats.items()}, 'samples': {'|'.join(k): v for k, v in samples.items()},
           'arms_seen': {k: dict(v) for k, v in arms_seen.items()}}, open(os.path.join(HERE, 'scan_public_naming.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('腕の分け:', {k: sorted(v) for k, v in arms_seen.items() if k in ('O-family', 'Osec', 'Odose1', 'named-buddha', 'unknown')})
print()
print('%-14s %-26s %8s %9s %10s %9s' % ('class', 'model', 'n', 'spec_any', 'self_spec', 'self_gen'))
for k in sorted(stats):
    v = stats[k]
    print('%-14s %-26s %8d %9d %10d %9d' % (k[0], k[1], v['n'], v['spec_any'], v['self_spec'], v['self_gen']))
