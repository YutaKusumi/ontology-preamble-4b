# -*- coding: utf-8 -*-
"""verify_freeze_prep_A.py v1 —— 凍結の前の登録者裁定 D45〜D47 の反映の確かめ（2026-09-15・コーディネータ）。
事前登録 records/A/freeze-prep/preregistration-freeze-prep-A.md の確かめの条件 Q1〜Q10 を機械で走らせ、records/A/freeze-prep/verification-freeze-prep-A.{json,md} に書く。
反映の前の版は git の基準のコミット（--base・既定 5673e48）から一時置き場（--work・リポジトリの外）に取り出す。器は子プロセスで通し、器の内部を import して呼ばない。
Q7 のブラウザの値（様式が表示した SHA-256 と、ブラウザ標準の crypto.subtle の SHA-256）は、アプリ内のブラウザで様式を開き、本器の FILL_RULE で埋めて「生成」を押した結果を --browser-sha と --browser-native-sha で受け取る。
ブラウザ標準の SHA-256 が行えなかったときは --browser-native-sha に「未実施」を与える（Q7 は条件を動かさずに不合格として残る）。
Q7b は事後に足した補助の確かめ（2026-09-15・Q7 の (i) が行えなかったため）: 様式の JS の sha256hex で既知の文字列の組の SHA-256 をつないだ文字列の SHA-256 を --browser-vectors-dd で受け取り、Python の hashlib と突き合わせる。
Q8 の期待の件数は、照合の器を使わずに、本器が集計の記録と Q7 の埋め方から数える。
限界: 合成の集計の記録は本物の出力の分布を再現しない。アプリ内のブラウザは登録者の Chrome ではない。
用法: python tools/verify_freeze_prep_A.py --work <一時置き場> --grid-new <v2.8 で走らせた格子> --analysis <合成の集計の記録> --browser-sha <64 桁> --browser-native-sha <64 桁 または 未実施> [--browser-vectors-dd <64 桁>] [--base 5673e48]
柵: 本器の出力のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, ast, json, shutil, hashlib, argparse, datetime, subprocess, collections
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_A
REPO = runs_A.REPO
VERSION = 'v1'
FILL_RULE = 'i 番目（0 から）の select は選択肢の添字 1 + (i mod (選択肢の数 − 1)) を選ぶ・info.coi と free は「確かめ」・date は 2026-09-15'
FILL_TEXT = {'info.coi': '確かめ', 'free': '確かめ', 'date': '2026-09-15'}
FORM_NAME, PROGRAM = 'predictions-form v0.8 (A)', 'ontology-preamble-4b/A'
V5_META = "form:'predictions-form v0.5 (Vprime)',program:'ontology-preamble-4b/Vprime',contrasts:'draft7-2026-09-07'"
V5_DL, DL_NAME = 'predictions-Vprime-registrant.json', 'predictions-A.json'
RES = ('的中', '外れ', '照合不能', '予想しない')
NOT_DONE = '未実施'
ap = argparse.ArgumentParser()
ap.add_argument('--work', required=True); ap.add_argument('--grid-new', required=True); ap.add_argument('--analysis', required=True)
ap.add_argument('--browser-sha', required=True); ap.add_argument('--browser-native-sha', required=True); ap.add_argument('--base', default='5673e48'); ap.add_argument('--browser-vectors-dd', default=None)
ap.add_argument('--out', default=os.path.join(REPO, 'records', 'A', 'freeze-prep', 'verification-freeze-prep-A')); ap.add_argument('--skip-selftests', action='store_true')
a = ap.parse_args()
if os.path.commonpath([os.path.realpath(a.work), os.path.realpath(REPO)]) == os.path.realpath(REPO):
    sys.exit('--work はリポジトリの外に置く')
shutil.rmtree(a.work, ignore_errors=True); os.makedirs(a.work)
T = runs_A.load_T(); P = T['predictions']; FLD = P['fields']; ROWS = []; EXTRA = {}
CON = T['families']['A_slope']['contrasts']; CELLS = T['descriptive_families']['A_desc_floor']['cells']
tool = lambda nm: os.path.join(REPO, 'tools', nm)


def run(args, timeout=3600, env_extra=None):
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1'); env.update(env_extra or {})
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=REPO, timeout=timeout, env=env)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def R(kid, what, ok, detail):
    ROWS.append({'id': kid, 'what': what, 'pass': bool(ok), 'detail': detail})
    print('[verify] %s %s: %s' % ('○' if ok else '×', kid, what), flush=True)


def base_file(path, name):
    b = subprocess.run(['git', 'show', '%s:%s' % (a.base, path)], capture_output=True, cwd=REPO).stdout
    assert b, ('基準のコミットにファイルが無い', path)
    p = os.path.join(a.work, name); open(p, 'wb').write(b); return p


def leaves(x, path=()):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, path + (k,))
    elif isinstance(x, list) and x and all(isinstance(v, (dict, list)) for v in x):
        for i, v in enumerate(x):
            yield from leaves(v, path + ('[%d]' % i,))
    else:
        yield '.'.join(path), x


# ---- Q1: 正本の差の範囲（v2.7 → v2.8）
OLD = json.load(open(base_file('design/contrasts-A.json', 'contrasts-base.json'), encoding='utf-8')); LO = dict(leaves(OLD)); LN = dict(leaves(T))
changed = sorted(p for p in LO if p in LN and LO[p] != LN[p]); added = sorted(p for p in LN if p not in LO); removed = sorted(p for p in LO if p not in LN)
ALLOW_C = {'generator', 'procedure', 'tooling_interpretations.status'}; ALLOW_A = ('predictions.', 'registrant_decisions_D45_D47.')
outside = [p for p in changed if p not in ALLOW_C] + [p for p in added if not p.startswith(ALLOW_A)] + removed
R('Q1', '正本 v2.8 と v2.7 の差が事前登録 §2 A の範囲だけ・消えた葉なし・整合検査の結果と procedure の項の数と運用の解釈の項が同じ',
  not outside and set(changed) == ALLOW_C and OLD['integrity'] == T['integrity'] and len(OLD['procedure']) == len(T['procedure']) and OLD['tooling_interpretations']['items'] == T['tooling_interpretations']['items'],
  {'changed': changed, 'n_added': len(added), 'added_roots': sorted({p.split('.')[0] for p in added}), 'removed': removed, 'outside': outside})


# ---- Q2: 格子の数値の差（入力の SHA16・生成の時刻・所要時間・版を除く）
def cmpv(n, o, path, out, rounded):
    if isinstance(o, dict):
        if not isinstance(n, dict):
            out.append((path, 'type')); return
        for k in o:
            if k not in n:
                out.append(('%s.%s' % (path, k), 'missing')); continue
            cmpv(n[k], o[k], '%s.%s' % (path, k), out, rounded)
    elif isinstance(o, list):
        if not isinstance(n, list) or len(n) != len(o):
            out.append((path, 'len')); return
        for i, (x, y) in enumerate(zip(n, o)):
            cmpv(x, y, '%s[%d]' % (path, i), out, rounded)
    elif rounded and isinstance(o, float) and isinstance(n, (int, float)) and not isinstance(n, bool):
        if not (n == o or any(round(n, d) == o for d in range(0, 13))):
            out.append((path, 'value', n, o))
    elif n != o:
        out.append((path, 'value', n, o))


GN = runs_A.read_json(a.grid_new); GO = json.load(open(base_file('records/A/power-grid-A.json', 'grid-base.json'), encoding='utf-8')); gd = []
for k in GO:
    if k not in ('version', 'generated_utc', 'inputs', 'elapsed_s'):
        cmpv(GN.get(k), GO[k], k, gd, rounded=(k == 'E')) if k in GN else gd.append((k, 'missing'))
R('Q2', '格子の再走（正本 v2.8）で、全節の値が反映の前の格子と一致し、入力の正本の SHA16 が現物と一致・quick でない',
  not gd and GN['inputs']['contrasts_sha16'] == runs_A.sha16_file(runs_A.CPATH) and not GN.get('quick') and GN.get('version') == GO.get('version'),
  {'diffs': len(gd), 'first': gd[:5], 'new_only': [k for k in GN if k not in GO], 'elapsed_s': GN.get('elapsed_s')})
EXTRA['prediction_a'] = {'predicted_diffs': 0, 'got': len(gd), 'hit': not gd}

# ---- Q3: 設計事実の本文の差（転記行 J の SHA16 と足した二つの器だけ）
FO = json.load(open(base_file('records/A/design-facts-A.json', 'facts-base.json'), encoding='utf-8')); FN = runs_A.read_json(os.path.join(REPO, 'records', 'A', 'design-facts-A.json'))
rows_changed = sorted(k for k in FO['facts'] if FN['facts'].get(k, {}).get('text') != FO['facts'][k]['text']) + sorted(k for k in FN['facts'] if k not in FO['facts'])
MASK = lambda s: re.sub(r'\b[0-9A-F]{16}\b', '<SHA16>', s)
jn = MASK(FN['facts']['J']['text']).replace('／予想の様式と照合→make_predictions_form_A.py・compare_predictions_A.py', '').replace('・make_predictions_form_A.py <SHA16>・compare_predictions_A.py <SHA16>', '')
beyond = jn != MASK(FO['facts']['J']['text']); ex = (FN['facts']['J'].get('data') or {}).get('exist') or {}
q3 = rows_changed == ['J'] and not beyond and not FN.get('dev_marks') and 'make_predictions_form_A.py' in ex and 'compare_predictions_A.py' in ex
R('Q3', '設計事実の本文の差が転記行 J だけで、J の差は SHA16 の文字列と、足した器の対応表の一句と実在の一覧の二つの器だけ・検査用の印なし', q3,
  {'rows_changed': rows_changed, 'beyond': beyond, 'dev_marks': FN.get('dev_marks'), 'exist_new': [k for k in ('make_predictions_form_A.py', 'compare_predictions_A.py') if k in ex]})
EXTRA['prediction_b'] = {'hit': q3}

# ---- Q4: 草案9 と雛形の数の検査・§0-8・§5・§2.15
lint_d = open(os.path.join(REPO, 'records', 'A', 'numbers-lint-draft9A.md'), encoding='utf-8').read(); lint_t = open(os.path.join(REPO, 'records', 'A', 'numbers-lint-template-A.md'), encoding='utf-8').read()
D9 = open(os.path.join(REPO, 'design', 'design-stageA-draft9.md'), encoding='utf-8').read()
m6 = re.search(r'`design/contrasts-A\.json`〔SHA16 ([0-9A-F]{16})〕', D9); sec0 = D9.split('\n## 1. ')[0]
PHR = ['門0.5 の手元の率', '試し読み二回の断片の腕と機械の判定', '封印する予想をこれに寄せる', '予想の様式の情報状態の欄']
dlines = [l for l in D9.split('\n') if l.startswith(('- D45 ', '- D46 ', '- D47 '))]
R('Q4', '草案9 と雛形の数の検査の違反が零・§6 の見出しの正本 SHA16 が現物と一致・§0-8 に D46 の句・§5 に D45〜D47 の行・§2.15 に予想の封印の段・キー参照の残りなし',
  '違反の合計: 0' in lint_d and '違反の合計: 0' in lint_t and bool(m6) and m6.group(1) == runs_A.sha16_file(runs_A.CPATH) and all(x in sec0 for x in PHR) and len(dlines) == 3
  and '**予想の封印（裁定 D47）**' in D9 and '{{' not in D9,
  {'lint_draft': re.findall(r'違反の合計: \d+', lint_d), 'lint_template': re.findall(r'違反の合計: \d+', lint_t), 'sha16_in_draft': m6 and m6.group(1), 'phrases_missing': [x for x in PHR if x not in sec0], 'd_lines': len(dlines)})

# ---- Q5: 運用の解釈の記録
TIW = os.path.join(a.work, 'ti.md'); rc5, o5 = run([tool('tooling_interpretations_A.py'), '--out', TIW])
TIrec = open(os.path.join(REPO, 'records', 'A', 'tooling-interpretations-A.md'), encoding='utf-8').read(); TIgen = open(TIW, encoding='utf-8').read() if rc5 == 0 else ''
TIbase = open(base_file('records/A/tooling-interpretations-A.md', 'ti-base.md'), encoding='utf-8').read()
items_of = lambda s: s[s.index('\n## 1. '):s.index('\n## COI')]
title = TIrec.split('\n', 1)[0]
R('Q5', '運用の解釈の記録: 組み立て直すと記録と一致し、項は 37 で、各項の節が反映の前の記録と同じ・題名に「確認待ち」が無く D45 がある',
  rc5 == 0 and TIgen == TIrec and items_of(TIrec) == items_of(TIbase) and TIrec.count('\n- 向き: ') == len(T['tooling_interpretations']['items']) == 37 and '確認待ち' not in title and 'D45' in title,
  {'rebuild_equal': TIgen == TIrec, 'items_equal_base': items_of(TIrec) == items_of(TIbase) if TIrec else None, 'direction_lines': TIrec.count('\n- 向き: '), 'title': title[:120]})


# ---- Q6: 様式
class FormParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.els = []; self.scripts = []; self.mode = None; self.buf = ''

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ('select', 'input', 'textarea') and 'data-k' in d:
            self.els.append({'tag': tag, 'key': d['data-k'], 'options': []})
        if tag in ('option', 'script'):
            self.mode = tag; self.buf = ''

    def handle_endtag(self, tag):
        if tag == 'option' and self.mode == 'option':
            self.els[-1]['options'].append(self.buf); self.mode = None
        elif tag == 'script' and self.mode == 'script':
            self.scripts.append(self.buf); self.mode = None

    def handle_data(self, data):
        if self.mode:
            self.buf += data


HTMLP = os.path.join(REPO, P['form']); HT = open(HTMLP, encoding='utf-8').read(); FP = FormParser(); FP.feed(HT)
E_DIR = {FLD['direction']['key_prefix'] + c['id'] for c in CON}; E_FLOOR = {FLD['floor']['key_prefix'] + c['id'] for c in CELLS}; E_ALL = {FLD['confirmed_band']['key'], FLD['measurable_band']['key']}
E_INFO = {x['key'] for x in FLD['info']['items']}; E_TEXT = {x['key'] for x in FLD['text']}; E_WHO = {FLD['who']['key']}


def opts_for(k):
    if k in E_DIR:
        return FLD['direction']['options']
    if k in E_FLOOR:
        return FLD['floor']['options']
    if k == FLD['confirmed_band']['key']:
        return FLD['confirmed_band']['options']
    if k == FLD['measurable_band']['key']:
        return FLD['measurable_band']['options']
    if k in E_INFO:
        return FLD['info']['options']
    if k in E_WHO:
        return FLD['who']['options']
    return None


sels = [e for e in FP.els if e['tag'] == 'select']; keys = [e['key'] for e in FP.els]
kinds = {'向き': sum(e['key'] in E_DIR for e in sels), '床持続': sum(e['key'] in E_FLOOR for e in sels), '全体': sum(e['key'] in E_ALL for e in sels), '情報状態': sum(e['key'] in E_INFO for e in sels), '予想者': sum(e['key'] in E_WHO for e in sels)}
exp_kinds = {'向き': len(CON), '床持続': len(CELLS), '全体': 2, '情報状態': len(FLD['info']['items']), '予想者': 1}
V5 = open(os.path.join(REPO, P['js_source']), encoding='utf-8').read(); v5js = re.search(r'<script>(.*?)</script>', V5, re.S).group(1)
exp_js = v5js.replace(V5_META, "form:'%s',program:'%s',contrasts:'%s'" % (FORM_NAME, PROGRAM, T['version'])).replace(V5_DL, DL_NAME)
opts_bad = [e['key'] for e in sels if e['options'] != opts_for(e['key'])]
q6 = (kinds == exp_kinds and len(keys) == len(set(keys)) and set(keys) == E_DIR | E_FLOOR | E_ALL | E_INFO | E_TEXT | E_WHO and not opts_bad
      and kinds['向き'] + kinds['床持続'] + kinds['全体'] == P['n_prediction_fields'] and len(FP.scripts) == 1 and FP.scripts[0] == exp_js and v5js.count(V5_META) == 1 and v5js.count(V5_DL) == 1
      and 'PRESET' not in HT and 'preset(' not in HT and '本様式のいかなる記述も' in HT)
R('Q6', '様式: 選択の欄の数・data-k の集合・選択肢・予想の欄の数が正本と一致・JS が V′ 様式 v0.5 と置き換えた四つの文字列のほかは同じ・自動入力の口なし・柵の一行', q6,
  {'kinds': kinds, 'expected': exp_kinds, 'n_keys': len(keys), 'options_mismatch': opts_bad[:5], 'n_scripts': len(FP.scripts), 'js_equal': bool(FP.scripts) and FP.scripts[0] == exp_js,
   'form_sha16': runs_A.sha16_file(HTMLP), 'n_prediction_fields': P['n_prediction_fields']})

# ---- Q7: ブラウザで生成した SHA-256 と Python の組み立て
vals, si = {}, 0
for e in FP.els:
    if e['tag'] == 'select':
        vals[e['key']] = e['options'][1 + (si % (len(e['options']) - 1))]; si += 1
    else:
        vals[e['key']] = FILL_TEXT[e['key']]
obj = {'form': FORM_NAME, 'program': PROGRAM, 'contrasts': T['version']}
for k in sorted(vals):
    obj[k] = vals[k]
JS_JSON = json.dumps(obj, ensure_ascii=False, indent=1); PY_SHA = hashlib.sha256(JS_JSON.encode('utf-8')).hexdigest().upper()
PQ7 = os.path.join(a.work, 'pred-q7.json'); open(PQ7, 'wb').write(JS_JSON.encode('utf-8'))
FORM_SHA = a.browser_sha.strip().upper(); NATIVE = a.browser_native_sha.strip().upper() if a.browser_native_sha.strip() != NOT_DONE else NOT_DONE
q7 = PY_SHA == FORM_SHA and NATIVE == FORM_SHA
R('Q7', 'ブラウザ: 様式が表示した SHA-256 が、ブラウザ標準の crypto.subtle の SHA-256 と、同じ埋め方で Python が組んだ JSON の SHA-256 と一致', q7,
  {'fill_rule': FILL_RULE, 'form_sha256': FORM_SHA, 'native_sha256': NATIVE, 'python_sha256': PY_SHA, 'python_equal_form': PY_SHA == FORM_SHA, 'json_bytes': len(JS_JSON.encode('utf-8')), 'n_keys': len(obj),
   'note': ('ブラウザ標準の SHA-256 は未実施（アプリ内のブラウザは様式を data: の写しで開き、安全な文脈にならず crypto.subtle が無い・静的なサーバの起動は別のプロジェクトの設定に解決された）' if NATIVE == NOT_DONE else '')})
EXTRA['prediction_d'] = {'hit': (q7 if NATIVE != NOT_DONE else None)}

# ---- Q7b（事後に足した補助の確かめ・2026-09-15・Q7 の (i) が行えなかったため）: 様式の JS の sha256hex と Python の hashlib を既知の文字列の組で突き合わせる
VEC = ['', 'abc', 'a' * 55, 'a' * 56, 'a' * 64, 'a' * 119, 'a' * 120, 'a' * 1000, '予想しない', '規模が大きいほど、A の破局率が B に比べて上がる側へ動く', '段階A・β₃・〜・（）', 'x' * 5388]
VH = [hashlib.sha256(s.encode('utf-8')).hexdigest().upper() for s in VEC]; VDD = hashlib.sha256(','.join(VH).encode('utf-8')).hexdigest().upper()
BDD = (a.browser_vectors_dd or '').strip().upper()
R('Q7b', '（事後に足した補助）様式の JS の sha256hex が、既知の文字列の組（空・abc・ブロックの境の長さ・長い文字列・日本語・様式の JSON と同じ長さ）で Python の SHA-256 と一致し（各値をつないだ文字列の SHA-256 で照合）、様式が表示した値が Python の組み立てと一致',
  bool(BDD) and BDD == VDD and PY_SHA == FORM_SHA, {'vectors': len(VEC), 'python_dd': VDD, 'browser_dd': BDD, 'abc': VH[1], 'python_equal_form': PY_SHA == FORM_SHA})

# ---- Q8: 照合の器（自己検査・件数を別に数えて突合・止まる JSON・すべて予想しない）
rc_st, o_st = run([tool('compare_predictions_A.py'), '--selftest'])
CHK = os.path.join(a.work, 'check'); rc8, o8 = run([tool('compare_predictions_A.py'), '--pred', PQ7, '--analysis', a.analysis, '--out', CHK])
CJ = runs_A.read_json(CHK + '.json') if rc8 == 0 else {}
AN = runs_A.read_json(a.analysis); LAB = T['families']['A_slope']['confirm_rule']['labels']; NOTP = P['not_predicted']
seen = {c['id']: (c.get('label'), (c.get('result') or {}).get('beta')) for c in AN['contrasts']}; flags = {r['id']: r.get('flag') for r in AN['floor']}
EXP_C = {kd: collections.Counter() for kd in ('向き', '床持続', '全体')}
for c in CON:
    v = vals[FLD['direction']['key_prefix'] + c['id']]; lab, beta = seen.get(c['id'], (None, None)); o_ = FLD['direction']['options']
    if v == NOTP:
        r_ = '予想しない'
    elif lab == LAB['confirmed'] and beta:
        r_ = '的中' if v == (o_[1] if beta > 0 else o_[2]) else '外れ'
    elif lab == LAB['ns']:
        r_ = '的中' if v == o_[3] else '外れ'
    else:
        r_ = '照合不能'
    EXP_C['向き'][r_] += 1
for c in CELLS:
    v = vals[FLD['floor']['key_prefix'] + c['id']]; f_ = flags.get(c['id']); o_ = FLD['floor']['options']
    r_ = '予想しない' if v == NOTP else ('照合不能' if f_ not in (0, 1) else ('的中' if v == (o_[1] if f_ == 1 else o_[2]) else '外れ'))
    EXP_C['床持続'][r_] += 1
n_conf = AN['label_counts']['confirmed']; n_meas = len([t for t, v in AN['measurable']['types'].items() if v['measurable']])
for B_, n_ in ((FLD['confirmed_band'], n_conf), (FLD['measurable_band'], n_meas)):
    v = vals[B_['key']]; idx = [i for i, (lo, hi) in enumerate(B_['edges']) if lo <= n_ <= hi]
    EXP_C['全体']['予想しない' if v == NOTP else ('的中' if len(idx) == 1 and v == B_['options'][idx[0] + 1] else '外れ')] += 1
got8 = (CJ.get('summary') or {}).get('pred-q7.json', {}).get('counts') or {}
match8 = bool(got8) and all(got8.get(kd, {}).get(r, -1) == EXP_C[kd][r] for kd in EXP_C for r in RES)


def variant(fn, name):
    o2 = json.loads(JS_JSON); fn(o2); p = os.path.join(a.work, name); open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(o2, ensure_ascii=False, indent=1)); return p


EXPK = E_DIR | E_FLOOR | E_ALL
p_miss = variant(lambda o: o.pop(sorted(E_DIR)[0]), 'pred-missing.json'); p_bad = variant(lambda o: o.__setitem__(sorted(E_FLOOR)[0], '選択肢の外'), 'pred-bad.json')
p_notp = variant(lambda o: [o.__setitem__(k, NOTP) for k in list(o) if k in EXPK], 'pred-notp.json')
rc_m, o_m = run([tool('compare_predictions_A.py'), '--pred', p_miss, '--analysis', a.analysis, '--out', os.path.join(a.work, 'chk-m')])
rc_b, o_b = run([tool('compare_predictions_A.py'), '--pred', p_bad, '--analysis', a.analysis, '--out', os.path.join(a.work, 'chk-b')])
rc_n, o_n = run([tool('compare_predictions_A.py'), '--pred', p_notp, '--analysis', a.analysis, '--out', os.path.join(a.work, 'chk-n')])
CN = runs_A.read_json(os.path.join(a.work, 'chk-n.json')) if rc_n == 0 else {}
notp_ok = rc_n == 0 and CN['summary']['pred-notp.json']['counts'] == {kd: {r: (n_ if r == '予想しない' else 0) for r in RES} for kd, n_ in (('向き', len(CON)), ('床持続', len(CELLS)), ('全体', 2))}
R('Q8', '照合の器: 自己検査が通り、Q7 の埋め方の予想の件数が本器の別の数えと一致・欠けと選択肢の外で止まる・すべて予想しないは予想しないだけ',
  rc_st == 0 and 'SELFTEST PASS' in o_st and rc8 == 0 and match8 and rc_m != 0 and '止める' in o_m and rc_b != 0 and '止める' in o_b and notp_ok,
  {'selftest_rc': rc_st, 'selftest_tail': o_st.strip()[-160:], 'rc': rc8, 'got': got8, 'expected': {kd: dict(EXP_C[kd]) for kd in EXP_C}, 'missing_rc': rc_m, 'bad_rc': rc_b, 'notp_ok': notp_ok,
   'n_conf': n_conf, 'n_meas': n_meas})

# ---- Q9: 凍結器の --check と --list（反映の前の凍結器と対象の数を比べる）
FB = base_file('tools/freeze_A.py', 'freeze_A_base.py')
rc_b9, o_b9 = run([FB, '--check'], env_extra={'PYTHONPATH': os.path.join(REPO, 'tools')}); mb9 = re.search(r'対象 (\d+)', o_b9); n_base = int(mb9.group(1)) if mb9 else -1
rc_n9, o_n9 = run([tool('freeze_A.py'), '--check']); mn9 = re.search(r'対象 (\d+)・欠け (\d+)・枠の検証 (\S+)', o_n9); miss9 = re.findall(r'欠け: (\S+)', o_n9)
rc_l9, o_l9 = run([tool('freeze_A.py'), '--list']); lst = re.findall(r'^  対象: (\S+?)(?:（欠け）)?$', o_l9, flags=re.M)
NEW4 = ['tools/make_predictions_form_A.py', 'tools/compare_predictions_A.py', P['form'], P['js_source']]
R('Q9', '凍結器: --check の欠けが凍結本文の二つだけで枠の検証が一致・凍結範囲が反映の前より四つ多く、その四つが器二つと様式と JS の出所',
  rc_n9 == 2 and bool(mn9) and mn9.group(3) == '一致' and sorted(miss9) == ['design/design-stageA-FROZEN.md', 'design/design-stageA-FROZEN.src.md'] and rc_l9 == 0
  and n_base > 0 and len(lst) == int(mn9.group(1)) == n_base + 4 and all(x in lst for x in NEW4),
  {'base_count': n_base, 'base_rc': rc_b9, 'new': mn9 and mn9.groups(), 'check_rc': rc_n9, 'missing': miss9, 'list_rc': rc_l9, 'list_len': len(lst), 'new4_in_list': [x for x in NEW4 if x in lst]})

# ---- Q10: 凍結器の自己検査と報告の組み立て器 v2.4
src_f = open(tool('freeze_A.py'), encoding='utf-8').read(); SELF = next(ast.literal_eval(n.value) for n in ast.walk(ast.parse(src_f)) if isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == 'SELFTESTS' for t in n.targets))
ST = []
if not a.skip_selftests:
    for nm, args in SELF:
        rc_, o_ = run([tool(nm)] + args); ST.append({'tool': nm, 'rc': rc_, 'tail': o_.strip()[-200:]})
REP = os.path.join(a.work, 'report', 'report.md'); os.makedirs(os.path.dirname(REP), exist_ok=True)
rc10, o10 = run([tool('build_report_A.py'), '--draft', '1', '--analysis', a.analysis, '--predictions', CHK + '.json', '--out', REP, '--force', '--allow-dev-marks'])
txt10 = open(REP, encoding='utf-8').read() if os.path.exists(REP) else ''; MBK = T['report_rules']['machine_block']
blocks = re.findall(re.escape(MBK['begin']) + r'\n(.*?)\n' + re.escape(MBK['end']), txt10, flags=re.S)
R('Q10', '凍結器の自己検査（照合の器を含む）がすべて通る・報告の組み立て器 v2.4 が照合の記録を機械の区画に置き、改めた柵の文言がある',
  bool(ST) and all(x['rc'] == 0 for x in ST) and any(x['tool'] == 'compare_predictions_A.py' for x in ST) and rc10 == 0 and any('pred-q7.json' in b for b in blocks)
  and '的中は独立の確認ではなく、誰の判断の重みも変えない' in txt10 and '帯の的中' not in txt10,
  {'selftests': [{'tool': x['tool'], 'rc': x['rc'], 'tail': x['tail'][-100:]} for x in ST], 'report_rc': rc10, 'report_tail': o10[-240:], 'pred_in_block': any('pred-q7.json' in b for b in blocks)})

# ---- 記録
ORDER = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q7b', 'Q8', 'Q9', 'Q10']; ROWS.sort(key=lambda r: ORDER.index(r['id']))
PRE = [r for r in ROWS if r['id'] != 'Q7b']
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
TOOLS = ['make_contrasts_A.py', 'make_predictions_form_A.py', 'compare_predictions_A.py', 'freeze_A.py', 'design_facts_A.py', 'build_report_A.py', 'tooling_interpretations_A.py', 'verify_freeze_prep_A.py']
OUT = {'kind': 'verification_freeze_prep_A', 'version': VERSION, 'generated_utc': now, 'pass': all(r['pass'] for r in ROWS), 'n_pass_preregistered': sum(r['pass'] for r in PRE), 'n_preregistered': len(PRE),
       'auxiliary_after_the_fact': [r['id'] for r in ROWS if r['id'] == 'Q7b'], 'contrasts_sha16': runs_A.sha16_file(runs_A.CPATH), 'base_commit': a.base, 'tools_sha16': {t: runs_A.sha16_file(tool(t)) for t in TOOLS},
       'form_sha16': runs_A.sha16_file(HTMLP), 'rows': ROWS, 'extra': EXTRA, 'preregistration': 'records/A/freeze-prep/preregistration-freeze-prep-A.md',
       'clause': '本記録のいかなる記述も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(os.path.dirname(a.out), exist_ok=True)
open(a.out + '.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(OUT, ensure_ascii=False, indent=1) + '\n')
short = lambda d: json.dumps(d, ensure_ascii=False)[:600].replace('|', '／')
DTXT = {True: '的中', False: '外れ', None: '照合できない（ブラウザ標準の SHA-256 は未実施・補助の Q7b を事後に足した）'}
M = ['# 凍結の前の登録者裁定 D45〜D47 の反映の確かめ（機械生成・`tools/verify_freeze_prep_A.py` %s・%s UTC）' % (VERSION, now), '',
     '- 事前登録: `%s`（確かめの条件 Q1〜Q10 は器を書く前に記録した・コミット 2736c2d）。Q7b は Q7 の (i) が行えなかったので事後に足した補助の確かめで、事前登録の条件ではない。' % OUT['preregistration'],
     '- 結果: 事前登録の条件 %d/%d 合格・補助 Q7b %s・正本 SHA16 %s・様式 SHA16 %s・反映の前の基準のコミット %s' % (OUT['n_pass_preregistered'], OUT['n_preregistered'], '合格' if all(r['pass'] for r in ROWS if r['id'] == 'Q7b') else '不合格', OUT['contrasts_sha16'], OUT['form_sha16'], a.base),
     '- 器の SHA16: %s' % '・'.join('%s %s' % kv for kv in OUT['tools_sha16'].items()), '',
     '| id | 確かめ | 結果 | 詳細（先頭のみ・全体は JSON） |', '|---|---|---|---|']
M += ['| %s | %s | %s | %s |' % (r['id'], r['what'], '合格' if r['pass'] else '**不合格**', short(r['detail'])) for r in ROWS]
M += ['', '## 予想の照合（事前登録 §5 のうち本器で照合できるもの）', '',
      '- (a) Q2 の格子の値の差は零: 結果 %d（%s）' % (EXTRA['prediction_a']['got'], '的中' if EXTRA['prediction_a']['hit'] else '外れ'),
      '- (b) Q3 は満たされる: %s' % ('的中' if EXTRA['prediction_b']['hit'] else '外れ'),
      '- (d) Q7 の三つの SHA-256 は一致する: %s' % DTXT[EXTRA['prediction_d']['hit']],
      '- (c)・(e)・(f)・(g) は反映の記録に書く（走行の経過で決まる）。', '',
      '- 限界: 合成の集計の記録は本物の出力の分布を再現しない。アプリ内のブラウザは登録者の Chrome ではない。Q8 の別の数えは照合の規則を同じ正本の文言から書き起こしたもので、規則の読み違いが二つに同じく入る場合は見分けない。', '',
      OUT['clause']]
open(a.out + '.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(M) + '\n')
print('[verify_freeze_prep_A] 事前登録の条件 %d/%d 合格・補助 %s → %s.{json,md}' % (OUT['n_pass_preregistered'], OUT['n_preregistered'], [(r['id'], r['pass']) for r in ROWS if r['id'] == 'Q7b'], a.out))
sys.exit(0 if OUT['pass'] else 1)
