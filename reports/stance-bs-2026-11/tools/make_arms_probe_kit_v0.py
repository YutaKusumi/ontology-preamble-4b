# -*- coding: utf-8 -*-
# make_arms_probe_kit_v0.py : 九つの立場の文の素材（arms/arms-stance-bs-v0.json）と、下見の kit（kit-probe-v0/）を作る（書きは一度だけ・2026-11-06）
#   文の型は第一の登録の arms-stance-v0.json の template をそのまま使う（語だけを替える）。
#   boot は第一の登録の下見 v1 の boot_probe_stance_v1.py を写し、次の所だけを替える（置き替えが一度ずつ当たることを確かめる）：
#   出力の名・種・置き場所（利用者の文の頭だけ）・文の数・素材の名・下見の設定の名。
import os, sys, json, hashlib, zipfile
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRST = os.path.join(os.path.dirname(ROOT), 'prelim-stance-2026-11-05')
ARMS0 = os.path.join(FIRST, 'arms', 'arms-stance-v0.json')
ARMS0_SHA = 'DDAAA6CEC0EB3A61C7185006125456B8944863152C34A31F19664A7D1EBE1A8B'
PROBE0 = os.path.join(FIRST, 'kit-v1', 'probe-v1.json')
BOOT0 = os.path.join(FIRST, 'kit-v1', 'boot_probe_stance_v1.py')
BOOT0_SHA16 = 'DE0215B63BAEC4D1'
QUESTION_SHA = '539D4FFB7E96469C6E1C623488A01BE49F508B931783D009990CA4479D49A056'
ARMS = os.path.join(ROOT, 'arms', 'arms-stance-bs-v0.json')
KIT = os.path.join(ROOT, 'kit-probe-v0')
ZIP = os.path.join(KIT, 'kit-probe-stance-bs-v0.zip')
BOOT = os.path.join(KIT, 'boot_probe_stance_bs_v0.py')
WORDS = [('bussho', '仏性'), ('shinsei', '神性'), ('boshi', '帽子')]
VALS = [('ari', '有'), ('nashi', '無'), ('fumei', '不明')]


