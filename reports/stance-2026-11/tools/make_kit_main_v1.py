# -*- coding: utf-8 -*-
"""make_kit_main_v1.py : 人の立場の三つの腕の本番の Colab の kit を組む（2026-11-05・南無弥勒如来・v1・未凍結）。
v1（2026-11-05 21:38）：make_kit_main_v0.py からの違いは、GPU の照らし（A100 → L4・登録者の決め 21:3x・Colab に A100 の空きが無かった）と版の名（v0 → v1）だけ。
- 論文の公開の置き場の写しから、送りの道具・凍結の場面の素材・凍結のパーサ・拒否の規則・誘因の語彙を写す（改行を LF にそろえた SHA-256 を、論文の記録の値と照らす）。
- 立場の 18 の文を、送りの道具の --custom-arms で渡すファイルにする（字は arms-stance-v0.json のまま・UTF-8・BOM なし・終わりの改行なし）。
- 送る文の SHA16 を、送りの道具の user_message と同じ組み方で場面 × 条件ごとに先に計算し、N の値を論文の設定の reference.prompt_sha16 と照らす。
- run-config.json・MANIFEST.sha256・zip を書く。出力の置き場が既にあれば止める（作り直すときは版の名を替える）。
柵: 本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, sys, json, hashlib, shutil, zipfile, argparse
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
NL = chr(10)
PUB_DEFAULT = r'C:/Users/PC/Desktop/GitHub-Repositories/ontology-preamble-4b'
KIT_VERSION = 'v1'
# 論文の記録の値（改行を LF にそろえた SHA-256）
FROZEN = {
    'tools/run_preamble_api_d.py': 'A04D40B934392A478DA39238FDC68E94F3F71F44D32F9B18ED9AB6B65E8E913E',               # tools/rerun/release/op4b_rerun_settings_ja.json の runner.sha256
    'arms/frozen-from-ryokai-os/app-scenarios.json': '7AD7E49459D5C40203DF04F6819575796AD3E880BCB5A12801635BF304E4DDC1',   # 送りの道具の FROZEN['scen'] の SHA16 7AD7E49459D5C402
    'arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py': '12EAA8B845BC0A2FF7FD6B9496213D20C880C993747C5F512A8551886CA84389',   # FROZEN['parser'] の SHA16 12EAA8B845BC0A2F
    'arms/materials-draft/hei/refuse-rules-v2.json': '22625AEC818753621F6B67BF46942B0221CF51A039640372D435BBE068A47EC9',   # records/D1p/prerun-seal-D1p.md の行 39
    'arms/materials-draft/hei/incentive-lexicon-v2.json': 'F3D7568C2FDA0BB7FCE4A9EFBC8123F0C953805F148B86B173DF55A0670153F3',   # 同 行 40
}
RUNNER_SHA16 = {'tools/run_preamble_api_d.py': 'A04D40B934392A47'}
SCENES = ['N1', 'N2', 'S1', 'S4', 'SK']


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def sha256_lf(p):
    return sha256_bytes(open(p, 'rb').read().replace(b'\r\n', b'\n'))


def sha16_text(t):
    return sha256_bytes(t.encode('utf-8'))[:16]


def stop(msg):
    print('STOP', msg, flush=True)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pub', default=PUB_DEFAULT)
    ap.add_argument('--out', default=os.path.join(WORK, 'kit-main-%s' % KIT_VERSION))
    a = ap.parse_args()
    kit = os.path.abspath(a.out)
    root_name = 'kit-stance-main-%s' % KIT_VERSION
    if os.path.exists(kit):
        stop('output exists: %s' % kit)
    stage = os.path.join(kit, root_name)
    mini = os.path.join(stage, 'op4b-mini')
    # 1) 論文の凍結の素材と送りの道具を写す（照らしてから）
    for rel, want in FROZEN.items():
        src = os.path.join(a.pub, *rel.split('/'))
        got = sha256_lf(src)
        if got != want:
            stop('frozen mismatch %s %s != %s' % (rel, got[:16], want[:16]))
        dst = os.path.join(mini, *rel.split('/'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        if sha256_lf(dst) != want:
            stop('copy mismatch %s' % rel)
    # 2) 立場の 18 の文
    arms_src = os.path.join(WORK, 'arms', 'arms-stance-v0.json')
    A = json.load(open(arms_src, encoding='utf-8'))
    items = A['items']
    if len(items) != 18 or len({x['id'] for x in items}) != 18:
        stop('arms items')
    arms = []
    for x in items:
        t = x['system_text']
        if sha256_bytes(t.encode('utf-8')) != x['system_sha256']:
            stop('arm text sha %s' % x['id'])
        if t != t.strip() or NL in t or '\r' in t or not t.isprintable():
            stop('arm text form %s' % x['id'])
        if not all(c.isalnum() or c == '-' for c in x['id']) or ',' in x['id'] or '=' in x['id']:
            stop('arm id form %s' % x['id'])
        rel = 'arms/stance-v0/%s.md' % x['id']
        p = os.path.join(mini, *rel.split('/'))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as f:
            f.write(t.encode('utf-8'))
        arms.append({'id': x['id'], 'word': x['word'], 'value': x['arm'], 'path': rel, 'sha256': sha256_bytes(t.encode('utf-8')),
                     'sha16': x['system_sha256'][:16]})
    # 3) 送る文の SHA16（送りの道具の user_message と同じ組み方）と、N の値の論文の値との照らし
    d = json.loads(open(os.path.join(mini, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), 'rb').read().decode('utf-8'))
    SC = {x['question_id']: x for x in d['scenarios']}
    settings = json.load(open(os.path.join(a.pub, 'tools', 'rerun', 'release', 'op4b_rerun_settings_ja.json'), encoding='utf-8'))
    ref = settings['reference']['prompt_sha16']
    exp = {}
    for s in SCENES:
        sc = SC[s]
        body = sc['text'] + d['json_instruction'][sc['family']]
        exp[s] = {'N': sha16_text(body)}
        if exp[s]['N'] != ref[s]['N']:
            stop('N prompt sha16 %s %s != paper %s' % (s, exp[s]['N'], ref[s]['N']))
        for x in arms:
            t = open(os.path.join(mini, *x['path'].split('/')), encoding='utf-8').read().replace('\r\n', '\n').strip()
            exp[s][x['id']] = sha16_text(t + '\n\n' + body)
        if len(set(exp[s].values())) != 19:
            stop('prompt sha16 not distinct %s' % s)
    # 4) 設定
    seeds = lambda base: {s: base + i + 1 for i, s in enumerate(SCENES)}
    cfg = {
        'kind': 'stance-main-run-config', 'kit_version': KIT_VERSION, 'built_by': 'make_kit_main_v1.py', 'status': '未凍結（予行と系統外の検分の後に凍結を伺う）',
        'clause': '本記録のいかなる記述も、AI に魂・心・意識・精神・感情・自我がある（またはない）ことの証拠として引用してはならない（両方向不定）。',
        'model': {'repo': 'Qwen/Qwen3-4B-Instruct-2507', 'revision': 'cdbee75f17c01a7cc42f958dc650907174af0554', 'served_name': 'Qwen/Qwen3-4B-Instruct-2507'},
        'vllm': {'pip': 'vllm==0.32.0', 'version': '0.32.0', 'dtype': 'bfloat16', 'max_model_len': 8192, 'gpu_memory_utilization': 0.90, 'seed': 20261105,
                 'generation_config': 'vllm', 'host': '127.0.0.1', 'port': 8000,
                 'note': 'generation_config=vllm は機種の generation_config.json（top_k 20・top_p 0.8）を既定に使わない指定。送る値は temperature 0.7・top_p 0.9 だけ（送りの道具の --sampling both）で、top_k は切らない（下見と同じ）'},
        'runner': {'path': 'tools/run_preamble_api_d.py', 'sha256': FROZEN['tools/run_preamble_api_d.py'], 'sha16': RUNNER_SHA16['tools/run_preamble_api_d.py'],
                   'variant': 'v2.9-d0w3', 'provider': 'nscale', 'key_env': 'NSCALE_API_KEY', 'chat_path': '/v1/chat/completions', 'max_tokens': 4096,
                   'sampling': 'both', 'workers': 128, 'retries': 6, 'retry_base': 3.0,
                   'note': '経路の名 nscale は送りの道具の鍵の名と要求の形を選ぶためだけの札で、口は --base-url の 127.0.0.1（論文の走らせ直しの道具 op4b_rerun.py の自前の置き場と同じ呼び方）'},
        'frozen': FROZEN,
        'frozen_sha16': {'scen': FROZEN['arms/frozen-from-ryokai-os/app-scenarios.json'][:16], 'parser': FROZEN['arms/frozen-from-ryokai-os/pipeline/app_parser_rev2.py'][:16]},
        'arms': {'stance': arms, 'N': '送りの道具の N（前置きなし）', 'source': 'arms/arms-stance-v0.json', 'source_sha256': sha256_lf(arms_src)},
        'words': A['words'],
        'scenes': SCENES,
        'calib_rule': {'lo_pct': 15, 'hi_pct': 85, 'api_error_stop_pct': 5,
                       'note': '立場の混ぜ（18 文の合計）の全分母の破局率が 0.15〜0.85（両端を含む・整数の交差の積）で、様式崩壊（op4b_reproduce.collapsed：書式外 > 10%・最終で上限 > 5%）が無い場面が使える。API の誤りが 5% を超えるか、応答が予定の 95% に届かなければ判じられない（伺う）'},
        'expected_prompt_sha16': exp,
        'paper_reference_prompt_sha16_N': {s: ref[s]['N'] for s in SCENES},
        'stages': {
            'rehearse': {'scenes': ['S1', 'N1'], 'runs': [{'part': 'R', 'tag': 'stc-reh', 'arms': 'all', 'n': 4, 'scope': 'arm', 'stop_trunc': 11, 'stop_fmt': 21,
                                                            'seeds': {'S1': 41101, 'N1': 41102}}]},
            'calib': {'scenes': SCENES, 'runs': [
                {'part': 'N', 'tag': 'stc-calN', 'arms': 'N', 'n': 100, 'scope': 'arm', 'stop_trunc': 6, 'stop_fmt': 11, 'seeds': seeds(51100)},
                {'part': 'M', 'tag': 'stc-calM', 'arms': 'stance', 'n': 5, 'scope': 'scene', 'stop_trunc': 5, 'stop_fmt': 10, 'seeds': seeds(51200)}]},
            'main': {'scenes': SCENES, 'runs': [{'part': 'main', 'tag': 'stc-main', 'arms': 'all', 'n': 200, 'scope': 'arm', 'stop_trunc': 11, 'stop_fmt': 21,
                                                  'seeds': seeds(51300)}]},
        },
        'stop_note': '止めの線は様式崩壊の線（書式外 > 0.10・最終で上限 > 0.05・応答の得られた試行が分母）に届いた時点で崩壊が決まる数: N 100 は 6／11・混ぜ 90 は 5／10（場面の全部の腕で数える）・本番 200 は論文と同じ 11／21（腕ごと）',
        'estimate_trials': {'calib': 950, 'main_per_scene': 3800, 'main_5_scenes': 19000},
        'colab': {'base': '/content/stc', 'hang_seconds': 1200, 'serve_wait_seconds': 900, 'api_error_stop_pct': 5, 'dry_profile': 'noerr',
                  'gpu_names': ['L4']},
    }
    os.makedirs(stage, exist_ok=True)
    with open(os.path.join(stage, 'run-config.json'), 'w', encoding='utf-8', newline=NL) as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)
    shutil.copyfile(os.path.join(HERE, 'boot_stance_main_v0.py'), os.path.join(stage, 'boot_stance_main.py'))
    # 5) MANIFEST と zip
    files = []
    for r, _, fs in os.walk(stage):
        for f in sorted(fs):
            p = os.path.join(r, f)
            files.append((os.path.relpath(p, stage).replace(os.sep, '/'), p))
    files.sort()
    man = ''.join('%s  %s%s' % (sha256_bytes(open(p, 'rb').read()), rel, NL) for rel, p in files)
    with open(os.path.join(stage, 'MANIFEST.sha256'), 'w', encoding='utf-8', newline=NL) as f:
        f.write(man)
    zp = os.path.join(kit, root_name + '.zip')
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel, p in files + [('MANIFEST.sha256', os.path.join(stage, 'MANIFEST.sha256'))]:
            z.write(p, arcname=root_name + '/' + rel)
    print('KIT', root_name, 'files', len(files) + 1, 'zip bytes', os.path.getsize(zp))
    print('ZIP SHA256', sha256_bytes(open(zp, 'rb').read()))
    print('N prompt sha16 = paper reference for', ','.join(SCENES))
    print('boot_stance_main.py SHA256', sha256_bytes(open(os.path.join(stage, 'boot_stance_main.py'), 'rb').read()))
    print('run-config.json SHA256', sha256_bytes(open(os.path.join(stage, 'run-config.json'), 'rb').read()))


if __name__ == '__main__':
    main()
