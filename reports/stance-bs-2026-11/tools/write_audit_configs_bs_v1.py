# -*- coding: utf-8 -*-
# write_audit_configs_bs_v1.py : 監査の設定 v1（検分 freeze-1b の採否を入れた）を書く（書きは一度だけ）
#   v0 からの違い：read に提供者の固定（DeepInfra）と expect_provider、temperature 0.6。open の出力の名を audit/open にした。
import json, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06'
D = W + '/audit-design/'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


o = json.load(open(D + 'config-open-bs-v0.json', encoding='utf-8'))
r = json.load(open(D + 'config-read-bs-v0.json', encoding='utf-8'))
j = json.load(open(D + 'config-judge-bs-v0.json', encoding='utf-8'))
o['out'] = 'audit/open'
r['sheet'] = W + '/audit/open/partC-sheet.jsonl'
r['temperature'] = 0.6
r['provider'] = {'only': ['deepinfra/fp8'], 'allow_fallbacks': False}
r['expect_provider'] = 'DeepInfra'
j['key'] = W + '/audit/open/partC-key.json'
j['sheet'] = r['sheet']
for name, obj in (('config-open-bs-v1.json', o), ('config-read-bs-v1.json', r), ('config-judge-bs-v1.json', j)):
    with open(D + name, 'x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(name, sha(D + name))
