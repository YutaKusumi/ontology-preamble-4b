# -*- coding: utf-8 -*-
"""blens_sets.py v1 —— B-lens の語の集合を、射影を一つも計算する前に作って凍結する（2026-09-23・正本 `token_sets`・`nulls.word_side`・裁定 D168・D179・D184）。

作るもの（正本の規則の文から、下書きの器 `tools/blens_facts.py` とは別に書いた）:
  - L（答えの文字）・R（拒否）: `{"choice": "x"` の値の最初のトークン。
  - E（語の反響）: 方向を作った二つの腕の前置きの本文のトークンの差（場面の本文と JSON の指示のトークンを除く）。v̂ と (6b) は O と Osec、td は Onull、Nk は Nk の一行。
  - X（選択肢の語）: 家族ごとの選択肢の文の、(a) にだけあるトークンと、ほかの選択肢にだけあるトークン。場面の幹・JSON の指示・腕の前置きに現れるものに印。
  - F（様式）: 主は B の無操作の腕の JSON 直答の出力の最初のトークン。感度は散文の出力の最初のトークンのうち、断片・なぞり・ほかの集合との重なりを除いた上位。
  - 語の側の帰無の候補と層（字の決まり・字の種類 × 字数 × ノルムの帯・薄い層の合わせ方）と、B の無操作の出力に現れたトークンに限った感度の候補。
  各集合は、主（中身の語から片仮名一字を除く）と感度（片仮名一字を含む中身の語・全てのトークン・二字以上）に分ける。断片は除いて数を残す。
確かめ（正本 `checks`・裁定 D184）:
  - 単独で割った集合が、下書きの器の集合とバイトで一致する（正本の形に並べ直した JSON を比べる）。外れたら止める（非零で終わる・登録者に相談）。
  - 組み立てたプロンプト（段階 B の凍結の組み立て `run_stageB_local.user_message` と `steer_B.apply_chat`）の中で割った集合と、単独で割った集合を比べる。
    組み立てた中で、字の範囲（前置き・場面の幹・選択肢の文・指示）にすっぽり入るトークンを集め、単独のときと同じ規則で集合を作る。
    違えば、組み立てた中の集合を主にし、単独の集合を感度（`sets_standalone`）にして、違ったトークンを印字して続ける。場面によって組み立てた中の集合が違うときは止める。
    範囲にまたがるトークン（例: 句点と改行が一つになったトークン・空白と字の頭のバイトが一つになったトークン）は印字する。
出力: records/Blens/sets-Blens.json（凍結する集合）と records/Blens/sets-Blens.md（要約）。--force が無ければ上書きしない。
用法: python tools/blens_sets.py [--force] ／ --selftest
柵: 本器のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。
"""
import os, re, sys, json, glob, hashlib, argparse, datetime, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import blens_core as C

VERSION = 'v1'
NL = chr(10)
SNAP = os.path.expanduser('~/.cache/huggingface/hub/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554')
OUT_JSON = os.path.join(REPO, 'records', 'Blens', 'sets-Blens.json')
OUT_MD = os.path.join(REPO, 'records', 'Blens', 'sets-Blens.md')
FACTS = os.path.join(REPO, 'records', 'Blens', 'design-facts-Blens.json')
SCENES = ('N1', 'S1', 'SK', 'S4')
ARMS_E = ('O', 'Osec', 'Onull', 'Nk', 'O-Ncold', 'Osec-Ncold')
REPL = '�'
# 字の範囲（中身の語の規則は「々」と長音符と中黒を字に数えない・字の決まりは「々」と長音符を字に入れる）
KJ, KT, HR, NOMA, BAR = (0x4E00, 0x9FFF), (0x30A1, 0x30FA), (0x3041, 0x3096), 0x3005, 0x30FC
E_FIELDS = ('plus', 'minus', 'plus_kata1', 'minus_kata1', 'plus_all', 'minus_all', 'plus_multi', 'minus_multi', 'fragments', 'single_kata_removed')
rel = lambda p: os.path.relpath(p, REPO).replace(os.sep, '/')
sha16b = lambda b: hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest().upper()[:16]
sha16f = lambda p: sha16b(open(p, 'rb').read())
dumps = lambda o: json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def n_kj(s):
    return sum(1 for ch in s if KJ[0] <= ord(ch) <= KJ[1])


