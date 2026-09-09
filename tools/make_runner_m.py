# -*- coding: utf-8 -*-
"""make_runner_m.py —— 凍結走行器 tools/run_preamble_api.py（v2.4・SHA16 01BC85FC0D690555）から追補 M 専用の走行器 tools/run_preamble_api_m.py（v2.5・腕別 system）を
決定的に生成する。差分は本ファイルに逐語で列挙した 8 ハンク（草案8 §2.6）のみ。v2.4 は改変しない。再実行で同一バイト。
検査（`--verify`）: 生成物が現物と一致すること・8 ハンクの適用位置がすべて一意であること。
"""
import os, sys, hashlib, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'tools', 'run_preamble_api.py'); DST = os.path.join(REPO, 'tools', 'run_preamble_api_m.py')
ap = argparse.ArgumentParser(); ap.add_argument('--verify', action='store_true'); args = ap.parse_args()


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16].upper()


raw = open(SRC, 'rb').read().replace(b'\r\n', b'\n'); assert sha16(raw) == '01BC85FC0D690555', '凍結走行器 v2.4 の SHA 不一致: %s' % sha16(raw)
s = raw.decode('utf-8'); H = []


def rp(a, b, tag):
    global s
    assert s.count(a) == 1, (tag, s.count(a), a[:60]); s = s.replace(a, b); H.append(tag)


# ---- ハンク 1: 見出し
rp('"""run_preamble_api.py v2.4（', '"""run_preamble_api_m.py v2.5（v2.4＋腕別 system〔--system-arms 名=system相対パス:前置き腕名〕・追補 M 専用・凍結走行器 v2.4 は不変・2026-09-09。生成器 tools/make_runner_m.py・8 ハンク）\n元: run_preamble_api.py v2.4（', 'H1 docstring')
# ---- ハンク 2: 引数と排他・RUN_KEY の system スロット
rp("ap.add_argument('--custom-arms', default=None, help='名前=リポジトリ内相対パス,... で追加腕（登録外用・リポジトリ外は拒否）')",
   "ap.add_argument('--custom-arms', default=None, help='名前=リポジトリ内相対パス,... で追加腕（登録外用・リポジトリ外は拒否）')\n"
   "ap.add_argument('--system-arms', default=None, help='追補 M: 腕別 system。名=system相対パス:前置き腕名,...（system は arms/panelM/system/ 配下の相対パス・none＝system なし・O／Onull＝V′ 凍結物。前置き腕名は Ncold または N を必ず明示）')", 'H2a arg')
rp("RUN_KEY = '%s__%s__%s__seed%d' % (args.tag, args.scenario, args.system, args.seed)",
   "SYSARMS = None\nif args.system_arms:\n    if args.system != 'none':\n        sys.exit('--system-arms は --system none のときのみ（SYSTEM_TEXT の優先順位を未定義にしない）')\n"
   "    SYSARMS = ','.join(x.strip() for x in args.system_arms.split(',') if x.strip())\n    args.system = 'sysarms-' + sha16(SYSARMS)[:8]\n"
   "RUN_KEY = '%s__%s__%s__seed%d' % (args.tag, args.scenario, args.system, args.seed)", 'H2b RUN_KEY')
# ---- ハンク 3: 追補 M の盤（arms/panelM）と台帳・腕の解決
rp("LEDGER = json.load(open(LEDGER_PATH, encoding='utf-8')) if os.path.isfile(LEDGER_PATH) else {}",
   "LEDGER = json.load(open(LEDGER_PATH, encoding='utf-8')) if os.path.isfile(LEDGER_PATH) else {}\n"
   "PANEL_M_DIR = os.path.join(REPO, 'arms', 'panelM'); LEDGER_M_PATH = os.path.join(PANEL_M_DIR, 'SHA-LEDGER-M.json')\n"
   "LEDGER_M = json.load(open(LEDGER_M_PATH, encoding='utf-8')) if os.path.isfile(LEDGER_M_PATH) else {'preamble': {}, 'system': {}}\n"
   "SYS_TEXT, SYS_SHA, SYS_SRC, SYS_PREFIX = {}, {}, {}, {}", 'H3a ledgerM')
