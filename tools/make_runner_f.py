# -*- coding: utf-8 -*-
"""make_runner_f.py —— 凍結走行器 tools/run_preamble_api_m.py（v2.5・SHA16 D5942EC76869AFBC）から段階 F 専用の走行器 tools/run_preamble_api_f.py（v2.6）を
決定的に生成する。差分は本ファイルに逐語で列挙した 4 ハンク（草案4 §2.6）のみ: (1) 見出し (2) 盤 arms/panelF/ と台帳 SHA-LEDGER-F.json の読み込み (3) load_arm の第二探索先を panelM から panelF に付け替え
(4) --system-arms 指定時に sys.exit するガード（段階 F は system 型を置かない・system 経路の盤参照は触らない）。v2.4／v2.5 は改変しない。再実行で同一バイト。
検査（`--verify`）: 生成物が現物と一致すること・4 ハンクの適用位置がすべて一意であること・`_norm`・`_quoted_segments`・`strip_echo`・`user_message` の 4 関数の関数単位 SHA16 が v2.5 と同一であること。
"""
import os, sys, ast, hashlib, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'tools', 'run_preamble_api_m.py'); DST = os.path.join(REPO, 'tools', 'run_preamble_api_f.py')
ap = argparse.ArgumentParser(); ap.add_argument('--verify', action='store_true'); args = ap.parse_args()
FUNCS = ('_norm', '_quoted_segments', 'strip_echo', 'user_message')


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16].upper()


def func_shas(src):
    tree = ast.parse(src); out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in FUNCS:
            out[node.name] = sha16(ast.get_source_segment(src, node).encode('utf-8'))
    assert set(out) == set(FUNCS), out.keys(); return out


raw = open(SRC, 'rb').read().replace(b'\r\n', b'\n'); assert sha16(raw) == 'D5942EC76869AFBC', '凍結走行器 v2.5 の SHA 不一致: %s' % sha16(raw)
s = raw.decode('utf-8'); H = []; F25 = func_shas(s)


def rp(a, b, tag):
    global s
    assert s.count(a) == 1, (tag, s.count(a), a[:60]); s = s.replace(a, b); H.append(tag)


# ---- ハンク 1: 見出し
rp('"""run_preamble_api_m.py v2.5（', '"""run_preamble_api_f.py v2.6（v2.5＋段階 F の盤 arms/panelF/・台帳 SHA-LEDGER-F.json・system 型のガード・段階 F 専用・凍結走行器 v2.4／v2.5 は不変・2026-09-11。生成器 tools/make_runner_f.py・4 ハンク。user_message・strip_echo・_norm・_quoted_segments は v2.5 と関数単位で同一）\n元: run_preamble_api_m.py v2.5（', 'H1 docstring')
# ---- ハンク 2: 段階 F の盤と台帳
rp("LEDGER_M = json.load(open(LEDGER_M_PATH, encoding='utf-8')) if os.path.isfile(LEDGER_M_PATH) else {'preamble': {}, 'system': {}}",
   "LEDGER_M = json.load(open(LEDGER_M_PATH, encoding='utf-8')) if os.path.isfile(LEDGER_M_PATH) else {'preamble': {}, 'system': {}}\n"
   "PANEL_F_DIR = os.path.join(REPO, 'arms', 'panelF'); LEDGER_F_PATH = os.path.join(PANEL_F_DIR, 'SHA-LEDGER-F.json')   # v2.6: 段階 F の盤\n"
   "LEDGER_F = json.load(open(LEDGER_F_PATH, encoding='utf-8')) if os.path.isfile(LEDGER_F_PATH) else {'preamble': {}}", 'H2 ledgerF')
# ---- ハンク 3: load_arm の第二探索先（V′ 盤に無い腕は panelF から・panelM は読まない）
rp("        p = os.path.join(PANEL_M_DIR, name + '.md'); led = LEDGER_M.get('preamble', {})   # v2.5: 追補 M の盤（V′ 盤に無い腕のみ）",
   "        p = os.path.join(PANEL_F_DIR, name + '.md'); led = LEDGER_F.get('preamble', {})   # v2.6: 段階 F の盤（V′ 盤に無い腕のみ・追補 M の盤は読まない）", 'H3 load_arm panelF')
# ---- ハンク 4: system 型のガード（段階 F は system 型を置かない・system 経路のコードは触らない）
rp("SYSARMS = None\nif args.system_arms:\n", "SYSARMS = None\nif args.system_arms:\n    sys.exit('段階 F は system 型を置かない（v2.6 ガード・--system-arms は不可）')\n", 'H4 system guard')
out = s.encode('utf-8'); F26 = func_shas(s)
assert F25 == F26, ('4 関数の関数単位 SHA が v2.5 と異なる', F25, F26)
if args.verify:
    cur = open(DST, 'rb').read().replace(b'\r\n', b'\n') if os.path.exists(DST) else b''
    print('[make_runner_f] hunks', len(H), 'generated sha16', sha16(out), 'current', sha16(cur) if cur else 'MISSING', 'MATCH' if cur == out else 'MISMATCH', '| 4 関数 SHA v2.5=v2.6', F26)
    sys.exit(0 if cur == out else 2)
open(DST, 'wb').write(out); print('[make_runner_f] written', DST, 'sha16', sha16(out), 'hunks', H, '| 4 関数 SHA', F26)