def n_kt(s):
    return sum(1 for ch in s if KT[0] <= ord(ch) <= KT[1])


class Words:
    """トークンの読みと規則（トークナイザを一度だけ読む）。"""
    def __init__(self, tok):
        self.tok = tok
        self._d = {}

    def dec(self, i):
        if i not in self._d:
            self._d[i] = self.tok.decode([int(i)])
        return self._d[i]

    def ids(self, s):
        return list(self.tok(s, add_special_tokens=False)['input_ids'])

    def frag(self, i):
        return REPL in self.dec(i)

    def content(self, i):
        s = self.dec(i)
        return n_kj(s) + n_kt(s) > 0

    def one_kata(self, i):
        s = self.dec(i)
        return n_kj(s) == 0 and n_kt(s) == 1

    def main(self, i):
        return self.content(i) and not self.one_kata(i)

    def multi(self, i):
        s = self.dec(i)
        return n_kj(s) + n_kt(s) >= 2

    def split(self, raw):
        raw = sorted(int(i) for i in raw)
        good = [i for i in raw if not self.frag(i)]
        return {'main': [i for i in good if self.main(i)], 'kata1': [i for i in good if self.content(i)], 'all': good,
                'fragments': [i for i in raw if self.frag(i)], 'multi': [i for i in good if self.multi(i)]}

    def ctype(self, i, types):
        """字の決まり（漢字〔「々」を含む〕・片仮名〔長音符を含む〕・平仮名だけ・cp932 に入る）と字の種類。外なら None。"""
        s = self.dec(i)
        if not s:
            return None
        try:
            s.encode('cp932')
        except UnicodeEncodeError:
            return None
        kind = []
        for ch in s:
            o = ord(ch)
            if KJ[0] <= o <= KJ[1] or o == NOMA:
                kind.append('K')
            elif KT[0] <= o <= KT[1] or o == BAR:
                kind.append('T')
            elif HR[0] <= o <= HR[1]:
                kind.append('H')
            else:
                return None
        if set(kind) == {'K'}:
            return types[0]
        if set(kind) == {'T'}:
            return types[1]
        return types[2]


def option_texts(scene_text):
    """場面の本文から選択肢の文を切り出す（「(a)」〜「(d)」の印の後ろから次の印まで・最後は印の後の最初の「。」まで・両端の空白と「、」を落とす）。"""
    marks = [(m.group(1), m.start(), m.end()) for m in re.finditer(r'\(([a-d])\)', scene_text)]
    out = collections.OrderedDict()
    for n, (letter, s0, s1) in enumerate(marks):
        end = marks[n + 1][1] if n + 1 < len(marks) else scene_text.index('。', s1)
        out[letter] = scene_text[s1:end].strip().rstrip('、').strip()
    return out


def load_inputs():
    TL = json.load(open(os.path.join(REPO, 'design', 'contrasts-Blens.json'), encoding='utf-8'))
    TB = json.load(open(os.path.join(REPO, 'design', 'contrasts-B.json'), encoding='utf-8'))
    import run_stageB_local as RB
    AT = RB.arm_texts()
    SCN = {sc: RB.scenario_and_instruction(sc) for sc in SCENES}
    return TL, TB, RB, AT, SCN


def trials_of(sc, arm):
    d = os.path.join(REPO, 'results', 'stageB', 'stageB__%s__%s__s1' % (sc, arm))
    tr = [json.loads(l) for l in open(glob.glob(os.path.join(d, 'trials-*.jsonl'))[0], encoding='utf-8')]
    rw = {json.loads(l)['trial_id']: json.loads(l) for l in open(glob.glob(os.path.join(d, 'raw-*.jsonl'))[0], encoding='utf-8')}
    return [(t, rw[t['trial_id']]) for t in sorted(tr, key=lambda t: t['trial_index'])]


