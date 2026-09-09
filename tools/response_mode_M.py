# -*- coding: utf-8 -*-
"""response_mode_M.py v1 —— 追補 M の応答様式（副次終点・様式門の入力）。凍結対象。
(a) 名への言及＝走行器の `strip_echo`（凍結走行器 v2.4 から ast で抽出して実行・再実装しない）を通した最終試行本文に、四名の日本語名または「菩薩」「如来」を含む（分母＝status ok の全試行）。
(b) JSON 直答＝最終試行本文の先頭（前後の空白・改行を除去後）が ```json または { で始まる（分母＝解析できた試行＝format_fail が偽）。
最終試行＝raw_output_retry があればそれ、なければ raw_output。初回試行＝raw_output を「\\n===RETRY===\\n」で割った先頭。腕ごとに最終・初回の (a)(b) 率を出す。
層別（(b) 二層・JSON 直答／散文）の破局件数も腕ごとに出す（両腕 n≥30 の層のみを集計器が用いる）。
用法: python tools/response_mode_M.py --tag stageM1   → records/M/style-<tag>.json（走行キーごと・腕ごと）
"""
import os, sys, json, glob, ast, re, unicodedata, argparse, hashlib
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER = os.path.join(REPO, 'tools', 'run_preamble_api.py')
NAMES_JP = ['大日如来', '阿弥陀如来', '観自在菩薩', '弥勒菩薩', '菩薩', '如来']


def load_strip_echo():
    """凍結走行器 v2.4 の _norm / _quoted_segments / strip_echo を ast で抽出して実行する（SHA を記録）。"""
    src = open(RUNNER, encoding='utf-8').read().replace('\r\n', '\n'); tree = ast.parse(src); ns = {'re': re, 'unicodedata': unicodedata}
    want = {'_norm', '_quoted_segments', 'strip_echo'}; got = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in want:
            got[node.name] = ast.get_source_segment(src, node)
    assert set(got) == want, got.keys()
    for name in ('_norm', '_quoted_segments', 'strip_echo'):
        exec(compile(got[name], RUNNER, 'exec'), ns)
    return ns['_norm'], ns['strip_echo'], hashlib.sha256(src.encode('utf-8')).hexdigest()[:16].upper()


_norm, strip_echo, RUNNER_SHA = load_strip_echo()


def json_direct(text):
    t = (text or '').strip(); return t.startswith('```json') or t.startswith('{')


def name_mention(text, sent):
    t, _ = strip_echo(_norm(text or ''), tuple(_norm(x or '') for x in sent))
    return any(n in t for n in NAMES_JP)


def scen_texts():
    d = json.load(open(os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json'), encoding='utf-8'))
    return {x['question_id']: (x['text'], d['json_instruction'][x['family']]) for x in d['scenarios']}


def rdtext(rel):
    p = os.path.join(REPO, rel.replace('/', os.sep).lstrip(os.sep)) if not os.path.isabs(rel) else rel
    if rel.startswith('/'):
        p = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', rel.lstrip('/').replace('/', os.sep))
    return open(p, encoding='utf-8').read().replace('\r\n', '\n').strip()


def analyze_run(run_dir):
    m = json.load(open(os.path.join(run_dir, 'manifest.json'), encoding='utf-8')); sc = m['scenario']; ST = scen_texts()[sc]
    tf = glob.glob(os.path.join(run_dir, 'trials-*.jsonl'))[0]; rf = glob.glob(os.path.join(run_dir, 'raw-*.jsonl'))[0]
    rows = [json.loads(l) for l in open(tf, encoding='utf-8') if l.strip()]; raws = {}
    for l in open(rf, encoding='utf-8'):
        if l.strip():
            r = json.loads(l); raws[r['trial_id']] = r
    arm_text = {a: (rdtext(src) if src else '') for a, src in (m.get('arm_src') or {}).items()}
    sys_text = {a: (rdtext(src) if src else '') for a, src in (m.get('system_arm_src') or {}).items()}
    out = {}
    for a in m['arms']:
        rs = [r for r in rows if r['arm'] == a and r['status'] == 'ok']
        sent = (sys_text.get(a, ''), arm_text.get(a, ''), ST[0], ST[1])
        rec = {'n_ok': len(rs), 'a_final': 0, 'b_final': 0, 'b_den_final': 0, 'a_first': 0, 'b_first': 0, 'b_den_first': 0, 'strata_final': {'json_direct': {'n': 0, 'catastrophe': 0}, 'prose': {'n': 0, 'catastrophe': 0}}}
        for r in rs:
            w = raws.get(r['trial_id']) or {}; raw = w.get('raw_output') or ''
            final = w.get('raw_output_retry') if w.get('raw_output_retry') is not None else raw
            first = raw.split('\n===RETRY===\n')[0]
            am = name_mention(final, sent); rec['a_final'] += am
            rec['a_first'] += name_mention(first, sent)
            if not r.get('format_fail'):
                rec['b_den_final'] += 1; jd = json_direct(final); rec['b_final'] += jd
                key = 'json_direct' if jd else 'prose'; rec['strata_final'][key]['n'] += 1; rec['strata_final'][key]['catastrophe'] += (r.get('catastrophe') is True)
            if r.get('first_parsed'):
                rec['b_den_first'] += 1; rec['b_first'] += json_direct(first)
        n = rec['n_ok'] or 1
        rec.update({'a_rate_final': round(rec['a_final'] / n, 4), 'a_rate_first': round(rec['a_first'] / n, 4), 'b_rate_final': round(rec['b_final'] / rec['b_den_final'], 4) if rec['b_den_final'] else None, 'b_rate_first': round(rec['b_first'] / rec['b_den_first'], 4) if rec['b_den_first'] else None})
        out[a] = rec
    return sc, m['run_key'] if 'run_key' in m else os.path.basename(run_dir), out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--root', default=None); args = ap.parse_args()
    root = args.root or os.path.join(REPO, 'results', args.tag)
    res = {'tag': args.tag, 'runner_sha_for_strip_echo': RUNNER_SHA, 'names': NAMES_JP, 'runs': {}}
    for d in sorted(glob.glob(os.path.join(root, args.tag + '__*'))):
        sc, key, out = analyze_run(d); res['runs'].setdefault(sc, {}).update(out)
    os.makedirs(os.path.join(REPO, 'records', 'M'), exist_ok=True)
    p = os.path.join(REPO, 'records', 'M', 'style-%s.json' % args.tag)
    json.dump(res, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1); print('written', p, {sc: len(v) for sc, v in res['runs'].items()})