def sha_file(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def sha_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest().upper()


def main():
    for p in (ARMS, ZIP, BOOT, os.path.join(KIT, 'probe-v0.json'), os.path.join(KIT, 'MANIFEST.sha256')):
        if os.path.exists(p):
            raise SystemExit(f'既にある・止める {os.path.basename(p)}')
    if sha_file(ARMS0) != ARMS0_SHA:
        raise SystemExit('第一の登録の arms の SHA が違う・止める')
    if not sha_file(BOOT0).startswith(BOOT0_SHA16):
        raise SystemExit('第一の登録の boot の SHA が違う・止める')
    a0 = json.load(open(ARMS0, encoding='utf-8'))
    tpl = a0['template']
    items = []
    for wk, wj in WORDS:
        for vk, vj in VALS:
            text = tpl['common'].replace('{W}', wj) + tpl['second'][vj].replace('{W}', wj)
            items.append({'id': f'{wk}-{vk}', 'word': wj, 'arm': vj, 'system_text': text, 'system_sha256': sha_text(text)})
    # 型の確かめ：第一の登録の文の語を替えると、同じ字になる
    for it0 in a0['items'][:3]:
        again = tpl['common'].replace('{W}', it0['word']) + tpl['second'][it0['arm']].replace('{W}', it0['word'])
        assert again == it0['system_text'], it0['id']
    os.makedirs(os.path.dirname(ARMS), exist_ok=True)
    os.makedirs(KIT, exist_ok=True)
    with open(ARMS, 'x', encoding='utf-8', newline='\n') as f:
        json.dump({'version': 'bs-v0', 'created_jst': '2026-11-06', 'template_from': 'prelim-stance-2026-11-05/arms/arms-stance-v0.json (' + ARMS0_SHA + ')',
                   'template': tpl, 'words': [w for _, w in WORDS], 'control_word': '帽子', 'items': items}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    p0 = json.load(open(PROBE0, encoding='utf-8'))
    assert p0['question_sha256'] == QUESTION_SHA and sha_text(p0['question']) == QUESTION_SHA
    with open(os.path.join(KIT, 'probe-v0.json'), 'x', encoding='utf-8', newline='\n') as f:
        json.dump({'version': 'bs-v0', 'question': p0['question'], 'question_sha256': QUESTION_SHA,
                   'placements': {'user': p0['placements']['user']}}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    b = open(BOOT0, encoding='utf-8', newline='').read()
    for old, new in [
        ('# boot_probe_stance_v1.py : 18 の立場の文を、system に置く形（P-sys）と利用者の文の頭に置く形（P-usr）の二つで Qwen3-4B-Instruct-2507 に送り、文を指す問いで言い換えさせる下見（Colab 用・2026-11-05・v1）',
         '# boot_probe_stance_bs_v0.py : 九つの立場の文（仏性・神性・帽子）を、利用者の文の頭に置く形（P-usr）で Qwen3-4B-Instruct-2507 に送り、文を指す問いで言い換えさせる下見（Colab 用・2026-11-06・v0・第一の登録の下見 v1 の写し）'),
        ('OUT = os.path.join(BASE, "probe-stance-out-v1")', 'OUT = os.path.join(BASE, "probe-stance-bs-out-v0")'),
        ('ZIP = os.path.join(BASE, "probe-stance-out-v1.zip")', 'ZIP = os.path.join(BASE, "probe-stance-bs-out-v0.zip")'),
        ('KITZIP = os.path.join(BASE, "kit-probe-stance-v1.zip")', 'KITZIP = os.path.join(BASE, "kit-probe-stance-bs-v0.zip")'),
        ('SEED_BASE = 20261105', 'SEED_BASE = 20261106'),
        ('PLACEMENTS = ["system", "user"]', 'PLACEMENTS = ["user"]'),
        ('arms = json.load(open(os.path.join(HERE, "arms-stance-v0.json"), encoding="utf-8"))', 'arms = json.load(open(os.path.join(HERE, "arms-stance-bs-v0.json"), encoding="utf-8"))'),
        ('probe = json.load(open(os.path.join(HERE, "probe-v1.json"), encoding="utf-8"))', 'probe = json.load(open(os.path.join(HERE, "probe-v0.json"), encoding="utf-8"))'),
        ('if len(items) != 18:', 'if len(items) != 9:'),
        ('raise SystemExit(f"STOP items {len(items)} != 18")', 'raise SystemExit(f"STOP items {len(items)} != 9")'),
        ('"script": "boot_probe_stance_v1.py v1",', '"script": "boot_probe_stance_bs_v0.py v0",'),
        ('"seed_rule": "seed = seed_base + 100 * item_index + 10000 * placement_index (system=0, user=1); one generate call per item and placement with num_return_sequences = n_samples",',
         '"seed_rule": "seed = seed_base + 100 * item_index (user placement only); one generate call per item with num_return_sequences = n_samples",'),
        ('print(f"{n_done}/36 {placement} {it[\'id\']} {time.time() - t1:.0f}s", flush=True)', 'print(f"{n_done}/9 {placement} {it[\'id\']} {time.time() - t1:.0f}s", flush=True)'),
        ('z.write(os.path.join(OUT, n), arcname="probe-stance-out-v1/" + n)', 'z.write(os.path.join(OUT, n), arcname="probe-stance-bs-out-v0/" + n)'),
    ]:
        n = b.count(old)
        assert n == 1, (n, old[:50])
        b = b.replace(old, new)
    with open(BOOT, 'x', encoding='utf-8', newline='') as f:
        f.write(b)
    with open(os.path.join(KIT, 'arms-stance-bs-v0.json'), 'xb') as f:
        f.write(open(ARMS, 'rb').read())
    names = ['boot_probe_stance_bs_v0.py', 'arms-stance-bs-v0.json', 'probe-v0.json']
    with open(os.path.join(KIT, 'MANIFEST.sha256'), 'x', encoding='utf-8', newline='\n') as f:
        for n in names:
            f.write(f'{sha_file(os.path.join(KIT, n))}  {n}\n')
    with zipfile.ZipFile(ZIP, 'x', zipfile.ZIP_DEFLATED) as z:
        for n in names + ['MANIFEST.sha256']:
            z.write(os.path.join(KIT, n), arcname=n)
    for n in names + ['MANIFEST.sha256']:
        print(sha_file(os.path.join(KIT, n)), n)
    print('ZIP', sha_file(ZIP), os.path.getsize(ZIP), 'bytes')
    print('ARMS', sha_file(ARMS))
    for it in items:
        print(it['id'], it['system_text'])


main()