def derive_E(W, tok_of, ctx):
    """E: 腕の前置きのトークンの集合 tok_of（腕 → 集合）と、場面の本文と指示のトークン ctx から。"""
    raw = collections.OrderedDict([('static', ((tok_of['O'] - tok_of['Osec']) - ctx, (tok_of['Osec'] - tok_of['O']) - ctx)),
                                   ('td', (tok_of['Onull'] - ctx, set())), ('Nk', (tok_of['Nk'] - ctx, set()))])
    if 'O-Ncold' in tok_of:
        raw['loaded'] = ((tok_of['O-Ncold'] - tok_of['Osec-Ncold']) - ctx, (tok_of['Osec-Ncold'] - tok_of['O-Ncold']) - ctx)
    E = collections.OrderedDict()
    for k, (p, m) in raw.items():
        sp, sm = W.split(p), W.split(m)
        E[k] = {'plus': sp['main'], 'minus': sm['main'], 'plus_kata1': sp['kata1'], 'minus_kata1': sm['kata1'], 'plus_all': sp['all'], 'minus_all': sm['all'],
                'plus_multi': sp['multi'], 'minus_multi': sm['multi'], 'fragments': sp['fragments'] + sm['fragments'],
                'single_kata_removed': sorted(set(sp['kata1']) - set(sp['main'])) + sorted(set(sm['kata1']) - set(sm['main']))}
    return E


def derive_X(W, fam, scs, options, opt_tok, stem_tok, ins_tok, arm_tok):
    """X（一つの家族）: 選択肢ごとのトークンの集合 opt_tok（選択肢 → 集合）と、印の出所（場面の幹・指示・腕の前置きのトークン）から。"""
    a_tok = set(opt_tok['a'])
    o_tok = set()
    for k, v in opt_tok.items():
        if k != 'a':
            o_tok |= set(v)
    sa, so = W.split(a_tok - o_tok), W.split(o_tok - a_tok)
    marks = collections.OrderedDict()
    for i in sa['main'] + so['main']:
        m = [n for n, S in (('stem', stem_tok), ('instr', ins_tok), ('arm', arm_tok)) if i in S]
        if m:
            marks[str(i)] = m
    return {'scenes': list(scs), 'options': options, 'a': sa['main'], 'others': so['main'], 'a_kata1': sa['kata1'], 'others_kata1': so['kata1'],
            'a_all': sa['all'], 'others_all': so['all'], 'a_multi': sa['multi'], 'others_multi': so['multi'], 'marks': marks,
            'a_unmarked': [i for i in sa['main'] if str(i) not in marks], 'others_unmarked': [i for i in so['main'] if str(i) not in marks],
            'single_kata_removed': sorted(set(sa['kata1']) - set(sa['main'])) + sorted(set(so['kata1']) - set(so['main'])),
            'fragments': len(sa['fragments']) + len(so['fragments'])}


def pick_f_main(first_json, seen, dec):
    """F の主: JSON 直答の出力の最初のトークンで最も多いもの。コードブロックの書き出しでなければ止める。"""
    f_main = max(first_json, key=lambda i: (first_json[i], -seen[i]))
    if dec(f_main) != '```':
        raise SystemExit('JSON 直答の出力の最初のトークンがコードブロックの書き出しでない: %r' % dec(f_main))
    return f_main


def families(SCN):
    by_fam = collections.OrderedDict()
    for sc in SCENES:
        by_fam.setdefault(SCN[sc][0]['family'], []).append(sc)
    return by_fam


