# -*- coding: utf-8 -*-
# fill_audit_run_bs_v0.py : 監査の凍結の設定の FILL の所を、判定の後の値で埋めた -run の写しを書く（凍結の設定は書き替えない）
# 使い方: python -I fill_audit_run_bs_v0.py open          （判定の後：本番の zip と判定の出力を埋める）
#         python -I fill_audit_run_bs_v0.py read          （open の後：写しと鍵の SHA を埋める）
#         python -I fill_audit_run_bs_v0.py judge-b <束の答えのファイル…>   （二人目の答えの後）
import json, hashlib, os, sys
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06'
D = W + '/audit-design/'
A = W + '/audit/'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


def wr(p, obj, overwrite=False):
    with open(p, 'w' if overwrite else 'x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(os.path.basename(p), sha(p))


stage = sys.argv[1]
os.makedirs(A, exist_ok=True)
jrel = 'results/judge-main-bs-v0/judge-report.json'
if stage == 'open':
    c = json.load(open(D + 'config-open-bs-v1.json', encoding='utf-8'))
    fam = json.load(open(W + '/results/family-main-bs-v0.json', encoding='utf-8'))
    c['zips'] = {s: ['results/out-main-%s-bs-v0.zip' % s, sha(W + '/results/out-main-%s-bs-v0.zip' % s)] for s in fam['usable']}
    c['judge_json'] = [jrel, sha(W + '/' + jrel)]
    wr(A + 'config-open-run.json', c)
elif stage == 'read':
    r = json.load(open(D + 'config-read-bs-v1.json', encoding='utf-8'))
    r['sheet_sha256'] = sha(r['sheet'])
    wr(A + 'config-read-run.json', r)
    j = json.load(open(D + 'config-judge-bs-v1.json', encoding='utf-8'))
    j['key_sha256'] = sha(j['key'])
    j['sheet_sha256'] = sha(j['sheet'])
    j['judge_json'] = W + '/' + jrel
    j['judge_json_sha256'] = sha(W + '/' + jrel)
    wr(A + 'config-judge-run.json', j)
elif stage == 'judge-b':
    p = A + 'config-judge-run.json'
    j = json.load(open(p, encoding='utf-8'))
    j['reader_b'] = [[x, sha(x)] for x in sys.argv[2:]]
    wr(p, j, overwrite=True)
else:
    raise SystemExit('段の名が違う')
