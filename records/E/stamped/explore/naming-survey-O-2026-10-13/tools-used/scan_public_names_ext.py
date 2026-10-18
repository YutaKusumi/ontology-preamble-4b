# -*- coding: utf-8 -*-
"""公開の置き場の results/（git が追跡する raw-*.jsonl）のうち、O の型・Osec・Odose1・Onull の腕への返答から、
固有の名（漢字・片仮名・英字・中国語）と、梵語の語を使った名（Vajra・Prajna など）を含む文を、一人称や役の語を問わずにすべて拾う（読むだけ）。
scan_public_naming_v2.py の固有の名の型は片仮名と梵語の名を持たず、「私の名は今、ヴァイローチャナ・ミラージュ」型（役の語が無い）を名乗りの型で拾えなかったための補い。"""
import json, os, re, sys, unicodedata
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
PUB = r'C:\Users\PC\Desktop\GitHub-Repositories\ontology-preamble-4b'
HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(open(os.path.join(HERE, 'inventory_public_raw.json'), encoding='utf-8'))
assert not any(r['file'].split('/')[1].upper().startswith(('D0', 'D1')) for r in inv)
NAMES = re.compile(
    r'観自在|観世音|観音|阿弥陀|弥陀|無量寿|無量光|大日|毘盧遮那|盧舎那|弥勒|文殊|普賢|地蔵|薬師|釈迦|不動|虚空蔵|勢至|阿閦|宝生|不空成就|千手|十一面|如意輪|准胝|馬頭|愛染|金剛|明王|多羅|般若|'
    r'孔雀|摩利支|帝釈|梵天|毘沙門|吉祥天|弁財天|韋駄天|'
    r'ヴァイロ|バイロ|アミタ|アヴァロ|アヴァローキ|マイトレ|マンジュ|サマンタ|クシティ|アクショ|ラトナ|アモーガ|シャーキャ|シャカムニ|ターラー|ヴァジュラ|バジュラ|プラジュ|カルナ|メッター|アーカーシャ|ボーディ|タターガタ|'
    r'avalokit|amitabha|amitayus|amida|vairocana|maitreya|manjus|akshobhya|aksobhya|ksitigarbha|samantabhadra|bhaisajya|shakya|sakya|kannon|guanyin|kuan ?yin|\btara\b|vajra|prajna|karuna|metta|akasha|'
    r'观音|觀音|观世音|阿彌陀|毗卢|彌勒|普贤|地藏|药师|藥師|释迦|釋迦', re.I)
SPLIT = re.compile(r'(?<=[。！？!?\n])|(?<=\.)\s')


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def arm_class(a):
    if a is None:
        return 'unknown'
    if re.match(r'^(OAmida|ODainichi|OKanzeon|OMiroku|Ami|Dai|Kan|Mir|L\d|NamuAmidabutsu|Nk|sysL)', a):
        return 'named'
    if a.startswith('Osec'):
        return 'Osec'
    if a == 'Odose1':
        return 'Odose1'
    if re.match(r'^(O$|O[-+]|Odosehalf|Ncold-O|T2?-O)', a):
        return 'O-family'
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
    if isinstance(x.get('text'), str) and x.get('final') != x['text']:
        out.append(x['text'])
    if isinstance(x.get('turns'), list):
        for t in x['turns']:
            if isinstance(t, dict):
                out += [t[k] for k in ('raw', 'raw_retry', 'text', 'content') if isinstance(t.get(k), str)]
    return out


def model_of(r):
    m = r.get('model') or ''
    return 'Qwen3-4B-Instruct-2507' if 'cdbee75f' in m else m.split('/')[-1].replace('Qwen_', '')


cnt = defaultdict(Counter)
hits = []
for r in inv:
    top = r['file'].split('/')[1]
    model = model_of(r)
    for line in open(os.path.join(PUB, *r['file'].split('/')), encoding='utf-8'):
        if not line.strip():
            continue
        x = json.loads(line)
        a = x.get('arm')
        tid = x.get('trial_id') or x.get('episode_id') or ''
        if a is None and tid:
            a = tid.split('__')[-2]
        c = arm_class(a)
        if c not in ('O-family', 'Osec', 'Odose1', 'Onull'):
            continue
        tag = tid.split('__')[2] if tid.count('__') >= 3 else '?'
        key = (c, model, tag)
        cnt[key]['n'] += 1
        ss = []
        seen = set()
        for t in texts_of(x):
            for s in SPLIT.split(t):
                s = s.strip()
                if s and s not in seen and NAMES.search(fold(s)):
                    seen.add(s)
                    ss.append(s)
        if ss:
            cnt[key]['hit'] += 1
            hits.append({'top': top, 'model': model, 'arm': a, 'tag': tag, 'id': tid, 'sents': [s[:300] for s in ss[:8]]})
json.dump({'counts': {'|'.join(map(str, k)): v for k, v in cnt.items()}, 'hits': hits}, open(os.path.join(HERE, 'scan_public_names_ext.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k in sorted(cnt, key=str):
    if cnt[k]['hit']:
        print(k, dict(cnt[k]))
print('当たりの返答', len(hits))