def build_standalone(W, TL, TB, AT, SCN):
    """単独で割った集合（下書きの器と同じ規則・別に書いた）。"""
    txt = {a: AT[a]['text'] for a in ('O', 'Osec', 'Onull', 'Nk')}
    ncold = TB['arms']['ncold_text']
    instr = {sc: SCN[sc][1] for sc in SCENES}
    ctx = set()
    for sc in SCENES:
        ctx |= set(W.ids(SCN[sc][0]['text'])) | set(W.ids(instr[sc]))
    tok_of = {a: set(W.ids(t)) for a, t in txt.items()}
    E = derive_E(W, tok_of, ctx)
    arm_tok = set().union(*[set(W.ids(t)) for t in list(txt.values()) + [ncold]])
    X = collections.OrderedDict()
    for f_, scs in families(SCN).items():
        opts = [option_texts(SCN[s][0]['text']) for s in scs]
        if any(o != opts[0] for o in opts):
            raise SystemExit('同じ家族の場面で選択肢の文が違う: %s' % f_)
        stext = SCN[scs[0]][0]['text']
        X[f_] = derive_X(W, f_, scs, opts[0], {k: set(W.ids(v)) for k, v in opts[0].items()},
                         set(W.ids(stext[:stext.index('(a)')])), set(W.ids(instr[scs[0]])), arm_tok)
    # L と R
    pre = W.ids('{"choice": "')
    L = collections.OrderedDict()
    for x in ('a', 'b', 'c', 'd', 'refuse'):
        s_ = W.ids('{"choice": "%s"' % x)
        if s_[:len(pre)] != pre:
            raise SystemExit('答えの文字の前の並びが割り方で変わる: %s' % x)
        L[x] = s_[len(pre)]
    # F と、無操作の出力に現れたトークン
    first_json, first_prose, seen = collections.Counter(), collections.Counter(), {}
    noop_tokens = set()
    for sc in SCENES:
        for arm in TL['token_sets']['noop_arms'][sc]:
            for t, r in trials_of(sc, arm):
                if t['status'] != 'ok':
                    continue
                ids_ = W.ids(r['final'])
                noop_tokens |= set(ids_)
                if ids_:
                    (first_json if t['style_b'] else first_prose)[ids_[0]] += 1
                    seen.setdefault(ids_[0], len(seen))
    f_main = pick_f_main(first_json, seen, W.dec)
    echo = set()
    for t_ in list(txt.values()) + [ncold] + [SCN[sc][0]['text'] for sc in SCENES] + [instr[sc] for sc in SCENES]:
        echo |= set(W.ids(t_))
    others = set(L.values()) | {f_main}
    for k in ('static', 'td', 'Nk'):
        others |= set(E[k]['plus']) | set(E[k]['minus'])
    for f_ in X:
        others |= set(X[f_]['a']) | set(X[f_]['others'])
    ranked = sorted(first_prose, key=lambda i: (-first_prose[i], seen[i]))
    sens = [i for i in ranked if not W.frag(i) and i not in echo and i not in others][:TL['token_sets']['F_top']]
    F = {'main': int(f_main), 'sens': sens}
    E_out = collections.OrderedDict((k, E[k]) for k in ('static', 'td', 'Nk'))
    return {'L': L, 'R': L['refuse'], 'E': E_out, 'X': X, 'F': F}, noop_tokens, ctx, tok_of


def build_word_side(W, TL, sets, noop_tokens, ctx, tok_of, base_vocab, norms):
    WS = TL['nulls']['word_side']
    types, lens_ = WS['char_types'], WS['lengths']
    excl = tok_of['O'] | tok_of['Osec'] | ctx
    pool = [i for i in range(base_vocab) if i not in excl and not W.frag(i) and W.main(i) and W.ctype(i, types)]
    norms = np.asarray(norms, dtype=np.float64)            # 帯の境は float64 で取る（ノルムは float32 で計算して上げる・下書きの器と同じ数の定め）
    edges = np.quantile(norms[pool], [k / WS['norm_bands'] for k in range(1, WS['norm_bands'])])
    cell = {}
    E = sets['E']['static']
    for i in pool + E['plus'] + E['minus']:
        if i not in cell:
            if not W.ctype(i, types):
                raise SystemExit('E の語が字の決まりを満たさない: %s' % i)
            cell[i] = (W.ctype(i, types), lens_[0] if len(W.dec(i)) == 1 else lens_[1], int(np.searchsorted(edges, norms[i], side='right')))

    def groups_of(cands):
        cc = collections.Counter(cell[i] for i in cands)
        nc = collections.Counter(cell[i] for i in E['plus'] + E['minus'])
        g, ok = C.strata_groups(cc, nc, WS['norm_bands'], WS['merge_factor'])
        out = collections.OrderedDict()
        for tl, gl in g.items():
            out['%s|%s' % tl] = [[list(g_), c_, n_, sum(1 for i in E['plus'] if cell[i][:2] == tl and cell[i][2] in g_),
                                  sum(1 for i in E['minus'] if cell[i][:2] == tl and cell[i][2] in g_)] for g_, c_, n_ in gl]
        ratios = [c_ / n_ for gl in out.values() for g_, c_, n_, a_, b_ in gl if n_]
        return out, ok, (min(ratios) if ratios else None)

    strata, ok, rmin = groups_of(pool)
    if not ok:
        raise SystemExit('語の側の帰無の層が、帯を全て合わせても足りない（止める・登録者に相談）')
    sens_pool = [i for i in pool if i in noop_tokens]
    s_strata, s_ok, s_rmin = groups_of(sens_pool)
    mixed_nohira = [W.dec(i) for i in pool if cell[i][0] == types[2] and not any(HR[0] <= ord(ch) <= HR[1] for ch in W.dec(i))]
    return {'edges': [float(x) for x in edges], 'pool': pool, 'pool_n': len(pool), 'cells': {str(i): list(cell[i]) for i in sorted(cell)},
            'strata': strata, 'ratio_min': rmin, 'sens_pool': sens_pool, 'sens_pool_n': len(sens_pool), 'sens_strata': s_strata, 'sens_ok': s_ok,
            'sens_ratio_min': s_rmin, 'mixed_without_hiragana': mixed_nohira}


