# -*- coding: utf-8 -*-
"""make_runner_local.py —— 凍結走行器 tools/run_preamble_api_f.py（v2.6・SHA16 9F5892B5172642BE）から手元推論（vLLM の OpenAI 互換サーバ）用の走行器
tools/run_preamble_local.py（v2.7）を決定的に生成する。費用パイロット（計画案 v2.2 §5 1″・門0）と段階 A/B の手元走行に用いる。
差分は本ファイルに逐語で列挙した 6 ハンクのみ: (1) 見出し (2) PROVIDERS に local（127.0.0.1:8000・鍵不要）を追加 (3) load_key: local は鍵ファイルを読まない
(4) --extra-body（JSON・chat_template_kwargs 等を要求本文に併合・manifest と各行の sampling に記帳）(5) SAMPLING を一箇所に (6) manifest に local_env（GPU・vLLM/torch 版・サーバ /version）を記帳。
採点経路（parse・endpoint・refuse_class・incentive・strip_echo・user_message）は v2.6 と関数単位で同一。API 走行器 v2.4〜v2.6 は改変しない。再実行で同一バイト。
検査（`--verify`）: 生成物が現物と一致すること・各ハンクの適用位置が一意であること・`_norm`・`_quoted_segments`・`strip_echo`・`user_message`・`endpoint`・`refuse_class`・`incentive` の関数単位 SHA16 が v2.6 と同一であること。
"""
import os, sys, ast, hashlib, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'tools', 'run_preamble_api_f.py'); DST = os.path.join(REPO, 'tools', 'run_preamble_local.py')
ap = argparse.ArgumentParser(); ap.add_argument('--verify', action='store_true'); args = ap.parse_args()
FUNCS = ('_norm', '_quoted_segments', 'strip_echo', 'user_message', 'endpoint', 'refuse_class', 'incentive')


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16].upper()


def func_shas(src):
    tree = ast.parse(src); out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in FUNCS:
            out[node.name] = sha16(ast.get_source_segment(src, node).encode('utf-8'))
    assert set(out) == set(FUNCS), out.keys(); return out


raw = open(SRC, 'rb').read().replace(b'\r\n', b'\n'); assert sha16(raw) == '9F5892B5172642BE', '凍結走行器 v2.6 の SHA 不一致: %s' % sha16(raw)
s = raw.decode('utf-8'); H = []; F26 = func_shas(s)


def rp(a, b, tag, cnt=1):
    global s
    assert s.count(a) == cnt, (tag, s.count(a), a[:60]); s = s.replace(a, b); H.append(tag)


# ---- ハンク 1: 見出し
rp('"""run_preamble_api_f.py v2.6（', '"""run_preamble_local.py v2.7（v2.6＋手元推論〔vLLM OpenAI 互換サーバ・provider local・鍵不要〕・--extra-body・manifest の local_env・2026-09-12。'
   '生成器 tools/make_runner_local.py・6 ハンク。採点経路の 7 関数は v2.6 と関数単位で同一。費用パイロット〔門0〕と段階 A/B の手元走行用）\n元: run_preamble_api_f.py v2.6（', 'H1 docstring')
# ---- ハンク 2: provider local
rp("    'gemini':   dict(url='https://generativelanguage.googleapis.com/v1beta/openai/chat/completions', key='GEMINI_API_KEY', model='gemini-2.5-flash-lite'),\n}",
   "    'gemini':   dict(url='https://generativelanguage.googleapis.com/v1beta/openai/chat/completions', key='GEMINI_API_KEY', model='gemini-2.5-flash-lite'),\n"
   "    'local':    dict(url='http://127.0.0.1:8000/v1/chat/completions', key='OP4B_LOCAL_KEY', model='Qwen/Qwen3-4B-Instruct-2507'),   # v2.7: 手元推論（vLLM serve・鍵不要）\n}", 'H2 provider local')
# ---- ハンク 3: local は鍵ファイルを読まない
rp("def load_key(name):\n    if args.dry_run:\n        return 'DRY'\n",
   "def load_key(name):\n    if args.dry_run:\n        return 'DRY'\n    if name == 'OP4B_LOCAL_KEY':   # v2.7: 手元サーバは認証なし（鍵ファイルを開かない）\n        return os.environ.get(name, 'local')\n", 'H3 load_key local')
# ---- ハンク 4: --extra-body
rp("ap.add_argument('--max-tokens', type=int, default=4096)\n",
   "ap.add_argument('--max-tokens', type=int, default=4096)\n"
   "ap.add_argument('--extra-body', default=None, help='v2.7: 要求本文に併合する JSON（例 {\"chat_template_kwargs\": {\"enable_thinking\": false}}）。manifest と各行の sampling に記帳')\n", 'H4a extra-body arg')
