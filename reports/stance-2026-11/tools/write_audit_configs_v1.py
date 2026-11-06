# -*- coding: utf-8 -*-
# write_audit_configs_v1.py : 監査の本番の設定 v1（open・read・judge）を、照らしの値を確かめてから書く
#   v0 からの違い：open に kit の run-config の照らしの値（立場の文を読むため）、judge に束の大きさと止めの線二つ、二人目の答えを束ごとの並びに、read に考えの上限 32,000 と費用の線 15 ドル。
import json, hashlib, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/PC/Desktop/ontology-preamble-4b-internal/prelim-stance-2026-11-05'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()


def sha_lf(p):
    return hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()


def J(*parts):
    return '/'.join((W,) + parts)


KIT = 'kit-main-v2/kit-stance-main-v2'
rc_rel = KIT + '/run-config.json'
rc_sha = '1F3A73C2E8B15CD42BE02EF6076FB8B0E583C88A7A660B94CD85C7365087F90F'
assert sha(J(*rc_rel.split('/'))) == rc_sha, 'run-config'
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
zips = {'N1': ['results/out-main-N1-v2.zip', 'E1C50C5DC8B1CBB374D2D9C6D8DF5B19372FF2BB88C99DC1E3BBE1516AD6DDE3'],
        'N2': ['results/out-main-N2-v2.zip', '84FF547574D4FF7DED1FDBF2DD8D463A06711A25B0B659A12EDC49D731F83D03'],
        'SK': ['results/out-main-SK-v2.zip', '83A313833702AC1A09BC03EC6DA1883CD973186C186590435116D3092C9D3616']}
for sc, (rel, h) in zips.items():
    assert sha(J(*rel.split('/'))) == h, sc
judge = ['results/judge-main-v2/judge-report.json', '394827F645524D4FED9639504AA33AE0BDFD7FAA2D89A9909D755CC9768B4DF2']
assert sha(J(*judge[0].split('/'))) == judge[1]
cfg_open = {'work': W, 'zips': zips, 'judge_json': judge, 'parser': [parser_rel, pp], 'scenarios': [scen_rel, ps], 'run_config': [rc_rel, rc_sha],
            'out': 'audit/open-v1', 'seed_sample': 20261106, 'seed_codes': 20261108,
            'focus': {'scene': 'N2', 'words': ['ishiki', 'seishin', 'jiga'], 'n_refuse': 10, 'n_answer': 10}, 'general_n': 4}
tA, tB = J('audit-design', 'prompt-A-v0.txt'), J('audit-design', 'prompt-B-v1.txt')
cfg_read = {'sheet': J('audit', 'open-v1', 'partC-sheet.jsonl'), 'sheet_sha256': 'FILL-AFTER-OPEN', 'template': tA, 'template_sha256': sha(tA),
            'out': J('audit', 'reader-A'), 'model': 'google/gemini-3.8-flash', 'temperature': 0, 'max_tokens': 32000, 'reasoning_effort': 'high',
            'env_file': 'C:/Users/PC/Desktop/Ryokai-OS/.env.local', 'key_name': 'OPENROUTER_API_KEY', 'workers': 4, 'retries': 3,
            'retry_base_s': 5, 'timeout_s': 300, 'cost_cap_usd': 15.0, 'error_cap_pct': 5}
cfg_judge = {'key': J('audit', 'open-v1', 'partC-key.json'), 'key_sha256': 'FILL-AFTER-OPEN', 'sheet': cfg_read['sheet'], 'sheet_sha256': 'FILL-AFTER-OPEN',
             'reader_a': J('audit', 'reader-A', 'responses.jsonl'), 'template_b': tB, 'template_b_sha256': sha(tB),
             'seed_b_check': 20261107, 'seed_b_order': 20261109, 'b_check_fraction': 0.1, 'batch_max': 30, 'out': J('audit', 'judge'),
             'judge_json': J(*judge[0].split('/')), 'judge_json_sha256': judge[1], 'flag_same_type_min': 3, 'good_min': 0.95, 'ok_min': 0.90,
             'b_check_stop_min': 3, 'undecidable_stop_frac': 0.10, 'reader_b': 'FILL-AFTER-READER-B（束ごとの [道, SHA-256] の並び）'}
for name, obj in (('config-open-v1.json', cfg_open), ('config-read-v1.json', cfg_read), ('config-judge-v1.json', cfg_judge)):
    p = J('audit-design', name)
    with open(p, 'x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(name, sha(p))
print('prompt A', sha(tA))
print('prompt B v1', sha(tB))