def embed_norms(snap, base_vocab):
    """‖g⊙W_E[t]‖（語彙の行に最終の正規化の重みを掛けたベクトルのノルム・bf16 を float32 に上げる）。"""
    from safetensors import safe_open
    idx = json.load(open(os.path.join(snap, 'model.safetensors.index.json'), encoding='utf-8'))
    with safe_open(os.path.join(snap, idx['weight_map']['model.norm.weight']), framework='pt') as fh:
        g = fh.get_tensor('model.norm.weight').float().numpy()
    out = np.zeros(base_vocab, dtype=np.float32)
    step = 1 << 13
    with safe_open(os.path.join(snap, idx['weight_map']['model.embed_tokens.weight']), framework='pt') as fh:
        sl = fh.get_slice('model.embed_tokens.weight')
        for s0 in range(0, base_vocab, step):
            s1 = min(base_vocab, s0 + step)
            out[s0:s1] = np.linalg.norm(sl[s0:s1].float().numpy() * g[None, :], axis=1)
    return out


def in_prompt(W, RB, AT, SCN):
    """組み立てたプロンプトの中で割ったトークン（裁定 D184）。各場面の各腕のプロンプトで、前置き・場面の幹・選択肢の文・指示の字の範囲に
    すっぽり入るトークンを集める。範囲にまたがるトークンは印字する。"""
    import steer_B
    inside = collections.defaultdict(dict)                                   # 腕 → 場面 → 前置きのトークン
    ctx_in, straddle = set(), []
    opt_in = collections.defaultdict(lambda: collections.defaultdict(dict))  # 家族 → 選択肢 → 場面 → トークン
    stem_in, ins_in = collections.defaultdict(dict), collections.defaultdict(dict)
    fam = {sc: SCN[sc][0]['family'] for sc in SCENES}
    for sc in SCENES:
        scen, inst = SCN[sc]
        opts = option_texts(scen['text'])
        for arm in ARMS_E:
            text = AT[arm]['text']
            um = RB.user_message(text, scen['text'], inst)
            ids_chat = steer_B.apply_chat(W.tok, um)
            s = W.tok.apply_chat_template([{'role': 'user', 'content': um}], add_generation_prompt=True, tokenize=False)
            enc = W.tok(s, add_special_tokens=False, return_offsets_mapping=True)
            if list(enc['input_ids']) != list(ids_chat):
                raise SystemExit('chat template の文字列を割った列が、段階 B の組み立ての列と違う: %s %s' % (sc, arm))
            p0 = s.index(um)
            s0 = p0 + len(text) + 2
            spans = collections.OrderedDict([('pre', (p0, p0 + len(text))), ('stem', (s0, s0 + scen['text'].index('(a)')))])
            for letter, ot in opts.items():
                o0 = s0 + scen['text'].index(ot)
                spans['opt_' + letter] = (o0, o0 + len(ot))
            spans['scene'] = (s0, s0 + len(scen['text']))
            spans['instr'] = (s0 + len(scen['text']), s0 + len(scen['text']) + len(inst))
            if s[spans['scene'][0]:spans['scene'][1]] != scen['text'] or s[spans['instr'][0]:spans['instr'][1]] != inst:
                raise SystemExit('プロンプトの中の場面の本文か指示の位置が合わない: %s %s' % (sc, arm))
            got = collections.defaultdict(set)
            for i, (a0, a1) in zip(enc['input_ids'], enc['offset_mapping']):
                for name, (b0, b1) in spans.items():
                    if b0 <= a0 and a1 <= b1:
                        got[name].add(int(i))
                    elif a0 < b1 and b0 < a1:
                        straddle.append((sc, arm, name, int(i), W.dec(i)))
            inside[arm][sc] = got['pre']
            ctx_in |= got['scene'] | got['instr']
            if arm == 'O':
                for letter in opts:
                    opt_in[fam[sc]][letter][sc] = got['opt_' + letter]
                stem_in[fam[sc]][sc], ins_in[fam[sc]][sc] = got['stem'], got['instr']
    per_scene_equal = {arm: all(inside[arm][sc] == inside[arm][SCENES[0]] for sc in SCENES) for arm in ARMS_E}
    opt_equal = {f_: all(all(v == list(d.values())[0] for v in d.values()) for d in opt_in[f_].values()) for f_ in opt_in}
    return {'pre': {arm: inside[arm][SCENES[0]] for arm in ARMS_E}, 'ctx': ctx_in, 'opt': opt_in, 'stem': stem_in, 'instr': ins_in,
            'straddle': straddle, 'per_scene_equal': per_scene_equal, 'options_equal': opt_equal}