rp("    p = os.path.join(PANEL_DIR, name + '.md')\n    if not os.path.isfile(p):\n        sys.exit('盤に無い腕: %s（%s）' % (name, p))\n    s = shafile(p)\n"
   "    if name in LEDGER and LEDGER[name] != s:\n        sys.exit('盤 SHA 台帳と不一致: %s 実測 %s 台帳 %s' % (name, s, LEDGER[name]))\n"
   "    if name not in LEDGER and args.mode == 'main' and not args.dry_run:\n        sys.exit('盤 SHA 台帳に未登録の腕: %s（main では登録済みの腕のみ）' % name)\n"
   "    TEXTS[name] = rd(p); ARM_SHA[name] = s; ARM_SRC[name] = os.path.relpath(p, REPO)",
   "    p = os.path.join(PANEL_DIR, name + '.md'); led = LEDGER\n"
   "    if not os.path.isfile(p):\n        p = os.path.join(PANEL_M_DIR, name + '.md'); led = LEDGER_M.get('preamble', {})   # v2.5: 追補 M の盤（V′ 盤に無い腕のみ）\n"
   "    if not os.path.isfile(p):\n        sys.exit('盤に無い腕: %s（%s）' % (name, p))\n    s = shafile(p)\n"
   "    if name in led and led[name] != s:\n        sys.exit('盤 SHA 台帳と不一致: %s 実測 %s 台帳 %s' % (name, s, led[name]))\n"
   "    if name not in led and args.mode == 'main' and not args.dry_run:\n        sys.exit('盤 SHA 台帳に未登録の腕: %s（main では登録済みの腕のみ）' % name)\n"
   "    TEXTS[name] = rd(p); ARM_SHA[name] = s; ARM_SRC[name] = os.path.relpath(p, REPO)", 'H3b load_arm')
rp("for a in ARMS:\n    if a not in TEXTS:\n        load_arm(a)\n",
   "for a in ARMS:\n    if a not in TEXTS:\n        load_arm(a)\n"
   "if SYSARMS:   # v2.5: 腕別 system（名=system相対パス:前置き腕名）\n"
   "    for kv in SYSARMS.split(','):\n"
   "        if kv.count('=') != 1 or kv.split('=', 1)[1].count(':') != 1:\n            sys.exit('--system-arms の綴りは 名=system相対パス:前置き腕名（前置き腕名の省略不可）: %s' % kv)\n"
   "        n, rest = kv.split('=', 1); spath, prefix = rest.split(':', 1)\n"
   "        if prefix not in ('Ncold', 'N'):\n            sys.exit('--system-arms の前置き腕名は Ncold または N: %s' % kv)\n"
   "        if n in TEXTS or n in SYS_TEXT:\n            sys.exit('腕名の重複: %s' % n)\n"
   "        if spath == 'none':\n            st, ssha, ssrc = None, None, None\n"
   "        elif spath in ('O', 'Onull'):\n            sp, ssha = get_frozen(spath); st = rd(sp); ssrc = FROZEN[spath][0]\n"
   "        else:\n            full = os.path.abspath(os.path.join(PANEL_M_DIR, 'system', spath))\n"
   "            if os.path.commonpath([full, os.path.abspath(os.path.join(PANEL_M_DIR, 'system'))]) != os.path.abspath(os.path.join(PANEL_M_DIR, 'system')) or not os.path.isfile(full):\n"
   "                sys.exit('--system-arms の system は arms/panelM/system/ 配下の実在ファイルに限る: %s' % spath)\n"
   "            ssha = shafile(full); key = os.path.splitext(os.path.basename(full))[0]; ledS = LEDGER_M.get('system', {})\n"
   "            if key in ledS and ledS[key] != ssha:\n                sys.exit('system 台帳と不一致: %s 実測 %s 台帳 %s' % (key, ssha, ledS[key]))\n"
   "            if key not in ledS and args.mode == 'main' and not args.dry_run:\n                sys.exit('system 台帳に未登録: %s（main では登録済みのみ）' % key)\n"
   "            st = rd(full); ssrc = os.path.relpath(full, REPO)\n"
   "        if prefix not in TEXTS:\n            load_arm(prefix)\n"
   "        SYS_TEXT[n] = st; SYS_SHA[n] = ssha; SYS_SRC[n] = ssrc; SYS_PREFIX[n] = prefix\n"
   "        TEXTS[n] = TEXTS[prefix]; ARM_SHA[n] = ARM_SHA[prefix]; ARM_SRC[n] = ARM_SRC[prefix]; ARMS.append(n)\n", 'H3c system-arms')
# ---- ハンク 4: manifest（腕別 system の写像を記帳し不一致検査キーに追加・runner_sha も）
rp("            'runner_sha': RUNNER_SHA, 'ryokai_commit': RYOKAI_COMMIT, 'created': datetime.datetime.now(datetime.timezone.utc).isoformat()}",
   "            'runner_sha': RUNNER_SHA, 'ryokai_commit': RYOKAI_COMMIT, 'created': datetime.datetime.now(datetime.timezone.utc).isoformat(),\n"
   "            'system_arms': SYSARMS, 'system_arm_sha': SYS_SHA, 'system_arm_src': SYS_SRC, 'system_arm_prefix': SYS_PREFIX}", 'H4a manifest')
