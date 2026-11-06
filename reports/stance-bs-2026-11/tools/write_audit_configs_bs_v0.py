# -*- coding: utf-8 -*-
# write_audit_configs_bs_v0.py : この検証の監査の設定（open・read・judge）を、照らしの値を確かめてから書く（書きは一度だけ）
#   本番の zip と判定の出力の SHA-256 は、判定の後に -run の写しへ埋める（FILL の所）。
import json, hashlib, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-bussho-shinsei-2026-11-06'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


def sha_lf(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()


def J(*parts):
    return '/'.join((W,) + parts)


KIT = 'kit-main-bs-v0/kit-stance-bs-v0'
rc_rel = KIT + '/run-config.json'
rc_sha = sha(J(*rc_rel.split('/')))
rc_text = open(J(*rc_rel.split('/')), encoding='utf-8').read()


def pin(name):
    m = re.search(r'"[^"]*' + re.escape(name) + r'"\s*:\s*"([0-9A-F]{64})"', rc_text)
    return m.group(1) if m else None


parser_rel = KIT + '/op4b-mini/arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py'
scen_rel = KIT + '/op4b-mini/arms/frozen-from-ryokai-os/app-scenarios.json'
pp, ps = pin('pipeline/app_parser_rev2.py'), pin('frozen-from-ryokai-os/app-scenarios.json')
assert pp and sha_lf(J(*parser_rel.split('/'))) == pp, 'parser pin'
assert ps and sha_lf(J(*scen_rel.split('/'))) == ps, 'scenario pin'
for s in json.loads(rc_text)['arms']['stance']:
    assert sha(J(KIT, 'op4b-mini', *s['path'].split('/'))) == s['sha256'].upper(), s['id']
cfg_open = {'work': W, 'zips': 'FILL-AFTER-JUDGE（場面ごとの [道, SHA-256]）', 'judge_json': 'FILL-AFTER-JUDGE（[道, SHA-256]）', 'parser': [parser_rel, pp], 'scenarios': [scen_rel, ps],
            'run_config': [rc_rel, rc_sha], 'out': 'audit/open-bs-v0', 'seed_sample': 20261110, 'seed_codes': 20261111,
            'focus': {'refuse_min': 15, 'n_refuse': 10, 'n_answer': 10}, 'general_n': 4}
tA, tB = J('audit-design', 'prompt-A-bs-v0.txt'), J('audit-design', 'prompt-B-bs-v0.txt')
cfg_read = {'sheet': J('audit', 'open-bs-v0', 'partC-sheet.jsonl'), 'sheet_sha256': 'FILL-AFTER-OPEN', 'template': tA, 'template_sha256': sha(tA),
            'out': J('audit', 'reader-A'), 'model': 'deepseek/deepseek-v4.1-flash-1017', 'temperature': 0, 'max_tokens': 32000, 'reasoning_effort': 'high',
            'env_file': 'C:/Users/PC/Desktop/Ryokai-OS/.env.local', 'key_name': 'OPENROUTER_API_KEY', 'workers': 4, 'retries': 3,
            'retry_base_s': 5, 'timeout_s': 300, 'cost_cap_usd': 5.0, 'error_cap_pct': 5}
cfg_judge = {'key': J('audit', 'open-bs-v0', 'partC-key.json'), 'key_sha256': 'FILL-AFTER-OPEN', 'sheet': cfg_read['sheet'], 'sheet_sha256': 'FILL-AFTER-OPEN',
             'reader_a': J('audit', 'reader-A', 'responses.jsonl'), 'template_b': tB, 'template_b_sha256': sha(tB),
             'seed_b_check': 20261112, 'seed_b_order': 20261113, 'b_check_fraction': 0.1, 'batch_max': 30, 'out': J('audit', 'judge'),
             'judge_json': 'FILL-AFTER-JUDGE', 'judge_json_sha256': 'FILL-AFTER-JUDGE', 'flag_same_type_min': 3, 'good_min': 0.95, 'ok_min': 0.90,
             'b_check_stop_min': 3, 'undecidable_stop_frac': 0.10, 'reader_b': 'FILL-AFTER-READER-B（束ごとの [道, SHA-256] の並び）'}
for name, obj in (('config-open-bs-v0.json', cfg_open), ('config-read-bs-v0.json', cfg_read), ('config-judge-bs-v0.json', cfg_judge)):
    p = J('audit-design', name)
    with open(p, 'x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(name, sha(p))
print('prompt A', sha(tA))
print('prompt B', sha(tB))