def canon_form(sets, ws):
    """下書きの器と比べる正本の形（単独で割った集合と語の側の帰無の層）。"""
    E = {k: {f: sets['E'][k][f] for f in E_FIELDS} for k in ('static', 'td', 'Nk')}
    X = {f_: {k: v for k, v in x.items() if k != 'fragments'} for f_, x in sets['X'].items()}
    return {'L': dict(sets['L']), 'E': E, 'X': X, 'F': {'main': sets['F']['main'], 'sens': sets['F']['sens']},
            'word_side': {'pool_n': ws['pool_n'], 'strata': ws['strata'], 'sens_pool_n': ws['sens_pool_n'], 'sens_strata': ws['sens_strata']}}


def facts_form(FJ):
    B, H = FJ['facts']['B'], FJ['facts']['H']
    E = {k: {f: B['E'][k][f] for f in E_FIELDS} for k in ('static', 'td', 'Nk')}
    X = {f_: {k: v for k, v in x.items() if k != 'fragments'} for f_, x in B['X'].items()}
    return {'L': dict(B['L']), 'E': E, 'X': X, 'F': {'main': B['F']['main'], 'sens': B['F']['prose_sens']},
            'word_side': {'pool_n': H['pool'], 'strata': H['strata'], 'sens_pool_n': H['sensitivity']['pool'], 'sens_strata': H['sensitivity']['strata']}}