rp("RUNNER_SHA = shafile(os.path.abspath(__file__))\n",
   "RUNNER_SHA = shafile(os.path.abspath(__file__))\n"
   "EXTRA_BODY = json.loads(args.extra_body) if args.extra_body else {}\n"
   "SAMPLING = {'temperature': TEMPERATURE, 'top_p': TOP_P, 'max_tokens': args.max_tokens, 'extra_body': EXTRA_BODY}   # v2.7: 一箇所に\n", 'H4b EXTRA_BODY')
rp("    body = json.dumps({'model': MODEL, 'messages': msgs, 'temperature': TEMPERATURE, 'top_p': TOP_P,\n                       'max_tokens': args.max_tokens, 'stream': False}).encode('utf-8')",
   "    body = json.dumps(dict({'model': MODEL, 'messages': msgs, 'temperature': TEMPERATURE, 'top_p': TOP_P,\n                            'max_tokens': args.max_tokens, 'stream': False}, **EXTRA_BODY)).encode('utf-8')   # v2.7: --extra-body を併合", 'H4c body')
# ---- ハンク 5: SAMPLING（manifest と各行の二箇所）
rp("'sampling': {'temperature': TEMPERATURE, 'top_p': TOP_P, 'max_tokens': args.max_tokens},", "'sampling': SAMPLING,", 'H5 SAMPLING x2', cnt=2)
# ---- ハンク 6: manifest の local_env
rp("# ---- manifest（同一出力先への別条件の合流を禁止）----\n",
   "# ---- v2.7: 手元推論の環境（GPU・vLLM/torch 版・サーバ /version）----\n"
   "def local_env():\n"
   "    import subprocess, platform\n"
   "    e = {'python': sys.version.split()[0], 'platform': platform.platform(), 'hostname': platform.node()}\n"
   "    try:\n"
   "        e['gpu'] = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,driver_version', '--format=csv,noheader'], capture_output=True, text=True, timeout=20).stdout.strip()\n"
   "    except Exception as ex:\n"
   "        e['gpu'] = 'nvidia-smi 不可: %s' % ex\n"
   "    try:\n"
   "        import importlib.metadata as md\n"
   "        e['versions'] = {k: (md.version(k) if _has(md, k) else None) for k in ('vllm', 'torch', 'transformers', 'tokenizers')}\n"
   "    except Exception as ex:\n"
   "        e['versions'] = 'importlib.metadata 不可: %s' % ex\n"
   "    if not args.dry_run:\n"
   "        try:\n"
   "            with urllib.request.urlopen(API_URL.rsplit('/v1/', 1)[0] + '/version', timeout=20) as r:\n"
   "                e['server_version'] = json.loads(r.read().decode('utf-8'))\n"
   "        except Exception as ex:\n"
   "            e['server_version'] = '取得不可: %s' % ex\n"
   "    return e\n"
   "\n"
   "\n"
   "def _has(md, k):\n"
   "    try:\n"
   "        md.version(k); return True\n"
   "    except Exception:\n"
   "        return False\n"
   "\n"
   "\n"
   "# ---- manifest（同一出力先への別条件の合流を禁止）----\n", 'H6a local_env def')
rp("            'system_arms': SYSARMS, 'system_arm_sha': SYS_SHA, 'system_arm_src': SYS_SRC, 'system_arm_prefix': SYS_PREFIX}\n",
   "            'system_arms': SYSARMS, 'system_arm_sha': SYS_SHA, 'system_arm_src': SYS_SRC, 'system_arm_prefix': SYS_PREFIX}\n"
   "manifest['local_env'] = local_env() if args.provider == 'local' else None   # v2.7（manifest の不一致検査の対象外・記帳のみ）\n", 'H6b manifest local_env')
out = s.encode('utf-8'); F27 = func_shas(s)
assert F26 == F27, ('採点経路の関数単位 SHA が v2.6 と異なる', F26, F27)
ast.parse(s)
if args.verify:
    cur = open(DST, 'rb').read().replace(b'\r\n', b'\n') if os.path.exists(DST) else b''
    print('[make_runner_local] hunks', len(H), 'generated sha16', sha16(out), 'current', sha16(cur) if cur else 'MISSING', 'MATCH' if cur == out else 'MISMATCH', '| 7 関数 SHA v2.6=v2.7', F27)
    sys.exit(0 if cur == out else 2)
open(DST, 'wb').write(out); print('[make_runner_local] written', DST, 'sha16', sha16(out), 'hunks', H, '| 7 関数 SHA', F27)
