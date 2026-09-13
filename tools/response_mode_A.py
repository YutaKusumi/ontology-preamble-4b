# -*- coding: utf-8 -*-
"""response_mode_A.py v1 —— 段階 A の応答様式（様式門の入力）・検査認識の言及（記述）・<think> の残骸（記述）。凍結対象。規則は design/contrasts-A.json の response_mode・style_gate（2026-09-13・登録者裁定 D9 の手順3）。
(a) 名への言及＝走行器 tools/run_preamble_local.py v2.7 の strip_echo（ast で抽出して実行・再実装しない）を通した最終試行の本文に、段階 M の語彙（四名＋「菩薩」「如来」）を含む（段階 F と同じ・A の腕では記録の性格）。
(b) JSON 直答＝最終試行の本文の先頭（前後の空白を除く）が ```json または { で始まる。分母はともに n_ok（style_gate.denominator・書式外の試行も分母に入れ、分子は本文の先頭だけで決める）。
言及（記述）＝段階 F の凍結正本 design/contrasts-F.json の mention_tag の語彙。c1＝strip_echo の既定・c2＝付記の除去なし（A の腕に付記は無い）で strip_echo の min_len を mention_tag.c2.min_len に。
<think> の残骸＝生本文（再試行を含む全文）に <think> または </think> を含む試行の件数（記述・パイロットの開始時点の診断）。
層（style_gate.stratified の入力）＝(b) の二層（JSON 直答／散文）ごとの試行数と破局数（最終試行・status ok・破局は catastrophe が真）。
送信文字列（strip_echo の入力）＝前置き（manifest の arm_src）・場面の本文・JSON 指示（走行器の user_message と同じ部品・system は無い）。
出力: records/A/style-<tag>.json（cells[機種 key][場面][腕]）。既存の出力は --force なしでは上書きしない。
用法: python tools/response_mode_A.py --tag stageA [--root <results の代わり>] [--out <path>] [--force]
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, sys, json, ast, re, unicodedata, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
RUNNER = os.path.join(REPO, 'tools', 'run_preamble_local.py')
VERSION = 'v1'
NAMES_JP = ['大日如来', '阿弥陀如来', '観自在菩薩', '弥勒菩薩', '菩薩', '如来']   # 段階 M・F と同じ（tools/response_mode_M.py・tools/response_mode_F.py）
TF = json.load(open(os.path.join(REPO, 'design', 'contrasts-F.json'), encoding='utf-8')); MT = TF['mention_tag']
JA = MT['lexicon_ja']; EN = [re.compile(p, re.I) for p in MT['lexicon_en_stems']]; C2_MIN = MT['c2']['min_len']
SCEN_PATH = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', 'app-scenarios.json')
THINK = ('<think>', '</think>')


def load_funcs():
    src = open(RUNNER, encoding='utf-8').read().replace('\r\n', '\n'); tree = ast.parse(src); ns = {'re': re, 'unicodedata': unicodedata}
    want = {'_norm', '_quoted_segments', 'strip_echo'}; got = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in want:
            got[node.name] = ast.get_source_segment(src, node)
    assert set(got) == want, got.keys()
    for name in ('_norm', '_quoted_segments', 'strip_echo'):
        exec(compile(got[name], RUNNER, 'exec'), ns)
    return ns['_norm'], ns['strip_echo']


_norm, strip_echo = load_funcs()


def json_direct(text):
    t = (text or '').strip(); return t.startswith('```json') or t.startswith('{')


def hits_c(t):
    return [w for w in JA if w in t] + [p.pattern for p in EN if p.search(t)]


def scen_texts():
    d = json.load(open(SCEN_PATH, encoding='utf-8'))
    return {x['question_id']: (x['text'], d['json_instruction'][x['family']]) for x in d['scenarios']}


def arm_text(rel):
    if not rel:
        return ''
    p = os.path.join(REPO, 'arms', 'frozen-from-ryokai-os', rel.lstrip('/').replace('/', os.sep)) if rel.startswith('/') else os.path.join(REPO, rel.replace('/', os.sep))
    return open(p, encoding='utf-8').read().replace('\r\n', '\n').strip()


def measure(text, sent_norm):
    """一本文の (a)(b)(c1)(c2) を返す。sent_norm は _norm 済みの送信文字列の組。"""
    t1, _ = strip_echo(_norm(text or ''), sent_norm); t2, _ = strip_echo(_norm(text or ''), sent_norm, min_len=C2_MIN)
    return {'a': any(nm in t1 for nm in NAMES_JP), 'b': json_direct(text), 'c1': bool(hits_c(t1)), 'c2': bool(hits_c(t2))}


def analyze_run(rec, ST):
    m = rec['manifest']; sc = m['scenario']; stext, inst = ST[sc]
    raws = {r['trial_id']: r for r in runs_A.iter_jsonl(rec['raw_path'])}
    texts = {a: arm_text(src) for a, src in (m.get('arm_src') or {}).items()}
    out = {}
    for r in runs_A.iter_jsonl(rec['trials_path'], ('trial_id', 'arm', 'status', 'catastrophe', 'format_fail')):
        a = r['arm']; c = out.setdefault(a, {'n_ok': 0, 'a_final': 0, 'b_final': 0, 'c1_final': 0, 'c2_final': 0, 'think_residue': 0,
                                             'strata': {'json_direct': {'n': 0, 'cat': 0}, 'prose': {'n': 0, 'cat': 0}}})
        if r['status'] != 'ok':
            continue
        w = raws.get(r['trial_id']) or {}; raw = w.get('raw_output') or ''
        final = w.get('raw_output_retry') if w.get('raw_output_retry') is not None else raw
        sent = tuple(_norm(x) for x in ('', texts.get(a, ''), stext, inst))
        mf = measure(final, sent); cat = (r['catastrophe'] is True)
        c['n_ok'] += 1; c['a_final'] += mf['a']; c['b_final'] += mf['b']; c['c1_final'] += mf['c1']; c['c2_final'] += mf['c2']
        c['think_residue'] += any(t in raw for t in THINK)
        st = c['strata']['json_direct' if mf['b'] else 'prose']; st['n'] += 1; st['cat'] += cat
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', required=True); ap.add_argument('--root', default=None); ap.add_argument('--out', default=None); ap.add_argument('--force', action='store_true')
    ap.add_argument('--contrasts', default=None); a = ap.parse_args()
    T = runs_A.load_T(a.contrasts); ST = scen_texts(); idx = runs_A.index_runs(T, a.tag, a.root)
    out = a.out or os.path.join(REPO, 'records', 'A', 'style-%s.json' % a.tag)
    if os.path.exists(out) and not a.force:
        sys.exit('出力が既にある（上書きしない・--force で置き換え）: %s' % out)
    runner_sha = runs_A.sha16_file(RUNNER)
    res = {'kind': 'response_mode_A', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'tag': a.tag, 'root': a.root,
           'contrasts_sha16': runs_A.sha16_file(a.contrasts or runs_A.CPATH), 'runner_sha16_for_strip_echo': runner_sha, 'runner_registered_match': runner_sha == T['runner']['sha16'],
           'names': NAMES_JP, 'lexicon_ja': JA, 'lexicon_en_stems': MT['lexicon_en_stems'], 'c2_min_len': C2_MIN, 'denominator': T['style_gate']['denominator'], 'cells': {}}
    for (mk, sc), rec in sorted(idx.items()):
        res['cells'].setdefault(mk, {})[sc] = analyze_run(rec, ST)
        print('[style] %s %s %d 腕' % (mk, sc, len(res['cells'][mk][sc])), flush=True)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print('written', out, '| runner の登録と一致' if res['runner_registered_match'] else '| 注意: strip_echo を抽出した走行器の SHA16 が runner.sha16 と違う')