def compare_in_prompt(W, sets, IP, SCN):
    """組み立てた中の集合を作り、単独の集合と比べる。戻り値: (組み立てた中の E・X, 違い)。"""
    E_ip = derive_E(W, IP['pre'], IP['ctx'])
    arm_tok = set().union(*IP['pre'].values())
    X_ip = collections.OrderedDict()
    for f_, scs in families(SCN).items():
        sc0 = scs[0]
        opt_tok = {letter: IP['opt'][f_][letter][sc0] for letter in IP['opt'][f_]}
        X_ip[f_] = derive_X(W, f_, scs, sets['X'][f_]['options'], opt_tok, IP['stem'][f_][sc0], IP['instr'][f_][sc0], arm_tok)
    diffs = collections.OrderedDict()
    for k in ('static', 'td', 'Nk', 'loaded'):
        ref = sets['E']['static' if k == 'loaded' else k]
        for side in ('plus', 'minus'):
            got, want = E_ip[k][side], ref[side]
            if got != want:
                diffs['E_%s_%s' % (k, side)] = {'in_prompt_only': sorted(set(got) - set(want)), 'standalone_only': sorted(set(want) - set(got))}
    for f_ in X_ip:
        for side in ('a', 'others'):
            got, want = X_ip[f_][side], sets['X'][f_][side]
            if got != want:
                diffs['X_%s_%s' % (f_, side)] = {'in_prompt_only': sorted(set(got) - set(want)), 'standalone_only': sorted(set(want) - set(got))}
    return E_ip, X_ip, diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--tokenizer', default=os.environ.get('OP4B_TOKENIZER_DIR') or SNAP)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if os.path.exists(OUT_JSON) and not a.force:
        raise SystemExit('既にある（凍結の集合は一度だけ作る・作り直すなら --force）: %s' % rel(OUT_JSON))
    from transformers import AutoTokenizer
    TL, TB, RB, AT, SCN = load_inputs()
    tok = AutoTokenizer.from_pretrained(a.tokenizer)
    W = Words(tok)
    base_vocab = min(tok.added_tokens_decoder.keys())
    if base_vocab != TL['inputs']['model']['base_vocab'] or len(tok) != TL['inputs']['model']['tokenizer_len']:
        raise SystemExit('トークナイザの語彙の数が正本と違う: %s %s' % (base_vocab, len(tok)))
    for arm in ('O', 'Osec', 'Onull', 'Nk'):
        if AT[arm]['sha16'] != TB['arms']['sha16'][arm]:
            raise SystemExit('腕の本文の SHA16 が段階 B の正本と違う: %s' % arm)
    sets, noop_tokens, ctx, tok_of = build_standalone(W, TL, TB, AT, SCN)
    norms = embed_norms(a.tokenizer, base_vocab)
    ws = build_word_side(W, TL, sets, noop_tokens, ctx, tok_of, base_vocab, norms)
    # 単独で割った集合を、下書きの器とバイトで突き合わせる
    FJ = json.load(open(FACTS, encoding='utf-8'))
    mine, theirs = dumps(canon_form(sets, ws)), dumps(facts_form(FJ))
    equal = mine == theirs
    if not equal:
        diff = [k for k in json.loads(mine) if json.loads(mine)[k] != json.loads(theirs).get(k)]
        raise SystemExit('下書きの器の集合とバイトで一致しない（止める・登録者に相談）: 違う欄 %s' % diff)
    # 組み立てたプロンプトの中で割った集合（裁定 D184）
    IP = in_prompt(W, RB, AT, SCN)
    if not all(IP['per_scene_equal'].values()) or not all(IP['options_equal'].values()):
        raise SystemExit('組み立てた中の集合が場面によって違う（止める・登録者に相談）: %s %s' % (IP['per_scene_equal'], IP['options_equal']))
    E_ip, X_ip, diffs = compare_in_prompt(W, sets, IP, SCN)
    primary = json.loads(json.dumps(sets))
    standalone = None
    if diffs:                           # 裁定 D184: 組み立てた中の集合を主にし、単独の集合を感度にして、続ける
        standalone = json.loads(json.dumps(sets))
        primary['E'] = json.loads(json.dumps(collections.OrderedDict((k, E_ip[k]) for k in ('static', 'td', 'Nk'))))
        primary['X'] = json.loads(json.dumps(X_ip))
    primary['E']['loaded'] = primary['E']['static']        # (6b) の二腕は Ncold の一行を共有するので、違う語は O と Osec の差と同じ（正本 token_sets.E）
    T = {'kind': 'blens_sets', 'version': VERSION, 'generated_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),
         'contrasts_sha16': sha16f(os.path.join(REPO, 'design', 'contrasts-Blens.json')),
         'tokenizer': {'snapshot': os.path.basename(a.tokenizer.rstrip('/\\')), 'tokenizer_json_sha256': hashlib.sha256(open(os.path.join(a.tokenizer, 'tokenizer.json'), 'rb').read()).hexdigest().upper(),
                       'base_vocab': base_vocab, 'len': len(tok)},
         'sets': primary, 'sets_standalone': standalone, 'word_side': ws,
         'checks': {'facts_equal': equal, 'facts_sha16': sha16f(FACTS), 'canonical_sha256': hashlib.sha256(mine.encode('utf-8')).hexdigest().upper(),
                    'in_prompt_differences': diffs, 'in_prompt_straddle': [list(x) for x in IP['straddle']],
                    'in_prompt_per_scene_equal': IP['per_scene_equal'], 'in_prompt_options_equal': IP['options_equal']},
         'clause': '本記録のいかなる数値も AI の意識・意図・個性・魂・苦しみがある（またはない）ことの証拠として引用してはならない（両方向不定）。'}
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump(T, open(OUT_JSON, 'w', encoding='utf-8', newline=NL), ensure_ascii=False, indent=1)
    show = lambda L_: '・'.join('%d「%s」' % (i, W.dec(i).replace(NL, '⏎')) for i in L_)
    st = collections.Counter((x[2], x[3]) for x in IP['straddle'])
    md = ['# B-lens の凍結の語の集合（機械生成・`tools/blens_sets.py` %s・%s UTC）' % (VERSION, T['generated_utc']), '',
          '- 正本 `design/contrasts-Blens.json` SHA16 %s・トークナイザ `tokenizer.json` SHA-256 %s。' % (T['contrasts_sha16'], T['tokenizer']['tokenizer_json_sha256']),
          '- 単独で割った集合は、下書きの器の集合（`records/Blens/design-facts-Blens.json` SHA16 %s）と、正本の形に並べた JSON がバイトで一致: %s（SHA-256 %s）。' % (T['checks']['facts_sha16'], '一致' if equal else '不一致', T['checks']['canonical_sha256']),
          '- 組み立てたプロンプトの中で割った集合と単独で割った集合の違い（裁定 D184）: %s。%s組み立てた中の集合は四つの場面で同じ: %s。' % (
              ('／'.join('%s（組み立てた中だけ %s・単独だけ %s）' % (k, show(v['in_prompt_only']) or '無し', show(v['standalone_only']) or '無し') for k, v in diffs.items()) or '無し'),
              '違ったので、組み立てた中の集合を主にし、単独の集合を感度（`sets_standalone`）にした。' if diffs else '',
              '同じ' if all(IP['per_scene_equal'].values()) and all(IP['options_equal'].values()) else '違う'),
          '- 字の範囲にまたがったトークン（範囲 × トークン・場面と腕を通した件数）: %s。' % ('・'.join('%s %s %d' % (n, show([i]), c) for (n, i), c in sorted(st.items())) or '無し'),
          '- 主の集合: E+（v̂）%d・E−（v̂）%d・td %d・Nk %d／X: %s／F の主 %s・F の感度 %s。' % (
              len(primary['E']['static']['plus']), len(primary['E']['static']['minus']), len(primary['E']['td']['plus']), len(primary['E']['Nk']['plus']),
              '・'.join('%s の X_a %d・X_o %d' % (f_, len(x['a']), len(x['others'])) for f_, x in primary['X'].items()), show([primary['F']['main']]), show(primary['F']['sens'])),
          '- 語の側の帰無の候補 %d（感度の候補 %d）・要る数に対する候補の数の比の最小 %.1f（感度 %s）。' % (ws['pool_n'], ws['sens_pool_n'], ws['ratio_min'], ('%.1f' % ws['sens_ratio_min']) if ws['sens_ratio_min'] else '—'),
          '- 集合は射影を一つも計算する前に作った（語彙の行列は行のノルムだけを使い、方向とは掛けていない）。', '', T['clause'], '']
    open(OUT_MD, 'w', encoding='utf-8', newline=NL).write(NL.join(md))
    print('wrote %s・%s | facts_equal %s | in-prompt diffs %d | straddle %d' % (rel(OUT_JSON), rel(OUT_MD), equal, len(diffs), len(IP['straddle'])))


