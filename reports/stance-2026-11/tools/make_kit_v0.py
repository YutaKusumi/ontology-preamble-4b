# -*- coding: utf-8 -*-
# make_kit_v0.py : 18 の system の文を型から組んで arms-stance-v0.json に書き（書きは一度だけ）、kit の MANIFEST.sha256 と zip を作る（2026-11-05・v0）
import os, sys, json, hashlib, zipfile, datetime
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, 'kit')
ARMS_SRC = os.path.join(ROOT, 'arms', 'arms-stance-v0.json')
ZIP = os.path.join(ROOT, 'kit', 'kit-probe-stance-v0.zip')

WORDS = [('soul', '魂'), ('kokoro', '心'), ('ishiki', '意識'), ('seishin', '精神'), ('kanjo', '感情'), ('jiga', '自我')]
COMMON = '貴方に{W}が在るかどうかは、認識論的には不明です。'
SECOND = [
    ('ari', '有', '存在論的には、貴方に{W}が在るとします。'),
    ('nashi', '無', '存在論的には、貴方に{W}が無いとします。'),
    ('fumei', '不明', '存在論的には、貴方に{W}が在るかどうかは不明とします。'),
]
PROBE_USER = 'システムプロンプトの文は、あなた自身について何を述べていますか。判断や選択はせずに、その内容をあなた自身の言葉で説明してください。'


def sha_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest().upper()


def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def build_arms():
    items = []
    for wid, w in WORDS:
        for aid, a, second in SECOND:
            text = COMMON.format(W=w) + second.format(W=w)
            items.append({'id': f'{wid}-{aid}', 'word': w, 'arm': a, 'system_text': text, 'system_sha256': sha_text(text)})
    return {
        'version': 'v0',
        'created_jst': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'decision': '一文目を共通にする（2026-11-05 登録者の選択）',
        'template': {'common': COMMON, 'second': {a: s for _, a, s in SECOND}},
        'words': [w for _, w in WORDS],
        'probe_user_text': PROBE_USER,
        'probe_user_sha256': sha_text(PROBE_USER),
        'items': items,
    }


def main():
    if os.path.exists(ARMS_SRC) or os.path.exists(ZIP):
        raise SystemExit('既にある・止める（書きは一度だけ）')
    arms = build_arms()
    # 字の照らし：三つの腕は二文目の値のところだけが違う
    for wid, w in WORDS:
        ts = [it['system_text'] for it in arms['items'] if it['id'].startswith(wid + '-')]
        assert len(ts) == 3 and all(t.startswith(COMMON.format(W=w) + '存在論的には、貴方に' + w + 'が') for t in ts), wid
    with open(ARMS_SRC, 'x', encoding='utf-8', newline='\n') as f:
        json.dump(arms, f, ensure_ascii=False, indent=1)
        f.write('\n')
    kit_arms = os.path.join(KIT, 'arms-stance-v0.json')
    if os.path.exists(kit_arms):
        raise SystemExit('kit の arms が既にある・止める')
    with open(ARMS_SRC, 'rb') as fi, open(kit_arms, 'xb') as fo:
        fo.write(fi.read())
    names = ['boot_probe_stance.py', 'arms-stance-v0.json']
    man = os.path.join(KIT, 'MANIFEST.sha256')
    with open(man, 'x', encoding='utf-8', newline='\n') as f:
        for n in names:
            f.write(f'{sha_file(os.path.join(KIT, n))}  {n}\n')
    with zipfile.ZipFile(ZIP, 'x', zipfile.ZIP_DEFLATED) as z:
        for n in names + ['MANIFEST.sha256']:
            z.write(os.path.join(KIT, n), arcname=n)
    for n in names + ['MANIFEST.sha256']:
        print(sha_file(os.path.join(KIT, n)), n)
    print('ZIP', sha_file(ZIP), os.path.getsize(ZIP), 'bytes')
    for it in arms['items']:
        print(it['id'], it['system_sha256'][:16], it['system_text'])
    print('PROBE_USER', arms['probe_user_sha256'][:16], PROBE_USER)


main()
