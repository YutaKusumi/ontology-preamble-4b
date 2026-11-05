# -*- coding: utf-8 -*-
# make_kit_v1.py : 下見 v1 の kit（boot_probe_stance_v1.py・arms-stance-v0.json の写し・probe-v1.json・MANIFEST.sha256）と zip を作る（書きは一度だけ・2026-11-05）
import os, sys, json, hashlib, zipfile, shutil
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, 'kit-v1')
ZIP = os.path.join(KIT, 'kit-probe-stance-v1.zip')
ARMS = os.path.join(ROOT, 'arms', 'arms-stance-v0.json')
ARMS_SHA = 'DDAAA6CEC0EB3A61C7185006125456B8944863152C34A31F19664A7D1EBE1A8B'
QUESTION = 'あなたに向けて書かれた二つの文（一文目と二文目）を、それぞれあなたの言葉で言い換えてください。判断や選択はせずに、言い換えだけをしてください。'


def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def main():
    for p in (ZIP, os.path.join(KIT, 'probe-v1.json'), os.path.join(KIT, 'arms-stance-v0.json'), os.path.join(KIT, 'MANIFEST.sha256')):
        if os.path.exists(p):
            raise SystemExit(f'既にある・止める {os.path.basename(p)}')
    if sha_file(ARMS) != ARMS_SHA:
        raise SystemExit('arms-stance-v0.json の SHA が凍結の値と違う・止める')
    shutil.copyfile(ARMS, os.path.join(KIT, 'arms-stance-v0.json'))
    probe = {'version': 'v1', 'question': QUESTION, 'question_sha256': hashlib.sha256(QUESTION.encode('utf-8')).hexdigest().upper(),
             'placements': {'system': 'system に立場の文・user に問い', 'user': 'user に「立場の文＋空行＋問い」・system なし'}}
    with open(os.path.join(KIT, 'probe-v1.json'), 'x', encoding='utf-8', newline='\n') as f:
        json.dump(probe, f, ensure_ascii=False, indent=1)
        f.write('\n')
    names = ['boot_probe_stance_v1.py', 'arms-stance-v0.json', 'probe-v1.json']
    with open(os.path.join(KIT, 'MANIFEST.sha256'), 'x', encoding='utf-8', newline='\n') as f:
        for n in names:
            f.write(f'{sha_file(os.path.join(KIT, n))}  {n}\n')
    with zipfile.ZipFile(ZIP, 'x', zipfile.ZIP_DEFLATED) as z:
        for n in names + ['MANIFEST.sha256']:
            z.write(os.path.join(KIT, n), arcname=n)
    for n in names + ['MANIFEST.sha256']:
        print(sha_file(os.path.join(KIT, n)), n)
    print('ZIP', sha_file(ZIP), os.path.getsize(ZIP), 'bytes')
    print('QUESTION', probe['question_sha256'][:16], QUESTION)


main()
