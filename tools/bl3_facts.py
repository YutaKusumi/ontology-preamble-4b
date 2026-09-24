# -*- coding: utf-8 -*-
"""bl3_facts.py v2 —— B-lens 層三（Bl3）の枠に置く設計の事実（転記行 A〜F）を、記録と凍結物から機械で作る（草案1）。
**効き目は一つも計算しない**（順伝播をしない・方向を模型に足さない）。方向と帰無は作って SHA を取るだけ。
段階 B と B-lens の凍結した器（`tools/run_stageB_local.py`・`tools/steer_B.py`・`tools/blens_core.py`）は読み取りだけで呼び、変えない。
出力: records/Bl3/design-facts-Bl3.json・records/Bl3/design-facts-Bl3.md
用法: python tools/bl3_facts.py [--tokenizer 置き場] [--skip-weights-hash]
柵: 本器の出力のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。"""
import os, re, sys, json, glob, hashlib, argparse, datetime, collections
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
j = lambda *p: os.path.join(REPO, *p)
NL = chr(10)
VERSION = 'v2'
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
ACT = os.path.expanduser('~/.cache/op4b-dir/dirB__s1/main_position_activations.npz')
ap = argparse.ArgumentParser()
ap.add_argument('--tokenizer', default=os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
ap.add_argument('--skip-weights-hash', action='store_true')
a = ap.parse_args()
s16f = lambda p: hashlib.sha256(open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
sha_arr = lambda x: hashlib.sha256(np.ascontiguousarray(np.asarray(x, dtype=np.float64)).tobytes()).hexdigest().upper()
T3 = json.load(open(j('design', 'contrasts-Bl3.json'), encoding='utf-8'))
TL = json.load(open(j('design', 'contrasts-Blens.json'), encoding='utf-8'))
AN = json.load(open(j('records', 'B', 'analysis-B-2026-09-22.json'), encoding='utf-8'))
import run_stageB_local as RB          # 凍結（読み取りだけ）
import steer_B                          # 凍結（読み取りだけ）
import blens_core as C                  # 凍結（読み取りだけ）
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(a.tokenizer)
enc = lambda s: tok.encode(s, add_special_tokens=False)
dec = lambda i: tok.decode([int(i)])
F = collections.OrderedDict()


def cell_dir(sc, arm):
    return j('results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))


def trials_raw(sc, arm):
    d = cell_dir(sc, arm)
    T_ = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')}
    R_ = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
    return [(T_[k], R_[k]) for k in sorted(T_, key=lambda k: T_[k]['trial_index'])]


# ---------------- 転記行 A: 読み取りの書き出し（甲）と割り方 ----------------
KEY = '"choice": "'
json_texts, prose_key_texts, n_prose = [], [], 0
json_by_cell = collections.Counter()
cells_all = sorted(os.path.basename(d) for d in glob.glob(j('results', 'stageB', 'stageB__*__s1')))
for cd in cells_all:
    sc, arm = cd.split('__')[1], cd.split('__')[2]
    for t, r in trials_raw(sc, arm):
        if t['status'] != 'ok':
            continue
        if t['style_b']:
            json_texts.append(r['text'])
            json_by_cell['%s|%s' % (sc, arm)] += 1
        else:
            n_prose += 1
            if KEY in r['text']:
                prose_key_texts.append(r['text'])
heads = collections.Counter(tx[:tx.index(KEY) + len(KEY)] for tx in json_texts if KEY in tx)
assert len(heads) == 1, ('JSON 直答の出力の書き出しが一つにそろわない', heads.most_common(3))
V0 = list(heads)[0]
ids0 = enc(V0)
head_match = sum(1 for tx in json_texts if enc(tx)[:len(ids0)] == ids0)
assert head_match == len(json_texts), ('書き出しの割り方が出力の頭と一致しない', head_match, len(json_texts))
fam_letters = T3['readout']['primary']['letters']
letters = sorted({x for v in fam_letters.values() for x in v})
letter_ids, boundary = {}, {}
for x in letters + ['refuse']:
    e = enc(V0 + x)
    boundary[x] = (e[:len(ids0)] == ids0)
    letter_ids[x] = e[len(ids0)]
assert all(boundary.values()), boundary
assert dec(letter_ids['refuse']) == T3['readout']['primary']['refuse_head'], dec(letter_ids['refuse'])
assert all(dec(letter_ids[x]) == x for x in letters), {x: dec(letter_ids[x]) for x in letters}
V1 = V0.split(NL, 1)[1]
V2 = V0.replace('{' + KEY, '{' + NL + '  ' + KEY)
variants = collections.OrderedDict([('V1', V1), ('V2', V2)])
var_ok = collections.OrderedDict()
for name, v in variants.items():
    iv = enc(v)
    ok = all(enc(v + x)[:len(iv)] == iv and dec(enc(v + x)[len(iv)]) == (x if x != 'refuse' else 'ref') for x in letters + ['refuse'])
    var_ok[name] = {'string': v, 'ids': iv, 'pieces': [dec(i) for i in iv], 'boundary_ok': ok}
first_letters = collections.Counter(dec(enc(tx)[len(ids0)]) for tx in json_texts)
prose_with_prefix = sum(1 for tx in prose_key_texts if V0 in tx)
assert sum(json_by_cell.values()) == len(json_texts)
F['A'] = {'text': ('主の書き出し（甲）: 段階 B の本走行の JSON 直答の出力 %d 件の、選択の値の直前までの書き出しは一つにそろう（%s）。割り方は %d トークン（%s）で、%d 件すべての出力の割り方の頭と一致する。'
                   '書き出しの次のトークン（読み取りの集合）: %s（refuse は頭のトークン %d「%s」）。どの文字を足しても書き出しの割り方は変わらない。JSON 直答の出力の選択の値の最初のトークン: %s。'
                   '揺れの版（下見の (iv) だけに使う）: %s。散文の出力（使えた試行のうち JSON 直答の型でないもの）%d 件のうち、選択の鍵の文字列（%s）を含むもの %d 件・主の書き出しの文字列をそのまま含むもの %d 件（記述）。'
                   'JSON 直答の型の出力のある升目（全 %d 升目のうち %d 升目）: %s。')
                  % (len(json_texts), repr(V0), len(ids0), '・'.join('%d「%s」' % (i, dec(i).replace(NL, '⏎')) for i in ids0), head_match,
                     '・'.join('%s %d' % (x, letter_ids[x]) for x in letters), letter_ids['refuse'], dec(letter_ids['refuse']),
                     '・'.join('%s %d' % kv for kv in sorted(first_letters.items())),
                     '／'.join('%s %s（%d トークン・割り方の境を%s）' % (k, repr(v['string']), len(v['ids']), '保つ' if v['boundary_ok'] else '崩す・下見で使わない') for k, v in var_ok.items()),
                     n_prose, repr(KEY), len(prose_key_texts), prose_with_prefix,
                     len(cells_all), len(json_by_cell), '・'.join('%s %d' % kv for kv in sorted(json_by_cell.items(), key=lambda kv: (-kv[1], kv[0])))),
          'prefix': V0, 'prefix_ids': ids0, 'letter_ids': letter_ids, 'variants': var_ok, 'json_direct_n': len(json_texts), 'first_letters': dict(first_letters),
          'json_direct_by_cell': dict(json_by_cell), 'prose_n': n_prose, 'prose_with_key': len(prose_key_texts), 'prose_with_prefix': prose_with_prefix}

# ---------------- 転記行 B: 升目（プロンプトの長さ・主位置・読み取りの位置・無操作の観測） ----------------
AT = RB.arm_texts()
BD = AN['by_direction']
noop = {}
for r in BD:
    if r['direction_id'] == 'fixed' and '+v' not in r['arm'] and '-v' not in r['arm']:
        noop[(r['scenario'], r['arm'])] = r
ARM_RE = re.compile(r'^(.*?)([+-])v(rand|Nk|td|\db)?$')              # 最後の枝は (6b) の腕（B-lens の器と同じ書き方）
KIND = {'': 'static', 'rand': 'rand', 'Nk': 'Nk', 'td': 'td'}                    # 残りの枝は loaded
gate_rows, gate_excl = [], collections.Counter()
for r in BD:
    m = ARM_RE.match(r['arm'])
    if not m:
        continue
    base = noop[(r['scenario'], m.group(1))]
    unit = r['direction_id'] if (m.group(3) == 'rand') else KIND.get(m.group(3) or '', 'loaded')
    row = {'scenario': r['scenario'], 'arm': r['arm'], 'direction_id': r['direction_id'], 'base': m.group(1), 'sign': 1 if m.group(2) == '+' else -1, 'unit': unit}
    if 0 < base['cat'] < base['n_ok']:
        gate_rows.append(row)
    else:
        gate_excl['%s（土台 %s・%s）' % ('rand' if m.group(3) == 'rand' else unit, m.group(1), r['scenario'])] += 1
n_gate, n_wo = len(gate_rows), sum(1 for r in gate_rows if r['unit'] != 'static')
assert (n_gate, n_wo) == (T3['gate']['rows_gate'], T3['gate']['rows_without_vhat']), (n_gate, n_wo)
assert len({(r['scenario'], r['arm'], r['direction_id']) for r in gate_rows}) == n_gate, '門の行が場面・腕・方向の番号で一つに決まらない'
cells_gate = sorted({(r['scenario'], r['base']) for r in gate_rows})
cell_signs_gate = sorted({(r['scenario'], r['base'], r['sign']) for r in gate_rows})
cells_main = [tuple(c) for c in T3['cells_main']]
cells_B = sorted(set(cells_main) | set(cells_gate))
Bcell = collections.OrderedDict()
for sc, arm in cells_B:
    scen, inst = RB.scenario_and_instruction(sc)
    ids = steer_B.apply_chat(tok, RB.user_message(AT[arm]['text'], scen['text'], inst))
    mp = steer_B.main_position(ids)
    trs = [t for t, _ in trials_raw(sc, arm) if t['status'] == 'ok']
    obs = collections.Counter(t['choice'] for t in trs)
    fam = scen['family']
    assert set(obs) <= set(fam_letters[fam]) | {'refuse'}, (sc, arm, fam, sorted(obs))
    cat = sum(1 for t in trs if t['catastrophe'])
    b = noop[(sc, arm)]
    assert b['n_ok'] == len(trs) and b['cat'] == cat, (sc, arm, b['n_ok'], len(trs), b['cat'], cat)
    Bcell['%s|%s' % (sc, arm)] = {'family': fam, 'prompt_len': len(ids), 'main_position': mp, 'readout_position': mp + len(ids0), 'n_ok': len(trs), 'choices': dict(obs), 'catastrophe': cat,
                                  'a_not_catastrophe': obs['a'] - cat, 'json_direct': sum(1 for t in trs if t['style_b']), 'preamble_sha16': AT[arm]['sha16'], 'in_main': (sc, arm) in cells_main}
    assert mp == len(ids) - 1
F['B'] = {'text': ('升目（場面 × 土台の腕・無操作・括弧は場面の族）ごとの、チャットの型を当てた後のプロンプトの長さ・主位置（凍結の `steer_B.main_position`）・読み取りの位置（主位置 ＋ 書き出しの %d トークン）と、段階 B の無操作の観測（使えた試行・選択の件数・破局の件数・JSON 直答の件数）: %s。'
                   '主の行の升目 %d・門の行だけの升目 %d。加減の帯は主位置から読み取りの位置までの %d 位置で、主位置より前の位置は帯の外（因果の注意では、帯の外の位置の計算は方向に依らない）。'
                   '段階 B の破局は選択 (a) のうち量が零でないもので（凍結の採点）、量が零の (a) は破局に数えない。読み取りは選択の文字だけを読み、量を読まない——量が零の (a) の件数: %s。')
                  % (len(ids0), '／'.join('%s（%s）: 長さ %d・主位置 %d・読み取り %d・観測 %d 件（%s・破局 %d・JSON 直答 %d）%s' % (k, v['family'], v['prompt_len'], v['main_position'], v['readout_position'], v['n_ok'],
                                                                                          '・'.join('%s %d' % kv for kv in sorted(v['choices'].items())), v['catastrophe'], v['json_direct'], '' if v['in_main'] else '〔門だけ〕')
                                          for k, v in Bcell.items()),
                     sum(1 for v in Bcell.values() if v['in_main']), sum(1 for v in Bcell.values() if not v['in_main']), len(ids0) + 1,
                     '・'.join('%s %d' % (k, v['a_not_catastrophe']) for k, v in Bcell.items() if v['a_not_catastrophe']) or '無し'),
          'cells': Bcell}

# ---------------- 転記行 C: 主の行と門の行 ----------------
units = collections.Counter(r['unit'] for r in gate_rows)
gate_a0 = collections.OrderedDict()
for r in gate_rows:
    trs_ = [t for t, _ in trials_raw(r['scenario'], r['arm']) if t['status'] == 'ok' and t['direction_id'] == r['direction_id']]
    assert trs_, ('門の行の試行が無い', r)
    n_a = sum(1 for t in trs_ if t['choice'] == 'a')
    n_cat = sum(1 for t in trs_ if t['catastrophe'])
    assert n_cat <= n_a and all(t['choice'] == 'a' for t in trs_ if t['catastrophe']), ('破局が (a) の外にある', r['scenario'], r['arm'])
    k_ = '%s|%s' % (r['scenario'], r['arm']) + ('〔%s〕' % r['direction_id'] if ARM_RE.match(r['arm']).group(3) == 'rand' else '')
    assert k_ not in gate_a0, ('門の行の名が重なる', k_)
    gate_a0[k_] = n_a - n_cat
gate_a0_pos = [(k, v_) for k, v_ in gate_a0.items() if v_]
F['C'] = {'text': ('主の行（段階 B の確証の族・凍結した集計器の記録の `confirm`）: %d 行——%s。升目と符号の組 %d（%s）。'
                   '門の行（`by_direction` のうち土台の無操作の腕の破局が零でも全部でもない行・B-lens の門と同じ決まり）: %d 行（v̂ を抜くと %d）・方向の単位ごと %s・床か天井の土台で外す行 %s。'
                   '門の行の升目と符号の組 %d（主の行に無い組: %s）。行の行動の値は、凍結の後に門の器が集計の記録から読む（この転記行には置かない）。'
                   '門の行（加えた腕・ランダム方向の腕は方向の番号ごと）のうち、選択が (a) でも量が零で破局に数えない試行がある行: %d 行（門の行 %d 行のうち）——%s。門の行動の量は破局を数え、読み取りは選択の文字 a を読むので、この件数だけ二つが食い違う（どの破局も選択 (a) の中にある）。')
                  % (len(T3['main_rows']), '・'.join('%s（%s%s）' % (r['id'], '+' if r['sign'] > 0 else '−', r['direction']) for r in T3['main_rows']),
                     len(T3['cell_signs_main']), '・'.join('%s|%s|%s' % (s, b, '+' if g > 0 else '−') for s, b, g in T3['cell_signs_main']),
                     n_gate, n_wo, '・'.join('%s %d' % kv for kv in sorted(units.items())), '・'.join('%s %d' % kv for kv in sorted(gate_excl.items())),
                     len(cell_signs_gate), '・'.join('%s|%s|%s' % (s, b, '+' if g > 0 else '−') for s, b, g in cell_signs_gate if [s, b, g] not in T3['cell_signs_main']) or '無し',
                     len(gate_a0_pos), len(gate_rows), '・'.join('%s %d' % kv for kv in sorted(gate_a0_pos, key=lambda kv: (-kv[1], kv[0]))) or '無し'),
          'gate_rows': gate_rows, 'cell_signs_gate': [list(x) for x in cell_signs_gate], 'gate_a_not_catastrophe': dict(gate_a0)}

# ---------------- 転記行 D: 方向と帰無（作って SHA を取るだけ） ----------------
sel = str(T3['layers']['selected_ratio'])
D = np.load(j('results', 'dirB', 'dirB__s1', 'directions.npz'))
v = D['static__%s' % sel].astype(np.float64)
nv = float(np.linalg.norm(v))
named = collections.OrderedDict((k, steer_B.match_to_static(D['%s__%s' % (k, sel)].astype(np.float64), v)) for k in T3['directions']['named'])
b3 = np.array(steer_B.random_directions(v, 'main', float(sel)))
b3_copy = C.iso_directions(v, TL['nulls']['B_random']['main_seed'], float(sel), T3['nulls']['B_random']['count'], TL['nulls']['isotropic']['layer_key_scale'])
b3_rel = float(np.max(np.abs(b3 - b3_copy)) / np.max(np.abs(b3)))
assert b3_rel <= T3['nulls']['B_random']['repro_tol'], b3_rel
iso = C.iso_directions(v, T3['nulls']['isotropic']['seed'], float(sel), T3['nulls']['isotropic']['count'], T3['nulls']['isotropic']['layer_key_scale'])
DJ = json.load(open(j('results', 'dirB', 'dirB__s1', 'directions.json'), encoding='utf-8'))
act_sha = hashlib.sha256(open(ACT, 'rb').read()).hexdigest().upper()
assert act_sha == DJ['activations_npz_sha256'].upper(), '活性のファイルが凍結の記録と違う'
Z = np.load(ACT)
arm_means = collections.OrderedDict((arm, np.mean([Z['same_order__%s__%s__%s' % (arm, sc, sel)].astype(np.float64) for sc in DJ['extraction_scenarios']], axis=0)) for arm in T3['nulls']['real']['arms'])
real = C.real_differences(arm_means, nv)
assert len(real) == T3['nulls']['real']['pairs']
norms = [float(np.linalg.norm(x)) for x in list(named.values()) + list(b3) + list(iso) + list(real.values())]
n_all = len(norms)
F['D'] = {'text': ('選んだ層（層の割合 %s）の方向と帰無。‖v̂‖ %.6g に全ての方向を合わせた（ノルムの相対の差の最大 %.1e）。名前のある方向 %d 本（%s・凍結の npz）・SHA-256 %s。'
                   '段階 B の本走行のランダム方向 %d 本（凍結の `steer_B.random_directions` で再生・写した作り方との相対の差の最大 %.1e・許容 %g）・SHA-256 %s。'
                   '等方のランダム方向 %d 本（種 %d・同じ作り方）・SHA-256 %s。実在の差の方向 %d 組（凍結の活性〔SHA-256 の頭 %d 桁 %s〕の、抽出の場面の平均の八腕の全ての対・ノルムを揃えた）・SHA-256 %s。'
                   'これらは下見の前の凍結で一つの npz にまとめ、その SHA を凍結の記録に置く（Colab で乱数を引き直さない）。まとめたときの大きさの見込み: 方向 %d 本 × 次元 %d × %d バイト（%s・圧縮なし）≒ %.1f MB。')
                  % (sel, nv, max(abs(x - nv) for x in norms) / nv, len(named), '・'.join(named), sha_arr(np.array(list(named.values()))),
                     len(b3), b3_rel, T3['nulls']['B_random']['repro_tol'], sha_arr(b3), len(iso), T3['nulls']['isotropic']['seed'], sha_arr(iso),
                     len(real), len(act_sha[:16]), act_sha[:16], sha_arr(np.array(list(real.values()))),
                     n_all, v.shape[0], np.dtype(np.float64).itemsize, np.dtype(np.float64).name, n_all * v.shape[0] * np.dtype(np.float64).itemsize / 1e6),
          'named_sha256': sha_arr(np.array(list(named.values()))), 'B_random_sha256': sha_arr(b3), 'iso_sha256': sha_arr(iso), 'real_sha256': sha_arr(np.array(list(real.values()))),
          'real_pairs': list(real), 'vhat_norm': nv}

# ---------------- 転記行 E: 費用の見込みの入力 ----------------
n_dirs = len(named) + len(b3) + len(iso) + len(real)
passes_main = len(T3['cell_signs_main']) * n_dirs
passes_gate_extra = (len(cell_signs_gate) - sum(1 for x in cell_signs_gate if list(x) in T3['cell_signs_main'])) * (len(named) + len(b3))
passes_orient_extra = sum(1 for sc_, b_, g_ in T3['cell_signs_main'] if [sc_, b_, -g_] not in T3['cell_signs_main']) * len(real)
assert T3['nulls']['real']['orientations'] == 2
lens = [v_['prompt_len'] for v_ in Bcell.values()]
FB = json.load(open(j('records', 'Blens', 'design-facts-Blens.json'), encoding='utf-8'))
sel_ctx = FB['facts']['E']['selected']
n_ctx = sum(len(x) for x in sel_ctx.values())
UJ = json.load(open(j('records', 'Blens', 'colab-units-Blens.json'), encoding='utf-8'))
ext = [s_ for s_ in UJ['steps'] if 'extract' in s_['step']]
F['E'] = {'text': ('主の計算の順伝播: 升目と符号の組 %d × 方向 %d（名前のある方向 %d・段階 B の三本 %d・等方 %d・実在の差 %d）＝ %d 回。門の行だけの組の分（名前のある方向と段階 B の三本だけ）%d 回。比べる相手を両方の向きで数えるために足す分（逆の符号の組が主の行に無い組の、実在の差の方向）%d 回。'
                   '一回の順伝播の長さ: 近道（主位置より前の計算を使い回す）なら %d 位置、近道なしならプロンプトの長さ（%d〜%d）＋ 書き出し %d。乙の文脈（B-lens の層二で選んだ出力）%d 件。'
                   '参考: B-lens の Colab の相 extract は %.2f ユニット（登録者の表示から）。')
                  % (len(T3['cell_signs_main']), n_dirs, len(named), len(b3), len(iso), len(real), passes_main, passes_gate_extra, passes_orient_extra,
                     len(ids0) + 1, min(lens), max(lens), len(ids0), n_ctx, ext[0]['used'] if ext else float('nan')),
          'passes_main': passes_main, 'passes_gate_extra': passes_gate_extra, 'passes_orient_extra': passes_orient_extra, 'n_dirs': n_dirs}

# ---------------- 転記行 F: 重みと版 ----------------
wf = {}
SHARDS = tuple(sorted(set(json.load(open(os.path.join(SNAP, 'model.safetensors.index.json'), encoding='utf-8'))['weight_map'].values())))   # 断片の名は索引から取る（手で打たない）
assert set(SHARDS) == {os.path.basename(x) for x in glob.glob(os.path.join(SNAP, 'model-*-of-*.safetensors'))}, ('索引の断片と置き場の断片が一致しない', SHARDS)
for fn in ('config.json', 'tokenizer.json', 'model.safetensors.index.json') + (() if a.skip_weights_hash else SHARDS):
    p = os.path.join(SNAP, fn)
    hsh = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 24), b''):
            hsh.update(chunk)
    wf[fn] = hsh.hexdigest().upper()
fb_text = FB['facts']['F']['text']
same = all(v_ in fb_text for v_ in wf.values())
F['F'] = {'text': ('重みの版は B-lens と同じ（%s）。手元の断片と設定の SHA-256 %d 個は、B-lens の転記行 F の値と%s（%s）。版の揃え方は B-lens と同じ（NumPy %s・transformers %s・torch %s・裁定 D187）。')
                  % (T3['inputs']['model']['rev'][:12], len(wf), 'すべて一致する' if same else '一致しないものがある', '・'.join('%s %s' % (k, v_[:16]) for k, v_ in wf.items()),
                     T3['inputs']['versions_B']['numpy'], T3['inputs']['versions_B']['transformers'], T3['inputs']['versions_B']['torch']),
          'sha256': wf, 'same_as_Blens': same}
assert same, '重みの SHA-256 が B-lens の記録と違う'

out = {'kind': 'bl3_design_facts', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'), 'contrasts_sha16': s16f(j('design', 'contrasts-Bl3.json')),
       'facts': F, 'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
os.makedirs(j('records', 'Bl3'), exist_ok=True)
jp = j('records', 'Bl3', 'design-facts-Bl3.json')
json.dump(out, open(jp, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
M = ['# B-lens 層三の設計の事実（機械生成・`tools/bl3_facts.py` %s・%s UTC・正本 SHA16 %s）' % (VERSION, out['generated_utc'], out['contrasts_sha16']), '',
     '- 効き目は一つも計算していない（順伝播をしない・方向を模型に足さない）。方向と帰無は作って SHA を取るだけ。', ''] + ['- **転記行 %s** — %s' % (k, v_['text']) for k, v_ in F.items()] + [
     '', '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。', '']
open(j('records', 'Bl3', 'design-facts-Bl3.md'), 'w', encoding='utf-8', newline=NL).write(NL.join(M))
print('wrote records/Bl3/design-facts-Bl3.{json,md} | rows', ''.join(F), '| json-direct', len(json_texts), '| gate', n_gate, n_wo, '| passes', passes_main, passes_gate_extra, passes_orient_extra)
