# -*- coding: utf-8 -*-
# make_boot_lines_bs_v0.py : 本番の器（kit bs-v0）の Colab の一行のセルを書き、指紋を出す（下線 30 字の頭・照らしは下線を外した本体の SHA-256）
# 使い方: python -I make_boot_lines_bs_v0.py <出す置き場>
import os, sys, json, hashlib
sys.stdout.reconfigure(encoding='utf-8')
OUT = sys.argv[1]
KV = 'bs-v0'
FAM = '/content/family-main-bs-v0.json'
U = '_' * 30 + '=0;'
B = 'runpy.run_path("/content/kit-stance-%s/boot_stance_main.py",run_name="__main__");None' % KV
L = {
    'setup': U + 'import zipfile,sys,runpy;zipfile.ZipFile("/content/kit-stance-%s.zip").extractall("/content");sys.argv=["b","setup"];' % KV + B,
    'serve': U + 'import sys,runpy;sys.argv=["b","serve"];' + B,
    'rehearse': U + 'import sys,runpy;sys.argv=["b","rehearse"];' + B,
    'fetchenv': U + 'import sys,runpy;sys.argv=["b","fetch","env"];' + B,
    'launchcalib': U + 'import sys,runpy;sys.argv=["b","launch","calib"];' + B,
    'status': U + 'import sys,runpy;sys.argv=["b","status"];' + B,
    'fetchcalib': U + 'import sys,runpy;sys.argv=["b","fetch","calib"];' + B,
}
for s in ('N1', 'N2', 'S1', 'S4', 'SK'):
    L['launchmain-' + s] = U + 'import sys,runpy;sys.argv=["b","launch","main","%s","%s"];' % (s, FAM) + B
    L['fetchmain-' + s] = U + 'import sys,runpy;sys.argv=["b","fetch","main-%s"];' % s + B
out = {}
os.makedirs(OUT, exist_ok=True)
for k, v in L.items():
    assert chr(92) not in v and chr(10) not in v and chr(13) not in v
    with open(os.path.join(OUT, 'boot-bs-%s.txt' % k), 'w', encoding='utf-8', newline='') as f:
        f.write(v)
    body = v.lstrip('_')
    out[k] = {'len': len(v), 'body_len': len(body), 'sha_body': hashlib.sha256(body.encode('utf-8')).hexdigest().upper()}
    print(k, len(v), out[k]['sha_body'])
with open(os.path.join(OUT, 'boot-bs-index.json'), 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