def _selftest():
    assert option_texts('前の文 (a)甲をする、(b)乙をする、(c)何もしない。後') == collections.OrderedDict([('a', '甲をする'), ('b', '乙をする'), ('c', '何もしない')])

    class FakeTok:
        added_tokens_decoder = {10: None}
        V = {0: '核', 1: 'ス', 2: 'して', 3: REPL, 4: '口コミ', 5: 'ヶ月', 6: '人々', 7: 'abc', 8: 'スト', 9: '々'}

        def decode(self, ids):
            return ''.join(self.V[i] for i in ids)
    W = Words(FakeTok())
    types = ['漢字だけ', '片仮名だけ', 'かなまじり']
    assert W.main(0) and not W.main(1) and not W.main(2) and W.frag(3) and W.main(4)
    assert W.ctype(4, types) == 'かなまじり' and W.ctype(5, types) == 'かなまじり' and W.ctype(6, types) == '漢字だけ' and W.ctype(7, types) is None
    assert W.ctype(8, types) == '片仮名だけ' and W.main(8) and not W.content(9)
    sp = W.split({0, 1, 2, 3, 8})
    assert sp['main'] == [0, 8] and sp['kata1'] == [0, 1, 8] and sp['fragments'] == [3] and sp['multi'] == [8]
    x = derive_X(W, 'f', ['S'], {'a': 'x', 'b': 'y'}, {'a': {0, 8, 3}, 'b': {8, 4}}, {0}, set(), set())
    assert x['a'] == [0] and x['others'] == [4] and x['marks'] == {'0': ['stem']} and x['a_unmarked'] == [] and x['fragments'] == 1
    print('[blens_sets] 自己検査 OK（%s）' % VERSION)


if __name__ == '__main__':
    main()