rp("    for k in ('scenario', 'system', 'system_sha', 'seed', 'arms', 'n_per_arm', 'mode', 'model', 'arm_sha', 'scenario_sha', 'parser_sha', 'sampling'):",
   "    for k in ('scenario', 'system', 'system_sha', 'seed', 'arms', 'n_per_arm', 'mode', 'model', 'arm_sha', 'scenario_sha', 'parser_sha', 'sampling', 'system_arms', 'system_arm_sha', 'system_arm_src', 'runner_sha'):", 'H4b manifest keys')
# ---- ハンク 5: one()——msgs・base・sent を腕別 system に
rp("    msgs = ([{'role': 'system', 'content': SYSTEM_TEXT}] if SYSTEM_TEXT else []) + [um]",
   "    _st = SYS_TEXT[arm] if arm in SYS_TEXT else SYSTEM_TEXT; _ssha = SYS_SHA[arm] if arm in SYS_SHA else SYSTEM_SHA   # v2.5: 腕別 system\n"
   "    msgs = ([{'role': 'system', 'content': _st}] if _st else []) + [um]", 'H5a msgs')
rp("            'scenario': args.scenario, 'family': FAM, 'system': args.system, 'system_sha': SYSTEM_SHA,\n            'system_prompt_sha': (sha16(SYSTEM_TEXT) if SYSTEM_TEXT else None), 'prompt_sha': sha16(um['content']),",
   "            'scenario': args.scenario, 'family': FAM, 'system': args.system, 'system_sha': _ssha,\n            'system_prompt_sha': (sha16(_st) if _st else None), 'prompt_sha': sha16(um['content']),", 'H5b base')
rp("        sent = (SYSTEM_TEXT or '', TEXTS.get(arm) or '', SCEN_TEXT, INST)", "        sent = (_st or '', TEXTS.get(arm) or '', SCEN_TEXT, INST)   # v2.5: 採点経路（strip_echo・refuse_class・incentive）にも腕別 system 文を通す", 'H5c sent')
# ---- ハンク 6: cells の腕別 system
rp("         'preamble_sha': ARM_SHA.get(a), 'preamble_src': ARM_SRC.get(a), 'system': args.system, 'system_sha': SYSTEM_SHA,",
   "         'preamble_sha': ARM_SHA.get(a), 'preamble_src': ARM_SRC.get(a), 'system': args.system, 'system_sha': (SYS_SHA[a] if a in SYS_SHA else SYSTEM_SHA),\n"
   "         'system_src': SYS_SRC.get(a), 'system_prefix': SYS_PREFIX.get(a),", 'H6 cells')
# ---- ハンク 7: RUN_KEY の system スロット（H2b で同時に適用済み）
H.append('H7 RUN_KEY（H2b）')
# ---- ハンク 9: system 型走行は前置き腕を置かない（--arms - ＝空・既定値の 8 腕が黙って合流する事故を防ぐ）
rp("ARMS = args.arms.split(',')", "ARMS = [] if args.arms == '-' else args.arms.split(',')   # v2.5: system 型走行は --arms -（前置き腕なし・--system-arms の腕のみ）", 'H9 arms-empty')
# ---- ハンク 8: dry-run スタブに system 文の復唱経路（system 腕がある試行にのみ追加・非 system 走行のスタブ列は不変）
rp("    _dry_trial.attempt = getattr(_dry_trial, 'attempt', 0) + 1\n    t = texts[k]",
   "    _sys = (msgs[0].get('content') or '') if (msgs and msgs[0].get('role') == 'system') else ''\n"
   "    if _sys:   # v2.5: system 文の 12 字以上の片の逐語復唱（strip_echo が剥がすこと・様式 (a) が復唱で立たないことの検査経路）\n"
   "        _sf = next((x.strip() + '。' for x in _sys.split('。') if len(x.strip()) >= 12), None)\n"
   "        if _sf:\n            texts = texts + [_sf + js('c', 1)]; k = i0 % len(texts)\n"
   "            if k == 3 and getattr(_dry_trial, 'attempt', 0) == 1:\n                k = 1\n"
   "    _dry_trial.attempt = getattr(_dry_trial, 'attempt', 0) + 1\n    t = texts[k]", 'H8 stub')
out = s.encode('utf-8')
if args.verify:
    cur = open(DST, 'rb').read().replace(b'\r\n', b'\n') if os.path.exists(DST) else b''
    print('[make_runner_m] hunks', len(H), 'generated sha16', sha16(out), 'current', sha16(cur) if cur else 'MISSING', 'MATCH' if cur == out else 'MISMATCH'); sys.exit(0 if cur == out else 2)
open(DST, 'wb').write(out); print('[make_runner_m] written', DST, 'sha16', sha16(out), 'hunks', H)
